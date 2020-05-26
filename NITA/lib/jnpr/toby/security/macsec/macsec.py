"""
Created on Jul 17, 2017

@author: Baba Syed Mazaz Hussain
"""
import re
import operator

def get_lowest_mac_device(device_dict=None):
    """
    Robot Usage Example :
       ${dict}=    Create Dictionary    r0=${tv['r0__r0r1__pic']}    r1=${tv['r1__r0r1__pic']}
       ${lowestMacDevice}=    Get Lowest Mac Device    ${dict}
       ${interface}=    Get From Dictionary    ${dict}    ${lowestMacDevice}
    To find lowest MAC interface device,
    from the dictionary ${dict}: key is device name, value is device interface
    using cli command "show interface <interface-name>"
    :param STR device_dict:
        **REQUIRED** Device name as key and interface name as value of string data type
    :return:
        device name is returned whose interface has lowest MAC
    :rtype: STR
    """
    if device_dict is None:
        t.log("ERROR", message="device dictionary is mandatory argument")
        raise Exception("device dictionary is mandatory argument")
    mac_dict = {}
    for dev in device_dict.keys():
        device = t.get_handle(resource=dev)
        interface = device_dict[dev]
        output = device.cli(command='show interfaces '+interface).response()
        match = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', output, re.I).group()
        mac_dict[dev] = match
    sorted_interface = sorted(mac_dict.items(), key=operator.itemgetter(1))
    if sorted_interface:
        return sorted_interface[0][0]
    return None

def get_pid(device_dict=None):
    """
    Robot Usage Example :
    ${dict}=    Create Dictionary    r2=dot1xd
    ${result}=    Get Pid    ${dict}
    ${pid}=    Get From Dictionary    ${result}    r2
    Gets the process id from the processes running in the device
    using cli command "show system processes extensive | grep dot1xd"
    :param STR device_dict:
        **REQUIRED** Device name as key and  process name as value of string data type
    :return:
        device name and process ID is returned whose interface has lowest MAC
    :rtype: STR
    """
    if device_dict is None:
        t.log("ERROR", message="device dictionary is mandatory argument")
        raise Exception("device dictionary is mandatory argument")
    process_dict = {}
    for dev in device_dict.keys():
        device = t.get_handle(resource=dev)
        process = device_dict[dev]
        response = device.cli(command='show system processes | grep '+ process).response()
        match = re.search(r'^\s*(\d+)\s+.*/usr/sbin/%s' % process, str(response), re.I).group(1)
        process_dict[dev] = match
    if process_dict:
        return process_dict
    return None
