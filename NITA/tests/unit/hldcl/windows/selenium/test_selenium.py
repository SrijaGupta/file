import sys
import unittest2 as unittest
from mock import patch, MagicMock

from jnpr.toby.hldcl.windows.selenium.selenium import Selenium
from jnpr.toby.hldcl.windows.windows import Windows
import os
import re
import time
from select import select
from jnpr.toby.utils.response import Response

class Testselenium(unittest.TestCase):
    @patch('jnpr.toby.hldcl.windows.windows.Windows.__init__')
    def test_init(self,Windows_patch):

        super_obj = MagicMock(spec=Selenium)
        Selenium.__init__(super_obj,host='host')

    def test_execute(self):
        sebject = MagicMock(spec=Selenium)
        sebject.prompt = "$"
        sebject.handle = MagicMock()
        sebject.handle.execute.return_value = True
        self.assertEqual(Selenium.execute(sebject,pattern="$",command="show version"),True)
        self.assertRaises(Exception,Selenium.execute,sebject,pattern="$")

    def test_shell(self):
        sebject = MagicMock(spec=Selenium)
        sebject.prompt = "$"
        sebject.execute.side_effect = [-1,1]
        sebject.response = "test\n"
        self.assertRaises(Exception,Selenium.shell,sebject,pattern="$",command="show version")
        self.assertIsInstance(Selenium.shell(sebject,pattern="$",command="show version"),Response)
        self.assertRaises(Exception,Selenium.shell,sebject,pattern="$")

    def test_close(self):
        sebject = MagicMock(spec=Selenium)
        sebject.connect_mode = "ssh"
        sebject.handle = MagicMock()
        sebject.handle.client = MagicMock()
        sebject.handle.client.close.return_value=True
        self.assertEqual(Selenium.close(sebject),True)
        sebject.connect_mode = "telnet"
        sebject.handle.close.side_effect= Exception('error')
        self.assertRaises(Exception,Selenium.close,sebject)

    @patch('jnpr.toby.hldcl.windows.selenium.selenium.re.search')
    @patch('jnpr.toby.hldcl.juniper.junos.Response')
    def test__download_selenium_jar(self, resp_patch, re_patch):
        sebject = MagicMock(spec=Selenium)
        resp_patch.return_value = 'file not found successfully'
        sebject.response = resp_patch.return_value
        sebject.selenium_jar_version = '3.141.59'
        sebject.selenium_jar_major_version = '3.141'
        sebject.nssm_interactive = 'enable'
        #pdb.set_trace()
        self.assertRaises(Exception, Selenium._Selenium__download_selenium_jar(sebject))
        self.assertRaises(Exception, Selenium._Selenium__create_selenium_script(sebject), 'Unable to create service file')
        self.assertEqual(Selenium._Selenium__delete_service_selenium(sebject), True)

        resp_patch.return_value =  'SERVICE_RUNNING'
        sebject.response = resp_patch.return_value
        self.assertEqual(Selenium._Selenium__check_selenium_status(sebject), True)

if __name__ == '__main__' :
    unittest.main()
