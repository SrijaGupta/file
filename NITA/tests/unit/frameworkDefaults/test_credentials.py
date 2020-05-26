import sys

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.frameworkDefaults.credentials  import *

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'


@attr('unit')
class TestCredentials(unittest.TestCase):

    def test___readonly__(self):
        sobject = MagicMock(spec=ReadOnlyDict)
    
        try:
            ReadOnlyDict.pop(sobject)
        except RuntimeError as err:
            self.assertEqual(err.args[0], "Cannot modify ReadOnlyDict")


    def test_get_credentials(self):

        self.assertEqual(type(get_credentials( os='JUNOS')), tuple)
        self.assertEqual(type(get_credentials( os='UNIX')), tuple)
        self.assertEqual(type(get_credentials( os='IOS')), tuple)
        self.assertEqual(type(get_credentials( os='SPIRENT')), tuple)
        self.assertEqual(type(get_credentials( os='IXIA')), tuple)
        self.assertEqual(type(get_credentials( os='WINDOWS')), tuple)
        self.assertEqual(type(get_credentials( os='BREAKINGPOINT')), tuple)

        try:
            get_credentials( os='IXIA')
        except Exception as err:
            self.assertEqual(err.args[0], 'Unknown Device OS')

        self.assertEqual(type(get_credentials ( user='user',password='password')), tuple)

        try:
            ReadOnlyDict(get_credentials( os='DOS'))
        except Exception as err:
            self.assertEqual(err.args[0], 'Unknown Device OS')

    @patch('jnpr.toby.frameworkDefaults.credentials.JUNOS', {
    'USERNAME': None,
    'PASSWORD': None,
    'FTPUSERNAME': None,
    'FTPPASSWORD': None,
    'SU': 'root',
    'SUPASSWORD': 'Embe1mpls',
})
    def test_get_credentials_failure(self):
        try:
            get_credentials (os='JUNOS') 
        except Exception as err:
            self.assertEqual(err.args[0], "Username/Password cannot be determined")

if __name__=='__main__':
    unittest.main()
