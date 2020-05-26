#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test Common Linux keywords
Author: Vincent Wang, wangdn@juniper.net
"""

import unittest
import mock

from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.common.common_linux import common_linux

# pylint: disable=line-too-long
# pylint: disable=invalid-name


class test_common_linux(unittest.TestCase):
    """
    Description: Linux common keywords unit test
    """
    def setUp(self):
        """
        Description: setUp unit test
        """
        self.device = mock.Mock()(spec=UnixHost)
        self.device.log = mock.Mock()
        self.linux = common_linux()

    def test_get_linux_process_id(self):
        """
        Author: Vincent Wang, wangdn@juniper.net
        Description: get_linux_process_id unit test
        """

        # device is none
        self.assertRaises(Exception, self.linux.get_linux_process_id)
        # process_name is none
        self.assertRaises(Exception, self.linux.get_linux_process_id, device=self.device)

        # command response have the process name and return the process_id
        self.device.shell().response.return_value = "root     20029  0.0  0.2  39692  2996 ?        S    Dec20   0:00 /usr/local/sbin/opensips -P /var/run/opensips.pid"
        self.assertEqual(self.linux.get_linux_process_id(device=self.device, process_name='opensips'), '20029')

        # command response don't have the process name and return None
        self.device.shell().response.return_value = ""
        self.assertEqual(self.linux.get_linux_process_id(device=self.device, process_name='opensips'), None)


if __name__ == '__main__':
    unittest.main()
