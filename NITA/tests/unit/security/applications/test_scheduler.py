import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.applications import scheduler
from jnpr.toby.hldcl.juniper.security.srx import Srx


class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_configure_scheduler_0(self):
        self.assertRaises(Exception, scheduler.configure_scheduler)
        self.assertRaises(Exception, scheduler.configure_scheduler, device=self.mocked_obj)
        self.assertRaises(Exception, scheduler.configure_scheduler, device=self.mocked_obj, scheduler_name=' ')
        self.assertRaises(Exception, scheduler.configure_scheduler, device=self.mocked_obj, scheduler_name=' ',
                          start_time=' ')

    def test_configure_scheduler_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(scheduler.configure_scheduler(device=self.mocked_obj, scheduler_name=' ', start_time=' ',
                                                       day=' ', stop_time=' ', commit=False), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(scheduler.configure_scheduler(device=self.mocked_obj, scheduler_name=' ', start_time=' ',
                                                       day=' ', stop_time=' ', commit=True), True)

if __name__ == '__main__':
    unittest.main()
