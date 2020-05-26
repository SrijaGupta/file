# coding: UTF-8
"""All system security-profile related methods

Below options are have same behavior:

+   device (OBJECT) - Device handler

+   timeout (INT) - Timeout for send command to device and waiting for response

In this module, all "search_xxx_xxx" method used to find specific entry.

Following types used to match entry value:

    -   IP:     IPAddress, IPRange or NETWORK related checking
    -   STR:    STR related checking
    -   NUMBER: INT or FLOAT related checking

And each type have below actions to match:

    -   EQ or EQUAL:                A == B. For IP, means IP A exact equal B (include netmask)
    -   NE or NOT_EQUAL             A != B.
    -   IN or CONTAIN               A in B.

                                    For NUMBER|FLOAT, checking NUMBER A in number range B. For example, below will return True:
                                        NUMBER A: 10.0
                                        NUMBER B: 1-100

                                    For IP, This means IP A is subnet of B or exact equal B. And you can give IP range like below,
                                    Action will return True because IP A is subnet of B:
                                        IP A: "192.168.1.50"
                                        IP B: "192.168.1.1-192.168.1.100"

                                    For STRING, searching STRING A from STRING B or A exact equal B.

                                    For DATE, search date STRING A between date range:
                                        DATE A:  2018-12-25 08:00:00 CST
                                        DATE B:  2018-12-20 08:00:00 CST-2018-12-30 08:00:00 CST

    -   GT or GREAT_THAN            A > B.  Only for INT|FLOAT|DATE checking
    -   GE or GREAT_AND_EQUAL_THAN  A >= B. Only for INT|FLOAT|DATE checking
    -   LT or LESS_THAN             A < B.  Only for INT|FLOAT|DATE checking
    -   LE or LESS_AND_EQUAL_THAN   A <= B. Only for INT|FLOAT|DATE checking
"""
# pylint: disable=invalid-name,consider-iterating-dictionary

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import copy

from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.hldcl import device as dev


class security_profile():
    """All system security-profile methods"""
    def __init__(self):
        """INIT"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()

        self.default = {
            "CLI_SHOW_TIMEOUT":     300,
            "CLI_COMMIT_TIMEOUT":   300,
        }

        self.debug_to_stdout = False
        self.runtime = {}

        # MTS compatible keywords
        self.get_address_book = self.fetch_address_book
        self.get_appfw_profile = self.fetch_appfw_profile
        self.get_appfw_rule = self.fetch_appfw_rule
        self.get_appfw_rule_set = self.fetch_appfw_rule_set
        self.get_auth_entry = self.fetch_auth_entry
        self.get_flow_gate = self.fetch_flow_gate
        self.get_flow_session = self.fetch_flow_session
        self.get_dslite_softwire_initiator = self.fetch_dslite_softwire_initiator
        self.get_nat_cone_binding = self.fetch_nat_cone_binding
        self.get_nat_destination_pool = self.fetch_nat_destination_pool
        self.get_nat_destination_rule = self.fetch_nat_destination_rule
        self.get_nat_interface_port_ol = self.fetch_nat_interface_port_ol
        self.get_nat_nopat_address = self.fetch_nat_nopat_address
        self.get_nat_pat_address = self.fetch_nat_pat_address
        self.get_nat_pat_portnum = self.fetch_nat_pat_portnum
        self.get_nat_port_ol_ipnumber = self.fetch_nat_port_ol_ipnumber
        self.get_nat_rule_referenced_prefix = self.fetch_nat_rule_referenced_prefix
        self.get_nat_source_pool = self.fetch_nat_source_pool
        self.get_nat_source_rule = self.fetch_nat_source_rule
        self.get_nat_static_rule = self.fetch_nat_static_rule
        self.get_policy = self.fetch_policy
        self.get_policy_with_count = self.fetch_policy_with_count
        self.get_scheduler = self.fetch_scheduler
        self.get_security_log_stream_number = self.fetch_security_log_stream_number
        self.get_zone = self.fetch_zone
        self.search_address_book = self.verify_address_book
        self.search_appfw_profile = self.verify_appfw_profile
        self.search_appfw_rule = self.verify_appfw_rule
        self.search_appfw_rule_set = self.verify_appfw_rule_set
        self.search_auth_entry = self.verify_auth_entry
        self.search_dslite_softwire_initiator = self.verify_dslite_softwire_initiator
        self.search_flow_gate = self.verify_flow_gate
        self.search_flow_session = self.verify_flow_session
        self.search_nat_cone_binding = self.verify_nat_cone_binding
        self.search_nat_destination_pool = self.verify_nat_destination_pool
        self.search_nat_destination_rule = self.verify_nat_destination_rule
        self.search_nat_interface_port_ol = self.verify_nat_interface_port_ol
        self.search_nat_nopat_address = self.verify_nat_nopat_address
        self.search_nat_pat_address = self.verify_nat_pat_address
        self.search_nat_pat_portnum = self.verify_nat_pat_portnum
        self.search_nat_port_ol_ipnumber = self.verify_nat_port_ol_ipnumber
        self.search_nat_rule_referenced_prefix = self.verify_nat_rule_referenced_prefix
        self.search_nat_source_pool = self.verify_nat_source_pool
        self.search_nat_source_rule = self.verify_nat_source_rule
        self.search_nat_static_rule = self.verify_nat_static_rule
        self.search_policy = self.verify_policy
        self.search_policy_with_count = self.verify_policy_with_count
        self.search_scheduler = self.verify_scheduler
        self.search_security_log_stream_number = self.verify_security_log_stream_number
        self.search_zone = self.verify_zone


    def _common_get_processing(self, device, cmd_keyword, kwargs):
        """Common processing to handle device xml response

        For "show system security-profile ..." cmds, device response almost have same data structure. This method
        extract common processing to treat these response

        :param STR cmd_keyword:
            **REQUIRED** feature command keyword.

        :param DICT kwargs:
            **REQUIRED** more_options

        :return:
            Return a LIST contain all entries or TEXT response
        """
        options = {}
        options["more_options"] = kwargs.pop('more_options', None)
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["timeout"] = int(kwargs.pop("timeout", self.default["CLI_COMMIT_TIMEOUT"]))

        cmd_element = []
        cmd_element.append("show system security-profile {}".format(cmd_keyword))

        if options["more_options"]:
            cmd_element.append(options["more_options"])

        if options["return_mode"] == "TEXT":
            response_format = "text"
        else:
            response_format = "xml"

        response = dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_element),
            channel="pyez",
            format=response_format,
            timeout=options["timeout"],
        )

        if options["return_mode"] == "TEXT":
            return response

        response = self.xml.strip_xml_response(self.xml.xml_to_pure_dict(response), return_list=True)
        if cmd_keyword == "nat-interface-port-ol":
            cmd_keyword = "nat-interface-po"

        main_path_keyword = "security-profile-{}-information".format(cmd_keyword)
        all_entry_list = []
        for item in response:
            info = {}
            for keyword in item:
                if keyword != main_path_keyword:
                    info[self.tool.underscore_and_lowercase_transit(keyword)] = str(item[keyword])

            for entry in self.tool.set_element_list(item[main_path_keyword]["security-profile-information"]):
                for keyword in entry:
                    info_keyword = self.tool.underscore_and_lowercase_transit(keyword)
                    info[info_keyword] = str(entry[keyword])

                all_entry_list.append(copy.deepcopy(info))

        return all_entry_list

    def _common_search_processing(self, device, previous_entry_list_keyword, get_entry_method, kwargs):
        """Common processing to search entry from entry list

        :param STR previous_entry_list_keyword:
            **REQUIRED** If match_from_previous_response option is True, will read previous entry from self.runtime, here indicate runtime
                         keyword.

        :param SELF.METHOD get_entry_method:
            **REQUIRED** Method handler in this class to get entry list.

        :param DICT kwargs:
            **REQUIRED** User option to find related entry

        :return:
            Return match all options' counter
        """
        options = {}
        options["more_options"] = kwargs.pop('more_options', None)
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["match_from_previous_response"] = self.tool.check_boolean(kwargs.pop("match_from_previous_response", False))
        options["timeout"] = int(kwargs.pop("timeout", self.default["CLI_COMMIT_TIMEOUT"]))

        filters = self.tool.create_verify_filters(
            device=device,
            named_options=kwargs,
            align_option_keyword=True,
            log_level="DEBUG",
            debug_to_stdout=self.debug_to_stdout,
        )

        # init previous get entry result
        dev_name = str(device)
        if dev_name not in self.runtime:
            self.runtime[dev_name] = {}

        if previous_entry_list_keyword not in self.runtime[dev_name]:
            self.runtime[dev_name][previous_entry_list_keyword] = None

        if not self.runtime[dev_name][previous_entry_list_keyword] or options["match_from_previous_response"] is False:
            self.runtime[dev_name][previous_entry_list_keyword] = get_entry_method(
                device=device,
                more_options=options["more_options"],
                return_mode="xml",
                timeout=options["timeout"],
            )

        all_entry_list = self.runtime[dev_name][previous_entry_list_keyword]
        matched_session_list = self.tool.filter_option_from_entry_list(
            device=device,
            filters=filters,
            entries=all_entry_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        self.tool.print_result_table(
            device=device,
            filters=filters,
            entries=matched_session_list,
            debug_to_stdout=self.debug_to_stdout,
        )

        return len(matched_session_list)

    def fetch_address_book(self, device, **kwargs):
        """Get all address book entries.

        Base command: "show system security-profile address-book"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="address-book", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_appfw_profile(self, device, **kwargs):
        """Get all appfw profile entries.

        Base command: "show system security-profile appfw-profile"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="appfw-profile", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_appfw_rule(self, device, **kwargs):
        """Get all appfw rule entries.

        Base command: "show system security-profile appfw-rule"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="appfw-rule", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_appfw_rule_set(self, device, **kwargs):
        """Get all appfw rule set entries.

        Base command: "show system security-profile appfw-rule-set"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="appfw-rule-set", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_auth_entry(self, device, **kwargs):
        """Get all appfw rule set entries.

        Base command: "show system security-profile auth-entry"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="auth-entry", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_flow_gate(self, device, **kwargs):
        """Get all appfw rule entries.

        Base command: "show system security-profile flow-gate"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="flow-gate", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_flow_session(self, device, **kwargs):
        """Get all appfw rule entries.

        Base command: "show system security-profile flow-session"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="flow-session", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_dslite_softwire_initiator(self, device, **kwargs):
        """Get all dslite softwire initiator entries.

        Base command: "show system security-profile dslite-softwire-initiator"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="dslite-softwire-initiator", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_cone_binding(self, device, **kwargs):
        """Get all nat cone binding entries.

        Base command: "show system security-profile nat-cone-binding"

        Support SA/HA setup and LE/HE platform.

        :params STR more_options:
            *OPTIONAL* more options will be tailed to base command. default: None

        :param STR return_mode:
            *OPTIONAL* If return_mode is "text", just return command response without "| display xml". default: None

        :param INT|STR timeout:
            *OPTIONAL* show and commit timeout. default: 300

        :return:
            If return_mode is "text", just return text response (without "| display xml").

            Otherwise return a LIST which contain all entries like below:

            SA:

                [
                    {
                        "logical_system_name": "root-logical-system",
                        "resources_maximum": "0",
                        "resources_reserved": "0",
                        "resources_used": "0",
                        "security_profile_name": "Default-Profile"
                     }
                 ]

            SA with MULTI-LSYS:

                [
                    {
                        "logical_system_name": "root-logical-system",
                        "resources_maximum": "2097152",
                        "resources_reserved": "0",
                        "resources_used": "0",
                        "security_profile_name": "Default-Profile"
                    },
                    {
                        "logical_system_name": "LSYS1",
                        "resources_maximum": "2097152",
                        "resources_reserved": "0",
                        "resources_used": "0",
                        "security_profile_name": "SP1"
                    },
                    {
                        "logical_system_name": "LSYS2",
                        "resources_maximum": "2097152",
                        "resources_reserved": "0",
                        "resources_used": "0",
                        "security_profile_name": "SP2"
                     }
                 ]

            HA:
                [
                    {
                        "logical_system_name": "root-logical-system",
                        "re_name": "node0",
                        "resources_maximum": "2097152",
                        "resources_reserved": "0",
                        "resources_used": "0",
                        "security_profile_name": "Default-Profile"
                    },
                    {
                        "logical_system_name": "root-logical-system",
                        "re_name": "node1",
                        "resources_maximum": "2097152",
                        "resources_reserved": "0",
                        "resources_used": "0",
                        "security_profile_name": "Default-Profile"
                     }
                 ]

        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-cone-binding", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_destination_pool(self, device, **kwargs):
        """Get all nat destination pool entries.

        Base command: "show system security-profile nat-destination-pool"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-destination-pool", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_destination_rule(self, device, **kwargs):
        """Get all nat destination rule entries.

        Base command: "show system security-profile nat-destination-rule"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-destination-rule", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_interface_port_ol(self, device, **kwargs):
        """Get all nat interface port ol entries.

        Base command: "show system security-profile nat-interface-port-ol"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-interface-port-ol", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_nopat_address(self, device, **kwargs):
        """Get all nat nopat address entries.

        Base command: "show system security-profile nat-nopat-address"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-nopat-address", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_pat_address(self, device, **kwargs):
        """Get all nat pat address entries.

        Base command: "show system security-profile nat-pat-address"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-pat-address", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_pat_portnum(self, device, **kwargs):
        """Get all nat pat portnum entries.

        Base command: "show system security-profile nat-pat-portnum"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-pat-portnum", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_port_ol_ipnumber(self, device, **kwargs):
        """Get all nat port ol ipnumber entries.

        Base command: "show system security-profile nat-port-ol-ipnumber"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-port-ol-ipnumber", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_rule_referenced_prefix(self, device, **kwargs):
        """Get all nat rule referenced prefix entries.

        Base command: "show system security-profile nat-rule-referenced-prefix"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-rule-referenced-prefix", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_source_pool(self, device, **kwargs):
        """Get all nat port ol ipnumber entries.

        Base command: "show system security-profile nat-source-pool"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-source-pool", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_source_rule(self, device, **kwargs):
        """Get all nat source rule.

        Base command: "show system security-profile nat-source-rule"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-source-rule", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_nat_static_rule(self, device, **kwargs):
        """Get all nat static rule entries.

        Base command: "show system security-profile nat-static-rule"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="nat-static-rule", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_policy(self, device, **kwargs):
        """Get all policy entries.

        Base command: "show system security-profile auth-entry"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="policy", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_policy_with_count(self, device, **kwargs):
        """Get all policy with count entries.

        Base command: "show system security-profile policy-with-count"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="policy-with-count", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_scheduler(self, device, **kwargs):
        """Get all scheduler entries.

        Base command: "show system security-profile scheduler"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="scheduler", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_security_log_stream_number(self, device, **kwargs):
        """Get all security log stream number entries.

        Base command: "show system security-profile security-log-stream-number"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="security-log-stream-num", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def fetch_zone(self, device, **kwargs):
        """Get all zone entries.

        Base command: "show system security-profile zone"

        Support SA/HA setup and LE/HE platform.

        Usage: same as method "get_nat_cone_binding"
        """
        all_entry_list = self._common_get_processing(device=device, cmd_keyword="zone", kwargs=kwargs)
        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), self.tool.pprint(all_entry_list)))
        return all_entry_list

    def verify_address_book(self, device, **kwargs):
        """search system security-profile address book entry

        Base on method self.get_address_book to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="address_book_entry_list",
            get_entry_method=self.get_address_book,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_appfw_profile(self, device, **kwargs):
        """search system security-profile appfw profile entry

        Base on method self.get_appfw_profile to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="appfw_profile_entry_list",
            get_entry_method=self.get_appfw_profile,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_appfw_rule(self, device, **kwargs):
        """search system security-profile appfw rule entry

        Base on method self.get_appfw_rule to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="appfw_rule_entry_list",
            get_entry_method=self.get_appfw_rule,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_appfw_rule_set(self, device, **kwargs):
        """search system security-profile appfw rule set entry

        Base on method self.get_appfw_rule_set to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="appfw_rule_set_entry_list",
            get_entry_method=self.get_appfw_rule_set,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_auth_entry(self, device, **kwargs):
        """search system security-profile auth entry

        Base on method self.get_auth_entry to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="auth_entry_list",
            get_entry_method=self.get_auth_entry,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_dslite_softwire_initiator(self, device, **kwargs):
        """search system security-profile dslite softwire initiator entry

        Base on method self.get_dslite_softwire_initiator to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="dslite_softwire_initiator_entry_list",
            get_entry_method=self.get_dslite_softwire_initiator,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_flow_gate(self, device, **kwargs):
        """search system security-profile flow gate entry

        Base on method self.get_flow_gate to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="flow_gate_entry_list",
            get_entry_method=self.get_flow_gate,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_flow_session(self, device, **kwargs):
        """search system security-profile flow session entry

        Base on method self.get_flow_sessionon to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="flow_session_entry_list",
            get_entry_method=self.get_flow_session,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_cone_binding(self, device, **kwargs):
        """search system security-profile nat cone binding entry

        Base on method self.get_nat_cone_binding to search specific entry.

        Searching option are all as below, default action is "eq":

            +   logical_system_name     (STR)
            +   security_profile_name   (STR)
            +   re_name                 (STR)
            +   resources_maximum       (INT|STR)
            +   resources_reserved      (INT|STR)
            +   resources_used          (INT|STR)
            +   resources_available     (INT|STR)
            +   total_profiles          (INT|STR)
            +   heaviest_usage          (INT|STR)
            +   heaviest_user           (INT|STR)
            +   lightest_usage          (INT|STR)
            +   lightest_user           (INT|STR)

        :param STR return_mode:
            *OPTIONAL* If return_mode is "counter", return match counter instead of True/False. default: None

        :params STR more_options:
            *OPTIONAL* This method use self.get_route_instance_entry to get all entries based on "show route instance". You can add more options such
                       as "brief", "detail", "summary", etc... default: None

        :params BOOL match_from_previous_response:
            *OPTIONAL* As default, this method will get latest info from device and do searching. You can set "True" to search from lastest result
                       from cache. If no cache is empty, will get entry from device automatically. default: False

        :params STR|INT timeout:
            *OPTIONAL* Timeout to get response from device. default: 300

        :return:
            If return_mode is "counter", return how many entries satisfied all given options, or 0. Otherwise return True/False
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_cone_binding_entry_list",
            get_entry_method=self.get_nat_cone_binding,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_destination_pool(self, device, **kwargs):
        """search system security-profile nat destination pool entry

        Base on method self.get_nat_destination_pool to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_destination_pool_entry_list",
            get_entry_method=self.get_nat_destination_pool,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_destination_rule(self, device, **kwargs):
        """search system security-profile nat destination rule entry

        Base on method self.get_nat_destination_rule to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_destination_rule_entry_list",
            get_entry_method=self.get_nat_destination_rule,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_interface_port_ol(self, device, **kwargs):
        """search system security-profile nat interface port ol entry

        Base on method self.get_nat_interface_port_ol to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_interface_port_ol_entry_list",
            get_entry_method=self.get_nat_interface_port_ol,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_nopat_address(self, device, **kwargs):
        """search system security-profile nat interface port ol entry

        Base on method self.get_nat_nopat_address to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_nopat_address_entry_list",
            get_entry_method=self.get_nat_nopat_address,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_pat_address(self, device, **kwargs):
        """search system security-profile nat pat address entry

        Base on method self.get_nat_pat_address to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_pat_address_entry_list",
            get_entry_method=self.get_nat_pat_address,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_pat_portnum(self, device, **kwargs):
        """search system security-profile nat pat portnu entry

        Base on method self.get_nat_pat_portnum to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_pat_portnu_entry_list",
            get_entry_method=self.get_nat_pat_portnum,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_port_ol_ipnumber(self, device, **kwargs):
        """search system security-profile nat port ol ipnumber entry

        Base on method self.get_nat_port_ol_ipnumber to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_port_ol_ipnumber_entry_list",
            get_entry_method=self.get_nat_port_ol_ipnumber,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_rule_referenced_prefix(self, device, **kwargs):
        """search system security-profile nat rule referenced prefix entry

        Base on method self.get_nat_rule_referenced_prefix to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_rule_referenced_prefix_entry_list",
            get_entry_method=self.get_nat_rule_referenced_prefix,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_source_pool(self, device, **kwargs):
        """search system security-profile nat source pool entry

        Base on method self.get_nat_source_pool to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_source_pool_entry_list",
            get_entry_method=self.get_nat_source_pool,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_source_rule(self, device, **kwargs):
        """search system security-profile nat source rule entry

        Base on method self.get_nat_source_rule to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_source_rule_entry_list",
            get_entry_method=self.get_nat_source_rule,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_nat_static_rule(self, device, **kwargs):
        """search system security-profile nat port ol ipnumber entry

        Base on method self.get_nat_static_rule to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="nat_static_rule_entry_list",
            get_entry_method=self.get_nat_static_rule,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_policy(self, device, **kwargs):
        """search system security-profile policy entry

        Base on method self.get_policy to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="policy_entry_list",
            get_entry_method=self.get_policy,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_policy_with_count(self, device, **kwargs):
        """search system security-profile policy with count entry

        Base on method self.get_policy_with_count to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="policy_with_count_entry_list",
            get_entry_method=self.get_policy_with_count,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_scheduler(self, device, **kwargs):
        """search system security-profile scheduler entry

        Base on method self.get_scheduler to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="scheduler_entry_list",
            get_entry_method=self.get_scheduler,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_security_log_stream_number(self, device, **kwargs):
        """search system security-profile nat security_log_stream_number entry

        Base on method self.get_nat_pat_portnum to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="security_log_stream_num",
            get_entry_method=self.get_security_log_stream_number,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value

    def verify_zone(self, device, **kwargs):
        """search system security-profile zone entry

        Base on method self.get_zone to search specific entry.

        Usage: Same as search_nat_cone_binding
        """
        return_value = self._common_search_processing(
            device=device,
            previous_entry_list_keyword="zone_entry_list",
            get_entry_method=self.get_zone,
            kwargs=kwargs,
        )
        device.log(message="{} return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value
