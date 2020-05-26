# coding: UTF-8
# pylint: disable=too-many-arguments,invalid-name,too-many-statements
"""SRX Platform ROBOT keywords"""
import re
import time

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.utils import run_multiple


TOOL = flow_common_tool()
RUNTIME = {}

def check_feature_support(device, feature, **kwargs):
    """Check device whether support specific feature

    This method get system license to check specific feature whether supported on device. Supported feature includes:

        +   "HE" - HighEnd series such as "SRX4100", "SRX4200", "SRX4600", "SRX5400", "SRX5600", "SRX5800", etc...

        +   "LE" - LowEnd (Branch) series. All platforms not in HE platform list.

        +   "MULTI_SPU", "MULTISPU" - Have multi-spu platform such as SRX5400, SRX5600, SRX5800

        +   "LSYS", "LD", "LOGICAL_SYSTEM", "LOGICAL_DOMAIN"

        +   "REMOTE_ACCESS_IPSEC_VPN", "IPSEC_VPN", "VPN"

        +   "VIRTUAL_APPLIANCE"

    All above feature keyword are case insensitive and "-" will be transited to "_", it means "Logical-System", "LOGICAL_SYSTEM",
    or "logical-system" are same.

    **Pay attention: This method only check whether have feature license, it means only checking feature "licensed" count >= 1 but never checking
    "used-license", "needed", "validity-type", etc... If want see license detail for specific feature, see
    jnpr.toby.security.system.system_license**

    :param STR|LIST|TUPLE feature:
        **REQUIRED** Feature STR or LIST. will checking them one by one.

    :param STR|INT timeout:
        *OPTIONAL* Timeout to get platform info. Default: 300

    :return:
        If device support all given features, return True, otherwise return False

    :example:
        status = feature_support_check(feature="LSYS")
        status = feature_support_check(feature=["HE", LSYS"])
    """
    return device.check_feature_support(feature, **kwargs)


def do_failover(device, **kwargs):
    """High Availability Failover Execution

    :param DEVICE_HANDLER device:
        **MANDATORY** SRX HA device handler.

    :param INT|STR|LIST|TUPLE rg:
        *OPTIONAL* Redundancy-Group(0..128) or Group LIST. Ex. rg="0" or rg=[0, 1, 2, 3]. Default: 0

    :param INT|STR node:
        *OPTIONAL* Node which needs to be made primary. "0", "1", "node0" or "node1" (case insensitive). Default: Performs a failover

    :param BOOL force:
        *OPTIONAL* Whether do force failover. Default: False

    :param INT|STR timeout:
        *OPTIONAL* Wait a while for rg failover, and then checking whether failover succeed.

    :param INT|STR reset_waiting_timeout:
        *OPTIONAL* As default, this method will reset previous failover and waiting 1 second to start new failover. But sometimes we need more
                   than one second to reset, this option used for this. Default: 1

    :param INT|STR check_cnt:
        *OPTIONAL* Another solution of "timeout". With option "check_interval" to do loop checking.
                   Default: If rg=0, check_cnt=15; otherwise (1..128) check_cnt=2

    :param INT|STR check_interval:
        *OPTIONAL* With option "check_cnt" to do loop checking. Default: If rg=0, check_cnt=60; otherwise (1..128) check_cnt=10

    :param BOOL print_response:
        *OPTIONAL* Print final result to stdout if this option is True. Default: False

    :return:
        Boolean(True/False) depending on passing and failing of failover.

    :example:
        + do failover for single RG: r0.failover(rg=0)
        + do failover for multiple RGs to specific node: r0.failover(rg=[0, 1, 2, 3], node=1)
    """
    return device.failover(**kwargs)


def get_tnpdump_info(device, **kwargs):
    """Based on tnpdump command to archive all info

    :param BOOL force_get:
        *OPTIONAL* Set True will send command to get info every time. If set False, only first time send command to device. Default: False

    :param STR platform:
        *OPTIONAL* Device platform such as X86, OCTEON, XLP, etc... Default: None means get platform automatically.

    :param INT|STR node:
        *OPTIONAL* For HA topology. Valid value include 0, 1, "node0" or "node1". Default: None

    :param INT timeout:
        *OPTIONAL* Timeout to run "tnpdump" command. Default: 300 (sec)

    :return:
        Return a DICT value have all archived tnpdump info, or return False

        For DICT value, if device working on StandardAlone mode, or working on HA mode but option 'node' is 0 or 1, will return DICT like below:

            {"cp_addr":     "...", "spu_addr_list":      ["spu1", "spu2"], "both_addr_list":   ["cp", "spu1", "spu2"]}

        If device working on HA mode and "node" is None, return DICT like:

            {
                "node0":    {
                    "cp_addr":          "cp",
                    "spu_addr_list":    ["spu1", "spu2"],
                    "both_addr_list":   ["cp", "spu1", "spu2"],
                },
                "node1":    {
                    "cp_addr":          "cp",
                    "spu_addr_list":    ["spu1", "spu2"],
                    "both_addr_list":   ["cp", "spu1", "spu2"],
                }
            }
    """
    return device.get_tnpdump_info(**kwargs)


def get_version_info(device, **kwargs):
    """Based on command "show version" to get device hostname, platform, image_info, etc...

    :param BOOL force_get:
        *OPTIONAL* Set True will send command to get info every time. If set False, only first
                   time send command to device. default: False

    :param INT|STR node:
        *OPTIONAL* Must be 0, 1, node0, node1 or BOTH. default: None

    :param INT timeout:
        *OPTIONAL* Timeout to run "show version" command. default: 60

    :return:
        Return a DICT value have all version info, or return False

        For DICT value, if device working on StandardAlone mode, or working on HA mode but option 'node' is 0 or 1, will return DICT like below:

            {"hostname":     "...", "version":      "..."}

        If device working on HA mode and "node" is None, return DICT like:

            {
                "node0":    {
                    "hostname":         "...",
                    "version":          "...",
                    "package_comment":  "...",
                    "product_model":    "...",
                    "product_name":     "...",
                },
                "node1":    {
                    "hostname":         "...",
                    "version":          "...",
                    "package_comment":  "...",
                    "product_model":    "...",
                    "product_name":     "...",
                }
            }
    """
    return device.get_version_info(**kwargs)

def ha_switch_to_primary_node(device):
    """For HA setup, set device handler to primary node

    :param HANDLER device:
        HA device handler. Most time we call r0, r1 etc...

    :return:
        No any return
    """
    return device.switch_to_primary_node()


def loop_ping(device, dst_addr, **kwargs):
    """Do ping in loop by time interval

    Sometimes we need do loop ping. For example:

    1.  IPSec tunnel need first packet to start tunnel establishment
    2.  Boardcard is in restarting but not sure when finished, because low-end need more time
        than high-end

    This method do loop ping by option dst_addr, "dst_addr" should be one IPv4/v6 IP address or LIST of IPs, and then return ping result.
    Both support Linux and SRX device

    Please see **Example** section to know more

    :param OBJECT device:
        **REQUIRED** Source HOST's handle to do ping

    :param IP|LIST dst_addr:
        **REQUIRED** Destination IP address or hostname, should be a LIST to ping several IPs in one shoot

    :param INT ping_counter:
        *OPTIONAL* ping packet counter. Default: 4

    :param STR ping_option:
        *OPTIONAL* ping cmd's option such as '-c 5' or '-f', it will concatenate to ping cmd.
                    Default: None

    :param INT timeout:
        *OPTIONAL* Each ping check timeout. Default: default timeout in __init__

    :param STR ipv4_ping_cmd:
        *OPTIONAL* IPv4 ping command's path. default: /bin/ping (Linux) or /sbin/ping (SRX)

    :param STR ipv6_ping_cmd:
        *OPTIONAL* IPv6 ping command's path. default: /bin/ping6 (Linux) or /sbin/ping6 (SRX)

    :param INT loop_cnt:
        *OPTIONAL* Loop times to do ping check. Default: 1

    :param INT loop_interval:
        *OPTIONAL* sleep second between each loop. Default: 10

    :param STR device_type:
        *OPTIONAL* One of "SRX" or "LINUX". Default: None

        "SRX" and "LINUX" device have different behavior to ping. As default, this method decide device type automatically, or you can set device_type
        manually.

    :param STR get_detail:
        *OPTIONAL* As default the method return True/False to indicate ping success or failed. But set this option to True to get a DICT value For
                    one ping result like below:

                    return_value = {
                        "lost_rate":        10,
                        "lost_packet":      1,
                        "received_rate":    90,
                        "received_packet":  9,
                        ....
                    }

                    If "dst_addr" is IP list, will return a DICT like this:

                    return_value = {
                        "192.168.1.2":  {
                            "lost_rate":        10,
                            "lost_packet":      1,
                            "received_rate":    90,
                            "received_packet":  9,
                            ....
                        }
                        "192.168.1.3":  {
                            ...
                        }
                    }

                    Default: None

    :return:
        +   "dst_addr" contain 1 IP and no "get_detail"     - return True/False
        +   "dst_addr" contain 1+ IP and not "get_detail"   - return LIST like: [True, True, False]
        +   "dst_addr" contain 1 IP and "get_detail"=True   - return DICT contain all details
        +   "dst_addr" contain 1+ IP and "get_detail"=True  - return DICT contain all IPs detail

    :Example:

        1.  1 IP and get_detail=None or False

            loop_ping(device=h0, dst_addr="192.168.100.2")
            => True

        2.  1+ IP and get_detail=None or False

            loop_ping(device=h0, dst_addr=("192.168.100.2", "2000:200::2"))
            > [True, False]

        3.  1 IP and get_detail=True

            loop_ping(device=h0, dst_addr="192.168.100.2", get_detail=True)
            => {
                "lost_rate":        10,
                "lost_packet":      1,
                "received_rate":    90,
                "received_packet":  9,
                ....
            }

        4.  1+ IP and get_detail=True

            loop_ping(device=h0, dst_addr=("192.168.100.2", "2000:200::2"), get_detail=True)
            => {
                "192.168.100.2":    {
                    "lost_rate":        10,
                    "lost_packet":      1,
                    "received_rate":    90,
                    "received_packet":  9,
                    ....
                },
                "2000:200::2":      {
                    "lost_rate":        10,
                    "lost_packet":      1,
                    "received_rate":    90,
                    "received_packet":  9,
                    ....
                },
            }

    """
    func_name = TOOL.get_current_function_name()
    device.log(message=TOOL.print_title(func_name), level="INFO")

    options = {}
    options["dst_addr"] = dst_addr
    options["ping_counter"] = int(kwargs.pop("ping_counter", 4))
    options["ping_option"] = kwargs.pop("ping_option", None)
    options["timeout"] = int(kwargs.pop("timeout", 300))
    options["ipv4_ping_cmd"] = kwargs.pop("ipv4_ping_cmd", None)
    options["ipv6_ping_cmd"] = kwargs.pop("ipv6_ping_cmd", None)
    options["loop_cnt"] = int(kwargs.pop("loop_cnt", 1))
    options["loop_interval"] = float(kwargs.pop("loop_interval", 10))
    options["get_detail"] = kwargs.pop("get_detail", None)
    options["device_type"] = kwargs.pop("device_type", None)

    if not isinstance(options["dst_addr"], (list, tuple)):
        options["dst_addr"] = (options["dst_addr"], )

    if options["device_type"] is None and str(device.get_model()).upper() in ("LINUX", "CENTOS", "FEDORA", "UBUNTU"):
        options["device_type"] = "LINUX"
    else:
        options["device_type"] = str(options["device_type"]).upper()

    if options["ipv4_ping_cmd"] is None:
        options["ipv4_ping_cmd"] = "/bin/ping" if options["device_type"] == "LINUX" else "/sbin/ping"

    if options["ipv6_ping_cmd"] is None:
        options["ipv6_ping_cmd"] = "/bin/ping6" if options["device_type"] == "LINUX" else "/sbin/ping6"

    all_info = {}
    for dst_addr_element in options["dst_addr"]:
        cmd_element = []
        if re.search(r":", dst_addr_element):
            cmd_element.append("{} -c {}".format(options["ipv6_ping_cmd"], options["ping_counter"]))
        else:
            cmd_element.append("{} -c {}".format(options["ipv4_ping_cmd"], options["ping_counter"]))

        if options["ping_option"] is not None:
            cmd_element.append(options["ping_option"])

        cmd_element.append(dst_addr_element)

        info = {}
        for index in range(1, options["loop_cnt"] + 1):
            device.log(message="Loop {}: ping check for '{}'".format(index, dst_addr_element), level="INFO")
            lines = dev.execute_shell_command_on_device(device=device, command=" ".join(cmd_element), timeout=options["timeout"])
            device.log(message="ping result: \n{}".format(lines), level="DEBUG")

            info["ttl"] = None
            info["transmitted"] = None
            info["received"] = None
            info["lost_rate"] = None
            info["min"] = None
            info["avg"] = None
            info["max"] = None
            info["mdev"] = None

            for line in lines.splitlines():
                match = re.search(r"(ttl|hlim)=(\d+)", line)
                if match:
                    info["ttl"] = int(match.group(2))
                    continue

                match = re.search(r"(\d+)\s+packets transmitted", line)
                if match:
                    info["transmitted"] = int(match.group(1))

                match = re.search(r"(\d+)\s+(packets\s)*received", line)
                if match:
                    info["received"] = int(match.group(1))

                match = re.search(r"(\d+)\%\s+packet loss", line)
                if match:
                    info["lost_rate"] = int(match.group(1))

                # Linux output
                match = re.search(r"min\/avg\/max\/mdev\s+=\s+(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\s+", line)
                if match:
                    info["min"] = float(match.group(1))
                    info["avg"] = float(match.group(2))
                    info["max"] = float(match.group(3))
                    info["mdev"] = float(match.group(4))

                # SRX device output
                match = re.search(r"round-trip min\/avg\/max\/stddev.*\s+(\S+)\/(\S+)\/(\S+)\/(\S+)\s+", line)
                if match:
                    info["min"] = float(match.group(1))
                    info["avg"] = float(match.group(2))
                    info["max"] = float(match.group(3))
                    info["mdev"] = float(match.group(4))
                    info["stddev"] = float(match.group(4))

            if info["received"] is not None and info["received"] >= 1:
                break

            device.log(message="Host '{}': waiting '{}' secs for next ping check...".format(dst_addr_element, options["loop_interval"], level="INFO"))
            time.sleep(options["loop_interval"])

        all_info[dst_addr_element] = info

    # final result
    if len(options["dst_addr"]) == 1:
        info = list(all_info.values())[0]
        if options["get_detail"] is True:
            return_value = info
        else:
            return_value = bool(info["received"])
    else:
        if options["get_detail"] is True:
            return_value = {}
            for dst_addr_element in all_info:
                return_value[dst_addr_element] = all_info[dst_addr_element]
        else:
            return_value = []
            for dst_addr_element in all_info:
                return_value.append(bool(all_info[dst_addr_element]['received']))

    if isinstance(return_value, dict):
        device.log(message="{} return value:\n{}".format(func_name, TOOL.pprint(return_value), level="INFO"))
    else:
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")

    return return_value

def get_interface_hardware_address(device, interface_name, **kwargs):
    """Get device interface MAC address

    This function get interface MAC address from Linux host or SRX device.

    :param STR platform:
        *OPTIONAL* Device platform string such as 'Linux' or 'srx'. Set None to get platform automatically. default: None

    :param BOOL uppercase:
        *OPTIONAL* Uppercase hardware address and return. default: False

    :return: Return interface MAC address or raise RuntimeException
    """
    func_name = TOOL.get_current_function_name()
    device.log(message=TOOL.print_title(func_name), level="INFO")

    options = {}
    options["platform"] = kwargs.pop("platform", None)
    options["uppercase"] = TOOL.check_boolean(kwargs.pop("uppercase", False))

    if not hasattr(device, "get_model"):
        raise RuntimeError("Device object '{}' do not have 'get_model' method.".format(str(device)))

    if options["platform"] is None:
        if str(device.get_model()).upper() in ("LINUX", "CENTOS", "FEDORA"):
            options["platform"] = "LINUX"
        else:
            options["platform"] = "SRX"
    else:
        options["platform"] = options["platform"].upper()

    # interface name maybe set to ge-0/0/1.0 or eth1:1, but only ge-0/0/1 and eth1 needed
    interface_name = re.split(r"[\.\:]", interface_name)[0]

    return_value = None
    if options["platform"] == "LINUX":
        result = dev.execute_shell_command_on_device(device=device, command="/sbin/ifconfig {}".format(interface_name))
        match = re.search(r"ether\s+(\S+)\s+", result)
        if match and len(re.split(r":", match.group(1))) == 6:
            return_value = match.group(1)
        else:
            raise RuntimeError("Cannot get interface MAC address from device '{}'\n{}".format(str(device), result))

    else:
        result = dev.execute_cli_command_on_device(
            device=device,
            format="xml",
            channel="xml",
            xml_to_dict=True,
            command="show interface {}".format(interface_name))

        if "physical-interface" not in result["interface-information"]:
            msg = "No interface response from device '{}'".format(str(device))
            if "rpc-error" in result["interface-information"]:
                msg = result["interface-information"]["rpc-error"]["error-message"]

            raise RuntimeError(msg)

        return_value = str(result["interface-information"]["physical-interface"]["hardware-physical-address"])

    if options["uppercase"] is True:
        return_value = return_value.upper()

    device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
    return return_value

def check_vmhost(device, **kwargs):
    """checking vmhost based device for SRX

    There are 2 ways to upgrade or ISSU upgrade device, one is "request system software ..." and the other is
    "request vmhost software ...". This method checking device hardware and tell you keyword of 'system' or 'vmhost'.

    Return:
        'system' or 'vmhost'
    """
    func_name = TOOL.get_current_function_name()
    dev_fingerprint = str(device)

    vmhost_keyword_list = (
        re.compile(r"RE-2000x6", re.I),
    )

    options = {}
    options["force"] = TOOL.check_boolean(kwargs.pop("force", False))

    if func_name not in RUNTIME:
        RUNTIME[func_name] = {}

    if dev_fingerprint not in RUNTIME[func_name]:
        RUNTIME[func_name][dev_fingerprint] = None

    if options["force"] is False and RUNTIME[func_name][dev_fingerprint] is not None:
        return RUNTIME[func_name][dev_fingerprint]

    cmd = "show chassis hardware"
    if device.is_ha() is True:
        cmd += " node 0"

    component_list = dev.execute_cli_command_on_device(device=device, channel="pyez", format="xml", xml_to_dict=True, command=cmd)
    if device.is_ha() is True:
        component_list = component_list["multi-routing-engine-results"]["multi-routing-engine-item"]

    # strip root tag then all sub chassis components should be list or tuple
    component_list = component_list["chassis-inventory"]["chassis"]["chassis-module"]
    if not isinstance(component_list, (tuple, list)):
        component_list = (component_list, )

    return_value = "system"
    for component in component_list:
        if "name" not in component or not re.match(r"Routing Engine", str(component["name"]).strip()):
            continue

        for pattern in vmhost_keyword_list:
            if re.search(pattern, component["description"]):
                return_value = "vmhost"
                break

        if return_value == "vmhost":
            break

    RUNTIME[func_name][dev_fingerprint] = return_value

    device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
    return return_value


def reboot_device_in_parallel(device_list, **kwargs):
    """Reboot list of devices in parallel

    Support JunOS and linux host both. For HA setup, all nodes will be rebooted.

    **Pay attention**: except option "device_list", all other options will set to all devices. This means if
    'device_list' include JunOS and Linux both, and set 'mode=cli', you will got RuntimeError because Linux do not
    support this argument.

    :param LIST|TUPLE device_list:
        **REQUIRED** A list of devices will reboot in parallel.

    :param INT|STR wait:
        *OPTIONAL* Wait time to re-connect all devices

    :param STR mode:
        *OPTIONAL* Rebooting mode that one of 'shell' or 'cli' for all devices. default: 'cli'

            cli - 'request system reboot'
            shell - 'reboot'

    :param INT|STR timeout:
        *OPTIONAL* Timeout to reboot and reconnect device. Default: 480 (sec)

    :param INT|STR interval:
        *OPTIONAL* Re-connect check interval. default: 20 (sec)

    :param STR device_type:
        *OPTIONAL* This option works only for 'cli' mode. Value should be set to 'vmhost' to reboot the vmhost

    :return:
        Return True if all devices reboot succeed, otherwise return False
    """
    if not isinstance(device_list, (list, tuple)):
        raise ValueError("option 'device_list' must be a list or tuple, but got '{}'".format(type(device_list)))

    func_name = TOOL.get_current_function_name()
    device_list[0].log(message=TOOL.print_title(func_name), level="INFO")

    # will not change invoked method's default value
    options = {}
    for keyword in ("wait", "mode", "timeout", "interval", "device_type"):
        if keyword in kwargs:
            options[keyword] = kwargs[keyword]

    all_devices = []
    for device in device_list:
        if "node0" in dir(device):
            all_devices.append(device.node0)
            all_devices.append(device.node1)
        else:
            all_devices.append(device)

    all_device_name_list = []
    for device in all_devices:
        if "name" in dir(device):
            all_device_name_list.append(device.name)
        else:
            all_device_name_list.append(device.current_node.current_controller.name)

    list_of_dicts = []
    for device in all_devices:
        list_of_dicts.append({
            "fname": device.reboot,
            "kwargs": options,
        })
    reboot_result_list = run_multiple(list_of_dicts)
    return_value = True if len(all_devices) == reboot_result_list.count(True) else False

    msg = [
        "{} return value: {}".format(func_name, return_value),
        "Device List:",
    ]
    for hostname, result in zip(all_device_name_list, reboot_result_list):
        msg.append("\t{}: {}".format(hostname, result))

    device_list[0].log(message="\n".join(msg), level="INFO")
    return return_value
