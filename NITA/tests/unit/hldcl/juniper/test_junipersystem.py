"""
    UT for junipersystem.py
"""

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.hldcl.juniper.junipersystem import JuniperSystem

class TestJuniperSystem(unittest.TestCase):
    def setUp(self):
        import builtins 
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('sys.stdout')
    @patch('jnpr.toby.hldcl.juniper.junipersystem.Juniper')
    @patch('jnpr.toby.hldcl.juniper.junipersystem.System.__init__')
    @patch('jnpr.toby.hldcl.juniper.junipersystem.Host._object_counts')
    def test_junipersystem_init(self, host_patch, sup_init_patch, juniper_patch, stdout_patch):
        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        
        self.assertIsInstance(JuniperSystem(system_data), JuniperSystem)
        self.assertTrue(sup_init_patch.called)

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        juniper_patch.return_value.is_master.return_value = True
        system_data['system']['primary']['controllers']['re1'] = {'test': {}, 'hostname' : 'xyz'}
        self.assertIsInstance(JuniperSystem(system_data), JuniperSystem)
        self.assertTrue(sup_init_patch.called)

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        juniper_patch.return_value.is_master.return_value = False
        system_data['system']['primary']['connect'] = True
        system_data['system']['primary']['controllers']['re1'] = {'test': {}, 'hostname' : 'xyz'}
        system_data['system']['secondary'] = system_data['system'].pop('primary')
        self.assertIsInstance(JuniperSystem(system_data, connect_dual_re=True), JuniperSystem)
        stdout_patch.write.assert_any_call("Skipping connection for controllerre0")
        stdout_patch.write.assert_any_call("Skipping connection for controllerre1")

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        system_data['system']['primary']['controllers']['re0']['connect'] = True
        system_data['system']['primary']['controllers']['re1'] = {'test': {}, 'hostname' : 'xyz'}
        system_data['system']['secondary'] = system_data['system'].pop('primary')
        self.assertIsInstance(JuniperSystem(system_data), JuniperSystem)

        JuniperSystem.is_controller_connect_set = MagicMock(return_value=True)
        system_data['system']['secondary']['connect'] = True
        self.assertIsInstance(JuniperSystem(system_data), JuniperSystem)
        
        JuniperSystem.is_controller_connect_set = MagicMock(return_value=True)
        system_data['system']['secondary'].pop('connect')
        self.assertIsInstance(JuniperSystem(system_data), JuniperSystem)

    def test_junipersystem_cli(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.cli.return_value = "test"
        self.assertEqual(JuniperSystem.cli(jobject), "test")

    def test_junipersystem_config(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.config.return_value = "test"
        self.assertEqual(JuniperSystem.config(jobject), "test")

    def test_junipersystem_commit(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.commit.return_value = "test"
        self.assertEqual(JuniperSystem.commit(jobject), "test")

    def test_junipersystem_save_config(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.save_config.return_value = "test"
        self.assertEqual(JuniperSystem.save_config(jobject), "test")

    def test_junipersystem_load_config(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.load_config.return_value = "test"
        self.assertEqual(JuniperSystem.load_config(jobject), "test")

    def test_junipersystem_get_rpc_equivalent(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.get_rpc_equivalent.return_value = "test"
        self.assertEqual(JuniperSystem.get_rpc_equivalent(jobject), "test")

    def test_junipersystem_execute_rpc(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.execute_rpc.return_value = "test"
        self.assertEqual(JuniperSystem.execute_rpc(jobject), "test")

    def test_junipersystem_switch_re_handle(self):
        jobject = MagicMock()
        jobject.current_node.switch_re_handle.return_value = "test"
        self.assertEqual(JuniperSystem.switch_re_handle(jobject), "test")

    @patch('jnpr.toby.hldcl.juniper.junipersystem.time.sleep')
    def test_junipersystem_software_install(self, time_patch):
        jobject = MagicMock()
        jobject.current_node.current_controller.software_install.return_value = "test"
        obj1 = MagicMock()
        obj2 = MagicMock()
        jobject.nodes = {'node0': obj1}
        obj1.controllers = {'re0': obj2}
        obj2.is_master.return_value = True
        self.assertEqual(JuniperSystem.software_install(jobject, controllers_all=False), True)

        # with issu
        obj2.is_master.return_value = False
        self.assertEqual(JuniperSystem.software_install(jobject, issu=True), True)

        # Exception
        jobject.current_node.current_controller.software_install.return_value = False
        self.assertRaises(Exception, JuniperSystem.software_install, jobject)        

    @patch('jnpr.toby.hldcl.juniper.junipersystem.time')
    def test_junipersystem_switch_re_master(self, time_patch):
        jobject = MagicMock()
        jobject.current_node.current_controller.is_master.return_value = True
        jobject.current_node.current_controller.switch_re_master.return_value = False
        self.assertFalse(JuniperSystem.switch_re_master(jobject))

        jobject.current_node.current_controller.switch_re_master.return_value = True
        self.assertFalse(JuniperSystem.switch_re_master(jobject))
        time_patch.sleep.assert_called_once_with(10)

        jobject.current_node.current_controller.is_master.side_effect = [True, False]
        self.assertTrue(JuniperSystem.switch_re_master(jobject))

    def test_junipersystem_vty(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.vty.return_value = False
        try :
            JuniperSystem.vty(jobject,command="",destination="")
        except :
            pass

        jobject.current_node.current_controller.vty.return_value = True
        self.assertTrue(JuniperSystem.vty(jobject, command="", destination=""))

    def test_junipersystem_cty(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.cty.return_value = False
        try :
            JuniperSystem.cty(jobject,command="",destination="")
        except :
            pass

        jobject.current_node.current_controller.cty.return_value = True
        self.assertTrue(JuniperSystem.cty(jobject, command="", destination=""))

    def test_junipersystem_detect_core(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        jobject = MagicMock(spec=JuniperSystem)
        jobject.nodes = {'primary': MagicMock()}
        jobject.nodes['primary'].current_controller.name = "re0"
        jobject.nodes['primary'].detect_core.return_value = 1
        self.assertEqual(JuniperSystem.detect_core(jobject), 1)

        import builtins
        builtins.t = MagicMock()
        builtins.t.t_get.return_value = "r0"
        builtins.t.log = MagicMock()
        jobject.nodes['primary'].detect_core.return_value = 0
        self.assertEqual(JuniperSystem.detect_core(jobject, resource="r0"), 0)

        jobject.nodes['secondary'] = jobject.nodes.pop('primary')
        self.assertEqual(JuniperSystem.detect_core(jobject, resource="r0"), 0)
   
    def test_junipersystem_pyez(self):
        jobject = MagicMock()
        jobject.current_node.current_controller.pyez.return_value = "test"
        self.assertEqual(JuniperSystem.pyez(jobject,command=''), "test") 
    
    def test_junipersystem_save_current_config(self):
        jobject = MagicMock()
        jobject.nodes= {'primary':MagicMock()}
        self.assertEqual(JuniperSystem.save_current_config(jobject,file=''), True)
        jobject.nodes= {}
        self.assertEqual(JuniperSystem.save_current_config(jobject,file=''), True)
    
    def test_junipersystem_load_saved_config(self):
        jobject = MagicMock()
        jsobj = MagicMock(spec=JuniperSystem)
        jsobj.nodes = {'secondary':''}
        jobject.nodes= {'primary':jsobj}
        jobject.detect_master_node.return_value = 'primary'
        jobject.vc = True
        #jobject.jsobj.load_saved_config.return_value = True
        self.assertEqual(JuniperSystem.load_saved_config(jobject,file=''), True)
        jobject.vc = False
        self.assertEqual(JuniperSystem.load_saved_config(jobject,file=''), True)
        jobject.nodes= {}
        del jobject.vc
        self.assertEqual(JuniperSystem.load_saved_config(jobject,file=''), True)

    def test_junipersystem_load_baseline_config(self):
        jobject = MagicMock(spec=JuniperSystem)
        jsobj   = MagicMock()
        jobject.nodes= {'primary':jsobj}
        jsobj.controllers = {'key1':'val1','key2':'val2'}
        self.assertEqual(JuniperSystem.load_baseline_config(jobject,load_config_from='path'), True)
        jsobj.controllers = {}
        self.assertEqual(JuniperSystem.load_baseline_config(jobject,load_config_from='path'), True)
   
    def test_junipersystem_check_interface_status(self):
        jobject = MagicMock()
        jobject.current_node.current_controller._check_interface_status.return_value = "test"
        self.assertEqual(JuniperSystem.check_interface_status(jobject,interfaces=''), "test")
          
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
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['osname'] = 'junos'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['host'] = 'host1'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['model'] = 'mx'
    init_data['t']['resources']['r0']['system']['primary']['osname'] = 'junos'
    return init_data


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestJuniperSystem)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()
