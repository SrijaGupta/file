import unittest
import builtins
from mock import patch, MagicMock, mock
from jnpr.toby.bbe.bbekeywords import *
from jnpr.toby.bbe.bbevar.bbevars import BBEVars, BBEVarInterface
#from jnpr.toby.bbe.bbevar.subscribers import DHCPSubscribers, PPPoESubscribers
from jnpr.toby.init.init import init
builtins.t = MagicMock()

builtins.t.log = MagicMock()

builtins.bbe = MagicMock()


class TestBBeKeywords(unittest.TestCase):
    """
    TestIxiaTester class to handle bbekeywords.py unit tests
    """
    @patch('jnpr.toby.bbe.cst.cstutils.cst_start_clients')
    def test_start_clients(self, patch_cst):
        patch_cst.return_value = True
        self.assertEqual(start_clients(), True)

    @patch('jnpr.toby.bbe.cst.cstutils.cst_release_clients')
    def test_stop_clients(self, patch_cst):
        patch_cst.return_value = True
        self.assertEqual(stop_clients(), True)

    def test_get_subscriber_handle(self):
        builtins.bbe.get_subscriber_handles.return_value = ['sub1']
        self.assertIsInstance(get_subscriber_handle(), list)

    @patch('builtins.hasattr')
    def test_subscriber_action(self, patch_attr):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        subs = [MagicMock()]
        self.assertEqual(subscriber_action(subscriber_handle=subs, action='start'), None)
        patch_attr.return_value = True
        subs[0].rt_dhcpv6_handle = None
        self.assertEqual(subscriber_action(subscriber_handle=subs, action='start'), None)
        patch_attr.side_effect = [False, True]
        self.assertEqual(subscriber_action(subscriber_handle=subs, action='start'), None)
        patch_attr.side_effect = None

    @patch('builtins.hasattr')
    def test_login_subscriber(self, patch_attr):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        subs = [MagicMock()]
        self.assertEqual(login_subscribers(subscriber_handle=subs), None)
        patch_attr.return_value = True
        subs[0].rt_dhcpv6_handle = None
        self.assertEqual(login_subscribers(subscriber_handle=subs), None)
        patch_attr.side_effect = [False, True]
        self.assertEqual(login_subscribers(subscriber_handle=subs), None)
        patch_attr.side_effect = None

    @patch('builtins.hasattr')
    def test_logout_subscriber(self, patch_attr):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        subs = [MagicMock()]
        self.assertEqual(logout_subscribers(subscriber_handle=subs), None)
        patch_attr.return_value = True
        subs[0].rt_dhcpv6_handle = None
        self.assertEqual(logout_subscribers(subscriber_handle=subs), None)
        patch_attr.side_effect = [False, True]
        self.assertEqual(logout_subscribers(subscriber_handle=subs), None)
        patch_attr.side_effect = None

    @patch('builtins.hasattr')
    def test_restart_unbound_subscribers(self, patch_attr):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        subs = [MagicMock()]
        self.assertEqual(restart_unbound_subscribers(subscriber_handle=subs), None)
        patch_attr.return_value = True
        subs[0].rt_dhcpv6_handle = None
        self.assertEqual(restart_unbound_subscribers(subscriber_handle=subs), None)
        patch_attr.side_effect = [False, True]
        self.assertEqual(restart_unbound_subscribers(subscriber_handle=subs), None)
        patch_attr.side_effect = None


    def test_get_configured_subscriber_count(self):
        self.assertIsInstance(get_configured_subscriber_count(), object)


    def test_match_subscriber_attribute(self):
        try:
            match_subscriber_attribute('r0', 'dhcp', 'user-name', 'test')
        except Exception as err:
            self.assertTrue('Values for attribute  dont match' in err.args[0])
        obj1 = MagicMock()
        obj1.text = 'test'
        obj2 = MagicMock()
        obj2.text = 'test2'
        builtins.t.get_handle.return_value.execute_rpc.return_value = MagicMock()
        builtins.t.get_handle.return_value.execute_rpc.return_value.response.return_value = MagicMock()
        builtins.t.get_handle.return_value.execute_rpc.return_value.response.return_value.findall.return_value = [obj1, obj2]
        self.assertEqual(match_subscriber_attribute('r0', 'dhcp', 'user-name', ['test', 'test2']), True)


    def test_start_all_protocols(self):
        self.assertEqual(start_all_protocols(), None)


    def test_stop_all_protocols(self):
        self.assertEqual(stop_all_protocols(), None)

    def test_bbe_get_interfaces(self):
        self.assertIsInstance(bbe_get_interfaces(), object)

    def test_get_configured_dhcp_client_count(self):
        self.assertIsInstance(get_configured_dhcp_client_count(), object)

    def test_get_dhcp_client_count(self):
        self.assertIsInstance(get_dhcp_client_count(), object)

    @patch('jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.get_dhcp_subscriber_count')
    def test_verify_dhcp_client_count(self, patch_junos):
        try:
            verify_dhcp_client_count(5)
        except Exception as err:
            self.assertTrue('expected DHCP subscribers are bound' in err.args[0])
        obj1 = MagicMock()
        obj1.active = 5
        patch_junos.return_value = obj1

        self.assertEqual(verify_dhcp_client_count(5), True)

    def test_login_all_dhcpv4_clients(self):
        obj1 = MagicMock()
        obj1.rt_dhcpv4_handle = 'v4'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(login_all_dhcpv4_clients(), None)

    def test_logout_all_dhcpv4_clients(self):
        obj1 = MagicMock()
        obj1.rt_dhcpv4_handle = 'v4'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(logout_all_dhcpv4_clients(), None)

    def test_restart_all_unbound_dhcpv4_clients(self):
        obj1 = MagicMock()
        obj1.rt_dhcpv4_handle = 'v4'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(restart_all_unbound_dhcpv4_clients(), None)

    def test_login_all_dhcpv6_clients(self):
        obj1 = MagicMock()
        obj1.rt_dhcpv6_handle = 'v6'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(login_all_dhcpv6_clients(), None)

    def test_logout_all_dhcpv6_clients(self):
        obj1 = MagicMock()
        obj1.rt_dhcpv6_handle = 'v6'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(logout_all_dhcpv6_clients(), None)

    def test_restart_all_unbound_dhcpv6_clients(self):
        obj1 = MagicMock()
        obj1.rt_dhcpv4_handle = 'v6'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(restart_all_unbound_dhcpv6_clients(), None)

    def test_bbe_get_rt_dhcp_server(self):
        self.assertIsInstance(bbe_get_rt_dhcp_server(), object)

    def test_get_configured_pppoe_client_count(self):
        self.assertIsInstance(get_configured_pppoe_client_count(), object)

    def test_get_pppoe_client_count(self):
        self.assertIsInstance(get_pppoe_client_count(), object)

    @patch('jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.get_pppoe_subscriber_count')
    def test_verify_pppoe_client_count(self, patch_junos):
        try:
            verify_pppoe_client_count(5)
        except Exception as err:
            self.assertTrue('expected PPPoE subscribers are active' in err.args[0])
        obj1 = MagicMock()
        obj1.active = 5
        patch_junos.return_value = obj1

        self.assertEqual(verify_pppoe_client_count(5), True)

    def test_login_all_pppoev4_clients(self):
        obj1 = MagicMock()
        obj1.rt_pppox_handle = 'v4'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(login_all_pppoev4_clients(), None)

    def test_logout_all_pppoev4_clients(self):
        obj1 = MagicMock()
        obj1.rt_pppox_handle = 'v4'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(logout_all_pppoev4_clients(), None)

    def test_restart_all_unbound_pppoev4_clients(self):
        obj1 = MagicMock()
        obj1.rt_pppox_handle = 'v4'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(restart_all_unbound_pppoev4_clients(), None)

    def test_login_all_pppoev6_clients(self):
        obj1 = MagicMock()
        obj1.rt_dhcpv6_handle = 'pppoxclient'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(login_all_pppoev6_clients(), None)

    def test_logout_all_pppoev6_clients(self):
        obj1 = MagicMock()
        obj1.rt_dhcpv6_handle = 'pppoxclient'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(logout_all_pppoev6_clients(), None)

    def test_restart_all_unbound_pppoev6_clients(self):
        obj1 = MagicMock()
        obj1.rt_dhcpv6_handle = 'l2tp'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(restart_all_unbound_pppoev6_clients(), None)

    @patch('jnpr.toby.bbe.bbeutils.junosutil.BBEJunosUtil.get_l2tp_subscriber_count')
    def test_verify_l2tp_client_count(self, patch_junos):
        try:
            verify_l2tp_client_count(5)
        except Exception as err:
            self.assertTrue('expected L2TP subscribers are active' in err.args[0])
        obj1 = MagicMock()
        obj1.active = 5
        patch_junos.return_value = obj1

        self.assertEqual(verify_l2tp_client_count(5), True)

    def test_login_all_l2tp_clients(self):
        obj1 = MagicMock()
        obj1.rt_pppox_handle = 'l2tp'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(login_all_l2tp_clients(), None)

    def test_logout_all_l2tp_clients(self):
        obj1 = MagicMock()
        obj1.rt_pppox_handle = 'l2tp'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(logout_all_l2tp_clients(), None)

    def test_flap_all_ancp_sublines(self):
        obj1 = MagicMock()
        obj1.rt_ancp_line_handle = 'line'
        obj1.has_ancp = True
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(flap_all_ancp_sublines(builtins.t.get_handle.return_value), None)

    def test_get_ancp_neighbor_count(self):
        self.assertIsInstance(get_ancp_neighbor_count('rt0'), object)

    def test_get_ancp_subscriber_count(self):
        self.assertIsInstance(get_ancp_subscriber_count('rt0'), object)

    @patch('re.match')
    def test_init_radius_server(self, patch_match):
        obj1 = MagicMock()
        self.assertIsInstance(init_radius_server(obj1), object)

    def test_add_radius_client(self):
        obj1 = MagicMock(spec=FreeRadius)
        self.assertEqual(add_radius_client(obj1, client_name='test'), None)

    def test_delete_radius_client(self):
        obj1 = MagicMock(spec=FreeRadius)
        self.assertEqual(delete_radius_client(obj1, client='test'), None)

    def test_add_radius_user(self):
        obj1 = MagicMock(spec=FreeRadius)
        self.assertEqual(add_radius_user(obj1, user='user', request_avp='request_avp', reply_avp='reply_avp'), None)

    def test_delete_radius_user(self):
        obj1 = MagicMock(spec=FreeRadius)
        self.assertEqual(delete_radius_user(obj1, 'user'), None)

    def test_commit_radius_user(self):
        obj1 = MagicMock(spec=FreeRadius)
        self.assertEqual(commit_radius_user(obj1), None)

    def test_modify_radius_auth(self):
        obj1 = MagicMock(spec=FreeRadius)
        self.assertEqual(modify_radius_auth(obj1, 'auth_order'), None)

    def test_start_radius(self):
        obj1 = MagicMock(spec=FreeRadius)
        self.assertEqual(start_radius(obj1), None)

    def test_stop_radius(self):
        obj1 = MagicMock(spec=FreeRadius)
        self.assertEqual(stop_radius(obj1), None)

    def test_restart_radius(self):
        obj1 = MagicMock(spec=FreeRadius)
        self.assertEqual(restart_radius(obj1), None)

    def test_add_bidirectional_dhcp_ipv4_subscriber_traffic(self):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        obj1 = MagicMock()
        obj1.protocol = 'dhcp'
        obj1.family = 'ipv4'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(add_bidirectional_dhcp_ipv4_subscriber_traffic(name='test'), None)

    def test_add_bidirectional_pppoe_ipv4_subscriber_traffic(self):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        obj1 = MagicMock()
        obj1.protocol = 'pppoe'
        obj1.family = 'ipv4'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(add_bidirectional_pppoe_ipv4_subscriber_traffic(name='test'), None)

    def test_add_bidirectional_ipv6_subscriber_traffic(self):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        obj1 = MagicMock()
        obj1.rt_dhcpv6_handle = 'v6'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        self.assertEqual(add_bidirectional_ipv6_subscriber_traffic(name='test'), None)

    def test_add_bidirectional_traffic_to_all_subscribers(self):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        obj1 = MagicMock()
        obj1.protocol = 'dhcp'
        obj1.family = 'ipv4'
        obj2 = MagicMock()
        obj2.protocol = 'dhcp'
        obj2.family = 'ipv6'
        obj3 = MagicMock()
        obj3.protocol = 'dhcp'
        obj3.family = 'dual'
        obj11 = MagicMock()
        obj11.protocol = 'pppoe'
        obj11.family = 'ipv4'
        obj12 = MagicMock()
        obj12.protocol = 'pppoe'
        obj12.family = 'ipv6'
        obj13 = MagicMock()
        obj13.protocol = 'pppoe'
        obj13.family = 'dual'
        builtins.bbe.get_subscriber_handles.return_value = [obj1, obj2, obj3, obj11, obj12, obj13]
        self.assertEqual(add_bidirectional_traffic_to_all_subscribers(), True)
        obj1.protocol = 'l2tp'
        builtins.bbe.get_subscriber_handles.return_value = [obj1]
        try:
            add_bidirectional_traffic_to_all_subscribers()
        except:
            self.assertRaises(Exception)


    @patch('jnpr.toby.bbe.bbekeywords.sleep', return_value=None)
    def test_edit_traffic_stream(self, patch_sleep):
        #patch_sleep.return_value = False
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        builtins.t.get_handle.return_value.traffic_item = ['test_s1', 'test_s1v4', 'test_s1v6']
        self.assertEqual(edit_traffic_stream(stream_name='s1'), True)
        try:
            edit_traffic_stream(stream_name=None)
        except:
            self.assertRaises(Exception)
        try:
            edit_traffic_stream(stream_name='s2')
        except:
            self.assertRaises(Exception)

    @patch('jnpr.toby.bbe.bbekeywords.sleep', return_value=None)
    def test_configure_traffic_stream(self, patch_sleep):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        obj1 = MagicMock()
        obj1.protocol = 'dhcp'
        obj1.family = 'ipv4'
        obj2 = MagicMock()
        obj2.protocol = 'dhcp'
        obj2.family = 'ipv6'
        obj3 = MagicMock()
        obj3.protocol = 'dhcp'
        obj3.family = 'dual'
        obj11 = MagicMock()
        obj11.protocol = 'pppoe'
        obj11.family = 'ipv4'
        obj12 = MagicMock()
        obj12.protocol = 'pppoe'
        obj12.family = 'ipv6'
        obj13 = MagicMock()
        obj13.protocol = 'pppoe'
        obj13.family = 'dual'
        builtins.bbe.get_subscriber_handles.return_value = [obj1, obj2, obj3, obj11, obj12, obj13]
        builtins.t.get_handle.return_value.traffic_item = ['item1']
        self.assertEqual(configure_traffic_stream('s1', subscriber_tag='test'), True)
        try:
            configure_traffic_stream(stream_name=None)
        except:
            self.assertRaises(Exception)
        self.assertEqual(configure_traffic_stream('s1', subscriber_tag='test', emulation_as_source=False,
                                                  bidirectional=1, uplink='uplink1'), True)

        try:
            obj1.family = 'l2tp'
            builtins.bbe.get_subscriber_handles.return_value = [obj1]
            self.assertEqual(configure_traffic_stream('s1', subscriber_tag='test'), True)
        except:
            self.assertRaises(Exception)

    @patch('jnpr.toby.bbe.bbekeywords.sleep', return_value=None)
    def test_perform_traffic_stream_action(self, patch_sleep):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        builtins.t.get_handle.return_value.traffic_item = ['item1']
        self.assertEqual(perform_traffic_stream_action('start'), True)
        builtins.t.get_handle.return_value.traffic_item = ['test_s1', 'test_s1v4', 'test_s1v6']
        self.assertEqual(perform_traffic_stream_action('start', stream_name='s1'), True)
        try:
            perform_traffic_stream_action('start', stream_name='s2')
        except:
            self.assertRaises(Exception)

    def test_verify_traffic_throughput(self):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        self.assertIsInstance(verify_traffic_throughput(), dict)

    def test_configure_raw_form_traffic_stream(self):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        self.assertIsInstance(configure_raw_form_traffic_stream('s1', '1/1', '1/2', '11', '22'), dict)

    @patch('jnpr.toby.bbe.bbekeywords.sleep', return_value=None)
    def test_add_bidirectional_l2_vlan_subscriber_traffic(self, patch_sleep):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}

        try:
            builtins.bbe.get_subscriber_handles.return_value = False
            add_bidirectional_l2_vlan_subscriber_traffic('100', 'uplink1')
        except:
            self.assertRaises(Exception)

        try:
            builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
            builtins.bbe.get_interfaces.return_value = False
            add_bidirectional_l2_vlan_subscriber_traffic('100', 'uplink1')
        except:
            self.assertRaises(Exception)
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
        builtins.bbe.get_interfaces.return_value = [MagicMock()]
        self.assertEqual(add_bidirectional_l2_vlan_subscriber_traffic('100', 'up'), None)

    def test_start_valid8_server(self):
        server1 = MagicMock()
        self.assertEqual(start_valid8_server(server1, 'h1', 'v4', 'cfg', 'pcrf', 'nasreq', 'ocs'), None)

    def test_stop_valid8_server(self):
        server1 = MagicMock()
        self.assertEqual(stop_valid8_server(server1, 'h1'), None)

    def test_send_asr(self):
        server1 = MagicMock()
        self.assertEqual(send_asr(server1, 'h1'), None)

    def test_init_valid8_server(self):
        server1 = MagicMock()
        self.assertIsInstance(init_valid8_server(server1), object)

    def test_clear_logs_from_dut(self):
        builtins.bbe.get_devices.return_value = [MagicMock()]
        self.assertEqual(clear_logs_from_dut(), True)

    #
    # def test_get_router_sub_summary(self):
    #     builtins.t.get_handle.return_value.pyez.return_value.resp = MagicMock()
    #     builtins.t.get_handle.return_value.pyez.return_value.resp.findall.return_value = [MagicMock()]
    #     self.assertIsInstance(get_router_sub_summary(), dict)

    @patch('jnpr.toby.bbe.bbekeywords.sleep', return_value=None)
    def test_ls_testcase_action(self, patch_sleep):
        try:
            bbe_ls_testcase_action(action='start')
        except Exception as err:
            self.assertEqual(err.args[0], 'subscriber must be provided')
        obj2 = MagicMock()
        obj2.isactive = True
        builtins.bbe.get_subscriber_handles.return_value = [obj2]
        actions = ['capture_stop', 'capture_start', 'logout', 'delete', 'results', 'check_session_status']
        sub1 = MagicMock()
        for action in actions:
            self.assertIsInstance(bbe_ls_testcase_action(subscriber=sub1, action=action, port='access', state='waiting'),
                                  object)
        sub1.action.return_value = False
        try:
            bbe_ls_testcase_action(subscriber=sub1, action='capture_stop', port='access')
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to get the pcap file after 20 retries')

        # action=capture_config
        result = bbe_ls_testcase_action(subscriber=sub1, action='capture_config', port='control', on_start='true',
                                    source_ip_filter='1.2.3.4', dest_ip_filter='4.3.2.1')
        # action=is_fireball
        self.assertIsInstance(bbe_ls_testcase_action(subscriber=sub1, action='is_fireball'), bool)

    @patch('yaml.load')
    @patch('builtins.open', create=True)
    def test_parse_bbe_license_file(self, patch_open, patch_yaml):
        patch_open.return_value = {'xx': 'yy'}
        patch_yaml.return_value = 'license'
        self.assertEqual(parse_bbe_license_file('test.yaml'), 'license')
        patch_open.side_effect = Exception
        self.assertEqual(parse_bbe_license_file('test.yaml'), False)
        patch_open.side_effect = None

    def test_bbe_get_devices(self):
        builtins.bbe.get_devices.return_value = [MagicMock()]
        self.assertIsInstance(bbe_get_devices(), list)
        builtins.t.get_junos_resources.return_value = ['r0']
        builtins.bbe.get_devices.side_effect = NameError
        self.assertEqual(bbe_get_devices(device_tag='r0'), ['r0'])
        builtins.bbe.get_devices.side_effect = None


    @patch('jnpr.toby.bbe.cst.cstutils.check_fpc')
    @patch('jnpr.toby.bbe.cst.cstutils.check_link_status')
    @patch('re.findall')
    def test_bbe_topology_check(self, patch_findall, patch_linkcheck, patch_checkfpc):
        obj1 = MagicMock()
        obj1.interface_config = {'ip': '10.0.0.1/24', 'ipv6': '2000::1/64'}
        obj2 = MagicMock()
        obj2.interface_config = {}
        obj2.interface_id = 'uplink0'
        builtins.bbe.get_interfaces.return_value = [obj1, obj2]
        builtins.bbe.get_connection.return_value = obj1
        router = MagicMock()
        builtins.t.get_handle.return_value = router
        router.cli.return_value.resp = "icmp_sequence 1"
        self.assertEqual(bbe_topology_check(), None)
        router.cli.return_value.resp = "icmp_sequence 1 Authentication: No response"
        with self.assertRaises(Exception) as context:
            bbe_topology_check()
        self.assertIn("Radius Daemon does not respond to the test", context.exception.args[0])
        patch_findall.return_value = False
        with self.assertRaises(Exception) as context:
            bbe_topology_check()
        self.assertIn("ping address", context.exception.args[0])
        patch_findall.return_value = MagicMock()

    def test_is_dual_re(self):
        router = MagicMock()
        builtins.t.get_handle.return_value = router
        self.assertEqual(is_dual_re(), False)
        router.vc = False
        router.current_node.controllers = {'re0':'', 're1':''}
        self.assertEqual(is_dual_re(), True)
        router.current_node.controllers = {'re0': ''}
        self.assertEqual(is_dual_re(), False)
        router.vc = True

if __name__ == '__main__':
    unittest.main()
