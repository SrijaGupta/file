import unittest
from unittest.mock import Mock

from jnpr.toby.hldcl.unix.unix import UnixHost
import jnpr.toby.security.aamw.traffic_cmd as cmd


class MockShellResponse(object):
    def __init__(self, response):
        self.s = response

    def response(self):
        return self.s


class TestTrafficCommand(unittest.TestCase):

    def setUp(self):
        self.handle = Mock(spec=UnixHost)
        self.handle.log = Mock()

    def test_send_email_traffic(self):
        self.handle.shell = Mock(return_value=MockShellResponse('   '))

        self.handle.shell = Mock(return_value=MockShellResponse(
            'No such file or directory'))
        with self.assertRaises(AssertionError):
            cmd.send_email_traffic(self.handle, self.handle, 'smtp', 'a',
                                   ['a', 'b'], '1.1.1.1')

        self.handle.shell = Mock(return_value=MockShellResponse('abc\ndef'))
        with self.assertRaises(AssertionError):
            cmd.send_email_traffic(self.handle, self.handle, 'bad', 'a',
                                   ['a', 'b'], '1.1.1.1')
        self.assertIsNone(cmd.send_email_traffic(
            self.handle, self.handle, 'smtp', 'a', ['a', 'b'], '1.1.1.1'))
        self.assertIsNone(cmd.send_email_traffic(
            self.handle, self.handle, 'smtps', 'a', ['a', 'b'], '1.1.1.1'))
        self.assertIsNone(cmd.send_email_traffic(
            self.handle, self.handle, 'smtp_tls', 'a', ['a', 'b'], '1.1.1.1'))

    def test_send_web_traffic(self):
        self.handle.shell = Mock()
        self.assertIsNone(cmd.send_web_traffic(self.handle, 'http', 'abc',
                                               'abc'))
        with self.assertRaises(AssertionError):
            cmd.send_web_traffic(self.handle, 'bad', 'abc', 'abc')

        self.handle.shell = Mock(side_effect=Exception('Boom!'))
        self.assertIsNone(cmd.send_web_traffic(self.handle, 'http', 'abc',
                                               'abc'))

    def test_fetch_mail(self):
        self.handle.shell = Mock(return_value=MockShellResponse(
            'OK Fetch completed FETCH (UID 123)'))
        self.assertIsNotNone(cmd.fetch_mail(self.handle, 'imap', 'abc', 'abc',
                                            'abc'))

        self.handle.shell = Mock(return_value=MockShellResponse(
            'FETCH (UID 123)'))
        self.assertIsNotNone(cmd.fetch_mail(self.handle, 'imap', 'abc', 'abc',
                                            'abc'))


if __name__ == '__main__':
    unittest.main()