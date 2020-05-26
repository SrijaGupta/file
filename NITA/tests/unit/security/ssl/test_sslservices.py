import jxmlease
import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.ssl.sslservices import SslServices


# from sslservices import SslServices

class Response:
    # To return response of shell() method
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    # Mocking the handle and its methods

    def setUp(self):
        self.mocked_object = MagicMock(spec=SslServices(MagicMock()))

    def test_get_ssl_proxy_statistics(self):
        proxy_stats_xml = {}
        proxy_stats_xml["output"] = [Response("PIC:spu-4 fpc[1] pic[1] ------\
                sessions matched                          6\
                sessions bypassed:non-ssl                 6\
                sessions bypassed:mem overflow            0\
                sessions bypassed:low memory              0\
                sessions created                          10\
                sessions ignored                          0\
                sessions active                           2\
                sessions dropped                          0\
                sessions whitelisted                      4\
                whitelisted url category match            3\
                default profile hit                       1\
                session dropped no default profile        2\
                policy hit no profile configured          3\
                PIC:spu-4 fpc[1] pic[2] ------\
                sessions matched                          6\
                sessions bypassed:non-ssl                 6\
                sessions bypassed:mem overflow            0\
                sessions bypassed:low memory              0\
                sessions created                          10\
                sessions ignored                          0\
                sessions active                           2\
                sessions dropped                          0\
                sessions whitelisted                      4\
                whitelisted url category match            3\
                default profile hit                       1\
                session dropped no default profile        2\
                policy hit no profile configured          3")]

        proxy_stats_return = {'active': 4, 'bypassed:mem overflow': 0, 'whitelisted': 8,
                              'dropped': 0, 'bypassed:non-ssl': 12, 'matched': 12, 'ignored': 0,
                              'created': 20, 'whitelisted url category match': 6,
                              'default profile hit': 2,
                              'session dropped no default profile': 4,
                              'policy hit no profile configured': 6}
        self.mocked_object.device.execute_as_rpc_command = MagicMock(return_value=proxy_stats_xml)
        self.mocked_object.device.cli = MagicMock(side_effect=proxy_stats_xml["output"])
        self.assertTrue(SslServices.get_ssl_statistics(self.mocked_object), proxy_stats_return)

        proxy_stats2_xml = {}
        proxy_stats2_xml["output"] = [Response("PIC:spu-4 fpc[1] pic[1] ------\
                        sessions matched                          6\
                        sessions bypassed:non-ssl                 6\
                        sessions bypassed:mem overflow            0\
                        sessions bypassed:low memory              0\
                        sessions created                          10\
                        sessions ignored                          0\
                        sessions active                           2\
                        sessions dropped                          0\
                        sessions whitelisted                      4\
                        whitelisted url category match            3\
                        default profile hit                       1\
                        session dropped no default profile        2\
                        policy hit no profile configured          3\
                        PIC:spu-4 fpc[1] pic[2] ------\
                        sessions matched                          6\
                        sessions bypassed:non-ssl                 6\
                        sessions bypassed:mem overflow            0\
                        sessions bypassed:low memory              0\
                        sessions created                          10\
                        sessions ignored                          0\
                        sessions active                           2\
                        sessions dropped                          0\
                        sessions whitelisted                      4\
                        whitelisted url category match            3\
                        default profile hit                       1\
                        session dropped no default profile        2\
                        policy hit no profile configured          3")]

        proxy_stats_return2 = {'active': 2, 'bypassed:mem overflow': 0, 'whitelisted': 4,
                               'dropped': 0, 'bypassed:non-ssl': 6, 'matched': 6, 'ignored': 0,
                               'created': 10, 'whitelisted url category match': 3,
                               'default profile hit': 2,
                               'session dropped no default profile': 4,
                               'policy hit no profile configured': 6}

        self.mocked_object.device.execute_as_rpc_command = MagicMock(return_value=proxy_stats2_xml)
        self.mocked_object.device.cli = MagicMock(side_effect=proxy_stats2_xml["output"])
        self.assertTrue(SslServices.get_ssl_statistics(self.mocked_object, pic="fpc1 pic1"),
                        proxy_stats_return2)

    def test_clear_ssl_statistics(self):
        self.mocked_object.device.execute_as_rpc_command = MagicMock(return_value=True)
        self.assertTrue(SslServices.clear_ssl_statistics(self.mocked_object))

    def test_conf_ssl_trace_options(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_trace_options(self.mocked_object, filename="thyag" \
                                                           , maxfiles="10", size="100", \
                                                           worldreadable="false", \
                                                           flag="cli-configuration", \
                                                           level="extensive", \
                                                           noremotetrace="yes", commit='yes'))

        self.assertTrue(SslServices.conf_ssl_trace_options(self.mocked_object, filename="thyag" \
                                                           , maxfiles="10", size="100", \
                                                           worldreadable="true", \
                                                           flag="cli-configuration", \
                                                           level="extensive", \
                                                           noremotetrace="yes"))
        self.assertTrue(SslServices.conf_ssl_trace_options(self.mocked_object, mode="delete"))

        self.assertTrue(SslServices.conf_ssl_trace_options(self.mocked_object))
        self.assertTrue(SslServices.conf_ssl_trace_options(self.mocked_object, filename="test"))
        self.assertTrue(SslServices.conf_ssl_trace_options(self.mocked_object, size="10"))

        self.assertTrue(SslServices.conf_ssl_trace_options(self.mocked_object, commit="yes"))

    def test_conf_ssl_cert_identifier(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(
            SslServices.conf_ssl_cert_identifier(self.mocked_object, sslprofile="sslprofile", \
                                                 certidentifier="ssl-inspect-ca",
                                                 sslplugin='termination'))
        self.assertTrue(
            SslServices.conf_ssl_cert_identifier(self.mocked_object, sslprofile="sslprofile", \
                                                 certidentifier="ssl-inspect-ca",
                                                 sslplugin='proxy'))
        self.assertTrue(
            SslServices.conf_ssl_cert_identifier(self.mocked_object, sslprofile="sslprofile", \
                                                 certidentifier="ssl-inspect-ca",
                                                 sslplugin='initiation'))
        self.assertTrue(
            SslServices.conf_ssl_cert_identifier(self.mocked_object, sslprofile="sslprofile", \
                                                 certidentifier="ssl-inspect-ca",
                                                 sslplugin='initiation', mode='delete',
                                                 commit='no'))
        self.assertTrue(
            SslServices.conf_ssl_cert_identifier(self.mocked_object, sslprofile="sslprofile", \
                                                 certidentifier="ssl-inspect-ca",
                                                 sslplugin='thyag'))
        try:
            SslServices.conf_ssl_cert_identifier(self.mocked_object, sslplugin=None, sslprofile=None,
                                                 certidentifier=None)
        except ValueError as err:
            self.assertTrue(err.args[0],
                            'sslprofile, sslplugin and certidentifier are REQUIRED key argument')
        try:
            SslServices.conf_ssl_cert_identifier(self.mocked_object, mode="delete", commit="yes", \
                                                 sslprofile="sslprofile", sslplugin="None",
                                                 certidentifier="ssl-inspect-ca")
        except ValueError as err:
            self.assertTrue(err.args[0],
                            'when mode is delete and commit should be no,             as its not appropriate to commit without root/server-certifcate statement')

    def test_conf_ssl_crl(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_crl(self.mocked_object, sslprofile="sslprofile", \
                                                 crlaction="if-not-present", \
                                                 ifnotpresent="allow"))
        self.assertTrue(SslServices.conf_ssl_crl(self.mocked_object, sslprofile="sslprofile", \
                                                 crlaction="disable"))
        self.assertTrue(SslServices.conf_ssl_crl(self.mocked_object, sslprofile="sslprofile", \
                                                 mode="delete", commit='no'))
        try:
            SslServices.conf_ssl_crl(self.mocked_object, mode="set", sslprofile=None, \
                                     crlaction=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and crlaction is REQUIRED key argument')
        try:
            SslServices.conf_ssl_crl(self.mocked_object, sslprofile=None, mode="delete")
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')
        try:
            SslServices.conf_ssl_crl(self.mocked_object, mode="set", sslprofile="sslprofile", \
                                     ifnotpresent=None, crlaction="if-not-present")
        except ValueError as err:
            self.assertTrue(err.args[0], 'ifnotpresent is REQUIRED key argument')

    def test_conf_ssl_custom_cipher(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_custom_cipher(self.mocked_object, \
                                                           sslprofile="sslprofile", \
                                                           ciphersuite="rsa-with-rc4-128-md5", \
                                                           ))
        self.assertTrue(SslServices.conf_ssl_custom_cipher(self.mocked_object, \
                                                           sslprofile="sslprofile", \
                                                           mode="delete", ciphersuite="test" \
                                                           ))
        self.assertTrue(SslServices.conf_ssl_custom_cipher(self.mocked_object, \
                                                           sslprofile="sslprofile", \
                                                           mode="delete", ciphersuite=None, \
                                                           commit='no'))

        try:
            SslServices.conf_ssl_custom_cipher(self.mocked_object, mode="set", sslprofile=None, \
                                               ciphersuite=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and ciphersuite is REQUIRED key argument')
        try:
            SslServices.conf_ssl_custom_cipher(self.mocked_object, mode="delete", \
                                               sslprofile=None, ciphersuite=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')

    def test_conf_ssl_preferred_cipher(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_preferred_cipher(self.mocked_object, \
                                                              sslprofile="sslprofile", \
                                                              ciphersuite="strong"))
        self.assertTrue(SslServices.conf_ssl_preferred_cipher(self.mocked_object, \
                                                              sslprofile="sslprofile", \
                                                              mode="delete", commit='no'))
        try:
            SslServices.conf_ssl_preferred_cipher(self.mocked_object, mode="set", sslprofile=None \
                                                  , ciphersuite=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and ciphersuite is REQUIRED key argument')
        try:
            SslServices.conf_ssl_preferred_cipher(self.mocked_object, mode="delete", \
                                                  sslprofile=None, )
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')

    def test_conf_ssl_ignore_serv_auth(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_ignore_serv_auth(self.mocked_object, \
                                                              sslprofile="sslprofile"))

        self.assertTrue(SslServices.conf_ssl_ignore_serv_auth(self.mocked_object, \
                                                              sslprofile="sslprofile", commit='no',
                                                              mode='delete'))

        try:
            SslServices.conf_ssl_ignore_serv_auth(self.mocked_object, sslprofile=None, )
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument')

    def test_conf_ssl_cache_timeout(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_cache_timeout(self.mocked_object, \
                                                           sslprofile="sslprofile", \
                                                           timeout="300"))
        self.assertTrue(SslServices.conf_ssl_cache_timeout(self.mocked_object, \
                                                           sslprofile="sslprofile", \
                                                           timeout="300", mode='delete',
                                                           commit='no'))
        try:
            SslServices.conf_ssl_cache_timeout(self.mocked_object, sslprofile=None, timeout=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and timeout is REQUIRED key argument')

    def test_conf_cert_cache_config(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_cert_cache_config(self.mocked_object,
                                                           cmd='certificate-cache-timeout',
                                                           timeout="350"))
        self.assertTrue(
            SslServices.conf_cert_cache_config(self.mocked_object, cmd='disable-cert-cache',
                                               mode='delete'))
        self.assertTrue(
            SslServices.conf_cert_cache_config(self.mocked_object, cmd='certificate-cache-timeout',
                                               mode='delete'))
        self.assertTrue(
            SslServices.conf_cert_cache_config(self.mocked_object, cmd='disable-cert-cache'))

        try:
            SslServices.conf_cert_cache_config(self.mocked_object, cmd='certificate-cache-timeout')
        except ValueError as err:
            self.assertTrue(err.args[0], 'timeout is REQUIRED key argument')

    def test_conf_ssl_trusted_ca(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_trusted_ca(self.mocked_object, \
                                                        trusted_ca_list="all", \
                                                        sslprofile="sslprofile"))
        self.assertTrue(
            SslServices.conf_ssl_trusted_ca(self.mocked_object, mode='delete',
                                            sslprofile="sslprofile", commit='no'))
        try:
            SslServices.conf_ssl_trusted_ca(self.mocked_object, sslprofile=None, \
                                            trusted_ca_list=None, mode='set')
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and trusted_ca_list is REQUIRED key argument')
        try:
            SslServices.conf_ssl_trusted_ca(self.mocked_object, sslprofile=None, mode='delete')
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')
        try:
            SslServices.conf_ssl_trusted_ca(self.mocked_object, sslprofile="test", \
                                            trusted_ca_list="ca1 all", mode='set')
        except ValueError as err:
            self.assertTrue(err.args[0],
                            'trusted_ca_list can\'t have both all and specific trusted ca profile')

    def test_conf_ssl_flow_trace(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_flow_trace(self.mocked_object, \
                                                        sslprofile='sslprofile'))
        self.assertTrue(SslServices.conf_ssl_flow_trace(self.mocked_object, \
                                                        sslprofile='sslprofile', mode='delete',
                                                        commit='no'))
        try:
            SslServices.conf_ssl_flow_trace(self.mocked_object, sslprofile=None, )
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument')

    def test_conf_disable_ssl_proxy_resump(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_disable_ssl_proxy_resump(self.mocked_object, \
                                                                  sslprofile='sslprofile'))

        self.assertTrue(SslServices.conf_disable_ssl_proxy_resump(self.mocked_object, \
                                                                  sslprofile='sslprofile',
                                                                  mode='delete', commit='no'))

        try:
            SslServices.conf_disable_ssl_proxy_resump(self.mocked_object, sslprofile=None, )
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument')

    def test_conf_ssl_proxy_renegotiation(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_proxy_renegotiation(self.mocked_object, \
                                                                 sslprofile='sslprofile', \
                                                                 renegotiation='allow'))
        self.assertTrue(SslServices.conf_ssl_proxy_renegotiation(self.mocked_object, \
                                                                 sslprofile='sslprofile', \
                                                                 renegotiation='allow',
                                                                 mode='delete', commit='no'))
        try:
            SslServices.conf_ssl_proxy_renegotiation(self.mocked_object, sslprofile=None, \
                                                     renegotiation=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and renegotiation is REQUIRED key argument')

    def test_conf_ssl_proxy_logging(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_proxy_logging(self.mocked_object, \
                                                           sslprofile='sslprofile', \
                                                           log='all'))
        self.assertTrue(
            SslServices.conf_ssl_proxy_logging(self.mocked_object, sslprofile='sslprofile',
                                               log='all', mode='delete', commit='no'))
        self.assertTrue(
            SslServices.conf_ssl_proxy_logging(self.mocked_object, sslprofile='sslprofile',
                                               log='all', mode='thyag', commit='no'))
        try:
            SslServices.conf_ssl_proxy_logging(self.mocked_object, sslprofile=None, log=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and log is REQUIRED key argument')

    def test_conf_ssl_proxy_whitelist(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_proxy_whitelist(self.mocked_object, \
                                                             sslprofile='sslprofile', \
                                                             whitelist='test'))
        self.assertTrue(
            SslServices.conf_ssl_proxy_whitelist(self.mocked_object, sslprofile='sslprofile',
                                                 mode='delete', commit='no'))
        try:
            SslServices.conf_ssl_proxy_whitelist(self.mocked_object, sslprofile=None, \
                                                 whitelist=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and whitelist is REQUIRED key argument')
        try:
            SslServices.conf_ssl_proxy_whitelist(self.mocked_object, sslprofile=None, mode='delete')
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')

    def test_conf_sslsp_server_cert_list(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_sslsp_server_cert_list(self.mocked_object, \
                                                                sslprofile='sslprofile', \
                                                                servercert='test'))
        self.assertTrue(
            SslServices.conf_sslsp_server_cert_list(self.mocked_object, sslprofile='sslprofile',
                                                    mode='delete', commit='no'))
        try:
            SslServices.conf_sslsp_server_cert_list(self.mocked_object, sslprofile=None, \
                                                    servercert=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and servercert is REQUIRED key argument')
        try:
            SslServices.conf_sslsp_server_cert_list(self.mocked_object, sslprofile=None, \
                                                    mode='delete')
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')

    def test_conf_ssl_protocol_version(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(
            SslServices.conf_ssl_protocol_version(self.mocked_object, sslprofile='sslprofile',
                                                  tls_version='tls1'))
        self.assertTrue(
            SslServices.conf_ssl_protocol_version(self.mocked_object, sslprofile='sslprofile',
                                                  tls_version='tls1', mode='delete', commit='no'))

        try:
            SslServices.conf_ssl_protocol_version(self.mocked_object, sslprofile=None,
                                                  tls_version=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and tls_version is REQUIRED key argument')

    def test_conf_ssl_enable_sess_cache(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.mocked_object(SslServices.conf_ssl_enable_sess_cache(self.mocked_object, \
                                                               sslprofile='sslprofiel', \
                                                               sslplugin='proxy'))
        self.mocked_object(SslServices.conf_ssl_enable_sess_cache(self.mocked_object, \
                                                               sslprofile='sslprofiel', \
                                                               sslplugin='proxy', mode='delete',
                                                               commit='no'))
        try:
            SslServices.conf_ssl_enable_sess_cache(self.mocked_object, sslprofile=None, \
                                                   sslplugin=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and sslplugin is REQUIRED key argument')

    def test_conf_ssl_proxy_whitelist_url(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        self.assertTrue(SslServices.conf_ssl_proxy_whitelist_url(self.mocked_object, \
                                                                 sslprofile='sslprofile', \
                                                                 whitelist='test'))
        self.assertTrue(
            SslServices.conf_ssl_proxy_whitelist_url(self.mocked_object, sslprofile='sslprofile',
                                                     mode='delete', commit='no'))
        try:
            SslServices.conf_ssl_proxy_whitelist_url(self.mocked_object, sslprofile=None, \
                                                     whitelist=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and whitelist is REQUIRED key argument')
        try:
            SslServices.conf_ssl_proxy_whitelist_url(self.mocked_object, sslprofile=None, \
                                                     mode='delete')
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')

    def testz_conf_ssl_proxy(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        SslServices.conf_ssl_cert_identifier = MagicMock(return_value=True)
        SslServices.conf_sslsp_server_cert_list = MagicMock(return_value=True)
        SslServices.conf_ssl_proxy_whitelist_url = MagicMock(return_value=True)
        SslServices.conf_ssl_proxy_whitelist = MagicMock(return_value=True)
        SslServices.conf_ssl_proxy_logging = MagicMock(return_value=True)
        SslServices.conf_ssl_proxy_renegotiation = MagicMock(return_value=True)
        SslServices.conf_disable_ssl_proxy_resump = MagicMock(return_value=True)
        SslServices.conf_ssl_flow_trace = MagicMock(return_value=True)
        SslServices.conf_ssl_trusted_ca = MagicMock(return_value=True)
        SslServices.conf_ssl_ignore_serv_auth = MagicMock(return_value=True)
        SslServices.conf_ssl_preferred_cipher = MagicMock(return_value=True)
        SslServices.conf_ssl_custom_cipher = MagicMock(return_value=True)
        SslServices.conf_ssl_crl = MagicMock(return_value=True)
        SslServices.conf_ssl_protocol_version = MagicMock(return_value=True)

        self.assertTrue(SslServices.conf_ssl_proxy(self.mocked_object, sslplugin='forward_proxy',
                                                   sslprofile='sslprofile',
                                                   certidentifier='ssl-inspect-ca',
                                                   whitelist_url="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                   log="all",
                                                   renegotiation="allow",
                                                   resumption="disable",
                                                   enable_flow_trace="true",
                                                   trusted_ca_list='all',
                                                   ignore_server_auth="true",
                                                   ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                                   crlaction='if-not-present',
                                                   ifnotpresent='aLLow',
                                                   tls_version='all'))
        self.assertTrue(SslServices.conf_ssl_proxy(self.mocked_object, sslplugin='forward_proxy',
                                                   sslprofile='sslprofile',
                                                   certidentifier='ssl-inspect-ca',
                                                   whitelist="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                   log="all",
                                                   renegotiation="allow",
                                                   resumption="disable",
                                                   enable_flow_trace="true",
                                                   trusted_ca_list='all',
                                                   ignore_server_auth="true",
                                                   ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                                   crlaction='if-not-present',
                                                   ifnotpresent='aLLow',
                                                   tls_version='all'))
        self.assertTrue(SslServices.conf_ssl_proxy(self.mocked_object, sslplugin='forward_proxy',
                                                   sslprofile='sslprofile',
                                                   certidentifier='ssl-inspect-ca',
                                                   whitelist_url="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                   log="all",
                                                   renegotiation="allow",
                                                   resumption="disable",
                                                   enable_flow_trace="true",
                                                   trusted_ca_list='all',
                                                   ignore_server_auth="true",
                                                   ciphersuite='weak',
                                                   crlaction='if-not-present',
                                                   ifnotpresent='aLLow',
                                                   tls_version='all'))
        self.assertTrue(SslServices.conf_ssl_proxy(self.mocked_object, sslplugin='forward_proxy',
                                                   sslprofile='sslprofile',
                                                   certidentifier='ssl-inspect-ca',
                                                   whitelist_url="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                   log="all",
                                                   renegotiation="allow",
                                                   resumption="disable",
                                                   enable_flow_trace="true",
                                                   trusted_ca_list='all',
                                                   ignore_server_auth="true",
                                                   ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                                   crlaction='disable',
                                                   ifnotpresent='aLLow',
                                                   tls_version='all'))
        self.assertTrue(SslServices.conf_ssl_proxy(self.mocked_object, sslplugin='reverse_proxy',
                                                   sslprofile='sslprofile',
                                                   certidentifier='ssl-inspect-ca',
                                                   whitelist_url="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                   log="all",
                                                   renegotiation="allow",
                                                   resumption="disable",
                                                   enable_flow_trace="true",
                                                   trusted_ca_list='all',
                                                   ignore_server_auth="true",
                                                   ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                                   crlaction='if-not-present',
                                                   ifnotpresent='aLLow',
                                                   tls_version='all'))
        self.assertTrue(SslServices.conf_ssl_proxy(self.mocked_object, sslprofile='sslprofile',
                                                   mode='delete', commit='no'))
        self.assertTrue(SslServices.conf_ssl_proxy(self.mocked_object, sslplugin='thyag',
                                                   sslprofile='sslprofile',
                                                   certidentifier='ssl-inspect-ca'))
        self.assertTrue(SslServices.conf_ssl_proxy(self.mocked_object, sslplugin='forward_proxy',
                                                   sslprofile='thyag',
                                                   certidentifier='ssl-inspect-ca', mode="thyag"))

        try:
            SslServices.conf_ssl_proxy(self.mocked_object, sslplugin=None, sslprofile=None,
                                       certidentifier=None)
        except ValueError as err:
            self.assertTrue(err.args[0],
                            'sslprofile, sslplugin and certidentifier is REQUIRED key argument')
        try:
            SslServices.conf_ssl_proxy(self.mocked_object, mode='delete', sslprofile=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')

    def testz_conf_ssl_initiation(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        SslServices.conf_ssl_cert_identifier = MagicMock(return_value=True)
        SslServices.conf_ssl_flow_trace = MagicMock(return_value=True)
        SslServices.conf_ssl_trusted_ca = MagicMock(return_value=True)
        SslServices.conf_ssl_ignore_serv_auth = MagicMock(return_value=True)
        SslServices.conf_ssl_preferred_cipher = MagicMock(return_value=True)
        SslServices.conf_ssl_custom_cipher = MagicMock(return_value=True)
        SslServices.conf_ssl_crl = MagicMock(return_value=True)
        SslServices.conf_ssl_protocol_version = MagicMock(return_value=True)
        SslServices.conf_ssl_enable_sess_cache = MagicMock(return_value=True)
        self.assertTrue(SslServices.conf_ssl_initiation(self.mocked_object, sslprofile='sslinit',
                                                        certidentifier='ssl-inspect-ca',
                                                        enable_flow_trace="true",
                                                        trusted_ca_list='all',
                                                        ignore_server_auth="true",
                                                        ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                                        crlaction='if-not-present',
                                                        ifnotpresent='aLLow',
                                                        tls_version='all',
                                                        enable_session_cache='true'))
        self.assertTrue(SslServices.conf_ssl_initiation(self.mocked_object, sslprofile='sslinit',
                                                        certidentifier='ssl-inspect-ca',
                                                        enable_flow_trace="true",
                                                        trusted_ca_list='all',
                                                        ignore_server_auth="true",
                                                        ciphersuite='weak',
                                                        crlaction='if-not-present',
                                                        ifnotpresent='aLLow',
                                                        tls_version='all',
                                                        enable_session_cache='true'))
        self.assertTrue(SslServices.conf_ssl_initiation(self.mocked_object, sslprofile='sslinit',
                                                        certidentifier='ssl-inspect-ca',
                                                        enable_flow_trace="true",
                                                        trusted_ca_list='all',
                                                        ignore_server_auth="true",
                                                        ciphersuite='weak',
                                                        crlaction='disable',
                                                        ifnotpresent='aLLow',
                                                        tls_version='all',
                                                        enable_session_cache='true'))
        self.assertTrue(SslServices.conf_ssl_initiation(self.mocked_object, mode='delete',
                                                        sslprofile='sslinit', commit='no'))
        self.assertTrue(SslServices.conf_ssl_initiation(self.mocked_object, sslprofile='sslinit',
                                                        certidentifier='ssl-inspect-ca',
                                                        ))
        self.assertTrue(SslServices.conf_ssl_initiation(self.mocked_object, sslprofile='sslinit',
                                                        certidentifier='ssl-inspect-ca',
                                                        mode="test"))
        try:
            SslServices.conf_ssl_initiation(self.mocked_object, sslprofile=None,
                                            certidentifier=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and certidentifier is REQUIRED key argument')
        try:
            SslServices.conf_ssl_initiation(self.mocked_object, mode='delete', sslprofile=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')

    def testz_conf_ssl_termination(self):
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        SslServices.conf_ssl_cert_identifier = MagicMock(return_value=True)
        SslServices.conf_ssl_flow_trace = MagicMock(return_value=True)
        SslServices.conf_ssl_preferred_cipher = MagicMock(return_value=True)
        SslServices.conf_ssl_custom_cipher = MagicMock(return_value=True)
        SslServices.conf_ssl_protocol_version = MagicMock(return_value=True)
        SslServices.conf_ssl_enable_sess_cache = MagicMock(return_value=True)
        self.assertTrue(
            SslServices.conf_ssl_termination(self.mocked_object, sslprofile='sslterm',
                                             certidentifier='ssl-inspect-ca',
                                             enable_flow_trace="true",
                                             ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                             tls_version='all',
                                             enable_session_cache='true'))
        self.assertTrue(
            SslServices.conf_ssl_termination(self.mocked_object, sslprofile='sslterm',
                                             certidentifier='ssl-inspect-ca',
                                             enable_flow_trace="true",
                                             ciphersuite='weak',
                                             tls_version='all',
                                             enable_session_cache='true'))
        self.assertTrue(SslServices.conf_ssl_termination(self.mocked_object, mode='delete',
                                                         sslprofile='sslterm', commit='no'))
        self.assertTrue(
            SslServices.conf_ssl_termination(self.mocked_object, sslprofile='sslterm',
                                             certidentifier='ssl-inspect-ca',
                                             enable_flow_trace="false", commit='no'
                                             ))
        self.assertTrue(SslServices.conf_ssl_termination(self.mocked_object, mode='test',
                                                         sslprofile='sslterm', commit='no'))

        try:
            SslServices.conf_ssl_termination(self.mocked_object, sslprofile=None,
                                             certidentifier=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile and certidentifier is REQUIRED key argument')
        try:
            SslServices.conf_ssl_termination(self.mocked_object, sslprofile=None, mode='delete')
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')

    def testz_conf_ssl_proxy_scale(self):
        self.mocked_object.device.cli = MagicMock()
        self.mocked_object.device.config = MagicMock()
        self.mocked_object.device.commit = MagicMock()
        try:
            SslServices.conf_ssl_proxy_scale(self.mocked_object, sslplugin=None, sslprofile=None,
                                             certidentifier=None, mode='set')
        except ValueError as err:
            self.assertTrue(err.args[0],
                            'sslprofile, sslplugin and certidentifier is REQUIRED key argument')
        try:
            SslServices.conf_ssl_proxy_scale(self.mocked_object, mode='delete', sslprofile=None)
        except ValueError as err:
            self.assertTrue(err.args[0], 'sslprofile is REQUIRED key argument when mode is delete')

        SslServices.conf_ssl_cert_identifier = MagicMock(return_value=True)
        SslServices.conf_sslsp_server_cert_list = MagicMock(return_value=True)
        SslServices.conf_ssl_proxy_whitelist_url = MagicMock(return_value=True)
        SslServices.conf_ssl_proxy_whitelist = MagicMock(return_value=True)
        SslServices.conf_ssl_proxy_logging = MagicMock(return_value=True)
        SslServices.conf_ssl_proxy_renegotiation = MagicMock(return_value=True)
        SslServices.conf_disable_ssl_proxy_resump = MagicMock(return_value=True)
        SslServices.conf_ssl_flow_trace = MagicMock(return_value=True)
        SslServices.conf_ssl_trusted_ca = MagicMock(return_value=True)
        SslServices.conf_ssl_ignore_serv_auth = MagicMock(return_value=True)
        SslServices.conf_ssl_preferred_cipher = MagicMock(return_value=True)
        SslServices.conf_ssl_custom_cipher = MagicMock(return_value=True)
        SslServices.conf_ssl_crl = MagicMock(return_value=True)
        SslServices.conf_ssl_protocol_version = MagicMock(return_value=True)

        self.assertTrue(SslServices.conf_ssl_proxy_scale(self.mocked_object, sslplugin='forward_proxy',
                                                         sslprofile='sslprofile',
                                                         certidentifier='ssl-inspect-ca',
                                                         whitelist_url="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                         log="all",
                                                         renegotiation="allow",
                                                         resumption="disable",
                                                         enable_flow_trace="true",
                                                         trusted_ca_list='all',
                                                         ignore_server_auth="true",
                                                         ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                                         crlaction='if-not-present',
                                                         ifnotpresent='aLLow',
                                                         tls_version='all', count=1, commitcount=1))
        self.assertTrue(SslServices.conf_ssl_proxy_scale(self.mocked_object, sslplugin='forward_proxy',
                                                         sslprofile='sslprofile',
                                                         certidentifier='ssl-inspect-ca',
                                                         whitelist="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                         log="all",
                                                         renegotiation="allow",
                                                         resumption="disable",
                                                         enable_flow_trace="true",
                                                         trusted_ca_list='all',
                                                         ignore_server_auth="true",
                                                         ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                                         crlaction='if-not-present',
                                                         ifnotpresent='aLLow',
                                                         tls_version='all', count=1, commitcount=1))
        self.assertTrue(SslServices.conf_ssl_proxy_scale(self.mocked_object, sslplugin='forward_proxy',
                                                         sslprofile='sslprofile',
                                                         certidentifier='ssl-inspect-ca',
                                                         whitelist_url="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                         log="all",
                                                         renegotiation="allow",
                                                         resumption="disable",
                                                         enable_flow_trace="true",
                                                         trusted_ca_list='all',
                                                         ignore_server_auth="true",
                                                         ciphersuite='weak',
                                                         crlaction='if-not-present',
                                                         ifnotpresent='aLLow',
                                                         tls_version='all', count=1, commitcount=1))
        self.assertTrue(SslServices.conf_ssl_proxy_scale(self.mocked_object, sslplugin='forward_proxy',
                                                         sslprofile='sslprofile',
                                                         certidentifier='ssl-inspect-ca',
                                                         whitelist_url="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                         log="all",
                                                         renegotiation="allow",
                                                         resumption="disable",
                                                         enable_flow_trace="true",
                                                         trusted_ca_list='all',
                                                         ignore_server_auth="true",
                                                         ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                                         crlaction='disable',
                                                         ifnotpresent='aLLow',
                                                         tls_version='all', count=1, commitcount=1))
        self.assertTrue(SslServices.conf_ssl_proxy_scale(self.mocked_object, sslplugin='reverse_proxy',
                                                         sslprofile='sslprofile',
                                                         certidentifier='ssl-inspect-ca',
                                                         whitelist_url="Enhanced_Financial_Data_and_Services Enhanced_Social_Web_Facebook",
                                                         log="all",
                                                         renegotiation="allow",
                                                         resumption="disable",
                                                         enable_flow_trace="true",
                                                         trusted_ca_list='all',
                                                         ignore_server_auth="true",
                                                         ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                                         crlaction='if-not-present',
                                                         ifnotpresent='aLLow',
                                                         tls_version='all', count=1, commitcount=1))
        self.assertTrue(SslServices.conf_ssl_proxy_scale(self.mocked_object, sslprofile='sslprofile',
                                                         mode='delete', count=1, commitcount=1,
                                                         commit='no'))
        self.assertTrue(SslServices.conf_ssl_proxy_scale(self.mocked_object, sslprofile='sslprofile',
                                                         mode='test', count=1, commitcount=1,
                                                         commit='no'))
        self.assertTrue(
            SslServices.conf_ssl_proxy_scale(self.mocked_object, sslprofile='sslprofile',
                                             count=1, commitcount=1, commit='no', sslplugin="test"))

        self.assertTrue(
            SslServices.conf_ssl_proxy_scale(self.mocked_object, sslprofile='sslprofile',
                                             count=5, commitcount=2, commit='no',
                                             sslplugin="test"))

        self.assertTrue(
            SslServices.conf_ssl_proxy_scale(self.mocked_object, sslplugin='forward_proxy',
                                             sslprofile='sslprofile',
                                             certidentifier='ssl-inspect-ca', count=1,
                                             commitcount=1))


if __name__ == '__main__':
    unittest.main()
