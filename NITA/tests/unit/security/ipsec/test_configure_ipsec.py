import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.ipsec import configure_ipsec
from jnpr.toby.hldcl.juniper.security.srx import Srx


class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_configure_ipsec_0(self):
        self.assertRaises(Exception, configure_ipsec.configure_ipsec)
        self.assertRaises(Exception, configure_ipsec.configure_ipsec, device=self.mocked_obj, vpn='vpn1')

    def test_configure_ipsec_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(configure_ipsec.configure_ipsec(device=self.mocked_obj,
                                                         policy=' ', policy_proposal=' ', policy_proposal_set=' ',
                                                         pfs_keys=' ',
                                                         proposal=' ', auth_algo=' ', enc_algo=' ', lifetime_kb=' ',
                                                         lifetime_sec=' ', protocol=' ',
                                                         security_association=' ',
                                                         vpn=' ', bind_interface=' ', copy_outer_dscp=True,
                                                         df_bit=' ', establish_tunnels=' ',
                                                         ike_gateway=' ', ike_idle_time=' ',
                                                         ike_install_interval=' ', ike_ipsec_policy=' ',
                                                         ike_no_anti_replay=True, ike_proxy_id=' ', manual=' ',
                                                         traffic_selector=' ', local_ip=' ', remote_ip=' ',
                                                         vpn_monitor_optimized=' ', vpn_monitor_dst_ip=' ',
                                                         vpn_monitor_src_interface=' ',
                                                         vpn_monitor_interval=' ', vpn_monitor_threshold=' '), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(configure_ipsec.configure_ipsec(device=self.mocked_obj,
                                                         policy=' ', policy_proposal=' ', policy_proposal_set=' ',
                                                         pfs_keys=' ',
                                                         proposal=' ', auth_algo=' ', enc_algo=' ', lifetime_kb=' ',
                                                         lifetime_sec=' ', protocol=' ',
                                                         security_association=' ',
                                                         vpn=' ', bind_interface=' ', copy_outer_dscp=True,
                                                         df_bit=' ', establish_tunnels=' ',
                                                         ike_gateway=' ', ike_idle_time=' ',
                                                         ike_install_interval=' ', ike_ipsec_policy=' ',
                                                         ike_no_anti_replay=True, ike_proxy_id=' ', manual=' ',
                                                         traffic_selector=' ', local_ip=' ', remote_ip=' ',
                                                         vpn_monitor_optimized=' ', vpn_monitor_dst_ip=' ',
                                                         vpn_monitor_src_interface=' ',
                                                         vpn_monitor_interval=' ', vpn_monitor_threshold=' ',
                                                         commit=True), True)

if __name__ == '__main__':
    unittest.main()

# UT will be completed in a month from date of commit.
