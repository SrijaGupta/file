import jxmlease
import unittest2 as unittest
from mock import MagicMock, patch
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.ssl.sslservices import SslServices
from jnpr.toby.security.ssl.ssl_proxy import conf_ssl_proxy_cert_identifier, \
    conf_ssl_proxy_crl, conf_ssl_proxy_custom_cipher, \
    conf_ssl_proxy_preferred_cipher, conf_ssl_proxy_ignore_serv_auth, \
    conf_ssl_proxy_flow_trace, conf_ssl_proxy_trusted_ca, \
    conf_disable_ssl_proxy_resump, conf_ssl_proxy_renegotiation,\
    conf_ssl_proxy_whitelist, conf_ssl_proxy_whitelist_url, conf_sslsp_server_cert_list, \
    conf_sslsp_server_cert_list, conf_ssl_proxy_protocol_version, conf_ssl_proxy, \
    conf_ssl_proxy_logging, get_vty_jsf_ssl_counters, conf_ssl_proxy_scale


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

    def test_conf_ssl_proxy_cert_identifier(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_cert_identifier", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_cert_identifier = MagicMock()
        x = conf_ssl_proxy_cert_identifier(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_crl(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_crl", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_crl = MagicMock()
        x = conf_ssl_proxy_crl(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_custom_cipher(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_custom_cipher", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_custom_cipher = MagicMock()
        x = conf_ssl_proxy_custom_cipher(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_preferred_cipher(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_preferred_cipher", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_preferred_cipher = MagicMock()
        x = conf_ssl_proxy_preferred_cipher(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_ignore_serv_auth(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_ignore_serv_auth", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_ignore_serv_auth = MagicMock()
        x = conf_ssl_proxy_ignore_serv_auth(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_trusted_ca(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_trusted_ca", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_trusted_ca = MagicMock()
        x = conf_ssl_proxy_trusted_ca(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_flow_trace(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_flow_trace", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_flow_trace = MagicMock()
        x = conf_ssl_proxy_flow_trace(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_disable_ssl_proxy_resump(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_disable_ssl_proxy_resump", new=MagicMock())
        p.start()
        #SslServices.conf_disable_ssl_proxy_resump = MagicMock()
        x = conf_disable_ssl_proxy_resump(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_renegotiation(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_proxy_renegotiation", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_proxy_renegotiation = MagicMock()
        x = conf_ssl_proxy_renegotiation(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_logging(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_proxy_logging", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_proxy_logging = MagicMock()
        x = conf_ssl_proxy_logging(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_whitelist(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_proxy_whitelist", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_proxy_whitelist = MagicMock()
        x = conf_ssl_proxy_whitelist(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_sslsp_server_cert_list(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_sslsp_server_cert_list", new=MagicMock())
        p.start()
        #SslServices.conf_sslsp_server_cert_list = MagicMock()
        x = conf_sslsp_server_cert_list(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_protocol_version(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_protocol_version", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_protocol_version = MagicMock()
        x = conf_ssl_proxy_protocol_version(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_proxy_whitelist_url(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_proxy_whitelist_url", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_proxy_whitelist_url = MagicMock()
        x = conf_ssl_proxy_whitelist_url(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()
      
    def test_conf_ssl_proxy(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_proxy", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_proxy = MagicMock()
        x = conf_ssl_proxy(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    @patch('jnpr.toby.security.ssl.ssl_proxy.get_vty_counters_as_dictionary')
    def test_get_vty_jsf_ssl_counters(self, get_vty_patch):
        try:
            get_vty_jsf_ssl_counters(device=None)
        except Exception as err:
            self.assertEqual(err.args[0], "device is a mandatory argument")

        dict_to_return = {'counter1':1, 'counter2':2}
        #get_vty_counters_as_dictionary = MagicMock(return_value=dict_to_return)
        get_vty_patch.return_value = dict_to_return
        self.assertEqual(get_vty_jsf_ssl_counters(device=self.mocked_obj_vty), dict_to_return)

    def test_conf_ssl_proxy_scale(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_proxy_scale", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_proxy_scale = MagicMock()
        x = conf_ssl_proxy_scale(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

if __name__ == '__main__':
    unittest.main()

