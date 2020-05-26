"""
    UT for junipersystem.py
"""

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from jnpr.toby.hldcl.juniper.switching.exsystem import ExSystem
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hldcl.system  import *

## place holder for exsystem testcases
class TestExSystem(unittest.TestCase):
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('jnpr.toby.hldcl.juniper.switching.exsystem.JuniperSystem.__init__')
    def test_exsystem_init(self, sup_init_patch):
        sobject = MagicMock()
        ExSystem.nodes = {}
        ExSystem.nodes['primary'] = MagicMock(return_value=sobject)
        sobject.current_controller = True
        ExSystem.current_node = MagicMock()

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        system_data['system']['primary']['controllers']['re0']['connect'] = True
        system_data['system']['member1']['controllers']['re0']['connect'] = True
        self.assertIsInstance(ExSystem(system_data), ExSystem)
        self.assertTrue(sup_init_patch.called)


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
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['model'] = 'ex'
    init_data['t']['resources']['r0']['system']['member1'] = dict()
    init_data['t']['resources']['r0']['system']['member1']['controllers'] = dict()
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0'] = dict()
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['hostname'] = 'abc1'
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['osname'] = 'junos'
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['host'] = 'host12'
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['model'] = 'ex'

    return init_data


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExSystem)
    unittest.TextTestRunner(verbosity=2).run(suite)

