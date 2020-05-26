import unittest
import builtins
import itertools
from unittest.mock import MagicMock
from unittest.mock import patch
import jnpr.toby.bbe.cst.cst_healthcheck as csthealthcheck


class TestCstHealthcheck(unittest.TestCase):
    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.router = MagicMock()
        builtins.t.get_handle.return_value = self.router
        builtins.bbe = MagicMock()
        builtins.bbe.get_devices.return_value = ["r0"]
        
    def test_healthcheck_pfe_resource_monitor(self):
        fpc_info_dict = {
            "fpc-slot": "0",
            "fpc-client-session-denied-count": "0",
            "fpc-service-session-denied-count": "0",
            "used-heap-mem": "279233552",
            "used-heap-mem-percent": "16"
        }
        pfe_info_dict = {
            "pfe-num": "0",
            "used-filter-counter": "17950080",
            "used-filter-counter-percent": "37",
            "used-ifl-counter": "730816",
            "used-ifl-counter-percent": "2"
        }
        fpc_info = MagicMock()
        fpc_info.findtext.side_effect = lambda x: fpc_info_dict[x]
        pfe_info = MagicMock()
        pfe_info.findtext.side_effect = lambda x: pfe_info_dict[x]

        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [fpc_info]
        fpc_info.findall.return_value = [pfe_info]

        expected_result = {
            "r0": {
                "fpc0": {
                    "fpc-client-session-denied-count": "0",
                    "fpc-service-session-denied-count": "0",
                    "used-heap-mem": "279233552",
                    "used-heap-mem-percent": "16"
                },
                "fpc0_pfe_0": {
                    "used-filter-counter": "17950080",
                    "used-filter-counter-percent": "37",
                    "used-ifl-counter": "730816",
                    "used-ifl-counter-percent": "2"
                }
            }
        }
        self.assertEqual(csthealthcheck.healthcheck_pfe_resource_monitor(), expected_result)

        pfe_info.findtext.side_effect = None
        pfe_info.findtext.return_value = False
        del expected_result["r0"]["fpc0_pfe_0"]
        self.assertEqual(csthealthcheck.healthcheck_pfe_resource_monitor(), expected_result)

        self.router.pyez = MagicMock()

    def test_healthcheck_get_kernel_mem(self):
        self.router.shell.return_value.resp = "vm.kmem_size:0\r\nvm.kmem_map_free:3"

        expected_result = {
            "r0": {
                "vm.kmem_size": "0",
                "vm.kmem_map_free": "3"
            }
        }
        self.assertEqual(csthealthcheck.healthcheck_get_kernel_mem(), expected_result)

        self.router.shell = MagicMock()

    def test_healthcheck_get_task_memory(self):
        resp_dict = {
            "task-memory-dynamic-allocs": 0,
            "task-memory-bss-bytes": 1,
            "task-memory-page-data-bytes": 2,
            "task-memory-dir-bytes": 3,
            "task-memory-total-bytes-in-use": 4
        }
        resp = self.router.pyez.return_value.resp
        resp.findtext.side_effect = lambda x: resp_dict[x]

        expected_result = {
            "name": "virtual_memory",
            "r0": {
                "Dynamically allocated memory": 0,
                "Program data+BSS memory": 1,
                "Page data overhead": 2,
                "Page directory size": 3,
                "Total bytes in use": 4
            }
        }
        self.assertEqual(csthealthcheck.healthcheck_get_task_memory(), expected_result)

        self.router.pyez = MagicMock()

    @patch("re.match")
    def test_healthcheck_run_pfe_command(self, patch_re_match):
        interface = MagicMock()
        interface.__contains__.return_value = True
        builtins.t.resources = {
            "r0": {
                "interfaces": [interface, interface]
            }
        }
        patch_re_match.return_value.group.side_effect = [20, 12]
        self.router.get_model.side_effect = ["mx2020", "m40"]
        self.assertEqual(csthealthcheck.healthcheck_run_pfe_command("cmd"), None)
        self.router.vc = False
        patch_re_match.return_value.group.side_effect = [20, 12]
        self.assertEqual(csthealthcheck.healthcheck_run_pfe_command("cmd"), None)

        self.router.vc = MagicMock()
        self.router.get_model = MagicMock()
        builtins.t.resources = MagicMock()

    @patch("builtins.print")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    def test_healthcheck_get_re_memory(self, patch_get_router_sub_summary, patch_print):
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [MagicMock()]
        resp.findall.return_value[0].findall.return_value = [MagicMock()]
        self.assertEqual(csthealthcheck.healthcheck_get_re_memory(), None)
        self.router.vc = False
        del builtins.t.re_mem_stats
        self.assertEqual(csthealthcheck.healthcheck_get_re_memory(), None)

        self.router.pyez = MagicMock()
        self.router.vc = MagicMock()
        builtins.t.re_mem_stats = MagicMock()

    @patch("builtins.print")
    @patch("re.sub")
    def test_healthcheck_get_shell_stats(self, patch_re_sub, patch_print):
        self.assertEqual(csthealthcheck.healthcheck_get_shell_stats(), None)

    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    def test_healthcheck_isvty_dfw_statesync(self, patch_get_master_re_name):
        self.router.current_node.controllers.keys.return_value.__len__.return_value = 2
        controller = self.router.current_node.current_controller
        controller.re_name = "member0"
        controller.is_master.return_value = True
        self.assertEqual(csthealthcheck.healthcheck_isvty_dfw_statesync(), None)
        controller.re_name = "member1"
        self.assertEqual(csthealthcheck.healthcheck_isvty_dfw_statesync(), None)
        self.router.vc = False
        builtins.t.get_resource.return_value = {"system": {"primary": {"controllers": [MagicMock(), MagicMock()]}}}
        self.router.cli.return_value.resp.split.return_value.__getitem__.side_effect = [MagicMock(), MagicMock()]
        with self.assertRaises(Exception) as context:
            csthealthcheck.healthcheck_isvty_dfw_statesync()
        self.assertIn("Master and standby RE bbe_dwf_state are NOT in sync.", context.exception.args[0])
        #self.assertEqual(csthealthcheck.healthcheck_isvty_dfw_statesync(), None)

        self.router.cli = MagicMock()
        self.router.current_node = MagicMock()
        self.router.vc = MagicMock()
        builtins.t.get_resource = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary_by_slot")
    def test_healthcheck_get_pfe_vty_jnhstats(self, patch_get_router_sub_summary_by_slot, patch_get_master_re_name):
        patch_get_router_sub_summary_by_slot.return_value = [MagicMock()]
        self.assertTrue(csthealthcheck.healthcheck_get_pfe_vty_jnhstats())
        self.router.vty.return_value.resp = "FLOW FAILED"
        with self.assertRaises(Exception) as context:
            csthealthcheck.healthcheck_get_pfe_vty_jnhstats()
        self.assertIn("jnh stats health check failed", context.exception.args[0])
        self.router.vty = MagicMock()

    def test_healthcheck_hasbbe_sdb_throttle_replication_on_off(self):
        self.assertTrue(csthealthcheck.healthcheck_hasbbe_sdb_throttle_replication_on_off())
        self.router.cli.return_value.resp = "BBE_SDB_THROTTLE_REPLICATION_ON"
        with self.assertRaises(Exception) as context:
            csthealthcheck.healthcheck_hasbbe_sdb_throttle_replication_on_off()
        self.assertIn('Found BBE_SDB_THROTTLE_REPLICATION_ON/OFF', context.exception.args[0])

        self.router.cli = MagicMock()

    def test_healthcheck_isbbe_ss_state_change(self):
        self.router.cli.return_value.resp = "BBE_SS_STATE_CHANGE 1 2 3 4 2"
        self.assertTrue(csthealthcheck.healthcheck_isbbe_ss_state_change())
        self.router.cli.return_value.resp = "BBE_SS_STATE_CHANGE 1 2 3 4 5"
        with self.assertRaises(Exception) as context:
            csthealthcheck.healthcheck_isbbe_ss_state_change()
        self.assertIn('BBE_SS_STATE_CHANGE count should not exceed 2', context.exception.args[0])
        self.router.cli = MagicMock()

    def test_healthcheck_shmlog_statserr(self):
        self.assertEqual(csthealthcheck.healthcheck_shmlog_statserr(), None)

    def test_healthcheck_get_bbe_vtystats(self):
        self.router.current_node.controllers.keys.return_value.__len__.return_value = 2
        self.assertEqual(csthealthcheck.healthcheck_get_bbe_vtystats(), None)

        self.router.current_node = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    def test_healthcheck_vtycos_statesync(self, patch_get_master_re_name):
        self.router.current_node.controllers.keys.return_value.__len__.return_value = 2
        self.router.current_node.current_controller.re_name = "member0"
        self.assertTrue(csthealthcheck.healthcheck_vtycos_statesync())
        self.router.current_node.current_controller.re_name = "member1"
        self.assertTrue(csthealthcheck.healthcheck_vtycos_statesync())
        self.router.vc = False
        builtins.t.get_resource.return_value = {"system": {"primary": {"controllers": [MagicMock(), MagicMock()]}}}
        self.router.cli.side_effect = itertools.cycle([MagicMock(resp=MagicMock()), MagicMock(resp=MagicMock())])
        with self.assertRaises(Exception) as context:
            csthealthcheck.healthcheck_vtycos_statesync()
        self.assertIn('Master and Standby RE files are not in sync', context.exception.args[0])

        self.router.cli = MagicMock()
        self.router.current_node = MagicMock()
        self.router.vc = MagicMock()
        builtins.t.get_resource = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    def test_healthcheck_get_storage_dev_md12(self, patch_get_router_sub_summary):
        self.assertEqual(csthealthcheck.healthcheck_get_storage_dev_md12(), None)
        self.router.vc = False
        self.assertEqual(csthealthcheck.healthcheck_get_storage_dev_md12(), None)
        del builtins.t.StorageDevMd12
        self.assertEqual(csthealthcheck.healthcheck_get_storage_dev_md12(), None)

        self.router.vc = MagicMock()
        builtins.t.StorageDevMd12 = MagicMock()

    def test_healthcheck_verify_memorymapped_filesystemalloc(self):
        self.assertTrue(csthealthcheck.healthcheck_verify_memorymapped_filesystemalloc())
        mock = MagicMock()
        mock.__float__.return_value = -1.0
        builtins.t.StorageDevMd12.__getitem__.return_value.__getitem__.return_value.__getitem__.return_value = mock
        with self.assertRaises(Exception) as context:
            csthealthcheck.healthcheck_verify_memorymapped_filesystemalloc()
        self.assertIn('storage_dev_md12 size changed after the action', context.exception.args[0])

        builtins.t.StorageDevMd12 = MagicMock()

    def test_healthcheck_verify_rememory(self):
        builtins.t.re_mem_stats = [
            {
                "r0": {
                    "not": "not",
                    "re": {
                        "memory-utilization": 1.0
                    },
                    "active-count": 5
                }
            },
            {
                "r0": {
                    "not": "not",
                    "re": {
                        "memory-utilization": 1.0
                    },
                    "active-count": 3
                }
            },
        ]
        self.assertTrue(csthealthcheck.healthcheck_verify_rememory())
        builtins.t.re_mem_stats[-2]["r0"]["re"]["memory-utilization"] = -1.0
        builtins.t.re_mem_stats[-1]["r0"]["re"]["memory-utilization"] = -1.0
        with self.assertRaises(Exception) as context:
            csthealthcheck.healthcheck_verify_rememory()
        self.assertIn('RE memory health check failed', context.exception.args[0])
        builtins.t.re_mem_stats[-2]["r0"]["active-count"] = 3
        with self.assertRaises(Exception) as context:
            csthealthcheck.healthcheck_verify_rememory()
        self.assertIn('RE memory health check failed', context.exception.args[0])

        builtins.t.re_mem_stats = MagicMock()

    def test_healthcheck_test_preambleactions(self):
        self.assertEqual(csthealthcheck.healthcheck_test_preambleactions(), None)

    def test_healthcheck_dhcppacketstats(self):
        self.assertEqual(csthealthcheck.healthcheck_dhcppacketstats(), None)

if __name__ == "__main__":
    unittest.main()
