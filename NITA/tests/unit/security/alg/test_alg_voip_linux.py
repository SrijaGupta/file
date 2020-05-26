#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test Linux VoIP ALG keywords
Author: Vincent Wang, wangdn@juniper.net
"""

import unittest
import mock

from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.alg.alg_voip_linux import alg_voip_linux

# pylint: disable=line-too-long
# pylint: disable=invalid-name


class test_alg_voip_linux(unittest.TestCase):
    """
    Description: Linux userfw keywords unit test
    """
    def setUp(self):
        """
        Description: setUp unit test
        """
        self.device = mock.Mock()(spec=UnixHost)
        self.device.log = mock.Mock()
        self.linux = alg_voip_linux()

    def test_config_linux_service_opensips(self):
        """
        Author: Vincent Wang, wangdn@juniper.net
        Description: config_linux_service_opensips unit test
        """
        # device is none
        self.assertRaises(Exception, self.linux.config_linux_service_opensips)
        # ip_list is none
        self.assertRaises(Exception, self.linux.config_linux_service_opensips, device=self.device)
        # one ip address in ip_list and protocol is udp
        self.assertTrue(self.linux.config_linux_service_opensips(device=self.device, ip_list=("1.1.1.1", )))
        # three ip addresses in ip_list and protocol is tcp
        self.assertTrue(self.linux.config_linux_service_opensips(device=self.device, ip_list=("1.1.1.1", "1.1.1.2", "2000::1:1"), protocol="tcp"))

    def test_set_linux_service_opensips_status(self):
        """
        Author: Vincent Wang, wangdn@juniper.net
        Description: config_linux_service_opensips unit test
        """
        # device is none
        self.assertRaises(Exception, self.linux.set_linux_service_opensips_status)
        # return started in response when set service restart
        self.device.shell().response.return_value = "INFO: started (pid: 19991)"
        self.assertTrue(self.linux.set_linux_service_opensips_status(device=self.device))

        # return OpenSIPS already runningp in response
        self.device.shell().response.return_value = "INFO: PID file exists (/var/run/opensips.pid)! OpenSIPS already running?"
        self.assertTrue(self.linux.set_linux_service_opensips_status(device=self.device, operator="start"))

        # return OpenSIPS stop
        self.device.shell().response.return_value = "INFO: stopped"
        self.assertTrue(self.linux.set_linux_service_opensips_status(device=self.device, operator="stop"))
        # return other info
        self.device.shell().response.return_value = "ERROR: PID file /var/run/opensips.pid does not exist -- OpenSIPS start failed"
        self.assertRaises(Exception, self.linux.set_linux_service_opensips_status, device=self.device, operator="start")

    def test_config_linux_linphone(self):
        """
        Author: Vincent Wang, wangdn@juniper.net
        Description: config_linux_linphone unit test
        """

        # device is none
        self.assertRaises(Exception, self.linux.config_linux_linphone)
        # phone_number is none or proxy_addr is none
        self.assertRaises(Exception, self.linux.config_linux_linphone, device=self.device)
        self.assertRaises(Exception, self.linux.config_linux_linphone, device=self.device, phone_number="8000")

        # proxy is IPv4 address and protocol is UDP
        self.assertTrue(self.linux.config_linux_linphone(device=self.device, phone_number="8000", proxy_address="20.0.172.170"))
        # proxy is IPv6 address and protocol is TCP
        self.assertTrue(self.linux.config_linux_linphone(device=self.device, phone_number="8000", proxy_address="2000::172:170", protocol="tcp", expires="300"))

    def test_run_linux_linphone(self):
        """
        Author: Vincent Wang, wangdn@juniper.net
        Description: run_linux_linphone unit test
        """
        # device is none
        self.assertRaises(Exception, self.linux.run_linux_linphone)
        # return refused in response
        self.device.shell().response.return_value = "ALSA lib pulse.c:229:(pulse_connect) PulseAudio: Unable to connect: Connection refused"
        self.assertRaises(Exception, self.linux.run_linux_linphone, device=self.device)
        # return No such file in response
        self.device.shell().response.return_value = "-bash: linphonerc: command not found, No such file"
        self.assertRaises(Exception, self.linux.run_linux_linphone, device=self.device)
        # return Cannot in response
        self.device.shell().response.return_value = "Cannot open config file"
        self.assertRaises(Exception, self.linux.run_linux_linphone, device=self.device)
        # return Ready in response
        self.device.shell().response.return_value = "Ready"
        self.assertTrue(self.linux.run_linux_linphone(device=self.device, config='/root/.linphonerc_ipv4', log='/root/linphone_ipv4.log', option='-d 6'))
        # return other info in response
        self.device.shell().response.return_value = "-bash: linphonec: command not found"
        self.assertRaises(Exception, self.linux.run_linux_linphone, device=self.device)

    def test_execute_command_on_linux_linphone(self):
        """
        Author: Vincent Wang, wangdn@juniper.net
        Description: execute_command_on_linux_linphone unit test
        """
        # device is none
        self.assertRaises(Exception, self.linux.execute_command_on_linux_linphone)
        # command is none
        self.assertRaises(Exception, self.linux.execute_command_on_linux_linphone, device=self.device)
        # return response for the command
        self.device.shell().response.return_value = "Establishing call id to <sip:8001@20.0.172.170>, assigned id 1"
        self.assertEqual(self.linux.execute_command_on_linux_linphone(device=self.device, command='call 8001'), "Establishing call id to <sip:8001@20.0.172.170>, assigned id 1")

    def test_stop_linux_linphone(self):
        """
        Author: Vincent Wang, wangdn@juniper.net
        Description: stop_linux_linphone unit test
        """
        # device is none
        self.assertRaises(Exception, self.linux.stop_linux_linphone)
        # return Terminating in response
        self.device.shell().response.return_value = "Terminating..."
        self.assertTrue(self.linux.stop_linux_linphone(device=self.device))
        # return other info in response
        self.device.shell().response.return_value = "Failed"
        self.assertRaises(Exception, self.linux.stop_linux_linphone, device=self.device)


if __name__ == '__main__':
    unittest.main()
