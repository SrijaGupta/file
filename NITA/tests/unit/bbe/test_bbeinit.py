"""
bbeinit.py unit test
"""

import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.bbeinit import BBEInit
import builtins
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.bbe.errors import BBEInitError
from jnpr.toby.bbe.bbevar.bbevars import BBEVars
builtins.t = MagicMock(spec=init)
builtins.t.log = MagicMock()


class TestBbeInit(unittest.TestCase):
    """
    test bbeinit.py
    """
    @patch('yaml.load')
    @patch('builtins.open')
    @patch('jnpr.toby.bbe.testers.bbert.bbe_rt_init')
    @patch('os.path.isfile')
    @patch('robot.libraries.BuiltIn.BuiltIn.get_variables', return_value = {'${SUITE_SOURCE}': 'test.robot'})
    @patch('jnpr.toby.bbe.bbevar.bbevars.BBEVars.initialize')
    def test_class_bbeinit(self, patch_bvar_init, patch_builtin, patch_os, patch_bbert, patch_open, pload):
        initobj = MagicMock(spec=BBEInit)
        initobj.log_tag = 'test'
        self.assertEqual(BBEInit.__init__(initobj), None)
        try:
            BBEInit.bbe_initialize(initobj, config_file='test.yaml')
        except:
            self.assertRaises(BBEInitError)

        try:
            patch_builtin.side_effect = Exception
            BBEInit.bbe_initialize(initobj)
        except:
            self.assertRaises(BBEInitError)
        patch_builtin.side_effect = None
        patch_os.return_value = True
        pload.return_value = {'bbevar': {'resource': {}}}
        self.assertEqual(BBEInit.bbe_initialize(initobj), None)
        patch_builtin.return_value = {'${SUITE_SOURCE}': 'test.robot.cfg'}
        try:
            BBEInit.bbe_initialize(initobj)
        except:
            self.assertRaises(BBEInitError)
        patch_builtin.return_value = {'${SUITE_SOURCE}': 'test.robot'}
        try:
            patch_os.return_value = False
            BBEInit.bbe_initialize(initobj)
        except:
            self.assertRaises(BBEInitError)
        patch_os.return_value = True
        try:
            pload.return_value = {'bbevar': [{'resource': {}}]}
            BBEInit.bbe_initialize(initobj)
        except:
            self.assertRaises(BBEInitError)
        builtins.t.user_variables = {'uv-bbevar': {'debug': {}}}
        builtins.t.t_dict = {'user_variables': {'uv-bbevar' :{'debug':{}}}, 'resources': {}}
        self.assertEqual(BBEInit.bbe_initialize(initobj), None)




    def test_log_info(self):
        builtins.bbe = MagicMock(spec=BBEVars)
        builtins.bbe.bbevar = {}
        initobj = MagicMock(spec=BBEInit)
        initobj.log_tag = 'test'
        self.assertEqual(BBEInit.log_test_info(initobj), None)
        builtins.bbe.bbevar = {'test': {}}
        self.assertEqual(BBEInit.log_test_info(initobj), None)
        builtins.bbe.bbevar = {'test': {'description': 'this is desc', 'type': 'up', 'id': '111'}}
        self.assertEqual(BBEInit.log_test_info(initobj), None)



if __name__ == '__main__':
    unittest.main()