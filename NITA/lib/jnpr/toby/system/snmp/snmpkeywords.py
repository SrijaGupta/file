"""
Python file containing functions specific to SNMP
"""
import os
import time
import re
#from random import random
#from time import sleep

def snmp_get(dev, system_node='current', controller='current', prettyprint=True,
             *args, **kwargs):
    '''
    Perform SNMP GET operation.
    This function performs similar to the following Net-SNMP command:
    $snmpget -v1 -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0

    Eg: snmp_get(dev0, oid="SNMPv2-MIB::sysDescr.0")
    :param dev:
        **REQUIRED** Router object to which SNMP getnext is called
    :param system_node
        **OPTIONAL** Node on which to run the command. Default to current_node
    :param controller
        **OPTIONAL** Controller on which to run the command.
        Default to current_controller
    :param snmp_channel_id:
        **OPTIONAL** Channel ID of SNMP object to be called.
        channel ID of first SNMP object created on the device will be selected
        if not specified.
    :param oid
        **REQUIRED**  a string which has one oid.
        Eg: SNMPv2-MIB::sysUpTime
    :param index
        **OPTIONAL** OID index. (No default value)
    :param community
        **OPTIONAL** snmp community string default is 'public'

     ----- SNMP V3 options: ---------------
     In most of the cases, it is the same as SNMP v3 options
     default values are defined in snmp init()

    :return data structure (dict)
    Eg: {'SNMPv2-MIB::sysUpTime.0': '211096159'}

    Eg:
        param = {'oid': "SNMPv2-MIB::sysUpTime", 'index': '0'}
        result = snmp_get(dev0, **param)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Snmp Get    device=${dev}
        ...    oid=SNMPv2-MIB::sysUpTime    index=0
    '''
    current_controller = _get_controller(dev, system_node, controller)
    channelid = kwargs.get('snmp_channel_id', None)
    snmp_channel = _get_snmp_channel(current_controller, channelid)

    oid = kwargs['oid']
    index = kwargs.get('index')
    if index:
        oid = oid + '.' + str(index)
    return_list = {}
    current_controller.log("Executing SNMP GET on %s" %
                           current_controller.host)
    comm_data = snmp_channel.create_community_data(**kwargs)
    obj_data = snmp_channel.create_object_identity(oid=oid)
    contextdata = snmp_channel.invoke(current_controller, 'ContextData',
                                      snmp_channel.context_engine,
                                      snmp_channel.context_name)
    snmpgetcmd = snmp_channel.invoke(current_controller, 'getCmd',
                                     snmp_channel.snmpchannel,
                                     comm_data, snmp_channel.transport,
                                     contextdata, obj_data)
    error_indication, error_status, error_index, var_binds = next(snmpgetcmd)
    # Check for errors and print out results
    if error_indication:
        current_controller.log(error_indication)
        return False
    elif error_status:
        current_controller.log(level='error', message='%s at %s' % (
            error_status.prettyPrint(), error_index and
            var_binds[int(error_index) - 1][0] or '?'))
        return False
    else:
        for name, val in var_binds:
            if not re.search(r'No Such Instance', val.prettyPrint(), re.I):
                if prettyprint is True:
                    return_list[name.prettyPrint()] = val.prettyPrint()
                else:
                    return_list[name.prettyPrint()] = val._value
            else:
                current_controller.log(
                    level='error', message='No Such Instance currently '
                    'exists at this OID')
                return False
    return return_list


def snmp_set(dev, system_node='current', controller='current', *args,
             **kwargs):
    '''
    This method to excecute snmpset command. used to actually modify
    information on the remote host. For each variable you want to set,
    you need to specify the OID to update, the data type and the value
    you want to set it to

    snmpset  <router> <community> <oid> <type> <val>

    :param dev:
        **REQUIRED** Router object to which SNMP getnext is called
    :param system_node
        **OPTIONAL** Node on which to run the command. Default to current_node
    :param controller
        **OPTIONAL** Controller on which to run the command.
        Default to current_controller
    :param snmp_channel_id:
        **OPTIONAL** Channel ID of SNMP object to be called.
        channel ID of first SNMP object created on the device will be selected
        if not specified.

    :param oid
        **REQUIRED** A string which has one oid.
    :param index
        **OPTIONAL** a string which has information of index
    :param value
        **REQUIRED** A value to be set must accompany each object
        identifier

     ----- SNMP V3 options: ---------------
     In most of the cases, it is the same as SNMP v3 options
     default values are defined in snmp_init();

    :return
        TRUE if SNMP set performed successful
        FALSE if SNMP set performed unsuccessful
    Eg:
        param = {'oid': "SNMPv2-MIB::sysContact", 'index': '0',
                 'value': 'test', 'community': 'private'}
        result = snmp_set(dev0, **param)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Snmp Set    device=${dev}
        ...    oid=SNMPv2-MIB::sysContact    index=0
        ...    value=test    community=private
    '''
    current_controller = _get_controller(dev, system_node, controller)
    channelid = kwargs.get('snmp_channel_id', None)
    snmp_channel = _get_snmp_channel(current_controller, channelid)

    oid = kwargs['oid']
    index = kwargs.get('index')
    if index:
        oid = oid + '.' + str(index)
    value = kwargs.get('value')

    current_controller.log("Executing SNMP SET on %s" %
                           current_controller.host)
    comm_data = snmp_channel.create_community_data(**kwargs)
    obj_data = snmp_channel.create_object_identity(oid=oid, value=value)
    contextdata = snmp_channel.invoke(current_controller, 'ContextData',
                                      snmp_channel.context_engine,
                                      snmp_channel.context_name)
    snmpsetcmd = snmp_channel.invoke(current_controller, 'setCmd',
                                     snmp_channel.snmpchannel,
                                     comm_data, snmp_channel.transport,
                                     contextdata, obj_data)
    error_indication, error_status, error_index, var_binds = next(snmpsetcmd)
    result = False
    # Check for errors and print out results
    if error_indication:
        current_controller.log(error_indication)
        return False
    elif error_status:
        current_controller.log(level='error', message='%s at %s' % (
            error_status.prettyPrint(), error_index and
            var_binds[int(error_index) - 1][0] or '?'))
        return False
    else:
        for name, val in var_binds:
            if not re.search(r'No Such Instance', val.prettyPrint(), re.I):
                current_controller.log(
                    message='SNMP set performed successful '
                    '%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                result = True
                break
            else:
                current_controller.log(
                    level='error', message='No Such Instance currently '
                    'exists at this OID')
    return result


def snmp_getnext(dev, system_node='current', controller='current', prettyprint=True, *args,
                 **kwargs):
    """
    Function to retrieve the next OID in table.
    Calls snmp_getnext method of SNMP class.
    :param dev:
        Router object to which SNMP getnext is called
    :param system_node
        Node on which to run the command. Default to current_node
    :param controller
        Controller on which to run the command. Default to current_controller
    :param snmp_channel_id:
        Channel ID of SNMP object to be called.
        channel ID of first SNMP object created on the device will be selected
        if not specified.
    :param oid
        **REQUIRED** A string which has one oid.
    :param index
        **OPTIONAL** a string which has information of index
    :param version:
        SNMP version 1 for SNMPv1, 2 for SNMPv2 and 3 for SNMPv3
    :param community
        **OPTIONAL** snmp community string default is 'public'
    ----- SNMP V3 options: ---------------
     In most of the cases, it is the same as SNMP v3 options
     default values are defined in snmp init()

    :return data structure (dict)
        data structure of returned value to a dict reference
        snmp_getnext()
    Eg:
        param = {'oid': "SNMPv2-MIB::sysUpTime", 'index': '0'}
        result = snmp_getnext(dev0, **param)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Snmp Get Next    device=${dev}
        ...    oid=SNMPv2-MIB::sysUpTime    index=0
    """

    current_controller = _get_controller(dev, system_node, controller)
    channelid = kwargs.get('snmp_channel_id', None)
    snmp_channel = _get_snmp_channel(current_controller, channelid)

    oid = kwargs['oid']
    index = kwargs.get('index')
    if index:
        oid = oid + '.' + str(index)

    current_controller.log("Executing SNMP GETNEXT on %s" %
                           current_controller.host)
    comm_data = snmp_channel.create_community_data(**kwargs)
    obj_data = snmp_channel.create_object_identity(oid=oid)
    contextdata = snmp_channel.invoke(current_controller, 'ContextData',
                                      snmp_channel.context_engine,
                                      snmp_channel.context_name)
    snmpgetcmd = snmp_channel.invoke(current_controller, 'nextCmd',
                                     snmp_channel.snmpchannel,
                                     comm_data, snmp_channel.transport,
                                     contextdata, obj_data)

    return_list = {}
    # Check for errors and print out results
    error_indication, error_status, error_index, var_binds = next(snmpgetcmd)
    if error_indication:
        current_controller.log(error_indication)
        return False
    elif error_status:
        current_controller.log(level='error', message='%s at %s' % (
            error_status.prettyPrint(), error_index and
            var_binds[int(error_index) - 1][0] or '?'))
        return False
    else:
        for name, val in var_binds:
            if not re.search(r'No Such Instance', val.prettyPrint(), re.I):
                if prettyprint is True:
                    return_list[name.prettyPrint()] = val.prettyPrint()
                else:
                    return_list[name.prettyPrint()] = val._value
            else:
                current_controller.log(level='error',
                                       message='No Such Instance currently '
                                       'exists at this OID')
                return False
    return return_list


def snmp_walk(dev, system_node='current', controller='current', prettyprint=True, *args,
              **kwargs):
    """
    Function to Send a SNMP walk requests to device
    Calls snmp_walk method of SNMP class.
    :param dev:
        Router object to which SNMP getnext is called
    :param system_node
        Node on which to run the command. Default to current_node
    :param controller
        Controller on which to run the command. Default to current_controller
    :param snmp_channel_id:
        Channel ID of SNMP object to be called.
        channel ID of first SNMP object created on the device will be selected
        if not specified.
    :param version:
        SNMP version 1 for SNMPv1, 2 for SNMPv2 and 3 for SNMPv3
    :param community
        **OPTIONAL** snmp community string default is 'public'
    ----- SNMP V3 options: ---------------
     In most of the cases, it is the same as SNMP v3 options
     default values are defined in snmp init()

    :return data structure (dict)
         data structure of returned value to a dict reference
         snmp_walk()
    Eg:
        param = {'oid': "IF-MIB::ifInOctets"}
        result = snmp_walk(dev0, **param)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Snmp Walk    device=${dev}
        ...    oid=IF-MIB::ifInOctets
    """

    current_controller = _get_controller(dev, system_node, controller)
    channelid = kwargs.get('snmp_channel_id', None)
    snmp_channel = _get_snmp_channel(current_controller, channelid)

    oid = kwargs['oid']
    current_controller.log("Executing SNMP WALK on %s" %
                           current_controller.host)
    comm_data = snmp_channel.create_community_data(**kwargs)
    obj_data = snmp_channel.create_object_identity(oid=oid)
    contextdata = snmp_channel.invoke(current_controller, 'ContextData',
                                      snmp_channel.context_engine,
                                      snmp_channel.context_name)
    next_cmd = snmp_channel.invoke(current_controller, 'nextCmd',
                                   snmp_channel.snmpchannel,
                                   comm_data, snmp_channel.transport,
                                   contextdata, obj_data, lexicographicMode=False,
                                   ignoreNonIncreasingOid=False)
    return_list = {}

    for (error_indication, error_status, error_index, var_binds) in next_cmd:
        if error_indication:
            current_controller.log(error_indication)
            return False
        elif error_status:
            current_controller.log(level='error', message='%s at %s' % (
                error_status.prettyPrint(), error_index and
                var_binds[int(error_index) - 1][0] or '?'))
            return False
        else:
            for name, val in var_binds:
                if not re.search(r'No Such Instance', val.prettyPrint(), re.I):
                    if prettyprint is True:
                        return_list[name.prettyPrint()] = val.prettyPrint()
                    else:
                        return_list[name.prettyPrint()] = val._value
                else:
                    current_controller.log(
                        level='error', message='No Such Instance currently '
                        'exists at this OID')
                    return False
    return return_list


def snmp_bulkget(dev, system_node='current', controller='current', prettyprint=True, *args,
                 **kwargs):
    """
    This method communicates with a network entity using SNMP BULK Requests
    Calls snmp_bulkget method of SNMP class.
    :param dev:
        Router object to which SNMP bulkget is called
    :param system_node
        Node on which to run the command. Default to current_node
    :param controller
        Controller on which to run the command. Default to current_controller
    :param snmp_channel_id:
        Channel ID of SNMP object to be called.
        channel ID of first SNMP object created on the device will be selected
        if not specified.
    :param non_repeaters (int):
         One MIB variable is requested in response for the first nonRepeaters
         MIB variables in request. Default: 0
    :param max_repetitions (int):
        maxRepetitions MIB variables are requested in response for each of the
        remaining MIB variables in the request. Default: 50
    :param version:
        SNMP version 1 for SNMPv1, 2 for SNMPv2 and 3 for SNMPv3
    :param community
        **OPTIONAL** snmp community string
    ----- SNMP V3 options: ---------------
     In most of the cases, it is the same as SNMP v3 options
     default values are defined in snmp init()

    :return data structure (dict)
         data structure of returned value to a dict reference
         snmp_bulkget() will return {} if snmp bulkget get no response.
    Eg:
        param = {'oid': "IF-MIB::ifInOctets"}
        result = snmp_bulkget(dev0, **param)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Snmp Bulkget    device=${dev}
        ...    oid=IF-MIB::ifInOctets
    """

    current_controller = _get_controller(dev, system_node, controller)
    channelid = kwargs.get('snmp_channel_id', None)
    snmp_channel = _get_snmp_channel(current_controller, channelid)

    oid = kwargs['oid']
    non_repeaters = kwargs.get('non_repeaters', 0)
    max_repetitions = kwargs.get('max_repetitions', 50)

    current_controller.log("Executing SNMP BULKGET on %s" %
                           current_controller.host)
    comm_data = snmp_channel.create_community_data(**kwargs)
    obj_data = snmp_channel.create_object_identity(oid=oid)
    contextdata = snmp_channel.invoke(current_controller, 'ContextData',
                                      snmp_channel.context_engine,
                                      snmp_channel.context_name)
    next_cmd = snmp_channel.invoke(current_controller, 'bulkCmd',
                                   snmp_channel.snmpchannel,
                                   comm_data, snmp_channel.transport,
                                   contextdata, non_repeaters,
                                   max_repetitions, obj_data,
                                   lexicographicMode=False,
                                   ignoreNonIncreasingOid=False)
    return_list = {}
    for (error_indication, error_status, error_index, var_binds) in next_cmd:
        if error_indication:
            current_controller.log(error_indication)
            return False
        elif error_status:
            current_controller.log(level='error', message='%s at %s' % (
                error_status.prettyPrint(), error_index and
                var_binds[int(error_index) - 1][0] or '?'))
            return False
        else:
            for name, val in var_binds:
                if not re.search(r'No Such Instance', val.prettyPrint(), re.I):
                    if prettyprint is True:
                        return_list[name.prettyPrint()] = val.prettyPrint()
                    else:
                        return_list[name.prettyPrint()] = val._value
                else:
                    current_controller.log(
                        level='error', message='No Such Instance currently '
                        'exists at this OID')
                    return False
    return return_list


def check_getnext(dev, system_node='current', controller='current', *args,
                  **kwargs):
    r"""
     check the value of a snmp leaf OID
    :param dev:
        Router handle
    :param system_node
        Node on which to run the command. Default to current_node
    :param controller
        Controller on which to run the command. Default to current_controller
    :param snmp_channel_id:
        Channel ID of SNMP object to be called.
        channel ID of first SNMP object created on the device will be selected
        if not specified.
    :param oid
        **REQUIRED** a string which has one oid.
    :param index
        **OPTIONAL** a string which has information of index

    :param community
        **OPTIONAL** snmp community string
    :param value_expected
        **OPTION** expected value from snmp (string or regrex)
        can be a regex pattern using r''
    :parm next_oid
        **REQUIRED** the next oid you expect to get (string or regrex)

    :return
        TRUE if the value is expected
        FALSE if it is not  expected

     Example:
        param = {'oid': "SNMPv2-MIB::sysUpTime", 'index': '0',
                 'next_oid': "SNMPv2-MIB::sysContact.0",
                 'value_expected': r'\w+'}
        result = check_getnext(**param)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Check Getnext    device=${dev}
        ...    oid=SNMPv2-MIB::sysUpTime    index=0
        ...    next_oid=SNMPv2-MIB::sysContact.0
        ...    value_expected=r'\w+'
    """

    value_expected = kwargs.get('value_expected')
    next_oid = kwargs.get('next_oid')
    oid = kwargs.get('oid')
    index = kwargs.get('index')

    if index:
        oid = oid + '.' + str(index)

    current_controller = _get_controller(dev, system_node, controller)

    # check value:
    try:
        snmpgetnext_result = snmp_getnext(dev, **kwargs)
        oid_result = list(snmpgetnext_result.keys())[0]
        value_result = snmpgetnext_result.get(oid_result)
    except Exception as exception:
        current_controller.log(message="SNMP Get next with oid "
                               "%s failed" % oid, level='error')
        return False

    if not (re.search(value_expected, value_result, re.I) and
            re.search(next_oid, oid_result, re.I)):
        current_controller.log(
            message="get / %s, %s /: " % (oid_result, value_result) +
            "-- expecting: / %s, %s /" % (
                next_oid, value_expected), level='warn')
        return False
    return True


def check_walk(dev, system_node='current', controller='current', *args,
               **kwargs):
    r"""
    check multiple varbinds with snmpwalk on default router /community
    :param dev:
        Router handle
    :param system_node
        Node on which to run the command. Default to current_node
    :param controller
        Controller on which to run the command. Default to current_controller
    :param snmp_channel_id:
        Channel ID of SNMP object to be called.
        channel ID of first SNMP object created on the device will be selected
        if not specified.
    :param check
        **REQUIRED** a dict which has multiple varbinds with snmpwalk
    :param value_expected
        **REQUIRED** a dict which has expected result with snmpwalk

    :return
        TRUE if the value is expected
        FALSE if it is not expected

    Example:
        check = {'oid': "SNMP-FRAMEWORK-MIB::snmpEngine",
                'community': "public"}
        value_expected=[{'variable': "SNMP-FRAMEWORK-MIB::snmpEngineBoots.0",
                        'value': r'\d+'},
                        {'variable': "SNMP-FRAMEWORK-MIB::snmpEngineTime.0",
                        'value': r'\d+'},
                        {'variable':
                        "SNMP-FRAMEWORK-MIB::snmpEngineMaxMessageSize.0",
                        'value': r'\d+'}]
        result = check_walk(dev0, check=check, value_expected=value_expected,
                            timeout=180)

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Check Walk    device=${dev}
        ...    check=${check}
        ...    value_expected=${value_expected}
        ...    timeout=${180}
    """
    value_expected = kwargs.get('value_expected')
    check = kwargs.get('check')
    timeout = kwargs.get('timeout', 30)

    current_controller = _get_controller(dev, system_node, controller)

    #"snmp_walk need hash input"
    check.update({'timeout': timeout})
    try:
        mib = snmp_walk(dev, **check)
    except Exception as exception:
        current_controller.log(message="SNMP walk failed", level='error')
        return False

    if not mib or not value_expected:
        return False
    err = 0
    for i in value_expected:
        oid = i['variable']
        expect = str(i['value'])
        res = str(mib[oid])
        if not re.search(expect, res, re.I):
            current_controller.log(
                message="%s gets wrong value: " % oid +
                "%s, should be %s" % (res, expect), level='warn')
            err = err + 1
    if err:
        return False
    return True


def check_varbind(dev, system_node='current', controller='current', *args,
                  **kwargs):
    '''
    check varbind with snmpget on default router /community
    :param dev:
        Router handle
    :param system_node
        Node on which to run the command. Default to current_node
    :param controller
        Controller on which to run the command. Default to current_controller
    :param snmp_channel_id:
        Channel ID of SNMP object to be called.
        channel ID of first SNMP object created on the device will be selected
        if not specified.
    :param varbind
        **REQUIRED** a dict which has varbind with snmpget
    :param value_expected
        **REQUIRED** a string or regular expression which has expected
        result with snmpget

    :return
        TRUE if the value is expected
        FALSE if it is not expected

    Example:
        param = {'varbind': {'oid': "SNMPv2-MIB::sysContact", 'version': 2,
                             'index': '0'},
                             'value_expected': 'new system contact'}
        result = check_varbind(**param)

    Robot Usage Example  :
        ${result} =    Check Varbind    device=${dev}
        ...    varbind=${varbind}    value_expected=${value_expected}

    '''

    value_expected = kwargs.get('value_expected')
    varbind = kwargs.get('varbind')
    current_controller = _get_controller(dev, system_node, controller)
    #  check value:
    #  return false if no value returned. ("0" is a valid value)
    try:
        result = snmp_get(dev, **varbind)
    except Exception as exception:
        current_controller.log(message="SNMP get failed", level='error')
        return False

    if not result:
        return False
    value = list(result.values())[0]

    if not re.search("%s" % value_expected, value):
        current_controller.log(message="get value %s: --expecting: %s" %
                               (value, value_expected), level='warn')
        return False

    return True


def get_if_snmp_index(dev, **kwargs):
    '''
    This method returns the SNMP index of the interface.
    If no SNMP index is found, it will return undef.

    :param dev:
        Router handle
    :param interface
        **REQUIRED** is the interface name ( "so-0/0/1", "ge-1/1/2.0",...)
    Example:
        get_if_snmp_index(dev=dev0, interface=interface)
    :return snmpindex
        snmp index

    Robot Usage Example  :
        ${dev} =    Get Handle   resource=device0
        ${result} =    Get If Snmp Index    device=${dev}
        ...    interface=ge-1/1/2.0
    '''

    interface = kwargs.get('interface')

    output = dev.cli(command='show interfaces extensive %s | match SNMP'
                     % interface).response()

    if len(output) < 1:
        dev.log(message="snmp index not found", level='info')
        return False
    # set snmp index
    matched_snmp = re.search(r'SNMP\s+ifIndex(:)?\s+(\d+)', output)
    if matched_snmp:
        snmpindex = matched_snmp.group(2)
    else:
        dev.log(message="snmp index not found", level='info')
        return False
    return snmpindex


def __kill_trapd(dev, port=None):
    '''
    Kill existing snmptrapd before starting a new one.
    :param dev:
        Router handle
    :return None
    '''

    cmd = 'ps auxw | grep snmptrapd'
    if port:
        cmd = cmd + " | grep %s" % port
    output = dev.shell(command=cmd).response()
    match = re.search(r'\S+\s+(\d+)\s+.*\s+snmptrapd', output)
    if match:
        pid = match.group(1)
        dev.shell(command="kill -9 %s" % pid)
        return True
    return False


def check_trap(dev, trigger, system_node='current', controller='current',
               *args, **kwargs):
    '''
    This method checks the received trap pdu for a given pattern.
    and returns TRUE if succeccful, FALSE if not.
    :param dev:
        Router handle
    :param trigger
       **REQUIRED** reference to a function, which will generate the trap
    :param pattern
       **REQUIRED** the pattern you are looking for in the trap pdu
    :param pattern_end_trap
        **OPTION** the pattern you are looking for in the trap to
        stop trap. If not defined, trap will be stopped after
         timeout value
    :param time_end_trap
        **OPTION** the time for running trap. Default: 30
    :param timeout
       **OPTION** the timeout for snmp trap. Default: 300

    :param config_trap
       **OPTION** true/fale value which allow to configure snmp
       trap on router or not. Default: true (configure smnmp trap)
    :param trap_group
       **OPTION** the name of the trap-group you configured in the router
       in order to test traps
    :param port
       **OPTION** the port of snmp trap.

    :return result
        False if received the expected trap
        True if didn't receive the expected trap during the timeout

    Eg: result= check_trap(dev0, send_test_trap, pattern='1.6.1.0',
        time_end_trap=15, trap_group='abc')
        if result:
            print ('received the expected trap')
        else:
            print ('Did not receive the expected trap')

    '''
    current_controller = _get_controller(dev, system_node, controller)
    channelid = kwargs.get('snmp_channel_id', None)

    snmp_channel = _get_snmp_channel(current_controller, channelid)
    port = kwargs.get('port', snmp_channel.trap_port)
    trap_group = kwargs.get('trap_group')
    timeout = kwargs.get('timeout', 300)
    pattern = kwargs.get('pattern')
    pattern_end_trap = kwargs.get('pattern_end_trap')
    time_end_trap = kwargs.get('time_end_trap', 30)

    if not isinstance(pattern, list):
        pattern = [pattern]

    config_trap = kwargs.get('config_trap', True)
    if config_trap and trap_group:
        dev.config(
            command_list=['set snmp trap-group %s destination-port %s'
                          % (trap_group, port), 'commit'])
        time.sleep(5)
    else:
        __kill_trapd(dev, port)

    return_value = snmp_channel.get_trap_result(trigger, pattern_end_trap,
                                                time_end_trap, timeout, port)
    found = 0
    for patt in pattern:
        if re.search(patt, return_value):
            found = found + 1
    if found < len(pattern):
        current_controller.log(message="Didn't receive the expected trap",
                               level='warn')
        return False
    return True


def __auto_set_mibdirs(dev, system_node='current', controller='current',
                       *args, **kwargs):
    r"""
     This method used to set the MIBDIRS environment variables
     to ensure that the tools that use the MIBs
     can find and load your MIB file

    Envrionment Arguments which have default values if you don't specify:
    :param default_mibdirs
        **OPTIONAL** point to the directory which has your mib files there.
        Default is
        "/volume/labtools/lib/MIBS:/volume/labtools/lib/MIBS/Juniper"

    :return None
    """
    pattern = r"\/volume\/labtools\/lib\/MIBS:\/volume" +\
        r"\/labtools\/lib\/MIBS\/Juniper"
    current_controller = _get_controller(dev, system_node, controller)
    channelid = kwargs.get('snmp_channel_id', None)
    current_mibdirs = ''

    snmp_channel = _get_snmp_channel(current_controller, channelid)
    default_mibdirs = snmp_channel.mibs_dir
    if default_mibdirs and\
            not re.search(pattern, default_mibdirs):
        current_mibdirs = default_mibdirs
    # Regarding PR 6296.
    if not current_mibdirs:
        current_mibdirs = get_mibs_dir(dev)
        if current_mibdirs == '':
            dev.log(message="Invalid Router Version.", level='warn')
    return current_mibdirs


def get_mibs_dir(dev):
    '''
    This method use to get mibdirs
    :param: dev
        Router object
    :param: host
        router need to get mibdirs
    '''
    ver_string = dev.get_version()
    if re.search(r'^\s*\d+\.\d+[BRISXF]\S+', ver_string):
        # Maintenance Release
        if re.search(r'^\s*(\d+.\d+)([BRISXF]\d+-[BRISXF])(\d+\.\d+|\d+)',
                     ver_string):
            check = re.search(
                r'^\s*(\d+.\d+)([BRISXF]\d+-[BRISXF])(\d+\.\d+|\d+)',
                ver_string)
            ver = check.group(1)
            build = check.group(3)
            _type = check.group(2)
        else:
            check = re.search(
                r'^\s*(\d+.\d+)([BRISXF])(\d+\.\d+|\d+)', ver_string)
        # TT-4371 added support for service-releases with
        # format 10.1S8,10.2S6,10.4X1 etc
            ver = check.group(1)
            _type = check.group(2)
            build = check.group(3)
    elif re.search(r'^\s*\d+.\d+-\d+_ib\S*', ver_string):
        # Integration Branch builds - PR1060399
        check = re.search(
            r'^\s*(\d+.\d+)-(\d+)_(ib[0-9_]+|ib_(?:\d+_){2}\w+)(\.\d+)',
            ver_string)
        # TT-3733, added support for 11.1-20101201_ib_11_3_ft.0 image
        ver = check.group(1)
        build = check.group(2) + check.group(4)
        _type = check.group(3)
    elif re.search(r'^\s*(\d+.\d+)-(\d+)_(pr.*)(\.\d+)\S*', ver_string):
        check = re.search(
            r'^\s*(\d+.\d+)-(\d+)_(pr.*)(\.\d+)\S*', ver_string)
        ver = check.group(1)
        build = check.group(2) + check.group(4)
        _type = check.group(3)
    elif re.search(r'^\s*(\d+.\d+)-(\d+)_((jc|eabu|cbu|slt|rpd|dev)_\d+\w+)(\.\d+)',
                   ver_string):
        check = re.search(r'^\s*(\d+.\d+)-(\d+)_((jc|eabu|cbu|slt|rpd|dev)_\d+\w+)(\.\d+)',
                          ver_string)
        ver = check.group(1)
        build = check.group(2) + check.group(5)
        _type = check.group(3)
    elif re.search(r'(\d+\.\d)-(\d+)_(\w+)\.(\d)', ver_string):
        check = re.search(r'(\d+\.\d)-(\d+)_(\w+)\.(\d)', ver_string)
        ver = check.group(1)
        build = check.group(2) + check.group(4)
        _type = check.group(3)
    elif re.search(r'^\s*\d+\.\d+\-\S+', ver_string):
        # Daily builds
        check = re.search(r'^\s*(\d+.\d+)-(\d+)\w*(\.\d+)?', ver_string)
        ver = check.group(1)
        build = check.group(2) + check.group(3)
        _type = None
    else:
        # others...
        check = re.search(r'^\s*(\d+\.\d+)\S+', ver_string)
        ver = check.group(1)
        build = None
        _type = None
        # if >= version 8.4, invalid version string
        # PR 1038333 removing this check
        # Not sure why this is here in the first place.
        # The next if statement contradict this logic anyway
        # if ($ver ge "8.4") {
        #    put_log(level=>'WARN',
        # msg=>"Unsupported version: $ver_string");
        #    return "";
        # else just ignore the rest of the version string

    if ver and build and float(ver) >= 8.4:
        if _type and re.search(r'^[BRF]', _type):
            # Maintenance Release
            mibs_dir = "/volume/build/junos/%s/" % ver +\
                "release/%s%s%s/src/juniper/shared/mibs" % (ver, _type, build)
            if float(ver) >= 9.5:
                mibs_dir = "/volume/build/junos/%s/" % ver +\
                    "release/%s%s%s/src/junos/" % (ver, _type, build) +\
                    "shared/mibs"
        elif _type and re.search(r'^[XS]', _type):
            # Service Release
            mibs_dir = "/volume/build/junos/%s/service/" % ver +\
                "%s%s%s/src/juniper/shared/mibs" % (ver, _type, build)
            if float(ver) >= 9.5:
                mibs_dir = "/volume/build/junos/%s/service/" % ver +\
                    "%s%s%s/src/junos/shared/mibs" % (ver, _type, build)
        elif _type and re.search(r'^ib', _type):
            # Integration Branch Release - PR1060399
            mibs_dir = "/volume/build/junos/%s/%s/" % (_type, ver) +\
                "development/%s/src/junos/shared/mibs" % build
        elif _type and re.search(r'pr', _type):
            mibs_dir = "/volume/build/junos/%s/%s/" % (_type, ver) +\
                "daily/%s/src/junos/shared/mibs" % build
        elif _type and re.search(r'(jc|eabu|cbu|slt|rpd|dev|exesp_morpheus)',
                                 _type):
            mibs_dir = "/volume/build/junos/%s/%s/" % (_type, ver) +\
                "development/%s/src/junos/shared/mibs" % build
        elif _type:
            # internal builds.
            # points to daily current
            mibs_dir = "/volume/build/junos/%s/daily/current/src/" % ver +\
                "juniper/shared/mibs"
            # 1046876
            if float(ver) >= 9.5:
                mibs_dir = "/volume/build/junos/%s/daily/current/src/" % ver +\
                    "junos/shared/mibs"

        else:
            # Daily build
            mibs_dir = "/volume/build/junos/%s/daily/%s/" % (ver, build) +\
                    "src/juniper/shared/mibs"
            # 1046876
            if float(ver) >= 9.5:
                mibs_dir = "/volume/build/junos/%s/daily/%s" % (ver, build) +\
                    "/src/junos/shared/mibs"

    elif 'WB_TC_LOGGING' in os.environ.keys():
        if re.search(r'^\s*(\d+\.\d+)I (\d+\-\d+\-\d+)\s', ver_string):
            check = re.search(r'^\s*(\d+\.\d+)I (\d+\-\d+\-\d+)\s', ver_string)
            mibs_dir = "/volume/regressions/JUNOS/CBR/%s/" % check.group(1) +\
                "%s/build/src/junos/shared/mibs" % check.group(2)
        else:
            dev.log(message="Unable to locate mib directory for CBR "
                    "build: %s" % ver_string, level='error')
            mibs_dir = None
    else:
        if _type and re.search(r'^[BR]', _type):
            # Maintenance Release
            mibs_dir = "/volume/build/%s%s%s/" % (ver, _type, build) +\
                "src/juniper/shared/mibs"
        elif _type:
            # internal builds.
            # points to daily current
            mibs_dir = "/volume/build/%s/current/src/" % ver +\
                "juniper/shared/mibs"
        else:
            # Daily build
            mibs_dir = "/volume/build/%s/%s/" % (ver, build) +\
                "src/juniper/shared/mibs"

    if 'MIBDIRS' in os.environ.keys():
        mibs_dir = os.environ['MIBDIRS']
        dev.log(message="MIBDIR %s picked from the ENV " % mibs_dir,
                level='info')
    return mibs_dir


def _get_snmp_channel(controller, channelid=None):
    """
    Get id of the oldest channel of controller object
    :param controller: Controller object
    :param channelid: ID of the channel to get
    :return: channel object, exception if no channel
    """

    if isinstance(controller.channels,
                  dict) and 'snmp' in controller.channels.keys():
        snmpchannel = controller.channels['snmp']
    else:
        raise Exception("SNMP channel not present in controller")

    if channelid:
        if channelid in snmpchannel.keys():
            return snmpchannel[channelid]
        else:
            raise Exception("SNMP channel with ID %s not found" % channelid)
    else:
        return list(snmpchannel.values())[0]


def _get_controller(dev, system_node, controller):
    """
    Get the controller object on which snmp is run.
    :param dev:
    :param system_node:
    :param controller:
    :return: Controller Object
    """
    system_node = system_node.lower()
    controller = controller.lower()
    if system_node == 'current':
        node = dev.current_node
    elif system_node in dev.nodes.keys():
        node = dev.nodes[system_node]
    else:
        raise Exception(
            "System Node %s does not exist for the device" % system_node)

    if controller == 'current':
        controller_obj = node.current_controller
    elif controller in node.controllers.keys():
        controller_obj = node.controllers[controller]
    else:
        raise Exception("Controller %s does not " % controller +
                        "exist for the device in node %s " % system_node)

    return controller_obj
