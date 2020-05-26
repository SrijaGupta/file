''' Unit Test for lxml_parser.py '''
#!/usr/local/bin/python3

import sys
import mock
from mock import patch
from mock import Mock
from mock import MagicMock
import unittest
import unittest2 as unittest
import unittest.mock
from optparse import Values

import builtins
from jnpr.toby.services.vsrx_aws.lxml_parser import *

builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

class test_lxml_parser(unittest.TestCase):

    @patch('lxml.etree.parse')
    @patch('lxml.etree.XSLT')
    def test_convert_config(self, lxml_arg, lxml_arg2):
        open = MagicMock()
        file_handler = MagicMock()
        convert_config.return_value = None
        self.assertEqual(convert_config('mock_file.xml', 'mock_xsltfile', 'mock_config_file'), 'mock_config_file')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_lxml_parser)

    unittest.TextTestRunner(verbosity=2).run(suite)
