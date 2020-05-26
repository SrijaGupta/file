"""
    UT for ciscosystem.py
"""

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.hldcl.cisco.ciscosystem import CiscoSystem

class TestCiscoSystem(unittest.TestCase):
    def setUp(self):
        import builtins 
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('sys.stdout')
    @patch('jnpr.toby.hldcl.cisco.ciscosystem.Cisco')
    @patch('jnpr.toby.hldcl.cisco.ciscosystem.System.__init__')
    @patch('jnpr.toby.hldcl.cisco.ciscosystem.Host._object_counts')
    def test_ciscosystem_init(self, host_patch, sup_init_patch, cisco_patch, stdout_patch):
        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        
        self.assertIsInstance(CiscoSystem(system_data), CiscoSystem)
        self.assertTrue(sup_init_patch.called)

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        from jnpr.toby.hldcl.cisco.cisco import Cisco
        cisco_patch = MagicMock(spec=Cisco)
        system_data['system']['primary']['controllers']['re1'] = {'test': {}, 'hostname' : 'xyz'}
        self.assertIsInstance(CiscoSystem(system_data), CiscoSystem)
        self.assertTrue(sup_init_patch.called)

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        system_data['system']['primary']['connect'] = True
        system_data['system']['primary']['controllers']['re1'] = {'test': {}, 'hostname' : 'xyz'}
        system_data['system']['primary']['controllers']['re0'] = {'test': {}, 'hostname' : 'xyz'}
        system_data['system']['secondary'] = system_data['system'].pop('primary')
        self.assertIsInstance(CiscoSystem(system_data, connect_dual_re=True), CiscoSystem)
                
        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        system_data['system']['primary']['controllers']['re0']['connect'] = True
        system_data['system']['primary']['controllers']['re1'] = {'test': {}, 'hostname' : 'xyz'}
        system_data['system']['secondary'] = system_data['system'].pop('primary')
        self.assertIsInstance(CiscoSystem(system_data), CiscoSystem)

        CiscoSystem.is_controller_connect_set = MagicMock(return_value=True)
        system_data['system']['secondary']['connect'] = True
        self.assertIsInstance(CiscoSystem(system_data), CiscoSystem)
        
        CiscoSystem.is_controller_connect_set = MagicMock(return_value=True)
        system_data['system']['secondary'].pop('connect')
        self.assertIsInstance(CiscoSystem(system_data), CiscoSystem)

    def test_ciscosystem_cli(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.cli.return_value = "test"
        self.assertEqual(CiscoSystem.cli(jobject), "test")

    def test_ciscosystem_config(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.config.return_value = "test"
        self.assertEqual(CiscoSystem.config(jobject), "test")
   
    def test_ciscosystem_save_config(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.save_config.return_value = "test"
        self.assertEqual(CiscoSystem.save_config(jobject), "test")

    def test_ciscosystem_load_config(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.load_config.return_value = "test"
        self.assertEqual(CiscoSystem.load_config(jobject), "test")

    def test_ciscosystem_clean_config(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.clean_config.return_value = "test"
        self.assertEqual(CiscoSystem.clean_config(jobject), "test")

    def test_ciscosystem_upgrade(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.upgrade.return_value = "test"
        self.assertEqual(CiscoSystem.upgrade(jobject), "test")

    def test_ciscosystem_switchover(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.switchover.return_value = "test"
        self.assertEqual(CiscoSystem.switchover(jobject), "test") 

def create_init_data():
    """
    Function to create init_data
    :return:
        Returns init_data
    """
    init_data = dict()
    init_data['t'] = dict()
    init_data['t']['resources'] = dict()
    init_data['t']['resources']['r0'] = dict()
    init_data['t']['resources']['r0']['system'] = dict()
    init_data['t']['resources']['r0']['system']['primary'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['osname'] = 'IOS'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['host'] = 'host1'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['model'] = '7200'
    init_data['t']['resources']['r0']['system']['primary']['osname'] = 'IOS'
    return init_data


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCiscoSystem)
    unittest.TextTestRunner(verbosity=2).run(suite)
