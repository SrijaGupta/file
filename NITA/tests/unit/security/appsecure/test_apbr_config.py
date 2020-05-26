import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.security.appsecure import apbr_config



class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):


    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    """
        Unit tests for configure_apbr_profile
    """

    def test_set_configure_apbr_profile_without_device_handle(self):
        try:
            apbr_config.configure_apbr_profile()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

    def test_del_configure_apbr_profile_without_device_handle(self):
        try:
            apbr_config.configure_apbr_profile(mode="delete")
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

    def test_set_configure_apbr_profile_without_profile_name(self):
        try:
            apbr_config.configure_apbr_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Profile name is a mandatory argument")

    def test_del_configure_apbr_profile_without_profile_name(self):
        try:
            apbr_config.configure_apbr_profile(device=self.mocked_obj, mode="delete")
        except Exception as err:
            self.assertEqual(err.args[0], "Profile name is a mandatory argument")

    def test_set_configure_apbr_profile_without_rule_name(self):
        try:
            apbr_config.configure_apbr_profile(device=self.mocked_obj,
                profile="p1")
        except Exception as err:
            self.assertEqual(err.args[0], "Rule name is a mandatory argument")

    def test_set_configure_apbr_profile_without_routing_instance(self):
        try:
            apbr_config.configure_apbr_profile(device=self.mocked_obj,
                profile="p1", rulename="r1")
        except Exception as err:
            self.assertEqual(err.args[0], "Routing instance is a mandatory argument")

    def test_set_configure_apbr_profile_without_app_and_appgroup(self):
        try:
            apbr_config.configure_apbr_profile(device=self.mocked_obj,
                profile="p1", rulename="r1", routing_instance="ri1")
        except Exception as err:
            self.assertEqual(err.args[0], "Application list or applicaiton group list should not be empty")

    def test_set_configure_apbr_profile_with_app_and_appgroup(self):
        try:
            apbr_config.configure_apbr_profile(device=self.mocked_obj,
                profile="p1", rulename="r1", routing_instance="ri1",
                app_list=["junos:HTTP", "junos:FTP", "junos:FACEBOOK-CHAT"],
                appgroup_list=["junos:web:social-networking:applications", "junos:p2p"])
        except Exception as err:
            self.assertEqual(err.args[0], "Application list and application group are mutually exclusive")

    def test_set_configure_apbr_profile_with_app(self):
        status = apbr_config.configure_apbr_profile(device=self.mocked_obj,
            profile="p1", rulename="r1", routing_instance="ri1",
            app_list=["junos:HTTP", "junos:FTP", "junos:FACEBOOK-CHAT"])
        assert status is True

    def test_set_configure_apbr_profile_with_appgroup(self):
        status = apbr_config.configure_apbr_profile(device=self.mocked_obj,
            profile="p1", rulename="r1", routing_instance="ri1",
            appgroup_list=["junos:web:social-networking:applications", "junos:p2p"])
        assert status is True

    def test_set_configure_apbr_profile_with_slarule(self):
        status = apbr_config.configure_apbr_profile(device=self.mocked_obj,
            profile="p1", rulename="r1", routing_instance="ri1",
            appgroup_list=["junos:web:social-networking:applications", "junos:p2p"],
            sla_rule="sla1")
        assert status is True



    """
        Unit tests for configure_apbr_traceoptions
    """

    def test_set_configure_apbr_traceoptions_without_device_handle(self):
        try:
            apbr_config.configure_apbr_traceoptions()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

    def test_del_configure_apbr_traceoptions_without_device_handle(self):
        try:
            apbr_config.configure_apbr_traceoptions(mode="delete")
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

    def test_configure_apbr_traceoptions(self):
        self.assertEqual(apbr_config.configure_apbr_traceoptions(
            self.mocked_obj, filename="apbr-userfile", maxfiles="10",
            size="100", worldreadable="false", flag="cli-configuration",
            level="extensive", noremotetrace="yes"), True)
        self.assertEqual(apbr_config.configure_apbr_traceoptions(
            self.mocked_obj, filename="apbr-userfile", maxfiles="10",
            size="100", worldreadable=True, flag="cli-configuration",
            level="extensive", noremotetrace=True, match="abc"), True)
        self.assertEqual(apbr_config.configure_apbr_traceoptions(
            self.mocked_obj, mode="delete"), True)
        self.assertEqual(apbr_config.configure_apbr_traceoptions(
            self.mocked_obj), True)

    """
        Unit tests for enable_apbr_zone
    """

    def test_set_enable_apbr_zone_without_device_handle(self):
        try:
            apbr_config.enable_apbr_zone()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

    def test_del_enable_apbr_zone_without_device_handle(self):
        try:
            apbr_config.enable_apbr_zone(mode="delete")
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

    def test_set_enable_apbr_zone_without_zone(self):
        try:
            apbr_config.enable_apbr_zone(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Zone is a mandatory argument")

    def test_del_enable_apbr_zone_without_zone(self):
        try:
            apbr_config.enable_apbr_zone(device=self.mocked_obj, mode="delete")
        except Exception as err:
            self.assertEqual(err.args[0], "Zone is a mandatory argument")

    def test_set_enable_apbr_zone_without_profile(self):
        try:
            apbr_config.enable_apbr_zone(device=self.mocked_obj, zone="z1")
        except Exception as err:
            self.assertEqual(err.args[0], "Profile is a mandatory argument")

    def test_del_enable_apbr_zone_without_profile(self):
        try:
            apbr_config.enable_apbr_zone(device=self.mocked_obj, zone="z1", mode="delete")
        except Exception as err:
            self.assertEqual(err.args[0], "Profile is a mandatory argument")

    def test_set_enable_apbr_zone(self):
        status = apbr_config.enable_apbr_zone(device=self.mocked_obj,
            profile="p1", zone="z1")
        assert status is True

    def test_del_enable_apbr_zone(self):
        status = apbr_config.enable_apbr_zone(device=self.mocked_obj,
            profile="p1", zone="z1")
        assert status is True
        status = apbr_config.enable_apbr_zone(device=self.mocked_obj, mode="delete",
            profile="p1", zone="z1")
        assert status is True

    def test_configure_apbr_profile1(self):
        status = apbr_config.configure_apbr_profile(device=self.mocked_obj, profile="ab",mode="delete")
        assert status is True

    def test_config_apbr_tunables(self):
        try:
            apbr_config.config_apbr_tunables()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        self.mocked_obj.config = MagicMock()
        self.mocked_obj.commit = MagicMock()

        self.assertEqual(apbr_config.config_apbr_tunables(device=self.mocked_obj), True)

if __name__ == '__main__':
    unittest.main()
