import unittest
from unittest.mock import Mock

from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.aamw.util import mail_util


class MockNode(object):
    def __init__(self, model):
        class Foo(object):
            pass
        self.model = model
        self.current_controller = Foo()
        self.current_controller.get_model = lambda: self.model


class MockResponse(object):
    def __init__(self, response):
        self.s = response

    def response(self):
        return self.s


class TestMailUtil(unittest.TestCase):
    def setUp(self):
        self.handle = Mock(spec=UnixHost)
        self.handle.log = Mock()
        self.handle.download = Mock()
        self.handle.su = Mock()

    def test_mail_server_action(self):
        self.handle.shell = Mock()
        self.assertIsNone(mail_util.mail_server_action(
            self.handle, mail_util.MailServerAct.STOP))
        self.assertIsNone(mail_util.mail_server_action(
            self.handle, mail_util.MailServerAct.START))
        self.assertIsNone(mail_util.mail_server_action(
            self.handle, mail_util.MailServerAct.RESTART))

        with self.assertRaises(AssertionError):
            self.assertIsNone(mail_util.mail_server_action(self.handle, 123))

    def test_add_mail_users(self):
        self.handle.shell = Mock(return_value=MockResponse(''))
        self.assertIsNone(mail_util.add_mail_users(self.handle,
                                                   {'abc': 'abc'}))

    def test_del_mail_users(self):
        self.handle.shell = Mock(return_value=MockResponse(''))
        self.assertIsNone(mail_util.del_mail_users(self.handle,
                                                   {'abc'}))

    def test_clear_mail_box(self):
        self.handle.shell = Mock(return_value=MockResponse(''))
        self.assertIsNone(mail_util.clear_mail_box(self.handle, '1.1.1.1',
                                                   {'abc': 'abc'}))

if __name__ == '__main__':
    unittest.main()
