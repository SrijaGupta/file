# coding: UTF-8
# pylint: disable=attribute-defined-outside-init
"""All unit test cases for telnet_client.py"""

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import sys
import pprint
import tempfile
import time
from telnetlib import Telnet
from unittest import TestCase, mock

from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.telnet_client import TelnetClient


class TestTelnetClient(TestCase):
    """All unit test cases for TelnetClient"""
    def setUp(self):
        """setup before all case"""
        self.tool = flow_common_tool()
        self.ins = TelnetClient()

    def tearDown(self):
        """teardown after all cases"""
        pass

    def test_user_option_parser(self):
        """test user option parser"""
        print("default options testing")
        user_options = ["-i", "everywhere"]
        options = self.ins.user_option_parser(user_options=user_options)
        print(self.tool.pprint(options))
        self.assertTrue(options["ipaddr"] == "everywhere")
        self.assertTrue(options["username"] == "regress")
        self.assertTrue(options["password"] == "MaRtInI")
        self.assertTrue(options["port"] == 23)
        self.assertTrue(options["hold_time"] == 0)
        self.assertTrue(options["timeout"] == 30)
        self.assertTrue(options["firewall_username"] is None)
        self.assertTrue(options["firewall_password"] is None)
        self.assertTrue(options["cmd_list"] == [])

        print("customer options testing")
        user_options = [
            "-i", "everywhere",
            "-u", "regress",
            "-p", "HELLO",
            "--port", "2323",
            "--hold-time", "50",
            "--timeout", "100",
            "--firewall-username", "a1",
            "--firewall-password", "a2",
            "-c", "ls -l, tcpdump: tshark",
        ]
        options = self.ins.user_option_parser(user_options=user_options)
        print(self.tool.pprint(options))
        self.assertTrue(options["ipaddr"] == "everywhere")
        self.assertTrue(options["username"] == "regress")
        self.assertTrue(options["password"] == "HELLO")
        self.assertTrue(options["port"] == 2323)
        self.assertTrue(options["hold_time"] == 50)
        self.assertTrue(options["timeout"] == 100)
        self.assertTrue(options["firewall_username"] is "a1")
        self.assertTrue(options["firewall_password"] is "a2")
        self.assertTrue("tshark" in options["cmd_list"])

        print("command is from list")
        user_options = ["-i", "everywhere", "--commands", ("ls -l", "tcpdump", "tshark")]
        options = self.ins.user_option_parser(user_options=user_options)
        print(self.tool.pprint(options))
        self.assertTrue("tshark" in options["cmd_list"])

        print("checking --to-srx-device option")
        user_options = [
            "-i", "everywhere",
            "-u", "regress",
            "-p", "HELLO",
            "--port", "2323",
            "--hold-time", "50",
            "--timeout", "100",
            "-c", "ls -l",
            "--to-srx-device",
        ]
        options = self.ins.user_option_parser(user_options=user_options)
        print(self.tool.pprint(options))
        self.assertTrue(options["ipaddr"] == "everywhere")
        self.assertTrue(options["username"] == "regress")
        self.assertTrue(options["password"] == "HELLO")
        self.assertTrue(options["port"] == 2323)
        self.assertTrue(options["hold_time"] == 50)
        self.assertTrue(options["timeout"] == 100)
        self.assertTrue(options["to_srx_device"])

    @mock.patch("time.sleep")
    @mock.patch.object(Telnet, "write")
    @mock.patch.object(Telnet, "expect")
    @mock.patch.object(Telnet, "open")
    @mock.patch.object(Telnet, "set_debuglevel")
    def test_firewall_login(self, mock_set_debuglevel, mock_open_connect, mock_expect, mock_write, mock_sleep):
        """test firewall login"""
        options = self.ins.user_option_parser(user_options=["-i", "everywhere"])

        print("Normal checking")
        mock_set_debuglevel.return_value = True
        mock_open_connect.return_value = True
        mock_expect.side_effect = ["username: ", "password: ", [0, "", "Accepted"]]
        mock_write.side_effect = [True, True]
        result = self.ins.firewall_login(ipaddr="everywhere", port=21, username="regress", password="password")
        self.assertTrue(result)

        print("checking no need username")
        mock_set_debuglevel.return_value = True
        mock_expect.side_effect = [[1, "", "Login: "], ]
        result = self.ins.firewall_login(ipaddr="everywhere", port=21, username="regress", password="password")
        self.assertTrue(result)

        print("checking login failed")
        mock_set_debuglevel.return_value = True
        mock_expect.side_effect = ["username: ", "password: ", [224, "", "Denied"]]
        mock_write.side_effect = [True, True]
        result = self.ins.firewall_login(ipaddr="everywhere", port=21, username="regress", password="password")
        self.assertFalse(result)

    @mock.patch("time.sleep")
    @mock.patch.object(Telnet, "write")
    @mock.patch.object(Telnet, "expect")
    @mock.patch.object(Telnet, "open")
    @mock.patch.object(Telnet, "set_debuglevel")
    def test_login(self, mock_set_debuglevel, mock_open_connect, mock_expect, mock_write, mock_sleep):
        """test login"""
        options = self.ins.user_option_parser(user_options=["-i", "everywhere"])

        print("Normal checking")
        mock_set_debuglevel.return_value = True
        mock_open_connect.return_value = True
        mock_expect.side_effect = [b"Login: ", b"password: ", [0, "", b"correct"]]
        mock_write.side_effect = [True, True]
        result = self.ins.login(ipaddr="everywhere", port=21, username="regress", password="password")
        self.assertTrue(result)

        print("checking no need username")
        mock_set_debuglevel.return_value = True
        mock_expect.side_effect = [b"Login: ", b"password: ", [224, "", b"incorrect"]]
        mock_write.side_effect = [True, True]
        result = self.ins.login(ipaddr="everywhere", port=21, username="regress", password="password")
        self.assertFalse(result)

        print("checking --to-srx-device option")
        mock_set_debuglevel.return_value = True
        mock_expect.side_effect = [b"Login: ", b"password: ", [224, "", b"incorrect"]]
        mock_write.side_effect = [True, True]
        self.ins.options["to_srx_device"] = True
        result = self.ins.login(ipaddr="everywhere", port=21, username="regress", password="password")
        self.assertFalse(result)

    @mock.patch("time.sleep")
    @mock.patch.object(Telnet, "write")
    @mock.patch.object(Telnet, "expect")
    def test_execute_cmd(self, mock_expect, mock_write, mock_sleep):
        """test execute command"""
        options = self.ins.user_option_parser(user_options=["-i", "everywhere"])

        print("normal checking")
        self.ins.hdl = Telnet()
        self.ins.options["cmd_list"] = ("ls -l", "hostname")
        mock_expect.side_effect = ([0, 0, b"aaa\r\njonjiang aaa$ "], [0, 0, b"new_host"])
        mock_write.side_effect = [True, True]
        self.assertTrue(self.ins.execute_cmd())

        print("checking hold_time")
        self.ins.options["hold_time"] = 10
        self.ins.options["cmd_list"] = ("ls -l", "hostname")
        mock_expect.side_effect = ([0, 0, b"aaa\r\njonjiang aaa$ "], [0, 0, b"new_host"])
        mock_write.side_effect = [True, True]
        self.assertTrue(self.ins.execute_cmd())
