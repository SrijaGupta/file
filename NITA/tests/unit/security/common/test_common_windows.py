#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test Windows common keywords
Author: Wentao Wu, wtwu@juniper.net
"""

import unittest
import mock
from jnpr.toby.hldcl.windows.windows import Windows
from jnpr.toby.security.common.common_windows import common_windows

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=protected-access


class test_common_windows(unittest.TestCase):
    """
    Description: Windows common keywords unit test
    """
    def setUp(self):
        """
        Description: Windows common keywords unit test setup
        """

        self.device = mock.Mock(spec=Windows)
        self.device.log = mock.Mock()
        self.win = common_windows()

    def test_run_windows_command(self):
        """
        Description: _run_windows_command unit test
        """

        # device is null
        self.assertRaises(Exception, self.win._run_windows_command)
        # command is null
        self.assertRaises(Exception, self.win._run_windows_command, device=self.device)
        # loop exception
        self.device.shell().response.return_value = " command denied "
        self.assertRaises(Exception, self.win._run_windows_command, device=self.device, command="not pass")
        # test pass
        self.device.shell().response.return_value = " test pass "
        self.assertEqual(self.win._run_windows_command(device=self.device, command='pass'), ' test pass ')
        self.device.shell().response.side_effect = ["first denied", " test pass "]
        self.assertEqual(self.win._run_windows_command(device=self.device, command='pass'), ' test pass ')

    @mock.patch("time.sleep")
    def test_config_windows_interface_ip_address(self, mock_sleep):
        """
        Description: config_windows_interface_ip_address unit test
        """

        self.win._run_windows_command = mock.Mock()
        # device exception test
        self.assertRaises(Exception, self.win.config_windows_interface_ip_address, device=None)
        # ip format exception
        self.assertRaises(ValueError, self.win.config_windows_interface_ip_address, device=self.device, interface="trf", ip="1234")
        self.assertRaises(Exception, self.win.config_windows_interface_ip_address, device=self.device, interface="trf", ip="1234")
        # command response exception test
        self.win._run_windows_command.return_value = "command incorrect"
        self.assertRaises(Exception, self.win.config_windows_interface_ip_address, device=self.device)
        self.win._run_windows_command.return_value = "command not pass"
        self.assertRaises(Exception, self.win.config_windows_interface_ip_address, device=self.device)
        # commmad response pass, ip not in response exception
        self.win._run_windows_command.return_value = "command pass"
        self.assertRaises(Exception, self.win.config_windows_interface_ip_address, device=self.device)
        # normal test
        self.win._run_windows_command.side_effect = ["pass", "default ip 1.2.3.4"]
        self.assertTrue(self.win.config_windows_interface_ip_address(device=self.device))
        response = ["pass", "1.1.1.1", "pass", "1234::4321"]
        self.win._run_windows_command.side_effect = response
        self.assertTrue(self.win.config_windows_interface_ip_address(device=self.device, interface="trf", ip="1.1.1.1"))
        self.assertTrue(self.win.config_windows_interface_ip_address(device=self.device, interface="trf", ip="1234::4321"))
        self.win._run_windows_command.side_effect = response
        self.assertTrue(self.win.config_windows_interface_ip_address(device=self.device, interface="trf", ip="1.1.1.1", mask="16"))
        self.assertTrue(self.win.config_windows_interface_ip_address(device=self.device, interface="trf", ip="1234::4321", mask="48"))
        self.win._run_windows_command.side_effect = response
        self.assertTrue(self.win.config_windows_interface_ip_address(device=self.device, interface="trf", ip="1.1.1.1", mask="16", interval=6))
        self.assertTrue(self.win.config_windows_interface_ip_address(device=self.device, interface="trf", ip="1234::4321", mask="48", interval=7, retry=5))

    @mock.patch("time.sleep")
    def test_delete_windows_interface_ip_address(self, mock_sleep):
        """
        Description: delete_windows_interface_ip_address unit test
        """

        self.win._run_windows_command = mock.Mock()
        # device exception test
        self.assertRaises(Exception, self.win.delete_windows_interface_ip_address, device=None)
        # command response exception test
        self.win._run_windows_command.return_value = "command incorrect"
        self.assertRaises(Exception, self.win.delete_windows_interface_ip_address, device=self.device)
        self.win._run_windows_command.return_value = "command not pass"
        self.assertRaises(Exception, self.win.delete_windows_interface_ip_address, device=self.device)
        # command pass, ip not in response exception
        self.win._run_windows_command.return_value = "command pass"
        self.assertRaises(Exception, self.win.delete_windows_interface_ip_address, device=self.device)
        # command pass, ip is not none
        self.assertTrue(self.win.delete_windows_interface_ip_address(device=self.device, interface="trf", ip="1.1.1.1"))
        self.assertTrue(self.win.delete_windows_interface_ip_address(device=self.device, interface="trf", ip="1234::4321"))
        self.assertTrue(self.win.delete_windows_interface_ip_address(device=self.device, interface="trf", ip="1.1.1.1", interval=6))
        self.assertTrue(self.win.delete_windows_interface_ip_address(device=self.device, interface="trf", ip="1234::4321", interval=7, retry=5))
        self.win._run_windows_command.side_effect = ["command pass", "1.1.1.1 else sleep", "test pass"]
        self.assertTrue(self.win.delete_windows_interface_ip_address(device=self.device, interface="trf", ip="1.1.1.1"))
        # command pass, ip is none
        self.win._run_windows_command.side_effect = ["command pass", "DHCP result Yes"]
        self.assertTrue(self.win.delete_windows_interface_ip_address(device=self.device))
        self.win._run_windows_command.side_effect = ["command pass", "else sleep", "DHCP result Yes"]
        self.assertTrue(self.win.delete_windows_interface_ip_address(device=self.device))


if __name__ == '__main__':
    unittest.main()
