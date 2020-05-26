import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.policy import policy
from jnpr.toby.hldcl.juniper.security.srx import Srx

class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_cofigure_policy_0(self):
        self.assertRaises(Exception, policy.configure_policy, default_policy_action=" ", default_policy=True)

    def test_configure_policy_1(self):
        source = [" ", " "]
        destination = [" ", " "]
        application = [" ", " "]
        self.mocked_obj.config = MagicMock()
        self.assertEqual(policy.configure_policy(device=self.mocked_obj, default_policy_action=" ", default_policy=True), True)
        self.assertEqual(policy.configure_policy(device=self.mocked_obj, policy_name=" ", source_address=" ", destination_address=" ",  application=" ", action=" ", logical_systems=" ", global_policy=True), True)
        self.assertEqual(policy.configure_policy(device=self.mocked_obj, from_zone="trust", to_zone="untrust", policy_name="p1", scheduler_name="daily_scheduler"),True)
        self.assertEqual(policy.configure_policy(device=self.mocked_obj, global_policy=True, policy_name="p1" ,source_address=source , destination_address=destination, application=application ,action="permit"), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(policy.configure_policy(device=self.mocked_obj, default_policy_action=" ", default_policy=True, commit=True), True)

if __name__ == '__main__':
    unittest.main()
