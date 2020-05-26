import sys

import unittest2 as unittest
from mock import patch, MagicMock

from jnpr.toby.hldcl.trafficgen.trafficgen import *


class Test_TrafficGen(unittest.TestCase):

    def test_TrafficGen(self):
        with patch('jnpr.toby.hldcl.host.Host.__init__',return_value=None) as super_patch:
            TrafficGen()

    def test_execute_tester_command(self):
        dobject = MagicMock()
        dobject.invoke.return_value = "test"
        execute_tester_command(device=dobject,command="test_cmd")
    
    def test_connect_tester(self):
        dobject = MagicMock()
        dobject.connect.return_value = "test"
        connect_tester(device1=dobject,command="test_cmd")

    def test_get_port_handle(self):
        dobject = MagicMock()
        dobject.get_port_handle.return_value = "test"
        get_port_handle(device=dobject,intf="test_cmd")


if __name__=='__main__':    
    unittest.main()
