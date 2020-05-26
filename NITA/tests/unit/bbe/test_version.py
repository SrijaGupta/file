import unittest
import builtins
from mock import patch, MagicMock
from jnpr.toby.bbe.version import *

class TestVersion(unittest.TestCase):
    """
    TestVersion class to handle version.py unit tests
    """
    def test_get_bbe_version(self):
        self.assertEqual(get_bbe_version(), '1.0')

    def test_get_bbe_full_version(self):
        self.assertEqual(get_bbe_full_version(), 'TOBY BBE RELEASE 1.0')

    @patch('jnpr.toby.bbe.version.get_bbe_full_version')
    def test_log_bbe_version(self, patch_version):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        patch_version.side_effect = Exception
        try:
            log_bbe_version()
        except Exception as err:
            self.assertTrue('failed:' in err.args[0])
        patch_version.side_effect = None

if __name__ == '__main__':
    unittest.main()