"""
Cisco utils functions
"""
import re
import time
from jnpr.toby.exception.toby_exception import TobyException

def get_loopback_adress(device, loop_ip=None):
    """
    Get the loopback address from the router
    :param loop_ip:
        *OPTIONAL* User can pass ipadress or
        else it will get from interface address
    :returns:
        Loopback address of the router
    """
    device.log(level="DEBUG",
               message="Entering 'get_loopback_address'\n" + __file__)
    match_loop = re.search(r'^127\.0\.0\.1', loop_ip)
    if loop_ip and match_loop:
        device.log(level='INFO',
                   message='Returning Loopback adsress %s' % loop_ip)
        device.log(level="DEBUG", message="Exiting 'get_loopback_address' "
                   "with return value/code :\n" + str(loop_ip))
        return loop_ip
    else:
        address = device.get_interface_address(interface='lo0')
        if address and isinstance(address, list):
            loop_ip = []
            for loopip in address:
                loop = re.search(r'^(.*)/.*$', loopip)
                if loop:
                    loop_ip.append(loop.group(1))
            device.log(level='INFO',
                       message='Returning loopback address %s' % loop_ip)
            device.log(level="DEBUG",
                       message="Exiting 'get_loopback_address' with "
                       "return value/code :\n" + str(loop_ip))
            return loop_ip
        elif address and isinstance(address, str):
            loop = re.search(r'^(.*)/.*$', address)
            loop_ip = loop.group(1)
            device.log(level='INFO',
                       message='Returning loopback address %s' % loop_ip)
            device.log(level="DEBUG",
                       message="Exiting 'get_loopback_address' with "
                       "return value/code :\n" + str(loop_ip))
            return loop_ip
        else:
            device.log(level='INFO',
                       message='Failed to get loopback address')
            result = False
            device.log(level="DEBUG",
                       message="Exiting 'get_loopback_address' with "
                       "return value/code %s:\n" % result)
            return result


def get_image(device):
    """
    Get the running image name
    :return:
        Get the running image name
    """
    device.log(level="DEBUG", message="Entering 'get_image'\n" + __file__)
    response = device.cli(command='show version', timeout=60).response()
    lines = response.split('\n')
    image = ''
    for line in lines:
        if re.search('System image file is |System Release: ', line, re.I):
            search = re.search(r'"?([^"\s]+)"?\s*$', line, re.I)
            if search:
                image = search.group(1)
                device.log(level='INFO',
                           message='get_image: Returning image:%s' % image)
                device.log(level="DEBUG", message="Exiting 'get_image' with "
                           "return value/code :\n" + str(image))
                break
            
    device.log(level='INFO',
               message='get_image: Returning image:%s' % image)
    device.log(level="DEBUG", message="Exiting 'get_image' with "
               "return value/code :\n" + str(image))
    return image


def check_isis_neighbor(device, system_id='', router_type='', interface='',
                        ip_address='', state='Up', circuit_id='',
                        num=None, timeout=90, interval=10, options=None):
    """
    Check isis neighbor
    :param system_id:
        *OPTIONAL* string or list of string system id of neighbors
    :param router_type:
        *OPTIONAL* string or list of string router type of neighbors
    :param interface:
        *OPTIONAL* string or list of string interface of neighbors
    :param ip_address:
        *OPTIONAL* string or list of string ip address of neighbors
    :param circuit_id:
        *OPTIONAL* string or list of string circuit id of neighbors
    :param state:
        *OPTIONAL* string state of neighbors
        Default: 'up'
    :param num:
        *OPTIONAL* int number of isis neighbor need to check
        if num is None: check all isis neighbors
    :param timeout:
        *OPTIONAL* number of retries. Default: 90
    :param interval
        *OPTIONAL* number seconds between retries. Default: 10
    :param options
        *OPTIONAL* option for show command

    :returns:
        TRUE if all isis neighbor is found
        FALSE if 1 or some of isis neighbors is not found
    """
    device.log(level="DEBUG",
               message="Entering 'check_isis_neighbor'\n" + __file__)
    if not isinstance(system_id, list):
        system_id = [system_id]
    if not isinstance(router_type, list):
        router_type = [router_type]
    if not isinstance(interface, list):
        interface = [interface]
    if not isinstance(ip_address, list):
        ip_address = [ip_address]
    if not isinstance(circuit_id, list):
        circuit_id = [circuit_id]

    max_value = max([len(system_id), len(router_type), len(interface),
                     len(ip_address), len(circuit_id)])
    system_id += (max_value - len(system_id)) * [""]
    router_type += (max_value - len(router_type)) * [""]
    interface += (max_value - len(interface)) * [""]
    ip_address += (max_value - len(ip_address)) * [""]
    circuit_id += (max_value - len(circuit_id)) * [""]

    cmd = 'show isis neighbors'
    if options:
        cmd = "%s %s" % (cmd, options)
    device.log(level='INFO', message='Executing %s' % cmd)
    return_value = False
    neighbor_re = r'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\w+)\s+\d+\s+(\S+)'
    while timeout >= 0:
        response = device.cli(command=cmd, timeout=30).response()
        lines = response.split('\n')
        number_neighbor = 0
        state_found = 0
        for line in lines:
            match = re.search(neighbor_re, line, re.I)
            if match:
                for sys_id, r_type, inter, ip_addr, cir_id in zip(
                        system_id, router_type, interface, ip_address,
                        circuit_id):
                    if re.search(sys_id, match.group(1), re.I) and \
                            re.search(r_type, match.group(2), re.I) and \
                            re.search(inter, match.group(3), re.I) and \
                            re.search(ip_addr, match.group(4), re.I) and \
                            re.search(cir_id, match.group(6), re.I):
                        number_neighbor += 1
                        if re.search(state, match.group(5), re.I):
                            state_found += 1
        if not num:
            num = number_neighbor
        if state_found >= num and state_found > 0:
            return_value = True
            device.log(level="info", message="%s neighbors: %s "
                       % (number_neighbor, state))
            break

        device.log(level="info", message="Continue checking states. "
                   "Expire in %s seconds" % timeout)
        timeout = timeout - interval
        time.sleep(interval)

    device.log(level="DEBUG", message="Exiting 'check_isis_neighbor'"
               "with return value/code :\n" + str(return_value))
    return return_value


def check_ospf_neighbor(device, ospfv3=False, address='', interface='',
                        router_id='', state='Full', num=None, timeout=90,
                        interval=10, options=None):
    """
    Check ospf neighbor
    :param ospfv3:
        *OPTIONAL* True/False. check ospf neighbor for ospfv3.
        Default: False
    :param address:
        *OPTIONAL* string or list of string ip address of neighbors
    :param router_id:
        *OPTIONAL* string or list of string router id of neighbors
    :param state:
        *OPTIONAL* string state of neighbors
        Default: 'Full'
    :param interface:
        *OPTIONAL* string or list of string interface of neighbors
    :param num:
        *OPTIONAL* int number of ospf neighbor need to check
        if num is None: check all ospf neighbors
    :param timeout:
        *OPTIONAL* number of retries. Default: 90
    :param interval:
        *OPTIONAL* number seconds between retries. Default: 10
    :param options:
        *OPTIONAL* option for show command

    :returns:
        TRUE if all ospf neighbor is found
        FALSE if 1 or some of ospf neighbors is not found
    """
    device.log(level="DEBUG",
               message="Entering 'check_ospf_neighbor'\n" + __file__)
    if not isinstance(address, list):
        address = [address]
    if not isinstance(interface, list):
        interface = [interface]
    if not isinstance(router_id, list):
        router_id = [router_id]
    max_value = max([len(address), len(interface), len(router_id)])
    address += (max_value - len(address)) * [""]
    interface += (max_value - len(interface)) * [""]
    router_id += (max_value - len(router_id)) * [""]
    if ospfv3:
        cmd = 'show ipv6 ospf neighbor'
    else:
        cmd = 'show ip ospf neighbor'
    if options:
        cmd = "%s %s" % (cmd, options)
    device.log(level='INFO', message='Executing %s' % cmd)
    return_value = False
    neighbor_re = r'(\S+)\s+\d+\s+(\w+)\/\S+\s+(\S+)\s+(\S+)\s+(\S+)'
    while timeout >= 0:
        response = device.cli(command=cmd, timeout=30).response()
        number_neighbor = 0
        state_found = 0
        for line in response.split('\n'):
            match = re.search(neighbor_re, line, re.I)
            if match:
                for rid, intf, add in zip(router_id, interface,
                                          address):
                    if re.search(rid, match.group(1), re.I) and \
                            re.search(add, match.group(4), re.I) and \
                            re.search(intf, match.group(5), re.I):
                        number_neighbor += 1
                        if re.search(state, match.group(2), re.I):
                            state_found += 1
        if not num:
            num = number_neighbor
        if state_found >= num and state_found > 0:
            return_value = True
            device.log(level="info", message="%s neighbors: %s "
                       % (number_neighbor, state))
            break
        device.log(level="info", message="Continue checking states. "
                   "Expire in %s seconds" % timeout)
        timeout = timeout - interval
        time.sleep(interval)

    device.log(level="DEBUG", message="Exiting 'check_ospf_neighbor' with "
               "return value/code :\n" + str(return_value))
    return return_value


def check_bgp_peer(device, state=None, peer=None, timeout=180):
    """
    Check peer's state for BGP
    :param state:
        **OPTIONAL** state of peer. Ex : Idle, Active
    :param peer:
        **REQUIRED** list of peer need for checking
    :param timeout:
        **OPTIONAL** timeout for checking. Default is 180s
    :returns:
        True if find peer and match state
        else False
    """
    device.log(level="DEBUG", message="Entering 'check_bgp_peer'\n" + __file__)
    interval = 10
    if peer and not isinstance(peer, list):
        peer = [peer]
    while timeout >= 0:
        result = True
        output = device.cli(command='show ip bgp summary').response()
        if not output or re.search(r'BGP is not running', output, re.I):
            device.log(level='error',
                       message="Output of cli is Null or BGP is not running")
            return False
        for per_peer in peer:
            peer_found = 0
            for line in output.split("\n"):
                match = re.search(
                    r'%s\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
                    r'\s+(\S+)\s+(\S+)\s+(\S+)' % per_peer, line)
                if match:
                    peer_found += 1
                    if not state:
                        if not match.group(9).isdigit():
                            device.log(
                                message=" Peer %s check failed with "
                                "state %s" % (per_peer, match.group(9)),
                                level='info')
                            result = False
                        else:
                            device.log(
                                level='info',
                                message='Peer %s check passed' % per_peer)
                    else:
                        if match.group(9) == state:
                            device.log(
                                level='info',
                                message='Peer %s check passed' % per_peer)
                        else:
                            device.log(
                                level='info',
                                message=" Peer %s check failed with state "
                                "%s" % (per_peer, match.group(9)))
                            result = False
            if peer_found == 0:
                device.log(level='info',
                           message='No found BGP peer %s ' % per_peer)
                result = False
        if not result:
            time.sleep(interval)
            timeout = timeout - interval
        else:
            break
    device.log(level="debug",
               message=" Exit 'check_bgp_peer': Returning %s" % result)
    return result


def check_interface_status(device, interface=None):
    """
    Checks interface status is in up or not.
    :param interface:
        *REQUIRED* Interface name
    :returns:
        Dictionary of interface name with True/False
        If the interface status as up then dictionary stores with True
        If the interface status as down then dictionary stores with False
    """
    if not interface:
        device.log(level='DEBUG', message='No interface specified')
        raise TobyException("No interface specified")
    status_all = {}
    if not isinstance(interface, list):
        interface = [interface]
    for intf in interface:
        response = device.cli(command="show interface %s" % intf).response()
        search = re.search(
            r'(?:invalid|incomplete|command)\s+(?:input|command|failed)',
            response, re.I)
        if not response or search:
            device.log(level="DEBUG",
                       message="Error while executing show interface command")
            raise TobyException("Error while executing the show interface command")
        else:
            output = response.split('\n')
            search1 = re.search(r'\S+\s+is\s+([^,]+),.*\s+is\s+(.*?)\s*$',
                                output[0], re.I)
            info_all = {}
            info_all[intf] = {}
            if search1:
                admin_status = search1.group(1)
                oper_status = search1.group(2)
            else:
                admin_status = ''
                oper_status = ''
        info_all[intf]['admin-status'] = admin_status
        info_all[intf]['oper-status'] = oper_status
        search_operstatus = re.search(r'up\s*$',
                                      info_all[intf]['oper-status'], re.I)
        if search_operstatus:
            status_all[intf] = {}
            status_all[intf]['oper-status'] = True
        else:
            status_all[intf] = {}
            status_all[intf]['oper-status'] = False
            device.log(level='INFO', message='for the interface '
                       '%s the protocol status is not in up' % intf)
    return status_all


def ping(device, host=None, ipv6=False, source=None, count=None, option=None,
         timeout=None, acceptable_packet_loss=0):
    """ping the host to make sure its reachable
        :param host:
            **REQUIRED** Destination ip to ping
        :param ipv6:
            **OPTION** Ping for IPv6. True for IPv6, False for Ipv4.
            Default: False
        :param count:
            **OPTION** Number of packet to send
        :param option:
            **OPTION** Other options for ping
        :param timeout
            **OPTION** timeout of ping
        :param acceptable_packet_loss
            **OPTION** Number of packets lost that is acceptable to
            consider the test PASS
            default: "0"
        :return: ping_result (dict of ping result)
        Eg:
            ping_result = {'reachable': True, 'round_trip': {'avg': '56',
            'max': '200', 'min': '20'}, 'packets_transmitted': 5,
            'packets_received': 5, 'packet_loss': 0}
    """
    ping_result = {}
    ping_result['reachable'] = False
    device.log(level="DEBUG", message="Entering 'ping'\n" + __file__)
    if not host:
        device.log(level="error", message="host is mandatory\n")
        raise TobyException("'host' is mandatory")
    if ipv6:
        host = "ipv6 %s" % host
    cmd = "ping %s" % host
    if source:
        if re.search(r'erx', device.model, re.I):
            cmd = "%s source address %s" % (cmd, source)
        else:
            cmd = "%s source %s" % (cmd, source)
    if count:
        cmd = "%s repeat %s" % (cmd, count)
    if option:
        cmd = "%s %s" % (cmd, option)
    if timeout:
        cmd = "%s timeout %s" % (cmd, timeout)
    device.log(level='INFO', message='Executing %s' % cmd)
    response = device.cli(command=cmd, timeout=300).response()
    if re.search(r'Unrecognized', response, re.I):
        device.log(level='error',
                   message="Cannot resolve hostname: %s" % host)
    else:
        match = re.search(
            r'round-trip\s+min/avg/max\s+=\s+(\d+)/(\d+)/(\d+)',
            response, re.I)
        if match:
            ping_result['round_trip'] = {}
            ping_result['round_trip']['min'] = match.group(1)
            ping_result['round_trip']['avg'] = match.group(2)
            ping_result['round_trip']['max'] = match.group(3)
            # Ping succeeded
            match = re.search(r'(\d+)\s*(?:percent|%)\s+\((\d+)/(\d+)\)',
                              response, re.MULTILINE)
            packet_loss = 100 - int(match.group(1))
            ping_result['packet_loss'] = packet_loss
            ping_result['packets_received'] = int(match.group(2))
            ping_result['packets_transmitted'] = int(match.group(3))
            if packet_loss <= int(acceptable_packet_loss):
                device.log(level='INFO',
                           message="Success: %s is reachable" % host)
                ping_result['reachable'] = True
            else:
                device.log(level='info',
                           message="Ping output was: %s" % response)
    device.log(level="DEBUG", message="Exiting 'ping' with "
               "return value/code :\n" + str(ping_result))
    return ping_result


def extended_ping(device, host=None, ipv6=False, tos=None, source=None,
                  count=None, timeout=None, pktsize=None, protocol=None,
                  acceptable_packet_loss=0, df=False, validate_reply=False,
                  data_pattern=None, misc=None, sweep=False,
                  sweep_min_size=None, sweep_max_size=None,
                  sweep_interval=None):
    """Extended ping the host to make sure its reachable
        :param host:
            **REQUIRED** Destination ip to ping
        :param ipv6:
            **OPTION** Ping for IPv6. True for IPv6, False for Ipv4.
            Default: False
        :param count:
            **OPTION** Number of packet to send
            default: 5
        :param timeout
            **OPTION** timeout of ping
        :param pktsize
            **OPTION** Datagram size of ping
        :param protocol
            **OPTION** protocol of ping
        :param df
            **OPTION** Set DF bit in IP header? True or False
            Default: False
        :param validate_reply
            **OPTION** Validate reply data? True or False
            Default: False
        :param data_pattern
            **OPTION** Data pattern of ping
        :param misc
            **OPTION** Loose, Strict, Record, Timestamp, Verbose
        :param sweep
            **OPTION** Sweep range of sizes? True or False
            Default: False
        :param sweep_min_size
            **OPTION** Sweep min size
        :param sweep_max_size
            **OPTION** Sweep max size
        :param sweep_interval
            **OPTION** Sweep interval
        :param acceptable_packet_loss
            **OPTION** Number of packets lost that is acceptable to
            consider the test PASS
            default: "0"
        :return: ping_result (dict of ping result)
        Eg:
            ping_result = {'reachable': True, 'round_trip': {'avg': '56',
            'max': '200', 'min': '20'}, 'packets_transmitted': 5,
            'packets_received': 5, 'packet_loss': 0}
    """
    ping_result = {}
    ping_result['reachable'] = False
    device.log(level="DEBUG", message="Entering 'extended_ping'\n" + __file__)
    if not host:
        device.log(level="error", message="host is mandatory\n")
        raise TobyException("'host' is mandatory")
    if ipv6:
        host = "ipv6 %s" % host
    response = device.cli(command='ping', pattern=[r':\s.*', r'%\s.*'],
                          timeout=30).response()
    pattern_list = ['Protocol', 'Target IP address', 'Repeat count',
                    'Datagram size', 'Timeout in seconds']
    command_list = [protocol, host, count, pktsize, timeout]
    i = 0
    for member in pattern_list:
        if re.search(r'%s' % member, response, re.I):
            command = command_list[i]
            if not command:
                command = ""
            response = device.execute(command='%s' % command,
                                      pattern=[r':\s.*', r'%\s.*'],
                                      timeout=15)
        i = i + 1
    extended_pattern_list = ['Source address', 'Type of service',
                             'Set DF bit', 'Validate reply data',
                             'Data pattern', 'Loose, Strict, Record']
    extended_command_list = [source, tos, df, validate_reply, data_pattern,
                             misc]
    if re.search(r'Extended commands', response, re.I):
        if source or tos or df or validate_reply or data_pattern or misc \
                or sweep_min_size:
            command = 'y'
        else:
            command = ''
        response = device.execute(command=command, pattern=[r':\s.*',
                                                            r'%\s.*'],
                                  timeout=15)
        i = 0
        for extended_member in extended_pattern_list:
            if re.search(r'%s' % extended_member, response, re.I):
                extended_command = extended_command_list[i]
                if not extended_command:
                    extended_command = ""
                response = device.execute(command='%s' % extended_command,
                                          pattern=[r':\s.*', r'%\s.*'],
                                          timeout=15)
            i = i + 1
        sweep_pattern_list = ['Sweep min size', 'Sweep max size',
                              'Sweep interval']
        sweep_command_list = [sweep_min_size, sweep_max_size,
                              sweep_interval]
        if re.search(r'Sweep range of sizes', response, re.I):
            if sweep:
                command = 'y'
            else:
                command = ''
            response = device.execute(command=command,
                                      pattern=[r':\s.*', r'%\s.*'], timeout=30)
            i = 0
            for sweep_member in sweep_pattern_list:
                if re.search(r'%s' % sweep_member, response, re.I):
                    sweep_command = sweep_command_list[i]
                    if not sweep_command:
                        sweep_command = ""
                    response = device.execute(command='%s' % sweep_command,
                                              pattern=[r':\s.*', r'%\s.*'],
                                              timeout=15)
                i = i + 1
    if re.search(r'Bad IP address', response, re.I):
        device.log(level='error',
                   message="Cannot resolve hostname: %s" % host)
    else:
        match = re.search(
            r'round-trip\s+min/avg/max\s+=\s+(\d+)/(\d+)/(\d+)',
            response, re.I)
        if match:
            ping_result['round_trip'] = {}
            ping_result['round_trip']['min'] = match.group(1)
            ping_result['round_trip']['avg'] = match.group(2)
            ping_result['round_trip']['max'] = match.group(3)
            # Ping succeeded
            match = re.search(r'(\d+)\s*(?:percent|%)\s+\((\d+)/(\d+)\)',
                              response, re.MULTILINE)
            packet_loss = 100 - int(match.group(1))
            ping_result['packet_loss'] = packet_loss
            ping_result['packets_received'] = int(match.group(2))
            ping_result['packets_transmitted'] = int(match.group(3))
            if packet_loss <= int(acceptable_packet_loss):
                device.log(level='INFO',
                           message="Success: %s is reachable" % host)
                ping_result['reachable'] = True
            else:
                device.log(level='info',
                           message="Ping output was: %s" % response)
    device.log(level="DEBUG", message="Exiting 'ping' with "
               "return value/code :\n" + str(ping_result))
    return ping_result


def traceroute(device, host=None, source=None, timeout=300,
               options=None, ttl=None, noresolve=False):
    """traceroute to the host to make sure its reachable
        :param host
            **REQUIRED** Destination ip to ping
        :param options
            **OPTION** source of traceroute command
        :param timeout
            **OPTION** timeout of traceroute command
        :param options
            **OPTION** option of traceroute command
        :param ttl
            **OPTION** ttl value of traceroute command
        :param noresolve
            **OPTION** Enable no-resolve or not. True/False
        Default: False

        :return: trace_result (dict of traceroute result)
        Eg:
            trace_result = {'reachable': True,
            'hop': ['10.20.15.66', '10.20.20.2']}
    """
    device.log(level="DEBUG", message="Entering 'traceroute'\n" + __file__)
    trace_result = {}
    trace_result['reachable'] = False
    if not host:
        device.log(level="error", message="host is mandatory\n")
        raise TobyException("'host' is mandatory")
    cmd = "traceroute %s" % host
    if source:
        cmd = "%s source %s" % (cmd, source)
    if ttl:
        cmd = "%s ttl %s" % (cmd, ttl)
    if noresolve:
        cmd = "%s no-resolve" % cmd

    dest_re = r'tracing the route to\s+(\S+)(\s+\((\S+)\))?'
    trace_re = r'(\d+)\s+((\S+)\s+)?(\((\S+)\)\s+)?(\[(AS\s+\d+)\]\s+)?' +\
        r'(\[.*\]\s+)?(\*|\d+\s+msec)\s+(\*|\d+\s+msec)\s+(\*|\d+\s+msec)'
    if options:
        cmd = "%s %s" % (cmd, options)
    device.log(level='INFO', message='Executing %s' % cmd)
    response = device.cli(command=cmd, timeout=timeout).response()
    lines = response.split('\n')

    hop = []
    for line in lines:
        match = re.search(dest_re, line, re.I)
        if match:
            if "(" not in line:
                dest = match.group(1)
            else:
                dest = match.group(3)
        match = re.search(trace_re, line, re.I)
        if match:
            if "(" not in line:
                dest_match = match.group(3)
            else:
                dest_match = match.group(5)
            hop.append(dest_match)
            if dest == dest_match:
                device.log(level='INFO',
                           message="Success: %s is reachable" % host)
                trace_result['reachable'] = True
                break
    trace_result['hop'] = hop
    device.log(level="DEBUG", message="Exiting 'traceroute' with "
               "return value/code :\n" + str(trace_result))
    return trace_result
