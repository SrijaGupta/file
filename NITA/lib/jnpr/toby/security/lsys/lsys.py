# coding: UTF-8
"""Have all Logical-system and Logic-domain related methods

Below options are have same behavior:

+   device (OBJECT) - Device handler

+   timeout (INT) - Timeout for send command to device and waiting for response
"""
# pylint: disable=invalid-name,consider-iterating-dictionary

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.security.chassis.chassis import chassis


class lsys(object):
    """All Logical-system and Logic-domain methods"""
    def __init__(self):
        """Init processing"""
        self.tool = flow_common_tool()
        self.chassis = chassis()

        self.default = {
            "CLI_SHOW_TIMEOUT":     300,
            "CLI_COMMIT_TIMEOUT":   300,
        }

        self.hidden_info = {}

    def change_multitenancy_mode(self, device, mode="lsys", **kwargs):
        """switch logical-system mode to tradition or logical-domain mode.

        Base on command "set system processes multitenancy mode" to change LSYS mode, and reboot device if needed.

        This method support both SA/HA. For HA setup, will reboot 2 nodes in parallel and waiting for all FPC online

        :param STR mode:
            *OPTIONAL* One of lsys, ld, logical-system or logical-domain (case insensitive). default: lsys

        :param BOOL reboot_if_need:
            *OPTIONAL* If multitenancy mode changed and need reboot, reboot device (SA) or all nodes (HA) in parallel. default: True

        :param INT|STR reboot_timeout:
            *OPTIONAL* reboot device timeout. default: 600

        :param BOOL checking_fpc_online:
            *OPTIONAL* After rebooting, waiting all FPC PIC online by loop checking. default: True

        :param INT|STR fpc_online_check_counter:
            *OPTIONAL* Loop counter to check FPC PIC online. default: 10

        :param INT|STR fpc_online_check_interval:
            *OPTIONAL* Loop interval between each checking. default: 30

        :param STR|LIST|TUPLE fpc_online_except_component:
            *OPTIONAL* As default, all device component must online, but you can give one or more component name here to avoid checking.

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

        :param INT|STR timeout:
            *OPTIONAL* show and commit timeout. default: 300

        :return:
            If lsys mode change succeed and implemented, and all PIC onlined, return True. Otherwise return False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["mode"] = mode.strip().upper()
        options["reboot_if_need"] = kwargs.get('reboot_if_need', True)
        options["reboot_timeout"] = int(kwargs.get("reboot_timeout", 600))
        options["checking_fpc_online"] = kwargs.get("checking_fpc_online", True)
        options["fpc_online_check_counter"] = int(kwargs.get("fpc_online_check_counter", 10))
        options["fpc_online_check_interval"] = int(kwargs.get("fpc_online_check_interval", 30))
        options["fpc_online_except_component"] = kwargs.get("fpc_online_except_component", ())
        options["timeout"] = int(kwargs.get("timeout", self.default["CLI_COMMIT_TIMEOUT"]))

        if options["mode"] in ("LSYS", "LOGICAL-SYSTEM"):
            wanted_mode = "logical-system"
        elif options["mode"] in ("LD", "LOGICAL-DOMAIN"):
            wanted_mode = "logical-domain"
        else:
            raise ValueError("'mode' must be 'LSYS' 'LD', 'Logical-system' or 'Logical-domain' but got '{}'".format(options["mode"]))

        # make sure operate on primary node for HA setup
        status = device.is_ha()
        if status is True:
            if device.node0.is_master() is True:
                primary_device = device.node0
            else:
                primary_device = device.node1
        else:
            primary_device = device

        status = dev.execute_config_command_on_device(
            device=primary_device,
            command="set system processes multitenancy mode {}".format(wanted_mode),
            get_response=False,
            commit=True,
            timeout=options["timeout"],
        )
        if status is False:
            device.log(message="commit multitenancy mode configuration failed.", level="ERROR")
            return status

        show_cmd = "show system processes multitenancy"
        response_dict = dev.execute_cli_command_on_device(device=primary_device, command=show_cmd, channel="pyez", format="xml", xml_to_dict=True)
        device.log(message="show command response:\n{}".format(self.tool.pprint(response_dict)), level="DEBUG")

        if "multi-routing-engine-results" in response_dict:
            response_dict = response_dict["multi-routing-engine-results"]["multi-routing-engine-item"]

        dev_configure_mode = response_dict["show-mtenancy"]["mtenancy-mode-config"]
        dev_configure_status = ""
        if "mtenancy-mode-config-status" in response_dict["show-mtenancy"]:
            dev_configure_status = response_dict["show-mtenancy"]["mtenancy-mode-config-status"]

        dev_running_mode = response_dict["show-mtenancy"]["mtenancy-mode-running"]
        dev_configure_status = ""
        if "mtenancy-mode-running-status" in response_dict["show-mtenancy"]:
            dev_configure_status = response_dict["show-mtenancy"]["mtenancy-mode-running-status"]

        if dev_configure_mode == dev_running_mode and not re.search(r"must reboot", dev_configure_status):
            device.log(message="multitenancy is working on '{}' mode and do not need rebooting.".format(dev_running_mode), level="INFO")
            device.log(message="{} return value: True".format(func_name), level="INFO")
            return True

        dev.reboot_device(device=device, all=True)

        # waiting for all PIC online
        return_value = self.chassis.waiting_for_pic_online(
            device=device,
            except_component=options["fpc_online_except_component"],
            check_counter=options["fpc_online_check_counter"],
            check_interval=options["fpc_online_check_interval"],
        )

        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value
