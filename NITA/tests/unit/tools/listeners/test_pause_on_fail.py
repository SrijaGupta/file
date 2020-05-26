import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.tools.listeners.pause_on_fail import pause_on_fail

class TestPauseOnFail(unittest.TestCase):
    """
    TestPauseOnFail class to handle pause_on_fail.py unit tests
    """
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('robot.running.context.EXECUTION_CONTEXTS')
    def test_new_obj(self, exec_ctx):
        obj = pause_on_fail()

    @patch('robot.libraries.BuiltIn.BuiltIn.get_variable_value')
    @patch('robot.running.context.EXECUTION_CONTEXTS')    
    def test_end_keyword(self, exec_ctx, get_variable_value_mock):
        obj = pause_on_fail()
        get_variable_value_mock.return_value = 'test.robot'
        rc = obj.end_keyword('test', {'status': 'PASS'})
        self.assertFalse(rc)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestPauseOnFail)
    unittest.TextTestRunner(verbosity=2).run(SUITE)