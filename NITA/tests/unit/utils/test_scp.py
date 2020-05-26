import sys

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.utils.scp import SCP

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'


class TestSCP(unittest.TestCase):
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('jnpr.toby.utils.scp.inspect')
    @patch('jnpr.toby.utils.scp.SCPClient.__init__')
    @patch('paramiko.SSHClient')
    def test_scp_init(self, sshclient_patch, scpclient_patch, inspect_patch):
        self.assertIsInstance(SCP('device', progress=True), SCP)
        # callable progress
        sobject = SCP('device', progress=SCP.open)
        self.assertEqual(sobject.host, "device")
        self.assertEqual(sobject.user, None)
        self.assertEqual(sobject.password, None)
        self.assertTrue(scpclient_patch.called)

        obj = MagicMock()
        inspect_patch.getargspec.return_value = obj
        obj.args = [1, 2, 3]
        sobject = SCP('device', user="regress", password="MaRtInI", progress=SCP.open)
        self.assertEqual(sobject.host, "device")
        self.assertEqual(sobject.user, "regress")
        self.assertEqual(sobject.password, "MaRtInI")
        self.assertTrue(scpclient_patch.called)
        sobject = MagicMock(spec=SCP)
        sobject._progress = True
        SCP('device', progress=SCP.open)
        
        obj.args = [1, 2]
        sobject = SCP('device', user="regress", password="MaRtInI", progress=SCP.open)
        obj.args = [1]
        sobject = SCP('device', user="regress", password="MaRtInI", progress=SCP.open)

    def test_scp_get_file(self):
        sobject = MagicMock(spec=SCP)
        sobject.proxy = True
        sobject._ssh = MagicMock()
        sobject._ssh.get.return_value = None
        self.assertTrue(
            SCP.get_file(sobject, remote_file='test', local_file='test')
        )

    def test_scp_get_file_failures(self):
        sobject = MagicMock(spec=SCP)
        sobject.get = MagicMock(side_effect=Exception)
        self.assertRaises(
            Exception,
            SCP.get_file, sobject, remote_file='test', local_file='test'
        )

    def test_scp_put_file(self):
        sobject = MagicMock(spec=SCP)
        sobject._ssh = MagicMock()
        sobject._ssh.put.return_value = None
        sobject.proxy = True
        self.assertTrue(
            SCP.put_file(sobject, local_file='test')
        )

        self.assertTrue(
            SCP.put_file(sobject, local_file=['test'], remote_file='test')
        )

    def test_scp_put_file_failures(self):
        sobject = MagicMock(spec=SCP)
        sobject.put = MagicMock(side_effect=Exception)
        self.assertRaises(
            Exception,
            SCP.put_file, sobject, local_file='test')

    def test_scp_scp_progress(self):
        sobject = MagicMock(spec=SCP)
        sobject._by10pct = MagicMock(return_value=False)
        self.assertEqual(SCP._scp_progress(sobject, _path='test', _total=100, _xfrd=50), None)

        self.assertEqual(SCP._scp_progress(sobject, _path='test', _total=100, _xfrd=51), None)

    def test_scp_progress_local(self):
        sobject = MagicMock(spec=SCP)
        sobject.host = MagicMock(return_value='test')
        self.assertEqual(SCP._progress_local(sobject, 100), None)

    @patch('scp.SCPClient')
    @patch('paramiko.SSHClient')
    def test_scp_context_manager(self, scpclient_mock, sshclinet_mock):
        with SCP('dev') as scp:
            self.assertIsInstance(scp, SCP)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestSCP)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
