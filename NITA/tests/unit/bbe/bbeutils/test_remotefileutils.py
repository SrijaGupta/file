import unittest
from mock import patch, MagicMock
from jnpr.toby.bbe.bbeutils.remotefileutils import *


class TestRemoteFileUtils(unittest.TestCase):
    """
    TestRemoteFileUtils class to handle remotefileutils.py unit tests
    """
    @patch('jnpr.toby.bbe.bbeutils.remotefileutils.SshConn')
    def test_clobber_remote_file(self, patch_sshconn):

        self.assertEqual(clobber_remote_file('hercules.englab.juniper.net', 'test',
                                             '/usr/local/etc/raddb/sample.txt'), True)

    @patch('jnpr.toby.bbe.bbeutils.remotefileutils.SshConn')
    def test_append_remote_file(self, patch_sshconn):
        self.assertEqual(append_remote_file('hercules.englab.juniper.net', 'test',
                                            '/usr/local/etc/raddb/sample.txt'), True)

    @patch('jnpr.toby.bbe.bbeutils.remotefileutils.SshConn')
    def test_prepend_remote_file(self, patch_sshconn):
        self.assertEqual(prepend_remote_file('hercules.englab.juniper.net', 'test',
                                             '/usr/local/etc/raddb/sample.txt'), True)

    @patch('jnpr.toby.bbe.bbeutils.remotefileutils.SshConn')
    def test_read_remote_file_to_string(self, patch_sshconn):
        self.assertIsInstance(read_remote_file_to_string('hercules.englab.juniper.net',
                                                         '/usr/local/etc/raddb/sample.txt'), object)

if __name__ == '__main__':
    unittest.main()