#! /usr/local/bin/python3

"""
 DESCRIPTION:   To get the hardware address of the junos device interface
     COMPANY:   Juniper Networks
"""
import re


def get_interface_hardware_address(device=None, interface=None):
    """
    To get hardware address for junos device interface
    Example:
        get_interface_hardware_address(device=device, interface=ge-0/0/1)
    ROBOT Example:
        get interface hardware address  device=${device}  interface=ge-0/0/0

    :param Device device:
        **REQUIRED** Device handle for junos device
    :param str interface:
        **REQUIRED** Interface name for which hardware address is required.
    :return: Hardware address of the junos device interface
    :rtype: str
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    if interface is None:
        device.log(
            level="ERROR",
            message="interface is a mandatory argument")
        raise Exception("interface is a mandatory argument")

    cmd = "show interface %s | match hardware" % (interface)
    device_resp = device.cli(command=cmd).response()
    interface_hardware_address = re.search(
        r'Hardware address:\s(([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2}))', device_resp)

    if interface_hardware_address:
        return interface_hardware_address.group(1)
    else:
        device.log(
            level="ERROR",
            message="Couldn't find the hardware address of interface %s" % (interface))
        raise Exception("Couldn't find the hardware address of interface %s" % (interface))
