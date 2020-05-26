# Copyright 2016- Juniper Networks
# Toby BBE development team
"""
The module is used to create RT simulation
"""
import re
import ipaddress
from jnpr.toby.bbe.errors import BBEDeviceError
#from functools import partial

# rt = t.get_handle(resource='rt0')
#
# def add_method(obj, func):
#     """
#     'Bind a function and store it in RT object'
#     :param obj:                 RT object
#     :param func:                method from ixiatester.py or from spirent
#     :return:
#     """
#
#     setattr(obj, func.__name__, partial(func, obj))

# Used to tag log messages from this module
__LOGTAG = '[BBERT]'


# def bbe_add_methods_to_rt():
#     """Add BBE tester functions to RT instance created by Toby
#
#     Note: implement this and call this from bbe_initialize
#
#     :return:
#     """
#     for device in bbe.bbevar['resources']:
#         obj = t.get_handle(resource=device)
#         if hasattr(obj, 'os') and obj.os == 'IxOS':
#             import jnpr.toby.bbe.testers.ixiatester as ixiatester
#             ###attach attributes and methods to the obj
#             name_list = [method for method in dir(ixiatester) if callable(getattr(ixiatester, method))]
#             for name in name_list:
#                 method = getattr(ixiatester, name)
#                 add_method(obj, method)
#
#             obj.initialize(obj.port_list)
#             #print(dir(obj))
#


def bbe_rt_init():
    """Initialize RT using created RT handle.

    Initializes RT subscribers, uplinks, and dhcp servers

    :return: None
    """
    def is_landslide(device_id):
        return 'landslide-manager' in t.resources[device_id]['system']['primary']

    t.log(str([device.device_id for device in bbe.get_devices()]))
    for device in bbe.get_devices():
        if 'rt' in device.device_id:
            if not is_landslide(device.device_id):
                t.log("Is not landslide:")
                t.log(device.device_id)
                tester = t.get_handle(resource=device.device_id)
                tester.invoke('bbe_initialize')
                # create AE links if necessary
                add_rt_ae(device.device_id)

    # All bbe var subscriber instances
    all_subs = bbe.get_subscriber_handles()
    t.log(str(all_subs))
    t.log(str([subs.subscribers_type for subs in all_subs]))
    if all_subs:
        # Creates RT subscribers.
        # RT handles are saved back to bbe var subscriber instances.
        test_id = 1
        for subs in all_subs:
            rt_device = subs.rt_device_id
            if not is_landslide(rt_device):
                create_ancp_node(rt_device, subs)

            if subs.subscribers_type == 'hag':
                create_rt_hag_subscribers(rt_device, subs, test_id)
                test_id += 1
            if subs.subscribers_type == 'cups':
                create_rt_cups_subscribers(rt_device, subs, test_id)
                test_id += 1
            if subs.subscribers_type == 'pgw':
                create_rt_pgw_subscribers(rt_device, subs, test_id)
                test_id += 1
            if subs.subscribers_type == 'fwa':                                                          
                create_fwa_subscribers(rt_device, subs, test_id)
                test_id += 1

            if subs.subscribers_type == 'dhcp':
                create_rt_dhcp_subscribers(rt_device, subs)
            if subs.subscribers_type == 'pppoe':
                create_rt_pppoe_subscribers(rt_device, subs)
            if subs.subscribers_type == 'l2tp':
                create_rt_l2tp_subscribers(rt_device, subs)
            if subs.subscribers_type == 'l2bsa':
                create_rt_l2bsa_subscribers(rt_device, subs)

            if not is_landslide(rt_device):
                add_mcast_client(rt_device, subs)
    else:
        t.log("no subscriber defined in yaml file")

    for device in bbe.get_devices():
        # Set RT subscribers call rates: csr and clr
        if 'rt' in device.device_id:
            if not is_landslide(device.device_id):
                set_subscribers_call_rate(device.device_id)
                # if subs.has_ancp:
                #     set_ancp_rate(device.device_id)
                # Add RT uplinks/Custom links
                add_rt_links(device.device_id)
                #Add RT LNS if there is
                add_rt_lns(device.device_id)
                #Add bgp neighbor
                add_rt_bgp_neighbor(device.device_id)
                add_rt_isis_l3(device.device_id)
                # Create DHCP servers if required
                add_rt_dhcp_servers(device.device_id, 'ipv4')
                add_rt_dhcp_servers(device.device_id, 'ipv6')


def create_rt_dhcp_subscribers(rt_device_id, subscriber):
    """Create RT DHCP subscribers

    TODO: support GRE attributes

    :param rt_device_id: RT device id such as 'rt0'
    :param subscriber: jnpr.toby.bbe.bbevar.subscribers.DHCPSubscribers instance
    :return: None
    May raise BBEDeviceError.
    """
    tester = t.get_handle(rt_device_id)
    # parameters to add_dhcp_client
    params = dict()
    params['port'] = subscriber.rt_port
    params['num_sessions'] = subscriber.count
    if int(subscriber.count) < 1:
        t.log('rt emulation for this dhcp sub {} is not created since the session is 0'.format(subscriber.tag))
        return
    params['ip_type'] = subscriber.family
    if subscriber.dhcpv4_gateway:
        params['dhcpv4_gateway'] = subscriber.dhcpv4_gateway
    if subscriber.rapid_commit:
        params['rapid_commit'] = subscriber.rapid_commit
    if subscriber.dhcpv4_gateway_custom is not None:
        params['dhcpv4_gateway_custom'] = subscriber.dhcpv4_gateway_custom
    if 'v6' in subscriber.family or 'dual' in subscriber.family:
        params['dhcpv6_ia_type'] = subscriber.dhcpv6_ia_type
        if int(subscriber.dhcpv6_iana_count) > 1:
            params['dhcpv6_iana_count'] = subscriber.dhcpv6_iana_count
        if int(subscriber.dhcpv6_iapd_count) > 1:
            params['dhcpv6_iapd_count'] = subscriber.dhcpv6_iapd_count
        if subscriber.dhcpv6_gateway:
            params['dhcpv6_gateway'] = subscriber.dhcpv6_gateway
        if subscriber.dhcpv6_gateway_custom is not None:
            params['dhcpv6_gateway_custom'] = subscriber.dhcpv6_gateway_custom

    if subscriber.vlan_range:
        params['vlan_start'] = subscriber.vlan_range.start
        params['vlan_step'] = subscriber.vlan_range.step
        params['vlan_repeat'] = subscriber.vlan_range.repeat
        params['vlan_length'] = subscriber.vlan_range.length
        if hasattr(subscriber, 'vlan_tpid'):
            params['vlan_tpid'] = subscriber.vlan_tpid
    if subscriber.svlan_range:
        params['svlan_start'] = subscriber.svlan_range.start
        params['svlan_step'] = subscriber.svlan_range.step
        params['svlan_repeat'] = subscriber.svlan_range.repeat
        params['svlan_length'] = subscriber.svlan_range.length
        if hasattr(subscriber, 'svlan_tpid'):
            params['svlan_tpid'] = subscriber.svlan_tpid

    if subscriber.mac:
        params['mac'] = subscriber.mac
        if subscriber.mac_step:
            params['mac_step'] = subscriber.mac_step

    if subscriber.has_option82:
        aci = subscriber.option82_aci
        ari = subscriber.option82_ari
        params['circuit_id'] = aci.id
        params['circuit_id_start'] = aci.start
        params['circuit_id_step'] = aci.step
        params['circuit_id_repeat'] = aci.repeat
        params['circuit_id_length'] = aci.length
        params['remote_id'] = ari.id
        params['remote_id_start'] = ari.start
        params['remote_id_step'] = ari.step
        params['remote_id_repeat'] = ari.repeat
        params['remote_id_length'] = ari.length
        params['tlv_include_in_messages'] = aci.messages

    if subscriber.has_option60:
        params['vendor_class_id'] = subscriber.option60.id
        params['vendor_class_id_start'] = subscriber.option60.start
        params['vendor_class_id_step'] = subscriber.option60.step
        params['vendor_class_id_repeat'] = subscriber.option60.repeat
        params['vendor_class_id_length'] = subscriber.option60.length

    if subscriber.has_option72:
        params['www_server'] = subscriber.option72.id

    if subscriber.has_option23:
        params['dns_server'] = subscriber.option23.id

    if subscriber.has_option18:
        params['interface_id'] = subscriber.option18.id
        params['interface_id_start'] = subscriber.option18.start
        params['interface_id_step'] = subscriber.option18.step
        params['interface_id_repeat'] = subscriber.option18.repeat
        params['interface_id_length'] = subscriber.option18.length

    if subscriber.has_option38:
        params['subscriber_id'] = subscriber.option38.id
        params['subscriber_id_start'] = subscriber.option38.start
        params['subscriber_id_step'] = subscriber.option38.step
        params['subscriber_id_repeat'] = subscriber.option38.repeat
        params['subscriber_id_length'] = subscriber.option38.length

    if subscriber.has_option37:
        params['v6_remote_id'] = subscriber.option37.id
        params['v6_remote_id_start'] = subscriber.option37.start
        params['v6_remote_id_step'] = subscriber.option37.step
        params['v6_remote_id_repeat'] = subscriber.option37.repeat
        params['v6_remote_id_length'] = subscriber.option37.length
        params['enterprise_id'] = subscriber.option37.entid
        params['enterprise_id_step'] = subscriber.option37.entid_step
    if subscriber.has_option6:
        params['option_req'] = subscriber.option6
    if subscriber.has_option20:
        params['option20'] = '1'

    if subscriber.has_softgre:
        params['softgre'] = '1'
        if subscriber.softgre_vlan_id:
            params['gre_vlan_id'] = subscriber.softgre_vlan_id
            if subscriber.softgre_vlan_id_step:
                params['gre_vlan_id_step'] = subscriber.softgre_vlan_id_step
            if subscriber.softgre_vlan_id_repeat:
                params['gre_vlan_id_repeat'] = subscriber.softgre_vlan_id_repeat

        v4addr = ipaddress.IPv4Interface(subscriber.softgre_source)
        source_ip = str(v4addr.ip)
        mask = str(v4addr.netmask)
        params['gre_local_ip'] = source_ip
        params['gre_dst_ip'] = subscriber.softgre_destination
        params['gre_gateway'] = subscriber.softgre_gateway
        params['gre_netmask'] = mask
        params['gre_tunnel_count'] = subscriber.softgre_count
    status = tester.invoke('add_dhcp_client', **params)

    if not status['status']:
        raise BBEDeviceError('Failed to create DHCP subscribers with tag {} on {}'.format(subscriber.tag,
                                                                                          subscriber.rt_device_id))
    # save handles to subscribers
    group_h = status.get('device_group_handle', None)
    if not group_h:
        raise BBEDeviceError('add_dhcp_client did not return device group handle')
    subscriber.rt_device_group_handle = group_h
    if 'ldra_v4_device_group' in status:
        handles = []
        handles.append(status['ldra_v4_device_group'])
        handles.append(group_h)
        subscriber.rt_device_group_handle = handles

    t.log('{} Stored rt device group handle into: {}'.format(__LOGTAG, subscriber))

    eth_h = status.get('ethernet_handle', None)
    if not eth_h:
        raise BBEDeviceError('add_dhcp_client did not return ether handle')
    subscriber.rt_ethernet_handle = eth_h
    t.log('{} Stored rt ethernet handle into: {}'.format(__LOGTAG, subscriber))

    if subscriber.family == 'ipv4' or subscriber.family == 'dual':
        v4_h = status.get('dhcpv4_client_handle', None)
        if not v4_h:
            raise BBEDeviceError('add_dhcp_client did not return dhcpv4 client handle')
        subscriber.rt_dhcpv4_handle = v4_h
        t.log('{} Stored rt dhcpv4 client handle into: {}'.format(__LOGTAG, subscriber))

    if subscriber.family == 'ipv6' or subscriber.family == 'dual':
        v6_h = status.get('dhcpv6_client_handle', None)
        if not v6_h:
            raise BBEDeviceError('add_dhcp_client did not return dhcpv6 client handle')
        subscriber.rt_dhcpv6_handle = v6_h
        t.log('{} Stored rt dhcpv6 client handle into: {}'.format(__LOGTAG, subscriber))
        if subscriber.has_option18 or subscriber.has_option37 or subscriber.has_option38:
            ldra_h = status.get('ldra_handle', None)
            if not ldra_h:
                raise BBEDeviceError('add_dhcp_client did not return ldra handle')
            subscriber.rt_ldra_handle = ldra_h
            t.log('{} Stored rt ldra client handle into: {}'.format(__LOGTAG, subscriber))
            tester.invoke('set_v6_option', handle=ldra_h, **params)

    log_mesg = '{} Created DHCP subscribers for '.format(__LOGTAG)
    log_mesg += 'Router-device: {}, Router-port: {}, '.format(subscriber.device_id, subscriber.router_port)
    log_mesg += 'RT-device: {}, RT-port: {}'.format(subscriber.rt_device_id, subscriber.rt_port)
    log_mesg += 'Subscribers-interface: {}, Subscirbers-tag: {}'.format(subscriber.interface_id,
                                                                        subscriber.tag)
    t.log(log_mesg)


def create_rt_pppoe_subscribers(rt_device_id, subscriber):
    """Create RT PPPoE subscribers

    :param rt_device_id: RT device id such as 'rt0'
    :param subscriber: jnpr.toby.bbe.bbevar.subscribers.PPPoESubscribers instance
    :return: None
    """
    tester = t.get_handle(rt_device_id)
    # parameters to add_pppoe_client
    params = dict()
    params['port'] = subscriber.rt_port
    params['num_sessions'] = subscriber.count
    if int(subscriber.count) < 1:
        t.log('rt emulation for this pppoe sub {} is not created since the session is 0'.format(subscriber.tag))
        return
    params['ip_type'] = subscriber.family
    params['auth_mode'] = subscriber.auth_method
    params['username'] = subscriber.username
    params['password'] = subscriber.password
    # if int(subscriber.keep_alive) == 0:
    #     params['echo_req'] = 0
    # else:
    #     params['echo_req'] = 1
    params['echo_req_interval'] = subscriber.keep_alive
    if 'v6' in subscriber.family or 'dual' in subscriber.family:
        if subscriber.dhcpv6_ia_type and subscriber.dhcpv6_ia_type != 'ndra':
            params['dhcpv6_ia_type'] = subscriber.dhcpv6_ia_type

    if subscriber.vlan_range:
        params['vlan_start'] = subscriber.vlan_range.start
        params['vlan_step'] = subscriber.vlan_range.step
        params['vlan_repeat'] = subscriber.vlan_range.repeat
        params['vlan_length'] = subscriber.vlan_range.length
        if hasattr(subscriber, 'vlan_tpid'):
            params['vlan_tpid'] = subscriber.vlan_tpid
    if subscriber.svlan_range:
        params['svlan_start'] = subscriber.svlan_range.start
        params['svlan_step'] = subscriber.svlan_range.step
        params['svlan_repeat'] = subscriber.svlan_range.repeat
        params['svlan_length'] = subscriber.svlan_range.length
        if hasattr(subscriber, 'svlan_tpid'):
            params['svlan_tpid'] = subscriber.svlan_tpid
    if subscriber.circuit_id:
        params['circuit_id'] = subscriber.circuit_id
    if subscriber.circuit_id_start:
        params['circuit_id_start'] = subscriber.circuit_id_start
    if subscriber.circuit_id_step:
        params['circuit_id_step'] = subscriber.circuit_id_step
    if subscriber.circuit_id_repeat:
        params['circuit_id_repeat'] = subscriber.circuit_id_repeat
    if subscriber.circuit_id_length:
        params['circuit_id_length'] = subscriber.circuit_id_length
    if subscriber.remote_id:
        params['remote_id'] = subscriber.remote_id
    if subscriber.remote_id_start:
        params['remote_id_start'] = subscriber.remote_id_start
    if subscriber.remote_id_step:
        params['remote_id_step'] = subscriber.remote_id_step
    if subscriber.remote_id_repeat:
        params['remote_id_repeat'] = subscriber.remote_id_repeat
    if subscriber.remote_id_length:
        params['remote_id_length'] = subscriber.remote_id_length
    if subscriber.ncp_retry:
        params['max_ipcp_req'] = subscriber.ncp_retry
    if subscriber.mac:
        params['mac'] = subscriber.mac
        if subscriber.mac_step:
            params['mac_step'] = subscriber.mac_step

    status = tester.invoke('add_pppoe_client', **params)

    if not status['status']:
        raise BBEDeviceError('Failed to create PPPoE subscribers with tag {} on {}'.format(subscriber.tag,
                                                                                           subscriber.rt_device_id))
    # save handles to subscribers
    group_h = status.get('device_group_handle', None)
    if not group_h:
        raise BBEDeviceError('add_pppoe_client did not return device group handle')
    subscriber.rt_device_group_handle = group_h
    t.log('{} Stored rt device group handle into: {}'.format(__LOGTAG, subscriber))

    eth_h = status.get('ethernet_handle', None)
    if not eth_h:
        raise BBEDeviceError('add_pppoe_client did not return ether handle')
    subscriber.rt_ethernet_handle = eth_h
    t.log('{} Stored rt ethernet handle into: {}'.format(__LOGTAG, subscriber))

    #if subscriber.family == 'ipv4' or subscriber.family == 'dual':
    pppox_h = status.get('pppox_client_handle', None)
    if not pppox_h:
        raise BBEDeviceError('add_pppoe_client did not return pppox client handle')
    subscriber.rt_pppox_handle = pppox_h
    t.log('{} Stored rt pppox client handle into: {}'.format(__LOGTAG, subscriber))

    if subscriber.family == 'ipv6' or subscriber.family == 'dual':
        if subscriber.essm_count or subscriber.dhcpv6_ia_type == 'ndra':
            v6_h = None
        else:
            v6_h = status.get('dhcpv6_client_handle', None)
            if not v6_h:
                raise BBEDeviceError('add_pppoe_client did not return dhcpv6 client handle')
            subscriber.rt_dhcpv6_handle = v6_h
            t.log('{} Stored rt dhcpv6 client handle into: {}'.format(__LOGTAG, subscriber))
            if subscriber.has_option6:
                option_req = subscriber.option6
                tester.invoke('set_v6_option', handle=v6_h, option_req=option_req)


    log_mesg = '{} Created PPPoE subscribers for '.format(__LOGTAG)
    log_mesg += 'Router-device: {}, Router-port: {}, '.format(subscriber.device_id, subscriber.router_port)
    log_mesg += 'RT-device: {}, RT-port: {}'.format(subscriber.rt_device_id, subscriber.rt_port)
    log_mesg += 'Subscribers-interface: {}, Subscirbers-tag: {}'.format(subscriber.interface_id,
                                                                        subscriber.tag)
    t.log(log_mesg)


def add_rt_lns(rt_device_id):
    """
    Create RT LNS server for L2TP, in this case, no uplink is needed
    :param rt_device_id: RT device id such as 'rt0'
    :return: None
    """

    tester = t.get_handle(rt_device_id)  # rt handle
    lns = bbe.get_interfaces(rt_device_id, interfaces='lns', id_only=False)
    for link in lns:
        params = dict()
        params['port'] = link.interface_pic
        con = bbe.get_connection(rt_device_id, link.interface_id)
        if con.interface_config:
            params['tun_auth_enable'] = con.interface_config.get('tun_auth_enable', '1')
            params['tun_secret'] = con.interface_config.get('tun_secret', 'joshua')
            v4addr = ipaddress.IPv4Interface(con.interface_config['ip'])
            params['l2tp_dst_addr'] = str(v4addr.ip)
            params['netmask'] = str(v4addr.netmask)
            params['l2tp_src_addr'] = con.interface_config['l2tp_dst_addr']
            params['l2tp_src_prefix_len'] = str(v4addr._prefixlen)
            params['auth_mode'] = con.interface_config.get('auth_mode', 'pap')
            params['username'] = con.interface_config.get('username', 'test@ABC1.com')
            params['password'] = con.interface_config.get('password', 'joshua')
            params['hostname'] = con.interface_config.get('hostname', 'mx_lac')
            params['lns_host_name'] = con.interface_config.get('lns_host_name', 'ixia_lns')

            if 'tun_hello_req' in con.interface_config:
                params['tun_hello_req'] = con.interface_config['tun_hello_req']
            if 'tun_hello_interval' in con.interface_config:
                params['tun_hello_interval'] = con.interface_config['tun_hello_interval']
            params['vlan_id'] = con.interface_config.get('vlan-id', '1')
            if 'ip_cp' in con.interface_config:
                params['ip_cp'] = con.interface_config['ip_cp']
            if 'lease-time' in con.interface_config:
                params['lease_time'] = con.interface_config['lease-time']
            if 'dhcpv6-ia-type' in con.interface_config:
                params['dhcpv6_ia_type'] = con.interface_config['dhcpv6-ia-type']
            if 'pool-prefix-start' in con.interface_config:
                params['pool_prefix_start'] = con.interface_config['pool-prefix-start']
            if 'pool-prefix-length' in con.interface_config:
                params['pool_prefix_length'] = con.interface_config['pool-prefix-length']
            if 'pool-prefix-size' in con.interface_config:
                params['pool_prefix_size'] = con.interface_config['pool-prefix-size']
            result = tester.invoke('add_l2tp_server', **params)
            if result['status'] != '1':
                raise BBEDeviceError('Failed to add LNS {} {}'.format(rt_device_id, link.interface_pic))
            else:
                link.rt_ethernet_handle = result.get('ethernet_handle', None)
                link.rt_ipv4_handle = result.get('ipv4_handle', None)
                link.rt_lns_handle = result.get('lns_handle', None)
                link.rt_lns_server_session_handle = result.get('pppox_server_sessions_handle', None)
                t.log('{} Added {} LNS {}'.format(__LOGTAG, rt_device_id, link.interface_pic))


def create_rt_l2tp_subscribers(rt_device_id, subscriber):
    """
    rt.add_l2tp_client(port='1/2',num_tunnels_per_lac=20,l2tp_dst_addr='100.0.0.3', l2tp_src_addr='10.200.0.2',
     tun_auth='authenticate_hostname', tun_secret='testlac', sessions_per_tunnel='6', hostname='lac',
      l2tp_src_count=10, l2tp_src_gw='10.200.0.1', l2tp_src_prefix_len='24', auth_mode='pap',
       username='test@domain?.com', password='joshua')
    :param rt_device_id:
    :param subscriber:
    :return:
    """
    tester = t.get_handle(rt_device_id)  # rt handle
    l2tp_params = dict()
    l2tp_params['port'] = subscriber.rt_port
    l2tp_params['num_tunnels_per_lac'] = subscriber.tunnels_per_lac
    l2tp_params['l2tp_src_count'] = subscriber.num_of_lac
    if int(subscriber.num_of_lac) < 1:
        t.log('rt emualtion for this l2tp sub {} is not created since the num_of_lac is 0'.format(subscriber.tag))
        return
    l2tp_params['sessions_per_tunnel'] = subscriber.sessions_per_tunnel
    l2tp_params['tun_auth_enable'] = subscriber.tunnel_auth_enable
    l2tp_params['tun_secret'] = subscriber.tunnel_secret
    l2tp_params['l2tp_src_addr'] = subscriber.tunnel_source_ip
    l2tp_params['l2tp_dst_addr'] = subscriber.tunnel_destination_ip
    if 'v4' in subscriber.family:
        l2tp_params['ip_cp'] = 'ipv4_cp'
    if 'v6' in subscriber.family:
        l2tp_params['ip_cp'] = 'ipv6_cp'
    if 'dual' in subscriber.family:
        l2tp_params['ip_cp'] = 'dual_stack'
    if subscriber.dhcpv6_ia_type:
        l2tp_params['dhcpv6_ia_type'] = subscriber.dhcpv6_ia_type
    l2tp_params['hostname'] = subscriber.lac_hostname
    l2tp_params['l2tp_src_gw'] = subscriber.tunnel_source_gateway
    l2tp_params['l2tp_src_prefix_len'] = subscriber.tunnel_prefix_length
    if subscriber.tunnel_source_step:
        l2tp_params['l2tp_src_step'] = subscriber.tunnel_source_step
    if subscriber.tunnel_destination_step:
        l2tp_params['l2tp_dst_step'] = subscriber.tunnel_destination_step
    l2tp_params['auth_mode'] = subscriber.auth_method
    l2tp_params['username'] = subscriber.username
    l2tp_params['password'] = subscriber.password
    l2tp_params['vlan_id'] = subscriber.tunnel_vlan_id
    l2tp_params['vlan_id_step'] = subscriber.tunnel_vlan_step
    if subscriber.tunnel_hello_req:
        l2tp_params['tun_hello_req'] = subscriber.tunnel_hello_req
    if subscriber.tunnel_hello_interval:
        l2tp_params['tun_hello_interval'] = subscriber.tunnel_hello_interval
    print(l2tp_params)
    t.log('l2tp params is {}'.format(l2tp_params))
    result = tester.invoke('add_l2tp_client', **l2tp_params)
    if result['status'] == '0':
        raise BBEDeviceError('Failed to add l2tp client {} {}'.format(rt_device_id, subscriber.rt_port))
    else:
        subscriber.rt_lac_handle = result['lac_handle']
        subscriber.rt_pppox_handle = result['pppox_client_handle']
        if 'dhcpv6_client_handle' in result:
            subscriber.rt_dhcpv6_handle = result['dhcpv6_client_handle']
        subscriber.rt_ethernet_handle = result['ethernet_handle']
        ###no device group return from ixia invoke, using pppox_client_handle for client_action
        subscriber.rt_device_group_handle = result['pppox_client_handle']


def add_rt_links(rt_device_id):
    """Create RT uplink interfaces

    :param rt_device_id: RT device id such as 'rt0'
    :return: None
    """
    tester = t.get_handle(rt_device_id)  # rt handle
    #tester = t.get_handle(rt_device_id)
    uplinks = bbe.get_interfaces(rt_device_id, interfaces='uplink', id_only=False)
    custom_links = bbe.get_interfaces(rt_device_id, interfaces='custom', id_only=False)
    links = uplinks + custom_links
    for link in links:
        params = dict()  # parameters to add_link
        params['port'] = link.interface_pic
        ip_addr = None
        mask = None
        ip_step = None
        gateway = None
        gateway_mac = None
        ipv6_addr = None
        ipv6_prefix_length = None
        ipv6_gateway = None
        ipv6_step = None
        mac_addr = None
        mac_step = None
        # Get gateway address from the other end of the connection
        try:
            con = bbe.get_connection(rt_device_id, link.interface_id)
            print(vars(con))
        except:
            t.log('No connection was found for this link: {}'.format(__LOGTAG, link))
            continue
        if con.interface_config:
            con_ipv4 = con.interface_config.get('ip', None)
            con_ipv6 = con.interface_config.get('ipv6', None)
            if 'mac' in con.interface_config:
                mac_addr = con.interface_config['mac']
            if not con.vlan_range and 'uplink0' in con.interface_id:
                params['vlan_start'] = '1'
                params['vlan_step'] = '0'
                params['vlan_repeat'] = '1'
                params['vlan_length'] = '1'
                params['count'] = '1'
            if con.vlan_range:
                params['vlan_start'] = con.vlan_range.start
                params['vlan_step'] = con.vlan_range.step
                params['vlan_repeat'] = con.vlan_range.repeat
                params['vlan_length'] = con.vlan_range.length
                params['count'] = int(con.vlan_range.repeat) * int(con.vlan_range.length)
                params['vlan_tpid'] = con.vlan_tpid
            if con.svlan_range:
                params['svlan_start'] = con.svlan_range.start
                params['svlan_step'] = con.svlan_range.step
                params['svlan_repeat'] = con.svlan_range.repeat
                params['svlan_length'] = con.svlan_range.length
                params['svlan_tpid'] = con.svlan_tpid
                params['count'] = int(con.svlan_range.repeat) * int(con.svlan_range.length)
            if con_ipv4:
                # from prefix to address and mask
                v4_addr = ipaddress.IPv4Interface(con_ipv4)
                gateway = str(v4_addr.ip)
                mask = str(v4_addr.netmask)
                ip_addr = str(v4_addr.ip + 1)
                ip_step = con.interface_config.get('ip-step', None)
                if con.is_ae:
                    result = re.match(r'ae(\d+)', con.ae_bundle)
                    mac_addr = "ae:00:00:00:00:" + result.group(1).zfill(2)
                    ip_step = '0.0.0.0'
                    mac_step = "00:00:00:00:00:00"
                gateway_mac = con.interface_config.get('gateway-mac', None)
            if con_ipv6:
                # from prefix to address and mask
                v6_addr = ipaddress.IPv6Interface(con_ipv6)
                ipv6_gateway = str(v6_addr.ip)
                ipv6_prefix_length = str(v6_addr._prefixlen)
                ipv6_addr = str(v6_addr.ip + 1)
                ipv6_step = con.interface_config.get('ipv6-step', None)
                if con.is_ae:
                    ipv6_step = "0:0:0:0:0:0:0:0"
                    mac_step = "00:00:00:00:00:00"
                gateway_mac = con.interface_config.get('gateway-mac', None)
            if not con_ipv4 and not con_ipv6 and 'uplink0' in link.interface_id:
                ip_addr = '200.0.0.2'
                mask = '255.255.255.0'
                gateway = '200.0.0.1'
                ipv6_addr = '200:0:0::2'
                ipv6_prefix_length = '64'
                ipv6_gateway = '200:0:0::1'
        elif 'uplink0' in con.interface_id:
            ip_addr = '200.0.0.2'
            mask = '255.255.255.0'
            gateway = '200.0.0.1'
            ipv6_addr = '200:0:0::2'
            ipv6_prefix_length = '64'
            ipv6_gateway = '200:0:0::1'
            params['vlan_start'] = '1'
            params['vlan_step'] = '0'
            params['vlan_repeat'] = '1'
            params['vlan_length'] = '1'
            params['count'] = '1'
            if con.is_ae_active:
                ip_step = "0.0.0.0"
                ipv6_step = "0:0:0:0:0:0:0:0"
        if ip_addr:
            params['ip_addr'] = ip_addr
        if mask:
            params['netmask'] = mask
        if gateway:
            params['gateway'] = gateway
        if gateway_mac:
            params['gateway_mac'] = gateway_mac
        if ip_step:
            params['ip_addr_step'] = ip_step
        if ipv6_addr:
            params['ipv6_addr'] = ipv6_addr
        if ipv6_gateway:
            params['ipv6_gateway'] = ipv6_gateway
        if ipv6_prefix_length:
            params['ipv6_prefix_length'] = ipv6_prefix_length
        if ipv6_step:
            params['ipv6_addr_step'] = ipv6_step
        if mac_addr:
            params['mac'] = mac_addr
        if mac_step:
            params['mac_step'] = mac_step
        if con.is_ae:
            if len(params) == 1 and 'port' in params:
                t.log('ignore this port {} for ae'.format(params['port']))
                continue
            else:
                params['mac_step'] = "00:00:00:00:00:01"
                if ip_addr:
                    params['ip_addr_step'] = "0.0.0.1"
                    params['gateway_step'] = "0.0.0.0"
                if ipv6_addr:
                    params['ipv6_addr_step'] = "00:00:00:00:00:00:00:01"
                    params['ipv6_gateway_step'] = "00:00:00:00:00:00:00:00"
        status = tester.invoke('add_link', **params)

        if status['status'] == '0':
            raise BBEDeviceError('Failed to add link {} {}'.format(rt_device_id, link.interface_pic))

        link.rt_device_group_handle = status.get('device_group_handle', None)
        link.rt_ethernet_handle = status.get('ethernet_handle', None)
        link.rt_ipv4_handle = status.get('ipv4_handle', None)
        link.rt_ipv6_handle = status.get('ipv6_handle', None)

        t.log('{} Added {} link {}'.format(__LOGTAG, rt_device_id, link.interface_pic))


def add_rt_isis_l3(rt_device_id):
    """Add RT ISIS emulation.

    Read configuration from BBE config yaml, e.g.
                uplink0:
                    uv-bbe-config:
                        ip: 200.0.0.1/24
                        ipv6: 3000:db8:ffff:1::1/64
                        isis:
                            auth_type: md5
                            auth_key: bharti
                            intf_type: ptop
                            prefix:
                                multiplier: 2
                                prefix_type: ipv4-prefix
                                ipv4_prefix_network_address: 101.1.0.0
                                ipv4_prefix_network_address_step: 1.0.0.0
                                ipv4_prefix_length: 24
                                ipv4_prefix_address_step: 1
                                ipv4_prefix_number_of_addresses: 22500

    :param rt_device_id: RT device id, e.g. 'rt0'
    :return: None

        handle:    eth handle
        auth_type: authentication type, e.g. 'md5'
        auth_key:  authentication password
        intf_type: interface type, e.g., ptop or broadcast

        multiplier: multiplier for prefix device groups
        prefix_type: family type, support ipv4-prefix only for now
        ipv4_prefix_network_address: base address
        ipv4_prefix_network_address_step: network address step, e.g, 1.0.0.0
        ipv4_prefix_length: prefix length, e.g. 24
        ipv4_prefix_address_step: address step, e.g., 1
        ipv4_prefix_number_of_addresses: number of addresses in each group, e.g., 2000

    """
    tester = t.get_handle(rt_device_id)  # rt handle
    interfaces = bbe.get_interfaces(rt_device_id)
    for interface in interfaces:
        # con the the non-rt device on which isis is configured
        con = bbe.get_connection(rt_device_id, interface.interface_id)
        if not con:
            continue
        if not con.interface_config:
            continue
        if 'isis' in con.interface_config:
            isis_cfg = con.interface_config['isis']
            isis_cfg_prefix = con.interface_config['isis']['prefix']

            isis_params = dict()
            isis_params['handle'] = interface.rt_ethernet_handle
            if 'auth_type' in isis_cfg:
                isis_params['auth_type'] = isis_cfg['auth_type']
            if 'auth_key' in isis_cfg:
                isis_params['auth_key'] = isis_cfg['auth_key']
            if 'intf_type' in isis_cfg:
                isis_params['intf_type'] = isis_cfg['intf_type']
            if 'multiplier' in isis_cfg_prefix:
                isis_params['multiplier'] = isis_cfg_prefix['multiplier']
            if 'prefix_type' in isis_cfg_prefix:
                isis_params['prefix_type'] = isis_cfg_prefix['prefix_type']
            if 'ipv4_prefix_network_address' in isis_cfg_prefix:
                isis_params['ipv4_prefix_network_address'] = isis_cfg_prefix['ipv4_prefix_network_address']
            if 'ipv4_prefix_network_address_step' in isis_cfg_prefix:
                isis_params['ipv4_prefix_network_address_step'] = isis_cfg_prefix['ipv4_prefix_network_address_step']
            if 'ipv4_prefix_length' in isis_cfg_prefix:
                isis_params['ipv4_prefix_length'] = isis_cfg_prefix['ipv4_prefix_length']
            if 'ipv4_prefix_address_step' in isis_cfg_prefix:
                isis_params['ipv4_prefix_address_step'] = isis_cfg_prefix['ipv4_prefix_address_step']
            if 'ipv4_prefix_number_of_addresses' in isis_cfg_prefix:
                isis_params['ipv4_prefix_number_of_addresses'] = isis_cfg_prefix['ipv4_prefix_number_of_addresses']

            t.log("bbert.add_rt_isis_l3 got ISIS data from configuration yaml: {}".format(isis_params))
            result = tester.invoke('add_isis', **isis_params)
            if result['status'] != '1':
                raise BBEDeviceError('Failed to add ISIS {} {} {}'.format(rt_device_id,
                                                                              interface.interface_id, isis_params))


def add_rt_bgp_neighbor(rt_device_id):
    """
    :param rt_device_id:        RT device id, e.g. 'rt0'
    :return: None
    """
    tester = t.get_handle(rt_device_id)  # rt handle
    interfaces = bbe.get_interfaces(rt_device_id)
    for interface in interfaces:
        con = bbe.get_connection(rt_device_id, interface.interface_id)
        if not con:
            continue
        if not con.interface_config:
            continue
        if 'bgp' in con.interface_config:
            bgp_params = dict()
            if con.vlan_range:
                vlan_id = int(con.vlan_range.start)
            for neighbor in con.interface_config['bgp']['neighbors']:
                v4addr = ipaddress.IPv4Interface(con.interface_config['ip'])
                if neighbor['remote-ip'] != str(v4addr.ip + 1):
                    #add new device group
                    link_params = dict()
                    link_params['port'] = interface.interface_pic
                    if neighbor['local-ip'] != str(v4addr.ip):
                        if con.vlan_range:
                            vlan_id += 1
                    if con.vlan_range:
                        link_params['vlan_start'] = str(vlan_id)
                    link_params['ip_addr'] = neighbor['remote-ip']
                    link_params['netmask'] = str(v4addr.netmask)
                    link_params['gateway'] = neighbor['local-ip']
                    result = tester.invoke('add_link', **link_params)
                    if result['status'] != '1':
                        raise BBEDeviceError('Failed to add link {} {}'.format(rt_device_id, link_params))
                    bgp_params['handle'] = result['ipv4_handle']
                else:
                    bgp_params['handle'] = interface.rt_ipv4_handle
                if 'keepalive' in neighbor:
                    bgp_params['keepalive'] = neighbor['keepalive']
                if 'holdtime' in neighbor:
                    bgp_params['hold_time'] = neighbor['holdtime']
                if 'restart_time' in neighbor:
                    bgp_params['restart_time'] = neighbor['restart_time']
                if 'enable_flap' in neighbor:
                    bgp_params['enable_flap'] = neighbor['enable_flap']
                    bgp_params['flap_up_time'] = neighbor['flap_up_time']
                    bgp_params['flap_down_time'] = neighbor['flap_down_time']
                if 'stale_time' in neighbor:
                    bgp_params['stale_time'] = neighbor['stale_time']
                if 'graceful_restart' in neighbor:
                    bgp_params['graceful_restart'] = neighbor['graceful_restart']
                bgp_params['type'] = neighbor['type']
                bgp_params['remote_ip'] = neighbor['local-ip']
                bgp_params['local_as'] = neighbor.get('remote-as', con.interface_config['bgp']['local-as'])
                bgp_params['prefix_group'] = neighbor['prefix']
                result = tester.invoke('add_bgp', **bgp_params)
                if result['status'] != '1':
                    raise BBEDeviceError('Failed to add bgp {} {} {}'.format(rt_device_id,
                                                                             interface.interface_id, bgp_params))

        if 'bgp+' in con.interface_config:
            bgp_params = dict()
            if con.vlan_range:
                vlan_id = int(con.vlan_range.start)
            for neighbor in con.interface_config['bgp+']['neighbors']:
                v6addr = ipaddress.IPv6Interface(con.interface_config['ipv6'])
                if neighbor['remote-ip'] != str(v6addr.ip + 1):
                    #add new device group
                    link_params = dict()
                    link_params['port'] = interface.interface_pic
                    if neighbor['local-ip'] != str(v6addr.ip):
                        if con.vlan_range:
                            vlan_id += 1
                    if con.vlan_range:
                        link_params['vlan_start'] = str(vlan_id)
                    link_params['ip_addr'] = neighbor['remote-ip']
                    link_params['netmask'] = str(v6addr.netmask)
                    link_params['gateway'] = neighbor['local-ip']
                    result = tester.invoke('add_link', **link_params)
                    if result['status'] != '1':
                        raise BBEDeviceError('Failed to add link {} {}'.format(rt_device_id, link_params))
                    bgp_params['handle'] = result['ipv6_handle']
                else:
                    bgp_params['handle'] = interface.rt_ipv6_handle
                if 'keepalive' in neighbor:
                    bgp_params['keepalive'] = neighbor['keepalive']
                if 'holdtime' in neighbor:
                    bgp_params['hold_time'] = neighbor['holdtime']
                if 'restart_time' in neighbor:
                    bgp_params['restart_time'] = neighbor['restart_time']
                if 'enable_flap' in neighbor:
                    bgp_params['enable_flap'] = neighbor['enable_flap']
                    bgp_params['flap_up_time'] = neighbor['flap_up_time']
                    bgp_params['flap_down_time'] = neighbor['flap_down_time']
                if 'stale_time' in neighbor:
                    bgp_params['stale_time'] = neighbor['stale_time']
                if 'graceful_restart' in neighbor:
                    bgp_params['graceful_restart'] = neighbor['graceful_restart']
                bgp_params['type'] = neighbor['type']
                bgp_params['remote_ip'] = neighbor['local-ip']
                bgp_params['local_as'] = neighbor.get('remote-as', con.interface_config['bgp+']['local-as'])
                bgp_params['prefix_group'] = neighbor['prefix']
                result = tester.invoke('add_bgp', **bgp_params)
                if result['status'] != '1':
                    raise BBEDeviceError('Failed to add bgp+ {} {} {}'.format(rt_device_id,
                                                                              interface.interface_id, bgp_params))


def add_rt_dhcp_servers(rt_device_id='rt0', family='ipv4'):
    """Add RT DHCP server.

    :param rt_device_id: RT device id, e.g., 'rt0'
    :param family: 'ipv4' or 'ipv6'
    :return: None
    """
    try:
        tester = t.get_handle(rt_device_id)  # rt handle
    except:
        t.log("no rt device {}, skip configuring rt dhcp server".format(rt_device_id))
        return
    #tester = t.get_handle(rt_device_id)
    # server is added on uplink0 only
    server = bbe.get_rt_dhcp_server(family)
    if server.server_mode.lower() == 'local':
        t.log('no need to create dhcp server foir family {}'.format(family))
        return
    uplinks = bbe.get_interfaces(rt_device_id, interfaces='uplink0', id_only=False)
    if len(uplinks) != 1:
        t.log('Cannot find {} uplink interface to add dhcp server'.format(rt_device_id))
        return

    uplink = uplinks[0]

    if family == 'ipv4':
        #server = bbe.get_rt_dhcp_server(family)
        if uplink.rt_ipv4_handle:
            status = tester.invoke('add_dhcp_server',
                                   handle=uplink.rt_ipv4_handle,
                                   pool_size=server.pool_size,
                                   pool_start_addr=server.pool_start_address,
                                   pool_mask_length=server.pool_mask_length,
                                   pool_gateway=server.pool_gateway,
                                   lease_time=server.lease_time,
                                   multi_servers_config_v4=server.multi_servers_config)

            if not status['status']:
                raise BBEDeviceError('Failed to add DHCPv4 server on {}'.format(rt_device_id))

            if not status.get('dhcpv4_server_handle', None):
                raise BBEDeviceError('add_dhcp_server did not return dhcpv4_server_handle')

            server.created = True
            server.server_interface = uplink
            server.server_handle = status['dhcpv4_server_handle']

    if family == 'ipv6':
        #server = bbe.get_rt_dhcp_server(family)
        if uplink.rt_ipv6_handle:
            status = tester.invoke('add_dhcp_server',
                                   handle=uplink.rt_ipv6_handle,
                                   pool_size=server.pool_size,
                                   pool_start_addr=server.pool_start_address,
                                   pool_mask_length=server.pool_mask_length,
                                   dhcpv6_ia_type=server.pool_ia_type,
                                   pool_prefix_start=server.pool_prefix_start,
                                   pool_prefix_length=server.pool_prefix_length,
                                   pool_prefix_size=server.pool_prefix_size,
                                   lease_time=server.lease_time,
                                   multi_servers_config_v6=server.multi_servers_config)

            if not status['status']:
                raise BBEDeviceError('Failed to add DHCPv6 server on {}'.format(rt_device_id))

            if not status.get('dhcpv6_server_handle', None):
                raise BBEDeviceError('add_dhcp_server did not return dhcpv6_server_handle')

            server.created = True
            server.server_interface = uplink
            server.server_handle = status['dhcpv6_server_handle']


def set_subscribers_call_rate(rt_device_id):
    """Set CSR and CLR rates

    IXIA requires setting rates separately for dhcpv4, dhcpv6, and pppoe.
    In addition, rates cannot be set individually for each emulation handle.
    But it requires a list of all rates for each type (dhcpv4, dhcpv6, pppoe)

    :param rt_device_id: RT device id, e.g., 'rt0'
    :return: None
    """
    tester = t.get_handle(rt_device_id)  # rt handle
    #tester = t.get_handle(rt_device_id)
    # Set dhcpv4 rate
    dhcpv4_subs = bbe.get_subscriber_handles(protocol='dhcp', family='ipv4')
    if dhcpv4_subs:  # not an empty list, any handle is ok to rt api
        a_handle = dhcpv4_subs[0].rt_dhcpv4_handle
        rates = bbe.get_subscribers_call_rate('dhcp', 'ipv4')
        tester.invoke('set_dhcp_rate', handle=a_handle, **rates)

    # Set dhcpv6 rates
    dhcpv6_subs = bbe.get_subscriber_handles(family='ipv6') + bbe.get_subscriber_handles(family='dual')
    actualv6 = []
    for subs in dhcpv6_subs:
        if subs.rt_dhcpv6_handle:
            actualv6.append(subs)

    if actualv6:  # not an empty list, any handle is ok to rt api
        a_handle = actualv6[0].rt_dhcpv6_handle
        rates = bbe.get_subscribers_call_rate('dhcp', 'ipv6')
        tester.invoke('set_dhcp_rate', handle=a_handle, **rates)

    # Set pppoe rates
    pppoe_subs = bbe.get_subscriber_handles(protocol='pppoe')
    l2tp_subs = bbe.get_subscriber_handles(protocol='l2tp')
    pppoe_subs += l2tp_subs
    if pppoe_subs:  # not an empty list, any handle is ok to rt api
        a_handle = pppoe_subs[0].rt_pppox_handle
        rates = bbe.get_subscribers_call_rate('pppoe')
        tester.invoke('set_pppoe_rate', handle=a_handle, **rates)

# def set_ancp_rate(rt_device_id):
#     """Set ANCP start/stop/port-up rates
#
#     IXIA requires setting rates separately for ANCP.
#     In addition, rates cannot be set individually for each emulation handle.
#     But it requires a list of all rates for ANCP.
#
#     :param rt_device_id: RT device id, e.g., 'rt0'
#     :return: None
#     """
#     tester = t.get_handle(rt_device_id)  # rt handle
#     # Set l2bsa rate
#     subs = bbe.get_subscriber_handles()
#     if subs:  # not an empty list, any handle is ok to rt api
#         a_handle = subs[0].rt_ethernet_handle
#         rates = bbe.get_ancp_rate()
#         tester.invoke('set_ancp_rate', handle=a_handle, **rates)

def create_ancp_node(rt_device_id, subscriber):
    """
    :param subscriber:   subscriber object
    :param rt_device_id:  rt device name
    :return:
    """
    if subscriber.has_ancp:
        tester = t.get_handle(rt_device_id)  # rt handle
        ancp_args = dict()
        ancp_args['port'] = subscriber.rt_port
        ancp_args['count'] = subscriber.ancp_count
        ancp_args['lines_per_node'] = subscriber.ancp_lines_per_node
        if subscriber.ancp_dsl_type:
            ancp_args['dsl_type'] = subscriber.ancp_dsl_type
        if subscriber.ancp_pon_type:
            ancp_args['tech_type'] = 'pon'
            ancp_args['pon_type'] = subscriber.ancp_pon_type
        ancp_args['dut_ip'] = subscriber.ancp_dut_ip
        v4address = ipaddress.IPv4Interface(subscriber.ancp_ip)
        source_ip = str(v4address.ip)
        mask = str(v4address.netmask)
        ancp_args['ip_addr'] = source_ip
        ancp_args['ip_addr_step'] = subscriber.ancp_ip_step
        ancp_args['netmask'] = mask
        ancp_args['gateway'] = subscriber.ancp_gateway
        if subscriber.ancp_gateway_step:
            ancp_args['gateway_step'] = subscriber.ancp_gateway_step
        ancp_args['vlan_allocation_model'] = subscriber.ancp_vlan_allocation_model

        if subscriber.ancp_vlan_range:
            ancp_args['vlan_start'] = subscriber.ancp_vlan_range.start
            ancp_args['vlan_step'] = subscriber.ancp_vlan_range.step
            ancp_args['vlan_repeat'] = subscriber.ancp_vlan_range.repeat
            ancp_args['vlan_length'] = subscriber.ancp_vlan_range.length
            ancp_args['vlan_tpid'] = subscriber.ancp_vlan_tpid
        if subscriber.ancp_svlan_range:
            ancp_args['svlan_start'] = subscriber.ancp_svlan_range.start
            ancp_args['svlan_step'] = subscriber.ancp_svlan_range.step
            ancp_args['svlan_repeat'] = subscriber.ancp_svlan_range.repeat
            ancp_args['svlan_length'] = subscriber.ancp_svlan_range.length
            ancp_args['svlan_tpid'] = subscriber.ancp_svlan_tpid

        if subscriber.subscribers_type == 'dhcp':
            ###get option82
            if subscriber.has_option82:
                ancp_args['circuit_id'] = subscriber.option82_aci.id
                ancp_args['circuit_id_start'] = subscriber.option82_aci.start
                ancp_args['circuit_id_step'] = subscriber.option82_aci.step
                ancp_args['circuit_id_repeat'] = subscriber.option82_aci.repeat
                ancp_args['circuit_id_length'] = subscriber.option82_aci.length
                if subscriber.ancp_enable_remoteid:
                    ancp_args['remote_id'] = subscriber.option82_ari.id
                    ancp_args['remote_id_start'] = subscriber.option82_ari.start
                    ancp_args['remote_id_step'] = subscriber.option82_ari.step
                    ancp_args['remote_id_repeat'] = subscriber.option82_ari.repeat
                    ancp_args['remote_id_length'] = subscriber.option82_ari.length
        if subscriber.subscribers_type == 'pppoe' or subscriber.subscribers_type == 'l2bsa':
            ###get circuit id /remote id
            if subscriber.circuit_id:
                ancp_args['circuit_id'] = subscriber.circuit_id
                if subscriber.circuit_id_start:
                    ancp_args['circuit_id_start'] = subscriber.circuit_id_start
                if subscriber.circuit_id_step:
                    ancp_args['circuit_id_step'] = subscriber.circuit_id_step
                if subscriber.circuit_id_repeat:
                    ancp_args['circuit_id_repeat'] = subscriber.circuit_id_repeat
                if subscriber.circuit_id_length:
                    ancp_args['circuit_id_length'] = subscriber.circuit_id_length
            if subscriber.ancp_enable_remoteid:
                ancp_args['remote_id'] = subscriber.remote_id
                if subscriber.remote_id_start:
                    ancp_args['remote_id_start'] = subscriber.remote_id_start
                if subscriber.remote_id_step:
                    ancp_args['remote_id_step'] = subscriber.remote_id_step
                if subscriber.remote_id_repeat:
                    ancp_args['remote_id_repeat'] = subscriber.remote_id_repeat
                if subscriber.remote_id_length:
                    ancp_args['remote_id_length'] = subscriber.remote_id_length
        if subscriber.vlan_range:
            ancp_args['customer_vlan_start'] = subscriber.vlan_range.start
            ancp_args['customer_vlan_step'] = subscriber.vlan_range.step
            ancp_args['customer_vlan_repeat'] = subscriber.vlan_range.repeat
            ancp_args['customer_vlan_length'] = subscriber.vlan_range.length

        if subscriber.svlan_range:
            ancp_args['service_vlan_start'] = subscriber.svlan_range.start
            ancp_args['service_vlan_step'] = subscriber.svlan_range.step
            ancp_args['service_vlan_repeat'] = subscriber.svlan_range.repeat
            ancp_args['service_vlan_length'] = subscriber.svlan_range.length
        if subscriber.ancp_flap_mode:
            ancp_args['flap_mode'] = subscriber.ancp_flap_mode
        result = tester.invoke('add_ancp', **ancp_args)
        if result['status'] != '1':
            raise BBEDeviceError('Failed to add ancp node on {} for sub {}'.format(rt_device_id, subscriber))
        subscriber.rt_ancp_handle = result['ancp_handle']
        subscriber.rt_ancp_line_handle = result['ancp_subscriber_lines_handle']

def add_mcast_client(rt_device_id, subscriber):
    """
    :param rt_device_id:              rt device name
    :param subscriber:                subscriber object
    :return:
    """
    tester = t.get_handle(rt_device_id)
    if hasattr(subscriber, 'rt_dhcpv4_handle') and subscriber.rt_dhcpv4_handle:
        v4handle = subscriber.rt_dhcpv4_handle
    if hasattr(subscriber, 'rt_pppox_handle') and subscriber.rt_pppox_handle:
        v4handle = subscriber.rt_pppox_handle
    if hasattr(subscriber, 'rt_dhcpv6_handle') and subscriber.rt_dhcpv6_handle:
        v6handle = subscriber.rt_dhcpv6_handle
    if subscriber.has_igmp:
        igmp_args = dict()
        igmp_args['handle'] = v4handle
        igmp_args['version'] = subscriber.igmp_version
        igmp_args['filter_mode'] = subscriber.igmp_filter_mode
        if subscriber.igmp_iptv:
            igmp_args['iptv'] = subscriber.igmp_iptv
        if subscriber.igmp_group_enable:
            igmp_args['group_start_addr'] = subscriber.igmp_mcast_group_range.start
            igmp_args['group_step'] = subscriber.igmp_mcast_group_range.step
            igmp_args['group_count'] = subscriber.igmp_mcast_group_range.count
            igmp_args['group_range'] = subscriber.igmp_group_range_count
            if int(subscriber.igmp_group_range_count) > 1:
                igmp_args['group_range_length'] = subscriber.igmp_group_range_count
                if subscriber.igmp_one_group_per_sub:
                    t.log('ERROR', 'does not support group range-count > 1 and one-group-per-sub at the same time')
            elif subscriber.igmp_one_group_per_sub:
                igmp_args['group_count'] = '1'
                igmp_args['group_range_length'] = subscriber.igmp_mcast_group_range.count
                igmp_args['group_range_step'] = subscriber.igmp_mcast_group_range.step

        if subscriber.igmp_source_enable:
            igmp_args['src_grp_start_addr'] = subscriber.igmp_mcast_source_range.start
            igmp_args['src_grp_step'] = subscriber.igmp_mcast_source_range.step
            igmp_args['src_grp_count'] = subscriber.igmp_mcast_source_range.count
            igmp_args['src_grp_range'] = subscriber.igmp_source_range_count
        result = tester.invoke('add_igmp_client', **igmp_args)
        if result['status'] != '1':
            raise BBEDeviceError('Failed to add igmp client  on handle {} for sub {}'.format(v4handle, subscriber))
        subscriber.rt_igmp_handle = result['igmp_host_handle']
        subscriber.rt_igmp_group_handle = result['igmp_group_handle']
        subscriber.rt_igmp_source_handle = result['igmp_source_handle']
    if subscriber.has_mld:
        mld_args = dict()
        mld_args['handle'] = v6handle
        mld_args['version'] = subscriber.mld_version
        mld_args['filter_mode'] = subscriber.mld_filter_mode
        if subscriber.mld_iptv:
            mld_args['iptv'] = subscriber.mld_iptv
        if subscriber.mld_group_enable:
            mld_args['group_start_addr'] = subscriber.mld_mcast_group_range.start
            mld_args['group_step'] = subscriber.mld_mcast_group_range.step
            mld_args['group_count'] = subscriber.mld_mcast_group_range.count
            mld_args['group_range'] = subscriber.mld_group_range_count
            if int(subscriber.mld_group_range_count) > 1:
                mld_args['group_range_length'] = subscriber.mld_group_range_count
                if subscriber.mld_one_group_per_sub:
                    t.log('ERROR', 'does not support group range-count > 1 and one-group-per-sub at the same time')
            elif subscriber.mld_one_group_per_sub:
                mld_args['group_count'] = '1'
                mld_args['group_range_length'] = subscriber.mld_mcast_group_range.count
                mld_args['group_range_step'] = subscriber.mld_mcast_group_range.step

        if subscriber.mld_source_enable:
            mld_args['src_grp_start_addr'] = subscriber.mld_mcast_source_range.start
            mld_args['src_grp_step'] = subscriber.mld_mcast_source_range.step
            mld_args['src_grp_count'] = subscriber.mld_mcast_source_range.count
            mld_args['src_grp_range'] = subscriber.mld_source_group_range_count
        result = tester.invoke('add_mld_client', **mld_args)
        if result['status'] != '1':
            raise BBEDeviceError('Failed to add mld client  on handle {} for sub {}'.format(v6handle, subscriber))
        subscriber.rt_mld_handle = result['mld_host_handle']
        subscriber.rt_mld_group_handle = result['mld_group_handle']
        subscriber.rt_mld_source_handle = result['mld_source_handle']


def create_rt_l2bsa_subscribers(rt_device_id, subscriber):
    """Create RT DHCP subscribers

    TODO: support GRE attributes

    :param rt_device_id: RT device id such as 'rt0'
    :param subscriber: jnpr.toby.bbe.bbevar.subscribers.L2BSASubscribers instance
    :return: None
    May raise BBEDeviceError.
    """
    tester = t.get_handle(rt_device_id)
    l2bsa_args = dict()
    l2bsa_args['port'] = subscriber.rt_port
    l2bsa_args['count'] = subscriber.count
    if int(subscriber.count) < 1:
        t.log('rt emulation for this l2bsa sub {} is not created since the session is 0'.format(subscriber.tag))
        return
    if subscriber.vlan_range:
        l2bsa_args['vlan_start'] = subscriber.vlan_range.start
        l2bsa_args['vlan_step'] = subscriber.vlan_range.step
        l2bsa_args['vlan_repeat'] = subscriber.vlan_range.repeat
        l2bsa_args['vlan_length'] = subscriber.vlan_range.length
        if hasattr(subscriber, 'vlan_tpid'):
            l2bsa_args['vlan_tpid'] = subscriber.vlan_tpid
    if subscriber.svlan_range:
        l2bsa_args['svlan_start'] = subscriber.svlan_range.start
        l2bsa_args['svlan_step'] = subscriber.svlan_range.step
        l2bsa_args['svlan_repeat'] = subscriber.svlan_range.repeat
        l2bsa_args['svlan_length'] = subscriber.svlan_range.length
        if hasattr(subscriber, 'svlan_tpid'):
            l2bsa_args['svlan_tpid'] = subscriber.svlan_tpid
    if subscriber.ip_addr:
        v4_addr = ipaddress.IPv4Interface(subscriber.ip_addr)
        l2bsa_args['ip_addr'] = str(v4_addr.ip)
        l2bsa_args['netmask'] = str(v4_addr.netmask)
        if subscriber.ip_addr_step:
            l2bsa_args['ip_addr_step'] = subscriber.ip_addr_step
        if subscriber.gateway:
            l2bsa_args['gateway'] = subscriber.gateway
        if subscriber.gateway_step:
            l2bsa_args['gateway_step'] = subscriber.gateway_step
        if subscriber.mac_resolve:
            l2bsa_args['mac_resolve'] = subscriber.mac_resolve

    if subscriber.ipv6_addr:
        v6_addr = ipaddress.IPv6Interface(subscriber.ipv6_addr)
        l2bsa_args['ipv6_addr'] = str(v6_addr.ip)
        l2bsa_args['ipv6_prefix_length'] = str(v6_addr._prefixlen)
        if subscriber.ipv6_addr_step:
            l2bsa_args['ipv6_addr_step'] = subscriber.ipv6_addr_step
        if subscriber.ipv6_gateway:
            l2bsa_args['ipv6_gateway'] = subscriber.ipv6_gateway
        if subscriber.ipv6_gateway_step:
            l2bsa_args['ipv6_gateway_step'] = subscriber.ipv6_gateway_step
        if subscriber.mac_resolve:
            l2bsa_args['mac_resolve'] = subscriber.mac_resolve

    result = tester.invoke('add_link', **l2bsa_args)
    if result['status'] == '0':
        raise BBEDeviceError('Failed to add l2bsa subscriber {} {}'.format(subscriber.tag, subscriber.rt_device_id))

    subscriber.rt_device_group_handle = result.get('device_group_handle', None)
    subscriber.rt_ethernet_handle = result.get('ethernet_handle', None)
    subscriber.rt_ipv4_handle = result.get('ipv4_handle', None)
    subscriber.rt_ipv6_handle = result.get('ipv6_handle', None)

    t.log('{} Added {} l2BSA subscriber {}'.format(__LOGTAG, rt_device_id, subscriber))


def add_rt_ae(rt_device_id):

    """Create RT uplink interfaces

    :param rt_device_id: RT device id such as 'rt0'
    :return: None
    """
    rt_handle = t.get_handle(rt_device_id)  # rt handle
    ae_members = dict()
    links = bbe.get_interfaces(rt_device_id)
    for link in links:
        con = bbe.get_connection(rt_device_id, link.interface_id)
        if con and con.is_ae:
            ae_name = con.ae_bundle
            if ae_name not in ae_members:
                ae_members[ae_name] = dict()
            if con.is_ae_active:
                if 'active' not in ae_members[ae_name]:
                    ae_members[ae_name]['active'] = []
                ae_members[ae_name]['active'].append(link.interface_pic)
            else:
                if 'standby' not in ae_members[ae_name]:
                    ae_members[ae_name]['standby'] = []
                ae_members[ae_name]['standby'].append(link.interface_pic)

    for ae_name in ae_members:
        lacp_args = dict()
        lacp_args['name'] = ae_name
        if 'standby' not in ae_members[ae_name]:
            lacp_args['port_list'] = ae_members[ae_name]['active']
            result = rt_handle.invoke('add_lacp', **lacp_args)
        else:
            groups = re.match(r'ae(\d+)', ae_name)
            try:
                lacp_args['actor_system_id'] = "11:00:00:00:00:" + groups.group(1).zfill(2)
            except:
                raise Exception(" bundle name should be defined like 'ae0'")
            lacp_args['port_list'] = ae_members[ae_name]['active']
            result = rt_handle.invoke('add_lacp', **lacp_args)
            lacp_args['port_list'] = ae_members[ae_name]['standby']
            lacp_args['name'] = ae_name + "-standby"
            result2 = rt_handle.invoke('add_lacp', **lacp_args)
            result['standby_lacp_handle'] = result2['lacp_handle']
            if result['status'] == '0':
                raise BBEDeviceError('Failed to add AE for interface {}'.format(lacp_args['port_list']))
        # for link in links:
        #     con = bbe.get_connection(rt_device_id, link.interface_id)
        #     if con and con.is_ae:
        #         if con.ae_bundle == ae_name and con.is_ae_active:
        #             link.rt_lacp_handle = result['lacp_handle']
        #         if con.ae_bundle == ae_name and not con.is_ae_active:
        #             link.rt_lacp_handle = result['standby_lacp_handle']


def create_rt_hag_subscribers(rt_device_id, subscriber, test_id):
    """

    :param rt_device_id:
    :param subscriber:
    :param test_id
    :return:
    """
    #import getpass
    #loginname = getpass.getuser()
    routername = t['resources']['r0']['system']['primary']['name']
    test_session_name = routername + '_' + t._script_name + '_' + str(test_id)
    #test_session_name = loginname + '_' + t._script_name + '_' + str(test_id)
    libraryname = 'sms'
    subscriber.libname = libraryname
    tsname = t['resources']['rt0']['system']['primary']['name']
    if 'uv-ts-name' in t['resources']['rt0']['system']['primary']:
        tsname = t['resources']['rt0']['system']['primary']['uv-ts-name']
    subscriber.tsname = tsname
    tslist = [tsname]
    testcasename = t._script_name + '_' + subscriber.tag + '_' + routername
    subscriber.test_case_name = testcasename
    # Create a new Session and assign the Test Server to be used
    subscriber.test_session_name = test_session_name
    #retdict = ls.create_test_session(testSessionName=test_session_name, libraryName=libraryname, tsList=tslist)
    tester = t.get_handle(rt_device_id)
    retdict = tester.invoke('create_test_session', testSessionName=test_session_name, libraryName=libraryname, tsList=tslist, enableActs=1)
    subscriber.test_session_handle = retdict['testSessionHandle']
    subscriber.test_server_handle = retdict['testServerHandleList'][tsname]
    sutname = t['resources']['r0']['system']['primary']['name']
    sutip = subscriber.sut_loopback_ip
    sutmgmtip = t['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip']
    sutusername = 'dummy'
    sutpasswd = 'dummy'

    # Create a SUT
    #ls.sut_config(name=sutname, ip=sutip, ManagementIp=sutmgmtip, Username=sutusername, Password=sutpasswd)
    tester.invoke('sut_config', name=sutname, ip=sutip, ManagementIp=sutmgmtip, Username=sutusername, Password=sutpasswd)
    test_args = {}
    test_args['mode'] = 'create'
    test_args['IpType'] = subscriber.family
    if subscriber.family == 'dual':
        test_args['IpType'] = 'DualStack'
        test_args['DhcpHwAsCliIdEn'] = 'true'
        test_args['DhcpBroadcastEn'] = 'true'
    if int(subscriber.count) > 1:
        test_args['DhcpHwAsCliIdEn'] = 'true'
    test_args['testSessionHandle'] = retdict['testSessionHandle']
    test_args['tsName'] = tsname
    test_args['testCaseName'] = testcasename
    test_args['libraryName'] = libraryname
    test_args['TestActivity'] = subscriber.test_activity
    test_args['EnableExternalData'] = subscriber.external_data
    test_args['TunnelType'] = subscriber.tunnel_type
    test_args['GreL3ProtocolType'] = 1
    test_args['HybridAccessEn'] = 'true'
    test_args['NumMs'] = subscriber.count
    test_args['MacAddr'] = subscriber.mac
    #test_args['NumLinksOrNodes'] = subscriber.lte_node_count
    test_args['NumLinksOrNodes'] = subscriber.count
    test_args['HgStartRate'] = subscriber.lte_activation_rate
    test_args['HgDisconnectRate'] = subscriber.lte_deactivation_rate
    test_args['HgClientId'] = subscriber.hag_client_id
    test_args['HgBypassTrafRate'] = subscriber.hag_bypass_rate
    test_args['HgTerminalHostPrefix'] = subscriber.hag_ipv6_prefix_th
    test_args['HgHaapPrefix'] = subscriber.hag_ipv6_prefix_haap
    test_args['HgLtePktDist'] = subscriber.hag_lte_pkt_distribution
    test_args['HgLteSetupReqTimeout'] = subscriber.hag_lte_request_timeout
    test_args['HgLteNoAnswerRetries'] = subscriber.hag_lte_no_answer_retry
    test_args['HgLteSetupDenyRetries'] = subscriber.hag_lte_setup_deny_retry
    test_args['HgLteSetupRetryInterval'] = subscriber.hag_lte_setup_retry_interval
    test_args['HgDslPktDist'] = subscriber.hag_dsl_pkt_distribution
    test_args['HgDslSetupReqTimeout'] = subscriber.hag_dsl_request_timeout
    test_args['HgDslNoAnswerRetries'] = subscriber.hag_dsl_no_answer_retry
    test_args['HgDslSetupDenyRetries'] = subscriber.hag_dsl_setup_deny_retry
    test_args['HgDslSetupRetryInterval'] = subscriber.hag_dsl_setup_retry_interval
    test_args['HgDslSyncRateEn'] = subscriber.hag_dsl_sync_enable
    test_args['HgDslSyncRate'] = subscriber.hag_dsl_sync_rate
    test_args['GreKeyEn'] = 'false'
    test_args['GreChksumEn'] = 'false'
    test_args['DhcpCliId'] = subscriber.dhcp_client_id
    test_args['DhcpLeaseTimeEn'] = "true"
    test_args['DhcpLeaseTime'] = 300
    test_args['DhcpRetries'] = subscriber.dhcp_retries
    test_args['DhcpOfferTime'] = 15
    test_args['DhcpAckTime'] = 15
    test_args['DhcpIaOpt6Type'] = subscriber.dhcp_v6_ia_type

    access_obj = bbe.get_interfaces('rt0', interfaces='access')[0]
    subscriber.access_interface = access_obj.interface_pic
    test_args['HgLteNodePhy'] = access_obj.interface_pic
    if '/' in subscriber.lte_node_ip:
        ltev4addr = ipaddress.IPv4Interface(subscriber.lte_node_ip)
        access_addr = str(ltev4addr.ip)
        access_mask = str(ltev4addr.netmask)
        test_args['HgLteNodeIp'] = access_addr
    else:
        test_args['HgLteNodeIp'] = subscriber.lte_node_ip
        access_mask = "255.0.0.0"
    test_args['HgLteNextHop'] = subscriber.lte_node_nexthop
    test_args['HgDslNodePhy'] = access_obj.interface_pic
    if '/' in subscriber.dsl_node_ip:
        dslv4addr = ipaddress.IPv4Interface(subscriber.dsl_node_ip)
        test_args['HgDslNodeIp'] = str(dslv4addr.ip)
    else:
        test_args['HgDslNodeIp'] = subscriber.dsl_node_ip
    test_args['HgDslNextHop'] = subscriber.lte_node_nexthop
    test_args['SutHaapSut'] = sutname
    # Reserve Ports
    uplink_obj = bbe.get_interfaces('rt0', interfaces='uplink')[0]
    uplink_addr = None
    netmask = None
    if uplink_obj:
        subscriber.uplink_interface = uplink_obj.interface_pic
        port_list = [access_obj.interface_pic, uplink_obj.interface_pic]
        if hasattr(subscriber, 'traffic_start_ip'):
            if '/' in subscriber.traffic_start_ip:
                v4addr = ipaddress.IPv4Interface(subscriber.traffic_start_ip)
                uplink_addr = str(v4addr.ip)
                netmask = str(v4addr.netmask)
            else:
                uplink_addr = subscriber.traffic_start_ip
                netmask = "255.255.255.0"
        else:
            uplink_addr = '20.20.20.2'
            netmask = "255.255.255.0"
    addr_list = [test_args['HgLteNodeIp']]
    mask_list = [access_mask]
    if uplink_addr:
        addr_list.append(uplink_addr)
        mask_list.append(netmask)

    ## Reserve ports
    if subscriber.traffic and subscriber.traffic_dualstack:
        port_list.append(uplink_obj.interface_pic + 'v6')

        if hasattr(subscriber, 'v6_traffic_start_ip'):
            if '/' in subscriber.v6_traffic_start_ip:
                v6addr = ipaddress.IPv6Interface(subscriber.v6_traffic_start_ip)
                v6_uplink_addr = str(v6addr.ip)
                v6_mask = '/' + str(v6addr._prefixlen)
            else:
                v6_uplink_addr = subscriber.v6_traffic_start_ip
                v6_mask = '/64'
        else:
            v6_uplink_addr = '2000::2'
            v6_mask = "/64"
        addr_list.append(v6_uplink_addr)
        mask_list.append(v6_mask)
        t.log("port_list is {}, addr_list is {}".format(port_list, addr_list))

        response = tester.invoke('reserve_ports', testSessionHandle=retdict['testSessionHandle'], portList=port_list,
                             ipAddressList=addr_list, tsName=tsname, type='ip', numAddressList=['150000', '50', '50'],
                             ipMaskList=mask_list)
        t.log("reserve ports {}, the response is {}".format(port_list, response))
    else:
        response = tester.invoke('reserve_ports', testSessionHandle=retdict['testSessionHandle'], portList=port_list,
                             ipAddressList=addr_list, tsName=tsname, type='ip', numAddressList=['150000', '50'],
                             ipMaskList=mask_list)
        t.log("reserve ports {}, the response is {}".format(port_list, response))
    if hasattr(subscriber, 'has_li') and subscriber.has_li:
        custom_obj = bbe.get_interfaces('rt0', interfaces='custom')[0]
        subscriber.custom_interface = custom_obj.interface_pic
        custom_port = [subscriber.custom_interface]
        if '/' in subscriber.li_ipaddr:
            liv4addr = ipaddress.IPv4Interface(subscriber.li_ipaddr)
            custom_addr = str(liv4addr.ip)
            custom_netmask = str(liv4addr.netmask)
        else:
            custom_addr = subscriber.li_ipaddr
            custom_netmask = "255.255.255.0"
        gateway_ip = subscriber.li_gateway
        #reserve custom port
        response = tester.invoke('reserve_ports', testSessionHandle=retdict['testSessionHandle'], portList=custom_port,
                             ipAddressList=[custom_addr], tsName=tsname, type='ip', numAddressList=['253'],
                             ipMaskList=[custom_netmask])
    dmf_lib_list = []
    dmf_name_list = []
    subscriber.dmf_handle = {}
    if subscriber.traffic:
        test_args['DataTraffic'] = "Continuous"
        test_args['TrafficMtu'] = subscriber.traffic_mtu
        test_args['NetworkHost'] = subscriber.traffic_network_host_type

        if test_args['NetworkHost'] == 'local':
            test_args['NetworkHostPhy'] = uplink_obj.interface_pic
            test_args['NetworkHostStartingIp'] = uplink_addr
            test_args['NetworkHostNumOfNodes'] = subscriber.traffic_node_count
            test_args['NetworkNextHop'] = subscriber.traffic_gateway
            if subscriber.family.lower() == 'ipv6':
                test_args['NetworkHostPhyIpv6'] = uplink_obj.interface_pic + 'v6'
                test_args['NetworkHostStartingIpv6'] = v6_uplink_addr
                test_args['NetworkHostNumOfNodes'] = subscriber.v6_traffic_node_count
                test_args['NetworkNextHopIpv6'] = subscriber.v6_traffic_gateway
            if subscriber.traffic_dualstack:
                test_args['NetworkHost'] = 'dualstack'
                test_args['NetworkHostPhyIpv6'] = uplink_obj.interface_pic + 'v6'
                test_args['NetworkHostStartingIpv6'] = v6_uplink_addr
                test_args['NetworkHostNumOfNodesIpv6'] = subscriber.v6_traffic_node_count
                test_args['NetworkNextHopIpv6'] = subscriber.v6_traffic_gateway

        if test_args['NetworkHost'] == 'remote':
            test_args['NetworkHostAddrRemoteList'] = [uplink_addr]
        if subscriber.traffic_vlan_enable:
            test_args['NetworkHostVlanId'] = subscriber.traffic_vlan_id
            if subscriber.traffic_dualstack:
                test_args['NetworkHostVlanIdIpv6'] = subscriber.traffic_vlan_id
            if hasattr(subscriber, 'traffic_svlan_id'):
                test_args['NetworkHostVlanId'] = subscriber.traffic_svlan_id
                test_args['NetworkHostInnerVlanId'] = subscriber.traffic_vlan_id
                if subscriber.traffic_dualstack:
                    test_args['NetworkHostVlanIdIpv6'] = subscriber.traffic_svlan_id
                    test_args['NetworkHostInnerVlanIdIpv6'] = subscriber.traffic_vlan_id
        dmf_role_list = []
        dmf_transport_list = []
        for name in subscriber.traffic_profile:
            dmf_args = {}
            dmf_args['dmfName'] = t._script_name + "_" + name
            dmf_args['mode'] = 'create'
            dmf_args['DataProtocol'] = subscriber.traffic_profile[name]['type']
            dmf_args['TransactionRate'] = subscriber.traffic_profile[name]['rate']
            dmf_args['TotalTransactions'] = subscriber.traffic_profile[name]['transaction']
            if subscriber.traffic_profile[name]['start'] == "paused":
                dmf_args['StartPaused'] = 'true'
            if subscriber.traffic_profile[name]['start'] == "on-event":
                dmf_args['StartOnEvent'] = 'true'
            dmf_args['PacketSize'] = subscriber.traffic_profile[name]['packet_size']
            dmf_args['libraryName'] = 'sms/spirentEval'
            dmf_args['TimeToLive'] = subscriber.traffic_profile[name]['ttl']
            dmf_args['SegmentSize'] = subscriber.traffic_profile[name]['segment_size']
            #dmf_args['InitiatingSide'] = subscriber.traffic_profile[name]['initiate_side']
            dmf_args['HostDataExpansionRatio'] = subscriber.traffic_profile[name]['ratio']
            dmf_args['InitiatingSide'] = subscriber.traffic_profile[name]['role']
            if dmf_args['DataProtocol'] == 'udp':
                if 'udp_burst_count' in subscriber.traffic_profile[name]:
                    dmf_args['BurstCount'] = subscriber.traffic_profile[name]['udp_burst_count']
            if dmf_args['DataProtocol'] == 'tcp':
                if 'tcp_socket_disc_side' in subscriber.traffic_profile[name]:
                    dmf_args['DisconnectSide'] = subscriber.traffic_profile[name]['tcp_socket_disc_side']
                if 'tcp_3way_handshake' in subscriber.traffic_profile[name]:
                    dmf_args['Force3Way'] = subscriber.traffic_profile[name]['tcp_3way_handshake']
                if 'tcp_disconnect_type' in subscriber.traffic_profile[name]:
                    dmf_args['DisconnectType'] = subscriber.traffic_profile[name]['tcp_disconnect_type']
                if 'tcp_congestion_avoid' in subscriber.traffic_profile[name]:
                    dmf_args['SlowStart'] = subscriber.traffic_profile[name]['tcp_congestion_avoid']
                if 'tcp_window_size' in subscriber.traffic_profile[name]:
                    dmf_args['WindowSize'] = subscriber.traffic_profile[name]['tcp_window_size']
                if 'tcp_max_segment_size' in subscriber.traffic_profile[name]:
                    dmf_args['MaxSegmentSize'] = subscriber.traffic_profile[name]['tcp_max_segment_size']
                if 'tcp_min_header_size' in subscriber.traffic_profile[name]:
                    dmf_args['MinTcpHeaderSize'] = subscriber.traffic_profile[name]['tcp_min_header_size']
                if 'tcp_max_packets_before_ack' in subscriber.traffic_profile[name]:
                    dmf_args['MaxPacketsToForceAck'] = subscriber.traffic_profile[name]['tcp_max_packets_before_ack']

            if 'tos' in subscriber.traffic_profile[name]:
                tos_list = subscriber.traffic_profile[name]['tos']
                for index in range(len(tos_list)):
                    dmf_name = t._script_name + "_" + name + str(index)
                    dmf_args['dmfName'] = dmf_name
                    if 'client_port' in subscriber.traffic_profile[name]:
                        dmf_args['ClientPort'] = int(subscriber.traffic_profile[name]['client_port']) + index
                    if 'server_port' in subscriber.traffic_profile[name]:
                        dmf_args['ServerPort'] = int(subscriber.traffic_profile[name]['server_port']) + index
                    dmf_args['TypeOfService'] = tos_list[index]

                    # subscriber.dmf_handle[dmf_name] = ls.config_dmf(**dmf_args)
                    subscriber.dmf_handle[dmf_name] = tester.invoke('config_dmf', **dmf_args)
                    t.log("created dmf stream {} with args {}".format(dmf_name, dmf_args))
                    dmf_lib_list.append('sms/spirentEval')
                    dmf_name_list.append(dmf_name)
                    dmf_role_list.append(subscriber.traffic_profile[name]['role'])
                    dmf_transport_list.append(subscriber.traffic_profile[name]['preferred_transport'])
            else:
                dmf_name = dmf_args['dmfName']
                # subscriber.dmf_handle[dmf_name] = ls.config_dmf(**dmf_args)
                subscriber.dmf_handle[dmf_name] = tester.invoke('config_dmf', **dmf_args)
                t.log("created dmf stream {} with args {}".format(dmf_name, dmf_args))
                dmf_lib_list.append('sms/spirentEval')
                dmf_name_list.append(dmf_name)
                dmf_role_list.append(subscriber.traffic_profile[name]['role'])
                dmf_transport_list.append(subscriber.traffic_profile[name]['preferred_transport'])

    #test_args['EnableExternalData'] = 0
        if dmf_role_list:
            test_args['nodeRoleList'] = dmf_role_list
        if dmf_transport_list:
            test_args['preferredTransportList'] = dmf_transport_list
    if dmf_lib_list:
        test_args['dmfLibraryList'] = dmf_lib_list
    if dmf_name_list:
        test_args['dmfList'] = dmf_name_list
    print("test_args is {}".format(test_args))
    # testcase_handle = ls.wifi_offload_gateway_nodal_testcase(**test_args)
    testcase_handle = tester.invoke('wifi_offload_gateway_nodal_testcase', **test_args)
    t.log("testcase {} is created with handle {}".format(testcasename, testcase_handle))
    subscriber.testcase_handle = testcase_handle
    if hasattr(subscriber, 'has_li') and subscriber.has_li:
        ###create a dummy dmf for it
        # Create a DMF - Data Message Flow for Data traffic

        dmfName = t._script_name + "_" + subscriber.tag + '_dummy'
        tester.invoke('config_dmf', mode='create', libraryName='sms/spirentEval', dmfName=dmfName, DataProtocol='raw',
                      TransactionRate=100, PacketSize=64, HostDataExpansionRatio=0)

        # Network Host Testcase
        testCaseName = t._script_name + "_" + subscriber.tag + '_li'
        testArgs = dict()
        testArgs['mode'] = 'create'
        testArgs['testSessionHandle'] = retdict['testSessionHandle']
        testArgs['tsName'] = tsname
        testArgs['testCaseName'] = testCaseName
        testArgs['libraryName'] = 'sms/spirentEval'
        testArgs['NetworkHostPhy'] = custom_port
        testArgs['NetworkHostIp'] = custom_addr
        testArgs['NumLinksOrNodes'] = 1
        testArgs['NetworkHostNextHop'] = subscriber.li_gateway
        testArgs['NumIpAddr'] = 1
        testArgs['DataTraffic'] = 'Continuous'
        testArgs['TrafficMtu'] = 1400
        testArgs['dmfLibraryList'] = [libraryname]
        testArgs['dmfList'] = [dmfName]
        # testArgs['DualStackEn'] = 'false'
        # testArgs['NetworkHostPhyIpv6'] = 'eth11v6'
        # testArgs['NetworkHostIpv6'] = "1000::3"
        # testArgs['NetworkNextHopIpv6'] = "1000::1"

        subscriber.li_testcase = tester.invoke('network_host_testcase', **testArgs)

        # Validate the test session
        validationStatus = tester.invoke('validate_test_configuration', testSessionHandle=retdict['testSessionHandle'])
        print("Validation Status: ", validationStatus)

        # Save the testcase
        tester.invoke('save_config', instance=subscriber.li_testcase, overwrite=1)


    t.log("Validate the test session {}".format(subscriber.test_session_name))
    #validation_status = ls.validate_test_configuration(testSessionHandle=subscriber.test_session_handle)
    validation_status = tester.invoke('validate_test_configuration', testSessionHandle=subscriber.test_session_handle)
    t.log("Validation Status: {}".format(validation_status))

    # ls.save_config(instance=testcase_handle, overwrite=1)
    # t.log("Save the testcase {}".format(testcasename))
    #ls.save_config(instance=subscriber.test_session_handle, overwrite=1)
    tester.invoke('save_config', instance=subscriber.test_session_handle, overwrite=1)
    t.log("Save the test session {}".format(subscriber.test_session_name))


def create_rt_cups_subscribers(rt_device_id, subscriber, test_id):
    """

    :param rt_device_id:
    :param subscriber:
    :param test_id
    :return:
    """
    import getpass
    loginname = getpass.getuser()
    test_session_name = loginname + '_' + t._script_name + '_' + str(test_id)
    libraryname = 'sms'
    subscriber.libname = libraryname
    tsname = t['resources'][rt_device_id]['system']['primary']['name']
    if 'uv-ts-name' in t['resources'][rt_device_id]['system']['primary']:
        tsname = t['resources'][rt_device_id]['system']['primary']['uv-ts-name']
    subscriber.tsname = tsname
    tslist = [tsname]
    nodal_testcasename = t._script_name + '_nodal_' + subscriber.tag
    subscriber.nodal_test_case_name = nodal_testcasename
    # Create a new Session and assign the Test Server to be used
    subscriber.test_session_name = test_session_name
    tester = t.get_handle(rt_device_id)
    retdict = tester.invoke('create_test_session', testSessionName=test_session_name, libraryName=libraryname,
                            tsList=tslist, enableActs=1)
    subscriber.test_session_handle = retdict['testSessionHandle']
    subscriber.test_server_handle = retdict['testServerHandleList'][tsname]
    sutname = t['resources']['r0']['system']['primary']['name']
    sutmgmtip = t['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip']
    sutusername = 'dummy'
    sutpasswd = 'dummy'

    # Create a SUT for the router, not needed in cups, since the subscriber.sgw_user_address
    sutips = []
    sutips.append(subscriber.sgw_control_address)
    sutips.append(subscriber.sgw_user_address)        # DUT local address for access-network-peers
    sutips.append(subscriber.pgw_address)
    sutips.append(subscriber.sxa_sxb_to_up_user_node) # DUT local address for control-network-peers
    if hasattr(subscriber, "sgw_v6_control_address"):
        sutips.append(subscriber.sgw_v6_control_address)
    if hasattr(subscriber, "sgw_v6_user_address"):
        sutips.append(subscriber.sgw_v6_user_address)
    if hasattr(subscriber, "pgw_v6_address"):
        sutips.append(subscriber.pgw_v6_address)
    if hasattr(subscriber, "sxa_sxb_to_up_v6_user_node"):
        sutips.append(subscriber.sxa_sxb_to_up_v6_user_node)
    for addr in sutips:
        tester.invoke('sut_config', name=addr, ip=addr, ManagementIp=addr, Username=sutusername, Password=sutpasswd)

    # Get Access address details
    sgwv4addr = ipaddress.IPv4Interface(subscriber.user_base_address)
    access_addr = str(sgwv4addr.ip)
    access_mask = str(sgwv4addr.netmask)
    num_access_address = sgwv4addr.network.num_addresses - 2
    num_access_address = str(num_access_address)

    # Get Control address details
    sx_v4addr = ipaddress.IPv4Interface(subscriber.control_base_address)
    control_addr = str(sx_v4addr.ip)
    control_mask = str(sx_v4addr.netmask)
    num_control_address = sx_v4addr.network.num_addresses - 2
    num_control_address = str(num_control_address)

    # Get Uplink v4 address details
    uplink_v4addr = ipaddress.IPv4Interface(subscriber.uplink_base_address)
    uplink_addr = str(uplink_v4addr.ip)
    # if '/' in str(uplink_v4addr):
    uplink_mask = str(uplink_v4addr.netmask)
    num_uplink_address = uplink_v4addr.network.num_addresses - 2
    num_uplink_address = str(num_uplink_address)

    # Check whether accessX and controlX are consolidated to a single port
    if subscriber.control_interface != subscriber.access_interface:
        # Control and Access do NOT share a port
        port_list = [subscriber.access_interface, subscriber.uplink_interface, subscriber.control_interface]
        addr_list = [access_addr, uplink_addr, control_addr]
        mask_list = [access_mask, uplink_mask, control_mask]
        num_address_per_port_list = [num_access_address, num_uplink_address, num_control_address]
    else:
        # Control and Access share a port and network
        subscriber.sxa_sxb_to_up_user_node = subscriber.sgw_user_address  # Same target address if sharing port
        port_list = [subscriber.access_interface, subscriber.uplink_interface]
        addr_list = [access_addr, uplink_addr]
        mask_list = [access_mask, uplink_mask]
        num_address_per_port_list = [num_access_address, num_uplink_address]

    if hasattr(subscriber, 'uplink_v6_base_address'):
        uplink_v6 = ipaddress.IPv6Interface(subscriber.uplink_v6_base_address)
        # We want to increase the end of the uplink_v6_base_address by 1 because landslide doesn't accept it otherwise
        uplink_v6addr = str(uplink_v6.ip + 1)
        uplink_v6_mask = str(uplink_v6.netmask)
        # Landslide cannot allocate very large v6 networks
        num_uplink_v6_address = min(4000, uplink_v6.network.num_addresses - 2)
        num_uplink_v6_address = str(num_uplink_v6_address)
        # Append reserve_ports lists
        port_list.append(subscriber.uplink_v6_interface)
        addr_list.append(uplink_v6addr)
        mask_list.append(uplink_v6_mask)
        num_address_per_port_list.append(num_uplink_v6_address)
    if hasattr(subscriber, 'user_v6_base_address'):
        access_v6 = ipaddress.IPv6Interface(subscriber.user_v6_base_address)
        # We want to increase the end of the access_v6_base_address by 1 because landslide doesn't accept it otherwise
        access_v6addr = str(access_v6.ip + 1)
        access_v6_mask = str(access_v6.netmask)
        # Landslide cannot allocate very large v6 networks
        num_access_v6_address = min(4000, access_v6.network.num_addresses - 2)
        num_access_v6_address = str(num_access_v6_address)
        # Append reserve_ports lists
        port_list.append(subscriber.access_v6_interface)
        addr_list.append(access_v6addr)
        mask_list.append(access_v6_mask)
        num_address_per_port_list.append(num_access_v6_address)
    # If the control interface == the access interface, we don't want to duplicate ports, so we don't add control
    if (hasattr(subscriber, 'control_v6_base_address') and
            not(hasattr(subscriber, 'user_v6_base_address') and subscriber.control_v6_interface == subscriber.access_v6_interface)):
        control_v6 = ipaddress.IPv6Interface(subscriber.control_v6_base_address)
        # We want to increase the end of the control_v6_base_address by 1 because landslide doesn't accept it otherwise
        control_v6addr = str(control_v6.ip + 1)
        control_v6_mask = str(control_v6.netmask)
        # Landslide cannot allocate very large v6 networks
        num_control_v6_address = min(4000, control_v6.network.num_addresses - 2)
        num_control_v6_address = str(num_control_v6_address)
        # Append reserve_ports lists
        port_list.append(subscriber.control_v6_interface)
        addr_list.append(control_v6addr)
        mask_list.append(control_v6_mask)
        num_address_per_port_list.append(num_control_v6_address)

    ## Reserve ports
    t.log("port_list is {}, addr_list is {}, mask_list is {}".format(port_list, addr_list, mask_list))

    response = tester.invoke('reserve_ports', testSessionHandle=retdict['testSessionHandle'], portList=port_list,
                         ipAddressList=addr_list, tsName=tsname, type='ip', numAddressList=num_address_per_port_list,
                         ipMaskList=mask_list)
    t.log("reserve ports {}, the response is {}".format(port_list, response))

    nodal_args = {}
    nodal_args['mode'] = 'create'
    nodal_args['IpType'] = subscriber.family
    nodal_args['testSessionHandle'] = retdict['testSessionHandle']
    nodal_args['tsName'] = tsname
    nodal_args['testCaseName'] = nodal_testcasename
    nodal_args['libraryName'] = libraryname
    nodal_args['TestActivity'] = subscriber.test_activity
    nodal_args['DedicatedsPerDefaultBearer'] = subscriber.dedicated_bearers
    nodal_args['UeInitBearerEn'] = 'true'
    nodal_args['S5Protocol'] = 'GTPv2'
    nodal_args['Sessions'] = subscriber.session_count
    nodal_args['DefaultBearers'] = subscriber.bearer_per_session
    # No Dual Stack support
    nodal_args['SutSgwUserSut'] = getattr(subscriber, 'sgw_v6_user_address', subscriber.sgw_user_address)
    nodal_args['SutSgwSut'] = getattr(subscriber, 'sgw_v6_control_address', subscriber.sgw_control_address)
    # nodal_args['SutPgwV4Sut'] = getattr(subscriber, 'pgw_v6_address', subscriber.pgw_address)
    nodal_args['SutPgwV4Sut'] = getattr(subscriber, 'sgw_v6_control_address', subscriber.sgw_control_address)

    nodal_args['Gtp2Version'] = subscriber.s11_gtpv2_version
    nodal_args['Gtp2Imsi'] = subscriber.s11_start_imsi
    nodal_args['Gtp2Imei'] = subscriber.s11_start_imei
    nodal_args['Gtp2N3Attempts'] = subscriber.s11_n3_requests
    nodal_args['Gtp2T3Time'] = subscriber.s11_t3_response_time
    nodal_args['Gtp2RadioAccessType'] = subscriber.s11_radio_access_type  # eutran means 6?
    nodal_args['Gtp2GtpcTunnelEndptId'] = subscriber.s11_gtp_c_tunnel_id
    nodal_args['Gtp2GtpuTunnelEndptId'] = subscriber.s11_gtp_u_tunnel_id
    nodal_args['Gtp2GtpuIncludeSeqEn'] = "true"
    nodal_args['Gtp2UliDbCmdCbRspEn'] = "true"
    nodal_args['Gtp2ApnTotalApns_0'] = subscriber.s11_total_apns
    nodal_args['Gtp2ApnNumSpecifiedApns_0'] = 0
    nodal_args['Gtp2ApnTotalApns_1'] = subscriber.s11_total_apns
    nodal_args['Gtp2ApnNumSpecifiedApns_1'] = 0
    nodal_args['Gtp2Apn_0'] = subscriber.apn_name
    nodal_args['Gtp2AmbrDownlink'] = '10000000'
    nodal_args['Gtp2AmbrUplink'] = '10000000'
    nodal_args['PgwNodeEn'] = 'false'
    # Builtin Dual Stack support not utilized
    nodal_args['MmeControlNodePhy'] = getattr(subscriber, 'control_v6_interface', subscriber.control_interface)
    nodal_args['MmeControlNodeIp'] = getattr(subscriber, 'mme_control_node_start_ipv6', subscriber.mme_control_node_start_ip)
    nodal_args['NumLinksOrNodes'] = subscriber.mme_control_node_count
    nodal_args['NumEnbPerMMe'] = subscriber.enodeb_user_node_count
    # No Dual Stack support
    nodal_args['eNodeBUserNodePhy'] = getattr(subscriber, 'access_v6_interface', subscriber.access_interface)
    nodal_args['eNodeBUserNodeIp'] = getattr(subscriber, 'enodeb_user_node_start_ipv6', subscriber.enodeb_user_node_start_ip)
    nodal_args['TargeteNodeBUserNodePhy'] = getattr(subscriber, 'access_v6_interface', subscriber.access_interface)
    nodal_args['TargeteNodeBUserNodeIp'] = getattr(subscriber, 'target_enodeb_user_node_v6', subscriber.target_enodeb_user_node)

    # Multiple CPF
    if int(subscriber.sgw_control_node_count) > 1:
        nodal_args['SgwNumSutsEn'] = 'true'
        nodal_args['SgwNumSuts'] = subscriber.sgw_control_node_count

    if subscriber.use_loopback_access:
        # No Dual Stack support
        nodal_args['eNodeBUserNodeNextHop'] = getattr(subscriber, 'v6_access_gateway', subscriber.access_gateway)
    if hasattr(subscriber, 'access_vlan_id'):
        nodal_args['eNodeBUserNodeVlanId'] = subscriber.access_vlan_id

    if subscriber.use_static_address:
        nodal_args['UseStaticBearerIp'] = 'true'
        nodal_args['BearerAddrPool'] = subscriber.bearer_ipv6_addr_pool
        nodal_args['BearerV4AddrPool'] = subscriber.bearer_ipv4_addr_pool

    nodal_args['HomeAddrType'] = subscriber.home_address_type

    subscriber.dmf_handle = {}

    ### Create SGW Nodal testcase
    print("nodal_args is {}".format(nodal_args))
    nodal_testcase_handle = tester.invoke('sgw_nodal_testcase', **nodal_args)
    t.log("nodal testcase {} is created with handle {}".format(nodal_testcasename, nodal_testcase_handle))
    subscriber.nodal_testcase_handle = nodal_testcase_handle

    # SGW Node Testcase
    testCaseName = 'node'
    node_testcasename = t._script_name + '_node_' + subscriber.tag
    subscriber.node_test_case_name = node_testcasename
    node_args = dict()
    node_args['mode'] = 'create'
    node_args['testSessionHandle'] = retdict['testSessionHandle']
    node_args['tsName'] = tsname
    node_args['testCaseName'] = node_testcasename
    node_args['libraryName'] = libraryname

    node_args['S5Protocol'] = 'GTPv2'
    node_args['SxaToSgwUEn'] = 'true'
    node_args['UeInitBearerEn'] = 'true'
    node_args['PgwNodeEn'] = 'true'
    node_args['TrafficMtu'] = subscriber.data_mtu
    node_args['Sessions'] = subscriber.session_count
    node_args['DefaultBearers'] = subscriber.bearer_per_session
    node_args['DedicatedsPerDefaultBearer'] = subscriber.dedicated_bearers
    node_args['ConnectBearerDelayList'] = [5, 10, ]
    # node_args['tftSettings'] = tft_settings
    # No Dual Stack support
    node_args['SutSxaGtpuSut'] = getattr(subscriber, 'sxa_sxb_to_up_v6_user_node', subscriber.sxa_sxb_to_up_user_node)
    node_args['SutSxaUserSut'] = getattr(subscriber, 'sxa_sxb_to_up_v6_user_node', subscriber.sxa_sxb_to_up_user_node)
    # node_args['SutSxaUPSut'] = getattr(subscriber, 'sxa_sxb_to_up_v6_user_node', subscriber.sxa_sxb_to_up_user_node)
    node_args['SutSxaUPSut'] = getattr(subscriber, 'sgw_v6_user_address', subscriber.sgw_user_address)

    # No Dual Stack support
    node_args['SgwControlNodePhy'] = getattr(subscriber, 'control_v6_interface', subscriber.control_interface)
    node_args['SgwControlNodeIp'] = getattr(subscriber, 'sgw_control_node_start_ipv6',
        subscriber.sgw_control_node_start_ip)
    node_args['SxaControlNodePhy'] = getattr(subscriber, 'control_v6_interface', subscriber.control_interface)
    node_args['SxaControlNodeIp'] = getattr(subscriber, 'sxa_sxb_control_node_start_ipv6',
        subscriber.sxa_sxb_control_node_start_ip)
    # node_args['SxaControlNodeNextHop'] = '100.0.0.1'  # temp
    node_args['SxaControlGtpUNodePhy'] = getattr(subscriber, 'control_v6_interface', subscriber.control_interface)
    node_args['SxaControlGtpUNodeIp'] = getattr(subscriber, 'sxa_sxb_control_gtp_node_start_ipv6', subscriber.sxa_sxb_control_gtp_node_start_ip)
    node_args['NumLinksOrNodes'] = subscriber.sgw_control_node_count

    if subscriber.use_loopback_control:
        # No Dual Stack support
        node_args['SxaControlNodeNextHop'] = getattr(subscriber, 'v6_control_gateway', subscriber.control_gateway)
    if hasattr(subscriber, 'control_vlan_id'):
        node_args['SxaControlNodeVlanId'] = subscriber.control_vlan_id

    node_args['Gtp2Version '] = subscriber.node_gtpv2_version
    node_args['Gtp2Imsi'] = subscriber.node_start_imsi
    node_args['Gtp2Imei'] = subscriber.node_start_imei
    node_args['Gtp2N3Attempts'] = subscriber.s11_n3_requests
    node_args['Gtp2T3Time'] = subscriber.s11_t3_response_time
    node_args['Gtp2RadioAccessType'] = subscriber.node_radio_access_type;  #
    node_args['Gtp2GtpcTunnelEndptId'] = subscriber.node_gtp_c_tunnel_id
    node_args['Gtp2GtpuTunnelEndptId'] = subscriber.node_gtp_u_tunnel_id

    node_args['Gtp2GtpuIncludeSeqEn'] = "true"
    node_args['Gtp2PersistentImsiEn'] = "false"
    node_args['Gtp2S5GtpcTunnelEndptId'] = subscriber.node_start_s5_gtp_c_teid
    node_args['Gtp2S5GtpuTunnelEndptId'] = subscriber.node_start_s5_gtp_u_teid
    node_args['Gtp2MobGtpuForwardingEndptId'] = subscriber.node_start_fwd_gtp_u_teid
    node_args['Gtp2ApnTotalApns_0'] = subscriber.node_total_apns
    node_args['Gtp2Apn_0'] = subscriber.apn_name
    node_args['Gtp2ApnNumSpecifiedApns_0'] = 0
    node_args['Gtp2AmbrDownlink'] = '10000000'
    node_args['Gtp2AmbrUplink'] = '10000000'
    node_args['BearerAddrPool'] = subscriber.bearer_ipv6_addr_pool
    node_args['BearerV4AddrPool'] = subscriber.bearer_ipv4_addr_pool
    node_args['SxaControlSpecVer'] = '3'    # PFCP v14.5.0
    node_args['SxaControlUserInitEn'] = str(subscriber.user_initiated_association).lower()
    node_args['SxaControlNodeHeartbeatRetries'] = subscriber.heartbeat_retries
    node_args['SxaControlNodeHeartbeatInterval'] = subscriber.heartbeat_interval
    node_args['SxaControlNodeRetries'] = subscriber.sx_node_retries
    node_args['SxaControlNodeRetryInterval'] = subscriber.sx_node_retry_interval
    node_args['SxaControlSessionRetries'] = subscriber.sx_session_retries
    node_args['SxaControlSessionRetryInterval'] = subscriber.sx_session_retry_interval

    print("node_args is {}".format(node_args))
    node_testcasehandle = tester.invoke('sgw_node_testcase', **node_args)
    t.log("node testcase {} is created with handle {}".format(node_testcasename, node_testcasehandle))
    subscriber.node_testcase_handle = node_testcasehandle
    t.log("Validate the test session {}".format(subscriber.test_session_name))
    validation_status = tester.invoke('validate_test_configuration', testSessionHandle=subscriber.test_session_handle)
    t.log("Validation Status: {}".format(validation_status))
    tester.invoke('save_config', instance=subscriber.test_session_handle, overwrite=1)
    t.log("Save the test session {}".format(subscriber.test_session_name))
    subscriber.action(action='automation_control')


def create_rt_pgw_subscribers(rt_device_id, subscriber, test_id):
    """

    :param rt_device_id:
    :param subscriber:
    :param test_id
    :return:
    """
    import getpass
    loginname = getpass.getuser()
    test_session_name = loginname + '_' + t._script_name + '_' + str(test_id)
    libraryname = 'sms'
    subscriber.libname = libraryname
    tsname = t['resources'][rt_device_id]['system']['primary']['name']
    if 'uv-ts-name' in t['resources'][rt_device_id]['system']['primary']:
        tsname = t['resources'][rt_device_id]['system']['primary']['uv-ts-name']
    subscriber.tsname = tsname
    tslist = [tsname]
    nodal_testcasename = t._script_name + '_nodal_' + subscriber.tag
    subscriber.nodal_test_case_name = nodal_testcasename
    # Create a new Session and assign the Test Server to be used
    subscriber.test_session_name = test_session_name
    tester = t.get_handle(rt_device_id)
    retdict = tester.invoke('create_test_session', testSessionName=test_session_name, libraryName=libraryname,
                            tsList=tslist)
    subscriber.test_session_handle = retdict['testSessionHandle']
    subscriber.test_server_handle = retdict['testServerHandleList'][tsname]
    sutname = t['resources']['r0']['system']['primary']['name']
    sutmgmtip = t['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip']
    sutusername = 'dummy'
    sutpasswd = 'dummy'

    # Create a SUT for the router, not needed in cups, since the subscriber.pgw_user_address
    sutips = []
    sutips.append(subscriber.pgw_control_address)
    sutips.append(subscriber.pgw_user_address)        # DUT local address for access-network-peers
    sutips.append(subscriber.sxb_to_up_user_node) # DUT local address for control-network-peers
    if hasattr(subscriber, "pgw_v6_control_address"):
        sutips.append(subscriber.pgw_v6_control_address)
    if hasattr(subscriber, "pgw_v6_user_address"):
        sutips.append(subscriber.pgw_v6_user_address)
    if hasattr(subscriber, "sxb_to_up_v6_user_node"):
        sutips.append(subscriber.sxb_to_up_v6_user_node)
    for addr in sutips:
        tester.invoke('sut_config', name=addr, ip=addr, ManagementIp=addr, Username=sutusername, Password=sutpasswd)

    # Get Access address details
    pgwv4addr = ipaddress.IPv4Interface(subscriber.user_base_address)
    access_addr = str(pgwv4addr.ip)
    access_mask = str(pgwv4addr.netmask)
    num_access_address = pgwv4addr.network.num_addresses - 2
    num_access_address = str(num_access_address)

    # Get Control address details
    sx_v4addr = ipaddress.IPv4Interface(subscriber.control_base_address)
    control_addr = str(sx_v4addr.ip)
    control_mask = str(sx_v4addr.netmask)
    num_control_address = sx_v4addr.network.num_addresses - 2
    num_control_address = str(num_control_address)

    # Get Uplink v4 address details
    uplink_v4addr = ipaddress.IPv4Interface(subscriber.uplink_base_address)
    uplink_addr = str(uplink_v4addr.ip)
    # if '/' in str(uplink_v4addr):
    uplink_mask = str(uplink_v4addr.netmask)
    num_uplink_address = uplink_v4addr.network.num_addresses - 2
    num_uplink_address = str(num_uplink_address)

    # Check whether accessX and controlX are consolidated to a single port
    if subscriber.control_interface != subscriber.access_interface:
        # Control and Access do NOT share a port
        port_list = [subscriber.access_interface, subscriber.uplink_interface, subscriber.control_interface]
        addr_list = [access_addr, uplink_addr, control_addr]
        mask_list = [access_mask, uplink_mask, control_mask]
        num_address_per_port_list = [num_access_address, num_uplink_address, num_control_address]
    else:
        # Control and Access share a port and network
        subscriber.sxb_to_up_user_node = subscriber.pgw_user_address  # Same target address if sharing port
        port_list = [subscriber.access_interface, subscriber.uplink_interface]
        addr_list = [access_addr, uplink_addr]
        mask_list = [access_mask, uplink_mask]
        num_address_per_port_list = [num_access_address, num_uplink_address]

    if hasattr(subscriber, 'uplink_v6_base_address'):
        uplink_v6 = ipaddress.IPv6Interface(subscriber.uplink_v6_base_address)
        # We want to increase the end of the uplink_v6_base_address by 1 because landslide doesn't accept it otherwise
        uplink_v6addr = str(uplink_v6.ip + 1)
        uplink_v6_mask = str(uplink_v6.netmask)
        # Landslide cannot allocate very large v6 networks
        num_uplink_v6_address = min(4000, uplink_v6.network.num_addresses - 2)
        num_uplink_v6_address = str(num_uplink_v6_address)
        # Append reserve_ports lists
        port_list.append(subscriber.uplink_v6_interface)
        addr_list.append(uplink_v6addr)
        mask_list.append(uplink_v6_mask)
        num_address_per_port_list.append(num_uplink_v6_address)
    if hasattr(subscriber, 'user_v6_base_address'):
        access_v6 = ipaddress.IPv6Interface(subscriber.user_v6_base_address)
        # We want to increase the end of the access_v6_base_address by 1 because landslide doesn't accept it otherwise
        access_v6addr = str(access_v6.ip + 1)
        access_v6_mask = str(access_v6.netmask)
        # Landslide cannot allocate very large v6 networks
        num_access_v6_address = min(4000, access_v6.network.num_addresses - 2)
        num_access_v6_address = str(num_access_v6_address)
        # Append reserve_ports lists
        port_list.append(subscriber.access_v6_interface)
        addr_list.append(access_v6addr)
        mask_list.append(access_v6_mask)
        num_address_per_port_list.append(num_access_v6_address)
    # If the control interface == the access interface, we don't want to duplicate ports, so we don't add control
    if (hasattr(subscriber, 'control_v6_base_address') and
            not(hasattr(subscriber, 'user_v6_base_address') and subscriber.control_v6_interface == subscriber.access_v6_interface)):
        control_v6 = ipaddress.IPv6Interface(subscriber.control_v6_base_address)
        # We want to increase the end of the control_v6_base_address by 1 because landslide doesn't accept it otherwise
        control_v6addr = str(control_v6.ip + 1)
        control_v6_mask = str(control_v6.netmask)
        # Landslide cannot allocate very large v6 networks
        num_control_v6_address = min(4000, control_v6.network.num_addresses - 2)
        num_control_v6_address = str(num_control_v6_address)
        # Append reserve_ports lists
        port_list.append(subscriber.control_v6_interface)
        addr_list.append(control_v6addr)
        mask_list.append(control_v6_mask)
        num_address_per_port_list.append(num_control_v6_address)

    ## Reserve ports
    t.log("port_list is {}, addr_list is {}, mask_list is {}".format(port_list, addr_list, mask_list))

    response = tester.invoke('reserve_ports', testSessionHandle=retdict['testSessionHandle'], portList=port_list,
                         ipAddressList=addr_list, tsName=tsname, type='ip', numAddressList=num_address_per_port_list,
                         ipMaskList=mask_list)
    t.log("reserve ports {}, the response is {}".format(port_list, response))

    nodal_args = {}
    nodal_args['mode'] = 'create'
    nodal_args['IpType'] = subscriber.family
    nodal_args['testSessionHandle'] = retdict['testSessionHandle']
    nodal_args['tsName'] = tsname
    nodal_args['testCaseName'] = nodal_testcasename
    nodal_args['libraryName'] = libraryname
    nodal_args['TestActivity'] = subscriber.test_activity
    nodal_args['SessionRetries'] = str(subscriber.session_retries).lower()
    nodal_args['DedicatedsPerDefaultBearer'] = subscriber.dedicated_bearers
    nodal_args['UeInitBearerEn'] = 'true'
    nodal_args['S5Protocol'] = 'GTPv2'
    nodal_args['Sessions'] = subscriber.session_count
    nodal_args['DefaultBearers'] = subscriber.bearer_per_session
    # No Dual Stack support
    nodal_args['SutPgwUserSut'] = getattr(subscriber, 'pgw_v6_user_address', subscriber.pgw_user_address)
    nodal_args['SutPgwSut'] = getattr(subscriber, 'pgw_v6_control_address', subscriber.pgw_control_address)

    nodal_args['Gtp2Version'] = subscriber.s11_gtpv2_version
    nodal_args['Gtp2Imsi'] = subscriber.s11_start_imsi
    nodal_args['Gtp2Imei'] = subscriber.s11_start_imei
    nodal_args['Gtp2N3Attempts'] = 5
    nodal_args['Gtp2T3Time'] = 20
    nodal_args['Gtp2RadioAccessType'] = subscriber.s11_radio_access_type  # eutran means 6?
    nodal_args['Gtp2GtpcTunnelEndptId'] = subscriber.s11_gtp_c_tunnel_id
    nodal_args['Gtp2GtpuTunnelEndptId'] = subscriber.s11_gtp_u_tunnel_id
    nodal_args['Gtp2GtpuIncludeSeqEn'] = "true"
    nodal_args['Gtp2UliDbCmdCbRspEn'] = "true"
    nodal_args['Gtp2ApnTotalApns_0'] = subscriber.s11_total_apns
    nodal_args['Gtp2ApnNumSpecifiedApns_0'] = 0
    nodal_args['Gtp2ApnTotalApns_1'] = subscriber.s11_total_apns
    nodal_args['Gtp2ApnNumSpecifiedApns_1'] = 0
    nodal_args['Gtp2Apn_0'] = subscriber.apn_name
    nodal_args['Gtp2AmbrDownlink'] = '10000000'
    nodal_args['Gtp2AmbrUplink'] = '10000000'
    nodal_args['PgwNodeEn'] = 'false'
    # No Dual Stack support
    nodal_args['SgwControlNodePhy'] = getattr(subscriber, 'control_v6_interface', subscriber.control_interface)
    nodal_args['SgwControlNodeIp'] = getattr(subscriber, 'sgw_control_node_start_ipv6', subscriber.sgw_control_node_start_ip)
    nodal_args['NumLinksOrNodes'] = subscriber.sgw_control_node_count
    nodal_args['TargetSgwControlNodePhy'] = getattr(subscriber, 'control_v6_interface', subscriber.control_interface)
    nodal_args['TargetSgwControlNodeIp'] = getattr(subscriber, 'target_sgw_control_node_v6', subscriber.target_sgw_control_node)
    # No Dual Stack support
    nodal_args['SgwUserNodePhy'] = getattr(subscriber, 'access_v6_interface', subscriber.access_interface)
    nodal_args['SgwUserNodeIp'] = getattr(subscriber, 'sgw_user_node_start_ipv6', subscriber.sgw_user_node_start_ip)
    nodal_args['TargetSgwUserNodePhy'] = getattr(subscriber, 'access_v6_interface', subscriber.access_interface)
    nodal_args['TargetSgwUserNodeIp'] = getattr(subscriber, 'target_sgw_user_node_v6', subscriber.target_sgw_user_node)

    # Multiple CPF
    if int(subscriber.pgw_control_node_count) > 1:
        nodal_args['PgwNumSutsEn'] = 'true'
        nodal_args['PgwNumSuts'] = subscriber.pgw_control_node_count

    if subscriber.use_loopback_access:
        # No Dual Stack support
        nodal_args['SgwUserNodeNextHop'] = getattr(subscriber, 'v6_access_gateway', subscriber.access_gateway)

    if hasattr(subscriber, 'access_vlan_id'):
        nodal_args['SgwUserNodeVlanId'] = subscriber.access_vlan_id
    if hasattr(subscriber, 'control_vlan_id'):
        nodal_args['SgwControlNodeVlanId'] = subscriber.control_vlan_id

    if subscriber.use_static_address:
        nodal_args['UseStaticBearerIp'] = 'true'
        nodal_args['MipStaticHomeAddress'] = subscriber.bearer_ipv6_addr_pool
        nodal_args['PmipV4HomeAddress'] = subscriber.bearer_ipv4_addr_pool

    nodal_args['HomeAddrType'] = subscriber.home_address_type

    subscriber.dmf_handle = {}

    ### Create PGW Nodal testcase
    print("nodal_args is {}".format(nodal_args))
    nodal_testcase_handle = tester.invoke('pgw_nodal_testcase', **nodal_args)
    t.log("nodal testcase {} is created with handle {}".format(nodal_testcasename, nodal_testcase_handle))
    subscriber.nodal_testcase_handle = nodal_testcase_handle

    # PGW Node Testcase
    testCaseName = 'node'
    node_testcasename = t._script_name + '_node_' + subscriber.tag
    subscriber.node_test_case_name = node_testcasename
    node_args = dict()
    node_args['mode'] = 'create'
    node_args['testSessionHandle'] = retdict['testSessionHandle']
    node_args['tsName'] = tsname
    node_args['testCaseName'] = node_testcasename
    node_args['libraryName'] = libraryname

    node_args['S5Protocol'] = 'GTPv2'
    node_args['SxbToPgwUEn'] = 'true'
    node_args['UeInitBearerEn'] = 'true'
    node_args['PgwNodeEn'] = 'true'
    node_args['TrafficMtu'] = subscriber.data_mtu
    node_args['Sessions'] = subscriber.session_count
    node_args['DefaultBearers'] = subscriber.bearer_per_session
    node_args['DedicatedsPerDefaultBearer'] = subscriber.dedicated_bearers
    node_args['ConnectBearerDelayList'] = [5, 10, ]
    # No Dual Stack support
    node_args['SutSxbGtpuSut'] = getattr(subscriber, 'sxb_to_up_v6_user_node', subscriber.sxb_to_up_user_node)
    node_args['SutSxbUserSut'] = getattr(subscriber, 'sxb_to_up_v6_user_node', subscriber.sxb_to_up_user_node)
    # node_args['SutSxbUPSut'] = getattr(subscriber, 'sxb_to_up_v6_user_node', subscriber.sxb_to_up_user_node)
    node_args['SutSxbUPSut'] = getattr(subscriber, 'pgw_v6_user_address', subscriber.pgw_user_address)

    # No Dual Stack support
    node_args['PgwControlNodePhy'] = getattr(subscriber, 'control_v6_interface', subscriber.control_interface)
    node_args['PgwControlNodeIp'] = getattr(subscriber, 'pgw_control_node_start_ipv6',
        subscriber.pgw_control_node_start_ip)
    node_args['SxbControlNodePhy'] = getattr(subscriber, 'control_v6_interface', subscriber.control_interface)
    node_args['SxbControlNodeIp'] = getattr(subscriber, 'sxb_control_node_start_ipv6',
        subscriber.sxb_control_node_start_ip)
    # node_args['SxbControlNodeNextHop'] = '100.0.0.1'  # temp
    node_args['SxbControlGtpUNodePhy'] = getattr(subscriber, 'control_v6_interface', subscriber.control_interface)
    node_args['SxbControlGtpUNodeIp'] = getattr(subscriber, 'sxb_control_gtp_node_start_ipv6', subscriber.sxb_control_gtp_node_start_ip)
    node_args['NumLinksOrNodes'] = subscriber.pgw_control_node_count

    if subscriber.use_loopback_control:
        # No Dual Stack support
        node_args['SxbControlNodeNextHop'] = getattr(subscriber, 'v6_control_gateway', subscriber.control_gateway)
    if hasattr(subscriber, 'control_vlan_id'):
        node_args['SxbControlNodeVlanId'] = subscriber.control_vlan_id

    node_args['Gtp2Version '] = subscriber.node_gtpv2_version
    node_args['Gtp2Imsi'] = subscriber.node_start_imsi
    node_args['Gtp2Imei'] = subscriber.node_start_imei
    node_args['Gtp2N3Attempts'] = 5
    node_args['Gtp2T3Time'] = 20
    node_args['Gtp2RadioAccessType'] = subscriber.node_radio_access_type;  #
    node_args['Gtp2GtpcTunnelEndptId'] = subscriber.node_gtp_c_tunnel_id
    node_args['Gtp2GtpuTunnelEndptId'] = subscriber.node_gtp_u_tunnel_id

    node_args['Gtp2GtpuIncludeSeqEn'] = "true"
    node_args['Gtp2PersistentImsiEn'] = "false"
    node_args['Gtp2ApnTotalApns_0'] = subscriber.node_total_apns
    node_args['Gtp2Apn_0'] = subscriber.apn_name
    node_args['Gtp2ApnNumSpecifiedApns_0'] = 0
    node_args['Gtp2AmbrDownlink'] = '10000000'
    node_args['Gtp2AmbrUplink'] = '10000000'
    node_args['BearerAddrPool'] = subscriber.bearer_ipv6_addr_pool
    node_args['BearerV4AddrPool'] = subscriber.bearer_ipv4_addr_pool
    node_args['SxbControlSpecVer'] = '3'    # PFCP v14.5.0
    node_args['SxbControlUserInitEn'] = str(subscriber.user_initiated_association).lower()
    node_args['SxbControlNodeHeartbeatRetries'] = subscriber.heartbeat_retries
    node_args['SxbControlNodeHeartbeatInterval'] = subscriber.heartbeat_interval
    node_args['SxbControlNodeRetries'] = subscriber.sx_node_retries
    node_args['SxbControlNodeRetryInterval'] = subscriber.sx_node_retry_interval
    node_args['SxbControlSessionRetries'] = subscriber.sx_session_retries
    node_args['SxbControlSessionRetryInterval'] = subscriber.sx_session_retry_interval

    print("node_args is {}".format(node_args))
    node_testcase_handle = tester.invoke('pgw_node_testcase', **node_args)
    t.log("node testcase {} is created with handle {}".format(node_testcasename, node_testcase_handle))
    subscriber.node_testcase_handle = node_testcase_handle
    t.log("Validate the test session {}".format(subscriber.test_session_name))
    validation_status = tester.invoke('validate_test_configuration', testSessionHandle=subscriber.test_session_handle)
    t.log("Validation Status: {}".format(validation_status))
    tester.invoke('save_config', instance=subscriber.test_session_handle, overwrite=1)
    t.log("Save the test session {}".format(subscriber.test_session_name))
    subscriber.action(action='automation_control')


def create_fwa_subscribers(rt_device_id, subscriber, test_id):
    """

    :param rt_device_id:
    :param subscriber:
    :param test_id
    :return:
    """
    import getpass
    loginname = getpass.getuser()
    test_session_name = loginname + '_' + t._script_name + '_' + str(test_id)
    libraryname = 'sms'
    subscriber.libname = libraryname
    tsname = t['resources']['rt0']['system']['primary']['name']
    if 'uv-ts-name' in t['resources']['rt0']['system']['primary']:
        tsname = t['resources']['rt0']['system']['primary']['uv-ts-name']
    subscriber.tsname = tsname
    tslist = [tsname]
    nodal_testcasename = t._script_name + '_nodal_' + subscriber.tag
    subscriber.nodal_test_case_name = nodal_testcasename
    # Create a new Session and assign the Test Server to be used
    subscriber.test_session_name = test_session_name
    tester = t.get_handle(rt_device_id)
    retdict = tester.invoke('create_test_session', testSessionName=test_session_name, libraryName=libraryname, tsList=tslist)
    subscriber.test_session_handle = retdict['testSessionHandle']
    subscriber.test_server_handle = retdict['testServerHandleList'][tsname]
    sutname = t['resources']['r0']['system']['primary']['name']
    sutip = subscriber.sut_loopback_ip
    sutmgmtip = t['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip']
    sutusername = 'dummy'
    sutpasswd = 'dummy'

    # Create a SUT for the router, not needed in cups, since the subscriber.sgw_user_address
    #tester.invoke('sut_config', name=sutname, ip=sutip, ManagementIp=sutmgmtip, Username=sutusername, Password=sutpasswd)
    sutip2 = subscriber.sgw_control_address
    sutip3 = subscriber.sgw_user_address
    sutip4 = subscriber.pgw_address
    for addr in [sutip2, sutip3, sutip4]:
        tester.invoke('sut_config', name=addr, ip=addr, ManagementIp=addr, Username=sutusername, Password=sutpasswd)
    nodal_args = {}
    nodal_args['mode'] = 'create'
    nodal_args['IpType'] = subscriber.family
    nodal_args['testSessionHandle'] = retdict['testSessionHandle']
    nodal_args['tsName'] = tsname
    nodal_args['testCaseName'] = nodal_testcasename
    nodal_args['libraryName'] = libraryname
    nodal_args['TestActivity'] = subscriber.test_activity
    #nodal_args['NumLinksOrNodes'] = subscriber.count
    nodal_args['DedicatedsPerDefaultBearer'] = subscriber.dedicated_bearers
    nodal_args['UeInitBearerEn'] = 'true'
    nodal_args['S5Protocol'] = 'GTPv2'
    nodal_args['Sessions'] = subscriber.count
    nodal_args['DefaultBearers'] = subscriber.bearer_per_session
    nodal_args['SutSgwUserSut'] = subscriber.sgw_user_address
    nodal_args['SutSgwSut'] = subscriber.sgw_control_address
    nodal_args['SutPgwV4Sut'] = subscriber.pgw_address
    nodal_args['Gtp2Version'] = subscriber.s11_gtpv2_version
    nodal_args['Gtp2Imsi'] = subscriber.s11_start_imsi
    nodal_args['Gtp2Imei'] = subscriber.s11_start_imei
    nodal_args['Gtp2N3Attempts'] = 5
    nodal_args['Gtp2T3Time'] = 20
    nodal_args['Gtp2RadioAccessType'] = subscriber.s11_radio_access_type  # eutran means 6?
    nodal_args['Gtp2GtpcTunnelEndptId'] = subscriber.s11_gtp_c_tunnel_id
    nodal_args['Gtp2GtpuTunnelEndptId'] = subscriber.s11_gtp_u_tunnel_id
    nodal_args['Gtp2GtpuIncludeSeqEn'] = "true"
    nodal_args['Gtp2UliDbCmdCbRspEn'] = "true"
    nodal_args['Gtp2ApnTotalApns_0'] = subscriber.s11_total_apns
    nodal_args['Gtp2ApnNumSpecifiedApns_0'] = 0
    nodal_args['Gtp2ApnTotalApns_1'] = subscriber.s11_total_apns
    nodal_args['Gtp2Apn_0'] = subscriber.apn_name
    nodal_args['Gtp2ApnNumSpecifiedApns_1'] = 0
    nodal_args['PgwNodeEn'] = 'false'

    nodal_args['UeDhcpV4En'] = "true"
    nodal_args['MacAddr'] = subscriber.dhcp_mac
    nodal_args['DhcpCliId'] = subscriber.dhcp_client_id
    nodal_args['DhcpRetries'] = subscriber.dhcp_retries
    nodal_args['DhcpOfferTime'] = 1
    nodal_args['DhcpAckTime'] = 1
    nodal_args['DhcpIaOpt6Type'] = subscriber.dhcp_v6_ia_type

    # Get Access interface details
    access_obj = bbe.get_interfaces('rt0', interfaces='access')[0]      # gets access0 interface
    subscriber.access_interface = access_obj.interface_pic              # returns port, something like 'eth1'
    sgwv4addr = ipaddress.IPv4Interface(subscriber.sgw_user_address)    # 'Special' address from your YAML
    access_addr = str(sgwv4addr.ip)
    if '/' in subscriber.sgw_user_address:
        access_mask = str(sgwv4addr.netmask)
    else:
        access_mask = "255.255.255.0"

    # Get Control interface details
    control_obj = bbe.get_interfaces('rt0', interfaces='control')[0]
    subscriber.control_interface = control_obj.interface_pic
    sx_v4addr = ipaddress.IPv4Interface(subscriber.sgw_control_address)
    control_addr = str(sx_v4addr.ip)
    if '/' in subscriber.sgw_control_address:
        control_mask = str(sx_v4addr.netmask)
    else:
        control_mask = "255.255.255.0"

    # Get Uplink interface details
    uplink_obj = bbe.get_interfaces('rt0', interfaces='uplink')[0]
    subscriber.uplink_interface = uplink_obj.interface_pic
    port_list = [access_obj.interface_pic, uplink_obj.interface_pic, control_obj.interface_pic]
    if hasattr(subscriber, 'traffic_start_ip'):
        if '/' in subscriber.traffic_start_ip:
            v4addr = ipaddress.IPv4Interface(subscriber.traffic_start_ip)
            uplink_addr = str(v4addr.ip)
            uplink_mask = str(v4addr.netmask)
        else:
            uplink_addr = subscriber.traffic_start_ip
            uplink_mask = "255.255.255.0"
    else:
        uplink_addr = '20.20.20.2'
        uplink_mask = "255.255.255.0"
    addr_list = [access_addr, uplink_addr, control_addr]
    mask_list = [access_mask, uplink_mask, control_mask]

    nodal_args['MmeControlNodePhy'] = subscriber.control_interface          # Changed from access --> control
    nodal_args['MmeControlNodeIp'] = subscriber.mme_control_node_start_ip
    nodal_args['NumLinksOrNodes'] = subscriber.mme_control_node_count
    nodal_args['eNodeBUserNodePhy'] = subscriber.access_interface
    nodal_args['eNodeBUserNodeIp'] = subscriber.enodeb_user_node_start_ip

    ## Reserve ports
    if subscriber.traffic and subscriber.traffic_dualstack:
        port_list.append(uplink_obj.interface_pic + 'v6')

        if hasattr(subscriber, 'v6_traffic_start_ip'):
            if '/' in subscriber.v6_traffic_start_ip:
                v6addr = ipaddress.IPv6Interface(subscriber.v6_traffic_start_ip)
                v6_uplink_addr = str(v6addr.ip)
                v6_mask = '/' + str(v6addr._prefixlen)
            else:
                v6_uplink_addr = subscriber.v6_traffic_start_ip
                v6_mask = '/64'
        else:
            v6_uplink_addr = '2000::2'
            v6_mask = "/64"
        addr_list.append(v6_uplink_addr)
        mask_list.append(v6_mask)
        t.log("port_list is {}, addr_list is {}".format(port_list, addr_list))

        response = tester.invoke('reserve_ports', testSessionHandle=retdict['testSessionHandle'], portList=port_list,
                                ipAddressList=addr_list, tsName=tsname, type='ip',
                                numAddressList=['200', '200', '200', '200'], ipMaskList=mask_list)
        t.log("reserve ports {}, the response is {}".format(port_list, response))
    else:
        response = tester.invoke('reserve_ports', testSessionHandle=retdict['testSessionHandle'], portList=port_list,
                             ipAddressList=addr_list, tsName=tsname, type='ip', numAddressList=['200', '200', '200'],
                             ipMaskList=mask_list)
        t.log("reserve ports {}, the response is {}".format(port_list, response))

    dmf_lib_list = []
    dmf_name_list = []
    subscriber.dmf_handle = {}
    if subscriber.traffic:
        nodal_args['DataTraffic'] = "Continuous"
        nodal_args['TrafficMtu'] = subscriber.traffic_mtu
        nodal_args['NetworkHost'] = subscriber.traffic_network_host_type
        nodal_args['TrafficStartType'] = "When Session Established"

        if nodal_args['NetworkHost'] == 'local':
            nodal_args['NetworkHostPhy'] = subscriber.uplink_interface
            nodal_args['NetworkHostStartingIp'] = uplink_addr
            nodal_args['NetworkHostNumOfNodes'] = subscriber.traffic_node_count
            nodal_args['NetworkNextHop'] = subscriber.traffic_gateway
            if subscriber.family.lower() == 'ipv6':
                nodal_args['NetworkHostPhyIpv6'] = uplink_obj.interface_pic + 'v6'
                nodal_args['NetworkHostStartingIpv6'] = v6_uplink_addr
                nodal_args['NetworkHostNumOfNodes'] = subscriber.v6_traffic_node_count
                nodal_args['NetworkNextHopIpv6'] = subscriber.v6_traffic_gateway
            if subscriber.traffic_dualstack:
                nodal_args['NetworkHost'] = 'dualstack'
                nodal_args['NetworkHostPhyIpv6'] = uplink_obj.interface_pic + 'v6'
                nodal_args['NetworkHostStartingIpv6'] = v6_uplink_addr
                nodal_args['NetworkHostNumOfNodesIpv6'] = subscriber.v6_traffic_node_count
                nodal_args['NetworkNextHopIpv6'] = subscriber.v6_traffic_gateway

        if nodal_args['NetworkHost'] == 'remote':
            nodal_args['NetworkHostAddrRemoteList'] = [uplink_addr]
        if subscriber.traffic_vlan_enable:
            nodal_args['NetworkHostVlanId'] = subscriber.traffic_vlan_id
            if subscriber.traffic_dualstack:
                nodal_args['NetworkHostVlanIdIpv6'] = subscriber.traffic_vlan_id
            if hasattr(subscriber, 'traffic_svlan_id'):
                nodal_args['NetworkHostVlanId'] = subscriber.traffic_svlan_id
                nodal_args['NetworkHostInnerVlanId'] = subscriber.traffic_vlan_id
                if subscriber.traffic_dualstack:
                    nodal_args['NetworkHostVlanIdIpv6'] = subscriber.traffic_svlan_id
                    nodal_args['NetworkHostInnerVlanIdIpv6'] = subscriber.traffic_vlan_id
        dmf_role_list = []
        dmf_transport_list = []
        for name in subscriber.traffic_profile:
            dmf_args = {}
            dmf_args['dmfName'] = t._script_name + "_" + name
            dmf_args['mode'] = 'create'
            dmf_args['DataProtocol'] = subscriber.traffic_profile[name]['type']
            dmf_args['TransactionRate'] = subscriber.traffic_profile[name]['rate']
            dmf_args['TotalTransactions'] = subscriber.traffic_profile[name]['transaction']
            if subscriber.traffic_profile[name]['start'] == "paused":
                dmf_args['StartPaused'] = 'true'
            if subscriber.traffic_profile[name]['start'] == "on-event":
                dmf_args['StartOnEvent'] = 'true'
            dmf_args['PacketSize'] = subscriber.traffic_profile[name]['packet_size']
            dmf_args['libraryName'] = 'sms/spirentEval'
            dmf_args['TimeToLive'] = subscriber.traffic_profile[name]['ttl']
            dmf_args['SegmentSize'] = subscriber.traffic_profile[name]['segment_size']
            #dmf_args['InitiatingSide'] = subscriber.traffic_profile[name]['initiate_side']
            dmf_args['HostDataExpansionRatio'] = subscriber.traffic_profile[name]['ratio']
            dmf_args['InitiatingSide'] = subscriber.traffic_profile[name]['role']
            if dmf_args['DataProtocol'] == 'udp':
                if 'udp_burst_count' in subscriber.traffic_profile[name]:
                    dmf_args['BurstCount'] = subscriber.traffic_profile[name]['udp_burst_count']
            if dmf_args['DataProtocol'] == 'tcp':
                if 'tcp_socket_disc_side' in subscriber.traffic_profile[name]:
                    dmf_args['DisconnectSide'] = subscriber.traffic_profile[name]['tcp_socket_disc_side']
                if 'tcp_3way_handshake' in subscriber.traffic_profile[name]:
                    dmf_args['Force3Way'] = subscriber.traffic_profile[name]['tcp_3way_handshake']
                if 'tcp_disconnect_type' in subscriber.traffic_profile[name]:
                    dmf_args['DisconnectType'] = subscriber.traffic_profile[name]['tcp_disconnect_type']
                if 'tcp_congestion_avoid' in subscriber.traffic_profile[name]:
                    dmf_args['SlowStart'] = subscriber.traffic_profile[name]['tcp_congestion_avoid']
                if 'tcp_window_size' in subscriber.traffic_profile[name]:
                    dmf_args['WindowSize'] = subscriber.traffic_profile[name]['tcp_window_size']
                if 'tcp_max_segment_size' in subscriber.traffic_profile[name]:
                    dmf_args['MaxSegmentSize'] = subscriber.traffic_profile[name]['tcp_max_segment_size']
                if 'tcp_min_header_size' in subscriber.traffic_profile[name]:
                    dmf_args['MinTcpHeaderSize'] = subscriber.traffic_profile[name]['tcp_min_header_size']
                if 'tcp_max_packets_before_ack' in subscriber.traffic_profile[name]:
                    dmf_args['MaxPacketsToForceAck'] = subscriber.traffic_profile[name]['tcp_max_packets_before_ack']

            if 'tos' in subscriber.traffic_profile[name]:
                tos_list = subscriber.traffic_profile[name]['tos']
                for index in range(len(tos_list)):
                    dmf_name = t._script_name + "_" + name + str(index)
                    dmf_args['dmfName'] = dmf_name
                    if 'client_port' in subscriber.traffic_profile[name]:
                        dmf_args['ClientPort'] = int(subscriber.traffic_profile[name]['client_port']) + index
                    if 'server_port' in subscriber.traffic_profile[name]:
                        dmf_args['ServerPort'] = int(subscriber.traffic_profile[name]['server_port']) + index
                    dmf_args['TypeOfService'] = tos_list[index]

                    # subscriber.dmf_handle[dmf_name] = ls.config_dmf(**dmf_args)
                    subscriber.dmf_handle[dmf_name] = tester.invoke('config_dmf', **dmf_args)
                    t.log("created dmf stream {} with args {}".format(dmf_name, dmf_args))
                    dmf_lib_list.append('sms/spirentEval')
                    dmf_name_list.append(dmf_name)
                    dmf_role_list.append(subscriber.traffic_profile[name]['role'])
                    dmf_transport_list.append(subscriber.traffic_profile[name]['preferred_transport'])
            else:
                dmf_name = dmf_args['dmfName']
                # subscriber.dmf_handle[dmf_name] = ls.config_dmf(**dmf_args)
                subscriber.dmf_handle[dmf_name] = tester.invoke('config_dmf', **dmf_args)
                t.log("created dmf stream {} with args {}".format(dmf_name, dmf_args))
                dmf_lib_list.append('sms/spirentEval')
                dmf_name_list.append(dmf_name)
                dmf_role_list.append(subscriber.traffic_profile[name]['role'])
                dmf_transport_list.append(subscriber.traffic_profile[name]['preferred_transport'])

    #nodal_args['EnableExternalData'] = 0
        if dmf_role_list:
            nodal_args['nodeRoleList'] = dmf_role_list
        if dmf_transport_list:
            nodal_args['preferredTransportList'] = dmf_transport_list
    if dmf_lib_list:
        nodal_args['dmfLibraryList'] = dmf_lib_list
    if dmf_name_list:
        nodal_args['dmfList'] = dmf_name_list
    print("nodal_args is {}".format(nodal_args))

    ###create nodal testcase
    nodal_testcase_handle = tester.invoke('sgw_nodal_testcase', **nodal_args)
    t.log("nodal testcase {} is created with handle {}".format(nodal_testcasename, nodal_testcase_handle))
    subscriber.nodal_testcase_handle = nodal_testcase_handle
    t.log("Validate the test session {}".format(subscriber.test_session_name))
    validation_status = tester.invoke('validate_test_configuration', testSessionHandle=subscriber.test_session_handle)
    t.log("Validation Status: {}".format(validation_status))
    tester.invoke('save_config', instance=subscriber.test_session_handle, overwrite=1)
    t.log("Save the test session {}".format(subscriber.test_session_name))
