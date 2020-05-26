import unittest2 as unittest
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.juniper.security.security import *
from jnpr.toby.hldcl.juniper.junos import Juniper


class TestJunosModule(unittest.TestCase):
    def test_security_re_slot_name(self):
        sobject = MagicMock(spec=Juniper)
        self.assertEqual(Security.re_slot_name(sobject), 'RE0')

    def test_security__is_master(self):
        sobject = MagicMock(spec=Juniper)
        self.assertEqual(Security._is_master(sobject), True)

