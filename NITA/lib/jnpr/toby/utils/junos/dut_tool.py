# coding: UTF-8
# pylint: disable=invalid-name
"""Device related methods

Below options are have same behavior:

+   device (Object) - Device handler

+   timeout (int) - Timeout for send command to device and waiting for response

+   get_response (bool) Default: False

    Set True means want get command's result string. False will return True/False to indicate
    command commit success or faile. if method no commit, it will return command result string.

+   commit (bool) Default: True

    Set True to commit configuration. Or False will just send conf to device but do not commit.

"""

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import copy
import threading
from queue import Queue

from jnpr.toby.frameworkDefaults import credentials
from jnpr.toby.security.system.system_license import system_license
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.message import message
from jnpr.toby.utils.xml_tool import xml_tool



class dut_tool(message):
    """Device related methods"""
    def __init__(self):
        """Init processing"""
        super().__init__()
        self.xml = xml_tool()
        self.tool = flow_common_tool()
        self.license = system_license()

        self.default = {
            "cli_commit_timeout":       120,
            "cli_show_timeout":         300,
            "cli_reboot_timeout":       600,
            "regress_username":         credentials.Junos["USERNAME"],
            "regress_password":         credentials.Junos["PASSWORD"],
            "root_username":            credentials.Junos["SU"],
            "root_password":            credentials.Junos["SUPASSWORD"],
        }

        self.info = {
            "version_info":                 {},             # for get_version_info method
            "tnpdump_info":                 {},             # for send_vty_cmd_and_get_response
            "root_permission":              {},             # indicate device whehter work in root
        }

    def send_cli_cmd(self, device, cmd, **kwargs):
        """Send command or command list to device and get response

        TOBY platform have 2 channels to operate device, PyEZ and SSH/Telnet

        PyEZ is based on netconf protocol to send cmd by XML, and device always return XML response
        as well. Whatever you want get response by XML or TEXT format, PyEZ always response XML
        object, and this method will transit the object to a DICT value.

        SSH/Telnet is based one pexpect (like JT). If format is "XML", this method will tail
        "display xml" and return XML string. For this situation, this method will transit XML string
        to DICT too.

        If you want get cmd's plain-text response, only way is channel="TEXT" and format="TEXT"


        :param STR|LIST cmd:
            **REQUIRED** cmd or cmd list will sent to device

        :param STR channel:
            *OPTIONAL* one of "text" or "pyez" to send command. Default: pyez

        :param STR format:
            *OPTIONAL* Response format that one of 'xml' or 'text'. Default: xml

        :param BOOL print_response:
            *OPTIONAL* Whether print device response to stdout. Default: True

        :param INT timeout:
            *OPTIONAL* Timeout for command send and get response

        :param BOOL no_more:
            *OPTIONAL* Append "no-more" to given command. Only for "SSH" channel (means option 'channel' and 'format' must be 'text'). default: False

        :return:
            +   DICT_VALUE = channel="PYEZ", format="XML"
            +   DICT_VALUE = channel="PYEZ", format="TEXT"
            +   DICT_VALUE = channel="TEXT", format="XML"
            +   STRING_VALUE = channel="TEXT", format="TEXT"

            May raise TypeError or ValueError
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        options["channel"] = kwargs.get("channel", "PYEZ").strip().upper()
        options['format'] = kwargs.get("format", "XML").strip().upper()
        options['timeout'] = int(kwargs.get("timeout", self.default['cli_show_timeout']))
        options['print_response'] = kwargs.get("print_response", True)
        options['no_more'] = kwargs.get("no_more", False)

        if isinstance(cmd, str):
            cmd_list = (cmd, )
        elif isinstance(cmd, (list, tuple)):
            cmd_list = copy.deepcopy(cmd)
        else:
            raise TypeError("'cmd' option must be a str, list or tuple, not '{}'".format(type(cmd)))

        if options["channel"] not in ("PYEZ", "TEXT"):
            raise ValueError("'channel' option must be 'text' or 'pyez', not '{}'".format(options["channel"]))

        if options["format"] not in ("TEXT", "XML"):
            raise ValueError("'format' option must be 'text' or 'xml', not '{}'".format(options["format"]))

        # send command
        for new_cmd in cmd_list:
            if options["channel"] == "PYEZ":
                self.display(level="INFO", msg="channel 'pyez' send cmd: {}".format(new_cmd))

            if options["channel"] == "TEXT" and options["format"] == "TEXT" and options["no_more"] is True:
                new_cmd += " | no-more"

            response = device.cli(command=new_cmd, format=options['format'], channel=options["channel"], timeout=options['timeout']).response()

        # only last command's response return
        if options["channel"] == "PYEZ" and options["format"] == "XML":
            return_value = self.xml.xml_obj_to_dict(response)
        elif options["channel"] == "PYEZ" and options["format"] == "TEXT":
            return_value = self.xml.xml_obj_to_dict(response)
        elif options["channel"] == "TEXT" and options["format"] == "XML":
            # if not pyez channel, text response may have unneeded output
            match = re.search(r"(\<rpc\-reply.*\<\/rpc\-reply\>)", response, re.S)
            if not match:
                raise RuntimeError("Not well-formated XML response")

            response = match.group(1)
            return_value = self.xml.xml_string_to_dict(response)
        else:
            return_value = response

        if options["print_response"] is True:
            self.display(level="INFO", msg="{} return value:\n{}".format(func_name, return_value))
        return return_value

    def send_shell_cmd(self, device, cmd, **kwargs):
        """Send given command to DUT and get response

        :param STR|LIST cmd:
            **REQUIRED** Single command or a command list to send to DUT.

        :param INT timeout:
            *OPTIONAL* Command running timeout. default: 60

        :param BOOL print_response:
            *OPTIONAL* Whether print device response to stdout. Default: True

        :return: Return last command's response string, or return False
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        if isinstance(cmd, str):
            cmd_list = (cmd, )
        elif isinstance(cmd, (list, tuple)):
            cmd_list = tuple(copy.deepcopy(cmd))
        else:
            raise TypeError("'cmd' option must be str, list or tuple, not '{}'".format(type(cmd)))

        options['timeout'] = int(kwargs.get('timeout', self.default["cli_show_timeout"]))
        options['print_response'] = kwargs.get('print_response', True)

        for new_cmd in cmd_list:
            response = device.shell(command=new_cmd, timeout=options['timeout'])

        if options["print_response"]:
            self.display(level="INFO", msg="{} return value:\n{}".format(func_name, response.response()))
        return response.response()

    def send_conf_cmd(self, device, cmd, **kwargs):
        """send given conf command to DUT and commit

        Given 1 or more command(s) to send to DUT device. According to 'get_response' option, it
        will return True/False or return STRING commit output

        :param STR/LIST/TUPLE cmd:
            **REQUIRE** A command string or a LIST/TUPLE to send to device

        :param STR config_mode:
            *OPTIONAL* 'exclusive' or 'private'. Default: ""

        :param BOOL get_response:
            *OPTIONAL* If set True, will return STRING value which contain command response.

                       Behaviors:

                        get_response = True && commit = False:

                            - Return last cmd's result. For negative testing, it can get error msg

                        get_response = True && commit = True

                            - reboot_if_need option worked only in this scenario. This will send cmd
                              to device and return commit string response. After device rebooting,
                              commit string response will return.

                        get_response = False && commit = False

                            - Just send cmd to device but not commit. Return True/False to indicate
                              command whether send success

                        get_response = False && commit = True

                            - Return True/False to indicate whether commit success.

                       Default: True

        :param BOOL commit:
            *OPTIONAL* If set True, will send cmd to device and commit. Default: True

        :param BOOL detail:
            *OPTIONAL* This is only worked if commit=True. If detail=True, commit detail info
                       (include each module check output) will return. default: False

        :param BOOL reboot_if_need:
            *OPTIONAL* If set True, it means get_response=True and commit=True, method will check commit response
                       whether have rebooting tips to reboot and reconnect DUT if needed.

            For HA topo, will reboot 2 nodes in parallel.

            Default: False

        :param BOOL print_response:
            *OPTIONAL* Whether print device response to stdout. Default: True

        :param INT timeout:
            *OPTIONAL* Command commit timeout.

        :return:
            Separated in each options
        """
        self.display_title(msg=self.tool.get_current_function_name())

        # default value and validation check
        options = {}
        options["config_mode"] = kwargs.get("config_mode", "")
        options["get_response"] = kwargs.get("get_response", True)
        options["detail"] = kwargs.get("detail", False)
        options["reboot_if_need"] = kwargs.get("reboot_if_need", False)
        options["commit"] = kwargs.get("commit", True)
        options["print_response"] = kwargs.get("print_response", True)
        options["timeout"] = int(kwargs.get("timeout", self.default['cli_commit_timeout']))

        if options["reboot_if_need"] is True:
            options["get_response"] = True
            options["commit"] = True

        if isinstance(cmd, str):
            cmd_list = [cmd, ]
        elif isinstance(cmd, (list, tuple)):
            cmd_list = list(copy.deepcopy(cmd))
        else:
            raise TypeError("Option 'cmd' must be str, list or tuple, not '{}'".format(type(cmd)))

        # send command and commit
        response = device.config(command_list=cmd_list, mode=options['config_mode'], timeout=options["timeout"])
        if options["commit"] is True:
            response = device.commit(timeout=options["timeout"], detail=options["detail"])

        if options["get_response"] is True:
            return_value = response.response()
        else:
            return_value = response.status()

        # make sure whether need reboot device
        if options["reboot_if_need"] is True:
            need_reboot = False

            reboot_keyword_pattern_list = (
                re.compile(r"must reboot the system"),
                re.compile(r"need to reboot"),
                re.compile(r"Multitenancy mode is changed\s+.*Must reboot"),
                re.compile(r"reboot the device"),
            )

            for pattern in reboot_keyword_pattern_list:
                if re.search(pattern, response.response()):
                    need_reboot = True
                    break

            # if reboot succeed, just return before rebooting's commit response
            if need_reboot:
                if device.is_ha():
                    reboot_dev = [device.node0, device.node1]
                else:
                    reboot_dev = device

                self.display_title(msg="START REBOOTING")
                if self.reboot(device=reboot_dev) is False:
                    return_value = False

        if options["print_response"] is True:
            self.display(level="INFO", msg="{} return value:\n{}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def send_vty_cmd(self, device, cmd, **kwargs):
        """According to platform to send vty command to device and get response

        Device have different commands to send command. For example, low-end or branch device use cprod command, but high-end use srx-cprod.sh. This
        method use different command to send cmd and get response.

        :param STR|LIST|TUPLE cmd:
            **REQUIRE** A command string or a LIST/TUPLE to send to device

        :param STR component:
            *OPTIONAL* CP, SPU or BOTH to send command. Default: CP

                       CP   - only send cmd to CP
                       SPU  - send cmd to all SPUs
                       BOTH - send cmd both to CP and SPUs

        :param STR tnpdump_addr:
            *OPTIONAL* Alternative of component option. If this option have tnpdump address, option component will ignored. Default: None

        :param INT send_cnt:
            *OPTIONAL* send cmd times. Default: 1.

                       Sometimes vty cmd cannot send to component. This special option used to send cmd again if got error.

                       If set 3 to this option, it means every cmd will re-send 2 times if got error.

        :param STR|INT node:
            *OPTIONAL* For HA topology. Default is None, that means:

                       +   For SA topo, send cmd as usual
                       +   For HA topo, send cmd to primary node, TNPaddr is from option "component" or "tnpdump_addr"

        :param INT timeout:
            *OPTIONAL* Timeout to get infomation

        :param BOOL print_response:
            *OPTIONAL* Whether print device response to stdout. Default: True

        :return:
            all vty command's response. or raise exception
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        options["cmd"] = cmd
        options["platform"] = kwargs.get("platform", None)
        options["component"] = kwargs.get("component", "CP")
        options["tnpdump_addr"] = kwargs.get("tnpdump_addr", None)
        options["send_cnt"] = int(kwargs.get("send_cnt", 1))
        options["node"] = kwargs.get("node", None)
        options["print_response"] = kwargs.get("print_response", True)
        options['timeout'] = kwargs.get('timeout', self.default['cli_reboot_timeout'])

        # option check
        if isinstance(cmd, str):
            user_cmd_list = [cmd, ]
        elif isinstance(cmd, (list, tuple)):
            user_cmd_list = list(copy.deepcopy(cmd))
        else:
            raise TypeError("Option 'cmd' must be str, list or tuple, not '{}'".format(type(cmd)))

        options["component"] = options["component"].upper()
        if options["component"] not in ("CP", "SPU", "BOTH"):
            raise ValueError("'component' must be 'CP', 'SPU' or 'BOTH', not '{}'".format(options["component"]))

        # This method need root permission
        if self.su(device=device) is False:
            raise Exception("{} cannot get root permission on device: {}".format(func_name, str(device)))

        # If tnpdump_addr has given, do not need do anything to get address, just send command
        if options["tnpdump_addr"] is not None:
            addr_list = [options["tnpdump_addr"], ]
        else:
            # if tnpdump_addr not given, according to component to send command
            tnpdump_info = self.get_tnpdump_info(
                device=device,
                platform=options["platform"],
                node=options["node"],
                timeout=options["timeout"],
            )
            if options["component"] == "CP":
                addr_list = [tnpdump_info["cp_addr"], ]
            elif options["component"] == "SPU":
                addr_list = tnpdump_info["spu_addr_list"]
            else:
                addr_list = tnpdump_info["both_addr_list"]

        # create cmd list
        cmd_list = []
        for user_cmd in user_cmd_list:
            for addr in addr_list:
                cmd_list.append("cprod -A {} -c '{}'".format(addr, user_cmd))

        response_list = []
        # due to sometimes vty command cannot send to component, we need re-send command several times.
        for new_cmd in cmd_list:
            cmd_send_cnt = options["send_cnt"]
            while cmd_send_cnt:
                self.display(level="INFO", msg="send cmd: {}".format(new_cmd))
                response = self.send_shell_cmd(device=device, cmd=new_cmd)
                response_list.append(response)

                if re.search(r"Couldn't initiate connection", response, re.I):
                    cmd_send_cnt -= 1
                else:
                    cmd_send_cnt = 0

        return_value = "\n".join(response_list)
        if options["print_response"] is True:
            self.display(level="INFO", msg="{} return value:\n{}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def software_install(self, device, package, **kwargs):
        """For SRX platform to install software

        This method use cli cmd to install JunOS package, cli cmd base: "request system software add ..."

        :param STR package:
            **REQUIRED** Absolute package path on box.

        :param BOOL no_copy:
            *OPTIONAL*   no-copy option. Default: False

        :param BOOL no_validate:
            *OPTIONAL*   no_validate option. Default: False

        :param BOOL reboot:
            *OPTIONAL*   whether reboot device after package installed. If True, will check version whether install succeed. Default: True

        :param INT wait:
            *OPTIONAL*   only for "reboot=True". See self.reboot method for detail.

        :param INT timeout:
            *OPTIONAL*   only for "reboot=True". See self.reboot method for detail.

        :param INT interval:
            *OPTIONAL*   only for "reboot=True". See self.reboot method for detail.

        :return:
            True/False
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        options["package"] = package
        options["no_copy"] = kwargs.get("no_copy", False)
        options["no_validate"] = kwargs.get("no_validate", False)
        options["reboot"] = kwargs.get("reboot", True)
        options["wait"] = kwargs.get("wait", 60)
        options["timeout"] = kwargs.get("timeout", self.default["cli_reboot_timeout"])
        options["interval"] = kwargs.get("interval", 20)

        cmd_element_list = []
        cmd_element_list.append("request system software add {}".format(options["package"]))

        if options["no_copy"] is True:
            cmd_element_list.append("no-copy")

        if options["no_validate"] is True:
            cmd_element_list.append("no-validate")

        cmd = " ".join(cmd_element_list)
        self.display(msg="send cmd: {}".format(cmd), level="INFO")
        self.send_cli_cmd(device=device, cmd=cmd, channel="text", format="text", timeout=options["timeout"])

        if options["reboot"] is True:
            self.display(msg="start rebooting device...", level="INFO")
            reboot_status = self.reboot(device=device, wait=options["wait"], timeout=options["timeout"], interval=options["interval"])
            if reboot_status is False:
                self.display(msg="device reboot failed...", level="ERROR")
                self.display(msg="{} return value: {}".format(func_name, reboot_status), level="ERROR")
                return reboot_status
            else:
                self.display(msg="device reboot succeed...", level="INFO")

        self.display(msg="{} return value: {}".format(func_name, True), level="INFO")
        return True

    def reboot(self, device, **kwargs):
        """Reboot device and make sure all hardware component online

        As default, will use cmd "show chassis fpc pic-status" to show all components and they must online. In HA environment, will check 2
        nodes

        :param INT|STR wait:
            *OPTIONAL* Wait time to re-connect device. Default: 60 secs

        :param INT|STR timeout:
            *OPTIONAL* Rebooting timeout if device hardware component not online

        :param STR mode:
            *OPTIONAL* Rebooting mode that one of 'shell' or 'cli'. Default: 'cli'

                        cli - 'request system reboot'
                        shell - 'reboot'

        :param INT|STR check_interval:
            *OPTIONAL* Re-connect check interval. Default: 20

        :param BOOL on_parallel:
            *OPTIONAL* parallel reboot all DUT. default: None

                +  for 1 device, rebooting it as normal
                +  for 2+ devices, rebooting device on parallel as default.
                +  if on_parallel set True or False, force rebooting device on or not on parallel

            **Pay attention:** parallel reboot device will no reboot processing output logged.

        :return: Return True if all rebooting success, otherwise return False
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        options["device"] = device
        options['wait'] = int(kwargs.get('wait', 60))
        options['timeout'] = int(kwargs.get('timeout', self.default['cli_reboot_timeout']))
        options['mode'] = kwargs.get('mode', "cli")
        options["check_interval"] = int(kwargs.get("check_interval", 20))
        options["on_parallel"] = kwargs.get("on_parallel", None)

        if not isinstance(options["device"], (list, tuple)):
            options["device"] = (options["device"], )

        dev_cnt = len(options["device"])
        if options["on_parallel"] is None:
            if dev_cnt == 1:
                options["on_parallel"] = False
            else:
                options["on_parallel"] = True

        queue = Queue(32)
        def run_function(target, wait, timeout, interval, mode):
            """run function and put output to queue"""
            try:
                self.display(msg="now rebooting '{}'".format(target))
                result = target(wait=wait, timeout=timeout, interval=interval, mode=mode)
                queue.put(result)
            except (Exception, RuntimeError) as err:
                queue.put(False)
                self.display(msg="Got error while rebooting device '{}' with err: {}".format(target, err), level="ERROR")

        if options["on_parallel"] is False:
            for dev in options["device"]:
                try:
                    self.display(msg="rebooting '{}' ...".format(dev))
                    queue.put(dev.reboot(wait=options["wait"], timeout=options["timeout"], interval=options["check_interval"], mode=options["mode"]))
                except (Exception, RuntimeError) as err:
                    queue.put(False)
                    self.display(msg=err, level="ERROR")
        else:
            thread_list = []
            for dev in options["device"]:
                thread_list.append(threading.Thread(
                    target=run_function,
                    name=str(dev),
                    args=(dev.reboot, options["wait"], options["timeout"], options["check_interval"], options["mode"])))

            for thread in thread_list:
                self.display(msg="parallel rebooting '{}' ...".format(thread))
                thread.start()

            for thread in thread_list:
                self.display(msg="waiting for '{}' online...".format(thread))
                thread.join(timeout=options["timeout"] + 10)

        reboot_result_list = []
        while True:
            if queue.empty():
                break
            reboot_result_list.append(queue.get())

        self.display(msg="all device reboot status: {}".format(reboot_result_list), level="INFO")
        return False not in reboot_result_list and len(reboot_result_list) == dev_cnt

    def su(self, device, **kwargs):
        """Su to root permission

        :return: True/False
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        options["password"] = kwargs.get("password", self.default["root_password"])
        options["su_command"] = kwargs.get("su_command", "su -")

        if isinstance(device, (list, tuple)):
            options["device"] = device
        else:
            options["device"] = (device, )

        result_list = []
        for dev in options["device"]:
            result_list.append(dev.su(password=options["password"], su_command=options["su_command"]))

        self.display(msg="su result: {}".format(result_list))

        return_value = False not in result_list
        self.display(msg="{} return value: {}".format(func_name, return_value))
        return return_value

    def get_version_info(self, device, **kwargs):
        """Based on command "show version" to get device hostname, platform, image_info, etc...

        :param BOOL force_get:
            *OPTIONAL* Set True will send command to get info every time. If set False, only first
                       time send command to device. default: False

        :param INT|STR node:
            *OPTIONAL* Must be 0, 1, node0, node1 or BOTH. default: None

        :param INT timeout:
            *OPTIONAL* Timeout to run "show version" command

        :return:
            Return a DICT value have all version info, or return False

            For DICT value, if device working on StandardAlone mode, or working on HA mode but option 'node' is 0 or 1, will return DICT like below:

                {"hostname":     "...", "version":      "..."}

            If device working on HA mode and "node" is None, return DICT like:

                {
                    "node0":    {
                        "hostname":     "...",
                        "version":      "...",
                    },
                    "node1":    {
                        "hostname":     "...",
                        "version":      "...",
                    }
                }
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        options["force_get"] = kwargs.get("force_get", False)
        options["node"] = kwargs.get("node", None)
        options["timeout"] = int(kwargs.get("timeout", self.default["cli_show_timeout"]))

        if options["node"] is not None:
            options["node"] = self.tool.get_node_value(options["node"], mode="STR")

        # If already have version info for specific device
        dev_keyword = str(device)
        if dev_keyword in self.info["version_info"] and options["force_get"] is False:
            if options["node"] is not None:
                node_name = options["node"]
                return_value = self.info["version_info"][dev_keyword][node_name]
            else:
                return_value = self.info["version_info"][dev_keyword]

            self.display(level="INFO", msg="{} return value:\n{}".format(func_name, self.tool.pprint(return_value)))
            return return_value

        # First time to get version info
        xml_dict = self.send_cli_cmd(device=device, cmd="show version", format="xml", channel="pyez", timeout=options["timeout"])
        if "multi-routing-engine-results" in xml_dict:
            xml_dict = xml_dict["multi-routing-engine-results"]["multi-routing-engine-item"]

        # For HA, should a LIST that contain 2 node output, but sometimes node maybe lost that not a LIST
        # Even for SA, transit output to list
        if not isinstance(xml_dict, (list, tuple)):
            xml_dict = [xml_dict, ]

        info = {}
        for element in xml_dict:
            # Analyse HA return
            if "re-name" in element:
                node_name = str(element["re-name"])
                info[node_name] = {}
                info[node_name]["hostname"] = None
                info[node_name]["version"] = None
                info[node_name]["package_comment"] = None
                info[node_name]["product_model"] = None
                info[node_name]["product_name"] = None

                try:
                    info[node_name]["hostname"] = str(element["software-information"]["host-name"])
                    info[node_name]["version"] = str(element["software-information"]["junos-version"])
                    info[node_name]["package_information"] = str(element["software-information"]["package-information"])
                    info[node_name]["product_model"] = str(element["software-information"]["product-model"])
                    info[node_name]["product_name"] = str(element["software-information"]["product-name"])
                except KeyError:
                    pass

            # Analyse SA return
            else:
                info["hostname"] = None
                info["version"] = None
                info["package_comment"] = None
                info["product_model"] = None
                info["product_name"] = None

                try:
                    info["hostname"] = str(element["software-information"]["host-name"])
                    info["version"] = str(element["software-information"]["junos-version"])
                    info["package_comment"] = str(element["software-information"]["package-information"])
                    info["product_model"] = str(element["software-information"]["product-model"])
                    info["product_name"] = str(element["software-information"]["product-name"])
                except KeyError:
                    pass

        # restore for next time invoking
        self.info["version_info"][dev_keyword] = info

        if options["node"] is not None:
            node_name = options["node"]
            return_value = info[node_name]
        else:
            return_value = info

        self.display(level="INFO", msg="{} return value:\n{}".format(func_name, self.tool.pprint(return_value)))
        return return_value

    def get_tnpdump_info(self, device, **kwargs):
        """Based on tnpdump command to archive all info

        :param BOOL force_get:
            *OPTIONAL* Set True will send command to get info every time. If set False, only first
                       time send command to device. Default: False

        :param STR platform:
            *OPTIONAL* Device platform such as srx345, srx5600, srx1500, etc... Default: None

                       Will get platform by "show version" command as default.

        :param INT|STR node:
            *OPTIONAL* For HA topology. Valid value include 0, 1, "node0" or "node1". Default: None

        :param INT timeout:
            *OPTIONAL* Timeout to run "tnpdump" command

        :return:
            Return a DICT value have all archived tnpdump info, or return False

            For DICT value, if device working on StandardAlone mode, or working on HA mode but option 'node' is 0 or 1, will return DICT like below:

                {"cp_addr":     "...", "spu_addr_list":      "...", "both_addr_list":   "..."}

            If device working on HA mode and "node" is None, return DICT like:

                {
                    "node0":    {
                        "cp_addr":          "...",
                        "spu_addr_list":    "...",
                    },
                    "node1":    {
                        "cp_addr":          "...",
                        "spu_addr_list":    "...",
                    }
                }
        """
        options = {}
        options["force_get"] = kwargs.get("force_get", False)
        options["platform"] = kwargs.get("platform", None)
        options["node"] = kwargs.get("node", None)
        options["timeout"] = int(kwargs.get("timeout", self.default["cli_show_timeout"]))

        return device.get_tnpdump_info(**options)

    def get_coredump_file(self, device, **kwargs):
        """Get coredump file info based on 'show system coredump'

        :param STR return_mode:
            *OPTIONAL* set "counter" to return coredump file counter. default: None

        :param INT|STR timeout:
            *OPTIONAL* get device response timeout. default: 300

        :return:
            As default return a LIST which contain found coredump filename. If option return_mode="counter", it will return file counter.
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        options["return_mode"] = kwargs.get("return_mode", None)
        options["timeout"] = kwargs.get("timeout", self.default["cli_show_timeout"])

        response = self.send_cli_cmd(device=device, cmd="show system core-dumps", channel="text", format="text")
        coredump_files = []
        for line in response.splitlines():
            elements = re.split(r"\s+", line.strip())
            if re.match(r"[\-rwx]{10}", elements[0]) and re.search(r"core", elements[-1]):
                coredump_files.append(elements[-1])

        if options["return_mode"] == "counter":
            return_value = len(coredump_files)
        else:
            return_value = coredump_files

        self.display(msg="{} return value: {}".format(func_name, return_value))
        return return_value

    def feature_support_check(self, device, feature, **kwargs):
        """check device whether support given feature

        This method checking system license to check specific feature whether supported on device. Supported feature includes:

            +   "HE" - use "show version" to get platform and return:

                    *   True - "SRX4100", "SRX4200", "SRX4600", "SRX5400", "SRX5600", "SRX5800"
                    *   False - all of others

            +   "LE" - all platforms not in HE platform list.

            +   "LSYS", "LD", "LOGICAL_SYSTEM", "LOGICAL_DOMAIN" - use "show system license usage" to check device wheter support LSYS related feature

            +   "REMOTE_ACCESS_IPSEC_VPN", "IPSEC_VPN", "VPN" - use "show system license usage" to check device whether support IPSec related feature

            +   "VIRTUAL_APPLIANCE" - use "show system usage" to check device whether support virtual appliance feature

        All above feature keyword are case insensitive and "-" will be transited to "_", it means "Logical-System", "LOGICAL_SYSTEM",
        or "logical-system" are same.

        :param STR|LIST feature:
            **REQUIRED** feature string or list. will checking them one by one.

        :param STR|INT timeout:
            *OPTIONAL* timeout to get platform info

        :return:
            If device support all given features, return True, otherwise return False

        :example:
            status = self.feature_support_check(device=r0, feature="LSYS")
            status = self.feature_support_check(device=r0, feature=["HE", LSYS"])
        """
        self.display_title(msg=self.tool.get_current_function_name())

        # make sure all user feature element is uppercase and is LIST variable
        if isinstance(feature, (list, tuple)):
            feature_list = copy.deepcopy(feature)
        else:
            feature_list = (str(feature), )
        feature_list = self.tool.list_element_to_uppercase_transit(feature_list)
        options = {}
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_commit_timeout"]))

        supported_feature_list = (
            "HE",
            "LE",
            "LSYS", "LD", "LOGICAL_SYSTEM", "LOGICAL_DOMAIN",
            "REMOTE_ACCESS_IPSEC_VPN", "IPSEC_VPN", "VPN",
            "VIRTUAL_APPLIANCE",
            "IDP_SIG", "IDP_SIGNATURE",
            "APPID_SIG", "APPID_SIGNATURE",
        )

        # feature keyword validate checking
        msg = []
        for element in feature_list:
            if element not in supported_feature_list:
                msg.append("Feature name '{}' is not supported...\n".format(feature))

        if msg:
            msg.append("Supported Feature List: {}".format(supported_feature_list))
            self.display(msg="\n".join(msg), level="ERROR")
            return False

        # delete un-necessary license checking element to make sure whether need get license entry from device
        tmp_list = copy.deepcopy(feature_list)
        for no_license_element in ("HE", "LE"):
            if no_license_element in tmp_list:
                del tmp_list[tmp_list.index(no_license_element)]

        if tmp_list:
            device_license_list = self.send_cli_cmd(
                device=device,
                cmd="show system license usage",
                channel="pyez",
                format="xml",
                timeout=options["timeout"],
            )

        high_end_platforms = ("SRX4100", "SRX4200", "SRX4600", "SRX5400", "SRX5600", "SRX5800")
        return_value = True
        msg = []
        for element in feature_list:
            element = self.tool.underscore_and_uppercase_transit(element)
            have_valid_license = False

            # highend, lowend checking
            if element in ("HE", "LE"):
                version = self.get_version_info(device=device, timeout=options["timeout"])
                if version is False:
                    msg.append("cannot get device '{}' version info".format(device))
                    return False

                if "node0" in version:
                    platform = version["node0"]["product_model"].upper()
                else:
                    platform = version["product_model"].upper()

                if element == "HE":
                    have_valid_license = platform in high_end_platforms
                    if have_valid_license is True:
                        msg.append("Device '{}' is High-End platform".format(platform))
                    else:
                        msg.append("Device '{}' is not High-End platform".format(platform))
                        return_value = False
                else:
                    have_valid_license = platform not in high_end_platforms
                    if have_valid_license is True:
                        msg.append("Device '{}' is Low-End platform".format(platform))
                    else:
                        msg.append("Device '{}' is not Low-End platform".format(platform))
                        return_value = False

                continue

            # for LSYS license
            elif element in ("LSYS", "LD", "LOGICAL_SYSTEM", "LOGICAL_DOMAIN"):
                have_valid_license = self.license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name="logical-system",
                    licensed=(1, "ge"),
                )

            # VPN related license
            elif element in ("REMOTE_ACCESS_IPSEC_VPN", "IPSEC_VPN", "VPN"):
                have_valid_license = self.license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name=("vpn", "in"),
                    licensed=(1, "ge"),
                )

            elif element in ("VIRTUAL_APPLIANCE", ):
                have_valid_license = self.license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name="Virtual Appliance",
                    licensed=(1, "ge"),
                )

            elif element in ("IDP_SIG", "IDP_SIGNATURE"):
                have_valid_license = self.license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name="idp-sig",
                    licensed=(1, "ge"),
                )

            elif element in ("APPID_SIG", "APPID_SIGNATURE"):
                have_valid_license = self.license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name="appid-sig",
                    licensed=(1, "ge"),
                )

            else:   # pragma: no cover
                pass

            if have_valid_license:
                msg.append("Feature '{}' has supported on device".format(element))
            else:
                msg.append("Feature '{}' is not supported on device".format(element))
                return_value = False

        self.display(msg="\n{}".format("\n".join(msg), level="INFO"))
        self.display(msg="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def ha_get_node_name(self, device):
        """Get given device handler's node name. such as 'node0', 'node1'

        :return:
            Return node name like 'node0/node1', or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())

        try:
            return_value = device.node_name()
        except Exception as err:
            self.display(level="ERR", msg=err)
            return_value = False

        self.display(level="INFO", msg="return value:\n{}".format(return_value))
        return return_value


    def ha_get_rg_status(self, device, **kwargs):
        """Get Redundancy Group's status from given device handler

        :param int/list rg:
            *OPTIONAL* RG number or list of RG number. Default: 0

        :return:
            If option rg is an INT, return STRING such as 'primary', 'secondary', 'hold', etc

            If option rg is a LIST or TUPLE, return LIST that contain all RG's status

            Any issue return False
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        options["rg"] = kwargs.get("rg", 0)

        rg_list = []
        if isinstance(options["rg"], (str, int)):
            rg_list.append(options["rg"])
        elif isinstance(options["rg"], (list, tuple)):
            rg_list = copy.deepcopy(options["rg"])
        else:
            raise TypeError("option 'rg' must INT, LIST or TUPLE, not '{}'".format(options["rg"]))

        rg_status_list = []
        for rg in rg_list:
            try:
                result = device.node_status(rg=str(rg))
                if not isinstance(result, bool):
                    result = str(result)
            except TypeError:
                result = False

            rg_status_list.append(result)

        if len(rg_status_list) == 1:
            return_value = rg_status_list[0]
        else:
            return_value = rg_status_list

        self.display(level="INFO", msg="{} return_value:\n{}".format(func_name, return_value))
        return return_value

    def ha_do_failover(self, device, node=0, rg=0, **kwargs):
        """do failover and for redundancy-group

        :param INT|STR node:
            *OPTIONAL* node number such as 0 or 1.

        :param INT|STR|LIST|TUPLE rg:
            *OPTIONAL* RG number or list want to do failover

        :param INT|STR rg0_waiting_time:
            *OPTIONAL* sometimes set waiting time after do failover for rg0. default: 0

        :param BOOL force:
            *OPTIONAL* Whether force failover. Force failover may cause connection broken. Default: False

        :param INT check_cnt:
            *OPTIONAL* With option "check_interval" to do loop checking.
                       Default: If rg=0, check_cnt=15; otherwise (1..128) check_cnt=2

        :param INT|FLOAT check_interval:
            *OPTIONAL* With option "check_cnt" to do loop checking.
                       Default: If rg=0, check_cnt=60; otherwise (1..128) check_cnt=10

        :return:
            Return True or False to indicate all rg(s) whether failover success.
        """
        func_name = self.tool.get_current_function_name()
        self.display_title(msg=func_name)

        options = {}
        options["node"] = node
        options["rg"] = rg
        options["force"] = kwargs.get("force", False)
        options["rg0_waiting_time"] = float(kwargs.get("rg0_waiting_time", 0))

        rg_list = []
        if isinstance(options["rg"], (str, int)):
            rg_list.append(options["rg"])
        elif isinstance(options["rg"], (list, tuple)):
            rg_list = list(copy.deepcopy(options["rg"]))
        else:
            raise TypeError("option 'rg' must INT, STR, LIST or TUPLE but got '{}'".format(type(options["rg"])))

        if not isinstance(options["node"], (str, int)):
            raise TypeError("option 'node' must INT or STR but got '{}'".format(type(options["node"])))

        result = []
        for element in rg_list:
            if element in (0, "0"):
                options["check_interval"] = float(kwargs.get("check_interval", 60))
                options["check_cnt"] = int(kwargs.get("check_cnt", 15))
            else:
                options["check_interval"] = float(kwargs.get("check_interval", 10))
                options["check_cnt"] = int(kwargs.get("check_cnt", 2))

            self.display(msg="do failover for redundancy-group {}".format(element), level="INFO")
            response = device.failover(
                rg=str(element),
                node=str(options["node"]),
                force=options["force"],
                check_cnt=options["check_cnt"],
                check_interval=options["check_interval"],
            )

            result.append(response)

        self.display(level="INFO", msg="failover result: {}".format(result))
        return_result = False if False in result else True
        self.display(level="INFO", msg="{} return value: {}".format(func_name, return_result))
        return return_result
