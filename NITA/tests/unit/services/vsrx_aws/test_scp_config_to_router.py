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
from jnpr.toby.services.vsrx_aws.scp_config_to_router import *

builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

class test_scp_config_to_router(unittest.TestCase):

    @patch('os.system')
    def test_scp_file_to_vsrx(self, os_system):
        print(os_system)
        self.assertEqual(scp_file_to_vsrx('127.0.0.1', 'mock_file.xml', 'Seoul'), True) 

        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_scp_config_to_router)

    unittest.TextTestRunner(verbosity=2).run(suite)

