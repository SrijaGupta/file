# coding: UTF-8
"""UT case for srx_manual_issu"""
from unittest import TestCase, mock
import pexpect
import re
import time

from jnpr.toby.security.issu.srx_manual_issu import srx_manual_issu


class TestSrxManualIssu(TestCase):
    """Unitest cases for SRX Manual ISSU module"""
    def setUp(self):
        """setup before all cases"""
        self.dev_object = mock.Mock()
        self.dev_object.default = {
            "username":                 "regress",
            "password":                 "MaRtInI",
            "cli_cmd_timeout":          300,
            "issu_finish_timeout":      43200
        }

        self.dev_object.prompt = {
            "shell":    re.compile(r'\%\s+'),
            "cli":      re.compile(r'\w+@\S+\>\s+'),
            "conf":     re.compile(r'\w+@\S+\#\s+'),
        }
        self.dev_object.hdl = mock.Mock()

        self.mock_hdl = mock.Mock()
        self.ins = srx_manual_issu()

    def tearDown(self):
        """Teardown"""
        pass

    @mock.patch("pexpect.spawnu")
    def test_login(self, mock_spawnu):
        """UT Case"""
        print("Normal testing")
        mock_spawnu.return_value = self.mock_hdl
        self.mock_hdl.expect.side_effect = [0, 0, 0]
        self.mock_hdl.sendline.side_effect = [True, True]
        self.assertTrue(srx_manual_issu.login(self.dev_object, ipaddr="127.0.0.1"))

        print("Input password")
        self.mock_hdl.expect.side_effect = [0, 0, 1]
        self.mock_hdl.sendline.side_effect = [True, True, True]
        self.assertTrue(srx_manual_issu.login(self.dev_object, ipaddr="127.0.0.1"))

        print("Login timeout")
        self.mock_hdl.expect.side_effect = [1, ]
        self.mock_hdl.sendline.side_effect = [True, True, True]
        self.assertFalse(srx_manual_issu.login(self.dev_object, ipaddr="127.0.0.1"))

        print("Other login issue")
        self.mock_hdl.expect.side_effect = [2, ]
        self.assertFalse(srx_manual_issu.login(self.dev_object, ipaddr="127.0.0.1"))

        self.mock_hdl.expect.side_effect = [3, ]
        self.assertFalse(srx_manual_issu.login(self.dev_object, ipaddr="127.0.0.1", show_process=True))

        self.mock_hdl.expect.side_effect = [0, 0, 2]
        self.mock_hdl.sendline.side_effect = [True, True]
        self.assertFalse(srx_manual_issu.login(self.dev_object, ipaddr="127.0.0.1"))

        self.mock_hdl.expect.side_effect = [0, 0, 3]
        self.mock_hdl.sendline.side_effect = [True, True]
        self.assertFalse(srx_manual_issu.login(self.dev_object, ipaddr="127.0.0.1"))

        print("device and ipaddr all None")
        self.assertRaisesRegex(
            RuntimeError,
            r"One of option 'device' or 'ipaddr' must be",
            self.ins.login,
        )

        print("only have device object and need get hostname")
        self.dev_object.get_host_name.return_value = "host1"
        self.mock_hdl.expect.side_effect = [0, 0, 5]
        self.mock_hdl.sendline.side_effect = [True, True, True]
        self.assertFalse(self.ins.login(device=self.dev_object, show_process=True))

    def test_mode_change(self):
        """UT Case"""
        self.dev_object.hdl = mock.Mock()

        # shell to shell
        self.dev_object.hdl.expect.side_effect = [0, 0]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="shell", show_process=True))

        # cli to shell
        self.dev_object.hdl.expect.side_effect = [1, 0, 0]
        self.dev_object.hdl.sendline.side_effect = [0, 0]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="shell"))

        # conf to shell
        self.dev_object.hdl.expect.side_effect = [2, 0, 0, 0]
        self.dev_object.hdl.sendline.side_effect = [True, 0, 0]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="shell"))

        self.dev_object.hdl.expect.side_effect = [2, 1, 0, 0, 0, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True, True, True]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="shell"))

        # shell to cli
        self.dev_object.hdl.expect.side_effect = [0, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="cli"))

        # cli to cli
        self.dev_object.hdl.expect.side_effect = [1, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="cli"))

        # conf to cli
        self.dev_object.hdl.expect.side_effect = [2, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="cli"))

        self.dev_object.hdl.expect.side_effect = [2, 1, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True, True]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="cli"))

        # shell to conf
        self.dev_object.hdl.expect.side_effect = [0, 0, 0, 0, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True, True, True, True]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="conf"))

        # cli to conf
        self.dev_object.hdl.expect.side_effect = [1, 0, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True, True]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="conf"))

        # conf to conf
        self.dev_object.hdl.expect.side_effect = [2, 0, ]
        self.dev_object.hdl.sendline.side_effect = [True, True]
        self.assertTrue(srx_manual_issu.mode_change(self.dev_object, mode="conf"))

    def test_send(self):
        """UT Cases"""
        self.dev_object.hdl = mock.Mock()

        # single cmd
        self.dev_object.hdl.expect.side_effect = [0, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True]
        self.assertTrue(srx_manual_issu.send(self.dev_object, cmd="ls", mode="shell", show_process=True, get_response=True) == '')

        # multiple cmd
        self.dev_object.hdl.expect.side_effect = [1, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True]
        response = srx_manual_issu.send(self.dev_object, cmd=["ls", "ls"], mode="cli", show_process=True, get_response=False)
        self.assertTrue(response == '')

        # multiple cmd
        self.dev_object.hdl.expect.side_effect = [2, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True]
        response = srx_manual_issu.send(self.dev_object, cmd=["ls", "ls"], mode="cli", show_process=True, get_response=False)
        self.assertTrue(response == '')

        self.dev_object.hdl.expect.side_effect = [4, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True]
        response = srx_manual_issu.send(self.dev_object, cmd=["ls", "ls"], mode="conf", show_process=True, get_response=False)
        self.assertTrue(response == '')

        # send cmd one by one
        self.dev_object.hdl.expect.side_effect = [3, 1]
        self.dev_object.hdl.sendline.side_effect = [True, True, True, True]
        response = srx_manual_issu.send(self.dev_object, cmd=["ls", "ls"], mode="cli", show_process=True, get_response=False)
        self.assertTrue(response == '')

        self.dev_object.hdl.expect.side_effect = [3, 0]
        self.dev_object.hdl.sendline.side_effect = [True, True, True, True]
        response = srx_manual_issu.send(self.dev_object, cmd=["show security", "ls"], mode="cli", show_process=True, get_response=False)
        self.assertTrue(response == '')

        # invalid option
        self.assertRaisesRegex(
            Exception,
            r"option 'cmd' must be a string or list",
            srx_manual_issu.send,
            self.dev_object, cmd=self.dev_object,
        )

    @mock.patch("time.sleep")
    def test_do_issu(self, mock_sleep):
        """UT Cases"""
        self.dev_object.hdl = mock.Mock()

        print("normal processing")
        self.ins.login = mock.Mock(return_value=True)
        self.ins.send = mock.Mock(side_effect = [True, "System going down IMMEDIATELY"])
        response = self.ins.do_issu(device=self.dev_object, package="image.tgz", more_options="more", system="vmhost")
        self.assertTrue(response)

        print("login fail")
        self.ins.login = mock.Mock(return_value=False)
        self.ins.send = mock.Mock(side_effect = [True, "System going down IMMEDIATELY"])
        response = self.ins.do_issu(device_ipaddr="127.0.0.1", package="image.tgz")
        self.assertFalse(response)

        self.ins.login = mock.Mock(return_value=True)
        self.ins.send = mock.Mock(side_effect = [True, "Do not reboot",])
        response = self.ins.do_issu(device_ipaddr="127.0.0.1", package="image.tgz")
        self.assertFalse(response)

        print("No package input")
        self.ins.login = mock.Mock(return_value=True)
        self.assertRaisesRegex(
            RuntimeError,
            r"option 'package' must be set",
            self.ins.do_issu,
            device_ipaddr="127.0.0.1",
        )

        print("reconnect device several times")
        self.ins.login = mock.Mock(side_effect=[True, False, False, False, True])
        self.ins.send = mock.Mock(side_effect = [True, "System going down IMMEDIATELY",])
        response = self.ins.do_issu(device_ipaddr="127.0.0.1", package="image.tgz", reconnection_counter=2, reconnection_interval=10)
        self.assertFalse(response)

