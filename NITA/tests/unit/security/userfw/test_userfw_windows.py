#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test Linux userfw keywords
Author: Ruby Wu, rubywu@juniper.net
"""

import unittest
import mock

from jnpr.toby.hldcl.windows.windows import Windows
from jnpr.toby.security.userfw.userfw_windows import userfw_windows

# pylint: disable=line-too-long
# pylint: disable=invalid-name


class test_userfw_windows(unittest.TestCase):
    """
    Description: windows userfw keywords unit test
    """
    def setUp(self):
        """
        Description: setUp unit test
        """
        self.device = mock.Mock(spec=Windows)
        self.device.log = mock.Mock()
        self.windows = userfw_windows()

    def test_get_windows_domain_name(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: get_windows_domain_name unit test
        """

        # device is none
        self.assertRaises(Exception, self.windows.get_windows_domain_name)

        self.device.shell().response.side_effect = ["USERDNS", "USERDNSDOMAIN=JNPR.NET\r\n"]
        # the windows PC isn't domain controller, please double check!
        self.assertRaises(Exception, self.windows.get_windows_domain_name, device=self.device)
        # this windows PC is official computer, can't domain controller!
        self.assertRaises(Exception, self.windows.get_windows_domain_name, device=self.device)

        # normal test
        self.device.shell().response.side_effect = ["USERDNSDOMAIN=ad-jims.com\r\n"]
        self.assertTrue(self.windows.get_windows_domain_name(device=self.device))


if __name__ == '__main__':
    unittest.main()
