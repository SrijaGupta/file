#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test Linux VoIP ALG keywords
Author: Vincent Wang, wangdn@juniper.net
"""

import unittest
import mock

from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.alg.alg_srx import alg_srx

# pylint: disable=line-too-long
# pylint: disable=invalid-name


class test_alg_srx(unittest.TestCase):
    """
    Description: ALG SRX keywords unit test
    """
    def setUp(self):
        """
        Description: setUp unit test
        """
        self.device = mock.Mock()(spec=UnixHost)
        self.device.log = mock.Mock()
        self.srx = alg_srx()

    def test_request_srx_service_twamp(self):
        """
        Author: Vincent Wang, wangdn@juniper.net
        Description: request_srx_service_twamp unit test
        """
        # device is none
        self.assertRaises(Exception, self.srx.request_srx_service_twamp)
        # operator is none
        self.assertRaises(Exception, self.srx.request_srx_service_twamp, device=self.device)
        # return error in response
        self.device.cli().response.return_value = "error"
        self.assertRaises(Exception, self.srx.request_srx_service_twamp, device=self.device, operator="start")
        # return True
        self.device.cli().response.return_value = "pass"
        self.assertEqual(self.srx.request_srx_service_twamp(device=self.device, operator="start", control_name="c1"), "pass")


if __name__ == '__main__':
    unittest.main()
