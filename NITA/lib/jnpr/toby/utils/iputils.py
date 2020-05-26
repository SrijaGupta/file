"""Module containing the utility functions"""
__author__ = ['Sumanth Inabathini']
__contact__ = 'isumanth@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import ipaddress
from netaddr import IPNetwork
import platform
import subprocess
import logging
import time


def ip_get_version(ip_addr=None):
    """Return version of the given IPv4/v6 address.

    :param string ip_addr:
        **REQUIRED** IPv4/v6 address. Default None

    :returns:
        Version of the given IP

    :rtype: int

    EXAMPLE::
        ip_get_version('1.1.1.1') will return 4
        ip_get_version('2000::2') will return 6
    """

    if ip_addr is None:
        raise Exception('Missing mandatory argument, ip_addr')

    ip_addr = strip_mask(ip_addr)
    return ipaddress.ip_address(ip_addr).version

def is_ip(ip_addr):
    """Check given string is IP or not. Works for IPv4/v6

    :param string ip_addr:
        **REQUIRED** IPv4/v6 address

    :return: True if given string is IP address else False

    :rtype: bool

    EXAMPLE::
        is_ip('1.1.1.1/24') will return True
        is_ip('1.1.1/24') will return False
        is_ip('2000::BEC/64') will return True
    """

    try:
        ip_addr = strip_mask(ip_addr)
        if ipaddress.ip_address(ip_addr):
            return True

    except (TypeError, ValueError):
        return False

def is_ip_ipv4(ip_addr):
    """Check given string is IPv4 address or not

    :param string ip_addr:
        **REQUIRED** IPv4 address

    :returns: True if given string is IPv4 address else False

    :rtype: bool

    EXAMPLE::
        is_ip_ipv4('1.1.1.1') will return True
        is_ip_ipv4('2000::2') will return False
    """
    ip_addr = strip_mask(ip_addr)
    return True if ip_get_version(ip_addr) == 4 else False

def is_ip_ipv6(ip_addr):
    """Check given string is IPv6 address or not

    :param string ip_addr:
        **REQUIRED** IPv6 address

    :returns: True if given string is IPv6 address else False

    :rtype: bool

    EXAMPLE::
        is_ip_ipv6('1.1.1.1') will return False
        is_ip_ipv6('2000::2') will return True
    """
    ip_addr = strip_mask(ip_addr)
    return True if ip_get_version(ip_addr) == 6 else False

def is_ip_in_subnet(ip_addr, subnet):
    """Check if given ip is in the given subnet or not. Works for IPv4/v6

    :param string ip_addr:
        **REQUIRED** IPv4/v6 address

    :param string subnet:
        **REQUIRED** subnet address

    :returns: True if given ip is in the given subnet else False

    :rtype: bool

    EXAMPLE::
        is_ip_in_subnet('1.1.1.1', '1.1.1.0/24') will return True
        is_ip_in_subnet('1.1.10.1', '1.1.1.0/24') will return False
        is_ip_in_subnet('2001:0:3238:DFE1:63::FEFB', '2001:0:3238:DFE1:63::0/112') will return True
    """

    return ipaddress.ip_address(ip_addr) in ipaddress.ip_network(subnet)

def cmp_ip(ip_addr1, ip_addr2):
    """Check if given two ips are equal or not. Works for IPv4/v6

    :param string ip_addr1:
        **REQUIRED** ip address

    :param string ip_addr2:
        **REQUIRED**  ip address

    :return: True given ips are equal else False

    :rtype: bool

    EXAMPLE::

        cmp_ip('1.1.1.1', '30.1.1.2') will return False
        cmp_ip('2001:0:3238:DFE1:63::FEFB', '2001:0:3238:DFE1:63::FEFC') will return False
    """
    return ipaddress.ip_address(ip_addr1) == ipaddress.ip_address(ip_addr2)

def get_mask(ip_addr):
    """Return mask from the given ip. Works for IPv4/v6

    :param string  ip_addr:
        **REQUIRED** IPv4/v6 address

    :return: Mask if mask present in IP else None

    :rtype: String or None type

    EXAMPLE::
        get_mask('1.1.1.1/24') will return 24
        get_mask('2001:0:3238:DFE1:63::FEFB/128') will return 128
    """
    return ip_addr.split('/')[1] if re.search('/', ip_addr) else None

def get_network_mask(ip_addr):
    """Return netmask of the given IPv4/v6 address.

    :param string ip_addr:
        **REQUIRED** IPv4/v6 address

    :returns: netmask if given string is IP else False

    :rtype: String or bool

    EXAMPLE::
        get_network_mask('1.1.1.1/24') will return '255.255.255.0'
        get_network_mask('2001:0:3238:DFE1:63::FEFB/112') will return
                        'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
    """

    if is_ip(ip_addr):
        return str(IPNetwork(ip_addr).netmask)
    else:
        return False

def get_network_address(ip_addr, with_prefix=False, with_netmask=False):
    """Return network address of the given IPv4/v6 address

    If with_prefix and with_netmask all set True, will return with prefix

    :param string ip_addr:
        **REQUIRED** IPv4/v6 address

    :param bool with_prefix:
        *OPTIONAL* return address with prefix. default: False

    :param bool with_netmask:
        *OPTIONAL* return address with netmask. default: False

    :returns: network address.

    :rtype: String

    EXAMPLE::
        get_network_address('1.1.1.1/16') will return '1.1.0.0'
        get_network_address('1.1.1.1/16', with_prefix=True) will return '1.1.0.0/16'
        get_network_address('1.1.1.1/16', with_netmask=True) will return '1.1.0.0/255.255.0.0'
        get_network_address('1.1.1.1/16', with_prefix=True, with_netmask=True) will return '1.1.0.0/16'
        get_network_address('2001:0:3238:DFE1:63::FEFB/112') will return '2001:0:3238:dfe1:63::'
        get_network_address('2001:0:3238:DFE1:63::FEFB/112', with_prefix=True) will return '2001:0:3238:dfe1:63::/112'
    """
    if not is_ip(ip_addr):
        return False

    if with_prefix is True and with_netmask is True:
        with_netmask = False

    addr_obj = IPNetwork(ip_addr)
    network = str(addr_obj.network)
    if with_prefix is True:
        network += "/{}".format(addr_obj.prefixlen)

    if with_netmask is True:
        network += "/{}".format(str(addr_obj.netmask))

    return network

def normalize_ipv6(ip_addr, compress_zero=False):
    """Normalize the given IPv6 address

    :param string ip_addr:
        **REQUIRED** The IPv6 address to be expanded

    :param bool compress_zero
        *OPTIONAL* The IPv6 address will represent with one "0" instead of multiple

    :returns: Normalized IPv6 address

    :rtype: String

    EXAMPLE::
        normalize_ipv6('2000::2') will return '2000:0000:0000:0000:0000:0000:0000:0002'
        normalize_ipv6('2000::2', compress_zero=True) will return '2000:0:0:0:0:0:0:2'

    """
    mask = get_mask(ip_addr)
    ip_addr = strip_mask(ip_addr)
    ip_addr = ipaddress.ip_address(ip_addr).exploded

    # To remove the multiple zeros if compress_zero is true
    if compress_zero is True and ipaddress.ip_address(ip_addr).version == 6:
        ip_addr = ':'.join([str(int(ip_hextet)) for ip_hextet in ip_addr.split(':')])

    if mask is not None:
        return ip_addr + '/' + mask
    else:
        return ip_addr

def strip_mask(ips):
    """Strip mask from the given IPv4/v6 address(es).

    Strips mask from the given IPv4/v6 address(es) and
    returns the IP address(es)

    :param ips:
        **REQUIRED** IPv4/v6 address with subnet
        Can be a single ip address or list of ip addresses
    :return ip:
        Ip address(es) with mask striped off

    EXAMPLE::
        strip_mask('10.0.1.2/24') will return '10.0.1.2'
        strip_mask('2001:0:3238:DFE1:63::FEFB/128') will return '2001:0:3238:DFE1:63::FEFB'
    """

    if isinstance(ips, list):
        ips[:] = [re.sub(r'/.*$', '', s) for s in ips]
    else:
        ips = re.sub(r'/.*$', '', ips)

    return ips

def incr_ip(address, step=1):
    """Increment IPv4/v6 by the given step

    Increments the given IPv4/v6 by a step value.
    If step value is not passed, it increments the ip by 1
    :param string address:
        **REQUIRED** IPv4/v6 address with subnet

    :param int step:
        **OPTIONAL** Increment step Default is 1

    :returns:
        Incremented ip

    :rtype: string

    EXAMPLE::

        incr_ip('10.0.1.2/24') will return '10.0.1.3/24'
        incr_ip('10.0.1.2/24', 10) will return '10.0.1.12/24'
        incr_ip('2000::BE/64',20) will return '2000::d2/64'
    """
    mask = None
    if re.search(r"\/(.*)", address):
        mask = re.search(r"\/(.*)", address).group()
        address = strip_mask(address)
    #if is_ip_ipv4(address):
        #ip_addr = ipaddress.IPv4Address(address) + int(step)
    #else:
        #ip_addr = ipaddress.IPv6Address(address) + int(step)
    ip_addr = ipaddress.ip_address(address) + int(step)
    if mask is not None:
        ip_addr = ip_addr.__str__() + mask
        return ip_addr
    else:
        return ip_addr.__str__()

def incr_ip_subnet(address, step=1):
    """Increment subnet of the given IPv4/v6 address.

    Increments subnet of the given IPv4/v6 address by given step value.
    IP needs to be passed with mask so that subnet can be incremented accordingly.
    Incase mask is missing in IP, 32 and 128 are added for IPv4 and IPv6 addresses respectively.

    :param ip address:
        **REQUIRED** IPv4/v6 address with subnet mask
    :param int step:
        **OPTIONAL** Increment step Default is 1

    :returns: Incremented IP

    :rtype: string

    EXAMPLE::
        incr_ip_subnet('10.0.1.2/24') will return '10.0.2.2/24'
        incr_ip_subnet('10.0.1.2/24', 10) will return '10.0.11.2/24'
        incr_ip_subnet('2000::BE/64',20) will return '2000:0:0:14::be/64'
    """

    #t.log('INFO', "Going to increment subnet of {} by {}".format(address,step))
    addr_obj = ipaddress.ip_address(strip_mask(address))
    mask = get_mask(address)
    if mask is None:
        mask = addr_obj.max_prefixlen
    count = (2 ** (addr_obj.max_prefixlen - int(mask))) * int(step)
    return '{}/{}'.format(addr_obj+count, mask)

def get_network_ip_range(network):
    """Return the given address's Network IP Range

    :param string network:
        **REQUIRED** Network address with mask

    :returns: IP Range

    :rtype: string

    Example::

        get_network_ip_range('10.10.10.0/24') will return '10.10.10.1-10.10.10.254'
    """

    _mask = int(get_mask(network))
    if _mask == 32:
        _ip = strip_mask(network)
        return '{}-{}'.format(_ip, _ip)
    network_obj = ipaddress.ip_network(network)
    ip_list = list(network_obj.hosts())
    return '{}-{}'.format(ip_list[0], ip_list[-1])


def ping(**kwargs):
    """ping the host to make sure its reachable

        :param host
            **REQUIRED** Destination ip to ping
        :param ipv6
            **OPTION** Ping for IPv6. True for IPv6, False for Ipv4.
            Default: False
        :param count:
            **OPTION** Number of packet to send
            default: 5
        :param option:
            **OPTION** Other options for ping
            Eg: "-l 1000" Send buffer size 1000.
        :param timeout
            **OPTION** timeout of ping
            Default: 30
        :param interval
            **OPTION** interval of ping
            Default: 10
        :param negative (True/False)
            **OPTION** Negative test
            Default: False
        :param acceptable_packet_loss
            **OPTION** Number of packets lost that is acceptable to consider
            the test PASS
            default: "0"
        :param fail_ok
            **OPTION**([error|info|warn]) Fail Msg log level as Warn or Info.
            allows you to prevent printing an error message in
            case of an acceptable failure.
            Setting to info will make any unsuccessful lookup be printed under
            log level INFO.
            Setting to W or warn will make any unsuccessful ping be reported
            under log level WARN.
        :return:
            True: Ping successful
            False: Ping unsuccessful
    """

    host = kwargs.get("host")
    ipv6 = kwargs.get("ipv6", False)
    count = kwargs.get("count", 5)
    option = kwargs.get("option")
    timeout = kwargs.get("timeout", 30)
    interval = kwargs.get("interval", 10)
    negative = kwargs.get("negative", False)
    fail_ok = kwargs.get("fail_ok", 'error')
    acceptable_packet_loss = kwargs.get("acceptable_packet_loss", 0)
    operating_sys = platform.system()
    # Ping should exit in a timely manner
    if count > 4:
        deadline = count + 1
    else:
        deadline = 6

    while timeout >= 0:
        if re.search(r'windows', operating_sys, re.I):
            if option:
                ping_cmd = "ping -n %s %s %s" % (count, option, host)
            else:
                ping_cmd = "ping -n %s %s" % (count, host)
        else:
            if ipv6:
                version = "ping6"
            else:
                version = "ping"
            if option:
                ping_cmd = [version, host, '-nc %s -w %s %s' % (count,
                                                                deadline,
                                                                option)]
            else:
                ping_cmd = [version, host, '-nc %s -w %s' % (count, deadline)]

        shell_needed = True if operating_sys == 'Windows' else False
        ping_hndl = subprocess.Popen(ping_cmd, shell=shell_needed, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = ping_hndl.communicate()
        ping_result = out.decode()
        ping_error = ''
        if error:
            ping_error = error.decode()

        timeout = timeout - interval
        result = False
        if re.search(r'unknown host|could not find host', ping_error, re.I):
            logging.error(msg="Cannot resolve hostname: %s" % host)
            return False
        elif not re.search(r'round trip times|rtt\s+.*min', ping_result, re.I):
            if negative:
                logging.info(msg="Success: %s is unreachable" % host)
                return True
            elif timeout < 0:
                if re.search(r'^w', fail_ok, re.I):
                    logging.warning(msg="%s not responding to ping" % host)
                elif re.search(r'^i', fail_ok, re.I):
                    logging.info(msg="%s not responding to ping" % host)
                else:
                    logging.error(msg="%s not responding to ping" % host)
                return False
            else:
                logging.debug(msg="Ping output was: %s" % ping_result)
                if re.search(r'^i', fail_ok, re.I):
                    logging.info(msg="%s : not responding to ping, "
                                 "trying again" % host)
                else:
                    logging.warning(msg="%s : not responding to ping, "
                                    "trying again" % host)
                # PR1032318
                time.sleep(interval)
        else:
            # Ping succeeded
            match = re.search(r'(\d+)%\s+(loss|packet loss)',
                              ping_result, re.I)
            if int(match.group(1)) > int(acceptable_packet_loss):
                result = False
            else:
                result = True
            if negative:
                if timeout < 0:
                    logging.debug(msg="Ping output was: %s" % ping_result)
                    if re.search(r'^i', fail_ok, re.I):
                        logging.info(msg="Failure: Could ping %s" % host)
                    elif re.search(r'^w', fail_ok, re.I):
                        logging.warning(msg="Failure: Could ping %s" % host)
                    else:
                        logging.error(msg="Failure: Could ping %s" % host)
                    return False
                else:
                    logging.debug(msg="Ping output was: %s" % ping_result)
                    if re.search(r'^i', fail_ok, re.I):
                        logging.info(msg="Could ping %s, trying again"
                                     % host)
                    else:
                        logging.warning(msg="Could ping %s, trying again"
                                        % host)
                    time.sleep(interval)
            else:
                logging.debug(msg="Ping output was: %s" % ping_result)
    if 'result' in locals():
        return result

def narrow_ip(ipaddr, with_prefix=False):
    """Transit normalize IP to simple IP

    Most time used for IPv6 like below:

    +   ipaddr="2000:0101:1000:0000:0000:0000:0:8/96", with_prefix=False    => '2000:101:1000::8'
    +   ipaddr="2000:0101:1000::8/96", with_prefix=True                     => '2000:101:1000::8/96'
    +   ipaddr="192.168.010.008/24", with_prefix=False                      => '192.168.10.8'
    +   ipaddr="192.168.010.008/255.255.255.0", with_prefix=True            => '192.168.10.8/24'

    :params BOOL with_prefix:
        *OPTIONAL* return string whether include netmask

    :return:
        Return string like above sample
    """
    if with_prefix is True:
        return str(IPNetwork(ipaddr))

    return str(IPNetwork(ipaddr).ip)

def get_broadcast_ip(ipaddr):
    """Return subnet broadcast address

    +   ipaddr="2000:121:11:11::3/96"       => 2000:121:11:11::ffff:ffff
    +   ipaddr="192.168.1.0/24"             => 192.168.1.255

    :param IP|NETWORK ipaddr:
        **REQUIRED**    network address

    :return:
        return a string
    """
    return str(IPNetwork(ipaddr).broadcast)


def generate_ipaddr(ip, count, step=1, with_mask=False):
    """Generate ip address based on the count and step.
    Works with both ipv4 and ipv6 versions
    :params ip(string):
        **REQUIRED**  pass either ipv4 or ipv6 with netmask as the base address to start with
    :params count(string/integer):
        **REQUIRED**  pass how many ip address need to generate
    :params step(string/interger):
        *OPTIONAL*  default is 1, step increment for each ip address
    :params with_mask(bool):
        *OPTIONAL*  default is False,
                    if True return ip address with mask otherwise reutn ip address without mask
    :return:
        Return list of ip address

    Example::
        Python -
        ip_list = generate_ipaddr('1.0.0.1/24', 3)
        above call return ['1.0.0.1', '1.0.1.1', '1.0.2.1']

        ip_list = generate_ipaddr('1000::/112', 3)
        above call  return ['1000::0:1', '1000::1:1', '1000::2:1']

        ip_list = generate_ipaddr('1.0.0.1/24', 3, with_mask=True)
        above call  return ['1.0.0.1/24', '1.0.1.1/24', '1.0.2.1/24']

        ip_list = generate_ipaddr('1000::/112', 3, with_mask=True)
        above call  return ['1000::0:1/112', '1000::1:1/112', '1000::2:1/112']

        ROBOT -
        ip_list = Generate IPaddr   '1.0.0.1/32'  4
        will return  ['1.0.0.1', '1.0.0.2', '1.0.0.3', '1.0.0.4']

        ip_list = Generate IPaddr   '1.0.0.1/32'  4  with_mask=${True}
        will return  ['1.0.0.1/32', '1.0.0.2/32', '1.0.0.3/32', '1.0.0.4/32']
    """
    i = 1
    ip_list = []
    while i <= int(count):
        if with_mask:
            ip_list.append(ip)
        else:
            ip_list.append(strip_mask(ip))
        ip = incr_ip_subnet(ip, step=int(step))
        i = i+1
    return ip_list
