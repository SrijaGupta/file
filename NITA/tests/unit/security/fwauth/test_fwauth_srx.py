#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test fwauth srx keywords
Author: Linjing Liu, ljliu@juniper.net
"""

import unittest
import mock

from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem
from jnpr.toby.security.fwauth.fwauth_srx import fwauth_srx

# pylint: disable=line-too-long
# pylint: disable=invalid-name


class test_fwauth_srx(unittest.TestCase):
    """Description: userfw srx keywords unit test"""
    def setUp(self):
        """setup before all case"""
        self.fwauth_srx = fwauth_srx()
        self.device = mock.Mock()(spec=SrxSystem)
        self.device.log = mock.Mock()

    def tearDown(self):
        """teardown after all case"""
        pass

    def test_check_srx_firewall_auth_jims_statistics(self):
        """
        Author: Linjing Liu, ljliu@juniper.net
        Description: test_check_srx_firewall_auth_jims_statistics unit test
        """

        # device is none
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_jims_statistics, device=None)
        # value is none
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_jims_statistics, value=None)

        self.device.cli().response.return_value = "Push success counter:  6 \r\n Push failure counter:  5"
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_jims_statistics(device=self.device, field="success", value=6))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_jims_statistics, device=self.device, field="success", value=4)
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_jims_statistics(device=self.device, field="fail", value=5))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_jims_statistics, device=self.device, field="fail", value=3)

    def test_clear_srx_firewall_auth_jims_statistics(self):
        """
        Author: Linjing Liu, ljliu@juniper.net
        Description: test_clear_srx_firewall_auth_jims_statistics unit test
        """

        # device is none
        self.assertRaises(Exception, self.fwauth_srx.clear_srx_firewall_auth_jims_statistics, device=None)
        # normal test
        self.assertTrue(self.fwauth_srx.clear_srx_firewall_auth_jims_statistics(device=self.device))

    def test_check_srx_firewall_auth_table(self):
        """
        Author: Linjing Liu, ljliu@juniper.net
        Description: check_srx_firewall_auth_table unit test
        """

        # device is none
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=None)

        self.device.cli().response.return_value = "Username: test\r\n Source IP: 1.1.1.1\r\n Authentication state: Success\r\n \
                                    Authentication method: passthrough\r\n Lsys: lsysa\r\n \
                                    Source zone: zone1\r\n Destination zone: zone2\r\n \
                                    Access profile: myprofile\r\n Client-groups: mygroup"
        # input ip doesn't match get ip
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, ip="1.1.2.2")

        # normal test
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table(device=self.device, ip="1.1.1.1"))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, logical_system="lsysa", ip="1.1.1.1", no_entry=True)
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table(device=self.device, logical_system="lsysa", ip="1.1.1.2", no_entry=True))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, logical_system="lsysa", ip="1.1.1.1", profile="ddd")
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, ip="1.1.1.1", logical_system="lsysa", username="aaa")
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table(device=self.device, ip="1.1.1.1", status="Success", logical_system="lsysa"))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, username="test", profile="myprofile", ip="1.1.1.1", logical_system="lsysb")
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table(device=self.device, username="test", profile="myprofile", ip="1.1.1.1"))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, status="Fail", profile="myprofile", method="passthrough", ip="1.1.1.1")
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table(device=self.device, status="Success", profile="myprofile", src_zone="zone1", dst_zone="zone2", client_groups="mygroup", logical_system="lsysa", ip="1.1.1.1"))

        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table(device=self.device, node='0', logical_system="lsysa", ip="1.1.1.2", no_entry=True))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, node='0', logical_system="lsysa", ip="1.1.1.1", method="webauth")
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, node='0', username="test", profile="myprofile", ip="1.1.1.1", src_zone="aaa")
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, node='0', username="test", client_groups="wronggroup", ip="1.1.1.1")
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table(device=self.device, node='0', status="Success", profile="myprofile", src_zone="zone1", dst_zone="zone2", logical_system="lsysa", ip="1.1.1.1"))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table, device=self.device, node='0', status="Success", method="passthrough", profile="myprofile", ip="1.1.1.1", dst_zone="dstzone")
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table(device=self.device, node='0', status="Success", method="passthrough", client_groups="mygroup", ip="1.1.1.1"))

    def test_check_srx_firewall_auth_table_on_pfe(self):
        """
        Author: Linjing Liu, ljliu@juniper.net
        Description: check_srx_firewall_auth_table_on_pfe unit test
        """

        # device is none
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=None)
        self.fwauth_srx.dut.send_vty_cmd = mock.Mock()
        self.fwauth_srx.dut.send_vty_cmd.return_value = "3 1.0.0.10        test1            4 Success  local_p P root_tr root_un"
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=self.device, ip='1.0.0.10')
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table_on_pfe(device=self.device, ip="1.1.1.1", no_entry=True))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=self.device, ip='1.0.0.10', no_entry=True, node=0)
        self.fwauth_srx.dut.send_vty_cmd.return_value = "Source IP: 1.0.0.10\r\n access profile: local_pf \r\n Username: test1 \r\n Groups List:  local-group1 local-group2\r\n Status: Success \r\n Zone: root_trust->root_untrust\r\n"
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table_on_pfe(device=self.device, ip="1.0.0.10", username="test1", profile="local_pf", status="Success", client_groups="local-group1", src_zone="root_trust", dst_zone="root_untrust"))
        self.assertTrue(self.fwauth_srx.check_srx_firewall_auth_table_on_pfe(device=self.device, ip="1.0.0.10", username="test1", profile="local_pf", status="Success"))
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=self.device, ip='1.0.0.10', username="ddd", node=0)
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=self.device, ip='1.0.0.10', client_groups="ddd", node=0)
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=self.device, ip='1.0.0.10', status="ddd", node=0)
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=self.device, ip='1.0.0.10', profile="ddd", node=0)
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=self.device, ip='1.0.0.10', src_zone="ddd", node=0)
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=self.device, ip='1.0.0.10', dst_zone="ddd", node=0)
        self.assertRaises(Exception, self.fwauth_srx.check_srx_firewall_auth_table_on_pfe, device=self.device, ip='1.2.0.10', node=0)


if __name__ == '__main__':
    unittest.main()
