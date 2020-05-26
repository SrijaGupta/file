#! /usr/local/bin/python3

from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.hldcl.juniper.junos import Juniper
import utm_command
#import jnpr.toby.security.utm.utm_command



class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=Juniper)
    mocked_obj.log = MagicMock()
    mocked_obj.cli = MagicMock()
    mocked_obj.config = MagicMock()
    mocked_obj.get_rpc_equivalent = MagicMock()

    def test_check_utm_ewf_status_exception_1(self):
        try:
           utm_command.check_utm_ewf_status() 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Device handle is a mandatory argument")


    def test_check_utm_ewf_status_execution_11(self):
        lst = [Response("Server status: Juniper Enhanced using Websense server UP")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.check_utm_ewf_status(device=self.mocked_obj), True)


    def test_check_utm_ewf_status_exception_11(self):
        lst = [Response("Server status: Juniper Enhanced using Websense server DOWN")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            utm_command.check_utm_ewf_status(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "UTM status is not expected here")


    def test_check_utm_ewf_status_exception_12(self):
        lst = [Response("Down")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            utm_command.check_utm_ewf_status(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Juniper Enhanced profile is not enabled")

    def test_check_utm_ewf_status_execution_21(self):
        lst = [Response("Server status: Websense Redirect using Websense server UP")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.check_utm_ewf_status(device=self.mocked_obj, server="websense_redirect"), True)

    def test_check_utm_ewf_status_exception_21(self):
        lst = [Response("Server status: Websense Redirect using Websense server DOWN")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            utm_command.check_utm_ewf_status(device=self.mocked_obj, server="websense_redirect")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "UTM status is not expected here")


    def test_check_utm_ewf_status_exception_22(self):
        lst = [Response("Down")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            utm_command.check_utm_ewf_status(device=self.mocked_obj, server="websense_redirect")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Websense Redirect profile is not enabled")

    def test_check_utm_ewf_status_execution_31(self):
        lst = [Response("Server status: Juniper local using Websense server UP")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.check_utm_ewf_status(device=self.mocked_obj, server="juniper_local"), True)


    def test_check_utm_ewf_status_exception_31(self):
        lst = [Response("Server status: using Websense server DOWN")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            utm_command.check_utm_ewf_status(device=self.mocked_obj, server="juniper_local")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "UTM status is not expected here")




#################################################
    def test_clear_utm_cache_exception_1(self):
        try:
            utm_command.clear_utm_cache()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")


    def test_clear_utm_cache_execution_1(self):
        lst = [Response("Flush cache OK")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.clear_utm_cache(device=self.mocked_obj), True)


    def test_clear_utm_cache_exception_2(self):
        lst = [Response("Suchi")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            utm_command.clear_utm_cache(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "UTM cache is not being flushed")


##################################################################
### UT for clear_utm_statistics
    def test_clear_utm_statistics_exception_1(self):
        try:
            utm_command.clear_utm_statistics()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")


    def test_clear_utm_statistics_execution_1(self):
        lst = [Response("Flush cache OK")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.clear_utm_statistics(device=self.mocked_obj), True)


####################################################################
### UT for get_utm_statistics
    def test_get_utm_statistics_exception_1(self):
        try:
            utm_command.get_utm_statistics()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")


    def test_get_utm_statistics_exception_2(self):
        try:
            utm_command.get_utm_statistics(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "key is mandatory argument")


    def test_get_utm_statistics_execution_1(self):
        lst = [Response("Flush cache OK")]
        self.mocked_obj.get_rpc_equivalent = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.get_utm_statistics(device=self.mocked_obj, key="custom-category-block"), {})


####################################################################
### UT for config_utm_url_pattern

    def test_config_utm_url_pattern_exception_1(self):
        try:
            utm_command.config_utm_url_pattern()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")

    def test_config_utm_url_pattern_exception_2(self):
        try:
            utm_command.config_utm_url_pattern(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Value is the mandatory argument")


    def test_config_utm_url_pattern_execution_1(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_url_pattern(device=self.mocked_obj, mode="delete_all"), None)


    def test_config_utm_url_pattern_execution_2(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_url_pattern(device=self.mocked_obj, value="gmail.com"), None)


    def test_config_utm_url_pattern_execution_3(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_url_pattern(device=self.mocked_obj, value="gmail.com", commit="True"), None)


####################################################################
### UT for config_utm_custom_url_category

    def test_config_utm_custom_url_category_exception_1(self):
        try:
            utm_command.config_utm_custom_url_category()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")

    def test_config_utm_custom_url_category_execution_1(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_custom_url_category(device=self.mocked_obj, mode="delete_all"), None)

    def test_config_utm_custom_url_category_execution_2(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_custom_url_category(device=self.mocked_obj, value="juniper.net"), None)

    def test_config_utm_custom_url_category_execution_3(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_custom_url_category(device=self.mocked_obj, value="juniper.net", commit="True"), None)



####################################################################
### UT for config_utm_custom_message

    def test_config_utm_custom_message_exception_1(self):
        try:
            utm_command.config_utm_custom_message()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")

    def test_config_utm_custom_message_exception_2(self):
        try:
            utm_command.config_utm_custom_message(device=self.mocked_obj, message_type="user-message")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "message_type and message_content are mandatory arguments")

    def test_config_utm_custom_message_execution_1(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_custom_message(device=self.mocked_obj, mode="delete_all"), None)

    def test_config_utm_custom_message_execution_2(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_custom_message(device=self.mocked_obj, message_type="user-message", message_content="Suchi"), None)

    def test_config_utm_custom_message_execution_3(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_custom_message(device=self.mocked_obj, message_type="user-message", message_content="Suchi", commit="True"), None)


####################################################################
### UT for config_utm_profile

    def test_config_utm_profile_exception_1(self):
        try:
            utm_command.config_utm_profile()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")

    def test_config_utm_profile_execution_1(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile(device=self.mocked_obj, mode="delete_all"), None)

    def test_config_utm_profile_execution_2(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile(device=self.mocked_obj, mode="delete_all", profile="juniper_local"), None)

    def test_config_utm_profile_execution_3(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile(device=self.mocked_obj, mode="delete_all", profile="websense_redirect"), None)

    def test_config_utm_profile_execution_4(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile(device=self.mocked_obj), None)

    def test_config_utm_profile_execution_5(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile(device=self.mocked_obj, profile="juniper_local"), None)

    def test_config_utm_profile_execution_6(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile(device=self.mocked_obj, profile="websense_redirect"), None)

    def test_config_utm_profile_execution_7(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile(device=self.mocked_obj, message="Suchishraba"), None)

    def test_config_utm_profile_execution_8(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile(device=self.mocked_obj, message="Suchishraba", commit="True"), None)


####################################################################
### UT for config_utm_profile_global

    def test_config_utm_profile_global_exception_1(self):
        try:
            utm_command.config_utm_profile_global()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")

    def test_config_utm_profile_global_execution_1(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile_global(device=self.mocked_obj), None)

    def test_config_utm_profile_global_execution_2(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile_global(device=self.mocked_obj, profile="juniper_local"), None)

    def test_config_utm_profile_global_execution_3(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile_global(device=self.mocked_obj, profile="websense_redirect"), None)

    def test_config_utm_profile_global_execution_4(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile_global(device=self.mocked_obj, default="yes"), None)

    def test_config_utm_profile_global_execution_5(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile_global(device=self.mocked_obj, custom_block_message="yes"), None)

    def test_config_utm_profile_global_execution_6(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile_global(device=self.mocked_obj, quarantine_custom_message="yes"), None)

    def test_config_utm_profile_global_execution_7(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile_global(device=self.mocked_obj, block_message="yes", url="juniper.net"), None)

    def test_config_utm_profile_global_execution_8(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile_global(device=self.mocked_obj, quarantine_message="yes", url="juniper.net"), None)

    def test_config_utm_profile_global_execution_9(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_profile_global(device=self.mocked_obj, quarantine_message="yes", url="juniper.net", commit="True"), None)



####################################################################
### UT for config_utm_wf_type

    def test_config_utm_wf_type_exception_1(self):
        try:
            utm_command.config_utm_wf_type()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")

    def test_config_utm_wf_type_execution_1(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_wf_type(device=self.mocked_obj), None)

    def test_config_utm_wf_type_execution_2(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_wf_type(device=self.mocked_obj, profile="juniper_local"), None)

    def test_config_utm_wf_type_execution_3(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_wf_type(device=self.mocked_obj, profile="websense_redirect"), None)

    def test_config_utm_wf_type_execution_4(self):
        lst = [Response("Suchi"), Response("pallai")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_wf_type(device=self.mocked_obj, server="juniper.net"), None)

    def test_config_utm_wf_type_execution_5(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_wf_type(device=self.mocked_obj, commit="True"), None)


####################################################################
### UT for config_utm_policy

    def test_config_utm_policy_exception_1(self):
        try:
            utm_command.config_utm_policy()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Device handle is a mandatory argument")

    def test_config_utm_policy_exception_2(self):
        try:
            utm_command.config_utm_policy(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "http profile is the mandatory argument")

    def test_config_utm_policy_execution_1(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_policy(device=self.mocked_obj, http_profile="jnpr_suchi"), None)

    def test_config_utm_policy_execution_2(self):
        lst = [Response("Suchi")]
        self.mocked_obj.config = MagicMock(side_effect=lst)
        self.assertEqual(utm_command.config_utm_policy(device=self.mocked_obj, http_profile="jnpr_suchi", commit="True"), None)
###########################

if __name__ == '__main__':
    unittest.main()
