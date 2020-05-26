"""
Linux Network Configuration keywords
"""

import re
import ipaddress
from jnpr.toby.utils.iputils import strip_mask as iputils_strip_mask

def get_ip_address_type(address):
    """
    To get the ip address family
    """
    addr = ipaddress.ip_address(str(address))
    ip_version = addr.version
    if "6" in str(ip_version):
        return "ipv6"
    elif "4" in str(ip_version):
        return "ipv4"


def restart_network_service(device=None):
    """
     To restart network service in Linux host
     Example:
       restart_network_service(device=linux)
     Robot Example
       restart network service  device=linux

     :param str device:
         **REQUIRED** Device handle for the Linux host
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    # Checking for mandatory arguments
    if device is None:
        raise ValueError("device is mandatory argument")

    response = device.shell(command="service network restart")
    match = re.search('Bringing up' + '.*' + 'FAILED', response.response())
    if match:
        device.log(level='ERROR', message="Network service restart Failed ")
        raise Exception("Network service restart Failed")
    return True

def configure_ip_address(device=None, interface=None, address=None, mask=None):
    """
     To configure IPv4/IPv6 address on Linux
     Example:
       configure_ip_address(device=linux, interface="eth2", address="2008::1", mask="64")
       configure_ip_address(device=linux, interface="eth1", address="4.0.0.1",
                            mask="255.0.0.0")
     Robot Example:
       configure ip address  device=$(linux)  interface="eth2"  address="2008::1"  mask="64"
       configure ip address  device=$(linux)  interface="eth1"  address="4.0.0.1"
                             mask="255.0.0.0"
     :param str device:
         **REQUIRED** Device handle for the Linux host
     :param str interface:
         **REQUIRED** Interface name to configure ip address
     :param str addr:
         **REQUIRED** IPv4/IPv6 Address to be configured
     :param str mask:
         **REQUIRED** Address mask to be configured.
              For IPv4 address, it should be 4 octets number such as "255.255.0.0"
              For IPv6 address, mask would be prefix as 64,128 etc.
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    # Checking for mandatory arguments
    if device is None:
        raise ValueError("device is mandatory argument")
    if interface is None or address is None:
        device.log(level='ERROR',
                   message="Interface and IPv4/IPv6 address are mandatory argument")
        raise ValueError("Interface and IPv4/IPv6 address are mandatory argument")

    # getting the ip address type and based on that start configuration
    ip_type = get_ip_address_type(iputils_strip_mask(address))
    if ip_type == "ipv6":
        cmd = "ifconfig %s inet6 add %s" % (interface, address)
        if mask is not None:
            cmd = cmd + "/" + mask
    else:
        cmd = "ifconfig %s %s" % (interface, address)
        if mask is not None:
            cmd = cmd + ' ' + "netmask " + mask
    device.log("Running: " + cmd)
    response = device.shell(command=cmd).response()
    device.log("Response: " + response)
    response = device.shell(command="ifconfig %s" % (interface))
    if ip_type == "ipv6":
        match = re.search('.*inet6' + '.*' + iputils_strip_mask(address) + '.*', response.response())
    else:
        match = re.search('.*inet' + '.*' + iputils_strip_mask(address) + '.*', response.response())
    # Verify if ip address configured properly
    if match:
        device.log(level='INFO', message="%s address is configured successfully" % (ip_type))
        return True
    else:
        device.log(level='ERROR', message="%s address is not configured successfully"
                   % (ip_type))
        raise Exception("IPv4/IPv6 address is not configured successfully")


def add_route(device=None, network=None, netmask=None, gateway=None, **kwargs):
    """
    To add ip/ipv6 route to the linux host
    Example:
      add_route(device=linux, network="3.0.0.0", netmask="255.0.0.0", gateway="4.0.0.1",
                interface="eth1")
      add_route(device=linux, host="1.2.3.4", gateway="4.0.0.1")
      add_route(device=linux, default_gateway="4.0.0.254")
      add_route(device=linux, network="2007::", netmask="64", gateway="2001::254",
                interface="eth1")
      add_route(device=linux, host="2007::1", gateway="2001::254")
      add_route(device=linux,default_gateway="2001::254")
    Robot Example:
      add route  device=$(linux)  network="3.0.0.0"  netmask="255.0.0.0"  gateway="4.0.0.1"
                                         interface="eth1"
      add route  device=$(linux)  host="1.2.3.4"  gateway="4.0.0.1"
      add route  device=$(linux)  default_gateway="4.0.0.254"
      add route  device=$(linux)  network="2007::"  netmask="64"  gateway="2001::254"
                                         interface="eth1"
      add route  device=$(linux)  host=""2007::1"  gateway="2001::254"
      add route  device=$(linux)  default_gateway="2001::254"

     :param str device:
         **REQUIRED** Device handle for Linux host
     :param str network:
         *OPTIONAL* IPv4/IPv6 network address, not applicable with host/default_gateway
     :param str netmask:
         *OPTIONAL* Address mask to be configured. Mandatory with network configuration
              For IPv4 address, it should be 4 octets number such as "255.255.0.0"
              For IPv6 address, mask would be prefix as 64,128 etc.
     :param str gateway:
         *OPTIONAL* Gateway address of network. Mandatory with network configuration
     :param str default_gateway:
         *OPTIONAL* Default gateway address. network, netmask, gateway and host are ignored
                    when default_gateway configured
     :param str host:
         *OPTIONAL* Host ip address route configuration. gateway is mandatory argument with
                    host. network and netmask are ignored.
     :param str interface:
         *OPTIONAL* Interface name to reach the next hop
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device argument is mandatory")

    # Configure default gw and ignore other configuration options
    if 'default_gateway' in kwargs:
        default_gateway = kwargs.get('default_gateway')
        ip_type = get_ip_address_type(default_gateway)
        if ip_type == "ipv6":
            cmd = "route -A inet6 add default gateway %s" % (default_gateway)
        else:
            cmd = "route add default gateway %s" % (default_gateway)
    # Configure host based route. Gateway is mandatory
    elif 'host' in kwargs:
        if gateway is None:
            device.log(level='ERROR',
                       message="Gateway address is required for host based route")
            raise ValueError("Gateway address is required for host based route")
        host = kwargs.get('host')
        ip_type = get_ip_address_type(host)
        if ip_type == "ipv6":
            cmd = "route -A inet6 add  %s gateway %s" % (host, gateway)
        else:
            cmd = "route add -host %s gateway %s" % (host, gateway)
    else:
        # Configure network based route
        if network is None or netmask is None or gateway is None:
            device.log(level='ERROR', \
                         message="network,netmask and gateway are required for network based route")
            raise ValueError("network,netmask and gateway are required for network based route")
        ip_type = get_ip_address_type(network)
        if ip_type == "ipv6":
            cmd = "route -A inet6 add %s/%s gateway %s" % (network, netmask, gateway)
        else:
            cmd = "route add -net %s netmask %s gateway %s" % (network, netmask, gateway)
    if 'interface' in kwargs:
        interface = kwargs.get('interface')
        cmd = cmd + " dev " + interface
    # Execute command on host
    device.shell(command=cmd)
    # Check for successfully configuration
    if ip_type == "ipv6":
        response = device.shell(command="route -n -A inet6")
    else:
        response = device.shell(command="netstat -nr")
    # Match response based on route type to check success
    if 'default_gateway' in kwargs:
        if ip_type == "ipv6":
            match = re.search("/*/0" + '.*' + default_gateway, response.response())
        else:
            match = re.search("0.0.0.0" + '.*' + default_gateway + '.*' + "0.0.0.0",
                              response.response())
    elif 'host' in kwargs:
        if ip_type == "ipv6":
            match = re.search(host + '/' + "128" + '.*' + gateway + '.*\n', response.response())
        else:
            match = re.search(host + '.*' + gateway + '.*' + "255.255.255.255" + '.*',
                              response.response())
    else:
        if ip_type == "ipv6":
            match = re.search(str(network) + "/" + str(netmask) + '.*' + str(gateway) + '.*',
                              response.response())
        else:
            match = re.search(str(network) + '.*' + str(gateway) + '.*' + str(netmask) + '.*',
                              response.response())
    if match:
        device.log(level='INFO', message="%s Route is configured" % (ip_type))
        return True
    else:
        device.log(level='ERROR', message="%s Route is not configured" % (ip_type))
        raise Exception("Route is not configured")


def delete_route(device=None, network=None, netmask=None, gateway=None, **kwargs):
    """
    To delete IPv4/IPv6 route in the linux host
    Example:
      delete_route(device=linux, network="3.0.0.0", netmask="255.0.0.0", gateway="4.0.0.254")
      delete_route(device=linux, host="1.2.3.4")
      delete_route(device=linux, default_gateway="4.0.0.254")
      delete_route(device=linux, network="2007::", netmask="64", gateway= "2008::254")
      delete_route(device=linux, host="2007::1")
      delete_route(device=linux, default_gateway="2001::254")
    Robot Example:
      delete route  device=$(linux)  network="3.0.0.0"  netmask="255.0.0.0"
                    gateway="4.0.0.254"
      delete route  device=$(linux)  host="1.2.3.4"
      delete route  device=$(linux)  default_gateway="4.0.0.254"
      delete route  device=$(linux)  network="2007::"  netmask="64"
      delete route  device=$(linux)  host=""2007::1"
      delete route  device=$(linux)  default_gateway="2001::254"

     :param str device:
         **REQUIRED** Device handle for linux host
     :param str network:
         *OPTIONAL* IPv4/IPv6 network address, not applicable with host or default route deletion
     :param str netmask:
         *OPTIONAL* Address mask . Mandatory with network delete configuration
              For IPv4 address, it should be 4 octets number such as "255.255.0.0"
              For IPv6 address, mask would be prefix as 64,128 etc.
     :param str gateway:
         *OPTIONAL* Gateway address for network based route deletion
     :param str default_gateway:
         *OPTIONAL* Default gateway address. network,gateway and host are ignored when deleting
                    default_gateway
     :param str host:
         *OPTIONAL* Host ip address , network and netmask are ignored when deleting host
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device argument is mandatory")

    # Configure to delete default gw and ignore other configuration options
    if 'default_gateway' in kwargs:
        default_gateway = kwargs.get('default_gateway')
        ip_type = get_ip_address_type(default_gateway)
        if ip_type == "ipv6":
            cmd = "route -A inet6 del default gateway %s" % (default_gateway)
        else:
            cmd = "route del default gateway %s" % (default_gateway)
    # Configure to delete host based route.
    elif 'host' in kwargs:
        host = kwargs.get('host')
        ip_type = get_ip_address_type(host)
        if ip_type == "ipv6":
            cmd = "route -A inet6 del  %s" % (host)
        else:
            cmd = "route del -host %s " % (host)
    # Configure to delete network based route , Network and netmask are  mandatory here
    else:
        if network is None or netmask is None:
            device.log(level='ERROR', \
                         message="network and netmask are required to delete network based route")
            raise ValueError("network and netmask are required to delete network based route")
        ip_type = get_ip_address_type(network)
        if ip_type == "ipv6":
            cmd = "route -A inet6 del %s/%s" % (network, netmask)
        else:
            cmd = "route del -net %s netmask %s" % (network, netmask)
        # if gateway is present add it in command
        if gateway is not None:
            cmd = cmd + ' gw' + ' ' + gateway

    # Execute command on host
    device.shell(command=cmd)
    # Check for successfully configuration
    if ip_type == "ipv6":
        response = device.shell(command="route -n -A inet6")
    else:
        response = device.shell(command="netstat -nr")
    # Match response based on route type to check success
    if 'default_gateway' in kwargs:
        if ip_type == "ipv6":
            match = re.search("/*/0" + '.*' + default_gateway, response.response())
        else:
            match = re.search("0.0.0.0" + '.*' + default_gateway + '.*' + "0.0.0.0",
                              response.response())
    elif 'host' in kwargs:
        if ip_type == "ipv6":
            match = re.search(host + '/' + "128" + '.*' + '.*', response.response())
        else:
            match = re.search(host + '.*' + "255.255.255.255" + '.*', response.response())
    else:
        if ip_type == "ipv6":
            match = re.search(network + "/" + netmask + '.*', response.resp)
        else:
            match = re.match(network + '.*' + netmask + '.*', response.response())

    if match:
        device.log(level='ERROR', message="%s Route is not deleted" % (ip_type))
        raise Exception("Route is not deleted")
    else:
        device.log(level='INFO', message="%s Route is deleted" % (ip_type))
        return True


def add_arp(device=None, ip_address=None, hardware_address=None):
    """
    To add ARP entry in Linux host
    Example:
      add_arp(device=linux, ip_address="4.0.0.7", hardware_address="84:18:88:14:A0:80")
    Robot Example:
      add arp  device=$(linux)  ip_address="4.0.0.7"  hardware_address="84:18:88:14:A0:80"

    :param str device:
         **REQUIRED** Device handle for linux host
    :param str ip_address:
         **REQUIRED** IP address
     :param str hardware_address:
         **REQUIRED** Hardware/MAC address
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if ip_address is None or hardware_address is None:
        device.log(level='ERROR', message="ip_addr and hardware_address are mandatory argument")
        raise ValueError("ip_addr and hw_addr are mandatory argument")

    device.shell(command="arp -s %s %s" % (ip_address, hardware_address))
    response = device.shell(command="arp -a")
    match = re.search('(' + ip_address + ')' + '.*' + 'ether', response.response())
    if match:
        device.log(level='INFO', message="ARP entry is added successfully")
        return True
    else:
        device.log(level='ERROR', message="ARP entry is not added successfully")
        raise Exception("ARP entry is not added successfully")


def delete_arp(device=None, ip_address=None):
    """
    To delete ARP entry in Linux host
    Example:
      delete_arp(device=linux, ip_address="4.0.0.7")
    Robot Example:
      delete arp  device=$(linux)  ip_address="4.0.0.7"

    :param str device:
         **REQUIRED** Device handle for linux host
    :param str ip_address:
         **REQUIRED** IP address
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if ip_address is None:
        device.log(level='ERROR', message="ip_address is mandatory argument")
        raise ValueError("ip_addr is mandatory argument")

    device.shell(command="arp -d %s" % (ip_address))
    response = device.shell(command="arp -a")
    match = re.search('(' + ip_address + ')' + '.*' + 'ether', response.response())
    if match:
        device.log(level='ERROR', message="ARP entry is not deleted successfully")
        raise Exception("ARP entry is not deleted successfully")
    else:
        device.log(level='INFO', message="ARP entry is deleted successfully")
        return True


def add_ipv6_neighbor(device=None, ipv6_address=None, link_address=None, interface=None):
    """
    To add ipv6 neighbor in Linux host
    Example:
       add_ipv6_neighbor(device=linux, ipv6_add="2005::1", link_address="00:50:56:9E:42:39")
    Robot example:
       add upv6 neighbor  device=linux  ipv6_add="2005::1"  link_address="00:50:56:9E:42:39"

    :param str device:
         **REQUIRED** Device handle for linux host
    :param str ipv6_address:
         **REQUIRED** IPv6 address of neighbor
     :param str link_address:
         **REQUIRED** Hardware/Link Layer address of neighbor
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """

    if device is None:
        raise ValueError("device is mandatory argument")
    if ipv6_address is None or link_address is None or interface is None:
        device.log(level='ERROR',
                   message="ipv6_address,link_address and interface are mandatory arguments")
        raise ValueError("ipv6_address,link_address and interface are mandatory arguments")

    link_address = link_address.lower()
    device.shell(
        command="ip -6 neigh add %s lladdr %s dev %s" % (ipv6_address, link_address, interface))
    response = device.shell(command=" ip -6 neigh")
    match = re.search(ipv6_address + '.*' + 'dev' + '.*' + interface + '.*' + 'lladdr' + '.*' +
                      link_address, response.response())
    if match:
        device.log(level='INFO', message="Neighbor is added successfully")
        return True
    else:
        device.log(level='ERROR', message="Neighbor is not added successfully")
        raise Exception("Neighbor is not added successfully")


def delete_ipv6_neighbor(device=None, ipv6_address=None, link_address=None, interface=None):
    """
    To delete ipv6 neighbor in Linux host
    Example:
       delete_ipv6_neighbor(device=linux, ipv6_add="2005::1", link_address="00:50:56:9E:42:39")
    Robot example:
       delete ipv6 neighbor  device=linux  ipv6_add="2005::1"  link_address="00:50:56:9E:42:39"

    :param str device:
         **REQUIRED** Device handle for linux host
    :param str ipv6_address:
         **REQUIRED** IPv6 address of neighbor
     :param str link_address:
         **REQUIRED** Hardware/Link Layer address of neighbor
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """

    if device is None:
        raise ValueError("device is mandatory argument")
    if ipv6_address is None or link_address is None or interface is None:
        device.log(level='ERROR',
                   message="ipv6_address,link_address and interface are mandatory arguments")
        raise ValueError("ipv6_address,link_address and interface are mandatory arguments")

    link_address = link_address.lower()
    device.shell(
        command="ip -6 neigh del %s lladdr %s dev %s" % (ipv6_address, link_address, interface))
    response = device.shell(command=" ip -6 neigh")
    match = re.search(ipv6_address + '.*' + 'dev' + '.*' + interface + '.*' + 'lladdr' + '.*'
                      + link_address, response.response())
    if match:
        device.log(level='ERROR', message="Neighbor is not deleted successfully")
        raise Exception("Neighbor is not deleted successfully")
    else:
        device.log(level='INFO', message="Neighbor is deleted successfully")
        return True


def get_linux_int_mac(device=None, interface=None):
    """
    To get Linux host's interface mac address
    Example:
        get_linux_int_mac(device=linux, interface="eth1")
    Robot Example:
        get linux int mac  device=${linux}  interface="eth1"

    :param str device:
         **REQUIRED** Device handle for Linux host
    :param interface:
        **REQUIRED** Interface name of Linux host.
    :return: return the mac address.
    :rtype: str
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if interface is None:
        device.log(level='ERROR', message="interface argument is mandatory")
        raise ValueError("interface argument is mandatory")

    response = device.shell(command="/sbin/ifconfig %s" % (interface))
    mac = re.search(r'(HWaddr|ether)\s+((([a-fA-F\d]{2}):){5}[a-fA-F\d]{2})', response.response())
    if mac:
        return mac.group(2)
    else:
        raise Exception("Couldn't find the MAC of interface %s" % (interface))

def get_linux_int_ip(device=None, interface=None):
    """
    Get ip address of physical interface of linux machine
    Example:
        get_physical_interface_ip(device=unix, intf="eth1")

    Robot Example:
        Get Physical Interface Ip    device=${traffic_generator_handle}
        ...    intf=${linux-interface1}.${linux-interface-vlan}

    :param device device:
        **REQUIRED** linux handle
    :param str linux interface for which we are seeking ip:
        **REQUIRED** interface name

    :return: Ip address of physical interface
    :rtype: String
    """

    pattern_ipv4 = "((inet addr:|inet\s+)((?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s)"
    if device is None:
        raise ValueError("device is mandatory argument")
    if interface is None:
        device.log(level='ERROR', message="device, interface are mandatory arguments")
        raise ValueError("interface argument is mandatory")

    output = device.shell(command='/sbin/ifconfig %s' %(interface))

    match = re.search(pattern_ipv4, output.response())
    if match:
        ipv4_address = match.group(3)
        return ipv4_address
    else:
        device.log(level='ERROR', message="Ipv4 address not configured in interface. " + output.response())
        raise Exception("Ipv4 address not configured in interface")


def get_linux_default_gateway(device=None):
    """
    To get the default gateway IP from the linux host.
    Example:
        get_linux_default_gateway(device=device)
    Robot Example:
        get linux default gateway    device=${client}

    :param Device device:
        **REQUIRED** Linux device handle
    :return: True
    """
    if device is None:
        raise Exception("Linux handle is a mandatory argument")

    resp = device.shell(command="ip route show | grep default").response()
    default_gw = re.search(r'default via (\d+.\d+.\d+.\d+) dev', resp)

    if default_gw:
        return default_gw.group(1)
    else:
        device.log(
            level="ERROR",
            message="Couldn't find the default gateway")
        raise Exception("Couldn't find the default gateway")


def check_ip_forward(device=None, mgt_intf="eth0", fwd_intf="eth1"):
    """
    To check whether ip forwarding is enabled.
    If not enabled, it'll enable ip forwarding seamlessly.
    Example:
        check_ip_forward(device=device, fwd_intf="eth2")
    Robot Example:
        check ip forward    device=${dut}

    :param Device device:
        **REQUIRED** Linux device handle
    :param str mgt_intf:
        **OPTIONAL** management interface to enable ip forwarding
        'Default Value' eth0
    :param str fwd_intf:
        *OPTIONAL* Forwarding interface to enable ip forwarding
        'Default Value' eth1
    :return: True in success
    :rtype: Bool
    """
    if device is None:
        raise Exception("Linux handle is a mandatory argument")

    resp = device.shell(command="sysctl net.ipv4.ip_forward").response()
    if re.search('net.ipv4.ip_forward = 1', resp):
        device.log(level='INFO', message="IP forwarding is already enabled in this device")
    else:
        device.shell(command="echo 1 > /proc/sys/net/ipv4/ip_forward")
        device.log(level='INFO', message="IP forwarding is enabled now in the device")

    device.shell(command="iptables --table nat --append POSTROUTING --out-interface %s -j MASQUERADE" %(mgt_intf))
    device.shell(command="iptables --append FORWARD --in-interface %s -j ACCEPT" %(fwd_intf))


def configure_linux_tunnel(device=None, remote_address=None,
                           local_address=None, interface=None, tunnel_name=None):
    """
    To confgiure ipip/ipip6 tunnel in Linux host
    IPIP6 Example:
    configure_linux_tunnel(device=linux, remote_address="2002:2010::1401:1", local_address="2002:2010::1401:65", interface="eth1",
    tunnel_name="dslite")

    configure_linux_tunnel(device=linux, remote_address="2.1.1.2", local_address="2.1.1.1", interface="eth1", tunnel_name="dslite")

    Robot example:
    configure linux tunnel  device=linux  remote_address="2002:2010::1401:1"  local_address="2002:2010::1401:65"  tunnel_name="dslite"

    configure linux tunnel  device=linux  remote_address="2.1.1.2"  local_address="2.1.1.1"  interface="eth1"  tunnel_name="dslite"

    :param str device:
        **REQUIRED** Device handle for linux host
    :param str remote_address:
        **REQUIRED** IPv4/IPv6 address, Mandatory with ipip/ipip6 tunnel configuration
    :param str local_address:
        **REQUIRED** IPv4/IPv6 address, Mandatory with ipip/ipip6 tunnel configuration
    :param str interface:
        **REQUIRED** Interface name to configure ipv4/ipv6 address
    :param str tunnel_name:
        **REQUIRED** Tunnel name, can be any string
    :return: True if successful.
                In all other cases Exception is raised
    :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if remote_address is None or local_address is None or interface is None or tunnel_name is None:
        device.log(level='ERROR',
                   message="remote address,local address,device interface\
                       and tunnel name are mandatory arguments")
        raise ValueError(
            "remote address,local address,device interface\
                and tunnel name are mandatory arguments")
    remote_ip_ver = ipaddress.ip_address(remote_address)
    local_ip_ver = ipaddress.ip_address(local_address)
    device.log(level='INFO', message="remote ip version is " + str(remote_ip_ver.version))
    device.log(level='INFO', message="local ip version is " + str(local_ip_ver.version))
    if remote_ip_ver.version == local_ip_ver.version:
        device.shell(command="modprobe tun")
        response = device.shell(command="lsmod | grep tun")
        match = re.search("tun\\s+\\d+\\s+\\d", response.response())
        if match is None:
            device.log(level='ERROR', message="tunnel service module not up")
            raise Exception("tunnel service module not up")
        if remote_ip_ver.version == 6:
            device.log(
                level='INFO',
                message="Configuring IPIP6 tunnel since remote address is IPV6 version")
            device.shell(command="modprobe ip6_tunnel")
            response = device.shell(command="lsmod | grep ip6_tunnel")
            match = re.search("ip6_tunnel\\s+\\d+\\s+\\d", response.response())
            if match is None:
                device.log(level='ERROR', message="ipip6 tunnel service not up")
                raise Exception("ipip6 tunnel service not up")
            device.shell(command="ip -6 tunnel del %s" % (tunnel_name))
            device.shell(
                command="ip -6 tunnel add %s mode ipip6 remote %s local %s dev %s" %
                (tunnel_name, remote_address, local_address, interface))
            device.shell(command="ip link set dev %s up" % (tunnel_name))
            response = device.shell(command="ip -6 tun")
            match = re.search(
                tunnel_name +':' +' ip/ipv6' +' remote ' +remote_address +' local ' +local_address +' dev ' +interface,
                response.response())
            if match is None:
                device.log(level='ERROR', message="ipip6 tunnel is not added successfully")
                raise Exception("ipip6 tunnel is not added successfully")
            else:
                device.log(level='INFO', message="ipip6 tunnel is added successfully")
                return True
        else:
            device.log(
                level='INFO',
                message="Configuring IPIP tunnel since remote address is IPV4 version")
            device.shell(command="modprobe ipip")
            response = device.shell(command="lsmod | grep ipip")
            match = re.search("ipip\\s+\\d+\\s+\\d", response.response())
            if match is None:
                device.log(level='ERROR', message="ipip tunnel service not up")
                raise Exception("ipip tunnel service not up")
            device.shell(command="ip tunnel del %s" % (tunnel_name))
            device.shell(command="ip tunnel add %s mode ipip remote %s local %s dev %s" %
                         (tunnel_name, remote_address, local_address, interface))
            device.shell(command="ip link set dev %s up" % (tunnel_name))
            response = device.shell(command="ip tun")
            match = re.search(
                tunnel_name +':' +' ip/ip  ' +'remote ' +remote_address +'  local ' +local_address +'  dev ' +interface,
                response.response())
            if match is None:
                device.log(level='ERROR', message="ipip tunnel is not added successfully")
                raise Exception("ipip tunnel is not added successfully")
            else:
                device.log(level='INFO', message="ipip tunnel is added successfully")
                return True
    else:
        device.log(level='ERROR', message="Remote and Local IP versions are not same")
        raise Exception("Remote and Local IP versions are not same")


def delete_linux_tunnel(device=None, remote_address=None,
                        local_address=None, interface=None, tunnel_name=None):
    """
    To delete ipip/ipip6 tunnel in Linux host
    IPIP/IPIP6 Example:
    delete_linux_tunnel(device=linux, remote_address="2002:2010::1401:1", local_address="2002:2010::1401:65", interface="eth1", tunnel_name="dslite")

    delete_linux_tunnel(device=linux, remote_address="2.1.1.2", local_address="2.1.1.1", interface="eth1", tunnel_name="dslite")

    Robot example:
    delete linux tunnel  device=linux  remote_address="2002:2010::1401:1"  local_address="2002:2010::1401:65"  tunnel_name="dslite"

    delete linux tunnel  device=linux  remote_address="2.1.1.2"  local_address="2.1.1.1"  interface="eth1"  tunnel_name="dslite"

    :param str device:
        **REQUIRED** Device handle for linux host
    :param str remote_address:
        **REQUIRED** IPv4/IPv6 address, Mandatory for deleting ipip/ipip6 tunnel configuration
    :param str local_address:
        **REQUIRED** IPv4/IPv6 address, Mandatory for ipip/ipip6 tunnel configuration
    :param str interface:
        **REQUIRED** Interface name to delete ipv4/ipv6 address
    :param str tunnel_name:
        **REQUIRED** Tunnel name, Mandatory for deleting tunnel
    :return: True if successful.
                In all other cases Exception is raised
    :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if remote_address is None or local_address is None or interface is None or tunnel_name is None:
        device.log(level='ERROR',
                   message="remote address,local address,device interface\
                       and tunnel name are mandatory arguments")
        raise ValueError(
            "remote address,local address,device interface\
                and tunnel name are mandatory arguments")
    remote_ip_ver = ipaddress.ip_address(remote_address)
    if remote_ip_ver.version == 6:
        device.log(level='INFO', message="Deleting IPIP6 tunnel since\
            remote address is IPV6 version")
        device.shell(command="modprobe -r tun")
        device.shell(command="modprobe -r ip6_tunnel")
        device.shell(command="ip -6 tunnel del %s" % (tunnel_name))
        response = device.shell(command="ip -6 %s" % (tunnel_name))
        match = re.search(
            tunnel_name +':' +' ip/ipv6' +' remote ' +remote_address +' local ' +local_address +' dev ' +interface,
            response.response())
        if match is None:
            device.log(level='INFO', message="ipip6 tunnel is deleted successfully")
            return True
        else:
            device.log(level='ERROR', message="ipip6 tunnel is not deleted successfully")
            raise Exception("ipip6 tunnel is not deleted successfully")
    else:
        device.log(level='INFO', message="Deleting IPIP tunnel since\
            remote address is IPV4 version")
        device.shell(command="modprobe -r tun")
        device.shell(command="modprobe -r ipip")
        device.shell(command="ip tunnel del %s" % (tunnel_name))
        response = device.shell(command="ip %s" % (tunnel_name))
        match = re.search(
            tunnel_name +':' +' ip/ip  ' +'remote ' +remote_address +'  local ' +local_address +'  dev ' +interface,
            response.response())
        if match is None:
            device.log(level='INFO', message="ipip tunnel is deleted successfully")
            return True
        else:
            device.log(level='ERROR', message="ipip tunnel is not deleted successfully")
            raise Exception("ipip tunnel is not deleted successfully")

def get_linux_interface_having_mac(device_handle, mac):

    """
    Keyword to get the name of the interface with specific mac address
    Example:
      get_linux_interface_having_mac(device_handle=linux, mac="00:00:00:10:10:10")

    Robot Example:
      Get Linux Interface Having MAC   device_handle=${linux}  mac=00:00:00:10:10:10

    :param str device_handle:
      **REQUIRED** Device Handle

    :param str mac:
      **REQUIRED** MAC address of the interface

    :return: Tuple containing status of operation and physical interface name
    :rtype: tuple
    """
    device_handle.log(level='INFO',
                      message="Fetching Linux Interface Name having MAC address: %s on device: %s" % (mac, device_handle))

    try:
        _cmd_ = "ip link show"
        _output_ = device_handle.shell(command=_cmd_)

        _phy_ = ""
        _mac_ = ""

        for _row_ in re.split(r"\n(?=\d)", _output_.response()):
            _match_ = re.match(r'\d+:\s*(\S*):.*\n\s+link\/ether\s(\S*)', _row_)
            if _match_ is not None:
                _phy_ = _match_.group(1)
                _mac_ = _match_.group(2)
                if _mac_.lower() == mac.lower():
                    device_handle.log(level='INFO', message="Found Interface: %s with MAC: %s" % (_phy_, mac))
                    return True, _phy_

        # no interface found
        return False, None

    except Exception as _exception_:
        raise Exception("Exception caught: %s: %s" % (type(_exception_), _exception_))

def get_linux_interface_statistics(device_handle, intf_name):

    """
    Keyword to fetch the statistics from an interface on a Linux Device
    Example:
      get_linux_interface_statistics(device_handle=linux, intf_name='eth1')
      get_linux_interface_statistics(device_handle=linux, intf_name='eth2')

    Robot Example:
      Get Linux Interface Statistics  device_handle=${linux}  intf_name=eth1
      Get Linux Interface Statistics  device_handle=${linux}  intf_name=eth2

    :param str device_handle:
      **REQUIRED** Device Handle

    :param str intf_name:
      **REQUIRED** Name of the Interface

    :return: Dictionary containing the following statistics of the interface
             as keys
            "tx_pkts"
            "rx_pkts"
            "tx_bytes"
            "rx_bytes"
            "tx_errors"
            "rx_errors"
    """


    try:

        device_handle.log(level='INFO', message="Fetching Statistics of Linux Interface: %s from Device: %s" % (intf_name, device_handle))
        _cmd_ = "ifconfig " + intf_name
        _output_ = device_handle.shell(command=_cmd_)

        _stats_dict_ = {
            "tx_pkts" : 0,
            "rx_pkts" : 0,
            "tx_bytes" : 0,
            "rx_bytes" : 0,
            "tx_errors" : 0,
            "rx_errors" : 0,
        }

        _status_ = True
        for _row_ in _output_.response().split("\n"):

            _match_ = re.match(r"\s+RX\s+packets:(\d+)\s+errors:(\d+)", _row_)
            if _match_ is not None:
                _stats_dict_["rx_pkts"] = _match_.group(1)
                _stats_dict_["rx_errors"] = _match_.group(2)
                continue

            _match_ = re.match(r"\s+TX\s+packets:(\d+)\s+errors:(\d+)", _row_)
            if _match_ is not None:
                _stats_dict_["tx_pkts"] = _match_.group(1)
                _stats_dict_["tx_errors"] = _match_.group(2)
                continue

            _match_ = re.match(r"\s+RX\s+bytes:(\d+).*TX\s+bytes:(\d+).*", _row_)
            if _match_ is not None:
                _stats_dict_["rx_bytes"] = _match_.group(1)
                _stats_dict_["tx_bytes"] = _match_.group(2)
                continue

        return _status_, _stats_dict_

    except Exception as _exception_:
        raise Exception("Exception caught: %s: %s" % (type(_exception_), _exception_))

def get_logged_in_user_ips(device_handle, mode="ssh"):

    """
    Keyword to return list of IP Addresses from where Users have logged in.
    Example:
      get_logged_in_user_ips(device_handle=linux, mode='ssh')
      get_logged_in_user_ips(device_handle=linux, mode='telnet')

    Robot Example:
      Get Logged In User IPs   device_handle=${linux}   mode=ssh
      Get Logged In User IPs   device_handle=${linux}   mode=telnet

    :param str device_handle:
      **REQUIRED** Device Handle

    :param str mode:
      **OPTIONAL** Login method ssh or telnet. Default: ssh

    :return: List of IP addresses
    """
    try:

        device_handle.log(level='INFO', message="Fetching IP addresses of logged in users on device: %s" % device_handle)

        _cmd_ = "netstat -W -tapen"
        _output_ = device_handle.shell(device=device_handle, command=_cmd_)

        _return_list_ = []
        _mode_tcp_port_ = {
            "ssh" : 22,
            "telnet" : 23
        }

        for _row_ in _output_.response().split("\n"):
            _match_ = re.match(r".*\s+(\S+):(22|23)\s+(\S+):(\S+)\s+.*ESTABLISHED", _row_)
            if _match_ is not None:
                if _match_.group(2) == _mode_tcp_port_[mode]:
                    device_handle.log(level='INFO',
                                      message="Found Logged in User IP: %s on Port: %s" %(_match_.group(3), _match_.group(2)))
                    _return_list_.append(_match_.group(3))

        if len(_return_list_) == 0:
            device_handle.log(level='ERROR', message="No users found logged in")
            return False, _return_list_

        return True, _return_list_

    except Exception as _exception_:
        raise Exception("Exception Caught in fetching logged in users: %s : %s" % (type(_exception_), _exception_))

def configure_linux_interface(device=None, interface=None, address=None, mask=None, vlan_id=None, status=None, mtu=None):
    """
     To configure vlan tagged or untagged interface on Linux host using IP commands
	 Supports configuring IP address/MTU/status on the Linux interface
     Tagged interface created will be in the format "interface.vlan_id" e.g eth2.100
     Example:
       configure_linux_address(device=linux, interface="eth2", address="2008::1", mask="64")
       configure_linux_address(device=linux, interface="eth1", address="4.0.0.1",
                            mask="24", vlan_id="200")
     Robot Example:
       configure linux address  device=$(linux)  interface="eth2"  address="2008::1"  mask="64"
       configure linux address  device=$(linux)  interface="eth1"  address="4.0.0.1"  vlan_id="200"
                             mask="24"
       Resulting tagged interface created: "eth1.200" with IP 4.0.0.1/24
     :param str device:
         **REQUIRED** Device handle for the Linux host
     :param str interface:
         **REQUIRED** Interface name on which to configure IP or create a tagged sub-interface
     :param str address:
         **REQUIRED** IPv4/IPv6 Address to be configured
     :param str status:
         **OPTIONAL** Interface link status should be changed up/down
     :param str mtu:
         **OPTIONAL** Modify the mtu on the interface
     :param str vlan_id:
         **OPTIONAL** 802.1Q vlan-id for the tagged interface
     :param str mask:
         **REQUIRED** Address mask to be configured.
              For IPv4 address, mask would be prefix as 20,24 etc.
              For IPv6 address, mask would be prefix as 64,128 etc.
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    # Checking for mandatory arguments
    if device is None:
        raise ValueError("device is a mandatory argument")

    if interface is None:
        raise ValueError("Interface is a mandatory argument")

    if address is None and mtu is None and status is None:
        device.log(level='ERROR',
                   message="Arguments are not enough to take any action!")
        raise ValueError("Arguments are not enough to take any action!")

    if status is not None:
        state_cmd = "ip link set dev " + interface + " " + status
        device.log("Running: " + state_cmd)
        response = device.shell(command=state_cmd).response()
        device.log("Response: " + response)
        response = device.shell(command="ip addr show %s" % (interface))
        match = re.search('.*state\s' + status.upper() + '.*', response.response())
        if match:
            device.log(level='INFO', message="Interface state set to %s" % (status))
        else:
            device.log(level='ERROR', message="Interface state could not be set to %s"
                       % (status))
            raise Exception("Interface state does not match")

    if mtu is not None:
        state_cmd = "ip link set " + interface + " mtu " + str(mtu)
        device.log("Running: " + state_cmd)
        response = device.shell(command=state_cmd).response()
        device.log("Response: " + response)
        response = device.shell(command="ip addr show %s" % (interface))
        match = re.search('.*mtu\s' + str(mtu) + '.*', response.response())
        if match:
            device.log(level='INFO', message="MTU of %s is configured successfully" % (mtu))
        else:
            device.log(level='ERROR', message="MTU of %s is not configured successfully"
                       % (mtu))
            raise Exception("MTU is not configured successfully")

    if address is not None:
        # getting the ip address type and based on that start configuration
        ip_type = get_ip_address_type(iputils_strip_mask(address))
        if vlan_id is None:
            if ip_type == "ipv6":
                cmd = "ip -6 addr add dev " + interface + " " + address
                if mask is not None:
                    cmd = cmd + "/" + str(mask)
            else:
                cmd = "ip addr add dev " + interface + " " + address
                if mask is not None:
                    cmd = cmd + "/" + str(mask)
            device.log("Running: " + cmd)
            response = device.shell(command=cmd).response()
            device.log("Response: " + response)
            response = device.shell(command="ifconfig %s" % (interface))
        else:
            cmd_list = []
            tagged_intf = interface + "." + str(vlan_id)
            cmd = "ip link add link " + interface + " name "+ tagged_intf
            cmd = cmd + " type vlan id " + str(vlan_id)
            cmd_list.append(cmd)
            if ip_type == "ipv6":
                cmd = "ip -6 addr add dev " + tagged_intf + " " + address
                if mask is not None:
                    cmd = cmd + "/" + str(mask)
                cmd_list.append(cmd)
            else:
                cmd = "ip addr add dev " + tagged_intf + " " + address
                if mask is not None:
                    cmd = cmd + "/" + str(mask)
                cmd_list.append(cmd)
            if status is not None:
                cmd = "ip link set dev " + tagged_intf + " " + status
                cmd_list.append(cmd)
            for cmd in cmd_list:
                device.log("Running: " + cmd)
                response = device.shell(command=cmd).response()
                device.log("Response: " + response)
            response = device.shell(command="ifconfig %s.%s" % (interface, str(vlan_id)))
        if ip_type == "ipv6":
            match = re.search('.*inet6' + '.*' + iputils_strip_mask(address) + '.*', response.response())
        else:
            match = re.search('.*inet' + '.*' + iputils_strip_mask(address) + '.*', response.response())
        # Verify if ip address configured properly
        if match:
            device.log(level='INFO', message="%s address is configured successfully" % (ip_type))
        else:
            device.log(level='ERROR', message="%s address is not configured successfully"
                       % (ip_type))
            raise Exception("IPv4/IPv6 address is not configured successfully")
    return True

