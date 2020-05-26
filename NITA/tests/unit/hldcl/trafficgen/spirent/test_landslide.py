import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import os
import sys

from jnpr.toby.hldcl.trafficgen.spirent.landslide import Landslide


class TestLandslide(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('builtins.super')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')
    @patch('jnpr.toby.hldcl.trafficgen.spirent.landslide.Landslide._get_version')
    def test_landslide_init(self, get_version_mock, host_log_patch, super_mock):
        super_mock.return_value = True
        get_version_mock.return_value = '4.77'
        sys.modules['ls'] = MagicMock()
        landslide_obj = Landslide(system_data=create_system_data(), landslide_lib_path='/foo', landslide_jre_path='/foo', landslide_tcl_bin='foo')
#        landslide_obj.add_interfaces(interfaces=create_interface_data())
        landslide_obj.add_intf_to_port_map(intf_to_port_map={'intf1':'1/1'})
        try:
            landslide_obj.connect(port_list=['1/1'])
            landslide_obj.invoke(command='test')
        except Exception:
            #expecting status 0 since no real SPIRENT connection exists 
            pass

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
    system_data['system']['primary']['controllers']['re0']['osname'] = 'SPIRENT'
    system_data['system']['primary']['name'] = 'abc'
    system_data['system']['primary']['model'] = 'SPIRENT'
    system_data['system']['primary']['make'] = 'SPIRENT'
    system_data['system']['primary']['osname'] = 'SPIRENT'
    system_data['system']['primary']['landslide-manager'] = '2.2.2.2'
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
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestLandslide)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
