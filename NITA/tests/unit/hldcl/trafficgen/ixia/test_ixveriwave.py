import unittest2 as unittest
from mock import patch, MagicMock

from jnpr.toby.hldcl.trafficgen.ixia.ixveriwave import IxVeriwave
import telnetlib
import sys, os

class TestIxVeriwave(unittest.TestCase):

    def setUp(self):
        import builtins
        import yaml
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()


    @patch('telnetlib.Telnet.write')
    @patch('telnetlib.Telnet.expect')
    @patch('telnetlib.Telnet.__init__')
    @patch('builtins.super')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')
    def test_breakingpoint_init(self, host_log_patch, super_mock, telnet_mock, telnet_expect_patch, telnet_write_patch):
        super_mock.return_value = True
        ixveriwave_obj = IxVeriwave(system_data=create_system_data())
        telnet_mock.return_value = None
        telnet_expect_patch.side_effect = [[1, 0, b'test'], [1, 0, b'test'], [1, 0, b'test'], [1, 0, b'test']]
        try:
            ixveriwave_obj.connect()
            ixveriwave_obj.invoke(command='test')
        except Exception as error:
            print("ERROR: " + error)
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
    system_data['system']['primary']['debug'] = 'true'
    system_data['system']['primary']['group'] = 1
    system_data['system']['primary']['controllers'] = dict()
    system_data['system']['primary']['controllers']['re0'] = dict()
    system_data['system']['primary']['controllers']['re0']['hostname'] = 'abc'
    system_data['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    system_data['system']['primary']['controllers']['re0']['osname'] = 'IxVeriwave'
    system_data['system']['primary']['controllers']['re0']['user'] = 'test'
    system_data['system']['primary']['controllers']['re0']['password'] = 'test'
    system_data['system']['primary']['name'] = 'abc'
    system_data['system']['primary']['model'] = 'IxVeriwave'
    system_data['system']['primary']['make'] = 'IxVeriwave'
    system_data['system']['primary']['osname'] = 'IxVeriwave'
    return system_data

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestIxVeriwave)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
