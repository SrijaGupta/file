import unittest2 as unittest
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.juniper.switching.ex import *
from jnpr.toby.hldcl.juniper.junos import Juniper

class TestJunosModule(unittest.TestCase):
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_pyez')
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_text')
    @patch('jnpr.toby.hldcl.juniper.switching.ex.switch.Switch.__init__', return_value=None)
    def test_ex(self,patch1, patch2, patch3):
        sobject = MagicMock(spec=Juniper)
        self.assertIsInstance(Ex(sobject,host='host'), Ex)

    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_pyez')
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_text')
    @patch('jnpr.toby.hldcl.juniper.switching.ex.switch.Switch.__init__', return_value=None)
    def test_qfx(self, patch1, patch2, patch3):
        sobject = MagicMock(spec=Juniper)
        self.assertIsInstance(Qfx(sobject,host='host'), Qfx)

    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_pyez')
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_text')
    @patch('jnpr.toby.hldcl.juniper.switching.ex.switch.Switch.__init__', return_value=None)
    def test_ocx(self,patch1,patch2, patch3):
        sobject = MagicMock(spec=Juniper)
        self.assertIsInstance(Ocx(sobject,host='host'), Ocx)

    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_pyez')
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_text')
    @patch('jnpr.toby.hldcl.juniper.switching.ex.switch.Switch.__init__', return_value=None)
    def test_nfx(self,patch1,patch2, patch3):
        sobject = MagicMock(spec=Juniper)
        self.assertIsInstance(Nfx(sobject,host='host'), Nfx)

