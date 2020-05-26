# coding: UTF-8
# pylint: disable=invalid-name
"""Have all flow module methods

FLOW module keywords that obey MTS (Master Test Script) behavior.

In this module, some options have same behavior of all method:

+   device

    Device handler will send command to it. For HA device, just set main handler such as r0, never given
    r0.node0 or r0.node1.

+   more_options

    Will concatenate given string to base command. For example: base command "show security flow session" used for
    method "fetch_all_flow_session", you can set more_options="source-address x.x.x.x" to reduce session count.

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
                   transit xml response to complex DICT structure. Here is a complex DICT for session:

                   [
                        {
                            "flow-gate-information": {
                                "displayed-gate-count": "0",
                                "displayed-gate-invalidated": "0",
                                "displayed-gate-other": "0",
                                "displayed-gate-pending": "0",
                                "displayed-gate-valid": "0"
                            },
                            "re-name": "node0"
                        },
                        {
                            "flow-gate-information": {
                                "displayed-gate-count": "0",
                                "displayed-gate-invalidated": "0",
                                "displayed-gate-other": "0",
                                "displayed-gate-pending": "0",
                                "displayed-gate-valid": "0"
                            },
                            "re-name": "node1"
                        }
                    ]

                    This is difficult to check complex dict in script. So you can set 'return_mode=flat_dict' let
                    complex dict structure to simple dict with long keyword. The long keyword only have lowercase
                    character and underscore. For example, above complex dict will be transited to:

                    [
                        {
                            "displayed_gate_count": "0",
                            "displayed_gate_invalidated": "0",
                            "displayed_gate_other": "0",
                            "displayed_gate_pending": "0",
                            "displayed_gate_valid": "0",
                            "re_name": "node0"
                        },
                        {
                            "displayed_gate_count": "0",
                            "displayed_gate_invalidated": "0",
                            "displayed_gate_other": "0",
                            "displayed_gate_pending": "0",
                            "displayed_gate_valid": "0",
                            "re_name": "node1"
                        }
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

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import copy
import time

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.exception.toby_exception import TobyException


class flows():
    """All FLOW related methods"""
    def __init__(self):
        """Init processing"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()

        self.debug_to_stdout = False
        self.default = {
            "cli_show_timeout":     300,
            "conf_commit_timeout":  300,
        }

        self.runtime = {}

        # MTS keyword behavior for previous script
        self.set_flow_advance_option = self.configure_flow_advance_option
        self.set_flow_forwarding_option = self.configure_flow_forwarding_option
        self.set_flow_aging = self.configure_flow_aging
        self.set_flow_enhance_configuration = self.configure_flow_enhance_configuration
        self.set_flow_tcp_mss = self.configure_flow_tcp_mss
        self.set_flow_tcp_session = self.configure_flow_tcp_session
        self.set_flow_traceoptions = self.configure_flow_traceoptions
        self.get_all_flow_session = self.fetch_flow_session
        self.get_flow_cp_session = self.fetch_flow_cp_session
        self.get_flow_cp_session_summary = self.fetch_flow_cp_session_summary
        self.get_flow_status = self.fetch_flow_status
        self.get_flow_statistics = self.fetch_flow_statistics
        self.get_flow_gate = self.fetch_flow_gate
        self.get_flow_session_summary = self.fetch_flow_session_summary
        self.get_all_flow_session_on_vty = self.fetch_flow_session_on_vty
        self.get_wing_per_thread = self.fetch_wing_per_thread
        self.search_flow_session = self.verify_flow_session
        self.search_flow_cp_session = self.verify_flow_cp_session
        self.search_flow_cp_session_summary = self.verify_flow_cp_session_summary
        self.check_flow_status = self.verify_flow_status
        self.check_flow_statistics = self.verify_flow_statistics
        self.check_flow_gate = self.verify_flow_gate
        self.check_flow_session_summary = self.verify_flow_session_summary
        self.search_flow_session_on_vty = self.verify_flow_session_on_vty
        self.delete_flow_configuration = self.operation_delete_flow_configuration
        self.clear_flow_session = self.execute_clear_flow_session
        self.clear_flow_ip_action = self.execute_clear_flow_ip_action
        self.clear_flow_statistics = self.execute_clear_flow_statistics
        self.fetch_all_flow_session = self.fetch_flow_session
        self.fetch_all_flow_session_on_vty = self.fetch_flow_session_on_vty

    @staticmethod
    def _summarize_all_fpcs_counter(entry_list, only_update_element_list=list()):
        """Summarize all FPCs entries for total counter

        :param LIST|TUPLE entry_list:
            **REQUIRED** All FPCs entry list

        :param LIST|TUPLE only_update_element_list:
            *OPTIONAL* If element keyword in this list, the value only do update without calculate. default: []

        :return:
            Return a LIST which contain 1 (SA) or 2 (HA for 2 nodes) summarized DICT
        """
        return_value = []
        summarized_counter = {"node0": {}, "node1": {}}
        for entry in entry_list:
            if "re_name" in entry:
                node_name = entry["re_name"].strip().lower()
            else:
                node_name = "node0"

            for keyword in entry:
                if keyword in only_update_element_list or not str(entry[keyword]).isdigit():
                    summarized_counter[node_name][keyword] = entry[keyword]
                    continue

                if keyword not in summarized_counter[node_name]:
                    summarized_counter[node_name][keyword] = 0

                summarized_counter[node_name][keyword] += int(entry[keyword])

        # node0 must be first element in list
        for node_name in ("node0", "node1"):
            # empty node will not return
            if summarized_counter[node_name]:
                # every value convert to string
                for keyword in summarized_counter[node_name]:
                    summarized_counter[node_name][keyword] = str(summarized_counter[node_name][keyword])

                return_value.append(copy.deepcopy(summarized_counter[node_name]))

        return return_value

    def configure_flow_advance_option(self, device, **kwargs):
        """Based on cmd 'set security flow advanced-options' to config

        :param BOOL drop_matching_link_local_address:
            *OPTIONAL* Enable/Disable drop-matching-link-local-address feature. Default: None

        :param BOOL drop_matching_reserved_ip_address:
            *OPTIONAL* Enable/Disable drop-matching-reserved-ip-address feature. Default: None

        :param BOOL commit:
            *OPTIONAL* Default: True

        :param BOOL get_response:
            *OPTIONAL* Default: False

        :return:
            True/False to indicate configure success or failed. Or return commit response according to option get_response

            Option 'return_cmd' used for unit test. Set True to return conf cmds

        :example:
            For robot:

            flows.Configure FLOW Advance Option    device=${r0}    drop_matching_link_local_address=True    drop_matching_reserved_ip_address=False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["drop_matching_link_local_address"] = self.tool.check_boolean(kwargs.pop('drop_matching_link_local_address', None))
        options["drop_matching_reserved_ip_address"] = self.tool.check_boolean(kwargs.pop("drop_matching_reserved_ip_address", None))
        options["commit"] = self.tool.check_boolean(kwargs.pop("commit", True))
        options["get_response"] = self.tool.check_boolean(kwargs.pop("get_response", False))
        options["timeout"] = int(kwargs.pop("timeout", self.default["conf_commit_timeout"]))
        options["return_cmd"] = kwargs.pop("return_cmd", None)

        cmd_list = []
        if options["drop_matching_link_local_address"] is True:
            cmd_list.append("set security flow advanced-options drop-matching-link-local-address")
        elif options["drop_matching_link_local_address"] is False:
            cmd_list.append("delete security flow advanced-options drop-matching-link-local-address")
        else: # pragma: no cover
            pass

        if options["drop_matching_reserved_ip_address"] is True:
            cmd_list.append("set security flow advanced-options drop-matching-reserved-ip-address")
        elif options["drop_matching_reserved_ip_address"] is False:
            cmd_list.append("delete security flow advanced-options drop-matching-reserved-ip-address")
        else: # pragma: no cover
            pass

        response = dev.execute_config_command_on_device(
            device=device,
            command=cmd_list,
            get_response=options["get_response"],
            commit=options["commit"],
        )

        if options["return_cmd"] is True:
            response = cmd_list

        device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
        return response

    def configure_flow_forwarding_option(self, device, **kwargs):
        """Based on "set security forwarding-options family" cmd to configure

        :param STR ipv6_mode:
            *OPTIONAL* IPv6 forwarding mode, should be "drop", "flow-based", "packet-based", etc...
                       cmd: "set security forwarding-options family inet6 mode <value>"

        :param STR iso_mode:
            *OPTIONAL* ISO forwarding mode, should be "packet-based" or others.
                       cmd: "set security forwarding-options family iso mode <value>"

        :param STR mpls_mode:
            *OPTIONAL* MPLS forwarding mode, should be "packet-based" or others.
                       cmd: "set security forwarding-options family mpls mode <value>"

        :param BOOL commit:
            *OPTIONAL* Whether commit configure. Default: True

        :param BOOL get_response:
            *OPTIONAL* Return configure commit response instead of True/False. default: False

        :return:
            True/False to indicate configure success or failed. Or return commit response according to option get_response

        :example:
            For robot:

            flows.Configure FLOW Forwarding Option    device=${r0}    ipv6_mode=flow-based    commit=True
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["ipv6_mode"] = kwargs.pop('ipv6_mode', None)
        options["iso_mode"] = kwargs.pop("iso_mode", None)
        options["mpls_mode"] = kwargs.pop("mpls_mode", None)
        options["commit"] = self.tool.check_boolean(kwargs.pop("commit", True))
        options["get_response"] = self.tool.check_boolean(kwargs.pop("get_response", False))
        options["timeout"] = int(kwargs.pop("timeout", self.default["conf_commit_timeout"]))
        options["return_cmd"] = kwargs.pop("return_cmd", None)

        set_base_cmd = "set security forwarding-options family"

        cmd_list = []
        if options["ipv6_mode"] is not None:
            cmd_list.append("{} inet6 mode {}".format(set_base_cmd, options["ipv6_mode"]))

        if options["iso_mode"] is not None:
            cmd_list.append("{} iso mode {}".format(set_base_cmd, options["iso_mode"]))

        if options["mpls_mode"] is not None:
            cmd_list.append("{} mpls mode {}".format(set_base_cmd, options["mpls_mode"]))

        response = device.execute_config_command_on_device(
            device=device,
            command=cmd_list,
            get_response=options["get_response"],
            commit=options["commit"],
        )

        if options["return_cmd"] is True:
            response = cmd_list

        device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
        return response

    def configure_flow_aging(self, device, **kwargs):
        """Based on cmd 'set security flow aging' to config

        :param INT early_ageout:
            *OPTIONAL* . set flow aging early-ageout. Default: None

        :param INT high_watermark:
            *OPTIONAL*  set flow aging high-watermark. Default: None

        :param INT low_watermark:
            *OPTIONAL*  set flow aging low-watermark. Default: None

        :param BOOL commit:
            *OPTIONAL* default: True

        :param BOOL get_response:
            *OPTIONAL* Return configure commit response instead of True/False. default: False

        :return:
            True/False to indicate configure success or failed. Or return commit response according to option get_response

            Option 'return_cmd' used for unit test. Set True to return conf cmds

        :example:
            For robot:

            flows.Configure FLOW Aging    device=${r0}    early_ageout=60
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["early_ageout"] = kwargs.get('early_ageout', None)
        options["high_watermark"] = kwargs.get("high_watermark", None)
        options["low_watermark"] = kwargs.get("low_watermark", None)
        options["commit"] = self.tool.check_boolean(kwargs.get("commit", True))
        options["get_response"] = self.tool.check_boolean(kwargs.get("get_response", False))
        options["timeout"] = int(kwargs.get("timeout", self.default["conf_commit_timeout"]))
        options["return_cmd"] = kwargs.get("return_cmd", None)

        base_cmd = "set security flow aging"
        cmd_list = []
        if options["early_ageout"] is not None:
            cmd_list.append("{} early-ageout {}".format(base_cmd, options["early_ageout"]))

        if options["high_watermark"] is not None:
            cmd_list.append("{} high-watermark {}".format(base_cmd, options["high_watermark"]))

        if options["low_watermark"] is not None:
            cmd_list.append("{} low-watermark {}".format(base_cmd, options["low_watermark"]))

        response = dev.execute_config_command_on_device(
            device=device,
            command=cmd_list,
            get_response=options["get_response"],
            commit=options["commit"],
        )

        if options["return_cmd"] is True:
            response = cmd_list

        device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
        return response

    def configure_flow_enhance_configuration(self, device, **kwargs):
        """Based on cmd 'set security flow ' to add enhance configuration

        :param BOOL force_ip_reassembly:
            *OPTIONAL* add conf: "set security flow force-ip-reassembly". Default: None

        :param BOOL allow_dns_reply:
            *OPTIONAL* add conf: "set security flow allow-dns-reply". Default: None

        :param BOOL allow_embedded_icmp:
            *OPTIONAL* add conf: "set security flow allow-embedded-icmp". Default: None

        :param BOOL mcast_buffer_enhance:
            *OPTIONAL* add conf: "set security flow mcast-buffer-enhance". Default: None

        :param BOOL sync_icmp_session:
            *OPTIONAL* add conf: "set security flow sync-icmp-session". Default: None

        :param STR pending_sess_queue_length:
            *OPTIONAL* add conf: "set security flow pending-sess-queue-length <value>"
                       should one of "high", "moderate" or "normal". Default: None

        :param STR syn_flood_protection_mode:
            *OPTIONAL* add conf: "set security flow syn-flood-protection-mode <value>"
                       should one of "syn-cookie" or "syn-proxy". Default: None

        :param INT route_change_timeout:
            *OPTIONAL* "set security flow route-change-timeout <value>". Default: None

        :param BOOL commit:
            *OPTIONAL* Default: True

        :param BOOL get_response:
            *OPTIONAL* Return configure commit response instead of True/False. default: False

        :return:
            True/False to indicate configure success or failed. Or return commit response according to option get_response

            Option 'return_cmd' used for unit test. Set True to return conf cmds

        :example:
            For robot:

            flows.Configure FLOW Enhance Configuration    device=${r0}    force_ip_reassembly=False    pending_sess_queue_length=200
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["commit"] = self.tool.check_boolean(kwargs.pop("commit", True))
        options["get_response"] = self.tool.check_boolean(kwargs.pop("get_response", False))
        options["timeout"] = int(kwargs.pop("timeout", self.default["conf_commit_timeout"]))
        options["return_cmd"] = kwargs.pop("return_cmd", None)

        user_keyword_dict = {
            # option_type, cmd_string
            "force_ip_reassembly":          ("BOOL", "force-ip-reassembly"),
            "allow_dns_reply":              ("BOOL", "allow-dns-reply"),
            "allow_embedded_icmp":          ("BOOL", "allow-embedded-icmp"),
            "mcast_buffer_enhance":         ("BOOL", "mcast-buffer-enhance"),
            "sync_icmp_session":            ("BOOL", "sync-icmp-session"),
            "pending_sess_queue_length":    ("STR", "pending-sess-queue-length"),
            "syn_flood_protection_mode":    ("STR", "syn-flood-protection-mode"),
            "route_change_timeout":         ("INT", "route-change-timeout"),
        }

        base_cmd = "set security flow"
        cmd_list = []
        for keyword in user_keyword_dict:
            options[keyword] = kwargs.pop(keyword, None)
            if options[keyword] is None:
                continue

            option_type, cmd_string = user_keyword_dict[keyword]
            if option_type == "BOOL" and self.tool.check_boolean(options[keyword]) is True:
                cmd_list.append("{} {}".format(base_cmd, cmd_string))
            else:
                cmd_list.append("{} {} {}".format(base_cmd, cmd_string, options[keyword]))

        response = dev.execute_config_command_on_device(
            device=device,
            command=cmd_list,
            get_response=options["get_response"],
            commit=options["commit"],
        )

        if options["return_cmd"] is True:
            response = cmd_list

        device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
        return response

    def configure_flow_tcp_mss(self, device, **kwargs):
        """Based on cmd 'set security flow tcp-mss' to config

        :param INT all_tcp_mss:
            *OPTIONAL* . set all tcp mss size. cmd: "set security flow tcp-mss all-tcp mss 64". default: None

        :param INT gre_in_mss:
            *OPTIONAL*  set all tcp mss size. cmd: "set security flow tcp-mss gre-in mss 64". default: None

        :param INT gre_out_mss:
            *OPTIONAL*  set all tcp mss size. cmd: "set security flow tcp-mss gre-out mss 64". default: None

        :param INT ipsec_vpn_mss:
            *OPTIONAL*  set all tcp mss size. cmd: "set security flow tcp-mss ipsec-vpn mss 64". default: None

        :param BOOL commit:
            *OPTIONAL* Default: True

        :param BOOL get_response:
            *OPTIONAL* Default: False

        :return:
            True/False to indicate configure success or failed. Or return commit response according to option get_response

            Option 'return_cmd' used for unit test. Set True to return conf cmds

        :example:
            For robot:

            flows.Configure FLOW TCP Mss    device=${r0}    all_tcp_mss=1024    commit=True
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["all_tcp_mss"] = kwargs.pop('all_tcp_mss', None)
        options["gre_in_mss"] = kwargs.pop("gre_in_mss", None)
        options["gre_out_mss"] = kwargs.pop("gre_out_mss", None)
        options["ipsec_vpn_mss"] = kwargs.pop("ipsec_vpn_mss", None)
        options["commit"] = self.tool.check_boolean(kwargs.pop("commit", True))
        options["get_response"] = self.tool.check_boolean(kwargs.pop("get_response", False))
        options["timeout"] = int(kwargs.pop("timeout", self.default["conf_commit_timeout"]))
        options["return_cmd"] = kwargs.pop("return_cmd", None)

        base_cmd = "set security flow tcp-mss"
        cmd_list = []
        if options["all_tcp_mss"] is not None:
            cmd_list.append("{} all-tcp mss {}".format(base_cmd, options["all_tcp_mss"]))

        if options["gre_in_mss"] is not None:
            cmd_list.append("{} gre-in mss {}".format(base_cmd, options["gre_in_mss"]))

        if options["gre_out_mss"] is not None:
            cmd_list.append("{} gre-out mss {}".format(base_cmd, options["gre_out_mss"]))

        if options["ipsec_vpn_mss"] is not None:
            cmd_list.append("{} ipsec-vpn mss {}".format(base_cmd, options["ipsec_vpn_mss"]))

        response = dev.execute_config_command_on_device(
            device=device,
            command=cmd_list,
            get_response=options["get_response"],
            commit=options["commit"],
        )

        if options["return_cmd"] is True:
            response = cmd_list

        device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
        return response

    def configure_flow_tcp_session(self, device, **kwargs):
        """Based on cmd 'set security flow tcp-session' to config

        :param BOOL fin_invalidate_session:
            *OPTIONAL* . add conf: "set security flow tcp-session fin-invalidate-session"
                         Default: None

        :param BOOL no_sequence_check:
            *OPTIONAL* . add conf: "set security flow tcp-session no-sequence-check"
                         Default: None

        :param BOOL no_syn_check:
            *OPTIONAL* . add conf: "set security flow tcp-session no-syn-check"
                         Default: None

        :param BOOL no_syn_check_in_tunnel:
            *OPTIONAL* . add conf: "set security flow tcp-session no-syn-check-in-tunnel"
                         Default: None

        :param BOOL rst_invalidate_session:
            *OPTIONAL* . add conf: "set security flow tcp-session rst-invalidate-session"
                         Default: None

        :param BOOL rst_sequence_check:
            *OPTIONAL* . add conf: "set security flow tcp-session rst-sequence-check"
                         Default: None

        :param BOOL strict_syn_check:
            *OPTIONAL* . add conf: "set security flow tcp-session strict-syn-check"
                         Default: None

        :param BOOL time_wait_state_apply_to_half_close_state:
            *OPTIONAL* . "set security flow tcp-session time-wait-state apply-to-half-close-state"
                         Default: None

        :param BOOL time_wait_state_session_ageout:
            *OPTIONAL* . "set security flow tcp-session time-wait-state session-ageout"
                         Default: None

        :param STR maximum_window:
            *OPTIONAL*  add conf: "set security flow tcp-session maximum-window <value>".
                        should be "64K" "128K", "256K", "512K", or "1M". Default: None

        :param INT tcp_initial_timeout:
            *OPTIONAL* add conf: "set security flow tcp-session tcp-initial-timeout <value>"
                       Default: None

        :param INT time_wait_state_session_timeout:
            *OPTIONAL* . "set security flow tcp-session time-wait-state session-timeout <value>"
                         Default: None

        :param BOOL commit:
            *OPTIONAL* Default: True

        :param BOOL get_response:
            *OPTIONAL* Default: False

        :return:
            True/False to indicate configure success or failed. Or return commit response according to option get_response

            Option 'return_cmd' used for unit test. Set True to return conf cmds
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["commit"] = self.tool.check_boolean(kwargs.get("commit", True))
        options["get_response"] = self.tool.check_boolean(kwargs.get("get_response", False))
        options["timeout"] = int(kwargs.get("timeout", self.default["conf_commit_timeout"]))
        options["return_cmd"] = kwargs.get("return_cmd", None)

        user_keyword_dict = {
            # option_type, cmd_string
            "fin_invalidate_session":               ("BOOL", "fin-invalidate-session"),
            "no_sequence_check":                    ("BOOL", "no-sequence-check"),
            "no_syn_check":                         ("BOOL", "no-syn-check"),
            "no_syn_check_in_tunnel":               ("BOOL", "no-syn-check-in-tunnel"),
            "rst_invalidate_session":               ("BOOL", "rst-invalidate-session"),
            "rst_sequence_check":                   ("BOOL", "rst-sequence-check"),
            "strict_syn_check":                     ("BOOL", "strict-syn-check"),
            "maximum_window":                       ("STR", "maximum-window"),
            "tcp_initial_timeout":                  ("INT", "tcp-initial-timeout"),
            "time_wait_state_session_ageout":       ("BOOL", "time-wait-state session-ageout"),
            "time_wait_state_session_timeout":      ("INT", "time-wait-state session-timeout"),
            "time_wait_state_apply_to_half_close_state": ("BOOL", "time-wait-state apply-to-half-close-state"),
        }

        base_cmd = "set security flow tcp-session"
        cmd_list = []
        for keyword in user_keyword_dict:
            options[keyword] = kwargs.get(keyword, None)
            if options[keyword] is None:
                continue

            option_type, cmd_string = user_keyword_dict[keyword]
            if option_type == "BOOL":
                cmd_list.append("{} {}".format(base_cmd, cmd_string))
            else:
                cmd_list.append("{} {} {}".format(base_cmd, cmd_string, options[keyword]))

        response = dev.execute_config_command_on_device(
            device=device,
            command=cmd_list,
            get_response=options["get_response"],
            commit=options["commit"],
        )

        if options["return_cmd"] is True:
            response = cmd_list

        device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
        return response

    def configure_flow_traceoptions(self, device, **kwargs):
        """Add flow traceoptions configuration

        For FLOW traceoption, this method will add traceoptions configuration in "set security" and "set security flow".

        :param STR filename:
            *OPTIONAL* traceoption filename. Default:"flow_trace.log" will save to "/var/log" folder

        :param INT|STR file_size:
            *OPTIONAL* trace log file size. Unit: Bytes. Default: 10485760 (10M)

        :param STR flag:
            *OPTIONAL* log level string.  Default: all

        :param BOOL commit:
            *OPTIONAL* Default: True

        :param BOOL get_response:
            *OPTIONAL* Default: False

        :return:
            True/False to indicate configure success or failed. Or return commit response according to option get_response

            Option 'return_cmd' used for unit test. Set True to return conf cmds

        :example:
            For robot

            flows.Configure FLOW Traceoptions    device=${r0}    filename=flow_trace.log    file_size=50M    flag=all
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["filename"] = kwargs.get("filename", "flow_trace.log")
        options["file_size"] = kwargs.get("file_size", 10485760)
        options["flag"] = kwargs.get("flag", "all")
        options["commit"] = self.tool.check_boolean(kwargs.get("commit", True))
        options["get_response"] = self.tool.check_boolean(kwargs.get("get_response", False))
        options["timeout"] = int(kwargs.get("timeout", self.default["conf_commit_timeout"]))
        options["return_cmd"] = kwargs.get("return_cmd", None)

        cmd_list = []
        cmd_list.append("set security traceoptions file {} size {}".format(options["filename"], options["file_size"]))
        cmd_list.append("set security flow traceoptions file {} size {}".format(options["filename"], options["file_size"]))
        cmd_list.append("set security traceoptions flag {}".format(options["flag"]))
        cmd_list.append("set security flow traceoptions flag {}".format(options["flag"]))

        response = dev.execute_config_command_on_device(
            device=device,
            command=cmd_list,
            get_response=options["get_response"],
            commit=options["commit"],
        )

        if options["return_cmd"] is True:
            response = cmd_list

        device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
        return response

    def fetch_flow_session(self, device, **kwargs):
        r"""Fetch flow sessions and return session list

        This method show flow session information and return all flow sessions by LIST. According to different option,
        base on command 'show security flow session', and other options will be tailed to base command.

        FLOW session from Highend/Lowend device have different output. For HE platform, session belong each FPC.PIC
        displayed separately, but LE or VSRX platform only have just 1 PIC so no PIC info in output.

        This method always return a LIST of sessions (even only 1 session in LIST). It is support all SRX series device
        (LowEnd, HighEnd, vSRX, etc..) and Standalone, HA topology.

        Everytime this method invoked for a device, all sessions will be cached internally. Another keyword called
        "verify_flow_session" have ability to get session list from internal cache.

        :param STR options:
            *OPTIONAL* a string contain all options you want that will added to baisc command. default: None

        :param STR more_options:
            *OPTIONAL* Same as "options" but "options" prority is higher. default: None

        :param STR return_type:
            *OPTIONAL* response format that one of "text" or "session_tuple". Default: session_tuple

        :param BOOL return_mode:
            *OPTIONAL* alias of option 'return_type' that response format one of "text", "session_tuple" or "flat_dict".
                       default: session_tuple

        :param INT timeout:
            *OPTIONAL* timeout to get command response. default: 300

        :return:
            If option 'return_type' is 'text', just return device response without any more process. Example:

                Session ID: 64, Policy name: default-policy-logical-system-00/2, Timeout: 2, Valid
                In: 100.1.0.2/1 --> 100.2.0.2/43583;icmp, Conn Tag: 0x0, If: ge-0/0/2.0, Pkts: 1, Bytes: 84,
                Out: 100.2.0.2/43583 --> 100.1.0.2/1;icmp, Conn Tag: 0x0, If: ge-0/0/3.0, Pkts: 1, Bytes: 84,

                Session ID: 65, Policy name: default-policy-logical-system-00/2, Timeout: 2, Valid
                In: 100.1.0.2/2 --> 100.2.0.2/43583;icmp, Conn Tag: 0x0, If: ge-0/0/2.0, Pkts: 1, Bytes: 84,
                Out: 100.2.0.2/43583 --> 100.1.0.2/2;icmp, Conn Tag: 0x0, If: ge-0/0/3.0, Pkts: 1, Bytes: 84,

                Session ID: 66, Policy name: default-policy-logical-system-00/2, Timeout: 4, Valid
                In: 100.1.0.2/3 --> 100.2.0.2/43583;icmp, Conn Tag: 0x0, If: ge-0/0/2.0, Pkts: 1, Bytes: 84,
                Out: 100.2.0.2/43583 --> 100.1.0.2/3;icmp, Conn Tag: 0x0, If: ge-0/0/3.0, Pkts: 1, Bytes: 84,
                Total sessions: 3

            If option 'return_type' is 'session_tuple' (default), append all PICs' session to a tuple. Example

            [
                {
                    "application-traffic-control-rule-name": "INVALID",
                    "application-traffic-control-rule-set-name": "INVALID",
                    "configured-timeout": "1800",
                    "duration": "2",
                    "dynamic-application-name": "junos:UNKNOWN",
                    "encryption-traffic-name": "Unknown",
                    "flow-fpc-pic-id": "on FPC0 PIC2:",
                    "flow-information": [
                        {
                            "byte-cnt": "2816",
                            "conn-tag": "0x0",
                            "dcp-session-id": "20002443",
                            "destination-address": "2000:200::2",
                            "destination-port": "54093",
                            "direction": "In",
                            "fin-sequence": "0",
                            "fin-state": "0",
                            "flag": "0x40001023",
                            "gateway": "2000:100::2",
                            "interface-name": "xe-2/0/0.0",
                            "pkt-cnt": "39",
                            "port-sequence": "0",
                            "protocol": "tcp",
                            "route": "0xd0010",
                            "seq-ack-diff": "0",
                            "session-token": "0x7",
                            "source-address": "2000:100::2",
                            "source-port": "58612",
                            "tunnel-information": "0"
                        },
                        {
                            "byte-cnt": "137776",
                            "conn-tag": "0x0",
                            "dcp-session-id": "20002443",
                            "destination-address": "2000:100::2",
                            "destination-port": "58612",
                            "direction": "Out",
                            "fin-sequence": "0",
                            "fin-state": "0",
                            "flag": "0x40001022",
                            "gateway": "2000:200::2",
                            "interface-name": "xe-2/0/1.0",
                            "pkt-cnt": "93",
                            "port-sequence": "0",
                            "protocol": "tcp",
                            "route": "0xe0010",
                            "seq-ack-diff": "0",
                            "session-token": "0x8",
                            "source-address": "2000:200::2",
                            "source-port": "54093",
                            "tunnel-information": "0"
                        }
                    ],
                    "logical-system": "",
                    "nat-source-pool-name": "Null",
                    "policy": "p1/4",
                    "sess-state": "Valid",
                    "session-flag": "0x40/0x0/0x8003",
                    "session-identifier": "20000753",
                    "session-mask": "0",
                    "start-time": "1200007",
                    "status": "Normal",
                    "timeout": "1798",
                    "wan-acceleration": ""
                }
            ]

            If option 'return_type' is 'flat_dict', will do more processing for each session that from complex DICT to
            FLAT DICT like below:

            # FLAT DICT:
            #   1. combine in_, out_ elements
            #   2. convert all "-" to "_", lowercase all keywords, and transit all value to STRING whatever it is an INT
            #      or IP, HEX, etc..

            [
                {
                    "application_traffic_control_rule_name": "INVALID",
                    "application_traffic_control_rule_set_name": "INVALID",
                    "configured_timeout": "1800",
                    "duration": "2",
                    "dynamic_application_name": "junos:UNKNOWN",
                    "encryption_traffic_name": "Unknown",
                    "flow_fpc_pic_id": "on FPC0 PIC2:",
                    "in_byte_cnt": "2816",
                    "in_conn_tag": "0x0",
                    "in_dcp_session_id": "20002443",
                    "in_destination_address": "2000:200::2",
                    "in_destination_port": "54093",
                    "in_fin_sequence": "0",
                    "in_fin_state": "0",
                    "in_flag": "0x40001023",
                    "in_gateway": "2000:100::2",
                    "in_interface_name": "xe-2/0/0.0",
                    "in_pkt_cnt": "39",
                    "in_port_sequence": "0",
                    "in_protocol": "tcp",
                    "in_route": "0xd0010",
                    "in_seq_ack_diff": "0",
                    "in_session_token": "0x7",
                    "in_source_address": "2000:100::2",
                    "in_source_port": "58612",
                    "in_tunnel_information": "0",
                    "logical_system": "",
                    "nat_source_pool_name": "Null",
                    "out_byte_cnt": "137776",
                    "out_conn_tag": "0x0",
                    "out_dcp_session_id": "20002443",
                    "out_destination_address": "2000:100::2",
                    "out_destination_port": "58612",
                    "out_fin_sequence": "0",
                    "out_fin_state": "0",
                    "out_flag": "0x40001022",
                    "out_gateway": "2000:200::2",
                    "out_interface_name": "xe-2/0/1.0",
                    "out_pkt_cnt": "93",
                    "out_port_sequence": "0",
                    "out_protocol": "tcp",
                    "out_route": "0xe0010",
                    "out_seq_ack_diff": "0",
                    "out_session_token": "0x8",
                    "out_source_address": "2000:200::2",
                    "out_source_port": "54093",
                    "out_tunnel_information": "0",
                    "policy": "p1/4",
                    "sess_state": "Valid",
                    "session_flag": "0x40/0x0/0x8003",
                    "session_identifier": "20000753",
                    "session_mask": "0",
                    "start_time": "1200007",
                    "status": "Normal",
                    "timeout": "1798",
                    "wan_acceleration": ""
                }
            ]

        :example:
            For robot

            ${session_list}    flows.Fetch FLOW Session    device=${r0}    more_options=protocol tcp    return_mode=flat_dict
            :FOR    ${session}    IN    @{session_list}
            \    ...

            For Python

            session_list = fetch_flow_session(device=r0, more_options="protocol tcp", return_mode="FLAT_DICT")
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        opt = {}
        opt["options"] = kwargs.pop('options', None)
        opt["more_options"] = kwargs.pop('more_options', None)
        opt["return_type"] = str(kwargs.pop("return_type", "session_tuple")).strip().upper()
        opt["return_mode"] = str(kwargs.pop("return_mode", opt["return_type"])).strip().upper()
        opt["timeout"] = int(kwargs.pop('timeout', self.default['cli_show_timeout']))

        if opt["return_mode"] not in ("TEXT", "SESSION_TUPLE", "FLAT_DICT"):
            raise ValueError("'return_mode' must be 'SESSION_TUPLE', 'TEXT' or 'FLAT_DICT', not '{}'".format(opt["return_mode"]))

        if opt["return_mode"] in ("SESSION_TUPLE", "FLAT_DICT"):
            response_format = "xml"
        else:
            response_format = "text"

        if opt["options"] is not None:
            opt["more_options"] = opt["options"]

        # combine options to basic command
        cmd = "show security flow session"
        if opt["more_options"] is not None:
            cmd += " {}".format(opt["more_options"])

        dev_fingerprint = str(device)
        if dev_fingerprint not in self.runtime:
            self.runtime[dev_fingerprint] = {}

        if "flow_session_list" not in self.runtime[dev_fingerprint]:
            self.runtime[dev_fingerprint]["flow_session_list_mode"] = None
            self.runtime[dev_fingerprint]["flow_session_list"] = None

        # get flow session
        device.log(message="send cmd: {}".format(cmd), level="INFO")
        response = dev.execute_cli_command_on_device(
            device=device,
            command=cmd,
            channel="text",
            format=response_format,
            timeout=opt["timeout"],
        )

        # whatever response, if user want get "text" mode response, just return here
        if opt["return_mode"] == "TEXT":
            self.runtime[dev_fingerprint]["flow_session_list_mode"] = opt["return_mode"]
            self.runtime[dev_fingerprint]["flow_session_list"] = response
            device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
            return response

        response = self.xml.xml_to_pure_dict(response)
        all_flow_session = []
        all_node_items = self.xml.strip_xml_response(response, return_list=True)
        for node_item in all_node_items:
            info = {}
            if "re-name" in node_item:
                info["re-name"] = node_item["re-name"]

            pic_session_list = node_item["flow-session-information"]
            if not isinstance(pic_session_list, (list, tuple)):
                pic_session_list = [pic_session_list, ]

            for pic_session in pic_session_list:
                # skip this item if no session
                if "flow-session" not in pic_session:
                    continue

                if "flow-fpc-pic-id" in pic_session:
                    info["flow-fpc-pic-id"] = pic_session["flow-fpc-pic-id"]

                flow_session_list = pic_session["flow-session"]
                if not isinstance(flow_session_list, (list, tuple)):
                    flow_session_list = [flow_session_list, ]

                for flow_session in flow_session_list:
                    wing_list = flow_session.pop("flow-information", list())
                    info.update(flow_session)

                    if not isinstance(wing_list, (list, tuple)):
                        wing_list = [wing_list, ]

                    info["flow-information"] = wing_list

                    all_flow_session.append(copy.deepcopy(info))

        all_flow_session = tuple(all_flow_session)
        if opt["return_mode"] == "SESSION_TUPLE":
            self.runtime[dev_fingerprint]["flow_session_list_mode"] = opt["return_mode"]
            self.runtime[dev_fingerprint]["flow_session_list"] = all_flow_session
            device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_flow_session)), level="INFO")
            return all_flow_session

        tuple_session_list = copy.deepcopy(all_flow_session)
        all_flow_session = []
        for tmp_session in tuple_session_list:
            info = {}
            session = copy.deepcopy(tmp_session)        # don't delete to prevent compat hidden info

            # get session In/Out direction's elements
            wing_session_list = session.pop("flow-information", list())

            # flat normal session elements
            session = self.tool.flat_dict(session, parent_key='', separate_char='_', lowercase=True, replace_dash_to_underline=True)
            info.update(session)

            # treat wing sessions. session elements have parent_key according to 'direction' such as in or out
            for wing_session in wing_session_list:
                if "direction" not in wing_session:
                    parent_key = ""         # pragma: no cover
                else:
                    parent_key = wing_session.pop("direction").strip().lower()

                wing_session = self.tool.flat_dict(
                    wing_session,
                    parent_key=parent_key,
                    separate_char='_',
                    lowercase=True,
                    replace_dash_to_underline=True,
                )

                info.update(wing_session)

            all_flow_session.append(copy.deepcopy(info))

        all_flow_session = tuple(all_flow_session)
        self.runtime[dev_fingerprint]["flow_session_list_mode"] = opt["return_mode"]
        self.runtime[dev_fingerprint]["flow_session_list"] = all_flow_session
        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_flow_session)), level="INFO")
        return all_flow_session

    def fetch_flow_cp_session(self, device, **kwargs):
        r"""Fetch all flow cp sessions based on command "show security flow cp-session".

        HighEnd platform support only.

        :param STR more_options:
            *OPTIONAL* String will tailed to base cmd. Default: None

        :param INT node:
            *OPTIONAL* For HA device to get specific node's status. Must one of 0, 1 or None (default)

        :param INT timeout:
            *OPTIONAL* Get response timeout

        :return:
            Return a LIST which contain all cp sessions. Every element in LIST is a DICT for a session. For example:

                [
                    {
                        "dcp_flow_fpc_pic_id":      "on FPC0 PIC1:",
                        "in_source_address":        "121.11.10.2",
                        ...
                    },
                    {
                        "dcp_flow_fpc_pic_id":      "on FPC0 PIC2:",
                        "in_source_address":        "121.11.10.3",
                        ...
                    },
                ]

        :example:
            For robot:

            ${cp_session_list}    flows.Fetch FLOW CP Session    device=${r0}    node=0 (or node0)
            :FOR    ${cp_session}    IN    @{cp_session_list}
            \    ......
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["more_options"] = kwargs.pop("more_options", None)
        options["node"] = kwargs.pop("node", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))

        cmd_element_list = ["show security flow cp-session", ]
        if options["node"] is not None:
            cmd_element_list.append("node {}".format(self.tool.get_node_value(options["node"], mode="INT")))

        if options["more_options"] is not None:
            cmd_element_list.append(options["more_options"])

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_element_list),
            format="xml",
            channel="text",
            timeout=options["timeout"],
        ))
        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return response

        # SA always a DICT, but HA is a LIST that contain 2 nodes' response
        item_list = self.xml.strip_xml_response(response, return_list=True)
        all_entry_list = []
        for item in item_list:
            info = {}
            if "re-name" in item:
                info["re_name"] = item["re-name"]

            pic_session_list = item["flow-session-information"]
            # For if only have one FPC
            if not isinstance(pic_session_list, (list, tuple)):
                pic_session_list = [pic_session_list, ]

            for pic_session in pic_session_list:
                flow_session_list = pic_session.pop("flow-session", list())
                for pic_session_keyword in pic_session:
                    info[self.tool.underscore_and_lowercase_transit(pic_session_keyword)] = pic_session[pic_session_keyword]

                if not flow_session_list:
                    all_entry_list.append(copy.deepcopy(info))
                    continue

                # every flow session should have 2 wings but sometimes maybe only have 1 direction
                if not isinstance(flow_session_list, (list, tuple)):
                    flow_session_list = [flow_session_list, ]

                for session in flow_session_list:
                    wing_list = session.pop("flow-information", list())
                    for session_keyword in session:
                        info[self.tool.underscore_and_lowercase_transit(session_keyword)] = session[session_keyword]

                    if not wing_list:
                        all_entry_list.append(copy.deepcopy(info))
                        continue

                    if not isinstance(wing_list, (list, tuple)):
                        wing_list = [wing_list, ]

                    for wing in wing_list:
                        direction = wing.pop("direction")
                        for wing_keyword in wing:
                            info[self.tool.underscore_and_lowercase_transit("{}_{}".format(direction, wing_keyword))] = wing[wing_keyword]

                    all_entry_list.append(copy.deepcopy(info))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_entry_list)), level="INFO")
        return all_entry_list

    def fetch_flow_cp_session_summary(self, device, **kwargs):
        """Fetch all flow cp sessions based on command "show security flow cp-session summary".

        HighEnd platform support only.

        :param STR more_options:
            *OPTIONAL* String will tailed to base cmd. Default: None

        :param INT node:
            *OPTIONAL* For HA device to get specific node's status. Default: None

                       Must one of 0, 1 or None

        :param INT timeout:
            *OPTIONAL* Get response timeout

        :param BOOL total_all_fpcs:
            *OPTIONAL* Only return all FPCs' total counter. default: False

        :return:
            If total_all_fpcs=${False} (default), will return a LIST that contain all FPCs' info like this:

            [
                {
                    "dcp_flow_fpc_pic_id": "on FPC0 PIC0:",
                    "displayed_session_count": "10",
                    "displayed_session_invalidated": "2",
                    "displayed_session_other": "5",
                    "displayed_session_pending": "1",
                    "displayed_session_valid": "1"
                },
                {
                    "dcp_flow_fpc_pic_id": "on FPC0 PIC1:",
                    "displayed_session_count": "20",
                    "displayed_session_invalidated": "5",
                    "displayed_session_other": "10",
                    "displayed_session_pending": "6",
                    "displayed_session_valid": "3",
                    "max_inet6_session_count": "7549747",
                    "max_session_count": "7549747"
                },
                ......
            ]

            Once total_all_fpcs=${True}, still return a LIST but only contain 1 DICT element (For HA topo, return 2
            DICTs if needed). In this DICT, all FPCs' counters are sumarized. Below based on above output but summarized

             [
                {
                    "dcp_flow_fpc_pic_id": "on FPC0 PIC1:",     <<< not summarized but only updated
                    "displayed_session_count": "30",
                    "displayed_session_invalidated": "7",
                    "displayed_session_other": "15",
                    "displayed_session_pending": "7",
                    "displayed_session_valid": "4",
                    "max_inet6_session_count": "7549747",
                    "max_session_count": "7549747",
                },
            ]

            For HA, every node have a summarized DICT (if option 'node' is given, return 1 DICT):
            [
                {
                    "re_name": "node0"
                    "dcp_flow_fpc_pic_id": "on FPC0 PIC1:",     <<< not combined but updated
                    ...
                },
                {
                    "re_name": "node1"
                    "dcp_flow_fpc_pic_id": "on FPC0 PIC1:",     <<< not combined but updated
                    ...
                },
            ]

        :example:
            For robot

            ${all_fpcs_counter}    flows.Fetch FLOW CP Session Summary    device=${r0}    total_all_fpcs=True

            For Python

            all_fpcs_counter = fetch_flow_cp_session_summary(device=r0, total_all_fpcs=True)
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["more_options"] = kwargs.pop("more_options", None)
        options["node"] = kwargs.pop("node", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))
        options["total_all_fpcs"] = self.tool.check_boolean(kwargs.pop("total_all_fpcs", False))

        cmd_element_list = ["show security flow cp-session summary", ]
        if options["node"] is not None:
            cmd_element_list.append("node {}".format(self.tool.get_node_value(options["node"], mode="INT")))

        if options["more_options"] is not None:
            cmd_element_list.append(options["more_options"])

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_element_list),
            format="xml",
            channel="text",
            timeout=options["timeout"],
        ))
        if response is False:
            device.log(message="{} return value: {}".format(func_name, response), level="INFO")
            return False

        # After fetch flow cp-session summary xml response, there are 2 types of xml structures. One is none-root-tag
        # xml and the other is have-root-tag.
        #
        # For none-root-tag xml, "flow-session-information" contain all elements but no "flow-session-per-pic"
        # For have-root-tag xml, "flow-session-per-pic" is under "flow-session-information", and new element
        # "dcp-flow-session-summary-information" added
        #
        response = self.xml.strip_xml_response(response, return_list=True)
        all_entry_list = []
        for node_item in response:
            info = {}
            if "re-name"in node_item:
                info["re_name"] = str(node_item["re-name"])

            flow_session_list = self.tool.set_element_list(node_item["flow-session-information"])
            # have root tag output
            if len(flow_session_list) >= 1 and "flow-session-per-pic" in flow_session_list[0]:
                flow_session_list = self.tool.set_element_list(flow_session_list[0]["flow-session-per-pic"])
                for flow_session in flow_session_list:
                    entry = self.tool.flat_dict(
                        flow_session.pop("dcp-flow-session-summary-information"),
                        parent_key='',
                        separate_char='_',
                        lowercase=True,
                        replace_dash_to_underline=True,
                    )
                    entry.update(self.tool.flat_dict(
                        flow_session,
                        parent_key='',
                        separate_char='_',
                        lowercase=True,
                        replace_dash_to_underline=True,
                    ))
                    entry.update(info)

                    # compatible support
                    compatible_element = {}
                    for keyword in entry:
                        match = re.match(r"dcp_(displayed_\w+)", keyword)
                        if match:
                            compatible_element[match.group(1)] = entry[keyword]
                    entry.update(compatible_element)

                    all_entry_list.append(copy.deepcopy(entry))

            # no root tag output
            else:
                for flow_session in flow_session_list:
                    for keyword in flow_session:
                        info[self.tool.underscore_and_lowercase_transit(keyword)] = flow_session[keyword]

                    all_entry_list.append(copy.deepcopy(info))

        return_value = all_entry_list
        only_update_element_list = (
            "re_name",
            "dcp_flow_fpc_id",
            "dcp_flow_pic_id",
            "dcp_flow_fpc_pic_id",
            "flow_fpc_id",
            "flow_pic_id",
        )
        if options["total_all_fpcs"] is True:
            return_value = self._summarize_all_fpcs_counter(
                entry_list=all_entry_list,
                only_update_element_list=only_update_element_list,
            )

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(return_value)), level="INFO")
        return return_value

    def fetch_flow_status(self, device, **kwargs):
        """Fetch all flow module's status based on command "show security flow status" command

        :param INT timeout:
            *OPTIONAL* Get response timeout

        :param STR node:
            *OPTIONAL* For HA device to get specific node's status. Must one of 0, 1 or None (default)

            **If node=None but device is HA, will set this option=0 automatically**

        :param BOOL return_mode:
            *OPTIONAL* return flow status as 'normal' or 'flat_dict'. default: "normal"

        :return:
            Return DICT contain all status.

            If return_mode=normal (default), return complex DICT:

            {
                "flow-status-all": {
                    "flow-forwarding-mode": {
                        "flow-forwarding-mode-inet": "flow based",
                        "flow-forwarding-mode-inet6": "flow based",
                        "flow-forwarding-mode-iso": "drop",
                        "flow-forwarding-mode-mpls": "drop"
                    },
                    "flow-ipsec-performance-acceleration": {
                        "ipa-status": "off"
                    },
                    "flow-packet-ordering": {
                        "ordering-mode": "Hardware"
                    },
                    "flow-session-distribution": {
                        "gtpu-distr-status": "Disabled",
                        "mode": "Hash-based"
                    },
                    "flow-trace-option": {
                        "flow-trace-options": "all",
                        "flow-trace-status": "on"
                    }
                }
            }

            If return_mode=flat_dict:

            {
                "flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet": "flow based",
                "flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet6": "flow based",
                "flow_status_all_flow_forwarding_mode_flow_forwarding_mode_iso": "drop",
                "flow_status_all_flow_forwarding_mode_flow_forwarding_mode_mpls": "drop",
                "flow_status_all_flow_ipsec_performance_acceleration_ipa_status": "off",
                "flow_status_all_flow_packet_ordering_ordering_mode": "Hardware",
                "flow_status_all_flow_session_distribution_gtpu_distr_status": "Disabled",
                "flow_status_all_flow_session_distribution_mode": "Hash-based",
                "flow_status_all_flow_trace_option_flow_trace_options": "all",
                "flow_status_all_flow_trace_option_flow_trace_status": "on"
            }

        :example:
            For robot

            ${flow_status}    flows.Fetch FLOW Status    device=${r0}    return_mode=FLAT_DICT
            Should Be True    '${flow_status["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet"]}' == 'flow based'
            Should Be True    '${flow_status["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet6"]}' == 'flow based'

            # better solution is keyword "Verify FLOW Status":

            ${status}    flows.Verify FLOW Status    device=${r0}
            ...    forwarding_mode_inet=flow based
            ...    forwarding_mode_inet6=flow based
            ...    session_distribution_mode=Hash-based
            Should Be True    ${status}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))
        options["node"] = kwargs.pop("node", None)
        options["return_mode"] = str(kwargs.pop("return_mode", "normal")).strip().upper()

        cmd = "show security flow status"

        if options["node"] is None and device.is_ha() is True:
            options["node"] = 0

        if options["node"] is not None:
            cmd += " node {}".format(self.tool.get_node_value(options["node"], mode="INT"))

        xml_dict = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=cmd,
            format="xml",
            channel="text",
            timeout=options["timeout"],
        ))

        if xml_dict is False:
            device.log(message="{} return value: {}".format(func_name, xml_dict), level="INFO")
            return False

        xml_dict = self.xml.strip_xml_response(xml_dict, return_list=False)
        if options["return_mode"] == "FLAT_DICT":
            xml_dict = self.tool.flat_dict(
                dict_variable=xml_dict,
                parent_key="",
                separate_char="_",
                lowercase=True,
                replace_dash_to_underline=True,
            )

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(xml_dict)), level="INFO")
        return xml_dict

    def fetch_flow_statistics(self, device, **kwargs):
        """Fetch FLOW statistics based on cmd "show security flow statistics"

        :param int timeout:
            *OPTIONAL* Get response timeout

        :param str node:
            *OPTIONAL* For HA device to get specific node's status. Default: None

                       Must one of 0, 1 or None

        :param BOOL return_mode:
            *OPTIONAL* See module doc. default: normal

        :return:
            if return_mode is 'normal' (default), will return a DICT only strip ["rpc-reply"] (SA topo) or
            ["rpc-reply"]["multi-routing-engine-results"]["multi-routing-engine-item"] (HE topo). For example:

            {
                "flow-statistics-all": [
                    {
                        "flow-frag-count-fwd": "0",
                        "flow-llf-pkt-count-prd": "0",
                        "flow-pkt-count-drop": "0",
                        "flow-pkt-count-fwd": "122",
                        "flow-session-count-valid": "4",
                        "flow-spu-id": "of FPC0 PIC1:"
                    },
                    .....
                ]
            }

            if return_mode is flat_dict. return a LIST like below, you can see all dash (-) converted to underscore (_):

            [
                {
                    "flow_frag_count_fwd": "0",
                    "flow_llf_pkt_count_prd": "0",
                    "flow_pkt_count_drop": "0",
                    "flow_pkt_count_fwd": "122",
                    "flow_session_count_valid": "4",
                    "flow_spu_id": "of FPC0 PIC1:"
                },
                ......
            ]

            For HA topo, "re_name" added. Even for LE platform, still return a LIST:

            [
                {
                    "flow_frag_count_fwd": "0",
                    "flow_pkt_count_drop": "705",
                    "flow_pkt_count_fwd": "705",
                    "flow_session_count_valid": "0",
                    "re_name": "node0",
                    "tunnel_frag_gen_post": "0",
                    "tunnel_frag_gen_pre": "0"
                }
            ]

            There is no option "total_all_fpcs" to summarized all PIC's result on HE platform. For HE, last element in
            LIST already summarized all counter by device.

        :example:
            For robot

            ${statistics_list}    flows.Fetch FLOW Statistics    device=${r0}    return_mode=FLAT_DICT
            ${summarized_counters}    Set Variable    ${statistics_list[-1]}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))
        options["return_mode"] = str(kwargs.pop("return_mode", "normal")).strip().upper()
        options["node"] = kwargs.pop("node", None)

        cmd = "show security flow statistics"
        if options["node"] is not None:
            cmd += " node {}".format(self.tool.get_node_value(options["node"], mode="INT"))

        xml_dict = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=cmd,
            format="xml",
            channel="text",
            timeout=options["timeout"],
        ))

        if xml_dict is False:
            device.log(message="{} return value: {}".format(func_name, xml_dict), level="INFO")
            return False

        xml_dict = self.xml.strip_xml_response(xml_dict, return_list=False)
        return_value = xml_dict

        if options["return_mode"] == "FLAT_DICT":
            if not isinstance(xml_dict, (list, tuple)):
                xml_dict = [xml_dict, ]

            all_entry_list = []
            for node_item in xml_dict:
                info = {}
                if "re-name" in node_item:
                    info["re_name"] = node_item["re-name"]

                if "flow-statistics-all" not in node_item:
                    all_entry_list.append(copy.deepcopy(info))
                    continue

                flow_statistics_entry_list = node_item["flow-statistics-all"]
                if not isinstance(flow_statistics_entry_list, (list, tuple)):
                    flow_statistics_entry_list = [flow_statistics_entry_list, ]

                for entry in flow_statistics_entry_list:
                    info.update(self.tool.flat_dict(
                        dict_variable=entry,
                        parent_key='',
                        separate_char='_',
                        lowercase=True,
                        replace_dash_to_underline=True,
                    ))
                    all_entry_list.append(copy.deepcopy(info))

            return_value = all_entry_list

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(return_value)), level="INFO")
        return return_value

    def fetch_flow_gate(self, device, **kwargs):
        r"""Fetch FLOW gate info based on cmd "show security flow gate"

        :param INT|STR node:
            *OPTIONAL* For HA device to get specific node's status. Must one of 0, 1 or None (default)

        :param INT timeout:
            *OPTIONAL* Get response timeout

        :param STR more_options:
            *OPTIONAL* Will tailed to base command. default: None

        :param BOOL return_mode:
            *OPTIONAL* See module doc. default: normal

        :return:
            If return_mode is "normal" (default), will return a DICT only strip ["rpc-reply"] (SA topo) or
            ["rpc-reply"]["multi-routing-engine-results"]["multi-routing-engine-item"] (HE topo).

            [
                {
                    "flow-gate-information": [
                        {
                            "displayed-gate-count": "0",
                            "displayed-gate-invalidated": "0",
                            "displayed-gate-other": "0",
                            "displayed-gate-pending": "0",
                            "displayed-gate-valid": "0",
                            "flow-gate-fpc-pic-id": "on FPC2 PIC0:"
                        },
                        {
                            "displayed-gate-count": "0",
                            "displayed-gate-invalidated": "0",
                            "displayed-gate-other": "0",
                            "displayed-gate-pending": "0",
                            "displayed-gate-valid": "0",
                            "flow-gate-fpc-pic-id": "on FPC2 PIC1:"
                        },
                        ......
                    ],
                    "re-name": "node0"
                },
                {
                    "flow-gate-information": [
                        {
                            "displayed-gate-count": "0",
                            "displayed-gate-invalidated": "0",
                            "displayed-gate-other": "0",
                            "displayed-gate-pending": "0",
                            "displayed-gate-valid": "0",
                            "flow-gate-fpc-pic-id": "on FPC2 PIC0:"
                        },
                        {
                            "displayed-gate-count": "0",
                            "displayed-gate-invalidated": "0",
                            "displayed-gate-other": "0",
                            "displayed-gate-pending": "0",
                            "displayed-gate-valid": "0",
                            "flow-gate-fpc-pic-id": "on FPC2 PIC1:"
                        },
                        ......
                    ],
                    "re-name": "node1"
                }
            ]

            If return_mode is "flat_dict", return a LIST that have all SPU's result

            [
                {
                    "displayed_gate_count": "0",
                    "displayed_gate_invalidated": "0",
                    "displayed_gate_other": "0",
                    "displayed_gate_pending": "0",
                    "displayed_gate_valid": "0",
                    "flow_gate_fpc_pic_id": "on FPC2 PIC0:",
                    "re_name": "node0"
                },
                {
                    "displayed_gate_count": "0",
                    "displayed_gate_invalidated": "0",
                    "displayed_gate_other": "0",
                    "displayed_gate_pending": "0",
                    "displayed_gate_valid": "0",
                    "flow_gate_fpc_pic_id": "on FPC2 PIC1:",
                    "re_name": "node0"
                },
                {
                    "displayed_gate_count": "0",
                    "displayed_gate_invalidated": "0",
                    "displayed_gate_other": "0",
                    "displayed_gate_pending": "0",
                    "displayed_gate_valid": "0",
                    "flow_gate_fpc_pic_id": "on FPC2 PIC0:",
                    "re_name": "node1"
                },
                {
                    "displayed_gate_count": "0",
                    "displayed_gate_invalidated": "0",
                    "displayed_gate_other": "0",
                    "displayed_gate_pending": "0",
                    "displayed_gate_valid": "0",
                    "flow_gate_fpc_pic_id": "on FPC2 PIC1:",
                    "re_name": "node1"
                },
                ......
            ]

        :example:
            For robot

            ${gate_entry_list}    flows.Fetch FLOW Gate    device=${r0}    return_mode=flat_dict
            :FOR    ${gate}    IN    ${gate_entry_list}
            \    ......
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["node"] = kwargs.pop("node", None)
        options["more_options"] = kwargs.pop("more_options", None)
        options["return_mode"] = str(kwargs.pop("return_mode", "normal")).strip().upper()
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))

        # combine each options
        cmd_element_list = ["show security flow gate", ]
        if options["more_options"] is not None:
            cmd_element_list.append(options["more_options"])

        if options["node"] is not None:
            cmd_element_list.append("node {}".format(self.tool.get_node_value(options["node"], mode="INT")))

        xml_dict = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_element_list),
            format="xml",
            channel="text",
            timeout=options["timeout"],
        ))

        if xml_dict is False:
            device.log(message="{} return value: {}".format(func_name, xml_dict), level="INFO")
            return False

        xml_dict = self.xml.strip_xml_response(xml_dict, return_list=False)
        if options["return_mode"] != "FLAT_DICT":
            device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(xml_dict)), level="INFO")
            return xml_dict

        # transit to flat dict
        if not isinstance(xml_dict, (list, tuple)):
            xml_dict = [xml_dict, ]

        all_entry_list = []
        for entry in xml_dict:
            info = {}
            if "re-name" in entry:
                info["re_name"] = entry["re-name"]

            fpc_entry_list = entry["flow-gate-information"]

            if not isinstance(fpc_entry_list, (list, tuple)):
                fpc_entry_list = [fpc_entry_list, ]

            for fpc_entry in fpc_entry_list:
                for keyword in fpc_entry:
                    info[self.tool.underscore_and_lowercase_transit(keyword)] = fpc_entry[keyword]

                all_entry_list.append(copy.deepcopy(info))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_entry_list)), level="INFO")
        return all_entry_list

    def fetch_flow_session_summary(self, device, **kwargs):
        """Based on cmd 'show security flow session summary' to fetch summary info

        Support LE/HE platform and SA/HA topology.

        :param STR more_options:
            *OPTIONAL* extensive options will tailed to basic cmd. default: None

        :param STR|INT node:
            *OPTIONAL* node number or name. default: None

        :param INT timeout:
            *OPTIONAL* get response timeout. default: 300

        :param BOOL total_all_fpcs:
            *OPTIONAL* Only return all FPCs' total counter. default: False

        :return:
            If total_all_fpcs=${False} (default), will return a LIST that contain all FPCs' info like this:

            [
                {
                    "active_multicast_sessions": "0",
                    "active_services_offload_sessions": "0",
                    "active_session_invalidated": "0",
                    "active_session_other": "0",
                    "active_session_pending": "0",
                    "active_session_valid": "0",
                    "active_sessions": "0",
                    "active_unicast_sessions": "0",
                    "failed_sessions": "0",
                    "max_sessions": "6291456",
                    "re_name": "node0"
                },
                {
                    "active_multicast_sessions": "0",
                    "active_services_offload_sessions": "0",
                    "active_session_invalidated": "1",
                    "active_session_other": "0",
                    "active_session_pending": "0",
                    "active_session_valid": "0",
                    "active_sessions": "1",
                    "active_unicast_sessions": "0",
                    "failed_sessions": "0",
                    "max_sessions": "6291456",
                    "re_name": "node0"
                },
                ......
            ]

            Once total_all_fpcs=${True}, still return a LIST but only contain 1 DICT element (For HA topo, return 2
            DICTs if needed). In this DICT, all FPCs' counters are sumarized. For above output, it is below:

             [
                {
                    "active_multicast_sessions": "0",
                    "active_services_offload_sessions": "0",
                    "active_session_invalidated": "1",
                    "active_session_other": "0",
                    "active_session_pending": "0",
                    "active_session_valid": "0",
                    "active_sessions": "1",
                    "active_unicast_sessions": "0",
                    "failed_sessions": "0",
                    "max_sessions": "12582912",
                    "re_name": "node0",
                },
            ]

            For HA, every node have a summarized DICT like this (if option 'node' is given, return 1 DICT):
            [
                {
                    "re_name": "node0"
                    "active_multicast_sessions": "0",
                    ...
                },
                {
                    "re_name": "node1"
                    "active_multicast_sessions": "0",
                    ...
                },
            ]

        :example:
            For robot

            ${all_fpcs_counter}    flows.Fetch FLOW Session Summary    device=${r0}    total_all_fpcs=${True}

            For Python

            all_fpcs_counter = fetch_flow_session_summary(device=r0, total_all_fpcs=True)

        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["more_options"] = kwargs.pop("more_options", None)
        options["node"] = kwargs.pop("node", None)
        options["total_all_fpcs"] = self.tool.check_boolean(kwargs.pop("total_all_fpcs", False))
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_show_timeout"]))

        cmd_elements = []
        cmd_elements.append("show security flow session summary")
        if options["more_options"] is not None:
            cmd_elements.append(options["more_options"])

        if options["node"] is not None:
            cmd_elements.append("node {}".format(self.tool.get_node_value(options["node"], mode="INT")))

        response = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_elements),
            channel="text",
            format="xml",
            timeout=options["timeout"],
        ))
        if response is False:
            return False

        # After fetch flow session summary xml response, there are 2 types of xml structures. One is none-root-tag xml
        # and the other is have-root-tag.
        #
        # For none-root-tag xml, "flow-session-summary-information" may in parallel of "flow-session-information"
        # For have-root-tag xml, "flow-session-per-pic" is under "flow-session-information", and
        # "flow-session-summary-information" is under "flow-session-per-pic"
        #
        response = self.xml.strip_xml_response(response, return_list=True)
        summary_entry_list = []
        for node_ele in response:
            info = {}
            if "re-name" in node_ele:
                info["re_name"] = node_ele["re-name"]

            if "flow-session-information" not in node_ele:
                continue

            if "flow-session-summary-information" in node_ele:
                all_session_list = self.tool.set_element_list(node_ele["flow-session-summary-information"])
            else:
                all_session_list = self.tool.set_element_list(node_ele["flow-session-information"])

            if len(all_session_list) >= 1 and "flow-session-per-pic" in all_session_list[0]:
                all_session_list = self.tool.set_element_list(all_session_list[0]["flow-session-per-pic"])

            for session in all_session_list:
                # have root tag
                if "flow-session-summary-information" in session or "dcp-flow-session-summary-information" in session:
                    if "flow-session-summary-information" in session:
                        summary_keyword = "flow-session-summary-information"
                    else:
                        summary_keyword = "dcp-flow-session-summary-information"

                    all_summary_session_list = self.tool.set_element_list(session.pop(summary_keyword))
                    entry = self.tool.flat_dict(
                        session,
                        parent_key='',
                        separate_char='_',
                        lowercase=True,
                        replace_dash_to_underline=True,
                    )
                    for summary_session in all_summary_session_list:
                        entry.update(self.tool.flat_dict(
                            summary_session,
                            parent_key='',
                            separate_char='_',
                            lowercase=True,
                            replace_dash_to_underline=True,
                        ))

                        tmp_dict = {}
                        for keyword in entry:
                            match = re.match(r"dcp_(\S+)", keyword)
                            if match:
                                tmp_dict[match.group(1)] = entry[keyword]

                        entry.update(tmp_dict)
                        entry.update(info)

                        summary_entry_list.append(copy.deepcopy(entry))

                # none root tag
                else:
                    entry = self.tool.flat_dict(
                        session,
                        parent_key='',
                        separate_char='_',
                        lowercase=True,
                        replace_dash_to_underline=True,
                    )
                    entry.update(info)
                    summary_entry_list.append(copy.deepcopy(entry))

        return_value = summary_entry_list
        only_update_element_list = (
            "re_name",
            "dcp_flow_fpc_id",
            "dcp_flow_pic_id",
            "dcp_flow_fpc_pic_id",
            "flow_fpc_id",
            "flow_pic_id",
        )
        if options["total_all_fpcs"] is True:
            return_value = self._summarize_all_fpcs_counter(
                entry_list=summary_entry_list,
                only_update_element_list=only_update_element_list,
            )

        device.log(message="'{}' return value:\n{}".format(func_name, self.tool.pprint(return_value)), level="INFO")
        return return_value

    def fetch_flow_session_on_vty(self, device, **kwargs):
        r"""On VTY mode, fetch flow session's detail information

        Based on VTY command "show usp flow session all" and return a list which contain all session infos

        :param STR destination:
            *OPTIONAL* Get session information from CP, SPU or ALL. Default: CP

        :return:
            Return a list contain all session informations. Every element for one session. Raise ValueError or
            RuntimeError if failed

            [
                {
                    "backup_session": false,
                    "failover_cnt": "37",
                    "flags": "80800040/8002000/3",
                    "forward_session": true,
                    "in_bytes": "60",
                    "in_classifier_cos": "0",
                    "in_conn_tag": "0x0",
                    "in_cosflag": "0x0",
                    "in_cp_sess_spu_id": "0",
                    "in_cp_session_id": "0",
                    "in_diff": "0",
                    "in_dp": "0",
                    "in_dst_addr": "121.11.30.2",
                    "in_dst_port": "23",
                    "in_flag": "0021",
                    "in_if": "reth1.0 (7)",
                    "in_nh": "0x0",
                    "in_pkts": "1",
                    "in_pmtu": "1500",
                    "in_protocol": "6",
                    "in_spd_info": "0000",
                    "in_src_addr": "121.11.10.2",
                    "in_src_port": "34998",
                    "in_thread_id": "1",
                    "in_tunnel_info": "0x0",
                    "in_tunnel_pmtu": "0",
                    "in_wsf": "0",
                    "logical_system": "root-logical-system",
                    "out_bytes": "0",
                    "out_classifier_cos": "0",
                    "out_conn_tag": "0x0",
                    "out_cosflag": "0x0",
                    "out_cp_sess_spu_id": "0",
                    "out_cp_session_id": "0",
                    "out_diff": "0",
                    "out_dp": "0",
                    "out_dst_addr": "121.11.30.2",
                    "out_dst_port": "23",
                    "out_flag": "0020",
                    "out_if": "reth3.0 (8)",
                    "out_nh": "0x572f28",
                    "out_pkts": "0",
                    "out_pmtu": "1500",
                    "out_protocol": "6",
                    "out_spd_info": "0000",
                    "out_src_addr": "121.11.10.2",
                    "out_src_port": "34998",
                    "out_thread_id": "255",
                    "out_tunnel_info": "0x0",
                    "out_tunnel_pmtu": "0",
                    "out_wsf": "0",
                    "policy": "2",
                    "retry_cnt": "0",
                    "session_id": "401187",
                    "state": "3",
                    "sync_id": "0x10186d7e",
                    "timeout": "6s 6s"
                },
                ......
            ]

        :example:
            For robot

            ${vty_flow_session_list}    flows.Fetch FLOW Session On VTY    device=${r0}    destination=CP
            :FOR    ${session}    IN    @{vty_flow_session_list}
            \    ......
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["destination"] = str(kwargs.get("destination", "CP")).upper()

        if options["destination"] not in ("CP", "SPU", "ALL"):
            raise ValueError("""option 'destination' should be 'CP', 'SPU' or 'ALL' but got '{}'""".format(options["destination"]))

        # VTY session looks like below:
        # Session Id: 401190, Logical system: root-logical-system, Policy: 2, Timeout: 14396s 14396s , state: 3, flags: 10000040/0/8003
        # Backup, failover cnt 9, sync id 0x200001c7, retry cnt 0,0
        #   (in)*  : 121.11.10.2/34998 -> 121.11.30.2/23;6, Conn Tag: 0x0, If: reth1.0 (7), CP session Id: 0, CP sess SPU Id: 0, ...
        #            thread id:1, classifier cos: 0, dp: 0, cosflag 0x0, nh: 0x5393c2, tunnel_info: 0x0, pkts: 0, bytes: 0
        #            pmtu : 1500,  tunnel pmtu: 0
        #   (out)  : 121.11.10.2/34998 <- 121.11.30.2/23;6, Conn Tag: 0x0, If: reth3.0 (8), CP session Id: 0, CP sess SPU Id: 0, ...
        #            thread id:255, classifier cos: 0, dp: 0, cosflag 0x0, nh: 0x572f28, tunnel_info: 0x0, pkts: 0, bytes: 0
        #            pmtu : 1500,  tunnel pmtu: 0
        response = dev.execute_vty_command_on_device(device=device, destination=options["destination"], command="show usp flow session all")
        session_line_blocks = []
        specific_session_lines = []

        # split each line and gather specific session lines
        for line in response.splitlines():
            line = line.strip()
            if not line or re.search(r"\={3,}\s+tnp\S+\s+\={3,}", line):
                continue

            match = re.match(r"\s*Session Id:\s+\d+", line)
            if match:
                session_line_blocks.append(specific_session_lines)
                specific_session_lines = [line, ]
                continue

            specific_session_lines.append(line)

        if specific_session_lines:
            session_line_blocks.append(specific_session_lines)

        # for specific session, each argument are separated by comma, so we do below step:
        # +   split line by comma (,) to get each argument
        # +   split each argument by colon (:) to separate argument name and value, and argument name convert to lower
        #     case and space to '_'
        # +   treat some special cases
        # +   some elements are special that we need treat one by one
        convert_to_valid_keyword = lambda x: re.sub(r"\s+|\-", "_", str(x).lower())

        return_value = []

        special_case_pattern_list = (
            (re.compile(r"Anchor tunnel session with nsp_tunnel - (\S+), tunnel info - (\S+)", re.I), "anchor_tunnel_session_with_nsp_tunnel", "tunnel_info"),
            (re.compile(r"iked_dist_id (\S+), anchor spu id (\S+)", re.I), "iked_dist_id", "anchor_spu_id"),
            (re.compile(r"tunnel id: (\S+), PMTU tunnel overhead: (\S+), flag (\S+), tun_flag (\S+)", re.I), "tunnel_id", "pmtu_tunnel_overhead", "flag", "tun_flag"),
            (re.compile(r"Bind if - (\S+), If - (\S+), HA if - (\S+)", re.I), "bind_if", "if", "ha_if"),
            (re.compile(r"tunnel session token (\S+) nt_next (\S+) nt_prev (\S+)", re.I), "tunnel_session_token", "nt_next", "nt_prev"),
            (re.compile(r"tunnel session nexthop (\S+)\s+final nh (\S+)", re.I), "tunnel_session_nexthop", "final_nh"),
        )

        for line_block in session_line_blocks:
            session_info = {}
            keyword_prefix = ""
            for line in line_block:
                # treat lines are special
                special_case = False
                for case in special_case_pattern_list:
                    match = re.search(case[0], line)
                    if match:
                        for group_index in range(1, len(case)):
                            session_info[case[group_index]] = match.group(group_index)
                        special_case = True
                        continue

                if special_case is True or re.search(r"CP session not installed", line, re.I):
                    continue

                elements = re.split(r",", line)
                for element in elements:
                    splited_element = re.split(r":", element, maxsplit=1)
                    keyword = convert_to_valid_keyword(splited_element[0].strip())
                    if r"(in)" in keyword:
                        keyword_prefix = "in_"
                    elif r"(out)" in keyword:
                        keyword_prefix = "out_"

                    if len(splited_element) == 2:
                        match = re.search(r"(\-\>|\<\-)", splited_element[1])
                        if match:
                            src_elements, _, dst_elements = re.split(r"(\-\>|\<\-)", splited_element[1])

                            session_info[keyword_prefix + "src_addr"], session_info[keyword_prefix + "src_port"] = re.split(r"/", src_elements.strip())
                            session_info[keyword_prefix + "dst_addr"], session_info[keyword_prefix + "dst_port"], session_info[keyword_prefix + "protocol"] = re.split(r"/|;", dst_elements.strip())
                            continue

                        session_info[keyword_prefix + keyword] = splited_element[1].strip()
                    else:
                        session_info[keyword_prefix + keyword] = None

            # some special case
            # 1. For HA topo, some session is backup or forward session. So add backup_session=True|False to indicate this
            need_delete_keyword = []
            need_add_keyword = {}

            for keyword in ("backup", "forward"):
                if keyword in session_info:
                    need_add_keyword["{}_session".format(keyword)] = True
                    need_delete_keyword.append(keyword)
                else:
                    need_add_keyword["{}_session".format(keyword)] = False

            # 2. failover cnt is not separated by colon, so separated them
            # 3. retry cnt's value is "retry cnt 0,0", this means value separated by comma in wrong behavior, so change them
            # 4. in/out cosflag is not separated by colon, so separated them
            # 5. sync_id is not separated by colon, so separated them
            for keyword in session_info:
                match = re.match(r"failover_cnt_(\d+)$", keyword)
                if match:
                    need_add_keyword["failover_cnt"] = match.group(1)
                    need_delete_keyword.append(keyword)
                    continue

                match = re.match(r"retry_cnt_(\d+)$", keyword)
                if match:
                    need_add_keyword["retry_cnt"] = match.group(1)
                    need_delete_keyword.append(keyword)
                    continue

                match = re.match(r"(in|out)_cosflag_(\S+)", keyword)
                if match:
                    need_add_keyword[match.group(1) + "_cosflag"] = match.group(2)
                    need_delete_keyword.append(keyword)
                    continue

                if keyword.isdigit() and session_info[keyword] is None:
                    need_delete_keyword.append(keyword)
                    continue

                match = re.match(r"sync_id_(\S+)$", keyword)
                if match:
                    need_add_keyword["sync_id"] = match.group(1)
                    need_delete_keyword.append(keyword)
                    continue

            for keyword in need_delete_keyword:
                del session_info[keyword]

            session_info.update(need_add_keyword)
            return_value.append(session_info)

        return_value = return_value[1:]
        device.log(message="'{}' return value:\n{}".format(func_name, self.tool.pprint(return_value)), level="INFO")
        return return_value

    def fetch_flow_pmi_statistics(self, device, **kwargs):
        r"""Fetch FLOW pmi statistics based on cmd "show security flow pmp statistics"

        :param int timeout:
            *OPTIONAL* Get response timeout

        :param str node:
            *OPTIONAL* For HA device to get specific node's status. Default: None

                       Must one of 0, 1 or None

        :param BOOL return_mode:
            *OPTIONAL* See module doc. default: normal

        :return:
            if return_mode is 'normal' (default), will strip ["rpc-reply"] (SA topo) or
            ["rpc-reply"]["multi-routing-engine-results"]["multi-routing-engine-item"] (HE topo), and then return a LIST
            that every element is DICT. For example (For SA topo, still a LIST but only contain 1 DICT):

            [
                {
                    "flow-pmi-statistics": {
                        "pmi-decap-bytes": "0",
                        "pmi-decap-pkts": "0",
                        "pmi-drop": "0",
                        "pmi-encap-bytes": "0",
                        "pmi-encap-pkts": "0",
                        "pmi-rfp": "0",
                        "pmi-rx": "0",
                        "pmi-tx": "0"
                    },
                    "re-name": "node0"
                },
                {
                    "flow-pmi-statistics": {
                        "pmi-decap-bytes": "0",
                        "pmi-decap-pkts": "0",
                        "pmi-drop": "0",
                        "pmi-encap-bytes": "0",
                        "pmi-encap-pkts": "0",
                        "pmi-rfp": "0",
                        "pmi-rx": "0",
                        "pmi-tx": "0"
                    },
                    "re-name": "node1"
                }
            ]

            if return_mode is flat_dict. above will convered to flat like:

            [
                {
                    "pmi_decap_bytes": "0",
                    "pmi_decap_pkts": "0",
                    "pmi_drop": "0",
                    "pmi_encap_bytes": "0",
                    "pmi_encap_pkts": "0",
                    "pmi_rfp": "0",
                    "pmi_rx": "0",
                    "pmi_tx": "0",
                    "re_name": "node0"
                },
                {
                    "pmi_decap_bytes": "0",
                    "pmi_decap_pkts": "0",
                    "pmi_drop": "0",
                    "pmi_encap_bytes": "0",
                    "pmi_encap_pkts": "0",
                    "pmi_rfp": "0",
                    "pmi_rx": "0",
                    "pmi_tx": "0",
                    "re_name": "node1"
                }
            ]

        :example:
            For robot

            ${pmi_statistics_enry_list}    flows.Fetch FLOW PMI Statistics    device=${r0}    return_mode=flat_dict
            :FOR    ${entry}    IN    @{pmi_statistics_enry_list}
            \    ......
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))
        options["return_mode"] = str(kwargs.pop("return_mode", "normal")).strip().upper()
        options["node"] = kwargs.pop("node", None)

        cmd = "show security flow pmi statistics"
        if options["node"] is not None:
            cmd += " node {}".format(self.tool.get_node_value(options["node"], mode="INT"))

        xml_dict = self.xml.xml_to_pure_dict(dev.execute_cli_command_on_device(
            device=device,
            command=cmd,
            format="xml",
            channel="text",
            timeout=options["timeout"],
        ))

        if xml_dict is False:
            device.log(message="{} return value: {}".format(func_name, xml_dict), level="INFO")
            return False

        xml_dict = self.xml.strip_xml_response(xml_dict, return_list=True)
        if options["return_mode"] != "FLAT_DICT":
            device.log(message="{} return value: {}".format(func_name, xml_dict), level="INFO")
            return xml_dict

        xml_dict = self.tool.set_element_list(xml_dict)
        all_entry_list = []
        for node_item in xml_dict:
            info = {}
            if "re-name" in node_item:
                info["re_name"] = node_item["re-name"]

            if "flow-pmi-statistics" not in node_item:
                continue

            pmi_entry_list = self.tool.set_element_list(node_item["flow-pmi-statistics"])
            for entry in pmi_entry_list:
                info.update(self.tool.flat_dict(
                    dict_variable=entry,
                    parent_key='',
                    separate_char='_',
                    lowercase=True,
                    replace_dash_to_underline=True,
                ))
                all_entry_list.append(copy.deepcopy(info))

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(all_entry_list)), level="INFO")
        return all_entry_list

    def verify_flow_session(self, device, **kwargs):
        r"""According to given option to check whether wanted session exists

        This method have dynamic options to filter device session one by one, and return True or False to indicate
        needed session whether exist. If option 'return_mode' set to 'counter', it will return matched session counter

        Pay attention:
            1. **If no any option given, it means sessions are all matched and return True**
            2. For INT/NUMBER compare, (100, "lt") means device counter less than 100
            3. For IP addr compare, ("192.168.100.0/24", "in") means IP addr in device must one of 192.168.100.1-254
            4. For STR compare, ("FPC0 PIC1", "in") means match "on FPC0 PIC1:" on device
            5. Any option=None means skip this option's checking. But if no other option given, it means all sessions
               are matched as well

        Each value of user option should be a STRING, INT, FLOAT, TUPLE or LIST. And you can use "-" or "~" for a range.
        For example, belows are all good in python:

        -   in_src_addr="192.168.10.1-254 in"       # IP range STRING
        -   in_dst_addr="100.1.1.1"                 # IP address STRING
        -   in_src_addr="192.168.1.0/24 in"         # Network STRING
        -   in_port="1024 ~ 65535 in"               # STRING that contain INT range
        -   in_port=69                              # Integer
        -   in_pkt_cnt=(1, "ge")                    # TUPLE contain check_value and check_action, same as STRING "1 ge"
        -   in_pkt_cnt=[10, "lt"]                   # LIST contain check_value and check_action, same as STRING "10 lt"
        -   in_interface="ge-0/0/1"                 # For STRING, default check_action is "IN", will match "ge-0/0/1" or
                                                    # "ge-0/0/1.0" both
        -   in_interface="ge-0/0/1 eq"              # STRING only match "ge-0/0/1" exactly

        Same options in robot file must be a STRING or INT without quotation mark such as " or '

        -   in_src_addr=192.168.10.1-254 in
        -   in_dst_addr=100.1.1.1
        -   in_src_addr=192.168.1.0/24 in
        -   in_port=1024 ~ 65535 in
        -   in_port=${69}
        -   in_pkt_cnt=1 ge
        -   in_pkt_cnt=10 lt
        -   in_interface=ge-0/0/1
        -   in_interface=ge-0/0/1 eq

        This method based on "fetch_flow_session", and it returns a flat list of sessions like below:

        [{
            "application_name": "junos-telnet",
            "application_traffic_control_rule_name": "INVALID",
            "application_traffic_control_rule_set_name": "INVALID",
            "application_value": "10",
            "configured_timeout": "1800",
            "duration": "35",
            "dynamic_application_name": "junos:UNKNOWN",
            "encryption_traffic_name": "Unknown",
            "flow_fpc_pic_id": "on FPC0 PIC2:",
            "in_byte_cnt": "1253",
            "in_conn_tag": "0x0",
            "in_dcp_session_id": "20001469",
            "in_destination_address": "100.0.1.2",
            "in_destination_port": "23",
            "in_dst_addr": "100.0.1.2",
            "in_dst_port": "23",
            "in_fin_sequence": "0",
            "in_fin_state": "0",
            "in_flag": "0x40001021",
            "in_gateway": "100.0.0.2",
            "in_interface": "xe-2/0/2.0",
            "in_interface_name": "xe-2/0/2.0",
            "in_pkt_cnt": "22",
            "in_port_sequence": "0",
            "in_protocol": "tcp",
            "in_route": "0xb0010",
            "in_seq_ack_diff": "0",
            "in_session_token": "0x600b",
            "in_source_address": "100.0.0.2",
            "in_source_port": "60437",
            "in_src_addr": "100.0.0.2",
            "in_src_port": "60437",
            "in_tunnel_information": "0",
            "logical_system": "",
            "nat_source_pool_name": "root_src_v4_pat",
            "out_byte_cnt": "1202",
            "out_conn_tag": "0x0",
            "out_dcp_session_id": "30001103",
            "out_destination_address": "30.0.1.1",
            "out_destination_port": "11181",
            "out_dst_addr": "30.0.1.1",
            "out_dst_port": "11181",
            "out_fin_sequence": "0",
            "out_fin_state": "0",
            "out_flag": "0x60001020",
            "out_gateway": "100.0.1.2",
            "out_interface": "xe-2/0/3.0",
            "out_interface_name": "xe-2/0/3.0",
            "out_pkt_cnt": "18",
            "out_port_sequence": "0",
            "out_protocol": "tcp",
            "out_route": "0x80010",
            "out_seq_ack_diff": "0",
            "out_session_token": "0x800c",
            "out_source_address": "100.0.1.2",
            "out_source_port": "23",
            "out_src_addr": "100.0.1.2",
            "out_src_port": "23",
            "out_tunnel_information": "0",
            "policy": "t_un/5",
            "sess_state": "Valid",
            "session_flag": "0x0/0x0/0x2008003",
            "session_identifier": "20001048",
            "session_mask": "0",
            "session_timeout": "1798",
            "start_time": "147472",
            "status": "Normal",
            "timeout": "1798",
            "wan_acceleration": ""
        },
        {...},
        ]

        All above sessions, **you can find any elements for specific session, these elements are all be an option**.
        In this method, given option value will be splited to a value and check_action automatically, and then checking
        value should be a STRING, INT, INT Range, Float, Float Range, IP, IP Range, Date or Date Range. If just a simple
        STRING without check_action characters, set check_action="IN", and others set check_action="EQ".

        Below are some examples for options:

        -   sess_state="Valid"          # match Valie or valid or any string that contain "valid"
        -   in_src_port="1024-65535 in" # match INT range

        :param INT|STR node:
            *OPTIONAL* HA testbed node name. node0 or node1, or just 0 or 1

        :param STR more_options:
            *OPTIONAL* Alias of "more_show_options" but have lower priority. default: None

        :param BOOL match_from_previous_response:
            *OPTIONAL* Every time this method get session from device and put result to cache. Set this option True to
                       verify session from cache. It will avoid run show command on device again. If no cache existing,
                       will get session from device automatically. default: False

        :param INT fetch_timeout:
            *OPTIONAL* Get session response timeout.

        :param STR return_mode:
            *OPTIONAL* As default just return True/False to indicate whether wanted session matched. Set 'counter' to
                       get how many sessions' matched all conditions

        :return: True/False, or return a integer if option 'return_mode' is 'counter'. Any issue will do raise

        :example:
            For Python

            status = search_flow_session(
                device=device,
                in_src_addr="{}-{} in".format(H0R0_IPV6_ADDR_LOWER, H0R0_IPV6_ADDR_HIGHER),
                in_dst_addr=H1R0_IPV6_ADDR + " eq",
                in_dst_port="2121 gt",
                in_protocol="tcp eq",
                out_src_addr=H1R0_IPV6_ADDR,
                out_dst_addr=H0R0_IPV6_ADDR,
            )

            For robot

            ${result}   search flow session
            ...             device=${r0}
            ...             in_src_addr=${H0R0_IPV6_ADDR_LOWER}-${H0R0_IPV6_ADDR_HIGHER} in
            ...             in_dst_addr=${H1R0_IPV6_ADDR} eq
            ...             in_dst_port=2121 eq
            ...             in_protocol=tcp
            ...             out_src_addr=${H1R0_IPV6_ADDR} eq
            ...             out_dst_addr=${H0R0_IPV6_ADDR} eq
            Run Keyword And Continue On Failure     Should Be True      ${result}       ${TRUE}

            Anyother robot example to mapping IP list pairs for scalling testing:


            # Fetch flow sessions to cache, and then match session from cache
            ${all_session_list}    flows.Fetch FLOW Session    device=${r0}    return_mode=FLAT_DICT

            @{in_src_addr_list}    Create List    192.168.10.10/32    192.168.10.20/32
            @{in_dst_addr_list}    Create List    192.168.20.10/32    192.168.20.20/32
            ${ip_pair_list}    Evaluate    zip(${in_src_addr_list}, ${in_dst_addr_list})
            :FOR    ${ip_pair}    IN    @{ip_pair_list}
            \    ${counter}    Verify FLOW Session
            \    ...    device=${r0}
            \    ...    return_mode=counter
            \    ...    match_from_previous_response=${True}            <<< search session from cache
            \    ...    in_src_addr=${ip_pair[0]}
            \    ...    in_dst_addr=${ip_pair[1]}
            \    ...    out_src_addr=${ip_pair[1]}
            \    ...    out_dst_addr=${ip_pair[0]}
            \    ...    in_protocol=tcp
            \    ...    sess_state=Valid
            \    ...    session_timeout=300-1800 in
            \    Should Be True    ${counter} >= ${1}

        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        # kwargs are mixed user filter options and function options. Remove funtion options here to cleanup user filters
        options = {}
        options["match_from_previous_response"] = kwargs.pop("match_from_previous_response", False)
        options["return_mode"] = kwargs.pop("return_mode", None)
        options["fetch_timeout"] = kwargs.pop("fetch_timeout", self.default["cli_show_timeout"])

        # For ticket https://engsupport.juniper.net/browse/TOBY-5532 to avoid if script have deprecated option "options"
        options["options"] = kwargs.pop("options", None)

        options["more_show_options"] = kwargs.pop("more_show_options", None)
        options["more_options"] = kwargs.pop("more_options", None)

        if options["options"] is not None:
            options["more_show_options"] = options["options"]

        if options["more_show_options"] is not None:
            options["more_options"] = options["more_show_options"]

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        dev_fingerprint = str(device)
        if dev_fingerprint not in self.runtime:
            self.runtime[dev_fingerprint] = {}

        if "flow_session_list" not in self.runtime[dev_fingerprint]:
            self.runtime[dev_fingerprint]["flow_session_list_mode"] = None
            self.runtime[dev_fingerprint]["flow_session_list"] = None

        if (options["match_from_previous_response"] is True
                and str(self.runtime[dev_fingerprint]["flow_session_list_mode"]).strip().upper() == "FLAT_DICT"
                and self.runtime[dev_fingerprint]["flow_session_list"] is not None):
            all_session_list = self.runtime[dev_fingerprint]["flow_session_list"]
        else:
            all_session_list = self.fetch_flow_session(
                device=device,
                options=options["more_options"],
                timeout=options["fetch_timeout"],
                return_mode="flat_dict",
            )
            self.runtime[dev_fingerprint]["flow_session_list"] = copy.deepcopy(all_session_list)

        compat_element_list = (
            # compatible_keyword, session_keyword
            ("session_id", "session_identifier"),
            ("session_timeout", "timeout"),
            ("node", "re_name"),
            ("in_src_addr", "in_source_address"),
            ("in_dst_addr", "in_destination_address"),
            ("in_src_port", "in_source_port"),
            ("in_dst_port", "in_destination_port"),
            ("in_interface", "in_interface_name"),
            ("out_src_addr", "out_source_address"),
            ("out_dst_addr", "out_destination_address"),
            ("out_src_port", "out_source_port"),
            ("out_dst_port", "out_destination_port"),
            ("out_interface", "out_interface_name"),
            ("resource_manager_client_name", "resource_manager_information_client_name"),
            ("resource_manager_group_identifier", "resource_manager_information_group_identifier"),
            ("resource_manager_resource_identifier", "resource_manager_information_resource_identifier"),
        )

        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            compat_element_list=compat_element_list,
            filters=filters,
            entries=all_session_list,
            index_option="session_identifier",
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_session_list,
            index_option="session_identifier",
            debug_to_stdout=self.debug_to_stdout,
        )
        return_value = len(matched_session_list) if options["return_mode"] == "counter" else bool(matched_session_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value


    def verify_flow_cp_session(self, device, **kwargs):
        r"""According to given options to find specific flow cp session

        This method based on "fetch_flow_cp_session". From base method, it will return LIST of sessions. This method
        loops sessions and check whether matching all given options.

        Here is an example that returns by fetch_flow_cp_session:

        [
            {
                "dcp_flow_fpc_pic_id": "on FPC0 PIC0:",
                "displayed_session_count": "0",
                "re_name": "node0"
            },
            {
                "dcp_flow_fpc_pic_id": "on FPC0 PIC0:",
                "displayed_session_count": "0",
                "re_name": "node1"
            },
            {
                "application_name": "",
                "application_value": "0",
                "configured_timeout": "0",
                "dcp_flow_fpc_pic_id": "on FPC0 PIC1:",
                "displayed_session_count": "1",
                "duration": "0",
                "dynamic_application_name": "INVALID",
                "in_byte_cnt": "0",
                "in_conn_tag": "0x0",
                "in_destination_address": "0.0.0.0",
                "in_destination_port": "0",
                "in_fin_sequence": "0",
                "in_fin_state": "0",
                "in_flag": "0x0",
                "in_gateway": "0.0.0.0",
                "in_interface_name": "",
                "in_pkt_cnt": "0",
                "in_port_sequence": "0",
                "in_protocol": "0",
                "in_route": "0x0",
                "in_seq_ack_diff": "0",
                "in_session_token": "0x0",
                "in_source_address": "0.0.0.0",
                "in_source_port": "0",
                "in_tunnel_information": "0",
                "logical_system": "",
                "nat_source_pool_name": "",
                "out_byte_cnt": "0",
                "out_conn_tag": "0x0",
                "out_destination_address": "121.11.15.11",
                "out_destination_port": "1135",
                "out_fin_sequence": "0",
                "out_fin_state": "0",
                "out_flag": "0x0",
                "out_gateway": "0.0.0.0",
                "out_interface_name": "",
                "out_pkt_cnt": "0",
                "out_port_sequence": "0",
                "out_protocol": "icmp",
                "out_route": "0x0",
                "out_seq_ack_diff": "0",
                "out_session_token": "0x0",
                "out_source_address": "121.11.20.2",
                "out_source_port": "47629",
                "out_tunnel_information": "0",
                "policy": "",
                "re_name": "node1",
                "sess_state": "Valid",
                "session_flag": "0x180000",
                "session_identifier": "10040149",
                "session_mask": "0",
                "session_spu_id": "3",
                "start_time": "0",
                "status": "",
                "timeout": "0",
                "wan_acceleration": ""
            }
        ]

        Every DICT keyword in above should be an option for this method. For more detail, pls see doc from
        "verify_flow_session"

        :param STR more_options:
            *OPTIONAL* option string will tailed to "show security flow cp-session" command. default: None

                       Notice: use keyword "fetch_flow_cp_session_summary" instead add "summary" in this method,
                       "cp-session summary" have different xml structure cause issue.

        :param INT|STR node:
            *OPTIONAL* node number or string. default: None

        :param STR return_mode:
            *OPTIONAL* As default this method just return True/False means whether match session. set 'counter' to get
                       how many sessions matched

        :param BOOL match_from_previous_response:
            *OPTIONAL* If set True, match based on last fetch. default: False

        :param INT timeout:
            *OPTIONAL* Timeout to get response. default: 300

        :return:
            If option "return_mode" == "counter", return matched session counter. other wise return True/False

        :example:
            For robot

            ${status}    Verify FLOW CP Session
            ...    device=${r0}
            ...    node=1
            ...    dcp_flow_fpc_pic_id=FPC1 in
            ...    in_src_addr=192.168.1.1-20 in
            Should Be True    ${status}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["match_from_previous_response"] = self.tool.check_boolean(kwargs.pop("match_from_previous_response", False))
        options["return_mode"] = kwargs.pop("return_mode", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_show_timeout"]))
        options["more_options"] = kwargs.pop("more_options", None)
        options["node"] = kwargs.get("node", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        dev_fingerprint = str(device)
        if dev_fingerprint not in self.runtime:
            self.runtime[dev_fingerprint] = {}

        if "flow_cp_session_list" not in self.runtime[dev_fingerprint]:
            self.runtime[dev_fingerprint]["flow_cp_session_list"] = None

        if options["match_from_previous_response"] is True and self.runtime[dev_fingerprint]["flow_cp_session_list"] is not None:
            all_session_list = self.runtime[dev_fingerprint]["flow_cp_session_list"]
        else:
            all_session_list = self.fetch_flow_cp_session(
                device=device,
                options=options["more_options"],
                node=options["node"],
                timeout=options["timeout"],
            )
            self.runtime[dev_fingerprint]["flow_cp_session_list"] = copy.deepcopy(all_session_list)

        if all_session_list is False:
            return_value = 0 if options["return_mode"] == "counter" else False
            device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
            return return_value

        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=all_session_list,
            index_option="session_identifier",
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_session_list,
            index_option="session_identifier",
            debug_to_stdout=self.debug_to_stdout,
        )
        return_value = len(matched_session_list) if options["return_mode"] == "counter" else bool(matched_session_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def verify_flow_cp_session_summary(self, device, **kwargs):
        r"""According to given options to find specific flow cp session summary entry

        This method based on "fetch_flow_cp_session_summary". From base method, it will return a LIST and every element
        is a cp session summary entry. The method will loop summary list and check whether the summary entry matching
        all given options. For more detail, please refer "fetch_flow_cp_session_summary"

        Here is an summary example:

        [
            {
                "dcp_flow_fpc_pic_id": "on FPC0 PIC0:",
                "displayed_session_count": "0",
                "displayed_session_invalidated": "0",
                "displayed_session_other": "0",
                "displayed_session_pending": "0",
                "displayed_session_valid": "0"
            },
            {
                "dcp_flow_fpc_pic_id": "on FPC0 PIC1:",
                "displayed_session_count": "0",
                "displayed_session_invalidated": "0",
                "displayed_session_other": "0",
                "displayed_session_pending": "0",
                "displayed_session_valid": "0",
                "max_inet6_session_count": "7549747",
                "max_session_count": "7549747"
            },
        ]

        All keyword in above DICT should be an option

        :param STR more_options:
            *OPTIONAL* option string will tailed to "show security flow cp-session" command. default: None

                       Notice: use keyword "search_flow_cp_session_summary" instead add "summary" in this method, "cp-session summary" have
                       different xml structure cause issue.

        :param INT|STR node:
            *OPTIONAL* node number or string. default: None

        :param BOOL total_all_fpcs:
            *OPTIONAL* Get total value from all FPCs on HE platform. default: None

        :param STR return_mode:
            *OPTIONAL* As default this method just return True/False means whether match a rule, but you can set 'counter' to return how
                       many rule matched

        :param INT timeout:
            *OPTIONAL* Timeout to get response. default: 300

        :return:
            If option "return_mode" == "counter", return matched session counter. other wise return True/False

        :example:
            For robot

            ${status}    flows.Verify FLOW CP Session Summary
            ...    device=${r0}
            ...    total_all_fpcs=True
            ...    displayed_session_valid=10 ge
            ...    displayed_session_invalidated=0 eq
            Should Be True    ${status}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        base_method_options = {}
        base_method_options["device"] = device
        base_method_options["timeout"] = kwargs.pop("timeout", None)
        base_method_options["more_options"] = kwargs.pop("more_options", None)
        base_method_options["total_all_fpcs"] = kwargs.pop("total_all_fpcs", None)
        base_method_options["node"] = kwargs.get("node", None)

        options = {}
        options["return_mode"] = kwargs.pop("return_mode", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        base_method_options = self.tool.dict_cleanup(base_method_options, delete_value=None)
        all_session_list = self.fetch_flow_cp_session_summary(**base_method_options)
        if all_session_list is False:
            return_value = 0 if options["return_mode"] == "counter" else False
            device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
            return return_value

        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=all_session_list,
            index_option="session_identifier",
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_session_list,
            index_option="session_identifier",
            debug_to_stdout=self.debug_to_stdout,
        )
        return_value = len(matched_session_list) if options["return_mode"] == "counter" else bool(matched_session_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def verify_flow_status(self, device, **kwargs):
        r"""By given option to check flow module's working status

        This method obey the rule from verify_flow_session method, please see detail from there.

        As default, checking mode is "exact" means given args match exactly string. But please pay
        attention: **string checking is case insensitive**

        :param STR forwarding_mode_inet:
            *OPTIONAL* To check flow engine run mode for IPv4. Default: None

        :param STR forwarding_mode_inet6:
            *OPTIONAL* To check flow engine run mode for IPv6. Default: None

        :param STR forwarding_mode_mpls:
            *OPTIONAL* To check flow engine run mode for MPLS. Default: None

        :param STR forwarding_mode_iso:
            *OPTIONAL* To check flow engine run mode for ISO. Default: None

        :param STR ipsec_performance_acceleration_ipa_status:
            *OPTIONAL* To check ipa_mode for ipsec performance acceleration engine. Default: None

        :param STR flow_packet_ordering_mode:
            *OPTIONAL* To check flow packet ordering mode. Default: None

        :param STR session_distribution_gtpu_distr_status:
            *OPTIONAL* To check "GTP-U distribution". Default: None

        :param STR session_distribution_mode:
            *OPTIONAL* To check session distribution mode. Default: None

        :param STR flow_trace_option:
            *OPTIONAL* To check flow trace options. Default: None

        :param STR flow_trace_status:
            *OPTIONAL* To check flow trace status. Default: None

        :param STR tap_mode:
            *OPTIONAL* To check flow tap mode. Default: None

        :param STR enhanced_services_mode:
            *OPTIONAL* To check flow enhanced services mode. Default: None

        :param STR node:
            *OPTIONAL* For HA device to get specific node's status. Default: None

                       Must one of 0, 1 or None

        :param INT check_cnt:
            *OPTIONAL* Low-end device may need waiting a while to show flow status. This parameter indicate how many
                       times try to get status result if got error msg. Default: 1

        :param INT|FLOAT check_interval:
            *OPTIONAL* With option "check_cnt" to set sleep interval. Default: 10

        :param int timeout:
            *OPTIONAL* Timeout to get status from device

        :return:
            Return True if all option matched, otherwise return False.
            If no any option given, return True.
            If keyword given but device don't have, return False.

        :example:
            For robot

            :FOR    ${index}    IN RANGE    1    5
            \    BuiltIn.Log    checking flow status '${index}' time...
            \    ${status}    flows.Verify FLOW Status
            \    ...    device=${r0}
            \    ...    forwarding_mode_inet=flow base
            \    ...    forwarding_mode_inet6=flow base
            \    Exit For Loop If    ${status} is ${True}
            \    BuiltIn.Sleep    10    waiting for next FLOW status checking...
            Should Be True    ${status}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["timeout"] = kwargs.pop("timeout", self.default['cli_show_timeout'])
        options["check_cnt"] = int(kwargs.pop("check_cnt", 1))
        options["check_interval"] = float(kwargs.pop("check_interval", 10))
        options["node"] = kwargs.get("node", None)

        # deprecated
        options["check_mode"] = kwargs.pop("check_mode", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        err_msg = ""
        for index in range(options["check_cnt"]):
            xml_dict = self.fetch_flow_status(
                device=device,
                node=options["node"],
                timeout=options["timeout"],
                return_mode="flat_dict",
            )
            # accident happened
            if xml_dict is False:
                err_msg = "get flow status failed."
            elif "error_message" in xml_dict:
                err_msg = xml_dict["error_message"]
                if "error_source_daemon" in xml_dict:
                    err_msg = "{}: {}".format(xml_dict["error_source_daemon"], err_msg)
            else:
                err_msg = ""
                break

            device.log(message="{}: {}".format(index, err_msg), level="WARN")
            self.tool.sleep(secs=options["check_interval"], msg="get next flow status...")

        if err_msg:
            device.log(message="{} return value: False".format(func_name), level="INFO")
            return False

        compat_element_list = (
            ("enhanced_routing_mode", "flow_status_all_flow_forwarding_mode_flow_enhanced_routing_mode"),
            ("forwarding_mode_inet", "flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet"),
            ("forwarding_mode_inet6", "flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet6"),
            ("forwarding_mode_mpls", "flow_status_all_flow_forwarding_mode_flow_forwarding_mode_mpls"),
            ("forwarding_mode_iso", "flow_status_all_flow_forwarding_mode_flow_forwarding_mode_iso"),
            ("tap_mode", "flow_status_all_flow_forwarding_mode_flow_tap_mode"),
            ("enhanced_services_mode", "flow_status_all_flow_forwarding_mode_flow_enhanced_services_mode"),
            ("ipsec_performance_acceleration_ipa_status", "flow_status_all_flow_ipsec_performance_acceleration_ipa_status"),
            ("flow_packet_ordering_mode", "flow_status_all_flow_packet_ordering_ordering_mode"),
            ("session_distribution_gtpu_distr_status", "flow_status_all_flow_session_distribution_gtpu_distr_status"),
            ("session_distribution_mode", "flow_status_all_flow_session_distribution_mode"),
            ("flow_trace_status", "flow_status_all_flow_trace_option_flow_trace_status"),
            ("flow_trace_option", "flow_status_all_flow_trace_option_flow_trace_options"),
            ("pmi_status", "flow_status_all_flow_power_mode_ipsec_pmi_status"),
        )

        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            compat_element_list=compat_element_list,
            filters=filters,
            entries=[xml_dict, ],
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_session_list,
            max_column_width=80,
            debug_to_stdout=self.debug_to_stdout,
        )

        return_value = bool(matched_session_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value


    def verify_flow_statistics(self, device, **kwargs):
        r"""According args to check flow statistics

        This method based on method "fetch_flow_statistics", all args in base method can be used properly.
        Notice: In fetch_flow_statistics have all base args.

        For HE device, you may get text output like below:

        ```
          Flow Statistics of FPC0 PIC1:
            Current sessions: 5
            Packets forwarded: 596
            Packets dropped: 0
            Fragment packets: 0

          Flow Statistics of FPC0 PIC2:
            Current sessions: 5
            Packets forwarded: 601
            Packets dropped: 1
            Fragment packets: 0

          Flow Statistics of FPC0 PIC3:
            Current sessions: 4
            Packets forwarded: 219
            Packets dropped: 0
            Fragment packets: 0

          Flow Statistics Summary:
            System total valid sessions: 14
            Packets forwarded: 1416
            Packets dropped: 1
            Fragment packets: 0
        ```

        But unfortunately, we always use XML response to check above output. This means args in this
        method based on XML keyword.

        Like "verify_flow_session" method, you should use keyword "eq", "lt", "gt", etc... to check
        each args. Please see "verify_flow_session" for detail.

        Below are all args and XML keyword mapping:

        :param str flow_spu_id:
            *OPTIONAL* Only occurred on HighEnd device like "FPC0 PIC1". As default, it always do
                       case insensitive check that means "fpc0 pic1" will match
                       "Flow Statistics of FPC0 PIC1".
                       Default: None

        :param int flow_session_count_valid:
            *OPTIONAL* checking "Current sessions" counter.

                       if option "flow_spu_id" is "summary", will checking
                       "System total valid sessions" counter.

                       Default: None

        :param int flow_pkt_count_fwd:
            *OPTIONAL* checking "Packets forwarded" counter. Default: None

        :param int flow_pkt_count_drop:
            *OPTIONAL* checking "Packets dropped" counter. Default: None

        :param int flow_frag_count_fwd:
            *OPTIONAL* checking "Fragment packets" counter. Default: None

        :param INT flow_pkt_count_rx:
            *OPTIONAL* checking "Packets received" counter. Default: None

        :param INT flow_pkt_count_tx:
            *OPTIONAL* checking "Packets transmitted" counter. Default: None

        :param INT flow_pkt_count_copy:
            *OPTIONAL* checking "Packets copied" counter. Default: None

        :param INT flow_llf_pkt_count_prd:
            *OPTIONAL* checking "Services-offload packets processed" counter. Default: None

        :param int node:
            *OPTIONAL* 0 or 1. Default: None

        :param int timeout:
            *OPTIONAL* checking timeout.

        :return:
            Return True/False to indicate checking status. Or raise the issue.

        :example:
            For Python

            # LowEnd platform. Do not set option "flow_spu_id" because it only occrred on HighEnd
            status = verify_flow_statistics(
                device=dev_handler,
                flow_session_count_valid=(100, "gt"),
                flow_pkt_count_drop=("0 equal"),
            )

            # HighEnd platform checking PIC counter
            status = verify_flow_statistics(
                device=dev_handler,
                flow_spu_id="FPC2",
                flow_session_count_valid=(100, "gt"),
                flow_pkt_count_drop=("0 equal"),
                flow_pkt_count_fwd="100 gt",
                flow_frag_count_fwd=0,
            )

            # checking summary counter
            status = verify_flow_statistics(
                device=dev_handler,
                flow_spu_id="SUMMARY",
                flow_session_count_valid=(100, "gt"),
                flow_pkt_count_drop=("0 equal"),
                flow_pkt_count_fwd="100 gt",
                flow_frag_count_fwd=0,
            )

            For robot

            ${status}    flows.Verify FLOW Statistics
            ...    device=${r0}
            ...    flow_spu_id=summary in
            ...    flow_session_count_valid=10 gt
            ...    flow_pkt_count_drop=0
            ...    flow_pkt_count_fwd=100 gt
            ...    flow_frag_count_fwd=0
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["timeout"] = kwargs.pop("timeout", self.default['cli_show_timeout'])
        options["node"] = kwargs.get("node", None)

        if options["node"] is not None:
            options["node"] = self.tool.get_node_value(options["node"], mode="INT")

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        all_session_list = self.fetch_flow_statistics(
            device=device,
            node=options["node"],
            timeout=options["timeout"],
            return_mode="flat_dict",
        )
        if all_session_list is False:
            raise RuntimeError("Get flow statistics response failed.")

        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=all_session_list,
            index_option="session_identifier",
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(device=device, filters=filters, entries=matched_session_list, debug_to_stdout=self.debug_to_stdout)
        device.log(message="{} return value: {}".format(func_name, bool(matched_session_list)), level="INFO")
        return bool(matched_session_list)


    def verify_flow_gate(self, device, **kwargs):
        r"""Use dynamic options to filter all FLOW gate entries.

        This method invoke method "fetch_flow_gate" and filter all entries by various options.

        Here is an return example from fetch_flow_gate. All keywords in DICT should be an option:

        [
            {
                "displayed_gate_count": "0",
                "displayed_gate_invalidated": "0",
                "displayed_gate_other": "0",
                "displayed_gate_pending": "0",
                "displayed_gate_valid": "0",
                "flow_gate_fpc_pic_id": "on FPC2 PIC0:",
                "re_name": "node0"
            },
            {
                "displayed_gate_count": "0",
                "displayed_gate_invalidated": "0",
                "displayed_gate_other": "0",
                "displayed_gate_pending": "0",
                "displayed_gate_valid": "0",
                "flow_gate_fpc_pic_id": "on FPC2 PIC1:",
                "re_name": "node0"
            },
        ]

        :param STR more_options:
            *OPTIONAL* Command string will be tailed to base command "show security flow gate". default: None

        :param STR node:
            *OPTIONAL* For HA device to get specific node's result. default: None

        :param INT timeout:
            *OPTIONAL* Timeout to get result from device.

        :param BOOL match_from_previous_response:
            *OPTIONAL* Fetch flow gate entries from runtime cache. default: False

        :return:
            Return True if all option matched, otherwise return False.
            If no any option given, return True.
            If keyword given but device don't have, return False.

        :example:
            For robot

            ${status}    flows.Verify FLOW Gate
            ...    device=${r0}
            ...    re_name=node0
            ...    flow_gate_fpc_pic_id=PIC1 in
            ...    displayed_gate_valid=1000 ge
            ...    displayed_gate_count=1000 gt
            Should Be True    ${status}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["more_options"] = kwargs.pop("more_options", None)
        options["node"] = kwargs.pop("node", None)
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_show_timeout"]))
        options["match_from_previous_response"] = self.tool.check_boolean(kwargs.pop("match_from_previous_response", False))

        if options["node"] is not None:
            options["node"] = self.tool.get_node_value(options["node"], mode="INT")

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        dev_fingerprint = str(device)
        if dev_fingerprint not in self.runtime:
            self.runtime[dev_fingerprint] = {}

        if "flow_gate_list" not in self.runtime[dev_fingerprint]:
            self.runtime[dev_fingerprint]["flow_gate_list"] = list()

        if options["match_from_previous_response"] is True and self.runtime[dev_fingerprint]["flow_gate_list"]: # pragma: no cover
            all_session_list = self.runtime[dev_fingerprint]["flow_gate_list"]
        else:
            all_session_list = self.fetch_flow_gate(
                device=device,
                more_options=options["more_options"],
                timeout=options["timeout"],
                return_mode="flat_dict",
            )
            self.runtime[dev_fingerprint]["flow_gate_list"] = copy.deepcopy(all_session_list)

        if all_session_list is False:
            raise RuntimeError("Fetch FLOW gate information failed")

        compat_element_list = (
            ("fpc_pic_id", "flow_gate_fpc_pic_id"),
        )

        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            compat_element_list=compat_element_list,
            filters=filters,
            entries=all_session_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(device=device, filters=filters, entries=matched_session_list, debug_to_stdout=self.debug_to_stdout)
        device.log(message="{} return value: {}".format(func_name, bool(matched_session_list)), level="INFO")
        return bool(matched_session_list)


    def verify_flow_session_summary(self, device, **kwargs):
        r"""Based on method "fetch_flow_session_summary" to check element

        This method based on "fetch_flow_session_summary". From base method, it will return a LIST and every element
        is a flow session summary entry. The method will loop summary list and check whether the summary entry matching
        all given options. For more detail, please refer "fetch_flow_session_summary"

        Here is an example of fetch_flow_session_summary. All keyword in DICT should be an option:

        [
            {
                "active_multicast_sessions": "0",
                "active_services_offload_sessions": "0",
                "active_session_invalidated": "0",
                "active_session_other": "0",
                "active_session_pending": "0",
                "active_session_valid": "0",
                "active_sessions": "0",
                "active_unicast_sessions": "0",
                "failed_sessions": "0",
                "max_sessions": "6291456",
                "re_name": "node0"
            },
            {
                "active_multicast_sessions": "0",
                "active_services_offload_sessions": "0",
                "active_session_invalidated": "1",
                "active_session_other": "0",
                "active_session_pending": "0",
                "active_session_valid": "0",
                "active_sessions": "1",
                "active_unicast_sessions": "0",
                "failed_sessions": "0",
                "max_sessions": "6291456",
                "re_name": "node1"
            },
            ......
        ]

        :param STR more_options:
            *OPTIONAL* extensive options will tailed to basic cmd, detail pls see "fetch_flow_session_summary" method.
                       default: None

        :param INT|STR node:
            *OPTIONAL* node number or name. default: None

        :param INT timeout:
            *OPTIONAL* get response timeout. default: 300

        :param BOOL total_all_fpcs:
            *OPTIONAL* Get total value from all FPCs on HE platform. default: None

        :param STR return_mode:
            *OPTIONAL* default return True/False to indicate all filters matched, but you can set 'counter' to return
                       match counter

        :return:
            See option "return_mode"

        :example:
            For Python

            status = verify_flow_session_summary(
                device=r0,
                re_name="node0",
                active_session_valid=("1-10", "in"),
                flow_fpc_pic_id=("FPC0 PIC0", "in"),
            )

            For robot

            ${status}    flows.Verify FLOW Session Summary
            ...    device=${r0}
            ...    re_name=node0
            ...    active_session_valid=1-10 in
            ...    flow_fpc_pic_id=FPC0 PIC0 in
            Should Be True    ${status}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        base_method_options = {}
        base_method_options["device"] = device
        base_method_options["timeout"] = kwargs.pop("timeout", None)
        base_method_options["more_options"] = kwargs.pop("more_options", None)
        base_method_options["total_all_fpcs"] = self.tool.check_boolean(kwargs.pop("total_all_fpcs", None))
        base_method_options["node"] = kwargs.get("node", None)

        options = {}
        options["return_mode"] = kwargs.pop("return_mode", None)

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        base_method_options = self.tool.dict_cleanup(base_method_options, delete_value=None)
        all_session_list = self.fetch_flow_session_summary(**base_method_options)
        if all_session_list is False:
            device.log(message="No response from device", level="WARN")
            device.log(message="{} return value: False".format(func_name), level="INFO")
            return False

        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=all_session_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(device=device, filters=filters, entries=matched_session_list, debug_to_stdout=self.debug_to_stdout)
        return_value = len(matched_session_list) if options["return_mode"] == "counter" else bool(matched_session_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def operation_delete_flow_configuration(self, device, **kwargs):
        """delete flow configuration based on cmd 'delete security flow'

        As default, this method will send "delete security flow" to delete all flow related
        configuration. But you can use "options" to do more exactly deletion like below:

            options = (
                "advanced-options drop-matching-link-local-address",
                "aging",
                "tcp-mss all-tcp",
            )

        Above options will send these cmds to DUT:
            ("delete security flow advanced-options drop-matching-link-local-address",
             "delete security flow aging",
             "delete security flow tcp-mss all-tcp")

        :param STR|LIST options:
            *OPTIONAL* a STR or LIST that contain sub configuration you want to delete.

        :param STR more_options:
            *OPTIONAL* alias for "options" but have higher priority. default: None

        :param INT timeout:
            *OPTIONAL* timeout to send cmd.

        :param BOOL return_cmd:
            *OPTIONAL* For unit test. Set True to return send cmds

        :return:
            Always return True or raise ValueError

        :example:
            For robot

            flows.Operation Delete FLOW Configuration    device=${r0}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["options"] = kwargs.pop("options", None)
        options["more_options"] = kwargs.pop("more_options", None)
        options["timeout"] = kwargs.pop("timeout", self.default['cli_show_timeout'])
        options["return_cmd"] = kwargs.pop("return_cmd", None)

        if options["options"] is not None:
            options["more_options"] = options["options"]

        cmd_list = ["delete security flow", ]
        if isinstance(options["more_options"], (list, tuple)):
            cmd_list.extend(options["more_options"])

        elif isinstance(options["more_options"], str):
            cmd_list.append(options["more_options"])

        else:
            raise ValueError("'options' must be STR, LIST or TUPLE, not '{}'".format(options["more_options"]))

        cmd = " ".join(cmd_list)
        response = dev.execute_config_command_on_device(
            device=device,
            command=cmd,
            format="xml",
            channel="pyez",
            timeout=options["timeout"],
        )
        if options["return_cmd"] is True:
            response = cmd

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(response)), level="INFO")
        return response

    def execute_clear_flow_session(self, device, **kwargs):
        """clear flow session based on cmd 'clear security flow session'

        :param BOOL all:
            *OPTIONAL* delete all flow sessions. Default: None

        :param BOOL advanced_anti_malware:
            *OPTIONAL* send cmd "clear security flow session advanced-anti-malware". Default: None

        :param BOOL application_firewall:
            *OPTIONAL* send cmd "clear security flow session application-firewall". Default: None

        :param BOOL application_traffic_control:
            *OPTIONAL* send cmd "clear security flow session application-traffic-control".
                       Default: None

        :param BOOL idp:
            *OPTIONAL* send cmd "clear security flow session idp". Default: None

        :param BOOL nat:
            *OPTIONAL* send cmd "clear security flow session nat". Default: None

        :param BOOL resource_manager:
            *OPTIONAL* send cmd "clear security flow session resource-manager". Default: None

        :param BOOL security_intelligence:
            *OPTIONAL* send cmd "clear security flow session security-intelligence". Default: None

        :param BOOL tunnel:
            *OPTIONAL* send cmd "clear security flow session tunnel". Default: None

        :param STR application:
            *OPTIONAL* send cmd "clear security flow session application <value>". Default: None

        :param INT conn_tag:
            *OPTIONAL* send cmd "clear security flow session conn-tag <value>". Default: None

        :param INT source_port || destination_port:
            *OPTIONAL* send cmd "clear security flow session source-port| destination-port <value>"
                       Default: None

        :param INT session_identifier:
            *OPTIONAL* send cmd "clear security flow session session-identifier <value>".
                       Default: None

        :param IP/Network source_prefix || destination_prefix:
            *OPTIONAL* send cmd "clear security flow session source-prefix| destination-prefix val"
                       Default: None

        :param STR family:
            *OPTIONAL* send cmd "clear security flow session family <value>". Default: None

        :param STR interface:
            *OPTIONAL* send cmd "clear security flow session interface <int_name>". Default: None

        :param INT/STR protocol:
            *OPTIONAL* send cmd "clear security flow session protocol <value>". Default: None

        :param INT/STR node:
            *OPTIONAL* send cmd to specific HA node. Default: None

        :param INT timeout:
            *OPTIONAL* timeout to send cmd.

        :param INT/FLOAT sleep:
            *OPTIONAL* sleep secondary after clear. default: 0

        :param BOOL return_cmd:
            *OPTIONAL* For unit test. Set True to return send cmds

        :return:
            Always return True or raise ValueError

        :example:
            flows.Execute Clear FLOW Session    device=${r0}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))
        options["return_cmd"] = self.tool.check_boolean(kwargs.pop("return_cmd", None))
        options["node"] = kwargs.pop("node", None)
        options["sleep"] = float(kwargs.pop("sleep", 0))

        all_user_option_list = (
            # (value_type, keyword)
            ("BOOL", "all"),
            ("BOOL", "advanced_anti_malware"),
            ("BOOL", "application_firewall"),
            ("BOOL", "application_traffic_control"),
            ("BOOL", "idp"),
            ("BOOL", "nat"),
            ("BOOL", "resource_manager"),
            ("BOOL", "security_intelligence"),
            ("BOOL", "tunnel"),
            ("STR", "application"),
            ("INT", "conn_tag"),
            ("INT", "source_port"),
            ("INT", "destination_port"),
            ("INT", "session_identifier"),
            ("IP", "source_prefix"),
            ("IP", "destination_prefix"),
            ("STR", "family"),
            ("STR", "interface"),
            ("INT", "protocol"),
        )

        for value_type, keyword in all_user_option_list:
            options[keyword] = kwargs.pop(keyword, None)

        base_cmd = "clear security flow session"
        if options["node"] is not None:
            base_cmd += " node {}".format(options["node"])

        cmd_list = []
        for value_type, keyword in all_user_option_list:
            if options[keyword] is None:
                continue

            device_keyword = keyword.replace("_", "-")
            if value_type == "BOOL" and self.tool.check_boolean(options[keyword]) is True:
                cmd_list.append(base_cmd + " " + device_keyword)
            else:
                cmd_list.append(base_cmd + " {} {}".format(device_keyword, options[keyword]))

        # no option given will clear all session
        if not cmd_list:
            cmd_list.append(base_cmd)

        response = dev.execute_cli_command_on_device(
            device=device,
            command=cmd_list,
            format="text",
            channel="pyez",
            timeout=options["timeout"],
        )
        time.sleep(options["sleep"])

        if options["return_cmd"] is True:
            response = cmd_list

        device.log(message="{} return value:\n{}".format(func_name, self.tool.pprint(response)), level="INFO")
        return response

    def execute_clear_flow_ip_action(self, device, **kwargs):
        """clear flow ip-action entry based on cmd 'clear security flow ip-action'

        :param BOOL all:
            *OPTIONAL* delete all flow ip-action entries. Default: None

        :param INT source_port || destination_port:
            *OPTIONAL* send cmd "clear security flow ip-action source-port|destination-port <value>"
                       Default: None

        :param IP/Network source_prefix || destination_prefix:
            *OPTIONAL* send cmd "clear security flow ip-action source-prefix|destination-prefix val"
                       Default: None

        :param STR family:
            *OPTIONAL* send cmd "clear security flow ip-action family <value>". Default: None

        :param INT/STR protocol:
            *OPTIONAL* send cmd "clear security flow ip-action protocol <value>". Default: None

        :param INT timeout:
            *OPTIONAL* timeout to send cmd.

        :param INT/FLOAT sleep:
            *OPTIONAL* sleep secondary after clear. default: 0

        :return:
            Return device response or raise ValueError

        :example:
            For robot

            flows.Execute Clear FLOW IP Action    device=${r0}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["timeout"] = int(kwargs.pop("timeout", self.default['cli_show_timeout']))
        options["return_cmd"] = kwargs.pop("return_cmd", None)
        options["sleep"] = float(kwargs.pop("sleep", 0))

        all_user_option_list = (
            # (value_type, keyword)
            ("BOOL", "all"),
            ("INT", "source_port"),
            ("INT", "destination_port"),
            ("IP", "source_prefix"),
            ("IP", "destination_prefix"),
            ("STR", "family"),
            ("INT", "protocol"),
        )

        for value_type, keyword in all_user_option_list:
            options[keyword] = kwargs.pop(keyword, None)

        base_cmd = "clear security flow ip-action"

        cmd_list = []
        for value_type, keyword in all_user_option_list:
            if options[keyword] is None:
                continue

            device_keyword = keyword.replace("_", "-")
            if value_type == "BOOL" and self.tool.check_boolean(options[keyword]) is True:
                cmd_list.append(base_cmd + " " + device_keyword)
            else:
                cmd_list.append(base_cmd + " {} {}".format(device_keyword, options[keyword]))

        # no option given will clear all session
        if not cmd_list:
            cmd_list.append(base_cmd)

        response = dev.execute_cli_command_on_device(
            device=device,
            command=cmd_list,
            format="text",
            channel="pyez",
            timeout=options["timeout"],
        )
        time.sleep(options["sleep"])

        device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
        return response

    def execute_clear_flow_statistics(self, device, **kwargs):
        """clear flow statistics counter based on cmd 'clear security flow statistics'

        :param STR more_options:
            *OPTIONAL* concatenate to base command. default: None

        :param INT timeout:
            *OPTIONAL* timeout to send cmd.

        :param BOOL return_cmd:
            *OPTIONAL* For unit test. Set True to return send cmds

        :param INT/FLOAT sleep:
            *OPTIONAL* sleep secondary after clear. default: 0

        :return:
            Always return True or raise ValueError

        :example:
            For robot

            flows.Execute Clean FLOW Statistics    device=${r0}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["more_options"] = kwargs.pop("more_options", None)
        options["timeout"] = kwargs.pop("timeout", self.default['cli_show_timeout'])
        options["return_cmd"] = kwargs.pop("return_cmd", None)
        options["sleep"] = float(kwargs.pop("sleep", 0))

        cmd = "clear security flow statistics"
        if options["more_options"] is not None:
            cmd += " {}".format(options["more_options"])

        response = dev.execute_cli_command_on_device(
            device=device,
            command=cmd,
            format="text",
            channel="text",
            timeout=options["timeout"],
        )
        time.sleep(options["sleep"])
        if options["return_cmd"] is True:
            response = cmd

        device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
        return response

    #Function to Get flow sessions wing per thread affinity anchored on all the threads in PIC where IPSEC is anchored
    #------------------------------------------------------------------------------------------------------------------
    def fetch_wing_per_thread(self, device, destination=None):
        r"""Fetch flow sessions wing per thread affinity anchored on all the threads
        :param device:
            **REQUIRED** device object

        :param destination:
    	    **REQUIRED**  tunnel anchored pic

        :return: flow sessions distributed on all the threads where tunnel is active
                 with PMI enabled.

        :example:
            For Python

            get_wing_per_thread(rh, 'fpc0.pic0')

            For robot

            Get Wing Per Thread    device=${srx0}     destination=${anchored_pic}
        """

        status = dev.execute_vty_command_on_device(
            device=device,
            command='show usp flow session summary wing-per-thread-affinity',
            destination=destination,
        )
        out_dict = {}
        for line in status.splitlines()[1:]:
            if not re.match(r'\d', line):
                continue
            row = line.split()
            out_dict[row[0]] = row[1]

        device.log(message="Output dict:\n{}".format(self.tool.pprint(out_dict)), level='DEBUG')
        return out_dict

    #Function to Verify flow sessions wing per thread affinity anchored on all the threads in PIC where IPSEC is anchored
    #------------------------------------------------------------------------------------------------------------------
    def verify_wing_per_thread(self, device, **kwargs):
        r"""Verify flow sessions wing per thread affinity anchored on all the threads

        :param device:
            **REQUIRED** device object

        :param destination:
    	    **REQUIRED**  tunnel anchored pic

        :param cp_flow:
    	    **OPTIONAL**  If tunnel anchored pic lands on Cp-Flow, where it will be having only 13 threads.

        :return:
            True/False

        :example:
            For Python

            verify_wing_per_thread(rh, 'fpc0.pic0')

            # To verify -ve scenario for all the threads are not occupied with flows. Send expecting_nonzero=False
            verify_wing_per_thread(rh, 'fpc0.pic0', False)

            # To verify flows specific to Cp-Flow if tunnel lands on CP-FLow
            verify_wing_per_thread(rh, 'fpc0.pic0', False)

            For robot

            ${status}    flows.Verify Wing Per Thread    ${srx0}    destination=${anchored_pic}    expecting_nonzero=${True}

            # To verify -ve scenario for all the threads are not occupied with flows. Send expecting_nonzero=False
            ${status}    flows.Verify Wing Per Thread    ${srx0}    destination=${anchored_pic}    expecting_nonzero=${False}

            # To verify flows specific to Cp-Flow if tunnel lands on CP-FLow
            ${status}    flows.Verify Wing Per Thread    ${srx0}    destination=${anchored_pic}    cp_flow=${True}

        """

        if 'destination' not in kwargs:
            raise KeyError("destination is mandatory for all srx5k series platforms")

        start_thread = kwargs.get('start_thread', 1)
        if 'cp_flow' in kwargs:
            start_thread = 15

        end_thread = kwargs.get('end_thread', 27)
        expecting_nonzero = kwargs.get('expecting_nonzero', True)
        out_dict = self.get_wing_per_thread(device, kwargs['destination'])
        partial_dict = {k: out_dict[k] for k in out_dict.keys() if int(k) in range(int(start_thread), int(end_thread) + 1)}
        device.log(message="partial_dict:\n{}".format(self.tool.pprint(partial_dict)), level="DEBUG")

        status = any(x == '0' for x in partial_dict.values())  # it will be True if any one is zero
        if not (status) == expecting_nonzero:
            # print("Given status " + str(expecting_nonzero) + " matches with pic status " + str(not status))
            device.log(
                message="Given status " + str(expecting_nonzero) + " matches with pic status " + str(not status),
                level='DEBUG')
        else:
            # print("Given status " + str(expecting_nonzero) + " doesnot matches with pic status " + str(not status))
            raise TobyException(
                "Given status " + str(expecting_nonzero) + " doesnot matches with pic status " + str(not status))

        return True

    def verify_flow_session_on_vty(self, device, condition=None, **kwargs):
        r"""Search VTY flow session based on method fetch_flow_session_on_vty

        This method invoke method fetch_flow_session_on_vty and then search each session to match all given
        arguments. Method will not searching if set to None

        robot Example:

            &{search_session}    Create Dictionary
            ...    in_src_addr=121.11.10.2
            ...    in_dst_addr=121.11.20.2
            ...    in_dst_port=23
            ...    in_protocol=tcp
            ...    out_src_addr=${None}         # will skip this argument

            ${status}    flows.Search FLOW Session On VTY    device=${r0}    condition=${search_session}

        Python Example:
            session = {"in_src_addr": "121.11.10.2", "in_dst_addr": "121.11.20.2", "in_dst_port": 23, "in_protocol": "tcp"}
            status = flows.search_flow_session_on_vty(device=r0, condition=session)

        Another condition structure has been supported that do not create condition dict first, just use dynamic options

        Here is the same behavior above:

            ${status}    flows.Search FLOW Session On VTY
            ...    device=${r0}
            ...    in_src_addr=121.11.10.2
            ...    in_dst_addr=121.11.20.2
            ...    in_dst_port=23
            ...    in_protocol=tcp
            ...    out_src_addr=${None}         # will skip this argument

        :param STR return_mode:
            *OPTIONAL* If set "counter", this method will return how many sessions match all condition

        :param STR destination:
            *OPTIONAL* Used by method "fetch_flow_session_on_vty". Should set to "CP", "SPU" or "ALL". Default: CP

        :param DICT condition:
            *OPTIONAL* condition is a dictionary which have dynamic key=values, it depends on returns of method
                       "fetch_flow_session_on_vty". For example, if fetch_flow_session_on_vty returns like below, all
                       keywords should be given for searching:

                       [
                            {
                                "anchor_spu_id": "256",
                                "anchor_tunnel_session_with_nsp_tunnel": "0x2abf2300",
                                "backup_session": false,
                                "bind_if": "st0.1",
                                "final_nh": "0x587f6c00",
                                "flag": "0x42/0x30",
                                "flags": "10000/0/1",
                                "forward_session": false,
                                "ha_if": "ge-0/0/1.0",
                                "if": "ge-0/0/1.0",
                                "iked_dist_id": "1024",
                                "in_bytes": "0",
                                "in_classifier_cos": "0",
                                "in_conn_tag": "0x0",
                                "in_cp_sess_spu_id": "0",
                                "in_cp_session_id": "0",
                                "in_diff": "0",
                                "in_dp": "0",
                                "in_dst_addr": "2030:0:0:0:0:0:0:1",
                                "in_dst_port": "12609",
                                "in_protocol": "50",
                                "in_flag": "0623",
                                "in_if": "ge-0/0/1.0 (9)",
                                "in_is_tunnel_cos_ready": "Nonh: 0x1b0010",
                                "in_pkts": "0",
                                "in_pmtu": "0",
                                "in_src_addr": "2030:0:0:0:0:0:0:2",
                                "in_src_port": "21825",
                                "in_thread_id": "1",
                                "in_tunnel_info": "0x0",
                                "in_tunnel_pmtu": "0",
                                "in_vrf_grp_id": "0(0)",
                                "in_wsf": "0",
                                "logical_system": "root-logical-system",
                                "nt_next": "0x0",
                                "nt_prev": "0x0",
                                "pmtu_tunnel_overhead": "96",
                                "policy": "0",
                                "session_id": "1",
                                "state": "3",
                                "timeout": "-1s -1s",
                                "tun_flag": "0x60",
                                "tunnel_id": "131074",
                                "tunnel_info": "0x20020002",
                                "tunnel_session_nexthop": "0x0",
                                "tunnel_session_token": "7"
                            },
                            ...
                        ]

            :return:
                If option "return_mode" is not set, return True/False. If return_mode="counter", return how many session match all given condition.
                if option "session" not given or None, it means match all sessions.
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["condition"] = condition
        options["destination"] = kwargs.pop('destination', "CP")
        options["return_mode"] = str(kwargs.pop('return_mode', None)).upper()

        if options["condition"] is None:
            options["condition"] = kwargs

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=options["condition"],
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        all_session_list = self.fetch_flow_session_on_vty(device=device, destination=options["destination"])
        if options["condition"] in (None, dict()):
            return_value = len(all_session_list) if options["return_mode"] == "COUNTER" else bool(all_session_list)
            device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
            return return_value

        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=all_session_list,
            index_option="session_id",
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_session_list,
            index_option="session_id",
            debug_to_stdout=self.debug_to_stdout,
        )
        return_value = len(matched_session_list) if options["return_mode"] == "COUNTER" else bool(matched_session_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value


    def verify_flow_pmi_statistics(self, device, **kwargs):
        r"""According to given option to check whether wanted pmi statistics entry exists

        This method based on 'fetch_flow_pmi_statistics' that have dynamic options to filter device session one by one,
        and return True or False to indicate needed entry whether exist. If option 'return_mode' set to 'counter',
        it will return matched session counter

        Here is an example of PMI statistics entry list, all keywords in every entry should be an option:

        [
            {
                "pmi_decap_bytes": "0",
                "pmi_decap_pkts": "0",
                "pmi_drop": "0",
                "pmi_encap_bytes": "0",
                "pmi_encap_pkts": "0",
                "pmi_rfp": "0",
                "pmi_rx": "0",
                "pmi_spu_id": "of FPC2 PIC0:",
                "pmi_tx": "0",
                "re_name": "node0"
            },
            {
                "pmi_decap_bytes": "0",
                "pmi_decap_pkts": "0",
                "pmi_drop": "0",
                "pmi_encap_bytes": "0",
                "pmi_encap_pkts": "0",
                "pmi_rfp": "0",
                "pmi_rx": "0",
                "pmi_spu_id": "summary:",
                "pmi_tx": "0",
                "re_name": "node1"
            }
        ]

        :param INT|STR node:
            *OPTIONAL* HA testbed node name. node0 or node1, or just 0 or 1

        :param INT timeout:
            *OPTIONAL* Timeout to fetch result from device.

        :param STR return_mode:
            *OPTIONAL* As default just return True/False to indicate whether wanted session matched. Set 'counter' to
                       get how many entry matched all conditions

        :return: True/False, or return a integer if option 'return_mode' is 'counter'. Any issue will do raise

        :example:
            For Python

            status = verify_flow_pmi_statistics(
                device=device,
                pmi_decap_bytes="0",
                pmi_decap_pkts="0",
                pmi_drop="0",
                pmi_encap_bytes="0",
                pmi_encap_pkts="0",
                pmi_rfp="0",
                pmi_rx="0",
                pmi_spu_id="PIC1 in",
                pmi_tx="0",
                re_name="node0",
            )

            For robot:

            ${result}   verify flow pmi statistics
            ...    device=${r0}
            ...    pmi_decap_bytes=0,
            ...    pmi_decap_pkts=0,
            ...    pmi_drop=0,
            ...    pmi_encap_bytes=0,
            ...    pmi_encap_pkts=0,
            ...    pmi_rfp=0,
            ...    pmi_rx=0,
            ...    pmi_spu_id=PIC1 in,
            ...    pmi_tx=0,
            ...    re_name=node0,
            Run Keyword And Continue On Failure     Should Be True      ${result}       ${True}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        # kwargs are mixed user filter options and function options. Remove funtion options here to cleanup user filters
        options = {}
        options["return_mode"] = kwargs.pop("return_mode", None)
        options["timeout"] = kwargs.pop("timeout", self.default["cli_show_timeout"])
        options["node"] = kwargs.get("node", None)

        if options["node"] is not None:
            options["node"] = self.tool.get_node_value(options["node"], mode="INT")


        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        all_session_list = self.fetch_flow_pmi_statistics(
            device=device,
            node=options["node"],
            timeout=options["timeout"],
            return_mode="flat_dict",
        )

        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=all_session_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_session_list,
            debug_to_stdout=self.debug_to_stdout,
        )
        return_value = len(matched_session_list) if options["return_mode"] == "counter" else bool(matched_session_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value
