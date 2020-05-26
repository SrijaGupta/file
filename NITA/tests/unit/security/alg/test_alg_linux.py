#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test Linux pptp keywords
Author: sebrinazhao, sebrinazhao@juniper.net
"""


import unittest
import mock

from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.alg.alg_linux import alg_linux

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments


class test_alg_linux(unittest.TestCase):
    """All unit test cases for setup_server module"""
    def setUp(self):
        """setup before all cases"""
        self.device = mock.Mock()(spec=UnixHost)
        self.device.log = mock.Mock()
        self.linux = alg_linux()

    def tearDown(self):
        """teardown after all cases"""
        pass

    def test_config_linux_pptp_client_option(self):
        """
        Description: test config_linux_pptp_client_option
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none
        self.assertRaises(Exception, self.linux.config_linux_pptp_client_option)

        # normal test
        self.assertTrue(self.linux.config_linux_pptp_client_option(device=self.device, option_file="111", option_file_bak="222", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_option(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_option(device=self.device, option_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client_option(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_option(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_option(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_option(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_option(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_option(device=self.device, option_file="111", timeout=60))

    def test_config_linux_pptp_client_chap_secrets(self):
        """
        Description: test config_linux_pptp_client_chap_secrets
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none
        self.assertRaises(Exception, self.linux.config_linux_pptp_client_chap_secrets)
        # normal test
        self.assertTrue(self.linux.config_linux_pptp_client_chap_secrets(device=self.device, chap_secrets_file="111", chap_secrets_file_bak="222", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))

    def test_config_linux_pptp_client_peers(self):
        """
        Description: test config_linux_pptp_client_peers
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none
        self.assertRaises(Exception, self.linux.config_linux_pptp_client_peers)
        # normal test
        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", peers_file_bak="222", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client_peers(device=self.device, peers_file="111", timeout=60))

    def test_config_linux_pptp_server_options(self):
        """
        Description: test config_linux_pptp_server_options
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none
        self.assertRaises(Exception, self.linux.config_linux_pptp_server_options)
        # normal test
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_options(device=self.device, option_file="111", timeout=60))

    def test_config_linux_pptp_server_pptpd(self):
        """
        Description: test config_linux_pptp_server_pptpd
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none"""
        self.assertRaises(Exception, self.linux.config_linux_pptp_server_pptpd)
        # normal test
        self.assertTrue(self.linux.config_linux_pptp_server_pptpd(device=self.device, pptpd_file="111", pptpd_file_bak="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_pptpd(device=self.device, pptpd_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_pptpd(device=self.device, pptpd_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_pptpd(device=self.device, pptpd_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_pptpd(device=self.device, pptpd_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_server_pptpd(device=self.device, pptpd_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_pptpd(device=self.device, pptpd_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_pptpd(device=self.device, pptpd_file="111", timeout=60))

    def test_config_linux_pptp_server_chap_secrets(self):
        """
        Description: test config_linux_pptp_server_chap_secrets
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none
        self.assertRaises(Exception, self.linux.config_linux_pptp_server_chap_secrets)
        # normal test
        self.assertTrue(self.linux.config_linux_pptp_server_chap_secrets(device=self.device, chap_secrets_file="111", chap_secrets_file_bak="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_server_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_server_chap_secrets(device=self.device, chap_secrets_file="111", timeout=60))

    def config_linux_pptp_client(self):
        """
        Description: test config_linux_pptp_client
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none
        self.assertRaises(Exception, self.linux.config_linux_pptp_server_pptpd, device=self.device)
        # normal test
        self.assertRaises(Exception, self.config_linux_pptp_client)
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", chap_secrets_file_bak="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))

    def test_set_linux_service_pptp_status(self):
        """
        Description: test set_linux_service_pptp_status
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none
        self.assertRaises(Exception, self.linux.set_linux_service_pptp_status)

        # can not find 0.0.0.0:1723 in response
        self.device.shell().response.side_effect = ["No such file or directory", "Entries have been built", ""]
        self.assertRaises(Exception, self.linux.set_linux_service_pptp_status, device=self.device, timeout=60)
        # can find 0.0.0.0:1723 in response
        self.device.shell().response.side_effect = ["0.0.0.0:1723"]
        self.assertTrue(self.linux.set_linux_service_pptp_status(device=self.device, timeout=60))

    def test_config_linux_pptp_client(self):
        """
        Description: test config_linux_pptp_client
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none
        self.assertRaises(Exception, self.linux.config_linux_pptp_client)

        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", chap_secrets_file_bak="222", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))

        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))
        self.assertTrue(self.linux.config_linux_pptp_client(device=self.device, chap_secrets_file="111", timeout=60))

    @mock.patch("time.sleep", return_value=None)
    def test_send_linux_pptp(self, mock_sleep):
        """
        Description: test send_linux_pptp
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        # device is none
        self.assertRaises(Exception, self.linux.send_linux_pptp)

        # device is none
        self.device.shell().response.side_effect = ["No such file or directory", "Entries have been built", ""]
        self.assertRaises(Exception, self.linux.send_linux_pptp, device=self.device, timeout=60)

        # normal test
        self.device.shell().response.side_effect = [" ppp0 ", " ppp0 ", " ppp0 "]
        self.assertTrue(self.linux.send_linux_pptp(device=self.device, timeout=60))
        self.assertTrue(self.linux.send_linux_pptp(device=self.device, operator="pon", timeout=60))
        self.assertTrue(self.linux.send_linux_pptp(device=self.device, operator="poff", timeout=60))


if __name__ == '__main__':
    unittest.main()
