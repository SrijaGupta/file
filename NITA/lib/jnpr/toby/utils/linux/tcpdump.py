"""
TCPdump utilities
"""
import re



def stop_tcpdump(device=None, pid=0):
    """
    To stop tcpdump by passing PID on the Linux PC/JunOS device. By default, all the tcpdump processes on
    the PC will be killed.
    Example:
        stop_tcpdump(device=dh)
        stop_tcpdump(device=dh, pid=25177)

    ROBOT Example:
        Stop Tcpdump    device=${dh}    pid=100

    :param device:
        **REQUIRED** The device handle of linux PC/JunOS device.
    :param int pid:
        *OPTIONAL* Process ID of the tcpdump to kill. By default, the routine kills all the
        tcpdump processes.
    """
    if device is None:
        raise Exception("device is a mandatory argument")
    if pid != 0:
        device.shell(command="kill -9 " + str(pid))
    else:
        device.shell(command="killall -9 tcpdump")


def check_pcap(
        device=None,
        protocol="tcp",
        state="presence",
        string="",
        pcap_name="/tmp/test.pcap",
        delete_pcap="no",
        **kwargs):
    """
    To check the existence of some string, source/ destination port and specific protocol in a
    given pcap file.
    Example:
        check_pcap(string="Frame", pcap_name="/tmp/kali_frag_route.pcap", dport=80,
                   times=1047, protocol="tcp", device=dh)
        check_pcap(string="Frame", pcap_name="/tmp/kali_frag_route.pcap", dport=80,
                   sport=48504, times=1047, protocol="tcp", device=dh)
        check_pcap(string="Frame", pcap_name="/tmp/kali_frag_route.pcap", times=104,
                   protocol="tcp", device=dh)
        check_pcap(string="Framewsdfs", pcap_name="/tmp/kali_frag_route.pcap", dport=80,
                   times=1047, protocol="tcp", state="absence", device=dh)
        check_pcap(string="Frame", pcap_name="/tmp/kali_frag_route.pcap", times=1047,
                   src_v4="4.0.0.1", dst_v4="5.0.0.1", protocol="tcp", device=dh)
        check_pcap(string="Frame", pcap_name="/tmp/kali_frag_route.pcap", times=1047,
                   src_v6="4::1", dst_v6="3::1",dport=80, protocol="tcp", delete_pcap="yes",
                   device=dh)

    ROBOT Example:
        Check Pcap    device=${dh}   string=Frame100   dport=${80}   state=absence

    :param device:
        **REQUIRED** The device handle of linux PC/JunOS device.
    :param str string:
        **REQUIRED** The string whose existence to look for in the pcap
    :param str pcap_name:
        *OPTIONAL* Name of the pcap file to be checked. Default path is"/tmp/test.pcap"
    :param int times:
        *OPTIONAL* Check for No. of times string found
    :param int sport:
        *OPTIONAL* Source port to be filtered
    :param int dport:
        *OPTIONAL* Destination port to be filtered
    :param str src_v4:
        *OPTIONAL* IPv4 Source Address to be filtered
    :param str dst_v4:
        *OPTIONAL* IPv4 Destination Address to be filtered
    :param str src_v6:
        *OPTIONAL* IPv6 Source Address to be filtered
    :param str dst_v6:
        *OPTIONAL* IPv6 Destination Address
    :param str protocol:
        *OPTIONAL* Protocol to be checked. Default value is "tcp"
    :param str state:
        *OPTIONAL* Depends on what what you want to check : presence or absence of the string.
        Default value is 'presence'. Supported values are 'absence' and 'presence'
    :param str delete_pcap:
        *OPTIONAL* Defines if you want to delete the pcap after checking in the end. Default
        value is 'no'. Supported values are 'yes' and 'no'
    :param int tcp_port:
        *OPTIONAL* TCP port number (used with -d option)
    :param str proto:
        *OPTIONAL* Protocol name (used with -d option, Mandatory when 'tcp_port' is passed)
    :return: returns TRUE or FALSE
    :rtype: bool
    """

    times = kwargs.get('times', -1)
    sport = kwargs.get('sport', 0)
    dport = kwargs.get('dport', 0)
    src_v4 = kwargs.get('src_v4', "")
    dst_v4 = kwargs.get('dst_v4', "")
    src_v6 = kwargs.get('src_v6', "")
    dst_v6 = kwargs.get('dst_v6', "")
    tcp_port = kwargs.get('tcp_port', 0)
    proto = kwargs.get('proto', "")

    if string == "" or device is None:
        raise ValueError(
            "Mandatory arguments: string and device have to be passed")

    # Creating command based on different arguments passed
    cmd = "tethereal -Vx "
    filter_cmd = ""
    flag = 0
    connector = ""

    # Creating filter command based on src_port, dest_port, src_ip and
    # dst_ip (v4 an v6)
    if sport:
        filter_cmd = filter_cmd + protocol + ".srcport == " + str(sport)
        flag = 1
    if dport:
        if flag:
            connector = " and "
        filter_cmd = filter_cmd + connector + \
                     protocol + ".dstport == " + str(dport)
        flag = 1
    if src_v4:
        if flag:
            connector = " and "
        filter_cmd = filter_cmd + connector + "ip.src == " + src_v4
        flag = 1
    if dst_v4:
        if flag:
            connector = " and "
        filter_cmd = filter_cmd + connector + "ip.dst == " + dst_v4
        flag = 1
    if src_v6:
        if flag:
            connector = " and "
        filter_cmd = filter_cmd + connector + "ipv6.src == " + src_v6
        flag = 1
    if dst_v6:
        if flag:
            connector = " and "
        filter_cmd = filter_cmd + connector + "ipv6.dst == " + dst_v6

    if filter_cmd:
        cmd = cmd + '-R "' + filter_cmd + '" '

    if tcp_port:
        if not proto:
            device.log(level="ERROR", message="'proto' is mandatory if 'tcp_port' is passed")
            raise Exception("'proto' is mandatory if 'tcp_port' is passed")
        cmd = cmd + ' -d tcp.port==' + str(tcp_port) + ',' + proto

    cmd = cmd + " -r " + pcap_name
    # Printing the whole pcap once
    device.shell(command=cmd)

    cmd = cmd + " > /tmp/check-pcap.txt"
    device.shell(command="rm -rf /tmp/check-pcap.txt")
    device.shell(command=cmd)

    if delete_pcap == "yes":
        device.shell(command="rm -rf " + pcap_name)

    response_obj = device.shell(
        command='cat /tmp/check-pcap.txt | grep ' + "'" + string + "'" + '| wc -l')
    response = response_obj.response()

    device.shell(command="rm -rf /tmp/check-pcap.txt")

    # Checking for absence or presence of the string
    if state == "presence":
        if times != -1:
            if int(response) == times:
                device.log(level="INFO", message="String is found " + response +
                                 " times in PCAP")
                return True
            else:
                device.log(level="ERROR", message="String is found " + response +
                                 " times in PCAP")
                raise Exception("String is found " + response + " times in PCAP")
        else:
            if int(response) >= 1:
                device.log(level="INFO", message="String is found " + response +
                                 " times in PCAP")
                return True
            else:
                device.log(level="ERROR", message="String is found " + response +
                                 " times in PCAP")
                raise Exception("String is found " + response + " times in PCAP")
    else:
        if int(response) >= 1:
            device.log(level="ERROR", message="String is found " + response +
                             " times in PCAP")
            raise Exception("String is found " + response + " times in PCAP")
        else:
            device.log(level="INFO", message="String is found " + response + " times in PCAP")
            return True


def start_tcpdump(
        device=None,
        pcapfile="/tmp/test.pcap",
        interface="",
        negate_port="",
        src="",
        dst="",
        ip_mode="",
        **kwargs):
    """
    To start tcpdump on the specified Unix PC
    Example:
        start_tcpdump(interface="eth1", device=dh)
        start_tcpdump(interface="eth1", pcapfile="/tmp/test_pcap.pcap", device=dh)
        start_tcpdump(interface="eth1", pcapfile="/tmp/2.pcap", port=1000, device=dh
                      negate_port="yes", dst="4.0.0.1", src="5.0.0.1", ip_mode = "ipv4")
        start_tcpdump(interface="eth1", pcapfile="/tmp/2.pcap", dst="4.0.0.1",
                      src="6.0.0.1", device=dh)
        start_tcpdump(interface="eth1", pcapfile="/tmp/2.pcap", port=100,
                      ip_mode="ipv6", device=dh)
        start_tcpdump(interface="eth1", pcapfile="/tmp/2.pcap", dst="4::1", src="3::1",
                      device=dh)

    ROBOT Example:
        Start Tcpdump   device=${dh}   interface=eth1   port=${80}

    :param device:
        **REQUIRED** The device handle of linux PC/JunOS device.
    :param str interface:
        **REQUIRED** Name of the interface on which tcpdump has to be started
    :param str pcapfile:
        *OPTIONAL* Path of the desired pcap file. Default path is "/tmp/idptest.pcap"
    :param int port:
        *OPTIONAL* Specific port no. where tcpdump has to be started.
    :param str negate_port:
        *OPTIONAL* TO negate the port no. option. i.e. except that port, apply tcpdump on every
        other port. Default is 'no'. Argument is only valid if port is defined. Supported
        values are 'yes' and 'no'
    :param str src:
        *OPTIONAL* To specify source address filter on tcpdump. Source Address (IPv4 or IPv6)
        needs to be given.
    :param str ip_mode:
        *OPTIONAL* To specify ipv4 or ipv6 filter or both on tcpdump. Supported values are :
            ipv4
            ipv6
            both
            Default value is 'both'
    :param str dst:
        *OPTIOMAL* To specify destination address filter on tcpdump/ Destination Address
                  (IPv4 or IPv6) needs to be given.
    :return: returns the pid (integer) of the tcpdump process.
    :rtype: int
    """

    if interface == "" or device is None:
        raise ValueError("Mandatory argument-'interface' and 'device' has to be passed")

    shelltype = device.shell(command="echo $0")
    device.shell(command="rm -rf %s" % pcapfile)
    port = kwargs.get('port', 0)

    if "csh" in shelltype.response():
        cmd = "(tcpdump -i" + interface + " -w" + pcapfile
    else:
        cmd = "tcpdump -i " + interface + " -s 0 -w " + pcapfile

    if ip_mode == "ipv4":
        cmd = cmd + " ip and "
    elif ip_mode == "ipv6":
        cmd = cmd + " ip6 and "
    else:
        cmd = cmd + " ip or ip6 and "

    # If port is not mentioned, default is not port 514, because port 514 is for syslog.
    # No need to monitor that in most of the cases.
    if port == 0:
        cmd = cmd + "not port 514"
    else:
        if negate_port == "yes":
            cmd = cmd + "not port " + str(port)
        else:
            cmd = cmd + "port " + str(port)

    # If source and destination filters are passed as arguments
    if src != "":
        cmd = cmd + " and src host " + src
    if dst != "":
        cmd = cmd + " and dst host " + dst
    if "csh" in shelltype.response():
        cmd = cmd + "> /dev/null) >& /tmp/start_tcpdump.txt &\n"
    else:
        cmd = cmd + " -U 2> /tmp/start_tcpdump.txt 1> /dev/null &\n"
    response1 = device.shell(command=cmd)
    response2 = device.shell(command="cat /tmp/start_tcpdump.txt")

    pid = ""
    if re.match(".*istening.*", response2.response(), re.DOTALL):
        device.log(level="INFO", message="Tcpdump started successfully")
        match = re.search("\\[[0-9]\\]\\s+(\\d+)", response1.response(), re.DOTALL)
        pid = match.group(1)

    else:
        device.log(level="ERROR", message="Tcpdump could not be started")

    device.shell(command="rm -rf /tmp/start_tcpdump.txt")
    if pid:
        return int(pid)
    raise Exception("Tcpdump could not be started")
