"""UT for the module jnpr.toby.hldcl.juniper.security.nfxsystem"""

import unittest2 as unittest
from mock import patch, MagicMock

from collections import defaultdict
from jnpr.toby.hldcl.juniper.security.nfxsystem import NfxSystem

class TestNfxSystem(unittest.TestCase):
    """UT for NfxSystem"""
    def test_nfxsystem_init(self):
        """Test '__init__' method of class NfxSystem"""
        nobject = MagicMock(spec=NfxSystem)
        self.assertIsInstance(nobject, NfxSystem)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestNfxSystem)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
