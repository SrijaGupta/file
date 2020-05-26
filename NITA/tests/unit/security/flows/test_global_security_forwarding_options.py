import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.security.flows import global_security_forwarding_options


class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_configure_global_security_forwarding_options_0(self):
        self.assertRaises(Exception, global_security_forwarding_options.configure_global_security_forwarding_options,
                          family=" ", mode=" ")
        self.assertRaises(Exception, global_security_forwarding_options.configure_global_security_forwarding_options,
                          device=self.mocked_obj, mode="")
        self.assertRaises(Exception, global_security_forwarding_options.configure_global_security_forwarding_options,
                          device=self.mocked_obj, family=" ")

    def test_configure_global_security_forwarding_options_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(
            global_security_forwarding_options.configure_global_security_forwarding_options(device=self.mocked_obj,
                                                                                            family=" ", mode=" "), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(
            global_security_forwarding_options.configure_global_security_forwarding_options(device=self.mocked_obj,
                                                                                            family=" ", mode=" ",
                                                                                            commit=True), True)


if __name__ == '__main__':
    unittest.main()
