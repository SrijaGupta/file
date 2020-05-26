import jxmlease
import unittest2 as unittest
from mock import MagicMock, patch
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.ssl.sslservices import SslServices
from jnpr.toby.security.ssl.ssl_initiation import conf_ssl_init_cert_identifier, conf_ssl_init_crl,\
    conf_ssl_init_custom_cipher, conf_ssl_init_enable_sess_cache, conf_ssl_init_flow_trace, \
    conf_ssl_init_ignore_serv_auth, conf_ssl_init_preferred_cipher, conf_ssl_init_profile,\
    conf_ssl_init_protocol_version, conf_ssl_init_trusted_ca


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

    def test_conf_ssl_init_cert_identifier(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_cert_identifier", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_cert_identifier = MagicMock()
        x = conf_ssl_init_cert_identifier(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_init_crl(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_crl", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_crl = MagicMock()
        x = conf_ssl_init_crl(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_init_custom_cipher(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_custom_cipher", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_custom_cipher = MagicMock()
        x = conf_ssl_init_custom_cipher(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_init_preferred_cipher(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_preferred_cipher", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_preferred_cipher = MagicMock()
        x = conf_ssl_init_preferred_cipher(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_init_ignore_serv_auth(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_ignore_serv_auth", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_ignore_serv_auth = MagicMock()
        x = conf_ssl_init_ignore_serv_auth(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_init_trusted_ca(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_trusted_ca", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_trusted_ca = MagicMock()
        x = conf_ssl_init_trusted_ca(device = self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_init_flow_trace(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_flow_trace", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_flow_trace = MagicMock()
        x = conf_ssl_init_flow_trace(device = self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_init_protocol_version(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_protocol_version", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_protocol_version = MagicMock()
        x = conf_ssl_init_protocol_version(device = self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_init_enable_sess_cache(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_enable_sess_cache", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_enable_sess_cache = MagicMock()
        x = conf_ssl_init_enable_sess_cache(device = self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_init_profile(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_initiation", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_initiation = MagicMock()
        x = conf_ssl_init_profile(device = self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()


if __name__ == '__main__':
    unittest.main()

