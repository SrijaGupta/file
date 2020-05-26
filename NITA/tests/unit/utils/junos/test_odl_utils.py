import builtins
from robot.libraries.BuiltIn import BuiltIn
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.utils.response import Response

from jnpr.toby.utils.junos.odl_utils import mount_junos_device_on_odl
from jnpr.toby.utils.junos.odl_utils import unmount_junos_device_on_odl
from jnpr.toby.utils.junos.odl_utils import get_mount_status_of_junos_device_on_odl
from jnpr.toby.utils.junos.odl_utils import poll_mount_status_of_junos_device_on_odl
from jnpr.toby.utils.junos.odl_utils import get_device_capability_list_from_odl
from jnpr.toby.utils.junos.odl_utils import execute_rpc_from_odl
from jnpr.toby.utils.junos.odl_utils import compare_xml_responses_between_odl_junos
from jnpr.toby.utils.junos.odl_utils import find_yang_module_name_for_rpc
from jnpr.toby.utils.junos.odl_utils import is_input_defined_for_rpc

import unittest
import builtins
import requests
from mock import MagicMock
from mock import patch

class TestTime(unittest.TestCase):

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 201
    response.content = ""
    @patch('requests.put', return_value=response)
    def test_mandatory_arg_exceptions(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        dut_ip = "10.204.41.77"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        try:
            self.assertEqual(mount_junos_device_on_odl(), "")
        except Exception as err:
            self.assertRegex(err.args[0], ".*missing.*required positional argument.*")

        try:
            self.assertEqual(mount_junos_device_on_odl(odl_ip, hostname), "")
        except Exception as err:
            self.assertRegex(err.args[0], ".*missing.*required positional argument.*")

        try:
            self.assertEqual(unmount_junos_device_on_odl(), "")
        except Exception as err:
            self.assertRegex(err.args[0], ".*missing.*required positional argument.*")

        try:
            self.assertEqual(unmount_junos_device_on_odl(odl_ip), "")
        except Exception as err:
            self.assertRegex(err.args[0], ".*missing.*required positional argument.*")
 
        try:
            self.assertEqual(get_mount_status_of_junos_device_on_odl(),"")
        except Exception as err:
            self.assertRegex(err.args[0], ".*missing.*required positional argument.*")

        try:
            self.assertEqual(get_mount_status_of_junos_device_on_odl(odl_ip),"")
        except Exception as err:
            self.assertRegex(err.args[0], ".*missing.*required positional argument.*")

    # ---
    # Unit Tests For Function: mount_junos_device_on_odl
    # ---
    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 201
    response.content = ""
    @patch('requests.put', return_value=response)
    def test_mount_junos_device_on_odl(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        dut_ip = "10.204.41.77"
        cache_dir = "temp"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(mount_junos_device_on_odl(odl_ip, hostname, dut_ip, cache_dir), True)

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 200
    response.content = ""
    @patch('requests.put', return_value=response)
    def test_mount_junos_device_on_odl_2(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        dut_ip = "10.204.41.77"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(mount_junos_device_on_odl(odl_ip, hostname, dut_ip), True)

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 201
    response.content = ""
    @patch('requests.put', return_value=response)
    def test_mount_junos_device_on_odl_addn_args(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        dut_ip = "10.204.41.77"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(mount_junos_device_on_odl(odl_ip, hostname, dut_ip, auth_user='root', auth_password='root'), True)

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 202
    response.content = ""
    @patch('requests.put', return_value=response)
    def test_mount_junos_device_on_odl_exception_resp_code(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        dut_ip = "10.204.41.77"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(mount_junos_device_on_odl(odl_ip, hostname, dut_ip, auth_user='root', auth_password='root'), "")  
        except Exception as err:
            self.assertEqual(err.args[0], "Response Code is not 201 while adding new device to ODL")

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 201
    response.content = ""
    @patch('requests.put', side_effect=Exception("test exception"))
    def test_mount_junos_device_on_odl_exception_request(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        dut_ip = "10.204.41.77"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(mount_junos_device_on_odl(odl_ip, hostname, dut_ip, auth_user='root', auth_password='root'), "")
        except Exception as err:
            self.assertRegex(err.args[0], "test exception")




    #============================================================================================================================
    # ---
    # Unit Tests For Function: unmount_junos_device_on_odl
    # ---
    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 200
    response.content = ""
    @patch('requests.delete', return_value=response)
    def test_unmount_junos_device_on_odl(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(unmount_junos_device_on_odl(odl_ip, hostname), True)

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 201
    response.content = ""
    @patch('requests.delete', return_value=response)
    def test_unmount_junos_device_on_odl_dev_not_found(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(unmount_junos_device_on_odl(odl_ip, hostname), True)
        except Exception as err:
            self.assertEqual(err.args[0], "Failed to delete device from ODL")

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 204
    response.content = ""
    @patch('requests.delete', return_value=response)
    def test_unmount_junos_device_on_odl_delete_fail(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try: 
            self.assertEqual(unmount_junos_device_on_odl(odl_ip, hostname), True)
        except Exception as err:
            self.assertEqual(err.args[0], "Failed to delete device from ODL")

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 200
    response.content = ""
    @patch('requests.delete', side_effect=Exception("test exception"))
    def test_umount_junos_device_on_odl_exception_request(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        dut_ip = "10.204.41.77"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(unmount_junos_device_on_odl(odl_ip, hostname), True)
        except Exception as err:
            self.assertRegex(err.args[0], "test exception")


    #============================================================================================================================
    # ---
    # tests for function get_mount_status_of_junos_device_on_odl
    # ---

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 200
    response.content = b"""
{
    "node": [
        {
            "node-id": "porter3c-ae-p1b-ft-03",
            "netconf-node-topology:clustered-connection-status": {
                "netconf-master-node": "akka.tcp://opendaylight-cluster-data@127.0.0.1:2550"
            },
            "netconf-node-topology:connection-status": "connected"
        }
    ]
}
"""
    @patch('requests.get', return_value=response)
    def test_get_mount_status_of_junos_device_on_odl_bytes_content(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(get_mount_status_of_junos_device_on_odl(odl_ip, hostname), "connected")

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 200
    response.content = b"""
{
    "node": [
        {
            "node-id": "porter3c-ae-p1b-ft-03",
            "netconf-node-topology:clustered-connection-status": {
                "netconf-master-node": "akka.tcp://opendaylight-cluster-data@127.0.0.1:2550"
            },
            "netconf-node-topology:connection-status": "connected"
        }
    ]
}
"""
    @patch('requests.get', return_value=response)
    def test_get_mount_status_of_junos_device_on_odl_str_content(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(get_mount_status_of_junos_device_on_odl(odl_ip, hostname), "connected")

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 200
    response.content = b"""
{
    "errors": {
        "error" : [
            {
            "error-message": "porter3c-ae-p1b-ft-03"
            }
        ]
    }
}
"""
    @patch('requests.get', return_value=response)
    def test_get_mount_status_of_junos_device_on_odl_err_response_exception(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(get_mount_status_of_junos_device_on_odl(odl_ip, hostname), "connected")
        except Exception as err:
            self.assertRegex(err.args[0], ".*Error in fetching stat.*")

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 200
    response.content = b"""
{
    "node": [
        {
            "node-id": "porter3c-ae-p1b-ft-03",
            "netconf-node-topology:clustered-connection-status": {
                "netconf-master-node": "akka.tcp://opendaylight-cluster-data@127.0.0.1:2550"
            },
            "netconf-node-topology:connection-status": "connected"
        }
    ]
}
"""
    @patch('requests.get', side_effect=Exception("test exception"))
    def test_get_mount_status_of_junos_device_on_odl_req_exception(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(get_mount_status_of_junos_device_on_odl(odl_ip, hostname), "connected")
        except Exception as err:
            self.assertRegex(err.args[0], ".*test exception.*")

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 404
    response.content = b"""
{
    "node": [
        {
            "node-id": "porter3c-ae-p1b-ft-03",
            "netconf-node-topology:clustered-connection-status": {
                "netconf-master-node": "akka.tcp://opendaylight-cluster-data@127.0.0.1:2550"
            },
            "netconf-node-topology:connection-status": "connected"
        }
    ]
}
"""
    @patch('requests.get', return_value=response)
    def test_get_mount_status_of_junos_device_on_odl_req_exception_404(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(get_mount_status_of_junos_device_on_odl(odl_ip, hostname), "connected")
        except Exception as err:
            self.assertRegex(err.args[0], ".*Device Not found.*")

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 200
    response.content = b"""
{
    "node": [
        {
            "node-id": "porter3c-ae-p1b-ft-03",
            "netconf--bad-node-topology:clustered-connection-status": {
                "netconf-master-node": "akka.tcp://opendaylight-cluster-data@127.0.0.1:2550"
            },
            "netconf-bad-node-topology:connection-status": "connected"
        }
    ]
}
"""
    @patch('requests.get', return_value=response)
    def test_get_mount_status_of_junos_device_on_odl_str_content(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(get_mount_status_of_junos_device_on_odl(odl_ip, hostname), "connected")
        except Exception as err:
            self.assertRegex(err.args[0], ".*doesn't match expected JSON.*")

    #============================================================================================================================
    # ---
    # tests for function poll_mount_status_of_junos_device_on_odl
    # ---

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 204
    response.content = b"""
{
    "node": [
        {
            "node-id": "porter3c-ae-p1b-ft-03",
            "netconf-node-topology:clustered-connection-status": {
                "netconf-master-node": "akka.tcp://opendaylight-cluster-data@127.0.0.1:2550"
            },
            "netconf-node-topology:connection-status": "connected"
        }
    ]
}
"""

    @patch('requests.get', return_value=response)
    def test_poll_mount_status_of_junos_device_on_odl(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(poll_mount_status_of_junos_device_on_odl(odl_ip, hostname), True)
        except Exception as err:
            self.assertRegex(err.args[0], ".*Error in fetching stat.*")


    #============================================================================================================================
    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 204
    response.content = b"test"
    @patch('requests.post', return_value=response)
    def test_execute_rpc_from_odl_bytes_content(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        yang_name = "junos-rpc-virtual-network-functions"
        rpc = "get-virtual-network-functions-information"
        args_dict = { "vnf-name" : "vjunos0" }
        expected_output = "test"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(execute_rpc_from_odl(odl_ip, hostname, yang_name, rpc, args_dict), expected_output)

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 204
    response.content = "test"
    @patch('requests.post', return_value=response)
    def test_execute_rpc_from_odl_str_content(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        yang_name = "junos-rpc-virtual-network-functions"
        rpc = "get-virtual-network-functions-information"
        args_dict = { "vnf-name" : "vjunos0" }
        expected_output = "test"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(execute_rpc_from_odl(odl_ip, hostname, yang_name, rpc, args_dict), expected_output)

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 201
    response.content = ""
    @patch('requests.post', side_effect=Exception("test exception"))
    def test_execute_rpc_from_odl_exception_request(self, patch_requests):

        odl_ip = "10.204.34.40"
        hostname = "porter3c-ae-p1b-ft-03"
        yang_name = "junos-rpc-virtual-network-functions"
        rpc = "get-virtual-network-functions-information"
        args_dict = { "vnf-name" : "vjunos0" }
        expected_output = "test"

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        try:
            self.assertEqual(execute_rpc_from_odl(odl_ip, hostname, yang_name, rpc, args_dict), "")
        except Exception as err:
            self.assertRegex(err.args[0], "test exception")

    # ---
    # Tests for function compare_xml_responses_between_odl_junos
    # ---
    def test_compare_xml_responses_between_odl_junos(self):

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        odl_response = "<rpc-reply><virtual-network-functions></virtual-network-functions></rpc-reply>"
        junos_response = "<rpc-reply><virtual-network-functions></virtual-network-functions></rpc-reply>"
        self.assertEqual(compare_xml_responses_between_odl_junos(odl_response, junos_response), True)

        odl_response = "<rpc-reply><virtual-network-functions>test</virtual-network-functions></rpc-reply>"
        junos_response = "<rpc-reply><virtual-network-functions>test</virtual-network-functions></rpc-reply>"
        self.assertEqual(compare_xml_responses_between_odl_junos(odl_response, junos_response, compare_values=True), True)

    def test_compare_xml_responses_between_odl_junos_xml_exceptions(self):

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        odl_response = "<rpc-reply><virtual-network-functions>test</virtual-network-functions></rpc-reply>"
        junos_response = "<rpc-reply><virtual-network-functions></virtual-network-functions></rpc-reply>"
        try:
            self.assertEqual(compare_xml_responses_between_odl_junos(odl_response, junos_response), True)
        except Exception as err:
            self.assertRegex(err.args[0],".*does not match.*")

        odl_response = ""
        junos_response = ""
        try:
            self.assertEqual(compare_xml_responses_between_odl_junos(odl_response, junos_response), True)
        except Exception as err:
            self.assertRegex(err.args[0],".*XMLSyntaxError.*")

        odl_response = "<rpc-reply></rpc-reply>"
        junos_response = "<rpc-reply></rpc-reply>"
        try:
            self.assertEqual(compare_xml_responses_between_odl_junos(odl_response, junos_response), True)
        except Exception as err:
            self.assertRegex(err.args[0],".*IndexError.*")

    # ---
    # Tests for function find_yang_module_name_for_rpc
    # ---

    def test_find_yang_module_name_for_rpc_exceptions(self):

        exp_response = ""
        rpc = "get-virtual-network-functions"

        mock_dev = MagicMock(spec=Juniper)
        mock_resp = MagicMock(spec=Response)
        mock_resp.response = MagicMock(return_value=exp_response)
        mock_dev.shell = MagicMock(return_value=mock_resp)

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        yang_dir = "/tmp/rpc-yang"

        try:
            self.assertEqual(find_yang_module_name_for_rpc(mock_dev, rpc, yang_dir), exp_response)
        except Exception as err:
            self.assertRegex(err.args[0],".*No yang file found under .*")

        exp_response = """
junos-rpc-vnf:rpc-get-virtual-network-functions
"""
        mock_resp.response = MagicMock(return_value=exp_response)
        mock_dev.shell = MagicMock(return_value=mock_resp)
        try:
            self.assertEqual(find_yang_module_name_for_rpc(mock_dev, rpc, yang_dir), exp_response)
        except Exception as err:
            self.assertRegex(err.args[0],".*No yang module .*")

    def test_find_yang_module_name_for_rpc(self):

        rpc = "get-virtual-network-functions"
        mock_dev = MagicMock(spec=Juniper)
        mock_resp = MagicMock(spec=Response)

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        yang_dir = "/tmp/rpc-yang"
        exp_response = """
junos-rpc-vnf:rpc-get-virtual-network-functions
  module junos-rpc-virtual-network-functions {
"""
        mock_resp.response = MagicMock(return_value=exp_response)
        mock_dev.shell = MagicMock(return_value=mock_resp)
        self.assertEqual(find_yang_module_name_for_rpc(mock_dev, rpc, yang_dir), "junos-rpc-virtual-network-functions")

        try:
            self.assertEqual(find_yang_module_name_for_rpc(mock_dev, "get-wrong-rpc", yang_dir), "junos-rpc-virtual-network-functions")
        except Exception as err:
            self.assertRegex(err.args[0], "No yang file.*")

    def test_is_input_defined_for_rpc(self):

        rpc = "get-virtual-network-functions"
        mock_dev = MagicMock(spec=Juniper)
        mock_resp = MagicMock(spec=Response)

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        yang_dir = "/tmp/rpc-yang"
        exp_response = """
junos-rpc-vnf:rpc-get-virtual-network-functions
  module junos-rpc-virtual-network-functions {
    rpc get-virtual-network-functions {
      input {
      }
    }
    rpc get-sample-rpc {
    }
  }
}
"""
        mock_resp.response = MagicMock(return_value=exp_response)
        mock_dev.shell = MagicMock(return_value=mock_resp)
        self.assertEqual(is_input_defined_for_rpc(mock_dev, rpc, yang_dir), True)

        rpc = "get-sample-rpc"
        mock_resp.response = MagicMock(return_value=exp_response)
        mock_dev.shell = MagicMock(return_value=mock_resp)
        self.assertEqual(is_input_defined_for_rpc(mock_dev, rpc, yang_dir), False)

    def test_is_input_defined_for_rpc_exception(self):

        rpc = "get-wrong-rpc"
        mock_dev = MagicMock(spec=Juniper)
        mock_resp = MagicMock(spec=Response)

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        yang_dir = "/tmp/rpc-yang"
        exp_response = """
junos-rpc-vnf:rpc-get-virtual-network-functions
}
"""
        mock_resp.response = MagicMock(return_value=exp_response)
        mock_dev.shell = MagicMock(return_value=mock_resp)
        try:
            self.assertEqual(is_input_defined_for_rpc(mock_dev, rpc, yang_dir), False)
        except Exception as err:
            self.assertRegex(err.args[0], "No yang file.*")

if __name__ =='__main__':
    unittest.main()

