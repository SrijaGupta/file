#!/usr/local/python-3.4.5/bin/python3

#
# This is HLTAPI common parameters data
# please note that this data is used to validate j_hltapi_ixia.py and j_hltapi_spirent.py using an external script.
# please do NOT forget to update this file whenever you add/delete any parameter for any API under j_hltapi_ixia.py and j_hltapi_spirent.py.
#

j_emulation_isis_control = {
      'handle', 'port_handle', 'mode', 'withdraw', 
      'advertise', 'flap_count', 'flap_down_time', 
      'flap_interval_time', 'flap_routes'  } 

j_emulation_isis_config = {
      'bfd_registration', 'handle', 
      'gateway_ip_addr', 'area_id', 'gateway_ip_addr_step', 
      'atm_encapsulation', 'gateway_ipv6_addr', 'count', 
      'gateway_ipv6_addr_step', 
      'graceful_restart_restart_time', 
      'graceful_restart', 'multi_topology', 'hello_interval', 
      'psnp_interval', 'intf_type', 'router_id', 'intf_ip_addr', 
      'router_id_step', 'intf_ip_addr_step', 'system_id', 
      'intf_ip_prefix_length', 'system_id_step', 
      'intf_ipv6_addr', 'te_max_bw', 'intf_ipv6_addr_step', 
      'te_max_resv_bw', 'intf_ipv6_prefix_length', 
      'te_unresv_bw_priority0', 'intf_metric', 
      'te_unresv_bw_priority1', 'ip_version', 
      'te_unresv_bw_priority2', 'lsp_refresh_interval', 
      'te_unresv_bw_priority3', 'overloaded', 
      'te_unresv_bw_priority4', 'routing_level', 
      'te_unresv_bw_priority5', 'te_enable', 
      'te_unresv_bw_priority6', 'te_router_id', 
      'te_unresv_bw_priority7', 'te_router_id_step', 
      'vlan_cfi', 'vci', 'vci_step', 'vlan', 'vlan_id', 'vlan_id_mode', 
      'vlan_user_priority', 'vpi', 'vpi_step', 'wide_metrics'  } 

j_emulation_igmp_control = {
      'handle'  } 

j_pppox_config = {
      'protocol', 'ac_select_mode', 'attempt_rate', 
      'wildcard_pound_start', 'auth_mode', 
      'wildcard_pound_end', 'username_wildcard', 
      'wildcard_question_start', 'password_wildcard', 
      'wildcard_question_end', 'auth_req_timeout', 
      'dut_assigned_src_addr', 'disconnect_rate', 
      'echo_req', 'intermediate_agent', 'include_id', 'mac_addr', 
      'local_magic', 'mac_addr_step', 'max_auth_req', 'max_padi_req', 
      'max_padr_req', 'padi_include_tag', 'padi_req_timeout', 
      'padr_include_tag', 'padr_req_timeout', 'qinq_incr_mode', 
      'term_req_timeout', 'vpi', 'vpi_count', 'pvc_incr_mode', 
      'vlan_id', 'vlan_user_priority', 'vlan_id_outer', 'username', 
      'password', 'port_handle', 'mode', 'ip_cp', 'service_name'  } 

j_emulation_oam_info = {
      'mode', 'action'  } 

j_emulation_pim_info = {
      'handle'  } 

j_emulation_mld_group_config = {
      'session_handle', 'group_pool_handle', 
      'handle', 'source_pool_handle', 'mode'  } 

j_emulation_rip_control = {
      'mode', 'flap_count', 'flap_interval_time'  } 

j_emulation_bgp_config = {
      'active_connect_enable', 'handle', 
      'bfd_registration', 'hold_time', 'count', 'local_as_step', 
      'graceful_restart_enable', 'local_as4', 
      'restart_time', 'local_addr_step', 'ip_version', 
      'local_router_id', 'ipv4_mpls_nlri', 'md5_key', 
      'ipv4_mpls_vpn_nlri', 'next_hop_ip', 
      'ipv4_multicast_nlri', 'remote_addr_step', 
      'ipv4_unicast_nlri', 'retry_time', 'ipv6_mpls_nlri', 
      'routes_per_msg', 'ipv6_mpls_vpn_nlri', 'vlan_cfi', 
      'ipv6_multicast_nlri', 'route_refresh', 
      'ipv6_unicast_nlri', 'local_as_mode', 'local_ip_addr', 
      'local_ipv6_addr', 'mac_address_start', 'md5_enable', 
      'netmask', 'remote_ip_addr', 'remote_ipv6_addr', 
      'staggered_start_enable', 'vci', 'vci_step', 
      'vlan_id', 'vlan_id_mode', 'vlan_user_priority', 'vpi', 'vpi_step', 
      'local_router_id_step', 'stale_time', 'vpls_nlri'  } 

j_l2tp_config = {
      'l2tp_src_addr', 'port_handle', 'l2tp_src_step', 
      'l2tp_dst_count', 'l2tp_dst_addr', 'sessions_per_tunnel', 
      'l2tp_dst_step', 'avp_framing_type', 'udp_src_port', 
      'avp_hide_list', 'attempt_rate', 'avp_tx_connect_speed', 
      'auth_mode', 'domain_group_map', 'username_wc', 'echo_req', 
      'password_wc', 'hello_req', 'wildcard_pound_start', 'hostname', 
      'wildcard_pound_end', 'ppp_server_step', 
      'wildcard_question_start', 'secret', 
      'wildcard_question_end', 'vpi', 'wildcard_bang_end', 
      'wildcard_bang_start', 'wildcard_dollar_end', 
      'wildcard_dollar_start', 'auth_req_timeout', 
      'max_auth_req', 'echo_req_interval', 'enable_magic', 
      'hostname_wc', 'ppp_client_ip', 'ppp_client_step', 
      'ppp_server_ip', 'pvc_incr_mode', 'redial_timeout', 'rws', 
      'secret_wc', 'session_id_start', 'terminate_req_timeout', 
      'tunnel_id_start', 'vlan_user_priority', 'l2_encap', 
      'username', 'password', 'redial'  } 

j_emulation_rsvp_info = {
      'mode'  } 

j_emulation_ldp_control = {
      'handle', 'mode'  } 

j_emulation_rsvp_control = {
      'port_handle', 'mode'  } 

j_emulation_rip_config = {
      'intf_prefix_length', 'count', 'md5_key_id', 
      'router_id', 'vci', 'router_id_step', 'vlan_id', 'vlan_id_mode', 
      'vlan_user_priority', 'vpi', 'intf_ip_addr', 
      'intf_ip_addr_step', 'neighbor_intf_ip_addr', 
      'neighbor_intf_ip_addr_step', 'mode', 
      'send_type', 'session_type'  } 

j_traffic_config = {
      'mac_dst', 'stream_id', 'mac_src', 
      'emulation_src_handle', 'vci', 'emulation_dst_handle', 
      'vlan_cfi', 'inter_stream_gap', 'vlan_user_priority', 
      'bidirectional', 'arp_dst_hw_addr', 'mac_dst_count', 
      'ip_dscp', 'mac_dst_step', 'ip_dst_step', 'mac_src_count', 
      'ip_fragment', 'mac_src_step', 'ip_fragment_offset', 
      'l3_imix1_ratio', 'ip_id', 'l3_imix1_size', 'ip_precedence', 
      'l3_imix2_ratio', 'ip_protocol', 'l3_imix2_size', 
      'ip_src_addr', 'l3_imix3_ratio', 'ip_src_step', 
      'l3_imix3_size', 'ipv6_dst_addr', 'l3_imix4_ratio', 
      'ipv6_flow_label', 'l3_imix4_size', 'ipv6_hop_limit', 
      'vlan_id_step', 'ipv6_next_header', 'arp_src_hw_count', 
      'ipv6_src_addr', 'arp_dst_hw_count', 'ipv6_traffic_class', 
      'ip_checksum', 'tcp_src_port', 'ip_dscp_step', 'tcp_dst_port', 
      'ip_dscp_count', 'tcp_urgent_ptr', 'ip_dst_addr', 
      'tcp_window', 'ipv6_dst_step', 'tcp_ack_flag', 'ipv6_src_step', 
      'tcp_fin_flag', 'tcp_reserved', 'tcp_psh_flag', 
      'icmp_checksum', 'tcp_rst_flag', 'igmp_group_step', 
      'tcp_syn_flag', 'igmp_msg_type', 'tcp_urg_flag', 'igmp_type', 
      'udp_dst_port', 'igmp_version', 'udp_src_port', 'rate_bps', 
      'udp_checksum', 'rate_pps', 'icmp_code', 'pkts_per_burst', 
      'icmp_id', 'mpls_labels', 'icmp_seq', 'icmp_type', 
      'igmp_group_addr', 'igmp_group_count', 
      'igmp_multicast_src', 'igmp_qqic', 'igmp_qrv', 
      'igmp_s_flag', 'burst_loop_count', 'arp_src_hw_addr', 
      'arp_src_hw_mode', 'arp_dst_hw_mode', 'arp_operation', 
      'ipv6_frag_id', 'ipv6_frag_more_flag', 'tcp_ack_num', 
      'rate_percent', 'mode', 'port_handle', 'port_handle2', 
      'mac_dst_mode', 'mac_src_mode', 'l2_encap', 'length_mode', 
      'vlan_id_mode', 'l3_protocol', 'ip_dst_mode', 'ip_src_mode', 
      'ipv6_dst_mode', 'ipv6_src_mode', 'l4_protocol', 
      'igmp_group_mode', 'transmit_mode'  } 

j_emulation_ospf_config = {
      'area_id', 'intf_ip_addr_step', 
      'area_id_step', 'lsa_retransmit_delay', 'bfd_registration', 
      'option_bits', 'dead_interval', 'router_id_step', 
      'demand_circuit', 'te_admin_group', 'hello_interval', 
      'te_max_bw', 'graceful_restart_enable', 'te_max_resv_bw', 
      'intf_ip_addr', 'te_unresv_bw_priority0', 
      'intf_prefix_length', 'te_unresv_bw_priority1', 
      'router_id', 'te_unresv_bw_priority2', 'router_priority', 
      'te_unresv_bw_priority3', 'session_type', 
      'te_unresv_bw_priority4', 'te_metric', 
      'te_unresv_bw_priority5', 'vci', 
      'te_unresv_bw_priority6', 'vlan_id_mode', 
      'te_unresv_bw_priority7', 'vlan_user_priority', 
      'vci_step', 'vpi', 'vlan_cfi', 'vpi_step', 'mode', 'area_type', 
      'authentication_mode', 'network_type'  } 

j_emulation_bfd_config = {
      'mode', 'intf_ipv6_addr_step', 'count', 
      'intf_ip_addr', 'intf_ip_addr_step', 'intf_ipv6_addr', 'vpi'  } 

j_emulation_igmp_querier_config = {
      'intf_ip_addr', 'handle', 
      'intf_ip_addr_step', 'count', 'intf_prefix_len', 
      'neighbor_intf_ip_addr', 
      'neighbor_intf_ip_addr_step', 'igmp_version', 
      'vlan_id', 'vlan_id_mode', 'vlan_user_priority'  } 

j_emulation_bfd_info = {
      'mode', 'port_handle'  } 

j_emulation_pim_group_config = {
      'rate_control', 
      'join_prune_per_interval', 'rp_ip_addr', 
      'register_per_interval', 'wildcard_group', 
      'register_stop_per_interval', 'mode'  } 

j_emulation_multicast_group_config = {
      'mode', 'handle', 'ip_prefix_len', 
      'ip_addr_start', 'ip_addr_step', 'num_groups'  } 

j_emulation_bgp_control = {
      'link_flap_down_time', 'handle', 
      'link_flap_up_time'  } 

j_connect = {
      'break_locks', 'device', 'sync', 'port_list', 'reset', 
      'timeout', 'username', 'nobios'  } 

j_emulation_dhcp_control = {
      'port_handle', 'handle'  } 

j_emulation_mld_config = {
      'filter_mode', 'handle', 'intf_ip_addr', 
      'general_query', 'intf_ip_addr_step', 'group_query', 
      'intf_prefix_len', 'ip_router_alert', 'mld_version', 
      'max_response_control', 'neighbor_intf_ip_addr', 
      'suppress_report', 'neighbor_intf_ip_addr_step', 
      'vlan_cfi', 'vlan_id', 'vlan_id_mode', 'vlan_user_priority', 
      'mode'  } 

j_emulation_igmp_config = {
      'filter_mode', 'port_handle', 'igmp_version', 
      'handle', 'intf_ip_addr', 'count', 'intf_ip_addr_step', 
      'general_query', 'intf_prefix_len', 'group_query', 
      'ip_router_alert', 'msg_interval', 'neighbor_intf_ip_addr', 
      'older_version_timeout', 
      'neighbor_intf_ip_addr_step', 'robustness', 
      'vlan_id', 'suppress_report', 'vlan_id_mode', 'vlan_cfi', 
      'vlan_user_priority'  } 

j_emulation_dhcp_group_config = {
      'num_sessions', 'handle', 'mac_addr', 
      'dhcp6_range_duid_enterprise_id', 
      'mac_addr_step', 'dhcp6_range_duid_vendor_id', 
      'qinq_incr_mode', 'dhcp6_range_duid_vendor_id_increment', 
      'vci', 'dhcp6_range_ia_t1', 'vpi', 'dhcp6_range_ia_t2', 'vlan_id', 
      'vlan_id_step', 'vlan_id_count', 'vlan_user_priority', 
      'vlan_id_outer', 'vlan_id_outer_step', 'vlan_id_outer_count', 
      'vci_step', 'vpi_step'  } 

j_device_info = {
      'ports', 'fspec_version'  } 

j_emulation_rsvp_config = {
      'bfd_registration', 'refresh_interval', 
      'bundle_msgs', 'srefresh_interval', 'count', 
      'egress_label_mode', 'gateway_ip_addr', 
      'gateway_ip_addr_step', 'graceful_restart', 
      'hello_msgs', 'intf_ip_addr', 'intf_ip_addr_step', 
      'intf_prefix_length', 'max_label_value', 
      'min_label_value', 'neighbor_intf_ip_addr', 
      'neighbor_intf_ip_addr_step', 'record_route', 
      'refresh_reduction', 'reliable_delivery', 'resv_confirm', 
      'summary_refresh', 'vci', 'vci_step', 'vlan_id_mode', 
      'vlan_user_priority', 'vpi', 'vpi_step', 'mode'  } 

j_l2tp_stats = {
      'mode', 'handle'  } 

j_emulation_bgp_info = {
      'handle', 'mode'  } 

j_interface_config = {
      'mode', 'port_handle', 'arp_send_req', 
      'arp_req_retries', 'autonegotiation', 'arp_req_timer', 
      'framing', 'control_plane_mtu', 'gateway', 'dst_mac_addr', 
      'gateway_step', 'internal_ppm_adjust', 'intf_ip_addr', 
      'ipv6_prefix_length', 'ipv6_intf_addr', 'netmask', 
      'ipv6_intf_addr_step', 'rx_equalization', 
      'ipv6_gateway_step', 'tx_preemphasis_main_tap', 
      'phy_mode', 'tx_preemphasis_post_tap', 'vlan', 'vlan_id', 
      'qinq_incr_mode', 'vlan_id_count', 'clocksource', 
      'vlan_id_step', 'intf_ip_addr_step', 'vlan_user_priority', 
      'duplex', 'tx_s1', 'speed', 'transmit_clock_source', 'tx_fcs', 
      'ipv6_gateway', 'src_mac_addr', 'src_mac_addr_step', 
      'intf_mode'  } 

j_emulation_multicast_source_config = {
      'mode', 'handle', 'ip_prefix_len', 
      'ip_addr_start', 'ip_addr_step', 'num_sources'  } 

j_emulation_dhcp_server_stats = {
      'action', 'dhcp_handle', 'ip_version', 
      'port_handle'  } 

j_pppox_control = {
      'action', 'handle'  } 

j_emulation_ospf_control = {
      'mode', 'handle', 'port_handle', 
      'flap_count', 'flap_down_time', 'flap_interval_time', 
      'withdraw_lsa', 'advertise', 'withdraw'  } 

j_emulation_dhcp_server_config = {
      'count', 'port_handle', 'ip_version', 
      'handle', 'local_mac', 'ipaddress_count', 'ip_address', 
      'dhcp_ack_time_offset', 'ip_step', 
      'dhcp_ack_circuit_id', 'ip_prefix_step', 
      'dhcp_ack_remote_id', 'ip_repeat', 
      'dhcp_offer_circuit_id', 'ip_gateway', 
      'dhcp_offer_remote_id', 'ipaddress_pool', 'vlan_id', 
      'ipaddress_increment', 'vlan_id_count', 
      'dhcp_ack_options', 'vlan_id_step', 
      'dhcp_ack_time_server_address', 
      'vlan_user_priority', 'dhcp_offer_options', 
      'remote_mac', 'dhcp_offer_time_offset', 
      'dhcp_offer_router_address', 
      'dhcp_offer_time_server_address', 
      'pvc_incr_mode', 'qinq_incr_mode', 'vpi', 'vpi_count', 
      'vpi_step'  } 

j_emulation_ldp_info = {
      'handle', 'mode'  } 

j_emulation_ldp_route_config = {
      'mode', 'handle', 'fec_ip_prefix_start', 
      'lsp_handle', 'fec_host_addr', 'num_lsps', 
      'fec_host_prefix_length', 'num_routes', 
      'fec_vc_cbit', 'fec_ip_prefix_length', 'fec_vc_count', 
      'fec_ip_prefix_step', 'fec_host_step', 
      'fec_vc_group_id', 'fec_vc_id_start', 'fec_type', 
      'fec_vc_id_step', 'fec_vc_intf_mtu', 'fec_vc_id_count'  } 

j_emulation_dhcp_config = {
      'ip_version', 'msg_timeout', 
      'outstanding_session_count'  } 

j_emulation_pim_config = {
      'bidir_capable', 'count', 'intf_ip_addr', 
      'dr_priority', 'intf_ip_addr_step', 'hello_holdtime', 
      'intf_ip_prefix_len', 'hello_interval', 'ip_version', 
      'join_prune_holdtime', 'neighbor_intf_ip_addr', 
      'join_prune_interval', 'pim_mode', 'port_handle', 
      'prune_delay', 'prune_delay_enable', 'router_id', 
      'router_id_step', 'vlan_id_mode', 'vlan_user_priority', 
      'mode', 'type'  } 

j_emulation_dhcp_server_control = {
      'port_handle', 'dhcp_handle'  } 

j_emulation_igmp_group_config = {
      'handle'  } 

j_emulation_oam_config_msg = {
      'count', 'mac_local_incr_mode', 
      'mac_local', 'mac_local_step', 'mac_remote_repeat', 
      'mac_local_list', 'vlan_id_outer_step', 'mac_remote', 
      'vlan_id_step', 'mac_remote_incr_mode', 'md_level_repeat', 
      'mac_remote_step', 'ttl', 'mac_remote_list', 
      'tlv_sender_chassis_id', 'md_level', 
      'tlv_sender_chassis_id_length', 
      'md_level_incr_mode', 'tlv_org_length', 'md_level_step', 
      'tlv_data_length', 'md_level_list', 'oam_standard', 
      'vlan_outer_id', 'msg_type', 'vlan_id', 
      'tlv_sender_chassis_id_subtype', 
      'tlv_org_value', 'tlv_data_pattern'  } 

j_emulation_rsvpte_tunnel_control = {
      'handle'  } 

j_emulation_bgp_route_config = {
      'atomic_aggregate', 'aggregator', 
      'cluster_list_enable', 'as_path', 'communities_enable', 
      'cluster_list', 'ip_version', 'communities', 'ipv4_mpls_nlri', 
      'local_pref', 'ipv4_mpls_vpn_nlri', 'multi_exit_disc', 
      'ipv4_multicast_nlri', 'netmask', 'ipv4_unicast_nlri', 
      'next_hop', 'ipv6_mpls_nlri', 'prefix', 'ipv6_mpls_vpn_nlri', 
      'prefix_step', 'ipv6_multicast_nlri', 'originator_id', 
      'ipv6_unicast_nlri', 'rd_type', 'max_route_ranges', 
      'rd_admin_step', 'next_hop_set_mode', 'rd_admin_value', 
      'next_hop_ip_version', 'rd_assign_value', 'num_routes', 
      'route_ip_addr_step', 'origin', 'target', 
      'originator_id_enable', 'packing_to', 
      'rd_assign_step', 'target_type', 'target_assign'  } 

j_traffic_stats = {
      'streams', 'port_handle', 'mode'  } 

j_emulation_ospf_topologY_route_config = {
      'grid_router_id', 
      'external_connect', 'grid_router_id_step', 
      'external_prefix_forward_addr', 'link_enable', 
      'external_prefix_length', 'link_intf_addr', 
      'external_prefix_start', 'router_id', 'grid_connect', 
      'grid_connect_session', 'grid_disconnect', 
      'grid_prefix_length', 'grid_prefix_start', 'mode', 
      'grid_prefix_step', 'grid_link_type', 
      'grid_stub_per_router', 'type', 'net_dr', 'net_ip', 
      'net_prefix_length', 'nssa_connect', 
      'nssa_number_of_prefix', 'nssa_prefix_forward_addr', 
      'nssa_prefix_length', 'nssa_prefix_metric', 
      'nssa_prefix_start', 'nssa_prefix_step', 
      'nssa_prefix_type', 'router_abr', 'router_asbr', 
      'router_connect', 'router_disconnect', 'summary_connect', 
      'summary_prefix_length', 'summary_prefix_start', 
      'summary_prefix_step'  } 

j_emulation_oam_config_topologY = {
      'mode', 'handle'  } 

j_emulation_oam_control = {
      'action'  } 

j_traffic_control = {
      'duration', 'action'  } 

j_emulation_ldp_config = {
      'bfd_registration', 'handle', 'count', 
      'egress_label_mode', 'gateway_ip_addr', 'label_start', 
      'gateway_ip_addr_step', 'label_step', 'intf_ip_addr', 
      'mac_address_init', 'intf_ip_addr_step', 'vlan_cfi', 
      'intf_prefix_length', 'loopback_ip_addr_step', 
      'label_adv', 'lsr_id', 'lsr_id_step', 'remote_ip_addr', 
      'remote_ip_addr_step', 'vci', 'vci_step', 'vlan_id', 
      'vlan_id_mode', 'vlan_user_priority', 'vpi', 'vpi_step', 
      'loopback_ip_addr', 'mode', 'hello_interval', 
      'peer_discovery', 'vlan_id_step'  } 

j_emulation_isis_info = {
      'handle', 'mode'  } 

j_emulation_rip_route_config = {
      'prefix_length', 'num_prefixes', 
      'route_tag', 'prefix_step', 'mode', 'next_hop', 'prefix_start'  } 

j_emulation_ospf_lsa_config = {
      'mode', 'handle', 'adv_router_id', 
      'lsa_handle', 'link_state_id', 'ls_seq', 'session_type', 
      'options', 'attached_router_id', 'external_number_of_prefix', 
      'net_attached_router', 'external_prefix_forward_addr', 
      'router_abr', 'external_prefix_length', 'router_asbr', 
      'external_prefix_start', 'router_link_data', 
      'external_prefix_step', 'router_link_id', 
      'net_prefix_length', 'router_link_metric', 
      'nssa_number_of_prefix', 'router_link_type', 
      'nssa_prefix_forward_addr', 
      'router_virtual_link_endpt', 
      'nssa_prefix_length', 'nssa_prefix_metric', 
      'nssa_prefix_start', 'nssa_prefix_step', 
      'router_link_mode', 'nssa_prefix_type', 'type', 
      'router_link_idx', 'summary_number_of_prefix', 
      'summary_prefix_length', 'summary_prefix_start', 
      'summary_prefix_step', 'te_tlv_type', 'te_link_id', 
      'te_link_type', 'te_instance_id', 'te_metric', 'te_local_ip', 
      'te_remote_ip', 'te_admin_group', 'te_max_bw', 
      'te_max_resv_bw'  } 

j_emulation_rsvp_tunnel_config = {
      'mode', 'count', 'avoid_node_id', 
      'ero_dut_pfxlen', 'egress_ip_addr', 
      'fast_reroute_hop_limit', 'egress_ip_step', 
      'port_handle', 'ero', 'sender_tspec_peak_data_rate', 
      'ero_list_loose', 'sender_tspec_token_bkt_rate', 
      'ero_list_pfxlen', 'sender_tspec_token_bkt_size', 
      'facility_backup', 'session_attr', 'fast_reroute', 
      'tunnel_id_step', 'ingress_ip_addr', 'ingress_ip_step', 
      'one_to_one_backup', 'plr_id', 'rro', 'rsvp_behavior', 
      'sender_tspec_max_pkt_size', 
      'sender_tspec_min_policed_size', 
      'session_attr_bw_protect', 'session_attr_flags', 
      'session_attr_label_record', 
      'session_attr_local_protect', 
      'session_attr_node_protect', 
      'session_attr_resource_affinities', 
      'session_attr_se_style', 'tunnel_id_start', 
      'ero_mode', 'ero_list_ipv4'  } 

j_emulation_mld_control = {
      'group_member_handle', 'handle', 'mode'  } 

j_emulation_mld_info = {
      'handle'  } 

j_interface_control = {
      'port_handle'  } 

j_emulation_pim_control = {
      'mode'  } 

j_emulation_dhcp_stats = {
      'port_handle', 'handle'  } 

j_l2tp_control = {
      'action', 'handle'  } 

j_cleanup_session = {
      'maintain_lock', 'port_handle'  } 

j_pppox_stats = {
      'mode', 'handle'  } 

j_emulation_bfd_control = {
      'mode', 'port_handle'  } 

j_emulation_igmp_info = {
      'handle', 'port_handle', 'mode'  } 