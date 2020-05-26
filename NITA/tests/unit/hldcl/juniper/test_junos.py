import sys

import unittest
from lxml import etree
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hldcl.juniper.junos import Junos
from lxml import etree
from jnpr.toby.utils.response import Response

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

@attr('unit')
class TestJunos(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = self
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()
       
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper')
    @patch('jnpr.toby.hldcl.juniper.routing.mxvc.MxVc')
    @patch('jnpr.toby.hldcl.juniper.routing.mx.Mx')
    @patch('jnpr.toby.hldcl.juniper.security.srx.Srx')
    @patch('logging.FileHandler')
    def test_junos_new(self, mjunos, Mxvc, Mx, Srx, log_mock):
        self.assertRaises(Exception, Junos, 'device-a')
        # check for no host
        self.assertRaises(Exception, Junos)
        # model as MXVC
        self.assertIsInstance(Junos(host='device-a', model='MXVC'), MagicMock)
        # model as MX
        self.assertIsInstance(Junos(host='device-a', model='MX'), MagicMock)
        # model as M
        self.assertIsInstance(Junos(host='device-a', model='M'), MagicMock)
        # model as SRX
        self.assertIsInstance(Junos(host='device-a', model='SRX'), MagicMock)
        self.assertIsInstance(Junos(host='device-a', os=''), MagicMock)
        self.assertIsInstance(Junos(host='device-a', os='junos', connect_mode='console', dual_re=True), MagicMock)

#    @patch('jnpr.toby.hldcl.juniper.junos.Pyez_Device')
#    @patch('jnpr.toby.hldcl.juniper.junos.Junos._get_credentials',
#           return_value=[1, 2])
#    @patch('logging.FileHandler')
#    def test_junos_connect(self, pyezdevice, log_mock):
#
#        pyezdevice.open.return_value = MagicMock
#        self.assertIsInstance(Junos._connect('device-a'), MagicMock)
#        # host not provided
#        self.assertRaises(Exception, Junos._connect)
#        # connect mode is telnet
#        self.assertIsInstance(Junos._connect('test', connect_mode='telnet'),
#                              MagicMock)
#        # Invalid connect_mode
#        self.assertRaises(Exception, Junos._connect, 'test',
#                          connect_mode='what')
#        # connect mode is ssh
#        self.assertIsInstance(Junos._connect('test', connect_mode='ssh'),
#                              MagicMock)

#    @patch('logging.FileHandler')
#    def test_junos_conect_failures(self, log_mock):
        # Exceptions
#        self.assertRaises(Exception, Junos._connect, 'device-a', MagicMock)

#    def test_junos_get_credentials_failures(self):
#        # username or password cannot be determined
#        self.assertRaises(Exception, Junos._get_credentials)

#    @patch('jnpr.toby.frameworkDefaults.credentials.JUNOS')
#    def test_junos_get_credentials(self, pjunos):
#        self.assertIsInstance(Junos._get_credentials(), tuple)
#        self.assertEqual(Junos._get_credentials(
#            user='test', password='test123'), ('test', 'test123'))

#    def test_junos_is_vc_capable(self):
#        handle = MagicMock()
#
#        # vc_capable NOT in facts and virtual chassis info is retrieved
#        self.assertTrue(Junos._is_vc_capable(handle))
#        # vc_capable present in facts
#        handle.configure_mock(**{'facts': {'vc_capable': False}})
#        self.assertFalse(Junos._is_vc_capable(handle))
#
#        handle.facts = {}
#        self.assertTrue(Junos._is_vc_capable(handle))
#        handle.rpc.get_virtual_chassis_information = MagicMock(return_value=True)
#        self.assertFalse(Junos._is_vc_capable(handle))
#        handle.rpc.get_virtual_chassis_information = MagicMock(side_effect=True)
#        self.assertFalse(Junos._is_vc_capable(handle))
        # TODO: vc_capable NOT in facts and retrieving vc info gives exception

#    def test_junos_get_model(self):
#        handle = MagicMock()
#        # Non VC case
#        xmldata = etree.XML('<software-information></software-information>')
#        handle.rpc.get_software_information = MagicMock(return_value=xmldata)
#        #self.assertEqual(Junos._get_model(handle), 'JUNOS')
#        self.assertRaises(Exception, Junos._get_model, handle)
#        # MX case
#        xmldata = etree.XML('<software-information><product-model>mx240</product-model></software-information>')
#        handle.rpc.get_software_information = MagicMock(return_value=xmldata)
#        self.assertEqual(Junos._get_model(handle), 'MX')
#        # default case
#        xmldata = etree.XML('<software-information><product-model>MM240</product-model></software-information>')
#        handle.rpc.get_software_information = MagicMock(return_value=xmldata)
#        self.assertEqual(Junos._get_model(handle), 'MM')
#        # unsupported model definition
#        xmldata = etree.XML('<software-information><product-model>77</product-model></software-information>')
#        handle.rpc.get_software_information = MagicMock(return_value=xmldata)
#        self.assertRaises(Exception, Junos._get_model, handle)
#        # VC case
#        xmldata=etree.XML(
#            '<multi-routing-engine-results><multi-routing-engine-item>'
#            '<software-information><product-model>mx240</product-model>'
#            '</software-information></multi-routing-engine-item>'
#            '</multi-routing-engine-results>'
#        )
#        handle.rpc.get_software_information = MagicMock(return_value=xmldata)
#        self.assertEqual(Junos._get_model(handle), 'MXVC')

    #@patch('jnpr.toby.hldcl.juniper.junos.Pyez_Device')
    #@patch('jnpr.toby.hldcl.juniper.junos.Juniper.re_slot_name', return_value='RE0') # I am here

    @patch('jnpr.toby.hldcl.juniper.junos.Juniper.shell')
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper.cli')
    @patch('jnpr.toby.hldcl.juniper.junos.TelnetConn')
    @patch('jnpr.toby.hldcl.juniper.junos.Pyez_Device')
    @patch('logging.FileHandler')
    @patch('logging.getLogger')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')
    def test_juniper_connect(self, host_log_patch, get_logger_patch, file_handle_patch, pyez_patch,
                             telnet_patch, cli_patch, shell_patch):
        cli_patch.return_value.response.return_value = "\'read-only\'"
        shell_patch.return_value.response.return_value = "20180201 11:13:09"
        self.assertIsInstance(
            Juniper('device-a', user='test', password='test123', host='host1', connect_channels="text",
            re_name='re0', global_logging=True, device_logging=True), Juniper
        )
        ## Added code to test text_port and pyez_port arguments

        self.assertIsInstance(
            Juniper('device-a', user='test', password='test123', host='host1', connect_channels="text", text_port=22,
             re_name='re0', global_logging=True, device_logging=True), Juniper
        )
        self.assertIsInstance(
            Juniper('device-a', user='test', password='test123', host='host1', pyez_port=22,
             re_name='re0', global_logging=True, device_logging=True), Juniper
        )
        # host not passed passed
        self.assertRaises(Exception, Juniper)
        # dual_re and routing_engine passed together
        self.assertRaises(
            Exception,
            Juniper, ('device-a',), {'dual_re': True, 'routing_engine': 'backup'}
        )

#    @patch('jnpr.toby.hldcl.juniper.junos.Juniper')
#    def test_juniper_open(self, junosp):
#        # master case, dual re case
#        jobject = MagicMock(spec=Juniper)
#        jobject._is_master = MagicMock(return_value=True)
#        jobject.re = 'RE0'
#        jobject._get_other_re_name = MagicMock(return_value='RE1')
#        jobject._kwargs = {'dual_re': True}
#        self.assertTrue(Juniper.open(jobject))
#
#        # master case, not dual re, routing_engine is backup
#        jobject._kwargs = {'routing_engine': 'backup'}
#        self.assertTrue(Juniper.open(jobject))
#
#        # Backup, dual_re
#        jobject._is_master = MagicMock(return_value=False)
#        jobject._kwargs = {'dual_re': True}
#        self.assertTrue(Juniper.open(jobject))
#
#        # backup, not dual_re, routing_engine is master
#        jobject._kwargs = {'routing_engine': 'master'}
#        jobject.vc_capable = False
#        self.assertTrue(Juniper.open(jobject))

    @patch('jnpr.toby.hldcl.juniper.junos.Response')
    def test_juniper_cli_failures(self, response_patch):
        jobject = MagicMock(spec=Juniper)
        jobject.prompt = '$'
        jobject.host = 'test'
        jobject.handle = MagicMock()
        jobject.name = 'foo'
        jobject.channels = []
        jobject._kwargs = MagicMock()
        jobject._kwargs.get = MagicMock(return_value = "'command' should be a string")
        # Junos object not connected
        #jobject.connected = False
        #self.assertFalse(Juniper.cli(jobject, command='show'))

        # Missing mandatory argument 'command'
        try:
            Juniper.cli(jobject)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Mandatory argument 'command' is missing!")

        # PyEZ object not connected
        #jobject.connected = True
        #jobject.handle.connected = False
        #self.assertFalse(Juniper.cli(jobject, command='show'))

        # Command is not string
        #jobject.handle.connected = True
        #self.assertFalse(Juniper.cli(jobject, command=['show']))
        try:
            Juniper.cli(jobject, command=['show'])
        except Exception as exp:
            self.assertEqual(exp.args[0], "'command' should be a string")

    @patch('jnpr.toby.hldcl.juniper.junos.Response')
    def test_juniper_cli(self, response_patch):
        jobject = MagicMock(spec=Juniper)
        jobject.prompt = '$'
        jobject.handle = MagicMock()
        jobject.handle.connected = True
        jobject.connected = True

        # Proper command
        xmldata = etree.XML('<shell></shell>')
        jobject.handle.cli = MagicMock(return_value=xmldata)
        response_patch.return_value = xmldata
        jobject.cli_timeout  = 60
        jobject.pyez_timeout = 60
        jobject._kwargs = MagicMock()
        jobject._kwargs.get = MagicMock(return_value="enable")
        self.assertEqual(
            etree.tostring(Juniper.cli(jobject, command='show')), b'<shell/>'
        )
        ## Added code to validate cli API by passing raw_output argument.
        self.assertEqual(
            etree.tostring(Juniper.cli(jobject, command='show', raw_output=True)), b'<shell/>'
        )

    def test_juniper_shell_failures(self):
        jobject = MagicMock(spec=Juniper)
        jobject.host = 'test'
        jobject.mode = 'shell'
        jobject.name = 'foo'
        jobject.channels = []
        jobject.handle = MagicMock()
        jobject.shell_timeout  = 60
        # Junos object not connected
        #jobject.connected = False
        #self.assertFalse(Juniper.shell(jobject, command='ls'))

        # Mandatory argument missing
        try:
            Juniper.shell(jobject)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Mandatory argument 'command' is missing!")

        # PyEZ object not connected
        #jobject.connected = True
        #jobject.handle.connected = False
        #self.assertFalse(Juniper.shell(jobject, command='ls'))

        # If 'command' is not a string
        try:
            Juniper.shell(jobject, command='ls')
        except Exception as exp:
            self.assertEqual(exp.args[0], "'command' should be a string")

        # Shell connection not present
        #jobject.handle.connected = True
        #jobject.shell_connection = False
        #self.assertFalse(Juniper.shell(jobject, command='ls'))

    def test_juniper_shell(self):
        jobject = MagicMock(spec=Juniper)
        jobject.mode = 'shell'
        #jobject.handle = MagicMock()
        #jobject.connected = True
        #jobject.shell_connection = MagicMock()
        #jobject.handle.connected = True
        #jobject.shell_connection.run = \
        #    MagicMock(return_value=(True,'shell output'))

        jobject.shell_timeout  = 60
        jobject.execute.return_value = 'shell output'
        self.assertEqual(Juniper.shell(jobject, command='ls').response(), 'shell output')
        ##   Added code to test shell API by passing raw_output argument.
        self.assertEqual(Juniper.shell(jobject, command='ls', raw_output=True).response(), 'shell output')

    @patch('jnpr.toby.hldcl.juniper.junos.Response')
    def test_juniper_execute(self, response_patch):
        """ Added test to validate execute API """
        jobject = MagicMock(spec=Juniper)
        jobject.mode = 'shell'
        jobject.prompt = "%"
        jobject.channels = {}
        jobject.channels['text'] = MagicMock()
        response_patch.return_value =  'execute output'
        jobject.response = response_patch.return_value
        self.assertEqual(Juniper.execute(jobject, command='ls'), 'execute output')
        self.assertEqual(Juniper.execute(jobject, command='ls', raw_output=True), 'execute output')

    @patch('jnpr.toby.hldcl.juniper.junos.Response')
    def test_juniper_vty(self, response_patch):
        """ Added test to validate vty API. """
        jobject = MagicMock(spec=Juniper)
        jobject.mode = 'vty'
        jobject.destination = 'fpc1'
        jobject.prompt = "#"
        jobject.channels = {}
        jobject.channels['text'] = MagicMock()
        response_patch.return_value =  'vty output'
        jobject.vty_timeout  = 60
        jobject.response = response_patch.return_value
        self.assertEqual(Juniper.vty(jobject, command='vty command', destination='fpc1'), 'vty output')
        self.assertEqual(Juniper.vty(jobject, command='vty command', destination='fpc1', raw_output=True), 'vty output')

    @patch('jnpr.toby.hldcl.juniper.junos.Response')
    def test_juniper_cty(self, response_patch):
        """ Added test to validate vty API. """
        jobject = MagicMock(spec=Juniper)
        jobject.mode = 'cty'
        jobject.destination = 'fpc1'
        jobject.prompt = "#"
        jobject.channels = {}
        jobject.channels['text'] = MagicMock()
        jobject.cty_timeout = 60
        response_patch.return_value =  'cty output'
        jobject.response = response_patch.return_value
        self.assertEqual(Juniper.cty(jobject, command='cty command', destination='fpc1'), 'cty output')

        ## Added code to validate config API by passing raw_output.
        self.assertEqual(Juniper.cty(jobject, command='cty command', destination='fpc1', raw_output=True), 'cty output')


    def test_juniper_config(self):
        jobject = MagicMock(spec=Juniper)
        jobject.mode = 'private'
        jobject.name = 'foo'
        jobject.channels = []
        #jobject.configObject = MagicMock()
        #jobject.handle = MagicMock()
        #jobject.configObject.load = MagicMock(return_value='Test')
        #self.assertEqual(
        #    Juniper.config(jobject, command_list=['show config']), 'Test')

        jobject.config_timeout = 60
        # Check return status
        robj = Juniper.config(jobject, command_list=['show config'])
        self.assertTrue(robj.status)

        ## Added code to validate config API by passing raw_output.
        robj = Juniper.config(jobject, command_list=['show config'], raw_output=True)
        self.assertTrue(robj.status)

        # Missing Mandatory argument 'command_list'
        try:
            Juniper.config(jobject)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Mandatory argument 'command_list' is missing!")

        # If 'command_list' argument is not a list
        try:
            Juniper.config(jobject, command_list='show config')
        except Exception as exp:
            self.assertEqual(exp.args[0], "Argument 'command_list' must be a list!")

        # configObject does not exist
        #jobject.configObject = MagicMock(side_effect=False)
        #self.assertIsInstance(
        #    Juniper.config(jobject, command_list=['show config']), MagicMock)

        # If command is not a string
        try:
            Juniper.config(jobject, command_list=[('show config')])
        except Exception as exp:
            self.assertEqual(exp.args[0], "Argument 'command_list' must be a list of strings!")

        # Check return value
        jobject.execute.return_value = "Test"
        robj = Juniper.config(jobject, command_list=['show config'], mode='private')
        self.assertEqual(robj.response(), "Test")

    @patch('jnpr.toby.hldcl.juniper.junos.time.sleep')
    def test_juniper_reboot(self, ptime):
        jobject = MagicMock(spec=Juniper)
        jobject.evo = True
        jobject._kwargs = {}
        jobject._kwargs['connect_targets'] = "console"
        jobject.channels = {}
        jobject.channels['text'] = MagicMock()
        #jobject.channels['text'].expect.return_value = [4]
        jobject.channels['text'].expect.side_effect = [[0,0,b'text'], [0], [0], [0]]
        jobject.shell.return_value = True
        jobject.reconnect.return_value=True
        jobject.host = "host1"
        jobject.user = "regress"
        jobject.password = "MaRtInI"
        jobject.su.return_value = False
        jobject.reboot_timeout = 60
        self.assertFalse(Juniper.reboot(jobject, timeout=0, interval=0))

        jobject.su.return_value = True
        self.assertTrue(Juniper.reboot(jobject, timeout=0, interval=0))

        jobject._kwargs['connect_targets'] = 'console'
        jobject.channels['text'].expect.side_effect = [[0,0,b'text'], [0], [0], [0]]
        self.assertTrue(Juniper.reboot(jobject, timeout=0, interval=0, mode='shell'))

        jobject._kwargs['connect_targets'] = 'management'
        jobject.reconnect.return_value=False
        self.assertFalse(Juniper.reboot(jobject, timeout=0, interval=0))

    @patch('jnpr.toby.hldcl.juniper.junos.time.sleep')
    def test_juniper_reboot_failures(self, ptime):
        jobject = MagicMock(spec=Juniper)
        jobject.evo = True
        jobject.handle = MagicMock()
        jobject.reboot_timeout = 60
        # Outer try exception
        jobject.reconnect = MagicMock(side_effect=Exception())
        self.assertFalse(Juniper.reboot(jobject, timeout=0, interval=0))
        # rpc.request_reboot exception
        jobject.handle.rpc.request_reboot = MagicMock(side_effect=Exception())
        self.assertFalse(Juniper.reboot(jobject, timeout=0, interval=0))

    def test_juniper_execute_rpc(self):
        jobject = MagicMock(spec=Juniper)
        jobject.channels = {}
        jobject.channels['pyez'] = MagicMock()
        jobject.channels['pyez'].execute.return_value = "data"
        jobject.rpc_timeout = 60
        self.assertEqual(Juniper.execute_rpc(jobject, command='ls', timeout=100).response(), 'data')

        # Returning xml data
        xmldata = etree.XML('<rpc></rpc>')
        
        jobject.channels['pyez'].execute.return_value = xmldata
        self.assertEqual(Juniper.execute_rpc(jobject, command='ls').response(), xmldata)


    def test_juniper_su(self):
        jobject = MagicMock(spec=Juniper)
        #jobject.shell_connection = MagicMock(spec=['touch'])
        self.assertRaises(Exception, Juniper.su, object)
        # Password prompt not found
        #self.assertFalse(Juniper.su(jobject, password='test123'))
        #jobject.shell_connection = MagicMock()
        #jobject.shell_connection.wait_for = MagicMock(return_value='Password:')
        jobject.set_prompt_shell.return_value = 'test'
        jobject.channels = {}
        jobject.channels['text'] = MagicMock()
        jobject.channels['text'].shell_prompt = '$'
        jobject.shell.return_value.response.return_value = "root"
        self.assertTrue(Juniper.su(jobject, password='test123'))

    def test_juniper_su_failures(self):
        jobject = MagicMock(spec=Juniper)
        #jobject.shell_connection = None
        # No shell_connection
        self.assertRaises(Exception, Juniper.su, jobject, password='test123')
        # password is None
        #jobject.shell_connection = MagicMock()
        self.assertRaises(Exception, Juniper.su, jobject)

        #jobject.shell_connection.wait_for = MagicMock(return_value='Test')
        jobject.set_prompt_shell.return_value = 'test'
        jobject.channels = {}
        jobject.channels['text'] = MagicMock()
        jobject.channels['text'].shell_prompt = '$'
        jobject.shell.return_value.response.return_value = "test"
        self.assertFalse(Juniper.su(jobject, password='test123'))

    @patch('jnpr.toby.hldcl.juniper.junos.time.sleep')
    #@patch(builtin_string + '.dir', return_value = ['RE0', 'as'])
    def test_juniper_reconnect(self, ptime):
        jobject = MagicMock(spec=Juniper)
        jobject._kwargs = {'channels':'test'}
        jobject.connect_channels = ['all']
        jobject.proxy = False
        jobject._connect_pyez.side_effect = [Exception,Exception,True]
        jobject._connect_text.side_effect = [Exception,Exception,True]
        jobject.connect_to_pyez = True
        Juniper.reconnect(jobject)
        self.assertFalse(Juniper.reconnect(jobject,timeout=0))
        jobject.connect_channels = []
        Juniper.reconnect(jobject)
        jobject.connect_channels = ['text']
        self.assertFalse(Juniper.reconnect(jobject,timeout=0))

    def test_juniper_disconnect(self):
        jobject = MagicMock(spec=Juniper)
        jobject.connected = True
        jobject.host = 'test'
        jobject.re = 'RE0'
        jobject.RE0 = MagicMock()
        Juniper.disconnect(jobject)
        jobject.connected = False
        self.assertFalse(Juniper.disconnect(jobject))

        jobject.rebooted = False
        jobject.connected = True
        jobject.handle = MagicMock()
        obj1 = MagicMock()
        obj1.close.return_value = "test"
        jobject.channels = {}
        jobject.channels['text'] = obj1  
     #jobject.handle.close = MagicMock()
        self.assertTrue(Juniper.disconnect(jobject))

    def test_juniper_disconnect_failures(self):
        jobject = MagicMock(spec=Juniper)
        jobject.handle = MagicMock()
        jobject.connected = True
        jobject.handle.close = MagicMock(side_effect=Exception)
        jobject.re = 'RE0'
        jobject.RE0 = MagicMock()
        jobject.RE0.handle = 'handle'
        self.assertFalse(Juniper.disconnect(jobject))


    @patch(builtin_string + '.dir', return_value=['RE0', 'RE1', 'self'])
    def test_juniper_close(self, pdir):
        jobject = MagicMock(spec=Juniper)
        jobject.connected = False
        jobject.log = MagicMock()
        jobject._replace_object = MagicMock()
        jobject.re = 'RE0'
        jobject.RE0.connected = True
        jobject.RE0.re = 'RE0'
        jobject.RE0.handle.connected = True
        #self.assertTrue(Juniper.close(jobject))
        self.assertFalse(Juniper.close(jobject))

        # all_routing_engines set to True
        jobject.connected = True
        jobject.channels = {}
        obj1 = MagicMock()
        obj1.close.return_value = "test"
        obj2 = MagicMock()
        obj2.close.return_value = "test"
        jobject.channels['text'] = obj1
        jobject.channels['pyez'] = obj2
        jobject.RE0.re = 'RE0'
        self.assertTrue(Juniper.close(jobject, all=True))

    def test_juniper_failures(self):
        jobject = MagicMock(spec=Juniper)
        jobject.re = 'RE0'
        jobject.RE0 = MagicMock()
        jobject.RE0.connected = True
        jobject.RE0.handle.connected = True
        jobject.RE0.handle.close = MagicMock(side_effect=Exception)
        self.assertFalse(Juniper.close(jobject))

#    def test_juniper_re_slot_name(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.handle = MagicMock()
#        jobject.re = 're0'
        # 2RE is False
#        jobject.handle.facts = {'2RE': False, 'master': 'RE0'}
#        self.assertEqual(Juniper.re_slot_name(jobject), 'RE0')

#        jobject.handle.facts = {'2RE': True, 'master': 'RE0'}
#        jobject._get_other_re_list = MagicMock(return_value=['RE1'])
#        jobject._get_all_re = MagicMock(return_value=['RE0', 'RE1'])
#        self.assertEqual(Juniper.re_slot_name(jobject), 'RE0')

#    def test_juniper_switch_re_failures(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.DUAL_RE = None
#        self.assertFalse(Juniper.switch_re(jobject))

#    def test_juniper_switch_re(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.DUAL_RE = MagicMock()
#        self.assertTrue(Juniper.switch_re(jobject, routing_engine='backup'))
#        self.assertTrue(Juniper.switch_re(jobject, routing_engine='re0'))
#        self.assertFalse(Juniper.switch_re(jobject, routing_engine='name'))

    @patch('jnpr.toby.hldcl.juniper.junos.Response')
    def test_juniper_commit(self, response_patch):
        jobject = MagicMock(spec=Juniper)
        jobject.configObject = MagicMock()
        jobject.handle = MagicMock()
        jobject.evo = True
        jobject.commit_timeout = 60
        xmld = etree.XML(
            '<rpc-reply><commit-results><routing-engine><name>re0</name>'
            '<commit-check-success/></routing-engine><routing-engine><name>'
            're1</name><commit-success/>Non-existant dump device /dev/ad1s1b'
            '</routing-engine><routing-engine><name>re0</name><commit-success/'
            '></routing-engine></commit-results></rpc-reply>')
        jobject.handle.rpc = MagicMock()
        jobject.handle.rpc.commit_configuration = MagicMock(return_value=xmld)
        kwargs = {'comment': 'Commit', 'confirm': 10, 'force_sync': True,
                  'full': True}
        self.assertTrue(Juniper.commit(jobject, **kwargs))

        # sync,
        response_patch.return_value = xmld
        kwargs = {'comment': 'Commit', 'confirm': 10, 'sync': True,
                  'full': True, 'detail': True}
        #self.assertTrue(Juniper.commit(jobject, **kwargs))        
        self.assertIsInstance(Juniper.commit(jobject, **kwargs), etree._Element)
        jobject.evo = False
        kwargs = {'comment': 'Commit', 'confirm': 10, 'sync': True,'force_sync':True,'full': True, 'detail': True}
        Juniper.commit(jobject, **kwargs)
        kwargs = {'comment': 'Commit', 'confirm': 10, 'sync': False,'force_sync':True,
                  'full': True, 'detail': True}
        Juniper.commit(jobject, **kwargs)
        kwargs = {'comment': 'Commit', 'confirm': 10, 'sync': True,'force_sync':False,
                  'full': True, 'detail': True}
        Juniper.commit(jobject, **kwargs)
        kwargs = {'comment': 'Commit', 'confirm': 10, 'sync': False,'force_sync':False,
                  'full': True, 'detail': True}
        Juniper.commit(jobject, **kwargs)

    def test_juniper_commit_failures(self):
        jobject = MagicMock(spec=Juniper)
        jobject.configObject = MagicMock()
        jobject.handle = MagicMock()
        jobject.evo = True
        xmld = etree.XML(
            '<rpc-reply><commit-results><routing-engine><name>re0</name>'
            '</routing-engine><routing-engine><name>'
            're1</name><commit-success/>Non-existant dump device /dev/ad1s1b'
            '</routing-engine><routing-engine><name>re0</name><commit-success/'
            '></routing-engine></commit-results></rpc-reply>')
        #jobject.handle.rpc = MagicMock()
        #jobject.handle.rpc.commit_configuration = MagicMock(return_value=xmld)
        #self.assertFalse(Juniper.commit(jobject).status)

        #jobject.handle.rpc.commit_configuration = MagicMock(side_effect=Exception)
        jobject.config.return_value.response.return_value = 'some errors, commit failed'
        self.assertRaises(Exception, Juniper.commit, jobject)


    #@patch(builtin_string + '.hasattr')
#    def test_juniper_switch_re_slot_failures(self):
#        jobject = MagicMock(spec=Juniper)
        # Invalid routing_engine
#        self.assertFalse(Juniper._switch_re_slot(
#            jobject, routing_engine='test'))

        # # provided slot does not exist
        # jobject1 = MagicMock(spec=['handle', 'log'])
        # self.assertFalse(Juniper._switch_re_slot(jobject1, routing_engine='re1'))

#    def test_juniper_switch_re_slot(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.RE0 = MagicMock()
#        self.assertTrue(Juniper._switch_re_slot(
#            jobject, routing_engine='RE0'))

#    def test_juniper_switch_re_role_failures(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.handle = MagicMock()
#        # Invalid routing_engine
#        self.assertFalse(Juniper._switch_re_role(
#            jobject, routing_engine='test'))
#
#        jobject.re = 'test'
#        xmldata = etree.XML(
#            '<rpc><route-engine><mastership-state>master</mastership-state>'
#            '<slot>1</slot></route-engine></rpc>')
#        jobject.handle.rpc.get_route_engine_information = \
#            MagicMock(return_value=xmldata)
#        self.assertFalse(Juniper._switch_re_role(jobject,
#                                                 routing_engine='master'))

#    def test_juniper_switch_re_role(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.handle = MagicMock()
#        jobject.re = 'RE1'
#        jobject.RE1 = MagicMock()
#        xmldata = etree.XML(
#            '<rpc><route-engine><mastership-state>backup</mastership-state>'
#            '<slot>1</slot></route-engine></rpc>')
#        jobject.handle.rpc.get_route_engine_information = MagicMock(return_value=xmldata)
#        self.assertTrue(Juniper._switch_re_role(
#            jobject, routing_engine='backup'))
#        jobject.re = 'RE'
#        self.assertTrue(Juniper._switch_re_role(
#            jobject, routing_engine='backup'))

#    def test_juniper_get_all_re(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.handle = MagicMock()
#        xmldata = etree.XML(
#            '<rpc><route-engine><mastership-state>backup</mastership-state>'
#            '<slot>1</slot></route-engine><route-engine><mastership-state>'
#            'master</mastership-state><slot>0</slot></route-engine></rpc>')
#        jobject.handle.rpc.get_route_engine_information = MagicMock(return_value=xmldata)
#        self.assertEqual(Juniper._get_all_re(jobject), ['RE1', 'RE0'])
#        # Routing egines not found
#        xmldata = etree.XML('<rpc></rpc>')
#        jobject.handle.rpc.get_route_engine_information = MagicMock(return_value=xmldata)
#        self.assertEqual(Juniper._get_all_re(jobject), [])

#    def test_juniper_get_all_re_failures(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.handle = MagicMock()
#        jobject.handle.rpc.get_route_engine_information = MagicMock(side_effect=Exception)
#        self.assertEqual(Juniper._get_all_re(jobject), [])

#    def test_juniper_get_other_re_list(self):
#        jobject = MagicMock(spec=Juniper)
#        xmldata = etree.XML('<rpc><multi-routing-engine-item><re-name>RE0'
#                            '</re-name></multi-routing-engine-item></rpc>')
#        jobject.cli = MagicMock(return_value=xmldata)
#        self.assertEqual(Juniper._get_other_re_list(jobject), ['RE0'])
#
#        # generic error
#        jobject.cli = MagicMock(return_value='')
#        self.assertRaises(Exception,
#                          Juniper._get_other_re_list, jobject)
#        # Could not connect error
#        jobject.cli = MagicMock(return_value='Could not connect to re0')
#        self.assertEqual(Juniper._get_other_re_list(jobject), ['RE0'])

    def test_juniper_init_failures(self):
        self.assertRaises(Exception, Juniper,
                          'Test', **{'dual_re': True, 'routing_engine': True})

#    @patch('jnpr.junos.utils.start_shell.StartShell')
#    @patch('jnpr.junos.utils.start_shell.StartShell.open')
#    def test_juniper_get_shell_connection(self, pshell, pshellopen):
#        jobject = MagicMock(spec=Juniper)
#        jobject._kwargs = MagicMock(return_value={'connect_mode': 'telnet'})
#        #pshell.open = MagicMock(return_value='SHELL')
#        self.assertEqual(Juniper._get_shell_connection(jobject),
#                              None)
#        # Connect mode is console
#        jobject._kwargs = {'connect_mode': 'console'}
#        self.assertTrue(Juniper._get_shell_connection(jobject))
#        jobject._kwargs = {'connect_mode': 'telnet'}

#    def test_juniper_create_other_re_kwargs(self):
#        jobject = MagicMock(spec=Juniper)
#        other_re_kwargs = \
#            Juniper._create_other_re_kwargs(
#                jobject, dict(model='mx', handle='True'), 'test1', 'backup'
#            )
#        self.assertEqual(other_re_kwargs['dual_re'], None)
#        self.assertEqual(other_re_kwargs['routing_engine'], 'backup')
#        self.assertEqual(other_re_kwargs.get('handle'), None)

#    def test_juniper_replace_object(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject1 = MagicMock(sepc=Juniper)
#        jobject1.handle = 'test123'
#        Juniper._replace_object(jobject, jobject1)
#        self.assertEqual(jobject.handle, 'test123')

#    def test_juniper_get_other_re_name(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.re = ''
#        # Not RE0/RE1
#        self.assertEqual(Juniper._get_other_re_name(jobject), None)
#        jobject.re = 'RE0'
#        self.assertEqual(Juniper._get_other_re_name(jobject), 'RE1')
#        jobject.re = 'RE1'
#        self.assertEqual(Juniper._get_other_re_name(jobject), 'RE0')

#    def test_juniper_get_connection_element(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.handle = MagicMock()
#        jobject._get_host_name = MagicMock(return_value='otherRE')
#        # host name
#        jobject.host = 'test'
#        self.assertEqual(Juniper._get_connection_element(jobject, 'RE0'),
#                         'otherRE')
#        # host name are same
#        jobject.host = 'otherRE'
#        jobject._get_host_ip = MagicMock(return_value='1.1.1.1')
#        self.assertEqual(Juniper._get_connection_element(jobject, 'RE0'),
#                         '1.1.1.1')
#        # host ip provided
#        jobject.host = '2.2.2.2'
#        self.assertEqual(Juniper._get_connection_element(jobject, 'RE0'),
#                         '1.1.1.1')

#    def test_juniper__get_host_ip(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.handle = MagicMock()
#        # management port is em0
#        xmldata = etree.XML(
#            '<rpc><groups><name>re0</name><interfaces><interface><name>em0'
#            '</name><unit><family><inet><address><name>1.1.1.1</name>'
#            '</address></inet></family></unit></interface></interfaces>'
#            '</groups></rpc>')
#        jobject.handle.rpc.get_configuration = MagicMock(return_value=xmldata)
#        self.assertEqual(Juniper._get_host_ip(jobject, 'RE0'), '1.1.1.1')
#        # management port is fxp0
#        xmldata = etree.XML(
#            '<rpc><groups><name>re1</name><interfaces><interface><name>fxp0'
#            '</name><unit><family><inet><address><name>1.1.1.2</name>'
#            '</address></inet></family></unit></interface></interfaces>'
#            '</groups></rpc>')
#        jobject.handle.rpc.get_configuration = MagicMock(return_value=xmldata)
#        self.assertEqual(Juniper._get_host_ip(jobject, 'RE1'), '1.1.1.2')
#        # Config does not have em0/fxp0
#        xmldata = etree.XML(
#            '<rpc><groups><name>re1</name><interfaces><interface><name>fx0'
#            '</name><unit><family><inet><address><name>1.1.1.2</name>'
#            '</address></inet></family></unit></interface></interfaces>'
#            '</groups></rpc>')
#        jobject.handle.rpc.get_configuration = MagicMock(return_value=xmldata)
#        self.assertRaises(Exception, Juniper._get_host_ip, jobject, 'RE1')

#    def test_juniper_get_host_name(self):
#        jobject = MagicMock(spec=Juniper)
#        jobject.handle = MagicMock()
#        xmldata = etree.XML('<rpc><groups><name>re1</name><system><host-name>'
#                            'test123</host-name></system></groups></rpc>')
#        jobject.handle.rpc.get_configuration = MagicMock(return_value=xmldata)
#        self.assertEqual(Juniper._get_host_name(jobject, 'RE1'), 'test123')

    def test_juniper_is_master(self):
        jobject = MagicMock(spec=Juniper)
        jobject.evo = True
        # bcakup case
        jobject.shell.return_value.response.return_value = "Backup"
        self.assertFalse(Juniper.is_master(jobject))
        # master case
        jobject.shell.return_value.response.return_value = "Master"
        self.assertTrue(Juniper.is_master(jobject))

        jobject.evo = False
        # bcakup case
        jobject.shell.return_value.response.return_value = "Backup"
        self.assertFalse(Juniper.is_master(jobject))
        # master case
        jobject.shell.return_value.response.return_value = "hw.re.mastership: 1"
        self.assertTrue(Juniper.is_master(jobject))

    def test_juniper_is_readonly_user(self):
        # first time connecting and user is read-only
        jobject = MagicMock(spec=Juniper)
        jobject.readonly_user = None
        jobject.cli.return_value.response.return_value = "\'read-only\'"
        self.assertTrue(Juniper.is_readonly_user(jobject))
        # we already know user is read-only so just returns read-only attribute
        jobject.readonly_user = True
        self.assertTrue(Juniper.is_readonly_user(jobject))
        # first time connectin and user is not read-only
        jobject2 = MagicMock(spec=Juniper)
        jobject2.readonly_user = None
        jobject2.cli.return_value.response.return_value = "test"
        self.assertFalse(Juniper.is_readonly_user(jobject2))
         # we already know user is not read-only so just returns read-only attribute
        jobject2.readonly_user = False
        self.assertFalse(Juniper.is_readonly_user(jobject2))        

    @patch(builtin_string + '.open')
    @patch('os.remove')
    def test_juniper_save_config(self, open_mock, remove_mock):
        jobject = MagicMock(spec=Juniper)
        jobject.A = MagicMock()
        jobject.host = MagicMock(return_value='test_device')
        jobject.RE0 = MagicMock(spec=Juniper)
        jobject.RE0.handle = MagicMock()
        jobject.RE0.host = MagicMock(return_value='test_device')
        jobject.RE0.upload = MagicMock()
        self.assertTrue(Juniper.save_config(jobject, file='test'))

    @patch(builtin_string + '.open')
    def test_juniper_save_config_failures(self, open_mock):
        jobject = MagicMock(spec=Juniper)
        jobject.name = 'foo'
        jobject.channels = []
        #jobject.A = MagicMock()
        #jobject.host = MagicMock(return_value='test_device')
        #jobject.RE0 = MagicMock(spec=Juniper)
        #jobject.RE0.handle = MagicMock()
        #jobject.RE0.host = MagicMock(return_value='test_device')
        #jobject.RE0.upload = MagicMock()
        #self.assertFalse(Juniper.save_config(jobject, file='test'))

        # Invalid 'type' argument
        try:
            Juniper.save_config(jobject, file='test', type='test')
        except Exception as exp:
            self.assertEqual(exp.args[0], 'Invalid value in parameter "type". Accepted values are "normal"/"xml"/"set"')

        # Invalid 'source' argument
        try:
            Juniper.save_config(jobject, file='test', source='test')
        except Exception as exp:
            self.assertEqual(exp.args[0], 'Invalid value in parameter "source". Accepted values are "committed"/"candidate"')

        # Unable to save configuration
        jobject.config.return_value.response.return_value = "some text"
        jobject.host = "host"
        try:
            Juniper.save_config(jobject, file='test')
        except Exception as exp:
            self.assertEqual(exp.args[0], "Could not save configuration on host. Output: some text")

    @patch('robot.libraries.BuiltIn.BuiltIn.get_variable_value', return_value='some_dummy_test')
    @patch(builtin_string + '.open')
    @patch('jnpr.junos.utils.config.Config')
    def test_juniper_load_config(self, pconfig, open_patch, patch_robot_builtin):
        jobject = MagicMock()
        #jobject.configObject = None
        #jobject.handle = MagicMock()
        # For non configObject case
        #self.assertFalse(Juniper.load_config(jobject, local_file='test', option='override'))
        self.assertRaises(Exception, Juniper.load_config, jobject, local_file='test', option='override')

        # Pass case and option is merge
        #jobject.configObject = MagicMock()
        jobject.config.return_value.response.return_value = "test"
        jobject.config.return_value.response.status = True
        
        self.assertTrue(Juniper.load_config(jobject, local_file='test', option='merge', format='text'))

        # Pass case and option is merge, with commit set to True
        #jobject.configObject = MagicMock()
        jobject.config.return_value.response.return_value = "test"
        jobject.config.return_value.response.status = True
        jobject.commit.return_value.response.return_value = "test-commit"
        jobject.commit.return_value.response.status = True
        self.assertTrue(Juniper.load_config(jobject, local_file='test', option='merge', format='text', commit=True))
        self.assertEqual( Juniper.load_config(jobject, local_file='test', option='merge', format='text', commit=True).response(), "Configuration loaded successfully. test-commit")

        # Pass case and option is merge, with commit set to False
        #jobject.configObject = MagicMock()
        jobject.config.return_value.response.return_value = "test"
        jobject.config.return_value.response.status = True
        jobject.commit.return_value.response.return_value = "test-commit"
        jobject.commit.return_value.response.status = True
        self.assertTrue(Juniper.load_config(jobject, local_file='test', option='merge', format='text', commit=False))
        self.assertEqual( Juniper.load_config(jobject, local_file='test', option='merge', format='text', commit=False).response(), "Configuration loaded successfully. ")


        # local_file not passed
        try:
            Juniper.load_config(jobject, option='merge')
        except Exception as exp:
            self.assertEqual(exp.args[0], "'local_file/remote_file/args[0]' option is mandatory")

        # remote_file passed
        jobject.shell.return_value.response.return_value = "test"
        self.assertTrue(Juniper.load_config(jobject,
                                            remote_file='test',
                                            option='merge'))
        # config is present in string
        jobject.device_logger._log_dir = "dir"
        self.assertTrue(Juniper.load_config(jobject,
                                            '',
                                            option='merge'))

#    def test_juniper_switch_routing_engine_handle_api(self):
#        from jnpr.toby.hldcl.juniper.junos import switch_routing_engine_handle_api
#        jobject = MagicMock()
#        jobject.switch_re = MagicMock(return_value=True)
#        self.assertTrue(switch_routing_engine_handle_api(jobject))

#    def test_juniper_retrieve_re_slot_name_api(self):
#        from jnpr.toby.hldcl.juniper.junos import retrieve_re_slot_name_api
#        jobject = MagicMock()
#        jobject.re_slot_name = MagicMock(return_value='RE0')
#        self.assertEqual(retrieve_re_slot_name_api(jobject), 'RE0')

    def test_juniper_add_channel(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper

        junos_object = MagicMock(spec=Juniper)
        self.assertTrue(Juniper.add_channel(junos_object, 'text'))
        junos_object.log.assert_called_with(level='DEBUG', message="Adding channel text currently not supported")
        self.assertTrue(Juniper.add_channel(junos_object, 'radius'))
        junos_object.log.assert_called_with(level='DEBUG', message="Invalid channel radius to add in Junos object")
        junos_object._add_snmp_channel = MagicMock(return_value='SNMP Object')
        self.assertEqual(Juniper.add_channel(junos_object, 'snmp'), 'SNMP Object')

    @patch('jnpr.toby.hldcl.channels.snmp.Snmp')
    def test_juniper_add_snmp_channel(self, patch_snmp):
        from jnpr.toby.hldcl.juniper.junos import Juniper

        patch_snmp.return_value.get_snmp_id = MagicMock()
        patch_snmp.return_value.get_snmp_id.return_value = 11
        junos_object = MagicMock(spec=Juniper)
        junos_object.host = 'router'
        junos_object.mibs_custom_dir = 'test'
        junos_object.channels = dict()
        self.assertEqual(Juniper._add_snmp_channel(junos_object), 11)
        self.assertEqual(junos_object.default_snmp_channel, 11)
        dict_keys = list(junos_object.channels['snmp'].keys())
        self.assertEqual(dict_keys, [11])

    def test__get_vc_chassis(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        from jnpr.toby.utils.response import Response
        jobject = MagicMock(spec=Juniper)
        jobject.facts = {'vc_chassis' : 'test'}
        self.assertEqual('test',Juniper._get_vc_chassis(jobject))
        jobject.facts = {}
        jobject.model = 'mx'
        jobject.shell = MagicMock(return_value=Response(response="current protocol mode 1 group type 5 \n"))
        jobject.facts = {}
        self.assertEqual((True,'master'),Juniper._get_vc_chassis(jobject))
        jobject.shell = MagicMock(return_value=Response(response="current protocol mode 2 group type 5 \n"))
        jobject.facts = {}
        self.assertEqual((True,'backup'),Juniper._get_vc_chassis(jobject))
        jobject.shell = MagicMock(return_value=Response(response="current protocol mode 0 group type 5 \n"))
        jobject.facts = {}
        self.assertEqual((True,'local'),Juniper._get_vc_chassis(jobject))
        jobject.shell = MagicMock(return_value=Response(response="current protocol mode 3 group type 5 \n"))
        jobject.facts = {}
        self.assertEqual((True,None),Juniper._get_vc_chassis(jobject))
        jobject.shell = MagicMock(return_value=Response(response="current protocol mode 2 group type 4 \n"))
        jobject.facts = {}
        self.assertEqual((False,None),Juniper._get_vc_chassis(jobject))
        jobject.model = 'ptx'
        jobject.facts = {}
        self.assertFalse(Juniper._get_vc_chassis(jobject))
        jobject.shell = MagicMock(return_value=Exception('err'))
        jobject.model = 'mx'
        jobject.facts = {}
        self.assertIsNone(Juniper._get_vc_chassis(jobject))

    def test__get_ha(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        jobject = MagicMock(spec=Juniper)
        jobject.facts = {'ha' : 'test'}
        self.assertEqual('test',Juniper._get_ha(jobject))
        jobject.facts = {}
        jobject.model = 'srx'
        jobject.is_ha = True
        self.assertTrue(Juniper._get_ha(jobject))
        jobject.facts = {}
        jobject.is_ha = False
        self.assertFalse(Juniper._get_ha(jobject))
        jobject.model = 'mx'
        jobject.facts = {}
        self.assertFalse(Juniper._get_ha(jobject))

    def test__get_manufacturing_mode(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        from jnpr.toby.utils.response import Response
        jobject = MagicMock(spec=Juniper)
        jobject.facts = {'manufacturing_mode' : 'test'}
        self.assertEqual('test',Juniper._get_manufacturing_mode(jobject))
        jobject.config= MagicMock(return_value=Response(response="boot -h -m manufacturing fpc"))
        jobject.facts = {}
        self.assertTrue(Juniper._get_manufacturing_mode(jobject))
        jobject.facts = {}
        jobject.config= MagicMock(return_value=Response(response="boot -h -m manufacturing"))
        self.assertFalse(Juniper._get_manufacturing_mode(jobject))
        jobject.facts = {}
        jobject.config = MagicMock(return_value=Exception('err'))
        self.assertIsNone(Juniper._get_manufacturing_mode(jobject))
 
    def test_get_vmhost_infra(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        from jnpr.toby.utils.response import Response
        jobject = MagicMock(spec=Juniper)
        jobject.facts = {'mt_rainier' : 'test'}
        self.assertEqual('test',Juniper.get_vmhost_infra(jobject))

        jobject.cli = MagicMock(return_value=Response(response="Model 2X00x4"))
        jobject.facts = {}
        self.assertTrue(Juniper.get_vmhost_infra(jobject))

        jobject.cli = MagicMock(return_value=Response(response="Model"))
        jobject.facts = {}
#        jobject.model = 'ptx'
        jobject.get_model = MagicMock(return_value="ptx")
        jobject.shell = MagicMock(return_value=Response(response="hw.re.vmhost_mode: 1"))
        self.assertTrue(Juniper.get_vmhost_infra(jobject))

        jobject.facts = {}
        jobject.model = 'ptx'
        jobject.shell = MagicMock(return_value=Response(response="hw.re.vmhost_mode: 2"))
        self.assertFalse(Juniper.get_vmhost_infra(jobject))

        jobject.facts = {}
        jobject.model = 'srx'
        self.assertFalse(Juniper.get_vmhost_infra(jobject))

        jobject.facts = {}
        jobject.model = 'nfx250'
        jobject.shell = MagicMock(return_value=Response(response=""))
        self.assertFalse(Juniper.get_vmhost_infra(jobject))

        jobject.facts = {}
        jobject.cli = MagicMock(return_value=Exception('err'))
        self.assertIsNone(Juniper.get_vmhost_infra(jobject))


    def test__get_tvp(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        from jnpr.toby.utils.response import Response
        jobject = MagicMock(spec=Juniper)
        jobject.facts = {'tvp' : 'test'}
        self.assertEqual('test',Juniper._get_tvp(jobject))

        jobject.shell = MagicMock(return_value=Response(response="pvi-model"))
        jobject.model = None
        jobject.facts = {}
        self.assertTrue(Juniper._get_tvp(jobject))

        jobject.shell = MagicMock(return_value=Response(response="model"))
        jobject.facts = {}
        jobject.model = 'acx50'
        jobject.cli   = MagicMock(return_value=Response(response="JUNOS Host Software"))
        self.assertTrue(Juniper._get_tvp(jobject))

        jobject.facts = {}
        jobject.model = 'acx50'
        jobject.cli   = MagicMock(return_value=Response(response="Software"))
        self.assertFalse(Juniper._get_tvp(jobject))

        jobject.facts = {}
        jobject.model = 'srx'
        self.assertFalse(Juniper._get_tvp(jobject))

        jobject.facts = {}
        jobject.shell = MagicMock(return_value=Exception('err'))
        self.assertIsNone(Juniper._get_tvp(jobject))

    def test__get_evo(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        jobject = MagicMock(spec=Juniper)
        jobject.facts = {'evo' : 'test'}
        self.assertEqual('test',Juniper._get_evo(jobject))

        with patch('jnpr.toby.hldcl.juniper.junos.Juniper.is_evo',return_value=True) as evo_patch:
            jobject.facts = {}
            self.assertTrue(Juniper._get_evo(jobject))
        jobject.is_evo = Exception('err')
        jobject.facts = {}
        self.assertIsNone(Juniper._get_evo(jobject))
 
    def test__get_fact(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        jobject = MagicMock(spec=Juniper)
        jobject._get_evo = MagicMock()
        Juniper._get_fact(jobject,attribute='evo')

    def test_get_facts(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        jobject = MagicMock(spec=Juniper)
        jobject.facts = {}
        jobject._get_fact = MagicMock(return_value='test')
        Juniper.get_facts(jobject,attribute='evo')
        Juniper.get_facts(jobject,attribute=['evo','tvp'])
        Juniper.get_facts(jobject)

    def test__get_version_from_textchnl(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        jobject = MagicMock(spec=Juniper)

        etree_xml = """
<rpc-reply>
    <software-information>
        <host-name>planck</host-name>
        <product-model>mx240</product-model>
        <product-name>mx240</product-name>
        <junos-version>16.2R2.8</junos-version>
     </software-information>
 </rpc-reply>
                                     """
        jobject.cli = MagicMock(return_value=Response(response=etree_xml))

        jobject.version = Juniper._get_version_from_textchnl(jobject)

    def test_get_version(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        jobject = MagicMock(spec=Juniper)
        jobject.major_version = 'test'

        jobject._get_version_from_textchnl = MagicMock(return_value='16.2R2.8')
        Juniper.get_version(jobject,major=True)
        
        jobject.version = 'test'
        Juniper.get_version(jobject,major=False)
      
        jobject.major_version = None
        j1 = MagicMock(spec=Juniper)
        j1.facts = {'version' : '1.1'}
        jobject.channels = {'pyez' :j1} 
        Juniper.get_version(jobject,major=True)
         
        jobject.version = None
        Juniper.get_version(jobject,major=False)
        
        jobject.channels = {'pyez' :None}
        jobject.version = None
        etree_xml = """
<rpc-reply>
    <software-information>
        <host-name>planck</host-name>
        <product-model>mx240</product-model>
        <product-name>mx240</product-name>
        <junos-version>16.2R2.8</junos-version>
     </software-information>
 </rpc-reply>
                                     """
        jobject.cli = MagicMock(return_value=Response(response=etree_xml))
        self.assertEqual('16.2R2.8',Juniper.get_version(jobject))

        etree_xml = None
        jobject = MagicMock(spec=Juniper)
        jobject.channels = {'pyez' :None}
        jobject.cli = MagicMock(return_value=Response(response=etree_xml))
        jobject.version = None
        jobject._get_version_from_textchnl = MagicMock(return_value=None)
        Juniper.get_version(jobject,major=False)
        
        jobject.channels = Exception('err')
        self.assertRaises(Exception,Juniper.get_version,jobject)

    def test_get_model(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        jobject = MagicMock(spec=Juniper)
                    
        j1 = MagicMock(spec=Juniper)
        j1.facts = {'model' :'test'}
        jobject.channels = {'pyez' :j1}
        self.assertEqual('test',Juniper.get_model(jobject))
        
        jobject = MagicMock(spec=Juniper) 
        jobject.channels = {'pyez' :None}
        etree_xml = """
<rpc-reply>
    <software-information>
        <host-name>planck</host-name>
        <product-model>mx240</product-model>
        <product-name>mx240</product-name>
        <junos-version>16.2R2.8</junos-version>
     </software-information>
 </rpc-reply>
                                     """
        jobject.cli = MagicMock(return_value=Response(response=etree_xml))
        self.assertEqual('MX240',Juniper.get_model(jobject))
        etree_xml = None
        jobject = MagicMock(spec=Juniper)
        jobject.channels = {'pyez' :None}
        jobject.cli = MagicMock(return_value=Response(response=etree_xml))
        jobject.model = None
        self.assertIsNone(Juniper.get_model(jobject))
        
        jobject = MagicMock(spec=Juniper) 
        jobject.channels = Exception('err')
        self.assertRaises(Exception,Juniper.get_model,jobject)

        
        jobject.model = 'test'
        self.assertEqual('test',Juniper.get_model(jobject))
    
    @patch('jnpr.toby.hldcl.juniper.junos.time.sleep')
    def test_switch_re_master(self,sleep_patch):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        from jnpr.toby.utils.response import Response
        jobject = MagicMock(spec=Juniper)
        
        jobject.dual_controller = True 
        jobject.cli = MagicMock(return_value=Response(response='The other routing engine becomes the master'))
        Juniper.switch_re_master(jobject)
        
        jobject.cli = MagicMock(return_value=Response(response='Not ready for mastership switch, try after '
                                  '2 secs.'))
    
        jobject.cli = MagicMock(return_value=Response(response='Not ready for mastership switch, try after '
                                  '169 seconds.'))          

        Juniper.switch_re_master(jobject)

        jobject.cli = MagicMock(return_value=Response(response=''))
        Juniper.switch_re_master(jobject)
         
        jobject.cli = Exception('err')
        self.assertRaises(Exception,Juniper.switch_re_master,jobject)

    @patch('jnpr.toby.hldcl.juniper.junos.time.sleep')
    def test_software_install(self, sleep_patch):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        jobject = MagicMock(spec=Juniper)
        
        self.assertRaises(Exception,Juniper.software_install,jobject)
       
        self.assertRaises(Exception,Juniper.software_install,jobject,package='package',pkg_set='pkg_set')
        jobject.channels = {'pyez':MagicMock()}
        jobject.upgrade_timeout = 60
        with patch('jnpr.junos.utils.sw.SW',return_value=MagicMock()) as sw_patch :
            sw_patch.install.return_value = True
            jobject.reboot = MagicMock(return_value=False)
            self.assertRaises(Exception,Juniper.software_install,jobject,package='package',pkg_set='pkg_set')

            jobject.reboot = MagicMock(return_value=True)
            Juniper.software_install(jobject,package='package',pkg_set='pkg_set',no_copy=True)

            Juniper.software_install(jobject,package='package',pkg_set='pkg_set',reboot=False,no_copy=True)
            sw_patch.install.return_value = True
            Juniper.software_install(jobject,package='package',pkg_set='pkg_set',reboot=False,no_copy=True)
       
    @patch('jnpr.toby.hldcl.juniper.junos.time.sleep') 
    def test__check_interface_status(self,sleep_patch):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        from jnpr.toby.utils.response import Response
        jobject = MagicMock(spec=Juniper)
        
        jobject.cli  = MagicMock(return_value=Response(response="(interface 1) int1 up (interface 2) int2 down"))
        self.assertTrue(Juniper._check_interface_status(jobject,interfaces=["(interface 1)"]))
        jobject = MagicMock(spec=Juniper)
        jobject.cli = MagicMock(return_value=Response(response="(interface 2) int2 down"))
        self.assertFalse(Juniper._check_interface_status(jobject,interfaces=["(interface 2)"]))
        jobject.cli = MagicMock(return_value=Response(response="""(interface 1) int1 up (interface 2) int2 down"""))
        self.assertFalse(Juniper._check_interface_status(jobject,interfaces=["Some other pattern"]))
        jobject.cli = MagicMock(return_value=Response(response="""(interface 1) """)) 
        self.assertFalse(Juniper._check_interface_status(jobject,interfaces=["(interface"]))

    @patch('jnpr.toby.hldcl.juniper.junos.time.sleep')
    def test_detect_core(self, sleep_patch):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        from jnpr.toby.utils.response import Response

        import builtins
        builtins.t = self
        t._timezone = "PDT"
        t._stage = "setup"
        t._test_stage = "tc1"
        from os import popen
        popen_mock = MagicMock(spec=popen)
        popen_mock.read = MagicMock(return_value="20170519 10:12:12.1")
        with patch('jnpr.toby.hldcl.juniper.junos.os.popen',return_value=popen_mock) as popen_patch:
            with patch('jnpr.toby.hldcl.juniper.junos.Time.convert_datetime_to_gmt',return_value=12) as time_patch:
                jobject = MagicMock(spec=Juniper)
                jobject._device_start_time = 1562577469
                jobject._kwargs = {}
                jobject.evo = True
                jobject.shell = MagicMock(return_value=Response(response="core 1 c1 a1 0 date 1 1:111 as\ncore 1 c1 a1 1 date 1 1:111 None\ncore 1 c1 a1 1"))
                jobject.controllers_data = {'hostname' :'h1'} 
                Juniper.detect_core(jobject,core_path="/var/crash/*core*")
                
    def test_set_prompt_shell(self):
        from jnpr.toby.hldcl.juniper.junos import Juniper
        from jnpr.toby.utils.response import Response
       
        jobject = MagicMock(spec=Juniper)
        j1 = MagicMock(spec=Juniper)
        j1.execute = MagicMock(side_effect=[-1,1,-1,1,1,-1,1,1,-1,1,1,-1,1,1,1,1,1])
        jobject.channels = {'text' :j1} 
        self.assertRaises(Exception,Juniper.set_prompt_shell,jobject,"$")
        self.assertRaises(Exception,Juniper.set_prompt_shell,jobject,"$")
        jobject.response  = '/bin/sh'
        self.assertRaises(Exception,Juniper.set_prompt_shell,jobject,"$")
        jobject.response  = '/bin/bash'
        self.assertRaises(Exception,Juniper.set_prompt_shell,jobject,"$")
        jobject.response  = 'csh'
        self.assertRaises(Exception,Juniper.set_prompt_shell,jobject,"$")
        jobject.response  = ''
        self.assertRaises(Exception,Juniper.set_prompt_shell,jobject,"$")
        jobject.response  = 'csh'
        self.assertTrue(Juniper.set_prompt_shell(jobject,"$"))
    
    @patch('jnpr.toby.hldcl.juniper.junos.Grpc') 
    def test__grpc_init(self,grpc_patch):
        from jnpr.toby.hldcl.channels.grpcConn import Grpc
        from jnpr.toby.hldcl.juniper.junos import Juniper
        from jnpr.toby.utils.response import Response
        grpc_patch.return_value = MagicMock(spec=Grpc)
        grpc_patch.get_grpc_id = MagicMock(return_value = 'id')
        jobject = MagicMock(spec=Juniper)
        jobject.default_grpc_channel = False
        jobject.channels = {'grpc':{'id':''}}
        Juniper._grpc_init(jobject,channel_attributes={})
        jobject = MagicMock(spec=Juniper)
        jobject.channels = {}
        Juniper._grpc_init(jobject,channel_attributes={'channel_id':'ch_id','host':'hostname'})








if __name__ == '__main__':
    unittest.main()
