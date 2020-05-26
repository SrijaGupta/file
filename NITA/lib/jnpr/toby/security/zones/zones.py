"""
Configure security zone
"""

__author__ = ['Sasikumar Sekar']
__contact__ = 'sasik@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_zone(zone=None, device=None, interface=None, host_inbound_traffic=False,
                   system_service=None, protocol=None, address=None,
                   address_book=False, address_set=None, ip_prefix=None, dns_name=None,
                   range_address_low=None, range_address_high=None,
                   wildcard_address=None, commit=False):
    """
    Configure security zone

    :Example:

    python: configure_zone(zone="trust", device=router_handle, interface=ge-0/0/1)

    robot:

    Configure Zone    device=${dh}    zone=trust
    Configure Zone    device=${dh}    zone=trust    interface=ge-0/0/1
    Configure Zone    device=${dh}    zone=trust    interface=ge-0/0/1
        host_inbound_traffic=${True}    system_service=all
    Configure Zone    device=${dh}    zone=trust    interface=ge-0/0/1
        host_inbound_traffic=${True}    protocol=all
    Configure Zone    device=${dh}    zone=trust    host_inbound_traffic=${True}
        system_service=${service}
    Configure Zone    device=${dh}    zone=trust    host_inbound_traffic=${True}
        protocol=${protocol}
    Configure Zone    device=${dh}    zone=trust    address_book=${True}
        address=trust_a_v4_spec_0    ip_prefix=10.0.0.1/32
    Configure Zone    device=${dh}    zone=trust    address_book=${True}
        address=trust_a_v4_spec_0    ip_prefix=2006::1/64
    Configure Zone    device=${dh}    zone=trust    address_book=${True}
        address=trust_a_v4_spec_0    dns_name=google.com
    Configure Zone    device=${dh}    zone=trust    address_book=${True}
        address=trust_a_v4_spec_0    range_address_low=1.1.1.1    range_address_high=1.1.1.5
    Configure Zone    device=${dh}    zone=trust    address_book=${True}
        address=trust_a_v4_spec_0    wildcard_address=1.1.1.5
    Configure Zone    device=${dh}    zone=trust    address_book=${True}
        address_set=trust_a_addset_v4    address=trust_a_v4_spec_0

    :param str zone:
        **REQUIRED** security-zone name. Ex. name = "Trust"
    :param Device device:
        **REQUIRED** device handler
    :param str interface:
        *OPTIONAL* interface name from device to host. Ex. ge-0/0/1
    :param bool host_inbound_traffic:
        **REQUIRED** Allowed system services & protocols. Default is False
    :param str system_service:
        *OPTIONAL* provide valid system service.
    :param str protocol:
        *OPTIONAL* provide valid protocol.
    :param bool address_book:
        **REQUIRED** Address book entries. Default is False
    :param str address:
        *OPTIONAL* Define a security address
    :param str address_set:
        *OPTIONAL* Define a security address set
    :param str ip_prefix:
        *OPTIONAL* Numeric IPv4 or IPv6 address with prefix
    :param str dns_name:
        *OPTIONAL* DNS address name
    :param str range_address_low:
        *OPTIONAL* Lower limit of address range
    :param str range_address_high:
        *OPTIONAL* Upper limit of address range
    :param str wildcard_address:
        *OPTIONAL* Numeric IPv4 wildcard address with in the form of a.d.d.r/netmask
    :param bool commit:
	    *OPTIONAL* provide if commit is needed. Ex. default = "False"

    :return:
        * ``True`` when zone configuration is committed
    :raises Exception: when mandatory parameter is missing
    """

    if zone is None:
        device.log(level="ERROR", msg="'zone' is mandatory parameter for configuring basic zones")
        raise Exception("'zone' is mandatory parameter for configuring basic zones")

    if device is None:
        raise Exception("'device' is mandatory parameter device handle")

    if zone is not None and device is not None:
        cmd = 'set security zones security-zone ' + zone

    if address_book or address_set is not None:

        if address_book:
            cmd = cmd + ' address-book '

        if address_set is not None:
            cmd = cmd + ' address-set ' + address_set
        if address is not None:
            cmd = cmd + ' address ' + address

        if ip_prefix is not None:
            cmd = cmd + ' ' + ip_prefix

        if dns_name is not None:
            cmd = cmd + ' dns-name ' + dns_name

        if range_address_low is not None and range_address_high is not None:
            cmd = cmd + ' range-address ' + range_address_low + ' to ' + range_address_high

        if wildcard_address is not None:
            cmd = cmd + ' wildcard-address ' + wildcard_address

        device.config(command_list=[cmd])
    else:

        if interface is not None:
            cmd = cmd + ' interfaces ' + interface

        device.config(command_list=[cmd])

        if host_inbound_traffic:
            cmd = cmd + ' host-inbound-traffic '

        if system_service is not None:
            if isinstance(system_service, list):
                for temp in system_service:
                    device.config(command_list=[cmd + ' system-services ' + temp])
            else:
                device.config(command_list=[cmd + ' system-services ' + system_service])

        if protocol is not None:
            if isinstance(protocol, list):
                for temp in protocol:
                    device.config(command_list=[cmd + ' protocols ' + temp])
            else:
                device.config(command_list=[cmd + ' protocols ' + protocol])


    if commit is True:
        return device.commit(timeout=60)
    else:
        return True
