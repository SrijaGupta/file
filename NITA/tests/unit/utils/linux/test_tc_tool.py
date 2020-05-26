import sys
import unittest2 as unittest
from unittest.mock import MagicMock, patch, PropertyMock
from jnpr.toby.utils.linux.tc_tool import *
from jnpr.toby.hldcl.unix.unix import *
import os

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class TestTc_tool(unittest.TestCase):
    def setUp(self):
        """setup before all cases"""
        self.device = MagicMock(spec=Unix)
        self.device.log =  MagicMock(return_value=True)

    def test_configure_qdisc_netem(self):
        lst = [Response("success"), Response("success"), Response("success")]
        self.device.shell = MagicMock(side_effect=lst)
        self.assertTrue(configure_qdisc_netem(device=self.device, intf='eth0', delay='100ms'))

        try:
            x = configure_qdisc_netem(intf='eth0', delay='100ms')
        except Exception as err:
            self.assertEqual(err.args[0], "device is mandatory argument")

        try:
            x = configure_qdisc_netem(device=self.device, delay='100ms')
        except Exception as err:
            self.assertEqual(err.args[0], "intf is mandatory argument")

        self.assertTrue(configure_qdisc_netem(device=self.device, intf='eth0', delay='100ms',
                        parent_qdisc_id='parent', handle_qdisc_id='1:',qdisc_kind='pfifo',
                        limit='1000'))

        self.assertTrue(configure_qdisc_netem(device=self.device, intf='eth0', delay='100ms',action='change',
                                              distribution='normal',loss='1%',corrupt='.1%',duplicate='1%',
                                              reorder='25%'))


if __name__ == '__main__':
    #import pdb
    #pdb.set_trace()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTc_tool)
    unittest.TextTestRunner(verbosity=2).run(suite)
