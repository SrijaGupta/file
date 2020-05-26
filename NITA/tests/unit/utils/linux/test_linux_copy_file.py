#! /usr/bin/python3

from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.utils.linux.linux_copy_file import linux_copy_file


class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.shell = MagicMock()


#### UT for linux_copy_file starts here
    def test_linux_copy_file_exception(self):
        try:
           linux_copy_file(linux_host=self.mocked_obj) 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "linux_host, remote ip and local_file are mandatory arguments")


    def test_linux_copy_file_execution_1(self):
        lst = [Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(linux_copy_file(linux_host=self.mocked_obj, remote_ip="5.0.0.1", local_file="testfile.txt", action="download"), True)

    def test_linux_copy_file_execution_1(self):
        lst = [Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(linux_copy_file(linux_host=self.mocked_obj, remote_ip="5.0.0.1", local_file="testfile.txt", action="upload"), True)

    def test_linux_copy_file_execution_2(self):
        lst = [Response("Permission denied")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            linux_copy_file(linux_host=self.mocked_obj, remote_ip="5.0.0.1", local_file="testfile.txt")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Could not copy the file")

if __name__ == '__main__':
    unittest.main()
