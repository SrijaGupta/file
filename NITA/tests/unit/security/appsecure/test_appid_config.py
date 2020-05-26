import unittest2 as unittest
from mock import MagicMock
#from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.appsecure.appid_config import configure_appid_sig_package, configure_application_firewall,\
    configure_apptrack, enable_apptrack_zone, clear_appid_stats_counters


# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.config = MagicMock()
    mocked_obj.commit = MagicMock()
    mocked_obj.cli = MagicMock()


    def test_configure_security_package_exception(self):
        try:
            configure_appid_sig_package()
        except Exception as err:
            self.assertEqual(err.args[0], "Argument: device is mandatory")
        try:
            configure_appid_sig_package(device=self.mocked_obj, interval="200")
        except Exception as err:
            self.assertEqual(err.args[0], "Start time is mandatory for a automatic update configuration")


        self.assertEqual(configure_appid_sig_package(device=self.mocked_obj,
                                                                url="https://devdb.juniper.net/cgi-bin/index.cgi",
                                                              secure_download=True, start_time="09-08.12:10", interval="200", ignore_server_validation=True), True)
        self.assertEqual(configure_appid_sig_package(device=self.mocked_obj), True)
        self.assertEqual(configure_appid_sig_package(device=self.mocked_obj,
                                                                mode="delete"), True)
        self.assertEqual(configure_appid_sig_package(device=self.mocked_obj,
                                                     mode="delete", commit=False), True)


    def test_configure_apptrack(self):
        try:
            configure_apptrack()
        except Exception as err:
            self.assertEqual(err.args[0], "Argument: device is mandatory")
        try:
            self.assertEqual(
                configure_apptrack(device=self.mocked_obj, what="first-update-interval"),
                True)
        except Exception as err:
            self.assertEqual(err.args[0], "Argument: Interval is mandatory when first-update-interval or session-update-interval is operation")

        self.assertEqual(configure_apptrack(device=self.mocked_obj, what="disable"), True)
        self.assertEqual((configure_apptrack(device=self.mocked_obj,what="first-update")), True)
        self.assertEqual(configure_apptrack(device=self.mocked_obj,what="first-update-interval", interval="5"), True)
        self.assertEqual(configure_apptrack(device=self.mocked_obj, what="session-update-interval", interval="5"), True)
        self.assertEqual(configure_apptrack(device=self.mocked_obj, what="thyag",
                                            interval="5"), True)

        self.assertEqual(
            configure_apptrack(device=self.mocked_obj, mode="delete"),
            True)

    def test_enable_apptrack_zone(self):
        try:
            enable_apptrack_zone()
        except Exception as err:
            self.assertEqual(err.args[0], "Argument: device is mandatory")

        self.assertEqual(enable_apptrack_zone(device=self.mocked_obj, zone="trust"), True)
        self.assertEqual(enable_apptrack_zone(device=self.mocked_obj, zone="trust", commit=False), True)

    def test_clear_appid_stats_counters(self):
        try:
            clear_appid_stats_counters()
        except Exception as err:
            self.assertEqual(err.args[0], "Argument: device and what is mandatory")

        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="apptrack"), True)
        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="appfw"), True)
        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="appfw", logical_system="test"), True)
        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="appcache"), True)
        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="appcache", logical_system="test"), True)
        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="appstats"), True)
        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="appstats", interval="1"), True)
        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="appstats", cumulative="yes"), True)
        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="all"),True)
        self.assertEqual(clear_appid_stats_counters(device=self.mocked_obj, what="thyag"), True)

    def test_configure_appfw(self):
        try:
            configure_application_firewall()
        except Exception as err:
            self.assertEqual(err.args[0], "Argument: device is mandatory")

        try:
            configure_application_firewall(mode="delete", profile=None, device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "To delete whole profile, argument profile is mandatory")

        try:
            configure_application_firewall(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "profile, rule, RI and app/appgroup is REQUIRED in each dictionary value")

        self.assertEqual(configure_application_firewall(device=self.mocked_obj, appgroup="test", profile="test", rule="1", action="allow"), True)
        self.assertEqual(configure_application_firewall(device=self.mocked_obj, app="test", profile="test", rule="1", action="allow"), True)
        self.assertEqual(configure_application_firewall(device=self.mocked_obj, appgroup="test", mode="delete", profile="test", rule="1", action="allow"), True)
        self.assertEqual(configure_application_firewall(device=self.mocked_obj, mode="delete", profile="test", rule="1", action="allow", commit=False), True)


if __name__ == '__main__':
    unittest.main()