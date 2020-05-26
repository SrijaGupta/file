from jnpr.toby.utils.linux.linux_ovs import extract_ports_in_ovs_bridge
from jnpr.toby.utils.linux.linux_ovs import check_ports_in_bridge
from jnpr.toby.utils.linux.linux_ovs import check_port_info_in_bridge
from jnpr.toby.utils.linux.linux_ovs import fetch_ovs_interface_number
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.utils.response import Response

import unittest
import builtins
import requests
from mock import MagicMock
from mock import patch

class TestTime(unittest.TestCase):

    # ---
    # Tests for function extract_ports_in_ovs_bridge
    # ---

    shell_response = """
08276fc0-fc63-4576-9fb6-4745e5baf24a
    Bridge ovs-sys-br
        Port "veth01"
            trunks: [1]
            Interface "veth01"
        Port "veth11"
            tag: 123
            Interface "veth11"
"""
    def test_extract_ports_in_ovs_bridge(self):

        exp_func_response = {
            "veth01" : {
                "mode" : "trunk",
                "vlan" : ['1']
            },
            "veth11" : {
                "mode" : "access",
                "vlan" : ["123"]
            }
        }

        mock_dev = MagicMock(spec=Juniper)
        mock_resp = MagicMock(spec=Response)
        mock_resp.response = MagicMock(return_value=self.shell_response)
        mock_dev.shell = MagicMock(return_value=mock_resp)

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(extract_ports_in_ovs_bridge(mock_dev, "ovs-sys-br"), (True, exp_func_response) )

    def test_extract_ports_in_ovs_bridge_exception_empty_bridgename(self):

        mock_dev = MagicMock(spec=Juniper)
        mock_resp = MagicMock(spec=Response)
        mock_resp.response = MagicMock(return_value=self.shell_response)
        mock_dev.shell = MagicMock(return_value=mock_resp)

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(extract_ports_in_ovs_bridge(mock_dev, ""), (True, exp_func_response) )
        except Exception as err:
            self.assertRegex(err.args[0], "Empty Bridge Name")

    def test_extract_ports_in_ovs_bridge_exception_cmd_exception(self):

        mock_dev = MagicMock(spec=Juniper)
        mock_resp = MagicMock(spec=Response)
        mock_resp.response = MagicMock(return_value=self.shell_response)
        mock_dev.shell = MagicMock(return_value=mock_resp)

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(extract_ports_in_ovs_bridge(mock_dev, ""), (True, exp_func_response) )
        except Exception as err:
            self.assertRegex(err.args[0], "Empty Bridge Name")

if __name__ =='__main__':
    unittest.main()
