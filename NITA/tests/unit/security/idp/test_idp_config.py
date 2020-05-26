import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.security.idp import idp_config


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


    def test_configure_idp_security_package_exception(self):
        try:
            idp_config.configure_idp_security_package()
        except Exception as err:
            self.assertEqual(err.args[0], "Argument: device is mandatory")

    def test_configure_security_package(self):
        self.mocked_obj.config = MagicMock()
        self.mocked_obj.commit = MagicMock()

        self.assertEqual(idp_config.configure_idp_security_package(device=self.mocked_obj, source_address="4.0.0.1", url="https://devdb.juniper.net/cgi-bin/index.cgi",
                                                                   ignore_version_check=True, automatic="enable", start_time="2016-09-08.12:10", interval="200"), True)
        self.assertEqual(idp_config.configure_idp_security_package(device=self.mocked_obj), True)
        self.assertEqual(idp_config.configure_idp_security_package(device=self.mocked_obj, mode="delete"), True)

if __name__ == '__main__':
    unittest.main()