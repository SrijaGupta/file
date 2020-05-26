import unittest
import builtins
import itertools
from unittest.mock import MagicMock
from unittest.mock import patch
import jnpr.toby.bbe.cst.cstutils as cst

# builtins.t = MagicMock()
# builtins.t.log = MagicMock()
# router = MagicMock()
# builtins.t.get_handle.return_value = router
# builtins.bbe = MagicMock()

class TestCstUtils(unittest.TestCase):
    """
    TestCstUtils class to handle cstutils.py unit tests
    """
    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.router = MagicMock()
        builtins.t.get_handle.return_value = self.router
        builtins.bbe = MagicMock()


    @patch("time.sleep")
    @patch("time.time")
    def test_check_link_status(self, patch_time, patch_sleep):
        self.router.invoke.return_value = {"status": "1"}
        obj1 = MagicMock()
        obj2 = MagicMock()
        builtins.bbe.get_interfaces.return_value = [obj1]
        builtins.bbe.get_connection.return_value = [obj2]
        obj3 = MagicMock()
        obj3.findtext.return_value = 'up'
        builtins.t.get_handle.return_value.pyez.return_value.resp.findall.return_value = [obj3]
        self.assertEqual(cst.check_link_status(), None)
        patch_time.side_effect = itertools.count(step=10)
        obj4 = MagicMock()
        obj4.findtext.return_value = 'down'
        builtins.t.get_handle.return_value.pyez.return_value.resp.findall.return_value = [obj4]
        with self.assertRaises(Exception) as context:
            cst.check_link_status()
        self.assertIn("some interfaces are still down after 600s", context.exception.args[0])
        patch_time.side_effect = None
        builtins.t.__getitem__.return_value.__getitem__.return_value = {"system": {"primary": {"make": "ixia"}}}
        self.router.invoke.return_value = {"status": "0"}
        with self.assertRaises(Exception) as context:
            cst.check_link_status()
        self.assertIn("some links in rt has problem, please check connections", context.exception.args[0])
        # patch_time.side_effect = itertools.count(step=10)
        # self.router.invoke.return_value = {"status": "1"}
        # builtins.t.get_interfaces_name.return_value = ["access0"]
        # obj1 = MagicMock()
        # obj1.findtext.return_value = "up"
        # self.assertEqual(cst.check_link_status(), None)
        #
        # obj1.findtext.return_value = "down"
        # resp = self.router.pyez.return_value.resp
        # resp.findall.return_value = [obj1]
        # with self.assertRaises(Exception) as context:
        #     cst.check_link_status()
        # self.assertIn("some interfaces are still down after 600s", context.exception.args[0])
        # builtins.t.__getitem__.return_value.__getitem__.return_value = {"system": {"primary": {"make": "ixia"}}}
        # self.router.invoke.return_value = {"status": "0"}
        # with self.assertRaises(Exception) as context:
        #     cst.check_link_status()
        # self.assertIn("some links in rt has problem, please check connections", context.exception.args[0])
        #
        # self.router.invoke = MagicMock()
        # self.router.pyez = MagicMock()
        # builtins.t.get_interfaces_name = MagicMock()
        # patch_time.side_effect = None

    @patch('jnpr.toby.bbe.cst.cstutils.time.sleep')
    @patch("jnpr.toby.bbe.cst.cstutils.start_rt_links")
    def test_prepare_rt_before_login(self, patch_start_rt_links, patch_sleep):
        obj1 = MagicMock()
        obj1.family = "dual"
        obj1.has_ancp = True
        obj1.rt_ancp_handle = "h1"
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.router.ae = {"handle": ["h1"]}
        builtins.t.user_variables = {"uv-bbevar": {"start-ancp-before-test": "1"}}
        builtins.t.__getitem__.return_value.__getitem__.return_value = {"system": {"primary": {"make": "ixia"}}}
        self.router.invoke.return_value = [MagicMock()]
        self.router.version = "8.41"
        self.assertEqual(cst.prepare_rt_before_login(), None)
        obj2 = MagicMock()
        builtins.bbe.get_interfaces.return_value = [obj2]
        self.assertEqual(cst.prepare_rt_before_login(autoneg=False), None)

        self.router.ae = MagicMock()
        self.router.version = MagicMock()
        self.router.invoke = MagicMock()
        builtins.t.user_variables = MagicMock()
        builtins.t.__getitem__ = MagicMock()
        builtins.bbe.get_subscriber_handles = MagicMock()

    def test_prepare_router_before_login(self):
        builtins.bbe.get_devices.return_value = ["r0"]
        self.assertEqual(cst.prepare_router_before_login(), None)
        self.router.vc = False
        self.router.current_node.controllers.keys.return_value.__len__.return_value = 2
        self.assertEqual(cst.prepare_router_before_login(), None)

        self.router.vc = MagicMock()
        self.router.current_node = MagicMock()
        builtins.bbe.get_devices = MagicMock()

    @patch('jnpr.toby.bbe.cst.cstutils.time.sleep')
    @patch('jnpr.toby.bbe.cst.cstutils.time.time')
    @patch("threading.Thread")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_client_route")
    @patch("jnpr.toby.bbe.cst.cstutils.clear_subscribers_in_router")
    @patch("jnpr.toby.bbe.cst.cstutils.get_rt_subs_info")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_route_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_re_fpc_memory")
    @patch("jnpr.toby.bbe.cst.cstutils.get_fpc_vty_stats")
    @patch("jnpr.toby.bbe.cst.cstutils.get_configured_subs")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_release_clients")
    def test_cst_start_clients(self, patch_cst_release_clients, patch_get_configured_subs, patch_get_fpc_vty_stats,
                               patch_get_re_fpc_memory, patch_get_route_summary, patch_get_router_sub_summary,
                               patch_get_rt_subs_info, patch_clear_subscribers_in_router, patch_verify_client_route,
                               patch_cpu_settle, patch_thread, patch_time, patch_sleep):
        # Make time go up by 5 sec every time it is called
        patch_time.side_effect = itertools.count(step=5)

        sub = MagicMock(rt_state="started")
        patch_get_configured_subs.return_value = {
            "expected_login_rate": 50,
            "expected_total_session_in_testers": 10,
            "expected_total_session_in_routers": 10
        }
        builtins.bbe.cst_stats = {"partial_login": 0}
        kwargs = {
            "subs": sub,
            "collect_pfe_info": True,
            "check_access_route": "True"
        }
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        kwargs["device_id"] = "rt0"
        del kwargs["subs"]
        builtins.bbe.get_subscriber_handles.return_value = [sub]
        rt_subs_before = {"rt_sessions_up": 0, "rt_sessions_down": 0, "rt_sessions_not_started": 10}
        rt_subs_during = {"rt_sessions_up": 5, "rt_sessions_down": 5, "rt_sessions_not_started": 0}
        rt_subs_during_alt = {"rt_sessions_up": 2, "rt_sessions_down": 2, "rt_sessions_not_started": 6}
        rt_subs_after = {"rt_sessions_up": 10, "rt_sessions_down": 0, "rt_sessions_not_started": 0}

        patch_get_router_sub_summary.side_effect = [{"client": 10}, {"client": 10}, {"client": 10}]
        patch_get_rt_subs_info.side_effect = [rt_subs_during, rt_subs_before, rt_subs_during, rt_subs_after, rt_subs_after]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_after, rt_subs_after]
        patch_get_router_sub_summary.side_effect = [{"client": 10}, {"client": 10}, {"client": 10}]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        patch_get_router_sub_summary.side_effect = [{"client": 10}, {"client": 10}, {"client": 10}]
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_after, rt_subs_after]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        patch_get_router_sub_summary.side_effect = None
        patch_get_router_sub_summary.return_value = {"client": 10}
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_after, rt_subs_after]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        patch_get_rt_subs_info.side_effect = [rt_subs_after, rt_subs_before, rt_subs_during, rt_subs_after, rt_subs_after]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        patch_thread.return_value.is_alive.return_value = False
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_after, rt_subs_after]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_during, rt_subs_after, rt_subs_after, rt_subs_after]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_during_alt,
                                              rt_subs_during_alt, rt_subs_during_alt, rt_subs_during_alt, rt_subs_during_alt,
                                              rt_subs_during_alt, rt_subs_during_alt, rt_subs_after, rt_subs_after, rt_subs_after]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        patch_time.side_effect = itertools.count(step=200)
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_during_alt, rt_subs_after, rt_subs_after, rt_subs_after]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)
        patch_time.side_effect = itertools.count(step=5)

        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_during, rt_subs_during,
                                              rt_subs_during, rt_subs_during, rt_subs_after, rt_subs_after, rt_subs_after, rt_subs_after]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)

        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_after, rt_subs_after]
        patch_get_router_sub_summary.side_effect = [{"client": 5}, {"client": 10}, {"client": 5}]
        with self.assertRaises(Exception) as context:
            cst.cst_start_clients(**kwargs)
        self.assertIn(" subscribers in routers, instead of expected", context.exception.args[0])
        patch_get_router_sub_summary.side_effect = None

        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_during, rt_subs_during,
                                              rt_subs_during, rt_subs_during, rt_subs_during, rt_subs_after, rt_subs_after]
        with self.assertRaises(Exception) as context:
            cst.cst_start_clients(**kwargs)
        #self.assertIn("subscriber still not fully bound after waiting", context.exception.args[0])

        patch_time.side_effect = itertools.count(step=20)
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_during, rt_subs_during,
                                              rt_subs_during, rt_subs_during, rt_subs_during, rt_subs_after, rt_subs_after]
        with self.assertRaises(Exception) as context:
            cst.cst_start_clients(**kwargs)
        #self.assertIn("subscriber still not fully bound after waiting", context.exception.args[0])

        patch_time.side_effect = itertools.count(step=0.001)
        patch_get_rt_subs_info.side_effect = itertools.chain(iter([rt_subs_before, rt_subs_before, rt_subs_during]), itertools.repeat(rt_subs_during))
        with self.assertRaises(Exception) as context:
            cst.cst_start_clients(**kwargs)
        self.assertIn("subscriber failed to be fully bounded after restart retries", context.exception.args[0])

        patch_time.side_effect = itertools.count(step=500)
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during]
        with self.assertRaises(Exception) as context:
            cst.cst_start_clients(**kwargs)
        #self.assertIn("No tx packets was seen in rt stats after 300s, please check", context.exception.args[0])

        patch_time.side_effect = itertools.count(step=0.001)
        patch_get_rt_subs_info.side_effect = itertools.chain(iter([rt_subs_before, rt_subs_before, rt_subs_during]), itertools.repeat(rt_subs_before))
        with self.assertRaises(Exception) as context:
            cst.cst_start_clients(**kwargs)
        self.assertIn("no subscriber login, please check router configurations", context.exception.args[0])

        kwargs["restart_unbound_only"] = True
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before]
        self.assertEqual(cst.cst_start_clients(**kwargs), None)
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before]
        with self.assertRaises(Exception) as context:
            cst.cst_start_clients(**kwargs)
        self.assertIn("some subscriber was not in started state when calling with restart unbound only", context.exception.args[0])
        builtins.bbe.get_subscriber_handles.return_value = [sub]
        del kwargs["restart_unbound_only"]

        kwargs["stabilize_time"] = 10
        patch_time.side_effect = itertools.count(step=5)
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_after, rt_subs_after,
                                              rt_subs_during, rt_subs_after, rt_subs_after, rt_subs_during]
        with self.assertRaises(Exception) as context:
            cst.cst_start_clients(**kwargs)
        #self.assertIn("some subscriber was not in started state when calling with restart unbound only", context.exception.args[0])

        kwargs["stabilize_time"] = 20
        patch_time.side_effect = itertools.count(step=20)
        patch_get_rt_subs_info.side_effect = [rt_subs_before, rt_subs_before, rt_subs_during, rt_subs_after, rt_subs_during, rt_subs_during]
        with self.assertRaises(Exception) as context:
            cst.cst_start_clients(**kwargs)
        #self.assertIn("not all subscribers log in RT finally", context.exception.args[0])
        del kwargs["stabilize_time"]

        builtins.bbe.get_subscriber_handles = MagicMock()
        builtins.bbe.cst_stats = MagicMock()
        patch_time.side_effect = None
        patch_get_rt_subs_info.side_effect = None

    @patch('jnpr.toby.bbe.cst.cstutils.time.sleep')
    @patch('jnpr.toby.bbe.cst.cstutils.time.time')
    @patch('jnpr.toby.bbe.cst.cstutils.get_rt_subs_info')
    @patch('jnpr.toby.bbe.cst.cstutils.get_router_sub_summary')
    @patch('jnpr.toby.bbe.cst.cstutils.get_configured_subs')
    @patch('jnpr.toby.bbe.cst.cstutils.clear_subscribers_in_router')
    def test_cst_release_client(self, patch_clear_subscribers_in_router, patch_get_configured_subs,
                                patch_get_router_sub_summary, patch_get_rt_subs_info, patch_time, patch_sleep):
        sub = MagicMock()
        sub.rt_state = "stopped"
        builtins.bbe.get_subscriber_handles.return_value = [sub]
        kwargs = {"device_id": "r0", "subs": sub}
        self.assertEqual(cst.cst_release_clients(**kwargs), True)
        self.assertEqual(cst.cst_release_clients(), True)
        sub.rt_state = "started"
        r_stat1 = {"client": 0, "total": 0}
        r_stat2 = {"client": 8, "total": 0}
        r_stat3 = {"client": 6, "total": 0}
        patch_get_configured_subs.return_value = {"expected_total_session_in_testers": 10, "expected_login_rate": 50,
                                     "expected_total_session_in_routers": 10}
        rtsub_stat1 = {"rt_sessions_up": 8, "rt_sessions_down": 0, "rt_sessions_not_started": 2, "rt_sessions_total": 10}
        rtsub_stat2 = {"rt_sessions_up": 0, "rt_sessions_down": 0, "rt_sessions_not_started": 10, "rt_sessions_total": 10}
        rtsub_stat3 = {"rt_sessions_up": 0, "rt_sessions_down": 0, "rt_sessions_not_started": 4, "rt_sessions_total": 10}
        patch_get_rt_subs_info.side_effect = [rtsub_stat1, rtsub_stat3, rtsub_stat2]
        patch_get_router_sub_summary.side_effect = [r_stat2, r_stat1, r_stat1]
        self.assertEqual(cst.cst_release_clients(**kwargs), None)
        patch_get_rt_subs_info.side_effect = [rtsub_stat1, rtsub_stat3, rtsub_stat2]
        patch_get_router_sub_summary.side_effect = [r_stat2, r_stat1, r_stat1]
        self.assertEqual(cst.cst_release_clients(release_method="abort"), None)
        patch_get_rt_subs_info.side_effect = [rtsub_stat1, rtsub_stat3, rtsub_stat2]
        patch_get_router_sub_summary.side_effect = [r_stat2, r_stat2, r_stat3, r_stat3, r_stat3, r_stat3, r_stat3, r_stat3,
                                       r_stat3, r_stat3, r_stat3, r_stat3, r_stat3, r_stat3]
        with self.assertRaises(Exception) as context:
            cst.cst_release_clients(**kwargs)
        #self.assertIn("some subscribers are still in routers, please check the router", context.exception.args[0])
        builtins.bbe.get_subscriber_handles.return_value = [sub, MagicMock()]
        patch_get_rt_subs_info.side_effect = [rtsub_stat1, rtsub_stat3, rtsub_stat2]
        patch_get_router_sub_summary.side_effect = [r_stat2, r_stat2, r_stat3, r_stat3, r_stat3, r_stat3, r_stat3, r_stat3,
                                       r_stat3, r_stat3, r_stat3, r_stat3, r_stat3, r_stat3]
        with self.assertRaises(Exception) as context:
            cst.cst_release_clients(**kwargs)
        #self.assertIn("some subscribers are still in routers, please check the router", context.exception.args[0])

        builtins.bbe.get_subscriber_handles = MagicMock()

    @patch("re.search")
    @patch("builtins.print")
    @patch("jnpr.toby.bbe.cst.cstutils.get_ae_info")
    def test_get_configured_subs(self, patch_get_ae_info, patch_print, patch_re_search):
        self.assertIsInstance(cst.get_configured_subs(), dict)
        self.assertIsInstance(cst.get_configured_subs(device_id="rt0",subs=[]), dict)

        patch_get_ae_info.return_value = {"ae_bundle": {"active": []}}
        builtins.t.get_junos_resources.return_value = ["r0"]
        builtins.bbe.get_interfaces.return_value = [MagicMock()]

        subs = MagicMock()
        subs.count = 1
        subs.csr = 1
        subs.clr = 1
        subs.ae_bundle = "ae_bundle"
        builtins.bbe.get_subscriber_handles.return_value = [subs]
        kwargs = {
            "device_id": "r0",
            "subs": subs
        }
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        patch_re_search.return_value = False
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        subs.subscribers_type = "l2bsa"
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        subs.subscribers_type = "pppoe"
        subs.family = "ipv4"
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        subs.family = "ipv6"
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        subs.subscribers_type = "dhcp"
        subs.family = "dual"
        subs.single_session = True
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        subs.single_session = False
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        subs.family = "ipv4"
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        subs.family = "ipv6"
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)

        kwargs["device_id"] = ["r0", "r1"]
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        kwargs["device_id"] = "r0"
        del kwargs["subs"]
        builtins.bbe.get_subscriber_handles.return_value = []
        with self.assertRaises(Exception) as context:
            cst.get_configured_subs(**kwargs)
        self.assertIn("no subscriber info defined", context.exception.args[0])
        builtins.t.resources = {
            "r0": {
                "system": {
                    "primary": {
                        "uv-bbe-config": {
                            "subscriber-info": {
                                "count-in-router": 0,
                                "count-in-tester": 0,
                                "route-count": 0
                            }
                        }
                    }
                }
            }
        }
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        kwargs["subs"] = [subs]
        builtins.bbe.get_subscriber_handles.return_value = [subs]
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock(count=1)]
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)
        kwargs["device_id"] = ["r0", "r1"]
        builtins.t.resources["r1"] = MagicMock()
        subs.device_id = "expected_route_count"
        self.assertIsInstance(cst.get_configured_subs(**kwargs), dict)

        builtins.t.get_junos_resources = MagicMock()
        builtins.t.resources = MagicMock()
        builtins.bbe.get_interfaces = MagicMock()
        builtins.bbe.get_subscriber_handles.return_value = MagicMock()

    @patch("builtins.print")
    def test_get_rt_subs_info(self, patch_print):
        builtins.bbe.get_devices.return_value = ["rt0"]
        self.router.invoke.return_value = {
            "global_per_protocol": {
                "PPPoX Client": {
                    "sessions_up": 10,
                    "setup_avg_rate": 50,
                    "sessions_down": 0,
                    "sessions_total": 10,
                    "teardown_avg_rate": 50,
                    "sessions_not_started": 0
                },
                "DHCPv4 Client": {
                    "sessions_up": 0,
                    "setup_avg_rate": 0,
                    "sessions_down": 0,
                    "sessions_total": 0,
                    "teardown_avg_rate": 0,
                    "sessions_not_started": 0
                },
                "DHCPv6 Client": {
                    "sessions_up": 0,
                    "setup_avg_rate": 0,
                    "sessions_down": 0,
                    "sessions_total": 0,
                    "teardown_avg_rate": 0,
                    "sessions_not_started": 0
                }
            }
        }
        builtins.bbe.cst_stats = {"partial_login": 0, "expected_total_session_in_testers": 10}
        self.assertIsInstance(cst.get_rt_subs_info(), dict)
        builtins.bbe.cst_stats["rt_login_rate"] = "50"
        self.assertIsInstance(cst.get_rt_subs_info(), dict)
        self.router.invoke.side_effect = Exception
        self.assertIsInstance(cst.get_rt_subs_info(), dict)
        self.router.invoke.side_effect = None
        self.router.invoke = MagicMock()
        builtins.bbe.get_devices = MagicMock()
        builtins.bbe.cst_stats = MagicMock()

    def test_get_master_re_name(self):
        self.router.detect_master_node.return_value = "primary"
        self.assertEqual(cst.get_master_re_name(), "primary-re0")
        self.router.vc = False
        self.router.current_node.current_controller.re_name = "member-re0"
        self.assertEqual(cst.get_master_re_name(), "member-re0")
        self.router.current_node.current_controller.is_master.return_value = False
        with self.assertRaises(Exception) as context:
            cst.get_master_re_name()
        self.assertIn("no master re was found", context.exception.args[0])
        #self.assertEqual(cst.get_master_re_name(), None)
        self.router.current_node.controllers = ["re0"]
        self.assertEqual(cst.get_master_re_name(), "re0")

        self.router.vc = MagicMock()
        self.router.current_node = MagicMock()
        self.router.detect_master_node = MagicMock()

    def test_get_router_sub_summary(self):
        resp = self.router.pyez.return_value.resp
        resp.getnext.return_value.findall.return_value = [MagicMock()]
        self.assertIsInstance(cst.get_router_sub_summary(), dict)

        self.router.pyez = MagicMock()

    def test_get_route_summary(self):
        protocol1 = MagicMock()
        protocol1.findtext.return_value = "inet.0"
        protocol2 = MagicMock()
        protocol2.findtext.side_effect = ["Access", "inet.0", 2]
        table = MagicMock()
        table.findall.return_value = [protocol1, protocol2]
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [table]
        self.assertEqual(cst.get_route_summary(), 2)
        protocol2.findtext.side_effect = None
        self.router.pyez = MagicMock()

    def test_get_router_sub_summary_by_port(self):
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [MagicMock()]
        self.assertIsInstance(cst.get_router_sub_summary_by_port(), dict)

        self.router.pyez = MagicMock()

    def test_get_router_sub_summary_by_slot(self):
        counter = MagicMock()
        counter.findtext.return_value = False
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [MagicMock(), counter]
        self.assertIsInstance(cst.get_router_sub_summary_by_slot(), dict)

        self.router.pyez = MagicMock()

    def test_get_aaa_authentication_stats(self):
        self.assertIsInstance(cst.get_aaa_authentication_stats(), dict)

    def test_get_aaa_accounting_stats(self):
        self.assertIsInstance(cst.get_aaa_accounting_stats(), dict)

    def test_get_aaa_jsrc_stats(self):
        self.assertIsInstance(cst.get_aaa_jsrc_stats(), MagicMock)

    def test_get_ppp_stats(self):
        self.assertEqual(cst.get_ppp_stats(), None)

    def test_get_pppoe_stats(self):
        self.assertEqual(cst.get_pppoe_stats(), None)

    def test_get_pppoe_inline_keepalive_stats(self):
        interface = MagicMock()
        interface.interface_pic = "ge-1/0/0"
        builtins.bbe.get_interfaces.return_value = [interface]
        self.assertEqual(cst.get_pppoe_inline_keepalive_stats(), None)
        interface.interface_pic = "ge-12/0/0"
        self.assertEqual(cst.get_pppoe_inline_keepalive_stats(), None)
        builtins.bbe.get_devices.return_value.is_mxvc = False
        self.assertEqual(cst.get_pppoe_inline_keepalive_stats(), None)

        builtins.bbe.get_devices = MagicMock()
        builtins.bbe.get_interfaces = MagicMock()

    def test_get_dhcp_stats(self):
        self.assertEqual(cst.get_dhcp_stats("r0"), None)

    def test_add_subscriber_mesh(self):
        self.router.invoke.return_value = {"status": "1"}
        subs = MagicMock()
        uplink = MagicMock()
        kwargs = {
            "rt_device_id": "rt0",
            "direction": "up",
            "subs": subs,
            "uplinks": uplink
        }
        self.assertEqual(cst.add_subscriber_mesh(**kwargs), None)
        kwargs["direction"] = "down"
        subs.rt_device_id = "rt0"
        uplink.device_id = "rt0"
        self.assertEqual(cst.add_subscriber_mesh(**kwargs), None)

        subs.family = "dual"
        subs.subscribers_type = "dhcp"
        self.assertEqual(cst.add_subscriber_mesh(**kwargs), None)
        subs.subscribers_type = "pppoe"
        self.assertEqual(cst.add_subscriber_mesh(**kwargs), None)
        subs.family = "ipv4"
        kwargs["traffic_args"] = {"type": "ipv4"}
        subs.subscribers_type = "dhcp"
        self.assertEqual(cst.add_subscriber_mesh(**kwargs), None)
        subs.subscribers_type = "pppoe"
        self.assertEqual(cst.add_subscriber_mesh(**kwargs), None)
        uplink.rt_lns_server_session_handle = False
        self.assertEqual(cst.add_subscriber_mesh(**kwargs), None)
        uplink.rt_lns_server_session_handle = True
        subs.family = "ipv6"
        kwargs["traffic_args"]["type"] = "ipv6"
        self.assertEqual(cst.add_subscriber_mesh(**kwargs), None)
        uplink.rt_lns_server_session_handle = False
        self.assertEqual(cst.add_subscriber_mesh(**kwargs), None)

        self.router.invoke.return_value["status"] = "0"
        subs.family = "ipv4"
        kwargs["traffic_args"] = {"type": "ipv4"}
        with self.assertRaises(Exception) as context:
            cst.add_subscriber_mesh(**kwargs)
        self.assertIn("failed to create v4 traffic", context.exception.args[0])
        subs.family = "ipv6"
        kwargs["traffic_args"] = {"type": "ipv6"}
        with self.assertRaises(Exception) as context:
            cst.add_subscriber_mesh(**kwargs)
        self.assertIn("failed to create v6 traffic", context.exception.args[0])

        self.router.invoke = MagicMock()

    def test_time_in_sec(self):
        self.assertEqual(cst.time_in_sec("1:1:1"), 3661)

    @patch('jnpr.toby.bbe.cst.cstutils.time.sleep')
    def test_verify_traffic(self, patch_sleep):
        kwargs = {
            "duration": 10,
            "traffic_name_loss": {
                "stream": 1
            }
        }
        self.router.invoke.return_value = {
            "stopped": "1",
            "waiting_for_stats": "0",
            "aggregate": {
                "rx": {
                    "total_pkts": {
                        "sum": 100
                    }
                },
                "tx": {
                    "total_pkts": {
                        "sum": 100
                    }
                }
            },
            "l23_test_summary": {
                "rx": {
                    "pkt_count": 100
                },
                "tx": {
                    "pkt_count": 100
                }
            },
            "traffic_item": {
                "stream": {
                    "rx": {
                        "total_pkts": 10000,
                        "total_pkts_bytes": 1000000,
                        "loss_pkts": 0,
                        "first_tstamp": "1:1:1",
                        "last_tstamp": "1:1:6",
                        "loss_percent": 0
                    },
                    "tx": {
                        "total_pkts": 10000
                    }
                },
                "aggregate": {}
            }
        }
        self.assertEqual(cst.verify_traffic(**kwargs), None)
        kwargs["mode"] = "summary"
        self.assertEqual(cst.verify_traffic(**kwargs), None)
        kwargs["mode"] = "traffic_item"
        self.assertEqual(cst.verify_traffic(**kwargs), None)
        del kwargs["traffic_name_loss"]
        kwargs["traffic_name_rate"] = {"stream": 1.6}
        self.assertEqual(cst.verify_traffic(**kwargs), None)
        del kwargs["traffic_name_rate"]
        self.assertEqual(cst.verify_traffic(**kwargs), None)

        kwargs["mode"] = "aggregate"
        self.router.invoke.return_value["aggregate"]["rx"]["total_pkts"]["sum"] = 1000
        with self.assertRaises(Exception) as context:
            cst.verify_traffic(**kwargs)
        self.assertIn("% traffic, out of the specified range", context.exception.args[0])
        kwargs["mode"] = "l23_test_summary"
        self.router.invoke.return_value["l23_test_summary"]["rx"]["pkt_count"] = 1000
        with self.assertRaises(Exception) as context:
            cst.verify_traffic(**kwargs)
        self.assertIn("% traffic, out of the specified range", context.exception.args[0])
        kwargs["mode"] = "traffic_item"
        kwargs["traffic_name_loss"] = {"stream": -2}
        with self.assertRaises(Exception) as context:
            cst.verify_traffic(**kwargs)
        self.assertIn("verify traffic failed", context.exception.args[0])
        #self.assertIn(" > expected loss percent ", context.exception.args[0])
        del kwargs["traffic_name_loss"]
        kwargs["mode"] = "traffic_item"
        kwargs["traffic_name_rate"] = {"stream": -2}
        with self.assertRaises(Exception) as context:
            cst.verify_traffic(**kwargs)
        self.assertIn("verify traffic failed", context.exception.args[0])
        #self.assertIn(", less than the specified rate ", context.exception.args[0])
        del kwargs["traffic_name_rate"]
        self.router.invoke.return_value["traffic_item"]["stream"]["rx"]["total_pkts"] = 1000000
        with self.assertRaises(Exception) as context:
            cst.verify_traffic(**kwargs)
        self.assertIn("verify traffic failed", context.exception.args[0])
        #self.assertIn("% traffic, out of the specified range", context.exception.args[0])

        self.router.invoke = MagicMock()

    @patch("time.sleep")
    @patch("time.time")
    @patch("builtins.print")
    def test_start_traffic(self, patch_print, patch_time, patch_sleep):
        # Make time go up by 5 sec every time it is called
        patch_time.side_effect = itertools.count(step=5)

        kwargs = {"duration": 10, "handle": MagicMock()}
        self.router.invoke.return_value = {"stopped": "0"}
        self.assertEqual(cst.start_traffic(**kwargs), None)
        del kwargs["duration"]
        self.router.invoke = MagicMock()
        with self.assertRaises(Exception) as context:
            cst.start_traffic(**kwargs)
        self.assertIn("traffic failed to start", context.exception.args[0])
        patch_time.side_effect = None

    @patch("time.sleep")
    def test_stop_traffic(self, patch_sleep):
        self.router.invoke.return_value = {"stopped": "1"}
        self.assertEqual(cst.stop_traffic(handle="handle"), None)

        self.router.invoke = MagicMock()

    def test_get_dhcp_addr_from_rt(self):
        kwargs = {
            "subs": [MagicMock()],
            "type": "ipv4"
        }
        self.router.invoke.return_value = {
            "status": "1",
            "session": {
                "item": {
                    "Address": "address",
                    "Prefix": "prefix"
                }
            }
        }
        self.assertIsInstance(cst.get_dhcp_addr_from_rt(**kwargs), list)
        kwargs["type"] = "ipv6"
        self.assertIsInstance(cst.get_dhcp_addr_from_rt(**kwargs), list)

        self.router.invoke.return_value["status"] = "0"
        with self.assertRaises(Exception) as context:
            cst.get_dhcp_addr_from_rt(**kwargs)
        self.assertIn("failed to get dhcp stats from rt for sub ", context.exception.args[0])

        self.router.invoke = MagicMock()

    def test_get_interface_from_address(self):
        response = MagicMock()
        response.findtext.return_value = "address"
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [response]
        self.assertEqual(cst.get_interface_from_address(address="address"), "address")
        #self.assertEqual(cst.get_interface_from_address(address="invalid"), None)
        with self.assertRaises(Exception) as context:
            cst.get_interface_from_address(address='invalid')
        self.assertIn("no interface was found for the address", context.exception.args[0])
        self.router.pyez = MagicMock()

    @patch("time.sleep")
    def test_start_rt_links(self, patch_sleep):
        kwargs = {
            "rt_device_id": "rt0",
            "uplinks": [MagicMock()]
        }
        kwargs["uplinks"][0].device_id = "rt0"
        self.assertEqual(cst.start_rt_links(**kwargs), None)
        builtins.bbe.get_connection.return_value.is_ae = False
        self.assertEqual(cst.start_rt_links(**kwargs), None)
        kwargs["uplinks"][0].device_id = "rt1"
        self.assertEqual(cst.start_rt_links(**kwargs), None)

        builtins.bbe.get_connection = MagicMock()

    @patch("builtins.print")
    @patch("jnpr.toby.bbe.cst.cstutils._myprint")
    def test_print_cst(self, patch_myprint, patch_print):
        builtins.bbe.cst_stats = {
            "key1": "val1",
            "key2": {}
        }
        self.assertEqual(cst.print_cst_stats(), None)

        builtins.bbe.cst_stats = MagicMock()

    @patch("builtins.print")
    def test_myprint(self, patch_print):
        data = {
            "key1": "val1",
            "key2": {}
        }
        self.assertEqual(cst._myprint(data), None)

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstutils.Device")
    def test_panic_re_recover(self, patch_device, patch_sleep):
        kwargs = {"host": "h1"}
        self.assertEqual(cst.panic_re_recover(**kwargs), None)
        kwargs["tomcat_mode"] = False
        self.assertEqual(cst.panic_re_recover(**kwargs), None)

        patch_device.side_effect = Exception
        with self.assertRaises(Exception) as context:
            cst.panic_re_recover(**kwargs)
        self.assertIn("failed to login to console", context.exception.args[0])
        patch_device.side_effect = None

    @patch("time.sleep")
    @patch("pexpect.spawn")
    def test_power_manager(self, patch_spawn, patch_sleep):
        kwargs = {
            "chassis": "chassis",
            "action": "on"
        }
        self.assertEqual(cst.power_manager(**kwargs), None)
        kwargs["action"] = "cycle"
        self.assertEqual(cst.power_manager(**kwargs), None)

    @patch('jnpr.toby.bbe.cst.cstutils.time.sleep')
    @patch("jnpr.toby.bbe.cst.cstutils.get_route_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_configured_subs")
    def test_verify_client_count(self, patch_get_configured_subs, patch_get_router_sub_summary, patch_get_route_summary, sleep_patch):
        patch_get_configured_subs.return_value = {
            "expected_total_session_in_routers": 0,
            "expected_route_count": 0
        }
        self.assertEqual(cst.verify_client_count(), None)
        patch_get_router_sub_summary.return_value = {"client": 0, "init": 1}
        patch_get_route_summary.return_value = 0
        builtins.bbe.defined_sub_info = {
            "rt0": {
                "count-in-router": 0,
                "route-count": 0
            }
        }
        kwargs = {
            "device_id": "rt0",
            "subs": MagicMock()
        }
        self.assertEqual(cst.verify_client_count(**kwargs), None)

        patch_get_configured_subs.return_value = {
            "expected_total_session_in_routers": 10,
            "expected_route_count": 10
        }
        builtins.bbe.defined_sub_info = {
            "rt0": {
                "count-in-router": 10,
                "route-count": 10
            }
        }
        with self.assertRaises(Exception) as context:
            cst.verify_client_count(**kwargs)
        self.assertIn("failed in subscriber count verification", context.exception.args[0])

        builtins.bbe.defined_sub_info = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstutils.get_route_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_configured_subs")
    def test_verify_client_route(self, patch_get_configured_subs, patch_get_router_sub_summary, patch_get_route_summary):
        patch_get_configured_subs.return_value = {
            "expected_total_session_in_routers": 0,
            "expected_route_count": 0
        }
        self.assertEqual(cst.verify_client_route(), None)
        patch_get_router_sub_summary.return_value = {"client": 0}
        patch_get_route_summary.return_value = 0
        builtins.bbe.defined_sub_info = {
            "rt0": {
                "count-in-router": 0,
                "route-count": 0
            }
        }
        kwargs = {
            "device_id": "rt0",
            "subs": MagicMock()
        }
        self.assertEqual(cst.verify_client_route(**kwargs), None)
        patch_get_configured_subs.return_value = {
            "expected_total_session_in_routers": 10,
            "expected_route_count": 10
        }
        builtins.bbe.defined_sub_info = {
            "rt0": {
                "count-in-router": 10,
                "route-count": 10
            }
        }
        with self.assertRaises(Exception) as context:
            cst.verify_client_route(**kwargs)
        self.assertIn("failed in access route count verification", context.exception.args[0])

        builtins.bbe.defined_sub_info = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.add_subscriber_mesh")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_release_clients")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_start_clients")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_router_before_login")
    def test_prepare_for_concurrent_test(self, patch_prepare_router_before_login, patch_cst_start_clients,
                                         patch_cst_release_clients, patch_add_subscriber_mesh, patch_start_traffic):
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
        with self.assertRaises(Exception) as context:
            cst.prepare_for_concurrent_test()
        self.assertIn("subscriber groups must be greater than 1", context.exception.args[0])
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock(), MagicMock()]
        self.assertIsInstance(cst.prepare_for_concurrent_test(), dict)
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock(), MagicMock(), MagicMock()]
        self.assertIsInstance(cst.prepare_for_concurrent_test(), dict)

        kwargs = {
            "background_subs": [MagicMock(), MagicMock()],
            "group_a": [],
            "verify_traffic": True
        }
        self.assertIsInstance(cst.prepare_for_concurrent_test(**kwargs), dict)
        patch_cst_start_clients.side_effect = [Exception, MagicMock()]
        self.assertIsInstance(cst.prepare_for_concurrent_test(**kwargs), dict)
        patch_cst_start_clients.side_effect = None
        builtins.bbe.get_subscriber_handles = MagicMock()

    @patch("os.environ")
    @patch("builtins.open")
    @patch("subprocess.call")
    @patch("jnpr.toby.bbe.cst.cstutils.tostring")
    @patch("jnpr.toby.bbe.cst.cstutils.parseString")
    @patch("jnpr.toby.bbe.cst.cstutils.dict_to_xml")
    @patch("jnpr.toby.bbe.cst.cstutils.print_cst_stats")
    @patch("jnpr.toby.bbe.cst.cstutils.get_configured_subs")
    def test_publish_cst_result(self, patch_get_configured_subs, patch_print_cst_stats, patch_dict_to_xml,
                                patch_parseString, patch_tostring, patch_call, patch_open, patch_os):
        tv_dict = MagicMock()
        tv_dict.__getitem__.return_value = "customer"
        tv_dict.__contains__.return_value = True
        builtins.tv = {
            "uv-bbevar": {
                "test": tv_dict,
                "dhcpserver": MagicMock()
            }
        }
        self.assertEqual(cst.publish_cst_result(), None)
        tv_dict.__getitem__.return_value = "scaling"
        self.assertEqual(cst.publish_cst_result(), None)
        kwargs = {"flows_per_sub": 3.0}
        self.assertEqual(cst.publish_cst_result(**kwargs), None)
        tv_dict.__getitem__.return_value = MagicMock()
        self.assertEqual(cst.publish_cst_result(), None)

        del builtins.tv

    @patch("jnpr.toby.bbe.cst.cstutils.Element")
    def test_dict_to_xml(self, patch_element):
        tag = "tag"
        data = {
            "key1": "val1",
            "key2": {}
        }
        self.assertIsInstance(cst.dict_to_xml(tag, data), MagicMock)

    @patch("time.sleep")
    def test_check_re_status(self, patch_sleep):
        resp = self.router.pyez.return_value.resp
        obj1 = MagicMock()
        obj1.findtext.return_value = "OK"
        resp.findall.return_value = [obj1]
        self.assertEqual(cst.check_re_status(), None)
        obj1.findtext.return_value = "NOK"
        with self.assertRaises(Exception) as context:
            cst.check_re_status()
        self.assertIn(" failed to come back", context.exception.args[0])

        self.router.pyez = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstutils.check_fpc")
    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    def test_clear_subscribers_in_router(self, patch_get_router_sub_summary, patch_sleep, path_checkfpc):
        patch_get_router_sub_summary.return_value = {"total": 0}
        self.assertEqual(cst.clear_subscribers_in_router(), None)
        patch_get_router_sub_summary.return_value = {"total": 1}
        self.assertEqual(cst.clear_subscribers_in_router(), None)
        # with self.assertRaises(Exception) as context:
        #     cst.clear_subscribers_in_router(type="dhcp")
        # self.assertIn("not all subscribers logout, please check router", context.exception.args[0])

    def test_get_ae_info(self):
        kwargs = {"device_id": "rt0"}
        builtins.bbe.get_interfaces.return_value = [MagicMock()]
        self.assertIsInstance(cst.get_ae_info(**kwargs), dict)
        builtins.bbe.get_connection.return_value.is_ae_active = False
        self.assertIsInstance(cst.get_ae_info(**kwargs), dict)

        builtins.bbe.get_interfaces = MagicMock()
        builtins.bbe.get_connection = MagicMock()

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.add_subscriber_mesh")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_start_clients")
    def test_prepare_subscriber_traffic(self, patch_cst_start_clients, patch_add_subscriber_mesh,
                                        patch_start_traffic, patch_stop, patch_verify_traffic, patch_sleep):
        self.assertEqual(cst.prepare_subscriber_traffic(duration=60), None)
        patch_cst_start_clients.side_effect = [Exception, None]
        self.assertEqual(cst.prepare_subscriber_traffic(), None)
        patch_cst_start_clients.side_effect = None

    @patch("re.match")
    @patch("re.search")
    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    def test_get_dirty_table(self, patch_get_master_re_name, patch_re_search, patch_re_match):
        self.router.vc = False
        self.assertIsInstance(cst.get_dirty_table(), int)
        patch_get_master_re_name.return_value = "re1"
        self.assertIsInstance(cst.get_dirty_table(), int)
        self.router.vc = MagicMock()
        self.assertIsInstance(cst.get_dirty_table(), int)
        patch_re_search.return_value = False
        self.assertIsInstance(cst.get_dirty_table(), int)

    @patch("time.sleep")
    @patch("time.time")
    def test_check_fpc(self, patch_time, patch_sleep):
        # Make time go up by 200 sec every time it is called
        patch_time.side_effect = itertools.count(step=200)
        self.router.shell.return_value.resp = 'hw.product.router_max_fpc_slots: 24'
        fpc_info = MagicMock()
        resp = self.router.pyez.return_value.resp
        fpc_info.findtext.return_value = "6"
        resp.findall.return_value = [fpc_info]
        with self.assertRaises(Exception) as context:
            cst.check_fpc()
        self.assertIn("FPCs failed to be online after 600 seconds", context.exception.args[0])
        fpc_info.findtext.side_effect = ['Empty', '6', None]
        self.assertEqual(cst.check_fpc(), [])
        fpc_info.findtext.side_effect = ['Online', '6', '2048']
        self.assertEqual(cst.check_fpc(), ['6'])
        fpc_info.findtext.side_effect = ['Offline', '6', '2048', "Unsupported FPC", "Unsupported FPC"]
        self.assertEqual(cst.check_fpc(), [])
        fpc_info.findtext.side_effect = None
        obj1 = MagicMock()
        obj1.findtext.side_effect = ['Online', '2048']
        self.router.pyez.return_value.resp = obj1
        self.assertEqual(cst.check_fpc(slot=['6']), ['6'])
        obj1.findtext.side_effect = ['Online', '2048']
        self.assertEqual(cst.check_fpc(slot=['18']), ['18'])
        obj1.findtext.side_effect = None


    def test_get_pic_info(self):
        pic_info = MagicMock()
        fpc_info = MagicMock()
        fpc_info.findall.return_value = [pic_info]
        engine = MagicMock()
        engine.findall.return_value = [fpc_info]
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [engine]
        self.assertIsInstance(cst.get_pic_info(), dict)
        fpc_info.findtext.return_value = "Online"
        self.assertIsInstance(cst.get_pic_info(), dict)
        pic_info.findtext.return_value = "Online"
        self.assertIsInstance(cst.get_pic_info(), dict)
        self.router.vc = False
        resp.findall.return_value = [fpc_info]
        self.assertIsInstance(cst.get_pic_info(), dict)
        pic_info.findtext.return_value = "Offline"
        self.assertIsInstance(cst.get_pic_info(), dict)
        fpc_info.findtext.return_value = "Offline"
        self.assertIsInstance(cst.get_pic_info(), dict)
        self.router.pyez = MagicMock()
        self.router.vc = MagicMock()

    def test_get_vcp_ports(self):
        port_info = MagicMock()
        member = MagicMock()
        member.findall.return_value = [port_info]
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [member]
        self.assertIsInstance(cst.get_vcp_ports(), dict)
        port_info.findtext.return_value = "up"
        self.assertIsInstance(cst.get_vcp_ports(), dict)

        self.router.pyez = MagicMock()

    def test_get_session_id(self):
        subs = MagicMock()
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [subs]
        self.assertIsInstance(cst.get_session_ids(return_session_detail=True), list)
        subs.findtext.return_value = "630"
        self.assertEqual(cst.get_session_ids(), ["630"])
        subs.findtext.return_value = None
        with self.assertRaises(Exception) as context:
            cst.get_session_ids()
        self.assertIn("no session id was found for the check", context.exception.args[0])

        self.router.pyez = MagicMock()

    def test_clear_subscriber_sessions(self):
        kwargs = {
            "interface_list": [MagicMock()],
            "session_id_list": [MagicMock()],
            "method": "cli",
            "client_type": "pppoe"
        }
        self.assertEqual(cst.clear_subscriber_sessions(**kwargs), None)
        kwargs["client_type"] = "l2tp"
        self.assertEqual(cst.clear_subscriber_sessions(**kwargs), None)
        kwargs["method"] = "radius"
        self.assertEqual(cst.clear_subscriber_sessions(**kwargs), None)

        kwargs["method"] = "cli"
        self.router.cli.return_value.resp = "not"
        with self.assertRaises(Exception) as context:
            cst.clear_subscriber_sessions(**kwargs)
        self.assertIn(" failed", context.exception.args[0])
        kwargs["method"] = "radius"
        self.router.shell.return_value.resp = "Error-Cause"
        with self.assertRaises(Exception) as context:
            cst.clear_subscriber_sessions(**kwargs)
        self.assertIn(" failed in disconnect", context.exception.args[0])

        self.router.cli = MagicMock()
        self.router.shell = MagicMock()

    def test_subscriber_service_action(self):
        self.router.cli.return_value.resp = "Successful"
        kwargs = {
            "method": "radius",
            "session_id_list": [MagicMock()],
            "service_name": "name",
            "action": "activate"
        }
        self.assertEqual(cst.subscriber_service_action(**kwargs), None)
        kwargs["action"] = "deactivate"
        self.assertEqual(cst.subscriber_service_action(**kwargs), None)
        kwargs["method"] = "cli"
        self.assertEqual(cst.subscriber_service_action(**kwargs), None)

        self.router.shell.return_value.resp = "CoA-NAK"
        self.router.cli.return_value.resp = "CoA-NAK"
        kwargs["method"] = "radius"
        with self.assertRaises(Exception) as context:
            cst.subscriber_service_action(**kwargs)
        self.assertIn(" service using command ", context.exception.args[0])
        kwargs["method"] = "cli"
        with self.assertRaises(Exception) as context:
            cst.subscriber_service_action(**kwargs)
        self.assertIn(" service using command ", context.exception.args[0])

        self.router.cli = MagicMock()
        self.router.shell = MagicMock()

    def test_get_session_service_name(self):
        self.router.cli.return_value.resp = "Service Name: test\r\n"
        self.assertEqual(cst.get_session_service_name(session_id="id"), ["test"])

        self.router.cli = MagicMock()

    @patch("builtins.print")
    def test_get_re_fpc_memory(self, patch_print):
        builtins.bbe.get_devices.return_value = ["r0"]
        fpc_info = MagicMock()
        fpc_info.findtext.return_value = "Online"
        fpc_info_offline = MagicMock()
        fpc_info_offline.findtext.return_value = "Offline"
        engine = MagicMock()
        engine.findall.return_value = [fpc_info]
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [engine]
        self.assertIsInstance(cst.get_re_fpc_memory(), dict)
        fpc_info.findtext.return_value = "Offline"
        self.assertIsInstance(cst.get_re_fpc_memory(), dict)

        self.router.vc = False
        fpc_info_offline.findtext.return_value = "Offline"
        fpc_info.findtext.side_effect = ["Online", "10", "1"]
        counter_empty = MagicMock()
        counter_empty.findtext.return_value = ""
        counter_xe = MagicMock()
        counter_xe.findtext.side_effect = ["xe-1", "20"]
        counter_ps = MagicMock()
        counter_ps.findtext.side_effect = ["ps-1", "30"]
        engine.findtext.side_effect = [False, "10"]
        resp.findall.side_effect = [[fpc_info_offline, fpc_info], [counter_empty, counter_xe, counter_ps], [engine]]
        self.router.cli.return_value.resp = "lt-1/0/0"
        self.assertIsInstance(cst.get_re_fpc_memory(), dict)
        fpc_info.findtext.side_effect = None
        counter_xe.findtext.side_effect = None
        counter_ps.findtext.side_effect = None
        engine.findtext.side_effect = None
        resp.findall.side_effect = None
        self.router.pyez = MagicMock()
        self.router.vc = MagicMock()
        self.router.cli = MagicMock()
        builtins.bbe.get_devices = MagicMock()

    @patch('jnpr.toby.bbe.cst.cstutils.time.sleep')
    @patch('jnpr.toby.bbe.cst.cstutils.time.time')
    def test_get_fpc_vty_stats(self, patch_time, patch_sleep):
        # Make time go up by 600 sec every time it is called
        patch_time.side_effect = itertools.count(step=600)

        builtins.bbe.get_devices.return_value = ["rt0"]
        builtins.t.resources = {
            "rt0": {
                "interfaces": {
                    "access": {
                        "pic": "lt-1/0/0"
                    }
                }
            }
        }
        obj = cst.get_fpc_vty_stats(60)
        obj.run()
        obj.stop()
        patch_time.side_effect = None
        builtins.t.resources = MagicMock()
        builtins.bbe.get_devices = MagicMock()

    def test_get_cst_stats(self):
        self.assertEqual(cst.get_cst_stats(), builtins.bbe.cst_stats)

    @patch('jnpr.toby.bbe.cst.cstutils.time.sleep')
    @patch('jnpr.toby.bbe.cst.cstutils.time.time')
    @patch('jnpr.toby.bbe.cst.cstutils.re.search')
    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    def test_check_gres_ready(self, patch_get_master_re_name, patch_re_search, patch_time, patch_sleep):
        # Make time go up by 60 sec every time it is called
        patch_time.side_effect = itertools.count(step=60)

        patch_get_master_re_name.return_value.split.return_value = [None, "re0"]
        self.router.detect_master_node.return_value = "primary"
        patch_re_search.return_value = False
        with self.assertRaises(Exception) as context:
            cst.check_gres_ready()
        self.assertIn(" is not ready for GRES after waiting for ", context.exception.args[0])

        patch_re_search.return_value = True
        self.router.cli.return_value.resp = ["Stateful Replication: Enabled", "Switchover Ready"]
        self.router.vc = False
        self.assertEqual(cst.check_gres_ready(), None)
        patch_time.side_effect = None
        self.router.cli = MagicMock()
        self.router.vc = MagicMock()
        self.router.detect_master_node = MagicMock()

    @patch("builtins.print")
    @patch("os.mkdir")
    def test_sp_collect_logs(self, patch_mkdir, patch_print):
        builtins.t.get_resource.return_value = {
            "system": {
                "primary": {
                    "controllers": {
                        "re0": None
                    }
                }
            }
        }
        self.router.shell.return_value.response.return_value.split.return_value = [MagicMock()]
        self.assertEqual(cst.sp_collect_logs("r0", "/var/log", "*era*"), None)

        self.router.shell = MagicMock()
        builtins.t.get_resource = MagicMock()

    @patch("time.time")
    def test_checkcli(self, patch_time):
        patch_time.side_effect = [0, 1]
        commands = "show subscribers summary"
        self.assertIsInstance(cst.CheckCli(self.router, commands), cst.CheckCli)
        checkcli = MagicMock(spec=cst.CheckCli)
        checkcli.runtime = 10
        checkcli.commands = ["show subscribers summary"]
        checkcli.responses = ["response"]
        checkcli.router = self.router
        self.assertEqual(cst.CheckCli.get_runtime(checkcli), 10)
        self.router.cli.return_value.resp = "response"
        self.assertEqual(cst.CheckCli.verify_cli_output(checkcli), None)
        self.router.cli.return_value.resp = "different response"
        with self.assertRaises(Exception) as context:
            cst.CheckCli.verify_cli_output(checkcli)
        self.assertIn("1 of 1 commands received a changed response", context.exception.args[0])
        patch_time.side_effect = None

    @patch("jnpr.toby.bbe.cst.cstutils.CheckCli")
    def test_check_cli_keyword(self, patch_checkcli):
        self.assertEqual(cst.check_cli(MagicMock(), MagicMock()), patch_checkcli.return_value)

    @patch("jnpr.toby.bbe.cst.cstutils.CheckCli")
    def test_get_runtime_of_check_cli_keyword(self, patch_checkcli):
        cli_checker = cst.CheckCli(MagicMock(), MagicMock())
        self.assertEqual(cst.get_runtime_of_check_cli(cli_checker), cli_checker.get_runtime.return_value)

    @patch("jnpr.toby.bbe.cst.cstutils.CheckCli")
    def test_verify_cli_output_keyword(self, patch_checkcli):
        cli_checker = cst.CheckCli(MagicMock(), MagicMock())
        self.assertEqual(cst.verify_cli_output(cli_checker), None)

    def test_remove_traffic(self):
        self.router.invoke.return_value = {'status': '0'}
        with self.assertRaises(Exception) as context:
            cst.remove_traffic(handle='h1')
        self.assertIn("failed to remove the traffic", context.exception.args[0])

    # @patch("os.environ")
    # @patch("builtins.open")
    # @patch("subprocess.call")
    # @patch("jnpr.toby.bbe.cst.cstutils.print_cst_stats")
    # @patch("jnpr.toby.bbe.cst.cstutils.get_configured_subs")
    def test_get_l2tp_stats_for_scaling(self):
       builtins.tv = {
            "uv-bbevar": {
                "l2tp": MagicMock(),
                "cos": {
                    "service-interface-fpc": MagicMock()
                }
             }
       }
       self.router.cli.return_value.resp = "Tunnels: 400, Sessions: 100"

       self.assertEqual(cst.get_l2tp_stats_for_scaling(), None)
       self.router.cli.return_value.resp = "Tunnels: 400"
       with self.assertRaises(Exception) as context:
            cst.get_l2tp_stats_for_scaling()
       self.assertIn("Could not get the stats for LAC/LNS Testing", context.exception.args[0])

    def test_add_addon_cst_result(self):
        d_spec = dict()
        d_spec['pfe_cps'] = 200
        cst.add_addon_cst_result(result_key='pfe_cps', result_value=200)
        d = cst.get_addon_cst_result()
        self.assertEqual(d, d_spec)

    def test_clear_addon_cst_result(self):
        # Add some
        d_spec = dict()
        d_spec['pfe_cps'] = 200
        cst.add_addon_cst_result(result_key='pfe_cps', result_value=200)
        d = cst.get_addon_cst_result()
        self.assertEqual(d, d_spec)
        # clear
        cst.clear_addon_cst_result()
        d = cst.get_addon_cst_result()
        self.assertEqual(d, {})

    def test_get_addon_cst_result(self):
        d_spec = dict()
        d_spec['pfe_cps'] = 200
        cst.add_addon_cst_result(result_key='pfe_cps', result_value=200)
        d = cst.get_addon_cst_result()
        self.assertEqual(d, d_spec)

if __name__ == '__main__':
    unittest.main()
