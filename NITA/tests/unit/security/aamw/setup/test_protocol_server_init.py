import copy
import unittest
from unittest.mock import Mock

from jnpr.toby.hldcl.unix.unix import UnixHost
import jnpr.toby.security.aamw.setup.protocol_server_init as protocol_init
import jnpr.toby.security.aamw.util.mail_util as mail_util


class MockResponse(object):
    def __init__(self, response):
        self.s = response

    def response(self):
        return self.s


class TestProtocolInit(unittest.TestCase):
    def setUp(self):
        self.handle = Mock(spec=UnixHost)
        self.handle.log = Mock()
        self.handle.download = Mock()
        self.handle.su = Mock()
        self.handle.upload = Mock()

    def test_init_http_server(self):
        self.handle.shell = Mock(return_value=MockResponse(''))
        self.assertIsNone(protocol_init.init_http_server(self.handle))

        self.handle.shell = Mock(return_value=MockResponse('Listen'))
        self.assertIsNone(protocol_init.init_http_server(self.handle))

    def test_init_email_server(self):
        self.handle.shell = Mock(return_value=MockResponse(''))

        orig_init_smtp_server_with_arg = protocol_init. \
            _init_smtp_server_with_arg

        protocol_init._init_smtp_server_with_arg = Mock(return_value=None)

        func_list = [
            protocol_init.init_smtp_server,
            protocol_init.init_smtps_server,
            protocol_init.init_smtp_tls_server,
            protocol_init.init_imap_server,
            protocol_init.init_imap_tls_server,
        ]

        try:
            for func in func_list:
                self.assertIsNone(func(self.handle,add_usr=False))
        finally:
            protocol_init._init_smtp_server_with_arg = \
                orig_init_smtp_server_with_arg

    def test_init_smtp_server_with_arg(self):
        self.handle.shell = Mock(return_value=MockResponse(''))

        orig_mail_server_action = mail_util.mail_server_action
        orig_add_mail_users = mail_util.add_mail_users

        mail_util.mail_server_action = Mock()
        mail_util.add_mail_users = Mock()

        try:
            self.assertIsNone(protocol_init._init_smtp_server_with_arg(
                self.handle, 'smtps', {'abc':'abc'}))
            self.assertIsNone(protocol_init._init_smtp_server_with_arg(
                self.handle, 'smtps', None))
        finally:
            mail_util.mail_server_action = orig_mail_server_action
            mail_util.add_mail_users = orig_add_mail_users


if __name__ == '__main__':
    unittest.main()
