import unittest2 as unittest
from jnpr.toby.hldcl.connectors.common import check_socket
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.host import Host
from nose.plugins.attrib import attr


@attr('unit')
class TestJunosModule(unittest.TestCase):
    @patch('socket.socket')
    @patch('logging.info')
    def test_check_socket(self, patch1, patch2):
        self.assertTrue(check_socket(host='dummy', socket_type='telnet'))

    @patch('socket.socket')
    @patch('time.sleep')
    @patch('logging.error')
    def test_check_socket_neg(self, patch1, patch2, patch3):
        self.assertFalse(check_socket(host='dummy', socket_type='ssh',
                                      negative=1))

    @patch('socket.socket.connect', side_effect=Exception())
    @patch('time.sleep')
    @patch('logging.error')
    def test_check_socket_exception(self, patch1, patch2, patch3):
        self.assertFalse(check_socket(host='dummy', socket_type='telnet'))

    @patch('socket.socket.connect', side_effect=Exception())
    @patch('time.sleep')
    @patch('logging.error')
    def test_check_socket_exception_neg(self, patch1, patch2, patch3):
        self.assertTrue(check_socket(host='dummy', port=22, negative=1))

    @patch('logging.error')
    def test_check_socket_invalid(self, patch1):
        self.assertFalse(check_socket(host='dummy'))
