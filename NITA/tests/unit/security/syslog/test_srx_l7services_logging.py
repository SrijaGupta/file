from mock import patch
import unittest2 as unittest
import builtins
from mock import MagicMock
from jnpr.toby.security.syslog import srx_l7services_logging
from jnpr.toby.hldcl.unix.unix import UnixHost
#import srx_l7services_logging


# To return response of shell() method
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    builtins.t = MagicMock()
    builtins.t.get_handle.return_value = MagicMock()
    obj1 = MagicMock()
    builtins.t.get_junos_resources.return_value = [obj1]
    builtins.t.__getitem__.return_value.__getitem__.return_value = {"system": {"primary": {"uv-syslog-host": '2.2.2.2'}}}
    builtins.t.get_version.return_value = '18.2R1'

    def test_validate_ssl_proxy_syslog_exception(self):

        try:
            srx_l7services_logging.validate_ssl_proxy_syslog()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'message' is a mandatory argument")

        try:
            srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj, message="revocation", message_type="ALLOW")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid value of Argument 'message' passed")

        try:
            srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj, message_type="INFO", message="renegotiation_started")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid value of Argument 'message' passed")

        try:
            srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj, message="abcd")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid value of Argument 'message' passed")

        try:
            srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj, message="cert_error")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid value of Argument 'message' passed")

        try:
            srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                                             message="custom")
        except Exception as err:
            self.assertEqual(err.args[0], "Argument 'custom_message' is mandatory if message=custom")

        try:
            srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj, message="cert_error:self_signed_cert", syslog_mode="abc")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid value for Argument : syslog_mode")


    @patch('jnpr.toby.security.syslog.srx_l7services_logging.check_syslog')
    def test_validate_ssl_proxy_syslog(self, patched_check_syslog):

        patched_check_syslog.return_value = True

        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj, message="cert_error:subject_issuer_mismatch"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj, syslog_mode="structured",
                                               message="insecure_renegotiation_not_permitted"), True)

        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="insecure_renegotiation_started"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="secure_renegotiation_started"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="insecure_renegotiation_completed"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="secure_renegotiation_completed"), True)

        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="revocation_reason:unspecified"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                                                          message="custom",
                                                                          custom_message="abc"),
                         True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="revocation_reason:compromise"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="revocation_reason:ca_compromise"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="revocation_reason:affiliation_changed"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="revocation_reason:superseded"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="revocation_reason:cessation_of_operation"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="revocation_reason:certificate_hold"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="revocation_reason:"), True)
        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                               message="revocation_reason:remove_from_crl"), True)

        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                                               message="revocation_reason:remove_from_crl", junos_version="11.3"), False)

        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                                               message="cert_error:self_signed_chain_cert"),
                         True)

        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                                               message="renegotiation_server_cert_different"),
                         True)

        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                                               message="cert_error:unable_to_get_local_issuer_cert"),
                         True)

        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                                               message="whitelist", message_type="WHITELIST"),
                         True)

        self.assertEqual(srx_l7services_logging.validate_ssl_proxy_syslog(device=self.mocked_obj,
                                                               message="whitelist", sni="youtube.com"),
                         True)


    def test_validate_apptrack_syslog_exception(self):
        try:
            srx_l7services_logging.validate_apptrack_syslog()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'message' is a mandatory argument")

        try:
            srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj, message="abc")
        except Exception as err:
            self.assertEqual(err.args[0], "INVALID message value")

        try:
            srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj,
                                                            message="abc", syslog_mode="abc")
        except Exception as err:
            self.assertEqual(err.args[0], "INVALID syslog mode")

    @patch('jnpr.toby.security.syslog.srx_l7services_logging.check_syslog')
    def test_validate_apptrack_syslog(self, patched_check_syslog):

        patched_check_syslog.return_value = True

        self.assertEqual(srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj,
                                                                         message="CLOSE"), True)
        self.assertEqual(srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj,
                                                                         message="CREATE"), True)
        self.assertEqual(srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj,
                                                                         message="VOL_UPDATE"),
                         True)

        self.assertEqual(srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj, message="CLOSE", reason="abc", syslog_mode="structured"), True)
        self.assertEqual(srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj, message="CREATE", syslog_mode="structured"), True)


        self.assertEqual(srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj,
                                                                         message="APBR_ZONE_MISMATCH",
                                                                         syslog_mode="structured", category="", subcategory="", destination_interface="", action="", lsys=True, routing_instance="", profile_name="", rule_name=""),
                         True)
        self.assertEqual(srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj,
                                                                         message="ROUTE_UPDATE", category="", subcategory="", destination_interface="", action="", lsys=True, routing_instance="", profile_name="", rule_name=""),
                         True)

        self.assertEqual(srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj,
                                                                         message="APBR_ZONE_MISMATCH",
                                                                         syslog_mode="event",
                                                                         category="",
                                                                         subcategory="",
                                                                         destination_interface="",
                                                                         action="", lsys=True,
                                                                         routing_instance="",
                                                                         profile_name="",
                                                                         rule_name=""),
                         True)
        self.assertEqual(srx_l7services_logging.validate_apptrack_syslog(device=self.mocked_obj,
                                                                         syslog_mode="structured",
                                                                         message="ROUTE_UPDATE",
                                                                         category="",
                                                                         subcategory="",
                                                                         destination_interface="",
                                                                         action="", lsys=True,
                                                                         routing_instance="",
                                                                         profile_name="",
                                                                         rule_name=""),
                         True)





if __name__ == '__main__':
    unittest.main()
