import unittest
import builtins
import itertools
from unittest.mock import MagicMock
from unittest.mock import patch
import jnpr.toby.bbe.cst.dtcp_suites as dtcp_suites


class TestDtcpSuites(unittest.TestCase):
    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.router = MagicMock()
        builtins.t.get_handle.return_value = self.router
        builtins.bbe = MagicMock()
        
    @patch("jnpr.toby.bbe.cst.dtcp_suites.time.sleep")
    @patch("random.sample")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.get_dtcp_li_candidates")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.run_multiple")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.stop_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_dtcp_concurrent_trigger_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_stop_traffic,
                                          patch_verify_traffic, patch_get_router_sub_summary, patch_run_multiple,
                                          patch_get_dtcp_li_candidates, patch_dtcp_add_li_trigger, patch_dtcp_delete_li_trigger,
                                          patch_random_sample, patch_sleep):
        with self.assertRaises(Exception) as e:
            self.assertEqual(dtcp_suites.dtcp_concurrent_trigger_test(), None)
        patch_run_multiple.side_effect = Exception
        with self.assertRaises(Exception) as e:
            with self.assertRaises(Exception) as context:
                dtcp_suites.dtcp_concurrent_trigger_test()
            self.assertIn("the parallel run of dtcp failed", context.exception.args[0])

    @patch("jnpr.toby.bbe.cst.dtcp_suites.time.sleep")
    @patch("random.sample")
    @patch("jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.cpu_settle")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.get_dtcp_li_candidates")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_release_clients")
    @patch("jnpr.toby.bbe.cst.cstutils.cst_start_clients")
    @patch("jnpr.toby.bbe.cst.cstutils.add_subscriber_mesh")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    def test_dtcp_logout_login_with_same_trigger_test(self, patch_start_traffic, patch_verify_traffic, patch_add_subscriber_mesh,
                                                      patch_cst_start_clients, patch_cst_release_clients, patch_get_router_sub_summary,
                                                      patch_get_dtcp_li_candidates, patch_dtcp_add_li_trigger,
                                                      patch_dtcp_delete_li_trigger, patch_cpu_settle, patch_random_sample, patch_sleep):
        with self.assertRaises(Exception) as e:
            self.assertEqual(dtcp_suites.dtcp_logout_login_with_same_trigger_test(), None)
        kwargs = {"no_trigger_change": False}
        kwargs["duration"] = 10
        with self.assertRaises(Exception) as e:
            self.assertEqual(dtcp_suites.dtcp_logout_login_with_same_trigger_test(**kwargs), None)

    @patch("re.search")
    @patch("random.sample")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_list_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.get_dtcp_li_candidates")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_dtcp_confidentiality_test(self, patch_prepare_subscriber_traffic, patch_get_dtcp_li_candidates, patch_dtcp_add_li_trigger,
                                       patch_dtcp_delete_li_trigger, patch_dtcp_list_li_trigger, patch_random_sample, patch_re_search):
        patch_get_dtcp_li_candidates.return_value = {
            "interface_id": ["Hello"],
            "session_id": ["World"]
        }
        patch_random_sample.return_value = ["Hello"]
        patch_dtcp_list_li_trigger.return_value = [MagicMock()]
        patch_re_search.return_value = False
        self.assertEqual(dtcp_suites.dtcp_confidentiality_test(), None)

        patch_re_search.return_value = True
        with self.assertRaises(Exception) as context:
            dtcp_suites.dtcp_confidentiality_test()
        self.assertIn("intercept id should not be visible in cli output", context.exception.args[0])
        patch_dtcp_list_li_trigger.return_value = [MagicMock(), MagicMock()]
        with self.assertRaises(Exception) as context:
            dtcp_suites.dtcp_confidentiality_test()
        self.assertIn(" li triggers in the router, not the expected ", context.exception.args[0])
        patch_dtcp_list_li_trigger.return_value = MagicMock()
        with self.assertRaises(Exception) as context:
            dtcp_suites.dtcp_confidentiality_test()
        self.assertIn("no criteria id returned, please check logs", context.exception.args[0])

    @patch("jnpr.toby.bbe.cst.dtcp_suites.time.sleep")
    @patch("random.sample")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_list_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_delete_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_add_li_trigger")
    @patch("jnpr.toby.bbe.cst.dtcp_suites.get_dtcp_li_candidates")
    @patch("jnpr.toby.bbe.cst.cstutils.get_router_sub_summary")
    @patch("jnpr.toby.bbe.cst.cstutils.verify_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.start_traffic")
    @patch("jnpr.toby.bbe.cst.cstutils.prepare_subscriber_traffic")
    def test_dtcp_trigger_test(self, patch_prepare_subscriber_traffic, patch_start_traffic, patch_verify_traffic,
                               patch_get_router_sub_summary, patch_get_dtcp_li_candidates, patch_dtcp_add_li_trigger,
                               patch_dtcp_delete_li_trigger, patch_dtcp_list_li_trigger, patch_random_sample, patch_sleep):
        patch_get_dtcp_li_candidates.return_value = {
            "interface_id": ["Hello"],
            "session_id": ["World"]
        }
        patch_dtcp_list_li_trigger.return_value = [MagicMock()]
        self.assertEqual(dtcp_suites.dtcp_trigger_test(), None)

        patch_dtcp_list_li_trigger.return_value = [MagicMock(), MagicMock()]
        with self.assertRaises(Exception) as context:
            dtcp_suites.dtcp_trigger_test()
        self.assertIn(" li triggers in the router, not the expected ", context.exception.args[0])
        patch_dtcp_list_li_trigger.return_value = MagicMock()
        with self.assertRaises(Exception) as context:
            dtcp_suites.dtcp_trigger_test()
        self.assertIn("no criteria id returned, please check logs", context.exception.args[0])

    @patch("time.sleep")
    @patch("time.time")
    @patch("re.search")
    @patch("re.findall")
    @patch("paramiko.SSHClient")
    @patch("jnpr.toby.bbe.cst.cstutils.get_master_re_name")
    def test_dtcp_flowtap_client(self, patch_get_master_re_name, patch_paramiko_SSHClient,
                                 patch_re_findall, patch_re_search, patch_time, patch_sleep):
        # Make time go up by 1 sec every time it is called
        patch_time.side_effect = itertools.count()

        kwargs = {"dtcp_cmds": "cmd"}
        client = patch_paramiko_SSHClient.return_value
        transport = client.get_transport.return_value
        channel = transport.open_session.return_value
        channel.send.return_value = 1
        data = channel.recv.return_value
        del builtins.bbe.dtcp_criteria
        del builtins.bbe.dtcp_seq_num

        patch_re_findall.return_value = [MagicMock()]
        data.decode.return_value = "200 OK: CRITERIA-NUM"
        self.assertEqual(dtcp_suites.dtcp_flowtap_client(**kwargs), patch_re_findall.return_value)
        data.decode.return_value = "200 OK"
        self.assertTrue(dtcp_suites.dtcp_flowtap_client(**kwargs))
        kwargs["dtcp_cmds"] = "ADD"
        kwargs["hostname"] = "hostname"
        self.assertEqual(dtcp_suites.dtcp_flowtap_client(**kwargs), [patch_re_search.return_value.group.return_value])

        data.decode.return_value = "NOT OK"
        with self.assertRaises(Exception) as context:
            dtcp_suites.dtcp_flowtap_client(**kwargs)
        self.assertIn(" DTCP commands failed", context.exception.args[0])
        channel.recv.return_value = 0
        with self.assertRaises(Exception) as context:
            dtcp_suites.dtcp_flowtap_client(**kwargs)
        self.assertIn("dtcp channel was closed unexpectedly", context.exception.args[0])
        channel.send.return_value = 0
        with self.assertRaises(Exception) as context:
            dtcp_suites.dtcp_flowtap_client(**kwargs)
        self.assertIn("failed to send command after retries", context.exception.args[0])
        channel.recv_ready.return_value = False
        with self.assertRaises(Exception) as context:
            dtcp_suites.dtcp_flowtap_client(**kwargs)
        self.assertIn("did not receive any data from router", context.exception.args[0])        

        builtins.bbe.dtcp_criteria = MagicMock()
        builtins.bbe.dtcp_seq_num = MagicMock()

    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_flowtap_client")
    def test_dtcp_delete_li_trigger(self, patch_dtcp_flowtap_client):
        self.assertEqual(dtcp_suites.dtcp_delete_li_trigger(), None)
        kwargs = {"criteria_id": "criteria_id"}
        self.assertEqual(dtcp_suites.dtcp_delete_li_trigger(**kwargs), None)

    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_flowtap_client")
    def test_add_li_trigger(self, patch_dtcp_flowtap_client):
        kwargs = {"trigger_list": "trigger", "trigger_type": "interface_id"}
        self.assertEqual(dtcp_suites.dtcp_add_li_trigger(**kwargs), patch_dtcp_flowtap_client.return_value)
        kwargs["trigger_type"] = "username"
        self.assertEqual(dtcp_suites.dtcp_add_li_trigger(**kwargs), patch_dtcp_flowtap_client.return_value)
        kwargs["trigger_type"] = "session_id"
        self.assertEqual(dtcp_suites.dtcp_add_li_trigger(**kwargs), patch_dtcp_flowtap_client.return_value)
        kwargs["trigger_type"] = "ip_addr"
        self.assertEqual(dtcp_suites.dtcp_add_li_trigger(**kwargs), patch_dtcp_flowtap_client.return_value)

    @patch("jnpr.toby.bbe.cst.dtcp_suites.dtcp_flowtap_client")
    def test_dtcp_list_li_trigger(self, patch_dtcp_flowtap_client):
        self.assertEqual(dtcp_suites.dtcp_list_li_trigger(), patch_dtcp_flowtap_client.return_value)

    def test_get_dtcp_li_candidates(self):
        resp = self.router.pyez.return_value.resp
        resp.findall.return_value = [MagicMock(text="*"), MagicMock(text="my_text")]
        expected_output = {
            "interface_id": ["my_text"],
            "username": ["*", "my_text"],
            "session_id": ["*", "my_text"]
        }
        self.assertEqual(dtcp_suites.get_dtcp_li_candidates(), expected_output)

        self.router.pyez = MagicMock()

if __name__ == "__main__":
    unittest.main()
