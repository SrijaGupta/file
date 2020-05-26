import unittest2 as unittest
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.juniper.switching.switch import Switch
from jnpr.toby.hldcl.juniper.junos import Juniper


class TestJunosModule(unittest.TestCase):
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_pyez')
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_text')
    @patch('jnpr.toby.hldcl.juniper.switching.switch.Juniper.__init__',return_value=None)
    def test_switch(self, patch1, patch2, patch3):
        sobject = MagicMock(spec=Juniper)
        self.assertIsInstance(Switch(sobject,host='host'), Switch)

