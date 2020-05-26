#!/usr/local/bin/python3

import sys

import mock
from mock import patch
from mock import Mock
from mock import MagicMock
import unittest
import unittest2 as unittest
from optparse import Values

#sys.modules['jnpr.toby.utils.linux'] = Mock()
#sys.modules['jnpr.toby.utils'] = Mock()
# sys.modules['TopoUtils'] = Mock()
# sys.modules['jnpr.toby.utils'] = Mock()
# sys.modules['utils'] = Mock()
# sys.modules['TopoUtils'] = Mock()


import builtins
builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

from jnpr.toby.trafficgen.ligen.ligen import ligen


class TestLigen(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()
        self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
        self.li_gen.log = t.log


    # #Passed
    def test_instanstiate_ligen_class(self):
        self.assertEqual(isinstance(ligen(test=None), ligen), True)


    # Passed
    def test_ligen_init_missing_args(self):
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None

        with self.assertRaises(Exception) as context:
            self.li_gen.init()
        self.assertTrue(
            'Missing mandatory argument, port_pair' in str(context.exception))

    # Passed
    # @patch(builtin_string + '.open')
    def test_ligen_init(self):
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        # self.li_gen.intf_data = {}
        # self.li_gen.intf_data['clnt'] = {}
        self.li_gen.intf_data['clnt']['uv-ip'] = '1.1.1.1'
        self.li_gen.intf_data['clnt']['uv-ipv6'] = '1.1.1.1'
        # self.li_gen.intf_data['srvr'] = {}
        self.li_gen.intf_data['srvr']['uv-ip'] = '1.1.1.1'
        self.li_gen.intf_data['srvr']['uv-ipv6'] = '1.1.1.1'
        self.li_gen._connect = MagicMock(sideeffect={})

        self.assertEqual(self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if']), True)

        # @patch(builtin_string + '.open')
    def test_ligen_init_missing_tar_details(self):

        self.li_gen = ligen()
        self.li_gen.log = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        with self.assertRaises(TypeError) as context:
            self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.assertTrue("Missing mandatory argument, tar_file_location/tar_file_name" in str(context.exception))

        # Passed
    def test_ligen_disconnect_is_connected_false(self):
        self.li_gen.is_connected = False

        self.assertEqual(self.li_gen.disconnect(), True)

    def test_ligen_disconnect(self):
        self.li_gen.is_connected = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.assertEqual(self.li_gen.disconnect(), True)


    def test_ligen_config_traffic_missing_args(self):
        self.li_gen.is_connected = True
        # is_intf_configured
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.li_gen.is_intf_configured = True
        with self.assertRaises(TypeError) as context:
            self.li_gen.configure_traffic()
        self.assertTrue("Missing mandatory arguments, ip_src_addr and ip_dst_addr" in str(context.exception))

        self.li_gen.is_intf_configured = False
        with self.assertRaises(RuntimeError) as context:
            self.li_gen.configure_traffic()
        self.assertTrue("Interfaces are not configured. configure_interfaces needs" in str(context.exception))
   
    def test_ligen_config_traffic_invalid_protocol(self):
        self.li_gen.is_connected = True
        self.li_gen.is_intf_configured = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        with self.assertRaises(TypeError) as context:
            self.li_gen.configure_traffic(ip_src_addr='1.1.1.1', ip_dst_addr='30.1.1.1', num_src_ips = 10, dst_port='80',protocol='abc')
        self.assertTrue("Invalid protocol" in str(context.exception))

    def test_ligen_config_traffic(self):
        self.li_gen.is_connected = True
        self.li_gen.is_intf_configured = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})
        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.li_gen.clnt_port = ""
        self.li_gen.srvr_port = ""

        self.li_gen._conf_subintf = MagicMock(sideeffect={})
        self.assertEqual(self.li_gen.configure_traffic(ip_src_addr='1.1.1.1', ip_dst_addr='30.1.1.1', num_src_ips = 10, dst_port='80', protocol='HttpBase', server_ip='1', vlan=10), True)
    
    def test_ligen_start_traffic_exception(self):
        self.li_gen.is_configured = False
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        with self.assertRaises(RuntimeError) as context:
            self.li_gen.start_traffic()
        self.assertTrue("No traffic profile is configured yet" in str(context.exception))
  
    @patch('jnpr.toby.utils.iputils.strip_mask')
    def test_ligen_start_traffic(self, test_patch):
        test_patch.return_value = None
        self.li_gen.is_configured = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})
        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.li_gen.clnt_hndl.shell = MagicMock()
        self.li_gen.clnt_hndl.shell.response = MagicMock()
        output = Mock()
        output.response =  MagicMock()
        output.response.return_value = 'Traffic started' 
        self.li_gen.clnt_hndl.shell.return_value = output
        self.li_gen.linux_tool_hndl = Values()
        self.li_gen.linux_tool_hndl.loop_ping = MagicMock(sideeffect={})
        self.li_gen.linux_tool_hndl.loop_ping.return_value = True
        self.li_gen.is_traffic_configured = True
        self.assertEqual(self.li_gen.start_traffic(), True)

    # @patch('jnpr.toby.utils.iputils.strip_mask')
    # def test_ligen_start_traffic_ping_failed(self, test_patch):
    #     test_patch.return_value = None
    #     self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #     self.li_gen.log = MagicMock(sideeffect={})
    #     self.li_gen.is_configured = True
    #     self.li_gen._verify_tar_version = MagicMock(sideeffect={})
    #     self.li_gen._verify_tar_version.return_value = False
    #     self.li_gen._setup_files = MagicMock(sideeffect={})
    #     self.li_gen._setup_files.return_value = None
    #     self.li_gen._get_res_info = MagicMock(sideeffect={})
    #     self.li_gen._get_res_info.return_value = None
    #     self.li_gen.resource = {}
    #     hndl = Values()
    #     hndl.su = MagicMock(sideeffect={})
    #     hndl.su.return_value = None
    #     hndl.shell = MagicMock(sideeffect={})
    #     hndl.shell.return_value = None
    #     nhndl = Values()
    #     nhndl.prompt = None
    #     for res in ['h0', 'h1']:
    #         self.li_gen.resource[res] = {}
    #         self.li_gen.resource[res]['obj'] = None
    #         self.li_gen.resource[res]['name'] = None
    #         self.li_gen.resource[res]['hndl'] = hndl
    #         self.li_gen.resource[res]['node_hndl'] = nhndl
    #         self.li_gen.resource[res]['prompt'] = None
    #     for res in ['clnt', 'srvr']:
    #         self.li_gen.intf_data[res] = {}
    #         self.li_gen.intf_data[res]['pic'] = None
    #     self.li_gen._connect = MagicMock(sideeffect={})

    #     self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
    #     self.li_gen.linux_tool_hndl = Values()
    #     self.li_gen.linux_tool_hndl.loop_ping = MagicMock(sideeffect={})
    #     self.li_gen.linux_tool_hndl.loop_ping.return_value = False
    #     with self.assertRaises(Exception) as context:
    #         self.li_gen.start_traffic()
    #     self.assertTrue("Ping failed as server is not reachable from client" in str(context.exception))
        # self.assertEqual(self.li_gen.start_traffic(), False)


    def test_ligen_stop_traffic_with_is_running_False(self):
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.assertEqual(self.li_gen.stop_traffic(), True)

    def test_ligen_stop_traffic(self):
        self.li_gen.is_running = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.li_gen.clnt_hndl.shell = MagicMock()
        self.li_gen.clnt_hndl.shell.response = MagicMock()
        output = Mock()
        output.response =  MagicMock()
        output.response.return_value = 'Traffic stopped' 
        self.li_gen.clnt_hndl.shell.return_value = output
        self.li_gen.linux_tool_hndl = Values()
        self.assertEqual(self.li_gen.stop_traffic(), True)

    def test_ligen_get_statistics(self):
        self.li_gen.is_running = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.li_gen.clnt_hndl.shell = MagicMock()
        self.li_gen.clnt_hndl.shell.response = MagicMock()
        stats = Mock()
        stats.response =  MagicMock()
        stats.response.return_value = 'client_stats = {"stat":10}' 
        self.li_gen.clnt_hndl.shell.return_value = stats

        self.assertEqual(self.li_gen.get_statistics(), {'stat': 10})

    def test_ligen_get_statistics_exception(self):
        self.li_gen.is_running = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.li_gen.clnt_hndl.shell = MagicMock()
        self.li_gen.clnt_hndl.shell.response = MagicMock()
        stats = Mock()
        stats.response =  MagicMock()
        stats.response.return_value = '' 
        self.li_gen.clnt_hndl.shell.return_value = stats
        self.li_gen.stats = {}
        with self.assertRaises(Exception) as context:
            self.li_gen.get_statistics()
        self.assertTrue("Error while retrieving statistics. The stats are empty" in str(context.exception))
     
    def test_ligen_get_session_count(self):
        self.li_gen.is_running = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.li_gen.get_statistics  = MagicMock()
        self.li_gen.stats = { 'udp': {'pkts_tx' : 10}}        
        proto_opts = Values()
        proto_opts.ip_src_addr = '1.1.1.1'
        proto_opts.num_src_ips = 1
        proto_opts.num_ports_per_src_ip = 1
        proto_opts.src_port = 1024
        proto_opts.ip_dst_addr = '1.1.1.1'
        proto_opts.dst_port = 1024
        proto_opts.protocol = 'Udp'
        self.li_gen.clnt_opts_list = [proto_opts]
        self.assertNotEqual(self.li_gen.get_session_count(), False)
   
    def test_ligen_get_sessions(self):
        self.li_gen.is_running = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        # self.li_gen._get_res_info = MagicMock(sideeffect={})
        # self.li_gen._get_res_info.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        proto_opts = Values()
        proto_opts.ip_src_addr = '1.1.1.1'
        proto_opts.num_src_ips = 1
        proto_opts.num_ports_per_src_ip = 1
        proto_opts.src_port = 1024
        proto_opts.ip_dst_addr = '1.1.1.1'
        proto_opts.dst_port = 1024
        proto_opts.protocol = 'Udp'
        self.li_gen.clnt_opts_list = [proto_opts]
        self.li_gen.is_pcp_configured = True        
        proto_opts = Values()
        proto_opts.client_ip = '1.1.1.1'
        proto_opts.intip = '1.1.1.1'
        proto_opts.num_int_ips = 1
        proto_opts.num_ports_per_int_ip = 1
        proto_opts.intport = 1024
        proto_opts.extip = '1.1.1.1'
        proto_opts.extport = 1024
        proto_opts.protocol = 'Udp'
        self.li_gen.pcp_opts_list = [proto_opts]
        # self.li_gen.clnt_opts = {}
        # self.li_gen.clnt_opts['udp'] = Values()
        # self.li_gen.clnt_opts['udp'].ip_src_addr = '1.1.1.3'
        # self.li_gen.clnt_opts['udp'].num_src_ips = 1
        # self.li_gen.clnt_opts['udp'].num_ports_per_src_ip = 1
        # self.li_gen.clnt_opts['udp'].src_port = 1024
        # self.li_gen.clnt_opts['udp'].ip_dst_addr = '1.1.1.1'
        # self.li_gen.clnt_opts['udp'].dst_port = '80'
        # self.li_gen.clnt_opts['udp'].protocol = 'udp'
        self.assertNotEqual(sorted(self.li_gen.get_sessions().items())[0][0], False)
    
    # def test_ligen_get_session_setup_rate(self):
    #     self.mocked_t = MagicMock()

    #     self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #     self.assertEqual(self.li_gen.get_session_setup_rate(), None)    

    # def test_ligen_gget_pkt_rate(self):
    #     self.mocked_t = MagicMock()

    #     self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #     self.assertEqual(self.li_gen.get_pkt_rate(), None) 

    # def test_ligen_add_stats(self):
    #     self.mocked_t = MagicMock()

    #     self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #     self.assertEqual(self.li_gen.add_stats(), None)
        
    @patch('jnpr.toby.trafficgen.ligen.ligen.linux_network_config.configure_ip_address')
    def test_ligen_configure_interfaces(self, test_patch):
        test_patch.return_value = None
        self.li_gen.intf_data = {}
        self.li_gen.intf_data['clnt'] = {}
        self.li_gen.intf_data['clnt']['uv-ip'] = '1.1.1.1'
        self.li_gen.intf_data['srvr'] = {}
        self.li_gen.intf_data['srvr']['uv-ip'] = '1.1.1.1'

        # self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.li_gen._add_routes = MagicMock()
        self.li_gen._add_routes.return_value = True

        self.linux_network_config = Values()
        self.linux_network_config.configure_ip_address = MagicMock()
        self.assertEqual(self.li_gen.configure_interfaces(clnt_port_ip='1.1.1.2/24', srvr_port_ip='2.2.2.2/24', clnt_gw_ip='1.1.1.1/24', srvr_gw_ip='2.2.2.1/24', clnt_port_ipv6='1.1.1.2/24', srvr_port_ipv6='2.2.2.2/24'), True)
        
    def test_ligen_configure_interfaces_server_exception(self):
        self.li_gen.intf_data = {}
        self.li_gen.intf_data['clnt'] = {}
        self.li_gen.intf_data['clnt']['uv-ip'] = '1.1.1.1'
        self.li_gen.intf_data['srvr'] = {}
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})


        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        with self.assertRaises(Exception) as context:
            self.li_gen.configure_interfaces(clnt_port_ip='1.1.1.2/24', clnt_gw_ip='1.1.1.1/24', srvr_gw_ip='2.2.2.1/24')
        self.assertTrue("Missing mandatory argument, srvr_port_ip" in str(context.exception))
  
    def test_ligen_configure_interfaces_client_exception(self):
        self.li_gen.intf_data = {}
        self.li_gen.intf_data['clnt'] = {}
        self.li_gen.intf_data['srvr'] = {}
        self.li_gen.intf_data['srvr']['uv-ip'] = '1.1.1.1'
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})


        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        with self.assertRaises(Exception) as context:
            self.li_gen.configure_interfaces( srvr_port_ip='2.2.2.2/24', clnt_gw_ip='1.1.1.1/24', srvr_gw_ip='2.2.2.1/24')
        self.assertTrue("Missing mandatory argument, clnt_port_ip" in str(context.exception))
    
    # @patch('jnpr.toby.trafficgen.ligen.ligen.linux_network_config.configure_ip_address')
    # def test_ligen_config_interface_exception(self, test_patch):
    #     test_patch.side_effect = Exception('Test')
    #     self.li_gen.intf_data['clnt'] = {}
    #     self.li_gen.intf_data['clnt']['uv-ip'] = '1.1.1.1'
    #     self.li_gen.intf_data['srvr'] = {}
    #     self.li_gen.intf_data['srvr']['uv-ip'] = '1.1.1.1'
    #     self.li_gen.log  = MagicMock()

    #     self.li_gen.add_static_route = MagicMock()
    #     self.li_gen.add_static_route.return_value = True
    #     with self.assertRaises(Exception) as context:
    #         self.li_gen.configure_interfaces( clnt_port_ip='1.1.1.2/24', srvr_port_ip='2.2.2.2/24', clnt_gw_ip='1.1.1.1/24', srvr_gw_ip='2.2.2.1/24')
    #     self.assertTrue("Error while configuring IP on client/server" in str(context.exception))
    
    @patch('jnpr.toby.services.utils.cmp_val')
    def test_ligen_verify_statistics(self, utils_cmp_val_patch):
      utils_cmp_val_patch.return_value = True
      self.mocked_t = MagicMock()
      self.li_gen.get_statistics = MagicMock()
      self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  10}}
      self.assertEqual(self.li_gen.verify_statistics(tol_perc=1, tol_val=10), True)
      self.li_gen.stats = { 'udp': { 'result' : 'FAIL', 'txns_tx' :  10 , "txns_rx" :  10}}
      with self.assertRaises(RuntimeError) as context:
            self.li_gen.verify_statistics()
      self.assertTrue("Traffic stats verification FAILED" in str(context.exception))
      # self.assertEqual(self.li_gen.verify_statistics(tol_perc=1, tol_val=10), False)

    # def test_ligen_verify_statistics_stats_empty_exception(self):
    #   self.mocked_t = MagicMock()
    #   self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #   self.li_gen.get_statistics = MagicMock()
    #   self.li_gen.stats = {}
    #   with self.assertRaises(Exception) as context:
    #         self.li_gen.verify_statistics()
    #   self.assertTrue("Stats retrieved from get_statistics are empty" in str(context.exception))
    #   # self.assertEqual(self.li_gen.verify_statistics(), True)

    @patch('jnpr.toby.services.utils.cmp_val')
    def test_ligen_verify_statistics_exception(self, utils_cmp_val_patch):
      utils_cmp_val_patch.return_value = False
      self.mocked_t = MagicMock()
      self.li_gen.get_statistics = MagicMock()
      self.li_gen.stats = { 'udp': { 'result' : 'FAIL', 'txns_tx' :  10 , "txns_rx" :  10}}
      with self.assertRaises(RuntimeError) as context:
            self.li_gen.verify_statistics()
      self.assertTrue("Traffic stats verification FAILED" in str(context.exception))
   
    @patch('jnpr.toby.services.utils.cmp_val')
    def test_ligen_verify_statistics_get_statistics(self, utils_cmp_val_patch):
      self.mocked_t = MagicMock()
      self.li_gen.get_statistics = MagicMock()
      self.li_gen.get_statistics.side_effect = Exception('statistic')
      self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  20}}
      with self.assertRaises(ValueError) as context:
            self.li_gen.verify_statistics()
      self.assertTrue("Error while retrieving statistics" in str(context.exception))
 
    def test_ligen_verify_statistics_mismatch_tx_rx(self):
      self.mocked_t = MagicMock()
      self.li_gen.get_statistics = MagicMock()
      self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  20}}
      # with self.assertRaises(Exception) as context:
      self.li_gen.verify_statistics()
      # self.assertTrue("Mismatch in the number of transactions sent and received for" in str(context.exception))

    def test_ligen_add_static_route_missing_args(self):
      self.mocked_t = MagicMock()
      self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  10}}
      with self.assertRaises(Exception) as context:
            self.li_gen.add_static_route()
      self.assertTrue("Missing mandatory argument(s), clnt_gw_ip/srvr_gw_ip" in str(context.exception))


    def test_ligen_add_static_route(self):
        self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  10}}
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        with self.assertRaises(Exception) as context:
            self.li_gen.add_static_route(clnt_gw_ip='1.1.1.1', srvr_gw_ip='1.1.1.2')
        self.assertTrue("Error while configuring static routes" in str(context.exception))

    @patch('jnpr.toby.trafficgen.ligen.ligen.linux_network_config.add_route')
    def test_ligen_add_static_route_ip_list_client(self, test_patch):
      test_patch.return_value = None

      self.li_gen.msg = ''
      self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  10}}

      self.linux_network_config = Values()
      self.linux_network_config.add_route = MagicMock()
      self.assertEqual(self.li_gen.add_static_route(clnt_gw_ip='1.1.1.1', srvr_gw_ip='1.1.1.2', ip_list=['112.1.1.0/24'], device='client'), True)
    
    @patch('jnpr.toby.trafficgen.ligen.ligen.linux_network_config.add_route')
    def test_ligen_add_static_route_ipv6_list_client(self, test_patch):
      test_patch.return_value = None

      self.li_gen.msg = ''
      self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  10}}

      self.linux_network_config = Values()
      self.linux_network_config.add_route = MagicMock()
      self.assertEqual(self.li_gen.add_static_route(clnt_gw_ipv6='2001:0:3238:DFE1:63:1:1:1/64', srvr_gw_ipv6='2001:0:3238:DFE1:66:1:1:2/64', ipv6_list=['9::/64'], device='client'), True)

    @patch('jnpr.toby.trafficgen.ligen.ligen.linux_network_config.add_route')
    def test_ligen_add_static_route_ip_list_server(self, test_patch):
      test_patch.return_value = None

      self.li_gen.msg = ''
      self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  10}}

      self.linux_network_config = Values()
      self.linux_network_config.add_route = MagicMock()
      self.assertEqual(self.li_gen.add_static_route(clnt_gw_ip='1.1.1.1', srvr_gw_ip='1.1.1.2', ip_list=['112.1.1.0/24'], device='server'), True)

    @patch('jnpr.toby.trafficgen.ligen.ligen.linux_network_config.add_route')
    def test_ligen_add_static_route_ip_list_server(self, test_patch):
      test_patch.return_value = None

      self.li_gen.msg = ''
      self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  10}}

      self.linux_network_config = Values()
      self.linux_network_config.add_route = MagicMock()
      self.assertEqual(self.li_gen.add_static_route(clnt_gw_ipv6='2::1/64', srvr_gw_ipv6='9::1/64', ipv6_list=['9::/64'], device='server'), True)
 
    @patch('jnpr.toby.trafficgen.ligen.ligen.linux_network_config.add_route')
    def test_ligen_add_routes(self, test_patch):
        self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
        self.li_gen.log = t.log
        test_patch.return_value = None
        self.li_gen.msg = ''
        self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  10}}

        #self.linux_network_config = Values()
        self.li_gen.srvr_port_ip = '1.1.1.1'
        self.li_gen.srvr_port_ip_netmask = '255.255.255.255'
        self.li_gen.clnt_gw_ip = '2.1.1.1'      
        self.li_gen.clnt_port_ip = '1.1.1.1'
        self.li_gen.clnt_port_ip_netmask = '255.255.255.255'
        self.li_gen.srvr_gw_ip = '2.1.1.1'
        self.li_gen.srvr_port_ipv6 = '1.1.1.1'
        self.li_gen.srvr_port_ipv6_netmask = '255.255.255.255'
        self.li_gen.clnt_gw_ipv6 = '2.1.1.1'      
        self.li_gen.clnt_port_ipv6 = '1.1.1.1'
        self.li_gen.clnt_port_ipv6_netmask = '255.255.255.255'
        self.li_gen.srvr_gw_ipv6 = '2.1.1.1'
        #self.linux_network_config.add_route = MagicMock()
        self.assertEqual(self.li_gen._add_routes(), True)

    # @patch('jnpr.toby.trafficgen.ligen.ligen.linux_network_config.add_route')
    # def test_ligen_add_routes_exception(self, test_patch):
    #   test_patch.side_effect = Exception('Test')
    #   self.li_gen.msg = ''
    #   self.li_gen.stats = { 'udp': { 'result' : 'PASS', 'txns_tx' :  10 , "txns_rx" :  10}}  
    #   with self.assertRaises(Exception) as context:
    #         self.li_gen._add_routes()
    #   self.assertTrue("Error while configuring static routes " in str(context.exception))

    @patch('jnpr.toby.frameworkDefaults.credentials.get_credentials')
    def test_setup_files(self, test_patch):
        self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
        self.li_gen.log = t.log
        scp = Values()
        scp.open = MagicMock()
        scp.put_file = MagicMock()
        test_patch.return_value = ('regress', 'MaRtInI')
        self.li_gen.dev_hndl = Values()
        self.li_gen.dev_hndl.shell = MagicMock()
        self.li_gen._create_ssh_client = MagicMock()
        self.li_gen.scp_clnt = MagicMock()
        scp = Values()
        scp.put = MagicMock()
        self.li_gen.scp_clnt.return_value = scp
        self.li_gen.base_setup = True
        self.assertEqual(self.li_gen._setup_files('Test', self.li_gen.dev_hndl), True)

    # @patch('jnpr.toby.frameworkDefaults.credentials.get_credentials')
    # def test_setup_files_user_pass_passed(self, test_patch):
    #     self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #     self.li_gen.log = t.log
    #     scp = Values()
    #     scp.open = MagicMock()
    #     scp.put_file = MagicMock()
    #     test_patch.return_value = ('regress', 'MaRtInI')

    #     self.li_gen.dev_hndl = Values()
    #     self.li_gen.dev_hndl.shell = MagicMock()
    #     self.li_gen._create_ssh_client = MagicMock()
    #     self.li_gen.SCPClient = MagicMock()
    #     self.li_gen.scp = Values()
    #     self.li_gen.scp.put = MagicMock()


    #     self.assertEqual(self.li_gen._setup_files('Test', self.li_gen.dev_hndl, scp_upload_username='regress', scp_upload_password='MaRtInI'), True)

    # @patch('jnpr.toby.trafficgen.ligen.ligen.scp.SCP')
    # def test_setup_files(self, test_patch):
    #   self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #   test_patch.side_effect = None
    #   scp = Values()
    #   scp.open = MagicMock()
    #   scp.put_file = MagicMock()
    #   test_patch.return_value = scp

    #   self.li_gen.dev_hndl = Values()
    #   self.li_gen.dev_hndl.shell = MagicMock()

    #   self.assertEqual(self.li_gen._setup_files('Test', self.li_gen.dev_hndl), None)

    # @patch('jnpr.toby.trafficgen.ligen.ligen.scp.SCP')
    # def test_setup_files_base_setup_true(self):
    #     self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #     self.li_gen.log = t.log
    #     scp = Values()
    #     scp.open = MagicMock()
    #     scp.put_file = MagicMock()

    #     self.li_gen.dev_hndl = Values()
    #     self.li_gen.dev_hndl.shell = MagicMock()
    #     self.li_gen.base_setup = True
    #     self.li_gen._create_ssh_client = MagicMock()
    #     self.li_gen.SCPClient = MagicMock()
    #     self.li_gen.scp = Values()
    #     self.li_gen.scp.put = MagicMock()

    #     self.assertEqual(self.li_gen._setup_files('Test', self.li_gen.dev_hndl), True)

    def test_create_ssh_client(self):
        client = Values()
        client.load_system_host_keys = MagicMock()
        client.set_missing_host_key_policy = MagicMock()
        client.connect = MagicMock()
        self.li_gen.paramiko = Values()
        self.li_gen.paramiko.SSHClient = MagicMock()
        self.li_gen.paramiko.SSHClient.return_value = client
        test = Values()
        self.assertEqual(type(self.li_gen._create_ssh_client('Test', 'Test', 'Test', 'Test')), type(test))    
   

    # @patch('jnpr.toby.trafficgen.ligen.ligen.scp.SCP')
    # def test_setup_files_base_setup_true(self, test_patch):
    #   self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #   test_patch.side_effect = None
    #   scp = Values()
    #   scp.open = MagicMock()
    #   scp.put_file = MagicMock()
    #   test_patch.return_value = scp

    #   self.li_gen.dev_hndl = Values()
    #   self.li_gen.dev_hndl.shell = MagicMock()
    #   self.li_gen.base_setup = True

    #   self.assertEqual(self.li_gen._setup_files('Test', self.li_gen.dev_hndl), None)
    @patch('jnpr.toby.trafficgen.ligen.ligen.re.search')
    @patch('jnpr.toby.trafficgen.ligen.ligen.importlib.machinery.SourceFileLoader')
    # @patch(builtin_string + '.open')
    def test_ligen_verify_tar_version(self, test_patch, test_patch_new):
      test_lig = Values()
      test_lig.ligen_pkg_version = '01.00'
      test_ver = Values()
      test_ver.load_module = MagicMock()
      test_ver.load_module.return_value = test_lig 

      test_patch.return_value = test_ver
      # test_patch.load_module = MagicMock()
      # test_patch.load_module.return_value = test_ver

      test = Values()
      test.group =  MagicMock()
      test.group.return_value =  '01.00'
      # test_patch_new.return_value = True
      test_patch_new.return_value = test

      self.li_gen.clnt_hndl = MagicMock()
      self.li_gen.clnt_hndl.shell = MagicMock()
      self.li_gen.clnt_hndl.shell.response = MagicMock()
      self.li_gen.clnt_hndl.shell.response.return_value = 'ligen_pkg_version = "(01.00)"'
      self.li_gen.response =  'ligen_pkg_version = "(01.00)"'
      # self.li_gen.tar_file_location = "/"
      self.assertEqual(self.li_gen._verify_tar_version(self.li_gen.clnt_hndl), True)
    
    @patch('jnpr.toby.trafficgen.ligen.ligen.re.search')
    @patch('jnpr.toby.trafficgen.ligen.ligen.importlib.machinery.SourceFileLoader')
    def test_ligen_verify_tar_version_exception(self, test_patch, test_patch_new):
      test_lig = Values()
      test_lig.ligen_pkg_version = '01.00'
      test_ver = Values()
      test_ver.load_module = MagicMock()
      test_ver.load_module.return_value = test_lig 

      test_patch.return_value = test_ver

      test = Values()
      test.group =  MagicMock()
      test.group.return_value =  1
      # test_patch_new.return_value = True
      test_patch_new.return_value = test

      self.li_gen.clnt_hndl = MagicMock()
      self.li_gen.clnt_hndl.shell = MagicMock()
      self.li_gen.clnt_hndl.shell.side_effect = Exception('Test')
      self.assertEqual(self.li_gen._verify_tar_version(self.li_gen.clnt_hndl), False)

    def test_ligen_connect(self):
        self.li_gen.clnt_hndl = Values()
        self.li_gen.srvr_hndl = Values()
        # self.clnt_hndl.su = MagicMock(sideeffect={})
        # self.clnt_hndl.su.return_value = None 
        self.li_gen.clnt_node_hndl = Values()
        self.li_gen.srvr_node_hndl = Values()
        self.li_gen.clnt_node_hndl.prompt = None
        self.li_gen.srvr_node_hndl.prompt = None
        self.li_gen.clnt_hndl.shell = MagicMock(sideeffect={})
        self.li_gen.srvr_hndl.shell = MagicMock(sideeffect={})
        self.li_gen.clnt_hndl.shell.return_value = None
        self.li_gen.srvr_hndl.shell.return_value = None
        self.dmn_cmd = None
        self.dmn_prompt = None
        self.assertEqual(self.li_gen._connect(), True)

    def test_ligen_connect_exception(self):
        self.li_gen.msg = ''
        self.li_gen.clnt_hndl = Values()
        self.li_gen.srvr_hndl = Values()
        # self.clnt_hndl.su = MagicMock(sideeffect={})
        # self.clnt_hndl.su.return_value = None 
        self.li_gen.clnt_node_hndl = Values()
        self.li_gen.srvr_node_hndl = Values()
        self.li_gen.clnt_node_hndl.prompt = None
        self.li_gen.srvr_node_hndl.prompt = None
        self.li_gen.clnt_hndl.shell = MagicMock(sideeffect={})
        self.li_gen.srvr_hndl.shell = MagicMock(sideeffect={})
        self.li_gen.clnt_hndl.shell.return_value = None
        self.li_gen.srvr_hndl.shell.return_value = None
        self.dmn_cmd = None
        self.dmn_prompt = None
        self.assertEqual(self.li_gen._connect(), True) 

    def test_ligen_connect_exception(self):
      self.li_gen.msg = ''
      self.li_gen.clnt_hndl = MagicMock()
      self.li_gen.clnt_hndl.shell = MagicMock()
      self.li_gen.clnt_hndl.shell.side_effect = Exception('A custom value error')
      self.li_gen.srvr_hndl = MagicMock()
      self.li_gen.srvr_hndl.shell = MagicMock()
      with self.assertRaises(Exception) as context:
            self.li_gen._connect()
      self.assertTrue("Unable to set the ulimit -n config" in str(context.exception))

    def test_ligen_get_res_info(self):
        self.li_gen.msg = ''
        self.li_gen.resource = {}

        res_info = {}
        res_info['system'] = {}
        res_info['system']['primary'] = {}
        res_info['system']['primary']['name'] = {}
        hndl = Values()
        hndl.prompt = None
        t.get_resource = MagicMock()
        t.get_resource.return_value = res_info
        t.get_interface = MagicMock()
        t.get_interface.return_value = None
        t.get_handle = MagicMock()
        t.get_handle.return_value = hndl
        self.li_gen.intf_data = {}
        self.assertEqual(self.li_gen._get_res_info(res='h0'), None)

    def test_ligen_init_update_pkg_false(self):
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})

        self.assertEqual(self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'], update_pkg=False), True)

    def test_ligen_init_self_connect_false(self):
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = True
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen.connect = False 
        self.li_gen._connect = MagicMock(sideeffect={})

        self.assertEqual(self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if']), True)

    @patch('jnpr.toby.trafficgen.ligen.ligen.linux_network_config.configure_ip_address')
    def test_ligen_configure_interfaces_gw_ip_none(self, test_patch):
        test_patch.return_value = None
        self.li_gen.intf_data = {}
        self.li_gen.intf_data['clnt'] = {}
        self.li_gen.intf_data['clnt']['uv-ip'] = '1.1.1.1'
        self.li_gen.intf_data['srvr'] = {}
        self.li_gen.intf_data['srvr']['uv-ip'] = '1.1.1.1'
        self.li_gen._add_routes = MagicMock()
        self.li_gen._add_routes.return_value = True

        self.linux_network_config = Values()
        self.linux_network_config.configure_ip_address = MagicMock()
        self.assertEqual(self.li_gen.configure_interfaces(clnt_port_ip='1.1.1.2/24', srvr_port_ip='2.2.2.2/24'), True)


    def test_ligen_config_traffic_num_src_ips_less_than_one(self):
        self.li_gen.is_connected = True
        self.li_gen.is_intf_configured = True
        self.li_gen._verify_tar_version = MagicMock(sideeffect={})
        self.li_gen._verify_tar_version.return_value = False
        self.li_gen._setup_files = MagicMock(sideeffect={})
        self.li_gen._setup_files.return_value = None
        self.li_gen._get_res_info = MagicMock(sideeffect={})
        self.li_gen._get_res_info.return_value = None
        self.li_gen.resource = {}
        hndl = Values()
        hndl.su = MagicMock(sideeffect={})
        hndl.su.return_value = None
        hndl.shell = MagicMock(sideeffect={})
        hndl.shell.return_value = None
        nhndl = Values()
        nhndl.prompt = None
        for res in ['h0', 'h1']:
            self.li_gen.resource[res] = {}
            self.li_gen.resource[res]['obj'] = None
            self.li_gen.resource[res]['name'] = None
            self.li_gen.resource[res]['hndl'] = hndl
            self.li_gen.resource[res]['node_hndl'] = nhndl
            self.li_gen.resource[res]['prompt'] = None
            self.li_gen.resource[res]['ip'] = None
        for res in ['clnt', 'srvr']:
            self.li_gen.intf_data[res] = {}
            self.li_gen.intf_data[res]['pic'] = None
        self.li_gen._connect = MagicMock(sideeffect={})
        self.li_gen._connect = MagicMock(sideeffect={})
        self.li_gen._conf_subintf = MagicMock(sideeffect={})
        self.li_gen.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'])
        self.assertEqual(self.li_gen.configure_traffic(ip_src_addr='1.1.1.1', ip_dst_addr='30.1.1.1', dst_port='80', protocol='Udp', num_src_ips=0), True)
      # with self.assertRaises(Exception) as context:
      #       self.li_gen._connect()
      # self.assertTrue("Unable to set the ulimit -n config" in str(context.exception))

    # @patch(builtin_string + '.open')
    # def test_ligen_verify_tar_version_not_equal_else(self, test_patch):
    #   print('Test')
    #   self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
    #   self.assertEqual(self.li_gen._verify_tar_version('Test'), False)
    def test_configure_pcp_map_request(self):
        self.li_gen.is_pcp_configured = True
        self.li_gen.clnt_hndl = MagicMock()
        self.li_gen.clnt_hndl.shell = MagicMock()
        self.li_gen.is_intf_configured = False
        with self.assertRaises(RuntimeError) as context:
            self.li_gen.configure_pcp_map_request()
        self.assertTrue("Interfaces are not configured" in str(context.exception))
        self.li_gen.is_intf_configured = True
        with self.assertRaises(TypeError) as context:
            self.li_gen.configure_pcp_map_request()
        self.assertTrue("Missing mandatory arguments" in str(context.exception))
        
        self.assertEqual(self.li_gen.configure_pcp_map_request(client_ip=1, server_ip=1, map_intport=0, map_extip=0, map_extport=0), True)


    def test_start_pcp_map_requests(self):
        self.li_gen.is_pcp_configured = True
        self.li_gen.clnt_hndl = MagicMock()
        self.li_gen.clnt_hndl.shell = MagicMock()
        self.assertEqual(self.li_gen.start_pcp_map_requests(), True)
        self.li_gen.is_pcp_configured = False
        with self.assertRaises(RuntimeError) as context:
            self.li_gen.start_pcp_map_requests()
        self.assertTrue("No PCP Map requests are configured yet" in str(context.exception))
  
    @patch('jnpr.toby.utils.iputils.strip_mask')
    def test_check_connectivity(self, test_patch):
        self.li_gen.is_traffic_configured = True
        self.li_gen.clnt_hndl = MagicMock()
        self.li_gen.clnt_hndl.shell = MagicMock()
        self.li_gen.linux_tool_hndl = Values()
        self.li_gen.linux_tool_hndl.loop_ping = MagicMock(sideeffect={})
        self.li_gen.linux_tool_hndl.loop_ping.return_value = True
        self.li_gen.clnt_hndl = MagicMock()
        self.assertEqual(self.li_gen.check_connectivity(), True)
        self.li_gen.linux_tool_hndl.loop_ping.return_value = False
        with self.assertRaises(RuntimeError) as context:
            self.li_gen.check_connectivity()
        self.assertTrue("Ping failed as server is not reachable from client" in str(context.exception))
        self.li_gen.is_traffic_configured = False
        with self.assertRaises(RuntimeError) as context:
            self.li_gen.check_connectivity()
        self.assertTrue("No traffic profile is configured yet" in str(context.exception))

    @patch('jnpr.toby.utils.iputils.strip_mask')
    @patch('jnpr.toby.utils.iputils.get_network_mask')
    def test_conf_subintf(self, net_mask, strip_mask):
        net_mask.return_value = '255.255.255.1'
        strip_mask.return_value = '10.0.0.1'
        self.li_gen = ligen(tar_file_name='ligen_setup.tar.gz', tar_file_location='/volume/labtools/lib/Testsuites/ligen/')
        self.li_gen.log = t.log
        self.li_gen.clnt_hndl = MagicMock()
        self.li_gen.clnt_hndl.shell = MagicMock()
        self.assertEqual(self.li_gen._conf_subintf(name="client", start_ip='10.0.0.1', interface="eth1.10", count=10, start_unit=1), True)

    def test_delete_all_profiles(self):
        self.li_gen.clnt_hndl = MagicMock()
        self.li_gen.clnt_hndl.shell = MagicMock()
        self.li_gen.srvr_hndl = MagicMock()
        self.li_gen.srvr_hndl.shell = MagicMock()
        self.assertEqual(self.li_gen.delete_all_profiles(),True)


if __name__ == '__main__':
    unittest.main()