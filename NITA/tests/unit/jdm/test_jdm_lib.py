
from mock import patch
from mock import MagicMock

import unittest2 as unittest
import unittest
import builtins
from jnpr.toby.jdm.jdm_lib import jdm_lib

from robot.libraries.BuiltIn import BuiltIn
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.device import execute_cli_command_on_device

class TestTime(unittest.TestCase):


    def test_get_expected_system_inventory_nfx(self):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        exp_dict = { "cpu" : 4, "hyper_thread" : 2, "cores" : 4, "logical_cpu" : 8 }
        exp_return_value = (True, exp_dict)
        self.assertEqual(jdm_lib_obj.get_expected_system_inventory_nfx("nfx250-ls1"), exp_return_value)

        exp_dict = { "cpu" : 6, "hyper_thread" : 2, "cores" : 6, "logical_cpu" : 12 }
        exp_return_value = (True, exp_dict)
        self.assertEqual(jdm_lib_obj.get_expected_system_inventory_nfx("nfx250-s1"), exp_return_value)

        exp_dict = { "cpu" : 4, "hyper_thread" : 1, "cores" : 4, "logical_cpu" : 4 }
        exp_return_value = (True, exp_dict)
        self.assertEqual(jdm_lib_obj.get_expected_system_inventory_nfx("nfx150_c-s1"), exp_return_value)

        exp_dict = { "cpu" : 8, "hyper_thread" : 1, "cores" : 8, "logical_cpu" : 8 }
        exp_return_value = (True, exp_dict)
        self.assertEqual(jdm_lib_obj.get_expected_system_inventory_nfx("nfx150_s1"), exp_return_value)

    def test_get_expected_system_inventory_nfx_exceptions(self):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        exp_dict = { "cpu" : 4, "hyper_thread" : 2, "cores" : 4, "logical_cpu" : 8 }
        exp_return_value = (True, exp_dict)

        try:
            self.assertEqual(jdm_lib_obj.get_expected_system_inventory_nfx("nfx350"), exp_return_value)
        except Exception as err:
            self.assertIn("Unknown Model", err.args[0])

    output = """
CPU Usages
----------------
CPU Id CPU Usage
------ ---------
0      37.299999999999997
1      44.700000000000003
2      0.0      
3      0.0      
4      0.0      
5      0.0      
6      0.0      
7      0.0      

CPU Pinning Information
"""
    @patch('jnpr.toby.jdm.jdm_lib.execute_cli_command_on_device', return_value=output)
    def test_fetch_cpu_usage(self, patch_exec_cli):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        dev_hdl = None
        cpu_usage_hash = { 0 : 37.3, 1 : 44.7, 2 : 0.0, 3 : 0.0, 4 : 0.0, 5 : 0.0, 6 : 0.0, 7 : 0.0 } 
  
        self.assertEqual(jdm_lib_obj.fetch_cpu_usage(dev_hdl), (True, cpu_usage_hash))

    output = """
"""
    @patch('jnpr.toby.jdm.jdm_lib.execute_cli_command_on_device', return_value=output)
    def test_fetch_cpu_usage_not_found(self, patch_exec_cli):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        dev_hdl = None
        cpu_usage_hash = { 0 : 37.3, 1 : 44.7, 2 : 0.0, 3 : 0.0, 4 : 0.0, 5 : 0.0, 6 : 0.0, 7 : 0.0 }

        try:
            self.assertEqual(jdm_lib_obj.fetch_cpu_usage(dev_hdl), (True, cpu_usage_hash))
        except Exception as err:
            self.assertIn("No CPU Usage", err.args[0])


    output = """
CPU Usages
----------------
CPU Id CPU Usage
------ ---------
CPU Pinning Information
"""
    @patch('jnpr.toby.jdm.jdm_lib.execute_cli_command_on_device', return_value=output)
    def test_fetch_cpu_usage_not_found_2(self, patch_exec_cli):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        dev_hdl = None
        cpu_usage_hash = { 0 : 37.3, 1 : 44.7, 2 : 0.0, 3 : 0.0, 4 : 0.0, 5 : 0.0, 6 : 0.0, 7 : 0.0 }

        try:
            self.assertEqual(jdm_lib_obj.fetch_cpu_usage(dev_hdl), (True, cpu_usage_hash))
        except Exception as err:
            self.assertIn("No CPU Usage", err.args[0])

    output = """
CPU Usages
----------------
CPU Id CPU Usage
------ ---------
0      33.899999999999999
1      0.0      
2      0.0      
3      0.0      
4      0.0      
5      0.0      
6      100.0    
7      3.2999999999999998
8      0.0      
9      0.0      
10     0.0      
11     0.0      

CPU Pinning Information
------------------------------------
Virtual Machine             vCPU CPU
--------------------------- ---- ---
vjunos0                     0    0  
centos1                     0    0  
centos1                     0    1  
centos1                     0    2  
centos1                     0    3  ^M
centos1                     0    4  ^M
centos1                     0    5  
centos1                     0    6  
centos1                     0    7  
centos1                     0    8  
centos1                     0    9  
centos1                     0    10 
centos1                     0    11 
centos2                     0    2
centos2                     1    3
centos-new                  0    2
centos-new                  1    3
"""
    @patch('jnpr.toby.jdm.jdm_lib.execute_cli_command_on_device', return_value=output)
    def test_fetch_cpu_pinning_info_vnf1(self, patch_exec_cli):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        dev_hdl = None 
        vnf_name = "centos1"
        cpu_pinning_hash = { '0' : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'] }
        self.assertEqual(jdm_lib_obj.fetch_cpu_pinning_info(dev_hdl, vnf_name), (True, cpu_pinning_hash))

    @patch('jnpr.toby.jdm.jdm_lib.execute_cli_command_on_device', return_value=output)
    def test_fetch_cpu_pinning_info_vnf2(self, patch_exec_cli):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        dev_hdl = None
        vnf_name = "centos2"
        cpu_pinning_hash = { '0' : ['2'], '1' : ['3']}
        self.assertEqual(jdm_lib_obj.fetch_cpu_pinning_info(dev_hdl, vnf_name), (True, cpu_pinning_hash))

    @patch('jnpr.toby.jdm.jdm_lib.execute_cli_command_on_device', return_value=output)
    def test_fetch_cpu_pinning_info_vnf3(self, patch_exec_cli):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        dev_hdl = None
        vnf_name = "centos3"
        cpu_pinning_hash = { '0' : ['2'], '1' : ['3']}
        try:
            self.assertEqual(jdm_lib_obj.fetch_cpu_pinning_info(dev_hdl, vnf_name), (True, cpu_pinning_hash))
        except Exception as err:
            self.assertIn("No CPU Pinning Information found for VNF: centos3", err.args[0])

    @patch('jnpr.toby.jdm.jdm_lib.execute_cli_command_on_device', return_value=output)
    def test_verify_vnf_cpu_pinning_vnf1(self, patch_exec_cli):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        dev_hdl = None
        vnf_name = "centos-new"
        cpu_pinning_hash = { '0' : [2], '1': [3] }
        self.assertEqual(jdm_lib_obj.verify_vnf_cpu_pinning(dev_hdl, vnf_name, cpu_pinning_hash), True)

    @patch('jnpr.toby.jdm.jdm_lib.execute_cli_command_on_device', return_value=output)
    def test_verify_vnf_cpu_pinning_vnf2(self, patch_exec_cli):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        dev_hdl = None
        vnf_name = "centos2"
        cpu_pinning_hash = { '0' : ['2'], '1' : ['3']}
        self.assertEqual(jdm_lib_obj.verify_vnf_cpu_pinning(dev_hdl, vnf_name, cpu_pinning_hash), True)

        cpu_pinning_hash = { '0' : ['2'], '1' : ['4']}
        self.assertEqual(jdm_lib_obj.verify_vnf_cpu_pinning(dev_hdl, vnf_name, cpu_pinning_hash), False)

    output = """
set virtual-network-functions centos1 image /var/third-party/images/centos-linux-1.img
set virtual-network-functions centos2 image /var/third-party/images/centos-linux-2.img
set virtual-network-functions centos3 image /var/third-party/images/centos-linux-3.img
set virtual-network-functions centos4 image /var/third-party/images/centos-linux-4.img
"""
    @patch('jnpr.toby.jdm.jdm_lib.execute_cli_command_on_device', return_value=output)
    def test_fetch_vnf_list_from_config(self, patch_exec_cli):

        jdm_lib_obj = jdm_lib()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        dev_hdl = None
        vnf_list = ["centos1", "centos2", "centos3", "centos4"]
        self.assertEqual(jdm_lib_obj.fetch_vnf_list_from_config(dev_hdl), vnf_list)


if __name__ =='__main__':
    unittest.main()
