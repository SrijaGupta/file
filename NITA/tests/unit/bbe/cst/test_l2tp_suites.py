import unittest
import builtins
import itertools
from unittest.mock import MagicMock
from unittest.mock import patch
import jnpr.toby.bbe.cst.l2tp_suites as l2tp_suites


class TestL2tpSuites(unittest.TestCase):
    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.router = MagicMock()
        builtins.t.get_handle.return_value = self.router
        builtins.bbe = MagicMock()
        
    @patch("time.sleep")
    @patch("time.time")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.set_bbe_junos_util_device_handle")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.cstsuites.unicast_traffic_test")
    @patch("jnpr.toby.bbe.cst.cstutils.get_rt_subs_info")
    @patch("jnpr.toby.bbe.cst.cstutils.get_configured_subs")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_client_count")
    @patch("jnpr.toby.bbe.cst.cstutils.get_aaa_accounting_stats")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_start_clients")
    @patch("jnpr.toby.bbe.cst.cstutils.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_l2tp_disconnect_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_stop_traffic,
                                  patch_cst_start_clients, patch_get_aaa_accounting_stats, patch_verify_client_count,
                                  patch_get_configured_subs, patch_get_rt_subs_info, patch_unicast_traffic_test,
                                  patch_dtcp_add_li_trigger, patch_dtcp_delete_li_trigger,
                                  patch_set_bbe_junos_util_device_handle, patch_cpu_settle, patch_time, patch_sleep):
        # Make time go up by 60 sec every time it is called
        patch_time.side_effect = itertools.count(step=60)

        builtins.bbe.get_devices.return_value = ["r0"]
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
        result = MagicMock()
        patch_get_configured_subs.return_value = result
        patch_get_rt_subs_info.return_value = result
        resp = self.router.pyez.return_value.resp
        resp.findtext.return_value = 0
        kwargs = {"dtcp_test": True}
        self.assertEqual(l2tp_suites.l2tp_disconnect_test(**kwargs), None)

        resp.findtext.return_value = 1
        with self.assertRaises(Exception) as context:
            l2tp_suites.l2tp_disconnect_test(**kwargs)
        self.assertIn("failed to clear session or tunnel in iteration ", context.exception.args[0])
        kwargs["clear_by"] = "session"
        kwargs["check_tunnel_close"] = True
        with self.assertRaises(Exception) as context:
            l2tp_suites.l2tp_disconnect_test(**kwargs)
        self.assertIn("failed to clear session or tunnel in iteration ", context.exception.args[0])
        kwargs["clear_by"] = "tunnel"
        with self.assertRaises(Exception) as context:
            l2tp_suites.l2tp_disconnect_test(**kwargs)
        self.assertIn("failed to clear session or tunnel in iteration ", context.exception.args[0])
        patch_get_configured_subs.return_value = MagicMock()
        patch_get_rt_subs_info.return_value = MagicMock()
        with self.assertRaises(Exception) as context:
            l2tp_suites.l2tp_disconnect_test(**kwargs)
        self.assertIn(" in tester is not the same as expected ", context.exception.args[0])
        patch_verify_client_count.side_effect = Exception
        with self.assertRaises(Exception) as context:
            l2tp_suites.l2tp_disconnect_test(**kwargs)
        self.assertIn("clients failed to reach the specified count after 1800s", context.exception.args[0])

        self.router.pyez = MagicMock()
        builtins.bbe.get_devices = MagicMock()
        builtins.bbe.get_subscriber_handles = MagicMock()

    @patch("time.sleep")
    @patch("time.time")
    @patch("random.choice")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.set_bbe_junos_util_device_handle")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_list_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.cstsuites.unicast_traffic_test")
    @patch("jnpr.toby.bbe.cst.cstutils.get_aaa_accounting_stats")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_start_clients")
    @patch("jnpr.toby.bbe.cst.cstutils.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_lns_cluster_failover_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_stop_traffic,
                                       patch_cst_start_clients, patch_get_router_sub_summary, patch_get_aaa_accounting_stats,
                                       patch_unicast_traffic_test, patch_dtcp_add_li_trigger, patch_dtcp_delete_li_trigger,
                                       patch_dtcp_list_li_trigger, patch_set_bbe_junos_util_device_handle,
                                       patch_cpu_settle, patch_random_choice, patch_time, patch_sleep):
        # Make time go up by 60 sec every time it is called
        patch_time.side_effect = itertools.count(step=60)

        kwargs = {"dtcp_test": True}
        builtins.bbe.get_devices.return_value = ["r0"]
        builtins.bbe.get_interfaces.return_value = [MagicMock()]
        get_router_sub_summary_iterator = itertools.count()
        self.assertEqual(l2tp_suites.lns_cluster_failover_test(**kwargs), None)
        patch_get_router_sub_summary.side_effect = lambda x: {"client": next(get_router_sub_summary_iterator)}
        with self.assertRaises(Exception) as context:
            l2tp_suites.lns_cluster_failover_test(**kwargs)
        self.assertIn("client count is not stable after 1200s", context.exception.args[0])

        builtins.bbe.get_devices = MagicMock()
        builtins.bbe.get_interfaces = MagicMock()
        builtins.bbe.get_router_sub_summary = MagicMock()

    @patch("random.choice")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_release_clients")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_start_clients")
    def test_lns_load_balance_test(self, patch_cst_start_clients, patch_cst_release_clients, patch_random_choice):
        builtins.bbe.get_devices.return_value = [MagicMock()]
        self.assertEqual(l2tp_suites.lns_load_balance_test(), None)

        builtins.bbe.get_devices = MagicMock()

if __name__ == "__main__":
    unittest.main()
