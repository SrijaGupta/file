# pylint: disable=undefined-variable,invalid-name,bad-whitespace,missing-docstring

import builtins
from datetime import datetime
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import re
import sys
from jnpr.toby.docs.doc_reader import reader as Reader

class TestDocReader(unittest.TestCase):

    def setUp(self):
        pass

    @patch('os.system')
    def test_doc_reader(self, system_patch):
        system_patch.return_value = True
        Reader(target = 'topics')
        Reader(target = 'macro_engine')

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDocReader)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
