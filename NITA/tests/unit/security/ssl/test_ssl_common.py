import jxmlease
import unittest2 as unittest
from mock import MagicMock, patch
from jnpr.toby.hldcl.unix.unix import UnixHost
#from jnpr.toby.security.ssl.sslservices import SslServices
from jnpr.toby.security.ssl.ssl_common import get_ssl_statistics, clear_ssl_statistics, \
    conf_ssl_cache_timeout, conf_ssl_trace_options, enroll_local_ca_cert_key, conf_cert_cache_config


class Response:
    # To return response of shell() method
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    # Mocking the handle and its methods
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.cli = MagicMock()
    mocked_obj.log = MagicMock()

    def test_get_ssl_statistics(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.get_ssl_statistics", new=MagicMock())
        p.start()
        #SslServices.get_ssl_statistics = MagicMock()
        x = get_ssl_statistics(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_clear_ssl_statistics(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.clear_ssl_statistics", new=MagicMock())
        p.start()
        #SslServices.clear_ssl_statistics = MagicMock()
        x = clear_ssl_statistics(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_trace_options(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_trace_options", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_trace_options = MagicMock()
        x = conf_ssl_trace_options(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_ssl_cache_timeout(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_ssl_cache_timeout", new=MagicMock())
        p.start()
        #SslServices.conf_ssl_cache_timeout = MagicMock()
        x = conf_ssl_cache_timeout(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()

    def test_conf_cert_cache_config(self):
        p = patch("jnpr.toby.security.ssl.sslservices.SslServices.conf_cert_cache_config", new=MagicMock())
        p.start()
        #SslServices.conf_cert_cache_config = MagicMock()
        x = conf_cert_cache_config(device=self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)
        p.stop()
  
    def test_enroll_local_ca_cert_key(self):
        try:
            self.assertEqual(enroll_local_ca_cert_key(device=self.mocked_obj))
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Arguments: filename, key and certid are mandatory")
        lst = [Response("Local certificate loaded successfully")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(enroll_local_ca_cert_key(device=self.mocked_obj, filename="test", key="test", certid="test"), True)

        lst = [Response("error: Command aborted as key file already exists. Retry after clearing the existing key file")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(
            enroll_local_ca_cert_key(device=self.mocked_obj, filename="test", key="test",
                                     certid="test"), False)

        lst = [Response(
            "error: syntax error: certificaid")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(
            enroll_local_ca_cert_key(device=self.mocked_obj, filename="test", key="test",
                                     certid="test"), False)
        lst = [Response(
            "test")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(
            enroll_local_ca_cert_key(device=self.mocked_obj, filename="test", key="test",
                                     certid="test"), False)

if __name__ == '__main__':
    unittest.main()
