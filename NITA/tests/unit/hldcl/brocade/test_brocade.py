import os
import unittest
import logging
from mock import MagicMock
from mock import patch
import builtins
from time import sleep
from jnpr.toby.hldcl.brocade.brocade import Brocade 
from jnpr.toby.utils.response import Response


class TestBrocadeModule(unittest.TestCase):
    
    def test_connect(self):
        from jnpr.toby.hldcl.brocade.brocade import Brocade
        device = MagicMock(spec=Brocade)
        device.host = 'test'
        device._connect = MagicMock(return_value=True)
        device.enable = MagicMock(return_value=True)
        device.log = MagicMock()
        device.execute = MagicMock(return_value='')
        Brocade.connect(device)
        device.execute = MagicMock(return_value='error')
        Brocade.connect(device)

    @patch('telnetlib.Telnet.close')
    @patch('jnpr.toby.hldcl.connectors.telnetconn.TelnetConn.__init__')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.__init__')
    def test_connect_(self, patch_sshconn, patch_TelnetConn, patch_telnetlib):
        from jnpr.toby.hldcl.connectors.telnetconn import TelnetConn
        from jnpr.toby.hldcl.connectors.sshconn import SshConn
        from jnpr.toby.hldcl.brocade.brocade import Brocade
        device = MagicMock(spec=Brocade)
        device.log = MagicMock()
        ######################################################################
        logging.info("Test case 1: Connect to device by console")
        device._kwargs = {}
        device.host = 'test'
        device._kwargs['connect_mode'] = 'console'
        device.log = MagicMock()
        result = Brocade._connect(device)
        self.assertEqual(result, None)
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 2: Connect to device with Unknown connection mode")
        device._kwargs = {}
        device.host = 'test'
        device._kwargs['connect_mode'] = 'abc'
        device.log = MagicMock()
        result = Brocade._connect(device)
        self.assertEqual(result, None)
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 3: Connect to device by ssh")
        device._kwargs = {}
        device.host = 'test'
        device.user = None
        device.password = None
        device._kwargs['connect_mode'] = 'ssh'
        device._kwargs['console'] = False
        device.log = MagicMock()
        patch_sshconn.return_value = None
        result = Brocade._connect(device)
        self.assertIsInstance(result, SshConn)
        logging.info("\tPassed")

    def test_execute(self):
        from jnpr.toby.hldcl.brocade.brocade import Brocade 
        device = MagicMock(spec=Brocade)
        device.log = MagicMock()
        ######################################################################
        logging.info("Test case 1: execute command successfully")
        device.prompt = '>'
        device.channel = MagicMock()
        device.channel.execute = MagicMock(return_value='abc')
        device.response = 'abc'
        result = Brocade.execute(device, command='interface f0/0')
        self.assertEqual(result, 'abc', 'Should be a response')
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 2: execute command unsuccessfully")
        device.channel = MagicMock()
        device.channel.execute = MagicMock(return_value=-1)
        with self.assertRaises(Exception) as context:
            result = Brocade.execute(device, command='interface f0/0', pattern='>')
        self.assertRaises(Exception, result)
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 3: execute without command")
        device.channel = MagicMock()
        result = Brocade.execute(device, pattern='>')
        self.assertEqual(result, 'abc', 'Should be False')
        logging.info("\tPassed")

    def test_close(self):
        device = MagicMock(spec=Brocade)
        device.log = MagicMock()
        device.channel = MagicMock()
        ###################################################################
        logging.info("Test case 1:with close success ")
        device.connected = True
        device.channel.close = MagicMock(return_value=True)
        result = Brocade.close(device)
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ################################################################
        logging.info("Test case 2:with close fail ")
        device.channel = MagicMock()
        device.channel.close = MagicMock(side_effect=Exception('Error'))
        result = Brocade.close(device)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")
        #######################################################################
        logging.info("Test case 3:with close success")
        device.connected = False
        device.channel.close = MagicMock(return_value=True)
        result = Brocade.close(device)
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ################################################################


if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name + ".log", level=logging.INFO)
    unittest.main()
