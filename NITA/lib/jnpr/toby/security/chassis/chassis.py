# coding: UTF-8
# pylint: disable=invalid-name
"""All keywords for CHASSIS component

Below options are have same behavior:

+   device (OBJECT) - Device handler

+   timeout (INT) - Timeout for send command to device and waiting for response
"""
__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import time

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool


class chassis(object):
    """All FLOW related methods"""
    def __init__(self):
        """Init processing"""
        super().__init__()
        self.tool = flow_common_tool()

        self.default = {
            "cli_show_timeout":         120,
        }

        self.info = {
            "chassis_hardware_info":    {},
            "chassis_fpc_pic_info":     {},
        }

    def get_chassis_hardware_info(self, device, **kwargs):
        """Based on command "show chassis hardware" to get all hardware infomation

        :param BOOL force_get:
            *OPTIONAL* Set True will send command to get info every time. If set False, only first time send command to device. Default: False

        :param INT timeout:
            *OPTIONAL* Timeout to run "show chassis hardware" command

        :return:
            Return a DICT value have all hardware info, or return False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["force_get"] = kwargs.get("force_get", False)
        options["timeout"] = int(kwargs.get("timeout", self.default["cli_show_timeout"]))
        options["unittest"] = kwargs.get("unittest", None)

        # return immediatelly if have info in previous
        dev_keyword = str(device)
        if dev_keyword not in self.info["chassis_hardware_info"] or options["force_get"] is True:
            self.info["chassis_hardware_info"][dev_keyword] = dev.execute_cli_command_on_device(
                device=device,
                command="show chassis hardware",
                format="xml",
                channel="pyez",
                xml_to_dict=True,
                timeout=options["timeout"],
            )

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(self.info["chassis_hardware_info"][dev_keyword])), level="INFO")
        return self.info["chassis_hardware_info"][dev_keyword]

    def get_chassis_fpc_info(self, device, **kwargs):
        """Based on cmd "show chassis fpc pic-status" to get all pic information

        :param BOOL force_get:
            *OPTIONAL* set True will send cmd to get info every time. Or set False to get info from previous. Default: False

        :param INT timeout:
            *OPTIONAL* get info timeout. Default: {}

        :return:
            Return a DICT value have all pic info, or return False
        """.format(self.default["cli_show_timeout"])
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["force_get"] = kwargs.get("force_get", False)
        options["timeout"] = int(kwargs.get("timeout", self.default["cli_show_timeout"]))

        # return immediatelly if have info in previous
        dev_keyword = str(device)
        if dev_keyword in self.info["chassis_fpc_pic_info"] and options["force_get"] is False:
            device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(self.info["chassis_fpc_pic_info"][dev_keyword])), level="INFO")
            return self.info["chassis_fpc_pic_info"][dev_keyword]

        self.info["chassis_fpc_pic_info"][dev_keyword] = dev.execute_cli_command_on_device(
            device=device,
            command="show chassis fpc pic-status",
            format="xml",
            channel="pyez",
            xml_to_dict=True,
            timeout=options["timeout"],
        )

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(self.info["chassis_fpc_pic_info"][dev_keyword])), level="INFO")
        return self.info["chassis_fpc_pic_info"][dev_keyword]

    def waiting_for_pic_online(self, device, **kwargs):
        """Waiting a while to make sure wantted pic online

        Based on cmd "show chassis fpc pic-status", this method checking wantted pic whether online. This is useful for device reboot

        :param STR|LIST|TUPLE except_component:
            **OPTIONAL** As default, all device component must online, but you can give one or more component name here to avoid checking.

            For example:

                ```
                Slot 0   Online       SRX5k SPC II
                  PIC 0  Offline      SPU Cp
                  PIC 1  Online       SPU Flow
                  PIC 2  Online       SPU Flow
                  PIC 3  Offline      SPU Flow
                Slot 2   Online       SRX5k IOC II
                  PIC 0  Online       10x 10GE SFP+
                ```

            Above output will create an internal offline list: ["SLOT 0 PIC 0", "SLOT 0 PIC 3", "PIC 0", "PIC 3"], you can list these
            keywords in this option to skip them. This means you can just skip "PIC 0" for all SLOT, or set "SLOT 0 PIC 0" for specific PIC.

            By the way, component keyword is case insensitive, this means keyword "pic 0", "PIC 0", or "Slot 0 Pic 0" all match above output

            For IOC 3, 2 PICs always offline, and this method will skip them automatically.

        :param INT check_counter:
            **OPTIONAL** how many times to checking device status. Default: 10

        :param INT check_interval:
            **OPTIONAL** waiting interval between checking. Default: 30

        :param INT timeout:
            **OPTIONAL** timeout to get device response.

        :return:
            True/False. Or raise ValueError for invalid option

        :example:
            status = self.waiting_for_pic_online(device=r0, except_component=("PIC 0", "Slot 0", "Slot 1 PIC 2"), check_counter=10, check_interval=60)
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["except_component"] = kwargs.get("except_component", ())
        options["check_counter"] = int(kwargs.get("check_counter", 10))
        options["check_interval"] = int(kwargs.get("check_interval", 30))
        options["timeout"] = int(kwargs.get("timeout", self.default["cli_show_timeout"]))

        if isinstance(options["except_component"], str):
            options["except_component"] = (options["except_component"], )

        checking_result = False
        get_pic_status_cmd = "show chassis fpc pic-status"
        for index in range(1, options["check_counter"] + 1):
            ioc3_component_cnt = 0
            device.log(message="Index {:02d}: FPC PIC status check...".format(index), level="INFO")

            response = dev.execute_cli_command_on_device(
                device=device,
                command=get_pic_status_cmd,
                channel="pyez",
                format="xml",
                xml_to_dict=True,
                timeout=options["timeout"],
            )
            if response is False:
                device.log(
                    message="cannot got FPC PIC status from device, waiting {} secs for next checking...".format(options["check_interval"]),
                    level="INFO",
                )
                time.sleep(options["check_interval"])
                continue

            if "multi-routing-engine-results" in response:
                response = response["multi-routing-engine-results"]["multi-routing-engine-item"]
                if not isinstance(response, (list, tuple)):
                    device.log(
                        message="only one node response occurred, waiting {} secs for next checking...".format(options["check_interval"]),
                        level="INFO",
                    )
                    time.sleep(options["check_interval"])
                    continue

            # SA always a DICT, but HA is a LIST that contain 2 nodes' response
            if not isinstance(response, (list, tuple)):
                response = [response, ]

            offline_component_list = []
            for node_item in response:
                try:
                    fpc_list = node_item["fpc-information"]["fpc"]
                except (TypeError, KeyError):
                    offline_component_list.append("FPC")
                    device.log(message="No FPC status contained.", level="INFO")
                    continue

                if not isinstance(fpc_list, (list, tuple)):
                    fpc_list = [fpc_list, ]

                for fpc in fpc_list:
                    fpc_state = fpc["state"] if "state" in fpc else None
                    fpc_slot = fpc["slot"] if "slot" in fpc else "Unknown"
                    fpc_description = fpc["description"] if "description" in fpc else "Unknown"
                    pic_list = fpc["pic"] if "pic" in fpc else None
                    fpc_name = "SLOT {}".format(fpc_slot)

                    if fpc_state is None or not re.match(r"Online", fpc_state.strip(), re.I):
                        if fpc_name not in offline_component_list:
                            offline_component_list.append(fpc_name)
                        continue

                    if re.search(r"\s+IOC3\s+", fpc_description):
                        device.log(message="'{}' card found on '{}'.".format(fpc_description, fpc_name), level="INFO")
                        ioc3_component_cnt += 1

                    if not pic_list:
                        device.log(message="no PIC infomation for FPC '{}'".format(fpc_description), level="INFO")
                        continue

                    if not isinstance(pic_list, (list, tuple)):
                        pic_list = [pic_list, ]

                    for pic in pic_list:
                        pic_slot = pic["pic-slot"] if "pic-slot" in pic else "Unknown"
                        pic_state = pic["pic-state"] if "pic-state" in pic else None
                        # pic_type = pic["pic-type"] if "pic-type" in pic else "Unknown"
                        pic_name = "{} PIC {}".format(fpc_name, pic_slot)

                        if pic_state is None or not re.match(r"Online", pic_state.strip(), re.I):
                            if pic_name not in offline_component_list:
                                offline_component_list.append(pic_name)

            if offline_component_list:
                device.log(message="OFFLINE component: {}".format(offline_component_list), level="INFO")

                for item in options["except_component"]:
                    item = item.upper()
                    if item in offline_component_list:
                        del offline_component_list[offline_component_list.index(item)]

            # IOC3 card always have 2 offline PIC
            if not offline_component_list or len(offline_component_list) == ioc3_component_cnt * 2:
                checking_result = True
                device.log(message="All FPC and PIC onlined...", level="INFO")
                break

            device.log(message="Waiting '{}' secs for next component checking...".format(options["check_interval"]), level="INFO")
            time.sleep(options["check_interval"])

        device.log(message="{} return value: {}".format(func_name, checking_result), level="INFO")
        return checking_result
