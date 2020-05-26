# coding: UTF-8
# pylint: disable=attribute-defined-outside-init
"""All unit test cases for ftp_client.py"""

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import os
import re
import sys
import pprint
import tempfile
from ftplib import FTP
from unittest import TestCase, mock

from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.ftp_client import FTPClient


class TestFTPClient(TestCase):
    """All unit test cases for FTPClient"""
    def setUp(self):
        """setup before all case"""
        self.tool = flow_common_tool()
        self.ins = FTPClient()

    def tearDown(self):
        """teardown after all cases"""
        pass

    def test_user_option_parser(self):
        """test user option parser"""
        print("default options testing")
        user_options = ["-i", "127.0.0.1", "-u", "anonymous", "-p", "anonymous"]
        options = self.ins.user_option_parser(user_options=user_options)
        pprint.pprint(options)
        self.assertTrue(options["ipaddr"] == "127.0.0.1")
        self.assertTrue(options["username"] == "anonymous")
        self.assertTrue(options["password"] == "anonymous")
        self.assertTrue(options["port"] == 21)
        self.assertTrue(options["hold_time"] == 0)
        self.assertTrue(options["timeout"] == 60)
        self.assertTrue(options["login_timeout"] == 30)
        self.assertTrue(options["passive"] is False)
        self.assertTrue(options["firewall_username"] is None)
        self.assertTrue(options["firewall_password"] is None)
        self.assertTrue(options["cmd_list"] == [])

        print("customer options testing")
        user_options = [
            "-i", "127.0.0.1",
            "-u", "regress",
            "-p", "HELLO",
            "--port", "2121",
            "--hold-time", "50",
            "--timeout", "100",
            "--login-timeout", "30",
            "--passive-mode",
            "--firewall-username", "a1",
            "--firewall-password", "a2",
            "-c", "ls -l, tcpdump: tshark",
        ]
        options = self.ins.user_option_parser(user_options=user_options)
        pprint.pprint(options)
        self.assertTrue(options["ipaddr"] == "127.0.0.1")
        self.assertTrue(options["username"] == "regress")
        self.assertTrue(options["password"] == "HELLO")
        self.assertTrue(options["port"] == 2121)
        self.assertTrue(options["hold_time"] == 50)
        self.assertTrue(options["timeout"] == 100)
        self.assertTrue(options["login_timeout"] == 30)
        self.assertTrue(options["passive"] is True)
        self.assertTrue(options["firewall_username"] is "a1")
        self.assertTrue(options["firewall_password"] is "a2")
        self.assertTrue("tshark" in options["cmd_list"])

        print("command is from list")
        user_options = ["-i", "127.0.0.1", "--commands", ("ls -l", "tcpdump", "tshark")]
        options = self.ins.user_option_parser(user_options=user_options)
        pprint.pprint(options)
        self.assertTrue("tshark" in options["cmd_list"])

    @mock.patch.object(FTP, "login")
    @mock.patch.object(FTP, "connect")
    @mock.patch.object(FTP, "set_debuglevel")
    def test_firewall_login(self, mock_set_debuglevel, mock_connect, mock_login):
        """test firewall login"""
        print("Normal checking")
        mock_set_debuglevel.return_value = True
        mock_connect.return_value = True
        mock_login.return_value = True
        result = self.ins.firewall_login(ipaddr="127.0.0.1", port=21, username="regress", password="password")
        self.assertTrue(result)

        print("checking no required option")
        self.assertRaisesRegex(TypeError, r"missing \d+ required positional arguments", self.ins.firewall_login, ipaddr="127.0.0.1")

        print("checking exception")
        mock_set_debuglevel.return_value = True
        mock_connect.return_value = True
        mock_login.side_effect = RuntimeError
        result = self.ins.firewall_login(ipaddr="127.0.0.1", port=21, username="regress", password="password")
        self.assertFalse(result)

    @mock.patch.object(FTP, "getwelcome")
    @mock.patch.object(FTP, "login")
    @mock.patch.object(FTP, "connect")
    @mock.patch.object(FTP, "set_debuglevel")
    def test_ftp_login(self, mock_set_debuglevel, mock_connect, mock_login, mock_getwelcome):
        """test ftp login"""
        print("Normal checking")
        mock_set_debuglevel.return_value = True
        mock_connect.return_value = True
        mock_login.return_value = True
        mock_getwelcome.return_value = True
        result = self.ins.ftp_login(ipaddr="127.0.0.1", port=21, username="regress", password="password")
        self.assertTrue(result)

        print("checking no required option")
        self.assertRaisesRegex(TypeError, r"missing \d+ required positional arguments", self.ins.ftp_login, ipaddr="127.0.0.1")

        print("checking exception")
        mock_set_debuglevel.return_value = True
        mock_connect.return_value = True
        mock_login.side_effect = RuntimeError
        result = self.ins.ftp_login(ipaddr="127.0.0.1", port=21, username="regress", password="password")
        self.assertFalse(result)

    @mock.patch.object(FTP, "getwelcome")
    @mock.patch.object(FTP, "login")
    @mock.patch.object(FTP, "connect")
    @mock.patch.object(FTP, "set_debuglevel")
    @mock.patch.object(FTP, "cwd")
    @mock.patch.object(FTP, "retrbinary")
    def test_get(self, mock_retrbinary, mock_cwd, mock_set_debuglevel, mock_connect, mock_login, mock_getwelcome):
        """test ftp get"""
        # prepare
        mock_set_debuglevel.return_value = True
        mock_connect.return_value = True
        mock_login.return_value = True
        mock_getwelcome.return_value = True
        self.ins.ftp_login(ipaddr="127.0.0.1", port=21, username="regress", password="password")

        print("retrive file from folder")
        mock_cwd.return_value = True
        mock_retrbinary.return_value = True
        self.assertTrue(self.ins.get("/aaa/bbb/ccc/ddd"))
        if os.path.isfile("ddd"):
            os.remove("ddd")

        print("retrive file from file")
        mock_cwd.return_value = True
        mock_retrbinary.return_value = True
        self.assertTrue(self.ins.get("ddd"))
        if os.path.isfile("ddd"):
            os.remove("ddd")

    @mock.patch.object(FTP, "storbinary")
    @mock.patch.object(FTP, "getwelcome")
    @mock.patch.object(FTP, "login")
    @mock.patch.object(FTP, "connect")
    @mock.patch.object(FTP, "set_debuglevel")
    def test_put(self, mock_set_debuglevel, mock_connect, mock_login, mock_getwelcome, mock_storbinary):
        """test ftp put"""
        # prepare
        mock_set_debuglevel.return_value = True
        mock_connect.return_value = True
        mock_login.return_value = True
        mock_getwelcome.return_value = True
        mock_storbinary.return_value = True
        self.ins.ftp_login(ipaddr="127.0.0.1", port=21, username="regress", password="password")

        print("retrive file from folder")
        mock_storbinary.return_value = True
        self.assertTrue(self.ins.put("/bin/ls"))

    @mock.patch.object(FTP, "pwd")
    @mock.patch.object(FTP, "getwelcome")
    @mock.patch.object(FTP, "login")
    @mock.patch.object(FTP, "connect")
    @mock.patch.object(FTP, "set_debuglevel")
    def test_pwd(self, mock_set_debuglevel, mock_connect, mock_login, mock_getwelcome, mock_pwd):
        """test ftp pwd"""
        # prepare
        mock_set_debuglevel.return_value = True
        mock_connect.return_value = True
        mock_login.return_value = True
        mock_getwelcome.return_value = True
        self.ins.ftp_login(ipaddr="127.0.0.1", port=21, username="regress", password="password")

        print("checking pwd action")
        mock_pwd.return_value = True
        self.assertTrue(self.ins.pwd())

    @mock.patch.object(FTP, "size")
    @mock.patch.object(FTP, "getwelcome")
    @mock.patch.object(FTP, "login")
    @mock.patch.object(FTP, "connect")
    @mock.patch.object(FTP, "set_debuglevel")
    def test_size(self, mock_set_debuglevel, mock_connect, mock_login, mock_getwelcome, mock_size):
        """test ftp size"""
        # prepare
        mock_set_debuglevel.return_value = True
        mock_connect.return_value = True
        mock_login.return_value = True
        mock_getwelcome.return_value = True
        self.ins.ftp_login(ipaddr="127.0.0.1", port=21, username="regress", password="password")

        print("checking size action")
        mock_size.return_value = True
        self.assertTrue(self.ins.size("aaa"))


    @mock.patch.object(FTP, "getwelcome")
    @mock.patch.object(FTP, "login")
    @mock.patch.object(FTP, "connect")
    @mock.patch.object(FTP, "set_debuglevel")
    def test_execute_cmd(self, mock_set_debuglevel, mock_connect, mock_login, mock_getwelcome):
        """test execute command"""
        # prepare
        mock_set_debuglevel.return_value = True
        mock_connect.return_value = True
        mock_login.return_value = True
        mock_getwelcome.return_value = True
        self.ins.ftp_login(ipaddr="127.0.0.1", port=21, username="regress", password="password")

        print("normal checking")
        self.ins.options["cmd_list"] = (
            "pwd",
            "get filename",
            "put filename",
            "size filename",
            "cd /tmp",
            "ls",
            "rmdir /aaa",
            "mkdir /aaa",
            "delete aaa",
            "delete /aaa/bbb",
        )
        self.assertTrue(self.ins.execute_cmd())

        print("unknown cmd")
        self.ins.options["cmd_list"] = ("unknown cmd")
        self.assertFalse(self.ins.execute_cmd())
        if os.path.isfile("filename"):
            os.remove("filename")
