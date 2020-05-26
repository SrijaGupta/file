
from mock import patch
from mock import MagicMock

import unittest2 as unittest
import unittest
import builtins
from jnpr.toby.utils.macutils import generate_mac_addresses

class TestTime(unittest.TestCase):

    def test_generate_mac_addresses(self):

        mac = "00:00:00:11:11:01"
        num = 5

        exp_return_list = [
            "00:00:00:11:11:01",
            "00:00:00:11:11:02",
            "00:00:00:11:11:03",
            "00:00:00:11:11:04",
            "00:00:00:11:11:05",
        ]

        self.assertEqual(generate_mac_addresses(first_mac=mac,number_of_macs=num), exp_return_list)

    def test_generate_mac_addresses_bad_mac(self):

        mac = "00:00:00:11:11"
        num = 5

        exp_return_list = [
            "00:00:00:11:11:01",
            "00:00:00:11:11:02",
            "00:00:00:11:11:03",
            "00:00:00:11:11:04",
            "00:00:00:11:11:05",
        ]

        try:
            self.assertEqual(generate_mac_addresses(first_mac=mac,number_of_macs=num), exp_return_list)
        except Exception as err:
            self.assertIn("not a valid mac", err.args[0])

    def test_generate_mac_addresses_bad_num(self):

        mac = "00:00:00:11:11:01"
        num = -10

        exp_return_list = [
            "00:00:00:11:11:01",
            "00:00:00:11:11:02",
            "00:00:00:11:11:03",
            "00:00:00:11:11:04",
            "00:00:00:11:11:05",
        ]

        try:
            self.assertEqual(generate_mac_addresses(first_mac=mac,number_of_macs=num), exp_return_list)
        except Exception as err:
            self.assertIn("must be greater than 0", err.args[0])

#    def test_generate_mac_addresses_beyond_range(self):
#
#        mac = "ff:ff:ff:ff:ff:f0"
#        num = 20
#
#        exp_return_list = [
#            "ff:ff:ff:ff:ff:f0",
#            "ff:ff:ff:ff:ff:f1",
#            "ff:ff:ff:ff:ff:f2",
#            "ff:ff:ff:ff:ff:f3",
#            "ff:ff:ff:ff:ff:f4",
#            "ff:ff:ff:ff:ff:f5",
#            "ff:ff:ff:ff:ff:f6",
#            "ff:ff:ff:ff:ff:f7",
#            "ff:ff:ff:ff:ff:f8",
#            "ff:ff:ff:ff:ff:f9",
#            "ff:ff:ff:ff:ff:fa",
#            "ff:ff:ff:ff:ff:fb",
#            "ff:ff:ff:ff:ff:fc",
#            "ff:ff:ff:ff:ff:fd",
#            "ff:ff:ff:ff:ff:fe",
#            "ff:ff:ff:ff:ff:ff",
#        ]
#
#        try:
#            self.assertEqual(generate_mac_addresses(first_mac=mac,number_of_macs=num), exp_return_list)
#        except Exception as err:
#            self.assertIn("hit the end limit", err.args[0])


if __name__ =='__main__':
    unittest.main()
