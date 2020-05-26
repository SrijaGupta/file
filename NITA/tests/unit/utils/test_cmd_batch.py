import sys
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from jnpr.toby.init.init import init
from jnpr.toby.utils.cmd_batch import TobyCmdBatch 

builtin_string = 'builtins'


class TestTobyCmdBatch(unittest.TestCase):
    def setUp(self):
        init_obj = MagicMock(spec=init)
        init_obj.t_dict = create_t_data()
        init_obj.log = MagicMock()
        init_obj.get_resource_list.return_value = 'r0'
        import builtins
        builtins.t = init_obj

    def test_cmd_batch_init(self):
        # callable progress
        cb_obj = TobyCmdBatch()

    def test_cmd_batch_run_commands(self):
        cb_obj = TobyCmdBatch()
        cb_obj.templates = dict()
        cb_obj.templates['test'] = list()
        cb_obj.templates['test'].append(dict())
        cb_obj.templates['test'][0]['commands'] = list()
        cb_obj.templates['test'][0]['commands'].append('cli(show version)')
        cb_obj.templates['test'][0]['commands'].append('shell(show version)')
        cb_obj.templates['test'][0]['commands'].append('pyez(show version)')
        cb_obj.templates['test'][0]['commands'].append('config(show version)')
        cb_obj.templates['test'][0]['commands'].append('vty(fpc0:show version)')
        cb_obj.templates['test'][0]['commands'].append('cty(fpc0:show version)')
   
        cb_obj.run_commands(template='test')

def create_t_data():
    """
    Function to create t_data
    :return:
        Returns t_data
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
    init_data['t']['resources']['r0']['system']['primary']['name'] = 'abc'
    init_data['t']['resources']['r0']['system']['primary']['model'] = 'mx'
    init_data['t']['resources']['r0']['system']['primary']['make'] = 'Juniper'
    init_data['t']['resources']['r0']['system']['primary']['osname'] = 'junos'
    return init_data

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestTobyCmdBatch)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
