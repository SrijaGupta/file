import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import os
import sys
import atexit
from jnpr.toby.hldcl.trafficgen.warp17.warp17 import Warp17


class TestWarp17(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('atexit.register')
    @patch('builtins.super')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')
    def test_warp17_init(self, host_log_patch, super_mock, atexit_mock):
        super_mock.return_value = True
        sys.modules['warp17'] = MagicMock()
        warp17_obj = Warp17(system_data=create_system_data())
        warp17_obj.warp17 = MagicMock()
        warp17_obj.device_logger = MagicMock()
        warp17_obj.logger_name = MagicMock()
        warp17_obj.t_exists = MagicMock()
        warp17_obj.global_logger = MagicMock()
        try:
            warp17_obj.connect()
            warp17_obj.invoke(command='test')
        except Exception:
            #expecting status 0 since no real Warp17 connection exists 
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
    system_data['system']['primary']['controllers']['re0']['osname'] = 'linux'
    system_data['system']['primary']['name'] = 'abc'
    system_data['system']['primary']['warp17'] = 'enable'
    system_data['system']['primary']['model'] = 'Warp17'
    system_data['system']['primary']['make'] = 'Linux'
    system_data['system']['primary']['server-ip'] = '1.1.1.2'
    system_data['system']['primary']['osname'] = 'linux'
    return system_data

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestWarp17)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
