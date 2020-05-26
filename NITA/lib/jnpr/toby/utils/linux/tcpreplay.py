#! /usr/local/bin/python3

"""
        FILE:   tcpreplay.py
 DESCRIPTION:   Replaying pcap both in l2 and l3 mode.
                To replay, tcpprep and tcpreplay-edit should be installed in the linux host.
     COMPANY:   Juniper Networks
"""
from jnpr.toby.utils.linux.linux_network_config import get_linux_int_mac 


def tcpreplay_l2mode(device=None, pcap_file=None, **kwargs):
    """
    Replaying pcap in l2 mode.
    tcpprep and tcpreplay-edit should be installed in the linux host.
    Example:
        tcpreplay_l2mode(device=unix1, pcap_file="/tmp/tcp_res_111.cap")
        tcpreplay_l2mode(device=unix1, pcap_file="/tmp/tcp_res_111.cap",  client_interface="eth1",
        server_interface="eth2")
        tcpreplay_l2mode(device=unix1, pcap_file="/tmp/tcp_res_111.cap",  client_interface="eth1",
        server_interface="eth2", pps="2")
        tcpreplay_l2mode(device=unix1, pcap_file="/tmp/tcp_res_111.cap",  client_interface="eth1",
        server_interface="eth2", mbps="10")
        tcpreplay_l2mode(device=unix1, pcap_file="/tmp/tcp_res_111.cap",  client_interface="eth1",
        server_interface="eth2", topspeed=yes)

    Robot Example:
        tcpreplay l2mode  device=${linux}  client_interface=eth1  server_interface=eth2
        pcap_file=/tmp/tcp_res_111.cap
        tcpreplay l2mode  device=${linux}  client_interface=eth1  server_interface=eth2
        pcap_file=/tmp/tcp_res_111.cap  pps=2
        tcpreplay l2mode  device=${linux}  client_interface=eth1  server_interface=eth2
        pcap_file=/tmp/tcp_res_111.cap  mbps=3
        tcpreplay l2mode  device=${linux}  client_interface=eth1  server_interface=eth2
        pcap_file=/tmp/tcp_res_111.cap  topspeed=yes

    :param Device device:
        **REQUIRED** Handle for linux host.
    :param str pcap_file:
        **REQUIRED** PCAP File to be replayed
    :param str client_interface:
        *OPTIONAL* Linux client interface to replay the pcap
        ``Default Value``: eth1
    :param str server_interface:
        *OPTIONAL* Linux server interface to replay the pcap
        ``Default Value``: eth2
    :param str multiplier:
        *OPTIONAL* Modify replay speed to a given multiple
    :param str pps:
        *OPTIONAL* Packets per second.
    :param str mbps:
        *OPTIONAL* Replay packets at a given Mbps
    :param str topspeed:
        *OPTIONAL* Replay packets as fast as possible
    :return: None
    """
    if device is None:
        raise Exception("linux handle is the mandatory argument")
    if pcap_file is None:
        device.log(
            level="ERROR",
            message="pcap_file is a mandatory argument for this keyword")
        raise Exception("pcap_file is a mandatory argument")

    client_interface = kwargs.get('client_interface', "eth1")
    server_interface = kwargs.get('server_interface', "eth2")
    multiplier = kwargs.get('multiplier', None)
    pps = kwargs.get('pps', None)
    mbps = kwargs.get('mbps', None)
    topspeed = kwargs.get('topspeed', None)

    client_mac = get_linux_int_mac(device=device, interface=client_interface)
    server_mac = get_linux_int_mac(device=device, interface=server_interface)

    cmd = "tcpreplay-edit -i %s " % (client_interface)
    if multiplier is not None:
        if pps is not None or mbps is not None or topspeed is not None:
            device.log(
                level="ERROR",
                message="Only one argument can be passed out of multiplier, pps, mbps and topspeed")
            raise Exception(
                "Only one argument can be passed out of multiplier, pps, mbps and topspeed")
        else:
            cmd = cmd + '--multiplier=' + multiplier
    elif pps is not None:
        if mbps is not None or topspeed is not None:
            device.log(
                level="ERROR",
                message="Only one argument can be passed out of multiplier, pps, mbps and topspeed")
            raise Exception(
                "Only one argument can be passed out of multiplier, pps, mbps and topspeed")
        else:
            cmd = cmd + '-p ' + pps
    elif mbps is not None:
        if topspeed is not None:
            device.log(
                level="ERROR",
                message="Only one argument can be passed out of multiplier, pps, mbps and topspeed")
            raise Exception(
                "Only one argument can be passed out of multiplier, pps, mbps and topspeed")
        else:
            cmd = cmd + '-M ' + mbps
    elif topspeed is not None:
        cmd = cmd + '-t'

    cmd = cmd + \
        ' --enet-smac=\"%s\" --enet-dmac=\"%s\" \"%s\"' % (server_mac, client_mac, pcap_file)
    cmd = cmd.replace('\r',"")
    resp = device.shell(command=cmd)
    return resp.response()


def tcpreplay_l3mode(device=None, pcap_file=None, **kwargs):
    """
    Replaying pcap in L3 mode.
    tcpprep and tcpreplay-edit should be installed in the linux host.
    Example:
        tcpreplay_l3mode(device=unix1, pcap_file="/tmp/tcp_res_111.cap"
        split_ip="192.168.158.139", device_ingress_mac="44:f4:77:92:58:b7",
        device_egress_mac="44:f4:77:92:58:b9", client_ip="4.0.0.1", server_ip="3.0.0.1")
        tcpreplay_l3mode(device=unix1, pcap_file="/tmp/tcp_res_111.cap",
        split_ip="192.168.158.139", device_ingress_mac="44:f4:77:92:58:b7",
        device_egress_mac="44:f4:77:92:58:b9", client_ip="4.0.0.1", server_ip="3.0.0.1",
        portmap=8080:80)
        tcpreplay_l3mode(device=unix1, pcap_file="/tmp/tcp_res_111.cap",
        split_ip="192.168.158.139", device_ingress_mac="44:f4:77:92:58:b7",
        device_egress_mac="44:f4:77:92:58:b9", client_ip="4.0.0.1", server_ip="3.0.0.1", pps="2")
        tcpreplay_l3mode(device=unix1, pcap_file="/tmp/tcp_res_111.cap",
        split_ip="192.168.158.139", device_ingress_mac="44:f4:77:92:58:b7",
        device_egress_mac="44:f4:77:92:58:b9", client_ip="4.0.0.1", server_ip="3.0.0.1",
        timer="nano")
        tcpreplay_l3mode(device=unix1, pcap_file="/tmp/T3_TELNET.pcap",
        split_ip="2001:1000:1111:2222:3333:4444:5555:6666",
        device_ingress_mac="44:f4:77:92:58:b7", device_egress_mac="44:f4:77:92:58:b9",
        client_ip="2001:1000:1111:2222:3333:4444:5555:6666", server_ip="2007::1", ipproto="ipv6")
        tcpreplay_l3mode(device=unix1, pcap_file="/tmp/T3_TELNET.pcap",
        split_ip="2001:1000:1111:2222:3333:4444:5555:6666",
        device_ingress_mac="44:f4:77:92:58:b7", device_egress_mac="44:f4:77:92:58:b9",
        client_ip="2001:1000:1111:2222:3333:4444:5555:6666", server_ip="2007::1", ipproto="ipv6",
        pps="2")
        tcpreplay_l3mode(device=unix1, pcap_file="/tmp/T3_TELNET.pcap",
        split_ip="2001:1000:1111:2222:3333:4444:5555:6666",
        device_ingress_mac="44:f4:77:92:58:b7", device_egress_mac="44:f4:77:92:58:b9",
        client_ip="2001:1000:1111:2222:3333:4444:5555:6666", server_ip="2007::1", ipproto="ipv6",
        pps="2", timer="nano")

    Robot Example:
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/tcp_res_111.cap
        split_ip=192.168.158.139  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=4.0.0.1  server_ip=3.0.0.1
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/tcp_res_111.cap
        split_ip=192.168.158.139  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=4.0.0.1  server_ip=3.0.0.1 portmap=8080:80
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/tcp_res_111.cap
        split_ip=192.168.158.139  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=4.0.0.1  server_ip=3.0.0.1 pps=2
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/tcp_res_111.cap
        split_ip=192.168.158.139  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=4.0.0.1  server_ip=3.0.0.1 mbps=3
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/tcp_res_111.cap
        split_ip=192.168.158.139  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=4.0.0.1  server_ip=3.0.0.1 topspeed=yes
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/tcp_res_111.cap
        split_ip=192.168.158.139  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=4.0.0.1  server_ip=3.0.0.1 pps=2 timer=nano
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/T3_TELNET.pcap
        split_ip=2001:1000:1111:2222:3333:4444:5555:6666  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=2007::1
        server_ip=2001:1000:1111:2222:3333:4444:5555:6666 ipproto=ipv6
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/T3_TELNET.pcap
        split_ip=2001:1000:1111:2222:3333:4444:5555:6666  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=2007::1
        server_ip=2001:1000:1111:2222:3333:4444:5555:6666 ipproto=ipv6 pps=2
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/T3_TELNET.pcap
        split_ip=2001:1000:1111:2222:3333:4444:5555:6666  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=2007::1
        server_ip=2001:1000:1111:2222:3333:4444:5555:6666 ipproto=ipv6 mbps=3
        tcpreplay l2mode  device=${linux}  pcap_file=/tmp/T3_TELNET.pcap
        split_ip=2001:1000:1111:2222:3333:4444:5555:6666  device_ingress_mac=44:f4:77:92:58:b7
        device_egress_mac=44:f4:77:92:58:b9  client_ip=2007::1
        server_ip=2001:1000:1111:2222:3333:4444:5555:6666 ipproto=ipv6 pps=2 timer=nano

    :param Device device:
        **REQUIRED** Handle for linux host
    :param str pcap_file:
        **REQUIRED** pcap file to be replayed.
    :param str client_interface:
        *OPTIONAL* Client interface to replay the pcap file.
        ``Default Value``: eth1
    :param str server_interface:
        *OPTIONAL* Server interface to replay the pcap file.
        ``Default Value``: eth2
    :param str split_ip:
        **REQUIRED** Split the packet according to this IP.
    :param str client_ip:
        **REQUIRED** Linux client IP.
    :param str server_ip:
        **REQUIRED** Linux Server IP.
    :param str device_ingress_mac:
        **REQUIRED** Device client side mac.
    :param str device_egress_mac:
        **REQUIRED** Device server side mac.
    :param str pps:
        *OPTIONAL* Packets per second.
    :param str mbps:
        *OPTIONAL* Replay packets at a given Mbps
    :param str topspeed:
        *OPTIONAL* Replay packets as fast as possible
    :param str ippproto:
        *OPTIONAL* Tells the IP protocol used.
        ``Default Value``: ipv4
        ``supported Value``: ipv4 and ipv6
    :param str timer:
        *OPTIONAL* packet timing mode.
        ``Supported Value``: gtod, rdtsc, nano
    :param str portmap:
        *OPTIONAL* Rewrite TCP/UDP ports
    :return: None
    """
    if device is None:
        raise Exception("linux handle is the mandatory argument")
    if pcap_file is None:
        device.log(
            level="ERROR",
            message="pcap_file is a mandatory argument for this keyword")
        raise Exception("To replay pcap, pcap file name is mandatory")

    client_interface = kwargs.get('client_interface', "eth1")
    server_interface = kwargs.get('server_interface', "eth2")
    split_ip = kwargs.get('split_ip', None)
    client_ip = kwargs.get('client_ip', None)
    server_ip = kwargs.get('server_ip', None)
    device_ingress_mac = kwargs.get('device_ingress_mac', None)
    device_egress_mac = kwargs.get('device_egress_mac', None)
    multiplier = kwargs.get('multiplier', None)
    pps = kwargs.get('pps', None)
    mbps = kwargs.get('mbps', None)
    topspeed = kwargs.get('topspeed', None)
    ipproto = kwargs.get('ipproto', "ipv4")
    timer = kwargs.get('timer', None)
    portmap = kwargs.get('portmap', None)

    if client_ip is None or server_ip is None or split_ip is None:
        device.log(
            level="ERROR",
            message="Mandatory arguments are client_ip, server_ip and split_ip")
        raise Exception(
            "Mandatory arguments are client_ip, server_ip and split_ip")
    if device_ingress_mac is None or device_egress_mac is None:
        device.log(
            level="ERROR",
            message="Mandatory arguments are device_ingress_mac and device_egress_mac")
        raise Exception(
            "Mandatory arguments are device_ingress_mac and device_egress_mac")

    client_mac = get_linux_int_mac(device=device, interface=client_interface)
    server_mac = get_linux_int_mac(device=device, interface=server_interface)

    if ipproto == "ipv6":
        split_ip = "[" + split_ip + "]"
        client_ip = "[" + client_ip + "]"
        server_ip = "[" + server_ip + "]"
        device.shell(
            command="ip6tables -A OUTPUT -p icmpv6 --icmpv6-type port-unreachable -j DROP")
        device.shell(command="ip6tables -A OUTPUT -p tcp --tcp-flags ALL RST -j DROP")
    else:
        device.shell(
            command="iptables -A OUTPUT -p icmp --icmp-type port-unreachable -j DROP")
        device.shell(command="iptables -A OUTPUT -p tcp --tcp-flags ALL RST -j DROP")

    cmd = 'tcpreplay-edit -i %s -I %s --enet-dmac="%s,%s" --enet-smac="%s,%s" -e "%s:%s" ' % (
        client_interface, server_interface, device_ingress_mac, device_egress_mac, client_mac, server_mac,
        client_ip, server_ip)

    if portmap is not None:
        cmd = cmd + '--portmap=' + portmap + ' '

    if multiplier is not None:
        if pps is not None or mbps is not None or topspeed is not None:
            device.log(
                level="ERROR",
                message="Only one argument can be passed out of multiplier, pps, mbps and topspeed")
            raise Exception(
                "Only one argument can be passed out of multiplier, pps, mbps and topspeed")
        else:
            cmd = cmd + '--multiplier=' + multiplier
    elif pps is not None:
        if mbps is not None or topspeed is not None:
            device.log(
                level="ERROR",
                message="Only one argument can be passed out of multiplier, pps, mbps and topspeed")
            raise Exception(
                "Only one argument can be passed out of multiplier, pps, mbps and topspeed")
        else:
            cmd = cmd + '-p ' + pps
    elif mbps is not None:
        if topspeed is not None:
            device.log(
                level="ERROR",
                message="Only one argument can be passed out of multiplier, pps, mbps and topspeed")
            raise Exception(
                "Only one argument can be passed out of multiplier, pps, mbps and topspeed")
        else:
            cmd = cmd + '-M ' + mbps
    elif topspeed is not None:
        cmd = cmd + '-t'

    if timer is not None:
        cmd = cmd + ' --timer=' + timer

    cmd1 = 'tcpprep --cachefile=/tmp/input.cache  -i %s -c %s' % (pcap_file, split_ip)
    cmd2 = cmd + ' -c /tmp/input.cache %s' % (pcap_file)
    cmd2 = cmd2.replace('\r',"")
    device.shell(command=cmd1)
    resp = device.shell(command=cmd2)

    if ipproto == 'ipv6':
        device.shell(command="ip6tables -F")
    else:
        device.shell(command="iptables -F")
    return resp.response()
