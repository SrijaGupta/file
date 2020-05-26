import logging
import time
import unittest
from unittest.mock import Mock

from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.aamw.util import helper_util


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


class TestHelperUtil(unittest.TestCase):
    def setUp(self):
        self.handle = Mock(spec=UnixHost)
        self.handle.log = Mock()
        self.handle.download = Mock()
        self.handle.su = Mock()

        self.time_sleep_orig = time.sleep
        self.logging_info_orig = logging.info

    def tearDown(self):
        time.sleep = self.time_sleep_orig
        logging.info = self.logging_info_orig

    def test_log_break(self):
        logging.info = Mock()

        self.assertIsNone(helper_util.log_break('test_len', 8))
        self.assertIsNone(helper_util.log_break('test', 8))

    def test_sleep(self):
        time.sleep = Mock(return_value=None)

        self.assertIsNone(helper_util.sleep(1.0, 'hey'))

    def test_get_vty_cmd_prefix(self):
        self.handle.current_node = MockNode('vsrx')
        self.assertIsNotNone(helper_util.get_vty_cmd_prefix(self.handle))

        self.handle.current_node = MockNode('srx550m')
        self.assertIsNotNone(helper_util.get_vty_cmd_prefix(self.handle))

        self.handle.current_node = MockNode('srx5400')
        self.assertIsNotNone(helper_util.get_vty_cmd_prefix(self.handle))

        self.handle.current_node = MockNode('bad')
        self.assertIsNotNone(helper_util.get_vty_cmd_prefix(self.handle))

    def test_generate_new_eicar_file(self):
        self.handle.shell = Mock()
        self.assertIsNone(helper_util.generate_new_eicar_file(self.handle))


if __name__ == '__main__':
    unittest.main()
