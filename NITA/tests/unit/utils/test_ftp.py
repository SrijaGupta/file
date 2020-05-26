import sys

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.utils.ftp import FTP

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'


@attr('unit')
class TestFTP(unittest.TestCase):
    @patch('ftplib.FTP.__init__')
    def test_ftp_init(self, ftp_mock):
        fobject = FTP('device')
        self.assertEqual(fobject.host, 'device')
        ftp_mock.assert_called_with(fobject, 'device', None, None, 30)

        fobject = FTP('device', user='user')
        self.assertEqual(fobject.host, 'device')
        self.assertEqual(fobject._ftpargs, {})
        ftp_mock.assert_called_with(fobject, 'device', 'user', None, 30)

        fobject = FTP('device', password='password', test='test')
        self.assertEqual(fobject.host, 'device')
        self.assertEqual(fobject._ftpargs, {'test':'test'})
        ftp_mock.assert_called_with(fobject, 'device', None, 'password', 30)

        fobject = FTP('device', user='user', password='password')
        self.assertEqual(fobject.host, 'device')
        self.assertEqual(fobject._ftpargs, {})
        ftp_mock.assert_called_with(fobject, 'device', 'user', 'password', 30)

    @patch(builtin_string + '.open')
    def test_ftp_put_file(self, open_mock):
        fobject = MagicMock(spec=FTP)
        fobject.storbinary = MagicMock()
        self.assertTrue(FTP.put_file(fobject, local_file='test'))
        fobject.storbinary.assert_called_with('STOR test', open_mock())
        self.assertTrue(FTP.put_file(fobject, local_file='test1', remote_file='test2'))
        fobject.storbinary.assert_called_with('STOR test2', open_mock())
        self.assertTrue(FTP.put_file(fobject, local_file=['test1', 'test2']))
        fobject.storbinary.assert_any_call('STOR test1', open_mock())
        fobject.storbinary.assert_any_call('STOR test2', open_mock())
        self.assertTrue(FTP.put_file(fobject, local_file=('test1', 'test2'), remote_file='test'))
        fobject.storbinary.assert_any_call('STOR test', open_mock())

    @patch('jnpr.toby.utils.ftp.logger.error')
    def test_ftp_put_file_failures(self, mock_logger):
        fobject = MagicMock(spec=FTP)
        fobject.storbinary = MagicMock()
        # When an exception occurs
        self.assertRaises(Exception, FTP.put_file, fobject, local_file='test')
        self.assertTrue(mock_logger.called)

    @patch(builtin_string + '.open')
    def test_ftp_get_file(self, open_mock):
        fobject = MagicMock(spec=FTP)
        fobject.retrbinary = MagicMock()
        self.assertTrue(
            FTP.get_file(fobject, remote_file='test', local_file='test')
        )

    @patch(builtin_string + '.open')
    @patch('jnpr.toby.utils.ftp.logger.error')
    def test_ftp_get_file_failures(self, mock_logger, open_mock):
        fobject = MagicMock(spec=FTP)
        fobject.retrbinary = MagicMock(side_effect=Exception)
        self.assertRaises(
            Exception,
            FTP.get_file, fobject, remote_file='test', local_file='test'
        )
        self.assertTrue(mock_logger.called)

    @patch('ftplib.FTP')
    def test_ftp_context_manager(self, ftp_mock):
        with FTP('dev') as ftp:
            self.assertIsInstance(ftp, FTP)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFTP)
    unittest.TextTestRunner(verbosity=2).run(suite)
