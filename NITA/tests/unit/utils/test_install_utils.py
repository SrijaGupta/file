import sys
import os
import unittest2 as unittest
from mock import patch, MagicMock, Mock
from jnpr.toby.utils.install_utils import _aft_pakcage_install, _ulc_pakcage_install
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.utils.response import Response

class TestInstallUtils(unittest.TestCase):
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        t.is_robot = True
        t._script_name = 'name'

    @patch('os.path.exists')
    def test_aft_pakcage_install(self, path_exists_mock):

        jobject = MagicMock(spec=Juniper)
        jobject.su.return_value = True
        jobject.upload.return_value = True
        path_exists_mock.return_value = True
        jobject.name = "abc"

        jobject.cli.return_value.response.return_value = "test"
        jobject.shell.return_value.response.return_value = "test"

        self.assertTrue(_aft_pakcage_install(jobject, package='package'))
        self.assertTrue(_ulc_pakcage_install(jobject, package='package.tgz, package.tgz.sha1'))
     

    @patch('os.path.exists')
    def test_ulc_pakcage_install(self, path_exists_mock ):

        jobject = MagicMock(spec=Juniper)
        jobject.su.return_value = True 
        jobject.upload.return_value = True
        path_exists_mock.return_value = True
        jobject.cli.return_value.response.return_value = "test"
        jobject.shell.return_value.response.return_value = "test"

        self.assertFalse(_ulc_pakcage_install(jobject, package='package'))
        self.assertTrue(_ulc_pakcage_install(jobject, package='package.tgz'))

if __name__ == '__main__':
	unittest.main()

