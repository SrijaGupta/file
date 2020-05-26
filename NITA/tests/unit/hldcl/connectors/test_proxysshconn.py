"""
    UT for proxysshconn.py
"""
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.hldcl.connectors.proxysshconn import Proxysshconn

class TestProxysshconn(unittest.TestCase):
    @patch('jnpr.toby.hldcl.connectors.proxysshconn.select')
    @patch('jnpr.toby.hldcl.connectors.proxysshconn.paramiko')
    def test_proxysshconn_init(self, paramiko_patch, select_patch):
        paramiko_patch.Transport.return_value.open_session.return_value.recv.return_value = b'> '
        select_patch.return_value = [1, 2, 3]
        pobject = Proxysshconn()
        self.assertEqual(pobject.proxy_connection, True)
        self.assertEqual(pobject.dest_connection, True)

        del select_patch.return_value
        select_patch.side_effect = [[0,None,None],[1,None,None]]
        Proxysshconn()
        del select_patch.side_effect
        
        paramiko_patch.Transport.return_value.open_session.return_value.recv.side_effect = [b'< ', b'> ']
        select_patch.side_effect = [[1, 2, 3], [1, 2, 3]]
        self.assertRaises(Exception, Proxysshconn)

        # Exception
        paramiko_patch.Transport.return_value.auth_password.return_value = ['test']
        self.assertRaises(Exception, Proxysshconn, proxy_host="10.10.10.1", proxy_user="puser",\
                          proxy_password="ppwd", proxy_port=22, host="192.168.0.1", user="user",\
                          password="pwd", port=22)

        # Exception
        paramiko_patch.Transport.return_value.auth_password.side_effect = [[], ['test']]
        self.assertRaises(Exception, Proxysshconn, proxy_host="10.10.10.1", proxy_user="puser",\
                          proxy_password="ppwd", proxy_port=22, host="192.168.0.1", user="user",\
                          password="pwd", port=22)

        paramiko_patch.Transport.return_value.auth_password.side_effect = [[], []]
        paramiko_patch.Transport.return_value.open_session.return_value.recv.side_effect = [ b'test'\
                       , b'>' ]
        select_patch.return_value = [1, 2, 3]
        self.assertRaises(Exception, Proxysshconn)

        # Exception
        paramiko_patch.Transport.return_value.auth_password.side_effect = [[], []]
        paramiko_patch.Transport.return_value.open_session.return_value.invoke_shell.side_effect =\
                       Exception
        self.assertRaises(Exception, Proxysshconn, proxy_host="10.10.10.1", proxy_user="puser",\
                          proxy_password="ppwd", host="192.168.0.1", user="user", password="pwd",
                          proxy_ssh_key='abc.txt')

    def test_proxysshconn_close(self):
        pobject = MagicMock()
        self.assertTrue(Proxysshconn.close(pobject))

        # Exception
        pobject.tunnel.close.side_effect = Exception
        self.assertRaises(Exception, Proxysshconn.close, pobject)

    def test_proxysshconn_execute(self):
        pobject = MagicMock(spec=Proxysshconn)
        pobject.handle = MagicMock()
        dhandle = MagicMock()
        self.assertEqual(Proxysshconn.execute(pobject, cmd="show version", pattern="os",\
                         device=dhandle, no_response='no_response'), 1)
        delattr(dhandle, "shelltype") 
        pobject.time = MagicMock()
        pobject.wait_for.return_value = (False, "test")
        self.assertEqual(Proxysshconn.execute(pobject, cmd="show version", pattern=["os"],\
                         device=dhandle), -1)
        pobject.wait_for.return_value = (True, "test")
        self.assertEqual(Proxysshconn.execute(pobject, cmd="show version", pattern="String",\
                         device=dhandle), 1)

        pobject.wait_for.side_effect = [ (True, "---(more)---"), (True, "test") ]
        self.assertEqual(Proxysshconn.execute(pobject, cmd="show version", pattern=["os"],\
                         device=dhandle), 1)

        pobject.wait_for.side_effect = [ (True, "---(more)---"), (True, "test") ]
        self.assertEqual(Proxysshconn.execute(pobject, cmd="show version", pattern=["os"],\
                         device=dhandle, raw_output=True), 1)

    @patch('jnpr.toby.hldcl.connectors.proxysshconn.select')
    def test_proxysshconn_wait_for(self, select_patch):
        pobject = MagicMock(spec=Proxysshconn)
        pobject.handle = MagicMock()
        pobject.handle.recv.return_value = b'test'
        select_patch.return_value = [ 0, 2, 3 ]
        pobject.time = MagicMock()
        pobject.time.side_effect = [ 10, 80 ]
        self.assertEqual(Proxysshconn.wait_for(pobject, shell='csh', timeout=1), (False, ''))

        pobject.time.side_effect = [ 10, 80 ]
        pobject.handle.recv.return_value = b'test'
        select_patch.return_value = [ 1, 2, 3 ]
        self.assertEqual(Proxysshconn.wait_for(pobject, expected=['test'], shell='csh'),\
                         (True, 'test'))

        pobject.time.side_effect = [ 10, 20, 10, 20 ]
        pobject.handle.recv.side_effect = [ b'temp', b'test' ]
        self.assertEqual(Proxysshconn.wait_for(pobject, expected=['test1', 'test'], shell='sh'),\
                        (True, 'temptest'))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProxysshconn)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()

