import unittest
import builtins
import itertools
from unittest.mock import MagicMock
from unittest.mock import patch
import jnpr.toby.bbe.cst.cstsuites as cstsuites

class TestCstSuites(unittest.TestCase):
    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.router = MagicMock()
        builtins.t.get_handle.return_value = self.router
        builtins.bbe = MagicMock()

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.add_subscriber_mesh")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_start_clients")
    def test_unicast_traffic_test(self, patch_cst_start_clients, patch_add_subscriber_mesh,
                                  patch_verify_traffic, patch_start_traffic, patch_stop_traffic, patch_sleep):
        self.assertEqual(cstsuites.unicast_traffic_test(), None)
        kwargs = {"duration": 120}
        self.assertEqual(cstsuites.unicast_traffic_test(**kwargs), None)
        patch_cst_start_clients.side_effect = [Exception, None]
        self.assertEqual(cstsuites.unicast_traffic_test(**kwargs), None)

    @patch("time.sleep")
    @patch("time.time")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_rt_subs_info")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_configured_subs")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_for_concurrent_test")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_start_clients")
    def test_concurrent_login_logout_test(self, patch_cst_start_clients, patch_prepare_for_concurrent_test, patch_get_rt_subs_info,
                                          patch_cpu_settle, patch_stop_traffic, patch_verify_traffic,
                                          patch_start_traffic, patch_get_router_sub_summary, patch_get_configured_subs,
                                          patch_time, patch_sleep):
        # Make time go up by 1 sec every time it is called
        patch_time.side_effect = itertools.count()
        patch_get_configured_subs.return_value = {
            "expected_login_rate": 50,
            "expected_total_session_in_testers": 10,
            "expected_total_session_in_routers": 10
        }
        self.assertEqual(cstsuites.concurrent_login_logout_test(), None)
        # with self.assertRaises(Exception) as context:
        #     cstsuites.concurrent_login_logout_test()
        # self.assertIn("not seen any packets out after waiting for", context.exception.args[0])

        patch_get_rt_subs_info.side_effect = ({"rt_sessions_not_started": i} for i in itertools.count())
        self.router.invoke.return_value = {"status": "0"}
        #with self.assertRaises(Exception) as context:
        cstsuites.concurrent_login_logout_test()
        #self.assertIn("tester returned failure, please check tester", context.exception.args[0])
        self.router.invoke = MagicMock()

        kwargs = {"group_a": [MagicMock()], "group_b": [MagicMock()]}
        patch_get_rt_subs_info.side_effect = ({"rt_sessions_not_started": i} for i in itertools.count())
        patch_get_configured_subs.return_value = {
            "expected_login_rate": 50,
            "expected_total_session_in_testers": 10,
            "expected_total_session_in_routers": 10
        }
        self.assertEqual(cstsuites.concurrent_login_logout_test(**kwargs), None)
        kwargs["router_id"] = [MagicMock()]
        kwargs["verify_traffic"] = True
        patch_get_configured_subs.return_value = {
            "expected_login_rate": 50,
            "expected_total_session_in_testers": 10,
            "expected_total_session_in_routers": 10
        }
        self.assertEqual(cstsuites.concurrent_login_logout_test(**kwargs), None)

        subs = MagicMock()
        # significantly higher than retry to test retry exit
        subs.count = 5
        kwargs["group_a"] = [subs, subs]
        kwargs["retry"] = 2
        patch_get_rt_subs_info.side_effect = ({"rt_sessions_not_started": i} for i in itertools.count())

        # 0, 0, 1, 1, 2, 2, ...
        # Repeats itself to test delta_sessions_up as 0 or non-0
        sessions_up_generator = (int(i) for i in itertools.count(0, 0.5))
        sessions_down_generator = itertools.repeat(2)
        sessions_not_started_generator = itertools.chain(iter([subs.count]), itertools.repeat(0, 12), itertools.repeat(subs.count))
        # subs.count in order to test logout group handling

        aggregate = MagicMock()
        aggregate.__getitem__.side_effect = lambda x: next({
            "sessions_up": sessions_up_generator,
            "sessions_down": sessions_down_generator,
            "sessions_not_started": sessions_not_started_generator
        }[x])
        self.router.invoke.return_value.__getitem__.return_value = {"aggregate": aggregate}
        self.assertEqual(cstsuites.concurrent_login_logout_test(**kwargs), None)

        # Repeat test, but this time start with retry -1 in order to raise exception
        sessions_up_generator = (int(i) for i in itertools.count(0, 0.5))
        sessions_down_generator = itertools.repeat(2)
        sessions_not_started_generator = itertools.chain(iter([subs.count]), itertools.repeat(0, 12), itertools.repeat(subs.count))
        aggregate = MagicMock()
        aggregate.__getitem__.side_effect = lambda x: next({
            "sessions_up": sessions_up_generator,
            "sessions_down": sessions_down_generator,
            "sessions_not_started": sessions_not_started_generator
        }[x])
        self.router.invoke.return_value.__getitem__.return_value = {"aggregate": aggregate}
        kwargs["retry"] = -1
        with self.assertRaises(Exception) as context:
            cstsuites.concurrent_login_logout_test(**kwargs)
        self.assertIn("in login group can login", context.exception.args[0])

        self.router.invoke = MagicMock()

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstsuites.Thread")
    @patch("jnpr.toby.bbe.cst.cstsuites.unicast_traffic_test")
    @patch("jnpr.toby.bbe.cst.cstsuites.run_multiple")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_for_concurrent_test")
    def test_inflight_tests(self, patch_prepare_for_concurrent_test, patch_run_multiple,
                            patch_unicast_traffic_test, patch_thread, patch_sleep):
        list_of_action_dicts = [{"fname": "False"}, {"fname": "False"}]
        # list_of_action_dicts = [{"fname": "print('eval is dangerous')"}, {"fname": "print('but acceptable here')"}]
        patch_thread.return_value.is_alive.side_effect = [False, True, True, False, True, False]
        self.assertEqual(cstsuites.inflight_tests(list_of_action_dicts), None)

        kwargs = {"mode": "parallel"}
        list_of_action_dicts = None
        patch_thread.return_value.is_alive.side_effect = [True, False]
        self.assertEqual(cstsuites.inflight_tests(list_of_action_dicts, **kwargs), None)

        patch_thread.return_value.start.side_effect = Exception
        #with self.assertRaises(Exception) as context:
        cstsuites.inflight_tests(list_of_action_dicts, **kwargs)
        #self.assertIn("failed to start concurrent login-logout in the background", context.exception.args[0])

    @patch("time.sleep")
    @patch("re.match")
    @patch("re.search")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_master_re_name")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_route")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_count")
    @patch("jnpr.toby.bbe.cst.cstsuites.panic_re_recover")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.unicast_traffic_test")
    def test_gres_test(self, patch_unicast_traffic_test, patch_start_traffic, patch_panic_re_recover,
                       patch_verify_client_count, patch_verify_client_route, patch_stop_traffic,
                       patch_verify_traffic, patch_get_master_re_name, patch_cpu_settle,
                       patch_re_search, patch_re_match, patch_sleep):
        builtins.t.get_resource.return_value = {"system": {"primary": {"controllers": {"re0":{}}}}}
        self.assertEqual(cstsuites.gres_test(), None)
        builtins.t.get_resource.return_value = {"system": {"primary": {"controllers": {"re0": {}, "re1": {}}}}}
        self.router.get_current_controller_name.return_value = "re0"
        patch_re_search.side_effect = itertools.cycle([False, True])
        patch_re_match.side_effect = itertools.cycle([False, True])
        resp = self.router.pyez.return_value.resp
        resp.findtext.side_effect = itertools.cycle(["Enabled", "Synchronized"])
        patch_get_master_re_name.return_value = "re1"
        self.router.cli.return_value.resp = 'Switchover Status: Ready'
        kwargs = {
            "gres_type": "cli",
            "command": "switch"
        }
        self.assertEqual(cstsuites.gres_test(**kwargs), None)
        kwargs["command"] = "release"
        self.assertEqual(cstsuites.gres_test(**kwargs), None)
        kwargs["command"] = "acquire"
        #builtins.t.get_resource.return_value = {"system": {"primary": {"controllers": {"re0":{}, "re1":{}}}}}
        self.assertEqual(cstsuites.gres_test(**kwargs), None)
        kwargs["gres_type"] = "power_cycle"
        self.assertEqual(cstsuites.gres_test(**kwargs), None)
        kwargs["gres_type"] = "kernel_crash"
        self.assertEqual(cstsuites.gres_test(**kwargs), None)

        patch_get_master_re_name.return_value = "re0"
        with self.assertRaises(Exception) as context:
            cstsuites.gres_test(**kwargs)
        self.assertIn("master RE did not change, please check the router", context.exception.args[0])
        self.router.reconnect.side_effect = Exception
        with self.assertRaises(Exception) as context:
            cstsuites.gres_test(**kwargs)
        self.assertIn("router connection failed to be restored after waiting for", context.exception.args[0])
        kwargs["gres_type"] = "power_cycle"
        patch_re_match.side_effect = None
        patch_re_match.return_value = False
        with self.assertRaises(Exception) as context:
            cstsuites.gres_test(**kwargs)
        self.assertIn("failed to power-on the other re after waiting", context.exception.args[0])
        resp.findtext.side_effect = None
        resp.findtext.return_value = None
        with self.assertRaises(Exception) as context:
            cstsuites.gres_test(**kwargs)
        self.assertIn("Database Replication - Not Synchronized", context.exception.args[0])
        patch_re_search.side_effect = None
        patch_re_search.return_value = False
        with self.assertRaises(Exception) as context:
            cstsuites.gres_test(**kwargs)
        self.assertIn("Routing Engine is not ready for master switch even after maximum wait of", context.exception.args[0])

        self.router.get_current_controller_name = MagicMock()
        self.router.pyez = MagicMock()
        builtins.t.get_resource = MagicMock()
        builtins.bbe.get_devices = MagicMock()

    @patch("time.sleep")
    @patch("time.time")
    @patch("re.match")
    @patch("re.search")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_release_clients")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_start_clients")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_count")
    @patch("jnpr.toby.bbe.cst.cstsuites.unicast_traffic_test")
    def test_fpc_mic_restart_test(self, patch_unicast_traffic_test, patch_verify_client_count,
                                  patch_cst_start_clients, patch_cst_release_clients, patch_cpu_settle,
                                  patch_re_search, patch_re_match, patch_time, patch_sleep):
        # Make time go up by 1 sec every time it is called
        patch_time.side_effect = itertools.count()

        patch_re_match.return_value.group.side_effect = lambda x: x
        builtins.bbe.get_interfaces.return_value = False

        kwargs = {
            "component": "fpc",
            "action": "restart"
        }
        resp = self.router.pyez.return_value.resp
        resp.findtext.side_effect = itertools.cycle(["Offline", "Online"])
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        builtins.bbe.get_interfaces.return_value = [MagicMock(), MagicMock(), MagicMock()]
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        patch_verify_client_count.side_effect = Exception
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        self.assertTrue(patch_cpu_settle.called)
        kwargs["fpc_slot"] = "25"
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        kwargs["action"] = "panic"
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        kwargs["action"] = "offon"
        patch_re_match.side_effect = lambda x, y, z="": False if x == r'MX(80|80-t|40|40-t|10|10-t|5|5-t)' else MagicMock()
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        patch_re_match.side_effect = None
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)

        kwargs["component"] = "mic"
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        kwargs["action"] = "restart"
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        patch_re_search.return_value = False
        del kwargs["fpc_slot"]
        pic1 = MagicMock()
        pic1.findtext.side_effect = ['0', 'offline']
        pic2 = MagicMock()
        pic2.findtext.side_effect = ['1', 'offline']
        pic3 = MagicMock()
        pic3.findtext.side_effect = ['0', 'online']
        pic4 = MagicMock()
        pic4.findtext.side_effect = ['1', 'online']
        resp.findall.side_effect = [[pic1, pic2], [pic3, pic4]]
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        pic5 = MagicMock()
        pic5.findtext.side_effect = ['0', 'offline']
        pic6 = MagicMock()
        pic6.findtext.side_effect = ['1', 'offline']
        pic7 = MagicMock()
        pic7.findtext.side_effect = ['0', 'online']
        pic8 = MagicMock()
        pic8.findtext.side_effect = ['1', 'online']
        resp.findall.side_effect = [[pic5, pic6], [pic7, pic8]]
        kwargs["action"] = "panic"
        self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)
        kwargs["action"] = "restart"
        resp.findall.side_effect = None
        pic = MagicMock()
        pic_cycle = itertools.cycle(["Offline", "Online"])
        pic.findtext.side_effect = lambda x: 2 if x == "pic-slot" else next(pic_cycle)
        resp.findall.return_value = [pic]
        with self.assertRaises(Exception) as context:
            cstsuites.fpc_mic_restart_test(**kwargs)
        self.assertIn(" failed to be ", context.exception.args[0])
        with self.assertRaises(Exception) as context:
            cstsuites.fpc_mic_restart_test(**kwargs)
        self.assertIn(" failed to be ", context.exception.args[0])
        #self.assertEqual(cstsuites.fpc_mic_restart_test(**kwargs), None)

        kwargs["action"] = "panic"
        with self.assertRaises(Exception) as context:
            cstsuites.fpc_mic_restart_test(**kwargs)
        self.assertIn(" failed to be ", context.exception.args[0])

        kwargs["action"] = "restart"
        with self.assertRaises(Exception) as context:
            cstsuites.fpc_mic_restart_test(**kwargs)
        self.assertIn(" failed to be ", context.exception.args[0])
        kwargs["component"] = "fpc"
        resp.findtext.side_effect = None
        with self.assertRaises(Exception) as context:
            cstsuites.fpc_mic_restart_test(**kwargs)
        self.assertIn(" failed to come back online after ", context.exception.args[0])
        kwargs["fpc_slot"] = "25"
        kwargs["action"] = "offon"
        patch_re_match.return_value = False
        with self.assertRaises(Exception) as context:
            cstsuites.fpc_mic_restart_test(**kwargs)
        self.assertIn(" failed to be offline", context.exception.args[0])
        kwargs["action"] = "panic"
        with self.assertRaises(Exception) as context:
            cstsuites.fpc_mic_restart_test(**kwargs)
        self.assertIn("not able to set vty security mode", context.exception.args[0])
        kwargs["action"] = "restart"
        with self.assertRaises(Exception) as context:
            cstsuites.fpc_mic_restart_test(**kwargs)
        self.assertIn(" can not be restarted", context.exception.args[0])


        self.router.pyez = MagicMock()
        builtins.bbe.get_interfaces = MagicMock()


    @patch("jnpr.toby.bbe.cst.cstsuites.daemon_actions")
    def test_daemon_restart_test(self, patch_daemon_actions):
        self.assertEqual(cstsuites.daemon_restart_test(), None)

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.add_subscriber_mesh")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_release_clients")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_start_clients")
    def test_login_logout_test(self, patch_cst_start_clients, patch_cst_release_clients, patch_add_subscriber_mesh,
                               patch_start_traffic, patch_verify_traffic, patch_cpu_settle, patch_sleep):
        self.assertEqual(cstsuites.login_logout_test(), None)
        kwargs = {"duration": 2}
        self.assertEqual(cstsuites.login_logout_test(**kwargs), None)
        patch_cst_start_clients.side_effect = itertools.chain(iter([Exception]), itertools.repeat(None))
        self.assertEqual(cstsuites.login_logout_test(**kwargs), None)

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_start_clients")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_interface_bounce_test(self, patch_prepare_subscriber_traffic, patch_cst_start_clients,
                                   patch_cpu_settle, patch_sleep):
        builtins.bbe.get_interfaces.return_value = [MagicMock(), MagicMock(), MagicMock()]
        self.assertEqual(cstsuites.interface_bounce_test(), None)
        patch_cst_start_clients.side_effect = [Exception, None]
        self.assertEqual(cstsuites.interface_bounce_test(), None)
        builtins.bbe.get_interfaces = MagicMock()

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_count")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_ae_info")
    def test_ae_failover_test(self, patch_get_ae_info, patch_prepare_subscriber_traffic,
                              patch_verify_client_count, patch_start_traffic, patch_stop_traffic,
                              patch_verify_traffic, patch_sleep):
        self.assertEqual(cstsuites.ae_failover_test(), None)
        ae_members = {
            "aename1": {
                "active": [MagicMock(), MagicMock(), MagicMock()],
            },
            "aename2": {
                "active": [MagicMock()],
                "standby": [MagicMock(), MagicMock(), MagicMock()]
            },
            "aename3": {
                "active": [MagicMock()],
                "standby": [MagicMock(), MagicMock(), MagicMock()]
            },
            "aename4": {
                "active": []
            },
            "aename5": {
                "active": []
            },
        }
        patch_get_ae_info.return_value = ae_members
        kwargs = {}
        kwargs["ae_list"] = list(ae_members.keys())
        kwargs["ae_list"].pop()
        kwargs["action"] = "deactivate"
        self.assertEqual(cstsuites.ae_failover_test(**kwargs), None)
        kwargs["action"] = "switchover"
        lacp_proto = MagicMock()
        lacp_proto_gen = itertools.cycle([ae_members["aename2"]["active"][0], ae_members["aename3"]["active"][0]])
        lacp_proto.findtext.side_effect = lambda x: "Collecting distributing" if x == "lacp-mux-state" else next(lacp_proto_gen)
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [lacp_proto]
        self.assertEqual(cstsuites.ae_failover_test(**kwargs), None)
        kwargs["action"] = "laseroff"
        self.assertEqual(cstsuites.ae_failover_test(**kwargs), None)

        lacp_proto.findtext.side_effect = lambda x: "Collecting distributing" if x == "lacp-mux-state" else ae_members["aename2"]["active"][0]
        with self.assertRaises(Exception) as context:
            self.assertEqual(cstsuites.ae_failover_test(**kwargs), None)
        self.assertIn(" failed to switch over", context.exception.args[0])
        kwargs["action"] = "switchover"
        with self.assertRaises(Exception) as context:
            self.assertEqual(cstsuites.ae_failover_test(**kwargs), None)
        self.assertIn(" failed to switch over", context.exception.args[0])

        lacp_proto_gen = itertools.cycle([ae_members["aename2"]["active"][0], ae_members["aename3"]["active"][0]])
        lacp_proto.findtext.side_effect = lambda x: "Collecting distributing" if x == "lacp-mux-state" else next(lacp_proto_gen)
        ae_members = {
            "aename1": {
                "active": [MagicMock(), MagicMock(), MagicMock()],
            }
        }
        kwargs["ae_list"] = list(ae_members.keys())
        self.assertEqual(cstsuites.ae_failover_test(**kwargs), None)
        kwargs["action"] = "laseroff"
        self.assertEqual(cstsuites.ae_failover_test(**kwargs), None)

        self.router.pyez = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstsuites.check_fpc")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_start_clients")
    def test_reboot_and_rebind_test(self, patch_cst_start_clients, patch_prepare_subscriber_traffic, patch_check_fpc):
        self.assertEqual(cstsuites.reboot_and_rebind_test(), None)
        self.router.reboot.return_value = False
        with self.assertRaises(Exception) as context:
            self.assertEqual(cstsuites.reboot_and_rebind_test(), None)
        self.assertIn("REs failed to be online after reboot", context.exception.args[0])

        self.router.reboot = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.re_actions")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_reboot_standby_re_test(self, patch_prepare_subscriber_traffic, patch_start_traffic,
                                    patch_re_actions, patch_stop_traffic, patch_verify_traffic):
        self.assertEqual(cstsuites.reboot_standby_re_test(), None)

    @patch("time.sleep")
    @patch("re.match")
    @patch("random.sample")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_router_sub_summary_by_port")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_port_laser_blink_test(self, patch_prepare_subscriber_traffic, patch_get_router_sub_summary,
                                   patch_get_router_sub_summary_by_port, patch_cpu_settle, patch_random_sample,
                                   patch_re_match, patch_sleep):
        self.assertEqual(cstsuites.port_laser_blink_test(), None)

        ports = [MagicMock(), MagicMock()]
        for i, port in enumerate(ports):
            port.interface_pic = str(i)
        patch_random_sample.return_value = [ports[0].interface_pic]
        patch_get_router_sub_summary_by_port.return_value = {ports[1].interface_pic: "Test"}
        builtins.bbe.get_interfaces.return_value = ports
        resp = self.router.pyez.return_value.resp
        resp.findtext.side_effect = itertools.cycle(["down", "up"])

        self.assertEqual(cstsuites.port_laser_blink_test(), None)
        builtins.bbe.get_connection.return_value.device_id = "rt"
        self.assertEqual(cstsuites.port_laser_blink_test(), None)

        patch_get_router_sub_summary_by_port.side_effect = [{"1": "Test"}, {"1": "Test", "2": "Nope"}]
        kwargs = {"rebind": False}
        with self.assertRaises(Exception) as context:
            cstsuites.port_laser_blink_test(**kwargs)
        self.assertIn("port laser blink test failed", context.exception.args[0])
        patch_get_router_sub_summary_by_port.side_effect = [{"1": "Test"}, {"1": "Nope"}]
        kwargs["rebind"] = True
        with self.assertRaises(Exception) as context:
            cstsuites.port_laser_blink_test(**kwargs)
        self.assertIn("port laser blink test failed", context.exception.args[0])
        patch_get_router_sub_summary_by_port.side_effect = None
        resp.findtext.side_effect = ["down", "down"]
        with self.assertRaises(Exception) as context:
            cstsuites.port_laser_blink_test(**kwargs)
        self.assertIn("port laser blink test failed", context.exception.args[0])
        builtins.bbe.get_interfaces.return_value = False
        self.assertEqual(cstsuites.port_laser_blink_test(**kwargs), None)

        self.router.pyez = MagicMock()
        builtins.bbe.get_interfaces = MagicMock()
        builtins.bbe.get_connection = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_route")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_count")
    @patch("jnpr.toby.bbe.cst.cstsuites.interface_bounce")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_vcp_ports")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_ae_info")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_link_redundancy_test(self, patch_prepare_subscriber_traffic, patch_get_ae_info,
                                  patch_get_vcp_ports, patch_interface_bounce, patch_verify_client_count,
                                  patch_verify_client_route):
        ae_members = {
            "aename1": {
                "active": [MagicMock(), MagicMock(), MagicMock()],
            },
            "aename2": {
                "active": [MagicMock()],
                "standby": [MagicMock(), MagicMock(), MagicMock()]
            }
        }
        patch_get_ae_info.return_value = ae_members
        patch_get_vcp_ports.return_value = {"member0": []}
        builtins.bbe.get_interfaces.return_value = [MagicMock()]
        kwargs = {"link_type": "uplink"}
        self.assertEqual(cstsuites.link_redundancy_test(**kwargs), None)

        patch_verify_client_count.side_effect = Exception
        with self.assertRaises(Exception) as context:
            cstsuites.link_redundancy_test(**kwargs)
        self.assertIn("link redundancy test failed", context.exception.args[0])

        builtins.bbe.get_interfaces = MagicMock()

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_release_clients")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_start_clients")
    def test_no_radius_bind_test(self, patch_cst_start_clients, patch_cst_release_clients, patch_sleep):
        resp = self.router.pyez.return_value.resp
        resp.findtext.side_effect = ["down", "up"]
        patch_cst_start_clients.side_effect = Exception
        self.assertEqual(cstsuites.no_radius_bind_test(), None)

        resp.findtext.side_effect = None
        resp.findtext.return_value = "down"
        with self.assertRaises(Exception) as context:
            cstsuites.no_radius_bind_test()
        self.assertIn("no radius bind test failed", context.exception.args[0])
        resp.findtext.return_value = "up"
        with self.assertRaises(Exception) as context:
            cstsuites.no_radius_bind_test()
        self.assertIn("no radius bind test failed", context.exception.args[0])
        patch_cst_start_clients.side_effect = None
        with self.assertRaises(Exception) as context:
            cstsuites.no_radius_bind_test()
        self.assertIn("no radius bind test failed", context.exception.args[0])

        self.router.pyez = MagicMock()

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_count")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_ae_info")
    def test_ae_member_delete_add_test(self, patch_get_ae_info, patch_prepare_subscriber_traffic, patch_start_traffic,
                                       patch_verify_traffic, patch_stop_traffic, patch_verify_client_count, patch_sleep):
        self.assertEqual(cstsuites.ae_member_delete_add_test(), None)

        ae_members = {
            "aename1": {
                "active": [MagicMock(), MagicMock(), MagicMock()],
            },
            "aename2": {
                "active": [MagicMock()],
                "standby": [MagicMock(), MagicMock(), MagicMock()]
            },
            "aename3": {
                "active": [MagicMock()]
            }
        }
        patch_get_ae_info.return_value = ae_members
        self.assertEqual(cstsuites.ae_member_delete_add_test(), None)
        patch_verify_client_count.side_effect = itertools.cycle([Exception, MagicMock()])
        with self.assertRaises(Exception) as context:
            cstsuites.ae_member_delete_add_test()
        self.assertIn("AE member add delete test failed", context.exception.args[0])
        self.router.cli.side_effect = lambda **kwargs: MagicMock(resp=MagicMock())
        with self.assertRaises(Exception) as context:
            cstsuites.ae_member_delete_add_test()
        self.assertIn(" state changed after delete/add", context.exception.args[0])

        self.router.cli = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_cgnat_traffic_test(self, patch_prepare_subscriber_traffic, patch_get_router_sub_summary,
                                patch_start_traffic, patch_stop_traffic, patch_verify_traffic):
        resp = self.router.pyez.return_value.resp
        patch_get_router_sub_summary.return_value = {"client": resp.findtext.return_value}
        self.assertEqual(cstsuites.cgnat_traffic_test(), None)
        patch_get_router_sub_summary.return_value = {"client": MagicMock()}
        with self.assertRaises(Exception) as context:
            cstsuites.cgnat_traffic_test()
        self.assertIn("the session count is not equal to the client count", context.exception.args[0])

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_lawful_intercept_test(self, patch_prepare_subscriber_traffic, patch_get_router_sub_summary,
                                   patch_start_traffic, patch_verify_traffic, patch_sleep):
        self.assertEqual(cstsuites.lawful_intercept_test(), None)
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [MagicMock()]
        self.assertEqual(cstsuites.lawful_intercept_test(), None)

        self.router.shell.side_effect = [MagicMock(), MagicMock(resp="CoA-NAK")]
        with self.assertRaises(Exception) as context:
            cstsuites.lawful_intercept_test()
        self.assertIn("failed to deactivate lawful intercept using command ", context.exception.args[0])
        self.router.shell.side_effect = [MagicMock(resp="CoA-NAK")]
        with self.assertRaises(Exception) as context:
            cstsuites.lawful_intercept_test()
        self.assertIn("failed to activate lawful intercept using command ", context.exception.args[0])

        self.router.pyez = MagicMock()
        self.router.shell = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstsuites.unicast_traffic_test")
    @patch("jnpr.toby.bbe.cst.cstsuites.check_fpc")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_router_before_login")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_release_clients")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_configured_subs")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_start_clients")
    @patch("jnpr.toby.bbe.cst.cstsuites.clear_subscribers_in_router")
    def test_stress_test(self, patch_unicast_traffic_test, patch_cst_start_clients, patch_get_configured_subs, patch_clear_subscribers_in_router,
                         patch_get_router_sub_summary, patch_cst_release_clients, patch_prepare_router_before_login,
                         patch_check_fpc):
        kwargs = {"csr": [400, 500]}
        builtins.bbe.cst_stats.__contains__.return_value = True
        patch_get_router_sub_summary.return_value = {"total": 10}
        #patch_get_configured_subs.return_value = {"expected_login_rate": 50}
        self.assertEqual(cstsuites.stress_test(**kwargs), None)
        kwargs["csr"] = 200
        self.assertEqual(cstsuites.stress_test(**kwargs), None)
        builtins.bbe.cst_stats = MagicMock()

    @patch("time.sleep")
    @patch("re.match")
    @patch("re.search")
    @patch("random.choice")
    @patch("jnpr.toby.bbe.cst.cstsuites.unicast_traffic_test")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_release_clients")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_radius_redundancy_test(self, patch_prepare_subscriber_traffic, patch_cst_release_clients, patch_unicast_traffic_test,
                                    patch_random_choice, patch_re_search, patch_re_match, patch_sleep):
        self.assertEqual(cstsuites.radius_redundancy_test(), None)
        builtins.bbe.get_devices.return_value = ["h0", "h1"]
        kwargs = {"radius_method": "not_stop"}
        patch_re_match.side_effect = [MagicMock(), False, MagicMock(), MagicMock(), False, MagicMock()]
        self.assertEqual(cstsuites.radius_redundancy_test(**kwargs), None)
        kwargs["radius_method"] = "stop"
        kwargs["radius_order"] = ["h0", "h1"]
        patch_re_match.side_effect = [False, MagicMock(), False, MagicMock()]
        self.assertEqual(cstsuites.radius_redundancy_test(**kwargs), None)
        patch_re_match.side_effect = None
        patch_re_match.return_value = False
        with self.assertRaises(Exception) as context:
            cstsuites.radius_redundancy_test(**kwargs)
        self.assertIn(" failed to be started", context.exception.args[0])
        patch_re_match.return_value = None
        patch_re_search.return_value = False
        with self.assertRaises(Exception) as context:
            cstsuites.radius_redundancy_test(**kwargs)
        self.assertIn("router did not detect the radius ", context.exception.args[0])
        patch_re_match.return_value = True
        with self.assertRaises(Exception) as context:
            cstsuites.radius_redundancy_test(**kwargs)
        self.assertIn("failed to shutdown radius server ", context.exception.args[0])

        builtins.bbe.get_devices = MagicMock()

    @patch("time.time")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cstsuites.CheckCli")
    @patch("jnpr.toby.bbe.cst.cstsuites.Thread")
    @patch("jnpr.toby.bbe.cst.cstsuites.gres_test")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_route")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_count")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_bbe_issu_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_stop_traffic,
                       patch_verify_traffic, patch_verify_client_count, patch_verify_client_route, patch_gres_test,
                       patch_thread, patch_checkcli, patch_cpu_settle, patch_time):
        # Make time go up by 1 sec every time it is called
        patch_time.side_effect = itertools.count()
        patch_checkcli.return_value.get_runtime.return_value = 1
        patch_checkcli.return_value.verify_cli_output.return_value = None
        kwargs = {
            "upgrade_image": MagicMock(),
            "pre_issu_action": ["traffic", "gres"],
            "post_issu_action": ["traffic", "gres"],
            "check_show_cmds": "show subscribers summary"
        }
        IDLE = "Chassisd ISSU State  IDLE\n    ISSU State           IDLE\n    ISSU Wait            0"
        SWITCHOVER_READY = "Chassisd ISSU State  DAEMON_SWITCHOVER_PREPARE\n    ISSU State           SWITCHOVER_READY\n    ISSU Wait            0"
        self.router.cli.side_effect = itertools.cycle([MagicMock(resp=IDLE),MagicMock(resp=SWITCHOVER_READY)])
        
        self.assertEqual(cstsuites.bbe_issu_test(**kwargs), None)

        # Test functions that are normally called within one of the threads
        #run_issu = patch_thread.call_args_list[0][1]["target"]
        #state_check = patch_thread.call_args_list[1][1]["target"]
        #exceptions_thrown = {"run_issu": None, "state_check": None} 
        #self.assertEqual(run_issu(self.router, MagicMock(), exceptions_thrown), None)
        #self.assertEqual(state_check(self.router, MagicMock(), MagicMock(), exceptions_thrown), None)
        #self.router.software_install.side_effect = Exception
        #self.assertEqual(run_issu(self.router, MagicMock(), exceptions_thrown), None)
        #self.assertIsNotNone(exceptions_thrown["run_issu"])
        #self.router.cli.side_effect = Exception
        #self.assertEqual(state_check(self.router, MagicMock(), MagicMock(), exceptions_thrown), None)
        #self.assertIsNotNone(exceptions_thrown["state_check"])

        # We need to change exceptions_thrown when running a new Thread
        # We use a named function because a lambda expression can't handle assignment
        #def add_exceptions_thrown_to_thread(**kwargs):
        #    kwargs["args"][-1]["run_issu"] = Exception()
        #    return MagicMock()
        #patch_thread.side_effect = add_exceptions_thrown_to_thread
        #with self.assertRaises(Exception) as context:
        #    cstsuites.bbe_issu_test(**kwargs)
        #def add_exceptions_thrown_to_thread(**kwargs):
        #    kwargs["args"][-1]["state_check"] = Exception()
        #    return MagicMock()
        #patch_thread.side_effect = add_exceptions_thrown_to_thread
        #with self.assertRaises(Exception) as context:
        #    cstsuites.bbe_issu_test(**kwargs)
        #patch_thread.side_effect = None

        kwargs["minimum_rx_percentage"] = 50
        self.assertEqual(cstsuites.bbe_issu_test(**kwargs), None)

        patch_checkcli.return_value.get_runtime.return_value = 90
        with self.assertRaises(Exception) as context:
            cstsuites.bbe_issu_test(**kwargs)
        self.assertIn("check_show_cmds took too long to run, would cause problems during testing ISSU", context.exception.args[0])

        patch_time.side_effect = None
        self.router.software_install.side_effect = None
        self.router.cli.side_effect = None

    @patch("time.sleep")
    @patch("time.time")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_rt_subs_info")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_clean_rebind_test(self, patch_prepare_subscriber_traffic, patch_get_router_sub_summary,
                               patch_get_rt_subs_info, patch_time, patch_sleep):
        # Make time go up by 1 sec every time it is called
        patch_time.side_effect = itertools.count()

        builtins.bbe.get_interfaces.return_value = [MagicMock(), MagicMock()]
        resp = self.router.pyez.return_value.resp
        resp.findtext.side_effect = ["down", "down", "down", "down", "up", "up", "up", "up"]
        patch_get_router_sub_summary.return_value = {"client": 0}
        patch_get_rt_subs_info.side_effect = [{"rt_sessions_up": 1}, {"rt_sessions_up": 0}]
        self.assertEqual(cstsuites.clean_rebind_test(), None)

        resp.findtext.side_effect = None
        resp.findtext.return_value = "down"
        patch_get_rt_subs_info.side_effect = [{"rt_sessions_up": 1}, {"rt_sessions_up": 0}]
        with self.assertRaises(Exception) as context:
            cstsuites.clean_rebind_test()
        self.assertIn("clean test failed", context.exception.args[0])
        patch_get_rt_subs_info.side_effect = None
        patch_get_rt_subs_info.return_value = {"rt_sessions_up": 1}
        patch_get_router_sub_summary.return_value = {"client": 1}
        with self.assertRaises(Exception) as context:
            cstsuites.clean_rebind_test()
        self.assertIn("clean test failed", context.exception.args[0])
        resp.findtext.return_value = "up"
        with self.assertRaises(Exception) as context:
            cstsuites.clean_rebind_test()
        self.assertIn("some interfaces failed to be in down state after disable", context.exception.args[0])

        builtins.bbe.get_interfaces = MagicMock()
        self.router.pyez = MagicMock()

    @patch("time.sleep")
    @patch("random.sample")
    @patch("jnpr.toby.bbe.cst.cstsuites.clear_subscriber_sessions")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_session_ids")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstsuites.get_configured_subs")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.cst_start_clients")
    def test_subscriber_delete_test(self, patch_cst_start_clients, patch_prepare_subscriber_traffic, patch_get_router_sub_summary, patch_get_configured_subs,
                                    patch_get_session_ids, patch_clear_subscriber_sessions, patch_random_sample, patch_sleep):
        kwargs = {"client_type": "dhcp"}
        patch_get_session_ids.return_value = [MagicMock()]
        patch_get_router_sub_summary.side_effect = [{"client": 10}, {"client": 9}]
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
        patch_get_configured_subs.return_value = {"expected_login_rate": 1}
        patch_get_router_sub_summary.side_effect = [{"client": 10}, {"client": 9}]
        #self.assertEqual(cstsuites.subscriber_delete_test(**kwargs), None)
        with self.assertRaises(Exception) as context:
            cstsuites.subscriber_delete_test(**kwargs)
        self.assertIn("client", context.exception.args[0])
        patch_get_router_sub_summary.side_effect = None
        patch_get_router_sub_summary.return_value = {"client": 10}
        with self.assertRaises(Exception) as context:
            cstsuites.subscriber_delete_test(**kwargs)
        self.assertIn("", context.exception.args[0])

        builtins.bbe.get_subscriber_handles = MagicMock()

    @patch("time.sleep")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_service_activate_deactive_test(self, patch_prepare_subscriber_traffic, patch_start_traffic,
                                            patch_stop_traffic, patch_verify_traffic, patch_sleep):
        kwargs = {
            "service_name": "service",
            "verify_traffic": True
        }
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [MagicMock(text=MagicMock())]
        self.router.cli.return_value.resp = "Successful"
        self.assertEqual(cstsuites.service_activate_deactive_test(**kwargs), None)
        kwargs["method"] = "radius"
        self.assertEqual(cstsuites.service_activate_deactive_test(**kwargs), None)

        kwargs["method"] = "cli"
        self.router.cli.return_value.resp = MagicMock()
        with self.assertRaises(Exception) as context:
            cstsuites.service_activate_deactive_test(**kwargs)
        self.assertIn(" service using command ", context.exception.args[0])
        kwargs["method"] = "radius"
        self.router.shell.side_effect = [MagicMock(), MagicMock(resp="CoA-NAK")]
        with self.assertRaises(Exception) as context:
            cstsuites.service_activate_deactive_test(**kwargs)
        self.assertIn("failed to deactive service using command ", context.exception.args[0])
        self.router.shell.side_effect = None
        self.router.shell.return_value.resp = "CoA-NAK"
        with self.assertRaises(Exception) as context:
            cstsuites.service_activate_deactive_test(**kwargs)
        self.assertIn("failed to active service using command ", context.exception.args[0])

        self.router.pyez = MagicMock()
        self.router.cli = MagicMock()
        self.router.shell = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstsuites.verify_client_count")
    @patch("jnpr.toby.bbe.cst.cstsuites.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.unicast_traffic_test")
    @patch("jnpr.toby.bbe.cst.cstsuites.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstsuites.prepare_subscriber_traffic")
    def test_image_upgrade_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_stop_traffic,
                                patch_unicast_traffic_test, patch_verify_traffic, patch_verify_client_count):
        kwargs = {"image_file": MagicMock()}
        self.assertEqual(cstsuites.image_upgrade_test(**kwargs), None)
        kwargs["style"] = "switch"
        self.assertEqual(cstsuites.image_upgrade_test(**kwargs), None)


if __name__ == "__main__":
    unittest.main()
