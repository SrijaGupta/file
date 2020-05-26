import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.zones import zones
from jnpr.toby.hldcl.juniper.security.srx import Srx

class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_configure_zone_0(self):
        self.assertRaises(Exception, zones.configure_zone, zone=" ")
        self.assertRaises(Exception, zones.configure_zone, device=self.mocked_obj)
    def test_configure_zone_1(self):
        system_service = [" ", " "]
        protocol = [" ", " "]
        self.mocked_obj.config = MagicMock()
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", interface="ge-0/0/1", host_inbound_traffic=True, system_service="all"), True)
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", interface="ge-0/0/1", host_inbound_traffic=True, protocol="all"), True)
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", interface="ge-0/0/1", host_inbound_traffic=True, system_service=system_service), True)
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", interface="ge-0/0/1", host_inbound_traffic=True, protocol=protocol), True)
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", address_book=" ", address="trust_a_v4_spec_0", ip_prefix="10.0.0.1/32"), True)
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", address_book=" ", address="trust_a_v4_spec_0", dns_name=" "), True)
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", address_book=" ", address="trust_a_v4_spec_0", range_address_low=" ", range_address_high=" "), True)
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", address_book=" ", address="trust_a_v4_spec_0", wildcard_address=" "), True)
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", address_book=" ", address="trust_a_v4_spec_0", address_set=" "), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(zones.configure_zone(device=self.mocked_obj, zone="trust", commit=True), True)

if __name__ == '__main__':
    unittest.main()