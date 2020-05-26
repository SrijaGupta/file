"""
Checkconfig.py Unit Test
"""
import unittest2 as unittest
from mock import call, patch

from jnpr.toby.engines.config.checkconfig import main as chkcfg
import getopt
import inspect

class TestCheckConfig(unittest.TestCase):
    """
    TestCheckConfig class to handle Checkconfig.py unit tests
    """
    @patch('jnpr.toby.engines.config.checkconfig.getopt.getopt')
    @patch('jnpr.toby.engines.config.checkconfig.usage')
    def test_checkconfig_main_no_args(self, usage_mock, getopt_mock):
        """
        Tests main() to raise SystemExit exception when no parameters are provided
        :param usage_mock:
            Mocked object for usage
        :param getopt_mock:
            Mocked object for getopt
        :return:
            Returns true or false depending on test results
        """
        getopt_mock.return_value = [None]
        self.assertRaises(SystemExit, chkcfg)
        self.assertTrue(usage_mock.called)

    @patch('jnpr.toby.engines.config.checkconfig.getopt.getopt')
    @patch('jnpr.toby.engines.config.checkconfig.usage')
    def test_checkconfig_main_raise_exception(self, usage_mock, getopt_mock):
        """
        Tests main() to raise SystemExit exception on getopt error with parameter fetching
        :param usage_mock:
            Mocked object for usage
        :param getopt_mock:
            Mocked object for getopt
        :return:
            Returns true or false depending on test results
        """
        getopt_mock.side_effect = getopt.GetoptError('message')
        self.assertRaises(SystemExit, chkcfg)
        self.assertTrue(usage_mock.called)

    @patch('jnpr.toby.engines.config.checkconfig.getopt.getopt')
    @patch('jnpr.toby.engines.config.checkconfig.usage')
    def test_checkconfig_main_usage(self, usage_mock, getopt_mock):
        """
        Tests main() help usage
        :param usage_mock:
            Mocked object for usage
        :param getopt_mock:
            Mocked object for getopt
        :return:
            Returns true or false depending on test results
        """
        getopt_mock.return_value = [[('-h', '')]]
        self.assertRaises(SystemExit, chkcfg)
        self.assertTrue(usage_mock.called)

    @patch('jnpr.toby.engines.config.checkconfig.getopt.getopt')
    @patch('jnpr.toby.engines.config.checkconfig.config')
    @patch('jnpr.toby.engines.config.checkconfig.config_utils')
    @patch('jnpr.toby.engines.config.checkconfig.print', create=True)
    @patch('jnpr.toby.engines.config.checkconfig.pprint', create=True)
    def test_checkconfig_main(self, pprint_mock, stdout_mock, configutils_mock, config_mock, getopt_mock):
        """
        Tests main() with parameters
        :param stdout_mock:
            Mocked stdout object
        :param configutils_mock:
            Mocked configutils object
        :param config_mock:
            Mocked config object
        :param getopt_mock:
            Mocked getopt object
        :return:
            Returns true or false depending on test results
        """
        getopt_mock.return_value = [[('-t', 'params_file_name'), ('-c', 'config_file_name'), ('-v', '')]]
        data = dict()
        data['t'] = dict()
        data['t']['resources'] = 'router'
        configutils_mock.read_yaml_file.return_value = data
        cfg = dict()
        cfg['router'] = ['set commands']
        config_mock.return_value.cfg = cfg
        config_mock.return_value.config_engine.return_value = cfg

        chkcfg()
#        self.assertTrue(config_mock.return_value._make_ifd_tvar.called)
        self.assertTrue(config_mock.return_value.config_engine.called)

        configutils_mock.read_yaml.return_value = None
        self.assertRaises(Exception, chkcfg)

    @patch('sys.exit')
    def test_checkconfig_execution(self, exit_mock):
        """
        Tests standalone execution of checkconfig.py
        :param exit_mock:
            Mocked sys.exit object
        :return:
            Returns true or false depending on test results
        """
        file_path = inspect.getfile(chkcfg)
        import types
        import importlib.machinery
        loader = importlib.machinery.SourceFileLoader('__main__', file_path)
        mod = types.ModuleType(loader.name)
        try:
            loader.exec_module(mod)
        except Exception:
            self.assertTrue(exit_mock.called)
