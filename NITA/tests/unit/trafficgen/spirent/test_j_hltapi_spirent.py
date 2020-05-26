import unittest
from mock import patch, MagicMock
from jnpr.toby.trafficgen.spirent.j_hltapi_spirent import *

#
# Auto-generated Dummy UT test file for Spirent VA code 
#
class JHltapiSpirent(unittest.TestCase):

   def test_j_emulation_igmp_info(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
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
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_ldp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_bfd_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_bfd_control(rt_handle, handle=handle), [{'port' : {'status' : 1}}])

   def test_j_emulation_ldp_route_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_ldp_route_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_multicast_source_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_multicast_source_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_igmp_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_igmp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_dhcp_server_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_dhcp_server_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_ospf_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_ospf_config(rt_handle, handle=handle), {'handles' : 'ospf_1','port' : {'status' : 1}})

   def test_j_l2tp_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_l2tp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_isis_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_isis_config(rt_handle, handle=handle), {'handles' : 'isis_1','port' : {'status' : 1}})

   def test_j_emulation_igmp_group_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_igmp_group_config(rt_handle, handle=handle), {'handles': 'igmp_group_1', 'port' : {'status' : 1}})

   def test_j_emulation_dhcp_group_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_dhcp_group_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_pim_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_pim_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_cleanup_session(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'status' : '1'}
      self.assertEqual(j_cleanup_session(rt_handle), {'status' : '1'})

   def test_j_pppox_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_pppox_config(rt_handle, handle=handle), {'handles' : 'ppp_1','port' : {'status' : 1}})

   def test_j_emulation_mld_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_mld_config(rt_handle, handle=handle), {'handles' : 'mld_1','port' : {'status' : 1}})

   def test_j_emulation_dhcp_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_dhcp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_rsvp_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_rsvp_config(rt_handle, handle=handle), {'handles' : 'rsvp_1','port' : {'status' : 1}})

   def test_j_emulation_isis_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_isis_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_bfd_info(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_bfd_info(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_dhcp_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_dhcp_control(rt_handle, handle=handle,action='start'), {'port' : {'status' : 1}})

   def test_j_emulation_mld_group_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_mld_group_config(rt_handle, handle=handle), {'handles': 'mld_group_1','port' : {'status' : 1}})

   def test_j_emulation_igmp_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_igmp_config(rt_handle, handle=handle), {'handles': 'igmp_1','port' : {'status' : 1}})

   def test_j_traffic_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      self.assertEqual(j_traffic_control(rt_handle), {'port' : {'status' : 1}})

   def test_j_emulation_rsvp_info(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_rsvp_info(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_bgp_route_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_bgp_route_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_l2tp_stats(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_l2tp_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_pim_group_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_pim_group_config(rt_handle, handle=handle), {'handles': 'pim_group_1','port' : {'status' : 1}})

   def test_j_emulation_dhcp_stats(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_dhcp_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_mld_info(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_mld_info(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_bgp_info(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_bgp_info(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_pppox_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_pppox_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_bfd_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_bfd_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_rsvp_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_rsvp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_dhcp_server_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_dhcp_server_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_bgp_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_bgp_config(rt_handle, handle=handle), {'handles': 'bgp_1','port' : {'status' : 1}})

   def test_j_emulation_isis_info(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_isis_info(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_ospf_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_ospf_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_bgp_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_bgp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_traffic_stats(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      self.assertEqual(j_traffic_stats(rt_handle), {'port': {'status': 1}, 'traffic_item': {}})

   def test_j_emulation_igmp_querier_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_igmp_querier_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_dhcp_server_stats(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_dhcp_server_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_pim_info(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_pim_info(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_pppox_stats(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_pppox_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_ldp_info(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_ldp_info(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_l2tp_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_l2tp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_ldp_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_ldp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_pim_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_pim_config(rt_handle, handle=handle), {'handles' : 'pim_1','port' : {'status' : 1}})

   def test_j_emulation_rsvpte_tunnel_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_rsvpte_tunnel_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_mld_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_mld_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_multicast_group_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_multicast_group_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_rsvp_tunnel_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_rsvp_tunnel_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_traffic_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      self.assertEqual(j_traffic_config(rt_handle), {'port' : {'status' : 1}})

   def test_j_pppox_server_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_pppox_server_config(rt_handle, handle=handle), {'handles' : 'pppox_1','port' : {'status' : 1}})

   def test_j_pppox_server_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_pppox_server_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_pppox_server_stats(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_pppox_server_stats(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_lacp_config(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_lacp_config(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_lacp_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_lacp_control(rt_handle, handle=handle), {'port' : {'status' : 1}})

   def test_j_emulation_lacp_info(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_emulation_lacp_info(rt_handle, handle=handle), {'aggregate': {'port': {'status': 1}}, 'port': {'status': 1}})

   def test_j_arp_control(self):
      rt_handle = MagicMock()
      rt_handle.invoke.return_value = {'port' : {'status' : 1}}
      handle = MagicMock()
      global_config[handle] = ['handle1']
      self.assertEqual(j_arp_control(rt_handle, stream_handle=handle), {'port' : {'status' : 1}})
