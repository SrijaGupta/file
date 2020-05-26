import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import os
import sys
import atexit

from jnpr.toby.hldcl.trafficgen.calnex.paragon import Paragon


class TestParagon(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('atexit.register')
    @patch('builtins.super')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')
    def test_paragon_init(self, host_log_patch, super_mock, atexit_mock):
        super_mock.return_value = True
        sys.modules['paragon'] = MagicMock()
        paragon_obj = Paragon(system_data=create_system_data(), paragon_lib_path='/foo')
        paragon_obj.device_logger = MagicMock()
        paragon_obj.logger_name = MagicMock()
        paragon_obj.t_exists = MagicMock()
        paragon_obj.global_logger = MagicMock()
        try:
            paragon_obj.connect()
            paragon_obj.invoke(command='test')
        except Exception:
            #expecting status 0 since no real Paragon connection exists 
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
    system_data['system']['primary']['controllers']['re0']['osname'] = 'Paragon'
    system_data['system']['primary']['name'] = 'abc'
    system_data['system']['primary']['model'] = 'Paragon'
    system_data['system']['primary']['make'] = 'Calnex'
    system_data['system']['primary']['server-ip'] = '1.1.1.2'
    system_data['system']['primary']['osname'] = 'Paragon'
    return system_data

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestParagon)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
