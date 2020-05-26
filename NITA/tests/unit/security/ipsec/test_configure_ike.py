import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.ipsec import configure_ike
from jnpr.toby.hldcl.juniper.security.srx import Srx


class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_configure_ike_0(self):
        self.assertRaises(Exception, configure_ike.configure_ike)
        self.assertRaises(Exception, configure_ike.configure_ike, device=self.mocked_obj, gateway='gw1')

    def test_configure_ike_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(configure_ike.configure_ike(device=self.mocked_obj, gateway=' ', gw_address=' ',
                                                     gw_advpn=' ', gw_dead_peer=' ', gw_dynamic=' ',
                                                     gw_ext_interface=' ', gw_general_ikeid=True, gw_ike_policy=' ',
                                                     gw_local_address=' ', gw_local_id=' ', gw_nat_keepalive=' ',
                                                     gw_no_nat_traversal=True, gw_remote_identity=' ',
                                                     gw_v1_only=True, gw_v2_only=True, gw_xauth_profile=' ',
                                                     policy=' ', certificate=' ', mode=' ', proposal_set=' ',
                                                     proposals=' ', pre_shared_key=' ', reauth_frequency=' ',
                                                     proposal=' ', auth_algo=' ', auth_method=' ', dh_group=' ',
                                                     enc_algo=' ', lifetime_sec=' ', respond_bad_spi=' ',
                                                     commit=False), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(configure_ike.configure_ike(device=self.mocked_obj, gateway=' ', gw_address=' ',
                                                     gw_advpn=' ', gw_dead_peer=' ', gw_dynamic=' ',
                                                     gw_ext_interface=' ', gw_general_ikeid=True, gw_ike_policy=' ',
                                                     gw_local_address=' ', gw_local_id=' ', gw_nat_keepalive=' ',
                                                     gw_no_nat_traversal=True, gw_remote_identity=' ',
                                                     gw_v1_only=True, gw_v2_only=True, gw_xauth_profile=' ',
                                                     policy=' ', certificate=' ', mode=' ', proposal_set=' ',
                                                     proposals=' ', pre_shared_key=' ', reauth_frequency=' ',
                                                     proposal=' ', auth_algo=' ', auth_method=' ', dh_group=' ',
                                                     enc_algo=' ', lifetime_sec=' ', respond_bad_spi=' ',
                                                     commit=True), True)

if __name__ == '__main__':
    unittest.main()

# UT will be completed in a month from date of commit.
