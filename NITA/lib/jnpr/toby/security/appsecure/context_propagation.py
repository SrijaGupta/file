#!/usr/bin/python3
"""Context propagation specific  keywords"""
#=========================================================================
#
#         FILE:  context_propagation.py
#  DESCRIPTION:  Context propagation specific  keywords
#       AUTHOR:  Mohammad Ismail Qureshi ( mqureshi)
#      COMPANY:  Juniper Networks
#      VERSION:  1.0
#=========================================================================

import re


def get_context_propagation_trace(device=None):
    """
    To get trace of all flow PICs
    Example:
     get_context_propagation_trace(device=srx)
    Robot Example:
     get context propagation trace  device=${srx}

    :param Device device:
               **REQUIRED** Handle for SRX device
     :return: Trace output.
     :rtype: str
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    output = ""
    destination = device.get_srx_pfe_names()
    for dstn in destination:
        response = device.vty(command="show usp flow trace 0", destination=dstn)
        output = output + response.response()
    return output


def clear_flow_trace(device=None):
    """
    To clear vty traces
    Example:
      clear_flow_trace(device=srx)
    Robot Example:
      clear flow trace  device=srx

    :param Device device:
               **REQUIRED** Handle for SRX device
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    destination = device.get_srx_pfe_names()
    for dstn in destination:
        device.vty(command="clear usp flow trace", destination=dstn)
    return True


def enable_jdpi_test_plugin(device=None, service_plugin=None):
    """
    To enable JDPI Test plugin and debug
    Example:
      enable_jdpi_test_plugin(device=srx, service_plugin= yes)
    Robot Example:
      enable jdpi test plugin  device handle=${srx}    service_plugin= yes

    :param Device device:
               **REQUIRED** Handle for SRX device
    :param str service_plugin:
               *OPTIONL* Flag to set command list for enabling plugin
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    plugin_enable_list = ["plugin jdpi set debug module flow enable",
                          "plugin jdpi set debug module engine enable",
                          "plugin jdpi set debug module asc enable",
                          "plugin jdpi set debug module engine_evt enable",
                          "test usp jsf test_plugin enable",
                          "test usp jsf test_plugin dpi enable",
                          "test usp jsf test_plugin dpi service mode 3",
                          "plugin jdpi test set display binary enable",
                          "plugin jdpi set debug level 3",
                          "plugin jdpi clear counters all",
                          "plugin jdpi set config force_pkt_plugin enable",
                          "set usp flow local-debug-buf state 1",
                          "test usp jsf test_plugin stream_short_circuit trace 0x8"]

    plugin_enable_list_service = ["test usp jsf test_plugin enable",
                          "plugin jdpi set config force_pkt_plugin enable",
                          "test usp jsf test_plugin dpi enable",
                          "test usp jsf test_plugin dpi service mode 1",
                          "test usp jsf test_plugin dpi service mode 3",
                          "plugin jdpi test set display binary enable",
                          "test usp jsf test_plugin dpi service mode 4",
                          "set usp flow local-debug-buf size 100000",
                          "set usp flow local-debug-buf state 1",
                          "plugin junos_ssl set debug enable",
                          "plugin junos_ssl set debug level 3",
                          "plugin junos_ssl set debug module all",
                          "plugin jdpi set debug level 3",
                          "plugin jdpi set debug module flow enable",
                          "plugin jdpi set debug module engine enable",
                          "plugin jdpi set debug module engine enable"]
    # Getting flow pics and then execting commands
    if service_plugin is None:
        cmd_list = plugin_enable_list
    else:
        cmd_list = plugin_enable_list_service

    destination = device.get_srx_pfe_names()
    for dstn in destination:
        for command in cmd_list:
            device.vty(command=command, destination=dstn)
    return True


def disable_jdpi_test_plugin(device=None):
    """
    To disable JDPI Test plugin and debug
    Example:
      disable_jdpi_test_plugin(device=srx)
    Robot Example:
      disable jdpi test plugin  device handle=${srx}

    :param Device device:
               **REQUIRED** Handle for SRX device
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    plugin_disable_list = ["plugin jdpi set debug module flow disable",
                           "plugin jdpi set debug module asc disable",
                           "plugin jdpi set debug module engine_evt disable",
                           "test usp jsf test_plugin disable",
                           "test usp jsf test_plugin dpi disable",
                           "plugin jdpi test set display binary disable",
                           "plugin junos_ssl set debug disable",
                           "plugin jdpi set debug module flow disable",
                           "plugin jdpi set debug module engine disable",
                           "plugin jdpi clear counter all"]
    # Get flow pics
    destination = device.get_srx_pfe_names()
    for dstn in destination:
        for command in plugin_disable_list:
            device.vty(command=command, destination=dstn)
    return True


def register_context(device=None, protocol_id=None, contexts=None):
    """
    To register protcol contexts
    Example:
     register_context(protocol_id="75", contexts=[2,555,513,519])
    Robot example:
      register context  protocol_id=75  contexts=[2,555,513,519]

    :param Device device:
               **REQUIRED** Handle for SRX device
    :param str protocol_id:
               **REQUIRED** Protocol id , to register protocol specific contexts
    :param list contexts:
               *OPTIONAL* Context list , to register specific contexts, if not passed all context
                          will be rigetered
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    if protocol_id is None:
        device.log(level='ERROR', message="protocol_id is mandatory argument")
        raise ValueError("protocol_id is mandatory argument")

    # Getting flow pic list from DUT
    destination = device.get_srx_pfe_names()
    # Context list is not passed , will register all context for given protocol
    if contexts is None:
        cmd = 'test usp jsf test_plugin dpi register single_proto_all_ctx ' + protocol_id
        for dstn in destination:
            response = device.vty(command=cmd, destination=dstn)
            if "Successfully Registered" in response.response():
                device.log(level='INFO', message="All contexts are registered successfully")
            else:
                device.log(level='ERROR', message="Contexts registration failed for %s" \
                                                                              %(protocol_id))
                raise Exception("Contexts registration failed")
        return True         
    # Context list passed by user will register them one by one
    cmd = 'test usp jsf test_plugin dpi register single_proto_single_ctxt'
    cmd = cmd + ' ' + protocol_id
    # Iterating flow pics and executing command for each context id
    for dstn in destination:
        for context in contexts:
            cmd1 = cmd + ' ' + str(context)
            response = device.vty(command=cmd1, destination=dstn)
            if "Successfully Registered" in response.response():
                device.log(level='INFO', message="Context %s is registered successfully"
                           % (str(context)))
            else:
                device.log(
                    level='ERROR',
                    message="Context %s registration failed" %
                    (str(context)))
                raise Exception("Context %s registration failed" % (context))
    return True


def deregister_context(device=None, protocol_id=None, contexts=None):
    """
    To register protcol contexts
    Example:
      deregister_context(protocol_id="75", contexts=["2","555","513","519"])
    Robot example:
      deregister context  protocol_id=75  contexts=["2","555","513","519"]

    :param Device device:
               **REQUIRED** Handle for SRX device
    :param str protocol_id:
               **REQUIRED** Protocol id , to deregister protcol specific contexts
    :param list contexts:
               *OPTIONAL* Context list , to deregister specific contexts,if not passed all context
                          will be derigetered
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    if protocol_id is None:
        device.log(level='ERROR', message="protocol_id is mandatory argument")
        raise ValueError("protocol_id is mandatory argument")

    # Getting flow pic list from DUT
    destination = device.get_srx_pfe_names()
    # Context list is not passed , will deregister all context for given protocol
    if contexts is None:
        cmd = "test usp jsf test_plugin dpi deregister single_proto_all_ctx %s" % (protocol_id)
        for dstn in destination:
            response = device.vty(command=cmd, destination=dstn)
            if "Successfully Deregistered" in response.response():
                device.log(level='INFO', message="All contexts are deregistered successfully")
            else:
                device.log(level='ERROR', message="Contexts deregistration failed")
                raise Exception("Contexts deregistration failed")
        return True
    # Context list passed by user will deregister them one by one
    cmd = "test usp jsf test_plugin dpi deregister single_proto_single_ctxt"
    cmd = cmd + " " + protocol_id + " "
    # Iterating flow pics and executing command for each context id
    for dstn in destination:
        for context in contexts:
            cmd1 = cmd + " " + context
            response = device.vty(command=cmd1, destination=dstn)
            if "Successfully Deregistered" in response.response():
                device.log(level='INFO', message="Context %s is deregistered successfully"
                           % (context))
            else:
                device.log(level='ERROR', message="Context %s deregistration failed" % (context))
                raise Exception("Context %s deregistration failed" % (context))
    return True


def clear_context_hit(device=None, protocol="all"):
    """
    To clear context hit
    Example:
      clear_context_hits(device=srx)
    Robot Example:
      clear context hits  device=srx

    :param Device device:
               **REQUIRED** Handle for SRX device
    :param str protocol:
               *OPTIONAL* Protocol name to clear context
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    destination = device.get_srx_pfe_names()
    for dstn in destination:
        response = device.vty(
            command="plugin jdpi clear application parsed_ctx_stats %s" \
                                                           % (protocol), destination=dstn)
        match = re.search('Cleared all the application context stats', response.response())
        if not match:
            device.log(level='ERROR', message="Contexts are not cleared")
            raise Exception("Contexts are not cleared")
    return True


def match_context_hit(device=None, context_name=None, context_id=None, hit_count=0, protocol="all"):
    """
    To match context hits
    Example:
      match_context_hit(device=srx, context_name="subject", context_id="607", hit_count="5")
    Robot example:
      match context hit  device=srx  context_name="subject"  context_id="607"  hit_count="5"

    :param Device device:
               **REQUIRED** Handle for SRX device
    :param str context_id`:
               **REQUIRED** Context id,to be matched
    :param str context_name:
               **REQUIRED** Context name, to be matched
    :param str hit_count:
               **REQUIRED** Context hit count , to be matched
    :param str protocol:
               *OPTIONAL* Protocol name to match protocol specific context
    :return: True if successful.
                 In all other cases Exception is raised
    :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    if context_name is None or context_id is None or hit_count is None:
        device.log(level='ERROR', message="context_name,context_id and hit_count are mandatory \
                   argument")
        raise ValueError("context_name,context_id and hit_count are mandatory argument")

    match_flag = False
    destination = device.get_srx_pfe_names()
    for dstn in destination:
        response = device.vty(
            command="plugin jdpi show application parsed_ctx_stats %s" % (protocol),
            destination=dstn)
        match = re.search(
            context_name + '.*' + '(' + context_id + ')' + '.*' + r'\s' + hit_count, response.response())
        if match:
            match_flag = True
            break
    if match_flag:
        device.log(level='INFO',
                   message=" %s context got hit %s times, match successfull" \
                                                                       % (context_name, hit_count))
        return True 
    else:
        device.log(level='ERROR',
                   message=" %s context was not hit %s times, match unsuccessfull" \
                                                                        % (context_name, hit_count))
        raise Exception("%s context was not hit %s times, match unsuccessfull"
                        % (context_name, hit_count))


def match_string_context_propagation(device=None, cntx_id=None, value=None, length=None,
                                     count=None, **kwargs):
    """
    To match context propagation of string type contexts
    Example:
      match_string_context_propagation(device=srx, cntx_id=607,value="mail via relay host", trace=trace)
      match_string_context_propagation(device=srx, cntx_id=607,value="mail via relay host",length=20
                                       count=1)
    Robot example:
      match string context propagation  device=${srx}  cntx_id=607  value="mail via relay host"
      match string context propagation  device=${srx}  cntx_id=607  value="mail via relay host"
                                        length=20  count=1  trace=trace

    :param Device device:
               **REQUIRED** Handle for SRX device
    :param str cntx_id:
               **REQUIRED** Context id,to be matched
    :param str value:
               **REQUIRED** Context value, to be matched
    :param str length:
               *OPTIONAL* Length of context value
    :param str count:
               *OPTIONAL* Count of match pattern
    :param str trace:
               *OPTIONAL* String containing vty trace logs for match
    :return: True if successful.
                 In all other cases Exception is raised
    :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    if cntx_id is None or value is None:
        device.log(level='ERROR', message="cntx_id,value and length are mandatory argument")
        raise ValueError("context_id and value are mandatory argument")

    # Get traces
    if 'trace' in kwargs:
        output = kwargs.get('trace')
    else:
        output = get_context_propagation_trace(device=device)

    device.log(level='INFO', message="Value is %s" % value)
    if length is None:
        match = re.findall \
            (r'pctxt_id : string => \[' + str(cntx_id) + '.*' + value,
            str(output), re.IGNORECASE)
    else:
        match = re.findall \
            (r'pctxt_id : string => \[' + str(cntx_id) + '.*' + value + r'\(' + str(length) + r'\)',
            str(output), re.IGNORECASE)   

    if match:
        match_count = len(match)
        device.log(level='INFO', message="Pattern found %d times in trace" % match_count)
        # Checking if pattern matched as per users's expectation ,if count is passed by user
        if count is None:
            device.log(level='INFO', message="Context propgated as per expectation")
        elif count is not None and int(match_count) == int(count):
            device.log(level='INFO', message="Context propgated as per expectation")
        else:
            device.log(level='ERROR', message="Context not propgated as per expectation")
            raise Exception("Context not propgated as per expectation")
    else:
        device.log(level='ERROR', message="%s pattern not found in trace" %(value))
        raise Exception("%s pattern not found in trace" %(value))
    return True


def match_integer_context_propagation(device=None, cntx_id=None, value=None, count=None, **kwargs):
    """
    To match context propagation of integer type contexts
    Example:
      match_integer_context_propagation(device=srx, cntx_id="869",value="27")
      match_integer_context_propagation(device=srx, cntx_id="11",value="250",count=2,trace=trace)
    Robot example:
      match integer context propagation  device=${srx}  cntx_id=869  value=27
      match integer context propagation  device=${srx}  cntx_id=11  value=250  count=2  trace=trace

    :param Device device:
               **REQUIRED** Handle for SRX device
    :param str cntx_id:
               **REQUIRED** Context id,to be matched
    :param str value:
               **REQUIRED** Context value, to be matched
    :param str count:
               *OPTIONAL* Count of match pattern
    :param str trace:
               *OPTIONAL* String containing vty trace logs for match
    :return: True if successful.
                 In all other cases Exception is raised
    :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    if cntx_id is None or value is None:
        device.log(level='ERROR', message="context_id and value length are mandatory argument")
        raise ValueError("context_id and value are mandatory argument")

    # Get traces
    if 'trace' in kwargs:
        output = kwargs.get('trace')
    else:
        output = get_context_propagation_trace(device=device)

    match = re.findall \
        ('pctxt_id :' + '.*' + r'\[' + str(cntx_id) + "=>" +
         str(value) + r'\]', str(output), re.IGNORECASE)
    if match:
        match_count = len(match)
        device.log(level='INFO', message="Pattern found %d times in trace" % match_count)
        # Checking if pattern matched as per users's expectation ,if count is passed by user
        if count is None:
            device.log(level='INFO', message="Context propgated as per expectation")
        elif count is not None and int(match_count) == int(count):
            device.log(level='INFO', message="Context propgated as per expectation")
        else:
            device.log(level='ERROR', message="Context not propgated as per expectation")
            raise Exception("Context not propgated as per expectation")
    else:
        device.log(level='ERROR', message="%s pattern not found in trace" %(value))
        raise Exception("%s pattern not found in trace" %(value))
    return True


def match_buffer_context_propagation(device=None, cntx_id=None, initial_bytes=None, last_bytes=None,
                                     length=None, **kwargs):
    """
    To match context propagation of buffer context
    Example:
    first_byte="54 68 69 73 20 69 73 20 6a 75"
    last_byte="66 6f 72 20 63 6f 6e 74 65 78"
    match_buffer_context_propagation(device=srx, cntx_id="514", initial_bytes=first_byte,
                                     last_bytes=last_byte, trace=trace)
    Robot example:-
    match buffer context propagation  device=${srx}  cntx_id="514"  initial_bytes=first_byte
                                     last_bytes=last_byte  trace=trace
    :param Device device:
               **REQUIRED** Handle for SRX device
    :param str cntx_id:
               **REQUIRED** Context ID of buffer context
    param str initial_bytes:
               **REQUIRED** Initial bytes of content , 1st 10 HEX byte
    param str last_bytes:
               **REQUIRED** Last bytes of content , last 10 HEX byte
    param str length:
               *OPTIONAL* Length of content
    :param str trace:
               *OPTIONAL* String containing vty trace logs for match
    :return: True if successful.
                 In all other cases Exception is raised
    :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")

    if cntx_id is None or initial_bytes is None or last_bytes is None:
        device.log(level='ERROR', message="context_id,initial_bytes and last_bytes are mandatory \
                                          argument")
        raise ValueError("context_id,initial_bytes and last_bytes are mandatory argument")

    # Get traces
    if 'trace' in kwargs:
        output = kwargs.get('trace')
    else:
        output = get_context_propagation_trace(device=device)
    # Matching length if passed by user
    if length is not None:
        match = re.search(r'pctxt_id : .* byte_array total len to print => \[' + str(cntx_id) +
                          '=>' + str(length), output)
        if match:
            device.log(level='INFO', message="Length of content is matched")
        else:
            device.log(level='ERROR', message="Length of content is not matched, \
                                             will not match content")
            raise Exception("Length of content is not matched,will not match content")
    initial_buffer_flag = False
    # Fetching initial byte of conetnt
    match = re.search(r'pctxt_id : .* byte_array partial info => \[' + str(cntx_id), output)
    if match:
        initial_buffer_flag = True
        match = re.search(r'pctxt_id : .* byte_array partial info => \[' + str(cntx_id) + '=>' +
                          '(.*)' + r'\([0-9]+\)\)\]', output)
        if match:
            initial_bytes_in_trace = match.group(1)
            initial_bytes_in_trace = initial_bytes_in_trace.replace("0x", "")
    # Fetching last bytes of content
    match = re.search(r'pctxt_id : .* byte_array final info => \[' + str(cntx_id), output)
    if match:
        match = re.search(r'pctxt_id : .* byte_array final info => \[' + str(cntx_id) + '=>' +
                          '(.*)' + r'\([0-9]+' + '.*' + r'\)\)\]', output)
        if match:
            last_bytes_in_trace = match.group(1)
            last_bytes_in_trace = last_bytes_in_trace.replace("0x", "")
            last_bytes_in_trace = last_bytes_in_trace[:-1]
    else:
        device.log(level='ERROR', message="Final/Last trace of content not found,match \
                                                                             cannot take place")
        raise Exception("Final/Last trace of content not found,match cannot take place")
    # Matching initial bytes of content
    if initial_buffer_flag:
        if initial_bytes in initial_bytes_in_trace:
            device.log(level='INFO', message="Starting contents matched")
        else:
            device.log(level='ERROR', message="Starting contents not matched")
            raise Exception("Starting contents not matched")
    else:
        # Handling case if contents are in single trace buffer
        if initial_bytes in last_bytes_in_trace:
            if last_bytes in last_bytes_in_trace:
                device.log(level='INFO', message="Contents matched fully")
                return True
            else:
                device.log(level='ERROR', message="Contents not matched fully")
                raise Exception("Contents not matched fully")
        else:
            device.log(level='ERROR', message="Initial contents not matched")
            raise Exception("Initial contents not matched")
    # If user has passed more byte as last bytes then bytes came in last trace buffer,
    # Will strip last bytes passed by user and match with bytes available in trace
    if len(last_bytes) > len(last_bytes_in_trace):
        strip_count = len(last_bytes) - len(last_bytes_in_trace)
        last_bytes = last_bytes[strip_count:]
    # Matching last bytes of content
    if last_bytes in last_bytes_in_trace:
        device.log(level='INFO', message="Contents matched fully")
        return True
    else:
        device.log(level='ERROR', message="Contents not matched fully")
        raise Exception("Contents not matched fully")
