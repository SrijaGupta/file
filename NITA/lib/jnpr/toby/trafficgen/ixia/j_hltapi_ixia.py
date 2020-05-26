#!/usr/local/python-3.4.5/bin/python3

'''

 This is Auto-generated IXIA HLTAPI common Stub code
 please do NOT modify the format/delete any comments in this file,
   this file is read and regenerated automatically

'''
import os
import traceback
from time import sleep
from collections import OrderedDict
import re
import shutil
import ipaddress
import inspect
import ftplib
true = re.compile("[T|t]rue")
false = re.compile("[F|f]alse")

# Constant to use as default value
jNone = "jNone"

handle_map = dict()
session_map = dict()
igmp_querier_handles = []
dhcp_group_handles = dict()
v4_handles = []
v6_handles = []
stream_list = dict()
device_group = dict()
connected = 1
NETWORK_TO_BGP_HANDLES = dict()
capturing = 0
capture_buffer = 0
capture_trigger = 0
capture_filter = 0
bidirectional = 0
packetCaptureObjInst = None
pfc_dict = dict()

def j_cleanup_session(rt_handle):
    """
    :param rt_handle:       RT object
    :return response from rt_handle.invoke(<parameters>)

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    global handle_map
    global session_map
    global igmp_querier_handles
    global dhcp_group_handles
    global v4_handles
    global v6_handles
    global stream_list
    global device_group
    global connected

    handle_map = dict()
    session_map = dict()
    igmp_querier_handles = []
    dhcp_group_handles = dict()
    v4_handles = []
    v6_handles = []
    stream_list = dict()
    device_group = dict()

    args = dict()
    args['maintain_lock'] = 0
    args['port_handle'] = list(rt_handle.handle_to_port_map.keys())
    args['reset'] = 1

    if connected == 1:
        ret = rt_handle.invoke('cleanup_session', **args)
        if ret['status'] == '1':
            connected = 0
        return ret


def j_connect(rt_handle):
    """
    :param rt_handle:       RT object
    :return response from rt_handle.invoke(<parameters>)

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    global connected

    if connected == 0:
        t.Initialize(force=True)
        connected = 1


def j_emulation_bfd_config(
        rt_handle,
        count=jNone,
        detect_multiplier=jNone,
        echo_rx_interval=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        gateway_ipv6_addr=jNone,
        gateway_ipv6_addr_step=jNone,
        handle=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_ipv6_addr=jNone,
        intf_ipv6_addr_step=jNone,
        ip_version=jNone,
        local_mac_addr=jNone,
        local_mac_addr_step=jNone,
        mode=jNone,
        remote_ip_addr=jNone,
        remote_ip_addr_step=jNone,
        remote_ipv6_addr=jNone,
        remote_ipv6_addr_step=jNone,
        vlan_id1=jNone,
        vlan_id2=jNone,
        vlan_id_mode1=jNone,
        vlan_id_mode2=jNone,
        vlan_id_step1=jNone,
        vlan_id_step2=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param count
    :param detect_multiplier - <2-100>
    :param echo_rx_interval - <0-10000>
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param gateway_ipv6_addr
    :param gateway_ipv6_addr_step
    :param handle
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_ipv6_addr
    :param intf_ipv6_addr_step
    :param ip_version - <IPv4:4|IPv6:6>
    :param local_mac_addr
    :param local_mac_addr_step
    :param mode - <create|modify|delete>
    :param remote_ip_addr
    :param remote_ip_addr_step
    :param remote_ipv6_addr
    :param remote_ipv6_addr_step
    :param vlan_id1 - <0-4095>
    :param vlan_id2 - <0-4095>
    :param vlan_id_mode1 - <fixed|increment>
    :param vlan_id_mode2 - <fixed|increment>
    :param vlan_id_step1 - <0-4095>
    :param vlan_id_step2 - <0-4095>
    :param port_handle

    Spirent Returns:


    IXIA Returns:
    {
        "bfd_router_handle": "/topology:1/deviceGroup:1/bfdRouter:2",
        "bfd_v4_interface_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1",
        "bfd_v4_session_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1/bfdv4Session",
        "handle": "/topology:1/deviceGroup:1/bfdRouter:2/item:1",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1",
        "interfaces": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1/item:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['count'] = count
    args['detect_multiplier'] = detect_multiplier
    args['echo_rx_interval'] = echo_rx_interval
    args['gateway_ip_addr'] = gateway_ip_addr
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['gateway_ipv6_addr'] = gateway_ipv6_addr
    args['gateway_ipv6_addr_step'] = gateway_ipv6_addr_step
    args['handle'] = handle
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_ipv6_addr'] = intf_ipv6_addr
    args['intf_ipv6_addr_step'] = intf_ipv6_addr_step
    args['ip_version'] = ip_version
    args['local_mac_addr'] = local_mac_addr
    args['local_mac_addr_step'] = local_mac_addr_step
    args['mode'] = mode
    args['remote_ip_addr'] = remote_ip_addr
    args['remote_ip_addr_step'] = remote_ip_addr_step
    args['remote_ipv6_addr'] = remote_ipv6_addr
    args['remote_ipv6_addr_step'] = remote_ipv6_addr_step
    args['vlan_id1'] = vlan_id1
    args['vlan_id2'] = vlan_id2
    args['vlan_id_mode1'] = vlan_id_mode1
    args['vlan_id_mode2'] = vlan_id_mode2
    args['vlan_id_step1'] = vlan_id_step1
    args['vlan_id_step2'] = vlan_id_step2
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_bfd_config.__doc__, **args)

    vlan_dict = {}
    vlan_args = ['vlan_id1', 'vlan_id2', 'vlan_id_mode1', 'vlan_id_mode2', 'vlan_id_step1', 'vlan_id_step2']
    for arg in vlan_args:
        if args.get(arg):
            vlan_dict[arg] = args.pop(arg)

    if mode == 'create':
        if args.get('port_handle'):
            count = args['count'] if args.get('count') else jNone
            handle = create_deviceGroup(rt_handle, args.pop('port_handle'), count)
            handle = handle['device_group_handle']
        elif not args.get('handle'):
            raise Exception("Please pass either handle or port_handle to the function call")
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        if hndl in session_map:
            args['ip_version'] = session_map[hndl]
        ret.append(rt_handle.invoke('emulation_bfd_config', **args))
        if vlan_dict:
            if mode == "create":
                vlan_config(rt_handle, vlan_dict, ret[-1]['bfd_v{}_interface_handle'.format(args['ip_version'])])
            else:
                vlan_config(rt_handle, vlan_dict, hndl)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'bfd_v4_interface_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['bfd_v4_interface_handle']
        if 'bfd_v6_interface_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['bfd_v6_interface_handle']
        if mode == 'create':
            __check_and_raise(ip_version)
            session_map[ret[index]['handles']] = args['ip_version']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bfd_control(rt_handle, handle=jNone,
                            mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|resume_pdus:resume_pdu|stop_pdus:stop_pdu|enable_demand:demand_mode_enable|disable_demand:demand_mode_disable|initiate_poll|admin_up:set_admin_up|admin_down:set_admin_down>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_bfd_control.__doc__, **args)
    args['protocol_name'] = 'bfd'
    # control_args = ['stop_pdu', 'resume_pdu', 'demand_mode_disable', 'demand_mode_enable', 'initiate_poll', 'set_admin_down', 'set_admin_up']
    # for arg in control_args:
        # if mode == arg:
            # args['protocol_name'] = 'bfd'

    ret = rt_handle.invoke('emulation_bfd_control', **args)

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bfd_info(rt_handle, handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle

    Spirent Returns:


    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1": {
            "bfd_learned_info": {
                "device#": "{1}",
                "my_discriminator": "{1}",
                "my_ip_address": "{3.3.3.1}",
                "peer_discriminator": "{1}",
                "peer_ip_address": "{3.3.3.2}",
                "peer_session_state": "{Up}",
                "recvd_min_rx_interval": "{1000}",
                "recvd_multiplier": "{3}",
                "recvd_peer_flags": "{P=0| F=0| C=0| A=0| D=0|}",
                "recvd_tx_interval": "{1000}",
                "session_state": "{Up}",
                "session_type": "{Single Hop}",
                "session_up_time": "{19}",
                "session_used_by_protocol": "{NONE}"
            }
        },
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1/item:1": {
            "session": {
                "control_pkts_rx": "27",
                "control_pkts_tx": "28",
                "echo_dut_pkts_rx": "0",
                "echo_dut_pkts_tx": "0",
                "echo_self_pkts_rx": "0",
                "echo_self_pkts_tx": "0",
                "mpls_rx": "0",
                "mpls_tx": "0",
                "port_name": "1/11/2",
                "session_flap_cnt": "0",
                "sessions_auto_created": "0",
                "sessions_auto_created_up": "0",
                "sessions_configured": "1",
                "sessions_configured_up": "1"
            }
        },
        "1/11/2": {
            "aggregate": {
                "control_pkts_rx": "21",
                "control_pkts_tx": "22",
                "echo_dut_pkts_rx": "0",
                "echo_dut_pkts_tx": "0",
                "echo_self_pkts_rx": "0",
                "echo_self_pkts_tx": "0",
                "mpls_rx": "0",
                "mpls_tx": "0",
                "port_name": "1/11/2",
                "session_flap_cnt": "0",
                "sessions_auto_created": "0",
                "sessions_auto_created_up": "0",
                "sessions_configured": "1",
                "sessions_configured_up": "1",
                "status": "started"
            }
        },
        "Device Group 1": {
            "Bfdv4 Stats Per Device": {
                "control_pkts_rx": "25",
                "control_pkts_tx": "26",
                "echo_dut_pkts_rx": "0",
                "echo_dut_pkts_tx": "0",
                "echo_self_pkts_rx": "0",
                "echo_self_pkts_tx": "0",
                "mpls_rx": "0",
                "mpls_tx": "0",
                "session_flap_cnt": "0",
                "sessions_auto_created": "0",
                "sessions_auto_created_up": "0",
                "sessions_configured": "1",
                "sessions_configured_up": "1",
                "status": "started"
            }
        },
        "bfd_session_state": "{Up}",
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    key_list = list(args.keys())
    for key in key_list:
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'aggregate'
        stats.update(rt_handle.invoke('emulation_bfd_info', **args))
        args['mode'] = 'learned_info'
        stats.update(rt_handle.invoke('emulation_bfd_info', **args))
        args['mode'] = 'stats_per_device_group'
        stats.update(rt_handle.invoke('emulation_bfd_info', **args))
        args['mode'] = 'stats_per_session'
        stats.update(rt_handle.invoke('emulation_bfd_info', **args))
        ret.append(stats)

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'bfd_learned_info' in ret[index][key]:
                if 'session_state' in ret[index][key]['bfd_learned_info']:
                    ret[index]['bfd_session_state'] = ret[index][key]['bfd_learned_info']['session_state']

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bgp_config(
        rt_handle,
        bfd_registration=jNone,
        count=jNone,
        graceful_restart_enable=jNone,
        handle=jNone,
        ip_version=jNone,
        local_as=jNone,
        local_as4=jNone,
        local_as_mode=jNone,
        local_ip_addr=jNone,
        local_ipv6_addr=jNone,
        local_router_id_step=jNone,
        mac_address_start=jNone,
        md5_enable=jNone,
        md5_key=jNone,
        netmask=jNone,
        remote_ip_addr=jNone,
        remote_ipv6_addr=jNone,
        restart_time=jNone,
        staggered_start_time=jNone,
        stale_time=jNone,
        update_interval=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        remote_as=jNone,
        router_id=jNone,
        neighbor_type=jNone,
        ipv4_unicast_nlri=jNone,
        next_hop_ip=jNone,
        ipv4_mpls_nlri=jNone,
        ipv4_mpls_vpn_nlri=jNone,
        ipv4_multicast_nlri=jNone,
        hold_time=jNone,
        vpls_nlri=jNone,
        retry_time=jNone,
        retries=jNone,
        local_as_step=jNone,
        local_addr_step=jNone,
        remote_addr_step=jNone,
        ipv6_mpls_nlri=jNone,
        ipv6_mpls_vpn_nlri=jNone,
        ipv6_unicast_nlri=jNone,
        ttl_value=jNone,
        remote_loopback_ip_addr=jNone,
        ipv6_multicast_nlri=jNone,
        asnum_4byte_enable=jNone,
        remote_ipv6_addr_step=jNone,
        local_ipv6_addr_step=jNone,
        active_connect_enable=jNone,
        local_router_id_enable=jNone,
        bfd_registration_mode=jNone,
        gateway_ip_addr=jNone,
        next_hop_enable=jNone,
        ipv4_multicast_vpn_nlri=jNone,
        ipv6_multicast_vpn_nlri=jNone,
        vpls_multicast_nlri=jNone,
        vpls_multicast_vpn_nlri=jNone,
        netmask_ipv6=jNone,
        next_hop_ipv6=jNone,
        port_handle=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        staggered_start_enable=jNone,
        next_hop_ip_step=jNone,
        vlan_outer_user_priority=jNone,
        bgp_stack_multiplier=jNone,
        ipv4_srtepolicy_nlri=jNone,
        ipv6_srtepolicy_nlri=jNone,
        ipv4_mpls_capability=jNone,
        bgp_session_ip_addr=jNone):
        # Below arguments are not supported by spirent, when spirent adds
        # this arguments can be uncommented
        # updates_per_iteration=jNone,
        # no_write=jNone
    """
    :param rt_handle:       RT object
    :param bfd_registration
    :param count
    :param graceful_restart_enable
    :param handle
    :param ip_version
    :param local_as - <1-65535>
    :param local_as4
    :param local_as_mode - <fixed|increment>
    :param local_ip_addr
    :param local_ipv6_addr
    :param local_router_id_step
    :param mac_address_start
    :param md5_enable
    :param md5_key
    :param netmask - <1-128>
    :param remote_ip_addr
    :param remote_ipv6_addr
    :param restart_time - <0-10000000>
    :param staggered_start_time - <0-10000>
    :param stale_time - <0-10000>
    :param update_interval - <0-10000>
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <1-4094>
    :param vlan_user_priority - <0-7>
    :param mode - <create|enable|disable|modify|reset>
    :param remote_as - <0-65535>
    :param router_id
    :param neighbor_type - <ibgp:internal|ebgp:external>
    :param ipv4_unicast_nlri
    :param next_hop_ip
    :param ipv4_mpls_nlri
    :param ipv4_mpls_vpn_nlri
    :param ipv4_multicast_nlri
    :param hold_time - <3-65535>
    :param vpls_nlri
    :param retry_time - <10-300>
    :param retries - <0-65535>
    :param local_as_step - <0-65535>
    :param local_addr_step
    :param remote_addr_step
    :param ipv6_mpls_nlri
    :param ipv6_mpls_vpn_nlri
    :param ipv6_unicast_nlri
    :param ttl_value
    :param remote_loopback_ip_addr
    :param ipv6_multicast_nlri
    :param asnum_4byte_enable
    :param remote_ipv6_addr_step
    :param local_ipv6_addr_step
    :param active_connect_enable
    :param local_router_id_enable - <1>
    :param bfd_registration_mode - <single_hop|multi_hop>
    :param gateway_ip_addr
    :param next_hop_enable - <1>
    :param ipv4_multicast_vpn_nlri
    :param ipv6_multicast_vpn_nlri
    :param vpls_multicast_nlri
    :param vpls_multicast_vpn_nlri
    :param netmask_ipv6 - <1-128>
    :param next_hop_ipv6
    :param port_handle
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <1-4094>
    :param staggered_start_enable
    :param next_hop_ip_step
    :param vlan_outer_user_priority - <0-7>
    :param bgp_stack_multiplier
    :param ipv4_srtepolicy_nlri - <0|1>
    :param ipv6_srtepolicy_nlri - <0|1>
    :param ipv4_mpls_capability - <0|1>
    :param bgp_session_ip_addr - <router_id>
    #Below arguments are not supported by spirent, when spirent adds
    #these arguments can be uncommented
    #updates_per_iteration
    #no_write

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "bgp_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['bfd_registration'] = bfd_registration
    args['graceful_restart_enable'] = graceful_restart_enable
    args['handle'] = handle
    args['ip_version'] = ip_version
    args['local_as'] = local_as
    args['local_as4'] = local_as4
    args['local_as_mode'] = local_as_mode
    args['local_ip_addr'] = local_ip_addr
    args['local_ipv6_addr'] = local_ipv6_addr
    args['local_router_id_step'] = local_router_id_step
    args['mac_address_start'] = mac_address_start
    args['md5_enable'] = md5_enable
    args['md5_key'] = md5_key
    args['netmask'] = netmask
    args['remote_ip_addr'] = remote_ip_addr
    args['remote_ipv6_addr'] = remote_ipv6_addr
    args['restart_time'] = restart_time
    args['staggered_start_time'] = staggered_start_time
    args['stale_time'] = stale_time
    args['update_interval'] = update_interval
    args['mode'] = mode
    args['remote_as'] = remote_as
    args['neighbor_type'] = neighbor_type
    args['ipv4_unicast_nlri'] = ipv4_unicast_nlri
    args['next_hop_ip'] = next_hop_ip
    args['ipv4_mpls_nlri'] = ipv4_mpls_nlri
    args['ipv4_mpls_vpn_nlri'] = ipv4_mpls_vpn_nlri
    args['ipv4_multicast_nlri'] = ipv4_multicast_nlri
    args['hold_time'] = hold_time
    args['vpls_nlri'] = vpls_nlri
    args['retry_time'] = retry_time
    args['retries'] = retries
    args['local_as_step'] = local_as_step
    args['local_addr_step'] = local_addr_step
    args['remote_addr_step'] = remote_addr_step
    args['ipv6_mpls_nlri'] = ipv6_mpls_nlri
    args['ipv6_mpls_vpn_nlri'] = ipv6_mpls_vpn_nlri
    args['ipv6_multicast_nlri'] = ipv6_multicast_nlri
    args['ipv6_unicast_nlri'] = ipv6_unicast_nlri
    args['ttl_value'] = ttl_value
    args['remote_loopback_ip_addr'] = remote_loopback_ip_addr
    args['asnum_4byte_enable'] = asnum_4byte_enable
    if 'ipv6:' in handle:
        args['remote_addr_step'] = remote_ipv6_addr_step
        args['local_addr_step'] = local_ipv6_addr_step
    args['active_connect_enable'] = active_connect_enable
    args['bfd_registration_mode'] = bfd_registration_mode
    args['gateway_ip_addr'] = gateway_ip_addr
    args['next_hop_enable'] = next_hop_enable
    args['staggered_start_enable'] = staggered_start_enable
    args['router_id'] = router_id
    args['local_router_id_enable'] = local_router_id_enable
    args['ipv4_multicast_vpn_nlri'] = ipv4_multicast_vpn_nlri
    args['ipv6_multicast_vpn_nlri'] = ipv6_multicast_vpn_nlri
    args['vpls_multicast_nlri'] = vpls_multicast_nlri
    args['vpls_multicast_vpn_nlri'] = vpls_multicast_vpn_nlri
    args['bgp_stack_multiplier'] = bgp_stack_multiplier
    args['ipv4_mpls_capability'] = ipv4_mpls_capability
    args['bgp_session_ip_addr'] = bgp_session_ip_addr
    if ip_version in ['6', 6]:
        args['gateway_ip_addr'] = next_hop_ipv6
        args['remote_ipv6_addr'] = next_hop_ipv6 if remote_ipv6_addr is jNone else remote_ipv6_addr

    args = get_arg_value(rt_handle, j_emulation_bgp_config.__doc__, **args)
    if args.get('local_router_id_step'):
        args['router_id_step'] = args.pop('local_router_id_step')
    if args.get('asnum_4byte_enable'):
        args['enable_4_byte_as'] = args.pop('asnum_4byte_enable')
    args['return_detailed_handles'] = 1

    if args.get('next_hop_ip'):
        if next_hop_ip_step != jNone and args.get('next_hop_enable') in [1, '1']:
            nargs = dict()
            nargs['pattern'] = 'counter'
            nargs['counter_start'] = args['next_hop_ip']
            nargs['counter_step'] = next_hop_ip_step
            nargs['counter_direction'] = 'increment'
            _result_ = rt_handle.invoke('multivalue_config', **nargs)
            args['next_hop_ip'] = _result_['multivalue_handle']
    # Below arguments are not supported by spirent, when spirent adds
    #this arguments can be uncommented
    #args['updates_per_iteration'] = updates_per_iteration
    #args['no_write'] = no_write

    if mode == 'enable' or mode == 'create':
        if args.get('ipv4_unicast_nlri') is None:
            args['ipv4_filter_unicast_nlri'] = 1
        else:
            args['ipv4_filter_unicast_nlri'] = args.pop('ipv4_unicast_nlri')

        if args.get('ipv6_unicast_nlri') is None:
            args['ipv6_filter_unicast_nlri'] = 1
        else:
            args['ipv6_filter_unicast_nlri'] = args.pop('ipv6_unicast_nlri')

    if args.get('ipv4_multicast_nlri'):
        args['ipv4_filter_multicast_nlri'] = args.pop('ipv4_multicast_nlri')
    if args.get('ipv4_mpls_nlri'):
        args['ipv4_filter_mpls_nlri'] = args.pop('ipv4_mpls_nlri')
    if args.get('ipv4_mpls_vpn_nlri'):
        args['ipv4_filter_mpls_vpn_nlri'] = args.pop('ipv4_mpls_vpn_nlri')
    if args.get('ipv6_multicast_nlri'):
        args['ipv6_filter_multicast_nlri'] = args.pop('ipv6_multicast_nlri')
    if args.get('ipv6_mpls_nlri'):
        args['ipv6_filter_mpls_nlri'] = args.pop('ipv6_mpls_nlri')
    if args.get('ipv6_mpls_vpn_nlri'):
        args['ipv6_filter_mpls_vpn_nlri'] = args.pop('ipv6_mpls_vpn_nlri')
    if args.get('vpls_nlri'):
        args['vpls_filter_nlri'] = args.pop('vpls_nlri')
    if args.get('ipv4_multicast_vpn_nlri'):
        args['ipv4_filter_multicast_vpn_nlri'] = args.pop('ipv4_multicast_vpn_nlri')
    if args.get('ipv6_multicast_vpn_nlri'):
        args['ipv6_filter_multicast_vpn_nlri'] = args.pop('ipv6_multicast_vpn_nlri')

    if args.get('vpls_multicast_nlri'):
        args['ipv4_multicast_nlri'] = args.get('vpls_multicast_nlri')
        args['vpls_nlri'] = args.pop('vpls_multicast_nlri')
    if args.get('vpls_multicast_vpn_nlri'):
        args['ipv4_multicast_vpn_nlri'] = args.get('vpls_multicast_vpn_nlri')
        args['vpls_nlri'] = args.pop('vpls_multicast_vpn_nlri')
    if args.get('bgp_stack_multiplier'):
        args['count'] = args.pop('bgp_stack_multiplier')
    if args.get('bgp_session_ip_addr'):
        args.pop('bgp_session_ip_addr')

    vlan_args = dict()
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_mode'] = vlan_id_mode
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_outer_id'] = vlan_outer_id
    vlan_args['vlan_outer_id_mode'] = vlan_outer_id_mode
    vlan_args['vlan_user_priority'] = vlan_user_priority
    vlan_args['vlan_outer_id_step'] = vlan_outer_id_step
    vlan_args['vlan_outer_user_priority'] = vlan_outer_user_priority
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    vlan_args = get_arg_value(rt_handle, j_emulation_bgp_config.__doc__, **vlan_args)

    ret = []
    if mode == 'active' or mode == 'inactive' or mode == 'readvertise' or mode == 'activate' or mode == 'delete':
        raise ValueError("The provided mode "+mode+" is not supported")

    if (mode == 'enable' or mode == 'create') and port_handle != jNone:
        handle = create_deviceGroup(rt_handle, port_handle, count)
        handle = handle['device_group_handle']
        __check_and_raise(ip_version)
        __check_and_raise(router_id)
    else:
        __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    if mode == 'reset' or mode == 'delete' or mode == 'disable':
        args['mode'] = 'delete'
        ret.append(rt_handle.invoke('emulation_bgp_config', **args))
    else:
        for hndl in handle:
            args['handle'] = hndl
            ret.append(rt_handle.invoke('emulation_bgp_config', **args))

    # ***** Return Value Modification *****
    for index in range(len(ret)):
        if port_handle is not jNone:
            ip_handle = re.findall(r'.+/ipv\d+:\d+', ret[index]['bgp_handle'])
            if len(ip_handle) > 0:
                ip_handle = ip_handle[0]
            else:
                raise Exception('Could not retrieve interface handle from bgp handle {}'.format(ret[index]['bgp_handle']))
            if netmask != jNone or netmask_ipv6 != jNone:
                if netmask is not jNone:
                    netmask = netmask
                elif netmask_ipv6 is not jNone:
                    netmask = netmask_ipv6
                mulval_hndl = invoke_ixnet(rt_handle, "getAttribute", ip_handle, "-prefix")
                mulval_hndl = mulval_hndl+'/singleValue'
                invoke_ixnet(rt_handle, "setAttribute", mulval_hndl, "-value", netmask)
                invoke_ixnet(rt_handle, "commit")
        if 'bgp_handle' in ret[index]:
            bgp_handle = ret[index]['bgp_handle']
            if ipv4_srtepolicy_nlri != jNone:
                mulval_hndl = invoke_ixnet(rt_handle, "getAttribute", bgp_handle, "-capabilitySRTEPoliciesV4")
                mulval_hndl = mulval_hndl+'/singleValue'
                invoke_ixnet(rt_handle, "setAttribute", mulval_hndl, "-value", ipv4_srtepolicy_nlri)
                invoke_ixnet(rt_handle, "commit")
            if ipv6_srtepolicy_nlri != jNone:
                mulval_hndl = invoke_ixnet(rt_handle, "getAttribute", bgp_handle, "-capabilitySRTEPoliciesV6")
                mulval_hndl = mulval_hndl+'/singleValue'
                invoke_ixnet(rt_handle, "setAttribute", mulval_hndl, "-value", ipv6_srtepolicy_nlri)
                invoke_ixnet(rt_handle, "commit")

        if 'handles' in ret[index]:
            ret[index]['bgp_intf_handles'] = ret[index]['handles']
        if 'bgp_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['bgp_handle']
            if vlan_args:
                vlan_config(rt_handle, vlan_args, ret[-1]['bgp_handle'])

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bgp_control(
        rt_handle,
        handle=jNone,
        mode=jNone,
        route_flap_down_time=jNone,
        route_flap_up_time=jNone,
        flap_count=jNone,
        route_handle=jNone,
        link_flap_up_time=jNone,
        link_flap_down_time=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|restart|link_flap|full_route_flap>
    :param route_flap_down_time - <0-10000000>
    :param route_flap_up_time - <0-10000000>
    :param flap_count
    :param route_handle
    :param link_flap_up_time - <0-10000000>
    :param link_flap_down_time - <0-10000000>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode
    link_args = dict()
    link_args['link_flap_down_time'] = link_flap_down_time
    link_args['link_flap_up_time'] = link_flap_up_time
    rt_link_args = dict()
    rt_link_args['route_flap_down_time'] = route_flap_down_time
    rt_link_args['route_flap_up_time'] = route_flap_up_time
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_bgp_control.__doc__, **args)
    link_args = get_arg_value(rt_handle, j_emulation_bgp_control.__doc__, **link_args)
    if link_args.get('link_flap_down_time'):
        link_args['flap_down_time'] = link_args.pop('link_flap_down_time')
    if link_args.get('link_flap_up_time'):
        link_args['flap_up_time'] = link_args.pop('link_flap_up_time')

    rt_link_args = get_arg_value(rt_handle, j_emulation_bgp_control.__doc__, **rt_link_args)
    if rt_link_args.get('route_flap_down_time'):
        rt_link_args['flap_down_time'] = rt_link_args.pop('route_flap_down_time')
    if rt_link_args.get('route_flap_up_time'):
        rt_link_args['flap_up_time'] = rt_link_args.pop('route_flap_up_time')

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    def set_flap_count(flap_handle, attribute, count):
        """ set_flap_count """
        count = int(count)
        m_val = invoke_ixnet(rt_handle, 'getAttribute', flap_handle, attribute)
        value_list = invoke_ixnet(rt_handle, 'add', m_val, 'valueList')
        m_val_len = len(invoke_ixnet(rt_handle, 'getAttribute', value_list, '-values'))
        if count < m_val_len:
            true_value = ['true'] * count
            false_value = ['false'] * (m_val_len - count)
            invoke_ixnet(rt_handle, 'setAttribute', value_list, '-values', true_value+false_value)
            invoke_ixnet(rt_handle, 'commit')
        else:
            invoke_ixnet(rt_handle, 'setAttribute', value_list, '-values', ['true']*m_val_len)
            invoke_ixnet(rt_handle, 'commit')

    ret = []
    if mode != 'full_route_flap':
        for hndl in handle:
            if (mode == 'advertise' or mode == 'withdraw') and ('networkGroup' in hndl):
                if mode == 'advertise':
                    hndl = get_bgp_route_property(rt_handle, hndl)
                    args['mode'] = 'readvertise_routes'
                if mode == 'withdraw':
                    hndl = get_bgp_route_property(rt_handle, hndl)
                    args['mode'] = 'age_out_routes'
                    args['age_out_percent'] = '100'
                args['handle'] = hndl
                ret.append(rt_handle.invoke('emulation_bgp_control', **args))
            elif mode == 'link_flap' and len(link_args.keys()) != 0:
                link_args['mode'] = 'modify'
                link_args['handle'] = hndl
                link_args['enable_flap'] = '1'
                ret.append(rt_handle.invoke('emulation_bgp_config', **link_args))
                if flap_count is not jNone:
                    set_flap_count(hndl, '-flap', flap_count)
                nargs = dict()
                nargs['action'] = 'apply_on_the_fly_changes'
                rt_handle.invoke('test_control', **nargs)
            else:
                args['handle'] = hndl
                ret.append(rt_handle.invoke('emulation_bgp_control', **args))
    if mode == 'full_route_flap' and route_handle is not jNone:
        if isinstance(route_handle, str):
            route_handle = [route_handle]
        for route in route_handle:
            if 'networkGroup' in route:
                rt_link_args['mode'] = 'modify'
                rt_link_args['handle'] = get_bgp_route_property(rt_handle, route)
                rt_link_args['enable_route_flap'] = '1'
                ret.append(rt_handle.invoke('emulation_bgp_route_config', **rt_link_args))
                if flap_count is not jNone:
                    set_flap_count(rt_link_args['handle'], '-enableFlapping', flap_count)
                nargs = dict()
                nargs['action'] = 'apply_on_the_fly_changes'
                rt_handle.invoke('test_control', **nargs)
            else:
                raise Exception('expected route handle but got {}'.format(route))

    if mode == 'start':
        for hndl in handle:
            vrf_type = "bgpVrf" if "ipv4" in hndl else "bgpV6Vrf"
            vrf = invoke_ixnet(rt_handle, 'getList', hndl, vrf_type)
            if len(vrf) > 0:
                invoke_ixnet(rt_handle, 'execute', 'start', vrf)
                sleep(3)
    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bgp_info(rt_handle, handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle

    Spirent Returns:
    {
        "asn": "100",
        "ip_address": "192.85.1.3",
        "keepalive_rx": "0",
        "keepalive_tx": "0",
        "last_routes_advertised_rx": "0",
        "notify_code_rx": "0",
        "notify_code_tx": "0",
        "notify_rx": "0",
        "notify_subcode_rx": "0",
        "notify_subcode_tx": "0",
        "notify_tx": "0",
        "num_node_routes": "0",
        "open_rx": "0",
        "open_tx": "0",
        "peers": "3.3.3.2",
        "route_withdrawn_tx": "0",
        "routes_advertised_rx": "0",
        "routes_advertised_tx": "0",
        "routes_withdrawn_rx": "0",
        "routes_withdrawn_tx": "0",
        "sessions_configured": "1",
        "sessions_established": "0",
        "status": "1",
        "update_rx": "0",
        "update_tx": "0"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1/item:1": {
            "session": {
                "Hold_timer_expireds_rx": "0",
                "active_on": "True",
                "attribute_flags_error": "0",
                "attribute_length_error": "0",
                "bad_bgp_id_rx": "0",
                "bad_peer_as_rx": "0",
                "error_link_state_nlri_rx": "0",
                "external_connects_accepted": "1",
                "external_connects_rx": "1",
                "fsm_state": "Established",
                "graceful_restart_attempted": "0",
                "graceful_restart_failed": "0",
                "hold_timer_expireds_tx": "0",
                "invalid_network_field": "0",
                "invalid_next_hop_attribute": "0",
                "invalid_opens_rx": "0",
                "invalid_opens_tx": "0",
                "invalid_origin_attribute": "0",
                "keepalive_rx": "3",
                "keepalive_tx": "3",
                "last_error_rx": "0",
                "last_error_tx": "0",
                "ls_ipv4_prefix_advertised_rx": "0",
                "ls_ipv4_prefix_advertised_tx": "0",
                "ls_ipv4_prefix_withdrawn_rx": "0",
                "ls_ipv4_prefix_withdrawn_tx": "0",
                "ls_ipv6_prefix_advertised_rx": "0",
                "ls_ipv6_prefix_advertised_tx": "0",
                "ls_ipv6_prefix_withdrawn_rx": "0",
                "ls_ipv6_prefix_withdrawn_tx": "0",
                "ls_link_advertised_rx": "0",
                "ls_link_advertised_tx": "0",
                "ls_link_withdrawn_rx": "0",
                "ls_link_withdrawn_tx": "0",
                "ls_node_advertised_rx": "0",
                "ls_node_advertised_tx": "0",
                "ls_node_withdrawn_rx": "0",
                "ls_node_withdrawn_tx": "0",
                "malformed_as_path": "0",
                "messages_rx": "5",
                "messages_tx": "5",
                "notify_rx": "0",
                "notify_tx": "0",
                "open_rx": "1",
                "open_tx": "1",
                "route_withdraws_rx": "0",
                "routes_advertised": "1",
                "routes_rx": "1",
                "routes_rx_graceful_restart": "0",
                "routes_withdrawn": "0",
                "session_status": "Up",
                "starts_occurred": "1",
                "update_errors_rx": "0",
                "update_errors_tx": "0",
                "update_rx": "1",
                "update_tx": "1"
            }
        },
        "1/11/2": {
            "aggregate": {
                "Hold_timer_expireds_rx": "0",
                "active_state": "0",
                "as_routing_loop": "0",
                "attribute_flags_error": "0",
                "attribute_length_error": "0",
                "authentication_failures_rx": "0",
                "bad_bgp_id_rx": "0",
                "bad_message_length": "0",
                "bad_message_type": "0",
                "bad_peer_as_rx": "0",
                "ceases_rx": "0",
                "ceases_tx": "0",
                "connect_state": "0",
                "connection_not_synchronized": "0",
                "error_link_state_nlri_rx": "0",
                "established_state": "1",
                "external_connects_accepted": "1",
                "external_connects_rx": "1",
                "graceful_restart_attempted": "0",
                "graceful_restart_failed": "0",
                "header_errors_rx": "0",
                "header_errors_tx": "0",
                "hold_timer_expireds_tx": "0",
                "idle_state": "0",
                "invalid_header_suberror_unspecified": "0",
                "invalid_network_field": "0",
                "invalid_next_hop_attribute": "0",
                "invalid_open_suberror_unspecified": "0",
                "invalid_opens_rx": "0",
                "invalid_opens_tx": "0",
                "invalid_origin_attribute": "0",
                "invalid_update_suberror_unspecified": "0",
                "keepalive_rx": "3",
                "keepalive_tx": "3",
                "ls_ipv4_prefix_advertised_rx": "0",
                "ls_ipv4_prefix_advertised_tx": "0",
                "ls_ipv4_prefix_withdrawn_rx": "0",
                "ls_ipv4_prefix_withdrawn_tx": "0",
                "ls_ipv6_prefix_advertised_rx": "0",
                "ls_ipv6_prefix_advertised_tx": "0",
                "ls_ipv6_prefix_withdrawn_rx": "0",
                "ls_ipv6_prefix_withdrawn_tx": "0",
                "ls_link_advertised_rx": "0",
                "ls_link_advertised_tx": "0",
                "ls_link_withdrawn_rx": "0",
                "ls_link_withdrawn_tx": "0",
                "ls_node_advertised_rx": "0",
                "ls_node_advertised_tx": "0",
                "ls_node_withdrawn_rx": "0",
                "ls_node_withdrawn_tx": "0",
                "malformed_as_path": "0",
                "malformed_attribute_list": "0",
                "messages_rx": "5",
                "messages_tx": "5",
                "missing_well_known_attribute": "0",
                "non_acceptable_hold_times_rx": "0",
                "notify_rx": "0",
                "notify_tx": "0",
                "open_rx": "1",
                "open_tx": "1",
                "openconfirm_state": "0",
                "opentx_state": "0",
                "optional_attribute_error": "0",
                "port_name": "1/11/2",
                "route_withdraws_rx": "0",
                "routes_advertised": "1",
                "routes_rx": "1",
                "routes_rx_graceful_restart": "0",
                "routes_withdrawn": "0",
                "session_flap_count": "0",
                "sessions_configured": "1",
                "sessions_down": "0",
                "sessions_established": "1",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "starts_occurred": "1",
                "state_machine_errors_rx": "0",
                "state_machine_errors_tx": "0",
                "status": "started",
                "unrecognized_well_known_attribute": "0",
                "unspecified_error_rx": "0",
                "unspecified_error_tx": "0",
                "unsupported_parameters_rx": "0",
                "unsupported_versions_rx": "0",
                "update_errors_rx": "0",
                "update_errors_tx": "0",
                "update_rx": "1",
                "update_tx": "1"
            }
        },
        "Device Group 1": {
            "aggregate": {
                "Hold_timer_expireds_rx": "0",
                "active_state": "0",
                "as_routing_loop": "0",
                "attribute_flags_error": "0",
                "attribute_length_error": "0",
                "authentication_failures_rx": "0",
                "bad_bgp_id_rx": "0",
                "bad_message_length": "0",
                "bad_message_type": "0",
                "bad_peer_as_rx": "0",
                "ceases_rx": "0",
                "ceases_tx": "0",
                "connect_state": "0",
                "connection_not_synchronized": "0",
                "error_link_state_nlri_rx": "0",
                "established_state": "1",
                "external_connects_accepted": "1",
                "external_connects_rx": "1",
                "graceful_restart_attempted": "0",
                "graceful_restart_failed": "0",
                "header_errors_rx": "0",
                "header_errors_tx": "0",
                "hold_timer_expireds_tx": "0",
                "idle_state": "0",
                "invalid_header_suberror_unspecified": "0",
                "invalid_network_field": "0",
                "invalid_next_hop_attribute": "0",
                "invalid_open_suberror_unspecified": "0",
                "invalid_opens_rx": "0",
                "invalid_opens_tx": "0",
                "invalid_origin_attribute": "0",
                "invalid_update_suberror_unspecified": "0",
                "keepalive_rx": "3",
                "keepalive_tx": "3",
                "ls_ipv4_prefix_advertised_rx": "0",
                "ls_ipv4_prefix_advertised_tx": "0",
                "ls_ipv4_prefix_withdrawn_rx": "0",
                "ls_ipv4_prefix_withdrawn_tx": "0",
                "ls_ipv6_prefix_advertised_rx": "0",
                "ls_ipv6_prefix_advertised_tx": "0",
                "ls_ipv6_prefix_withdrawn_rx": "0",
                "ls_ipv6_prefix_withdrawn_tx": "0",
                "ls_link_advertised_rx": "0",
                "ls_link_advertised_tx": "0",
                "ls_link_withdrawn_rx": "0",
                "ls_link_withdrawn_tx": "0",
                "ls_node_advertised_rx": "0",
                "ls_node_advertised_tx": "0",
                "ls_node_withdrawn_rx": "0",
                "ls_node_withdrawn_tx": "0",
                "malformed_as_path": "0",
                "malformed_attribute_list": "0",
                "messages_rx": "5",
                "messages_tx": "5",
                "missing_well_known_attribute": "0",
                "non_acceptable_hold_times_rx": "0",
                "notify_rx": "0",
                "notify_tx": "0",
                "open_rx": "1",
                "open_tx": "1",
                "openconfirm_state": "0",
                "opentx_state": "0",
                "optional_attribute_error": "0",
                "route_withdraws_rx": "0",
                "routes_advertised": "1",
                "routes_rx": "1",
                "routes_rx_graceful_restart": "0",
                "routes_withdrawn": "0",
                "session_flap_count": "0",
                "sessions_configured": "1",
                "sessions_down": "0",
                "sessions_established": "1",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "starts_occurred": "1",
                "state_machine_errors_rx": "0",
                "state_machine_errors_tx": "0",
                "status": "started",
                "unrecognized_well_known_attribute": "0",
                "unspecified_error_rx": "0",
                "unspecified_error_tx": "0",
                "unsupported_parameters_rx": "0",
                "unsupported_versions_rx": "0",
                "update_errors_rx": "0",
                "update_errors_tx": "0",
                "update_rx": "1",
                "update_tx": "1"
            }
        },
        "asn": "100",
        "ip_address": "\"3.3.3.1\"",
        "keepalive_rx": "3",
        "keepalive_tx": "3",
        "notify_rx": "0",
        "notify_tx": "0",
        "open_rx": "1",
        "open_tx": "1",
        "peers": "3.3.3.2",
        "routes_advertised_rx": "1",
        "routes_advertised_tx": "1",
        "routes_withdrawn_rx": "0",
        "routes_withdrawn_tx": "0",
        "sessions_configured": "1",
        "sessions_established": "1",
        "status": "1",
        "update_rx": "1",
        "update_tx": "1"
    }

    Common Return Keys:
        "status"
        "asn"
        "ip_address"
        "keepalive_rx"
        "keepalive_tx"
        "notify_rx"
        "notify_tx"
        "open_rx"
        "open_tx"
        "peers"
        "routes_advertised_rx"
        "routes_advertised_tx"
        "routes_withdrawn_rx"
        "routes_withdrawn_tx"
        "sessions_configured"
        "sessions_established"
        "update_rx"
        "update_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    key_list = list(args.keys())
    for key in key_list:
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'stats'
        stats.update(rt_handle.invoke('emulation_bgp_info', **args))
        args['mode'] = 'learned_info'
        stats.update(rt_handle.invoke('emulation_bgp_info', **args))
        args['mode'] = 'settings'
        stats.update(rt_handle.invoke('emulation_bgp_info', **args))
        args['mode'] = 'session'
        stats.update(rt_handle.invoke('emulation_bgp_info', **args))
        args['mode'] = 'neighbors'
        stats.update(rt_handle.invoke('emulation_bgp_info', **args))
        args['mode'] = 'stats_per_device_group'
        stats.update(rt_handle.invoke('emulation_bgp_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                if 'established_state' in ret[index][key]['aggregate']:
                    ret[index]['sessions_established'] = ret[index][key]['aggregate']['established_state']
                if 'keepalive_rx' in ret[index][key]['aggregate']:
                    ret[index]['keepalive_rx'] = ret[index][key]['aggregate']['keepalive_rx']
                if 'keepalive_tx' in ret[index][key]['aggregate']:
                    ret[index]['keepalive_tx'] = ret[index][key]['aggregate']['keepalive_tx']
                if 'routes_rx' in ret[index][key]['aggregate']:
                    ret[index]['routes_advertised_rx'] = ret[index][key]['aggregate']['routes_rx']
                if 'routes_advertised' in ret[index][key]['aggregate']:
                    ret[index]['routes_advertised_tx'] = ret[index][key]['aggregate']['routes_advertised']
                if 'route_withdraws_rx' in ret[index][key]['aggregate']:
                    ret[index]['routes_withdrawn_rx'] = ret[index][key]['aggregate']['route_withdraws_rx']
                if 'routes_withdrawn' in ret[index][key]['aggregate']:
                    ret[index]['routes_withdrawn_tx'] = ret[index][key]['aggregate']['routes_withdrawn']
                if 'notify_rx' in ret[index][key]['aggregate']:
                    ret[index]['notify_rx'] = ret[index][key]['aggregate']['notify_rx']
                if 'notify_tx' in ret[index][key]['aggregate']:
                    ret[index]['notify_tx'] = ret[index][key]['aggregate']['notify_tx']
                if 'open_rx' in ret[index][key]['aggregate']:
                    ret[index]['open_rx'] = ret[index][key]['aggregate']['open_rx']
                if 'open_tx' in ret[index][key]['aggregate']:
                    ret[index]['open_tx'] = ret[index][key]['aggregate']['open_tx']
                if 'update_rx' in ret[index][key]['aggregate']:
                    ret[index]['update_rx'] = ret[index][key]['aggregate']['update_rx']
                if 'update_tx' in ret[index][key]['aggregate']:
                    ret[index]['update_tx'] = ret[index][key]['aggregate']['update_tx']
                if 'sessions_configured' in ret[index][key]['aggregate']:
                    ret[index]['sessions_configured'] = ret[index][key]['aggregate']['sessions_configured']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bgp_route_config(
        rt_handle,
        aggregator=jNone,
        handle=jNone,
        ip_version=jNone,
        ipv6_prefix_length=jNone,
        max_route_ranges=jNone,
        next_hop_ip_version=jNone,
        next_hop_set_mode=jNone,
        num_routes=jNone,
        origin=jNone,
        originator_id_enable=jNone,
        packing_to=jNone,
        rd_admin_value=jNone,
        rd_assign_step=jNone,
        route_handle=jNone,
        target=jNone,
        target_assign=jNone,
        prefix=jNone,
        mode=jNone,
        as_path=jNone,
        netmask=jNone,
        originator_id=jNone,
        rd_assign_value=jNone,
        rd_type=jNone,
        target_type=jNone,
        route_ip_addr_step=jNone,
        srte_ip_version=jNone,
        srte_aspath_segment_type=jNone,
        srte_community=jNone,
        srte_distinguisher=jNone,
        srte_endpoint=jNone,
        srte_local_pref=jNone,
        srte_nexthop=jNone,
        srte_origin=jNone,
        srte_policy_color=jNone,
        srte_binding_sid=jNone,
        srte_binding_sid_len=jNone,
        srte_color=jNone,
        srte_flags=jNone,
        srte_preference=jNone,
        srte_remote_endpoint_addr=jNone,
        srte_remote_endpoint_as=jNone,
        srte_segment_list_subtlv=jNone,
        srte_weight=jNone,
        ipv4_mpls_vpn_nlri=jNone,
        ipv4_unicast_nlri=jNone,
        label_id=jNone,
        label_incr_mode=jNone,
        label_step=jNone,
        local_pref=jNone,
        next_hop=jNone,
        min_lables=jNone,
        vpls_nlri=jNone,
        l2_enable_vlan=jNone,
        l2_vlan_id=jNone,
        label_block_offset=jNone,
        cluster_list_enable=jNone,
        end_of_rib=jNone,
        as_path_set_mode=jNone,
        enable_as_path=jNone,
        enable_local_pref=jNone,
        next_hop_enable=jNone,
        mtu=jNone,
        origin_route_enable=jNone,
        label_value=jNone,
        rd_admin_value_step=jNone,
        num_sites=jNone,
        prefix_step=jNone,
        l2_vlan_id_incr=jNone,
        target_count=jNone,
        target_step=jNone,
        communities_enable=jNone,
        next_hop_ip_step=jNone,
        srte_enable_route_target=jNone,
        srte_route_target=jNone,
        srte_aspath=jNone,
        route_type=jNone,
        srte_ipv6_endpoint=jNone,
        srte_ipv6_nexthop=jNone,
        srte_type1_label=jNone,
        srte_type1_sbit=jNone,
        srte_type1_segment_type=jNone,
        label_start=jNone,
        advertise_as_bgp_3107=jNone):
        #Below arguments are not supported by spirent,
        #when spirent adds this arguments can be uncommented
        #enable_traditional_nlri=jNone,
        #prefix_from=jNone,
        #prefix_to=jNone,
        #rd_assign_value_step_across_vrfs=jNone,
        #rd_assign_value_step=jNone,
        #no_write=jNone,
        #packing_from=jNone,
        #next_hop_mode=jNone,
        #prefix_step=jNone,
        #import_target_type=jNone,
        #import_target=jNone,
        #import_target_assign=jNone
    """
    :param rt_handle:       RT object
    :param aggregator
    :param handle
    :param ip_version
    :param ipv6_prefix_length - <1-128>
    :param max_route_ranges
    :param next_hop_ip_version
    :param next_hop_set_mode - <same|manual>
    :param num_routes
    :param origin - <igp|egp|incomplete>
    :param originator_id_enable
    :param packing_to - <0-65535>
    :param rd_admin_value
    :param rd_assign_step
    :param route_handle
    :param target
    :param target_assign
    :param prefix
    :param mode - <add|modify|remove>
    :param as_path
    :param netmask
    :param originator_id
    :param rd_assign_value
    :param rd_type - <0-1>
    :param target_type
    :param route_ip_addr_step
    :param srte_ip_version
    :param srte_aspath_segment_type
    :param srte_community - <NO_EXPORT|NO_ADVERTISE>
    :param srte_distinguisher
    :param srte_endpoint
    :param srte_local_pref
    :param srte_nexthop
    :param srte_origin - <igp|egp|incomplete>
    :param srte_policy_color
    :param srte_binding_sid
    :param srte_binding_sid_len - <length_0|length_4|length_16>
    :param srte_color
    :param srte_flags - <color|preference|binding_sid|remote_endpoint>
    :param srte_preference
    :param srte_remote_endpoint_addr
    :param srte_remote_endpoint_as
    :param srte_segment_list_subtlv - <weight|0>
    :param srte_weight
    :param ipv4_mpls_vpn_nlri
    :param ipv4_unicast_nlri
    :param label_id - <0-16777215>
    :param label_incr_mode - <fixed|prefix>
    :param label_step - <0-16777215>
    :param local_pref - <0-4294927695>
    :param next_hop
    :param min_lables - <1-65535>
    :param vpls_nlri
    :param l2_enable_vlan
    :param l2_vlan_id - <0-4095>
    :param l2_vlan_id_incr - <1-4094>
    :param label_block_offset - <1-65535>
    :param cluster_list_enable
    :param end_of_rib
    :param as_path_set_mode
    :param enable_as_path - <1>
    :param enable_local_pref - <1>
    :param next_hop_enable - <1>
    :param mtu
    :param origin_route_enable - <1>
    :param label_value - <0-1048575>
    :param rd_admin_value_step
    :param num_sites
    :param prefix_step
    :param target_count
    :param target_step
    :param communities_enable - <0|1>
    :param next_hop_ip_step
    :param srte_enable_route_target - <true|false>
    :param srte_route_target
    :param srte_aspath
    :param route_type
    :param srte_ipv6_endpoint
    :param srte_ipv6_nexthop
    :param srte_type1_label - <0-1048575>
    :param srte_type1_sbit - <0|1>
    :param srte_type1_segment_type
    :param label_start
    :param advertise_as_bgp_3107
    :return response from rt_handle.invoke(<parameters>)
    #Below arguments are not supported by spirent,
    #when spirent adds this arguments can be uncommented
    #enable_traditional_nlri
    #prefix_from
    #prefix_to
    #rd_assign_value_step_across_vrfs
    #rd_assign_value_step
    #rd_count
    #rd_count_per_vrf
    #prefix_step_across_vrfs
    #no_write
    #packing_from
    #next_hop_mode
    #import_target_type
    #import_target
    #import_target_assign

    Spirent Returns:
    {
        "handles": "bgpipv4routeconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "bgp_routes": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/bgpIPRouteProperty:2/item:1",
        "handles": "/topology:1/deviceGroup:1/networkGroup:1",
        "ip_routes": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/bgpIPRouteProperty:2",
        "macpool_ip_prefix": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1",
        "network_group_handle": "/topology:1/deviceGroup:1/networkGroup:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    global NETWORK_TO_BGP_HANDLES

    args = dict()
    args['aggregator'] = aggregator
    args['handle'] = handle
    args['ip_version'] = ip_version
    args['max_route_ranges'] = max_route_ranges
    args['next_hop_ip_version'] = next_hop_ip_version
    args['next_hop_set_mode'] = next_hop_set_mode
    args['num_routes'] = num_routes
    args['origin'] = origin
    args['originator_id_enable'] = originator_id_enable
    args['packing_to'] = packing_to
    args['rd_admin_value'] = rd_admin_value
    args['rd_assign_step'] = rd_assign_step
    args['route_handle'] = route_handle
    args['target'] = target
    args['target_assign'] = target_assign
    args['prefix'] = prefix
    args['mode'] = mode
    args['as_path'] = as_path
    args['netmask'] = netmask_to_length(netmask) if re.match(r'^\d+\.\d+\.\d+\.\d+$', netmask) else netmask
    args['originator_id'] = originator_id
    args['rd_assign_value'] = rd_assign_value
    args['rd_type'] = rd_type
    args['target_type'] = target_type
    args['route_ip_addr_step'] = route_ip_addr_step
    args['srte_ip_version'] = srte_ip_version
    args['srte_aspath_segment_type'] = srte_aspath_segment_type
    args['srte_distinguisher'] = srte_distinguisher
    args['srte_community'] = srte_community
    args['srte_endpoint'] = srte_endpoint
    args['srte_local_pref'] = srte_local_pref
    args['srte_nexthop'] = srte_nexthop
    args['srte_origin'] = srte_origin
    args['srte_policy_color'] = srte_policy_color
    args['srte_binding_sid'] = srte_binding_sid
    args['srte_binding_sid_len'] = srte_binding_sid_len
    args['srte_color'] = srte_color
    args['srte_flags'] = srte_flags
    args['srte_preference'] = srte_preference
    args['srte_remote_endpoint_addr'] = srte_remote_endpoint_addr
    args['srte_remote_endpoint_as'] = srte_remote_endpoint_as
    args['srte_segment_list_subtlv'] = srte_segment_list_subtlv
    args['srte_weight'] = srte_weight
    args['ipv4_mpls_vpn_nlri'] = ipv4_mpls_vpn_nlri
    args['ipv4_unicast_nlri'] = ipv4_unicast_nlri
    args['label_id'] = label_id
    args['label_incr_mode'] = label_incr_mode
    args['label_step'] = label_step
    args['local_pref'] = local_pref
    args['next_hop_ipv4' if re.match(r'^\d+.\d+.\d+.\d+$', next_hop) else 'next_hop'] = next_hop
    args['min_lables'] = min_lables
    args['vpls_nlri'] = vpls_nlri
    args['l2_enable_vlan'] = l2_enable_vlan
    args['l2_vlan_id'] = l2_vlan_id
    args['label_block_offset'] = label_block_offset
    args['cluster_list_enable'] = cluster_list_enable
    args['end_of_rib '] = end_of_rib
    args['as_path_set_mode'] = as_path_set_mode
    args['enable_as_path'] = enable_as_path
    args['enable_local_pref'] = enable_local_pref
    args['next_hop_enable'] = next_hop_enable
    args['mtu'] = mtu
    args['origin_route_enable'] = origin_route_enable
    args['label_value'] = label_value
    args['rd_admin_value_step'] = rd_admin_value_step
    args['num_sites'] = num_sites
    args['prefix_step'] = prefix_step
    args['l2_vlan_id_incr'] = l2_vlan_id_incr
    args['target_count'] = target_count
    args['target_step'] = target_step
    args['communities_enable'] = communities_enable
    args['next_hop_ip_step'] = next_hop_ip_step
    args['srte_enable_route_target'] = srte_enable_route_target
    args['srte_route_target'] = srte_route_target
    args['srte_aspath'] = srte_aspath
    args['route_type'] = route_type
    args['srte_ipv6_endpoint'] = srte_ipv6_endpoint
    args['srte_ipv6_nexthop'] = srte_ipv6_nexthop
    args['srte_type1_label'] = srte_type1_label
    args['srte_type1_sbit'] = srte_type1_sbit
    args['srte_type1_segment_type'] = srte_type1_segment_type
    args['label_start'] = label_start
    args['advertise_as_bgp_3107'] = advertise_as_bgp_3107

    # Below arguments are not supported by spirent,
    #when spirent adds this arguments can be uncommented
    #args['enable_traditional_nlri'] = enable_traditional_nlri
    #args['prefix_from'] = prefix_from
    #args['prefix_to'] = prefix_to
    #args['rd_assign_value_step_across_vrfs'] = rd_assign_value_step_across_vrfs
    #args['rd_assign_value_step'] = rd_assign_value_step
    #args['rd_count'] = rd_count
    #args['rd_count_per_vrf'] = rd_count_per_vrf
    #args['prefix_step_across_vrfs'] = prefix_step_across_vrfs
    #args['no_write'] = no_write
    #args['packing_from'] = packing_from
    #args['next_hop_mode'] = next_hop_mode
    #args['prefix_step'] = prefix_step
    #args['import_target_type'] = import_target_type
    #args['import_target'] = import_target
    #args['import_target_assign'] = import_target_assign

    # ***** Argument Modification *****
    if 'ipv6' in handle or ip_version == 6 or ip_version == '6':
        args['prefix_from'] = ipv6_prefix_length
    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_bgp_route_config.__doc__, **args)
    if args.get('netmask'):
        args['prefix_from'] = args.pop('netmask')
    if args.get('min_lables'):
        args['num_labels'] = args.pop('min_lables')

    if args.get('next_hop_ipv4') and args.get('next_hop_ip_step'):
        nargs = dict()
        nargs['pattern'] = 'counter'
        nargs['counter_start'] = args.get('next_hop_ipv4')
        nargs['counter_step'] = args.pop('next_hop_ip_step')
        nargs['counter_direction'] = 'increment'
        _result_ = rt_handle.invoke('multivalue_config', **nargs)
        args['next_hop_ipv4'] = _result_['multivalue_handle']

    if args.get('next_hop') and args.get('next_hop_ip_step'):
        nargs = dict()
        nargs['pattern'] = 'counter'
        nargs['counter_start'] = args.pop('next_hop')
        nargs['counter_step'] = args.pop('next_hop_ip_step')
        nargs['counter_direction'] = 'increment'
        _result_ = rt_handle.invoke('multivalue_config', **nargs)
        args['next_hop_ipv6'] = _result_['multivalue_handle']

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if as_path_set_mode != jNone:
        if as_path_set_mode in ['include_as_seq', 'sequence']:
            args['as_path_set_mode'] = 'include_as_seq'
        elif as_path_set_mode in ['include_as_set', 'set']:
            args['as_path_set_mode'] = 'include_as_set'
        elif as_path_set_mode in ['include_as_seq_conf', 'confed_seq']:
            args['as_path_set_mode'] = 'include_as_seq_conf'
        elif as_path_set_mode in ['include_as_set_conf', 'confed_set']:
            args['as_path_set_mode'] = 'include_as_set_conf'
        elif as_path_set_mode == 'custom':
            raise ValueError("INVALID VALUE , PLEASE PROVIDE THE CORRECT VALUE")

    nargs = dict()
    srteArgs = ['enableLocalPreference', 'enableOrigin', 'srte_endpoint', 'srte_ip_version', 'srte_nexthop', 'srte_local_pref',
                'enableNextHop', 'setNextHopIpType', 'srte_origin', 'srte_aspath_segment_type', 'srte_policy_color', 'srte_distinguisher',
                'srte_community', 'srte_remote_endpoint_addr', 'enableColor', 'srte_preference', 'enablePref', 'srte_binding_sid',
                'enableRemoteEndPoint', 'srte_remote_endpoint_as', 'srte_color', 'enableBinding', 'srte_binding_sid_len',
                'srte_segment_list_subtlv', 'srte_weight', 'srte_flags', 'srte_enable_route_target', 'srte_route_target',
                'srte_aspath', 'route_type', 'srte_ipv6_endpoint', 'srte_ipv6_nexthop', 'srte_type1_label', 'srte_type1_sbit',
                'srte_type1_segment_type']

    vrf_args = dict()
    vrfArgsList = ['ipv4_mpls_vpn_nlri', 'ipv6_mpls_vpn_nlri', 'max_route_ranges', 'num_sites', 'target', 'target_step', 'target_assign',
                   'target_type', 'import_rt_as_export_rt', 'target_count', 'import_target_count', 'import_target', 'import_target_step',
                   'import_target_assign', 'import_target_type']

    key_list = list(args.keys())
    for key in key_list:
        if key in srteArgs:
            nargs[key] = args[key]
            del args[key]

    key_list = list(args.keys())
    for key in key_list:
        if key in vrfArgsList:
            vrf_args[key] = args[key]
            del args[key]

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        if mode == 'withdraw':
            raise ValueError("mode withdraw is not supported.Supported values add|modify|remove")
        if mode == 'modify' and 'networkGroup' in hndl:
            args['handle'] = get_bgp_route_property(rt_handle, hndl)
        if nargs:
            if mode == 'add':
                nargs['handle'] = hndl
                invoke_ixnet(rt_handle, 'setAttribute', nargs['handle'], "-numberSRTEPolicies", 1)
                invoke_ixnet(rt_handle, 'commit')
            if mode == 'modify':
                ntwrkGroupHandle = __get_parent_handle(hndl, 'networkGroup')
                if ntwrkGroupHandle != jNone:
                    if ntwrkGroupHandle in NETWORK_TO_BGP_HANDLES.keys():
                        nargs['handle'] = NETWORK_TO_BGP_HANDLES[ntwrkGroupHandle]
                    else:
                        raise Exception("Could not retrieve the BGP handle for the provided network group handle {}".format(ntwrkGroupHandle))
                else:
                    raise Exception("Could not retrieve the BGP handle for the provided handle {}".format(hndl))
            __config_bgp_srte(rt_handle, nargs)
        if mode == 'add':
            nargs = dict()
            nargs['mode'] = 'create'
            nargs['protocol_handle'] = __get_parent_handle(hndl, "deviceGroup")
            nargs['enable_device'] = 1
            nargs['type'] = "ipv4-prefix" if ip_version == 4 or ip_version == '4' else "ipv6-prefix"
            vrf_type = "bgpVrf" if "ipv4" in hndl else "bgpV6Vrf"
            if len(vrf_args) != 0:
                bgp_hndl = hndl
                hndl = invoke_ixnet(rt_handle, 'getList', hndl, vrf_type)
                if len(hndl) == 0:
                    hndl = invoke_ixnet(rt_handle, 'add', bgp_hndl, vrf_type)
                    invoke_ixnet(rt_handle, 'commit')
                    hndl = invoke_ixnet(rt_handle, 'remapIds', hndl)
                vrf_args['mode'] = 'modify'
                vrf_args['handle'] = hndl
                rt_handle.invoke('emulation_bgp_route_config', **vrf_args)
                vrf_args.pop('handle')
            args.pop('ip_version')
            nargs['connected_to_handle'] = hndl
            netGroup = rt_handle.invoke('network_group_config', **nargs)
            pool = "ipv"+str(ip_version)+"_prefix_pools_handle"
            if netGroup.get(pool):
                bgpproperty = "bgpIPRouteProperty" if "ipv4" in hndl else "bgpV6IPRouteProperty"
                if len(vrf_args) != 0:
                    bgpproperty = "bgpL3VpnRouteProperty" if "ipv4" in nargs['type'] else "bgpV6L3VpnRouteProperty"
                bgprouteproperty = rt_handle._invokeIxNet("getList", netGroup[pool], bgpproperty)
                if not len(bgprouteproperty):
                    raise Exception("Error: No Property handle in the child list {}".format(bgpproperty))
            else:
                raise Exception("ERROR: could not retrieve bgp property handle")
            args['mode'] = 'modify'
            args['handle'] = bgprouteproperty
            args.update(vrf_args)
            retDict = rt_handle.invoke('emulation_bgp_route_config', **args)
            if len(bgprouteproperty) > 1:
                retDict['ip_routes'] = bgprouteproperty
            else:
                retDict['ip_routes'] = bgprouteproperty[0]
            netGroup.pop('status')
            retDict.update(netGroup)
            ret.append(retDict)
            if re.search("ipv4", ret[-1]['ip_routes']):
                v4_handles.append(ret[-1]['network_group_handle'])
                NETWORK_TO_BGP_HANDLES[ret[-1]['network_group_handle']] = hndl
            elif re.search("ipv6", ret[-1]['ip_routes']):
                v6_handles.append(ret[-1]['network_group_handle'])
                NETWORK_TO_BGP_HANDLES[ret[-1]['network_group_handle']] = hndl
        else:
            ret.append(rt_handle.invoke('emulation_bgp_route_config', **args))

        # if re.search("ipv4", ret[-1]['ip_routes']):
            # v4_handles.append(ret[-1]['network_group_handle'])
            # NETWORK_TO_BGP_HANDLES[ret[-1]['network_group_handle']] = hndl
        # elif re.search("ipv6", ret[-1]['ip_routes']):
            # v6_handles.append(ret[-1]['network_group_handle'])
            # NETWORK_TO_BGP_HANDLES[ret[-1]['network_group_handle']] = hndl

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'network_group_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['network_group_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_config(
        rt_handle,
        dhcp6_reb_timeout=jNone,
        dhcp6_rel_max_rc=jNone,
        dhcp6_rel_timeout=jNone,
        dhcp6_ren_max_rt=jNone,
        dhcp6_ren_timeout=jNone,
        dhcp6_req_max_rc=jNone,
        dhcp6_req_max_rt=jNone,
        dhcp6_req_timeout=jNone,
        dhcp6_sol_max_rc=jNone,
        dhcp6_sol_max_rt=jNone,
        dhcp6_sol_timeout=jNone,
        handle=jNone,
        ip_version=jNone,
        release_rate=jNone,
        request_rate=jNone,
        retry_count=jNone,
        mode=jNone,
        dhcp6_reb_max_rt=jNone,
        outstanding_session_count=jNone,
        msg_timeout=jNone,
        broadcast_bit_flag=jNone,
        relay_agent_ip_addr=jNone,
        server_ip_addr=jNone,
        dhcp6_request_rate=jNone,
        dhcp6_release_rate=jNone,
        circuit_id=jNone,
        remote_id=jNone,
        client_id=jNone,
        dhcp_range_use_relay_agent=jNone,
        client_id_type=jNone,
        port_handle=jNone,
        outstanding_releases_count=jNone):

        # ****Arguments added below are supported in Ixia but not in Spirent****
        # ****Uncomment once the support is present in Spirent *****
        #
        # override_global_setup_rate=jNone,
        # server_port=jNone,
        # dhcp6_echo_ia_info=jNone,
        # msg_timeout_factor=jNone,
        # override_global_teardown_rate=jNone,

    """
    :param rt_handle:       RT object
    :param dhcp6_reb_timeout - <1-100>
    :param dhcp6_rel_max_rc - <1-32>
    :param dhcp6_rel_timeout - <1-100>
    :param dhcp6_ren_max_rt - <1-10000>
    :param dhcp6_ren_timeout - <1-100>
    :param dhcp6_req_max_rc - <1-32>
    :param dhcp6_req_max_rt - <1-10000>
    :param dhcp6_req_timeout - <1-100>
    :param dhcp6_sol_max_rc - <1-32>
    :param dhcp6_sol_max_rt - <1-10000>
    :param dhcp6_sol_timeout - <1-100>
    :param handle
    :param ip_version - <4|6>
    :param release_rate - <1-10000>
    :param request_rate - <1-10000>
    :param retry_count - <1-32>
    :param mode - <create|modify|reset>
    :param dhcp6_reb_max_rt - <1-10000>
    :param outstanding_session_count - <1-2048>
    :param msg_timeout - <1000-65535>
    :param broadcast_bit_flag - <0|1>
    :param relay_agent_ip_addr
    :param server_ip_addr
    :param dhcp6_request_rate - <1-10000>
    :param dhcp6_release_rate - <1-10000>
    :param circuit_id
    :param remote_id
    :param client_id
    :param dhcp_range_use_relay_agent - <0|1>
    :param client_id_type - <0-255>
    :param port_handle
    :param outstanding_releases_count - <1-1000>

    Spirent Returns:
    {
        "handle": {
            "port1": "dhcpv4portconfig1"
        },
        "handles": "dhcpv4portconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/dhcpv4client:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    nargs = dict()
    tlvArgs = dict()
    args['dhcp6_reb_timeout'] = dhcp6_reb_timeout
    args['dhcp6_rel_max_rc'] = dhcp6_rel_max_rc
    args['dhcp6_rel_timeout'] = dhcp6_rel_timeout
    args['dhcp6_ren_max_rt'] = dhcp6_ren_max_rt
    args['dhcp6_ren_timeout'] = dhcp6_ren_timeout
    args['dhcp6_req_max_rc'] = dhcp6_req_max_rc
    args['dhcp6_req_max_rt'] = dhcp6_req_max_rt
    args['dhcp6_req_timeout'] = dhcp6_req_timeout
    args['dhcp6_sol_max_rc'] = dhcp6_sol_max_rc
    args['dhcp6_sol_max_rt'] = dhcp6_sol_max_rt
    args['dhcp6_sol_timeout'] = dhcp6_sol_timeout
    args['handle'] = handle
    args['ip_version'] = ip_version
    args['release_rate'] = release_rate
    args['request_rate'] = request_rate
    args['retry_count'] = retry_count
    args['mode'] = mode
    args['outstanding_session_count'] = outstanding_session_count
    args['dhcp6_reb_max_rt'] = dhcp6_reb_max_rt
    args['msg_timeout'] = msg_timeout
    args['dhcp6_request_rate'] = dhcp6_request_rate
    args['dhcp6_release_rate'] = dhcp6_release_rate
    nargs['dhcp_range_use_relay_agent'] = dhcp_range_use_relay_agent
    nargs['broadcast_bit_flag'] = broadcast_bit_flag
    nargs['relay_agent_ip_addr'] = relay_agent_ip_addr
    nargs['server_ip_addr'] = server_ip_addr
    tlvArgs['circuit_id'] = circuit_id
    tlvArgs['remote_id'] = remote_id
    tlvArgs['client_id'] = client_id
    tlvArgs['client_id_type'] = client_id_type
    args['outstanding_releases_count'] = outstanding_releases_count


    # ****Arguments added below are supported in Ixia but not in Spirent****
    # ****Uncomment once the support is present in Spirent *****
    #
    # args['override_global_setup_rate'] = override_global_setup_rate
    # args['server_port'] = server_port
    # args['dhcp6_echo_ia_info'] = dhcp6_echo_ia_info
    # args['msg_timeout_factor'] = msg_timeout_factor
    # args['override_global_teardown_rate'] = override_global_teardown_rate
    # args['outstanding_releases_count'] = outstanding_releases_count

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_dhcp_config.__doc__, **args)
    if args.get('dhcp6_request_rate'):
        args['request_rate'] = args.pop('dhcp6_request_rate')
    if args.get('dhcp6_release_rate'):
        args['release_rate'] = args.pop('dhcp6_release_rate')
    if args.get('ip_version'):
        args['ip_version'] = args.pop('ip_version')
    else:
        args['ip_version'] = 4

    nargs = get_arg_value(rt_handle, j_emulation_dhcp_config.__doc__, **nargs)
    if nargs.get('broadcast_bit_flag'):
        nargs['dhcp4_broadcast'] = nargs.pop('broadcast_bit_flag')
    if nargs.get('relay_agent_ip_addr'):
        nargs['dhcp_range_relay_first_address'] = nargs.pop('relay_agent_ip_addr')
    if nargs.get('server_ip_addr'):
        nargs['dhcp_range_server_address'] = nargs.pop('server_ip_addr')

    tlvArgs = get_arg_value(rt_handle, j_emulation_dhcp_config.__doc__, **tlvArgs)

    class DhcpConfigObject:
        def __init__(self, args, group_args, tlv_args):
            self.args = args
            self.group_args = group_args
            self.tlv_args = tlv_args
            self.ip_version = None
            self.dhcp_handle = None
            self.client_handle = None
            self.relay_handle = None

    ret = dict()
    if mode == 'create':
        if port_handle != jNone:
            topo_handle = create_topology(rt_handle, port_handle)
        elif handle != jNone:
            topo_handle = __get_parent_handle(handle, 'deviceGroup')
        else:
            __check_and_raise(port_handle)
        args.pop('mode')
        obj = DhcpConfigObject(args=args, group_args=nargs, tlv_args=tlvArgs)
        obj.dhcp_handle = topo_handle
        obj.ip_version = args['ip_version']
        ret['handles'] = obj
        ret['status'] = 1
    else:
        __check_and_raise(handle)
        if 'DhcpConfigObject' in str(handle.__class__):
            if handle.client_handle is None and handle.relay_handle is None:
                handle.args.update(args)
                handle.group_args.update(nargs)
                handle.tlv_args.update(tlvArgs)
                return {'status' : 1}
            else:
                args['handle'] = handle.client_handle
        ret.update(rt_handle.invoke('emulation_dhcp_config', **args))
    # ***** Return Value Modification *****
    # if len(ret) == 1:
        # ret = ret[0]

    # ***** End of Return Value Modification *****
    return ret


def j_emulation_dhcp_group_config(
        rt_handle,
        dhcp6_range_duid_enterprise_id=jNone,
        dhcp6_range_ia_t1=jNone,
        dhcp6_range_ia_t2=jNone,
        handle=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        num_sessions=jNone,
        qinq_incr_mode=jNone,
        vlan_id=jNone,
        vlan_id_count=jNone,
        vlan_id_outer_count=jNone,
        vlan_id_outer_step=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        dhcp_range_ip_type=jNone,
        encap=jNone,
        dhcp_range_server_address=jNone,
        dhcp_range_relay_first_address=jNone,
        dhcp4_broadcast=jNone,
        rapid_commit_mode=jNone,
        dhcp_range_use_relay_agent=jNone,
        dhcp6_range_duid_type=jNone,
        duid_value=jNone,
        dhcp6_client_mode=jNone,
        dhcp_range_relay_count=jNone,
        dhcp_range_relay_destination=jNone,
        dhcp6_range_duid_vendor_id=jNone,
        dhcp6_range_duid_vendor_id_increment=jNone,
        dhcp6_range_ia_id=jNone,
        dhcp6_range_ia_id_increment=jNone,
        dhcp6_range_ia_type=jNone,
        dhcp_range_relay_gateway=jNone,
        dhcp_range_param_request_list=jNone,
        dhcp_range_relay_first_vlan_id=jNone,
        dhcp_range_relay_vlan_count=jNone,
        dhcp_range_relay_vlan_increment=jNone,
        dhcp_range_relay_address_increment=jNone,
        dhcp_range_relay_subnet=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_priority=jNone,
        circuit_id=jNone,
        remote_id=jNone,
        enable_ldra=jNone,
        enable_reconfig_accept=jNone,
        circuit_id_enable=jNone,
        remote_id_enable=jNone,
        enable_router_option=jNone,
        dst_addr_type=jNone):
    """
    :param rt_handle:       RT object
    :param dhcp6_range_duid_enterprise_id
    :param dhcp6_range_ia_t1
    :param dhcp6_range_ia_t2
    :param handle
    :param mac_addr
    :param mac_addr_step
    :param num_sessions - <1-65536>
    :param qinq_incr_mode - <inner|outer|both>
    :param vlan_id - <1-4095>
    :param vlan_id_count - <1-4095>
    :param vlan_id_outer_count - <1-4094>
    :param vlan_id_outer_step - <1-4094>
    :param vlan_id_step - <1-4095>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|reset>
    :param dhcp_range_ip_type - <4:ipv4|6:ipv6>
    :param encap - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq|vc_mux|llcsnap>
    :param dhcp_range_server_address
    :param dhcp_range_relay_first_address
    :param dhcp4_broadcast - <0|1>
    :param rapid_commit_mode - <ENABLE:1|DISABLE:0>
    :param dhcp_range_use_relay_agent - <0|1>
    :param dhcp6_range_duid_type - <en:duid_en|ll:duid_ll|llt:duid_llt|EN:duid_en|LL:duid_ll|LLT:duid_llt>
    :param duid_value
    :param dhcp6_client_mode - <DHCPV6:iana|DHCPV6ANDPD:iana_iapd|DHCPPD:iapd>
    :param dhcp_range_relay_count -  <1-65536>
    :param dhcp_range_relay_destination
    :param dhcp6_range_duid_vendor_id
    :param dhcp6_range_duid_vendor_id_increment
    :param dhcp6_range_ia_id
    :param dhcp6_range_ia_id_increment
    :param dhcp6_range_ia_type - <DHCPV6:iana|DHCPV6ANDPD:iana_iapd|DHCPPD:iapd>
    :param dhcp_range_relay_gateway
    :param dhcp_range_param_request_list
    :param dhcp_range_relay_first_vlan_id - <1-4095>
    :param dhcp_range_relay_vlan_count - <1-4094>
    :param dhcp_range_relay_vlan_increment - <1-4093>
    :param dhcp_range_relay_address_increment
    :param dhcp_range_relay_subnet
    :param vlan_id_outer - <1-4094>
    :param vlan_id_outer_priority - <0-7>
    :param circuit_id
    :param remote_id
    :param enable_ldra - <true|false>
    :param enable_reconfig_accept - <true|false>
    :param circuit_id_enable - <true:1|false:0>
    :param remote_id_enable - <true:1|false:0>
    :param enable_router_option - <true:1|false:0>
    :param dst_addr_type - <ALL_DHCP_RELAY_AGENTS_AND_SERVERS|ALL_DHCP_SERVERS>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "dhcpv4blockconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/dhcpv4client:1/item:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    vlan_args = dict()
    tlvArgs = dict()
    args['dhcp6_range_duid_enterprise_id'] = dhcp6_range_duid_enterprise_id
    args['dhcp6_range_ia_t1'] = dhcp6_range_ia_t1
    args['dhcp6_range_ia_t2'] = dhcp6_range_ia_t2
    args['handle'] = handle
    args['mac_addr'] = mac_addr
    args['mac_addr_step'] = mac_addr_step
    args['num_sessions'] = num_sessions
    vlan_args['qinq_incr_mode'] = qinq_incr_mode
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_count'] = vlan_id_count
    vlan_args['vlan_id_inner_count'] = vlan_id_outer_count
    vlan_args['vlan_id_inner_step'] = vlan_id_outer_step
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['dhcp_range_ip_type'] = dhcp_range_ip_type
    args['encap'] = encap
    args['dhcp_range_server_address'] = dhcp_range_server_address
    args['dhcp_range_relay_first_vlan_id'] = dhcp_range_relay_first_vlan_id
    args['dhcp_range_relay_vlan_count'] = dhcp_range_relay_vlan_count
    args['dhcp_range_relay_vlan_increment'] = dhcp_range_relay_vlan_increment
    args['dhcp_range_relay_address_increment'] = dhcp_range_relay_address_increment
    args['dhcp_range_relay_subnet'] = dhcp_range_relay_subnet
    args['vlan_id_outer'] = vlan_id_outer
    args['vlan_id_outer_priority'] = vlan_id_outer_priority
    args['enable_ldra'] = enable_ldra
    args['dhcp4_broadcast'] = dhcp4_broadcast
    args['dhcp_range_use_relay_agent'] = dhcp_range_use_relay_agent
    args['dhcp6_range_duid_type'] = dhcp6_range_duid_type
    args['dhcp_range_relay_count'] = dhcp_range_relay_count
    args['dhcp6_range_duid_vendor_id'] = dhcp6_range_duid_vendor_id
    args['dhcp6_range_duid_vendor_id_increment'] = dhcp6_range_duid_vendor_id_increment
    args['dhcp6_range_ia_id'] = dhcp6_range_ia_id
    args['dhcp6_range_ia_id_increment'] = dhcp6_range_ia_id_increment
    args['dhcp6_range_ia_type'] = dhcp6_range_ia_type
    args['dhcp6_client_mode'] = dhcp6_client_mode
    args['dhcp_range_relay_destination'] = dhcp_range_relay_destination
    args['dhcp_range_relay_first_address'] = dhcp_range_relay_first_address
    args['dhcp_range_relay_gateway'] = dhcp_range_relay_gateway
    args['dst_addr_type'] = dst_addr_type

    args = get_arg_value(rt_handle, j_emulation_dhcp_group_config.__doc__, **args)
    vlan_args = get_arg_value(rt_handle, j_emulation_dhcp_group_config.__doc__, **vlan_args)

    if args.get('enable_ldra') in ['true', True] and args.get('dhcp_range_ip_type') == 'ipv6':
        args['dhcp_range_relay_type'] = 'lightweight'
        args['dhcp_range_use_relay_agent'] = '1'
    elif args.get('enable_ldra') in ['false', False]:
        args['dhcp_range_relay_type'] = 'normal'
    if args.get('enable_ldra'):
        args.pop('enable_ldra')

    if args.get('encap') == 'None':
        args['encap'] = 'ethernet_ii'
    if args.get('rapid_commit_mode'):
        args['use_rapid_commit'] = args.pop('rapid_commit_mode')
    if args.get('duid_value'):
        tlvArgs['duid_type'] = 'custom'
        duid_value = str(hex(int(args.pop('duid_value'))))
        tlvArgs['duid_value'] = duid_value
    if args.get('dhcp6_client_mode'):
        args['dhcp6_range_ia_type'] = args.pop('dhcp6_client_mode')

    if args.get('dst_addr_type') == 'ALL_DHCP_RELAY_AGENTS_AND_SERVERS':
        args['dhcp6_gateway_address'] = 'ff02::1:2'
        args.pop('dst_addr_type')
    elif args.get('dst_addr_type') == 'ALL_DHCP_SERVERS':
        args['dhcp6_gateway_address'] = 'ff05::1:3'
        args.pop('dst_addr_type')

    def create_multivalue(arg_value):
        nargs = dict()
        nargs['pattern'] = 'single_value'
        nargs['single_value'] = arg_value
        result = rt_handle.invoke('multivalue_config', **nargs)
        return result['multivalue_handle']
    if args.get('dhcp_range_use_relay_agent') == '1' and \
       args.get('dhcp_range_ip_type') == 'ipv6' and \
       args['dhcp_range_relay_type'] != 'lightweight':
        mul = create_multivalue('2000:0:1:1::2' if args.get('dhcp_range_relay_destination') is 'None' else args.get('dhcp_range_relay_destination'))
        args['dhcp_range_relay_destination'] = mul
        mul = create_multivalue('2000:0:1:1::2' if args.get('dhcp_range_relay_first_address') is 'None' else args.get('dhcp_range_relay_first_address'))
        args['dhcp_range_relay_first_address'] = mul
        mul = create_multivalue(args.get('dhcp_range_relay_gateway') if args.get('dhcp_range_relay_gateway') else '2000:0:1:1::2')
        args['dhcp_range_relay_gateway'] = mul
    else:
        if args.get('dhcp_range_relay_destination'):
            args['dhcp_range_relay_destination'] = args.pop('dhcp_range_relay_destination')
        if args.get('dhcp_range_relay_first_address'):
            args['dhcp_range_relay_first_address'] = args.pop('dhcp_range_relay_first_address')
        if args.get('dhcp_range_relay_gateway'):
            args['dhcp_range_relay_gateway'] = args.pop('dhcp_range_relay_gateway')
    tlvArgs['circuit_id'] = circuit_id
    tlvArgs['remote_id'] = remote_id
    tlvArgs['enable_reconfig_accept'] = enable_reconfig_accept
    tlvArgs['circuit_id_enable'] = circuit_id_enable
    tlvArgs['remote_id_enable'] = remote_id_enable
    tlvArgs['enable_router_option'] = enable_router_option
    tlvArgs = get_arg_value(rt_handle, j_emulation_dhcp_group_config.__doc__, **tlvArgs)
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    __check_and_raise(handle)
    # if not isinstance(handle, list):
        # handle = [handle]
    # handle = list(set(handle))

    ret = dict()
    client_handle, relay_handle, client_eth, relay_eth, eth_upper_handles = None, None, None, None, list()
    if mode == 'create':
        if 'DhcpConfigObject' in str(handle.__class__):
            if 'deviceGroup' in handle.dhcp_handle:
                handle.dhcp_handle = create_deviceGroup(rt_handle, handle.dhcp_handle, num_sessions)['device_group_handle']
            args['handle'] = handle.dhcp_handle
            group_args = handle.group_args
            group_args.update(args)
            args.update(group_args)
            tlv_args = handle.tlv_args
            tlv_args.update(tlvArgs)
            tlvArgs.update(tlv_args)
            ret.update(rt_handle.invoke('emulation_dhcp_group_config', **args))
            handle.client_handle = ret.get('dhcpv{}client_handle'.format(handle.ip_version))
            client_handle = handle.client_handle
            handle.relay_handle = ret.get('dhcpv{}relayagent_handle'.format(handle.ip_version))
            relay_handle = handle.relay_handle
            nargs = dict()
            nargs['mode'] = 'modify'
            nargs['handle'] = client_handle
            if handle.args.get('handle'):
                handle.args.pop('handle')
            nargs.update(handle.args)
            rt_handle.invoke('emulation_dhcp_config', **nargs)
            client_eth = __get_parent_handle(client_handle, 'ethernet')
            if relay_handle is not None:
                relay_eth = __get_parent_handle(relay_handle, 'ethernet')
            ret['handles'] = handle
        else:
            stack = traceback.extract_stack()
            try:
                filename, lineno, function, code = stack[-3]
            except:
                function = None
            if function is not 'j_emulation_dhcp_config':
                raise ValueError("Please call j_emulation_dhcp_config() " + \
                "before j_emulation_dhcp_group_config() call")
        if len(vlan_args.keys()) > 0:
            vlan_args['mode'] = 'modify'
            vlan_args['vlan'] = 1 if encap == 'ethernet_ii_vlan' or encap == 'ethernet_ii_qinq' else 0
            # if encap == 'ethernet_ii_qinq':
            vlan_args['protocol_handle'] = __get_parent_handle("".join(handle), 'ethernet') if client_eth is None else client_eth
            rt_handle.invoke('interface_config', **vlan_args)
            if relay_eth is not None:
                vlan_args['protocol_handle'] = relay_eth
                rt_handle.invoke('interface_config', **vlan_args)
    else:
        new_handle = client_handle = handle
        if 'DhcpConfigObject' in str(handle.__class__):
            new_handle = client_handle = handle.client_handle
            relay_handle = handle.relay_handle
            args['handle'] = [client_handle] if handle.relay_handle is None else [client_handle, relay_handle]
            client_eth = __get_parent_handle(client_handle, 'ethernet')
            if relay_handle is not None:
                relay_eth = __get_parent_handle(relay_handle, 'ethernet')
        if mode == 'reset':
            eth_handle = __get_parent_handle(new_handle, 'ethernet')
            eth_length = len(eth_handle.split('/'))
            handles_dict = list(rt_handle.invoke('protocol_info', mode='handles').keys())
            pattern = re.compile(r"{}.*".format(eth_handle))
            match_list = list(filter(pattern.match, handles_dict))
            eth_upper_handles = [each_handle for each_handle in match_list \
                                   if len(each_handle.split('/')) == eth_length+1]
        if len(eth_upper_handles) != 1:
            ret.update(rt_handle.invoke('emulation_dhcp_group_config', **args))
        else:
            invoke_ixnet(rt_handle, 'remove', __get_parent_handle(new_handle, "deviceGroup"))
            invoke_ixnet(rt_handle, "commit")
        if mode != 'reset':
            if len(vlan_args.keys()) > 0:
                vlan_args['mode'] = 'modify'
                vlan_args['vlan'] = 1
                vlan_args['protocol_handle'] = __get_parent_handle("".join(handle), 'ethernet') if client_eth is None else client_eth
                rt_handle.invoke('interface_config', **vlan_args)
                if relay_eth is not None:
                    vlan_args['protocol_handle'] = relay_eth
                    rt_handle.invoke('interface_config', **vlan_args)
    if dhcp_range_param_request_list is not jNone:
        for i in dhcp_range_param_request_list:
            tlvConfig(rt_handle, client_handle, {'dhcp_range_param_request_list' : str(i)})
    if len(tlvArgs.keys()) > 0:
        tlvConfig(rt_handle, client_handle, tlvArgs)
    return ret


def j_emulation_dhcp_control(
        rt_handle,
        handle=jNone,
        port_handle=jNone,
        action=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle
    :param action

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['action'] = action

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_dhcp_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        # args['handle'] = hndl
        if 'DhcpConfigObject' in str(hndl.__class__):
            client_handle = hndl.client_handle
            relay_handle = hndl.relay_handle
            args['handle'] = [client_handle] if hndl.relay_handle is None else [client_handle, relay_handle]
        else:
            args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_dhcp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_server_config(
        rt_handle,
        count=jNone,
        dhcp_offer_options=jNone,
        handle=jNone,
        ip_prefix_length=jNone,
        ip_prefix_step=jNone,
        ip_repeat=jNone,
        ip_version=jNone,
        lease_time=jNone,
        local_mac=jNone,
        port_handle=jNone,
        qinq_incr_mode=jNone,
        vlan_id=jNone,
        vlan_id_count=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        ipaddress_pool=jNone,
        ipaddress_count=jNone,
        mode=jNone,
        ip_address=jNone,
        ip_step=jNone,
        ip_gateway=jNone,
        remote_mac=jNone,
        vlan_id_mode=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone,
        prefix_pool_start_addr=jNone):
    """
    :param rt_handle:       RT object
    :param count - <1-100000>
    :param dhcp_offer_options - <0|1>
    :param handle
    :param ip_prefix_length - <0-32>
    :param ip_prefix_step
    :param ip_repeat
    :param ip_version - <4|6>
    :param lease_time - <300-30000000>
    :param local_mac
    :param port_handle
    :param qinq_incr_mode - <inner|outer|both>
    :param vlan_id - <0-4095>
    :param vlan_id_count - <1-4095>
    :param vlan_id_step - <0-4095>
    :param vlan_user_priority - <0-7>
    :param ipaddress_pool
    :param ipaddress_count
    :param mode - <create|modify|reset>
    :param ip_address
    :param ip_step
    :param ip_gateway
    :param remote_mac
    :param vlan_id_mode - <fixed|increment>
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <0-4095>
    :param vlan_outer_user_priority - <0-7>
    :param prefix_pool_start_addr

    Spirent Returns:
    {
        "handle": {
            "dhcp_handle": "host3",
            "port_handle": "port2"
        },
        "handles": "host3",
        "status": "1"
    }

    IXIA Returns:
    {
        "dhcpv4server_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/dhcpv4server:1",
        "handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/dhcpv4server:1/item:1",
        "handles": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/dhcpv4server:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    vlan_args = dict()
    args['count'] = count
    args['dhcp_offer_options'] = dhcp_offer_options
    args['handle'] = handle
    args['ip_prefix_length'] = ip_prefix_length
    args['ip_prefix_step'] = ip_prefix_step
    args['ip_repeat'] = ip_repeat
    args['ip_version'] = ip_version
    args['lease_time'] = lease_time
    args['local_mac'] = local_mac
    args['port_handle'] = port_handle
    args['qinq_incr_mode'] = qinq_incr_mode
    args['ipaddress_pool'] = ipaddress_pool
    args['ipaddress_count'] = ipaddress_count
    args['mode'] = mode
    args['ip_address'] = ip_address
    args['ip_step'] = ip_step
    args['ip_gateway'] = ip_gateway
    args['remote_mac'] = remote_mac
    args['prefix_pool_start_addr'] = prefix_pool_start_addr
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_count'] = vlan_id_count
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_user_priority'] = vlan_user_priority
    vlan_args['vlan_id_mode'] = vlan_id_mode
    vlan_args['vlan_outer_id'] = vlan_outer_id
    vlan_args['vlan_outer_id_mode'] = vlan_outer_id_mode
    vlan_args['vlan_outer_id_step'] = vlan_outer_id_step
    vlan_args['vlan_outer_user_priority'] = vlan_outer_user_priority

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_dhcp_server_config.__doc__, **args)
    if args.get('ip_version') == '6' and args.get('ip_gateway'):
        args['ipv6_gateway'] = args.pop('ip_gateway')
    if args.get('remote_mac'):
        args['manual_gateway_mac'] = args.pop('remote_mac')

    if re.match(r"\d+\/\d+\/\d+", handle):
        args['port_handle'] = handle

    if args.get('prefix_pool_start_addr'):
        args['ipaddress_pool'] = prefix_pool_start_addr

    if mode == 'create':
        if args.get('port_handle'):
            handle = create_deviceGroup(rt_handle, args.pop('port_handle'))
            handle = handle['device_group_handle']
        elif args.get('handle'):
            deviceGroup_hndl = __get_parent_handle(handle, 'deviceGroup')
            handle = create_deviceGroup(rt_handle, deviceGroup_hndl)['device_group_handle']
        elif not args.get('handle'):
            raise Exception("Please pass either handle or port_handle to the function call")

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if mode == 'reset':
        nargs = dict()
        nargs['action'] = 'stop_all_protocols'
        nargs['handle'] = handle
        rt_handle.invoke('test_control', **nargs)
        sleep(5)

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_dhcp_server_config', **args))
        if vlan_args:
            if mode == 'create':
                if 'dhcpv4server_handle' in ret[-1]:
                    vlan_config(rt_handle, vlan_args, ret[-1]['dhcpv4server_handle'])
                elif 'dhcpv6server_handle' in ret[-1]:
                    vlan_config(rt_handle, vlan_args, ret[-1]['dhcpv6server_handle'])
            else:
                vlan_config(rt_handle, vlan_args, hndl)

    # ***** Return Value Modification *****

    if mode == 'create':
        for index in range(len(ret)):
            if 'dhcpv4server_handle' in ret[index]:
                ret[index]['handles'] = ret[index]['dhcpv4server_handle']
                v4_handles.append(ret[index]['dhcpv4server_handle'])
            elif 'dhcpv6server_handle' in ret[index]:
                ret[index]['handles'] = ret[index]['dhcpv6server_handle']
                v6_handles.append(ret[index]['dhcpv6server_handle'])

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_dhcp_server_control(
        rt_handle,
        action=jNone,
        handle=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param action
    :param handle
    :param port_handle

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['dhcp_handle'] = handle
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    if action == 'start':
        args['action'] = 'collect'
    elif action == 'stop':
        args['action'] = 'reset'

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['dhcp_handle'] = hndl
        ret.append(rt_handle.invoke('emulation_dhcp_server_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_server_stats(rt_handle, action=jNone, handle=jNone,
                                  ip_version=jNone, port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param action
    :param handle
    :param ip_version
    :param port_handle

    Spirent Returns:
    {
        "aggregate": {
            "ack": "1",
            "decline": "0",
            "discover": "1",
            "host3": {
                "rx": {
                    "decline": "0",
                    "discover": "1",
                    "inform": "0",
                    "release": "0",
                    "request": "1"
                }
            },
            "inform": "0",
            "nak": "0",
            "offer": "1",
            "offer_count": "1",
            "release": "0",
            "release_count": "0",
            "request": "1"
        },
        "dhcp_handle": {
            "host3": {
                "tx": {
                    "ack": "1",
                    "nak": "0",
                    "offer": "1"
                }
            }
        },
        "dhcp_server_state": "UP",
        "status": "1"
    },
    {
        "aggregate": {
            "current_bound_count": "1",
            "release_count": "0",
            "rx_confirm_count": "0",
            "rx_decline_count": "0",
            "rx_info_request_count": "0",
            "rx_rebind_count": "0",
            "rx_release_count": "0",
            "rx_renew_count": "0",
            "rx_request_count": "1",
            "rx_soilicit_count": "1",
            "total_bound_count": "1",
            "total_expired_count": "0",
            "total_release_count": "0",
            "total_renewed_count": "0",
            "tx_advertise_count": "1",
            "tx_reconfigure_count": "0",
            "tx_reconfigure_rebind_count": "0",
            "tx_reconfigure_renew_count": "0",
            "tx_reply_count": "1"
        },
        "dhcp_server_state": "UP",
        "ipv6": {
            "dhcp_handle": {
                "host4": {
                    "current_bound_count": "1",
                    "rx_confirm_count": "0",
                    "rx_decline_count": "0",
                    "rx_info_request_count": "0",
                    "rx_rebind_count": "0",
                    "rx_release_count": "0",
                    "rx_renew_count": "0",
                    "rx_request_count": "1",
                    "rx_soilicit_count": "1",
                    "total_bound_count": "1",
                    "total_expired_count": "0",
                    "total_release_count": "0",
                    "total_renewed_count": "0",
                    "tx_advertise_count": "1",
                    "tx_reconfigure_count": "0",
                    "tx_reconfigure_rebind_count": "0",
                    "tx_reconfigure_renew_count": "0",
                    "tx_reply_count": "1"
                }
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "Device Group 3": {
            "aggregate": {
                "bind/rapid_commit_count": "0",
                "bind_count": "1",
                "force_renew_count": "0",
                "offer_count": "1",
                "release_count": "0",
                "renew_count": "0",
                "session_total": "1",
                "sessions_down": "0",
                "sessions_not_started": "0",
                "sessions_up": "1",
                "status": "started"
            }
        },
        "aggregate": {
            "bind/rapid_commit_count": "0",
            "bind_count": "1",
            "force_renew_count": "0",
            "offer_count": "1",
            "release_count": "0",
            "renew_count": "0",
            "session_total": "1",
            "sessions_down": "0",
            "sessions_not_started": "0",
            "sessions_up": "1",
            "status": "started"
        },
        "status": "1"
    },
    {
        "Device Group 4": {
            "aggregate": {
                "status": "started"
            }
        },
        "aggregate": {
            "status": "started"
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['dhcp_handle'] = handle
    args['ip_version'] = ip_version
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
#    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['dhcp_handle'] = hndl
        ret.append(rt_handle.invoke('emulation_dhcp_server_stats', **args))

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                ret[index]['aggregate'] = ret[index][key]['aggregate']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_stats(rt_handle, handle=jNone, port_handle=jNone,
                           action=jNone, dhcp_version=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle
    :param action
    :param dhcp_version

    Spirent Returns:
    {
        "aggregate": {
            "ack_rx_count": "1",
            "attempted_rate": "0",
            "average_setup_time": "0.01307518",
            "bind_rate": "75.8329491130578",
            "bound_renewed": "0",
            "currently_attempting": "0",
            "currently_bound": "1",
            "currently_idle": "0",
            "discover_tx_count": "1",
            "elapsed_time": "0.01326492",
            "maximum_setup_time": "0.01307518",
            "minimum_setup_time": "0.01307518",
            "nak_rx_count": "0",
            "offer_rx_count": "1",
            "release_tx_count": "0",
            "request_tx_count": "1",
            "success_percentage": "100",
            "total_attempted": "1",
            "total_bound": "1",
            "total_failed": "0",
            "total_retried": "0"
        },
        "group": {
            "dhcpv4blockconfig1": {
                "1": {
                    "discover_resp_time": "0.00952004",
                    "error_status": "OK",
                    "ipv4_addr": "1.1.1.10",
                    "lease_left": "290.39396338",
                    "lease_rx": "300",
                    "mac_addr": "00:10:94:00:00:02",
                    "request_resp_time": "0.00355514",
                    "session_state": "BOUND",
                    "vci": "32",
                    "vlan_id": "1",
                    "vpi": "0"
                },
                "ack_rx_count": "1",
                "attempt_rate": "0",
                "bind_rate": "75.8329491130578",
                "bound_renewed": "0",
                "currently_attempting": "0",
                "currently_bound": "1",
                "currently_idle": "0",
                "discover_tx_count": "1",
                "elapsed_time": "0.01326492",
                "nak_rx_count": "0",
                "offer_rx_count": "1",
                "release_rate": "-",
                "release_tx_count": "0",
                "request_rate": "-",
                "request_tx_count": "1",
                "total_attempted": "1",
                "total_bound": "1",
                "total_failed": "0",
                "total_retried": "0"
            }
        },
        "session": {
            "dhcpv4blockconfig1": {
                "ack_rx_count": "1",
                "address": "1.1.1.10",
                "attempt_rate": "0",
                "bind_rate": "75.8329491130578",
                "bound_renewed": "0",
                "currently_attempting": "0",
                "currently_bound": "1",
                "currently_idle": "0",
                "discover_resp_time": "0.00952004",
                "discover_tx_count": "1",
                "elapsed_time": "0.01326492",
                "error_status": "OK",
                "ipv4_addr": "1.1.1.10",
                "lease_left": "290.39396338",
                "lease_rx": "300",
                "lease_time": "300",
                "mac_addr": "00:10:94:00:00:02",
                "nak_rx_count": "0",
                "offer_rx_count": "1",
                "release_rate": "-",
                "release_tx_count": "0",
                "request_rate": "-",
                "request_resp_time": "0.00355514",
                "request_tx_count": "1",
                "session_state": "BOUND",
                "total_attempted": "1",
                "total_bound": "1",
                "total_failed": "0",
                "total_retried": "0",
                "vci": "32",
                "vlan_id": "1",
                "vpi": "0"
            }
        },
        "status": "1"
    },
    {
        "aggregate": {
            "adv_rx_count": "1",
            "avg_rebind_repl_time": "0",
            "avg_release_repl_time": "0",
            "avg_renew_repl_time": "0",
            "avg_request_repl_time": "3.24344",
            "avg_soli_adv_time": "18.7403",
            "avg_soli_repl_time": "1004.3191",
            "currently_attempting": "0",
            "currently_bound": "1",
            "currently_idle": "0",
            "elapsed_time": "2.00734522",
            "info_request_tx_count": "0",
            "max_rebind_repl_time": "0",
            "max_release_repl_time": "0",
            "max_renew_repl_time": "0",
            "max_request_repl_time": "3.24344",
            "max_soli_adv_time": "18.7403",
            "max_soli_repl_time": "1004.3191",
            "min_rebind_repl_time": "0",
            "min_release_repl_time": "0",
            "min_renew_repl_time": "0",
            "min_request_repl_time": "3.24344",
            "min_soli_adv_time": "18.7403",
            "min_soli_repl_time": "1004.3191",
            "prefix_count": "1",
            "rebind_rate": "0",
            "release_tx_count": "0",
            "renew_rate": "0",
            "reply_rx_count": "1",
            "request_tx_count": "1",
            "setup_fail": "0",
            "setup_initiated": "1",
            "setup_success": "1",
            "setup_success_rate": "0.995699474400118",
            "solicits_tx_count": "1",
            "state": "BOUND"
        },
        "ipv6": {
            "aggregate": {
                "adv_rx_count": "1",
                "avg_rebind_repl_time": "0",
                "avg_release_repl_time": "0",
                "avg_renew_repl_time": "0",
                "avg_request_repl_time": "3.24344",
                "avg_soli_adv_time": "18.7403",
                "avg_soli_repl_time": "1004.3191",
                "currently_attempting": "0",
                "currently_bound": "1",
                "currently_idle": "0",
                "elapsed_time": "2.00734522",
                "info_request_tx_count": "0",
                "max_rebind_repl_time": "0",
                "max_release_repl_time": "0",
                "max_renew_repl_time": "0",
                "max_request_repl_time": "3.24344",
                "max_soli_adv_time": "18.7403",
                "max_soli_repl_time": "1004.3191",
                "min_rebind_repl_time": "0",
                "min_release_repl_time": "0",
                "min_renew_repl_time": "0",
                "min_request_repl_time": "3.24344",
                "min_soli_adv_time": "18.7403",
                "min_soli_repl_time": "1004.3191",
                "prefix_count": "1",
                "rebind_rate": "0",
                "release_tx_count": "0",
                "renew_rate": "0",
                "reply_rx_count": "1",
                "request_tx_count": "1",
                "setup_fail": "0",
                "setup_initiated": "1",
                "setup_success": "1",
                "setup_success_rate": "0.995699474400118",
                "solicits_tx_count": "1",
                "state": "BOUND"
            },
            "dhcpv6blockconfig1": {
                "1": {
                    "dhcpv6_ipv6_addr": "abcd::10",
                    "dhcpv6_lease_left": "289.9923833",
                    "dhcpv6_lease_rx": "300",
                    "dhcpv6_prefix_length": "0",
                    "dhcpv6_session_state": "BOUND",
                    "dhcpv6_status_code": "OK",
                    "dhcpv6_status_string": "",
                    "ipv6_addr": "abcd::10",
                    "lease_left": "289.9923833",
                    "lease_rx": "300",
                    "mac_addr": "00:10:94:00:00:02",
                    "pd_ipv6_addr": "::",
                    "pd_lease_left": "0",
                    "pd_lease_rx": "0",
                    "pd_prefix_length": "0",
                    "pd_session_state": "IDLE",
                    "pd_status_code": "OK",
                    "pd_status_string": "",
                    "request_resp_time": "0.00324344",
                    "session_index": "0",
                    "session_state": "BOUND",
                    "solicit_resp_time": "0.0187403",
                    "status_code": "OK",
                    "status_string": "",
                    "vlan_id": ""
                }
            }
        },
        "session": {
            "dhcpv6blockconfig1": {
                "address": "abcd::10",
                "dhcpv6_ipv6_addr": "abcd::10",
                "dhcpv6_lease_left": "289.9923833",
                "dhcpv6_lease_rx": "300",
                "dhcpv6_prefix_length": "0",
                "dhcpv6_session_state": "BOUND",
                "dhcpv6_status_code": "OK",
                "dhcpv6_status_string": "",
                "ipv6_addr": "abcd::10",
                "lease_left": "289.9923833",
                "lease_rx": "300",
                "lease_time": "300",
                "mac_addr": "00:10:94:00:00:02",
                "pd_ipv6_addr": "::",
                "pd_lease_left": "0",
                "pd_lease_rx": "0",
                "pd_prefix_length": "0",
                "pd_session_state": "IDLE",
                "pd_status_code": "OK",
                "pd_status_string": "",
                "request_resp_time": "0.00324344",
                "session_index": "0",
                "session_state": "BOUND",
                "solicit_resp_time": "0.0187403",
                "status_code": "OK",
                "status_string": "",
                "vlan_id": ""
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "1/11/2": {
            "aggregate": {
                "ack_rx_count": "1",
                "addr_discovered": "1",
                "average_setup_time": "1.00",
                "avgerage_teardown_rate": "0.00",
                "currently_attempting": "1",
                "currently_bound": "1",
                "currently_idle": "0",
                "declines_tx_count": "0",
                "discover_tx_count": "1",
                "enabled_interfaces": "1",
                "nak_rx_count": "0",
                "offer_rx_count": "1",
                "port_name": "1/11/2",
                "release_tx_count": "0",
                "request_tx_count": "1",
                "rx": {
                    "force_renew": "0"
                },
                "sessions_not_started": "0",
                "sessions_total": "1",
                "setup_fail": "0",
                "setup_initiated": "1",
                "setup_success": "1",
                "success_percentage": "100",
                "teardown_failed": "0",
                "teardown_initiated": "0",
                "teardown_success": "0",
                "total_attempted": "1",
                "total_failed": "0"
            }
        },
        "aggregate": {
            "ack_rx_count": "1",
            "addr_discovered": "1",
            "average_setup_time": "1.00",
            "avgerage_teardown_rate": "0.00",
            "currently_attempting": "1",
            "currently_bound": "1",
            "currently_idle": "0",
            "declines_tx_count": "0",
            "discover_tx_count": "1",
            "enabled_interfaces": "1",
            "nak_rx_count": "0",
            "offer_rx_count": "1",
            "port_name": "1/11/2",
            "release_tx_count": "0",
            "request_tx_count": "1",
            "rx": {
                "force_renew": "0"
            },
            "sessions_not_started": "0",
            "sessions_total": "1",
            "setup_fail": "0",
            "setup_initiated": "1",
            "setup_success": "1",
            "success_percentage": "100",
            "teardown_failed": "0",
            "teardown_initiated": "0",
            "teardown_success": "0",
            "total_attempted": "1",
            "total_failed": "0"
        },
        "session": {
            "/topology:1/deviceGroup:1/ethernet:1/dhcpv4client:1/item:1": {
                "Address": "1.1.1.10",
                "Gateway": "removePacket[Unresolved]",
                "Prefix": "24",
                "ack/rapid_commit_rx": "0",
                "ack_rx_count": "1",
                "address": "1.1.1.10",
                "declines_tx_count": "0",
                "device_group": "Device Group 1",
                "device_id": "1",
                "discover/rapid_commit_tx": "0",
                "discover_tx_count": "1",
                "gateway": "0.0.0.0",
                "information": "none",
                "lease/rapid_commit": "No",
                "lease_establishment_time": "6",
                "lease_time": "300",
                "nak_rx_count": "0",
                "offer_rx_count": "1",
                "protocol": "DHCPv4 Client 1",
                "release_tx_count": "0",
                "request_tx_count": "1",
                "rx": {
                    "force_renew": "0"
                },
                "status": "Up",
                "topology": "Topology 1"
            }
        },
        "status": "1"
    },
    {
        "1/11/2": {
            "aggregate": {
                "addr_discovered": "1",
                "adv_ignored": "0",
                "adv_rx_count": "1",
                "average_setup_time": "0.48",
                "avgerage_teardown_rate": "0.00",
                "currently_attempting": "1",
                "currently_bound": "1",
                "currently_idle": "0",
                "enabled_interfaces": "1",
                "information_request_tx": "0",
                "port_name": "1/11/2",
                "rebinds_tx": "0",
                "reconfigure_rx": "0",
                "release_tx_count": "0",
                "renew_tx": "0",
                "reply_rx_count": "1",
                "request_tx_count": "1",
                "rx": {
                    "nak": "0"
                },
                "sessions_not_started": "0",
                "sessions_total": "1",
                "setup_fail": "0",
                "setup_initiated": "1",
                "setup_success": "1",
                "solicits_tx_count": "1",
                "success_percentage": "100",
                "teardown_failed": "0",
                "teardown_initiated": "0",
                "teardown_success": "0",
                "total_attempted": "1",
                "total_failed": "0"
            }
        },
        "aggregate": {
            "addr_discovered": "1",
            "adv_ignored": "0",
            "adv_rx_count": "1",
            "average_setup_time": "0.48",
            "avgerage_teardown_rate": "0.00",
            "currently_attempting": "1",
            "currently_bound": "1",
            "currently_idle": "0",
            "enabled_interfaces": "1",
            "information_request_tx": "0",
            "port_name": "1/11/2",
            "rebinds_tx": "0",
            "reconfigure_rx": "0",
            "release_tx_count": "0",
            "renew_tx": "0",
            "reply_rx_count": "1",
            "request_tx_count": "1",
            "rx": {
                "nak": "0"
            },
            "sessions_not_started": "0",
            "sessions_total": "1",
            "setup_fail": "0",
            "setup_initiated": "1",
            "setup_success": "1",
            "solicits_tx_count": "1",
            "success_percentage": "100",
            "teardown_failed": "0",
            "teardown_initiated": "0",
            "teardown_success": "0",
            "total_attempted": "1",
            "total_failed": "0"
        },
        "session": {
            "/topology:1/deviceGroup:2/ethernet:1/dhcpv6client:1/item:1": {
                "Address": "abcd:0:0:0:0:0:0:10",
                "Gateway": "removePacket[Unresolved]",
                "NumberOfAddresses": "0",
                "NumberOfPrefixes": "0",
                "Prefix": "removePacket[Unresolved]",
                "PrefixLength": "removePacket[Unresolved]",
                "address": "abcd:0:0:0:0:0:0:10",
                "adv_ignored": "0",
                "adv_rx_count": "1",
                "device_group": "Device Group 2",
                "device_id": "1",
                "dns_search_list": "Not Available",
                "dns_server_list": "Not Available",
                "establishment_time": "1047",
                "gw_addr": "0:0:0:0:0:0:0:0",
                "info_req_tx": "0",
                "information": "none",
                "ip_addr": "abcd:0:0:0:0:0:0:10",
                "lease/rapid_commit": "No",
                "lease_id": "1",
                "lease_time": "300",
                "lease_time_prefix": "0",
                "prefix_addr": "0:0:0:0:0:0:0:0",
                "prefix_len": "0",
                "protocol": "DHCPv6 Client 1",
                "rebinds_tx": "0",
                "reconfigure_rx": "0",
                "release_tx_count": "0",
                "renew_tx": "0",
                "replies/rapid_commit_rx": "0",
                "reply_rx_count": "1",
                "request_tx_count": "1",
                "session_id": "1",
                "solicits/rapid_commit_tx": "0",
                "solicits_tx_count": "1",
                "status": "Up",
                "topology": "Topology 1"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['port_handle'] = port_handle
    args['handle'] = handle
    args['action'] = action
    if dhcp_version == '4':
        args['dhcp_version'] = 'dhcp4'
    elif dhcp_version == '6':
        args['dhcp_version'] = 'dhcp6'

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
#    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if 'DhcpConfigObject' in str(hndl.__class__):
            client_handle = hndl.client_handle
            relay_handle = hndl.relay_handle
            args['handle'] = [client_handle] if hndl.relay_handle is None else [client_handle, relay_handle]
        else:
            args['handle'] = hndl
        stats = dict()
        args['mode'] = 'aggregate_stats'
        stats.update(rt_handle.invoke('emulation_dhcp_stats', **args))
        args['mode'] = 'session'
        stats.update(rt_handle.invoke('emulation_dhcp_stats', **args))
        args['mode'] = 'aggregate_stats_relay_agent'
        stats.update(rt_handle.invoke('emulation_dhcp_stats', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                ret[index]['aggregate'] = ret[index][key]['aggregate']
        if 'session' in ret[index]:
            for key in list(ret[index]['session']):
                if 'ip_addr' in ret[index]['session'][key]:
                    ret[index]['session'][key]['address'] = ret[index]['session'][key]['ip_addr']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_igmp_config(
        rt_handle,
        filter_mode=jNone,
        handle=jNone,
        igmp_version=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_len=jNone,
        ip_router_alert=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        port_handle=jNone,
        count=jNone,
        msg_interval=jNone,
        general_query=jNone,
        group_query=jNone,
        max_response_control=jNone,
        max_response_time=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_mode=jNone,
        vlan_id_outer_step=jNone,
        vlan_outer_user_priority=jNone):
        # Below arguments are not supported by spirent, when spirent adds
        # this functionality the arguments can be uncommented
        # msg_count_per_interval=jNone

    """
    :param rt_handle:       RT object
    :param filter_mode - <include|exclude>
    :param handle
    :param igmp_version - <v1|v2|v3>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_len - <1-32>
    :param ip_router_alert - <0|1>
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4096>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|delete|disable_all>
    :param port_handle
    :param count - <1-65535>
    :param msg_interval - <0-4294967295>
    :param general_query - <1>
    :param group_query - <1>
    :param max_response_time
    :param max_response_control
    :param vlan_id_outer - <0-4095>
    :param vlan_id_outer_mode - <fixed|increment>
    :param vlan_id_outer_step - <0-4096>
    :param vlan_outer_user_priority - <0-7>
    #Below arguments are not supported by spirent, when spirent adds
    #this functionality the arguments can be uncommented
    #msg_count_per_interval

    Spirent Returns:
    {
        "handle": "host2",
        "handles": "igmphostconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1",
        "igmp_host_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1",
        "igmp_host_iptv_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/iptv",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['filter_mode'] = filter_mode
    args['handle'] = handle
    args['igmp_version'] = igmp_version
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_len'] = intf_prefix_len
    args['ip_router_alert'] = ip_router_alert
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['neighbor_intf_ip_addr_step'] = neighbor_intf_ip_addr_step
    args['mode'] = mode
    args['count'] = count
    args['msg_interval'] = msg_interval
    args['general_query'] = general_query
    args['group_query'] = group_query
    args['max_response_control'] = max_response_control
    args['max_response_time'] = max_response_time
    vlan_args = dict()
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_mode'] = vlan_id_mode
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_user_priority'] = vlan_user_priority
    vlan_args['vlan_id_outer'] = vlan_id_outer
    vlan_args['vlan_id_outer_mode'] = vlan_id_outer_mode
    vlan_args['vlan_id_outer_step'] = vlan_id_outer_step
    vlan_args['vlan_outer_user_priority'] = vlan_outer_user_priority

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_igmp_config.__doc__, **args)
    vlan_args = get_arg_value(rt_handle, j_emulation_igmp_config.__doc__, **vlan_args)

    if mode == 'create':
        if port_handle != jNone:
            handle = create_deviceGroup(rt_handle, port_handle, count)['device_group_handle']
        elif handle == jNone:
            raise Exception('Please provide port_handle or handle')
    elif mode == 'modify':
        __check_and_raise(handle)
    else:
        __check_and_raise(handle)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret_value = rt_handle.invoke('emulation_igmp_config', **args)
        ret.append(ret_value)
        eth_handle = None
        if 'ethernet' in hndl:
            eth_handle = __get_parent_handle(hndl, 'ethernet')
        elif ret_value.get('igmp_host_handle') is not None:
            eth_handle = __get_parent_handle(ret_value.get('igmp_host_handle'), 'ethernet')
        if eth_handle is not None:
            if vlan_args:
                vlan_config(rt_handle, vlan_args, eth_handle)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'igmp_host_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['igmp_host_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_igmp_control(rt_handle, handle=jNone,
                             mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <restart|join:start|leave:stop>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_igmp_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_igmp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_igmp_group_config(
        rt_handle,
        group_pool_handle=jNone,
        handle=jNone,
        mode=jNone,
        session_handle=jNone,
        source_pool_handle=jNone,
        g_filter_mode=jNone):
    """
    :param rt_handle:       RT object
    :param group_pool_handle
    :param handle
    :param mode - <create|modify|delete|clear_all>
    :param session_handle
    :param source_pool_handle
    :param g_filter_mode - <include|exclude>

    Spirent Returns:
    {
        "group_handles": "ipv4group1",
        "handle": "igmpgroupmembership1",
        "status": "1"
    }

    IXIA Returns:
    {
        "group_handles": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList",
        "igmp_group_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList",
        "igmp_source_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList/igmpUcastIPv4SourceList",
        "source_handles": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList/igmpUcastIPv4SourceList",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "group_handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['group_pool_handle'] = group_pool_handle
    args['handle'] = handle
    args['mode'] = mode
    args['session_handle'] = session_handle
    args['source_pool_handle'] = source_pool_handle
    args['g_filter_mode'] = g_filter_mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_igmp_group_config.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if source_pool_handle == jNone:
        n_args = dict()
        n_args['mode'] = 'create'
        n_args['num_sources'] = 1
        n_args['handle'] = handle
        n_args['ip_addr_start'] = '0.0.0.0'
        n_ret = rt_handle.invoke('emulation_multicast_source_config', **n_args)
        if 'multicast_source_handle' in n_ret:
            args['source_pool_handle'] = n_ret['multicast_source_handle']

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        if mode == 'create':
            args['session_handle'] = hndl
        ret.append(rt_handle.invoke('emulation_igmp_group_config', **args))

        if mode == 'create':
            n_args = dict()
            n_args['handle'] = ret[-1]['igmp_group_handle']
            n_args['mode'] = 'enable'
            rt_handle.invoke('emulation_igmp_group_config', **n_args)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'igmp_group_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['igmp_group_handle']
        if 'igmp_group_handle' in ret[index]:
            ret[index]['group_handles'] = ret[index]['igmp_group_handle']
        if 'igmp_source_handle' in ret[index]:
            ret[index]['source_handles'] = ret[index]['igmp_source_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_igmp_info(
        rt_handle,
        handle=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle

    Spirent Returns:
    {
        "dropped_pkts": "0",
        "group_membership_stats": {
            "group_addr": {
                "225": {
                    "0": {
                        "0": {
                            "1": {
                                "host_addr": {
                                    "3": {
                                        "3": {
                                            "3": {
                                                "2": {
                                                    "duplicate_join": "false",
                                                    "join_failure": "false",
                                                    "join_latency": "0",
                                                    "join_timestamp": "4Days-03:43:59.31120207",
                                                    "leave_latency": "0",
                                                    "leave_timestamp": "0Days-00:00:00.00000000",
                                                    "state": "IDLE_MEMBER",
                                                    "state_change_timestamp": "4Days-03:44:03.48055190"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "igmpv1_mem_reports_rx": "0",
        "igmpv1_mem_reports_tx": "0",
        "igmpv1_queries_rx": "0",
        "igmpv2_group_queries_rx": "0",
        "igmpv2_leave_tx": "0",
        "igmpv2_mem_reports_rx": "0",
        "igmpv2_mem_reports_tx": "2",
        "igmpv2_queries_rx": "0",
        "igmpv3_group_queries_rx": "0",
        "igmpv3_group_src_queries_rx": "0",
        "igmpv3_mem_reports_rx": "0",
        "igmpv3_mem_reports_tx": "0",
        "igmpv3_queries_rx": "0",
        "invalid_pkts": "0",
        "port_stats": {
            "port2": {
                "-": {
                    "dropped_pkts": "0",
                    "invalid_pkts": "0"
                },
                "V1": {
                    "igmpv1_mem_reports_rx": "0",
                    "igmpv1_mem_reports_tx": "0",
                    "igmpv1_queries_rx": "0"
                },
                "V2": {
                    "igmpv2_group_queries_rx": "0",
                    "igmpv2_leave_tx": "0",
                    "igmpv2_mem_reports_rx": "0",
                    "igmpv2_mem_reports_tx": "2",
                    "igmpv2_queries_rx": "0"
                },
                "V3": {
                    "igmpv3_group_queries_rx": "0",
                    "igmpv3_group_src_queries_rx": "0",
                    "igmpv3_mem_reports_rx": "0",
                    "igmpv3_mem_reports_tx": "0",
                    "igmpv3_queries_rx": "0"
                }
            }
        },
        "session": {
            "igmphostconfig1": {
                "avg_join_latency": "0",
                "avg_leave_latency": "0",
                "max_join_latency": "0",
                "max_leave_latency": "0",
                "min_join_latency": "0",
                "min_leave_latency": "0"
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/item:1": {
            "session": {
                "igmp": {
                    "aggregate": {
                        "gen_query_rx": "1",
                        "grp_query_rx": "0",
                        "invalid_rx": "0",
                        "leave_v2_rx": "0",
                        "leave_v2_tx": "0",
                        "pair_joined": "1",
                        "port_name": "1/11/1",
                        "rprt_v1_rx": "0",
                        "rprt_v1_tx": "0",
                        "rprt_v2_rx": "0",
                        "rprt_v2_tx": "2",
                        "rprt_v3_rx": "0",
                        "rprt_v3_tx": "0",
                        "total_rx": "1",
                        "total_tx": "2",
                        "v3_allow_new_source_rx": "0",
                        "v3_allow_new_source_tx": "0",
                        "v3_block_old_source_rx": "0",
                        "v3_block_old_source_tx": "0",
                        "v3_change_mode_exclude_rx": "0",
                        "v3_change_mode_exclude_tx": "0",
                        "v3_change_mode_include_rx": "0",
                        "v3_change_mode_include_tx": "0",
                        "v3_mode_exclude_rx": "0",
                        "v3_mode_exclude_tx": "0",
                        "v3_mode_include_rx": "0",
                        "v3_mode_include_tx": "0"
                    }
                }
            }
        },
        "Device Group 2": {
            "IGMP Host Stats Per Device": {
                "igmp": {
                    "aggregate": {
                        "gen_query_rx": "1",
                        "grp_query_rx": "0",
                        "invalid_rx": "0",
                        "leave_v2_rx": "0",
                        "leave_v2_tx": "0",
                        "pair_joined": "1",
                        "rprt_v1_rx": "0",
                        "rprt_v1_tx": "0",
                        "rprt_v2_rx": "0",
                        "rprt_v2_tx": "2",
                        "rprt_v3_rx": "0",
                        "rprt_v3_tx": "0",
                        "total_rx": "1",
                        "total_tx": "2",
                        "v3_allow_new_source_rx": "0",
                        "v3_allow_new_source_tx": "0",
                        "v3_block_old_source_rx": "0",
                        "v3_block_old_source_tx": "0",
                        "v3_change_mode_exclude_rx": "0",
                        "v3_change_mode_exclude_tx": "0",
                        "v3_change_mode_include_rx": "0",
                        "v3_change_mode_include_tx": "0",
                        "v3_group_and_source_specific_queries_rx": "0",
                        "v3_mode_exclude_rx": "0",
                        "v3_mode_exclude_tx": "0",
                        "v3_mode_include_rx": "0",
                        "v3_mode_include_tx": "0"
                    }
                },
                "sessions_down": "0",
                "sessions_notstarted": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "status": "started"
            }
        },
        "igmpv1_mem_reports_rx": "0",
        "igmpv1_mem_reports_tx": "0",
        "igmpv2_group_queries_rx": "0",
        "igmpv2_leave_tx": "0",
        "igmpv2_mem_reports_rx": "0",
        "igmpv2_mem_reports_tx": "2",
        "igmpv2_queries_rx": "1",
        "igmpv3_group_src_queries_rx": "0",
        "igmpv3_mem_reports_rx": "0",
        "igmpv3_mem_reports_tx": "0",
        "status": "1"
    },
    {
        "1/11/2": {
            "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:1": {
                "querier_address": "3.3.3.1",
                "querier_version": "v2",
                "record": {
                    "1": {
                        "compatibility_mode": "v2",
                        "compatibility_timer": "0",
                        "filter_mode": "N/A",
                        "group_adress": "225.0.0.1",
                        "group_timer": "247",
                        "source_address": "N/A",
                        "source_timer": "0"
                    }
                }
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
        "igmpv1_mem_reports_rx"
        "igmpv1_mem_reports_tx"
        "igmpv2_group_queries_rx"
        "igmpv2_leave_tx"
        "igmpv2_mem_reports_rx"
        "igmpv2_mem_reports_tx"
        "igmpv2_queries_rx"
        "igmpv3_group_src_queries_rx"
        "igmpv3_mem_reports_rx"
        "igmpv3_mem_reports_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        if args['handle'] in igmp_querier_handles:
            args['mode'] = 'learned_info'
            stats.update(rt_handle.invoke('emulation_igmp_info', **args))
        else:
            args['mode'] = 'aggregate'
            stats.update(rt_handle.invoke('emulation_igmp_info', **args))
            args['mode'] = 'stats_per_session'
            stats.update(rt_handle.invoke('emulation_igmp_info', **args))
            args['mode'] = 'stats_per_device_group'
            stats.update(rt_handle.invoke('emulation_igmp_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        # if handle[index] in session_map:
            # igmp_version = session_map[handle[index]]
        igmp_version = invoke_ixnet(rt_handle, 'getAttribute', handle[index], '-versionType')
        igmp_version = invoke_ixnet(rt_handle, 'getAttribute', igmp_version, '-values')[0]
        for key in list(ret[index]):
            if 'IGMP Host Stats Per Device' in ret[index][key]:
                if 'igmp' in ret[index][key]['IGMP Host Stats Per Device']:
                    if 'aggregate' in ret[index][key]['IGMP Host Stats Per Device']['igmp']:
                        if 'rprt_v1_rx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                            ret[index]['igmpv1_mem_reports_rx'] = ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['rprt_v1_rx']
                        if 'rprt_v1_tx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                            ret[index]['igmpv1_mem_reports_tx'] = ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['rprt_v1_tx']
                        if 'rprt_v2_rx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                            ret[index]['igmpv2_mem_reports_rx'] = ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['rprt_v2_rx']
                        if 'rprt_v2_tx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                            ret[index]['igmpv2_mem_reports_tx'] = ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['rprt_v2_tx']
                        if 'rprt_v3_rx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                            ret[index]['igmpv3_mem_reports_rx'] = ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['rprt_v3_rx']
                        if 'rprt_v3_tx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                            ret[index]['igmpv3_mem_reports_tx'] = ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['rprt_v3_tx']
                        if 'leave_v2_tx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                            ret[index]['igmpv2_leave_tx'] = ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['leave_v2_tx']
                        if 'v3_group_and_source_specific_queries_rx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                            ret[index]['igmpv3_group_src_queries_rx'] = \
                            ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['v3_group_and_source_specific_queries_rx']
                        if igmp_version == 'v1':
                            if 'gen_query_rx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                                ret[index]['igmpv1_queries_rx'] = ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['gen_query_rx']
                        if igmp_version == 'v2':
                            if 'gen_query_rx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                                ret[index]['igmpv2_queries_rx'] = ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['gen_query_rx']
                            if 'grp_query_rx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                                ret[index]['igmpv2_group_queries_rx'] = \
                                ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['grp_query_rx']
                        if igmp_version == 'v3':
                            if 'gen_query_rx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                                ret[index]['igmpv3_queries_rx'] = \
                                ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['gen_query_rx']
                            if 'grp_query_rx' in ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']:
                                ret[index]['igmpv3_group_queries_rx'] = \
                                ret[index][key]['IGMP Host Stats Per Device']['igmp']['aggregate']['grp_query_rx']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_igmp_querier_config(
        rt_handle,
        handle=jNone,
        igmp_version=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_len=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        query_interval=jNone,
        robustness_variable=jNone,
        startup_query_count=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param igmp_version - <v1|v2|v3>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_len - <1-32>
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param query_interval - <1-31744>
    :param robustness_variable - <2-7>
    :param startup_query_count - <2-255>
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4096>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|delete>
    :param port_handle

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1",
        "igmp_querier_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1",
        "igmp_querier_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['igmp_version'] = igmp_version
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_len'] = intf_prefix_len
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['neighbor_intf_ip_addr_step'] = neighbor_intf_ip_addr_step
    args['query_interval'] = query_interval
    args['robustness_variable'] = robustness_variable
    args['startup_query_count'] = startup_query_count
    args['mode'] = mode

    vlan_args = dict()
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_mode'] = vlan_id_mode
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_user_priority'] = vlan_user_priority

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_igmp_querier_config.__doc__, **args)
    args['discard_learned_info'] = 0

    vlan_args = get_arg_value(rt_handle, j_emulation_igmp_querier_config.__doc__, **vlan_args)

    if mode == 'create':
        if port_handle != jNone:
            handle = create_deviceGroup(rt_handle, port_handle)['device_group_handle']
        elif handle == jNone:
            raise Exception('Please provide port_handle or handle')
    elif mode == 'modify':
        __check_and_raise(handle)
    else:
        __check_and_raise(handle)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_igmp_querier_config', **args))

        if len(vlan_args) != 0:
            vlan_config(rt_handle, vlan_args, hndl)
    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'igmp_querier_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['igmp_querier_handle']
            igmp_querier_handles.append(ret[index]['handles'])

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_isis_config(
        rt_handle,
        area_id=jNone,
        bfd_registration=jNone,
        count=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        gateway_ipv6_addr=jNone,
        gateway_ipv6_addr_step=jNone,
        graceful_restart=jNone,
        graceful_restart_restart_time=jNone,
        handle=jNone,
        hello_interval=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_ip_prefix_length=jNone,
        intf_ipv6_addr=jNone,
        intf_ipv6_addr_step=jNone,
        intf_ipv6_prefix_length=jNone,
        intf_metric=jNone,
        intf_type=jNone,
        lsp_life_time=jNone,
        lsp_refresh_interval=jNone,
        overloaded=jNone,
        router_id=jNone,
        routing_level=jNone,
        te_enable=jNone,
        te_max_bw=jNone,
        te_max_resv_bw=jNone,
        te_unresv_bw_priority0=jNone,
        te_unresv_bw_priority1=jNone,
        te_unresv_bw_priority2=jNone,
        te_unresv_bw_priority3=jNone,
        te_unresv_bw_priority4=jNone,
        te_unresv_bw_priority5=jNone,
        te_unresv_bw_priority6=jNone,
        te_unresv_bw_priority7=jNone,
        vlan=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        wide_metrics=jNone,
        mode=jNone,
        system_id=jNone,
        port_handle=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):
    """
    :param rt_handle:       RT object
    :param area_id
    :param bfd_registration
    :param count
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param gateway_ipv6_addr
    :param gateway_ipv6_addr_step
    :param graceful_restart
    :param graceful_restart_restart_time - <0-65535>
    :param handle
    :param hello_interval - <1-65535>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_ip_prefix_length - <1-32>
    :param intf_ipv6_addr
    :param intf_ipv6_addr_step
    :param intf_ipv6_prefix_length - <1-128>
    :param intf_metric - <0-16777215>
    :param intf_type - <broadcast|ptop>
    :param lsp_life_time - <1-65535>
    :param lsp_refresh_interval - <1-65535>
    :param overloaded
    :param router_id
    :param routing_level - <L1|L2|L1L2>
    :param te_enable
    :param te_max_bw
    :param te_max_resv_bw
    :param te_unresv_bw_priority0
    :param te_unresv_bw_priority1
    :param te_unresv_bw_priority2
    :param te_unresv_bw_priority3
    :param te_unresv_bw_priority4
    :param te_unresv_bw_priority5
    :param te_unresv_bw_priority6
    :param te_unresv_bw_priority7
    :param vlan
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <1-4094>
    :param vlan_user_priority - <0-7>
    :param wide_metrics - <0|1>
    :param mode - <create|modify|delete|inactive:disable|active:enable>
    :param system_id
    :param port_handle
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <1-4094>
    :param vlan_outer_user_priority - <0-7>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "session_router": "isislspconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/isisL3:2",
        "isis_l3_handle": "/topology:1/deviceGroup:1/ethernet:1/isisL3:2",
        "isis_l3_router_handle": "/topology:1/deviceGroup:1/isisL3Router:1",
        "isis_l3_te_handle": "/topology:1/deviceGroup:1/ethernet:1/isisL3:2/isisTrafficEngineering",
        "sr_tunnel_handle_rtr": "/topology:1/deviceGroup:1/isisL3Router:1/isisSRTunnelList",
        "sr_tunnel_seg_handle_rtr": "/topology:1/deviceGroup:1/isisL3Router:1/isisSRTunnelList/isisSegmentList:1",
        "srgb_range_handle_rtr": "/topology:1/deviceGroup:1/isisL3Router:1/isisSRGBRangeSubObjectsList:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    vargs = dict()
    args['area_id'] = area_id
    args['bfd_registration'] = bfd_registration
    args['count'] = count
    args['gateway_ip_addr'] = gateway_ip_addr
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['gateway_ipv6_addr'] = gateway_ipv6_addr
    args['gateway_ipv6_addr_step'] = gateway_ipv6_addr_step
    args['graceful_restart'] = graceful_restart
    args['graceful_restart_restart_time'] = graceful_restart_restart_time
    args['handle'] = handle
    args['hello_interval'] = hello_interval
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_ip_prefix_length'] = intf_ip_prefix_length
    args['intf_ipv6_addr'] = intf_ipv6_addr
    args['intf_ipv6_addr_step'] = intf_ipv6_addr_step
    args['intf_ipv6_prefix_length'] = intf_ipv6_prefix_length
    args['intf_metric'] = intf_metric
    args['intf_type'] = intf_type
    args['lsp_life_time'] = lsp_life_time
    args['lsp_refresh_interval'] = lsp_refresh_interval
    args['overloaded'] = overloaded
    args['router_id'] = router_id
    args['routing_level'] = routing_level
    args['te_enable'] = te_enable
    args['te_max_bw'] = te_max_bw
    args['te_max_resv_bw'] = te_max_resv_bw
    args['te_unresv_bw_priority0'] = te_unresv_bw_priority0
    args['te_unresv_bw_priority1'] = te_unresv_bw_priority1
    args['te_unresv_bw_priority2'] = te_unresv_bw_priority2
    args['te_unresv_bw_priority3'] = te_unresv_bw_priority3
    args['te_unresv_bw_priority4'] = te_unresv_bw_priority4
    args['te_unresv_bw_priority5'] = te_unresv_bw_priority5
    args['te_unresv_bw_priority6'] = te_unresv_bw_priority6
    args['te_unresv_bw_priority7'] = te_unresv_bw_priority7
    vargs['vlan'] = vlan
    vargs['vlan_id'] = vlan_id
    vargs['vlan_id_mode'] = vlan_id_mode
    vargs['vlan_id_step'] = vlan_id_step
    vargs['vlan_user_priority'] = vlan_user_priority
    args['wide_metrics'] = wide_metrics
    args['mode'] = mode
    args['system_id'] = system_id
    args['port_handle'] = port_handle
    vargs['vlan_outer_id'] = vlan_outer_id
    vargs['vlan_outer_id_mode'] = vlan_outer_id_mode
    vargs['vlan_outer_id_step'] = vlan_outer_id_step
    vargs['vlan_outer_user_priority'] = vlan_outer_user_priority

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_isis_config.__doc__, **args)
    args['discard_lsp'] = 0
    args['redistribution'] = 'up'
    args['return_detailed_handles'] = 1

    vargs = get_arg_value(rt_handle, j_emulation_isis_config.__doc__, **vargs)

    if mode == 'create' and port_handle != jNone:
        _result_ = create_deviceGroup(rt_handle, port_handle, count)
        handle = _result_['device_group_handle']

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_isis_config', **args))
        if vargs:
            if mode == 'create':
                vlan_config(rt_handle, vargs, ret[-1]['isis_l3_handle'])
            else:
                vlan_config(rt_handle, vargs, hndl)

    # ***** Return Value Modification *****
    for index in range(len(ret)):
        if 'isis_l3_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['isis_l3_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_isis_control(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|restart>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_isis_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_isis_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_isis_info(rt_handle, handle=jNone,
                          port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle

    Spirent Returns:
    {
        "aggregated_l1_csnp_rx": "0",
        "aggregated_l1_csnp_tx": "0",
        "aggregated_l1_lan_hello_rx": "0",
        "aggregated_l1_lan_hello_tx": "0",
        "aggregated_l1_lsp_rx": "0",
        "aggregated_l1_lsp_tx": "0",
        "aggregated_l1_psnp_rx": "0",
        "aggregated_l1_psnp_tx": "0",
        "aggregated_l2_csnp_rx": "8",
        "aggregated_l2_csnp_tx": "0",
        "aggregated_l2_lan_hello_rx": "10",
        "aggregated_l2_lan_hello_tx": "10",
        "aggregated_l2_lsp_rx": "5",
        "aggregated_l2_lsp_tx": "1",
        "aggregated_l2_psnp_rx": "0",
        "aggregated_l2_psnp_tx": "0",
        "aggregated_p2p_hello_rx": "0",
        "aggregated_p2p_hello_tx": "0",
        "handles": "host1",
        "procName": "emulation_isis_info",
        "status": "1"
    }

    IXIA Returns:
    {
        "Device Group 1": {
            "aggregate": {
                "aggregated_l1_csnp_rx": "0",
                "aggregated_l1_csnp_tx": "0",
                "aggregated_l1_db_size": "0",
                "aggregated_l1_full_count": "0",
                "aggregated_l1_hellos_rx": "0",
                "aggregated_l1_hellos_tx": "0",
                "aggregated_l1_init_count": "0",
                "aggregated_l1_lsp_rx": "0",
                "aggregated_l1_lsp_tx": "0",
                "aggregated_l1_p2p_hellos_rx": "0",
                "aggregated_l1_p2p_hellos_tx": "0",
                "aggregated_l1_psnp_rx": "0",
                "aggregated_l1_psnp_tx": "0",
                "aggregated_l2_csnp_rx": "1",
                "aggregated_l2_csnp_tx": "0",
                "aggregated_l2_db_size": "2",
                "aggregated_l2_full_count": "1",
                "aggregated_l2_hellos_rx": "2",
                "aggregated_l2_hellos_tx": "2",
                "aggregated_l2_init_count": "0",
                "aggregated_l2_lsp_rx": "1",
                "aggregated_l2_lsp_tx": "0",
                "aggregated_l2_p2p_hellos_rx": "0",
                "aggregated_l2_p2p_hellos_tx": "0",
                "aggregated_l2_psnp_rx": "0",
                "aggregated_l2_psnp_tx": "0",
                "l1_full_neighbors": "0",
                "l1_sessions_flap": "0",
                "l1_sessions_up": "0",
                "l2_full_neighbors": "1",
                "l2_sessions_flap": "0",
                "l2_sessions_up": "1",
                "sessions_down": "0",
                "sessions_notstarted": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "status": "started"
            }
        },
        "aggregated_l1_csnp_rx": "0",
        "aggregated_l1_csnp_tx": "0",
        "aggregated_l1_lan_hello_rx": "0",
        "aggregated_l1_lan_hello_tx": "0",
        "aggregated_l1_lsp_rx": "0",
        "aggregated_l1_lsp_tx": "0",
        "aggregated_l1_psnp_rx": "0",
        "aggregated_l1_psnp_tx": "0",
        "aggregated_l2_csnp_rx": "1",
        "aggregated_l2_csnp_tx": "0",
        "aggregated_l2_lan_hello_rx": "2",
        "aggregated_l2_lan_hello_tx": "2",
        "aggregated_l2_lsp_rx": "1",
        "aggregated_l2_lsp_tx": "0",
        "aggregated_l2_psnp_rx": "0",
        "aggregated_l2_psnp_tx": "0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "aggregated_l1_csnp_rx"
        "aggregated_l1_csnp_tx"
        "aggregated_l1_lan_hello_rx"
        "aggregated_l1_lan_hello_tx"
        "aggregated_l1_lsp_rx"
        "aggregated_l1_lsp_tx"
        "aggregated_l1_psnp_rx"
        "aggregated_l1_psnp_tx"
        "aggregated_l2_csnp_rx"
        "aggregated_l2_csnp_tx"
        "aggregated_l2_lan_hello_rx"
        "aggregated_l2_lan_hello_tx"
        "aggregated_l2_lsp_rx"
        "aggregated_l2_lsp_tx"
        "aggregated_l2_psnp_rx"
        "aggregated_l2_psnp_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'stats'
        stats.update(rt_handle.invoke('emulation_isis_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                if 'aggregated_l1_csnp_rx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l1_csnp_rx'] = ret[index][key]['aggregate']['aggregated_l1_csnp_rx']
                if 'aggregated_l1_csnp_tx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l1_csnp_tx'] = ret[index][key]['aggregate']['aggregated_l1_csnp_tx']
                if 'aggregated_l1_hellos_rx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l1_lan_hello_rx'] = ret[index][key]['aggregate']['aggregated_l1_hellos_rx']
                if 'aggregated_l1_hellos_tx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l1_lan_hello_tx'] = ret[index][key]['aggregate']['aggregated_l1_hellos_tx']
                if 'aggregated_l1_lsp_rx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l1_lsp_rx'] = ret[index][key]['aggregate']['aggregated_l1_lsp_rx']
                if 'aggregated_l1_lsp_tx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l1_lsp_tx'] = ret[index][key]['aggregate']['aggregated_l1_lsp_tx']
                if 'aggregated_l1_psnp_rx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l1_psnp_rx'] = ret[index][key]['aggregate']['aggregated_l1_psnp_rx']
                if 'aggregated_l1_psnp_tx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l1_psnp_tx'] = ret[index][key]['aggregate']['aggregated_l1_psnp_tx']
                if 'aggregated_l2_csnp_rx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l2_csnp_rx'] = ret[index][key]['aggregate']['aggregated_l2_csnp_rx']
                if 'aggregated_l2_csnp_tx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l2_csnp_tx'] = ret[index][key]['aggregate']['aggregated_l2_csnp_tx']
                if 'aggregated_l2_hellos_rx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l2_lan_hello_rx'] = ret[index][key]['aggregate']['aggregated_l2_hellos_rx']
                if 'aggregated_l2_hellos_tx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l2_lan_hello_tx'] = ret[index][key]['aggregate']['aggregated_l2_hellos_tx']
                if 'aggregated_l2_lsp_rx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l2_lsp_rx'] = ret[index][key]['aggregate']['aggregated_l2_lsp_rx']
                if 'aggregated_l2_lsp_tx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l2_lsp_tx'] = ret[index][key]['aggregate']['aggregated_l2_lsp_tx']
                if 'aggregated_l2_psnp_rx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l2_psnp_rx'] = ret[index][key]['aggregate']['aggregated_l2_psnp_rx']
                if 'aggregated_l2_psnp_tx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_l2_psnp_tx'] = ret[index][key]['aggregate']['aggregated_l2_psnp_tx']
                if 'aggregated_p2p_hello_rx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_p2p_hello_rx'] = ret[index][key]['aggregate']['aggregated_p2p_hello_rx']
                if 'aggregated_p2p_hello_tx' in ret[index][key]['aggregate']:
                    ret[index]['aggregated_p2p_hello_tx'] = ret[index][key]['aggregate']['aggregated_p2p_hello_tx']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_lacp_config(
        rt_handle,
        handle=jNone,
        mode=jNone,
        protocol=jNone,
        actor_key=jNone,
        actor_key_step=jNone,
        actor_port_priority=jNone,
        actor_port_priority_step=jNone,
        actor_port_number=jNone,
        actor_port_number_step=jNone,
        lacp_timeout=jNone,
        lacp_activity=jNone,
        actor_system_id=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <create|delete|modify|enable|disable>
    :param protocol - <lacp>
    :param actor_key - <0-65535>
    :param actor_key_step - <0-65535>
    :param actor_port_priority - <0-65535>
    :param actor_port_priority_step - <0-65535>
    :param actor_port_number - <0-65535>
    :param actor_port_number_step - <0-65535>
    :param lacp_timeout - <long|short>
    :param lacp_activity - <active|passive>
    :param actor_system_id
    :param port_handle

    Spirent Returns:

    IXIA Returns:
    {
        "handle": "/topology:1/deviceGroup:1/ethernet:1/lacp:1/item:1",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/lacp:1/item:1",
        "lacp_handle": "/topology:1/deviceGroup:1/ethernet:1/lacp:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['handle'] = handle
    args['mode'] = mode
    args['protocol'] = protocol
    args['actor_key'] = actor_key
    args['actor_key_step'] = actor_key_step
    args['actor_port_priority'] = actor_port_priority
    args['actor_port_priority_step'] = actor_port_priority_step
    args['actor_port_number'] = actor_port_number
    args['actor_port_number_step'] = actor_port_number_step
    args['lacp_timeout'] = lacp_timeout
    args['lacp_activity'] = lacp_activity
    args['actor_system_id'] = actor_system_id
#    args['active'] = 1
#    args['lag_id'] = 1
#    args['count'] = 1
#    args['reset'] = None

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_lacp_config.__doc__, **args)
    if args.get('protocol'):
        args['session_type'] = args.pop('protocol')
    if args.get('actor_port_priority'):
        args['actor_port_pri'] = args.pop('actor_port_priority')
    if args.get('actor_port_priority_step'):
        args['actor_port_pri_step'] = args.pop('actor_port_priority_step')
    if args.get('actor_port_number'):
        args['actor_port_num'] = args.pop('actor_port_number')
    if args.get('actor_port_number_step'):
        args['actor_port_num_step'] = args.pop('actor_port_number_step')

    if args.get('lacp_timeout') and lacp_timeout == 'long':
        args['lacp_timeout'] = 90
    elif args.get('lacp_timeout') and lacp_timeout == 'short':
        args['lacp_timeout'] = 3

    if mode == 'create':
        if args.get('port_handle'):
            handle = create_deviceGroup(rt_handle, args.pop('port_handle'))
            handle = handle['device_group_handle']
            nargs = dict()
            nargs['mode'] = 'config'
            nargs['protocol_handle'] = handle
            nargs['src_mac_addr'] = args['actor_system_id']
            nret = rt_handle.invoke('interface_config', **nargs)
            handle = nret['ethernet_handle']
        elif not args.get('handle'):
            raise Exception("Please pass either handle or port_handle to the function call")
        __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if mode == 'delete':
        nargs = dict()
        nargs['action'] = 'stop_all_protocols'
        nargs['handle'] = handle
        rt_handle.invoke('test_control', **nargs)
        sleep(5)

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_lacp_link_config', **args))

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'lacp_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['lacp_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_lacp_control(
        rt_handle,
        action=jNone,
        handle=jNone):
    """
    :param rt_handle:       RT object
    :param action - <start|stop>
    :param handle

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = action
    args['port_handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_lacp_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_lacp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_lacp_info(
        rt_handle,
        handle=jNone,
        mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode

    Spirent Returns:
    {
        "actor_operational_key": "1",
        "actor_port": "1",
        "actor_state": "61",
        "actor_systemid": "00:11:01:00:00:01",
        "aggregate": {
            "actor_operational_key": "1",
            "actor_port": "1",
            "actor_state": "61",
            "actor_systemid": "00:11:01:00:00:01",
            "lacp_state": "UP",
            "marker_pdus_rx": "0",
            "marker_pdus_tx": "0",
            "marker_response_pdus_rx": "0",
            "marker_response_pdus_tx": "0",
            "partner_collector_max_delay": "50000",
            "partner_operational_key": "1",
            "partner_port": "1",
            "partner_port_priority": "1",
            "partner_state": "61",
            "partner_system_id": "00:11:02:00:00:01",
            "partner_system_priority": "1",
            "pdus_rx": "4",
            "pdus_tx": "4",
            "status": "1"
        },
        "lacp_state": "UP",
        "marker_pdus_rx": "0",
        "marker_pdus_tx": "0",
        "marker_response_pdus_rx": "0",
        "marker_response_pdus_tx": "0",
        "partner_collector_max_delay": "50000",
        "partner_operational_key": "1",
        "partner_port": "1",
        "partner_port_priority": "1",
        "partner_state": "61",
        "partner_system_id": "00:11:02:00:00:01",
        "partner_system_priority": "1",
        "pdus_rx": "4",
        "pdus_tx": "4",
        "status": "1"
    },

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/lacp:1/item:1": {
            "aggregate": {
                "actor_key": "1",
                "actor_port_number": "1",
                "actor_system_id": "00 11 01 00 00 01"
            }
        },
        "Device Group 1": {
            "aggregate": {
                "device_group": "Device Group 1",
                "lacpdu_rx": "5",
                "lacpdu_tx": "5",
                "lacpdu_tx_rate_violation_count": "0",
                "lacpu_malformed_rx": "0",
                "lag_member_ports_up": "1",
                "marker_pdu_rx": "0",
                "marker_pdu_tx": "0",
                "marker_pdu_tx_rate_violation_count": "0",
                "marker_res_pdu_rx": "0",
                "marker_res_pdu_tx": "0",
                "marker_res_timeout_count": "0",
                "sessions_down": "0",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "total_lag_member_ports": "1"
            }
        },
        "InnerGlobalStats": {
            "aggregate": {
                "total_Number_of_operational_lags": "2",
                "total_number_of_user_defined_lags": "2"
            }
        },
        "[(0001:00-11-01-00-00-01:0001:00:0000):(0001:00-11-02-00-00-01:0001:00:0000)]": {
            "aggregate": {
                "lacpdu_rx": "5",
                "lacpdu_tx": "5",
                "lacpdu_tx_rate_violation_count": "0",
                "lacpu_malformed_rx": "0",
                "lag_id": "[(0001:00-11-01-00-00-01:0001:00:0000):(0001:00-11-02-00-00-01:0001:00:0000)]",
                "lag_member_ports_up": "1",
                "marker_pdu_rx": "0",
                "marker_pdu_tx": "0",
                "marker_pdu_tx_rate_violation_count": "0",
                "marker_res_pdu_rx": "0",
                "marker_res_pdu_tx": "0",
                "marker_res_timeout_count": "0",
                "session_flap_count": "0",
                "total_lag_member_ports": "1"
            }
        },
        "[(0001:00-11-02-00-00-01:0001:00:0000):(0001:00-11-01-00-00-01:0001:00:0000)]": {
            "aggregate": {
                "lacpdu_rx": "5",
                "lacpdu_tx": "5",
                "lacpdu_tx_rate_violation_count": "0",
                "lacpu_malformed_rx": "0",
                "lag_id": "[(0001:00-11-02-00-00-01:0001:00:0000):(0001:00-11-01-00-00-01:0001:00:0000)]",
                "lag_member_ports_up": "1",
                "marker_pdu_rx": "0",
                "marker_pdu_tx": "0",
                "marker_pdu_tx_rate_violation_count": "0",
                "marker_res_pdu_rx": "0",
                "marker_res_pdu_tx": "0",
                "marker_res_timeout_count": "0",
                "session_flap_count": "0",
                "total_lag_member_ports": "1"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
        "aggregate"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'per_device_group'
        stats.update(rt_handle.invoke('emulation_lacp_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                ret[index]['aggregate'] = ret[index][key]['aggregate']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ldp_config(
        rt_handle,
        bfd_registration=jNone,
        count=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        handle=jNone,
        hello_interval=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_length=jNone,
        keepalive_interval=jNone,
        label_adv=jNone,
        loopback_ip_addr=jNone,
        loopback_ip_addr_step=jNone,
        lsr_id=jNone,
        lsr_id_step=jNone,
        reconnect_time=jNone,
        remote_ip_addr=jNone,
        remote_ip_addr_step=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        enable_graceful_restart=jNone,
        graceful_recovery_time=jNone,
        mac_address_init=jNone,
        auth_key=jNone,
        auth_mode=jNone,
        port_handle=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):
        # Below arguments are not supported by spirent, when spirent adds
        # this functionality the arguments can be uncommented
        # targeted_hello_interval=jNone,
        # targeted_hello_hold_time=jNone,
        # atm_vc_dir=jNone,
        # label_space=jNone,
        # discard_self_adv_fecs=jNone,
        # keepalive_holdtime=jNone,
        # hello_hold_time=jNone,
        # bfd_registration_mode=jNone,
    """
    :param rt_handle:       RT object
    :param bfd_registration - <0|1>
    :param count
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param handle
    :param hello_interval - <1-65535>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_length - <1-32>
    :param keepalive_interval - <1-21845>
    :param label_adv - <unsolicited|on_demand>
    :param loopback_ip_addr
    :param loopback_ip_addr_step
    :param lsr_id
    :param lsr_id_step
    :param reconnect_time - <0-300000>
    :param remote_ip_addr
    :param remote_ip_addr_step
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <1-4094>
    :param vlan_user_priority - <0-7>
    :param mode - <create|delete|inactive:disable|active:enable|modify>
    :param enable_graceful_restart - <0|1>
    :param graceful_recovery_time - <0-300000>
    :param mac_address_init
    :param auth_key - <1-255>
    :param auth_mode - <none:null|md5>
    :param port_handle
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <1-4094>
    :param vlan_outer_user_priority - <0-7>
    # Below arguments are not supported by spirent, when spirent adds
    # this functionality the arguments can be uncommented
    #targeted_hello_interval
    #targeted_hello_hold_time
    #atm_vc_dir
    #label_space
    #discard_self_adv_fecs
    #keepalive_holdtime
    #hello_hold_time
    #bfd_registration_mode
    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpBasicRouter:1/item:1",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpBasicRouter:1",
        "ldp_basic_router_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpBasicRouter:1",
        "ldp_connected_interface_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpConnectedInterface:2",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    vargs = dict()
    args['bfd_registration'] = bfd_registration
    args['count'] = count
    args['gateway_ip_addr'] = gateway_ip_addr
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['handle'] = handle
    args['hello_interval'] = hello_interval
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_length'] = intf_prefix_length
    args['keepalive_interval'] = keepalive_interval
    args['label_adv'] = label_adv
    args['loopback_ip_addr'] = loopback_ip_addr
    args['loopback_ip_addr_step'] = loopback_ip_addr_step
    args['lsr_id'] = lsr_id
    args['lsr_id_step'] = lsr_id_step
    args['reconnect_time'] = reconnect_time
    args['remote_ip_addr'] = remote_ip_addr
    args['remote_ip_addr_step'] = remote_ip_addr_step
    vargs['vlan_id'] = vlan_id
    vargs['vlan_id_mode'] = vlan_id_mode
    vargs['vlan_id_step'] = vlan_id_step
    vargs['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['graceful_restart_enable'] = enable_graceful_restart
    args['mac_address_init'] = mac_address_init
    args['auth_key'] = auth_key
    if auth_mode.lower() == 'none':
        args['auth_mode'] = 'null'
    else:
        args['auth_mode'] = auth_mode
    vargs['vlan_outer_id'] = vlan_outer_id
    vargs['vlan_outer_id_mode'] = vlan_outer_id_mode
    vargs['vlan_outer_id_step'] = vlan_outer_id_step
    vargs['vlan_outer_user_priority'] = vlan_outer_user_priority

    # Below arguments are not supported by spirent, when spirent adds
    # this functionality the arguments can be uncommented
    # args['targeted_hello_interval'] = targeted_hello_interval
    # args['targeted_hello_hold_time'] = targeted_hello_hold_time
    # args['atm_vc_dir'] = atm_vc_dir
    # args['label_space'] = label_space
    # args['discard_self_adv_fecs'] = discard_self_adv_fecs
    # args['keepalive_holdtime'] = keepalive_holdtime
    # args['hello_hold_time'] = hello_hold_time
    # args['bfd_registration_mode'] = bfd_registration_mode

    # ***** Argument Modification *****
    if graceful_recovery_time != jNone:
        graceful_recovery_time = int(graceful_recovery_time)
        if graceful_recovery_time > 300:
            raise ValueError("Argument "+ "\"graceful_recovery_time\" value should be in the range 0-300 seconds")
        else:
            graceful_recovery_time = graceful_recovery_time*1000
            args['recovery_time'] = graceful_recovery_time
    if reconnect_time != jNone:
        reconnect_time = int(reconnect_time)
        if reconnect_time > 300:
            raise ValueError("Argument "+ "\"reconnect_time\" value should be in the range 0-300 seconds")
        else:
            reconnect_time = reconnect_time*1000
            args['reconnect_time'] = reconnect_time
    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ldp_config.__doc__, **args)
    vargs = get_arg_value(rt_handle, j_emulation_ldp_config.__doc__, **vargs)

    nargs = dict()
    nargs['intf_ip_addr'] = intf_ip_addr
    nargs['intf_ip_addr_step'] = intf_ip_addr_step
    if args.get('intf_prefix_length'):
        nargs['netmask'] = cidr_to_netmask(intf_prefix_length)
    nargs['gateway'] = gateway_ip_addr
    nargs['gateway_step'] = gateway_ip_addr_step
    for key in list(nargs.keys()):
        if nargs[key] == jNone:
            del nargs[key]
    if mode == 'create' and port_handle != jNone:
        _result_ = create_deviceGroup(rt_handle, port_handle, count)
        nargs['protocol_handle'] = _result_['device_group_handle']
        _result_ = rt_handle.invoke('interface_config', **nargs)
        handle = _result_['ipv4_handle']

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if mode != 'create' and 'ldpConnectedInterface' in hndl:
            ipv4_handle = __get_parent_handle(hndl, 'ipv4')
            ldpBasicRouter = invoke_ixnet(rt_handle, 'getList', ipv4_handle, 'ldpBasicRouter')
            hndl = ldpBasicRouter[0].strip('::ixNet::OBJ-')
        args['handle'] = hndl
        ret_value = rt_handle.invoke('emulation_ldp_config', **args)
        ret.append(ret_value)
        if vargs:
            if mode == 'create':
                if 'ethernet' in hndl:
                    eth_handle = __get_parent_handle(hndl, 'ethernet')
                    vlan_config(rt_handle, vargs, eth_handle)
                elif ret_value.get('ldp_connected_interface_handle'):
                    vlan_config(rt_handle, vargs, ret_value.get('ldp_connected_interface_handle'))
                elif ret_value.get('ldp_basic_router_handle'):
                    vlan_config(rt_handle, vargs, ret_value.get('ldp_basic_router_handle'))
                elif ret_value.get('ldp_targeted_router_handle'):
                    vlan_config(rt_handle, vargs, ret_value.get('ldp_targeted_router_handle'))
            else:
                vlan_config(rt_handle, vargs, hndl)
    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'ldp_basic_router_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['ldp_basic_router_handle']
        if 'ldp_connected_interface_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['ldp_connected_interface_handle']
        if 'ldp_targeted_router_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['ldp_targeted_router_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ldp_control(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|restart>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ldp_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_ldp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ldp_info(rt_handle, handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle

    Spirent Returns:
    {
        "abort_rx": "0",
        "abort_tx": "0",
        "elapsed_time": "60.0983300209",
        "fec_type": "ipv4_prefix ipv4_prefix",
        "hello_hold_time": "15",
        "hello_interval": "5",
        "intf_ip_addr": "10.10.10.1",
        "ip_address": "10.10.10.1",
        "keepalive_holdtime": "135",
        "keepalive_interval": "45",
        "label": "16 16",
        "label_adv": "unsolicited unsolicited",
        "label_space": "0",
        "linked_hellos_rx": "12",
        "linked_hellos_tx": "12",
        "lsp_pool_handle": "ipv4prefixlsp1",
        "map_rx": "1",
        "map_tx": "1",
        "notif_rx": "0",
        "notif_tx": "0",
        "num_incoming_egress_lsps": "1",
        "num_incoming_ingress_lsps": "1",
        "num_lsps_setup": "1",
        "num_opened_lsps": "1",
        "prefix": "20.20.20.0 20.20.20.0",
        "prefix_length": "24 24",
        "release_rx": "0",
        "release_tx": "0",
        "req_rx": "0",
        "req_tx": "0",
        "session_state": "operational",
        "source": {
            "ldplspresults1": "ldplspresults2"
        },
        "status": "1",
        "targeted_hellos_rx": "0",
        "targeted_hellos_tx": "0",
        "type": "egress egress",
        "withdraw_rx": "0",
        "withdraw_tx": "0"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpBasicRouter:1/item:1": {
            "session": {
                "abort_rx": "0",
                "abort_tx": "0",
                "basic_sessions": "0",
                "established_lsp_ingress": "0",
                "initialized_state_count": "0",
                "map_rx": "0",
                "map_tx": "0",
                "non_existent_state_count": "0",
                "notif_rx": "0",
                "notif_tx": "0",
                "open_state_count": "0",
                "operational_state_count": "0",
                "port_name": "1/11/2",
                "pw_status_cleared_rx": "0",
                "pw_status_cleared_tx": "0",
                "pw_status_down": "0",
                "pw_status_notif_rx": "0",
                "pw_status_notif_tx": "0",
                "release_rx": "0",
                "release_tx": "0",
                "req_rx": "0",
                "req_tx": "0",
                "targeted_session_down": "0",
                "withdraw_rx": "0",
                "withdraw_tx": "0"
            }
        },
        "1/11/2": {
            "aggregate": {
                "abort_rx": "0",
                "abort_tx": "0",
                "basic_sessions": "0",
                "established_lsp_ingress": "0",
                "initialized_state_count": "0",
                "map_rx": "0",
                "map_tx": "0",
                "non_existent_state_count": "0",
                "notif_rx": "0",
                "notif_tx": "0",
                "open_state_count": "0",
                "operational_state_count": "0",
                "port_name": "1/11/2",
                "pw_status_cleared_rx": "0",
                "pw_status_cleared_tx": "0",
                "pw_status_down": "0",
                "pw_status_notif_rx": "0",
                "pw_status_notif_tx": "0",
                "release_rx": "0",
                "release_tx": "0",
                "req_rx": "0",
                "req_tx": "0",
                "status": "started",
                "targeted_session_down": "0",
                "withdraw_rx": "0",
                "withdraw_tx": "0"
            }
        },
        "abort_rx": "0",
        "abort_tx": "0",
        "lsp_labels": {
            "fec_type_list": {
                "Fec Type": "ipv4_prefix vc vc"
            },
            "group_id_list": {
                "Group ID": "removePacket[N/A] removePacket[N/A]",
                "Group Id": "N/A"
            },
            "label_list": {
                "Label": "removePacket[N/A] removePacket[N/A] removePacket[N/A]"
            },
            "label_space_id_list": {
                "Label Space ID": "removePacket[N/A]",
                "Label Space Id": "N/A N/A"
            },
            "prefix_length_list": {
                "FEC Prefix Length": "N/A N/A"
            },
            "prefix_list": {
                "FEC": "removePacket[N/A] N/A N/A"
            },
            "source_list": {
                "Peer": "removePacket[N/A] removePacket[N/A] removePacket[N/A]"
            },
            "state_list": {
                "PW State": "N/A N/A",
                "State": "N/A"
            },
            "type_list": {
                "Type": "learned learned learned"
            },
            "vc_id_list": {
                "VC ID": "removePacket[N/A] N/A",
                "Vc Id": "N/A"
            },
            "vc_type_list": {
                "VC Type": "N/A N/A",
                "Vc Type": "N/A"
            },
            "vci_list": {
                "Vci": "N/A N/A N/A"
            },
            "vpi_list": {
                "Vpi": "N/A N/A N/A"
            }
        },
        "map_rx": "0",
        "map_tx": "0",
        "neighbors": {
            "Peer": "removePacket[N/A]"
        },
        "notif_rx": "0",
        "notif_tx": "0",
        "release_rx": "0",
        "release_tx": "0",
        "req_rx": "0",
        "req_tx": "0",
        "settings": {
            "atm_range_max_vci": {
                "atm_range_max_vci": "N/A"
            },
            "atm_range_max_vpi": {
                "atm_range_max_vpi": "N/A"
            },
            "atm_range_min_vci": {
                "atm_range_min_vci": "N/A"
            },
            "atm_range_min_vpi": {
                "atm_range_min_vpi": "N/A"
            },
            "hello_hold_time": {
                "hello_hold_time": "/multivalue:3561"
            },
            "hello_interval": {
                "hello_interval": "/multivalue:3560"
            },
            "hold_time": {
                "hold_time": "/multivalue:3561"
            },
            "intf_ip_addr": {
                "intf_ip_addr": "/multivalue:6"
            },
            "ip_address": {
                "ip_address": "/multivalue:6"
            },
            "keepalive": {
                "keepalive": "/multivalue:3552"
            },
            "keepalive_holdtime": {
                "keepalive_holdtime": "/multivalue:3553"
            },
            "keepalive_interval": {
                "keepalive_interval": "/multivalue:3552"
            },
            "label_adv": {
                "label_adv": "/multivalue:3558"
            },
            "label_space": {
                "label_space": "/multivalue:3559"
            },
            "targeted_hello": {
                "targeted_hello": "N/A"
            },
            "vci": {
                "vci": "N/A"
            },
            "vpi": {
                "vpi": "N/A"
            }
        },
        "status": "1",
        "withdraw_rx": "0",
        "withdraw_tx": "0"
    }

    Common Return Keys:
        "status"
        "abort_rx"
        "abort_tx"
        "map_rx"
        "map_tx"
        "notif_rx"
        "notif_tx"
        "release_rx"
        "release_tx"
        "req_rx"
        "req_tx"
        "withdraw_rx"
        "withdraw_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if 'ldpConnectedInterface' in hndl:
            ipv4_handle = __get_parent_handle(hndl, 'ipv4')
            ldpBasicRouter = invoke_ixnet(rt_handle, 'getList', ipv4_handle, 'ldpBasicRouter')
            hndl = ldpBasicRouter[0].strip('::ixNet::OBJ-')
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'stats'
        stats.update(rt_handle.invoke('emulation_ldp_info', **args))
        args['mode'] = 'settings'
        stats.update(rt_handle.invoke('emulation_ldp_info', **args))
        if 'ldpTargetedRouter' not in hndl:
            args['mode'] = 'neighbors'
            stats.update(rt_handle.invoke('emulation_ldp_info', **args))
        args['mode'] = 'lsp_labels'
        stats.update(rt_handle.invoke('emulation_ldp_info', **args))
        args['mode'] = 'stats_per_device_group'
        stats.update(rt_handle.invoke('emulation_ldp_info', **args))
        args['mode'] = 'session'
        stats.update(rt_handle.invoke('emulation_ldp_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                if 'abort_rx' in ret[index][key]['aggregate']:
                    ret[index]['abort_rx'] = ret[index][key]['aggregate']['abort_rx']
                if 'abort_tx' in ret[index][key]['aggregate']:
                    ret[index]['abort_tx'] = ret[index][key]['aggregate']['abort_tx']
                if 'map_rx' in ret[index][key]['aggregate']:
                    ret[index]['map_rx'] = ret[index][key]['aggregate']['map_rx']
                if 'map_tx' in ret[index][key]['aggregate']:
                    ret[index]['map_tx'] = ret[index][key]['aggregate']['map_tx']
                if 'notif_rx' in ret[index][key]['aggregate']:
                    ret[index]['notif_rx'] = ret[index][key]['aggregate']['notif_rx']
                if 'notif_tx' in ret[index][key]['aggregate']:
                    ret[index]['notif_tx'] = ret[index][key]['aggregate']['notif_tx']
                if 'release_rx' in ret[index][key]['aggregate']:
                    ret[index]['release_rx'] = ret[index][key]['aggregate']['release_rx']
                if 'release_tx' in ret[index][key]['aggregate']:
                    ret[index]['release_tx'] = ret[index][key]['aggregate']['release_tx']
                if 'req_rx' in ret[index][key]['aggregate']:
                    ret[index]['req_rx'] = ret[index][key]['aggregate']['req_rx']
                if 'req_tx' in ret[index][key]['aggregate']:
                    ret[index]['req_tx'] = ret[index][key]['aggregate']['req_tx']
                if 'withdraw_rx' in ret[index][key]['aggregate']:
                    ret[index]['withdraw_rx'] = ret[index][key]['aggregate']['withdraw_rx']
                if 'withdraw_tx' in ret[index][key]['aggregate']:
                    ret[index]['withdraw_tx'] = ret[index][key]['aggregate']['withdraw_tx']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ldp_route_config(
        rt_handle,
        fec_ip_prefix_length=jNone,
        fec_ip_prefix_start=jNone,
        fec_vc_cbit=jNone,
        fec_vc_count=jNone,
        fec_vc_group_id=jNone,
        fec_vc_intf_mtu=jNone,
        fec_vc_id_start=jNone,
        fec_vc_id_step=jNone,
        handle=jNone,
        lsp_handle=jNone,
        mode=jNone,
        fec_type=jNone,
        fec_vc_type=jNone,
        num_lsps=jNone,
        egress_label_mode=jNone,
        label_value_start=jNone,
        fec_ip_prefix_step=jNone):
        # Below arguments are not supported by spirent, when spirent adds
        # this functionality the arguments can be uncommented
        # fec_vc_mac_range_enable=jNone,
        # fec_vc_label_value_start=jNone,
        # fec_vc_peer_address=jNone,
        # fec_vc_mac_range_first_vlan_id=jNone,
        # fec_vc_mac_range_count=jNone,
        # fec_vc_atm_max_cells=jNone,
        # fec_vc_cem_option=jNone,
        # fec_vc_atm_enable=jNone,
        # fec_vc_fec_type=jNone,
        # fec_vc_cem_payload=jNone,
        # fec_vc_cem_payload_enable=jNone,
        # fec_vc_cem_option_enable=jNone,
        # fec_vc_intf_desc=jNone,
        # packing_enable=jNone,

    """
    :param rt_handle:       RT object
    :param fec_ip_prefix_length - <1-32>
    :param fec_ip_prefix_start
    :param fec_vc_cbit - <0|1>
    :param fec_vc_count
    :param fec_vc_group_id
    :param fec_vc_intf_mtu - <0-65535>
    :param fec_vc_id_start - <0-2147483647>
    :param fec_vc_id_step - <0-2147483647>
    :param handle
    :param lsp_handle
    :param mode - <create|modify|delete>
    :param fec_type - <prefix:ipv4_prefix|host_addr|vc>
    :param fec_vc_type - <cem|eth|eth_vlan|eth_vpls|fr_dlci|ppp>
    :param num_lsps - <1-34048>
    :param egress_label_mode - <nextlabel>
    :param label_value_start - <0-1046400>
    :param fec_ip_prefix_step
    # Below arguments are not supported by Spirent, when Spirent adds
    # this functionality the arguments can be uncommented
    #fec_vc_mac_range_enable
    #fec_vc_label_value_start
    #fec_vc_peer_address
    #fec_vc_mac_range_first_vlan_id
    #fec_vc_mac_range_count
    #fec_vc_atm_max_cells
    #fec_vc_cem_option
    #fec_vc_atm_enable
    #fec_vc_fec_type
    #fec_vc_cem_payload
    #fec_vc_cem_payload_enable
    #fec_vc_cem_option_enable
    #fec_vc_intf_desc
    #packing_enable

    Spirent Returns:
    {
        "handles": "ipv4prefixlsp1",
        "lsp_handle": "ipv4prefixlsp1",
        "status": "1"
    }

    IXIA Returns:
    {
        "fecproperty_handle": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/ldpFECProperty:1",
        "handles": "/topology:1/deviceGroup:1/networkGroup:1",
        "network_group_handle": "/topology:1/deviceGroup:1/networkGroup:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['fec_ip_prefix_length'] = fec_ip_prefix_length
    args['fec_ip_prefix_start'] = fec_ip_prefix_start
    args['fec_vc_cbit'] = fec_vc_cbit
    args['fec_vc_count'] = fec_vc_count
    args['fec_vc_intf_mtu'] = fec_vc_intf_mtu
    args['handle'] = handle
    args['lsp_handle'] = lsp_handle
    args['mode'] = mode
    args['fec_type'] = fec_type
    args['fec_vc_type'] = fec_vc_type
    args['num_lsps'] = num_lsps
    args['fec_vc_group_id'] = fec_vc_group_id
    args['fec_vc_id_start'] = fec_vc_id_start
    args['fec_vc_id_step'] = fec_vc_id_step
    args['egress_label_mode'] = egress_label_mode
    args['label_value_start'] = label_value_start
    args['fec_ip_prefix_step'] = fec_ip_prefix_step

    # Below arguments are not supported by spirent, when spirent adds
    # this functionality the arguments can be uncommented
    # args['fec_vc_mac_range_enable'] = fec_vc_mac_range_enable
    # args['fec_vc_label_value_start'] = fec_vc_label_value_start
    # args['fec_vc_peer_address'] = fec_vc_peer_address
    # args['fec_vc_mac_range_first_vlan_id'] = fec_vc_mac_range_first_vlan_id
    # args['fec_vc_mac_range_count'] = fec_vc_mac_range_count
    # args['fec_vc_atm_max_cells'] = fec_vc_atm_max_cells
    # args['fec_vc_cem_option'] = fec_vc_cem_option
    # args['fec_vc_atm_enable'] = fec_vc_atm_enable
    # args['fec_vc_fec_type'] = fec_vc_fec_type
    # args['fec_vc_cem_payload'] = fec_vc_cem_payload
    # args['fec_vc_cem_payload_enable'] = fec_vc_cem_payload_enable
    # args['fec_vc_cem_option_enable'] = fec_vc_cem_option_enable
    # args['packing_enable'] = packing_enable
    # args['fec_vc_intf_desc'] = fec_vc_intf_desc

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ldp_route_config.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if 'ldpConnectedInterface' in hndl:
            ipv4_handle = __get_parent_handle(hndl, 'ipv4')
            ldpBasicRouter = invoke_ixnet(rt_handle, 'getList', ipv4_handle, 'ldpBasicRouter')
            hndl = ldpBasicRouter[0].strip('::ixNet::OBJ-')
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_ldp_route_config', **args))

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'network_group_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['network_group_handle']
            v4_handles.append(ret[-1]['handles'])

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_mld_config(
        rt_handle,
        count=jNone,
        filter_mode=jNone,
        handle=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_len=jNone,
        mld_version=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        port_handle=jNone,
        general_query=jNone,
        ip_router_alert=jNone,
        group_query=jNone,
        active=jNone,
        max_response_time=jNone,
        name=jNone,
        enable_iptv=jNone,
        max_response_control=jNone,
        msg_interval=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_mode=jNone,
        vlan_id_outer_step=jNone,
        vlan_outer_user_priority=jNone):
    """
    :param rt_handle:       RT object
    :param count - <1-4000>
    :param filter_mode - <include|exclude>
    :param handle
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_len - <1-128>
    :param mld_version - <v1|v2>
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4094>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|delete>
    :param port_handle
    :param general_query - <1>
    :param ip_router_alert - <1>
    :param group_query - <1>
    :param active
    :param max_response_time - <0-999999>
    :param name
    :param enable_iptv
    :param max_response_control - <0>
    :param msg_interval - <0-999999999>
    :param vlan_id_outer - <0-4095>
    :param vlan_id_outer_mode - <fixed|increment>
    :param vlan_id_outer_step - <0-4094>
    :param vlan_outer_user_priority - <0-7>
    Spirent Returns:
    {
        "handle": "mldhostconfig1",
        "handles": "mldhostconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1",
        "mld_host_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1",
        "mld_host_iptv_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/iptv",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    vargs = dict()
    args['count'] = count
    args['filter_mode'] = filter_mode
    args['handle'] = handle
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_len'] = intf_prefix_len
    args['mld_version'] = mld_version
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['neighbor_intf_ip_addr_step'] = neighbor_intf_ip_addr_step
    vargs['vlan_id'] = vlan_id
    vargs['vlan_id_mode'] = vlan_id_mode
    vargs['vlan_id_step'] = vlan_id_step
    vargs['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['port_handle'] = port_handle
    args['general_query'] = general_query
    args['ip_router_alert'] = ip_router_alert
    args['group_query'] = group_query
    args['active'] = active
    args['max_response_time'] = max_response_time
    args['name'] = name
    args['enable_iptv'] = enable_iptv
    args['max_response_control'] = max_response_control
    args['msg_interval'] = msg_interval
    vargs['vlan_id_outer'] = vlan_id_outer
    vargs['vlan_id_outer_mode'] = vlan_id_outer_mode
    vargs['vlan_id_outer_step'] = vlan_id_outer_step
    vargs['vlan_outer_user_priority'] = vlan_outer_user_priority
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_mld_config.__doc__, **args)

    vargs = get_arg_value(rt_handle, j_emulation_mld_config.__doc__, **vargs)

    if mode == 'create' and port_handle != jNone:
        _result_ = create_deviceGroup(rt_handle, port_handle, count)
        handle = _result_['device_group_handle']

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret_value = rt_handle.invoke('emulation_mld_config', **args)
        ret.append(ret_value)
        if vargs:
            if mode == 'create':
                vlan_config(rt_handle, vargs, ret_value.get('mld_host_handle'))
            else:
                vlan_config(rt_handle, vargs, hndl)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'mld_host_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['mld_host_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_mld_control(
        rt_handle,
        group_member_handle=jNone,
        handle=jNone,
        mode=jNone):
    """
    :param rt_handle:       RT object
    :param group_member_handle
    :param handle
    :param mode - <join:start|leave:stop|leave_join:restart>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['group_member_handle'] = group_member_handle
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_mld_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_mld_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_mld_group_config(
        rt_handle,
        group_pool_handle=jNone,
        handle=jNone,
        mode=jNone,
        session_handle=jNone,
        source_pool_handle=jNone):
    """
    :param rt_handle:       RT object
    :param group_pool_handle
    :param handle
    :param mode - <create|modify|delete>
    :param session_handle
    :param source_pool_handle

    Spirent Returns:
    {
        "group_handles": "ipv6group1",
        "handle": "mldgroupmembership1",
        "status": "1"
    }

    IXIA Returns:
    {
        "group_handles": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList",
        "mld_group_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList",
        "mld_source_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList/mldUcastIPv6SourceList",
        "source_handles": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList/mldUcastIPv6SourceList",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "group_handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['group_pool_handle'] = group_pool_handle
    args['handle'] = handle
    args['mode'] = mode
    args['session_handle'] = session_handle
    args['source_pool_handle'] = source_pool_handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_mld_group_config.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if source_pool_handle == jNone:
        n_args = dict()
        n_args['mode'] = 'create'
        n_args['num_sources'] = 1
        n_args['handle'] = handle
        n_args['ip_addr_start'] = '::'
        n_ret = rt_handle.invoke('emulation_multicast_source_config', **n_args)
        if 'multicast_source_handle' in n_ret:
            args['source_pool_handle'] = n_ret['multicast_source_handle']

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        if mode == 'create':
            args['session_handle'] = hndl
        ret.append(rt_handle.invoke('emulation_mld_group_config', **args))

        if 'mld_group_handle' in ret[-1]:
            v6_handles.append(ret[-1]['mld_group_handle'])
        if 'mld_source_handle' in ret[-1]:
            v6_handles.append(ret[-1]['mld_source_handle'])

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'mld_group_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['mld_group_handle']
        if 'mld_group_handle' in ret[index]:
            ret[index]['group_handles'] = ret[index]['mld_group_handle']
        if 'mld_source_handle' in ret[index]:
            ret[index]['source_handles'] = ret[index]['mld_source_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_mld_info(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode

    Spirent Returns:
    {
        "group_membership_stats": {
            "group_addr": {
                "ff00::1111": {
                    "host_addr": {
                        "fe80::1": {
                            "join_latency": "0",
                            "leave_latency": "0",
                            "state": "IDLE_MEMBER"
                        }
                    }
                }
            }
        },
        "session": {
            "mldhostconfig1": {
                "avg_join_latency": "0",
                "avg_leave_latency": "0",
                "max_join_latency": "0",
                "max_leave_latency": "0",
                "min_join_latency": "0",
                "min_leave_latency": "0"
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/item:1": {
            "session": {
                "invalid_packets_rx": "0",
                "joined_groups": "0",
                "total_frames_rx": "0",
                "total_frames_tx": "0",
                "v1_done_rx": "0",
                "v1_done_tx": "0",
                "v1_general_queries_rx": "0",
                "v1_general_queries_tx": "0",
                "v1_group_specific_queries_rx": "0",
                "v1_group_specific_queries_tx": "0",
                "v1_membership_reports_rx": "0",
                "v1_membership_reports_tx": "0",
                "v2_allow_new_sources_rx": "0",
                "v2_allow_new_sources_tx": "0",
                "v2_block_old_sources_rx": "0",
                "v2_block_old_sources_tx": "0",
                "v2_change_to_exclude_rx": "0",
                "v2_change_to_exclude_tx": "0",
                "v2_change_to_include_rx": "0",
                "v2_change_to_include_tx": "0",
                "v2_general_queries_rx": "0",
                "v2_general_queries_tx": "0",
                "v2_group_specific_queries_rx": "0",
                "v2_group_specific_queries_tx": "0",
                "v2_membership_reports_rx": "0",
                "v2_membership_reports_tx": "0",
                "v2_mode_is_exclude_rx": "0",
                "v2_mode_is_exclude_tx": "0",
                "v2_mode_is_include_rx": "0",
                "v2_mode_is_include_tx": "0"
            }
        },
        "Device Group 2": {
            "aggregate": {
                "invalid_packets_rx": "0",
                "joined_groups": "0",
                "sessions_down": "1",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "0",
                "status": "started",
                "total_frames_rx": "0",
                "total_frames_tx": "0",
                "v1_done_rx": "0",
                "v1_done_tx": "0",
                "v1_general_queries_rx": "0",
                "v1_general_queries_tx": "0",
                "v1_group_specific_queries_rx": "0",
                "v1_group_specific_queries_tx": "0",
                "v1_membership_reports_rx": "0",
                "v1_membership_reports_tx": "0",
                "v2_allow_new_sources_rx": "0",
                "v2_allow_new_sources_tx": "0",
                "v2_block_old_sources_rx": "0",
                "v2_block_old_sources_tx": "0",
                "v2_change_to_exclude_rx": "0",
                "v2_change_to_exclude_tx": "0",
                "v2_change_to_include_rx": "0",
                "v2_change_to_include_tx": "0",
                "v2_general_queries_rx": "0",
                "v2_general_queries_tx": "0",
                "v2_group_and_source_specific_queries_rx": "0",
                "v2_group_and_source_specific_queries_tx": "0",
                "v2_group_specific_queries_rx": "0",
                "v2_group_specific_queries_tx": "0",
                "v2_membership_reports_rx": "0",
                "v2_membership_reports_tx": "0",
                "v2_mode_is_exclude_rx": "0",
                "v2_mode_is_exclude_tx": "0",
                "v2_mode_is_include_rx": "0",
                "v2_mode_is_include_tx": "0"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl

        stats = dict()
        args['mode'] = 'aggregate'
        stats.update(rt_handle.invoke('emulation_mld_info', **args))
        args['mode'] = 'stats'
        stats.update(rt_handle.invoke('emulation_mld_info', **args))
        args['mode'] = 'stats_per_session'
        stats.update(rt_handle.invoke('emulation_mld_info', **args))
        ret.append(stats)


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_multicast_group_config(
        rt_handle,
        handle=jNone,
        num_groups=jNone,
        mode=jNone,
        ip_addr_start=jNone,
        ip_addr_step=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param num_groups - <1-65535>
    :param mode - <create|modify|delete>
    :param ip_addr_start
    :param ip_addr_step

    Spirent Returns:
    {
        "handle": "ipv4group1",
        "handles": "ipv4group1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/igmpMcastIPv4GroupList:HLAPI0",
        "handles": "/igmpMcastIPv4GroupList:HLAPI0",
        "multicast_group_handle": "/igmpMcastIPv4GroupList:HLAPI0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['num_groups'] = num_groups
    args['mode'] = mode
    args['ip_addr_start'] = ip_addr_start
    if ip_addr_step is not jNone and (re.match(r'^\d+\.\d+\.\d+\.\d+$', ip_addr_start)):
        args['ip_addr_step'] = ip_addr_step if re.match(r'^\d+\.\d+\.\d+\.\d+$', ip_addr_step) \
                           else ipaddress.IPv4Address(int(ip_addr_step))
    else:
        args['ip_addr_step'] = ipaddress.IPv6Address(int(ip_addr_step)) if re.match(r'^\d+$', ip_addr_step) \
                           else ip_addr_step

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_multicast_group_config.__doc__, **args)

    ret = []
    ret.append(
        rt_handle.invoke(
            'emulation_multicast_group_config',
            **args))

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'multicast_group_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['multicast_group_handle']

            if re.search("IPv4", ret[-1]['handles']):
                v4_handles.append(ret[-1]['handles'])
            elif re.search("IPv6", ret[-1]['handles']):
                v6_handles.append(ret[-1]['handles'])

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_multicast_source_config(
        rt_handle,
        handle=jNone,
        num_sources=jNone,
        mode=jNone,
        ip_addr_start=jNone,
        ip_addr_step=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param num_sources - <1-65535>
    :param mode - <create|modify|delete>
    :param ip_addr_start
    :param ip_addr_step

    Spirent Returns:
    {
        "handle": "multicastSourcePool(0)",
        "handles": "multicastSourcePool(0)",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/igmpUcastIPv4SourceList:HLAPI0",
        "handles": "/igmpUcastIPv4SourceList:HLAPI0",
        "multicast_source_handle": "/igmpUcastIPv4SourceList:HLAPI0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['num_sources'] = num_sources
    args['mode'] = mode
    args['ip_addr_start'] = ip_addr_start
    if ip_addr_step is not jNone and (re.match(r'^\d+\.\d+\.\d+\.\d+$', ip_addr_start)):
        args['ip_addr_step'] = ip_addr_step if re.match(r'^\d+\.\d+\.\d+\.\d+$', ip_addr_step) \
                           else ipaddress.IPv4Address(int(ip_addr_step))
    else:
        args['ip_addr_step'] = ipaddress.IPv6Address(int(ip_addr_step)) if re.match(r'^\d+$', ip_addr_step) \
                           else ip_addr_step

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_multicast_source_config.__doc__, **args)

    ret = []
    ret.append(
        rt_handle.invoke(
            'emulation_multicast_source_config',
            **args))

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'multicast_source_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['multicast_source_handle']

            if re.search("IPv4", ret[-1]['handles']):
                v4_handles.append(ret[-1]['handles'])
            elif re.search("IPv6", ret[-1]['handles']):
                v6_handles.append(ret[-1]['handles'])

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ospf_config(
        rt_handle,
        area_id=jNone,
        area_id_step=jNone,
        bfd_registration=jNone,
        count=jNone,
        dead_interval=jNone,
        demand_circuit=jNone,
        graceful_restart_enable=jNone,
        handle=jNone,
        hello_interval=jNone,
        interface_cost=jNone,
        intf_prefix_length=jNone,
        md5_key_id=jNone,
        option_bits=jNone,
        router_id=jNone,
        router_priority=jNone,
        session_type=jNone,
        te_max_bw=jNone,
        te_max_resv_bw=jNone,
        te_metric=jNone,
        te_unresv_bw_priority0=jNone,
        te_unresv_bw_priority1=jNone,
        te_unresv_bw_priority2=jNone,
        te_unresv_bw_priority3=jNone,
        te_unresv_bw_priority4=jNone,
        te_unresv_bw_priority5=jNone,
        te_unresv_bw_priority6=jNone,
        te_unresv_bw_priority7=jNone,
        vci=jNone,
        vci_step=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        vpi=jNone,
        vpi_step=jNone,
        mac_address_start=jNone,
        port_handle=jNone,
        network_type=jNone,
        mode=jNone,
        intf_ip_addr=jNone,
        gateway_ip_addr=jNone,
        authentication_mode=jNone,
        te_admin_group=jNone,
        intf_ip_addr_step=jNone,
        gateway_ip_addr_step=jNone,
        password=jNone,
        mtu=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):
        # Below arguments are not supported by spirent, when spirent adds
        # this functionality the arguments can be uncommented
        # neighbor_router_id=jNone,
        # te_enable=jNone,
        # vlan=jNone,
        # graceful_restart_helper_mode_enable=jNone,
        # strict_lsa_checking=jNone,
        # support_reason_sw_reload_or_upgrade=jNone,
        # support_reason_sw_restart=jNone,
        # support_reason_switch_to_redundant_processor_control=jNone,
        # support_reason_unknown=jNone,
        # instance_id=jNone,

    """
    :param rt_handle:       RT object
    :param area_id
    :param area_id_step
    :param bfd_registration
    :param count - <1-100>
    :param dead_interval - <1-65535>
    :param demand_circuit
    :param graceful_restart_enable
    :param handle
    :param hello_interval - <1-65535>
    :param interface_cost - <1-65535>
    :param intf_prefix_length - <1-128>
    :param md5_key_id - <1-255>
    :param option_bits
    :param router_id
    :param router_priority - <0-255>
    :param session_type - <ospfv2|ospfv3>
    :param te_max_bw
    :param te_max_resv_bw
    :param te_metric
    :param te_unresv_bw_priority0
    :param te_unresv_bw_priority1
    :param te_unresv_bw_priority2
    :param te_unresv_bw_priority3
    :param te_unresv_bw_priority4
    :param te_unresv_bw_priority5
    :param te_unresv_bw_priority6
    :param te_unresv_bw_priority7
    :param vci - <0-65535>
    :param vci_step - <0-65535>
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4095>
    :param vlan_user_priority - <0-7>
    :param vpi
    :param vpi_step
    :param mac_address_start
    :param port_handle
    :param network_type - <broadcast|ptop|native:ptomp>
    :param mode - <create|delete|modify|active:enable|inactive:disable>
    :param intf_ip_addr
    :param gateway_ip_addr
    :param authentication_mode - <none:null|simple|md5>
    :param te_admin_group
    :param intf_ip_addr_step
    :param gateway_ip_addr_step
    :param password
    :param mtu - <68-9216>
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <0-4095>
    :param vlan_outer_user_priority - <0-7>
    #Below arguments are not supported by spirent, when spirent adds
    #this functionality the arguments can be uncommented
    #neighbor_router_id
    #te_enable
    #graceful_restart_helper_mode_enable
    #strict_lsa_checking
    #support_reason_sw_reload_or_upgrade
    #support_reason_sw_restart
    #support_reason_switch_to_redundant_processor_control
    #support_reason_unknown
    #instance_id


    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "session_router": "ospfv2routerconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1",
        "ospfv2_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1",
        "status": "1"
    }

    Common Return Keys:
        "handles"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['area_id'] = area_id
    args['area_id_step'] = area_id_step
    args['bfd_registration'] = bfd_registration
    args['count'] = count
    args['dead_interval'] = dead_interval
    args['demand_circuit'] = demand_circuit
    args['graceful_restart_enable'] = graceful_restart_enable
    args['handle'] = handle
    args['hello_interval'] = hello_interval
    args['interface_cost'] = interface_cost
    args['intf_prefix_length'] = intf_prefix_length
    args['md5_key_id'] = md5_key_id
    args['option_bits'] = option_bits
    args['router_id'] = router_id
    args['router_priority'] = router_priority
    args['session_type'] = session_type
    args['te_max_bw'] = te_max_bw
    args['te_max_resv_bw'] = te_max_resv_bw
    args['te_metric'] = te_metric
    args['te_unresv_bw_priority0'] = te_unresv_bw_priority0
    args['te_unresv_bw_priority1'] = te_unresv_bw_priority1
    args['te_unresv_bw_priority2'] = te_unresv_bw_priority2
    args['te_unresv_bw_priority3'] = te_unresv_bw_priority3
    args['te_unresv_bw_priority4'] = te_unresv_bw_priority4
    args['te_unresv_bw_priority5'] = te_unresv_bw_priority5
    args['te_unresv_bw_priority6'] = te_unresv_bw_priority6
    args['te_unresv_bw_priority7'] = te_unresv_bw_priority7
    args['vci'] = vci
    args['vci_step'] = vci_step
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['vpi'] = vpi
    args['vpi_step'] = vpi_step
    args['mac_address_start'] = mac_address_start
    args['network_type'] = network_type
    args['mode'] = mode
    args['te_admin_group'] = te_admin_group
    args['password'] = password
    args['mtu'] = mtu
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['neighbor_intf_ip_addr_step'] = neighbor_intf_ip_addr_step
    args['vlan_outer_id'] = vlan_outer_id
    args['vlan_outer_id_mode'] = vlan_outer_id_mode
    args['vlan_outer_id_step'] = vlan_outer_id_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority
    args['authentication_mode'] = authentication_mode
    nargs = dict()
    nargs['ipv6_intf_addr' if 'ospfv3' in session_type else 'intf_ip_addr'] = intf_ip_addr
    nargs['ipv6_gateway' if 'ospfv3' in session_type else 'gateway'] = gateway_ip_addr
    nargs['ipv6_intf_addr_step' if 'ospfv3' in session_type else 'intf_ip_addr_step'] = intf_ip_addr_step
    nargs['ipv6_gateway_step' if 'ospfv3' in session_type else 'gateway_step'] = gateway_ip_addr_step
    # Below arguments are not supported by spirent, when spirent adds
    # this functionality the arguments can be uncommented
    # args['neighbor_router_id'] = neighbor_router_id
    # args['te_enable'] = te_enable
    # args['vlan'] = vlan
    # args['graceful_restart_helper_mode_enable'] = graceful_restart_helper_mode_enable
    # args['strict_lsa_checking'] = strict_lsa_checking
    # args['support_reason_sw_reload_or_upgrade'] = support_reason_sw_reload_or_upgrade
    # args['support_reason_sw_restart'] = support_reason_sw_restart
    # args['support_reason_switch_to_redundant_processor_control'] = support_reason_switch_to_redundant_processor_control
    # args['support_reason_unknown'] = support_reason_unknown
    # args['instance_id'] = instance_id

    # ***** Argument Modification *****

    if te_admin_group != jNone:
        if not re.match('^0x[0-9a-f]{1,8}$', te_admin_group):
            te_admin_group = int(te_admin_group)
            te_admin_group = hex(te_admin_group)
            args['te_admin_group'] = te_admin_group
        else:
            args['te_admin_group'] = te_admin_group
    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ospf_config.__doc__, **args)
    if args.get('mac_address_start'):
        args['mac_address_init'] = args.pop('mac_address_start')
    args['lsa_discard_mode'] = 0
    args['return_detailed_handles'] = 1
    if args.get('authentication_mode') == 'md5' and args.get('password'):
        args['md5_key'] = args.pop('password')

    vlan_dict = dict()
    for key in list(nargs.keys()):
        if nargs[key] == jNone:
            del nargs[key]

    vlanArgs = ['vlan_id', 'vlan_id_mode', 'vlan_id_step', 'vlan_user_priority', 'vlan_outer_id',
                'vlan_outer_id_mode', 'vlan_outer_id_step', 'vlan_outer_user_priority']
    for arg in vlanArgs:
        if args.get(arg):
            vlan_dict[arg] = args.pop(arg)

    if mode == 'create':
        __check_and_raise(router_id)
        __check_and_raise(session_type)
        if port_handle != jNone:
            count = args['count'] if args.get('count') else jNone
            #create_topology(rt_handle, port_handle)
            _result_ = create_deviceGroup(rt_handle, port_handle, count)
            handle = _result_['device_group_handle']
            handle_map[handle] = port_handle
            handle_map[port_handle].append(handle)
        elif handle == jNone:
            raise Exception("Please provide either handle or port_handle")
    else:
        __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]

    if mode == 'delete' or mode == 'create':
        vargs = dict()
        vargs['action'] = 'stop_protocol'
        for hndl in handle:
            vargs['handle'] = __get_parent_handle(hndl, 'deviceGroup')
            rt_handle.invoke('test_control', **vargs)

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        if hndl in session_map:
            args['session_type'] = session_map[hndl]
        ret.append(rt_handle.invoke('emulation_ospf_config', **args))
        if mode == 'create' and port_handle != jNone and (len(nargs.keys()) > 0 or len(vlan_dict.keys()) > 0):
            if vlan_dict:
                vlan_config(rt_handle, vlan_dict, ret[-1]['{}_handle'.format(session_type)])
            if nargs:
                nargs['mode'] = 'modify'
                ip_version = 'ipv4' if 'ospfv2' in session_type else 'ipv6'
                nargs['protocol_handle'] = __get_parent_handle(ret[-1]['{}_handle'.format(session_type)], ip_version)
                rt_handle.invoke('interface_config', **nargs)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'ospfv2_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['ospfv2_handle']
        elif 'ospfv3_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['ospfv3_handle']
        if mode == 'create':
            port_handle = __get_handle(handle[index])
            handle_map[port_handle].append(ret[index]['handles'])
            handle_map[ret[index]['handles']] = port_handle
            session_map[ret[index]['handles']] = session_type

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ospf_control(rt_handle, handle=jNone,
                             port_handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle
    :param mode - <start|stop|restart|stop_hellos:stop_hello|resume_hellos:resume_hello|advertise>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['port_handle'] = port_handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ospf_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = split_stack_and_handle(hndl)[1]
        ret.append(rt_handle.invoke('emulation_ospf_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ospf_network_group_config(rt_handle):
    """
    :param rt_handle:       RT object
    :return response from rt_handle.invoke(<parameters>)

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    ret = rt_handle.invoke('emulation_ospf_network_group_config', **args)

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ospf_topology_route_config(
        rt_handle,
        elem_handle=jNone,
        external_number_of_prefix=jNone,
        external_prefix_length=jNone,
        external_prefix_metric=jNone,
        external_prefix_step=jNone,
        external_prefix_type=jNone,
        grid_col=jNone,
        grid_row=jNone,
        summary_number_of_prefix=jNone,
        summary_prefix_length=jNone,
        summary_prefix_metric=jNone,
        type=jNone,
        mode=jNone,
        summary_prefix_start=jNone,
        handle=jNone,
        summary_prefix_step=jNone,
        router_abr=jNone,
        router_asbr=jNone,
        grid_router_id=jNone,
        grid_router_id_step=jNone,
        external_prefix_start=jNone,
        nssa_prefix_start=jNone,
        nssa_prefix_step=jNone,
        nssa_prefix_length=jNone,
        nssa_number_of_prefix=jNone,
        nssa_prefix_metric=jNone,
        grid_prefix_start=jNone,
        grid_prefix_step=jNone,
        grid_prefix_length=jNone,
        link_te_max_bw=jNone,
        link_te_max_resv_bw=jNone,
        link_te_metric=jNone,
        link_te_unresv_bw_priority0=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_length=jNone,
        router_id=jNone,
        router_id_step=jNone):
        # link_te=jNone,
    """
    :param rt_handle:       RT object
    :param elem_handle
    :param external_number_of_prefix - <1-65535>
    :param external_prefix_length - <1-128>
    :param external_prefix_metric - <1-16777215>
    :param external_prefix_step
    :param external_prefix_type - <1-2>
    :param grid_col - <1-10000>
    :param grid_row - <1-10000>
    :param summary_number_of_prefix - <1-16000000>
    :param summary_prefix_length - <1-128>
    :param summary_prefix_metric - <1-16777215>
    :param type - <grid|summary_routes|ext_routes|nssa_routes>
    :param mode - <create|modify|delete>
    :param summary_prefix_start
    :param handle
    :param summary_prefix_step
    :param router_abr
    :param router_asbr
    :param grid_router_id
    :param grid_router_id_step
    :param external_prefix_start
    :param nssa_prefix_start
    :param nssa_prefix_step
    :param nssa_prefix_length - <1-128>
    :param nssa_number_of_prefix - <1-128>
    :param nssa_prefix_metric - <1-16777215>
    :param grid_prefix_start
    :param grid_prefix_step
    :param grid_prefix_length - <1-128>
    :param link_te_max_bw
    :param link_te_max_resv_bw
    :param link_te_metric - <0-65535>
    :param link_te_unresv_bw_priority0
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_length - <1-128>
    :param router_id
    :param router_id_step
    :return response from rt_handle.invoke(<parameters>)

    Spirent Returns:
    {
        "elem_handle": "summarylsablock1",
        "handles": "summarylsablock1",
        "status": "1",
        "summary": {
            "connected_routers": "routerlsa1",
            "summary_lsas": "summarylsablock1",
            "version": "ospfv2"
        }
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/networkGroup:1",
        "ipv4_prefix_interface_handle": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/ospfRouteProperty:1",
        "ipv4_prefix_pools_handle": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1",
        "network_group_handle": "/topology:1/deviceGroup:1/networkGroup:1",
        "status": "1"
    }


    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['elem_handle'] = elem_handle
    args['external_number_of_prefix'] = external_number_of_prefix
    args['external_prefix_length'] = external_prefix_length
    args['external_prefix_metric'] = external_prefix_metric
    args['external_prefix_step'] = external_prefix_step
    args['external_prefix_type'] = external_prefix_type
    args['grid_col'] = grid_col
    args['grid_row'] = grid_row
    args['summary_number_of_prefix'] = summary_number_of_prefix
    args['summary_prefix_length'] = summary_prefix_length
    args['summary_prefix_metric'] = summary_prefix_metric
    args['type'] = type
    args['mode'] = mode
    args['summary_prefix_start'] = summary_prefix_start
    args['handle'] = handle
    args['summary_prefix_step'] = summary_prefix_step
    args['router_abr'] = router_abr
    args['router_asbr'] = router_asbr
    args['external_prefix_start'] = external_prefix_start
    args['nssa_prefix_start'] = nssa_prefix_start
    args['nssa_prefix_step'] = nssa_prefix_step
    args['nssa_prefix_length'] = nssa_prefix_length
    args['nssa_number_of_prefix'] = nssa_number_of_prefix
    args['nssa_prefix_metric'] = nssa_prefix_metric
    args['grid_prefix_start'] = grid_prefix_start
    args['grid_prefix_step'] = grid_prefix_step
    args['grid_prefix_length'] = grid_prefix_length
    args['link_te_max_bw'] = link_te_max_bw
    args['link_te_metric'] = link_te_metric
    args['link_te_max_resv_bw'] = link_te_max_resv_bw
    args['link_te_unresv_bw_priority0'] = link_te_unresv_bw_priority0
    args['router_id_step'] = grid_router_id_step if type == 'grid' else router_id_step
    args['router_id'] = grid_router_id if type == 'grid' else router_id
    # args['link_te'] = link_te

    args = get_arg_value(rt_handle, j_emulation_ospf_topology_route_config.__doc__, **args)
    __check_and_raise(type)

    ospf_type = None
    stack_version = None
    if mode == 'create':
        if re.search("ipv6", handle):
            stack_version = '6'
            ospf_type = 'ospfv3'
        else:
            stack_version = '4'
            ospf_type = 'ospfv2'
    elif mode == 'modify' or mode == 'delete':
        handle = split_stack_and_handle(handle)[1]
        handle = __get_parent_handle(handle, 'networkGroup')
        args['handle'] = handle
        if len(invoke_ixnet(rt_handle, "getList", handle+"/networkTopology", "ospfv3SimulatedTopologyConfig")) > 0:
            ospf_type = 'ospfv3'
            stack_version = '6'
        elif len(invoke_ixnet(rt_handle, "getList", handle+"/networkTopology", "ospfSimulatedTopologyConfig")) > 0:
            ospf_type = 'ospfv2'
            stack_version = '4'

    if type == 'summary_routes':
        if ospf_type == 'ospfv3':
            args['type'] = 'linear'
            if args.get('summary_prefix_start'):
                args['inter_area_prefix_network_address'] = args.pop('summary_prefix_start')
            if args.get('summary_prefix_step'):
                nargs = dict()
                nargs['pattern'] = 'counter'
                nargs['counter_start'] = summary_prefix_start
                ipv4_v6_step = args.pop('summary_prefix_step')
                ipv4_v6_step = int(ipv4_v6_step) if re.match(r'^\d+$', ipv4_v6_step) is not None else ipv4_v6_step
                nargs['counter_step'] = ipaddress.IPv6Address(ipv4_v6_step)
                nargs['counter_direction'] = 'increment'
                _result_ = rt_handle.invoke('multivalue_config', **nargs)
                args['inter_area_prefix_network_address'] = _result_['multivalue_handle']
            if args.get('summary_prefix_length'):
                args['inter_area_prefix_prefix'] = args.pop('summary_prefix_length')
            if args.get('summary_number_of_prefix'):
                args['inter_area_prefix_prefix_count'] = args.pop('summary_number_of_prefix')
            if args.get('summary_prefix_metric'):
                args['inter_area_prefix_metric'] = args.pop('summary_prefix_metric')
            args['inter_area_prefix_active'] = '1'
        else:
            args['type'] = 'linear'
            if args.get('summary_prefix_start'):
                args['summary_network_address'] = args.pop('summary_prefix_start')
            if args.get('summary_prefix_step'):
                args['summary_network_address_step'] = args.pop('summary_prefix_step') \
                if re.match(r'^\d+\.\d+\.\d+\.\d+$', args.get('summary_prefix_step')) \
                else ipaddress.IPv4Address(int(args.pop('summary_prefix_step')))
            if args.get('summary_prefix_length'):
                args['summary_prefix'] = args.pop('summary_prefix_length')
            if args.get('summary_number_of_prefix'):
                args['summary_number_of_routes'] = args.pop('summary_number_of_prefix')
            if args.get('summary_prefix_metric'):
                args['summary_metric'] = args.pop('summary_prefix_metric')
            args['summary_active'] = '1'
    elif type == 'ext_routes':
        args['type'] = 'linear'
        if args.get('external_prefix_type') == '1':
            args.pop('external_prefix_type')
            if args.get('external_prefix_length'):
                args['external1_prefix'] = args.pop('external_prefix_length')
            if args.get('external_prefix_step'):
                args['external1_network_address_step'] = args.pop('external_prefix_step') \
                    if re.match(r'^\d+\.\d+\.\d+\.\d+$', args.get('external_prefix_step')) \
                    else ipaddress.IPv4Address(int(args.pop('external_prefix_step')))
            if args.get('external_number_of_prefix'):
                args['external1_number_of_routes'] = args.pop('external_number_of_prefix')
            if args.get('external_prefix_metric'):
                args['external1_metric'] = args.pop('external_prefix_metric')
            if args.get('external_prefix_start'):
                args['external1_network_address'] = args.pop('external_prefix_start')
            args['external1_active'] = '1'
        elif args.get('external_prefix_type') == '2':
            args.pop('external_prefix_type')
            if args.get('external_prefix_length'):
                args['external2_prefix'] = args.pop('external_prefix_length')
            if args.get('external_prefix_step'):
                args['external2_network_address_step'] = args.pop('external_prefix_step') \
                    if re.match(r'^\d+\.\d+\.\d+\.\d+$', args.get('external_prefix_step')) \
                    else ipaddress.IPv4Address(int(args.pop('external_prefix_step')))
            if args.get('external_number_of_prefix'):
                args['external2_number_of_routes'] = args.pop('external_number_of_prefix')
            if args.get('external_prefix_metric'):
                args['external2_metric'] = args.pop('external_prefix_metric')
            if args.get('external_prefix_start'):
                args['external2_network_address'] = args.pop('external_prefix_start')
            args['external2_active'] = '1'
    elif type == 'nssa_routes':
        if ospf_type == 'ospfv2':
            if args.get('nssa_prefix_step'):
                nssa_prefix_step = args.pop('nssa_prefix_step') \
                if re.match(r'^\d+\.\d+\.\d+\.\d+$', args.get('nssa_prefix_step')) \
                else ipaddress.IPv4Address(int(args.pop('nssa_prefix_step')))
        else:
            if args.get('nssa_prefix_step'):
                nssa_prefix_step = ipaddress.IPv6Address(int(args.pop('nssa_prefix_step'))) \
                if re.match(r'^\d+$', args.get('nssa_prefix_step')) \
                else args.pop('nssa_prefix_step')
        args['type'] = 'linear'
        if args.get('nssa_prefix_start'):
            args['nssa_network_address'] = args.pop('nssa_prefix_start')
        if args.get('nssa_prefix_step'):
            args['nssa_network_address_step'] = args.pop('nssa_prefix_step')
        if args.get('nssa_prefix_length'):
            args['nssa_prefix'] = args.pop('nssa_prefix_length')
        if args.get('nssa_number_of_prefix'):
            args['nssa_number_of_routes'] = args.pop('nssa_number_of_prefix')
        if args.get('nssa_prefix_metric'):
            args['nssa_metric'] = args.pop('nssa_prefix_metric')
        args['nssa_active'] = '1'
    elif type == 'grid':
        if args.get('grid_prefix_length'):
            args['subnet_prefix_length'] = args.pop('grid_prefix_length')
        if ospf_type == 'ospfv2':
            if args.get('grid_prefix_start'):
                args['from_ip'] = args.pop('grid_prefix_start')
        else:
            if args.get('grid_prefix_start'):
                args['from_ipv6'] = args.pop('grid_prefix_start')
        if args.get('grid_prefix_step'):
            nargs = dict()
            nargs['pattern'] = 'counter'
            nargs['counter_start'] = grid_prefix_start
            nargs['counter_step'] = args.pop('grid_prefix_step')
            nargs['counter_direction'] = 'increment'
            _result_ = rt_handle.invoke('multivalue_config', **nargs)
            if ospf_type == 'ospfv2':
                args['from_ip'] = _result_['multivalue_handle']
            else:
                args['from_ipv6'] = _result_['multivalue_handle']

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if intf_ip_addr != jNone or intf_prefix_length != jNone:
        nargs = dict()
        nargs['mode'] = 'modify'
        nargs['handle'] = args['handle']
        if intf_ip_addr != jNone:
            nargs['intf_ip_addr'] = intf_ip_addr
            if intf_ip_addr_step != jNone:
                nargs['intf_ip_addr_step'] = intf_ip_addr_step
        if intf_prefix_length != jNone:
            nargs['intf_prefix_length'] = intf_prefix_length
        _result_ = rt_handle.invoke('emulation_ospf_config', **nargs)

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_ospf_network_group_config', **args))
        if mode == 'create':
            try:
                nargs = dict()
                nargs['mode'] = 'modify'
                deviceGroup = __get_parent_handle(hndl, 'deviceGroup')
                nargs['handle'] = invoke_ixnet(rt_handle, 'getList', deviceGroup, 'networkGroup')
                nargs['connected_to_handle'] = hndl
                nargs['enable_device'] = 1
                rt_handle.invoke('emulation_ospf_network_group_config', **nargs)
            except:
                rt_handle.log("WARN", "connected_to_handle for ospf supports from IxOS 8.5")

        if 'ipv4_prefix_pools_handle' in ret[-1]:
            v4_handles.append(ret[-1]['network_group_handle'])
        elif 'ipv6_prefix_pools_handle' in ret[-1]:
            v6_handles.append(ret[-1]['network_group_handle'])

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'summary_handle' in ret[index] and type == 'summary_routes':
            ret[index]['handles'] = ret[index]['summary_handle']
        elif 'v3_inter_area_prefix_handle' in ret[index] and type == 'summary_routes':
            ret[index]['handles'] = ret[index]['v3_inter_area_prefix_handle']
        elif 'external1_handle' in ret[index] and external_prefix_type == '1':
            ret[index]['handles'] = ret[index]['external1_handle']
        elif 'external2_handle' in ret[index] and external_prefix_type == '2':
            ret[index]['handles'] = ret[index]['external2_handle']
        elif 'nssa_handle' in ret[index] and type == 'nssa_routes':
            ret[index]['handles'] = ret[index]['nssa_handle']
        elif 'v3_nssa_handle' in ret[index] and type == 'nssa_routes':
            ret[index]['handles'] = ret[index]['v3_nssa_handle']
        elif 'network_group_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['network_group_handle']
        if ret[index].get('handles'):
            ret[index]['handles'] = '|:STACK=='+stack_version+':|'+ret[index]['handles']
    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ospf_lsa_config(
        rt_handle,
        type=jNone,
        mode=jNone,
        handle=jNone,
        external_number_of_prefix=jNone,
        external_prefix_length=jNone,
        external_prefix_metric=jNone,
        external_prefix_step=jNone,
        external_prefix_type=jNone,
        summary_number_of_prefix=jNone,
        summary_prefix_length=jNone,
        summary_prefix_metric=jNone,
        summary_prefix_start=jNone,
        summary_prefix_step=jNone,
        router_abr=jNone,
        router_asbr=jNone,
        external_prefix_start=jNone,
        nssa_prefix_length=jNone,
        nssa_prefix_step=jNone,
        nssa_number_of_prefix=jNone,
        nssa_prefix_metric=jNone,
        nssa_prefix_start=jNone,
        intra_area_link_state_id=jNone,
        intra_area_prefix_start=jNone,
        intra_area_prefix_step=jNone,
        intra_area_number_of_prefix=jNone,
        intra_area_prefix_length=jNone,
        intra_area_prefix_metric=jNone,
        intra_area_ref_ls_type=jNone,
        intra_area_ref_link_state_id=jNone,
        intra_area_ref_advertising_router_id=jNone,
        te_metric=jNone,
        te_max_bw=jNone,
        te_max_resv_bw=jNone,
        te_unres_bw_priority0=jNone,
        te_unres_bw_priority1=jNone,
        te_unres_bw_priority2=jNone,
        te_unres_bw_priority3=jNone,
        te_unres_bw_priority4=jNone,
        te_unres_bw_priority5=jNone,
        te_unres_bw_priority6=jNone,
        te_unres_bw_priority7=jNone,
        te_tlv_type=jNone,
        adv_router_id=jNone):

    """
    :param rt_handle:       RT object
    :param external_number_of_prefix
    :param external_prefix_length - <1-128>
    :param external_prefix_metric - <1-16777215>
    :param external_prefix_step - <1-16777215>
    :param external_prefix_type - <1-2>
    :param summary_number_of_prefix
    :param summary_prefix_length - <1-128>
    :param summary_prefix_metric - <1-65535>
    :param type
    :param mode - <create|modify|delete|reset>
    :param summary_prefix_start
    :param handle
    :param summary_prefix_step - <1-65535>
    :param router_abr
    :param router_asbr
    :param external_prefix_start
    :param nssa_prefix_length - <1-128>
    :param nssa_prefix_step
    :param nssa_number_of_prefix
    :param nssa_prefix_metric - <1-16777215>
    :param nssa_prefix_start
    :param intra_area_link_state_id
    :param intra_area_prefix_start
    :param intra_area_prefix_step
    :param intra_area_number_of_prefix
    :param intra_area_prefix_length - <1-128>
    :param intra_area_prefix_metric - <0-65535>
    :param intra_area_ref_ls_type
    :param intra_area_ref_link_state_id
    :param intra_area_ref_advertising_router_id
    :param te_metric - <0-65535>
    :param te_max_bw
    :param te_max_resv_bw
    :param te_unres_bw_priority0
    :param te_unres_bw_priority1
    :param te_unres_bw_priority2
    :param te_unres_bw_priority3
    :param te_unres_bw_priority4
    :param te_unres_bw_priority5
    :param te_unres_bw_priority6
    :param te_unres_bw_priority7
    :param te_tlv_type
    :param adv_router_id
    :return response from rt_handle.invoke(<parameters>)

    Spirent Returns:
    {
        "handles": "summarylsablock1",
        "status": "1",
        "summary": {
            "connected_routers": "routerlsa1",
            "summary_lsas": "summarylsablock1",
            "version": "ospfv2"
        }
    }

    IXIA Returns:
    {
        'handles': '/topology:1/deviceGroup:1/networkGroup:1',
        'external2_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/
        ospfPseudoRouterType2ExtRoutes:1',
        'sim_interface_ipv4_config_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simInterface:1/simInterfaceIPv4Config:1',
        'nssa_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterStubRoutes:1',
        'summary_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterSummaryRoutes:1',
        'simulated_interface_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simInterface:1/simInterfaceIPv4Config:1/
        ospfPseudoInterface:1',
        'network_group_handle': '/topology:1/deviceGroup:1/networkGroup:1',
        'external1_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/
        ospfPseudoRouterType1ExtRoutes:1',
        'simulated_router_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1',
        'stub_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterStubNetworks:1',
        'status': '1'

    }


    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['type'] = type
    args['mode'] = mode
    args['handle'] = handle
    args['router_id'] = adv_router_id
    __check_and_raise(type)
    ospf_type = None
    stack_version = None
    if mode == 'create':
        if re.search("ipv6", handle):
            ospf_type = 'ipv6_prefix'
            args['type'] = 'ipv6-prefix'
            stack_version = '6'
        else:
            ospf_type = 'ipv4_prefix'
            args['type'] = 'ipv4-prefix'
            stack_version = '4'
    elif mode == 'modify' or mode == 'delete':
        if '|:STACK==' in handle:
            handle = split_stack_and_handle(handle)[1]
            handle = __get_parent_handle(handle, 'networkGroup')
        args['handle'] = handle
        if len(invoke_ixnet(rt_handle, "getList", handle, "ipv4PrefixPools")) > 0:
            ospf_type = 'ipv4_prefix'
            args['type'] = 'ipv4-prefix'
            stack_version = '4'
        elif len(invoke_ixnet(rt_handle, "getList", handle, "ipv6PrefixPools")) > 0:
            ospf_type = 'ipv6_prefix'
            args['type'] = 'ipv6-prefix'
            stack_version = '6'
    if ospf_type == 'ipv6_prefix':
        route_origin = {
            'summary_pool' : 'anotherarea',
            'external_type_1' : 'externaltype1',
            'external_type_2' : 'externaltype2'
        }
    else:
        route_origin = {
            'summary_pool' : 'another_area',
            'external_type_1' : 'external_type_1',
            'external_type_2' : 'external_type_2'
        }
    if summary_prefix_step != jNone:
        summary_prefix_step = summary_prefix_step \
            if re.match(r'\d+\.\d+\.\d+\.\d+', summary_prefix_step) \
                else ipaddress.IPv4Address(int(summary_prefix_step))
    if external_prefix_step != jNone:
        external_prefix_step = external_prefix_step \
            if re.match(r'\d+\.\d+\.\d+\.\d+', external_prefix_step) \
                else ipaddress.IPv4Address(int(external_prefix_step))
    if type == 'summary_pool' or type == 'ext_pool':
        args[ospf_type+'_network_address'] = summary_prefix_start \
            if 'summary_pool' in type else external_prefix_start
        args[ospf_type+'_network_address_step'] = summary_prefix_step \
            if 'summary_pool' in type else external_prefix_step
        args[ospf_type+'_length'] = summary_prefix_length \
            if 'summary_pool' in type else external_prefix_length
        args[ospf_type+'_number_of_addresses'] = summary_number_of_prefix \
            if 'summary_pool' in type else external_number_of_prefix
        args[ospf_type+'_metric'] = summary_prefix_metric \
            if 'summary_pool' in type else external_prefix_metric
        external_prefix_type = 'external_type_2' \
            if external_prefix_type == '2' else 'external_type_1'
        args[ospf_type+'_route_origin'] = route_origin['summary_pool'] \
            if 'summary_pool' in type else route_origin[external_prefix_type]
    elif type == 'nssa_ext_pool':
        if nssa_prefix_step != jNone:
            nssa_prefix_step = ipaddress.IPv4Address(int(nssa_prefix_step)) \
                if ospf_type == 'ipv4_prefix' else ipaddress.IPv6Address(int(nssa_prefix_step))
        args[ospf_type+'_network_address'] = nssa_prefix_start
        args[ospf_type+'_network_address_step'] = nssa_prefix_step
        args[ospf_type+'_length'] = nssa_prefix_length
        args[ospf_type+'_number_of_addresses'] = nssa_number_of_prefix
        args[ospf_type+'_metric'] = nssa_prefix_metric
        args[ospf_type+'_route_origin'] = 'nssa'
    elif type == 'router':
        args['type'] = 'linear'
        args['router_abr'] = router_abr
        args['router_asbr'] = router_asbr
    elif type == 'opaque_type_9':
        #if re.search("ipv6", handle):
        args['type'] = 'linear'
        args['intra_area_network_address'] = intra_area_prefix_start
        if intra_area_prefix_step != jNone:
            args['intra_area_network_address_step'] = ipaddress.IPv6Address(int(intra_area_prefix_step))
        args['intra_area_prefix_count'] = intra_area_number_of_prefix
        args['prefix'] = intra_area_prefix_length
        args['intra_area_metric'] = intra_area_prefix_metric
        args['intra_area_link_state_id'] = intra_area_link_state_id
        args['intra_area_reference_ls_type'] = intra_area_ref_ls_type
        args['intra_area_referenced_link_state_id'] = intra_area_ref_link_state_id
        args['intra_area_referenced_router_id'] = intra_area_ref_advertising_router_id
    elif type == 'opaque_type_10':
        __check_and_raise(te_tlv_type)
        if te_tlv_type == 'link':
            args['type'] = 'linear'
            args['link_te_metric'] = te_metric
            args['link_te_max_bw'] = te_max_bw
            args['link_te_max_resv_bw'] = te_max_resv_bw
            args['link_te_unresv_bw_priority0'] = te_unres_bw_priority0
            args['link_te_unresv_bw_priority1'] = te_unres_bw_priority1
            args['link_te_unresv_bw_priority2'] = te_unres_bw_priority2
            args['link_te_unresv_bw_priority3'] = te_unres_bw_priority3
            args['link_te_unresv_bw_priority4'] = te_unres_bw_priority4
            args['link_te_unresv_bw_priority5'] = te_unres_bw_priority5
            args['link_te_unresv_bw_priority6'] = te_unres_bw_priority6
            args['link_te_unresv_bw_priority7'] = te_unres_bw_priority7
        else:
            raise Exception("te_tlv_type router is not supporting")

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]
    args = get_arg_value(rt_handle, j_emulation_ospf_lsa_config.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_ospf_network_group_config', **args))
        if mode == 'create':
            try:
                nargs = dict()
                nargs['mode'] = 'modify'
                deviceGroup = __get_parent_handle(hndl, 'deviceGroup')
                nargs['handle'] = invoke_ixnet(rt_handle, 'getList', deviceGroup, 'networkGroup')
                nargs['connected_to_handle'] = hndl
                nargs['enable_device'] = 1
                rt_handle.invoke('emulation_ospf_network_group_config', **nargs)
            except:
                rt_handle.log("WARN", "connected_to_handle for ospf supports from IxOS 8.5")
        if 'ipv4_prefix_pools_handle' in ret[-1]:
            v4_handles.append(ret[-1]['network_group_handle'])
        elif 'ipv6_prefix_pools_handle' in ret[-1]:
            v6_handles.append(ret[-1]['network_group_handle'])

    # ***** Return Value Modification *****
    if mode == 'create':
        for index in range(len(ret)):
            if 'v3_intra_area_prefix_handle' in ret[index] and type == 'opaque_type_9':
                ret[index]['handles'] = ret[index]['v3_intra_area_prefix_handle']
            elif 'network_group_handle' in ret[index]:
                ret[index]['handles'] = ret[index]['network_group_handle']
        if ret[index].get('handles'):
            ret[index]['handles'] = '|:STACK=='+stack_version+':|'+ret[index]['handles']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_pim_config(
        rt_handle,
        bidir_capable=jNone,
        handle=jNone,
        intf_ip_prefix_len=jNone,
        ip_version=jNone,
        override_interval=jNone,
        pim_mode=jNone,
        prune_delay=jNone,
        prune_delay_enable=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        neighbor_intf_ip_addr=jNone,
        router_id=jNone,
        count=jNone,
        type=jNone,
        port_handle=jNone,
        dr_priority=jNone,
        hello_holdtime=jNone,
        hello_interval=jNone,
        prune_delay_tbit=jNone,
        bootstrap_interval=jNone,
        bootstrap_priority=jNone,
        join_prune_holdtime=jNone,
        join_prune_interval=jNone,
        router_id_step=jNone,
        bootstrap_enable=jNone,
        bootstrap_timeout=jNone,
        generation_id_mode=jNone,
        send_generation_id=jNone,
        intf_ip_addr=jNone,
        mac_address_start=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):

        # ****Arguments added below are supported in Ixia but not in Spirent****
        # ****Uncomment once the support is present in Spirent *****
        # bootstrap_support_unicast=jNone,
        # bootstrap_hash_mask_len=jNone,

    """
    :param rt_handle:       RT object
    :param bidir_capable
    :param handle
    :param intf_ip_prefix_len - <1-128>
    :param ip_version - <4|6>
    :param override_interval - <100-32767>
    :param pim_mode - <sm|ssm>
    :param prune_delay - <100-32767>
    :param prune_delay_enable
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <1-4094>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|delete|inactive:disable|active:enable>
    :param neighbor_intf_ip_addr
    :param router_id
    :param count - <1-65535>
    :param type - <remote_rp>
    :param port_handle
    :param dr_priority - <1-4294967295>
    :param hello_holdtime - <1-65535>
    :param hello_interval - <1-65535>
    :param prune_delay_tbit
    :param bootstrap_interval - <1-3600>
    :param bootstrap_priority - <1-255>
    :param join_prune_holdtime - <1-65535>
    :param join_prune_interval - <1-65535>
    :param router_id_step
    :param bootstrap_enable
    :param bootstrap_timeout - <1-65535>
    :param generation_id_mode - <increment|random|fixed:constant>
    :param send_generation_id
    :param intf_ip_addr
    :param mac_address_start
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <1-4094>
    :param vlan_outer_user_priority - <0-7>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1",
        "pim_router_handle": "/topology:1/deviceGroup:1/pimRouter:2",
        "pim_v4_interface_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['bidir_capable'] = bidir_capable
    args['handle'] = handle
    args['intf_ip_prefix_len'] = intf_ip_prefix_len
    args['ip_version'] = ip_version
    args['override_interval'] = override_interval
    args['pim_mode'] = pim_mode
    args['prune_delay'] = prune_delay
    args['prune_delay_enable'] = prune_delay_enable
    args['mode'] = mode
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['router_id'] = router_id
    args['count'] = count
    args['type'] = type
    args['dr_priority'] = dr_priority
    args['hello_holdtime'] = hello_holdtime
    args['hello_interval'] = hello_interval
    args['prune_delay_tbit'] = prune_delay_tbit
    args['bootstrap_interval '] = bootstrap_interval
    args['bootstrap_priority'] = bootstrap_priority
    args['join_prune_holdtime'] = join_prune_holdtime
    args['join_prune_interval'] = join_prune_interval
    args['router_id_step'] = router_id_step
    args['bootstrap_enable'] = bootstrap_enable
    args['bootstrap_timeout'] = bootstrap_timeout
    args['generation_id_mode'] = generation_id_mode
    args['send_generation_id'] = send_generation_id
    vlan_args = dict()
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_mode'] = vlan_id_mode
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_user_priority'] = vlan_user_priority
    vlan_args['vlan_outer_id'] = vlan_outer_id
    vlan_args['vlan_outer_id_mode'] = vlan_outer_id_mode
    vlan_args['vlan_outer_id_step'] = vlan_outer_id_step
    vlan_args['vlan_outer_user_priority'] = vlan_outer_user_priority
    args['intf_ip_addr'] = intf_ip_addr
    args['mac_address_start'] = mac_address_start

    # ****Arguments added below are supported in Ixia but not in Spirent****
    # ****Uncomment once the support is present in Spirent *****
    # args['bootstrap_support_unicast'] = bootstrap_support_unicast
    # args['bootstrap_hash_mask_len'] = bootstrap_hash_mask_len


    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_pim_config.__doc__, **args)
    args['discard_learnt_rp_info'] = 0
    args['learn_selected_rp_set'] = 1
    if args.get('mac_address_start'):
        args['mac_address_init'] = args.pop('mac_address_start')

    vlan_args = get_arg_value(rt_handle, j_emulation_pim_config.__doc__, **vlan_args)

    if mode == 'create':
        if port_handle != jNone:
            handle = create_deviceGroup(rt_handle, port_handle, count)['device_group_handle']
            if args.get('neighbor_intf_ip_addr'):
                args['gateway_intf_ip_addr'] = args.get('neighbor_intf_ip_addr')
        elif handle == jNone:
            raise Exception('Please provide port_handle or handle')
    elif mode == 'modify':
        __check_and_raise(handle)
    else:
        __check_and_raise(handle)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        # if hndl in session_map:
            # args['ip_version'] = session_map[hndl]
        if 'ipv6' in hndl and ip_version == jNone:
            args['ip_version'] = 6
        elif ip_version == jNone:
            args['ip_version'] = 4
        ret_value = rt_handle.invoke('emulation_pim_config', **args)
        ret.append(ret_value)
        eth_handle = None
        if 'ethernet' in hndl:
            eth_handle = __get_parent_handle(hndl, 'ethernet')
        elif ret_value.get('pim_v{}_interface_handle'.format(args['ip_version'])) is not None:
            eth_handle = __get_parent_handle(ret_value.get('pim_v{}_interface_handle'.format(args['ip_version'])), 'ethernet')
        if eth_handle is not None:
            if vlan_args:
                vlan_config(rt_handle, vlan_args, eth_handle)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'pim_v4_interface_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['pim_v4_interface_handle']
        if 'pim_v6_interface_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['pim_v6_interface_handle']
        if mode == 'create':
            session_map[ret[index]['handles']] = args['ip_version']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_pim_control(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <stop|start|restart|join>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_pim_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_pim_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_pim_group_config(
        rt_handle,
        group_pool_handle=jNone,
        handle=jNone,
        interval=jNone,
        join_prune_per_interval=jNone,
        mode=jNone,
        rate_control=jNone,
        register_per_interval=jNone,
        register_stop_per_interval=jNone,
        rp_ip_addr=jNone,
        session_handle=jNone,
        wildcard_group=jNone,
        crp_ip_addr=jNone,
        group_pool_mode=jNone,
        source_pool_handle=jNone,
        group_range_type=jNone,
        default_mdt_mode=jNone,
        join_prune_aggregation_factor=jNone,
        register_tx_iteration_gap=jNone,
        s_g_rpt_group=jNone,
        send_null_register=jNone,
        source_group_mapping=jNone):
    """
    :param rt_handle:       RT object
    :param group_pool_handle
    :param handle
    :param interval - <1-1000>
    :param join_prune_per_interval - <1-1000>
    :param mode - <create|modify|delete>
    :param rate_control
    :param register_per_interval - <1-1000>
    :param register_stop_per_interval - <1-1000>
    :param rp_ip_addr
    :param session_handle
    :param wildcard_group
    :param crp_ip_addr
    :param group_pool_mode - <send|register>
    :param source_pool_handle
    :param group_range_type
    :param default_mdt_mode
    :param join_prune_aggregation_factor
    :param register_tx_iteration_gap - <100-1000>
    :param s_g_rpt_group
    :param send_null_register
    :param source_group_mapping - <one_to_one|fully_meshed>

    Spirent Returns:
    {
        "group_handles": "ipv4group1",
        "group_pool_handle": "ipv4group1",
        "handle": "pimv4groupblk1 pimv4groupblk2",
        "source_handles": "multicastSourcePool(0)",
        "source_pool_handle": "multicastSourcePool(0)",
        "status": "1"
    }

    IXIA Returns:
    {
        "group_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4JoinPruneList",
        "pim_v4_candidate_rp_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4CandidateRPsList",
        "pim_v4_join_prune_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4JoinPruneList",
        "pim_v4_source_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4SourcesList",
        "source_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4SourcesList",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "group_handles"
        "source_handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['group_pool_handle'] = group_pool_handle
    args['handle'] = handle
    args['interval'] = interval
    args['join_prune_per_interval'] = join_prune_per_interval
    args['mode'] = mode
    args['rate_control'] = rate_control
    args['register_per_interval'] = register_per_interval
    args['register_stop_per_interval'] = register_stop_per_interval
    args['rp_ip_addr'] = rp_ip_addr
    args['session_handle'] = session_handle
    args['wildcard_group'] = wildcard_group
    args['crp_ip_addr'] = crp_ip_addr
    args['group_pool_mode'] = group_pool_mode
    args['source_pool_handle'] = source_pool_handle
    args['group_range_type'] = group_range_type
    args['group_range_type'] = 'sourcetogroup'
    args['default_mdt_mode'] = default_mdt_mode
    args['join_prune_aggregation_factor'] = join_prune_aggregation_factor
    args['register_tx_iteration_gap'] = register_tx_iteration_gap
    args['s_g_rpt_group'] = s_g_rpt_group
    args['send_null_register'] = send_null_register
    args['source_group_mapping'] = source_group_mapping

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_pim_group_config.__doc__, **args)
    args['discard_sg_join_states'] = 0

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    if mode == 'create':
        args['session_handle'] = handle
    if wildcard_group == jNone:
        args['wildcard_group'] = 0
    for hndl in handle:
        args['handle'] = hndl
        if args['wildcard_group']:
            args['group_range_type'] = 'startogroup'
        ret.append(rt_handle.invoke('emulation_pim_group_config', **args))
        if group_pool_mode == 'register':
            args['group_pool_mode'] = 'candidate_rp'
            args['crp_ip_addr'] = rp_ip_addr
            rt_handle.invoke('emulation_pim_group_config', **args)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'pim_v4_source_handle' in ret[index]:
            ret[index]['source_handles'] = ret[index]['pim_v4_source_handle']
            v4_handles.append(ret[index]['pim_v4_source_handle'])
        if 'pim_v4_join_prune_handle' in ret[index]:
            ret[index]['group_handles'] = ret[index]['pim_v4_join_prune_handle']
            v4_handles.append(ret[index]['pim_v4_join_prune_handle'])
        if 'pim_v6_source_handle' in ret[index]:
            ret[index]['source_handles'] = ret[index]['pim_v6_source_handle']
            v6_handles.append(ret[index]['pim_v6_source_handle'])
        if 'pim_v6_join_prune_handle' in ret[index]:
            ret[index]['group_handles'] = ret[index]['pim_v6_join_prune_handle']
            v6_handles.append(ret[index]['pim_v6_join_prune_handle'])
        if 'group_handles' in ret[index]:
            ret[index]['handles'] = ret[index]['group_handles']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_pim_info(rt_handle, handle=jNone,
                         port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle

    Spirent Returns:
    {
        "bsm_rx": "0",
        "bsm_tx": "0",
        "crp_rx": "0",
        "duration": "35.5476400852",
        "group_assert_rx": "0",
        "group_join_rx": "0",
        "group_join_tx": "0",
        "handle": "host1",
        "hello_rx": "1",
        "hello_tx": "2",
        "j_p_pdu_rx": "1",
        "j_p_pdu_tx": "1",
        "reg_rx": "0",
        "reg_stop_rx": "0",
        "router_id": "192.0.0.1",
        "router_state": "NEIGHBOR",
        "s_g_join_rx": "2",
        "s_g_join_tx": "2",
        "status": "1",
        "upstream_neighbor_addr": "3.3.3.2"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/item:1": {
            "session": {
                "bootstrap_rx": "0",
                "bootstrap_tx": "0",
                "group_join_rx": "0",
                "group_join_tx": "0",
                "group_prune_rx": "0",
                "group_prune_tx": "0",
                "hello_rx": "2",
                "hello_tx": "1",
                "normal_crp_adv_msg_rx": "0",
                "normal_crp_adv_msg_tx": "0",
                "null_reg_rx": "0",
                "null_reg_tx": "0",
                "num_neighbors_learnt": "1",
                "port_name": "1/11/2",
                "reg_rx": "0",
                "reg_stop_rx": "0",
                "reg_stop_tx": "0",
                "reg_tx": "0",
                "rp_join_rx": "0",
                "rp_join_tx": "0",
                "rp_prune_rx": "0",
                "rp_prune_tx": "0",
                "s_g_join_rx": "0",
                "s_g_join_tx": "0",
                "s_g_prune_rx": "0",
                "s_g_prune_tx": "0",
                "s_g_rpt_join_rx": "0",
                "s_g_rpt_join_tx": "0",
                "s_g_rpt_prune_rx": "0",
                "s_g_rpt_prune_tx": "0",
                "session_flap": "0",
                "shutdown_crp_adv_msg_rx": "0",
                "shutdown_crp_adv_msg_tx": "0"
            }
        },
        "1/11/2": {
            "aggregate": {
                "bootstrap_rx": "0",
                "bootstrap_tx": "0",
                "group_join_rx": "0",
                "group_join_tx": "0",
                "group_prune_rx": "0",
                "group_prune_tx": "0",
                "hello_rx": "2",
                "hello_tx": "1",
                "normal_crp_adv_msg_rx": "0",
                "normal_crp_adv_msg_tx": "0",
                "null_reg_rx": "0",
                "null_reg_tx": "0",
                "num_neighbors_learnt": "1",
                "num_routers_configured": "1",
                "num_routers_running": "1",
                "port_name": "1/11/2",
                "reg_rx": "0",
                "reg_stop_rx": "0",
                "reg_stop_tx": "0",
                "reg_tx": "0",
                "rp_join_rx": "0",
                "rp_join_tx": "0",
                "rp_prune_rx": "0",
                "rp_prune_tx": "0",
                "s_g_join_rx": "0",
                "s_g_join_tx": "0",
                "s_g_prune_rx": "0",
                "s_g_prune_tx": "0",
                "s_g_rpt_join_rx": "0",
                "s_g_rpt_join_tx": "0",
                "s_g_rpt_prune_rx": "0",
                "s_g_rpt_prune_tx": "0",
                "session_flap": "0",
                "shutdown_crp_adv_msg_rx": "0",
                "shutdown_crp_adv_msg_tx": "0",
                "status": "started"
            }
        },
        "bsm_rx": "0",
        "bsm_tx": "0",
        "crp_rx": "0",
        "group_join_rx": "0",
        "group_join_tx": "0",
        "hello_rx": "2",
        "hello_tx": "1",
        "reg_rx": "0",
        "reg_stop_rx": "0",
        "s_g_join_rx": "0",
        "s_g_join_tx": "0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "bsm_rx"
        "bsm_tx"
        "crp_rx"
        "group_join_rx"
        "group_join_tx"
        "hello_rx"
        "hello_tx"
        "reg_rx"
        "reg_stop_rx"
        "s_g_join_rx"
        "s_g_join_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'aggregate'
        stats.update(rt_handle.invoke('emulation_pim_info', **args))
        args['mode'] = 'stats_per_session'
        stats.update(rt_handle.invoke('emulation_pim_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                if 'bootstrap_rx' in ret[index][key]['aggregate']:
                    ret[index]['bsm_rx'] = ret[index][key]['aggregate']['bootstrap_rx']
                if 'bootstrap_tx' in ret[index][key]['aggregate']:
                    ret[index]['bsm_tx'] = ret[index][key]['aggregate']['bootstrap_tx']
                if 'normal_crp_adv_msg_rx' in ret[index][key]['aggregate']:
                    ret[index]['crp_rx'] = ret[index][key]['aggregate']['normal_crp_adv_msg_rx']
                if 'group_join_rx' in ret[index][key]['aggregate']:
                    ret[index]['group_join_rx'] = ret[index][key]['aggregate']['group_join_rx']
                if 'group_join_tx' in ret[index][key]['aggregate']:
                    ret[index]['group_join_tx'] = ret[index][key]['aggregate']['group_join_tx']
                if 'hello_rx' in ret[index][key]['aggregate']:
                    ret[index]['hello_rx'] = ret[index][key]['aggregate']['hello_rx']
                if 'hello_tx' in ret[index][key]['aggregate']:
                    ret[index]['hello_tx'] = ret[index][key]['aggregate']['hello_tx']
                if 'reg_rx' in ret[index][key]['aggregate']:
                    ret[index]['reg_rx'] = ret[index][key]['aggregate']['reg_rx']
                if 'reg_stop_rx' in ret[index][key]['aggregate']:
                    ret[index]['reg_stop_rx'] = ret[index][key]['aggregate']['reg_stop_rx']
                if 's_g_join_rx' in ret[index][key]['aggregate']:
                    ret[index]['s_g_join_rx'] = ret[index][key]['aggregate']['s_g_join_rx']
                if 's_g_join_tx' in ret[index][key]['aggregate']:
                    ret[index]['s_g_join_tx'] = ret[index][key]['aggregate']['s_g_join_tx']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_rsvp_config(
        rt_handle,
        count=jNone,
        gateway_ip_addr_step=jNone,
        handle=jNone,
        hello_interval=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_length=jNone,
        recovery_time=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        neighbor_intf_ip_addr=jNone,
        mode=jNone,
        bfd_registration=jNone,
        graceful_restart=jNone,
        hello_msgs=jNone,
        max_label_value=jNone,
        min_label_value=jNone,
        refresh_reduction=jNone,
        srefresh_interval=jNone,
        bundle_msg_sending=jNone,
        intf_ip_addr=jNone,
        actual_restart_time=jNone,
        hello_retry_count=jNone,
        graceful_restart_recovery_time=jNone,
        port_handle=jNone,
        gateway_ip_addr=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):

        # ****Arguments added below are supported in Ixia but not in Spirent****
        # ****Uncomment once the support is present in Spirent *****
        #
        # actual_restart_time=jNone,
        # graceful_restart_helper_mode=jNone,
        # vlan=jNone,
        # graceful_restart_start_time=jNone,
        # graceful_restart_up_time=jNone,
        # graceful_restarts_count=jNone,

    """
    :param rt_handle:       RT object
    :param count
    :param gateway_ip_addr_step
    :param handle
    :param hello_interval
    :param intf_ip_addr_step
    :param intf_prefix_length
    :param recovery_time
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <1-4094>
    :param vlan_user_priority - <0-7>
    :param neighbor_intf_ip_addr
    :param mode - <create|active:enable|inactive:disable|modify|delete>
    :param bfd_registration
    :param graceful_restart
    :param hello_msgs
    :param max_label_value
    :param min_label_value
    :param refresh_reduction
    :param srefresh_interval
    :param bundle_msg_sending
    :param intf_ip_addr
    :param actual_restart_time
    :param hello_retry_count
    :param graceful_restart_recovery_time
    :param port_handle
    :param gateway_ip_addr
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <1-4094>
    :param vlan_outer_user_priority - <0-7>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1",
        "rsvp_if_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args = get_arg_value(rt_handle, j_emulation_rsvp_config.__doc__, **args)
    vlan_args = dict()
    args['count'] = count
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['hello_interval'] = hello_interval
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_length'] = intf_prefix_length
    args['recovery_time'] = recovery_time
    args['gateway_ip_addr'] = neighbor_intf_ip_addr
    args['enable_bfd_registration '] = bfd_registration
    args['enable_graceful_restart_restarting_mode'] = graceful_restart
    args['enable_hello_extension'] = hello_msgs
    args['label_space_end'] = max_label_value
    args['label_space_start'] = min_label_value
    args['enable_refresh_reduction'] = refresh_reduction
    args['summary_refresh_interval'] = srefresh_interval
    args['enable_bundle_message_sending'] = bundle_msg_sending
    args['intf_ip_addr'] = intf_ip_addr
    args['actual_restart_time'] = actual_restart_time
    args['hello_timeout_multiplier'] = hello_retry_count
    args['recovery_time'] = graceful_restart_recovery_time
    args['port_handle'] = port_handle
    args['gateway_ip_addr'] = gateway_ip_addr
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_mode'] = vlan_id_mode
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_user_priority'] = vlan_user_priority
    vlan_args['vlan_outer_id'] = vlan_outer_id
    vlan_args['vlan_outer_id_mode'] = vlan_outer_id_mode
    vlan_args['vlan_outer_id_step'] = vlan_outer_id_step
    vlan_args['vlan_outer_user_priority'] = vlan_outer_user_priority


    # ****Arguments added below are supported in Ixia but not in Spirent****
    # ****Uncomment once the support is present in Spirent *****
    #
    # args['actual_restart_time'] = actual_restart_time
    # args['enable_graceful_restart_helper_mode'] = graceful_restart_helper_mode
    # args['vlan'] = vlan
    # args['restart_start_time'] = graceful_restart_start_time
    # args['restart_up_time'] = graceful_restart_up_time
    # args['number_of_restarts'] = graceful_restarts_count

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    if (handle != jNone and mode == 'create'
            and re.match('/topology:\d+/deviceGroup:\d+/ethernet:\d+/isisL3:\d+', handle)):
        ethernetObj = __get_parent_handle(handle, 'ethernet')
        ipv4Objs = invoke_ixnet(rt_handle, 'getList', ethernetObj, 'ipv4')
        handle = ipv4Objs[0].lstrip('::ixNet::OBJ-')
    args['handle'] = handle

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    if mode == 'create':
        if args.get('port_handle'):
            handle = create_deviceGroup(rt_handle, args.pop('port_handle'))
            handle = handle['device_group_handle']
        elif not args.get('handle'):
            raise Exception("Please pass either handle or port_handle to the function call")
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_rsvp_config', **args))
        if vlan_args:
            if mode == "create":
                vlan_config(rt_handle, vlan_args, ret[-1]['rsvp_if_handle'])
            else:
                vlan_config(rt_handle, vlan_args, hndl)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'rsvp_if_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['rsvp_if_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_rsvp_control(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|restart|stop_hellos:stop_hello>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_rsvp_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_rsvp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_rsvp_info(rt_handle, handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle

    Spirent Returns:
    {
        "egress_path_rx": "3",
        "egress_patherr_rx": "0",
        "egress_pathtear_rx": "0",
        "egress_resv_tx": "2",
        "egress_resvconf_rx": "0",
        "egress_resverr_tx": "0",
        "egress_resvtear_tx": "0",
        "hellos_rx": "0",
        "hellos_tx": "0",
        "ingress_path_tx": "2",
        "ingress_patherr_tx": "0",
        "ingress_pathtear_tx": "0",
        "ingress_resv_rx": "3",
        "ingress_resvconf_tx": "0",
        "ingress_resverr_rx": "0",
        "ingress_resvtear_rx": "0",
        "intf_ip_address": "10.10.10.1",
        "lsp_connecting": "0",
        "lsp_count": "1",
        "lsp_created": "1",
        "lsp_deleted": "0",
        "max_setup_time": "0",
        "min_setup_time": "0",
        "msg_rx": "6",
        "msg_tx": "4",
        "neighbor_intf_ip_addr": "10.10.10.2",
        "num_lsps_setup": "1",
        "status": "1"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1": {
            "learned_info": {
                "assigned": {
                    "BandWidth (in bps)": "0",
                    "Current State": "Up",
                    "Device#": "1",
                    "Dut IP": "10.10.10.2",
                    "ERO AS Number": "NA",
                    "ERO IP": "NA",
                    "ERO Prefix Length": "NA",
                    "ERO Type": "NA",
                    "Head End IP": "10.10.10.2",
                    "LSP ID": "1",
                    "Label": "1000",
                    "Last Flap Reason": "None",
                    "Our IP": "10.10.10.1",
                    "Reservation State(for Graceful-Restart)": "None",
                    "Session IP": "10.10.10.1",
                    "Setup Time(ms)": "0",
                    "Tunnel ID": "1",
                    "Up Time(ms)": "39276"
                },
                "p2mp": {
                    "Current State": "Down Down",
                    "Device#": "NA NA",
                    "Dut IP": "NA NA",
                    "Head End IP": "NA NA",
                    "LSP ID": "NA NA",
                    "Label": "NA NA",
                    "Last Flap Reason": "None None",
                    "Leaf IP": "NA NA",
                    "Our IP": "NA NA",
                    "P2MP ID": "NA NA",
                    "P2MP ID as Number": "NA NA",
                    "Reservation State(for Graceful-Restart)": "None None",
                    "Setup Time(ms)": "NA NA",
                    "Sub Group ID": "NA NA",
                    "Sub Group Originator ID": "NA NA",
                    "Tunnel ID": "NA NA",
                    "Up Time(ms)": "NA NA"
                },
                "received": {
                    "BandWidth (in bps)": "0",
                    "Current State": "Up",
                    "Device#": "1",
                    "Dut IP": "10.10.10.2",
                    "ERO AS Number": "NA",
                    "ERO IP": "NA",
                    "ERO Prefix Length": "NA",
                    "ERO Type": "NA",
                    "Head End IP": "10.10.10.1",
                    "LSP ID": "1",
                    "Label": "1000",
                    "Last Flap Reason": "None",
                    "Our IP": "10.10.10.1",
                    "RRO C-Type": "NA",
                    "RRO IP": "NA",
                    "RRO Label": "NA",
                    "RRO Type": "NA",
                    "Reservation State(for Graceful-Restart)": "None",
                    "Session IP": "10.10.10.2",
                    "Setup Time(ms)": "4",
                    "Symbolic Path Name": "RSVP P2P LSP 1",
                    "Tunnel ID": "1",
                    "Up Time(ms)": "39283"
                }
            }
        },
        "1/11/2": {
            "aggregate": {
                "acks_rx": "0",
                "acks_tx": "0",
                "bundle_messages_rx": "0",
                "bundle_messages_tx": "0",
                "down_state_count": "0",
                "egress_lsps_up": "1",
                "egress_out_of_order_messages_rx": "0",
                "egress_sub_lsps_up": "0",
                "hellos_rx": "0",
                "hellos_tx": "0",
                "ingress_lsps_configured": "1",
                "ingress_lsps_up": "1",
                "ingress_out_of_order_messages_rx": "0",
                "ingress_sub_lsps_configured": "0",
                "ingress_sub_lsps_up": "0",
                "nacks_rx": "0",
                "nacks_tx": "0",
                "no_of_path_re_optimizations": "0",
                "own_graceful_restarts": "0",
                "path_errs_rx": "0",
                "path_errs_tx": "0",
                "path_re_evaluation_request_tx": "0",
                "path_sent_state_count": "0",
                "path_tears_rx": "0",
                "path_tears_tx": "0",
                "paths_rx": "2",
                "paths_tx": "2",
                "paths_with_recovery_label_rx": "0",
                "paths_with_recovery_label_tx": "0",
                "peer_graceful_restarts": "0",
                "resv_confs_rx": "0",
                "resv_confs_tx": "0",
                "resv_errs_rx": "0",
                "resv_errs_tx": "0",
                "resv_tears_rx": "0",
                "resv_tears_tx": "0",
                "resvs_rx": "2",
                "resvs_tx": "2",
                "session_flap_count": "0",
                "sessions_down": "0",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "srefreshs_rx": "0",
                "srefreshs_tx": "0",
                "status": "started",
                "unrecovered_resvs_deleted": "0",
                "up_state_count": "1"
            }
        },
        "hellos_rx": "0",
        "hellos_tx": "0",
        "lsp_count": "1",
        "lsp_created": "1",
        "lsp_deleted": "0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "hellos_rx"
        "hellos_tx"
        "lsp_count"
        "lsp_created"
        "lsp_deleted"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'stats'
        stats.update(rt_handle.invoke('emulation_rsvp_info', **args))
        args['mode'] = 'learned_info'
        stats.update(rt_handle.invoke('emulation_rsvp_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                if 'sessions_up' in ret[index][key]['aggregate']:
                    ret[index]['lsp_created'] = ret[index][key]['aggregate']['sessions_up']
                if 'sessions_down' in ret[index][key]['aggregate']:
                    ret[index]['lsp_deleted'] = ret[index][key]['aggregate']['sessions_down']
                if 'hellos_rx' in ret[index][key]['aggregate']:
                    ret[index]['hellos_rx'] = ret[index][key]['aggregate']['hellos_rx']
                if 'hellos_tx' in ret[index][key]['aggregate']:
                    ret[index]['hellos_tx'] = ret[index][key]['aggregate']['hellos_tx']
                if 'sessions_total' in ret[index][key]['aggregate']:
                    ret[index]['lsp_count'] = ret[index][key]['aggregate']['sessions_total']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_rsvp_tunnel_config(
        rt_handle,
        avoid_node_id=jNone,
        count=jNone,
        fast_reroute_bandwidth=jNone,
        fast_reroute_exclude_any=jNone,
        fast_reroute_holding_priority=jNone,
        fast_reroute_include_all=jNone,
        fast_reroute_include_any=jNone,
        fast_reroute_setup_priority=jNone,
        handle=jNone,
        plr_id=jNone,
        send_detour=jNone,
        mode=jNone,
        ingress_dst_ip_addr=jNone,
        ingress_ip_addr=jNone,
        session_attr_bw_protect=jNone,
        fast_reroute=jNone,
        session_attr_ra_exclude_any=jNone,
        facility_backup=jNone,
        session_attr_resource_affinities=jNone,
        fast_reroute_hop_limit=jNone,
        one_to_one_backup=jNone,
        session_attr_hold_priority=jNone,
        session_attr_ra_include_all=jNone,
        session_attr_ra_include_any=jNone,
        session_attr_label_record=jNone,
        session_attr_local_protect=jNone,
        sender_tspec_max_pkt_size=jNone,
        sender_tspec_min_policed_size=jNone,
        session_attr_node_protect=jNone,
        sender_tspec_peak_data_rate=jNone,
        session_attr_se_style=jNone,
        session_attr_setup_priority=jNone,
        sender_tspec_token_bkt_size=jNone,
        sender_tspec_token_bkt_rate=jNone,
        ero=jNone,
        rsvp_behavior=jNone,
        ingress_dst_ip_addr_step=jNone,
        lsp_id_count=jNone,
        tunnel_id_start=jNone,
        tunnel_id_step=jNone,
        tunnel_count=jNone,
        egress_ip_addr=jNone,
        ero_list_ipv4=jNone,
        ero_list_pfxlen=jNone,
        ero_list_loose=jNone):
        # reservation_style=jNone,
        # enable_send_as_rro=jNone,
        # rro=jNone,
    """
    :param rt_handle:       RT object
    :param avoid_node_id
    :param count
    :param fast_reroute_bandwidth
    :param fast_reroute_exclude_any
    :param fast_reroute_holding_priority
    :param fast_reroute_include_all
    :param fast_reroute_include_any
    :param fast_reroute_setup_priority
    :param handle
    :param plr_id
    :param send_detour
    :param mode - <create|modify|delete>
    :param ingress_dst_ip_addr
    :param ingress_ip_addr
    :param session_attr_bw_protect
    :param fast_reroute
    :param session_attr_ra_exclude_any
    :param facility_backup
    :param session_attr_resource_affinities
    :param fast_reroute_hop_limit
    :param one_to_one_backup
    :param session_attr_hold_priority
    :param session_attr_ra_include_all
    :param session_attr_ra_include_any
    :param session_attr_label_record
    :param session_attr_local_protect
    :param sender_tspec_max_pkt_size
    :param sender_tspec_min_policed_size
    :param session_attr_node_protect
    :param sender_tspec_peak_data_rate
    :param session_attr_se_style
    :param session_attr_setup_priority
    :param sender_tspec_token_bkt_size
    :param sender_tspec_token_bkt_rate
    :param ero
    :param rsvp_behavior
    :param ingress_dst_ip_addr_step
    :param lsp_id_count
    :param tunnel_id_start
    :param tunnel_id_step
    :param tunnel_count
    :param egress_ip_addr
    :param ero_list_ipv4
    :param ero_list_pfxlen
    :param ero_list_loose
    #reservation_style
    #enable_send_as_rro
    #rro

    Spirent Returns:
    {
        "egress_handles": [
            "host1"
        ],
        "handles": "rsvpingresstunnelparams1",
        "ingress_handles": [
            "host1"
        ],
        "status": "1",
        "tunnel_handle": "rsvpingresstunnelparams1"
    }


    IXIA Returns:
    {
        "egress_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2/rsvpP2PEgressLsps",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2",
        "ingress_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2/rsvpP2PIngressLsps",
        "rsvpte_lsp_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2",
        "rsvpte_p2p_egress_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2/rsvpP2PEgressLsps",
        "rsvpte_p2p_ingress_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2/rsvpP2PIngressLsps",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "egress_handles"
        "handles"
        "ingress_handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args = get_arg_value(rt_handle, j_emulation_rsvp_tunnel_config.__doc__, **args)
    args['avoid_node_id'] = avoid_node_id
    args['count'] = count
    args['fast_reroute_bandwidth'] = fast_reroute_bandwidth
    args['fast_reroute_exclude_any'] = fast_reroute_exclude_any
    args['fast_reroute_holding_priority'] = fast_reroute_holding_priority
    args['fast_reroute_include_all'] = fast_reroute_include_all
    args['fast_reroute_include_any'] = fast_reroute_include_any
    args['fast_reroute_setup_priority'] = fast_reroute_setup_priority
    args['handle'] = handle
    args['plr_id'] = plr_id
    args['send_detour'] = send_detour
    args['remote_ip'] = ingress_dst_ip_addr
    args['enable_fast_reroute'] = fast_reroute
    args['one_to_one_backup_desired'] = one_to_one_backup
    args['facility_backup_desired'] = facility_backup
    args['holding_priority'] = session_attr_hold_priority
    args['label_recording_desired'] = session_attr_label_record
    args['local_protection_desired'] = session_attr_local_protect
    args['hop_limit'] = fast_reroute_hop_limit
    args['include_all'] = session_attr_ra_include_all
    args['include_any'] = session_attr_ra_include_any
    args['maximum_packet_size'] = sender_tspec_max_pkt_size
    args['minimum_policed_unit'] = sender_tspec_min_policed_size
    args['bandwidth_protection_desired'] = session_attr_bw_protect
    args['resource_affinities'] = session_attr_resource_affinities
    args['exclude_any'] = session_attr_ra_exclude_any
    args['node_protection_desired'] = session_attr_node_protect
    args['peak_data_rate'] = sender_tspec_peak_data_rate
    args['se_style_desired'] = session_attr_se_style
    args['setup_priority'] = session_attr_setup_priority
    args['token_bucket_rate'] = sender_tspec_token_bkt_rate
    args['token_bucket_size'] = sender_tspec_token_bkt_size
    args['enable_ero'] = ero
    args['p2p_ingress_lsps_count'] = lsp_id_count
    args['p2mp_egress_tunnel_count'] = tunnel_count
    args['egress_ip'] = egress_ip_addr

    # ***** Arguments supported in Ixia not in Spirent *****

    #args['send_rro'] = enable_send_as_rro
    #args['reservation_style'] = reservation_style

    # ***** Argument Modification *****

    if session_attr_hold_priority != jNone:
        if int(args['holding_priority']) > 7:
            rt_handle.log(level="info", message="Range in Spirent <0-7> value defined is not in range.Hence setting its value to default value")
            args['holding_priority'] = str(7)
    if session_attr_setup_priority != jNone:
        if int(args['setup_priority']) > 7:
            rt_handle.log(level="info", message="Range in Spirent <0-7> value defined is not in range.Hence setting its value to default value")
            args['setup_priority'] = '7'

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if 'rsvpteIf' in hndl:
            hndl = __get_parent_handle(hndl, 'ipv4')
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_rsvp_tunnel_config', **args))

    vargs = dict()
    if mode == 'create':
        vargs['mode'] = 'modify'
        handle = ret[0]['rsvpte_lsp_handle']
        if ingress_dst_ip_addr != jNone:
            if ingress_dst_ip_addr_step != jNone:
                nargs = dict()
                nargs['pattern'] = 'counter'
                nargs['counter_start'] = ingress_dst_ip_addr
                nargs['counter_step'] = ingress_dst_ip_addr_step
                nargs['counter_direction'] = 'increment'
                _result_ = rt_handle.invoke('multivalue_config', **nargs)
                vargs['remote_ip'] = _result_['multivalue_handle']
            else:
                vargs['remote_ip'] = ingress_dst_ip_addr
            vargs['handle'] = '%s/%s' %(handle, 'rsvpP2PIngressLsps')
            rt_handle.invoke('emulation_rsvp_tunnel_config', **vargs)
        if tunnel_id_start != jNone:
            if tunnel_id_step != jNone:
                nargs = dict()
                nargs['pattern'] = 'counter'
                nargs['counter_start'] = tunnel_id_start
                nargs['counter_step'] = tunnel_id_step
                nargs['counter_direction'] = 'increment'
                _result_ = rt_handle.invoke('multivalue_config', **nargs)
                vargs['tunnel_id'] = _result_['multivalue_handle']
            else:
                vargs['tunnel_id'] = tunnel_id_start
            vargs['handle'] = '%s/%s' %(handle, 'rsvpP2PIngressLsps')
            rt_handle.invoke('emulation_rsvp_tunnel_config', **vargs)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'rsvpte_lsp_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['rsvpte_lsp_handle']
            ret[index]['ingress_handles'] = '%s/%s' %(ret[index]['handles'], 'rsvpP2PIngressLsps')
            ret[index]['egress_handles'] = '%s/%s' %(ret[index]['handles'], 'rsvpP2PEgressLsps')
            v4_handles.append(ret[-1]['handles'])
        if 'rsvpte_p2p_ingress_handle' in ret[index]:
            ret[index]['ingress_handles'] = ret[index]['rsvpte_p2p_ingress_handle']
            v4_handles.append(ret[-1]['ingress_handles'])
        if 'rsvpte_p2p_egress_handle'  in ret[index]:
            ret[index]['egress_handles'] = ret[index]['rsvpte_p2p_egress_handle']
            v4_handles.append(ret[-1]['egress_handles'])

        if ero_list_ipv4 != jNone or ero_list_pfxlen != jNone or ero_list_loose != jNone:
            configure_ero(rt_handle, ret[index]['ingress_handles'], ero_list_ipv4, ero_list_pfxlen, ero_list_loose)

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_rsvpte_tunnel_control(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode
    args = get_arg_value(rt_handle, j_emulation_rsvpte_tunnel_control.__doc__, **args)

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_rsvpte_tunnel_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_interface_config(
        rt_handle,
        arp_send_req=jNone,
        autonegotiation=jNone,
        clocksource=jNone,
        framing=jNone,
        gateway=jNone,
        gateway_step=jNone,
        internal_ppm_adjust=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        ipv6_gateway_step=jNone,
        ipv6_intf_addr=jNone,
        ipv6_intf_addr_step=jNone,
        ipv6_prefix_length=jNone,
        qinq_incr_mode=jNone,
        vlan=jNone,
        vlan_id=jNone,
        vlan_tpid=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        speed=jNone,
        intf_prefix_len=jNone,
        src_mac_addr=jNone,
        port_handle=jNone,
        mode=jNone,
        handle=jNone,
        ipv6_gateway=jNone,
        topology_name=jNone,
        device_group_name=jNone,
        src_mac_addr_step=jNone,
        phy_mode=jNone,
        mtu=jNone,
        intf_mode=jNone,
        duplex=jNone,
        arp_req_retries=jNone,
        intf_count=jNone,
        vlan_id_repeat_count=jNone,
        arp_on_linkup=jNone,
        transmit_mode=jNone,
        flow_control=jNone,
        type_a_ordered_sets=jNone,
        fault_type=jNone,
        block_mode=jNone,
        resolve_gateway_mac=jNone,
        gateway_mac=jNone,
        priority0=jNone,
        priority1=jNone,
        priority2=jNone,
        priority3=jNone,
        priority4=jNone,
        priority5=jNone,
        priority6=jNone,
        priority7=jNone,
        gre_count=jNone,
        gre_dst_ip_addr=jNone,
        gre_dst_ip_addr_step=jNone,
        gre_checksum_enable=jNone,
        gre_key_in=jNone,
        gre_key_out=jNone,
        gre_seq_enable=jNone):

        # ****Arguments added below are supported in Ixia but not in Spirent****
        # ****Uncomment once the support is present in Spirent *****
        #
        # vlan_user_priority_step=jNone
        # single_arp_per_gateway=jNone
        # data_integrity=jNone
        # ns_on_linkup=jNone
        # l23_config_type=jNone
        # data_integrity=jNone
        # tx_gap_control_mode=jNone
        # check_opposite_ip_version=jNone
        # single_ns_per_gateway=jNone
        # send_router_solicitation=jNone
        # router_solicitation_retries=jNone
        # interface_handle=jNone
        # no_write=jNone
        # static_vlan_enable=jNone

    """
    :param rt_handle:       RT object
    :param arp_send_req - <1|0>
    :param autonegotiation - <1|0>
    :param clocksource - <internal|loop|external>
    :param framing - <sonet|sdh>
    :param gateway
    :param gateway_step
    :param internal_ppm_adjust - <-100-100>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param ipv6_gateway_step
    :param ipv6_intf_addr
    :param ipv6_intf_addr_step
    :param ipv6_prefix_length - <0-128>
    :param qinq_incr_mode - <both|inner|outer>
    :param vlan
    :param vlan_id
    :param vlan_tpid
    :param vlan_id_step
    :param vlan_user_priority
    :param speed
    :param intf_prefix_len - <1-32>
    :param src_mac_addr
    :param port_handle
    :param mode - <config|modify|destroy>
    :param handle
    :param ipv6_gateway
    :param topology_name
    :param device_group_name
    :param src_mac_addr_step
    :param phy_mode - <copper|fiber>
    :param mtu - <68-9216>
    :param intf_mode - <ethernet|pos_hdlc|pos_ppp|atm|fc>
    :param duplex - <full|half>
    :param arp_req_retries - <0-100>
    :param intf_count
    :param vlan_id_repeat_count
    :param arp_on_linkup - <true:1|false:0>
    :param transmit_mode - <RATE_BASED:advanced|PORT_BASED:stream>
    :param flow_control - <true:1|flase:0>
    :param type_a_ordered_sets - <REMOTE:remote_fault|LOCAL:local_fault|RESET>
    :param fault_type - <CONTINUOUS>
    :param block_mode
    :param resolve_gateway_mac - <true:1|false:0>
    :param gateway_mac
    :param priority0 - <0|1>
    :param priority1 - <0|1>
    :param priority2 - <0|1>
    :param priority3 - <0|1>
    :param priority4 - <0|1>
    :param priority5 - <0|1>
    :param priority6 - <0|1>
    :param priority7 - <0|1>
    :param gre_count
    :param gre_dst_ip_addr
    :param gre_dst_ip_addr_step
    :param gre_checksum_enable
    :param gre_key_in
    :param gre_key_out
    :param gre_seq_enable


    Spirent Returns:
    {
        "handle": "host1",
        "handles": {
            "ipv4": "host1",
            "ipv6": "host2"
        },
        "ipv4_handle": "host1",
        "ipv6_handle": "host2",
        "status": "1"
    }

    IXIA Returns:
    {
        "ethernet_handle": "/topology:1/deviceGroup:1/ethernet:1",
        "handles": {
            "ipv4": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1",
            "ipv6": "/topology:1/deviceGroup:2/ethernet:1/ipv6:1"
        },
        "interface_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:1 /topology:1/deviceGroup:1/ethernet:1/item:1",
        "ipv4_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1",
        "ipv6_handle": "/topology:1/deviceGroup:2/ethernet:1/ipv6:1",
        "status": "1"
    }

    Common Return Keys:
        "handles"
        "ipv4_handle"
        "ipv6_handle"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    faultArgs = dict()
    vargs = dict()
    pfcargs = dict()
    args['arp_send_req'] = arp_send_req
    args['autonegotiation'] = autonegotiation
    args['clocksource'] = clocksource
    args['framing'] = framing
    args['gateway'] = gateway
    args['gateway_step'] = gateway_step
    args['internal_ppm_adjust'] = internal_ppm_adjust
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['ipv6_gateway_step'] = ipv6_gateway_step
    args['ipv6_intf_addr'] = ipv6_intf_addr
    args['ipv6_intf_addr_step'] = ipv6_intf_addr_step
    args['ipv6_prefix_length'] = ipv6_prefix_length
    args['qinq_incr_mode'] = qinq_incr_mode
    args['vlan'] = vlan
    args['speed'] = speed
    args['intf_prefix_len'] = intf_prefix_len
    args['src_mac_addr'] = src_mac_addr
    args['src_mac_addr_step'] = src_mac_addr_step
    args['mode'] = mode
    args['ipv6_gateway'] = ipv6_gateway
    args['phy_mode'] = phy_mode
    args['mtu'] = mtu
    args['intf_mode'] = intf_mode
    args['duplex'] = duplex
    args['arp_req_retries'] = arp_req_retries
    if vlan_id_repeat_count is not jNone:
        vargs['vlan_id'] = vlan_id
        vargs['vlan_id_step'] = vlan_id_step
        vargs['vlan_user_priority'] = vlan_user_priority
        vargs['vlan_id_repeat_count'] = vlan_id_repeat_count
        vargs['intf_count'] = intf_count
        vargs['vlan_tpid'] = vlan_tpid
    else:
        args['vlan_id'] = vlan_id
        args['vlan_id_step'] = vlan_id_step
        args['vlan_user_priority'] = vlan_user_priority
        args['intf_count'] = intf_count
        args['vlan_tpid'] = vlan_tpid
    args['arp_on_linkup'] = arp_on_linkup
    args['transmit_mode'] = transmit_mode
    args['flow_control'] = flow_control
    args['resolve_gateway_mac'] = resolve_gateway_mac
    args['gateway_mac'] = gateway_mac
    args['auto_detect_instrumentation_type'] = 'end_of_frame'
    args['gre_count'] = gre_count
    args['gre_dst_ip_addr'] = gre_dst_ip_addr
    args['gre_dst_ip_addr_step'] = gre_dst_ip_addr_step
    args['gre_checksum_enable'] = gre_checksum_enable
    args['gre_key_in'] = gre_key_in
    args['gre_key_out'] = gre_key_out
    args['gre_seq_enable'] = gre_seq_enable

    faultArgs['type_a_ordered_sets'] = type_a_ordered_sets
    faultArgs['fault_type'] = fault_type
    pfcargs['priority0'] = priority0
    pfcargs['priority1'] = priority1
    pfcargs['priority2'] = priority2
    pfcargs['priority3'] = priority3
    pfcargs['priority4'] = priority4
    pfcargs['priority5'] = priority5
    pfcargs['priority6'] = priority6
    pfcargs['priority7'] = priority7

    # ***** Arguments supported in Ixia not in Spirent *****
    #args['vlan_user_priority_step'] = vlan_user_priority_step
    #args['vlan_tpid'] = vlan_tpid
    #args['single_arp_per_gateway'] = single_arp_per_gateway
    #args['data_integrity'] = data_integrity
    #args['ns_on_linkup'] = ns_on_linkup
    #args['l23_config_type'] = l23_config_type
    #args['data_integrity'] = data_integrity
    #args['tx_gap_control_mode'] = tx_gap_control_mode
    #args['check_opposite_ip_version'] = check_opposite_ip_version
    #args['single_ns_per_gateway'] = single_ns_per_gateway
    #args['send_router_solicitation'] = send_router_solicitation
    #args['router_solicitation_retries'] = router_solicitation_retries
    #args['interface_handle'] = interface_handle
    #args['no_write'] = no_write
    #args['static_vlan_enable'] = static_vlan_enable

    # ***** End of Argument *****

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_interface_config.__doc__, **args)
    vargs = get_arg_value(rt_handle, j_interface_config.__doc__, **vargs)
    faultArgs = get_arg_value(rt_handle, j_interface_config.__doc__, **faultArgs)
    pfcargs = get_arg_value(rt_handle, j_interface_config.__doc__, **pfcargs)

    if args.get('intf_prefix_len'):
        args['netmask'] = cidr_to_netmask(args.pop('intf_prefix_len'))

    if args.get('gre_key_in') or args.get('gre_key_out'):
            args['gre_key_enable'] = 1

    if args.get('gateway_mac'):
        args['ipv4_manual_gateway_mac' if args.get('intf_ip_addr') else 'ipv6_manual_gateway_mac'] = args.pop('gateway_mac')
        args['ipv4_resolve_gateway' if args.get('intf_ip_addr') else 'ipv6_resolve_gateway'] = 0

    if args.get('resolve_gateway_mac'):
        args['ipv4_resolve_gateway'] = args.pop('resolve_gateway_mac')

    if args.get('transmit_mode'):
        transmit_mode = args.pop('transmit_mode')
        if transmit_mode.lower().strip() in ['port_based', 'stream']:
            args['transmit_mode'] = 'stream'
        elif transmit_mode.lower().strip() in ['rate_based', 'advanced']:
            args['transmit_mode'] = 'advanced'
        elif transmit_mode.lower().strip() in ['priority_based', 'manual_based']:
            raise Exception("Ixia does not support priority_based and manual_based modes for transmit_mode")
        else:
            args['transmit_mode'] = transmit_mode

    if args.get('flow_control'):
        flow_control = args.pop('flow_control')
        if flow_control.lower() == 'true':
            args['enable_flow_control'] = 1
        elif flow_control.lower() == 'false':
            args['enable_flow_control'] = 0

    if faultArgs.get('type_a_ordered_sets'):
        if faultArgs.get('type_a_ordered_sets') in ['RESET', 'reset']:
            faultArgs['start_error_insertion'] = 0
            faultArgs.pop('type_a_ordered_sets')
        faultArgs['send_sets_mode'] = 'type_a_only'

    if faultArgs.get('fault_type'):
        fault_type = faultArgs.pop('fault_type')
        if fault_type.lower() == 'continuous':
            faultArgs['loop_continuously'] = 1
        else:
            raise Exception("Error: {0} fault type is not supported".format(fault_type))

    if vargs.get('intf_count'):
        vargs['connected_count'] = vargs.pop('intf_count')

    if args.get('intf_count'):
        args['connected_count'] = args.pop('intf_count')

    if len(pfcargs.keys()) > 0:
        create_pfc_dict(rt_handle, pfcargs, handle, port_handle)

    ret = []
    __check_and_raise(mode)
    handles = ""
    index = 0

    if mode == 'config':
        __check_and_raise(port_handle)
        create_topology(rt_handle, port_handle, topology_name)
        _result_ = create_deviceGroup(rt_handle, port_handle, intf_count, device_group_name)
        args['port_handle'] = port_handle
        if faultArgs:
            faultArgs['port_handle'] = args['port_handle']
            rt_handle.invoke('interface_config', **faultArgs)
        args['protocol_handle'] = _result_['device_group_handle']
        if vlan is not jNone and vlan_id_repeat_count is jNone:
            if isinstance(vlan_id, list):
                args = __interface_config_vlan(rt_handle, args)
        ret.append(rt_handle.invoke('interface_config', **args))
        if vlan is not jNone and vlan_id_repeat_count is not jNone:
            __interface_config_vlan(rt_handle, vargs, ret[0]['ethernet_handle'])
    elif mode == 'modify':
        __check_and_raise(handle)
        if not isinstance(handle, list) and isinstance(handle, str):
            handle = [handle]
        if isinstance(handle, (dict, tuple)):
            raise Exception('handle type shall be ether list or string')
        if topology_name != jNone:
            nargs = dict()
            nargs['mode'] = mode
            nargs['topology_name'] = topology_name
            nargs['topology_handle'] = __get_parent_handle(handle[0], 'topology')
            rt_handle.invoke('topology_config', **nargs)
        for hndl in handle:
            if not isinstance(handle_map[hndl], list):
                args['protocol_handle'] = hndl
            else:
                args['protocol_handle'] = hndl
            if faultArgs:
                faultArgs['port_handle'] = get_ixia_port_handle(rt_handle, hndl)
                rt_handle.invoke('interface_config', **faultArgs)
            if device_group_name != jNone or intf_count != jNone:
                nargs = dict()
                deviceGroup = __get_parent_handle(hndl, 'deviceGroup')
                if device_group_name != jNone:
                    nargs['device_group_name'] = device_group_name
                if intf_count != jNone:
                    nargs['device_group_multiplier'] = intf_count
                nargs['device_group_handle'] = deviceGroup
                nargs['mode'] = mode
                _result_ = rt_handle.invoke('topology_config', **nargs)
                # args['protocol_handle'] = deviceGroup
            if vlan is not jNone and vlan_id_repeat_count is jNone:
                if isinstance(vlan_id, list):
                    args = __interface_config_vlan(rt_handle, args)
            ret.append(rt_handle.invoke('interface_config', **args))
            if vlan is not jNone and vlan_id_repeat_count is not jNone:
                __interface_config_vlan(rt_handle, vargs, hndl)
            port = get_ixia_port_handle(rt_handle, hndl)
            ###### Configure PFC ##########################
            if pfcargs:
                configure_pfc(rt_handle, port, mode='modify')

        rt_handle.invoke('test_control', action='apply_on_the_fly_changes')
    else:
        __check_and_raise(port_handle)
        args['port_handle'] = port_handle
        ret.append(rt_handle.invoke('interface_config', **args))
    if (arp_on_linkup is not jNone) and (mode == 'config' or mode == 'modify'):
        arp_args = dict()
        arp_args['protocol_handle'] = '/globals'
        #logic to map [T|t]rue, [F|f]alse, '1', 1, '0', 0 if not matched will default to 1
        arp_on_linkup = str(arp_on_linkup)
        if true.match(arp_on_linkup) or arp_on_linkup == '1':
            arp_on_linkup = 1
        elif false.match(arp_on_linkup) or arp_on_linkup == '0':
            arp_on_linkup = 0
        else:
            arp_on_linkup = 1
        arp_args['arp_on_linkup'] = arp_on_linkup
        rt_handle.invoke('interface_config', **arp_args)
    # ***** Return Value Modification *****

    intfv4_handles, intfv6_handles = list(), list()
    if 'ipv4_handle' in ret[index]:
        pattern = ret[index]['ipv4_handle']+r"/item:\d+"
        intfv4_handles = re.findall(pattern, ret[index]['interface_handle'])
    if 'ipv6_handle' in ret[index]:
        pattern = ret[index]['ipv6_handle']+r"/item:\d+"
        intfv6_handles = re.findall(pattern, ret[index]['interface_handle'])

    if 'greoipv4_handle' in ret[index]:
            ret[index]['gre_handle'] = ret[index]['greoipv4_handle']

    if 'ipv4_handle' in ret[index] and 'ipv6_handle' in ret[index]:
        ret[index]['handles'] = dict()
        ret[index]['handles']['ipv4'] = ret[index]['ipv4_handle']
        ret[index]['handles']['ipv6'] = ret[index]['ipv6_handle']
        v4_handles.append(ret[index]['ipv4_handle'])
        v6_handles.append(ret[index]['ipv6_handle'])
        ret[index]['intf_handles'] = {'ipv4': intfv4_handles, 'ipv6': intfv6_handles}
    elif 'ipv4_handle' in ret[index]:
        ret[index]['handles'] = ret[index]['ipv4_handle']
        v4_handles.append(ret[index]['ipv4_handle'])
        ret[index]['intf_handles'] = intfv4_handles
    elif 'ipv6_handle' in ret[index]:
        ret[index]['handles'] = ret[index]['ipv6_handle']
        v6_handles.append(ret[index]['ipv6_handle'])
        ret[index]['intf_handles'] = intfv6_handles
    elif 'ethernet_handle' in ret[index]:
        ret[index]['handles'] = ret[index]['ethernet_handle']

    if  block_mode in [1, '1']:
        if ret[index].get('intf_handles'):
            ret[index].pop('intf_handles')

    if mode == 'config':
        if isinstance(ret[index]['handles'], dict):
            if 'ipv4' in ret[index]['handles']:
                handle_map[ret[index]['handles']['ipv4']] = port_handle
                handle_map[port_handle].append(ret[index]["ipv4_handle"])
            if 'ipv6' in ret[index]['handles']:
                handle_map[ret[index]['handles']['ipv6']] = port_handle
                handle_map[port_handle].append(ret[index]["ipv6_handle"])
        else:
            handle_map[port_handle].append(ret[index]['handles'])
            handle_map[ret[index]['handles']] = port_handle

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ipv6_autoconfig(
        rt_handle,
        handle=jNone,
        port_handle=jNone,
        mode=jNone,
        ip_version=jNone,
        encap=jNone,
        count=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        local_ip_addr=jNone,
        local_ip_addr_step=jNone,
        local_ip_prefix_len=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        router_solicit_retry=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_id_repeat_count=jNone,
        vlan_priority=jNone,
        dad_enable=jNone):

    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle
    :param mode - <create:config|modify|reset:destroy>
    :param ip_version - <6|4_6>
    :param encap - <ethernet_ii|ethernet_vlan|ethernet_ii_vlan>
    :param count - <1-65536>
    :param mac_addr
    :param mac_addr_step
    :param local_ip_addr
    :param local_ip_addr_step
    :param local_ip_prefix_len - <0-32>
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param router_solicit_retry - <1-100>
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4094>
    :param vlan_id_repeat_count
    :param vlan_priority - <0-7>
    :param dad_enable
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    args = dict()
    vargs = dict()
    ip_args = dict()
    args['mode'] = mode
    args['port_handle'] = port_handle
    args['mac_addr'] = mac_addr
    args['mac_addr_step'] = mac_addr_step
    args['router_solicit_retry'] = router_solicit_retry
    args['encap'] = encap
    args['ip_version'] = ip_version
    args['count'] = count
    vargs['vlan_id'] = vlan_id
    vargs['vlan_id_mode'] = vlan_id_mode
    vargs['vlan_priority'] = vlan_priority
    vargs['vlan_id_step'] = vlan_id_step
    ip_args['local_ip_addr'] = local_ip_addr
    ip_args['local_ip_addr_step'] = local_ip_addr_step
    ip_args['local_ip_prefix_len'] = local_ip_prefix_len
    ip_args['gateway_ip_addr'] = gateway_ip_addr
    ip_args['gateway_ip_addr_step'] = gateway_ip_addr_step


    args = get_arg_value(rt_handle, j_emulation_ipv6_autoconfig.__doc__, **args)
    vargs = get_arg_value(rt_handle, j_emulation_ipv6_autoconfig.__doc__, **vargs)
    ip_args = get_arg_value(rt_handle, j_emulation_ipv6_autoconfig.__doc__, **ip_args)

    vlan = jNone
    vlan_args = [vlan_id, vlan_id_mode, vlan_priority, vlan_id_step, vlan_id_repeat_count]
    ipv4_list = [local_ip_addr, local_ip_addr_step, local_ip_prefix_len, gateway_ip_addr, gateway_ip_addr_step]

    if mode == 'create':
        args['mode'] = mode = 'config'
        args['ipv6_addr_mode'] = 'autoconfig'

    if args.get('encap'):
        args.pop('encap')
        if encap == 'ethernet_ii':
            vlan = args['vlan'] = 0
            for vlan_arg in vlan_args:
                if vlan_arg != jNone:
                    raise Exception("Error: Please pass encap as ethernet_vlan for VLAN related configuration")
        elif encap == 'ethernet_vlan' or encap == 'ethernet_ii_vlan':
            vlan = args['vlan'] = 1

    if args.get('router_solicit_retry'):
        args['router_solicitation_retries'] = args.pop('router_solicit_retry')

    if args.get('mac_addr'):
        args['src_mac_addr'] = args.pop('mac_addr')

    if args.get('mac_addr_step'):
        args['src_mac_addr_step'] = args.pop('mac_addr_step')

    if args.get('ip_version'):
        args.pop('ip_version')
        if ip_version in [6, '6']:
            for ipv4_arg in ipv4_list:
                if ipv4_arg != jNone:
                    raise Exception("Please set argument ip_version as 4_6 to configure v4 attributes")

        if ip_version == "4_6" or mode == 'modify':
            ip_dict = {'local_ip_addr': 'intf_ip_addr', 'local_ip_addr_step': 'intf_ip_addr_step',\
                    'local_ip_prefix_len': 'netmask', 'gateway_ip_addr': 'gateway',\
                    'gateway_ip_addr_step': 'gateway_step'}
            for each_arg in list(ip_dict.keys()):
                if ip_args.get(each_arg):
                    args[ip_dict[each_arg]] = ip_args.pop(each_arg)

    if vlan_id_repeat_count is not jNone:
        vargs['vlan_id_repeat_count'] = vlan_id_repeat_count
        if vargs.get('vlan_priority'):
            vargs['vlan_user_priority'] = vargs.pop('vlan_priority')
        if args.get('count'):
            vargs['connected_count'] = args.pop('count')
    else:
        if vargs.get('vlan_priority'):
            args['vlan_user_priority'] = vargs.pop('vlan_priority')
        if args.get('count'):
            args['connected_count'] = args.pop('count')

    # ***** End of Argument *****

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    if 'netmask' in args:
        args['netmask'] = cidr_to_netmask(args['netmask'])

    ret = []
    __check_and_raise(mode)
    handles = ""
    index = 0

    if mode == 'config':
        __check_and_raise(port_handle)
        _result_ = create_deviceGroup(rt_handle, port_handle, count)
        args['port_handle'] = port_handle
        args['protocol_handle'] = _result_['device_group_handle']
        if vlan is not jNone and vlan_id_repeat_count is jNone:
            if isinstance(vlan_id, list):
                args = __interface_config_vlan(rt_handle, args)
        ret.append(rt_handle.invoke('interface_config', **args))
        if vlan is not jNone and vlan_id_repeat_count is not jNone:
            __interface_config_vlan(rt_handle, vargs, ret[0]['ethernet_handle'])
    elif mode == 'modify':
        __check_and_raise(handle)
        if not isinstance(handle, list) and isinstance(handle, str):
            handle = [handle]
        if isinstance(handle, (dict, tuple)):
            raise Exception('handle type shall be ether list or string')
        for hndl in handle:
            args['protocol_handle'] = hndl
            if count != jNone:
                nargs = dict()
                deviceGroup = __get_parent_handle(hndl, 'deviceGroup')
                if count != jNone:
                    nargs['device_group_multiplier'] = count
                nargs['device_group_handle'] = deviceGroup
                nargs['mode'] = mode
                _result_ = rt_handle.invoke('topology_config', **nargs)
            if vlan is not jNone and vlan_id_repeat_count is jNone:
                if isinstance(vlan_id, list):
                    args = __interface_config_vlan(rt_handle, args)
            ret.append(rt_handle.invoke('interface_config', **args))
            if vlan is not jNone and vlan_id_repeat_count is not jNone:
                __interface_config_vlan(rt_handle, vargs, hndl)
    else:
        __check_and_raise(handle)
        if not isinstance(handle, list):
            handle = [handle]
        for hndl in handle:
            args['port_handle'] = get_ixia_port_handle(rt_handle, hndl)
            ret.append(rt_handle.invoke('interface_config', **args))

    if dad_enable != jNone:
        check_port = get_ixia_port_handle(rt_handle, handle) if handle != jNone else port_handle
        global_protocol_settings(rt_handle, check_port, '-dadEnabled', dad_enable)

    # ***** Return Value Modification *****

    intfv4_handles, ipv6_autoconfig_handles = list(), list()
    if 'ipv4_handle' in ret[index]:
        pattern = ret[index]['ipv4_handle']+r"/item:\d+"
        intfv4_handles = re.findall(pattern, ret[index]['interface_handle'])
    if 'ipv6autoconfiguration_handle' in ret[index]:
        pattern = ret[index]['ipv6autoconfiguration_handle']+r"/item:\d+"
        ipv6_autoconfig_handles = re.findall(pattern, ret[index]['interface_handle'])
    if 'ipv4_handle' in ret[index] and 'ipv6autoconfiguration_handle' in ret[index]:
        ret[index]['handles'] = dict()
        ret[index]['handles']['ipv4'] = ret[index]['ipv4_handle']
        ret[index]['handles']['ipv6'] = ret[index]['ipv6autoconfiguration_handle']
        v4_handles.append(ret[index]['ipv4_handle'])
        v6_handles.append(ret[index]['ipv6autoconfiguration_handle'])
        ret[index]['intf_handles'] = {'ipv4': intfv4_handles, 'ipv6': ipv6_autoconfig_handles}
    elif 'ipv4_handle' in ret[index]:
        ret[index]['handles'] = ret[index]['ipv4_handle']
        v4_handles.append(ret[index]['ipv4_handle'])
        ret[index]['intf_handles'] = intfv4_handles
    elif 'ipv6autoconfiguration_handle' in ret[index]:
        ret[index]['handles'] = ret[index]['ipv6autoconfiguration_handle']
        ret[index]['intf_handles'] = ipv6_autoconfig_handles
    elif 'ethernet_handle' in ret[index]:
        ret[index]['handles'] = ret[index]['ethernet_handle']
    if mode == 'config':
        if isinstance(ret[index]['handles'], dict):
            if 'ipv4' in ret[index]['handles']:
                handle_map[ret[index]['handles']['ipv4']] = port_handle
                handle_map[port_handle].append(ret[index]["ipv4_handle"])
            if 'ipv6' in ret[index]['handles']:
                handle_map[ret[index]['handles']['ipv6']] = port_handle
                handle_map[port_handle].append(ret[index]["ipv6autoconfiguration_handle"])
        else:
            handle_map[port_handle].append(ret[index]['handles'])
            handle_map[ret[index]['handles']] = port_handle

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****
    return ret

def j_emulation_ipv6_autoconfig_control(
        rt_handle,
        handle=jNone,
        port_handle=jNone,
        action=jNone):

    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle
    :param action - <start|stop>
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    args = dict()
    __check_and_raise(action)
    args['port_handle'] = port_handle
    args['handle'] = handle
    args['action'] = action

    args = get_arg_value(rt_handle, j_emulation_ipv6_autoconfig_control.__doc__, **args)
    if port_handle != jNone:
        args['action'] = action.strip() + "_all_protocols"
    elif handle != jNone:
        args['action'] = action.strip() + "_protocol"
    else:
        raise Exception("Please pass either handle or port_handle to the function call")

    # ***** End of Argument *****

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    ret = rt_handle.invoke('test_control', **args)

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ipv6_autoconfig_stats(
        rt_handle,
        mode=jNone,
        handle=jNone,
        action=jNone,
        port_handle=jNone):

    """
    :param rt_handle:       RT object
    :param mode
    :param handle
    :param action
    :param port_handle
    """

    __check_and_raise(action)
    root = invoke_ixnet(rt_handle, 'getRoot')
    if action == 'collect':
        stats = invoke_ixnet(rt_handle, "getList", root, "statistics")
        stat_handles = invoke_ixnet(rt_handle, "getList", stats[0], "view")
        caption_list = ["Port Summary", "IPv6 Autoconfiguration Per Port"]
        ret = {'session': '', 'aggregate': ''}
        if handle != jNone:
            if not isinstance(handle, list):
                handle = handle.split()
            port_handle = [get_ixia_port_handle(rt_handle, hndl)  for hndl in handle]
        for caption in caption_list:
            port_dict = dict()
            pattern = re.compile(r".*{}.*".format(caption))
            hndl = list(filter(pattern.match, stat_handles))
            page_object = invoke_ixnet(rt_handle, "getList", hndl[0], "page")
            stat_key = invoke_ixnet(rt_handle, "getAttribute", page_object[0], "-columnCaptions")
            stat_key_value = invoke_ixnet(rt_handle, "getAttribute", page_object[0], "-rowValues")
            for i in range(0, len(stat_key_value)):
                port = stat_key_value[i][0][0]
                if caption == "Port Summary":
                    port_dict[port] = dict(zip(stat_key, stat_key_value[i][0]))
                    ret['session'] = port_dict
                if caption == 'IPv6 Autoconfiguration Per Port':
                    port_dict[port] = dict(zip(stat_key, stat_key_value[i][0]))
                    port_dict1 = {'tx_rtr_sol': port_dict[port].get('Router Solicits Tx'),\
                                 'rx_rtr_adv': port_dict[port].get('Router Advertisements Rx'),\
                                 'tx_nbr_sol': port_dict[port].get('Neighbor Solicits Tx'),\
                                 'rx_nbr_adv': port_dict[port].get('Neighbor Advertisements Rx')}
                    port_dict[port].update(port_dict1)
                    ret['aggregate'] = port_dict

        protocol_dict = rt_handle.invoke('protocol_info', mode='handles')
        protocol_handles = list(protocol_dict.keys())
        pattern = re.compile(r".*ipv6Autoconfiguration:\d+")
        ipv6_blocks = list(filter(pattern.match, protocol_handles))
        ip_dict = dict()
        session_ip_dict = dict()
        for block in ipv6_blocks:
            portName = get_ixia_port_handle(rt_handle, block)
            item_handles = protocol_dict[block]['handles']['sessions_total'].split()
            item_values = [invoke_ixnet(rt_handle, "getAttribute", item, "-address") for item in item_handles]
            ip_dict = dict(zip(item_handles, item_values))
            session_ip_dict['session_ip'] = ip_dict
            ret['session'][portName].update(session_ip_dict)
        statDict = dict()
        if mode != jNone:
            if port_handle == jNone:
                return ret[mode]
            elif not isinstance(port_handle, list):
                port_handle = port_handle.split()
            for port in port_handle:
                if port in ret[mode].keys():
                    statDict[port] = ret[mode][port]
                else:
                    raise Exception("Error: Port {} not present. Please check!!!".format(port))
            return statDict
    elif action == 'clear':
        return invoke_ixnet(rt_handle, 'execute', "clearStats", root)
    else:
        raise Exception("Error: Invalid value for arg action. It supports only collect|clear")

    return ret

def j_l2tp_config(
        rt_handle,
        attempt_rate=jNone,
        auth_mode=jNone,
        auth_req_timeout=jNone,
        config_req_timeout=jNone,
        echo_req_interval=jNone,
        hello_interval=jNone,
        hostname=jNone,
        l2tp_src_count=jNone,
        max_auth_req=jNone,
        max_ipcp_req=jNone,
        max_terminate_req=jNone,
        mode=jNone,
        num_tunnels=jNone,
        redial_max=jNone,
        redial_timeout=jNone,
        rws=jNone,
        secret=jNone,
        sessions_per_tunnel=jNone,
        udp_src_port=jNone,
        vlan_count=jNone,
        vlan_id=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        wildcard_bang_end=jNone,
        wildcard_bang_start=jNone,
        wildcard_dollar_end=jNone,
        wildcard_dollar_start=jNone,
        wildcard_pound_end=jNone,
        wildcard_pound_start=jNone,
        wildcard_question_end=jNone,
        wildcard_question_start=jNone,
        handle=jNone,
        username=jNone,
        password=jNone,
        l2_encap=jNone,
        l2tp_src_addr=jNone,
        l2tp_dst_addr=jNone,
        l2tp_mac_addr=jNone,
        ppp_server_ip=jNone,
        ppp_client_ip=jNone,
        ppp_client_step=jNone,
        port_handle=jNone,
        l2tp_node_type=jNone,
        vlan_id_outer=jNone,
        vlan_id_step_outer=jNone,
        vlan_user_priority_outer=jNone):

    """
    :param rt_handle:       RT object
    :param attempt_rate - <1-1000>
    :param auth_mode - <none|pap|chap|pap_or_chap>
    :param auth_req_timeout - <1-65535>
    :param config_req_timeout - <1-120>
    :param echo_req_interval - <1-65535>
    :param hello_interval - <1-180>
    :param hostname
    :param l2tp_src_count - <1-112>
    :param max_auth_req - <1-65535>
    :param max_ipcp_req - <1-255>
    :param max_terminate_req - <1-1000>
    :param mode - <create|modify|delete:remove>
    :param num_tunnels - <1-32000>
    :param redial_max - <1-20>
    :param redial_timeout - <1-20>
    :param rws - <1-2048>
    :param secret
    :param sessions_per_tunnel - <1-64000>
    :param udp_src_port - <1-65535>
    :param vlan_count - <1-4094>
    :param vlan_id - <1-4095>
    :param vlan_id_step - <0-4093>
    :param vlan_user_priority - <0-7>
    :param wildcard_bang_end - <0-65535>
    :param wildcard_bang_start - <0-65535>
    :param wildcard_dollar_end - <0-65535>
    :param wildcard_dollar_start - <0-65535>
    :param wildcard_pound_end - <0-65535>
    :param wildcard_pound_start - <0-65535>
    :param wildcard_question_end - <0-65535>
    :param wildcard_question_start - <0-65535>
    :param handle
    :param username
    :param password
    :param l2_encap - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq|atm_snap|atm_vc_mux>
    :param l2tp_src_addr
    :param l2tp_dst_addr
    :param l2tp_mac_addr
    :param ppp_server_ip
    :param ppp_client_ip
    :param ppp_client_step
    :param port_handle
    :param l2tp_node_type - <lac|lns>
    :param vlan_id_outer - <1-4095>
    :param vlan_id_step_outer - <0-4093>
    :param vlan_user_priority_outer - <0-7>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "procName": "l2tp_config",
        "status": "1"
    }

    IXIA Returns:
    {
        "ethernet_handle": "/topology:1/deviceGroup:1/ethernet:1",
        "handle": "/range:HLAPI0",
        "handles": "/range:HLAPI0",
        "ipv4_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1",
        "lns_auth_credentials_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/lnsAuthCredentials",
        "lns_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1",
        "pppox_server_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/pppoxserver:1",
        "pppox_server_sessions_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/pppoxserver:1/pppoxServerSessions",
        "status": "1"
    }
    {
        "ethernet_handle": "/topology:2/deviceGroup:1/deviceGroup:1/ethernet:1 /topology:2/deviceGroup:1/ethernet:1",
        "handle": "/range:HLAPI1",
        "handles": "/range:HLAPI1",
        "ipv4_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1",
        "lac_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/lac:1",
        "pppox_client_handle": "/topology:2/deviceGroup:1/deviceGroup:1/ethernet:1/pppoxclient:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    vlan_args = dict()
    args['attempt_rate'] = attempt_rate
    args['auth_mode'] = auth_mode
    args['auth_req_timeout'] = auth_req_timeout
    args['config_req_timeout'] = config_req_timeout
    args['echo_req_interval'] = echo_req_interval
    args['hello_interval'] = hello_interval
    args['hostname'] = hostname
    args['l2tp_src_count'] = l2tp_src_count
    args['max_auth_req'] = max_auth_req
    args['max_ipcp_req'] = max_ipcp_req
    args['max_terminate_req'] = max_terminate_req
    args['num_tunnels'] = num_tunnels
    args['redial_max'] = redial_max
    args['redial_timeout'] = redial_timeout
    args['rws'] = rws
    args['secret'] = secret
    args['sessions_per_tunnel'] = sessions_per_tunnel
    args['udp_src_port'] = udp_src_port
    args['vlan_count'] = vlan_count
    args['wildcard_bang_end'] = wildcard_bang_end
    args['wildcard_bang_start'] = wildcard_bang_start
    args['wildcard_dollar_end'] = wildcard_dollar_end
    args['wildcard_dollar_start'] = wildcard_dollar_start
    args['wildcard_pound_end'] = wildcard_pound_end
    args['wildcard_pound_start'] = wildcard_pound_start
    args['wildcard_question_end'] = wildcard_question_end
    args['wildcard_question_start'] = wildcard_question_start
    args['username'] = username
    args['password'] = password
    args['l2_encap'] = l2_encap
    args['l2tp_src_addr'] = l2tp_src_addr
    args['l2tp_dst_addr'] = l2tp_dst_addr
    args['l2tp_mac_addr'] = l2tp_mac_addr
    args['ppp_server_ip'] = ppp_server_ip
    args['ppp_client_ip'] = ppp_client_ip
    args['ppp_client_step'] = ppp_client_step
    args['port_handle'] = port_handle
    args['l2tp_node_type'] = l2tp_node_type
    args['handle'] = handle
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_user_priority'] = vlan_user_priority
    vlan_args['vlan_id_outer'] = vlan_id_outer
    vlan_args['vlan_id_step_outer'] = vlan_id_step_outer
    vlan_args['vlan_user_priority_outer'] = vlan_user_priority_outer

    defaultValues = {'l2tp_dst_addr': "192.85.1.3", 'l2tp_src_addr': "192.85.1.3", 'l2_encap': 'ethernet_ii', 'num_tunnels': 1}
    for key in defaultValues.keys():
        if args.get(key) == jNone:
            args[key] = defaultValues[key]

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_l2tp_config.__doc__, **args)
    if args.get('mode'):
        args['action'] = args.pop('mode')
    if args.get('l2tp_mac_addr'):
        args['src_mac_addr'] = args.pop('l2tp_mac_addr')
    if args.get('l2tp_node_type'):
        args['mode'] = args.pop('l2tp_node_type')
    if not args.get('mode'):
        args['mode'] = 'lac'

    vlan_args = get_arg_value(rt_handle, j_l2tp_config.__doc__, **vlan_args)

    if mode == 'create':
        __check_and_raise(port_handle)
        handle = port_handle
    elif mode == 'modify':
        __check_and_raise(handle)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = list()
    for hndl in handle:
        if re.match(r"\d+\/\d+\/\d+", hndl):
            args['port_handle'] = hndl
        else:
            args['handle'] = hndl
        ret.append(rt_handle.invoke('l2tp_config', **args))
        if args['mode']+'_handle' in ret[-1]:
            handle = args['mode']+'_handle'
            ret[-1]['handles'] = ret[-1][handle]
        if vlan_args:
            if mode == "create":
                if l2tp_node_type.lower() == 'lac':
                    ethernet_handle = ret[-1]['ethernet_handle'].split()
                    ethernet_handle = ethernet_handle[-1]
                else:
                    ethernet_handle = ret[-1]['ethernet_handle']
                vlan_config(rt_handle, vlan_args, ethernet_handle)
            else:
                vlan_config(rt_handle, vlan_args, hndl)

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_l2tp_control(rt_handle, action=jNone, handle=jNone):
    """
    :param rt_handle:       RT object
    :param action - <connect|disconnect|retry>
    :param handle

    Spirent Returns:
    {
        "procName": "l2tp_control",
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_l2tp_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if action == 'connect' or action == 'retry':
            if 'lns' in hndl:
                pppoxserver_hndl = invoke_ixnet(rt_handle, 'getList', hndl, 'pppoxserver')
                hndl = pppoxserver_hndl[0].strip("::ixNet::OBJ-")
            elif 'lac' in hndl:
                deviceGroup_hndl = __get_parent_handle(hndl, 'deviceGroup')
                dg_hndl = invoke_ixnet(rt_handle, 'getList', deviceGroup_hndl, 'deviceGroup')
                eth_handle = invoke_ixnet(rt_handle, 'getList', dg_hndl[0], 'ethernet')
                pppoxclient_hndl = invoke_ixnet(rt_handle, 'getList', eth_handle[0], 'pppoxclient')
                hndl = pppoxclient_hndl[0].strip("::ixNet::OBJ-")
        args['handle'] = hndl
        ret.append(rt_handle.invoke('l2tp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_l2tp_stats(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode

    Spirent Returns:
    {
        "aggregate": {
            "avg_setup_time": "8",
            "cdn_rx": "0",
            "cdn_tx": "0",
            "chap_rx": "2",
            "chap_tx": "1",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "disconnect_success": "0",
            "disconnecting": "0",
            "echo_reply_rx": "0",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "hello_rx": "0",
            "hello_tx": "0",
            "iccn_rx": "0",
            "iccn_tx": "1",
            "icrp_rx": "1",
            "icrp_tx": "0",
            "icrq_rx": "0",
            "icrq_tx": "1",
            "idle": "0",
            "ipcp_rx": "3",
            "ipcp_tx": "3",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "max_setup_time": "8",
            "min_setup_time": "8",
            "retry_count": "0",
            "scccn_rx": "0",
            "scccn_tx": "1",
            "sccrp_rx": "1",
            "sccrp_tx": "0",
            "sccrq_rx": "0",
            "sccrq_tx": "1",
            "session_status": "CONNECTED",
            "sessions_down": "0",
            "sessions_up": "1",
            "sli_rx": "0",
            "sli_tx": "0",
            "stopccn_rx": "0",
            "stopccn_tx": "0",
            "success_setup_rate": "122",
            "term_ack_rx": "0",
            "term_ack_txv": "0",
            "term_req_rx": "0",
            "term_req_tx": "0",
            "tunnels_up": "1",
            "tx_pkt_acked": "2",
            "wen_rx": "0",
            "wen_tx": "0",
            "zlb_rx": "2",
            "zlb_tx": "0"
        },
        "handles": "host2",
        "procName": "l2tp_status",
        "session": {
            "1": {
                "1": {
                    "cdn_rx": "0",
                    "cdn_tx": "0",
                    "iccn_rx": "0",
                    "iccn_tx": "1",
                    "icrp_rx": "1",
                    "icrp_tx": "0",
                    "icrq_rx": "0",
                    "icrq_tx": "1"
                }
            },
            "host2": {
                "1": {
                    "cdn_rx": "0",
                    "cdn_tx": "0",
                    "iccn_rx": "0",
                    "iccn_tx": "1",
                    "icrp_rx": "1",
                    "icrp_tx": "0",
                    "icrq_rx": "0",
                    "icrq_tx": "1"
                }
            }
        },
        "status": "1",
        "tunnel": {
            "1": {
                "hello_rx": "0",
                "hello_tx": "0",
                "scccn_rx": "0",
                "scccn_tx": "1",
                "sccrp_rx": "1",
                "sccrp_tx": "0",
                "sli_rx": "0",
                "sli_tx": "0",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tx_pkt_acked": "0",
                "wen_rx": "0",
                "wen_tx": "0"
            }
        }
    }

    IXIA Returns:
    {
        "/topology:2/deviceGroup:1/deviceGroup:1/ethernet:1/pppoxclient:1/item:1": {
            "session": {
                "ac_cookie": "Not Available",
                "ac_cookie_tag_rx": "0",
                "ac_generic_error_occured": "False",
                "ac_mac_addr": "Not Available",
                "ac_name": "Not Available",
                "ac_offers_rx": "0",
                "ac_system_error_occured": "False",
                "ac_system_error_tag_rx": "0",
                "auth_id": "user",
                "auth_latency": "1462",
                "auth_password": "secret",
                "auth_protocol_rx": "CHAP",
                "auth_protocol_tx": "None",
                "auth_total_rx": "2",
                "auth_total_tx": "1",
                "avg_setup_time": "12646",
                "call_id": "1",
                "call_state": "Established",
                "chap_auth_chal_rx": "1",
                "chap_auth_fail_rx": "0",
                "chap_auth_role": "Peer",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "cookie": "Not Available",
                "cookie_len": "0",
                "cumulative_setup_failed": "0",
                "cumulative_setup_initiated": "1",
                "cumulative_setup_succeeded": "1",
                "cumulative_teardown_failed": "0",
                "cumulative_teardown_succeeded": "0",
                "data_ns": "0",
                "destination_ip": "1.1.1.1",
                "destination_port": "1701",
                "dns_server_list": "Not Available",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "gateway_ip": "1.1.1.1",
                "generic_error_tag_rx": "0",
                "host_mac_addr": "Not Available",
                "host_name": "Not Available",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "1",
                "ipcp_cfg_nak_tx": "0",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "1",
                "ipcp_cfg_req_tx": "2",
                "ipcp_latency": "3454",
                "ipcp_state": "NCP Open",
                "ipv6_addr": "0:0:0:0:0:0:0:0",
                "ipv6_prefix_len": "0",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_latency": "0",
                "ipv6cp_router_adv_rx": "0",
                "ipv6cp_state": "NCP Disable",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_latency": "1485",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "local_ip_addr": "1.1.1.3",
                "local_ipv6_iid": "Not Available",
                "loopback_detected": "False",
                "magic_no_negotiated": "True",
                "magic_no_rx": "1816763613",
                "magic_no_tx": "1022819482",
                "mru": "1500",
                "mtu": "1500",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "negotiation_end_ms": "0",
                "negotiation_start_ms": "0",
                "padi_timeouts": "0",
                "padi_tx": "0",
                "pado_rx": "0",
                "padr_timeouts": "0",
                "padr_tx": "0",
                "pads_rx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "peer_call_id": "1",
                "peer_id": "1",
                "peer_ipv6_iid": "Not Available",
                "ppp_close_mode": "None",
                "ppp_state": "PPP Connected",
                "pppoe_discovery_latency": "0",
                "pppoe_session_id": "0",
                "pppox_state": "Init",
                "primary_wins_server": "0.0.0.0",
                "relay_session_id_tag_rx": "0",
                "remote_ip_addr": "1.1.1.1",
                "secondary_wins_server": "0.0.0.0",
                "service_name": "Not Available",
                "service_name_error_tag_rx": "0",
                "source_ip": "1.1.1.2",
                "source_port": "1701",
                "status": "up",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "total_bytes_rx": "0",
                "total_bytes_tx": "0",
                "tunnel_id": "1",
                "tunnel_state": "Tunnel established",
                "vendor_specific_tag_rx": "0"
            }
        },
        "1/25/1": {
            "aggregate": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "chap_auth_chal_rx": "1",
                "chap_auth_fail_rx": "0",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "client_interfaces_in_ppp_negotiation": "0",
                "client_session_avg_latency": "12646.00",
                "client_session_max_latency": "12646",
                "client_session_min_latency": "12646",
                "client_tunnels_up": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "cumulative_setup_failed": "0",
                "cumulative_setup_initiated": "1",
                "cumulative_setup_succeeded": "1",
                "cumulative_teardown_failed": "0",
                "cumulative_teardown_succeeded": "0",
                "duplicate_rx": "0",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "0",
                "iccn_tx": "1",
                "icrp_rx": "1",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "1",
                "in_order_rx": "2",
                "interfaces_in_pppoe_l2tp_negotiation": "0",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "1",
                "ipcp_cfg_nak_tx": "0",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "1",
                "ipcp_cfg_req_tx": "2",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_router_adv_rx": "0",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "144",
                "l2tp_tunnel_total_bytes_tx": "308",
                "lcp_avg_latency": "1485.00",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_max_latency": "1485",
                "lcp_min_latency": "1485",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "ncp_avg_latency": "3454.00",
                "ncp_max_latency": "3454",
                "ncp_min_latency": "3454",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "num_sessions": "1",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "padi_timeouts": "0",
                "padi_tx": "0",
                "pado_rx": "0",
                "padr_timeouts": "0",
                "padr_tx": "0",
                "pads_rx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "ppp_total_bytes_rx": "161",
                "ppp_total_bytes_tx": "104",
                "retransmits": "0",
                "scccn_rx": "0",
                "scccn_tx": "1",
                "sccrp_rx": "1",
                "sccrp_tx": "0",
                "sccrq_rx": "0",
                "sccrq_tx": "1",
                "sessions_failed": "0",
                "sessions_not_started": "0",
                "sessions_up": "1",
                "sli_rx": "0",
                "sli_tx": "0",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "success_setup_rate": "0",
                "teardown_failed": "0",
                "teardown_rate": "0",
                "teardown_succeeded": "0",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "total_bytes_rx": "0",
                "total_bytes_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "4",
                "tx_pkt_acked": "4",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "2",
                "zlb_tx": "0"
            }
        },
        "aggregate": {
            "cdn_rx": "0",
            "cdn_tx": "0",
            "chap_auth_chal_rx": "1",
            "chap_auth_fail_rx": "0",
            "chap_auth_rsp_tx": "1",
            "chap_auth_succ_rx": "1",
            "client_interfaces_in_ppp_negotiation": "0",
            "client_session_avg_latency": "12646.00",
            "client_session_max_latency": "12646",
            "client_session_min_latency": "12646",
            "client_tunnels_up": "1",
            "code_rej_rx": "0",
            "code_rej_tx": "0",
            "cumulative_setup_failed": "0",
            "cumulative_setup_initiated": "1",
            "cumulative_setup_succeeded": "1",
            "cumulative_teardown_failed": "0",
            "cumulative_teardown_succeeded": "0",
            "duplicate_rx": "0",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_rsp_rx": "0",
            "echo_rsp_tx": "0",
            "hello_rx": "0",
            "hello_tx": "0",
            "iccn_rx": "0",
            "iccn_tx": "1",
            "icrp_rx": "1",
            "icrp_tx": "0",
            "icrq_rx": "0",
            "icrq_tx": "1",
            "in_order_rx": "2",
            "interfaces_in_pppoe_l2tp_negotiation": "0",
            "ipcp_cfg_ack_rx": "1",
            "ipcp_cfg_ack_tx": "1",
            "ipcp_cfg_nak_rx": "1",
            "ipcp_cfg_nak_tx": "0",
            "ipcp_cfg_rej_rx": "0",
            "ipcp_cfg_rej_tx": "0",
            "ipcp_cfg_req_rx": "1",
            "ipcp_cfg_req_tx": "2",
            "ipv6cp_cfg_ack_rx": "0",
            "ipv6cp_cfg_ack_tx": "0",
            "ipv6cp_cfg_nak_rx": "0",
            "ipv6cp_cfg_nak_tx": "0",
            "ipv6cp_cfg_rej_rx": "0",
            "ipv6cp_cfg_rej_tx": "0",
            "ipv6cp_cfg_req_rx": "0",
            "ipv6cp_cfg_req_tx": "0",
            "ipv6cp_router_adv_rx": "0",
            "l2tp_calls_up": "1",
            "l2tp_tunnel_total_bytes_rx": "144",
            "l2tp_tunnel_total_bytes_tx": "308",
            "lcp_avg_latency": "1485.00",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "lcp_max_latency": "1485",
            "lcp_min_latency": "1485",
            "lcp_protocol_rej_rx": "0",
            "lcp_protocol_rej_tx": "0",
            "lcp_total_msg_rx": "2",
            "lcp_total_msg_tx": "2",
            "ncp_avg_latency": "3454.00",
            "ncp_max_latency": "3454",
            "ncp_min_latency": "3454",
            "ncp_total_msg_rx": "3",
            "ncp_total_msg_tx": "3",
            "num_sessions": "1",
            "out_of_order_rx": "0",
            "out_of_win_rx": "0",
            "padi_timeouts": "0",
            "padi_tx": "0",
            "pado_rx": "0",
            "padr_timeouts": "0",
            "padr_tx": "0",
            "pads_rx": "0",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_rx": "0",
            "pap_auth_nak_rx": "0",
            "pap_auth_req_tx": "0",
            "ppp_total_bytes_rx": "161",
            "ppp_total_bytes_tx": "104",
            "retransmits": "0",
            "scccn_rx": "0",
            "scccn_tx": "1",
            "sccrp_rx": "1",
            "sccrp_tx": "0",
            "sccrq_rx": "0",
            "sccrq_tx": "1",
            "sessions_failed": "0",
            "sessions_not_started": "0",
            "sessions_up": "1",
            "sli_rx": "0",
            "sli_tx": "0",
            "stopccn_rx": "0",
            "stopccn_tx": "0",
            "success_setup_rate": "0",
            "teardown_failed": "0",
            "teardown_rate": "0",
            "teardown_succeeded": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0",
            "total_bytes_rx": "0",
            "total_bytes_tx": "0",
            "tun_tx_win_close": "0",
            "tun_tx_win_open": "4",
            "tx_pkt_acked": "4",
            "wen_rx": "0",
            "wen_tx": "0",
            "zlb_rx": "2",
            "zlb_tx": "0"
        },
        "session": {
            "/range:HLAPI1": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "duplicate_rx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "0",
                "iccn_tx": "1",
                "icrp_rx": "1",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "1",
                "in_order_rx": "2",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "144",
                "l2tp_tunnel_total_bytes_tx": "308",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "retransmits": "0",
                "scccn_rx": "0",
                "scccn_tx": "1",
                "sccrp_rx": "1",
                "sccrp_tx": "0",
                "sccrq_rx": "0",
                "sccrq_tx": "1",
                "sli_rx": "0",
                "sli_tx": "0",
                "status": "up",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "4",
                "tx_pkt_acked": "4",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "2",
                "zlb_tx": "0"
            },
            "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/lac:1/item:1_1": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "duplicate_rx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "0",
                "iccn_tx": "1",
                "icrp_rx": "1",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "1",
                "in_order_rx": "2",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "144",
                "l2tp_tunnel_total_bytes_tx": "308",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "retransmits": "0",
                "scccn_rx": "0",
                "scccn_tx": "1",
                "sccrp_rx": "1",
                "sccrp_tx": "0",
                "sccrq_rx": "0",
                "sccrq_tx": "1",
                "sli_rx": "0",
                "sli_tx": "0",
                "status": "up",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "4",
                "tx_pkt_acked": "4",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "2",
                "zlb_tx": "0"
            }
        },
        "status": "1"
    },
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/pppoxserver:1/item:1": {
            "session": {
                "ac_mac_addr": "Not Available",
                "ac_name": "Not Available",
                "auth_id": "user",
                "auth_latency": "1401",
                "auth_password": "secret",
                "auth_protocol_rx": "None",
                "auth_protocol_tx": "CHAP",
                "auth_total_rx": "1",
                "auth_total_tx": "2",
                "avg_setup_time": "9386",
                "call_id": "1",
                "call_state": "Established",
                "chap_auth_chal_tx": "1",
                "chap_auth_fail_tx": "0",
                "chap_auth_role": "Peer",
                "chap_auth_rsp_rx": "1",
                "chap_auth_succ_tx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "cookie": "Not Available",
                "cookie_len": "0",
                "data_ns": "0",
                "destination_ip": "1.1.1.2",
                "destination_port": "1701",
                "dns_server_list": "Not Available",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "gateway_ip": "1.1.1.2",
                "generic_error_tag_rx": "0",
                "host_mac_addr": "Not Available",
                "host_name": "Not Available",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "0",
                "ipcp_cfg_nak_tx": "1",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "2",
                "ipcp_cfg_req_tx": "1",
                "ipcp_latency": "3527",
                "ipcp_state": "NCP Open",
                "ipv6_addr": "0:0:0:0:0:0:0:0",
                "ipv6_prefix_len": "0",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_latency": "0",
                "ipv6cp_router_adv_tx": "0",
                "ipv6cp_router_solicitation_rx": "0",
                "ipv6cp_state": "NCP Disable",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_latency": "2442",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "local_ip_addr": "1.1.1.1",
                "local_ipv6_iid": "Not Available",
                "loopback_detected": "False",
                "magic_no_negotiated": "True",
                "magic_no_rx": "1022819482",
                "magic_no_tx": "1816763613",
                "mru": "1500",
                "mtu": "1500",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "negotiation_end_ms": "0",
                "negotiation_start_ms": "0",
                "padi_rx": "0",
                "pado_tx": "0",
                "padr_rx": "0",
                "pads_tx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_tx": "0",
                "pap_auth_nak_tx": "0",
                "pap_auth_req_rx": "0",
                "peer_call_id": "1",
                "peer_id": "1",
                "peer_ipv6_iid": "Not Available",
                "ppp_close_mode": "None",
                "ppp_state": "PPP Connected",
                "pppoe_discovery_latency": "0",
                "pppoe_session_id": "0",
                "pppox_state": "Init",
                "primary_wins_server": "0.0.0.0",
                "relay_session_id_tag_rx": "0",
                "remote_ip_addr": "1.1.1.3",
                "secondary_wins_server": "0.0.0.0",
                "service_name": "Not Available",
                "source_ip": "1.1.1.1",
                "source_port": "1701",
                "status": "up",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "total_bytes_rx": "0",
                "total_bytes_tx": "0",
                "tunnel_id": "1",
                "tunnel_state": "Tunnel established",
                "vendor_specific_tag_rx": "0"
            }
        },
        "1/25/2": {
            "aggregate": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "chap_auth_chal_tx": "1",
                "chap_auth_fail_tx": "0",
                "chap_auth_rsp_rx": "1",
                "chap_auth_succ_tx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "duplicate_rx": "0",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "1",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "1",
                "icrq_rx": "1",
                "icrq_tx": "0",
                "in_order_rx": "4",
                "interfaces_in_pppoe_l2tp_negotiation": "0",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "0",
                "ipcp_cfg_nak_tx": "1",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "2",
                "ipcp_cfg_req_tx": "1",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_router_adv_tx": "0",
                "ipv6cp_router_solicitation_rx": "0",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "210",
                "l2tp_tunnel_total_bytes_tx": "172",
                "lcp_avg_latency": "2442.00",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_max_latency": "2442",
                "lcp_min_latency": "2442",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "ncp_avg_latency": "3527.00",
                "ncp_max_latency": "3527",
                "ncp_min_latency": "3527",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "num_sessions": "1",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "padi_rx": "0",
                "pado_tx": "0",
                "padr_rx": "0",
                "pads_tx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_tx": "0",
                "pap_auth_nak_tx": "0",
                "pap_auth_req_rx": "0",
                "ppp_total_bytes_rx": "104",
                "ppp_total_bytes_tx": "161",
                "retransmits": "0",
                "scccn_rx": "1",
                "scccn_tx": "0",
                "sccrp_rx": "0",
                "sccrp_tx": "1",
                "sccrq_rx": "1",
                "sccrq_tx": "0",
                "server_interfaces_in_ppp_negotiation": "0",
                "server_session_avg_latency": "9386.00",
                "server_session_max_latency": "9386",
                "server_session_min_latency": "9386",
                "server_tunnels_up": "1",
                "sessions_failed": "0",
                "sessions_not_started": "0",
                "sessions_up": "1",
                "sli_rx": "0",
                "sli_tx": "0",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "total_bytes_rx": "0",
                "total_bytes_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "2",
                "tx_pkt_acked": "2",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "0",
                "zlb_tx": "2"
            }
        },
        "aggregate": {
            "cdn_rx": "0",
            "cdn_tx": "0",
            "chap_auth_chal_tx": "1",
            "chap_auth_fail_tx": "0",
            "chap_auth_rsp_rx": "1",
            "chap_auth_succ_tx": "1",
            "code_rej_rx": "0",
            "code_rej_tx": "0",
            "duplicate_rx": "0",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_rsp_rx": "0",
            "echo_rsp_tx": "0",
            "hello_rx": "0",
            "hello_tx": "0",
            "iccn_rx": "1",
            "iccn_tx": "0",
            "icrp_rx": "0",
            "icrp_tx": "1",
            "icrq_rx": "1",
            "icrq_tx": "0",
            "in_order_rx": "4",
            "interfaces_in_pppoe_l2tp_negotiation": "0",
            "ipcp_cfg_ack_rx": "1",
            "ipcp_cfg_ack_tx": "1",
            "ipcp_cfg_nak_rx": "0",
            "ipcp_cfg_nak_tx": "1",
            "ipcp_cfg_rej_rx": "0",
            "ipcp_cfg_rej_tx": "0",
            "ipcp_cfg_req_rx": "2",
            "ipcp_cfg_req_tx": "1",
            "ipv6cp_cfg_ack_rx": "0",
            "ipv6cp_cfg_ack_tx": "0",
            "ipv6cp_cfg_nak_rx": "0",
            "ipv6cp_cfg_nak_tx": "0",
            "ipv6cp_cfg_rej_rx": "0",
            "ipv6cp_cfg_rej_tx": "0",
            "ipv6cp_cfg_req_rx": "0",
            "ipv6cp_cfg_req_tx": "0",
            "ipv6cp_router_adv_tx": "0",
            "ipv6cp_router_solicitation_rx": "0",
            "l2tp_calls_up": "1",
            "l2tp_tunnel_total_bytes_rx": "210",
            "l2tp_tunnel_total_bytes_tx": "172",
            "lcp_avg_latency": "2442.00",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "lcp_max_latency": "2442",
            "lcp_min_latency": "2442",
            "lcp_protocol_rej_rx": "0",
            "lcp_protocol_rej_tx": "0",
            "lcp_total_msg_rx": "2",
            "lcp_total_msg_tx": "2",
            "ncp_avg_latency": "3527.00",
            "ncp_max_latency": "3527",
            "ncp_min_latency": "3527",
            "ncp_total_msg_rx": "3",
            "ncp_total_msg_tx": "3",
            "num_sessions": "1",
            "out_of_order_rx": "0",
            "out_of_win_rx": "0",
            "padi_rx": "0",
            "pado_tx": "0",
            "padr_rx": "0",
            "pads_tx": "0",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_tx": "0",
            "pap_auth_nak_tx": "0",
            "pap_auth_req_rx": "0",
            "ppp_total_bytes_rx": "104",
            "ppp_total_bytes_tx": "161",
            "retransmits": "0",
            "scccn_rx": "1",
            "scccn_tx": "0",
            "sccrp_rx": "0",
            "sccrp_tx": "1",
            "sccrq_rx": "1",
            "sccrq_tx": "0",
            "server_interfaces_in_ppp_negotiation": "0",
            "server_session_avg_latency": "9386.00",
            "server_session_max_latency": "9386",
            "server_session_min_latency": "9386",
            "server_tunnels_up": "1",
            "sessions_failed": "0",
            "sessions_not_started": "0",
            "sessions_up": "1",
            "sli_rx": "0",
            "sli_tx": "0",
            "stopccn_rx": "0",
            "stopccn_tx": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0",
            "total_bytes_rx": "0",
            "total_bytes_tx": "0",
            "tun_tx_win_close": "0",
            "tun_tx_win_open": "2",
            "tx_pkt_acked": "2",
            "wen_rx": "0",
            "wen_tx": "0",
            "zlb_rx": "0",
            "zlb_tx": "2"
        },
        "session": {
            "/range:HLAPI0": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "duplicate_rx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "1",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "1",
                "icrq_rx": "1",
                "icrq_tx": "0",
                "in_order_rx": "4",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "210",
                "l2tp_tunnel_total_bytes_tx": "172",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "retransmits": "0",
                "scccn_rx": "1",
                "scccn_tx": "0",
                "sccrp_rx": "0",
                "sccrp_tx": "1",
                "sccrq_rx": "1",
                "sccrq_tx": "0",
                "server_tunnels_up": "1",
                "session_status": "Up",
                "sli_rx": "0",
                "sli_tx": "0",
                "status": "up",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "2",
                "tx_pkt_acked": "2",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "0",
                "zlb_tx": "2"
            },
            "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/item:1_1": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "duplicate_rx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "1",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "1",
                "icrq_rx": "1",
                "icrq_tx": "0",
                "in_order_rx": "4",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "210",
                "l2tp_tunnel_total_bytes_tx": "172",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "retransmits": "0",
                "scccn_rx": "1",
                "scccn_tx": "0",
                "sccrp_rx": "0",
                "sccrp_tx": "1",
                "sccrq_rx": "1",
                "sccrq_tx": "0",
                "server_tunnels_up": "1",
                "session_status": "Up",
                "sli_rx": "0",
                "sli_tx": "0",
                "status": "up",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "2",
                "tx_pkt_acked": "2",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "0",
                "zlb_tx": "2"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
        "aggregate"
        "session"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'aggregate'
        stats.update(rt_handle.invoke('l2tp_stats', **args))
        args['mode'] = 'session'
        stats.update(rt_handle.invoke('l2tp_stats', **args))
        args['mode'] = 'session_dhcpv6pd'
        stats.update(rt_handle.invoke('l2tp_stats', **args))
        if 'session' in stats:
            for key in list(stats['session']):
                stats['session'][args['handle']] = stats['session'][key]
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                ret[index]['aggregate'] = ret[index][key]['aggregate']
    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_pppox_config(
        rt_handle,
        attempt_rate=jNone,
        auth_mode=jNone,
        auth_req_timeout=jNone,
        config_req_timeout=jNone,
        disconnect_rate=jNone,
        echo_req_interval=jNone,
        handle=jNone,
        intermediate_agent=jNone,
        ipcp_req_timeout=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        max_auth_req=jNone,
        max_configure_req=jNone,
        max_ipcp_req=jNone,
        max_outstanding=jNone,
        max_padi_req=jNone,
        max_padr_req=jNone,
        max_terminate_req=jNone,
        num_sessions=jNone,
        padi_req_timeout=jNone,
        padr_req_timeout=jNone,
        password_wildcard=jNone,
        qinq_incr_mode=jNone,
        username_wildcard=jNone,
        vlan_id=jNone,
        vlan_id_count=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_count=jNone,
        vlan_id_outer_step=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        username=jNone,
        password=jNone,
        protocol=jNone,
        mode=jNone,
        ip_cp=jNone,
        port_handle=jNone,
        vlan_outer_user_priority=jNone,
        encap=jNone,
        echo_req=jNone):
    """
    :param rt_handle:       RT object
    :param attempt_rate - <1-1000>
    :param auth_mode - <none|pap|chap|pap_or_chap>
    :param auth_req_timeout - <1-65535>
    :param config_req_timeout - <1-120>
    :param disconnect_rate - <1-1000>
    :param echo_req_interval - <1-3600>
    :param handle
    :param intermediate_agent - <0|1>
    :param ipcp_req_timeout - <1-120>
    :param mac_addr
    :param mac_addr_step
    :param max_auth_req - <1-65535>
    :param max_configure_req - <1-255>
    :param max_ipcp_req - <1-255>
    :param max_outstanding - <1-1000>
    :param max_padi_req - <1-65535>
    :param max_padr_req - <1-65535>
    :param max_terminate_req - <1-65535>
    :param num_sessions - <1-32000>
    :param padi_req_timeout - <1-65535>
    :param padr_req_timeout - <1-65535>
    :param password_wildcard - <0|1>
    :param qinq_incr_mode - <inner|outer|both>
    :param username_wildcard - <0|1>
    :param vlan_id - <0-4095>
    :param vlan_id_count - <1-4094>
    :param vlan_id_outer - <0-4095>
    :param vlan_id_outer_count - <1-4094>
    :param vlan_id_outer_step - <0-4094>
    :param vlan_id_step - <0-4094>
    :param vlan_user_priority - <0-7>
    :param username
    :param password
    :param protocol - <pppoe|pppoa|pppoeoa>
    :param mode - <create:add|modify|reset:remove>
    :param ip_cp - <ipv4_cp|ipv6_cp|ipv4v6_cp:dual_stack>
    :param port_handle
    :param vlan_outer_user_priority - <0-7>
    :param encap - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq|vc_mux|llcsnap>
    :param echo_req - <0|1>


    Spirent Returns:
    {
        "handle": "host3",
        "handles": "host3",
        "port_handle": "port2",
        "pppoe_port": "pppoxportconfig2",
        "pppoe_session": "pppoeclientblockconfig1",
        "procName": "sth::pppox_config",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/range:HLAPI1",
        "handles": "/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1",
        "pppox_client_handle": "/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    vlan_args = dict()
    args['attempt_rate'] = attempt_rate
    args['auth_mode'] = auth_mode
    args['auth_req_timeout'] = auth_req_timeout
    args['config_req_timeout'] = config_req_timeout
    args['disconnect_rate'] = disconnect_rate
    args['echo_req_interval'] = echo_req_interval
    args['handle'] = handle
    args['intermediate_agent'] = intermediate_agent
    args['ipcp_req_timeout'] = ipcp_req_timeout
    args['mac_addr'] = mac_addr
    args['mac_addr_step'] = mac_addr_step
    args['max_auth_req'] = max_auth_req
    args['max_configure_req'] = max_configure_req
    args['max_ipcp_req'] = max_ipcp_req
    args['max_outstanding'] = max_outstanding
    args['max_padi_req'] = max_padi_req
    args['max_padr_req'] = max_padr_req
    args['max_terminate_req'] = max_terminate_req
    args['num_sessions'] = num_sessions
    args['padi_req_timeout'] = padi_req_timeout
    args['padr_req_timeout'] = padr_req_timeout
    args['password_wildcard'] = password_wildcard
    args['qinq_incr_mode'] = qinq_incr_mode
    args['username_wildcard'] = username_wildcard
    args['vlan_id_count'] = vlan_id_count
    args['vlan_id_outer_count'] = vlan_id_outer_count
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_outer'] = vlan_id_outer
    vlan_args['vlan_id_outer_step'] = vlan_id_outer_step
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_user_priority'] = vlan_user_priority
    vlan_args['vlan_outer_user_priority'] = vlan_outer_user_priority
    args['username'] = username
    args['password'] = password
    args['protocol'] = protocol
    args['encap'] = encap
    args['mode'] = mode
    args['ip_cp'] = ip_cp
    args['port_handle'] = port_handle
    args['echo_req'] = echo_req

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_pppox_config.__doc__, **args)
    args['port_role'] = 'access'
    if ip_cp == 'ipv4':
        args['ip_cp'] = 'ipv4_cp'
        args['client_ipv4_ncp_configuration'] = 'learned'
    elif ip_cp == 'ipv6':
        args['ip_cp'] = 'ipv6_cp'
        args['client_ipv6_ncp_configuration'] = 'learned'

    vlan_args = get_arg_value(rt_handle, j_pppox_config.__doc__, **vlan_args)

    if mode == 'create':
        if args.get('port_handle'):
            handle = create_deviceGroup(rt_handle, args.pop('port_handle'))
            handle = handle['device_group_handle']
        elif not args.get('handle'):
            raise Exception("Please pass either handle or port_handle to the function call")

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    ret = []
    for hndl in handle:
        if re.match(r"\d+\/\d+\/\d+", hndl):
            args['port_handle'] = hndl
        else:
            args['handle'] = hndl
        ret.append(rt_handle.invoke('pppox_config', **args))
        if vlan_args:
            if mode == 'create':
                vlan_config(rt_handle, vlan_args, ret[-1]['pppox_client_handle'])
            else:
                vlan_config(rt_handle, vlan_args, hndl)
        if 'pppox_client_handle' in ret[-1]:
            ret[-1]['handles'] = ret[-1]['pppox_client_handle']

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_pppox_control(rt_handle, action=jNone, handle=jNone):
    """
    :param rt_handle:       RT object
    :param action - <connect|disconnect|reset>
    :param handle

    Spirent Returns:
    {
        "handles": "host3",
        "procName": "sth::pppox_control",
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_pppox_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('pppox_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_pppox_stats(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <aggregate|session>

    Spirent Returns:
    {
        "agg": {
            "attempted": "1",
            "chap_auth_chal_rx": "2",
            "chap_auth_fail_rx": "2",
            "chap_auth_rsp_tx": "1",
            "chap_auth_succ_rx": "1",
            "completed": "0",
            "connect_success": "1",
            "echo_req_rx": "0",
            "echo_rsp_tx": "0",
            "failed_connect": "0",
            "failed_disconnect": "0",
            "ip_addr": "1.1.1.2",
            "ipcp_cfg_ack_rx": "3",
            "ipcp_cfg_ack_tx": "3",
            "ipcp_cfg_nak_rx": "3",
            "ipcp_cfg_nak_tx": "3",
            "ipcp_cfg_rej_rx": "3",
            "ipcp_cfg_rej_tx": "3",
            "ipcp_cfg_req_rx": "3",
            "ipcp_cfg_req_tx": "3",
            "ipv6_addr": "::",
            "ipv6_global_addr": "::",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "padi_rx": "0",
            "padi_tx": "1",
            "pado_rx": "1",
            "pado_tx": "0",
            "padr_rx": "0",
            "padr_tx": "1",
            "pads_rx": "1",
            "pads_tx": "0",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_rx": "0",
            "pap_auth_nak_rx": "0",
            "pap_auth_req_tx": "0",
            "setup_time": "113",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "aggregate": {
            "abort": "0",
            "atm_mode": "0",
            "avg_setup_time": "113",
            "chap_auth_chal_rx": "2",
            "chap_auth_fail_rx": "2",
            "chap_auth_rsp_tx": "1",
            "chap_auth_succ_rx": "2",
            "connect_attempts": "1",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "disconnect_failed": "0",
            "disconnect_success": "0",
            "disconnecting": "0",
            "echo_req_rx": "0",
            "echo_rsp_tx": "0",
            "idle": "0",
            "ipcp_cfg_ack_rx": "3",
            "ipcp_cfg_ack_tx": "3",
            "ipcp_cfg_nak_rx": "3",
            "ipcp_cfg_nak_tx": "3",
            "ipcp_cfg_rej_rx": "3",
            "ipcp_cfg_rej_tx": "3",
            "ipcp_cfg_req_rx": "3",
            "ipcp_cfg_req_tx": "3",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "max_setup_time": "113",
            "min_setup_time": "113",
            "num_sessions": "1",
            "padi_rx": "0",
            "padi_tx": "1",
            "pado_rx": "1",
            "padr_rx": "0",
            "padr_tx": "1",
            "pads_rx": "1",
            "pads_tx": "0",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_rx": "0",
            "pap_auth_nak_rx": "0",
            "pap_auth_req_tx": "0",
            "sessions_down": "0",
            "sessions_up": "1",
            "success_setup_rate": "8",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "handles": "host3",
        "procName": "sth::pppox_stats",
        "session": {
            "1": {
                "attempted": "1",
                "chap_auth_chal_rx": "2",
                "chap_auth_fail_rx": "2",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "completed": "0",
                "connect_success": "1",
                "echo_req_rx": "0",
                "echo_rsp_tx": "0",
                "failed_connect": "0",
                "failed_disconnect": "0",
                "ip_addr": "1.1.1.2",
                "ipcp_cfg_ack_rx": "3",
                "ipcp_cfg_ack_tx": "3",
                "ipcp_cfg_nak_rx": "3",
                "ipcp_cfg_nak_tx": "3",
                "ipcp_cfg_rej_rx": "3",
                "ipcp_cfg_rej_tx": "3",
                "ipcp_cfg_req_rx": "3",
                "ipcp_cfg_req_tx": "3",
                "ipv6_addr": "::",
                "ipv6_global_addr": "::",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "padi_rx": "0",
                "padi_tx": "1",
                "pado_rx": "1",
                "pado_tx": "0",
                "padr_rx": "0",
                "padr_tx": "1",
                "pads_rx": "1",
                "pads_tx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "setup_time": "113",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0"
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "Range 1/25/1 2 False": {
            "aggregate": {
                "auth_avg_time": "6303.00",
                "auth_max_time": "6303",
                "auth_min_time": "6303",
                "avg_setum_rate": "1.00",
                "avg_setup_time": "88601.00",
                "avg_teardown_rate": "0.00",
                "call_disconnect_notifiy_rx": "0",
                "call_disconnect_notifiy_tx": "0",
                "chap_auth_chal_rx": "1",
                "chap_auth_fail_rx": "0",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "connect_success": "1",
                "connected": "1",
                "connecting": "0",
                "cumulative_setup_failed": "0",
                "cumulative_setup_initiated": "1",
                "cumulative_setup_succeeded": "1",
                "cumulative_teardown_failed": "0",
                "cumulative_teardown_succeeded": "0",
                "device_group": "Range 1/25/1 2 False",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_resp_rx": "0",
                "echo_resp_tx": "0",
                "idle": "0",
                "incoming_call_connected_rx": "0",
                "incoming_call_connected_tx": "0",
                "incoming_call_reply_rx": "0",
                "incoming_call_reply_tx": "0",
                "incoming_call_request_rx": "0",
                "incoming_call_request_tx": "0",
                "interfaces_in_chap_negotiation": "0",
                "interfaces_in_ipcp_negotiation": "0",
                "interfaces_in_ipv6cp_negotiation": "0",
                "interfaces_in_lcp_negotiation": "0",
                "interfaces_in_pap_negotiation": "0",
                "interfaces_in_ppp_negotiation": "0",
                "interfaces_in_pppoe_l2tp_negotiation": "0",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "1",
                "ipcp_cfg_nak_tx": "0",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "1",
                "ipcp_cfg_req_tx": "2",
                "ipv6cp_avg_time": "0.00",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_max_time": "0",
                "ipv6cp_min_time": "0",
                "ipv6cp_router_adv_rx": "0",
                "lcp_avg_latency": "23071.00",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_max_latency": "23071",
                "lcp_min_latency": "23071",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "ncp_avg_latency": "6248.00",
                "ncp_max_latency": "6248",
                "ncp_min_latency": "6248",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "num_sessions": "1",
                "padi_timeout": "0",
                "padi_tx": "1",
                "pado_rx": "1",
                "padr_timeout": "0",
                "padr_tx": "1",
                "pads_rx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "ppp_total_bytes_rx": "147",
                "ppp_total_bytes_tx": "92",
                "pppoe_avg_latency": "52893.00",
                "pppoe_max_latency": "52893",
                "pppoe_min_latency": "52893",
                "pppoe_total_bytes_rx": "36",
                "pppoe_total_bytes_tx": "20",
                "sessions_down": "0",
                "sessions_failed": "0",
                "sessions_initiated": "0",
                "sessions_up": "1",
                "set_link_info_rx": "0",
                "set_link_info_tx": "0",
                "teardown_failed": "0",
                "teardown_succeded": "0",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0"
            }
        },
        "aggregate": {
            "auth_avg_time": "6303.00",
            "auth_max_time": "6303",
            "auth_min_time": "6303",
            "avg_setum_rate": "1.00",
            "avg_setup_time": "88601.00",
            "avg_teardown_rate": "0.00",
            "call_disconnect_notifiy_rx": "0",
            "call_disconnect_notifiy_tx": "0",
            "chap_auth_chal_rx": "1",
            "chap_auth_fail_rx": "0",
            "chap_auth_rsp_tx": "1",
            "chap_auth_succ_rx": "1",
            "code_rej_rx": "0",
            "code_rej_tx": "0",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "cumulative_setup_failed": "0",
            "cumulative_setup_initiated": "1",
            "cumulative_setup_succeeded": "1",
            "cumulative_teardown_failed": "0",
            "cumulative_teardown_succeeded": "0",
            "device_group": "Range 1/25/1 2 False",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_resp_rx": "0",
            "echo_resp_tx": "0",
            "idle": "0",
            "incoming_call_connected_rx": "0",
            "incoming_call_connected_tx": "0",
            "incoming_call_reply_rx": "0",
            "incoming_call_reply_tx": "0",
            "incoming_call_request_rx": "0",
            "incoming_call_request_tx": "0",
            "interfaces_in_chap_negotiation": "0",
            "interfaces_in_ipcp_negotiation": "0",
            "interfaces_in_ipv6cp_negotiation": "0",
            "interfaces_in_lcp_negotiation": "0",
            "interfaces_in_pap_negotiation": "0",
            "interfaces_in_ppp_negotiation": "0",
            "interfaces_in_pppoe_l2tp_negotiation": "0",
            "ipcp_cfg_ack_rx": "1",
            "ipcp_cfg_ack_tx": "1",
            "ipcp_cfg_nak_rx": "1",
            "ipcp_cfg_nak_tx": "0",
            "ipcp_cfg_rej_rx": "0",
            "ipcp_cfg_rej_tx": "0",
            "ipcp_cfg_req_rx": "1",
            "ipcp_cfg_req_tx": "2",
            "ipv6cp_avg_time": "0.00",
            "ipv6cp_cfg_ack_rx": "0",
            "ipv6cp_cfg_ack_tx": "0",
            "ipv6cp_cfg_nak_rx": "0",
            "ipv6cp_cfg_nak_tx": "0",
            "ipv6cp_cfg_rej_rx": "0",
            "ipv6cp_cfg_rej_tx": "0",
            "ipv6cp_cfg_req_rx": "0",
            "ipv6cp_cfg_req_tx": "0",
            "ipv6cp_max_time": "0",
            "ipv6cp_min_time": "0",
            "ipv6cp_router_adv_rx": "0",
            "lcp_avg_latency": "23071.00",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "lcp_max_latency": "23071",
            "lcp_min_latency": "23071",
            "lcp_protocol_rej_rx": "0",
            "lcp_protocol_rej_tx": "0",
            "lcp_total_msg_rx": "2",
            "lcp_total_msg_tx": "2",
            "ncp_avg_latency": "6248.00",
            "ncp_max_latency": "6248",
            "ncp_min_latency": "6248",
            "ncp_total_msg_rx": "3",
            "ncp_total_msg_tx": "3",
            "num_sessions": "1",
            "padi_timeout": "0",
            "padi_tx": "1",
            "pado_rx": "1",
            "padr_timeout": "0",
            "padr_tx": "1",
            "pads_rx": "1",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_rx": "0",
            "pap_auth_nak_rx": "0",
            "pap_auth_req_tx": "0",
            "ppp_total_bytes_rx": "147",
            "ppp_total_bytes_tx": "92",
            "pppoe_avg_latency": "52893.00",
            "pppoe_max_latency": "52893",
            "pppoe_min_latency": "52893",
            "pppoe_total_bytes_rx": "36",
            "pppoe_total_bytes_tx": "20",
            "sessions_down": "0",
            "sessions_failed": "0",
            "sessions_initiated": "0",
            "sessions_up": "1",
            "set_link_info_rx": "0",
            "set_link_info_tx": "0",
            "teardown_failed": "0",
            "teardown_succeded": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "session": {
            "/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1/item:1": {
                "ac_cookie": "",
                "ac_cookie_tag_rx": "0",
                "ac_generic_error": "False",
                "ac_mac_addr": "00:11:01:00:00:01",
                "ac_name": "ixia",
                "ac_offer_rx": "1",
                "ac_system_error": "False",
                "ac_system_error_tag_rx": "0",
                "auth_establishment_time": "6303",
                "auth_id": "user",
                "auth_password": "secret",
                "auth_protocol_rx": "CHAP",
                "auth_protocol_tx": "None",
                "auth_total_rx": "2",
                "auth_total_tx": "1",
                "call_state": "Idle",
                "cdn_rx": "0",
                "cdn_tx": "0",
                "chap_auth_chal_rx": "1",
                "chap_auth_fail_rx": "0",
                "chap_auth_role": "Peer",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "cumulative_setup_failed": "0",
                "cumulative_setup_initiated": "1",
                "cumulative_setup_succeeded": "1",
                "cumulative_teardown_failed": "0",
                "cumulative_teardown_succeeded": "0",
                "data_ns": "0",
                "destination_ip": "0.0.0.0",
                "destination_port": "0",
                "device_group": "Range 1/25/1 2 False",
                "device_id": "1",
                "dns_server_list": "Not Available",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_resp_rx": "0",
                "echo_resp_tx": "0",
                "establishment_time": "88601",
                "gateway_ip": "0.0.0.0",
                "generic_error_tag_tx": "0",
                "host_mac_addr": "00:11:02:00:00:01",
                "host_name": "Not Available",
                "host_uniq": "",
                "iccn_rx": "0",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "0",
                "ip_cpe_establishment_time": "6248",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "1",
                "ipcp_cfg_nak_tx": "0",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "1",
                "ipcp_cfg_req_tx": "2",
                "ipcp_state": "NCP Open",
                "ipv6_addr": "0:0:0:0:0:0:0:0",
                "ipv6_cpe_establishment_time": "0",
                "ipv6_prefix_len": "0",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_router_adv_rx": "0",
                "ipv6cp_state": "NCP Disable",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_establishment_time": "23071",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "local_ip_addr": "1.1.1.2",
                "local_ipv6_iid": "Not Available",
                "loopback_detected": "False",
                "magic_no_negotiated": "True",
                "magic_no_rx": "3769293702",
                "magic_no_tx": "771179460",
                "mru": "1500",
                "mtu": "1500",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "negotiation_end_ms": "534097804",
                "negotiation_start_ms": "534009203",
                "our_call_id": "0",
                "our_cookie": "Not Available",
                "our_cookie_length": "0",
                "our_peer_id": "0",
                "our_tunnel_id": "0",
                "padi_timeout": "0",
                "padi_tx": "1",
                "pado_rx": "1",
                "padr_timeout": "0",
                "padr_tx": "1",
                "pads_rx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "peer_call_id": "0",
                "peer_ipv6_iid": "Not Available",
                "peer_tunnel_id": "0",
                "ppp_close_mode": "None",
                "ppp_state": "PPP Connected",
                "ppp_total_rx": "147",
                "ppp_total_tx": "92",
                "pppoe_latency": "52893",
                "pppoe_state": "Session",
                "pppoe_total_bytes_rx": "36",
                "pppoe_total_bytes_tx": "20",
                "primary_wins_server": "0.0.0.0",
                "protocol": "PPPoX Client 1",
                "relay_session_id_tag_rx": "0",
                "remote_ip_addr": "1.1.1.1",
                "secondary_wins_server": "0.0.0.0",
                "service_name": "",
                "service_name_error_tag_rx": "0",
                "session_id": "1",
                "source_ip": "0.0.0.0",
                "source_port": "0",
                "status": "up",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "topology": "T 1/25/1",
                "tunnel_state": "Tunnel Idle",
                "vendor_specific_tag_rx": "0"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "aggregate"
        "session"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    args = get_arg_value(rt_handle, j_pppox_stats.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'aggregate'
        stats.update(rt_handle.invoke('pppox_stats', **args))
        args['mode'] = 'session'
        stats.update(rt_handle.invoke('pppox_stats', **args))
        args['mode'] = 'session_dhcpv6pd'
        stats.update(rt_handle.invoke('pppox_stats', **args))
        if 'session' in stats:
            for key in list(stats['session']):
                stats['session'][args['handle']] = stats['session'][key]
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                ret[index]['aggregate'] = ret[index][key]['aggregate']
    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_test_control(rt_handle, action):
    """
    :param rt_handle:       RT object
    :param action
    :return response from rt_handle.invoke(<parameters>)

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    if action == 'start_all_protocols' or action == 'stop_all_protocols':
        args['action'] = action
    else:
        raise Exception("Error: {0} is not supported in Spirent".format(action))
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    ret = rt_handle.invoke('test_control', **args)

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret


def j_traffic_config(rt_handle, **kwargs):
    """
    :param rt_handle:       RT object
    :param arp_dst_hw_addr
    :param arp_dst_hw_count
    :param arp_dst_hw_mode - <fixed|increment|decrement>
    :param arp_operation - <arpRequest|arpReply|rarpRequest|rarpReply>
    :param arp_src_hw_addr
    :param arp_src_hw_count
    :param arp_src_hw_mode - <fixed|increment|decrement>
    :param bidirectional
    :param burst_loop_count
    :param emulation_dst_handle
    :param emulation_src_handle
    :param frame_size
    :param frame_size_max
    :param frame_size_min
    :param frame_size_step
    :param icmp_checksum
    :param icmp_code
    :param icmp_id
    :param icmp_seq
    :param icmp_type
    :param igmp_group_addr
    :param igmp_group_count
    :param igmp_group_mode
    :param igmp_group_step
    :param igmp_max_response_time
    :param igmp_msg_type
    :param igmp_multicast_src
    :param igmp_qqic
    :param igmp_qrv
    :param igmp_s_flag
    :param igmp_type
    :param igmp_version
    :param inner_ip_dst_addr
    :param inner_ip_dst_count
    :param inner_ip_dst_mode
    :param inner_ip_dst_step
    :param inner_ip_src_addr
    :param inner_ip_src_count
    :param inner_ip_src_mode
    :param inner_ip_src_step
    :param inter_stream_gap
    :param ip_checksum
    :param ip_dscp
    :param ip_dscp_count
    :param ip_dscp_step
    :param ip_dst_addr
    :param ip_dst_count
    :param ip_dst_mode
    :param ip_dst_step
    :param ip_fragment
    :param ip_fragment_offset
    :param ip_fragment_last
    :param ip_hdr_length
    :param ip_id
    :param ip_precedence
    :param ip_precedence_count
    :param ip_precedence_step
    :param ip_protocol
    :param ip_src_addr
    :param ip_src_count
    :param ip_src_mode
    :param ip_src_step
    :param ip_ttl
    :param ipv6_auth_payload_len
    :param ipv6_auth_seq_num
    :param ipv6_auth_spi
    :param ipv6_auth_string
    :param ipv6_dst_addr
    :param ipv6_dst_count
    :param ipv6_dst_mode - <fixed|random|increment|decrement>
    :param ipv6_dst_step
    :param ipv6_extension_header
    :param ipv6_frag_id
    :param ipv6_frag_more_flag
    :param ipv6_frag_offset
    :param ipv6_hop_by_hop_options
    :param ipv6_hop_limit
    :param ipv6_next_header
    :param ipv6_next_header_mode
    :param ipv6_next_header_count
    :param ipv6_next_header_step
    :param ipv6_routing_node_list
    :param ipv6_routing_res
    :param ipv6_src_addr
    :param ipv6_src_count
    :param ipv6_src_mode - <fixed|random|increment|decrement>
    :param ipv6_src_step
    :param ipv6_traffic_class
    :param l2_encap
    :param l3_imix1_ratio
    :param l3_imix1_size
    :param l3_imix2_ratio
    :param l3_imix2_size
    :param l3_imix3_ratio
    :param l3_imix3_size
    :param l3_imix4_ratio
    :param l3_imix4_size
    :param l3_length
    :param l3_length_max
    :param l3_length_min
    :param l3_protocol
    :param l4_protocol
    :param length_mode
    :param mac_dst
    :param mac_dst2
    :param mac_dst_count
    :param mac_dst_mode
    :param mac_dst_step
    :param mac_src
    :param mac_src2
    :param mac_src_count
    :param mac_src_mode
    :param mac_src_step
    :param mode - <create|modify|remove|enable|disable|reset|append_header>
    :param mpls_bottom_stack_bit
    :param mpls_labels
    :param mpls_labels_count
    :param mpls_labels_mode
    :param mpls_labels_step
    :param mpls_ttl
    :param mpls_exp_bit
    :param name
    :param pkts_per_burst
    :param port_handle
    :param port_handle2
    :param rate_bps
    :param rate_percent
    :param rate_pps
    :param stream_id
    :param tcp_ack_flag
    :param tcp_ack_num
    :param tcp_checksum
    :param tcp_data_offset
    :param tcp_dst_port_count
    :param tcp_dst_port_mode - <increment:incr|decrement:decr>
    :param tcp_dst_port_step
    :param tcp_fin_flag
    :param tcp_psh_flag
    :param tcp_reserved
    :param tcp_rst_flag
    :param tcp_seq_num
    :param tcp_src_port
    :param tcp_src_port_count
    :param tcp_src_port_mode - <increment:incr|decrement:decr>
    :param tcp_src_port_step
    :param tcp_syn_flag
    :param tcp_urg_flag
    :param tcp_urgent_ptr
    :param tcp_window
    :param transmit_mode
    :param udp_checksum
    :param udp_dst_port
    :param udp_dst_port_count
    :param udp_dst_port_mode - <increment:incr|decrement:decr>
    :param udp_dst_port_step
    :param udp_src_port
    :param udp_src_port_count
    :param udp_src_port_mode - <increment:incr|decrement:decr>
    :param udp_src_port_step
    :param vci
    :param vci_count
    :param vci_step
    :param vlan_cfi
    :param vlan_id
    :param vlan_id_count
    :param vlan_id_mode
    :param vlan_id_step
    :param vlan_user_priority
    :param vpi
    :param vpi_count
    :param vpi_step
    :param emulation_multicast_dst_handle
    :param emulation_multicast_dst_handle_type
    :param tcp_dst_port
    :param ip_precedence_mode - <increment:incr|decrement:decr> # random and shuffle is not supported in Ixia
    :param rate_mbps
    :param arp_dst_protocol_addr
    :param arp_dst_protocol_addr_count
    :param arp_dst_protocol_addr_mode
    :param arp_dst_protocol_addr_step
    :param arp_src_protocol_addr
    :param arp_src_protocol_addr_count
    :param arp_src_protocol_addr_mode
    :param arp_src_protocol_addr_step
    :param fcs_error
    :param icmpv6_type
    :param icmpv6_pointer
    :param icmpv6_target_address
    :param icmpv6_oflag
    :param icmpv6_rflag
    :param icmpv6_sflag
    :param icmpv6_suppress_flag
    :param icmpv6_max_resp_delay
    :param icmpv6_mcast_addr
    :param icmpv6_prefix_option_valid_lifetime
    :param icmpv6_dest_address
    :param icmpv6_qqic
    :param icmpv6_qrv
    :param icmpv6_code
    :param high_speed_result_analysis
    :param enable_stream
    :param ipv4_header_options
    :param ipv4_router_alert
    :param ipv4_nop
    :param ipv4_loose_source_route
    :param ipv4_strict_source_route
    :param ipv4_record_route
    :param arp_dst_hw_step
    :param arp_protocol_addr_length
    :param arp_src_hw_step
    :param data_pattern
    :param data_pattern_mode - <constant:fixed|incr:incr_byte|decr:decr_byte>
    :param ether_type
    :param ether_type_mode
    :param ether_type_count
    :param ether_type_step
    :param global_dest_mac_retry_count
    :param global_dest_mac_retry_delay
    :param global_enable_dest_mac_retry - <1>
    :param global_enable_mac_change_on_fly
    :param ip_cost
    :param ip_delay
    :param ip_dscp_mode
    :param gre_key_enable
    :param gre_key
    :param gre_seq_enable
    :param gre_seq_number
    :param gre_checksum_enable
    :param gre_checksum
    :param gre_reserved1
    :param gre_version
    :param l3_outer_protocol
    :param vlan_protocol_tag_id
    :param vlan_protocol_tag_id_mode
    :param vlan_protocol_tag_id_count
    :param vlan_protocol_tag_id_step
    :param tcp_cwr_flag
    :param tcp_cwr_flag_mode
    :param tcp_ecn_echo_flag
    :param tcp_ecn_echo_flag_mode
    :param tcp_fin_flag_mode
    :param tcp_psh_flag_mode
    :param tcp_reserved_mode
    :param tcp_reserved_count
    :param tcp_reserved_step
    :param vlan_user_priority_count
    :param vlan_user_priority_mode - <fixed|increment:incr|decrement:decr>
    :param vlan_user_priority_step
    :param ip_reliability
    :param ip_throughput
    :param tcp_ack_flag_mode
    :param tcp_ack_num_mode
    :param tcp_ack_num_count
    :param tcp_ack_num_step
    :param tcp_rst_flag_mode
    :param tcp_seq_num_mode
    :param tcp_syn_flag_mode
    :param tcp_urg_flag_mode
    :param tcp_urgent_ptr_mode
    :param tcp_urgent_ptr_count
    :param tcp_urgent_ptr_step
    :param tcp_window_mode
    :param tcp_window_count
    :param tcp_window_step
    :param vlan_cfi_mode
    :param vlan_cfi_count
    :param vlan_cfi_step
    :param ipv6_flow_label
    :param disable_signature
    :param ip_dst_outer_addr
    :param ip_dst_outer_count
    :param ip_outer_dscp
    :param ip_outer_dscp_count
    :param ip_outer_dscp_step
    :param ip_dst_outer_mode
    :param ip_dst_outer_step
    :param ip_fragment_outer_offset
    :param ip_hdr_outer_length
    :param ip_outer_checksum
    :param ip_outer_ttl
    :param ip_outer_id
    :param ip_outer_protocol
    :param ip_outer_precedence
    :param ip_outer_precedence_mode
    :param ip_outer_precedence_count
    :param ip_outer_precedence_step
    :param ip_src_outer_addr
    :param ip_src_outer_count
    :param ip_src_outer_mode
    :param ip_src_outer_step
    :param ipv6_dst_outer_count
    :param ipv6_dst_outer_mode
    :param ipv6_dst_outer_step
    :param ipv6_src_outer_count
    :param ipv6_src_outer_mode
    :param ipv6_src_outer_step
    :param ipv6_outer_src_addr
    :param ipv6_outer_dst_addr
    :param ipv6_outer_hop_limit
    :param ipv6_outer_traffic_class
    :param ipv6_outer_next_header
    :param ipv6_outer_flow_label
    :param ether_type_tracking
    :param ip_precedence_tracking
    :param tcp_ack_num_tracking
    :param tcp_cwr_flag_tracking
    :param tcp_dst_port_tracking
    :param tcp_ecn_echo_flag_tracking
    :param tcp_fin_flag_tracking
    :param tcp_psh_flag_tracking
    :param tcp_reserved_tracking
    :param tcp_rst_flag_tracking
    :param tcp_seq_num_tracking
    :param tcp_src_port_tracking
    :param tcp_syn_flag_tracking
    :param tcp_urg_flag_tracking
    :param tcp_urgent_ptr_tracking
    :param vlan_id_tracking
    :param vlan_cfi_tracking
    :param vlan_protocol_tag_id_tracking
    :param tcp_window_tracking
    :param udp_dst_port_tracking
    :param udp_src_port_tracking
    :param tx_delay
    :param vlan_user_priority_tracking
    :param arp_hw_address_length
    :param arp_hw_address_length_mode
    :param arp_operation_mode
    :param arp_protocol_addr_length_mode
    :param ip_cost_tracking
    :param ip_delay_tracking
    :param ip_dst_tracking
    :param arp_hw_address_length_count
    :param arp_hw_address_length_step
    :param arp_protocol_addr_length_count
    :param arp_protocol_addr_length_step
    :param ip_fragment_last_mode
    :param ip_fragment_last_tracking
    :param ip_fragment_offset_mode
    :param ip_fragment_offset_tracking
    :param ip_id_mode
    :param ip_id_tracking
    :param src_dest_mesh
    :param tcp_ack_flag_tracking
    :param ip_protocol_mode
    :param ip_protocol_tracking
    :param ip_reliability_tracking
    :param ip_reserved
    :param ip_reserved_tracking
    :param ip_src_tracking
    :param ip_throughput_tracking
    :param ip_ttl_mode
    :param ip_ttl_tracking
    :param ipv6_dst_tracking
    :param ipv6_flow_label_mode
    :param ipv6_flow_label_tracking
    :param ipv6_hop_limit_mode
    :param ipv6_hop_limit_tracking
    :param ipv6_src_tracking
    :param ipv6_traffic_class_count
    :param ipv6_traffic_class_mode
    :param ipv6_traffic_class_step
    :param ipv6_traffic_class_tracking
    :param mac_dst_tracking
    :param mac_src_tracking
    :param ip_fragment_offset_count
    :param ip_fragment_offset_step
    :param ip_id_count
    :param ip_id_step
    :param ip_protocol_count
    :param ip_protocol_step
    :param ip_ttl_count
    :param ip_ttl_step
    :param ipv6_flow_label_count
    :param ipv6_flow_label_step
    :param ipv6_hop_limit_count
    :param ipv6_hop_limit_step
    :param mac_src_tracking
    :param ip_fragment_offset_count
    :param ip_fragment_offset_step
    :param ip_id_count
    :param ip_id_step
    :param ip_protocol_count
    :param ip_protocol_step
    :param ip_ttl_count
    :param ip_ttl_step
    :param ipv6_flow_label_count
    :param ipv6_flow_label_step
    :param ipv6_hop_limit_count
    :param ipv6_hop_limit_step
    :param custom_pattern
    :param ipv6_srcprefix
    :param ipv6_dstprefix
    :param ip_dscp_tracking
    :param mac_discovery_gw
    :param mac_discovery_gw_step
    :param icmpv6_link_layer_type
    :param icmpv6_link_layer_value
    :param icmpv6_link_layer_length
    :param icmpv6_prefix_option_prefix
    :param icmpv6_prefix_option_length
    :param icmpv6_prefix_option_prefix_len
    :param icmpv6_prefix_option_abit
    :param icmpv6_prefix_option_lbit
    :param icmpv6_prefix_option_preferred_lifetime
    :param icmpv6_prefix_option_reserved1
    :param icmpv6_prefix_option_reserved2
    :param icmpv6_prefix_option_type
    :param icmpv6_prefix_option_valid_lifetime
    :param icmpv6_mtu_option_mtu
    :param icmpv6_mtu_option_type
    :param icmpv6_mtu_option_length
    :param icmpv6_mtu_option_reserved
    :param icmpv6_ip_hop_limit
    :param icmpv6_redirect_hdr_type
    :param icmpv6_redirect_hdr_length
    :param icmpv6_redirect_hdr_reserved1
    :param icmpv6_redirect_hdr_reserved2
    :param frame_rate_distribution_port
    :param route_mesh - <fully|one_to_one>
    :param ethernet_pause
    :param l4_ip_dst_addr
    :param l4_ip_src_addr
    :param field_linked_to
    :param field_linked
    :param frame_rate_distribution_stream - <apply_to_all>
    :param dhcp_msg_header_type
    :param dhcp_cli_msg_client_addr
    :param dhcp_cli_msg_your_addr
    :param dhcp_cli_msg_cli_hw_client_hwa
    :param dhcp_cli_msg_type_code
    :param dhcp_cli_msg_hops
    :param dhcp_cli_msg_req_addr
    :param dhcp_srv_msg_type_code
    :param dhcp_srv_msg_next_serv_addr
    :param gtp
    :param gtp_protocol_type
    :param gtp_extended_header
    :param gtp_seq_num_flag
    :param gtp_n_pdu_flag
    :param gtp_message_type
    :param gtp_te_id
    :param start_protocol - <0|1>
    :param gtp_te_id_count
    :param gtp_te_id_step
    :param icmpv6_cur_hoplimit
    :param icmpv6_mbit
    :param icmpv6_obit
    :param icmpv6_reachable_time
    :param icmpv6_retrans_time
    :param icmpv6_router_lifetime
    :param router_adv_reserved
    :param qos_type
    :param qos_value
    :param qos_value_mode
    :param tx_port_sending_traffic_to_self_en - <true:1|false:0>
    :param ip_ecn - <00|01|10|11>
    :param disable_flow_tracking

    Spirent Returns:
    {
        "status": "1",
        "stream_handles": [
            "streamblock1",
            "streamblock2"
        ],
        "stream_id": {
            "port1": "streamblock2",
            "port2": "streamblock1"
        }
    }


    IXIA Returns:
    {
        "::ixNet::OBJ-/traffic/trafficItem:1/configElement:1": {
            "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1": {
                "headers": "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:\"ethernet-1\" \
                ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:\"ipv4-2\" ::ixNet::OBJ-/traffic/
                trafficItem:1/highLevelStream:1/stack:\"fcs-3\""
            },
            "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:2": {
                "headers": "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:2/stack:\"ethernet-1\" \
                ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:2/stack:\"ipv4-2\" ::ixNet::OBJ-/traffic/
                trafficItem:1/highLevelStream:2/stack:\"fcs-3\""
            },
            "encapsulation_name": "Ethernet.IPv4",
            "endpoint_set_id": "1",
            "headers": "::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:\"ethernet-1\" \
            ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:\"ipv4-2\" ::ixNet::OBJ-/traffic/
            trafficItem:1/configElement:1/stack:\"fcs-3\"",
            "stream_ids": "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1 \
            ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:2"
        },
        "log": "",
        "status": "1",
        "stream_handles": [
            "TI0-HLTAPI_TRAFFICITEM_540"
        ],
        "stream_id": "TI0-HLTAPI_TRAFFICITEM_540",
        "traffic_item": "::ixNet::OBJ-/traffic/trafficItem:1/configElement:1"
    }

    Common Return Keys:
        "status"
        "stream_handles"
        "stream_id"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    kwargs = get_arg_value(rt_handle, j_traffic_config.__doc__, **kwargs)
    if kwargs.get('mode') == 'remove' or kwargs.get('mode') == 'disable' or kwargs.get('mode') == 'enable':
        return remove_or_disable_traffic(rt_handle, **kwargs)
    if kwargs.get('mode') == 'modify' and (kwargs.get('field_linked') != None or kwargs.get('field_linked_to') != None):
        field_value = list([kwargs.get('field_linked')]) if isinstance(kwargs.get('field_linked'), str) else kwargs.get('field_linked')
        if any('/stackLink:' in field for field in field_value):
            kwargs['field_linked'] = process_field_link_handle(rt_handle, kwargs.get('stream_id'), kwargs.get('field_linked'))
        field_value = list([kwargs.get('field_linked_to')]) if isinstance(kwargs.get('field_linked_to'), str) else kwargs.get('field_linked_to')
        if any('/stackLink:' in field for field in field_value):
            kwargs['field_linked_to'] = process_field_link_handle(rt_handle, kwargs.get('stream_id'), kwargs.get('field_linked_to'))
    args_dt = dict()
    args_dt['arp_dst_hw_addr'] = 'arp_dst_hw_addr'
    args_dt['arp_dst_hw_count'] = 'arp_dst_hw_count'
    args_dt['arp_dst_hw_mode'] = 'arp_dst_hw_mode'
    args_dt['arp_operation'] = 'arp_operation'
    args_dt['arp_src_hw_addr'] = 'arp_src_hw_addr'
    args_dt['arp_src_hw_count'] = 'arp_src_hw_count'
    args_dt['arp_src_hw_mode'] = 'arp_src_hw_mode'
    args_dt['bidirectional'] = 'bidirectional'
    args_dt['burst_loop_count'] = 'burst_loop_count'
    args_dt['emulation_dst_handle'] = 'emulation_dst_handle'
    args_dt['emulation_src_handle'] = 'emulation_src_handle'
    args_dt['frame_size'] = 'frame_size'
    args_dt['frame_size_max'] = 'frame_size_max'
    args_dt['frame_size_min'] = 'frame_size_min'
    args_dt['frame_size_step'] = 'frame_size_step'
    args_dt['icmp_checksum'] = 'icmp_checksum'
    args_dt['icmp_code'] = 'icmp_code'
    args_dt['icmp_id'] = 'icmp_id'
    args_dt['icmp_seq'] = 'icmp_seq'
    args_dt['icmp_type'] = 'icmp_type'
    args_dt['igmp_group_addr'] = 'igmp_group_addr'
    args_dt['igmp_group_count'] = 'igmp_group_count'
    args_dt['igmp_group_mode'] = 'igmp_group_mode'
    args_dt['igmp_group_step'] = 'igmp_group_step'
    args_dt['igmp_max_response_time'] = 'igmp_max_response_time'
    args_dt['igmp_msg_type'] = 'igmp_msg_type'
    args_dt['igmp_multicast_src'] = 'igmp_multicast_src'
    args_dt['igmp_qqic'] = 'igmp_qqic'
    args_dt['igmp_qrv'] = 'igmp_qrv'
    args_dt['igmp_s_flag'] = 'igmp_s_flag'
    args_dt['igmp_type'] = 'igmp_type'
    args_dt['igmp_version'] = 'igmp_version'
    args_dt['inner_ip_dst_addr'] = 'inner_ip_dst_addr'
    args_dt['inner_ip_dst_count'] = 'inner_ip_dst_count'
    args_dt['inner_ip_dst_mode'] = 'inner_ip_dst_mode'
    args_dt['inner_ip_dst_step'] = 'inner_ip_dst_step'
    args_dt['inner_ip_src_addr'] = 'inner_ip_src_addr'
    args_dt['inner_ip_src_count'] = 'inner_ip_src_count'
    args_dt['inner_ip_src_mode'] = 'inner_ip_src_mode'
    args_dt['inner_ip_src_step'] = 'inner_ip_src_step'
    args_dt['inter_stream_gap'] = 'inter_stream_gap'
    args_dt['ip_checksum'] = 'ip_checksum'
    args_dt['ip_dscp'] = 'ip_dscp'
    args_dt['ip_dscp_count'] = 'ip_dscp_count'
    args_dt['ip_dscp_step'] = 'ip_dscp_step'
    args_dt['ip_dst_addr'] = 'ip_dst_addr'
    args_dt['ip_dst_count'] = 'ip_dst_count'
    args_dt['ip_dst_mode'] = 'ip_dst_mode'
    args_dt['ip_dst_step'] = 'ip_dst_step'
    args_dt['ip_fragment'] = 'ip_fragment'
    args_dt['ip_fragment_offset'] = 'ip_fragment_offset'
    args_dt['ip_fragment_last'] = 'ip_fragment_last'
    args_dt['ip_hdr_length'] = 'ip_hdr_length'
    args_dt['ip_id'] = 'ip_id'
    args_dt['ip_precedence'] = 'ip_precedence'
    args_dt['ip_precedence_count'] = 'ip_precedence_count'
    args_dt['ip_precedence_step'] = 'ip_precedence_step'
    args_dt['ip_protocol'] = 'ip_protocol'
    args_dt['ip_src_addr'] = 'ip_src_addr'
    args_dt['ip_src_count'] = 'ip_src_count'
    args_dt['ip_src_mode'] = 'ip_src_mode'
    args_dt['ip_src_step'] = 'ip_src_step'
    args_dt['ip_ttl'] = 'ip_ttl'
    args_dt['ipv6_auth_payload_len'] = 'ipv6_auth_payload_len'
    args_dt['ipv6_auth_seq_num'] = 'ipv6_auth_seq_num'
    args_dt['ipv6_auth_spi'] = 'ipv6_auth_spi'
    args_dt['ipv6_auth_string'] = 'ipv6_auth_md5sha1_string'
    args_dt['ipv6_dst_addr'] = 'ipv6_dst_addr'
    args_dt['ipv6_dst_count'] = 'ipv6_dst_count'
    args_dt['ipv6_dst_mode'] = 'ipv6_dst_mode'
    args_dt['ipv6_dst_step'] = 'ipv6_dst_step'
    args_dt['ipv6_extension_header'] = 'ipv6_extension_header'
    args_dt['ipv6_frag_id'] = 'ipv6_frag_id'
    args_dt['ipv6_frag_more_flag'] = 'ipv6_frag_more_flag'
    args_dt['ipv6_frag_offset'] = 'ipv6_frag_offset'
    args_dt['ipv6_hop_by_hop_options'] = 'ipv6_hop_by_hop_options'
    args_dt['ipv6_hop_limit'] = 'ipv6_hop_limit'
    args_dt['ipv6_next_header'] = 'ipv6_next_header'
    args_dt['ipv6_next_header_mode'] = 'ipv6_next_header_mode'
    args_dt['ipv6_next_header_count'] = 'ipv6_next_header_count'
    args_dt['ipv6_next_header_step'] = 'ipv6_next_header_step'
    args_dt['ipv6_routing_node_list'] = 'ipv6_routing_node_list'
    args_dt['ipv6_routing_res'] = 'ipv6_routing_res'
    args_dt['ipv6_src_addr'] = 'ipv6_src_addr'
    args_dt['ipv6_src_count'] = 'ipv6_src_count'
    args_dt['ipv6_src_mode'] = 'ipv6_src_mode'
    args_dt['ipv6_src_step'] = 'ipv6_src_step'
    args_dt['ipv6_traffic_class'] = 'ipv6_traffic_class'
    args_dt['l3_imix1_ratio'] = 'l3_imix1_ratio'
    args_dt['l3_imix1_size'] = 'l3_imix1_size'
    args_dt['l3_imix2_ratio'] = 'l3_imix2_ratio'
    args_dt['l3_imix2_size'] = 'l3_imix2_size'
    args_dt['l3_imix3_ratio'] = 'l3_imix3_ratio'
    args_dt['l3_imix3_size'] = 'l3_imix3_size'
    args_dt['l3_imix4_ratio'] = 'l3_imix4_ratio'
    args_dt['l3_imix4_size'] = 'l3_imix4_size'
    args_dt['l3_length'] = 'l3_length'
    args_dt['l3_length_max'] = 'l3_length_max'
    args_dt['l3_length_min'] = 'l3_length_min'
    args_dt['l3_protocol'] = 'l3_protocol'
    args_dt['length_mode'] = 'length_mode'
    args_dt['mac_dst'] = 'mac_dst'
    args_dt['mac_dst2'] = 'mac_dst2'
    args_dt['mac_dst_count'] = 'mac_dst_count'
    args_dt['mac_dst_mode'] = 'mac_dst_mode'
    args_dt['mac_dst_step'] = 'mac_dst_step'
    args_dt['mac_src'] = 'mac_src'
    args_dt['mac_src2'] = 'mac_src2'
    args_dt['mac_src_count'] = 'mac_src_count'
    args_dt['mac_src_mode'] = 'mac_src_mode'
    args_dt['mac_src_step'] = 'mac_src_step'
    args_dt['mode'] = 'mode'
    args_dt['mpls_bottom_stack_bit'] = 'mpls_bottom_stack_bit'
    args_dt['mpls_labels_count'] = 'mpls_labels_count'
    args_dt['mpls_labels_step'] = 'mpls_labels_step'
    args_dt['name'] = 'name'
    args_dt['pkts_per_burst'] = 'pkts_per_burst'
    args_dt['port_handle'] = 'port_handle'
    args_dt['port_handle2'] = 'port_handle2'
    args_dt['rate_bps'] = 'rate_bps'
    args_dt['rate_percent'] = 'rate_percent'
    args_dt['rate_pps'] = 'rate_pps'
    args_dt['stream_id'] = 'stream_id'
    args_dt['tcp_ack_flag'] = 'tcp_ack_flag'
    args_dt['tcp_ack_num'] = 'tcp_ack_num'
    args_dt['tcp_checksum'] = 'tcp_checksum'
    args_dt['tcp_data_offset'] = 'tcp_data_offset'
    args_dt['tcp_dst_port_count'] = 'tcp_dst_port_count'
    args_dt['tcp_dst_port_mode'] = 'tcp_dst_port_mode'
    args_dt['tcp_dst_port_step'] = 'tcp_dst_port_step'
    args_dt['tcp_fin_flag'] = 'tcp_fin_flag'
    args_dt['tcp_psh_flag'] = 'tcp_psh_flag'
    args_dt['tcp_reserved'] = 'tcp_reserved'
    args_dt['tcp_rst_flag'] = 'tcp_rst_flag'
    args_dt['tcp_seq_num'] = 'tcp_seq_num'
    args_dt['tcp_src_port'] = 'tcp_src_port'
    args_dt['tcp_src_port_count'] = 'tcp_src_port_count'
    args_dt['tcp_src_port_mode'] = 'tcp_src_port_mode'
    args_dt['tcp_src_port_step'] = 'tcp_src_port_step'
    args_dt['tcp_syn_flag'] = 'tcp_syn_flag'
    args_dt['tcp_urg_flag'] = 'tcp_urg_flag'
    args_dt['tcp_urgent_ptr'] = 'tcp_urgent_ptr'
    args_dt['tcp_window'] = 'tcp_window'
    args_dt['transmit_mode'] = 'transmit_mode'
    args_dt['udp_checksum'] = 'udp_checksum'
    args_dt['udp_dst_port'] = 'udp_dst_port'
    args_dt['udp_dst_port_count'] = 'udp_dst_port_count'
    args_dt['udp_dst_port_mode'] = 'udp_dst_port_mode'
    args_dt['udp_dst_port_step'] = 'udp_dst_port_step'
    args_dt['udp_src_port'] = 'udp_src_port'
    args_dt['udp_src_port_count'] = 'udp_src_port_count'
    args_dt['udp_src_port_mode'] = 'udp_src_port_mode'
    args_dt['udp_src_port_step'] = 'udp_src_port_step'
    args_dt['vci'] = 'vci'
    args_dt['vci_count'] = 'vci_count'
    args_dt['vci_step'] = 'vci_step'
    args_dt['vlan_cfi'] = 'vlan_cfi'
    args_dt['vlan_id'] = 'vlan_id'
    args_dt['vlan_id_count'] = 'vlan_id_count'
    args_dt['vlan_id_mode'] = 'vlan_id_mode'
    args_dt['vlan_id_step'] = 'vlan_id_step'
    args_dt['vlan_user_priority'] = 'vlan_user_priority'
    args_dt['vpi'] = 'vpi'
    args_dt['vpi_count'] = 'vpi_count'
    args_dt['vpi_step'] = 'vpi_step'
    args_dt['emulation_multicast_dst_handle'] = 'emulation_multicast_dst_handle'
    args_dt['emulation_multicast_dst_handle_type'] = 'emulation_multicast_dst_handle_type'
    args_dt['tcp_dst_port'] = 'tcp_dst_port'
    args_dt['ip_precedence_mode'] = 'ip_precedence_mode'
    args_dt['rate_mbps'] = 'rate_mbps'
    args_dt['arp_dst_protocol_addr'] = 'arp_dst_protocol_addr'
    args_dt['arp_dst_protocol_addr_count'] = 'arp_dst_protocol_addr_count'
    args_dt['arp_dst_protocol_addr_mode'] = 'arp_dst_protocol_addr_mode'
    args_dt['arp_dst_protocol_addr_step'] = 'arp_dst_protocol_addr_step'
    args_dt['arp_src_protocol_addr'] = 'arp_src_protocol_addr'
    args_dt['arp_src_protocol_addr_count'] = 'arp_src_protocol_addr_count'
    args_dt['arp_src_protocol_addr_mode'] = 'arp_src_protocol_addr_mode'
    args_dt['arp_src_protocol_addr_step'] = 'arp_src_protocol_addr_step'
    args_dt['arp_dst_hw_step'] = 'arp_dst_hw_step'
    args_dt['arp_protocol_addr_length'] = 'arp_protocol_addr_length'
    args_dt['arp_src_hw_step'] = 'arp_src_hw_step'
    args_dt['data_pattern'] = 'data_pattern'
    args_dt['data_pattern_mode'] = 'data_pattern_mode'
    args_dt['ether_type'] = 'ethernet_value'
    args_dt['ether_type_mode'] = 'ethernet_value_mode'
    args_dt['ether_type_count'] = 'ethernet_value_count'
    args_dt['ether_type_step'] = 'ethernet_value_step'
    args_dt['global_dest_mac_retry_count'] = 'global_dest_mac_retry_count'
    args_dt['global_dest_mac_retry_delay'] = 'global_dest_mac_retry_delay'
    args_dt['global_enable_dest_mac_retry'] = 'global_enable_dest_mac_retry'
    args_dt['global_enable_mac_change_on_fly'] = 'global_enable_mac_change_on_fly'
    args_dt['ip_cost'] = 'ip_cost'
    args_dt['ip_delay'] = 'ip_delay'
    args_dt['ip_dscp_mode'] = 'ip_dscp_mode'
    args_dt['gre_key_enable'] = 'gre_key_enable'
    args_dt['gre_key'] = 'gre_key'
    args_dt['gre_seq_enable'] = 'gre_seq_enable'
    args_dt['gre_seq_number'] = 'gre_seq_number'
    args_dt['gre_checksum_enable'] = 'gre_checksum_enable'
    args_dt['gre_checksum'] = 'gre_checksum'
    args_dt['gre_reserved1'] = 'gre_reserved1'
    args_dt['gre_version'] = 'gre_version'
    args_dt['vlan_protocol_tag_id'] = 'vlan_protocol_tag_id'
    args_dt['vlan_protocol_tag_id_mode'] = 'vlan_protocol_tag_id_mode'
    args_dt['vlan_protocol_tag_id_count'] = 'vlan_protocol_tag_id_count'
    args_dt['vlan_protocol_tag_id_step'] = 'vlan_protocol_tag_id_step'
    args_dt['tcp_cwr_flag'] = 'tcp_cwr_flag'
    args_dt['tcp_cwr_flag_mode'] = 'tcp_cwr_flag_mode'
    args_dt['tcp_ecn_echo_flag'] = 'tcp_ecn_echo_flag'
    args_dt['tcp_ecn_echo_flag_mode'] = 'tcp_ecn_echo_flag_mode'
    args_dt['tcp_fin_flag_mode'] = 'tcp_fin_flag_mode'
    args_dt['tcp_psh_flag_mode'] = 'tcp_psh_flag_mode'
    args_dt['tcp_reserved_mode'] = 'tcp_reserved_mode'
    args_dt['tcp_reserved_count'] = 'tcp_reserved_count'
    args_dt['tcp_reserved_step'] = 'tcp_reserved_step'
    args_dt['vlan_user_priority_count'] = 'vlan_user_priority_count'
    args_dt['vlan_user_priority_mode'] = 'vlan_user_priority_mode'
    args_dt['vlan_user_priority_step'] = 'vlan_user_priority_step'
    args_dt['ip_reliability'] = 'ip_reliability'
    args_dt['ip_throughput'] = 'ip_throughput'
    args_dt['tcp_ack_flag_mode'] = 'tcp_ack_flag_mode'
    args_dt['tcp_ack_num_mode'] = 'tcp_ack_num_mode'
    args_dt['tcp_ack_num_count'] = 'tcp_ack_num_count'
    args_dt['tcp_ack_num_step'] = 'tcp_ack_num_step'
    args_dt['tcp_rst_flag_mode'] = 'tcp_rst_flag_mode'
    args_dt['tcp_seq_num_mode'] = 'tcp_seq_num_mode'
    args_dt['tcp_syn_flag_mode'] = 'tcp_syn_flag_mode'
    args_dt['tcp_urg_flag_mode'] = 'tcp_urg_flag_mode'
    args_dt['tcp_urgent_ptr_mode'] = 'tcp_urgent_ptr_mode'
    args_dt['tcp_urgent_ptr_count'] = 'tcp_urgent_ptr_count'
    args_dt['tcp_urgent_ptr_step'] = 'tcp_urgent_ptr_step'
    args_dt['tcp_window_mode'] = 'tcp_window_mode'
    args_dt['tcp_window_count'] = 'tcp_window_count'
    args_dt['tcp_window_step'] = 'tcp_window_step'
    args_dt['vlan_cfi_mode'] = 'vlan_cfi_mode'
    args_dt['vlan_cfi_count'] = 'vlan_cfi_count'
    args_dt['vlan_cfi_step'] = 'vlan_cfi_step'
    args_dt['ipv6_flow_label'] = 'ipv6_flow_label'
    args_dt['disable_signature'] = 'frame_sequencing'
    args_dt['ether_type_tracking'] = 'ethernet_value_tracking'
    args_dt['ip_precedence_tracking'] = 'ip_precedence_tracking'
    args_dt['tcp_ack_num_tracking'] = 'tcp_ack_num_tracking'
    args_dt['tcp_cwr_flag_tracking'] = 'tcp_cwr_flag_tracking'
    args_dt['tcp_dst_port_tracking'] = 'tcp_dst_port_tracking'
    args_dt['tcp_ecn_echo_flag_tracking'] = 'tcp_ecn_echo_flag_tracking'
    args_dt['tcp_fin_flag_tracking'] = 'tcp_fin_flag_tracking'
    args_dt['tcp_psh_flag_tracking'] = 'tcp_psh_flag_tracking'
    args_dt['tcp_reserved_tracking'] = 'tcp_reserved_tracking'
    args_dt['tcp_rst_flag_tracking'] = 'tcp_rst_flag_tracking'
    args_dt['tcp_seq_num_tracking'] = 'tcp_seq_num_tracking'
    args_dt['tcp_src_port_tracking'] = 'tcp_src_port_tracking'
    args_dt['tcp_syn_flag_tracking'] = 'tcp_syn_flag_tracking'
    args_dt['tcp_urg_flag_tracking'] = 'tcp_urg_flag_tracking'
    args_dt['tcp_urgent_ptr_tracking'] = 'tcp_urgent_ptr_tracking'
    args_dt['vlan_id_tracking'] = 'vlan_id_tracking'
    args_dt['vlan_cfi_tracking'] = 'vlan_cfi_tracking'
    args_dt['vlan_protocol_tag_id_tracking'] = 'vlan_protocol_tag_id_tracking'
    args_dt['tcp_window_tracking'] = 'tcp_window_tracking'
    args_dt['udp_dst_port_tracking'] = 'udp_dst_port_tracking'
    args_dt['udp_src_port_tracking'] = 'udp_src_port_tracking'
    args_dt['tx_delay'] = 'tx_delay'
    args_dt['vlan_user_priority_tracking'] = 'vlan_user_priority_tracking'
    args_dt['arp_hw_address_length'] = 'arp_hw_address_length'
    args_dt['arp_hw_address_length_mode'] = 'arp_hw_address_length_mode'
    args_dt['arp_operation_mode'] = 'arp_operation_mode'
    args_dt['arp_protocol_addr_length_mode'] = 'arp_protocol_addr_length_mode'
    args_dt['ip_cost_tracking'] = 'ip_cost_tracking'
    args_dt['ip_delay_tracking'] = 'ip_delay_tracking'
    args_dt['ip_dst_tracking'] = 'ip_dst_tracking'
    args_dt['arp_hw_address_length_count'] = 'arp_hw_address_length_count'
    args_dt['arp_hw_address_length_step'] = 'arp_hw_address_length_step'
    args_dt['arp_protocol_addr_length_count'] = 'arp_protocol_addr_length_count'
    args_dt['arp_protocol_addr_length_step'] = 'arp_protocol_addr_length_step'
    args_dt['ip_fragment_last_mode'] = 'ip_fragment_last_mode'
    args_dt['ip_fragment_last_tracking'] = 'ip_fragment_last_tracking'
    args_dt['ip_fragment_offset_mode'] = 'ip_fragment_offset_mode'
    args_dt['ip_fragment_offset_tracking'] = 'ip_fragment_offset_tracking'
    args_dt['ip_id_mode'] = 'ip_id_mode'
    args_dt['ip_id_tracking'] = 'ip_id_tracking'
    args_dt['src_dest_mesh'] = 'src_dest_mesh'
    args_dt['tcp_ack_flag_tracking'] = 'tcp_ack_flag_tracking'
    args_dt['ip_protocol_mode'] = 'ip_protocol_mode'
    args_dt['ip_protocol_tracking'] = 'ip_protocol_tracking'
    args_dt['ip_reliability_tracking'] = 'ip_reliability_tracking'
    args_dt['ip_reserved'] = 'ip_reserved'
    args_dt['ip_reserved_tracking'] = 'ip_reserved_tracking'
    args_dt['ip_src_tracking'] = 'ip_src_tracking'
    args_dt['ip_throughput_tracking'] = 'ip_throughput_tracking'
    args_dt['ip_ttl_mode'] = 'ip_ttl_mode'
    args_dt['ip_ttl_tracking'] = 'ip_ttl_tracking'
    args_dt['ipv6_dst_tracking'] = 'ipv6_dst_tracking'
    args_dt['ipv6_flow_label_mode'] = 'ipv6_flow_label_mode'
    args_dt['ipv6_flow_label_tracking'] = 'ipv6_flow_label_tracking'
    args_dt['ipv6_hop_limit_mode'] = 'ipv6_hop_limit_mode'
    args_dt['ipv6_hop_limit_tracking'] = 'ipv6_hop_limit_tracking'
    args_dt['ipv6_src_tracking'] = 'ipv6_src_tracking'
    args_dt['ipv6_traffic_class_count'] = 'ipv6_traffic_class_count'
    args_dt['ipv6_traffic_class_mode'] = 'ipv6_traffic_class_mode'
    args_dt['ipv6_traffic_class_step'] = 'ipv6_traffic_class_step'
    args_dt['ipv6_traffic_class_tracking'] = 'ipv6_traffic_class_tracking'
    args_dt['mac_dst_tracking'] = 'mac_dst_tracking'
    args_dt['mac_src_tracking'] = 'mac_src_tracking'
    args_dt['ip_fragment_offset_count'] = 'ip_fragment_offset_count'
    args_dt['ip_fragment_offset_step'] = 'ip_fragment_offset_step'
    args_dt['ip_id_count'] = 'ip_id_count'
    args_dt['ip_id_step'] = 'ip_id_step'
    args_dt['ip_protocol_count'] = 'ip_protocol_count'
    args_dt['ip_protocol_step'] = 'ip_protocol_step'
    args_dt['ip_ttl_count'] = 'ip_ttl_count'
    args_dt['ip_ttl_step'] = 'ip_ttl_step'
    args_dt['ipv6_flow_label_count'] = 'ipv6_flow_label_count'
    args_dt['ipv6_flow_label_step'] = 'ipv6_flow_label_step'
    args_dt['ipv6_hop_limit_count'] = 'ipv6_hop_limit_count'
    args_dt['ipv6_hop_limit_step'] = 'ipv6_hop_limit_step'
    args_dt['mac_discovery_gw'] = 'mac_discovery_gw'
    args_dt['mac_discovery_gw_step'] = 'mac_discovery_gw_step'
    args_dt['frame_rate_distribution_port'] = 'frame_rate_distribution_port'
    args_dt['route_mesh'] = 'route_mesh'
    args_dt['frame_rate_distribution_stream'] = 'frame_rate_distribution_stream'
    args_dt['dhcp_cli_msg_client_addr'] = 'dhcp_client_ip_addr'
    args_dt['dhcp_cli_msg_your_addr'] = 'dhcp_your_ip_addr'
    args_dt['dhcp_cli_msg_cli_hw_client_hwa'] = 'dhcp_client_hw_addr'
    args_dt['dhcp_cli_msg_hops'] = 'dhcp_hops'
    args_dt['dhcp_srv_msg_next_serv_addr'] = 'dhcp_server_ip_addr'
    args_dt['disable_flow_tracking'] = 'disable_flow_tracking'

    start_protocol = 1
    if kwargs.get('start_protocol') is not None:
        start_protocol = kwargs.pop('start_protocol')
        if start_protocol in [0, '0']:
            start_protocol = 0

    args = dict()
    dhcp_list = ['dhcp_msg_header_type', 'dhcp_cli_msg_client_addr', 'dhcp_cli_msg_your_addr',
                 'dhcp_cli_msg_cli_hw_client_hwa', 'dhcp_cli_msg_type_code',
                 'dhcp_cli_msg_hops', 'dhcp_cli_msg_req_addr',
                 'dhcp_srv_msg_type_code', 'dhcp_srv_msg_next_serv_addr']

    for dhcp_arg in dhcp_list:
        if kwargs.get(dhcp_arg):
            args['l4_protocol'] = 'dhcp'
            break

    dhcp_dict = {}
    dhcp_value = {'discover': '1', 'request': '3', 'decline': '4', 'release': '7',
                  'inform': '8', 'offer': '2', 'ack': '5', 'nak': '6'}

    if kwargs.get('dhcp_msg_header_type'):
        dhcp_dict['dhcpMessageType.messageType'] = dhcp_value[kwargs.pop('dhcp_msg_header_type')]
    if kwargs.get('dhcp_cli_msg_req_addr'):
        dhcp_dict['requestedIPAddress.address'] = kwargs.pop('dhcp_cli_msg_req_addr')
    if kwargs.get('dhcp_cli_msg_type_code'):
        dhcp_dict['dhcpMessageType.messageType'] = dhcp_value[kwargs.pop('dhcp_cli_msg_type_code')]
    if kwargs.get('dhcp_srv_msg_type_code'):
        dhcp_dict['dhcpMessageType.messageType'] = dhcp_value[kwargs.pop('dhcp_srv_msg_type_code')]

    gtp_dict = {}
    gtp_incrdecr_dict = {}
    if kwargs.get('gtp') in [1, '1']:
        kwargs.pop('gtp')
        if kwargs.get('gtp_protocol_type'):
            gtp_dict['header.pt-2'] = 1 if kwargs['gtp_protocol_type'] == "gtp" else 0
            kwargs.pop('gtp_protocol_type')
        if kwargs.get('gtp_extended_header'):
            gtp_dict['header.e-4'] = kwargs.pop('gtp_extended_header')
        if kwargs.get('gtp_seq_num_flag'):
            gtp_dict['header.s-5'] = kwargs.pop('gtp_seq_num_flag')
        if kwargs.get('gtp_n_pdu_flag'):
            gtp_dict['header.n-6'] = kwargs.pop('gtp_n_pdu_flag')
        if kwargs.get('gtp_message_type'):
            gtp_dict['header.type-7'] = kwargs.pop('gtp_message_type')
        if kwargs.get('gtp_te_id'):
            if isinstance(kwargs['gtp_te_id'], int):
                gtp_dict['header.teid-9'] = str(hex(int(kwargs.pop('gtp_te_id'))))
            else:
                gtp_dict['header.teid-9'] = kwargs.pop('gtp_te_id')
        if kwargs.get('gtp_te_id_count'):
            gtp_incrdecr_dict['step_count'] = kwargs.pop('gtp_te_id_count')
        if kwargs.get('gtp_te_id_step'):
            gtp_incrdecr_dict['step'] = kwargs.pop('gtp_te_id_step')
        if gtp_incrdecr_dict:
            gtp_incrdecr_dict['start_value'] = gtp_dict['header.teid-9']
            gtp_dict['header.teid-9'] = gtp_incrdecr_dict

    if kwargs.get('field_linked_to'):
        args['field_linked_to'] = kwargs.pop('field_linked_to')
    if kwargs.get('field_linked'):
        args['field_linked'] = kwargs.pop('field_linked')

    if not kwargs.get('port_handle') and kwargs.get('mode') == 'create':
        raise Exception("Error: Please pass port_handle as it is mandatory argument for create mode")

    mpls_list = ['mpls_bottom_stack_bit', 'mpls_labels', 'mpls_labels_count', 'mpls_labels_mode', 'mpls_labels_step', 'mpls_ttl', 'mpls_exp_bit']

    for mpls_arg in mpls_list:
        if kwargs.get(mpls_arg):
            args['mpls'] = 'enable'
            break

    if kwargs.get('fcs_error'):
        args['fcs'] = kwargs.pop('fcs_error')
        if args['fcs'] in [1, '1']:
            args['fcs_type'] = 'bad_CRC'
    if kwargs.get('l2_encap'):
        args['l2_encap'] = kwargs.pop('l2_encap')
        if 'ethernet_ii_vlan' in args['l2_encap']:
            args['vlan'] = 'enable'
        elif args['l2_encap'] == 'ethernet_ii_vlan_mpls' or \
             args['l2_encap'] == 'ethernet_ii_vlan_unicast_mpls' or \
             args['l2_encap'] == 'ethernet_ii_unicast_mpls':
            args['mpls'] = 'enable'
    if kwargs.get('l4_protocol'):
        args['l4_protocol'] = kwargs.pop('l4_protocol')
        if args['l4_protocol'] == "icmpv6":
            args['l4_protocol'] = 'icmp'
        elif args['l4_protocol'] == 'gre':
            msg = '''
                'Please provide gre via l3_protocol option
                 and ipv4/6 using l3_outer_protocol options'
            '''
            raise Exception(msg)
    if kwargs.get('qos_type'):
        args['qos_type_ixn'] = kwargs.pop('qos_type')
    if kwargs.get('qos_value'):
        args['qos_value_ixn'] = kwargs.pop('qos_value')
    if kwargs.get('qos_value_mode'):
        args['qos_value_ixn_mode'] = kwargs.pop('qos_value_mode')
    if kwargs.get('ip_ecn') != None:
        value = kwargs.pop('ip_ecn')
    else:
        value = None

    if kwargs.get('ip_dscp_tracking'):
        args['ip_dscp_tracking'] = kwargs.pop('ip_dscp_tracking')
        args['qos_type_ixn'] = "dscp"
        args['qos_value_ixn'] = "dscp_default"

    if kwargs.get('tx_port_sending_traffic_to_self_en'):
        args['allow_self_destined'] = kwargs.pop('tx_port_sending_traffic_to_self_en')

    l4_protocol = '0'
    if args.get('l4_protocol') == "ipv4":
        if kwargs.get('l4_ip_src_addr'):
            args['ip_src_addr'] = kwargs.pop('l4_ip_src_addr')
        if kwargs.get('l4_ip_dst_addr'):
            args['ip_dst_addr'] = kwargs.pop('l4_ip_dst_addr')
        args['l3_protocol'] = args.pop('l4_protocol')
        l4_protocol = '1'

    outer_protocol_list = ['ip_dst_outer_addr', 'ip_dst_outer_count', 'ip_outer_dscp',\
                           'ip_outer_dscp_count', 'ip_outer_dscp_step', 'ip_dst_outer_mode',\
                           'ip_dst_outer_step', 'ip_fragment_outer_offset',\
                           'ip_hdr_outer_length', 'ip_outer_checksum', 'ip_outer_ttl',\
                           'ip_outer_id', 'ip_outer_protocol', 'ip_outer_precedence',\
                           'ip_outer_precedence_mode', 'ip_outer_precedence_count',\
                           'ip_outer_precedence_step', 'ip_src_outer_addr',
                           'ip_src_outer_count', 'ip_src_outer_mode', 'ip_src_outer_step',\
                           'ipv6_dst_outer_count', 'ipv6_dst_outer_mode',\
                           'ipv6_dst_outer_step', 'ipv6_src_outer_count', 'ipv6_src_outer_mode',\
                           'ipv6_src_outer_step', 'ipv6_outer_src_addr',\
                           'ipv6_outer_dst_addr', 'ipv6_outer_hop_limit',\
                           'ipv6_outer_traffic_class', 'ipv6_outer_next_header', 'ipv6_outer_flow_label']

    custom_pattern = kwargs.pop('custom_pattern') if kwargs.get('custom_pattern') else None
    pause = kwargs.pop('ethernet_pause') if kwargs.get('ethernet_pause') else None

    if kwargs.get('l3_protocol'):
        if kwargs['l3_protocol'] == 'gre':
            args['l4_protocol'] = kwargs.pop('l3_protocol')
        else:
            args['l3_protocol'] = kwargs.pop('l3_protocol')

    l3_outer_protocol = kwargs.get('l3_outer_protocol') if kwargs.get('l3_outer_protocol') is not None else "Dummy"
    if re.match(r'^ipv\d', l3_outer_protocol) and args.get('l3_protocol') == 'gre':
        args['l4_protocol'] = args['l3_protocol']
        args['l3_protocol'] = kwargs.pop('l3_outer_protocol')
    if kwargs.get('l3_outer_protocol'):
        args['l3_protocol'] = kwargs.pop('l3_outer_protocol')
        kwargs_list = list(kwargs.keys())
        for arg in kwargs_list:
            if arg in outer_protocol_list:
                arg_name = arg.replace('outer_', '').strip()
                args[arg_name] = kwargs.pop(arg)

    if  kwargs.get('disable_signature'):
        if kwargs.pop('disable_signature') == '1':
            args['frame_sequencing'] = 'disable'
        else:
            args['frame_sequencing'] = 'enable'

    if 'frame_size' in kwargs and 'length_mode' not in kwargs:
        args['frame_size'] = kwargs.pop('frame_size')
        args['length_mode'] = 'fixed'

    if kwargs.get('mpls_labels_mode'):
        args['mpls_labels_mode'] = kwargs.pop('mpls_labels_mode')
        if isinstance(args['mpls_labels_mode'], str):
            if re.match(r'\{\"list\"', args['mpls_labels_mode']):
                args['mpls_labels_mode'] = re.findall(r'[a-z]+', args['mpls_labels_mode'])
    if kwargs.get('mpls_labels'):
        args['mpls_labels'] = kwargs.pop('mpls_labels')
        if isinstance(args['mpls_labels'], str):
            if re.match(r'{{[\d\s]+}|{[\d\s]+}', args['mpls_labels']):
                args['mpls_labels'] = re.findall(r'{([\d\s]+)}', args['mpls_labels'])
    if kwargs.get('mpls_ttl'):
        args['mpls_ttl'] = kwargs.pop('mpls_ttl')
        if isinstance(args['mpls_ttl'], str):
            if re.match(r'{{[\d\s]+}|{[\d\s]+}', args['mpls_ttl']):
                args['mpls_ttl'] = re.findall(r'{([\d\s]+)}', args['mpls_ttl'])
    def bin_to_int(bin):
        bin_ret = list()
        if isinstance(bin, list):
            for b in bin:
                if isinstance(b, list):
                    bin_ret.append(bin_to_int(b))
                else:
                    b = str(b)
                    if len(b) == 1:
                        bin_ret.append(str(b))
                    else:
                        bin_ret.append(str(int(b, 2)))
            return bin_ret
        else:
            if len(bin) == 1:
                return str(bin)
            else:
                return str(int(bin, 2))

    if kwargs.get('mpls_exp_bit') is not None and not isinstance(kwargs.get('mpls_exp_bit'), list):
        args['mpls_exp_bit'] = str(kwargs.pop('mpls_exp_bit'))
        if re.match(r'{{([\d]+)', args['mpls_exp_bit']):
            args['mpls_exp_bit'] = re.findall(r'\{(.+)\}$', args['mpls_exp_bit'])[0].strip('{').strip('}')
            mpls_exp = args['mpls_exp_bit'].split('} {')
            args['mpls_exp_bit'] = bin_to_int([re.findall(r'(\d+)', exp) for exp in mpls_exp])
        elif re.match(r'{([\d]+)', args['mpls_exp_bit']):
            args['mpls_exp_bit'] = bin_to_int(re.findall(r'([\d]+)', args['mpls_exp_bit']))
    elif kwargs.get('mpls_exp_bit') is not None:
        args['mpls_exp_bit'] = bin_to_int(kwargs.pop('mpls_exp_bit'))

    vlan_list = ['vlan_cfi', 'vlan_id', 'vlan_id_count', 'vlan_id_mode', 'vlan_id_step',
                 'vlan_user_priority', 'vlan_protocol_tag_id', 'vlan_protocol_tag_id_mode', 'vlan_protocol_tag_id_count',
                 'vlan_protocol_tag_id_step', 'vlan_user_priority_count', 'vlan_user_priority_mode',
                 'vlan_user_priority_step', 'vlan_cfi_mode', 'vlan_cfi_count', 'vlan_cfi_step', 'vlan_id_tracking',
                 'vlan_cfi_tracking', 'vlan_protocol_tag_id_tracking', 'vlan_user_priority_tracking']

    for each_vlan_arg in vlan_list:
        if each_vlan_arg in kwargs:
            args['vlan'] = 'enable'
            break

    #----------set incr and decr mode for args---------
    def set_arg_mode(m_arg_key, m_arg_value, args):
        mode_list2 = ['ipv6_dst_mode', 'ipv6_src_mode']
        if "random" in m_arg_value or "shuffle" in m_arg_value:
            message = \
            "random and shuffle mode of {} is not supported in Ixia Tgen and setting it to increment".format(m_arg_key)
            if m_arg_key in mode_list2:
                args[m_arg_key] = 'increment'
            else:
                args[m_arg_key] = 'incr'
        elif "increment" in m_arg_value or "decrement" in m_arg_value:
            if m_arg_key not in mode_list2:
                args[m_arg_key] = m_arg_value[:4]
            else:
                args[m_arg_key] = m_arg_value
        else:
            args[m_arg_key] = m_arg_value
    mode_list = [
        'ip_precedence_mode', 'tcp_src_port_mode',
        'tcp_dst_port_mode', 'udp_src_port_mode',
        'udp_dst_port_mode', 'ipv6_dst_mode',
        'ipv6_src_mode'
    ]
    for each_mode in mode_list:
        if kwargs.get(each_mode):
            m_arg_value = kwargs.pop(each_mode)
            set_arg_mode(each_mode, m_arg_value, args)
        elif args.get(each_mode):
            set_arg_mode(each_mode, args[each_mode], args)
    ip_header_options = [
        'ipv4_router_alert', 'ipv4_nop',
        'ipv4_loose_source_route', 'ipv4_strict_source_route',
        'ipv4_record_route', 'ipv4_header_options', 'ipv4_security', 'ipv4_stream_id'
    ]
    ip_opt_args = dict()
    if kwargs.get("ipv4_header_options"):
        ipv4_header_options = kwargs.get("ipv4_header_options")
    for ip_opt in ip_header_options:
        if kwargs.get(ip_opt.strip()):
            ip_opt_args[ip_opt.strip()] = kwargs.pop(ip_opt.strip())

    icmpv6_args = ['icmpv6_link_layer_type', 'icmpv6_link_layer_value',
                   'icmpv6_link_layer_length', 'icmpv6_prefix_option_prefix',
                   'icmpv6_prefix_option_length', 'icmpv6_oflag', 'icmpv6_target_address',
                   'icmpv6_prefix_option_abit', 'icmpv6_prefix_option_lbit',
                   'icmpv6_prefix_option_preferred_lifetime', 'icmpv6_msg_fields', 'icmpv6_type',
                   'icmpv6_prefix_option_prefix_len', 'icmpv6_prefix_option_reserved1',
                   'icmpv6_prefix_option_reserved2', 'icmpv6_prefix_option_type',
                   'icmpv6_prefix_option_valid_lifetime', 'icmpv6_mtu_option_mtu',
                   'icmpv6_mtu_option_type', 'icmpv6_mtu_option_length', 'icmpv6_mtu_option_reserved',
                   'icmpv6_redirect_hdr_type', 'icmpv6_redirect_hdr_length',
                   'icmpv6_redirect_hdr_reserved1', 'icmpv6_redirect_hdr_reserved2', 'icmpv6_code',
                   'icmpv6_checksum', 'icmpv6_unused', 'icmpv6_pointer', 'icmpv6_id', 'icmpv6_seq', 'icmpv6_mcast_addr',
                   'icmpv6_max_resp_delay', 'icmpv6_suppress_flag', 'icmpv6_qrv', 'icmpv6_qqic', 'icmpv6_num_source',
                   'icmpv6_ip_src_addr', 'icmpv6_grp_record_mcast_addr', 'icmpv6_grp_record_record_type',
                   'icmpv6_grp_record_aux_data_len', 'icmpv6_data', 'icmpv6_rflag', 'icmpv6_ip_hop_limit',
                   'icmpv6_sflag', 'icmpv6_dest_address', 'icmpv6_ip_dst_addr', 'icmpv6_mbit', 'icmpv6_obit',
                   'icmpv6_reachable_time', 'icmpv6_retrans_time', 'icmpv6_router_lifetime']

    icmpv6_dict = {}
    if kwargs.get('icmpv6_link_layer_value'):
        icmpv6_dict['icmpv6_link_layer_value'] = ':'.join(re.findall(r'\w\w', kwargs.pop('icmpv6_link_layer_value')))
    if kwargs.get('icmpv6_prefix_option_reserved2'):
        icmpv6_dict['icmpv6_prefix_option_reserved2'] = hex(int(kwargs.pop('icmpv6_prefix_option_reserved2')))
    if kwargs.get('icmpv6_redirect_hdr_reserved1'):
        icmpv6_dict['icmpv6_redirect_hdr_reserved1'] = hex(int(kwargs.pop('icmpv6_redirect_hdr_reserved1')))
    if kwargs.get('icmpv6_redirect_hdr_reserved2'):
        icmpv6_dict['icmpv6_redirect_hdr_reserved2'] = hex(int(kwargs.pop('icmpv6_redirect_hdr_reserved2')))
    if kwargs.get('icmpv6_mtu_option_reserved'):
        icmpv6_dict['icmpv6_mtu_option_reserved'] = hex(int(kwargs.pop('icmpv6_mtu_option_reserved')))
    for icmpv6_opt in icmpv6_args:
        if kwargs.get(icmpv6_opt.strip()):
            icmpv6_dict[icmpv6_opt.strip()] = kwargs.pop(icmpv6_opt.strip())

    if kwargs.get('icmpv6_ip_hop_limit'):
        args['ipv6_hop_limit'] = kwargs.pop('icmpv6_ip_hop_limit')

    if not kwargs.get('mode'):
        raise KeyError("Please provide mode argument to the function call")

    if kwargs.get('frame_rate_distribution_port'):
        args['frame_rate_distribution_port'] = kwargs.get('frame_rate_distribution_port')
        args['frame_rate_distribution_stream'] = 'apply_to_all'

    dummy_args_list = ['ipv6_dstprefix', 'ipv6_srcprefix', 'enable_stream', 'high_speed_result_analysis']
    for dummy_arg in dummy_args_list:
        if dummy_arg in kwargs:
            kwargs.pop(dummy_arg)

    kwargs_list = list(kwargs.keys())
    for arg in kwargs_list:
        arg = arg.strip()
        if not args_dt.get(arg):
            raise Exception('Argument {} is not supported by JHLT for j_traffic_config API'.format(arg))
        args[args_dt[arg].strip()] = kwargs.pop(arg)

    if args.get('ipv6_dst_step'):
        args['ipv6_dst_step'] = ipaddress.IPv6Address(int(args.get('ipv6_dst_step'))) if re.match(r'^\d+$', args.get('ipv6_dst_step')) \
                                else args.get('ipv6_dst_step')

    if args.get('ipv6_src_step'):
        args['ipv6_src_step'] = ipaddress.IPv6Address(int(args.get('ipv6_src_step'))) if re.match(r'^\d+$', args.get('ipv6_src_step')) \
                                else args.get('ipv6_src_step')
    if args['mode'] != 'create':
        if args.get('stream_id'):
            if not isinstance(args['stream_id'], list):
                args['stream_id'] = [args['stream_id']]
            args['stream_id'] = list(set([stream.split('::')[0] for stream in args['stream_id']]))
            if len(args['stream_id']) == 1:
                args['stream_id'] = args['stream_id'][0]

    if args['mode'] == 'create':
        args['source_filter'] = 'all'
        args['destination_filter'] = 'all'
        if args.get('disable_flow_tracking') not in [1, '1']:
            args['track_by'] = 'traffic_item'
        if args.get('disable_flow_tracking'):
            args.pop('disable_flow_tracking')
        args['global_stream_control'] = 'iterations'
        args['global_stream_control_iterations'] = 1
        stream_list = invoke_ixnet(rt_handle, 'getList', '/traffic', 'trafficItem')
        args = set_source_destination_handle(rt_handle, **args)
        if args.get('transmit_mode'):
            tx_mode = get_vport_transmit_mode(rt_handle)
            if args['transmit_mode'] == 'multi_burst':
                if not args.get('burst_loop_count'):
                    args['burst_loop_count'] = 30
                if tx_mode == 'stream':
                    args['global_stream_control'] = 'iterations'
                    args['global_stream_control_iterations'] = 1
            elif args['transmit_mode'] == 'single_burst' or args['transmit_mode'] == 'single_pkt':
                if len(stream_list):
                    args['burst_loop_count'] = 0
                else:
                    args['burst_loop_count'] = 1
            elif args['transmit_mode'] == 'continuous_burst' or args['transmit_mode'] == 'continuous':
                args['global_stream_control'] = 'continuous'

    # ***** Argument Modification *****

    args = configure_mac_discovery(rt_handle, l4_protocol, args)

    # ***** End of Argument Modification *****

    args['tx_mode'] = get_vport_transmit_mode(rt_handle)
    if args['tx_mode'] is None:
        args['tx_mode'] = 'advanced'
    ret = rt_handle.invoke('traffic_config', **args)
    if len(list(ip_opt_args.keys())) > 0:
        configure_ip_options(rt_handle, ret, ip_opt_args, ipv4_header_options)
    if len(list(icmpv6_dict.keys())) > 0:
        configure_icmpv6_options(rt_handle, ret, args.get('mode'), icmpv6_dict, icmpv6_dict.pop('icmpv6_type'))
    if len(list(dhcp_dict.keys())) > 0:
        configure_traffic_options(rt_handle, ret, "dhcp", dhcp_dict)
    if len(list(gtp_dict.keys())) > 0:
        traffic_ret = add_protocol_template(rt_handle, ret['traffic_item'], 'gtpu')
        configure_traffic_options(rt_handle, traffic_ret, "gtpu", gtp_dict)
    if args['mode'] == 'create':
        if start_protocol:
            nargs = dict()
            nargs['action'] = 'start_all_protocols'
            rt_handle.invoke('test_control', **nargs)
            sleep(5)
    elif args['mode'] == 'reset':
        nargs = dict()
        nargs['action'] = 'stop_all_protocols'
        rt_handle.invoke('test_control', **nargs)
        sleep(5)
    if args.get('qos_type_ixn') is None and value != None:
        msg = 'To configure ip_ecn qos_type and qos_value are mandatory!!'
        rt_handle.log('INFO', msg)
    if value != None and args.get('qos_type_ixn') == "dscp" or args.get('qos_type_ixn') == "tos":
        configure_ip_priority(rt_handle, ret, args['mode'], value, args['qos_type_ixn'])

    # ***** Setting Custom Values *********

    if custom_pattern:
        var = 1 if not args.get('l3_protocol') and not args.get('l4_protocol') else 0
        traffic_item = ret['traffic_item']
        config_custom_pattern(rt_handle, traffic_item, custom_pattern, var)

    if pause:
        config_ethernet_pause(rt_handle, ret['traffic_item'], pause)
    port_handle = args.get('port_handle')
    if not isinstance(port_handle, list) and port_handle is not None:
        port_handle = list(port_handle)
    condition = True if port_handle is not None else False
    if condition:
        for port in port_handle:
            if pfc_dict.get(port) is None:
                continue
            configure_pfc(rt_handle, port, traffic_item=ret['traffic_item'])

    # ***** Return Value Modification *****

    if 'stream_id' in ret:
        stream_list = ret['stream_id']
        ret['stream_handles'] = []
        if args.get('bidirectional') in [1, '1']:
            direction1, direction2 = stream_list+"::"+"direction1", stream_list+"::"+"direction2"
            stream_list = [direction1, direction2]
            ret['stream_handles'].extend(stream_list)
            return ret
        ret['stream_handles'].append(stream_list)

    # ***** End of Return Value Modification *****

    return ret


def j_traffic_control(
        rt_handle,
        action=jNone,
        duration=jNone,
        port_handle=jNone,
        db_file=jNone,
        enable_arp=1,
        stream_handle=jNone,
        delay_variation_enable=jNone,
        cpdp_convergence_enable=jNone,
        max_wait_timer=30,
        latency_control=jNone,
        latency_bins=jNone,
        latency_values=jNone):
    """
    :param rt_handle:       RT object
    :param action <run|stop|reset|destroy|clear_stats|poll>
    :param duration
    :param port_handle
    :param db_file
    :param enable_arp
    :param stream_handle
    :param delay_variation_enable
    :param cpdp_convergence_enable
    :param max_wait_timer
    :param latency_control
    :param latency_bins
    :param latency_values

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global capturing

    args = dict()
    args['action'] = action
    args = get_arg_value(rt_handle, j_traffic_control.__doc__, **args)
    args['duration'] = duration
    args['port_handle'] = port_handle
    args['handle'] = stream_handle
    args['delay_variation_enable'] = delay_variation_enable
    if delay_variation_enable is not jNone:
        args['latency_enable'] = 0
    args['cpdp_convergence_enable'] = cpdp_convergence_enable
    args['max_wait_timer'] = max_wait_timer
    args['latency_control'] = latency_control
    if action == "run" or action == "sync_run":
        args['packet_loss_duration_enable'] = 1
    args['latency_bins'] = latency_bins
    args['latency_values'] = latency_values

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    # if bidirectional == 1:
    if stream_handle != jNone:
        if not isinstance(stream_handle, list):
            stream_handle = [stream_handle]
        args['handle'] = stream_handle = list(set([stream.split("::")[0] for stream in stream_handle]))

    if enable_arp in [1, '1'] and action not in ['stop', 'destroy', 'clear_stats']:
        if stream_handle != jNone:
            j_arp_control(rt_handle, stream_handle=stream_handle)
        if port_handle != jNone:
            j_arp_control(rt_handle, port_handle=port_handle)
        if stream_handle == jNone and port_handle == jNone:
            j_arp_control(rt_handle)

    if action == 'run':
        root = invoke_ixnet(rt_handle, 'getRoot')
        vports = invoke_ixnet(rt_handle, 'getList', root, "vport")
        for vport in vports:
            invoke_ixnet(rt_handle, 'execute', "sendArp", vport)
            invoke_ixnet(rt_handle, 'execute', "sendNs", vport)
        if capturing:
            args['action'] = 'stop'
            ret = rt_handle.invoke('traffic_control', **args)
            traffic_state = invoke_ixnet(rt_handle, 'getAttribute', '/traffic', '-isTrafficRunning')
            if traffic_state == 'false':
                for value in ['regenerate', 'apply']:
                    if stream_handle == jNone:
                        rt_handle.invoke('traffic_control', action=value)
                    else:
                        rt_handle.invoke('traffic_control', action=value, handle=stream_handle)
            packet_args = dict()
            if 'packetCaptureObj' in str(packetCaptureObjInst.__class__):
                packet_args.update(packetCaptureObjInst.args)
                rt_handle.invoke('packet_control', **packet_args)
            args['action'] = 'run'
        else:
            nargs = dict()
            if stream_handle != jNone:
                nargs['handle'] = stream_handle
            traffic_state = invoke_ixnet(rt_handle, 'getAttribute', '/traffic', '-isTrafficRunning')
            if traffic_state == 'false':
                try:
                    nargs['action'] = 'regenerate'
                    rt_handle._ixiangpf.traffic_control(**nargs)
                    state = invoke_ixnet(rt_handle, 'getAttribute', '/traffic', '-state')
                    if state == 'unapplied':
                        nargs['action'] = 'apply'
                        rt_handle._ixiangpf.traffic_control(**nargs)
                except:
                    nargs['action'] = 'sync_run'
                    rt_handle._ixiangpf.traffic_control(**nargs)

    if action == 'stop':
        ret = rt_handle.invoke('traffic_control', **args)
        status = 0
        for i in range(50):
            status = invoke_ixnet(rt_handle, 'getAttribute', '/traffic', '-isTrafficRunning')
            if status == 'true':
                sleep(1)
            else:
                status = 1
                break
        return ret
    ret = rt_handle.invoke('traffic_control', **args)
    if args.get('duration') is not None:
        sleep(int(args.get('duration')) + 5)
    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret

def j_traffic_stats(
        rt_handle,
        port_handle=jNone,
        mode=jNone,
        streams=jNone,
        scale_mode=jNone):
    """
    :param rt_handle:       RT object
    :param port_handle
    :param mode
    :param streams
    :param scale_mode

    Spirent Returns:
    {
        "port1": {
            "aggregate": {
                "rx": {
                    "fcoe_frame_count": "0",
                    "fcoe_frame_rate": "0",
                    "ip_pkts": "40",
                    "oversize_count": "0",
                    "oversize_rate": "0",
                    "pfc_frame_count": "0",
                    "pfc_frame_rate": "0",
                    "pkt_bit_rate": "0",
                    "pkt_byte_count": "4360",
                    "pkt_count": "20",
                    "pkt_rate": "0",
                    "raw_pkt_count": "40",
                    "tcp_checksum_errors": "0",
                    "tcp_pkts": "0",
                    "total_pkt_bytes": "4360",
                    "total_pkt_rate": "0",
                    "total_pkts": "40",
                    "udp_pkts": "0",
                    "undersize_count": "0",
                    "undersize_rate": "0",
                    "vlan_pkts_count": "0",
                    "vlan_pkts_rate": "0"
                },
                "tx": {
                    "ip_pkts": "20",
                    "pfc_frame_count": "",
                    "pkt_bit_rate": "0",
                    "pkt_byte_count": "4360",
                    "pkt_count": "20",
                    "pkt_rate": "0",
                    "raw_pkt_count": "40",
                    "raw_pkt_rate": "0",
                    "total_pkt_bytes": "4360",
                    "total_pkt_rate": "0",
                    "total_pkts": "40"
                }
            },
            "stream": {
                "streamblock2": {
                    "rx": {
                        "avg_delay": "4398.742",
                        "dropped_pkts": "0",
                        "duplicate_pkts": "0",
                        "first_tstamp": "0.0",
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "last_tstamp": "0.0",
                        "max_delay": "5396.31",
                        "max_pkt_length": "128",
                        "min_delay": "3617.53",
                        "min_pkt_length": "128",
                        "misinserted_pkts": "0",
                        "out_of_sequence_pkts": "0",
                        "prbs_bit_errors": "0",
                        "rx_port": "10.220.1.153-1-2 //1/2  10.220.1.153-1-2 //1/2 ",
                        "rx_sig_count": "10",
                        "rx_sig_rate": "0",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    },
                    "tx": {
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    }
                },
                "streamblock4": {
                    "rx": {
                        "avg_delay": "3991.514",
                        "dropped_pkts": "0",
                        "duplicate_pkts": "0",
                        "first_tstamp": "0.0",
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "last_tstamp": "0.0",
                        "max_delay": "7607.02",
                        "max_pkt_length": "128",
                        "min_delay": "2799.9",
                        "min_pkt_length": "128",
                        "misinserted_pkts": "0",
                        "out_of_sequence_pkts": "0",
                        "prbs_bit_errors": "0",
                        "rx_port": "10.220.1.153-1-2 //1/2  10.220.1.153-1-2 //1/2 ",
                        "rx_sig_count": "10",
                        "rx_sig_rate": "0",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    },
                    "tx": {
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    }
                }
            }
        },
        "port2": {
            "aggregate": {
                "rx": {
                    "fcoe_frame_count": "0",
                    "fcoe_frame_rate": "0",
                    "ip_pkts": "36",
                    "oversize_count": "0",
                    "oversize_rate": "0",
                    "pfc_frame_count": "0",
                    "pfc_frame_rate": "0",
                    "pkt_bit_rate": "0",
                    "pkt_byte_count": "4000",
                    "pkt_count": "20",
                    "pkt_rate": "0",
                    "raw_pkt_count": "36",
                    "tcp_checksum_errors": "0",
                    "tcp_pkts": "0",
                    "total_pkt_bytes": "4000",
                    "total_pkt_rate": "0",
                    "total_pkts": "36",
                    "udp_pkts": "0",
                    "undersize_count": "0",
                    "undersize_rate": "0",
                    "vlan_pkts_count": "0",
                    "vlan_pkts_rate": "0"
                },
                "tx": {
                    "ip_pkts": "20",
                    "pfc_frame_count": "",
                    "pkt_bit_rate": "0",
                    "pkt_byte_count": "4720",
                    "pkt_count": "20",
                    "pkt_rate": "0",
                    "raw_pkt_count": "44",
                    "raw_pkt_rate": "0",
                    "total_pkt_bytes": "4720",
                    "total_pkt_rate": "0",
                    "total_pkts": "44"
                }
            },
            "stream": {
                "streamblock1": {
                    "rx": {
                        "avg_delay": "14002.352",
                        "dropped_pkts": "0",
                        "duplicate_pkts": "0",
                        "first_tstamp": "0.0",
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "last_tstamp": "0.0",
                        "max_delay": "14919.78",
                        "max_pkt_length": "128",
                        "min_delay": "13072.44",
                        "min_pkt_length": "128",
                        "misinserted_pkts": "0",
                        "out_of_sequence_pkts": "0",
                        "prbs_bit_errors": "0",
                        "rx_port": "10.220.1.153-1-1 //1/1  10.220.1.153-1-1 //1/1 ",
                        "rx_sig_count": "10",
                        "rx_sig_rate": "0",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    },
                    "tx": {
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    }
                },
                "streamblock3": {
                    "rx": {
                        "avg_delay": "12167.942",
                        "dropped_pkts": "0",
                        "duplicate_pkts": "0",
                        "first_tstamp": "0.0",
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "last_tstamp": "0.0",
                        "max_delay": "12873.59",
                        "max_pkt_length": "128",
                        "min_delay": "11388.79",
                        "min_pkt_length": "128",
                        "misinserted_pkts": "0",
                        "out_of_sequence_pkts": "0",
                        "prbs_bit_errors": "0",
                        "rx_port": "10.220.1.153-1-1 //1/1  10.220.1.153-1-1 //1/1 ",
                        "rx_sig_count": "10",
                        "rx_sig_rate": "0",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    },
                    "tx": {
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    }
                }
            }
        },
        "status": "1",
        "traffic_item": {
            "streamblock1": {
                "rx": {
                    "avg_delay": "14002.352",
                    "dropped_pkts": "0",
                    "duplicate_pkts": "0",
                    "first_tstamp": "0.0",
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "last_tstamp": "0.0",
                    "max_delay": "14919.78",
                    "max_pkt_length": "128",
                    "min_delay": "13072.44",
                    "min_pkt_length": "128",
                    "misinserted_pkts": "0",
                    "out_of_sequence_pkts": "0",
                    "prbs_bit_errors": "0",
                    "rx_port": "10.220.1.153-1-1 //1/1  10.220.1.153-1-1 //1/1 ",
                    "rx_sig_count": "10",
                    "rx_sig_rate": "0",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                },
                "tx": {
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                }
            },
            "streamblock2": {
                "rx": {
                    "avg_delay": "4398.742",
                    "dropped_pkts": "0",
                    "duplicate_pkts": "0",
                    "first_tstamp": "0.0",
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "last_tstamp": "0.0",
                    "max_delay": "5396.31",
                    "max_pkt_length": "128",
                    "min_delay": "3617.53",
                    "min_pkt_length": "128",
                    "misinserted_pkts": "0",
                    "out_of_sequence_pkts": "0",
                    "prbs_bit_errors": "0",
                    "rx_port": "10.220.1.153-1-2 //1/2  10.220.1.153-1-2 //1/2 ",
                    "rx_sig_count": "10",
                    "rx_sig_rate": "0",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                },
                "tx": {
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                }
            },
            "streamblock3": {
                "rx": {
                    "avg_delay": "12167.942",
                    "dropped_pkts": "0",
                    "duplicate_pkts": "0",
                    "first_tstamp": "0.0",
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "last_tstamp": "0.0",
                    "max_delay": "12873.59",
                    "max_pkt_length": "128",
                    "min_delay": "11388.79",
                    "min_pkt_length": "128",
                    "misinserted_pkts": "0",
                    "out_of_sequence_pkts": "0",
                    "prbs_bit_errors": "0",
                    "rx_port": "10.220.1.153-1-1 //1/1  10.220.1.153-1-1 //1/1 ",
                    "rx_sig_count": "10",
                    "rx_sig_rate": "0",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                },
                "tx": {
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                }
            },
            "streamblock4": {
                "rx": {
                    "avg_delay": "3991.514",
                    "dropped_pkts": "0",
                    "duplicate_pkts": "0",
                    "first_tstamp": "0.0",
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "last_tstamp": "0.0",
                    "max_delay": "7607.02",
                    "max_pkt_length": "128",
                    "min_delay": "2799.9",
                    "min_pkt_length": "128",
                    "misinserted_pkts": "0",
                    "out_of_sequence_pkts": "0",
                    "prbs_bit_errors": "0",
                    "rx_port": "10.220.1.153-1-2 //1/2  10.220.1.153-1-2 //1/2 ",
                    "rx_sig_count": "10",
                    "rx_sig_rate": "0",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                },
                "tx": {
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                }
            }
        }
    }

    IXIA Returns:
    {
        "1/11/1": {
            "aggregate": {
                "duplex_mode": "N/A",
                "port_name": "1/11/1",
                "rx": {
                    "collisions_count": "N/A",
                    "control_frames": "0",
                    "crc_errors": "N/A",
                    "data_int_errors_count": "N/A",
                    "data_int_frames_count": "N/A",
                    "misdirected_packet_count": "N/A",
                    "oversize_count": "N/A",
                    "oversize_crc_errors_count": "N/A",
                    "oversize_crc_errors_rate_count": "N/A",
                    "oversize_rate": "N/A",
                    "oversize_rate_count": "N/A",
                    "pkt_bit_count": "N/A",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000",
                    "raw_pkt_count": "20",
                    "raw_pkt_rate": "0",
                    "rs_fec_corrected_error_count": "N/A",
                    "rs_fec_corrected_error_count_rate": "N/A",
                    "rs_fec_uncorrected_error_count": "N/A",
                    "rs_fec_uncorrected_error_count_rate": "N/A",
                    "rx_aal5_frames_count": "N/A",
                    "rx_aal5_frames_rate": "N/A",
                    "rx_atm_cells_count": "N/A",
                    "rx_atm_cells_rate": "N/A",
                    "total_pkts": "20",
                    "uds1_frame_count": "20",
                    "uds1_frame_rate": "0",
                    "uds2_frame_count": "20",
                    "uds2_frame_rate": "0",
                    "uds3_frame_count": "N/A",
                    "uds3_frame_rate": "N/A",
                    "uds4_frame_count": "N/A",
                    "uds4_frame_rate": "N/A",
                    "uds5_frame_count": "20",
                    "uds5_frame_rate": "0",
                    "uds6_frame_count": "20",
                    "uds6_frame_rate": "0"
                },
                "tx": {
                    "control_frames": "0",
                    "elapsed_time": "2841736040",
                    "line_speed": "N/A",
                    "pkt_bit_count": "N/A",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000",
                    "raw_pkt_count": "20",
                    "scheduled_pkt_count": "20",
                    "scheduled_pkt_rate": "N/A",
                    "total_pkt_rate": "0",
                    "total_pkts": "20",
                    "tx_aal5_bytes_count": "N/A",
                    "tx_aal5_bytes_rate": "N/A",
                    "tx_aal5_frames_count": "N/A",
                    "tx_aal5_frames_rate": "N/A",
                    "tx_aal5_scheduled_cells_count": "N/A",
                    "tx_aal5_scheduled_cells_rate": "N/A",
                    "tx_aal5_scheduled_frames_count": "20",
                    "tx_aal5_scheduled_frames_rate": "N/A",
                    "tx_atm_cells_count": "N/A",
                    "tx_atm_cells_rate": "N/A"
                }
            },
            "data_plane_port": {
                "first_timestamp": "00:00:02.003",
                "last_timestamp": "00:00:04.827",
                "rx": {
                    "avg_latency": "2039728",
                    "l1_bit_rate": "0.000",
                    "l1_load_percent": "0.000",
                    "max_latency": "4189420",
                    "min_latency": "490840",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0.000",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "l1_load_percent": "0.000",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_rate": "0.000",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000"
                }
            },
            "flow": {
                "1": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "0",
                        "last_tstamp": "0",
                        "loss_percent": "0",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_byte_rate": "0",
                        "total_pkt_bytes": "0",
                        "total_pkt_kbit_rate": "0",
                        "total_pkt_mbit_rate": "0",
                        "total_pkt_rate": "0",
                        "total_pkts": "0",
                        "total_pkts_bytes": "0"
                    },
                    "tx": {
                        "flow_name": "1/11/2 TI0-HLTAPI_TRAFFICITEM_540",
                        "pgid_value": "N/A",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "2": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:02.003",
                        "flow_name": "1/11/1 TI0-HLTAPI_TRAFFICITEM_540",
                        "last_tstamp": "00:00:02.003",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pgid_value": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0",
                        "total_pkts": "0"
                    }
                },
                "3": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "0",
                        "last_tstamp": "0",
                        "loss_percent": "0",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_byte_rate": "0",
                        "total_pkt_bytes": "0",
                        "total_pkt_kbit_rate": "0",
                        "total_pkt_mbit_rate": "0",
                        "total_pkt_rate": "0",
                        "total_pkts": "0",
                        "total_pkts_bytes": "0"
                    },
                    "tx": {
                        "flow_name": "1/11/2 TI1-HLTAPI_TRAFFICITEM_540",
                        "pgid_value": "N/A",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "4": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:04.824",
                        "flow_name": "1/11/1 TI1-HLTAPI_TRAFFICITEM_540",
                        "last_tstamp": "00:00:04.827",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pgid_value": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0",
                        "total_pkts": "0"
                    }
                }
            },
            "stream": {
                "TI0-HLTAPI_TRAFFICITEM_540": {
                    "rx": {
                        "avg_delay": "2780722",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:02.003",
                        "last_tstamp": "00:00:02.003",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "4189420",
                        "min_delay": "1358460",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "TI1-HLTAPI_TRAFFICITEM_540": {
                    "rx": {
                        "avg_delay": "1298734",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:04.824",
                        "last_tstamp": "00:00:04.827",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "2217160",
                        "min_delay": "490840",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                }
            }
        },
        "1/11/2": {
            "aggregate": {
                "duplex_mode": "N/A",
                "port_name": "1/11/2",
                "rx": {
                    "collisions_count": "N/A",
                    "control_frames": "0",
                    "crc_errors": "N/A",
                    "data_int_errors_count": "N/A",
                    "data_int_frames_count": "N/A",
                    "misdirected_packet_count": "N/A",
                    "oversize_count": "N/A",
                    "oversize_crc_errors_count": "N/A",
                    "oversize_crc_errors_rate_count": "N/A",
                    "oversize_rate": "N/A",
                    "oversize_rate_count": "N/A",
                    "pkt_bit_count": "N/A",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000",
                    "raw_pkt_count": "20",
                    "raw_pkt_rate": "0",
                    "rs_fec_corrected_error_count": "N/A",
                    "rs_fec_corrected_error_count_rate": "N/A",
                    "rs_fec_uncorrected_error_count": "N/A",
                    "rs_fec_uncorrected_error_count_rate": "N/A",
                    "rx_aal5_frames_count": "N/A",
                    "rx_aal5_frames_rate": "N/A",
                    "rx_atm_cells_count": "N/A",
                    "rx_atm_cells_rate": "N/A",
                    "total_pkts": "20",
                    "uds1_frame_count": "20",
                    "uds1_frame_rate": "0",
                    "uds2_frame_count": "20",
                    "uds2_frame_rate": "0",
                    "uds3_frame_count": "N/A",
                    "uds3_frame_rate": "N/A",
                    "uds4_frame_count": "N/A",
                    "uds4_frame_rate": "N/A",
                    "uds5_frame_count": "20",
                    "uds5_frame_rate": "0",
                    "uds6_frame_count": "20",
                    "uds6_frame_rate": "0"
                },
                "tx": {
                    "control_frames": "0",
                    "elapsed_time": "2826269560",
                    "line_speed": "N/A",
                    "pkt_bit_count": "N/A",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000",
                    "raw_pkt_count": "20",
                    "scheduled_pkt_count": "20",
                    "scheduled_pkt_rate": "N/A",
                    "total_pkt_rate": "0",
                    "total_pkts": "20",
                    "tx_aal5_bytes_count": "N/A",
                    "tx_aal5_bytes_rate": "N/A",
                    "tx_aal5_frames_count": "N/A",
                    "tx_aal5_frames_rate": "N/A",
                    "tx_aal5_scheduled_cells_count": "N/A",
                    "tx_aal5_scheduled_cells_rate": "N/A",
                    "tx_aal5_scheduled_frames_count": "20",
                    "tx_aal5_scheduled_frames_rate": "N/A",
                    "tx_atm_cells_count": "N/A",
                    "tx_atm_cells_rate": "N/A"
                }
            },
            "data_plane_port": {
                "first_timestamp": "00:00:02.006",
                "last_timestamp": "00:00:04.845",
                "rx": {
                    "avg_latency": "1310229",
                    "l1_bit_rate": "0.000",
                    "l1_load_percent": "0.000",
                    "max_latency": "2687700",
                    "min_latency": "-238220",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0.000",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "l1_load_percent": "0.000",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_rate": "0.000",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000"
                }
            },
            "flow": {
                "1": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:02.006",
                        "flow_name": "1/11/2 TI0-HLTAPI_TRAFFICITEM_540",
                        "last_tstamp": "00:00:02.008",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pgid_value": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0",
                        "total_pkts": "0"
                    }
                },
                "2": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "0",
                        "last_tstamp": "0",
                        "loss_percent": "0",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_byte_rate": "0",
                        "total_pkt_bytes": "0",
                        "total_pkt_kbit_rate": "0",
                        "total_pkt_mbit_rate": "0",
                        "total_pkt_rate": "0",
                        "total_pkts": "0",
                        "total_pkts_bytes": "0"
                    },
                    "tx": {
                        "flow_name": "1/11/1 TI0-HLTAPI_TRAFFICITEM_540",
                        "pgid_value": "N/A",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "3": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:04.840",
                        "flow_name": "1/11/2 TI1-HLTAPI_TRAFFICITEM_540",
                        "last_tstamp": "00:00:04.845",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pgid_value": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0",
                        "total_pkts": "0"
                    }
                },
                "4": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "0",
                        "last_tstamp": "0",
                        "loss_percent": "0",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_byte_rate": "0",
                        "total_pkt_bytes": "0",
                        "total_pkt_kbit_rate": "0",
                        "total_pkt_mbit_rate": "0",
                        "total_pkt_rate": "0",
                        "total_pkts": "0",
                        "total_pkts_bytes": "0"
                    },
                    "tx": {
                        "flow_name": "1/11/1 TI1-HLTAPI_TRAFFICITEM_540",
                        "pgid_value": "N/A",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                }
            },
            "stream": {
                "TI0-HLTAPI_TRAFFICITEM_540": {
                    "rx": {
                        "avg_delay": "1807008",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:02.006",
                        "last_tstamp": "00:00:02.008",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "2687700",
                        "min_delay": "1171900",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "TI1-HLTAPI_TRAFFICITEM_540": {
                    "rx": {
                        "avg_delay": "813450",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:04.840",
                        "last_tstamp": "00:00:04.845",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "1927200",
                        "min_delay": "-238220",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                }
            }
        },
        "aggregate": {
            "duplex_mode": {
                "count": "N/A"
            },
            "port_name": {
                "count": "2"
            },
            "rx": {
                "collisions_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "control_frames": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "crc_errors": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "data_int_errors_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "data_int_frames_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "misdirected_packet_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "oversize_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "oversize_crc_errors_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "oversize_crc_errors_rate_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "oversize_rate_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "pkt_bit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_byte_count": {
                    "avg": "2560",
                    "count": "2",
                    "max": "2560",
                    "min": "2560",
                    "sum": "5120"
                },
                "pkt_byte_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "pkt_kbit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_mbit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "40.0"
                },
                "raw_pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "raw_pkt_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "rs_fec_corrected_error_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rs_fec_corrected_error_count_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rs_fec_uncorrected_error_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rs_fec_uncorrected_error_count_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rx_aal5_frames_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rx_aal5_frames_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rx_atm_cells_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rx_atm_cells_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "total_pkts": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "uds1_frame_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20"
                },
                "uds1_frame_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "uds2_frame_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20"
                },
                "uds2_frame_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "uds3_frame_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A"
                },
                "uds3_frame_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "uds4_frame_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A"
                },
                "uds4_frame_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "uds5_frame_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20"
                },
                "uds5_frame_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "uds6_frame_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20"
                },
                "uds6_frame_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                }
            },
            "tx": {
                "control_frames": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "elapsed_time": {
                    "avg": "2834002800",
                    "count": "2",
                    "max": "2841736040",
                    "min": "2826269560",
                    "sum": "5668005600"
                },
                "line_speed": {
                    "count": "N/A"
                },
                "pkt_bit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_byte_count": {
                    "avg": "2560",
                    "count": "2",
                    "max": "2560",
                    "min": "2560",
                    "sum": "5120"
                },
                "pkt_byte_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "pkt_kbit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_mbit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "raw_pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "scheduled_pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "scheduled_pkt_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "total_pkt_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "total_pkts": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "tx_aal5_bytes_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_bytes_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_frames_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_frames_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_scheduled_cells_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_scheduled_cells_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_scheduled_frames_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "tx_aal5_scheduled_frames_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_atm_cells_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_atm_cells_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                }
            }
        },
        "flow": {
            "1": {
                "flow_name": "1/11/2 TI0-HLTAPI_TRAFFICITEM_540",
                "pgid_value": "N/A",
                "rx": {
                    "avg_delay": "1807008",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:02.006",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:02.008",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "2687700",
                    "min_delay": "1171900",
                    "misdirected_pkts": "N/A",
                    "misdirected_ports": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "port": "1/11/2",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "1280",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10",
                    "total_pkts_bytes": "1280"
                },
                "tracking": {
                    "1": {
                        "tracking_name": "Traffic Item",
                        "tracking_value": "TI0-HLTAPI_TRAFFICITEM_540"
                    },
                    "count": "1"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "port": "1/11/1",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10"
                }
            },
            "2": {
                "flow_name": "1/11/1 TI0-HLTAPI_TRAFFICITEM_540",
                "pgid_value": "N/A",
                "rx": {
                    "avg_delay": "2780722",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:02.003",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:02.003",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "4189420",
                    "min_delay": "1358460",
                    "misdirected_pkts": "N/A",
                    "misdirected_ports": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "port": "1/11/1",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "1280",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10",
                    "total_pkts_bytes": "1280"
                },
                "tracking": {
                    "1": {
                        "tracking_name": "Traffic Item",
                        "tracking_value": "TI0-HLTAPI_TRAFFICITEM_540"
                    },
                    "count": "1"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "port": "1/11/2",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10"
                }
            },
            "3": {
                "flow_name": "1/11/2 TI1-HLTAPI_TRAFFICITEM_540",
                "pgid_value": "N/A",
                "rx": {
                    "avg_delay": "813450",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:04.840",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:04.845",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "1927200",
                    "min_delay": "-238220",
                    "misdirected_pkts": "N/A",
                    "misdirected_ports": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "port": "1/11/2",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "1280",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10",
                    "total_pkts_bytes": "1280"
                },
                "tracking": {
                    "1": {
                        "tracking_name": "Traffic Item",
                        "tracking_value": "TI1-HLTAPI_TRAFFICITEM_540"
                    },
                    "count": "1"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "port": "1/11/1",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10"
                }
            },
            "4": {
                "flow_name": "1/11/1 TI1-HLTAPI_TRAFFICITEM_540",
                "pgid_value": "N/A",
                "rx": {
                    "avg_delay": "1298734",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:04.824",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:04.827",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "2217160",
                    "min_delay": "490840",
                    "misdirected_pkts": "N/A",
                    "misdirected_ports": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "port": "1/11/1",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "1280",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10",
                    "total_pkts_bytes": "1280"
                },
                "tracking": {
                    "1": {
                        "tracking_name": "Traffic Item",
                        "tracking_value": "TI1-HLTAPI_TRAFFICITEM_540"
                    },
                    "count": "1"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "port": "1/11/2",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10"
                }
            }
        },
        "l23_test_summary": {
            "rx": {
                "avg_latency": "1674978",
                "max_latency": "4189420",
                "min_latency": "-238220",
                "pkt_bit_rate": "0.000",
                "pkt_byte_rate": "0.000",
                "pkt_count": "40",
                "pkt_kbit_rate": "0.000",
                "pkt_mbit_rate": "0.000",
                "pkt_rate": "0.000"
            },
            "tx": {
                "pkt_bit_rate": "0.000",
                "pkt_byte_rate": "0.000",
                "pkt_count": "40",
                "pkt_kbit_rate": "0.000",
                "pkt_mbit_rate": "0.000",
                "pkt_rate": "0.000"
            }
        },
        "measure_mode": "mixed",
        "status": "1",
        "traffic_item": {
            "TI0-HLTAPI_TRAFFICITEM_540": {
                "rx": {
                    "avg_delay": "2293865",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:02.003",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:02.008",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "4189420",
                    "min_delay": "1171900",
                    "misdirected_pkts": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "2560",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "20",
                    "total_pkts_bytes": "2560"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "20"
                }
            },
            "TI1-HLTAPI_TRAFFICITEM_540": {
                "rx": {
                    "avg_delay": "1056092",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:04.824",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:04.845",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "2217160",
                    "min_delay": "-238220",
                    "misdirected_pkts": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "2560",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "20",
                    "total_pkts_bytes": "2560"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "20"
                }
            },
            "aggregate": {
                "rx": {
                    "avg_delay": {
                        "avg": "1674978",
                        "count": "2",
                        "max": "2293865",
                        "min": "1056092",
                        "sum": "3349957"
                    },
                    "big_error": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "expected_pkts": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "first_tstamp": {
                        "count": "2"
                    },
                    "l1_bit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "last_tstamp": {
                        "count": "2"
                    },
                    "loss_percent": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "loss_pkts": {
                        "avg": "0",
                        "count": "2",
                        "max": "0",
                        "min": "0",
                        "sum": "0"
                    },
                    "max_delay": {
                        "avg": "3203290",
                        "count": "2",
                        "max": "4189420",
                        "min": "2217160",
                        "sum": "6406580"
                    },
                    "min_delay": {
                        "avg": "466840",
                        "count": "2",
                        "max": "1171900",
                        "min": "-238220",
                        "sum": "933680"
                    },
                    "misdirected_pkts": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "misdirected_rate": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "pkt_loss_duration": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "reverse_error": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "small_error": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "total_pkt_bit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_byte_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_bytes": {
                        "avg": "2560",
                        "count": "2",
                        "max": "2560",
                        "min": "2560",
                        "sum": "5120"
                    },
                    "total_pkt_kbit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_mbit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkts": {
                        "avg": "20",
                        "count": "2",
                        "max": "20",
                        "min": "20",
                        "sum": "40"
                    },
                    "total_pkts_bytes": {
                        "avg": "2560",
                        "count": "2",
                        "max": "2560",
                        "min": "2560",
                        "sum": "5120"
                    }
                },
                "tx": {
                    "l1_bit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_bit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_byte_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_kbit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_mbit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkts": {
                        "avg": "20",
                        "count": "2",
                        "max": "20",
                        "min": "20",
                        "sum": "40"
                    }
                }
            }
        },
        "waiting_for_stats": "0"
    }
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['mode'] = mode
    args['streams'] = streams

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    args['mode'] = 'all'

    if streams != jNone:
        if not isinstance(streams, list):
            args['streams'] = [streams]
        args['streams'] = list(set([stream.split("::")[0] for stream in args['streams']]))

    ret = rt_handle.invoke('traffic_stats', **args)

    # ***** Return Value Modification *****

    map_dict = dict()
    traffic_items = invoke_ixnet(rt_handle, 'getList', "::ixNet::OBJ-/traffic", 'trafficItem')
    bidirec_items = [item for item in traffic_items if invoke_ixnet(rt_handle, 'getAttribute', item, '-biDirectional') in ['true', True]]
    streams_dict = dict()
    if bidirec_items:
        endpoint_sets = list()
        stream_names = [invoke_ixnet(rt_handle, 'getAttribute', item, '-name') for item in bidirec_items]
        endpoint_sets = [invoke_ixnet(rt_handle, 'getList', item, 'endpointSet')[0] for item in bidirec_items]

        for index, each_endpoint in enumerate(endpoint_sets):
            destination = get_ixia_port_handle(rt_handle, invoke_ixnet(rt_handle, 'getAttribute', each_endpoint, '-destinations')[0])
            source = get_ixia_port_handle(rt_handle, invoke_ixnet(rt_handle, 'getAttribute', each_endpoint, '-sources')[0])
            map_dict[stream_names[index]] = {'source': source, 'destination': destination}

        for stream in stream_names:
            if map_dict.get(stream):
                if ret.get(map_dict[stream]['source']):
                    if ret[map_dict[stream]['source']].get('stream') is not None:
                        if stream in ret[map_dict[stream]['source']].get('stream'):
                            ret[map_dict[stream]['source']]['stream'][stream+"::direction2"] = ret[map_dict[stream]['source']]['stream'][stream]
                            streams_dict.update({stream+"::direction2": ret[map_dict[stream]['source']]['stream'][stream]})

                if ret.get(map_dict[stream]['destination']):
                    if ret[map_dict[stream]['destination']].get('stream') is not None:
                        if stream in ret[map_dict[stream]['destination']].get('stream'):
                            ret[map_dict[stream]['destination']]['stream'][stream+"::direction1"] = ret[map_dict[stream]['destination']]['stream'][stream]
                            streams_dict.update({stream+"::direction1": ret[map_dict[stream]['destination']]['stream'][stream]})

    for key in list(ret):
        if 'aggregate' in ret[key]:
            for new_key in ret[key]['aggregate']:
                if 'oversize_rate_count' in ret[key]['aggregate'][new_key]:
                    ret[key]['aggregate'][new_key]['oversize_rate'] = ret[key]['aggregate'][new_key]['oversize_rate_count']
                if 'pkt_byte_count' in ret[key]['aggregate'][new_key]:
                    ret[key]['aggregate'][new_key]['total_pkt_bytes'] = ret[key]['aggregate'][new_key]['pkt_byte_count']

        if re.match(r"\d+\/\d+\/\d+", key):
            if 'stream' in ret[key]:
                stream_list = list(ret[key]['stream'])
                for each_stream in stream_list:
                    for new_key in ret[key]['stream'][each_stream]:
                        if 'loss_percent' in ret[key]['stream'][each_stream][new_key]:
                            ret[key]['stream'][each_stream][new_key]['dropped_pkts_percent'] = ret[key]['stream'][each_stream][new_key]['loss_percent']
                        if 'loss_pkts' in ret[key]['stream'][each_stream][new_key]:
                            ret[key]['stream'][each_stream][new_key]['dropped_pkts'] = ret[key]['stream'][each_stream][new_key]['loss_pkts']

        if key == 'traffic_item':
            stream_id_list = list(ret[key])
            if 'aggregate' in stream_id_list:
                stream_id_list.remove('aggregate')
            for each_stream_id in streams_dict:
                ret[key][each_stream_id] = streams_dict[each_stream_id]


    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ospf_info(
        rt_handle,
        port_handle=jNone,
        handle=jNone):
    """
    :param rt_handle:       RT object
    :param port_handle
    :param handle

    Spirent Returns:
    {
        "adjacency_status": "FULL",
        "router_state": "POINT_TO_POINT",
        "rx_ack": "2",
        "rx_asexternal_lsa": "0",
        "rx_dd": "2",
        "rx_external_link_lsa": "0",
        "rx_external_prefix_lsa": "0",
        "rx_hello": "1",
        "rx_network_lsa": "0",
        "rx_nssa_lsa": "0",
        "rx_request": "1",
        "rx_router_asbr": "0",
        "rx_router_info_lsa": "0",
        "rx_router_lsa": "2",
        "rx_summary_lsa": "1",
        "rx_te_lsa": "0",
        "status": "1",
        "tx_ack": "2",
        "tx_as_external_lsa": "0",
        "tx_asbr_summry_lsa": "0",
        "tx_dd": "4",
        "tx_external_link_lsa": "0",
        "tx_external_prefix_lsa": "0",
        "tx_hello": "1",
        "tx_network_lsa": "0",
        "tx_nssa_lsa": "0",
        "tx_request": "1",
        "tx_router_info_lsa": "0",
        "tx_router_lsa": "2",
        "tx_summary_lsa": "1",
        "tx_te_lsa": "0"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1/item:1": {
            "session": {
                "database_description_rx": "2",
                "database_description_tx": "3",
                "hellos_rx": "3",
                "hellos_tx": "3",
                "information": "none",
                "linkstate_ack_rx": "1",
                "linkstate_ack_tx": "1",
                "linkstate_advertisement_rx": "2",
                "linkstate_advertisement_tx": "2",
                "linkstate_request_rx": "1",
                "linkstate_request_tx": "1",
                "linkstate_update_rx": "1",
                "linkstate_update_tx": "1",
                "lsa_acknowledge_rx": "2",
                "lsa_acknowledged": "2",
                "ospfIfaceState": "pointToPoint",
                "ospfNeighborState": "full",
                "status": "up"
            }
        },
        "Device Group 1": {
            "aggregate": {
                "database_description_rx": "2",
                "database_description_tx": "3",
                "external_lsa_rx": "0",
                "external_lsa_tx": "0",
                "grace_lsa_rx": "0",
                "hellos_rx": "3",
                "hellos_tx": "3",
                "helpermode_attempted": "0",
                "helpermode_failed": "0",
                "linkstate_ack_rx": "1",
                "linkstate_ack_tx": "1",
                "linkstate_advertisement_rx": "2",
                "linkstate_advertisement_tx": "2",
                "linkstate_request_rx": "1",
                "linkstate_request_tx": "1",
                "linkstate_update_rx": "1",
                "linkstate_update_tx": "1",
                "lsa_acknowledge_rx": "2",
                "lsa_acknowledged": "2",
                "neighbor_2way_count": "0",
                "neighbor_attempt_count": "0",
                "neighbor_down_count": "0",
                "neighbor_exchange_count": "0",
                "neighbor_exstart_count": "0",
                "neighbor_full_count": "1",
                "neighbor_init_count": "0",
                "neighbor_loading_count": "0",
                "network_lsa_rx": "0",
                "network_lsa_tx": "0",
                "nssa_lsa_rx": "0",
                "nssa_lsa_tx": "0",
                "opaque_area_lsa_rx": "0",
                "opaque_area_lsa_tx": "0",
                "opaque_domain_lsa_rx": "0",
                "opaque_domain_lsa_tx": "0",
                "opaque_local_lsa_rx": "0",
                "opaque_local_lsa_tx": "0",
                "router_lsa_rx": "1",
                "router_lsa_tx": "1",
                "sessions_configured": "1",
                "status": "started",
                "summary_iplsa_rx": "1",
                "summary_iplsa_tx": "1"
            }
        },
        "rx_ack": "1",
        "rx_hello": "3",
        "rx_network_lsa": "0",
        "rx_nssa_lsa": "0",
        "rx_request": "1",
        "rx_router_lsa": "1",
        "rx_summary_lsa": "1",
        "status": "up",
        "tx_ack": "1",
        "tx_hello": "3",
        "tx_network_lsa": "0",
        "tx_nssa_lsa": "0",
        "tx_request": "1",
        "tx_router_lsa": "1",
        "tx_summary_lsa": "1",
        "adjacency_status": "full",
        "router_state": "pointToPoint",
        "rx_asexternal_lsa": "0",
        "rx_dd": "3",
        "tx_as_external_lsa": "0",
        "tx_dd": "2",
    }

    Common Return Keys:
        "status"
        "rx_ack"
        "rx_hello"
        "rx_network_lsa"
        "rx_nssa_lsa"
        "rx_request"
        "rx_router_lsa"
        "rx_summary_lsa"
        "tx_ack"
        "tx_hello"
        "tx_network_lsa"
        "tx_nssa_lsa"
        "tx_request"
        "tx_router_lsa"
        "tx_summary_lsa"
        "adjacency_status"
        "router_state"
        "rx_asexternal_lsa"
        "rx_dd"
        "tx_as_external_lsa"
        "tx_dd"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['handle'] = handle

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        args['session_type'] = session_map[hndl]
        stats = dict()
        args['mode'] = 'aggregate_stats'
        stats.update(rt_handle.invoke('emulation_ospf_info', **args))
        args['mode'] = 'learned_info'
        stats.update(rt_handle.invoke('emulation_ospf_info', **args))
        args['mode'] = 'session'
        stats.update(rt_handle.invoke('emulation_ospf_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                if 'hellos_rx' in ret[index][key]['aggregate']:
                    ret[index]['rx_hello'] = ret[index][key]['aggregate']['hellos_rx']
                if 'hellos_tx' in ret[index][key]['aggregate']:
                    ret[index]['tx_hello'] = ret[index][key]['aggregate']['hellos_tx']
                if 'network_lsa_rx' in ret[index][key]['aggregate']:
                    ret[index]['rx_network_lsa'] = ret[index][key]['aggregate']['network_lsa_rx']
                if 'network_lsa_tx' in ret[index][key]['aggregate']:
                    ret[index]['tx_network_lsa'] = ret[index][key]['aggregate']['network_lsa_tx']
                if 'nssa_lsa_rx' in ret[index][key]['aggregate']:
                    ret[index]['rx_nssa_lsa'] = ret[index][key]['aggregate']['nssa_lsa_rx']
                if 'nssa_lsa_tx' in ret[index][key]['aggregate']:
                    ret[index]['tx_nssa_lsa'] = ret[index][key]['aggregate']['nssa_lsa_tx']
                if 'linkstate_request_rx' in ret[index][key]['aggregate']:
                    ret[index]['rx_request'] = ret[index][key]['aggregate']['linkstate_request_rx']
                if 'linkstate_request_tx' in ret[index][key]['aggregate']:
                    ret[index]['tx_request'] = ret[index][key]['aggregate']['linkstate_request_tx']
                if 'router_lsa_rx' in ret[index][key]['aggregate']:
                    ret[index]['rx_router_lsa'] = ret[index][key]['aggregate']['router_lsa_rx']
                if 'router_lsa_tx' in ret[index][key]['aggregate']:
                    ret[index]['tx_router_lsa'] = ret[index][key]['aggregate']['router_lsa_tx']
                if 'summary_iplsa_rx' in ret[index][key]['aggregate']:
                    ret[index]['rx_summary_lsa'] = ret[index][key]['aggregate']['summary_iplsa_rx']
                if 'summary_iplsa_tx' in ret[index][key]['aggregate']:
                    ret[index]['tx_summary_lsa'] = ret[index][key]['aggregate']['summary_iplsa_tx']
                if 'linkstate_ack_rx' in ret[index][key]['aggregate']:
                    ret[index]['rx_ack'] = ret[index][key]['aggregate']['linkstate_ack_rx']
                if 'linkstate_ack_tx' in ret[index][key]['aggregate']:
                    ret[index]['tx_ack'] = ret[index][key]['aggregate']['linkstate_ack_tx']
                if 'database_description_rx' in ret[index][key]['aggregate']:
                    ret[index]['rx_dd'] = ret[index][key]['aggregate']['database_description_rx']
                if 'database_description_tx' in ret[index][key]['aggregate']:
                    ret[index]['tx_dd'] = ret[index][key]['aggregate']['database_description_tx']
                if 'external_lsa_tx' in ret[index][key]['aggregate']:
                    ret[index]['tx_as_external_lsa'] = ret[index][key]['aggregate']['external_lsa_tx']
                if 'external_lsa_rx' in ret[index][key]['aggregate']:
                    ret[index]['rx_asexternal_lsa'] = ret[index][key]['aggregate']['external_lsa_rx']
            elif 'session' in ret[index][key]:
                if 'ospfIfaceState' in ret[index][key]['session']:
                    ret[index]['router_state'] = ret[index][key]['session']['ospfIfaceState']
                if 'ospfNeighborState' in ret[index][key]['session']:
                    ret[index]['adjacency_status'] = ret[index][key]['session']['ospfNeighborState']
                if 'status' in ret[index][key]['session']:
                    ret[index]['status'] = ret[index][key]['session']['status']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_isis_topology_route_config(
        rt_handle,
        mode=jNone,
        handle=jNone,
        type=jNone,
        external_ip_start=jNone,
        external_ip_pfx_len=jNone,
        router_routing_level=jNone,
        external_up_down_bit=jNone,
        external_metric=jNone,
        router_system_id=jNone,
        external_count=jNone,
        external_ip_step=jNone,
        external_ipv6_pfx_len=jNone,
        external_ipv6_start=jNone,
        external_ipv6_step=jNone):
    """
    :param rt_handle:       RT object
    :param mode - <create|modify|delete>
    :param handle
    :param type - <ipv4|ipv6>
    :param external_ip_start
    :param external_ip_pfx_len - <1-32>
    :param external_up_down_bit - <0|1>
    :param external_metric - <1-63>
    :param router_system_id
    :param external_count - <1-35000>
    :param external_ip_step
    :param external_ipv6_pfx_len - <1-128>
    :param external_ipv6_start
    :param external_ipv6_step

    Spirent Returns:
    {
        "elem_handle": "isisRouteHandle0",
        "external": "num_networks 1",
        "handles": "isisRouteHandle0",
        "status": "1",
        "version": "4"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/networkGroup:1",
        "ipv4_prefix_interface_handle": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/isisL3RouteProperty:1",
        "network_group_handle": "/topology:1/deviceGroup:1/networkGroup:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args['handle'] = handle
    args['type'] = type
    args['external_ip_start'] = external_ip_start
    args['external_ip_pfx_len'] = external_ip_pfx_len
    args['external_metric'] = external_metric
    args['external_up_down_bit'] = external_up_down_bit
    args['router_system_id'] = router_system_id
    args['external_count'] = external_count
    args['external_ip_step'] = external_ip_step
    args['external_ipv6_pfx_len'] = external_ipv6_pfx_len
    args['external_ipv6_start'] = external_ipv6_start
    args['external_ipv6_step'] = external_ipv6_step

    args = get_arg_value(rt_handle, j_emulation_isis_topology_route_config.__doc__, **args)
    if args.get('external_metric'):
        args['stub_metric' if type == 'ipv4' else 'external_metric'] = args.pop('external_metric')
    __check_and_raise(type)
    if type == 'ipv6':
        args['type'] = 'ipv6-prefix'
        if args.get('external_ipv6_start'):
            args['ipv6_prefix_network_address'] = args.pop('external_ipv6_start')
        if args.get('external_ipv6_step'):
            nargs = dict()
            nargs['pattern'] = 'counter'
            nargs['counter_start'] = args['ipv6_prefix_network_address']
            nargs['counter_step'] = args.pop('external_ipv6_step')
            nargs['counter_direction'] = 'increment'
            _result_ = rt_handle.invoke('multivalue_config', **nargs)
            args['ipv6_prefix_network_address'] = _result_['multivalue_handle']
        if args.get('external_ipv6_pfx_len'):
            args['ipv6_prefix_length'] = args.pop('external_ipv6_pfx_len')
        if args.get('external_count'):
            args['ipv6_prefix_number_of_addresses'] = args.pop('external_count')
    else:
        args['type'] = 'ipv4-prefix'
        if args.get('external_ip_start'):
            args['ipv4_prefix_network_address'] = args.pop('external_ip_start')
        if args.get('external_ip_step'):
            nargs = dict()
            nargs['pattern'] = 'counter'
            nargs['counter_start'] = args['ipv4_prefix_network_address']
            nargs['counter_step'] = args.pop('external_ip_step')
            nargs['counter_direction'] = 'increment'
            _result_ = rt_handle.invoke('multivalue_config', **nargs)
            args['ipv4_prefix_network_address'] = _result_['multivalue_handle']
        if args.get('external_ip_pfx_len'):
            args['ipv4_prefix_length'] = args.pop('external_ip_pfx_len')
        if args.get('external_count'):
            args['ipv4_prefix_number_of_addresses'] = args.pop('external_count')

    if args.get('external_up_down_bit') == 'None':
        args['external_up_down_bit'] = 0

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_isis_network_group_config', **args))

        if 'ipv4_prefix_interface_handle' in ret[-1]:
            v4_handles.append(ret[-1]['network_group_handle'])
        elif 'ipv6_prefix_interface_handle' in ret[-1]:
            v6_handles.append(ret[-1]['network_group_handle'])

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'network_group_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['network_group_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_arp_control(
        rt_handle,
        stream_handle=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param stream_handle
    :param port_handle

    Spirent Returns:
    {
        "arpnd_status": "1",
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global capturing
    message = '''
        Make sure The Protocols are up and running before you call j_arp_control API
        Make sure the handle provided is interface handle or traffic item or stream id
    '''
    rt_handle.log(level="INFO", message=message)
    args = dict()
    args['handle'] = stream_handle
    if stream_handle != jNone:
        new_streams = list()
        if not isinstance(stream_handle, list):
            args['handle'] = stream_handle = [stream_handle]
        for stream in args['handle']:
            if re.search(r'.*::direction\d', stream):
                new_streams.append(stream.split("::")[0])
        if len(new_streams) > 0:
            args['handle'] = stream_handle = new_streams
        if len(args['handle']) == 1:
            args['handle'] = args['handle'][0]
    if not capturing:
        args['action'] = 'regenerate'
    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]
    ret = dict()
    ret_list = list()
    if port_handle != jNone:
        if isinstance(port_handle, list):
            port_list = list()
            for port in port_handle:
                port_list = port_list + port.split()
            port_handle = port_list
        else:
            port_handle = port_handle.split()
        for port in port_handle:
            if handle_state(rt_handle, port_handle=port) != "NoTOPO":
                ret_list.append(call_protocol_info(rt_handle, jNone, 1, port))
    if stream_handle == jNone and port_handle == jNone:
        port_list = get_list_of_port_handles(rt_handle)
        stream_list = get_list_of_bound_streams(rt_handle)
        if len(port_list) > 0:
            ret_list.append(j_arp_control(rt_handle, port_handle=port_list))
        if len(stream_list) > 0:
            ret_list.append(j_arp_control(rt_handle, stream_handle=stream_list))
        stream_handle = jNone
        port_handle = jNone
        # handle_state(rt_handle, stream_handle)
        # ret_list.append(call_protocol_info(rt_handle, stream_handle, 1))
    import xml.etree.ElementTree as ET
    tree = None
    if stream_handle != jNone:
        if isinstance(stream_handle, str):
            stream_handle = [stream_handle]
        for each_stream in stream_handle:
            each_stream = "".join(each_stream).strip()
            if re.match(r'.+/ipv\d:\d+$', each_stream):
                each_stream = each_stream.strip('::ixNet::OBJ-')
                handle_state(rt_handle, each_stream)
                ret.update(call_protocol_info(rt_handle, each_stream, 1))
            elif 'trafficItem' in each_stream:
                each_stream = re.findall(r'.+/trafficItem:\d+', each_stream)
                tree = ET.fromstring(invoke_ixnet(rt_handle, "execute", "resolveAptixiaEndpoints", each_stream[0]))
            else:
                traffic_items = invoke_ixnet(rt_handle, "getList", "/traffic", "trafficItem")
                for each_traffic in traffic_items:
                    ti = invoke_ixnet(rt_handle, "getAttribute", each_traffic, "-name")
                    if ti.strip() == each_stream:
                        tree = ET.fromstring(invoke_ixnet(rt_handle, "execute", "resolveAptixiaEndpoints", each_traffic))
                        break
            if tree is not None:
                try:
                    ret.update(rt_handle._ixiangpf.traffic_control(**args))
                except:
                    pass
                traffic_set = tree.getchildren()
                dst_mac = list()
                for each_set in traffic_set:
                    children = each_set.getchildren()
                    for each_child in children:
                        if each_child.tag == 'dst_mac':
                            dst_mac.append(each_child.getchildren()[0])
                arp_list = list()
                for mac in dst_mac:
                    arp_list.append(mac.getchildren()[0].getchildren()[0].text)
                if 'removePacket' in arp_list:
                    ret['arpnd_status'] = 0
                    ret['status'] = 0
                else:
                    ret['arpnd_status'] = 1
                    ret['status'] = 1
            if len(ret) == 0:
                raise Exception("Failed to do ARP operation using j_arp_control API for {}".format(each_stream))
            ret_list.append(ret)
            ret = dict()
    # ***** Return Value Modification *****
    # ***** End of Return Value Modification *****
    if len(ret_list) == 1:
        return ret_list[0]
    else:
        status = list()
        arpnd_status = list()
        for each_ret in ret_list:
            status.append(each_ret['status'])
            arpnd_status.append(each_ret['arpnd_status'])
        ret = dict()
        ret['status'] = 1 if len(status) == status.count(1) else 0
        ret['arpnd_status'] = 1 if len(arpnd_status) == arpnd_status.count(1) else 0
        return ret

def call_protocol_info(rt_handle, handle, count, port_handle=jNone):
    def get_result(result, handle, port_handle):
        if result.get(handle):
            if port_handle != jNone:
                session_dt = result[handle]['aggregate'].get(port_handle)
            else:
                session_dt = result[handle].get('aggregate')
            if session_dt == None:
                return 0
            down = session_dt['sessions_down']
            up = session_dt['sessions_up']
            total = session_dt['sessions_total']
            if 'n/a' in total or 'N/A' in total:
                raise Exception('invalid range of Total sessions when executing protocol_info via arp_control')
            elif 'n/a' in down or 'N/A' in down:
                raise Exception('invalid range of down sessions when executing protocol_info via arp_control')
            elif 'n/a' in up or 'N/A' in up:
                raise Exception('invalid range of up sessions when executing protocol_info via arp_control')
            if up != total:
                if count:
                    rt_handle.invoke('test_control', handle=handle, action='restart_down')
                    sleep(1)
                    return call_protocol_info(rt_handle, handle, 0, port_handle)['status']
                return 0
            else:
                return 1
    args = dict()
    args['mode'] = 'aggregate'
    if port_handle != jNone:
        args['port_filter'] = port_handle
    try:
        _result_ = rt_handle.invoke('protocol_info', **args)
    except:
        _result_ = dict()
    result_list = list()
    if handle == jNone:
        for hndl in _result_:
            if re.match(r'.+ipv[4|6]:\d+$', hndl):
                result_list.append(get_result(_result_, hndl, port_handle))
    else:
        result_list.append(get_result(_result_, handle, port_handle))
    if len(result_list) == result_list.count(1):
        return {'status' : 1, 'arpnd_status': 1}
    else:
        return {'status' : 0, 'arpnd_status': 0}

def handle_state(rt_handle, handle=jNone, port_handle=jNone):
    """ handle_state """
    if port_handle != jNone:
        topology = get_topology_handle(rt_handle, get_vport_handle(rt_handle, port_handle))
        status = list()
        if topology == None:
            msg = "Could not retrive topology handle from port handle <{}>".format(port_handle)
            rt_handle.log(level="info", message=msg)
            return "NoTOPO"
        status.append(invoke_ixnet(rt_handle, 'getAttribute', topology, '-status'))
        if 'notStarted' in status or 'mixed' in status:
            invoke_ixnet(rt_handle, 'execute', 'start', topology)
            wait_on_state(rt_handle, topology, '-status', 'started')
    elif handle == jNone:
        handle = invoke_ixnet(rt_handle, 'getList', '/', 'topology')
        status = list()
        for hndl in handle:
            status.append(invoke_ixnet(rt_handle, 'getAttribute', hndl, '-status'))
        if 'notStarted' in status or 'mixed' in status:
            rt_handle.invoke('test_control', action='start_all_protocols')
            wait_on_state(rt_handle, hndl, '-status', 'started')
    else:
        status = invoke_ixnet(rt_handle, 'getAttribute', handle, '-status')
        if 'notStarted' in status or 'mixed' in status:
            rt_handle.invoke('test_control', action='start_all_protocols')
            wait_on_state(rt_handle, handle, '-status', 'started')

def wait_on_state(rt_handle, handle_obj, attribute, state, sleep_time=0.5, loops=10):
    """wait_on_state"""
    verdict = False
    for loop in range(loops):
        value = invoke_ixnet(rt_handle, 'getAttribute', handle_obj, attribute)
        if value.strip().lower() == state.strip().lower():
            break
            verdict = True
        else:
            sleep(sleep_time)
    return verdict

def j_pppox_server_config(
        rt_handle,
        attempt_rate=jNone,
        auth_mode=jNone,
        auth_req_timeout=jNone,
        config_req_timeout=jNone,
        disconnect_rate=jNone,
        echo_req_interval=jNone,
        handle=jNone,
        intermediate_agent=jNone,
        ipcp_req_timeout=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        max_auth_req=jNone,
        max_configure_req=jNone,
        max_ipcp_req=jNone,
        max_outstanding=jNone,
        max_padi_req=jNone,
        max_padr_req=jNone,
        max_terminate_req=jNone,
        num_sessions=jNone,
        padi_req_timeout=jNone,
        padr_req_timeout=jNone,
        password_wildcard=jNone,
        qinq_incr_mode=jNone,
        username_wildcard=jNone,
        vlan_id=jNone,
        vlan_id_count=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_count=jNone,
        vlan_id_outer_step=jNone,
        vlan_outer_user_priority=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        username=jNone,
        password=jNone,
        ip_cp=jNone,
        ipv4_pool_addr_start=jNone,
        ipv4_pool_addr_prefix_len=jNone,
        ipv6_pool_addr_start=jNone,
        ipv6_pool_addr_prefix_len=jNone,
        intf_ip_addr=jNone,
        intf_ip_prefix_length=jNone,
        protocol=jNone,
        mode=jNone,
        encap=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param attempt_rate - <1-1000>
    :param auth_mode - <none|pap|chap|pap_or_chap>
    :param auth_req_timeout
    :param config_req_timeout - <1-120>
    :param disconnect_rate - <1-1000>
    :param echo_req_interval - <1-3600>
    :param handle
    :param intermediate_agent
    :param ipcp_req_timeout - <1-120>
    :param mac_addr
    :param mac_addr_step
    :param max_auth_req
    :param max_configure_req - <1-255>
    :param max_ipcp_req - <1-255>
    :param max_outstanding - <2-1000>
    :param max_padi_req
    :param max_padr_req
    :param max_terminate_req - <1-65535>
    :param num_sessions - <1-32000>
    :param padi_req_timeout
    :param padr_req_timeout
    :param password_wildcard - <1|0>
    :param qinq_incr_mode - <inner|outer|both>
    :param username_wildcard - <1|0>
    :param vlan_id - <0-4095>
    :param vlan_id_count - <1-4094>
    :param vlan_id_outer - <0-4095>
    :param vlan_id_outer_count - <1-4094>
    :param vlan_id_outer_step - <0-4094>
    :param vlan_outer_user_priority - <0-7>
    :param vlan_id_step - <1-4095>
    :param vlan_user_priority - <0-7>
    :param username
    :param password
    :param ip_cp - <ipv4_cp|ipv6_cp|ipv4v6_cp:dual_stack>
    :param ipv4_pool_addr_start
    :param ipv4_pool_addr_prefix_len
    :param ipv6_pool_addr_start
    :param ipv6_pool_addr_prefix_len
    :param intf_ip_addr
    :param intf_ip_prefix_length
    :param protocol - <pppoe|pppoa|pppoeoa>
    :param mode - <create:add|modify|reset:remove>
    :param encap - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq|vc_mux|llcsnap>
    :param port_handle

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "port_handle": "port1",
        "pppox_port": "pppoxportconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/range:HLAPI0",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1",
        "pppox_server_handle": "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1",
        "pppox_server_sessions_handle": "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1/pppoxServerSessions",
        "status": "1"
    }

    Common Return Keys:
        "handles"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    vlan_args = dict()
    args['attempt_rate'] = attempt_rate
    args['auth_mode'] = auth_mode
    args['auth_req_timeout'] = auth_req_timeout
    args['config_req_timeout'] = config_req_timeout
    args['disconnect_rate'] = disconnect_rate
    args['echo_req_interval'] = echo_req_interval
    args['handle'] = handle
    args['intermediate_agent'] = intermediate_agent
    args['ipcp_req_timeout'] = ipcp_req_timeout
    args['mac_addr'] = mac_addr
    args['mac_addr_step'] = mac_addr_step
    args['max_auth_req'] = max_auth_req
    args['max_configure_req'] = max_configure_req
    args['max_ipcp_req'] = max_ipcp_req
    args['max_outstanding'] = max_outstanding
    args['max_padi_req'] = max_padi_req
    args['max_padr_req'] = max_padr_req
    args['max_terminate_req'] = max_terminate_req
    args['num_sessions'] = num_sessions
    args['padi_req_timeout'] = padi_req_timeout
    args['padr_req_timeout'] = padr_req_timeout
    args['password_wildcard'] = password_wildcard
    args['qinq_incr_mode'] = qinq_incr_mode
    args['username_wildcard'] = username_wildcard
    vlan_args['vlan_id'] = vlan_id
    vlan_args['vlan_id_count'] = vlan_id_count
    vlan_args['vlan_id_outer'] = vlan_id_outer
    vlan_args['vlan_id_outer_count'] = vlan_id_outer_count
    vlan_args['vlan_id_outer_step'] = vlan_id_outer_step
    vlan_args['vlan_outer_user_priority'] = vlan_outer_user_priority
    vlan_args['vlan_id_step'] = vlan_id_step
    vlan_args['vlan_user_priority'] = vlan_user_priority
    args['username'] = username
    args['password'] = password
    args['ipv4_pool_addr_start'] = ipv4_pool_addr_start
    args['ipv4_pool_addr_prefix_len'] = ipv4_pool_addr_prefix_len
    args['ipv6_pool_addr_start'] = ipv6_pool_addr_start
    args['ipv6_pool_prefix_len'] = ipv6_pool_addr_prefix_len
    args['ppp_local_ip'] = intf_ip_addr
    args['intf_ip_prefix_length'] = intf_ip_prefix_length
    args['protocol'] = protocol
    args['encap'] = encap
    args['port_handle'] = port_handle
    args['mode'] = mode
    args['ip_cp'] = ip_cp


    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_pppox_server_config.__doc__, **args)
    vlan_args = get_arg_value(rt_handle, j_pppox_server_config.__doc__, **vlan_args)
    if args.get('ipv4_pool_addr_start'):
        args['ppp_peer_ip'] = args.pop('ipv4_pool_addr_start')
    if args.get('ipv4_pool_addr_prefix_len'):
        args['client_netmask'] = args.pop('ipv4_pool_addr_prefix_len')
    if args.get('ipv6_pool_addr_start'):
        args['ipv6_pool_prefix'] = args.pop('ipv6_pool_addr_start')
    if args.get('ipv6_pool_addr_prefix_len'):
        args['ipv6_pool_prefix_len'] = args.pop('ipv6_pool_addr_prefix_len')
    if args.get('intf_ip_addr'):
        args['ppp_local_ip'] = args.pop('intf_ip_addr')
    if args.get('intf_ip_prefix_length'):
        args['server_netmask'] = args.pop('intf_ip_prefix_length')
    args['port_role'] = 'network'

    if ip_cp == 'ipv4':
        args['ip_cp'] = 'ipv4_cp'
        args['server_ipv4_ncp_configuration'] = 'serveronly'
    elif ip_cp == 'ipv6':
        args['ip_cp'] = 'ipv6_cp'
        args['server_ipv6_ncp_configuration'] = 'serveronly'

    if 'client_netmask' in args:
        args['client_netmask'] = cidr_to_netmask(args['client_netmask'])
    if 'server_netmask' in args:
        args['server_netmask'] = cidr_to_netmask(args['server_netmask'])

    if mode == 'create':
        if args.get('port_handle'):
            handle = create_deviceGroup(rt_handle, args.pop('port_handle'))
            handle = handle['device_group_handle']
        elif not args.get('handle'):
            raise Exception("Please pass either handle or port_handle to the function call")

    if mode == 'modify' or args.get('mode') == "remove":
        if 'pppoxserver' in handle:
            handle = __get_parent_handle(handle, "pppoxserver")

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if re.match(r"\d+\/\d+\/\d+", hndl):
            args['port_handle'] = hndl
        else:
            args['handle'] = hndl
        ret.append(rt_handle.invoke('pppox_config', **args))
        if vlan_args:
            if mode == 'create':
                vlan_config(rt_handle, vlan_args, ret[-1]['pppox_server_handle'])
            else:
                vlan_config(rt_handle, vlan_args, hndl)
        # if 'pppox_server_handle' in ret[-1]:
            # ret[-1]['handles'] = ret[-1]['pppox_server_handle']
        if 'pppox_server_sessions_handle' in ret[-1]:
            ret[-1]['handles'] = ret[-1]['pppox_server_sessions_handle']

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_pppox_server_control(rt_handle, action=jNone, handle=jNone):
    """
    :param rt_handle:       RT object
    :param action - <abort|connect|disconnect|reset>
    :param handle

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    args = get_arg_value(rt_handle, j_pppox_server_control.__doc__, **args)

    if 'pppoxServerSessions' in handle:
        handle = __get_parent_handle(handle, "pppoxserver")

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('pppox_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_pppox_server_stats(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <aggregate|session>

    Spirent Returns:
    {
        "aggregate": {
            "abort": "0",
            "atm_mode": "0",
            "avg_setup_time": "0",
            "chap_auth_rx": "1",
            "chap_auth_tx": "2",
            "connect_attempts": "0",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "disconnect_failed": "0",
            "disconnect_success": "0",
            "disconnecting": "0",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_rsp_rx": "0",
            "echo_rsp_tx": "0",
            "idle": "0",
            "ipcp_rx": "3",
            "ipcp_tx": "3",
            "ipcpv6_rx": "0",
            "ipcpv6_tx": "0",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "max_setup_time": "0",
            "min_setup_time": "0",
            "num_sessions": "1",
            "padi_rx": "1",
            "padi_tx": "0",
            "pado_rx": "0",
            "pado_tx": "1",
            "padr_rx": "1",
            "padr_tx": "0",
            "pads_rx": "0",
            "pads_tx": "1",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_rx": "0",
            "pap_auth_tx": "0",
            "session_retried": "0",
            "sessions_down": "0",
            "sessions_up": "1",
            "success_setup_rate": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "port_handle": "port1",
        "session": {
            "host1": {
                "abort": "0",
                "atm_mode": "0",
                "chap_auth_rx": "1",
                "chap_auth_tx": "2",
                "connect_success": "1",
                "connected": "1",
                "connecting": "0",
                "disconnect_failed": "0",
                "disconnect_success": "0",
                "disconnecting": "0",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "idle": "0",
                "ipcp_rx": "3",
                "ipcp_tx": "3",
                "ipcpv6_rx": "0",
                "ipcpv6_tx": "0",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "padi_rx": "1",
                "pado_tx": "1",
                "padr_rx": "1",
                "pads_tx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_rx": "0",
                "pap_auth_tx": "0",
                "sessions_down": "0",
                "sessions_up": "1",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0"
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "Range 1/25/2 2 False": {
            "aggregate": {
                "auth_avg_time": "2727.30",
                "auth_max_time": "27273",
                "auth_min_time": "27273",
                "avg_setup_time": "8464.20",
                "chap_auth_chal_tx": "1",
                "chap_auth_fail_tx": "0",
                "chap_auth_rsp_rx": "1",
                "chap_auth_succ_tx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "connect_success": "1",
                "connected": "1",
                "connecting": "0",
                "device_group": "Range 1/25/2 2 False",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_resp_rx": "0",
                "echo_resp_tx": "0",
                "idle": "9",
                "interfaces_in_chap_negotiation": "0",
                "interfaces_in_ipcp_negotiation": "0",
                "interfaces_in_ipv6cp_negotiation": "0",
                "interfaces_in_lcp_negotiation": "0",
                "interfaces_in_pap_negotiation": "0",
                "interfaces_in_ppp_negotiation": "0",
                "interfaces_in_pppoe_l2tp_negotiation": "0",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "0",
                "ipcp_cfg_nak_tx": "1",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "2",
                "ipcp_cfg_req_tx": "1",
                "ipv6_cp_router_solicitaion_rx": "0",
                "ipv6cp_avg_time": "0.00",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_max_time": "0",
                "ipv6cp_min_time": "0",
                "ipv6cp_router_adv_tx": "0",
                "lcp_avg_latency": "4736.20",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_max_latency": "47362",
                "lcp_min_latency": "47362",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "ncp_avg_latency": "573.80",
                "ncp_max_latency": "5738",
                "ncp_min_latency": "5738",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "num_sessions": "10",
                "padi_rx": "1",
                "pado_tx": "1",
                "padr_rx": "1",
                "pads_tx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_tx": "0",
                "pap_auth_nak_tx": "0",
                "pap_auth_req_rx": "0",
                "ppp_total_bytes_rx": "92",
                "ppp_total_bytes_tx": "147",
                "pppoe_avg_latency": "413.50",
                "pppoe_max_latency": "4135",
                "pppoe_min_latency": "4135",
                "pppoe_total_bytes_rx": "20",
                "pppoe_total_bytes_tx": "36",
                "sessions_down": "0",
                "sessions_failed": "0",
                "sessions_initiated": "9",
                "sessions_up": "1",
                "teardown_failed": "0",
                "teardown_succeded": "0",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0"
            }
        },
        "aggregate": {
            "auth_avg_time": "2727.30",
            "auth_max_time": "27273",
            "auth_min_time": "27273",
            "avg_setup_time": "8464.20",
            "chap_auth_chal_tx": "1",
            "chap_auth_fail_tx": "0",
            "chap_auth_rsp_rx": "1",
            "chap_auth_succ_tx": "1",
            "code_rej_rx": "0",
            "code_rej_tx": "0",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "device_group": "Range 1/25/2 2 False",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_resp_rx": "0",
            "echo_resp_tx": "0",
            "idle": "9",
            "interfaces_in_chap_negotiation": "0",
            "interfaces_in_ipcp_negotiation": "0",
            "interfaces_in_ipv6cp_negotiation": "0",
            "interfaces_in_lcp_negotiation": "0",
            "interfaces_in_pap_negotiation": "0",
            "interfaces_in_ppp_negotiation": "0",
            "interfaces_in_pppoe_l2tp_negotiation": "0",
            "ipcp_cfg_ack_rx": "1",
            "ipcp_cfg_ack_tx": "1",
            "ipcp_cfg_nak_rx": "0",
            "ipcp_cfg_nak_tx": "1",
            "ipcp_cfg_rej_rx": "0",
            "ipcp_cfg_rej_tx": "0",
            "ipcp_cfg_req_rx": "2",
            "ipcp_cfg_req_tx": "1",
            "ipv6_cp_router_solicitaion_rx": "0",
            "ipv6cp_avg_time": "0.00",
            "ipv6cp_cfg_ack_rx": "0",
            "ipv6cp_cfg_ack_tx": "0",
            "ipv6cp_cfg_nak_rx": "0",
            "ipv6cp_cfg_nak_tx": "0",
            "ipv6cp_cfg_rej_rx": "0",
            "ipv6cp_cfg_rej_tx": "0",
            "ipv6cp_cfg_req_rx": "0",
            "ipv6cp_cfg_req_tx": "0",
            "ipv6cp_max_time": "0",
            "ipv6cp_min_time": "0",
            "ipv6cp_router_adv_tx": "0",
            "lcp_avg_latency": "4736.20",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "lcp_max_latency": "47362",
            "lcp_min_latency": "47362",
            "lcp_protocol_rej_rx": "0",
            "lcp_protocol_rej_tx": "0",
            "lcp_total_msg_rx": "2",
            "lcp_total_msg_tx": "2",
            "ncp_avg_latency": "573.80",
            "ncp_max_latency": "5738",
            "ncp_min_latency": "5738",
            "ncp_total_msg_rx": "3",
            "ncp_total_msg_tx": "3",
            "num_sessions": "10",
            "padi_rx": "1",
            "pado_tx": "1",
            "padr_rx": "1",
            "pads_tx": "1",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_tx": "0",
            "pap_auth_nak_tx": "0",
            "pap_auth_req_rx": "0",
            "ppp_total_bytes_rx": "92",
            "ppp_total_bytes_tx": "147",
            "pppoe_avg_latency": "413.50",
            "pppoe_max_latency": "4135",
            "pppoe_min_latency": "4135",
            "pppoe_total_bytes_rx": "20",
            "pppoe_total_bytes_tx": "36",
            "sessions_down": "0",
            "sessions_failed": "0",
            "sessions_initiated": "9",
            "sessions_up": "1",
            "teardown_failed": "0",
            "teardown_succeded": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "session": {
            "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1/item:1": {
                "ac_mac_addr": "00:11:02:00:00:01",
                "ac_name": "",
                "auth_establishment_time": "27273",
                "auth_id": "user",
                "auth_password": "secret",
                "auth_protocol_rx": "None",
                "auth_protocol_tx": "CHAP",
                "auth_total_rx": "1",
                "auth_total_tx": "2",
                "call_state": "Idle",
                "cdn_rx": "0",
                "cdn_tx": "0",
                "chap_auth_chal_tx": "1",
                "chap_auth_fail_tx": "0",
                "chap_auth_role": "Peer",
                "chap_auth_rsp_rx": "1",
                "chap_auth_succ_tx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "data_ns": "0",
                "destination_ip": "0.0.0.0",
                "destination_port": "0",
                "device_group": "Range 1/25/2 2 False",
                "device_id": "1",
                "dns_server_list": "Not Available",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_resp_rx": "0",
                "echo_resp_tx": "0",
                "establishment_time": "84642",
                "gateway_ip": "0.0.0.0",
                "generic_error_tag_tx": "0",
                "host_mac_addr": "00:11:01:00:00:01",
                "host_name": "Not Available",
                "iccn_rx": "0",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "0",
                "ip_cpe_establishment_time": "5738",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "0",
                "ipcp_cfg_nak_tx": "1",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "2",
                "ipcp_cfg_req_tx": "1",
                "ipcp_state": "NCP Open",
                "ipcp_terminate_ack_rx": "0",
                "ipcp_terminate_ack_tx": "0",
                "ipcp_terminate_req_rx": "0",
                "ipcp_terminate_req_tx": "0",
                "ipv6_addr": "0:0:0:0:0:0:0:0",
                "ipv6_cp_router_solicitaion_rx": "0",
                "ipv6_cpe_establishment_time": "0",
                "ipv6_prefix_len": "0",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_router_adv_tx": "0",
                "ipv6cp_state": "NCP Disable",
                "ipv6cp_terminate_ack_rx": "0",
                "ipv6cp_terminate_ack_tx": "0",
                "ipv6cp_terminate_req_rx": "0",
                "ipv6cp_terminate_req_tx": "0",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_establishment_time": "47362",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "local_ip_addr": "1.1.1.1",
                "local_ipv6_iid": "Not Available",
                "loopback_detected": "False",
                "magic_no_negotiated": "True",
                "magic_no_rx": "771179460",
                "magic_no_tx": "3769293702",
                "mru": "1500",
                "mtu": "1500",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "negotiation_end_ms": "534096587",
                "negotiation_start_ms": "534011945",
                "our_call_id": "0",
                "our_cookie": "Not Available",
                "our_cookie_length": "0",
                "our_tunnel_id": "0",
                "padi_rx": "1",
                "pado_tx": "1",
                "padr_rx": "1",
                "pads_tx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_tx": "0",
                "pap_auth_nak_tx": "0",
                "pap_auth_req_rx": "0",
                "peer_call_id": "0",
                "peer_ipv6_iid": "Not Available",
                "peer_tunnel_id": "0",
                "ppp_close_mode": "None",
                "ppp_state": "PPP Connected",
                "ppp_total_rx": "92",
                "ppp_total_tx": "147",
                "pppoe_latency": "4135",
                "pppoe_state": "Session",
                "pppoe_total_bytes_rx": "20",
                "pppoe_total_bytes_tx": "36",
                "primary_wins_server": "0.0.0.0",
                "protocol": "PPPoX Server 1",
                "relay_session_id_tag_rx": "0",
                "remote_ip_addr": "1.1.1.2",
                "secondary_wins_server": "0.0.0.0",
                "service_name": "",
                "session_id": "1",
                "source_ip": "0.0.0.0",
                "source_port": "0",
                "status": "up",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "topology": "T 1/25/2",
                "tunnel_state": "Tunnel Idle",
                "vendor_specific_tag_rx": "0"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "aggregate"
        "session"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_pppox_server_stats.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        stats = dict()
        args['mode'] = 'aggregate'
        stats.update(rt_handle.invoke('pppox_stats', **args))
        args['mode'] = 'session'
        stats.update(rt_handle.invoke('pppox_stats', **args))
        args['mode'] = 'session_dhcpv6pd'
        stats.update(rt_handle.invoke('pppox_stats', **args))
        if 'session' in stats:
            for key in list(stats['session']):
                stats['session'][args['handle']] = stats['session'][key]
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                ret[index]['aggregate'] = ret[index][key]['aggregate']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ptp_config(
        rt_handle,
        mode=jNone,
        port_handle=jNone,
        handle=jNone,
        log_announce_interval=jNone,
        announce_receipt_timeout=jNone,
        log_sync_interval=jNone,
        log_delay_req_interval=jNone,
        role=jNone,
        communication_mode=jNone,
        transport_type=jNone,
        master_mac_address=jNone,
        master_mac_increment_by=jNone,
        slave_mac_address=jNone,
        slave_mac_increment_by=jNone,
        master_ip_address=jNone,
        master_ip_increment_by=jNone,
        slave_ip_address=jNone,
        slave_ip_increment_by=jNone,
        master_ipv6_address=jNone,
        master_ipv6_increment_by=jNone,
        slave_ipv6_address=jNone,
        slave_ipv6_increment_by=jNone,
        first_clock=jNone,
        clock_class=jNone,
        port_number=jNone,
        domain=jNone,
        announce_frequency_traceable=jNone,
        step_mode=jNone,
        announce_time_traceable=jNone,
        announce_leap59=jNone,
        announce_leap61=jNone,
        clock_accuracy=jNone,
        priority1=jNone,
        priority2=jNone,
        signal_unicast_handling=jNone,
        use_clock_identity=jNone,
        current_utc_offset=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_length=jNone,
        intf_ipv6_addr=jNone,
        intf_ipv6_addr_step=jNone,
        intf_prefixv6_length=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        neighbor_intf_ipv6_addr=jNone,
        neighbor_intf_ipv6_addr_step=jNone,
        vlan_id1=jNone,
        vlan_id2=jNone,
        vlan_id_mode1=jNone,
        vlan_id_mode2=jNone,
        vlan_id_step1=jNone,
        vlan_id_step2=jNone,
        vlan_priority1=jNone,
        vlan_priority2=jNone,
        multicastAddress=jNone,
        offset_scaled_log_variance=jNone):
    """
    :param rt_handle   RT object
    :param mode - <create|delete|modify>
    :param port_handle
    :param handle
    :param log_announce_interval
    :param announce_receipt_timeout
    :param log_sync_interval
    :param log_delay_req_interval
    :param role
    :param communication_mode
    :param transport_type
    :param master_mac_address
    :param master_mac_increment_by
    :param slave_mac_address
    :param slave_mac_increment_by
    :param master_ip_address
    :param master_ip_increment_by
    :param slave_ip_address
    :param slave_ip_increment_by
    :param master_ipv6_address
    :param master_ipv6_increment_by
    :param slave_ipv6_address
    :param slave_ipv6_increment_by
    :param first_clock
    :param clock_class
    :param vlan_id1 - <0 - 4095>
    :param port_number
    :param domain
    :param announce_frequency_traceable
    :param step_mode
    :param announce_time_traceable
    :param announce_leap59
    :param announce_leap61
    :param clock_accuracy
    :param priority1
    :param priority2
    :param signal_unicast_handling
    :param use_clock_identity
    :param current_utc_offset
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_length
    :param intf_ipv6_addr
    :param intf_ipv6_addr_step
    :param intf_prefixv6_length
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param neighbor_intf_ipv6_addr
    :param neighbor_intf_ipv6_addr_step
    :param vlan_id2 - <0 - 4095>
    :param vlan_id_mode1 - <fixed|increment>
    :param vlan_id_mode2 - <fixed|increment>
    :param vlan_id_step1 - <0-4095>
    :param vlan_id_step2 - <0-4095>
    :param vlan_priority1 - <0-7>
    :param vlan_priority2 - <0-7>
    :param multicastAddress
    :param offset_scaled_log_variance

    Spirent Returns:
    {
        "port_handle": port1
        "handle": router1
        "status": "1"
    }

    IXIA Returns:
    {
        "ptp_handle": "/topology:2/deviceGroup:1/ethernet:1/ptp:1
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args = get_arg_value(rt_handle, j_emulation_ptp_config.__doc__, **args)
    args['handle'] = handle
    args['parent_handle'] = port_handle
    args['log_announce_interval'] = log_announce_interval
    args['announce_receipt_timeout'] = announce_receipt_timeout
    args['log_sync_interval'] = log_sync_interval
    args['log_delay_req_interval'] = log_delay_req_interval
    if role is jNone:
        args['role'] = 'master'
    else:
        args['role'] = role
    if transport_type == 'ethernet_ii':
        args['master_mac_address'] = master_mac_address
        args['master_mac_increment_by'] = master_mac_increment_by
        args['slave_mac_address'] = slave_mac_address
        args['slave_mac_increment_by'] = slave_mac_increment_by
    elif transport_type == 'ipv4':
        args['master_ip_address'] = master_ip_address
        args['master_ip_increment_by'] = master_ip_increment_by
        args['slave_ip_address'] = slave_ip_address
        args['slave_ip_increment_by'] = slave_ip_increment_by
    elif transport_type == 'ipv6':
        args['master_ipv6_address'] = master_ipv6_address
        args['master_ipv6_increment_by'] = master_ip_increment_by
        args['slave_ipv6_address'] = slave_ipv6_address
        args['slave_ipv6_increment_by'] = slave_ipv6_increment_by
    else:
        raise Exception("Error: argument transport_type is not defined")
    args['first_clock'] = first_clock
    args['clock_class'] = clock_class
    args['port_number'] = port_number
    args['domain'] = domain
    args['announce_frequency_traceable'] = announce_frequency_traceable
    args['step_mode'] = step_mode
    args['announce_time_traceable'] = announce_time_traceable
    args['announce_leap59'] = announce_leap59
    args['announce_leap61'] = announce_leap61
    args['clock_accuracy'] = clock_accuracy
    args['priority1'] = priority1
    args['priority2'] = priority2
    args['signal_unicast_handling'] = signal_unicast_handling
    args['use_clock_identity'] = use_clock_identity
    if current_utc_offset != jNone:
        args['announce_current_utc_offset_valid'] = 1
        args['current_utc_offset'] = current_utc_offset
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_length'] = intf_prefix_length
    args['intf_ipv6_addr'] = intf_ipv6_addr
    args['intf_ipv6_addr_step'] = intf_ipv6_addr_step
    args['intf_prefixv6_length'] = intf_prefixv6_length
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['neighbor_intf_ip_addr_step'] = neighbor_intf_ip_addr_step
    args['neighbor_intf_ipv6_addr'] = neighbor_intf_ipv6_addr
    args['neighbor_intf_ipv6_addr_step'] = neighbor_intf_ipv6_addr_step
    vlan_args = dict()
    vlan_args['vlan_id1'] = vlan_id1
    vlan_args['vlan_id2'] = vlan_id2
    vlan_args['vlan_id_mode1'] = vlan_id_mode1
    vlan_args['vlan_id_mode2'] = vlan_id_mode2
    vlan_args['vlan_id_step1'] = vlan_id_step1
    vlan_args['vlan_id_step2'] = vlan_id_step2
    vlan_args['vlan_priority1'] = vlan_priority1
    vlan_args['vlan_priority2'] = vlan_priority2
    args['multicastAddress'] = multicastAddress
    args['offset_scaled_log_variance'] = offset_scaled_log_variance
    args['communication_mode'] = communication_mode

    # ***** Argument Modification *****
    # ***** End of Argument Modification *****

    # ***** Argument not supported in Spirent *****
    #args['setup_rate'] = setup_rate
    #args['teardown_rate'] = teardown_rate
    #args['override_global_rate_options'] = override_global_rate_options
    #args['style'] = style
    #args['step_mode'] = step_mode

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]
    for key in list(vlan_args.keys()):
        if vlan_args[key] == jNone:
            del vlan_args[key]

    ret = []
    if transport_type == 'ipv4' or transport_type == 'ipv6':
        command = 'ptp_over_ip_config'
        args['ip_type'] = transport_type
    else:
        command = 'ptp_over_mac_config'
    if mode == 'create':
        if 'handle' in args and command == 'ptp_over_ip_config':
            args['parent_handle'] = args['handle']
        elif port_handle is not jNone:
            topo_handle = create_topology(rt_handle, port_handle)
            args['parent_handle'] = topo_handle
        else:
            raise Exception("Error: please provide handle or port_handle")
    elif mode == 'modify':
        __check_and_raise(handle)
        args['handle'] = handle
        args['parent_handle'] = __get_parent_handle(handle, "ethernet")
    ret.append(rt_handle.invoke(command, **args))
    if vlan_args and mode != "delete":
        ethernet_handle = __get_parent_handle(ret[0]['ptp_handle'], 'ethernet')
        vlan_config(rt_handle, vlan_args, ethernet_handle)

    # ***** Return Value Modification *****
    for index in range(len(ret)):
        if 'ptp_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['ptp_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****
    return ret

def j_emulation_ptp_control(
        rt_handle,
        handle=jNone,
        action=jNone):
    """
    :param rt_handle   RT object
    :param handle
    :param action - <start|stop>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['action'] = action
    args = get_arg_value(rt_handle, j_emulation_ptp_control.__doc__, **args)

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]
    ret = []
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    for hndl in handle:
        args['handle'] = hndl
        type = re.search(r".*(ipv4|ipv6).*", hndl)
        if type:
            command = 'ptp_over_ip_control'
        else:
            command = 'ptp_over_mac_control'
        ret.append(rt_handle.invoke(command, **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****
    return ret

def j_emulation_ptp_stats(
        rt_handle,
        handle=jNone):
    """
    :param rt_handle   RT object
    :param handle

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        type = re.search(r".*(ipv4|ipv6).*", hndl)
        if type:
            command = 'ptp_over_ip_stats'
        else:
            command = 'ptp_over_mac_stats'

        stats = dict()
        args['mode'] = 'aggregate'
        stats.update(rt_handle.invoke(command, **args))
        args['mode'] = 'session'
        stats.update(rt_handle.invoke(command, **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_interface_control(
        rt_handle,
        mode=jNone,
        port_handle=jNone):
    """
    :param rt_handle   RT object
    :param mode - <break_link|restore_link>
    :param port_handle

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args = get_arg_value(rt_handle, j_interface_control.__doc__, **args)
    args['port_handle'] = port_handle
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    global device_group
    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]
    __check_and_raise(mode)
    __check_and_raise(port_handle)
    # if device_group.get(port_handle) is not None:
    root = invoke_ixnet(rt_handle, 'getRoot')
    vport = list()
    if device_group.get(port_handle) is not None:
        vport = invoke_ixnet(rt_handle, 'getAttribute', root+device_group[port_handle], "-vports")
        if len(vport) == 0:
            raise Exception("No vports associated the provided port handle {}".format(port_handle))
    else:
        vports = invoke_ixnet(rt_handle, 'getList', root, "vport")
        for vp in vports:
            vprt = invoke_ixnet(rt_handle, 'getAttribute', vp, "-assignedTo").split(":")
            vprt.pop(0)
            vprt = "/".join(vprt)
            if vprt in port_handle:
                vport.append(vp)
    if len(vport) == 0:
        raise Exception("No vports associated the provided port handle {}".format(port_handle))
    ret = {}
    try:
        if mode == "break_link":
            ret1 = invoke_ixnet(rt_handle, 'execute', "linkUpDn", vport, "down")
        elif mode == "restore_link":
            ret1 = invoke_ixnet(rt_handle, 'execute', "linkUpDn", vport, "up")
            if device_group.get(port_handle) is not None:
                nargs = dict()
                sleep(0.5)
                nargs['action'] = "start_protocol"
                nargs['handle'] = device_group[port_handle]
                rt_handle.invoke("test_control", **nargs)
        else:
            msg = "Argument mode supports only break_link and restore_link but provided {} which will not take affect".format(mode)
            rt_handle.log(level="WARNING", message=msg)
            ret['log'] = msg
        ret['status'] = 1
    except Exception as e:
        ret['status'] = 0
        ret['log'] = str(e)

    # ***** Return Value Modification *****


    # ***** End of Return Value Modification *****
    return ret


def j_save_config(
        rt_handle,
        filename=jNone):
    """
    :param rt_handle   RT object
    :param filename

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = 'save'
    filename, ext = os.path.splitext(filename)
    args['config_file'] = filename + '.ixncfg'

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(filename)

    ret = []
    try:
        ret.append(rt_handle.invoke('connect', **args))
    except:
        pass

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_packet_config_buffers(
        rt_handle,
        port_handle=jNone,
        action=jNone,
        data_plane_capture_enable=jNone,
        control_plane_capture_enable=jNone):
    """
    :param rt_handle   RT object
    :param port_handle
    :param action - <wrap|stop>
    :param data_plane_capture_enable
    :param control_plane_capture_enable

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global capture_buffer
    global capture_filter
    global capture_trigger

    args = dict()
    args = get_arg_value(rt_handle, j_packet_config_buffers.__doc__, **args)
    args['port_handle'] = port_handle
    args['capture_mode'] = 'continuous'
    args['data_plane_capture_enable'] = data_plane_capture_enable if data_plane_capture_enable != jNone else 1
    args['control_plane_capture_enable'] = control_plane_capture_enable if control_plane_capture_enable != jNone else 1

    if capture_trigger == 1:
        args['capture_mode'] = 'trigger'
    if capture_filter == 1:
        args['continuous_filter'] = 'filter'
    if capture_trigger == 1 and capture_filter == 1:
        args['after_trigger_filter'] = 'condition_filter'

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(port_handle)
    __check_and_raise(action)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    port_handle = list(set(port_handle))
    capture_buffer = 1

    ret = []
    for hndl in port_handle:
        args['port_handle'] = hndl
        ret.append(rt_handle.invoke('packet_config_buffers', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_packet_config_filter(
        rt_handle,
        port_handle=jNone,
        filter=jNone):
    """
    :param rt_handle   RT object
    :param port_handle
    :param filter

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global capture_buffer
    global capture_filter
    global capture_trigger

    args = dict()
    args['port_handle'] = port_handle
    args['mode'] = 'create'
    args['capture_filter'] = 1
    if isinstance(filter, str):
        if filter == 'invalidfcs':
            args['capture_filter_error'] = 'errBadCRC'
        elif filter == 'ipCheckSum':
            args['capture_filter_error'] = 'errAnyIpTcpUdpChecksumError'
        elif filter == 'oversize':
            args['capture_filter_error'] = 'errOversize'
        elif filter == 'undersize':
            args['capture_filter_error'] = 'errUndersize'
        elif filter == 'oos':
            args['capture_filter_error'] = 'errAnySequenceError'
    elif isinstance(filter, list):
        if filter[0] == 'length':
            args['capture_filter_framesize'] = 1
            args['capture_filter_framesize_from'] = filter[1]
            args['capture_filter_framesize_to'] = filter[1]

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(port_handle)
    __check_and_raise(filter)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    port_handle = list(set(port_handle))
    capture_filter = 1

    ret = []
    for hndl in port_handle:
        args['port_handle'] = hndl

        if capture_buffer == 1:
            nargs = dict()
            nargs['port_handle'] = hndl
            nargs['continuous_filter'] = 'filter'
            if capture_trigger == 1:
                nargs['after_trigger_filter'] = 'condition_filter'
            rt_handle.invoke('packet_config_buffers', **nargs)

        ret.append(rt_handle.invoke('packet_config_triggers', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_packet_config_triggers(
        rt_handle,
        port_handle=jNone,
        trigger=jNone):
    """
    :param rt_handle   RT object
    :param port_handle
    :param trigger

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global capture_buffer
    global capture_filter
    global capture_trigger

    args = dict()
    args['port_handle'] = port_handle
    args['mode'] = 'create'
    args['capture_trigger'] = 1
    if isinstance(trigger, str):
        if trigger == 'invalidfcs':
            args['capture_trigger_error'] = 'errBadCRC'
        elif trigger == 'ipCheckSum':
            args['capture_trigger_error'] = 'errAnyIpTcpUdpChecksumError'
        elif trigger == 'oversize':
            args['capture_trigger_error'] = 'errOversize'
        elif trigger == 'undersize':
            args['capture_trigger_error'] = 'errUndersize'
        elif trigger == 'oos':
            args['capture_trigger_error'] = 'errAnySequenceError'
    elif isinstance(trigger, list):
        if trigger[0] == 'length':
            args['capture_trigger_framesize'] = 1
            args['capture_trigger_framesize_from'] = trigger[1]
            args['capture_trigger_framesize_to'] = trigger[1]

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(port_handle)
    __check_and_raise(trigger)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    port_handle = list(set(port_handle))
    capture_trigger = 1

    ret = []
    for hndl in port_handle:
        args['port_handle'] = hndl

        if capture_buffer == 1:
            nargs = dict()
            nargs['port_handle'] = hndl
            nargs['capture_mode'] = 'trigger'
            if capture_filter == 1:
                nargs['after_trigger_filter'] = 'condition_filter'
            rt_handle.invoke('packet_config_buffers', **nargs)

        ret.append(rt_handle.invoke('packet_config_triggers', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_packet_control(
        rt_handle,
        port_handle=jNone,
        action=jNone):
    """
    :param rt_handle   RT object
    :param port_handle
    :param action - <start|stop>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global capturing

    args = dict()
    args['port_handle'] = port_handle
    args['action'] = action
    args = get_arg_value(rt_handle, j_packet_control.__doc__, **args)
    args['packet_type'] = 'both'

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(port_handle)
    __check_and_raise(action)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    args['port_handle'] = port_handle = list(set(port_handle))

    global packetCaptureObjInst

    class packetCaptureObj:
        def __init__(self, args):
            self.args = args

    capturing = 0
    if action == 'start':
        if globals().get('packetCaptureObjInst') is not None:
            port_handle_obj = packetCaptureObjInst.args.get('port_handle')
            port_handle_obj.extend(port_handle)
            packetCaptureObjInst.args['port_handle'] = list(set(port_handle_obj))
        else:
            packetCaptureObjInst = packetCaptureObj(args=args)
        capturing = 1
        return {'status' : 1}
    else:
        ret = []
        args['port_handle'] = port_handle
        ret.append(rt_handle.invoke('packet_control', **args))
        if len(ret) == 1:
            ret = ret[0]
        return ret


def j_packet_stats(
        rt_handle,
        port_handle=jNone,
        stop=jNone,
        format=jNone,
        filename=jNone,
        var_num_frames='20'):
    """
    :param rt_handle   RT object
    :param port_handle
    :param stop
    :param format
    :param filename
    :param var_num_frames

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['stop'] = stop
    args['packet_type'] = 'both'
    args['dirname'] = 'C:/capture'
    if format == 'pcap' or format == 'cap' or format == 'txt' or format == 'var':
        args['format'] = 'cap'
    else:
        raise ValueError("Supported capture formats - pcap | cap | txt | var")

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(port_handle)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    port_handle = list(set(port_handle))
    if filename == jNone:
        filename = list()
    if isinstance(filename, str):
        filename = [filename]

    if len(port_handle) > len(filename):
        file_len = len(filename)
        for index in range(file_len, len(port_handle)):
            filename.append(port_handle[index].replace('/', '-'))
    for lst_index, each_file in enumerate(filename):
        each_file = each_file.strip().rstrip('cap|pcap|pcapng|txt').rstrip('.') + '.pcap'
        if '/' in each_file:
            filename[lst_index] = each_file
            continue
        else:
            filename[lst_index] = os.path.join(rt_handle.device_logger.log_dir(), each_file)
        lst_index += 1
    ixia_log_dir = os.path.join(rt_handle.device_logger.log_dir(), 'ixia')
    if os.path.isdir(ixia_log_dir) is False:
        os.mkdir(ixia_log_dir)
    if shutil.which("mergecap") == None:
        raise FileNotFoundError("Please install mergecap")
    if format == 'txt':
        if shutil.which("tshark") == None:
            raise FileNotFoundError("Please install tshark")
    args['dirname'] = invoke_ixnet(rt_handle, 'getAttribute', '/globals/scriptgen', '-scriptFilename').split('/')
    args['dirname'].pop(-1)
    args['dirname'] = '/'.join(args['dirname'])
    ret = []
    ret_final = list()
    counter = 600
    # capture_file = args['dirname'] + '/' + filename + '.' + args['format']
    vports = invoke_ixnet(rt_handle, 'getList', '/', 'vport')
    vport_dt = dict()
    for vport in vports:
        vp_key = invoke_ixnet(rt_handle, 'getAttribute', vport, '-assignedTo').split(':')
        vp_key.pop(0)
        vp_key = "/".join(vp_key)
        vport_dt[vp_key.strip()] = vport
    rt_handle.log(level='INFO', message='{}'.format(vport_dt))
    return_filenames = list()
    for port_index, hndl in enumerate(port_handle):
        args['port_handle'] = hndl
        vp_hndl = hndl
        if re.match(r'\d+/\d+/\d+', vp_hndl):
            vp_hndl = vp_hndl.split('/')
            vp_hndl.pop(0)
            vp_hndl = "/".join(vp_hndl)
        if vport_dt.get(vp_hndl.strip()) is None:
            raise Exception('Could not retrieve vport handle from port handle {}'.format(vp_hndl))
        invoke_ixnet(rt_handle, 'execute', 'stop', vport_dt.get(vp_hndl)+'/capture', 'allTraffic')
        for i in range(counter):
            cap_run = invoke_ixnet(rt_handle, 'getAttribute', vport_dt.get(vp_hndl)+'/capture', '-isCaptureRunning')
            cap_data_state = invoke_ixnet(rt_handle, 'getAttribute', vport_dt.get(vp_hndl)+'/capture', '-dataCaptureState')
            cap_ctrl_state = invoke_ixnet(rt_handle, 'getAttribute', vport_dt.get(vp_hndl)+'/capture', '-controlCaptureState')
            cap_run = 0 if cap_run.lower() == 'true' or cap_run == 1 or cap_run == '1' else 1
            cap_data_state = 1 if cap_data_state.lower() == 'ready' else 0
            cap_ctrl_state = 1 if cap_ctrl_state.lower() == 'ready' else 0
            if cap_run and cap_data_state and cap_ctrl_state:
                break
            else:
                sleep(1)
        ret.append(rt_handle.invoke('packet_stats', **args))
        capture_file = args['dirname'] + '/' + hndl.replace('/', '-') + '_HW' + '.' + args['format']
        local_file_data = hndl.replace('/', '-') + '_data' + '.' + args['format']
        local_file_data = os.path.join(ixia_log_dir, local_file_data)
        input_handle = invoke_ixnet(rt_handle, 'readFrom', capture_file, '-ixNetRelative')
        output_handle = invoke_ixnet(rt_handle, 'writeTo', local_file_data, '-overwrite')
        invoke_ixnet(rt_handle, 'execute', 'copyFile', input_handle, output_handle)

        capture_file = args['dirname'] + '/' + hndl.replace('/', '-') + '_SW' + '.' + args['format']
        local_file_control = hndl.replace('/', '-') + '_control' + '.' + args['format']
        local_file_control = os.path.join(ixia_log_dir, local_file_control)
        input_handle = invoke_ixnet(rt_handle, 'readFrom', capture_file, '-ixNetRelative')
        output_handle = invoke_ixnet(rt_handle, 'writeTo', local_file_control, '-overwrite')
        invoke_ixnet(rt_handle, 'execute', 'copyFile', input_handle, output_handle)
        local_file_merge = filename[port_index]
        import subprocess
        subprocess.run(["mergecap -v {} {} -w {}".format(local_file_control, local_file_data, local_file_merge)],
                       stderr=subprocess.PIPE, shell=True)
        if format == 'txt':
            os.system("tshark -r {} > {}".format(local_file_merge, local_file_merge.strip('.pcap') + '.txt'))
            local_file_merge = local_file_merge.strip('.pcap') + '.txt'
        ret[-1]['capture_file'] = local_file_merge


        # ***** Adding Var Modifications *****
        if format == 'var':
            import json
            ret_var = dict()
            os.system("tshark -x -r {} -T json -c {} > {}".format(local_file_merge,\
                                                               var_num_frames,\
                                                               local_file_merge.strip('.pcap') + '.json'))
            # total_control_packets = subprocess.check_output("tshark -r " + local_file + "| wc -l", shell=True)
            # total_packets = int(total_data_packets[:-1]) + int(total_control_packets[:-1])
            #status = ret[0]['status']
            data_capture = None
            try:
                with open(local_file_merge.strip('.pcap') + '.json', 'r') as f:
                    data_capture = json.load(f)
            except Exception as e:
                raise Exception("Could not retrieve data from json file. Error: {}".format(e))

            if data_capture:
                ret_var.update({'status' : ret[-1]['status']})
                ret_var.update({hndl : {'aggregate' : {'num_frames' : str(len(data_capture))}}})
                ret_var[hndl].update({'frame' : {}})
                # capture_time = []
                # for value in data_capture:
                    # capture_time.append(value['_source']['layers']['frame']["frame.time_epoch"])
                # capture_time = sorted(capture_time)[:int(var_num_frames)]
                # for index, time in enumerate(capture_time):
                for index, packet in enumerate(data_capture):
                    raw_frames = str(packet['_source']['layers']['frame_raw'])
                    frame = re.split(r'(\w{2})', raw_frames)
                    frame = ' '.join(frame[1::2])
                    frame_length = str(packet['_source']['layers']['frame']["frame.len"])
                    ret_var[hndl]['frame'].update({index : {'length' : frame_length, 'frame' : frame}})
            else:
                ret_var.update({hndl : {'aggregate' : {'num_frames' : str(0)}}})
                ret_var[hndl].update({'frame' : {}})
            ret_final.append(ret_var)
    if format == 'var':
        ret = ret_final
        # del ret[0]['status']
    # ***** End Of Var Modifications *****

    # ***** Return Value Modification *****
    invoke_ixnet(rt_handle, 'execute', 'closeAllTabs')
    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def __get_parent_handle(handle, parent, skip_patt=0):
    """ get parent handle """
    handle = handle.split('/')
    ret_handle = []
    for handle_object in handle:
        if parent in handle_object:
            if not skip_patt:
                pattern = parent+r':\d+'
            else:
                pattern = parent
            handle_object = re.findall(pattern, handle_object)[0]
            ret_handle.append(handle_object)
            break
        else:
            ret_handle.append(handle_object)
    ret_handle = "/".join(ret_handle)
    if ret_handle == handle:
        raise Exception("Could not find the parent handle {} from handle {}".format(parent, handle))
    return ret_handle

def __config_bgp_srte(rt_handle, nargs):
    """ __config_bgp_srte """
    argDictSRT = {'srte_ip_version': '-policyType', 'srte_aspath_segment_type': '-asSetMode', 'srte_distinguisher': '-distinguisher',
                  'srte_endpoint': '-endPointV4', 'srte_local_pref': '-localPreference', 'enableLocalPreference': '-enableLocalPreference',
                  'srte_nexthop': '-ipv4NextHop', 'enableNextHop': '-enableNextHop', 'setNextHopIpType': '-setNextHopIpType',
                  'srte_origin': '-origin', 'enableOrigin':'-enableOrigin', 'srte_policy_color': '-policyColor',
                  'srte_ipv6_endpoint':'-endPointV6', 'srte_ipv6_nexthop':'-ipv6NextHop', 'srte_enable_route_target':'-active', 'srte_aspath':'-addPathId', 'srte_route_target':'-aggregatorAs'}
    argDictComm = {'srte_community': '-type'}
    argDictExtComm = {'route_type':'-type'}
    asPathDict = {}
    SegCollDict = {'srte_type1_segment_type':'-segmentType', 'srte_type1_label':'-label', 'srte_type1_sbit':'-bottomOfStack'}

    tunnelEncapDict = {'enableBinding': '-enBindingTLV', 'enableColor': '-enColorTLV', 'enablePref': '-enPrefTLV', 'srte_binding_sid': '-SID4Octet', 'srte_binding_sid_len': '-bindingSIDType', 'srte_color': '-colorValue', 'srte_preference': '-prefValue',
                       'enableRemoteEndPoint': '-enRemoteEndPointTLV', 'srte_remote_endpoint_addr': '-remoteEndpointIPv4',
                       'srte_remote_endpoint_as':'-as4Number'}
    segmentDict = {'srte_segment_list_subtlv':'-enWeight', 'srte_weight': '-weight'}

    if re.search(r'bgpIpv4Peer:\d+', nargs['handle']):
        policyHandle = invoke_ixnet(rt_handle, 'getList', nargs['handle'], 'bgpSRTEPoliciesListV4')
        policyListObj = ''.join(policyHandle)
        tunnelHandle = invoke_ixnet(rt_handle, 'getList', policyListObj, 'bgpSRTEPoliciesTunnelEncapsulationListV4')
        tunnelEncapObj = ''.join(tunnelHandle)
    elif re.search(r'bgpIpv6Peer:\d+', nargs['handle']):
        policyHandle = invoke_ixnet(rt_handle, 'getList', nargs['handle'], 'bgpSRTEPoliciesListV6')
        policyListObj = ''.join(policyHandle)
        tunnelHandle = invoke_ixnet(rt_handle, 'getList', policyListObj, 'bgpSRTEPoliciesTunnelEncapsulationListV6')
        tunnelEncapObj = ''.join(tunnelHandle)
    else:
        raise Exception("Please provide the valid handle")

    aSPathSegmentListObj = invoke_ixnet(rt_handle, 'getList', policyListObj, 'bgpAsPathSegmentList')
    aSPathSegmentListObj = ''.join(aSPathSegmentListObj)
    clusterObj = invoke_ixnet(rt_handle, 'getList', policyListObj, 'bgpClusterIdList')
    clusterObj = ''.join(clusterObj)
    bgpCommunityObj = invoke_ixnet(rt_handle, 'getList', policyListObj, 'bgpCommunitiesList')
    bgpCommunityObj = ''.join(bgpCommunityObj)
    bgpExtndCommunityObj = invoke_ixnet(rt_handle, 'getList', policyListObj, 'bgpExtendedCommunitiesList')
    bgpExtndCommunityObj = ''.join(bgpExtndCommunityObj)
    if re.search(r'bgpIpv4Peer:\d+', tunnelEncapObj):
        segmentObj = invoke_ixnet(rt_handle, 'getList', tunnelEncapObj, 'bgpSRTEPoliciesSegmentListV4')
        segmentObj = ''.join(segmentObj)
        segmentCollectionObj = invoke_ixnet(rt_handle, 'getList', segmentObj, 'bgpSRTEPoliciesSegmentsCollectionV4')

    elif re.search(r'bgpIpv6Peer:\d+', tunnelEncapObj):
        segmentObj = invoke_ixnet(rt_handle, 'getList', tunnelEncapObj, 'bgpSRTEPoliciesSegmentListV6')
        segmentObj = ''.join(segmentObj)
        segmentCollectionObj = invoke_ixnet(rt_handle, 'getList', segmentObj, 'bgpSRTEPoliciesSegmentsCollectionV6')
    segmentCollectionObj = ''.join(segmentCollectionObj)

    # ***********Modification of arguments***************************************
    if 'srte_aspath_segment_type' in nargs.keys():
        if nargs['srte_aspath_segment_type'].lower() == 'sequence':
            nargs['srte_aspath_segment_type'] = 'includelocalasasasseq'
        else:
            msg = "Argument srte_aspath_segment_type supports only <sequence>, Please provide correct value"
            raise Exception(msg)
    if 'srte_community' in nargs.keys():
        if nargs['srte_community'].lower() == 'no_export':
            nargs['srte_community'] = 'noexport'
        elif nargs['srte_community'].lower() == 'no_advertise':
            nargs['srte_community'] = 'noadvertised'
        else:
            msg = "Argument  srte_community supports only NO_EXPORT|NO_ADVERTISE,Please provide correct value"
            raise Exception(msg)
    if 'srte_local_pref' in nargs and nargs['srte_local_pref']:
        nargs['enableLocalPreference'] = 1
    if 'srte_nexthop' in nargs and nargs['srte_nexthop']:
        nargs['enableNextHop'] = 1
    if 'srte_ipv6_nexthop' in nargs and nargs['srte_ipv6_nexthop']:
        nargs['enableNextHop'] = 1
        if 'ipv4' in nargs['handle']:
            nargs['setNextHopIpType'] = 'ipv4'
        elif 'ipv6' in nargs['handle']:
            nargs['setNextHopIpType'] = 'ipv6'
    if 'srte_origin' in nargs and nargs['srte_origin']:
        nargs['enableOrigin'] = 1
    if 'srte_binding_sid' in nargs or 'srte_binding_sid_len' in nargs:
        if nargs['srte_binding_sid'] or nargs['srte_binding_sid_len']:
            nargs['enableBinding'] = 1
    if 'srte_binding_sid_len' in nargs and nargs['srte_binding_sid_len']:
        if nargs['srte_binding_sid_len'].lower() == 'length_0':
            nargs['srte_binding_sid_len'] = "nobinding"
        elif nargs['srte_binding_sid_len'].lower() == 'length_4':
            nargs['srte_binding_sid_len'] = "sid4"
        elif nargs['srte_binding_sid_len'].lower() == 'length_16':
            nargs['srte_binding_sid_len'] = "ipv6sid"
        else:
            msg = "Argument srte_binding_sid_len supports only length_0|length_4|length_16. Please provide correct values"
            raise Exception(msg)

    if 'srte_color' in nargs:
        nargs['enableColor'] = 1
    if 'srte_preference' in nargs:
        nargs['enablePref'] = 1
    if 'srte_flags' in nargs and nargs['srte_flags']:
        if not isinstance(nargs['srte_flags'], list):
            nargs['srte_flags'] = nargs['srte_flags'].split()
        for flag in nargs['srte_flags']:
            if flag.lower() == 'color':
                nargs['enableColor'] = 1
            elif flag.lower() == 'preference':
                nargs['enablePref'] = 1
            elif flag.lower() == 'binding_sid':
                nargs['enableBinding'] = 1
            elif flag.lower() == 'remote_endpoint':
                nargs['enableRemoteEndPoint'] = 1
            else:
                msg = "Provided value {} for arg srte_flags is not valid, supported values are  color|preference|binding_sid|remote_endpoint.\
                Please provide correct value".format(flag)
                raise Exception(msg)
        del nargs['srte_flags']
    if 'srte_segment_list_subtlv' in nargs:
        if nargs['srte_segment_list_subtlv'].lower() == 'weight':
            nargs['srte_segment_list_subtlv'] = 1
        else:
            nargs['srte_segment_list_subtlv'] = 0

    srtflag, comm, extcomm, aspath, tunnel, seg = 1, 1, 1, 1, 1, 1

    for arg in nargs.keys():
        if argDictSRT.get(arg):
            if srtflag:
                enableSrte = invoke_ixnet(rt_handle, 'getAttribute', policyListObj, '-active')
                invoke_ixnet(rt_handle, 'setAttribute', enableSrte+"/singleValue", "-value", 1)
                invoke_ixnet(rt_handle, 'commit')
                srtflag = 0
            if arg == 'srte_aspath_segment_type':
                if aspath:
                    enableAsPath = invoke_ixnet(rt_handle, 'getAttribute', policyListObj, '-enableAsPathSegments')
                    setAttributesMode = invoke_ixnet(rt_handle, 'getAttribute', policyListObj, '-overridePeerAsSetMode')
                    invoke_ixnet(rt_handle, 'setAttribute', enableAsPath+"/singleValue", "-value", 1)
                    invoke_ixnet(rt_handle, 'setAttribute', setAttributesMode+"/singleValue", "-value", 1)
                    invoke_ixnet(rt_handle, 'commit')
                    aspath = 0
            if re.search(r'bgpIpv6Peer:\d+', tunnelEncapObj):
                if arg == 'srte_endpoint':
                    argDictSRT[arg] = '-endPointV6'
                if arg == 'srte_nexthop':
                    argDictSRT[arg] = '-ipv6NextHop'
            if  arg == 'srte_ipv6_endpoint':
                argDictSRT[arg] = '-endPointV6'
            if arg == 'srte_ipv6_nexthop':
                argDictSRT[arg] = '-ipv6NextHop'
            multival = invoke_ixnet(rt_handle, 'getAttribute', policyListObj, argDictSRT[arg])
            invoke_ixnet(rt_handle, 'setAttribute', multival+"/singleValue", "-value", nargs[arg])
            invoke_ixnet(rt_handle, 'commit')

        if argDictComm.get(arg):
            if comm:
                enableComm = invoke_ixnet(rt_handle, 'getAttribute', policyListObj, '-enableCommunity')
                invoke_ixnet(rt_handle, 'setAttribute', enableComm+"/singleValue", "-value", 1)
                invoke_ixnet(rt_handle, 'commit')
                comm = 0
            multival = invoke_ixnet(rt_handle, 'getAttribute', bgpCommunityObj, argDictComm[arg])
            invoke_ixnet(rt_handle, 'setAttribute', multival+"/singleValue", "-value", nargs[arg])
            invoke_ixnet(rt_handle, 'commit')

        if argDictExtComm.get(arg):
            if extcomm:
                enableExtComm = invoke_ixnet(rt_handle, 'getAttribute', policyListObj, '-enableExtendedCommunity')
                invoke_ixnet(rt_handle, 'setAttribute', enableExtComm+"/singleValue", "-value", 1)
                invoke_ixnet(rt_handle, 'commit')
                extcomm = 0
            multival = invoke_ixnet(rt_handle, 'getAttribute', bgpExtndCommunityObj, argDictExtComm[arg])
            invoke_ixnet(rt_handle, 'setAttribute', multival+"/singleValue", "-value", nargs[arg])
            invoke_ixnet(rt_handle, 'commit')

        if asPathDict.get(arg):
            multival = invoke_ixnet(rt_handle, 'getAttribute', aSPathSegmentListObj, asPathDict[arg])
            invoke_ixnet(rt_handle, 'setAttribute', multival+"/singleValue", "-value", nargs[arg])
            invoke_ixnet(rt_handle, 'commit')

        if SegCollDict.get(arg):
            multival = invoke_ixnet(rt_handle, 'getAttribute', segmentCollectionObj, SegCollDict[arg])
            invoke_ixnet(rt_handle, 'setAttribute', multival+"/singleValue", "-value", nargs[arg])
            invoke_ixnet(rt_handle, 'commit')

        if tunnelEncapDict.get(arg):
            if tunnel:
                enTunnel = invoke_ixnet(rt_handle, 'getAttribute', tunnelEncapObj, '-active')
                invoke_ixnet(rt_handle, 'setAttribute', enTunnel+"/singleValue", '-value', 1)
                invoke_ixnet(rt_handle, 'commit')
                tunnel = 0
            if arg == 'srte_remote_endpoint_addr':
                if re.search(r'bgpIpv6Peer:\d+', tunnelEncapObj):
                    tunnelEncapDict[arg] = '-remoteEndpointIPv6'
            multival = invoke_ixnet(rt_handle, 'getAttribute', tunnelEncapObj, tunnelEncapDict[arg])
            invoke_ixnet(rt_handle, 'setAttribute', multival+"/singleValue", "-value", nargs[arg])
            invoke_ixnet(rt_handle, 'commit')
        if segmentDict.get(arg):
            if seg:
                enSeg = invoke_ixnet(rt_handle, 'getAttribute', segmentObj, '-active')
                invoke_ixnet(rt_handle, 'setAttribute', enSeg+"/singleValue", '-value', 1)
                invoke_ixnet(rt_handle, 'commit')
                seg = 0
            multival = invoke_ixnet(rt_handle, 'getAttribute', segmentObj, segmentDict[arg])
            invoke_ixnet(rt_handle, 'setAttribute', multival+"/singleValue", "-value", nargs[arg])
            invoke_ixnet(rt_handle, 'commit')
    return

def __check_and_raise(arg):
    """ __check_and_raise """
    if arg == jNone:
        stack = traceback.extract_stack()
        filename, lineno, function, code = stack[-2]
        orig_arg = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
        raise KeyError(
            "Please provide '" +
            orig_arg +
            "' argument to " +
            function +
            "() call")


def __get_handle(handle):
    """ __get_handle """
    if handle in handle_map:
        return handle_map[handle]

def cidr_to_netmask(cidr):
    """ cidr_to_netmask """
    cidr = int(cidr)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
    return (str((0xff000000 & mask) >> 24)   + '.' + \
        str((0x00ff0000 & mask) >> 16)   + '.' + \
        str((0x0000ff00 & mask) >> 8)    + '.' + \
        str((0x000000ff & mask)))

def get_ixia_port_handle(rt_handle, handle):
    """ get_port_handle """
    port = None
    if 'topology' in handle:
        topo = __get_parent_handle(handle, 'topology')
        vports = invoke_ixnet(rt_handle, 'getAttribute', topo, '-vports')
        port = invoke_ixnet(rt_handle, 'getAttribute', vports[0], '-assignedTo').split(':')
        port[0] = '1'
        port = "/".join(port)
    elif 'vport' in handle:
        handle = __get_parent_handle(handle, 'vport')
        port = invoke_ixnet(rt_handle, 'getAttribute', handle, '-assignedTo').split(':')
        port[0] = '1'
        port = "/".join(port)
    else:
        raise Exception('invalid handle passed {}'.format(handle))
    return port

def get_vport_handle(rt_handle, port_handle):
    """ get_ixia_port_handle """
    vports = invoke_ixnet(rt_handle, 'getList', '/', 'vport')
    found_vport = None
    if re.match(r'0/0/\d+', port_handle) and port_handle != '0/0/0':
        found_vport = vports[int(port_handle.split('/')[-1]) - 1]
    else:
        for vport in vports:
            port = invoke_ixnet(rt_handle, 'getAttribute', vport, '-assignedTo').split(':', 1)[-1].replace(':', '/')
            if port.strip() == port_handle.split('/', 1)[-1].strip():
                found_vport = vport
                break
        if found_vport is None:
            msg = 'Could not retrieve the vport from port handle {}'.format(port_handle)
            raise Exception(msg)
    return found_vport


def get_topology_handle(rt_handle, vport_handle):
    """ get_topology_handle """
    topo_handles = invoke_ixnet(rt_handle, 'getList', '/', 'topology')
    found_topo = None
    for topo in topo_handles:
        vport = invoke_ixnet(rt_handle, 'getAttribute', topo, '-vports')
        if vport_handle in vport:
            found_topo = topo
            break
    return found_topo


def create_topology(rt_handle, port_handle, topology_name=jNone):
    """ create_topology """
    global handle_map
    global device_group
    topology = get_topology_handle(rt_handle, get_vport_handle(rt_handle, port_handle))
    if topology == None:
        args = dict()
        args['mode'] = 'config'
        args['port_handle'] = port_handle
        if topology_name is not jNone:
            args['topology_name'] = topology_name
        topology = rt_handle.invoke('topology_config', **args)['topology_handle']
    try:
        handle_map[port_handle]
    except KeyError:
        handle_map[port_handle] = []
    try:
        device_group[port_handle]
    except:
        device_group[port_handle] = topology

    return topology

def create_deviceGroup(rt_handle, port_handle, intf_count=jNone, device_group_name=jNone):
    """ create_deviceGroup """
    nargs = dict()
    if device_group_name != jNone:
        nargs['device_group_name'] = device_group_name
    nargs['device_group_multiplier'] = 1 if intf_count == jNone else intf_count
    if 'deviceGroup' in port_handle:
        nargs['device_group_handle'] = port_handle
    else:
        nargs['topology_handle'] = create_topology(rt_handle, port_handle)
    nargs['mode'] = 'config'
    _result_ = rt_handle.invoke('topology_config', **nargs)
    return _result_

def __interface_config_vlan(rt_handle, args, handle=""):
    """ __interface_config_vlan """
    vlanlist = ['vlan_id', 'vlan_id_step', 'vlan_user_priority', 'vlan_tpid', 'vlan_id_mode']
    vlandict = {'vlan_id' : '-vlanId',
                'vlan_user_priority' : '-priority',
                'vlan_tpid' : '-tpid',
               }
    tagging = 0
    for arg in vlanlist:
        if args.get(arg) is not jNone and args.get(arg):
            if isinstance(args[arg], list):
                tagging = len(args[arg])
                break
            else:
                tagging = 1
                break
    if handle == "":
        if tagging > 1:
            args['vlan_id_count'] = tagging
            for arg in vlanlist:
                if args.get(arg):
                    if isinstance(args[arg], list):
                        args[arg] = ','.join([str(value) for value in args[arg]])
                    else:
                        raise Exception("Error: args {} expected list but got {}".format(arg, type(args[arg])))
        return args
    else:
        for arg in list(args.keys()):
            if args[arg] is not jNone:
                if tagging > 1:
                    if isinstance(args[arg], list) and tagging == len(args[arg]):
                        pass
                    elif arg == "connected_count":
                        continue
                    else:
                        raise Exception("Error: length of {} arg must equal the length of {}".format(arg, tagging))
            else:
                del args[arg]
        eth_handle = __get_parent_handle(handle, 'ethernet')
        invoke_ixnet(rt_handle, "setAttribute", eth_handle, "-useVlans", "true")
        invoke_ixnet(rt_handle, "setAttribute", eth_handle, "-vlanCount", tagging)
        invoke_ixnet(rt_handle, "commit")
        vlans = invoke_ixnet(rt_handle, "getList", eth_handle, "vlan")
        if len(vlans) != tagging:
            raise Exception("Error: could not create {} tagged vlans using lowlevel API".format(tagging))
        index = 0
        for vlan in vlans:
            for key in vlandict:
                attribute = ""
                if args.get(key):
                    attribute = invoke_ixnet(rt_handle, "getAttribute", vlan, vlandict[key])
                    if tagging == 1:
                        attr_value = args[key]
                        vlan_mode = args['vlan_id_mode'] if args.get('vlan_id_mode') else "fixed"
                        vlan_step = args['vlan_id_step'] if args.get('vlan_id_step') else 1
                    else:
                        attr_value = args[key][index]
                        vlan_mode = args['vlan_id_mode'][index] if args.get('vlan_id_mode') else "fixed"
                        vlan_step = args['vlan_id_step'][index] if args.get('vlan_id_step') else 1
                    if attribute is not None:
                        if key == 'vlan_id' and vlan_mode != "fixed" and 'vlan_id_repeat_count' not in args:
                            vlan_mode = "increment" if "incr" in vlan_mode.lower() else vlan_mode
                            invoke_ixnet(rt_handle, "setMultiAttribute", attribute, "-pattern", "counter", "-clearOverlays", "false")
                            invoke_ixnet(rt_handle, "setMultiAttribute", attribute+"/counter", "-start", attr_value, "-step",
                                         vlan_step, "-direction", vlan_mode)
                            invoke_ixnet(rt_handle, "commit")
                        elif 'vlan_id_repeat_count' in args and key == 'vlan_id':
                            mValue = invoke_ixnet(rt_handle, "getAttribute", vlan, "-vlanId")
                            create_vlan_multivalue(rt_handle, mValue, args, index, eth_handle)
                        else:
                            if re.match(r'^0x[0-9A-Fa-f]{4}$', str(attr_value)):
                                tpid_num = attr_value.split('0x')[1]
                                attr_value = 'ethertype'+tpid_num
                            invoke_ixnet(rt_handle, "setAttribute", attribute+"/singleValue", "-value", attr_value)
                            invoke_ixnet(rt_handle, "commit")
            index += 1
    return

def create_vlan_multivalue(rt_handle, mValue, args, index=0, ethernet_handle=""):
    """"
        This definition is specific to vlan_id_repeat_count argument
    """
    invoke_ixnet(rt_handle, "setMultiAttribute", mValue, "-clearOverlays", "false")
    custom = invoke_ixnet(rt_handle, "add", mValue, "custom")
    if args.get('vlan_id'):
        start = args['vlan_id'] if isinstance(args['vlan_id'], (str, int)) else args['vlan_id'][index]
    else:
        start = 1
    invoke_ixnet(rt_handle, "setMultiAttribute", custom, "-start", start, "-step", 0)
    invoke_ixnet(rt_handle, "commit")
    custom = invoke_ixnet(rt_handle, "remapIds", custom)
    if args.get('vlan_id_step'):
        step = args['vlan_id_step'] if isinstance(args['vlan_id_step'], (str, int)) else args['vlan_id_step'][index]
    else:
        step = 1
    if args.get('connected_count'):
        intf_count = args['connected_count'] if isinstance(args['connected_count'], (str, int)) else args['connected_count'][index]
    else:
        if ethernet_handle != "":
            intf_count = invoke_ixnet(rt_handle, "getAttribute", ethernet_handle, "-count")
        else:
            intf_count = 1
    incr1 = invoke_ixnet(rt_handle, "add", custom[0], "increment")
    invoke_ixnet(rt_handle, "setMultiAttribute", incr1, "-value", step, "-count", intf_count)
    invoke_ixnet(rt_handle, "commit")
    incr1 = invoke_ixnet(rt_handle, "remapIds", incr1)
    if args.get('vlan_id_repeat_count'):
        repeat = args['vlan_id_repeat_count'] if isinstance(args['vlan_id_repeat_count'], (str, int)) else args['vlan_id_repeat_count'][index]
    else:
        repeat = 1
    incr2 = invoke_ixnet(rt_handle, "add", incr1[0], "increment")
    invoke_ixnet(rt_handle, "setMultiAttribute", incr2, "-value", 0, "-count", repeat)
    invoke_ixnet(rt_handle, "commit")
    incr2 = invoke_ixnet(rt_handle, "remapIds", incr2)
    return

def invoke_ixnet(rt_handle, command, *args):
    """ invoke_ixnet """
    return rt_handle._invokeIxNet(command, *args)


def get_header_handle(traffic_ret, stack_val):
    """ get_header_handle """
    header_stack = traffic_ret
    if isinstance(traffic_ret, dict):
        header_stack = traffic_ret[traffic_ret["traffic_item"]]['headers']
        header_stack = header_stack.split()
    for each_header in header_stack:
        stack_match = re.match(r'(^.*%s-\d\"$)'%stack_val, each_header)
        if stack_match:
            stack_match = stack_match.group(1)
            break
    if stack_match is None:
        message = "Could not retrieve %s stack header from  the headers" %stack_val
        raise Exception(message)
    else:
        return stack_match


def get_field_handle_list(rt_handle, stack_handle, ip_option):
    """ get_field_handle_list """
    nargs = dict()
    nargs['mode'] = "get_available_fields"
    nargs['header_handle'] = stack_handle
    hndl = rt_handle.invoke('traffic_config', **nargs)
    field_list = hndl['handle'].split()
    opt_field = []
    pattern_dt = {
        "ipv4_router_alert": ['option.routerAlert', 3],
        "ipv4_nop" : ['option.nop', 1],
        "ipv4_loose_source_route" : ['option.lsrr', 2],
        "ipv4_strict_source_route" : ['option.ssrr', 2],
        "ipv4_record_route" : ['option.recordRoute', 2],
        "pointer" : ['option.pointer', 1],
        "ip_value" : ['option.routeData', 1],
        "ipv4_security" : ['option.security', 6],
        "ipv4_stream_id" : ['option.streamId', 3]
    }
    pattern = pattern_dt[ip_option][0]
    option_count = pattern_dt[ip_option][1]
    for index in range(len(field_list)-1, -1, -1):
        # field_match = re.match(pattern, field_list[index])
        if pattern in field_list[index]:
            opt_field.append(field_list[index])
            if len(opt_field) == option_count:
                break
    return opt_field


def get_user_option_values(opt_val_str):
    """ get_user_option_values """
    dict1 = dict()
    list_val = {x.split(':')[0]:x.split(':')[1] for x in opt_val_str.split()}
    return list_val


def configure_ip_options(rt_handle, ret, ip_opt_args, ipv4_header_options):
    """ configure_ip_options """
    header_hndl = get_header_handle(ret, "ipv4")
    if isinstance(ipv4_header_options,str) is True:
        ip_option_list = ipv4_header_options.split()
    else:
        ip_option_list = ipv4_header_options
    count = 0
    field_dt = {
        "ipv4_router_alert" : OrderedDict(),
        "ipv4_nop" : OrderedDict(),
        "ipv4_loose_source_route" : OrderedDict(),
        "ipv4_strict_source_route" : OrderedDict(),
        "ipv4_record_route" : OrderedDict(),
        "ipv4_security" : OrderedDict(),
        "ipv4_stream_id" : OrderedDict(),
    }
    field_dt['ipv4_router_alert']['optiontype'] = "option.routerAlert.type"
    field_dt['ipv4_router_alert']['length'] = "option.routerAlert.length"
    field_dt['ipv4_router_alert']['routeralertvalue'] = "option.routerAlert.value"
    field_dt['ipv4_nop']['optiontype'] = "option.nop"
    field_dt['ipv4_loose_source_route']['optiontype'] = "option.lsrr.type"
    field_dt['ipv4_loose_source_route']['length'] = "option.lsrr.length"
    field_dt['ipv4_strict_source_route']['optiontype'] = "option.ssrr.type"
    field_dt['ipv4_strict_source_route']['length'] = "option.ssrr.length"
    field_dt['ipv4_record_route']['optiontype'] = "option.recordRoute.type"
    field_dt['ipv4_record_route']['length'] = "option.recordRoute.length"
    field_dt['ipv4_security']['optiontype'] = "option.security.type"
    field_dt['ipv4_security']['length'] = "option.security.length"
    field_dt['ipv4_security']['security'] = "option.security.security"
    field_dt['ipv4_security']['compartments'] = "option.security.compartments"
    field_dt['ipv4_security']['handling'] = "option.security.handling"
    field_dt['ipv4_security']['tcc'] = "option.security.tcc"
    field_dt['ipv4_stream_id']['optiontype'] = "option.streamId.type"
    field_dt['ipv4_stream_id']['length'] = "option.streamId.length"
    field_dt['ipv4_stream_id']['id'] = "option.streamId.id"

    add_field_level = 0
    for ip_option in ip_option_list:
        ip_option = "ipv4_"+ip_option
        field_values = dict()
        if ip_opt_args.get(ip_option):
            field_values = get_user_option_values(ip_opt_args[ip_option])
        else:
            rt_handle.log(level="INFO", message="{} option argument is not provided so enabling with default values")
        def get_field_handle(handle_list, field):
            """ get_field_handle """
            handle = None
            for hndl in handle_list:
                if field in hndl:
                    handle = hndl
                    break
            if handle is None:
                message = "Could not retrieve the field handle for {} field".format(field)
                raise Exception(message)
            return handle
        if add_field_level:
            field_args['mode'] = 'add_field_level'
            field_args['header_handle'] = header_hndl
            field_args['field_handle'] = field_handle
            rt_handle.invoke("traffic_config", **field_args)
        field_list = get_field_handle_list(rt_handle, header_hndl, ip_option)
        for field in field_dt[ip_option]:
            field_args = dict()
            if field == 'optiontype':
                field_args['field_optionalEnabled'] = 1
            elif field == 'pointer' or field == 'ip_value':
                field_args = dict()
                field_args['mode'] = 'add_field_level'
                field_args['header_handle'] = header_hndl
                field_args['field_handle'] = field_handle
                rt_handle.invoke("traffic_config", **field_args)
                field_args = dict()
                field_list = get_field_handle_list(rt_handle, header_hndl, field)
                field_handle = get_field_handle(field_list, field_dt[ip_option][field])
                field_args['field_optionalEnabled'] = 1
                if field_values.get(field):
                    if field == 'ip_value':
                        field_args['field_valueType'] = 'valueList'
                        field_args['field_valueList'] = ip_value_to_dec(field_values[field])
                    else:
                        field_args['field_fieldValue'] = field_values[field]
            else:
                if field_values.get(field):
                    field_args['field_fieldValue'] = field_values[field]
            if len(list(field_args.keys())) > 0:
                field_handle = get_field_handle(field_list, field_dt[ip_option][field])
                field_args['mode'] = 'set_field_values'
                field_args['field_handle'] = field_handle
                field_args['header_handle'] = header_hndl
                rt_handle.invoke("traffic_config", **field_args)
        add_field_level = 1


def ip_value_to_dec(ip_value):
    """ ip_value_to_dec """
    ip_value = ip_value.split(",")
    ip_ret = list()
    for ip in ip_value:
        lst = list()
        for oct in ip.split('.'):
            oct = hex(int(oct)).split('x')[-1]
            if len(oct) == 1:
                oct = '0'+ oct
            lst.append(oct)
        ip_ret.append(int("".join(lst), 16))
    return ip_ret

def tlvConfig(rt_handle, handle, tlvArgs):
    """ tlvConfig """
    if 'dhcp_range_param_request_list' not in tlvArgs.keys():
        tlvArgs['dhcp_range_param_request_list'] = '-1'
    tlvProfiles = {
        '82' : {'name' : '{[82] DHCP Relay Agent Information}'},
        '61' : {'name' : '{[61] Client Identifier}'},
        '01' : {'name' : '{[01] Client Identifier}'},
        '55' : {'name' : '{[55] Parameter Request List}'},
        '18' : {'name' : '{[18] Interface-ID}'},
        '20' : {'name': '{[20] Reconfigure Accept}'}
    }
    requestParam = {
        '-1': None,
        '1': '{[01] Subnet Mask}',
        '3': '{[03] Router Address}',
        '6': '{[06] Domain Name Server}',
        '15': '{[15] Domain Name}',
        '33': '{[33] Static Route}',
        '44': '{[44] NetBIOS over TCP/IP Name Server}',
        '46': '{[46] NetBIOS over TCP/IP Node Type}',
        '47': '{[47] NetBIOS over TCP/IP Scope}',
        '51': '{[51] IP Address Lease Time}',
        '54': '{[54] Server Identifier}',
        '58': '{[58] Renewal (T1) Time Value}',
        '59': '{[59] Renewal (T2) Time Value}'
    }
    sub_tlv = {
        'circuit_id' : {
            'name' : '{Circuit ID}',
            'encoding' : 'string',
            'cont_level' : 0,
            'tlv_no': '82',
            'object' : 1
        },
        'circuit_id_enable' : {
            'name' : '{Circuit ID}',
            'cont_level' : 0,
            'tlv_no': '82',
            'object' : 1
        },
        'remote_id' : {
            'name' : '{Remote ID}',
            'encoding' : 'string',
            'cont_level' : 0,
            'tlv_no': '82',
            'object' : 2
        },
        'remote_id_enable': {
            'name' : '{Remote ID}',
            'cont_level' : 0,
            'tlv_no': '82',
            'object' : 2
        },
        'client_id' : {
            'name' : '{Client Identifier}',
            'encoding' : 'hex',
            'cont_level' : 1,
            'tlv_no': '61',
            'object' : 4,
            'valueObj' : 2
        },
        'client_id_enable' : {
            'name' : '{Client Identifier}',
            'cont_level' : 1,
            'tlv_no': '61',
            'object' : 4,
            'valueObj' : 2
        },
        'client_id_type' : {
            'name' : '{Hardware Type}',
            'encoding' : 'decimal',
            'cont_level' : 1,
            'tlv_no': '61',
            'object' : 4,
            'valueObj' : 1
        },
        'duid_type' : {
            'name' : 'DUID-Custom',
            'encoding' : None,
            'cont_level' : 1,
            'tlv_no': '01',
            'object' : 5
        },
        'duid_value' : {
            'name' : '{Custom DUID Byte}',
            'encoding' : 'hex',
            'cont_level' : 2,
            'tlv_no': '01',
            'object' : 5,
            'subObj' : 2,
            'valueObj' : 1
        },
        'dhcp_range_param_request_list' : {
            'name' : requestParam[tlvArgs['dhcp_range_param_request_list']],
            'encoding' : 'decimal',
            'cont_level' : -1,
            'tlv_no': '55',
            'object' : int(tlvArgs['dhcp_range_param_request_list']) + 1,
        },
        'enable_reconfig_accept' : {
            'name' : '',
            'encoding' : 'decimal',
            'cont_level' : None,
            'tlv_no': '20',
        },
        'enable_router_option': {
            'name': requestParam['3'],
            'cont_level': -1,
            'tlv_no': '55',
            'object': 4
        }
    }
    tlvs_created = get_default_tlvs(rt_handle, handle)
    for tlv_key in tlvArgs:
        if (tlv_key == 'dhcp_range_param_request_list') or (tlv_key == 'enable_router_option'):
            if sub_tlv[tlv_key]['name'] == None:
                continue
        if not list(tlvs_created.keys()).count(sub_tlv[tlv_key]['tlv_no']):
            args = dict()
            args['tlv_name'] = tlvProfiles[sub_tlv[tlv_key]['tlv_no']]['name']
            args['mode'] = 'create_tlv'
            args['handle'] = handle
            args['tlv_is_enabled'] = 1
            _result_1 = rt_handle.invoke('tlv_config', **args)
            tlvs_created.update({sub_tlv[tlv_key]['tlv_no'] : _result_1})
        tlv_value_handle = tlvs_created[sub_tlv[tlv_key]['tlv_no']]['tlv_value_handle']
        _result_ = tlvs_created[sub_tlv[tlv_key]['tlv_no']]
        if sub_tlv[tlv_key]['cont_level'] == None:
            nargs = dict()
            nargs['mode'] = 'modify'
            nargs['tlv_is_enabled'] = tlvArgs[tlv_key]
            nargs['handle'] = _result_['tlv_handle']
            rt_handle.invoke('tlv_config', **nargs)
        elif sub_tlv[tlv_key]['cont_level'] == -1:
            nargs = dict()
            nargs['mode'] = 'modify'
            tlv_no = sub_tlv[tlv_key]['tlv_no']
            nargs['handle'] = tlvs_created[tlv_no]['tlv_value_handle'] + "/object:" + \
                              str(sub_tlv[tlv_key]['object']) + "/field"
            if tlv_key == 'enable_router_option':
                nargs['field_is_enabled'] = tlvArgs[tlv_key]
            else:
                nargs['field_name'] = sub_tlv[tlv_key]['name']
                nargs['field_is_enabled'] = 1
                nargs['field_is_editable'] = 1
            rt_handle.invoke('tlv_config', **nargs)
        elif sub_tlv[tlv_key]['cont_level'] == 0:
            option_number = sub_tlv[tlv_key]['object']
            if tlv_key in ['circuit_id_enable', 'remote_id_enable']:
                field_handle = tlv_value_handle + "/object:" + str(option_number) + "/subTlv"
                invoke_ixnet(rt_handle, 'setAttribute', field_handle, "-isEnabled", tlvArgs[tlv_key])
                invoke_ixnet(rt_handle, 'commit')
            else:
                field_handle = tlv_value_handle + "/object:" + str(option_number) + "/subTlv"
                invoke_ixnet(rt_handle, 'setAttribute', field_handle, "-isEnabled", 1)
                invoke_ixnet(rt_handle, 'commit')
                nargs = dict()
                nargs['field_name'] = sub_tlv[tlv_key]['name']
                nargs['mode'] = 'modify'
                nargs['field_is_enabled'] = 1
                nargs['field_is_editable'] = 1
                nargs['field_value'] = tlvArgs[tlv_key]
                sub_tlv_handle = tlv_value_handle + "/object:" + str(option_number) + "/subTlv/value"
                tlv_no = sub_tlv[tlv_key]['tlv_no']
                if tlvs_created[tlv_no][tlv_value_handle].get(sub_tlv_handle):
                    nargs['handle'] = tlvs_created[tlv_no][tlv_value_handle][sub_tlv_handle]['tlv_field_handle']
                else:
                    nargs['handle'] = sub_tlv_handle+"/object:1/field"
                rt_handle.invoke('tlv_config', **nargs)
        else:
            objects = invoke_ixnet(rt_handle, "getList", tlv_value_handle, "object")
            for object in objects:
                invoke_ixnet(rt_handle, "setAttribute", object+"/container", "-isEnabled", 0)
                invoke_ixnet(rt_handle, "commit")
            tlv_container_handle = tlv_value_handle + "/object:" + str(sub_tlv[tlv_key]['object']) + "/container"
            if tlv_key in ['client_id_enable']:
                value = tlvArgs[tlv_key]
                invoke_ixnet(rt_handle, "setAttribute", tlv_container_handle, "-isEnabled", tlvArgs[tlv_key])
                invoke_ixnet(rt_handle, "commit")
            else:
                invoke_ixnet(rt_handle, "setAttribute", tlv_container_handle, "-isEnabled", 1)
                invoke_ixnet(rt_handle, "commit")
                nargs = dict()
                if sub_tlv[tlv_key].get('subObj'):
                    sub_cont = tlv_container_handle + \
                            '/object:' + \
                            str(sub_tlv[tlv_key]['subObj']) + \
                            '/repeatableContainer/object:' + str(sub_tlv[tlv_key]['valueObj']) + '/field'
                    nargs['handle'] = sub_cont
                    nargs['field_name'] = sub_tlv[tlv_key]['name']
                    nargs['mode'] = 'modify'
                    nargs['field_is_enabled'] = 1
                    nargs['field_is_editable'] = 1
                    nargs['field_value'] = tlvArgs[tlv_key]
                    rt_handle.invoke('tlv_config', **nargs)
                elif sub_tlv[tlv_key].get('valueObj'):
                    obj_no = str(sub_tlv[tlv_key]['valueObj'])
                    nargs = dict()
                    nargs['handle'] = tlv_container_handle + '/object:' + obj_no + '/field'
                    nargs['field_name'] = sub_tlv[tlv_key]['name']
                    nargs['mode'] = 'modify'
                    nargs['field_is_enabled'] = 1
                    nargs['field_is_editable'] = 1
                    nargs['field_value'] = tlvArgs[tlv_key]
                    rt_handle.invoke('tlv_config', **nargs)


def get_default_tlvs(rt_handle, handle):
    """ get_default_tlvs """
    tlvs_created = dict()
    tlvs = list()
    dtlv = invoke_ixnet(rt_handle, 'getList', handle+'/tlvProfile', 'defaultTlv')
    if len(dtlv) > 0:
        tlvs = tlvs + dtlv
    ntlv = invoke_ixnet(rt_handle, 'getList', handle+'/tlvProfile', 'tlv')
    if len(ntlv) > 0:
        tlvs = tlvs + ntlv
    for each_tlv in tlvs:
        name = invoke_ixnet(rt_handle, 'getAttribute', each_tlv, '-name')
        tlv_num = re.findall(r'\[(\d+)\].+', str(name))
        if len(tlv_num) > 0:
            tlv_num = tlv_num[0]
            tlvs_created[tlv_num] = dict()
            tlvs_created[tlv_num]['tlv_value_handle'] = each_tlv+'/value'
            tlvs_created[tlv_num][each_tlv+'/value'] = dict()

    return tlvs_created

def config_custom_pattern(rt_handle, traffic_item, custom_pattern, var):
    """ config_custom_pattern """
    length = len(bin(int(custom_pattern, 16))) - 2
    custom_template = '::ixNet::OBJ-/traffic/protocolTemplate:"custom"'
    header_stack = invoke_ixnet(rt_handle, "getList", traffic_item, "stack")
    invoke_ixnet(rt_handle, "execute", "appendProtocol", header_stack[-2], custom_template)
    invoke_ixnet(rt_handle, "commit")
    stack_handles = invoke_ixnet(rt_handle, "getList", traffic_item, "stack")
    custom_handle = stack_handles[-2]
    custom_len, custom_data = invoke_ixnet(rt_handle, "getList", custom_handle, "field")
    invoke_ixnet(rt_handle, 'setAttribute', custom_len, "-optionalEnabled", true)
    invoke_ixnet(rt_handle, 'setAttribute', custom_len, "-seed", 1)
    invoke_ixnet(rt_handle, 'setAttribute', custom_len, "-fieldValue", length)
    invoke_ixnet(rt_handle, 'setAttribute', custom_len, "-singleValue", length)
    invoke_ixnet(rt_handle, "commit")
    invoke_ixnet(rt_handle, 'setAttribute', custom_data, "-optionalEnabled", true)
    invoke_ixnet(rt_handle, 'setAttribute', custom_data, "-seed", 1)
    invoke_ixnet(rt_handle, 'setAttribute', custom_data, "-fieldValue", custom_pattern)
    invoke_ixnet(rt_handle, 'setAttribute', custom_data, "-singleValue", custom_pattern)
    invoke_ixnet(rt_handle, "commit")

    if var:
        for stack in range(len(stack_handles)-2):
            invoke_ixnet(rt_handle, "execute", "remove", stack_handles[stack])
            invoke_ixnet(rt_handle, "commit")

    return


def config_ethernet_pause(rt_handle, traffic_item, ethernet_pause):
    """configure ethernet pause"""
    pause_template = '::ixNet::OBJ-/traffic/protocolTemplate:"pfcPause"'
    header_stack = invoke_ixnet(rt_handle, "getList", traffic_item, "stack")
    invoke_ixnet(rt_handle, "execute", "insertProtocol", header_stack[0], pause_template)
    invoke_ixnet(rt_handle, "commit")
    stack_handles = invoke_ixnet(rt_handle, "getList", traffic_item, "stack")
    invoke_ixnet(rt_handle, "execute", "remove", stack_handles[1])
    invoke_ixnet(rt_handle, "commit")
    pause_handle = stack_handles[0]
    values = invoke_ixnet(rt_handle, "getList", pause_handle, "field")
    opcode = values[3]
    quantas = values[4:]
    header_stack = invoke_ixnet(rt_handle, "getList", traffic_item, "stack")
    invoke_ixnet(rt_handle, 'setAttribute', opcode, "-fieldValue", "0x0001")
    invoke_ixnet(rt_handle, "commit")
    for quanta in quantas:
        invoke_ixnet(rt_handle, 'setAttribute', quanta, "-fieldValue", ethernet_pause)
    invoke_ixnet(rt_handle, "commit")
    return


def get_vport_transmit_mode(rt_handle, port_handle=None):
    """ get_vport_transmit_mode """
    tx_mode = list()
    return_val = None
    if port_handle is not None:
        vport = get_vport_handle(port_handle)
        if vport is not None:
            tx_mode.append(invoke_ixnet(rt_handle, 'getAttribute', vport, '-txMode'))
        else:
            return get_vport_transmit_mode()
    else:
        vports = invoke_ixnet(rt_handle, 'getList', '/', 'vport')
        for each_vport in vports:
            tx_mode.append(invoke_ixnet(rt_handle, 'getAttribute', each_vport, '-txMode'))
    if tx_mode.count('interleaved'):
        return_val = 'advanced'
    elif tx_mode.count('interleavedCoarse'):
        return_val = 'advanced'
    elif tx_mode.count('sequential'):
        return_val = 'stream'
    elif tx_mode.count('sequentialCoarse'):
        return_val = 'stream'
    return return_val

def j_emulation_dot1x_config(
        rt_handle,
        mode=jNone,
        port_handle=jNone,
        handle=jNone,
        eap_auth_method=jNone,
        encapsulation=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        gateway_ipv6_addr=jNone,
        gateway_ipv6_addr_step=jNone,
        ip_version=jNone,
        local_ip_addr=jNone,
        local_ip_addr_step=jNone,
        local_ip_prefix_len=jNone,
        local_ipv6_addr=jNone,
        local_ipv6_addr_step=jNone,
        local_ipv6_prefix_len=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        password=jNone,
        username=jNone,
        auth_retry_count=jNone,
        auth_retry_interval=jNone,
        max_authentications=jNone,
        supplicant_auth_rate=jNone,
        num_sessions=jNone,
        vlan_id=jNone,
        vlan_ether_type=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        vlan_outer_id=jNone,
        vlan_outer_ether_type=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone,
        supplicant_logoff_rate=jNone,
        peer_certificate_file=jNone,
        certificate_directory=jNone,
        password_wildcard=jNone,
        username_wildcard=jNone,
        wildcard_pound_start=jNone,
        wildcard_pound_end=jNone):

    """
    :param rt_handle:       RT object
    :param mode - <create|modify|delete>
    :param port_handle
    :param handle
    :param eap_auth_method - <md5|fast|tls>
    :param encapsulation - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq>
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param gateway_ipv6_addr
    :param gateway_ipv6_addr_step
    :param ip_version - <ipv4|ipv6|ipv4_6>
    :param local_ip_addr
    :param local_ip_addr_step
    :param local_ip_prefix_len - <0-32>
    :param local_ipv6_addr
    :param local_ipv6_addr_step
    :param local_ipv6_prefix_len - <0-128>
    :param mac_addr
    :param mac_addr_step
    :param password
    :param username
    :param auth_retry_count - <1-100>
    :param auth_retry_interval - <1-3600>
    :param max_authentications - <1-100>
    :param supplicant_auth_rate - <1-3600>
    :param num_sessions
    :param vlan_id - <0-4095>
    :param vlan_ether_type - <0x8100|0x88A8|0x9100|0x9200>
    :param vlan_id_step - <0-4095>
    :param vlan_user_priority - <0-7>
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_ether_type - <0x8100|0x88A8|0x9100|0x9200>
    :param vlan_outer_id_step - <0-4095>
    :param vlan_outer_user_priority - <0-7>
    :param supplicant_logoff_rate - <1-1024>
    :param peer_certificate_file
    :param certificate_directory
    :param password_wildcard - <0|1>
    :param username_wildcard - <0|1>
    :param wildcard_pound_start - <0-65535>
    :param wildcard_pound_end - <0-65535>
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    nargs = dict()
    vargs = dict()
    globalDict = dict()
    args['mode'] = mode
    args['port_handle'] = port_handle
    args['handle'] = handle
    args['eap_auth_method'] = eap_auth_method
    nargs['gateway_ip_addr'] = gateway_ip_addr
    nargs['gateway_ip_addr_step'] = gateway_ip_addr_step
    nargs['gateway_ipv6_addr'] = gateway_ipv6_addr
    nargs['gateway_ipv6_addr_step'] = gateway_ipv6_addr_step
    nargs['local_ip_addr'] = local_ip_addr
    nargs['local_ip_addr_step'] = local_ip_addr_step
    nargs['local_ip_prefix_len'] = local_ip_prefix_len
    nargs['local_ipv6_addr'] = local_ipv6_addr
    nargs['local_ipv6_addr_step'] = local_ipv6_addr_step
    nargs['local_ipv6_prefix_len'] = local_ipv6_prefix_len
    nargs['mac_addr'] = mac_addr
    nargs['mac_addr_step'] = mac_addr_step
    args['password'] = password
    args['username'] = username
    args['auth_retry_count'] = auth_retry_count
    args['auth_retry_interval'] = auth_retry_interval
    args['max_authentications'] = max_authentications
    args['supplicant_auth_rate'] = supplicant_auth_rate

    args = get_arg_value(rt_handle, j_emulation_dot1x_config.__doc__, **args)
    nargs = get_arg_value(rt_handle, j_emulation_dot1x_config.__doc__, **nargs)

    if eap_auth_method == jNone:
        args['protocol_type'] = 'md5'
    else:
        args['protocol_type'] = args.pop('eap_auth_method')
    if nargs.get('gateway_ip_addr'):
        nargs['gateway'] = nargs.pop('gateway_ip_addr')
    if nargs.get('gateway_ip_addr_step'):
        nargs['gateway_step'] = nargs.pop('gateway_ip_addr_step')
    if nargs.get('gateway_ipv6_addr'):
        nargs['ipv6_gateway'] = nargs.pop('gateway_ipv6_addr')
    if nargs.get('gateway_ipv6_addr_step'):
        nargs['ipv6_gateway_step'] = nargs.pop('gateway_ipv6_addr_step')
    if nargs.get('local_ip_addr'):
        nargs['intf_ip_addr'] = nargs.pop('local_ip_addr')
    if nargs.get('local_ip_addr_step'):
        nargs['intf_ip_addr_step'] = nargs.pop('local_ip_addr_step')
    if nargs.get('local_ip_prefix_len'):
        nargs['netmask'] = nargs.pop('local_ip_prefix_len')
    if nargs.get('local_ipv6_addr'):
        nargs['ipv6_intf_addr'] = nargs.pop('local_ipv6_addr')
    if nargs.get('local_ipv6_addr_step'):
        nargs['ipv6_intf_addr_step'] = nargs.pop('local_ipv6_addr_step')
    if nargs.get('local_ipv6_prefix_len'):
        nargs['ipv6_prefix_length'] = nargs.pop('local_ipv6_prefix_len')
    if nargs.get('mac_addr'):
        nargs['src_mac_addr'] = nargs.pop('mac_addr')
    if nargs.get('mac_addr_step'):
        nargs['src_mac_addr_step'] = nargs.pop('mac_addr_step')
    if args.get('password'):
        args['user_pwd'] = args.pop('password')
    if args.get('username'):
        args['user_name'] = args.pop('username')
    if args.get('auth_retry_count'):
        args['max_start'] = args.pop('auth_retry_count')
    if args.get('auth_retry_interval'):
        args['start_period'] = args.pop('auth_retry_interval')
    if args.get('max_authentications'):
        args['successive_start'] = args.pop('max_authentications')
    if args.get('supplicant_auth_rate'):
        args['authentication_wait_period'] = args.pop('supplicant_auth_rate')

    args['tls_version'] = 'tls1_0'
    globalDict['max_teardown_rate'] = supplicant_logoff_rate
    if encapsulation == "ethernet_ii_vlan" or "ethernet_ii_qinq":
        vargs['vlan_id'] = vlan_id
        vargs['vlan_ether_type'] = vlan_ether_type
        vargs['vlan_id_step'] = vlan_id_step
        vargs['vlan_user_priority'] = vlan_user_priority
    if encapsulation == "ethernet_ii_qinq":
        vargs['vlan_outer_id'] = vlan_outer_id
        vargs['vlan_outer_ether_type'] = vlan_outer_ether_type
        vargs['vlan_outer_id_step'] = vlan_outer_id_step
        vargs['vlan_outer_user_priority'] = vlan_outer_user_priority

    if args.get('mode') == 'create':
        nargs['mode'] = 'config'

    vargs = get_arg_value(rt_handle, j_emulation_dot1x_config.__doc__, **vargs)

    for key in list(globalDict.keys()):
        if globalDict[key] == jNone:
            del globalDict[key]

    if 'netmask' in nargs:
        nargs['netmask'] = cidr_to_netmask(nargs['netmask'])

    if eap_auth_method.lower() == 'tls':
        if certificate_directory == jNone and peer_certificate_file == jNone:
            raise Exception("certificate_directory and peer_certificate_file are mandatory params for eap_auth_method TLS")
        rt_handle.log(level="WARN", message="Mandatory: Please enable FTP on the appserver to copy the certificate file to it")
        if not os.path.exists(certificate_directory):
            raise FileNotFoundError("Path Error: Provided path does not Exist")
        srcFile = "%s/%s" % (certificate_directory, peer_certificate_file)
        if not os.path.isfile(srcFile):
            raise FileNotFoundError("Provided file {0} is not present in the directory {1}".format(peer_certificate_file, certificate_directory))
        server = rt_handle.connect_args['ixnetwork_tcl_server']
        ftp_load_config(server, 'Tgen', 'Embe1mpls', srcFile)
        args['certificate_directory'] = 'C:\\inetpub\\ftproot'
        args['peer_certificate_file'] = peer_certificate_file
        args['certificate_key_in_same_file'] = True

    __check_and_raise(mode)
    if mode == 'create':
        if args.get('handle'):
            args['handle'] = handle
            if num_sessions != jNone:
                if not isinstance(handle, list):
                    handle = handle.split()
                for each_handle in handle:
                    device_group_handle = __get_parent_handle(each_handle, 'deviceGroup')
                    rt_handle.invoke("topology_config", mode='modify',\
                                      device_group_handle=device_group_handle,\
                                      device_group_multiplier=int(num_sessions))
        elif args.get('port_handle'):
            if num_sessions != jNone:
                handle = create_deviceGroup(rt_handle, port_handle, intf_count=int(num_sessions))['device_group_handle']
            else:
                handle = create_deviceGroup(rt_handle, port_handle)['device_group_handle']
            args['handle'] = handle
        else:
            raise Exception("Please pass either handle or port_handle to the function call")

    if password_wildcard in [1, '1'] or username_wildcard in [1, '1']:
        for each_pound in [wildcard_pound_start, wildcard_pound_end]:
            if each_pound == jNone:
                each_pound = 1

        if '#' in username:
            username = username.split('#')
            substitute = "{"+"Inc:"+str(wildcard_pound_start)+',1,'+str(wildcard_pound_end)+'}'
            string_pattern = substitute.join(username)
            args['user_name'] = rt_handle.invoke('multivalue_config', string_pattern=string_pattern, pattern='string')['multivalue_handle']

        if '#' in password:
            password = password.split('#')
            substitute = "{"+"Inc:"+str(wildcard_pound_start)+',1,'+str(wildcard_pound_end)+'}'
            string_pattern = substitute.join(password)
            args['user_pwd'] = rt_handle.invoke('multivalue_config', string_pattern=string_pattern, pattern='string')['multivalue_handle']

    if mode == 'modify':
        __check_and_raise(handle)
        if re.search(r'.*ipv[4|6].*', handle):
            if nargs:
                nargs['protocol_handle'] = handle
                nargs['mode'] = 'modify'
            if args:
                handle = __get_parent_handle(handle, 'dotOneX')
        else:
            if nargs:
                nargs['protocol_handle'] = __get_parent_handle(handle, 'ethernet')
                nargs['mode'] = 'modify'

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = list()
    for hndl in handle:
        args['handle'] = hndl
        ret.append(rt_handle.invoke('emulation_dotonex_config', **args))
        if globalDict:
            globalDict['handle'] = "/globals"
            globalDict['mode'] = mode
            rt_handle.invoke('emulation_dotonex_config', **globalDict)
        if nargs:
            if mode == 'create':
                handle = ret[-1]['dotonex_device_handle']
                nargs['protocol_handle'] = handle
            ret[-1].update(rt_handle.invoke('interface_config', **nargs))
        if vargs:
            vlan_config(rt_handle, vargs, hndl)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'ipv4_handle' in ret[index] and 'ipv6_handle' in ret[index]:
            ret[index]['handles'] = dict()
            ret[index]['handles']['ipv4'] = ret[index]['ipv4_handle']
            ret[index]['handles']['ipv6'] = ret[index]['ipv6_handle']
        elif 'ipv4_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['ipv4_handle']
        elif 'ipv6_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['ipv6_handle']
        elif 'dotonex_device_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['dotonex_device_handle']

    # ***** End of Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    return ret

def j_emulation_dot1x_control(
        rt_handle,
        mode=jNone,
        handle=jNone):

    """
    :param rt_handle:       RT object
    :param mode - <start|stop|logout>
    :param handle
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args['handle'] = handle

    args = get_arg_value(rt_handle, j_emulation_dot1x_control.__doc__, **args)

    __check_and_raise(handle)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = list()
    for hndl in handle:
        args['handle'] = hndl
        if mode in ['stop', 'logout']:
            hndl = __get_parent_handle(hndl, 'dotOneX')
            if mode == 'stop':
                rt_handle.invoke('emulation_dotonex_config', mode='modify', handle=hndl, disable_logoff=1)
            elif mode == 'logout':
                rt_handle.invoke('emulation_dotonex_config', mode='modify', handle=hndl, disable_logoff=0)
        ret.append(rt_handle.invoke('emulation_dotonex_control', **args))

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    return ret

def j_emulation_dot1x_stats(
        rt_handle,
        mode=jNone,
        handle=jNone):

    """
    :param rt_handle:       RT object
    :param mode
    :param handle
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    if mode == 'aggregate':
        mode = 'per_port_stats'
    elif mode == 'sessions':
        mode = 'per_session_stats'
    else:
        mode = 'per_port_stats'

    args = dict()
    args['mode'] = mode
    args['handle'] = handle

    key_list = list(args.keys())
    for key in key_list:
        if args[key] == jNone:
            del args[key]

    ret = []
    __check_and_raise(mode)
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = handle.split()

    for hndl in handle:
        args['handle'] = __get_parent_handle(hndl, 'dotOneX')
        stats = dict()
        args['mode'] = 'per_port_stats'
        stats.update(rt_handle.invoke('emulation_dotonex_info', **args))
        args['mode'] = 'per_session_stats'
        stats.update(rt_handle.invoke('emulation_dotonex_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****
    for index in range(len(ret)):
        for key in list(ret[index]):
            if 'aggregate' in ret[index][key]:
                ret[index]['aggregate'] = ret[index][key]['aggregate']
            if 'session' in ret[index][key]:
                ret[index]['session'] = ret[index][key]['session']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_test_rfc2544_config(
        rt_handle,
        mode=jNone,
        handle=jNone,
        src_port=jNone,
        dst_port=jNone,
        device_count=jNone,
        mac_addr=jNone,
        port_mac_step=jNone,
        device_mac_step=jNone,
        vlan=jNone,
        port_vlan_step=jNone,
        device_vlan_step=jNone,
        vlan_priority=jNone,
        ipv4_addr=jNone,
        port_ipv4_addr_step=jNone,
        device_ipv4_addr_step=jNone,
        ipv4_prefix_len=jNone,
        ipv4_gateway=jNone,
        port_ipv4_gateway_step=jNone,
        ipv6_addr=jNone,
        port_ipv6_addr_step=jNone,
        device_ipv6_addr_step=jNone,
        ipv6_prefix_len=jNone,
        ipv6_gateway=jNone,
        port_ipv6_gateway_step=jNone,
        endpoint_map=jNone,
        test_type='b2b',
        bidirectional=jNone,
        iteration_count=jNone,
        test_duration=jNone,
        frame_size_mode=jNone,
        frame_size=jNone,
        frame_size_start=jNone,
        frame_size_end=jNone,
        frame_size_step=jNone,
        frame_size_min=jNone,
        frame_size_max=jNone,
        load_type=jNone,
        load_unit=jNone,
        load_list=jNone,
        load_start=jNone,
        load_end=jNone,
        load_step=jNone,
        load_min=jNone,
        load_max=jNone,
        latency_type=jNone,
        start_traffic_delay=jNone,
        enable_learning=jNone,
        learning_mode=jNone,
        learning_frequency=jNone,
        learning_rate=jNone,
        l3_learning_retry_count=jNone,
        l2_learning_repeat_count=jNone,
        enable_jitter_measure=jNone,
        accept_frame_loss=jNone,
        search_mode=jNone,
        rate_lower_limit=jNone,
        rate_upper_limit=jNone,
        initial_rate=jNone,
        rate_step=jNone,
        back_off=jNone,
        resolution=jNone,
        rfc5180_enable=jNone,
        ipv6_percentage_iteration_mode=jNone,
        fixed_ipv6_percentage=jNone,
        ipv6_percentage_list=jNone,
        random_ipv6_percentage_min=jNone,
        random_ipv6_percentage_max=jNone,
        ipv6_percentage_start=jNone,
        ipv6_percentage_step=jNone,
        ipv6_percentage_end=jNone):
    """
    :param rt_handle:       RT object
    :param mode - <create|modify|delete>
    :param handle
    :param src_port
    :param dst_port
    :param device_count
    :param mac_addr
    :param port_mac_step
    :param device_mac_step
    :param vlan
    :param port_vlan_step
    :param device_vlan_step
    :param vlan_priority
    :param ipv4_addr
    :param port_ipv4_addr_step
    :param device_ipv4_addr_step
    :param ipv4_prefix_len
    :param ipv4_gateway
    :param port_ipv4_gateway_step
    :param ipv6_addr
    :param port_ipv6_addr_step
    :param device_ipv6_addr_step
    :param ipv6_prefix_len
    :param ipv6_gateway
    :param port_ipv6_gateway_step
    :param endpoint_map
    :param test_type
    :param bidirectional
    :param iteration_count
    :param test_duration
    :param frame_size_mode
    :param frame_size
    :param frame_size_start
    :param frame_size_end
    :param frame_size_step
    :param frame_size_min
    :param frame_size_max
    :param load_type
    :param load_unit
    :param load_list
    :param load_start
    :param load_end
    :param load_step
    :param load_min
    :param load_max
    :param latency_type
    :param start_traffic_delay
    :param enable_learning
    :param learning_mode
    :param learning_frequency
    :param learning_rate
    :param l3_learning_retry_count
    :param l2_learning_repeat_count
    :param enable_jitter_measure
    :param accept_frame_loss
    :param search_mode
    :param rate_lower_limit
    :param rate_upper_limit
    :param initial_rate
    :param rate_step
    :param back_off
    :param resolution
    :param rfc5180_enable
    :param ipv6_percentage_iteration_mode
    :param fixed_ipv6_percentage
    :param ipv6_percentage_list
    :param random_ipv6_percentage_min
    :param random_ipv6_percentage_max
    :param ipv6_percentage_start
    :param ipv6_percentage_step
    :param ipv6_percentage_end

    Spirent Returns:
    {
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        'handles': '<j_hltapi_ixia.j_test_rfc2544_config.<locals>.RFC object at 0x05021E70>',
        'ethernet_handle': '::ixNet::OBJ-/topology:2/deviceGroup:1/ethernet:1',
        'ipv4_handle': '::ixNet::OBJ-/topology:2/deviceGroup:1/ethernet:1/ipv4:2',
        'traffic_item': '::ixNet::OBJ-/traffic/trafficItem:1',
        'status': '1'
    }

    Common Return Keys:
        "status"
        "handles"
    """

    __check_and_raise(mode)
    from inspect import getargvalues, currentframe
    frame = currentframe()
    arg_values = getargvalues(frame)[3]
    arg_values.pop('frame')
    arg_values.pop('currentframe')
    arg_values.pop('getargvalues')
    args = dict()
    args = get_arg_value(rt_handle, j_test_rfc2544_config.__doc__, **args)
    args['mac_args'] = dict()
    args['vlan_args'] = dict()
    args['ipv4_args'] = dict()
    args['ipv6_args'] = dict()
    args['test_config'] = dict()
    args['learn_frames'] = dict()

    test_config = {
        'iteration_count' : 'numtrials',
        'test_duration_mode' : '',
        'test_duration' : 'duration',
        'frame_size_mode' : 'frameSizeMode',
        'frame_size' : 'framesize',
        'frame_size_imix' : '',
        'frame_size_start' : 'minIncrementFrameSize',
        'frame_size_end' : 'maxIncrementFrameSize',
        'frame_size_step' : 'stepIncrementFrameSize',
        'frame_size_min' : 'minRandomFrameSize',
        'frame_size_max' : 'maxRandomFrameSize',
        'load_type' : 'loadType',
        'load_unit' : (load_type if load_type == jNone else 'custom') + 'LoadUnit',
        'load_list' : 'loadRateList',
        'load_start' : 'initialStepLoadRate',
        'load_end' : 'maxStepLoadRate',
        'load_step' : 'stepStepLoadRate',
        'load_min' : 'minRandomLoadRate',
        'load_max' : 'maxRandomLoadRate',
        'latency_type' : 'latencyType',
        'start_traffic_delay' : 'txDelay',
        'enable_jitter_measure' : 'calculateJitter',
        'accept_frame_loss' : 'binaryTolerance',
    }
    if search_mode == 'step':
        search_mode = 'increment'
    if ipv6_percentage_iteration_mode == 'step':
        ipv6_percentage_iteration_mode = 'increment'
    if search_mode in ['binary', 'combo'] and test_type == 'throughput':
        test_config['resolution'] = 'binaryResolution' if search_mode == 'binary' else 'comboResolution'
        test_config['back_off'] = 'binaryBackoff' if search_mode == 'binary' else 'comboBackoff'
        test_config.update({
            'search_mode' : 'loadType',
            'rate_lower_limit' : 'minBinaryLoadRate',
            'rate_upper_limit' : 'maxBinaryLoadRate',
            'initial_rate' : 'initialBinaryLoadRate',
            'rate_step' : 'stepIncrementLoadRate',
            'back_off' : 'binaryBackoff',
            'resolution' : 'binaryResolution'})
    if rfc5180_enable == 'true':
        test_config['ipv6_percentage_iteration_mode'] = 'ipRatioMode'
        test_config['fixed_ipv6_percentage'] = 'ipv6rate'
        test_config['ipv6_percentage_list'] = 'ipv6RatioList'
        test_config['random_ipv6_percentage_min'] = 'minRandomIpv6Ratio'
        test_config['random_ipv6_percentage_max'] = 'maxRandomIpv6Ratio'
        test_config['ipv6_percentage_start'] = 'minIncrementIpv6Ratio'
        test_config['ipv6_percentage_step'] = 'stepIncrementIpv6Ratio'
        test_config['ipv6_percentage_end'] = 'maxIncrementIpv6Ratio'

    learn_frames = {
        'enable_learning' : 'learnFrequency',
        'learning_mode' : 'learnSendMacOnly',
        'learning_frequency' : 'learnFrequency',
        'learning_rate' : 'learnRate',
        'l3_learning_retry_count' : 'learnNumFrames',
        'l2_learning_repeat_count' : 'learnNumFrames',
    }
    arg_value_map = {
        'load_unit' : {
            'bits_per_second' : 'bpsRate',
            'frames_per_second' : 'fpsRate',
            'inter_burst_gap' : '',
            'kilobits_per_second' : 'kbpsRate',
            'megabits_per_second' : 'mbpsRate',
            'percent_line_rate' : 'percentMaxRate',
            'default' : 'fpsRate'
        },
        'test_type' : {
            'b2b' : "rfc2544back2back",
            'fl' : "rfc2544frameLoss",
            'latency' : "rfc2544throughput",
            'throughput' : "rfc2544throughput"
        },
        'enable_learning' : {1 : 'oncePerTest', '1' : 'oncePerTest', 0 : 'never', '0' : 'never'},
        'learning_mode' : {'l2' : 'true', 'l3' : 'false'},
        'learning_frequency' : {
            'learn_once' : 'oncePerTest',
            'learn_every_trial' : 'onTrial',
            'learn_every_frame_size' : 'oncePerFramesize',
            'learn_every_iteration' : 'onBinaryIteration',
        },
        'latency_type' : {
            'LILO' : 'forwardingDelay',
            'LIFO' : 'storeForward',
            'FIFO' : 'cutThrough'
        },
        'enable_jitter_measure' : {1 : 'true', '1' : 'true', 0 : 'false', '0' : 'false'},
    }
    for arg in arg_values:
        if arg_values.get(arg) == jNone:
            continue
        value = arg_values.get(arg)
        if arg in arg_value_map.keys():
            arg_values[arg] = arg_value_map[arg][value]
        if value is None:
            msg = 'value {} is not supported and setting to default {}'.format(arg_values.get(arg), arg_value_map[arg]['default'])
            rt_handle.log('INFO', msg)
        if arg in learn_frames.keys():
            args['learn_frames'][arg] = [arg_values[arg], '-'+learn_frames.get(arg)]
        elif arg in test_config.keys():
            args['test_config'][arg] = [arg_values[arg], '-'+test_config.get(arg)]
        elif 'mac_' in arg:
            args['mac_args'][arg] = arg_values[arg]
        elif 'vlan' in arg:
            args['vlan_args'][arg] = arg_values[arg]
        elif 'ipv4_' in arg:
            args['ipv4_args'][arg] = arg_values[arg]
        elif 'ipv6_' in arg:
            args['ipv6_args'][arg] = arg_values[arg]
        else:
            args[arg] = arg_values[arg]

    def get_parent(handle, parent, skip_patt=0):
        """ get parent """
        return __get_parent_handle(handle, parent, skip_patt)

    class RFC(object):
        """ RFC 2544 class """
        def __init__(self, rt_handle, args):
            """ constructor """
            self.rfc_handle = None
            self.tgen = rt_handle
            self.mac_args = args.pop('mac_args')
            self.vlan_args = args.pop('vlan_args')
            self.ipv4_args = args.pop('ipv4_args')
            self.ipv6_args = args.pop('ipv6_args')
            self.test_config = args.pop('test_config')
            self.learn_frames = args.pop('learn_frames')
            self.args = args
            self.__initialize__(args)

        def __initialize__(self, args):
            """ initialization """
            self.test_type = args['test_type']
            self.base = '/quickTest'
            self.vports = list()
            self.wizard = self.__select_l23_protocol__()
            self.__create_rfc_2544__(self.test_type)
            if args.get('src_port') is not None and args.get('dst_port') is not None:
                self.ports = self.__create_ports__(args.get('src_port'), args.get('dst_port'))
            self.__configure_wizard__()
            self.configure_traffic_end_points()
            self.configure_test_config('testConfig', self.test_config)
            self.configure_test_config('learnFrames', self.learn_frames)
            invoke_ixnet(rt_handle, 'execute', 'applyITWizardConfiguration', self.rfc_handle)

        def __create_rfc_2544__(self, test_type):
            """ RFC 2544 Creation """
            self.rfc_handle = invoke_ixnet(self.tgen, 'add', self.base, test_type)
            invoke_ixnet(self.tgen, 'setMultiAttribute', self.rfc_handle, '-mode', 'newMode', '-forceApplyQTConfig', 'true')
            ngpf_protocol = {
                'ethernet' : ['-protocolType', 'ngpf', '-ethernet', 'true', '-ipv4', 'false', '-ipv6', 'false'],
                'ipv4' : ['-protocolType', 'ngpf', '-ethernet', 'false', '-ipv4', 'true', '-ipv6', 'false'],
                'ipv6' : ['-protocolType', 'ngpf', '-ethernet', 'false', '-ipv4', 'false', '-ipv6', 'true'],
                'ipmix' : ['-protocolType', 'ngpf', '-ethernet', 'false', '-ipv4', 'true', '-ipv6', 'true']
            }
            protocol_setting = self.rfc_handle + '/protocolSettings'
            invoke_ixnet(self.tgen, 'setMultiAttribute', protocol_setting, *ngpf_protocol[self.wizard.rstrip('Wizard').strip()])
            invoke_ixnet(self.tgen, 'commit')
            self.rfc_handle = invoke_ixnet(self.tgen, r'remapIds', self.rfc_handle)
            self.rfc_handle = self.rfc_handle[0]

        def __select_l23_protocol__(self):
            """ define the protocol wizard """
            if len(self.ipv4_args.keys()) == 0 and len(self.ipv6_args.keys()) == 0:
                return r'ethernetWizard'
            elif len(self.ipv4_args.keys()) > 0 and len(self.ipv6_args.keys()) > 0:
                return r'ipmixWizard'
            elif len(self.ipv4_args.keys()) > 0:
                return r'ipv4Wizard'
            elif len(self.ipv6_args.keys()) > 0:
                return r'ipv6Wizard'
            else:
                return r'ethernetWizard'

        def __create_ports__(self, src_port, dst_port):
            """ create ports """
            if not re.match(r'\d+/\d+/\d+', src_port) and re.match(r'\d+/\d+/\d+', dst_port):
                raise Exception(r'invalid src_port or dst_port handle expecting \d+\d+\d+ but got {} {}'.format(src_port, dst_port))

            vport = get_vport_handle(self.tgen, src_port)
            self.vports.append(vport)
            name = invoke_ixnet(self.tgen, 'getAttribute', vport, '-name')
            port = invoke_ixnet(self.tgen, 'add', self.rfc_handle, 'ports')
            attributes = ['-id', vport, '-inTest', 'true', '-name', name]
            invoke_ixnet(self.tgen, 'setMultiAttribute', port, *attributes)

            vport = get_vport_handle(self.tgen, dst_port)
            self.vports.append(vport)
            port = invoke_ixnet(self.tgen, 'add', self.rfc_handle, 'ports')
            name = invoke_ixnet(self.tgen, 'getAttribute', vport, '-name')
            attributes = ['-id', vport, '-inTest', 'true', '-name', name]
            invoke_ixnet(self.tgen, 'setMultiAttribute', port, *attributes)
            invoke_ixnet(self.tgen, 'commit')
            ret = invoke_ixnet(self.tgen, 'getList', self.rfc_handle, 'ports')
            return ret

        def configure_multivalue(self, wizard, stack, address, device_step, port_step):
            """ configure multivalue """
            if stack == 'mac':
                default_value = '00:00:00:00:00:00'
            elif stack in ['vlanId', 'prefix', 'priority']:
                default_value = 0
            elif stack in ['addresses', 'gateways']:
                if re.match(r'\d+\.\d+\.\d+\.\d+', stack):
                    default_value = '0.0.0.0'
                else:
                    default_value = '0:0:0:0:0:0:0:0'
            handle = invoke_ixnet(self.tgen, 'add', wizard, stack)
            invoke_ixnet(self.tgen, 'commit')
            handle = invoke_ixnet(self.tgen, 'remapIds', handle)
            handle = handle[0]
            pattern = invoke_ixnet(self.tgen, 'add', handle, 'pattern')
            invoke_ixnet(self.tgen, 'commit')
            pattern = invoke_ixnet(self.tgen, 'remapIds', pattern)
            pattern = pattern[0]
            nest_count = invoke_ixnet(self.tgen, 'add', pattern, 'nestedCounter')
            m_list = ['mvIncr', [address, device_step, 1]]
            invoke_ixnet(self.tgen, 'setMultiAttribute',
                         nest_count, '-mvCounterSequence',
                         m_list, '-useTailSequence', 'false')
            invoke_ixnet(self.tgen, 'commit')
            nest_count = invoke_ixnet(self.tgen, 'remapIds', nest_count)
            nest_count = nest_count[0]
            nest_elem = invoke_ixnet(self.tgen, 'add', nest_count, 'nestElements')
            m_list = ['mvIncr', [default_value, port_step, 2]]
            invoke_ixnet(self.tgen, 'setMultiAttribute',
                         nest_elem, '-mvCounterSequence',
                         m_list, '-owner', 'Topology',
                         '-preferredUserInputType', '-1')
            invoke_ixnet(self.tgen, 'commit')

        def modify_multivalue(self, wizard, stack,
                              address=None, device_step=None, port_step=None):
            """ modify multivalue """
            handle = invoke_ixnet(self.tgen, 'getList', wizard, stack)
            handle = handle[0]
            pattern = invoke_ixnet(self.tgen, 'getList', handle, 'pattern')
            pattern = pattern[0]
            nest_count = invoke_ixnet(self.tgen, 'getList', pattern, 'nestedCounter')
            nest_count = nest_count[0]
            m_list = invoke_ixnet(self.tgen, 'getAttribute',
                                  nest_count, '-mvCounterSequence')
            counter_list = list()
            if address is not None:
                m_list[1][0] = address
                counter_list.append('-start')
                counter_list.append(address)
            if device_step is not None:
                m_list[1][1] = device_step
                counter_list.append('-step')
                counter_list.append(device_step)
            invoke_ixnet(self.tgen, 'setAttribute',
                         nest_count, '-mvCounterSequence', m_list)
            invoke_ixnet(self.tgen, 'commit')
            nest_elem = invoke_ixnet(self.tgen, 'getList', nest_count, 'nestElements')
            nest_elem = nest_elem[0]
            m_list = invoke_ixnet(self.tgen, 'getAttribute',
                                  nest_elem, '-mvCounterSequence')
            nest_list = list()
            if port_step is not None:
                m_list[1][1] = port_step
                nest_list = ['-step', port_step]
            invoke_ixnet(self.tgen, 'setMultiAttribute',
                         nest_elem, '-mvCounterSequence', m_list)
            invoke_ixnet(self.tgen, 'commit')
            if stack in ['vlanId', 'priority']:
                eth_handle = get_parent(wizard, 'ethernetPage1', 1)
                eth_handle = self.get_ref_handle(eth_handle)
                stack_handle = invoke_ixnet(self.tgen, 'getList', eth_handle, 'vlan')
                stack_handle = stack_handle[0]
            else:
                stack_handle = self.get_ref_handle(wizard)
            mv_dict = {'counter' : counter_list, 'nest' : nest_list}
            stack = stack[:7]+'Ip' if 'gateway' in stack else stack[:7]
            mv_list = self.set_get_attr_list(stack_handle, '-'+stack, **mv_dict)
            mv_list = ['mvList', mv_list]
            invoke_ixnet(self.tgen, 'setAttribute', handle, '-mvSequence', mv_list)
            invoke_ixnet(self.tgen, 'commit')

        def configure_mac(self, args):
            """ configure mac page """
            handle = self.rfc_handle+'/'+self.wizard+'/ethernetPage1'
            mac_addr = args.get('mac_addr')
            if self.args.get('mode') == 'create' and mac_addr is None:
                mac_addr = '00:11:01:00:00:01'
            port_mac_step = args.get('port_mac_step')
            if self.args.get('mode') == 'create' and port_mac_step is None:
                port_mac_step = '00:00:01:00:00:00'
            device_mac_step = args.get('device_mac_step')
            if self.args.get('mode') == 'create' and device_mac_step is None:
                device_mac_step = '00:00:01:00:00:00'
            if self.args.get('mode') == 'create':
                self.configure_multivalue(handle, 'mac', mac_addr, device_mac_step, port_mac_step)
            else:
                self.modify_multivalue(handle, 'mac', mac_addr, device_mac_step, port_mac_step)

        def configure_vlan(self, args):
            """ configure vlan page """
            handle = self.rfc_handle+'/'+self.wizard+'/ethernetPage1'
            vlan_handle = invoke_ixnet(self.tgen, 'getList', handle, 'vlanList')
            if len(vlan_handle) == 0:
                vlan_handle = invoke_ixnet(self.tgen, 'add', handle, 'vlanList')
                invoke_ixnet(self.tgen, 'commit')
                vlan_handle = invoke_ixnet(self.tgen, 'remapIds', vlan_handle)
            vlan_handle = vlan_handle[0]
            vlan_id = args.get('vlan')
            if self.args.get('mode') == 'create' and vlan_id is None:
                vlan_id = 1
            device_step = args.get('device_vlan_step')
            if self.args.get('mode') == 'create' and device_step is None:
                device_step = 1
            port_step = args.get('port_vlan_step')
            if self.args.get('mode') == 'create' and port_step is None:
                port_step = 1
            vlan_priority = args.get('vlan_priority')
            if self.args.get('mode') == 'create' and vlan_priority is None:
                vlan_priority = 1
            if self.args.get('mode') == 'create':
                self.configure_multivalue(vlan_handle, 'vlanId',
                                          vlan_id, device_step, port_step)
                self.configure_multivalue(vlan_handle, 'priority', vlan_priority, 0, 0)
            elif self.args.get('mode') == 'modify':
                self.modify_multivalue(vlan_handle, 'vlanId', vlan_id, device_step, port_step)
                self.modify_multivalue(vlan_handle, 'priority', vlan_priority, 0, 0)
            enable_vlan = invoke_ixnet(self.tgen, 'getList', handle, 'enableVlans')
            if len(args.keys()) > 0 and len(enable_vlan) == 0:
                enable_vlan = invoke_ixnet(self.tgen, 'add', handle, 'enableVlans')
                invoke_ixnet(self.tgen, 'setMultiAttribute',
                             enable_vlan, '-mvSequence', ['mvSingle', ['true']])
                invoke_ixnet(self.tgen, 'commit')

        def configure_ipv4(self, args):
            """ configure ipv4 page """
            handle = self.rfc_handle+'/'+self.wizard+'/ipv4Page1'

            ipv4_addr = args.get('ipv4_addr')
            if self.args.get('mode') == 'create' and ipv4_addr is None:
                ipv4_addr = '100.1.0.2'

            port_addr_step = args.get('port_ipv4_addr_step')
            if self.args.get('mode') == 'create' and port_addr_step is None:
                port_addr_step = '1.0.0.0'

            device_addr_step = args.get('device_ipv4_addr_step')
            if self.args.get('mode') == 'create' and device_addr_step is None:
                device_addr_step = '0.0.1.0'

            if self.args.get('mode') == 'create':
                self.configure_multivalue(handle, 'addresses', ipv4_addr, device_addr_step, port_addr_step)
            elif self.args.get('mode') == 'modify':
                self.modify_multivalue(handle, 'addresses', ipv4_addr, device_addr_step, port_addr_step)

            ipv4_prefix_len = args.get('ipv4_prefix_len')
            if self.args.get('mode') == 'create' and ipv4_prefix_len is not None:
                self.configure_multivalue(handle, 'prefix', ipv4_prefix_len, 0, 0)
            elif self.args.get('mode') == 'modify':
                self.modify_multivalue(handle, 'prefix', ipv4_prefix_len, None, 0)

            port_gateway_step = args.get('port_ipv4_gateway_step')
            if self.args.get('mode') == 'create' and port_gateway_step is None:
                port_gateway_step = '0.0.0.0'

            ipv4_gateway = args.get('ipv4_gateway')
            if self.args.get('mode') == 'create' and args.get('ipv4_gateway') is not None:
                self.configure_multivalue(handle, 'gateways', ipv4_gateway, '0.0.0.0', port_gateway_step)
            elif self.args.get('mode') == 'modify':
                self.modify_multivalue(handle, 'gateways', ipv4_gateway, None, port_gateway_step)

        def configure_ipv6(self, args):
            """ configure ipv6 page """
            handle = self.rfc_handle+'/'+self.wizard+'/ipv6Page1'
            ipv6_addr = args.get('ipv6_addr')
            if self.args.get('mode') == 'create' and ipv6_addr is None:
                ipv6_addr = '2000:0:0:1:0:0:0:2'

            port_addr_step = args.get('port_ipv6_addr_step')
            if self.args.get('mode') == 'create' and port_addr_step is None:
                port_addr_step = '1:0:0:0:0:0:0:0'

            device_addr_step = args.get('device_ipv6_addr_step')
            if self.args.get('mode') == 'create' and device_addr_step is None:
                device_addr_step = '0:0:0:1:0:0:0:0'

            if self.args.get('mode') == 'create':
                self.configure_multivalue(handle, 'addresses', ipv6_addr, device_addr_step, port_addr_step)
            else:
                self.modify_multivalue(handle, 'addresses', ipv6_addr, device_addr_step, port_addr_step)

            ipv6_prefix_len = args.get('ipv6_prefix_len')
            if self.args.get('mode') == 'create' and ipv6_prefix_len is not None:
                self.configure_multivalue(handle, 'prefix', ipv6_prefix_len, 0, 0)
            elif self.args.get('mode') == 'modify':
                self.modify_multivalue(handle, 'prefix', ipv6_prefix_len)

            port_gateway_step = args.get('port_ipv6_gateway_step')
            if self.args.get('mode') == 'create' and port_gateway_step is None:
                port_gateway_step = '0:0:0:0:0:0:0:0'

            ipv6_gateway = args.get('ipv6_gateway')
            if self.args.get('mode') == 'create' and args.get('ipv6_gateway') is not None:
                self.configure_multivalue(handle, 'gateways', ipv6_gateway, '0:0:0:0:0:0:0:0', port_gateway_step)
            elif self.args.get('mode') == 'modify':
                self.modify_multivalue(handle, 'gateways', ipv6_gateway, None, port_gateway_step)

        def configure_topology(self, args):
            """ configure topology page """
            handle = self.rfc_handle+'/'+self.wizard+'/topologyPage'
            if args.get('device_count') is not None:
                invoke_ixnet(self.tgen, 'setAttribute', handle, '-overallMultiplier', args.get('device_count'))
                invoke_ixnet(self.tgen, 'commit')

        def configure_traffic_end_points(self):
            """ configure traffic end points """
            handle = self.rfc_handle+"/trafficMapping"
            if self.args.get('mode') == 'create':
                invoke_ixnet(self.tgen, 'setAttribute', handle, '-usesLightMaps', 'true')
                traffic_map = invoke_ixnet(self.tgen, 'add', handle, 'lightMap')
                invoke_ixnet(self.tgen, 'commit')
                traffic_map = invoke_ixnet(self.tgen, 'remapIds', traffic_map)
                traffic_map = traffic_map[0]
                source = invoke_ixnet(self.tgen, 'getList', traffic_map, 'source')
                source = traffic_map + '/source:1'
                invoke_ixnet(self.tgen, 'setAttribute', source, '-portId', self.vports[0])
                invoke_ixnet(self.tgen, 'commit')
                destination = invoke_ixnet(self.tgen, 'getList', traffic_map, 'destination')
                destination = traffic_map + '/destination:1'
                invoke_ixnet(self.tgen, 'setAttribute', destination, '-portId', self.vports[1])
                invoke_ixnet(self.tgen, 'commit')
            args_list = list()
            if self.args.get('endpoint_map'):
                mesh = {'one_to_one' : 'oneToOne', 'one_to_many' : 'oneToMany'}
                args_list.append('-mesh')
                args_list.append(mesh[self.args.get('endpoint_map')])
            if self.args.get('bidirectional'):
                args_list.append('-bidirectional')
                args_list.append(self.args.get('bidirectional'))
            if len(args_list) > 0:
                invoke_ixnet(self.tgen, 'setMultiAttribute', handle, *args_list)
                invoke_ixnet(self.tgen, 'commit')

        def __configure_wizard__(self):
            """ configure wizard """
            if self.wizard == 'ethernetWizard':
                self.configure_mac(self.mac_args)
                self.configure_vlan(self.vlan_args)
            elif self.wizard == 'ipv4Wizard':
                self.configure_mac(self.mac_args)
                self.configure_vlan(self.vlan_args)
                self.configure_ipv4(self.ipv4_args)
            elif self.wizard == 'ipv6Wizard':
                self.configure_mac(self.mac_args)
                self.configure_vlan(self.vlan_args)
                self.configure_ipv6(self.ipv6_args)
            elif self.wizard == 'ipmixWizard':
                self.configure_mac(self.mac_args)
                self.configure_vlan(self.vlan_args)
                self.configure_ipv4(self.ipv4_args)
                self.configure_ipv6(self.ipv6_args)
            self.configure_test_config('testConfig', self.test_config)
            self.configure_test_config('learnFrames', self.learn_frames)
            self.configure_topology(self.args)

        def get_ref_handle(self, stack_handle):
            """ configure ref """
            ref = invoke_ixnet(self.tgen, 'getList', stack_handle, 'commitInfo')
            ref = invoke_ixnet(self.tgen, 'getAttribute', ref[0], '-ref')
            return ref

        def set_get_attr_list(self, handle, attribute, **args):
            """ configure attributes """
            attr = invoke_ixnet(self.tgen, 'getAttribute', handle, attribute)
            counter = args['counter']
            nest = args['nest']
            if '/multivalue:' in attr:
                if len(counter) > 0:
                    invoke_ixnet(self.tgen, 'setMultiAttribute', attr + r'/counter', *counter)
                nes = invoke_ixnet(self.tgen, 'getList', attr, 'nest')
                if len(nest) > 0 and len(nes) > 0:
                    invoke_ixnet(self.tgen, 'setMultiAttribute', nes[0], *nest)
                invoke_ixnet(self.tgen, 'commit')
                return invoke_ixnet(self.tgen, 'getAttribute', attr, '-values')
            else:
                return attr

        def configure_test_config(self, child, args):
            """ configure test """
            handle = self.rfc_handle + '/' + child
            attr_list = list()
            if len(args.keys()) > 0:
                for attr in args:
                    if attr[1] is None:
                        continue
                    attr_list.append(args[attr][1])
                    attr_list.append(args[attr][0])
                invoke_ixnet(self.tgen, 'setMultiAttribute', handle, *attr_list)
                invoke_ixnet(self.tgen, 'commit')

        def modify_wizard(self, **args):
            """ modify wizard """
            self.mac_args = args.pop('mac_args')
            self.vlan_args = args.pop('vlan_args')
            self.ipv4_args = args.pop('ipv4_args')
            self.ipv6_args = args.pop('ipv6_args')
            self.test_config = args.pop('test_config')
            self.learn_frames = args.pop('learn_frames')
            self.args = args
            self.__configure_wizard__()
            invoke_ixnet(self.tgen, 'execute', 'applyITWizardConfiguration', self.rfc_handle)

        def get_rfc_handles(self):
            """ get rfc2544 handles """
            handle = self.rfc_handle + '/' +self.wizard
            eth = invoke_ixnet(self.tgen, 'getAttribute', handle+'/ethernetPage1/commitInfo:1', '-ref')
            ret = dict()
            if eth is not None:
                ret['ethernet_handle'] = eth
                ipv4_handle = invoke_ixnet(self.tgen, 'getList', eth, 'ipv4')
                ret.update({} if len(ipv4_handle) == 0 else {'ipv4_handle' : ipv4_handle[0]})
                ipv6_handle = invoke_ixnet(self.tgen, 'getList', eth, 'ipv6')
                ret.update({} if len(ipv6_handle) == 0 else {'ipv6_handle' : ipv6_handle[0]})
            traffic_item = invoke_ixnet(self.tgen, 'getAttribute', self.rfc_handle+'/trafficSelection', '-id')
            ret.update({} if traffic_item is None else {'traffic_item' : traffic_item})
            return ret

        def delete(self):
            """ delete rfc2544 """
            if self.wizard is not None and self.rfc_handle is not None:
                handle = self.rfc_handle + '/' +self.wizard
                topo = invoke_ixnet(self.tgen, 'getAttribute', handle+'/ethernetPage1/commitInfo:1', '-ref')
                topo = get_parent(topo, 'topology')
                traffic_item = invoke_ixnet(self.tgen, 'getAttribute', self.rfc_handle+'/trafficSelection', '-id')
                invoke_ixnet(self.tgen, 'remove', traffic_item)
                invoke_ixnet(self.tgen, 'commit')
                invoke_ixnet(self.tgen, 'remove', topo)
                invoke_ixnet(self.tgen, 'commit')
                invoke_ixnet(self.tgen, 'remove', self.rfc_handle)
                invoke_ixnet(self.tgen, 'commit')
            elif self.rfc_handle is not None:
                invoke_ixnet(self.tgen, 'remove', self.rfc_handle)
                invoke_ixnet(self.tgen, 'commit')

    ret = dict()
    if mode == 'create':
        ret['handles'] = RFC(rt_handle, args)
        ret['status'] = 1
        ret.update(ret['handles'].get_rfc_handles())
    elif mode == 'modify':
        __check_and_raise(handle)
        handle.modify_wizard(**args)
    elif mode == 'delete':
        if handle is not None:
            handle.delete()
            ret['status'] = 0
    return ret


def j_test_rfc2544_control(rt_handle, action=jNone, wait=jNone):
    """
    :param rt_handle:       RT object
    :param action - <run|stop>
    :param wait - <0-1>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        'status': '1'
    }

    Common Return Keys:
        "status"
    """
    __check_and_raise(action)
    args = dict()
    args['action'] = action
    args['wait'] = wait
    args = get_arg_value(rt_handle, j_test_rfc2544_control.__doc__, **args)
    if action == 'run' and wait in [jNone, 0]:
        action = 'start'
    rfc_types = [r'rfc2544back2back', r'rfc2544frameLoss', r'rfc2544throughput']
    ret = []
    for each_type in rfc_types:
        rfc = invoke_ixnet(rt_handle, r'getList', r'/quickTest', each_type)
        if len(rfc) > 0:
            ret.append(invoke_ixnet(rt_handle, r'execute', action, rfc))
    if wait:
        if ret.count('fail') > 0:
            return {'status' : 1}
        else:
            return {'status' : 0}
    else:
        return {'status' : 1}


def j_test_rfc2544_info(rt_handle, test_type=jNone):
    """
    :param rt_handle:       RT object
    :param test_type - <b2b|fl|latency|throughput>

    Spirent Returns:
    {
        'status': '1',
        'rfc2544throughput': {
            'detail': {
            'iteration': {
                '1': {
                'frame_size': {
                    '64': {
                    'oload': '10.0',
                    'out_of_seq_exceed': '0',
                    'throughput_mbps': '2000.0',
                    'frame_loss': '50.0',
                    'max_latency_exceed': '0',
                    'iload': '10.0',
                    'throughput_fps': '1488095.24',
                    'throughput_percent': '0.0'
                    }
                }
                }
            }
            },
            'summary': {
            'total_iteration_count': '1',
            'frame_size': {
                '64': {
                'throughput_mbps': '2000.0',
                'iload': '10.0',
                'throughput_fps': '1488095.24',
                'throughput_percent': '0.0',
                'oload': '10.0'
                }
            }
            }
        }
    }

    IXIA Returns:
    {'rfc2544throughput': {
        detail': {
            'iteration': {
                '1': {
                    'frame_size': {
                        '100': {
                            'max_latency': '501362.46',
                            'throughput_mbps': '1.289',
                            'throughput_fps': '1610.724',
                            'frame_loss': '99.279',
                            'tx_frames': '1070296',
                            'throughput_percent': '0.155',
                            'rx_frames': '7719',
                            'frame_lost': '1062577',
                            'min_latency': '41795.36'
                        },
                        '74': {
                            'max_latency': '1064089.22',
                            'throughput_mbps': '0.916',
                            'throughput_fps': '1547.150',
                            'frame_loss': '99.292',
                            'tx_frames': '1085948',
                            'throughput_percent': '0.116',
                            'rx_frames': '7692',
                            'frame_lost': '1078256',
                            'min_latency': '42494.24'
                        }
                    }
                }
            }
        }
        }
    'status': '1',
    }

    Common Return Keys:
    {'rfc2544throughput': {
        detail': {
            'iteration': {
                '1': {
                    'frame_size': {
                        '<frame_size>': {
                            'max_latency': '',
                            'avg_latency': '',
                            'throughput_mbps': '',
                            'throughput_fps': '',
                            'frame_loss': '',
                            'tx_frames': '',
                            'throughput_percent': '',
                            'rx_frames': '',
                            'frame_lost': '',
                            'min_latency': ''
                        }
                    }
                }
            }
        }
    }
    status: 1
    }
    """
    __check_and_raise(test_type)
    args = dict()
    args['test_type'] = test_type
    args = get_arg_value(rt_handle, j_test_rfc2544_info.__doc__, **args)
    test_type = test_type.strip()
    rfc_type = {
        'b2b' : "rfc2544back2back",
        'fl' : "rfc2544frameLoss",
        'latency' : "rfc2544throughput",
        'throughput' : "rfc2544throughput"
    }
    def get_rfc_stats(result_path):
        """ get the RFC stats"""
        import csv
        stat = {'rfc2544'+test_type : {'detail' : {'iteration' : dict()}}}
        iter_file = result_path + '/iteration.csv'
        local_file = 'iteration.csv'
        input_handle = invoke_ixnet(rt_handle, 'readFrom', iter_file, '-ixNetRelative')
        output_handle = invoke_ixnet(rt_handle, 'writeTo', local_file, '-overwrite')
        invoke_ixnet(rt_handle, 'execute', 'copyFile', input_handle, output_handle)
        csvfile = open(local_file)
        reader = csv.DictReader(csvfile)
        stat_keys = {'throughput_percent' : 'Rx Throughput (% Line Rate)', 'throughput_fps' : 'Rx Throughput (fps)',
                     'throughput_mbps' : 'Rx Throughput (Mbps)', 'frame_loss' : 'Frame Loss (%)', 'avg_latency' : 'Avg Latency (ns)',
                     'min_latency' : 'Min Latency (ns)', 'max_latency' : 'Max Latency (ns)', 'frame_lost' : 'Frame Loss (frames)',
                     'tx_frames' : 'Tx Count (frames)', 'rx_frames' : 'Rx Count (frames)'
                    }
        for row in reader:
            iter_var = stat['rfc2544'+test_type]['detail']['iteration']
            if iter_var.get(row['Trial']) is None:
                iter_var.update({row['Trial'] : {'frame_size' : dict()}})
            if iter_var[row['Trial']]['frame_size'].get(row['Framesize']) is None:
                iter_var[row['Trial']]['frame_size'].update({row['Framesize'] : dict()})
            for key in stat_keys:
                value = row.get(stat_keys[key])
                if '_latency' in key and value is not None:
                    value = str(int(value)/1000)
                iter_var[row['Trial']]['frame_size'][row['Framesize']].update({key : value})
        return stat
    rfc_handle = invoke_ixnet(rt_handle, 'getList', '/quickTest', rfc_type.get(test_type))
    ret = dict()
    for each_rfc in rfc_handle:
        result_path = invoke_ixnet(rt_handle, 'getAttribute', each_rfc+'/results', '-resultPath')
        result_path = result_path.strip()
        if result_path == '' or result_path is None:
            raise Exception('Could not retrive the stat results')
        else:
            try:
                ret.update(get_rfc_stats(result_path))
                ret.update({'status' : 1})
            except Exception as error_string:
                raise Exception('Could not retrive the stat results\n {}'.format(error_string))
    return ret

def get_circuit_end_point_type(rt_handle, emulation_src_handle, emulation_dst_handle):
    circuit_endpoint_type = ""
    if 'pppox' in emulation_src_handle[0] or 'pppox' in emulation_dst_handle[0]:
        for each_src_hndl in emulation_src_handle:
            src_ncp_type, handle = get_stack_and_handle(rt_handle, each_src_hndl, 1)
        for each_dst_hndl in emulation_dst_handle:
            dst_ncp_type, handle = get_stack_and_handle(rt_handle, each_dst_hndl, 1)
        if src_ncp_type[0] == 'ipv4' and dst_ncp_type[0] == 'ipv4':
            circuit_endpoint_type = 'ipv4'
        elif src_ncp_type[0] == 'ipv6' and dst_ncp_type[0] == 'ipv6':
            circuit_endpoint_type = 'ipv6'
        else:
            circuit_endpoint_type = 'ipv4'
        return circuit_endpoint_type
    elif 'ethernet' in emulation_src_handle[0] or 'ethernet' in emulation_dst_handle[0]:
        circuit_endpoint_type = 'ethernet_vlan'
        return circuit_endpoint_type

def get_stack_and_handle(rt_handle, handle, return_stack=0):
    """ get_stack_and_handle """
    stack, handle = split_stack_and_handle(handle)
    if 'pppox' in handle:
        if 'pppoxServerSessions' in handle:
            handle = __get_parent_handle(handle, 'pppoxserver')
            m_val = invoke_ixnet(rt_handle, 'getAttribute', handle, '-ncpType')
            stack = invoke_ixnet(rt_handle, 'getAttribute', m_val, '-values')
        elif 'pppoxclient' in handle:
            m_val = invoke_ixnet(rt_handle, 'getAttribute', handle, '-ncpType')
            stack = invoke_ixnet(rt_handle, 'getAttribute', m_val, '-values')
    elif stack is None and return_stack == 1:
        hndl = __get_parent_handle(handle, 'networkGroup')
        v4_list = ['bgpIPRouteProperty', 'bgpMVpnReceiverSitesIpv4', 'bgpMVpnSenderSitesIpv4',
                   'bgpL3VpnRouteProperty', 'evpnIPv4PrefixRange', 'ipv4PrefixPools',
                   'ldpFECProperty', 'ospfRouteProperty']
        v6_list = ['bgpMVpnReceiverSitesIpv6', 'bgpMVpnSenderSitesIpv6', 'bgpV6IPRouteProperty',
                   'bgpV6L3VpnRouteProperty', 'evpnIPv6PrefixRange', 'ipv6PrefixPools',
                   'ldpIpv6FECProperty', 'ospfv3RouteProperty']
        for version_4, version_6 in zip(v4_list, v6_list):
            try:
                version_4 = invoke_ixnet(rt_handle, 'getList', hndl, version_4)
                if len(version_4) > 0:
                    stack = '4'
                    break
                version_6 = invoke_ixnet(rt_handle, 'getList', hndl, version_6)
                if len(version_6) > 0:
                    stack = '6'
                    break
            except:
                continue
    if return_stack:
        return [stack, handle]
    else:
        return handle

def split_stack_and_handle(handle):
    """ split_stack_and_handle """
    stack = None
    handle = handle
    if '|:STACK==' in handle:
        stack = re.findall(r'\|:STACK==(\d):\|', handle)[0]
        handle = re.split(r'\|:STACK==\d:\|', handle)[-1]
    return [stack, handle]

def netmask_to_length(mask):
    """ netmask_to_length """
    mask = eval("+".join([str(bin(int(m)).lstrip('0b').count('1')) for m in mask.split('.')]))
    return mask

def vlan_config(rt_handle, args, handle):
    """ vlan configuration """
    vlandict = {'vlan_id' : [args.get('vlan_id'), args.get('vlan_outer_id'), \
                             args.get('vlan_id_outer'), args.get('vlan_id1'), \
                             args.get('vlan_id2')],
                'vlan_user_priority' : [args.get('vlan_user_priority'), args.get('vlan_outer_user_priority'), \
                                        args.get('vlan_user_priority_outer')],
                'vlan_id_mode' : [args.get('vlan_id_mode'), args.get('vlan_outer_id_mode'), \
                                  args.get('vlan_id_outer_mode'), args.get('vlan_id_mode1'), \
                                  args.get('vlan_id_mode2')],
                'vlan_id_step' : [args.get('vlan_id_step'), args.get('vlan_outer_id_step'), args.get('vlan_id_step_outer'), \
                                  args.get('vlan_id_outer_step'), args.get('vlan_id_step1'), \
                                  args.get('vlan_id_step2')],
                'vlan_tpid' : [args.get('vlan_ether_type'), args.get('vlan_outer_ether_type')]
               }
    for key, values in vlandict.items():
        while None in values: values.remove(None)
        while jNone in values: values.remove(jNone)

    for key in list(vlandict.keys()):
        if len(vlandict[key]) == 0:
            del vlandict[key]
        elif len(vlandict[key]) == 1:
            vlandict[key] = vlandict[key][0]
    __interface_config_vlan(rt_handle, vlandict, handle)

def verify_and_raise(arg_value, arg_name):
    """ verify_and_raise """
    if arg_value == jNone or arg_value is None:
        raise Exception("Error:  Please check the existence of variable {} and the value passed is valid".format(arg_name))



def configure_icmpv6_options(rt_handle, ret_or_stream_id, mode, icmpv6_args, icmp_type):
    """ configure_icmpv6_options """
    # stack_handle = get_header_handle(ret, "icmpv6")
    icmpv6_message_type = {
        "1"     : "destinationUnreachableMessage",
        "2"     : "packetTooBigMessage",
        "3"     : "timeExceededMessage",
        "4"     : "parameterProblemMessage",
        "128"   : "echoRequestMessage",
        "129"   : "echoReplyMessage",
        "130"   : "multicastListenerQueryMessageVersion1",
        "131"   : "multicastListenerReportMessageVersion1",
        "132"   : "multicastListenerDoneMessage",
        "133"   : "ndpRouterSolicitationMessage",
        "134"   : "ndpRouterAdvertisementMessage",
        "135"   : "ndpNeighborSolicitationMessage",
        "136"   : "ndpNeighborAdvertisementMessage",
        "137"   : "ndpRedirectMessage",
        "143"   : "multicastListenerReportMessageVersion2",
        "144"   : "mobileDHAADRequestMessage",
        "145"   : "mobileDHAADReplyMessage",
        "146"   : "mobilePrefixSolicitationMessage",
        "147"   : "mobilePrefixAdvertisementMessage",
    }
    if mode == "create":
        config_elem = ret_or_stream_id['traffic_item']
        stack_handle = invoke_ixnet(rt_handle, 'getList', config_elem, 'stack')[-2]
        if "icmpv6" in stack_handle:
            stack_handle = invoke_ixnet(rt_handle, 'getList', config_elem, 'stack')[-2]
        else:
            stack_handle = invoke_ixnet(rt_handle, 'getList', config_elem, 'stack')[-2]
            invoke_ixnet(rt_handle, 'execute', 'appendProtocol', stack_handle, '::ixNet::OBJ-/traffic/protocolTemplate:"icmpv6"')
            invoke_ixnet(rt_handle, 'commit')
            stack_handle = invoke_ixnet(rt_handle, 'getList', config_elem, 'stack')[-2]
    elif mode == "modify":
        if ret_or_stream_id is None:
            return
        stream = find_traffic_handle_by_stream_id(rt_handle, ret_or_stream_id)
        stack_handle = invoke_ixnet(rt_handle, 'getList', stream, 'stack')
        stack_handle = [stk for stk in stack_handle if 'stack:"icmpv6' in stk]
        if len(stack_handle) == 0:
            raise Exception("Could not retrieve the icmpv6 handle from the stack {}".format(stack_handle))
        stack_handle = stack_handle[0]

    link_layer_type = {
        "1": "sourceLinkLayerAddressOption",
        "2": "targetLinkLayerAddressOption",
        "3": "prefixInformationOption",
        "4": "redirectedHeaderOption",
        "5": "maximumTransmissionUnitOption"
    }
    link_layer_type_args = {
        "sourceLinkLayerAddressOption": {
            'optionType': icmpv6_args.get('icmpv6_link_layer_type'),
            'optionLength': icmpv6_args.get('icmpv6_link_layer_length'),
            'linkLayerAddress': icmpv6_args.get('icmpv6_link_layer_value')
            },
        "targetLinkLayerAddressOption": {
            'optionType': icmpv6_args.get('icmpv6_link_layer_type'),
            'length': icmpv6_args.get('icmpv6_link_layer_length'),
            'linkLayerAddress': icmpv6_args.get('icmpv6_link_layer_value')
            },
        "prefixInformationOption": {
            'optionType': icmpv6_args.get('icmpv6_prefix_option_type'),
            'length': icmpv6_args.get('icmpv6_prefix_option_length'),
            'prefixLength': icmpv6_args.get('icmpv6_prefix_option_prefix_len'),
            'flags.onLinkLFlag': icmpv6_args.get('icmpv6_prefix_option_lbit'),
            'flags.autonomousAddressConfigurationAFlag': icmpv6_args.get('icmpv6_prefix_option_abit'),
            'reserved': [icmpv6_args.get('icmpv6_prefix_option_reserved1'), icmpv6_args.get('icmpv6_prefix_option_reserved2')],
            'validLifetime': icmpv6_args.get('icmpv6_prefix_option_valid_lifetime'),
            'preferredLifetime': icmpv6_args.get('icmpv6_prefix_option_preferred_lifetime'),
            'prefix': icmpv6_args.get('icmpv6_prefix_option_prefix')
            },
        "redirectedHeaderOption": {
            'optionType': icmpv6_args.get('icmpv6_redirect_hdr_type'),
            'optionLength': icmpv6_args.get('icmpv6_redirect_hdr_length'),
            'reserved': [icmpv6_args.get('icmpv6_redirect_hdr_reserved1'), icmpv6_args.get('icmpv6_redirect_hdr_reserved2')],
            },
        "maximumTransmissionUnitOption": {
            'optionType': icmpv6_args.get('icmpv6_mtu_option_type'),
            'length': icmpv6_args.get('icmpv6_mtu_option_length'),
            'reserved': icmpv6_args.get('icmpv6_mtu_option_reserved'),
            'maximumTransmissionUnit': icmpv6_args.get('icmpv6_mtu_option_mtu')
            }
    }
    icmpv6_msg_fields = {
        "destinationUnreachableMessage" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "unused" : icmpv6_args.get('icmpv6_unused')
        },
        "packetTooBigMessage" : {
            "code"  : icmpv6_args.get('icmpv6_code'),
            "maximumTransmissionUnit"   :   icmpv6_args.get('icmpv6_mtu_option_mtu')
        },
        "timeExceededMessage" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "unused" : icmpv6_args.get('icmpv6_unused')
        },
        "parameterProblemMessage" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "pointer" : icmpv6_args.get('icmpv6_pointer')
        },
        "echoRequestMessage" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "identifier" : icmpv6_args.get('icmpv6_id'),
            "sequenceNumber" : icmpv6_args.get('icmpv6_seq')
        },
        "echoReplyMessage" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "identifier" : icmpv6_args.get('icmpv6_id'),
            "sequenceNumber" : icmpv6_args.get('icmpv6_seq')
        },
        "multicastListenerQueryMessageVersion1" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "maximumResponseDelaymilliseconds" : icmpv6_args.get('icmpv6_max_resp_delay'),
            "reserved" : icmpv6_args.get('router_adv_reserved'),
            "multicastAddress" : icmpv6_args.get('icmpv6_mcast_addr')
        },
        "multicastListenerQueryMessageVersion2" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "maximumResponseDelaymilliseconds" : icmpv6_args.get('icmpv6_max_resp_delay'),
            "reserved" : icmpv6_args.get('router_adv_reserved'),
            "multicastAddress" : icmpv6_args.get('icmpv6_mcast_addr'),
            "suppressRoutersideProcessingSFlag" :   icmpv6_args.get('icmpv6_suppress_flag'),
            "qrv"   :   icmpv6_args.get('icmpv6_qrv'),
            "qqic"  :   icmpv6_args.get('icmpv6_qqic'),
            "numberOfSources"   : icmpv6_args.get('icmpv6_num_source'),
            "sourceAddress" :   icmpv6_args.get('icmpv6_ip_src_addr')
        },
        "multicastListenerReportMessageVersion1" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "maximumResponseDelaymilliseconds" : icmpv6_args.get('icmpv6_max_resp_delay'),
            "reserved" : icmpv6_args.get('router_adv_reserved'),
            "multicastAddress" : icmpv6_args.get('icmpv6_mcast_addr')
        },
        "multicastListenerDoneMessage" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "maximumResponseDelaymilliseconds" : icmpv6_args.get('icmpv6_max_resp_delay'),
            "reserved" : icmpv6_args.get('router_adv_reserved'),
            "multicastAddress" : icmpv6_args.get('icmpv6_mcast_addr')
        },
        "multicastListenerReportMessageVersion2" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "reserved" : icmpv6_args.get('router_adv_reserved'),
            "numberOfMulticastAddressRecords" : icmpv6_args.get('icmpv6_grp_record_mcast_addr'),
            "recordType" : icmpv6_args.get('icmpv6_grp_record_record_type'),
            "numberOfSources" : icmpv6_args.get('icmpv6_num_source'),
            "auxiliaryDataLength"   :   icmpv6_args.get('icmpv6_grp_record_aux_data_len'),
            "multicastAddress"  :   icmpv6_args.get('icmpv6_mcast_addr'),
            "dataLengthoctets"  :   icmpv6_args.get('icmpv6_data'),
            "auxiliaryData" :   icmpv6_args.get('icmpv6_grp_record_aux_data_len')
        },
        "ndpRouterSolicitationMessage" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "reserved" : icmpv6_args.get('router_adv_reserved'),
            "numberOfMulticastAddressRecords" : icmpv6_args.get('icmpv6_grp_record_mcast_addr'),
            "optionType" : icmpv6_args.get('icmpv6_link_layer_type'),
            "optionLength"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "linkLayerAddress"  :   icmpv6_args.get('icmpv6_link_layer_value'),
            "length"    :   icmpv6_args.get('icmpv6_link_layer_length'),
            "prefixLength"  :   icmpv6_args.get('icmpv6_prefix_option_prefix_len'),
            "onLinkLFlag"   :   icmpv6_args.get('icmpv6_prefix_option_lbit'),
            "autonomousAddressConfigurationAFlag"   :   icmpv6_args.get('icmpv6_prefix_option_abit'),
            "routerAddressRFlag"    :   icmpv6_args.get('icmpv6_rflag'),
            "validLifetime" :   icmpv6_args.get('icmpv6_prefix_option_valid_lifetime'),
            "preferredLifetime" :   icmpv6_args.get('icmpv6_prefix_option_preferred_lifetime'),
            "prefix"    :   icmpv6_args.get('icmpv6_prefix_option_prefix'),
            "dataLengthoctets"  :   icmpv6_args.get('icmpv6_data'),
            "data"  :   icmpv6_args.get('icmpv6_data'),
            "maximumTransmissionUnit": icmpv6_args.get('icmpv6_mtu_option_mtu')
        },
        "ndpRouterAdvertisementMessage" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "currentHopLimit" : icmpv6_args.get('icmpv6_cur_hoplimit'),
            "otherStatefulConfigurationOflag" : icmpv6_args.get('icmpv6_oflag'),
            "reserved" : icmpv6_args.get('router_adv_reserved'),
            "routerLifetime" : icmpv6_args.get('icmpv6_router_lifetime'),
            "reachableTime" : icmpv6_args.get('icmpv6_reachable_time'),
            "retransmissionTimer" : icmpv6_args.get('icmpv6_retrans_time'),
            "optionType" : icmpv6_args.get('icmpv6_link_layer_type'),
            "linkLayerAddress" : icmpv6_args.get('icmpv6_link_layer_value'),
            "length" : icmpv6_args.get('icmpv6_link_layer_length'),
            "prefixLength" : icmpv6_args.get('icmpv6_prefix_option_prefix_len'),
            "onLinkLFlag" : icmpv6_args.get('icmpv6_prefix_option_lbit'),
            "autonomousAddressConfigurationAFlag" : icmpv6_args.get('icmpv6_prefix_option_abit'),
            "routerAddressRFlag" : icmpv6_args.get('icmpv6_rflag'),
            "validLifetime" : icmpv6_args.get('icmpv6_prefix_option_valid_lifetime'),
            "preferredLifetime" : icmpv6_args.get('icmpv6_prefix_option_preferred_lifetime'),
            "prefix" : icmpv6_args.get('icmpv6_prefix_option_prefix'),
            "dataLengthoctets" : icmpv6_args.get('icmpv6_data'),
            "data" : icmpv6_args.get('icmpv6_data')
        },
        "ndpNeighborSolicitationMessage" : {
            "code" : icmpv6_args.get('icmpv6_code'),
            "reserved" : icmpv6_args.get('router_adv_reserved'),
            "targetAddress": icmpv6_args.get('icmpv6_target_address'),
            "optionType"  : icmpv6_args.get('icmpv6_link_layer_type'),
            "optionLength"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "linkLayerAddress"  : icmpv6_args.get('icmpv6_link_layer_value'),
            "length"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "prefixLength"  : icmpv6_args.get('icmpv6_prefix_option_prefix_len'),
            "onLinkLFlag"  : icmpv6_args.get('icmpv6_prefix_option_lbit'),
            "autonomousAddressConfigurationAFlag" : icmpv6_args.get('icmpv6_prefix_option_abit'),
            "routerAddressRFlag"  : icmpv6_args.get('icmpv6_rflag'),
            "validLifetime"  : icmpv6_args.get('icmpv6_prefix_option_valid_lifetime'),
            "preferredLifetime"  : icmpv6_args.get('icmpv6_prefix_option_preferred_lifetime'),
            "prefix"  : icmpv6_args.get('icmpv6_prefix_option_prefix'),
            "dataLengthoctets"  : icmpv6_args.get('icmpv6_data'),
            "data"  : icmpv6_args.get('icmpv6_data'),
            "maximumTransmissionUnit"  : icmpv6_args.get('icmpv6_mtu_option_mtu')
        },
        "ndpNeighborAdvertisementMessage"   :   {
            "code"  : icmpv6_args.get('icmpv6_code'),
            "routerRflag"  : icmpv6_args.get('icmpv6_rflag'),
            "neighborSolicitationSflag"  : icmpv6_args.get('icmpv6_sflag'),
            "overrideExistingCacheEntryOflag"  : icmpv6_args.get('icmpv6_oflag'),
            "reserved"  : icmpv6_args.get('router_adv_reserved'),
            "targetAddress"  : icmpv6_args.get('icmpv6_target_address'),
            "optionType"  : icmpv6_args.get('icmpv6_link_layer_type'),
            "optionLength"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "linkLayerAddress"  : icmpv6_args.get('icmpv6_link_layer_value'),
            "length"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "prefixLength"  : icmpv6_args.get('icmpv6_prefix_option_prefix_len'),
            "onLinkLFlag"  : icmpv6_args.get('icmpv6_prefix_option_lbit'),
            "autonomousAddressConfigurationAFlag"  : icmpv6_args.get('icmpv6_prefix_option_abit'),
            "routerAddressRFlag"  : icmpv6_args.get('icmpv6_rflag'),
            "validLifetime"  : icmpv6_args.get('icmpv6_prefix_option_valid_lifetime'),
            "preferredLifetime"  : icmpv6_args.get('icmpv6_prefix_option_preferred_lifetime'),
            "prefix"  : icmpv6_args.get('icmpv6_prefix_option_prefix'),
            "dataLengthoctets"  : icmpv6_args.get('icmpv6_data'),
            "data"  : icmpv6_args.get('icmpv6_data'),
            "maximumTransmissionUnit"  : icmpv6_args.get('icmpv6_mtu_option_mtu')
        },
        "ndpRedirectMessage"    :   {
            "code"  : icmpv6_args.get('icmpv6_code'),
            "reserved"  : icmpv6_args.get('router_adv_reserved'),
            "targetAddress"  : icmpv6_args.get('icmpv6_target_address'),
            "destinationAddress"  : icmpv6_args.get('icmpv6_ip_dst_addr'),
            "optionType"  : icmpv6_args.get('icmpv6_link_layer_type'),
            "optionLength"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "linkLayerAddress"  : icmpv6_args.get('icmpv6_link_layer_value'),
            "length"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "prefixLength"  : icmpv6_args.get('icmpv6_prefix_option_prefix_len'),
            "onLinkLFlag"  : icmpv6_args.get('icmpv6_prefix_option_lbit'),
            "autonomousAddressConfigurationAFlag"  : icmpv6_args.get('icmpv6_prefix_option_abit'),
            "routerAddressRFlag"  : icmpv6_args.get('icmpv6_rflag'),
            "validLifetime"  : icmpv6_args.get('icmpv6_prefix_option_valid_lifetime'),
            "preferredLifetime"  : icmpv6_args.get('icmpv6_prefix_option_preferred_lifetime'),
            "prefix"  : icmpv6_args.get('icmpv6_prefix_option_prefix'),
            "dataLengthoctets"  : icmpv6_args.get('icmpv6_data'),
            "data"  : icmpv6_args.get('icmpv6_data'),
            "maximumTransmissionUnit"  : icmpv6_args.get('icmpv6_mtu_option_mtu')
        },
        "mobileDHAADRequestMessage" :   {
            "code"  : icmpv6_args.get('icmpv6_code'),
            "identifier"  : icmpv6_args.get('icmpv6_id'),
            "reserved"  : icmpv6_args.get('router_adv_reserved'),
        },
        "mobileDHAADReplyMessage"   :   {
            "code"  : icmpv6_args.get('icmpv6_code'),
            "identifier"  : icmpv6_args.get('icmpv6_id'),
            "reserved"  : icmpv6_args.get('router_adv_reserved')
        },
        "mobilePrefixSolicitationMessage"   :   {
            "code"  : icmpv6_args.get('icmpv6_code'),
            "identifier"  : icmpv6_args.get('icmpv6_id'),
            "reserved"  : icmpv6_args.get('router_adv_reserved'),
            "optionType"  : icmpv6_args.get('icmpv6_link_layer_type'),
            "optionLength"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "linkLayerAddress"  : icmpv6_args.get('icmpv6_link_layer_value'),
            "length"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "prefixLength"  : icmpv6_args.get('icmpv6_prefix_option_prefix_len'),
            "onLinkLFlag"  : icmpv6_args.get('icmpv6_prefix_option_lbit'),
            "autonomousAddressConfigurationAFlag"  : icmpv6_args.get('icmpv6_prefix_option_abit'),
            "routerAddressRFlag"  : icmpv6_args.get('icmpv6_rflag'),
            "validLifetime"  : icmpv6_args.get('icmpv6_prefix_option_valid_lifetime'),
            "preferredLifetime"  : icmpv6_args.get('icmpv6_prefix_option_preferred_lifetime'),
            "prefix"  : icmpv6_args.get('icmpv6_prefix_option_prefix'),
            "dataLengthoctets"  : icmpv6_args.get('icmpv6_data'),
            "data"  : icmpv6_args.get('icmpv6_data'),
            "maximumTransmissionUnit"  : icmpv6_args.get('icmpv6_mtu_option_mtu')
        },
        "mobilePrefixAdvertisementMessage"  :   {
            "code"  : icmpv6_args.get('icmpv6_code'),
            "identifier"  : icmpv6_args.get('icmpv6_id'),
            "mBit"  : icmpv6_args.get('icmpv6_mbit'),
            "oBit"  : icmpv6_args.get('icmpv6_obit'),
            "reserved"  : icmpv6_args.get('router_adv_reserved'),
            "optionType"  : icmpv6_args.get('icmpv6_link_layer_type'),
            "optionLength"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "linkLayerAddress"  : icmpv6_args.get('icmpv6_link_layer_value'),
            "length"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "prefixLength"  : icmpv6_args.get('icmpv6_prefix_option_prefix_len'),
            "onLinkLFlag"  : icmpv6_args.get('icmpv6_prefix_option_lbit'),
            "autonomousAddressConfigurationAFlag"  : icmpv6_args.get('icmpv6_prefix_option_abit'),
            "routerAddressRFlag"  : icmpv6_args.get('icmpv6_rflag'),
            "validLifetime"  : icmpv6_args.get('icmpv6_prefix_option_valid_lifetime'),
            "preferredLifetime"  : icmpv6_args.get('icmpv6_prefix_option_preferred_lifetime'),
            "prefix"  : icmpv6_args.get('icmpv6_prefix_option_prefix'),
            "dataLengthoctets"  : icmpv6_args.get('icmpv6_data'),
            "data"  : icmpv6_args.get('icmpv6_data'),
            "length"  : icmpv6_args.get('icmpv6_link_layer_length'),
            "maximumTransmissionUnit"  : icmpv6_args.get('icmpv6_mtu_option_mtu')
        },
    }

    def set_field_value(stack_handle, field_handle, value):
        """ set_field_value """
        count = 0
        if isinstance(value, list):
            count = 1
        if value is not None:
            args = dict()
            args['mode'] = 'set_field_values'
            args['header_handle'] = stack_handle
            args['field_activeFieldChoice'] = 1
            args['field_optionalEnabled'] = 1
            args['field_valueType'] = 'singleValue'
            if len(field_handle) >= 2 and count != 0:
                for val in value:
                    if val is not None:
                        i = value.index(val)
                        args['field_singleValue'] = val
                        args['field_handle'] = field_handle[i]
                        args['field_singleValue'] = val
                        rt_handle.invoke('traffic_config', **args)
            else:
                args['field_handle'] = field_handle[0]
                args['field_singleValue'] = value
                rt_handle.invoke('traffic_config', **args)
    count = 0
    nargs = dict()
    nargs['mode'] = "get_available_fields"
    nargs['header_handle'] = stack_handle
    hndl = (rt_handle.invoke('traffic_config', **nargs)['handle']).split()
    if mode == "create":
        create_patt = re.compile(r".*{0}.me.+Type-\d+".format(icmpv6_message_type[str(icmp_type)]))
        type_handle = list(filter(create_patt.match, hndl))
        set_field_value(stack_handle, type_handle, str(icmp_type))
    else:
        lst_hndl = invoke_ixnet(rt_handle, 'getList', stack_handle, 'field')
        for num, type in icmpv6_message_type.items():
            create_patt = re.compile(r".*{0}.me.+Type-\d+".format(type))
            type_handle = list(filter(create_patt.match, lst_hndl))
            choice = invoke_ixnet(rt_handle, 'getAttribute', type_handle[0], '-activeFieldChoice')
            if choice == "true":
                break
        icmp_type = num


    pattern1 = re.compile(r".*{0}.*".format(icmpv6_message_type[icmp_type]))
    field_list = list(filter(pattern1.match, hndl))
    if icmpv6_args.get('icmpv6_link_layer_type'):
        layer = link_layer_type[icmpv6_args['icmpv6_link_layer_type']]
        pattern2 = re.compile(r".*{0}.*".format(layer))
        layer_field_list = list(filter(pattern2.match, field_list))
        if len(layer_field_list) > 0:
            for key, value in link_layer_type_args[layer].items():
                args = dict()
                pattern3 = re.compile(r".*{0}\-\d+".format(key))
                field_handle = list(filter(pattern3.match, layer_field_list))
                set_field_value(stack_handle, field_handle, value)
        else:
            raise Exception("Error: {0} doesnot exists for message type {1}".format(layer, icmpv6_message_type[icmp_type]))

    layer1 = icmpv6_message_type[icmp_type]
    pattern2 = re.compile(r".*{0}.*".format(layer1))
    layer_field_list = list(filter(pattern2.match, field_list))
    if len(layer_field_list) > 0:
        for key, value in icmpv6_msg_fields[layer1].items():
            args = dict()
            pattern3 = re.compile(r".*{0}\-\d+".format(key))
            field_handle = list(filter(pattern3.match, layer_field_list))
            set_field_value(stack_handle, field_handle, value)
    else:
        raise Exception("Error: {0} doesnot exists for message type {1}".format(layer1, icmpv6_message_type[icmp_type]))


def get_gateway_mac_addr(
        rt_handle,
        mac_discovery_gw=None,
        ip_src_addr=None,
        mac_src=None,
        mac_discovery_gw_step=None,
        ip_src_step=None,
        mac_src_step=None):
    """ get the gateway mac address """
    step = True
    item_handles = list()
    gateway_mac_addr_list = list()
    handle = jNone
    handle_state(rt_handle, handle)
    _result_ = rt_handle.invoke('protocol_info', mode='handles')
    if len(_result_.keys()) == 1:
        raise Exception('please create interface handles before configuring traffic')
    for hndl in _result_:
        if re.match(r'.+ipv[4|6]:\d+$', hndl):
            item_handles.append(hndl)

    for hndl in item_handles:
        if mac_discovery_gw:
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', mac_discovery_gw):
                check_addr = mac_discovery_gw
            else:
                check_addr = ipaddress.IPv6Address(mac_discovery_gw).exploded
                check_addr = check_addr.split(':')
                new_addr = []
                for x in check_addr:
                    if re.match(r'[a-f0-9]{4}', x) and not re.match(r'[0-9]{4}', x):
                        x = x.lstrip('0')
                    else:
                        x = str(int(x))
                    new_addr.append(x)
                new_addr = ":".join(new_addr)
                check_addr = new_addr
            multivalue_handle = invoke_ixnet(rt_handle, 'getAttribute', hndl, '-gatewayIp')
            if not mac_discovery_gw_step:
                step = False
        if ip_src_addr:
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', ip_src_addr):
                check_addr = ip_src_addr
            else:
                check_addr = ipaddress.IPv6Address(ip_src_addr).exploded
                check_addr = check_addr.split(':')
                new_addr = []
                for x in check_addr:
                    if re.match(r'[a-f0-9]{4}', x) and not re.match(r'[0-9]{4}', x):
                        x = x.lstrip('0')
                    else:
                        x = str(int(x))
                    new_addr.append(x)
                new_addr = ":".join(new_addr)
                check_addr = new_addr
            multivalue_handle = invoke_ixnet(rt_handle, 'getAttribute', hndl, '-address')
            if not ip_src_step:
                step = False
        if mac_src:
            check_addr = mac_src
            ether_hndl = __get_parent_handle(hndl, 'ethernet')
            multivalue_handle = invoke_ixnet(rt_handle, 'getAttribute', ether_hndl, '-mac')
            if not mac_src_step:
                step = False
        address_list = invoke_ixnet(rt_handle, 'getAttribute', multivalue_handle, '-values')
        check_addr = check_addr.strip()
        if check_addr in address_list:
            index = address_list.index(check_addr)
            # Wait for protocols to come up if gw mac not resolved
            for i in range(12):
                gateway_mac_addr_list = invoke_ixnet(rt_handle, 'getAttribute', hndl, '-resolvedGatewayMac')
                if 'Unresolved' in gateway_mac_addr_list[index]:
                    sleep(5)
                else:
                    break
            if not step:
                try:
                    gateway_mac_addr_list = [gateway_mac_addr_list[index]]
                except:
                    raise Exception("Failed to retrieve the resolvedGatewayMac for the provided Address {}".format(check_addr))
            break
    return gateway_mac_addr_list


def get_arg_value(rt_handle, docstring, **arguments):
    """ get arg value """
    called_function = inspect.stack()[1][3]
    key_list = list(arguments.keys())
    for key in key_list:
        if arguments[key] == jNone:
            del arguments[key]

    for arg in arguments:
        get_value = re.match(r".*param\s+"+arg+r"\s+\-\s+<(\S+)>.*", docstring, re.S)
        if get_value is not None:
            string_value = get_value.group(1)
        else:
            continue

        if '-' in string_value:
            range_arg = re.match(r'(\d+)\-(\d+)', string_value, re.S)
            if range_arg is not None:
                minimum = int(range_arg.group(1))
                maximum = int(range_arg.group(2))
                arg_value = int(arguments[arg])
                if arg_value < minimum:
                    arguments[arg] = minimum
                    msg = "Argument {} value of {} is not in valid range. Setting it to minimum value supported : {}".format(arg,\
                          called_function, minimum)
                    rt_handle.log("WARN", msg)
                elif arg_value > maximum:
                    arguments[arg] = maximum
                    msg = "Argument {} value of {} is not in valid range. Setting it to maximum value supported : {}".format(arg, \
                          called_function, maximum)
                    rt_handle.log("WARN", msg)
                continue
        elif ':' in string_value or '|' in string_value:
            if str(arguments[arg]) not in string_value:
                raise RuntimeError('Argument {} value {} is not supported for {}. Supported values are {}'.format(arg, \
                                   arguments[arg], called_function, string_value))
            for value in string_value.split('|'):
                if value == arguments[arg]:
                    arguments[arg] = value
                    break
                elif ':' in value and arguments[arg] in value:
                    (spirent_value, ixia_value) = value.split(':')
                    if rt_handle.os.lower() == 'spirent':
                        arguments[arg] = spirent_value
                    elif rt_handle.os.lower() == 'ixos':
                        arguments[arg] = ixia_value.strip()
            continue
        elif re.match(r'\d+', string_value, re.S):
            if int(arguments[arg]) != int(string_value):
                msg = 'Argument {} value {} is not supported for {} and supported value(s) is/are <{}>'\
                      .format(arg, arguments[arg], called_function, string_value)
                raise RuntimeError(msg)
        elif re.match(r'\w+', string_value, re.S):
            if arguments[arg] != string_value:
                msg = 'Argument {} value {} is not supported for {} and supported value(s) is/are <{}>'\
                      .format(arg, arguments[arg], called_function, string_value)
                raise RuntimeError(msg)
    return arguments


def get_bgp_route_property(rt_handle, bgp_route_handle):
    """   get_bgp_route_property """
    ret_handle = None
    v6_prefix_pool = invoke_ixnet(rt_handle, "getList", bgp_route_handle, "ipv6PrefixPools")
    v4_prefix_pool = invoke_ixnet(rt_handle, "getList", bgp_route_handle, "ipv4PrefixPools")
    if len(v6_prefix_pool) > 0:
        prefix_pools = re.sub('::ixNet::OBJ-', '', v6_prefix_pool[0])
        bgp_route_property = "bgpV6IPRouteProperty"
        bgp_handle = invoke_ixnet(rt_handle, "getList", prefix_pools, bgp_route_property)
        if len(bgp_handle) == 0:
            bgp_handle = invoke_ixnet(rt_handle, "getList", prefix_pools, 'bgpV6L3VpnRouteProperty')
        if len(bgp_handle) == 0:
            raise Exception("Unable to retrieve bgp router property handle for {}". format(bgp_route_handle))
        bgp_route_handle = re.sub('::ixNet::OBJ-', '', bgp_handle[0])
    elif len(v4_prefix_pool) > 0:
        prefix_pools = re.sub('::ixNet::OBJ-', '', v4_prefix_pool[0])
        bgp_route_property = "bgpIPRouteProperty"
        bgp_handle = invoke_ixnet(rt_handle, "getList", prefix_pools, bgp_route_property)
        if len(bgp_handle) == 0:
            bgp_handle = invoke_ixnet(rt_handle, "getList", prefix_pools, 'bgpL3VpnRouteProperty')
        if len(bgp_handle) == 0:
            raise Exception("Unable to retrieve bgp router property handle for {}". format(bgp_route_handle))
        bgp_route_handle = re.sub('::ixNet::OBJ-', '', bgp_handle[0])
    ret_handle = bgp_route_handle
    return ret_handle


def ftp_load_config(server, username, password, filepath):
    """
    This method performs ftp from script server tp APP server
    """
    try:
        session = ftplib.FTP(server, username, password)
    except Exception as err:
        raise Exception('Could establish FTP session\n {}'.format(err))
    try:
        filename = filepath.split("/")[-1]
        file = open(filepath, 'rb')
        session.storbinary('STOR {}'.format(filename), file)
        file.close()
        session.quit()
        return 1
    except Exception as err:
        raise Exception('FTP transfer failed \n {}'.format(err))


def get_list_of_port_handles(rt_handle):
    """ gets the list of port handles configured in the current session """
    vports = get_list_of_vport_handles(rt_handle)
    get_port = lambda vport: invoke_ixnet(rt_handle, "getAttribute", vport, '-assignedTo')
    return ["1/"+"/".join(get_port(vp).split(':')[1:]) for vp in vports]


def get_list_of_vport_handles(rt_handle):
    """ get list of vport handles configured in the current session """
    return invoke_ixnet(rt_handle, 'getList', '/', 'vport')


def get_list_of_bound_streams(rt_handle):
    """ get the list of bound streams """
    tr_items = invoke_ixnet(rt_handle, 'getList', '/traffic', 'trafficItem')
    get_bound = lambda traff_item: invoke_ixnet(rt_handle, "getAttribute", traff_item, '-trafficType')
    return [traff for traff in tr_items if get_bound(traff) != 'raw']


def j_session_info(rt_handle, mode='get_traffic_items'):
    """
    :param rt_handle:       RT object
    :param mode - <get_traffic_items>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        'status': '1'
    }

    Common Return Keys:
        "status"
    """
    args = dict()
    args['mode'] = mode
    ret = dict()
    result = rt_handle.invoke('session_info', **args)
    ret.update({'status' : result.pop('status')})
    ret.update({'traffic_config' : result.pop('traffic_config')})
    ret['traffic_streams'] = list(result.keys())
    return ret

def add_protocol_template(rt_handle, traffic_item, stack_name):
    template = '::ixNet::OBJ-/traffic/protocolTemplate:' + '"' + stack_name + '"'
    header_stack = invoke_ixnet(rt_handle, "getList", traffic_item, "stack")
    invoke_ixnet(rt_handle, "execute", "appendProtocol", header_stack[-2], template)
    invoke_ixnet(rt_handle, "commit")
    ret = invoke_ixnet(rt_handle, "getList", traffic_item, "stack")
    return ret

def configure_traffic_options(rt_handle, traffic_ret, protocol, args):
    args = OrderedDict(args)
    stack_handle = get_header_handle(traffic_ret, protocol)
    nargs = dict()
    nargs['mode'] = "get_available_fields"
    nargs['header_handle'] = stack_handle
    hndl = (rt_handle.invoke('traffic_config', **nargs)['handle']).split()
    options_list = list(set([key.split('.')[0] for key in args.keys()]))
    level = len(options_list)
    set_level = 0
    for key in args.keys():
        lvl = options_list.index(key.split('.')[0])
        pattern1 = re.compile(r".*{0}.*".format(key))
        if set_level:
            nargs['mode'] = "get_available_fields"
            nargs['header_handle'] = stack_handle
            hndl = (rt_handle.invoke('traffic_config', **nargs)['handle']).split()
        field_handle = list(filter(pattern1.match, hndl))
        field_handle = field_handle[lvl-1]
        if not set_level and level != 1:
            set_level = set_options_field_value(rt_handle, stack_handle, field_handle, level=level)
        set_options_field_value(rt_handle, stack_handle, field_handle, args[key])

def set_options_field_value(rt_handle, stack_handle, field_handle, value=None, level=0):
    """ set_field_value """
    args = dict()
    if level > 1:
        for i in range(level):
            args['mode'] = 'add_field_level'
            args['header_handle'] = stack_handle
            args['field_handle'] = field_handle
            rt_handle.invoke('traffic_config', **args)
    if value is not None:
        if isinstance(value, dict):
            args['field_valueType'] = value['step_mode'] if value.get('step_mode') else 'increment'
            args['field_startValue'] = value['start_value'] if value.get('start_value') else 0
            args['field_stepValue'] = value['step'] if value.get('step') else 1
            args['field_countValue'] = value['step_count'] if value.get('step_count') else 1
        else:
            args['field_valueType'] = 'singleValue'
            args['field_singleValue'] = value
        args['mode'] = 'set_field_values'
        args['header_handle'] = stack_handle
        args['field_activeFieldChoice'] = 1
        args['field_optionalEnabled'] = 1
        args['field_handle'] = field_handle
        rt_handle.invoke('traffic_config', **args)
    return 1

def configure_ero(rt_handle, ingress_handle, ero_list_ipv4, ero_list_pfxlen, ero_list_loose):
    """To configure parameters of ero"""
    if ero_list_ipv4 != jNone and ero_list_pfxlen != jNone and ero_list_loose != jNone:
        list_len = []
        for each_list in [ero_list_ipv4, ero_list_pfxlen, ero_list_loose]:
            if not isinstance(each_list, list):
                raise Exception("Error: Please pass the value for arg {} in list format".format(each_list))
            list_len.append(len(each_list))
        if len(list(set(list_len))) > 1:
            raise Exception("Error: Please pass same number of values to each argument")

        for loose_index in range(len(ero_list_loose)):
            ero_list_loose[loose_index] = 'true' if ero_list_loose[loose_index] in [1, '1'] else 'false'

        invoke_ixnet(rt_handle, "setMultiAttribute", ingress_handle, "-numberOfEroSubObjects", list_len[0])
        invoke_ixnet(rt_handle, "commit")
        ero_list = invoke_ixnet(rt_handle, 'getList', ingress_handle, "rsvpEROSubObjectsList")
        for i, value in enumerate(ero_list):
            ero_handle = value
            for (ero_attribute, attr)  in zip([ero_list_ipv4, ero_list_pfxlen, ero_list_loose], ['-ip', '-prefixLength', '-looseFlag']):
                value = ero_attribute[i]
                getAttr = invoke_ixnet(rt_handle, 'getAttribute', ero_handle, attr)
                invoke_ixnet(rt_handle, 'setMultiAttribute', getAttr, '-clearOverlays', false)
                add_handle = invoke_ixnet(rt_handle, 'add', getAttr, "singleValue")
                invoke_ixnet(rt_handle, 'setMultiAttribute', add_handle, "-value", value)
                invoke_ixnet(rt_handle, "commit")
    else:
        raise Exception("Error: Please pass all of the three dependent args {}".format('ero_list_ipv4, ero_list_pfxlen, ero_list_loose'))
    return


def global_protocol_settings(rt_handle, port_handle, attr_name, attr_value):
    """To set the attributes in the Global Protocol Settings"""
    vport = get_vport_handle(rt_handle, port_handle)
    options_object = vport+'/'+'protocolStack'+'/'+'options'
    invoke_ixnet(rt_handle, "setAttribute", options_object, attr_name, attr_value)
    invoke_ixnet(rt_handle, "commit")
    return


def is_rawtraffic(rt_handle, port_handle, port_handle2, emulation_src_handle):
    """Returns true if traffic is type RAW"""
    if emulation_src_handle is not None:
        if re.match(r'^\d+/\d+/\d+$', emulation_src_handle[0]):
            return True
    elif port_handle is not None and port_handle2 is not None:
        return True
    return False


def configure_mac_discovery(rt_handle, l4_protocol, args):
    """TO configure mac_discovery_gw for raw traffic"""

    intf_args = dict()
    map_dict = {'ip_src_addr': 'intf_ip_addr', 'ip_src_step': 'intf_ip_addr_step',
                'ipv6_src_addr': 'ipv6_intf_addr', 'ipv6_src_step': 'ipv6_intf_addr_step',
                'mac_src': 'src_mac_addr', 'mac_src_step': 'src_mac_addr_step'}

    for each_arg in list(map_dict.keys()):
        if args.get(each_arg):
            intf_args[map_dict[each_arg]] = args[each_arg]

    if is_rawtraffic(rt_handle, args.get('port_handle'), args.get('port_handle2'), args.get('emulation_src_handle')):
        gateway_mac_addr = list()
        check_port = args['emulation_src_handle'] if args.get('emulation_src_handle') is not None else args['port_handle']
        if args.get('mode') == 'create' and l4_protocol == '0':
            if args.get('mac_discovery_gw'):
                if handle_state(rt_handle, port_handle=check_port) == "NoTOPO":
                    handle = create_deviceGroup(rt_handle, check_port)
                    handle = handle['device_group_handle']
                    intf_args['mode'] = 'config'
                    intf_args['protocol_handle'] = handle

                    if ipaddress.ip_address(args['mac_discovery_gw']).version in [6, '6']:
                        intf_args['ipv6_gateway'] = args['mac_discovery_gw']
                        if args.get('mac_discovery_gw_step'):
                            intf_args['ipv6_gateway_step'] = args['mac_discovery_gw_step']
                    else:
                        intf_args['gateway'] = args['mac_discovery_gw']
                        if args.get('mac_discovery_gw_step'):
                            intf_args['gateway_step'] = args['mac_discovery_gw_step']

                    if intf_args.get('intf_ip_addr') is None and intf_args.get('ipv6_intf_addr') is None:
                        if ipaddress.ip_address(args['mac_discovery_gw']).version in [4, '4']:
                            intf_args['intf_ip_addr'] = str(ipaddress.IPv4Address(args['mac_discovery_gw']) + 1)
                        else:
                            intf_args['ipv6_intf_addr'] = str(ipaddress.IPv6Address(args['mac_discovery_gw']) + 1)
                    rt_handle.invoke('interface_config', **intf_args)
                mac_discovery_gw = args.pop('mac_discovery_gw')
                mac_discovery_gw_step = args.pop('mac_discovery_gw_step') if args.get('mac_discovery_gw_step') else None
                gateway_mac_addr = get_gateway_mac_addr(rt_handle, mac_discovery_gw=mac_discovery_gw,\
                                                            mac_discovery_gw_step=mac_discovery_gw_step)

            elif args.get('mac_discovery_gw') is None and args.get('mac_dst') is None:
                if handle_state(rt_handle, port_handle=check_port) == "NoTOPO":
                    raise Exception("Error: Topology does not exist on port <{}>".format(check_port))

                if args.get('ip_src_addr') or args.get('ipv6_src_addr'):
                    ip_src_addr = args.get('ip_src_addr') if args.get('ip_src_addr') else args.get('ipv6_src_addr')
                    ip_src_step = args.get('ip_src_step') if args.get('ip_src_step') \
                                    else args.get('ipv6_src_step') if args.get('ipv6_src_step') else None
                    gateway_mac_addr = get_gateway_mac_addr(rt_handle, ip_src_addr=ip_src_addr,\
                                                            ip_src_step=ip_src_step)
                elif args.get('mac_src'):
                    mac_src = args.get('mac_src')
                    mac_src_step = args.get('mac_src_step') if args.get('mac_src_step') else None
                    gateway_mac_addr = get_gateway_mac_addr(rt_handle, mac_src=mac_src, \
                                                            mac_src_step=mac_src_step)

        if gateway_mac_addr:
            args['mac_dst'] = gateway_mac_addr if len(gateway_mac_addr) > 1 else gateway_mac_addr[0]
            if isinstance(args['mac_dst'], list):
                args['mac_dst_mode'] = 'list'
        elif not gateway_mac_addr:
            if args.get('mac_discovery_gw'):
                raise Exception("Failed to get mac destination address.")
            elif (args.get('ip_src_addr') or args.get('ipv6_src_addr') or \
            args.get('mac_src')) and not args.get('mac_dst'):
                raise Exception("Failed to get mac destination address.")

    elif args.get('mac_discovery_gw'):
        args.pop('mac_discovery_gw')

    return args

def configure_pfc(rt_handle, port, traffic_item=None, mode='create'):
    """Configure the pfc parameters"""
    qmapdict = {'priority0': '/field:"pfcPause.header.macControl.pauseQuanta.pfcQueue0-6"',
                'priority1': '/field:"pfcPause.header.macControl.pauseQuanta.pfcQueue1-7"',
                'priority2': '/field:"pfcPause.header.macControl.pauseQuanta.pfcQueue2-8"',
                'priority3': '/field:"pfcPause.header.macControl.pauseQuanta.pfcQueue3-9"',
                'priority4': '/field:"pfcPause.header.macControl.pauseQuanta.pfcQueue4-10"',
                'priority5': '/field:"pfcPause.header.macControl.pauseQuanta.pfcQueue5-11"',
                'priority6': '/field:"pfcPause.header.macControl.pauseQuanta.pfcQueue6-12"',
                'priority7': '/field:"pfcPause.header.macControl.pauseQuanta.pfcQueue7-13"'
               }


    if traffic_item is not None:
        if not isinstance(traffic_item, list):
            traffic_item = [traffic_item]

        if pfc_dict.get(port):
            if not pfc_dict[port].get('traffic_items'):
                pfc_dict[port]['traffic_items'] = list()
            pfc_dict[port]['traffic_items'].extend(traffic_item)

    if traffic_item is None:
        if pfc_dict.get(port):
            if pfc_dict[port].get('traffic_items'):
                traffic_item = pfc_dict[port]['traffic_items']


    Qlist = list(set(pfc_dict[port]['qlist']))
    if len(Qlist) == 1 and Qlist[0] in [0, '0']:
        if traffic_item is not None:
            for traffic in traffic_item:
                stack_handles = invoke_ixnet(rt_handle, "getList", traffic, "stack")
                for stack in stack_handles:
                    if 'pfcPause' in stack:
                        invoke_ixnet(rt_handle, "execute", "remove", stack)
                        invoke_ixnet(rt_handle, "commit")
        return
    pfc_handle = list()
    if mode == 'create':
        for each_item in traffic_item:
            pause_template = '::ixNet::OBJ-/traffic/protocolTemplate:"pfcPause"'
            header_stack = invoke_ixnet(rt_handle, "getList", each_item, "stack")
            invoke_ixnet(rt_handle, "execute", "insertProtocol", header_stack[0], pause_template)
            invoke_ixnet(rt_handle, "commit")
            stack_handles = invoke_ixnet(rt_handle, "getList", each_item, "stack")
            invoke_ixnet(rt_handle, "execute", "remove", stack_handles[1])
            invoke_ixnet(rt_handle, "commit")
            pfc_handle.append(stack_handles[0])
    elif mode == 'modify':
        if pfc_dict.get(port):
            if pfc_dict[port].get('traffic_items'):
                for traffic in pfc_dict[port]['traffic_items']:
                    stack_handles = invoke_ixnet(rt_handle, "getList", traffic, "stack")
                    pfc_handle = [stack for stack in stack_handles if 'pfcPause' in stack]

    if pfc_handle:
        pfcdict = pfc_dict[port]
        for key, value in pfcdict.items():
            if qmapdict.get(key):
                for pause_handle in pfc_handle:
                    invoke_ixnet(rt_handle, 'setAttribute', pause_handle+qmapdict[key], "-fieldValue", value)
                    invoke_ixnet(rt_handle, "commit")
    return

def create_pfc_dict(rt_handle, pfcargs, handle, port_handle):
    """ create_pfc_dict """
    if handle != jNone and isinstance(handle, str):
        handle = list(handle)
        hndl_list = list()
        for hndl in handle:
            hndl_list.append(get_ixia_port_handle(rt_handle, hndl))
    if port_handle != jNone and isinstance(port_handle, str):
        port_handle = list(port_handle)
    if handle != jNone and port_handle != jNone:
        handle = jNone

    port_list = hndl_list if handle != jNone else port_handle
    for port in port_list:
        for key, value in pfcargs.items():
            if not pfc_dict.get(port):
                pfc_dict[port] = dict()
                pfc_dict[port]['qlist'] = ['0', '0', '0', '0', '0', '0', '0', '0']
            if 'priority' in key:
                pfc_dict[port]['qlist'][int(key[-1])] = str(value)
            pfc_dict[port][key] = value
    return


def remove_or_disable_traffic(rt_handle, **kwargs):
    """ remove_or_disable_traffic """
    exec_block = 0
    tr_list = list()
    if kwargs.get('stream_id') != None:
        stream_ids = kwargs.get('stream_id')
        if not isinstance(stream_ids, list):
            stream_ids = list([stream_ids])
        stream_list = list()
        for stream in stream_ids:
            strm_hndl = find_traffic_handle_by_stream_id(rt_handle, stream)
            tr_list.append(__get_parent_handle(strm_hndl, 'trafficItem'))
    if kwargs.get('port_handle') != None and kwargs.get('stream_id') == None:
        port_handle = kwargs.get('port_handle')
        if not isinstance(port_handle, list):
            port_handle = list([port_handle])
        for port in port_handle:
            tr_list.extend(find_traffic_by_port_handle(rt_handle, port))
    if kwargs.get('stream_id') == None and kwargs.get('port_handle') == None:
        raise Exception('port_handle/stream_id is mandatory argument for traffic_config API')

    tr_list = set(tr_list)
    for tr in tr_list:
        if tr == None:
            continue
        if kwargs.get('mode') == 'remove':
            invoke_ixnet(rt_handle, 'remove', tr)
            invoke_ixnet(rt_handle, 'commit')
        elif kwargs.get('mode') == 'disable':
            invoke_ixnet(rt_handle, 'setAttribute', tr, '-enabled', 'false')
            invoke_ixnet(rt_handle, 'commit')
        elif kwargs.get('mode') == 'enable':
            invoke_ixnet(rt_handle, 'setAttribute', tr, '-enabled', 'true')
            invoke_ixnet(rt_handle, 'commit')
        else:
            raise Exception("invalid mode passed {}". format(kwargs.get('mode')))
    ret = {'status': '1'}
    return ret


def find_traffic_by_port_handle(rt_handle, port_handle):
    """ find_traffic_by_port_handle """
    tr_items = invoke_ixnet(rt_handle, "getList", "/traffic", "trafficItem")
    tr_list = list()
    for tr in tr_items:
        endpoints = invoke_ixnet(rt_handle, 'getList', tr, 'endpointSet')
        for ep in endpoints:
            src_list, dst_list = get_traffic_sources_and_destinations(rt_handle, ep)
            if port_handle in src_list or port_handle in dst_list:
                tr_list.append(tr)
    return tr_list


def get_traffic_sources_and_destinations(rt_handle, tr_item_endpoint):
    """ get_traffic_sources_and_destinations """
    sources = invoke_ixnet(rt_handle, "getAttribute", tr_item_endpoint, "-sources")
    destinations = invoke_ixnet(rt_handle, "getAttribute", tr_item_endpoint, "-destinations")
    src_ports = list()
    dst_ports = list()
    for src, dst in zip(sources, destinations):
        src_ports.append(get_ixia_port_handle(rt_handle, src))
        dst_ports.append(get_ixia_port_handle(rt_handle, dst))
    return [src_ports, dst_ports]


def process_field_link_handle(rt_handle, stream_id, field_handle):
    """ process_field_link_handle """
    if stream_id == None:
        raise Exception('stream_id param cannot be None in mode modify')
    if isinstance(field_handle, str):
        field_handle = list(set([field_handle]))
    handle_list = list()
    for field_hndl in field_handle:
        if stream_id in field_hndl:
            tr_hndl = find_traffic_handle_by_stream_id(rt_handle, stream_id)
            stackLink = field_hndl.strip(stream_id)
            handle_list.append(tr_hndl + stackLink)
        elif "trafficItem" in field_hndl:
            handle_list.append(field_hndl)
        else:
            raise Exception("Please pass a valid field handle to set the stackLink, passed {}".format(field_hndl))
    return handle_list


def find_traffic_handle_by_stream_id(rt_handle, stream_id):
    """ find_traffic_handle_by_stream_id """
    traff_items = invoke_ixnet(rt_handle, 'getList', '/traffic', 'trafficItem')
    handle_found = None
    for traff in traff_items:
        if invoke_ixnet(rt_handle, 'getAttribute', traff, '-name') in stream_id:
            handle_found = traff + '/configElement:1'
            break
    if handle_found == None:
        raise Exception("Please check the stream id is valid, Could not retrieve the handle from the stream id {}". format(stream_id))
    return handle_found

def configure_ip_priority(rt_handle, ret, mode, value, qos_type):
    """ To set the unused bit values in ip priority
        ip_ecn values: for dscp: 00,01,10,11
                       for tos: 0,1    """

    if mode == "create":
        config_elem = ret['traffic_item']
        stack_hdl = invoke_ixnet(rt_handle, 'getList', config_elem, 'stack')
        for st_hdl in stack_hdl:
            if "ipv4" in st_hdl.split("/stack")[1]:
                stack_handle = st_hdl
    elif mode == "modify":
        stream = find_traffic_handle_by_stream_id(rt_handle, ret['stream_id'])
        stack_hdl = invoke_ixnet(rt_handle, 'getList', stream, 'stack')
        for st_hdl in stack_hdl:
            if "ipv4" in st_hdl.split("/stack")[1]:
                stack_handle = st_hdl
        if len(stack_handle) == 0:
            stack_handle = stack_handle[0]
    field_hdl = invoke_ixnet(rt_handle, 'getList', stack_handle, 'field')
    for fh in field_hdl:
        if qos_type == 'dscp':
            if "defaultPHB.unused" in fh:
                field_handle = fh.split("/field:")[1]
        elif qos_type == "tos":
            if "tos.unused" in fh:
                field_handle = fh.split("/field:")[1]
    set_ipv4_field_value(rt_handle, stack_handle, field_handle, value)

def set_ipv4_field_value(rt_handle, stack_handle, field_handle, value):
    """ set ipv4 field value ip_ecn/unused bits"""
    count = 0
    if isinstance(value, list):
        count = 1
    if value is not None:
        args = dict()
        args['mode'] = 'set_field_values'
        args['header_handle'] = stack_handle
        args['field_activeFieldChoice'] = 1
        args['field_optionalEnabled'] = 1
        args['field_valueType'] = 'singleValue'
        args['field_handle'] = field_handle
        if len(field_handle) >= 2 and count != 0:
            for val in value:
                if val is not None:
                    i = value.index(val)
                    args['field_singleValue'] = val
                    args['field_handle'] = field_handle[i]
                    args['field_singleValue'] = val
                    rt_handle.invoke('traffic_config', **args)
        else:
            args['field_handle'] = field_handle
            args['field_singleValue'] = value
            rt_handle.invoke('traffic_config', **args)

def set_source_destination_handle(rt_handle, **args):
    emulation_src_handle = proces_emulation_handles(rt_handle, args.get('emulation_src_handle'))
    emulation_dst_handle = proces_emulation_handles(rt_handle, args.get('emulation_dst_handle'))
    circuit_endpoint_type = None
    circuit_endpoint_type_dst = None
    circuit_endpoint_type_src = None
    if emulation_src_handle is not None and emulation_dst_handle is not None:
        circuit_endpoint_type_src = get_circuit_types(rt_handle, args.get('emulation_src_handle'))
        circuit_endpoint_type_dst = get_circuit_types(rt_handle, args.get('emulation_dst_handle'))
        args['emulation_src_handle'] = emulation_src_handle
        args['emulation_dst_handle'] = emulation_dst_handle
        circuit_endpoint_type = get_circuit_end_point_type(rt_handle, emulation_src_handle, emulation_dst_handle)
    if circuit_endpoint_type_src == 'raw' or circuit_endpoint_type_dst == 'raw':
        args['circuit_type'] = 'raw'
    elif circuit_endpoint_type_src is not None:
        args['circuit_endpoint_type'] = circuit_endpoint_type_src
    elif circuit_endpoint_type_dst is not None:
        args['circuit_endpoint_type'] = circuit_endpoint_type_dst
    elif circuit_endpoint_type is not None:
        args['circuit_endpoint_type'] = circuit_endpoint_type
    elif args.get('port_handle') is not None and args.get('port_handle2') is not None:
        args['circuit_type'] = 'raw'
    else:
        args['circuit_endpoint_type'] = 'ipv4'
    return args

def proces_emulation_handles(rt_handle, src_or_dst_handle):
    ret_handle_list = list()
    if src_or_dst_handle is None:
        return None
    if isinstance(src_or_dst_handle, str):
        src_or_dst_handle = list([src_or_dst_handle.strip()])
    if "DhcpConfigObject" in str(src_or_dst_handle.__class__):
        src_or_dst_handle = list([src_or_dst_handle.client_handle])
    for each_src_hndl in src_or_dst_handle:
        if '|:STACK==' in each_src_hndl:
            ret_handle_list.append(get_stack_and_handle(rt_handle, each_src_hndl, 1)[1])
        else:
            ret_handle_list.append(each_src_hndl)
    return ret_handle_list

def get_circuit_types(rt_handle, src_or_dst_handle):
    if src_or_dst_handle is None:
        return None
    ret_type = None
    if isinstance(src_or_dst_handle, str):
        src_or_dst_handle = list([src_or_dst_handle.strip()])
    if "DhcpConfigObject" in str(src_or_dst_handle.__class__):
        src_or_dst_handle = list([src_or_dst_handle.client_handle])
    if re.match(r'^\d+/\d+/\d+$', src_or_dst_handle[0]):
        ret_type = 'raw'
    elif 'ipv4' in src_or_dst_handle[0] or 'dhcpv4' in src_or_dst_handle[0]:
        ret_type = 'ipv4'
    elif 'ipv6' in src_or_dst_handle[0] or 'dhcpv6' in src_or_dst_handle[0]:
        ret_type = 'ipv6'
    src_stack = None
    for each_hndl in src_or_dst_handle:
        if 'networkGroup' in each_hndl:
            src_stack, hndl = get_stack_and_handle(rt_handle, each_hndl, 1)
    if src_stack is not None:
        ret_type = 'ipv'+src_stack
    return ret_type