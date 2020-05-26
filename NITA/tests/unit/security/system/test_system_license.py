# coding: UTF-8
"""All unit test cases for system license module"""
# pylint: disable=attribute-defined-outside-init,invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
from unittest import TestCase, mock

from jnpr.toby.utils.junos.dut_tool import dut_tool
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.security.system.system_license import system_license


class TestLicense(TestCase):
    """Unitest cases for license module"""
    def setUp(self):
        """setup before all cases"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.ins = system_license()

        self.response = {}
        self.response["MULTI_LICENSE"] = """
    <license-usage-summary xmlns="http://xml.juniper.net/junos/15.1I0/junos-license">
        <features-used/>
        <feature-summary>
            <name>idp-sig</name>
            <description>IDP Signature</description>
            <licensed>1</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <end-date junos:seconds="1545696000">2018-12-25</end-date>
        </feature-summary>
        <feature-summary>
            <name>appid-sig</name>
            <description>APPID Signature</description>
            <licensed>1</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <end-date junos:seconds="1545696000">2018-12-25</end-date>
        </feature-summary>
        <feature-summary>
            <name>logical-system</name>
            <description>Logical System Capacity</description>
            <licensed>1</licensed>
            <used-licensed>1</used-licensed>
            <used-given>0</used-given>
            <needed>0</needed>
            <validity-type>permanent</validity-type>
        </feature-summary>
        <feature-summary>
            <name>remote-access-ipsec-vpn-client</name>
            <description>remote-access-ipsec-vpn-client</description>
            <licensed>2</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <validity-type>permanent</validity-type>
        </feature-summary>
        <feature-summary>
            <name>Virtual Appliance</name>
            <description>Virtual Appliance</description>
            <licensed>1</licensed>
            <used-licensed>1</used-licensed>
            <needed>0</needed>
            <remaining-time>
                <remaining-validity-value junos:seconds="2572880">29 days</remaining-validity-value>
            </remaining-time>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["SINGLE_PERMANENT_LICENSE"] = """
    <license-usage-summary xmlns="http://xml.juniper.net/junos/15.1I0/junos-license">
        <feature-summary>
            <name>logical-system</name>
            <description>Logical System Capacity</description>
            <licensed>1</licensed>
            <used-licensed>1</used-licensed>
            <used-given>0</used-given>
            <needed>0</needed>
            <validity-type>permanent</validity-type>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["SINGLE_END_DATE_LICENSE"] = """
    <license-usage-summary xmlns="http://xml.juniper.net/junos/15.1I0/junos-license">
        <feature-summary>
            <name>idp-sig</name>
            <description>IDP Signature</description>
            <licensed>1</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <end-date junos:seconds="1545696000">2018-12-25</end-date>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["SINGLE_REMAINING_TIME_LICENSE"] = """
    <license-usage-summary xmlns="http://xml.juniper.net/junos/15.1I0/junos-license">
        <feature-summary>
            <name>Virtual Appliance</name>
            <description>Virtual Appliance</description>
            <licensed>1</licensed>
            <used-licensed>1</used-licensed>
            <needed>0</needed>
            <remaining-time>
                <remaining-validity-value junos:seconds="2572880">29 days</remaining-validity-value>
            </remaining-time>
        </feature-summary>
    </license-usage-summary>
        """

    def tearDown(self):
        """teardown after all case"""
        pass

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_search_license(self, mock_send_cli_cmd):
        """checking search license"""
        print("search license from MULTI_LICENSE response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"])
        response = self.ins.search_license(device=object, name="remote-access-ipsec-vpn-client", validity_type="permanent")
        self.assertTrue(response)

        print("search license from PREVIOUS MULTI_LICENSE response")
        response = self.ins.search_license(device=object, match_from_previous_response=True, name="Virtual Appliance", remaining_time="29 days")
        self.assertTrue(response)

        print("search license by SINGLE END_DATE response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SINGLE_END_DATE_LICENSE"])
        response = self.ins.search_license(device=object, name="idp-sig", licensed="1 ge", needed="0", end_date="2018-12-25 00:00:00")
        self.assertTrue(response)

        print("Invalid option")
        self.assertRaisesRegex(
            ValueError,
            r"option 'device' or 'device_license_list' must given",
            self.ins.search_license,
            name="idp-sig", licensed="1 ge",
        )

        print("give option device_license_list")
        response = self.ins.search_license(
            device_license_list=self.xml.xml_string_to_dict(self.response["SINGLE_END_DATE_LICENSE"]),
            name="idp-sig",
            licensed="1 ge",
            used_licensed=0,
            needed="0",
        )
        self.assertTrue(response)

        print("check not match")
        response = self.ins.search_license(
            device_license_list=self.xml.xml_string_to_dict(self.response["SINGLE_END_DATE_LICENSE"]),
            name="idp-sig",
            licensed="1 ge",
            used_licensed=0,
            needed="0",
            end_date="2019-12-25 00:00:00",
        )
        self.assertFalse(response)

        print("search license name by 'in' behavior")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"])
        response = self.ins.search_license(device=object, name="vpn in", licensed=2)
        self.assertTrue(response)

        print("matching INT for action")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"])
        response = self.ins.search_license(device=object, name="vpn in", licensed="1-10000 in")
        self.assertTrue(response)

        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"])
        response = self.ins.search_license(device=object, name="vpn in", licensed="1 ge")
        self.assertTrue(response)
