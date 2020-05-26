
import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.nfx_infra import nfx_utils
from jnpr.toby.hldcl.juniper.junos import Juniper



# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=Juniper)
    mocked_obj.log = MagicMock()


    def test_get_flowd_mapping_exception(self):
        try:
            nfx_utils.get_flowd_mapping()
        except Exception as err:
            self.assertEqual(err.args[0], "device is a mandatory argument")

        self.mocked_obj.get_model = MagicMock(return_value="SRX")
        try:
            nfx_utils.get_flowd_mapping(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "This keyword is only for NFX box")


    def test_get_flowd_mapping(self):
        self.mocked_obj.get_model = MagicMock(return_value="NFX")
        x = "set host-os virtualization-options interfaces ge-0/0/0 mapping interface heth-0-0\nset host-os virtualization-options interfaces ge-0/0/1 mapping interface heth-0-1\n set host-os virtualization-options interfaces ge-0/0/2 mapping interface heth-0-2"
        self.mocked_obj.cli = MagicMock(return_value=Response(x))
        dct = {'heth-0-0' : 'ge-0/0/0', 'heth-0-1' : 'ge-0/0/1', 'heth-0-2' : 'ge-0/0/2'}

        self.assertEqual(nfx_utils.get_flowd_mapping(device=self.mocked_obj), dct)

        self.mocked_obj.cli.return_value = Response(" ")
        dct = {}
        self.assertEqual(nfx_utils.get_flowd_mapping(device=self.mocked_obj), dct)


if __name__ == '__main__':
    unittest.main()