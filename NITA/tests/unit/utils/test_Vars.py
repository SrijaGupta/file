import unittest2 as unittest
from mock import patch, MagicMock, create_autospec
from nose.plugins.attrib import attr

import jnpr.toby.utils.Vars as Vars
import importlib

@attr('unit')
class TestVars(unittest.TestCase):
    def test_module_expr(self):
        with patch.dict('sys.modules', {'robot.running.context':None}):
            importlib.reload(Vars)
            self.assertEqual(Vars.robot_lib_ctx, False)
        with patch.dict('sys.modules', {'robot.running.context.EXECUTION_CONTEXTS':None}):
            importlib.reload(Vars)
            self.assertEqual(Vars.robot_lib_ctx, False)
        with patch('robot.running.context.EXECUTION_CONTEXTS') as robo_mock:
            robo_mock.current = True
            robo_mock.top = True
            importlib.reload(Vars)
            self.assertEqual(Vars.robot_lib_ctx, True)

    @patch('jnpr.toby.utils.Vars.BuiltIn')
    def test_get_global_variable(self, builtin_mock):
        # Robot mode
        Vars.robot_lib_ctx = True
        builtin_mock().get_variable_value = MagicMock(return_value='test')
        self.assertEqual(Vars.Vars.get_global_variable('test'), 'test')
        # non-Robot mode
        Vars.robot_lib_ctx = False
        self.assertEqual(Vars.Vars.get_global_variable('test'), None)
        with patch.dict('jnpr.toby.utils.Vars.Vars.global_vars', {'test':'test'}, clear=True):
            self.assertEqual(Vars.Vars.get_global_variable('test'), 'test')

    @patch('jnpr.toby.utils.Vars.BuiltIn')
    def test_set_global_variable(self, builtin_mock):
        # Robot mode
        Vars.robot_lib_ctx = True
        mock_fn = create_autospec(builtin_mock().set_variable_value, return_value='test')
        Vars.Vars.set_global_variable('test', 'test')
        mock_fn.assert_called_once_with('test', 'test')
        # non-Robot mode
        Vars.robot_lib_ctx = False
        self.assertTrue(Vars.Vars.set_global_variable('test', 'test'))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVars)
    unittest.TextTestRunner(verbosity=2).run(suite)
