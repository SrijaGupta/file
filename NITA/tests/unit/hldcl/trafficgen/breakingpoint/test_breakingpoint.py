import unittest2 as unittest
from mock import patch, MagicMock

from jnpr.toby.hldcl.trafficgen.breakingpoint.breakingpoint import Breakingpoint
import sys, os

class TestBreakingpoint(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('jnpr.toby.hldcl.trafficgen.breakingpoint.breakingpoint.Breakingpoint._get_version')
    # @patch('jnpr.toby.hldcl.trafficgen.breakingpoint.breakingpoint.Breakingpoint._get_lib_version')
    @patch('jnpr.toby.hldcl.trafficgen.breakingpoint.breakingpoint.yaml.safe_load')
    @patch('builtins.open')
    @patch('builtins.super')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')
    def test_breakingpoint_init(self, host_log_patch, super_mock, open_mock, yaml_load_patch, get_version_mock, os_listdir_patch, os_path_isdir_patch):
        super_mock.return_value = True
        # get_lib_version_mock.return_value = '8.30.1350.13'
        get_version_mock.return_value = '8.10.1'
        yaml_load_patch.return_value = {'breakingpoint-lib-path':'/lib/path'}
        os_listdir_patch.return_value = ['8.10.1']
        os_path_isdir_patch.return_value = True
        sys.modules['bpsRest'] = MagicMock()
        bp_obj = Breakingpoint(system_data=create_system_data())
        bp_obj.add_intf_to_port_map(intf_to_port_map={'intf1':'1/1'})

        try:
            bp_obj.connect(port_list=['1/1'])
            bp_obj.invoke(command='test')
        except Exception:
            #expecting status 0 since no real Breakingpoint connection exists
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
    system_data['system']['primary']['controllers']['re0']['osname'] = 'BreakingPoint'
    system_data['system']['primary']['controllers']['re0']['user'] = 'test'
    system_data['system']['primary']['controllers']['re0']['password'] = 'test'
    system_data['system']['primary']['name'] = 'abc'
    system_data['system']['primary']['model'] = 'BreakingPoint'
    system_data['system']['primary']['make'] = 'BreakingPoint'
    system_data['system']['primary']['osname'] = 'BreakingPoint'
    system_data['system']['primary']['appserver'] = '2.2.2.2'
    system_data['system']['primary']['port-order'] = 'intf1'
    return system_data

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestBreakingpoint)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
