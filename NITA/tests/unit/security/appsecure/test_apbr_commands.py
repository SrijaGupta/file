from mock import patch
import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.appsecure import apbr_commands
from jnpr.toby.hldcl.juniper.security.srx import Srx



class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):

    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_get_apbr_profile(self):
        try:
            apbr_commands.get_apbr_profile()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

        dict_to_return = {'apbr-profiles':
                                            {'apbr-profiles': {'pic': 0
                                                              }
                                            }
                         }
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=dict_to_return)
        self.assertEqual(apbr_commands.get_apbr_profile(device=self.mocked_obj), {})

        dict_to_return = {'apbr-profiles':
                              {'apbr-profiles': {'profile-name': "abc",
                                                 'zone-name': "trust"
                                                 }
                               }
                          }
        self.mocked_obj.execute_as_rpc_command.return_value = dict_to_return
        self.assertEqual(apbr_commands.get_apbr_profile(device=self.mocked_obj), {"abc":"trust"})

        dict_to_return = {'apbr-profiles':
                              {'apbr-profiles': {'profile-name': ["abc", "def"],
                                                 'zone-name': ["trust", "untrust"]
                                                 }
                               }
                          }

        x = {"abc":"trust", "def":"untrust"}
        self.mocked_obj.execute_as_rpc_command.return_value = dict_to_return
        self.assertEqual(apbr_commands.get_apbr_profile(device=self.mocked_obj), x)


    def test_verify_apbr_profile(self):
        try:
            apbr_commands.verify_apbr_profile()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            apbr_commands.verify_apbr_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'profile_name' is a mandatory argument")

        x = {"abc": "trust", "def": "untrust"}
        self.assertEqual(apbr_commands.verify_apbr_profile(device=self.mocked_obj, profile_dict=x, profile_name="def", zone_name="untrust"), True)
        self.assertEqual(apbr_commands.verify_apbr_profile(device=self.mocked_obj, profile_dict={}, no_profile=True),True)

        p = patch("jnpr.toby.security.appsecure.apbr_commands.get_apbr_profile", new=MagicMock(return_value=x))
        p.start()
        self.assertEqual(apbr_commands.verify_apbr_profile(device=self.mocked_obj, profile_name="abc"),True)
        p.stop()

        try:
            apbr_commands.verify_apbr_profile(device=self.mocked_obj, profile_dict={}, profile_name="abc", zone_name="untrust")
        except Exception as err:
            self.assertEqual(err.args[0], "No profiles configured")

        try:
            apbr_commands.verify_apbr_profile(device=self.mocked_obj, profile_dict=x, no_profile=True)
        except Exception as err:
            self.assertEqual(err.args[0], "Expected-NO profile, but some profile was found")

        try:
            apbr_commands.verify_apbr_profile(device=self.mocked_obj, profile_dict=x, profile_name="abc", zone_name="untrust")
        except Exception as err:
            self.assertEqual(err.args[0], "Zone name NOT matching")

        try:
            apbr_commands.verify_apbr_profile(device=self.mocked_obj, profile_dict=x, profile_name="abcd", zone_name="untrust")
        except Exception as err:
            self.assertEqual(err.args[0], "Profile name not found")


    def test_get_apbr_stats(self):
        try:
            apbr_commands.get_apbr_stats()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

        dict_to_return = {'apbr-statistics':
                              {'apbr-statistics': {'pic': 0
                                                 }
                               }
                          }
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=dict_to_return)
        self.assertEqual(apbr_commands.get_apbr_stats(device=self.mocked_obj), {'pic':0})


    def test_verify_apbr_stats(self):
        try:
            apbr_commands.verify_apbr_stats()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

        try:
            apbr_commands.verify_apbr_stats(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "counter_values is None, it is mandatory argument")


        x = {"a" : "1", "b":"2", "c":"3"}
        p = patch("jnpr.toby.security.appsecure.apbr_commands.get_apbr_stats", new=MagicMock(return_value=x))
        p.start()

        self.assertEqual(apbr_commands.verify_apbr_stats(device=self.mocked_obj, counter_values={"b":2, "c":3}), True)


        try:
            apbr_commands.verify_apbr_stats(device=self.mocked_obj, counter_values={"b": 1, "c": 3})
        except Exception as err:
            self.assertEqual(err.args[0], "APBR statistics validation failed")

        try:
            apbr_commands.verify_apbr_stats(device=self.mocked_obj, counter_values={"d": 1, "c": 3})
        except Exception as err:
            self.assertEqual(err.args[0], "APBR statistics validation failed")


    def test_clear_apbr_stats(self):
        try:
            apbr_commands.clear_apbr_stats()
        except Exception as err:
            self.assertEqual(err.args[0],"Device handle is a mandatory argument" )

        self.mocked_obj.cli = MagicMock(return_value=Response(""))

        try:
            apbr_commands.clear_apbr_stats(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "APBR stats couldn't be cleared")

        self.mocked_obj.cli.return_value = Response("Advance-policy-based-routing statistics clear done")

        self.assertEqual(apbr_commands.clear_apbr_stats(device=self.mocked_obj), True)





if __name__ == '__main__':
    unittest.main()