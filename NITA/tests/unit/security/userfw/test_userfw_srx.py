#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test userfw srx keywords
Author: Ruby Wu, rubywu@juniper.net
Author: Terry Peng, tpengu@juniper.net
"""

import unittest
import mock

from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem
from jnpr.toby.security.userfw.userfw_srx import userfw_srx

# pylint: disable=line-too-long
# pylint: disable=invalid-name


class test_userfw_srx(unittest.TestCase):
    """Description: userfw srx keywords unit test"""
    def setUp(self):
        """setup before all case"""
        self.userfw_srx = userfw_srx()
        self.device = mock.Mock()(spec=SrxSystem)
        self.device.log = mock.Mock()

    def tearDown(self):
        """teardown after all case"""
        pass

    def test_delete_srx_userfw_webapi(self):
        """
        Author: Terry Peng, tpeng@juniper.net
        Description: delete_srx_userfw_webapi unit test
        """
        # device handle exception test
        self.assertRaises(Exception, self.userfw_srx.delete_srx_userfw_webapi, device=None)
        # normal test
        self.device.config().response.return_value = " test pass "
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item=None, client_ip=None, commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item='password', client_ip=None, commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item='user', client_ip=None, commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item=None, client_ip='1.1.1.1', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item='client', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item='http port', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item='https port', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item='pki-local-certificate', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item='default-certificate', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item='https', commit=False), " test pass ")
        # commit is true test
        self.device.commit.return_value = " commit complete "
        self.assertEqual(self.userfw_srx.delete_srx_userfw_webapi(device=self.device, item='user', client_ip='1.1.1.1', commit=True), " commit complete ")

    def test_config_srx_userfw_webapi(self):
        """
        Author: Terry Peng, tpeng@juniper.net
        Description: config_srx_userfw_webapi unit test
        """
        # device handle exception test
        self.assertRaises(Exception, self.userfw_srx.config_srx_userfw_webapi, device=None)
        # normal test
        self.device.config().response.return_value = " test pass "
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, client_ip='1.1.1.1', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, user='user1', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, password='123456', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, http_port='8080', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, https_port='8443', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, certificate='1.crt', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, client_ip='1.1.1.1', user='user1', password='123456', http_port='8080', https_port='8443', certificate='1.crt', commit=False), " test pass ")
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, client_ip='1.1.1.1', user='user1', password='123456', http_port='8080', https_port='8443', certificate=None, commit=False), " test pass ")
        # commit is true test
        self.device.commit.return_value = " commit complete "
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, client_ip='1.1.1.1', user='user1', password='123456', http_port='8080', https_port='8443', certificate='1.crt', commit=True), " commit complete ")
        self.assertEqual(self.userfw_srx.config_srx_userfw_webapi(device=self.device, client_ip='1.1.1.1', user='user1', password='123456', http_port='8080', https_port='8443', certificate=None, commit=True), " commit complete ")

    def test_check_srx_userfw_no_user_auth_entry(self):
        """
        Author: John Chen, xjchen@juniper.net
        Description: check_srx_userfw_no_user_auth_entry
        """
        # device handle exception test
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_no_user_auth_entry, device=None)

        self.device.cli().response.return_value = "1.1.1.1"
        # normal test:did not find ip
        self.assertTrue(self.userfw_srx.check_srx_userfw_no_user_auth_entry(device=self.device, auth_source="active-directory", domain="ad03.net", ip="1.1.1.2", node='0', logical_system='ld1'))
        self.assertTrue(self.userfw_srx.check_srx_userfw_no_user_auth_entry(device=self.device, domain="ad03.net", ip="1.1.1.2", node='0'))
        self.assertTrue(self.userfw_srx.check_srx_userfw_no_user_auth_entry(device=self.device, domain="ad03.net", auth_source="JIMS-active directory", ip="1.1.1.2", node='0'))
        # exception test: found ip
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_no_user_auth_entry, device=self.device, auth_source="JIMS-active directory", ip="1.1.1.1")
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_no_user_auth_entry, device=self.device, node='0')

        self.device.cli().response.side_effect = ["warning", "error:"]
        # normal test:did not find ip
        self.assertTrue(self.userfw_srx.check_srx_userfw_no_user_auth_entry(device=self.device, domain="ad03.net", node='0'))
        self.assertTrue(self.userfw_srx.check_srx_userfw_no_user_auth_entry(device=self.device, domain="ad03.net", auth_source="Aruba-Clearpass", node='0'))

    @mock.patch("time.sleep")
    def test_check_srx_userfw_auth_table_number(self, mock_sleep):
        """
        Author: John Chen, xjchen@juniper.net
        Description: check_srx_userfw_auth_table_number
        """
        # device handle exception test
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_auth_table_number, device=None)
        self.device.cli().response.return_value = "Total entries: 10"
        # exception test: total_number !=0 and total_number > real_number
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_auth_table_number, device=self.device, domain="ad02.net", total_number=11, node='0')
        # exception test: total_number == 0 and doesn't match pattern
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_auth_table_number, device=self.device, domain="ad03.net", total_number=0, node='1')
        # normal test:total_number !=0 and total_number <= real_number
        self.assertTrue(self.userfw_srx.check_srx_userfw_auth_table_number(device=self.device, auth_source="active-directory", domain="ad03.net", total_number=1, node='0', logical_system='ld1'))

        self.device.cli().response.return_value = "warning:"
        # normal test:total_number ==0 and match pattern
        self.assertTrue(self.userfw_srx.check_srx_userfw_auth_table_number(device=self.device, auth_source="aruba-clearpass", total_number=0, node='0'))
        # exception test: total_number != 0 and match "warning:"
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_auth_table_number, device=self.device, domain="ad03.net", total_number=1, node='0')

        self.device.cli().response.return_value = "error:"
        # exception test: total_number == 0 and doesn't match pattern1
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_auth_table_number, device=self.device, auth_source="JIMS-Active directory", domain="ad02.net", total_number=0, node='0')
        # exception test: total_number != 0 and match "error:"
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_auth_table_number, device=self.device, domain="ad03.net", total_number=1, node='0')

    @mock.patch("time.sleep")
    def test_check_srx_userfw_device_entry_number(self, mock_sleep):
        """
        Author: John Chen, xjchen@juniper.net
        Description: check_srx_userfw_device_entry_number
        """
        # device handle exception test
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_device_entry_number, device=None)
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_device_entry_number, device=self.device, domain=None)
        self.device.cli().response.return_value = "Total entries: 10"
        # exception test: total_number !=0 and total_number > real_number
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_device_entry_number, device=self.device, domain="ad02.net", total_number=11, node='0')
        # exception test: total_number == 0 and doesn't match pattern
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_device_entry_number, device=self.device, domain="ad03.net", total_number=0, node='1')
        # normal test:total_number !=0 and total_number <= real_number
        self.assertTrue(self.userfw_srx.check_srx_userfw_device_entry_number(device=self.device, domain="ad03.net", total_number=1, node='0', logical_system='ld1'))

        self.device.cli().response.return_value = "warning:"
        # normal test:total_number ==0 and match pattern
        self.assertTrue(self.userfw_srx.check_srx_userfw_device_entry_number(device=self.device, domain="ad03.net", total_number=0, node='0'))
        # exception test: total_number != 0 and match "warning:"
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_device_entry_number, device=self.device, domain="ad03.net", total_number=1, node='0')

        self.device.cli().response.return_value = "error:"
        # exception test: total_number == 0 and doesn't match pattern1
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_device_entry_number, device=self.device, domain="ad02.net", total_number=0, node='0')
        # exception test: total_number != 0 and match "error:"
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_device_entry_number, device=self.device, domain="ad03.net", total_number=1, node='0')

    def test_check_srx_userfw_clearpass_auth_table_on_pfe(self):
        """
        Author: Terry Peng, tpeng@juniper.net
        Description: check_srx_userfw_clearpass_auth_table_on_pfe
        """
        # device handle exception test
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_auth_table_on_pfe, device=None)
        self.userfw_srx.dut.send_vty_cmd = mock.Mock()
        self.userfw_srx.dut.send_vty_cmd.return_value = """User Name: user10 Domain Name: ad03.net IP address: 3000:0:0:0:0:0:0:10
        State: valid Group number:1"""
        # user not match exception test
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_auth_table_on_pfe, device=self.device, ip='3000::10', user='user11')
        # domain not match exception test
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_auth_table_on_pfe, device=self.device, ip='3000::10', domain='ad02.net')
        # state not match exception test
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_auth_table_on_pfe, device=self.device, ip='3000::10', state='invalid')
        # group number not match exception test
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_auth_table_on_pfe, device=self.device, ip='3000::10', group_number='2')
        # auth entry not existexception test
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_auth_table_on_pfe, device=self.device, ip='3000::11')
        # normal test
        self.assertTrue(self.userfw_srx.check_srx_userfw_clearpass_auth_table_on_pfe(device=self.device, ip='3000::10', user='user10', domain='ad03.net', state='valid', group_number='1'))
        self.assertTrue(self.userfw_srx.check_srx_userfw_clearpass_auth_table_on_pfe(device=self.device, ip='3000::10', user='user10', domain='ad03.net', state='valid', group_number='1', node='0'))

    def test_config_srx_userfw_clearpass_userquery(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: config_srx_userfw_clearpass_userquery unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.config_srx_userfw_clearpass_userquery)

        # normal test
        self.assertTrue(self.userfw_srx.config_srx_userfw_clearpass_userquery(device=self.device, server_name="test"))
        self.assertTrue(self.userfw_srx.config_srx_userfw_clearpass_userquery(device=self.device, server_name="test", address="1.1.1.1", client_id="Clinet1", client_secret="Netscreen1", commit=True))
        self.assertTrue(self.userfw_srx.config_srx_userfw_clearpass_userquery(device=self.device, server_name="test", address="aaaa::bbbb", client_id="Clinet1", client_secret="Netscreen1", method="http", port="80", token_api="aa", query_api="server", commit=True))

    def test_delete_srx_userfw_clearpass_userquery(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: delete_srx_userfw_clearpass_userquery unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.delete_srx_userfw_clearpass_userquery)

        # normal test
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass_userquery(device=self.device))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass_userquery(device=self.device, item="address"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass_userquery(device=self.device, item="method", commit=True))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass_userquery(device=self.device, item="port"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass_userquery(device=self.device, item="id"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass_userquery(device=self.device, item="secret"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass_userquery(device=self.device, item="token-api"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass_userquery(device=self.device, item="query-api"))

    def test_show_srx_userfw_auth_table_all(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: show_srx_userfw_auth_table_all unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.show_srx_userfw_auth_table_all)

        # normal test, node is none
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, user="test"))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, user="test", domain="test.com"))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, group="group"))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, group="group", domain="test.com"))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, source="ad", domain="test.com"))

        # normal test, node isn't none
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, node='0', logical_system="ld1"))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, node='0', user="test"))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, node='0', user="test", domain="test.com"))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, node='0', group="group"))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, node='0', group="group", domain="test.com"))
        self.assertTrue(self.userfw_srx.show_srx_userfw_auth_table_all(device=self.device, node='0', source="cp", domain="test.com"))

    def test_delete_srx_userfw_auth_table_by_request(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: delete_srx_userfw_auth_table_by_request unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.delete_srx_userfw_auth_table_by_request)

        # normal test
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, source="aruba-clearpass", ip="1.1.1.1"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, source="active-directory", domain="test.com"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, source="identity-management", group="group1"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, source="all"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, source_name="forscot"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, source_name="forscot", domain="test.com"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, user="test_user", domain="test.com"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, group="test_group", domain="test.com"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, domain="test.com"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, user="test_user"))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_auth_table_by_request(device=self.device, group="test_group"))

    def test_check_srx_userfw_no_auth_entry_on_pfe_with_ip(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: check_srx_userfw_no_auth_entry_on_pfe_with_ip unit test
        """

        self.userfw_srx.dut.send_vty_cmd = mock.Mock()

        # device is none
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_no_auth_entry_on_pfe_with_ip)
        # ip is none
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_no_auth_entry_on_pfe_with_ip, device=self.device)
        # the specified IP doesn't exist
        self.userfw_srx.dut.send_vty_cmd.return_value = "1.1.1.1"
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_no_auth_entry_on_pfe_with_ip, device=self.device, ip='1.1.1.1')

        # normal test
        self.userfw_srx.dut.send_vty_cmd.return_value = "-------------plugin-userfw--------------"
        self.assertTrue(self.userfw_srx.check_srx_userfw_no_auth_entry_on_pfe_with_ip(device=self.device, userfw_type='ad-auth', ip='1.1.1.1'))
        self.assertTrue(self.userfw_srx.check_srx_userfw_no_auth_entry_on_pfe_with_ip(device=self.device, node=0, ip='a::a'))

    def test_check_srx_userfw_auth_entry_count_on_pfe(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: check_srx_userfw_auth_entry_count_on_pfe unit test
        """

        self.userfw_srx.dut.send_vty_cmd = mock.Mock()
        # device is none
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_auth_entry_count_on_pfe)
        # auth entry is unexpected value on pfe
        self.userfw_srx.dut.send_vty_cmd.return_value = "total auth entry count: 0"
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_auth_entry_count_on_pfe, device=self.device, count=1)

        # normal test
        self.userfw_srx.dut.send_vty_cmd.return_value = "total auth entry count: 1"
        self.assertTrue(self.userfw_srx.check_srx_userfw_auth_entry_count_on_pfe(device=self.device, userfw_type='ad-auth', count=1))
        self.assertTrue(self.userfw_srx.check_srx_userfw_auth_entry_count_on_pfe(device=self.device, node=0, userfw_type='local-auth-table', count=1))

    @mock.patch("time.sleep")
    def test_check_srx_userfw_clearpass_query_status(self, mock_sleep):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: check_srx_userfw_clearpass_query_status unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_query_status)

        self.device.cli().response.side_effect = ["Web server Address: cccc::100\r\n", "Web server Address: 2.2.2.2\r\n Status: Offline\r\n"]
        # input ip doesn't match get ip
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_query_status, device=self.device)
        # input status doesn't match get status
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_query_status, device=self.device, ip="2.2.2.2")

        # normal test
        self.device.cli().response.side_effect = ["Web server Address: 1.1.1.1\r\n Status: Online\r\n", "Web server Address: 2.2.2.2\r\n Status: Offline\r\n", "Web server Address: 2::2\r\n Status: Online\r\n"]
        self.assertTrue(self.userfw_srx.check_srx_userfw_clearpass_query_status(device=self.device))
        self.assertTrue(self.userfw_srx.check_srx_userfw_clearpass_query_status(device=self.device, ip="2.2.2.2", status="Offline"))
        self.assertTrue(self.userfw_srx.check_srx_userfw_clearpass_query_status(device=self.device, ip="2::2", status="Online"))

    def test_check_srx_userfw_clearpass_query_counter(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: check_srx_userfw_clearpass_query_counter unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_query_counter)

        self.device.cli().response.side_effect = ["Web server Address: cccc::100\r\n", "Web server Address: 1.1.1.1\r\n Access token: NULL\r\n"]
        # input ip doesn't match get ip
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_query_counter, device=self.device)
        # token is unexpected
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_query_counter, device=self.device, online=1)

        self.device.cli().response.side_effect = ["Web server Address: a::a\r\n Access token: abc\r\n Request sent number: 0\r\n", "Web server Address: 1.1.1.1\r\n Access token: abc\r\n Request sent number: 1\r\n Total response received number: 0\r\n"]
        # request number is unexpected
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_query_counter, device=self.device, ip="a::a", online=1, request_number=1)
        # response number is unexpected
        self.assertRaises(Exception, self.userfw_srx.check_srx_userfw_clearpass_query_counter, device=self.device, online=1, request_number=1, response_number=1)

        # normal test
        self.device.cli().response.side_effect = ["Web server Address: a::a\r\n Access token: abc\r\n Request sent number: 1\r\n Total response received number: 1\r\n", "Web server Address: 2.2.2.2\r\n Access token: NULL\r\n Request sent number: 0\r\n Total response received number: 0\r\n"]
        self.assertTrue(self.userfw_srx.check_srx_userfw_clearpass_query_counter(device=self.device, ip="a::a", online=1, request_number=1, response_number=1))
        self.assertTrue(self.userfw_srx.check_srx_userfw_clearpass_query_counter(device=self.device, ip="2.2.2.2", online=0, offline=1, request_number=0, response_number=0))

    def test_clear_srx_userfw_clearpass_query_counter(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: clear_srx_userfw_clearpass_query_counter unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.clear_srx_userfw_clearpass_query_counter)

        # normal test
        self.assertTrue(self.userfw_srx.clear_srx_userfw_clearpass_query_counter(device=self.device))

    @mock.patch("time.sleep")
    def test_request_srx_userfw_query(self, mock_sleep):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: request_srx_userfw_query unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.request_srx_userfw_query)

        self.device.cli().response.return_value = "error"
        # do request query failed
        self.assertRaises(Exception, self.userfw_srx.request_srx_userfw_query, device=self.device)

        # normal test
        self.device.cli().response.return_value = "pass"
        self.assertTrue(self.userfw_srx.request_srx_userfw_query(device=self.device, userfw_type="cp"))
        self.assertTrue(self.userfw_srx.request_srx_userfw_query(device=self.device, userfw_type="jims"))
        self.assertTrue(self.userfw_srx.request_srx_userfw_query(device=self.device, userfw_type="abc"))

    def test_config_srx_userfw_clearpass(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: request_srx_userfw_query unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.config_srx_userfw_clearpass)

        # normal test
        self.assertTrue(self.userfw_srx.config_srx_userfw_clearpass(device=self.device, entry_timeout=1440))
        self.assertTrue(self.userfw_srx.config_srx_userfw_clearpass(device=self.device, invalid_timeout=100))
        self.assertTrue(self.userfw_srx.config_srx_userfw_clearpass(device=self.device, no_user_query="yes", commit=True))

    def test_delete_srx_userfw_clearpass(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: request_srx_userfw_query unit test
        """

        # device is none
        self.assertRaises(Exception, self.userfw_srx.delete_srx_userfw_clearpass)

        # normal test
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass(device=self.device, entry_timeout=1440))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass(device=self.device, invalid_timeout=100))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass(device=self.device, item='authentication-entry-timeout'))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass(device=self.device, item='invalid-authentication-entry-timeout'))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass(device=self.device, item='no-user-query'))
        self.assertTrue(self.userfw_srx.delete_srx_userfw_clearpass(device=self.device, commit=True))


if __name__ == '__main__':
    unittest.main()
