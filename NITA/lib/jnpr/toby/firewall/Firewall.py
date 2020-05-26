'''
Created on Sep 26, 2016
@author: Terralogic Team
'''
import time
import re
import datetime
import xml.etree.ElementTree as ET
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hldcl.device import Device
import logging


config_arr = []
cmd = dict(
    set_fw_bandwidth_limit='set firewall policer %s if-exceeding ' +
                           'bandwidth-limit %s',
    set_bw_percent='set firewall policer %s if-exceeding ' +
                   'bandwidth-percent %s',
    set_fw_burst_size='set firewall policer %s ' +
                      'if-exceeding burst-size-limit %s',
    set_fw_action='set firewall policer %s then %s',
    set_rpf_feasible='set routing-options forwarding-table ' +
                     'unicast-reverse-path feasible-paths',
    set_acc_scu='%s interfaces %s unit %s family %s ' +
                'accounting source-class-usage',
    set_scu='%s interfaces %s unit %s family %s source-class-usage',
    set_sampling='%s interfaces %s unit %s family %s sampling',
    set_fw_filter='%s interfaces %s unit %s family %s',
    clear_filter_counter='clear firewall filter %s counter %s',
    clear_filter='clear firewall filter %s',
    clear_firewall_all='clear firewall all',
    set_from_prot='set policy-options policy-statement dcu ' +
                  'from protocol %s',
    set_des_class='set policy-options policy-statement dcu ' +
                  'then destination-class %s',
    set_forwarding_table='set routing-options forwarding-table ' +
                         'export %s',
    set_scu_from_prot='set policy-options policy-statement ' +
                      'scu from protocol %s',
    set_scu_source_class='set policy-options policy-statement ' +
                         'scu then source-class %s',
    set_scu_forwarding_table='set routing-options ' +
                             'forwarding-table export %s',
    show_fw_pre_action='show firewall prefix-action-stats ' +
                       'filter %s prefix-action %s from %s to %s',
    set_policer='%s interfaces %s unit %s family %s policer',
    show_dcu='show interfaces destination-class %s %s',
    show_scu='show interfaces source-class %s %s',
    deacti_rpf="%s routing-options forwarding-table",
    del_rpf_feasible="%s routing-options forwarding-table " +
    'unicast-reverse-path feasible-paths')


def function_name():
    '''
    To get the fucntion name.
    :returns:
    The function name
    '''
    import traceback
    return traceback.extract_stack(None, 2)[0][2]


def check_args(valid_key, required_key, kw_dict):
    '''
        -Check all value in valid_key list is existed in kw_dict
        -Check all value in requred_key list is existed
        in kw_dict and it is defined

      :param valid_key:
        REQUIRED the list of valid keys need to be checked (list)
      :param required_key:
        REQUIRED the list of required keys need to be checked (list)
      :param kw_dict:
        REQUIRED all arguments need to be checked  (dict)

       :return:
        kw_dict: all arguments
        Eg:
            valid_keys = ['name', 'family', 'term', 'match','action'
            ,'if_specific', 'commit']
            required_key = ['name', 'term']
            kwargs = check_args(valid_keys, required_key, kwargs)
    '''
    # Check valid_value in kwargs
    for current_key in kw_dict.keys():
        if current_key not in valid_key:
            raise Exception("%s value is not valid" % current_key)
    # Check all value in required_key list is existed
    for required_k in required_key:
        if required_k not in valid_key or kw_dict[required_k] == '':
            raise Exception("%s value is not defined" % required_k)
    return kw_dict


def configure_firewall_filter(device, **kwargs):
    '''
        Configure firewall filter by doing the following actions:
        - Enable interface-specific instances of the filter
        - Configure the match conditions for the term.
        - If match conditions is not defined, configure the actions
        for the term.
        - Commit

      :param name:
        REQUIRED filter name (string)
      :param filter_type
        OPTIONAL the filter type. Eg: filter, simple-filter, service-filter.
        Default: filter
      :param family:
        OPTIONAL the name of instance (string), Eg: inet.

      :param enhanced_mode:
        OPTIONAL Define filter for chassis network-services enhanced mode.
        True or False. Default: False
      :param enhanced_mode_override:
        OPTIONAL Override the default chassis network-services enhanced mode
        for dynamic filter. True or False. Default: False
      :param fast_lookup_filter:
        OPTIONAL Configure filter in the fast lookup hardware block.
        True or False. Default: False
      :param instance_shared:
        OPTIONAL Filter is routing-instance shared. True or False.
        Default: False
      :param interface_shared:
        OPTIONAL Filter is interface-shared. True or False. Default: False
      :param physical_interface_filter:
        OPTIONAL Filter is interface-shared. True or False. Default: False
      :param interface_specific:
        OPTIONAL Defined counters are interface specific. True or False.
        Default: False

      :param term:
        REQUIRED the match conditions for the term (string)
      :param match:
        OPTIONAL the list of match conditions in from statement (list)
      :param action:
        OPTIONAL the list of actions for the term in then statement (list)
        this option will be used if match option is not defined
      :param commit:
        OPTIONAL if commit value is defined, will commit the configuration
        to device

       :return:
        TRUE: if no error occurred
        FALSE: if error occurred

        Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${match} =    Create List    protocol udp    port 5060
        ${action} =    Create List   next term     dscp cs4
        ${result} =    Configure Firewall Filter    device=${dev}
        ...    name=VOIP-COS1    family=inet    term=SIP
        ...    match=${match}    action=${action}    commit=True

    '''
    # Check parameter
    valid_keys = ['name', 'filter_type', 'enhanced_mode',
                  'enhanced_mode_override', 'fast_lookup_filter',
                  'instance_shared', 'interface_shared', 'interface_specific',
                  'physical_interface_filter', 'family', 'term', 'match',
                  'action', 'commit']
    required_key = ['name']
    kwargs = check_args(valid_keys, required_key, kwargs)
    name = kwargs.get('name', 'term')
    filter_type = kwargs.get('filter_type', 'filter')

    enhanced_mode = kwargs.get('enhanced_mode', False)
    enhanced_mode_override = kwargs.get('enhanced_mode_override', False)
    fast_lookup_filter = kwargs.get('fast_lookup_filter', False)
    instance_shared = kwargs.get('instance_shared', False)
    interface_specific = kwargs.get('interface_specific', False)
    physical_interface_filter = kwargs.get('physical_interface_filter', False)
    interface_shared = kwargs.get('interface_shared', False)

    family = kwargs.get('family')
    term = kwargs.get('term')
    match = kwargs.get('match')
    action = kwargs.get('action')
    commit = kwargs.get('commit')
    command_list = []
    if not match and not action:
        device.log(message="match value and action value is not defined",
                   level='error')
        return False
    else:
        if match:
            if not isinstance(match, list):
                match = [match]
        if action:
            if not isinstance(action, list):
                action = [action]

    # Call put_log
    logging.info(msg="Inside %s function" % function_name())

    cfg_cmd = "set firewall"
    if family:
        cfg_cmd = "%s family %s" % (cfg_cmd, family)
    if enhanced_mode:
        cfg_enhanced_mode = "%s enhanced-mode" % cfg_cmd
        command_list.append(cfg_enhanced_mode)
    if enhanced_mode_override:
        cfg_enhanced_mode_override = "%s enhanced-mode-override" % cfg_cmd
        command_list.append(cfg_enhanced_mode_override)
    if fast_lookup_filter:
        cfg_fast_lookup_filter = "%s fast-lookup-filter" % cfg_cmd
        command_list.append(cfg_fast_lookup_filter)
    if interface_shared:
        cfg_interface_shared = "%s interface-shared" % cfg_cmd
        command_list.append(cfg_interface_shared)
    if instance_shared:
        cfg_instance_shared = "%s instance-shared" % cfg_cmd
        command_list.append(cfg_instance_shared)
    if interface_specific:
        cfg_interface_specific = "%s interface-specific" % cfg_cmd
        command_list.append(cfg_interface_specific)
    if physical_interface_filter:
        cfg_physical_if_filter = "%s physical-interface-filter" % cfg_cmd
        command_list.append(cfg_physical_if_filter)

    cfg_cmd = "%s %s %s term %s" % (cfg_cmd, filter_type, name, term)
    if match:
        for match_value in match:
            cfg_cmd_match = cfg_cmd
            cfg_cmd_match = "%s from %s" % (cfg_cmd_match, match_value)
            command_list.append(cfg_cmd_match)
    if action:
        for act in action:
            cfg_cmd_action = cfg_cmd
            cfg_cmd_action = "%s then %s" % (cfg_cmd_action, act)
            command_list.append(cfg_cmd_action)

    result = device.config(command_list=command_list).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s"
                   % result, level='error')
        return False
    if commit:
        return device.commit().status()
    return True


def configure_firewall_psa(device, **kwargs):
    '''
        Configure firewall prefix-specific action by doing the
        following actions:
        - configure firewall prefix specific action:

        [edit firewall family inet]
        prefix-action prefix-action-name {
            count;
            destination-prefix-length prefix-length;
            filter-specific;
            policer policer-name;
            source-prefix-length prefix-length;
            subnet-prefix-length prefix-length;
        }
        - commit
        :param name:
            REQUIRED prefix-action-name (string)
        :param family:
            OPTIONAL the name of instance (string). If family value is
            not defined, the value is 'inet'
        :param count:
            OPTIONAL If 'count' value is defined, counter will be enabled
        :param policer:
            OPTIONAL the name of policer (string).
        :param filter_specific:
            OPTIONAL If 'filter_specific' value is defined, filter
            specific will be enabled
        :param destination_prefix_length:
            OPTIONAL the name of destination prefix length (string)
        :param source_prefix_length:
            OPTIONAL the name of source prefix length (string)
        :param subnet_prefix_length:
            OPTIONAL the name of subnet prefix length (string)
        :param commit:
            OPTIONAL if commit value is defined, will commit the
            configuration to device

       :return:
        TRUE: if no error occurred
        FALSE: if error occurred

        Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        Configure Firewall Policer    device=${dev}    name=1Mbps-policer
         ...    bw_limit=1m    burst_size=63k    action=discard    commit=1
        ${result} =    Configure Firewall Psa    device=${dev}
        ...    name=psa-1Mbps-per-source-24-32-256-1
        ...    count=1    policer=1Mbps-policer    source_prefix_length=32
        ...    subnet_prefix_length=24    commit=True


    '''
    # Check parameter
    valid_keys = ['name', 'family', 'count', 'policer', 'filter_specific',
                  'destination_prefix_length', 'source_prefix_length',
                  'subnet_prefix_length', 'commit']
    required_key = ['name']

    kwargs = check_args(valid_keys, required_key, kwargs)

    name = kwargs.get('name')
    family = kwargs.get('family', 'inet')
    count = kwargs.get('count')
    filter_specific = kwargs.get('filter_specific')
    dest_pfx_len = kwargs.get('destination_prefix_length')
    src_pfx_len = kwargs.get('source_prefix_length')
    policer = kwargs.get('policer')
    subnet_pfx_len = kwargs.get('subnet_prefix_length')
    commit = kwargs.get('commit')

    # sub=function_name()
    function = function_name()
    # call put_log from jt
    logging.info(msg="Inside %s function" % function)

    cfg_cmd = "set firewall family " + family + " prefix-action " + name
    if count:
        cfg_cmd += " count "
    if filter_specific:
        cfg_cmd += " filter-specific "
    if dest_pfx_len:
        dest_pfx_len = kwargs['destination_prefix_length']
        cfg_cmd += " destination-prefix-length " + dest_pfx_len
    if src_pfx_len:
        src_pfx_len = kwargs['source_prefix_length']
        cfg_cmd += " source-prefix-length " + src_pfx_len
    if policer:
        policer = kwargs['policer']
        cfg_cmd += " policer " + policer
    if subnet_pfx_len:
        subnet_pfx_len = kwargs['subnet_prefix_length']
        cfg_cmd += " subnet-prefix-length " + subnet_pfx_len

    result = device.config(command_list=[cfg_cmd]).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s"
                   % result, level='error')
        return False

    if commit:
        return device.commit().status()
    return True


def configure_prefix_list(device, **kwargs):
    '''
        Configure firewall prefix-specific action by doing the
        following actions:
        - configure prefix list
        - commit

        :param name:
            REQUIRED name of prefix-list (string)
        :param list:
            REQUIRED the list of prefix (list).
        :param commit
            OPTIONAL if commit value is defined, will commit
            the configuration to device

       :return:
        TRUE: if no error occurred
        FALSE: if error occurred

        Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${list_subnet} =    Create List    172.16.1.16/28    172.16.1.32/28
        ...    172.16.1.48/28
        ${result} =    Configure Prefix List    device=${dev}    name=customers
        ...    list=${list_subnet}    commit=True

    '''
    # Check parameter
    valid_keys = ['name', 'list', 'commit']
    required_key = ['name', 'list']

    kwargs = check_args(valid_keys, required_key, kwargs)

    name = kwargs.get('name')
    list_prefix = kwargs.get('list')
    commit = kwargs.get('commit')

    function = function_name()
    # call put_log from jt
    logging.info(msg="Inside %s function" % function)

    if not isinstance(list_prefix, list):
        list_prefix = [list_prefix]

    policy_option = "set policy-options prefix-list %s" % name
    for prefix in list_prefix:
        cfg_cmd = "%s %s" % (policy_option, prefix)
        result = device.config(command_list=[cfg_cmd]).response()
        if re.search(r'invalid|error', result, re.IGNORECASE):
            device.log(message="Config set failed on device: %s"
                       % result, level='error')
            return False

    if commit:
        return device.commit().status()
    return True


def get_rpf_counter(device, **kwargs):
    '''
        Get Unicast reverse-path forwarding (RPF) counter
        by doing the following actions:
        - show interfaces extensive by xml format
        - Get 'route-rpf-packets' and 'route-rpf-bytes'
        in route-rpf-statistics

        :param interface:
            REQUIRED name of interface (string).
        :return:
            rpf_counter (dict).
            Eg: route-rpf-packets value: rpf_counter['packets'];
            route-rpf-bytes value: rpf_counter['bytes']

        Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Rpf Counter    device=${dev}    interface=xe-0/0/0.1

    '''
    # Check parameter
    valid_keys = ['interface']
    required_key = ['interface']

    kwargs = check_args(valid_keys, required_key, kwargs)

    interface = kwargs.get('interface')

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)
    rpf_counter = {}

    if isinstance(interface, list):
        for i in interface:
            rpf_counter[i] = get_rpf_counter(device, interface=i)
        device.log(message="%s: if(%s) return" % (function, interface) + " " +
                   str(rpf_counter), level='debug')
        return rpf_counter

    cmd = "show interfaces extensive " + interface
    try:
        rpc_str = device.get_rpc_equivalent(command=cmd)
        response = device.execute_rpc(command=rpc_str).response()
    except:
        device.log(message="Get response from %s failed on device" % interface,
                   level='error')
        return rpf_counter

    route_rpf_xml = ".//logical-interface/address-family/" + \
        "route-rpf-statistics"
    if response.find(route_rpf_xml) is not None:
        rpf_counter['packets'] = response.find(
            ".//route-rpf-packets").text.strip()
        rpf_counter['bytes'] = response.find(
            ".//route-rpf-bytes").text.strip()
    return rpf_counter


def get_firewall_psc(device, **kwargs):
    '''
        Get firewall prefix specific action counter by doing the following
        actions:
        - show firewall prefix-action-stats filter by xml format
        - Get 'packet-count' and 'byte-count' in
        firewall-prefix-action-information

        :param filter:
            REQUIRED Name of a filter (string)
        :param prefix_action:
            REQUIRED Name of a prefix action (string)
        :param from:
            OPTION Starting counter or policer (string). Default: 0
        :param to:
            OPTION Ending counter or policer (string). Default: 65535

        :return:
            psc_counter (dict).
            psc_counter = {
                'counter_name1': {'byte_count': '1','packet_count': '5'},
                'counter_name2': {'byte_count': '3', 'packet_count': '25'},
                'counter_name3': {'byte_count': '2', 'packet_count': '15'}
                }

        Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{input} =    Create Dictionary    filter=limit-source-one-24
        ...    prefix_action=psa-1Mbps-per-source-24-32-256-one
        ...    from=${0}    to=${3}
        ${result} =    Get Firewall Psc    device=${dev}    &{input}

    '''
    # Check parameter
    valid_keys = ['filter', 'prefix_action', 'from', 'to']
    required_key = ['filter', 'prefix_action']
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs['filter']
    prefix_action = kwargs['prefix_action']

    _from = kwargs.get('from', 0)
    _to = kwargs.get('to', 65535)

    psc_counter = {}

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    cfg_cmd = "show firewall prefix-action-stats filter %s prefix-action \
            %s from %s to %s" % (_filter, prefix_action, _from, _to)

    try:
        rpc_str = device.get_rpc_equivalent(command=cfg_cmd)
        response = device.execute_rpc(command=rpc_str).response()
    except:
        device.log(message="Get response from prefix-action-stats filter %s \
                    failed on device" % _filter, level='error')
        return psc_counter

    counter_names = []
    byte_counts = []
    packet_counts = []

    elements = response.findall(".//counter/counter-name")
    for element in elements:
        counter_names.append(element.text.strip())
    for counter_name in counter_names:
        psc_counter[counter_name] = {}

    elements = response.findall(".//counter/byte-count")
    for element in elements:
        byte_counts.append(element.text.strip())

    elements = response.findall(".//counter/packet-count")
    for element in elements:
        packet_counts.append(element.text.strip())

    for i in range(0, len(counter_names)):
        psc_counter[counter_names[i]]['packet_count'] = packet_counts[i]
        psc_counter[counter_names[i]]['byte_count'] = byte_counts[i]

    return psc_counter


def get_firewall_counter(device, **kwargs):
    '''
    Get firewall counter (packets, bytes) from the filter name by cli:
        "show firewall filter firewall_name counter couter_name"
    or "show firewall filter firewall_name"

    :param filter:
        OPTION name of filter
    :param counter:
        OPTION Name of counter
    :param interface:
        OPTION Name of interface
    :param input:
        OPTION to set filter, counter format ( + "-i")
    :param output:
        OPTION to set filter, counter format (+ "-0")


    :return fw_counter(dict):
        values of firewall counter (packets, bytes)
        Eg: {'COUNTER1-ae2.0-i': {'byte_count': '7422104196',
            'packet_count': '31718394'}}

    Robot Usage Example  :
    ${dev} =    Get Handle   resource=device0
    &{input} =    Create Dictionary    filter=icmp_syslog
    ${result} =    Get Firewall Counter    device=${dev}    &{input}

    '''

    # Check parameter
    valid_keys = ['filter', 'counter', 'interface', 'input', 'output']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    fw_counter = {}

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    _filter = kwargs.get('filter')
    counter = kwargs.get('counter')
    interface = kwargs.get('interface')
    _input = kwargs.get('input')
    output = kwargs.get('output')

    if not interface and not _filter:
        device.log(message="%s filter or interface value\
             must be specified" % function, level='error')
        return False

    if interface:
        if _input and output:
            device.log(message="%s cannot specifiy both input and output\
                     options to get counter for interface specific\
                      filter" % function, level='error')
            return False

        _filter = interface
        if _input:
            _filter = _filter + "-i"
        else:
            _filter = _filter + "-o"

        if counter:
            counter = counter + '-' + interface
            if _input:
                counter = counter + "-i"
            else:
                counter = counter + "-o"

            param = {'filter': _filter, 'counter': counter}
            return get_firewall_counter(device, **param)
        else:
            param = {'filter': _filter}
            return get_firewall_counter(device, **param)

    else:
        if counter:
            device.log(message="%s: filter(%s), counter(%s)"
                       % (function, _filter, counter), level='debug')
            cmd = "show firewall filter %s counter %s" % (_filter, counter)
        else:
            device.log(message="%s: filter(%s)" % (function, _filter),
                       level='debug')
            cmd = "show firewall filter %s" % _filter

    try:
        rpc_str = device.get_rpc_equivalent(command=cmd)
        response = device.execute_rpc(command=rpc_str).response()
    except Exception:
        device.log(message="get the response from firewall filter \
                failed on device", level='error')
        return False

    counter_names = []
    byte_counts = []
    packet_counts = []

    elements = response.findall(".//counter/counter-name")
    for element in elements:
        counter_names.append(element.text.strip())

    elements = response.findall(".//counter/byte-count")
    for element in elements:
        byte_counts.append(element.text.strip())

    elements = response.findall(".//counter/packet-count")
    for element in elements:
        packet_counts.append(element.text.strip())

    for counter_name in counter_names:
        fw_counter[counter_name] = {}

    for i in range(0, len(counter_names)):
        fw_counter[counter_names[i]]['packet_count'] = packet_counts[i]
        fw_counter[counter_names[i]]['byte_count'] = byte_counts[i]

    return fw_counter


def check_firewall_counter(device, **kwargs):
    '''
    Check firewall counter for interface specific filter

    :param filter:
        OPTION name of filter
    :param counter:
        OPTION name of counter
    :param interface:
        OPTION Interface name (i.e. so-0/1/0.0)
    :param input:
        OPTION 1 | 0 (default it 1 if interface)
    :param ouptut:
        OPTION input 0|1 (default is 0 if interface)
    :param packet:
        OPTION A long integer value, an array of [min, max] or
            a regular expression for expect packet count
    :param byte:
        OPTION A long integer value, an array of [min, max] or
            a regular expression for expect byte count
    :param check_count:
        OPTION Check count (default is 1)
    :param check_interval:
        REQUIRED Wait time before next retry (default 10 seconds)

    :return True/False:
        - True if packet checking passed
        - False if packet checking failed

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${byte} =    Create List    ${0}    ${7571314296}
        &{input} =    Create Dictionary    filter=icmp_syslog
        ...    counter=packets    byte=${byte}
        ${result} =    Check Firewall Counter    device=${dev}    &{input}
    '''

    # Check parameter
    valid_keys = ['filter', 'counter', 'interface', 'input',
                  'output', 'packet', 'byte', 'chk_count', 'chk_interval']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    fw_counter = {}

    function = function_name()
    logging.info(msg="Inside %s function" % function)

    _filter = kwargs.get('filter')
    counter = kwargs.get('counter')
    interface = kwargs.get('interface')
    _input = kwargs.get('input')
    _output = kwargs.get('output')
    packet = kwargs.get('packet')
    byte = kwargs.get('byte')
    chk_count = kwargs.get('chk_count', 1)
    chk_interval = kwargs.get('chk_interval', 10)

    if not interface and not _filter:
        device.log(message="%s filter or interface value\
             must be specified" % function, level='error')
        return False

    if interface:
        if _input is not None:
            _input = 1
        else:
            _output = 1

    function = function_name()
    logging.info(msg="Inside %s function" % function)

    if packet:
        device.log(message="%s : packet %s " % (function, packet),
                   level='debug')
    if byte:
        device.log(message="%s : byte %s " % (function, byte),
                   level='debug')

    packet_ok = 0
    if packet is None:
        packet_ok = 1
    byte_ok = 0
    if byte is None:
        byte_ok = 1
    for i in range(0, chk_count):
        if i > 0:
            time.sleep(chk_interval)
        param = {'filter': _filter, 'counter': counter,
                 'interface': interface, 'input': _input,
                 'output': _output}
        fw_counter = get_firewall_counter(device, **param)
        packets_count = []
        bytes_count = []
        if fw_counter:
            for key in fw_counter.keys():
                packets_count.append(fw_counter[key]['packet_count'])
                bytes_count.append(fw_counter[key]['byte_count'])

            if packet_ok and byte_ok:
                break
            if not packet_ok:
                if __check_value(packets_count, packet):
                    packet_ok = 1
            if not byte_ok:
                if __check_value(bytes_count, byte):
                    byte_ok = 1

    if packet_ok and byte_ok:
        device.log(message="%s : byte/packet checking passed"
                   % function, level='info')
        return True
    else:
        device.log(message="%s : byte/packet checking failed"
                   % function, level='warn')
        return False


def get_firewall_log(device, **kwargs):
    '''
    Get informations from cli "show firewall log detail/show firewall log
    interface detail":
        1. action name
        2. source address
        3. destination address
        4. protocol name
        5. packet length

    :param interface:
        OPTION name of interface
    :param protocol:
        OPTION name of protocol: TCP, ICP, ...
    :param filter:
        OPTION name of filter
    :param action:
        OPTION name of action: D, ...
    :param source_address:
        OPTION source address: IP format
    :param destination_address:
        OPTION destination address: IP format
    :param from:
        OPTION from time of Log: format is hh:mm:ss
    :param to:
        OPTION to time of Log: format is hh:mm:ss
    :param packet_length
        OPTION packet length

    :return fw_log:
        Dictionary of action name, source address, destination address,
        protocol name, packet length
        Eg: {'packet_length': '328', 'action': 'discard',
        'filter': 'ACCESS-CNTRL',
        'protocol': 'UDP', 'source_address': '0.0.0.0:68',
        'destination_address': '255.255.255.255:67'}

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Firewall Log    device=${dev}    filter=pfe
        ...    interface=xe-0/0/0.1
        ...    action=accept    from=00:00:00    to=23:59:59
    '''

    valid_keys = ['filter', 'protocol', 'interface', 'action', 'from',
                  'to', 'source_address', 'destination_address',
                  'packet_length']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    interface = kwargs.get('interface')
    _filter = kwargs.get('filter')
    protocol = kwargs.get('protocol')
    action = kwargs.get('action')
    _from = kwargs.get('from')
    _to = kwargs.get('to')
    src_addr = kwargs.get('source_address')
    dst_addr = kwargs.get('destination_address')
    pkt_len = kwargs.get('packet_length')

    fw_log = {}
    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    cli_cmd = "show firewall log"
    if interface:
        cli_cmd += "  interface " + interface
    cli_cmd += "  detail"

    try:
        rpc_str = device.get_rpc_equivalent(command=cli_cmd)
        response = device.execute_rpc(command=rpc_str).response()
    except Exception:
        device.log(message="get the response from show firewall log \
                failed on device", level='error')
        return False

    if response.find(".//log-information") is not None:
        times = []
        actions = []
        filters = []
        interfaces = []
        src_addrs = []
        dst_addrs = []
        protocols = []
        pkt_lens = []

        elements = response.findall(".//time")
        for element in elements:
            times.append(element.text.strip())
        elements = response.findall(".//action-name")
        for element in elements:
            actions.append(element.text.strip())
        elements = response.findall(".//filter-name")
        for element in elements:
            filters.append(element.text.strip())
        elements = response.findall(".//interface-name")
        for element in elements:
            interfaces.append(element.text.strip())
        elements = response.findall('.//source-address')
        for element in elements:
            src_addrs.append(element.text.strip())
        elements = response.findall('.//destination-address')
        for element in elements:
            dst_addrs.append(element.text.strip())
        elements = response.findall('.//protocol-name')
        for element in elements:
            protocols.append(element.text.strip())
        elements = response.findall('.//packet-length')
        for element in elements:
            pkt_lens.append(element.text.strip())

        for i in range(0, len(times)):
            match = 1
            if action and actions[i] != action:
                match = 0
            elif _filter and filters[i] != _filter:
                match = 0
            elif src_addr and src_addrs[i] != src_addr:
                match = 0
            elif dst_addr and dst_addrs[i] != dst_addr:
                match = 0
            elif protocol and protocols[i] != protocol:
                match = 0
            elif pkt_len and pkt_lens[i] != pkt_len:
                match = 0
            elif _from or _to:
                current_time = times[i]
                matched = re.search(r"\s+(\d+\:\d+\:\d+)\s+", current_time)
                _time = matched.group(1)
                if _from and __timeless(_time, _from):
                    match = 0
                if _to and __timeless(_to, _time):
                    match = 0

            if match:
                fw_log['filter'] = filters[i]
                fw_log['source_address'] = src_addrs[i]
                fw_log['destination_address'] = dst_addrs[i]
                fw_log['protocol'] = protocols[i]
                fw_log['action'] = actions[i]
                fw_log['packet_length'] = pkt_lens[i]

    return fw_log


def check_firewall_log(device, **kwargs):
    '''
        Check firewall syslog entry found or not
        :param interface
            OPTION  Interface name (i.e. so-0/1/0 or so-0/1/0.0)
        :param filter
            OPTION Filter name (string)
        :param protocol
            OPTION Protocol name/number (string)
        :param source_address
            OPTION Source address (string)
        :param destination_address
            OPTION destination address (string)
        :param action
            OPTION Action name (i.e. accept, reject, discard)
        :param from
            OPTION Start time (hh:mm:ss)
        :param to
            OPTION End time (hh:mm:ss)
        :param chk_count
            OPTION Check count (default is 1)
        :param chk_interval
            OPTION Wait time before next retry (default 10 seconds)

       :return:
            True: syslog entry is found
            False: syslog entry is not found

        Robot Usage Example  :
            ${dev} =    Get Handle   resource=device0
            ${result} =    Check Firewall Log    device=${dev}
            ...    filter=icmp_syslog    interface=fxp0.0
            ...    interface=fxp0.0    action=accept    from=00:00:00
            ...    protocol=TCP    to=23:59:59    chk_count=${2}
            ...    chk_interval=${10}
    '''

    valid_keys = ['filter', 'protocol', 'interface', 'action', 'from',
                  'to', 'source_address', 'destination_address',
                  'packet_length', 'chk_count', 'chk_interval']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    interface = kwargs.get('interface')
    _filter = kwargs.get('filter')
    protocol = kwargs.get('protocol')
    action = kwargs.get('action')
    _from = kwargs.get('from')
    _to = kwargs.get('to')
    src_addr = kwargs.get('source_address')
    dst_addr = kwargs.get('destination_address')
    pkt_len = kwargs.get('packet_length')
    chk_count = kwargs.get('chk_count', 1)
    chk_interval = kwargs.get('chk_interval', 10)

    fw_log = {}
    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    for i in range(0, chk_count):
        if i > 0:
            time.sleep(chk_interval)
        param = {'filter': _filter, 'protocol': protocol,
                 'interface': interface, 'action': action,
                 'from': _from, 'to': _to, 'source_address': src_addr,
                 'destination_address': dst_addr, 'packet_length': pkt_len}
        fw_log = get_firewall_log(device, **param)

        if fw_log:
            device.log(message="%s log entry found" % function, level='info')
            return True

    device.log(message="%s log entry not found" % function, level='warn')
    return False


def check_firewall_psc(device, **kwargs):
    '''
    Check firewall prefix-action-stats for interface specific filter

    :param filter:
        REQUIRED name of filter
    :param prefix_action:
        REQUIRED name of prefix action
    :param index:
        index of counter
    :param packet:
        OPTION 0|1 packet checking. Default: 1
    :param byte:
        OPTION 0|1 byte checking. Default: 1
    :param chk_count:
        OPTION number of checking times. Default: 0
    :param chk_interval:
        OPTION interval of each checking cycle. Default: 10

    :return True/False:
        - True if byte/packet checking passed
        - False if byte/packet checking failed

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Check Firewall Psc    device=${dev}
        ...    filter=limit-source-one-24
        ...    prefix_action=psa-1Mbps-per-source-24-32-256-one
    '''

    # Check parameter
    valid_keys = ['filter', 'prefix_action', 'index', 'packet',
                  'byte', 'chk_count', 'chk_interval']
    required_key = ['filter', 'prefix_action']
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs.get('filter')
    prefix_action = kwargs.get('prefix_action')
    index = kwargs.get('index')
    packet = kwargs.get('packet')
    byte = kwargs.get('byte')

    chk_count = kwargs.get('chk_count', 1)
    chk_interval = kwargs.get('chk_interval', 10)

    psc_counter = {}

    function = function_name()
    logging.info(msg="Inside %s function" % function)

    packet_ok = False
    if packet is None:
        packet_ok = True
    byte_ok = False
    if byte is None:
        byte_ok = True

    for i in range(0, chk_count):
        if i > 0:
            time.sleep(chk_interval)
        param = {'filter': _filter, 'prefix_action': prefix_action,
                 'from': index, 'to': index}
        psc_counter = get_firewall_psc(device, **param)

        packets_count = []
        bytes_count = []
        if psc_counter:
            for key in psc_counter.keys():
                packets_count.append(psc_counter[key]['packet_count'])
                bytes_count.append(psc_counter[key]['byte_count'])

            if packet_ok and byte_ok:
                break
            if not packet_ok:
                if __check_value(packets_count, packet):
                    packet_ok = True
            if not byte_ok:
                if __check_value(bytes_count, byte):
                    byte_ok = True

    if packet_ok and byte_ok:
        device.log(message=" %s : byte/packet checking passed " % function,
                   level='info')
        return True
    else:
        device.log(message=" %s : byte/packet checking failed " % function,
                   level='warn')
        return False


def get_pfe_kmem(device, **kwargs):
    '''
    Get PFE kernel memory usage by doing the following actions:
    1. show kernel memory
    2. Get total and used kernel memory
    :param pfe
        REQUIRED name of PFE. Eg: fpc0, fpc1... (string)

    :return:
        pfe_kmem (dict) Eg: pfe_kmem['total'] , pfe_kmem['used']
        Eg: {'total': '1879034044', 'used': '1093999040'}

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Pfe Kmem    device=${dev}    pfe=fpc0
    '''
    function = function_name()
    logging.info(msg="Inside %s function" % function)

    # Check parameter
    valid_keys = ['pfe']
    required_key = ['pfe']
    kwargs = check_args(valid_keys, required_key, kwargs)
    pfe = kwargs.get('pfe')

    pfe_kmem = {}

    cli_cmd = 'cprod -A ' + pfe + ' -c "show memory"'

    try:
        res = device.shell(command=cli_cmd)
        response = res.response()
    except Exception:
        device.log(message="get the response from show memory \
                failed on device", level='error')
        return False

    match = re.search(r'(\S+)\s+\S+\s+(\S+)\s+\S+\s+Kernel',
                      response, re.DOTALL)

    if match:
        pfe_kmem['total'] = match.group(1)
        pfe_kmem['used'] = match.group(2)
    else:
        device.log(message="%s : unexpected output" % function, level='error')

    return pfe_kmem


def get_pfe_jmem(device, **kwargs):
    '''
    Get PFE jtree memory usage by doing the following actions:
    1. show jtree memory
    2. Get total and used jtree memory

    :param pfe
        REQUIRED name of PFE. Eg: fpc0, fpc1... (string)
    :param number
        REQUIRED the number of instance (string)

    :return:
        pfe_jmem (dict) Eg: pfe_jmem['total'] , pfe_jmem['used']
        Eg: {'used': '5280856', 'total': '16777216'}

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Pfe Jmem    device=${dev}    pfe=fpc0    num=${1}
    '''
    function = function_name()
    logging.info(msg="Inside %s function" % function)

    # Check parameter
    valid_keys = ['pfe', 'num']
    required_key = ['pfe', 'num']
    kwargs = check_args(valid_keys, required_key, kwargs)

    pfe = kwargs.get('pfe')
    num = kwargs.get('num')

    pfe_jmem = {}

    cli_cmd = 'cprod -A ' + pfe + ' -c "show jtree ' + \
              str(num) + ' memory"'
    try:
        res = device.shell(command=cli_cmd)
        response = res.response()
    except Exception:
        device.log(message="get the response from show jtree \
                failed on device", level='error')
        return False

    match = re.search(r'\s+(\S+)\s+bytes total.*\s+(\S+)\s+bytes used',
                      response, re.DOTALL)

    if match:
        pfe_jmem['total'] = match.group(1)
        pfe_jmem['used'] = match.group(2)
    else:
        device.log(message="%s : unexpected output" % function, level='error')

    return pfe_jmem


def get_pfe_list(device, **kwargs):
    '''
    Get a list of PFEs for give interfaces

    :param interface
        REQUIRED Interface or list of interfaces
        Eg. "ge-0/0/1'", or ['ge0/0/1'', 'xe-0/1/1']

   :return:
        pfe_list (list) Eg. ['fpc0', 'fpc1']

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${interface} =    Create List    xe-0/0/0    xe-2/2/0
        ${result} =    Get Pfe List    device=${dev}    interface=${interface}
    '''

    function = function_name()
    logging.info(msg="Inside %s function" % function)

    # Check parameter
    valid_keys = ['interface']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)

    interface = kwargs.get('interface')

    if not isinstance(interface, list):
        interface = [interface]

    pfe_list = []
    regex_if = r'(\w+)(?:-(\d+)/(\d+)/(\d+))?(?::(\d+))?(?:\.(\d+))?'
    for intf in interface:
        match = re.search(regex_if, intf)
        if match.group(2):
            pfe = 'fpc' + match.group(2)
            pfe_list.append(pfe)

    return pfe_list


def get_firewall_policer(device, **kwargs):
    '''
    Get firewall policer counter (packets, bytes) from the filter name and
    policer name

    :param filter:
        REQUIRED name of filter
    :param policer:
        REQUIRED Name of policer
    :param interface:
        REQUIRED Name of interface
    :param input:
        OPTION to set filter, counter format ( + "-i" or "-o"). Default 1
    :param output:
        OPTION to set filter, counter format (+ "-"). Default 0

    :return fw_policer:
        values of firewall policer (packets, bytes)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Firewall Policer    device=${dev}
        ...    filter=ACCESS-CNTRL
    '''

    # Check parameter
    valid_keys = ['filter', 'policer', 'interface', 'input', 'output']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    fw_policer = {}

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    _filter = kwargs.get('filter')
    policer = kwargs.get('policer')
    interface = kwargs.get('interface')
    _input = kwargs.get('input', 1)
    output = kwargs.get('output', 0)

    if not interface and not _filter:
        device.log(message="%s filter or interface value\
             must be specified" % function, level='error')
        return False

    if interface:
        if _input and output:
            device.log(message="%s cannot specifiy both input and output\
                     options to get counter for interface specific\
                      filter" % function, level='error')
            return False

        _filter = interface
        if _input:
            _filter = _filter + "-i"
        else:
            _filter = _filter + "-o"

        if policer:
            policer = policer + '-' + interface
            if _input:
                policer = policer + "-i"
            else:
                policer = policer + "-o"

            param = {'filter': _filter, 'policer': policer}
        else:
            param = {'filter': _filter}
        return get_firewall_policer(device, **param)

    else:
        if policer:
            device.log(message="%s: filter(%s), policer(%s)"
                       % (function, _filter, policer), level='debug')
            cmd = "show firewall filter %s counter %s" % (_filter, policer)
        else:
            device.log(message="%s: filter(%s)" % (function, _filter),
                       level='debug')
            cmd = "show firewall filter %s" % _filter

    try:
        rpc_str = device.get_rpc_equivalent(command=cmd)
        response = device.execute_rpc(command=rpc_str).response()
    except Exception:
        device.log(message="get the response from firewall policer \
                failed on device", level='error')
        return False

    if response.find(".//policer/policer-name") is not None:
        counter_names = []
        byte_counts = []
        packet_counts = []

        elements = response.findall(".//policer/policer-name")
        for element in elements:
            counter_names.append(element.text.strip())
        elements = response.findall(".//policer/byte-count")
        for element in elements:
            byte_counts.append(element.text.strip())
        elements = response.findall(".//policer/packet-count")
        for element in elements:
            packet_counts.append(element.text.strip())
        for counter_name in counter_names:
            fw_policer[counter_name] = {}
        for i in range(0, len(counter_names)):
            fw_policer[counter_names[i]]['packet_count'] = packet_counts[i]
            fw_policer[counter_names[i]]['byte_count'] = byte_counts[i]

    return fw_policer


def check_firewall_policer(device, **kwargs):
    '''
    Check firewall policer for interface specific filter

    :param filter:
        REQUIRED name of filter
    :param policer:
        REQUIRED name of policer
    :param interface:
        REQUIRED interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param input:
        OPTION input 0|1 apply filter to input interface. Default 1
    :param ouptut:
        OPTION input 0|1 apply filter to input interface. Default 0
    :param packet:
        OPTION A long integer value, an array of [min, max] or
            a regular expression for expect packet count
    :param byte:
        OPTION A long integer value, an array of [min, max] or
            a regular expression for expect byte count
    :param check_count:
        OPTION Check count (default is 1)
    :param check_interval:
        REQUIRED Wait time before next retry (default 10 seconds)

    :return True/False:
        - True if packet checking passed
        - False if packet checking failed

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${byte} =    Create List    ${0}    ${10000}
        ${packet} =    Create List    ${0}    ${10000}
        ${result} =    Check Firewall Policer    device=${dev}
        ...    filter=ACCESS-CNTRL    policer=1Mbps-policer
        ...    byte=${byte}    packet=${packet}
    '''

    valid_keys = ['filter', 'policer', 'interface', 'input', 'output',
                  'packet', 'byte', 'chk_count', 'chk_interval']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs.get('filter')
    policer = kwargs.get('policer')
    interface = kwargs.get('interface')
    _input = kwargs.get('input', 1)
    output = kwargs.get('output', 0)
    packet = kwargs.get('packet')
    byte = kwargs.get('byte')
    chk_count = kwargs.get('chk_count', 1)
    chk_interval = kwargs.get('chk_interval', 10)

    function = function_name()
    logging.info(msg="Inside %s" % function)

    if not interface and not _filter:
        device.log(message="%s filter or interface value\
             must be specified" % function, level='error')
        return False

    if interface:
        if _input and output:
            device.log(message="%s cannot specifiy both input and output\
                     options to get counter for interface specific\
                      filter" % function, level='error')
            return False

    if packet:
        device.log(message="%s : packet %s " % (function, packet),
                   level='debug')
    if byte:
        device.log(message="%s : byte %s " % (function, byte),
                   level='debug')

    packet_ok = 0
    if packet is None:
        packet_ok = 1
    byte_ok = 0
    if byte is None:
        byte_ok = 1

    for i in range(0, chk_count):
        if i > 0:
            time.sleep(chk_interval)
        param = {'filter': _filter, 'policer': policer,
                 'interface': interface, 'input': _input, 'output': output}
        fw_policer = get_firewall_policer(device, **param)
        packets_count = []
        bytes_count = []
        if fw_policer:
            for key in fw_policer.keys():
                packets_count.append(fw_policer[key]['packet_count'])
                bytes_count.append(fw_policer[key]['byte_count'])

            if packet_ok and byte_ok:
                break
            if not packet_ok:
                if __check_value(packets_count, packet):
                    packet_ok = 1
            if not byte_ok:
                if __check_value(bytes_count, byte):
                    byte_ok = 1

    if packet_ok and byte_ok:
        device.log(message="%s : byte/packet checking passed" % function,
                   level='info')
        return True
    else:
        device.log(message="%s : byte/packet checking failed" % function,
                   level='warn')
        return False


def check_filter_install(device, **kwargs):
    '''
    Check filter is installed on pfe or not by doing the
    following actions:

    - Get pfe list from interface list
    - Get filter index from pfe, filter, interf, input, output,
    if_specific
    - Check filter is installed on pfe or not from filter index

    :param filter:
        REQUIRED name of filter (string)
    :param interface:
        REQUIRED list of interface (list of string)
    :param if_specific:
        OPTION 1 | 0 (default is 0)
    :param input:
        OPTION 1 | 0 (default it 1 if if_specific)
    :param output:
        OPTION 1 | 0 (default is 0 if if_specific)
    :param chk_count:
        OPTION Check count (default is 1)
    :param chk_interval:
        OPTION Wait time before next retry (default 10 seconds)

    :return:
        True: filter is installed on pfe
        False: filter is not installed on pfe

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Check Filter Install    device=${dev}
        ...    filter=icmp_syslog    interface=xe-0/0/0.1
    '''

    valid_keys = ['filter', 'interface', 'if_specific', 'input', 'output',
                  'chk_count', 'chk_interval']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs.get('filter')
    interface = kwargs.get('interface')
    if_specific = kwargs.get('if_specific')

    _input = kwargs.get('input', 1)
    _output = kwargs.get('output', 0)
    chk_count = kwargs.get('chk_count', 1)
    chk_interval = kwargs.get('chk_interval', 10)

    function = function_name()
    logging.info(msg="Inside %s function" % function)

    if not isinstance(interface, list):
        interface = [interface]

    filter_install_regexp1 = r'\s*Pfe\s+Inst\s*:\s*(\d)\s*Hw\s+Instance'
    filter_install_regexp2 = r'Filter Install \((\d+) active planes\).*\s+'
    '0x[0-9a-f]+\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+(\d+)\s+'
    install_ok = 0

    for interf in interface:
        filter_index = 0
        param = {'interface': interf}
        pfe = get_pfe_list(device, **param)[0]
        for i in range(0, chk_count):
            if i > 0:
                time.sleep(chk_interval)
            device.log(message="%s pfe(%s)" % (function, pfe), level='debug')
            if filter_index <= 0:
                param = {'pfe': pfe, 'filter': _filter,
                         'interface': interf, 'input': _input,
                         'output': _output, 'if_specific': if_specific}
                filter_index = get_filter_index(device, **param)
            if not filter_index:
                device.log(message="%s (i=%s): filter(%s) not installed\
                                    on pfe(%s) kernel" % (function, i,
                                                          _filter, pfe),
                           level='warn')
                continue
            device.log(message="%s :checking filter(%s) installation on\
                pfe(%s)" % (function, filter, pfe), level='debug')

            response = __cprod(device, name=pfe,
                               cmd="show filter index " + str(filter_index) +
                               ' detail')

            for line in response:
                if re.search(filter_install_regexp1, line, re.DOTALL):
                    install_ok = 1
                    break
                if re.search(filter_install_regexp2, line, re.DOTALL):
                    install_ok = 1
                    break

    if not install_ok:
        device.log(message='%s filter %s failed to be installed on pfe %s'
                   % (function, _filter, pfe), level='warn')
        return False
    return True


def check_filter_remove(device, **kwargs):
    '''
    Check filter is removed on pfe or not by doing the following
    actions:
    - Get pfe list from interface list
    - Get filter index from pfe, filter, interf, input, output,
     if_specific
    - Check filter is removed on pfe or not from filter index

    :param filter:
        REQUIRED name of filter (string)
    :param interface:
        REQUIRED list of interface (list of string)
    :param if_specific:
        OPTION 1 | 0 (default is 0)
    :param input:
        OPTION 1 | 0 (default it 1 if if_specific)
    :param output:
        OPTION 1 | 0 (default is 0 if if_specific)
    :param chk_count:
        OPTION Check count (default is 0)
    :param chk_interval:
        OPTION Wait time before next retry (default 10 seconds)

    :return:
        True: filter is removed on pfe
        False: filter is not removed on pfe

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Check Filter Remove    device=${dev}
        ...    filter=ACCESS-DELETE    interface=xe-0/0/0.2
    '''
    valid_keys = ['filter', 'interface', 'if_specific', 'input', 'output',
                  'chk_count', 'chk_interval']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs.get('filter')
    interface = kwargs.get('interface')
    if_specific = kwargs.get('if_specific')

    _input = kwargs.get('input', 1)
    _output = kwargs.get('output', 0)
    chk_count = kwargs.get('chk_count', 1)
    chk_interval = kwargs.get('chk_interval', 10)

    function = function_name()
    logging.info(msg="Inside %s function" % function)

    if not isinstance(interface, list):
        interface = [interface]

    filter_install_regexp1 = r'\s*Pfe\s+Inst\s*:\s*(\d)\s*Hw\s+Instance'
    filter_install_regexp2 = r'Filter Install \((\d+) active planes\).*\s+'
    '0x[0-9a-f]+\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+(\d+)\s+'
    remove_ok = 1

    for interf in interface:
        filter_index = 0
        param = {'interface': interf}
        pfe = get_pfe_list(device, **param)[0]
        for i in range(0, chk_count):
            if i > 0:
                time.sleep(chk_interval)
            device.log(message="%s pfe(%s)" % (function, pfe), level='debug')
            if filter_index <= 0:
                param = {'pfe': pfe, 'filter': _filter,
                         'interface': interf, 'input': _input,
                         'output': _output, 'if_specific': if_specific}
                filter_index = get_filter_index(device, **param)
            if not filter_index:
                device.log(message="%s (i=%s): filter(%s) not installed\
                            on pfe(%s) kernel" % (function, i, _filter, pfe
                                                  ), level='warn')
                continue
            device.log(message="%s :checking filter(%s) installation on \
                    pfe(%s)" % (function, filter, pfe), level='debug')

            response = __cprod(device, name=pfe, cmd="show filter index " +
                               str(filter_index) + ' detail')

            for line in response:
                if re.search(filter_install_regexp1, line, re.DOTALL):
                    remove_ok = 0
                    break
                if re.search(filter_install_regexp2, line, re.DOTALL):
                    remove_ok = 0
                    break

    if not remove_ok:
        device.log(message='%s filter %s failed to be installed on pfe %s'
                   % (function, _filter, pfe), level='warn')
        return False
    return True


def get_rchip_stat(device, **kwargs):
    '''
    Get RCHIP statistics for failure analysis by doing the
    following actions:
    - Check platforms is supported of getting RCHIP command or not
    - show rchip with options: counter, statistics errors, registers hnp...

    :param vty:
        REQUIRED vty name, i.e. fpc1, fpc12 (string).
    :param rchip:
        OPTION list of rchip (list of number), default [0,1]

    :return:
        TRUE: if no error occurred
        FALSE: if error occurred

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device1
        ${result} =    Get Rchip Stat    device=${dev}    vty=fpc0    rchip=1

    '''

    valid_keys = ['vty', 'rchip']
    required_key = ['vty']
    kwargs = check_args(valid_keys, required_key, kwargs)

    vty_name = kwargs.get('vty')
    rchip = kwargs.get('rchip', [0, 1])

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    if not re.search(r'^m[13]20$', device.get_model(), re.IGNORECASE):
        device.log(message="Sub %s can only run on m320,\
                 m120 and T platforms" % function, level='error')
        return False

    if not isinstance(rchip, list):
        rchip = [rchip]
    count = 0
    for i in rchip:
        rch = str(i)
        try:
            response = device.vty(destination=vty_name,
                                  command="show rchip " + rch).response()
        except Exception:
            device.log(message="get the response from show rchip \
                        failed on device", level='error')
            return False
        if not re.search(r'not exist', response):
            count += 1

        cmds = ["show rchip " + rch + " counter",
                "show rchip " + rch + " statistics errors",
                "show rchip " + rch + " registers hnp",
                "show rchip " + rch + " registers icp",
                "show rchip " + rch + " registers kme_ctl",
                "show rchip " + rch + " registers rcp",
                "show rchip " + rch + " registers sr",
                "show rchip " + rch + " registers top",
                "show jtree " + rch + " debug ip on-chip check table"]

        for cmd in cmds:
            device.vty(destination=vty_name, command=cmd)

    if count == 0:
        device.log(message="function %s no rchip found" % function,
                   level='error')
        return False

    return True


def __timeless(time1, time2):
    '''
     This funtion used to get the time on firewall log:
     Example: Time of Log: 2004-10-13 10:37:17 PDT

    :param time1: time to start
    :param time2: time to finish

    :return:
        TRUE if the time before > after
        FALSE if the time after < before

    '''
    date1 = datetime.datetime.strptime(time1, '%H:%M:%S')
    date2 = datetime.datetime.strptime(time2, '%H:%M:%S')

    if date1 < date2:
        return True
    return False


def __check_value(value1, value2):
    '''
    Check value value1 in value2
    if value2 is list. Eg: [100, 400]
        if all elements of value1 in range value2 100...400
            return true
    else if value2 is interger. Eg: 100
        if all elements of list value1 match with value2
            return true
    else if value is regular expression.
        if all elements of list value1 match with regular expression
            return true
    else
        return false

    :param value1:
        list. Eg: [1,3,4,100]
    :param value2:
        list with two element. Eg: [1,100]
        or integer number. Eg: 1
        or string of regular expression.
    :return True/False:
        True if value1 in value2
        False if value1 not in value2:
    '''
    function = function_name()
    logging.info(msg="Inside %s function" % function)

    chk_ok = 0
    if not isinstance(value1, list):
        value1 = [value1]
    for element in value1:
        if isinstance(element, str):
            if element.isdigit():
                element = int(element)
        if isinstance(value2, list):
            if element >= value2[0] and element <= value2[1]:
                chk_ok = 1
        if isinstance(value2, int):
            if element == value2:
                chk_ok = 1
        if isinstance(value2, str):
            if re.search(str(element), value2):
                chk_ok = 1
    if chk_ok:
        return True
    else:
        return False


def configure_firewall_policer(device, **kwargs):
    '''
    Configure firewall policer with these options:
        1. bandwidth-limit
        2. bandwidth-percent
        3. burst-size-limit

    :param name:
        OPTION name of policer name. Default is "policer"
    :param bw_limit:
        OPTION bandwidth limit (8000..100000000000 bits
                                             per second)
    :param bw_percent:
        OPTION bandwidth limit in percentage (1..100 percent)
    :param burst_size:
        OPTION burst size limit (1500..100000000000 bytes)
    :param action:
        OPTION action to take if the rate limits are exceeded
        Default is "discard"
    :param limit_type:
        OPTION limit type
        Default is 'if-exceeding'
    :param filter_specific:
        OPTION filter specific
     :param packet_burst:
        OPTION packet burst
    :param pps_limit:
        OPTION pps limit
    :param logical_bandwidth_policer:
        OPTION logical bandwidth policer
    :param logical_interface_policer:
        OPTION logical interface policer
    :param physical_interface_policer:
        OPTION physical interface policer
    :param shared_bandwidth_policer:
        OPTION shared bandwidth policer
    :param commit:
        OPTION if commit value is defined, will commit the
        configuration to device

    :return:
        TRUE if there is no error of configuration

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Configure Firewall Policer    ${dev}
        ...    name=1Mbps-policer    bw_limit=1m    bw_percent=${0}
        ...    burst_size=63k    action=discard    commit=${1}
    '''
    valid_keys = ['name', 'bw_limit', 'bw_percent', 'burst_size', 'action',
                  'commit', 'limit_type', 'packet_burst', 'pps_limit',
                  'logical_bandwidth_policer', 'logical_interface_policer',
                  'physical_interface_policer', 'shared_bandwidth_policer',
                  'filter_specific']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)
    name = kwargs.get('name', 'policer')
    action = kwargs.get('action', 'discard')
    bw_limit = kwargs.get('bw_limit')
    bw_percent = kwargs.get('bw_percent')
    burst_size = kwargs.get('burst_size')
    commit = kwargs.get('commit')
    filter_specific = kwargs.get('filter_specific')
    limit_type = kwargs.get('limit_type', 'if-exceeding')
    packet_burst = kwargs.get('packet_burst')
    pps_limit = kwargs.get('pps_limit')
    logical_bandwidth_policer = kwargs.get('logical_bandwidth_policer')
    logical_interface_policer = kwargs.get('logical_interface_policer')
    physical_interface_policer = kwargs.get('physical_interface_policer')
    shared_bandwidth_policer = kwargs.get('shared_bandwidth_policer')
    function = function_name()
    logging.info(msg="Inside %s" % function)
    config_cmds = []
    if filter_specific:
        config_cmds.append(
            'set firewall policer %s filter-specific' % name)
    if logical_bandwidth_policer:
        config_cmds.append(
            'set firewall policer %s logical-bandwidth-policer' % name)
    if logical_interface_policer:
        config_cmds.append(
            'set firewall policer %s logical-interface-policer' % name)
    if physical_interface_policer:
        config_cmds.append(
            'set firewall policer %s physical-interface-policer' % name)
    if shared_bandwidth_policer:
        config_cmds.append(
            'set firewall policer %s shared-bandwidth-policer' % name)
    if limit_type == "if-exceeding":
        if burst_size and bw_limit:
            config_cmds.append(
                'set firewall policer %s if-exceeding bandwidth-limit %s' % (
                    name, bw_limit))
            config_cmds.append(
                'set firewall policer %s if-exceeding burst-size-limit %s' % (
                    name, burst_size))
        elif burst_size and bw_percent:
            config_cmds.append(
                'set firewall policer %s if-exceeding bandwidth-percent %s' % (
                    name, bw_percent))
            config_cmds.append(
                'set firewall policer %s if-exceeding burst-size-limit %s' % (
                    name, burst_size))
        else:
            device.log(
                message="With if-exceeding, you must specify " +
                "burst-size-limit and bandwidth as limit/percent!!!",
                level='error')
            return False
    elif limit_type == "if-exceeding-pps":
        if packet_burst and pps_limit:
            config_cmds.append(
                'set firewall policer %s %s packet-burst %s' % (
                    name, limit_type, packet_burst))
            config_cmds.append(
                'set firewall policer %s %s pps-limit %s' % (
                    name, limit_type, pps_limit))
        else:
            device.log(
                message="With if-exceeding-pps, you must specify " +
                "packet-burst and pps-limit!!!",
                level='error')
            return False
    else:
            device.log(
                message="you must specify limit type correctly", level='error')
            return False
    if isinstance(action, list):
        for act in action:
            config_cmds.append('set firewall policer %s then %s' % (name, act))
    else:
        config_cmds.append('set firewall policer %s then %s' % (name, action))
    result = device.config(command_list=config_cmds).response()
    if re.search(r'invalid|error', result, re.IGNORECASE) or\
            re.search(r'\r\n', result):
        device.log(message="Config set failed on device: %s"
                   % result, level='error')
        return False
    if commit:
        return device.commit().status()
    return True


def get_dcu_counter(device, **kwargs):
    '''
    Get Destination Class Usage counter (packets, bytes) from the interface
        1. show interfaces destination-class Destination Class Usage
        2. get counter of packets, bytes

    :param dcu_name tring:
        REQUIRED name of destination class
    :param interface string or list of string:
        REQUIRED Name of logical interface

    :return dcu_counter:
        values of Destination Class Usage couter (packets, bytes)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Dcu Counter    device=${dev}    interface=xe-0/0/0.1
        ...    dcu_name=dcu
    '''
    valid_keys = ['interface', 'dcu_name']
    required_key = ['interface', 'dcu_name']
    kwargs = check_args(valid_keys, required_key, kwargs)

    dcu_name = kwargs.get('dcu_name')
    interface = kwargs.get('interface')

    function = function_name()
    logging.info(msg="Inside %s" % function)

    dcu_counter = {}
    if isinstance(interface, list):
        for i in interface:
            dcu_counter[i] = get_dcu_counter(device, dcu_name=dcu_name,
                                             interface=i)
        device.log(message="%s: interface(%s) return"
                   % (function, interface) + " " +
                   str(dcu_counter), level='debug')

        return dcu_counter

    cmd_dcu = cmd['show_dcu'] % (dcu_name, interface)
    try:
        rpc_str = device.get_rpc_equivalent(command=cmd_dcu)
        response = device.execute_rpc(command=rpc_str).response()
    except Exception:
        raise Exception('Fail to get the response of dcu counter')

    if response.findall(".//destination-class/dcu-class-name"):
        dcu_names = []
        byte_counts = []
        packet_counts = []

        elements = response.findall(".//destination-class/dcu-class-name")
        for element in elements:
            dcu_names.append(element.text.strip())

        elements = response.findall(
            ".//destination-class/dcu-class-packets")
        for element in elements:
            packet_counts.append(element.text.strip())

        elements = response.findall(".//destination-class/dcu-class-bytes")
        for element in elements:
            byte_counts.append(element.text.strip())

        for dcu_name in dcu_names:
            dcu_counter[dcu_name] = {}

        for i in range(0, len(dcu_names)):
            dcu_counter[dcu_names[i]]['packet_count'] = packet_counts[i]
            dcu_counter[dcu_names[i]]['byte_count'] = byte_counts[i]

    return dcu_counter


def get_scu_counter(device, **kwargs):
    '''
    Get Source Class Usage counter (packets, bytes) from the interface
        1. show interfaces destination-class Source Class Usage
        2. get counter of packets, bytes

    :param scu_name string:
        REQUIRED name of source class
    :param interface string or list of string:
        REQUIRED Name of logical interface

    :return scu_counter:
        values of Source Class Usage couter (packets, bytes)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Scu Counter    device=${dev}    interface=xe-0/0/0.1
        ...    scu_name=scu
    '''
    valid_keys = ['interface', 'scu_name']
    required_key = ['interface', 'scu_name']
    kwargs = check_args(valid_keys, required_key, kwargs)

    scu_name = kwargs.get('scu_name')
    interface = kwargs.get('interface')

    function = function_name()
    logging.info(msg="Inside %s" % function)

    scu_counter = {}
    if isinstance(interface, list):
        for i in interface:
            scu_counter[i] = get_scu_counter(device, scu_name=scu_name,
                                             interface=i)
        device.log(message="%s: interface(%s) return"
                   % (function, interface) + " " +
                   str(scu_counter), level='debug')

        return scu_counter

    cmd_scu = cmd['show_scu'] % (scu_name, interface)
    try:
        rpc_str = device.get_rpc_equivalent(command=cmd_scu)
        response = device.execute_rpc(command=rpc_str).response()
    except Exception:
        raise Exception("Fail to get the response of scu counter")

    if response.findall(".//source-class/scu-class-name"):
        scu_names = []
        byte_counts = []
        packet_counts = []

        elements = response.findall(".//source-class/scu-class-name")
        for element in elements:
            scu_names.append(element.text.strip())

        elements = response.findall(".//source-class/scu-class-packets")
        for element in elements:
            packet_counts.append(element.text.strip())

        elements = response.findall(".//source-class/scu-class-bytes")
        for element in elements:
            byte_counts.append(element.text.strip())

        for scu_name in scu_names:
            scu_counter[scu_name] = {}

        for i in range(0, len(scu_names)):
            scu_counter[scu_names[i]]['packet_count'] = packet_counts[i]
            scu_counter[scu_names[i]]['byte_count'] = byte_counts[i]

    return scu_counter


def clear_vty_syslog(device, **kwargs):
    '''
    This funtion used to clear the PFE (packet forwarding engine) syslog
    messages.

    :param VTY:
        REQUIRED vty name to telnet session from shell mode.

    :return:
        Error if failed to clear syslog message on vty
        True if clear syslog message successfully

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Clear Vty Syslog    device=${dev}    vty=fpc0

    '''
    valid_keys = ['vty']
    required_key = ['vty']
    kwargs = check_args(valid_keys, required_key, kwargs)

    vtys = kwargs.get('vty')

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    if not isinstance(vtys, list):
        vtys = [vtys]

    vty_err = 0
    for vty in vtys:
        res = device.vty(destination=vty, command='clear syslog messages',
                         timeout=10)
        status = res.status()
        if not status:
            device.log(message="%s failed to clear syslog messages on %s" %
                       (function, vty), level='error')
            vty_err += 1
            continue
    if vty_err != 0:
        return False
    return True


def get_vty_syslog(device, **kwargs):
    '''
    This funtion used to get the PFE (packet forwarding engine) syslog
    by using command " show syslog messages'
    messages.

    :param VTY:
         REQUIRED vty name to telnet session from shell mode.

    :return:
         output message vty syslog

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Vty Syslog    device=${dev}    vty=fpc0
    '''
    valid_keys = ['vty']
    required_key = ['vty']
    kwargs = check_args(valid_keys, required_key, kwargs)

    vtys = kwargs.get('vty')

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    if not isinstance(vtys, list):
        vtys = [vtys]

    vty_syslog = ''
    for vty in vtys:
        response = device.vty(destination=vty,
                              command="show syslog messages").response()
        vty_syslog += response
    return vty_syslog


def check_vty_error(device, **kwargs):
    '''
    This funtion used to check the PFE (packet forwarding engine) syslog
    messages.

    :param VTY:
         REQUIRED telnet session from shell mode.
    :param ERROR:
         REQUIRED to check ASIC error

    :return:
         TRUE if error > 0, mean we found the error log when check vty
         FALSE if error = 0, mean we did not found any error log.

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Check Vty Error    device=${dev}    vty=fpc0
        ...    error=Failed to find nh
    '''
    valid_keys = ['vty', 'error']
    required_key = ['vty', 'error']
    kwargs = check_args(valid_keys, required_key, kwargs)

    vtys = kwargs.get('vty')
    error = kwargs.get('error')

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    if not isinstance(vtys, list):
        vtys = [vtys]

    vty_err = 0
    for vty_name in vtys:
        res = device.vty(destination=vty_name,
                         command="show syslog messages")
        response = res.response()
        if re.search(r"LOG:\s+Err.*%s.*" % error, response, re.DOTALL):
            device.log(message="%s vty %s syslog error" %
                       (function, vty_name) + response, level='warn')
            vty_err += 1

    if vty_err > 0:
        return True
    else:
        device.log(message="%s failed no LOG: Err %s" % (function, vty_err),
                   level='error')

        return False


def get_firewall_psp(device, **kwargs):
    '''
    Get firewall prefix specific action policer by doing the following
    actions:
    - show firewall prefix-action-stats filter by xml format
    - Get 'packet-count' and 'byte-count' in
    firewall-prefix-action-information

    :param filter:
        REQUIRED Name of a filter (string)
    :param prefix_action:
        REQUIRED Name of a prefix action (string)
    :param from:
        OPTION Starting policer or policer (string). Default: 0
    :param to:
        OPTION Ending policer or policer (string). Default: 65535

    :return:
        psp_counter (dict).
        Eg: psp_counter = {
            'policer_name1': {'byte_count': '1','packet_count': '5'},
            'policer_name2': {'byte_count': '3', 'packet_count': '25'},
            'policer_name3': {'byte_count': '2', 'packet_count': '15'}
            }

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Firewall Psp    device=${dev}
        ...    filter=limit-source-one-24
        ...    prefix_action=psa-1Mbps-per-source-24-32-256-one
        ...    from=${0}    to=${3}
    '''
    # Check parameter
    valid_keys = ['filter', 'prefix_action', 'from', 'to']
    required_key = ['filter', 'prefix_action']
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs['filter']
    prefix_action = kwargs['prefix_action']
    _from = kwargs.get('from', 0)
    _to = kwargs.get('to', 65535)
    psp_counter = {}

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    cfg_cmd = cmd['show_fw_pre_action'] % (_filter, prefix_action,
                                           _from, _to)

    rpc_str = device.get_rpc_equivalent(command=cfg_cmd)
    response = device.execute_rpc(command=rpc_str).response()

    policer_names = []
    byte_counts = []
    packet_counts = []

    elements = response.findall(".//policer/policer-name")
    for element in elements:
        policer_names.append(element.text.strip())
    for policer_name in policer_names:
        psp_counter[policer_name] = {}

    elements = response.findall(".//policer/byte-count")
    for element in elements:
        byte_counts.append(element.text.strip())

    elements = response.findall(".//policer/packet-count")
    for element in elements:
        packet_counts.append(element.text.strip())

    for i in range(0, len(policer_names)):
        psp_counter[policer_names[i]]['packet_count'] = packet_counts[i]
        psp_counter[policer_names[i]]['byte_count'] = byte_counts[i]

    return psp_counter


def get_filter_index(device, **kwargs):

    '''
    Get filter index when show the filter on
    Packet Forwarding Engine

    :param pfe:
        OPTION Packet Forwarding Engine name
    :param filter:
        OPTION name of filter
    :param interface:
        OPTION interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param input:
        OPTION to set filter name: filter += "i".
        1 | 0 (default it 1 if if_specific)
    :param output:
        OPTION to set filter name: filter += "o".
        1 | 0 (default is 0 if if_specific)
    :param family:
        OPTION to set family type. Eg: inet|inet6|vpls|mpls|ccc
    :param if_specific:
        OPTION 1 if use interface name | 0 if use filter (default is 0)

    :return filter_index:int
        The index of filter

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get Filter Index    device=${dev}    filter=icmp_syslog
        ...    pfe=fpc0
    '''
    fun = function_name()
    logging.info(msg="Inside %s function" % fun)

    valid_keys = ['pfe', 'filter', 'interface', 'input',
                  'output', 'if_specific', 'family']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    # get params
    _filter = kwargs.get('filter')
    pfe = kwargs.get('pfe')
    if_specific = kwargs.get('if_specific')
    interface = kwargs.get('interface')
    family = kwargs.get('family')

    # check if_specific
    if if_specific:
        _input = kwargs.get('input', 1)
        _output = kwargs.get('output', 0)
        if interface:
            device.log(message='%s: interface (%s)' % (fun, interface),
                       level='debug')
        else:
            raise Exception('%s : argument "interface" is required for '
                            'interface-specific filter' % fun)

        if _input and _output:
            raise Exception('%s : cannot specifiy both input '
                            'and output options' % fun)
        if _filter:
            _filter = _filter + "-" + interface
        else:
            _filter = interface
        if family:
            _filter = _filter + "-" + family
        if _input:
            _filter = _filter + "-i"
        if _output:
            _filter = _filter + "-o"
    if not _filter:
        return None
    device.log(message="%s:  before get filter(%s) index on pfe(%s)... " % (
        fun, _filter, pfe), level='debug')
    if not pfe:
        pfe = get_pfe_list(device, interface=interface)[0]
    device.log(message="%s: get filter(%s) index on pfe(%s)..." % (
        fun, _filter, pfe), level='debug')
    rsp = __cprod(device, name=pfe, cmd="show filter")
    for line in rsp:
        if _filter in line:
            return int(line.strip().split(' ')[0])


def __cprod(device, **kwargs):
    '''
        To run cprod commands
        :params name:
            REQUIRED Packet Forwarding Engine name
        :params option:
            REQUIRED cprod option:
               -t = test mode, doesn't connect to SCB, just parses files
               -d = set debugging level
               -o = select output file, ("standard out" if none specified)
               -c = execute the next argument(s) as a one-shot command
               -w = manually set the timeout value
               -z = set the timeout after cprod finishes a batch script
               -s = use specified port, numeric port or well-known app(idp)
               -J = use the __juniper_private3__ routing instance
        :params cmd:
            Command

        :return response object
    '''
    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)
    name = ''
    dst_addr = ''
    option = kwargs.get('option')

    if kwargs.get('name'):
        name = kwargs.get('name')
    elif not option:
        raise Exception('%s: Name is required unless there are options '
                        'present' % function)
    if not kwargs.get('cmd') and not option:
        raise Exception('%s: Either cmd or cmd_array must be specified unless '
                        'there are options present' % function)

    # login as root
    device.su()

    if name:
        if device.get_version() == '5.4':
            dst_addr = name
        else:
            dst_addr = __get_dst_addrss(device, name)

        cmd = "cprod -A %s" % dst_addr
    else:
        cmd = "cprod"
    if option:
        cmd += option
    time_out = kwargs.get('time_out', 60)
    cmd += ' -c "%s"' % kwargs.get('cmd')
    rsp = device.shell(command=cmd, timeout=time_out).response()
    # exit root sudoer
    device.shell(command='exit')
    return rsp.splitlines()


def __get_dst_addrss(device, pfe=''):
    '''
        Get the TNP address for a pfe name
        :params pfe:
            REQUIRED Packet Forwarding Engine name
    '''
    result = device.shell(command='tnpdump').response()
    if result:
        addr = re.search(r"%s\s+(.*)\s+\w{2}:" % pfe, result)
        if addr:
            return addr.group(1)
        else:
            device.log(message='No such vty %s' % pfe, level='error')
            return ''


def check_firewall_psp(device, **kwargs):
    '''
    Check firewall prefix action information of policers (packets)
    with expected packets value

    :param filter:
        REQUIRED name of filter
    :param prefix_action:
        REQUIRED name of Prefix-action
    :param index:
        OPTION  counter or policer (0..65535)
    :param packet:
        REQUIRED name of the packet
    :param chk_count:
        REQUIRED integer value: use for loops
    :param chk_interval:
        REQUIRED timer for a loop excution

    :return True/False:
        True if packet = expected packet
        False if packet # expected packet

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${packet} =    Create List    ${0}    ${40000}
        ${result} =    Check Firewall Psp    device=${dev}
        ...    filter=limit-source-one-24
        ...    prefix_action=psa-1Mbps-per-source-24-32-256-one
        ...    index=${3}    packet=${packet}
    '''
    # Check parameter
    valid_keys = ['filter', 'prefix_action', 'index', 'packet',
                  'chk_count', 'chk_interval']
    required_key = ['filter', 'prefix_action', 'packet']
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs.get('filter')
    prefix_action = kwargs.get('prefix_action')
    index = kwargs.get('index')
    packet = kwargs.get('packet')
    chk_count = kwargs.get('chk_count', 1)
    chk_interval = kwargs.get('chk_interval', 10)

    function = function_name()
    device.log(message="%s: packet(%s)" % (function, packet), level='debug')

    packet_ok = 0
    for i in range(0, chk_count):
        if i > 0:
            time.sleep(chk_interval)
        param = {'filter': _filter, 'prefix_action': prefix_action,
                 'from': index, 'to': index}
        psp_counter = get_firewall_psp(device, **param)
        packets_count = []
        if psp_counter:
            for key in psp_counter.keys():
                packets_count.append(psp_counter[key]['packet_count'])

            if packet_ok:
                break
            else:
                if __check_value(packets_count, packet):
                    packet_ok = 1

    if packet_ok:
        device.log(message="%s: packet checking passed" % function,
                   level='info')
        return True

    device.log(message="%s: packet checking failed" % function,
               level='warn')
    return False


def set_firewall_syslog(device, **kwargs):
    '''
        This funtion used to set or activate the firewall syslog

        :param activate:
            OPTIONAL ACTIVATE for command.
        :param log_file:
            OPTION to point the file or messages need to get.
            Default is 'messages'
        :param log_level:
            OPTION to choose the level we want to set or information .
            Default is 'info'

        :return:
            TRUE if no error. not expect FALSE.

        Robot Usage Example  :
            ${dev} =    Get Handle   resource=device0
            ${result} =    Set Firewall Syslog    device=${dev}    activate=set
            ...    log_file=messages
            ...    commit=${1}    log_level=info
    '''
    valid_keys = ['log_file', 'log_level', 'activate', 'commit']
    required_key = []

    kwargs = check_args(valid_keys, required_key, kwargs)

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)
    log_file = kwargs.get('log_file', 'messages')
    log_level = kwargs.get('log_level', 'info')
    activate = kwargs.get('activate')
    commit = kwargs.get('commit')

    if activate:
        cmd = kwargs['activate']
    else:
        cmd = 'set'

    cfg_cmd_ = "%s system syslog file %s firewall %s" % (cmd, log_file,
                                                         log_level)

    result = device.config(command_list=[cfg_cmd_]).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s" % result,
                   level='error')
        return False

    if commit:
        return device.commit().status()
    return True


def set_firewall_filter(device, **kwargs):
    '''
    This funtion used to set and apply firewall filter to interfaces.

    :param filter:
        REQUIRED kind of filter for command include: filter, simple_filter
        service. Default is 'filter'.
    :param filter_name
        OPTIONAL name of filter
    :param family:
        OPTIONAL  faminy name for command like net|any|inet6|mpls.
        Default is 'inet'.
    :param interface:
        REQUIRED Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param commit:
        OPTIONAL Commit after configuration? Default is 0.
    :param input:
        OPTIONAL input 0|1 apply filter to input interface.
    :param ouptut:
        OPTIONAL input 0|1 apply filter to input interface
    :param if_specific:
        OPTIONAL 0|1 interface specific. Need it for check_filter_install()
    :param service_set:
        OPTIONAL 0|1 interface running interface service
    :param chk_count:
        REQUIRED chk_count command to check number of retries
        for check_filter_install()
    :param chk_interval:
        OPTIONAL chk_interval to check Seconds between retries
        for check_filter_install()

    :return:
        TRUE if filter is loaded on PFE
        FALSE if filter not loaded on PFE

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Set Firewall Filter    device=${dev}
        ...    interface=ge-0/0/2.0    family=inet    filter=icmp_syslog
        ...    input=${1}    commit=${1}    chk_count=${1}

    '''
    valid_keys = ['filter', 'family', 'interface', 'input',
                  'activate', 'output', 'commit', 'chk_count', 'service_set',
                  'chk_interval', 'interface', 'if_specific', 'filter_name']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)

    function = function_name()
    logging.info(msg='Inside %s function' % function)
    family = kwargs.get('family', 'inet')
    _filter = kwargs.get('filter')
    _filter_name = kwargs.get('filter_name')
    activate = kwargs.get("activate")
    interface = kwargs.get('interface')
    service_set = kwargs.get('service_set')
    _input = kwargs.get('input', 1)
    output = kwargs.get('output', 1)
    chk_count = kwargs.get('chk_count')
    chk_interval = kwargs.get('chk_interval', 10)
    if_specific = kwargs.get('if_specific')
    commit = kwargs.get('commit')

    # set input if neither input nor output is specified

    if activate:
        cmd = kwargs.get('activate')
    else:
        cmd = 'set'
    if not isinstance(interface, list):
        interface = [interface]

    if not isinstance(_filter_name, list):
        _filter_name = [_filter_name]
    command_list = []
    for ifl in interface:
        unit = 0
        ifd = ifl
        matched = re.search(r"^(\S+)\.(\d+)$", ifl)
        if matched:
            ifd = matched.group(1)
            unit = matched.group(2)
        if _filter == 'filter':
            if _input:
                for filter_name in _filter_name:
                    cfg_cmd_ = "%s interfaces %s " % (cmd, ifd) +\
                        "unit %s family %s %s input-list %s" % (unit, family,
                                                                _filter,
                                                                filter_name)
                    command_list.append(cfg_cmd_)

            if output:
                for filter_name in _filter_name:
                    cfg_cmd_ = "%s interfaces %s unit %s" % (cmd, ifd, unit) +\
                        " family %s %s" % (family, _filter) +\
                        " output-list %s" % (filter_name)
                    command_list.append(cfg_cmd_)

        if _filter == 'simple-filter':
            if _input:
                for filter_name in _filter_name:
                    cfg_cmd_ = "%s interfaces %s " % (cmd, ifd) +\
                        "unit %s family %s " % (unit, family) +\
                        "%s input %s" % (_filter, filter_name)
                    command_list.append(cfg_cmd_)
            if output:
                for filter_name in _filter_name:
                    cfg_cmd_ = "%s interfaces %s " % (cmd, ifd) +\
                        "unit %s family %s %s output %s" % (unit, family,
                                                            _filter,
                                                            filter_name)
                command_list.append(cfg_cmd_)

        if _filter == 'service':
            if _input:
                for filter_name in _filter_name:
                    cfg_cmd_ = '%s interfaces %s ' % (cmd, ifd) +\
                        'unit %s family %s %s ' % (unit, family, _filter) +\
                        'input service-set %s service-filter %s' % (
                            service_set, filter_name)
                    command_list.append(cfg_cmd_)
                    cfg_cmd_ = '%s interfaces %s ' % (cmd, ifd) +\
                        'unit %s family %s %s ' % (unit, family, _filter) +\
                        'input post-service-filter %s' % (filter_name)
                    command_list.append(cfg_cmd_)
            if output:
                for filter_name in _filter_name:
                    cfg_cmd_ = '%s interfaces %s ' % (cmd, ifd) +\
                        'unit %s family %s %s ' % (unit, family, _filter) +\
                        'output service-set %s service-filter %s' % (
                            service_set, filter_name)
                    command_list.append(cfg_cmd_)

    result = device.config(command_list=command_list).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config filter set failed on device: %s"
                   % result, level='error')
        return False

    # Make sure to commit before check filter installed ok on PFE
    if commit:
        device.commit()
    if chk_count:
        for filter_name in _filter_name:
            if check_filter_install(device, **{'filter': filter_name,
                                               'interface': interface,
                                               'if_specific': if_specific,
                                               'input': _input,
                                               'output': output,
                                               'chk_count': chk_count,
                                               'chk_interval': chk_interval}):
                device.log(message="%s: check_filter_install() %s"
                           % (function, filter_name), level='info')
            else:
                device.log(message="%s: check_filter_install() %s"
                           % (function, filter_name), level='error')
    return True


def set_firewall_policer(device, **kwargs):
    '''
    This funtion used to set firewall policer

    :param policer:
        REQUIRED policer name for command. Default is 'policer'.
    :param family:
        OPTIONAL  faminy name for command like net|any|inet6|mpls.
        Default is 'inet'.
    :param interface:
        OPTIONAL Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param commit:
        OPTIONAL Commit after configuration? Default is 0.
    :param input:
        REQUIRED input 0|1 apply policer to input interface.
    :param ouptut:
        OPTIONAL input 0|1 apply policer to input interface
    :param chk_count:
        REQUIRED chk_count command to check number of retries
        for check_filter_install()
    :return:
        TRUE if policer is loaded on PFE
        FALSE if policer not loaded on PFE

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Set Firewall Policer    device=${dev}    activate=set
        ...    chk_count=${0}    interface=lo0    policer=1Mbps-policer
        ...    commit=${1}    input=${1}

    '''
    valid_keys = ['policer', 'family', 'if_specific',
                  'input', 'activate', 'output', 'commit', 'chk_count',
                  'chk_interval', 'interface']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)
    function = function_name()
    logging.info(msg='Inside %s function' % function)
    family = kwargs.get('family', 'inet')
    policer = kwargs.get('policer', 'policer')
    activate = kwargs.get("activate")
    interface = kwargs.get('interface')
    _input = kwargs.get('input')
    output = kwargs.get('output')
    chk_count = kwargs.get('chk_count')
    chk_interval = kwargs.get('chk_interval', '10')
    if_specific = kwargs.get('if_specific')
    commit = kwargs.get('commit')

    # set input if neither input nor output is specified
    command_list = []
    if not (_input or output):
        _input = 1
        output = 1
    if activate:
        cmd = kwargs.get('activate')
    else:
        cmd = 'set'
    if not isinstance(interface, list):
        interface = [interface]

    for ifl in interface:
        (ifd, unit) = (ifl, 0)
        matched = re.search(r"^(\S+)\.(\d+)$", ifl)
        if matched:
            ifd = matched.group(1)
            unit = matched.group(2)
        if _input:
            cfg_cmd_ = '%s interfaces %s ' % (cmd, ifd) +\
                'unit %s family %s' % (unit, family) +\
                ' policer input %s' % policer
            command_list.append(cfg_cmd_)
        if output:
            cfg_cmd_ = '%s interfaces %s ' % (cmd, ifd) +\
                'unit %s family %s' % (unit, family) +\
                ' policer output %s' % policer
            command_list.append(cfg_cmd_)

    result = device.config(command_list=command_list).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s"
                   % result, level='error')
        return False

    # Make sure to commit before check filter installed ok on PFE
    if commit:
        device.commit()
    if chk_count:
        if not check_filter_install(device, **{'filter': policer,
                                               'interface': interface,
                                               'if_specific': if_specific,
                                               'input': _input,
                                               'output': output,
                                               'chk_count': chk_count,
                                               'chk_interval': chk_interval}):
            device.log(message="%s: check_filter_install() failed" % function,
                       level='error')

    return True


def set_ftf_filter(device, **kwargs):
    '''
    This funtion used to set and apply forwarding table filter to
    interfaces

    :param filter:
        REQUIRED filter name for command. Default is 'ftf'.
    :param family:
        OPTIONAL  faminy name for command like net|any|inet6|mpls.
        Default is 'inet'.
    :param commit:
        OPTIONAL Commit after configuration? Default is 0.
    :param input:
        REQUIRED input 0|1 apply filter to input interface.
    :param ouptut:
        REQUIRED input 0|1 apply filter to input interface
    :return:
        TRUE if filter is loaded on PFE
        FALSE if filter not loaded on PFE

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Set Ftf Filter    device=${dev}    interface=ge-2/0/2
        ...    commit=${1}    filter=limit-source-one-24
        ...    routing_instance=FTF_FILTER    activate=set    chk_count=${0}
    '''
    valid_keys = ['commit', 'activate', 'routing_instance', 'interface',
                  'family', 'chk_count', 'chk_interval', 'filter']
    required_key = ['filter']
    kwargs = check_args(valid_keys, required_key, kwargs)
    function = function_name()
    logging.info(msg='Inside %s function' % function)
    family = kwargs.get('family', 'inet')
    interface = kwargs.get('interface')
    routing_instance = kwargs.get('routing_instance')
    chk_count = kwargs.get('chk_count')
    _filter = kwargs.get('filter', 'ftf')
    chk_interval = kwargs.get('chk_interval', 10)
    cfg_cmd_ = kwargs.get('activate', 'set')
    commit = kwargs.get('commit')

    if routing_instance:
        cfg_cmd_ += "  routing-instances %s" % routing_instance

    cfg_cmd_ += " forwarding-options family %s filter input %s" % \
                (family, _filter)

    result = device.config(command_list=[cfg_cmd_]).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s" % result,
                   level='error')
        return False

    # Make sure to commit before check filter installed ok on PFE
    if commit:
        device.commit()
    if chk_count:
        if not check_filter_install(device, **{'filter': _filter,
                                               'chk_count': chk_count,
                                               'chk_interval': chk_interval,
                                               'interface': interface}):
            device.log(message="%s: check_filter_install() failed)"
                       % function, level='debug')
    return True


def set_sampling(device, **kwargs):
    '''
    This funtion used to enable traffic sampling of a physical interface.

    :param activate:
        OPTIONAL ACTIVATE for command.
    :param family:
        OPTIONAL  faminy name for command like net|any|inet6|mpls.
        Default is 'inet'.
    :param if:
        OPTIONAL Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param commit:
        REQUIRED Commit after configuration? Default is 0.
    :param input:
        REQUIRED input 0|1 apply filter to input interface.
    :param ouptut:
        REQUIRED input 0|1 apply filter to input interface
    :param chk_count:
        REQUIRED chk_count command to check number of retries
        for check_filter_install()
    :param chk_interval:
        REQUIRED chk_interval to check Seconds between retries
        for check_filter_install()

    :return:
        TRUE if the commit is successful
        FALSE if the commit is not successful

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Set Sampling    device=${dev}    interface=ge-2/0/2
        ...    input=${1}    commit=${1}
    '''
    valid_keys = ['policer', 'family', 'interface', 'input',
                  'activate', 'output', 'commit', 'interface']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)

    function = function_name()
    logging.info(msg='Inside %s function' % function)
    family = kwargs.get('family', 'inet')
    interface = kwargs.get('interface')
    _input = kwargs.get('input')
    output = kwargs.get('output')
    _cmd = kwargs.get('activate', 'set')
    commit = kwargs.get('commit')

    # set input if neither input nor output is specified
    if not (_input or output):
        _input = 1
        output = 1

    if not isinstance(interface, list):
        interface = [interface]

    for ifl in interface:
        unit = 0  # default value
        ifd = ifl
        check = re.search(r'^(\S+)\.(\d+)$', ifl)
        if check:
            ifd = check.group(1)
            unit = check.group(2)

        cfg_cmd = cmd['set_sampling'] % (_cmd, ifd, unit, family)

        if _input:
            cfg_cmd += " input"
        if output:
            cfg_cmd += " output"

        res_config = device.config(command_list=[cfg_cmd]).response()
        if re.search(r'invalid|error', res_config):
            device.log(message="%s sampling fail" % _cmd, level="error")
            return False

    if commit:
        return device.commit().status()
    return True


def delete_firewall_syslog(device, **kwargs):
    '''
    Deactivate of delete firewall syslog
        - deactivate/delete firewall family/filter/term

    :param negative:
        OPTION if it is set, call method commit with
        argument is negative
    :param file:
        OPTION name of file in which to log data
    :param level:
        OPTION log level: alert/any/critical/emergency/...
    :param deactivate:
        OPTION deactivate configuration
    :param commit:
        OPTION if commit value is defined, will commit the
        configuration to device

    :return True/False:
        - True when commit successful
        - False when commit fail

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Delete Firewall Syslog    device=${dev}
        ...    deactivate=deactivate    level=${0}    file=abc    commit=${1}
    '''
    valid_keys = ['deactivate', 'level', 'file', 'commit']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    log_level = kwargs.get('level')
    log_file = kwargs.get('file', 'messages')
    commit = kwargs.get('commit')

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    cfg_cmd = kwargs.get('deactivate', 'delete')
    cfg_cmd += " system syslog file %s firewall" % log_file

    if log_level:
        cfg_cmd += " %s" % log_level

    result = device.config(command_list=[cfg_cmd]).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s" % result,
                   level='error')
        return False

    if commit:
        return device.commit().status()
    return True


def delete_firewall(device, **kwargs):
    '''
    Deactivate of delete firewall by command:
        - deactivate/delete firewall family inet/inet6 filter filter_name
        term term_name

    :param filter:
        REQUIRED name of filter
    :param family:
        OPTION protocol family: inet, inet6, ...
    :param term:
        REQUIRED name of term for routing policy
    :param deactivate:
        OPTION deactivate configuration
    :param commit:
        OPTION if commit value is defined, will commit the
        configuration to device

    :return True/False:
        - True when commit successful
        - False when commit fail

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Delete Firewall    device=${dev}
        ...    deactivate=deactivate    family=inet    filter=filter-name
        ...    term=term-name    commit=${1}
    '''
    valid_keys = ['filter', 'family', 'term', 'deactivate',
                  'commit']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    _filter = kwargs.get('filter')
    family = kwargs.get('family')
    term = kwargs.get('term')
    cfg_cmd = kwargs.get('deactivate', 'delete')
    commit = kwargs.get('commit')

    cfg_cmd += " firewall"

    if family:
        cfg_cmd += " family %s" % family
    if _filter:
        cfg_cmd += " filter %s" % _filter
    if term:
        cfg_cmd += " term %s" % term

    result = device.config(command_list=[cfg_cmd]).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s" % result,
                   level='error')
        return False

    if commit:
        return device.commit().status()
    return True


def delete_firewall_filter(device, **kwargs):
    '''
    Deactivate or delete firewall filter

    :param negative:
        OPTION if it is set, call method commit with
        argument is negative
    :param filter:
        OPTION name of filter
    :param family:
        OPTION protocol family: inet, inet6, ...
    :param interface:
        REQUIRED Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param input:
        OPTION filter to be applied to received packets
    :param output:
        OPTION filter to be applied to transmitted packets
    :param deactivate:
        OPTION to deactivate configuration
    :param commit:
        OPTION commit and load configuration. Default is 0
    :param chk_count:
        REQUIRED integer value: use for loops
    :param chk_interval:
        REQUIRED interval for each loop
    :param if_specific:
        REQUIRED name of interface

    :return True/False:
        - True when commit true and not error
        - False when commit fail or error

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Delete Firewall Filter    device=${dev}
        ...    filter=icmp_syslog    family=inet    interface=ge-0/0/2
        ...    input=input    chk_count=${1}    chk_interval=${1}
        ...    commit=${1}    deactivate=deactivate
    '''
    valid_keys = ['commit', 'filter', 'deactivate', 'interface', 'family',
                  'input', 'output', 'chk_count', 'chk_interval',
                  'if_specific']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs.get('filter', 'filter')
    family = kwargs.get('family', 'inet')
    interface = kwargs.get('interface')
    _input = kwargs.get('input')
    output = kwargs.get('output')
    chk_count = kwargs.get('chk_count')
    chk_interval = kwargs.get('chk_interval')
    if_specific = kwargs.get('if_specific')
    commit = kwargs.get('commit')
    cmd = kwargs.get('deactivate', 'delete')

    function = function_name()
    logging.info(msg="Inside %s" % function)

    if not (_input or output):  # remove both input/output by default
        _input = 1
        output = 1

    if not isinstance(interface, list):
        interface = [interface]
    command_list = []
    for ifl in interface:
        ifd = ifl
        unit = 0  # default value
        check = re.search(r'^(\S+)\.(\d+)$', ifl)
        if check:
            ifd = check.group(1)
            unit = check.group(2)

        cfg_cmd = '%s interfaces %s unit %s family %s' % (cmd, ifd, unit,
                                                          family)
        if _input:
            cfg_cmd = cfg_cmd + ' filter input'
            command_list.append(cfg_cmd)
        if output:
            cfg_cmd = cfg_cmd + ' filter output'
            command_list.append(cfg_cmd)
    result = device.config(command_list=command_list).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s"
                   % result, level='error')
        return False

    if commit:
        device.commit()

    if chk_count and chk_count > 0:
        if not check_filter_install(device, **{'filter': _filter,
                                               'interface': interface,
                                               'if_specific': if_specific,
                                               'input': _input,
                                               'output': output,
                                               'chk_count': chk_count,
                                               'chk_interval': chk_interval}):
            device.log(message="%s: check_filter_install() shows filter"
                       % function, level='error')

    return True


def delete_firewall_policer(device, **kwargs):
    '''
    Deactivate or delete firewall policer

    :param policer:
        OPTION name of policer
    :param family:
        OPTION protocol family: inet, inet6, ...
    :param interface:
        REQUIRED Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param input:
        OPTION filter to be applied to received packets
    :param output:
        OPTION filter to be applied to transmitted packets
    :param deactivate:
        OPTION to deactivate configuration
    :param commit:
        OPTION commit and load configuration. Default is 0
    :param chk_count:
        OPTION integer value: use for loops
    :param chk_interval:
        OPTION timer for a loop excution

    :return True/False:
        - True when commit successfully and no error
        - False when commit fail or error

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{param} =    Create Dictionary    policer=policer    family=inet
        ...    interface=ge-2/0/7    input=input    output=output
        ...    chk_count=${5}    chk_interval=${10}    commit=${1}
        ...    deactivate=deactivate
        ${result} =    Delete Firewall Policer    device=${dev}    &{param}
    '''
    valid_keys = ['policer', 'family', 'interface', 'input',
                  'output', 'chk_count', 'chk_interval',
                  'deactivate', 'commit']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs.get('policer')
    family = kwargs.get('family', 'inet')
    interface = kwargs.get('interface')
    _input = kwargs.get('input')
    output = kwargs.get('output')
    chk_count = kwargs.get('chk_count')
    chk_interval = kwargs.get('chk_interval')
    commit = kwargs.get('commit')
    _cmd = kwargs.get('deactivate', 'delete')

    function = function_name()
    logging.info(msg="Inside %s" % function)

    if not isinstance(interface, list):
        interface = [interface]
    command_list = []
    for ifl in interface:
        ifd = ifl
        unit = 0  # default value
        check = re.search(r'^(\S+)\.(\d+)$', ifl)
        if check:  # i.e. so-1/0/0.1
            ifd = check.group(1)
            unit = check.group(2)
        if not (_input or output):
            _input = 1
            output = 1

        if _input and output:
            cfg_cmd = cmd['set_policer'] % (_cmd, ifd, unit, family)
            command_list.append(cfg_cmd)
        elif _input:
            cfg_cmd = cmd['set_policer'] % (_cmd, ifd, unit, family)
            cfg_cmd = cfg_cmd + ' input'
            command_list.append(cfg_cmd)
        else:
            cfg_cmd = cmd['set_policer'] % (_cmd, ifd, unit, family)
            cfg_cmd = cfg_cmd + ' output'
            command_list.append(cfg_cmd)

    result = device.config(command_list=command_list).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s"
                   % result, level='error')
        return False

    if commit:
        device.commit()
    # Make sure to commit before calling check_filter_install()

    if chk_count and chk_count > 0:
        # Need to check if filter is loaded on PFE
        for i in ['i', 'o']:
            if i == 'i':
                if not _input:
                    continue
            else:
                if not output:
                    continue
            if check_filter_install(device, **{'filter': _filter,
                                               'interface': interface,
                                               'chk_count': chk_count,
                                               'chk_interval': chk_interval}):
                device.log(message='%s: check_filter_install(filter=filter) \
                            FAIL' % function)
            else:
                device.log(message='%s: check_filter_install(filter=_filter) \
                            PASS' % function)
    return True


def delete_forwarding_table_filter(device, **kwargs):
    '''
    Deactivate or Delete the deactivated Forwarding Table Filters

    :param filter string:
        OPTION name of filter
    :param family string:
        OPTION protocol family: inet, inet6, ...
    :param deactivate string:
        OPTION deactivate cofiguration
    :param routing_instance string:
        OPTION name of routing-instance
    :param commit:
        OPTION commit configuration
    :param chk_count integer:
        OPTION integer value: use for loops
    :param chk_interval integer:
        OPTION timer for a loop excution

    :return True/False:
        - True when commit successfully and no error
        - False when commit not successfully or error

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{param} =    Create Dictionary    filter=icmp_syslog    family=inet
        ...    interface=ge-0/0/2.0    routing_instance=abc    chk_count=${5}
        ...    chk_interval=${10}    commit=${1}
        ...    deactivate=deactivate
        ${result} =    Delete Forwarding Table Filter    device=${dev}
        ...    &{param}
    '''
    valid_keys = ['filter', 'family', 'routing_instance',
                  'chk_count', 'chk_interval', 'commit', 'deactivate',
                  'interface']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs.get('filter', 'filter')
    family = kwargs.get('family', 'inet')
    routing_instance = kwargs.get('routing_instance')
    chk_count = kwargs.get('chk_count')
    chk_interval = kwargs.get('chk_interval')
    commit = kwargs.get('commit')
    action = kwargs.get('deactivate', 'delete')
    interface = kwargs.get('interface')
    cfg_cmd = action

    function = function_name()
    logging.info(msg="Inside %s" % function)

    if routing_instance:
        cfg_cmd += " routing-instances %s" % routing_instance
    cfg_cmd += " forwarding-options family %s filter input" % family

    result = device.config(command_list=[cfg_cmd]).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s" % result,
                   level='error')
        return False

    if commit:
        device.commit()

    if chk_count and chk_count > 0:
        param = {'filter': _filter, 'chk_count': chk_count,
                 'chk_interval': chk_interval, 'interface': interface}
        if check_filter_install(device, **param):
            device.log(message="%s: check_filter_install() still show filter"
                       % function)

    return True


def delete_sampling(device, **kwargs):
    '''
    Deactivate or Delete sampling from interface

    :param family:
        OPTION protocol family: inet, inet6, ...
    :param interface:
        REQUIRED Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param input:
        OPTION filter to be applied to received packets
    :param output:
        OPTION filter to be applied to transmitted packets
    :param deactivate:
        OPTION deactivate configuration
    :param commit:
        OPTION commit and load configuration. Default is 0

    :return True/False:
        - True when commit successful or no error
        - False when commit fail or error

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{param} =    Create Dictionary    interface=ge-2/0/2
        ...    deactivate=deactivate    commit=${1}
        ${result} =    Delete Sampling    device=${dev}    &{param}
    '''
    valid_keys = ['commit', 'deactivate', 'interface', 'family',
                  'input', 'output']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)

    function = function_name()
    logging.info(msg="Inside %s" % function)

    family = kwargs.get('family', 'inet')
    interface = kwargs.get('interface')
    _input = kwargs.get('input')
    output = kwargs.get('output')
    _cmd = kwargs.get('deactivate', 'delete')
    commit = kwargs.get('commit')

    if not isinstance(interface, list):
        interface = [interface]

    for ifl in interface:
        unit = 0  # default value
        ifd = ifl
        interface_matched = re.search(r'^(\S+)\.(\d+)$', ifl)
        if interface_matched:
            ifd = interface_matched.group(1)
            unit = interface_matched.group(2)
        cfg_cmd = cmd['set_sampling'] % (_cmd, ifd, unit, family)
        if not (_input and output):
            if _input:
                cfg_cmd += " input"
            if output:
                cfg_cmd += " output"

        result = device.config(command_list=[cfg_cmd]).response()
        if re.search(r'invalid|error', result, re.IGNORECASE):
            device.log(message="%s sampling fail" % _cmd, level="error")
            return False

    if commit:
        return device.commit().status()
    return True


def clear_firewall_counter(device, **kwargs):
    '''
    Clear firewall count with these option:
        - clear firewall filter filter-name counter counter-name
        - clear firewall filter filter-name
        - clear firewall filter all

    :param filter:
        OPTION name of filter
    :param counter:
        OPTION name of counter

    :return True/False:
        - True when clear successful
        - False when clear fail

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =       Create Dictionary    filter=filter    counter=counter
        ${result} =       Clear Firewall Counter    ${dev}  &{kwargs}

    '''
    valid_keys = ['filter', 'counter']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    _filter = kwargs.get('filter')
    counter = kwargs.get('counter')

    function = function_name()
    logging.info(msg="Inside %s" % function)
    command_list = []
    if counter:
        cmd_clear_counter = cmd['clear_filter_counter'] % (_filter, counter)
        command_list.append(cmd_clear_counter)
    elif _filter:
        cmd_filter = cmd['clear_filter'] % _filter
        command_list.append(cmd_filter)
    else:
        cmd_firewall = cmd['clear_firewall_all']
        command_list.append(cmd_firewall)
    result = device.config(command_list=command_list).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="clear firewall filter all failed",
                   level="error")
        return False
    return True


def configure_protocol_dcu(device, **kwargs):
    '''
    Configure Destination Class Usage for a protocol such as BGP etc

    :param commit:
        OPTION commit and load configuration. Default is 0
    :param protocol:
        REQUIRED Protocol such as bgp, ospf etc
    :param interface:
        OPTION Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param name:
        OPTION name Destination Class Usage. Default is 'dcu'

    :return True/False:
        - True when commit successful
        - False when commit fail

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    protocol=vpls    name=dcu
        ...    commit=${1}
        ${result} =    Configure Protocol Dcu    ${dev}    &{kwargs}
    '''
    valid_keys = ['commit', 'interface', 'name', 'protocol']
    required_key = ['protocol']
    kwargs = check_args(valid_keys, required_key, kwargs)

    prot = kwargs.get('protocol')
    interface = kwargs.get('interface')
    name = kwargs.get('name', 'dcu')
    commit = kwargs.get('commit')

    function = function_name()
    logging.info(msg="Inside %s" % function)

    cfg_cmd_1 = cmd['set_from_prot'] % prot
    cfg_cmd_2 = cmd['set_des_class'] % name
    cfg_cmd_3 = cmd['set_forwarding_table'] % name
    cmd_list = [cfg_cmd_1, cfg_cmd_2, cfg_cmd_3]
    result = device.config(command_list=cmd_list).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="configure protocol dcu failed", level="error")
        return False

    if interface:
        set_dcu(device, interface=interface)

    if commit:
        return device.commit().status()
    return True


def set_dcu(device, **kwargs):
    '''
    Apply Destination Class Usage to interfaces

    :param commit:
        OPTION commit and load configuration. Default is 0
    :param interface:
        REQUIRED interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param family:
        OPTION protocol family: inet, inet6, ...

    :return True/False:
        - True when commit successful: error = 0
        - False when commit fail: error # 0

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    interface=ge-0/0/2    commit=${1}
        ${result} =    Set Dcu  ${dev}    &{kwargs}
    '''
    valid_keys = ['commit', 'interface', 'family']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)
    family = kwargs.get('family', 'inet')
    interface = kwargs.get('interface')
    commit = kwargs.get('commit')
    function = function_name()
    logging.info(msg="Inside %s" % function)

    if not isinstance(interface, list):
        interface = [interface]

    for ifl in interface:
        unit = 0
        matched = re.search(r"^(\S+)\.(\d+)$", ifl)
        if matched:
            unit = matched.group(2)

        ver = device.get_version()

        if matched:
            ver = matched.group(1)

        if ver == "5.4":
            cfg_cmd = ["set interfaces %s unit %s family %s" %
                       (ifl, unit, family) + " destination-class-usage"]
            result = device.config(command_list=cfg_cmd).response()
            if re.search(r'invalid|error', result, re.IGNORECASE):
                device.log(message="%s set dcu pass" % cfg_cmd, level="error")
                return False
        else:
            cfg_cmd = [
                "set interfaces %s unit %s family %s" % (ifl, unit, family) +
                " accounting destination-class-usage"]

            result = device.config(command_list=cfg_cmd).response()
            if re.search(r'invalid|error', result, re.IGNORECASE):
                device.log(message="%s set dcu fail" % cfg_cmd, level="error")
                return False

    if commit:
        return device.commit().status()


def configure_rpf_feasible(device, **kwargs):
    '''
        This funtion used to config uRPF (unicast reverse path) feasible by
        using the command "set routing-options forwarding-table
        unicast-reverse-path feasible-paths"

        :param commit:
            REQUIRED Commit after configuration? Default is 0.

        :return:
            TRUE when no error on commit. Not expect FALSE.

        Robot Usage Example  :
            ${dev} =    Get Handle   resource=device0
            &{kwargs} =    Create Dictionary    commit=${1}
            ${result} =    Configure Rpf Feasible    ${dev}  &{kwargs}
    '''
    valid_keys = ['commit']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)
    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    commit = kwargs.get('commit')

    cfg_cmd_ = cmd['set_rpf_feasible']

    result = device.config(command_list=[cfg_cmd_]).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="config set failed: %s" % result, level="error")
        return False

    if commit:
        return device.commit().status()


def delete_rpf_feasible(device, **kwargs):

    '''
    This funtion used to deactivate or delete uRPF (unicast reverse path)
     feasible by using the command "deactivate/delete routing-options
     forwarding-table unicast-reverse-path feasible-paths"

    :param if:
        OPTIONAL Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param commit:
        REQUIRED Commit after configuration? Default is 0.
    :param deactivate:
        OPTIONAL DEACTIVATE for command.

    :return:
        TRUE when no error on commit. Not expect FALSE.

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    commit=${1}    deactivate=delete
        ${result} =    Delete Rpf Feasible    ${dev}    &{kwargs}

    '''
    valid_keys = ['commit', 'deactivate']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)
    function = function_name()
    logging.info(msg='Inside %s function' % function)
    commit = kwargs.get('commit')
    deactivate = kwargs.get('deactivate', 'delete')

    if deactivate == 'delete':
        cfg_cmd_ = cmd['del_rpf_feasible'] % deactivate
    else:
        cfg_cmd_ = cmd['deacti_rpf'] % deactivate

    result = device.config(command_list=[cfg_cmd_]).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="config set failed: %s" % result, level="error")
        return False
    if commit:
        return device.commit().status()


def set_rpf_check(device, **kwargs):
    '''
    This funtion used to apply uRPF (unicast reverse path) feasible
    to interfaces

    :param interface:
        REQUIRED Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param commit:
        REQUIRED Commit after configuration? Default is 0.
    :param activate:
        OPTIONAL ACTIVATE for command.
    :param family:
        OPTIONAL  faminy name for command like net|any|inet6|mpls.
        Default is 'inet'.
    :param loose_mode:
        OPTIONAL mode loose for command.
    :param fail_filter:
        REQUIRED FAIL_FILTER (fail-filter) for command.

    :return:
        TRUE when no error on commit. Not expect FALSE.

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    interface=ge-2/0/2
        ...    loose_mode=${1}    fail_filter=icmp_syslog    commit=${1}
        ${result} =    Set Rpf Check    ${dev}    &{kwargs}
    '''
    valid_keys = ['commit', 'interface', 'family', 'loose_mode', 'fail_filter']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)
    loose_mode = kwargs.get('loose_mode')
    family = kwargs.get('family', 'inet')
    fail_filter = kwargs.get('fail_filter')
    interface = kwargs.get('interface')
    commit = kwargs.get('commit')
    function = function_name()
    logging.info(msg="Inside %s %s" % (function, str(kwargs)))

    if not isinstance(interface, list):
        interface = [interface]

    for ifl in interface:
        (ifd, unit) = (ifl, 0)
        matched = re.search(r"^(\S+)\.(\d+)$", ifl)
        if matched:
            ifd = matched.group(1)
            unit = matched.group(2)

        cfg_cmd = "set interfaces %s unit %s family %s rpf-check" % (ifd,
                                                                     unit,
                                                                     family)
        if fail_filter:
            cfg_cmd += " fail-filter %s" % fail_filter
        if loose_mode:
            cfg_cmd += ' mode loose'

        result = device.config(command_list=[cfg_cmd]).response()
        if re.search(r'invalid|error', result, re.IGNORECASE):
            device.log(message="%s set fail_filter fail"
                       % str, level="error")
            return False

    if commit:
        return device.commit().status()


def delete_rpf_check(device, **kwargs):
    '''
    Remove Unicast Reverse-Path-Forwarding from interfaces

    :param commit:
        OPTIONAL commit and load configuration. Default is 0
    :param interface:
        REQUIRED interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param family:
        OPTION protocol family: inet, inet6, ...
    :param deactivate:
        OPTION deactivate configuration
    :param fail-filter:
        REQUIRED Name of filter applied to packets failing
        Reverse-Path-Forwarding check

    :return True/False:
        - True when commit successful: error = 0
        - False when commit fail: error # 0

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    interface=ge-2/0/2
        ...    fail_filter=icmp_syslog    commit=${1}
        ${result} =    Delete Rpf Check    device=${dev}    &{kwargs}
    '''
    valid_keys = ['commit', 'interface', 'family',
                  'deactivate', 'fail_filter']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)
    deactivate = kwargs.get('deactivate', 'delete')
    family = kwargs.get('family', 'inet')
    fail_filter = kwargs.get('fail_filter')
    interface = kwargs.get('interface')
    commit = kwargs.get('commit')
    function = function_name()
    logging.info(msg="Inside %s %s" % (function, str(kwargs)))

    if not isinstance(interface, list):
        interface = [interface]

    for ifl in interface:
        (ifd, unit) = (ifl, 0)
        matched = re.search(r"^(\S+)\.(\d+)$", ifl)
        if matched:
            ifd = matched.group(1)
            unit = matched.group(2)

        cfg_cmd = "%s interfaces %s unit %s family %s rpf-check" % (deactivate,
                                                                    ifd, unit,
                                                                    family)
        if fail_filter:
            cfg_cmd += " fail-filter"
            if deactivate == 'delete':
                cfg_cmd += " " + fail_filter

        result = device.config(command_list=[cfg_cmd]).response()
        if re.search(r'invalid|error', result, re.IGNORECASE):
            device.log(message="%s set fail_filter fail" % str,
                       level="error")
            return False

    if commit:
        return device.commit().status()


def delete_scu(device, **kwargs):
    '''
    Deactivate or delete Destination Class Usage from interfaces

    :param deactivate:
        OPTION deactivate configuration
    :param commit:
        OPTION commit and load configuration. Default is 0
    :param interface:
        REQUIRED interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param family:
        OPTION protocol family: inet, inet6, ...

    :return True/False:
        - True when no error or commit successful
        - False when error or commit fail

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    interface=ge-2/0/2
        ...    deactivate=deactivate    family=inet    commit=${1}
        ${result} =     Delete Scu    ${dev}    &{kwargs}
    '''
    valid_keys = ['commit', 'deactivate', 'interface', 'family']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)
    interface = kwargs.get('interface')
    family = kwargs.get('family', 'inet')
    commit = kwargs.get('commit')

    function = function_name()
    logging.info(msg="Inside %s" % function)

    if not interface:
        device.log(message='%s: argument \'interface\' has to be defined'
                   % function, level='error')
        return False
    if not isinstance(interface, list):
        interface = [interface]

    ver = ''
    res = device.cli(command='show version', format='text')
    response = res.response()
    matched = re.search(r"Junos:\s+(\d+\.\d+)\S+", response)
    if matched:
        ver = matched.group(1)

    _cmd = kwargs.get('deactivate', 'delete')
    for ifl in interface:
        unit = 0  # default value
        ifd = ifl
        check1 = re.search(r'^(\S+)\.(\d+)$', ifl)
        if check1:
            ifd = check1.group(1)
            unit = check1.group(2)

        if ver == "5.4":
            cfg_cmd = cmd['set_scu'] % (_cmd, ifd, unit, family)
            result = device.config(command_list=[cfg_cmd]).response()
            if re.search(r'invalid|error', result, re.IGNORECASE):
                device.log(message="%s scu fail" % _cmd, level="error")
                return False
        else:
            cfg_cmd = cmd['set_acc_scu'] % (_cmd, ifd, unit, family)
            result = device.config(command_list=[cfg_cmd]).response()
            if re.search(r'invalid|error', result, re.IGNORECASE):
                device.log(message="%s scu fail" % _cmd, level="error")
                return False

    if commit:
        return device.commit().status()


def delete_dcu(device, **kwargs):
    '''
    This funtion used to delete DCU (Destination class usage)
    from interfaces

    :param deactivate:
        REQUIRED DEACTIVATE for command.
    :param commit:
        OPTIONAL Commit after configuration? Default is 0.
    :param interface:
        REQUIRED Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param family:
        *OPTION* protocol family: inet, inet6, ...

    :return :
        TRUE if no error. Not expect FALSE.

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    interface=ge-2/0/2
        ...    deactivate=deactivate    family=inet    commit=${1}
        ${result} =     Delete Dcu    ${dev}    &{kwargs}
    '''
    valid_keys = ['commit', 'interface', 'family', 'deactivate']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)
    family = kwargs.get('family', 'inet')
    interface = kwargs.get('interface')
    deactivate = kwargs.get('deactivate', 'delete ')
    commit = kwargs.get('commit')
    function = function_name()
    logging.info(msg="Inside %s" % function)

    if not isinstance(interface, list):
        interface = [interface]

    for ifl in interface:
        unit = 0
        matched = re.search(r"^(\S+)\.(\d+)$", ifl)
        if matched:
            ifl = matched.group(1)
            unit = matched.group(2)

        ver = device.get_version()

        if ver == "5.4":
            cfg_cmd = ["%s interfaces %s unit %s family %s" %
                       (deactivate, ifl, unit, family) +
                       " destination-class-usage"]
            result = device.config(command_list=cfg_cmd).response()
            if re.search(r'invalid|error', result, re.IGNORECASE):
                device.log(message="%s set dcu pass" % cfg_cmd, level="error")
                return False
        else:
            cfg_cmd = ["%s interfaces %s unit %s family %s" %
                       (deactivate, ifl, unit, family) +
                       " accounting destination-class-usage"]

            result = device.config(command_list=cfg_cmd).response()
            if re.search(r'invalid|error', result, re.IGNORECASE):
                device.log(message="%s set dcu fail" % cfg_cmd, level="error")
                return False

    if commit:
        return device.commit().status()


def configure_protocol_scu(device, **kwargs):
    '''
    This funtion used to configure the protocol scu (source class usage)

    :param prot:
        REQUIRED PROT has to be define the protocol
    :param interface:
        OPTIONAL Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param commit:
        OPTIONAL Commit after configuration? Default is 0.
    :param name:
        OPTION name of policer name

    :return:
        TRUE if no error. Not expect FALSE.

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    prot=vpls    name=scu
        ...    commit=${1}
        ${result} =     Configure Protocol Scu    ${dev}    &{kwargs}

    '''
    valid_keys = ['commit', 'interface', 'name', 'prot']
    required_key = ['prot']
    kwargs = check_args(valid_keys, required_key, kwargs)

    prot = kwargs.get('prot')
    interface = kwargs.get('interface')
    name = kwargs.get('name', 'scu')
    commit = kwargs.get('commit')

    function = function_name()
    logging.info(msg="Inside %s" % function)

    cfg_cmd_1 = cmd['set_scu_from_prot'] % prot
    cfg_cmd_2 = cmd['set_scu_source_class'] % name
    cfg_cmd_3 = cmd['set_scu_forwarding_table'] % name
    cfg_list = [cfg_cmd_1, cfg_cmd_2, cfg_cmd_3]
    result = device.config(command_list=cfg_list).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="configure protocol scu failed", level="error")
        return False

    if interface:
        set_scu(device, interface=interface)

    if commit:
        return device.commit().status()


def set_scu(device, **kwargs):
    '''
    This funtion used to apply DCU (Destination class usage) to interfaces.

    :param activate:
        OPTIONAL ACTIVATE for command.
    :param interface:
        REQUIRED Interfaces such as "so.1", "so" or ['so.0', 'ge.1']
    :param commit:
        OPTIONAL Commit after configuration? Default is 0.
    :param family:
        OPTIONAL  faminy name for command like net|any|inet6|mpls.
        Default is 'inet'.

    :return:
        TRUE if no error. Not expect FALSE.

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    interface=xe-0/0/0.1    commit=${1}
        ${result} =    Set Scu    ${dev}    &{kwargs}

    '''
    valid_keys = ['commit', 'interface', 'family']
    required_key = ['interface']
    kwargs = check_args(valid_keys, required_key, kwargs)
    family = kwargs.get('family', 'inet')
    interface = kwargs.get('interface')
    commit = kwargs.get('commit')
    function = function_name()
    logging.info(msg="Inside %s" % function)

    if not isinstance(interface, list):
        interface = [interface]

    for ifl in interface:
        unit = 0
        matched = re.search(r"^(\S+)\.(\d+)$", ifl)
        if matched:
            ifl = matched.group(1)
            unit = matched.group(2)

        ver = device.get_version()

        if ver == "5.4":
            cfg_cmd = ["set interfaces %s unit %s family %s" %
                       (ifl, unit, family) +
                       " source-class-usage input output"]
            result = device.config(command_list=cfg_cmd).response()
            if re.search(r'invalid|error', result, re.IGNORECASE):
                device.log(message="%s set dcu fail" % cfg_cmd, level="error")
                return False
        else:
            cfg_cmd = ["set interfaces %s unit %s family %s" %
                       (ifl, unit, family) +
                       " accounting source-class-usage input output"]

            result = device.config(command_list=cfg_cmd).response()
            if re.search(r'invalid|error', result, re.IGNORECASE):
                device.log(message="%s set dcu fail" % cfg_cmd, level="error")
                return False

    if commit:
        return device.commit().status()


def configure_three_color_policer(device, **kwargs):
    '''
    This funtion used to configure three color policer

    :param policer_name:
        REQUIRED policer name
    :param rate_type:
        REQUIRED rate type. Eg:  single-rate, two-rate, three-color
    :param color_aware:
        OPTIONAL (0|1). Default 0. Enable color-aware option or not
    :param committed_information_rate:
        OPTIONAL committed-information-rate bps
    :param excess_burst_size:
        OPTIONAL excess-burst-size bytes value
    :param peak_information_rate:
        OPTIONAL peak-burst-size bytes value
    :param peak_burst_size:
        OPTIONAL peak-burst-size bytes
    :param action_discard:
        OPTIONAL (0|1). Default 0. enable loss-priority high then discard
    :param filter_specific:
        OPTIONAL (0|1). Default 0. enable filter_specific
    :param logical_interface_policer:
        OPTIONAL (0|1). Default 0. enable logical-interface-policer
    :param physical_interface_policer:
        OPTIONAL (0|1). Default 0. enable physical-interface-policer
    :param shared_bandwidth_policer:
        OPTIONAL (0|1). Default 0. enable shared-bandwidth-policer

    :return :
        TRUE if no error.
        FALSE if has error

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    policer_name=abc
        ...    rate_type=single-rate    committed_information_rate=100k
        ...    color_aware=${1}
        ...    committed_burst_size=100k    excess_burst_size=100k
        ...    action_discard=${1}    filter_specific=${1}
        ...    logical_interface_policer=${1}
        ...    physical_interface_policer=${1}
        ...    shared_bandwidth_policer=${1}
        ${result} =    Configure Three Color Policer    ${dev}  &{kwargs}
    '''
    function = function_name()
    device.log(message="Inside %s..." % function, level="info")

    #  Validating mandatory argument is provided
    valid_keys = ["policer_name", "rate_type", "color_aware",
                  "committed_information_rate", "committed_burst_size",
                  "excess_burst_size", "peak_information_rate",
                  "peak_burst_size", "action_discard", "filter_specific",
                  "logical_interface_policer", "physical_interface_policer",
                  "shared_bandwidth_policer"]
    required_key = ["policer_name", "rate_type"]
    kwargs = check_args(valid_keys, required_key, kwargs)

    #  Default values
    policer_name = kwargs.get("policer_name")
    rate_type = kwargs.get("rate_type")

    #  two-packet-rate
    color_aware = kwargs.get("color_aware", 0)
    committed_information_rate = kwargs.get("committed_information_rate", "")
    committed_burst_size = kwargs.get("committed_burst_size", "")
    excess_burst_size = kwargs.get("excess_burst_size", "")
    peak_information_rate = kwargs.get("peak_information_rate", "")
    peak_burst_size = kwargs.get("peak_burst_size", "")
    action_discard = kwargs.get("action_discard", 0)

    #  Knobs configuration
    filter_specific = kwargs.get("filter_specific", 0)
    logical_interface_policer = kwargs.get("logical_interface_policer", 0)
    physical_interface_policer = kwargs.get("physical_interface_policer", 0)
    shared_bandwidth_policer = kwargs.get("shared_bandwidth_policer", 0)

    #  Empty config string initially
    config_string = []
    if filter_specific:
        config_string.append("set firewall three-color-policer %s filter-"
                             "specific" % policer_name)
    if logical_interface_policer:
        config_string.append("set firewall three-color-policer %s logical-"
                             "interface-policer" % policer_name)
    if physical_interface_policer:
        config_string.append("set firewall three-color-policer %s physical-"
                             "interface-policer" % policer_name)
    if shared_bandwidth_policer:
        config_string.append("set firewall three-color-policer %s shared-"
                             "bandwidth-policer" % policer_name)

    #  Color-aware or color-blind mode
    if color_aware:
        config_string.append("set firewall three-color-policer %s %s color-"
                             "aware" % (policer_name, rate_type))
    else:  # if nothing specified, default is color-blind mode
        config_string.append("set firewall three-color-policer %s %s color-"
                             "blind" % (policer_name, rate_type))

    #  rate-type should be one of single-rate | single-packet-rate
    #  |two-rate | two-packet-rate
    if rate_type == "single-rate" or rate_type == "single-packet-rate":
        if committed_information_rate and committed_burst_size and\
                excess_burst_size:
            config_string.append("set firewall three-color-"
                                 "policer %s %s committed-information-"
                                 "rate %s" % (policer_name,
                                              rate_type,
                                              committed_information_rate)
                                 )
            config_string.append("set firewall three-color-"
                                 "policer %s %s committed-burst-"
                                 "size %s" % (policer_name,
                                              rate_type,
                                              committed_burst_size)
                                 )
            config_string.append("set firewall three-color-"
                                 "policer %s %s excess-burst-"
                                 "size %s" % (policer_name,
                                              rate_type,
                                              excess_burst_size)
                                 )
        else:
            device.log(message="With single-rate, you must specify "
                               "CIR, CBS and EBS!!!", level="error")
            return False
    elif rate_type == "two-rate" or rate_type == "two-packet-rate":
        if committed_information_rate and committed_burst_size and\
                peak_information_rate and peak_burst_size:
            config_string.append("set firewall three-color-"
                                 "policer %s %s committed-information-"
                                 "rate %s" % (policer_name,
                                              rate_type,
                                              committed_information_rate)
                                 )
            config_string.append("set firewall three-color-"
                                 "policer %s %s committed-burst-"
                                 "size %s" % (policer_name,
                                              rate_type,
                                              committed_burst_size)
                                 )
            config_string.append("set firewall three-color-"
                                 "policer %s %s peak-information-"
                                 "rate %s" % (policer_name,
                                              rate_type,
                                              peak_information_rate)
                                 )
            config_string.append("set firewall three-color-"
                                 "policer %s %s peak-burst-"
                                 "size %s" % (policer_name,
                                              rate_type,
                                              peak_burst_size)
                                 )
        else:
            device.log(message="With two-rate, you must specify "
                       "CIR, CBS, PIR and PBS!!!", level="error")
            return False
    else:
        device.log(message="Invalid rate_type %s specified" % rate_type,
                   level="error")
        return False

    #  Action in three-color-policer is optional; if true, then set
    #  high loss-priority packets to be discarded
    if action_discard:
        config_string.append("set firewall three-color-policer %s action "
                             "loss-priority high then discard" % policer_name)

    device.config(command_list=config_string)

    try:
        device.commit()
        device.log(message="Config Committed successfully", level="info")
        return True
    except Exception:
        device.log(message="Unable to commit config", level="warn")
        return False


def configure_hierarchical_policer(device, **kwargs):
    '''
    This funtion used to configure three color policer

    :param policer_name:
        REQUIRED policer name
    :param aggr_then_actions:
        REQUIRED Then action Split the then_actions with comma
    :param aggr_limit_type:
        OPTIONAL limit-type. Eg: if-exceeding, if-exceeding-pps
    :param aggr_burst_size_limit:
        OPTIONAL burst-size-limit value
    :param aggr_bandwidth_limit:
        OPTIONAL bandwidth-limit value
    :param aggr_packet_burst:
        OPTIONAL packet burst value
    :param aggr_pps_limit:
        OPTIONAL pps limit value
    :param premium_limit_type:
        OPTIONAL premium-limit-type value. Eg: if-exceeding, if-exceeding-pps
    :param premium_burst_size_limit:
        OPTIONAL premium-burst-size-limit value
    :param premium_bandwidth_limit:
        OPTIONAL premium-bandwidth-limit value
    :param premium_packet_burst:
        OPTIONAL premium-packet-burst value
    :param premium_pps_limit:
        OPTIONAL premium_pps_limit value
    :param filter_specific:
        OPTIONAL (0|1). Default 0. enable filter-specific
    :param logical_interface_policer:
        OPTIONAL (0|1). Default 0. enable logical-interface-policer
    :param physical_interface_policer:
        OPTIONAL (0|1). Default 0. enable physical-interface-policer
    :param shared_bandwidth_policer:
        OPTIONAL (0|1). Default 0. enable shared-bandwidth-policer

    :return :
        TRUE if no error.
        FALSE if has error

    Robot Usage Example  :
         ${dev} =    Get Handle   resource=device0
         &{kwargs} =    Create Dictionary    policer_name=hierarchical_policer
         ...    aggr_limit_type=if-exceeding
         ...    aggr_burst_size_limit=${1500}
         ...    aggr_bandwidth_limit=70m
         ...    aggr_then_actions=discard,forwarding-class af,loss-priority low
         ...    premium_limit_type=if-exceeding
         ...    premium_burst_size_limit=${1500}
         ...    premium_bandwidth_limit=50m
         ...    filter_specific=${1}
         ...    logical_interface_policer=${1}
         ...    shared_bandwidth_policer=${1}
         ${result} =    Configure Hierarchical Policer    ${dev}  &{kwargs}
    '''
    sub = function_name()
    device.log(message="Inside %s..." % sub, level='debug')

    # Validating mandatory argument is provided
    valid_key = ['policer_name', 'aggr_then_actions', 'aggr_limit_type',
                 'aggr_burst_size_limit', 'aggr_bandwidth_limit',
                 'aggr_packet_burst', 'aggr_pps_limit', 'premium_limit_type',
                 'premium_burst_size_limit', 'premium_bandwidth_limit',
                 'premium_packet_burst', 'premium_pps_limit',
                 'filter_specific', 'logical_interface_policer',
                 'physical_interface_policer', 'shared_bandwidth_policer']
    required_key = ['policer_name', 'aggr_then_actions']
    check_args(valid_key, required_key, kwargs)

    # Default values
    policer_name = kwargs['policer_name']
    aggr_limit_type = kwargs.get('aggr_limit_type', 'if-exceeding')
    aggr_burst_size_limit = kwargs.get('aggr_burst_size_limit', None)
    aggr_bandwidth_limit = kwargs.get('aggr_bandwidth_limit', None)
    aggr_packet_burst = kwargs.get('aggr_packet_burst', None)
    aggr_pps_limit = kwargs.get('aggr_pps_limit', None)
    aggr_then_actions = kwargs.get('aggr_then_actions', None)
    premium_limit_type = kwargs.get('premium_limit_type', 'if-exceeding')
    premium_burst_size_limit = kwargs.get('premium_burst_size_limit', None)
    premium_bandwidth_limit = kwargs.get('premium_bandwidth_limit', None)
    premium_packet_burst = kwargs.get('premium_packet_burst', None)
    premium_pps_limit = kwargs.get('premium_pps_limit', None)

    # Some of the knobs
    filter_specific = kwargs.get('filter_specific', None)
    logical_interface_policer = kwargs.get('logical_interface_policer', None)
    physical_interface_policer = kwargs.get('physical_interface_policer', None)
    shared_bandwidth_policer = kwargs.get('shared_bandwidth_policer', None)

    # Split the then_actions with comma
    actions = aggr_then_actions.split(',')

    # Empty configure string initially
    config_str = []

    if filter_specific:
        config_str.append(
            "set firewall hierarchical-policer %s filter-specific"
            % policer_name)

    if logical_interface_policer:
        config_str.append(
            "set firewall hierarchical-policer %s logical-interface-policer"
            % policer_name)

    if physical_interface_policer:
        config_str.append(
            "set firewall hierarchical-policer %s physical-interface-policer"
            % policer_name)

    if shared_bandwidth_policer:
        config_str.append(
            "set firewall hierarchical-policer %s shared-bandwidth-policer"
            % policer_name)

    # Configure the "aggregate" stanza ...
    # limit-type should be either "if-exceeding" or "if-exceeding-pps"
    if aggr_limit_type == "if-exceeding":
        if aggr_burst_size_limit and aggr_bandwidth_limit:
            config_str.append(
                "set firewall hierarchical-policer %s aggregate %s "
                "burst-size-limit %s"
                % (policer_name, aggr_limit_type, aggr_burst_size_limit))
            config_str.append(
                "set firewall hierarchical-policer %s aggregate %s "
                "bandwidth-limit %s"
                % (policer_name, aggr_limit_type, aggr_bandwidth_limit))
        else:
            device.log(
                level='ERROR',
                message="With if-exceeding, you must specify burst-size-limit "
                "and bandwidth-limit!!!")
            return False
    elif aggr_limit_type == "if-exceeding-pps":
        if aggr_packet_burst and aggr_pps_limit:
            config_str.append(
                "set firewall hierarchical-policer %s aggregate %s "
                "packet-burst %s"
                % (policer_name, aggr_limit_type, aggr_packet_burst))
            config_str.append(
                "set firewall hierarchical-policer %s aggregate %s "
                "pps-limit %s"
                % (policer_name, aggr_limit_type, aggr_pps_limit))
        else:
            device.log(
                level='ERROR',
                message="With if-exceeding-pps, you must specify packet-burst "
                "and pps-limit!!!")
            return False
    else:
        device.log(
            level='ERROR',
            message="Invalid limit_type %s under aggregate "
            "specified - it should be either if-exceeding or if-exceeding-pps"
            % aggr_limit_type)
        return False

    # Processing for the then actions specified under aggregate
    for val in actions:
        config_str.append(
            "set firewall hierarchical-policer %s aggregate then %s"
            % (policer_name, val))

    # Configure the "premium" stanza ...
    # limit-type should be either "if-exceeding" or "if-exceeding-pps"
    if premium_limit_type == "if-exceeding":
        if premium_burst_size_limit and premium_bandwidth_limit:
            config_str.append(
                "set firewall hierarchical-policer %s premium %s "
                "burst-size-limit %s"
                % (policer_name, premium_limit_type, premium_burst_size_limit))
            config_str.append(
                "set firewall hierarchical-policer %s premium %s "
                "bandwidth-limit %s"
                % (policer_name, premium_limit_type, premium_bandwidth_limit))
            # Always then action is to discard under premium
            config_str.append(
                "set firewall hierarchical-policer %s premium then discard"
                % policer_name)
        else:
            device.log(
                level='ERROR',
                message="With if-exceeding, you must specify burst-size-limit "
                "and bandwidth-limit!!!")
            return False

    elif premium_limit_type == "if-exceeding-pps":
        if premium_packet_burst and premium_pps_limit:
            config_str.append(
                "set firewall hierarchical-policer %s premium %s "
                "packet-burst %s"
                % (policer_name, premium_limit_type, premium_packet_burst))
            config_str.append(
                "set firewall hierarchical-policer %s premium %s pps-limit %s"
                % (policer_name, premium_limit_type, premium_pps_limit))
            # Always then action is to discard under premium
            config_str.append(
                "set firewall hierarchical-policer %s premium then discard"
                % policer_name)
        else:
            device.log(
                level='ERROR',
                message="With if-exceeding-pps, you must specify packet-burst "
                "and pps-limit!!!")
            return False
    else:
        device.log(
            level='ERROR',
            message="Invalid limit_type %s under premium specified - "
            "it should be either if-exceeding or if-exceeding-pps"
            % premium_limit_type)
        return False

    # Execute all command
    device.config(command_list=config_str)

    try:
        device.commit()
        device.log(message="Config Committed successfully", level="info")
        return True
    except Exception:
        device.log(message="Unable to commit config", level="warn")
        return False


def configure_tunnel_end_point(device, **kwargs):
    '''
     Define a tunnel template

    :param tunnel_name:
        **REQUIRED** Name that identifies the tunnel template using a
        non-reserved string of not more than 64 characters.
    :param transport_protocol:
        **OPTION** The IP network protocol used to transport encapsulated
        passenger protocol packets. Eg: ipv4, ipv6, mpls.
    :param encapsulation_protocol:
        **OPTION** Encapsulation protocol. Eg: gre, l2tp
    :param destination_address:
        **OPTIONAL** IP address or address range of the de-encapsulator
        (the remote egress PE router)
    :param source_address:
        **OPTIONAL** IP address or address range of the encapsulator
        (the local ingress PE router).
    :param logical_system:
        OPTIONAL name of logical-system for tunnel-end-point configure

    :return:
        TRUE if no error.
        FALSE if has an error.

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    tunnel_name=sample_tunnel
        ...    transport_protocol=ipv4    encapsulation_protocol=gre
        ...    destination_address=1.1.1.1    source_address=2.2.2.2
        ...    commit=True
        ${result} =    Configure Tunnel End Point    ${dev}  &{kwargs}

    '''
    valid_keys = ['logical_system', 'encapsulation_protocol', 'source_address',
                  'destination_address', 'transport_protocol', 'tunnel_name',
                  'commit']
    required_key = ['tunnel_name']
    kwargs = check_args(valid_keys, required_key, kwargs)
    logical_system = kwargs.get('logical_system')
    source_address = kwargs.get('source_address')
    destination_address = kwargs.get('destination_address')
    transport_protocol = kwargs.get('transport_protocol')
    encapsulation_protocol = kwargs.get('encapsulation_protocol')
    tunnel_name = kwargs.get('tunnel_name')
    commit = kwargs.get('commit')

    function = function_name()
    logging.info(msg="Inside %s" % function)
    config_cmds = []

    if logical_system is not None:
        cmd = "set logical-systems %s firewall" % logical_system
    else:
        cmd = "set firewall"

    cmd = "%s tunnel-end-point %s" % (cmd, tunnel_name)
    if encapsulation_protocol is not None:
        config_cmds.append("%s %s" % (cmd, encapsulation_protocol))
    if transport_protocol is not None:
        if source_address is None and destination_address is None:
            device.log(message="No value specified for source_address or "
                       "destination_address", level="error")
            return False
        if source_address is not None:
            config_cmds.append("%s %s source-address %s" % (
                cmd, transport_protocol, source_address))

        if destination_address is not None:
            config_cmds.append("%s %s destination-address %s" % (
                cmd, transport_protocol, destination_address))

    result = device.config(command_list=config_cmds).response()
    if re.search(r'invalid|error', result, re.IGNORECASE):
        device.log(message="Config set failed on device: %s"
                   % result, level='error')
        return False

    if commit:
        return device.commit().status()
    device.log(message="configure tunnel end point passed", level="info")
    return True


def get_pfe_firewall_syslog(device, **kwargs):
    '''
    Get information from the log messages in the specified log file by
    command:
        - show log filename/ show log messages

    :param file:
        OPTION name of syslog file
    :param interface:
        OPTION name of interface
    :param action:
        OPTION Action name (i.e. A, R, D)
    :param inner_vlan:
        OPTION inner vlan
    :param outer_vlan:
        OPTION outer vlan
    :param src_mac:
        OPTION source mac address
    :param dst_mac:
        OPTION destination mac address
    :param src_ip
        OPTION source ip address
    :param dst_ip
        OPTION destination ip address
    :param ip_protocol
        OPTION ip protocol
    :param from:
        OPTION from timer..
    :param to:
        OPTION to timer..
    :param count:
        OPTION number of line syslog need to get. Default: get
        all line of syslog

    :return fw_syslog:
       List of logs match with conditions

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    file=Firewall    from=11:30:00
        ...    to=11:35:00    inner_vlan=2    src_mac=00:00:00:00:00:06
        ...    dst_mac=40:b4:f0:e2:b9:9c    src_ip=20:1:1:1:1:1:1:2
        ...    dst_ip=21:1:1:1:1:1:1:2
        ${result} =    Get Pfe Firewall Syslog    device=${dev}    &{kwargs}
    '''
    valid_keys = ['file', 'interface', 'inner_vlan', 'outer_vlan', 'src_mac',
                  'dst_mac', 'src_ip', 'dst_ip', 'ip_protocol', 'from', 'to',
                  'count', 'action']
    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    _file = kwargs.get('file', 'messages')
    interface = kwargs.get('interface')
    action = kwargs.get('action')
    inner_vlan = kwargs.get('inner_vlan')
    outer_vlan = kwargs.get('outer_vlan')
    src_mac = kwargs.get('src_mac')
    dst_mac = kwargs.get('dst_mac')

    src_ip = kwargs.get('src_ip')
    dst_ip = kwargs.get('dst_ip')
    ip_protocol = kwargs.get('ip_protocol')

    _from = kwargs.get('from')
    _to = kwargs.get('to')
    count = kwargs.get('count')
    fw_syslog = []

    function = function_name()
    logging.info(msg="Inside %s" % function)

    cli_cmd = "show log " + _file

    try:
        response = device.cli(command=cli_cmd, format='text').response()
    except Exception:
        device.log(message="get the response from show log "
                   "failed on device", level='error')
        return False
    lines = response.split('\n')
    lines = [x for x in lines if "FW:" in x]

    for line in lines:
        syslog = {}
        check_interface = False
        check_action = False
        check_outer_vlan = False
        check_inner_vlan = False
        check_ip_protocol = False
        check_mac = False
        check_ip = False
        match_time = re.search(r'(\w+\s+\d+)\s+(\d+\:\d+\:\d+)\s+(\S+)\s+\w',
                               line, re.I)
        if match_time:
            syslog['date'] = match_time.group(1)
            syslog['time'] = match_time.group(2)
            syslog['hostname'] = match_time.group(3)
        match_interface = re.search(r'(\w+\-\d+\/\d+\/\d+\.\d+)', line, re.I)
        if match_interface:
            syslog['interface'] = match_interface.group(1)
            check_interface = True
        match_action = re.search(r'\s+(A|D|R)\s+', line)
        if match_action:
            syslog['action'] = match_action.group(1)
            check_action = True
        match_vlan1 = re.search(r'\s+[A|D|R]\s+(\w+)\:(\w+)\:(\w+)\s+', line)
        match_vlan2 = re.search(r'\s+[A|D|R]\s+(\w+)\:(\w+)\s+', line)

        if match_vlan1:
            out_vlan_hex = match_vlan1.group(1)
            out_vlan = int(out_vlan_hex, 16)
            syslog['outer_vlan'] = str(out_vlan)
            in_vlan_hex = match_vlan1.group(2)
            in_vlan = int(in_vlan_hex, 16)
            syslog['inner_vlan'] = str(in_vlan)
            syslog['ether_type'] = match_vlan1.group(3)
            check_outer_vlan = True
            check_inner_vlan = True
        if match_vlan2:
            in_vlan_hex = match_vlan2.group(1)
            in_vlan = int(in_vlan_hex, 16)
            syslog['inner_vlan'] = str(in_vlan)
            syslog['ether_type'] = match_vlan2.group(2)
            check_inner_vlan = True
        match_mac = re.search(r'(\S+)\s+\-\>\s+(\S+)\s+', line)
        if match_mac:
            syslog['src_mac'] = match_mac.group(1)
            syslog['dst_mac'] = match_mac.group(2)
            check_mac = True
        match_protocol = re.search(r'\S+\s+\-\>\s+\S+\s+(\d+)', line)
        if match_protocol:
            syslog['ip_protocol'] = match_protocol.group(1)
            check_ip_protocol = True
        match_ip1 = re.search(r'\s+SA\s+(\S+)\s+\-\>\s+DA\s+(\S+)\s+\(', line)
        match_ip2 = re.search(
            r'\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', line)
        if match_ip1:
            syslog['src_ip'] = match_ip1.group(1)
            syslog['dst_ip'] = match_ip1.group(2)
            check_ip = True
        elif match_ip2:
            syslog['src_ip'] = match_ip2.group(1)
            syslog['dst_ip'] = match_ip2.group(2)
            check_ip = True
        match = 1
        if check_interface:
            if interface and syslog['interface'] != interface:
                match = 0
        if check_action:
            if action and syslog['action'] != action:
                match = 0
        if check_inner_vlan:
            if inner_vlan and syslog['inner_vlan'] != inner_vlan:
                match = 0
        if check_outer_vlan:
            if outer_vlan and syslog['outer_vlan'] != outer_vlan:
                match = 0
        if check_mac:
            if src_mac and syslog['src_mac'] != src_mac:
                match = 0
            if dst_mac and syslog['dst_mac'] != dst_mac:
                match = 0
        if check_ip_protocol:
            if ip_protocol and syslog['ip_protocol'] != ip_protocol:
                match = 0
        if check_ip:
            if src_ip and syslog['src_ip'] != src_ip:
                match = 0
            if dst_ip and syslog['dst_ip'] != dst_ip:
                match = 0
        if match_time:
            if _from and __timeless(syslog['time'], _from):
                match = 0
            if _to and __timeless(_to, syslog['time']):
                match = 0

        if match:
            if syslog:
                fw_syslog.append(syslog)
            if count:
                if count == len(fw_syslog):
                    break

    return fw_syslog


def check_pfe_firewall_syslog(device, **kwargs):
    '''
    Check firewall syslog entry found or not

    :param file:
        OPTION name of syslog file
    :param interface:
        OPTION name of interface
    :param action:
        OPTION Action name (i.e. A, R, D)
    :param inner_vlan:
        OPTION inner vlan
    :param outer_vlan:
        OPTION outer vlan
    :param src_mac:
        OPTION source mac address
    :param dst_mac:
        OPTION destination mac address
    :param src_ip
        OPTION source ip address
    :param dst_ip
        OPTION destination ip address
    :param ip_protocol
        OPTION ip protocol
    :param action_name:
        OPTION Action name (i.e. A, R, D)
    :param from:
        OPTION Start time (hh:mm:ss)
    :param to:
        OPTION End time (hh:mm:ss)

    :param chk_count:
        OPTION Check count (default is 1)
    :param chk_interval:
        OPTION Wait time before next retry (default 10 seconds)

    :return:
        True: syslog entry is found
        False: syslog entry is not found

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        &{kwargs} =    Create Dictionary    file=Firewall    from=11:30:00
        ...    to=11:35:00    inner_vlan=2    src_mac=00:00:00:00:00:06
        ...    dst_mac=40:b4:f0:e2:b9:9c    src_ip=20:1:1:1:1:1:1:2
        ...    dst_ip=21:1:1:1:1:1:1:2    chk_count=${2}    chk_interval=${1}
        ${result} =    Check Pfe Firewall Syslog    device=${dev}    &{kwargs}
    '''
    valid_keys = ['file', 'interface', 'inner_vlan', 'outer_vlan', 'src_mac',
                  'dst_mac', 'src_ip', 'dst_ip', 'ip_protocol', 'from', 'to',
                  'action', 'chk_count', 'chk_interval']

    required_key = []
    kwargs = check_args(valid_keys, required_key, kwargs)

    _file = kwargs.get('file', 'messages')
    interface = kwargs.get('interface')
    action = kwargs.get('action')
    inner_vlan = kwargs.get('inner_vlan')
    outer_vlan = kwargs.get('outer_vlan')
    src_mac = kwargs.get('src_mac')
    dst_mac = kwargs.get('dst_mac')

    src_ip = kwargs.get('src_ip')
    dst_ip = kwargs.get('dst_ip')
    ip_protocol = kwargs.get('ip_protocol')

    _from = kwargs.get('from')
    _to = kwargs.get('to')

    chk_count = kwargs.get('chk_count', 1)
    chk_interval = kwargs.get('chk_interval', 10)

    fw_syslog = {}
    function = function_name()
    # Call put_log from JT
    logging.info(msg="Inside %s function" % function)

    for i in range(0, chk_count):
        if i > 0:
            time.sleep(chk_interval)
        param = {'file': _file, 'interface': interface,
                 'inner_vlan': inner_vlan,
                 'outer_vlan': outer_vlan,
                 'src_mac': src_mac, 'dst_mac': dst_mac,
                 'src_ip': src_ip, 'dst_ip': dst_ip,
                 'ip_protocol': ip_protocol, 'from': _from, 'to': _to,
                 'action': action, 'count': 1}
        fw_syslog = get_pfe_firewall_syslog(device, **param)

        if fw_syslog:
            device.log(message="%s syslog entry found" % function,
                       level='info')
            return True

    device.log(message="%s syslog entry not found" % function,
               level='warn')
    return False
