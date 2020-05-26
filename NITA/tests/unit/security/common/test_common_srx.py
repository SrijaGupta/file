#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test common srx keywords
Author: Ruby Wu, rubywu@juniper.net
"""

import unittest
import mock

from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem
from jnpr.toby.security.common.common_srx import common_srx

# pylint: disable=line-too-long
# pylint: disable=invalid-name


class test_common_srx(unittest.TestCase):
    """
    Description: common srx keywords unit test
    """
    def setUp(self):
        """
        Description: setUp unit test
        """
        self.device = mock.Mock()(spec=SrxSystem)
        self.device.log = mock.Mock()
        self.srx = common_srx()

    def test_clear_srx_security_pki_local_certificate(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: clear_srx_security_pki_local_certificate unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.clear_srx_security_pki_local_certificate)

        # normal test
        self.assertTrue(self.srx.clear_srx_security_pki_local_certificate(device=self.device))
        self.assertTrue(self.srx.clear_srx_security_pki_local_certificate(device=self.device, file='certificate_file'))

    def test_config_srx_security_pki_local_certificate(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: config_srx_security_pki_local_certificate unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.config_srx_security_pki_local_certificate)

        # generate key pair failed
        self.device.cli().response.return_value = "key pair failed"
        self.assertRaises(Exception, self.srx.config_srx_security_pki_local_certificate, device=self.device)
        # generate self signed certificate id failed
        self.device.cli().response.side_effect = ["Generated key pair cert_file, key size 2048 bits", "certificate generated and loaded failed"]
        self.assertRaises(Exception, self.srx.config_srx_security_pki_local_certificate, device=self.device)

        # normal test
        self.device.cli().response.side_effect = ["Generated key pair cert_file, key size 2048 bits", "Self-signed certificate generated and loaded successfully", "Generated key pair aruba, key size 1024 bits", "Self-signed certificate generated and loaded successfully"]
        self.assertTrue(self.srx.config_srx_security_pki_local_certificate(device=self.device))
        self.assertTrue(self.srx.config_srx_security_pki_local_certificate(device=self.device, file="aruba", size=1024, domain="test.com", email="123@juniper.net", ip="2.2.2.2", subject="CN=test,OU=Sales,O=Juniper,L=Sunnyvale,ST=CA,C=US"))

    def test_config_srx_system_login(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: config_srx_system_login unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.config_srx_system_login)
        # uid is unexcepted value
        self.device.config().response.return_value = "uid is unexcepted value"
        self.assertRaises(Exception, self.srx.config_srx_system_login, device=self.device, uid='50')

        self.device.config().response.side_effect = ["error: minimum password length is 6", " ", "error: Passwords are not equal"]
        # password doesn't satisfy specific rule
        self.assertRaises(Exception, self.srx.config_srx_system_login, device=self.device)

        # normal test
        self.device.config().response.side_effect = [" ", " ", " ", " ", " ", " ", " ", " "]
        self.assertTrue(self.srx.config_srx_system_login(device=self.device, flag='class'))
        self.assertTrue(self.srx.config_srx_system_login(device=self.device, flag='user', commit=True))
        self.assertTrue(self.srx.config_srx_system_login(device=self.device))
        self.assertTrue(self.srx.config_srx_system_login(device=self.device, class_name='class_test', logical_system='logic_test', permissions='test', user='ld', full_name='fn', uid='500', password='Netscreen1'))

    def test_delete_srx_system_login(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: delete_srx_system_login unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.delete_srx_system_login)

        # normal test
        self.assertTrue(self.srx.delete_srx_system_login(device=self.device, class_name='class', user='user'))
        self.assertTrue(self.srx.delete_srx_system_login(device=self.device, class_name='class', logical_system='logic_test', commit=True))
        self.assertTrue(self.srx.delete_srx_system_login(device=self.device, class_name='class', permissions='test'))
        self.assertTrue(self.srx.delete_srx_system_login(device=self.device, class_name='class'))
        self.assertTrue(self.srx.delete_srx_system_login(device=self.device, user='ld', full_name='fn'))
        self.assertTrue(self.srx.delete_srx_system_login(device=self.device, user='ld', uid='500'))
        self.assertTrue(self.srx.delete_srx_system_login(device=self.device, user='ld'))
        self.assertTrue(self.srx.delete_srx_system_login(device=self.device))

    def test_config_srx_system_process_multitenancy(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: config_srx_system_process_multitenancy unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.config_srx_system_process_multitenancy)
        # normal test
        self.assertTrue(self.srx.config_srx_system_process_multitenancy(device=self.device))
        self.assertTrue(self.srx.config_srx_system_process_multitenancy(device=self.device, commit=True))

    def test_delete_srx_system_process_multitenancy(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: delete_srx_system_process_multitenancy unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.delete_srx_system_process_multitenancy)
        # normal test
        self.assertTrue(self.srx.delete_srx_system_process_multitenancy(device=self.device))
        self.assertTrue(self.srx.delete_srx_system_process_multitenancy(device=self.device, commit=True))

    def test_config_srx_lsys0(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: config_srx_lsys0 unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.config_srx_lsys0)
        # unit and peer_unit shouldn't be equal
        self.assertRaises(Exception, self.srx.config_srx_lsys0, device=self.device, unit='50', peer_unit='50')

        # normal test
        self.assertTrue(self.srx.config_srx_lsys0(device=self.device))
        self.assertTrue(self.srx.config_srx_lsys0(device=self.device, commit=True))
        self.assertTrue(self.srx.config_srx_lsys0(device=self.device, interfaces='lt-0/0/1', unit='50', peer_unit='51', routing_instances='vr_test', commit=True))
        self.assertTrue(self.srx.config_srx_lsys0(device=self.device, flag='interfaces'))
        self.assertTrue(self.srx.config_srx_lsys0(device=self.device, flag='instances', unit='50', peer_unit='51'))

    def test_delete_srx_lsys0(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: delete_srx_lsys0 unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.delete_srx_lsys0)

        # normal test
        self.assertTrue(self.srx.delete_srx_lsys0(device=self.device, commit=True))
        self.assertTrue(self.srx.delete_srx_lsys0(device=self.device, routing_instances='vr_test', interfaces='lt-0/0/0', unit='21'))
        self.assertTrue(self.srx.delete_srx_lsys0(device=self.device, routing_instances='vr_test'))
        self.assertTrue(self.srx.delete_srx_lsys0(device=self.device, interfaces='lt-0/0/0', unit='21', peer_unit='20'))
        self.assertTrue(self.srx.delete_srx_lsys0(device=self.device, interfaces='lt-0/0/0', unit='21'))
        self.assertTrue(self.srx.delete_srx_lsys0(device=self.device, interfaces='lt-0/0/0'))

    def test_config_srx_interface_ip_address(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: config_srx_interface_ip_address unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.config_srx_interface_ip_address)

        # normal test
        self.assertTrue(self.srx.config_srx_interface_ip_address(device=self.device, logical_systems='ld2', interface='lt-0/0/0', unit='1', ip='19.0.0.1', peer_unit='20'))
        self.assertTrue(self.srx.config_srx_interface_ip_address(device=self.device, logical_systems='ld3', interface='lt-0/0/0', unit='2', ip='19::1', peer_unit='22', inet='inet6', mask='64'))
        self.assertTrue(self.srx.config_srx_interface_ip_address(device=self.device, interface='lt-0/0/0', unit='1', ip='9.0.0.1', peer_unit='101'))
        self.assertTrue(self.srx.config_srx_interface_ip_address(device=self.device, interface='lt-0/0/0', unit='1', ip='9::1', peer_unit='102', inet='inet6', mask='64'))
        self.assertTrue(self.srx.config_srx_interface_ip_address(device=self.device, interface='ge-0/0/0', unit='1', ip='60.60.60.1', commit=True))
        self.assertTrue(self.srx.config_srx_interface_ip_address(device=self.device, logical_systems='ld2', interface='ge-0/0/0', unit='2', ip='70.60.60.1'))
        self.assertTrue(self.srx.config_srx_interface_ip_address(device=self.device, logical_systems='ld2', interface='ge-0/0/0', unit='2', ip='70.60.60.1', web_authentication='https'))

    def test_config_srx_static_route(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: config_srx_static_route unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.config_srx_static_route)

        # normal test
        self.assertTrue(self.srx.config_srx_static_route(device=self.device, logical_systems='ld2', subnet='2.2.2.0', nexthop='19.0.0.1'))
        self.assertTrue(self.srx.config_srx_static_route(device=self.device, subnet='2.2.2.0', mask='16', nexthop='19.0.0.1', commit=True))
        self.assertTrue(self.srx.config_srx_static_route(device=self.device, logical_systems='ld2', subnet='2::2', nexthop='19::1'))
        self.assertTrue(self.srx.config_srx_static_route(device=self.device, subnet='2::2', mask='64', nexthop='19::1', commit=True))

    def test_delete_srx_static_route(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: delete_srx_static_route unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.delete_srx_static_route)

        # normal test
        self.assertTrue(self.srx.delete_srx_static_route(device=self.device, logical_systems='ld2', subnet='2.2.2.0'))
        self.assertTrue(self.srx.delete_srx_static_route(device=self.device, subnet='2.2.2.0', mask='16', commit=True))
        self.assertTrue(self.srx.delete_srx_static_route(device=self.device, logical_systems='ld2', subnet='2::0'))
        self.assertTrue(self.srx.delete_srx_static_route(device=self.device, subnet='2::0', mask='16', commit=True))
        self.assertTrue(self.srx.delete_srx_static_route(device=self.device, flag='ipv4'))
        self.assertTrue(self.srx.delete_srx_static_route(device=self.device, flag='ipv6'))
        self.assertTrue(self.srx.delete_srx_static_route(device=self.device, flag='ipv6', logical_systems='ld2'))
        self.assertTrue(self.srx.delete_srx_static_route(device=self.device, logical_systems='ld2'))
        self.assertTrue(self.srx.delete_srx_static_route(device=self.device))

    def test_config_srx_system_security_profile(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: config_srx_system_security_profile unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.config_srx_system_security_profile)

        # normal test
        self.assertTrue(self.srx.config_srx_system_security_profile(device=self.device))
        self.assertTrue(self.srx.config_srx_system_security_profile(device=self.device, logical_systems='ld2', commit=True))
        self.assertTrue(self.srx.config_srx_system_security_profile(device=self.device, security_profile='p1', logical_systems='ld2', logical_systems_number='10'))

    def test_delete_srx_system_security_profile(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: delete_srx_system_security_profile unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.delete_srx_system_security_profile)

        # normal test
        self.assertTrue(self.srx.delete_srx_system_security_profile(device=self.device))
        self.assertTrue(self.srx.delete_srx_system_security_profile(device=self.device, security_profile='p1', commit=True))
        self.assertTrue(self.srx.delete_srx_system_security_profile(device=self.device, security_profile='p1', logical_systems='ld2'))

    def test_check_srx_system_license(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: check_srx_system_license unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.check_srx_system_license)
        # feature_name is none
        self.assertRaises(Exception, self.srx.check_srx_system_license, device=self.device)

        self.device.cli().response.side_effect = ["logical-system 1 20 0 permanent\r\n", "logical-system 1 60 0 invalid\r\n"]
        # input licenses installed number is less than get licenses installed number, this's unexpected
        self.assertRaises(Exception, self.srx.check_srx_system_license, device=self.device, feature_name='logical-system', licenses_installed=30)
        # licenses doesn't work, please check it
        self.assertRaises(Exception, self.srx.check_srx_system_license, device=self.device, feature_name='logical-system', licenses_installed=30)

        # normal test
        self.device.cli().response.side_effect = ["logical-system 1 3 0 permanent\r\n", "logical-system 1 30 0 permanent\r\n"]
        self.assertTrue(self.srx.check_srx_system_license(device=self.device, feature_name='logical-system'))
        self.assertTrue(self.srx.check_srx_system_license(device=self.device, feature_name='logical-system', licenses_installed=30))

    def test_check_srx_system_processes_multitenancy(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: check_srx_system_license unit test
        """

        # device is none
        self.assertRaises(Exception, self.srx.check_srx_system_processes_multitenancy)

        # normal test
        self.device.cli().response.side_effect = ["mode: logical-system ", "mode: logical-domain "]
        self.assertFalse(self.srx.check_srx_system_processes_multitenancy(device=self.device, mode='logical-domain'))
        self.assertTrue(self.srx.check_srx_system_processes_multitenancy(device=self.device, mode='logical-domain'))


if __name__ == '__main__':
    unittest.main()
