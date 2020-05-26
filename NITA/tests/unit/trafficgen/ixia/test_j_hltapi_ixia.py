

import unittest
from mock import patch, MagicMock
from jnpr.toby.trafficgen.ixia.j_hltapi_ixia import *

#
# Auto-generated Dummy UT test file for Ixia VA code 
#
class JHltapiIxia(unittest.TestCase):

    def test_j_emulation_igmp_info(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_igmp_info(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_connect(self):
       import builtins
       builtins.t = MagicMock()
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = None
       t.Initialize.return_value = None
       self.assertEqual(j_connect(rt_handle), None)
    
    def test_j_emulation_ldp_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_ldp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_bfd_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_bfd_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_ldp_route_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_ldp_route_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_multicast_source_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_multicast_source_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_igmp_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_igmp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dhcp_server_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       #handle = MagicMock()
       handle = "/dummy/"
       self.assertEqual(j_emulation_dhcp_server_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_ospf_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_ospf_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_l2tp_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       #handle = MagicMock()
       handle = "/dummy/"
       self.assertEqual(j_l2tp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_isis_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_isis_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_igmp_group_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_igmp_group_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dhcp_group_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = 'handle'
       self.assertRaises(ValueError, j_emulation_dhcp_group_config, rt_handle, handle=handle, mode='create')
    
    def test_j_emulation_pim_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_pim_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_cleanup_session(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'status' : '1'}
       self.assertEqual(j_cleanup_session(rt_handle), {'status' : '1'})
    
    def test_j_pppox_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       #handle = MagicMock()
       handle = "/dummy/"
       self.assertEqual(j_pppox_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_mld_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_mld_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dhcp_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_dhcp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_rsvp_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_rsvp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_isis_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_isis_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_bfd_info(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_bfd_info(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dhcp_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_dhcp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_mld_group_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_mld_group_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_igmp_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_igmp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_traffic_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       self.assertEqual(j_traffic_control(rt_handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_rsvp_info(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_rsvp_info(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_bgp_route_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'ip_routes' : '1'}
       handle = MagicMock()
       self.assertEqual(j_emulation_bgp_route_config(rt_handle, handle=handle), {'ip_routes' : '1'})
    
    def test_j_l2tp_stats(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_l2tp_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_pim_group_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_pim_group_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dhcp_stats(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_dhcp_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_mld_info(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_mld_info(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_bgp_info(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_bgp_info(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_pppox_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_pppox_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_bfd_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_bfd_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_rsvp_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_rsvp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dhcp_server_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_dhcp_server_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_bgp_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_bgp_config(rt_handle, handle=handle, mode='create'), {'port' : {'status' : 1}})
    
    def test_j_emulation_isis_info(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_isis_info(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_ospf_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_ospf_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_bgp_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_bgp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_traffic_stats(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       self.assertEqual(j_traffic_stats(rt_handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_igmp_querier_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_igmp_querier_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dhcp_server_stats(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_dhcp_server_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_pim_info(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_pim_info(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_pppox_stats(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_pppox_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_ldp_info(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_ldp_info(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_l2tp_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_l2tp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_ldp_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_ldp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_pim_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_pim_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_rsvpte_tunnel_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_rsvpte_tunnel_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_mld_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_mld_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_multicast_group_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_multicast_group_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_rsvp_tunnel_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_rsvp_tunnel_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_traffic_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       self.assertRaises(KeyError, j_emulation_dhcp_group_config, rt_handle)
    
    def test_j_pppox_server_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       self.assertEqual(j_pppox_server_config(rt_handle, handle='dummy/handle'), {'port' : {'status' : 1}})
    
    def test_j_pppox_server_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_pppox_server_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_pppox_server_stats(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_pppox_server_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_lacp_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_lacp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_lacp_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_lacp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_lacp_info(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_lacp_info(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_arp_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port': {'status' : 1}}
       rt_handle._invokeIxNet.return_value = '''
       <learnResults>
         <trafficSet endpointName="cpf.Topology 1.Device Group 1.IPv4 1.1/16/1">
           <dst_mac>
             <multiValue format="mac" length="48">
                 <counter id="">
                 <value name="startValue">00:12:01:00:00:01</value>
                 <value name="stepValue">00:00:00:00:00:00</value>
                 <value name="stepCount">1</value>
                 <value name="increment">True</value>
                 </counter>
             </multiValue>
           </dst_mac>
         </trafficSet>
       </learnResults>
       '''
       handle = "traffic/trafficItem:1"
       self.assertEqual(j_arp_control(rt_handle, stream_handle=handle), {'status' : 1, 'arpnd_status': 1})
    
    def test_j_emulation_ptp_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = '/topology:1/deviceGroup:1/ethernet:1/ipv4:1'
       self.assertEqual(j_emulation_ptp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_ptp_stats(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = '/topology:1/deviceGroup:1/ethernet:1/ipv4:1'
       self.assertEqual(j_emulation_ptp_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dot1x_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_dot1x_control(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dot1x_stats(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = '/topology:1/deviceGroup:1/ethernet:1/ipv4:1'
       self.assertEqual(j_emulation_dot1x_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})
    
    def test_j_emulation_dot1x_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'dotonex_device_handle' : '/dotonex:1', 'status': 1}
      handle = MagicMock()
      ret = {'dotonex_device_handle': '/dotonex:1', 'handles': '/dotonex:1', 'status': 1}
      self.assertEqual(j_emulation_dot1x_config(rt_handle, handle=handle, mode='create'), ret)


    def test_j_emulation_ipv6_autoconfig(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       self.assertEqual(j_emulation_ipv6_autoconfig(rt_handle, handle='/ipv6auto:1', mode='modify'), {'port' : {'status' : 1}})

    def test_j_emulation_ipv6_autoconfig_control(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_ipv6_autoconfig_control(rt_handle, handle=handle, action='start'), {'port' : {'status' : 1}})
    
    def test_j_emulation_ipv6_autoconfig_stats(self):
       rt_handle = MagicMock()
       rt_handle._invokeIxNet.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_ipv6_autoconfig_stats(rt_handle, handle=handle, action='clear'), {'port' : {'status' : 1}})
    
    def test_j_emulation_ptp_config(self):
       rt_handle = MagicMock()
       rt_handle.invoke.return_value = {'port' : {'status' : 1}}
       handle = MagicMock()
       self.assertEqual(j_emulation_ptp_config(rt_handle, handle=handle, transport_type='ipv4'), {'port' : {'status' : 1}})

if __name__ == '__main__':
    unittest.main()
