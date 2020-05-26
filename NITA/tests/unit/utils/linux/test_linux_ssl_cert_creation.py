from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.utils.linux.linux_ssl_cert_creation import generate_self_signed_cert
from jnpr.toby.hldcl.unix.unix import UnixHost

# To return response of shell() mehtod
class Response:

    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.execute = MagicMock()


    def test_generate_self_signed_certificate(self):
        try:
            generate_self_signed_cert(device=None)
        except ValueError as err:
            self.assertTrue(err.args[0],
                            'device is mandatory argument')

        self.assertEqual(
            generate_self_signed_cert(device=self.mocked_obj,
                                             serial_number="453968775956623377962957509531432590656820121612",
                                             key_filename="20byteserver_key_path.key",
                                             cert_filename="20byteserver_key_path.crt"), True)

        self.assertEqual(
            generate_self_signed_cert(device=self.mocked_obj,
                                             key_filename="20byteserver_key_path.key",
                                             cert_filename="20byteserver_key_path.crt"), True)

if __name__ == '__main__':
    unittest.main()
