import unittest
import builtins
from mock import patch, MagicMock
import jnpr.toby.trafficgen.spirent.spirenttester as tester
from jnpr.toby.bbe.bbevar.bbevars import BBEVars, BBEVarInterface
from jnpr.toby.init.init import init
builtins.t = MagicMock()

builtins.t = MagicMock(spec=init)
builtins.t.log = MagicMock()

builtins.bbe = MagicMock(spec=BBEVars)
rthandle = MagicMock()

class TestSpirentTester(unittest.TestCase):
    """
    TestSpirentTester class to handle spirenttester.py unit tests
    """
    def test_bbe_initialize(self):
        self.assertEqual(tester.bbe_initialize(rthandle), None)

    #........................................................#
    # Unit test for set_subscriber_mac API
    #........................................................#
    def test_set_subscriber_mac(self):
        # Test 1
        result2 = {'status': '1'}
        test_args = {'handle': 'emulateddevice1', 'mac': '11:22:33:44:55:66'}
        rthandle.invoke.side_effect =[result2]
        self.assertIsInstance(tester.set_subscriber_mac(rthandle, **test_args), dict)

        # Test 2
        result1 = 'emulateddevice101'
        result2 = {'status': '1'}
        test_args = {'handle': 'dhcpv4blkconfig', 'mac': '11:22:33:44:55:66'}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.set_subscriber_mac(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_vlan API 
    #........................................................#
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.set_subscriber_mac', return_value = {'result' : '1'})
    def test_set_vlan(self , patch_mac):
        # Test 1
        result1 = {'status': '1'}
        test_args = {'handle': 'emulateddevice1', 'mac': '11:22:33:44:55:66', 'vlan_start': '1', 'svlan_start': '1', 'mac_step': '1', 'vlan_priority': '1', 'vlan_priority_step': '1', 'vlan_user_priority_step': '1', 'svlan_priority': '1', 'svlan_priority_step': '1'}
        #test_args = {'handle': 'emulateddevice1', 'mac': '11:22:33:44:55:66', 'vlan_start': '1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.set_vlan(rthandle, **test_args), dict)

        # Test 2
        result1 = 'emulateddevice101'
        result2 = {'status': '1'}
        test_args = {'handle': 'dhcpv4blkconfig', 'mac': '11:22:33:44:55:66', 'vlan_start': '1', 'svlan_start': '1', 'mac_step': '1', 'vlan_priority': '1', 'vlan_priority_step': '1', 'vlan_user_priority_step': '1', 'svlan_priority': '1', 'svlan_priority_step': '1'}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.set_vlan(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for add_ancp API 
    #........................................................#
    def test_add_ancp(self):
        test_args = {'vlan_start': 30, 'service_vlan_repeat': 1, 'port': '1/2', 'service_vlan_start': 1, 'circuit_id_step': 1, 'dut_ip': '100.0.0.1', 'gateway': '35.1.9.1', 'count': 1, 'circuit_id': 'DTAG_ACI.0100.000000000055', 'vlan_length': 5, 'circuit_id_start': 100, 'lines_per_node': 1, 'customer_vlan_start': 1, 'customer_vlan_repeat': 1, 'service_vlan_step': 1, 'vlan_step': 10, 'circuit_id_repeat': 1, 'vlan_repeat': 1, 'customer_vlan_step': 1, 'vlan_allocation_model': '1_1', 'ip_addr': '35.1.9.2', 'netmask': '255.255.255.0', 'service_vlan_length': 4094, 'customer_vlan_length': 4094, 'dsl_type': 'adsl2_plus', 'ip_addr_step': '10.0.0.0'}
        #result1 = {'handle': 'router1 router2 router3 router4 router5', 'status': '1'}
        result1 = {'handle': 'router1', 'status': '1'}
        result2 = 'ancpaccessloopblockconfig1'
        #result3 = 'ancpaccessloopblockconfig1'
        result4 = ''
        result5 = {'handle': 'host1', 'status': '1'}
        result6 = 'ethiif1'
        result7 = {'handle': 'host1', 'ancp_subscriber_lines_handle': 'ancpaccessloopblockconfig1', 'status': '1'}
        result8 = 'subscriberdsllineprofile1'
        result9 = 'AncpWildcardModifier1'
        rthandle.invoke.side_effect =[result1, result2, result2, result4, result5, result7, result8, result9, result4]
        self.assertIsInstance(tester.add_ancp(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for add_pppoe_client API 
    #........................................................#
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.set_pppox_wildcard', return_value =  {'status': '1'})
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.set_vlan', return_value =  {'status': '1'})
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.set_option_82', return_value =  1)
    def test_add_pppoe_client(self, patch_pppox_wildcard, patch_set_vlan, patch_option82):
        test_args = {'vlan_start': 1, 'svlan_length': 4094, 'svlan_repeat': 1, 'port': '1/2', 'auth_mode': 'pap', 'username': 'RES_TERM_PPPOE', 'ip_type': 'ipv4', 'vlan_step': 1, 'remote_id_repeat': 1, 'circuit_id': 'DTAG_ACI.0100.000000000055', 'remote_id_start': 100, 'vlan_length': 4094, 'password': 'joshua', 'remote_id': 'DTAG_ARI.0100.000000000055', 'circuit_id_step': 1, 'circuit_id_repeat': 1, 'vlan_repeat': 1, 'remote_id_step': 1, 'svlan_step': 1, 'svlan_start': 1, 'mac': '00:11:11:11:00:01', 'circuit_id_start': 100, 'num_sessions': 10}

        result1 = {'handles': 'host3', 'procName': 'sth::pppox_config', 'handle': 'host3', 'status': '1', 'pppoe_session': 'pppoeclientblockconfig1', 'port_handle': 'port1', 'pppoe_port': 'pppoxportconfig1'}
        result2 = 'ethiiif7'
        result3 = str()
        result4 = "pppoxclientblockconfig"
        rthandle.invoke.side_effect =[result1, result2, result3, result4]
        self.assertIsInstance(tester.add_pppoe_client(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_pppox_wildcard API 
    #........................................................#
    def test_set_pppox_wildcard(self):
        test_args = {'auth_mode': 'PAP', 'username':'test', 'password':'test', 'agent_circuit_id':'ACI', 'agent_remote_id':'ARI'}

        result1 = "return"
        rthandle.invoke.side_effect =[result1]
        pppox_handle = 'pppoxclientblockconfig1'
        self.assertIsInstance(tester.set_pppox_wildcard(rthandle, pppox_handle, **test_args), str)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for get_pppoe_config API 
    #........................................................#
    def test_get_pppoe_config(self):
        test_args = {'num_sessions':1, 'vlan_start':1, 'svlan_start':1, 'auth_req_timeout':1, 'echo_req':1, 'ip_type': 'ipv4', 'ipcp_req_timeout':1, 'max_auth_req':1, 'max_padi_req':1, 'max_padr_req':1, 'max_ipcp_retry':1, 'max_terminate_req':1, 'echo_req_interval':1, 'auth_mode':'PAP', 'agent_circuit_id':'ACI', 'agent_remote_id':'ARI'}
        result1 = (str)
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.get_pppoe_config(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for pppoe_client_action API 
    #........................................................#
    def test_pppoe_client_action(self):
        # Test 1
        test_args = {'action':'start', 'handle':'pppoxclientblockconfig1',}
        result1 = 'host1'
        result2 = {'status':1}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.pppoe_client_action(rthandle, **test_args), dict)
        # Test 2 
        test_args = {'action':'start', 'handle':['pppoxclientblockconfig1'],}
        result1 = 'host1'
        result2 = {'status':1}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.pppoe_client_action(rthandle, **test_args), dict)
        # Test 3
        test_args = {'action':'stop', 'handle':'pppoxclientblockconfig1',}
        result1 = 'host1'
        result2 = {'status':1}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.pppoe_client_action(rthandle, **test_args), dict)
        # Test 4
        test_args = {'action':'restart', 'handle':'pppoxclientblockconfig1',}
        result1 = 'host1'
        result2 = {'status':1}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.pppoe_client_action(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_pppoe_rate API 
    #........................................................#
    def test_set_pppoe_rate(self):
        test_args = {'login_rate':[10], 'logout_rate':[10], 'outstanding':[100], 'handle':'pppoxclientblockconfig1'}
        result1 = 'host1'
        result2 = {'status':1}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.set_pppoe_rate(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for pppoe_client_stats API 
    #........................................................#
    def test_pppoe_client_stats(self):
        test_args = {}
        result1 = dict()
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.pppoe_client_stats(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for add_link API
    #........................................................#
    def test_add_link(self):
        test_args = {'port':'2/1', 'count':1, 'mtu':1500, 'vlan_start':1, 'vlan_step':1, 'vlan_count':1, 'vlan_id':1, 'vlan_id_step':1, 'vlan_id_count':1, 'svlan_start':1, 'svlan_step':1, 'svlan_count':1, 'svlan_id':1, 'vlan_user_priority':1, 'ip_addr':'1.1.1.2', 'ip_addr_step':'0.0.0.1', 'gateway':'1.1.1.1', 'netmask':'24', 'ipv6_addr':'2001::2', 'ipv6_gateway':'2001::1', 'gre_dst_ip':'20.1.1.2', 'gre_dst_ip':'30.1.1.2',}

        result1 = {'status':'1', 'handles':'host1'}
        result7 = 'ethiiif1'
        result2 = 'ipv4if1'
        result3 = 'ipv6if1 ipv6if2'
        result4 = str()
        result5 = {'status':'1', 'handles':'host2'}
        result6 = {'status':'1', 'gre_handle':'host2'}
        rthandle.invoke.side_effect =[result1, result7, result2, result3, result4, result5, result6]
        self.assertIsInstance(tester.add_link(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for  add_traffic API
    #........................................................#
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.get_endpoint_handles', return_value =  ['host1'])
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.port_emulation_map', return_value =  {'port1':'host1'})
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.create_streamblock', return_value =  {'status':'1', 'stream_id':'streamblock1'})
    def test_add_traffic(self,patch_get_endpoint_handles, patch_port_emulation_map, patch_create_streamblock):
        test_args = {'port':'2/1', 'name':'unitTest', 'l3_length':256, 'transmit_mode':'burst', 'pkts_per_burst':10, 'line_rate':10, 'burst_rate':'35%', 'frame_size':'256', 'rate':10, 'source':'pppclientblockconfig1', 'type':'ipv4', 'destination':'host2', 'ip_precedence': 2, 'ip_precedence_mode':'incr', 'ip_precedence_step':1, 'ip_precedence_count':10, 'ip_dscp':2, 'ip_dscp_step':1, 'ip_dscp_count':10, 'tcp_dst_port':'1000', 'tcp_dst_port_step':1, 'tcp_dst_port_count':1, 'tcp_src_port':1001, 'tcp_src_port_step':1, 'tcp_src_port_count':1, 'udp_dst_port':1000, 'udp_dst_port_step':1, 'udp_dst_port_count':1, 'udp_src_port':1000, 'udp_src_port_step':1, 'udp_src_port_count':1, }
   
        result4 = str()
        rthandle.invoke.side_effect =[result4]
        self.assertIsInstance(tester.add_traffic(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_traffic API
    #........................................................#
    def test_set_traffic(self):
        test_args = {'stream_id':'streamblock1', 'port':'port1', 'source':'host1', 'destination':'host2', 'rate':'10%', 'frame_size':[100, 200, 10], }
        result4 = {'status':'1'}
        rthandle.invoke.side_effect =[result4]
        self.assertIsInstance(tester.set_traffic(rthandle, **test_args), str)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for traffic_action API
    #........................................................#
    def test_traffic_action(self):
        test_args = {'handle':'unitTestv4','enable_arp':1, 'action':'run', 'duration':30, }
        result1 = 'ipv6'
        result2 = str() 
        result3 = str() 
        result4 = str() 
        result5 = str() 
        result6 = {'status':'1'}
        rthandle.stream_name_map={'unitTestv4':['streamblock1']}
        rthandle.invoke.side_effect =[result1, result2, result3, result4, result5, result6]
        self.assertIsInstance(tester.traffic_action(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None


    #........................................................#
    # Unit test for start_all API
    #........................................................#
    def test_start_all(self):
        test_args = {}
        rthandle.ancp_handle = []
        result = str()
        rthandle.invoke.side_effect =[result, result, result]
        self.assertIsInstance(tester.start_all(rthandle, **test_args), str)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for stop_all API
    #........................................................#
    def test_stop_all(self):
        test_args = {}
        rthandle.ancp_handle = []
        result1 = "ESTABLISHED"
        result = str()
        rthandle.invoke.side_effect =[result1, result, result1, result, result]
        self.assertIsInstance(tester.stop_all(rthandle, **test_args), str)
        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for add_dhcp_server API
    #........................................................#
    def test_add_dhcp_server(self):
        # Test 1
        test_args = {'handle':'ipv4if1', 'lease_time':10, 'pool_start_addr':'32.1.1.1', 'pool_mask_length':24, 'pool_size':100, 'pool_gateway':'32.1.1.1', }

        rthandle.dhcpv4_server_handle = list()
        result1 = "host1"
        result2 = {'status':'1', 'handle':{'dhcp_handle':'host1'}}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.add_dhcp_server(rthandle, **test_args),dict)

        # Test 2
        test_args = {'handle':'ipv6if1', 'dhcpv6_ia_type':'IANA', 'pool_start_addr':'2001::2', 'pool_mask_length':128, 'pool_size':100, 'pool_prefix_start':'1000::2', 'pool_prefix_length':128, 'pool_prefix_size':100, }
        rthandle.dhcpv6_server_handle = list()
        result1 = "host1"
        result2 = {'status':'1', 'handle':{'dhcpv6_handle':'host1'}}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.add_dhcp_server(rthandle, **test_args),dict)

        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_dhcp_server API
    #........................................................#
    def test_set_dhcp_server(self):
        test_args = {}
        result2 = {'status':'1', 'handle':{'dhcpv6_handle':'host1'}}
        rthandle.invoke.side_effect =[result2]
        self.assertIsInstance(tester.set_dhcp_server(rthandle, **test_args),str)

        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for dhcp_server_action API
    #........................................................#
    def test_dhcp_server_action(self):
        # Test 1
        test_args = {'handle':'host1', 'action':'stop',}
        result1 = 'dhcpv6serverconfig'
        result2 = {'status':'1'}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.dhcp_server_action(rthandle, **test_args),str)

        # Test 2
        test_args = {'handle':'host1', 'action':'reset',}
        result1 = 'dhcpv6serverconfig'
        result2 = {'status':'1'}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.dhcp_server_action(rthandle, **test_args),str)

        # Test 3
        test_args = {'handle':'host1', 'action':'stop',}
        result1 = 'dhcpv4serverconfig'
        result2 = {'status':'1'}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.dhcp_server_action(rthandle, **test_args),str)

        # Test 4
        test_args = {'handle':'host1', 'action':'reset',}
        result1 = 'dhcpv4serverconfig'
        result2 = {'status':'1'}
        rthandle.invoke.side_effect =[result1, result2]
        self.assertIsInstance(tester.dhcp_server_action(rthandle, **test_args),str)

        rthandle.invoke.side_effect = None
    

    #........................................................#
    # Unit test for emulation_ancp_subscriber_lines_config API
    #........................................................#
    #def test_emulation_ancp_subscriber_lines_config(self):
    #    test_args = {'circuit_id': 'DTAG_ACI.0100.000000000055100', 'actual_rate_downstream': 300, 'actual_rate_upstream': 300, 'tlv_customer_vlan_id': 1, 'mode': 'create', 'ancp_client_handle': 'router1', 'handle': 'host1', 'data_link': 'ethernet', 'dsl_type': 'adsl2_plus', 'subscriber_lines_per_access_node': 1, 'tlv_service_vlan_id': 1}
    #    result1 = "hDslLineProfile"
    #    result2 = "hTlv"
    #    result3 = "origFrameConfig"
    #    result4 = str()
    #    rthandle.invoke.side_effect =[result1, result2,result3, result4, result3, result4,result3, result4,]
    #    self.assertIsInstance(tester.emulation_ancp_subscriber_lines_config(rthandle, **test_args), int)

    #   rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_pppoe_dsl_attribute API
    #........................................................#
    def test_set_pppoe_dsl_attribute(self):
        test_args = {'handle': 'pppoeclientblockconfig1', 'downstream_rate': '55000', 'upstream_rate': '52000', 'dsltype': 'adsl_2_p'}
        result1 = ''
        result = str()
        rthandle.invoke.side_effect =[result1, result, result,result,result,result, result,result]
        self.assertIsInstance(tester.set_pppoe_dsl_attribute(rthandle, **test_args), int)

        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for ancp_action API
    #........................................................#
    def test_ancp_action(self):
        # Test 1
        test_args = {'handle':'host1', 'action':'start'}
        result1 = {'status': '1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.ancp_action(rthandle, **test_args),dict)

        # Test 2
        test_args = {'handle':'host1', 'action':'stop'}
        result1 = {'status': '1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.ancp_action(rthandle, **test_args),dict)

        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for ancp_line_action API
    #........................................................#
    def test_ancp_line_action(self):
        # Test 1
        test_args = {'handle':'host1', 'action':'flap_start'}
        result1 = {'status': '1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.ancp_line_action(rthandle, **test_args),dict)

        # Test 2
        test_args = {'handle':'host1', 'action':'flap_stop'}
        result1 = {'status': '1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.ancp_line_action(rthandle, **test_args),dict)

        # Test 3
        test_args = {'handle':'host1', 'action':'flap_start_resync'}
        result1 = {'status': '1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.ancp_line_action(rthandle, **test_args),dict)

        # Test 4
        test_args = {'handle':'host1', 'action':'port_up'}
        result1 = {'status': '1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.ancp_line_action(rthandle, **test_args),dict)

        # Test 5
        test_args = {'handle':'host1', 'action':'port_down'}
        result1 = {'status': '1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.ancp_line_action(rthandle, **test_args),dict)

        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_v6_option API
    #........................................................#
    def test_set_v6_option(self):
        test_args={'handle':'ipv6if1', 'interface_id':'interface_id', 'interface_id_start':1, 'v6_remote_id':'v6_remote_id', 'v6_remote_id_start':1, 'enterprise_id':'enterprise_id', }
        result1 = str()
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.set_v6_option(rthandle, **test_args), str)

        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_option_82 API
    #........................................................#
    def test_set_option_82(self):
        test_args={'handle':'host1', 'circuit_id':'circuit_id', 'circuit_id_start':1, 'remote_id':'remote_id', 'remote_id_start':1, }
        result1 = str()
        rthandle.invoke.side_effect =[result1]
        rthandle.remote_id = dict()
        rthandle.circuit_id = dict()
        self.assertIsInstance(tester.set_option_82(rthandle, **test_args), str)

        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for add_dhcp_client API
    #........................................................#
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.set_v6_option', return_value =  {'status': '1'})
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.set_vlan', return_value =  {'status': '1'})
    @patch('jnpr.toby.trafficgen.spirent.spirenttester.set_option_82', return_value =  1)
    def test_add_dhcp_client(self, patch_set_v6_option, patch_set_vlan, patch_set_option_82):
        test_args={'port':'2/1', 'ip_type':'dual', 'vlan_start':1, 'svlan_start':1, 'dhcp4_broadcast':1, 'rapid_commit':'1', 'dhcpv6_ia_type':'IANA_IAPD', 'home_gw_ipv6':'1.1.1.1', 'softgre':1, 'gre_dst_ip':'1.1.1.1', 'gre_local_ip':'1.1.1.2', 'gre_gateway':'1.1.1.1', 'gre_vlan_id':1, 'gre_netmask':'255.255.255.0'}

        result1 = {'status':'1', 'handle':'host1', 'key':'1'}
        result2 = 'ethiiif1'
        #result3 = 'dhcpv4blockconfig1'
        result4 = {'status':'1', 'handles':'host1', 'handle':'host1', 'dhcpv6_handle': 'dhcpv6blockconfig1', 'key':'2'}
        result5 = {'status':'1', 'handle':'host2', 'dhcpv6_handle': 'dhcpv6blockconfig1', 'key':'3'}
        result6 = str()
        result7 = {'status':'1', 'key':'4'}
        result8 = {'status':'1', 'key':'5'}
        result9 = {'status':'1', 'key':'6'}
        
        rthandle.invoke.side_effect =[result1,result2,result4,result5,result6,result7, result8, result9]
        self.assertIsInstance(tester.add_dhcp_client(rthandle, **test_args), dict)

        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_dhcp_client API
    #........................................................#
    def test_set_dhcp_client(self):
        # Test 1
        test_args = {'handle':'host1v4', 'login_rate':1, 'logout_rate':2, 'outstanding':3, 'msg_timeout':4, 'retry_count':5, }
        result1 = {'status':'1', 'handle':'host1', 'key':'1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.set_dhcp_client(rthandle, **test_args), str)

        # Test 2
        test_args = {'handle':'host1v6', 'login_rate':1, 'logout_rate':2, 'outstanding':3, 'msg_timeout':4, 'retry_count':5, }
        result1 = {'status':'1', 'handle':'host1', 'key':'1'}
        rthandle.invoke.side_effect =[result1]
        self.assertIsInstance(tester.set_dhcp_client(rthandle, **test_args), str)

        rthandle.invoke.side_effect = None

    #........................................................#
    # Unit test for set_dhcp_rate API
    #........................................................#
    def test_set_dhcp_rate(self):
        # Test 1
        test_args = {'handle':'host1v4', 'login_rate':[1], 'logout_rate':[1], 'outstanding':[1], 'msg_timeout':[1], 'retry_count':[1], }
        result1 = "host1"
        result2 = "port1"
        result3 = str()
        result4 = dict()
        rthandle.invoke.side_effect =[result1,result2,result3, result4]
        self.assertIsInstance(tester.set_dhcp_rate(rthandle, **test_args), dict)

        # Test 2
        test_args = {'handle':'host1v6', 'login_rate':[1], 'logout_rate':[1], 'outstanding':[1], 'msg_timeout':[1], 'retry_count':[1], }
        result1 = "host1"
        result2 = "port1"
        result3 = str()
        result4 = dict()
        rthandle.invoke.side_effect =[result1,result2,result3, result4]
        self.assertIsInstance(tester.set_dhcp_rate(rthandle, **test_args), dict)
        rthandle.invoke.side_effect = None

if __name__ == '__main__':
    #SUITE = unittest.TestLoader().loadTestsFromTestCase(TestIxiaTester)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)
    unittest.main()
