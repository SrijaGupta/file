from mock import patch

import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.interfaces.interfaces import *
from jnpr.toby.hldcl.juniper.security.srx import Srx


# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()



    def test_interfaces_0(self):

        try:
            configure_interface()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a device handle and it is a mandatory parameter ")

    def test_interfaces_1(self):
        
        try:
            configure_interface(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'interface' is a mandatory parameter ")

    def test_interfaces_2(self):
        
        try:
            configure_interface(device=self.mocked_obj,interface=" ")
        except Exception as err:
            self.assertEqual(err.args[0], "'address' is mandatory parameter for configuring basic interface")


    def test_interface_3(self):

        self.mocked_obj.config = MagicMock()
        self.mocked_obj.commit = MagicMock(return_value= 1)

        self.assertEqual(configure_interface(device=self.mocked_obj, interface=" ", address=" ", unit=" ", inet_mode=" ", commit=True), 1)
    
    def test_interface_5(self):

        self.mocked_obj.config = MagicMock()
        self.mocked_obj.commit = MagicMock(return_value= 1)

        self.assertEqual(configure_interface(device=self.mocked_obj, interface=" ", address=" ", unit=" ", inet_mode=" "), 1)

    def test_interface_6(self):

        self.mocked_obj.config = MagicMock()
        self.mocked_obj.commit = MagicMock(return_value= 1)

        self.assertTrue(configure_interface(device=self.mocked_obj, interface="st0", unit=1))

if __name__ == '__main__':
    unittest.main()
