import unittest
import builtins
from mock import patch, MagicMock
from jnpr.toby.bbe.radius.valid8 import Valid8

class TestValid8(unittest.TestCase):
    """
    TestValid8 class to handle valid8.py unit tests
    """
    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.valid8 = Valid8(dev_handle=MagicMock())

    def test_valid8_class(self):
        self.assertIsInstance(self.valid8, Valid8)

    @patch('http.client.HTTPConnection')
    def test_start_valid8_server(self, patch_http):
        try:
            self.valid8.start_valid8_server(server_name=None)
        except Exception as err:
            self.assertEqual(err.args[0], 'Server information is not given')
        try:
            self.valid8.start_valid8_server(server_name='s1')
        except Exception as err:
            self.assertEqual(err.args[0], 'IP version file information is not given')
        try:
            self.valid8.start_valid8_server(server_name='s1', ip_version='v4')
        except Exception as err:
            self.assertEqual(err.args[0], 'Config file information is not given')

        self.assertEqual(self.valid8.start_valid8_server(server_name='s1', ip_version='v4', config='cfg'), True)
        self.assertEqual(self.valid8.start_valid8_server('s1', 'v4', 'cfg', 'nas', 'pcrf', 'ocs'), True)

    @patch('http.client.HTTPConnection')
    def test_stop_valid8_server(self, patch_http):
        try:
            self.valid8.stop_valid8_server(server_name=None)
        except Exception as err:
            self.assertEqual(err.args[0], 'Server information is not given')
        self.assertEqual(self.valid8.stop_valid8_server(server_name='s1'), True)

    @patch('http.client.HTTPConnection')
    def test_send_asr(self, patch_http):
        try:
            self.valid8.send_asr(server_name=None)
        except Exception as err:
            self.assertEqual(err.args[0], 'Server information is not given')
        self.assertEqual(self.valid8.send_asr(server_name='s1'), True)

if __name__ == '__main__':
    unittest.main()
