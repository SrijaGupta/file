# coding: UTF-8
# pylint: disable=invalid-name
"""License related keywords

Below options are have same behavior:

+   device (OBJECT) - Device handler

+   timeout (INT) - Timeout for send command to device and waiting for response

In this module, below keywords have option to compare IP/STR/NUMBER/DATE:

+   search_license

Following types used to match entry value:

    -   IP:     IPAddress, IPRange or NETWORK related checking
    -   STR:    STR related checking
    -   NUMBER: INT or FLOAT related checking
    -   DATE:   DATE or DATE RANGE STRING

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

For more detail, see jnpr.toby.utils.flow_common_tool.do_compare
"""
import copy

from jnpr.toby.utils.message import message
from jnpr.toby.utils.flow_common_tool import flow_common_tool

class system_license(message):
    """License related keywords"""
    def __init__(self):
        """Init"""
        super().__init__()
        self.tool = flow_common_tool()

        self.default = {
            "CLI_SHOW_TIMEOUT":     300,
            "CLI_COMMIT_TIMEOUT":   300,
        }

        self.hidden_info = {}
        self.hidden_info["license"] = {}

    def search_license(self, **kwargs):
        """search license from device

        Based on command "show system license usage" command to checking license whether existing.

        On device, there are 3 types of license:

        1.  remaining-time:

            ```
                                Licenses used     Licenses installed    Licenses needed    Expiry
            Virtual Appliance   1                 1                     0                  30 days
            ```

            self.search_license(
                device_license_list=device_license_list,
                name="Virtual Appliance",
                licensed=1,                 # License installed
                needed=0,                   # License needed
                used_licensed=1,            # License used
                remaining_time="30 days",   # Expiry
            )

        2.  permanent and embed license

            ```
                                Licenses used     Licenses installed    Licenses needed    Expiry
            logical-system      1                 1                     0                  permanent
            ```

            self.search_license(
                device_license_list=device_license_list,
                name="logical-system",
                licensed=1,                 # License installed
                needed=0,                   # License needed
                used_licensed=1,            # License used
                validity_type="permanent",  # Expiry
            )


        3.  expiry date

            ```
                                Licenses used     Licenses installed    Licenses needed    Expiry
            idp-sig             0                 1                     0                  2018-12-25 08:00:00 CST
            ```

            self.search_license(
                device_license_list=device_license_list,
                name="idp-sig",
                licensed=1,                 # License installed
                needed=0,                   # License needed
                used_licensed=0,            # License used
                end_date="2018-12-25 08:00:00 CST",  # Expiry
            )

        :param OBJECT device:
            *OPTIONAL* Device handler. Use command "show system license usage" to get license from device. default: None

        :param LIST device_license_list:
            *OPTIONAL* License information from device. Will ignore option 'device'. default: None

        :param STR name:
            *OPTIONAL* license name. default: None

        :param INS|STR licensed:
            *OPTIONAL* licensed number. default: None

        :param INS|STR needed:
            *OPTIONAL* needed number. default: None

        :param INS|STR remaining_time:
            *OPTIONAL* remaining days number. default: None

        :param INS|STR used_licensed:
            *OPTIONAL* used_licensed number. default: None

        :param INS|STR used_given:
            *OPTIONAL* used_given number. default: None

        :param STR validity_type:
            *OPTIONAL* validity_type string. default: None

        :param STR end_date:
            *OPTIONAL* end_date string. default: None

        :param INT|STR timeout:
            *OPTIONAL* Timeout to get license from device. default: 30

        :param BOOL match_from_previous_response:
            *OPTIONAL* Match license info from previous result, if no previous result, get from device automatically. default: True
        """
        self.display_title(msg=self.tool.get_current_function_name())

        options = {}
        options["device"] = kwargs.pop("device", None)
        options["device_license_list"] = kwargs.pop("device_license_list", None)
        options["match_from_previous_response"] = kwargs.pop("match_from_previous_response", True)
        options["timeout"] = int(kwargs.pop("timeout", self.default["CLI_SHOW_TIMEOUT"]))

        # option validation
        if options["device"] is None and options["device_license_list"] is None:
            raise ValueError("option 'device' or 'device_license_list' must given")

        known_options = {
            "name":                 (None, "STR", "EQ"),
            "remaining_time":       (None, "STR", "EQ"),
            "validity_type":        (None, "STR", "EQ"),
            "licensed":             (None, "INT", "EQ"),
            "used_licensed":        (None, "INT", "EQ"),
            "used_given":           (None, "INT", "EQ"),
            "needed":               (None, "INT", "EQ"),
            "end_date":             (None, "DATE", "LE"),
        }
        search_options = self.tool.get_user_values(
            default_value_mode_action_dict=known_options,
            user_value_dict=kwargs,
            unknown_keyword_value=None,
            unknown_keyword_mode="STR",
            unknown_keyword_action="EQ",
        )

        if options["device_license_list"]:
            license_list = copy.deepcopy(options["device_license_list"])
        else:
            device_name = str(options["device"])
            if device_name in self.hidden_info["license"] and options["match_from_previous_response"] is True:
                license_list = copy.deepcopy(self.hidden_info["license"][device_name])
            else:
                from jnpr.toby.utils.junos.dut_tool import dut_tool
                srx = dut_tool()
                self.hidden_info["license"][device_name] = srx.send_cli_cmd(
                    device=options["device"],
                    cmd="show system license usage",
                    channel="pyez",
                    format="xml",
                    timeout=options["timeout"],
                )
                license_list = copy.deepcopy(self.hidden_info["license"][device_name])

        license_list = license_list["license-usage-summary"]["feature-summary"]
        if not isinstance(license_list, (list, tuple)):
            license_list = [license_list, ]

        return_value = False
        for entry in license_list:
            # align device license entry. next time will comparing entry element by keywords
            #   +   remaining_time have sub-xml element
            #   +   end_date only have YYYY-MM-DD from device that must add HH:MM:SS for DATE comparing
            dev_info = {}
            for keyword in entry:
                lowercase_keyword = self.tool.underscore_and_lowercase_transit(keyword)
                if lowercase_keyword == "remaining_time":
                    dev_info[lowercase_keyword] = entry[keyword]["remaining-validity-value"]
                    continue

                if lowercase_keyword == "end_date":
                    dev_info[lowercase_keyword] = "{} 00:00:00".format(entry[keyword])
                    continue

                dev_info[lowercase_keyword] = entry[keyword]

            # do comparation by user options
            #   +   ignore if user option is None
            license_matched = True
            for keyword in search_options:
                user_value = search_options[keyword][0]
                mode = search_options[keyword][1].upper()
                action = search_options[keyword][2].upper()

                if user_value is None:
                    continue

                if keyword not in dev_info:
                    self.display(msg="No keyword '{}' in license entry".format(keyword), level="TRACE")
                    license_matched = False
                    continue

                # for INT mode, use device value to compare user value
                if mode in ("INT", "NUMBER", "FLOAT"):
                    status = self.tool.do_compare(value_a=dev_info[keyword], value_b=user_value, mode=mode, action=action)
                else:
                    status = self.tool.do_compare(value_a=user_value, value_b=dev_info[keyword], mode=mode, action=action)
                if status is False:
                    self.display(
                        msg="Element '{:16s}' not match: (wanted) {:>20s} <==> {:<20s} (on device)".format(
                            str(keyword), str(user_value), str(dev_info[keyword])
                        ),
                        level="TRACE",
                    )
                    license_matched = False

            if license_matched is True:
                self.display(msg="Match License:")
                for keyword in entry:
                    self.display(msg="\t{:20s}: {}".format(str(keyword), str(entry[keyword])))
                return_value = True

        self.display("'{}' return value: {}".format(self.tool.get_current_function_name(), return_value))
        return return_value
