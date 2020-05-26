#
"""
This module provides additional user function methods for Spirent tester

"""
import ipaddress
import re
#import os
from netaddr import IPAddress, EUI
from time import sleep

def bbe_initialize(rt_handle, **kwargs):
    """
    :param rt_handle:                RT object
    :param port_list:           list of RT ports
    :return:
    """
    rt_handle.handles = {}
    rt_handle.bgp_handle = []
    rt_handle.dhcpv4_client_handle = []
    rt_handle.dhcpv6_client_handle = []
    rt_handle.pppox_client_handle = []
    rt_handle.device_group_handle = []
    rt_handle.dhcpv4_server_handle = []
    rt_handle.dhcpv6_server_handle = []
    rt_handle.ancp_handle = []
    rt_handle.ancp_line_handle = []
    rt_handle.ancp_line_args = {}
    rt_handle.lac_handle = []
    rt_handle.lns_handle = []
    rt_handle.l2tp_client_handle = []
    rt_handle.l2tp_server_session_handle = []
    rt_handle.link_ip_handle = []
    rt_handle.link_ipv6_handle = []
    rt_handle.link_gre_handle = []
    rt_handle.remote_id = {}
    rt_handle.circuit_id = {}
    rt_handle.interface_id = {}
    rt_handle.v6_remote_id = {}
    rt_handle.enterprise_id = {}
    rt_handle.dhcpv4_index = 0
    rt_handle.dhcpv6_index = 0
    rt_handle.pppoev4_index = 0
    rt_handle.pppoev6_index = 0
    rt_handle.traffic_item = []
    rt_handle.stream_id = []
    rt_handle.igmp_handles = {}
    rt_handle.igmp_handle_to_group = {}
    rt_handle.mld_handles = {}
    rt_handle.mld_handle_to_group = {}
    rt_handle.ae = {}
    rt_handle.device_to_dhcpv4_index = dict()
    rt_handle.device_to_dhcpv6_index = dict()
    rt_handle.device_to_pppoe_index = dict()
    rt_handle.port_to_dhcp_index = dict()
    rt_handle.port_to_pppoe_index = dict()
    rt_handle.stream_Name = ''
    rt_handle.streamBlockDurationMap = dict()
    rt_handle.stream_name_map = dict()
    rt_handle.topology = []
    rt_handle.homeGwToClientMap = dict() # Dict that maps Home Gateway to the clients behind it.
    rt_handle.dhcpv4_client_device_handle = []
    rt_handle.dhcpv6_client_device_handle = []
    rt_handle.link_ip_device_handle = []
    rt_handle.link_ipv6_device_handle = []
    rt_handle.pppox_client_device_handle = []
    rt_handle.base_subscriber_mac = '00:AA:AA:00:00:01'  # this value will be advanced by 16K in set_subscriber_mac under subscriber host handles
    port_list = list(rt_handle.port_to_handle_map.keys())

    for port in port_list:
        port_handle = rt_handle.port_to_handle_map[port]
        rt_handle.handles[port] = {}
        rt_handle.handles[port]['device_group_handle'] = []
        rt_handle.handles[port]['ethernet_handle'] = []
        rt_handle.handles[port]['ipv4_handle'] = []
        rt_handle.handles[port]['ipv6_handle'] = []
        rt_handle.handles[port]['dhcpv4_client_handle'] = []
        rt_handle.handles[port]['dhcpv6_client_handle'] = []
        rt_handle.handles[port]['pppox_client_handle'] = []
        rt_handle.handles[port]['port_handle'] = rt_handle.port_to_handle_map[port]
        rt_handle.handles[port]['dhcpv6_over_pppox_handle'] = {}

    for port in port_list:
        port_handle = rt_handle.port_to_handle_map[port]
        handle_list = list(t.t_dict['resources']['rt0']['interfaces'].keys())
        for handle in handle_list:
            if t.t_dict['resources']['rt0']['interfaces'][handle]['name'] == port:
                rt_handle.invoke('invoke', cmd='stc::config {} -name {}'.format(port_handle, handle))

def set_v6_option(rt_handle, **kwargs):
    """
    dhcpv6 interface_id(option 17) and remote_id (option 38)
    :param rt_handle:                    RT object
    :param kwargs:
    handle:                         dhcpv6 device handle
    interface_id:                   interface_id string, if with ? inside it, it means the string will increase based
                                    on the start/step/repeat at that location or default
    interface_id_start:             interface_id_start num
    interface_id_step:              interface_id_step num
    interface_id_repeat:            interface_id_repeat num
    remote_id:                      remote_id string, if with ? inside it, it means the string will increase based on
                                    the start/step/repeat or default
    remote_id_start:                remote_id_start num
    remote_id_step:                 remote_id_step num
    remote_id_repeat:               remote_id_repeat num
    enterprise_id:                  enterprise_id used inside of remote id
    enterprise_id_step:             enterprise_id_step num
    :return:
    status:                         1 or 0
    """
    status = '1'
    args = ''
    if 'handle' in kwargs and 'v6' in kwargs['handle']:
        handle = kwargs.get('handle')
        args += ' -EnableLdra true '
        if 'interface_id' in kwargs or 'v6_remote_id' in kwargs or 'enterprise_id' in kwargs:
            if 'interface_id' in kwargs:
                interface_id = kwargs.get('interface_id')
                if 'interface_id_start' in kwargs:
                    start = kwargs.get('interface_id_start')
                    step = kwargs.get('interface_id_step', '1')
                    repeat = int(kwargs.get('interface_id_repeat', '1'))-1
                    if repeat < 0:
                        repeat = 0
                    increment = '@x({},0,{},0,{})'.format(start, step, repeat)
                    if '?' in interface_id:
                        interface_id = interface_id.replace('?', increment)
                    else:
                        interface_id = interface_id + increment
                args += ' -EnableInterfaceId true -InterfaceId {{{}}} '.format(interface_id)
                rt_handle.interface_id[handle] = interface_id

            if 'v6_remote_id' in kwargs:
                v6_remote_id = kwargs.get('v6_remote_id')
                if 'v6_remote_id_start' in kwargs:
                    start = kwargs.get('v6_remote_id_start')
                    step = kwargs.get('v6_remote_id_step', '1')
                    repeat = int(kwargs.get('v6_remote_id_repeat', '1'))-1
                    if repeat < 0:
                        repeat = 0
                    increment = '@x({},0,{},0,{})'.format(start, step, repeat)
                    if '?' in v6_remote_id:
                        v6_remote_id = v6_remote_id.replace('?', increment)
                    else:
                        v6_remote_id = v6_remote_id + increment
                args += ' -EnableRemoteId true -RemoteId {{{}}} '.format(v6_remote_id)
                rt_handle.v6_remote_id[handle] = v6_remote_id

            if 'enterprise_id' in kwargs:
                enterprise_id = kwargs.get('enterprise_id')
                if re.match('-EnableRemoteId\s+true', args, re.I):
                    args += ' -RemoteIdEnterprise {} '.format(enterprise_id)
                else:
                    args += ' -EnableRemoteId true -RemoteIdEnterprise {{{}}} '.format(enterprise_id)
                rt_handle.enterprise_id[handle] = enterprise_id

            if args:
                rt_handle.invoke('invoke', cmd='stc::config {} {}'.format(handle, args))

        if 'dns_server' in kwargs:
            payload_string = str(kwargs['dns_server'])
            enable_wildcards = False
            print("Payload string is:", payload_string)
            if not create_dhcpv6_message(rt_handle, handle=handle, option_type=23, payload_string=payload_string,
                                         enable_wildcards=enable_wildcards):
                status = 0

    return status


def set_vlan(rt_handle, **kwargs):
    """
    :param rt_handle:                RT object
    :param kwargs:
    handle                      device group handle
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    svlan_length:               svlan sequence length
    :return:
    result
    """
    # handle can be device handle or children protocol handle
    if 'handle' not in kwargs:
        raise Exception("device handle is mandatory")
    vlan_args = dict()

    if not re.match('host|router|emulateddevice', kwargs['handle']):
        vlan_args['handle'] = rt_handle.invoke('invoke', cmd='stc::get ' + kwargs['handle'] + ' -parent')
    else:
        vlan_args['handle'] = kwargs['handle']

    vlan_map = {'vlan_start'  :['vlan_id', 100],
                'vlan_step'   :['vlan_id_step', 1],
                'vlan_repeat' :['vlan_id_repeat_count', 1],
                #'vlan_tpid'   :['vlan_tpid', 8100],
                'vlan_length' :['vlan_id_count', 4094],
                'svlan_start' :['vlan_outer_id', 100],
                'svlan_step'  :['vlan_outer_id_step', 1],
                'svlan_repeat':['vlan_outer_id_repeat_count', 1],
                #'svlan_tpid'  :['vlan_outer_tpid', 8100],
                'svlan_length':['vlan_outer_id_count', 4094]}

    if '__set_vlan_no_default' in kwargs:
        # only get those that have values in kwargs, for modify
        for key in vlan_map:
            if key in kwargs:
                vlan_args[vlan_map.get(key)[0]] = kwargs.get(key)
    else:
        # get all values or default values, for create
        if 'vlan_start' in kwargs:
            vlan_args['encapsulation'] = 'ethernet_ii_vlan'
        if 'svlan_start' in kwargs:
            vlan_args['encapsulation'] = 'ethernet_ii_qinq'
        if 'encapsulation' in kwargs:
            vlan_args['encapsulation'] = kwargs['encapsulation']
        for key in vlan_map:
            if 'repeat' in key:
#                print "Repeat value needs to be manipulated for STC, current value:" + str(kwargs.get(key, vlan_map.get(key)[1]))
                vlan_args[vlan_map.get(key)[0]] = int(kwargs.get(key, vlan_map.get(key)[1]))-1 if int(kwargs.get(key, vlan_map.get(key)[1]))-1 >= 0 else 0
#                print "Repeat value after manipulation:" + str(vlan_args[vlan_map.get(key)[0]])
            else:
                vlan_args[vlan_map.get(key)[0]] = kwargs.get(key, vlan_map.get(key)[1])
#            vlan_args[vlan_map.get(key)[0]] = kwargs.get(key, vlan_map.get(key)[1])

    vlan_args['mode'] = 'modify'
    result = rt_handle.invoke('emulation_device_config', **vlan_args)
    if result['status'] != '1':
        raise Exception("failed to set vlan for {}".format(vlan_args['handle']))

    set_subscriber_mac(rt_handle, **kwargs)

    return result

def set_subscriber_mac(rt_handle, **kwargs):
    """
    :param rt_handle:                RT object
    :param kwargs:
    handle                      device group handle
    mac:                        mac
    :return:
    result
    """
    # handle can be device handle or children protocol handle
    if 'handle' not in kwargs:
        raise Exception("device handle is mandatory")
    mac_args = dict()

    if not re.match('host|router|emulateddevice', kwargs['handle']):
        mac_args['handle'] = rt_handle.invoke('invoke', cmd='stc::get ' + kwargs['handle'] + ' -parent')
    else:
        mac_args['handle'] = kwargs['handle']

    mac_args['mac_addr'] = kwargs.get('mac', rt_handle.base_subscriber_mac)

    # we advance default mac as spirent by default advances mac addresses from host (a group of subscribers)
    # to the next host only by 00:00:00:00:01 - this creates overlapping mac addresses from one group
    # of subscribers to the next which will result in subscribers not registering against the BNG
    if 'mac' in kwargs:
        mac = EUI(rt_handle.base_subscriber_mac)
        macstring_plus_sixteenk = str(format((int(mac)+16000), '02X')).zfill(12)
        delimiter = ":"
        mac_segments = re.findall('..', macstring_plus_sixteenk)
        rt_handle.base_subscriber_mac = delimiter.join(mac_segments)
    mac_args['mode'] = 'modify'
    result = rt_handle.invoke('emulation_device_config', **mac_args)
    if result['status'] != '1':
        raise Exception("failed to set mac for {}".format(mac_args['handle']))

    return result

def create_dhcpv6_message(rt_handle, **kwargs):
    '''
    This method is used to create DHCPv6 custom messages.
    '''

    if 'handle' not in kwargs:
        raise ValueError('handle is a mandatory argument to the create_dhcpv6_message API')
    handle = kwargs['handle']

    if 'option_type' not in kwargs:
        raise ValueError('option_type is a mandatory argument to the create_dhcpv6_message API')

    # Check if the device already has DHCPv6 custom options set, and if so,
    # check if the same option type is already configured. If so, delete it
    # and create a new one with the provided parameters.

    existing_custom_option_list = rt_handle.invoke('invoke', cmd='stc::get '+ handle +' -children-Dhcpv6MsgOption').strip().split()
    for custom_option_handle in existing_custom_option_list:
        if int(rt_handle.invoke('invoke', cmd='stc::get '+ custom_option_handle +' -OptionType')) == int(kwargs['option_type']):
            rt_handle.invoke('invoke', cmd='stc::delete '+ custom_option_handle)
            break

    # Configure the custom option
    rt_handle.invoke('invoke', cmd='stc::create Dhcpv6MsgOption -under '+ handle +' -MsgType BOTH -optionType '+str(kwargs['option_type'])+' -Payload {'+ kwargs['payload_string'] + '} -enableWildcards '+ str(kwargs['enable_wildcards']))

    return 1

def create_dhcpv4_message(rt_handle, **kwargs):
    '''
    This method is used to create DHCPv4 custom messages.
    '''

    if 'handle' not in kwargs:
        raise ValueError('handle is a mandatory argument to the create_dhcpv4_message API')
    handle = kwargs['handle']

    if 'option_type' not in kwargs:
        raise ValueError('option_type is a mandatory argument to the create_dhcpv4_message API')

    # Check if the device already has DHCPv4 custom options set, and if so,
    # check if the same option type is already configured. If so, delete it
    # and create a new one with the provided parameters.

    existing_custom_option_list = rt_handle.invoke('invoke', cmd='stc::get '+ handle +' -children-Dhcpv4MsgOption').strip().split()
    for custom_option_handle in existing_custom_option_list:
        if int(rt_handle.invoke('invoke', cmd='stc::get '+ custom_option_handle +' -OptionType')) == int(kwargs['option_type']):
            rt_handle.invoke('invoke', cmd='stc::delete '+ custom_option_handle)
            break

    # Configure the custom option
    rt_handle.invoke('invoke', cmd='stc::create Dhcpv4MsgOption -under '+ handle +' -MsgType BOTH -optionType '+str(kwargs['option_type'])+' -Payload {'+ kwargs['payload_string'] + '} -enableWildcards '+ str(kwargs['enable_wildcards']))

    return 1

def set_v4_option(rt_handle, **kwargs):
    '''
    This method is used to configure the DHCPv4 client options like remote ID, circuit ID etc..,
    '''
    return_status = 1
    if 'handle' not in kwargs:
        raise ValueError('handle is a mandatory argument to the set_v4_option API')
    handle = kwargs['handle']

    # v4 Clients: Remote ID and Circuit ID.
    if 'remote_id' in kwargs or 'circuit_id' in kwargs:
        if not set_option_82(rt_handle, **kwargs):
            return_status = 0

    # v4 Clients: Vendor class ID
    if 'vendor_class_id' in kwargs:
        payload_string = str(kwargs['vendor_class_id'])
        enable_wildcards = False
        if 'vendor_class_id_start' in kwargs:
            enable_wildcards = True
            vendor_class_id_start = str(kwargs['vendor_class_id_start'])
            vendor_class_id_length = str(kwargs.get('vendor_class_id_length', 1))
            vendor_class_id_step = str(kwargs.get('vendor_class_id_step', 1))
            vendor_class_id_repeat = 0
            if 'vendor_class_id_repeat' in kwargs and kwargs['vendor_class_id_repeat'] > 0:
                vendor_class_id_repeat = str(int(kwargs['vendor_class_id_repeat'] -1))
            payload_string += '@x('+vendor_class_id_start+','+vendor_class_id_length+','+vendor_class_id_step+',0,'+vendor_class_id_repeat+')'
        print("Payload string is:", payload_string)
        if not create_dhcpv4_message(rt_handle, handle=handle, option_type=60, payload_string=payload_string, enable_wildcards=enable_wildcards):
            return_status = 0

    return return_status

def set_option_82(rt_handle, **kwargs):
    """
    this is for dhcpv4 option 82
    :param rt_handle:                RT object
    :param kwargs:
    handle:                     dhcpv4 client handle
    circuit_id:                 circuit id string( if with ? with the circuit id, it will replace ? with the increase)
    circuit_id_start:           circuit id start num
    circuit_id_step:            circuit id step num
    circuit_id_repeat:          circuit_id_repeat_num
    remote_id:                  remote id string
    remote_id_start:            remote id start num
    remote_id_step:             remote_id_step num
    remote_id_repeat:           remote_id_repeat num
    :return:
    status:                     1 or 0
    """
    status = '1'
    args = ''
    #if 'handle' in kwargs and 'v4' in kwargs.get('handle'):
    if 'handle' in kwargs:
        handle = kwargs.get('handle')
        if 'circuit_id' in kwargs:
            circuit_id = str(kwargs.get('circuit_id'))
            if 'circuit_id_start' in kwargs:
                start = kwargs.get('circuit_id_start')
                step = kwargs.get('circuit_id_step', '1')
                repeat = int(kwargs.get('circuit_id_repeat', '1'))-1
                if repeat < 0:
                    repeat = 0
                increment = '@x({},0,{},0,{})'.format(start, step, repeat)
                if '?' in circuit_id:
                    circuit_id = circuit_id.replace('?', increment)
                else:
                    circuit_id = circuit_id + increment
            if 'pppoe' in handle:
                args += ' -EnableRelayAgent true -RelayAgentType DSL_FORUM -CircuitId {{{}}} '.format(circuit_id)
            else:
                args += ' -EnableCircuitId true -CircuitId {{{}}} '.format(circuit_id)
            rt_handle.circuit_id[handle] = circuit_id

        if 'remote_id' in kwargs:
            remote_id = str(kwargs.get('remote_id'))
            if 'remote_id_start' in kwargs:
                start = kwargs.get('remote_id_start')
                step = kwargs.get('remote_id_step', '1')
                repeat = int(kwargs.get('remote_id_repeat', '1'))-1
                if repeat < 0:
                    repeat = 0
                increment = '@x({},0,{},0,{})'.format(start, step, repeat)
                if '?' in remote_id:
                    remote_id = remote_id.replace('?', increment)
                else:
                    remote_id = remote_id + increment
            if 'pppoe' in handle:
                args += ' -RemoteOrSessionId {{{}}} '.format(remote_id)
            else:
                args += ' -EnableRemoteId true -RemoteId {{{}}} '.format(remote_id)
            rt_handle.remote_id[handle] = remote_id

    if args:
        rt_handle.invoke('invoke', cmd='stc::config {} {}'.format(handle, args))

    return status

def add_dhcp_client(rt_handle, **kwargs):
    """
    :param rt_handle:                RT object
    :param kwargs:
    mandatory:
    port:                       Tester physical port
    num_sessions:               client counts

    optional:
    ip_type:                    ipv4, ipv6, dual
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    svlan_length:               svlan sequence length
    remote_id:                  option82 remote_id string
    remote_id_start:            remote id start number
    remote_id_step:             remote id step number
    remote_id_repeat:           remote id repeat number
    circuit_id:                 option82 circuit id string
    circuit_id_start:           circuit id start number
    circuit_id_step:            circuit id step number
    circuit_id_repeat:          circuit id repeat number
    v6_remote_id:               v6 option 38 remote id string
    v6_remote_id_start:         remote id start number
    v6_remote_id_step:          remote id step number
    v6_remote_id_repeat:        remote id repeat number
    enterprise_id:              v6 enterprise vendor id, used with remote id
    enterprise_id_step:         enterprise id increase step
    interface_id:               v6 option 17 interface id string
    interface_id_start:         v6 interface id start number
    interface_id_step:          v6 interface id step number
    interface_id_repeat:        v6 interface id repeat number
    rapid_commit:               use_rapid_commit value 1 or 0
    dhcp4_broadcast:            dhcpv4 broadcast value 1 or 0
    dhcpv6_ia_type:             dhcpv6 IA type: IANA, IAPD, IANA_IAPD
    v6_max_no_per_client:       The maximum number of addresses/prefixes that can be negotiated by a DHCPv6 Client
    dhcpv6_iana_count:          The number of IANA IAs requested in a single negotiation
    dhcpv6_iapd_count:          The number of IAPD IAs requested in a single negotiation
    softgre:                    softgre feature 1 or 0
    gre_dst_ip:                 softgre tunnel destination address
    gre_local_ip:               softgre tunnel local address
    gre_netmask:                softgre tunnel mask
    gre_gateway:                softgre tunnel gateway address
    gre_vlan_id:                softgre vlan id
    gre_vlan_id_step:           softgre vlan id step
    mac:                        mac start addr
    mac_step:                   mac address step

    :return: a dictionary of status and handle
    status:                     1 or 0
    device_group_handle:
    ethernet_handle:
    dhcpv4_client_handle:
    dhcpv6_client_handle:
    """

    result = dict()
    result['status'] = '1'
    device_args = dict()
    dhcp_args = dict()
    dhcpv4_args = dict()
    dhcpv6_args = dict()

    # create device group
    if 'port' in kwargs:
        port = kwargs.get('port')
        port_handle = rt_handle.port_to_handle_map[port]
        device_args['port_handle'] = port_handle
        device_args['mode'] = 'create'
        device_args['encapsulation'] = 'ethernet_ii'

        if 'ip_type' in kwargs:
            if 'dual' in kwargs['ip_type']:
                device_args['ip_version'] = 'ipv46'
            elif kwargs['ip_type'] == "ipv6":
                device_args['ip_version'] = 'ipv6'
            else:
                device_args['ip_version'] = 'ipv4'

        if 'vlan_start' in kwargs:
            device_args['encapsulation'] = kwargs.get('encapsulation', 'ethernet_ii_vlan')
        if 'svlan_start' in kwargs:
            device_args['encapsulation'] = kwargs.get('encapsulation', 'ethernet_ii_qinq')
        device_args['count'] = kwargs.get('num_sessions', 1)
        device_status = rt_handle.invoke('emulation_device_config', **device_args)
        if device_status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create device group for port handle {}".format(port_handle))

        result['device_group_handle'] = device_status['handle']
        result['ethernet_handle'] = rt_handle.invoke('invoke', cmd='stc::get ' + device_status['handle'] + ' -children-ethiiif')
        result['ethernet_handle'] = result['ethernet_handle'].strip()

        dhcp_args['mode'] = 'enable'
        dhcp_args['handle'] = device_status['handle']
        dhcp_args['encap'] = device_args['encapsulation']
        block_config_handle = str()
        host_handle = device_status['handle']
    elif 'handle' in kwargs:
        # modify dhcp client
        # handle is dhcpblockconfig
        dhcp_args['mode'] = 'modify'
        block_config_handle = kwargs['handle']
        host_handle = rt_handle.invoke('invoke', cmd='stc::get ' + kwargs['handle'] + ' -parent').strip()
        dhcp_args['handle'] = kwargs['handle']

        if 'v4' in kwargs['handle'] or 'dual' in kwargs['ip_type']:
            dhcpv4_args['encap'] = 'ethernet_ii'
            vlan_objs = rt_handle.invoke('invoke', cmd='stc::get ' + host_handle + ' -children-vlanif').strip()
            if vlan_objs != '':
                encap_map = {1:'ethernet_ii_vlan', 2:'ethernet_ii_qinq'}
                vlan_num = len(vlan_objs.split())
                dhcpv4_args['encap'] = encap_map.get(vlan_num, 'ethernet_ii_mvlan')
        if 'num_sessions' in kwargs:
            dhcpv4_args['num_sessions'] = kwargs['num_sessions']
            device_args['count'] = kwargs['num_sessions']
            device_args['handle'] = host_handle
            device_args['mode'] = 'modify'
            device_status = rt_handle.invoke('emulation_device_config', **device_args)
            if device_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to set num_sessions for handle {}".format(device_args['handle']))
        if 'vlan_start' in kwargs or 'svlan_start' in kwargs:
            if 'vlan_start' in kwargs:
                dhcpv4_args['encap'] = 'ethernet_ii_vlan'
            if 'svlan_start' in kwargs:
                dhcpv4_args['encap'] = 'ethernet_ii_qinq'
        if 'v6' in kwargs['handle']:
            dhcp_args['handle'] = host_handle

    # dhcp
    if 'dhcp4_broadcast' in kwargs:
        dhcpv4_args['broadcast_bit_flag'] = kwargs.get('dhcp4_broadcast')
    if 'rapid_commit' in kwargs:
        rapid_commit_map = {'1':'ENABLE', '0':'DISABLE', 1:'ENABLE', 0:'DISABLE', 'True':'ENABLE', 'False':'DISABLE', 'true':'ENABLE', 'false':'DISABLE'}
        dhcpv6_args['rapid_commit_mode'] = rapid_commit_map[kwargs.get('rapid_commit')]
    if 'dhcpv6_ia_type' in kwargs:
        #dhcpv6_sth_type = {'IANA':'DHCPV6', 'IAPD':'DHCPPD', 'IANA_IAPD':'DHCPV6ANDPD'}
        # kwargs['dhcpv6_ia_type'] getting default IANA_IAPD .As of Bojan suggestion changed DHCPV6ANDPD to DHCPPD
        # 02/20/2018: Mapping this correctly.
        dhcpv6_sth_type = {'IANA':'DHCPV6', 'IAPD':'DHCPPD', 'IANA_IAPD':'DHCPV6ANDPD'}
        dhcpv6_args['dhcp6_client_mode'] = dhcpv6_sth_type.get(kwargs.get('dhcpv6_ia_type').upper())

    # looks like Donald has added home GW support in YAML using the knob named dhcpv6_gateway
    if 'dhcpv6_gateway' in kwargs:
        kwargs['home_gw_ipv6'] = kwargs['dhcpv6_gateway']

    if 'home_gw_ipv6' in kwargs:
        my_current_ip = ipaddress.ip_address(kwargs['home_gw_ipv6'])
        my_next_ip = int(my_current_ip) + 1
        home_ipv6 = ipaddress.ip_address(my_next_ip).compressed
        dhcpv6_args['local_ipv6_addr'] = home_ipv6
        dhcpv6_args['gateway_ipv6_addr'] = kwargs['home_gw_ipv6']

    # Enable LDRA if interface_id or v6_remote_id is being configured for the DHCPv6 client emulation
    ldra = 0
    if 'ip_type' in kwargs and (kwargs['ip_type'] == 'dual' or kwargs['ip_type'] == 'ipv6') and ('interface_id' in kwargs or 'v6_remote_id' in kwargs or 'enterprise_id' in kwargs):
        dhcpv6_args['enable_ldra'] = "true"
        ldra = 1

    if 'ip_type' in kwargs:
        if 'dual' in kwargs['ip_type']:
            if 'handle' in kwargs:
                # get another dhcpblockconfig to modify both
                dual_v6_handle = host_handle
                if re.match('dhcpv4blockconfig', kwargs['handle']):
                    dual_v4_handle = kwargs['handle']
                else:
                    dual_v4_handle = rt_handle.invoke('invoke', cmd='stc::get {} -children-dhcpv4blockconfig'.format(host_handle).strip())

                if 'dhcp4_broadcast' in kwargs:
                    rt_handle.invoke('invoke', cmd='stc::config {} -UseBroadcastFlag {}'.format(dual_v4_handle, kwargs['dhcp4_broadcast']))
            else:
                dhcp_args['dhcp_range_ip_type'] = '4'
                dhcpv4_args.update(dhcp_args)
                config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcpv4_args)
                if config_status['status'] != '1':
                    result['status'] = '0'
                    raise Exception("failed to add dhcp client")
                else:
                    if 'handles' in config_status:
                        handle = config_status['handles']
                        result['dhcpv4_client_handle'] = handle
                        if 'handle' not in kwargs:
                            rt_handle.dhcpv4_index += 1
                            rt_handle.device_to_dhcpv4_index[handle] = rt_handle.dhcpv4_index
                            rt_handle.dhcpv4_client_handle.append(handle)
                            rt_handle.handles[port]['dhcpv4_client_handle'].append(handle)
                            rt_handle.dhcpv4_client_device_handle.append(config_status['handle'])

            dhcp_args['dhcp_range_ip_type'] = '6'
            dhcpv6_args.update(dhcp_args)
            if 'handle' in kwargs:
                dhcpv6_args['handle'] = dual_v6_handle
            config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcpv6_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcpv6 client for dual stack")
            else:
                if 'handles' in config_status:
                    v6handle = config_status['handles']
                    v6_host_handle = config_status['dhcpv6_handle']
                    result['dhcpv6_client_handle'] = v6handle
                    if ldra:
                        result['ldra_handle'] = v6handle
                    if 'handle' not in kwargs:
                        # If mode is DHCPPD or DHCPV6ANDPD, we need to create the
                        # clients behind the home gateway
                        if 'PD' in dhcpv6_args['dhcp6_client_mode']:
                            print("DHCPv6 PD requested. Creating the clients behind the HG")
                            client_args = dict()
                            client_args['count'] = kwargs.get('num_sessions', 1)
                            client_args['mode'] = 'create'
                            client_args['port_handle'] = port_handle
                            client_args['encapsulation'] = 'ethernet_ii'
                            client_args['ip_version'] = 'ipv46'
                            client_args['link_local_ipv6_addr'] = 'fe80::'
                            client_config_status = rt_handle.invoke('emulation_device_config', **client_args)
                            if client_config_status['status'] != '1':
                                result['status'] = '0'
                                raise Exception("failed to add dhcpv6 client")
                            else:
                                client_handle = client_config_status['handle']
                            # Add the Home gateway link
                            home_gw_handle = config_status['dhcpv6_handle']
                            rt_handle.invoke('invoke', cmd='stc::perform ArpNdStart -HandleList {} '.format(home_gw_handle).strip())
                            link_args = dict()
                            link_args['link_src'] = client_handle
                            link_args['link_dst'] = home_gw_handle
                            link_args['link_type'] = 'Home_Gateway_Link'
                            link_create_status = rt_handle.invoke('link_config', **link_args)
                            if link_create_status['status'] != '1':
                                result['status'] = '0'
                                raise Exception("failed to add dhcpv6 client")
                            else:
                                rt_handle.homeGwToClientMap[v6handle] = client_handle
                                rt_handle.homeGwToClientMap[v6_host_handle] = client_handle

                        # End of mode DHCPPD/DHCPV6ANDPD client creation loop
                        rt_handle.dhcpv6_index += 1
                        rt_handle.device_to_dhcpv6_index[v6handle] = rt_handle.dhcpv6_index
                        rt_handle.dhcpv6_client_handle.append(v6handle)
                        rt_handle.handles[port]['dhcpv6_client_handle'].append(v6handle)
                        rt_handle.dhcpv6_client_device_handle.append(config_status['dhcpv6_handle'])

        elif kwargs['ip_type'] == "ipv4":
            if 'handle' in kwargs:
                if 'dhcp4_broadcast' in kwargs:
                    rt_handle.invoke('invoke', cmd='stc::config {} -UseBroadcastFlag {}'.format(kwargs['handle'], kwargs['dhcp4_broadcast']))
            else:
                dhcp_args['dhcp_range_ip_type'] = '4'
                dhcpv4_args.update(dhcp_args)
                config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcpv4_args)
                if config_status['status'] != '1':
                    result['status'] = '0'
                    raise Exception("failed to add dhcp client")
                else:
                    if 'handles' in config_status:
                        handle = config_status['handles']
                        result['dhcpv4_client_handle'] = handle
                        if 'handle' not in kwargs:
                            rt_handle.dhcpv4_index += 1
                            rt_handle.device_to_dhcpv4_index[handle] = rt_handle.dhcpv4_index
                            rt_handle.dhcpv4_client_handle.append(handle)
                            rt_handle.handles[port]['dhcpv4_client_handle'].append(handle)
                            rt_handle.dhcpv4_client_device_handle.append(config_status['handle'])

        elif kwargs['ip_type'] == "ipv6":
            dhcp_args['dhcp_range_ip_type'] = '6'
            dhcpv6_args.update(dhcp_args)
            config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcpv6_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcpv6 client")
            else:
                if 'handles' in config_status:
                    v6handle = config_status['handles']
                    v6_host_handle = config_status['dhcpv6_handle']
                    result['dhcpv6_client_handle'] = v6handle
                    if ldra:
                        result['ldra_handle'] = v6handle
                    if 'handle' not in kwargs:
                        # If mode is DHCPPD or DHCPV6ANDPD, we need to create the
                        # clients behind the home gateway
                        if 'PD' in dhcpv6_args['dhcp6_client_mode']:
                            print("DHCPv6 PD requested. Creating the clients behind the HG")
                            client_args = dict()
                            client_args['count'] = kwargs.get('num_sessions', 1)
                            client_args['mode'] = 'create'
                            client_args['port_handle'] = port_handle
                            client_args['encapsulation'] = 'ethernet_ii'
                            client_args['ip_version'] = 'ipv6'
                            client_args['link_local_ipv6_addr'] = 'fe80::'
                            client_config_status = rt_handle.invoke('emulation_device_config', **client_args)
                            if client_config_status['status'] != '1':
                                result['status'] = '0'
                                raise Exception("failed to add dhcpv6 client")
                            else:
                                client_handle = client_config_status['handle']
                            # Add the Home gateway link
                            home_gw_handle = config_status['dhcpv6_handle']
                            rt_handle.invoke('invoke', cmd='stc::perform ArpNdStart -HandleList {} '.format(home_gw_handle).strip())
                            link_args = dict()
                            link_args['link_src'] = client_handle
                            link_args['link_dst'] = home_gw_handle
                            link_args['link_type'] = 'Home_Gateway_Link'
                            link_create_status = rt_handle.invoke('link_config', **link_args)
                            if link_create_status['status'] != '1':
                                result['status'] = '0'
                                raise Exception("failed to add dhcpv6 client")
                            else:
                                rt_handle.homeGwToClientMap[v6handle] = client_handle
                                rt_handle.homeGwToClientMap[v6_host_handle] = client_handle

                        # End of mode DHCPPD/DHCPV6ANDPD client creation loop
                        rt_handle.dhcpv6_index += 1
                        rt_handle.device_to_dhcpv6_index[v6handle] = rt_handle.dhcpv6_index
                        rt_handle.dhcpv6_client_handle.append(v6handle)
                        rt_handle.handles[port]['dhcpv6_client_handle'].append(v6handle)
                        rt_handle.dhcpv6_client_device_handle.append(config_status['dhcpv6_handle'])

    else:
        if 'handle' in kwargs:
            if 'dhcp4_broadcast' in kwargs:
                rt_handle.invoke('invoke', cmd='stc::config {} -UseBroadcastFlag {}'.format(kwargs['handle'], kwargs['dhcp4_broadcast']))
        else:
            kwargs['ip_type'] = "ipv4"
            dhcp_args['dhcp_range_ip_type'] = '4'
            dhcpv4_args.update(dhcp_args)
            config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcpv4_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcp client")
            else:
                if 'handles' in config_status:
                    handle = config_status['handles']
                    result['dhcpv4_client_handle'] = handle
                    if 'handle' not in kwargs:
                        rt_handle.dhcpv4_client_handle.append(handle)
                        rt_handle.handles[port]['dhcpv4_client_handle'].append(handle)
                        #rt_handle.device_to_dhcpv4_index[handle] = rt_handle.dhcpv4_index


    if 'vlan_start' in kwargs or 'svlan_start' in kwargs:
        if 'handle' in kwargs:
            set_vlan(rt_handle, **kwargs)
        else:
            #kwargs['handle'] = device_status['handle']
            set_vlan(rt_handle, handle=device_status['handle'], **kwargs)


    # v4 Clients: Remote ID, Circuit ID and Vendor Class ID. Takes DHCPv4 block config
    # object as handle input.
    if 'remote_id' in kwargs or 'circuit_id' in kwargs or 'vendor_class_id' in kwargs:
        if 'handle' in kwargs:
            #kwargs['handle'] = block_config_handle
            if 'dual' in kwargs['ip_type'] and 'v4' not in kwargs['handle']:
                kwargs['handle'] = rt_handle.invoke('invoke', cmd='stc::get {} -children-dhcpv4blockconfig'.format(host_handle).strip())
            if not set_v4_option(rt_handle, **kwargs):
                result['status'] = '0'
        else:
            if not set_v4_option(rt_handle, handle=handle, **kwargs):
                result['status'] = '0'

    # v6 Clients: Interface ID, Remote ID and Enterprise ID. Takes DHCPv6 PD/NA block
    # config object as handle input.
    if 'interface_id' in kwargs or 'v6_remote_id' in kwargs or 'enterprise_id' in kwargs or 'dns_server' in kwargs:
        if 'handle' in kwargs:
            #kwargs['handle'] = block_config_handle
            if 'dual' in kwargs['ip_type'] and 'v6' not in kwargs['handle']:
                dual_v6_handle = rt_handle.invoke('invoke', cmd='stc::get {} -children-dhcpv6blockconfig'.format(host_handle).strip())
                if not dual_v6_handle:
                    dual_v6_handle = rt_handle.invoke('invoke', cmd='stc::get {} -children-dhcpv6pdblockconfig'.format(host_handle).strip())
                kwargs['handle'] = dual_v6_handle
            if not set_v6_option(rt_handle, **kwargs):
                result['status'] = '0'
        else:
            if not set_v6_option(rt_handle, handle=v6handle, **kwargs):
                result['status'] = '0'

    # create only, no modify
    if 'handle' not in kwargs and 'softgre' in kwargs:
        gre_args = dict()
        gre_args['mode'] = 'create'
        gre_args['gre_tnl_type'] = '4'
        gre_args['gre_port_handle'] = port_handle
        if 'gre_src_mac_addr' not in kwargs:
            gre_args['gre_src_mac_addr'] = '00:00:00:00:00:00'
        if 'gre_dst_ip' in kwargs:
            gre_args['gre_dst_addr'] = kwargs['gre_dst_ip']
        if 'gre_local_ip' in kwargs:
            gre_args['gre_src_addr'] = kwargs['gre_local_ip']
        if 'gre_gateway' in kwargs:
            gre_args['gre_tnl_addr'] = kwargs['gre_gateway']
        if 'gre_vlan_id' in kwargs:
            gre_args['gre_encapsulation'] = 'ethernet_ii_vlan'
            gre_args['gre_vlan_id'] = kwargs['gre_vlan_id']
            gre_args['gre_vlan_id_step'] = kwargs.get('gre_vlan_id_step', '1')
        if 'gre_netmask' in kwargs:
            gre_args['gre_prefix_len'] = kwargs['gre_netmask']
            if '.' in kwargs['gre_netmask']:
                binary = ''
                for seg in kwargs['gre_netmask'].split('.'):
                    binary += '{:0<8b}'.format(int(seg))
                gre_args['gre_prefix_len'] = binary.find('0')

        gre_handle = rt_handle.invoke('emulation_gre_config', **gre_args)

        link_args = dict()
        link_args['link_type'] = 'L2_GRE_Tunnel_Link'
        link_args['link_src'] = device_status['handle']
        link_args['link_dst'] = gre_handle
        link_status = rt_handle.invoke('link_config', **link_args)
        if link_status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to add link")

    return result




def set_dhcp_client(rt_handle, **kwargs):
    """
     release_rate='220', outstanding_releases_count='900',outstanding_session_count='1000', ip_version='4')
    :param rt_handle:                RT object
    :param kwargs:
    Mandatory:
     handle:                    dhcp client handle

    Optional:
    type:                       dhcpv4 or v6, can be used for setting login/logout rate only
    msg_timeout:                timeout for a msg like discover
    login_rate:                 request rate (must be a list for all the device/ports
    outstanding:                outstanding size for login(must be a list for all)
    logout_rate:                release rate(must be a list for all the device/ports)
    retry_count:                retry times for msg
    login_rate_mode:            starting scale mode (per port/per device)
    logout_rate_mode:           stop scale mode
    remote_id:                  option82 remote_id string
    remote_id_start:            remote id start number
    remote_id_step:             remote id step number
    remote_id_repeat:           remote id repeat number
    circuit_id:                 option82 circuit id string
    circuit_id_start:           circuit id start number
    circuit_id_step:            circuit id step number
    circuit_id_repeat:          circuit id repeat number
    v6_remote_id:               v6 option 38 remote id string
    v6_remote_id_start:         remote id start number
    v6_remote_id_step:          remote id step number
    v6_remote_id_repeat:        remote id repeat number
    enterprise_id:              v6 enterprise vendor id, used with remote id
    enterprise_id_step:         enterprise id increase step
    interface_id:               v6 option 17 interface id string
    interface_id_start:         v6 interface id start number
    interface_id_step:          v6 interface id step number
    interface_id_repeat:        v6 interface id repeat number

    :return:
    status                      1 or 0
    """

    status = '1'
    if not ('handle' in kwargs or 'type' in kwargs):
        raise Exception("dhcp handle or type  must be provided")
    dhcp_args = dict()
    args = dict()

    if 'login_rate' in kwargs:
        args['request_rate'] = kwargs.get('login_rate')
    if 'logout_rate' in kwargs:
        args['release_rate'] = kwargs['logout_rate']
    if 'outstanding' in kwargs:
        args['outstanding_session_count'] = kwargs.get('outstanding')

    if 'v4' in kwargs['handle']:
        if 'msg_timeout' in kwargs:
            dhcp_args['msg_timeout'] = kwargs['msg_timeout']
        if 'retry_count' in kwargs:
            dhcp_args['retry_count'] = kwargs['retry_count']
    if 'v6' in kwargs['handle']:
        if 'msg_timeout' in kwargs:
            # rebind
            dhcp_args['dhcp6_reb_max_rt'] = kwargs['msg_timeout']
            # renew
            dhcp_args['dhcp6_ren_max_rt'] = kwargs['msg_timeout']
            # request
            dhcp_args['dhcp6_req_max_rt'] = kwargs['msg_timeout']
            # solicit
            dhcp_args['dhcp6_sol_max_rt'] = kwargs['msg_timeout']
            # info-req
            dhcp_args['dhcp6_inforeq_max_rt'] = kwargs['msg_timeout']
            # confirm
            dhcp_args['dhcp6_cfm_max_rt'] = kwargs['msg_timeout']
        if 'retry_count' in kwargs:
            # release
            dhcp_args['dhcp6_rel_max_rc'] = kwargs['retry_count']
            # info-req
            dhcp_args['dhcp6_req_max_rc'] = kwargs['retry_count']
            # solicit
            dhcp_args['dhcp6_sol_max_rc'] = kwargs['retry_count']
            # decline
            dhcp_args['dhcp6_dec_max_rc'] = kwargs['retry_count']

    if dhcp_args or args:
        port_list = []
        if 'v4' in kwargs['handle']:
            dhcp_args['ip_version'] = '4'
            for item in rt_handle.dhcpv4_client_handle:
                for elem in rt_handle.handles.values():
                    if item in elem['dhcpv4_client_handle']:
                        port_list.append(elem['port_handle'])
        if 'v6' in kwargs['handle']:
            dhcp_args['ip_version'] = '6'
            for item in rt_handle.dhcpv6_client_handle:
                for elem in rt_handle.handles.values():
                    if item in elem['dhcpv6_client_handle']:
                        port_list.append(elem['port_handle'])

        dhcp_args['mode'] = "create"
        i = 0
        for port in port_list:
            dhcp_args['port_handle'] = port
            if 'v4' in kwargs['handle']:
                dhcp_args['request_rate'] = args['request_rate'][i]
                dhcp_args['release_rate'] = args['release_rate'][i]
                dhcp_args['outstanding_session_count'] = args['outstanding_session_count'][i]
            if 'v6' in kwargs['handle']:
                dhcp_args['dhcp6_request_rate'] = args['request_rate'][i]
                dhcp_args['dhcp6_release_rate'] = args['release_rate'][i]
                dhcp_args['dhcp6_outstanding_session_count'] = args['outstanding_session_count'][i]
            config_status = rt_handle.invoke('emulation_dhcp_config', **dhcp_args)
            if config_status['status'] != '1':
                status = '0'
                raise Exception("failed to change dhcp client {}".format(kwargs['handle']))
            i = i + 1
    else:
        return rt_handle.add_dhcp_client(**kwargs)

    return status



def set_dhcp_rate(rt_handle, **kwargs):
    """
    :param rt_handle:                RT object
    :param kwargs:
    Mandatory:
     handle:                    dhcp client handle

    Optional:
    type:                       dhcpv4 or v6, can be used for setting login/logout rate only
    msg_timeout:                timeout for a msg like discover
    login_rate:                 request rate (must be a list for all the device/ports
    outstanding:                outstanding size for login(must be a list for all)
    logout_rate:                release rate(must be a list for all the device/ports)
    retry_count:                retry times for msg
    login_rate_mode:            starting scale mode (per port/per device)
    logout_rate_mode:           stop scale mode

    :return:
    result                      dictionary of status
    """

    if 'handle' not in kwargs:
        raise Exception("dhcp handle must be provided")
    dhcp_args = dict()


    dhcp_args['mode'] = 'modify'

    # ixia can itemize per group of subscribers under under a port
    #  where spirent can only set the call login and logout rates on the port level
    #  thereby, we select the minimum rates specified in the bbeconfig yaml file
    if 'login_rate' in kwargs:
        min_call_login_rate = min(kwargs['login_rate'])
        if 'v4' in kwargs['handle']:
            dhcp_args['request_rate'] = str(min_call_login_rate)
        else:
            dhcp_args['dhcp6_request_rate'] = str(min_call_login_rate)

    if 'logout_rate' in kwargs:
        min_call_logout_rate = min(kwargs['logout_rate'])
        if 'v4' in kwargs['handle']:
            dhcp_args['release_rate'] = str(min_call_logout_rate)
        else:
            dhcp_args['dhcp6_release_rate'] = str(min_call_logout_rate)

    if 'outstanding' in kwargs:
        min_call_outstanding = min(list(map(int, (kwargs['outstanding']))))
        if 'v4' in kwargs['handle']:
            dhcp_args['outstanding_session_count'] = str(min_call_outstanding)
        else:
            dhcp_args['dhcp6_outstanding_session_count'] = str(min_call_outstanding)

    if 'msg_timeout' in kwargs:
        min_call_msg_timeOut = str(min(kwargs['msg_timeout']))
        if 'v4' in kwargs['handle']:
            dhcp_args['msg_timeout'] = min_call_msg_timeOut
        else:
            # rebind
            dhcp_args['dhcp6_reb_max_rt'] = min_call_msg_timeOut
            # renew
            dhcp_args['dhcp6_ren_max_rt'] = min_call_msg_timeOut
            # request
            dhcp_args['dhcp6_req_max_rt'] = min_call_msg_timeOut
            # solicit
            dhcp_args['dhcp6_sol_max_rt'] = min_call_msg_timeOut
            # info-req
            dhcp_args['dhcp6_inforeq_max_rt'] = min_call_msg_timeOut
            # confirm
            dhcp_args['dhcp6_cfm_max_rt'] = min_call_msg_timeOut

    if 'retry_count' in kwargs:
        min_call_retry_count = str(min(kwargs['retry_count']))
        if 'v4' in kwargs['handle']:
            dhcp_args['retry_count'] = min_call_retry_count
        else:
            # release
            dhcp_args['dhcp6_rel_max_rc'] = min_call_retry_count
            # info-req
            dhcp_args['dhcp6_req_max_rc'] = min_call_retry_count
            # solicit
            dhcp_args['dhcp6_sol_max_rc'] = min_call_retry_count
            # decline
            dhcp_args['dhcp6_dec_max_rc'] = min_call_retry_count

    if 'handle' in kwargs:
        host_instance = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle'] + " -parent")
        port_instance = rt_handle.invoke('invoke', cmd="stc::get "+host_instance+" -affiliationport-targets")
        # Set the handle
        if 'v4' in kwargs['handle']:
            dhcp_args['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+port_instance+" -children-dhcpv4portconfig")
            dhcp_args['port_handle'] = port_instance
        elif 'v6' in kwargs['handle']:
            dhcp_args['ip_version'] = "6"
            dhcp_args['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+port_instance+" -children-dhcpv6portconfig")
        result = rt_handle.invoke('emulation_dhcp_config', **dhcp_args)


    return result


def dhcp_client_action(rt_handle, **kwargs):
    """
    :param rt_handle:        RT object
    :param kwargs:
    port_handle:        specify a port handle to login all the clients?
    handle:             dhcp handles
    action:             start, stop, renew, abort, restart_down
    :return:
    result              dictionary include status and log message

    #rt.dhcp_client_action(handle=rt.handles['1/1']['dhcpv4_client_handle'][0], action='bind')
    #rt.dhcp_client_action(port_handle='1/1/1', action='bind')
    """
    result = dict()
    dhcp_args = dict()
    result['status'] = '1'
    if 'handle' not in kwargs or 'action' not in kwargs:
        print("mandatory params 'handle/action' not provided ")
        result['status'] = '0'
    else:
        dhcp_args['handle'] = kwargs['handle']
        dhcp_args['action'] = kwargs['action']
        if 'restart' in kwargs['action']:
            # Spirent does not have an option to restart unbound
            # client emulations. However, issuing a bind works for
            # this scenario.
            dhcp_args['action'] = 'bind'
        elif 'start' in kwargs['action']:
            dhcp_args['action'] = 'bind'
        elif 'stop' in kwargs['action']:
            dhcp_args['action'] = 'release'
        # ip_version is needed to figure out if we need to start DHCPv4 client
        # or DHCPv6 client. By default, we start DHCPv4 clients.
        if 'ip_version' not in kwargs:
            if 'dhcpv6' in kwargs['handle']:
                dhcp_args['ip_version'] = '6'
                # Observation:
                # emulation_dhcp_control API for DHCPv6 is not able to start the DHCPv6 clients
                # if the handle is dhcpv6blockconfig1. It starts the DHCPv6 clients if the handle
                # is host or emulateddevice. Hence, for DHCPv6 client emulation, we query for the
                # host or emulateddevice handle and set is dhcp_args['handle']. Mo issue observed
                # with DHCPv4.
                dhcp_args['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+dhcp_args['handle']+" -parent")
            else:
                dhcp_args['ip_version'] = '4'
        else:
            dhcp_args['ip_version'] = kwargs['ip_version']

        result = rt_handle.invoke('emulation_dhcp_control', **dhcp_args)
    return result


def dhcp_client_stats(rt_handle, **kwargs):
    """
    :param rt_handle:        RT object
    :param kwargs:
    port_handle:        specify a port handle to get the aggregated stats
    handle:             specify a dhcp handle to get the stats
    dhcp_version:       dhcp4/dhcp6
    execution_timeout   specify the timeout for the command
    mode:               aggregate_stats/session
    :return:            dictionary

    Example calls:
    dhcp_client_stats(rt_handle,mode='session',handle=blk_cfg,ip_version='4')
    dhcp_client_stats(rt_handle,mode='session',handle=Dhcpv6hHost,ip_version='6')
    """

    if 'handle' not in kwargs:
        raise ValueError('handle is a mandatory argument to the dhcp_client_stats API')
    if 'ip_version' not in kwargs:
        raise ValueError('ip_version is a mandatory argument to the dhcp_client_stats API')

    result_mode = kwargs.get('mode', 'session')

    return rt_handle.invoke('emulation_dhcp_stats', **{'mode':result_mode, 'ip_version':kwargs['ip_version'], 'handle':kwargs['handle']})

def get_pppoe_config(rt_handle, **kwargs):
    """
    Get common pppoe configuration to create or modify
    """
    pppoe_args = dict()

    if 'num_sessions' in kwargs:
        pppoe_args['num_sessions'] = kwargs['num_sessions']
    pppoe_args['encap'] = 'ethernet_ii'
    if 'vlan_start' in kwargs:
        pppoe_args['encap'] = 'ethernet_ii_vlan'
    if 'svlan_start' in kwargs:
        pppoe_args['encap'] = 'ethernet_ii_qinq'
    if 'auth_req_timeout' in kwargs:
        pppoe_args['auth_req_timeout'] = kwargs['auth_req_timeout']
    if 'echo_req' in kwargs:
        pppoe_args['echo_req'] = kwargs['echo_req']
    if 'ip_type' in kwargs:
        if 'v4' in kwargs['ip_type']:
            pppoe_args['ip_cp'] = 'ipv4_cp'
        if 'v6' in kwargs['ip_type']:
            pppoe_args['ip_cp'] = 'ipv6_cp'
        if 'dual' in kwargs['ip_type']:
            pppoe_args['ip_cp'] = 'ipv4v6_cp'

    if 'ipcp_req_timeout' in kwargs:
        pppoe_args['ipcp_req_timeout'] = kwargs['ipcp_req_timeout']
    if 'max_auth_req' in kwargs:
        pppoe_args['max_auth_req'] = kwargs['max_auth_req']
    if 'max_padi_req' in kwargs:
        pppoe_args['max_padi_req'] = kwargs['max_padi_req']
    if 'max_padr_req' in kwargs:
        pppoe_args['max_padr_req'] = kwargs['max_padr_req']
    if 'max_ipcp_retry' in kwargs:
        pppoe_args['max_ipcp_req'] = kwargs['max_ipcp_retry']
    if 'max_terminate_req' in kwargs:
        pppoe_args['max_terminate_req'] = kwargs['max_terminate_req']
    if 'echo_req_interval' in kwargs:
        pppoe_args['echo_req_interval'] = kwargs['echo_req_interval']
    if 'auth_mode' in kwargs:
        pppoe_args['auth_mode'] = kwargs['auth_mode']
    if 'agent_circuit_id' in kwargs:
        pppoe_args['intermediate_agent'] = 1
        pppoe_args['agent_type'] = 'dsl'
    if 'agent_remote_id' in kwargs:
        pppoe_args['intermediate_agent'] = 1
        pppoe_args['agent_type'] = 'dsl'

    return pppoe_args

def set_pppox_wildcard(rt_handle, pppox_handle, **kwargs):
    """
    set pppox arguments with wildcard by Native API
    :param rt_handle:        RT object
    :pppox_handle       pppoxclientblockhandle
    :param kwargs:
    """
    if not re.match('pppo.clientblockconfig', pppox_handle):
        raise Exception('pppoxclientblockconfig handle is needed: {}'.format(pppox_handle))

    status = '1'
    args = ''
    if 'auth_mode' in kwargs:
        if 'username' in kwargs:
            username = kwargs['username'].replace('?', '@x(1,0,1,0,0)')
            args += ' -Username {{{}}} '.format(username)
        if 'password' in kwargs:
            password = kwargs['password']
            args += ' -Password {{{}}} '.format(password)

    if 'agent_circuit_id' in kwargs:
        agent_circuit_id = kwargs['agent_circuit_id'].replace('?', '@x(1,0,1,0,0)')
        args += ' -CircuitId {{{}}} '.format(agent_circuit_id)

    if 'agent_remote_id' in kwargs:
        agent_remote_id = kwargs['agent_remote_id'].replace('?', '@x(1,0,1,0,0)')
        args += ' -RemoteOrSessionId {{{}}} '.format(agent_remote_id)

    if args:
        rt_handle.invoke('invoke', cmd='stc::config {} {}'.format(pppox_handle, args))

    return status

def add_pppoe_client(rt_handle, **kwargs):
    """
    :param rt_handle:               RT object
    :param kwargs:
    port:                      specify a port  for creating a simulation
    num_sessions:              specify the simulation count

    auth_req_timeout:          authentication request timeout
    echo_req:                  echo request 1 or 0
    #echo_rsp:                  echo response 1 or 0    # not supported by Spirent HLTAPI
    ip_type:                    v4/dual/v6
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    svlan_length:               svlan sequence length
    agent_remote_id:            agent_remote_id string, for example can be "remoteid" or "remoteid?"
    agent_circuit_id:           agent_circuit_id string
    auth_mode:                  authentication mode: pap/chap/pap_or_chap
    username:                   ppp username
    password:                   ppp password
    ipcp_req_timeout:           ipcp request timeout
    max_auth_req:               maximum authentication requests
    max_padi_req:               maximum PADI requests
    max_padr_req:               maximum PADR requests
    max_ipcp_retry:             maximum ipcp retry
    max_terminate_req:          maximum terminate requests
    echo_req_interval:          echo requests interval
    dhcpv6_ia_type:             dhcpv6 ia type: iapd/iana/iana_iapd

    :return:
    result:                     dictionary of status, pppox_client_handle, dhcpv6_client_handle
    """
    result = dict()
    result['status'] = '1'
    #config_status = dict()
    pppoe_args = dict()
    dhcpv6_args = dict()
    if 'port' in kwargs:
        port = kwargs.get('port')
        port_handle = rt_handle.port_to_handle_map[port]
        pppoe_args['port_handle'] = port_handle
        pppoe_args['mode'] = 'create'
        pppoe_args.update(get_pppoe_config(rt_handle, **kwargs))

    if 'handle' in kwargs:
        pppoe_args['handle'] = kwargs['handle']
        pppox_handle = kwargs['handle']
        if re.match('pppo.clientblockconfig', pppoe_args['handle']):
            # device handle for modify mode
            pppoe_args['handle'] = rt_handle.invoke('invoke', cmd='stc::get ' + pppoe_args['handle'] + ' -parent').strip()
        pppoe_args['mode'] = 'modify'
        pppoe_args.update(get_pppoe_config(rt_handle, **kwargs))

    if 'vlan_start' in kwargs:
        pppoe_args['encap'] = 'ethernet_ii_vlan'
    if 'svlan_start' in kwargs:
        pppoe_args['encap'] = 'ethernet_ii_qinq'
    if 'encapsulation' in kwargs:
        pppoe_args['encap'] = kwargs['encapsulation']


    config_status = rt_handle.invoke('pppox_config', **pppoe_args)

    if config_status['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to add/modify pppoe client for port {}".format(port))
    else:
        result['device_group_handle'] = config_status['handle']
        handle = config_status['handle']
        result['ethernet_handle'] = rt_handle.invoke('invoke', cmd='stc::get ' + config_status['handle'] + ' -children-ethiiif')
        result['ethernet_handle'] = result['ethernet_handle'].strip()

        # native API for chap and pap_or_chap
        auth_args = ''
        if pppoe_args['auth_mode'] == 'chap':
            if 'auth_req_timeout' in pppoe_args:
                auth_args += ' -ChapChalRequestTimeout ' + str(pppoe_args['auth_req_timeout'])
            if 'max_auth_req' in pppoe_args:
                auth_args += ' -MaxChapRequestReplyAttempts ' + str(pppoe_args['max_auth_req'])
            auth_args += ' -Authentication CHAP_MD5'
        if pppoe_args['auth_mode'] == 'pap':
            if 'auth_req_timeout' in pppoe_args:
                auth_args += ' -PapRequestTimeout ' + str(pppoe_args['auth_req_timeout'])
            if 'max_auth_req' in pppoe_args:
                auth_args += ' -MaxPapRequestAttempts ' + str(pppoe_args['max_auth_req'])
            auth_args += ' -Authentication PAP'
        if pppoe_args['auth_mode'] == 'pap_or_chap':
            if 'auth_req_timeout' in pppoe_args:
                auth_args += ' -PapRequestTimeout ' + str(pppoe_args['auth_req_timeout']) + ' -ChapChalRequestTimeout ' + str(pppoe_args['auth_req_timeout'])
            if 'max_auth_req' in pppoe_args:
                auth_args += ' -MaxPapRequestAttempts ' + str(pppoe_args['max_auth_req']) + ' -MaxChapRequestReplyAttempts ' + str(pppoe_args['max_auth_req'])
            auth_args += ' -Authentication AUTO'
        if auth_args:
            rt_handle.invoke('invoke', cmd='stc::config ' + config_status['pppoe_session'] + " " + auth_args)
        # set wildcard options
        if 'handle' in kwargs:
            #rt_handle.set_pppox_wildcard(pppox_handle=pppox_handle, **kwargs)
            set_pppox_wildcard(rt_handle, pppox_handle=pppox_handle, **kwargs)
        else:
            #rt_handle.set_pppox_wildcard(pppox_handle=config_status['pppoe_session'], **kwargs)
            set_pppox_wildcard(rt_handle, pppox_handle=config_status['pppoe_session'], **kwargs)
        # enable dhcpv6
        if 'handle' not in kwargs and \
           'dhcpv6_ia_type' in kwargs and \
           'ip_type' in kwargs and \
           ('v6' in kwargs['ip_type'] or 'dual' in kwargs['ip_type']):
            dhcpv6_args['dhcp_range_ip_type'] = 6
            #dhcpv6_sth_type = {'IANA':'DHCPV6', 'IAPD':'DHCPPD', 'IANA_IAPD':'DHCPV6ANDPD'}
            # kwargs['dhcpv6_ia_type'] getting default as IANA_IAPD .As per Bojan suggestion changed DHCPV6ANDPD to DHCPPD
            dhcpv6_sth_type = {'IANA':'DHCPV6', 'IAPD':'DHCPPD', 'IANA_IAPD':'DHCPPD'}
            dhcpv6_args['dhcp6_client_mode'] = dhcpv6_sth_type.get(kwargs.get('dhcpv6_ia_type', 'IAPD').upper())
            dhcpv6_args['mode'] = 'enable'
            dhcpv6_args['handle'] = config_status['handle']
            dhcpv6_args['encap'] = pppoe_args['encap']
            dhcpv6_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcpv6_args)
            if dhcpv6_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to enable dhcpv6 on pppox client")
            else:
                if 'handles' in dhcpv6_status:
                    v6handle = dhcpv6_status['handles']
                    v6_host_handle = dhcpv6_status['dhcpv6_handle']
                    result['dhcpv6_client_handle'] = v6handle
                    if 'handle' not in kwargs:
                        # If mode is DHCPPD or DHCPV6ANDPD, we need to create the
                        # clients behind the home gateway
                        if 'PD' in dhcpv6_args['dhcp6_client_mode']:
                            print("DHCPv6 PD requested. Creating the clients behind the HG")
                            client_args = dict()
                            client_args['count'] = kwargs.get('num_sessions', 1)
                            client_args['mode'] = 'create'
                            client_args['port_handle'] = port_handle
                            client_args['encapsulation'] = 'ethernet_ii'
                            client_args['ip_version'] = 'ipv6'
                            client_args['link_local_ipv6_addr'] = 'fe80::'
                            client_config_status = rt_handle.invoke('emulation_device_config', **client_args)
                            if client_config_status['status'] != '1':
                                result['status'] = '0'
                                raise Exception("failed to add dhcpv6 client")
                            else:
                                client_handle = client_config_status['handle']
                            # Add the Home gateway link
                            home_gw_handle = dhcpv6_status['dhcpv6_handle']
                            #rt_handle.invoke('invoke', cmd='stc::perform ArpNdStart -HandleList {} ' .format(home_gw_handle)).strip()
                            link_args = dict()
                            link_args['link_src'] = client_handle
                            link_args['link_dst'] = home_gw_handle
                            link_args['link_type'] = 'Home_Gateway_Link'
                            link_create_status = rt_handle.invoke('link_config', **link_args)
                            if link_create_status['status'] != '1':
                                result['status'] = '0'
                                raise Exception("failed to add dhcpv6 client")
                            else:
                                rt_handle.homeGwToClientMap[v6handle] = client_handle
                                rt_handle.homeGwToClientMap[v6_host_handle] = client_handle

                        # End of mode DHCPPD/DHCPV6ANDPD client creation loop
                        rt_handle.dhcpv6_index += 1
                        rt_handle.device_to_dhcpv6_index[v6handle] = rt_handle.dhcpv6_index
                        rt_handle.dhcpv6_client_handle.append(v6handle)
                        rt_handle.handles[port]['dhcpv6_client_handle'].append(v6handle)
                        rt_handle.dhcpv6_client_device_handle.append(dhcpv6_status['dhcpv6_handle'])


        # set vlan
        if 'vlan_start' in kwargs or 'svlan_start' in kwargs:
            if 'handle' in kwargs:
                set_vlan(rt_handle, __set_vlan_no_default=1, **kwargs)
            else:
                set_vlan(rt_handle, handle=config_status['handle'], **kwargs)
        if 'pppoe_session' in config_status:
            handle = config_status['pppoe_session']
            result['pppox_client_handle'] = handle
            if 'handle' not in kwargs:
                rt_handle.pppox_client_handle.append(handle)
                rt_handle.handles[port]['pppox_client_handle'].append(handle)
                rt_handle.pppox_client_device_handle.append(result['device_group_handle'])
            if 'handle' not in kwargs and 'ip_type' in kwargs and 'dhcpv6_ia_type' in kwargs:
                if 'v6' in kwargs['ip_type'] or 'dual' in kwargs['ip_type']:
                    v6handle = dhcpv6_status['handles']
                    if v6handle not in rt_handle.dhcpv6_client_handle:
                        rt_handle.dhcpv6_client_handle.append(v6handle)
                    result['dhcpv6_client_handle'] = v6handle
                    rt_handle.handles[port]['dhcpv6_over_pppox_handle'][handle] = v6handle
                    #rt_handle.dhcpv6_client_device_handle.append(config_status['dhcpv6_handle'])
        # Configure Relay agent
        if 'remote_id' in kwargs or 'circuit_id' in kwargs:
            if 'handle' in kwargs:
                kwargs['handle'] = kwargs['handle']
                if 'dual' in kwargs['ip_type'] and 'v4' not in kwargs['handle']:
                    kwargs['handle'] = rt_handle.invoke('invoke', cmd='stc::get '+handle+' -children-PppoeClientBlockConfig')
                if not set_option_82(rt_handle, **kwargs):
                    result['status'] = '0'
            else:
                kwargs['handle'] = handle
                if not set_option_82(rt_handle, **kwargs):
                    result['status'] = '0'

        # Configure ANCP Subscriber line
        #if re.match('host|router|emulateddevice', rt_handle.ancp_handle):
        #    line_args = dict()
        #    line_args = rt_handle.ancp_line_args
        #    line_args['handle'] = config_status['handle']
        #    add_ancp_subscriber_lines_config(rt_handle, **line_args)

    return result


def set_pppoe_client(rt_handle, **kwargs):
    """
    :param rt_handle:                RT object
    :param kwargs:
    handle:                     specify a pppox handle
    num_sessions:               specify the simulation count
    auth_req_timeout:           authentication request timeout
    echo_req:                   echo request 1 or 0
    #echo_rsp:                   echo response 1 or 0   # not supported by Spirent HLTAPI
    type:                       v4/dual/v6
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    vlan_length:                svlan sequence length
    agent_remote_id:            agent_remote_id string, for example can be "remoteid" or "remoteid?"
    agent_circuit_id:           agent_circuit_id string
    auth_mode:                  authentication mode: pap/chap/pap_or_chap
    ipcp_req_timeout:           ipcp request timeout
    max_auth_req:               maximum authentication requests
    max_padi_req:               maximum PADI requests
    max_padr_req:               maximum PADR requests
    max_ipcp_retry:             maximum ipcp retry
    max_terminate_req:          maximum terminate requests
    echo_req_interval:          echo requests interval
    login_rate:                 login rate
    outstanding:                outstanding size for login
    logout_rate:                logout rate
    :return:
    """
    if not ('login_rate' in kwargs or 'logout_rate' in kwargs):
        status = rt_handle.add_pppoe_client(**kwargs)
        return status

    else:
    ##set the login/logout rate
        status = '1'
        pppox_args = dict()
        pppox_args['mode'] = 'modify'

        i = 0
        for host in rt_handle.pppox_client_device_handle:
            # get vlan type because '-encap' is mandatory
            vlan_objs = rt_handle.invoke('invoke', cmd='stc::get ' + host + ' -children-vlanif').strip()    #BOJAN
            if vlan_objs != '':
                encap_map = {1:'ethernet_ii_vlan', 2:'ethernet_ii_qinq'}
                vlan_num = len(vlan_objs.split())
                pppox_args['encap'] = encap_map.get(vlan_num, 'ethernet_ii_mvlan')
            else:
                pppox_args['encap'] = 'ethernet_ii'

            pppox_args['handle'] = host
            if 'login_rate' in kwargs:
                pppox_args['attempt_rate'] = kwargs['login_rate'][i]
            if 'logout_rate' in kwargs:
                pppox_args['disconnect_rate'] = kwargs['logout_rate'][i]
            if 'outstanding' in kwargs:
                pppox_args['max_outstanding'] = kwargs['outstanding'][i]
            i = i + 1

            result = rt_handle.invoke('pppox_config', **pppox_args)
            if result['status'] != '1':
                status = '0'
        return status



def pppoe_client_action(rt_handle, **kwargs):
    """
    login/logout pppoe client
    :param rt_handle:            RT object
    :param kwargs:
    handle:                 pppox handles/ dhcpv6 over pppox handle
    action:                 start, stop, restart, reset, abort
    :return:
    status
    """
    result = dict()
    result['status'] = '1'
    pppoe_args = dict()

    if 'action' not in kwargs or 'handle' not in kwargs:
        print("mandatory params 'handle/action' not provided ")
        result['status'] = '0'
    else:
        if isinstance(kwargs['handle'], str):
            pppoe_args['handle'] = rt_handle.invoke('invoke', cmd='stc::get ' + kwargs['handle'] + ' -parent')
        else:
            pppoe_args['handle'] = []
            for hnd in kwargs['handle']:
                pppoe_args['handle'].append(rt_handle.invoke('invoke', cmd='stc::get ' + hnd + ' -parent'))

        pppoe_args['action'] = kwargs.get('action')
        if 'restart' in kwargs['action']:
            #pppoe_args['action'] = 'connect'
            pppoe_args['action'] = 'retry'
        elif 'start' in kwargs['action']:
            pppoe_args['action'] = 'connect'
        elif 'stop' in kwargs['action']:
            if 'dhcpv6' in kwargs['handle']:
                #Stop DHCPv6 now. Call dhcp_client_action
                result = dhcp_client_action(rt_handle, **kwargs)
                # Sleep for some time so that DHCP comes Down
                sleep(10)
                pppoe_args['action'] = 'disconnect'
            else:
                pppoe_args['action'] = 'disconnect'

        result = rt_handle.invoke('pppox_control', **pppoe_args)
        if 'dhcpv6' in (kwargs['handle']) and 'start' in kwargs['action']:
            # Sleep for some time so that PPP comes up
            sleep(60)
            # Start DHCPv6 now. Call dhcp_client_action
            result = dhcp_client_action(rt_handle, **kwargs)

    return result

def set_pppoe_rate(rt_handle, **kwargs):
    """
    :param rt_handle:                RT object
    :param kwargs:
    handle:                     specify a pppox handle
    login_rate:                 login rate
    outstanding:                outstanding size for login
    logout_rate:                logout rate
    :return:
    """
    if not ('login_rate' in kwargs or 'logout_rate' in kwargs):
        #status = rt_handle.pppox_config(mode='modify', **kwargs)
        status = rt_handle.invoke('pppox_config', mode='modify', **kwargs)
        return status

    else:
    ##set the login/logout rate
    # ixia can itemize per group of subscribers under under a port
    #  where spirent can only set the call login and logout rates on the port level
    #  thereby, we select the minimum rates specified in the bbeconfig yaml file
        pppox_args = dict()
        #pppox_args['port_role'] = "access"
        pppox_args['mode'] = 'modify'
        if 'login_rate' in kwargs:
            min_call_login_rate = min(kwargs['login_rate'])
            pppox_args['attempt_rate'] = str(min_call_login_rate)
        if 'logout_rate' in kwargs:
            min_call_logout_rate = min(kwargs['logout_rate'])
            pppox_args['disconnect_rate'] = str(min_call_logout_rate)
        if 'outstanding' in kwargs:
            min_call_outstanding = min(list(map(int, (kwargs['outstanding']))))
            pppox_args['max_outstanding'] = str(min_call_outstanding)
        if 'handle' in kwargs:
            pppox_args['encap'] = 'ethernet_ii_vlan'
            pppox_args['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -parent")
            result = rt_handle.invoke('pppox_config', **pppox_args)
        return result

def pppoe_client_stats(rt_handle, **kwargs):
    """
    get statistics for pppoe client
    :param rt_handle:                RT object
    :param kwargs:
    port_handle:                port handle used to retrieve the statistics
    handle:                     pppox handle used to retrieve the statistics
    mode:                       aggregate /session /session all
    execution_timeout:          the execution timeout setting, default is 1800
    :return:
    status
    """
    status = rt_handle.invoke('pppox_stats', **kwargs)
    return status


def add_link(rt_handle, **kwargs):
    """
    :param rt_handle:                RT object
    :param kwargs:
    port                        physical tester port
    vlan_id                     link vlan id
    vlan_id_step
    svlan_id
    svlan_id_step
    ip_addr
    ip_addr_step
    mask
    gateway
    ipv6_addr
    ipv6_addr_step
    ipv6_prefix_length
    ipv6_gateway
    gre_dst_ip
    gre_dst_ip_step
    count

    :return:
    device group handle
    ethernet handle
    ip handle
    gre handle
    """
    if 'port' not in kwargs:
        raise Exception("port is mandatory when adding link device")
    port = kwargs.get('port')
    port_handle = rt_handle.port_to_handle_map[port]
    count = kwargs.get('count', '1')
    #intf_args = dict()
    gre_args = dict()
    result = dict()
    result['status'] = '1'

    #create device group first
    link_args = {}
    link_args['mode'] = 'config'
    link_args['create_host'] = 'true'
    link_args['port_handle'] = port_handle
    # Commenting below port level load parameters. All load parameters need to be set at SB level
    #link_args['scheduling_mode'] = 'PORT_BASED'
    #link_args['port_loadunit'] = 'PERCENT_LINE_RATE'
    #link_args['port_load'] = '10'
    link_args['autonegotiation'] = '1'
    link_args['control_plane_mtu'] = kwargs.get('mtu', '1500')

    #Add Vlan Procedure
    if 'vlan_start' in kwargs:
        link_args['vlan_id'] = kwargs.get('vlan_start')
        link_args['vlan'] = '1'
        link_args['vlan_id_step'] = kwargs.get('vlan_step', '1')
        link_args['vlan_id_count'] = kwargs.get('vlan_count', count)

    if 'vlan_id' in kwargs:
        link_args['vlan_id'] = kwargs.get('vlan_id')
        link_args['vlan'] = '1'
        link_args['vlan_id_step'] = kwargs.get('vlan_id_step', '1')
        link_args['vlan_id_count'] = kwargs.get('vlan_id_count', count)

    #Add svaln Procedure
    if 'svlan_start' in kwargs:
        link_args['qinq_incr_mode'] = 'both'
        link_args['vlan_outer_id'] = kwargs['svlan_start']
        link_args['vlan_outer_id_step'] = kwargs.get('svlan_step', '1')
        link_args['vlan_outer_id_count'] = kwargs.get('svlan_count', count)
        link_args['vlan'] = '1'
        link_args['vlan_id'] = kwargs.get('vlan_start', '1')
        link_args['vlan_id_step'] = kwargs.get('vlan_step', '1')
        link_args['vlan_id_count'] = kwargs.get('vlan_count', count)

    if 'svlan_id' in kwargs:
        link_args['qinq_incr_mode'] = 'both'
        link_args['vlan_outer_id'] = kwargs['svlan_id']
        link_args['vlan_outer_id_step'] = kwargs.get('svlan_id_step', '1')
        link_args['vlan_outer_id_count'] = kwargs.get('svlan_id_count', count)
        link_args['vlan'] = '1'
        link_args['vlan_id'] = kwargs.get('vlan_id', '1')
        link_args['vlan_id_step'] = kwargs.get('vlan_id_step', '1')
        link_args['vlan_id_count'] = kwargs.get('vlan_id_count', count)
    if 'vlan_user_priority' in kwargs:
        link_args['vlan_user_priority'] = kwargs.get('vlan_user_priority')
    if 'vlan_user_priority_step' in kwargs:
        print('vlan_user_priority_step is not supported in HltApi!')
    #link_args['vlan_user_priority_step'] = kwargs.get('vlan_user_priority_step', '1')

    # create ethernet

    #set up ipv4 addr
    if 'ip_addr' in kwargs:
        link_args['intf_ip_addr'] = kwargs['ip_addr']
        link_args['intf_ip_addr_step'] = kwargs.get('ip_addr_step', '0.0.0.1')
        if 'gateway' in kwargs:
            link_args['gateway'] = kwargs['gateway']
            link_args['gateway_step'] = kwargs.get('ip_addr_step', '0.0.0.1')
        if 'netmask' in kwargs:
            link_args['netmask'] = kwargs['netmask']
    #set up ipv6 addr
    if 'ipv6_addr' in kwargs:
        link_args['ipv6_intf_addr'] = kwargs['ipv6_addr']
        link_args['ipv6_intf_addr_step'] = kwargs.get('ipv6_addr_step', '00:00:00:01:00:00:00:00')
        if 'ipv6_gateway' in kwargs:
            link_args['ipv6_gateway'] = kwargs['ipv6_gateway']
            link_args['ipv6_gateway_step'] = kwargs.get('ipv6_addr_step', '00:00:00:01:00:00:00:00')
        if 'ipv6_prefix_length' in kwargs:
            link_args['ipv6_prefix_length'] = kwargs.get('ipv6_prefix_length', '64')
    #Remove Condition for only Vlan Configuration
    status_config = rt_handle.invoke('interface_config', **link_args)
    device_group_handle = status_config['handles']

    if status_config['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to add device group for port {}".format(port))
    #if status_config['status'] != '1':
    #    result['status'] = '0'
    #    raise Exception("failed to add ethernet for device group {}".format(device_group_handle))
    #if status_config['status'] != '1':
    #    result['status'] = '0'
    #    raise Exception("failed to add ip/ipv6 address for ethernet {}".format(ethernet_handle))
    else:
        rt_handle.device_group_handle.append(device_group_handle)
        rt_handle.handles[port]['device_group_handle'].append(device_group_handle)
        result['device_group_handle'] = device_group_handle
        ethernet_handle = rt_handle.invoke('invoke', cmd='stc::get %s -children-ethiiif' % device_group_handle)
        rt_handle.handles[port]['ethernet_handle'].append(ethernet_handle)
        result['ethernet_handle'] = ethernet_handle
        if 'ip_addr' in kwargs:
            ip_handle = rt_handle.invoke('invoke', cmd='stc::get %s -children-ipv4if' % device_group_handle)
            rt_handle.link_ip_handle.append(ip_handle)
            # pass link_ip_device_handle to emulation_dst_handle under add_traffic
            rt_handle.link_ip_device_handle.append(device_group_handle)
            rt_handle.handles[port]['ipv4_handle'] = ip_handle
            result['ipv4_handle'] = ip_handle
        if 'ipv6_addr' in kwargs:
            # Every host has 2 IPv6If children - One for link local and other
            # for non link local. Taking the non link local Ipv6if child
            ipv6_handle = rt_handle.invoke('invoke', cmd='stc::get %s -children-ipv6if' % device_group_handle).split()[0].strip()    #BOJAN
            rt_handle.link_ipv6_handle.append(ipv6_handle)
            # pass link_ipv6_handle to emulation_dst_handle under add_traffic
            rt_handle.link_ipv6_device_handle.append(device_group_handle)
            rt_handle.handles[port]['ipv6_handle'].append(ipv6_handle)
            result['ipv6_handle'] = ipv6_handle
    #Set device Name
    if 'name' in kwargs:
        rt_handle.invoke('invoke', cmd="stc::config  " +device_group_handle+ " -Name  " +kwargs['name'])
    else:
        rt_handle.invoke('invoke', cmd="stc::config  " +device_group_handle+ " -Name  Device")
    # create gre tunnel
    if 'gre_dst_ip' in kwargs:
        ### config gre over ip
        gre_args['mode'] = 'create'
        gre_args['gre_tnl_type '] = '4'
        gre_args['gre_port_handle'] = port_handle
        gre_args['gre_count'] = count
        gre_args['gre_encapsulation'] = 'ethernet_ii'
        gre_args['gre_src_mac_addr'] = '00:00:00:00:00:00'
        if 'vlan_id' in kwargs:
            gre_args['gre_vlan_id'] = kwargs.get('vlan_id')
            gre_args['gre_vlan_id_step'] = kwargs.get('vlan_id_step', '1')
            gre_args['gre_encapsulation'] = 'ethernet_ii_vlan'

        if 'svlan_id' in kwargs:
            gre_args['gre_vlan_outer_id'] = kwargs.get('svlan_id')
            gre_args['gre_vlan_outer_id_step'] = kwargs.get('svlan_id_step', '1')
            gre_args['gre_vlan_id'] = kwargs.get('vlan_id', '1')
            gre_args['gre_vlan_id_step'] = kwargs.get('vlan_id_step', '1')
            gre_args['gre_encapsulation'] = 'ethernet_ii_qinq'

        if 'vlan_user_priority' in kwargs:
            gre_args['gre_vlan_user_priority'] = kwargs.get('vlan_user_priority')

        if 'vlan_user_priority_step' in kwargs:
            print('vlan_user_priority is not supported in Gre configuration')

        if 'ip_addr' in kwargs:
            gre_args['gre_src_addr'] = kwargs['ip_addr']

        if 'gateway' in kwargs:
            gre_args['gre_tnl_addr'] = kwargs['gateway']
        if 'gre_dst_ip' in kwargs:
            gre_args['gre_dst_addr'] = kwargs['gre_dst_ip']
        if 'netmask' in kwargs:
            #need process
            if '.' in kwargs['netmask']:
                binary = ''
                for seg in kwargs['netmask'].split('.'):
                    binary += '{:0<8b}'.format(int(seg))
                    gre_args['gre_prefix_len'] = binary.find('0')
            else:
                if 'gre_netmask' in kwargs:
                    gre_args['gre_prefix_len'] = kwargs['gre_netmask']

        if 'gre_dst_ip_step' in kwargs:
            gre_args['gre_dst_mode'] = 'increment'
            gre_args['gre_dst_addr_step'] = kwargs['gre_dst_ip_step']

        gre_ret = rt_handle.invoke('emulation_gre_config', **gre_args)
        link_config_args = dict()
        link_config_args['link_src'] = device_group_handle
        link_config_args['link_dst'] = gre_ret
        link_config_args['link_type'] = 'L2_GRE_Tunnel_Link'
#        status_config = rt_handle.invoke('link_config', (link_src = device_group_handle , link_dst = gre_ret , link_type = 'L2_GRE_Tunnel_Link' ))   #BOJAN
        status_config = rt_handle.invoke('link_config', **link_config_args)   #BOJAN
        if status_config['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to add gre destination address for ip handle {}".format(ip_handle))
        else:
            gre_handle = status_config['gre_handle']
            rt_handle.link_gre_handle.append(gre_handle)
            rt_handle.handles[port]['gre_handle'] = gre_handle
            result['gre_handle'] = gre_handle
    return result


def add_traffic(rt_handle, **kwargs):
    #add_traffic(rt_handle, source=rt_handle.dhcpv4_client_handle, frame_size=[100,1500, 10])
    """
    set traffic streams
    :param rt_handle:                RT object
    :param kwargs:
    name:                       used defined stream name (optional)
    source:                     a list of traffic source handle
    destination:                a list of traffic destination handle
    bidirectional:              1 or 0
    rate:                       traffic rate , can be mbps, pps, percent, for example: 1000mbps, 1000pps, 100%
    type:                       traffic type "ipv4" or "ipv6"
    mesh_type                   traffic mesh type, default is many_to_many, can be one_to_one
    dynamic_update:             dynamic_udate the address values from ppp
    frame_size:                 single value /a list [min max step]
    track_by:                   how to track the statistics,  by default is
                                trafficItem and source destination value pair
    stream_id:                  needed when trying to modify existing traffic streams
    tcp_dst_port:               tcp destination port
    tcp_dst_port_mode:          tcp dst port mode(fixed, incr, decr)
    tcp_src_port:               tcp source port
    tcp_src_port_mode:          tcp src port mode(fixed, incr, decr)
    udp_dst_port:               udp destination port
    udp_src_port:               udp source port
    ip_precedence:              ip precedence value (0-7)
    ip_precedence_mode          ip precedence mode (increment,decrement,random,shuffle)
    ip_precedence_step          ip precedence step
    ip_precedence_count         incr count
    ip_dscp:                    ip dscp value
    ip_dscp_mode                ip dscp is not supported for this release.Later release will give support
    ipv6_traffic_class:         ipv6 traffic class value
    ipv6_traffic_class_mode:    ipv6 traffic class mode(fixed, incr,decr)
    egress_tracking:            egress tracking mode: dscp/ipv6TC/tos_precedence/outer_vlan_priority
    packets_count:              number of packets to be transmitted
    burst_rate:                 set the mean burst rate for the stream(% of line rate), must be used with frame_size, pkts_per_burst, line_rate
    multicast:                  a list of destination multicast address

    :return:
    status and hash
    """
    traffic_args = dict()
    return_status = dict()
    return_status['status'] = '1'
    return_status['stream_id'] = ''
    stream_id_list = []
    emulation_src_handle = []
    emulation_dst_handle = []
    # Reset rt_handle.stream_Name
    rt_handle.stream_Name = ''

    # Default mode - create
    traffic_args['mode'] = 'create'
    if 'port' in kwargs:
        port_handle = rt_handle.port_to_handle_map[kwargs['port']]
        traffic_args['port_handle'] = port_handle

    #Specifies the name for currently selected traffic stream.
    if 'name' in kwargs:
        traffic_args['name'] = kwargs['name']

    if 'NAME' in kwargs:
        traffic_args['name'] = kwargs['NAME']
        kwargs['name'] = kwargs['NAME']

    if 'l3_length' in kwargs:
        traffic_args['l3_length'] = kwargs['l3_length']
    if 'transmit_mode' in kwargs and 'burst' in kwargs['transmit_mode']:
        traffic_args['transmit_mode'] = kwargs['transmit_mode']
    if 'burst_rate' in kwargs:
        traffic_args['transmit_mode'] = 'multi_burst'
        traffic_args['pkts_per_burst'] = kwargs['pkts_per_burst']
        traffic_args['rate_percent'] = '100'
        line_rate = int(kwargs.get('line_rate', '1000000000'))
        burst_rate = float(kwargs['burst_rate'].rstrip('%'))
        ##20 = preamble 8 + inter packet gap 12
        frame_length = int(kwargs['frame_size']) + 20
        burst_bytes = frame_length * int(kwargs['pkts_per_burst'])
        ibg_bytes = burst_bytes * int((100 / burst_rate - 1))
        nano_secs = ibg_bytes * 8 * 1000000000 / line_rate
        ##use nano seconds before HLAPI bug solved
        traffic_args['inter_burst_gap'] = nano_secs
        traffic_args['inter_frame_gap_unit'] = 'bytes'
        if 'rate' in kwargs:
            kwargs.pop('rate')


    # Loop to determine and update traffic_args['emulation_src_handle'].
    # We assume that this API is called either with source OR
    #emulation_src_handle, but not both.
    if 'source' in kwargs:
        emulation_src_handle = kwargs['source'] if type(kwargs['source']) \
            is list else emulation_src_handle # If List
        emulation_src_handle.append(kwargs['source']) if type(kwargs['source']) \
            is str else emulation_src_handle # If string
    elif 'emulation_src_handle' in kwargs:
        emulation_src_handle = kwargs['emulation_src_handle'] \
            if type(kwargs['emulation_src_handle']) is list \
            else emulation_src_handle # If List
        emulation_src_handle.append(kwargs['emulation_src_handle']) \
            if type(kwargs['emulation_src_handle']) is str \
            else emulation_src_handle # If string
    else:
        # Neither source or emulation_src_handle is provided. set
        # emulation_src_handle based on v6 (DHCPv6) or v4
        # (DHCPv4 and PPPoEv4) subscriber emulations
        if 'type' in kwargs and 'v6' in kwargs['type']:
            emulation_src_handle = rt_handle.dhcpv6_client_handle
        else:
            emulation_src_handle = rt_handle.dhcpv4_client_handle + \
                rt_handle.pppox_client_handle
    # Create the port to device mapping for the source handles
    emulation_src_handle = get_endpoint_handles(rt_handle, emulation_src_handle)
    src_port_emulation_handle_map = port_emulation_map(rt_handle, emulation_src_handle)

    # Loop to determine the update traffic_args['emulation_dst_handle'].
    # We assume that this API is called either with destination OR
    # emulation_dst_handle, but not both.
    if 'destination' in kwargs:
        emulation_dst_handle = kwargs['destination'] if type(kwargs['destination']) \
            is list else emulation_dst_handle # If List
        emulation_dst_handle.append(kwargs['destination']) if type(kwargs['destination']) \
            is str else emulation_dst_handle # If string
    elif 'emulation_dst_handle' in kwargs:
        emulation_dst_handle = kwargs['emulation_dst_handle'] \
            if type(kwargs['emulation_dst_handle']) is list \
            else emulation_dst_handle # If List
        emulation_dst_handle.append(kwargs['emulation_dst_handle']) \
            if type(kwargs['emulation_dst_handle']) is str \
            else emulation_dst_handle # If string
    elif 'multicast' in kwargs:
        # TO DO: When IGMP/Mcast is supported
        traffic_args['emulation_multicast_dst_handle'] = kwargs['multicast']
    else:
        # Neither source or emulation_src_handle is provided. set
        # emulation_dst_handle based on uplink devices created.
        if 'type' in kwargs and 'v6' in kwargs['type']:
            emulation_dst_handle = rt_handle.link_ipv6_handle
        else:
            emulation_dst_handle = rt_handle.link_ip_handle
    # Create the port to device mapping for the destination handles
    emulation_dst_handle = get_endpoint_handles(rt_handle, emulation_dst_handle)
    dst_port_emulation_handle_map = port_emulation_map(rt_handle, emulation_dst_handle)

    # Set the rate parameters
    if 'rate' in kwargs:
        if 'mbps' in kwargs['rate']:
            traffic_args['rate_mbps'] = re.sub('mbps', '', kwargs['rate'])
        if 'pps' in kwargs['rate']:
            traffic_args['rate_pps'] = re.sub('pps', '', kwargs['rate'])
        if '%' in kwargs['rate']:
            traffic_args['rate_percent'] = re.sub('%', '', kwargs['rate'])
    else:
        traffic_args['rate_pps'] = '1000'

    # Set the L3 protocol parameter
    if 'type' in kwargs:
        if 'arp' in kwargs['type']:
            traffic_args['l3_protocol'] = 'arp'
        elif 'v4' in kwargs['type']:
            traffic_args['l3_protocol'] = 'ipv4'
        elif 'v6' in kwargs['type']:
            traffic_args['l3_protocol'] = 'ipv6'
        elif 'ethernet_vlan' in kwargs['type']:
            traffic_args['traffic_type'] = 'L2'
            traffic_args['l2_encap'] = 'ethernet_ii_vlan'
    else:
        traffic_args['l3_protocol'] = 'ipv4'

    # Dualstack kwargs['name'] is retun as names endswith v4 and v6
    if 'name' in kwargs and kwargs['name'].endswith('v6'):
        traffic_args['l3_protocol'] = 'ipv6'


    # Determine the mode. If stream_id of an existing streamblock is provided
    # we assume that the API is called to modify the streamblock parameters.
    # Else, we create a new streamblock.
    if 'stream_id' in kwargs:
        traffic_args['mode'] = 'modify'
    else:
        traffic_args['mode'] = 'create'

    # TO DO: circuit_endpoint_type need to support latter releases
    #if 'type' in kwargs:
    #   traffic_args['circuit_endpoint_type'] = kwargs['type']

    #Configure the TOS 3-bits Precedence field in the IP header
    if 'ip_precedence' in kwargs:
        traffic_args['ip_precedence'] = kwargs['ip_precedence']
    if 'ip_precedence_mode' in kwargs:
        traffic_args['ip_precedence_mode'] = kwargs['ip_precedence_mode']
    if 'ip_precedence_step' in kwargs:
        traffic_args['ip_precedence_step'] = kwargs['ip_precedence_step']
    if 'ip_precedence_count' in kwargs:
        traffic_args['ip_precedence_count'] = kwargs['ip_precedence_count']

    #Specifies the DSCP field in Layer 4 IP header for particular stream
    if 'ip_dscp' in kwargs:
        traffic_args['ip_dscp'] = kwargs['ip_dscp']
    if 'ip_dscp_step' in kwargs:
        traffic_args['ip_dscp_step'] = kwargs['ip_dscp_step']
    if 'ip_dscp_count' in kwargs:
        traffic_args['ip_dscp_count'] = kwargs['ip_dscp_count']

    # Set the frame size related parameters
    if 'frame_size' in kwargs:
        if isinstance(kwargs['frame_size'], list):
            if len(kwargs['frame_size']) == 3:
                traffic_args['length_mode'] = 'increment'
                traffic_args['frame_size_min'] = kwargs['frame_size'][0]
                traffic_args['frame_size_max'] = kwargs['frame_size'][1]
                traffic_args['frame_size_step'] = kwargs['frame_size'][2]
            if len(kwargs['frame_size']) == 2:
                traffic_args['length_mode'] = 'random'
                traffic_args['frame_size_min'] = kwargs['frame_size'][0]
                traffic_args['frame_size_max'] = kwargs['frame_size'][1]
        else:
            traffic_args['frame_size'] = kwargs.get('frame_size', '1000')
            traffic_args['length_mode'] = 'fixed'
    else:
        traffic_args['frame_size'] = 1000
        traffic_args['length_mode'] = 'fixed'

    # Specifies the IPv6 traffic class setting to use for application
    # layer traffic.
    if 'ipv6_traffic_class' in kwargs:
        traffic_args['ipv6_traffic_class'] = kwargs['ipv6_traffic_class']

    # Specifies the ports on the sending TCP module
    if 'tcp_dst_port' in kwargs or 'tcp_src_port' in kwargs:
        traffic_args['l4_protocol'] = 'tcp'
        if 'tcp_dst_port' in kwargs:
            traffic_args['tcp_dst_port'] = kwargs['tcp_dst_port']
            traffic_args['tcp_dst_port_mode'] = kwargs.get('tcp_dst_port_mode', 'fixed')
            if 'tcp_dst_port_step' in kwargs:
                traffic_args['tcp_dst_port_step'] = kwargs['tcp_dst_port_step']
            if 'tcp_dst_port_count' in kwargs:
                traffic_args['tcp_dst_port_count'] = kwargs['tcp_dst_port_count']
        if 'tcp_src_port' in kwargs:
            traffic_args['tcp_src_port'] = kwargs['tcp_src_port']
            traffic_args['tcp_src_port_mode'] = kwargs.get('tcp_src_port_mode', 'fixed')
            if 'tcp_src_port_step' in kwargs:
                traffic_args['tcp_src_port_step'] = kwargs['tcp_src_port_step']
            if 'tcp_src_port_count' in kwargs:
                traffic_args['tcp_src_port_count'] = kwargs['tcp_src_port_count']

    #Specifies the ports on the sending UDP module
    if 'udp_dst_port' in kwargs or 'udp_src_port' in kwargs:
        traffic_args['l4_protocol'] = 'udp'
        if 'udp_dst_port' in kwargs:
            traffic_args['udp_dst_port'] = kwargs['udp_dst_port']
            traffic_args['udp_dst_port_mode'] = kwargs.get('udp_dst_port_mode', 'increment')
            if 'udp_dst_port_step' in kwargs:
                traffic_args['udp_dst_port_step'] = kwargs['udp_dst_port_step']
            if 'udp_dst_port_count' in kwargs:
                traffic_args['udp_dst_port_count'] = kwargs['udp_dst_port_count']
        if 'udp_src_port' in kwargs:
            traffic_args['udp_src_port'] = kwargs['udp_src_port']
            traffic_args['udp_src_port_mode'] = kwargs.get('udp_src_port_mode', 'increment')
            if 'udp_src_port_step' in kwargs:
                traffic_args['udp_src_port_step'] = kwargs['udp_src_port_step']
            if 'udp_src_port_count' in kwargs:
                traffic_args['udp_src_port_count'] = kwargs['udp_src_port_count']

    # Check and set the bidirectional knob
    bidirectional = kwargs.get('bidirectional', '1')

    # Determine the Traffic Pattern
    if len(src_port_emulation_handle_map) == 1 and len(dst_port_emulation_handle_map) == 1:
        src_dest_mesh = 'one_to_one'
    else:
        src_dest_mesh = kwargs.get('mesh_type', 'many_to_many')

    # Create the streamblocks for traffic pattern Many to Many
    if src_dest_mesh is 'many_to_many':
        traffic_args['bidirectional'] = '0'
        print('mesh many_to_many')
        for (port_hdl, emululation_hld_list) in src_port_emulation_handle_map.items():
            traffic_args['emulation_src_handle'] = emululation_hld_list
            traffic_args['port_handle'] = port_hdl
            traffic_args['emulation_dst_handle'] = emulation_dst_handle
            #config_status = rt_handle.invoke('traffic_config', **traffic_args)
            config_status = create_streamblock(rt_handle, **traffic_args)
            if config_status['status'] == '1':
                stream_id_list.append(config_status['stream_id'])
            return_status['status'] = return_status['status'] and config_status['status']
        if  bidirectional is '1':
            port_emulation_handle_map = dst_port_emulation_handle_map
            for (port_hdl, emululation_hld_list)in port_emulation_handle_map.items():
                traffic_args['emulation_src_handle'] = emululation_hld_list
                traffic_args['port_handle'] = port_hdl
                traffic_args['emulation_dst_handle'] = emulation_src_handle
                #config_status = rt_handle.invoke('traffic_config', **traffic_args)
                config_status = create_streamblock(rt_handle, **traffic_args)
                if config_status['status'] == '1':
                    stream_id_list.append(config_status['stream_id'])
                return_status['status'] = return_status['status'] and config_status['status']

    # Create the streamblocks for traffic pattern Many to Many
    elif src_dest_mesh is 'one_to_one':
        print('mesh one to one')
        src_port_list = sorted(src_port_emulation_handle_map.keys())
        dst_port_list = sorted(dst_port_emulation_handle_map.keys())
        if src_port_emulation_handle_map == dst_port_emulation_handle_map:
            port_num = len(dst_port_list)
        else:
            port_num = len(src_port_list)
        for i in range(0, port_num):
            traffic_args['port_handle'] = src_port_list[i]
            if bidirectional is '1':
                traffic_args['bidirectional'] = '1'
                traffic_args['port_handle2'] = dst_port_list[i]
            else:
                traffic_args['bidirectional'] = '0'
            traffic_args['emulation_src_handle'] = src_port_emulation_handle_map[src_port_list[i]]
            traffic_args['emulation_dst_handle'] = dst_port_emulation_handle_map[dst_port_list[i]]
            print(traffic_args)
            #config_status = rt_handle.invoke('traffic_config', **traffic_args)
            config_status = create_streamblock(rt_handle, **traffic_args)
            if config_status['status'] == '1':
                stream_id_list.append(config_status['stream_id'])
            return_status['status'] = return_status['status'] and config_status['status']

    elif src_dest_mesh is 'fully':
        print('fully')
        emulation_dst_handle_list = list()
        all_port_emulation_handle_map = src_port_emulation_handle_map
        all_port_emulation_handle_map.update(dst_port_emulation_handle_map)
        for (port_hdl, src_emulatin_hdls) in all_port_emulation_handle_map.items():
            traffic_args['port_handle'] = port_hdl
            traffic_args['emulation_src_handle'] = src_emulatin_hdls
            for (port_hdl2, dst_emulatin_hdls) in all_port_emulation_handle_map.items():
                emulation_dst_handle_list.extend(dst_emulatin_hdls)
            traffic_args['emulation_dst_handle'] = list(set(emulation_dst_handle_list).difference(set(traffic_args['emulation_src_handle'])))
            #config_status = rt_handle.invoke('traffic_config', **traffic_args)
            config_status = create_streamblock(rt_handle, **traffic_args)
            if config_status['status'] == '1':
                stream_id_list.append(config_status['stream_id'])
            return_status['status'] = return_status['status'] and config_status['status']

    # Duration configuration for the created streamblocks
    # Spirent HLTAPI does not configure duration in the traffic_config API
    # but does so in the traffic_control API. Hence we will store the duration
    # provided to us in a dictionary, and configure it in the traffic_action API.
    if 'duration' in kwargs:
        rt_handle.streamBlockDurationMap[rt_handle.stream_Name] = kwargs['duration']

    if len(stream_id_list) > 1:
        return_status['stream_id'] = stream_id_list
    else:
        return_status['stream_id'] = stream_id_list[0]
    return return_status

def get_endpoint_handles(rt_handle, endpoint_list):
    """
    This private method is used to determine the valid handles
    for the emulation_src_handle and emulation_dst_handle
    arguments of traffic_config API. Spirent HLTAPI can take
    dhcpv4blockconfig as valid inputs, but not pppoeclientblockconfig
    and ipv4/6if and dhcpv6blockconfig. Hence this method checks for
    these handle values and returns the parent host that can be used
    as the argument value.

    ** TODO: Current loop needs to be updated when we support Mcast
    traffic, as the argument value might be ipv4networkblock1
    or ipv6networkblock1, and hence we need return the parent.
    """
    ret_list = []
    for end_point in endpoint_list:
        # Check if the endpoint is DHCPv6 block config. If so we need to
        # check if this is a PD emulation. In case of PD emulation
        # we need to use the clients behind the home gateway as
        # the end point
        if 'dhcpv6blockconfig' in end_point or 'dhcpv6pdblockconfig' in end_point or 'host' in end_point:
            # Check if we have the PD to client mapping
            if end_point in rt_handle.homeGwToClientMap:
                end_point = rt_handle.homeGwToClientMap[end_point]
        if 'ppp' in end_point or 'ipv' in end_point or 'ethiiif' in end_point or 'dhcpv6' in end_point:
            ret_list.append(rt_handle.invoke('invoke', cmd="stc::get "+end_point+" -parent").strip())
        else:
            ret_list.append(end_point)
    return ret_list

def create_streamblock(rt_handle, **kwargs):
    """
    Common method that takes care of creating the streamblock for
    different traffic patterns based on the args provided.

    Also updates the below data structures:
    rt_handle.stream_id: Appends the streamblock handles.
    rt_handle.traffic_item: Appends the streamblock name
    rt_handle.stream_name_map: Updates the streamblk name to streamblk handle map
    """
    config_status = rt_handle.invoke('traffic_config', **kwargs)
    if config_status['status'] == '1':
        # Check if the traffic_config API creates more than one
        # streamblock (returns a list) for just one.
        if type(config_status['stream_id']) is dict:
            # HLTAPI now also returns _pylist as one of the keys of stream_id
            # as per an enhancement request. However, in this API flow, we dont
            # need it. Will delete these _pylist keys from the dict.
            keys_to_delete = list()
            for key in config_status['stream_id']:
                if 'pylist' not in key:
                    # Update the rt_handle.stream_id list with the streamblock handle
                    rt_handle.stream_id.append(config_status['stream_id'][key])
                    rt_handle.stream_Name = rt_handle.invoke('invoke', cmd='stc::get %s -name' % config_status['stream_id'][key].strip())
                else:
                    keys_to_delete.append(key)
            # Delete the _pylist keys in the dict
            for key_to_delete in keys_to_delete:
                del config_status['stream_id'][key_to_delete]

            # Update the rt_handle.stream_name_map dict
            if rt_handle.stream_Name in rt_handle.stream_name_map:
                rt_handle.stream_name_map[rt_handle.stream_Name] = \
                          rt_handle.stream_name_map[rt_handle.stream_Name] + \
                          list(config_status['stream_id'].values())
            else:
                rt_handle.stream_name_map[rt_handle.stream_Name] = \
                          list(config_status['stream_id'].values())
            # update the rt_handle.traffic_item list
            if rt_handle.stream_Name not in rt_handle.traffic_item:
                rt_handle.traffic_item.append(rt_handle.stream_Name)
        else:
            rt_handle.stream_Name = rt_handle.invoke('invoke', cmd='stc::get %s -name' % config_status['stream_id'].strip())
            # Update the rt_handle.stream_id list with the streamblock handle
            rt_handle.stream_id.append(config_status['stream_id'])

            # update the rt_handle.traffic_item list
            if rt_handle.stream_Name not in rt_handle.traffic_item:
                rt_handle.traffic_item.append(rt_handle.stream_Name)

            # Update the rt_handle.stream_name_map dict
            if rt_handle.stream_Name in rt_handle.stream_name_map:
                rt_handle.stream_name_map[rt_handle.stream_Name].append(config_status['stream_id'])
            else:
                rt_handle.stream_name_map[rt_handle.stream_Name] = [config_status['stream_id']]
    return config_status

def port_emulation_map(rt_handle, emulation_handle_list):
    """
    This is an internal function used to get the port to device handle map
    """
    port_emulation_handle_map = {}
    print(emulation_handle_list)
    for emulation_hdl in emulation_handle_list:
        # Check if the handle sent is that of a host, or of the emulation type - dhcpv4blockconfig1 or pppoeclientblockconfig1
        if 'host' in emulation_hdl or 'emulateddevice' in emulation_hdl:
            port_hdl = rt_handle.invoke('invoke', cmd='stc::get %s -affiliationport-Targets' %  emulation_hdl.strip())
        else:
            host_hdl = rt_handle.invoke('invoke', cmd='stc::get %s -parent' %  emulation_hdl.strip())
            port_hdl = rt_handle.invoke('invoke', cmd='stc::get %s -affiliationport-Targets' %  host_hdl.strip())
        if port_hdl in port_emulation_handle_map:
            port_emulation_handle_map[port_hdl].append(emulation_hdl)
        else:
            port_emulation_handle_map[port_hdl] = []
            port_emulation_handle_map[port_hdl].append(emulation_hdl)
    print(port_emulation_handle_map)
    return port_emulation_handle_map


def set_traffic(rt_handle, **kwargs):
    """
    modify existing trafficitem
    :param rt_handle:                RT object
    :param kwargs:
    source:                     a list of traffic source handle
    destination:                a list of traffic destination handle
    bidirectional:              1 or 0
    rate:                       traffic rate , can be bps, pps, percent, for example: 1000000bps, 1000pps, 100%
    type:                       traffic type "ipv4" or "ipv6"
    mesh_type                   traffic mesh type, default is many_to_many, can be one_to_one
    dynamic_update:             dynamic_udate the address values from ppp
    frame_size:                 single value /a list [min max step]
    track_by:                   how to track the statistics,
                                by default is trafficItem and source destination endpoint pair
    stream_id:                  needed when trying to modify existing traffic streams
    :return:
    status:                    1 or 0
    """
    traffic_args = dict()
    emulation_src_handle = []
    emulation_dst_handle = []
    status = '1'
    if 'stream_id' not in kwargs:
        status = '0'
        print("stream_id is mandotory when modifying traffic item")
        return status
    traffic_args['mode'] = 'modify'
    traffic_args['stream_id'] = kwargs['stream_id']
    if 'port' not in kwargs:
        traffic_args['port_handle'] = rt_handle.invoke('invoke', cmd='stc::get %s -parent' % kwargs['stream_id'])

    if 'source' in kwargs:
        if type(kwargs['source']) is list:
            emulation_src_handle = kwargs['source']
        else:
            emulation_src_handle.append(kwargs['source'])
    else:
        # this argument 'type' need test .
        if 'type' in kwargs and 'v6' in kwargs['type']:
            emulation_src_handle = rt_handle.dhcpv6_client_device_handle
        else:
            emulation_src_handle = rt_handle.dhcpv4_client_device_handle + rt_handle.pppox_client_handle

    if 'destination' in kwargs:
        if type(kwargs['destination']) is list:
            emulation_src_handle = kwargs['destination']
        else:
            emulation_dst_handle.append(kwargs['destination'])
    else:
        if 'type' in kwargs and 'v6' in kwargs['type']:
            emulation_dst_handle = rt_handle.link_ipv6_device_handle
        else:
            emulation_dst_handle = rt_handle.link_ip_device_handle

    if 'rate' in kwargs:
        if 'mbps' in kwargs['rate']:
            traffic_args['rate_mbps'] = re.sub('mbps', '', kwargs['rate'])
        if 'pps' in kwargs['rate']:
            traffic_args['rate_pps'] = re.sub('pps', '', kwargs['rate'])
        if '%' in kwargs['rate']:
            traffic_args['rate_percent'] = re.sub('%', '', kwargs['rate'])
    else:
        traffic_args['rate_pps'] = '1000'
    #if 'type' in kwargs:
    #    traffic_args['circuit_endpoint_type'] = kwargs['type']
    #if 'dynamic_update' in kwargs:
    #    traffic_args['dynamic_update_fields'] = kwargs['dynamic_update']
    if 'frame_size' in kwargs:
        if isinstance(kwargs['frame_size'], list):
            traffic_args['length_mode'] = 'increment'
            traffic_args['frame_size_min'] = kwargs['frame_size'][0]
            traffic_args['frame_size_max'] = kwargs['frame_size'][1]
            traffic_args['frame_size_step'] = kwargs['frame_size'][2]
    else:
        traffic_args['frame_size'] = kwargs.get('frame_size', '1000')
        traffic_args['length_mode'] = 'fixed'

    result = rt_handle.invoke('traffic_config', **traffic_args)
    status = result['status']
    return status

def get_traffic_stats(rt_handle, **kwargs):
    """

    :param kwargs:
    :param rt_handle:         RT object
    mode:                all/traffic_item
    :return:
    """
    stats_args = {}
    # Stream Level Results
    if 'traffic_item' in kwargs['mode']:
        stats_args['mode'] = 'streams'
        # Mode streams needs stream_name, else reports for all streams
        if 'stream_name' in kwargs:
            stats_args['streams'] = rt_handle.stream_name_map[kwargs['stream_name']]
            streamName = kwargs['stream_name']
        else:
            print("No stream_name provided. Report stream level results for all streams")
    # Or, Mode : All
    if 'all' in kwargs['mode'] or 'l23_test_summary' in kwargs['mode']:
        stats_args['mode'] = 'all'
        stats_args['port_handle'] = rt_handle.invoke('invoke', cmd='stc::get project1 -children-port').strip().split()

    # Call the traffic_stats HLT API
    stats_status = rt_handle.invoke('traffic_stats', **stats_args)

    # Ixia returns some of the stats in a diff key-value combination. Below
    # loop tries to address those return values
    if 'all' in kwargs['mode'] or 'l23_test_summary' in kwargs['mode']:
        # Get the port handles as a list
        portKeyList = rt_handle.invoke('invoke', cmd='stc::get project1 -children-port').strip().split()

        # Loop to return:
        # rx_packets = traffic_dict['aggregate']['rx']['raw_pkt_count']['avg']
        # tx_packets = traffic_dict['aggregate']['tx']['raw_pkt_count']['avg']
        aggTxFrameCount = 0
        aggRxFrameCount = 0
        for portKey in portKeyList:
            #aggTxFrameCount+= int(stats_status[portKey]['aggregate']['tx']['total_pkts'])
            #aggRxFrameCount+= int(stats_status[portKey]['aggregate']['rx']['total_pkts'])
            aggTxFrameCount += int(stats_status[portKey]['aggregate']['tx']['pkt_count'])
            aggRxFrameCount += int(stats_status[portKey]['aggregate']['rx']['pkt_count'])

        # Declare the multi-level dict with default values
        stats_status.setdefault('aggregate', {}).setdefault('rx', {}).setdefault('raw_pkt_count', {})
        stats_status.setdefault('aggregate', {}).setdefault('tx', {}).setdefault('raw_pkt_count', {})
        # Populate the dictionary
        stats_status['aggregate']['tx']['raw_pkt_count']['avg'] = aggTxFrameCount
        stats_status['aggregate']['rx']['raw_pkt_count']['avg'] = aggRxFrameCount

    if 'traffic_item' in kwargs['mode']:
        # Get the stream handles as a list
        if 'throughput' in kwargs['verify_by'] or 'packetcount' in kwargs['verify_by']:
            # Get the stream throughput percentage and packets count
            aggTxFrameCount = 0
            aggRxFrameCount = 0
            #Get stats from particular Stream name
            if 'stream_name' in kwargs:
                # Declare the multi-level dict with default values
                stats_status.setdefault('traffic_item', {}).setdefault(streamName, {}).setdefault('rx', {}).setdefault('total_pkts', {})
                stats_status.setdefault('traffic_item', {}).setdefault(streamName, {}).setdefault('tx', {}).setdefault('total_pkts', {})
                for streamKey in rt_handle.stream_name_map[streamName]:
                    aggTxFrameCount += int(stats_status[streamKey]['tx']['total_pkts'])
                    aggRxFrameCount += int(stats_status[streamKey]['rx']['total_pkts'])
            else:
                #Get Stas from all Stream Blocks
                for streamName in rt_handle.traffic_item:
                    # Declare the multi-level dict with default values
                    stats_status.setdefault('traffic_item', {}).setdefault(streamName, {}).setdefault('rx', {}).setdefault('total_pkts', {})
                    stats_status.setdefault('traffic_item', {}).setdefault(streamName, {}).setdefault('tx', {}).setdefault('total_pkts', {})
                for streamKey in rt_handle.stream_name_map[streamName]:
                    aggTxFrameCount += int(stats_status[streamKey]['tx']['total_pkts'])
                    aggRxFrameCount += int(stats_status[streamKey]['rx']['total_pkts'])
            # Populate the dictionary
            stats_status['traffic_item'][streamName]['tx']['total_pkts'] = aggTxFrameCount
            stats_status['traffic_item'][streamName]['rx']['total_pkts'] = aggRxFrameCount
        elif 'rate' in kwargs['verify_by']:
            # Get the stream measured rate
            aggTxFrameRate = 0
            aggRxFrameRate = 0
            #Get stats from particular Stream name
            if 'stream_name' in kwargs:
                # Declare the multi-level dict with default values
                stats_status.setdefault('traffic_item', {}).setdefault(streamName, {}).setdefault('rx', {}).setdefault('total_pkt_mbit_rate', {})
                stats_status.setdefault('traffic_item', {}).setdefault(streamName, {}).setdefault('tx', {}).setdefault('total_pkt_mbit_rate', {})
                for streamKey in rt_handle.stream_name_map[streamName]:
                    aggTxFrameRate += int(stats_status[streamKey]['tx']['total_pkt_bit_rate'])
                    aggRxFrameRate += int(stats_status[streamKey]['rx']['total_pkt_bit_rate'])
            else:
                #Get Stas from all Stream Blocks
                for streamName in rt_handle.traffic_item:
                    # Declare the multi-level dict with default values
                    stats_status.setdefault('traffic_item', {}).setdefault(streamName, {}).setdefault('rx', {}).setdefault('total_pkt_mbit_rate', {})
                    stats_status.setdefault('traffic_item', {}).setdefault(streamName, {}).setdefault('tx', {}).setdefault('total_pkt_mbit_rate', {})
                for streamKey in rt_handle.stream_name_map[streamName]:
                    aggTxFrameRate += int(stats_status[streamKey]['tx']['total_pkt_bit_rate'])
                    aggRxFrameRate += int(stats_status[streamKey]['rx']['total_pkt_bit_rate'])
            # Populate the dictionary
            stats_status['traffic_item'][streamName]['tx']['total_pkt_mbit_rate'] = float(aggTxFrameRate/1000000)
            stats_status['traffic_item'][streamName]['rx']['total_pkt_mbit_rate'] = float(aggRxFrameRate/1000000)

    return stats_status

def traffic_action(rt_handle, **kwargs):
    """
    #rt.traffic_action(action='start')
    :param rt_handle:            RT object
    :param kwargs:
    action:                 start/stop/delete/poll/regenerate/apply/clearstats/reset
    handle:                 specify a specific traffic item if needed
    :return:
    """
    traffic_args = dict()
    #if 'timeout' in kwargs:
    #    traffic_args['max_wait_timer'] = kwargs['timeout']
    if 'handle' in kwargs:
    # In Dual Stack stream Blocks BBEkeywords append name with #PPPov4v6 #PPPoV6v6
        if kwargs['handle'].endswith('v4v4'):
            kwargs['handle'] = kwargs['handle'].replace("v4", "", 1)
        if kwargs['handle'].endswith('v6v6'):
            kwargs['handle'] = kwargs['handle'].replace("v6", "", 1)

        #traffic_args['stream_handle'] = rt_handle.stream_id
        traffic_args['stream_handle'] = rt_handle.stream_name_map[kwargs['handle']]
        print("Traffic action API called for streamblocks with handle: "+ format(traffic_args['stream_handle']))
        # DHCPv6PD Uplink Traffic issue - Update the streamblock
        for tmpSbHandle in traffic_args['stream_handle']:
            # Stupid attempt to force the SB stack update
            tmpIpv6Handle = rt_handle.invoke('invoke', cmd="stc::get "+tmpSbHandle+" -children-ipv6:ipv6")
            if 'ipv6' in tmpIpv6Handle:
                rt_handle.invoke('invoke', cmd="stc::delete "+tmpIpv6Handle)
                rt_handle.invoke('invoke', cmd="stc::apply")
            rt_handle.invoke('invoke', cmd="stc::perform StreamBlockUpdateCommand -StreamBlock "+tmpSbHandle)
        # Check if the streamblock was created with duration
        if kwargs['handle'] in rt_handle.streamBlockDurationMap:
            traffic_args['duration'] = rt_handle.streamBlockDurationMap[kwargs['handle']]
    else:
        traffic_args['port_handle'] = 'all'

    # Perform ARP for ALL devices
    #rt_handle.invoke('invoke', cmd="stc::perform ArpNdStartOnAllDevicesCommand")
    # Check if the streamblock was created with duration
    #if kwargs['handle'] in rt_handle.streamBlockDurationMap:
    #    traffic_args['duration'] = rt_handle.streamBlockDurationMap[kwargs['handle']]

    # Disable ARP, unless requested for
    traffic_args['enable_arp'] = 0
    if 'enable_arp' in kwargs:
        traffic_args['enable_arp'] = kwargs['enable_arp']

    traffic_args['action'] = 'run'
    if 'start' in kwargs['action']:
        traffic_args['traffic_start_mode'] = 'sync'
    if 'stop' in kwargs['action']:
        traffic_args['action'] = 'stop'
    if 'poll' in kwargs['action']:
        traffic_args['action'] = 'poll'
    if 'clearstats' in kwargs['action']:
        traffic_args['action'] = 'clear_stats'
    if 'reset' in kwargs['action']:
        traffic_args['action'] = 'reset'
    if 'regenerate' in kwargs['action']:
        traffic_args['action'] = 'run'
    if 'duration' in kwargs:
        traffic_args['duration'] = kwargs['duration']
    #if 'apply' in kwargs['action']:
    #    traffic_args['action'] = 'apply'
    print(traffic_args)
    # Delete Stream Blocks individual
    if 'delete' in kwargs['action']:
        result = dict()
        if 'stream_handle' in traffic_args:
            # Delete the specific streamblocks
            for sbHdl in traffic_args['stream_handle']:
                rt_handle.invoke('invoke', cmd="stc::delete " +sbHdl)
        else:
            # Action delete called with no streamblock handles
            # Delete all streamblocks
            for eachItem in rt_handle.traffic_item:
                for eachStream in rt_handle.stream_name_map[eachItem]:
                    rt_handle.invoke('invoke', cmd="stc::delete " +eachStream)
        result['status'] = '1'
    else:
        if traffic_args['action'] == 'run':
            # Perform ARP for ALL devices
            rt_handle.invoke('invoke', cmd="stc::perform ArpNdStartOnAllDevicesCommand")
        result = rt_handle.invoke('traffic_control', **traffic_args)

    # Delete streamblock names and references from rt_handle datastructures
    if result['status'] == '1' and 'delete' in kwargs['action']:
        if 'handle' in kwargs:
            # Remove references of particular stream
            rt_handle.traffic_item.remove(kwargs['handle'])
            del rt_handle.stream_name_map[kwargs['handle']]
        else:
            # Remove references of all streams
            rt_handle.traffic_item.clear()
            rt_handle.stream_name_map.clear()

    return result

def start_all(rt_handle):
    """
    start all protocols
    :param rt_handle:                    RT object
    :return:
    a dictionary of status and other information
    """
    # Check and start ANCP
    if len(rt_handle.ancp_handle) > 0:
        ancp_router_handles = ' '.join(rt_handle.ancp_handle) # For AncpInitiateAdjacencyWait and AncpPortUpWait
        ancp_access_node_handles = str() # For AncpInitiateAdjacency and AncpPortUp

        for ancp_router in rt_handle.ancp_handle:
            ancp_access_node_handles += " "+ rt_handle.invoke('invoke', cmd="stc::get "+ancp_router+" -children-AncpAccessNodeConfig")

        # Initiate the ANCP Adjacency
        rt_handle.invoke('invoke', cmd="stc::perform AncpInitiateAdjacency -BlockList {"+ancp_access_node_handles.strip()+"}")
        rt_handle.invoke('invoke', cmd="stc::perform AncpInitiateAdjacencyWait -ObjectList {"+ancp_router_handles+"} -AdjacencyBlockState ESTABLISHED -WaitTime 50")

        # Send Port UP
        rt_handle.invoke('invoke', cmd="stc::perform AncpPortUp -BlockList {"+ancp_access_node_handles.strip()+"}")
        rt_handle.invoke('invoke', cmd="stc::perform AncpPortUpWait -ObjectList {"+ancp_router_handles+"} -SubscriberBlockState ESTABLISHED -WaitTime 30")

    # For other protocols
    rt_handle.invoke('invoke', cmd="stc::perform DevicesStartAllCommand")
    sleep(15)
    return rt_handle.invoke('invoke', cmd="stc::perform DevicesStartAllCommand")


def stop_all(rt_handle):
    """
    stop all protocols
    :param rt_handle:                    RT object
    :return:
    a dictionary of status and other information
    """

    # Check and stop ANCP
    if len(rt_handle.ancp_handle) > 0:
        ancp_router_handles = ' '.join(rt_handle.ancp_handle) # For AncpInitiateAdjacencyWait and AncpPortUpWait
        ancp_access_node_handles = str() # For AncpInitiateAdjacency and AncpPortUp

        for ancp_router in rt_handle.ancp_handle:
            ancp_access_node_handles += " "+ rt_handle.invoke('invoke', cmd="stc::get "+ancp_router+" -children-AncpAccessNodeConfig")

        # Send Port Down
        rt_handle.invoke('invoke', cmd="stc::perform AncpPortDown -BlockList {"+ancp_access_node_handles.strip()+"}")
        rt_handle.invoke('invoke', cmd="stc::perform AncpPortDownWait -ObjectList {"+ancp_router_handles+"} -SubscriberBlockState IDLE -WaitTime 30")

        # Terminate the ANCP Adjacency
        rt_handle.invoke('invoke', cmd="stc::perform AncpTerminateAdjacency -BlockList {"+ancp_access_node_handles.strip()+"}")
        rt_handle.invoke('invoke', cmd="stc::perform AncpTerminateAdjacencyWait -ObjectList {"+ancp_router_handles+"} -AdjacencyBlockState IDLE -WaitTime 30")

    # For all other protocols
    return rt_handle.invoke('invoke', cmd="stc::perform DevicesStopAllCommand")


def add_application_traffic(rt_handle, **kwargs):
    """
    :param rt_handle:
    :return:
    """
    pass

def add_dhcp_server(rt_handle, **kwargs):
    """
    :param rt_handle                            RT object
    :param kwargs:
    handle:                                ipv4 handle or ipv6 handle
    pool_size:                             server pool size
    pool_start_addr:                       pool start address
    pool_mask_length:                      pool prefix length
    pool_gateway:                          pool gateway address
    lease_time                             pool address lease time
    dhcpv6_ia_type:                        v6 IA type "iana, iapd, iana+iapd"
    pool_prefix_start:                     v6 PD start prefix
    pool_prefix_length:                    v6 prefix length
    pool_prefix_size:                      v6 prefix pool size
 
    # use_rapid_commit                       = "0",
    # subnet_addr_assign                     = "0",
    # subnet                                 = "relay",
 
    :param kwargs:
    :return:
    a dictionary of status dhcpv4_server_handle dhcpv6_server_handle
    """
    result = dict()
    result['status'] = '1'
    dhcp_args = dict()
    if 'handle' not in kwargs:
        raise Exception("Mandatory argument - handle - not provided to the add_dhcp_server method.")
 
    # The argument handle being provided to add_dhcp_server is either
    # uplink.rt_ipv4_handle or uplink.rt_ipv6_handle which means, the handle
    # the handle would be ipv4if1 or ipv6if1. Hence, we need to get the
    # parent (host/emulateddevice) handle. Also, the mode would be enable.
    dhcp_args['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle'].split()[0]+" -parent")    # BOJAN
    dhcp_args['mode'] = 'enable'
 
 
    # configure DHCPv4 server
    if 'v4' in kwargs['handle']:
        dhcp_args['ip_version'] = '4'
        if 'lease_time' in kwargs:
            dhcp_args['lease_time'] = kwargs['lease_time']
        if 'pool_start_addr' in kwargs:
            dhcp_args['ipaddress_pool'] = kwargs['pool_start_addr']
        if 'pool_mask_length' in kwargs:
            dhcp_args['enable_custom_pool'] = 'true'
            dhcp_args['host_addr_prefix_length'] = kwargs['pool_mask_length']
        if 'pool_size' in kwargs:
            dhcp_args['ipaddress_count'] = kwargs['pool_size']
        if 'pool_gateway' in kwargs:
            dhcp_args['dhcp_offer_options'] = '1'
            dhcp_args['dhcp_offer_router_address'] = kwargs['pool_gateway']
 
    # configure DHCPv6 server
    if 'v6' in kwargs['handle']:
        dhcp_args['ip_version'] = '6'
        if 'dhcpv6_ia_type' in kwargs:
            if 'IANA' in kwargs['dhcpv6_ia_type'].upper():
                dhcp_args['server_emulation_mode'] = "DHCPV6"
                if 'pool_start_addr' in kwargs:
                    dhcp_args['addr_pool_start_addr'] = kwargs['pool_start_addr']
                if 'pool_mask_length' in kwargs:
                    dhcp_args['addr_pool_prefix_length'] = kwargs['pool_mask_length']
                if 'pool_size' in kwargs:
                    dhcp_args['addr_pool_addresses_per_server'] = kwargs['pool_size']
            elif 'PD' in kwargs['dhcpv6_ia_type'].upper():
                dhcp_args['server_emulation_mode'] = "DHCPV6_PD"
 
        if 'pool_prefix_start' in kwargs:
            dhcp_args['prefix_pool_start_addr'] = kwargs['pool_prefix_start']
        if 'pool_prefix_length' in kwargs:
            dhcp_args['prefix_pool_prefix_length'] = kwargs['pool_prefix_length']
        if 'pool_prefix_size' in kwargs:
            dhcp_args['prefix_pool_per_server'] = kwargs['pool_prefix_size']
        if 'lease_time' in kwargs:
            dhcp_args['preferred_lifetime'] = kwargs['lease_time']
            dhcp_args['valid_lifetime'] = kwargs['lease_time']
 
    config_status = rt_handle.invoke('emulation_dhcp_server_config', **dhcp_args)
    if config_status['status'] != '1':
        result['status'] = '0'
    else:
        if dhcp_args['ip_version'] == "4":
            rethandle = config_status['handle']
            rt_handle.dhcpv4_server_handle.append(rethandle['dhcp_handle'])
            result['dhcpv4_server_handle'] = rethandle['dhcp_handle']
        else:
            rethandle = config_status['handle']
            rt_handle.dhcpv6_server_handle.append(rethandle['dhcpv6_handle'])
            result['dhcpv6_server_handle'] = rethandle['dhcpv6_handle']
    return result

def set_dhcp_server(rt_handle, **kwargs):
    """
    change the dhcp server setting
    :param rt_handle:                    RT object
    :param kwargs:
    :return:
    status
    """
    config_status = rt_handle.invoke('emulation_dhcp_server_config', **kwargs)
    print(config_status)
    return config_status['status']


def dhcp_server_action(rt_handle, **kwargs):
    """
    :param rt_handle:                    RT object
    :param kwargs:
     handle:                        dhcp server handle
     action:                        'start' or stop
    :return:
     status
    """
    dhcp_args = dict()
    if 'handle' in kwargs:
        dhcp_args['dhcp_handle'] = kwargs['handle']
    if 'action' in kwargs:
        if 'start' in kwargs['action']:
            dhcp_args['action'] = 'connect'
        if 'stop' in kwargs['action']:
            dhcp_args['action'] = 'reset'

    if 'ip_version' not in kwargs:
        if 'dhcpv6serverconfig' in rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children"):
            dhcp_args['ip_version'] = '6'
        else:
            dhcp_args['ip_version'] = '4'
    else:
        dhcp_args['ip_version'] = kwargs['ip_version']
    result = rt_handle.invoke('emulation_dhcp_server_control', **dhcp_args)
    return result['status']


def verify_traffic_throughput_tester(rt_handle, minimum_rx_percentage=97, mode='l23_test_summary', stream_name=None, verify_by='throughput', instantaneous_rate='0mbps', packet_count=-1, error_tolerance=1, **kwargs):
    """
    Verifies traffic three different ways (throughput/packetcount/rate). Read below for arguments required by the
    different verifications.

    If mode is set to 'all', traffic throughput (percentage of packets received) is the
    only verification available.


    :param minimum_rx_percentage:       Minimum percentage of traffic that must be received to pass. Default is 97.
                                        This only affects verification when verify_by is 'throughout'.

    :param mode:                        Default is 'all'. Can target specific traffic item with mode='traffic_item'

    :param stream_name:                 Name of the stream you want to verify. Mode must be set to 'traffic_item'

    :param verify_by:                   throughput/packetcount/rate. Please note rate is measured INSTANTANEOUSLY.
                                        This means your traffic stream must be running to get a non-zero measurement!

    :param instantaneous_rate           Only required when verify_by is 'rate'. This is the rate you want to verify
                                        against the rate measured by the RT. Example '5mbps'. All rates assumed to
                                        be in units of mbps.

    :param packet_count                 Only required when verify_by is 'packetcount'. Integer value of expected
                                        packet count.

    :param error_tolerance:             Only used in verifications where verify_by is 'rate'. Sets the tolerance
                                        percent for upper/lower bound limits of RX rate. Acceptable inputs are integers
                                        between 1-100. Defaults to 1.

    :param kwargs:
    :return:                            Returns a dictionary containing traffic stats if verification is successful.
                                        Raises an exception if the verification fails.
    """

    rt = t.get_handle(resource='rt0')
    mode = mode.strip()
    error_tolerance = int(error_tolerance)

    if 'all' in mode:
        # Supporting legacy argument 'all'. 'l23_test_summary' gives stats quicker at scale than 'all'
        mode = 'l23_test_summary'
    elif 'l23_test_summary' not in mode and 'traffic_item' not in mode:
        # Sanity checks on mode
        t.log('error', 'Invalid mode. Please try l23_test_summary or traffic_item. You selected: {0}'.format(mode))
        raise Exception

    kwargs['mode'] = mode
    kwargs['verify_by'] = verify_by
    kwargs['stream_name'] = stream_name

    #traffic_dict = rt_handle.invoke('get_traffic_stats', **kwargs)      # mode='all' or mode='traffic_item'
    traffic_dict = get_traffic_stats(rt_handle, **kwargs)      # mode='all' or mode='traffic_item'

    #changed if mode is all to all in mode the condition is  fail  because of white spaces
    #if mode is 'all':
    if 'l23_test_summary' in mode:
        # Aggregate traffic verification
        # Calculate whether [Tx / Rx] * 100 is greater than minimum_rx_percentage
        rx_packets = traffic_dict['aggregate']['rx']['raw_pkt_count']['avg']
        tx_packets = traffic_dict['aggregate']['tx']['raw_pkt_count']['avg']
        if int(tx_packets) > 0:
            throughput_percentage = (int(rx_packets) / int(tx_packets)) * 100
        else:
            throughput_percentage = 0

        if throughput_percentage < int(minimum_rx_percentage):
            # Aggregate throughput is < expected
            t.log('error', 'Observed aggregate throughput of {0}% is less than minimum allowable '
                           'percentage of {1}!'.format(throughput_percentage, minimum_rx_percentage))
            raise Exception
        else:
            # Aggregate throughput is >= expected
            t.log('info', 'Observed aggregate throughput of {0}% is greater than or equal to the '
                          'minimum allowable percentage of {1}! Aggregate traffic throughput '
                          'verified.'.format(throughput_percentage, minimum_rx_percentage))

    elif 'traffic_item' in mode and stream_name is not None:

        # Traffic_item can't work on DUAL Beacause we declare streamName in rt_handle.traffic_item with v4 and v6  --username pyarlagadda
        # Find the traffic_item associated with stream_name
        stream_id = None
        for name in rt_handle.traffic_item:
            if name.endswith(stream_name):
                stream_id = name

        if stream_id is None:
            # Couldn't find the stream, raise exception
            t.log('error', '{0} does not match any configured stream stream names.'.format(stream_name))
            raise Exception
        else:
            # Proceed with verification of valid traffic_item
            if 'throughput' in verify_by:
                # Verify throughput percentage
                rx_packets = traffic_dict['traffic_item'][stream_id]['rx']['total_pkts']
                tx_packets = traffic_dict['traffic_item'][stream_id]['tx']['total_pkts']

                throughput_percentage = (int(rx_packets) / int(tx_packets)) * 100

                if throughput_percentage < int(minimum_rx_percentage):
                    # traffic_item throughput is < expected
                    t.log('error', 'Observed aggregate throughput of {0}% is less than minimum allowable '
                                   'percentage of {1}!'.format(throughput_percentage, minimum_rx_percentage))
                    raise Exception
                else:
                    # traffic_item throughput is >= expected
                    t.log('info', 'Observed aggregate throughput of {0}% is greater than or equal to the '
                                  'minimum allowable percentage of {1}! Aggregate traffic throughput '
                                  'verified.'.format(throughput_percentage, minimum_rx_percentage))

            elif 'rate' in verify_by:
                # Verify measured rate
                t.log("Verify by rate has been selected. Please note that rate statistics will not be available "
                      "unless the stream is actively sending traffic.")

                measured_rx_rate = traffic_dict['traffic_item'][stream_id]['rx']['total_pkt_mbit_rate']

                mbps_rate = instantaneous_rate.split('mbps')

                if len(mbps_rate) is not 2:
                    t.log('error', 'Parsed multiple digits from entered instantaneous_rate of {0}. Please select'
                                   'a valid entry, such as 5mbps'.format(instantaneous_rate))
                    raise Exception

                mbps_rate = mbps_rate[0]
                lower_bound = float(mbps_rate) - (float(error_tolerance) / 100) * float(mbps_rate)
                upper_bound = float(mbps_rate) + (float(error_tolerance) / 100) * float(mbps_rate)

                if float(lower_bound) < float(measured_rx_rate) < float(upper_bound):
                    # Measured rate is within bounds
                    t.log('info', 'Measured traffic rate of {0} is within +/-{1}% range of {2}!'
                          .format(measured_rx_rate, error_tolerance, instantaneous_rate))
                else:
                    # Measured rate is outside of expected bounds
                    t.log('error', 'Measured traffic rate of {0}mbps is NOT within +/-{1}% range of {1}!'
                          .format(measured_rx_rate, instantaneous_rate))
                    raise Exception

            elif 'packetcount' in verify_by:
                # Verify number of packets received
                t.log('info', 'Verify by packet count has been selected.')
                rx_packets = traffic_dict['traffic_item'][stream_id]['rx']['total_pkts']

                if int(rx_packets) == int(packet_count):
                    # Received packets matches amount expected by user
                    t.log('info', '{0} packets received. {1} packets expected.'.format(rx_packets, packet_count))
                else:
                    # Received packets is not equal to amount expected by user
                    t.log('error', '{0} packets received are less than {1} packets expected'
                          .format(rx_packets, packet_count))
                    raise Exception
            else:
                # Invalid verification
                t.log('error', 'You selected an invalid verify_by parameter: {0}. Acceptable values are '
                               'throughtput/rate/packetcount'.format(verify_by))
    else:
        # Invalid mode. Should raise exception rather than falling through and returning traffic_dict
        t.log('error', 'Invalid mode! You selected: {0}. Please try l23_test_summary or traffic_item.'.format(mode))
        raise Exception

    return traffic_dict

#def iptv_command_sequencer (rt_handle, **kwargs):
#    """
#    :param rt_handle:                    RT object
#    :param kwargs:
#     handle:                        PPPoE device handle
#     accessPrt:                     Access port handle
#     uplinkPrt:                     uplink port handle
#     dbName:                        Data base file name
#     iptvVlanSubFilter              inner or outer
#     iptvTypeTest                   CHANNEL_ZAPPING_TEST or CHANNEL_VERIFICATION_TEST
#     iptvTestTime                   seconds (0 - 429496729)
#     ipType                         IPV4 or IPV6
#    :return:
#     status
#    """
#    status = '1'
#    if 'handle' in kwargs and 'accessPrt' in kwargs and 'uplinkPrt' in kwargs:
#        #Sequecer Group
#        seqGrp = rt_handle.invoke('invoke', cmd="stc::create sequencergroupcommand -under system1")
#        #Create Sequencer
#        Sequencer = rt_handle.invoke('invoke', cmd="stc::create sequencer -under system1")
#        rt_handle.invoke('invoke', cmd="stc::config " +Sequencer+ " -sequencerfinalizetype-Targets " +seqGrp)
#        rt_handle.invoke('invoke', cmd="stc::config " +Sequencer+ " -CleanupCommand " +seqGrp)
#        #PPPoE Connect
#        PPPoEConnect = rt_handle.invoke('invoke', cmd="stc::create pppoxconnectcommand  -under " +Sequencer)
#        #PPPoE Connect Wait
#        PPPoEConnectWait = rt_handle.invoke('invoke', cmd="stc::create pppoxconnectwaitcommand  -under " +Sequencer)
#        rt_handle.invoke('invoke', cmd="stc::config " +PPPoEConnectWait+ " -WaitTime 300" )
#        #DHCPv6 Bind
#        dhcpv6Bind = rt_handle.invoke('invoke', cmd="stc::create dhcpv6bindcommand  -under " +Sequencer)
#        #DHCPv6 Connect Wait
#        dhcpv6BindWait = rt_handle.invoke('invoke', cmd="stc::create dhcpv6bindwaitcommand  -under " +Sequencer)
#        rt_handle.invoke('invoke', cmd="stc::config " +dhcpv6BindWait+ " -WaitTime 300" )
#        #Arp Start on all devices
#        portHandles = "{" +rt_handle.invoke('invoke', cmd="stc::get project1 -children-port")+ "}"
#        arpStart = rt_handle.invoke('invoke', cmd="stc::create arpndstartonalldevicescommand -under " +Sequencer)
#        rt_handle.invoke('invoke', cmd="stc::config " +arpStart+ " -PortList " +portHandles)
#        #Start traffic
#        genStart = rt_handle.invoke('invoke', cmd="stc::create generatorstartcommand  -under " +Sequencer)
#        gen = rt_handle.invoke('invoke', cmd="stc::get " +kwargs['uplinkPrt']+  " -children-generator")
#        rt_handle.invoke('invoke', cmd="stc::config " +genStart+ " -GeneratorList " +gen)
#        #IPTV Start
#        iptvStart = rt_handle.invoke('invoke', cmd="stc::create iptvstarttestcommand  -under " +Sequencer)
#        if 'iptvVlanSubFilter' in kwargs:
#            rt_handle.invoke('invoke', cmd="stc::config " +iptvStart+ " -VlanSubFilter " +kwargs['iptvVlanSubFilter'])
#        if 'iptvTypeTest' in kwargs:
#            rt_handle.invoke('invoke', cmd="stc::config " +iptvStart+ " -TypeOfTest " +kwargs['iptvTypeTest'])
#        if 'iptvTestTime' in kwargs:
#            rt_handle.invoke('invoke', cmd="stc::config " +iptvStart+ " -TestTime " +kwargs['iptvTestTime'])
#        #IPTV wait for test completion
#        iptvWait = rt_handle.invoke('invoke', cmd="stc::create iptvwaitfortestcompletioncommand  -under " +Sequencer)
#        #Stop traffic
#        genStop = rt_handle.invoke('invoke', cmd="stc::create generatorstopcommand  -under " +Sequencer)
#        rt_handle.invoke('invoke', cmd="stc::config " +genStop+ " -GeneratorList " +gen)
#        #Stop Analyzer
#        anaStop = rt_handle.invoke('invoke', cmd="stc::create analyzerstopcommand  -under " +Sequencer)
#        #PPPoE Disconnect
#        PPPoEDisConnect = rt_handle.invoke('invoke', cmd="stc::create pppoxdisconnectcommand  -under " +Sequencer)
#        #PPPoE DisConnect wait
#        PPPoEDisConnectWait = rt_handle.invoke('invoke', cmd="stc::create pppoxdisconnectwaitcommand  -under " +Sequencer)
#        rt_handle.invoke('invoke', cmd="stc::config " +PPPoEDisConnectWait+ " -WaitTime 300")
#        #DHCPv6 Release
#        dhcpv6Rl = rt_handle.invoke('invoke', cmd="stc::create dhcpv6releasecommand -under " +Sequencer)
#        #DHCPv6 Release wait
#        dhcpv6RlWait = rt_handle.invoke('invoke', cmd="stc::create dhcpv6releasewaitcommand  -under " +Sequencer)
#        rt_handle.invoke('invoke', cmd="stc::config " +dhcpv6RlWait+ " -WaitTime 300")
#        #Configure Session handles
#        for dev in kwargs['handle']:
#            PPPoEblk = rt_handle.invoke('invoke', cmd="stc::get " +dev+  " -children-pppoeclientblockconfig")
#            rt_handle.invoke('invoke', cmd="stc::config " +PPPoEConnect+ " -BlockList " +PPPoEblk)
#            rt_handle.invoke('invoke', cmd="stc::config " +PPPoEConnectWait+ " -ObjectList " +dev)
#            rt_handle.invoke('invoke', cmd="stc::config " +PPPoEDisConnect+ " -BlockList " +PPPoEblk)
#            rt_handle.invoke('invoke', cmd="stc::config " +PPPoEDisConnectWait+ " -ObjectList " +dev)
#            iptvBlk = rt_handle.invoke('invoke', cmd="stc::get " +dev+  " -children-iptvstbblockconfig")
#            rt_handle.invoke('invoke', cmd="stc::config " +iptvStart+ " -StbBlockList " +iptvBlk)
#            rt_handle.invoke('invoke', cmd="stc::config " +dhcpv6Bind+ " -BlockList " +dev)
#            rt_handle.invoke('invoke', cmd="stc::config " +dhcpv6BindWait+ " -ObjectList " +dev)
#            rt_handle.invoke('invoke', cmd="stc::config " +dhcpv6Rl+ " -BlockList " +dev)
#            rt_handle.invoke('invoke', cmd="stc::config " +dhcpv6RlWait+ " -ObjectList " +dev)
#        for port in kwargs['accessPrt']:
#            analyzer = rt_handle.invoke('invoke', cmd="stc::get " +port+  " -children-analyzer")
#            rt_handle.invoke('invoke', cmd="stc::config " +anaStop+ " -AnalyzerList " +analyzer)
#        #Configure Command Sequencer
#        if 'IPV6' in kwargs['ipType']:
#           seq_cmd = "{" + PPPoEConnect + " " + PPPoEConnectWait + " " + dhcpv6Bind + " " +dhcpv6BindWait+ " " + arpStart + " " + genStart + " " + iptvStart + " " + iptvWait + " "+ genStop + " " + anaStop + " " +dhcpv6Rl+ " " +dhcpv6RlWait+ " " + PPPoEDisConnect + " "+ PPPoEDisConnectWait +"}"
#        else:
#           seq_cmd = "{" + PPPoEConnect + " " + PPPoEConnectWait + " " + arpStart + " " + genStart + " " + iptvStart + " " + iptvWait + " "+ genStop + " " + anaStop + " "+ PPPoEDisConnect + " "+ PPPoEDisConnectWait +"}"
#        rt_handle.invoke('invoke', cmd="stc::config " +Sequencer+ " -commandList "+seq_cmd)
#    # Create CSV File on log directory
#    if 'dbName' in kwargs:
#        log_dir = t.t_dict['resources']['rt0']['system']['dh'].log_dir
#        os.makedirs(name=log_dir + '/Results', exist_ok=True)
#        db_Path = log_dir + '/Results' + '/' +kwargs['dbName'] + ".db"
#        #IptvAggregateResults
#        aggCsv_Path = log_dir + '/Results' + '/' +kwargs['dbName'] + "_AggregateResults.csv"
#        rt_handle.invoke('invoke', cmd="stc::perform SaveResult -SaveDetailedResults true -SaveToDatabase true -OverwriteIfExist true -DatabaseConnectionString  " +db_Path)
#        aggResults = "/volume/labtools/lib/Spirent/Spirent_TestCenter_4.75/Spirent_TestCenter_Application_Linux/results_reporter/ResultsReporterCLI.sh -o " +db_Path+ "  -f csv -d  " +aggCsv_Path+ " -t /volume/labtools/lib/Spirent/Spirent_TestCenter_4.75/Spirent_TestCenter_Application_Linux/results_reporter/templates/IptvAggregateResultsTemplate.rtp  --StartIndex 0"
#        os.system(aggResults)
#
#    return status

#def bkupcreate_pattern_modifier_list(**kwargs):
#    returnList = []
#    num = int()
#    if kwargs['noMod'] == 0:
#        num = kwargs['start']
#    repeatFlag = 1
#    while len(returnList) < kwargs['count']:
#        if kwargs['noMod']:
#            returnList.append(kwargs['suffix'])
#        else:
#            if '?' in kwargs['suffix']:
#                returnList.append(kwargs['suffix'].replace('?', format(num)))
#            else:
#                returnList.append(kwargs['suffix'] + format(num))
#
#            if repeatFlag < kwargs['repeat']:
#                repeatFlag += 1
#            else:
#                num = num + int(kwargs['step'])
#                repeatFlag = 1
#                if num == kwargs['start'] + (kwargs['length'])*kwargs['step']:
#                    num = kwargs['start']
#    return returnList
#
#def bkupcreate_modifier_list(**kwargs):
#    returnList = []
#    num = 0
#    repeatFlag = 1
#    while len(returnList) < kwargs['count']:
#        if kwargs['noMod']:
#            returnList.append(kwargs['start'])
#        else:
#            returnList.append(kwargs['start'] + num)
#
#            if repeatFlag < kwargs['repeat']:
#                repeatFlag += 1
#            else:
#                repeatFlag = 1
#                #if kwargs['start']+num > kwargs['length']:
#                #    num = kwargs['length']-kwargs['start']
#                if kwargs['start']+num < 4094:
#                    num = num + int(kwargs['step'])
#                #if num >= kwargs['length']:
#                #    num = 0
#    return returnList

def create_modifier_list(**kwargs):
    """
    This is an internal fucntion to create a list of values that is used as
    an input to the modifier
    """
    return_list = []
    #num = 0
    #repeat_flag = 1
    start = kwargs['start']
    step = kwargs['step']
    repeat = kwargs['repeat']
    #length = kwargs['length']
    lines_per_node = kwargs['lines_per_node']
    if repeat == 0:
        repeat = 1
    while len(return_list) < kwargs['count']:
        if kwargs['noMod']:
            return_list.append(kwargs['start'])
        else:
            hex_start = '{:08x}'.format(start, 'x')
            hex_step = '{:08x}'.format(step, 'x')
            wildcard_string = "@\$("+str(hex_start)+","+str(lines_per_node)+","+str(hex_step)+",1, "+str(repeat-1)+")"
            start = start+(lines_per_node*step)
            if start >= 4094:
                start = 4094
                step = 0
        return_list.append(wildcard_string)

    return return_list

def create_pattern_modifier_list(**kwargs):
    """
    This is an internal fucntion to create a list of values that is used as
    an input to the modifier, specifically for patterns.
    """
    return_list = []
    num = int()
    #repeat_flag = 1
    lines_per_node = kwargs['lines_per_node']
    step = kwargs['step']
    repeat = kwargs['repeat']
    suffix = kwargs['suffix']
    count = kwargs['count']
    start = kwargs['start']
    if repeat == 0:
        repeat = 1

    if kwargs['noMod'] == 0:
        num = start

    while len(return_list) < count:
        if kwargs['noMod']:
            return_list.append(suffix)
        else:
            wildcard_string = "@x("+str(num)+","+str(lines_per_node)+","+str(step)+", 1, "+ str(repeat-1)+")"
            if '?' in suffix:
                return_list.append(suffix.replace('?', format(wildcard_string)))
            else:
                return_list.append(suffix + format(wildcard_string))

            num = num + (int(step) * int(lines_per_node))

    return return_list

# Pass thru to modify ancp DSL tlv's:
def emulation_ancp_subscriber_lines_config(rt_handle, **kwargs):
    """
    This is an internal fucntion used to create ANCP subscriber lines
    """
    if kwargs['mode'] == "modify":
        if type(kwargs['handle']) is list:
            h_access_loop_list = kwargs['handle']
        else:
            h_access_loop_list = kwargs['handle'].strip().split()

        # DSL Type mapper
        dsl_type_map = {'adsl1':'01', 'adsl2': '02', 'adsl2_plus': '03', 'vdsl1': '04', 'vdsl2': '05', 'sdsl': '06', 'unknown': '07'}

        for h_dsl_line_profile in h_access_loop_list:
            #h_dsl_line_profile = rt_handle.invoke('invoke', cmd='stc::get '+format(hAccessLoop)+'.ancpsubscribermap -affiliatedsubscriberdsllineprofile-Targets')
            h_tlv = rt_handle.invoke('invoke', cmd='stc::get '+h_dsl_line_profile+' -children-ancptlvconfig')
            if 'actual_rate_downstream' in kwargs:
                orig_frame_config = rt_handle.invoke('invoke', cmd="stc::get "+h_tlv+" -frameconfig")
                match_obj = re.search('.*:(ActualNetDataRateDownstreamTlv"><Length>[0-9]+</Length><Rate>[0-9]+</Rate>).*', orig_frame_config)
                new_rate = re.sub('<Rate>[0-9]+</Rate>', '<Rate>'+format(kwargs['actual_rate_downstream'])+'</Rate>', match_obj.group(1))
                new_frame_config = re.sub(match_obj.group(1), new_rate, orig_frame_config)
                rt_handle.invoke('invoke', cmd="stc::config "+h_tlv+" -frameconfig {"+new_frame_config+"}")
            if 'actual_rate_upstream' in kwargs:
                orig_frame_config = rt_handle.invoke('invoke', cmd="stc::get "+h_tlv+" -frameconfig")
                match_obj = re.search('.*:(ActualNetDataRateUpstreamTlv"><Length>[0-9]+</Length><Rate>[0-9]+</Rate>).*', orig_frame_config)
                new_rate = re.sub('<Rate>[0-9]+</Rate>', '<Rate>'+format(kwargs['actual_rate_upstream'])+'</Rate>', match_obj.group(1))
                new_frame_config = re.sub(match_obj.group(1), new_rate, orig_frame_config)
                rt_handle.invoke('invoke', cmd="stc::config "+h_tlv+" -frameconfig {"+new_frame_config+"}")
            if 'dsl_type' in kwargs:
                orig_frame_config = rt_handle.invoke('invoke', cmd="stc::get "+h_tlv+" -frameconfig")
                match_obj = re.search('.*:(DslTypeTlv"><Length>4</Length><DslType>[0-9]+</DslType>).*', orig_frame_config)
                new_dsl_type = re.sub('<DslType>[0-9]+</DslType>', '<DslType>'+format(dsl_type_map[kwargs['dsl_type']])+'</DslType>', match_obj.group(1))
                new_frame_config = re.sub(match_obj.group(1), new_dsl_type, orig_frame_config)
                rt_handle.invoke('invoke', cmd="stc::config "+h_tlv+" -frameconfig {"+new_frame_config+"}")
        return 1
    else:
        #return rt_handle.invoke('emulation_ancp_subscriber_lines_config', **kwargs)
        return rt_handle.sth.emulation_ancp_subscriber_lines_config(**kwargs)

def set_pppoe_dsl_attribute(rt_handle, **kwargs):
    """
    This is an internal function used to configure the DSL attributes for PPPoE
    """
    handle = kwargs['handle']
    dsl_type_map = {'adsl_1':'00000001', 'adsl_2': '00000002', 'adsl_2_p': '00000003', 'vdsl_1': '00000004', 'vdsl_2': '00000005', 'sdsl': '00000006', 'unknown': '00000007'}

    # Before we create the new TLV's based on the inputs
    # check and delete any previous DSL TLV's. Create a
    # dictionary to track the existing TLV's based on their types.
    # If this API is called to modify a specific TLV, we can refer
    # to this dictionary, delete the TLV and create a new one based
    # on the inputs.
    dsl_tlv_dict = dict()
    if 'vendorspecificdslftag' in rt_handle.invoke('invoke', cmd="stc::get "+handle+" -children-vendorspecificdslftag"):
        dsl_list = rt_handle.invoke('invoke', cmd="stc::get "+handle+" -children-vendorspecificdslftag").strip().split()
        for dsl_tlv in dsl_list:
            tag_type = rt_handle.invoke('invoke', cmd="stc::get "+dsl_tlv+" -tagtype")
            if tag_type == 'ACTUAL_DATA_RATE_UPSTREAM':
                dsl_tlv_dict['upstream_rate'] = dsl_tlv
            elif tag_type == 'ACTUAL_DATA_RATE_DOWNSTREAM':
                dsl_tlv_dict['downstream_rate'] = dsl_tlv
            elif tag_type == 'CUSTOM':
                dsl_tlv_dict['dsltype'] = dsl_tlv


    # Configure Actual Upstream Rate TLV
    if 'upstream_rate' in kwargs:
        # Check and delete if there is an upstream rate TLV already configured
        if 'upstream_rate' in dsl_tlv_dict:
            rt_handle.invoke('invoke', cmd="stc::delete "+dsl_tlv_dict['upstream_rate'])
            del dsl_tlv_dict['upstream_rate']
        rt_handle.invoke('invoke', cmd="stc::create VendorSpecificDslfTag -under "+handle+" -tagtype ACTUAL_DATA_RATE_UPSTREAM -tagdata "+kwargs['upstream_rate'])

    # Configure Actual Downstream Rate TLV
    if 'downstream_rate' in kwargs:
        # Check and delete if there is an downstream rate TLV already configured
        if 'downstream_rate' in dsl_tlv_dict:
            rt_handle.invoke('invoke', cmd="stc::delete "+dsl_tlv_dict['downstream_rate'])
            del dsl_tlv_dict['downstream_rate']
        rt_handle.invoke('invoke', cmd="stc::create VendorSpecificDslfTag -under "+handle+" -tagtype ACTUAL_DATA_RATE_DOWNSTREAM -tagdata "+kwargs['downstream_rate'])

    # Configure DSL Type TLV
    if 'dsltype' in kwargs:
        # Check and delete if there is an DSL type TLV already configured
        if 'dsltype' in dsl_tlv_dict:
            rt_handle.invoke('invoke', cmd="stc::delete "+dsl_tlv_dict['dsltype'])
            del dsl_tlv_dict['dsltype']
        rt_handle.invoke('invoke', cmd="stc::create VendorSpecificDslfTag -under "+handle+" -tagtype CUSTOM -TagLength 4 -CustomTag 145 -CustomTagData "+dsl_type_map[kwargs['dsltype']])

    rt_handle.invoke('invoke', cmd="stc::apply")
    return 1

def add_ancp(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    count:                      ANCP node count
    lines_per_node:             subscriber lines per ancp node
    dut_ip:                     router loopback ip address
    port                        physical tester port
    vlan_start:                 ancp vlan id
    vlan_step:                  ancp vlan increase step
    vlan_repeat:                ancp vlan repeat number
    vlan_length:                ancp vlan sequence length
    svlan_start:                ancp svlan id
    svlan_step:                 ancp svlan increase step
    svlan_repeat:               ancp svlan repeat number
    svlan_length:               ancp svlan sequence length
    ip_addr:                    ip address
    ip_addr_step:               ip address step
    netmask:                       mask
    gateway:                    gateway address
    ancp_standard:              ancp standard (rfc6320/ietf-ancp-protocol5), by default rfc6320
    keep_alive:                 ancp keepalive timer
    keep_alive_retries:         ancp keepalive retries, by default is 3
    remote_loopback:            1/0
    dsl_type:                   adsl1 adsl2 adsl2_plus vdsl1 vdsl2 sdsl unknown
    vlan_allocation_model:      1_1 or N_1 or disabled, by default is 1_1
    flap_mode:                  none/reset/resynchronize, default is none
    remote_id:                  remote_id string, for example can be "remoteid" or "remoteid?"
    remote_id_start:            remote_id start value
    remote_id_step:             remote_id step value
    remote_id_repeat:           remote_id repeat value
    remote_id_length:           remote_id length
    circuit_id:                 agent_circuit_id string
    circuit_id_start:           circuit_id start value
    circuit_id_step:            circuit_id step value
    circuit_id_repeat:          circuit_id repeat value
    circuit_id_length:          circuit_id length
    enable_remote_id:           1/0, by default is 0
    customer_vlan_start:        the first customer vlan id
    customer_vlan_step:         vlan increase step
    customer_vlan_repeat:       vlan repeat number
    customer_vlan_length:       vlan sequence length
    service_vlan_start:         first service vlan id
    service_vlan_step:          service vlan increase step
    service_vlan_repeat:        svlan repeat number
    service_vlan_length:        svlan sequence length
    :return:                    dictionary of handles: ancp_handle, ancp_subscriber_lines_handle, status
    """

    result = dict()
    result['status'] = '1'

    # Step 1: Create ANCP Node
    ancp_args = dict()
    if 'port' in kwargs:
        port = kwargs.get('port')
        ancp_args['port_handle'] = rt_handle.port_to_handle_map[port]
    ancp_args['ancp_standard'] = kwargs.get('ancp_standard', 'rfc_6320')
    ancp_args['mode'] = 'create'
    ancp_args['topology_discovery'] = '1'
    ancp_args['device_count'] = kwargs['count']
    if 'keep_alive' in kwargs:
        ancp_args['keep_alive'] = kwargs['keep_alive']
    #set up Interface ipv4 addr is Mandatory Argument when mode is create
    if 'ip_addr' in kwargs:
        ancp_args['intf_ip_addr'] = kwargs['ip_addr']
        ancp_args['intf_ip_step'] = kwargs.get('ip_addr_step', '0.0.0.1')
        if 'gateway' in kwargs:
            ancp_args['gateway_ip_addr'] = kwargs['gateway']
            ancp_args['gateway_ip_step'] = kwargs.get('ip_addr_step', '0.0.0.1')
            ancp_args['gateway_ip_repeat'] = 1
    if 'netmask' in kwargs:
        ancp_args['intf_ip_prefix_len'] = IPAddress(kwargs['netmask']).netmask_bits()
    ancp_args['sut_ip_addr'] = kwargs.get('dut_ip', '100.0.0.1')
    ancp_args['vlan_id'] = kwargs['vlan_start']
    ancp_args['vlan_id_count'] = kwargs['vlan_length']
    ancp_args['vlan_id_step'] = kwargs['vlan_step']
    ancp_args['tcp_port'] = '6068'

    ancp_status = rt_handle.invoke('emulation_ancp_config', **ancp_args)
    if ancp_status['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to create ANCP Router for port handle {}".format(ancp_args['port_handle']))

    # Retrieve the ANCP handles list and populate the return dict and rt_handle dict
    ancp_handle = ancp_status['handle'].strip().split() # Should be a list of handles
    rt_handle.ancp_handle += ancp_handle
    result['ancp_handle'] = ancp_handle

    # The emulation_ancp_config API creates on AncpAccessLoopBlockConfig by default.
    # The subsequent emulation_ancp_subscriber_lines_config API also creates AncpAccessLoopBlockConfig
    # and uses the newly created AncpAccessLoopBlockConfig for access loop configuration.
    # Hence the default AncpAccessLoopBlockConfig created by emulation_ancp_config is
    # left idle without proper subscriber, DSL line profile and ANCP TLV association.
    # Hence, delete the default AncpAccessLoopBlockConfig created by emulation_ancp_config API
    for hAncpDevice in ancp_handle:
        if 'ancpaccessloopblockconfig' in rt_handle.invoke('invoke', cmd='stc::get '+hAncpDevice+'.ancpaccessnodeconfig -children-AncpAccessLoopBlockConfig'):
            hTmpAncpAccessLoopBlockConfig = rt_handle.invoke('invoke', cmd='stc::get '+hAncpDevice+'.ancpaccessnodeconfig -children-AncpAccessLoopBlockConfig')
            rt_handle.invoke('invoke', cmd='stc::delete '+hTmpAncpAccessLoopBlockConfig)

    # Step 2: Create a dummy host that will act as the subscriber behind the access loop
    linesPerNode = kwargs.get('lines_per_node', 1)
    deviceArgs = {'mode':"create", 'port_handle': rt_handle.port_to_handle_map[port], 'count':linesPerNode, 'intf_ip_addr':"192.168.0.2", 'gateway_ip_addr':"192.168.0.1"}
    deviceStatus = rt_handle.invoke('emulation_device_config', **deviceArgs)
    #ethIf = rt_handle.invoke('invoke', cmd='stc::get '+format(deviceStatus['handle'])+' -children-ethiiif')
    h_host = deviceStatus['handle']

    # Get the handles of the devices created
    deviceHandles = ancp_status['handle'].strip().split()

    #rt_handle.ancp_line_args = kwargs

    # Step 3: Create the Access loops and configure the TLV's and DSL profile.
    # Create the modifier lists
    modCount = kwargs['count']

    # Step 3.1: Circuit ID modifier list
    if 'circuit_id' in kwargs:
        suffix = kwargs['circuit_id']
        if 'circuit_id_start' in kwargs:
            modStart = int(kwargs.get('circuit_id_start'))
            modStep = int(kwargs.get('circuit_id_step', 1))
            modRepeat = int(kwargs.get('circuit_id_repeat', 1))
            modLength = int(kwargs.get('circuit_id_length', 0))
            circuitIdList = create_pattern_modifier_list(start=modStart, suffix=suffix, step=modStep, repeat=modRepeat, length=modLength, count=modCount, noMod=0, lines_per_node=linesPerNode)
        else:
            circuitIdList = create_pattern_modifier_list(circuit_id="ACI", count=modCount, noMod=1)

    # Step 3.2: Service VLAN:
    if 'service_vlan_start' in kwargs:
        modStart = kwargs.get('service_vlan_start')
        modStep = kwargs.get('service_vlan_step', 1)
        modRepeat = kwargs.get('service_vlan_repeat', 1)
        modLength = kwargs.get('service_vlan_length', 4094)
        sVlanIdList = create_modifier_list(noMod=0, start=modStart, step=modStep, repeat=modRepeat, length=modLength, count=modCount, lines_per_node=linesPerNode)

    # Step 3.3: Customer VLAN:
    if 'customer_vlan_start' in kwargs:
        modStart = kwargs.get('customer_vlan_start')
        modStep = kwargs.get('customer_vlan_step', 1)
        modRepeat = kwargs.get('customer_vlan_repeat', 1)
        modLength = kwargs.get('customer_vlan_length', 4094)
        cVlanIdList = create_modifier_list(noMod=0, start=modStart, step=modStep, repeat=modRepeat, length=modLength, count=modCount, lines_per_node=linesPerNode)

    # Step 3.4:  Device handle list
    deviceHandlesList = []
    for deviceHandle in deviceHandles:
        deviceHandlesList.append(deviceHandle)

    # Step 3.5: DSL rate - no code in ixiatester.py. Setting it to default 300
    rateUpStream = 300
    rateDownStream = 300

    # Create the subscriber line configs
    hCommonDslLineProfile = str()
    result['ancp_subscriber_lines_handle'] = []
    for index in range(modCount):
        lineConfigArgs = {'ancp_client_handle':deviceHandlesList[index], 'handle':h_host, 'data_link':'ethernet', 'dsl_type': kwargs['dsl_type'], 'mode':'create', 'actual_rate_upstream': rateUpStream, 'actual_rate_downstream': rateDownStream, 'subscriber_lines_per_access_node':linesPerNode}
        if 'circuit_id' in kwargs:
            lineConfigArgs['circuit_id'] = "{"+circuitIdList[index]+"}"
        if 'service_vlan_start' in kwargs:
            lineConfigArgs['tlv_service_vlan_id'] = "{"+sVlanIdList[index]+"}"
            lineConfigArgs['tlv_service_vlan_id_wildcard'] = 1
        if 'customer_vlan_start' in kwargs:
            lineConfigArgs['tlv_customer_vlan_id'] = "{"+cVlanIdList[index]+"}"
            lineConfigArgs['tlv_customer_vlan_id_wildcard'] = 1

        lineConfigResult = rt_handle.invoke('emulation_ancp_subscriber_lines_config', **lineConfigArgs)
        if lineConfigResult['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create ANCP subscriber line handles")

        # Retrieve the handles of the access loop and the associated DSL line profile.
        hAccessLoop = lineConfigResult['ancp_subscriber_lines_handle'].strip()
        h_dsl_line_profile = rt_handle.invoke('invoke', cmd='stc::get '+format(hAccessLoop)+'.ancpsubscribermap -affiliatedsubscriberdsllineprofile-Targets')

        # TO DO: Circuit ID Wildcard edit
        if 'circuit_id' in lineConfigArgs:
            rt_handle.invoke('invoke', cmd='stc::create AncpWildcardModifier -under '+format(hAccessLoop)+'.ancptlvconfig -OffsetReference {proto1.ID} -Data '+lineConfigArgs['circuit_id'])

        # The emulation_ancp_subscriber_lines_config API creates a DSL line profile everytime
        # it is called. All the DSL line profiles created have the same parameters.
        # When the user test case calls the emulation_ancp_subscriber_lines_config API
        # with mode as modify to change some of the DSL line parameters, we have to change
        # all the created DSL line profiles. This is not optimal design and also increases
        # the run time. The below loop will get the handle of the first DSL line profile
        # and associates it as the common DSL line profile for all the access loops being created.
        # That way, when the user script tries to modify the DSL line parameters, it is sufficient
        # if we change it on the one common DSL line profile.

        if index == 0:
            # First DSL line profile.
            hCommonDslLineProfile = h_dsl_line_profile
        else:
            # Associate the first DSL line profile and delete the existing redundant line profile
            rt_handle.invoke('invoke', cmd='stc::config '+format(hAccessLoop)+'.ancpsubscribermap -AffiliatedSubscriberDslLineProfile-targets '+hCommonDslLineProfile)
            rt_handle.invoke('invoke', cmd='stc::config '+format(hAccessLoop)+' -AffiliatedAncpDslLineProfile-targets '+hCommonDslLineProfile)
            rt_handle.invoke('invoke', cmd='stc::delete '+h_dsl_line_profile)

    # Retrieve the handles of the subscriber lines (access loops) and update
    # the result and rt_handle dicts
    rt_handle.ancp_line_handle += hCommonDslLineProfile.strip().split()
    result['ancp_subscriber_lines_handle'] += hCommonDslLineProfile.strip().split()

    # Return
    rt_handle.invoke('invoke', cmd='stc::apply')
    return result

#def add_ancp_subscriber_lines_config(rt_handle, **kwargs):
#    """
#    :param rt_handle:
#    :param kwargs:
#    lines_per_node:             subscriber lines per ancp node
#    port                        physical tester port
#    ip_addr:                    ip address
#    ip_addr_step:               ip address step
#    mask:                       mask
#    gateway:                    gateway address
#    ancp_standard:              ancp standard (rfc6320/ietf-ancp-protocol5), by default rfc6320
#    keep_alive:                 ancp keepalive timer
#    keep_alive_retries:         ancp keepalive retries, by default is 3
#    remote_loopback:            1/0
#    dsl_type:                   adsl1 adsl2 adsl2_plus vdsl1 vdsl2 sdsl unknown
#    vlan_allocation_model:      1_1 or N_1 or disabled, by default is 1_1
#    flap_mode:                  none/reset/resynchronize, default is none
#    remote_id:                  remote_id string, for example can be "remoteid" or "remoteid?"
#    remote_id_start:            remote_id start value
#    remote_id_step:             remote_id step value
#    remote_id_repeat:           remote_id repeat value
#    remote_id_length:           remote_id length
#    circuit_id:                 agent_circuit_id string
#    circuit_id_start:           circuit_id start value
#    circuit_id_step:            circuit_id step value
#    circuit_id_repeat:          circuit_id repeat value
#    circuit_id_length:          circuit_id length
#    enable_remote_id:           1/0, by default is 0
#    customer_vlan_start:        the first customer vlan id
#    customer_vlan_step:         vlan increase step
#    customer_vlan_repeat:       vlan repeat number
#    customer_vlan_length:       vlan sequence length
#    service_vlan_start:         first service vlan id
#    service_vlan_step:          service vlan increase step
#    service_vlan_repeat:        svlan repeat number
#    service_vlan_length:        svlan sequence length
#    :return:                    dictionary of handles: ancp_handle, ancp_subscriber_lines_handle, status
#    """
#    #Create Subscriber Line Config
#    line_args = dict()
#    result = dict()
#    line_args['mode'] = 'create'
#    line_args['handle'] = kwargs['handle']
#    line_args['ancp_client_handle'] = rt_handle.ancp_handle
#    line_args['subscriber_lines_per_access_node'] = kwargs.get('lines_per_node', '1')
#    line_args['dsl_type'] = kwargs.get('dsl_type', "adsl1")
#    #Circuit Id configuration
#    if 'circuit_id' in kwargs:
#        line_args['circuit_id'] = kwargs['circuit_id']
#    if 'circuit_id_start' in kwargs:
#        line_args['circuit_id_suffix'] = kwargs.get('circuit_id_start')
#    if 'circuit_id_step' in kwargs:
#        line_args['circuit_id_suffix_step'] = kwargs.get('circuit_id_step', '1')
#    if 'circuit_id_repeat' in kwargs:
#        line_args['circuit_id_suffix_repeat'] = int(kwargs.get('circuit_id_repeat', '1'))-1
#    #Remote Id configuration
#    if 'remote_id' in kwargs:
#        line_args['remote_id'] = kwargs.get('remote_id')
#    if 'remote_id_start' in kwargs:
#        line_args['remote_id_suffix'] = kwargs.get('remote_id_start')
#    if 'remote_id_step' in kwargs:
#        line_args['remote_id_suffix_step'] = kwargs.get('remote_id_step', '1')
#    if 'remote_id_repeat' in kwargs:
#        line_args['remote_id_suffix_repeat'] = int(kwargs.get('remote_id_repeat', '1'))-1
#    #AccessAggregationCircuitIdBinaryVlanTlv
#    #customer_vlan Id Configuration
#    #if 'customer_vlan_start' in kwargs:
#    #    line_args['tlv_customer_vlan_id'] = kwargs.get('customer_vlan_start','0')
#    #    line_args['tlv_customer_vlan_id_wildcard'] = "0"
#    #customer_vlan Id wildcard Configuration
#    #if 'customer_vlan_step' in kwargs:
#    #    start = kwargs.get('customer_vlan_start')
#    #    step = kwargs.get('customer_vlan_step', '1')
#    #    repeat = int(kwargs.get('customer_vlan_repeat', '1'))-1
#    #    if repeat < 0:
#    #       repeat = 0
#    #    line_args['tlv_customer_vlan_id'] = '@x({},0,{},0,{})'.format(start, step, repeat)
#    #    line_args['tlv_customer_vlan_id_wildcard'] = "1"
#    #service_vlan Id Configuration
#    #if 'service_vlan_start' in kwargs:
#    #   line_args['tlv_service_vlan_id'] = kwargs.get('service_vlan_start','0')
#    #   line_args['tlv_service_vlan_id_wildcard'] = "0"
#    #service_vlan Id wild card Configuration
#    #if 'service_vlan_step' in kwargs:
#    #    start = kwargs.get('service_vlan_start')
#    #    step = kwargs.get('service_vlan_step', '1')
#    #    repeat = int(kwargs.get('service_vlan_repeat', '1'))-1
#    #    if repeat < 0:
#    #       repeat = 0
#    #    line_args['tlv_service_vlan_id'] = '@x({},0,{},0,{})'.format(start, step, repeat)
#    #    line_args['tlv_service_vlan_id_wildcard'] = "1"
#
#    ancp_subscriber_lines_status = rt_handle.invoke('emulation_ancp_subscriber_lines_config', **line_args)
#    if ancp_subscriber_lines_status['status'] != '1':
#       result['status'] ='0'
#       raise Exception("failed to create ANCP Subscriber line for port handle {}".format(port_handle))
#    ancp_subscriber_lines_handle = ancp_subscriber_lines_status['handle']
#    result['ancp_subscriber_lines_handle'] = ancp_subscriber_lines_handle
#    rt_handle.ancp_line_handle.append(ancp_subscriber_lines_handle)
#    return result

def ancp_action(rt_handle, **kwargs):
    """

    :param rt_handle:
    :param kwargs:
    handle:             ancp_handle
    action:             start/stop/abort
    :return:
    """
    ancp_handle = kwargs['handle']
    action = kwargs['action']
    action_control = str()
    #Initiate the ANCP Adjacency
    if 'start' in action:
        action_control = "start"
        action = "initiate"
    #Stop the ANCP Adjacency
    elif 'stop' in action:
        action_control = "stop"
        action = "initiate"
    return rt_handle.invoke('emulation_ancp_control', ancp_handle=ancp_handle, action=action, action_control=action_control)


def ancp_line_action(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    handle:             ancp_handle
    action:             flap_start/flat_stop/flap_start_resync/port_up/port_down
    :return:
    """
    ancp_handle = kwargs['handle']
    action = kwargs['action']
    action_control = str()
    #Start the Flapping operation on the Subscriber line
    if 'flap_start' in action:
        action = 'flap_start'
        action_control = 'start'
    #Stop the Flapping operation on the Subscriber line
    elif 'flap_stop' in action:
        action = 'flap_stop'
        action_control = 'stop'
    elif 'flap_start_resync' in action:
        action = 'flap_start'
        action_control = 'start'
    #Sends ANCP port up messages
    elif 'port_up' in action:
        action = 'send'
        action_control = 'start'
    #Sends ANCP port down messages
    elif 'port_down' in action:
        action = 'send'
        action_control = 'stop'

    #return rt_handle.invoke('emulation_ancp_control',ancp_handle=ANCP_handle,action=action,action_control=action_control,ancp_subscriber=sub_handle)
    return rt_handle.invoke('emulation_ancp_control', ancp_handle=ancp_handle, action=action, action_control=action_control)

def add_igmp_client(rt_handle, **kwargs):
    """
    :param rt_handle:                    RT object
    :param kwargs:
    handle:                         dhcp client handle or pppoe client handle
    version:                        version 2 or 3, default is 2
    filter_mode:                    include/exclude, default is include
    iptv:                           1 or 0, default is 0
    group_range:                    multicast group range, default is 1
    group_range_step:               the pattern that the range start address, default is 0.0.1.0
    group_start_addr:               multicast group start address
    group_step:                     group step pattern
    group_count:                    group counts
    src_grp_range:                  multicast source group range, default is 1
    src_grp_range_step:             multicast source group range step pattern, default is 0.0.1.0
    src_grp_start_addr:             multicast source group start address
    src_grp_step:                   multicast soutce group step pattern, default is 0.0.0.1
    src_grp_count:                  multicast source group count

    :return:
    result                          a dictionary include status, igmp_host_handle, igmp_group_handle, igmp_source_handle
    """
    result = dict()
    result['status'] = '1'
    #Configure IGMP host
    igmp_param = dict()
    igmp_param['handle'] = kwargs.get('handle')
    igmp_param['mode'] = kwargs.get('mode', 'create')
    if 'create' in igmp_param['mode']:
        igmp_param['handle'] = rt_handle.invoke('invoke', cmd='stc::get ' + kwargs['handle'] + ' -parent')
    igmp_param['filter_mode'] = kwargs.get('filter_mode', 'include')
    #igmp_param['enable_iptv'] = kwargs.get('iptv', '0')
    igmp_param['igmp_version'] = 'v' + str(kwargs.get('version', '2'))
    _result_ = rt_handle.invoke('emulation_igmp_config', **igmp_param)
    print(_result_)
    if _result_['status'] != '1':
        result['log'] = "failed to add igmp client"
        result['status'] = '0'
        return result
    else:
        igmp_handle = _result_['handle']
        rt_handle.igmp_handles[kwargs.get('handle')] = igmp_handle
        rt_handle.igmp_handle_to_group[igmp_handle] = {}
        result['igmp_host_handle'] = igmp_handle
    #Configure Multicast Group
    mcast_args = dict()
    mcast_args['mode'] = "create"
    mcast_args['ip_addr_start'] = kwargs.get('group_start_addr', '225.0.0.1')
    mcast_args['ip_prefix_len'] = IPAddress(kwargs.get('group_step', "0.0.1.0")).netmask_bits()
    mcast_args['ip_addr_step'] = "1"
    mcast_args['num_groups'] = kwargs.get('group_count', "1")
    _result_ = rt_handle.invoke('emulation_multicast_group_config', **mcast_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
    else:
        igmp_group_handle = _result_['handle']
        rt_handle.igmp_handle_to_group[igmp_handle]['group_handle'] = igmp_group_handle

    #Configure Multicast Source
    src_args = dict()
    src_args['mode'] = "create"
    src_args['ip_addr_start'] = kwargs.get('src_grp_start_addr', "10.10.10.1")
    src_args['ip_prefix_len'] = IPAddress(kwargs.get('src_grp_step', "0.0.1.0")).netmask_bits()
    src_args['ip_addr_step'] = "1"
    src_args['num_sources'] = kwargs.get('src_grp_count', "1")
    _result_ = rt_handle.invoke('emulation_multicast_source_config', **src_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
    else:
        igmp_source_handle = _result_['handle']
        rt_handle.igmp_handle_to_group[igmp_handle]['src_group_handle'] = igmp_source_handle
    #Configure IGMP Group
    grp_args = dict()
    grp_args['mode'] = kwargs.get('mode', "create")
    grp_args['filter_mode'] = kwargs.get('filter_mode', "include")
    grp_args['group_pool_handle'] = igmp_group_handle
    grp_args['session_handle'] = igmp_handle
    grp_args['source_pool_handle'] = igmp_source_handle
    _result_ = rt_handle.invoke('emulation_igmp_group_config', **grp_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        result['log'] = "failed to config the igmp group and src group set"
    else:
        result['igmp_group_handle'] = _result_['handle']
        result['igmp_source_handle'] = igmp_source_handle
        rt_handle.igmp_handle_to_group[igmp_handle]['igmp_group_handle'] = _result_['handle']
        rt_handle.igmp_handle_to_group[igmp_handle]['igmp_source_handle'] = igmp_source_handle

    return result


def igmp_client_action(rt_handle, **kwargs):
    """
    :param rt_handle:                                RT object
    :param kwargs:
    handle:                                     igmp host handle
    action:                                     restart/join/leave
    :return:
    """
    action_param = dict()
    action_param['handle'] = kwargs['handle']
    if 'action' in kwargs:
        action_param['mode'] = kwargs['action']
    return rt_handle.invoke('emulation_igmp_control', **action_param)

def add_mld_client(rt_handle, **kwargs):
    """
    :param rt_handle:                     RT object
    :param kwargs:
     handle:                         dhcpv6 client handle
     version:                        version 1 or 2, default is 1
     filter_mode:                    include/exclude, default is include
     iptv:                           1 or 0, default is 0
     group_range:                    multicast group range, default is 1
     group_range_step:               the pattern that the range start address, default is ::1:0
     group_start_addr:               multicast group start address
     group_step:                     group step pattern, default is ::1
     group_count:                    group counts
     src_grp_range:                  multicast source group range, default is 1
     src_grp_range_step:             multicast source group range step pattern, default is ::1:0
     src_grp_start_addr:             multicast source group start address
     src_grp_step:                   multicast soutce group step pattern, default is ::1
     src_grp_count:                  multicast source group count

     :return:
     result                          a dictionary include status, mld_host_handle, mld_group_handle, mld_source_handle
     """
    result = dict()
    result['status'] = '1'
    #Configure MLD host
    mld_param = dict()
    mld_param['handle'] = kwargs.get('handle')
    mld_param['mode'] = kwargs.get('mode', 'create')
    if 'create' in mld_param['mode']:
        mld_param['handle'] = rt_handle.invoke('invoke', cmd='stc::get ' + kwargs['handle'] + ' -parent')
    mld_param['filter_mode'] = kwargs.get('filter_mode', 'include')
    mld_param['mld_version'] = 'v' + str(kwargs.get('version', '1'))
    _result_ = rt_handle.invoke('emulation_mld_config', **mld_param)
    print(_result_)
    if _result_['status'] != '1':
        result['log'] = "failed to add mld client"
        result['status'] = '0'
        return result
    else:
        mld_handle = _result_['handle']
        rt_handle.mld_handles[kwargs.get('handle')] = mld_handle
        rt_handle.mld_handle_to_group[mld_handle] = {}
        result['mld_host_handle'] = mld_handle
    #Configure Multicast Group
    mcast_args = dict()
    mcast_args['mode'] = "create"
    mcast_args['ip_addr_start'] = ipaddress.IPv6Address(kwargs.get('group_start_addr', 'ff03::1')).exploded
    group_step = ipaddress.IPv6Address(kwargs.get('group_step', "0:0:0:0:0:0:0:1")).exploded
    mcast_args['ip_prefix_len'] = IPAddress(group_step).netmask_bits()
    mcast_args['ip_addr_step'] = "1"
    mcast_args['num_groups'] = kwargs.get('group_count', "1")
    _result_ = rt_handle.invoke('emulation_multicast_group_config', **mcast_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
    else:
        mld_group_handle = _result_['handle']
        rt_handle.mld_handle_to_group[mld_handle]['group_handle'] = mld_group_handle
    #Configure Multicast Source
    src_args = dict()
    src_args['mode'] = "create"
    src_args['ip_addr_start'] = ipaddress.IPv6Address(kwargs.get('src_grp_start_addr', "200::1")).exploded
    src_grp_step = ipaddress.IPv6Address(kwargs.get('src_grp_step', "0:0:0:0:0:0:0:1")).exploded
    src_args['ip_prefix_len'] = IPAddress(src_grp_step).netmask_bits()
    src_args['ip_addr_step'] = "1"
    src_args['num_sources'] = kwargs.get('src_grp_count', "1")
    _result_ = rt_handle.invoke('emulation_multicast_source_config', **src_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
    else:
        mld_source_handle = _result_['handle']
        rt_handle.mld_handle_to_group[mld_handle]['src_group_handle'] = mld_source_handle
    #Configure MLD group Config
    grp_args = dict()
    grp_args['mode'] = kwargs.get('mode', "create")
    grp_args['group_pool_handle'] = mld_group_handle
    grp_args['session_handle'] = mld_handle
    _result_ = rt_handle.invoke('emulation_mld_group_config', **grp_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        result['log'] = "failed to config the mld group and src group set"
    else:
        result['mld_group_handle'] = _result_['handle']
        result['mld_source_handle'] = mld_source_handle
        rt_handle.mld_handle_to_group[mld_handle]['mld_group_handle'] = mld_group_handle
        rt_handle.mld_handle_to_group[mld_handle]['mld_source_handle'] = mld_source_handle

    return result


def mld_client_action(rt_handle, **kwargs):
    """
    :param rt_handle:                                RT object
    :param kwargs:
    handle:                                     mld host handle
    action:                                     join/leave/leave_join
    :return:
    """
    action_param = dict()
    action_param['handle'] = kwargs['handle']
    if 'action' in kwargs:
        action_param['mode'] = kwargs['action']
    return rt_handle.invoke('emulation_mld_control', **action_param)

def get_protocol_stats(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param mode:        'global_per_protocol'| 'global_per_port', by default is 'global_per_protocol'
    :param handle:      'pppoeclientblockconfig'| 'dhcpv4blockconfig'|'dhcpv6.blockconfig'
    :return:
    """
    stats_status = dict()
    mode = kwargs.get('mode', 'global_per_protocol')
    if 'handle' in kwargs:
        #Get PPPoE Handles
        if re.match('pppoeclientblockconfig', kwargs['handle']):
            h_pppoe_list = rt_handle.invoke('invoke', cmd='stc::get ' + kwargs['handle'] + '-parent')
        #Get DHCPv4 Handles
        elif re.match('dhcpv4blockconfig', kwargs['handle']):
            h_dhcpv4_list = rt_handle.invoke('invoke', cmd='stc::get ' + kwargs['handle'] + '-parent')
        #Get DHCPv6 Handles
        elif re.match('dhcpv6.blockconfig', kwargs['handle']):
            h_dhcpv6_list = rt_handle.invoke('invoke', cmd='stc::get ' + kwargs['handle'] + '-parent')
    else:
        #Get Device handles form rt_handles
        h_pppoe_list = rt_handle.pppox_client_handle
        h_dhcpv4_list = rt_handle.dhcpv4_client_handle
        h_dhcpv6_list = rt_handle.dhcpv6_client_handle

    # Clear results first
    rt_handle.invoke('invoke', cmd='stc::perform ResultsClearAllProtocolCommand')
    #PPPoE Stats
    pppoesessions_up = pppoesessions_down = pppoesessions_total = pppoesessions_not_started = pppoesetup_avg_rate = pppoeteardown_avg_rate = 0
    for blk_cfg in h_pppoe_list:
        tmp_sessions_up = int(rt_handle.invoke('invoke', cmd='stc::get ' + blk_cfg + '.pppoeclientblockresults -SessionsUp'))
        tmp_sessionstotal = int(rt_handle.invoke('invoke', cmd='stc::get ' + blk_cfg + '.pppoeclientblockresults -Sessions'))
        tmp_sessions_attempted = int(rt_handle.invoke('invoke', cmd='stc::get ' + blk_cfg + '.pppoeclientblockresults -AttemptedCount'))
        tmp_sessions_down = int(rt_handle.invoke('invoke', cmd='stc::get ' + blk_cfg + '.pppoeclientblockresults -FailedConnectCount'))

        if tmp_sessionstotal == tmp_sessions_up:
            tmp_sessions_down = 0
        #tmp_sessions_not_started = tmp_sessionstotal-tmp_sessions_attempted
        ## Sometimes tmp_sessions_attempted will be greater than tmp_sessionstotal (due to retries)
        ## tmp_sessions_not_started should be 0 in those cases.
        #tmp_sessions_not_started = tmp_sessions_not_started if tmp_sessions_not_started > 0 else 0
        tmp_sessions_not_started = tmp_sessionstotal-tmp_sessions_up-tmp_sessions_down
        tmp_sessions_not_started = tmp_sessions_not_started if tmp_sessions_not_started > 0 else 0

        if tmp_sessions_up == 0 and tmp_sessions_not_started == 0:
            # This is the scenario when PPP is stopped. The sessions not started
            # count should equal the total PPP session count.
            tmp_sessions_not_started = tmp_sessionstotal

        pppoesessions_up += tmp_sessions_up
        pppoesessions_down += tmp_sessions_down
        pppoesessions_total += tmp_sessionstotal
        pppoesessions_not_started += tmp_sessions_not_started
        pppoesetup_avg_rate += float(rt_handle.invoke('invoke', cmd='stc::get ' + blk_cfg + '.pppoeclientblockresults -SuccSetupRate').strip())
        pppoe_host = rt_handle.invoke('invoke', cmd='stc::get ' + blk_cfg + ' -parent')
        pppoe_hport = rt_handle.invoke('invoke', cmd='stc::get ' + pppoe_host + ' -affiliationPORT-Targets')
        pppoeteardown_avg_rate += float(rt_handle.invoke('invoke', cmd='stc::get ' + pppoe_hport + '.PppoxPortConfig -DisconnectRate'))
    #DHCPv4 Stats
    dhcpv4_sessions_up = dhcpv4_sessions_down = dhcpv4_sessions_total = dhcpv4_sessions_not_started = dhcpv4_setup_avg_rate = dhcpv4_teardown_avg_rate = 0
    for blk_cfg in h_dhcpv4_list:
        dhcpv4_host = rt_handle.invoke('invoke', cmd='stc::get ' + blk_cfg + ' -parent')
        dhcpv4_h_port = rt_handle.invoke('invoke', cmd='stc::get ' + dhcpv4_host + ' -affiliationPORT-Targets')
        stats_status = dhcp_client_stats(rt_handle, mode='session', handle=blk_cfg, ip_version='4')

        tmp_dhcpv4_sessions_up = int(stats_status['group'][blk_cfg]['currently_bound'])
        tmp_dhcpv4_sessions_down = int(stats_status['group'][blk_cfg]['currently_idle'])
        tmp_dhcpv4_sessions_total = int(rt_handle.invoke('invoke', cmd='stc::get ' + dhcpv4_host + ' -DeviceCount'))
        tmp_dhcpv4_sessions_not_started = int(stats_status['group'][blk_cfg]['currently_idle'])

        if tmp_dhcpv4_sessions_up == 0 and tmp_dhcpv4_sessions_not_started == 0:
            # This is the scenario when DHCP is stopped. The sessions not started
            # count should equal the total DHCP session count.
            tmp_dhcpv4_sessions_not_started = tmp_dhcpv4_sessions_total

        dhcpv4_sessions_up += tmp_dhcpv4_sessions_up
        dhcpv4_sessions_down += tmp_dhcpv4_sessions_down
        dhcpv4_sessions_total += tmp_dhcpv4_sessions_total
        dhcpv4_sessions_not_started += tmp_dhcpv4_sessions_not_started

        dhcpv4_setup_avg_rate += float(stats_status['group'][blk_cfg]['attempt_rate'])
        dhcpv4_teardown_avg_rate += float(rt_handle.invoke('invoke', cmd='stc::get ' + dhcpv4_h_port + '.Dhcpv4PortConfig -ReleaseRate'))
    #DHCPv6 Stats
    dhcpv6_sessions_up = dhcpv6_sessions_down = dhcpv6_sessions_total = dhcpv6_sessions_not_started = dhcpv6_setup_avg_rate = dhcpv6_teardown_avg_rate = 0
    for blk_cfg in h_dhcpv6_list:
        dhcpv6_h_host = rt_handle.invoke('invoke', cmd='stc::get ' + blk_cfg + ' -parent')
        dhcpv6_h_port = rt_handle.invoke('invoke', cmd='stc::get ' + dhcpv6_h_host + ' -affiliationPORT-Targets')
        stats_status = dhcp_client_stats(rt_handle, mode='session', handle=dhcpv6_h_host, ip_version='6')

        tmp_dhcpv6_sesssions_total = int(rt_handle.invoke('invoke', cmd='stc::get ' + dhcpv6_h_host + ' -DeviceCount'))
        tmp_dhcpv6_sessions_up = int(stats_status['ipv6']['aggregate']['currently_bound'])
        tmp_dhcpv6_sessions_down = int(stats_status['ipv6']['aggregate']['currently_idle'])
        tmp_dhcpv6_sessions_not_started = int(stats_status['ipv6']['aggregate']['currently_idle'])

        if tmp_dhcpv6_sessions_up == 0 and tmp_dhcpv6_sessions_not_started == 0:
            # This could be a DHCPv6oPPP emulation. Device counts do not
            # get updated till PPP is up. Set idle count to device count
            tmp_dhcpv6_sessions_not_started = tmp_dhcpv6_sesssions_total

        dhcpv6_sessions_up += tmp_dhcpv6_sessions_up
        dhcpv6_sessions_down += tmp_dhcpv6_sessions_down
        dhcpv6_sessions_total += tmp_dhcpv6_sesssions_total
        dhcpv6_sessions_not_started += tmp_dhcpv6_sessions_not_started

        dhcpv6_setup_avg_rate += float(stats_status['ipv6']['aggregate']['setup_success_rate'])
        dhcpv6_teardown_avg_rate += float(rt_handle.invoke('invoke', cmd='stc::get ' + dhcpv6_h_port + '.Dhcpv6PortConfig -ReleaseRate'))

    # Return stats dict
    return_stats_dict = dict()
    #Get global pet protocol stats
    if 'global_per_protocol' in mode:
        # Declare the multi-level dict with default values
        access_prtl = ['PPPoX Client', 'DHCPv4 Client', 'DHCPv6 Client']
        for access in access_prtl:
            return_stats_dict.setdefault('global_per_protocol', {}).setdefault(access, {}).setdefault('sessions_up', 0)
            return_stats_dict.setdefault('global_per_protocol', {}).setdefault(access, {}).setdefault('sessions_down', 0)
            return_stats_dict.setdefault('global_per_protocol', {}).setdefault(access, {}).setdefault('sessions_total', 0)
            return_stats_dict.setdefault('global_per_protocol', {}).setdefault(access, {}).setdefault('sessions_not_started', 0)
            return_stats_dict.setdefault('global_per_protocol', {}).setdefault(access, {}).setdefault('setup_avg_rate', 0)
            return_stats_dict.setdefault('global_per_protocol', {}).setdefault(access, {}).setdefault('teardown_avg_rate', 0)
        #PPPoE Protocol Stats
        #Number of PPPoE Sessions Up
        return_stats_dict['global_per_protocol']['PPPoX Client']['sessions_up'] = pppoesessions_up
        #Number of PPPoE Session Down
        return_stats_dict['global_per_protocol']['PPPoX Client']['sessions_down'] = pppoesessions_down
        #Number of PPPoE Sessions
        return_stats_dict['global_per_protocol']['PPPoX Client']['sessions_total'] = pppoesessions_total
        #Number of PPPoE sessions not started
        return_stats_dict['global_per_protocol']['PPPoX Client']['sessions_not_started'] = pppoesessions_not_started
        #PPPoE SetUp Avg Rate
        return_stats_dict['global_per_protocol']['PPPoX Client']['setup_avg_rate'] = 0
        #PPPoE teardown Avg Rate
        return_stats_dict['global_per_protocol']['PPPoX Client']['teardown_avg_rate'] = 0
        if len(h_pppoe_list) != 0:
            return_stats_dict['global_per_protocol']['PPPoX Client']['setup_avg_rate'] = pppoesetup_avg_rate/len(h_pppoe_list)
            return_stats_dict['global_per_protocol']['PPPoX Client']['teardown_avg_rate'] = pppoeteardown_avg_rate/len(h_pppoe_list)

        #DHCPv4 Protocol stats
        #Number of DHCPv4 Sessions Up
        return_stats_dict['global_per_protocol']['DHCPv4 Client']['sessions_up'] = dhcpv4_sessions_up
        #Number of DHCPv4 Session Down
        return_stats_dict['global_per_protocol']['DHCPv4 Client']['sessions_down'] = dhcpv4_sessions_down
        #Number of DHCPv4 Sessions
        return_stats_dict['global_per_protocol']['DHCPv4 Client']['sessions_total'] = dhcpv4_sessions_total
        #Number of DHCPv4 sessions not started
        return_stats_dict['global_per_protocol']['DHCPv4 Client']['sessions_not_started'] = dhcpv4_sessions_not_started
        #DHCPv4 SetUp Avg Rate
        return_stats_dict['global_per_protocol']['DHCPv4 Client']['setup_avg_rate'] = 0
        #DHCPv4 teardown Avg Rate
        return_stats_dict['global_per_protocol']['DHCPv4 Client']['teardown_avg_rate'] = 0
        if len(h_dhcpv4_list) != 0:
            return_stats_dict['global_per_protocol']['DHCPv4 Client']['setup_avg_rate'] = dhcpv4_setup_avg_rate/len(h_dhcpv4_list)
            return_stats_dict['global_per_protocol']['DHCPv4 Client']['teardown_avg_rate'] = dhcpv4_teardown_avg_rate/len(h_dhcpv4_list)

        #DHCPv6 Protocol stats
        #Number of DHCPv6 Sessions Up
        return_stats_dict['global_per_protocol']['DHCPv6 Client']['sessions_up'] = dhcpv6_sessions_up
        #Number of DHCPv6 Session Down
        return_stats_dict['global_per_protocol']['DHCPv6 Client']['sessions_down'] = dhcpv6_sessions_down
        #Number of DHCPv6 Sessions
        return_stats_dict['global_per_protocol']['DHCPv6 Client']['sessions_total'] = dhcpv6_sessions_total
        #Number of DHCPv6 sessions not started
        return_stats_dict['global_per_protocol']['DHCPv6 Client']['sessions_not_started'] = dhcpv6_sessions_not_started
        #DHCPv6 SetUp Avg Rate
        return_stats_dict['global_per_protocol']['DHCPv6 Client']['setup_avg_rate'] = 0
        #DHCPv6 teardown Avg Rate
        return_stats_dict['global_per_protocol']['DHCPv6 Client']['teardown_avg_rate'] = 0
        if len(h_dhcpv6_list) != 0:
            return_stats_dict['global_per_protocol']['DHCPv6 Client']['setup_avg_rate'] = dhcpv6_setup_avg_rate/len(h_dhcpv6_list)
            return_stats_dict['global_per_protocol']['DHCPv6 Client']['teardown_avg_rate'] = dhcpv6_teardown_avg_rate/len(h_dhcpv6_list)

    return return_stats_dict

def set_protocol_stacking_mode(rt_handle, **kwargs):
    """
    :param rt_handle:                    RT object
    :param mode:                    parallel or sequential, default is parallel
    :return:

    03/19/2018: This is a newly added API. Currently, we are implementing as a pass thru.
    This API will configure whether protocols need to be started in parallel or in seq.
    Refer topology config API in guide.
    """
    mode = kwargs.get('mode', 'parallel')
    #return rt_handle.invoke('topology_config', mode='modify', protocol_stacking_mode=mode, topology_handle=rt_handle.topology[0])
    return

def client_action_ancp(rt_handle, **kwargs):
    """
    This is an internal function to start/stop ANCP devices
    """

    h_ancp_node = kwargs['handle'] #ancpaccessnodeconfig1
    h_router = rt_handle.invoke('invoke', cmd="stc::get "+h_ancp_node+" -parent") # router1

    if kwargs['action'] == 'start':
        # Initiate the ANCP Adjacency
        rt_handle.invoke('invoke', cmd="stc::perform AncpInitiateAdjacency -BlockList {"+h_ancp_node+"}")
        rt_handle.invoke('invoke', cmd="stc::perform AncpInitiateAdjacencyWait -ObjectList {"+h_router+"} -AdjacencyBlockState ESTABLISHED -WaitTime 50")

        # Send Port UP
        rt_handle.invoke('invoke', cmd="stc::perform AncpPortUp -BlockList {"+h_ancp_node+"}")
        rt_handle.invoke('invoke', cmd="stc::perform AncpPortUpWait -ObjectList {"+h_router+"} -SubscriberBlockState ESTABLISHED -WaitTime 30")

    elif kwargs['action'] == 'stop':
        # Send Port Down
        rt_handle.invoke('invoke', cmd="stc::perform AncpPortDown -BlockList {"+h_ancp_node+"}")
        rt_handle.invoke('invoke', cmd="stc::perform AncpPortDownWait -ObjectList {"+h_router+"} -SubscriberBlockState IDLE -WaitTime 30")

        # Terminate the ANCP Adjacency
        rt_handle.invoke('invoke', cmd="stc::perform AncpTerminateAdjacency -BlockList {"+h_ancp_node+"}")
        rt_handle.invoke('invoke', cmd="stc::perform AncpTerminateAdjacencyWait -ObjectList {"+h_router+"} -AdjacencyBlockState IDLE -WaitTime 30")
    return 1

def client_action_device(rt_handle, **kwargs):
    """
    This is an internal function to control device start/stop actions.
    """
    h_device = kwargs['handle']
    if 'config' in kwargs['handle']:
        h_device = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -parent")

    if kwargs['action'] == 'start':
        rt_handle.invoke('invoke', cmd="stc::perform DeviceStartCommand  -DeviceList "+h_device)
    elif kwargs['action'] == 'stop':
        rt_handle.invoke('invoke', cmd="stc::perform DeviceStopCommand  -DeviceList "+h_device)

def client_action_host(rt_handle, **kwargs):
    """
    This is an internal function to control host start/stop actions.
    """
    params = dict(kwargs)

    #is_device_started = 0 # Currently not being used. Hence commenting it out.
    is_ppp_configured = 0

    # PPP
    if 'ppoeclientblockconfig' in rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-pppoeclientblockconfig"):
        params['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-pppoeclientblockconfig")
        pppoe_client_action(rt_handle, **params)
        #is_device_started = 1
        is_ppp_configured = 1

    # DHCPv4
    if 'dhcpv4blockconfig' in rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-dhcpv4blockconfig"):
        params['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-dhcpv4blockconfig")
        dhcp_client_action(rt_handle, **params)
        #is_device_started = 1

    # DHCPv6NA dhcpv6blockconfig
    if 'dhcpv6blockconfig' in rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-dhcpv6blockconfig"):
        params['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-dhcpv6blockconfig")
        # Check PPP for DHCPv6oPPP Scenarios
        if is_ppp_configured == 1:
            pppoe_client_action(rt_handle, **params)
            sleep(5)

        dhcp_client_action(rt_handle, **params)
        #is_device_started = 1

    # DHCPv6PD dhcpv6pdblockconfig
    if 'dhcpv6pdblockconfig' in rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-dhcpv6pdblockconfig"):
        params['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-dhcpv6pdblockconfig")
        # Check PPP for DHCPv6oPPP Scenarios
        if is_ppp_configured == 1:
            pppoe_client_action(rt_handle, **params)
            sleep(5)

        dhcp_client_action(rt_handle, **params)
        #is_device_started = 1

    # ANCP
    if 'ancpaccessnodeconfig' in rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-ancpaccessnodeconfig"):
        params['handle'] = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -children-ancpaccessnodeconfig")
        client_action_ancp(rt_handle, **params)
        #is_device_started = 1

    # If none of the protocols are started...
    #if is_device_started == 0:
    client_action_device(rt_handle, **params)

    return 1

def client_action(rt_handle, **kwargs):
    """
    :param rt_handle:                            RT object
    :param kwargs:
    handle:                                 client handle(pppox client handle/dhcp client handle)
    action:                                 start/stop/abort/restart_down
    stack:                                  dhcpv6/all
    :return:                                status dictionary
    """
    if kwargs['action'] == "restart_down":
        kwargs['action'] = "restart"

    stack = kwargs.get('stack', 'all')
    if stack == 'dhcpv6':
        h_host = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -parent")
        return dhcp_client_action(rt_handle, **kwargs)

    elif 'ppp' in kwargs['handle']:
        return pppoe_client_action(rt_handle, **kwargs)

    elif 'dhcpv' in kwargs['handle']:
        h_host = rt_handle.invoke('invoke', cmd="stc::get "+kwargs['handle']+" -parent")
        if 'ppoeclientblockconfig' in rt_handle.invoke('invoke', cmd="stc::get "+h_host+" -children-pppoeclientblockconfig"):
            pppoe_client_action(rt_handle, **kwargs)
        return dhcp_client_action(rt_handle, **kwargs)

    elif 'ancpaccessnode' in kwargs['handle']:
        return client_action_ancp(rt_handle, **kwargs)

    elif 'host' in kwargs['handle'] or 'emulateddevice' in kwargs['handle'] or 'router' in kwargs['handle']:
        return client_action_host(rt_handle, **kwargs)

    else:
        return client_action_device(rt_handle, **kwargs)
