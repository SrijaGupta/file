#
"""
This module is methods for Ixia tester, while will be used for BBE feature
"""
import ipaddress
import re


def add_string_mv(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    string_name:            string name
    :return:                dictionary
    """
    mv_args = dict()
    mv_args['pattern'] = "string"
    mv_args['string_pattern'] = kwargs['string_name']
    result = rt_handle.invoke('multivalue_config', **mv_args)
    return result


def reboot_port(rt_handle, **kwargs):
    """
    reboot port cpu
    :param rt_handle:
    :param port_list:            the tester port_list e.g. ['1/1', '1/2']
    :return:                    dictionary (status)
    """
    port_handle_list = []
    port_list = kwargs['port_list']
    if isinstance(port_list, str):
        ports = []
        ports.append(port_list)
        port_list = ports
    for port in port_list:
        port_handle = rt_handle.port_to_handle_map[port]
        port_handle_list.append(port_handle)
    result = rt_handle.invoke('reboot_port_cpu', port_list=port_handle_list)
    if result['status'] == '1':
        return rt_handle.invoke('interface_config', port_handle=port_handle_list, phy_mode='fiber')
    return result


def bbe_initialize(rt_handle):
    """
    :param rt_handle:                RT object
    :return:
    """
    rt_handle.handles = {}
    rt_handle.bgp_handle = []
    rt_handle.bbe_isis_handle = []
    rt_handle.dhcpv4_client_handle = []
    rt_handle.dhcpv6_client_handle = []
    rt_handle.ldra_handle = []
    rt_handle.pppox_client_handle = []
    rt_handle.device_group_handle = []
    rt_handle.dhcpv4_server_handle = []
    rt_handle.dhcpv6_server_handle = []
    rt_handle.ancp_handle = []
    rt_handle.ancp_line_handle = []
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
    rt_handle.ae = {}
    # rt_handle.dhcpv4_index = 0
    # rt_handle.dhcpv6_index = 0
    # rt_handle.pppoev4_index = 0
    # rt_handle.pppoev6_index = 0
    rt_handle.traffic_item = []
    rt_handle.stream_id = []
    rt_handle.igmp_handles = {}
    rt_handle.igmp_handle_to_group = {}
    rt_handle.mld_handles = {}
    rt_handle.mld_handle_to_group = {}

def add_topology(rt_handle, **kwargs):
    """
    create topoloogy for ports
    :param rt_handle:
    :param kwargs:
    port_list:                              a list of ports
    :return:                                dictionary of status and topology handle
    """
    rt_handle.topology = []

    if isinstance(kwargs['port_list'], list):
        port_list = kwargs['port_list']
    else:
        raise Exception("port_list argument should be a list")
    port_handle = []
    for port in port_list:
        if 'lag' not in port:
            port_handle.append(rt_handle.port_to_handle_map[port])
        else:
            topology_status = rt_handle.invoke('topology_config', lag_handle=port)
    if port_handle:
        topology_status = rt_handle.invoke('topology_config', port_handle=port_handle)
    for port in port_list:
        if topology_status['topology_handle'] not in rt_handle.topology:
            rt_handle.topology.append(topology_status['topology_handle'])
        rt_handle.handles[port] = {}
        rt_handle.handles[port]['topo'] = topology_status['topology_handle']
        rt_handle.handles[port]['device_group_handle'] = []
        rt_handle.handles[port]['ethernet_handle'] = []
        rt_handle.handles[port]['ipv4_handle'] = []
        rt_handle.handles[port]['ipv6_handle'] = []
        rt_handle.handles[port]['dhcpv4_client_handle'] = []
        rt_handle.handles[port]['dhcpv6_client_handle'] = []
        rt_handle.handles[port]['pppox_client_handle'] = []
        if 'lag' not in port:
            rt_handle.handles[port]['port_handle'] = rt_handle.port_to_handle_map[port]
        rt_handle.handles[port]['dhcpv6_over_pppox_handle'] = {}
    return topology_status


def set_protocol_stacking_mode(rt_handle, **kwargs):
    """
    :param rt_handle:                    RT object
    :param mode:                    parallel or sequential, default is parallel
    :return:
    """
    mode = kwargs.get('mode', 'parallel')
    return rt_handle.invoke('topology_config', mode='modify', protocol_stacking_mode=mode, topology_handle=rt_handle.topology[0])


def _set_custom_pattern(rt_handle, **kwargs):
    """
    custom pattern for create vlan/svlan
    :param rt_handle:            RT object
    :param kwargs:
    start:                  vlan start num
    step:                   vlan step num
    repeat:                 vlan repeat num
    count:                  vlan squence length
    :return:
    multivalue:             multivalue handle for the custom pattern
    """
    try:
        _result_ = rt_handle.invoke('multivalue_config', pattern="custom")

        multivalue_handle = _result_['multivalue_handle']
        mv_args = dict()
        mv_args['multivalue_handle'] = multivalue_handle
        mv_args['custom_start'] = kwargs['start']
        mv_args['custom_step'] = "0"
        _result_ = rt_handle.invoke('multivalue_config', **mv_args)
        custom_1_handle = _result_['custom_handle']
        custom_args = dict()
        custom_args['custom_handle'] = custom_1_handle
        custom_args['custom_increment_value'] = kwargs['step']
        custom_args['custom_increment_count'] = kwargs.get('count', '4094')
        _result_ = rt_handle.invoke('multivalue_config', **custom_args)

        increment_1_handle = _result_['increment_handle']
        increment_args = dict()
        increment_args['increment_handle'] = increment_1_handle
        increment_args['custom_increment_value'] = "0"
        increment_args['custom_increment_count'] = kwargs['repeat']
        _result_ = rt_handle.invoke('multivalue_config', **increment_args)
    except:
        raise Exception("failed to create custom pattern")
    #increment_2_handle = _result_['increment_handle']
    return multivalue_handle


def add_type_tlv(rt_handle, **kwargs):
    """
    create tlv type
    :param rt_handle:
    :param kwargs:
    handle:                            dhcpv6 client handle
    tlv_name:                          type name
    tlv_include_in_messages:           tlv included in which messages
    :return:                            dictionary
    """
    tlv_args = dict()
    tlv_args['handle'] = kwargs['handle']
    tlv_args['mode'] = "create_tlv"
    tlv_args['tlv_name'] = kwargs['tlv_name']
    tlv_args['tlv_is_enabled'] = "1"
    tlv_args['tlv_include_in_messages'] = kwargs['tlv_include_in_messages']
    tlv_args['tlv_enable_per_session'] = "1"
    tlv_args['type_name'] = "Type"
    tlv_args['type_is_editable'] = "0"
    tlv_args['type_is_required'] = "1"
    tlv_args['length_name'] = "Length"
    tlv_args['length_description'] = "DHCPv6 client TLV length field."
    tlv_args['length_encoding'] = "decimal"
    tlv_args['length_size'] = "2"
    tlv_args['length_value'] = "0"
    tlv_args['length_is_editable'] = "0"
    tlv_args['length_is_enabled'] = "1"
    tlv_args['disable_name_matching'] = "1"
    _result_ = rt_handle.invoke('tlv_config', **tlv_args)
    return _result_


def add_code_tlv(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    type_handle:            result from type tlv
    field_value:            field value
    :return:                dictionary
    """
    tlv_args = dict()
    tlv_args['handle'] = kwargs['type_handle']
    tlv_args['mode'] = "create_field"
    tlv_args['field_name'] = "Code"
    tlv_args['field_value'] = kwargs['field_value']
    tlv_args['field_description'] = "DHCPv6 client TLV type field."
    tlv_args['field_encoding'] = "decimal"
    tlv_args['field_size'] = "2"
    tlv_args['field_is_editable'] = "0"
    tlv_args['field_is_enabled'] = "1"
    result = rt_handle.invoke('tlv_config', **tlv_args)
    return result


def add_field_tlv(rt_handle, **kwargs):
    """
    :param rt_handle:
    value_handle:            tlv_value_handle from type tlv
    field_name:              field name
    field_value:             field value
    mode:                    optional
    :param kwargs:
    :return:                dictionary
    """
    field_param = dict()
    field_param['handle'] = kwargs['value_handle']
    field_param['field_name'] = kwargs['field_name']
    field_param['mode'] = kwargs.get('mode', 'create_field')
    field_param['field_value'] = kwargs['field_value']
    field_param['field_is_enabled'] = '1'
    field_param['field_size'] = '2'
    field_param['field_encoding'] = 'decimal'
    field_param['field_is_editable'] = '0'
    result = rt_handle.invoke('tlv_config', **field_param)
    return result

def set_v6_option(rt_handle, **kwargs):
    """
    dhcpv6 interface_id(option 17) and remote_id (option 38)
    :param rt_handle:                    RT object
    :param kwargs:
    handle:                         dhcpv6 device handle/dhcpv6 relay agent handle
    interface_id:                   interface_id string, if with ? inside it, it means the string will increase based
                                    on the start/step/repeat at that location or default
    interface_id_start:             interface_id_start num
    interface_id_step:              interface_id_step num
    interface_id_repeat:            interface_id_repeat num
    interface_id_length:            interface_id_length
    remote_id:                      remote_id string, if with ? inside it, it means the string will increase based on
                                    the start/step/repeat or default
    remote_id_start:                remote_id_start num
    remote_id_step:                 remote_id_step num
    remote_id_repeat:               remote_id_repeat num
    remote_id_length:               remote_id_length
    enterprise_id:                  enterprise_id used inside of remote id
    enterprise_id_step:             enterprise_id_step num
    subscriber_id:                  subscriber_id string, if with ? inside it, it means the string will increase based
                                    on the start/step/repeat at that location or default
    subscriber_id_start:            subscriber_id_start num
    subscriber_id_step:             subscriber_id_step num
    subscriber_id_repeat:           subscriber_id_repeat num
    subsriber_id_length:            subscriber_id_length
    option_req:                     a list of field of option_request, e.g.[6, 67]
    tlv_include_in_messages:        the tlv included in which messages, e.g. "kSolicit kRequest"
    :return:
    result:                         dictionary of status
    """
    if 'handle' in kwargs and 'relayAgent' in kwargs['handle']:
        dhcpv6_handle = kwargs['handle']
        if 'interface_id' in kwargs:
            interface_id = kwargs.get('interface_id')
            if 'interface_id_start' in kwargs:
                start = str(kwargs.get('interface_id_start'))
                step = str(kwargs.get('interface_id_step', '1'))
                repeat = str(kwargs.get('interface_id_repeat', '1'))
                length = str(kwargs.get('interface_id_length', '1'))

                if '?' in interface_id:
                    increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                    interface_id = interface_id.replace('?', increment)
                else:
                    interface_id = interface_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
            tlv_args = dict()
            tlv_args['handle'] = dhcpv6_handle + "/lightweightDhcp6RelayTlvProfile/tlvProfile/defaultTlv:1"
            tlv_args['mode'] = 'modify'
            tlv_args['tlv_name'] = "[18] Interface-ID"
            tlv_args['tlv_include_in_messages'] = "kRelayForw"
            tlv_args['tlv_enable_per_session'] = '1'
            tlv_args['disable_name_matching'] = '1'
            _result_ = rt_handle.invoke('tlv_config', **tlv_args)
            print(_result_)
            _result_ = add_string_mv(rt_handle, string_name=interface_id)
            print(_result_)
            multivalue_2_handle = _result_['multivalue_handle']
            tlv2_args = dict()
            tlv_field = "/lightweightDhcp6RelayTlvProfile/tlvProfile/defaultTlv:1/value/object:1/field"
            tlv2_args['handle'] = dhcpv6_handle + tlv_field
            tlv2_args['mode'] = 'modify'
            tlv2_args['field_name'] = "Interface-ID"
            tlv2_args['field_encoding'] = 'string'
            tlv2_args['field_size'] = "0"
            tlv2_args['field_value'] = multivalue_2_handle
            tlv2_args['field_is_enabled'] = "1"
            tlv2_args['field_is_editable'] = "1"
            result = rt_handle.invoke('tlv_config', **tlv2_args)
            print(result)
        if 'v6_remote_id' in kwargs:
            remote_id = kwargs['v6_remote_id']
            if 'v6_remote_id_start' in kwargs:
                start = str(kwargs.get('v6_remote_id_start'))
                step = str(kwargs.get('v6_remote_id_step', '1'))
                repeat = str(kwargs.get('v6_remote_id_repeat', '1'))
                length = str(kwargs.get('v6_remote_id_length', '1'))
                if '?' in remote_id:
                    increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                    remote_id = remote_id.replace('?', increment)
                else:
                    remote_id = remote_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
            tlv_args = dict()
            tlv_args['handle'] = dhcpv6_handle + "/lightweightDhcp6RelayTlvProfile/tlvProfile/defaultTlv:2"
            tlv_args['mode'] = 'modify'
            tlv_args['tlv_name'] = "[37] Relay Agent Remote-ID"
            tlv_args['tlv_include_in_messages'] = "kRelayForw"
            tlv_args['tlv_enable_per_session'] = '1'
            tlv_args['disable_name_matching'] = '1'
            tlv_args['tlv_is_enabled'] = "1"
            _result_ = rt_handle.invoke('tlv_config', **tlv_args)

            _result_ = add_string_mv(rt_handle, string_name=remote_id)
            print(_result_)
            multivalue_3_handle = _result_['multivalue_handle']
            tlv2_args = dict()
            tlv2_field = "/lightweightDhcp6RelayTlvProfile/tlvProfile/defaultTlv:2/value/object:2/field"
            tlv2_args['handle'] = dhcpv6_handle + tlv2_field
            tlv2_args['mode'] = 'modify'
            tlv2_args['field_name'] = "Remote-ID String"
            tlv2_args['field_encoding'] = 'string'
            tlv2_args['field_size'] = "0"
            tlv2_args['field_value'] = multivalue_3_handle
            tlv2_args['field_is_enabled'] = "1"
            tlv2_args['field_is_editable'] = "1"
            result = rt_handle.invoke('tlv_config', **tlv2_args)
            print(result)
            if 'enterprise_id' in kwargs:
                mv_args = dict()
                mv_args['pattern'] = "counter"
                mv_args['counter_start'] = kwargs['enterprise_id']
                mv_args['counter_step'] = kwargs.get('enterprise_id_step', 0)
                mv_args['counter_direction'] = "increment"
                _result_ = rt_handle.invoke('multivalue_config', **mv_args)
                print(_result_)
                subtlv_obj = "/lightweightDhcp6RelayTlvProfile/tlvProfile/defaultTlv:2/value/object:1/field"
                field_args = dict()
                field_args['handle'] = dhcpv6_handle + subtlv_obj
                field_args['mode'] = "modify"
                field_args['field_name'] = "Enterprise number"
                field_args['field_encoding'] = "decimal"
                field_args['field_size'] = "4"
                field_args['field_value'] = _result_['multivalue_handle']
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "1"
                result = rt_handle.invoke('tlv_config', **field_args)
                print(result)
        if 'subscriber_id' in kwargs:
            subscriber_id = kwargs.get('subscriber_id')
            if 'subscriber_id_start' in kwargs:
                start = str(kwargs.get('subscriber_id_start'))
                step = str(kwargs.get('subscriber_id_step', '1'))
                repeat = str(kwargs.get('subscriber_id_repeat', '1'))
                length = str(kwargs.get('subscriber_id_length', ''))

                if '?' in subscriber_id:
                    increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                    subscriber_id = subscriber_id.replace('?', increment)
                else:
                    subscriber_id = subscriber_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
            handle = dhcpv6_handle + "/lightweightDhcp6RelayTlvProfile/tlvProfile/defaultTlv:3"
            subtlv_args = dict()
            subtlv_args['handle'] = handle
            subtlv_args['mode'] = "modify"
            subtlv_args['tlv_name'] = "[38] Relay Agent Subscriber-ID"
            subtlv_args['tlv_is_enabled'] = "1"
            subtlv_args['tlv_include_in_messages'] = "kRelayForw"
            subtlv_args['tlv_enable_per_session'] = "1"
            subtlv_args['disable_name_matching'] = "1"
            _result_ = rt_handle.invoke('tlv_config', **subtlv_args)
            print(_result_)
            _result_ = add_string_mv(rt_handle, string_name=subscriber_id)
            print(_result_)
            field_handle = "/lightweightDhcp6RelayTlvProfile/tlvProfile/defaultTlv:3/value/object:1/field"
            field_args = dict()
            field_args['handle'] = dhcpv6_handle + field_handle
            field_args['mode'] = "modify"
            field_args['field_name'] = "Subscriber-ID"
            field_args['field_description'] = "Relay agent subscriber ID."
            field_args['field_encoding'] = "string"
            field_args['field_size'] = "0"
            field_args['field_value'] = _result_['multivalue_handle']
            field_args['field_is_enabled'] = "1"
            field_args['field_is_editable'] = "1"
            result = rt_handle.invoke('tlv_config', **field_args)
            print(result)

    if 'handle' in kwargs and 'relayAgent' not in kwargs['handle']:
        v6option_args = dict()
        v6option_args['handle'] = kwargs['handle']
        tlv_in_message = kwargs.get('tlv_include_in_messages',
                                    "kSolicit kRequest kInformReq kRelease kRenew kRebind")
        v6option_args['tlv_include_in_messages'] = tlv_in_message

        if 'option_req' in kwargs:
            v6option_args['tlv_name'] = "[06] Option Request"
            _result_ = add_type_tlv(rt_handle, **v6option_args)
            if _result_['status'] == '0':
                return _result_
            field_list = []
            if isinstance(kwargs['option_req'], list):
                field_list = kwargs['option_req']
            else:
                field_list.append(kwargs['option_req'])
            for field in field_list:
                v6option_args['field_name'] = "[{}]".format(field)
                v6option_args['value_handle'] = _result_['tlv_value_handle']
                v6option_args['field_value'] = field
                result = add_field_tlv(rt_handle, **v6option_args)
                if result['status'] == '0':
                    return result
            v6option_args['field_value'] = '6'
            v6option_args['type_handle'] = _result_['tlv_type_handle']
            result = add_code_tlv(rt_handle, **v6option_args)

        if 'option20' in kwargs:
            v6option_args['tlv_name'] = "[20] Reconfigure Accept"
            _result_ = add_type_tlv(rt_handle, **v6option_args)
            if _result_['status'] != '1':
                return _result_
            v6option_args['field_value'] = '20'
            v6option_args['type_handle'] = _result_['tlv_type_handle']
            v6option_args['field_value'] = '20'
            result = add_code_tlv(rt_handle, **v6option_args)
    return result


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
    circuit_id_length:          circuit_id_length
    remote_id:                  remote id string
    remote_id_start:            remote id start num
    remote_id_step:             remote_id_step num
    remote_id_repeat:           remote_id_repeat num
    remote_id_length:           remote_id_length
    tlv_include_in_messages:    tlv include in certain messages
    :return:
    status:                     1 or 0
    """
    if 'handle' in kwargs and 'v4' in kwargs.get('handle'):
        handle = kwargs.get('handle')
        if 'circuit_id' in kwargs:
            circuit_id = kwargs.get('circuit_id')
            if 'circuit_id_start' in kwargs:
                start = str(kwargs.get('circuit_id_start'))
                step = str(kwargs.get('circuit_id_step', '1'))
                repeat = str(kwargs.get('circuit_id_repeat', '1'))
                length = str(kwargs.get('circuit_id_length', '1'))
                if '?' in circuit_id:
                    increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                    circuit_id = circuit_id.replace('?', increment)
                else:
                    circuit_id = circuit_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'

        if 'remote_id' in kwargs:
            remote_id = kwargs.get('remote_id')
            if 'remote_id_start' in kwargs:
                start = str(kwargs.get('remote_id_start'))
                step = str(kwargs.get('remote_id_step', '1'))
                repeat = str(kwargs.get('remote_id_repeat', '1'))
                length = str(kwargs.get('remote_id_length', '1'))
                if '?' in remote_id:
                    increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                    remote_id = remote_id.replace('?', increment)
                else:
                    remote_id = remote_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
        if handle not in rt_handle.circuit_id and handle not in rt_handle.remote_id:
            ##create option82 TLV
            if 'circuit_id' in kwargs or 'remote_id' in kwargs:
                tlv_args = dict()
                tlv_args['handle'] = kwargs['handle']
                tlv_args['mode'] = "create_tlv"
                tlv_args['tlv_name'] = "[82] DHCP Relay Agent Information"
                tlv_args['tlv_is_enabled'] = "1"
                tlv_args['tlv_include_in_messages'] = kwargs.get('tlv_include_in_messages', "kDiscover kRequest")
                tlv_args['tlv_enable_per_session'] = "1"
                tlv_args['type_name'] = "Type"
                tlv_args['type_is_editable'] = "0"
                tlv_args['type_is_required'] = "1"
                tlv_args['length_name'] = "Length"
                tlv_args['length_encoding'] = "decimal"
                tlv_args['length_size'] = "1"
                tlv_args['length_value'] = "0"
                tlv_args['length_is_editable'] = "0"
                tlv_args['length_is_enabled'] = "1"
                tlv_args['disable_name_matching'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **tlv_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option82 tlv")
                # tlv_1_handle = _result_['tlv_handle']
                value_1_handle = _result_['tlv_value_handle']
                # length_1_handle = _result_['tlv_length_handle']
                field_args = dict()
                field_args['handle'] = _result_['tlv_type_handle']
                field_args['mode'] = "create_field"
                field_args['field_name'] = "Code"
                field_args['field_description'] = "Dhcp client TLV type field."
                field_args['field_encoding'] = "decimal"
                field_args['field_size'] = "1"
                field_args['field_value'] = "82"
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option82 tlv type field")

            if 'circuit_id' in kwargs:
                type_args = dict()
                type_args['handle'] = value_1_handle
                type_args['mode'] = "create_tlv"
                type_args['tlv_name'] = "[1] Agent Circuit ID"
                type_args['tlv_is_enabled'] = "1"
                type_args['tlv_enable_per_session'] = "1"
                type_args['type_name'] = "Type"
                type_args['type_is_editable'] = "0"
                type_args['type_is_required'] = "1"
                type_args['length_name'] = "Length"
                type_args['length_encoding'] = "decimal"
                type_args['length_size'] = "1"
                type_args['length_value'] = "0"
                type_args['length_is_editable'] = "0"
                type_args['length_is_enabled'] = "1"
                type_args['disable_name_matching'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **type_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option82 circuitid tlv")
                #subTlv_1_handle = _result_['subtlv_handle']
                value_2_handle = _result_['tlv_value_handle']
                #length_2_handle = _result_['tlv_length_handle']
                type_2_handle = _result_['tlv_type_handle']
                _result_ = add_string_mv(rt_handle, string_name=circuit_id)
                multivalue_4_handle = _result_['multivalue_handle']
                field_args = dict()
                field_args['handle'] = value_2_handle
                field_args['mode'] = "create_field"
                field_args['field_name'] = "Circuit ID"
                field_args['field_encoding'] = "string"
                field_args['field_size'] = "0"
                field_args['field_value'] = multivalue_4_handle
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option82 circuitid field")
                rt_handle.circuit_id[handle] = _result_['tlv_field_handle']
                field_args = dict()
                field_args['handle'] = type_2_handle
                field_args['mode'] = "create_field"
                field_args['field_name'] = "Code"
                field_args['field_encoding'] = "decimal"
                field_args['field_description'] = "Dhcp client TLV type field."
                field_args['field_size'] = "1"
                field_args['field_value'] = "1"
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "0"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option82 tlv circuitid type field")

            if 'remote_id' in kwargs:
                type_args = dict()
                type_args['handle'] = value_1_handle
                type_args['mode'] = "create_tlv"
                type_args['tlv_name'] = "[2] Agent Remote ID"
                type_args['tlv_is_enabled'] = "1"
                type_args['tlv_enable_per_session'] = "1"
                type_args['type_name'] = "Type"
                type_args['type_is_editable'] = "0"
                type_args['type_is_required'] = "1"
                type_args['length_name'] = "Length"
                type_args['length_encoding'] = "decimal"
                type_args['length_size'] = "1"
                type_args['length_value'] = "0"
                type_args['length_is_editable'] = "0"
                type_args['length_is_enabled'] = "1"
                type_args['disable_name_matching'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **type_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option82 remoteid tlv")
                #subTlv_2_handle = _result_['subtlv_handle']
                value_3_handle = _result_['tlv_value_handle']
                #length_3_handle = _result_['tlv_length_handle']
                type_3_handle = _result_['tlv_type_handle']
                _result_ = add_string_mv(rt_handle, string_name=remote_id)
                multivalue_5_handle = _result_['multivalue_handle']
                field_args = dict()
                field_args['handle'] = value_3_handle
                field_args['mode'] = "create_field"
                field_args['field_name'] = "Remote ID"
                field_args['field_encoding'] = "string"
                field_args['field_size'] = "0"
                field_args['field_value'] = multivalue_5_handle
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option82 remote id field")
                rt_handle.remote_id[handle] = _result_['tlv_field_handle']
                field_args = dict()
                field_args['handle'] = type_3_handle
                field_args['mode'] = "create_field"
                field_args['field_name'] = "Code"
                field_args['field_encoding'] = "decimal"
                field_args['field_description'] = "Dhcp client TLV type field."
                field_args['field_size'] = "1"
                field_args['field_value'] = "2"
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "0"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option82 remote id type field")
            return _result_
        if handle in rt_handle.circuit_id and 'circuit_id' in kwargs:
            field_args = dict()
            field_args['handle'] = rt_handle.circuit_id[handle]
            field_args['mode'] = "modify"
            field_args['field_name'] = "Circuit ID"
            field_args['field_encoding'] = "string"
            field_args['field_size'] = "0"
            field_args['field_value'] = circuit_id
            field_args['field_is_enabled'] = "1"
            field_args['field_is_editable'] = "1"
            _result_ = rt_handle.invoke('tlv_config', **field_args)
            if _result_['status'] != '1':
                raise Exception("failed to modify option82 circuitid")
        if handle in rt_handle.remote_id and 'remote_id' in kwargs:
            field_args = dict()
            field_args['handle'] = rt_handle.remote_id[handle]
            field_args['mode'] = "modify"
            field_args['field_name'] = "Remote ID"
            field_args['field_encoding'] = "string"
            field_args['field_size'] = "0"
            field_args['field_value'] = circuit_id
            field_args['field_is_enabled'] = "1"
            field_args['field_is_editable'] = "1"
            _result_ = rt_handle.invoke('tlv_config', **field_args)
            print(_result_)
            if _result_['status'] != '1':
                raise Exception("failed to modify option82 remote id ")
        return _result_

def set_option_60(rt_handle, **kwargs):
    """
    this is for dhcpv4 option 60
    :param rt_handle:                RT object
    :param kwargs:
    handle:                     dhcpv4 client handle
    vendor_class_id:            Vendor Class id string( if with ? with the Vendor Class id, it will replace ? with the increase)
    vendor_class_id_start:      circuit id start num
    vendor_class_id_step:       circuit id step num
    vendor_class_id_repeat:     circuit_id_repeat_num
    vendor_class_id_length:     circuit_id_length
    tlv_include_in_messages:    tlv include in certain messages
    :return:
    status:                     1 or 0
    """
    if 'handle' in kwargs and 'v4' in kwargs.get('handle'):
        handle = kwargs.get('handle')
        if 'vendor_class_id' in kwargs:
            vendor_class_id = kwargs.get('vendor_class_id')
            if 'vendor_class_id_start' in kwargs:
                start = str(kwargs.get('vendor_class_id_start'))
                step = str(kwargs.get('vendor_class_id_step', '1'))
                repeat = str(kwargs.get('vendor_class_id_repeat', '1'))
                length = str(kwargs.get('vendor_class_id_length', '1'))
                if '?' in vendor_class_id:
                    increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                    vendor_class_id = vendor_class_id.replace('?', increment)
                else:
                    vendor_class_id = vendor_class_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'

            ##create option60 TLV
            if 'vendor_class_id' in kwargs:
                tlv_args = dict()
                tlv_args['handle'] = kwargs['handle']
                tlv_args['mode'] = "create_tlv"
                tlv_args['tlv_name'] = "[60] Vendor Class Identifier"
                tlv_args['tlv_is_enabled'] = "1"
                tlv_args['tlv_include_in_messages'] = kwargs.get('tlv_include_in_messages', "kDiscover kRequest")
                tlv_args['tlv_enable_per_session'] = "1"
                tlv_args['type_name'] = "Type"
                tlv_args['type_is_editable'] = "0"
                tlv_args['type_is_required'] = "1"
                tlv_args['length_name'] = "Length"
                tlv_args['length_encoding'] = "decimal"
                tlv_args['length_size'] = "1"
                tlv_args['length_value'] = "0"
                tlv_args['length_is_editable'] = "0"
                tlv_args['length_is_enabled'] = "1"
                tlv_args['disable_name_matching'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **tlv_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option60 tlv")
                tlv_1_handle = _result_['tlv_handle']
                value_1_handle = _result_['tlv_value_handle']
                length_1_handle = _result_['tlv_length_handle']
                type_1_handle = _result_['tlv_type_handle']
                _result_ = add_string_mv(rt_handle, string_name=vendor_class_id)
                multivalue_1_handle = _result_['multivalue_handle']

                field_args = dict()
                field_args['handle'] = value_1_handle
                field_args['mode'] = "create_field"
                field_args['field_name'] = "Class Identifier"
                field_args['field_description'] = "The information is a string of n octets, interpreted by servers."
                field_args['field_encoding'] = "string"
                field_args['field_size'] = "0"
                field_args['field_value'] = multivalue_1_handle
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option60 tlv value field")

                type_args = dict()
                type_args['handle'] = type_1_handle
                field_args['mode'] = "create_field"
                field_args['field_name'] = "Code"
                field_args['field_encoding'] = "decimal"
                field_args['field_description'] = "Dhcp client TLV type field."
                field_args['field_size'] = "1"
                field_args['field_value'] = "60"
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "0"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option60 tlv vendor-class-id type field")
    return _result_

def set_option_72(rt_handle, **kwargs):
    """
    this is for dhcpv4 option 72
    :param rt_handle:                RT object
    :param kwargs:
    handle:                     dhcpv4 client handle
    www_server:                 Default WWW Server (The WWW server option specifies a list of WWW available to the client. Servers should be listed in order of preference)
    tlv_include_in_messages:    tlv include in certain messages
    :return:
    status:                     1 or 0
    """
    if 'handle' in kwargs and 'v4' in kwargs.get('handle'):
        handle = kwargs.get('handle')
        if 'www_server' in kwargs:
            www_server = kwargs.get('www_server')
            server_list = list(www_server.split(" "))

            ##create option72 TLV
            if 'www_server' in kwargs:
                tlv_args = dict()
                tlv_args['handle'] = kwargs['handle']
                tlv_args['mode'] = "create_tlv"
                tlv_args['tlv_name'] = "[72] Default World Wide Web (WWW) Server"
                tlv_args['tlv_is_enabled'] = "1"
                tlv_args['tlv_include_in_messages'] = kwargs.get('tlv_include_in_messages', "kDiscover kRequest")
                tlv_args['tlv_enable_per_session'] = "1"
                tlv_args['type_name'] = "Type"
                tlv_args['type_is_editable'] = "0"
                tlv_args['type_is_required'] = "1"
                tlv_args['length_name'] = "Length"
                tlv_args['length_encoding'] = "decimal"
                tlv_args['length_size'] = "1"
                tlv_args['length_value'] = "0"
                tlv_args['length_is_editable'] = "0"
                tlv_args['length_is_enabled'] = "1"
                tlv_args['disable_name_matching'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **tlv_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option72 tlv")
                tlv_1_handle = _result_['tlv_handle']
                value_1_handle = _result_['tlv_value_handle']
                length_1_handle = _result_['tlv_length_handle']
                type_1_handle = _result_['tlv_type_handle']

                field_args = dict()
                field_args['handle'] = value_1_handle
                field_args['mode'] = "create_tlv_container"
                field_args['container_name'] = "Server Address(IPv4) List"
                field_args['container_is_enabled'] = "1"
                field_args['container_is_repeatable'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option72 container field")

                repeatableContainer_1_handle = _result_['tlv_container_handle']

                for each_server in server_list:
                    field_args = dict()
                    field_args['handle'] = repeatableContainer_1_handle
                    field_args['mode'] = "create_field"
                    field_args['field_name'] = "Server Address (IPv4)"
                    field_args['field_description'] = "Default World Wide Web server IP address."
                    field_args['field_encoding'] = "ipv4"
                    field_args['field_size'] = "4"
                    field_args['field_value'] = each_server
                    field_args['field_is_enabled'] = "1"
                    field_args['field_is_editable'] = "1"
                    _result_ = rt_handle.invoke('tlv_config', **field_args)
                    if _result_['status'] != '1':
                        raise Exception("failed to create option72 value field")

                type_args = dict()
                type_args['handle'] = type_1_handle
                field_args['mode'] = "create_field"
                field_args['field_name'] = "Code"
                field_args['field_encoding'] = "decimal"
                field_args['field_description'] = "Dhcp client TLV type field."
                field_args['field_size'] = "1"
                field_args['field_value'] = "72"
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "0"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option72 type field")
    return _result_


def set_option_23(rt_handle, **kwargs):
    """
    this is for dhcpv6 option 23
    :param rt_handle:                RT object
    :param kwargs:
    handle:                     dhcpv6 client handle
    dns_server:                 Default DNS Server (The DNS Recursive Name Server option provides a list of one or more IPv6 addresses of DNS recursive name servers to which a client's DNS resolver MAY send DNS queries. The DNS servers are listed in the order of preference for use by the client resolver.)
    tlv_include_in_messages:    tlv include in certain messages
    :return:
    status:                     1 or 0
    """
    if 'handle' in kwargs:
        handle = kwargs.get('handle')
        if 'dns_server' in kwargs:
            dns_server = kwargs.get('dns_server')
            server_list = list(dns_server.split(" "))
            tlv_args = dict()
            tlv_args['handle'] = kwargs['handle']
            tlv_args['mode'] = "create_tlv"
            tlv_args['tlv_name'] = "[23] DNS Recursive Name Server"
            tlv_args['tlv_is_enabled'] = "1"
            tlv_args['tlv_include_in_messages'] = kwargs.get('tlv_include_in_messages', "kSolicit kRequest kInformReq kRelease kRenew kRebind")
            tlv_args['tlv_enable_per_session'] = "1"
            tlv_args['type_name'] = "Type"
            tlv_args['type_is_editable'] = "0"
            tlv_args['type_is_required'] = "1"
            tlv_args['length_name'] = "Length"
            tlv_args['length_encoding'] = "decimal"
            tlv_args['length_size'] = "2"
            tlv_args['length_value'] = "0"
            tlv_args['length_is_editable'] = "0"
            tlv_args['length_is_enabled'] = "1"
            tlv_args['disable_name_matching'] = "1"
            _result_ = rt_handle.invoke('tlv_config', **tlv_args)
            if _result_['status'] != '1':
                raise Exception("failed to create option23 tlv")
            tlv_1_handle = _result_['tlv_handle']
            value_1_handle = _result_['tlv_value_handle']
            length_1_handle = _result_['tlv_length_handle']
            type_1_handle = _result_['tlv_type_handle']

            field_args = dict()
            field_args['handle'] = value_1_handle
            field_args['mode'] = "create_tlv_container"
            field_args['container_name'] = "Server Address(IPv6) List"
            field_args['container_is_enabled'] = "1"
            field_args['container_is_repeatable'] = "1"
            _result_ = rt_handle.invoke('tlv_config', **field_args)
            if _result_['status'] != '1':
                raise Exception("failed to create option23 container field")

            repeatableContainer_1_handle = _result_['tlv_container_handle']

            for each_server in server_list:
                field_args = dict()
                field_args['handle'] = repeatableContainer_1_handle
                field_args['mode'] = "create_field"
                field_args['field_name'] = "Server Address (IPv6)"
                field_args['field_description'] = "IPv6 address of DNS recursive name server."
                field_args['field_encoding'] = "ipv6"
                field_args['field_size'] = "16"
                field_args['field_value'] = each_server
                field_args['field_is_enabled'] = "1"
                field_args['field_is_editable'] = "1"
                _result_ = rt_handle.invoke('tlv_config', **field_args)
                if _result_['status'] != '1':
                    raise Exception("failed to create option23 value field")

            type_args = dict()
            type_args['handle'] = type_1_handle
            field_args['mode'] = "create_field"
            field_args['field_name'] = "Code"
            field_args['field_encoding'] = "decimal"
            field_args['field_description'] = "Dhcpv6 client TLV type field."
            field_args['field_size'] = "2"
            field_args['field_value'] = "23"
            field_args['field_is_enabled'] = "1"
            field_args['field_is_editable'] = "0"
            _result_ = rt_handle.invoke('tlv_config', **field_args)
            if _result_['status'] != '1':
                raise Exception("failed to create option23 type field")
    return _result_

def set_vlan(rt_handle, **kwargs):
    """
    rt.invoke('set_vlan', handle=interf.rt_ethernet_handle, vlan_start='1', vlan_priority='3')
    :param rt_handle:                RT object
    :param kwargs:
    handle                      device group handle
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    vlan_tpid:                  vlan tpid value, 0x9100, 0x8100, 0x88a8, 0x88A8, 0x9200, 0x9300
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    svlan_length:               svlan sequence length
    svlan_tpid:                 svlan tpid value, 0x9100, 0x8100, 0x88a8, 0x88A8, 0x9200, 0x9300
    vlan_priority:              vlan priority value
    vlan_priority_step:         vlan priority step value
    mac:                        MAC address
    mac_step:                   MAC address step
    mtu:                        MTU value
    :return:
    result
    """
    if 'handle' not in kwargs:
        raise Exception("handle is mandatory")
    vlan_args = dict()
    if 'svlan_start' in kwargs:
        vlan_args['start'] = kwargs.get('svlan_start')
        vlan_args['step'] = kwargs.get('svlan_step', '1')
        vlan_args['repeat'] = kwargs.get('svlan_repeat', '1')
        vlan_args['count'] = kwargs.get('svlan_length', '4094')
        svlan_handle = _set_custom_pattern(rt_handle, **vlan_args)
    if 'vlan_start' in kwargs:
        vlan_args['start'] = kwargs.get('vlan_start')
        vlan_args['step'] = kwargs.get('vlan_step', '1')
        vlan_args['repeat'] = kwargs.get('vlan_repeat', '1')
        vlan_args['count'] = kwargs.get('vlan_length', '4094')
        vlan_handle = _set_custom_pattern(rt_handle, **vlan_args)

    intf_args = dict()
    intf_args['protocol_handle'] = kwargs.get('handle')
    #intf_args['return_detailed_handles'] = '0'
    ###mtu must be set, otherwise, the API call will have problem
    intf_args['mtu'] = kwargs.get('mtu', '1500')
    if 'mac' in kwargs:
        intf_args['src_mac_addr'] = kwargs.get('mac')
        intf_args['src_mac_addr_step'] = "00:00:00:00:00:01"
    if 'mac_step' in kwargs:
        intf_args['src_mac_addr_step'] = kwargs['mac_step']
    if 'vlan_start' in kwargs:
        intf_args['vlan'] = '1'
        intf_args['vlan_id_count'] = '1'
        intf_args['vlan_id'] = vlan_handle
        vlan_tpid = kwargs.get('vlan_tpid', '0x8100')
        if 'vlan_tpid' in kwargs:
            intf_args['vlan_tpid'] = vlan_tpid
    if 'svlan_start' in kwargs:
        intf_args['vlan_id_count'] = '2'
        intf_args['vlan_id'] = "{},{}".format(svlan_handle, vlan_handle)
        svlan_tpid = kwargs.get('svlan_tpid', '0x8100')
        if 'svlan_tpid' in kwargs or 'vlan_tpid' in kwargs:
            intf_args['vlan_tpid'] = "{},{}".format(svlan_tpid, vlan_tpid)
    if 'ethernet' in kwargs['handle']:
        intf_args['mode'] = 'modify'
    if 'vlan_priority' in kwargs:
        intf_args['vlan_user_priority'] = kwargs['vlan_priority']
    if 'vlan_priority_step' in kwargs:
        intf_args['vlan_user_priority_step'] = kwargs['vlan_priority_step']
    if 'svlan_priority' in kwargs:
        intf_args['vlan_user_priority'] = '{},{}'.format(kwargs['svlan_priority'], kwargs['vlan_priority'])
    if 'svlan_priority_step' in kwargs:
        intf_args['vlan_user_priority_step'] = \
            '{},{}'.format(kwargs['svlan_priority_step'], kwargs['svlan_priority_step'])
    _result_ = rt_handle.invoke('interface_config', **intf_args)
    #print(_result_)
    return _result_


def add_device_group(rt_handle, **kwargs):
    """
    :param rt_handle:            RT object
    :param kwargs:
    port_handle:            provide a port handle
    topology_handle:        provide a topology handle
    device_handle:          provide a device handle
    device_count:           provide device group multiplier
    name:                   device group name

    :return: a dictionary of status and device handle
    status                  1 or 0
    device_handle
    """
    device_args = dict()
    port_list = []
    if 'port_handle' in kwargs:
        port_handle = kwargs.get('port_handle')
        print(port_handle)
        port = rt_handle.handle_to_port_map[port_handle]
        port_list.append(port)
        if port not in rt_handle.handles:
            _result_ = add_topology(rt_handle, port_list=[port])
        topo_handle = rt_handle.handles[port]['topo']
        device_args['topology_handle'] = topo_handle
    elif 'topology_handle' in kwargs:
        device_args['topology_handle'] = kwargs['topology_handle']
        for key in rt_handle.handles.keys():
            if rt_handle.handles[key]['topo'] == kwargs['topology_handle']:
                port_list.append(key)
    elif 'device_group_handle' in kwargs:
        device_args['device_group_handle'] = kwargs['device_group_handle']
        for key in rt_handle.handles.keys():
            if kwargs['device_group_handle'] in rt_handle.handles[key]['device_group_handle']:
                port = key
                port_list.append(key)
    device_args['device_group_multiplier'] = kwargs.get('device_count', '1')
    result = dict()
    result['status'] = '1'
    if 'name' in kwargs:
        device_args['device_group_name'] = kwargs['name']
    status = rt_handle.invoke('topology_config', **device_args)
    if status['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to create device group ")
    else:
        device_handle = status['device_group_handle']
        rt_handle.device_group_handle.append(device_handle)
        for port in port_list:
            rt_handle.handles[port]['device_group_handle'].append(device_handle)
        result['device_group_handle'] = device_handle
    return result


def add_ldra(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    port:
    handle:
    :return:
    """
    result = dict()
    result['status'] = '1'
    if 'port' in kwargs:
        port = kwargs.get('port')
        if port not in rt_handle.handles:
            _result_ = add_topology(rt_handle, port_list=[port])
            topo_handle = _result_['topology_handle']
        else:
            topo_handle = rt_handle.handles[port]['topo']
        port_handle = rt_handle.port_to_handle_map[port]
        ##create devicegroup

        dev_args = dict()
        dev_args['device_count'] = '1'
        if rt_handle.ae and port in rt_handle.ae:
            device_handle = rt_handle.handles[port]['device_group_handle'][0]
            dev_args['device_group_handle'] = device_handle
        else:
            dev_args['topology_handle'] = topo_handle
        _result_ = add_device_group(rt_handle, **dev_args)
        if _result_['status'] != '1':
            raise Exception("failed to add device group for ldra")
        device_handle = _result_['device_group_handle']
        result['device_group_handle'] = device_handle
        _result_ = set_vlan(rt_handle, handle=device_handle)
        if _result_['status'] != '1':
            raise Exception("failed to add ethernet for ldra")
        ethernet_handle = _result_['ethernet_handle']
        result['ethernet_handle'] = ethernet_handle
        dhcp_args = dict()
        dhcp_args['mode'] = "create_relay_agent"
        dhcp_args['handle'] = ethernet_handle
        dhcp_args['protocol_name'] = "Lightweight DHCPv6 Relay Agent 1"
        dhcp_args['dhcp_range_relay_type'] = "lightweight"
        _result_ = rt_handle.invoke('emulation_dhcp_group_config', **dhcp_args)
        if _result_['status'] != '1':
            raise Exception("failed to add lightweight dhcpv6relayagent for ldra")
        ldra_handle = _result_['dhcpv6relayagent_handle']
        result['ldra_handle'] = ldra_handle
        rt_handle.ldra_handle.append(ldra_handle)
        return result

def add_dhcp_client(rt_handle, **kwargs):
    """
    :param rt_handle:                RT object
    :param kwargs:
    mandatory:
    port:                       Tester physical port
    num_sessions:               client counts

    optional:
    ip_type:                    ipv4, ipv4, dual
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
    option_req:                 v6 option request
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
    gre_vlan_id:                softgre vlan id (optional)
    gre_vlan_id_step:           softgre vlan id step(optional)
    gre_vlan_id_repeat:         softgre vlan id repeat(optional)
    gre_tunnel_count:             softgre tunnel number, by default is 1
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
    dhcp_args = dict()
    ldra = 0
    if 'ip_type' in kwargs:
        if kwargs['ip_type'] == 'dual' or kwargs['ip_type'] == 'ipv6':
            if 'interface_id' in kwargs or 'v6_remote_id' in kwargs:
                ldra = 1
    if 'port' in kwargs:
        port = kwargs.get('port')
        if port not in rt_handle.handles:
            _result_ = add_topology(rt_handle, port_list=[port])
            topo_handle = _result_['topology_handle']
        else:
            topo_handle = rt_handle.handles[port]['topo']
       # port_handle = rt_handle.port_to_handle_map[port]
        ##create devicegroup

        if 'softgre' in kwargs:
            gre_args = dict()
            gre_args['port'] = port
            gre_args['ip_addr'] = kwargs['gre_local_ip']
            gre_args['gateway'] = kwargs['gre_gateway']
            gre_args['gre_dst_ip'] = kwargs['gre_dst_ip']
            if 'gre_vlan_id' in kwargs:
                gre_args['vlan_start'] = kwargs['gre_vlan_id']
                gre_args['vlan_step'] = kwargs.get('gre_vlan_id_step', '1')
                gre_args['vlan_repeat'] = kwargs.get('gre_vlan_id_repeat', "1")
            if 'gre_netmask' in kwargs:
                gre_args['netmask'] = kwargs['gre_netmask']
            if 'gre_tunnel_count' in kwargs:
                gre_args['count'] = kwargs['gre_tunnel_count']
            # reset num_sessions
            kwargs['num_sessions'] = int(int(kwargs['num_sessions'])/int(kwargs['gre_tunnel_count']))
            config_status = add_link(rt_handle, **gre_args)
            device_handle = config_status['device_group_handle']
            result['gre_handle'] = config_status['gre_handle']
            topology_status = add_device_group(rt_handle,
                                               device_group_handle=device_handle,
                                               device_count=kwargs.get('num_sessions', '1'))
        elif ldra:
            params = kwargs
            if kwargs['ip_type'] == 'dual':
                params.pop('ip_type')
                _result_ = add_dhcp_client(rt_handle, **params)
                if _result_['status'] != '1':
                    raise Exception("failed to add dhcp client for v4 users when in LDRA dual mode")
                result['dhcpv4_client_handle'] = _result_['dhcpv4_client_handle']
                result['ldra_v4_device_group'] = _result_['device_group_handle']
            _result_ = add_ldra(rt_handle, **kwargs)
            if _result_['status'] != '1':
                raise Exception("failed to add ldra device")
            ldra_handle = _result_['ldra_handle']
            result['ldra_handle'] = ldra_handle
            device_handle = _result_['device_group_handle']
            kwargs['ip_type'] = 'ipv6'
            topology_status = add_device_group(rt_handle,
                                               device_group_handle=device_handle,
                                               device_count=kwargs.get('num_sessions', '1'))
        else:
            if rt_handle.ae and port in rt_handle.ae:
                device_handle = rt_handle.handles[port]['device_group_handle'][0]
                topology_status = add_device_group(rt_handle,
                                                   device_group_handle=device_handle,
                                                   device_count=kwargs.get('num_sessions', '1'))
            else:
                topology_status = add_device_group(rt_handle,
                                                   topology_handle=topo_handle,
                                                   device_count=kwargs.get('num_sessions', '1'))
        if topology_status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create device group for port handle {}".format(port))

        device_handle = topology_status['device_group_handle']
        result['device_group_handle'] = topology_status['device_group_handle']
        status = set_vlan(rt_handle, handle=device_handle, **kwargs)
        if status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create ethernet for device group {}".format(device_handle))
        #dhcp_args = dict()
        #dhcp_args['handle'] = port_handle
        dhcp_args['handle'] = status['ethernet_handle']
        result['ethernet_handle'] = status['ethernet_handle']
        dhcp_args['mode'] = 'create'
    elif 'handle' in kwargs:
        dhcp_args['mode'] = 'modify'
        dhcp_args['handle'] = kwargs['handle']
        if 'num_sessions' in kwargs:
            dhcp_args['num_sessions'] = kwargs['num_sessions']
        if 'vlan_start' in kwargs or 'svlan_start' in kwargs or 'mac' in kwargs:
            set_vlan(rt_handle, **kwargs)

    if 'dhcpv6_ia_type' in kwargs:
        dhcp_args['dhcp6_range_ia_type'] = kwargs.get('dhcpv6_ia_type')
    if 'dhcpv6_gateway' in kwargs:
        dhcp_args['dhcp6_gateway_address'] = kwargs['dhcpv6_gateway']
    if 'dhcpv6_gateway_custom' in kwargs:
        t.log('info', 'Configure custom dhcpv6 gateway')
        mv1_args = dict()
        mv1_args['pattern'] = "custom"
        mv1_args['nest_step'] = '0:0:0:0:0:0:0:1'
        mv1_args['nest_owner'] = topo_handle
        mv1_args['nest_enabled'] = '0'
        _result_ = rt_handle.invoke('multivalue_config', **mv1_args)
        mv1_handle = _result_['multivalue_handle']

        mv2_args = dict()
        mv2_args['multivalue_handle'] = mv1_handle
        mv2_args['custom_start'] = kwargs['dhcpv6_gateway_custom']['start-value']
        mv2_args['custom_step'] = '0:0:0:0:0:0:0:0'
        _result_ = rt_handle.invoke('multivalue_config', **mv2_args)
        mv2_handle = _result_['custom_handle']

        mv3_args = dict()
        mv3_args['custom_handle'] = mv2_handle
        mv3_args['custom_increment_value'] = kwargs['dhcpv6_gateway_custom']['step']
        mv3_args['custom_increment_count'] = kwargs['dhcpv6_gateway_custom']['sequence-length']
        _result_ = rt_handle.invoke('multivalue_config', **mv3_args)
        mv3_handle = _result_['increment_handle']

        mv4_args = dict()
        mv4_args['increment_handle'] = mv3_handle
        mv4_args['custom_increment_value'] = '0:0:0:0:0:0:0:0'
        mv4_args['custom_increment_count'] = kwargs['dhcpv6_gateway_custom']['repeat-each-value']
        _result_ = rt_handle.invoke('multivalue_config', **mv4_args)

        dhcp_args['dhcp6_gateway_address'] = mv1_handle

    # single value manual dhcpv4 gateway
    if 'dhcpv4_gateway' in kwargs:
        dhcp_args['dhcp4_gateway_address'] = kwargs['dhcpv4_gateway']
    # custom manual dhcpv4 gateway
    if 'dhcpv4_gateway_custom' in kwargs:
        t.log('info', 'Configure custom dhcpv4 gateway')
        mv1_args = dict()
        mv1_args['pattern'] = "custom"
        mv1_args['nest_step'] = '0.0.0.1'
        mv1_args['nest_owner'] = topo_handle
        mv1_args['nest_enabled'] = '0'
        _result_ = rt_handle.invoke('multivalue_config', **mv1_args)
        mv1_handle = _result_['multivalue_handle']

        mv2_args = dict()
        mv2_args['multivalue_handle'] = mv1_handle
        mv2_args['custom_start'] = kwargs['dhcpv4_gateway_custom']['start-value']
        mv2_args['custom_step'] = '0.0.0.0'
        _result_ = rt_handle.invoke('multivalue_config', **mv2_args)
        mv2_handle = _result_['custom_handle']

        mv3_args = dict()
        mv3_args['custom_handle'] = mv2_handle
        mv3_args['custom_increment_value'] = kwargs['dhcpv4_gateway_custom']['step']
        mv3_args['custom_increment_count'] = kwargs['dhcpv4_gateway_custom']['sequence-length']
        _result_ = rt_handle.invoke('multivalue_config', **mv3_args)
        mv3_handle = _result_['increment_handle']

        mv4_args = dict()
        mv4_args['increment_handle'] = mv3_handle
        mv4_args['custom_increment_value'] = '0.0.0.0'
        mv4_args['custom_increment_count'] = kwargs['dhcpv4_gateway_custom']['repeat-each-value']
        _result_ = rt_handle.invoke('multivalue_config', **mv4_args)

        dhcp_args['dhcp4_gateway_address'] = mv1_handle

    if 'rapid_commit' in kwargs:
        rapid_commit_map = {'1':1, '0':0, 1:1, 0:0, 'True':1, 'False':0, 'true':1, 'false':0}
        #dhcp_args['use_rapid_commit'] = kwargs.get('rapid_commit')
        dhcp_args['use_rapid_commit'] = rapid_commit_map[kwargs.get('rapid_commit')]

    if 'dhcp4_broadcast' in kwargs:
        dhcp_args['dhcp4_broadcast'] = kwargs.get('dhcp4_broadcast')

    if 'v6_max_no_per_client' in kwargs:
        dhcp_args['dhcp6_range_max_no_per_client'] = kwargs.get('v6_max_no_per_client')

    if 'dhcpv6_iana_count' in kwargs:
        dhcp_args['dhcp6_range_iana_count'] = kwargs.get('dhcpv6_iana_count')

    if 'dhcpv6_iapd_count' in kwargs:
        dhcp_args['dhcp6_range_iapd_count'] = kwargs.get('dhcpv6_iapd_count')
    v6handle = None
    handle = None
    if 'ip_type' in kwargs:
        if 'dual' in kwargs['ip_type']:
            config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcp_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcp client")
            else:
                if 'dhcpv4client_handle' in config_status and 'create' in dhcp_args['mode']:
                    handle = config_status['dhcpv4client_handle']
                    # rt_handle.dhcpv4_index += 1
                    # rt_handle.device_to_dhcpv4_index[handle] = rt_handle.dhcpv4_index
                    rt_handle.dhcpv4_client_handle.append(handle)
                    rt_handle.handles[port]['dhcpv4_client_handle'].append(handle)
                    result['dhcpv4_client_handle'] = handle

            dhcp_args['dhcp_range_ip_type'] = 'ipv6'
            config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcp_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcpv6 client for dual stack")
            else:
                if 'dhcpv6client_handle' in config_status and 'create' in dhcp_args['mode']:
                    v6handle = config_status['dhcpv6client_handle']
                    # rt_handle.dhcpv6_index += 1
                    # rt_handle.device_to_dhcpv6_index[v6handle] = rt_handle.dhcpv6_index
                    rt_handle.dhcpv6_client_handle.append(v6handle)
                    rt_handle.handles[port]['dhcpv6_client_handle'].append(v6handle)
                    result['dhcpv6_client_handle'] = v6handle

        elif kwargs['ip_type'] == "ipv4":
            dhcp_args['dhcp_range_ip_type'] = kwargs.get('ip_type')
            config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcp_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcp client")
            else:
                if 'dhcpv4client_handle' in config_status:
                    handle = config_status['dhcpv4client_handle']
                    # rt_handle.dhcpv4_index += 1
                    # rt_handle.device_to_dhcpv4_index[handle] = rt_handle.dhcpv4_index
                    rt_handle.dhcpv4_client_handle.append(handle)
                    rt_handle.handles[port]['dhcpv4_client_handle'].append(handle)
                    result['dhcpv4_client_handle'] = handle

        elif kwargs['ip_type'] == "ipv6":
            dhcp_args['dhcp_range_ip_type'] = kwargs.get('ip_type')
            config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcp_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcpv6 client")
            else:
                if 'dhcpv6client_handle' in config_status:
                    v6handle = config_status['dhcpv6client_handle']
                    # rt_handle.dhcpv6_index += 1
                    # rt_handle.device_to_dhcpv6_index[v6handle] = rt_handle.dhcpv6_index
                    rt_handle.dhcpv6_client_handle.append(v6handle)
                    rt_handle.handles[port]['dhcpv6_client_handle'].append(v6handle)
                    result['dhcpv6_client_handle'] = v6handle
    else:
        kwargs['ip_type'] = "ipv4"
        dhcp_args['dhcp_range_ip_type'] = kwargs.get('ip_type')
        config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcp_args)
        if config_status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to add dhcp client")
        else:
            if 'dhcpv4client_handle' in config_status:
                handle = config_status['dhcpv4client_handle']
                rt_handle.dhcpv4_client_handle.append(handle)
                rt_handle.handles[port]['dhcpv4_client_handle'].append(handle)
                # rt_handle.dhcpv4_index += 1
                result['dhcpv4_client_handle'] = handle
                #rt_handle.device_to_dhcpv4_index[handle] = rt_handle.dhcpv4_index
    if handle:
        if 'remote_id' in kwargs or 'circuit_id' in kwargs:
            if not set_option_82(rt_handle, handle=handle, **kwargs):
                result['status'] = '0'
        if 'vendor_class_id' in kwargs:
            if not set_option_60(rt_handle, handle=handle, **kwargs):
                result['status'] = '0'
        if 'www_server' in kwargs:
            if not set_option_72(rt_handle, handle=handle, **kwargs):
                result['status'] = '0'
    if v6handle:
        if 'interface_id' in kwargs or 'v6_remote_id' in kwargs and ldra:
            set_v6_option(rt_handle, handle=ldra_handle, **kwargs)
        if 'option_req' in kwargs or 'option20' in kwargs:
            set_v6_option(rt_handle, handle=v6handle, **kwargs)
        if 'dns_server' in kwargs:
            set_option_23(rt_handle, handle=v6handle, **kwargs)

    return result


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
    if not ('handle' in kwargs or 'type' in kwargs):
        raise Exception("dhcp handle or type  must be provided")
    dhcp_args = dict()

    if 'login_rate' in kwargs:
        dhcp_args['start_scale_mode'] = kwargs.get('login_rate_mode', 'device_group')

        login_rate = _add_rate_multivalue(rt_handle, kwargs['login_rate'])
        dhcp_args['request_rate'] = login_rate

        dhcp_args['outstanding_session_count'] = '1000'
        dhcp_args['override_global_setup_rate'] = '1'
        if 'outstanding' in kwargs:
            dhcp_args['outstanding_session_count'] = _add_rate_multivalue(rt_handle, kwargs['outstanding'])
            ##will change to multivalue handle for the rates in the future

    if 'logout_rate' in kwargs:
        dhcp_args['stop_scale_mode'] = kwargs.get('logout_rate_mode', 'device_group')
        logout_rate = _add_rate_multivalue(rt_handle, kwargs['logout_rate'])
        dhcp_args['release_rate'] = logout_rate
        dhcp_args['outstanding_releases_count'] = '1000'
        dhcp_args['override_global_teardown_rate'] = '1'

    if 'msg_timeout' in kwargs:
        dhcp_args['msg_timeout'] = kwargs['msg_timeout']

    if 'retry_count' in kwargs:
        dhcp_args['retry_count'] = kwargs['retry_count']

    if 'dhcpv6_sol_retries' in kwargs:
        dhcp_args['dhcp6_sol_max_rc'] = kwargs['dhcpv6_sol_retries']

    if 'dhcpv6_sol_timeout' in kwargs:
        dhcp_args['dhcp6_sol_timeout'] = kwargs['dhcpv6_sol_timeout']

    if dhcp_args:
        if 'v4' in kwargs['handle']:
            dhcp_args['dhcp4_arp_gw'] = '1'
            dhcp_args['ip_version'] = '4'
        if 'v6' in kwargs['handle']:
            dhcp_args['dhcp6_ns_gw'] = '1'
            dhcp_args['ip_version'] = '6'
            dhcp_args['dhcp6_echo_ia_info'] = '1'
        dhcp_args['handle'] = "/globals"
        dhcp_args['mode'] = "create"
        config_status = rt_handle.invoke('emulation_dhcp_config', **dhcp_args)
    return config_status


def _add_rate_multivalue(rt_handle, listitem):
    """
    :param rt_handle:                RT object
    :param listitem:            a list of rate values
    :return:
    """
    if isinstance(listitem, list):
        value = ''
        index = ''
        length = len(listitem)
        seq = 0
        for i in listitem:
            seq += 1
            if seq == length:
                value += "{}".format(i)
                index += "{}".format(seq)
            else:
                value += "{},".format(i)
                index += "{},".format(seq)
        print(value)
        print(index)
        mv_args = dict()
        mv_args['pattern'] = "single_value"
        mv_args['single_value'] = "50"
        mv_args['overlay_value'] = "{}".format(value)
        mv_args['overlay_index'] = "{}".format(index)
        _result_ = rt_handle.invoke('multivalue_config', **mv_args)
        if _result_['status'] != '1':
            raise Exception("failed to create multivalue handle for listitem {}".format(listitem))
        else:
            return  _result_['multivalue_handle']
    else:
        raise Exception("login rate must be a list")


def dhcp_client_action(rt_handle, **kwargs):
    """
    :param rt_handle:        RT object
    :param kwargs:
    port_handle:        specify a port handle to login all the clients?
    handle:             dhcp handles
    action:             start_handle, stop, renew, abort_handle, restart_down
    :return:
    result              dictionary include status and log message

    #dhcp_client_action(rt_handle, handle=rt_handle.handles['1/1']['dhcpv4_client_handle'][0], action='bind')
    #dhcp_client_action(rt_handle, port_handle='1/1/1', action='bind')
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
            dhcp_args['action'] = 'restart_down'
        elif 'start' in kwargs['action']:
            dhcp_args['action'] = 'bind'
        elif 'stop' in kwargs['action']:
            dhcp_args['action'] = 'release'

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
    """
    result = rt_handle.invoke('emulation_dhcp_stats', **kwargs)
    return result


def add_pppoe_client(rt_handle, **kwargs):
    """
    :param rt_handle:               RT object
    :param kwargs:
    port:                      specify a port  for creating a simulation
    num_sessions:              specify the simulation count

    auth_req_timeout:          authentication request timeout
    echo_req:                  echo request 1 or 0
    echo_rsp:                  echo response 1 or 0
    ip_type:                    v4/dual/v6
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    svlan_length:               svlan sequence length
    remote_id:                  agent_remote_id string, for example can be "remoteid" or "remoteid?"
    remote_id_start:            remote_id start value
    remote_id_step:             remote_id step value
    remote_id_repeat:           remote_id repeat value
    remote_id_length:           remote_id length
    circuit_id:                 agent_circuit_id string
    circuit_id_start:           circuit_id start value
    circuit_id_step:            circuit_id step value
    circuit_id_repeat:          circuit_id repeat value
    circuit_id_length:          circuit_id length
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
    pppoe_args = dict()
    if 'port' in kwargs:
        port = kwargs.get('port')
        if port not in rt_handle.handles:
            _result_ = add_topology(rt_handle, port_list=[port])
        #port_handle = rt_handle.port_to_handle_map[port]
        if rt_handle.ae and port in rt_handle.ae:
            device_handle = rt_handle.handles[port]['device_group_handle'][0]
            topology_status = add_device_group(rt_handle,
                                               device_group_handle=device_handle,
                                               device_count=kwargs.get('num_sessions', '1'))
        else:
        ##create devicegroup
            topo_handle = rt_handle.handles[port]['topo']
            topology_status = add_device_group(rt_handle,
                                               topology_handle=topo_handle,
                                               device_count=kwargs.get('num_sessions', '1'))
        if topology_status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create device group for port handle {}".format(port))

        device_handle = topology_status['device_group_handle']
        result['device_group_handle'] = topology_status['device_group_handle']
        status = set_vlan(rt_handle, handle=device_handle, **kwargs)
        if status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create ethernet for device group {}".format(device_handle))

        pppoe_args['handle'] = status['ethernet_handle']
        result['ethernet_handle'] = status['ethernet_handle']
        pppoe_args['mode'] = 'add'
        pppoe_args['port_role'] = 'access'
    if 'handle' in kwargs:
        pppoe_args['handle'] = kwargs['handle']
        pppoe_args['mode'] = 'modify'
        if 'num_sessions' in kwargs:
            pppoe_args['num_sessions'] = kwargs['num_sessions']
        if 'vlan_start' in kwargs or 'svlan_start' in kwargs:
            set_vlan(rt_handle, **kwargs)
    pppoe_args['port_role'] = 'access'
    if 'auth_req_timeout' in kwargs:
        pppoe_args['auth_req_timeout'] = kwargs['auth_req_timeout']
    if 'echo_req' in kwargs:
        pppoe_args['echo_req'] = kwargs['echo_req']
    if 'echo_rsp' in kwargs:
        pppoe_args['echo_rsp'] = kwargs['echo_rsp']
    if 'ip_type' in kwargs:
        if 'v4' in kwargs['ip_type']:
            pppoe_args['ip_cp'] = 'ipv4_cp'
        if 'v6' in kwargs['ip_type']:
            pppoe_args['ip_cp'] = 'ipv6_cp'
            if 'dhcpv6_ia_type' in kwargs:
                pppoe_args['dhcpv6_hosts_enable'] = '1'
                pppoe_args['dhcp6_pd_client_range_ia_type'] = kwargs['dhcpv6_ia_type']
        if 'dual' in kwargs['ip_type']:
            pppoe_args['ip_cp'] = 'dual_stack'
            if 'dhcpv6_ia_type' in kwargs:
                pppoe_args['dhcpv6_hosts_enable'] = '1'
                pppoe_args['dhcp6_pd_client_range_ia_type'] = kwargs['dhcpv6_ia_type']

    if 'ipcp_req_timeout' in kwargs:
        pppoe_args['ipcp_req_timeout'] = kwargs['ipcp_req_timeout']
    if 'max_auth_req' in kwargs:
        pppoe_args['max_auth_req'] = kwargs['max_auth_req']
    if 'max_padi_req' in kwargs:
        pppoe_args['max_padi_req'] = kwargs['max_padi_req']
    if 'max_padr_req' in kwargs:
        pppoe_args['max_padr_req'] = kwargs['max_padr_req']
    if 'max_ipcp_req' in kwargs:
        pppoe_args['max_ipcp_req'] = kwargs['max_ipcp_req']
    if 'max_terminate_req' in kwargs:
        pppoe_args['max_terminate_req'] = kwargs['max_terminate_req']
    if 'echo_req_interval' in kwargs:
        pppoe_args['echo_req_interval'] = kwargs['echo_req_interval']
    if 'auth_mode' in kwargs:
        pppoe_args['auth_mode'] = kwargs['auth_mode']
        if 'username' in kwargs:
            username = kwargs['username'].replace('?', '{Inc:1,,,1}')
            _result_ = add_string_mv(rt_handle, string_name=username)
            multivalue_5_handle = _result_['multivalue_handle']
        if 'pap' in kwargs['auth_mode']:
            if 'username'  in kwargs:
                pppoe_args['username'] = multivalue_5_handle
            if 'password' in kwargs:
                pppoe_args['password'] = kwargs['password']
        if 'chap' in kwargs['auth_mode']:
            if 'username' in kwargs:
                pppoe_args['chap_name'] = multivalue_5_handle
            if 'password' in kwargs:
                pppoe_args['chap_secret'] = kwargs['password']

    if 'circuit_id' in kwargs:
        circuit_id = kwargs.get('circuit_id')
        if 'circuit_id_start' in kwargs:
            start = str(kwargs.get('circuit_id_start'))
            step = str(kwargs.get('circuit_id_step', '1'))
            repeat = str(kwargs.get('circuit_id_repeat', '1'))
            length = str(kwargs.get('circuit_id_length', ''))
            if '?' in circuit_id:
                increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                circuit_id = circuit_id.replace('?', increment)
            else:
                circuit_id = circuit_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
        else:
            circuit_id = kwargs['circuit_id'].replace('?', '{Inc:1,,,1}')
        _result_ = add_string_mv(rt_handle, string_name=circuit_id)
        print(_result_)
        multivalue_6_handle = _result_['multivalue_handle']
        pppoe_args['agent_circuit_id'] = multivalue_6_handle

    if 'remote_id' in kwargs:
        remote_id = kwargs.get('remote_id')
        if 'remote_id_start' in kwargs:
            start = str(kwargs.get('remote_id_start'))
            step = str(kwargs.get('remote_id_step', '1'))
            repeat = str(kwargs.get('remote_id_repeat', '1'))
            length = str(kwargs.get('remote_id_length', ''))
            if '?' in remote_id:
                increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                remote_id = remote_id.replace('?', increment)
            else:
                remote_id = remote_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
        else:
            remote_id = kwargs['remote_id'].replace('?', '{Inc:1,,,1}')
        _result_ = add_string_mv(rt_handle, string_name=remote_id)
        print(_result_)
        multivalue_7_handle = _result_['multivalue_handle']
        pppoe_args['agent_remote_id'] = multivalue_7_handle
    if 'circuit_id' in kwargs or 'remote_id' in kwargs:
        pppoe_args['enable_client_signal_loop_id'] = '1'
    pppoe_args['redial'] = kwargs.get('redial', 0)
    config_status = rt_handle.invoke('pppox_config', **pppoe_args)
    #print(config_status)
    if config_status['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to add/modify pppoe client for port {}".format(port))
    else:
        if 'pppox_client_handle' in config_status and 'add' in pppoe_args['mode']:
            handle = config_status['pppox_client_handle']
            rt_handle.pppox_client_handle.append(handle)
            result['pppox_client_handle'] = handle
            rt_handle.handles[port]['pppox_client_handle'].append(handle)
            if 'ip_type' in kwargs:
                if 'v6' in kwargs['ip_type'] or 'dual' in kwargs['ip_type']:
                    if 'dhcpv6_client_handle' in config_status:
                        v6handle = config_status['dhcpv6_client_handle']
                        rt_handle.dhcpv6_client_handle.append(v6handle)
                        result['dhcpv6_client_handle'] = v6handle
                        rt_handle.handles[port]['dhcpv6_over_pppox_handle'][handle] = v6handle

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
        status = rt_handle.invoke('pppox_config', mode='modify', **kwargs)
        return status

    else:
    ##set the login/logout rate
        pppox_args = dict()
        pppox_args['port_role'] = "access"
        pppox_args['handle'] = "/globals"
        pppox_args['mode'] = 'add'
        if 'login_rate' in kwargs:
            login_rate = _add_rate_multivalue(rt_handle, kwargs['login_rate'])
            pppox_args['attempt_rate'] = login_rate
            pppox_args['attempt_max_outstanding'] = '1000'
            pppox_args['attempt_scale_mode'] = kwargs.get('rate_mode', 'device_group')
            if 'outstanding' in kwargs:
                pppox_args['attempt_max_outstanding'] = _add_rate_multivalue(rt_handle, kwargs['outstanding'])
        if 'logout_rate' in kwargs:
            logout_rate = _add_rate_multivalue(rt_handle, kwargs['logout_rate'])
            pppox_args['disconnect_rate'] = logout_rate
            pppox_args['disconnect_max_outstanding'] = '1000'
            pppox_args['disconnect_scale_mode'] = kwargs.get('rate_mode', 'device_group')

        result = rt_handle.invoke('pppox_config', **pppox_args)
        return result


def pppoe_client_action(rt_handle, **kwargs):
    """
    login/logout pppoe client
    :param rt_handle:            RT object
    :param kwargs:
    handle:                 pppox handles/ dhcpv6 over pppox handle
    action:                 start, stop, restart_down, reset, abort
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
        pppoe_args['action'] = kwargs.get('action')
        if 'restart' in kwargs['action']:
            pppoe_args['action'] = 'restart_down'
        elif 'start' in kwargs['action']:
            pppoe_args['action'] = 'connect'
        elif 'stop' in kwargs['action']:
            match = re.match(r'.*pppoxclient:\d+', kwargs['handle'])
            kwargs['handle'] = match.group(0)
            pppoe_args['action'] = 'disconnect'

        pppoe_args['handle'] = kwargs['handle']
        result = rt_handle.invoke('pppox_control', **pppoe_args)
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
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    svlan_length:               svlan sequence length
    ip_addr
    ip_addr_step
    netmask:                    netmask, e.g. 255.255.255.0
    gateway
    gateway_step:
    ipv6_addr
    ipv6_addr_step
    ipv6_prefix_length
    ipv6_gateway
    ipv6_gateway_step:
    gateway_mac:                gateway mac address
    gre_dst_ip
    gre_dst_ip_step
    count
    mac_resolve:               resolve gateway
    name:                      link name

    :return:
    device group handle
    ethernet handle
    ip handle
    gre handle
    status
    """
    if 'port' not in kwargs:
        raise Exception("port is mandatory when adding link device")
    port = kwargs.get('port')
    #port_handle = rt_handle.port_to_handle_map[port]
    if port not in rt_handle.handles:
        _result_ = add_topology(rt_handle, port_list=[port])
    topo_handle = rt_handle.handles[port]['topo']
    count = kwargs.get('count', '1')
    link_args = dict()
    result = dict()
    result['status'] = '1'
    device_args = {}
    if 'name' in kwargs:
        device_args['device_group_name'] = kwargs['name']
    if rt_handle.ae and port in rt_handle.ae:
        device_handle = rt_handle.handles[port]['device_group_handle'][0]
        device_args['device_group_handle'] = device_handle
    else:
        device_args['topology_handle'] = topo_handle
    device_args['device_count'] = count
    #create device group first
    status_config = add_device_group(rt_handle, **device_args)
    if status_config['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to add device group for port {}".format(port))
    else:
        device_group_handle = status_config['device_group_handle']
        link_args['protocol_handle'] = device_group_handle
        rt_handle.device_group_handle.append(device_group_handle)
        rt_handle.handles[port]['device_group_handle'].append(device_group_handle)
        result['device_group_handle'] = device_group_handle

    # create ethernet and set vlans
    status_config = set_vlan(rt_handle, handle=device_group_handle, **kwargs)
    if status_config['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to add ethernet/vlan for device group {}".format(device_group_handle))
    else:
        ethernet_handle = status_config['ethernet_handle']

        rt_handle.handles[port]['ethernet_handle'].append(ethernet_handle)
        result['ethernet_handle'] = ethernet_handle
        tag_status = kwargs.get('set_tag', False)
        if tag_status:
            repeat = int(kwargs.get('vlan_repeat', 1))
            length = int(int(count) / repeat) + (int(count) % repeat > 0)
            tag_mv = rt_handle.invoke('_set_custom_pattern', start=1, step=1, repeat=repeat, count=length)
            rt_handle.invoke('traffic_tag_config', handle=ethernet_handle, enabled='1', name="TAG", id=tag_mv)

    intf_args = dict()
    intf_args['protocol_handle'] = ethernet_handle
    if 'ip_addr' in kwargs:
        intf_args['intf_ip_addr'] = kwargs['ip_addr']
        intf_args['intf_ip_addr_step'] = kwargs.get('ip_addr_step', '0.0.1.0')
        if 'gateway' in kwargs:
            intf_args['gateway'] = kwargs['gateway']
            intf_args['gateway_step'] = kwargs.get('ip_addr_step', '0.0.1.0')
            if intf_args['intf_ip_addr_step'] == '0.0.0.1':
                intf_args['gateway_step'] = '0.0.0.0'
            if 'gateway_step' in kwargs:
                intf_args['gateway_step'] = kwargs['gateway_step']
        if 'netmask' in kwargs:
            intf_args['netmask'] = kwargs['netmask']
        if 'mac_resolve' in kwargs:
            intf_args['ipv4_resolve_gateway'] = kwargs['mac_resolve']
        if 'gateway_mac' in kwargs:
            intf_args['ipv4_resolve_gateway'] = '0'
            intf_args['ipv4_manual_gateway_mac'] = kwargs['gateway_mac']

    if 'ipv6_addr' in kwargs:
        intf_args['ipv6_intf_addr'] = kwargs['ipv6_addr']
        intf_args['ipv6_intf_addr_step'] = kwargs.get('ipv6_addr_step', '00:00:00:01:00:00:00:00')
        if 'ipv6_gateway' in kwargs:
            intf_args['ipv6_gateway'] = kwargs['ipv6_gateway']
            intf_args['ipv6_gateway_step'] = kwargs.get('ipv6_addr_step', '00:00:00:01:00:00:00:00')
            if 'ipv6_gateway_step' in kwargs:
                intf_args['ipv6_gateway_step'] = kwargs['ipv6_gateway_step']

        if 'ipv6_prefix_length' in kwargs:
            intf_args['ipv6_prefix_length'] = kwargs.get('ipv6_prefix_length', '64')
        if 'mac_resolve' in kwargs:
            intf_args['ipv6_resolve_gateway'] = kwargs['mac_resolve']
        if 'gateway_mac' in kwargs:
            intf_args['ipv6_resolve_gateway'] = '0'
            intf_args['ipv6_manual_gateway_mac'] = kwargs['gateway_mac']
    if 'ip_addr' in kwargs or 'ipv6_addr' in kwargs:
        status_config = rt_handle.invoke('interface_config', **intf_args)
        if status_config['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to add ip/ipv6 address for ethernet {}".format(ethernet_handle))
        else:
            if 'ipv4_handle' in status_config:
                ip_handle = status_config['ipv4_handle']
                rt_handle.link_ip_handle.append(ip_handle)
                rt_handle.handles[port]['ipv4_handle'] = ip_handle
                result['ipv4_handle'] = ip_handle
            if 'ipv6_handle' in status_config:
                ipv6_handle = status_config['ipv6_handle']
                rt_handle.link_ipv6_handle.append(ipv6_handle)
                rt_handle.handles[port]['ipv6_handle'].append(ipv6_handle)
                result['ipv6_handle'] = ipv6_handle

    if 'gre_dst_ip' in kwargs:
        ###config gre over ip
        gre_args = dict()
        gre_args['protocol_handle'] = ip_handle
        gre_args['gre_dst_ip_addr'] = kwargs['gre_dst_ip']
        if 'gre_dst_ip_step' in kwargs:
            gre_args['gre_dst_ip_addr_step'] = kwargs['gre_dst_ip_step']

        status_config = rt_handle.invoke('interface_config', **gre_args)
        if status_config['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to add gre destination address for ip handle {}".format(ip_handle))
        else:
            gre_handle = status_config['greoipv4_handle']
            rt_handle.link_gre_handle.append(gre_handle)
            rt_handle.handles[port]['gre_handle'] = gre_handle
            result['gre_handle'] = gre_handle

    return result


def remove_link(rt_handle, **kwargs):
    # rt_handle.invoke('topology_config(mode='destroy', device_group_handle='/topology:2/deviceGroup:1')
    """
    :param rt_handle:                        RT object
    :param device_handle:               Device handle
    :return:
    """
    device_handle = kwargs['device_handle']
    status = rt_handle.invoke('topology_config', mode='destroy', device_group_handle=device_handle)
    rt_handle.device_group_handle.remove(device_handle)
    return status


def link_action(rt_handle, **kwargs):
    """
    start/stop links
    :param rt_handle:                    RT object
    :param kwargs:
    handle:                         device_group/ip handle
    action:                         start/stop/abort/check_link_state(which use port_handle only)
    :return:
    status:                         1 or 0
    """
    control_args = dict()
    control_args['handle'] = kwargs['handle']

    if 'start' in kwargs['action']:
        control_args['action'] = 'start_protocol'
    elif 'stop' in kwargs['action']:
        control_args['action'] = 'stop_protocol'
    elif 'abort' in kwargs['action']:
        control_args['action'] = 'abort_protocol'
    else:
        control_args['action'] = kwargs['action']

    return rt_handle.invoke('test_control', **control_args)


def add_traffic(rt_handle, **kwargs):
    #add_traffic(rt_handle, source=rt_handle.dhcpv4_client_handle, frame_size=[100,1500, 10])
    """
    set traffic streams
    :param rt_handle:                RT object
    :param kwargs:
    name:                       used defined stream name (optional)
    source:                     a list of traffic source handle
    destination:                a list of traffic destination handle
    multicast:                  a list of destination multicast address(can be "all_multicast_ranges" or in the format of ['225.0.0.1/0.0.0.1/2']
    bidirectional:              1 or 0
    rate:                       traffic rate , can be mbps, pps, percent, for example: 1000mbps, 1000pps, 100%
    packets_count:              number of packets to be transmitted
    duration:                   number of seconds to transmit traffic
    type:                       traffic type "ipv4" or "ipv6" or "ethernet_vlan"
    mesh_type                   traffic mesh type, default is many_to_many, can be one_to_one
    dynamic_update:             dynamic_udate the address values from ppp
    frame_size:                 single value /a list [min max step]/[min max]
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
    ip_dscp:                    ip dscp value
    ipv6_traffic_class:         ipv6 traffic class value
    ipv6_traffic_class_mode:    ipv6 traffic class mode(fixed, incr,decr)
    egress_tracking:            egress tracking mode: dscp/ipv6TC/tos_precedence/outer_vlan_priority
    burst_rate:                 set the mean burst rate for the stream(% of line rate), must be used with frame_size, pkts_per_burst
    :return:
    status and hash
    """
    traffic_args = dict()
    traffic_args['traffic_generator'] = "ixnetwork_540"
    traffic_args['src_dest_mesh'] = kwargs.get('mesh_type', 'many_to_many')
    traffic_args['bidirectional'] = kwargs.get('bidirectional', '1')
    if 'l3_length' in kwargs:
        traffic_args['l3_length'] = kwargs['l3_length']
    if 'transmit_mode' in kwargs and 'burst' in kwargs['transmit_mode']:
        traffic_args['transmit_mode'] = kwargs['transmit_mode']
    if 'transmit_distribution' in kwargs:
        traffic_args['transmit_distribution'] = kwargs['transmit_distribution']
    if 'rate_distribution_mode' in kwargs:
        traffic_args['frame_rate_distribution_stream'] = kwargs['rate_distribution_mode']
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
        traffic_args['inter_burst_gap'] = ibg_bytes
        traffic_args['inter_burst_gap_unit'] = 'bytes'
        nano_secs = ibg_bytes * 8 * 1000000000 / line_rate
        ##use nano seconds before HLAPI bug solved
        #traffic_args['inter_burst_gap'] = nano_secs
        #traffic_args['inter_frame_gap_unit'] = 'bytes' #ns
        if 'rate' in kwargs:
            kwargs.pop('rate')
    #import re
    if 'convert_to_raw' in kwargs:
        traffic_args['convert_to_raw'] = "1"
    if 'name' in kwargs:
        traffic_args['name'] = kwargs['name']
    if 'source' in kwargs:
        traffic_args['emulation_src_handle'] = kwargs['source']
        if 'v6' in kwargs['source']:
            traffic_args['circuit_endpoint_type'] = "ipv6"
    else:
        if 'type' in kwargs and 'v6' in kwargs['type']:
            traffic_args['emulation_src_handle'] = rt_handle.dhcpv6_client_handle
        else:
            traffic_args['emulation_src_handle'] = rt_handle.dhcpv4_client_handle + rt_handle.pppox_client_handle

    if 'destination' in kwargs:
        traffic_args['emulation_dst_handle'] = kwargs['destination']
        if 'v6' in kwargs['destination']:
            traffic_args['circuit_endpoint_type'] = "ipv6"
    elif 'multicast' in kwargs:
        traffic_args['emulation_multicast_dst_handle'] = kwargs['multicast']
        traffic_args['emulation_dst_handle'] = ''
        traffic_args['emulation_multicast_dst_handle_type'] = 'none'
    else:
        if 'type' in kwargs and 'v6' in kwargs['type']:
            traffic_args['emulation_dst_handle'] = rt_handle.link_ipv6_handle
        else:
            traffic_args['emulation_dst_handle'] = rt_handle.link_ip_handle

    if 'rate' in kwargs:
        if 'mbps' in kwargs['rate']:
            traffic_args['rate_mbps'] = re.sub('mbps', '', kwargs['rate'])
        if 'pps' in kwargs['rate']:
            traffic_args['rate_pps'] = re.sub('pps', '', kwargs['rate'])
        if '%' in kwargs['rate']:
            traffic_args['rate_percent'] = re.sub('%', '', kwargs['rate'])
    else:
        if 'burst_rate' not in kwargs:
            traffic_args['rate_pps'] = '1000'

    if 'packets_count' in kwargs:
        traffic_args['transmit_mode'] = 'single_burst'
        #traffic_args['pkts_per_burst'] = kwargs['packets_count']
        traffic_args['number_of_packets_per_stream'] = kwargs['packets_count']

    if 'duration' in kwargs:
        traffic_args['duration'] = kwargs['duration']
    if 'stream_id' in kwargs:
        traffic_args['mode'] = 'modify'
    else:
        traffic_args['mode'] = 'create'

    if 'type' in kwargs:
        traffic_args['circuit_endpoint_type'] = kwargs['type']
    if 'dynamic_update' in kwargs:
        traffic_args['dynamic_update_fields'] = kwargs['dynamic_update']
    if 'ip_precedence' in kwargs:
        traffic_args['ip_precedence'] = kwargs['ip_precedence']
    if 'ip_precedence_mode' in kwargs:
        traffic_args['ip_precedence_mode'] = kwargs['ip_precedence_mode']
    if 'ip_precedence_step' in kwargs:
        traffic_args['ip_precedence_step'] = kwargs['ip_precedence_step']
    if 'ip_precedence_count' in kwargs:
        traffic_args['ip_precedence_count'] = kwargs['ip_precedence_count']
    if 'ip_dscp' in kwargs:
        traffic_args['ip_dscp'] = kwargs['ip_dscp']
    if 'ip_dscp_mode' in kwargs:
        traffic_args['ip_dscp_mode'] = kwargs['ip_dscp_mode']
    if 'ip_dscp_step' in kwargs:
        traffic_args['ip_dscp_step'] = kwargs['ip_dscp_step']
    if 'ip_dscp_count' in kwargs:
        traffic_args['ip_dscp_count'] = kwargs['ip_dscp_count']
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
            traffic_args['frame_size'] = kwargs['frame_size']
    else:
        if 'l3_length' not in kwargs:
            traffic_args['frame_size'] = '1000'
    ##can also track by sourceDestEndpointPair0
    traffic_args['track_by'] = kwargs.get('track_by', 'sourceDestValuePair0 trackingenabled0')
    if 'egress_tracking' in kwargs:
        traffic_args['egress_tracking'] = kwargs['egress_tracking']
    if 'ipv6_traffic_class' in kwargs:
        traffic_args['ipv6_traffic_class'] = kwargs['ipv6_traffic_class']
        traffic_args['ipv6_traffic_class_mode'] = kwargs.get('ipv6_traffic_class_mode', 'fixed')
        if 'ipv6_traffic_class_step' in kwargs:
            traffic_args['ipv6_traffic_class_step'] = kwargs['ipv6_traffic_class_step']
        if 'ipv6_traffic_class_count' in kwargs:
            traffic_args['ipv6_traffic_class_count'] = kwargs['ipv6_traffic_class_count']
    if 'traffic_generate' in kwargs:
        traffic_args['traffic_generate'] = kwargs['traffic_generate']
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

    if 'udp_dst_port' in kwargs or 'udp_src_port' in kwargs:
        traffic_args['l4_protocol'] = 'udp'
        if 'udp_dst_port' in kwargs:
            traffic_args['udp_dst_port'] = kwargs['udp_dst_port']
            traffic_args['udp_dst_port_mode'] = kwargs.get('udp_dst_port_mode', 'fixed')
            if 'udp_dst_port_step' in kwargs:
                traffic_args['udp_dst_port_step'] = kwargs['udp_dst_port_step']
            if 'udp_dst_port_count' in kwargs:
                traffic_args['udp_dst_port_count'] = kwargs['udp_dst_port_count']
        if 'udp_src_port' in kwargs:
            traffic_args['udp_src_port'] = kwargs['udp_src_port']
            traffic_args['udp_src_port_mode'] = kwargs.get('udp_src_port_mode', 'fixed')
            if 'udp_src_port_step' in kwargs:
                traffic_args['udp_src_port_step'] = kwargs['udp_src_port_step']
            if 'udp_src_port_count' in kwargs:
                traffic_args['udp_src_port_count'] = kwargs['udp_src_port_count']

    if 'scalable_src' in kwargs:
        rt_handle.ixiatcl.set_py('ti_scalable_srcs(EndpointSet-1)',[kwargs['source']])
        rt_handle.ixiatcl.set_py('ti_scalable_srcs_port_start(EndpointSet-1)',
                                 [int(kwargs.get('scalable_src_port_start', 1))])
        rt_handle.ixiatcl.set_py('ti_scalable_srcs_port_count(EndpointSet-1)',
                                 [int(kwargs.get('scalable_src_port_count', 1))])
        rt_handle.ixiatcl.set_py('ti_scalable_srcs_intf_start(EndpointSet-1)',
                                 [int(kwargs.get('scalable_src_intf_start', 1))])
        rt_handle.ixiatcl.set_py('ti_scalable_srcs_intf_count(EndpointSet-1)',
                                 [int(kwargs.get('scalable_src_intf_count', 1))])
        traffic_args['emulation_scalable_src_handle'] = 'ti_scalable_srcs'
        traffic_args['emulation_scalable_src_port_start'] = 'ti_scalable_srcs_port_start'
        traffic_args['emulation_scalable_src_port_count'] = 'ti_scalable_srcs_port_count'
        traffic_args['emulation_scalable_src_intf_start'] = 'ti_scalable_srcs_intf_start'
        traffic_args['emulation_scalable_src_intf_count'] = 'ti_scalable_srcs_intf_count'

    if 'scalable_dst' in kwargs:
        rt_handle.ixiatcl.set_py('ti_scalable_dsts(EndpointSet-1)',[kwargs['destination']])
        rt_handle.ixiatcl.set_py('ti_scalable_dsts_port_start(EndpointSet-1)',
                                 [int(kwargs.get('scalable_dst_port_start', 1))])
        rt_handle.ixiatcl.set_py('ti_scalable_dsts_port_count(EndpointSet-1)',
                                 [int(kwargs.get('scalable_dst_port_count', 1))])
        rt_handle.ixiatcl.set_py('ti_scalable_dsts_intf_start(EndpointSet-1)',
                                 [int(kwargs.get('scalable_dst_intf_start', 1))])
        rt_handle.ixiatcl.set_py('ti_scalable_dsts_intf_count(EndpointSet-1)',
                                 [int(kwargs.get('scalable_dst_intf_count', 1))])
        traffic_args['emulation_scalable_dst_handle'] = 'ti_scalable_dsts'
        traffic_args['emulation_scalable_dst_port_start'] = 'ti_scalable_dsts_port_start'
        traffic_args['emulation_scalable_dst_port_count'] = 'ti_scalable_dsts_port_count'
        traffic_args['emulation_scalable_dst_intf_start'] = 'ti_scalable_dsts_intf_start'
        traffic_args['emulation_scalable_dst_intf_count'] = 'ti_scalable_dsts_intf_count'
    if 'tag' in kwargs:
        result = kwargs['tag'].split(sep=',')
        item_list = []
        for item in result:
            if '-' in item:
                result.remove(item)
                tagrange = item.split(sep='-')
                item_list = item_list + [key for key in range(int(tagrange[0]), int(tagrange[-1]) + 1)]

        item_list += [int(item) for item in result]
        item_list.sort()
        tagvalue = 'TAG:' + ','.join(str(item) for item in item_list)
        traffic_args['tag_filter'] = tagvalue

    config_status = rt_handle.invoke('traffic_config', **traffic_args)
    if config_status['status'] == '1':
        if traffic_args['mode'] == 'create':
            rt_handle.traffic_item.append(config_status['stream_id'])
            rt_handle.stream_id.append(config_status['traffic_item'])
    return config_status


def set_traffic(rt_handle, **kwargs):
    """
    modify existing trafficitem
    :param rt_handle:                RT object
    :param kwargs:              see Ixia API library

    :return:
    status:                    1 or 0
    """
    result = dict()
    result['status'] = '1'
    if 'stream_id' not in kwargs:
        result['status'] = '0'
        print("stream_id is mandatory when modifying traffic item")
        return result
    result = rt_handle.invoke('traffic_config', mode='modify', **kwargs)
    return result


def get_traffic_stats(rt_handle, **kwargs):
    """

    :param kwargs:
    :param rt_handle:         RT object
    mode:                all/traffic_item/l23_test_summary
    :return:
    """
    stats_status = rt_handle.invoke('traffic_stats', **kwargs)
    return stats_status


def get_protocol_stats(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param mode:        'global_per_protocol'| 'global_per_port', by default is 'global_per_protocol'
    :return:
    """
    mode = kwargs.get('mode', 'global_per_protocol')
    stats_status = rt_handle.invoke('protocol_info', mode=mode)

    return stats_status


def traffic_action(rt_handle, **kwargs):
    """
    #traffic_action(rt_handle, action='start')
    :param rt_handle:            RT object
    :param kwargs:
    action:                 start/stop/delete/poll/regenerate/apply/clearstats/reset
    handle:                 specify a specific traffic item if needed
    duration:               specify the traffic running time
    timeout:                max wait time
    type:                   traffic type, default l23, <l47|l23>
    :return:
    """
    traffic_args = dict()
    if 'timeout' in kwargs:
        traffic_args['max_wait_timer'] = kwargs['timeout']
    if 'handle' in kwargs:
        traffic_args['handle'] = kwargs['handle']
    traffic_args['action'] = 'run'
    if 'start' in kwargs['action']:
        traffic_args['action'] = 'sync_run'
    if 'stop' in kwargs['action']:
        traffic_args['action'] = 'stop'
    if 'poll' in kwargs['action']:
        traffic_args['action'] = 'poll'
    if 'clearstats' in kwargs['action']:
        traffic_args['action'] = 'clear_stats'
    if 'reset' in kwargs['action']:
        traffic_args['action'] = 'reset'
    if 'regenerate' in kwargs['action']:
        traffic_args['action'] = 'regenerate'
    if 'apply' in kwargs['action']:
        traffic_args['action'] = 'apply'
    if 'delete' in kwargs['action']:
        traffic_args['action'] = 'destroy'
    if 'duration' in kwargs:
        traffic_args['duration'] = kwargs['duration']
    if 'type' in kwargs:
        traffic_args['type'] = kwargs['type']

    if 'delete' in kwargs['action'] and 'handle' in kwargs:
        traffic_args['mode'] = 'remove'
        traffic_args.pop('handle')
        traffic_args.pop('action')
        traffic_args['stream_id'] = kwargs['handle']
        result = rt_handle.invoke('traffic_config', **traffic_args)
        print(traffic_args)
    else:
        result = rt_handle.invoke('traffic_control', **traffic_args)
    if result['status'] == '1' and 'delete' in kwargs['action']:
        if 'handle' in kwargs:
            rt_handle.traffic_item.remove(kwargs['handle'])
        else:
            rt_handle.traffic_item.clear()
    return result


def start_all(rt_handle):
    """
    start all protocols
    :param rt_handle:                    RT object
    :return:
    a dictionary of status and other information
    """
    return rt_handle.invoke('test_control', action='start_all_protocols')


def stop_all(rt_handle):
    """
    stop all protocols
    :param rt_handle:                    RT object
    :return:
    a dictionary of status and other information
    """
    return rt_handle.invoke('test_control', action='stop_all_protocols')


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
    igmp_param = dict()
    igmp_param['handle'] = kwargs.get('handle')
    igmp_param['mode'] = kwargs.get('mode', 'create')
    igmp_param['active'] = kwargs.get('active', '1')
    igmp_param['filter_mode'] = kwargs.get('filter_mode', 'include')
    igmp_param['enable_iptv'] = kwargs.get('iptv', '0')
    igmp_param['igmp_version'] = 'v' + str(kwargs.get('version', '2'))

    _result_ = rt_handle.invoke('emulation_igmp_config', **igmp_param)
    print(_result_)
    if _result_['status'] != '1':
        result['log'] = "failed to add igmp client"
        result['status'] = '0'
        return result
    else:
        igmp_handle = _result_['igmp_host_handle']
        rt_handle.igmp_handles[kwargs.get('handle')] = igmp_handle
        rt_handle.igmp_handle_to_group[igmp_handle] = {}
        result['igmp_host_handle'] = igmp_handle

    addr_param = dict()
    addr_param['start'] = kwargs.get('group_start_addr', '225.0.0.1')
    addr_param['step'] = kwargs.get('group_range_step', "0.0.1.0")
    addr_param['count'] = kwargs.get('group_range_length', "1")
    multivalue_2_handle = _add_addr_custom_pattern(rt_handle, **addr_param)
    mcast_args = dict()
    mcast_args['mode'] = "create"
    mcast_args['ip_addr_start'] = multivalue_2_handle
    mcast_args['ip_addr_step'] = kwargs.get('group_step', "0.0.0.1")
    mcast_args['num_groups'] = kwargs.get('group_count', "1")
    mcast_args['active'] = kwargs.get('active', "1")
    _result_ = rt_handle.invoke('emulation_multicast_group_config', **mcast_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        return result
    else:
        igmp_group_handle = _result_['multicast_group_handle']
        rt_handle.igmp_handle_to_group[igmp_handle]['group_handle'] = igmp_group_handle


    src_addr_param = dict()
    src_addr_param['start'] = kwargs.get('src_grp_start_addr', "10.10.10.1")
    src_addr_param['step'] = kwargs.get('src_grp_range_step', "0.0.1.0")
    src_addr_param['count'] = kwargs.get('src_grp_range', "1")
    multivalue_3_handle = _add_addr_custom_pattern(rt_handle, **src_addr_param)
    src_args = dict()
    src_args['mode'] = "create"
    src_args['ip_addr_start'] = multivalue_3_handle
    src_args['ip_addr_step'] = kwargs.get('src_grp_step', "0.0.0.1")
    src_args['num_sources'] = kwargs.get('src_grp_count', "1")
    src_args['active'] = "1"
    _result_ = rt_handle.invoke('emulation_multicast_source_config', **src_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        return result
    else:
        igmp_source_handle = _result_['multicast_source_handle']
        rt_handle.igmp_handle_to_group[igmp_handle]['src_group_handle'] = igmp_source_handle
    grp_args = dict()
    grp_args['mode'] = kwargs.get('mode', "create")
    grp_args['g_filter_mode'] = kwargs.get('filter_mode', "include")
    grp_args['group_pool_handle'] = igmp_group_handle
    grp_args['no_of_grp_ranges'] = kwargs.get('group_range', "1")
    grp_args['no_of_src_ranges'] = kwargs.get('src_grp_range', "1")
    grp_args['session_handle'] = igmp_handle
    grp_args['source_pool_handle'] = igmp_source_handle
    _result_ = rt_handle.invoke('emulation_igmp_group_config', **grp_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        result['log'] = "failed to config the igmp group and src group set"
    else:
        result['igmp_group_handle'] = _result_['igmp_group_handle']
        result['igmp_source_handle'] = _result_['igmp_source_handle']
        rt_handle.igmp_handle_to_group[igmp_handle]['igmp_group_handle'] = _result_['igmp_group_handle']
        rt_handle.igmp_handle_to_group[igmp_handle]['igmp_source_handle'] = _result_['igmp_source_handle']

    return result


def igmp_client_action(rt_handle, **kwargs):
    """
    :param rt_handle:                                RT object
    :param kwargs:
    handle:                                     igmp host handle
    action:                                     start/stop/join/leave/igmp_send_specific_query
    start_group_addr:                           only used for igmp_send_secific_query
    group_count:                                only used for igmp_send_secific_query
    start_source_addr:                          only used for igmp_send_secific_query
    source_count:                               only used for igmp_send_secific_query
    :return:
    """
    action_param = dict()
    action_param['handle'] = kwargs['handle']
    if 'action' in kwargs:
        action_param['mode'] = kwargs['action']
    if 'start_group_addr' in kwargs:
        action_param['start_group_address'] = kwargs['start_group_addr']
    if 'group_count' in kwargs:
        action_param['group_count'] = kwargs['group_count']
    if 'start_source_addr' in kwargs:
        action_param['start_source_address'] = kwargs['start_source_addr']
    if 'source_count' in kwargs:
        action_param['source_count'] = kwargs['source_count']
    return rt_handle.invoke('emulation_igmp_control', **action_param)


def _add_addr_custom_pattern(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    :return:        multivalue_handle
    """

    if 'type' not in kwargs:
        ip_type = 'v4'
    else:
        ip_type = kwargs['type']

    _result_ = rt_handle.invoke('multivalue_config', pattern="custom")
    print(_result_)
    multivalue_handle = _result_['multivalue_handle']
    if 'v4' in ip_type:
        custom_step = kwargs.get('outstep', "0.0.0.0")
        custom_start = kwargs.get('start')
        increment_value = kwargs.get('step')

    else:
        custom_step = ipaddress.IPv6Address(kwargs.get('outstep', '::')).exploded
        custom_start = ipaddress.IPv6Address(kwargs['start']).exploded
        increment_value = ipaddress.IPv6Address(kwargs['step']).exploded
    _result_ = rt_handle.invoke('multivalue_config',
                                multivalue_handle=multivalue_handle,
                                custom_start=custom_start,
                                custom_step=custom_step,)
    print(_result_)
    custom_1_handle = _result_['custom_handle']

    _result_ = rt_handle.invoke('multivalue_config',
                                custom_handle=custom_1_handle,
                                custom_increment_value=increment_value,
                                custom_increment_count=kwargs.get('count'),)
    print(_result_)
    return multivalue_handle


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
    mld_param = dict()
    mld_param['handle'] = kwargs.get('handle')
    mld_param['mode'] = kwargs.get('mode', 'create')
    mld_param['active'] = kwargs.get('active', '1')
    mld_param['filter_mode'] = kwargs.get('filter_mode', 'include')
    mld_param['enable_iptv'] = kwargs.get('iptv', '0')
    mld_param['mld_version'] = 'v' + str(kwargs.get('version', '1'))

    _result_ = rt_handle.invoke('emulation_mld_config', **mld_param)
    print(_result_)
    if _result_['status'] != '1':
        result['log'] = "failed to add mld client"
        result['status'] = '0'
        return result
    else:
        mld_handle = _result_['mld_host_handle']
        rt_handle.mld_handles[kwargs.get('handle')] = mld_handle
        rt_handle.mld_handle_to_group[mld_handle] = {}
        result['mld_host_handle'] = mld_handle

    addr_param = dict()
    addr_param['start'] = ipaddress.IPv6Address(kwargs.get('group_start_addr', 'ff03::1')).exploded
    addr_param['step'] = ipaddress.IPv6Address(kwargs.get('group_range_step', "0:0:0:0:0:0:1:0")).exploded
    addr_param['count'] = kwargs.get('group_range_length', "1")
    addr_param['type'] = 'v6'
    multivalue_2_handle = _add_addr_custom_pattern(rt_handle, **addr_param)
    mcast_args = dict()
    mcast_args['mode'] = "create"
    mcast_args['ip_addr_start'] = multivalue_2_handle
    mcast_args['ip_addr_step'] = ipaddress.IPv6Address(kwargs.get('group_step', "0:0:0:0:0:0:0:1")).exploded
    mcast_args['num_groups'] = kwargs.get('group_count', "1")
    mcast_args['active'] = kwargs.get('active', "1")
    _result_ = rt_handle.invoke('emulation_multicast_group_config', **mcast_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        return result
    else:
        mld_group_handle = _result_['multicast_group_handle']
        rt_handle.mld_handle_to_group[mld_handle]['group_handle'] = mld_group_handle

    src_addr_param = dict()
    src_addr_param['start'] = ipaddress.IPv6Address(kwargs.get('src_grp_start_addr', "200::1")).exploded
    src_addr_param['step'] = ipaddress.IPv6Address(kwargs.get('src_grp_range_step', "0:0:0:0:0:0:1:0")).exploded
    src_addr_param['count'] = kwargs.get('src_grp_range', "1")
    src_addr_param['type'] = 'v6'
    multivalue_3_handle = _add_addr_custom_pattern(rt_handle, **src_addr_param)
    src_args = dict()
    src_args['mode'] = "create"
    src_args['ip_addr_start'] = multivalue_3_handle
    src_args['ip_addr_step'] = ipaddress.IPv6Address(kwargs.get('src_grp_step', "0:0:0:0:0:0:0:1")).exploded
    src_args['num_sources'] = kwargs.get('src_grp_count', "1")
    src_args['active'] = "1"
    _result_ = rt_handle.invoke('emulation_multicast_source_config', **src_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        return result
    else:
        mld_source_handle = _result_['multicast_source_handle']
        rt_handle.mld_handle_to_group[mld_handle]['src_group_handle'] = mld_source_handle
    grp_args = dict()
    grp_args['mode'] = kwargs.get('mode', "create")
    grp_args['g_filter_mode'] = kwargs.get('filter_mode', "include")
    grp_args['group_pool_handle'] = mld_group_handle
    grp_args['no_of_grp_ranges'] = kwargs.get('group_range', "1")
    grp_args['no_of_src_ranges'] = kwargs.get('src_grp_range', "1")
    grp_args['session_handle'] = mld_handle
    grp_args['source_pool_handle'] = mld_source_handle
    _result_ = rt_handle.invoke('emulation_mld_group_config', **grp_args)
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        result['log'] = "failed to config the mld group and src group set"
    else:
        result['mld_group_handle'] = _result_['mld_group_handle']
        result['mld_source_handle'] = _result_['mld_source_handle']
        rt_handle.mld_handle_to_group[mld_handle]['mld_group_handle'] = _result_['mld_group_handle']
        rt_handle.mld_handle_to_group[mld_handle]['mld_source_handle'] = _result_['mld_source_handle']

    return result


def mld_client_action(rt_handle, **kwargs):
    """
    :param rt_handle:                                RT object
    :param kwargs:
    handle:                                     mld host handle
    action:                                     start/stop/join/leave/mld_send_specific_query
    start_group_addr:                           only used for mld_send_secific_query
    group_count:                                only used for mld_send_secific_query
    start_source_addr:                          only used for mld_send_secific_query
    source_count:                               only used for mld_send_secific_query
    :return:
    """
    action_param = dict()
    action_param['handle'] = kwargs['handle']
    if 'action' in kwargs:
        action_param['mode'] = kwargs['action']
    if 'start_group_addr' in kwargs:
        action_param['start_group_address'] = kwargs['start_group_addr']
    if 'group_count' in kwargs:
        action_param['group_count'] = kwargs['group_count']
    if 'start_source_addr' in kwargs:
        action_param['start_source_address'] = kwargs['start_source_addr']
    if 'source_count' in kwargs:
        action_param['source_count'] = kwargs['source_count']
    return rt_handle.invoke('emulation_mld_control', **action_param)


def add_application_traffic(rt_handle, **kwargs):
    """

    :param rt_handle:
    :param kwargs:
     type:                             ipv4/ipv6
     source:                           source handle
     destination:                      destination handle
     flow:                             application, e,g, "HTTP_302_Redirect"
     name:                             stream name
     per_ip_stats:                     1 or 0, default is 0

    :return:
    """
    app_args = dict()
    app_args['mode'] = kwargs.get('mode', 'create')
    app_args['objective_type'] = kwargs.get('objective_type', "users")
    app_args['objective_value'] = kwargs.get('objective_value', "100")
    app_args['objective_distribution'] = kwargs.get('objective_distribution', "apply_full_objective_to_each_port")
    app_args['enable_per_ip_stats'] = kwargs.get('per_ip_stats', "0")
    if 'name' in kwargs:
        app_args['name'] = kwargs['name']
    if 'source' in kwargs:
        app_args['emulation_src_handle'] = kwargs['source']
    if 'destination' in kwargs:
        app_args['emulation_dst_handle'] = kwargs['destination']

    if 'flows' in kwargs:
        app_args['flows'] = kwargs['flows']

    if 'type' in kwargs:
        if 'v4' in kwargs['type']:
            app_args['circuit_endpoint_type'] = "ipv4_application_traffic"
        if 'v6' in kwargs['type']:
            app_args['circuit_endpoint_type'] = "ipv6_application_traffic"
    result = rt_handle.invoke('traffic_l47_config', **app_args)
    return result


def add_isis(rt_handle, **kwargs):
    """Add ISIS emulation

    :param rt_handle:
    :param kwargs:
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

    :return: result dictionary with keys status and bbe_isis_handle
    """
    t.log("ixixtester.add_isis to configure ISIS on {}".format(rt_handle))
    eth_handle = kwargs['handle']  # e.g. '/topology:2/deviceGroup:1/ethernet:1'
    # Obtain topology handle from eth handle
    match = re.match(r'\/topology:\d+', eth_handle)
    topology_handle = match.group(0)  # e.g, '/topology:2'
    # Obtain device group handle from eth handle
    match = re.match(r'\/topology:\d+\/deviceGroup:\d+', eth_handle)
    devicegroup_handle = match.group(0)

    result = dict()
    result['status'] = '1'

    # Create multivalues
    mvp6 = dict()
    mvp6['pattern'] = "counter"
    mvp6['counter_start'] = "9001"
    mvp6['counter_step'] = "1"
    mvp6['counter_direction'] = "increment"
    mvp6['nest_step'] = '{}'.format(("0"))
    mvp6['nest_owner'] = '{}'.format(topology_handle)
    mvp6['nest_enabled'] = '{}'.format("1")
    _result6 = rt_handle.invoke('multivalue_config', **mvp6)
    multivalue_6_handle = _result6['multivalue_handle']

    mvp7 = dict()
    mvp7['pattern'] = "counter"
    mvp7['counter_start'] = "1.1.1.1"
    mvp7['counter_step'] = "0.0.0.1"
    mvp7['counter_direction'] = "increment"
    mvp7['nest_step'] = '{}'.format(("0.1.0.0"))
    mvp7['nest_owner'] = '{}'.format(topology_handle)
    mvp7['nest_enabled'] = '{}'.format("1")
    _result7 = rt_handle.invoke('multivalue_config', **mvp7)
    multivalue_7_handle = _result7['multivalue_handle']

    mvp8 = dict()
    mvp8['pattern'] = "counter"
    mvp8['counter_start'] = "1.1.1.1"
    mvp8['counter_step'] = "0.0.0.1"
    mvp8['counter_direction'] = "increment"
    mvp8['nest_step'] = '{}'.format(("0.1.0.0"))
    mvp8['nest_owner'] = '{}'.format(topology_handle)
    mvp8['nest_enabled'] = '{}'.format("1")
    _result8 = rt_handle.invoke('multivalue_config', **mvp8)
    multivalue_8_handle = _result8['multivalue_handle']

    mvp9 = dict()
    mvp9['pattern'] = "counter"
    mvp9['counter_start'] = "0"
    mvp9['counter_step'] = "1"
    mvp9['counter_direction'] = "increment"
    mvp9['nest_step'] = '{}'.format(("0"))
    mvp9['nest_owner'] = '{}'.format(topology_handle)
    mvp9['nest_enabled'] = '{}'.format("1")
    _result9 = rt_handle.invoke('multivalue_config', **mvp9)
    multivalue_9_handle = _result9['multivalue_handle']

    mvp10 = dict()
    mvp10['pattern'] = "counter"
    mvp10['counter_start'] = "64:01:00:01:00:00"
    mvp10['counter_step'] = "00:00:00:01:00:00"
    mvp10['counter_direction'] = "increment"
    mvp10['nest_step'] = '{}'.format(("00:01:00:00:00:00"))
    mvp10['nest_owner'] = '{}'.format(topology_handle)
    mvp10['nest_enabled'] = '{}'.format("1")
    _result10 = rt_handle.invoke('multivalue_config', **mvp10)
    multivalue_10_handle = _result10['multivalue_handle']

    # args for emulation_isis_config
    isis_p = dict()
    isis_p['mode'] = 'create'
    isis_p['handle'] = eth_handle
    if 'auth_type' in kwargs:
        isis_p['auth_type'] = kwargs['auth_type']
        isis_p['area_authentication_mode'] = kwargs['auth_type']
        isis_p['domain_authentication_mode'] = kwargs['auth_type']
    if 'auth_key' in kwargs:
        isis_p['area_password'] = kwargs['auth_key']
        isis_p['domain_password'] = kwargs['auth_key']
        isis_p['circuit_tranmit_password_md5_key'] = 'bharti'
    if 'intf_type' in kwargs:
        isis_p['intf_type'] = kwargs['intf_type']
    isis_p['interface_adj_sid'] = multivalue_6_handle
    isis_p['router_id'] = multivalue_7_handle
    isis_p['node_prefix'] = multivalue_8_handle
    isis_p['sid_index_label'] = multivalue_9_handle
    isis_p['system_id'] = multivalue_10_handle
    isis_p['start_sid_label'] = '{}'.format("16000")
    isis_p['sid_count'] = '{}'.format("8000")
    isis_p['routing_level'] = 'L2'
    isis_p['area_id'] = "00000000000000000000490001"
    isis_p['interface_v_flag'] = '1'
    isis_p['interface_l_flag'] = '1'
    isis_p['discard_lsp'] = "0"
    isis_p['wide_metrics'] = "1"
    isis_p['max_area_addresses'] = "20"
    isis_p['ignore_receive_md5'] = "0"
    isis_p['pdu_per_burst'] = "10"
    isis_p['n_flag'] = "1"

    # Invoke RT to add ISIS emulation
    _result = rt_handle.invoke('emulation_isis_config', **isis_p)
    if _result['status'] == '1':
        bbe_isis_handle = _result['isis_l3_handle']
        rt_handle.bbe_isis_handle.append(bbe_isis_handle)
        result['bbe_isis_handle'] = bbe_isis_handle
        t.log("ixixtester.add_isis successfully invoked emulation_isis_config")
        t.log("ixixtester.add_isis stored isis_l3_handle under rt_handle as bbe_isis_handle")
    else:
        return _result

    # add network group for prefix
    prefix_p = dict()
    prefix_p['protocol_handle'] = devicegroup_handle
    prefix_p['multiplier'] = kwargs.get('multiplier', '1')
    prefix_p['enable_device'] = "1"
    prefix_p['connected_to_handle'] = bbe_isis_handle
    prefix_p['type'] = kwargs.get('prefix_type', "ipv4-prefix")
    prefix_p['ipv4_prefix_network_address'] = kwargs.get('ipv4_prefix_network_address', "101.0.0.0")
    prefix_p['ipv4_prefix_network_address_step'] = kwargs.get('ipv4_prefix_network_address_step', "1.0.0.0")
    prefix_p['ipv4_prefix_length'] = kwargs.get('ipv4_prefix_length', "24")
    prefix_p['ipv4_prefix_address_step'] = kwargs.get('ipv4_prefix_address_step', "1")
    prefix_p['ipv4_prefix_number_of_addresses'] = kwargs.get('ipv4_prefix_number_of_addresses', "1000")

    # Create network group
    _result1 = rt_handle.invoke('network_group_config', **prefix_p)
    if _result1['status'] == '1':
        network_group_3_handle = _result1['network_group_handle']
        t.log("ixixtester.add_isis successfully invoked network_group_config to add ISIS prefix")
    else:
        return _result1

    # Create multivalue args
    mvp = dict()
    mvp['pattern'] = "counter"
    mvp['counter_start'] = "1"
    mvp['counter_step'] = "1"
    mvp['counter_direction'] = "increment"
    mvp['nest_step'] = '{},{}'.format("1", "0")
    mvp['nest_owner'] = '{},{}'.format(devicegroup_handle, topology_handle)
    mvp['nest_enabled'] = '{},{}'.format("0", "1")
    _result2 = rt_handle.invoke('multivalue_config', **mvp)
    if _result2['status'] == '1':
        multivalue_16_handle = _result2['multivalue_handle']
    else:
        return _result2

    # isis_network_group_config
    isis_p1 = dict()
    isis_p1['handle'] = network_group_3_handle
    isis_p1['mode'] = 'modify'
    isis_p1['routerange_ipv4_sid_index_label'] = multivalue_16_handle
    _result3 = rt_handle.invoke('emulation_isis_network_group_config', **isis_p1)
    if _result3['status'] != '1':
        return _result3

    t.log("ixixtester.add_isis successfully configured ISIS")
    return result


def add_bgp(rt_handle, **kwargs):
    """

    :param rt_handle:
    :param kwargs:
    handle:                     ipv4 handle or ipv6 handle
    type:                       external/internal
    remote_ip:                  neighbor ip address
    local_as:                   Local as number
    hold_time:                  bgp hold time
    restart_time:               bgp restart time
    keepalive:                  bgp keepalive timer
    router_id:                  bgp router id
    stale_time:                 bgp stale time
    enable_flap:                bgp flap enable 1/0
    flap_down_time:             flap down time
    flap_up_time:               flap up time
    graceful_restart:           graceful restart 1/0
    prefix_group:               list of prefixes which was a dictionary include
                                network_prefix:             bgp network prefix
                                network_step:               bgp network prefix increment step
                                network_count:              bgp network counter
                                sub_prefix_length:      network sub prefix length
                                sub_prefix_count:       network sub prefix count

    :return:                    result dictionary: status, bgp_handle, network_group_handle,
    """
    result = dict()
    result['status'] = '1'
    result['network_group_handle'] = []
    bgp_params = dict()
    bgp_params['mode'] = 'enable'
    bgp_params['handle'] = kwargs['handle']
    match = re.match(r'\/topology:\d+\/deviceGroup:\d+', kwargs['handle'])
    devicegroup_handle = match.group(0)
    bgp_params['neighbor_type'] = kwargs['type']
    bgp_params['local_as'] = kwargs['local_as']
    if 'hold_time' in kwargs:
        bgp_params['hold_time'] = kwargs['hold_time']
    if 'restart_time' in kwargs:
        bgp_params['restart_time'] = kwargs['restart_time']
    if 'keepalive' in kwargs:
        bgp_params['keepalive_timer'] = kwargs['keepalive']
    if 'enable_flap' in kwargs:
        bgp_params['enable_flap'] = kwargs['enable_flap']
        bgp_params['flap_up_time'] = kwargs['flap_up_time']
        bgp_params['flap_down_time'] = kwargs['flap_down_time']
    if 'stale_time' in kwargs:
        bgp_params['stale_time'] = kwargs['stale_time']
    if 'graceful_restart' in kwargs:
        bgp_params['graceful_restart_enable'] = kwargs['graceful_restart']

    if 'v4' in kwargs['handle']:
        bgp_params['ip_version'] = '4'
        bgp_params['remote_ip_addr'] = kwargs['remote_ip']
        if 'router_id' in kwargs:
            bgp_params['router_id'] = kwargs['router_id']
    if 'v6' in kwargs['handle']:
        bgp_params['ip_version'] = '6'
        bgp_params['remote_ipv6_addr'] = kwargs['remote_ip']

    _result_ = rt_handle.invoke('emulation_bgp_config', **bgp_params)
    if _result_['status'] == '1':
        bgp_handle = _result_['bgp_handle']
        rt_handle.bgp_handle.append(bgp_handle)
        result['bgp_handle'] = bgp_handle
    else:
        return _result_
    for prefix in kwargs['prefix_group']:

        _result_ = rt_handle.invoke('multivalue_config',
                                    pattern="counter",
                                    counter_start=prefix['network_prefix'],
                                    counter_step=prefix['network_step'],
                                    counter_direction="increment",)
        multivalue_11_handle = _result_['multivalue_handle']

        network_params = dict()
        network_params['protocol_handle'] = devicegroup_handle
        if 'network_count' in prefix:
            network_params['multiplier'] = prefix['network_count']
        network_params['connected_to_handle'] = bgp_handle
        if 'v4' in kwargs['handle']:
            network_params['type'] = "ipv4-prefix"
            network_params['ipv4_prefix_network_address'] = multivalue_11_handle
            network_params['ipv4_prefix_length'] = prefix['sub_prefix_length']
            if 'sub_prefix_count' in prefix:
                network_params['ipv4_prefix_number_of_addresses'] = prefix['sub_prefix_count']
        if 'v6' in kwargs['handle']:
            network_params['type'] = "ipv6-prefix"
            network_params['ipv6_prefix_network_address'] = multivalue_11_handle
            network_params['ipv6_prefix_length'] = prefix['sub_prefix_length']
            if 'sub_prefix_count' in prefix:
                network_params['ipv6_prefix_number_of_addresses'] = prefix['sub_prefix_count']

        _result_ = rt_handle.invoke('network_group_config', **network_params)
        if _result_['status'] == '1':
            network_group_handle = _result_['network_group_handle']
            result['network_group_handle'].append(network_group_handle)
        else:
            return _result_
        route_params = dict()
        if 'ipv4_prefix_pools_handle' in _result_:
            prefix_pool_handle = _result_['ipv4_prefix_pools_handle']
            route_params['ip_version'] = '4'
            route_params["ipv4_unicast_nlri"] = "1"
        if 'ipv6_prefix_pools_handle' in _result_:
            prefix_pool_handle = _result_['ipv6_prefix_pools_handle']
            route_params['ip_version'] = '6'
            route_params["ipv6_unicast_nlri"] = "1"
        route_params['handle'] = network_group_handle
        route_params['mode'] = 'create'
        route_params['prefix'] = multivalue_11_handle
        route_params['num_routes'] = prefix.get('sub_prefix_count', '1')
        route_params['prefix_from'] = prefix['sub_prefix_length']
        route_params['max_route_ranges'] = prefix.get('network_count', '1')

        _result_ = rt_handle.invoke('emulation_bgp_route_config', **route_params)
        if _result_['status'] != '1':
            result['status'] = '0'
    return result


def bgp_action(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    handle:                                 bgp session handle
    action:                                 start/stop/restart/abort/restart_down/delete
    :return:
    """
    bgp_params = dict()
    bgp_params['mode'] = kwargs['action']
    bgp_params['handle'] = kwargs['handle']
    if 'delete' in kwargs['action']:
        match = re.match(r'\/topology:\d+\/deviceGroup:\d+', kwargs['handle'])
        devicegroup_handle = match.group(0)
        rt_handle.invoke('test_control', handle=devicegroup_handle, action='stop_protocol')
        return rt_handle.invoke('emulation_bgp_config', handle=kwargs['handle'], mode='delete')

    return rt_handle.invoke('emulation_bgp_control', **kwargs)


def add_l2tp_server(rt_handle, **kwargs):
    """
    rt_handle.invoke('l2tp_config(mode='lns',port_handle='1/1/3',lns_host_name='ixia_lns',
    tun_auth='authenticate_hostname', secret='ixia', hostname='lac', l2_encap='ethernet_ii_vlan',
    l2tp_dst_addr='10.2.0.2', l2tp_src_addr='10.2.0.1', num_tunnels=1,auth_mode='pap_or_chap',
    username='test', password='pwd', l2tp_src_prefix_len=24)
    :param rt_handle:                                            RT object
    :param kwargs:
    port:                                port
    handle:                             ipv4 handle
    tun_auth_enable:                    1 or 0, authentication method for tunnel('authenticate_hostname'/
                                        tunnel_authentication_disabled), default is 1
    tun_secret:                         tunnel secret
    tun_hello_req:                      send tunnel hello request , value could be 1/0
    l2tp_dst_addr:                      l2tp destionation start address(mandatory)
    l2tp_src_addr:                      l2tp source start address(mandatory)
    netmask:                            ip address netmask
    hostname:                           lac hostname, default is 'lac'
    lns_host_name:                      lns hostname, default is 'ixia_lns'
    tun_hello_req:                      send tunnel hello request , value could be 1/0
    l2tp_src_prefix_len:                l2tp source prefix length, default is 24
    auth_mode:                          authentication mode, none/pap/chap/pap_or_chap, default is none
    username:                           username for authentication
    password:                           password for authentication
    ip_cp:                              ip_cp mode, could be ipv4_cp/ipv6_cp/dual_stack, default is ipv4_cp
    vlan_id:                            interface vlan id
    lease_time                             pool address lease time
    dhcpv6_ia_type:                        v6 IA type "iana, iapd"
    pool_prefix_start:                     v6 PD start prefix
    pool_prefix_length:                    v6 prefix length
    pool_prefix_size:                      v6 prefix pool size
    :return:
    """

    lns_params = dict()
    link_args = dict()
    lns_params['mode'] = 'lns'
    lns_params['num_tunnels'] = '1'
    lns_params['hostname'] = kwargs.get('hostname', 'mx_lac')
    lns_params['lns_host_name'] = kwargs.get('lns_host_name', 'ixia_lns')
    #lns_params['vlan_id'] = kwargs.get('vlan_id', '1')
    #lns_params['l2_encap'] = 'ethernet_ii_vlan'
    if 'handle' in kwargs:
        lns_params['handle'] = kwargs['handle']
    if 'port' in kwargs:
        port = kwargs['port']
        link_args['port'] = port
        link_args['ip_addr'] = kwargs['l2tp_dst_addr']
        link_args['gateway'] = kwargs['l2tp_src_addr']
        link_args['netmask'] = kwargs['netmask']
        if 'vlan_id' in kwargs:
            link_args['vlan_start'] = kwargs['vlan_id']
        _result_ = add_link(rt_handle, **link_args)
        if _result_['status'] == '0':
            raise Exception("failed to add ip address for lns")
        ipv4_handle = _result_['ipv4_handle']
        ethernet_handle = _result_['ethernet_handle']
        lns_params['handle'] = ipv4_handle

    # if port not in rt_handle.handles:
    #     _result_ = add_topology(rt_handle, port_list=[port])
    # if rt_handle.ae and port in rt_handle.ae:
    #     device_handle = rt_handle.handles[port]['device_group_handle'][0]
    #     lns_params['handle'] = device_handle
    # else:
    #     lns_params['port_handle'] = rt_handle.port_to_handle_map[kwargs['port']]
    # lns_params['l2tp_src_addr'] = kwargs['l2tp_src_addr']
    # lns_params['l2tp_dst_addr'] = kwargs['l2tp_dst_addr']
    if int(kwargs.get('tun_auth_enable', '1')):
        lns_params['tun_auth'] = 'authenticate_hostname'
    else:
        lns_params['tun_auth'] = 'tunnel_authentication_disabled'
    lns_params['secret'] = kwargs.get('tun_secret', 'secret')
    #lns_params['l2tp_src_prefix_len'] = kwargs.get('l2tp_src_prefix_len', '24')
    lns_params['sessions_per_tunnel'] = kwargs.get('total_sessions', '32000')
    if 'tun_hello_req' in kwargs:
        lns_params['hello_req'] = kwargs['tun_hello_req']
    if 'tun_hello_interval' in kwargs:
        lns_params['hello_interval'] = kwargs['tun_hello_interval']
    if 'username' in kwargs:
        lns_params['username'] = kwargs['username']
    if 'password' in kwargs:
        lns_params['password'] = kwargs['password']
    # if 'ip_cp' in kwargs:
    #     lns_params['ip_cp'] = kwargs['ip_cp']
    #     if 'dual' in kwargs['ip_cp'] or 'v6' in kwargs['ip_cp']:
    #         lns_params['dhcpv6_hosts_enable'] = '1'
    lns_params['auth_mode'] = kwargs.get('auth_mode', 'pap_or_chap')
    result = rt_handle.invoke('l2tp_config', **lns_params)
    if result['status'] == "1":
        rt_handle.lns_handle.append(result['lns_handle'])
        rt_handle.l2tp_server_session_handle.append(result['pppox_server_sessions_handle'])
        pppox_server_handle = result['pppox_server_handle']
        if 'dhcpv6_server_handle' in result:
            rt_handle.dhcpv6_server_handle.append(result['dhcpv6_server_handle'])
    ##add dhcpv6 server if necessary
    if 'ip_cp' in kwargs:
        if 'dual' in kwargs['ip_cp'] or 'v6' in kwargs['ip_cp']:
            kwargs['handle'] = pppox_server_handle
            config = add_dhcp_server(rt_handle, **kwargs)
            if config['status'] == '0':
                result['status'] = '0'
            result['dhcpv6_server_handle'] = config['dhcpv6_server_handle']
    return result


def l2tp_server_action(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    handle:                     lns handle
    action:                     start/stop
    :return:
    """
    param = dict()
    match = re.match(r'\/topology:\d+\/deviceGroup:\d+', kwargs['handle'])
    param['handle'] = match.group(0)
    param['action'] = kwargs['action']
    return rt_handle.invoke('test_control', **param)


def add_l2tp_client(rt_handle, **kwargs):
    """
    maximum sessions per port is 32000
    :param rt_handle:                        RT Object from toby
    :param kwargs:
    port                                tester port(mandatory)
    num_tunnels_per_lac:                number of tunnels configured per LAC
    sessions_per_tunnel:                sessions per LAC, default is 5
    tun_auth_enable:                    1 or 0,       authentication method for tunnel('authenticate_hostname'/
                                        tunnel_authentication_disabled), default is 1
    tun_secret:                         tunnel secret
    tun_hello_req:                      send tunnel hello request , value could be 1/0
    tun_hello_interval:                 tunnel hello interval, valid only when tun_hello_req is 1
    echo_req:                           enable/disable ppp keepalive request by RT
    echo_req_interval:                  ppp keepalive request interval
    l2tp_dst_addr:                      l2tp destionation start address, default is '100.0.0.1'
    l2tp_src_addr:                      l2tp source start address(mandatory)
    hostname:                           lac hostname, default is 'lac'
    l2tp_src_count:                     l2tp source address counts(same as lac count), default is 1
    l2tp_src_step:                      l2tp source address step, default is 0.0.1.0
    l2tp_src_gw:                        l2tp source gateway(mandatory)
    l2tp_src_gw_step:                   l2tp source gateway step, default is 0.0.1.0
    l2tp_src_prefix_len:                l2tp source prefix length, default is 24
    l2tp_dst_step:                      l2tp destintion address step
    vlan_id:                            start vlan id for the connection, default is 1
    vlan_id_step:                       vlan id step, default is 1
    auth_mode:                          authentication mode, none/pap/chap/pap_or_chap, default is none
    username:                           username for authentication
    password:                           password for authentication
    ip_cp:                              ip_cp mode, could be ipv4_cp/ipv6_cp/dual_stack, default is ipv4_cp
    dhcpv6_ia_type:                     can be iana/iapd/iana_iapd, default is iapd
    #domain_name:                        domain name, (eg. if you set this to abc?.com, the domain name will increase
                                        from 1, and repeat sessions_per_tunnel)
    :return:                            dictionary of status , ethernet_handle, ipv4_handle, lac_handle,
                                        pppox_client_handle, dhcpv6_client_handle
    """
    lac_params = dict()
    lac_params['mode'] = 'lac'
    # lac_params['vlan_id'] = kwargs.get('vlan_id', '1')
    # lac_params['vlan_id_step'] = kwargs.get('vlan_id_step', '1')
    #lac_params['l2_encap'] = 'ethernet_ii_vlan'
    #lac_params['port_handle'] = rt_handle.port_to_handle_map[kwargs['port']]
    # port = kwargs['port']
    # if port not in rt_handle.handles:
    #     _result_ = add_topology(rt_handle, port_list=[port])
    if 'port' in kwargs:
        port = kwargs['port']
        link_args = dict()
        if port not in rt_handle.handles:
            _result_ = add_topology(rt_handle, port_list=[port])
        link_args['port'] = port
        link_args['ip_addr'] = kwargs['l2tp_src_addr']
        link_args['ip_addr_step'] = kwargs.get('l2tp_src_step', '0.0.1.0')
        link_args['gateway'] = kwargs['l2tp_src_gw']
        v4addr = ipaddress.IPv4Interface('0.0.0.0/' + str(kwargs.get('l2tp_src_prefix_len', '24')))
        link_args['netmask'] = str(v4addr.netmask)
        link_args['count'] = kwargs.get('l2tp_src_count', '1')
        if 'vlan_id' in kwargs:
            link_args['vlan_start'] = kwargs['vlan_id']
        if 'vlan_id_step' in kwargs:
            link_args['vlan_step'] = kwargs['vlan_id_step']
        _result_ = add_link(rt_handle, **link_args)
        if _result_['status'] == '0':
            raise Exception("failed to add ip address for lns")
        ipv4_handle = _result_['ipv4_handle']
        ethernet_handle = _result_['ethernet_handle']
        lac_params['handle'] = ipv4_handle
    # if rt_handle.ae and port in rt_handle.ae:
    #     device_handle = rt_handle.handles[port]['device_group_handle'][0]
    #     lac_params['handle'] = device_handle
    # else:
    #     lac_params['port_handle'] = rt_handle.port_to_handle_map[kwargs['port']]
    if int(kwargs.get('tun_auth_enable', '1')):
        lac_params['tun_auth'] = 'authenticate_hostname'
    else:
        lac_params['tun_auth'] = 'tunnel_authentication_disabled'
    if 'tun_secret' in kwargs:
        lac_params['secret'] = kwargs['tun_secret']
    lac_params['num_tunnels'] = kwargs.get('num_tunnels_per_lac', '1')
    lac_params['sessions_per_tunnel'] = kwargs.get('sessions_per_tunnel', '5')
    lac_params['l2tp_dst_addr'] = kwargs.get('l2tp_dst_addr', '100.0.0.1')
    if 'l2tp_dst_step' in kwargs:
        lac_params['l2tp_dst_step'] = kwargs['l2tp_dst_step']
    if 'l2tp_dst_count' in kwargs:
        lac_params['l2tp_dst_count'] = kwargs['l2tp_dst_count']
#    lac_params['l2tp_src_addr'] = kwargs['l2tp_src_addr']
#   lac_params['l2tp_src_gw'] = kwargs['l2tp_src_gw']
#    lac_params['l2tp_src_count'] = kwargs.get('l2tp_src_count', '1')
#    lac_params['l2tp_src_step'] = kwargs.get('l2tp_src_step', '0.0.1.0')
#    lac_params['l2tp_src_gw_step'] = kwargs.get('l2tp_src_gw_step', lac_params['l2tp_src_step'])
#    lac_params['l2tp_src_prefix_len'] = kwargs.get('l2tp_src_prefix_len', '24')
    lac_params['hostname'] = kwargs.get('hostname', 'lac')
    if 'echo_req' in kwargs:
        lac_params['echo_req'] = kwargs['echo_req']
        if 'echo_req_interval' in kwargs:
            lac_params['echo_req_interval'] = kwargs['echo_req_interval']
    if 'mode' in kwargs:
        lac_params['action'] = kwargs['mode']
    #lac_params['tun_distribution'] = kwargs.get('tun_distribution', 'next_tunnelfill_tunnel')
    if 'tun_hello_req' in kwargs:
        lac_params['hello_req'] = kwargs['tun_hello_req']
        if 'tun_hello_interval' in kwargs:
            lac_params['hello_interval'] = kwargs['tun_hello_interval']
    if 'l2tp_dst_step' in kwargs:
        lac_params['l2tp_dst_step'] = kwargs['l2tp_dst_step']
    if 'ip_cp' in kwargs:
        lac_params['ip_cp'] = kwargs['ip_cp']
    #     if 'ipv6' in kwargs['ip_cp'] or 'dual' in kwargs['ip_cp']:
    #         lac_params['dhcpv6_hosts_enable'] = '1'
    #         lac_params['dhcp6_pd_client_range_ia_type'] = kwargs.get('dhcpv6_ia_type', 'iapd')

    lac_params['auth_mode'] = kwargs.get('auth_mode', 'none')
    if 'auth_mode' in kwargs:
        lac_params['auth_mode'] = kwargs['auth_mode']
        if 'username' in kwargs:
            lac_params['username'] = kwargs['username']
            if '?' in lac_params['username']:
                increment = '{Inc:' + '1,,,' + str(lac_params['sessions_per_tunnel']) + '}'
                lac_params['username'] = kwargs['username'].replace('?', increment)

        if 'chap' in kwargs['auth_mode'].lower():
            if 'username' in kwargs:
                lac_params['chap_name'] = lac_params['username']
            if 'password' in kwargs:
                lac_params['chap_secret'] = kwargs['password']

    if 'password' in kwargs:
        lac_params['password'] = kwargs['password']

    if int(kwargs.get('l2tp_src_count', '1')) > 1:
        ##increase the lac hostname
        lac_params['hostname'] = lac_params['hostname'] + '{Inc:1,,,' + str(lac_params['num_tunnels']) + '}'
        _result_ = rt_handle.invoke('multivalue_config',
                                    pattern="counter",
                                    counter_start="1701",
                                    counter_step="1",
                                    counter_direction="increment")
        lac_params['udp_src_port'] = _result_['multivalue_handle']

    result = rt_handle.invoke('l2tp_config', **lac_params)
    if result['status'] == '1':
        rt_handle.lac_handle.append(result['lac_handle'])
        if 'dhcpv6_client_handle' in result:
            rt_handle.dhcpv6_client_handle.append(result['dhcpv6_client_handle'])
            rt_handle.l2tp_client_handle.append(result['dhcpv6_client_handle'])
        else:
            rt_handle.l2tp_client_handle.append(result['pppox_client_handle'])
        rt_handle.pppox_client_handle.append(result['pppox_client_handle'])
    if 'ip_cp' in kwargs:
        if 'ipv6' in kwargs['ip_cp'] or 'dual' in kwargs['ip_cp']:
            dhcp_args = dict()
            dhcp_args['handle'] = result['pppox_client_handle']
            if 'dhcpv6_ia_type' in kwargs:
                dhcp_args['dhcp6_range_ia_type'] = kwargs.get('dhcpv6_ia_type')

            if 'rapid_commit' in kwargs:
                dhcp_args['use_rapid_commit'] = kwargs.get('rapid_commit')

            if 'dhcp4_broadcast' in kwargs:
                dhcp_args['dhcp4_broadcast'] = kwargs.get('dhcp4_broadcast')

            if 'v6_max_no_per_client' in kwargs:
                dhcp_args['dhcp6_range_max_no_per_client'] = kwargs.get('v6_max_no_per_client')

            if 'dhcpv6_iana_count' in kwargs:
                dhcp_args['dhcp6_range_iana_count'] = kwargs.get('dhcpv6_iana_count')

            if 'dhcpv6_iapd_count' in kwargs:
                dhcp_args['dhcp6_range_iapd_count'] = kwargs.get('dhcpv6_iapd_count')
            dhcp_args['dhcp_range_ip_type'] = 'ipv6'
            config_status = rt_handle.invoke('emulation_dhcp_group_config', **dhcp_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcpv6 client over l2tp")
            else:
                result['dhcpv6_client_handle'] = config_status['dhcpv6client_handle']
                rt_handle.dhcpv6_client_handle.append(result['dhcpv6_client_handle'])
                rt_handle.l2tp_client_handle.append(result['dhcpv6_client_handle'])
    return result


def l2tp_client_action(rt_handle, **kwargs):
    """
    :param rt_handle:                            RT object
    :param kwargs:
    handle:                                 l2tp client handle(pppox client handle/dhcpv6 client handle)
    action:                                 start/stop/abort/restart_down
    :return:                                status dictionary
    """
    param = dict()
    match = re.match(r'\/topology:\d+\/deviceGroup:\d+\/deviceGroup:\d+', kwargs['handle'])
    print(match)
    param['handle'] = match.group(0)
    if 'restart' in kwargs['action']:
        param['action'] = 'restart_down'
    elif 'start' in kwargs['action']:
        param['action'] = 'start_protocol'
    elif 'stop' in kwargs['action']:
        param['action'] = 'stop_protocol'
    elif 'abort' in kwargs['action']:
        param['action'] = 'abort_protocol'
    return rt_handle.invoke('test_control', **param)



def client_action(rt_handle, **kwargs):
    """
    :param rt_handle:                            RT object
    :param kwargs:
    handle:                                 client handle(pppox client handle/dhcp client handle)
    action:                                 start/stop/abort/restart_down
    :return:                                status dictionary
    """
    param = dict()
    match = re.match(r'.*deviceGroup:\d+', kwargs['handle'])
    print(match)
    stack = kwargs.get('stack', 'all')
    if stack == 'dhcpv6':
        param['handle'] = kwargs['handle']
    else:
        param['handle'] = match.group(0)
    if 'restart' in kwargs['action']:
        param['action'] = 'restart_down'
    elif 'start' in kwargs['action']:
        param['action'] = 'start_protocol'
    elif 'stop' in kwargs['action']:
        param['action'] = 'stop_protocol'
    elif 'abort' in kwargs['action']:
        param['action'] = 'abort_protocol'
    return rt_handle.invoke('test_control', **param)


def l2tp_client_stats(rt_handle, **kwargs):
    """

    :param rt_handle:
    :param kwargs:
    handle:                             l2tp client handle/ pppox client handle/ dhcpv6 client handle
    mode:                               aggregate/session/tunnel/session_all/session_dhcpv6pd
    :return:
    """
    if 'lac' in kwargs['handle']:
        return rt_handle.invoke('l2tp_stats', **kwargs)
    elif 'dhcpv6' in kwargs['handle']:
        return rt_handle.invoke('dhcp_client_stats', handle=kwargs['handle'], mode='aggregate_stats')
    elif 'pppox' in kwargs['handle']:
        return rt_handle.invoke('pppoe_client_stats', **kwargs)


def add_dhcp_server(rt_handle, **kwargs):
    """
    :param rt_handle                       RT object
    :param kwargs:
    handle:                                ipv4 handle or ipv6 handle or pppox server handle
    pool_size:                             server pool size
    pool_start_addr:                       pool start address
    pool_step:                             pool step for more than one pools
    pool_mask_length:                      pool prefix length
    pool_gateway:                          pool gateway address
    pool_gateway_step:                     pool gateway address step for more than one gateways
    lease_time                             pool address lease time
    dhcpv6_ia_type:                        v6 IA type "iana, iapd, iana+iapd"
    pool_prefix_start:                     v6 PD start prefix
    pool_prefix_length:                    v6 prefix length
    pool_prefix_size:                      v6 prefix pool size
    multi_servers_config_v4                None or a dict of key/values for v4 multi-servers config
    multi_servers_config_v6                None or a dict of key/values for v6 multi-servers config

    # use_rapid_commit                       = "0",
    # subnet_addr_assign                     = "0",
    # subnet                                 = "relay",

    :param kwargs:
    :return:
    a dictionary of status dhcpv4_server_handle dhcpv6_server_handle
    """
    result = dict()
    result['status'] = '1'
    if 'handle' not in kwargs:
        raise Exception("ip handle must be provided ")
    dhcp_args = dict()
    dhcp_args['handle'] = kwargs['handle']
    dhcp_args['mode'] = 'create'
    if 'lease_time' in kwargs:
        dhcp_args['lease_time'] = kwargs['lease_time']
    if 'pool_start_addr' in kwargs:
        dhcp_args['ipaddress_pool'] = kwargs['pool_start_addr']
    if 'pool_step' in kwargs and kwargs['pool_step'] is not None:
        dhcp_args['ipaddress_pool_inside_step'] = kwargs['pool_step']
    if 'pool_mask_length' in kwargs:
        dhcp_args['ipaddress_pool_prefix_length'] = kwargs['pool_mask_length']
        dhcp_args['ipaddress_pool_prefix_inside_step'] = 0
    if 'pool_size' in kwargs:
        dhcp_args['ipaddress_count'] = kwargs['pool_size']
    if 'pool_gateway' in kwargs:
        dhcp_args['dhcp_offer_router_address'] = kwargs['pool_gateway']
    if 'v4' in kwargs['handle']:
        dhcp_args['ip_version'] = '4'

    # for multiple dhcp servers want customized pool addresses
    if 'multi_servers_config_v4' in kwargs and kwargs['multi_servers_config_v4'] is not None:
        msc = kwargs['multi_servers_config_v4']
        t.log('info', 'dhcpv4 multi servers config: {}'.format(msc))
        match = re.match(r'\/topology:\d+', kwargs['handle'])
        arg_topology_handle = match.group(0)

        dhcp_args['dhcp_offer_router_address_inside_step'] = msc['pool_gateway_inside_step']
        dhcp_args['ipaddress_pool_inside_step'] = msc['pool_inside_step']

        if msc['pool_gateways'] is not None:
            arg_pool_gw_len = len(msc['pool_gateways'].split(','))
            arg_pool_gw_overlay_index = ','.join(str(x+1) for x in range(arg_pool_gw_len))
            arg_pool_gw_overlay_index_step = ','.join('0' for _ in range(arg_pool_gw_len))
            arg_pool_gw_overlay_count = ','.join('1' for _ in range(arg_pool_gw_len))

            mv_args = dict()
            mv_args['pattern'] = "counter"
            mv_args['counter_start'] = kwargs['pool_gateway']
            mv_args['counter_step'] = msc['pool_inside_step']
            mv_args['nest_owner'] = arg_topology_handle
            mv_args['nest_enabled'] = '0'
            mv_args['overlay_value'] = msc['pool_gateways']
            mv_args['overlay_index'] = arg_pool_gw_overlay_index
            mv_args['overlay_index_step'] = arg_pool_gw_overlay_index_step
            mv_args['overlay_count'] = arg_pool_gw_overlay_count
            t.log('info','dhcp server dhcp_offer_router_address mv_args')
            t.log('info', mv_args)
            _result_ = rt_handle.invoke('multivalue_config', **mv_args)
            dhcp_args['dhcp_offer_router_address'] = _result_['multivalue_handle']

        if msc['lease_times'] is not None:
            arg_pool_lt_len = len(msc['lease_times'].split(','))
            arg_pool_lt_overlay_index = ','.join(str(x+1) for x in range(arg_pool_lt_len))
            arg_pool_lt_overlay_index_step = ','.join('0' for _ in range(arg_pool_lt_len))
            arg_pool_lt_overlay_count = ','.join('1' for _ in range(arg_pool_lt_len))

            mv_args = dict()
            mv_args['pattern'] = "single_value"
            mv_args['single_value'] = kwargs['lease_time']
            mv_args['nest_owner'] = arg_topology_handle
            mv_args['nest_enabled'] = '0'
            mv_args['overlay_value'] = msc['lease_times']
            mv_args['overlay_index'] = arg_pool_lt_overlay_index
            mv_args['overlay_index_step'] = arg_pool_lt_overlay_index_step
            mv_args['overlay_count'] = arg_pool_lt_overlay_count
            t.log('info','dhcp server lease_time mv_args')
            t.log('info', mv_args)
            _result_ = rt_handle.invoke('multivalue_config', **mv_args)
            dhcp_args['lease_time'] = _result_['multivalue_handle']

        if msc['pool_start_addresses'] is not None:
            arg_pool_addrs_len = len(msc['pool_start_addresses'].split(','))
            arg_pool_overlay_index = ','.join(str(x+1) for x in range(arg_pool_addrs_len))
            arg_pool_overlay_index_step = ','.join('0' for _ in range(arg_pool_addrs_len))
            arg_pool_overlay_count = ','.join('1' for _ in range(arg_pool_addrs_len))

            mv_args = dict()
            mv_args['pattern'] = "counter"
            mv_args['counter_start'] = kwargs['pool_start_addr']
            mv_args['counter_step'] = msc['pool_inside_step']
            mv_args['nest_owner'] = arg_topology_handle
            mv_args['nest_enabled'] = '0'
            mv_args['overlay_value'] = msc['pool_start_addresses']
            mv_args['overlay_index'] = arg_pool_overlay_index
            mv_args['overlay_index_step'] = arg_pool_overlay_index_step
            mv_args['overlay_count'] = arg_pool_overlay_count
            t.log('info','dhcp server ipaddress_pool mv_args')
            t.log('info', mv_args)
            _result_ = rt_handle.invoke('multivalue_config', **mv_args)
            dhcp_args['ipaddress_pool'] = _result_['multivalue_handle']

        if msc['pool_sizes'] is not None:
            arg_pool_sizes_len = len(msc['pool_sizes'].split(','))
            arg_pool_sizes_overlay_index = ','.join(str(x + 1) for x in range(arg_pool_sizes_len))
            arg_pool_sizes_overlay_index_step = ','.join('0' for x in range(arg_pool_sizes_len))
            arg_pool_sizes_overlay_count = ','.join('1' for x in range(arg_pool_sizes_len))

            mv1_args = dict()
            mv1_args['pattern'] = "single_value"
            mv1_args['single_value'] = kwargs['pool_size']
            mv1_args['nest_owner'] = arg_topology_handle
            mv1_args['nest_enabled'] = '0'
            mv1_args['overlay_value'] = msc['pool_sizes']
            mv1_args['overlay_index'] = arg_pool_sizes_overlay_index
            mv1_args['overlay_index_step'] = arg_pool_sizes_overlay_index_step
            mv1_args['overlay_count'] = arg_pool_sizes_overlay_count
            _result1_ = rt_handle.invoke('multivalue_config', **mv1_args)
            dhcp_args['ipaddress_count'] = _result1_['multivalue_handle']

        if msc['pool_mask_lengths'] is not None:
            arg_pool_mask_lens_len = len(msc['pool_mask_lengths'].split(','))
            arg_pool_mask_lens_overlay_index = ','.join(str(x + 1) for x in range(arg_pool_mask_lens_len))
            arg_pool_mask_lens_overlay_index_step = ','.join('0' for x in range(arg_pool_mask_lens_len))
            arg_pool_mask_lens_overlay_count = ','.join('1' for x in range(arg_pool_mask_lens_len))

            mv2_args = dict()
            mv2_args['pattern'] = "counter"
            mv2_args['counter_start'] = kwargs['pool_size']
            mv2_args['counter_step'] = 0
            mv2_args['nest_owner'] = arg_topology_handle
            mv2_args['nest_enabled'] = '0'
            mv2_args['overlay_value'] = msc['pool_mask_lengths']
            mv2_args['overlay_index'] = arg_pool_mask_lens_overlay_index
            mv2_args['overlay_index_step'] = arg_pool_mask_lens_overlay_index_step
            mv2_args['overlay_count'] = arg_pool_mask_lens_overlay_count
            t.log('info','dhcp server ipaddress_pool_prefix_length mv_args')
            t.log('info', mv2_args)
            _result_ = rt_handle.invoke('multivalue_config', **mv2_args)
            dhcp_args['ipaddress_pool_prefix_length'] = _result_['multivalue_handle']
        if msc['subnet_addr_assign'] is not None:
            arg_pool_subnet_aa_len = len(msc['subnet_addr_assign'].split(','))
            arg_pool_subnet_aa_lens_overlay_index = ','.join(str(x + 1) for x in range(arg_pool_subnet_aa_len))
            arg_pool_subnet_aa_lens_overlay_index_step = ','.join('0' for x in range(arg_pool_subnet_aa_len))
            arg_pool_subnet_aa_lens_overlay_count = ','.join('1' for x in range(arg_pool_subnet_aa_len))

            mv_args = dict()
            mv_args['pattern'] = "single_value"
            mv_args['single_value'] = '0'
            mv_args['overlay_value'] = msc['subnet_addr_assign']
            mv_args['overlay_index'] = arg_pool_subnet_aa_lens_overlay_index
            mv_args['overlay_index_step'] = arg_pool_subnet_aa_lens_overlay_index_step
            mv_args['overlay_count'] = arg_pool_subnet_aa_lens_overlay_count
            t.log('info','dhcp server subnet_addr_assign mv_args')
            t.log('info', mv_args)
            _result_ = rt_handle.invoke('multivalue_config', **mv_args)
            dhcp_args['subnet_addr_assign'] = _result_['multivalue_handle']

    if 'v6' in kwargs['handle'] or 'pppox' in kwargs['handle']:
        t.log('info', 'Configure dhcpv6 server')
        dhcp_args['ip_version'] = '6'
        if 'dhcpv6_ia_type' in kwargs:
            dhcp_args['dhcp6_ia_type'] = kwargs['dhcpv6_ia_type']
        if 'pool_prefix_start' in kwargs:
            dhcp_args['start_pool_prefix'] = kwargs['pool_prefix_start']
        if 'pool_prefix_length' in kwargs:
            dhcp_args['prefix_length'] = kwargs['pool_prefix_length']
        if 'pool_prefix_size' in kwargs:
            dhcp_args['pool_prefix_size'] = kwargs['pool_prefix_size']

        # for multiple dhcp servers want customized pool addresses
        if 'multi_servers_config_v6' in kwargs and kwargs['multi_servers_config_v6'] is not None:
            t.log('info', 'Configure dhcpv6 mutiple servers parameters')
            match = re.match(r'\/topology:\d+', kwargs['handle'])
            arg_topology_handle = match.group(0)
            msc = kwargs['multi_servers_config_v6']

            # for simple increment pool
            mv_args = dict()
            mv_args['pattern'] = "counter"
            mv_args['counter_start'] = kwargs['pool_start_addr']
            mv_args['counter_step'] = msc['pool_inside_step']
            mv_args['counter_direction'] = 'increment'
            mv_args['nest_step'] = '0:0:0:1:0:0:0:0'
            mv_args['nest_owner'] = arg_topology_handle
            mv_args['nest_enabled'] = '1'
            _result_ = rt_handle.invoke('multivalue_config', **mv_args)
            dhcp_args['ipaddress_pool'] = _result_['multivalue_handle']

            mv_args = dict()
            mv_args['pattern'] = "counter"
            mv_args['counter_start'] = kwargs['pool_prefix_start']
            mv_args['counter_step'] = msc['pool_prefix_inside_step']
            mv_args['counter_direction'] = 'increment'
            mv_args['nest_step'] = '0:1:0:0:0:0:0:0'
            mv_args['nest_owner'] = arg_topology_handle
            mv_args['nest_enabled'] = '1'
            _result_ = rt_handle.invoke('multivalue_config', **mv_args)
            dhcp_args['start_pool_prefix'] = _result_['multivalue_handle']

            if msc['pool_start_addresses'] is not None:
                t.log('info', 'Configure dhcpv6 mutiple servers ipaddress_pool')

                arg_pool_addrs_len = len(msc['pool_start_addresses'].split(','))
                arg_pool_overlay_index = ','.join(str(x+1) for x in range(arg_pool_addrs_len))
                arg_pool_overlay_index_step = ','.join('0' for _ in range(arg_pool_addrs_len))
                arg_pool_overlay_count = ','.join('1' for _ in range(arg_pool_addrs_len))

                mv_args = dict()
                mv_args['pattern'] = "counter"
                mv_args['counter_start'] = kwargs['pool_start_addr']
                mv_args['counter_step'] = msc['pool_inside_step']
                mv_args['nest_owner'] = arg_topology_handle
                mv_args['nest_enabled'] = '1'
                mv_args['overlay_value'] = msc['pool_start_addresses']
                mv_args['overlay_index'] = arg_pool_overlay_index
                mv_args['overlay_index_step'] = arg_pool_overlay_index_step
                mv_args['overlay_count'] = arg_pool_overlay_count
                t.log('info','dhcpv6 server ipaddress_pool mv_args')
                t.log('info', mv_args)
                _result_ = rt_handle.invoke('multivalue_config', **mv_args)
                dhcp_args['ipaddress_pool'] = _result_['multivalue_handle']

            if msc['pool_prefix_starts'] is not None:
                t.log('info', 'Configure dhcpv6 mutiple servers start_pool_prefix')

                arg_pool_prefix_len = len(msc['pool_prefix_starts'].split(','))
                arg_pool_prefix_overlay_index = ','.join(str(x+1) for x in range(arg_pool_prefix_len))
                arg_pool_prefix_overlay_index_step = ','.join('0' for _ in range(arg_pool_prefix_len))
                arg_pool_prefix_overlay_count = ','.join('1' for _ in range(arg_pool_prefix_len))

                mv_args = dict()
                mv_args['pattern'] = "counter"
                mv_args['counter_start'] = kwargs['pool_prefix_start']
                mv_args['counter_step'] = msc['pool_prefix_inside_step']
                mv_args['nest_owner'] = arg_topology_handle
                mv_args['nest_enabled'] = '1'
                mv_args['overlay_value'] = msc['pool_prefix_starts']
                mv_args['overlay_index'] = arg_pool_prefix_overlay_index
                mv_args['overlay_index_step'] = arg_pool_prefix_overlay_index_step
                mv_args['overlay_count'] = arg_pool_prefix_overlay_count
                t.log('info','dhcpv6 server start_pool_prefix mv_args')
                t.log('info', mv_args)
                _result_ = rt_handle.invoke('multivalue_config', **mv_args)
                dhcp_args['start_pool_prefix'] = _result_['multivalue_handle']

            if msc['pool_sizes'] is not None:
                t.log('info', 'Configure dhcpv6 mutiple servers ipaddress_count')
                arg_pool_sizes_len = len(msc['pool_sizes'].split(','))
                arg_pool_sizes_overlay_index = ','.join(str(x + 1) for x in range(arg_pool_sizes_len))
                arg_pool_sizes_overlay_index_step = ','.join('0' for x in range(arg_pool_sizes_len))
                arg_pool_sizes_overlay_count = ','.join('1' for x in range(arg_pool_sizes_len))

                mv_args = dict()
                mv_args['pattern'] = "single_value"
                mv_args['single_value'] = kwargs['pool_size']
                mv_args['nest_owner'] = arg_topology_handle
                mv_args['nest_enabled'] = '0'
                mv_args['overlay_value'] = msc['pool_sizes']
                mv_args['overlay_index'] = arg_pool_sizes_overlay_index
                mv_args['overlay_index_step'] = arg_pool_sizes_overlay_index_step
                mv_args['overlay_count'] = arg_pool_sizes_overlay_count
                t.log('info','dhcpv6 server ipaddress_count mv_args')
                t.log('info', mv_args)
                _result1_ = rt_handle.invoke('multivalue_config', **mv_args)
                dhcp_args['ipaddress_count'] = _result1_['multivalue_handle']

            if msc['pool_prefix_sizes'] is not None:
                t.log('info', 'Configure dhcpv6 mutiple servers pool_prefix_size')
                arg_pool_prefix_sizes_len = len(msc['pool_prefix_sizes'].split(','))
                arg_pool_prefix_sizes_overlay_index = ','.join(str(x + 1) for x in range(arg_pool_prefix_sizes_len))
                arg_pool_prefix_sizes_overlay_index_step = ','.join('0' for x in range(arg_pool_prefix_sizes_len))
                arg_pool_prefix_sizes_overlay_count = ','.join('1' for x in range(arg_pool_prefix_sizes_len))

                mv_args = dict()
                mv_args['pattern'] = "single_value"
                mv_args['single_value'] = kwargs['pool_prefix_size']
                mv_args['nest_owner'] = arg_topology_handle
                mv_args['nest_enabled'] = '1'
                mv_args['overlay_value'] = msc['pool_prefix_sizes']
                mv_args['overlay_index'] = arg_pool_prefix_sizes_overlay_index
                mv_args['overlay_index_step'] = arg_pool_prefix_sizes_overlay_index_step
                mv_args['overlay_count'] = arg_pool_prefix_sizes_overlay_count
                t.log('info','dhcpv6 server pool_prefix_sizes mv_args')
                t.log('info', mv_args)
                _result1_ = rt_handle.invoke('multivalue_config', **mv_args)
                dhcp_args['pool_prefix_size'] = _result1_['multivalue_handle']

            if msc['pool_mask_lengths'] is not None:
                t.log('info', 'Configure dhcpv6 mutiple servers ipaddress_pool_prefix_length')
                arg_pool_mask_len = len(msc['pool_mask_lengths'].split(','))
                arg_pool_mask_overlay_index = ','.join(str(x + 1) for x in range(arg_pool_mask_len))
                arg_pool_mask_overlay_index_step = ','.join('0' for x in range(arg_pool_mask_len))
                arg_pool_mask_overlay_count = ','.join('1' for x in range(arg_pool_mask_len))

                mv_args = dict()
                mv_args['pattern'] = "counter"
                mv_args['counter_start'] = kwargs['pool_mask_length']
                mv_args['counter_step'] = '0'
                mv_args['nest_owner'] = arg_topology_handle
                mv_args['nest_enabled'] = '0'
                mv_args['overlay_value'] = msc['pool_mask_lengths']
                mv_args['overlay_index'] = arg_pool_mask_overlay_index
                mv_args['overlay_index_step'] = arg_pool_mask_overlay_index_step
                mv_args['overlay_count'] = arg_pool_mask_overlay_count
                t.log('info','dhcpv6 server ipaddress_pool_prefix_length mv_args')
                t.log('info', mv_args)
                _result_ = rt_handle.invoke('multivalue_config', **mv_args)
                dhcp_args['ipaddress_pool_prefix_length'] = _result_['multivalue_handle']

            if msc['pool_prefix_lengths'] is not None:
                t.log('info', 'Configure dhcpv6 mutiple servers prefix_length')
                arg_pool_prefix_len_len = len(msc['pool_prefix_lengths'].split(','))
                arg_pool_prefix_len_overlay_index = ','.join(str(x + 1) for x in range(arg_pool_prefix_len_len))
                arg_pool_prefix_len_overlay_index_step = ','.join('0' for x in range(arg_pool_prefix_len_len))
                arg_pool_prefix_len_overlay_count = ','.join('1' for x in range(arg_pool_prefix_len_len))

                mv_args = dict()
                mv_args['pattern'] = "single_value"
                mv_args['single_value'] = kwargs['pool_prefix_length']
                mv_args['nest_owner'] = arg_topology_handle
                mv_args['nest_enabled'] = '0'
                mv_args['overlay_value'] = msc['pool_prefix_lengths']
                mv_args['overlay_index'] = arg_pool_prefix_len_overlay_index
                mv_args['overlay_index_step'] = arg_pool_prefix_len_overlay_index_step
                mv_args['overlay_count'] = arg_pool_prefix_len_overlay_count
                t.log('info','dhcpv6 server prefix_length mv_args')
                t.log('info', mv_args)
                _result1_ = rt_handle.invoke('multivalue_config', **mv_args)
                dhcp_args['prefix_length'] = _result1_['multivalue_handle']

    config_status = rt_handle.invoke('emulation_dhcp_server_config', **dhcp_args)
    if config_status['status'] != '1':
        result['status'] = '0'
    else:
        if dhcp_args['ip_version'] == "4":
            rt_handle.dhcpv4_server_handle.append(config_status['dhcpv4server_handle'])
            result['dhcpv4_server_handle'] = config_status['dhcpv4server_handle']
        else:
            rt_handle.dhcpv6_server_handle.append(config_status['dhcpv6server_handle'])
            result['dhcpv6_server_handle'] = config_status['dhcpv6server_handle']
    return result


def dhcp_server_action(rt_handle, **kwargs):
    """
    :param rt_handle:                    RT object
    :param kwargs:
     handle:                        dhcp server handle
     action:                        'start' or stop
    :return:
     result
    """
    dhcp_args = dict()
    if 'handle' in kwargs:
        dhcp_args['handle'] = kwargs['handle']
    if 'action' in kwargs:
        if 'start' in kwargs['action']:
            dhcp_args['action'] = 'start_protocol'
        if 'stop' in kwargs['action']:
            dhcp_args['action'] = 'stop_protocol'
    result = rt_handle.invoke('test_control', **dhcp_args)
    return result


def traffic_simulation(rt_handle, **kwargs):
    """
     rt.invoke('traffic_simulation',src_port='1/5',dst_port='1/6',frame_size='1500',rate_pps='1000',
     vlan_id='1',svlan_id='2',src_mac='01:02:00:00:00:01',dst_mac='FF:FF:FF:FF:FF:FF',
     l3_protocol='ipv4',ip_precedence_mode='list', ip_precedence=['1','2','3'])

     rt.invoke('traffic_simulation',src_port='1/5',dst_port='1/6',frame_size='1500',rate_pps='1000',vlan_id='1',
     src_mac='01:02:00:00:00:01',dst_mac='09:01:02:00:00:03', vlan_mode='increment',vlan_step='1', vlan_count='4000',
     vlan_priority_mode='list', vlan_priority='{1} {3} {5}')

     rt.invoke('traffic_simulation',src_port='1/5',dst_port='1/6',frame_size='1500',rate_pps='1000',vlan_id='1',
     src_mac='01:02:00:00:00:01',dst_mac='09:01:02:00:00:03', vlan_mode='increment',vlan_step='1',
     vlan_count='4000', vlan_priority_mode='list', vlan_priority='{1} {3} {5}', svlan_id='2', svlan_priority='{2} {4}')

    simulation traffic
    :param rt_handle:
    src_port:                            source port
    dst_port:                            destination port
    encap_pppoe:                         pppoe simulation
    l3_protocol:                         ipv4/ipv6
    l4_protocol:                         icmpv6/dhcp/dhcpv6/udp
    frame_size:                          frame size
    rate_pps:                            rate in pps
    rate_bps:                            rate in bps
    rate_percent:                        rate in percent
    packets_count:                       number of packets to be transmitted
    duration:                            traffic duration
    message_type:                        message type used by icmpv6(echo_req|echo_reply)/dhcp(discover|request|
                                         |release)/dhcpv6(solicit|request|release)/pppoe(PADI/PADR/PADT)
    vlan_id:                             start vlan id
    vlan_mode:                           vlan id mode
    vlan_step:                           vlan step mode
    vlan_count:                          vlan counts
    svlan_id:                            start svlan id
    svlan_step:                          svlan step mode
    svlan_count:                         svlan counts
    src_mac:                             source mac address
    src_mac_step:                        source mac step
    src_mac_count:                       source mac count
    dst_mac:                             destination mac address
    dst_mac_step:                        destination mac step
    dst_mac_count:                       destination mac count
    src_ip:                              source ipv4 address
    src_ip_step:                         source ipv4 address step
    src_ip_count:                        source ipv4 count
    dst_ip:                              destination ipv4 address
    dst_ip_step:                         destination ipv4 address step
    dst_ip_count:                        destination ipv4 count
    src_ipv6:                            source ipv6 address
    src_ipv6_step:                       source ipv6 address step
    src_ipv6_count:                      source ipv6 address count
    dst_ipv6:                            destination ipv6 address
    dst_ipv6_step:                       destination ipv6 address step
    dst_ipv6_count:                      destination ipv6 address count


    :param kwargs:
    :return: result:                     dictionary of status/stream_id/traffic_item
    """
    traffic_args = dict()
    pppoe_args = dict()
    stack_index = 1
    traffic_args['traffic_generator'] = 'ixnetwork_540'
    traffic_args['circuit_type'] = 'raw'
    traffic_args['track_by'] = 'traffic_item'
    traffic_args['emulation_dst_handle'] = rt_handle.port_to_handle_map[kwargs['dst_port']]
    traffic_args['emulation_src_handle'] = rt_handle.port_to_handle_map[kwargs['src_port']]
    traffic_args['mode'] = 'create'
    if 'frame_size' in kwargs:
        traffic_args['frame_size'] = kwargs.get('frame_size')
    else:
        if 'l3_length' not in kwargs:
            traffic_args['frame_size'] = '1000'
    if 'l3_length' in kwargs:
        traffic_args['l3_length'] = kwargs['l3_length']
    if 'transmit_mode' in kwargs and 'burst' in kwargs['transmit_mode']:
        traffic_args['transmit_mode'] = 'continuous_burst'
    if 'name' in kwargs:
        traffic_args['name'] = kwargs['name']
    if 'rate_pps' in kwargs:
        traffic_args['rate_pps'] = kwargs['rate_pps']
    if 'rate_bps' in kwargs:
        traffic_args['rate_bps'] = kwargs['rate_bps']
    if 'rate_percent' in kwargs:
        traffic_args['rate_percent'] = kwargs['rate_percent']
    if 'packets_count' in kwargs:
        traffic_args['transmit_mode'] = 'single_burst'
        #traffic_args['pkts_per_burst'] = kwargs['packets_count']
        traffic_args['number_of_packets_per_stream'] = kwargs['packets_count']

    if 'duration' in kwargs:
        traffic_args['duration'] = kwargs['duration']

    if 'vlan_id' in kwargs:
        stack_index += 1
        traffic_args['vlan'] = 'enable'
        traffic_args['vlan_id'] = kwargs['vlan_id']
        if 'vlan_mode' in kwargs:
            traffic_args['vlan_id_mode'] = kwargs['vlan_mode']
        if 'vlan_step' in kwargs:
            traffic_args['vlan_id_step'] = kwargs['vlan_step']
        if 'vlan_count' in kwargs:
            traffic_args['vlan_id_count'] = kwargs['vlan_count']
        if 'svlan_id' in kwargs:
            stack_index += 1
            traffic_args['vlan_id'] = [kwargs['svlan_id'], kwargs['vlan_id']]
            if 'svlan_step' in kwargs or 'vlan_step' in kwargs:
                traffic_args['vlan_id_step'] = [kwargs.get('svlan_step', 1), kwargs.get('vlan_step', 1)]
            if 'svlan_count' in kwargs or 'vlan_count' in kwargs:
                traffic_args['vlan_id_count'] = [kwargs.get('svlan_count', 1), kwargs.get('vlan_count', 1)]
        if 'vlan_priority' in kwargs:
            traffic_args['vlan_user_priority'] = kwargs['vlan_priority']
        if 'vlan_priority_mode' in kwargs:
            traffic_args['vlan_user_priority_mode'] = kwargs['vlan_priority_mode']
        if 'vlan_priority_step' in kwargs:
            traffic_args['vlan_user_priority_step'] = kwargs['vlan_priority_step']
        if 'svlan_priority' in kwargs:
            traffic_args['vlan_user_priority'] = [kwargs['svlan_priority'], kwargs['vlan_priority']]
        if 'svlan_priority_step' in kwargs:
            traffic_args['vlan_user_priority_step'] = [kwargs['svlan_priority_step'], kwargs['svlan_priority_step']]
    if 'src_mac' in kwargs:
        traffic_args['mac_src'] = kwargs['src_mac']
        if 'src_mac_step' in kwargs:
            traffic_args['mac_src_mode'] = 'increment'
            traffic_args['mac_src_step'] = kwargs['src_mac_step']
            traffic_args['mac_src_count'] = kwargs.get('src_mac_count', 1)
    if 'dst_mac' in kwargs:
        traffic_args['mac_dst'] = kwargs['dst_mac']
        if 'dst_mac_step' in kwargs:
            traffic_args['mac_dst_mode'] = 'increment'
            traffic_args['mac_dst_step'] = kwargs['dst_mac_step']
            traffic_args['mac_dst_count'] = kwargs.get('dst_mac_count', 1)

    if 'src_ip' in kwargs:
        traffic_args['ip_src_addr'] = kwargs['src_ip']
        if 'src_ip_step' in kwargs:
            traffic_args['ip_src_mode'] = 'increment'
            traffic_args['ip_src_step'] = kwargs['src_ip_step']
            traffic_args['ip_src_count'] = kwargs.get('src_ip_count', 1)

    if 'src_ipv6' in kwargs:
        traffic_args['ipv6_src_addr'] = kwargs['src_ipv6']
        if 'src_ipv6_step' in kwargs:
            traffic_args['ipv6_src_mode'] = 'increment'
            traffic_args['ipv6_src_step'] = kwargs['src_ipv6_step']
            traffic_args['ipv6_src_count'] = kwargs.get('src_ipv6_count', 1)

    if 'dst_ip' in kwargs:
        traffic_args['ip_dst_addr'] = kwargs['dst_ip']
        if 'dst_ip_step' in kwargs:
            traffic_args['ip_dst_mode'] = 'increment'
            traffic_args['ip_dst_step'] = kwargs['dst_ip_step']
            traffic_args['ip_dst_count'] = kwargs.get('dst_ip_count', 1)
    if 'dst_ipv6' in kwargs:
        traffic_args['ipv6_dst_addr'] = kwargs['dst_ipv6']

        if 'dst_ipv6_step' in kwargs:
            traffic_args['ipv6_dst_mode'] = 'increment'
            traffic_args['ipv6_dst_step'] = kwargs['dst_ipv6_step']
            traffic_args['ipv6_dst_count'] = kwargs.get('dst_ipv6_count', 1)

    if 'ip_precedence' in kwargs:
        traffic_args['ip_precedence'] = kwargs['ip_precedence']
    if 'ip_precedence_mode' in kwargs:
        traffic_args['ip_precedence_mode'] = kwargs['ip_precedence_mode']
    if 'ip_precedence_step' in kwargs:
        traffic_args['ip_precedence_step'] = kwargs['ip_precedence_step']
    if 'ip_precedence_count' in kwargs:
        traffic_args['ip_precedence_count'] = kwargs['ip_precedence_count']
    if 'ip_dscp' in kwargs:
        traffic_args['ip_dscp'] = kwargs['ip_dscp']
    if 'ip_dscp_mode' in kwargs:
        traffic_args['ip_dscp_mode'] = kwargs['ip_dscp_mode']
    if 'ip_dscp_step' in kwargs:
        traffic_args['ip_dscp_step'] = kwargs['ip_dscp_step']
    if 'ip_dscp_count' in kwargs:
        traffic_args['ip_dscp_count'] = kwargs['ip_dscp_count']

    if 'l4_protocol' in kwargs:
        traffic_args['l4_protocol'] = kwargs['l4_protocol']
        if 'dhcpv6' in kwargs['l4_protocol']:
            traffic_args['l4_protocol'] = 'udp'

    if 'l3_protocol' in kwargs:
        traffic_args['l3_protocol'] = kwargs['l3_protocol']

    result = rt_handle.invoke('traffic_config', **traffic_args)
    if result['status'] != '1':
        return result
    else:
        rt_handle.traffic_item.append(result['stream_id'])
        traffic_handle = result['stream_id']
        stream_id = result['traffic_item']
        headers = result[stream_id]['headers'].split(' ')
        index = stack_index - 1
        pppoe_header = headers[index]
        pppoe_index = stack_index

    if 'l4_protocol' in kwargs and kwargs['l4_protocol'] == 'dhcp':
        ##enable dhcp option
        header_handle = headers[-2]
        message_handle = 'dhcp.header.options.fields.nextOption.field.dhcpMessageType.code-182'
        option_args = dict()
        option_args['mode'] = 'set_field_values'
        option_args['traffic_generator'] = 'ixnetwork_540'
        option_args['header_handle'] = header_handle
        option_args['field_handle'] = message_handle
        option_args['field_optionalEnabled'] = '1'
        rt_handle.invoke('traffic_config', **option_args)
        ## set dhcp message type
        dhcp_msg = 'DHCP' + kwargs['message_type'].upper()
        msg_args = dict()
        msg_args['mode'] = 'set_field_values'
        message_handle = 'dhcp.header.options.fields.nextOption.field.dhcpMessageType.messageType-184'
        msg_args['traffic_generator'] = 'ixnetwork_540'
        msg_args['field_handle'] = message_handle
        msg_args['header_handle'] = header_handle
        msg_args['field_fieldValue'] = dhcp_msg
        result = rt_handle.invoke('traffic_config', **msg_args)
        return result

    if 'l4_protocol' in kwargs and 'dhcpv6' in kwargs['l4_protocol']:
        stack_index += 3  ##ipv6 layer + udp layer + dhcpv6 layer
        dhcpv6_args = dict()
        dhcpv6_args['traffic_generator'] = 'ixnetwork_540'
        dhcpv6_args['mode'] = 'modify_or_insert'
        dhcpv6_args['stream_id'] = stream_id
        dhcpv6_args['stack_index'] = stack_index
        dhcpv6_args['pt_handle'] = 'dhcpv6ClientServer'
        ## this is dhcpv6 solicit by default
        result = rt_handle.invoke('traffic_config', **dhcpv6_args)
        if result['status'] != '1':
            traffic_action(rt_handle, handle=traffic_handle, action='delete')
            return result
        else:
            headers = result[stream_id]['headers'].split(' ')
            field_handle = result['traffic_item']
            if 'message_type' in kwargs:
                msg_type = kwargs['message_type'].capitalize()
                v6_msg_args = dict()
                v6_msg_args['mode'] = 'set_field_values'
                v6_msg_args['header_handle'] = headers[-2]
                v6_msg_args['field_handle'] = 'dhcpv6ClientServer.header.messageType-1'
                v6_msg_args['field_fieldValue'] = msg_type
                rt_handle.invoke('traffic_config', **v6_msg_args)

    if 'l4_protocol' in kwargs and 'icmpv6' in kwargs['l4_protocol']:

        if 'message_type' in kwargs and 'echo_req' in kwargs['message_type']:
            field_handle = "icmpv6.icmpv6Message.icmpv6MessegeType.echoRequestMessage.messageType-17"
        if 'message_type' in kwargs and 'echo_reply' in kwargs['message_type']:
            field_handle = "icmpv6.icmpv6Message.icmpv6MessegeType.echoReplyMessage.messageType-22"
        if 'message_type' in kwargs:
            result2 = rt_handle.invoke('traffic_config',
                                       mode='set_field_values',
                                       traffic_generator='ixnetwork_540',
                                       pt_handle='icmpv6',
                                       header_handle=headers[-2],
                                       field_handle=field_handle,
                                       field_activeFieldChoice='1')
            if result2['status'] != '1':
                traffic_action(rt_handle, handle=result['stream_id'], action='delete')
                return result2

    if 'pppoe_encap' in kwargs and kwargs['pppoe_encap']:
        pppoe_args = dict()
        pppoe_args['traffic_generator'] = 'ixnetwork_540'
        pppoe_args['mode'] = 'append_header'
        pppoe_args['stream_id'] = pppoe_header
        pppoe_args['stack_index'] = pppoe_index
        if 'message_type' in kwargs:
            pppoe_args['pt_handle'] = 'pppoEDiscovery'
        else:
            pppoe_args['pt_handle'] = 'pppoESession'
        result3 = rt_handle.invoke('traffic_config', **pppoe_args)
        if result3['status'] != '1':
            traffic_action(rt_handle, handle=result['stream_id'], action='delete')
            return result3
        headers = result3['handle']

        if 'message_type' in kwargs:
            pppoe_msg_type = kwargs['message_type'].upper()
            pppoe_msg_args = dict()
            pppoe_msg_args['mode'] = 'set_field_values'
            pppoe_msg_args['header_handle'] = headers
            pppoe_msg_args['field_handle'] = 'pppoEDiscovery.header.header.opcode-3'
            pppoe_msg_args['field_fieldValue'] = pppoe_msg_type
            rt_handle.invoke('traffic_config', **pppoe_msg_args)

            if kwargs['message_type'] == 'PADT' and 'session_id' in kwargs:
                pppoe_msg_args = dict()
                pppoe_msg_args['mode'] = 'set_field_values'
                pppoe_msg_args['header_handle'] = headers
                pppoe_msg_args['field_handle'] = 'pppoEDiscovery.header.header.sessionID-4'
                pppoe_msg_args['field_fieldValue'] = kwargs['session_id']
                rt_handle.invoke('traffic_config', **pppoe_msg_args)

            if kwargs['message_type'] == 'PADR' and 'service_name_enable' in kwargs:
                pppoe_msg_args = dict()
                pppoe_msg_args['mode'] = 'set_field_values'
                pppoe_msg_args['header_handle'] = headers
                pppoe_msg_args['field_handle'] = 'pppoEDiscovery.header.tags.type.serviceName.type-6'
                pppoe_msg_args['field_activeFieldChoice'] = '1'
                pppoe_msg_args['field_optionalEnabled'] = '1'
                rt_handle.invoke('traffic_config', **pppoe_msg_args)

            if kwargs['message_type'] == 'PADR' and 'ac_cookie_enable' in kwargs:
                pppoe_msg_args = dict()
                pppoe_msg_args['mode'] = 'set_field_values'
                pppoe_msg_args['header_handle'] = headers
                pppoe_msg_args['field_handle'] = 'pppoEDiscovery.header.tags.type.acCookie.type-44'
                pppoe_msg_args['field_activeFieldChoice'] = '1'
                pppoe_msg_args['field_optionalEnabled'] = '1'
                rt_handle.invoke('traffic_config', **pppoe_msg_args)

    return result


def ancp_action(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    handle:             ancp_handle
    action:             start/stop/abort/restartdown
    :return:
    """
    import time

    handle = kwargs['handle']
    action = kwargs['action'].lower()
    if 'start' == action:
        action = 'enable'
    elif 'stop' == action:
        action = 'disable'

    if action in ('enable', 'disable', 'abort'):
        rt_handle.invoke('emulation_ancp_control', ancp_handle=handle, action=action)

    if 'abort' == action:
        return

    if 'restartdown' == action:
        rt_handle._invokeIxNet('execute', 'restartDown', handle)

    check_status = kwargs.get('check_status', True)
    if check_status:
        time.sleep(2)
        handle = '::ixNet::OBJ-' + handle
        retry = 0
        while True:
            resp = rt_handle.invoke('IxNet::getAttribute', handle, '-sessionStatus')
            if action == 'enable' and resp[0] == 'up':
                break
            if action == 'restartdown' and resp[0] == 'up':
                break
            if action == 'disable' and resp[0] == 'notStarted':
                break
            time.sleep(3)
            retry += 1
            if retry > 10:
                raise Exception("ancp action {} failed with status {}".format(action, resp))


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
    mask:                       mask
    gateway:                    gateway address
    ancp_standard:              ancp standard (rfc6320/ietf-ancp-protocol5), by default rfc6320
    keep_alive:                 ancp keepalive timer
    keep_alive_retries:         ancp keepalive retries, by default is 3
    remote_loopback:            1/0
    dsl_type:                   adsl1 adsl2 adsl2_plus vdsl1 vdsl2 sdsl unknown
    pon_type:                   gpon xgpon1 twdmpon xgspon wdmpon other
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
    result = add_link(rt_handle, **kwargs)
    if result['status'] != '1':
        return result
    ip_handle = result['ipv4_handle']
    device_handle = result['device_group_handle']
    ancp_args = dict()
    ancp_args['handle'] = ip_handle
    ancp_args['ancp_standard'] = kwargs.get('ancp_standard', 'rfc6320')
    ancp_args['trigger_access_loop_events'] = '1'
    ancp_args['mode'] = 'create'
    ancp_args['line_config'] = '1'
    ancp_args['topology_discovery'] = '1'
    if 'keep_alive' in kwargs:
        ancp_args['keep_alive'] = kwargs['keep_alive']
    if 'keep_alive_retries' in kwargs:
        ancp_args['keep_alive_retires'] = kwargs['keep_alive_retries']
    ancp_args['sut_ip_addr'] = kwargs.get('dut_ip', '100.0.0.1')
    ancp_args['sut_service_port'] = '6068'
    ancp_args['remote_loopback'] = kwargs.get('remote_loopback', '0')
    _result_ = rt_handle.invoke('emulation_ancp_config', **ancp_args)
    if _result_['status'] != '1':
        return _result_
    ancp_handle = _result_['ancp_handle']
    rt_handle.ancp_handle.append(ancp_handle)
    ##create network group first since using ancp_client_handle directly does not work
    network_args = dict()
    network_args['protocol_handle'] = device_handle
    network_args['multiplier'] = kwargs.get('lines_per_node', '1')
    network_args['enable_device'] = "1"
    _result_ = rt_handle.invoke('network_group_config', **network_args)
    if _result_['status'] != '1':
        return _result_

    networkgroup_handle = _result_['network_group_handle']
    line_args = dict()
    line_args['mode'] = 'create'
    line_args['handle'] = networkgroup_handle
    #line_args['ancp_client_handle'] = ancp_handle
    #line_args['subscriber_lines_per_access_node'] = kwargs.get('lines_per_node', '1')
    if 'dsl_type' in kwargs:
        line_args['dsl_type'] = kwargs['dsl_type']
        line_args['enable_dsl_type'] = '1'
    if 'pon_type' in kwargs:
        line_args['pon_type'] = kwargs['pon_type']
    if 'tech_type' in kwargs:
        line_args['tech_type'] = kwargs['tech_type']
    line_args['vlan_allocation_model'] = kwargs.get('vlan_allocation_model', '1_1')
    if 'flap_mode' in kwargs:
        line_args['flap_mode'] = kwargs['flap_mode']
    if 'circuit_id' in kwargs:
        circuit_id = kwargs['circuit_id']
        if 'circuit_id_start' in kwargs:
            start = str(kwargs.get('circuit_id_start'))
            step = str(kwargs.get('circuit_id_step', '1'))
            repeat = str(kwargs.get('circuit_id_repeat', '1'))
            length = str(kwargs.get('circuit_id_length', '1'))
            if '?' in circuit_id:
                increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                circuit_id = circuit_id.replace('?', increment)
            else:
                circuit_id = circuit_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
        _result_ = add_string_mv(rt_handle, string_name=circuit_id)
        print(_result_)
        multivalue_6_handle = _result_['multivalue_handle']
        line_args['circuit_id'] = multivalue_6_handle
    if 'remote_id' in kwargs:
        remote_id = kwargs.get('remote_id')
        if 'remote_id_start' in kwargs:
            start = str(kwargs.get('remote_id_start'))
            step = str(kwargs.get('remote_id_step', '1'))
            repeat = str(kwargs.get('remote_id_repeat', '1'))
            length = str(kwargs.get('remote_id_length', '1'))
            if '?' in remote_id:
                increment = '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'
                remote_id = remote_id.replace('?', increment)
            else:
                remote_id = remote_id + '{Inc:' + start + ',' + step + ',' + length + ',' + repeat + '}'

        _result_ = add_string_mv(rt_handle, string_name=remote_id)
        print(_result_)
        multivalue_7_handle = _result_['multivalue_handle']
        line_args['remote_id'] = multivalue_7_handle
        line_args['enable_remote_id'] = '1'

    vlan_args = dict()
    if 'service_vlan_start' in kwargs:
        vlan_args['start'] = kwargs.get('service_vlan_start')
        vlan_args['step'] = kwargs.get('service_vlan_step', '1')
        vlan_args['repeat'] = kwargs.get('service_vlan_repeat', '1')
        vlan_args['count'] = kwargs.get('service_vlan_length', '4094')
        line_args['service_vlan_id'] = _set_custom_pattern(rt_handle, **vlan_args)
    if 'customer_vlan_start' in kwargs:
        vlan_args['start'] = kwargs.get('customer_vlan_start')
        vlan_args['step'] = kwargs.get('customer_vlan_step', '1')
        vlan_args['repeat'] = kwargs.get('customer_vlan_repeat', '1')
        vlan_args['count'] = kwargs.get('customer_vlan_length', '4094')
        line_args['customer_vlan_id'] = _set_custom_pattern(rt_handle, **vlan_args)
    line_args['enable_actual_rate_upstream'] = 'true'
    line_args['enable_actual_rate_downstream'] = 'true'

    result = rt_handle.invoke('emulation_ancp_subscriber_lines_config', **line_args)
    if result['status'] != '1':
        return result
    result['ancp_handle'] = ancp_handle
    rt_handle.ancp_line_handle.append(result['ancp_subscriber_lines_handle'])
    return result


def add_lacp(rt_handle, **kwargs):
    """

    :param rt_handle:
    :param kwargs:
    port_list(mandatory):                              ports in AE
    name(mandatory):                                   LAG AE name
    protocol:                               lacp or statisLag
    mode:                                   active or passive
    admin_key:                              administrative key
    actor_system_id:                        AE system id
    actor_key:                              AE actor key
    actor_port_pri:                         AE port priority
    :return:                                dictionary
    """
    if 'handle' not in rt_handle.ae:
        rt_handle.ae['handle'] = []
    rt_handle.ae[kwargs['name']] = []
    #rt_handle.ae[kwargs['name']] = kwargs['port_list']
    for port in kwargs['port_list']:
        rt_handle.ae[port] = dict()
        rt_handle.ae[kwargs['name']].append(port)
    result = add_topology(rt_handle, port_list=kwargs['port_list'])
    if result['status'] != "1":
        raise Exception("failed at add topology for ports {}".format(kwargs['port_list']))
    topo_handle = result['topology_handle']
    dev_args = dict()
    dev_args['topology_handle'] = topo_handle
    if 'name' in kwargs:
        dev_args['name'] = kwargs['name']
    result = add_device_group(rt_handle, **dev_args)
    if result['status'] != "1":
        raise Exception("failed at add device for ports {}".format(kwargs['port_list']))
    device_handle = result['device_group_handle']
    result = set_vlan(rt_handle, handle=device_handle)
    ethernet_handle = result['ethernet_handle']
    lacp_args = dict()
    lacp_args['mode'] = "create"
    lacp_args['handle'] = ethernet_handle
    if 'protocol' in kwargs:
        lacp_args['session_type'] = kwargs['protocol']
    if 'actor_key' in kwargs:
        lacp_args['actor_key'] = kwargs['actor_key']

    lacp_args['actor_port_num'] = kwargs.get('actor_port_num', '1')
    lacp_args['actor_port_num_step'] = kwargs.get('actor_port_dum_step', '1')
    if 'admin_key' in kwargs:
        lacp_args['administrative_key'] = kwargs['admin_key']
    if 'actor_system_id' in kwargs:
        lacp_args['actor_system_id'] = kwargs['actor_system_id']
    if 'mode' in kwargs:
        lacp_args['lacp_activity'] = kwargs['mode']
    if 'actor_port_pri' in kwargs:
        lacp_args['actor_port_pri'] = kwargs['actor_port_pri']

    result = rt_handle.invoke('emulation_lacp_link_config', **lacp_args)
    if result['status'] != "1":
        raise Exception("failed to add lacp for ports {}".format(kwargs['port_list']))
    if 'lacp_handle' in result:
        lacp_handle = result['lacp_handle']
    elif 'staticLag_handle' in result:
        lacp_handle = result['staticLag_handle']
    rt_handle.ae['handle'].append(lacp_handle)
    for port in kwargs['port_list']:
        rt_handle.ae[port]['device_group_handle'] = device_handle
        if 'name' in kwargs:
            rt_handle.ae[port]['ae_name'] = kwargs['name']
        rt_handle.ae[port]['lacp_handle'] = lacp_handle

    return result


def ancp_line_action(rt_handle, **kwargs):
    """
    :param rt_handle:
    :param kwargs:
    handle:             ancp_handle
    action:             flap_start/flat_stop/flap_start_resync/port_up/port_down
    :return:
    """
    sub_handle = kwargs['handle']
    action = kwargs['action']
    if 'flap_start_resync' in action:
        action = 'flap_start_resync'
    elif 'flap_stop' in action:
        action = 'flap_stop'
    elif 'flap_start' in action:
        action = 'flap_start'
    elif 'port_up' in action:
        action = 'send_port_up'
    elif 'port_down' in action:
        action = 'send_port_down'
    elif 'disable' in action:
        action = 'disable'

    return rt_handle.invoke('emulation_ancp_control', ancp_subscriber=sub_handle, action=action)


def verify_traffic_throughput_tester(rt_handle, minimum_rx_percentage=97, mode='l23_test_summary', stream_name=None,
                                     verify_by='throughput', instantaneous_rate='0mbps', packet_count=-1,
                                     error_tolerance=1, **kwargs):
    """
    Verifies traffic three different ways (throughput/packetcount/rate). Read below for arguments required by the
    different verifications.

    If mode is set to 'all', traffic throughput (percentage of packets received) is the
    only verification available.


    :param minimum_rx_percentage:       Minimum percentage of traffic that must be received to pass. Default is 97.
                                        This only affects verification when verify_by is 'throughout'.

    :param mode:                        Default is 'l23_test_summary'. Can target specific traffic item with
                                        mode='traffic_item'

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

    mode = mode.strip()
    error_tolerance = int(error_tolerance)

    if 'all' in mode:
        # Supporting legacy argument 'all'. 'l23_test_summary' gives stats quicker at scale than 'all'
        mode = 'l23_test_summary'
    elif 'l23_test_summary' not in mode and 'traffic_item' not in mode:
        # Sanity checks on mode
        raise Exception('Invalid mode. Please try l23_test_summary or traffic_item. You selected: {0}'.format(mode))

    kwargs['mode'] = mode

    traffic_dict = rt_handle.invoke('get_traffic_stats', **kwargs)      # mode='all' or mode='traffic_item'

    if 'l23_test_summary' in mode:
        # Aggregate traffic verification
        # Calculate whether [Tx / Rx] * 100 is greater than minimum_rx_percentage
        rx_packets = traffic_dict['l23_test_summary']['rx']['pkt_count']
        tx_packets = traffic_dict['l23_test_summary']['tx']['pkt_count']
        throughput_percentage = (int(rx_packets) / int(tx_packets)) * 100

        if throughput_percentage < int(minimum_rx_percentage):
            # Aggregate throughput is < expected
            raise Exception('Observed aggregate throughput of {0}% is less than minimum allowable '
                            'percentage of {1}!'.format(throughput_percentage, minimum_rx_percentage))

        else:
            # Aggregate throughput is >= expected
            t.log('info', 'Observed aggregate throughput of {0}% is greater than or equal to the '
                          'minimum allowable percentage of {1}! Aggregate traffic throughput '
                          'verified.'.format(throughput_percentage, minimum_rx_percentage))

    elif 'traffic_item' in mode and stream_name is not None:

        # Find the traffic_item associated with stream_name
        stream_id = None
        for name in rt_handle.traffic_item:
            if name.endswith(stream_name):
                stream_id = name

        if stream_id is None:
            # Couldn't find the stream, raise exception
            raise Exception('{0} does not match any configured stream stream names.'.format(stream_name))
        else:
            # Proceed with verification of valid traffic_item
            if 'throughput' in verify_by:
                # Verify throughput percentage
                rx_packets = traffic_dict['traffic_item'][stream_id]['rx']['total_pkts']
                tx_packets = traffic_dict['traffic_item'][stream_id]['tx']['total_pkts']

                throughput_percentage = (int(rx_packets) / int(tx_packets)) * 100

                if throughput_percentage < int(minimum_rx_percentage):
                    # traffic_item throughput is < expected
                    raise Exception('Observed aggregate throughput of {0}% is less than minimum allowable '
                                    'percentage of {1}!'.format(throughput_percentage, minimum_rx_percentage))

                else:
                    # traffic_item throughput is >= expected
                    t.log('info', 'Observed aggregate throughput of {0}% is greater than or equal to the '
                                  'minimum allowable percentage of {1}! Aggregate traffic throughput '
                                  'verified.'.format(throughput_percentage, minimum_rx_percentage))

            elif 'rate' in verify_by:
                # Verify measured rate
                t.log('info', 'Verify by rate has been selected. Please note that rate statistics will not be available'
                      'unless the stream is actively sending traffic.')

                measured_rx_rate = traffic_dict['traffic_item'][stream_id]['rx']['total_pkt_mbit_rate']

                mbps_rate = instantaneous_rate.split('mbps')

                if len(mbps_rate) is not 2:
                    raise Exception('Parsed multiple digits from entered instantaneous_rate of {0}. Please select '
                                    'a valid entry, such as 5mbps'.format(instantaneous_rate))

                mbps_rate = mbps_rate[0]
                lower_bound = float(mbps_rate) - (error_tolerance / 100) * float(mbps_rate)
                upper_bound = float(mbps_rate) + (error_tolerance / 100) * float(mbps_rate)

                if float(lower_bound) <= float(measured_rx_rate) <= float(upper_bound):
                    # Measured rate is within bounds
                    t.log('info', 'Measured traffic rate of {0} is within +/-{1}% range of {2}!'
                          .format(measured_rx_rate, error_tolerance, instantaneous_rate))
                else:
                    # Measured rate is outside of expected bounds
                    raise Exception('Measured traffic rate of {0}mbps is NOT within +/-{1}% range of {2}!'
                                    .format(measured_rx_rate, error_tolerance, instantaneous_rate))


            elif 'packetcount' in verify_by:
                # Verify number of packets received
                t.log('info', 'Verify by packet count has been selected.')
                rx_packets = traffic_dict['traffic_item'][stream_id]['rx']['total_pkts']

                if int(rx_packets) == int(packet_count):
                    # Received packets matches amount expected by user
                    t.log('info', '{0} packets received. {1} packets expected.'.format(rx_packets, packet_count))
                else:
                    # Received packets is not equal to amount expected by user
                    raise Exception('{0} packets received are less than {1} packets expected'
                                    .format(rx_packets, packet_count))

            else:
                # Invalid verification
                raise Exception('You selected an invalid verify_by parameter: {0}. Acceptable values are '
                                'throughtput/rate/packetcount'.format(verify_by))
    else:
        # Invalid mode. Should raise exception rather than falling through and returning traffic_dict
        raise Exception('Invalid mode! You selected: {0}. Please try l23_test_summary or traffic_item.'.format(mode))

    return traffic_dict


def set_pppoe_dsl_attribute_Ixnet(rt_handle, **kwargs):
    """
    rt._invokeIxNet('set_pppoe_dsl_attribute', dsltype='adsl_1', upstream_rate='30000', downstream_rate='50000', handle=handle)

    :param kwargs:
    handle:                 pppox simulation handle
    upstream_rate:          upstream rate
    downstream_rate:        downstream rate
    dsltype:                none/adsl_1/adsl_2/adsl_2_p/vdsl_1/vdsl_2/sdsl/g_fast/svvdsl/sdsl_bonded/vdsl_bonded/g_fast_bonded/svvdsl_bonded/other/userdefined

    :return:
    """
    #2147483647=none 1=adsl_1 2=adsl_2 3=adsl_2_p 4=vdsl_1 5=vdsl_2 6=sdsl 8=g_fast 9=svvdsl 10=sdsl_bonded 11=vdsl_bonded 12=g_fast_bonded 13=svvdsl_bonded 0=other 14=userdefined
    root = rt_handle._invokeIxNet("getRoot")
    handle = root + kwargs['handle']
    attrs = dict()
    attrs['-clientSignalLoopChar'] = 'true'
    if 'dsltype' in kwargs:
        att_value = kwargs.get('dsltype')
        attrs['-dslTypeTlv'] = att_value
    if 'upstream_rate' in kwargs:
        attrs['-actualRateUpstream'] = kwargs['upstream_rate']
    if 'downstream_rate' in kwargs:
        attrs['-actualRateDownstream'] = kwargs['downstream_rate']

    for attr in attrs:
        t.log("attr is {}".format(attr))
        dsl = rt_handle._invokeIxNet('getAttribute', handle, attr)
        t.log("dsl obj is {}".format(dsl))

        if rt_handle._invokeIxNet('getList', dsl, 'singleValue'):
            dsl = rt_handle._invokeIxNet('getList', dsl, 'singleValue')[0]
        else:
            newdsl = rt_handle._invokeIxNet('add', dsl, 'singleValue')
            rt_handle._invokeIxNet("commit")
            dsl = rt_handle._invokeIxNet("remapIds", newdsl)[0]

        rt_handle._invokeIxNet('setAttribute', dsl, '-value', attrs[attr])
        t.log('set dsl obj {} value {}'.format(dsl, attrs[attr]))
        try:
            rt_handle._invokeIxNet('commit')
        except:
            raise Exception('failed to set {} for pppoe client {}'.format(attr, handle))

def set_pppoe_dsl_attribute(rt_handle, **kwargs):
    """
    rt.invoke('set_pppoe_dsl_attribute', dsltype='adsl_1', upstream_rate='30000', downstream_rate='50000', handle=handle)

    :param kwargs:
    handle:                 pppox simulation handle
    upstream_rate:          upstream rate
    downstream_rate:        downstream rate
    dsltype:                none/adsl_1/adsl_2/adsl_2_p/vdsl_1/vdsl_2/sdsl/g_fast/svvdsl/sdsl_bonded/vdsl_bonded/g_fast_bonded/svvdsl_bonded/other/userdefined

    :return:
    """
    #2147483647=none 1=adsl_1 2=adsl_2 3=adsl_2_p 4=vdsl_1 5=vdsl_2 6=sdsl 8=g_fast 9=svvdsl 10=sdsl_bonded 11=vdsl_bonded 12=g_fast_bonded 13=svvdsl_bonded 0=other 14=userdefined
    root = rt_handle.invoke("IxNet::getRoot")
    handle = root + kwargs['handle']
    attrs = dict()
    attrs['-clientSignalLoopChar'] = 'true'
    if 'dsltype' in kwargs:
        att_value = kwargs.get('dsltype')
        attrs['-dslTypeTlv'] = att_value
    if 'upstream_rate' in kwargs:
        attrs['-actualRateUpstream'] = kwargs['upstream_rate']
    if 'downstream_rate' in kwargs:
        attrs['-actualRateDownstream'] = kwargs['downstream_rate']

    for attr in attrs:
        t.log("attr is {}".format(attr))
        dsl = rt_handle.invoke('IxNet::getAttribute', handle, attr)
        t.log("dsl obj is {}".format(dsl))

        if rt_handle.invoke('IxNet::getList', dsl, 'singleValue'):
            dsl = rt_handle.invoke('IxNet::getList', dsl, 'singleValue')[0]
        else:
            newdsl = rt_handle.invoke('IxNet::add', dsl, 'singleValue')
            rt_handle.invoke("IxNet::commit")
            dsl = rt_handle.invoke("IxNet::remapIds", newdsl)[0]

        rt_handle.invoke('IxNet::setAttribute', dsl, '-value', attrs[attr])
        t.log('set dsl obj {} value {}'.format(dsl, attrs[attr]))
        try:
            rt_handle.invoke('IxNet::commit')
        except:
            raise Exception('failed to set {} for pppoe client {}'.format(attr, handle))


def set_pppoe_ia_attribute(rt_handle, **kwargs):
    """
    rt.invoke('set_pppoe_ia_attribute', dsltype='adsl_1', upstream_rate='30000', downstream_rate='50000', handle=handle)
    rt.invoke('set_pppoe_ia_attribute', dsltype='adsl_2_p', upstream_rate='4000', downstream_rate='8000',
     handle=subs[0].rt_pppox_handle, aggregate_circuit_id='agg{Inc:1,,,1}', remote_id='Inremote', circuit_id='cir{Inc:1,,,1}')
    set/change pppoe ia arributes
    :param kwargs:
    handle:                 pppox simulation handle
    upstream_rate:          upstream rate
    downstream_rate:        downstream rate
    dsltype:                none/adsl_1/adsl_2/adsl_2_p/vdsl_1/vdsl_2/sdsl/g_fast/svvdsl/sdsl_bonded/vdsl_bonded/g_fast_bonded/svvdsl_bonded/other/userdefined
    aggregate_circuit_id:   used to set the agent_access_aggregation_circuit_id, e.g. test{Inc:1,1,,1}
    pon_type:               set pon type,
    remote_id:              set the remote id e.g. remte1{Inc:1,,,1}
    circuit_id:             set the circuit_id in pppoe e.g. cir{Inc:1,,,1}
    :return:
    """
    #2147483647=none 1=adsl_1 2=adsl_2 3=adsl_2_p 4=vdsl_1 5=vdsl_2 6=sdsl 8=g_fast 9=svvdsl 10=sdsl_bonded 11=vdsl_bonded 12=g_fast_bonded 13=svvdsl_bonded 0=other 14=userdefined
    pppoe_args = {}
    if 'aggregate_circuit_id' in kwargs:
        result = rt_handle.invoke('multivalue_config', pattern='string', string_pattern=kwargs['aggregate_circuit_id'])
        pppoe_args['agent_access_aggregation_circuit_id'] = result['multivalue_handle']
    if 'circuit_id' in kwargs:
        result = rt_handle.invoke('multivalue_config', pattern='string', string_pattern=kwargs['circuit_id'])
        pppoe_args['agent_circuit_id'] = result['multivalue_handle']
    if 'remote_id' in kwargs:
        result = rt_handle.invoke('multivalue_config', pattern='string', string_pattern=kwargs['remote_id'])
        pppoe_args['agent_remote_id'] = result['multivalue_handle']
    pppoe_args['handle'] = kwargs['handle']
    pppoe_args['mode'] = 'modify'
    pppoe_args['enable_client_signal_loop_char'] = '1'
    if 'dsltype' in kwargs:
        pppoe_args['dsl_type_tlv'] = kwargs['dsltype']
        #pppoe_args['pon_type_tlv'] = 'none'
    if 'pon_type' in kwargs:
        pppoe_args['pon_type_tlv'] = kwargs['pon_type']
        #pppoe_args['dsl_type_tlv'] = 'none'
    if 'upstream_rate' in kwargs:
        pppoe_args['actual_rate_upstream'] = kwargs['upstream_rate']
    if 'downstream_rate' in kwargs:
        pppoe_args['actual_rate_downstream'] = kwargs['downstream_rate']
    resp = rt_handle.invoke('pppox_config', **pppoe_args)
    if resp['status'] != '1':
        raise Exception("failed to set the pppoe ia attributes {}".format(kwargs))

def set_pppoe_tlv(rt_handle, **kwargs):
    """
    used to set the pppoe pon/dsl tlvs
    1, set/change pon/dsl tlvs
    dict1 = {'ONT/ONU-Average-Data-Rate-Downstream': '1000','ONT/ONU-Peak-Data-Rate-Downstream': '2000',
         'ONT/ONU-Maximum-Data-Rate-Upstream': '3000','ONT/ONU-Assured-Data-Rate-Upstream': '4000'}
    rt.invoke('set_pppoe_pon_tlv', handle=subs[2].rt_pppox_handle, pon_tlv_value_dict=dict1)
    dict1={'Minimum-Net-Data-Rate-Upstream':'1000', 'Minimum-Net-Data-Rate-Downstream':'2000',
     'Minimum-Net-Low-Power-Data-Rate-Upstream':'3000', 'Maximum-Interleaving-Delay-Downstream':'4000'}
    rt.invoke('set_pppoe_pon_tlv', handle=subs[2].rt_pppox_handle, dsl_tlv_value_dict=dict1)
    2, to delete tlv:
    dict2 = {'ONT/ONU-Maximum-Data-Rate-Upstream': 'disable','ONT/ONU-Peak-Data-Rate-Downstream': 'disable' }
    rt.invoke('set_pppoe_tlv', handle=subs[2].rt_pppox_handle, pon_tlv_value_dict=dict2)
    3, set circuit id
    rt.invoke('set_pppoe_tlv', handle=subs[0].rt_pppox_handle, access_loop_circuit_id='test1')
    4, set remote id
    rt.invoke('set_pppoe_tlv', handle=subs[0].rt_pppox_handle, access_loop_remote_id='remote3')
    5, set ascii
    rt.invoke('set_pppoe_tlv', handle=subs[0].rt_pppox_handle, access_aggregation_ascii='testascii')
    6, set binary
    rt.invoke('set_pppoe_tlv', handle=subs[0].rt_pppox_handle, access_aggregation_binary={'inner_vlan': '3', 'outer_vlan':'4'})
    :param rt_handle:
    handle:                    use pppox handle, e.g.subs[0].rt_pppox_handle
    access_loop_circuit_id:    circuit id
    access_loop_remote_id:     remote id
    access_aggregation_ascii:  aggregation ascii
    access_aggregation_binary: aggregation binary ditcionary, format is {'inner_vlan': '2', 'outer_vlan': '3'}
    dsl_tlv_value_dict:        dsl_tlv_value dictionary based on the tlv_default_dict keys()
    pon_tlv_value_dict:        pon_tlv_value dictionary based on the tlv_default_dict keys()
    :param kwargs:
    :return:
    """
    handle = kwargs['handle']
    if 'access_loop_circuit_id' in kwargs:
        circuit_id = kwargs['access_loop_circuit_id']
        if not hasattr(rt_handle, 'pppoe_access_loop_circuit_id'):
            rt_handle.pppoe_access_loop_circuit_id = {}
        if handle not in rt_handle.pppoe_access_loop_circuit_id:
            resp = rt_handle.invoke('tlv_config', handle=handle, mode='create_tlv',
                                    tlv_name="[01] Access-Loop-Circuit-ID", tlv_is_enabled='1', protocol='pppox_client')
            field_handle = resp[resp['tlv_value_handle']]['tlv_field_handle']
            tlv_handle = resp['tlv_handle']
            rt_handle.pppoe_access_loop_circuit_id[handle] = {'tlv_handle': tlv_handle, 'filed_handle': field_handle}
        else:
            field_handle = rt_handle.pppoe_access_loop_circuit_id[handle]['field_handle']
            tlv_handle = rt_handle.pppoe_access_loop_circuit_id[handle]['tlv_handle']
        if circuit_id != 'disable':
            rt_handle.invoke('tlv_config', mode='modify', handle=tlv_handle, tlv_is_enabled='1')
            rt_handle.invoke('tlv_config', mode='modify', handle=field_handle, field_value=circuit_id)
        else:
            rt_handle.invoke('tlv_config', mode='modify', handle=tlv_handle, tlv_is_enabled='0')

    if 'access_loop_remote_id' in kwargs:
        remote_id = kwargs['access_loop_remote_id']
        if not hasattr(rt_handle, 'pppoe_access_loop_remote_id'):
            rt_handle.pppoe_access_loop_remote_id = {}
        if handle not in rt_handle.pppoe_access_loop_remote_id:
            resp = rt_handle.invoke('tlv_config', handle=handle, mode='create_tlv',
                                    tlv_name="[02] Access-Loop-Remote-ID", tlv_is_enabled='1', protocol='pppox_client')
            field_handle = resp[resp['tlv_value_handle']]['tlv_field_handle']
            tlv_handle = resp['tlv_handle']
            rt_handle.pppoe_access_loop_remote_id[handle] = {'tlv_handle': tlv_handle, 'filed_handle': field_handle}
        else:
            field_handle = rt_handle.pppoe_access_loop_remote_id[handle]['field_handle']
            tlv_handle = rt_handle.pppoe_access_loop_remote_id[handle]['tlv_handle']
        if remote_id != 'disable':
            rt_handle.invoke('tlv_config', mode='modify', handle=tlv_handle, tlv_is_enabled='1')
            rt_handle.invoke('tlv_config', mode='modify', handle=field_handle, field_value=remote_id)
        else:
            rt_handle.invoke('tlv_config', mode='modify', handle=tlv_handle, tlv_is_enabled='0')

    if 'access_aggregation_ascii' in kwargs:
        access_ascii = kwargs['access_aggregation_ascii']
        if not hasattr(rt_handle, 'pppoe_access_aggregation_ascii'):
            rt_handle.pppoe_access_aggregation_ascii = {}
        if handle not in rt_handle.pppoe_access_aggregation_ascii:
            resp = rt_handle.invoke('tlv_config', handle=handle, mode='create_tlv',
                                    tlv_name="[03] Access-Aggregation-Circuit-ID-ASCII",
                                    tlv_is_enabled='1', protocol='pppox_client')
            field_handle = resp[resp['tlv_value_handle']]['tlv_field_handle']
            tlv_handle = resp['tlv_handle']
            rt_handle.pppoe_access_aggregation_ascii[handle] = {'tlv_handle': tlv_handle, 'filed_handle': field_handle}
        else:
            field_handle = rt_handle.pppoe_access_aggregation_ascii[handle]['field_handle']
            tlv_handle = rt_handle.pppoe_access_aggregation_ascii[handle]['tlv_handle']
        if access_ascii != 'disable':
            rt_handle.invoke('tlv_config', mode='modify', handle=tlv_handle, tlv_is_enabled='1')
            rt_handle.invoke('tlv_config', mode='modify', handle=field_handle, field_value=access_ascii)
        else:
            rt_handle.invoke('tlv_config', mode='modify', handle=tlv_handle, tlv_is_enabled='0')

    if 'access_aggregation_binary' in kwargs:
        access_bin = kwargs['access_aggregation_binary']
        if not hasattr(rt_handle, 'pppoe_access_aggregation_binary'):
            rt_handle.pppoe_access_aggregation_binary = {}
        if handle not in rt_handle.pppoe_access_aggregation_binary:
            resp = rt_handle.invoke('tlv_config', handle=handle, mode='create_tlv',
                                    tlv_name="[06] Access-Aggregation-Circuit-ID-Binary",
                                    tlv_is_enabled='1', protocol='pppox_client')
            tlv_container_handle = resp[resp['tlv_value_handle']]['tlv_container_handle']
            field_handle = resp[resp['tlv_value_handle']][tlv_container_handle]['tlv_field_handle'].split(" ")
            tlv_handle = resp['tlv_handle']
            rt_handle.pppoe_access_aggregation_binary[handle] = {'tlv_handle': tlv_handle, 'field_handle': field_handle}
        else:
            field_handle = rt_handle.pppoe_access_aggregation_binary[handle]['field_handle']
            tlv_handle = rt_handle.pppoe_access_aggregation_binary[handle]['tlv_handle']
        for item in access_bin:
            f_handle = field_handle[0] if 'inner' in item else field_handle[1]
            f_value = access_bin[item]
            if f_value != 'disable':
                rt_handle.invoke('tlv_config', mode='modify', handle=f_handle, field_value=f_value, field_is_enabled='1')
            else:
                rt_handle.invoke('tlv_config', mode='modify', handle=f_handle, field_is_enabled='0')

    tlv_dict = {}
    if 'dsl_tlv_value_dict' in kwargs:
        tlv_dict = kwargs['dsl_tlv_value_dict']
        tlv_list = ['DSL-Type', 'Actual-Net-Data-Rate-Upstream', 'Actual-Net-Data-Rate-Downstream',
                    'Minimum-Net-Data-Rate-Upstream', 'Minimum-Net-Data-Rate-Downstream',
                    'Attainable-Net-Data-Rate-Upstream', 'Attainable-Net-Data-Rate-Downstream',
                    'Maximum-Net-Data-Rate-Upstream', 'Maximum-Net-Data-Rate-Downstream',
                    'Minimum-Net-Low-Power-Data-Rate-Upstream', 'Minimum-Net-Low-Power-Data-Rate-Downstream',
                    'Maximum-Interleaving-Delay-Upstream', 'Actual-Interleaving-Delay-Upstream',
                    'Maximum-Interleaving-Delay-Downstream', 'Actual-Interleaving-Delay-Downstream',
                    'DSL-Line-State', 'Access-Loop-Line-Encapsulation',
                    'Expected-Throughput-upstream', 'Expected-Throughput-downstream',
                    'Attainable-Expected-Throughput-upstream', 'Attainable-Expected-Throughput-downstream',
                    'Gamma-data-rate-upstream', 'Gamma-data-rate-downstream',
                    'Attainable-Gamma-data-rate-upstream', 'Attainable-Gamma-data-rate-downstream', 'Custom TLV']
        if not hasattr(rt_handle, 'pppoe_dsl_tlv'):
            rt_handle.pppoe_dsl_tlv = {}
        if handle not in rt_handle.pppoe_dsl_tlv:
            resp = rt_handle.invoke('tlv_config',
                                    mode='create_tlv',
                                    handle=handle,
                                    tlv_name='DSL-Line-Attributes',
                                    tlv_is_enabled='1',
                                    protocol='pppox_client')

            rt_handle.pppoe_dsl_tlv[handle] = {'tlv_handle': resp['tlv_handle'],
                                               'tlv_value_handle': resp[resp['tlv_value_handle']]['subtlv_handle']}

    elif 'pon_tlv_value_dict' in kwargs:
        tlv_dict = kwargs['pon_tlv_value_dict']
        tlv_list = ['PON-Access-Type', 'ONT/ONU-Average-Data-Rate-Downstream', 'ONT/ONU-Peak-Data-Rate-Downstream',
                    'ONT/ONU-Maximum-Data-Rate-Upstream', 'ONT/ONU-Assured-Data-Rate-Upstream',
                    'PON-Tree-Maximum-Data-Rate-Upstream', 'PON-Tree-Maximum-Data-Rate-Downstream']
        if not hasattr(rt_handle, 'pppoe_pon_tlv'):
            rt_handle.pppoe_pon_tlv = {}

        if handle not in rt_handle.pppoe_pon_tlv:
            resp = rt_handle.invoke('tlv_config',
                                    mode='create_tlv',
                                    handle=handle,
                                    tlv_name='PON-Access-Line-Attributes',
                                    tlv_is_enabled='1',
                                    protocol='pppox_client')

            rt_handle.pppoe_pon_tlv[handle] = {'tlv_handle': resp['tlv_handle'],
                                               'tlv_value_handle': resp[resp['tlv_value_handle']]['subtlv_handle']}

    if 'all' in tlv_dict:
        value = tlv_dict['all']
        tlv_dict = {}
        for item in tlv_list:
            tlv_dict[item] = value

    for name in tlv_dict:
        if name in tlv_list:
            index = tlv_list.index(name)
            t.log("{} handle index is {}".format(name, index))
            if 'pon_tlv_value_dict' in kwargs:
                handle1 = rt_handle.pppoe_pon_tlv[handle]['tlv_handle'] + '/value/object:{}/subTlv'.format(index + 1)
            elif 'dsl_tlv_value_dict' in kwargs:
                handle1 = rt_handle.pppoe_dsl_tlv[handle]['tlv_handle'] + '/value/object:{}/subTlv'.format(index + 1)
            if tlv_dict[name] == 'disable':
                rt_handle.invoke('tlv_config', handle=handle1, mode='modify', tlv_is_enabled='0')
                continue
            rt_handle.invoke('tlv_config', handle=handle1, mode='modify', tlv_is_enabled='1')
            rt_handle.invoke('tlv_config',
                             handle=handle1 + '/value/object:1/field',
                             mode='modify', field_name='Value', field_value=tlv_dict[name], field_is_enabled='1')


def set_ancp_line_attribute(rt_handle, **kwargs):
    """
    when modify the line attribute when it is started, you need to call ancp_action to stop the ancp node first
    examples:
    rt.invoke('set_ancp_line_attribute', handle=subs[0].rt_ancp_line_handle, upstream_rate='3000',
     downstream_rate='6000', pon_type='wdmpon', circuit_id='testcir', remote_id='testremote')

    to create the aggregate_circuit_id_ascci for the first time:
    resp = rt.invoke('set_ancp_line_attribute', handle=subs[0].rt_ancp_line_handle, aggregate_circuit_id='cir1')
    {'aggregate_circuit_id_handle': '/topology:1/deviceGroup:1/networkGroup:1/dslPools:1/tlvProfile/tlv:4/value/object:1/field'}

    to modify this asscii:
     rt.invoke('set_ancp_line_attribute', handle=resp['aggregate_circuit_id_handle'], aggregate_circuit_id='cir2')

    to set the pon_tlv_value_dict:
     rt.invoke('set_ancp_line_attribute', handle=subs[1].rt_ancp_line_handle, pon_tlv_value_dict={'all':'4'})
    to modify some of the tlv value dictionary
     dict1={'PON-Tree-Maximum-Data-Rate-Upstream':'disable', 'PON-Tree-Maximum-Data-Rate-Downstream':'2000'}
     rt.invoke('set_ancp_line_attribute', handle=subs[1].rt_ancp_line_handle, pon_tlv_value_dict=dict1)
    to add new pon access tlv for teck type dsl
    rt.invoke('set_ancp_line_attribute', handle=subs[0].rt_ancp_line_handle, new_pon_access_tlv=True,
     pon_type_in_tlv='4', pon_tlv_value_dict={'all':'3'})


    :param rt_handle:
    :param kwargs:
    handle:                 mandatory, ancp line handle/ancp line field handle
    upstream_rate:          upstream rate kbps
    downstream_rate:        downstream rate kbps
    pon_type:               pon type in line config, e.g. gpon xgpon1 twdmpon xgspon wdmpon other
    dsl_type:               dsl type in line config, e.g. adsl1 adsl2 adsl2_plus vdsl1 vdsl2 sdsl unknown
    dsl_type_in_tlv:        TLV DSL Type value 0~6  ADSL1=1; ADSL2=2; ADSL2+=3; VDSL1=4; VDSL2=5; SDSL = 6; OTHER = 0
    pon_type_in_tlv:        TLV Pon Access Type 0~7  GPON=1;XG-PON1=2;TWDM-PON=3;XGS-PON=4;WDM-PON=5;OTHER=0;Unknown=7
    aggregate_circuit_id:   used to set the line agent_access_aggregation_circuit_id, e.g. test123
    remote_id:              set remote_id
    circuit_id:             set circuit_id
    dsl_tlv_value_dict:      dictionary of tlv name and value, can be {'all':value} if set all attributes to a value
    pon_tlv_value_dict:      dictionary of tlv name and value, can be {'all':value} if set all attributes to a value
    new_dsl_line_tlv:        True, will create a new tlv and return a tlv handle, used for tech_type pon to add dsl tlv
    new_pon_access_tlv:      True, will create a new tlv and return a tlv handle, used for tech_type dsl to add pon tlv
    :return:           return a dictionary if set the aggregate_circuit_id for the first time with key 'aggregate_circuit_id_handle'
    """
    line_args = {}
    resp = {}
    if 'new_pon_access_tlv' in kwargs and kwargs['new_pon_access_tlv']:
        _result_ = rt_handle.invoke('tlv_config',
                                    handle=kwargs['handle'],
                                    mode="create_tlv",
                                    tlv_name="PON-Access-Line-Attributes",
                                    tlv_is_enabled="1",
                                    tlv_include_in_messages="kPortUp",
                                    tlv_enable_per_session="1")
        resp['tlv_handle'] = _result_['tlv_handle']

    if 'new_dsl_access_tlv' in kwargs and kwargs['new_dsl_access_tlv']:
        _result_ = rt_handle.invoke('tlv_config',
                                    handle=kwargs['handle'],
                                    mode="create_tlv",
                                    tlv_name="DSL-Line-Attributes",
                                    tlv_is_enabled="1",
                                    tlv_include_in_messages="kPortUp",
                                    tlv_enable_per_session="1")
        resp['tlv_handle'] = _result_['tlv_handle']

    if 'aggregate_circuit_id' in kwargs:
        result = rt_handle.invoke('multivalue_config', pattern='string', string_pattern=kwargs['aggregate_circuit_id'])
        ascii_handle = result['multivalue_handle']
        if 'field' not in kwargs['handle']:
            result = rt_handle.invoke('tlv_config',
                                      handle=kwargs['handle'],
                                      mode='create_tlv',
                                      tlv_name="Access-Aggregation-Circuit-ID-ASCII",
                                      tlv_description="""ANCP TLV.""",
                                      tlv_include_in_messages="kPortUp",)
            t.log("create tlv for agent_access_aggregation_circuit_uid in {}".format(result))
            # tlv_2_handle = result['tlv_handle']
            value_2_handle = result['tlv_value_handle']
            # length_2_handle = result['tlv_length_handle']
            # type_2_handle = result['tlv_type_handle']
            field_handle = result[value_2_handle]['tlv_field_handle']
            resp['aggregate_circuit_id_handle'] = field_handle
        else:
            field_handle = kwargs['handle']
        result = rt_handle.invoke('tlv_config',
                                  mode='modify',
                                  field_name="Value",
                                  field_value=ascii_handle,
                                  handle=field_handle)
        if result['status'] != '1':
            raise Exception("failed to set aggregate_ascii")
        t.log("set agent_access_aggregation_circuit_uid successfully".format(result))

    if 'dsl_type_in_tlv' in kwargs or 'pon_type_in_tlv' in kwargs:
        if 'dsl_type_in_tlv' in kwargs:
            tlv_name = 'DSL-Type'
            # rt_handle.invoke('emulation_ancp_subscriber_lines_config', handle=kwargs['handle'],
            #                  enable_dsl_type='0', mode='modify')
            tlv_value = kwargs['dsl_type_in_tlv']
        elif 'pon_type_in_tlv' in kwargs:
            tlv_name = 'PON-Access-Type'
            tlv_value = kwargs['pon_type_in_tlv']
            # rt_handle.invoke('emulation_ancp_subscriber_lines_config', handle=kwargs['handle'],
            #                  enable_pon_type='1', mode='modify')
        if 'new_dsl_access_tlv' in kwargs or 'new_pon_access_tlv' in kwargs:
            type_handle = resp['tlv_handle'] + '/value/object:1/subTlv'
        elif 'tlv' in kwargs['handle']:
            type_handle = kwargs['handle'] + '/value/object:1/subTlv'
        else:
            type_handle = kwargs['handle'] + '/tlvProfile/defaultTlv:1/value/object:1/subTlv'
        rt_handle.invoke('tlv_config', handle=type_handle, mode='modify', tlv_name=tlv_name, tlv_is_enabled=1)
        value_handle = type_handle + '/value/object:1/field'
        rt_handle.invoke('tlv_config',
                         handle=value_handle,
                         mode='modify',
                         field_name='Value',
                         field_is_enabled=1,
                         field_value=tlv_value)

    if 'dsl_type' in kwargs:
        line_args['dsl_type'] = kwargs['dsl_type']
        line_args['enable_dsl_type'] = '1'
        # the below one line is commented out due to work around for ixia hot-fix (2019/05/09)
        #line_args['tech_type'] = 'dsl'
    if 'pon_type' in kwargs:
        line_args['pon_type'] = kwargs['pon_type']
        line_args['enable_pon_type'] = '1'
        # the below one line is commented out due to work around for ixia hot-fix (2019/05/09)
        #line_args['tech_type'] = 'pon'
        #line_args['dsl_type_tlv'] = 'none'
    if 'access_type' in kwargs:
        line_args['tech_type'] = kwargs['access_type']
    if 'upstream_rate' in kwargs:
        line_args['actual_rate_upstream'] = kwargs['upstream_rate']
    if 'downstream_rate' in kwargs:
        line_args['actual_rate_downstream'] = kwargs['downstream_rate']
    if 'remote_id' in kwargs:
        res1 = rt_handle.invoke('multivalue_config', pattern='string', string_pattern=kwargs['remote_id'])
        remoteid_handle = res1['multivalue_handle']
        line_args['remote_id'] = remoteid_handle
        line_args['enable_remote_id'] = '1'
    if 'circuit_id' in kwargs:
        res1 = rt_handle.invoke('multivalue_config', pattern='string', string_pattern=kwargs['remote_id'])
        circuitid_handle = res1['multivalue_handle']
        line_args['circuit_id'] = circuitid_handle
    if line_args:
        line_args['handle'] = kwargs['handle']
        line_args['mode'] = 'modify'
        result = rt_handle.invoke('emulation_ancp_subscriber_lines_config', **line_args)
        if result['status'] != '1':
            raise Exception("failed to set the ancp line attributes {}".format(kwargs))
    if 'dsl_tlv_value_dict' in kwargs or 'pon_tlv_value_dict' in kwargs:
        if 'dsl_tlv_value_dict' in kwargs:
            tlv_dict = kwargs.get('dsl_tlv_value_dict')
            tlv_list = ['Minimum-Net-Data-Rate-Upstream', 'Minimum-Net-Data-Rate-Downstream',
                        'Attainable-Net-Data-Rate-Upstream', 'Attainable-Net-Data-Rate-Downstream',
                        'Maximum-Net-Data-Rate-Upstream', 'Maximum-Net-Data-Rate-Downstream',
                        'Minimum-Net-Low-Power-Data-Rate-Upstream', 'Minimum-Net-Low-Power-Data-Rate-Downstream',
                        'Actual-Interleaving-Delay-Upstream', 'Actual-Interleaving-Delay-Downstream',
                        'Maximum-Interleaving-Delay-Upstream', 'Maximum-Interleaving-Delay-Downstream']
        if 'pon_tlv_value_dict' in kwargs:
            tlv_dict = kwargs.get('pon_tlv_value_dict')
            tlv_list = ['ONT/ONU-Average-Data-Rate-Downstream', 'ONT/ONU-Peak-Data-Rate-Downstream',
                        'ONT/ONU-Maximum-Data-Rate-Upstream', 'ONT/ONU-Assured-Data-Rate-Upstream TLV',
                        'PON-Tree-Maximum-Data-Rate-Upstream', 'PON-Tree-Maximum-Data-Rate-Downstream']
        if 'all' in tlv_dict:
            value = tlv_dict['all']
            tlv_dict = {}
            for item in tlv_list:
                tlv_dict[item] = value

        for name in tlv_dict:
            if name in tlv_list:
                index = tlv_list.index(name) + 1
                if 'new_dsl_access_tlv' in kwargs or 'new_pon_access_tlv' in kwargs:
                    handle1 = resp['tlv_handle'] + '/value/object:{}/subTlv'.format(index + 1)
                elif 'tlv' in kwargs['handle']:
                    handle1 = kwargs['handle'] + '/value/object:{}/subTlv'.format(index + 1)
                else:
                    handle1 = kwargs['handle'] + '/tlvProfile/defaultTlv:1/value/object:{}/subTlv'.format(index + 1)
                if tlv_dict[name] == 'disable':
                    rt_handle.invoke('tlv_config', handle=handle1, tlv_name=name, mode='modify', tlv_is_enabled='0')
                    continue
                rt_handle.invoke('tlv_config', handle=handle1, tlv_name=name, mode='modify', tlv_is_enabled='1')
                rt_handle.invoke('tlv_config',
                                 handle=handle1 + '/value/object:1/field',
                                 mode='modify', field_name='Value', field_value=tlv_dict[name], field_is_enabled='1')

    return resp


def set_ancp_rate(rt_handle, **kwargs):
    """Set ANCP rates.

    Usage:
        Keyword example usage:
        {rt_handle}=    Get handle    resource=rt0
        Execute Tester Command    ${rt_handle}
        ...                       command=set_ancp_rate
        ...                       global_start_rate=200
        ...                       global_start_rate_max_outstanding=1000
        ...                       global_stop_rate=200
        ...                       global_stop_rate_max_outstanding=1000
        ...                       global_port_up_rate=200
        ...                       global_port_up_rate_max_outstanding=1000
        ...                       global_port_down_rate=200
        ...                       global_port_down_rate_max_outstanding=1000

    :param rt_handle: RT object, mandatory
    :param kwargs:
        global_start_rate:                      global start rate
        global_start_rate_max_outstanding:      global start rate outstanding
        global_start_rate_interval:             global start rate interval, unit is ms
        global_start_rate_scale_mode:           global start rate scale mode, <device_group|port>

        global_stop_rate:                       global stop rate
        global_stop_rate_max_outstanding:       global stop rate outstanding
        global_stop_rate_interval:              global stop rate interval, unit is ms
        global_stop_rate_scale_mode:           global stop rate scale mode, <device_group|port>

        global_port_up_rate:                    global port up rate
        global_port_up_rate_interval:           global port up rate interval, unit is ms
        global_port_up_rate_max_outstanding:    global port up rate max outstanding, defualt 400
        global_port_up_rate_scale_mode:         global port up rate scale mode, <device_group|port>

        global_port_down_rate:                  global port down rate
        global_port_down_rate_interval:         global port down rate interval, unit is ms
        global_port_down_rate_max_outstanding:  global port down rate max outstanding
        global_port_down_rate_scale_mode:       global port down down rate scale mode, <device_group|port>

    :return: None if operation succeeds.
    :raises: Exception if operation fails.
    """
    # Supported parameters for this function
    supported_p = {'global_start_rate': None,
                   'global_start_rate_max_outstanding': None,
                   'global_start_rate_interval': None,
                   'global_start_rate_scale_mode': None,
                   'global_stop_rate': None,
                   'global_stop_rate_max_outstanding': None,
                   'global_stop_rate_interval': None,
                   'global_stop_rate_scale_mode': None,
                   'global_port_up_rate': None,
                   'global_port_up_rate_max_outstanding': None,
                   'global_port_up_rate_interval': None,
                   'global_port_up_rate_scale_mode': None,
                   'global_port_down_rate': None,
                   'global_port_down_rate_max_outstanding': None,
                   'global_port_down_rate_interval': None,
                   'global_port_down_rate_scale_mode' : None}

    for k, v in kwargs.items():
        if k not in supported_p:
            raise Exception("Invalid parameter {}".format(k))
        else:
            supported_p[k] = v

    ancp_rate_args = {k: v for k, v in supported_p.items() if v is not None}
    ancp_rate_args['handle'] = "/globals"
    ancp_rate_args['mode'] = 'modify'

    result = rt_handle.invoke('emulation_ancp_config', **ancp_rate_args)

    if result['status'] != '1':
        raise Exception("Failed to set ANCP rates {}".format(ancp_rate_args))

    t.log("Set ANCP rate done")


def set_ancp_access_type(rt_handle, **kwargs):
    """Set ANCP dsl and pon access types.

    Usage:
        Keyword example usage:
        # suppose cfg.yaml defines tag ancp_sub_group_1 for a group of subscribers.
        ${a_sub_handle}=    Get Subscriber Handle    tag=ancp_sub_group_1
        Execute Tester Command    ${rt_handle}
        ...                       command=set_ancp_access_type
        ...                       handle=${a_sub_handle[0].rt_ancp_line_handle}
        ...                       enable_dsl_type=${True}
        ...                       enable_pon_type=${False}
        ...                       tech_type=dsl

    :param rt_handle: RT object, mandatory
    :param kwargs:
        handle:             ancp line handle, mandatory
        enable_dsl_type:    boolean, True to enable dsl type, False to disable dsl type.
        enable_pon_type:    boolean, True to enable pon type, False to disable pon type.
        tech_type:          string, <dsl|pon>.
    :return: None if operation succeeds.
    :raises: Exception if operation fails.
    """

    # aat: ancp access type
    aat_args = dict()
    aat_args['handle'] = kwargs.get('handle')
    aat_args['mode'] = 'modify'

    if 'enable_dsl_type' in kwargs:
        if kwargs.get('enable_dsl_type'):
            aat_args['enable_dsl_type'] = 'true'
        else:
            aat_args['enable_dsl_type'] = 'false'

    if 'enable_pon_type' in kwargs:
        if kwargs.get('enable_pon_type'):
            aat_args['enable_pon_type'] = 1
        else:
            aat_args['enable_pon_type'] = 0

    tech_type = kwargs.get('tech_type', None)
    if tech_type:
        assert tech_type == 'dsl' or tech_type == 'pon'
        aat_args['tech_type'] = tech_type

    result = rt_handle.invoke('emulation_ancp_subscriber_lines_config', **aat_args)

    if result['status'] != '1':
        raise Exception("Failed to set ANCP access type {}".format(aat_args))

    t.log("Set ANCP access type done")


def j_add_evpn_node(rt_handle, **kwargs):
    """
    used to add EVPN simulation
    resp = rt.invoke('j_add_evpn_node', port='6/10',connect_ip='10.5.1.2', connect_gateway='10.5.1.1', connect_vlan='512', dut_count=2,dut_loop_ip='100.100.100.253', rr_loop_ip='100.100.100.1', evpn_mode='multihome', evi_count=3)
    resp = rt.invoke('j_add_evpn_node', port='6/10',connect_ip='10.5.1.2', connect_gateway='10.5.1.1', connect_vlan='512', dut_loop_ip='100.100.100.253', dut_count=2, rr_loop_ip='100.100.100.1', evi_count=3)
    :param rt_handle:
    :param kwargs:
    port:      port used to simulate evpn
    connect_ip:     ip address connect to router reflector
    connect_netmask:    netmask of ip
    connect_gateway:    ip address of router reflect
    connect_vlan:     vlan for the connection, default is None
    connect_protocol:     default is ospf
    label_protocol:       default is rsvp
    node_count:           simulated pe count, default is 1 for single home and 2 for multihome
    rr_loop_ip:            router reflector loop ip
    dut_count:             dut counts (1 means singlehome, 2 means multihome)
    dut_loop_ip:           dut loopback start ip
    as_number:             AS number, default is 65221
    evi_count:             evpn instance count, default is 1
    evpn_mode:             singlehome/multihome
    mac_count:             mac_count per evi
    evpn_vlan_start:       evpn vlan start id
    :return:
    """
    result = {}
    evpn_mode = kwargs.get('evpn_mode', 'singlehome')
    connect_vlan = kwargs.get('connect_vlan', None)
    connect_args = {}
    connect_args['port'] = kwargs['port']
    connect_args['ip_addr'] = kwargs['connect_ip']
    connect_args['netmask'] = kwargs.get('connect_netmask', '255.255.255.0')
    connect_args['gateway'] = kwargs['connect_gateway']
    if connect_vlan:
        connect_args['vlan_start'] = connect_vlan
    #add link connection and protocol
    resp = rt_handle.invoke('add_link', **connect_args)
    connect_v4_handle = resp['ipv4_handle']
    connect_dev_handle = resp['device_group_handle']
    result['device_group_handle'] = connect_dev_handle
    result['status'] = resp['status']
    link_protocol = kwargs.get('connect_protocol', 'ospf')
    v4_addr = ipaddress.IPv4Interface(kwargs['rr_loop_ip'])
    rr_loop_ip = str(v4_addr.ip)
    protocol_router_id = str(v4_addr.ip + 1)
    protocol_start_ip = str(v4_addr.ip + 2)
    protocol_args = {}
    if link_protocol == 'ospf':
        ospf_args = {}
        ospf_args['handle'] = connect_v4_handle
        ospf_args['router_id'] = protocol_router_id
        ospf_args['area_id_as_number'] = 0
        ospf_args['te_enable'] = 1
        ospf_args['network_type'] = 'broadcast'
        resp = rt_handle.invoke('emulation_ospf_config', **ospf_args)
        protocol_handle = resp['ospfv2_handle']
    ##add network group for protocol simulation
    protocol_args['protocol_handle'] = connect_dev_handle
    protocol_args['type'] = 'ipv4-prefix'
    protocol_args['ipv4_prefix_network_address'] = protocol_start_ip
    protocol_args['ipv4_prefix_length'] = 32
    protocol_args['ipv4_prefix_address_step'] = 1
    node_count = kwargs.get('node_count', 1)
    if evpn_mode == 'multihome':
        node_count = int(node_count) * 2
    protocol_args['ipv4_prefix_number_of_addresses'] = node_count
    resp = rt_handle.invoke('network_group_config', **protocol_args)
    network_handle = resp['network_group_handle']
    ##config bgp device and evi

    resp = rt_handle.invoke('add_device_group', device_group_handle=network_handle, device_count=node_count)
    dev2_handle = resp['device_group_handle']
    resp = rt_handle.invoke('multivalue_config',
                            pattern='counter',
                            counter_start=protocol_start_ip,
                            counter_step='0.0.0.1',
                            counter_direction='increment')
    mv1 = resp['multivalue_handle']
    interface_args = {}
    interface_args['protocol_handle'] = dev2_handle
    interface_args['enable_loopback'] = 1
    interface_args['intf_ip_addr'] = mv1
    interface_args['netmask'] = '255.255.255.255'
    interface_args['connected_to_handle'] = network_handle
    resp = rt_handle.invoke('interface_config', **interface_args)
    loop_handle = resp['ipv4_loopback_handle']

    dut_loop_ip = kwargs.get('dut_loop_ip')
    dut_count = kwargs.get('dut_count', 1)
    #config rsvp
    label_protocol = kwargs.get('label_protocol', 'rsvp')
    if label_protocol.lower() == 'rsvp':
        resp = rt_handle.invoke('emulation_rsvp_tunnel_config', handle=loop_handle, mode='create', p2p_ingress_lsps_count=dut_count)
        lsp_handle = resp['rsvpte_lsp_handle']
        lsp_ingress = lsp_handle + '/rsvpP2PIngressLsps'
        dut_mv1 = rt_handle.invoke('_add_addr_custom_pattern', start=dut_loop_ip, step='0.0.0.1', count=dut_count)
        resp = rt_handle.invoke('emulation_rsvp_tunnel_config', handle=lsp_ingress, mode='modify', remote_ip=dut_mv1)
    if label_protocol.lower() == 'ldp':
        ldp_args = {}
        ldp_args['mode'] = 'create'
        ldp_args['handle'] = connect_v4_handle
        ldp_args['router_active'] = 1
        ldp_args['interface_active'] = 1
        ldp_args['lsr_id'] = protocol_router_id
        resp = rt_handle.invoke('emulation_ldp_config', **ldp_args)
        ldp_router_handle = resp['ldp_basic_router_handle']
        ldp_intf_handle = resp['ldp_connected_interface_handle']

    # config bgp
    evi_count = kwargs.get('evi_count', '1')
    bgp_args = {}
    bgp_args['mode'] = 'enable'
    bgp_args['handle'] = loop_handle
    bgp_args['ip_version'] = 4,
    bgp_args['remote_ip_addr'] = rr_loop_ip
    bgp_args['local_as'] = kwargs.get('as_number', '65221')
    bgp_args['neighbor_type'] = 'internal'
    bgp_args['filter_evpn'] = '1'
    bgp_args['local_router_id'] = mv1
    bgp_args['router_id'] = mv1

    if 'irb_enable' in kwargs:
        irb_addr = kwargs['irb_addr_start']
        irb_step = '0.0.1.0'
        mv_irb = rt_handle.invoke('_add_addr_custom_pattern', start=irb_addr, step=irb_step, count=evi_count)
        bgp_args['irb_ipv4_address'] = mv_irb
        irb_interface_label = kwargs.get('irb_interface_label', '16')

    resp = rt_handle.invoke('emulation_bgp_config', **bgp_args)
    bgp_handle = resp['bgp_handle']
    result['status'] = resp['status']
    resp = rt_handle.invoke('emulation_bgp_route_config', handle=bgp_handle, mode='create', evpn=1)
    evi_handle = resp['evpn_evi']
    result['status'] = resp['status']
    result['bgp_handle'] = bgp_handle
    result['evi_handle'] = evi_handle

    if evpn_mode == 'multihome':
        bgp_mh_args = {}
        bgp_mh_args['handle'] = bgp_handle
        bgp_mh_args['evis_count'] = evi_count
        bgp_mh_args['mode'] = 'modify'
        if 'esi_type' in kwargs:
            bgp_mh_args['esi_type'] = kwargs['esi_type']
        bgp_mh_args['esi_value'] = kwargs.get('esi_value', '010203040506070809')
        bgp_mh_args['support_multihomed_es_auto_discovery'] = '1'
        bgp_mh_args['support_fast_convergence'] = '1'
        if 'esi_count' in kwargs:
            bgp_mh_args['active_ethernet_segment'] = kwargs['esi_count']
        if 'single_active' in kwargs:
            bgp_mh_args['enable_single_active'] = kwargs['single_active']
        if 'use_control_word' in kwargs:
            bgp_mh_args['use_control_word'] = kwargs['use_control_word']
        rt_handle.invoke('emulation_bgp_config', **bgp_mh_args)
        ###using low level API to config aliasing
        handle = bgp_handle + '/bgpEthernetSegmentV4'
        low_hdl = rt_handle._invokeIxNet('getAttribute', handle, '-advertiseAliasingAutomatically')
        value_hdl = low_hdl + '/singleValue'
        rt_handle._invokeIxNet('setAttribute', value_hdl, '-value', 1)
        rt_handle._invokeIxNet('commit')
    if evpn_mode == 'singlehome':
        bgp_sh_args = {}
        bgp_sh_args['handle'] = bgp_handle
        bgp_sh_args['evis_count'] = evi_count
        bgp_sh_args['mode'] = 'modify'
        bgp_sh_args['esi_value'] = '000000000000000000'
        if 'use_control_word' in kwargs:
            bgp_sh_args['use_control_word'] = kwargs['use_control_word']
        rt_handle.invoke('emulation_bgp_config', **bgp_sh_args)

    target_start = kwargs.get('target_start', '1')
    t_repeat = kwargs.get('target_repeat', '1')
    target_mv = rt_handle.invoke('_set_custom_pattern', start=target_start, step=1, repeat=t_repeat, count=evi_count)
    rd_start = kwargs.get('rd_start', '1')
    evi_rd_mv = rt_handle.invoke('_set_custom_pattern', start=rd_start, step=1, repeat=t_repeat, count=evi_count)
    evpn_vlan_start = kwargs.get('evpn_vlan_start', '1')
    vlan_length = 4000 if int(evi_count) > 4000 else evi_count
    vlan_id_mv = rt_handle.invoke('_set_custom_pattern', start=evpn_vlan_start, step=1, repeat=1, count=vlan_length)
    label_mv = rt_handle.invoke('_set_custom_pattern', start=16, step=1, repeat=1, count=evi_count)
    bgp_route_args = {}
    bgp_route_args['handle'] = evi_handle
    bgp_route_args['mode'] = 'modify'
    bgp_route_args['enable_vlan_aware_service'] = kwargs.get('evpn_vlan_enable', '1')
    bgp_route_args['no_of_mac_pools'] = kwargs.get('mac_pool_count', '1')
    bgp_route_args['export_rt_as_number'] = kwargs.get('export_rt_as_no', '100')
    bgp_route_args['export_rt_type'] = 'as'
    bgp_route_args['export_rt_assigned_number'] = target_mv
    bgp_route_args['rd_evi'] = evi_rd_mv
    bgp_route_args['ethernet_tag_id'] = vlan_id_mv
    bgp_route_args['upstream_downstream_assigned_mpls_label'] = label_mv
    rt_handle.invoke('emulation_bgp_route_config', **bgp_route_args)

    ###config mac pools
    mac_start = kwargs.get('mac_start', 'a0:10:00:00:00:01')
    outstep = "00:00:00:00:00:00"
    mac_step = "00:00:00:01:00:00"

    mac_pool_mv = rt_handle.invoke('_add_addr_custom_pattern', start=mac_start, outstep=outstep, step=mac_step,
                                   count=evi_count)
    mac_pool_args = {}
    mac_pool_args['connected_to_handle'] = evi_handle
    mac_pool_args['protocol_handle'] = dev2_handle
    mac_pool_args['type'] = kwargs.get('mac_pool_type', 'mac-pools')
    mac_pool_args['mac_pools_number_of_addresses'] = kwargs.get('mac_count', '1')
    mac_pool_args['mac_pools_prefix_length'] = '48'
    mac_pool_args['mac_pools_use_vlans'] = kwargs.get('pool_use_vlan', '1')
    mac_pool_args['mac_pools_mac'] = mac_pool_mv
    mac_pool_args['mac_pools_vlan_count'] = kwargs.get('vlan_count', '1')
    mac_pool_args['mac_pools_vlan_id'] = vlan_id_mv
    dual_vlan = kwargs.get('evpn_svlan_start', None)
    if dual_vlan:
        svlan_id_mv = rt_handle.invoke('_set_custom_pattern', start=dual_vlan, step=1, repeat=vlan_length, count=evi_count)
        mac_pool_args['mac_pools_vlan_id'] = "{},{}".format(svlan_id_mv, vlan_id_mv)
        #mac_pool_args['mac_pools_vlan_tpid'] = "{},{}".format('0x8100', '0x8100')
        mac_pool_args['mac_pools_vlan_count'] = '2'
    if 'evpn_ipv4_start' in kwargs and 'evpn_ipv6_start' in kwargs:
        mac_pool_args['type'] = 'mac-dual-stack-prefix'
        mac_pool_args['ipv4_prefix_network_address'] = kwargs.get('evpn_ipv4_start', '200.0.0.1')
        mac_pool_args['ipv4_prefix_network_address_step'] = "0.1.0.0"
        mac_pool_args['ipv6_prefix_network_address'] = kwargs.get('evpn_ipv6_start', '3000:0:1:1::1')
        mac_pool_args['ipv6_prefix_network_address_step'] = "0:0:1:0:0:0:0:0"
    elif 'evpn_ipv4_start' in kwargs:
        mac_pool_args['type'] = 'mac-ipv4-prefix'
        mac_pool_args['ipv4_prefix_network_address'] = kwargs.get('evpn_ipv4_start', '200.0.0.1')
        mac_pool_args['ipv4_prefix_network_address_step'] = "0.1.0.0"
    elif 'evpn_ipv6_start' in kwargs:
        mac_pool_args['type'] = 'mac-ipv6-prefix'
        mac_pool_args['ipv6_prefix_network_address'] = kwargs.get('evpn_ipv6_start', '3000:0:1:1::1')
        mac_pool_args['ipv6_prefix_network_address_step'] = "0:0:1:0:0:0:0:0"

    resp = rt_handle.invoke('network_group_config', **mac_pool_args)
    result['mac_pools_handle'] = resp['mac_pools_handle']
    result['status'] = resp['status']
    tag_mv = rt_handle.invoke('_set_custom_pattern', start=1, step=1, repeat=1, count=evi_count)
    rt_handle.invoke('traffic_tag_config', handle=resp['mac_pools_handle'], enabled='1', name="TAG", id=tag_mv)
    return result

def add_lag(rt_handle, **kwargs):
    """
    Add lag emulation
    :param rt_handle:
    :param kwargs:
    port_list:
    :return:
    """
    handles = dict()
    #_result_ = rt_handle.invoke('emulation_lag_config', mode='create', lag_name='ae1', port_handle=['/vport:1', '/vport:2'], protocol_type='lag_port_lacp')
    port_list = kwargs['port_list']
    port_handle_list = []
    for port in port_list:
        index = rt_handle.port_list.index(port)
        index += 1
        vport = '/vport:' + str(index)
        port_handle_list.append(vport)
    #port handle list (must be in format ['/vport:1', '/vport:2'])
    result = rt_handle.invoke('emulation_lag_config', mode='create', port_handle=port_handle_list, protocol_type='lag_port_lacp')
    lag_1_handle = result['lag_handle']
    return lag_1_handle
