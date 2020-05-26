import unittest2 as unittest
import builtins
from mock import patch, Mock, MagicMock, call
from jnpr.toby.init.init import init
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.juniper.junos import Juniper
import jnpr.toby.hardware.chassis.chassis as chassis
import jnpr.toby.engines.events.event_engine_utils as eutil
import jnpr.toby.utils.triggers as triggers
from jnpr.toby.engines.events.event_engine_utils import cli_pfe


class TestTriggers(unittest.TestCase):

    def setUp(self):
        import builtins
        #builtins.t = self
        builtins.t = MagicMock(spec=init)
        t.log = MagicMock(return_value=True)
        t.log_console = MagicMock(return_value=True)

    def test_on_cli(self):
        dh = MagicMock()
        # cli returned successfully
        dh.cli.return_value = Response(status=True, response='test')
        self.assertTrue(triggers.on_cli(dh, 'show chassis alarm'))

        # cli returned syntax error
        dh.cli.return_value = Response(status=True, response='syntax error')
        self.assertFalse(triggers.on_cli(dh, 'show chassis alarm'))

        # cli returned status False
        dh.cli.return_value = Response(status=False, response='anything')
        self.assertFalse(triggers.on_cli(dh, 'show chassis alarm'))

        dh.cli.side_effect = Exception
        self.assertFalse(triggers.on_cli(dh, 'show chassis alarm'))

    def test_on_config(self):
        dh = MagicMock()
        # config returned successfully
        dh.config.return_value = Response(status=True, response='test')
        self.assertTrue(triggers.on_config(dh, 'set this'))

        # config returned syntax error
        dh.config.return_value = Response(status=True, response='syntax error')
        self.assertFalse(triggers.on_config(dh, 'set this'))

        # config returned status False
        dh.config.return_value = Response(status=False, response='anything')
        self.assertFalse(triggers.on_config(dh, 'set this'))

        dh.config.side_effect = Exception
        self.assertFalse(triggers.on_config(dh, 'set this'))

    def test_on_shell(self):
        dh = MagicMock()
        # cli returned successfully
        dh.shell.return_value = Response(status=True, response='test')
        self.assertTrue(triggers.on_shell(dh, 'ls'))

        # no shell method
        try:
            triggers.on_shell(dh, 'suu()')
        except:
            assertRaises(Exception)

        # shell method:
        dh.su = MagicMock(side_effect=Exception)
        self.assertFalse(triggers.on_shell(dh, 'su()'))

    def test_on_vty(self):
        dh = MagicMock()
        # cli returned successfully
        dh.get_model = MagicMock(return_value='mx80')
        dh.vty.return_value = Response(status=True, response='test')
        self.assertTrue(triggers.on_vty(dh, 'show version', 'xe-0/0/0'))

        # no method
        try:
            triggers.on_vty(dh, 'suu()', 'xe-0/0/0')
        except:
            assertRaises(Exception)

        # method call:
        dh.cprod = MagicMock(side_effect=Exception)
        self.assertFalse(triggers.on_vty(dh, 'cprod()', 'xe-0/0/0'))
        
    @patch('jnpr.toby.utils.triggers._check_vmhost', return_value='True')
    @patch('jnpr.toby.hardware.chassis.chassis.function_name', return_value='red')
    @patch('jnpr.toby.utils.triggers._check_master_re', return_value='True')
    @patch('jnpr.toby.utils.triggers._check_daemon', return_value='3')
    def test_kill_daemon(self, check_daemon_mock, check_master_re_mock, func_name_mock, check_vmhost_mock):
        dh = MagicMock()
        dh.get_model = MagicMock(return_value='mx80')
        dh.shell.return_value = Response(status=True, response='ok')
        dh.su.return_value = True


        check_daemon_mock.side_effect =[None, 1, 2, 111, 222, 44, 44, 3, 3]
        check_master_re_mock.return_value = True
        check_vmhost_mock.return_value = True

        dh.get_current_controller_name.return_value = 're0'
        dh.set_current_controller.return_value = False

        # no process
        self.assertFalse(triggers.kill_daemon(dh, daemon='wrong'))

        self.assertTrue(triggers.kill_daemon(dh, daemon='rpd'))

        dh.get_model = MagicMock(return_value='qfx10002-60C')
        self.assertTrue(triggers.kill_daemon(dh, daemon='dcpfe'))


    @patch('jnpr.toby.hardware.chassis.chassis.function_name', return_value='red')
    @patch('jnpr.toby.utils.triggers._check_master_re', return_value='True')
    @patch('jnpr.toby.utils.triggers._check_daemon', return_value='3')
    def test_restart_process(self, check_daemon_mock, check_master_re_mock, func_name_mock):
        dh = MagicMock()

        # process is None
        #self.assertFalse(restart_process(dh, process=None))

        # no process
        #self.assertFalse(restart_process(dh, process='wrong'))

        #check_daemon_mock.side_effect =[1, 2, 111, 222, 44, 44, 11, 5, 9, 88, 45, 46]
        check_master_re_mock.return_value = True

        dh.get_current_controller_name.return_value = 're0'
        dh.set_current_controller.return_value = False

        self.assertTrue(triggers.restart_process(dh, process='kernel-replication'))

        dh.get_current_controller_name.return_value = 're1'
        dh.cli.return_value = Response(status= False, response='syntax error')
        self.assertTrue(triggers.restart_process(dh, process='kernel-replication', option='soft'))

        check_master_re_mock.return_value = False
        self.assertTrue(triggers.restart_process(dh, process='kernel-replication'))

        # no pid
        check_master_re_mock.return_value = True
        dh.cli.return_value = Response(status= True, response='123')
        self.assertTrue(triggers.restart_process(dh, process='interface-control'))

        self.assertTrue(triggers.restart_process(dh, process='chassis-control'))


        # syntax error in method name
        dh.cli.return_value = Response(status=True, response='syntax error')
        #self.assertFalse(triggers.restart_process(dh, process='snmp'))
        self.assertFalse(triggers.restart_process(dh, process='snmp',force_restart_process=True))

        #dual_re= True
        dh.cli.return_value = Response(status= True, response='123')
        check_master_re_mock.return_value = False
        dh.get_current_controller_name.return_value = 're0'
        dh.set_current_controller.return_value = True
        self.assertTrue(triggers.restart_process(dh, process='kernel-replication'))
        dh.get_current_controller_name.return_value = 're1'
        self.assertTrue(triggers.restart_process(dh, process='kernel-replication'))

        # handle exception from hldcl
        dh.cli.side_effect = Exception
        self.assertFalse(triggers.restart_process(dh, process='snmp'))

    @patch('jnpr.toby.hardware.chassis.chassis.function_name', return_value='sub')
    def test_change_config_state(self, fun_name):
        dh = MagicMock()
        dh.get_model.return_value = 'mx380'
        dh.config.return_value = True
        dh.commit.return_value = True
        config = 'protocols'
        act = 'deactivate'
        self.assertTrue(triggers.change_config_state(dh, action=act, config=config))

    @patch('jnpr.toby.utils.triggers._check_vmhost', return_value='True')
    def test__check_daemon(self,check_vmhost_mock):
        dh = MagicMock()
        check_vmhost_mock.return_value = False
        dh.cli.return_value = Response(status=True, \
            response=' 4598 root        3  20    0   860M 55640K kqread   3:05   0.00% rpd')

        self.assertTrue(triggers._check_daemon(dh, daemon='rpd', mode='cli'))
        self.assertFalse(triggers._check_daemon(dh, daemon='wrong', mode='cli'))


    def test__check_master_re(self):
        dh = MagicMock()
        dh.shell.side_effect = [Response(status=True, response='hw.re.mastership: 1'),
                                Response(status=True, response='something')]
        self.assertTrue(triggers._check_master_re(dh))
        self.assertFalse(triggers._check_master_re(dh))


if __name__ == '__main__':
    unittest.main()

