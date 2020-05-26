"""
BBE Keywords exposed for BBE Engine in Toby
"""
from time import sleep
import yaml
from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil
from jnpr.toby.bbe.radius.freeradius import FreeRadius
from jnpr.toby.bbe.radius.valid8 import Valid8
import jnpr.toby.bbe.cst.cstutils as cst


#######################
# Subscriber Keywords #
#######################


def start_clients(**kwargs):
    """
    BBE start clients, verify tester count and subscriber count
    :param kwargs:
    subs:                     subscriber object list that is used to start
    login_retries:            retry times, default is 10
    restart_unbound_only:     True/False, by default is false, restart unbounded clients only
    stablize_time:            stable time after subs login
    device_id:                router resource name list to collect the client info
    check_access_route:       True/False, default is True
    verify_router:            True/False, default is true, verify the client number and access route count
    :return:
    """
    return cst.cst_start_clients(check_cpu=False, **kwargs)


def stop_clients(**kwargs):
    """
    BBE release client, it verify the client in tester and router
    :param kwargs:
    subs:           bbe subscriber object list
    device_id:      router_id, eg. 'r0', default is an id list of duts
    verify_router:  True/False, default is True, check access route and client count after release
    logout_retry:   retry waiting iteration, default is 20
    :return:
    """
    return cst.cst_release_clients(**kwargs)


def get_subscriber_handle(**kwargs):
    """
    Return the BBE subscriber handle(s) for the requested arguments
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param protocol: optional, string, subscriber protocol, e.g., 'dhcp, 'pppoe'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    :param family: optional, string. Supported values -- 'ipv4', 'ipv6', 'dual'
    :return: A list of subscriber handles
    """
    return bbe.get_subscriber_handles(**kwargs)


def subscriber_action(subscriber_handle, action):
    """
    Perform the requested action on the passed in subscriber object
    :param subscriber_handle: subcriber handle to perform action
    :param action: action to perform
    :return:
    """
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscriber_handle:
        if subscriber.rt_dhcpv6_handle:
            rthandle.invoke('client_action', handle=subscriber.rt_dhcpv6_handle, action=action)
        elif hasattr(subscriber, 'rt_dhcpv4_handle'):
            rthandle.invoke('client_action', handle=subscriber.rt_dhcpv4_handle, action=action)
        elif hasattr(subscriber, 'rt_pppox_handle'):
            rthandle.invoke('client_action', handle=subscriber.rt_pppox_handle, action=action)


def login_subscribers(subscriber_handle):
    """
    Login the subscribers on the requested handle
    :param subscriber_handle: subcriber handle to perform action
    :return:
    """
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscriber_handle:
        if subscriber.rt_dhcpv6_handle:
            rthandle.invoke('client_action', handle=subscriber.rt_dhcpv6_handle, action='start')
        elif hasattr(subscriber, 'rt_dhcpv4_handle'):
            rthandle.invoke('client_action', handle=subscriber.rt_dhcpv4_handle, action='start')
        elif hasattr(subscriber, 'rt_pppox_handle'):
            rthandle.invoke('client_action', handle=subscriber.rt_pppox_handle, action='start')


def logout_subscribers(subscriber_handle):
    """
    Logout the subsribers on the requested handle
    :param subscriber_handle: subcriber handle to perform action
    :return:
    """
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscriber_handle:
        if subscriber.rt_dhcpv6_handle:
            rthandle.invoke('client_action', handle=subscriber.rt_dhcpv6_handle, action='stop')
        elif hasattr(subscriber, 'rt_dhcpv4_handle'):
            rthandle.invoke('client_action', handle=subscriber.rt_dhcpv4_handle, action='stop')
        elif hasattr(subscriber, 'rt_pppox_handle'):
            rthandle.invoke('client_action', handle=subscriber.rt_pppox_handle, action='stop')


def restart_unbound_subscribers(subscriber_handle):
    """
    Restart the unbound subscribers on the requested handle
    :param subscriber_handle: subcriber handle to perform action
    :return:
    """
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscriber_handle:
        if subscriber.rt_dhcpv6_handle:
            rthandle.invoke('client_action', handle=subscriber.rt_dhcpv6_handle, action='restart_down')
        elif hasattr(subscriber, 'rt_dhcpv4_handle'):
            rthandle.invoke('client_action', handle=subscriber.rt_dhcpv4_handle, action='restart_down')
        elif hasattr(subscriber, 'rt_pppox_handle'):
            rthandle.invoke('client_action', handle=subscriber.rt_pppox_handle, action='restart_down')


def get_configured_subscriber_count(**kwargs):
    """
    Returns the total number of requested subcribers configured in BBE config
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param protocol: optional, string, subscriber protocol, e.g., 'dhcp, 'pppoe'
    :param tag: optional, string, subscriber group tag.
    :param ri: optional, string, routing instance name
    :param family: optional, string, Supported values -- 'ipv4', 'ipv6', 'dual'
    :return: integer count
    """
    return bbe.get_configured_subscribers_count(**kwargs)


def match_subscriber_attribute(device_name, client_type, attribute, attribute_value):
    """
    match_subscriber_attribute can be used to match any attribute listed in
    show subscriber client-type <client-type> CLI output. attribute_value
    should be a list to  accommodate possibilities of having
    more than 1 subscriber

    param device_name: device id (e.g. r0)
    param client_type: client type (e,g. dhcp,l2tp,ppp,vlan)
    param attribute: attribute to be checked (e,g. user-name)
    param attribute_value: List of values to be matched.


    Example:
    attribute_value =["DEFAULTUSER1","DEFAULTUSER2"]
    Match Subscriber Attribute =device0  dhcp  user-name   attribute_value

    :return: True if the all he values in attibute_values match
    raise Exception if values dont match
    """

    router = t.get_handle(resource=device_name)
    if isinstance(attribute_value, (str)):
        attribute_value = [attribute_value]
    elif isinstance(attribute_value, (list, tuple)):
        attribute_value = attribute_value
    rpc_str = router.get_rpc_equivalent(command="show subscribers client-type {0}".format(client_type))
    resp = router.execute_rpc(command=rpc_str)
    output = resp.response()
    temp_value = output.findall("subscriber/{0}".format(attribute))
    actual_value = list()
    for temp in temp_value:
        actual_value.append(temp.text)

    attribute_value.sort()
    actual_value.sort()
    if attribute_value != actual_value:
        raise Exception("Values for attribute  dont match , Expected value\
                        : {0}, Actual Value : {1}".format(attribute_value, actual_value))

    t.log("Correct Value for attribute found, Expected Value : {0}\
           Actaul Value : {1}".format(attribute_value, actual_value))

    return True


#################
# Ixia Keywords #
#################

def start_all_protocols():
    """This function is deprecated. Please use bbe_start_all_protocols."""

    _bbe_issue_deprecated_mesg(start_all_protocols.__name__)
    bbe_start_all_protocols()


def bbe_start_all_protocols():
    """
    Starts all emulations on the tester
    :return:
    """
    rthandle = t.get_handle(resource='rt0')
    rthandle.invoke('start_all')


def stop_all_protocols():
    """This function is deprecated. Please use bbe_stop_all_protocols."""

    _bbe_issue_deprecated_mesg(stop_all_protocols.__name__)
    bbe_stop_all_protocols()


def bbe_stop_all_protocols():
    """
    stops all emulations on the tester
    :return:
    """
    rthandle = t.get_handle(resource='rt0')
    rthandle.invoke('stop_all')


def bbe_get_interfaces(rtid='rt0', **kwargs):
    """Get RT Interface Object

    :param rtid: 'rt0'
    :return: instance of interface obj
    """
    return bbe.get_interfaces(rtid, **kwargs)


#################
# DHCP Keywords #
#################

def get_configured_dhcp_client_count(**kwargs):
    """
    Returns the total number of DHCP subcribers configured in BBE config
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag.
    :param ri: optional, string, routing instance name
    :param family: optional, string, Supported values -- 'ipv4', 'ipv6', 'dual'
    :return: The configured dhcp client count in the bbe object based on the supplied args
    """
    kwargs['protocol'] = 'dhcp'
    return bbe.get_configured_subscribers_count(**kwargs)


def get_dhcp_client_count(device='r0'):
    """
    Returns the current number of dhcp clients on router
    :param device: device string to query for subcriber counts (DEFAULT: r0)
    :return: number of DHCP subscribers on device
    """
    # set the handle of the router you want to query
    BBEJunosUtil.router_handle = t.get_handle(resource=device)

    return BBEJunosUtil.get_dhcp_subscriber_count()


def verify_dhcp_client_count(expected_count, device='r0'):
    """
    Verifies the number of DHCPv4 subscribers bound on the DUT matches the expected_count passed
    :param expected_count: the expected count of subscribers
    :param device: device string to query for subcriber counts (DEFAULT: r0)
    :return: exception if expected_count doesn't match the router count
    """
    expected_count = int(expected_count)

    # set the handle of the router you want to query
    BBEJunosUtil.router_handle = t.get_handle(resource=device)

    count = BBEJunosUtil.get_dhcp_subscriber_count()
    t.log('info', 'expected_count:{0}, count.active:{1}'.format(expected_count, count.active))
    if expected_count != count.active:
        raise Exception('{0} of {1} expected DHCP subscribers are bound'.format(count.active, expected_count))

    t.log('info', '{0} of {1} expected DHCP subscribers are bound'.format(count.active, expected_count))

    return True


def login_all_dhcpv4_clients(**kwargs):
    """
    login all DHCPv4 clients
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'dhcp'
    kwargs['family'] = 'ipv4'

    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        rthandle.invoke('dhcp_client_action', handle=subscriber.rt_dhcpv4_handle, action='start')


def logout_all_dhcpv4_clients(**kwargs):
    """
    release all DHCPv4 clients
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'dhcp'
    kwargs['family'] = 'ipv4'

    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        rthandle.invoke('dhcp_client_action', handle=subscriber.rt_dhcpv4_handle, action='stop')


def restart_all_unbound_dhcpv4_clients(**kwargs):
    """
     restart all unbound DHCPv4 clients
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'dhcp'
    kwargs['family'] = 'ipv4'

    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        rthandle.invoke('dhcp_client_action', handle=subscriber.rt_dhcpv4_handle, action='restart_down')


def login_all_dhcpv6_clients(**kwargs):
    """
    login all DHCPv6 clients
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'dhcp'
    kwargs['family'] = 'ipv6'

    # Get the RT handle
    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        # only if the subscriber is stacked on a PPPoE emulation
        # PPP handle looks like: /topology:1/deviceGroup:2/ethernet:1/pppoxclient:1/dhcpv6client:1
        if 'pppoxclient' not in subscriber.rt_dhcpv6_handle:
            rthandle.invoke('dhcp_client_action', handle=subscriber.rt_dhcpv6_handle, action='start')


def logout_all_dhcpv6_clients(**kwargs):
    """
    logout all DHCPv6 clients
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'dhcp'
    kwargs['family'] = 'ipv6'

    # Get the RT handle
    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        # only if the subscriber is NOT stacked on a PPPoE emulation.
        # PPP handle looks like: /topology:1/deviceGroup:2/ethernet:1/pppoxclient:1/dhcpv6client:1
        if 'pppoxclient' not in subscriber.rt_dhcpv6_handle:
            rthandle.invoke('dhcp_client_action', handle=subscriber.rt_dhcpv6_handle, action='stop')


def restart_all_unbound_dhcpv6_clients(**kwargs):
    """
     restart all unbound DHCPv6 clients
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'dhcp'
    kwargs['family'] = 'ipv6'

    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        # only if the subscriber is NOT stacked on a PPPoE emulation.
        # PPP handle looks like: /topology:1/deviceGroup:2/ethernet:1/pppoxclient:1/dhcpv6client:1
        if 'pppoxclient' not in subscriber.rt_dhcpv6_handle:
            rthandle.invoke('dhcp_client_action', handle=subscriber.rt_dhcpv6_handle, action='restart_down')


def bbe_get_rt_dhcp_server(family='ipv4'):
    """Get RT DHCP server instance

    :param family: 'ipv4' or 'ipv6'.
    :return: instance of either RT
    """
    return bbe.get_rt_dhcp_server(family)


##################
# PPPoE Keywords #
##################

def get_configured_pppoe_client_count(**kwargs):
    """
    Returns the total number of PPPoE subcribers configured in BBE config
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag.
    :param ri: optional, string, routing instance name
    :param family: optional, string, Supported values -- 'ipv4', 'ipv6', 'dual'
    :return: The configured pppoe client count in the bbe object based on the supplied args
    """
    kwargs['protocol'] = 'pppoe'
    return bbe.get_configured_subscribers_count(**kwargs)


def get_pppoe_client_count(device='r0'):
    """
    Returns the current number of pppoe clients on router
    :param device: device string to query for subcriber counts (DEFAULT: r0)
    :return: number of PPPoE subscribers on
    """
    # set the handle of the router you want to query
    BBEJunosUtil.router_handle = t.get_handle(resource=device)

    return BBEJunosUtil.get_pppoe_subscriber_count()


def verify_pppoe_client_count(expected_count, device='r0'):
    """
    Verify the number of subscrobers on device are the expected_count
    :param expected_count: the expected count of subscribers
    :param device: device string to query for subcriber counts
    :return: exception if expected_count doesn't match the router count
    """

    expected_count = int(expected_count)

    # set the handle of the router you want to query
    BBEJunosUtil.router_handle = t.get_handle(resource=device)

    # Get the stats off the router
    count = BBEJunosUtil.get_pppoe_subscriber_count()
    t.log('info', 'expected_count:{0}, count.active:{1}'.format(expected_count, count.active))
    if expected_count != count.active:
        raise Exception('{0} of {1} expected PPPoE subscribers are active'.format(count.active, expected_count))

    t.log('info', '{0} of {1} expected PPPoE subscribers are active'.format(count, expected_count))

    return True


def login_all_pppoev4_clients(**kwargs):
    """
    login all PPPoE v4 clients on tester
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'pppoe'
    kwargs['family'] = 'ipv4'

    # Get the RT handle
    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        rthandle.invoke('pppoe_client_action', handle=subscriber.rt_pppox_handle, action='start')


def logout_all_pppoev4_clients(**kwargs):
    """
    logout all PPPoE v4 clients on tester
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'pppoe'
    kwargs['family'] = 'ipv4'

    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        rthandle.invoke('pppoe_client_action', handle=subscriber.rt_pppox_handle, action='stop')


def restart_all_unbound_pppoev4_clients(**kwargs):
    """
    restart all unbound PPPoE clients
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'pppoe'
    kwargs['family'] = 'ipv4'

    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        rthandle.invoke('pppoe_client_action', handle=subscriber.rt_pppox_handle, action='restart_down')


def login_all_pppoev6_clients(**kwargs):
    """
    login all DHCPv6 clients on top of the PPPoE session
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'pppoe'
    kwargs['family'] = 'ipv6'
    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        if 'pppoxclient' in subscriber.rt_dhcpv6_handle  or 'dhcpv6pdblockconfig' in subscriber.rt_dhcpv6_handle:
            rthandle.invoke('pppoe_client_action', handle=subscriber.rt_dhcpv6_handle, action='start')


def logout_all_pppoev6_clients(**kwargs):
    """
    logout all DHCPv6 clients on top of the PPPoE session
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'pppoe'
    kwargs['family'] = 'ipv6'

    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        if 'pppoxclient' in subscriber.rt_dhcpv6_handle or 'dhcpv6pdblockconfig' in subscriber.rt_dhcpv6_handle:
            rthandle.invoke('pppoe_client_action', handle=subscriber.rt_dhcpv6_handle, action='stop')


def restart_all_unbound_pppoev6_clients(**kwargs):
    """
    restart all unbound DHCPv6 clients on top of the PPPoE session
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """
    kwargs['protocol'] = 'dhcp'
    kwargs['family'] = 'ipv6'

    subscribers = bbe.get_subscriber_handles(**kwargs)
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        # only if the subscriber is NOT stacked on a PPPoE emulation.
        # PPP handle looks like: /topology:1/deviceGroup:2/ethernet:1/pppoxclient:1/dhcpv6client:1
        if 'pppoxclient' not in subscriber.rt_dhcpv6_handle:
            rthandle.invoke('dhcp_client_action', handle=subscriber.rt_dhcpv6_handle, action='restart_down')


#################
# L2TP Keywords #
#################

def verify_l2tp_client_count(expected_count, device='r0'):
    """
    Verify the number of L2TP subscrobers on device are the expected_count
    :param expected_count: the expected count of subscribers
    :param device: device string to query for subcriber counts
    :return: exception if expected_count doesn't match the router count
    """

    expected_count = int(expected_count)

    # set the handle of the router you want to query
    BBEJunosUtil.router_handle = t.get_handle(resource=device)

    # Get the stats off the router
    count = BBEJunosUtil.get_l2tp_subscriber_count()
    t.log('info', 'expected_count:{0}, count.active:{1}'.format(expected_count, count.active))
    if expected_count != count.active:
        raise Exception('{0} of {1} expected L2TP subscribers are active'.format(count.active, expected_count))

    t.log('info', '{0} of {1} expected L2TP subscribers are active'.format(count, expected_count))

    return True


def login_all_l2tp_clients(protocol='l2tp', family='ipv4', rtid='rt0', **kwargs):
    """
    login all l2tp clients on tester
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """

    # Get the RT handle
    subscribers = bbe.get_subscriber_handles(protocol=protocol, family=family, **kwargs)
    rthandle = t.get_handle(resource=rtid)
    for subscriber in subscribers:
        rthandle.invoke('l2tp_client_action', handle=subscriber.rt_pppox_handle, action='start')


def logout_all_l2tp_clients(protocol='l2tp', family='ipv4', rtid='rt0', **kwargs):
    """
    logout all PPPoE v4 clients on tester
    :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
    :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
    for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
    :param ri: optional, string, routing instance name
    """

    subscribers = bbe.get_subscriber_handles(protocol=protocol, family=family, **kwargs)
    rthandle = t.get_handle(resource=rtid)
    for subscriber in subscribers:
        rthandle.invoke('pppoe_client_action', handle=subscriber.rt_pppox_handle, action='stop')

#################
# ANCP Keywords #
#################


def flap_all_ancp_sublines(rt_handle, action='flap_start'):
    """
    flap all ancp lines on the requested rt, default action is flap_start
    :param rt_handle: rt handle to perform action; action: flap_start or flap_stop
    :return:
    """

    subscribers = bbe.get_subscriber_handles()
    for subscriber in subscribers:
        if subscriber.has_ancp:
            rt_handle.invoke('emulation_ancp_control', ancp_subscriber=subscriber.rt_ancp_line_handle, action=action)


def get_ancp_neighbor_count(device, neighbor_status='established'):
    """Get ancp neighbor count

    :param device: device name, configured/establishing/established/not-established/total-status;
                                default is established neighobr state
    :return: ancp neighbor count
    """

    router_handle = t.get_handle(resource=device)
    rpc_cmd = '<get-ancp-neighbor-summary></get-ancp-neighbor-summary>'
    resp = router_handle.execute_rpc(command=rpc_cmd).resp

    return resp.findtext('ancp-neighbors-summary/ancp-{0}-status-nbr-summary'.format(neighbor_status))


def get_ancp_subscriber_count(device, subline_status='total'):
    """Get ancp subscribers count

    :param device: device name, total/show-time/idle/silent/unknown; default is show-time subscriber state
    :return: ancp subscriber count
    """

    router_handle = t.get_handle(resource=device)
    rpc_cmd = '<get-ancp-subscriber-summary></get-ancp-subscriber-summary>'
    resp = router_handle.execute_rpc(command=rpc_cmd).resp

    return resp.findtext('ancp-subscribers-summary/ancp-{0}-status-subscr-summary'.format(subline_status))


###################
# RADIUS Keywords #
###################


def init_radius_server(radius_server):
    """
    Initialize FreeRadius for the server
    :param radius_server: Toby object to Linux host running RADIUS
    :return: FreeRADIUS object

    example:
    ${radius_server} =    Get handle    resource=h0
    ${radius_server} =    Init Radius Server  ${radius_server}
    """

    return FreeRadius(dev_handle=radius_server)


def add_radius_client(radius_server, client_ip='100.0.0.1', secret='joshua', commit=True, new=True, **kwargs):
    """
    Add a RADIUS client to the radius server with the supplied parameters
    :param radius_server: Toby object to the Linux host running RADIUS
    :param client_ip: IP address of the RADIUS client. Typically the loopback address of the DUT (DEFAULT: 100.0.0.1)
    :param secret:  Shared password between RADIUS server and RADIUS client (DEFAULT: joshua)
    :param commit:  Commmit the config to the RADIUS server
    :param new:  Create a new file on the RADIUS server or append to existing file (DEFAULT: True)
    :param kwargs:
    :return:
    """

    radius_server.add_radius_client(client=client_ip, secret=secret, short_name=kwargs['client_name'], \
                                    commit=commit, new=new)


def delete_radius_client(radius_server, client):
    """
    delete a radius client
    :param radius_server:       Toby object to the Linux host running RADIUS
    :param client:              client name(short name)
    :return:
    """
    radius_server.delete_radius_client(client)


def add_radius_user(radius_server, user, request_avp, reply_avp, commit=True, new=False):
    """
    :param radius_server: Toby object to the Linux host running RADIUS
    :param user: Username of the user being added
    :param request_avp: String with request AVP for the RADIUS user
    :param reply_avp: String with reply AVP for the RADIUS user
    :param commit: Commmit the config to the RADIUS server
    :param new: Create a new file on the RADIUS server or append to existing file (DEFAULT: True)
    :return:
    """

    radius_server.add_radius_user(user=user, request_avp=request_avp, reply_avp=reply_avp, commit=commit, new=new)


def delete_radius_user(radius_server, user):
    """
    :param radius_server: Toby object to the Linux host running RADIUS
    :param user: Username of the user being deleted
    :return:
    """
    radius_server.delete_radius_user(user)


def commit_radius_user(radius_server, new=False):
    """
    Commit Users File on radius server
    :param radius_server: Toby object to the Linux host running RADIUS
    :param new: commit NEW file on radius server
    :return:
    """
    radius_server.commit_radius_user(new=new)


def modify_radius_auth(radius_server, auth_order):
    """

    :param radius_server:   sbr radius object
    :param auth_order:      sbr auth order
    :return:
    """
    radius_server.modify_radius_auth(auth_order)


def start_radius(radius_server):
    """
    Start the radius server process on requested radius server
    :param radius_server: Toby object to the Linux host running RADIUS
    :return:
    """

    radius_server.start_radius_server()


def stop_radius(radius_server):
    """
    Stop the radius server process on requested radius server
    :param radius_server: Toby object to the Linux host running RADIUS
    :return:
    """

    radius_server.stop_radius_server()


def restart_radius(radius_server):
    """
    Restart the radius server process on requested radius server
    :param radius_server: Toby object to the Linux host running RADIUS
    :return:
    """

    radius_server.restart_radius_server()


####################
# Traffic Keywords #
####################

def add_bidirectional_dhcp_ipv4_subscriber_traffic(**kwargs):
    """
    Add IPv4 bidirectional traffic from all DHCPv4 subscribers to the uplink port
    :return:
    """
    if 'name' in kwargs:
        t.log('warn', 'You have specified the \'name\' argument when multiple streams are being created. This name '
                      'will not be retained. Instead, you can find the stream names under the list rt.traffic_item. '
                      'If the nature of your testing requires a custom stream name, please use keyword Configure '
                      'Traffic Stream')
        kwargs['name'] = ''

    subscribers = bbe.get_subscriber_handles()
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        if 'dhcp' in subscriber.protocol and 'ipv4' in subscriber.family:
            rthandle.invoke('add_traffic', type='ipv4', emulation_src_handle=subscriber.rt_dhcpv4_handle, **kwargs)


def add_bidirectional_pppoe_ipv4_subscriber_traffic(**kwargs):
    """
    Add IPv4 bidirectional traffic from all PPPoE subscribers to the uplink port
    :return:
    """
    if 'name' in kwargs:
        t.log('warn', 'You have specified the \'name\' argument when multiple streams are being created. This name '
                      'will not be retained. Instead, you can find the stream names under the list rt.traffic_item. '
                      'If the nature of your testing requires a custom stream name, please use keyword Configure '
                      'Traffic Stream')
        kwargs['name'] = ''

    subscribers = bbe.get_subscriber_handles()
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        if 'pppoe' in subscriber.protocol and 'ipv4' in subscriber.family:
            rthandle.invoke('add_traffic', type='ipv4', emulation_src_handle=subscriber.rt_pppox_handle, **kwargs)


def add_bidirectional_ipv6_subscriber_traffic(**kwargs):
    """
    Add IPv46 bidirectional traffic from subscriber to uplink port
    :return:
    """

    if 'name' in kwargs:
        t.log('warn', 'You have specified the \'name\' argument when multiple streams are being created. This name '
                      'will not be retained. Instead, you can find the stream names under the list rt.traffic_item. '
                      'If the nature of your testing requires a custom stream name, please use keyword Configure '
                      'Traffic Stream')
        kwargs['name'] = ''

    subscribers = bbe.get_subscriber_handles()
    rthandle = t.get_handle(resource='rt0')
    for subscriber in subscribers:
        rthandle.invoke('add_traffic', type='ipv6', emulation_src_handle=subscriber.rt_dhcpv6_handle, **kwargs)


def add_bidirectional_traffic_to_all_subscribers(**kwargs):
    """This function is deprecated. Please use bbe_add_bidirectional_traffic_to_all_subscribers."""

    _bbe_issue_deprecated_mesg(add_bidirectional_traffic_to_all_subscribers.__name__)
    return bbe_add_bidirectional_traffic_to_all_subscribers(**kwargs)


def bbe_add_bidirectional_traffic_to_all_subscribers(**kwargs):
    """
    Add traffic for all configured subscribers in BBEVar. Currently supports DHCP and PPPoE.

    Please note: Modifying additional **kwargs parameters within the rthandle.invoke('add_traffic', ) underlying method
    may result in unexpected behavior, since options like tcp source port, destination port, etc. would
    be unilaterally applied to  all traffic streams for all subscriber types. Please only use the arguments
    specifically shown below.

    :param kwargs:
    mesh_type:                  traffic mesh type, default is many_to_many, can be one_to_one
    dynamic_update:             dynamic_udate the address values from ppp
    frame_size:                 single value /a list [min max step]/[min max]
    ip_precedence:              ip precedence value (0-7)
    ip_dscp:                    ip dscp value

    :return:
    True                        Returns True if all traffic meshes created successfully, else raises an exception.
    False                       False is never returned since this is an exposed ROBOT keyword.
    """
    subscribers = bbe.get_subscriber_handles()
    for subscriber in subscribers:
        if 'dhcp' in subscriber.protocol and 'ipv4' in subscriber.family:
            # Add traffic for DHCPv4 emulation
            add_bidirectional_dhcp_ipv4_subscriber_traffic(**kwargs)
        elif 'dhcp' in subscriber.protocol and 'ipv6' in subscriber.family:
            # Add traffic for DHCPv6 emulation
            add_bidirectional_ipv6_subscriber_traffic(**kwargs)
        elif 'dhcp' in subscriber.protocol and 'dual' in subscriber.family:
            # Add traffic for DHCP dual stack emulation
            add_bidirectional_dhcp_ipv4_subscriber_traffic(**kwargs)
            add_bidirectional_ipv6_subscriber_traffic(**kwargs)
        elif 'pppoe' in subscriber.protocol and 'ipv4' in subscriber.family:
            # Add traffic for PPPoEv4 emulation
            add_bidirectional_pppoe_ipv4_subscriber_traffic(**kwargs)
        elif 'pppoe' in subscriber.protocol and 'ipv6' in subscriber.family:
            # Add traffic for PPPoEv6 emulation
            add_bidirectional_ipv6_subscriber_traffic(**kwargs)
        elif 'pppoe' in subscriber.protocol and 'dual' in subscriber.family:
            # Add traffic for PPPoE dual stack emulation
            add_bidirectional_pppoe_ipv4_subscriber_traffic(**kwargs)
            add_bidirectional_ipv6_subscriber_traffic(**kwargs)
        else:
            # Unrecognized protocol
            raise Exception

    return True


def edit_traffic_stream(stream_name, **kwargs):
    """This function is deprecated. Please use bbe_edit_traffic_stream."""

    _bbe_issue_deprecated_mesg(edit_traffic_stream.__name__)
    return bbe_edit_traffic_stream(stream_name, **kwargs)


def bbe_edit_traffic_stream(stream_name, **kwargs):
    """

    :param stream_name:         Name of the stream you want to edit. Required.

    :param kwargs:
    ip_precedence:              ip precedence value (0-7). CoS testers may want to use this arg
    ip_dscp:                    ip dscp value. CoS testers may want to use this arg

    rate:                       traffic rate , can be mbps, pps, percent, for example: 1000mbps, 1000pps, 100%
    frame_size:                 single value /a list [min max step]/[min max]
    track_by:                   how to track the statistics, by default is trafficItem and source/dest value pair

    emulation_src_handle:       handle of your client emulation
    source_port:                source RT port
    destination_port:           destination RT port

    type:                       traffic type "ipv4" or "ipv6"
    ipv6_traffic_class:         ipv6 traffic class value
    ipv6_traffic_class_mode:    ipv6 traffic class mode (fixed, incr,decr)

    tcp_dst_port:               tcp destination port
    tcp_dst_port_mode:          tcp dst port mode(fixed, incr, decr)
    tcp_src_port:               tcp source port
    tcp_src_port_mode:          tcp src port mode(fixed, incr, decr)

    udp_dst_port:               udp destination port
    udp_src_port:               udp source port

    :return:
    """
    try:
        bbe.bbevar
    except NameError:
        raise Exception("This is BBE Keyword edit_traffic_stream,"
                        " please use other lib if not working on BBE feature")
    if stream_name is None:
        t.log('error', 'stream_name is a required argument.')
        raise Exception

    rthandle = t.get_handle(resource='rt0')
    stream_id = None

    # Find the stream_id for the stream we want to edit, if the user specified one
    for name in rthandle.traffic_item:
        if name.endswith(stream_name):
            # Normal scenario
            kwargs['stream_id'] = name
            rthandle.invoke('add_traffic', **kwargs)
            stream_id = name
            sleep(10)
        if name.endswith(stream_name + 'v4'):
            # v4 stream (for dual stack scenario)
            kwargs['stream_id'] = name
            rthandle.invoke('add_traffic', **kwargs)
            stream_id = name
            sleep(10)
        if name.endswith(stream_name + 'v6'):
            # v4 stream (for dual stack scenario)
            kwargs['stream_id'] = name
            rthandle.invoke('add_traffic', **kwargs)
            stream_id = name
            sleep(10)

    if stream_id is None:
        t.log('error', '{0} does not match any configured stream stream names.'.format(stream_name))
        raise Exception
    else:
        t.log('info', 'Stream edited successfully!')
        return True


def configure_traffic_stream(stream_name, subscriber_tag=None, emulation_as_source=True, bidirectional=0, **kwargs):
    """This function is deprecated. Please use bbe_configure_traffic_stream."""

    _bbe_issue_deprecated_mesg(configure_traffic_stream.__name__)
    return bbe_configure_traffic_stream(stream_name, subscriber_tag, emulation_as_source, bidirectional, **kwargs)


def bbe_configure_traffic_stream(stream_name, subscriber_tag=None, emulation_as_source=True, bidirectional=0, **kwargs):
    """
    This keyword is used for flexible creation of subscriber traffic stream(s).

    Streams created for dual stack subscribers will create both IPv4 and IPv6 traffic streams. Because all streams
    must have a unique name, 'v4' or 'v6' will be appended to the respective stream_name supplied by the user.

    :param stream_name:         Name of the stream you want to create. Must be unique. Required.
    :param subscriber_tag:      BBEVar YAML tag of subscriber group you want to apply this stream to. Optional.
    :param emulation_as_source: True if emulation-to-port traffic is desired, False if port-to-emulation traffic
                                is desired. Default is True, where client emulation is the source handle.
    :param bidirectional:       If unset by user, defaults to 0. Set to 1 for bidirectional traffic stream.
    :param kwargs:
    ip_precedence:              ip precedence value (0-7). CoS testers may want to use this arg
    ip_dscp:                    ip dscp value. CoS testers may want to use this arg
    rate:                       traffic rate , can be mbps, pps, percent, for example: 1000mbps, 1000pps, 100%
    frame_size:                 single value /a list [min max step]/[min max]
    track_by:                   how to track the statistics, by default is trafficItem and source/dest value pair

    type:                       traffic type "ipv4" or "ipv6".
    ipv6_traffic_class:         ipv6 traffic class value
    ipv6_traffic_class_mode:    ipv6 traffic class mode (fixed, incr,decr)

    tcp_dst_port:               tcp destination port
    tcp_dst_port_mode:          tcp dst port mode(fixed, incr, decr)
    tcp_src_port:               tcp source port
    tcp_src_port_mode:          tcp src port mode(fixed, incr, decr)

    udp_dst_port:               udp destination port
    udp_src_port:               udp source port
    uplink:                     uplink tag, used to specify a specific uplink

    :return:
    """
    rthandle = t.get_handle(resource='rt0')
    try:
        bbe.bbevar
    except NameError:
        raise Exception("This is BBE Keyword configure_traffic_stream,"
                        " please use other lib if not working on BBE feature")
    # Default is unidirectional stream
    kwargs['bidirectional'] = bidirectional


    if stream_name is None:
        # generate a default stream name in the future
        t.log('error', 'Please specify a stream name. This identifier will allow you to edit your stream '
                       'later as needed.')
        raise Exception
    else:
        # This sets stream_name as an identifier in rthandle.traffic_items list
        # once rthandle.add_traffic() is called
        kwargs['name'] = stream_name

    # Acquire uplink ipv4/ipv6 handle
    uplink_interface = bbe.get_interfaces('rt0', interfaces='uplink0')
    if 'uplink' in kwargs:
        uplink_interface = bbe.get_interfaces('rt0', interfaces=kwargs['uplink'])  # overwrite the default uplink0 to a different uplink port
    if subscriber_tag is not None:
        subscribers = bbe.get_subscriber_handles(tag=subscriber_tag)
        for sub in subscribers:
            t.log('info', 'Creating traffic for subscribers tagged {0} in BBEVar YAML.'.format(subscriber_tag))

            if 'dhcp' in sub.protocol and 'ipv4' in sub.family:
                # Set kwargs for DHCPv4 emulation
                kwargs['type'] = 'ipv4'

                # Determine if emulation is source or destination
                if emulation_as_source:
                    kwargs['source'] = sub.rt_dhcpv4_handle
                    kwargs['destination'] = uplink_interface[0].rt_ipv4_handle
                else:
                    kwargs['destination'] = sub.rt_dhcpv4_handle
                    kwargs['source'] = uplink_interface[0].rt_ipv4_handle

                rthandle.invoke('add_traffic', **kwargs)
            elif 'dhcp' in sub.protocol and 'ipv6' in sub.family:
                # Set kwargs for DHCPv6 emulation
                kwargs['type'] = 'ipv6'

                # Determine if emulation is source or destination
                if emulation_as_source:
                    kwargs['source'] = sub.rt_dhcpv6_handle
                    kwargs['destination'] = uplink_interface[0].rt_ipv6_handle
                else:
                    kwargs['destination'] = sub.rt_dhcpv6_handle
                    kwargs['source'] = uplink_interface[0].rt_ipv6_handle

                rthandle.invoke('add_traffic', **kwargs)

            elif 'dhcp' in sub.protocol and 'dual' in sub.family:
                # Add traffic for DHCP dual stack emulation. Requires two calls to add_traffic

                # Determine if emulation is source or destination (v4)
                if emulation_as_source:
                    kwargs['source'] = sub.rt_dhcpv4_handle
                    kwargs['destination'] = uplink_interface[0].rt_ipv4_handle
                else:
                    kwargs['destination'] = sub.rt_dhcpv4_handle
                    kwargs['source'] = uplink_interface[0].rt_ipv4_handle

                kwargs['type'] = 'ipv4'
                kwargs['name'] = stream_name + 'v4'
                rthandle.invoke('add_traffic', **kwargs)      # Generate v4 stream

                # Determine if emulation is source or destination (v6)
                if emulation_as_source:
                    kwargs['source'] = sub.rt_dhcpv6_handle
                    kwargs['destination'] = uplink_interface[0].rt_ipv6_handle
                else:
                    kwargs['destination'] = sub.rt_dhcpv6_handle
                    kwargs['source'] = uplink_interface[0].rt_ipv6_handle

                kwargs['type'] = 'ipv6'
                kwargs['name'] = stream_name + 'v6'
                rthandle.invoke('add_traffic', **kwargs)      # Generate v6 stream


            elif 'pppoe' in sub.protocol and 'ipv4' in sub.family:
                # Set kwargs for PPPoEv4 emulation
                kwargs['type'] = 'ipv4'

                # Determine if emulation is source or destination
                if emulation_as_source:
                    kwargs['source'] = sub.rt_pppox_handle
                    kwargs['destination'] = uplink_interface[0].rt_ipv4_handle
                else:
                    kwargs['destination'] = sub.rt_pppox_handle
                    kwargs['source'] = uplink_interface[0].rt_ipv4_handle

                rthandle.invoke('add_traffic', **kwargs)

            elif 'pppoe' in sub.protocol and 'ipv6' in sub.family:
                # Set kwargs for PPPoEv6 emulation
                kwargs['type'] = 'ipv6'

                # Determine if emulation is source or destination
                if emulation_as_source:
                    kwargs['source'] = sub.rt_dhcpv6_handle
                    kwargs['destination'] = uplink_interface[0].rt_ipv6_handle
                else:
                    kwargs['destination'] = sub.rt_dhcpv6_handle
                    kwargs['source'] = uplink_interface[0].rt_ipv6_handle

                rthandle.invoke('add_traffic', **kwargs)

            elif 'pppoe' in sub.protocol and 'dual' in sub.family:
                # Set kwargs for PPPoE dual stack emulation

                # Determine if emulation is source or destination (v4)
                if emulation_as_source:
                    kwargs['source'] = sub.rt_pppox_handle
                    kwargs['destination'] = uplink_interface[0].rt_ipv4_handle
                else:
                    kwargs['destination'] = sub.rt_pppox_handle
                    kwargs['source'] = uplink_interface[0].rt_ipv4_handle

                kwargs['type'] = 'ipv4'
                kwargs['name'] = stream_name + 'v4'
                rthandle.invoke('add_traffic', **kwargs)

                # Determine if emulation is source or destination (v6)
                if emulation_as_source:
                    kwargs['source'] = sub.rt_dhcpv6_handle
                    kwargs['destination'] = uplink_interface[0].rt_ipv6_handle
                else:
                    kwargs['destination'] = sub.rt_dhcpv6_handle
                    kwargs['source'] = uplink_interface[0].rt_ipv6_handle

                kwargs['type'] = 'ipv6'
                kwargs['name'] = stream_name + 'v6'
                rthandle.invoke('add_traffic', **kwargs)
            else:
                # Unrecognized protocol
                t.log('error', 'Unrecognized subscriber protocol/family. Could not create traffic stream.')
                raise Exception

    # Sleep for 30s following setup of initial traffic item. First traffic item takes longer to setup than others
    if len(rthandle.traffic_item) is 1:
        t.log('info', 'Sleeping after setup of first traffic item')
        sleep(30)

    return True


def perform_traffic_stream_action(action, stream_name=None, **kwargs):
    """This function is deprecated. Please use bbe_perform_traffic_stream_action."""

    _bbe_issue_deprecated_mesg(perform_traffic_stream_action.__name__)
    return bbe_perform_traffic_stream_action(action, stream_name, **kwargs)


def bbe_perform_traffic_stream_action(action, stream_name=None, **kwargs):
    """
    Performs common actions on a chosen traffic stream

    :param stream_name:          The configured stream you want to modify
           timeout:              max_wait_timer
    :param action:               Valid actions are start/stop/delete/poll/regenerate/apply/clearstats/reset

    :return:
    True                         True only if rthandle.traffic_action() is executed
    False                        Never returns false. Only raises an exception in error scenarios.
    """
    try:
        bbe.bbevar
    except NameError:
        raise Exception("This is BBE Keyword perform_traffic_stream_action,"
                        " please use other libs if not working on BBE feature")
    rthandle = t.get_handle(resource='rt0')
    stream_id = None

    # Perform stream action on ALL configured streams
    if stream_name is None:
        t.log('info', 'Because \'stream_name\' parameter is set to None, desired action {0} will be performed on all'
                      ' configured streams. If this is not your intention, please specify a valid stream'
                      ' name.'.format(action))

        for stream in rthandle.traffic_item:
            t.log('info', 'Performing {0} action on following traffic item: {1}'.format(action, stream))
            rthandle.invoke('traffic_action', handle=stream, action=action, **kwargs)
            sleep(5)
        return True

    # Find the stream_id for the stream we want to edit. This flow assumes the user specified a stream name
    for name in rthandle.traffic_item:
        if name.endswith(stream_name):
            stream_id = name
            rthandle.invoke('traffic_action', handle=stream_id, action=action, **kwargs)
        if name.endswith(stream_name + 'v4'):
            # v4 stream (for dual stack scenario)
            stream_id = name
            rthandle.invoke('traffic_action', handle=stream_id, action=action, **kwargs)
            sleep(10)
        if name.endswith(stream_name + 'v6'):
            # v4 stream (for dual stack scenario)
            stream_id = name
            rthandle.invoke('traffic_action', handle=stream_id, action=action, **kwargs)
            sleep(10)

    if stream_id is None:
        t.log('error', '{0} does not match any configured stream stream names.'.format(stream_name))
        raise Exception
    else:
        t.log('info', 'Stream action {0} performed successfully!'.format(action))
        return True


def verify_traffic_throughput(**kwargs):
    """This function is deprecated. Please use bbe_verify_traffic_throughput."""

    _bbe_issue_deprecated_mesg(verify_traffic_throughput.__name__)
    return bbe_verify_traffic_throughput(**kwargs)


def bbe_verify_traffic_throughput(**kwargs):
    """
    Verifies traffic three different ways (throughput/packetcount/rate). Read below for arguments required by the
    different verifications.

    If mode is set to 'all', traffic throughput (percentage of packets received) is the
    only verification available.


    :param minimum_rx_percentage:       Minimum percentage of traffic that must be received to pass. Default is 97.
                                        This only affects verification when verify_by is 'throughout'.

    :param mode:                        Default is 'l23_test_summary'. Can target specific traffic item with
                                        mode='traffic_item'

    :param stream_name:                 Name of the stream you want to verify. Mode must be set to 'traffic_item'

    :param verify_by:                   throughput/packetcount/rate. Please note rate is measured INSTANTANEOUSLY.
                                        This means your traffic stream must be running to get a non-zero measurement!

    :param instantaneous_rate           Only required when verify_by is 'rate'. This is the rate you want to verify
                                        against the rate measured by the RT. Example '5mbps'. All rates assumed to
                                        be in units of mbps.

    :param packet_count                 Only required when verify_by is 'packetcount'. Integer value of expected
                                        packet count.

    :param error_tolerance:             Only used in verifications where verify_by is 'rate'. Sets the tolerance
                                        percent for upper/lower bound limits of RX rate. Acceptable inputs are integers
                                        between 1-100. Defaults to 1.

    :param kwargs:
    :return:                            Returns a dictionary containing traffic stats if verification is successful.
                                        Raises an exception if the verification fails.
    """
    try:
        bbe.bbevar
    except NameError:
        raise Exception("This is BBE Keyword verify_traffic_throughput,"
                        " please use other libs if not working on BBE feature")
    rthandle = t.get_handle(resource='rt0')
    return rthandle.invoke('verify_traffic_throughput_tester', **kwargs)


def configure_raw_form_traffic_stream(stream_name, source_rt_port, destination_rt_port, source_mac, destination_mac,
                                      **kwargs):
    """This function is deprecated. Please use bbe_configure_raw_form_traffic_stream."""

    _bbe_issue_deprecated_mesg(configure_raw_form_traffic_stream.__name__)
    return bbe_configure_raw_form_traffic_stream(stream_name, source_rt_port, destination_rt_port, source_mac,
                                                 destination_mac, **kwargs)


def bbe_configure_raw_form_traffic_stream(stream_name, source_rt_port, destination_rt_port, source_mac, destination_mac,
                                          **kwargs):
    """
    Configures a raw traffic stream using rthandle.invoke('traffic_simulation', **kwargs)

    :param stream_name:             stream name
    :param source_rt_port:          Port number of the desired source port on your chassis. Required.
                                    (Ex. wf-ixchassis2:1/5 port is '1/5')
    :param destination_rt_port:     Port number of the desired destination port on your chassis. Required.
                                    (Ex. wf-ixchassis2:1/5 port is '1/5')
    :param source_mac:              Source MAC address. Required.
    :param destination_mac:         Destination MAC address. Required.

    :param kwargs:
    encap_pppoe:                         pppoe simulation
    l3_protocol:                         ipv4/ipv6
    l4_protocol:                         icmpv6/dhcp/dhcpv6/udp
    frame_size:                          frame size
    rate_pps:                            rate in pps
    rate_bps:                            rate in bps
    rate_percent:                        rate in percent
    message_type:                        message type used by icmpv6(echo_req|echo_reply)/dhcp(discover|request|
                                         |release)/dhcpv6(solicit|request|release)/pppoe(PADI/PADR/PADT)
    vlan_id:                             start vlan id
    vlan_step:                           vlan step mode
    vlan_count:                          vlan counts
    svlan_id:                            start svlan id
    svlan_step:                          svlan step mode
    svlan_count:                         svlan counts
    src_mac_step:                        source mac step
    src_mac_count:                       source mac count
    dst_mac_step:                        destination mac step
    dst_mac_count:                       destination mac count
    src_ip:                              source ipv4 address
    src_ip_step:                         source ipv4 address step
    src_ip_count:                        source ipv4 count
    dst_ip:                              destination ipv4 address
    dst_ip_step:                         destination ipv4 address step
    dst_ip_count:                        destination ipv4 count
    src_ipv6:                            source ipv6 address
    src_ipv6_step:                       source ipv6 address step
    src_ipv6_count:                      source ipv6 address count
    dst_ipv6:                            destination ipv6 address
    dst_ipv6_step:                       destination ipv6 address step
    dst_ipv6_count:                      destination ipv6 address count

    Examples:

        1. PADI traffic with frame_size and rate_pps configured. VLAN and SVLAN also specified
        configure_raw_form_traffic_stream(source_rt_port='1/3',destination_rt_port='1/2',
                                          source_mac='01:02:00:00:00:01', destination_mac='FF:FF:FF:FF:FF:FF',
                                          frame_size='1500',rate_pps='1000', vlan_id='1',svlan_id='2', pppoe_encap = 1,
                                          message_type='padi')

        2. DHCPv6 traffic
        configure_raw_form_traffic_stream(source_rt_port='1/3',destination_rt_port='1/2',
                                          source_mac='01:02:00:00:00:01', destination_mac='FF:FF:FF:FF:FF:FF',
                                          frame_size='1500',rate_pps='1000', l3_protocol='ipv6', l4_protocol='dhcpv6',
                                          vlan_id='1',svlan_id='2', src_ipv6='3000:db8:ffff:1::2',
                                          dst_ipv6='2000::2',pppoe_encap = 1)

    :return:                             dictionary of status/stream_id/traffic_item
    """
    try:
        bbe.bbevar
    except NameError:
        raise Exception("This is BBE Keyword verify_traffic_throughput,"
                        " please use other libs if not working on BBE feature")
    kwargs['name'] = stream_name

    rthandle = t.get_handle(resource='rt0')
    result = rthandle.invoke('traffic_simulation', src_port=source_rt_port, dst_port=destination_rt_port,
                             src_mac=source_mac, dst_mac=destination_mac, **kwargs)
    t.log("Raw-form (no subscribers) traffic stream successfully created.")
    return result


def add_bidirectional_l2_vlan_subscriber_traffic(packets_count, uplink_name, rt='rt0', client_type='l2bsa',
                                                 bidirectional=1, mesh_type='one_to_one', traffic_type='ethernet_vlan',
                                                 **kwargs):
    """
    Adds l2vlan subscriber bidirectional traffic.

    :param rt: rt handle to perform action
    :param client_type: client type (e,g. dhcp,l2tp,ppp,vlan, l2bsa)
    :param uplink_name: uplink name (e.g uplink0,uplink1,custom0,custom1)
    :param bidirectional: traffic direction (e.g 1 or 0)
    :return:
    """
    kwargs['bidirectional'] = bidirectional
    kwargs['packets_count'] = packets_count
    kwargs['type'] = traffic_type
    kwargs['mesh_type'] = mesh_type

    client_type = client_type.strip()
    rtid = rt.strip()
    uplink_name = uplink_name.strip()

    uplink_inf = bbe.get_interfaces(rt, interfaces=uplink_name)
    rt_handle = t.get_handle(resource=rtid)
    clients = bbe.get_subscriber_handles(protocol=client_type)

    if clients is False:
        # Because bbe.get_subscriber_handles returns an empty list when no results are found and the empty list
        # evaluate to false, we should fail out here
        t.log('error', 'No {0} clients found'.format(client_type))
        raise Exception

    if uplink_inf is False:
        # Because bbe.get_interfaces returns an empty list when no results are found and the empty list evaluates
        # to false, we should fail out here
        t.log('error', 'Specified uplink interface was not found. Please provide a valid uplink interface name')
        raise Exception

    for l2bsa_subscriber_handle in clients:
        rt_handle.invoke('add_traffic', source=uplink_inf[0].rt_ethernet_handle,
                         destination=l2bsa_subscriber_handle.rt_ethernet_handle, **kwargs)
        sleep(10)


##########
# Valid8 #
##########

def start_valid8_server(valid8_server, server_name, ip_version, config, pcrf, nasreq, ocs):
    """
    :param valid8_server: Toby object to the Linux host running valid8
    :param server_name: pass the valid8 server name
    :param ip_version: pass the version file name to valid8
    :param config: pass the config file name to be used while starting valid8
    :param pcrf: pass the pcrf filename to be selected by PCRF program
    :param nasreq: pass the nasreq filename to be selected by NASREQ program
    :param ocs: pass the ocs filename to be selected by OCS program
    :return:
    """
    valid8_server.start_valid8_server(server_name=server_name, ip_version=ip_version, config=config, pcrf=pcrf,
                                      nasreq=nasreq, ocs=ocs)


def stop_valid8_server(valid8_server, server_name):
    """
    :param valid8_server: Toby object to the Linux host running valid8
    :param server_name: pass the valid8 server name
    :return:
    """
    valid8_server.stop_valid8_server(server_name=server_name)


def send_asr(valid8_server, server_name):
    """
    :param valid8_server: Toby object to the Linux host running valid8
    :param server_name: pass the valid8 server name
    :return:
    """
    valid8_server.send_asr(server_name=server_name)


def init_valid8_server(valid8_handle):
    """
    Initialize valid8
    :param valid8_handle: Toby object to Linux host running valid8
    :return: FreeRADIUS object

    example:
    ${valid8_handle} =    Get handle    resource=h0
    ${valid8_server} =    Init valid8 server  ${valid8_handle}
    """

    return Valid8(dev_handle=valid8_handle)

########
# Misc #
########


def clear_logs_from_dut():
    """This function is deprecated. Please use bbe_clear_logs_from_dut."""

    _bbe_issue_deprecated_mesg(clear_logs_from_dut.__name__)
    return bbe_clear_logs_from_dut()


def bbe_clear_logs_from_dut():
    """
    Clear logs from JunOS devices marked with tag dut
    /var/log/*.*
    /var/tmp/logs_*tgz
    /var/tmp/shmlog_*
    It removes *.* - the rolled over logs and zipped logs
    """
    try:
        duts = bbe.get_devices(device_tags='dut')
    except NameError:
        raise Exception("This is BBE keyword clear_logs_from_dut, please initialize BBE or refer to other libs")
    for dut in duts:
        device = dut.device_id
        t.log("Clear logs on {0}".format(device))
        device = t.get_handle(resource=device)
        device.su()
        command = 'rm -f /var/log/*.*'
        device.shell(command=command)
        command = 'rm -f /var/tmp/logs_*tgz'
        device.shell(command=command)
        command = 'rm -f /var/tmp/shmlog_*'
        device.shell(command=command)

    return True


def ls_testcase_action(**kwargs):
    """This function is deprecated. Please use bbe_ls_testcase_action."""

    _bbe_issue_deprecated_mesg(ls_testcase_action.__name__)
    return bbe_ls_testcase_action(**kwargs)


def bbe_ls_testcase_action(**kwargs):
    """
    this is for spirent landslide tester
    @{sub} =     get subscriber handle    protocol=hag
    Ls Testcase Action    subscriber=@{sub}[0]    action=start
    Ls Testcase Action    subscriber=@{sub}[0]    action=stop
    Ls Testcase Action    action=logout
    Ls Testcase Action    subscriber=@{sub}[0]    action=capture_start    port=access
    Ls Testcase Action    subscriber=@{sub}[0]    action=results
    @{filelist} =     Ls Testcase Action    subscriber=@{sub}[0]    action=capture_stop    port=access
    start_with_auto_pcap action will start the subscriber and packet capture together, and it will save the file in the
    landslide management page.
    :param kwargs:
    subscriber:                 bbe subscriber object, mandatory for all actions except logout
    action:                     start/stop/results/logout/capture_start/capture_stop/start_with_auto_pcap
    port:                       access/uplink, used by capture_start/capture_stop
    state:                      running/complete/waiting, used by check_session_status
    on_start:                   true/false. port capture enabled on start. Used by capture_config
    source_ip_filter:           source IP filter for generated pcaps. Used by capture_config
    dest_ip_filter:             destination IP filter for generated pcaps. Used by capture_config
    :return:            filename, used by capture_stop action only
    """
    try:
        bbe.bbevar
    except NameError:
        raise Exception("This BBE keyword ls_testcase_action, please initialize BBE")
    if kwargs['action'] != "logout":
        if 'subscriber' not in kwargs:
            raise Exception("subscriber must be provided")
        else:
            subscriber = kwargs['subscriber']
    action = kwargs['action']
    if action == 'capture_start':
        return subscriber.action(action=action, port=kwargs['port'])
    if action == 'capture_stop':
        subscriber.action(action=action, port=kwargs['port'])
        sleep(3)
        result = subscriber.action(action='capture_save', port=kwargs['port'])
        retries = 0
        while not result:
            retries += 1
            t.log("waiting for retries #{} for retrieving file".format(retries))
            sleep(5)
            result = subscriber.action(action='capture_save', port=kwargs['port'])
            if retries > 20:
                raise Exception("failed to get the pcap file after 20 retries")
        return result
    if action == 'logout':
        total_subs = bbe.get_subscriber_handles(protocol='hag') + bbe.get_subscriber_handles(protocol='cups')
        for subs in total_subs:
            if subs.isactive:
                t.log("Testcase {} is still active, will stop it now ".format(subs.tag))
                subs.action('stop')
            subs.action('delete')
        return subs.action('logout')
    if action == 'check_session_status':
        return subscriber.action(action='check_session_status', state=kwargs['state'])
    if action == 'is_fireball':
        return subscriber.action(action='is_fireball')
    if action == 'capture_config':
        capture_args = dict()
        capture_args['port'] = kwargs['port']
        if 'on_start' in kwargs:
            capture_args['onstart'] = kwargs['on_start']
        if 'source_ip_filter' in kwargs:
            capture_args['SourceIpFilter'] = kwargs['source_ip_filter']
        if 'dest_ip_filter' in kwargs:
            capture_args['DestIpFilter'] = kwargs['dest_ip_filter']
        return subscriber.action(action='capture_config', **capture_args)
    elif action == 'delete':
        if subscriber.isactive:
            t.log("Testcase {} is still active, will stop it now ".format(subscriber.tag))
            subscriber.action('stop')
    return subscriber.action(action=action)


def parse_bbe_license_file(filename):
    """
    parse the bbe license file, return dictionary, if the file is not available, return False
    :param filename:        license file name
    :return:    a dictionary of license based on model or False if failed
    """
    try:
        t.log("loading file {}".format(filename))
        license_string = yaml.load(open(filename))
    except:
        t.log("failed to open file {}".format(filename))
        return False
    return license_string


def bbe_get_devices(**kwargs):
    """
    return bbe devices
    :param kwargs:
    device_tags:    tag name
    id_only:        True/False
    :return:
    """
    try:
        return bbe.get_devices(**kwargs)
    except NameError:
        return t.get_junos_resources()


def bbe_topology_check(device_id='r0'):
    """
    ping uplink/radius address and check radius connection
    :param device_id:             device id, e.g. 'r0'
    :return:
    """
    #check ping for uplinks/radius link
    t.log("Pre Test check started, will ping uplinks/radius if available, and test radius server")
    import re
    import ipaddress
    cst.check_fpc(device_id=device_id)
    t.log("check link status in both Testers and Routers")
    cst.check_link_status(router=device_id)
    router = t.get_handle(device_id)
    uplinks = bbe.get_interfaces(device=device_id, interfaces='uplink')
    for uplink in uplinks:

        v4addr = uplink.interface_config.get('ip', None)
        v6addr = uplink.interface_config.get('ipv6', None)
        if uplink.interface_id == 'uplink0' and not v4addr and not v6addr:
            if not v4addr:
                v4addr = '200.0.0.1'
            if not v6addr:
                v6addr = '200:0:0::1'
        addrlist = []
        if v4addr:
            v4_addr = ipaddress.IPv4Interface(v4addr)
            address = str(v4_addr.ip + 1)
            addrlist.append(address)
        if v6addr:
            v6_addr = ipaddress.IPv6Interface(v6addr)
            address2 = str(v6_addr.ip + 1)
            addrlist.append(address2)
        for addr in addrlist:
            command = 'ping {} count 5'.format(addr)
            resp = router.cli(command=command).resp
            result = re.findall(r'icmp_seq', resp)
            if result:
                t.log("ping check for link {} address {} passed".format(uplink.interface_id, addr))
            else:
                raise Exception("ping address {} on link {} failed".format(addr, uplink.interface_id))

    radius_links = bbe.get_interfaces(device=device_id, interfaces='radius')
    for link in radius_links:
        con = bbe.get_connection(device_id, link.interface_id)

        v4addr = con.interface_config.get('ip', '9.0.0.9')
        v4_addr = ipaddress.IPv4Interface(v4addr)
        v4addr = str(v4_addr.ip)

        # Support for radius source-ip and ri
        # E.g.
        # resources:
        #   r0:
        #     radius0:
        #       uv-bbe-config:
        #         ip: 9.0.0.1/24
        #         source-ip: 102.0.0.1
        #         ri: test_ri
        source_addr = link.interface_config.get('source-ip', '100.0.0.1')  # '100.0.0.1'
        source_addr = ipaddress.IPv4Interface(source_addr)                 # IPv4Interface('100.0.0.1/32')
        source_addr = str(source_addr.ip)                                  # '100.0.0.1'
        rad_ri = link.interface_config.get('ri', 'default')                # radius routing-instance

        # ping without source first
        command = 'ping {} count 5 routing-instance {}'.format(v4addr, rad_ri)
        resp = router.cli(command=command).resp
        result = re.findall(r'icmp_seq', resp)
        if result:
            t.log("ping check for radius {} passed with ri {}".format(v4addr, rad_ri))
        else:
            # ping with source
            command_source = 'ping {} count 5 source {} routing-instance {}'.format(v4addr, source_addr, rad_ri)
            resp_source = router.cli(command=command_source).resp
            result_source = re.findall(r'icmp_seq', resp_source)
            if result_source:
                t.log("ping check for radius {} passed with source {} ri {}".format(v4addr, source_addr, rad_ri))
            else:
                raise Exception("ping address {} on radius {} failed".format(v4addr, link.interface_id))

        # test radius if available
        command = "test aaa ppp user test password test routing-instance {} | no-more".format(rad_ri)
        resp = router.cli(command=command).resp

        if 'Authentication: No response' in resp:
            raise Exception("Radius Daemon does not respond to the test")
        else:
            t.log("Radius test passed")


def is_dual_re(device_id='r0'):
    """This function is deprecated. Please use bbe_is_dual_re."""

    _bbe_issue_deprecated_mesg(is_dual_re.__name__)
    return bbe_is_dual_re(device_id)


def bbe_is_dual_re(device_id='r0'):
    """
    :param device_id:                     router device id, e.g. default is r0
    :return: True/False
    """
    router = t.get_handle(device_id)
    if hasattr(router, 'vc') and router.vc:
        t.log("this is MXVC")
        return False
    if len(router.current_node.controllers.keys()) == 2:
        return True
    return False


def _bbe_issue_deprecated_mesg(func_name, mesg=""):
    """Issues function deprecation messages.

    :param func_name: name of the deprecated function
    :param mesg: customized message
    :return:
    """
    old_kw = ' '.join(func_name.split('_')).title()

    if not mesg:
        deprecated_mesg = ' '.join(("This keyword '{}' is deprecated.".format(old_kw),
                                    "Please use 'BBE {}' instead.".format(old_kw)))
    else:
        deprecated_mesg = mesg

    t.log('warn', deprecated_mesg)
    t.log_console(deprecated_mesg)


