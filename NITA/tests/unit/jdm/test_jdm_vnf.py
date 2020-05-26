
from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
import builtins

from jnpr.toby.jdm.jdm_vnf import jdm_vnf

from robot.libraries.BuiltIn import BuiltIn
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.device import execute_cli_command_on_device

from mock import patch
from mock import MagicMock

class TestTime(unittest.TestCase):


    def test_log_funcs(self):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.__log_info__("Test Message")
        jdm_vnf_obj.__log_warning__("Test Message")
        jdm_vnf_obj.__log_error__("Test Message")

    def test_get_vnf_handle(self):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_console_handles = {}
        jdm_vnf_obj.vnf_console_handles["r0"] = {}
        jdm_vnf_obj.vnf_console_handles["r0"]["centos"] = 1

        jdm_vnf_obj.vnf_ssh_handles = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"] = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"]["centos"] = None

        self.assertEqual(jdm_vnf_obj.get_vnf_handle("r0", "centos", mode="console"), (True, 1))

        try:
            self.assertEqual(jdm_vnf_obj.get_vnf_handle("r0", "cento", mode="console"), (True, 1))
        except Exception as err:
            self.assertRegex(err.args[0], ".*No Handle.*")

    output = "test_output"
    @patch('jnpr.toby.jdm.jdm_vnf.execute_shell_command_on_device', return_value=output)
    def test_execute_command_on_vnf(self, patch_exec_shell):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_console_handles = {}
        jdm_vnf_obj.vnf_console_handles["r0"] = {}
        jdm_vnf_obj.vnf_console_handles["r0"]["centos"] = 1

        jdm_vnf_obj.vnf_ssh_handles = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"] = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"]["centos"] = None
 
        output = "test_output"
        self.assertEqual(jdm_vnf_obj.execute_command_on_vnf("r0", "centos", "test-cmd", console=True), (True, output))

        try:
            self.assertEqual(jdm_vnf_obj.execute_command_on_vnf("r0", "centos", "test-cmd", console=False), (True, output))
        except Exception as err:
            self.assertRegex(err.args[0], ".*No Handle.*")

        try:
            self.assertEqual(jdm_vnf_obj.execute_command_on_vnf("r0", "centos", "test-cmd", console=False, mode="test"), (True, output))
        except Exception as err:
            self.assertRegex(err.args[0], ".*Unsupported.*")

    @patch('jnpr.toby.jdm.jdm_vnf.disconnect_from_device', return_value=True)
    def test_disconnect_ssh_to_vnf_via_jdm(self, patch_disconnect):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_ssh_handles = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"] = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"]["centos"] = None

        self.assertEqual(jdm_vnf_obj.disconnect_ssh_to_vnf_via_jdm("r0", "centos"), True)
        self.assertEqual(jdm_vnf_obj.disconnect_ssh_to_vnf_via_jdm("r0", "new-centos"), True)
        self.assertEqual(jdm_vnf_obj.disconnect_ssh_to_vnf_via_jdm("r1", "new-centos"), True)

    @patch('jnpr.toby.jdm.jdm_vnf.disconnect_from_device', return_value=False)
    def test_disconnect_ssh_to_vnf_via_jdm_disconnect_failed(self, patch_disconnect):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_ssh_handles = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"] = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"]["centos"] = 1

        try: 
            self.assertEqual(jdm_vnf_obj.disconnect_ssh_to_vnf_via_jdm("r0", "centos"), True)
        except Exception as err:
            self.assertRegex(err.args[0], ".*Disconnect.*failed.*")

    @patch('jnpr.toby.jdm.jdm_vnf.disconnect_from_device', side_effect=Exception("test-msg"))
    def test_disconnect_ssh_to_vnf_via_jdm_exception_1(self, patch_disconnect):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_ssh_handles = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"] = {}
        jdm_vnf_obj.vnf_ssh_handles["r0"]["centos"] = None
        jdm_vnf_obj.vnf_ssh_handles["r0"]["new-centos"] = 1

        try: 
            self.assertEqual(jdm_vnf_obj.disconnect_ssh_to_vnf_via_jdm("r0", "new-centos"), True)
        except Exception as err:
            self.assertRegex(err.args[0], ".*test-msg.*")

    @patch('jnpr.toby.jdm.jdm_vnf.disconnect_from_device', return_value=True)
    def test_disconnect_ssh_to_vnf_via_jdm_exception_2(self, patch_disconnect):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_ssh_handles = "Test"

        try:
            self.assertEqual(jdm_vnf_obj.disconnect_ssh_to_vnf_via_jdm("r0", "new-centos"), True)
        except Exception as err:
            self.assertRegex(err.args[0], ".*test-msg.*")
   
    @patch('jnpr.toby.jdm.jdm_vnf.execute_shell_command_on_device', return_value=True)
    @patch('jnpr.toby.jdm.jdm_vnf.close_device_handle', return_value=True)
    def test_disconnect_console_to_vnf_via_jdm(self, patch_disconnect, patch_exec):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_console_handles = {}
        jdm_vnf_obj.vnf_console_handles["r0"] = {}
        jdm_vnf_obj.vnf_console_handles["r0"]["centos"] = 1
        jdm_vnf_obj.vnf_console_handles["r0"]["new-centos"] = None

        jdm_vnf_obj.vnf_type = {}
        jdm_vnf_obj.vnf_type["r0"] = {}
        jdm_vnf_obj.vnf_type["r0"]["centos"] = "junos"
        jdm_vnf_obj.vnf_type["r0"]["new-centos"] = None

        self.assertEqual(jdm_vnf_obj.disconnect_console_to_vnf_via_jdm("r0", "centos"), True)
        self.assertEqual(jdm_vnf_obj.disconnect_console_to_vnf_via_jdm("r0", "new-centos"), True)

    @patch('jnpr.toby.jdm.jdm_vnf.execute_shell_command_on_device', return_value=True)
    @patch('jnpr.toby.jdm.jdm_vnf.close_device_handle', return_value=True)
    def test_disconnect_console_to_vnf_via_jdm_exception_1(self, patch_disconnect, patch_exec):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_console_handles = "test"

        try:
            self.assertEqual(jdm_vnf_obj.disconnect_console_to_vnf_via_jdm("r0", "centos"), True)
        except Exception as err:
            self.assertRegex(err.args[0], ".*Exception Raised in disconnect_console_to_vn.*")

    @patch('jnpr.toby.jdm.jdm_vnf.execute_shell_command_on_device', side_effect=Exception("test-msg"))
    @patch('jnpr.toby.jdm.jdm_vnf.close_device_handle', return_value=True)
    def test_disconnect_console_to_vnf_via_jdm_exception_2(self, patch_disconnect, patch_exec):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_console_handles = {}
        jdm_vnf_obj.vnf_console_handles["r0"] = {}
        jdm_vnf_obj.vnf_console_handles["r0"]["centos"] = 1
        jdm_vnf_obj.vnf_console_handles["r0"]["new-centos"] = None

        jdm_vnf_obj.vnf_type = {}
        jdm_vnf_obj.vnf_type["r0"] = {}
        jdm_vnf_obj.vnf_type["r0"]["centos"] = "junos"
        jdm_vnf_obj.vnf_type["r0"]["new-centos"] = None

        try:
            self.assertEqual(jdm_vnf_obj.disconnect_console_to_vnf_via_jdm("r0", "centos"), True)
        except Exception as err:
            self.assertRegex(err.args[0], ".*Exception in sending exit command.*")

    @patch('jnpr.toby.jdm.jdm_vnf.execute_shell_command_on_device', return_value=True)
    @patch('jnpr.toby.jdm.jdm_vnf.close_device_handle',  side_effect=Exception("test-msg"))
    def test_disconnect_console_to_vnf_via_jdm_exception_3(self, patch_disconnect, patch_exec):

        jdm_vnf_obj = jdm_vnf()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        jdm_vnf_obj.vnf_console_handles = {}
        jdm_vnf_obj.vnf_console_handles["r0"] = {}
        jdm_vnf_obj.vnf_console_handles["r0"]["centos"] = 1
        jdm_vnf_obj.vnf_console_handles["r0"]["new-centos"] = None

        jdm_vnf_obj.vnf_type = {}
        jdm_vnf_obj.vnf_type["r0"] = {}
        jdm_vnf_obj.vnf_type["r0"]["centos"] = "junos"
        jdm_vnf_obj.vnf_type["r0"]["new-centos"] = None

        try:
            self.assertEqual(jdm_vnf_obj.disconnect_console_to_vnf_via_jdm("r0", "centos"), True)
        except Exception as err:
            self.assertRegex(err.args[0], ".*Closing Console Handle failed to VNF.*")

if __name__ =='__main__':
    unittest.main()
