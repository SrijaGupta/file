import copy
import unittest
from unittest.mock import Mock

from jnpr.toby.hldcl.unix.unix import UnixHost
import jnpr.toby.security.aamw.server_init as server_init


class MockResponse(object):
    def __init__(self, response):
        self.s = response

    def response(self):
        return self.s


class TestServerInit(unittest.TestCase):
    def setUp(self):
        self.handle = Mock(spec=UnixHost)
        self.handle.log = Mock()
        self.handle.download = Mock()
        self.handle.su = Mock()

    def test_single_init_network(self):
        self.handle.shell = Mock(return_value=MockResponse(''))

        res = server_init._single_init_network(
            self.handle, 'eth1', '1.1.1.1', '1.1.1.2', '1.1.1.254', '8',
            '3000::1', '3000::2', '3000::ffff', '16')
        self.assertIs(res, True)

    def test_pc_init_network(self):
        self.handle.shell = Mock(return_value=MockResponse(''))
        orig_single_init_network = server_init._single_init_network

        server_init._single_init_network = Mock(return_value=True)
        try:
            res = server_init._pc_init_network(self.handle, self.handle, True)
            self.assertIs(res, True)

            res = server_init._pc_init_network(self.handle, self.handle,
                                               False)
            self.assertIs(res, True)
        finally:
            server_init._single_init_network = orig_single_init_network

    def test_init_aamw_linux(self):
        self.handle.shell = Mock(return_value=MockResponse(''))
        orig_pc_init_network = server_init._pc_init_network
        orig_init_server_func_dict = copy.copy(server_init.SERVER_DICT)

        server_init._pc_init_network = Mock()
        server_init.SERVER_DICT = {key: Mock() for key in
                                   list(server_init.SERVER_DICT)}
        try:
            for protocol in server_init.SERVER_DICT:
                self.assertIsNone(server_init.init_aamw_linux(
                    self.handle, self.handle, protocol))
        finally:
            server_init._pc_init_network = orig_pc_init_network
            server_init.SERVER_DICT = orig_init_server_func_dict

if __name__ == '__main__':
    unittest.main()
