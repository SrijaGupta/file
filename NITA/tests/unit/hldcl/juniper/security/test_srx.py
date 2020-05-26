import unittest2 as unittest
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.juniper.security.srx import *
from jnpr.toby.hldcl.juniper.junos import *

class TestJunosModule(unittest.TestCase):
    def test_srx_vty(self):
        sobject = MagicMock(spec=Srx)
        try:
            Srx.vty(sobject)
        except Exception as err:
            self.assertEqual(type(err.args[0]), str )

    def test_srx_vty2(self):
        sobject = MagicMock(spec=Srx)
        sobject.su.return_value = False
        self.assertEqual(Srx.vty(sobject,command='ls',destination='ls'), False)

    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_pyez')
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_text')
    @patch('jnpr.toby.hldcl.host.Logger')
    @patch('jnpr.toby.hldcl.juniper.security.srx.Security.__init__', return_value=None)
    def test_CSrx(self, patch1, patch2, patch3, patch4):
        sobject = MagicMock(spec=Juniper)
        sobject.device_logger = MagicMock()
        sobject.device_logger._log.return_value = True
        self.assertIsInstance(CSrx(sobject,host='host'), CSrx)

    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_pyez')
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_text')
    @patch('jnpr.toby.hldcl.host.Logger')
    @patch('jnpr.toby.hldcl.juniper.security.srx.Security.__init__', return_value=None)
    def test_VSrx(self, patch1, patch2, patch3, patch4):
        sobject = MagicMock(spec=Juniper)
        self.assertIsInstance(VSrx(sobject,host='host'), VSrx)

