import unittest
import builtins
from mock import patch, MagicMock
import jnpr.toby.trafficgen.ixia.ixiatester as tester
from jnpr.toby.bbe.bbevar.bbevars import BBEVars, BBEVarInterface
from jnpr.toby.init.init import init

builtins.t = MagicMock()
builtins.t = MagicMock(spec=init)
builtins.t.log = MagicMock()
builtins.bbe = MagicMock(spec=BBEVars)
rthandle = MagicMock()


class TestIxiaTester(unittest.TestCase):
    """
    TestIxiaTester class to handle ixiatester.py unit tests
    """
    def test_add_string_mv(self):
        rthandle.invoke.return_value = {'status': '1'}
        self.assertIsInstance(tester.add_string_mv(rthandle, string_name='test'), dict)

    def test_reboot_port(self):
        rthandle.invoke.return_value = {'status': '1'}
        self.assertIsInstance(tester.reboot_port(rthandle, port_list='1/1'), dict)
        rthandle.invoke.return_value = {'status': '0'}
        self.assertIsInstance(tester.reboot_port(rthandle, port_list='1/1'), dict)

    def test_bbe_initialize(self):
        self.assertEqual(tester.bbe_initialize(rthandle), None)

    def test_add_tobopogy(self):
        try:
            tester.add_topology(rthandle, port_list='1/0')
        except Exception as err:
            self.assertEqual(err.args[0], 'port_list argument should be a list')
        rthandle.invoke.return_value = {'status': '1', 'topology_handle': 'h1'}
        self.assertIsInstance(tester.add_topology(rthandle, port_list=['1', '2', 'lag']), dict)

    def test_set_protocol_stacking_mode(self):
        rthandle.invoke.return_value = {'status': '1'}
        self.assertIsInstance(tester.set_protocol_stacking_mode(rthandle, mode='test'), dict)

    def test_set_custom_pattern(self):
        result1 = {'multivalue_handle': 'h1'}
        result2 = {'custom_handle': 'h2'}
        result3 = {'increment_handle': 'h3'}
        result4 = {'status': '1'}
        rthandle.invoke.side_effect = [result1, result2, result3, result4]
        self.assertIsInstance(tester._set_custom_pattern(rthandle, start=1, step=2, repeat=3, count=4), str)
        rthandle.invoke.side_effect = Exception()
        try:
            tester._set_custom_pattern(rthandle, start=1, step=2)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create custom pattern')
        rthandle.invoke.side_effect = None

    def test_add_type_tlv(self):
        rthandle.invoke.return_value = {'status': '1'}
        self.assertIsInstance(tester.add_type_tlv(rthandle, handle='h1',
                                                  tlv_name='test', tlv_include_in_messages='1'), dict)

    def test_add_code_tlv(self):
        rthandle.invoke.return_value = {'status': '1'}
        self.assertIsInstance(tester.add_code_tlv(rthandle, type_handle='type', field_value='field'), dict)

    def test_add_field_tlv(self):
        rthandle.invoke.return_value = {'status': '1'}
        self.assertIsInstance(tester.add_field_tlv(rthandle, value_handle='1',
                                                   field_name='field', field_value='1'), dict)

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_code_tlv', return_value={'status': '1'})
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_field_tlv')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_type_tlv')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_string_mv', return_value={'multivalue_handle': 'h1'})
    def test_set_v6_option(self, patch_string_mv, patch_type, patch_field, patch_code):
        patch_type.return_value = {'status': '1', 'tlv_value_handle': '2', 'tlv_type_handle': '3'}
        patch_field.return_value = {'status': '1'}
        rthandle.invoke.return_value = {'status': '1', 'multivalue_handle': 'h2'}
        test_args = {'handle': 'relayAgent', 'interface_id': 'id', 'enterprise_id':'enid', 'interface_id_start': '1',
                     'v6_remote_id': 'v6', 'v6_remote_id_start': '1', 'subscriber_id': 'sid',
                     'subscriber_id_start': '1'}
        self.assertIsInstance(tester.set_v6_option(rthandle, **test_args), dict)
        test_args = {'handle': 'relayAgent', 'interface_id': 'id?', 'enterprise_id': 'enid?', 'interface_id_start': '1',
                     'v6_remote_id': 'v6?', 'v6_remote_id_start': '1', 'subscriber_id': 'sid?',
                     'subscriber_id_start': '1'}
        self.assertIsInstance(tester.set_v6_option(rthandle, **test_args), dict)
        test_args = {'handle': 'h0', 'option_req': '1', 'option20': '1'}
        self.assertIsInstance(tester.set_v6_option(rthandle, **test_args), dict)
        patch_field.return_value = {'status': '0'}
        test_args = {'handle': 'h0', 'option_req': ['1']}
        self.assertIsInstance(tester.set_v6_option(rthandle, **test_args), dict)
        test_args = {'handle': 'h0', 'option20': '1'}
        patch_type.return_value = {'status': '0'}
        self.assertIsInstance(tester.set_v6_option(rthandle, **test_args), dict)
        test_args = {'handle': 'h0', 'option_req': '1'}
        self.assertIsInstance(tester.set_v6_option(rthandle, **test_args), dict)

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_string_mv', return_value={'multivalue_handle': 'h1'})
    def test_set_option82(self, patch_string_mv):
        rthandle.invoke.return_value = {'status': '1', 'tlv_value_handle': 'h2',
                                        'tlv_type_handle': 'h3', 'tlv_field_handle': 'h4'}
        rthandle.circuit_id = {}
        rthandle.remote_id = {}
        test_args = {'handle': 'v4', 'circuit_id': 'id', 'circuit_id_start': '1',
                     'remote_id': 'remo', 'remote_id_start': '1'}
        self.assertIsInstance(tester.set_option_82(rthandle, **test_args), dict)
        self.assertIsInstance(tester.set_option_82(rthandle, **test_args), dict)
        test_args['circuit_id'] = 'id?'
        test_args['remote_id'] = 'remo?'
        rthandle.invoke.return_value['status'] = '0'
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to modify option82 circuitid')
        rthandle.circuit_id.pop('v4')
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to modify option82 remote id ')

        rthandle.circuit_id = {}
        rthandle.remote_id = {}
        test_args = {'handle': 'v4', 'circuit_id': 'id', 'circuit_id_start': '1',
                     'remote_id': 'remo', 'remote_id_start': '1'}
        rthandle.invoke.return_value['status'] = '0'
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create option82 tlv')
        result1 = {'status': '1', 'tlv_value_handle': 'h2', 'tlv_type_handle': 'h3', 'tlv_field_handle': 'h4'}
        result2 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2]
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create option82 tlv type field')

        rthandle.invoke.side_effect = [result1, result1, result2]
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create option82 circuitid tlv')
        rthandle.invoke.side_effect = [result1, result1, result1, result2]
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create option82 circuitid field')

        rthandle.invoke.side_effect = [result1, result1, result1, result1, result2]
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create option82 tlv circuitid type field')

        test_args.pop('circuit_id')
        rthandle.circuit_id = {}
        rthandle.remote_id = {}
        rthandle.invoke.side_effect = [result1, result1, result2]
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create option82 remoteid tlv')
        rthandle.invoke.side_effect = [result1, result1, result1, result2]
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create option82 remote id field')

        rthandle.invoke.side_effect = [result1, result1, result1, result1, result2]
        try:
            tester.set_option_82(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create option82 remote id type field')

        rthandle.invoke.side_effect = None

    @patch('jnpr.toby.trafficgen.ixia.ixiatester._set_custom_pattern', return_value={'result' : '1'})
    def test_set_vlan(self, patch_pattern):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'ethernet', 'mac': '11:22:33:44:55:66', 'vlan_start': '1', 'svlan_start': '1',\
                     'mac_step': '1', 'vlan_priority': '1', 'vlan_priority_step': '1', 'vlan_user_priority_step': '1',\
                     'svlan_priority': '1', 'svlan_priority_step': '1'}
        self.assertIsInstance(tester.set_vlan(rthandle, **test_args), dict)
        test_args.pop('handle')
        try:
            tester.set_vlan(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'handle is mandatory')

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_topology', return_value={'status': '1'})
    def test_add_device_group(self, patch_topo):
        rthandle.invoke.return_value = {'status': '1', 'device_group_handle': 'd1'}

        test_args = {'port_handle': 'p1', 'device_count': '2', 'name': 'n1'}
        self.assertIsInstance(tester.add_device_group(rthandle, **test_args), dict)
        rthandle.handles = {'h1': {'topo': 't1', 'device_group_handle': ['d1']}}
        test_args.pop('port_handle')
        test_args['topology_handle'] = 't1'
        self.assertIsInstance(tester.add_device_group(rthandle, **test_args), dict)
        test_args.pop('topology_handle')
        test_args['device_group_handle'] = 'd1'
        self.assertIsInstance(tester.add_device_group(rthandle, **test_args), dict)
        rthandle.invoke.return_value = {'status': '0'}
        try:
            tester.add_device_group(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to create device group ')

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.set_vlan')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_device_group')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_topology', return_value={'status': '1', 'topology_handle': 't1'})
    def test_add_ldra(self, patch_topo, patch_device, patch_vlan):
        rthandle.invoke.return_value = {'status': '1', 'dhcpv6relayagent_handle': 'd1'}
        rthandle.handles = MagicMock()
        patch_device.return_value = {'status': '1', 'device_group_handle': 'd1'}
        patch_vlan.return_value = {'status': '1', 'ethernet_handle': 'e1'}
        test_args = {'port': 'p1'}
        self.assertIsInstance(tester.add_ldra(rthandle, **test_args), dict)
        rthandle.handles = {'p1': {'topo': 't1', 'device_group_handle':['h1']}}

        rthandle.ae = False
        self.assertIsInstance(tester.add_ldra(rthandle, **test_args), dict)
        patch_device.return_value['status'] = '0'
        try:
            tester.add_ldra(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add device group for ldra')
        patch_device.return_value['status'] = '1'
        patch_vlan.return_value['status'] = '0'
        try:
            tester.add_ldra(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add ethernet for ldra')
        rthandle.invoke.return_value['status'] = '0'
        patch_vlan.return_value['status'] = '1'
        try:
            tester.add_ldra(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add lightweight dhcpv6relayagent for ldra')

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.set_v6_option')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.set_option_82', return_value=True)
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.set_vlan')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_ldra')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_device_group')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_link',
           return_value={'device_group_handle': 'd1', 'gre_handle': 'g1'})
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_topology', return_value={'status': '1', 'topology_handle': 't1'})
    def test_add_dhcp_client(self, patch_topo, patch_link, patch_device, patch_ldra, patch_vlan, patch_82, patch_v6):
        rthandle.invoke.return_value = {'status': '1', 'device_group_handle': 'dg3', 'dhcpv4client_handle': 'v4',
                                        'dhcpv6client_handle': 'v6'}
        rthandle.handles = MagicMock()
        patch_device.return_value = {'status': '1', 'device_group_handle': 'dg2', 'ethernet_handle': 'eth1'}
        patch_ldra.return_value = {'status': '1', 'ldra_handle': 'ld1', 'device_group_handle': 'dg1'}
        patch_vlan.return_value = {'status': '1', 'ethernet_handle': 'eth2'}
        test_args = {'port': 'p1', 'ip_type': 'dual', 'interface_id': 'id1', 'gre_vlan_id': '1',
                     'gre_netmask': '24', 'gre_tunnel_count': '1', 'dhcpv6_ia_type': 'iapd', 'dhcpv6_gateway': '1000::1',
                     'dhcpv4_gateway': '100.0.0.1', 'rapid_commit': '1', 'dhcp4_broadcast': '1', 'circuit_id': '2'}
        self.assertIsInstance(tester.add_dhcp_client(rthandle, **test_args), dict)

        gw_custom_args = dict(test_args)
        gw_custom_args.update({'dhcpv6_gateway_custom': MagicMock(), 'dhcpv4_gateway_custom': MagicMock()})
        rthandle.invoke.return_value['multivalue_handle'] = MagicMock()
        rthandle.invoke.return_value['custom_handle'] = MagicMock()
        rthandle.invoke.return_value['increment_handle'] = MagicMock()
        self.assertIsInstance(tester.add_dhcp_client(rthandle, **gw_custom_args), dict)

        rthandle.handles = {'p1': {'dhcpv4_client_handle': [], 'dhcpv6_client_handle': [], 'topo': 't2'}}
        test_args2 = {'softgre': True, 'gre_local_ip': '1.1.1.1', 'gre_gateway': '1.1.1.2', 'gre_dst_ip': '2.2.2.2',
                      'num_sessions': 1}

        test_args['ip_type'] = 'ipv4'
        #new_args = {**test_args, **test_args2}
        test_args2.update(test_args)
        new_args = test_args2
        self.assertIsInstance(tester.add_dhcp_client(rthandle, **new_args), dict)
        test_args['ip_type'] = 'dual'
        patch_82.return_value = False
        try:
            tester.add_dhcp_client(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add dhcp client for v4 users when in LDRA dual mode')
        patch_82.return_value = True
        patch_ldra.return_value['status'] = '0'
        try:
            tester.add_dhcp_client(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add ldra device')
        rthandle.ae = {'p1': 'ae0'}
        rthandle.handles = {'p1': {'device_group_handle': ['d1'], 'topo': 't1', 'dhcpv4_client_handle': [],
                                   'dhcpv6_client_handle': []}}
        test_args['ip_type'] = 'ipv4'
        patch_device.return_value['status'] = '0'
        try:
            tester.add_dhcp_client(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to create device group for port handle' in err.args[0])
        patch_device.return_value['status'] = '1'
        patch_vlan.return_value['status'] = '0'
        try:
            tester.add_dhcp_client(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to create ethernet for device group' in err.args[0])

        patch_vlan.return_value['status'] = '1'

        test_args['num_sessions'] = '5'
        test_args['mac'] = '11:22:33:44:55:66'
        test_args['ip_type'] = 'dual'
        test_args.pop('circuit_id')
        test_args.pop('interface_id')
        self.assertIsInstance(tester.add_dhcp_client(rthandle, **test_args), dict)
        test_args.pop('port')
        test_args['handle'] = 'h1'
        rthandle.invoke.return_value['status'] = '0'
        try:
            tester.add_dhcp_client(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add dhcp client')
        result1 = {'status': '1', 'dhcpv4_client_handle': 'v4'}
        result2 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2]
        try:
            tester.add_dhcp_client(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add dhcpv6 client for dual stack')

        rthandle.invoke.side_effect = None

        test_args['ip_type'] = 'ipv4'
        rthandle.invoke.return_value['status'] = '0'
        try:
            tester.add_dhcp_client(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add dhcp client')

        test_args['ip_type'] = 'ipv6'
        rthandle.invoke.return_value['status'] = '0'
        try:
            tester.add_dhcp_client(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add dhcpv6 client')

        test_args.pop('ip_type')
        try:
            tester.add_dhcp_client(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add dhcp client')

        test_args['option20'] = '1'
        test_args['port'] = 'p1'
        test_args.pop('handle')
        test_args['ip_type'] = 'ipv6'
        rthandle.invoke.return_value['status'] = '1'
        self.assertIsInstance(tester.add_dhcp_client(rthandle, **test_args), dict)

    @patch('jnpr.toby.trafficgen.ixia.ixiatester._add_rate_multivalue', return_value='h1')
    def test_set_dhcp_rate(self, patch_rate):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'v4v6h1', 'login_rate': [20, 30], 'logout_rate': [20, 30], 'outstanding': 200,
                     'msg_timeout': '1', 'retry_count': 2, 'dhcpv6_sol_retries': 2, 'dhcpv6_sol_timeout': 30}
        self.assertIsInstance(tester.set_dhcp_rate(rthandle, **test_args), dict)
        test_args.pop('handle')
        try:
            tester.set_dhcp_rate(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'dhcp handle or type  must be provided')


    def test_add_rate_multivalue(self):
        rthandle.invoke.return_value = {'status': '1', 'multivalue_handle': 'm1'}
        listitem = '1'
        try:
            tester._add_rate_multivalue(rthandle, listitem)
        except Exception as err:
            self.assertEqual(err.args[0], 'login rate must be a list')
        listitem = ['1', '2']
        self.assertEqual(tester._add_rate_multivalue(rthandle, listitem), 'm1')
        rthandle.invoke.return_value = {'status': '0'}
        try:
            tester._add_rate_multivalue(rthandle, listitem)
        except Exception as err:
            self.assertTrue('failed to create multivalue handle for listitem' in err.args[0])

    def test_dhcp_client_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        for action in ['start', 'restart', 'stop']:
            test_args = {'handle': 'h1', 'action': action}
            self.assertIsInstance(tester.dhcp_client_action(rthandle, **test_args), dict)
        test_args.pop('handle')
        self.assertIsInstance(tester.dhcp_client_action(rthandle, **test_args), dict)

    def test_dhcp_client_stats(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'h1', 'mode': 'session'}
        self.assertIsInstance(tester.dhcp_client_stats(rthandle, **test_args), dict)

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_string_mv')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.set_vlan')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_device_group')
    #@patch('jnpr.toby.trafficgen.ixia.ixiatester.add_topology', return_value={'status': '1'})
    def test_add_pppoe_client(self, patch_device, patch_vlan, patch_string):
        #rthandle.handles = MagicMock()
        rthandle.handles = {'p1': {'pppox_client_handle': [], 'topo': 'to1', 'dhcpv6_over_pppox_handle': {'h1': ''}}}
        rthandle.invoke.return_value = {'status': '1', 'pppox_client_handle': 'pppoe', 'dhcpv6_client_handle': 'v6',
                                        'topology_handle': 'to1'}
        patch_vlan.return_value = {'status': '1', 'ethernet_handle': 'eth'}
        patch_device.return_value = {'status': '1', 'device_group_handle': 'dg1'}
        patch_string.return_value = {'multivalue_handle': 'm1'}
        test_args = {'port': 'p1', 'num_sessions': '2', 'vlan_start': '1', 'auth_req_timeout': '2',
                     'echo_req': '1', 'echo_rsp': '1', 'ip_type': 'v4_v6_dual', 'dhcpv6_ia_type': 'iapd',
                     'ipcp_req_timeout': 20, 'max_auth_req': 3, 'max_padi_req': 1, 'max_padr_req': 1,
                     'max_ipcp_retry': '1', 'max_terminate_req': 1, 'echo_req_interval': 1, 'auth_mode': 'pap_chap',
                     'username': 'tst?', 'password': 'tst', 'circuit_id': 'c1?', 'circuit_id_start': 1,
                     'circuit_id_step': 1, 'circuit_id_repeat': 1, 'circuit_id_length': 1, 'remote_id': 'rem?',
                     'remote_id_start': 1, 'remote_id_step': 1, 'remote_id_repeat': 1, 'remote_id_length': 1}
        self.assertIsInstance(tester.add_pppoe_client(rthandle, **test_args), dict)
        test_args['circuit_id'] = 'c1'
        test_args['remote_id'] = 'rem1'
        self.assertIsInstance(tester.add_pppoe_client(rthandle, **test_args), dict)
        test_args.pop('circuit_id_start')
        test_args.pop('remote_id_start')
        test_args.pop('port')
        test_args['handle'] = 'h1'
        self.assertIsInstance(tester.add_pppoe_client(rthandle, **test_args), dict)
        rthandle.handles = {}
        test_args.pop('handle')
        test_args['port'] = 'p1'
        try:
            patch_device.return_value['status'] = '0'
            tester.add_pppoe_client(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to create device group for port handle' in err.args[0])
        rthandle.handles = MagicMock()
        rthandle.ae = {'p1': {}}
        patch_device.return_value['status'] = '1'
        try:
            patch_vlan.return_value['status'] = '0'
            tester.add_pppoe_client(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to create ethernet for device group' in err.args[0])

        patch_vlan.return_value['status'] = '1'
        try:
            rthandle.invoke.return_value['status'] = '0'
            tester.add_pppoe_client(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to add/modify pppoe client for port' in err.args[0])

    @patch('jnpr.toby.trafficgen.ixia.ixiatester._add_rate_multivalue')
    def test_set_pppoe_rate(self, patch_rate):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'login_rate': 10, 'logout_rate': 20, 'outstanding': 10}
        self.assertIsInstance(tester.set_pppoe_rate(rthandle, **test_args), dict)
        test_args.pop('login_rate')
        test_args.pop('logout_rate')
        self.assertIsInstance(tester.set_pppoe_rate(rthandle, **test_args), dict)


    def test_pppoe_client_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'pppoxclient:1', 'action': 'start'}
        self.assertIsInstance(tester.pppoe_client_action(rthandle, **test_args), dict)
        test_args['action'] = 'restart'
        self.assertIsInstance(tester.pppoe_client_action(rthandle, **test_args), dict)
        test_args['action'] = 'stop'
        self.assertIsInstance(tester.pppoe_client_action(rthandle, **test_args), dict)
        test_args.pop('action')
        self.assertIsInstance(tester.pppoe_client_action(rthandle, **test_args), dict)

    def test_pppoe_client_stats(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'h1', 'mode': 'session'}
        self.assertIsInstance(tester.pppoe_client_stats(rthandle, **test_args), dict)

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.set_vlan')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_device_group')
    def test_add_link(self, patch_device, patch_vlan):

        rthandle.invoke.return_value = {'status': '1', 'greoipv4_handle': 'gre', 'ipv4_handle': 'v4',
                                        'ipv6_handle': 'v6', 'topology_handle': 'to1'}
        patch_vlan.return_value = {'status': '1', 'ethernet_handle': 'eth'}
        patch_device.return_value = {'status': '1', 'device_group_handle': 'dg1'}
        test_args = {'port': 'p2', 'name': 'test', 'ip_addr': '10.1.1.2', 'gateway': '10.1.1.1',
                     'gateway_step': '0.0.0.1', 'netmask': '24', 'mac_resolve': True,
                     'gateway_mac': '11:22:33:44:55:66', 'ipv6_addr': '2000::2', 'ipv6_gateway': '2000::1',
                     'ipv6_gateway_step': '::1', 'ipv6_prefix_length': '64', 'gre_dst_ip': '100.0.0.3',
                     'gre_dst_ip_step': '0.0.0.1', 'ip_addr_step': '0.0.0.1'}
        self.assertIsInstance(tester.add_link(rthandle, **test_args), dict)
        test_args.pop('port')
        try:
            tester.add_link(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'port is mandatory when adding link device')
        test_args['port'] = 'p2'
        rthandle.ae = {'p2': {}}
        self.assertIsInstance(tester.add_link(rthandle, **test_args), dict)
        try:
            patch_device.return_value['status'] = '0'
            tester.add_link(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to add device group for port' in err.args[0])
        patch_device.return_value['status'] = '1'
        patch_vlan.return_value['status'] = '0'
        try:
            tester.add_link(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to add ethernet/vlan for device group' in err.args[0])

        patch_vlan.return_value['status'] = '1'
        try:
            rthandle.invoke.return_value['status'] = '0'
            tester.add_link(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to add ip/ipv6 address for ethernet' in err.args[0])
        rthandle.handles = {'p1': {'topo': 't1', 'device_group_handle': [], 'ethernet_handle': [],
                                   'ipv4_handle': [], 'ipv6_handle': []}}
        test_args['port'] = 'p1'
        result1 = {'status': '1', 'greoipv4_handle': 'gre', 'ipv4_handle': 'v4',
                   'ipv6_handle': 'v6', 'topology_handle': 'to1'}
        result2 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2]
        try:
            tester.add_link(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to add gre destination address for ip handle' in err.args[0])
        rthandle.invoke.side_effect = None

    def test_remove_link(self):
        rthandle.device_group_handle = ['h1']
        rthandle.invoke.return_value = {'status': '1'}
        self.assertIsInstance(tester.remove_link(rthandle, device_handle='h1'), dict)

    def test_link_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'h1', 'action': 'start_stop_abort'}
        self.assertIsInstance(tester.link_action(rthandle, **test_args), dict)

    def test_add_traffic(self):
        rthandle.invoke.return_value = {'status': '1', 'stream_id': 's1', 'traffic_item': 'tr1'}
        test_args = {'l3_length': '1', 'transmit_mode': 'burst', 'burst_rate': '100', 'pkts_per_burst': '100',
                     'frame_size': '1000', 'convert_to_raw': '1', 'name': 't1', 'source': 'v6',
                     'destination': 'v6', 'rate': '10mbpspps%', 'packets_count': 10, 'duration': '20',
                     'stream_id': 's1', 'type': 'v6', 'multicast': 'm1', 'dynamic_update': '1',
                     'ip_precedence': '8', 'ip_precedence_mode': 'tos', 'ip_precedence_step': '8',
                     'ip_precedence_count': '4', 'ip_dscp': '24', 'ip_dscp_mode': 'dscp', 'ip_dscp_step': '8',
                     'ip_dscp_count': '8', 'egress_tracking': '1', 'ipv6_traffic_class': '16',
                     'ipv6_traffic_class_step': '8', 'traffic_generate': '1', 'tcp_dst_port': '23',
                     'tcp_src_port': '22', 'tcp_dst_port_step': '2', 'tcp_dst_port_count': '2',
                     'tcp_src_port_step': '2', 'tcp_src_port_count': '2', 'udp_dst_port': '22', 'udp_src_port': '22',
                     'udp_dst_port_step': '8', 'udp_dst_port_count': '2', 'udp_src_port_step': '2',
                     'udp_src_port_count': '3', 'ipv6_traffic_class_count': '2'}
        self.assertIsInstance(tester.add_traffic(rthandle, **test_args), dict)
        test_args.pop('source')
        test_args.pop('destination')
        test_args.pop('burst_rate')
        test_args['frame_size'] = ['10', '20', '30']
        self.assertIsInstance(tester.add_traffic(rthandle, **test_args), dict)
        test_args.pop('multicast')
        test_args.pop('stream_id')
        test_args['type'] = 'v4'
        test_args['frame_size'] = ['10', '20']
        self.assertIsInstance(tester.add_traffic(rthandle, **test_args), dict)
        test_args['type'] = 'v6'
        test_args.pop('rate')
        test_args.pop('frame_size')
        test_args.pop('l3_length')
        self.assertIsInstance(tester.add_traffic(rthandle, **test_args), dict)
        test_args['source'] = 'v4'
        test_args['destination'] = 'v4'
        test_args['scalable_src'] = '1'
        test_args['scalable_dst'] = '1'
        self.assertIsInstance(tester.add_traffic(rthandle, **test_args), dict)

    def test_set_traffic(self):
        rthandle.invoke.return_value = {'status': '1', 'stream_id': 's1', 'traffic_item': 'tr1'}
        test_args = {}
        self.assertIsInstance(tester.set_traffic(rthandle, **test_args), dict)
        test_args['stream_id'] = 'tf1'
        self.assertIsInstance(tester.set_traffic(rthandle, **test_args), dict)

    def test_get_traffic_stats(self):
        rthandle.invoke.return_value = {'status': '1', 'stream_id': 's1', 'traffic_item': 'tr1'}
        test_args = {'mode': 'summary'}
        self.assertIsInstance(tester.get_traffic_stats(rthandle, **test_args), dict)

    def test_get_protocol_stats(self):
        rthandle.invoke.return_value = {'status': '1', 'stream_id': 's1', 'traffic_item': 'tr1'}
        test_args = {'mode': 'summary'}
        self.assertIsInstance(tester.get_protocol_stats(rthandle, **test_args), dict)

    def test_traffic_action(self):
        rthandle.invoke.return_value = {'status': '1', 'stream_id': 's1', 'traffic_item': 'tr1'}
        rthandle.traffic_item = ['t1']
        test_args = {'timeout': '10', 'handle': 't1', 'type': 'l23',
                     'action': 'start_stop_poll_clearstats_reset_regenerate_apply_delete', 'duration': '20'}
        self.assertIsInstance(tester.traffic_action(rthandle, **test_args), dict)
        test_args.pop('handle')
        self.assertIsInstance(tester.traffic_action(rthandle, **test_args), dict)

    def test_start_all(self):
        rthandle.invoke.return_value = {'status': '1'}
        self.assertIsInstance(tester.start_all(rthandle), dict)

    def test_stop_all(self):
        rthandle.invoke.return_value = {'status': '1'}
        self.assertIsInstance(tester.stop_all(rthandle), dict)

    @patch('jnpr.toby.trafficgen.ixia.ixiatester._add_addr_custom_pattern')
    def test_add_igmp_client(self, patch_addr):
        patch_addr.return_value = 'ch1'
        rthandle.invoke.return_value = {'status': '1', 'igmp_group_handle': 'igmp1', 'igmp_source_handle': 'src1',
                                        'igmp_host_handle': 'h1', 'multicast_group_handle': 'm1',
                                        'multicast_source_handle': 'ms1'}
        test_args = {'handle': 'h1', 'filter_mode': 'exclude', 'iptv': '1', 'group_start_addr': '225.0.0.2'}
        self.assertIsInstance(tester.add_igmp_client(rthandle, **test_args), dict)
        rthandle.invoke.return_value['status'] = '0'
        self.assertIsInstance(tester.add_igmp_client(rthandle, **test_args), dict)
        result1 = {'status': '1', 'igmp_host_handle': 'h1'}
        result2 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2]
        self.assertIsInstance(tester.add_igmp_client(rthandle, **test_args), dict)
        result2 = {'status': '1', 'multicast_group_handle': 'gh1'}
        result3 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2, result3]
        self.assertIsInstance(tester.add_igmp_client(rthandle, **test_args), dict)
        result3 = {'status': '1', 'multicast_source_handle': 'ms1'}
        result4 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2, result3, result4]
        self.assertIsInstance(tester.add_igmp_client(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    def test_igmp_client_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'h1', 'action': 'start', 'start_group_addr': '225.0.0.1', 'group_count': '1',
                     'start_source_addr': '10.0.0.1', 'source_count': '1'}
        self.assertIsInstance(tester.igmp_client_action(rthandle, **test_args), dict)

    def test_add_addr_custom_pattern(self):
        rthandle.invoke.return_value = {'status': '1', 'multivalue_handle': 'mh1', 'custom_handle': 'ch1'}
        self.assertEqual(tester._add_addr_custom_pattern(rthandle, start='225.0.0.1', step='0.0.0.1'), 'mh1')
        self.assertEqual(tester._add_addr_custom_pattern(rthandle, type='v6', start='2000::1', step='::1'), 'mh1')

    @patch('jnpr.toby.trafficgen.ixia.ixiatester._add_addr_custom_pattern')
    def test_add_mld_client(self, patch_addr):
        patch_addr.return_value = 'ch1'
        rthandle.invoke.return_value = {'status': '1', 'mld_group_handle': 'mld1', 'mld_source_handle': 'src1',
                                        'mld_host_handle': 'h1', 'multicast_group_handle': 'm1',
                                        'multicast_source_handle': 'ms1'}
        test_args = {'handle': 'h1', 'filter_mode': 'exclude', 'iptv': '1', 'group_start_addr': 'FF02::2'}
        self.assertIsInstance(tester.add_mld_client(rthandle, **test_args), dict)
        rthandle.invoke.return_value['status'] = '0'
        self.assertIsInstance(tester.add_mld_client(rthandle, **test_args), dict)
        result1 = {'status': '1', 'mld_host_handle': 'h1'}
        result2 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2]
        self.assertIsInstance(tester.add_mld_client(rthandle, **test_args), dict)
        result2 = {'status': '1', 'multicast_group_handle': 'gh1'}
        result3 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2, result3]
        self.assertIsInstance(tester.add_mld_client(rthandle, **test_args), dict)
        result3 = {'status': '1', 'multicast_source_handle': 'ms1'}
        result4 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2, result3, result4]
        self.assertIsInstance(tester.add_mld_client(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    def test_mld_client_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'h1', 'action': 'start', 'start_group_addr': 'FF02::1', 'group_count': '1',
                     'start_source_addr': '1000::1', 'source_count': '1'}
        self.assertIsInstance(tester.mld_client_action(rthandle, **test_args), dict)

    def test_add_application_traffic(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'name': 'n1', 'source': 's1', 'destination': 'd1', 'flows': '100', 'type': 'v4v6'}
        self.assertIsInstance(tester.add_application_traffic(rthandle, **test_args), dict)

    def test_add_bgp(self):
        rthandle.invoke.return_value = {'status': '1', 'bgp_handle': 'b1', 'multivalue_handle': 'mh1',
                                        'network_group_handle': 'ng1', 'ipv4_prefix_pools_handle': 'v4prex',
                                        'ipv6_prefix_pools_handle': 'v6pref'}
        test_args = {'handle': '/topology:1/deviceGroup:1/ethernet:1/ipv4:1', 'type': 'ebgp', 'local_as': '65000',
                     'hold_time': 20, 'restart_time': 10, 'keepalive': 15, 'enable_flap': 1, 'flap_up_time': 10,
                     'flap_down_time': 10, 'stale_time': 10, 'graceful_restart': 1, 'remote_ip': '10.0.0.2',
                     'router_id': '100.0.0.1', 'prefix_group': [{'network_prefix': '10.0.0.0/8', 'network_step': '1',
                                                                 'network_count': '8', 'sub_prefix_length': '24',
                                                                 'sub_prefix_count': '2'}]}
        self.assertIsInstance(tester.add_bgp(rthandle, **test_args), dict)
        rthandle.invoke.return_value['status'] = '0'
        test_args['handle'] = '/topology:1/deviceGroup:1/ethernet:1/ipv6:1'
        self.assertIsInstance(tester.add_bgp(rthandle, **test_args), dict)
        rthandle.invoke.return_value['status'] = '1'
        self.assertIsInstance(tester.add_bgp(rthandle, **test_args), dict)
        result1 = rthandle.invoke.return_value
        result2 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result1, result2]
        self.assertIsInstance(tester.add_bgp(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = [result1, result1, result1, result2]
        self.assertIsInstance(tester.add_bgp(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    def test_add_isis(self):
        rthandle.invoke.return_value = {'status': '1',
                                        'multivalue_handle': 'multivalue_handle',
                                        'network_group_handle': 'network_group_handle',
                                        'isis_l3_handle': 'isis_l3_handle',
                                        'isis_l3_te_handle': 'isis_l3_te_handle',
                                        'sr_algoList_handle_rtr': 'sr_algoList_handle_rtr',
                                        'srlg_range_handle_rtr': 'srlg_range_handle_rtr',
                                        'srgb_range_handle_rtr': 'srgb_range_handle_rtr',
                                        'srlb_descList_handle_rtr': 'srlb_descList_handle_rtr',
                                        'isis_l3_router_handle': 'isis_l3_router_handle'}
        test_args = {'handle': '/topology:2/deviceGroup:1/ethernet:1',
                     'auth_type': 'md5',
                     'auth_key': 'joshua',
                     'intf_type': 'ptop',
                     'multiplier': 1,
                     'prefix_type': 'ipv4-prefix',
                     'ipv4_prefix_network_address': '101.1.0.0',
                     'ipv4_prefix_network_address_step': '1.0.0.0',
                     'ipv4_prefix_length': '24',
                     'ipv4_prefix_address_step': '1',
                     'ipv4_prefix_number_of_addresses': '1000',}
        #self.assertIsInstance(tester.add_isis(rthandle, **test_args), dict)
        rthandle.invoke.return_value['status'] = '0'
        #self.assertIsInstance(tester.add_isis(rthandle, **test_args), dict)

    def test_bgp_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': '/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bgp:1', 'action': 'start'}
        self.assertIsInstance(tester.bgp_action(rthandle, **test_args), dict)
        test_args['action'] = 'delete'
        self.assertIsInstance(tester.bgp_action(rthandle, **test_args), dict)

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_dhcp_server')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_link')
    def test_add_l2tp_server(self, patch_link, patch_dhcp):
        rthandle.invoke.return_value = {'status': '1', 'ipv4_handle': 'v4', 'ethernet_handle': 'eth1',
                                        'lns_handle': 'lns1', 'pppox_server_sessions_handle': 'pssh',
                                        'pppox_server_handle': 'psh1', 'dhcpv6_server_handle': 'dsh1'}
        test_args = {'port': '1/1', 'l2tp_dst_addr': '10.1.1.2', 'l2tp_src_addr': '10.1.1.1', 'netmask': '24',
                     'vlan_id': '1', 'handle': 'h1', 'tun_hello_req': 1, 'tun_hello_interval': 1,
                     'username': 'test', 'password': 'pwd', 'ip_cp': 'dual'}
        patch_link.return_value = {'status': '1', 'ipv4_handle': 'v4', 'ethernet_handle': 'eth1'}
        patch_dhcp.return_value = {'status': '1', 'dhcpv6_server_handle': 'dsh1'}
        self.assertIsInstance(tester.add_l2tp_server(rthandle, **test_args), dict)
        try:
            patch_link.return_value['status'] = '0'
            tester.add_l2tp_server(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add ip address for lns')
        patch_link.return_value['status'] = '1'
        test_args['tun_auth_enable'] = 0
        patch_dhcp.return_value['status'] = '0'
        self.assertIsInstance(tester.add_l2tp_server(rthandle, **test_args), dict)

    def test_l2tp_server_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': '/topology:1/deviceGroup:1/ethernet:1/ipv4:1', 'action': 'start'}
        self.assertIsInstance(tester.l2tp_server_action(rthandle, **test_args), dict)

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_link')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_topology')
    def test_add_l2tp_client(self, patch_topo, patch_link):
        patch_link.return_value = {'status': '1', 'ipv4_handle': 'v4', 'ethernet_handle': 'eth1'}
        rthandle.invoke.return_value = {'status': '1', 'multivalue_handle': 'mv1', 'lac_handle': 'lac1',
                                        'pppox_client_handle': 'ppp', 'dhcpv6client_handle': 'v6',
                                        'dhcpv6_client_handle': 'v62'}
        test_args = {'port': '1/1', 'l2tp_src_addr': '10.1.1.1', 'vlan_id': '1', 'vlan_id_step': '1',
                     'tun_secret': 'sec', 'l2tp_dst_step': '1', 'l2tp_dst_count': '1', 'echo_req': '2',
                     'echo_req_interval': '10', 'tun_hello_req': '2', 'tun_hello_interval': 10, 'auth_mode': 'chap',
                     'l2tp_dst_step': '1', 'mode': 'txt', 'username': 'test?', 'password': 'pwd',
                     'sessions_per_tunnel': 10, 'num_tunnels': '2', 'l2tp_src_count': '2', 'ip_cp': 'dual',
                     'dhcpv6_ia_type': 'iapd', 'rapid_commit': '1', 'dhcp4_broadcast': '1',
                     'v6_max_no_per_client': '1', 'dhcpv6_iana_count': '1', 'dhcpv6_iapd_count': '1',
                     'l2tp_src_gw': '10.1.1.2'}
        self.assertIsInstance(tester.add_l2tp_client(rthandle, **test_args), dict)
        try:
            patch_link.return_value['status'] = '0'
            tester.add_l2tp_client(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add ip address for lns')
        patch_link.return_value['status'] = '1'
        test_args['tun_auth_enable'] = '0'
        rthandle.invoke.return_value.pop('dhcpv6_client_handle')
        result1 = rthandle.invoke.return_value
        result2 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result1, result2]
        try:
            tester.add_l2tp_client(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'failed to add dhcpv6 client over l2tp')

        rthandle.invoke.side_effect = None

    def test_l2tp_client_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        for action in ['start', 'stop', 'abort', 'restart']:
            test_args = {'handle': '/topology:1/deviceGroup:1/deviceGroup:1/ethernet:1/ipv4:1/l2tp:1', 'action': action}
            self.assertIsInstance(tester.l2tp_client_action(rthandle, **test_args), dict)


    def test_client_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        for action in ['start', 'stop', 'abort', 'restart']:
            test_args = {'handle': '/topology:1/deviceGroup:1/deviceGroup:1/ethernet:1/ipv4:1', 'action': action}
            self.assertIsInstance(tester.client_action(rthandle, **test_args), dict)

    def test_l2tp_client_stats(self):
        rthandle.invoke.return_value = {'status': '1'}
        for handle in ['lac', 'dhcpv6', 'pppox']:
            self.assertIsInstance(tester.l2tp_client_stats(rthandle, handle=handle), dict)

    def test_add_dhcp_server(self):
        rthandle.invoke.return_value = {'status': '1', 'dhcpv4server_handle': 'v4', 'dhcpv6server_handle': 'v6'}
        test_args = {'handle': 'v4', 'lease_time': '300', 'pool_start_addr': '100.0.0.2', 'pool_mask_length': '8',
                     'pool_size': '1400', 'pool_gateway': '100.0.0.1', 'dhcpv6_ia_type': 'pd',
                     'pool_prefix_start': '2000::1', 'pool_prefix_length': '8', 'pool_prefix_size': '4600'}
        self.assertIsInstance(tester.add_dhcp_server(rthandle, **test_args), dict)

        # v4 multi-servers
        ms_v4_args = dict(test_args)
        ms_dict = {'pool_gateways': MagicMock(),
                   'lease_times': MagicMock(),
                   'pool_start_addresses': MagicMock(),
                   'pool_sizes': MagicMock(),
                   'pool_mask_lengths': MagicMock(),
                   'pool_gateway_inside_step': MagicMock(),
                   'subnet_addr_assign': MagicMock(),
                   'pool_inside_step': MagicMock()}
        ms_v4_args.update({'multi_servers_config_v4': ms_dict,
                           'handle': '/topology:1/deviceGroup:1/ethernet:1/ipv4:1'})
        rthandle.invoke.return_value['multivalue_handle'] = MagicMock()
        self.assertIsInstance(tester.add_dhcp_server(rthandle, **ms_v4_args), dict)

        test_args['handle'] = 'v6'
        rthandle.invoke.return_value['status'] = '1'
        self.assertIsInstance(tester.add_dhcp_server(rthandle, **test_args), dict)
        rthandle.invoke.return_value['status'] = '0'
        self.assertIsInstance(tester.add_dhcp_server(rthandle, **test_args), dict)
        try:
            test_args.pop('handle')
            tester.add_dhcp_server(rthandle, **test_args)
        except Exception as err:
            self.assertEqual(err.args[0], 'ip handle must be provided ')

        # v6 multi-servers
        ms_v6_args = dict(test_args)
        ms_dict = {'pool_inside_step': MagicMock(),
                   'pool_prefix_inside_step': MagicMock(),
                   'pool_start_addresses': MagicMock(),
                   'pool_prefix_starts': MagicMock(),
                   'pool_sizes': MagicMock(),
                   'pool_prefix_sizes': MagicMock(),
                   'pool_prefix_lengths': MagicMock(),
                   'pool_mask_lengths': MagicMock()}
        ms_v6_args.update({'multi_servers_config_v6': ms_dict,
                           'handle': '/topology:1/deviceGroup:1/ethernet:1/ipv6:1'})
        rthandle.invoke.return_value['multivalue_handle'] = MagicMock()
        self.assertIsInstance(tester.add_dhcp_server(rthandle, **ms_v6_args), dict)

    def test_dhcp_server_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'h1', 'action': 'start_stop'}
        self.assertIsInstance(tester.dhcp_server_action(rthandle, **test_args), dict)


    @patch('jnpr.toby.trafficgen.ixia.ixiatester.traffic_action')
    def test_traffic_simulation(self, patch_action):
        rthandle.invoke.return_value = {'status': '1', 'tr1': {'headers': 's1 s2 s3'}, 'traffic_item': 'tr1',
                                        'stream_id': 's1', 'handle': 'h1'}
        test_args = {'dst_port': '1/2', 'src_port': '1/1', 'frame_size': '1500', 'l3_length': '1400',
                     'transmit_mode': 'burst', 'name': 'tr1', 'rate_pps': '100', 'rate_bps': '100',
                     'rate_percent': '100', 'packets_count': '100', 'duration': '60', 'vlan_id': '1', 'vlan_step': '1',
                     'vlan_count': '1', 'svlan_id': '1', 'vlan_priority': '7', 'vlan_priority_step': '1',
                     'svlan_priority': '7', 'svlan_priority_step': '1', 'src_mac': '11:22:33:44:55:66',
                     'dst_mac': '01:02:03:04:05:06', 'src_mac_step': 1, 'dst_mac_step': '1', 'src_ip': '10.0.0.1',
                     'src_ip_step': '1', 'dst_ip': '10.0.0.2', 'dst_ip_step': '1', 'src_ipv6': '2000::1',
                     'src_ipv6_step': '1', 'dst_ipv6': '3000::1', 'dst_ipv6_step': '::1', 'ip_precedence': '1',
                     'ip_precedence_mode': 'm', 'ip_precedence_step': '1', 'ip_precedence_count': '4', 'ip_dscp': '32',
                     'ip_dscp_mode': 'm2', 'ip_dscp_step': '8', 'ip_dscp_count': '8', 'l4_protocol': 'dhcpv6',
                     'l3_protocol': 'ip', 'message_type': 'ty1', 'pppoe_encap': True}
        self.assertIsInstance(tester.traffic_simulation(rthandle, **test_args), dict)
        test_args.pop('frame_size')
        test_args.pop('l3_length')
        rthandle.invoke.return_value['status'] = '0'
        self.assertIsInstance(tester.traffic_simulation(rthandle, **test_args), dict)
        rthandle.invoke.return_value['status'] = '1'
        test_args['l4_protocol'] = 'dhcp'
        self.assertIsInstance(tester.traffic_simulation(rthandle, **test_args), dict)
        test_args['l4_protocol'] = 'dhcpv6'
        result1 = rthandle.invoke.return_value
        result2 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2]
        self.assertIsInstance(tester.traffic_simulation(rthandle, **test_args), dict)
        test_args['l4_protocol'] = 'icmpv6'
        test_args['message_type'] = 'echo_req_echo_reply'
        rthandle.invoke.side_effect = [result1, result2]
        self.assertIsInstance(tester.traffic_simulation(rthandle, **test_args), dict)
        test_args.pop('message_type')
        rthandle.invoke.side_effect = [result1, result2]
        self.assertIsInstance(tester.traffic_simulation(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    @patch('time.sleep')
    def test_ancp_action(self, patch_sleep):
        self.assertEqual(tester.ancp_action(rthandle, handle='ancp1', action='abort'), None)

        rthandle.invoke.return_value = ['up']
        self.assertEqual(tester.ancp_action(rthandle, handle='ancp1', action='start'), None)

        rthandle.invoke.return_value = ['up']
        rthandle._invokeIxNet.return_value = 'obj'
        self.assertEqual(tester.ancp_action(rthandle, handle='ancp1', action='restartdown'), None)

        rthandle.invoke.return_value = ['notStarted']
        self.assertEqual(tester.ancp_action(rthandle, handle='ancp1', action='stop'), None)

        rthandle.invoke.return_value = ['down']
        try:
            tester.ancp_action(rthandle, handle='ancp1', action='start')
        except Exception as err:
            self.assertTrue('ancp action enable failed with status' in err.args[0])

        rthandle.invoke.return_value = ['up']
        try:
            tester.ancp_action(rthandle, handle='ancp1', action='stop')
        except Exception as err:
            self.assertTrue('ancp action disable failed with status' in err.args[0])

        rthandle.invoke.return_value = ['down']
        try:
            tester.ancp_action(rthandle, handle='ancp1', action='restartdown')
        except Exception as err:
            self.assertTrue('ancp action restartdown failed with status' in err.args[0])

    @patch('jnpr.toby.trafficgen.ixia.ixiatester._set_custom_pattern')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_string_mv')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_link')
    def test_add_ancp(self, patch_link, patch_string, patch_custom):
        patch_custom.return_value = 'custom'
        patch_string.return_value = {'status': '1', 'multivalue_handle': 'mv1'}
        patch_link.return_value = {'status': '1', 'ipv4_handle': 'v4', 'device_group_handle': 'gd1'}
        rthandle.invoke.return_value = {'status': '1', 'ancp_handle': 'ancp', 'ancp_subscriber_lines_handle': 'line',
                                        'network_group_handle': 'ngh'}
        test_args = {'flap_mode': 'f1', 'circuit_id': 'c1?', 'circuit_id_start': '1', 'keep_alive_retries': '3',
                     'keep_alive': '20', 'remote_id': 'rm?', 'remote_id_start': '1', 'service_vlan_start': '1',
                     'customer_vlan_start': '1', 'pon_type': 'gpon', 'tech_type': 'dsl', 'dsl_type': 'adsl_2'}
        self.assertIsInstance(tester.add_ancp(rthandle, **test_args), dict)
        patch_link.return_value['status'] = '0'
        self.assertIsInstance(tester.add_ancp(rthandle, **test_args), dict)
        patch_link.return_value['status'] = '1'
        rthandle.invoke.return_value['status'] = '0'
        self.assertIsInstance(tester.add_ancp(rthandle, **test_args), dict)
        rthandle.invoke.return_value['status'] = '1'
        result1 = rthandle.invoke.return_value
        result2 = {'status': '0'}
        rthandle.invoke.side_effect = [result1, result2]
        self.assertIsInstance(tester.add_ancp(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = [result1, result1, result2]
        test_args['circuit_id'] = 'cir1'
        test_args['remote_id'] = 'rem1'
        self.assertIsInstance(tester.add_ancp(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    @patch('jnpr.toby.trafficgen.ixia.ixiatester.set_vlan')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_device_group')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_topology')
    def test_add_lacp(self, patch_topo, patch_device, patch_vlan):
        patch_topo.return_value = {'status': '1', 'topology_handle': 'topo1', 'device_group_handle': 'dg1'}
        patch_vlan.return_value = {'status': '1', 'ethernet_handle': 'eth1'}
        patch_device.return_value = {'status': '1', 'device_group_handle': 'dg1'}
        rthandle.invoke.return_value = {'status': '1', 'lacp_handle': 'lacp1', 'staticLag_handle': 's1'}
        test_args = {'name': 'ae1', 'port_list': ['1/1', '1/2'], 'protocol': 'lacp', 'actor_key': 'a1',
                     'admin_key': '1', 'actor_system_id': '64', 'mode': 'active', 'actor_port_pri': '2'}
        self.assertIsInstance(tester.add_lacp(rthandle, **test_args), dict)
        patch_topo.return_value['status'] = '0'
        try:
            tester.add_lacp(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed at add topology for ports' in err.args[0])
        patch_topo.return_value['status'] = '1'
        patch_device.return_value['status'] = '0'
        try:
            tester.add_lacp(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed at add device for ports' in err.args[0])
        patch_device.return_value['status'] = '1'
        rthandle.invoke.return_value['status'] = '0'
        try:
            tester.add_lacp(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to add lacp for ports' in err.args[0])
        rthandle.invoke.return_value['status'] = '1'
        rthandle.invoke.return_value.pop('lacp_handle')
        self.assertIsInstance(tester.add_lacp(rthandle, **test_args), dict)

    def test_ancp_line_action(self):
        rthandle.invoke.return_value = {'status': '1'}
        for action in ['flap_start', 'flap_stop', 'flap_start_resync', 'port_up', 'port_down']:
            self.assertIsInstance(tester.ancp_line_action(rthandle, handle='h1', action=action), dict)

    def test_set_pppoe_ia_attribute(self):
        rthandle.invoke.return_value = {'status': '1', 'multivalue_handle': 'mv1'}
        test_args = {'handle': 'pppox', 'dsltype': 'adsl_1', 'upstream_rate': '20', 'downstream_rate': '30',
                     'pon_type': 'gpon', 'aggregate_circuit_id': 'aci', 'circuit_id': 'cid', 'remote_id': 'rid'}
        self.assertEqual(tester.set_pppoe_ia_attribute(rthandle, **test_args), None)
        test_args = {'handle': 'pppox'}
        rthandle.invoke.return_value = {'status': '0'}
        try:
            tester.set_pppoe_ia_attribute(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('failed to set the pppoe ia attributes' in err.args[0])

    def test_set_ancp_line_sttribute(self):
        rthandle.invoke.return_value = {'tlv_handle': 'tlv1', 'multivalue_handle': 'mv1',
                                        'tlv_value_handle': 'v1', 'v1': {'tlv_field_handle': 'f1'}, 'status': '1'}
        test_args = {'handle': 'h1', 'aggregate_circuit_id': 'cir1'}
        self.assertEqual(tester.set_ancp_line_attribute(rthandle, **test_args), {'aggregate_circuit_id_handle': 'f1'})
        test_args = {'handle': 'h1', 'new_pon_access_tlv': True, 'new_dsl_access_tlv': True, 'dsl_type_in_tlv': '3',
                     'dsl_type': '5', 'upstream_rate': '50', 'downstream_rate': '500', 'remote_id': 'rid',
                     'circuit_id': 'cid',}
        self.assertEqual(tester.set_ancp_line_attribute(rthandle, **test_args), {'tlv_handle': 'tlv1'})
        test_args = {'handle': 'tlv1', 'dsl_tlv_value_dict': {'all': '2'}}
        self.assertEqual(tester.set_ancp_line_attribute(rthandle, **test_args), {})
        test_args = {'handle': 't1', 'dsl_tlv_value_dict': {'all': '2'}, 'new_dsl_access_tlv': True}
        self.assertEqual(tester.set_ancp_line_attribute(rthandle, **test_args), {'tlv_handle': 'tlv1'})
        test_args = {'handle': 'h1', 'pon_tlv_value_dict': {'PON-Tree-Maximum-Data-Rate-Upstream':'disable',
                                                              'PON-Tree-Maximum-Data-Rate-Downstream':'2000'}}
        self.assertEqual(tester.set_ancp_line_attribute(rthandle, **test_args), {})
        rthandle.invoke.return_value = {'tlv_handle': 'tlv1', 'multivalue_handle': 'mv1',
                                        'tlv_value_handle': 'v1', 'v1': {'tlv_field_handle': 'f1'}, 'status': '0'}
        try:
            tester.set_ancp_line_attribute(rthandle, handle='field1', aggregate_circuit_id='aci1')
        except Exception as err:
            self.assertTrue('failed to set aggregate_ascii' in err.args[0])
        self.assertEqual(tester.set_ancp_line_attribute(rthandle, handle='tlv', pon_type_in_tlv='5'), {})
        try:
            tester.set_ancp_line_attribute(rthandle, handle='h1', pon_type='gpon', dsl_type_in_tlv='3')
        except Exception as err:
            self.assertTrue('failed to set the ancp line attributes' in err.args[0])

    def test_verify_traffic_throughput_tester(self):
        rthandle.traffic_item = ['s1']
        rthandle.invoke.return_value = {'l23_test_summary': {'rx': {'pkt_count': '1000'}, 'tx': {'pkt_count': '1000'}}}
        self.assertIsInstance(tester.verify_traffic_throughput_tester(rthandle, minimum_rx_percentage=97,
                                                                      mode='all'), dict)
        try:
            tester.verify_traffic_throughput_tester(rthandle, mode='traffic_item', stream_name=None)
        except Exception as err:
            self.assertTrue('Invalid mode!' in err.args[0])
        rthandle.invoke.return_value = {'l23_test_summary': {'rx': {'pkt_count': '900'}, 'tx': {'pkt_count': '1000'}}}
        try:
            tester.verify_traffic_throughput_tester(rthandle)
        except Exception as err:
            self.assertTrue('Observed aggregate throughput' in err.args[0])
        try:
            tester.verify_traffic_throughput_tester(rthandle, mode='other')
        except Exception as err:
            self.assertTrue('Invalid mode. Please try l23_test_summary or traffic_item.' in err.args[0])

        rthandle.invoke.return_value = {'traffic_item': {'s1': {'rx': {'total_pkts': '1000'},
                                                                'tx': {'total_pkts': '1000'}}}}
        try:
            tester.verify_traffic_throughput_tester(rthandle, mode='traffic_item', stream_name='p2')
        except Exception as err:
            self.assertTrue('does not match any configured stream stream names' in err.args[0])

        self.assertIsInstance(tester.verify_traffic_throughput_tester(rthandle, mode='traffic_item', stream_name='s1'),
                              dict)
        rthandle.invoke.return_value['traffic_item']['s1']['rx']['total_pkts'] = '900'
        try:
            tester.verify_traffic_throughput_tester(rthandle, mode='traffic_item', stream_name='s1')
        except Exception as err:
            self.assertTrue('Observed aggregate throughput of' in err.args[0])

        rthandle.invoke.return_value = {'traffic_item': {'s1': {'rx': {'total_pkt_mbit_rate': '100'},
                                                                'tx': {'total_pkt_mbit_rate': '100'}}}}
        test_args = {'mode': 'traffic_item', 'stream_name': 's1', 'instantaneous_rate': '100mbps', 'verify_by': 'rate'}
        self.assertIsInstance(tester.verify_traffic_throughput_tester(rthandle, **test_args), dict)
        test_args['instantaneous_rate'] = '97mbpsmbps'
        try:
            tester.verify_traffic_throughput_tester(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('Parsed multiple digits from entered instantaneous_rate' in err.args[0])
        test_args['instantaneous_rate'] = '97mbps'
        try:
            tester.verify_traffic_throughput_tester(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('Measured traffic rate of' in err.args[0])
        rthandle.invoke.return_value = {'traffic_item': {'s1': {'rx': {'total_pkts': '1000'}}}}

        test_args.pop('instantaneous_rate')
        test_args['verify_by'] = 'packetcount'
        test_args['packet_count'] = '1000'
        self.assertIsInstance(tester.verify_traffic_throughput_tester(rthandle, **test_args), dict)
        try:
            test_args['packet_count'] = '1200'
            tester.verify_traffic_throughput_tester(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('packets received are less than' in err.args[0])
        try:
            test_args['verify_by'] = 'other'
            tester.verify_traffic_throughput_tester(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('You selected an invalid verify_by parameter' in err.args[0])

    def test_set_pppoe_dsl_attribute(self):
        rthandle.invoke.return_value = 'obj'
        test_args = {'handle': 'pppox', 'dsltype': 'adsl_1', 'upstream_rate': '20', 'downstream_rate': '30'}
        self.assertEqual(tester.set_pppoe_dsl_attribute(rthandle, **test_args), None)
        test_args = {'handle': 'pppox'}
        rthandle.invoke.side_effect = ['obj', 'obj', 0, 'obj', 'obj', 'obj', 'obj', Exception]
        try:
            tester.set_pppoe_dsl_attribute(rthandle, **test_args)
        except:
            self.assertRaises(Exception)
        rthandle.invoke.side_effect = None

    def test_set_pppoe_dsl_attribute_IxNet(self):
        rthandle._invokeIxNet.return_value = 'obj'
        test_args = {'handle': 'pppox', 'dsltype': 'adsl_1', 'upstream_rate': '20', 'downstream_rate': '30'}
        self.assertEqual(tester.set_pppoe_dsl_attribute_Ixnet(rthandle, **test_args), None)
        test_args = {'handle': 'pppox'}
        rthandle._invokeIxNet.side_effect = ['obj', 'obj', 0, 'obj', 'obj', 'obj', 'obj', Exception]
        try:
            tester.set_pppoe_dsl_attribute_Ixnet(rthandle, **test_args)
        except:
            self.assertRaises(Exception)
        rthandle._invokeIxNet.side_effect = None

    def test_set_pppoe_tlv(self):
        dict1 = {'ONT/ONU-Average-Data-Rate-Downstream': '1000', 'ONT/ONU-Peak-Data-Rate-Downstream': '2000',
                 'ONT/ONU-Maximum-Data-Rate-Upstream': '3000', 'ONT/ONU-Assured-Data-Rate-Upstream': '4000'}
        rthandle.invoke.return_value = {'tlv_handle': 't1', 'tlv_value_handle': 'v1',
                                        'v1': {'subtlv_handle': 'sub1','tlv_field_handle': 'tv1',
                                               'tlv_container_handle': 'con', 'con': {'tlv_field_handle': 'h1 h2'}},
                                        'tlv_type_handle': 'tt1', 'tt1': {'tlv_field_handle': 'tv2'}}
        self.assertEqual(tester.set_pppoe_tlv(rthandle, handle='h1', pon_tlv_value_dict=dict1), None)
        dict2 = {'all': '100'}
        self.assertEqual(tester.set_pppoe_tlv(rthandle, handle='h1', pon_tlv_value_dict=dict2), None)
        rthandle.pppoe_pon_tlv = {'h1':{'tlv_handle': 'tt2',
                                        'tlv_value_handle': {'ONT/ONU-Peak-Data-Rate-Downstream': 'v1'}}}
        dict3 = {'ONT/ONU-Peak-Data-Rate-Downstream': '1000'}
        self.assertEqual(tester.set_pppoe_tlv(rthandle, handle='h1', pon_tlv_value_dict=dict3), None)
        dict4 = {'ONT/ONU-Peak-Data-Rate-Downstream': 'disable'}
        self.assertEqual(tester.set_pppoe_tlv(rthandle, handle='h1', pon_tlv_value_dict=dict4), None)
        dict1 = {'Minimum-Net-Data-Rate-Upstream':'1000', 'Minimum-Net-Data-Rate-Downstream':'2000',
                 'Minimum-Net-Low-Power-Data-Rate-Upstream':'3000', 'Maximum-Interleaving-Delay-Downstream':'4000'}
        self.assertEqual(tester.set_pppoe_tlv(rthandle, handle='h1', dsl_tlv_value_dict=dict1), None)
        self.assertEqual(tester.set_pppoe_tlv(rthandle, handle='h1', access_loop_circuit_id='test1'), None)
        self.assertEqual(tester.set_pppoe_tlv(rthandle, handle='h1', access_loop_remote_id='test1'), None)
        self.assertEqual(tester.set_pppoe_tlv(rthandle, handle='h1', access_aggregation_ascii='testascii'), None)
        self.assertEqual(tester.set_pppoe_tlv(rthandle, handle='h1', access_aggregation_binary={'inner_vlan': '3'}), None)

    def test_set_ancp_rate(self):
        # Test invoke Exception
        rthandle.invoke.return_value = {'status': '0'}
        try:
            tester.set_ancp_rate(rthandle, global_start_rate="200", global_stop_rate="200")
        except Exception as err:
            self.assertTrue('Failed to set ANCP rates' in err.args[0])

        # Test invalid parameter Exception
        rthandle.invoke.return_value = {'status': '1'}
        try:
            tester.set_ancp_rate(rthandle, start_rate="200", stop_rate="200")
        except Exception as err:
            self.assertTrue('Invalid parameter' in err.args[0])

        # Test successful rt invoke
        rthandle.invoke.return_value = {'status': '1'}
        self.assertEqual(tester.set_ancp_rate(rthandle, global_start_rate="200", global_stop_rate="200"), None)

    def test_set_ancp_access_type(self):
        test_args = {'handle': 'rt_ancp_line_handle'}

        # Test Exception
        rthandle.invoke.return_value = {'status': '0'}
        try:
            tester.set_ancp_access_type(rthandle, **test_args)
        except Exception as err:
            self.assertTrue('Failed to set ANCP access type' in err.args[0])

        # Test successful rt invoke
        rthandle.invoke.return_value = {'status': '1'}
        test_args = {'handle': 'rt_ancp_line_handle',
                     'enable_dsl_type': True,
                     'enable_pon_type': False,
                     'tech_type': 'dsl'}
        self.assertEqual(tester.set_ancp_access_type(rthandle, **test_args), None)

        test_args = {'handle': 'rt_ancp_line_handle',
                     'enable_dsl_type': False,
                     'enable_pon_type': True,
                     'tech_type': 'dsl'}
        self.assertEqual(tester.set_ancp_access_type(rthandle, **test_args), None)

    @patch('jnpr.toby.trafficgen.ixia.ixiatester._add_addr_custom_pattern')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester._set_custom_pattern')
    @patch('jnpr.toby.trafficgen.ixia.ixiatester.add_link')
    def test_j_add_evpn_node(self, patch_addr, patch_custom, patch_link):
        test_args = {'port': '6/10', 'connect_ip': '10.5.1.2', 'connect_gateway': '10.5.1.1', 'connect_vlan': '512',
                     'dut_count': 2, 'dut_loop_ip': '100.100.100.253', 'rr_loop_ip': '100.100.100.1', 'esi_count': '1',
                     'evpn_mode': 'multihome', 'evi_count': 3, 'esi_type': '0', 'single_active': '1',
                     'use_control_word': '1', 'evpn_svlan_start': '1', 'evpn_ipv4_start': '200.0.0.1'}
        patch_addr.return_value = 'mv_addr'
        patch_custom.return_value = 'mv'
        patch_link.return_value = {'ipv4_handle': 'ipv4', 'device_group_handle': 'dh1', 'status': '1'}
        rthandle.invoke.return_value = {'ospfv2_handle': 'os1', 'network_group_handle': 'n1', 'status': '1',
                                        'device_group_handle': 'd1', 'multivalue_handle': 'mv2',
                                        'ipv4_loopback_handle': 'ip1', 'rsvpte_lsp_handle': 'rsvp',
                                        'ldp_basic_router_handle': 'ldp1', 'ldp_connected_interface_handle': 'ldp2',
                                        'bgp_handle': 'bgp1', 'evpn_evi': 'evi', 'mac_pools_handle': 'macpool',
                                        'ipv4_handle': 'ipv4'}

        self.assertIsInstance(tester.j_add_evpn_node(rthandle, **test_args), dict)
        test_args['label_protocol'] = 'ldp'
        test_args['evpn_mode'] = 'singlehome'
        test_args['irb_enable'] = '1'
        test_args['irb_addr_start'] = '1.2.3.4'
        test_args['use_control_word'] = '1'
        test_args['evpn_ipv6_start'] = '3000::1'
        self.assertIsInstance(tester.j_add_evpn_node(rthandle, **test_args), dict)
        test_args.pop('evpn_ipv4_start')
        self.assertIsInstance(tester.j_add_evpn_node(rthandle, **test_args), dict)

    def test_add_lag(self):
        rthandle.invoke.return_value = {'lag_handle': 'lag:1'}
        test_args={'port_list': ['6/10', '6/11']}
        self.assertEqual(tester.add_lag(rthandle, **test_args), 'lag:1')

if __name__ == '__main__':
    unittest.main()
