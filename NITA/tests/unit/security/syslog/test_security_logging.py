# coding: UTF-8
"""All unit test cases for syslog module"""
# pylint: disable=attribute-defined-outside-init

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import time
from unittest import TestCase, mock
from jnpr.toby.utils.junos.dut_tool import dut_tool
from jnpr.toby.utils.message import message
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.security.syslog.security_logging import security_logging


class TestSecurityLogging(TestCase):
    """Unitest cases for SYSLOG module"""
    def setUp(self):
        """setup before all case"""
        self.log = message(name="SYSLOG")
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.ins = security_logging()

    def tearDown(self):
        """teardown after all case"""
        pass

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_get_and_check_security_log_report_summary(self, mock_send_cli_cmd):
        """checking security log report summary result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "checking summary number is 0"
        response = """
        <security-log-report-summary>
            <security-log-report-summary-total-count>0</security-log-report-summary-total-count>
        </security-log-report-summary>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report summary dict value")
        result = self.ins.get_and_check_security_log_report_summary(
            device=None,
            type="all",
            option="logical-systems LSYS1",
            number="0"
        )
        #self.assertTrue(isinstance(result, dict))
        self.assertTrue(result)

        msg = "checking summary type is none"
        response = """
        <security-log-report-summary>
            <security-log-report-summary-total-count>0</security-log-report-summary-total-count>
        </security-log-report-summary>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report summary dict value")
        result = self.ins.get_and_check_security_log_report_summary(
            device=None,
            number="0"
        )
        #self.assertTrue(isinstance(result, dict))
        self.assertTrue(result)

        msg = "checking summary number is not correct"
        response = """
        <security-log-report-summary>
            <security-log-report-summary-total-count>1</security-log-report-summary-total-count>
        </security-log-report-summary>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report summary dict value")
        result = self.ins.get_and_check_security_log_report_summary(
            device=None,
            number="2"
        )
        #self.assertTrue(isinstance(result, dict))
        self.assertFalse(result)

        msg = "checking summary result is none"
        response = """
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report summary dict value")
        result = self.ins.get_and_check_security_log_report_summary(
            device=None,
            type="all",
            number="3"
        )
        #self.assertTrue(isinstance(result, dict))
        self.assertFalse(result)

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_get_security_log_report_in_interval(self, mock_send_cli_cmd):
        """checking security log report in interval result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "checking in interval result is existing"
        response = """
        <security-log-report-in-interval>
            <security-log-report-in-interval-entry style="session-denied-n-all">
                <security-log-report-in-interval-time>
                2017-02-22T14:15:20
                </security-log-report-in-interval-time>
                <security-log-report-in-interval-denied>
                0
                </security-log-report-in-interval-denied>
                <security-log-report-in-interval-all>
                0
                </security-log-report-in-interval-all>
            </security-log-report-in-interval-entry>
        </security-log-report-in-interval>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in interval dict value")
        result = self.ins.get_security_log_report_in_interval(
            device=None,
            type="session-all",
            start_time="2017-02-22T14:15:20",
            stop_time="2017-02-22T14:16:00",
            option="logical-systems LSYS1",
        )
        self.assertTrue(isinstance(result, dict))


        msg = "checking in interval result is none"
        response = """
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report summary dict value")
        result = self.ins.get_security_log_report_in_interval(
            device=None,
            type="session-all",
            start_time="2017-02-22T14:15:20",
            stop_time="2017-02-22T14:16:00",
        )
        self.assertFalse(isinstance(result, dict))

        msg = "checking in interval parameter is none"
        response = """
        <security-log-report-in-interval>
            <security-log-report-in-interval-entry style="session-denied-n-all">
                <security-log-report-in-interval-time>
                2017-02-22T14:15:20
                </security-log-report-in-interval-time>
                <security-log-report-in-interval-denied>
                0
                </security-log-report-in-interval-denied>
                <security-log-report-in-interval-all>
                0
                </security-log-report-in-interval-all>
            </security-log-report-in-interval-entry>
        </security-log-report-in-interval>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report summary dict value")
        result = self.ins.get_security_log_report_in_interval(
            device=None,
        )
        self.assertTrue(isinstance(result, dict))

        msg = "checking in interval parameter is none"
        response = """
        <security-log-report-in-interval>
        </security-log-report-in-interval>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report summary dict value")
        result = self.ins.get_security_log_report_in_interval(
            device=None,
        )
        self.assertEqual(result['security-log-report-in-interval'], '')

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_compare_security_log_report_in_interval(self, mock_send_cli_cmd):
        """Checking compare security log report in interval result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "Compare in interval result"
        response = [{'security-log-report-in-interval-all': '0',
        'security-log-report-in-interval-denied': '0',
        'security-log-report-in-interval-time': '2017-02-22T14:15:20'},
        {'security-log-report-in-interval-all': '0',
        'security-log-report-in-interval-denied': '0',
        'security-log-report-in-interval-time': '2017-02-22T14:15:30'}
        ]

        #mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in interval dict value")
        result = self.ins.compare_security_log_report_in_interval(
            device=None,
            content=response,
            time=["2017-02-22T14:15:20", "2017-02-22T14:15:30"],
            denied_number=["0", "0"],
            all_number=["0", "0"]
        )
        self.assertTrue(result)

        msg = "Compare in interval result with error"
        response = [{'security-log-report-in-interval-all': '0',
        'security-log-report-in-interval-denied': '0',
        'security-log-report-in-interval-time': '2017-02-22T14:15:20'},
        {'security-log-report-in-interval-all': '0',
        'security-log-report-in-interval-denied': '0',
        'security-log-report-in-interval-time': '2017-02-22T14:15:30'}
        ]

        #mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in interval dict value")
        result = self.ins.compare_security_log_report_in_interval(
            device=None,
            content=response,
            time=["2017-02-22T14:15:20", "2017-02-22T14:15:50"],
            denied_number=["0", "1"],
            all_number=["2", "0"]
        )
        self.assertFalse(result)

    @mock.patch("time.sleep")
    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_get_security_log_report_top(self, mock_send_cli_cmd, mock_sleep):
        """Get security log top result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "get top result is existing"
        response = """
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user1
                </security-log-report-top-user>
                <security-log-report-top-volume>
                2513920.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                2455
                </security-log-report-top-count>
                <security-log-report-top-app>
                application1
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                2048000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                2000
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report top dict value")
        result = self.ins.get_security_log_report_top(
            device=None,
            type="session-close",
            top_number="40",
            group_by="user",
            order_by="volume",
            with_var="application",
            #ascending="ascending",
            start_time="2017-02-22T14:15:20",
            stop_time="2017-02-22T14:15:50",
            where_action="action",
            where_application="application",
            exist="yes",
            option="logical-systems LSYS1",
        )
        self.assertTrue(isinstance(result, list))

        msg = "get top result with no exist parameter"
        response = """
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report top dict value")
        result = self.ins.get_security_log_report_top(
            device=None,
            type="session-close",
            top_number="40",
            group_by="user",
            order_by="volume",
            with_var="application",
            start_time="2017-02-22T14:15:20",
            stop_time="2017-02-22T14:15:50",
            where_action="action",
            where_application="application",
        )
        self.assertFalse(result)

        msg = "get top result is none"
        response = """
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report top dict value")
        result = self.ins.get_security_log_report_top(
            device=None,
            type="session-close",
            top_number="10",
            group_by="application",
            order_by="volume",
            ascending="ascending",
            exixt="no"
        )
        self.assertFalse(result)

        msg = "get top result exist=yes"
        response = """
        <security-log-report-top>
        </security-log-report-top>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report top dict value")
        result = self.ins.get_security_log_report_top(
            device=None,
            type="session-close",
            top_number="10",
            group_by="application",
            order_by="volume",
            exist="yes"
        )
        self.assertFalse(result)

        msg = "get top result exist=no"
        response = """
        <security-log-report-top>
        </security-log-report-top>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report top dict value")
        result = self.ins.get_security_log_report_top(
            device=None,
            type="session-close",
            top_number="10",
            group_by="application",
            order_by="volume",
            exist="no"
        )
        self.assertTrue(result)

        msg = "get top result exist=no but has content"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-top>
        </security-log-report-top>
        """),
        )


        #mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report top dict value")
        result = self.ins.get_security_log_report_top(
            device=None,
            type="session-close",
            top_number="10",
            group_by="application",
            order_by="volume",
            exist="no"
        )
        self.assertTrue(result)

        msg = "get top result exist=no but has content"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-top>
            <security-log-report-top-entry style="user-volume-with-application">
                <security-log-report-top-user>
                user2
                </security-log-report-top-user>
                <security-log-report-top-volume>
                1536000.000000
                </security-log-report-top-volume>
                <security-log-report-top-count>
                1500
                </security-log-report-top-count>
                <security-log-report-top-app>
                application2
                </security-log-report-top-app>
                <security-log-report-top-app-volume>
                1536000.000000
                </security-log-report-top-app-volume>
                <security-log-report-top-app-count>
                1500
                </security-log-report-top-app-count>
            </security-log-report-top-entry>
        </security-log-report-top>
        """)
        )


        #mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report top dict value")
        result = self.ins.get_security_log_report_top(
            device=None,
            type="session-close",
            top_number="10",
            group_by="application",
            order_by="volume",
            exist="no"
        )
        self.assertFalse(result)

        msg = "get top result with no parameter"
        response = """
        <security-log-report-top>
        </security-log-report-top>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report top dict value")
        result = self.ins.get_security_log_report_top(
            device=None,
            exist="yes"
        )
        self.assertTrue(result)

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_compare_security_log_report_top(self, mock_send_cli_cmd):
        """Checking compare security log report top result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "Compare top result user"
        response = [{'security-log-report-top-app': 'application1',
                    'security-log-report-top-count': '2000',
                    'security-log-report-top-user': 'user1',
                    'security-log-report-top-user-count': '2000',
                    'security-log-report-top-user-volume': '2048000.000000',
                    'security-log-report-top-volume': '2048000.000000'},
                    {'security-log-report-top-app': 'application2',
                    'security-log-report-top-count': '1638',
                    'security-log-report-top-user': 'user2',
                    'security-log-report-top-user-count': '1500',
                    'security-log-report-top-user-volume': '1536000.000000',
                    'security-log-report-top-volume': '1677312.000000'}]

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            user=["user1", "user2"],
            volume=["2048000.000000", "1677312.000000"],
            count=["2000", "1638"],
            app=["application1", "application2"],
            user_volume=["2048000.000000", "1536000.000000"],
            user_count=["2000", "1500"],
            order_by="volume"
        )
        self.assertTrue(result)

        response = {'security-log-report-top-app': 'application1',
                    'security-log-report-top-count': '2000',
                    'security-log-report-top-user': 'user1',
                    'security-log-report-top-user-count': '2000',
                    'security-log-report-top-user-volume': '2048000.000000',
                    'security-log-report-top-volume': '2048000.000000'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            user=["user1"],
            volume=["2048000.000000"],
            count=["2000"],
            app=["application1"],
            user_volume=["2048000.000000"],
            user_count=["2000"],
            order_by="volume"
        )
        self.assertTrue(result)

        msg = "Compare top result user with error"
        response = [{'security-log-report-top-app': 'application1',
                    'security-log-report-top-count': '2000',
                    'security-log-report-top-user': 'user1',
                    'security-log-report-top-user-count': '2000',
                    'security-log-report-top-user-volume': '2048000.000000',
                    'security-log-report-top-volume': '2048000.000000'},
                    {'security-log-report-top-app': 'application2',
                    'security-log-report-top-count': '1638',
                    'security-log-report-top-user': 'user2',
                    'security-log-report-top-user-count': '1500',
                    'security-log-report-top-user-volume': '1536000.000000',
                    'security-log-report-top-volume': '1677312.000000'}]

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            user=["user3", "user2"],
            volume=["2048050.000000", "1677312.000000"],
            count=["2000", "1738"],
            app=["application1", "application10"],
            user_volume=["2048000.000000", "2536000.000000"],
            user_count=[3, "1500"],
            order_by="volume"
        )
        self.assertFalse(result)

        response = {'security-log-report-top-app': 'application1',
                    'security-log-report-top-count': '2000',
                    'security-log-report-top-user': 'user1',
                    'security-log-report-top-user-count': '2000',
                    'security-log-report-top-user-volume': '2048000.000000',
                    'security-log-report-top-volume': '2048000.000000'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            user=["user4"],
            volume=["2048000.00200"],
            count=[2000],
            app=["application5"],
            user_volume=["2248000.000000"],
            user_count=[2400],
            order_by="volume"
        )
        self.assertFalse(result)


        msg = "Compare top result with application"
        response = [{'security-log-report-top-app': 'application1',
                    'security-log-report-top-app-count': '2000',
                    'security-log-report-top-app-volume': '2048000.000000',
                    'security-log-report-top-count': '2455',
                    'security-log-report-top-user': 'user1',
                    'security-log-report-top-volume': '2513920.000000'},
                    {'security-log-report-top-app': 'application8',
                    'security-log-report-top-app-count': '400',
                    'security-log-report-top-app-volume': '409600.000000',
                    'security-log-report-top-count': '-',
                    'security-log-report-top-user': '-',
                    'security-log-report-top-volume': '-'}]

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            user=["user1", "-"],
            volume=["2513920.000000", "-"],
            count=["2455", "-"],
            app=["application1", "application8"],
            app_volume=["2048000.000000", "409600.000000"],
            app_count=["2000", "400"],
            order_by="volume",
            order="descending"
        )
        self.assertTrue(result)

        response = {'security-log-report-top-app': 'application8',
                    'security-log-report-top-app-count': '400',
                    'security-log-report-top-app-volume': '409600.000000',
                    'security-log-report-top-count': '-',
                    'security-log-report-top-user': '-',
                    'security-log-report-top-volume': '-'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            user=["-"],
            volume=["-"],
            count=["-"],
            app=["application8"],
            app_volume=["409600.000000"],
            app_count=["400"],
            order_by="volume",
        )
        self.assertTrue(result)

        msg = "Compare top result with application with error"
        response = [{'security-log-report-top-app': 'application1',
                    'security-log-report-top-app-count': '2000',
                    'security-log-report-top-app-volume': '2048000.000000',
                    'security-log-report-top-count': '2455',
                    'security-log-report-top-user': 'user1',
                    'security-log-report-top-volume': '2513920.000000'},
                    {'security-log-report-top-app': 'application8',
                    'security-log-report-top-app-count': '400',
                    'security-log-report-top-app-volume': '409600.000000',
                    'security-log-report-top-count': '-',
                    'security-log-report-top-user': '-',
                    'security-log-report-top-volume': '-'}]

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            user=["user11", "-"],
            volume=["5", 4],
            count=["-", "-"],
            app=["application10", "application8"],
            app_volume=["2048300.000000", "409600.000000"],
            app_count=[2000, "4050"],
            order_by="count",
            order="descending"
        )
        self.assertFalse(result)

        response = {'security-log-report-top-app': 'application8',
                    'security-log-report-top-app-count': '400',
                    'security-log-report-top-app-volume': '409600.000000',
                    'security-log-report-top-count': '-',
                    'security-log-report-top-user': '-',
                    'security-log-report-top-volume': '-'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            user=["3"],
            volume=["2"],
            count=[1],
            app=["applicatio"],
            app_volume=["40900.000000"],
            app_count=[4070],
            order_by="volume",
        )
        self.assertFalse(result)



        msg = "Compare top no parameter"
        response = [{'security-log-report-top-app': 'application1',
                    'security-log-report-top-count': '2000',
                    'security-log-report-top-user': 'user1',
                    'security-log-report-top-user-count': '2000',
                    'security-log-report-top-user-volume': '2048000.000000',
                    'security-log-report-top-volume': '2048000.000000'},
                    {'security-log-report-top-app': 'application2',
                    'security-log-report-top-count': '1638',
                    'security-log-report-top-user': 'user2',
                    'security-log-report-top-user-count': '1500',
                    'security-log-report-top-user-volume': '1536000.000000',
                    'security-log-report-top-volume': '1677312.000000'}]

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
        )
        self.assertTrue(result)

        response = {'security-log-report-top-app': 'application2',
                    'security-log-report-top-count': '1638',
                    'security-log-report-top-user': 'user2',
                    'security-log-report-top-user-count': '1500',
                    'security-log-report-top-user-volume': '1536000.000000',
                    'security-log-report-top-volume': '1677312.000000'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
        )
        self.assertTrue(result)


        msg = "Compare top result user"
        response = [{'security-log-report-top-count': '1000',
                    'security-log-report-top-header': 'RT_FLOW_SESSION_CLOSE'},
                    {'security-log-report-top-count': '1000',
                    'security-log-report-top-header': 'RT_FLOW_SESSION_CREATE'}]

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["RT_FLOW_SESSION_CLOSE", "SESSION_CREATE"],
            count=["1000", 100],
            order_by="count"
        )
        self.assertFalse(result)

        response = {'security-log-report-top-count': '1000',
                    'security-log-report-top-header': 'RT_FLOW_SESSION_CLOSE'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["RT_FLOW_SESSION"],
            count=[10],
            order_by="count"
        )
        self.assertFalse(result)

        response = {'security-log-report-top-count': '1000',
                    'security-log-report-top-header': 'RT_FLOW_SESSION_CLOSE'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["RT_FLOW_SESSION_CLOSE"],
            count=[1000],
            order_by="count"
        )
        self.assertTrue(result)

        msg = "Compare top result user number"
        response = [{'security-log-report-top-count': '400',
                    'security-log-report-top-header': 'http://www.viruslist.com/en/search?VN=EICAR-Test-File_1',
                    'security-log-report-top-usernumber': '1'},
                    {'security-log-report-top-count': '300',
                    'security-log-report-top-header': 'http://www.viruslist.com/en/search?VN=EICAR-Test-File_2',
                    'security-log-report-top-usernumber': '1'}]

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["RT_FLOW_SESSION_CLOSE", "SESSION_CREATE"],
            count=["400", 300],
            user_number=["1", 2],
            order_by="count"
        )
        self.assertFalse(result)
        response = {'security-log-report-top-count': '400',
                    'security-log-report-top-header': 'http://www.viruslist.com/en/search?VN=EICAR-Test-File_1',
                    'security-log-report-top-usernumber': '1'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["http://www.viruslist.com/en/search?VN=EICAR-Test-File_1"],
            count=["400"],
            user_number=[3],
            order_by="count"
        )
        self.assertFalse(result)
        response = {'security-log-report-top-count': '400',
                    'security-log-report-top-header': 'http://www.viruslist.com/en/search?VN=EICAR-Test-File_1',
                    'security-log-report-top-usernumber': '1'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["http://www.viruslist.com/en/search?VN=EICAR-Test-File_1"],
            count=["400"],
            user_number=["1"],
            order_by="count"
        )
        self.assertTrue(result)

        msg = "Compare top result packet"
        response = [{'security-log-report-top-header': 'source_zone1',
                    'security-log-report-top-packet': '1717986917600'},
                    {'security-log-report-top-header': 'source_zone2',
                    'security-log-report-top-packet': '1288490188200'}]

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["source_zone1", "source_zone2"],
            packet=["1717986917600", 1000],
            order_by="packet"
        )
        self.assertFalse(result)
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["source_zone1", "source_zone2"],
            packet=["1717986917600", "222"],
            order_by="count"
        )
        self.assertFalse(result)
        response = {'security-log-report-top-header': 'source_zone1',
                    'security-log-report-top-packet': '1717986917600'}

        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["source_zone1"],
            packet=[3],
            order_by="packet"
        )
        self.assertFalse(result)
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["source_zone1"],
            packet=["-"],
            order_by="count"
        )
        self.assertFalse(result)

        response = {'security-log-report-top-header': 'source_zone1',
                    'security-log-report-top-packet': '1717986917600'}
        self.log.display(level="INFO", msg="compare security log report top dict value")
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["source_zone1"],
            packet=["1717986917600"],
            order_by="packet"
        )
        self.assertTrue(result)
        result = self.ins.compare_security_log_report_top(
            device=None,
            content=response,
            header_name=["source_zone1"],
            packet=["1717986917600"],
            order_by="count"
        )
        self.assertTrue(result)

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_calculate_volume(self, mock_send_cli_cmd):
        """Checking calculate volume result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "calculate volume with number"
        response = ["2000", "400", "-"]

        result = self.ins.calculate_volume(
            device=None,
            count=response,
        )
        self.assertTrue(result)

        msg = "calculate volume with number with wing1_volume"
        response = ["2000", "400"]

        result = self.ins.calculate_volume(
            device=None,
            count=response,
            wing1_volume="1000"
        )
        self.assertTrue(result)

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_count_list_calculate(self, mock_send_cli_cmd):
        """Checking Count List Calculate result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "Count List Calculate total count with user"
        result = self.ins.count_list_calculate(
            device=None,
            count_list=[2000, "user9", "application1", 200, "user9", "application2"],
            user="user9",
            return_argu="total_count"
        )
        self.assertTrue(isinstance(result, list))
        msg = "Count List Calculate user count with user"
        result = self.ins.count_list_calculate(
            device=None,
            count_list=[2000, "user9","application1"],
            user="user9",
            return_argu="user_count"
        )
        self.assertTrue(isinstance(result, list))
        msg = "Count List Calculate total count with application"
        result = self.ins.count_list_calculate(
            device=None,
            count_list=[2000, "user9", "application1", 200, "user9", "application1", 20, "user1", "application3"],
            application="application1",
            return_argu="total_count"
        )
        self.assertTrue(isinstance(result, list))
        msg = "Count List Calculate user count with user"
        result = self.ins.count_list_calculate(
            device=None,
            count_list=[2000, "user9","application1"],
            application="application2",
            return_argu="count"
        )
        self.assertFalse(result)

    @mock.patch("time.sleep")
    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_get_security_log_report_in_detail(self, mock_send_cli_cmd, mock_sleep):
        """Get security log report in detail result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "get in detail result is existing"
        response = """
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
           </entry>
        </security-log-report-in-detail>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_report_in_detail(
            device=None,
            type="session-close",
            category="1",
            source_address="192.168.100.103",
            source_zone="source_zone1",
            source_interface="1",
            destination_address="192.168.200.103",
            threat_severity="1",
            count="1",
            reason="1",
            service="1",
            url="1",
            role="1",
            profile="1",
            protocol="1",
            policy_name="1",
            rule_name="1",
            nested_application="1",
            operation="1",
            application="1",
            user="1",
            source_name="1",
            event_type="1",
            start_from="1",
            start_time="1",
            stop_time="1",
            check_content="cnrd-ngsrxqavm40",
            option="logical-systems LSYS1",
            exist="yes",
        )
        self.assertTrue(isinstance(result, str))

        msg = "get in detail result with no parameter"
        response = """
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        result = self.ins.get_security_log_report_in_detail(
            device=None,
            check_content="cnrd-ngsrxqavm40",
            exist="yes",
        )
        self.assertTrue(isinstance(result, str))

        msg = "get in detail result exist is none"
        response = """
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_report_in_detail(
            device=None,
            type="session-close",
            check_content="cnrd-ngsrxqavm40",
        )
        self.assertFalse(result)

        msg = "get in detail result is none"
        response = """
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_report_in_detail(
            device=None,
            type="session-close",
            check_content="cnrd-ngsrxqavm40",
        )
        self.assertFalse(result)

        msg = "get in detail result exist is no with no check_content"
        response = """
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_report_in_detail(
            device=None,
            type="session-close",
            check_content="1234567",
            exist="no"
        )
        self.assertTrue(result)


        msg = "get in detail result check_content is wrong"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        )
        result = self.ins.get_security_log_report_in_detail(
            device=None,
            check_content="cnrd-ngsrxqavm40",
            exist="yes",
        )
        self.assertTrue(isinstance(result, str))



        msg = "get in detail result check_content is wrong"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        )
        result = self.ins.get_security_log_report_in_detail(
            device=None,
            check_content="1234567",
            exist="yes",
        )
        self.assertFalse(result)


        msg = "get in detail result check_content is wrong"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        )
        result = self.ins.get_security_log_report_in_detail(
            device=None,
            check_content="cnrd-ngsrxqavm40",
            exist="no",
        )
        self.assertFalse(result)


        msg = "get in detail result exist is no"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
            </entry>
        </security-log-report-in-detail>
        """),
        self.xml.xml_string_to_dict("""
        <security-log-report-in-detail>
            <entry>
            </entry>
        </security-log-report-in-detail>
        """),
        )

        #mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_report_in_detail(
            device=None,
            type="session-close",
            source_address="192.168.100.103",
            check_content="cnrd-ngsrxqavm40",
            exist="no",
        )
        self.assertTrue(result)

    @mock.patch("time.sleep")
    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_get_security_log_with_cmd(self, mock_send_cli_cmd, mock_sleep):
        """Get security log with CMD result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "get in detail result is existing"
        response = """
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_with_cmd(
            device=None,
            type="stream",
            file_name="file",
            stream_file_name="f1",
            category="1",
            source_address="192.168.100.103",
            source_zone="source_zone1",
            source_interface="1",
            destination_address="192.168.200.103",
            threat_severity="1",
            count="1",
            reason="1",
            service="1",
            url="1",
            role="1",
            profile="1",
            protocol="1",
            policy_name="1",
            rule_name="1",
            nested_application="1",
            operation="1",
            application="1",
            user="1",
            source_name="1",
            event_type="1",
            start_from="1",
            start_time="1",
            stop_time="1",
            check_content="cnrd-ngsrxqavm40",
            option="logical-systems LSYS1",
            exist="yes",
        )
        self.assertTrue(isinstance(result, str))

        msg = "get in detail result with no parameter"
        response = """
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        result = self.ins.get_security_log_with_cmd(
            device=None,
            check_content="cnrd-ngsrxqavm40",
            exist="yes",
        )
        self.assertTrue(isinstance(result, str))

        msg = "get in detail result exist is none"
        response = """
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_with_cmd(
            device=None,
            type="session-close",
            check_content="cnrd-ngsrxqavm40",
        )
        self.assertFalse(result)

        msg = "get in detail result is none"
        response = """
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_with_cmd(
            device=None,
            type="session-close",
            check_content="cnrd-ngsrxqavm40",
        )
        self.assertFalse(result)

        msg = "get in detail result exist is no with no check_content"
        response = """
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_with_cmd(
            device=None,
            type="session-close",
            check_content="1234567",
            exist="no"
        )
        self.assertTrue(result)


        msg = "get in detail result check_content is wrong"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        )
        result = self.ins.get_security_log_with_cmd(
            device=None,
            check_content="cnrd-ngsrxqavm40",
            exist="yes",
        )
        self.assertTrue(isinstance(result, str))



        msg = "get in detail result check_content is wrong"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        )
        result = self.ins.get_security_log_with_cmd(
            device=None,
            check_content="1234567",
            exist="yes",
        )
        self.assertFalse(result)


        msg = "get in detail result check_content is wrong"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        )
        result = self.ins.get_security_log_with_cmd(
            device=None,
            check_content="cnrd-ngsrxqavm40",
            exist="no",
        )
        self.assertFalse(result)


        msg = "get in detail result exist is no"
        mock_send_cli_cmd.side_effect = (
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                &lt;14&gt;1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="8003" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="8003" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]
               </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        self.xml.xml_string_to_dict("""
        <security-logging-information>
            <show-hpl-infile>
                <entry>
                </entry>
           </show-hpl-infile>
        </security-logging-information>
        """),
        )

        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.get_security_log_with_cmd(
            device=None,
            type="session-close",
            source_address="192.168.100.103",
            check_content="cnrd-ngsrxqavm40",
            exist="no",
        )
        self.assertTrue(result)

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_check_security_log_content(self, mock_send_cli_cmd):
        """Check log conteng result"""
        self.log.display_title(title=self.tool.get_current_function_name())
        self.log.step_num = 0
        msg = "get in detail result is existing"
        response = '<14>1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="20005" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="20005" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]'
        # mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.check_security_log_content(
            device=None,
            content=response,
            count="1",
            check_count=1,
            source_address="192.168.100.103",
            destination_address="192.168.200.103",
            service="Medium",
            application="application4",
            nested_application="nested_application4",
            operation="or",
            username="user4",
            event_type="RT_FLOW_SESSION_CLOSE",
            start_from="1",
            start_from_content="RT_FLOW_SESSION_CLOSE",
            start_time="2017-02-22T14:15:30",
            stop_time="2017-02-22T14:15:45",
            device_name="cnrd-ngsrxqavm40",
            check_content="cnrd-ngsrxqavm40",
        )
        self.assertTrue(result)

        response = '<14>1 2015-11-23T14:06:00.715+08:00 bjsolar RT_IDP - IDP_ATTACK_LOG_EVENT [junos@2636.1.1.1.2.26 epoch-time="1448258760" message-type="SIG" source-address="25.0.0.254" source-port="2" destination-address="192.1.1.2" destination-port="44386" protocol-name="ICMP" service-name="SERVICE_IDP" application-name="NONE" rule-name="1" rulebase-name="IPS" policy-name="idp-policy1" export-id="9025" repeat-count="0" action="NONE" threat-severity="INFO" attack-name="ICMP:INFO:ECHO-REPLY" nat-source-address="0.0.0.0" nat-source-port="0" nat-destination-address="0.0.0.0" nat-destination-port="0" elapsed-time="0" inbound-bytes="0" outbound-bytes="0" inbound-packets="0" outbound-packets="0" source-zone-name="cppm" source-interface-name="ge-11/0/4.0" destination-zone-name="trust" destination-interface-name="ge-11/0/1.0" packet-log-id="0" alert="no" username="N/A" roles="N/A" message="-"]'
        # mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.check_security_log_content(
            device=None,
            content=response,
            count="1",
            check_count=1,
            source_address="25.0.0.254",
            destination_address="192.1.1.2",
            threat_severity="INFO",
            protocol_name="ICMP",
            rule_name="1",
            application_name="NONE",
            event_type="IDP_ATTACK_LOG_EVENT",
            start_from="1",
            start_from_content="IDP_ATTACK_LOG_EVENT",
            start_time="2015-11-23T14:06:00",
            stop_time="2015-11-23T14:06:00",
            device_name="bjsolar",
            check_content="bjsolar",
        )
        self.assertTrue(result)

        msg = "get in detail result is existing"
        response = '<14>1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="20005" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="20005" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]'
        # mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        self.log.display(level="INFO", msg="get security log report in detail dict value")
        result = self.ins.check_security_log_content(
            device=None,
            content=response,
            count="3",
            check_count=1,
            category="1",
            source_address="192222",
            destination_address="12222",
            threat_severity="1",
            reason="1",
            service="1",
            url="1",
            roles="1",
            profile="1",
            protocol_name="1",
            rule_name="1",
            nested_application="1",
            operation="1",
            application="1",
            application_name="1",
            username="1",
            source_name="1",
            event_type="aaaaaN_CLOSE",
            start_from="1",
            start_from_content="333",
            start_time="2017-02-22T14:16:30",
            stop_time="2017-02-22T14:16:45",
            device_name="cnrd-ngsrxqavm40",
            check_content="5555",
        )
        self.assertFalse(result)

        msg = "get in detail result with no parameter"
        response = '<14>1 2017-02-22T14:15:35 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - RT_FLOW_SESSION_CLOSE [junos@2636.1.1.1.2.129 reason="Some reason" source-address="192.168.100.103" source-port="20005" destination-address="192.168.200.103" destination-port="32768" connection-tag="0" service-name="Medium" nat-source-address="192.168.100.103" nat-source-port="20005" nat-destination-address="192.168.200.103" nat-destination-port="32768" nat-connection-tag="0" src-nat-rule-type="Fake src nat rule" src-nat-rule-name="Fake src nat rule" dst-nat-rule-type="Fake dst nat rule" dst-nat-rule-name="Fake dst nat rule" protocol-id="17" policy-name="session_policy4" source-zone-name="source_zone4" destination-zone-name="Fake dst zone" session-id-32="4" packets-from-client="4294967295" bytes-from-client="1073741824" packets-from-server="4294967294" bytes-from-server="1073741824" elapsed-time="4294967291" application="application4" nested-application="nested_application4" username="user4" roles="Fake UAC roles" packet-incoming-interface="source_interface4" encrypted="Fake info telling if the traffic is encrypted"]'
        # mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        result = self.ins.check_security_log_content(
            device=None,
            content=response,
        )
        self.assertTrue(result)

        msg = "get in detail result without check_content"
        response = """
        <12>1 2017-05-11T13:45:24 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - WEBFILTER_URL_BLOCKED [junos@2636.1.1.1.2.129 source-address="1.16.16.16" source-port="36733" destination-address="2.16.16.16" destination-port="80" session-id="1" category="N/A" reason="TESTSPAM" profile="PROFILE" url="http://www.viruslist.com/en/search?VN=EICAR-Test-File" obj="N/A" username="N/A" roles="N/A"]
        <14>1 2017-05-11T13:45:24 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - WEBFILTER_URL_PERMITTED [junos@2636.1.1.1.2.129 source-address="1.16.16.16" source-port="36733" destination-address="2.16.16.16" destination-port="80" session-id="1" category="N/A" reason="TESTSPAM" profile="PROFILE" url="http://www.viruslist.com/en/search?VN=EICAR-Test-File" obj="N/A" username="N/A" roles="N/A"]
        """
        # mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        result = self.ins.check_security_log_content(
            device=None,
            check_count="2",
            content=response,
            category="N/A",
            reason="TESTSPAM",
            url="http://www.viruslist.com/en/search?VN=EICAR-Test-File",
            roles="N/A",
            profile="PROFILE",
        )
        self.assertTrue(result)

        msg = "get in detail result with source-name"
        response = """
        <14>1 2017-05-11T13:45:24 cnrd-ngsrxqavm40 RT_LOG_SELF_TEST - ANTISPAM_SPAM_DETECTED_MT [junos@2636.1.1.1.2.129 source-name="spamtest@spamtest.com" source-address="1.16.16.16" profile-name="PROFILE" action="BLOCKED" reason="TESTSPAM" username="N/A" roles="N/A"]
        """
        # mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        result = self.ins.check_security_log_content(
            device=None,
            check_count="1",
            content=response,
            source_name="spamtest@spamtest.com",
        )
        self.assertTrue(result)
