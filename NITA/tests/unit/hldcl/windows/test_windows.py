import sys

import unittest2 as unittest
from mock import patch, MagicMock

from jnpr.toby.hldcl.windows.windows import Windows
#from jnpr.toby.hldcl.system  import *
import os
import re
import time
from select import select

import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.hldcl.connectors.telnetconn import TelnetConn
from jnpr.toby.hldcl.connectors.common import check_socket
from jnpr.toby.hldcl.host import Host
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.connectors.sshconn import SshConn

class Testwindows(unittest.TestCase):
    
    """
    @patch('jnpr.toby.hldcl.windows.windows.TelnetConn',side_effect=[MagicMock(),Exception('error')])
    @patch('jnpr.toby.hldcl.windows.windows.host.Host')
    @patch('jnpr.toby.hldcl.windows.windows.credentials.get_credentials',return_value=list(['test_user','test_pwd']))
    def test_init(self,cred_patch,Telnet_patch):
        # self.assertRaises(Exception,Windows)
        super_obj = MagicMock(spec=Host)
        Windows.__init__(super_obj,host='host')
        #Windows(host='host')
    """
  
    def test_execute(self):
        wobject = MagicMock(spec=Windows)
        wobject.prompt = "$"
        wobject.handle = MagicMock()
        wobject.handle.execute.return_value = True
        self.assertEqual(Windows.execute(wobject,pattern="$",command="show version"),True)
        self.assertRaises(Exception,Windows.execute,wobject,pattern="$")

    def test_shell(self):
        wobject = MagicMock(spec=Windows)
        wobject.prompt = "$"
        wobject.execute.side_effect = [-1,1]
        wobject.response = "test\n"
        self.assertRaises(Exception,Windows.shell,wobject,pattern="$",command="show version")
        self.assertIsInstance(Windows.shell(wobject,pattern="$",command="show version"),Response)
        self.assertRaises(Exception,Windows.shell,wobject,pattern="$")
    
    def test_close(self):
        wobject = MagicMock(spec=Windows)
        wobject.connect_mode = "ssh"
        wobject.handle = MagicMock()
        wobject.handle.client = MagicMock()
        wobject.handle.client.close.return_value=True
        self.assertEqual(Windows.close(wobject),True)
        wobject.connect_mode = "telnet"
        wobject.handle.close.side_effect= Exception('error')
        self.assertRaises(Exception,Windows.close,wobject)

    @patch('jnpr.toby.hldcl.windows.windows.time.sleep')    
    def test_reboot(self,sleep_patch):
        wobject = MagicMock(spec=Windows)
        wobject.host = ''
        wobject.connect_mode = 'ssh'
        wobject.handle = MagicMock()
        wobject.reconnect = MagicMock()
        wobject.handle.close.return_value = True
        wobject.execute.side_effect = [-1,1,1,1]
        self.assertRaises(Exception,Windows.reboot,wobject)
        with patch('jnpr.toby.hldcl.windows.windows.check_socket',side_effect=[False,True,False,True,True]) as socket_patch:
            self.assertRaises(Exception,Windows.reboot,wobject)
            self.assertRaises(Exception,Windows.reboot,wobject)
            self.assertTrue(Windows.reboot(wobject))
    
    @patch('jnpr.toby.hldcl.windows.windows.time.sleep')  
    @patch('jnpr.toby.hldcl.windows.windows.SshConn') 
    @patch('jnpr.toby.hldcl.windows.windows.TelnetConn')
    def test_reconnect(self,telnet_patch,sshconn_patch,sleep_patch):
        wobject = MagicMock(spec=Windows)
        wobject.prompt = '>'
        wobject.host = 'host'
        wobject.connect_mode = 'ssh'
        wobject.user = "test"
        wobject.password= "test"
        wobject.port = 23
        wobject.handle = MagicMock()
        wobject.handle.client.get_transport.isAlive.side_effect = [False,True]
        wobject.handle.close.return_value = True
        with patch('jnpr.toby.hldcl.windows.windows.check_socket',side_effect=[True,False,True,True]) as socket_patch:
            self.assertTrue(Windows.reconnect(wobject))
            self.assertRaises(Exception,Windows.reconnect,wobject)
            self.assertTrue(Windows.reconnect(wobject))      
            wobject.connect_mode = 'telnet'
            self.assertTrue(Windows.reconnect(wobject))
    

if __name__ == '__main__' :
    unittest.main()
