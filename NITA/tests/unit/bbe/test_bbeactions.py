import unittest
import builtins
from mock import patch, MagicMock
from jnpr.toby.bbe.bbeactions import BBEActions
from jnpr.toby.bbe.bbevar.bbevars import BBEVars
from jnpr.toby.hldcl.system import System
from jnpr.toby.hldcl.device import Device
#from jnpr.toby.init.init import init



class TestBBEActions(unittest.TestCase):
    """
    TestBBEActions class to handle bbeactions.py unit tests
    """
    def setUp(self):
        builtins.t = MagicMock()

        builtins.t.log = MagicMock()

        builtins.bbe = MagicMock()
        self.rthandle = MagicMock()
        builtins.t.get_handle.return_value = self.rthandle


    @patch('re.search')
    @patch('time.sleep')
    def test_restart_daemons(self, patch_sleep, patch_search):
        self.rthandle.invoke.return_value = {'status': '1'}
        try:
            BBEActions().restart_daemons()
        except Exception as err:
            self.assertEqual(err.args[0], 'Device information not given')
        try:
            BBEActions().restart_daemons(device='r0')
        except Exception as err:
            self.assertTrue('Daemon Restart Failed!' in err.args[0])
        try:
            daemons = {'dhcp-service', 'unkow-service'}
            BBEActions().restart_daemons(device='r0', skip_daemons={'dhcp-service'}, daemons=daemons)
        except Exception as err:
            self.assertTrue('Unknown daemon' in err.args[0])

        patch_search.return_value = False
        self.assertIsInstance(BBEActions().restart_daemons(device='r0'), dict)
        self.assertIsInstance(BBEActions().restart_daemons(device='r0', restart_method='soft'), dict)
        patch_search.return_value = MagicMock()
        patch_search.return_value.group.side_effect = ['10', '20']
        self.assertIsInstance(BBEActions().restart_daemons(device='r0', daemons={'dhcp-service'}), dict)
        patch_search.return_value.group.side_effect = None

    @patch('time.sleep')
    @patch('re.search')
    def test_gres_by_routing_engine_master_switch(self, patch_search, patch_sleep):
        try:
            BBEActions().gres_by_routing_engine_master_switch()
        except Exception as err:
            self.assertEqual(err.args[0], 'Device information not given')
        try:
            BBEActions().gres_by_routing_engine_master_switch(device='r0')
        except Exception as err:
            self.assertTrue('Database Replication - Not Synchronized' in err.args[0])
        builtins.t.get_handle.return_value.is_master.return_value = False
        patch_search.return_value = None
        try:
            BBEActions().gres_by_routing_engine_master_switch(device='r0')
        except Exception as err:
            self.assertTrue('Routing Engine is not ready for master switch even after maximum wait' in err.args[0])
        patch_search.return_value = True
        obj1 = MagicMock()
        obj1.text = 'Enabled'
        obj3 = MagicMock()
        obj3.text = 'Synchronized'
        builtins.t.get_handle.return_value.execute_rpc.return_value.response.return_value = [obj1, 'obj1', 'obj2', obj3]
        try:
            BBEActions().gres_by_routing_engine_master_switch(device='r0')
        except Exception as err:
            self.assertEqual(err.args[0], 'GRES by master switch Failed!')
        patch_search.side_effect = [True, False]
        builtins.t.get_handle.return_value.is_master.return_value = True
        self.assertEqual(BBEActions().gres_by_routing_engine_master_switch(device='r0'), True)
        patch_search.side_effect = None
        builtins.t.get_handle.return_value.execute_rpc.return_value.response.return_value = MagicMock()

    @patch('re.search')
    @patch('time.sleep')
    def test_restart_fpc(self, patch_sleep, patch_search):
        try:
            BBEActions().restart_fpc()
        except Exception as err:
            self.assertEqual(err.args[0], 'Device information not given for restart of fpc')
        try:
            BBEActions().restart_fpc(device='r0')
        except Exception as err:
            self.assertEqual(err.args[0], 'No slots information passed in argument to restart fpc')

        builtins.t.get_handle.return_value.execute_rpc.return_value.response.return_value.\
            findtext.return_value = 'Online'
        self.assertEqual(BBEActions().restart_fpc(device='r0', slots=['1']), None)
        builtins.t.get_handle.return_value.execute_rpc.return_value.response.return_value.\
            findtext.return_value = 'Offline'
        try:
            BBEActions().restart_fpc(device='r0', slots=['1'])
        except Exception as err:
            self.assertEqual(err.args[0], 'FPC Restart failed, not all slots are back online')

    def test_login_ppp_subscribers(self):
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
        self.assertEqual(BBEActions().login_ppp_subscribers(), True)
        self.assertEqual(BBEActions().login_ppp_subscribers(tag='al'), True)

    def test_logout_ppp_subscribers(self):
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
        self.assertEqual(BBEActions().logout_ppp_subscribers(), True)
        self.assertEqual(BBEActions().logout_ppp_subscribers(tag='al'), True)

    def test_collect_debug_information(self):
        builtins.bbe.get_devices.return_value = [MagicMock()]
        self.assertEqual(BBEActions().collect_debug_information(), True)

    @patch('jnpr.toby.engines.config.config.config.CONFIG_SET')
    def test_enable_daemon_traceoptions(self, patch_config):
        builtins.bbe.get_devices.return_value = [MagicMock()]
        builtins.bbe.bbevar = {'debug': {'user-debug-logs': ['ancpd', 'authd', 'autoconfd', 'bbesmgd', 'chassisd',
                                                             'cosd', 'dfcd', 'dcd', 'dfwd', 'jdhcpd', 'jpppd', 'jl2tpd',
                                                             'ksyncd', 'lacpd', 'messages', 'pfed', 'pppd', 'pppoed',
                                                             'relayd', 'smid', 'snmpd', 'rpd', 'vccpd']}}
        patch_config.return_value = True

        self.assertEqual(BBEActions().enable_daemon_traceoptions(), True)

    @patch('os.system')
    @patch('jnpr.toby.hldcl.device.Device.__new__')
    @patch('time.sleep')
    @patch('re.findall')
    def test_collect_debug_event(self, patch_find, patch_sleep, patch_device, patch_os):
        builtins.bbe.get_devices.return_value = [MagicMock()]
        patch_find.return_value = ["1"]
        builtins.t.get_resource.return_value = {'system': {'primary': {'controllers': {'re0':{}}}}}
        patch_device.return_value = MagicMock()
        patch_device.return_value.upload.return_value = True
        patch_device.return_value.close.return_value = True
        builtins.t.get_handle.return_value = MagicMock()
        builtins.t.get_handle.return_value.cli.return_value = MagicMock()
        builtins.t.get_handle.return_value.shell.return_value = MagicMock()
        self.assertEqual(BBEActions().collect_debug_event('r0'), None)
        patch_device.return_value.upload.side_effect = Exception
        self.assertEqual(BBEActions().collect_debug_event('r0'), None)
        patch_device.return_value.upload.side_effect = None
        builtins.t.get_handle.return_value.download.side_effect = Exception
        self.assertEqual(BBEActions().collect_debug_event('r0'), None)
        builtins.t.get_handle.return_value.download.side_effect = None


if __name__ == '__main__':
    unittest.main()
