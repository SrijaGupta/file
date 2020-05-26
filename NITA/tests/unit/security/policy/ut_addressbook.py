#! /usr/local/bin/python3

from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.hldcl.juniper.junos import Juniper
import jnpr.toby.security.policy.addressbook 

class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=Juniper)
    mocked_obj.log = MagicMock()
    mocked_obj.cli = MagicMock()

    def test_addressbook_exception_1(self):
        try:
           addressbook.address_book_config() 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Device handle is a mandatory argument")

    def test_address_book_config_execution_1(self):
        lst = [Response("abc")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(addressbook.address_book_config(device=self.mocked_obj, mode="delete"), 
                        None)

    def test_address_book_config_execution_2(self):
        lst = [Response("def")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(addressbook.address_book_config(device=self.mocked_obj, addr_name="addrname", ip_prefix="5.0.0.1/32"),
                        None)

    def test_address_book_config_execution_3(self):
        lst = [Response("ghi")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(addressbook.address_book_config(device=self.mocked_obj, addr_name="dnsname", domain_name="facebook.com"),
                        None)

    def test_address_book_config_exception_2(self):
        lst = [Response("Hardware address suchi: 44:f4:77:92:58:b4")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            addressbook.address_book_config(device=self.mocked_obj, addr_name="dnsname")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Either ip_prefix or domain_name is a mandatory argument for addr_name")

    def test_address_book_config_execution_4(self):
        lst = [Response("ghi")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(addressbook.address_book_config(device=self.mocked_obj, addr_set="addrset", addr_set_name="addrsetname"),
                        None)


    def test_address_book_config_exception_3(self):
        lst = [Response("Hardware address suchi: 44:f4:77:92:58:b4")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            addressbook.address_book_config(device=self.mocked_obj, addr_set="addrset")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "addr_set_name is a mandatory argument for addr_set")


if __name__ == '__main__':
    unittest.main()
