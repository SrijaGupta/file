"""
    UT for junipersystem.py
"""

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from jnpr.toby.hldcl.juniper.switching.qfxsystem import QfxSystem
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hldcl.system  import *

## place holder for mxsystem testcases
class TestQfxSystem(unittest.TestCase):
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('jnpr.toby.hldcl.juniper.switching.qfxsystem.JuniperSystem.__init__')
    def test_qfxsystem_init(self, sup_init_patch):
        sobject = MagicMock()
        QfxSystem.nodes = {}
        QfxSystem.nodes['primary'] = MagicMock(return_value=sobject)
        sobject.current_controller = True
        QfxSystem.current_node = MagicMock()

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        system_data['system']['primary']['controllers']['re0']['connect'] = True
        system_data['system']['member1']['controllers']['re0']['connect'] = True
        self.assertIsInstance(QfxSystem(system_data), QfxSystem)
        self.assertTrue(sup_init_patch.called)



    @patch('jnpr.toby.hldcl.juniper.switching.qfxsystem.JuniperSystem.__init__')
    def test_qfxsystem_reboot(self, sup_init_patch):
        qfxobject = QfxSystem(system_data=create_system_data())
        qfxobject.reboot(system_nodes='all-members')
        qfxobject.reboot(system_nodes='member2')
        qfxobject.reboot(system_nodes='local')



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
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['model'] = 'qfx'
    init_data['t']['resources']['r0']['system']['member1'] = dict()
    init_data['t']['resources']['r0']['system']['member1']['controllers'] = dict()
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0'] = dict()
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['hostname'] = 'abc1'
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['osname'] = 'junos'
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['host'] = 'host12'
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['model'] = 'qfx'

    return init_data


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
    system_data['system']['primary']['controllers']['re0']['osname'] = 'junos'
    system_data['system']['primary']['controllers']['re0']['host'] = 'host1'
    system_data['system']['primary']['controllers']['re0']['model'] = 'qfx123'
    system_data['system']['primary']['name'] = 'abc'
    system_data['system']['primary']['model'] = 'qfx123'
    system_data['system']['primary']['make'] = 'Juniper'
    system_data['system']['primary']['osname'] = 'junos'

    return system_data


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQfxSystem)
    unittest.TextTestRunner(verbosity=2).run(suite)

