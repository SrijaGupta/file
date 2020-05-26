"""UT for the module jnpr.toby.hldcl.juniper.security.nfxnode"""

import unittest2 as unittest
from mock import patch, MagicMock

from collections import defaultdict
from jnpr.toby.hldcl.juniper.security.nfxnode import NfxNode

class TestNfxNode(unittest.TestCase):
    """UT for NfxNode"""
    def test_nfxnode_init(self):
        """Test '__init__' method of class NfxNode"""
        nobject = MagicMock(spec=NfxNode)
        self.assertIsInstance(nobject, NfxNode)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestNfxNode)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
