# coding: UTF-8
# pylint: disable=invalid-name
"""Common tools

Must create an instance to use this module. Instance "INS" created by:

```py
from jnpr.toby.utils.flow_common_tool import flow_common_tool
INS = flow_common_tool()
```

+   get_current_function_name

    This is a simple tool to get local method or function's name like '__FUNCTION__' in C language.
    For example:

    ```py
    def im_a_function():
        print("In function: {}".format(INS.get_current_function_name()))
    im_a_function()
    ==> im_a_function
    ```

+   split_string_to_value_and_action

    .robot use keyword to invoke Python code and sometimes need do comparing for a value.
    For example: below strings all have value and comparing action:

        *   Invoke Keyword    session_cnt=1 eq       total_cnt=10 gt
        *   Invoke Keyword    dut_response=commit complete contain
        *   Invoke Keyword    int_ipaddr=192.168.1.0/24 in
        *   Invoke Keyword    int_ipaddr=192.168.1.1-192.168.1.25 in
        *   Invoke Keyword    session_cnt=1

    In Python code, above parameter's value are strings and both have value and comparing action.

    "split_string_to_value_and_action" will separate above string to value and action and then
    return a tuple like this:

        *   (1, "eq") and (10, "gt")
        *   ("commit complete", "contain")
        *   ("192.168.1.0/24", "in")
        *   (1, None)

    This method split string by space and search comparing action keyword from last element. Action
    keyword is from "self.valid_action_list". If last element not an action keyword, will set None.

+   sleep

    In JT, we use $t->sleep(secs=>10, msg="waiting for conf implement") to sleep and print message,
    but so far official TOBY platfrom cannot do it.

    This method have same behavior like JT:

    ```py
    INS.sleep(secs=10, msg="conf implement")
    => sleep '10' secs for conf implement

    INS.sleep(secs=10, msg="waiting for conf implement", add_title=False)
    => waiting for conf implement
    ```

+   do_compare

    Do compare between 2 values (A, B). This method provide below types comparing:

    *   STRING - ("IN", "CONTAIN", "EXACT", "EQ", "EQUAL")

        "IN", "CONTAIN"             - STR_A in STR_B
        "EXACT", "EQ", "EQUAL"      - STR_A == STR_B

        "case_insensitive=True" used to check string with case insensitive or not

    *  INT|FLOAT - ("EQ", "NE", "LT", "LE", "GT", "GE", etc...)

       "EQ", "EQUAL"                - check INT_A == INT_B
       "NE", "NOT_EQUAL"            - check INT_A != INT_B
       "LT", "LESS_THAN"            - check INT_A <  INT_B
       "LE", "LESS_OR_EQUAL_THAN"   - check INT_A <= INT_B
       "GT", "GREAT_THAN"           - check INT_A >  INT_B
       "GE", "GREAT_OR_EQUAL_THAN"  - check INT_A >= INT_B

    *  IPADDR|NETWORK - ("IN", "EQ", "NE", "CONTAIN", "EQUAL", "NOT_EQUAL")

       An IP address or network string like "192.168.1.1", "192.168.1.1/32", "10.208.2.0/24", etc...

       "IN", "CONTAIN"      - IP_A in IP_B
       "EQ", "EQUAL"        - IP_A == IP_B
       "NE", "NOT_EQUAL"    - IP_A != IP_B

+   download_file_by_http

    download file by HTTP or HTTPS

+   flat_dict

    transit a complex dictionary to simple dictionary like below:

    complex_dict = {
        "aaa": {
            "BBB-dd": "bb",
            "Ccc_ee": "cc",
            "eee": {
                "fff": "fff",
                "ggg": "GGG",
            }
        },
        "ddd": "dd",
    }
    print(flat_dict(dict_variable=complex_dict, parent_key="snat"))
    => {
        'snat_aaa_bbb_dd': 'bb',
        'snat_aaa_ccc_ee': 'cc',
        'snat_aaa_eee_fff': 'fff',
        'snat_aaa_eee_ggg': 'GGG',
        'snat_ddd': 'dd',
    }
"""

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import os
import re
import inspect
import time
import netaddr
import requests
import json
import certifi
import copy
import collections


class flow_common_tool():
    """Basic tools for common function"""
    def __init__(self):
        """Init function"""
        self.get_current_function_name = lambda: inspect.stack()[1][3]
        self.pprint = lambda x: json.dumps(x, indent=4, sort_keys=True, default=str, ensure_ascii=False)
        self.print_title = lambda x, width=80, fillchar="=": " {} ".format(x).upper().center(width, fillchar)
        self.underscore_and_lowercase_transit = lambda x: re.sub(r"-", "_", str(x)).lower()
        self.underscore_and_uppercase_transit = lambda x: re.sub(r"-", "_", str(x)).upper()
        self.valid_name_transit = lambda x: self.underscore_and_lowercase_transit(re.sub(r"[\.\:\/]", "_", x))
        self.list_element_to_lowercase_transit = lambda x: [s.lower() for s in x]
        self.list_element_to_uppercase_transit = lambda x: [s.upper() for s in x]
        self.split_string_by_len = lambda string, length: [string[i:i+length] for i in range(0, len(string), length)]
        self.get_string_byte_length = lambda string, codeset="UTF-8": len(string.encode(codeset))
        self.strip_duplicate = lambda x: list(set(x))
        self.strip_quotation_sign = lambda x: re.sub(r"[\"\']", "", x)
        self.set_element_list = lambda x: x if isinstance(x, (list, tuple)) else [x, ]
        self.dict_cleanup = lambda x, delete_value=None: {key: value for key, value in x.items() if value != delete_value}

        self.valid_action_list = (
            "IN", "CONTAIN", "EXACT",
            "EQ", "EQUAL",
            "NE", "NOT_EQUAL",
            "LT", "LESS_THAN",
            "LE", "LESS_OR_EQUAL_THAN",
            "GT", "GREAT_THAN",
            "GE", "GREAT_OR_EQUAL_THAN",
        )

    def split_string_to_value_and_action(self, user_string, with_mode=False, default_mode="STR", strip_user_string=True):
        """Split user given string to check_value and check_action

        :param STR user_string:
            **REQUIRED** User given string

        :param BOOL strip_user_string:
            *OPTIONAL* Strip user given string. default: True

        :param BOOL with_mode:
            *OPTIONAL* checking value is INT, FLOAT, IP, or STR. default: False

        :return: Return a TUPLE like below:

            return_list = (
                (user_value, check_action),
                (user_value, check_action),
            )

            If with_mode=True:

            return_list = (
                (user_value, check_action, check_mode),
                (user_value, check_action, check_mode),
            )

            If no check_action, it set to None

            Any issue return False
        """
        default_action = {
            "INT": "EQ",
            "INT_RANGE": "IN",
            "FLOAT": "EQ",
            "FLOAT_RANGE": "IN",
            "DATE": "EQ",
            "DATE_RANGE": "IN",
            "IP": "EQ",
            "IP_RANGE": "IN",
            "NETWORK": "IN",
            "STR": "IN",
        }

        if strip_user_string is True:
            user_string = str(user_string).strip()

        value = None
        action = None
        mode = None

        # Get user value, and user action if user string have it
        elements = re.split(r"\s+", str(user_string))
        if elements[-1].upper() in self.valid_action_list:
            value = " ".join(elements[:-1])
            action = elements[-1].upper()
        else:
            value = " ".join(elements)


        type_list = []
        item_list = re.split(r"\s*[~\-]\s*", value)

        # special case for DATE
        if re.match(r"\d{4}\-\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}", value):
            type_list.append("DATE")
            if re.search(r"\s*~\s*\d{4}\-\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}", value):
                type_list.append("DATE")

        # special case for IP address or IP range
        try:
            if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", item_list[0]) or re.search(r":", item_list[0]):
                ipaddr, prefix = str(netaddr.IPNetwork(item_list[0])).split(r"/")
                if prefix in ("32", "128"):
                    type_list.append("IP")
                else:
                    type_list.append("NETWORK")

                if len(item_list) == 2 and type_list[0] == "IP" and re.match(r"[0-9a-fA-F]+$", item_list[1]):
                    value = "{}~{}{}".format(
                        ipaddr,
                        re.sub(r"([:\.])[0-9a-fA-F]+$", "\g<1>", ipaddr, count=1),
                        item_list[1],
                    )
                    type_list.append("IP")

        except netaddr.AddrFormatError:
            pass

        for item in item_list:
            # break if special case checked
            already_checked = False
            for special_type in ("IP", "NETWORK", "DATE"):
                if special_type in type_list:
                    already_checked = True
                    break
            if already_checked is True:
                break

            if item.isdigit():
                type_list.append("INT")
                continue

            try:
                if float(item):
                    type_list.append("FLOAT")
                    continue
            except ValueError:
                pass

            type_list.append(str(default_mode).strip().upper())
            break

        # Now checking all types
        if type_list.count("STR") >= 1:
            action = action if action else default_action["STR"]
            mode = "STR"
        elif type_list.count("IP") == 1:
            action = action if action else default_action["IP"]
            mode = "IP"
        elif type_list.count("IP") == 2:
            action = action if action else default_action["IP_RANGE"]
            mode = "IP"
        elif type_list.count("NETWORK") >= 1:
            action = action if action else default_action["NETWORK"]
            mode = "IP"
        elif type_list.count("INT") == 1:
            action = action if action else default_action["INT"]
            mode = "INT"
        elif type_list.count("INT") == 2:
            action = action if action else default_action["INT_RANGE"]
            mode = "INT"
        elif type_list.count("FLOAT") == 1:
            action = action if action else default_action["FLOAT"]
            mode = "FLOAT"
        elif type_list.count("FLOAT") == 2:
            action = action if action else default_action["FLOAT_RANGE"]
            mode = "FLOAT"
        elif type_list.count("DATE") == 1:
            action = action if action else default_action["DATE"]
            mode = "DATE"
        elif type_list.count("DATE") == 2:
            action = action if action else default_action["DATE_RANGE"]
            mode = "DATE"
        else: # pragma: no cover
            raise RuntimeError("Unknown value type of '{}'".format(value))

        return_list = [str(value), action]
        if with_mode is True:
            return_list.append(mode)

        return tuple(return_list)

    @staticmethod
    def sleep(secs=0, msg="", add_title=True):
        """Wait a while and print msg during sleeping

        :param float/int secs:
            *OPTIONAL* sleep secs

        :param bool add_title:
            *OPTIONAL* Set True will add title string about waiting time, otherwise just pring msg.

        :param str msg:
            *OPTIONAL* message to displayed

        :return:
            True/False
        """
        try:
            secs = float(secs)
        except (ValueError, TypeError) as err:
            print(err)
            return False

        if add_title is True:
            msg = "sleep '{}' secs for {}".format(secs, msg)

        print(msg)
        time.sleep(secs)
        return True

    def do_compare(self, value_a, value_b, mode, action, **kwargs):
        """Do compare checking for IP, number, string, etc...

        For IP related comparing, value_a and value_b must be IPv4/6 string to be an address, network or IP range.

        Example: '192.168.1.1/32', '192.168.1.0/24', '192.168.1.1', "192.168.100.100-192.168.100.200",
                 "192.168.100.100 ~ 192.168.100.200", etc...

        For NUMBER related comparing, value must be an INT, FLOAT, or at least a STR but can convert to INT. But
        whatever INT or FLOAT, they will transit to FLOAT to compare.

        Number Range, IP Network or IP Range are special, the compare only for value_a in value_b. This means value_a
        always be an INT, FLOAT, IP address (with /32 or not), and value_b must be a range string like "10-20" or
        "10.0 ~ 20.0". Don't forget set action to "IN" or "CONTAIN", otherwise raise exception.

        Example: 10, "100", "100.03", "10-20"

        For STR related comparing, value must be STR, and option "case_insensitive" can be used.

        For DATE related comparing, value must be DATE STRING like "2018-12-25 18:30:30" or DATE STRANGE RANGE like
        "2018-12-25 18:30:30~2018-12-30 18:30:00", keypoint includes:

            +   DATE STRING must be YYYY-MM-DD HH:MM:SS, you can give "2018-12-25 18:30:30 CST" but timezone string will
                be ignored.
            +   DATE STRANGE RANGE separated by "~", not "-" because it is used in DATE STRANGE

        :param STR mode:
            **REQUIRED** One of below:

                            IP      - IPAddress, IPRange or NETWORK related checking
                            NUMBER  - INT or FLOAT related checking
                            STR     - STR related checking
                            DATE    - DATE related checking

        :param STR action:
            **REQUIRED** compare action string one of self.valid_action_list

        :param STR value_a:
            **REQUIRED** compare_value A

        :param STR value_b:
            **REQUIRED** compare_value B

        :param BOOL case_insensitive:
            *OPTIONAL* Only for STR comparing. Default: False

        :param OBJECT device:
            *OPTIONAL* As default error message will print to stdout. Give device object will print by device.log().
                       default: False

        :param BOOL raise_exception:
            *OPTIONAL* Set True will raise ValueError and stop script. Set False just print error message without raise.
                       default: True

        :return:
            Return True/False to indicate compare resule, or raise error.
        """
        options = {}
        options["mode"] = mode.upper()
        options["action"] = action.upper()
        options["value_a"] = value_a
        options["value_b"] = value_b
        options["case_insensitive"] = self.check_boolean(kwargs.pop("case_insensitive", False))
        options["device"] = kwargs.pop("device", None)
        options["raise_exception"] = self.check_boolean(kwargs.pop("raise_exception", True))

        # valid check
        mode_valid_keywords = (
            "IP", "IPADDR", "IPADDRESS", "NETWORK",
            "INT", "INTEGER", "FLOAT", "NUMBER",
            "STR", "STRING", "TEXT",
            "DATE", "TIME",
        )

        try:
            if options["mode"] not in mode_valid_keywords:
                raise ValueError("valid mode include {}, not {}".format(
                    mode_valid_keywords, options["mode"]
                ))
            if options["action"] not in self.valid_action_list:
                raise ValueError("valid action include {}, not {}".format(
                    self.valid_action_list, options["action"]
                ))

            pattern = {
                "split_range": re.compile(r"\s*[~\-]\s*"),
                "date_pattern": re.compile(r"\d{4}\-\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}$"),
            }

            return_value = None
            runtime = {}
            # IP, NETWORK related check
            if options["mode"] in ("IP", "IPADDR", "IPADDRESS", "NETWORK"):
                options["value_a"] = str(options["value_a"]).strip()
                options["value_b"] = str(options["value_b"]).strip()

                try:
                    if options["action"] in ("IN", "CONTAIN"):
                        # For "IP" mode, action "IN" have 2 types of values.
                        #   - IPRange by netmask. example: "192.168.1.0/24"
                        #   - IPRange by dash or tilde. example: "192.168.1.1 - 192.168.1.254 or 192.168.1.1~192.168.1.254"
                        #
                        # Variable "netmask_compare_mode" used for distinguish them.
                        # If netmask_compare_mode is True, use "ip in ip_range" to compare.
                        # If False, use "start_ip <= ip <= end_ip" to compare.
                        if re.search(pattern["split_range"], options["value_a"]):
                            raise ValueError("For IP 'IN' or 'CONTAIN' compearison, value_a must not be a range but got '{}'".format(value_a))

                        runtime["value_a_object"] = netaddr.IPNetwork(options["value_a"])

                        runtime["value_b_elements"] = re.split(pattern["split_range"], options["value_b"])
                        runtime["value_b_element_objects"] = []
                        runtime["value_b_element_objects"].append(netaddr.IPNetwork(runtime["value_b_elements"][0]))
                        if len(runtime["value_b_elements"]) == 1:
                            pass
                        elif len(runtime["value_b_elements"]) == 2:
                            # secondary IP address is complete like 192.168.1.10 or 2000::2
                            if re.search(r"[:\.]", runtime["value_b_elements"][1]):
                                runtime["value_b_element_objects"].append(netaddr.IPNetwork(runtime["value_b_elements"][1]))
                            else:
                                # sometimes use "192.168.1.100-200", need re-creation end_ip to catenate from start_ip
                                runtime["value_b_element_objects"].append(netaddr.IPNetwork(
                                    re.search(r"(.*[\.\:])[0-9a-fA-F]", runtime["value_b_elements"][0]).group(1) + runtime["value_b_elements"][1]
                                ))
                        else:
                            raise ValueError("For IP 'IN' or 'CONTAIN' compearison, value_b must is IP Network, IP Range "
                                            "only have 1 or 2 elements but got '{}'".format(runtime["value_b_elements"]))

                        if len(runtime["value_b_element_objects"]) == 1:
                            return_value = bool(runtime["value_a_object"] in runtime["value_b_element_objects"][0])
                        else:
                            return_value = bool(runtime["value_b_element_objects"][0] <= runtime["value_a_object"] <= runtime["value_b_element_objects"][1])

                    elif options["action"] in ("EQ", "EQUAL"):
                        runtime["val_a_object"] = netaddr.IPNetwork(options["value_a"])
                        runtime["val_b_object"] = netaddr.IPNetwork(options["value_b"])
                        return_value = bool(runtime["val_a_object"] == runtime["val_b_object"])

                    elif options["action"] in ("NE", "NOT_EQUAL"):
                        runtime["val_a_object"] = netaddr.IPNetwork(options["value_a"])
                        runtime["val_b_object"] = netaddr.IPNetwork(options["value_b"])
                        return_value = bool(runtime["val_a_object"] != runtime["val_b_object"])

                    else:
                        raise ValueError("mode {} not support action {}".format(
                            options["mode"], options["action"]
                        ))

                except netaddr.AddrFormatError as err:
                    raise ValueError(err)

            if options["mode"] in ("INT", "INTEGER", "FLOAT", "NUMBER"):
                # Number range checking
                runtime["val_a_object"] = float(options["value_a"])
                if not re.search(pattern["split_range"], str(options["value_b"])):
                    runtime["val_b_object"] = float(options["value_b"])

                if options["action"] in ("IN", "CONTAIN"):
                    elements = re.split(pattern["split_range"], str(options["value_b"]))
                    if len(elements) == 1:
                        return_value = bool(runtime["val_a_object"] == float(elements[0]))
                    else:
                        return_value = bool(float(elements[0]) <= runtime["val_a_object"] <= float(elements[1]))

                elif options["action"] in ("EQ", "EQUAL"):
                    return_value = bool(runtime["val_a_object"] == runtime["val_b_object"])
                elif options["action"] in ("NE", "NOT_EQUAL"):
                    return_value = bool(runtime["val_a_object"] != runtime["val_b_object"])
                elif options["action"] in ("LT", "LESS_THAN"):
                    return_value = bool(runtime["val_a_object"] < runtime["val_b_object"])
                elif options["action"] in ("LE", "LESS_OR_EQUAL_THAN"):
                    return_value = bool(runtime["val_a_object"] <= runtime["val_b_object"])
                elif options["action"] in ("GT", "GREAT_THAN"):
                    return_value = bool(runtime["val_a_object"] > runtime["val_b_object"])
                elif options["action"] in ("GE", "GREAT_OR_EQUAL_THAN"):
                    return_value = bool(runtime["val_a_object"] >= runtime["val_b_object"])
                else:
                    raise ValueError("mode {} not support action {}".format(
                        options["mode"], options["action"]
                    ))

            if options["mode"] in ("STR", "STRING", "TEXT"):
                for value in (options["value_a"], options["value_b"]):
                    if not isinstance(value, str):
                        raise ValueError("'{}' not a STR".format(type(value)))

                runtime["val_a_object"] = str(options["value_a"])
                runtime["val_b_object"] = str(options["value_b"])
                if options["case_insensitive"] is True:
                    runtime["val_a_object"] = runtime["val_a_object"].upper()
                    runtime["val_b_object"] = runtime["val_b_object"].upper()

                if options["action"] in ("IN", "CONTAIN"):
                    return_value = bool(runtime["val_a_object"] in runtime["val_b_object"])
                elif options["action"] in ("EQ", "EQUAL", "EXACT"):
                    return_value = bool(runtime["val_a_object"] == runtime["val_b_object"])
                else:
                    raise ValueError("mode {} not support action {}".format(options["mode"], options["action"]))

            if options["mode"] in ("DATE", "TIME"):
                for value in (options["value_a"], options["value_b"]):
                    if not isinstance(value, str):
                        raise ValueError("'{}' not a STR".format(type(value)))

                date_format = "%Y-%m-%d %H:%M:%S"
                match = re.match(pattern["date_pattern"], options["value_a"].strip())
                if not match:
                    raise ValueError("DATE STRING must be 'YYYY-MM-DD HH:MM:SS'")

                # ignore other characters
                check_time = time.strptime(match.group(0), date_format)
                if options["action"] in ("IN", "CONTAIN"):
                    try:
                        start_time, end_time = re.split(r"\s*~\s*", options["value_b"].strip())
                        start_time = time.strptime(start_time, date_format)
                        end_time = time.strptime(end_time, date_format)
                    except ValueError as err:
                        raise ValueError("DATE STRING RANGE must separated by '~' and have 2 DATE STRING with 'start_time', 'end_time'")

                    return_value = start_time <= check_time <= end_time

                elif options["action"] in ("EQ", "EQUAL", "EXACT"):
                    return_value = bool(check_time == time.strptime(options["value_b"], date_format))
                elif options["action"] in ("NE", "NOT_EQUAL"):
                    return_value = bool(check_time != time.strptime(options["value_b"], date_format))
                elif options["action"] in ("LT", "LESS_THAN"):
                    return_value = bool(check_time < time.strptime(options["value_b"], date_format))
                elif options["action"] in ("LE", "LESS_OR_EQUAL_THAN"):
                    return_value = bool(check_time <= time.strptime(options["value_b"], date_format))
                elif options["action"] in ("GT", "GREAT_THAN"):
                    return_value = bool(check_time > time.strptime(options["value_b"], date_format))
                elif options["action"] in ("GE", "GREAT_OR_EQUAL_THAN"):
                    return_value = bool(check_time >= time.strptime(options["value_b"], date_format))
                else: # pragma: no cover
                    pass

        except BaseException as err:
            return_value = False
            if options["device"] is None:
                print(err)
            else:
                options["device"].log(message=err, level="INFO")

            if options["raise_exception"] is True:
                raise

        return return_value

    def get_user_values(self, default_value_mode_action_dict, user_value_dict, **kwargs):
        """According to default_value_mode_action_dict to get user values

        Main option is 'default_value_mode_action_dict', will loop this DICT and set options based on keyword.

        :param DICT default_value_mode_action_dict:
            **REQUIRED** default_value_mode_action_dict is a DICT that contain every keyword's default value, compare mode and default compare action.
            For example:

                default_value_mode_action_dict = {
                    # value: (default_value, default_check_mode, default_check_action)
                    "blk_high_port":        (None, "INT", "eq"),
                    "blk_low_port":         (None, "INT", "eq"),
                    "blk_internal_ip":      (None, "IP", "eq"),
                    "blk_ports_ol":         (None, "INT", "eq"),
                    "blk_ports_total":      (None, "INT", "eq"),
                    "blk_ports_used":       (None, "INT", "eq"),
                    "blk_reflexive_ip":     (None, "IP", "eq"),
                }

        :param DICT user_value_dict:
            **REQUIRED** user value from .robot or .py. For example:

                user_value_dict = {
                    "blk_high_port":        "1000 eq",
                    "blk_low_port":         (2000, "gt"),
                    "blk_internal_ip":      "192.168.100.1-192.168.100.20 in",
                    "blk_ports_ol":         ("100-200", "in"),
                    "blk_ports_total":      (3000, "eq"),
                    "strange_option:"       30,
                }

        :param unknown_keyword_value || unknown_keyword_mode || unknown_keyword_action:
            *OPTIONAL* if keyword in user_value_dict is not match any default_value_mode_action_dict entry, use this to set value, mode or action

                        default: unknown_keyword_value = None, unknown_keyword_mode = "STR", unknown_keyword_action = "eq"

        :param BOOL delete_value_none_keyword:
            *OPTIONAL* If set to True, will delete first value == None keyword. Default: False

        :return:
            According to above example, return DICT as below:

            **Notice: Action and Mode string will be transited to uppercase**

                return_value = {
                    "blk_high_port":        (1000, "INT", "EQ"),
                    "blk_low_port":         (2000, "INT", "GT"),
                    "blk_internal_ip":      ("192.168.100.1-192.168.100.20", "IP", "IN"),
                    "blk_ports_ol":         ("100-200", "INT", "IN"),
                    "blk_ports_total":      (3000, "INT", "EQ"),
                    "blk_ports_used":       (None, "INT", "EQ"),
                    "blk_reflexive_ip":     (None, "IP", "EQ"),
                    "strange_option":       (30, "STR", "EQ"),
                }

            But if delete_value_none_keyword == True, return:

                return_value = {
                    "blk_high_port":        (1000, "INT", "EQ"),
                    "blk_low_port":         (2000, "INT", "GT"),
                    "blk_internal_ip":      ("192.168.100.1-192.168.100.20", "IP", "IN"),
                    "blk_ports_ol":         ("100-200", "INT", "IN"),
                    "blk_ports_total":      (3000, "INT", "EQ"),
                    "strange_option":       (30, "STR", "EQ"),
                }
        """
        options = {}
        options["unknown_keyword_value"] = kwargs.get("unknown_keyword_value", None)
        options["unknown_keyword_mode"] = str(kwargs.get("unknown_keyword_mode", "STR")).strip().upper()
        options["unknown_keyword_action"] = str(kwargs.get("unknown_keyword_action", "EQ")).strip().upper()
        options["delete_value_none_keyword"] = self.check_boolean(kwargs.get("delete_value_none_keyword", False))

        all_user_options = {}
        for keyword in user_value_dict:
            element = []
            # if given value is None, just set all elements to default value
            if user_value_dict[keyword] is None:
                element.append(options["unknown_keyword_value"])
                element.append(options["unknown_keyword_mode"])
                element.append(options["unknown_keyword_action"])

            elif isinstance(user_value_dict[keyword], (str, int, float)):
                value, action = self.split_string_to_value_and_action(user_value_dict[keyword])
                element.append(value)

                if keyword in default_value_mode_action_dict:
                    element.append(default_value_mode_action_dict[keyword][1])

                    if action:
                        element.append(action)
                    else: # pragma: no cover
                        element.append(default_value_mode_action_dict[keyword][2])
                else:
                    element.append(options["unknown_keyword_mode"])
                    element.append(options["unknown_keyword_action"])

            elif isinstance(user_value_dict[keyword], (list, tuple)):
                element.append(user_value_dict[keyword][0])

                if keyword in default_value_mode_action_dict:
                    element.append(default_value_mode_action_dict[keyword][1])
                else:
                    element.append(options["unknown_keyword_mode"])

                element.append(user_value_dict[keyword][1])

            else:
                raise ValueError("Unknown given value: {}".format(user_value_dict[keyword]))

            element[1] = str(element[1]).strip().upper()
            element[2] = str(element[2]).strip().upper()
            all_user_options[keyword] = tuple(element)

        for keyword in default_value_mode_action_dict:
            if keyword not in all_user_options:
                all_user_options[keyword] = (
                    default_value_mode_action_dict[keyword][0],
                    str(default_value_mode_action_dict[keyword][1]).strip().upper(),
                    str(default_value_mode_action_dict[keyword][2]).strip().upper(),
                )

        if options["delete_value_none_keyword"] is True:
            new_user_options = copy.deepcopy(all_user_options)
            for keyword in new_user_options:
                if all_user_options[keyword][0] is None:
                    del all_user_options[keyword]
            del new_user_options

        return all_user_options

    @staticmethod
    def get_node_value(node_value, mode="STR"):
        """Return node name by STR or INT mode

        User may give node name by an INT (1), or STR ("1") or name ("node0"), but node name are different for CLI cmd and search re-name.
        For example, CLI cmd should tail "show security flow session node 0", but search flow session from "re-name" must be "node0".

        This method will transit user given value whatever 1, "1", or "node1" to "node1" if mode="STR", and 1 if mode="INT"
        """
        node_value = str(node_value).lower()
        mode = str(mode).upper()
        if node_value in ("0", "node0"):
            node_str = "node0"
            node_int = 0
        elif node_value in ("1", "node1"):
            node_str = "node1"
            node_int = 1
        else:
            raise ValueError("'node' must be 0, '0', node0, 1, '1' or node1, but got '{}'".format(node_value))

        if mode == "STR":
            return node_str

        return node_int

    @staticmethod
    def download_file_by_http(url, dst_path, username=None, password=None, verify=False):
        """Download file by HTTP or HTTPS

        :param STR url:
            **REQUIRED** download file url.

        :param STR dst_path:
            **REQUIRED** download file restore path.

        :param STR username:
            *OPTIONAL*  HTTPS username.

        :param STR password:
            *OPTIONAL*  HTTPS password

        :return:
            True/False for download succeed or failed
        """
        if username is not None and password is not None:
            if verify: # pragma: no cover
                request = requests.get(url, auth=(username, password), verify=certifi.where())
            else:
                request = requests.get(url, auth=(username, password))
        else:
            request = requests.get(url)

        if request.status_code != 200:
            print("Failed to download file from '{}'".format(url))
            return False

        with open(os.path.expanduser(dst_path), "wb") as fid:
            fid.write(request.content)

        return True

    @staticmethod
    def check_boolean(value):
        """Check boolean string or object"""
        value = str(value).strip().upper()

        if value == "TRUE":
            return_value = True
        elif value == "FALSE":
            return_value = False
        elif value == "NONE":
            return_value = None
        else:
            raise ValueError("Boolean string must be 'True', 'False' or 'None', but got '{}'".format(value))

        return return_value

    def flat_dict(self, dict_variable, **kwargs):
        """Transit complex dictionary to simple dictionary

        While a dictionary have complex structure (1+ keyword level, e.g: ["source-pool-address-range"]["address-range-low"]), it will transit to
        "source_pool_address_range_address_range_low". Action includes:

        +  2 level keywords separated by underline (_)
        +   keyword inner dash (-) will be replaced to underline (_) as well
        +   do lowercase transit for all keyword

        :param DICT dict_variable:
            **REQUIRED**  complex dictionary variable

        :param STR parent_key:
            *OPTIONAL*  prefix string before keyword. default=''. Example:

            ```python
            complex_dict = {"A": 1, "B": 2, "C": {"D": 3, "E": 4}}
            flat_dict(complex_dict, parent_key="my_")
            => {"my_a": 1, "my_b": 2, "my_c_d": 3, "my_c_e": 4}
            ```

        :param STR separate_char:
            *OPTIONAL*  middleware chars for each element. default="_". Example:

            ```python
            complex_dict = {"A": 1, "B": 2, "C": {"D": 3, "E": 4}}
            flat_dict(complex_dict, separate_char="%")
            => {"a": 1, "b": 2, "c%d": 3, "c%e": 4}
            ```

        :param BOOL lowercase:
            *OPTIONAL*  whether transit all keywords lowercase. default=True

        :param BOOL replace_dash_to_underline:
            *OPTIONAL*  whether replace all keywords dash char to underline char. default=True

        :return:
            dictionary
        """
        options = {}
        options["parent_key"] = kwargs.pop("parent_key", "")
        options["separate_char"] = kwargs.pop("separate_char", "_")
        options["lowercase"] = self.check_boolean(kwargs.pop("lowercase", True))
        options["replace_dash_to_underline"] = self.check_boolean(kwargs.pop("replace_dash_to_underline", True))

        items = []
        for key, value in dict_variable.items():
            key = key.strip()

            if options["lowercase"] is True:
                key = key.lower()

            if options["replace_dash_to_underline"] is True:
                key = key.replace(r"-", "_")

            new_key = options["separate_char"].join([options["parent_key"], key]) if options["parent_key"] else key
            if isinstance(value, collections.MutableMapping):
                items.extend(self.flat_dict(
                    dict_variable=value,
                    parent_key=new_key,
                    separate_char=options["separate_char"],
                    lowercase=options["lowercase"],
                    replace_dash_to_underline=options["replace_dash_to_underline"],
                ).items())
            else:
                items.append((new_key, value))

        return dict(items)


    def create_verify_filters(self, device, named_options, **kwargs):
        """Analyze user options to create verify filters

        This module have many "verify_" keyword that works on dynamic options. Here is an universal method to get all
        user options and create filter DICT as below then return.

            {
                "option_name_1": [filter_value, filter_action, filter_mode],
                "option_name_2": [filter_value, filter_action, filter_mode],
                ...
            }

        Below rules applied to create filters:

        +   For every named_options element, value must be a LIST, TUPLE, STRING or None.

        +   If value=None, will not applied to filter

        +   If value is STRING, will checking last word is an action word such as "eq", "ne", "ge", "gt", "le", "lt",
            etc.. If no action word found, set default action as below:

            -   STRING: in
            -   IPv4, IPv6 or NETWORK: eq
            -   INT, NUMBER, FLOAT: eq
            -   DATE: eq

        +   If value is INT, NUMBER or FLOAT, default action "eq" will be set

        +   For filter mode, will checking automatically. This mean set to "IP" if value string can be initiate by
            netaddr, or set to "INT" if can initiate by int() or float(), or a "DATE" if string looks like
            "2020-03-25 18:00:00". Default mode is "STR"

        :param DICT named_options:
            **REQUIRED** kwargs dict used to create filters. For example:

            {
                "in_src_addr": ["192.168.1.0/24", "in"],
                "in_dst_addr": "192.168.2.0/24 in",
                "in_src_port": "1024-65535 in",
                "in_dst_port": 21,
                "in_protocol": "tcp",
                "in_pkt_cnt": "10 gt",
            }

        :param BOOL align_re_name:
            *OPTIONAL* re_name always used to match HA setup response for each node, it can be set to 0, 1, node0 or
                       node1. Most time re_name value from device is node0/node1, so set this option True to transit
                       0, 1 to node0, node1 to avoid compare issue. default: True

        :param BOOL align_option_keyword:
            *OPTIONAL* Transit option keyword all lowercase and underscore. default: False

        :param BOOL skip_for_none:
            *OPTIONAL* If value=None, skip create this filter. default: True

        :param STR log_level:
            *OPTIONAL* Device log level. default: DEBUG

        :param BOOL debug_to_stdout:
            *OPTIONAL* whether print debug info to stdout. default: False

        :return: Return fiter DICT
        """
        options = {}
        options["align_re_name"] = self.check_boolean(kwargs.pop("align_re_name", True))
        options["align_option_keyword"] = self.check_boolean(kwargs.pop("align_option_keyword", False))
        options["skip_for_none"] = self.check_boolean(kwargs.pop("skip_for_none", True))
        options["log_level"] = kwargs.pop("log_level", "DEBUG")
        options["debug_to_stdout"] = self.check_boolean(kwargs.pop("debug_to_stdout", False))

        # option 'node' and 're_name' is special, they are alias for each other and may need transit to node string
        if options["align_re_name"] is True:
            if "node" in named_options:
                named_options["re_name"] = named_options.pop("node")

            if "re_name" in named_options:
                if named_options["re_name"] is None:
                    del named_options["re_name"]
                else:
                    named_options["re_name"] = self.get_node_value(named_options["re_name"], mode="STR")

        if options["align_option_keyword"] is True:
            new_named_options = {}
            for keyword in named_options:
                new_named_options[self.underscore_and_lowercase_transit(keyword)] = named_options[keyword]
            named_options = copy.deepcopy(new_named_options)
            del new_named_options

        filters = {}
        for keyword in sorted(named_options.keys()):
            if named_options[keyword] is None:
                if options["skip_for_none"] is True:
                    continue
                else:
                    named_options[keyword] = str(named_options[keyword])

            if isinstance(named_options[keyword], (tuple, list)):
                named_options[keyword] = "{} {}".format(str(named_options[keyword][0]), str(named_options[keyword][1]))

            if isinstance(named_options[keyword], str):
                filters[keyword] = self.split_string_to_value_and_action(
                    named_options[keyword],
                    with_mode=True,
                    default_mode="STR",
                )

            # If given value is integer or decimal, will checking by INT mode and always 'equal'
            elif isinstance(named_options[keyword], (int, float)):
                filters[keyword] = (str(named_options[keyword]), "EQ", "INT")

            else:
                raise TypeError("Value for each named options must be STR, INT, FLOAT, LIST, TUPLE or None, but got '{}'".format(
                    type(named_options[keyword])
                ))

        device.log(message="User filters:\n{}".format(self.pprint(filters)), level=options["log_level"])
        if options["debug_to_stdout"] is True:
            print("User filters:\n{}".format(self.pprint(filters)))

        return filters

    def filter_option_from_entry_list(self, device, filters, entries, **kwargs):
        """Normally filter behavior to checking entries

        This is a standardized behavior to check given entries whether match all filters

        :param DICT filters:
            **REQUIRED** filters which from method "create_verify_filters"

        :param LIST|TUPLE entries:
            **REQUIRED** entry list

        :param LIST|TUPLE compat_element_list:
            *OPTIONAL* element alias to support previous script. default: []

            compat_element_list = (
                # previous keyword, current_keyword
                ("session_id", "session_identifier"),
                ("session_timeout", "timeout"),
                ("node", "re_name"),
            )

        :param STR index_option:
            *OPTIONAL* index keyword to identify each entry. default: None

        :param BOOL debug_to_stdout:
            *OPTIONAL* print debug info to stdout. default: False

        :return:
            Return a LIST which contain all matched entries.
        """
        options = {}
        options["compat_element_list"] = kwargs.pop("compat_element_list", list())
        options["index_option"] = kwargs.pop("index_option", None)
        options["debug_to_stdout"] = kwargs.pop("debug_to_stdout", False)

        matched_entry_list = []
        for index, entry in enumerate(entries, start=1):
            for compat_element in options["compat_element_list"]:
                if compat_element[1] in entry:
                    entry[compat_element[0]] = entry[compat_element[1]]

            if options["index_option"] is not None and options["index_option"] in entry:
                index = "Element '{}={}'".format(options["index_option"], entry[options["index_option"]])
            else:
                index = "Entry '{}'".format(index)

            entry_matched = True

            for filter_keyword in filters:
                if filter_keyword not in entry:
                    msg = "{} is not contain '{}'".format(index, filter_keyword)
                    if options["debug_to_stdout"] is True:
                        print(msg)

                    device.log(message=msg, level="INFO")
                    entry_matched = False
                    continue

                value, action, mode = filters[filter_keyword]
                if mode in ("IP", "INT"):
                    status = self.do_compare(
                        device=device,
                        mode=mode,
                        action=action,
                        value_a=entry[filter_keyword],
                        value_b=value,
                        raise_exception=False,
                    )
                else:
                    status = self.do_compare(
                        device=device,
                        mode=mode,
                        action=action,
                        value_a=value,
                        value_b=entry[filter_keyword],
                        case_insensitive=True,
                        raise_exception=False,
                    )

                if status is False:
                    msg = "{} is not match option '{}': (device) {:>s} <==> {:<s} '{}' '{}' (user)".format(
                        index, filter_keyword, entry[filter_keyword], value, action, mode
                    )
                    if options["debug_to_stdout"] is True:
                        print(msg)

                    device.log(message=msg, level="INFO")
                    entry_matched = False

            if entry_matched is True:
                matched_entry_list.append(copy.deepcopy(entry))

        return matched_entry_list

    def print_result_table(self, device, filters, entries, **kwargs):
        """Print pretty result table

        :param DICT filters:
            **REQUIRED** User filters

        :param LIST|TUPLE entries:
            **REQUIRED** Matched entries shown in result table.

        :param STR index_option:
            *OPTIONAL* Index option string shown for match keyword. As default, will print auto-increase index number.
                       default: None

        :param INT max_column_width:
            *OPTIONAL* Max length for each column. default: 60

        :param STR log_level:
            *OPTIONAL* Log level. default: INFO

        :param BOOL debug_to_stdout:
            *OPTIONAL* Print to stdout for debugging. default: False

        :return: Return pretty table structure
        """
        options = {}
        options["index_option"] = kwargs.pop("index_option", None)
        options["max_column_width"] = int(kwargs.pop("max_column_width", 60))
        options["blank_char"] = str(kwargs.pop("blank_char", "-"))
        options["log_level"] = str(kwargs.pop("log_level", "INFO")).strip().upper()
        options["debug_to_stdout"] = self.check_boolean(kwargs.pop("debug_to_stdout", False))

        messages = []
        title_list = ("OPTION", "ON DEVICE", "USER WANT", "ACTION", "MODE")
        for entry_index, entry in enumerate(entries, start=1):
            if options["index_option"] is None or options["index_option"] not in entry:
                messages.append("Match entry '{}':".format(entry_index))
            else:
                messages.append("Match '{}={}':".format(options["index_option"], entry[options["index_option"]]))

            line_list = []
            for option_name in entry:
                user_value = str(filters[option_name][0]) if option_name in filters else options["blank_char"]
                user_action = str(filters[option_name][1]) if option_name in filters else options["blank_char"]
                user_mode = str(filters[option_name][2]) if option_name in filters else options["blank_char"]
                line_list.append((option_name, entry[option_name], user_value, user_action, user_mode))

            # got every element max length for pretty print result
            length = {}
            for index, title in enumerate(title_list):
                length[title_list[index]] = 0
                for line in line_list:
                    length[title_list[index]] = max(len(str(line[index])), length[title_list[index]])

            for title in title_list:
                if length[title] < len(title):
                    length[title] = len(title)

                if length[title] > options["max_column_width"]:
                    length[title] = options["max_column_width"]

            # table title
            messages.append("    | {} | {} | {} | {} | {} |".format(
                title_list[0].center(length[title_list[0]]),
                title_list[1].center(length[title_list[1]]),
                title_list[2].center(length[title_list[2]]),
                title_list[3].center(length[title_list[3]]),
                title_list[4].center(length[title_list[4]]),
            ))
            messages.append("    | {} | {} | {} | {} | {} |".format(
                "-" * length[title_list[0]],
                "-" * length[title_list[1]],
                "-" * length[title_list[2]],
                "-" * length[title_list[3]],
                "-" * length[title_list[4]],
            ))

            for line in line_list:
                messages.append("    | {} | {} | {} | {} | {} |".format(
                    str(line[0]).ljust(length[title_list[0]]),
                    str(line[1]).ljust(length[title_list[1]]),
                    str(line[2]).ljust(length[title_list[2]]),
                    str(line[3]).ljust(length[title_list[3]]),
                    str(line[4]).ljust(length[title_list[4]]),
                ))

            messages.append("")

        for msg in messages:
            device.log(message=msg, level=options["log_level"])
            if options["debug_to_stdout"] is True:
                print(msg)

        return messages
