# coding: UTF-8
"""Have all NAT module methods

NAT module keywords that obey MTS (Master Test Script) behavior.

In this module, some options have same behavior of all method:

+   device

    Device handler will send command to it. For HA device, just set main handler such as r0, never use r0.node0 or
    r0.node1.

+   more_options

    Will concatenate given string to base command. For example: base command "show security nat source deterministic"
    used for method "fetch_source_nat_deterministic", you can set more_options="host-ip x.x.x.x" to reduce output.

    Tips 1: Do not set "| display xml" or "no-more" to this option

    Tips 2: Several method may have another option called "options", it is now deprecated. more_options have higher
            priority now.

+   return_mode

    Even different method have specific value for this option, below values have same behavior in this module.

    -   counter: offen appeared in 'verify_' method. For example: method 'verify_flow_session' always invoke
                 'fetch_flow_session' to get all sessions from device, then filter these sessions then return True/False
                 to indicate whether find wanted session. But if return_mode="counter", it will return matched session
                 counter instead of True/False.

    -   flat_dict: offen appeared in 'fetch_' method. As normal, 'fetch_' method will send command to device then
                   transit xml response to complex DICT structure. Here is a complex DICT for SNAT pool information:

                   [
                        {
                            "source-nat-pool-detail-information": {
                                "source-nat-pool-info-entry": {
                                    "address-pool-hits": "495",
                                    "pool-id": "4",
                                    "pool-name": "root_src_v4_pat",
                                    "port-overloading-factor": "1",
                                    "routing-instance-name": "default",
                                    "source-pool-address-assignment": "no-paired",
                                    "source-pool-address-range": {
                                        "address-range-high": "200.0.1.11",
                                        "address-range-low": "200.0.1.11",
                                        "single-port": "3",
                                        "twin-port": "0"
                                    },
                                    "source-pool-address-range-sum": {
                                        "single-port-sum": "3",
                                        "twin-port-sum": "0"
                                    },
                                    "source-pool-blk-atv-timeout": "0",
                                    "source-pool-blk-interim-log-cycle": "0",
                                    "source-pool-blk-log": "Enable",
                                    "source-pool-blk-max-per-host": "8",
                                    "source-pool-blk-size": "1",
                                    "source-pool-blk-total": "2500",
                                    "source-pool-blk-used": "4",
                                    "source-pool-last-blk-rccl-timeout": "0",
                                    "source-pool-port-translation": "[10001, 12500]",
                                    "total-pool-address": "1"
                                }
                            }
                        },
                    ]

                    This is difficult to check complex dict in script. So you can set 'return_mode=flat_dict' let
                    complex dict structure to simple dict with long keyword. The long keyword only have lowercase
                    character and underscore. For example, above complex dict will be transited to:

                    [
                        {
                            source_nat_pool_info_entry_address_pool_hits': '495',
                            source_nat_pool_info_entry_pool_id': '4',
                            source_nat_pool_info_entry_pool_name': 'root_src_v4_pat',
                            source_nat_pool_info_entry_port_overloading_factor': '1',
                            source_nat_pool_info_entry_routing_instance_name': 'default',
                            source_nat_pool_info_entry_source_pool_address_assignment': 'no-paired',
                            source_nat_pool_info_entry_source_pool_address_range_address_range_high': '200.0.1.11',
                            source_nat_pool_info_entry_source_pool_address_range_address_range_low': '200.0.1.11',
                            source_nat_pool_info_entry_source_pool_address_range_single_port': '3',
                            source_nat_pool_info_entry_source_pool_address_range_twin_port': '0',
                            source_nat_pool_info_entry_source_pool_address_range_sum_single_port_sum': '3',
                            source_nat_pool_info_entry_source_pool_address_range_sum_twin_port_sum': '0',
                            source_nat_pool_info_entry_source_pool_blk_atv_timeout': '0',
                            source_nat_pool_info_entry_source_pool_blk_interim_log_cycle': '0',
                            source_nat_pool_info_entry_source_pool_blk_log': 'Enable',
                            source_nat_pool_info_entry_source_pool_blk_max_per_host': '8',
                            source_nat_pool_info_entry_source_pool_blk_size': '1',
                            source_nat_pool_info_entry_source_pool_blk_total': '2500',
                            source_nat_pool_info_entry_source_pool_blk_used': '4',
                            source_nat_pool_info_entry_source_pool_last_blk_rccl_timeout': '0',
                            source_nat_pool_info_entry_source_pool_port_translation': '[10001, 12500]',
                            source_nat_pool_info_entry_total_pool_address': '1',
                        },
                    ]

In this module, all keywords are support both Lowend, Highend SRX device, and support SA, HA environment also. Below
rules are implemented for all methods:

+   For 'fetch_' method, send command to device for **XML** response. Then transit XML object to python LIST and each
    element is python DICT. For HE platform, will got multiple elements LIST for each FPC.PIC. For LE platform, will got
    1 element LIST.

+   For 'verify_' method, they all have dynamic options. 'verify_' method always invoke 'fetch_' keyword to get XML
    response, and make all given options to internal filter list, then filter xml elements one by one. Dynamic options
    avoid change source code frequently, but you have to set option carefully because wrong option cause no element
    matched.

    Value for specific option should be a string that separated by blank and can be splited to value and compare mode.
    For example:

    -   "192.168.1.0/24 in": find IP that contained in network 192.168.1.0/24
    -   "192.168.1.1 eq": find IP that equal "192.168.1.1"
    -   "FPC0 in": find string that contain FPC0
    -   "100 ge" or "100": find integer that great and equal then 100

    Compare characters are case insensitive, and list as below:

    -   "in" or "CONTAIN": Used for "INT Range", "IP", "NETWORK", "DATE", "STRING". This is default mode for "STRING"

    -   "eq" or "EQUAL": Used for "INT Range", "IP", "NETWORK", "DATE", "STRING". This is default mode for all type
                         except "STRING"

    -   "ne" or "NOT_EQUAL": Used for "INT Range", "IP", "NETWORK", "DATE", "STRING".

    -   "ge" or "GREAT_OR_EQUAL_THAN": device value >= wanted value. Used for "INT", "FLOAT" or "DATE"

    -   "gt" or "GREAT_THAN": device value > wanted value. Used for "INT", "FLOAT" or "DATE"

    -   "le" or "LESS_OR_EQUAL_THAN": device value <= wanted value. Used for "INT", "FLOAT" or "DATE"

    -   "lt" or "LESS_THAN": device value < wanted value. Used for "INT", "FLOAT" or "DATE"

"""
# pylint: disable=invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import copy
import re

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool


class nat():
    """All NAT related methods"""
    def __init__(self):
        """Init processing"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()

        self.default = {
            "cli_show_timeout":     300,
            "indent":               4,
        }

        self.debug_to_stdout = False

        # compatible support
        self.get_source_nat_interface_nat_ports = self.fetch_source_nat_interface_nat_ports
        self.get_source_nat_deterministic = self.fetch_source_nat_deterministic
        self.get_source_nat_pool = self.fetch_source_nat_pool
        self.get_source_nat_rule = self.fetch_source_nat_rule
        self.get_source_nat_port_block = self.fetch_source_nat_port_block
        self.get_source_nat_resource_usage = self.fetch_source_nat_resource_usage
        self.get_pool_id_owner_spu = self.fetch_pool_id_owner_spu
        self.get_pst_nat_table_summary = self.fetch_pst_nat_table_summary
        self.get_pst_nat_table_entry = self.fetch_pst_nat_table_entry
        self.search_source_nat_interface_nat_ports = self.verify_source_nat_interface_nat_ports
        self.search_source_nat_deterministic = self.verify_source_nat_deterministic
        self.search_source_nat_pool = self.verify_source_nat_pool
        self.search_source_nat_rule = self.verify_source_nat_rule
        self.search_source_nat_port_block = self.verify_source_nat_port_block
        self.search_source_nat_resource_usage = self.verify_source_nat_resource_usage

    def fetch_source_nat_interface_nat_ports(self, device, **kwargs):
        """Get SNAT interface-nat-ports info from LE/HE SA/HA topology

        Based on cmd: show security nat interface-nat-port

        Whatever option "node" given, this method always get all node's response from HA topology.

        :param INT|STR node:
            *OPTIONAl* Node number only for HA topology. default: all

        :param STR lsys_name:
            *OPTIONAL* lsys name. default: None

        :param STR more_options:
            *OPTIONAL* Add more option string tail of basic cmd: "show security nat interface-nat-ports". Make sure new option don't impact
                       xml structure.

        :param INT timeout:
            *OPTIONAl* Get info response timeout.

        :return:
            Return a normal LIST like below if return_mode="normal", every list element contain an interface nat ports entry

                LIST = [
                    {
                        "pool_index":                   value,
                        "single-ports-allocated":       value,
                        "re_name":                      "node0",            << HA topo only
                        ...
                    },
                    {
                        "pool_index":                   value,
                        "single-ports-allocated":       value,
                        "re_name":                      "node0",            << HA topo only
                        ...
                    }
                ]

            Return False for any issue.
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["node"] = kwargs.pop("node", None)
        options["lsys_name"] = kwargs.pop("lsys_name", None)
        options["more_options"] = kwargs.pop("more_options", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_show_timeout"]))

        cmd_element_list = []
        cmd_element_list.append("show security nat interface-nat-ports")

        if options["lsys_name"]:
            cmd_element_list.append("logical-system {}".format(options["lsys_name"]))

        if options["node"] is not None:
            cmd_element_list.append("node {}".format(self.tool.get_node_value(options["node"], mode="INT")))

        if options["more_options"] is not None:
            cmd_element_list.append(options["more_options"])

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_element_list),
            channel="pyez",
            format="xml",
            timeout=options["timeout"],
        ))
        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return response

        entry_list = self.xml.strip_xml_response(response, return_list=True)

        all_entry_list = []
        for entry in entry_list:
            info = {}
            if "re-name" in entry:
                info["re_name"] = str(entry["re-name"])

            try:
                interface_nat_ports_entry_list = entry["interface-nat-ports-information"]["interface-nat-ports-entry"]
            except (KeyError, TypeError) as err:
                device.log(message="cannot get interface nat ports entry: {}".format(err), level="ERROR")
                return False

            # if only one entry occurred
            if not isinstance(interface_nat_ports_entry_list, (list, tuple)):
                interface_nat_ports_entry_list = [interface_nat_ports_entry_list, ]

            for port_entry in interface_nat_ports_entry_list:
                info.update(self.tool.flat_dict(
                    dict_variable=port_entry,
                    parent_key="",
                    separate_char="_",
                    lowercase=True,
                    replace_dash_to_underline=True,
                ))

                all_entry_list.append(copy.deepcopy(info))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_source_nat_deterministic(self, device, **kwargs):
        """Get SNAT deterministic info from LE/HE SA/HA topology

        Based on cmd: show security nat source deterministic

        Whatever options given, this method will tail given option to base cmd, and get XML response from device.

        From device, XML response have 2 main parts of "determ-blk-table-entry" and "determ-pool-info-entry" to separately contain block and
        pool entries, but there is no any relationship between block entry and pool entry. This means we don't know a block whether belone
        a specific pool. So this method just combine node_name and block related entry to a DICT (but without pool info), and each entry
        DICT append to a LIST.

        Here is a return example:

            [
                {
                    # node related
                    "re_name":              "node0",

                    # block related
                    "blk_high_port":        1151,
                    "blk_internal_ip":      "192.168.150.0",
                    "blk_low_port":         1024,
                    "blk_ports_ol":         1,
                    "blk_ports_total":      128,
                    "blk_reflexive_ip":     "192.168.150.0",
                },
                {
                    "re_name":              "node0",
                    "blk_high_port":        1152,
                    "blk_internal_ip":      "192.168.150.1",
                    "blk_low_port":         1024,
                    "blk_ports_ol":         1,
                    "blk_ports_total":      128,
                    "blk_reflexive_ip":     "192.168.150.0",
                },
                ...
            ]

        Above return value is a LIST, and every element is a DICT that contain all infos.

        :param STR lsys_name:
            *OPTIONAL* lsys name. default: None

        :param STR more_options:
            *OPTIONAL* Add more option string tailed to base cmd to narrow down device output

        :param INT|STR node:
            *OPTIONAL* Node number that only for HA topology

        :param INT timeout:
            *OPTIONAL* Timeout to get info from device

        :return:
            Return a DICT which contain all deterministic table info. Or return False

        :example:
            xml_dict = self.get_source_nat_deterministic(device=r0, node=0, more_options="host-address-range pool A_POOL")
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        # Get and check user option
        options = {}
        options["lsys_name"] = kwargs.pop("lsys_name", None)
        options["more_options"] = kwargs.pop("more_options", None)
        options["node"] = kwargs.pop("node", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_show_timeout"]))

        if options["node"] is not None:
            options["node"] = self.tool.get_node_value(options["node"], mode="INT")

        # Create show cmd and send to device
        cmd_element_list = ["show security nat source deterministic", ]

        if options["lsys_name"]:
            cmd_element_list.append("logical-system {}".format(options["lsys_name"]))

        if options["node"]:
            cmd_element_list.append("node {}".format(options["node"]))

        if options["more_options"]:
            cmd_element_list.append(options["more_options"])

        cmd = " ".join(cmd_element_list)
        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=cmd,
            format="xml",
            channel="pyez",
            timeout=options["timeout"],
        ))
        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return response

        response = self.xml.strip_xml_response(response, return_list=True)
        return_value = []
        for ele in response:
            info = {}
            if "determ-blk-table" not in ele or "determ-blk-table-entry" not in ele["determ-blk-table"]:
                continue    # pragma: no cover

            if "re-name" in ele:
                info["re_name"] = str(ele["re-name"])

            entry_list = ele["determ-blk-table"]["determ-blk-table-entry"]
            # if only one entry occurred
            if not isinstance(entry_list, (list, tuple)):
                entry_list = [entry_list, ]

            for entry in entry_list:
                info.update(self.tool.flat_dict(
                    dict_variable=entry,
                    parent_key="",
                    separate_char="_",
                    lowercase=True,
                    replace_dash_to_underline=True,
                ))

                return_value.append(copy.deepcopy(info))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(return_value)))
        return return_value

    def fetch_source_nat_pool(self, device, **kwargs):
        """Based on command "show security nat source pool"

        :param STR pool_name:
            *OPTIONAL* pool name. default: all

        :param STR lsys_name:
            *OPTIONAL* lsys name. default: None

        :param STR|INT node:
            *OPTIONAL* node name or number for HA topology. default: None

        :param INT timeout:
            *OPTIONAL* Get pool info timeout. Default: 300

        :return:
            Return a list which contain all pool's info (1 pool will in list too). For example:

                LIST = [
                    {
                        "re_name":          "node0",                << HA only
                        "pool_name":        "A_POOL",
                        "pool_id":          "4",
                        "routing_instance_name":        "default",
                        "source_pool_port_translation": "[1024, 63487]",
                        "address_range_low":            "192.168.150.5",
                        "address_range_high":           "192.168.150.10",
                        ...
                    },
                    {
                        "re_name":          "node0",
                        "pool_name":        "B_POOL",
                        "pool_id":          "5",
                        "routing_instance_name":        "default",
                        "source_pool_port_translation": "[1024, 63487]",
                        "address_range_low":            "192.168.160.5",
                        "address_range_high":           "192.168.160.10",
                        ...
                    },
                ]

            If pool value have 1+ level like ["source-pool-address-range"]["address-range-low"], keyword will covered to flat as below:

            source_pool_address_range_address_range_low

            This means all keyword will combined wich separate_char "_" and all characters do lowercase and replace "-" to "_"
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["pool_name"] = kwargs.pop("pool_name", "all")
        options["lsys_name"] = kwargs.pop("lsys_name", None)
        options["node"] = kwargs.pop("node", None)
        options["more_options"] = kwargs.pop("more_options", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))

        if options["node"] is not None:
            options["node"] = self.tool.get_node_value(options["node"], mode="INT")

        cmd_element_list = []
        cmd_element_list.append("show security nat source pool {}".format(options["pool_name"]))

        if options["lsys_name"]:
            cmd_element_list.append("logical-system {}".format(options["lsys_name"]))

        if options["node"]:
            cmd_element_list.append("node {}".format(options["node"]))

        if options["more_options"]:
            cmd_element_list.append(options["more_options"])

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_element_list),
            format="xml",
            channel="pyez",
            timeout=options["timeout"],
        ))

        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return response

        response = self.xml.strip_xml_response(response, return_list=True)
        compat_element_list = (
            # compatible_keyword, session_keyword
            ("address_range_low", "source_pool_address_range_address_range_low"),
            ("address_range_high", "source_pool_address_range_address_range_high"),
            ("single_port", "source_pool_address_range_single_port"),
            ("twin_port", "source_pool_address_range_twin_port"),
            ("single_port_sum", "source_pool_address_range_sum_single_port_sum"),
            ("twin_port_sum", "source_pool_address_range_sum_twin_port_sum"),
            ("overflow_pool", "source_pool_overflow_pool"),
        )

        all_entry_list = []
        for ele in response:
            info = {}
            if "re-name" in ele:
                info["re_name"] = str(ele["re-name"])

            if "source-nat-pool-detail-information" not in ele or "source-nat-pool-info-entry" not in ele["source-nat-pool-detail-information"]:
                continue

            snat_entry_list = ele["source-nat-pool-detail-information"]["source-nat-pool-info-entry"]
            if not isinstance(snat_entry_list, (list, tuple)):
                snat_entry_list = [snat_entry_list, ]

            for entry in snat_entry_list:
                info.update(self.tool.flat_dict(
                    dict_variable=entry,
                    parent_key="",
                    separate_char="_",
                    lowercase=True,
                    replace_dash_to_underline=True
                ))

                # for previous compatible
                for compat_keyword, current_keyword in compat_element_list:
                    info[compat_keyword] = info[current_keyword] if current_keyword in info else None

                all_entry_list.append(copy.deepcopy(info))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_source_nat_rule(self, device, **kwargs):
        """Get SNAT rule informaton

        Based on command "show security nat source rule all" to get all informations

        :param STR rule_name:
            *OPTIONAL* Rule name to get just one rule's information. Default: 'all'

        :param STR|INT node:
            *OPTIONAL* node name of 0, 1, "node0" or node1. default: None

        :param STR lsys_name:
            *OPTIONAL* lsys name. default: None

        :param STR more_options:
            *OPTIONAL* more options. default: None

        :params INT timeout:
            *OPTIONAL* Get information timeout.

        :return: Return a dict with all information

        :example:
            snat_rule_info_dict = self.get_source_nat_rule(rule_namt="all", timeout=60)
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["rule_name"] = kwargs.pop("rule_name", "all")
        options["node"] = kwargs.pop("node", None)
        options["lsys_name"] = kwargs.pop("lsys_name", None)
        options["more_options"] = kwargs.pop("more_options", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))

        cmd_element_list = []
        cmd_element_list.append("show security nat source rule {}".format(options["rule_name"]))

        if options["node"] is not None:
            cmd_element_list.append("node {}".format(self.tool.get_node_value(options["node"], mode="INT")))

        if options["lsys_name"]:
            cmd_element_list.append("logical-system {}".format(options["lsys_name"]))

        if options["more_options"]:
            cmd_element_list.append(options["more_options"])

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_element_list),
            format="xml",
            channel="pyez",
            timeout=options["timeout"],
        ))
        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return False

        response = self.xml.strip_xml_response(response, return_list=True)
        compat_element_list = (
            # compatible_keyword, session_keyword
            ("rule_source_address_low_range", "source_address_range_entry_rule_source_address_low_range"),
            ("rule_source_address_high_range", "source_address_range_entry_rule_source_address_high_range"),
            ("rule_destination_address_low_range", "destination_address_range_entry_rule_destination_address_low_range"),
            ("rule_destination_address_high_range", "destination_address_range_entry_rule_destination_address_high_range"),
            ("src_nat_application", "src_nat_app_entry_src_nat_application"),
            ("source_nat_rule_action", "source_nat_rule_action_entry_source_nat_rule_action"),
            ("persistent_nat_type", "source_nat_rule_action_entry_persistent_nat_type"),
            ("persistent_nat_mapping_type", "source_nat_rule_action_entry_persistent_nat_mapping_type"),
            ("persistent_nat_timeout", "source_nat_rule_action_entry_persistent_nat_timeout"),
            ("persistent_nat_max_session", "source_nat_rule_action_entry_persistent_nat_max_session"),
            ("rule_translation_hits", "source_nat_rule_hits_entry_rule_translation_hits"),
            ("succ_hits", "source_nat_rule_hits_entry_succ_hits"),
            ("failed_hits", "source_nat_rule_hits_entry_failed_hits"),
            ("concurrent_hits", "source_nat_rule_hits_entry_concurrent_hits"),
        )

        all_entry_list = []
        for ele in response:
            info = {}
            if "re-name" in ele:
                info["re_name"] = str(ele["re-name"])

            if "source-nat-rule-detail-information" not in ele or "source-nat-rule-entry" not in ele["source-nat-rule-detail-information"]:
                continue    # pragma: no cover

            entry_list = ele["source-nat-rule-detail-information"]["source-nat-rule-entry"]
            if not isinstance(entry_list, (list, tuple)):
                entry_list = [entry_list, ]

            for entry in entry_list:
                info.update(self.tool.flat_dict(
                    dict_variable=entry,
                    parent_key="",
                    separate_char="_",
                    lowercase=True,
                    replace_dash_to_underline=True
                ))

                for compat_keyword, current_keyword in compat_element_list:
                    info[compat_keyword] = info[current_keyword] if current_keyword in info else None

                all_entry_list.append(copy.deepcopy(info))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_source_nat_port_block(self, device, **kwargs):
        """Get SNAT port block info

        Based on command "show security nat source port-block" to get all infomation

        :param STR more_options:
            *OPTIONAL* A string will tailed to basic cmd. For example: "pool A_POOL xlated-ip 192.168.150.0". default: None

        :param STR lsys_name:
            *OPTIONAL* lsys name. default: None

        :param STR|INT node:
            *OPTIONAL* For HA topology. default: None

        :param int timeout:
            *OPTIONAL* Get information timeout

        :return:
            Return a LIST which contain all blocks. For example:

            [   {   'blk_high_port': '1279',
                'blk_internal_ip': '121.11.10.2',
                'blk_left_time': '-',
                'blk_low_port': '1216',
                'blk_ports_ol': '1',
                'blk_ports_total': '64',
                'blk_ports_used': '0',
                'blk_reflexive_ip': '121.11.15.11',
                'blk_status': 'Query',
                'pba_blk_total': '40',
                'pba_blk_used': '3',
                'pba_last_blk_timeout': '0',
                'pba_olfactor': '1',
                'pba_per_host': '2',
                'pba_pool_name': 'A_POOL',
                'pba_size': '64',
                'pba_timeout': '0',
                're_name': 'node0'},
            {   'blk_high_port': '1279',
                'blk_internal_ip': '121.11.10.3',
                'blk_left_time': '-',
                'blk_low_port': '1216',
                'blk_ports_ol': '1',
                'blk_ports_total': '64',
                'blk_ports_used': '0',
                'blk_reflexive_ip': '121.11.15.12',
                'blk_status': 'Query',
                'pba_blk_total': '40',
                'pba_blk_used': '3',
                'pba_last_blk_timeout': '0',
                'pba_olfactor': '1',
                'pba_per_host': '2',
                'pba_pool_name': 'A_POOL',
                'pba_size': '64',
                'pba_timeout': '0',
                're_name': 'node0'},
            {   'pba_blk_total': '40',
                'pba_blk_used': '0',
                'pba_last_blk_timeout': '0',
                'pba_olfactor': '1',
                'pba_per_host': '2',
                'pba_pool_name': 'B_POOL',
                'pba_size': '64',
                'pba_timeout': '0',
                're_name': 'node1'}]

            Every element is port block entry with pool and node info. If a pool no any port block entry, just contain pool info.

            Any issue will return False

        :example:
            port_block_list = self.get_source_nat_port_block(timeout=60, more_options="pool A_POOL", node="node0")
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["more_options"] = kwargs.pop("more_options", None)
        options["node"] = kwargs.pop("node", None)
        options["lsys_name"] = kwargs.pop("lsys_name", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))

        cmd_element_list = []
        cmd_element_list.append("show security nat source port-block")

        if options["more_options"]:
            cmd_element_list.append(options["more_options"])

        if options["node"] is not None:
            cmd_element_list.append("node {}".format(self.tool.get_node_value(options["node"], mode="INT")))

        if options["lsys_name"]:
            cmd_element_list.append("logical-system {}".format(options["lsys_name"]))

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_element_list),
            format="xml",
            channel="pyez",
            timeout=options["timeout"],
        ))
        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return False

        response = self.xml.strip_xml_response(response, return_list=True)
        all_entry_list = []
        # node loop
        for node_entry in response:
            info = {}
            if "re-name" in node_entry:
                info["re_name"] = str(node_entry["re-name"])

            if "pba-blk-table" not in node_entry or "pba-pool-info-entry" not in node_entry["pba-blk-table"]:
                continue    # pragma: no cover

            # pool loop
            pool_entry_list = node_entry["pba-blk-table"]["pba-pool-info-entry"]
            if not isinstance(pool_entry_list, (list, tuple)):
                pool_entry_list = (pool_entry_list, )

            # pool loop
            for pool_entry in pool_entry_list:
                if "pba-blk-table-entry" in pool_entry:
                    block_entry_list = pool_entry.pop("pba-blk-table-entry")
                    if not isinstance(block_entry_list, (list, tuple)):
                        block_entry_list = (block_entry_list, )
                else:
                    block_entry_list = []

                info.update(self.tool.flat_dict(
                    dict_variable=pool_entry,
                    parent_key="",
                    separate_char="_",
                    lowercase=True,
                    replace_dash_to_underline=True
                ))

                # if no block entry in pool, just add pool info
                if not block_entry_list:
                    all_entry_list.append(copy.deepcopy(info))
                    continue

                # port block loop
                for block_entry in block_entry_list:
                    info.update(self.tool.flat_dict(
                        dict_variable=block_entry,
                        parent_key="",
                        separate_char="_",
                        lowercase=True,
                        replace_dash_to_underline=True
                    ))

                    all_entry_list.append(copy.deepcopy(info))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_source_nat_resource_usage(self, device, source_pool="all", **kwargs):
        """Get SNAT resource-usage info

        Based on command "show security nat resource-usage source-pool <pool_name>" to get all infomation

        :param STR more_options:
            *OPTIONAL* A string will tailed to basic cmd. For example: "logical-system lsys1". default: None

        :param STR|INT node:
            *OPTIONAL* For HA topology. default: None

        :param STR lsys_name:
            *OPTIONAL* lsys name. default: None

        :param int timeout:
            *OPTIONAL* Get information timeout

        :return:
            Return a LIST which contain all resource usage infos. For example:

            Every element contain one resource usage entry. Node info also combined.

            Any issue will return False

        :example:
            resource_usage_list = self.get_source_nat_resource_usage(timeout=60, source_pool="B_POOL", node="node0")
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["more_options"] = kwargs.pop("more_options", None)
        options["node"] = kwargs.pop("node", None)
        options["lsys_name"] = kwargs.pop("lsys_name", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))

        cmd_element_list = []
        cmd_element_list.append("show security nat resource-usage source-pool {}".format(source_pool))

        if options["more_options"]:
            cmd_element_list.append(options["more_options"])

        if options["node"] is not None:
            cmd_element_list.append("node {}".format(self.tool.get_node_value(options["node"], mode="INT")))

        if options["lsys_name"]:
            cmd_element_list.append("logical-system {}".format(options["lsys_name"]))

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_element_list),
            format="xml",
            channel="pyez",
            timeout=options["timeout"],
        ))
        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return False

        response = self.xml.strip_xml_response(response, return_list=True)
        all_entry_list = []
        # node loop
        for node_entry in response:
            info = {}
            if "re-name" in node_entry:
                info["re_name"] = str(node_entry["re-name"])

            if ("source-resource-usage-pool-information" not in node_entry or
                    "resource-usage-entry" not in node_entry["source-resource-usage-pool-information"]):
                continue    # pragma: no cover

            resource_usage_pool_entry_list = node_entry["source-resource-usage-pool-information"]["resource-usage-entry"]
            if not isinstance(resource_usage_pool_entry_list, (list, tuple)):
                resource_usage_pool_entry_list = (resource_usage_pool_entry_list, )

            # pool loop
            for resource_entry in resource_usage_pool_entry_list:
                info.update(self.tool.flat_dict(
                    dict_variable=resource_entry,
                    parent_key="",
                    separate_char="_",
                    lowercase=True,
                    replace_dash_to_underline=True
                ))

                all_entry_list.append(copy.deepcopy(info))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_pool_id_owner_spu(self, device, pool_id, **kwargs):
        """Find which SPU owned specific pool

        According to pool_id to find pool's own SPU address.

        :param STR|INT pool_id:
            **REQUIRED** pool id number.

        :param INT timeout:
            *OPTIONAL* get result timeout. default: 300

        :param STR|INT node:
            *OPTIONAL* node number or name. default: None

        :return:
            SPU address string like "fpc0.pic2". From SA topology, you can use the address directly, but must add node related string for HA

            return False for any issue
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["pool_id"] = str(int(pool_id))
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_show_timeout"]))
        options["node"] = kwargs.pop("node", None)

        if options["node"] is not None:
            options["node"] = self.tool.get_node_value(node_value=options["node"], mode="STR")

        cmd_element_list = []
        cmd_element_list.append("show usp spu load-balance spuid pool {}".format(pool_id))

        spu_pool_id = 0
        response = dev.execute_vty_command_on_device(device=device, destination="CP", command=" ".join(cmd_element_list), node=options["node"])
        for line in response.splitlines():
            match = re.match(r"SPUID: (\d+)", line.strip(), re.I)
            if not match:
                continue

            spu_pool_id = str(int(match.group(1)))

        device.log(message="SPU id is {}".format(spu_pool_id), level="DEBUG")

        response = dev.execute_vty_command_on_device(device=device, destination="CP", command="show usp spu chassis", node=options["node"])
        mapping_spu = {}

        for line in response.splitlines():
            match = re.match(r"(\d+)\s+(\d+)\s+(\d+)\s+.*(CP|SPU)", line.strip(), re.I)
            if not match:
                continue

            spu_id = str(int(match.group(1)))
            fpc_num = str(int(match.group(2)))
            pic_num = str(int(match.group(3)))
            mapping_spu[spu_id] = "fpc{}.pic{}".format(fpc_num, pic_num)

        device.log(message="mapping_spu: {}".format(mapping_spu), level="DEBUG")
        if spu_pool_id in mapping_spu:
            device.log(message="{} return value: {}".format(func_name, mapping_spu[spu_pool_id]), level="INFO")
            return mapping_spu[spu_pool_id]

        device.log(message="{} cannot find pool id '{}' related SPU address. Return: False".format(func_name, spu_pool_id), level="INFO")
        return False

    def fetch_pst_nat_table_summary(self, device, **kwargs):
        """Check SNAT persistent nat table summary

        Based on command "show security nat source persistent-nat-table summary" to get info

        :param STR root:
            *OPTIONAL* root system

        :param STR lsys:
            *OPTIONAL* logical-system name

        :param INT node:
            *OPTIONAL* node id, should be 0 or 1.

        :param STR more_options:
            *OPTIONAL* Add more option string tailed to base cmd to narrow down device output

        :param STR return_mode:
            *OPTIONAL* As default, Return a dict {'binding in use': a, 'enode in use': b} with summary numbers for all
                       SPU(M)s. If set to "FLAT_DICT", will return xml flat dict

        :return:
            return_mode="normal"

            {'binding in use': a, 'enode in use': b}

            return_mode="flat_dict"

            [
                {
                    "persist_nat_table_statistic_persist_nat_binding_in_use": "100",
                    "persist_nat_table_statistic_persist_nat_binding_total": "524288",
                    "persist_nat_table_statistic_persist_nat_enode_in_use": "300",
                    "persist_nat_table_statistic_persist_nat_enode_total": "4194304",
                    "persist_nat_table_statistic_persist_nat_spu_id": "on FPC0 PIC1:"
                },
                {
                    "persist_nat_table_statistic_persist_nat_binding_in_use": "200",
                    "persist_nat_table_statistic_persist_nat_binding_total": "524288",
                    "persist_nat_table_statistic_persist_nat_enode_in_use": "200",
                    "persist_nat_table_statistic_persist_nat_enode_total": "4194304",
                    "persist_nat_table_statistic_persist_nat_spu_id": "on FPC0 PIC2:"
                },
                {
                    "persist_nat_table_statistic_persist_nat_binding_in_use": "100",
                    "persist_nat_table_statistic_persist_nat_binding_total": "524288",
                    "persist_nat_table_statistic_persist_nat_enode_in_use": "100",
                    "persist_nat_table_statistic_persist_nat_enode_total": "4194304",
                    "persist_nat_table_statistic_persist_nat_spu_id": "on FPC0 PIC3:"
                }
            ]
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["root"] = kwargs.pop("root", None)
        options["lsys"] = kwargs.pop("lsys", None)
        options["node"] = kwargs.pop("node", None)
        options["more_options"] = kwargs.pop("more_options", None)
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))

        if options["node"] is not None:
            options["node"] = self.tool.get_node_value(options["node"], mode="INT")


        cmd = ["show security nat source persistent-nat-table summary", ]
        if options['lsys'] is not None:
            cmd.append("logical-system {}".format(options['lsys']))

        if options['root']:
            cmd.append("root-logical-system")

        if options['node'] is not None:
            cmd.append("node {}".format(options['node']))

        if options["more_options"]:
            cmd.append(options["more_options"])

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd),
            format="xml",
            channel="text",
            timeout=options["timeout"],
        ))
        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return False

        response = self.xml.strip_xml_response(response, return_list=True)
        all_entry_list = []
        for node_entry in response:
            info = {}
            if "re-name" in node_entry:
                info["re_name"] = str(node_entry["re-name"])

            if "persist-nat-table" not in node_entry:
                continue    # pragma: no cover

            session_list = node_entry["persist-nat-table"]
            if not isinstance(session_list, (list, tuple)):
                session_list = (session_list, )

            # pool loop
            for session in session_list:
                info.update(self.tool.flat_dict(
                    dict_variable=session,
                    parent_key="",
                    separate_char="_",
                    lowercase=True,
                    replace_dash_to_underline=True
                ))

                all_entry_list.append(copy.deepcopy(info))

        return_value = all_entry_list
        if options["return_mode"] != "FLAT_DICT":
            binding_in_use = 0
            enode_in_use = 0
            for entry in all_entry_list:
                if "persist_nat_table_statistic_persist_nat_binding_in_use" in entry:
                    binding_in_use += int(entry["persist_nat_table_statistic_persist_nat_binding_in_use"])

                if "persist_nat_table_statistic_persist_nat_enode_in_use" in entry:
                    enode_in_use += int(entry["persist_nat_table_statistic_persist_nat_enode_in_use"])

            return_value = {'binding in use': binding_in_use, 'enode in use': enode_in_use}

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(return_value)), level="INFO")
        return return_value


    def fetch_pst_nat_table_entry(self, device, in_ip, **kwargs):
        """Check SNAT persistent nat table summary

        Based on command "show security nat source persistent-nat-table internal-ip xxx"
        to get persistent-nat table binding entries.

        :param str in_ip:
            *CONSTRAINT* Internal IP, IPv4/6 address string (no netmask) such as '192.168.0.1' or '2000::1'

        :param int in_port:
            *OPTIONAL* Internal Port

        :param int/str in_proto:
            *OPTIONAL*
                <protocol-number>|icmp|icmp6|tcp|udp

        :param str root:
            *OPTIONAL* root system

        :param str lsys:
            *OPTIONAL* logical-system name

        :param int node:
            *OPTIONAL* node id, should be 0 or 1.

        :param STR more_options:
            *OPTIONAL* Add more option string tailed to base cmd to narrow down device output

        :return:
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))
        options["more_options"] = kwargs.pop("more_options", None)
        options["in_port"] = kwargs.pop("in_port", None)
        options["in_proto"] = kwargs.pop("in_proto", None)
        options["lsys"] = kwargs.pop("lsys", None)
        options["root"] = kwargs.pop("root", None)
        options["node"] = kwargs.pop("node", None)

        if options["node"] is not None:
            options["node"] = self.tool.get_node_value(options["node"], mode="INT")

        cmd = []
        cmd.append("show security nat source persistent-nat-table internal-ip {}".format(in_ip))

        if options['in_port'] is not None:
            cmd.append("internal-port {}".format(options['in_port']))

        if options['in_proto'] is not None:
            cmd.append("internal-protocol {}".format(options['in_proto']))

        if options['lsys'] is not None:
            cmd.append("logical-system {}".format(options['lsys']))

        if options['root']:
            cmd.append("root-logical-system")

        if options['node'] is not None:
            cmd.append("node {}".format(options['node']))

        if options["more_options"]:
            cmd.append(options["more_options"])

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd),
            format="xml",
            channel="text",
            timeout=options["timeout"],
        ))
        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return False

        response = self.xml.strip_xml_response(response, return_list=True)
        compat_element_list = (
            ("in_ip", "persist_nat_internal_ip"),
            ("in_port", "persist_nat_internal_port"),
            ("in_proto", "persist_nat_internal_proto"),
            ("ref_ip", "persist_nat_reflexive_ip"),
            ("ref_port", "persist_nat_reflexive_port"),
            ("ref_proto", "persist_nat_reflexive_proto"),
            ("nat_pool", "persist_nat_pool_name"),
            ("pst_type", "persist_nat_type"),
            ("life_time", "persist_nat_left_time"),
            ("cfg_time", "persist_nat_config_time"),
            ("curr_sess", "persist_nat_current_session_num"),
            ("max_sess", "persist_nat_max_session_num"),
            ("nat_rule", "persist_nat_rule_name"),
        )

        all_entry_list = []
        for node_entry in response:
            info = {}
            if "re-name" in node_entry:
                info["re_name"] = str(node_entry["re-name"])

            persist_nat_table_list = []
            if "persist-nat-table" in node_entry:
                persist_nat_table_list = node_entry["persist-nat-table"]

            if not isinstance(persist_nat_table_list, (list, tuple)):
                persist_nat_table_list = [persist_nat_table_list, ]

            for persist_nat_table in persist_nat_table_list:
                if "persist-nat-spu-id" in persist_nat_table:
                    info["spu_id"] = str(persist_nat_table["persist-nat-spu-id"])
                    info["persist_nat_spu_id"] = info["spu_id"]

                persist_nat_table_entry_list = []
                if "persist-nat-table-entry" in persist_nat_table:
                    persist_nat_table_entry_list = persist_nat_table["persist-nat-table-entry"]

                if not isinstance(persist_nat_table_entry_list, (list, tuple)):
                    persist_nat_table_entry_list = [persist_nat_table_entry_list, ]

                for session in persist_nat_table_entry_list:
                    info.update(self.tool.flat_dict(
                        dict_variable=session,
                        parent_key="",
                        separate_char="_",
                        lowercase=True,
                        replace_dash_to_underline=True
                    ))

                    for compat_keyword, current_keyword in compat_element_list:
                        if current_keyword in info:
                            info[compat_keyword] = info[current_keyword]

                    all_entry_list.append(copy.deepcopy(info))

        return_value = []
        for entry in all_entry_list:
            for keyword in entry:
                if entry[keyword].strip() == "-":
                    entry[keyword] = None

            return_value.append(copy.deepcopy(entry))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(return_value)))
        return return_value


    def verify_source_nat_interface_nat_ports(self, device, **kwargs):
        """Based on method fetch_source_nat_interface_nat_ports and filter (option) to search specific entry

        Most option in this method is a **filter**, it means a specific entry must match all your given filter.

        Due to all filters are optional, if no any filter given, it means all existing entry matched

        Below keywords all be an INT, and default value is None:

            pool_index, single_ports_allocated, single_ports_available, total_ports, twin_ports_allocated, twin_ports_available, re_name

        :param INT|STR node:
            *OPTIONAL* node name should be "node0" or "node1". default: None

        :param BOOL return_mode:
            *OPTIONAL* set "counter" to return how many existing entries match all filter. or just reurn True/False as default.
                       default: None

        :return:
            Return True/False or return match counter if option return_mode = 'counter'.
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["node"] = kwargs.get("node", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        entry_list = self.fetch_source_nat_interface_nat_ports(device=device, node=options["node"])
        if entry_list is False:
            return False

        matched_entry_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=entry_list,
            index_option="pool_index",
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_entry_list,
            index_option="pool_index",
            debug_to_stdout=self.debug_to_stdout,
        )

        return_value = len(matched_entry_list) if options["return_mode"] == "COUNTER" else bool(matched_entry_list)
        device.log(message="'{}' return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def verify_source_nat_deterministic(self, device, **kwargs):
        """checking SNAT deterministic table entry

        Based on "fetch_source_nat_deterministic" method to get all entries from device, and checking whether match all
        given filters. This method support HE/LE platform and SA/HE topology. Option 'node' will be skipped on SA topo.

        "fetch_source_nat_deterministic" only return a LIST **ONLY** contain block entry (read method doc for detail).
        If you want filter block entries for specific pool, just give pool related keyword to more_options. For example:

            +   Normal search:  verify_source_nat_deterministic(device=r0, blk_high_port=1000)
            +   Specific pool:  verify_source_nat_deterministic(device=r0, more_options="pool A_POOL", blk_high_port=1000)

        :params INT all_entries_counter:
            *OPTIONAL* checking all deterministic table entries counter.

        :params STR node:
            *OPTIONAL* node name of 0, 1, node0 or node1

        :params STR more_options:
            *OPTIONAL* more options tailed to "show security nat source deterministic" command. default: None

        :params INT|STR timeout:
            *OPTIONAL* timeout to get device response

        :params STR return_mode:
            *OPTIONAL* as default this method just return True/False to indicate whether match all filters, but set
                       "counter" to get how many entries matched all filters.

        :return:
            According to return_mode.

        :example:
            please see method "verify_source_nat_pool" to see detail

            result = self.verify_source_nat_deterministic(
                device=r0,
                return_mode="counter",
                blk_high_port="1151 eq",
                blk_low_port="1000 gt",
                blk_internal_ip="192.168.150.1",
                blk_port_ol=(1, "eq"),
                blk_port_used=1,
            )
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["more_options"] = kwargs.pop("more_options", None)
        options["node"] = kwargs.get("node", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        # start checking
        entry_list = self.fetch_source_nat_deterministic(device=device, node=options["node"], more_options=options["more_options"])
        if entry_list is False:
            device.log(message="{} return value: False".format(func_name), level="INFO")
            return False

        matched_entry_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=entry_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_entry_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        return_value = len(matched_entry_list) if options["return_mode"] == "COUNTER" else bool(matched_entry_list)
        device.log(message="'{}' return value: {}".format(func_name, return_value), level="INFO")
        return return_value


    def verify_source_nat_pool(self, device, **kwargs):
        """According to given options to find specific pool

        Ever user option should have 2 elements, for example: address_pool_hits=(256, "eq") means this pool hits 256 times.
        Below types used for element checkint:

            1. Number

                Must be INT, INT_RANGE, FLOAT or STR with compare action (optional), for example:

                    address_pool_hits=(100, "eq")           # LIST contain number and compare action

                    single_port_sum=("100-200", "in")       # LIST contain number range and compare action

                    block_size="100 eq"                     # STR contain number and compare action

            2. STR

                STR used by protocol or policy id, for example:

                    # address assign mode contain 'pair' keyword, it means 'pair' or 'no-pair' all matched.
                    source_pool_address_assignment=("paired", "contain")

                    # address assign mode exactly equal 'no-pair'. Default
                    source-pool-address-assignment=("no-paired", "exact")

            3. IP

                IP address should be IP, Network and IP range:

                    address_range_high = "192.168.150.10 eq"

                    address_range_high = "192.168.150.10-192.168.150.20 in"

                    address_range_high = "192.168.150.0/24"

        Below are all supported options and compare mode. As default, they are all None means no need to search

        +   IP address, IP range or Network

            -   address_range_high or source_pool_address_range_address_range_high
            -   address_range_low or source_pool_address_range_address_range_low
            -   host_address_base

        +   Number or Number range

            -   address_pool_hits
            -   pool_id
            -   port_overloading_factor
            -   single_port or source_pool_address_range_single_port
            -   single_port_sum or source_pool_address_range_sum_single_port_sum
            -   source_pool_blk_size
            -   source_pool_blk_atv_timeout
            -   source_pool_last_blk_rccl_timeout
            -   source_pool_blk_interim_log_cycle
            -   source_pool_blk_used
            -   source_pool_blk_total
            -   source_pool_max_per_host
            -   source_pool_determ_host_range_num
            -   total_pool_address
            -   twin_port or source_pool_address_range_twin_port
            -   twin_port_sum or source_pool_address_range_sum_twin_port_sum
            -   psid_offset
            -   psid_length

        +   String

            -   pool_name
            -   re_name
            -   routing_instance_name
            -   source_pool_address_assignment
            -   source_pool_port_translation
            -   source_pool_twin_port
            -   source_pool_blk_log
            -   overflow_pool or source_pool_overflow_pool
            -   mape_domain
            -   mape_rule
            -   psid
            -   clear_alarm_threshold
            -   raise_alarm_threshold

        :param bool return_mode:
            *OPTIONAL* As default this method just return True/False means whether match a pool, but you can set 'counter' to return how
                       many pool matched

        :return:
            Return True if have a pool to match all filters, or return False if not found. If return_mode is 'counter' that will return
            match counter.

        :Example Python:
            status = search_source_nat_pool(
                device=device,
                port_overloading_factor="1-10, in",
                total_pool_address="256 eq",
                address_range_high=("192.168.1.255", "eq"),
                address_range_low=("192.168.1.0/24", "in"),
                address_assignment=("no-paired", "contain"),
                translation_hits="0 ge",
            )

        :Example robot:
            ${status}   search_source_nat_pool
            ...             device=device
            ...             port_overloading=1
            ...             total_pool_address=256
            ...             address_range_high=192.168.1.255
            ...             address_range_low=192.168.1.0
            ...             address_assignment=no-paired contain
            ...             translation_hits=0 ge

        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["pool_name"] = kwargs.pop("pool_name", "all")
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["node"] = kwargs.get("node", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        entry_list = self.fetch_source_nat_pool(device=device, pool_name=options["pool_name"], node=options["node"])
        if entry_list is False:
            device.log(message="No entry found from device", level="INFO")
            return False

        matched_entry_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=entry_list,
            index_option="pool_id",
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_entry_list,
            index_option="pool_id",
            debug_to_stdout=self.debug_to_stdout,
        )

        return_value = len(matched_entry_list) if options["return_mode"] == "COUNTER" else bool(matched_entry_list)
        device.log(message="{} return value: {}".format(func_name, return_value))
        return return_value

    def verify_source_nat_rule(self, device, **kwargs):
        """According to given options to find specific pool

        Below are all supported options and compare mode. As default, they are all None means no need to search

        +   IP address, IP range or Network

            -   rule_destination_address_high_range or destination_address_range_entry_rule_destination_address_high_range
            -   rule_destination_address_low_range or destination_address_range_entry_rule_destination_address_low_range
            -   rule_source_address_high_range or source_address_range_entry_rule_source_address_high_range
            -   rule_source_address_low_range or source_address_range_entry_rule_source_address_low_range

        +   Number or Number range

            -   concurrent_hits or source_nat_rule_hits_entry_concurrent_hits
            -   failed_hits or source_nat_rule_hits_entry_failed_hits
            -   persistent_nat_max_session or source_nat_rule_action_entry_persistent_nat_max_session
            -   persistent_nat_timeout or source_nat_rule_action_entry_persistent_nat_timeout
            -   rule_id
            -   rule_matching_position
            -   rule_translation_hits or source_nat_rule_hits_entry_rule_translation_hits
            -   succ_hits or source_nat_rule_hits_entry_succ_hits

        +   String

            -   destination_port_entry
            -   persistent_nat_mapping_type or source_nat_rule_action_entry_persistent_nat_mapping_type
            -   persistent_nat_type or source_nat_rule_action_entry_persistent_nat_type
            -   re_name
            -   rule_from_context
            -   rule_from_context_name
            -   rule_name
            -   rule_set_name
            -   rule_to_context
            -   rule_to_context_name
            -   source_nat_rule_action or source_nat_rule_action_entry_source_nat_rule_action
            -   source_port_entry
            -   src_nat_application or src_nat_app_entry_src_nat_application
            -   src_nat_protocol_entry

        :param STR rule_name:
            *OPTIONAL* rule name. default: all

        :param STR return_mode:
            *OPTIONAL* As default this method just return True/False means whether match a rule, but you can set 'counter' to return how
                       many rule matched

        :return:
            Return True if a rule match all filters, or return False if not found. If return_mode is 'counter' that will return
            match counter.
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["rule_name"] = kwargs.pop("rule_name", "all")
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["node"] = kwargs.get("node", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        entry_list = self.fetch_source_nat_rule(device=device, rule_name=options["rule_name"], node=options["node"])
        if entry_list is False:
            device.log(message="No entry found from device", level="INFO")
            return False

        matched_entry_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=entry_list,
            index_option="rule_id",
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_entry_list,
            index_option="rule_id",
            debug_to_stdout=self.debug_to_stdout,
        )

        return_value = len(matched_entry_list) if options["return_mode"] == "COUNTER" else bool(matched_entry_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def verify_source_nat_port_block(self, device, **kwargs):
        """checking SNAT port block entry

        Based on "fetch_source_nat_port_block" method to get all entries from device, and checking whether match all given filters.
        This method support HE/LE platform and SA/HE topology. Option 'node' will be skipped on SA topo.

        Below are all supported options and compare mode. As default, they are all None means no need to search

        +   IP address, IP range or Network

            -   blk_internal_ip
            -   blk_reflexive_ip

        +   Number or Number range

            -   blk_high_port
            -   blk_left_time
            -   blk_low_port
            -   blk_ports_ol
            -   blk_ports_total
            -   blk_ports_used
            -   pba_blk_total
            -   pba_blk_used
            -   pba_last_blk_timeout
            -   pba_olfactor
            -   pba_per_host
            -   pba_size
            -   pba_timeout

        +   String

            -   blk_status
            -   pba_pool_name
            -   re_name


        :params STR node:
            *OPTIONAL* node name of 0, 1, node0 or node1

        :params STR more_options:
            *OPTIONAL* more options tailed to "show security nat source port-block" command. default: None

        :params INT|STR timeout:
            *OPTIONAL* timeout to get device response

        :params STR return_mode:
            *OPTIONAL* as default this method just return True/False to indicate whether match all filters, but you can set "counter" to get
                       how many times all filters matched.

        :return:
            According to return_mode.

        :example:
            please see method "search_source_nat_pool" to see detail

            result = self.search_source_nat_port_block(
                device=r0,
                return_mode="counter",
                blk_high_port="1151 eq",
                blk_low_port="1000 gt",
                blk_internal_ip="192.168.150.1",
                blk_ports_ol=(1, "eq"),
                blk_ports_used=1,
            )
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["more_options"] = kwargs.pop("more_options", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_show_timeout"]))
        options["node"] = kwargs.get("node", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        # start checking
        entry_list = self.fetch_source_nat_port_block(
            device=device,
            node=options["node"],
            more_options=options["more_options"],
            timeout=options["timeout"],
        )
        if entry_list is False:
            device.log(message="No entry found from device", level="INFO")
            return False

        print("entry_list:\n", self.tool.pprint(entry_list))

        matched_entry_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=entry_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_entry_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        return_value = len(matched_entry_list) if options["return_mode"] == "COUNTER" else bool(matched_entry_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def verify_source_nat_resource_usage(self, device, source_pool="all", **kwargs):
        """checking SNAT resource usage entry

        Based on "fetch_source_nat_resource_usage" method to get all entries from device, and checking whether match all
        given filters. This method support HE/LE platform and SA/HE topology. Option 'node' will be skipped on SA topo.

        Below are all supported options and compare mode. As default, they are all None means no need to search

        +   Number or Number range

            -   resource_usage_port_ol_factor
            -   resource_usage_total_address
            -   resource_usage_total_avail
            -   resource_usage_total_pool_num
            -   resource_usage_total_total
            -   resource_usage_total_used

        +   String

            -   re_name
            -   resource_usage_peak_date_time
            -   resource_usage_peak_usage
            -   resource_usage_pool_name
            -   resource_usage_total_usage

        :params STR node:
            *OPTIONAL* node name of 0, 1, node0 or node1

        :params STR more_options:
            *OPTIONAL* more options tailed to "show security nat resource-usage source-pool <pool_name>" command. default: None

        :params INT|STR timeout:
            *OPTIONAL* timeout to get device response

        :params STR return_mode:
            *OPTIONAL* as default this method just return True/False to indicate whether match all filters, but you can set "counter" to get
                       how many times all filters matched.

        :return:
            According to return_mode.

        :example:
            result = self.search_source_nat_resource_usage(
                device=r0,
                return_mode="counter",
                re_name="node0",
                resource_usage_peak_usage="1% eq",
                resource_usage_total_pool_num="1000-2000 in",
                resource_usage_total_used=0,
            )
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["more_options"] = kwargs.pop("more_options", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_show_timeout"]))
        options["node"] = kwargs.get("node", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        entry_list = self.fetch_source_nat_resource_usage(
            device=device,
            source_pool=source_pool,
            node=options["node"],
            more_options=options["more_options"],
            timeout=options["timeout"],
        )
        if entry_list is False:
            device.log(message="No entry found from device", level="INFO")
            return False

        matched_entry_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=entry_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_entry_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        return_value = len(matched_entry_list) if options["return_mode"] == "COUNTER" else bool(matched_entry_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value
