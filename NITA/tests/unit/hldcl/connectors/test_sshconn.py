import unittest2 as unittest
from jnpr.toby.hldcl.connectors.sshconn import SshConn
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.host import Host
from nose.plugins.attrib import attr

class Shellmock(object):
    @staticmethod
    def recv(self, *args, **kwargs):
        return b'FreeBSD $'

class Shellmock1:
    def __init__(self):
        self.var = 0
    def recv(self, *args, **kwargs):
        self.var +=1
        if self.var == 2:
            return b'FreeBSD $'
        return b'FreeBSD '
    def send(self, *args, **kwargs):
        pass

class Shellmock2(object):
    @staticmethod
    def recv(self, *args, **kwargs):
        return b'> FreeBSD $'
    def send(self, *args, **kwargs):
        pass

class Shellmock4(object):
    @staticmethod
    def recv(self, *args, **kwargs):
        return b' \xC4abc $'
    def send(self, *args, **kwargs):
        pass

class Shellmock5(object):
    @staticmethod
    def recv(self, *args, **kwargs):
        return b'> \xC4abc $'
    def send(self, *args, **kwargs):
        pass

@attr('unit')
class TestJunosModule(unittest.TestCase):
   
    maxDiff = None
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.set_missing_host_key_policy')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.get_transport')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.connect')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.invoke_shell', return_value=Shellmock())
    @patch('jnpr.toby.hldcl.connectors.sshconn.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    def test_sshconn(self, sleep_patch, patch1, patch2, patch3, patch4, patch5):
        handle = SshConn(host='dummy', user='regress', password='MaRtInI')
        self.assertIsInstance(handle, SshConn)

        handle = SshConn(host='dummy', user='regress', password='MaRtInI',port='555')
        self.assertIsInstance(handle, SshConn)

    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.set_missing_host_key_policy')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.get_transport')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.connect')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.invoke_shell', return_value=Shellmock2())
    @patch('jnpr.toby.hldcl.connectors.sshconn.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    def test_sshconn2(self, sleep_patch, patch1, patch2, patch3, patch4, patch5):
        handle = SshConn(host='dummy', user='regress', password='MaRtInI')
        self.assertIsInstance(handle, SshConn)
        handle = SshConn(host='dummy', user='regress', password='MaRtInI', ssh_key_file = "file")
        self.assertIsInstance(handle, SshConn)
        handle = SshConn(host='dummy', user='regress', password='MaRtInI', ssh_key_file = "file",port="22")
        self.assertIsInstance(handle, SshConn)
        with patch('jnpr.toby.hldcl.connectors.sshconn.select',side_effect = [(0,'',''),(1,'',''),(1,'','')]) as select_patch:
            patch2.return_value = Shellmock1()
            handle = SshConn(host='dummy', user='regress', password='MaRtInI', ssh_key_file = "file",port="22")
            self.assertIsInstance(handle,SshConn)


    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.set_missing_host_key_policy', side_effect=Exception)
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.get_transport', side_effect=Exception)
    @patch('logging.error')
    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    def test_sshconn_exception(self, sleep_patch, patch1, patch2, patch3):
        self.assertRaises(Exception, lambda: SshConn(host='dummy', user='regress', password='MaRtInI'))
    
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.set_missing_host_key_policy')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.get_transport')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.connect')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.invoke_shell', return_value=Shellmock4())
    @patch('jnpr.toby.hldcl.connectors.sshconn.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    def test_sshconn4(self, sleep_patch, patch1, patch2, patch3, patch4, patch5):
        handle = SshConn(host='dummy', user='regress', password='MaRtInI')
        self.assertIsInstance(handle, SshConn)

        handle = SshConn(host='dummy', user='regress', password='MaRtInI',port='555')
        self.assertIsInstance(handle, SshConn)

    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.set_missing_host_key_policy')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.get_transport')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.connect')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.invoke_shell', return_value=Shellmock5())
    @patch('jnpr.toby.hldcl.connectors.sshconn.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    def test_sshconn5(self, sleep_patch, patch1, patch2, patch3, patch4, patch5):
        handle = SshConn(host='dummy', user='regress', password='MaRtInI')
        self.assertIsInstance(handle, SshConn)

        handle = SshConn(host='dummy', user='regress', password='MaRtInI',port='555')
        self.assertIsInstance(handle, SshConn)

    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    def test_sshconn_execute(self, sleep_patch):
        sobject = MagicMock(spec=SshConn)
        sobject.client = MagicMock()
        dhandle = MagicMock()
        self.assertEqual(SshConn.execute(sobject, cmd="show version", pattern="os",\
                         device=dhandle, no_response='no_response'), 1)
        delattr(dhandle, "shelltype")
        sobject.wait_for.return_value = (False, "test")
        #self.assertRaises(SshConn.execute(sobject, cmd="show version", pattern=["os"],\
        #                 device=dhandle), -1)
        sobject.wait_for.return_value = (True, "test")
        self.assertEqual(SshConn.execute(sobject, cmd="show version", pattern="String",\
                         device=dhandle), 1)

        sobject.wait_for.side_effect = [ (True, "---(more)---"), (True, "test") ]
        self.assertEqual(SshConn.execute(sobject, cmd="show version", pattern=["os"],\
                         device=dhandle), 1)
        
        sobject.wait_for.side_effect = [ (True, "---(more)---"), (True, "test") ]
        
        self.assertEqual(SshConn.execute(sobject, cmd="show version", pattern="String",\
                         device=dhandle, raw_output=True), 1)

        sobject.wait_for.side_effect = [ (True, """test
        abc"""), (True, """test
        abc""") ]
        self.assertEqual(SshConn.execute(sobject, cmd="show version", pattern="String",\
                         device=dhandle, raw_output=False), 1)

    @patch('jnpr.toby.hldcl.connectors.sshconn.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    def test_sshconn_waitfor1(self, patch1, patch2):
        sshhandle = MagicMock(spec=SshConn)
        sshhandle.client = MagicMock()
        sshhandle.client.recv = MagicMock()
        sshhandle.client.recv.return_value = b'FreeBSD $'
        self.assertEqual(SshConn.wait_for(sshhandle, expected=['$', '#'], shell='sh'), (True, 'FreeBSD $'))
        self.assertEqual(SshConn.wait_for(sshhandle, shell='csh'), (True, 'FreeBSD $'))
        with patch('jnpr.toby.hldcl.connectors.sshconn.select',side_effect = [(0,'',''),(1,'',''),(1,'','')]) as select_patch:
            patch2.return_value = Shellmock1()
            self.assertEqual(SshConn.wait_for(sshhandle, shell='csh'), (True, 'FreeBSD $'))

    @patch('jnpr.toby.hldcl.connectors.sshconn.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    def test_sshconn_waitfor2(self, patch1, patch2):
        sshhandle = MagicMock(spec=SshConn)
        sshhandle.client = MagicMock()
        sshhandle.client.recv = MagicMock()
        sshhandle.client.recv.return_value = b' '
        self.assertEqual(SshConn.wait_for(sshhandle, expected=['ab', 'c'],
                                          timeout=0,
                                          shell='csh'), (False, ' '))

    @patch('jnpr.toby.hldcl.connectors.sshconn.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    @patch('jnpr.toby.hldcl.connectors.sshconn.re.search')
    def test_sshconn_waitfor3(self, search_patch, patch1, patch2):
        sshhandle = MagicMock(spec=SshConn)
        sshhandle.client = MagicMock()
        data_obj = MagicMock()
        decode_obj = MagicMock()
        data_obj.decode.return_value = decode_obj
        sshhandle.client.recv = data_obj
        data_obj.decode = MagicMock(return_value='Test')
        self.assertNotEqual(SshConn.wait_for(sshhandle, expected=['ab', 'c'],
                                          timeout=1,
                                          shell='csh'), (True, decode_obj))

    @patch('jnpr.toby.hldcl.connectors.sshconn.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.connectors.sshconn.time.sleep')
    def test_sshconn_waitfor4(self, patch1, patch2):
        sshhandle = MagicMock(spec=SshConn)
        sshhandle.client = MagicMock()
        sshhandle.client.recv = MagicMock()
        sshhandle.client.recv.return_value = b'\xC4abc'
        self.assertEqual(SshConn.wait_for(sshhandle, expected=['ab', 'c'],
                                          timeout=True,
                                          shell='csh'), (True, 'Äabc'))
if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestJunosModule)
    unittest.TextTestRunner(verbosity=2).run(SUITE) 
