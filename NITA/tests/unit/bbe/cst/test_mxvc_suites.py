import unittest
import builtins
import itertools
from unittest.mock import MagicMock
from unittest.mock import patch
import jnpr.toby.bbe.cst.mxvc_suites as mxvc_suites


class TestMxvcSuites(unittest.TestCase):
    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.router = MagicMock()
        builtins.t.get_handle.return_value = self.router
        builtins.bbe = MagicMock()
        
    @patch("time.sleep")
    @patch("re.match")
    @patch("random.choice")
    @patch("jnpr.toby.bbe.cst.cstutils.get_vcp_ports")
    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary_by_port")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_mxvc_vcp_link_down_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_stop_traffic,
                                     patch_verify_traffic, patch_get_router_sub_summary_by_port, patch_get_master_re_name,
                                     patch_get_vcp_ports, patch_random_choice, patch_re_match, patch_sleep):
        patch_get_master_re_name.return_value = "primary-secondary"
        self.assertEqual(mxvc_suites.mxvc_vcp_link_down_test(), None)
        patch_get_router_sub_summary_by_port.side_effect = itertools.count()
        with self.assertRaises(Exception) as context:
            mxvc_suites.mxvc_vcp_link_down_test()
        self.assertIn("mxvc vcp link down test failed in iteration ", context.exception.args[0])
        self.router.cli.side_effect = itertools.count()
        self.assertEqual(mxvc_suites.mxvc_vcp_link_down_test(), None)

        self.router.cli = MagicMock()

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_run_pfe_command")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_get_task_memory")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_pfe_resource_monitor")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.cstutils.power_manager")
    @patch("jnpr.toby.bbe.cst.cstutils.check_gres_ready")
    @patch("jnpr.toby.bbe.cst.cstutils.get_vcp_ports")
    @patch("jnpr.toby.bbe.cst.cstutils.get_re_fpc_memory")
    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_client_count")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_mxvc_chassis_reboot(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_stop_traffic,
                                 patch_verify_traffic, patch_verify_client_count, patch_get_router_sub_summary,
                                 patch_get_master_re_name, patch_get_re_fpc_memory, patch_get_vcp_ports, patch_check_gres_ready,
                                 patch_power_manager, patch_dtcp_add_li_trigger, patch_dtcp_delete_li_trigger,
                                 patch_healthcheck_pfe_resource_monitor, patch_healthcheck_get_task_memory,
                                 patch_healthcheck_run_pfe_command, patch_cpu_settle, patch_sleep):
        kwargs = {
            "dtcp_test": True,
            "health_check": True,
            "method": "cli",
            "chassis": "VC-STDBY-RE-ALL"
        }
        self.assertEqual(mxvc_suites.mxvc_chassis_reboot(**kwargs), None)
        kwargs["chassis"] = "VC-M"
        self.router.detect_master_node.return_value = "primary"
        self.assertEqual(mxvc_suites.mxvc_chassis_reboot(**kwargs), None)
        self.router.detect_master_node.return_value = "secondary"
        self.assertEqual(mxvc_suites.mxvc_chassis_reboot(**kwargs), None)
        kwargs["chassis"] = "VC-B"
        self.router.detect_master_node.return_value = "primary"
        self.assertEqual(mxvc_suites.mxvc_chassis_reboot(**kwargs), None)
        self.router.detect_master_node.return_value = "secondary"
        self.assertEqual(mxvc_suites.mxvc_chassis_reboot(**kwargs), None)
        kwargs["method"] = "powercycle"
        self.assertEqual(mxvc_suites.mxvc_chassis_reboot(**kwargs), None)

        self.router.detect_master_node = MagicMock()

    @patch("time.sleep")
    @patch("time.time")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_run_pfe_command")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_get_task_memory")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_pfe_resource_monitor")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.cstutils.get_vcp_ports")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_rt_subs_info")
    @patch("jnpr.toby.bbe.cst.cstutils.get_re_fpc_memory")
    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    @patch("jnpr.toby.bbe.cst.cstutils.get_configured_subs")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_release_clients")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_start_clients")
    @patch("jnpr.toby.bbe.cst.cstutils.check_gres_ready")
    @patch("jnpr.toby.bbe.cst.cstutils.check_fpc")
    @patch("jnpr.toby.bbe.cst.cstutils.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_mxvc_blackout_period_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_stop_traffic,
                                       patch_check_fpc, patch_check_gres_ready, patch_cst_starts_clients, patch_cst_release_clients,
                                       patch_get_configured_subs, patch_get_master_re_name, patch_get_re_fpc_memory, patch_get_rt_subs_info,
                                       patch_get_router_sub_summary, patch_get_vcp_ports, patch_dtcp_add_li_trigger,
                                       patch_dtcp_delete_li_trigger, patch_healthcheck_pfe_resource_monitor, patch_healthcheck_get_task_memory,
                                       patch_healthcheck_run_pfe_command, patch_cpu_settle, patch_time, patch_sleep):
        # Make time go up by 1 sec every time it is called
        patch_time.side_effect = itertools.count()

        builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
        patch_get_rt_subs_info.return_value = {
            "rt_sessions_up": 5,
            "rt_sessions_down": 5
        }
        patch_get_configured_subs.return_value = {
            "expected_total_session_in_testers": 0
        }
        kwargs = {
            "dtcp_test": True,
            "health_check": True
        }
        self.assertEqual(mxvc_suites.mxvc_blackout_period_test(**kwargs), None)
        patch_get_rt_subs_info.side_effect = [
            {
                "rt_sessions_up": 5,
                "rt_sessions_down": 5
            },
            {
                "rt_sessions_up": 6,
                "rt_sessions_down": 6
            }
        ]
        self.assertEqual(mxvc_suites.mxvc_blackout_period_test(**kwargs), None)

        builtins.bbe.get_subscriber_handles = MagicMock()

    @patch("time.sleep")
    @patch("time.time")
    @patch("random.choice")
    @patch("re.search")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_run_pfe_command")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_get_task_memory")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_pfe_resource_monitor")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_list_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_re_fpc_memory")
    @patch("jnpr.toby.bbe.cst.cstutils.get_pic_info")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_mxvc_fpc_mic_reboot_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_get_pic_info,
                                      patch_get_re_fpc_memory, patch_get_router_sub_summary, patch_dtcp_add_li_trigger,
                                      patch_dtcp_delete_li_trigger, patch_dtcp_list_li_trigger, patch_healthcheck_pfe_resource_monitor,
                                      patch_healthcheck_get_task_memory, patch_healthcheck_run_pfe_command, patch_re_search,
                                      patch_random_choice, patch_time, patch_sleep):
        # Make time go up by 1 sec every time it is called
        patch_time.side_effect = itertools.count()

        patch_re_search.side_effect = itertools.cycle([True, True, False])
        kwargs = {
            "dtcp_test": True,
            "health_check": True,
            "component": "fpc",
            "method": "panic"
        }
        self.assertEqual(mxvc_suites.mxvc_fpc_mic_reboot_test(**kwargs), None)
        kwargs["method"] = "offline"
        self.assertEqual(mxvc_suites.mxvc_fpc_mic_reboot_test(**kwargs), None)
        kwargs['slot_info'] = {"member": "member", "slot": "slot"}
        patch_get_pic_info.return_value = {"member": {"slot": ["0", "1", "2", "3", "MPC"]}}
        self.assertEqual(mxvc_suites.mxvc_fpc_mic_reboot_test(**kwargs), None)
        kwargs["component"] = "pic"
        self.assertEqual(mxvc_suites.mxvc_fpc_mic_reboot_test(**kwargs), None)
        kwargs["component"] = "mic"
        self.assertEqual(mxvc_suites.mxvc_fpc_mic_reboot_test(**kwargs), None)

        kwargs["component"] = "fpc"
        patch_re_search.side_effect = None
        patch_re_search.return_value = False
        with self.assertRaises(Exception) as context:
            mxvc_suites.mxvc_fpc_mic_reboot_test(**kwargs)
        self.assertIn(" failed to transit to the expected state", context.exception.args[0])

    @patch("time.sleep")
    @patch("builtins.input")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_run_pfe_command")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_get_task_memory")
    @patch("jnpr.toby.bbe.cst.cst_healthcheck.healthcheck_pfe_resource_monitor")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_list_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.cstutils.panic_re_recover")
    @patch("jnpr.toby.bbe.cst.cstutils.get_vcp_ports")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_re_fpc_memory")
    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    @patch("jnpr.toby.bbe.cst.cstutils.check_link_status")
    @patch("jnpr.toby.bbe.cst.cstutils.check_gres_ready")
    @patch("jnpr.toby.bbe.cst.cstutils.check_fpc")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_mxvc_gres_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_stop_traffic, patch_verify_traffic,
                            patch_check_fpc, patch_check_gres_ready, patch_check_link_status, patch_get_master_re_name,
                            patch_get_re_fpc_memory, patch_get_router_sub_summary, patch_get_vcp_ports, patch_panic_re_recover,
                            patch_dtcp_add_li_trigger, patch_dtcp_delete_li_trigger, patch_dtcp_list_li_trigger,
                            patch_healthcheck_pfe_resource_monitor, patch_healthcheck_get_task_memory,
                            patch_healthcheck_run_pfe_command, patch_cpu_settle, patch_input, patch_sleep):
        kwargs = {
            "dtcp_test": True,
            "health_check": True,
            "gres_type": "global",
            "gres_method": "cli"
        }
        self.assertEqual(mxvc_suites.mxvc_gres_test(**kwargs), None)
        kwargs["gres_method"] = "kernel_crash"
        self.assertEqual(mxvc_suites.mxvc_gres_test(**kwargs), None)
        kwargs["gres_method"] = "scb_failover"
        self.assertEqual(mxvc_suites.mxvc_gres_test(**kwargs), None)
        kwargs["gres_type"] = "localbackup"
        kwargs["gres_method"] = "reboot"
        self.assertEqual(mxvc_suites.mxvc_gres_test(**kwargs), None)
        kwargs["gres_method"] = "cli"
        self.assertEqual(mxvc_suites.mxvc_gres_test(**kwargs), None)
        patch_get_master_re_name.side_effect = [MagicMock(), MagicMock()]
        self.assertEqual(mxvc_suites.mxvc_gres_test(**kwargs), None)
        patch_get_master_re_name.side_effect = None

        self.router.cli.return_value.resp = "error"
        with self.assertRaises(Exception) as context:
            mxvc_suites.mxvc_gres_test(**kwargs)
        self.assertIn("failed to execute local switch", context.exception.args[0])

        self.router.cli = MagicMock()

if __name__ == "__main__":
    unittest.main()
