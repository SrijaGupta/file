# coding: UTF-8
"""Have all security log module methods"""
# pylint: disable=invalid-name
__author__ = ['Joyce Zhu', 'Jon Jiang']
__contact__ = ['joycezhu@juniper.net', 'jonjiang@juniper.net']
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import time

from jnpr.toby.utils.message import message
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.junos.dut_tool import dut_tool
"""Device related methods

Below options are have same behavior:

+   device (Object) - Device handler
"""

class security_logging(message):
    """All SYSLOG related methods"""

    def __init__(self):
        """Init processing"""
        super().__init__()
        self.xml = xml_tool()
        self.tool = flow_common_tool()
        self.dut = dut_tool()

        self.default = {
            "cli_show_timeout":     300,
            "conf_commit_timeout":  300,
        }

    def get_and_check_security_log_report_summary(self, device, **kwargs):
        """Get security log report in-interval result

        :param Device device:
        **REQUIRED** Handle of the device on which commands have to be executed.

        :param str type:
            *OPTIONAL* Type keyword that one of 'idp', 'session-all', etc... or 'all'

        :param str option:
            *OPTIONAL* Option keyword that could input any option

        :param str number:
            *OPTIONAL* Number keyword that the number of summary result

        :return: Return a dict value which contain all elements, or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())

        all_option_list = (
            "type", "number","option",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)
        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])

        # send command to device and get response
        cmd_element_list = ["show security log report summary ", ]
        if options['type'] is not None:
            cmd_element_list.append("{}".format(options['type']))
        if options['option'] is not None:
            cmd_element_list.append("{}".format(options['option']))

        cmd = " ".join(cmd_element_list)
        self.display(level="info", msg=cmd)
        response = self.dut.send_cli_cmd(
            device=device,
            cmd=cmd,
            format="xml",
            channel="pyez",
            #channel="text",
            timeout=options["timeout"],
        )

        if not response:
            return False
        response = response['security-log-report-summary']['security-log-report-summary-total-count']
#         if isinstance(number,str):
#             number = int(number)
#         if isinstance(response,str):
#             response = int(response)
        if options['number'] == response:
            self.display(level="info", msg="Summary options['type'] count is {}, correct".format(response))
        else:
            self.display(level="info", msg="!!Summary options['type'] count is {}, NOT correct, should be {} ".format(response, options['number']))
            return False

        return True







    def get_security_log_report_in_interval(self, device, **kwargs):
        """Get security log report in-interval result

        :param Device device:
        **REQUIRED** Handle of the device on which commands have to be executed.

        :param str type:
            *OPTIONAL* Type keyword that one of 'idp', 'session-all', etc...

        :param str start_time:
            *OPTIONAL* Start-time keyword that 'YYYY-MM-DDTHH:MM:SS'.

        :param str stop_time:
            *OPTIONAL* Stop-time keyword that 'YYYY-MM-DDTHH:MM:SS'.

        :param str option:
            *OPTIONAL* Option keyword that could input any option


        :return: Return a dict value which contain all elements, or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())

        all_option_list = (
            "type", "start_time", "stop_time","option",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)
        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])

        # send command to device and get response
        cmd_element_list = ["show security log report in-interval ", ]
        if options['type'] is not None:
            cmd_element_list.append("{}".format(options['type']))

        if options['start_time'] is not None:
            cmd_element_list.append("start-time {}".format(options['start_time']))

        if options['stop_time'] is not None:
            cmd_element_list.append("stop-time {}".format(options['stop_time']))

        if options['option'] is not None:
            cmd_element_list.append("{}".format(options['option']))

        cmd = " ".join(cmd_element_list)
        self.display(level="info", msg=cmd)
        response = self.dut.send_cli_cmd(
            device=device,
            cmd=cmd,
            format="xml",
            channel="pyez",
            #channel="text",
            timeout=options["timeout"],
        )

        if not response:
            return False
        if response['security-log-report-in-interval'] == '':
            self.display(level="INFO", msg="return value: {}".format(response))
            return response
        else:
            response = response['security-log-report-in-interval']['security-log-report-in-interval-entry']
            self.display(level="INFO", msg="return value: {}".format(response))
            return response

    def compare_security_log_report_in_interval(self, **kwargs):
        """Compare the security log report top result

        :param str content:
            *OPTIONAL* Content keyword that is the result get from keywords get_security_log_report_top

        :param str time:
            *OPTIONAL* Time keyword that the input of detail time.

        :param str denied_number:
            *OPTIONAL* Denied_number keyword that the input of detail denied number.

        :param str all_number:
            *OPTIONAL* All-number keyword that the input of detail all number.

        :return: Return True or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())
        all_option_list = (
            "content", "time", "denied_number", "all_number",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)

        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])


        i = 0
        j = 0

        for content_detail in options['content']:
            get_time = content_detail['security-log-report-in-interval-time']
            self.display(level="info", msg="Find security-log-report-in-interval-time = {}".format(get_time))
            if get_time == options['time'][i]:
                self.display(level="info", msg="Time intervals {} is correct".format(get_time))
            else:
                self.display(level="info", msg="!!Time intervals {} is wrong, should be {}".format(get_time, options['time'][i]))
                j = j+1

            get_denied_number = content_detail['security-log-report-in-interval-denied']
            self.display(level="info", msg="Find security-log-report-in-interval-denied = {}".format(get_denied_number))
            if get_denied_number == options['denied_number'][i]:
                self.display(level="info", msg="Blocked/Denied events {} is correct".format(get_denied_number))
            else:
                self.display(level="info", msg="!!Blocked/Denied events {} is wrong, should be {}".format(get_denied_number, options['denied_number'][i]))
                j = j+1
            get_all_number = content_detail['security-log-report-in-interval-all']
            self.display(level="info", msg="Find security-log-report-in-interval-all = {}".format(get_all_number))
            if get_all_number == options['all_number'][i]:
                self.display(level="info", msg="All events {} is correct".format(get_all_number))
            else:
                self.display(level="info", msg="!!All events  {} is wrong, should be {}".format(get_all_number, options['all_number'][i]))
                j = j+1
            i = i+1
        if j != 0:
            return False
        return True


    def get_security_log_report_top(self, device, **kwargs):
        """Get security log report top result

        :param Device device:
        **REQUIRED** Handle of the device on which commands have to be executed.

        :param str type:
            *OPTIONAL* Type keyword that one of 'idp', 'session-all', etc..., or just give 'all'

        :param int top_number:
            *OPTIONAL* Get top-number number

        :param str group_by:
            *OPTIONAL* Group-by keyword that one of 'event-type', 'application', etc.

        :param str order_by:
            *OPTIONAL* Order-by keyword that one of 'count', 'user-number', etc.

        :param str exist:
            *OPTIONAL* Exist keyword that should be 'yes', 'no'.

        :param str with_var:
            *OPTIONAL* with_var keyword that one of 'application' or 'user'.

        :param str ascending:
            *OPTIONAL* Ascending keyword that 'ascending'.

        :param str start_time:
            *OPTIONAL* Start-time keyword that 'YYYY-MM-DDTHH:MM:SS'.

        :param str stop_time:
            *OPTIONAL* Stop-time keyword that 'YYYY-MM-DDTHH:MM:SS'.

        :param str where_action:
            *OPTIONAL* Where-action keyword that  one of 'block' or 'permit'..

        :param str where_application:
            *OPTIONAL* Where-application keyword that 'http'.

        :param str option:
            *OPTIONAL* Option keyword that could input any option

        :return: Return a dict value which contain all elements, or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())

        all_option_list = (
            "type", "top_number", "group_by", "order_by", "exist", "with_var", "ascending",
            "start_time", "stop_time", "where_action", "where_application","option",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)
        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])


        # send command to device and get response
        cmd_element_list = ["show security log report top", ]
        if options['type'] is not None:
            cmd_element_list.append("{}".format(options['type']))

        if options['top_number'] is not None:
            cmd_element_list.append("top-number {}".format(options['top_number']))

        if options['group_by'] is not None:
            cmd_element_list.append("group-by {}".format(options['group_by']))

        if options['order_by'] is not None:
            cmd_element_list.append("order-by {}".format(options['order_by']))

        if options['with_var'] is not None:
            cmd_element_list.append("with {}".format(options['with_var']))

        if options['ascending'] is not None:
            cmd_element_list.append("{}".format(options['ascending']))

        if options['start_time'] is not None:
            cmd_element_list.append("start-time {}".format(options['start_time']))

        if options['stop_time'] is not None:
            cmd_element_list.append("stop-time {}".format(options['stop_time']))

        if options['where_action'] is not None:
            cmd_element_list.append("where-action {}".format(options['where_action']))

        if options['where_application'] is not None:
            cmd_element_list.append("where-application {}".format(options['where_application']))

        if options['option'] is not None:
            cmd_element_list.append("{}".format(options['option']))

        cmd = " ".join(cmd_element_list)
        self.display(level="info", msg=cmd)
        response = self.dut.send_cli_cmd(
            device=device,
            cmd=cmd,
            format="xml",
            channel="pyez",
            #channel="text",
            timeout=options["timeout"],
        )

        if not response:
            return False

        response = response['security-log-report-top']
        self.display(level="info", msg=response)
        if options['exist'] == "yes":
            if 'security-log-report-top-entry' not in response:
                return False
            response = response['security-log-report-top-entry']
            self.display(level="INFO", msg="return value: {}".format(response))
            return response
        elif options['exist'] == "no":
            for i in range(1, 3):
                response = self.dut.send_cli_cmd(
                    device=device,
                    cmd=cmd,
                    format="xml",
                    channel="pyez",
                    #channel="text",
                    timeout=options["timeout"],
                )
                response = response['security-log-report-top']
                if 'security-log-report-top-entry' in response:
                    self.display(level="info", msg="Find security-log-report-top-entry, should NOT find it, will sleep 3 secs")
                    time.sleep(3)
                else:
                    return True

            response = self.dut.send_cli_cmd(
                device=device,
                cmd=cmd,
                format="xml",
                channel="pyez",
                #channel="text",
                timeout=options["timeout"],
            )

            response = response['security-log-report-top']
            if 'security-log-report-top-entry' in response:
                return False
            else:
                return True
        else:
            self.display(level="info", msg="Parameter exist input is wrong, should be yes or no.")
            return False


    def compare_security_log_report_top(self, **kwargs):
        """Compare the security log report top result

        :param str content:
            *OPTIONAL* Content keyword that is the result get from keywords get_security_log_report_top

        :param str header_name:
            *OPTIONAL* Header-name keyword that the input of detail header name.

        :param str packet:
            *OPTIONAL* Packet keyword that the input of detail packet number.

        :param str user_number:
            *OPTIONAL* User-number keyword that the input of detail user number.

        :param str count:
            *OPTIONAL* Count keyword that the input of detail count.

        :param str volume:
            *OPTIONAL* Volume keyword that the input of detail volume.

        :param str order:
            *OPTIONAL* Order keyword that one of 'descending' or 'ascending'.

        :param str app:
            *OPTIONAL* App keyword that the input of detail app.

        :param str user:
            *OPTIONAL* User keyword that the input of detail user.

        :param str user_volume:
            *OPTIONAL* User-volume keyword that the input of detail user-volume.

        :param str user_count:
            *OPTIONAL* User-count keyword that the input of detail user-count.

        :param str app_volume:
            *OPTIONAL* App-volume keyword that the input of detail app-volume.

        :param str app_count:
            *OPTIONAL* App-count keyword that the input of detail app-count.

        :param str order_by:
            *OPTIONAL* Order-by keyword that one of 'count', 'volume', etc.

        :return: Return True or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())
        all_option_list = (
            "content", "header_name", "packet", "user_number", "count", "volume", "order", "app", "user", "user_volume",
            "user_count", "app_volume", "app_count", "order_by",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)

        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])


        i = 0
        j = 0
        content_detail = options['content']
        header_name_detail = options['header_name']
        pkt_detail = options['packet']
        volume_detail = options['volume']
        count_detail = options['count']
        order_detail = options['order']
        app_detail = options['app']
        user_detail = options['user']
        user_volume_detail = options['user_volume']
        user_count_detail = options['user_count']
        app_volume_detail = options['app_volume']
        app_count_detail = options['app_count']
        order_by_detail = options['order_by']


        if order_detail is None:
            order_detail = "descending"

        if isinstance(content_detail, dict):
            if header_name_detail is not None:
                get_header_name = content_detail['security-log-report-top-header']
                self.display(level="info", msg="Find security-log-report-top-header = {}".format(get_header_name))
                if get_header_name == header_name_detail[0]:
                    self.display(level="info", msg="Header name {} is correct".format(get_header_name))
                else:
                    self.display(level="info", msg="!!Header name {} is wrong, should be {}".format(get_header_name, header_name_detail[0]))
                    j = j+1
                    #return False

            if count_detail is not None:
                get_count_detail = content_detail['security-log-report-top-count']
                self.display(level="info", msg="Find security-log-report-top-counter = {}".format(get_count_detail))
                if isinstance(count_detail[0], int):
                    count_detail[0] = str(count_detail[0])
                if get_count_detail == count_detail[0]:
                    self.display(level="info", msg="Count {} is correct".format(get_count_detail))
                    if order_by_detail == "count" and get_count_detail != "-":
                        self.display(level="info", msg="Count is {} order, correct".format(order_detail))
                else:
                    self.display(level="info", msg="!!Count {} is NOT correct, should be {} ".format(get_count_detail, count_detail[0]))
                    j = j+1
                    #return False
                    if order_by_detail == "count" and get_count_detail != "-":
                        self.display(level="info", msg="!!Count is NOT {} order".format( order_detail))
                        j = j+1
                        #return False

            if pkt_detail is not None:
                get_pkt_detail = content_detail['security-log-report-top-packet']
                self.display(level="info", msg="Find security-log-report-top-packet = {}".format(get_pkt_detail))
                if isinstance(pkt_detail[0], int):
                    pkt_detail[0] = str(pkt_detail[0])
                if get_pkt_detail == pkt_detail[0]:
                    self.display(level="info", msg="Packet {} is correct".format(get_pkt_detail))
                    if order_by_detail == "packet" and get_pkt_detail != "-":
                        self.display(level="info", msg="Packet is {} order, correct".format(order_detail))
                else:
                    self.display(level="info", msg="!!Packet {} is NOT correct, should be {} ".format(get_pkt_detail, pkt_detail[0]))
                    j = j+1
                    #return False
                    if order_by_detail == "packet" and get_pkt_detail != "-":
                        self.display(level="info", msg="!!Packet is NOT {} order".format(order_detail))
                        j = j+1
                        #return False
            if options['user_number'] is not None:
                get_user_number_detail = content_detail['security-log-report-top-usernumber']
                self.display(level="info", msg="Find security-log-report-top-usernumber = {}".format(get_user_number_detail))
                if isinstance(options['user_number'][0], int):
                    options['user_number'][0] = str(options['user_number'][0])
                if get_user_number_detail == options['user_number'][0]:
                    self.display(level="info", msg="User number {} is correct".format(get_user_number_detail))
                else:
                    self.display(level="info", msg="!!User number {} is NOT correct, should be {} ".format(get_user_number_detail, options['user_number'][0]))
                    j = j+1


            if volume_detail is not None:
                get_volume_detail = content_detail['security-log-report-top-volume']
                self.display(level="info", msg="Find security-log-report-top-volume = {}".format(get_volume_detail))
                if get_volume_detail == volume_detail[0]:
                    self.display(level="info", msg="Volume {} is correct".format(get_volume_detail))
                    if order_by_detail == "volume" and get_count_detail != "-":
                        self.display(level="info", msg="Volume is {} order, correct".format(order_detail))
                else:
                    self.display(level="info", msg="!!Volume {} is wrong, should be {}".format(get_volume_detail, volume_detail[0]))
                    j = j+1
                    #return False
                    if order_by_detail == "volume" and get_count_detail != "-":
                        self.display(level="info", msg="!!Volume is NOT {} order".format(order_detail))
                        j = j+1

            if app_detail is not None:
                get_app_detail = content_detail['security-log-report-top-app']
                self.display(level="info", msg="Find security-log-report-top-app = {}".format(get_app_detail))
                if get_app_detail == app_detail[0]:
                    self.display(level="info", msg="Application {} is correct".format(get_app_detail))
                else:
                    self.display(level="info", msg="!!Application {} is wrong, should be {}".format(get_app_detail, app_detail[0]))
                    j = j+1

            if user_detail is not None:
                get_user_detail = content_detail['security-log-report-top-user']
                self.display(level="info", msg="Find security-log-report-top-user = {}".format(get_user_detail))
                if get_user_detail == user_detail[0]:
                    self.display(level="info", msg="User {} is correct".format(get_user_detail))
                else:
                    self.display(level="info", msg="!!User {} is wrong, should be {}".format(get_user_detail, user_detail[0]))
                    j = j+1

            if user_volume_detail is not None:
                get_user_volume_detail = content_detail['security-log-report-top-user-volume']
                self.display(level="info", msg="Find security-log-report-top-user-volume = {}".format(get_user_volume_detail))
                if get_user_volume_detail == user_volume_detail[0]:
                    self.display(level="info", msg="User volume {} is correct".format(get_user_volume_detail))
                else:
                    self.display(level="info", msg="!!User volume {} is wrong, should be {}".format(get_user_volume_detail, user_volume_detail[0]))
                    j = j+1

            if user_count_detail is not None:
                get_user_count_detail = content_detail['security-log-report-top-user-count']
                self.display(level="info", msg="Find security-log-report-top-user-count = {}".format(get_user_count_detail))
                if isinstance(user_count_detail[0], int):
                    user_count_detail[0] = str(user_count_detail[0])
                if get_user_count_detail == user_count_detail[0]:
                    self.display(level="info", msg="User count {} is correct".format(get_user_count_detail))
                else:
                    self.display(level="info", msg="!!User count {} is wrong, should be {}".format(get_user_count_detail, user_count_detail[0]))
                    j = j+1

            if app_volume_detail is not None:
                get_app_volume_detail = content_detail['security-log-report-top-app-volume']
                self.display(level="info", msg="Find security-log-report-top-app-volume = {}".format(get_app_volume_detail))
                if get_app_volume_detail == app_volume_detail[0]:
                    self.display(level="info", msg="Application volume {} is correct".format(get_app_volume_detail))
                else:
                    self.display(level="info", msg="!!Application volume {} is wrong, should be {}".format(get_app_volume_detail, app_volume_detail[0]))
                    j = j+1

            if app_count_detail is not None:
                get_app_count_detail = content_detail['security-log-report-top-app-count']
                self.display(level="info", msg="Find security-log-report-top-app-counter = {}".format(get_app_count_detail))
                if isinstance(app_count_detail[0], int):
                    app_count_detail[0] = str(app_count_detail[0])
                if get_app_count_detail == app_count_detail[0]:
                    self.display(level="info", msg="Application count {} is correct".format(get_app_count_detail))
                else:
                    self.display(level="info", msg="!!Application count {} is wrong, should be {}".format(get_app_count_detail, app_count_detail[0]))
                    j = j+1

        else:

            for a in content_detail:

                if header_name_detail is not None:
                    get_header_name = a['security-log-report-top-header']
                    self.display(level="info", msg="Find security-log-report-top-header = {}".format(get_header_name))
                    if get_header_name == header_name_detail[i]:
                        self.display(level="info", msg="Header name {} is correct".format(get_header_name))
                    else:
                        self.display(level="info", msg="!!Header name {} is wrong, should be {}".format(get_header_name, header_name_detail[i]))
                        j = j+1

                if count_detail is not None:
                    get_count_detail = a['security-log-report-top-count']
                    self.display(level="info", msg="Find security-log-report-top-counter = {}".format(get_count_detail))
                    if isinstance(count_detail[i], int):
                        count_detail[i] = str(count_detail[i])
                    if get_count_detail == count_detail[i]:
                        self.display(level="info", msg="Count {} is correct".format(get_count_detail))
                        if order_by_detail == "count" and get_count_detail != "-":
                            self.display(level="info", msg="Count is {} order, correct".format(order_detail))
                    else:
                        self.display(level="info", msg="!!Count {} is NOT correct, should be {} ".format(get_count_detail, count_detail[i]))
                        j = j+1
                        if order_by_detail == "count" and get_count_detail != "-":
                            self.display(level="info", msg="!!Count is NOT {} order".format(order_detail))
                            j = j+1

                if pkt_detail is not None:
                    get_pkt_detail = a['security-log-report-top-packet']
                    self.display(level="info", msg="Find security-log-report-top-packet = {}".format(get_pkt_detail))
                    if isinstance(pkt_detail[i], int):
                        pkt_detail[i] = str(pkt_detail[i])
                    if get_pkt_detail == pkt_detail[i]:
                        self.display(level="info", msg="Packet {} is correct".format(get_pkt_detail))
                        if order_by_detail == "packet" and get_pkt_detail != "-":
                            self.display(level="info", msg="Packet is {} order, correct".format(order_detail))
                    else:
                        self.display(level="info", msg="!!Packet {} is NOT correct, should be {} ".format(get_pkt_detail, pkt_detail[i]))
                        j = j+1
                        if order_by_detail == "packet" and get_pkt_detail != "-":
                            self.display(level="info", msg="!!Packet is NOT {} order".format(order_detail))
                            j = j+1
                if options['user_number'] is not None:
                    get_user_number_detail = a['security-log-report-top-usernumber']
                    self.display(level="info", msg="Find security-log-report-top-usernumber = {}".format(get_user_number_detail))
                    if isinstance(options['user_number'][i], int):
                        options['user_number'][i] = str(options['user_number'][i])
                    if get_user_number_detail == options['user_number'][i]:
                        self.display(level="info", msg="User number {} is correct".format(get_user_number_detail))
                    else:
                        self.display(level="info", msg="!!User number {} is NOT correct, should be {} ".format(get_user_number_detail, options['user_number'][i]))
                        j = j+1

                if volume_detail is not None:
                    get_volume_detail = a['security-log-report-top-volume']
                    self.display(level="info", msg="Find security-log-report-top-volume = {}".format(get_volume_detail))
                    if get_volume_detail == volume_detail[i]:
                        self.display(level="info", msg="Volume {} is correct".format(get_volume_detail))
                        if order_by_detail == "volume" and get_count_detail != "-":
                            self.display(level="info", msg="Volume is {} order, correct".format(order_detail))
                    else:
                        self.display(level="info", msg="!!Volume {} is wrong, should be {}".format(get_volume_detail, volume_detail[i]))
                        j = j+1
                        #return False
                        if order_by_detail == "volume" and get_count_detail != "-":
                            self.display(level="info", msg="!!Volume is NOT {} order".format(order_detail))
                            j = j+1
                            #return False

                if app_detail is not None:
                    get_app_detail = a['security-log-report-top-app']
                    self.display(level="info", msg="Find security-log-report-top-app = {}".format(get_app_detail))
                    if get_app_detail == app_detail[i]:
                        self.display(level="info", msg="Application {} is correct".format(get_app_detail))
                    else:
                        self.display(level="info", msg="!!Application {} is wrong, should be {}".format(get_app_detail, app_detail[i]))
                        j = j+1
                        #return False

                if user_detail is not None:
                    get_user_detail = a['security-log-report-top-user']
                    self.display(level="info", msg="Find security-log-report-top-user = {}".format(get_user_detail))
                    if get_user_detail == user_detail[i]:
                        self.display(level="info", msg="User {} is correct".format(get_user_detail))
                    else:
                        self.display(level="info", msg="!!User {} is wrong, should be {}".format(get_user_detail, user_detail[i]))
                        j = j+1
                        #return False

                if user_volume_detail is not None:
                    get_user_volume_detail = a['security-log-report-top-user-volume']
                    self.display(level="info", msg="Find security-log-report-top-user-volume = {}".format(get_user_volume_detail))
                    if get_user_volume_detail == user_volume_detail[i]:
                        self.display(level="info", msg="User volume {} is correct".format(get_user_volume_detail))
                    else:
                        self.display(level="info", msg="!!User volume {} is wrong, should be {}".format(get_user_volume_detail, user_volume_detail[i]))
                        j = j+1
                        #return False

                if user_count_detail is not None:
                    get_user_count_detail = a['security-log-report-top-user-count']
                    self.display(level="info", msg="Find security-log-report-top-user-count = {}".format(get_user_count_detail))
                    if isinstance(user_count_detail[i], int):
                        user_count_detail[i] = str(user_count_detail[i])
                    if get_user_count_detail == user_count_detail[i]:
                        self.display(level="info", msg="User count {} is correct".format(get_user_count_detail))
                    else:
                        self.display(level="info", msg="!!User count {} is wrong, should be {}".format(get_user_count_detail, user_count_detail[i]))
                        j = j+1
                        #return False

                if app_volume_detail is not None:
                    get_app_volume_detail = a['security-log-report-top-app-volume']
                    self.display(level="info", msg="Find security-log-report-top-app-volume = {}".format(get_app_volume_detail))
                    if get_app_volume_detail == app_volume_detail[i]:
                        self.display(level="info", msg="Application volume {} is correct".format(get_app_volume_detail))
                    else:
                        self.display(level="info", msg="!!Application volume {} is wrong, should be {}".format(get_app_volume_detail, app_volume_detail[i]))
                        j = j+1
                        #return False

                if app_count_detail is not None:
                    get_app_count_detail = a['security-log-report-top-app-count']
                    self.display(level="info", msg="Find security-log-report-top-app-counter = {}".format(get_app_count_detail))
                    if isinstance(app_count_detail[i], int):
                        app_count_detail[i] = str(app_count_detail[i])
                    if get_app_count_detail == app_count_detail[i]:
                        self.display(level="info", msg="Application count {} is correct".format(get_app_count_detail))
                    else:
                        self.display(level="info", msg="!!Application count {} is wrong, should be {}".format(get_app_count_detail, app_count_detail[i]))
                        j = j+1
                        #return False
                i = i+1
        if j != 0:
            return False
        return True

    def calculate_volume(self, **kwargs):
        """Compare the security log report top result

        :param str count:
            *OPTIONAL* Count keyword that is the input counter

        :param str wing1_volume:
            *OPTIONAL* Wing1_volume keyword that the input of wing1 volume.

        :return: Return True or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())
        all_option_list = (
            "count", "wing1_volume",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)

        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])
        volume_list = []
        i = 0
        tail = ".000000"
        if options['wing1_volume'] is None:
            options['wing1_volume'] = "1024"
        for count_detail in options['count']:
            if count_detail == "-":
                volume_detail = "-"
                volume_list.append(volume_detail)
                self.display(level="info", msg=volume_list[i])
            else:
                volume_detail = int(count_detail)*int(options['wing1_volume'])
                #volume_detail = str(volume_detail)
                volume_list.append("{}{}".format(volume_detail, tail))
                self.display(level="info", msg=volume_list[i])
            i = i+1

        return volume_list

    def count_list_calculate(self, **kwargs):
        """Compare the security log report top result

        :param str count_list:
            *OPTIONAL* Count list keyword that is the input of count list

        :param str user:
            *OPTIONAL* User keyword that the input of expected user name.

        :param str application:
            *OPTIONAL* Application keyword that the input of expected application name.

        :param str return_argu:
            *OPTIONAL* Return_argu keyword that the input of expected return content, one of 'total_count' or 'user_count' or 'app_count'.

        :return: Return True or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())
        all_option_list = (
            "count_list", "user", "application", "return_argu",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)

        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])
        count_list_detail = []
        count_with_line = []
        count = 0
        i = 0
        j = -1
        counter = 0
        for count_detail in options['count_list']:
            if isinstance(count_detail, int):
                m = i+1
                n = i+2
                if options['count_list'][m] == options['user']:
                    count = count+count_detail
                    self.display(level="info", msg="count_user={}".format(count))
                    count_list_detail.append(count_detail)
                    j = j+1
                if options['count_list'][n] == options['application']:
                    count = count+count_detail
                    self.display(level="info", msg="count_app={}".format(count))
                    count_list_detail.append(count_detail)
                    j = j+1
                i = i+1
            else:
                i = i+1
                continue
        count_list_detail.sort(reverse=True)
        count_with_line.append(count)
        while counter < j:
            count_with_line.append("-")
            counter = counter+1
        if options['return_argu'] == "total_count":
            self.display(level="info", msg=count_with_line)
            return count_with_line
        elif options['return_argu'] == "user_count" or options['return_argu'] == "app_count":
            self.display(level="info", msg=count_list_detail)
            return count_list_detail
        else:
            return False

    def get_security_log_report_in_detail(self, device, **kwargs):
        """Get security log report in-detail result

        :param Device device:
        **REQUIRED** Handle of the device on which commands have to be executed.

        :param str type:
            *OPTIONAL* Type keyword that one of 'all', 'session-all', etc..., or just give 'all'

        :param str category:
            *OPTIONAL* Category keyword that one of 'idp', 'session-all', etc..., or just give 'all'

        :param str source_address:
            *OPTIONAL* Source_address keyword that input of source address

        :param str source_zone:
            *OPTIONAL* Source_zone keyword that input of source zone

        :param str source_interface:
            *OPTIONAL* Source_interface keyword that input of source interface

        :param str destination_address:
            *OPTIONAL* Destination_address keyword that input of destination address

        :param str threat_severity:
            *OPTIONAL* Threat-severity keyword that input of threat-severity

        :param int count:
            *OPTIONAL* Get count number

        :param str reason:
            *OPTIONAL* Reason keyword that one of 'TESTSPAM', etc.

        :param str service:
            *OPTIONAL* Service keyword that input of service.

        :param str url:
            *OPTIONAL* URL keyword that input of url.

        :param str role:
            *OPTIONAL* Role keyword that input of role.

        :param str profile:
            *OPTIONAL* Profile keyword that input of profile.

        :param str protocol:
            *OPTIONAL* Protocol keyword that input of protocol.

        :param str policy_name:
            *OPTIONAL* Policy-name keyword that input of policy-name.

        :param str rule_name:
            *OPTIONAL* Rule-name keyword that input of rule-name.

        :param str nested_application:
            *OPTIONAL* Nested-application keyword input of nested-application.

        :param str operation:
            *OPTIONAL* Operation keyword that one of 'or' or 'and'.

        :param str application:
            *OPTIONAL* Application keyword input of application.

        :param str user:
            *OPTIONAL* User keyword input of user name.

        :param str source_name:
            *OPTIONAL* Source-name keyword that the input of detail source_name.

        :param str event_type:
            *OPTIONAL* Event_type keyword that the input of detail event_type.

        :param str start_from:
            *OPTIONAL* Start-from keyword that input of the log index.

        :param str start_time:
            *OPTIONAL* Start-time keyword that 'YYYY-MM-DDTHH:MM:SS'.

        :param str stop_time:
            *OPTIONAL* Stop-time keyword that 'YYYY-MM-DDTHH:MM:SS'.

        :param str check_content:
            *OPTIONAL* Check-content keyword that the input of string need to check.

        :param str exist:
            *OPTIONAL* Exist keyword that should be 'yes', 'no'.

        :param str option:
            *OPTIONAL* Option keyword that could input any option

        :return: Return a dict value which contain all elements, or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())

        all_option_list = (
            "type", "category", "start_from", "count", "source_address", "source_zone", "source_interface", "reason", "service",
            "destination_address", "application", "user", "threat_severity", "policy_name",
            "nested_application", "operation", "rule_name",
            "url", "role", "profile", "protocol", "source_name", "event_type",
            "start_time", "stop_time", "check_content", "exist","option",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)
        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])

        # send command to device and get response
        cmd_element_list = ["show security log report in-detail", ]

        if options['type'] is not None:
            cmd_element_list.append("{}".format(options['type']))

        if options['category'] is not None:
            cmd_element_list.append("category {}".format(options['category']))

        if options['start_from'] is not None:
            cmd_element_list.append("start-from {}".format(options['start_from']))

        if options['count'] is not None:
            cmd_element_list.append("count {}".format(options['count']))

        if options['source_address'] is not None:
            cmd_element_list.append("source-address {}".format(options['source_address']))

        if options['source_zone'] is not None:
            cmd_element_list.append("source-zone {}".format(options['source_zone']))

        if options['source_interface'] is not None:
            cmd_element_list.append("source-interface {}".format(options['source_interface']))

        if options['destination_address'] is not None:
            cmd_element_list.append("destination-address {}".format(options['destination_address']))

        if options['threat_severity'] is not None:
            cmd_element_list.append("threat-severity {}".format(options['threat_severity']))

        if options['reason'] is not None:
            cmd_element_list.append("reason {}".format(options['reason']))

        if options['service'] is not None:
            cmd_element_list.append("service {}".format(options['service']))

        if options['url'] is not None:
            cmd_element_list.append("url \"{}\"".format(options['url']))

        if options['role'] is not None:
            cmd_element_list.append("role {}".format(options['role']))

        if options['profile'] is not None:
            cmd_element_list.append("profile {}".format(options['profile']))

        if options['protocol'] is not None:
            cmd_element_list.append("protocol {}".format(options['protocol']))

        if options['policy_name'] is not None:
            cmd_element_list.append("policy-name {}".format(options['policy_name']))

        if options['rule_name'] is not None:
            cmd_element_list.append("rule-name {}".format(options['rule_name']))

        if options['nested_application'] is not None:
            cmd_element_list.append("nested-application {}".format(options['nested_application']))

        if options['application'] is not None:
            cmd_element_list.append("application {}".format(options['application']))

        if options['user'] is not None:
            cmd_element_list.append("user {}".format(options['user']))

        if options['source_name'] is not None:
            cmd_element_list.append("source-name {}".format(options['source_name']))

        if options['event_type'] is not None:
            cmd_element_list.append("event-type {}".format(options['event_type']))

        if options['start_time'] is not None:
            cmd_element_list.append("start-time {}".format(options['start_time']))

        if options['stop_time'] is not None:
            cmd_element_list.append("stop-time {}".format(options['stop_time']))

        if options['operation'] is not None:
            cmd_element_list.append("operation {}".format(options['operation']))

        if options['option'] is not None:
            cmd_element_list.append("{}".format(options['option']))


        cmd = " ".join(cmd_element_list)
        self.display(level="info", msg=cmd)
        response = self.dut.send_cli_cmd(
            device=device,
            cmd=cmd,
            format="xml",
            channel="pyez",
            timeout=options["timeout"],
        )
        if not response:
            return False

        response = response['security-log-report-in-detail']['entry']

        if options['exist'] == "yes":
            for i in range(1, 3):
                response = self.dut.send_cli_cmd(
                    device=device,
                    cmd=cmd,
                    format="xml",
                    channel="pyez",
                    timeout=options["timeout"],
                )
                response = response['security-log-report-in-detail']['entry']
                if options['check_content'] not in response:
                    self.display(level="info", msg="!!!NOT find options['check_content'], should find it, will sleep 5 secs")
                    time.sleep(5)
                else:
                    self.display(level="INFO", msg="return value: {}".format(response))
                    return str(response)
            response = self.dut.send_cli_cmd(
                device=device,
                cmd=cmd,
                format="xml",
                channel="pyez",
                timeout=options["timeout"],
            )
            response = response['security-log-report-in-detail']['entry']
            if options['check_content'] not in response:
                return False
            else:
                self.display(level="INFO", msg="return value: {}".format(response))
                return str(response)
        elif options['exist'] == "no":
            for i in range(1, 3):
                response = self.dut.send_cli_cmd(
                    device=device,
                    cmd=cmd,
                    format="xml",
                    channel="pyez",
                    timeout=options["timeout"],
                )
                response = response['security-log-report-in-detail']['entry']
                if options['check_content'] in response:
                    self.display(level="info", msg="Find options['check_content'], should NOT find it, will sleep 5 secs")
                    time.sleep(5)
                else:
                    return True
            response = self.dut.send_cli_cmd(
                device=device,
                cmd=cmd,
                format="xml",
                channel="pyez",
                timeout=options["timeout"],
            )
            response = response['security-log-report-in-detail']['entry']
            if options['check_content'] in response:
                return False
            else:
                return True
        else:
            return False

    def get_security_log_with_cmd(self, device, **kwargs):
        """Get security log content

        :param Device device:
        **REQUIRED** Handle of the device on which commands have to be executed.

        :param str type:
            *OPTIONAL* Type keyword that one of 'query', 'stream', etc...

        :param str category:
            *OPTIONAL* Category keyword that one of 'idp', 'session-all', etc..., or just give 'all'

        :param str file_name:
            *OPTIONAL* File_name keyword that input of file name

        :param str stream_file_name:
            *OPTIONAL* File_name keyword that input of stream file name

        :param str source_address:
            *OPTIONAL* Source_address keyword that input of source address

        :param str source_zone:
            *OPTIONAL* Source_zone keyword that input of source zone

        :param str source_interface:
            *OPTIONAL* Source_interface keyword that input of source interface

        :param str destination_address:
            *OPTIONAL* Destination_address keyword that input of destination address

        :param str threat_severity:
            *OPTIONAL* Threat-severity keyword that input of threat-severity

        :param int count:
            *OPTIONAL* Get count number

        :param str reason:
            *OPTIONAL* Reason keyword that one of 'TESTSPAM', etc.

        :param str service:
            *OPTIONAL* Service keyword that input of service.

        :param str url:
            *OPTIONAL* URL keyword that input of url.

        :param str role:
            *OPTIONAL* Role keyword that input of role.

        :param str profile:
            *OPTIONAL* Profile keyword that input of profile.

        :param str protocol:
            *OPTIONAL* Protocol keyword that input of protocol.

        :param str policy_name:
            *OPTIONAL* Policy-name keyword that input of policy-name.

        :param str rule_name:
            *OPTIONAL* Rule-name keyword that input of rule-name.

        :param str nested_application:
            *OPTIONAL* Nested-application keyword input of nested-application.

        :param str operation:
            *OPTIONAL* Operation keyword that one of 'or' or 'and'.

        :param str application:
            *OPTIONAL* Application keyword input of application.

        :param str user:
            *OPTIONAL* User keyword input of user name.

        :param str source_name:
            *OPTIONAL* Source-name keyword that the input of detail source_name.

        :param str event_type:
            *OPTIONAL* Event_type keyword that the input of detail event_type.

        :param str start_from:
            *OPTIONAL* Start-from keyword that input of the log index.

        :param str check_content:
            *OPTIONAL* Check-content keyword that the input of string need to check.

        :param str exist:
            *OPTIONAL* Exist keyword that should be 'yes', 'no'.

        :param str option:
            *OPTIONAL* Option keyword that could input any option

        :return: Return a dict value which contain all elements, or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())

        all_option_list = (
            "type", "category", "count", "source_address", "source_zone", "source_interface", "reason", "service",
            "destination_address", "application", "user", "threat_severity", "policy_name",
            "nested_application", "operation", "rule_name", "file_name", "stream_file_name",
            "url", "role", "profile", "protocol", "source_name", "event_type","option",
            "check_content", "exist",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)
        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])

        # send command to device and get response
        cmd_element_list = ["show security log", ]

        if options['type'] is not None:
            cmd_element_list.append("{}".format(options['type']))

        if options['file_name'] is not None:
            cmd_element_list.append("{}".format(options['file_name']))

        if options['stream_file_name'] is not None:
            cmd_element_list.append("file {}".format(options['stream_file_name']))

        if options['category'] is not None:
            cmd_element_list.append("category {}".format(options['category']))

        if options['count'] is not None:
            cmd_element_list.append("count {}".format(options['count']))

        if options['source_address'] is not None:
            cmd_element_list.append("source-address {}".format(options['source_address']))

        if options['source_zone'] is not None:
            cmd_element_list.append("source-zone {}".format(options['source_zone']))

        if options['source_interface'] is not None:
            cmd_element_list.append("source-interface {}".format(options['source_interface']))

        if options['destination_address'] is not None:
            cmd_element_list.append("destination-address {}".format(options['destination_address']))

        if options['threat_severity'] is not None:
            cmd_element_list.append("threat-severity {}".format(options['threat_severity']))

        if options['reason'] is not None:
            cmd_element_list.append("reason {}".format(options['reason']))

        if options['service'] is not None:
            cmd_element_list.append("service {}".format(options['service']))

        if options['url'] is not None:
            cmd_element_list.append("url \"{}\"".format(options['url']))

        if options['role'] is not None:
            cmd_element_list.append("role {}".format(options['role']))

        if options['profile'] is not None:
            cmd_element_list.append("profile {}".format(options['profile']))

        if options['protocol'] is not None:
            cmd_element_list.append("protocol {}".format(options['protocol']))

        if options['policy_name'] is not None:
            cmd_element_list.append("policy-name {}".format(options['policy_name']))

        if options['rule_name'] is not None:
            cmd_element_list.append("rule-name {}".format(options['rule_name']))

        if options['nested_application'] is not None:
            cmd_element_list.append("nested-application {}".format(options['nested_application']))

        if options['application'] is not None:
            cmd_element_list.append("application {}".format(options['application']))

        if options['user'] is not None:
            cmd_element_list.append("user {}".format(options['user']))

        if options['source_name'] is not None:
            cmd_element_list.append("source-name {}".format(options['source_name']))

        if options['event_type'] is not None:
            cmd_element_list.append("event-type {}".format(options['event_type']))

        if options['operation'] is not None:
            cmd_element_list.append("operation {}".format(options['operation']))

        if options['option'] is not None:
            cmd_element_list.append("{}".format(options['option']))


        cmd = " ".join(cmd_element_list)
        self.display(level="info", msg=cmd)
        response = self.dut.send_cli_cmd(
            device=device,
            cmd=cmd,
            format="xml",
            channel="pyez",
            timeout=options["timeout"],
        )

        if not response:
            return False

        response = response['security-logging-information']['show-hpl-infile']['entry']
        if options['exist'] == "yes":
            for i in range(1, 3):
                response = self.dut.send_cli_cmd(
                    device=device,
                    cmd=cmd,
                    format="xml",
                    channel="pyez",
                    timeout=options["timeout"],
                )
                response = response['security-logging-information']['show-hpl-infile']['entry']
                if options['check_content'] not in response:
                    self.display(level="info", msg="!!!NOT find options['check_content'], should find it, will sleep 5 secs")
                    time.sleep(5)
                else:
                    self.display(level="INFO", msg="return value: {}".format(response))
                    return str(response)
            response = self.dut.send_cli_cmd(
                device=device,
                cmd=cmd,
                format="xml",
                channel="pyez",
                timeout=options["timeout"],
            )
            response = response['security-logging-information']['show-hpl-infile']['entry']
            if options['check_content'] not in response:
                return False
            else:
                self.display(level="INFO", msg="return value: {}".format(response))
                return str(response)
        elif options['exist'] == "no":
            for i in range(1, 3):
                response = self.dut.send_cli_cmd(
                    device=device,
                    cmd=cmd,
                    format="xml",
                    channel="pyez",
                    timeout=options["timeout"],
                )
                response = response['security-logging-information']['show-hpl-infile']['entry']
                if options['check_content'] in response:
                    self.display(level="info", msg="Find options['check_content'], should NOT find it, will sleep 5 secs")
                    time.sleep(5)
                else:
                    return True
            response = self.dut.send_cli_cmd(
                device=device,
                cmd=cmd,
                format="xml",
                channel="pyez",
                timeout=options["timeout"]
            )
            response = response['security-logging-information']['show-hpl-infile']['entry']
            if options['check_content'] in response:
                return False
            else:
                return True
        else:
            return False


    def check_security_log_content(self, **kwargs):
        """Compare the security log result

        :param str content:
            *OPTIONAL* Content keyword that is the result get from keywords get_security_log_report_in_detail

        :param str check_content:
            *OPTIONAL* Check_content keyword that is the input of the string need to be check

        :param str category:
            *OPTIONAL* Category keyword that one of 'idp', 'session-all', etc..., or just give 'all'

        :param str source_address:
            *OPTIONAL* Source_address keyword that input of source address

        :param str destination_address:
            *OPTIONAL* Destination_address keyword that input of destination address

        :param int count:
            *OPTIONAL* Get count number

        :param int check_count:
            *OPTIONAL* Get check count number

        :param str start_from_content:
            *OPTIONAL* Start-from content keyword that input of the string need to be check.

        :param str start_time:
            *OPTIONAL* Start time keyword that the input of start time.

        :param str stop_time:
            *OPTIONAL* Stop time keyword that the input of stop time.

        :param str device_name:
            *OPTIONAL* Device name keyword that the input of device name.

        :param str reason:
            *OPTIONAL* Reason keyword that the input of detail reason.

        :param str category:
            *OPTIONAL* Category keyword that the input of detail category.

        :param str source_name:
            *OPTIONAL* Source-name keyword that the input of detail source_name.

        :param str roles:
            *OPTIONAL* roles keyword that input of roles.

        :param str profile:
            *OPTIONAL* Profile keyword that input of profile.

        :param str protocol_name:
            *OPTIONAL* protocol_name keyword that input of protocol_name.

        :param str username:
            *OPTIONAL* username keyword input of username name.

        :param str application:
            *OPTIONAL* Application keyword that input of application.

        :param str nested_application:
            *OPTIONAL* Nested-application keyword that input of Nested-application.

        :param str application_name:
            *OPTIONAL* Application_name keyword that input of application_name.

        :param str event_type:
            *OPTIONAL* Event_type keyword that input of event_type.

        :param str rule_name:
            *OPTIONAL* Rule-name keyword that input of rule-name.

        :param str threat_severity:
            *OPTIONAL* Threat_severity keyword that input of threat_severity.

        :return: Return True or return False
        """
        self.display_title(msg=self.tool.get_current_function_name())
        all_option_list = (
            "content", "check_content", "source_address", "destination_address", "count",
            "check_count", "start_time", "stop_time", "device_name",
            "reason", "category", "source_name", "start_from_content", "username", "roles",
            "profile", "protocol_name", "rule_name",
            "application", "application_name", "nested_application", "event_type", "threat_severity",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)

        options['timeout'] = kwargs.get('timeout', self.default['cli_show_timeout'])

        j = 0
        content_list = options['content'].split("\n")
        self.display(level="info", msg=content_list)
        if options['count'] is not None:
            count_int = int(options['count'])
            if len(content_list) == count_int:
                self.display(level="info", msg="Log total count {} is correct".format(len(content_list)))
            else:
                self.display(level="info", msg="!!Log total count {} is wrong, should be {}".format(len(content_list), count_int))
                j = j+1
        if options['check_count'] is not None:
            check_count_int = int(options['check_count'])
        if options['start_time'] is not None:
            start_time_group = re.search(r"T(\d+)\:(\d+)\:(\d+)", options['start_time'])
            start_time_sec = int(start_time_group.group(1))*3600+int(start_time_group.group(2))*60+int(start_time_group.group(3))
        if options['stop_time'] is not None:
            stop_time_group = re.search(r"T(\d+)\:(\d+)\:(\d+)", options['stop_time'])
            stop_time_sec = int(stop_time_group.group(1))*3600+int(stop_time_group.group(2))*60+int(stop_time_group.group(3))
            for log_detail in content_list:
                self.display(level="info", msg=log_detail)
                self.display(level="info", msg=options['device_name'])
                log_time_obj = re.search(r"\s+(.*)\s+{}".format(options['device_name']), log_detail)
                self.display(level="info", msg=log_time_obj)
                log_time_detail = log_time_obj.group(1)
                log_time_group = re.search(r"T(\d+)\:(\d+)\:(\d+)", log_time_detail)
                log_time_sec = int(log_time_group.group(1))*3600+int(log_time_group.group(2))*60+int(log_time_group.group(3))
                if start_time_sec <= log_time_sec and log_time_sec <= stop_time_sec:
                    self.display(level="info", msg="Log time {} is in time range {} to {}.".format(log_time_detail, options['start_time'], options['stop_time']))
                else:
                    self.display(level="info", msg="!!Log time {} is NOT in time range {} to {}.".format(log_time_detail, options['start_time'], options['stop_time']))
                    j = j+1


        if options['check_content'] is not None:
            check_content_count = options['content'].count(options['check_content'])
            if check_content_count == check_count_int:
                self.display(level="info", msg="The \"{}\" match count {} is correct".format(options['check_content'], check_content_count))
            else:
                self.display(level="info", msg="!!The \"{}\" match count {} is wrong, should be {}".format(options['check_content'], check_content_count, check_count_int))
                j = j+1
                #return False
        if options['start_from_content'] is not None:
            self.display(level="info", msg="compare_start_from_content={}".format(options['start_from_content']))
            if options['start_from_content'] in content_list[0]:
                self.display(level="info", msg="Find {} in the first shown log".format(options['start_from_content']))
            else:
                self.display(level="info", msg="!!Not find {} in the first shown log, should find it".format(options['start_from_content']))
                j = j+1
        if options['source_address'] is not None:
            compare_source_address = "{}{}".format(" source-address=\"", options['source_address'])
            self.display(level="info", msg="compare_source_address={}".format(compare_source_address))
            source_address_count = options['content'].count(compare_source_address)
            if source_address_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_source_address, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_source_address, source_address_count, check_count_int))
                j = j+1
        if options['destination_address'] is not None:
            compare_destination_address = "{}{}".format(" destination-address=\"", options['destination_address'])
            self.display(level="info", msg="compare_destination_address={}".format(compare_destination_address))
            destination_address_count = options['content'].count(compare_destination_address)
            if destination_address_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_destination_address, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_destination_address, destination_address_count, check_count_int))
                j = j+1
        if options['reason'] is not None:
            compare_reason = "{}{}".format(" reason=\"", options['reason'])
            self.display(level="info", msg="compare_reason={}".format(compare_reason))
            reason_count = options['content'].count(compare_reason)
            if reason_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_reason, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_reason, reason_count, check_count_int))
                j = j+1
        if options['roles'] is not None:
            compare_roles = "{}{}".format(" roles=\"", options['roles'])
            self.display(level="info", msg="compare_roles={}".format(compare_roles))
            roles_count = options['content'].count(compare_roles)
            if roles_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_roles, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_roles, roles_count, check_count_int))
                j = j+1
        if options['profile'] is not None:
            compare_profile = "{}{}".format(" profile=\"", options['profile'])
            self.display(level="info", msg="compare_profile={}".format(compare_profile))
            profile_count = options['content'].count(compare_profile)
            if profile_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_profile, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_profile, profile_count, check_count_int))
                j = j+1
        if options['protocol_name'] is not None:
            compare_protocol_name = "{}{}".format(" protocol-name=\"", options['protocol_name'])
            self.display(level="info", msg="compare_protocol_name={}".format(compare_protocol_name))
            protocol_name_count = options['content'].count(compare_protocol_name)
            if protocol_name_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_protocol_name, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_protocol_name, protocol_name_count, check_count_int))
                j = j+1
        if options['username'] is not None:
            compare_username = "{}{}".format(" username=\"", options['username'])
            self.display(level="info", msg="compare_username={}".format(compare_username))
            username_count = options['content'].count(compare_username)
            if username_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_username, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_username, username_count, check_count_int))
                j = j+1
        if options['category'] is not None:
            compare_category = "{}{}".format(" category=\"", options['category'])
            self.display(level="info", msg="compare_category={}".format(compare_category))
            category_count = options['content'].count(compare_category)
            if category_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_category, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_category, category_count, check_count_int))
                j = j+1
        if options['source_name'] is not None:
            compare_source_name = "{}{}".format(" source-name=\"", options['source_name'])
            self.display(level="info", msg="compare_source_name={}".format(compare_source_name))
            source_name_count = options['content'].count(compare_source_name)
            if source_name_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_source_name, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_source_name, source_name_count, check_count_int))
                j = j+1
        if options['application'] is not None:
            compare_application = "{}{}".format(" application=\"", options['application'])
            self.display(level="info", msg="compare_application={}".format(compare_application))
            application_count = options['content'].count(compare_application)
            if application_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_application, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_application, application_count, check_count_int))
                j = j+1
        if options['nested_application'] is not None:
            compare_nested_application = "{}{}".format(" nested-application=\"", options['nested_application'])
            self.display(level="info", msg="compare_nested_application={}".format(compare_nested_application))
            nested_application_count = options['content'].count(compare_nested_application)
            if nested_application_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_nested_application, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_nested_application, nested_application_count, check_count_int))
                j = j+1
        if options['application_name'] is not None:
            compare_application_name = "{}{}".format(" application-name=\"", options['application_name'])
            self.display(level="info", msg="compare_application_name={}".format(compare_application_name))
            application_name_count = options['content'].count(compare_application_name)
            if application_name_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_application_name, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_application_name, application_name_count, check_count_int))
                j = j+1
        if options['event_type'] is not None:
            event_type_count = options['content'].count(options['event_type'])
            if event_type_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(options['event_type'], check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(options['event_type'], event_type_count, check_count_int))
                j = j+1
        if options['threat_severity'] is not None:
            compare_threat_severity = "{}{}".format(" threat-severity=\"", options['threat_severity'])
            self.display(level="info", msg="compare_threat_severity={}".format(compare_threat_severity))
            threat_severity_count = options['content'].count(compare_threat_severity)
            if threat_severity_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_threat_severity, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_threat_severity, threat_severity_count, check_count_int))
                j = j+1
        if options['rule_name'] is not None:
            compare_rule_name = "{}{}".format(" rule-name=\"", options['rule_name'])
            self.display(level="info", msg="compare_rule_name={}".format(compare_rule_name))
            rule_name_count = options['content'].count(compare_rule_name)
            if rule_name_count == check_count_int:
                self.display(level="info", msg="\"{}\" match count {} is correct".format(compare_rule_name, check_count_int))
            else:
                self.display(level="info", msg="!!\"{}\" match count {} is wrong, should be {}".format(compare_rule_name, rule_name_count, check_count_int))
                j = j+1
        if j != 0:
            return False
        return True

