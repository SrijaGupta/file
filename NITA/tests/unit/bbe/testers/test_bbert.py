"""
bbert.py unit test
"""

import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.bbevar.bbevars import BBEVars, BBEVarInterface
from jnpr.toby.bbe.errors import BBEDeviceError
import builtins
from jnpr.toby.bbe.testers.bbert import create_ancp_node, create_rt_dhcp_subscribers, create_rt_hag_subscribers,\
    create_rt_l2bsa_subscribers, create_rt_l2tp_subscribers, create_rt_pppoe_subscribers, add_mcast_client,\
    add_rt_ae, add_rt_bgp_neighbor, add_rt_dhcp_servers, add_rt_links, add_rt_lns, set_subscribers_call_rate,\
    bbe_rt_init, create_rt_cups_subscribers, create_rt_pgw_subscribers, create_fwa_subscribers, add_rt_isis_l3
builtins.t = MagicMock(spec=init)
builtins.t.log.return_value = MagicMock()
builtins.t.resources = {'rt0':{'system':{'primary':{'tapip':'10.0.2.1'}}}}
builtins.t.get_handle.return_value = MagicMock()
builtins.bbe = MagicMock(spec=BBEVars)
from jnpr.toby.bbe.bbevar.subscribers import HAGSubscribers, DHCPSubscribers, PPPoESubscribers, L2BSASubscribers,\
    L2TPSubscribers, DHCPOption, VlanRange


class TestBbeRt(unittest.TestCase):
    """
    test bbert.py
    """
    @patch('jnpr.toby.bbe.testers.bbert.create_fwa_subscribers')
    @patch('jnpr.toby.bbe.testers.bbert.create_rt_pgw_subscribers')
    @patch('jnpr.toby.bbe.testers.bbert.create_rt_cups_subscribers')
    @patch('jnpr.toby.bbe.testers.bbert.add_rt_dhcp_servers')
    @patch('jnpr.toby.bbe.testers.bbert.add_rt_bgp_neighbor')
    @patch('jnpr.toby.bbe.testers.bbert.add_rt_isis_l3')
    @patch('jnpr.toby.bbe.testers.bbert.add_rt_lns')
    @patch('jnpr.toby.bbe.testers.bbert.add_rt_links')
    @patch('jnpr.toby.bbe.testers.bbert.set_subscribers_call_rate')
    @patch('jnpr.toby.bbe.testers.bbert.add_mcast_client')
    @patch('jnpr.toby.bbe.testers.bbert.create_rt_l2bsa_subscribers')
    @patch('jnpr.toby.bbe.testers.bbert.create_rt_l2tp_subscribers')
    @patch('jnpr.toby.bbe.testers.bbert.create_rt_pppoe_subscribers')
    @patch('jnpr.toby.bbe.testers.bbert.create_rt_dhcp_subscribers')
    @patch('jnpr.toby.bbe.testers.bbert.create_ancp_node')
    @patch('jnpr.toby.bbe.testers.bbert.add_rt_ae')
    @patch('jnpr.toby.bbe.testers.bbert.create_rt_hag_subscribers')
    def test_bbe_rt_init(self, patch_hag, patch_add_ae, patch_ancp, patch_dhcp, patch_pppoe, patch_l2tp, patch_l2bsa,
                         patch_mcast, patch_set_rate, patch_link, patch_lns, patch_isis, patch_bgp, patch_dhcpserver,
                         patch_cups, patch_pgw, patch_fwa):
        builtins.t.resources = {'rt0': {'system': {'primary': {'landslide-manager': '10.0.2.1'}}}}
        builtins.bbe.bbevar = {'resources': {'rt0':{}}}
        rt_device = MagicMock()
        rt_device.device_id = 'rt0'
        builtins.bbe.get_devices.return_value = [rt_device]
        hag_sub = MagicMock()
        hag_sub.rt_device_id = 'rt0'
        hag_sub.subscribers_type = 'hag'
        cups_sub = MagicMock()
        cups_sub.rt_device_id = 'rt0'
        cups_sub.subscribers_type = 'cups'
        pgw_sub = MagicMock()
        pgw_sub.rt_device_id = 'rt0'
        pgw_sub.subscribers_type = 'pgw'
        fwa_sub = MagicMock()
        fwa_sub.rt_device_id = 'rt0'
        fwa_sub.subscribers_type = 'fwa'
        builtins.bbe.get_subscriber_handles.return_value = [hag_sub, cups_sub, pgw_sub, fwa_sub]
        self.assertEqual(bbe_rt_init(), None)
        builtins.t.resources = {'rt0': {'system': {'primary': {}}}}
        builtins.t.get_handle.return_value.invoke.return_value = True
        dhcp_sub = MagicMock()
        dhcp_sub.rt_device_id = 'rt0'
        dhcp_sub.subscribers_type = 'dhcp'
        pppoe_sub = MagicMock()
        pppoe_sub.rt_device_id = 'rt0'
        pppoe_sub.subscribers_type = 'pppoe'
        l2tp_sub = MagicMock()
        l2tp_sub.rt_device_id = 'rt0'
        l2tp_sub.subscribers_type = 'l2tp'
        l2bsa_sub = MagicMock()
        l2bsa_sub.rt_device_id = 'rt0'
        l2bsa_sub.subscribers_type = 'l2bsa'
        builtins.bbe.get_subscriber_handles.return_value = [dhcp_sub, pppoe_sub, l2tp_sub, l2bsa_sub]
        self.assertEqual(bbe_rt_init(), None)
        builtins.bbe.get_subscriber_handles.return_value = []
        self.assertEqual(bbe_rt_init(), None)

    def test_create_rt_dhcp_sub(self):
        subs = MagicMock(spec=DHCPSubscribers)
        subs.dhcpv4_gateway = '10.1.1.1'
        subs.dhcpv6_gateway = '1000::1'
        subs.rapid_commit = 1
        subs.dhcpv6_iana_count = 2
        subs.dhcpv6_iapd_count = 2
        subs.mac = '11:22:33:44:55:66'
        subs.family = 'dual'
        subs.mac_step = "00:00:00:00:00:01"
        subs.has_option38 = True
        subs.option38 = DHCPOption(1, 1, 1, 1, 1, 0, 0, 0)
        subs.has_option6 = True
        subs.option6 = 'xx'
        subs.has_option20 = True
        subs.option20 = '1'
        subs.has_softgre = True
        subs.softgre_vlan_id = '1'
        subs.softgre_vlan_id_step = '1'
        subs.softgre_vlan_id_repeat = '1'
        subs.softgre_source = '10.1.1.1'
        subs.softgre_destination = '1.1.1.1'
        subs.softgre_gateway = '10.1.1.2'
        subs.softgre_count = 1
        subs.dhcpv4_gateway_custom = {'start-value': '100.128.0.1',
                                      'step': '0.0.4.0',
                                      'repeat-each-value': '250',
                                      'sequence-length': '4'}
        subs.dhcpv6_gateway_custom = {'start-value': '1000:2000::100:128:0:1',
                                      'step': '0:0:0:0:0:0:4:0',
                                      'repeat-each-value': '250',
                                      'sequence-length': '4'}
        builtins.t.get_handle.return_value.invoke.return_value = {'status': True, 'device_group_handle': 'dgh',
                                                                  'ldra_v4_device_group': 'ldra',
                                                                  'ethernet_handle': 'eth',
                                                                  'dhcpv4_client_handle': 'v4handle',
                                                                  'dhcpv6_client_handle': 'v6',
								  'ldra_handle': 'ldrav6'}
        self.assertEqual(create_rt_dhcp_subscribers('rt0', subs), None)
        for result in [{'status': False}, {'status': True}, {'status': True, 'device_group_handle': 'dg'},
                       {'status': True, 'device_group_handle': 'dg', 'ethernet_handle': 'eth'},
                       {'status': True, 'device_group_handle': 'dg', 'ethernet_handle': 'eth',
                        'dhcpv4_client_handle': 'v4'},
                       {'status': True, 'device_group_handle': 'dg', 'ethernet_handle': 'eth',
                        'dhcpv6_client_handle': 'v6'},
                       {'status': True, 'device_group_handle': 'dg', 'ethernet_handle': 'eth',
                        'dhcpv6_client_handle': 'v6', 'ldra_handle': 'ldrav6'}]:
            try:
                builtins.t.get_handle.return_value.invoke.return_value = result
                create_rt_dhcp_subscribers('rt0', subs)
            except:
                self.assertRaises(BBEDeviceError)

        subs.count = 0
        self.assertEqual(create_rt_dhcp_subscribers('rt0', subs), None)

    def test_create_rt_pppoe_sub(self):
        subs = MagicMock(spec=PPPoESubscribers)
        subs.circuit_id = 'cir'
        subs.circuit_id_start = 1
        subs.circuit_id_step = 1
        subs.circuit_id_repeat = 1
        subs.circuit_id_length = 1
        subs.remote_id = 'cir'
        subs.remote_id_start = 1
        subs.remote_id_step = 1
        subs.remote_id_repeat = 1
        subs.remote_id_length = 1
        subs.mac = '11:22:33:44:55:66'
        subs.family = 'dual'
        subs.mac_step = "00:00:00:00:00:01"
        subs.has_option38 = True
        subs.option38 = DHCPOption(1, 1, 1, 1, 1, 0, 0, 0)
        subs.has_option6 = True
        subs.option6 = 'xx'
        subs.has_option20 = True
        subs.option20 = '1'
        subs.ncp_retry = 1
        subs.essm_count = None
        builtins.t.get_handle.return_value.invoke.return_value = {'status': True, 'device_group_handle': 'dgh',
                                                                  'ldra_v4_device_group': 'ldra',
                                                                  'ethernet_handle': 'eth',
                                                                  'pppox_client_handle': 'v4handle',
                                                                  'dhcpv6_client_handle': 'v6'}
        self.assertEqual(create_rt_pppoe_subscribers('rt0', subs), None)
        for result in [{'status': False}, {'status': True}, {'status': True, 'device_group_handle': 'dg'},
                       {'status': True, 'device_group_handle': 'dg', 'ethernet_handle': 'eth'},
                       {'status': True, 'device_group_handle': 'dg', 'ethernet_handle': 'eth',
                        'pppox_client_handle': 'v4'}]:
            try:
                builtins.t.get_handle.return_value.invoke.return_value = result
                create_rt_pppoe_subscribers('rt0', subs)
            except:
                self.assertRaises(BBEDeviceError)

        subs.count = 0
        self.assertEqual(create_rt_pppoe_subscribers('rt0', subs), None)

    @patch('ipaddress.IPv4Interface')
    def test_add_rt_lns(self, patch_ipaddr):
        builtins.bbe.get_interfaces.return_value = [MagicMock(spec=BBEVarInterface)]
        cons = MagicMock()
        cons.interface_config = {'tun_hello_req': '1', 'tun_hello_interval': '1', 'ip_cp': '1', 'lease-time': '1',
                                 'dhcpv6-ia-type': 'iapd', 'pool-prefix-start': '00', 'pool-prefix-length': '8',
                                 'pool-prefix-size': '100', 'ip': '10.10.10.1', 'l2tp_dst_addr': '1.1.1.1'}
        builtins.bbe.get_connection.return_value = cons

        builtins.t.get_handle.return_value.invoke.return_value = {'status': False}
        try:
            add_rt_lns('rt0')
        except:
            self.assertRaises(BBEDeviceError)

        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1', }
        self.assertEqual(add_rt_lns('rt0'), None)

    def test_create_rt_l2tp_sub(self):
        subs = MagicMock(spec=L2TPSubscribers)

        try:
            builtins.t.get_handle.return_value.invoke.return_value = {'status': '0'}
            create_rt_l2tp_subscribers('rt0', subs)
        except:
            self.assertRaises(BBEDeviceError)
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1', 'lac_handle':'lac',
                                                                  'pppox_client_handle': 'ppp',
                                                                  'dhcpv6_client_handle': 'dhcp',
                                                                  'ethernet_handle': 'eth'}
        self.assertEqual(create_rt_l2tp_subscribers('rt0', subs), None)
        subs.family = 'v4v6dual'
        self.assertEqual(create_rt_l2tp_subscribers('rt0', subs), None)
        subs.num_of_lac = 0
        self.assertEqual(create_rt_l2tp_subscribers('rt0', subs), None)

    def test_create_l2bsa_sub(self):
        subs = MagicMock(spec=L2BSASubscribers)
        subs.ip_addr = '10.1.1.1'
        subs.ip_addr_step = '0.0.0.1'
        subs.gateway = '10.0.0.1'
        subs.gateway_step = '0.0.0.1'
        subs.mac_resolve = '1'
        subs.ipv6_addr = '1000::1'
        subs.ipv6_addr_step = '::1'
        subs.ipv6_gateway = '1000::2'
        subs.ipv6_gateway_step = '::1'

        try:
            builtins.t.get_handle.return_value.invoke.return_value = {'status': '0'}
            create_rt_l2bsa_subscribers('rt0', subs)
        except:
            self.assertRaises(BBEDeviceError)
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        self.assertEqual(create_rt_l2bsa_subscribers('rt0', subs), None)
        subs.count = 0
        self.assertEqual(create_rt_l2bsa_subscribers('rt0', subs), None)

    @patch('jnpr.toby.bbe.bbevar.subscribers.CUPSSubscribers', create=True)
    def test_create_cups_sub(self, patch_subs):
        builtins.t._script_name = 'test'
        builtins.t['resources']['rt0']['system']['primary']['uv-ts-name'] = 'test2'
        patch_subs.traffic_network_host_type = 'local'
        patch_subs.family = 'ipv4'
        patch_subs.sgw_user_address = '10.1.4.1'
        patch_subs.sgw_control_address = '20.1.4.1'
        patch_subs.traffic_start_ip = '30.1.4.1'
        patch_subs.control_interface = 'access0'
        patch_subs.access_interface = 'access0'
        patch_subs.uplink_v6_base_address = 'BEEF:D00D::/64'
        patch_subs.control_v6_base_address = 'FEED:D00D::/64'
        patch_subs.user_v6_base_address = 'C0DE:D00D::/64'
        patch_subs.uplink_base_address = '30.1.4.1/24'
        patch_subs.control_base_address = '20.1.4.1/24'
        patch_subs.user_base_address = '10.1.4.1/24'
        patch_subs.use_loopback = True
        patch_subs.use_static_address = True
        patch_subs.access_vlan_id = '100'
        patch_subs.sgw_control_node_count = '10'

        result1 = {'testSessionHandle': 'ts', 'testServerHandleList': 'list'}
        result2 = True
        result3 = True
        result4_1 = 'name'
        result4_2 = 'name2'
        result4_3 = 'name3'
        result5 = 'testhandle'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]
        self.assertEqual(create_rt_cups_subscribers('rt0', subscriber=patch_subs, test_id=1), None)

        result1 = {'testSessionHandle': 'ts1', 'testServerHandleList': 'list1'}
        result2 = True
        result3 = True
        result4_1 = 'name1'
        result4_2 = 'name2'
        result4_3 = 'name3'
        result5 = 'testhandle1'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]
        # Subnet IP address code paths
        patch_subs.sgw_user_address = '10.1.4.1/24'
        patch_subs.sgw_control_address = '20.1.4.1/24'
        patch_subs.traffic_start_ip = '30.1.4.1/24'
        patch_subs.control_interface = 'control0'
        self.assertEqual(create_rt_cups_subscribers('rt0', subscriber=patch_subs, test_id=2), None)

        # Subscriber missing traffic_start_ip attribute code path
        del patch_subs.traffic_start_ip
        result1 = {'testSessionHandle': 'ts2', 'testServerHandleList': 'list2'}
        result2 = True
        result3 = True
        result4_1 = 'name7'
        result4_2 = 'name8'
        result4_3 = 'name9'
        result5 = 'testhandle77'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]

        self.assertEqual(create_rt_cups_subscribers('rt0', subscriber=patch_subs, test_id=3), None)
        builtins.t.get_handle.return_value.invoke.side_effect = None

    @patch('jnpr.toby.bbe.bbevar.subscribers.PGWSubscribers', create=True)
    def test_create_pgw_sub(self, patch_subs):
        builtins.t._script_name = 'test'
        builtins.t['resources']['rt0']['system']['primary']['uv-ts-name'] = 'test2'
        patch_subs.traffic_network_host_type = 'local'
        patch_subs.family = 'ipv4'
        patch_subs.pgw_user_address = '10.1.4.1'
        patch_subs.pgw_control_address = '20.1.4.1'
        patch_subs.traffic_start_ip = '30.1.4.1'
        patch_subs.control_interface = 'access0'
        patch_subs.access_interface = 'access0'
        patch_subs.uplink_v6_base_address = 'BEEF:D00D::/64'
        patch_subs.control_v6_base_address = 'FEED:D00D::/64'
        patch_subs.user_v6_base_address = 'C0DE:D00D::/64'
        patch_subs.uplink_base_address = '30.1.4.1/24'
        patch_subs.control_base_address = '20.1.4.1/24'
        patch_subs.user_base_address = '10.1.4.1/24'
        patch_subs.use_loopback = True
        patch_subs.use_static_address = True
        patch_subs.access_vlan_id = '100'
        patch_subs.pgw_control_node_count = '10'

        result1 = {'testSessionHandle': 'ts', 'testServerHandleList': 'list'}
        result2 = True
        result3 = True
        result4_1 = 'name'
        result4_2 = 'name2'
        result4_3 = 'name3'
        result5 = 'testhandle'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]
        self.assertEqual(create_rt_pgw_subscribers('rt0', subscriber=patch_subs, test_id=1), None)

        result1 = {'testSessionHandle': 'ts1', 'testServerHandleList': 'list1'}
        result2 = True
        result3 = True
        result4_1 = 'name1'
        result4_2 = 'name2'
        result4_3 = 'name3'
        result5 = 'testhandle1'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]
        # Subnet IP address code paths
        patch_subs.sgw_user_address = '10.1.4.1/24'
        patch_subs.sgw_control_address = '20.1.4.1/24'
        patch_subs.traffic_start_ip = '30.1.4.1/24'
        patch_subs.control_interface = 'control0'
        self.assertEqual(create_rt_pgw_subscribers('rt0', subscriber=patch_subs, test_id=2), None)

        # Subscriber missing traffic_start_ip attribute code path
        del patch_subs.traffic_start_ip
        result1 = {'testSessionHandle': 'ts2', 'testServerHandleList': 'list2'}
        result2 = True
        result3 = True
        result4_1 = 'name7'
        result4_2 = 'name8'
        result4_3 = 'name9'
        result5 = 'testhandle77'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]

        self.assertEqual(create_rt_pgw_subscribers('rt0', subscriber=patch_subs, test_id=3), None)
        builtins.t.get_handle.return_value.invoke.side_effect = None


    @patch('jnpr.toby.bbe.bbevar.subscribers.FWASubscribers', create=True)
    def test_create_fwa_sub(self, patch_subs):
        builtins.t._script_name = 'test'
        patch_subs.traffic_network_host_type = 'local'
        patch_subs.family = 'ipv6'
        patch_subs.sgw_user_address = '40.1.4.1'
        patch_subs.sgw_control_address = '50.1.4.1'
        patch_subs.traffic_start_ip = '60.1.4.1'
        patch_subs.v6_traffic_start_ip = '3000::1/64'

        traffdict1 = {'type': 'udp', 'rate': '10', 'transaction': '100', 'start': 'paused', 'packet_size': '1000',
                      'ttl': 2, 'segment_size': '800', 'initiate_side': '1', 'ratio': '1', 'udp_burst_count': '100',
                      'tos': [0,1], 'client_port': '20', 'server_port': '80', 'role': 'client',
                      'preferred_transport': 'ipv4'}
        traffdict2 = {'type': 'tcp', 'rate': '10', 'transaction': '100', 'start': 'on-event', 'packet_size': '1000',
                      'ttl': 2, 'segment_size': '800', 'initiate_side': '1', 'ratio': '1', 'role': 'client',
                      'tcp_socket_disc_side': '100', 'tcp_3way_handshake': '1', 'tcp_disconnect_type': '1',
                      'tcp_congestion_avoid': '1', 'tcp_window_size': '100', 'tcp_max_segment_size': '800',
                      'tcp_min_header_size': '100', 'tcp_max_packets_before_ack': '1', 'preferred_transport': 'ipv4'}

        patch_subs.traffic_profile = {'traf1': traffdict1, 'traf2': traffdict2}
        result1 = {'testSessionHandle': 'ts', 'testServerHandleList': 'list'}
        result2 = True
        result3 = True
        result4_1 = 'name'
        result4_2 = 'name2'
        result4_3 = 'name3'
        result5 = 'testhandle'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]
        self.assertEqual(create_fwa_subscribers('rt0', subscriber=patch_subs, test_id=1), None)
        builtins.t.get_handle.return_value.invoke.side_effect = None        

        result1 = {'testSessionHandle': 'ts1', 'testServerHandleList': 'list1'}
        result2 = True
        result3 = True
        result4_1 = 'name1'
        result4_2 = 'name2'
        result4_3 = 'name3'
        result5 = 'testhandle1'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]
        patch_subs.sgw_user_address = '40.1.4.1/24'
        patch_subs.sgw_control_address = '50.1.4.1/24'
        patch_subs.traffic_start_ip = '60.1.4.1/24'
        patch_subs.traffic = True
        patch_subs.traffic_dualstack = True
        patch_subs.v6_traffic_start_ip = '4000::1'
        patch_subs.traffic_network_host_type = 'remote'
        self.assertEqual(create_fwa_subscribers('rt0', subscriber=patch_subs, test_id=2), None)

        del patch_subs.traffic_start_ip
        patch_subs.traffic = None
        patch_subs.traffic_dualstack = None
        del patch_subs.traffic_dualstack
        del patch_subs.v6_traffic_start_ip   
        result1 = {'testSessionHandle': 'ts2', 'testServerHandleList': 'list2'}
        result2 = True
        result3 = True
        result4_1 = 'name7'
        result4_2 = 'name8'
        result4_3 = 'name9'
        result5 = 'testhandle77'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]
        self.assertEqual(create_fwa_subscribers('rt0', subscriber=patch_subs, test_id=3), None)

        patch_subs.traffic = True
        patch_subs.traffic_dualstack = True
        result1 = {'testSessionHandle': 'ts2', 'testServerHandleList': 'list2'}
        result2 = True
        result3 = True
        result4_1 = 'name7'
        result4_2 = 'name8'
        result4_3 = 'name9'
        result5 = 'testhandle77'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result2, result2, result2,
                                                                 result3, result4_1, result4_2, result4_3,
                                                                 result5, result5, result6, result7]
        self.assertEqual(create_fwa_subscribers('rt0', subscriber=patch_subs, test_id=3), None)
        builtins.t.get_handle.return_value.invoke.side_effect = None


    @patch('jnpr.toby.bbe.bbevar.subscribers.HAGSubscribers', create=True)
    def test_create_hag_sub(self, patch_subs):
        builtins.t._script_name = 'test'
        patch_subs.traffic_network_host_type = 'local'
        patch_subs.lte_node_ip = '192.168.1.2'
        patch_subs.traffic_start_ip = '192.168.1.1/24'
        patch_subs.v6_traffic_start_ip = '2000::1/64'
        patch_subs.family = 'ipv6'
        traffdict1 = {'type': 'udp', 'rate': '10', 'transaction': '100', 'start': 'paused', 'packet_size': '1000',
                      'ttl': 2, 'segment_size': '800', 'initiate_side': '1', 'ratio': '1', 'udp_burst_count': '100',
                      'tos': [0,1], 'client_port': '20', 'server_port': '80', 'role': 'client',
                      'preferred_transport': 'ipv4'}
        traffdict2 = {'type': 'tcp', 'rate': '10', 'transaction': '100', 'start': 'on-event', 'packet_size': '1000',
                      'ttl': 2, 'segment_size': '800', 'initiate_side': '1', 'ratio': '1', 'role': 'client',
                      'tcp_socket_disc_side': '100', 'tcp_3way_handshake': '1', 'tcp_disconnect_type': '1',
                      'tcp_congestion_avoid': '1', 'tcp_window_size': '100', 'tcp_max_segment_size': '800',
                      'tcp_min_header_size': '100', 'tcp_max_packets_before_ack': '1', 'preferred_transport': 'ipv4'}

        patch_subs.traffic_profile = {'traf1': traffdict1, 'traf2': traffdict2}
        result1 = {'testSessionHandle': 'ts', 'testServerHandleList': 'list'}
        result2 = True
        result3 = True
        result4_1 = 'name'
        result4_2 = 'name2'
        result4_3 = 'name3'
        result5 = 'testhandle'
        result6 = 'validate'
        result7 = True
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result3, result4_1,
                                                                 result4_2, result4_3, result5, result6, result7,
                                                                 result7,result7, result7, result7, result7]
        self.assertEqual(create_rt_hag_subscribers('rt0', subscriber=patch_subs, test_id=1), None)
        builtins.t.get_handle.return_value.invoke.side_effect = None
        patch_subs.lte_node_ip ='2.2.2.2/24'
        patch_subs.dsl_node_ip = '2.2.2.2/24'
        patch_subs.family = 'dual'
        patch_subs.count = 2
        patch_subs.traffic_start_ip = '1.1.1.1/24'
        patch_subs.v6_traffic_start_ip = '1000::1/64'
        builtins.t.get_handle.return_value.invoke.side_effect = [result1, result2, result3, result4_1,
                                                                 result4_2, result4_3, result5, result6, result7,
                                                                 result7, result7, result7, result7, result7]
        self.assertEqual(create_rt_hag_subscribers('rt0', subscriber=patch_subs, test_id=1), None)
        builtins.t.get_handle.return_value.invoke.side_effect = None

    @patch('re.match')
    @patch('ipaddress.IPv6Interface')
    @patch('ipaddress.IPv4Interface')
    def test_add_rt_links(self, patch_v4, patch_v6, patch_re):
        intf1 = MagicMock(spec=BBEVarInterface)
        builtins.bbe.get_interfaces.return_value = [intf1]
        self.assertEqual(add_rt_links('rt0'), None)
        con1 = MagicMock(spec=BBEVarInterface)
        con1.interface_config = None
        con1.interface_id = 'uplink0'
        builtins.bbe.get_connection.return_value = con1
        self.assertEqual(add_rt_links('rt0'), None)
        con1.interface_config = {'test': {}, 'mac': 'xx'}
        con1.vlan_range = None
        con1.svlan_range = None
        intf1.interface_id = 'uplink0'
        self.assertEqual(add_rt_links('rt0'), None)
        builtins.bbe.get_connection.side_effect = Exception()
        try:
            add_rt_links('rt0')
        except:
            self.assertRaises(Exception)
        builtins.bbe.get_connection.side_effect = None
        try:
            builtins.t.get_handle.return_value.invoke.return_value = {'status': '0'}
            add_rt_links('rt0')
        except:
            self.assertRaises(BBEDeviceError)



    def test_add_rt_dhcp_server(self):
        builtins.bbe.get_interfaces.return_value = [MagicMock(spec=BBEVarInterface)]
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1', 'dhcpv4_server_handle': 'v4',
                                                                  'dhcpv6_server_handle': 'v6'}
        self.assertEqual(add_rt_dhcp_servers(rt_device_id='rt0', family='ipv4'), None)
        self.assertEqual(add_rt_dhcp_servers(rt_device_id='rt0', family='ipv6'), None)

    def test_set_subscriber_call_rate(self):
        builtins.bbe.get_subscriber_handles.side_effect = None
        builtins.bbe.get_subscriber_handles.return_value = [MagicMock()]
        self.assertEqual(set_subscribers_call_rate('rt0'), None)

    @patch('ipaddress.IPv4Interface')
    @patch('jnpr.toby.bbe.bbevar.subscribers.DHCPSubscribers', create=True)
    def test_create_ancp_node(self, patch_dhcp, patch_ipaddv4):
        #sub0 = MagicMock(spec=DHCPSubscribers)
        patch_dhcp.subscribers_type = 'dhcp'
        try:
            builtins.t.get_handle.return_value.invoke.return_value = {'status': '0'}
            create_ancp_node('rt0', subscriber=patch_dhcp)
        except:
            self.assertRaises(BBEDeviceError)
        patch_dhcp.subscribers_type = 'pppoe'
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1', 'ancp_handle': 'ancp',
                                                                  'ancp_subscriber_lines_handle': 'line'}
        self.assertEqual(create_ancp_node('rt0', subscriber=patch_dhcp), None)

    @patch('jnpr.toby.bbe.bbevar.subscribers.DHCPSubscribers', create=True)
    def test_add_mcast_client(self, patch_dhcp):
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1', 'igmp_host_handle': 'h1',
                                                                  'igmp_group_handle': 'h2', 'igmp_source_handle': 'h3',
                                                                  'mld_host_handle': 'h1', 'mld_group_handle': 'h2',
                                                                  'mld_source_handle': 'h3'}
        self.assertEqual(add_mcast_client('rt0', patch_dhcp), None)
        for status in [False, True]:
            patch_dhcp.has_igmp = status
            builtins.t.get_handle.return_value.invoke.return_value = {'status': '0'}
            try:
                add_mcast_client('rt0', patch_dhcp)
            except:
                self.assertRaises(BBEDeviceError)

    @patch('re.match')
    def test_add_rt_ae(self, patch_re):
        builtins.bbe.get_interfaces.return_value = [MagicMock(spec=BBEVarInterface)]


        self.assertEqual(add_rt_ae('rt0'), None)
        builtins.bbe.get_interfaces.return_value = [MagicMock(spec=BBEVarInterface), MagicMock(spec=BBEVarInterface)]
        intf1 = MagicMock(spec=BBEVarInterface)
        intf1.is_ae_active = True
        intf1.ae_bundle = 'ae0'
        intf2 = MagicMock(spec=BBEVarInterface)
        intf2.is_ae_active = False
        intf2.ae_bundle = 'ae0'
        builtins.bbe.get_connection.side_effect = [intf1, intf2]
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '0', 'lacp_handle': 'lacp'}
        try:
            add_rt_ae('rt0')
        except:
            self.assertRaises(BBEDeviceError)
        builtins.bbe.get_connection.side_effect = [intf1, intf2]
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1', 'lacp_handle': 'lacp'}
        self.assertEqual(add_rt_ae('rt0'), None)
        builtins.bbe.get_connection.side_effect = [intf1, intf2]
        try:
            patch_re.return_value = ''
            add_rt_ae('rt0')
        except:
            self.assertRaises(Exception)
        builtins.bbe.get_connection.side_effect = None

    def test_add_rt_bgp(self):
        builtins.bbe.get_interfaces.return_value = [MagicMock(spec=BBEVarInterface), MagicMock(spec=BBEVarInterface)]
        intf1 = MagicMock(spec=BBEVarInterface)
        intf1.vlan_range = VlanRange(1,1,1,1)

        intf1.interface_config = {'bgp': {'neighbors': [{'remote-ip': '10.1.1.2', 'local-ip': '10.1.1.1',
                                                         'type':'ebgp', 'remote-as': '1',
                                                         'prefix': '200.0.0.0/8'}], 'local-as': '2'}, 'ip': '10.1.1.1'}
        intf2 = MagicMock(spec=BBEVarInterface)
        intf2.vlan_range = VlanRange(1, 1, 1, 1)
        builtins.bbe.get_connection.side_effect = [intf1, intf2]
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '0'}
        try:
            add_rt_bgp_neighbor('rt0')
        except:
            self.assertRaises(BBEDeviceError)
        intf1.interface_config['bgp']['neighbors'][0]['remote-ip'] = '10.1.1.3'
        builtins.bbe.get_connection.side_effect = [intf1, intf2]
        try:
            add_rt_bgp_neighbor('rt0')
        except:
            self.assertRaises(BBEDeviceError)

        builtins.bbe.get_connection.side_effect = [intf1, intf2]
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1', 'ipv4_handle': '4', 'ipv6_handle': '6'}

        intf1.interface_config = {'bgp': {'neighbors': [{'remote-ip': '10.1.1.3', 'local-ip': '10.1.1.2',
                                                         'keepalive': '1', 'holdtime': '30', 'restart_time': '50',
                                                         'type': 'ebgp', 'remote-as': '1', 'enable_flap': '1',
                                                         'flap_up_time': '1', 'flap_down_time': '2',
                                                         'stale_time': '20', 'graceful_restart': '1',
                                                         'prefix': '200.0.0.0/8'}], 'local-as': '2'}, 'ip': '10.1.1.1'}
        intf2.interface_config = {'bgp+': {'neighbors': [{'remote-ip': '1000::3', 'local-ip': '1000::2',
                                                         'keepalive': '1', 'holdtime': '30', 'restart_time': '50',
                                                         'type': 'ebgp', 'remote-as': '1', 'enable_flap': '1',
                                                         'flap_up_time': '1', 'flap_down_time': '2',
                                                         'stale_time': '20', 'graceful_restart': '1',
                                                         'prefix': '2000::/64'}], 'local-as': '2'}, 'ipv6': '1000::1'}
        builtins.bbe.get_connection.side_effect = [intf1, intf2]
        self.assertEqual(add_rt_bgp_neighbor('rt0'), None)
        builtins.bbe.get_connection.side_effect = [intf1, intf2]
        intf1.interface_config = None
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '0'}
        try:
            add_rt_bgp_neighbor('rt0')
        except:
            self.assertRaises(BBEDeviceError)
        intf2.interface_config['bgp+']['neighbors'][0]['remote-ip'] = '1000::2'
        builtins.bbe.get_connection.side_effect = [intf1, intf2]
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '0'}
        try:
            add_rt_bgp_neighbor('rt0')
        except:
            self.assertRaises(BBEDeviceError)

        builtins.bbe.get_connection.side_effect = None

    def test_add_rt_isis_l3(self):
        builtins.bbe.get_interfaces.return_value = [MagicMock(spec=BBEVarInterface)]
        intf1 = MagicMock(spec=BBEVarInterface)
        intf1.vlan_range = VlanRange(1,1,1,1)

        intf1.interface_config = {'isis': {'auth_type': 'md5', 'auth_key': 'joshua', 'intf_type': 'ptop',
                                           'prefix': {'multiplier': 2,
                                                      'prefix_type': 'ipv4-prefix',
                                                      'ipv4_prefix_network_address': '101.1.0.0',
                                                      'ipv4_prefix_network_address_step': '1.0.0.0',
                                                      'ipv4_prefix_length': '24',
                                                      'ipv4_prefix_address_step': '1',
                                                      'ipv4_prefix_number_of_addresses': '2000'}}}

        builtins.bbe.get_connection.side_effect = [intf1]
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '0'}
        try:
            add_rt_isis_l3('rt0')
        except:
            self.assertRaises(BBEDeviceError)

        intf1.interface_config = {'isis': {'auth_type': 'md5', 'auth_key': 'joshua', 'intf_type': 'ptop',
                                           'prefix': {'multiplier': 2,
                                                      'prefix_type': 'ipv4-prefix',
                                                      'ipv4_prefix_network_address': '101.1.0.0',
                                                      'ipv4_prefix_network_address_step': '1.0.0.0',
                                                      'ipv4_prefix_length': '24',
                                                      'ipv4_prefix_address_step': '1',
                                                      'ipv4_prefix_number_of_addresses': '2000'}}}
        builtins.t.get_handle.return_value.invoke.return_value = {'status': '1'}
        builtins.bbe.get_connection.side_effect = [intf1]
        self.assertEqual(add_rt_bgp_neighbor('rt0'), None)

        builtins.bbe.get_connection.side_effect = None


if __name__ == '__main__':
    unittest.main()
