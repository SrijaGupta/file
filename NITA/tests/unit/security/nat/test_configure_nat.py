import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.nat import configure_nat
from jnpr.toby.hldcl.juniper.security.srx import Srx


class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_nat_pool_0(self):
        self.assertRaises(Exception, configure_nat.configure_nat_pool, flavour='source', pool='p1')
        self.assertRaises(Exception, configure_nat.configure_nat_pool, device=self.mocked_obj, pool='p1')
        self.assertRaises(Exception, configure_nat.configure_nat_pool, device=self.mocked_obj, flavour='source')
        self.assertRaises(Exception, configure_nat.configure_nat_pool, device=self.mocked_obj, flavour='source',
                          pool='p1')

    def test_nat_pool_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(configure_nat.configure_nat_pool(device=self.mocked_obj,
                                                          flavour='source', pool='p1', address='20.20.20.20/32'), True)
        self.assertEqual(configure_nat.configure_nat_pool(device=self.mocked_obj,
                                                          flavour='source', pool='p1', routing_instance='red'), True)
        self.assertEqual(configure_nat.configure_nat_pool(device=self.mocked_obj,
                                                          flavour='source', pool='p1', port='range 2020 to 2022'), True)
        self.assertEqual(configure_nat.configure_nat_pool(device=self.mocked_obj,
                                                          flavour='source', pool='p1', port=['range 2020 to 2022'],
                                                          overflow_pool=' ', host_address_base=' ',
                                                          address_persistent=True), True)
        self.assertEqual(configure_nat.configure_nat_pool(device=self.mocked_obj,
                                                          flavour='source', pool='p1', address='20.20.20.20/32',
                                                          logical_system='l1'), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(configure_nat.configure_nat_pool(device=self.mocked_obj, flavour='source', pool='p1',
                                                          address='20.20.20.20/32', commit=True), True)

    def test_nat_rule_set_0(self):
        self.assertRaises(Exception, configure_nat.configure_nat_rule_set,
                          flavour='source', rule_set='rs1', rule='r1')
        self.assertRaises(Exception, configure_nat.configure_nat_rule_set,
                          device=self.mocked_obj, rule_set='rs1', rule='r1')
        self.assertRaises(Exception, configure_nat.configure_nat_rule_set,
                          device=self.mocked_obj, flavour='source', rule_set='rs1')
        self.assertRaises(Exception, configure_nat.configure_nat_rule_set,
                          device=self.mocked_obj, flavour='source', rule='r1')
        self.assertRaises(Exception, configure_nat.configure_nat_rule_set,
                          device=self.mocked_obj, flavour='source', rule_set='rs1', rule='r1')

    def test_nat_rule_set_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(configure_nat.configure_nat_rule_set(device=self.mocked_obj, flavour='source', rule_set=' ',
                                                              from_routing_instance=' ', from_interface=' ',
                                                              from_zone=' ', to_routing_instance=' ',
                                                              to_interface=' ', to_zone=' ', rule=' ',
                                                              match_application=' ', match_protocol=' ',
                                                              match_source_address='20.20.20.20/32',
                                                              match_destination_address='20.20.20.20/32',
                                                              match_source_address_name='a1',
                                                              match_destination_address_name='d1',
                                                              then_off=True,
                                                              match_source_port=' ', match_destination_port=' ',
                                                              then_interface=True, then_pool=' ', then_prefix=' ',
                                                              then_prefix_routing_instance=' ', commit=False),
                         True)
        self.assertEqual(configure_nat.configure_nat_rule_set(device=self.mocked_obj, flavour='source', rule_set=' ',
                                                              from_routing_instance=' ', from_interface=' ',
                                                              from_zone=' ', to_routing_instance=' ',
                                                              to_interface=' ', to_zone=' ', rule=' ',
                                                              match_application=' ', match_protocol=' ',
                                                              match_source_address='20.20.20.20/32',
                                                              match_destination_address='20.20.20.20/32',
                                                              match_source_port=' ', match_destination_port=' ',
                                                              then_interface=True, then_pool=' ', then_prefix=' ',
                                                              logical_system='lsys1', commit=False),
                         True)
        self.assertEqual(configure_nat.configure_nat_rule_set(device=self.mocked_obj, flavour='source', rule_set=' ',
                                                              from_routing_instance=' ', from_interface=' ',
                                                              from_zone=' ', to_routing_instance=' ',
                                                              to_interface=' ', to_zone=' ', rule=' ',
                                                              match_application=' ', match_protocol=' ',
                                                              match_source_address='20.20.20.20/32',
                                                              match_destination_address='20.20.20.20/32',
                                                              match_source_port=' ', match_destination_port=' ',
                                                              then_interface=True, then_pool=' ', then_prefix=' ',
                                                              raise_threshold='55', clear_threshold='25',
                                                              logical_system='lsys1', commit=False),
                         True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(configure_nat.configure_nat_rule_set(device=self.mocked_obj, flavour='source', rule_set=' ',
                                                              from_routing_instance=' ', from_interface=' ',
                                                              from_zone=' ', to_routing_instance=' ',
                                                              to_interface=' ', to_zone=' ', rule=' ',
                                                              match_application=' ', match_protocol=' ',
                                                              match_source_address='20.20.20.20/32',
                                                              match_destination_address='20.20.20.20/32',
                                                              match_source_port=' ', match_destination_port=' ',
                                                              then_interface=True, then_pool=' ', then_prefix=' ',
                                                              then_prefix_routing_instance=' ', commit=True),
                         True)


if __name__ == '__main__':
    unittest.main()
