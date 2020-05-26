# coding: UTF-8
"""Have all route related methods

Below options are have same behavior:

+   device (OBJECT) - Device handler

+   timeout (INT) - Timeout for send command to device and waiting for response
"""
# pylint: disable=invalid-name,consider-iterating-dictionary

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import copy

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.utils.flow_common_tool import flow_common_tool


class route(object):
    """All route instance related methods"""
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

        # MTS behavior compatible support
        self.get_route_instance_entry = self.fetch_route_instance_entry
        self.search_route_instance_entry = self.verify_route_instance_entry


    def fetch_route_instance_entry(self, device, **kwargs):
        """Get route instance entries

        This method use basic command "show route instance". More options will be tailed to basic command.

        HighEnd/LowEnd, SA/HA are supported. According to option "return_mode", method can return a LIST contain all
        flat entries or just plain-text

        :param STR name:
            *OPTIONAL* Instance name. default: None

        :param STR more_options:
            *OPTIONAL* String will tailed to base cmd. Default: None

        :param str return_mode:
            *OPTIONAL* response format that one of "TEXT", "ENTRY_LIST" or "FLAT_DICT. Default: ENTRY_LIST

        :param int timeout:
            *OPTIONAL* timeout to get command response. default: 300

        :return:
            If option "return_mode" is 'TEXT', just return device response without any more process.

            if option 'return_mode' is 'ENTRY_LIST' (default), return a LIST contain all entries. No entry found just
            return empty LIST

        :example:
            [
                {
                    'instance_name': 'master',
                    'instance_type': 'forwarding',
                    'instance_rib': [
                        {
                            'irib_name': 'inet.0',
                            'irib_active_count': '22',
                            'irib_holddown_count': '0',
                            'irib_hidden_count': '0'
                        },
                        {
                            'irib_name': 'inet6.0',
                            'irib_active_count': '7',
                            'irib_holddown_count': '0',
                            'irib_hidden_count': '0'
                        }
                    ]
                }
            ]

            if option 'return_mode' is 'FLAT_DICT', return a LIST contain all entries like below:

        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["name"] = kwargs.pop('name', None)
        options["more_options"] = kwargs.pop('more_options', None)
        options["return_mode"] = str(kwargs.pop("return_mode", "ENTRY_LIST")).strip().upper()
        options["print_response"] = kwargs.pop("print_response", True)
        options["timeout"] = int(kwargs.pop('timeout', self.default['cli_show_timeout']))

        if options["return_mode"] not in ("TEXT", "ENTRY_LIST"):
            raise ValueError("'return_mode' must be 'ENTRY_LIST' or 'TEXT', not '{}'".format(options["return_mode"]))

        if options["return_mode"]  == "ENTRY_LIST":
            response_format = "xml"
        else:
            response_format = "text"

        # combine options to basic command
        cmd_elements = []
        cmd_elements.append("show route instance")

        if options["name"]:
            cmd_elements.append(options["name"])

        if options["more_options"]:
            cmd_elements.append(options["more_options"])

        # get route instance entries
        response = dev.execute_cli_command_on_device(
            device=device,
            command=" ".join(cmd_elements),
            channel="pyez",
            format=response_format,
            timeout=options["timeout"],
        )

        # if user want get "text" mode response, just return here
        if options["return_mode"] == "TEXT":
            device.log(message="{} return value:\n{}".format(func_name, response), level="INFO")
            return response

        if response is False:
            return False

        response = self.xml.strip_xml_response(self.xml.xml_to_pure_dict(response), return_list=False)
        instance_core_list = self.tool.set_element_list(response["instance-information"]["instance-core"])
        route_instance_entry_list = []
        # HE/LE, SA/HA device all have same structure response
        for instance_core in instance_core_list:
            info = {}
            for keyword in instance_core:
                underscore_keyword = self.tool.underscore_and_lowercase_transit(keyword)

                # instance_rib have another argument list
                if underscore_keyword == "instance_rib":
                    rib_list = []
                    instance_core[keyword] = self.tool.set_element_list(instance_core[keyword])
                    for rib_entry in instance_core[keyword]:
                        rib_info = {}
                        for rib_keyword in rib_entry:
                            rib_underscore_keyword = self.tool.underscore_and_lowercase_transit(rib_keyword)
                            rib_info[rib_underscore_keyword] = str(rib_entry[rib_keyword])
                        rib_list.append(rib_info)

                    info[underscore_keyword] = rib_list
                    continue

                info[underscore_keyword] = str(instance_core[keyword])

            route_instance_entry_list.append(info)

        flat_entry_list = []
        for entry in route_instance_entry_list:
            info = {}
            for keyword in entry:
                if keyword != "instance_rib":
                    info[keyword] = entry[keyword]

            if "instance_rib" in entry:
                for instance_rib_entry in entry["instance_rib"]:
                    for keyword in instance_rib_entry:
                        info["instance_rib_{}".format(keyword)] = instance_rib_entry[keyword]

                    flat_entry_list.append(copy.deepcopy(info))
            else:
                flat_entry_list.append(copy.deepcopy(info))

        if options["print_response"] is True:
            device.log(message="return value:\n{}".format(self.tool.pprint(flat_entry_list)), level="INFO")
        return flat_entry_list

    def verify_route_instance_entry(self, device, **kwargs):
        """According to given option to check whether wanted route instance entry exists

        This method have many options to filter route instance entry one by one, and return True or False to indicate at
        least one entry found, or if option 'return_mode' set to 'counter' to return match counter

        Pay attention:
            1. **If no any option given, it means all entry matched and return True**
            2. For INT/NUMBER compare, (100, "lt") means device counter less than 100
            3. For STR compare, ("inet6", "in") means match "inet6color.0" or "inet6" both on device

        For all options, default value is None means do not search this element. And you can set option like below:

        1. Have 2 elements that first one is what you want to search, secondary one is mathing mode.

            # match "mater", "MASTER" or "master.0"
            instance_name=("master", "in")          # Python code
            instance_name=master in                 # Robot code

            # match counter from 10 to 100
            instance_rib_irib_holddown_count=("10-100", "in")       # Python code
            instance_rib_irib_holddown_count=10-100 in              # Robot code

        2. Only a STRING or NUMBER, mathing mode is default action.

            # only match master and case sensitive
            instance_name="master"                  # Python code
            instance_name=master                    # Robot code

            # match counter 100
            instance_rib_irib_holddown_count=100    # Python code
            instance_rib_irib_holddown_count=100    # Robot code

        Searching option are all as below, default action is "eq":

            +   instance_name
            +   instance_type
            +   instance_rib_irib_name
            +   instance_rib_irib_active_count
            +   instance_rib_irib_holddown_count
            +   instance_rib_irib_hidden_count
            +   instance_rib_irib_route_count

        :params STR more_options:
            *OPTIONAL* This method use self.get_route_instance_entry to get all entries based on "show route instance".
                       You can add more options such as "brief", "detail", "summary", etc... default: None

        :params BOOL match_from_previous_response:
            *OPTIONAL* As default, this method will get latest info from device and do searching. You can set "True" to
                       search from lastest result from cache. If no cache is empty, will get entry from device
                       automatically. default: False

        :params STR return_mode:
            *OPTIONAL* If is 'counter', will return how many entries matched.

        :params STR|INT timeout:
            *OPTIONAL* Timeout to get instance entry. default: 300

        :return:
            True/False, or return a number if option 'return_mode' is 'counter'. Any issue will do raise

        :Example Python:
            status = verify_route_instance_entry(
                device=device,
                instance_name=("master", "in"),                         # case insensitive, match "master", "MASTER"
                instance_rib_irib_name="inet6.0",                       # case sensitive, exact match
                instance_rib_irib_active_count=("10-100", "in"),        # match number range from 10 to 100
                instance_rib_irib_hidden_count=0,                       # must equal 0
            )

        :Example robot:
            ${status}   Verify Route Instance Entry
            ...             device=${r0}
            ...             instance_name=master in
            ...             instance_rib_irib_name=inet6.0
            ...             instance_rib_irib_active_count=10-100 in
            ...             instance_rib_irib_hidden_count=0
            Run Keyword And Continue On Failure     Should Be True      ${result}       ${True}
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["more_options"] = kwargs.pop("more_options", None)
        options["match_from_previous_response"] = kwargs.pop("match_from_previous_response", False)
        options["return_mode"] = str(kwargs.pop("return_mode", None)).strip().upper()
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_show_timeout"]))

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

        if "route_instance_entry_list" not in self.runtime[dev_fingerprint]:
            self.runtime[dev_fingerprint]["route_instance_entry_list"] = None

        if (options["match_from_previous_response"] is True and self.runtime[dev_fingerprint]["route_instance_entry_list"] is not None):
            all_entry_list = self.runtime[dev_fingerprint]["route_instance_entry_list"]
        else:
            all_entry_list = self.fetch_route_instance_entry(
                device=device,
                options=options["more_options"],
                timeout=options["timeout"],
                return_mode="ENTRY_LIST",
            )
            self.runtime[dev_fingerprint]["route_instance_entry_list"] = copy.deepcopy(all_entry_list)

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
        return_value = len(matched_session_list) if options["return_mode"] == "COUNTER" else bool(matched_session_list)
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value
