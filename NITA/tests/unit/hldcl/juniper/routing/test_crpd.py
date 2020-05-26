"""
    UT for crpd.py
"""

import unittest2 as unittest
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.juniper.routing.crpd import Crpd


class TestCrpd(unittest.TestCase):
    @patch('jnpr.toby.hldcl.juniper.routing.router.Router.__init__', return_value=None)
    def test__init__(self, router_patch):
        cobject = MagicMock(spec=Crpd)
        self.assertIsInstance(Crpd(cobject), Crpd)

    @patch('jnpr.toby.hldcl.juniper.junos.time.sleep')
    def test__check_interface_status(self, sleep_patch):
        from jnpr.toby.hldcl.juniper.routing.crpd import Crpd
        from jnpr.toby.utils.response import Response
        import builtins
        cobject = MagicMock(spec=Crpd)
        builtins.t = cobject

        cobject.cli = MagicMock(return_value=Response(response="lsi   Up    MPLS  enabled"))
        self.assertTrue(Crpd._check_interface_status(cobject, interfaces=["lsi"]))
        cobject = MagicMock(spec=Crpd)
        cobject.cli = MagicMock(return_value=Response(response="lsi   down    MPLS  enabled"))
        self.assertFalse(Crpd._check_interface_status(cobject, interfaces=["(interface 2)"]))
        cobject.cli = MagicMock(return_value=Response(response="""(interface 1) int1 up (interface 2) int2 down"""))
        self.assertFalse(Crpd._check_interface_status(cobject, interfaces=["Some other pattern"]))
        cobject.cli = MagicMock(return_value=Response(response="""(interface 1) """))
        self.assertFalse(Crpd._check_interface_status(cobject, interfaces=["(interface"]))

if __name__ == "__main__":
    unittest.main()
