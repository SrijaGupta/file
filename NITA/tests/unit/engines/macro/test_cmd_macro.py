# pylint: disable=undefined-variable,invalid-name,bad-whitespace,missing-docstring

import builtins
from datetime import datetime
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import re
from jnpr.toby.utils.response import Response
from jnpr.toby.init.init import init
from jnpr.toby.hldcl.device import Device
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.engines.macro.cmd_macro import cmd_macro as TobyMacro

class TestCmdMacro(unittest.TestCase):

    def setUp(self):
        builtins.t = MagicMock(spec=init)
        t.is_robot = True
        t._script_name = "test_init"
        t.background_logger = MagicMock()
        t.log = MagicMock()
        t.log_console = MagicMock()
        create_t_data()
        t.resources = t.t_dict['resources']
        t.__getitem__ = MagicMock(return_value=t.t_dict['resources'])

    def test__init(self):
        new_cmd_macro = TobyMacro()
        self.assertIsInstance(new_cmd_macro, TobyMacro)

    @patch('jnpr.toby.engines.macro.cmd_macro.BuiltIn')
    def test_run_macros_on_failure(self, BuiltIn_patch):
        cmd_macro_obj = MagicMock(spec=TobyMacro)
        BuiltIn_patch.set_suite_variable.return_value = True
        TobyMacro.run_macros_on_failure(self, macro_lib='Test', macro='Test', Abc='Abc')

    @patch('jnpr.toby.engines.macro.cmd_macro.yaml.safe_load')
    @patch('builtins.open')
    @patch('jnpr.toby.engines.macro.cmd_macro.os.path.dirname')
    @patch('builtins.hasattr')
    def test_load_macros(self, hasattr_patch, os_dirname_patch, open_patch, yaml_safe_load_patch):
        cmd_macro_obj = MagicMock(spec=TobyMacro)
        hasattr_patch.return_value = False
        with self.assertRaises(TobyException):
            TobyMacro.load_macros(cmd_macro_obj, macro_lib='Test')

        hasattr_patch.return_value = True
        macro_lib = 'Test1'
        os_dirname_patch.return_value = 'Test'
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.close.return_value = True
        open_patch.return_value = open_obj
        yaml_safe_load_patch.return_value = {'Test':'Test'}
        with self.assertRaises(TobyException):
            TobyMacro.load_macros(cmd_macro_obj, macro_lib=macro_lib)

        cmd_macro_obj.all_macro_libs = {'vars' : {'Test': 'Test'}}
        yaml_safe_load_patch.return_value = {'filetype' : 'macro_lib', 'import': ['/Test', 'Test']}
        with self.assertRaises(TobyException):
            TobyMacro.load_macros(cmd_macro_obj, macro_lib=macro_lib)

        yaml_safe_load_patch.return_value = {'filetype' : 'constraint', 'constraint': 'Test'}
        cmd_macro_obj.addon_constraints = {}
        cmd_macro_obj.local_vars = {}
        self.assertIsNone(TobyMacro.load_macros(cmd_macro_obj, macro_lib=macro_lib, variables={'Test':'Test'}))

    @patch('builtins.open')
    @patch('jnpr.toby.engines.macro.cmd_macro.logging.getLogger')
    @patch('jnpr.toby.engines.macro.cmd_macro.yaml')
    @patch('jnpr.toby.engines.macro.cmd_macro.BuiltIn')
    @patch('jnpr.toby.engines.macro.cmd_macro.literal_eval')
    @patch('jnpr.toby.engines.macro.cmd_macro.os.makedirs')
    @patch('jnpr.toby.engines.macro.cmd_macro.get_log_dir')
    @patch('jnpr.toby.engines.macro.cmd_macro.Vars')
    def test_run_macros(self, Vars_patch, get_log_dir_patch, os_makedirs_patch, literal_eval_patch, BuiltIn_patch,
                              yaml_patch, getLogger_patch, open_patch):
        cmd_macro_obj = MagicMock(spec=TobyMacro)
        self.assertIsNone(TobyMacro.run_macros(cmd_macro_obj, macros='mac=ro', resources='Test'))

        Vars_patch.get_global_variable.return_value = 'Some Test'
        cmd_macro_obj.loggers = {'default' : 'Test'}
        cmd_macro_obj.log_files = []
        cmd_macro_obj.all_macro_libs = False
        self.assertIsNone(TobyMacro.run_macros(cmd_macro_obj, macros='Test', resources='r0'))

        cmd_macro_obj.all_macro_libs = True
        literal_eval_patch.return_value = {'r0':'Test'}
        Test = MagicMock()
        Test.reconnect.return_value = True
        t.get_handle.side_effect = [Exception('Test'), Test]
        cmd_macro_obj.handles = {'r1' : 'Test', 'r0' : Test}
        cmd_macro_obj.__setup_logger = 'Test'
        cmd_macro_obj.user_targets = {}
        b_obj = MagicMock()
        b_obj.get_variables.side_effect = Exception('Test')
        BuiltIn_patch.return_value = b_obj
        cmd_macro_obj.__log = True
        yaml_patch.dump.return_value = True
        yaml_patch.safe_load.return_value = {'Test2': {'ABC' : 'xyz'}, 'Test3' : ['Test3List'], 'Test4' : 'Test4Str'} #<---------
        cmd_macro_obj.__process_vars = True
        cmd_macro_obj.__process_file_vars = True
        cmd_macro_obj.target_macros = []
        cmd_macro_obj.__run_single_macro = True
        cmd_macro_obj.core_collect = True
        cmd_macro_obj.__core_collect = True
        log_obj = MagicMock()
        handle_obj = MagicMock()
        getLogger_patch.return_value = log_obj
        log_obj.handlers = {handle_obj}
        log_obj.removeHandler.return_vale = True
        handle_obj.flush.return_value = True
        handle_obj.close.return_value = True
        open_obj = MagicMock()
        open_obj.read().replace.return_value = True
        open_obj.write.return_value = True
        open_obj.close.return_value = True        
        open_patch.return_value = open_obj
        self.assertIsNone(TobyMacro.run_macros(cmd_macro_obj, macros='Test1:Test2:Test3:Test4', resources=['r1', 'r0'], message="Msg", targets={'r0':'Test'}))
        self.assertIsNone(TobyMacro.run_macros(cmd_macro_obj, macros='Test1:Test2:Test3:Test4', resources='r1:r0', message="Msg", targets={'r0':'Test'}))
        self.assertIsNone(TobyMacro.run_macros(cmd_macro_obj, macros='Test1:Test2:Test3:Test4', resources='all' , message="Msg", targets={'r0':'Test'}))


    @patch('jnpr.toby.engines.macro.cmd_macro.os.system')
    @patch('jnpr.toby.engines.macro.cmd_macro.StringIO')
    @patch('jnpr.toby.engines.macro.cmd_macro.detect_core')
    @patch('jnpr.toby.engines.macro.cmd_macro.time.sleep')
    @patch('jnpr.toby.engines.macro.cmd_macro.get_log_dir')
    def test__core_collect(self, get_log_dir_patch, sleep_patch, detect_core_patch, StringIO_patch, os_system_patch):
        from jnpr.toby.engines.macro.cmd_macro import cmd_macro

        cmd_macro_obj = MagicMock(spec=cmd_macro)
        cmd_macro_obj.core_check_wait = True
        cmd_macro_obj.log_prefix = 'Test'
        t.core = {'stage' : {'dummy_host' : {'controller' : {'core_src_path' : 'core_src_path_value/', 'core_name' : 'core_name_value'}}}}
        cmd_macro_obj.core_collect = {'r0' : 'Test'}
        cmd_macro_obj.core_check_wait = True
        sleep_patch.return_value = True
        detect_core_patch.return_value = True
        cmd_macro_obj.__log = True
        Test = MagicMock()
        Test.download.return_value = True
        cmd_macro_obj.handles = {'r0' : Test}
        os_system_patch.side_effect = Exception

        self.assertIsNone(cmd_macro._cmd_macro__core_collect(cmd_macro_obj))
        Test.download.return_value = False
        self.assertIsNone(cmd_macro._cmd_macro__core_collect(cmd_macro_obj))
        detect_core_patch.return_value = False
        self.assertIsNone(cmd_macro._cmd_macro__core_collect(cmd_macro_obj))

    @patch('jnpr.toby.engines.macro.cmd_macro.re.search')
    def test__process_vars(self, re_search_patch):
        from jnpr.toby.engines.macro.cmd_macro import cmd_macro

        cmd_macro_obj = MagicMock(spec=cmd_macro)
        re_obj = MagicMock()
        re_obj.group.return_value = 'Test'
        re_search_patch.return_value = re_obj
        cmd_macro_obj.robot_vars = {"${Test}" : False}
        cmd_macro_obj.__log = True
        self.assertTrue(cmd_macro._cmd_macro__process_vars(cmd_macro_obj, macro_lib='Test'))

        cmd_macro_obj.robot_vars = {"Non-Test" : False}
        cmd_macro_obj.local_vars = {'Test' : False}
        self.assertTrue(cmd_macro._cmd_macro__process_vars(cmd_macro_obj, macro_lib='Test'))

        cmd_macro_obj.local_vars = {'Non-Test' : False}
        tv = ['Test']
        self.assertTrue(cmd_macro._cmd_macro__process_vars(cmd_macro_obj, macro_lib='Test'))

    def test__fill_addon_constraints(self):
        from jnpr.toby.engines.macro.cmd_macro import cmd_macro

        cmd_macro_obj = MagicMock(spec=cmd_macro)
        constraint_set = {'constraint_key' : {'Test' : 'Test'}}
        cmd_macro_obj.__fill_addon_constraints = True
        cmd_macro._cmd_macro__fill_addon_constraints(cmd_macro_obj, constraint_set)

        constraint_set = {'user_value' : 'user_value'}
        cmd_macro_obj.addon_constraints = {'user_value' : {'user_value' : {'key' : 'key_value'}}}
        cmd_macro._cmd_macro__fill_addon_constraints(cmd_macro_obj, constraint_set)

    @patch('builtins.__import__')
    @patch('jnpr.toby.engines.macro.cmd_macro.sys')
    @patch('jnpr.toby.engines.macro.cmd_macro.json.dumps')
    @patch('jnpr.toby.engines.macro.cmd_macro.requests')
    @patch('jnpr.toby.engines.macro.cmd_macro.urllib3.disable_warnings')
    def test__rest_call(self, urllib_patch, requests_patch, json_dumps_patch, sys_patch, import_patch):
        cmd_macro_obj = MagicMock(spec=TobyMacro)
        urllib_patch.return_value = True
        command = {'cmd' : {'operation' : 'SomeOperation'}}
        cmd_macro_obj.__log = True
        self.assertIsNone(TobyMacro._rest_call(cmd_macro_obj, command))

        command = {'cmd' : {'operation' : 'get'}}
        rest_response_obj = MagicMock()
        rest_response_obj.text = Exception('Test')
        rest_response_obj.status_code = 200
        rest_call = MagicMock(return_vaue=rest_response_obj)
        requests_patch.operation.return_value = rest_call
        self.assertTrue(TobyMacro._rest_call(cmd_macro_obj, command))

        command = {'cmd' : {'output_formatter' : 'Value', 'auth' : {'user' : 'some_user', 'password' : 'some_password'}}}
        self.assertTrue(TobyMacro._rest_call(cmd_macro_obj, command))

        command = {'cmd' : {'output_formatter' : 'Val/ue.py:Value'}}
        sys_patch.path.insert.return_value = True
        self.assertTrue(TobyMacro._rest_call(cmd_macro_obj, command))

        command = {'cmd' : {'json' : 'json_value', 'data' : 'some_data'}}
        json_dumps_patch.return_value = 'Some_Data'
        self.assertTrue(TobyMacro._rest_call(cmd_macro_obj, command))

        command = {'cmd' : 'Test'}
        self.assertTrue(TobyMacro._rest_call(cmd_macro_obj, command))

    def test__log(self):
        from jnpr.toby.engines.macro.cmd_macro import cmd_macro

        cmd_macro_obj = MagicMock(spec=cmd_macro)
        Obj = MagicMock()
        Obj.info.return_value = True
        cmd_macro_obj.loggers = {'r0' : Obj, 'default' : Obj}
        cmd_macro._cmd_macro__log(cmd_macro_obj, message='Test', resource='r0')

        cmd_macro._cmd_macro__log(cmd_macro_obj, message='Test')

    @patch('jnpr.toby.engines.macro.cmd_macro.logging')
    def test__setup_logger(self, logging_patch):
        from jnpr.toby.engines.macro.cmd_macro import cmd_macro

        cmd_macro_obj = MagicMock(spec=cmd_macro)
        logging_patch.Formatter.return_value = True
        handler_obj = MagicMock()
        handler_obj.setFormatter.return_value = True 
        logging_patch.FileHandler.return_value = handler_obj
        logger_obj = MagicMock()
        logger_obj.setLevel.return_value = True
        logger_obj.addHandler.return_value = True
        logging_patch.getLogger.return_value = logger_obj
        self.assertEqual(cmd_macro._cmd_macro__setup_logger(cmd_macro_obj, name='Test', log_file='Test', level='Test'), logger_obj)

    @patch('builtins.open')
    @patch('jnpr.toby.engines.macro.cmd_macro.re')
    def test__process_file_vars(self, re_patch, open_patch):
        from jnpr.toby.engines.macro.cmd_macro import cmd_macro

        cmd_macro_obj = MagicMock(spec=cmd_macro)
        fhandle = MagicMock()
        fhandle.read.return_value = True
        fhandle.close.return_value = True
        open_patch.return_value = fhandle
        match_obj = MagicMock()
        match = MagicMock()
        match.replace.return_value = True
        match_obj.group.return_value = 'yy[hh\fdgd]'
        re_patch.search.side_effect = [match_obj, False]
        re_patch.sub.return_value = True
        self.assertTrue(cmd_macro._cmd_macro__process_file_vars(cmd_macro_obj, macro_lib='Test'))

    @patch('jnpr.toby.engines.macro.cmd_macro.subprocess')
    def test__system(self, subprocess_patch):
        from jnpr.toby.engines.macro.cmd_macro import cmd_macro

        cmd_macro_obj = MagicMock(spec=cmd_macro)
        subprocess_patch.check_output.side_effect = Exception('Test\\nTesttt')
        self.assertTrue(cmd_macro._cmd_macro__system(cmd_macro_obj, command='Testing')) 

    @patch('jnpr.toby.engines.macro.cmd_macro.re')
    @patch('jnpr.toby.engines.macro.cmd_macro.cli')
    def test_show_chassis_hardware(self, cli_patch, re_patch):
        cmd_macro_obj = MagicMock(spec=TobyMacro)
        cmd_macro_obj.resources_modules = {}
        cmd_macro_obj.handles = {'r0' : 'Test'}
        cli_patch.return_value = True
        re_patch.return_value = True
        cmd_macro_obj._process_hardware_info.return_value = True
        self.assertEqual(TobyMacro.show_chassis_hardware(cmd_macro_obj, mode='mode', resource='r0'), [])

        cmd_macro_obj.resources_modules = {'resource' : [{'module1' : ''}, {'name' : 'name value'}]}
        cmd_macro_obj.user_targets = {'resource' : {'mode' : ['Test']}}
        self.assertEqual(TobyMacro.show_chassis_hardware(cmd_macro_obj, mode='mode', resource='resource', name=[]), [])
        self.assertEqual(TobyMacro.show_chassis_hardware(cmd_macro_obj, mode='mode', resource='resource', name='not-name'), [])
        self.assertEqual(TobyMacro.show_chassis_hardware(cmd_macro_obj, mode='mode', resource='resource', notftn='not-name'), [])

        cmd_macro_obj.user_targets = {'Test' : {'mode' : ['Test']}}
        self.assertEqual(TobyMacro.show_chassis_hardware(cmd_macro_obj, mode='mode', resource='resource'), ['namevalue'])

    def test__process_hw_list(self):
        cmd_macro_obj = MagicMock(spec=TobyMacro)
        cmd_macro_obj._process_hw_list.return_value = True
        cmd_macro_obj.resources_modules = {'r0' : []}
        targets = [['Test'], {'chassis' : 'chassis_value', 'key2' : [{'data' : 'data_value'}], 'key3' : ['Test'], 'key4' : 'Test'  }]
        resource='r0'
        self.assertIsNone(TobyMacro._process_hw_list(cmd_macro_obj, targets, resource))

    @patch('jnpr.toby.engines.macro.cmd_macro.json')
    def test__process_hardware_info(self, json_patch):
        cmd_macro_obj = MagicMock(spec=TobyMacro)
        json_patch.loads.side_effect = Exception('Test')
        cmd_macro_obj._process_hw_list.return_value = True
        cmd_macro_obj.resources_modules = {}
        self.assertIsNone(TobyMacro._process_hardware_info(cmd_macro_obj, json_content='Test', resource='r0'))

        json_patch.loads = MagicMock(return_value={'chassis-inventory':'Test'})
        self.assertIsNone(TobyMacro._process_hardware_info(cmd_macro_obj, json_content='Test', resource='r0'))

    @patch('jnpr.toby.engines.macro.cmd_macro.re')
    def test__run_single_macro(self, re_patch):
        from jnpr.toby.engines.macro.cmd_macro import cmd_macro

        cmd_macro_obj = MagicMock(spec=cmd_macro)
        cmd_macro_obj.__log = True
        macro = 'macro'
        macro_content = ['Test']
        self.assertIsNone(cmd_macro._cmd_macro__run_single_macro(cmd_macro_obj, macro, macro_content))

        macro_content = {'macros' : 'Not-list'}
        with self.assertRaises(TobyException):
            cmd_macro._cmd_macro__run_single_macro(cmd_macro_obj, macro, macro_content)

        macro_content = {'macros' : ['nested-macro', 'something-else']}
        cmd_macro_obj.target_macros = ['nested-macro']
        cmd_macro_obj.completed_macros = []
        self.assertIsNone(cmd_macro._cmd_macro__run_single_macro(cmd_macro_obj, macro, macro_content))

        macro_content = {'commands' : 'malformed-macro'}
        with self.assertRaises(TobyException):
            cmd_macro._cmd_macro__run_single_macro(cmd_macro_obj, macro, macro_content)

        macro_content = {'constraints' : ['not-dict']}
        with self.assertRaises(TobyException):
            cmd_macro._cmd_macro__run_single_macro(cmd_macro_obj, macro, macro_content)

        macro_content = {'comment' : 'str-comment', 
                         'target' : 'Test',
                         'constraints' : {'params' : {'tags' : 'f-tags'}, 'resources' : {'controllers' : ['Test']}}}
        cmd_macro_obj.comments = {}
        cmd_macro_obj.current_resources = ['r0']
        t.get_resource_list.return_value = ['r0']
        cmd_macro_obj.__fill_addon_constraints = True
        self.assertIsNone(cmd_macro._cmd_macro__run_single_macro(cmd_macro_obj, macro, macro_content))

        macro_content = {'constraints' : {'resources' : {'model' : 'Test'}}}
        self.assertIsNone(cmd_macro._cmd_macro__run_single_macro(cmd_macro_obj, macro, macro_content))

        macro_content = {'commands' : ['command_type()'],
                         'constraints' : {'resources' : {}, 'targets' : {'mode1' : 'var_unknown(something)', 'mode2' : 'something,else'}}}
        cmd_macro_obj.verbosity = 'medium'
        match_obj = MagicMock()
        match_obj.group.return_value = 'True'
        re_patch.search.return_value = match_obj
        self.assertIsNone(cmd_macro._cmd_macro__run_single_macro(cmd_macro_obj, macro, macro_content))


def create_t_data():
    """
    Create t data
    :return:
        Returns t data
    """
    t.t_dict = dict()
    t.t_dict['resources'] = dict()
    t.t_dict['resources']['r0'] = dict()
    t.t_dict['resources']['r0']['interfaces'] = dict()
    t.t_dict['resources']['r0']['interfaces']['fe0'] = dict()
    t.t_dict['resources']['r0']['interfaces']['fe0']['name'] = 'fe0.0'
    t.t_dict['resources']['r0']['interfaces']['fe0']['link'] = 'link'
    t.t_dict['resources']['r0']['system'] = dict()
    t.t_dict['resources']['r0']['system']['dh'] = "test"
    t.t_dict['resources']['r0']['system']['primary'] = dict()
    t.t_dict['resources']['r0']['system']['primary']['controllers'] = dict()
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'dummy_host'
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '10.1.1.1'
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['osname'] = 'JunOS'
    t.t_dict['resources']['r0']['system']['primary']['name'] = 'dummy_host'
    t.t_dict['resources']['r0']['system']['primary']['model'] = 'mx'
    t.t_dict['resources']['r0']['system']['primary']['make'] = 'Juniper'
    t.t_dict['resources']['r0']['system']['primary']['osname'] = 'JunOS'
    t.t_dict['user_variables'] = dict()
    t.t_dict['user_variables']['uv_var1'] = 'test-value-1'
    t.t_dict['user_variables']['uv-var2'] = 'test-value-2'

def create_macro_lib_dict():
    macro_lib = {'filetype':'macro_lib','vars':{'a':'b'},'macro1':{'macros':['macroa','macrob']},'macroa':{'constraints':{'resources':{'model':'mx','osname':'JUNOS'},'targets':{'vty':{'function':'show_chassis_hardware','name':'fpc'}}},'commands':{'cli':['show chassis hardware', "some command with var['uv_var1']", "some command with var['uv-var2']"],'config':['set foo'],'shell':['ls /tmp'],'vty':['show version']}},'macrob':{'system':['ls /tmp'],'commands':['fetch_cores()','rest(http://foo123abc.juniper.net)']}}
    return macro_lib

def create_macro_lib_str():
    macro_lib = '''
filetype:macro_lib
vars:
  a:b
macro1:
  macros:
  - macroa
  - macrob

macroa:
  constraints:
    resources:
      model:mx
      osname:JUNOS
    targets:
      vty:
        function:show_chassis_hardware
        name:fpc
  commands:
    cli:
    - show chassis hardware
    - some command with var['uv_var1']
    - some command with var['uv-var2']
    shell:
    - ls /tmp
    config:
    - set foo
    vty:
    - show version
macrob:
  system:
    - ls /tmp
  commands:
    - fetch_cores()
    - rest('http://foo123.juniper.net')'''

    return macro_lib
      
if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestCmdMacro)
    unittest.TextTestRunner(verbosity=2).run(SUITE)