import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.syslog import traceoptions
from jnpr.toby.hldcl.juniper.security.srx import Srx


class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_configure_traceoptions_set_0(self):
        self.assertRaises(Exception, traceoptions.configure_traceoptions)

    def test_configure_traceoptions_set_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(traceoptions.configure_traceoptions(device=self.mocked_obj, feature='policies',
                                                             description=' ', commit=False),
                         True)
        self.assertEqual(traceoptions.configure_traceoptions(device=self.mocked_obj, description=' ', commit=False),
                         True)

        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(traceoptions.configure_traceoptions(device=self.mocked_obj, description=' ', commit=True),
                         True)

if __name__ == '__main__':
    unittest.main()
