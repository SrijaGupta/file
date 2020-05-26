#!/usr/local/bin/python3

from mock import patch
from mock import MagicMock
from mock import Mock
import logging
import unittest
import unittest2 as unittest

from jnpr.toby.utils import iputils
from jnpr.toby.utils.ipaddressutils import __ip_to_int as ip_to_int
from jnpr.toby.utils.ipaddressutils import mask2cidr

class test_ipaddressutils(unittest.TestCase):
    def setUp(self):
        logging.info("\n##################################################\n")

    def tearDown(self):
        logging.info("\n##################################################\n")

    def test_ip_to_int(self):
        logging.info(".........Test : ip_to_int ............")
        ###################################################################
        logging.info("Test case 1: convert pass")
        ip = '192.168.1.1'
        expected = 3232235777
        test = ip_to_int(ip)
        self.assertEqual(test, expected, "string is not equal")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 2: convert fail")
        ip = '192.168.1'
        expected = None
        test = ip_to_int(ip)
        self.assertEqual(test, expected, "string is not equal")
        logging.info("\tPassed")

    def test_mask2cidr(self):
        logging.info(".........Test : mask2cidr ............")
        ###################################################################
        logging.info("Test case 1: convert pass")
        ip = '255.255.255.255'
        expected = 32
        test = mask2cidr(ip)
        self.assertEqual(test, expected, "cidr is not equal as expectation")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 2: convert fail")
        ip = '0.0.0.0'
        expected = 0
        test = mask2cidr(ip)
        self.assertEqual(test, expected, "cidr is not equal as expectation")
        logging.info("\tPassed")

if __name__ == '__main__':
    unittest.main()
