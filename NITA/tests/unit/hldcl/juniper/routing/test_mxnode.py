import unittest2 as unittest
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.juniper.routing.mxnode import *
from jnpr.toby.hldcl.juniper.junipernode import JuniperNode


class TestJunosModule(unittest.TestCase):
    def test_mxnode(self):
        sobject = MagicMock(spec=JuniperNode)
        data={'connect':False, 'vc':False, 'controllers':{'re0':{'osname':'JUNOS','connect':True}}}
        self.assertIsInstance(MxNode(data), MxNode)


