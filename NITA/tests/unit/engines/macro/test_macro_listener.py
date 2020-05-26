# pylint: disable=undefined-variable,invalid-name,bad-whitespace,missing-docstring

import builtins
from datetime import datetime
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import re
import sys
from jnpr.toby.engines.macro.macro_listener import macro_listener as MacroListener

class TestMacroListener(unittest.TestCase):

    def setUp(self):
        pass

    @patch('robot.libraries.BuiltIn.BuiltIn')
    def test_macro_listener(self, builtin_patch):
        builtin_patch.get_variables = MagicMock()
        macro_listener = MacroListener()
#        cmd_macro.loggers = MagicMock()
        result = MagicMock()
        result.passed = False
        macro_listener.end_test(data='foo',result=result)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestMacroListener)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
