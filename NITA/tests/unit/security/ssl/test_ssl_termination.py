import jxmlease
import unittest2 as unittest
from mock import MagicMock, patch
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.ssl.sslservices import SslServices
from jnpr.toby.security.ssl.ssl_termination import conf_ssl_term_cert_identifier, \
    conf_ssl_term_custom_cipher, conf_ssl_term_enable_sess_cache, conf_ssl_term_flow_trace,\
    conf_ssl_term_preferred_cipher, conf_ssl_term_protocol_version, conf_ssl_termination


class Response:
    # To return response of shell() method
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    # Mocking the handle and its methods
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj_vty = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()

    def test_conf_ssl_term_cert_identifier(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_cert_identifier", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_cert_identifier = MagicMock()
        x = conf_ssl_term_cert_identifier(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_term_custom_cipher(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_custom_cipher", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_custom_cipher = MagicMock()
        x = conf_ssl_term_custom_cipher(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_term_preferred_cipher(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_preferred_cipher", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_preferred_cipher = MagicMock()
        x = conf_ssl_term_preferred_cipher(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_term_flow_trace(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_flow_trace", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_flow_trace = MagicMock()
        x = conf_ssl_term_flow_trace(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_term_protocol_version(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_protocol_version", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_protocol_version = MagicMock()
        x = conf_ssl_term_protocol_version(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_term_enable_sess_cache(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_enable_sess_cache", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_enable_sess_cache = MagicMock()
        x = conf_ssl_term_enable_sess_cache(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_termination(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_termination", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_termination = MagicMock()
        x = conf_ssl_termination(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()


if __name__ == '__main__':
    unittest.main()

