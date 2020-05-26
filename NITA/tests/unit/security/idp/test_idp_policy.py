from mock import patch
import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.idp import idp_policy
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

    @patch('jnpr.toby.security.idp.idp_policy.get_idp_policy_commit_status')
    def test_internal_install_idp_policy(self, patched_function):
        p = patch("time.sleep", new=MagicMock())
        p.start()
        d1 = {'status': ""}
        d2 = {'status': "error", 'message':"HELLO"}

        patched_function.side_effect= [d1, d2]


        try:
            idp_policy._install_idp_policy(self.mocked_obj,"node0", 50, True)
        except Exception as err:
            self.assertEqual(err.args[0], "IDP Policy installation is failed : HELLO")

        d3 = {'status': "success"}
        patched_function.side_effect = [d3]

        self.assertEqual(idp_policy._install_idp_policy(self.mocked_obj,"node0", 50, True), d3)

        d4 = {'status': ""}
        patched_function.side_effect = [d4]

        try:
            idp_policy._install_idp_policy(self.mocked_obj,"node0", 20, True)
        except Exception as err:
            self.assertEqual(err.args[0], "IDP Security policy install timed out. Waited for 20 secs")

        d5 = {'status': 'error', 'message': "IDP Security policy install timed out"}
        patched_function.side_effect = [d5]
        self.assertEqual(idp_policy._install_idp_policy(self.mocked_obj,"node0", 20, False), d5)

        p.stop()


    @patch('jnpr.toby.security.idp.idp_policy._install_idp_policy')
    def test_install_idp_policy(self, patched_function):
        try:
            idp_policy.install_idp_policy()
        except Exception as err:
            self.assertEqual(err.args[0], "device is mandatory argument")

        self.mocked_obj.is_ha = MagicMock(return_value=False)

        patched_function.side_effect = [1]
        self.assertEqual(idp_policy.install_idp_policy(device=self.mocked_obj, node="node0"), 1)

        self.mocked_obj.is_ha.return_value = True
        patched_function.side_effect = [1,1]

        self.assertEqual(idp_policy.install_idp_policy(device=self.mocked_obj), 1)
        patched_function.side_effect = [1, 2]

        try:
            idp_policy.install_idp_policy(device=self.mocked_obj, validate=True)
        except Exception as err:
            self.assertEqual(err.args[0], "IDP Policy installation status doesn't match on both nodes")







if __name__ == '__main__':
    unittest.main()