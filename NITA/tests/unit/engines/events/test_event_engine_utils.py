# pylint: disable=undefined-variable,missing-docstring,invalid-name,bad-continuation,import-error,unused-variable,unused-import

import unittest2 as unittest
import builtins
from mock import patch, Mock, MagicMock, call
import datetime
from jnpr.toby.init.init import init
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.device import Device
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.engines.events.event_engine_utils import *


class TestTriggers(unittest.TestCase):

    def setUp(self):
        import builtins
        #builtins.t = self
        builtins.t = MagicMock(spec=init)
        t.log = MagicMock(return_value=True)
        t.log_console = MagicMock(return_value=True)
        t.get_handle = MagicMock(spec=Device)
        builtins.tv = {'r0__name': 'tetra'}
        t.resources = {'r0':
                    {'interfaces':
                        {'r0r1_2':
                           {'pic': 'ge-1/0/7',
                            'management': 0,
                            'name': 'ge-1/0/7.0',
                            'link': 'link2',
                            'type': ['10x', '1GE', 'LAN', 'EQ', 'SFP-SX', 'QDPCE-R-40X', 'B3', 'I3', 'ether', 'ge'],
                            'unit': 0},
                         'r0r1_1':
                             {'management': 0,
                             'uv_test': 2,
                             'uv-test2': 3,
                             'unit': 0,
                             'type': ['10x', '1GE', 'LAN', 'EQ', 'SFP-SX', 'QDPCE-R-40X', 'B3', 'I3', 'ether', 'ge'],
                             'pic': 'ge-1/0/6', 'name': 'ge-1/0/6.0', 'link': 'link1'}},
                     'system':
                        {'primary':
                             {'cube': ['COMMON-LISP::OR', 'rbu-cst-core-wf-1', 'misc'],
                              'osname': 'JunOS',
                              'name': 'tetra',
                              'model': 'mx240',
                              'make': 'juniper',
                              'controllers':
                                {'re0':
                                     {'domain': 'englab.juniper.net',
                                      'isoaddr': '47.0005.80ff.f800.0000.0108.0001.0100.0923.4220.00',
                                      'con-ip': '10.9.53.203',
                                      'loop-ip': '10.9.234.220',
                                      'hostname': 'tetra',
                                      'mgt-ip': '10.9.33.24',
                                      'loop-ipv6': 'abcd::10:9:234:220',
                                      'osname': 'JunOS',
                                      'mgt-ipv6': 'abcd::10:9:33:24',
                                      'mgt-intf-name': 'fxp0.0'}},
                             }}},
                       'r1':
                    {'interfaces':
                        {'r0r1_2':
                            {'pic': 'ge-0/0/3',
                             'management': 0,
                             'name': 'ge-0/0/3.0',
                             'link': 'link2',
                             'type': ['IQ2E', 'SFP-SX', 'DOWN', 'B3', 'E-FPC', 'ge', 'ether', '4x', '1GE', 'LAN'],
                             'unit': 0},
                         'r0r1_1':
                             {'pic': 'ge-0/0/2',
                              'management': 0,
                              'name': 'ge-0/0/2.0', 'link': 'link1',
                              'type': ['ge', 'ether', '4x', '1GE', 'LAN', 'IQ2E', 'SFP-SX', 'DOWN', 'B3', 'E-FPC'],
                              'unit': 0}},
                     'system':
                        {'primary':
                            {'re_type': 'RE-5.0',
                             'cube': ['COMMON-LISP::OR', 'rbu-cst-core-wf-1', 'misc'],
                             'osname': 'JunOS',
                             'name': 'brandeis',
                             'model': 'm10i',
                             'make': 'juniper',
                             'controllers':
                                 {'re0':
                                    {'domain': 'englab.juniper.net',
                                     'isoaddr': '47.0005.80ff.f800.0000.0108.0001.0100.0901.0154.00',
                                     'con-ip': '10.9.17.141',
                                     'loop-ip': '10.9.10.154',
                                     'hostname': 'brandeis',
                                     'mgt-ip': '10.9.2.154',
                                     'loop-ipv6': 'abcd::10:9:10:154',
                                     'osname': 'JunOS',
                                     'mgt-ipv6': 'abcd::10:9:2:154',
                                     'mgt-intf-name': 'fxp0.0'}},
                            }
                        }
                    }}

    def test_add_tag_name_to_handle(self):
        self.assertEqual(add_tag_name_to_handle(), None)

    def test_device_handle_parser(self):
        dh = MagicMock()
        dh.get_current_controller_name.return_value = 're0'
        t.get_handle.get_current_controller_name = MagicMock(return_value='re0')
        #t.get_handle.name.return_value = 'tetra'
        self.assertEqual(device_handle_parser(device='r0').tag, 'r0')
        self.assertEqual(device_handle_parser(device='tetra').name, 'tetra')
        t.resources['r0']['system']['primary']['name'] = 'device'
        dh.get_current_controller_name.return_value = 're0'
        t.get_handle.get_current_controller_name = MagicMock(return_value='re0')
        self.assertEqual(device_handle_parser(debug_log_on='test'), None)
        self.assertRaises(Exception, device_handle_parser, device='noname')
        re = MagicMock()
        re.match = MagicMock(return_value=True)
        self.assertEqual(device_handle_parser(device="r0", debug_log_on='Test').tag, 'r0')

    def test_get_dev_handle(self):
       dev_handle_map = {'resource' : 'bradis'}

    #@patch('jnpr.toby.engines.events.event_engine_utils.interface')
    def test_interface_handler_to_ifd(self):
        self.assertEqual('external_device', "external_device", interface_handler_to_ifd(device='external_device', interface="external_device"))

    def test_get_device_info_from_handle(self):
        dh = MagicMock()
        dh.current_node = MagicMock()
        dh.current_node.current_controller = MagicMock()
        dh.current_node.current_controller.name = "itshost"
        t.resources['r1']['system']['primary']['name'] = 'itshost'
        self.assertEqual(get_device_info_from_handle(dh, debug_log_on='Test'), True)
        dh.current_node.current_controller.name = False
        dh.current_node.current_controller.host = "10.9.2.154"
        self.assertEqual(get_device_info_from_handle(dh), None)
        t.resources['r1']['system']['primary']['controllers'] = 'r_engine'

    def test_func_name(self):
        stack = MagicMock(return_value='Test')

    def test_mon_eng_annotate(self):
        dh = MagicMock()
        self.assertEqual(mon_eng_annotate(message=True, me_object="Test"), True)

    def test_nice_string(self):
        list_or_iterator = [1, 2, 3, 4]
        self.assertEqual(nice_string(list_or_iterator), '1, 2, 3, 4')
        self.assertEqual(nice_string(list_or_iterator='list'), 'list')

    @patch('jnpr.toby.engines.events.event_engine_utils.ET')
    def test_strip_xml_namespace(self, et_mock):
        ab = MagicMock()
        Abc = MagicMock()
        Abc.tag = 123
        et_mock.fromstring.return_value.getchildren.return_value = [ab]
        ab.xpath.return_value = [Abc]
        et_mock.QName.localname.return_value = Abc.tag
        self.assertEqual(strip_xml_namespace('Testa'), ab) 

    @patch('jnpr.toby.engines.events.event_engine_utils.execute_custom_mode')
    @patch('jnpr.toby.engines.events.event_engine_utils.add_mode')
    @patch('jnpr.toby.engines.events.event_engine_utils.get_dh_tag')
    def test_cli_pfe(self, get_dh_tag, add_mode, custom_mode):
        add_mode.return_value = 'some'
        get_dh_tag.return_value = 'r0'
        custom_mode.return_value = 'Executed'
        dh = MagicMock()
        dh.su = MagicMock()
        custom_modes = {'r0':{}}
        self.assertEqual('Executed', cli_pfe(dh, cmd='\n'))
        get_dh_tag.return_value = 'r0'
        custom_mode.return_value = 'Executed'
        dh = MagicMock()
        dh.su = MagicMock()
        custom_modes = {}
        self.assertEqual('Executed', cli_pfe(dh, cmd='\n'))
        get_dh_tag.return_value = 'r0'
        dh = MagicMock()
        dh.su = MagicMock()
        dh.command.return_value = True
        custom_mode.return_value = False
        custom_modes = {'r0' : {'val': 'hii'}}
        self.assertEqual('False', cli_pfe(dh, cmd='\n'))


    @patch('jnpr.toby.engines.events.event_engine_utils.execute_custom_mode')
    @patch('jnpr.toby.engines.events.event_engine_utils.add_mode')
    @patch('jnpr.toby.engines.events.event_engine_utils.get_dh_tag')
    def test_hshell(self, get_dh_tag, add_mode, custom_mode):
        add_mode.return_value = 'some'
        get_dh_tag.return_value = 'r0'
        custom_mode.return_value = 'Executed'
        dh = MagicMock()
        dh.su = MagicMock()
        custom_modes = {'r0':{}}
        self.assertEqual('Executed', hshell(dh, cmd='\n'))
        get_dh_tag.return_value = 'r0'
        custom_mode.return_value = 'Executed'
        dh = MagicMock()
        dh.su = MagicMock()
        custom_modes = {'r1':{}}
        self.assertEqual('Executed', hshell(dh, cmd='\n'))

    @patch('jnpr.toby.engines.events.event_engine_utils.execute_custom_mode')
    @patch('jnpr.toby.engines.events.event_engine_utils.add_mode')
    @patch('jnpr.toby.engines.events.event_engine_utils.get_dh_tag')
    def test_vhclient(self, get_dh_tag, add_mode, custom_mode):
        add_mode.return_value = 'some'
        get_dh_tag.return_value = 'r0'
        custom_mode.return_value = 'Executed'
        dh = MagicMock()
        dh.su = MagicMock()
        custom_modes = {'r0':{'all':22}}
        self.assertEqual('Executed', vhclient(dh, cmd='\n'))
        get_dh_tag.return_value = 'r0'
        custom_mode.return_value = 'Executed'
        dh = MagicMock()
        dh.su = MagicMock()
        custom_modes = {'r2':{'all':22}}
        self.assertEqual('Executed', vhclient(dh, cmd='\n'))

    def test_get_dh_name(self):
        dh = MagicMock()
        dh.host = 'tetra'
        self.assertEqual(get_dh_name(dh), 'tetra')
        dh.name = 'ucsc'
        self.assertEqual(get_dh_name(dh), 'ucsc')

    def test_get_dh_tag(self):
        dh = MagicMock()
        dh.tag = 'r0'
        self.assertEqual(get_dh_tag(dh), 'r0')

    def test_get_pfe(self):
        dh = MagicMock()
        models = {'mx80': 'tfeb0',
                  'mx104': 'afeb0',
                  'ptx10001': 'fpc0.0',
                  'psd': 'fpc1',
                  'm10i': 'cfeb',
                  #'qfx10008': 'cli-pfe',
                  'ptx10003-80C' : 'fpc1',
                  'qfx5110': 'fpc0',
                  'srx550': 'fwdd',
                  'acx1100': 'feb0',
                  'QFX5200-32c-32q': 'cli-pfe',
                  'unknown': None
                 }
        dh.get_model.side_effect = models.keys()
        for model in models:
            self.assertEqual(get_pfe(dh, 'xe-1/0/0'), models[model])

    def test_elog(self):
        #dt.strftime.return_value = '12:10'
        #self.assertTrue(elog('no_level') )
        elog('no_level')


if __name__ == '__main__':
    unittest.main()

