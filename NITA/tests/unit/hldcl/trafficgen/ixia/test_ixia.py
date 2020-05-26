import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from jnpr.toby.utils.iputils import ping
import os
import sys
from jnpr.toby.hldcl.trafficgen.ixia.ixia import Ixia
import telnetlib
import re


class TestIxia(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.Ixia._configure_promiscuous')
    @patch('builtins.super')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.Ixia._get_version')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.Ixia._get_lib_version')
    def test_ixia_init(self, get_lib_version_mock, get_version_mock, host_log_patch, super_mock, configure_promiscuous_mock):
        configure_promiscuous_mock.return_value = True
        super_mock.return_value = True
        get_lib_version_mock.return_value = '8.30.1350.13'
        get_version_mock.return_value = '8.30.1350.13'
        sys.modules['ixiatcl'] = MagicMock()
        sys.modules['ixiahlt'] = MagicMock()
        sys.modules['ixiangpf'] = MagicMock()
        ixia_obj = Ixia(system_data=create_system_data(), ixia_lib_path='/foo')
        ixia_obj.add_interfaces(interfaces=create_interface_data())
        ixia_obj.add_intf_to_port_map(intf_to_port_map={'intf1':'1/1'})
        try:
            ixia_obj.connect(port_list=['1/1'])
            ixia_obj.invoke(command='test')
        except Exception:
            #expecting status 0 since no real IXIA connection exists 
            pass

    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.Ixia._configure_promiscuous')
    @patch('builtins.super')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')
    @patch('jnpr.toby.utils.iputils.ping')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.Ixia._get_version')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.Ixia._get_lib_version')
    def test_device_reachabiliy(self,get_lib_version_mock, get_version_mock, ping_check_mock, host_log_patch, super_mock, promiscuous_mock):
        promiscuous_mock.return_value = True
        super_mock.return_value = True
        ping_check_mock.return_value = True
        get_lib_version_mock.return_value = '8.30.1350.13'
        get_version_mock.return_value = '8.30.1350.13'
        sys.modules['ixiatcl'] = MagicMock()
        sys.modules['ixiahlt'] = MagicMock()
        sys.modules['ixiangpf'] = MagicMock()
        ixia_obj = Ixia(system_data=create_system_data(), ixia_lib_path='/foo')
        try:
            print("test_device_reachabiliy test")
            check_device_reachabiliy(ixia_obj, ixia_obj.host)
            ping_check_mock.return_value = False
            check_device_reachabiliy(ixia_obj, ixia_obj.host)
        except Exception:
            pass

    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.time.sleep')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.re.search')
    @patch('telnetlib.Telnet')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.os.popen')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.Ixia._configure_promiscuous')
    @patch('builtins.super')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')
    @patch('jnpr.toby.utils.iputils.ping')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.Ixia._get_lib_version')
    def test_get_version(self,get_lib_version_mock, ping_check_mock, host_log_patch, super_mock, promiscuous_mock, popen_mock,
                         telnetlib_mock, re_search_mock, time_sleep_patch):
        promiscuous_mock.return_value = True
        super_mock.return_value = True
        ping_check_mock.return_value = True
        get_lib_version_mock.return_value = '8.30.1350.13'
        popen_mock.return_value = 'test'
        sys.modules['ixiatcl'] = MagicMock()
        sys.modules['ixiahlt'] = MagicMock()
        sys.modules['ixiangpf'] = MagicMock()
        telnetlib_mock.return_value = MagicMock()
        re_search_mock.return_value.group.return_value = '8.40'
        ixia_obj = Ixia(system_data=create_system_data(), ixia_lib_path='/foo')

def create_system_data():
    """
    Function to create system_data
    :return:
        Returns system_data
    """
    system_data = dict()
    system_data['system'] = dict()
    system_data['system']['primary'] = dict()
    system_data['system']['primary']['controllers'] = dict()
    system_data['system']['primary']['controllers']['re0'] = dict()
    system_data['system']['primary']['controllers']['re0']['hostname'] = 'abc'
    system_data['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    system_data['system']['primary']['controllers']['re0']['osname'] = 'IXIA'
    system_data['system']['primary']['name'] = 'abc'
    system_data['system']['primary']['model'] = 'IXIA'
    system_data['system']['primary']['make'] = 'IXIA'
    system_data['system']['primary']['osname'] = 'IXIA'
    system_data['system']['primary']['appserver'] = '2.2.2.2'
    system_data['system']['primary']['port-order'] = 'intf1'
    return system_data

def create_interface_data():
    """
    Function to create interface_data
    :return:
        Returns interface_data
    """
    interface_data = dict()
    interface_data['intf1'] = dict()
    interface_data['intf1']['name'] = '1/1'

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestIxia)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
