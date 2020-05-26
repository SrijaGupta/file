import unittest2 as unittest
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.juniper.routing.router import *
from jnpr.toby.hldcl.juniper.junos import Juniper


class TestJunosModule(unittest.TestCase):
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_pyez')
    @patch('jnpr.toby.hldcl.juniper.junos.Juniper._connect_text')
    @patch('jnpr.toby.hldcl.host.Logger')
    @patch('jnpr.toby.hldcl.juniper.routing.router.Juniper.__init__', return_value=None)
    def test_router(self,patch1, patch2, patch3, patch4):
        sobject = MagicMock(spec=Juniper)
        self.assertIsInstance(Router(sobject,host='host'), Router)


