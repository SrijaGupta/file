#! /usr/local/bin/python3

from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.hldcl.juniper.junos import Juniper
import jnpr.toby.utils.junos.interface_utils 



class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=Juniper)
    mocked_obj.log = MagicMock()
    mocked_obj.cli = MagicMock()

    def test_get_interface_hardware_address_exception(self):
        try:
           interface_utils.get_interface_hardware_address() 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Device handle is a mandatory argument")

        try:
           interface_utils.get_interface_hardware_address(device=self.mocked_obj) 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "interface is a mandatory argument")

    def test_get_interface_hardware_address_execution_1(self):
        lst = [Response("Hardware address: 44:f4:77:92:58:b4")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(interface_utils.get_interface_hardware_address(device=self.mocked_obj, interface="xe-2/2/0"), 
                         "44:f4:77:92:58:b4")

    def test_get_interface_hardware_address_execution_2(self):
        lst = [Response("Hardware address suchi: 44:f4:77:92:58:b4")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        try:
            interface_utils.get_interface_hardware_address(device=self.mocked_obj, interface="xe-2/2/0")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Couldn't find the hardware address of interface xe-2/2/0")


if __name__ == '__main__':
    unittest.main()
