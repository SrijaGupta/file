"""
    UT for brocadesystem.py
"""

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.hldcl.brocade.brocadesystem import BrocadeSystem

class TestBrocadeSystem(unittest.TestCase):
    def setUp(self):
        import builtins 
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('sys.stdout')
    @patch('jnpr.toby.hldcl.brocade.brocadesystem.Brocade')
    @patch('jnpr.toby.hldcl.brocade.brocadesystem.System.__init__')
    @patch('jnpr.toby.hldcl.brocade.brocadesystem.Host._object_counts')
    def test_brocadesystem_init(self, host_patch, sup_init_patch, brocade_patch, stdout_patch):
        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        
        self.assertIsInstance(BrocadeSystem(system_data), BrocadeSystem)
        self.assertTrue(sup_init_patch.called)

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        from jnpr.toby.hldcl.brocade.brocade import Brocade 
        brocade_patch = MagicMock(spec=Brocade)
        system_data['system']['primary']['controllers']['re1'] = {'test': {}, 'hostname' : 'xyz'}
        self.assertIsInstance(BrocadeSystem(system_data), BrocadeSystem)
        self.assertTrue(sup_init_patch.called)

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        system_data['system']['primary']['connect'] = True
        system_data['system']['primary']['controllers']['re0'] = {'test': {}, 'hostname' : 'xyz'}
        system_data['system']['secondary'] = system_data['system'].pop('primary')
        self.assertIsInstance(BrocadeSystem(system_data, connect_dual_re=True), BrocadeSystem)
                
        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        system_data['system']['primary']['controllers']['re0']['connect'] = True
        system_data['system']['primary']['controllers']['re1'] = {'test': {}, 'hostname' : 'xyz'}
        system_data['system']['secondary'] = system_data['system'].pop('primary')
        self.assertIsInstance(BrocadeSystem(system_data), BrocadeSystem)

        BrocadeSystem.is_controller_connect_set = MagicMock(return_value=True)
        system_data['system']['secondary']['connect'] = True
        self.assertIsInstance(BrocadeSystem(system_data), BrocadeSystem)
        
        BrocadeSystem.is_controller_connect_set = MagicMock(return_value=True)
        system_data['system']['secondary'].pop('connect')
        self.assertIsInstance(BrocadeSystem(system_data), BrocadeSystem)


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
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['osname'] = 'BORCADE'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['host'] = 'host1'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['model'] = '7200'
    init_data['t']['resources']['r0']['system']['primary']['osname'] = 'IOS'
    return init_data


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBrocadeSystem)
    unittest.TextTestRunner(verbosity=2).run(suite)
