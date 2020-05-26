"""
    UT for junipersystem.py
"""

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from jnpr.toby.hldcl.juniper.routing.mxsystem import MxSystem

## place holder for mxsystem testcases
class TestMxSystem(unittest.TestCase):
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('jnpr.toby.hldcl.juniper.routing.mxsystem.JuniperSystem.__init__')
    def test_mxsystem_init(self, sup_init_patch):
        sobject = MagicMock()
        MxSystem.nodes = {}
        MxSystem.nodes['primary'] = MagicMock(return_value=sobject)
        sobject.current_controller = True
        MxSystem.current_node = MagicMock()

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        system_data['system']['primary']['controllers']['re0']['connect'] = True
        system_data['system']['member1']['controllers']['re0']['connect'] = True
        self.assertIsInstance(MxSystem(system_data), MxSystem)
        self.assertTrue(sup_init_patch.called)

    def test_mxsystem_switch_re_master(self):
        sobject = MagicMock()
        sobject.current_node.current_controller.is_master.return_value = True
        sobject.current_node.current_controller.switch_re_master.return_value = False
        self.assertFalse(MxSystem.switch_re_master(sobject))

    @patch('jnpr.toby.hldcl.juniper.routing.mxsystem.JuniperSystem.reboot')
    def test_mxsystem_reboot(self, sup_reboot_patch):
        sobject = MagicMock()
        obj1 = MagicMock()
        obj2 = MagicMock()
        sobject.nodes={'node0':obj1}
        obj1.controllers={'re0':obj2}
        obj2.reboot.return_value = True
#        self.assertEqual(MxSystem.reboot(sobject),True)
        self.assertFalse(sup_reboot_patch.called)

    @patch('jnpr.toby.hldcl.juniper.routing.mxsystem.JuniperSystem.reconnect')
    def test_mxsystem_reconnect(self, sup_reconnect_patch):
        sobject = MagicMock()
        obj1 = MagicMock()
        obj2 = MagicMock()
        sobject.nodes={'node0':obj1}
        obj1.controllers={'re0':obj2}
        obj2.reconnect.return_value = True
        self.assertFalse(sup_reconnect_patch.called)

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
    init_data['t']['resources']['r0']['system']['member1'] = dict()
    init_data['t']['resources']['r0']['system']['member1']['controllers'] = dict()
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0'] = dict()
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['hostname'] = 'abc1'
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['osname'] = 'junos'
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['host'] = 'host12'
    init_data['t']['resources']['r0']['system']['member1']['controllers']['re0']['model'] = 'mx'

    return init_data


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMxSystem)
    unittest.TextTestRunner(verbosity=2).run(suite)

