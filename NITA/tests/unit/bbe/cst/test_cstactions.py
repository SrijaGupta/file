import unittest
import builtins
import itertools
from unittest.mock import MagicMock
from unittest.mock import patch
import jnpr.toby.bbe.cst.cstactions as cstactions


class TestCstActions(unittest.TestCase):
    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.router = MagicMock()
        builtins.t.get_handle.return_value = self.router
        builtins.bbe = MagicMock()

    @patch("time.sleep")
    @patch("re.match")
    @patch("jnpr.toby.bbe.cst.cstutils.panic_re_recover")
    @patch("jnpr.toby.bbe.cst.cstutils.check_re_status")
    def test_re_actions(self, patch_check_re_status, patch_panic_re_recover, patch_re_match, patch_sleep):
        kwargs = {
            "action": "power_cycle",
            "type": "master"
        }
        builtins.t.get_resource.return_value = {
            "system": {
                "primary": {
                    "controllers": [self.router.get_current_controller_name.return_value, MagicMock()]
                }
            }
        }
        resp = self.router.pyez.return_value.resp
        resp.findtext.return_value = "Present"
        self.assertEqual(cstactions.re_actions(**kwargs), None)
        kwargs["action"] = "reboot"
        self.assertEqual(cstactions.re_actions(**kwargs), None)
        kwargs["action"] = "kernel_crash"
        self.assertEqual(cstactions.re_actions(**kwargs), None)

        kwargs["action"] = "power_cycle"
        resp.findtext.return_value = MagicMock()
        with self.assertRaises(Exception) as context:
            cstactions.re_actions(**kwargs)
        self.assertIn(" was in abnormal state", context.exception.args[0])

        self.router.pyez = MagicMock()
        builtins.t.get_resource = MagicMock()

    @patch("time.sleep")
    @patch("re.match")
    @patch("random.choice")
    def test_interface_bounce(self, patch_random_choice, patch_re_match, patch_sleep):
        kwargs = {"method": "cli", "interface": {"vcp": MagicMock()}}
        self.router.cli.side_effect = [MagicMock(), MagicMock(), MagicMock(resp="error"), MagicMock(), MagicMock()]
        self.assertEqual(cstactions.interface_bounce(**kwargs), None)
        self.router.cli.side_effect = None
        del kwargs["interface"]
        kwargs["interface_id"] = "radius"
        resp = self.router.pyez.return_value.resp
        resp.findtext.side_effect = ["down", "up"]
        self.assertEqual(cstactions.interface_bounce(**kwargs), None)
        kwargs["method"] = "laseroff"
        resp.findtext.side_effect = ["down", "up"]
        builtins.bbe.get_interfaces.return_value = [MagicMock(interface_pic=MagicMock())]
        self.assertEqual(cstactions.interface_bounce(**kwargs), None)

        resp.findtext.side_effect = None
        del kwargs["interface_id"]
        with self.assertRaises(Exception) as context:
            cstactions.interface_bounce(**kwargs)
        self.assertIn(" state not in expected state after flapping", context.exception.args[0])
        kwargs["method"] = "cli"
        with self.assertRaises(Exception) as context:
            cstactions.interface_bounce(**kwargs)
        self.assertIn(" state not in expected state after flapping", context.exception.args[0])
        self.router.config.return_value.resp = "error"
        with self.assertRaises(Exception) as context:
            cstactions.interface_bounce(**kwargs)
        self.assertIn(" state not in expected state after flapping", context.exception.args[0])
        patch_random_choice.return_value = {"vcp": MagicMock()}
        self.router.cli.side_effect = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(resp="error")]
        with self.assertRaises(Exception) as context:
            cstactions.interface_bounce(**kwargs)
        self.assertIn(" state not in expected state after flapping", context.exception.args[0])

        self.router.pyez = MagicMock()
        self.router.cli = MagicMock()
        self.router.config = MagicMock()
        builtins.bbe.get_interfaces = MagicMock()

    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    @patch("jnpr.toby.bbe.cst.cstactions.re_actions")
    def test_re_failover(self, patch_re_actions, patch_get_master_re_name):
        self.assertEqual(cstactions.re_failover(), None)
        self.assertEqual(cstactions.re_failover(method="reboot"), None)

    @patch("time.sleep")
    @patch("time.time")
    @patch("re.match")
    @patch("re.search")
    @patch("random.choice")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.get_rt_subs_info")
    def test_fpc_actions(self, patch_get_rt_subs_info, patch_get_router_sub_summary, patch_random_choice,
                         patch_re_search, patch_re_match, patch_time, patch_sleep):
        # Make time go up by 60 sec every time it is called
        patch_time.side_effect = itertools.count(step=60)
        resp = self.router.pyez.return_value.resp
        resp.findtext.return_value = "Online"
        builtins.bbe.get_interfaces.return_value = [MagicMock()]
        kwargs = {"action": "restart"}
        self.assertEqual(cstactions.fpc_actions(**kwargs), None)
        kwargs["action"] = "panic"
        self.assertEqual(cstactions.fpc_actions(**kwargs), None)
        kwargs["action"] = "offon"
        self.assertEqual(cstactions.fpc_actions(**kwargs), None)
        kwargs["fpc"] = MagicMock()
        self.assertEqual(cstactions.fpc_actions(**kwargs), None)

        patch_get_rt_subs_info.side_effect = itertools.cycle([{"rt_sessions_up": 0}, {"rt_sessions_up": 1}])
        with self.assertRaises(Exception) as context:
            cstactions.fpc_actions(**kwargs)
        self.assertIn("subscribers count still not stable after 3600s", context.exception.args[0])
        resp.findtext.return_value = "Offline"
        with self.assertRaises(Exception) as context:
            cstactions.fpc_actions(**kwargs)
        self.assertIn(" failed to come back online after 600s", context.exception.args[0])
        patch_re_match.return_value = False
        kwargs["action"] = "offon"
        with self.assertRaises(Exception) as context:
            cstactions.fpc_actions(**kwargs)
        self.assertIn("failed to be offline", context.exception.args[0])
        patch_re_search.return_value = False
        kwargs["action"] = "panic"
        with self.assertRaises(Exception) as context:
            cstactions.fpc_actions(**kwargs)
        self.assertIn("not able to set vty security mode", context.exception.args[0])
        del kwargs["action"]
        patch_random_choice.return_value = "restart"
        with self.assertRaises(Exception) as context:
            cstactions.fpc_actions(**kwargs)
        self.assertIn(" can not be restarted", context.exception.args[0])
        del kwargs["fpc"]
        builtins.bbe.get_interfaces.return_value = False
        self.assertEqual(cstactions.fpc_actions(**kwargs), None)

        self.router.pyez = MagicMock()
        builtins.bbe.get_interfaces = MagicMock()

    @patch("time.sleep")
    @patch("re.match")
    @patch("re.search")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    @patch("jnpr.toby.bbe.cst.cstutils.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.add_subscriber_mesh")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_start_clients")
    def test_daemon_actions(self, patch_cst_start_clients, patch_add_subscriber_mesh, patch_start_traffic,
                            patch_verify_traffic, patch_stop_traffic, patch_get_master_re_name, patch_cpu_settle,
                            patch_re_search, patch_re_match, patch_sleep):
        kwargs = {"verify_traffic": True, "re_in_action": MagicMock()}
        patch_cst_start_clients.side_effect = [Exception, None]
        self.assertEqual(cstactions.daemon_actions(**kwargs), None)
        patch_cst_start_clients.side_effect = None
        kwargs["duration"] = 10
        self.router.vc = False
        self.assertEqual(cstactions.daemon_actions(**kwargs), None)
        kwargs["action"] = "coredump"
        # Two different match iterms to make pid/new_pid not equal
        patch_re_match.return_value = False
        patch_re_search.return_value = False
        self.assertEqual(cstactions.daemon_actions(**kwargs), None)
        patch_re_match.return_value = MagicMock()
        patch_re_match.side_effect = itertools.cycle([MagicMock(), MagicMock()])
        self.assertEqual(cstactions.daemon_actions(**kwargs), None)
        kwargs["action"] = "kill"
        self.assertEqual(cstactions.daemon_actions(**kwargs), None)

        kwargs["action"] = "coredump"
        patch_re_search.return_value = True
        patch_re_match.side_effect = [MagicMock(), MagicMock(), False]
        with self.assertRaises(Exception) as context:
            cstactions.daemon_actions(**kwargs)
        #self.assertIn("daemon was not restarted", context.exception.args[0])
        patch_re_search.side_effect = None
        patch_re_match.side_effect = None
        kwargs["action"] = "kill"
        with self.assertRaises(Exception) as context:
            cstactions.daemon_actions(**kwargs)
        self.assertIn(" was not killed", context.exception.args[0])
        patch_re_search.return_value = False
        kwargs["daemon_list"] = ["authd", "fake"]
        self.assertEqual(cstactions.daemon_actions(**kwargs), None)
        kwargs["daemon_list"] = "authd"
        self.assertEqual(cstactions.daemon_actions(**kwargs), None)

        self.router.vc = MagicMock()

    @patch("time.sleep")
    @patch("re.match")
    @patch("re.findall")
    def test_kill_busy_process(self, patch_re_findall, patch_re_match, patch_sleep):
        patch_re_findall.return_value = ["Hello", "World"]
        self.assertEqual(cstactions.kill_busy_process(), None)
        builtins.bbe.cst_action_stats = {"processed_daemon": ["Hello", "World"]}
        patch_re_match.return_value.group.return_value = "Hello"
        with self.assertRaises(Exception) as context:
            cstactions.kill_busy_process()
        self.assertIn(" was not killed", context.exception.args[0])

        builtins.bbe.cst_action_stats = MagicMock()

    @patch("time.sleep")
    @patch("random.choice")
    @patch("jnpr.toby.bbe.cst.cstutils.get_ae_info")
    def test_ae_reconfig(self, patch_get_ae_info, patch_random_choice, patch_sleep):
        patch_random_choice.return_value = "ae_intf"
        patch_get_ae_info.return_value = {"ae_intf": {"active": 5, "standby": 5}}
        self.assertEqual(cstactions.ae_reconfig(), None)
        patch_get_ae_info.return_value = None
        self.assertEqual(cstactions.ae_reconfig(), None)

if __name__ == "__main__":
    unittest.main()
