import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.tools.listeners.lib_version import lib_version

class TestLibVersion(unittest.TestCase):
    """
    TestLibVersion class to handle lib_version.py unit tests
    """
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self._obj = lib_version()

    @patch('robot.running.context.EXECUTION_CONTEXTS')
    def test_new_obj(self, exec_ctx):
        obj = lib_version()

    @patch('robot.libraries.BuiltIn.BuiltIn.get_variable_value')
    @patch('robot.running.context.EXECUTION_CONTEXTS')    
    def test_start_suite(self, exec_ctx, get_variable_value_mock):
        obj = lib_version()
        get_variable_value_mock.return_value = "./"
   
    def test_library_import(self):
        self._obj.library_import('test', {'importer': 'abc', 'source': '/some/path/some_lib.py'})

    def test_resource_import(self):
        self._obj.resource_import('test', {'importer': 'abc', 'source': '/some/path/some_lib.py'})

    def test_variables_import(self):
        self._obj.variables_import('test', {'importer': 'abc', 'source': '/some/path/some_lib.py'})

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestLibVersion)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
