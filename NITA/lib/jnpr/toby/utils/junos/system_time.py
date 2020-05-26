"""
Keywords for Junos date & time
"""

from datetime import datetime
import re
import jxmlease


def get_system_time(device=None, node=None):
    """
    To get current system time
    Example :
        get_system_time(device=dh)
        get_system_time(device=dh, node="node0")

    ROBOT Example:
        Get System Time    device=${dh}
        Get System Time    device=${dh}   node=node0

    :param str device:
        **REQUIRED** Device Handle of the DUT
    :param str node:
        *OPTIONAL* In case of HA, Node from which we need to check the time. By default it will
        check the primary node.
        ``Supported values``: "node0" and "node1"
    :return: Returns the date and time of the DUT
    :rtype: datetime
    """
    if device is None:
        raise ValueError("device is a mandatory argument")

    rpc_str = device.get_rpc_equivalent(command="show system uptime")
    srx_ha_flag = 0

    if re.match(".*(s|S)(r|R)(x|X).*", device.get_model(), re.DOTALL):
        if device.is_ha():
            if node is None:
                node = device.node_name()
            elif not (node == "node1" or node == "node0"):
                device.log(level='ERROR', message="Invalid HA Node value")
                raise ValueError("Invalid HA Node value")
            srx_ha_flag = 1
            etree_obj = device.execute_rpc(command=rpc_str).response()
            status = jxmlease.parse_etree(etree_obj)
            status = status['multi-routing-engine-results']['multi-routing-engine-item']
            for lst in status:
                if lst['re-name'] == node:
                    date_time = lst['system-uptime-information']['current-time']['date-time']
                    break

    if srx_ha_flag == 0:
        etree_obj = device.execute_rpc(command=rpc_str).response()
        status = jxmlease.parse_etree(etree_obj)
        date_time = status['system-uptime-information']['current-time']['date-time']

    match = re.match(r"([0-9-: ]+)\s([A-Z]+)", date_time, re.DOTALL)
    current_time_dt = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
    return current_time_dt


def set_system_time(device=None, date_time=None, node=None, validate=True, tolerance_in_seconds=5):
    """
    To set the system time of the DUT.
    Example :
        set_system_time(device=dh, date_time=dt)
        set_system_time(device=dh, date_time=dt, node="node0")
        set_system_time(device=dh, date_time=dt, node="all", validate=False)

    ROBOT Example:
        Set System Time    device=${dh}   date_time=${dt}
        Set System Time    device=${dh}   date_time=${dt}   node=node0
        Set System Time    device=${dh}   date_time=${dt}   node=all   validate=${False}

    :param str device:
        **REQUIRED** Device Handle of the DUT
    :param str node:
        *OPTIONAL* In case of HA, Node on which to set the time. By default it sets on both
        the nodes.
        ``Supported values``: "node0" and "node1"
    :param datetime date_time:
        **REQUIRED** Date and time which needs to be set in the DUT should be passed in a datetime
        object
    :param bool validate:
        *OPTIONAL* To validate if the time is set correctly. By default it is True.
    :param int tolerance_in_seconds:
        *OPTIONAL* In case of validation of time, how much tolerance should be tolerated. By default
        tolerance is 5 seconds.

    :return: Response from cli
    :rtype: str
    """

    if device is None:
        raise ValueError("device is a mandatory argument")
    if date_time is None:
        device.log(level='ERROR', message="date_time is a mandatory argument")
        raise ValueError("date_time is a mandatory argument")

    parsed_date_time = date_time.strftime("%Y%m%d%H%M.%S")
    cmd = "set date " + parsed_date_time
    response = device.cli(command=cmd, node=node).response()

    if validate is True:
        current_date = get_system_time(device=device, node=node)
        diff = current_date - date_time
        sec = diff.total_seconds()
        if sec > tolerance_in_seconds:
            device.log(level='ERROR', message="Time not able to set correctly")
        else:
            device.log(level='INFO', message="Time has been set correctly")
    return response


def sync_system_time_with_ntp(device=None, node=None):
    """
    To sync the system time back with NTP, provided NTP configuration is on the DUT.
    Example:
        sync_system_time_with_ntp(device=dh)
        sync_system_time_with_ntp(device=dh, node="node1")

    ROBOT Example:
        Sync System Time with Ntp   device=${dh}
        Sync System Time with Ntp   device=${dh}   node=node1

    :param str device:
        **REQUIRED** Device Handle of the DUT
    :param node:
        *OPTIONAL* In case of HA, Node on which to sync the time with NTP. By default it syncs on
        both the nodes.
        ``Supported values``: "node0", "node1"
    :return: Response from cli after setting the time
    :rtype: str
    """

    if device is None:
        raise ValueError("device is a mandatory argument")

    cmd = "set date ntp"
    return device.cli(command=cmd, node=node).response()
