#!/usr/bin/python3
"""
#=========================================================================
#  DESCRIPTION:  Uses template file and L4_session tool to start/send/check traffic
#       AUTHOR:  Ara Amudhan R
#      COMPANY:  Juniper Networks
#      VERSION:  1.0
#=========================================================================
"""
import re
import yaml


def l4_session_traffic(template_file=None, template=None, session_args=None, traffic_args=None):
    """
    Reads the template file; send and check the the traffic as per the template
    Example:
        l4_sesssion_traffic()
        l4 session traffic   template_file=/homes/ara/PycharmProjects/testsuites/idp/L4_Traffic.yaml
        ...                   template=${template}    session_args=${session_args}

    :param str template_file:
        *Mandatory* Name of the template file with full path
    :param str template:
        *Mandatory* Name of the template in the template file to be used for the traffic
    :param dict session_args:
        *Mandatory* L4 Session related data to open the client/server and send data
    :param dict traffic_args:
        *OPTIONAL*
    :return: Returns True if executed Successfully
    :rtype: bool
    """
    with open(template_file) as trafficfile:
        templatefile = yaml.load(trafficfile)
    if 'ARGS' in templatefile[template]:
        traffic_args = _traffic_args(templatefile[template]['ARGS'], traffic_args)
    traffic_seq = _parse_update_traffic(templatefile[template]['TRAFFIC'], traffic_args)
    _send_traffic(traffic_seq, session_args)
    return True


def _replace(args=None, data=None):
    arg_reg = r"(var\[\\*'([-\w]+)\\*'\])"
    matches = re.findall(arg_reg, data)
    for match in matches:
        data = data.replace(match[0], args[match[1]])
    return data


def _traffic_args(template_args=None, traffic_args=None):
    updated_args = {}
    for args in template_args:
        updated_args.update(args)
# Update the template args with the passed traffic_args
    updated_args.update(traffic_args)
    return updated_args


def _parse_update_traffic(traffic_list=None, args=None):
    device_knobs = ('client', 'server')
    action_knobs = ('start', 'close', 'send', 'send_hex', 'check')
    traffic_seq = []
    for traffic in traffic_list:
        for device in traffic:
            if device not in device_knobs:
                raise Exception(device + ": Not in " + str(device_knobs))
            if traffic[device][0] not in action_knobs:
                raise Exception(traffic[device][0] + ": Not in " + str(action_knobs))
            action_items = [device, traffic[device][0]]
            action_items.append(_replace(args, str(traffic[device][1])))
            if len(traffic[device]) > 1:
                action_items = action_items + traffic[device][2:]
            traffic_seq.append(action_items)
    return traffic_seq


def _qq(word):
    temp = '"'  # double quote
    return temp + word + temp


def _other(device):
    if device == 'client':
        return 'server'
    if device == 'server':
        return 'client'


def _send_traffic(traffic_list=None, args=None):
    device = {}
    device['server'] = args.get('server', None)
    device['client'] = args.get('client', None)
    server_ip = args.get('server_ip', None)
    client_ip = args.get('client_ip', None)
    protocol = args.get('protocol', 'TCP')
    server_port = args.get('server_port', 0)
    if not isinstance(server_port, int):
        server_port = int(server_port)
    client_port = args.get('client_port', 0)
    if not isinstance(client_port, int):
        client_port = int(client_port)
    ipv6 = args.get('ipv6', False)

    for item in traffic_list:
        if item[1] == 'start':
            sessid = 0
            if item[0] == 'server' and item[2] == 'True':
                device[item[0]].dh.log(level='debug', message='Starting the Server')
                sessid = device[item[0]].start(mode=item[0], server_ip=server_ip, protocol=protocol,
                                               server_port=server_port)
                device[item[0]].pktSent = 0
            elif item[0] == 'client' and item[2] == 'True':
                device[item[0]].dh.log(level='debug', message='Starting the Client')
                sessid = device[item[0]].start(mode=item[0], server_ip=server_ip, protocol=protocol,
                                               server_port=server_port, client_port=client_port,
                                               client_ip=client_ip)
                device[item[0]].pktSent = 0
            if sessid == 0:
                raise Exception("Server/Client failed to start")
        elif item[1] == 'close':
            device[item[0]].dh.log(level='debug', message='Closing the Connection')
            device[item[0]].close(ipv6=ipv6)
        elif item[1] == 'send':
            device[item[0]].dh.log(level='debug', message='Sending data from %s (packet: %d)'
                                   % (item[0], device[item[0]].pktSent + 1))
            device[item[0]].send_data(data=_qq(item[2]), ipv6=ipv6)
        elif item[1] == 'send_hex':
            device[item[0]].dh.log(level='debug', message='Sending HEX data from %s (packet: %d)'
                                   % (item[0], device[item[0]].pktSent + 1))
            device[item[0]].send_data(data=item[2], hex_format=True, ipv6=ipv6)
        elif item[1] == 'check' and item[2] in ('presence', 'absence'):
            device[item[0]].dh.log(level='debug',
                                   message="Check l4_session %s on %s" % (item[2], item[0]))
            device[item[0]].check_status(state=item[2])
        elif item[1] == 'check' and item[2] in ('dropped', 'received'):
            other = _other(item[0])
            device[item[0]].dh.log(level='debug', message="Check last packet (%d) sent is %s on %s"
                                   % (device[other].pktSent, item[2], item[0]))
            device[item[0]].check_data_received(state=item[2], pktrec=device[other].pktSent)
    return True
