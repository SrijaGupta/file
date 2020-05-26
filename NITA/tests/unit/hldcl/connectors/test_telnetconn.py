"""UT for the module jnpr.toby.hldcl.connectors.telnetconn"""

import unittest2 as unittest
from mock import patch, MagicMock
import sys
from jnpr.toby.hldcl.connectors.telnetconn import TelnetConn
#from telnetconn import TelnetConn

class TestTelnetConn(unittest.TestCase):
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    """UT for TelnetConn"""
    @patch('jnpr.toby.hldcl.connectors.telnetconn.Telnet.__del__')
    @patch('jnpr.toby.hldcl.connectors.telnetconn.logging')
    @patch('jnpr.toby.hldcl.connectors.telnetconn.Telnet.write')
    @patch('jnpr.toby.hldcl.connectors.telnetconn.Telnet.expect')
    @patch('jnpr.toby.hldcl.connectors.telnetconn.Telnet.__init__')
    @patch('jnpr.toby.hldcl.connectors.telnetconn.time.sleep')
    def test_telnetconn_init(self, time_patch, telnet_init_patch, expect_patch, write_patch, logging_patch, del_patch):
        """Test '__init__' method of class TelnetConn"""

        expect_patch.side_effect = [[2, 0, b'test'], [2, 0, b'test'], [0, 0, b'test'], [2, 0, b'test'], [2, 0, b'test'], [-1, 0, b'test']]
        self.assertIsInstance(TelnetConn(host='192.168.0.1', user='test', password='test'), TelnetConn)
        telnet_init_patch.assert_called_with(host='192.168.0.1')
        self.assertEqual(write_patch.call_count, 4)

        expect_patch.side_effect = [[2, 0, b'test'], [2, 0, b'test'], [0, 0, b'test'], [2, 0, b'test'], [2, 0, b'test'], [-1, 0, b'test']]
        self.assertIsInstance(TelnetConn(host='192.168.0.1', user='test', password='test', port=23), TelnetConn)
        telnet_init_patch.assert_called_with(host='192.168.0.1', port=23)
        self.assertEqual(write_patch.call_count,8)

        expect_patch.side_effect = [[2, 0, b'test'], [2, 0, b'test'], [0, 0, b'test'], [2, 0, b'test'], [2, 0, b'test'], [-1, 0, b'test']]
        self.assertIsInstance(TelnetConn(host='192.168.0.1', user='test', password='test', port=23), TelnetConn)
        telnet_init_patch.assert_called_with(host='192.168.0.1', port=23)
        self.assertEqual(write_patch.call_count,12)

        expect_patch.side_effect = [[2, 0, b'test'], [2, 0, b'test'], [0, 0, b'test'], [2, 0, b'test'], [2, 0, b'test'], [-1, 0, b'test']]
        self.assertIsInstance(TelnetConn(host='192.168.0.1', user='test', password='test', port=23), TelnetConn)
        telnet_init_patch.assert_called_with(host='192.168.0.1', port=23)
        self.assertEqual(write_patch.call_count, 16)

        expect_patch.side_effect = [[-1, 0, b'test'], [2, 0, b'test'], [2, 0, b'test'], [2, 0, b'test'], [-1, 0, b'test']]
        self.assertRaises(Exception, TelnetConn, host='192.168.0.1', user='test', password='test', port=23)
        telnet_init_patch.assert_called_with(host='192.168.0.1', port=23)
        self.assertEqual(write_patch.call_count,17)

        expect_patch.side_effect = [[2, 0, b'test'], [-1, 0, b'temp'], [2, 0, b'test'], [2, 0, b'test'], [-1, 0, b'test']]
        self.assertRaises(Exception, TelnetConn, host='192.168.0.1', user='user', password='test', port=23)
        telnet_init_patch.assert_called_with(host='192.168.0.1', port=23)
        self.assertEqual(write_patch.call_count, 19)
        logging_patch.error.assert_called_with("Expected 'login' or 'shell/config/cli prompt' from 192.168.0.1, but instead got:\r\n'temp'")

        expect_patch.side_effect = [[2, 0, b'test'], [2, 0, b'test'], [-1, 0, b'temp'], [2, 0, b'test'], [-1, 0, b'test']]
        self.assertRaises(Exception, TelnetConn, host='192.168.0.1', user='user', password='pwd', port=23)
        telnet_init_patch.assert_called_with(host='192.168.0.1', port=23)
        self.assertEqual(write_patch.call_count, 21)
        logging_patch.error.assert_called_with("Expected 'login' from 192.168.0.1, but instead got:\r\n'temp'")

        expect_patch.side_effect = [[2, 0, b'test'], [2, 0, b'test'], [0, 0, b'test'], [2, 0, b'test'], [2, 0, b'test'], [0, 0, b'test']]
        self.assertIsInstance(TelnetConn(host='192.168.0.1', user='test', password='test', port=23), TelnetConn)
        telnet_init_patch.assert_called_with(host='192.168.0.1', port=23)
        self.assertEqual(write_patch.call_count,25)

        #del expect_patch.side_effect 
        expect_patch.side_effect = [[1, 0, b'test'], [0, 0, b'test'], [-1,0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        #del expect_patch.side_effect
        expect_patch.side_effect = [[1, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[0, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[0, 0, b'test'], [0, 0, b'test'],[-1,0,b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[2, 0, b'test'], [1, 0, b'test'],[1,0,b'test'],[0,0,b'test'],[3,0,b'test'],[3,0,b'test'],[1,0,b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[1, 0, b'test'], [1, 0, b'test'],[1,0,b'test'],[3,0,b'test'],[3,0,b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass
 
        expect_patch.side_effect = [[5, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[5, 0, b'test'], [1, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[4, 0, b'test'], [2, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[5, 0, b'test'], [0, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[3, 0, b'test'], [0, 0, b'test'], [2, 0, b'test'], \
                                   [0, 0, b'test'], [4, 0, b'test'], [0, 0, b'test'], [0, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[4, 0, b'test'], [2, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23, console=True)
        except :
            pass

        expect_patch.side_effect = [[1, 0, b'test'], [0, 0, b'test'], [0, 0, b'test'], [0, 0, b'test'], \
                                   [0, 0, b'test'], [3, 0, b'test'], [3, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[1, 0, b'test'], [0, 0, b'test'], [0, 0, b'test'], [0, 0, b'test'], \
                                   [0, 0, b'test'], [0, 0, b'test'], [3, 0, b'test'], [3, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[1, 0, b'test'], [0, 0, b'test'], [0, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[1, 0, b'test'], [-1, 0, b'test'], [0, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[1, 0, b'test'], [-1, 0, b'test'], [0, 0, b'test'], [0, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[1, 0, b'test'], [-1, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[1, 0, b'test'], [-1, 0, b'test'], [1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23)
        except :
            pass

        expect_patch.side_effect = [[1, 0, b'test'], [-1, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23, kill_sessions='no')
        except :
            pass

        expect_patch.side_effect = [[0, 0, b'test'], [4, 0, b'test'], [3, 0, b'test']]
        try :
            TelnetConn(host='192.168.0.1', user='test', password='test', port=23, kill_sessions='no')
        except :
            pass

    @patch('jnpr.toby.hldcl.connectors.telnetconn.time.sleep')
    def test_telnetconn_execute(self, sleep_patch):
        """Test 'execute' method of class TelnetConn"""
        tobject = MagicMock(spec=TelnetConn)
        dev_obj = MagicMock()

        tobject.expect.side_effect = [[-1, 0, b'test']]
        #self.assertEqual(TelnetConn.execute(tobject, cmd="show version", pattern="junos", device=dev_obj), -1)

        tobject.expect.side_effect = [[-1, 0, b'test']]
        #self.assertEqual(TelnetConn.execute(tobject, cmd="\x03", pattern=["junos"], device=dev_obj), -1)
        
        tobject.expect.side_effect = [[-1, 0, b'test']]
        self.assertEqual(TelnetConn.execute(tobject, cmd="show version", pattern="junos", device=dev_obj, no_response=1), 1)
        
        dev_obj.response = "test"
        tobject.expect.side_effect = [[0, 0, b'version'], [1, 0, b'test2']]
        self.assertEqual(TelnetConn.execute(tobject, cmd="\x03", pattern="junos", device=dev_obj, raw_output=True), 0)
        self.assertEqual(dev_obj.response, 'test')
 

        tobject.expect.side_effect = [[1, 0, b'test1'], [0, 0, b'test2']]
        self.assertEqual(TelnetConn.execute(tobject, cmd="show version", pattern="junos", device=dev_obj), 0)
        self.assertEqual(dev_obj.response, 'test1test2')

        dev_obj.prompt = "$"
        tobject.expect.side_effect = [[0, 0, b'test2'], [0, 0, b'show version']]
        self.assertEqual(TelnetConn.execute(tobject, cmd="show version", pattern="junos", device=dev_obj), 0)
        self.assertEqual(dev_obj.response, 'test2')

        tobject.expect.side_effect = [[0, 0, b'version'], [1, 0, b'test2']]
        self.assertEqual(TelnetConn.execute(tobject, cmd="show version", pattern="junos", device=dev_obj), 0)
        self.assertEqual(dev_obj.response, 'version')

        dev_obj.response = "test"
        tobject.expect.side_effect = [[0, 0, b'version'], [1, 0, b'test2']]
        self.assertEqual(TelnetConn.execute(tobject, cmd="\x03", pattern="junos", device=dev_obj), 0)
        self.assertEqual(dev_obj.response, 'test')

        output = "test1".encode('utf-8')
        output2 = "test2".encode('utf-8')
        tobject.expect.side_effect = [[1, 0, output], [0, 0, output2]]
        self.assertEqual(TelnetConn.execute(tobject, cmd="test", pattern="junos", device=dev_obj), 0)

        output = "test1".encode('utf-8')
        tobject.expect.side_effect = [[0, 0, output]]
        self.assertEqual(TelnetConn.execute(tobject, cmd="test", pattern="junos", device=dev_obj), 0)

        output = "test1".encode('utf-8')
        tobject.expect.side_effect = [[0, 0, output]]
        self.assertEqual(TelnetConn.execute(tobject, cmd="test", pattern="junos", device=dev_obj, raw_output=True), 0)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestTelnetConn)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
