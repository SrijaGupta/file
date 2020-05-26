"""
Init.py Unit Test
"""
import unittest2 as unittest
from mock import patch, MagicMock, call
from importlib import reload
import builtins,sys,jnpr.toby.init.init,importlib
from jnpr.toby.init.init import init
from lxml import etree
from collections import defaultdict


class TestInit(unittest.TestCase):
    """
    TestInit class to handle Init.py unit tests
    """
  
    def __check_assertion__(self, init_data=None):
        """
        Function to check exceptions raised
        :param init_data:
            init_data required for checking assertions
        :return:
            Returns true or false depending on test results
        """
        init_obj = init()
        del init_data['t']['resources']['r0']['system']['primary']['osname']
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system']['primary']['osname'] = 'junos'

        del init_data['t']['resources']['r0']['system']['primary']['model']
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system']['primary']['model'] = 'mx'

        del init_data['t']['resources']['r0']['system']['primary']['name']
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system']['primary']['name'] = 'abc'

        del init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname']
        del init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip']
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'

        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = 'abc'
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'

        init_data['t']['resources']['r0']['system']['primary']['controllers'] = 're0'
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'

        del init_data['t']['resources']['r0']['system']['primary']['controllers']
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'

        del init_data['t']['resources']['r0']['interfaces']['fe0']['name']
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['interfaces']['fe0']['name'] = 'fe0.0'

        init_data['t']['resources']['r0']['interfaces']['fe0'] = 'fe0.0'
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['interfaces']['fe0'] = dict()
        init_data['t']['resources']['r0']['interfaces']['fe0']['name'] = 'fe0.0'
        init_data['t']['resources']['r0']['interfaces']['fe0']['link'] = 'link'

        init_data['t']['resources']['r0']['interfaces'] = 'fe0'
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['interfaces'] = dict()
        init_data['t']['resources']['r0']['interfaces']['fe0'] = dict()
        init_data['t']['resources']['r0']['interfaces']['fe0']['name'] = 'fe0.0'
        init_data['t']['resources']['r0']['interfaces']['fe0']['link'] = 'link'

        init_data['t']['resources']['r0']['system']['primary'] = 're0'
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system']['primary'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
        init_data['t']['resources']['r0']['system']['primary']['name'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['model'] = 'mx'
        init_data['t']['resources']['r0']['system']['primary']['make'] = 'Juniper'
        init_data['t']['resources']['r0']['system']['primary']['osname'] = 'junos'

        del init_data['t']['resources']['r0']['system']['primary']
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system']['primary'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
        init_data['t']['resources']['r0']['system']['primary']['name'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['model'] = 'mx'
        init_data['t']['resources']['r0']['system']['primary']['make'] = 'Juniper'
        init_data['t']['resources']['r0']['system']['primary']['osname'] = 'junos'

        init_data['t']['resources']['r0']['system'] = 'primary'
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system'] = dict()
        init_data['t']['resources']['r0']['system']['primary'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
        init_data['t']['resources']['r0']['system']['primary']['name'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['model'] = 'mx'
        init_data['t']['resources']['r0']['system']['primary']['make'] = 'Juniper'
        init_data['t']['resources']['r0']['system']['primary']['osname'] = 'junos'

        del init_data['t']['resources']['r0']['system']
        self.assertRaises(Exception, init_obj.Initialize, init_file='init_file', force=True)
        init_data['t']['resources']['r0']['system'] = dict()
        init_data['t']['resources']['r0']['system']['primary'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
        init_data['t']['resources']['r0']['system']['primary']['name'] = 'abc'
        init_data['t']['resources']['r0']['system']['primary']['model'] = 'mx'
        init_data['t']['resources']['r0']['system']['primary']['make'] = 'Juniper'
        init_data['t']['resources']['r0']['system']['primary']['osname'] = 'junos'


    @patch('jnpr.toby.init.init.get_script_name')
    @patch('jnpr.toby.init.init.get_log_dir')
    def test_init(self, get_logdir_mock, get_scriptname_mock):
        get_logdir_mock.return_value = 'log_dir'
        get_scriptname_mock.return_value = 'script_name'
        init_obj = init(initialize_t=True)   
        self.assertEqual(init_obj._log_dir, 'log_dir')
        self.assertEqual(init_obj._script_name, 'script_name')
        self.assertEqual(init_obj.is_robot, False)

    @patch('robot.libraries.BuiltIn.BuiltIn')
    @patch('robot.libraries.BuiltIn._Misc')
    @patch('robot.api.logger.console')
    def test_init_exception(self, robot_api_mock, robot_misc_mock, robot_builtin_mock):
        reload(jnpr.toby.init.init)
        init_obj = init()
        self.assertEqual(init_obj.is_robot, True)

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.platform')
    @patch('jnpr.toby.init.init.Vars')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.Logger')
    @patch('jnpr.toby.init.init.os.unlink')
    @patch.dict('os.environ',{'USER':'regress'})
    def test_initialize(self, os_mock, logger_mock, yaml_mock, open_mock, connect_mock, vars_mock, platform_mock,
                        server_patch, log_file_version_patch):
        os_mock.return_value = True
        from jnpr.toby.init.init import init 
        init_obj = init()
        init_obj.is_robot = True
        init_obj.robot_log_level = None
        logger_mock.return_value.log_dir.return_value = 'dir'
        yaml_mock.safe_load.return_value = ''
        open_mock.return_value = True
        try:
            init_obj.Initialize(init_file='init_file', force=True)
        except Exception:
            self.assertTrue(yaml_mock.safe_load.called)

        init_data = create_init_data()
        yaml_mock.safe_load.return_value = init_data
        connect_mock.return_value = True
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        from jnpr.toby.init.init import init
        init_obj = init()
        init_obj.is_robot = True
        init_obj.robot_log_level = "INFO"
        self.__check_assertion__(init_data)
        logger_mock.return_value.log_dir.return_value = 'dir'
        init_obj.Initialize(init_file='abc.yaml:efg.yaml', force=True)    
        self.assertEqual(init_obj.t_dict, init_data['t'])

        from jnpr.toby.init.init import init
        init_obj = init()
        init_obj.is_robot = False
        vars_mock.get_global_variable.return_value = True
        logger_mock.return_value.log_dir.return_value = 'dir'
        yaml_mock.safe_load.return_value = init_data
        platform_mock.system.return_value = 'Linux'
        init_obj.Initialize(init_file=None, force=True)

        init_data = {}
        yaml_mock.safe_load.return_value = init_data
        try:
            init_obj.Initialize(init_file=None, force=True)
        except Exception:
            self.assertTrue(yaml_mock.safe_load.called)

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.platform')
    @patch('jnpr.toby.init.init.Vars')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.Logger')
    @patch('jnpr.toby.init.init.os.environ')
    @patch('jnpr.toby.init.init.os.unlink')
    def test_initialize_other_cases(self, os_unlink_mock, os_env_mock, logger_mock, yaml_mock, open_mock, connect_mock,
                                    vars_mock, platform_mock, server_patch, log_patch):
        iobject = MagicMock(spec=init)
        iobject.is_robot = False
        iobject._log_dir = 'dir1'
        iobject._script_name = "test_init"
        iobject._validate_t_data.return_value = "test"
        iobject._validate_and_handle_framework_variables.return_value = "test"
        iobject._print_topology_info.return_value = "test"
        iobject.logger.log_dir.return_value = 'dir'
        platform_mock.system.return_value = "Windows"
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        os_env_mock['USER'] = "regress"

        #vars_mock.return_value.get_global_variable.side_effect = [ False, {}, True, 'test' ]
        #self.assertIsNone(init.Initialize(iobject))
        #iobject.log_console.assert_called_with("Toby Log: dir/test_init.log")

        #vars_mock.return_value.get_global_variable.side_effect = [ False, {}, False, 'test' ]
        #self.assertIsNone(init.Initialize(iobject))
        #iobject.log_console.assert_called_with("Toby Log: dir/test_init.log")

        yaml_mock.safe_load.return_value = {'t':{'resources':False}}
        vars_mock.return_value.get_global_variable.side_effect = [ True, 'config:test.yaml', False, 'test' ]
        self.assertIsNone(init.Initialize(iobject,force=True))
        iobject.log_console.assert_called_with("\nToby device initialization complete\n")

        yaml_mock.safe_load.return_value = {}
        vars_mock.return_value.get_global_variable.side_effect = [ False, {}, True, 'test' ]
        self.assertRaises(Exception, init.Initialize, iobject, force=True)
        
        vars_mock.return_value.get_global_variable.side_effect = [ False, {}, True ]
        yaml_mock.safe_load.side_effect = Exception('test') 
        self.assertRaises(Exception, init.Initialize, iobject, force=True)

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch('sys.stdout')
    @patch.dict('os.environ',{'USER':'regress'})
    def test_get_system(self, stdout_mock, open_mock, connect_mock, yaml_mock, server_cpu, log_patch):
        init_obj = init()
        self.assertRaises(Exception, init_obj.get_system)

        init_data = create_init_data()
        yaml_mock.safe_load.return_value = init_data
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        connect_mock.return_value = True
        init_obj = init()
        init_obj.Initialize(init_file='init_file', force=True)

        system = init_obj.get_system(resource='r0')
        self.assertEqual(system, init_data['t']['resources']['r0']['system'])
        init_obj.get_system(resource='r3');

    def test_get_resource_list(self):
        init_data = create_init_data()
        builtins.t = init_data['t']
        iobject = MagicMock(spec=init)
        self.assertEqual(list,type(init.get_resource_list(iobject,all_data=True)))
        self.assertEqual(list,type(init.get_resource_list(iobject)))
        t['resources']['r0']['system']['primary']={'tags':['string']}
        self.assertEqual(list,type(init.get_resource_list(iobject,tag=['string'],all_data=True)))
        self.assertEqual(list,type(init.get_resource_list(iobject,tag='string')))

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage') 
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch('sys.stdout')
    @patch.dict('os.environ',{'USER':'regress'})
    def test_get_resource(self, stdout_mock, open_mock, connect_mock, yaml_mock, server_cpu_patch, log_patch):
        init_obj = init()
        self.assertRaises(Exception, init_obj.get_resource)

        init_data = create_init_data()
        yaml_mock.safe_load.return_value = init_data
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        connect_mock.return_value = True
        init_obj = init()
        init_obj.Initialize(init_file='init_file', force=True)

        system = init_obj.get_resource(resource='r0')
        self.assertEqual(system, init_data['t']['resources']['r0'])
        init_obj.get_resource(resource='r3');

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch.dict('os.environ',{'USER':'regress'})
    def test_get_interface_list(self, open_mock, connect_mock, yaml_mock, server_cpu_patch, log_file_version_patch):
        init_data = create_init_data()
        yaml_mock.safe_load.return_value = init_data
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        connect_mock.return_value = True
        init_obj = init()
        init_obj.Initialize(init_file='init_file', force=True)

        system = init_obj.get_interface_list(resource='r0')
        self.assertEqual(system, list(init_data['t']['resources']['r0']['interfaces'].keys()))
        self.assertRaises(Exception, init_obj.get_interface_list, resource='r3')
        
        builtins.t = init_data['t']
        iobject = MagicMock(spec=init)
        self.assertEqual(list,type(init.get_interface_list(iobject)))
        self.assertEqual(list,type(init.get_interface_list(iobject,all_data=True)))
        
        self.assertEqual(list,type(init.get_interface_list(iobject,resource='r0',all_data=True)))
        t['resources']['r0']['interfaces']['fe0'] = {'tags':['string']}       
        self.assertEqual(list,type(init.get_interface_list(iobject,tag='string',resource='r0',all_data=True)))
        self.assertEqual(list,type(init.get_interface_list(iobject,tag='string',resource='r0',all_data=False)))
        self.assertEqual(list,type(init.get_interface_list(iobject,tag='string',all_data=True)))
        self.assertEqual(list,type(init.get_interface_list(iobject,tag='string',all_data=False)))

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch.dict('os.environ', {'USER':'regress'})
    def test_get_interface(self, open_mock, connect_mock, yaml_mock, server_patch, log_file_version_patch):
        init_obj = init()
        self.assertRaises(Exception, init_obj.get_interface)

        init_data = create_init_data()
        yaml_mock.safe_load.return_value = init_data
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        connect_mock.return_value = True
        init_obj = init()
        init_obj.Initialize(init_file='init_file', force=True)

        system = init_obj.get_interface(resource='r0', intf='fe0')
        self.assertEqual(system, init_data['t']['resources']['r0']['interfaces']['fe0'])
        self.assertRaises(Exception, init_obj.get_interface, resource='r3', intf='fe0')

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch.dict('os.environ',{'USER':'regress'})
    def test_get_t_link(self,  open_mock, connect_mock, yaml_mock, server_cpu_usage_patch, log_file):
        init_data = create_init_data()
        yaml_mock.safe_load.return_value = init_data
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        connect_mock.return_value = True
        init_obj = init()
        init_obj.Initialize(init_file='init_file', force=True)

        system = init_obj.get_t_link(link='link')
        self.assertEqual(system['r0'], ['fe0'])

        init_data['t']['resources']['r0']['interfaces']['fe1'] = {}
        init_data['t']['resources']['r0']['interfaces']['fe1']['link'] = 'link'
        system = init_obj.get_t_link(link='link')
        system['r0'].sort()
        self.assertEqual(system['r0'], ['fe0', 'fe1'])

        system = init_obj.get_t_link(link='test')
        self.assertEqual(system, {})

        init_data['t']['resources']['r0'].pop('interfaces')
        system = init_obj.get_t_link(link='link')
        self.assertEqual(system, {})

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch.dict('os.environ',{'USER':'regress'})
    def test_get_t(self, open_mock, connect_mock, yaml_mock, server_cpu_usage_patch, log_file):
        init_data = create_init_data()
        yaml_mock.safe_load.return_value = init_data
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        connect_mock.return_value = True
        init_obj = init()
        init_obj.Initialize(init_file='init_file', force=True)

        r0_data = {'name': 'abc', 'controllers': {'re0': {'mgt-ip': '1.1.1.1', 'hostname': 'abc'}}, 'model': 'mx',
         'osname': 'junos', 'make': 'Juniper'}
        system = init_obj.get_t('r0')
        self.assertEqual(system, r0_data)

        system = init_obj.get_t('r0', system_node='primary')
        self.assertEqual(system, r0_data)

        r0_data = {'r0': {'controllers': {'re0': {'mgt-ip': '1.1.1.1', 'hostname': 'abc'}}, 'model': 'mx', 'osname': 'junos', 'name': 'abc', 'make': 'Juniper'}}
        system = init_obj.get_t(('r0',))
        self.assertEqual(system, r0_data)

        r0_data = {'hostname': 'abc', 'mgt-ip': '1.1.1.1'}
        system = init_obj.get_t('r0', system_node='primary', controller='re0')
        self.assertEqual(system, r0_data)

        r0_data = {'name': 'fe0.0', 'link': 'link'}
        system = init_obj.get_t('r0', system_node='primary', controller='re0', interface='fe0')
        self.assertEqual(system, r0_data)

        r0_data = {'fe0': {'link': 'link', 'name': 'fe0.0'}}
        system = init_obj.get_t('r0', interface=('fe0',))
        self.assertEqual(system, r0_data)

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch.dict('os.environ',{'USER':'regress'})
    def test__get_system(self,open_mock,connect_mock, yaml_mock, server_cpu_usage_mock, log_file_version_patch):
        init_data = create_init_data()
        yaml_mock.safe_load.return_value = init_data
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        connect_mock.return_value = True
        init_obj = init()
        init_obj.Initialize(init_file='init_file', force=True)

        system = init_obj._get_system('r0', 'primary', 're0', 'hostname')
        self.assertEqual(system, 'abc')

        system = init_obj._get_system('r0', 'primary', None, None)
        self.assertEqual(system, init_data['t']['resources']['r0']['system']['primary'])

        self.assertRaises(Exception, init_obj._get_system, 'r0', 'secondary', None, None)
        self.assertRaises(Exception, init_obj._get_system, 'r0', 'primary', None, 'attribute')
        self.assertRaises(Exception, init_obj._get_system, 'r0', 'primary', 're1', None)
        self.assertRaises(Exception, init_obj._get_system, 'r0', 'primary', 're0', 'attribute')

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch.dict('os.environ',{'USER':'regress'})
    def test__get_interface(self, open_mock, connect_mock, yaml_mock, server_cpu_usage_patch, log_server_patch):
        init_data = create_init_data()
        yaml_mock.safe_load.return_value = init_data
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        connect_mock.return_value = True
        init_obj = init()
        init_obj.Initialize(init_file='init_file', force=True)

        system = init_obj._get_interface('r0', 'fe0', 'link')
        self.assertEqual(system, 'link')

        system = init_obj._get_interface('r0', 'fe0', None)
        self.assertEqual(system, init_data['t']['resources']['r0']['interfaces']['fe0'])

        self.assertRaises(Exception, init_obj._get_interface, 'r0', 'fe1', None)
        self.assertRaises(Exception, init_obj._get_interface, 'r0', 'fe0', 'attribute')

    def test_log_console(self):
        init_obj = init()
        self.assertRaises(Exception, init_obj.log_console)

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    @patch('jnpr.toby.init.init.yaml')
    @patch('jnpr.toby.init.init.init._connect_device')
    @patch('builtins.open')
    @patch.dict('os.environ',{'USER':'regress'})
    def test__print_topology_info(self,open_mock, connect_mock, yaml_mock, cpu_patch, log_file_version_patch):
        init_data = create_init_data()
        del init_data['t']['resources']['r0']['interfaces']['fe0']['link']
        yaml_mock.safe_load.return_value = init_data
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        connect_mock.return_value = True
        init_obj = init()
        init_obj.Initialize(init_file='init_file',force=True)
        init_obj._print_topology_info()

        init_data['t']['resources']['r0'].pop('interfaces')
        init_obj._print_topology_info()

    @patch('jnpr.toby.init.init.Logger')
    @patch('jnpr.toby.init.init.minidom')
    def test_log(self, minidom_patch, logger_patch):
        iobject = MagicMock(spec=init)
        self.assertRaises(Exception, init.log, iobject)

        iobject.is_robot = True
        iobject.background_logger = MagicMock()
        iobject.console_log_flag = False
        iobject.robot_log_level = None
        self.assertIsNone(init.log(iobject, level="INFO"))
        self.assertTrue(iobject.logger._log.called)

        xmldata = etree.XML('<software-information></software-information>')

        iobject._script_name = "name"
        iobject.logger = False
        iobject.console_log_flag = False
        self.assertIsNone(init.log(iobject, level="INFO", message=xmldata))
        logger_patch.assert_called_once_with('name', console= False)

        iobject.console_log_flag ="enable"
        iobject.logger = False
        iobject.console_log_flag ="enable"
        iobject.is_robot = False
        iobject.background_logger = None
        iobject.console_log_flag = True
        self.assertIsNone(init.log(iobject, level="INFO", message=xmldata))
        logger_patch.assert_called_with('name', console= True)
        with patch('jnpr.toby.utils.Vars.Vars.get_global_variable',side_effect=["enable","disable"]) as Vars_patch:
            iobject = MagicMock(spec=init)
            iobject.is_robot = False
            iobject.background_logger = None
            iobject.logger = MagicMock()
            iobject.console_log_flag = True
            init.log(iobject,"DEBUG","Message")

    def test_import(self):
        import jnpr.toby.init.init as init
        sys.modules['builtin'] = sys.modules['builtins']
        with patch.dict('sys.modules', {'builtins':None}):
            importlib.reload(init)


    def test_toby_suite_setup(self):
        iobject = MagicMock(spec=init)
        builtins.t = False
        self.assertIsNone(init.toby_suite_setup(iobject, force=True))
        self.assertTrue(iobject.detect_core_on_junos_device.called)
        self.assertIsNone(init.toby_suite_setup(iobject, force=False)) 

    @patch('jnpr.toby.init.init.builtins.t')
    def test_toby_suite_setup_raise_exception(self, builtins_patch):
        builtins_patch = MagicMock(return_value=Exception("error"))
        iobject = MagicMock(spec=init)
        self.assertIsNone(init.toby_suite_setup(iobject))

    def test_toby_suite_setup_with_init_already_called(self):
        iobject = MagicMock(spec=init)
        builtins.t = True
        self.assertIsNone(init.toby_suite_setup(iobject))

    def test_toby_suite_teardown(self):
        iobject = MagicMock(spec=init)
        self.assertIsNone(init.toby_suite_teardown(iobject))
        self.assertTrue(iobject.detect_core_on_junos_device.called)

    def test_toby_test_setup(self):
        builtins.t = MagicMock()
        iobject = MagicMock(spec=init)
        iobject.get_junos_resources = MagicMock(return_value=['r0','r1'])
        iobject.get_system =  MagicMock(return_value={'primary':{'fv-connect-controllers':'none'}})
        self.assertIsNone(init.toby_test_setup(iobject))
        iobject.get_system = MagicMock(return_value={'primary':{}})
        handle = MagicMock()
        handle.cli = MagicMock(return_value='True')
        iobject.get_handle =  MagicMock(return_value=handle)
        self.assertIsNone(init.toby_test_setup(iobject))
        iobject.get_system =  MagicMock(return_value={'primary':{}})
        handle = MagicMock()
        handle.cli.side_effect =  Exception('some exception')
        handle.reconnect= MagicMock(return_value=True)
        iobject.get_handle =  MagicMock(return_value=handle)
        self.assertIsNone(init.toby_test_setup(iobject))

    def test_toby_test_teardown(self):
        iobject = MagicMock(spec=init)
        self.assertIsNone(init.toby_test_teardown(iobject))
        self.assertTrue(iobject.detect_core_on_junos_device.called)

    def test_toby_initialize(self):
        iobject = MagicMock(spec=init)
        builtins.t = False 
        self.assertIsNone(init.toby_initialize(iobject))
        iobject.Initialize.assert_called_with(init_file=None)

        self.assertIsNone(init.toby_initialize(iobject, init_file="test"))
        iobject.Initialize.assert_called_with(init_file="test")

    @patch('jnpr.toby.init.init.yaml')
    def test__validate_and_handle_framework_variables(self, yaml_mock):
        iobject = MagicMock(spec=init)
        iobject._validate_allowed_values_for_fvar.return_value = "test1"
        iobject._update_t_dict_with_framework_variable.return_value = "test2"
        init_data = create_init_data()
        iobject.t_dict = init_data['t']
        iobject.t_dict['framework_variables'] = {'fv-test':'test'}
        iobject.t_dict['console_log'] = 'enable' 
        iobject.t_dict['resources']['r0']['system']['primary']['fv-test'] = "test"
        self.assertRaises(Exception, init._validate_and_handle_framework_variables, iobject)

        yaml_mock.safe_load.return_value = {'fv-test':{'test':'test','destination':'interfaces'}}
        self.assertIsNone(init._validate_and_handle_framework_variables(iobject))
        self.assertTrue(iobject._update_t_dict_with_framework_variable.called)

        yaml_mock.safe_load.return_value = {'fv-test':{'test':'test','destination':'test'}}
        iobject.t_dict['resources']['r0']['interfaces']['xe.*'] = {'fv-test':'test'} 
        self.assertIsNone(init._validate_and_handle_framework_variables(iobject))

    def test__update_t_dict_with_framework_variable(self):
        iobject = MagicMock(spec=init)

        ## Without arguments
        self.assertRaises(TypeError, init._update_t_dict_with_framework_variable, iobject)

        ## With all positional arguments
        init_data = create_init_data()
        iobject.t_dict = init_data['t']
        fvar_structure = defaultdict(lambda: defaultdict(dict))

        # String
        fvar_structure['type'] = "string"
        fvar_structure['content']['key'] = "hostname"
        fvar_structure['destination'] = "test"
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'xyz', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], "abc")

        fvar_structure['destination'] = "controllers"
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'xyz', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], "xyz")

        fvar_structure['content']['key'] = "name"
        fvar_structure['destination'] = "system-nodes"
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'xyz', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['name'], "xyz")

        # Boolean
        fvar_structure['type'] = "boolean"
        fvar_structure['content']['value'] = "test1"
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'all', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['name'], "test1")

        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'primary:all', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['name'], "test1")

        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'test:all', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['name'], "test1")

        fvar_structure['destination'] = "controllers"
        fvar_structure['content']['key'] = "hostname"
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'all', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], "test1")

        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 're0:all', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], "test1")

        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'test:all', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], "test1")

        fvar_structure['destination'] = "test"
        iobject.t_dict['resources']['r0']['system']['primary']['name'] = "abc"
        iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = "abc"
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'all', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['name'], "abc")
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], "abc")

        # List
        fvar_structure['type'] = 'list'
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'all', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['name'], "abc")
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], "abc")

        fvar_structure['destination'] = "system-nodes"
        fvar_structure['content']['key'] = "name"
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'xyz', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['name'], ["xyz"])

        fvar_structure['destination'] = "controllers"
        fvar_structure['content']['key'] = "hostname"
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'all', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], ['all'])

        # Dictionary
        fvar_structure['type'] = 'dictionary'
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'key=test1', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], 'test1')

        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'key1=test1', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], 'test1')

        fvar_structure['destination'] = "test"
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'key=test1', fvar_structure))
        self.assertEqual(iobject.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'], 'test1')

        # Unknown
        fvar_structure['type'] = 'unknown'
        self.assertIsNone(init._update_t_dict_with_framework_variable(iobject, 'r0', 'test', 'test1', fvar_structure))

    def test__validate_allowed_values_for_fvar(self):
        iobject = MagicMock(spec=init)

        ## Without arguments
        self.assertRaises(TypeError, init._validate_allowed_values_for_fvar, iobject)

        ## With all positional arguments
        fvar_structure = {}
        self.assertIsNone(init._validate_allowed_values_for_fvar(iobject, 'r0', 'test', fvar_structure))

        fvar_structure['allowed-values'] = {}
        self.assertRaises(Exception, init._validate_allowed_values_for_fvar, iobject, 'r0', 'test', fvar_structure)

        fvar_structure['allowed-values'] = ['test']
        self.assertIsNone(init._validate_allowed_values_for_fvar(iobject, 'r0', 'test', fvar_structure))

    def test__validate_t_data(self):
        iobject = MagicMock(spec=init)

        iobject.t_dict = {}
        self.assertRaises(Exception, init._validate_t_data, iobject)

        iobject.t_dict['resources'] = "test"
        self.assertRaises(Exception, init._validate_t_data, iobject)

        iobject.t_dict['resources'] = {'r0':'test'}
        self.assertRaises(Exception, init._validate_t_data, iobject)

    @patch('jnpr.toby.init.init.Device')
    def test__connect_device(self, device_patch):
        iobject = MagicMock(spec=init)

        init_data = create_init_data()
        iobject.t_dict = init_data['t']
        self.assertIsNone(init._connect_device(iobject, 'r0'))

        init_data = create_init_data()
        iobject.t_dict = init_data['t']
        iobject.t_dict['resources']['r0']['system']['primary'].pop('osname')
        self.assertRaises(Exception, init._connect_device, iobject, 'r0')
        
        init_data = create_init_data()
        iobject.t_dict = init_data['t']
        iobject.t_dict['resources']['r0']['system']['primary'].pop('osname')
        iobject.t_dict['resources']['r0']['system']['primary']['model'] = "nux"
        self.assertIsNone(init._connect_device(iobject, 'r0'))

        init_data = create_init_data()
        iobject.t_dict = init_data['t']
        device_patch.return_value.current_node.current_controller.channels = {'pyez': MagicMock()}
        device_patch.return_value.current_node.current_controller.channels['pyez'].\
                                  facts_refresh.side_effect = Exception
        self.assertIsNone(init._connect_device(iobject, 'r0'))
        iobject.log.assert_any_call(level="INFO", message='Could not refresh facts for pyez channel')

        init_data = create_init_data()
        iobject.t_dict = init_data['t']
        iobject.t_dict['resources']['r0']['system']['primary']['osname'] = "spirent"
        self.assertIsNone(init._connect_device(iobject, 'r0'))
        self.assertTrue(device_patch.return_value.connect.called)
        self.assertTrue(device_patch.return_value.add_intf_to_port_map.called)

    def test_get_handle(self):
        iobject = MagicMock(spec=init)

        # Exception
        self.assertRaises(Exception, init.get_handle, iobject, 'r0')

        init_data = create_init_data()
        init_data['t']['resources']['r0']['system']['dh'] = "test"
        builtins.t = init_data['t']
        self.assertEqual(init.get_handle(iobject, 'r0'), "test")

        init_data['t']['resources']['r0']['system']['dh'] = MagicMock()
        init_data['t']['resources']['r0']['system']['dh'].nodes = {'backup': 'test1'}
        self.assertEqual(init.get_handle(iobject, 'r0', system_node="backup"), "test1")

        init_data['t']['resources']['r0']['system']['dh'].current_node = "test2"
        self.assertEqual(init.get_handle(iobject, 'r0', system_node="current"), "test2")

        init_data['t']['resources']['r0']['system']['dh'] = MagicMock()
        init_data['t']['resources']['r0']['system']['dh'].current_node.controllers = {'backup': 'test3'}
        self.assertEqual(init.get_handle(iobject, 'r0', controller="backup"), "test3")

        init_data['t']['resources']['r0']['system']['dh'].current_node.current_controller = "test4"
        self.assertEqual(init.get_handle(iobject, 'r0', controller="current"), "test4")

        self.assertEqual(init.get_handle(iobject, 'r0', system_node="current", controller="current"), "test4")
        self.assertEqual(init.get_handle(iobject, 'r0', system_node="current", controller="backup"), "test3")

        init_data['t']['resources']['r0']['system']['dh'].nodes['backup'].current_controller = "test5"
        self.assertEqual(init.get_handle(iobject, 'r0', system_node="backup", controller="current"), "test5")

        init_data['t']['resources']['r0']['system']['dh'].nodes['backup'].controllers =  {'backup': 'test6'}
        self.assertEqual(init.get_handle(iobject, 'r0', system_node="backup", controller="backup"), "test6")

    def test___contains__(self):
        iobject = MagicMock(spec=init)

        iobject.__dict__ = {'key': 'test'}
        self.assertEqual(init.__contains__(iobject, "key"), True)

    def test___repr__(self):
        iobject = MagicMock(spec=init)

        iobject.__dict__ = {'key': 'test'}
        self.assertEqual(init.__repr__(iobject), "{'key': 'test'}")

    def test_get_junos_resources(self):
        iobject = MagicMock(spec=init)

        self.assertEqual(init.get_junos_resources(iobject), [])

        init_data = create_init_data()
        builtins.t = init_data['t']
        iobject.get_resource_list.return_value = ['r0']
        self.assertEqual(init.get_junos_resources(iobject), ['r0'])

        init_data['t']['resources']['r0']['system']['primary']['osname'] = 'unix'
        self.assertEqual(init.get_junos_resources(iobject), [])

    def test_core_info(self):
        builtins.t = MagicMock()
        t._stage = 'sample'
        t.core = {'sample':'test'}
        iobject = MagicMock(spec=init)
        init.core_info(iobject)
        t._stage = 'string'
        init.core_info(iobject) 

    @patch('jnpr.toby.init.init.run_multiple')
    def test_detect_core_on_junos_device(self, run_patch):
        iobject = MagicMock(spec=init)

        init_data = create_init_data()
        builtins.t = init_data['t']
        iobject.get_junos_resources.return_value = ['r0']
        self.assertIsNone(init.detect_core_on_junos_device(iobject))
        self.assertEqual(run_patch.call_count, 0)

        init_data['t']['resources']['r0']['system']['primary'] = {'core-check':'enable'} 
        iobject.get_handle.return_value.detect_core = True
        list_of_dicts = [{'fname': True, 'kwargs': {'resource': 'r0'}}]
        self.assertTrue(init.detect_core_on_junos_device(iobject, resource="r0"))
        run_patch.assert_called_once_with(list_of_dicts)

        list_of_dicts = [{'fname': True, 'kwargs': {'core_path': 'path', 'resource': 'r0'}}]
        self.assertTrue(init.detect_core_on_junos_device(iobject, core_path="path", resource="r0"))
        run_patch.assert_called_with(list_of_dicts)

        iobject.get_junos_resources.return_value = []
        self.assertRaises(Exception, init.detect_core_on_junos_device, iobject, resource="r0")
    
    @patch('jnpr.toby.init.init.run_multiple') 
    def test_check_interface_status(self,run_patch):
        init_data = create_init_data()
        builtins.t = init_data['t']
        iobject = MagicMock(spec=init)
        init_data['t']['resources']['r0']['system']['primary']['interface-status-check'] = "enable"
        iobject.get_junos_resources.return_value = ['r0']
        init.check_interface_status(iobject)
        iobject.get_interfaces_name.return_value = None
        self.assertRaises(Exception,init.check_interface_status,iobject)
        iobject.get_interfaces_name.return_value = "test"
        run_patch.return_value = [False]
        self.assertRaises(Exception,init.check_interface_status,iobject)

    def test__load_baseline_config(self):
        init_data = create_init_data()
        builtins.t = init_data['t']
        iobject = MagicMock(spec=init)
        init_data['t']['resources']['r0']['system']['primary']['load-baseline-config-from'] = "default"
        iobject.get_junos_resources.return_value = ['r0']
        iobject.get_handle.load_baseline_config = MagicMock()
        self.assertTrue(init._load_baseline_config(iobject))
        init_data['t']['resources']['r0']['system']['primary']['load-baseline-config-from'] = "Userdefined"
        self.assertTrue(init._load_baseline_config(iobject))

    def test_load_saved_config(self):
        iobject = MagicMock(spec=init)
        iobject._script_name = "name"
        iobject.get_junos_resources.return_value = ['r0']
        iobject.get_handle.load_saved_config = MagicMock()
        self.assertTrue(init.load_saved_config(iobject))
        self.assertTrue(init.load_saved_config(iobject,config_id=123,resource='r0'))
        self.assertRaises(Exception,init.load_saved_config,iobject,config_id=123,resource='r1')

    def test_save_current_config(self):
        iobject = MagicMock(spec=init)
        iobject._script_name = "name"
        iobject.get_junos_resources.return_value = ['r0']
        iobject.get_handle.save_current_config = MagicMock()
        self.assertTrue(init.save_current_config(iobject))
        self.assertTrue(init.save_current_config(iobject,config_id=123,resource='r0'))
        self.assertRaises(Exception,init.save_current_config,iobject,config_id=123,resource='r1')
 
    def test_keys(self):
        iobject = MagicMock(spec=init)
        init.keys(iobject)

    @patch('jnpr.toby.init.init.log_file_version')
    @patch('jnpr.toby.init.init.server_cpu_usage')
    def test_get_interfaces_name(self, server_cpu_patch, log_patch):
        iobject = MagicMock(spec=init)
        init_data = create_init_data()
        builtins.t = init_data['t']
        init_data['t']['resources']['r0'] = {'interfaces':{'xe': {'pic': 1, 'tags': 'abc'}}}
        self.assertIsNotNone(init.get_interfaces_name(iobject,resource='r0',tags=None))
        self.assertIsNone(init.get_interfaces_name(iobject,resource='r0',tags="abc"))
        self.assertIsNone(init.get_interfaces_name(iobject,resource='r0',tags=['test1','test2']))  

 
     
    @patch('jnpr.toby.init.init.pdb')
    def test_pause(self,pdb_patch):
        iobject = MagicMock(spec=init)
        init.pause(iobject)
    @patch('jnpr.toby.utils.Vars.Vars.get_global_variable')
    def test_get_session_id(self,vars_patch):
        iobject = MagicMock(spec=init)
        vars_patch.return_value = True
        init.get_session_id(iobject)
        vars_patch.return_value= False
        self.assertRaises(Exception,init.get_session_id,iobject)

    def test_get_package_name(self):
        iobject = MagicMock(spec=init)
        self.assertIsNotNone(init.get_package_name(iobject,release=15.1,model='mx240'))
        self.assertIsNotNone(init.get_package_name(iobject,release=15.1,model='mx240', arch=64))
        self.assertIsNotNone(init.get_package_name(iobject,release=15.1,model='mx240'))
        self.assertIsNotNone(init.get_package_name(iobject,release=15.1,model='mx240'))
        self.assertIsNotNone(init.get_package_name(iobject,release=15.1,model='mx240',package_type='vmhost'))
        self.assertIsNotNone(init.get_package_name(iobject,release=15.1,model='mx240',package_type='occam'))
        self.assertRaises(Exception,init.get_package_name,iobject,release=15.1,model='mx240',package_type='unknown')


    @patch('jnpr.toby.init.init.run_multiple')
    def test_install_package(self,run_patch):
        builtins.t = create_init_data()['t']
        iobject = MagicMock(spec=init)
        iobject.get_resource_list.return_value= ['r0']
        iobject.get_package_name.return_value = 'package'
        iobject.get_handle.software_install = MagicMock()

        iobject._get_package_details.return_value = ('vmhost',64,'path','issu','ALL','remote_path','nssu',None, None)
        init.install_package(iobject,release=15.1)
        iobject._get_package_details.return_value = ('vmhost',64,'path','issu',None,'remote_path','nssu',None, None)
        init.install_package(iobject,release=15.1)
        iobject._get_package_details.return_value = ('vmhost',64,'path','issu','in_tag','remote_path','nssu',None, None)
        init.install_package(iobject,release=15.1)
        t['resources']['r0']['system']['primary']['osname'] = 'IOS'
        init.install_package(iobject,release=15.1)
    
    def test_get_package_details(self):
        init_data = {'t':{'framework_variables':{'software-install':{'package':{'from':[{'release':15.1}],'to':{'release':15.1}}}}}} 
        builtins.t = init_data['t']
        iobject = MagicMock(spec=init)
        init._get_package_details(iobject,release=15.1,remote_path='remote')
        init._get_package_details(iobject,release=14.1,remote_path='remote')
        init_data = {'t':{'framework_variables':{'software-install':{'package':{}}}}}  
        builtins.t = init_data['t']
        init._get_package_details(iobject,release=15.1,remote_path='remote')
     
    def test__merge_fv_uv_yaml_content_in_t(self):
        iobject = MagicMock(spec=init)
        input_data = {'user_variables':{'uva':'val'}}
        iobject.t_dict = {}
        init._merge_fv_uv_yaml_content_in_t(iobject,input_data)
        iobject.t_dict = {'user_variables':{}}
        init._merge_fv_uv_yaml_content_in_t(iobject,input_data)
        
        input_data = {'framework_variables':{'uva':'val'}}
        iobject.t_dict = {}
        init._merge_fv_uv_yaml_content_in_t(iobject,input_data)
        iobject.t_dict = {'framework_variables':{}}
        init._merge_fv_uv_yaml_content_in_t(iobject,input_data)

        iobject.t_dict  = input_data = create_init_data()['t'] 
        input_data['resources']['r0']['system']['primary'] = {'fv-a':'val'}
        init._merge_fv_uv_yaml_content_in_t(iobject,input_data)
        input_data['resources']['r0']['system']['primary'] = {'var':'val'}
        init._merge_fv_uv_yaml_content_in_t(iobject,input_data)
 
        input_data['resources']['r0']['system'] = {}
        init._merge_fv_uv_yaml_content_in_t(iobject,input_data)
        
        input_data['resources']['r0']['interfaces']['fe0'] = {'fv-a':'val'}
        init._merge_fv_uv_yaml_content_in_t(iobject,input_data)
        input_data['resources']['r0']['interfaces']['fe0'] = {'var':'val'}
        init._merge_fv_uv_yaml_content_in_t(iobject,input_data)


    @patch('robot.libraries.BuiltIn.BuiltIn')
    @patch('robot.libraries.BuiltIn.BuiltIn.get_variable_value')
    def test_code_coverage_close(self,builtin_variable_patch,builtin_patch):
        builtin_variable_patch.return_value = {'${SUITE_NAME}': 'Sample_test', '${SUITE_STATUS}': 'Sample_test'}
        sys.modules['jnpr.codecoverage.codecoverage'] = MagicMock()	
        CodeCoverage = MagicMock()
        CodeCoverage.register_coverage_data = MagicMock(return_value=True) 	
        iobject = MagicMock(spec=init)	
        builtins.t = MagicMock()	
        t.code_coverage = MagicMock(return_value='True')	
        self.assertIsNone(init._code_coverage_close(iobject))	
        t.code_coverage = MagicMock(return_value=False)	
        self.assertIsNone(init._code_coverage_close(iobject))	
        CodeCoverage.register_coverage_data.return_value = False	
        self.assertIsNone(init._code_coverage_close(iobject))        	
        CodeCoverage.code_coverage_close = MagicMock(return_value=True)	
        t['framework_variables']['code_coverage']['data_registration'] = False	
        self.assertIsNone(init._code_coverage_close(iobject))	
        CodeCoverage.code_coverage_close = MagicMock(return_value=False)	
        self.assertIsNone(init._code_coverage_close(iobject))  


    @patch('robot.libraries.BuiltIn.BuiltIn')
    @patch('robot.libraries.BuiltIn.BuiltIn.get_variable_value')
    def test_code_coverage_dump(self,builtin_variable_patch,builtin_patch):
        builtin_variable_patch.return_value = {'${TEST_NAME}': 'Sample_test', '${TEST_STATUS}': 'Sample_test'}	
        sys.modules['jnpr.codecoverage.codecoverage'] = MagicMock()
        CodeCoverage = MagicMock()
        builtins.t = MagicMock()	
        iobject = MagicMock(spec=init)	
        t.code_coverage = MagicMock(return_value='True')	
        self.assertIsNone(init._code_coverage_dump(iobject))	
        t.code_coverage = MagicMock(return_value='True')	
        t['framework_variables']['code_coverage']['collect_gcov_data_for'] = "abc"	
        self.assertIsNone(init._code_coverage_dump(iobject))


    def test__get_associated_systems(self):	
        init_data = create_init_data() 	
        iobject = MagicMock(spec=init)	
        iobject.t_dict = init_data['t']	
        self.assertIsNotNone(init._get_associated_systems(iobject,resource='r0', t_dict='t_dict',key='True'))


    def test_process_proxy_resource_aliases(self):	
        codecoverage = MagicMock()
        codecoverage.codecoverage = MagicMock()
        codecoverage.codecoverage.CodeCoverage = MagicMock()
        init_data = create_init_data1()	
        iobject = MagicMock(spec=init)	
        iobject.t_dict = init_data['t']	
        self.assertIsNone(init._process_proxy_resource_aliases(iobject))


    @patch('robot.libraries.BuiltIn.BuiltIn')
    @patch('robot.libraries.BuiltIn.BuiltIn.get_variable_value')
    def test_code_coverage_init(self,builtin_variable_patch,builtin_patch):
          builtin_variable_patch.return_value = {'${SUITE_SOURCE}': 'Sample_test'}
          Builtin = MagicMock()
          Builtin.get_variables = MagicMock(return_value = {'${SUITE_SOURCE}': 'test.robot'})
          builtins.t = MagicMock()       
          builtins.t.code_coverage = MagicMock()    

          sys.modules['jnpr.codecoverage.codecoverage'] = MagicMock()
          CodeCoverage = MagicMock()
          CodeCoverage.get_gcov_data_path = MagicMock(return_type=True) 
 
          class MyMock(object):
            def __init__(self,d):
                 self.d = d
            def __getitem__(self, x):
              return self.d[x]
            def __contains__(self, x):
              return x in self.d
            def log(self, level=None, message=None):
              pass

          mobject = MyMock({'framework_variables': {'code_coverage': {'registration': {'activity_type': '10'}, 'data_path':None}}}) 

          self.assertFalse(init._code_coverage_init(mobject))  	

          CodeCoverage.cc_attributes_valiation = MagicMock(return_type=True)          

          mobject = MyMock({'framework_variables': {'code_coverage': {'registration': {'activity_type': '10'}, 'data_path': 'data_path' ,'filters': {'filters': 'filters'}}}})   

          self.assertFalse(init._code_coverage_init(mobject))  	

                                      
          mobject = MyMock({'framework_variables': {'code_coverage': {'registration': {'activity_type': '10'}, 'data_path': None ,'filters': {'filters': 'filters'}}}})

          self.assertFalse(init._code_coverage_init(mobject))


    def test_check_and_reconnect(self):
        handle = MagicMock()
        handle.reconnect= MagicMock(return_value=True)
        iobject = MagicMock(spec=init)
        iobject.get_junos_resources = MagicMock(return_value=['r0','r1'])
        iobject.get_system = MagicMock(return_value={'primary':{'core-check':'enable','fv-connect-controllers':'none'}})
        iobject.get_handle = MagicMock(return_value=handle)
        self.assertIsNone(init._check_and_reconnect(iobject))       
        iobject.get_system = MagicMock(return_value={'primary':{'core-check':'enable'}})  
        self.assertIsNone(init._check_and_reconnect(iobject))     
        handle.reconnect= MagicMock(return_value=False)
        self.assertRaises(Exception, init._check_and_reconnect, iobject)

    def test__create_global_tv_dictionary(self):
        iobject = MagicMock(spec=init)
        iobject.t_dict = create_init_data1()['t']
        iobject.t_dict.update({'user_variables':{'uva':'val'}})
        iobject.tv_dict = {}
        init._create_global_tv_dictionary(iobject)
        iobject.tv_dict = {}
        init._create_global_tv_dictionary(iobject)
        
        iobject.t_dict = create_init_data1()['t']
        iobject.t_dict['resources']['r0']['interfaces']['fe0']['name'] = 'fe-1/1/1.a.b'
        iobject.t_dict.update({'user_variables':{'uva':'val'}})
        init._create_global_tv_dictionary(iobject)

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
    init_data['t']['resources']['r0']['interfaces'] = dict()
    init_data['t']['resources']['r0']['interfaces']['fe0'] = dict()
    init_data['t']['resources']['r0']['interfaces']['fe0']['name'] = 'fe0.0'
    init_data['t']['resources']['r0']['interfaces']['fe0']['link'] = 'link'
    init_data['t']['resources']['r0']['system'] = dict()
    init_data['t']['resources']['r0']['system']['primary'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    init_data['t']['resources']['r0']['system']['primary']['name'] = 'abc'
    init_data['t']['resources']['r0']['system']['primary']['model'] = 'mx'
    init_data['t']['resources']['r0']['system']['primary']['make'] = 'Juniper'
    init_data['t']['resources']['r0']['system']['primary']['osname'] = 'junos'
    init_data['t']['user_variables'] = dict()
    init_data['t']['user_variables']['uva'] = 'val'
    return init_data

def create_init_data1():
    """
    Function to create init_data
    :return:
        Returns init_data
    """
    init_data = dict()
    init_data['t'] = dict()
    init_data['t']['resources'] = dict()
    init_data['t']['resources']['r0'] = dict()
    init_data['t']['resources']['r0']['interfaces'] = dict()
    init_data['t']['resources']['r0']['interfaces']['fe0'] = dict()
    init_data['t']['resources']['r0']['interfaces']['fe0']['name'] = 'fe0.0'
    init_data['t']['resources']['r0']['interfaces']['fe0']['link'] = 'link'
    init_data['t']['resources']['r0']['system'] = dict()
    init_data['t']['resources']['r0']['system']['primary'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    init_data['t']['resources']['r0']['system']['primary']['name'] = 'abc'
    init_data['t']['resources']['r0']['system']['primary']['model'] = 'mx'
    init_data['t']['resources']['r0']['system']['primary']['make'] = 'Juniper'
    init_data['t']['resources']['r0']['system']['primary']['osname'] = 'junos'

    init_data['t']['resources']['r0']['system'] = dict()
    init_data['t']['resources']['r0']['system']['secondary'] = dict()
    init_data['t']['resources']['r0']['system']['secondary']['controllers'] = dict()
    init_data['t']['resources']['r0']['system']['secondary']['controllers']['re0'] = dict()
    init_data['t']['resources']['r0']['system']['secondary']['controllers']['re0']['hostname'] = 'abc'
    init_data['t']['resources']['r0']['system']['secondary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    init_data['t']['resources']['r0']['system']['secondary']['name'] = 'abc'
    init_data['t']['resources']['r0']['system']['secondary']['model'] = 'mx'
    init_data['t']['resources']['r0']['system']['secondary']['make'] = 'Juniper'
    init_data['t']['resources']['r0']['system']['secondary']['osname'] = 'junos'
    return init_data


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestInit)
    unittest.TextTestRunner(verbosity=2).run(SUITE)

