# coding: UTF-8
# pylint: disable=invalid-name
"""Services Offload (SOF) methods"""

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2019'

import re
import time

from jnpr.toby.hldcl import device as dev
from jnpr.toby.security.chassis.chassis import chassis
from jnpr.toby.utils.flow_common_tool import flow_common_tool


class services_offload(object):
    """All services offload related methods"""
    def __init__(self):
        """Init processing"""
        self.tool = flow_common_tool()
        self.chassis = chassis()
        self.hidden_info = {}

    def get_ioc_slot_number(self, device, **kwargs):
        """Get IOC slot id

        This method based on command "show chassis fpc pic-status" and return ioc's slot number. This is useful to enable/disable services-offload
        configuration later.

        :param INT|STR|LIST except_slot_number:
            *OPTIONAL* Given slot number(s) will not added to list. Default: None

        :param INT|STR largest_slot_number:
            *OPTIONAL* For HA topology. Ignore slot id greater or equal given slot number. Default: 6

        :param BOOL force_get:
            *OPTIONAL* If set True, will get ioc_slot_number list every time. Set False will return ioc_slot_number from cache.

            **IMPORTANT: If 'force_get' is False, this method will return ioc_slot_number from cache, it means will not remove 'except_slot_number'.**
            **If need except more slot number, pls set 'force_get'=True**

            Default: False

        :return:
            Return a LIST that contain all IOC's slot number
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["except_slot_number"] = kwargs.pop("except_slot_number", [])
        options["largest_slot_number"] = int(kwargs.pop("largest_slot_number", 6))
        options["force_get"] = self.tool.check_boolean(kwargs.pop("force_get", False))

        if not isinstance(options["except_slot_number"], (list, tuple)):
            options["except_slot_number"] = (options["except_slot_number"], )

        if len(options["except_slot_number"]) != 0 \
           or func_name not in self.hidden_info \
           or str(device) not in self.hidden_info[func_name]:
            options["force_get"] = True

        if options["force_get"] is False and str(device) in self.hidden_info[func_name]:
            return_value = self.hidden_info[func_name][str(device)]
            device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
            return return_value

        ioc_number_sets = set()
        response = dev.execute_cli_command_on_device(device=device, command="show interface terse", channel="text", format="text")
        for line in response.splitlines():
            match = re.search(r"xe\-(\d+)\/\d+\/\d+\s+", line)
            if match and int(match.group(1)) <= options["largest_slot_number"]:
                ioc_number_sets.add(int(match.group(1)))

        for except_number in options["except_slot_number"]:
            except_number = int(except_number)
            if except_number in ioc_number_sets:
                ioc_number_sets.remove(except_number)

        return_value = list(ioc_number_sets)
        if func_name not in self.hidden_info:
            self.hidden_info[func_name] = {}
        self.hidden_info[func_name][str(device)] = return_value

        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def set_services_offload(self, device, ioc_slot_number, **kwargs):
        """Enable/Disable services offload on FPC

        :param INT|STR|LIST ioc_slot_number:
            *MANDATORY* IOC slot number or number list to enable/disable services-offload.

        :param STR action:
            *OPTIONAL* Enable or Disable services-offload on given ioc slot number(s). Default: Enable

        :param STR reboot_mode:
            *OPTIONAL* One of "None", "Reboot", "Gracefully", "Immediately" or "Soft". Case-insensitive. Default: None

            - None: Do not reboot
            - Reboot: Reboot device by command: "request system reboot"
            - Gracefully: by command: "restart chassis-control gracefully"
            - Immediately: by command: "restart chassis-control immediately"
            - Soft: by command: "restart chassis-control soft"

        :param BOOL waiting_for_pic_online:
            *OPTIONAL* Waiting for all PIC online after device reboot. This option only for option 'reboot_mode' is not None. Default: True

        :param STR|LIST waiting_for_pic_online_except_component:
            *OPTIONAL* Set security.chassis.chassis.waiting_for_pic_online for detail. Default: ()

        :param INT|STR waiting_for_pic_online_check_interval:
            *OPTIONAL* Check interval (sec) during waiting_for_pic_online. Default: 30

        :param INT|STR waiting_for_pic_online_check_counter:
            *OPTIONAL* Check counter (sec) during waiting_for_pic_online. Default: 20

        :return:
            True/False for services-offload enabled/disabled for given ioc_slot_number.
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["ioc_slot_number"] = ioc_slot_number
        options["action"] = str(kwargs.pop("action", "Enable")).upper()
        options["reboot_mode"] = str(kwargs.pop("reboot_mode", None)).lower()
        options["waiting_for_pic_online"] = self.tool.check_boolean(kwargs.pop("waiting_for_pic_online", True))
        options["waiting_for_pic_online_except_component"] = kwargs.pop("waiting_for_pic_online_except_component", ())
        options["waiting_for_pic_online_check_interval"] = int(kwargs.pop("waiting_for_pic_online_check_interval", 30))
        options["waiting_for_pic_online_check_counter"] = int(kwargs.pop("waiting_for_pic_online_check_counter", 20))

        if not isinstance(options["ioc_slot_number"], (list, tuple)):
            options["ioc_slot_number"] = (options["ioc_slot_number"], )

        if options["action"] not in ("ENABLE", "DISABLE"):
            raise ValueError("{}: option 'action' must be enable or disable but got '{}'".format(func_name, options["action"]))

        if options["reboot_mode"] not in ("none", "reboot", "gracefully", "immediately", "soft"):
            raise ValueError("{}: option 'reboot_mode' must be 'none', 'reboot', 'gracefully', 'immediately' or 'soft'".format(func_name))

        action_str = "set" if options["action"] == "ENABLE" else "delete"
        cmds = []
        for number in options["ioc_slot_number"]:
            cmds.append("{} chassis fpc {} np-cache".format(action_str, number))
        status = dev.execute_config_command_on_device(device=device, command=cmds, commit=True)

        if options["reboot_mode"] == "none":
            device.log(message="{} return value: {}".format(func_name, status), level="INFO")
            return status

        elif options["reboot_mode"] == "reboot":
            if device.is_ha() is True:
                status = dev.reboot_device(device=device, timeout=1200, all=True)
            else:
                status = dev.reboot_device(device=device, timeout=1200)

        else:
            status = dev.execute_cli_command_on_device(
                device=device,
                channel="text",
                format="text",
                command="restart chassis-control {}".format(options["reboot_mode"]),
            )

        if options["waiting_for_pic_online"] is False:
            device.log(message="{} return value: {}".format(func_name, status), level="INFO")
            return status

        time.sleep(10)
        status = self.chassis.waiting_for_pic_online(
            device=device,
            except_component=options["waiting_for_pic_online_except_component"],
            check_interval=options["waiting_for_pic_online_check_interval"],
            check_counter=options["waiting_for_pic_online_check_counter"],
        )
        device.log(message="{} return value: {}".format(func_name, status), level="INFO")
        return status
