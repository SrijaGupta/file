#! /usr/local/bin/python3

from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.hldcl.juniper.junos import Juniper
import jnpr.toby.security.policy.firewall_policy



class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=Juniper)
    mocked_obj.log = MagicMock()
    mocked_obj.cli = MagicMock()

    def test_configure_application_services_exception_1(self):
        try:
           firewall_policy.configure_application_services() 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Device handle is a mandatory argument")

        try:
           firewall_policy.configure_application_services(device=self.mocked_obj) 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "zones and service are the mandatory arguments")

    def test_configure_application_services_execution_1(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="idp"), None)


    def test_configure_application_services_execution_2(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="ssl", service_profile="sslprofile"), None)

    def test_configure_application_services_execution_3(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="utm", service_profile="utmprofile"), None)

    def test_configure_application_services_execution_4(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="app_firewall", service_profile="appfw"), None)

    def test_configure_application_services_execution_5(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="app_qos", service_profile="appqos"), None)

    def test_configure_application_services_execution_6(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="anti_malware", service_profile="antimalware"), None)

    def test_configure_application_services_execution_7(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="sec_intel", service_profile="secintel"), None)

    def test_configure_application_services_execution_8(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="ssl", mode="delete"), None)


    def test_configure_application_services_exception_2(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="ssl")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ssl_profile name is mandatory for sslfp")


    def test_configure_application_services_exception_3(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="utm")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "utm_policy is mandatory for utm")


    def test_configure_application_services_exception_4(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="app_firewall")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "rule_set_name is mandatory for app_firewall")


    def test_configure_application_services_exception_5(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="app_qos")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "rule_set_name is mandatory for app_qos")


    def test_configure_application_services_exception_6(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="anti_malware")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "anti_malware_policy is mandatory for anti_malware service")

    def test_configure_application_services_exception_7(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="sec_intel")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "sec_intel_policy is mandatory for sec_intel service")


    def test_configure_application_services_exception_8(self):
        lst = [Response("a"), Response("b")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            firewall_policy.configure_application_services(device=self.mocked_obj, from_zone="trust", to_zone="untrust", service="suchi")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Unknown service")


if __name__ == '__main__':
    unittest.main()
