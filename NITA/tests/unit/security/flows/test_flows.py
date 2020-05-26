# coding: UTF-8
"""All unit test cases for FLOW module"""
__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'
# pylint: disable=attribute-defined-outside-init,invalid-name
import re
import copy
from unittest import TestCase, mock

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.security.flows.flows import flows
from jnpr.toby.utils.junos.dut_tool import dut_tool


class TestFlows(TestCase):
    """Unitest cases for flows module"""
    def setUp(self):
        """setup before all cases"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.ins = flows()
        self.ins.debug_to_stdout = True

        self.var = {
            "R0H0_IF":              "ge-5/1/0",
            "R0H1_IF":              "ge-5/1/1",
            "R0H0_IPV4_ADDRESS":    "192.168.100.1",
            "R0H1_IPV4_ADDRESS":    "192.168.200.1",
            "H0R0_IPV4_ADDRESS":    "192.168.100.2",
            "H1R0_IPV4_ADDRESS":    "192.168.200.2",
            "IPV4_MASK":            "24",
        }

        self.response = {}
        self.response["he_text"] = """
        Flow Sessions on FPC0 PIC1:

        Session ID: 10000001, Policy name: N/A, Timeout: N/A, Valid
          In: 5ffd::2/1 --> 5ffd::1/1;gre, Conn Tag: 0x0, If: ge-5/2/1.0, Pkts: 0, Bytes: 0, CP Session ID: 0

        Session ID: 10000002, Policy name: N/A, Timeout: N/A, Valid
          In: 50.0.0.2/1 --> 50.0.0.1/1;gre, Conn Tag: 0x0, If: ge-5/2/1.0, Pkts: 0, Bytes: 0, CP Session ID: 0

        Session ID: 10000006, Policy name: default-policy-logical-system-00/2, Timeout: 2, Valid
          In: 100.1.0.2/4 --> 100.2.0.2/8280;icmp, Conn Tag: 0x0, If: ge-5/1/0.0, Pkts: 1, Bytes: 84, CP Session ID: 10000140
          Out: 100.2.0.2/8280 --> 100.1.0.2/4;icmp, Conn Tag: 0x0, If: ge-5/1/1.0, Pkts: 1, Bytes: 84, CP Session ID: 10000140
        Total sessions: 3

        Flow Sessions on FPC0 PIC2:

        Session ID: 20000001, Policy name: N/A, Timeout: N/A, Valid
          In: 5ffd::2/1 --> 5ffd::1/1;gre, Conn Tag: 0x0, If: ge-5/2/1.0, Pkts: 0, Bytes: 0, CP Session ID: 0

        Session ID: 20000002, Policy name: N/A, Timeout: N/A, Valid
          In: 50.0.0.2/1 --> 50.0.0.1/1;gre, Conn Tag: 0x0, If: ge-5/2/1.0, Pkts: 0, Bytes: 0, CP Session ID: 0

        Session ID: 20000005, Policy name: default-policy-logical-system-00/2, Timeout: 2, Valid
          In: 100.1.0.2/3 --> 100.2.0.2/8280;icmp, Conn Tag: 0x0, If: ge-5/1/0.0, Pkts: 1, Bytes: 84, CP Session ID: 20000140
          Out: 100.2.0.2/8280 --> 100.1.0.2/3;icmp, Conn Tag: 0x0, If: ge-5/1/1.0, Pkts: 1, Bytes: 84, CP Session ID: 20000140

        Session ID: 20000006, Policy name: default-policy-logical-system-00/2, Timeout: 4, Valid
          In: 100.1.0.2/5 --> 100.2.0.2/8280;icmp, Conn Tag: 0x0, If: ge-5/1/0.0, Pkts: 1, Bytes: 84, CP Session ID: 20000141
          Out: 100.2.0.2/8280 --> 100.1.0.2/5;icmp, Conn Tag: 0x0, If: ge-5/1/1.0, Pkts: 1, Bytes: 84, CP Session ID: 20000141
        Total sessions: 4

        Flow Sessions on FPC0 PIC3:

        Session ID: 30000001, Policy name: N/A, Timeout: N/A, Valid
          In: 5ffd::2/1 --> 5ffd::1/1;gre, Conn Tag: 0x0, If: ge-5/2/1.0, Pkts: 0, Bytes: 0, CP Session ID: 0

        Session ID: 30000002, Policy name: N/A, Timeout: N/A, Valid
          In: 50.0.0.2/1 --> 50.0.0.1/1;gre, Conn Tag: 0x0, If: ge-5/2/1.0, Pkts: 0, Bytes: 0, CP Session ID: 0
        Total sessions: 2
        """

        self.response["le_text"] = """
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
        """

        self.response["SA_HE_FLOW_SESSION_EMPTY_XML"] = """
            <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
                <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                    <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                    <displayed-session-count>0</displayed-session-count>
                </flow-session-information>
                <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                    <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                    <displayed-session-count>0</displayed-session-count>
                </flow-session-information>
                <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                    <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                    <displayed-session-count>0</displayed-session-count>
                </flow-session-information>
                <cli>
                    <banner></banner>
                </cli>
            </rpc-reply>
        """

        self.response["SA_LE_FLOW_SESSION_WITH_MULTI_ENTRY"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-session junos:style="brief">
                    <session-identifier>70</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x80000040/0x0/0x800003</session-flag>
                    <policy>default-policy-logical-system-00/2</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>4</configured-timeout>
                    <timeout>2</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>95259</start-time>
                    <duration>3</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>100.1.0.2</source-address>
                        <source-port>2</source-port>
                        <destination-address>100.2.0.2</destination-address>
                        <destination-port>49983</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/2.0</interface-name>
                        <session-token>0x6</session-token>
                        <flag>0x21</flag>
                        <route>0x90010</route>
                        <gateway>100.1.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>100.2.0.2</source-address>
                        <source-port>49983</source-port>
                        <destination-address>100.1.0.2</destination-address>
                        <destination-port>2</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/3.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x20</flag>
                        <route>0xa0010</route>
                        <gateway>100.2.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>71</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x80000040/0x0/0x800003</session-flag>
                    <policy>default-policy-logical-system-00/2</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>4</configured-timeout>
                    <timeout>2</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>95260</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>100.1.0.2</source-address>
                        <source-port>3</source-port>
                        <destination-address>100.2.0.2</destination-address>
                        <destination-port>49983</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/2.0</interface-name>
                        <session-token>0x6</session-token>
                        <flag>0x21</flag>
                        <route>0x90010</route>
                        <gateway>100.1.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>100.2.0.2</source-address>
                        <source-port>49983</source-port>
                        <destination-address>100.1.0.2</destination-address>
                        <destination-port>3</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/3.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x20</flag>
                        <route>0xa0010</route>
                        <gateway>100.2.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>72</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x80000040/0x0/0x800003</session-flag>
                    <policy>default-policy-logical-system-00/2</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>4</configured-timeout>
                    <timeout>4</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>95261</start-time>
                    <duration>1</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>100.1.0.2</source-address>
                        <source-port>4</source-port>
                        <destination-address>100.2.0.2</destination-address>
                        <destination-port>49983</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/2.0</interface-name>
                        <session-token>0x6</session-token>
                        <flag>0x21</flag>
                        <route>0x90010</route>
                        <gateway>100.1.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>100.2.0.2</source-address>
                        <source-port>49983</source-port>
                        <destination-address>100.1.0.2</destination-address>
                        <destination-port>4</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/3.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x20</flag>
                        <route>0xa0010</route>
                        <gateway>100.2.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>73</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x80000040/0x0/0x800003</session-flag>
                    <policy>default-policy-logical-system-00/2</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>4</configured-timeout>
                    <timeout>4</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>95262</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>100.1.0.2</source-address>
                        <source-port>5</source-port>
                        <destination-address>100.2.0.2</destination-address>
                        <destination-port>49983</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/2.0</interface-name>
                        <session-token>0x6</session-token>
                        <flag>0x21</flag>
                        <route>0x90010</route>
                        <gateway>100.1.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>100.2.0.2</source-address>
                        <source-port>49983</source-port>
                        <destination-address>100.1.0.2</destination-address>
                        <destination-port>5</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/3.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x20</flag>
                        <route>0xa0010</route>
                        <gateway>100.2.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                </flow-session>
                <displayed-session-count>4</displayed-session-count>
            </flow-session-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["SA_LE_FLOW_SESSION_WITH_ONE_ENTRY"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-session junos:style="brief">
                    <session-identifier>70</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x80000040/0x0/0x800003</session-flag>
                    <policy>default-policy-logical-system-00/2</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>4</configured-timeout>
                    <timeout>2</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>95259</start-time>
                    <duration>3</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>100.1.0.2</source-address>
                        <source-port>2</source-port>
                        <destination-address>100.2.0.2</destination-address>
                        <destination-port>49983</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/2.0</interface-name>
                        <session-token>0x6</session-token>
                        <flag>0x21</flag>
                        <route>0x90010</route>
                        <gateway>100.1.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>100.2.0.2</source-address>
                        <source-port>49983</source-port>
                        <destination-address>100.1.0.2</destination-address>
                        <destination-port>2</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-0/0/3.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x20</flag>
                        <route>0xa0010</route>
                        <gateway>100.2.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["SA_LE_FLOW_SESSION_WITH_NO_ENTRY"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["not_well_format"] = """
        <reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>10000001</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x10000/0x0/0x1</session-flag>
                    <policy>N/A</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>N/A</configured-timeout>
                    <timeout>N/A</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>30</start-time>
                    <duration>1412</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>5ffd::2</source-address>
                        <source-port>1</source-port>
                        <destination-address>5ffd::1</destination-address>
                        <destination-port>1</destination-port>
                        <protocol>gre</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-5/2/1.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x80100623</flag>
                        <route>0x0</route>
                        <gateway>5ffd::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                        <dcp-session-id>0</dcp-session-id>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>10000002</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x10000/0x0/0x1</session-flag>
                    <policy>N/A</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>N/A</configured-timeout>
                    <timeout>N/A</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>30</start-time>
                    <duration>1412</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>50.0.0.2</source-address>
                        <source-port>1</source-port>
                        <destination-address>50.0.0.1</destination-address>
                        <destination-port>1</destination-port>
                        <protocol>gre</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-5/2/1.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x80100621</flag>
                        <route>0x0</route>
                        <gateway>50.0.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                        <dcp-session-id>0</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>2</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>20000001</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x10000/0x0/0x1</session-flag>
                    <policy>N/A</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>N/A</configured-timeout>
                    <timeout>N/A</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>30</start-time>
                    <duration>1411</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>5ffd::2</source-address>
                        <source-port>1</source-port>
                        <destination-address>5ffd::1</destination-address>
                        <destination-port>1</destination-port>
                        <protocol>gre</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-5/2/1.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x80100623</flag>
                        <route>0x0</route>
                        <gateway>5ffd::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                        <dcp-session-id>0</dcp-session-id>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>20000002</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x10000/0x0/0x1</session-flag>
                    <policy>N/A</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>N/A</configured-timeout>
                    <timeout>N/A</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>30</start-time>
                    <duration>1411</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>50.0.0.2</source-address>
                        <source-port>1</source-port>
                        <destination-address>50.0.0.1</destination-address>
                        <destination-port>1</destination-port>
                        <protocol>gre</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>ge-5/2/1.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x80100621</flag>
                        <route>0x0</route>
                        <gateway>50.0.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                        <dcp-session-id>0</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>2</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>30000001</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x10000/0x0/0x1</session-flag>
                    <policy>N/A</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <applicatition>
                    <start-time>29</start-time>
                    <duration>1376</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>5ffd::2</source-address>
                        <source-port>1</source-port>

                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                        <dcp-session-id>0</dcp-session-id>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>30000002</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x10000/0x0/0x1</session-flag>
        </reply>
        """

        self.response["flow_status"] = """
        <flow-status-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
            <flow-forwarding-mode>
                <flow-forwarding-mode-inet>flow based</flow-forwarding-mode-inet>
                <flow-forwarding-mode-inet6>flow based</flow-forwarding-mode-inet6>
                <flow-forwarding-mode-mpls>drop</flow-forwarding-mode-mpls>
                <flow-forwarding-mode-iso>drop</flow-forwarding-mode-iso>
            </flow-forwarding-mode>
            <flow-trace-option>
                <flow-trace-status>on</flow-trace-status>
                <flow-trace-options>all</flow-trace-options>
            </flow-trace-option>
            <flow-session-distribution>
                <mode>Hash-based</mode>
                <gtpu-distr-status>Disabled</gtpu-distr-status>
            </flow-session-distribution>
            <flow-ipsec-performance-acceleration>
                <ipa-status>off</ipa-status>
            </flow-ipsec-performance-acceleration>
            <flow-packet-ordering>
                <ordering-mode>Hardware</ordering-mode>
            </flow-packet-ordering>
        </flow-status-all>
        """

        self.response["FLOW_STATUS_TAP_MODE"] = """
    <flow-status-all>
        <flow-forwarding-mode>
            <flow-forwarding-mode-inet>flow based</flow-forwarding-mode-inet>
            <flow-forwarding-mode-inet6>flow based</flow-forwarding-mode-inet6>
            <flow-forwarding-mode-mpls>drop</flow-forwarding-mode-mpls>
            <flow-forwarding-mode-iso>drop</flow-forwarding-mode-iso>
            <flow-tap-mode>disabled (default)</flow-tap-mode>
            <flow-enhanced-services-mode>Disabled</flow-enhanced-services-mode>
        </flow-forwarding-mode>
        <flow-trace-option>
            <flow-trace-status>off</flow-trace-status>
        </flow-trace-option>
        <flow-session-distribution>
            <mode>Hash-based</mode>
            <gtpu-distr-status>Disabled</gtpu-distr-status>
        </flow-session-distribution>
        <flow-ipsec-performance-acceleration>
            <ipa-status>off</ipa-status>
        </flow-ipsec-performance-acceleration>
        <flow-packet-ordering>
            <ordering-mode>Hardware</ordering-mode>
        </flow-packet-ordering>
        <flow-power-mode-ipsec>
            <pmi-status>Disabled</pmi-status>
        </flow-power-mode-ipsec>
        <flow-fat-core-group>
            <fcg-status>off</fcg-status>
        </flow-fat-core-group>
        <utm-onbox-av-load-flavor>
        </utm-onbox-av-load-flavor>
    </flow-status-all>
        """

        self.response["HE_XML_FLOW_STATISTICS_INFO"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-statistics-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-spu-id> of FPC0 PIC1:</flow-spu-id>
                <flow-session-count-valid>4</flow-session-count-valid>
                <flow-pkt-count-fwd>122</flow-pkt-count-fwd>
                <flow-pkt-count-drop>0</flow-pkt-count-drop>
                <flow-frag-count-fwd>0</flow-frag-count-fwd>
                <flow-llf-pkt-count-prd>0</flow-llf-pkt-count-prd>
            </flow-statistics-all>
            <flow-statistics-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-spu-id> of FPC0 PIC2:</flow-spu-id>
                <flow-session-count-valid>4</flow-session-count-valid>
                <flow-pkt-count-fwd>117</flow-pkt-count-fwd>
                <flow-pkt-count-drop>1</flow-pkt-count-drop>
                <flow-frag-count-fwd>0</flow-frag-count-fwd>
                <flow-llf-pkt-count-prd>0</flow-llf-pkt-count-prd>
            </flow-statistics-all>
            <flow-statistics-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-spu-id> of FPC0 PIC3:</flow-spu-id>
                <flow-session-count-valid>4</flow-session-count-valid>
                <flow-pkt-count-fwd>261</flow-pkt-count-fwd>
                <flow-pkt-count-drop>0</flow-pkt-count-drop>
                <flow-frag-count-fwd>0</flow-frag-count-fwd>
                <flow-llf-pkt-count-prd>36</flow-llf-pkt-count-prd>
            </flow-statistics-all>
            <flow-statistics-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-spu-id> Summary:</flow-spu-id>
                <flow-session-valid-system>12</flow-session-valid-system>
                <flow-pkt-count-fwd>500</flow-pkt-count-fwd>
                <flow-pkt-count-drop>1</flow-pkt-count-drop>
                <flow-frag-count-fwd>0</flow-frag-count-fwd>
                <flow-llf-pkt-count-prd>36</flow-llf-pkt-count-prd>
            </flow-statistics-all>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["LE_HA_XML_FLOW_STATISTICS_AFTER_RLI36411"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.1D0/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-statistics-all xmlns="http://xml.juniper.net/junos/18.1D0/junos-flow">
                <flow-session-count-valid>0</flow-session-count-valid>
                <flow-pkt-count-rx>8</flow-pkt-count-rx>
                <flow-pkt-count-tx>8</flow-pkt-count-tx>
                <flow-pkt-count-fwd>0</flow-pkt-count-fwd>
                <flow-pkt-count-copy>0</flow-pkt-count-copy>
                <flow-pkt-count-drop>0</flow-pkt-count-drop>
                <flow-frag-count-fwd>0</flow-frag-count-fwd>
                <tunnel-frag-gen-pre>0</tunnel-frag-gen-pre>
                <tunnel-frag-gen-post>0</tunnel-frag-gen-post>
            </flow-statistics-all>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-statistics-all xmlns="http://xml.juniper.net/junos/18.1D0/junos-flow">
                <flow-session-count-valid>0</flow-session-count-valid>
                <flow-pkt-count-rx>1</flow-pkt-count-rx>
                <flow-pkt-count-tx>0</flow-pkt-count-tx>
                <flow-pkt-count-fwd>0</flow-pkt-count-fwd>
                <flow-pkt-count-copy>0</flow-pkt-count-copy>
                <flow-pkt-count-drop>1</flow-pkt-count-drop>
                <flow-frag-count-fwd>0</flow-frag-count-fwd>
                <tunnel-frag-gen-pre>0</tunnel-frag-gen-pre>
                <tunnel-frag-gen-post>0</tunnel-frag-gen-post>
            </flow-statistics-all>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["LE_SA_XML_FLOW_STATISTICS_AFTER_RLI36411"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.1D0/junos">
    <flow-statistics-all xmlns="http://xml.juniper.net/junos/18.1D0/junos-flow">
        <flow-session-count-valid>0</flow-session-count-valid>
        <flow-pkt-count-rx>8</flow-pkt-count-rx>
        <flow-pkt-count-tx>8</flow-pkt-count-tx>
        <flow-pkt-count-fwd>0</flow-pkt-count-fwd>
        <flow-pkt-count-copy>0</flow-pkt-count-copy>
        <flow-pkt-count-drop>0</flow-pkt-count-drop>
        <flow-frag-count-fwd>0</flow-frag-count-fwd>
        <tunnel-frag-gen-pre>0</tunnel-frag-gen-pre>
        <tunnel-frag-gen-post>0</tunnel-frag-gen-post>
    </flow-statistics-all>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["LE_SA_XML_FLOW_STATISTICS_INVALID"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.1D0/junos">
    <flow-statistics xmlns="http://xml.juniper.net/junos/18.1D0/junos-flow">
        <flow-session-count-valid>0</flow-session-count-valid>
        <flow-pkt-count-rx>8</flow-pkt-count-rx>
        <flow-pkt-count-tx>8</flow-pkt-count-tx>
        <flow-pkt-count-fwd>0</flow-pkt-count-fwd>
        <flow-pkt-count-copy>0</flow-pkt-count-copy>
        <flow-pkt-count-drop>0</flow-pkt-count-drop>
        <flow-frag-count-fwd>0</flow-frag-count-fwd>
        <tunnel-frag-gen-pre>0</tunnel-frag-gen-pre>
        <tunnel-frag-gen-post>0</tunnel-frag-gen-post>
    </flow-statistics>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["LE_XML_FLOW_STATISTICS_INFO"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-statistics-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-session-count-valid>0</flow-session-count-valid>
                <flow-pkt-count-fwd>1927</flow-pkt-count-fwd>
                <flow-pkt-count-drop>18</flow-pkt-count-drop>
                <flow-frag-count-fwd>0</flow-frag-count-fwd>
                <tunnel-frag-gen-pre>0</tunnel-frag-gen-pre>
                <tunnel-frag-gen-post>0</tunnel-frag-gen-post>
            </flow-statistics-all>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["LE_XML_NODE0_FLOW_STATISTICS_INFO"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-statistics-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-session-count-valid>0</flow-session-count-valid>
                        <flow-pkt-count-fwd>705</flow-pkt-count-fwd>
                        <flow-pkt-count-drop>705</flow-pkt-count-drop>
                        <flow-frag-count-fwd>0</flow-frag-count-fwd>
                        <tunnel-frag-gen-pre>0</tunnel-frag-gen-pre>
                        <tunnel-frag-gen-post>0</tunnel-frag-gen-post>
                    </flow-statistics-all>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{secondary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HE_XML_FLOW_GATE_INFO"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-gate-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC0 PIC1:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC0 PIC2:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC0 PIC3:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["LE_XML_FLOW_GATE_INFO"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-gate-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_NODE0_XML_FLOW_GATE_INFO"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-gate-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <displayed-gate-valid>0</displayed-gate-valid>
                        <displayed-gate-pending>0</displayed-gate-pending>
                        <displayed-gate-invalidated>0</displayed-gate-invalidated>
                        <displayed-gate-other>0</displayed-gate-other>
                        <displayed-gate-count>0</displayed-gate-count>
                    </flow-gate-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{primary:node1}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_MULTI_FPC"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>20000753</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1798</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1200007</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>58612</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>54093</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>39</pkt-cnt>
                        <byte-cnt>2816</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>54093</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>58612</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>93</pkt-cnt>
                        <byte-cnt>137776</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>30000755</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1800</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1199969</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>35597</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>2121</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>10</pkt-cnt>
                        <byte-cnt>806</byte-cnt>
                        <dcp-session-id>30002680</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>2121</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>35597</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>11</pkt-cnt>
                        <byte-cnt>1083</byte-cnt>
                        <dcp-session-id>30002680</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        # HighEnd Platform on SA topo that one FPC have single session
        self.response["SA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>20000753</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1798</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1200007</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>58612</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>54093</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>39</pkt-cnt>
                        <byte-cnt>2816</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>54093</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>58612</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>93</pkt-cnt>
                        <byte-cnt>137776</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        # HighEnd Platform on SA topo that one FPC have 2 sessions
        self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_ONE_FPC"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>30000755</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1800</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1199969</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>35597</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>2121</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>10</pkt-cnt>
                        <byte-cnt>806</byte-cnt>
                        <dcp-session-id>30002680</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>2121</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>35597</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>11</pkt-cnt>
                        <byte-cnt>1083</byte-cnt>
                        <dcp-session-id>30002680</dcp-session-id>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>20000753</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1798</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1200007</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>58612</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>54093</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>39</pkt-cnt>
                        <byte-cnt>2816</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>54093</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>58612</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>93</pkt-cnt>
                        <byte-cnt>137777</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>2</displayed-session-count>
            </flow-session-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        # HighEnd Platform on SA topo that one FPC have single session and another FPC have 2 sessions
        self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_MULTI_FPC_2"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>20000753</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1798</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1200007</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>58612</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>54093</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>39</pkt-cnt>
                        <byte-cnt>2816</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>54093</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>58612</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>93</pkt-cnt>
                        <byte-cnt>137776</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>30000755</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1800</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1199969</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>35597</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>2121</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>10</pkt-cnt>
                        <byte-cnt>806</byte-cnt>
                        <dcp-session-id>30002680</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>2121</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>35597</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>11</pkt-cnt>
                        <byte-cnt>1083</byte-cnt>
                        <dcp-session-id>30002680</dcp-session-id>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>20000753</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1798</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1200007</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>58612</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>54093</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>39</pkt-cnt>
                        <byte-cnt>2816</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>54093</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>58612</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>93</pkt-cnt>
                        <byte-cnt>137777</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>2</displayed-session-count>
            </flow-session-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """




        self.response["INVALID_HE_FLOW_FTP_SESSION"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <fpc-pic-id> on FPC0 PIC1:</fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <fpc-pic-id> on FPC0 PIC2:</fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>20000753</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1798</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1200007</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>58612</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>54093</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>39</pkt-cnt>
                        <byte-cnt>2816</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>54093</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>58612</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>93</pkt-cnt>
                        <byte-cnt>137776</byte-cnt>
                        <dcp-session-id>20002443</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <fpc-pic-id> on FPC0 PIC3:</fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>30000755</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x40/0x0/0x8003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1800</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1199969</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000:100::2</source-address>
                        <source-port>35597</source-port>
                        <destination-address>2000:200::2</destination-address>
                        <destination-port>2121</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40001023</flag>
                        <route>0xd0010</route>
                        <gateway>2000:100::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>10</pkt-cnt>
                        <byte-cnt>806</byte-cnt>
                        <dcp-session-id>30002680</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:200::2</source-address>
                        <source-port>2121</source-port>
                        <destination-address>2000:100::2</destination-address>
                        <destination-port>35597</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40001022</flag>
                        <route>0xe0010</route>
                        <gateway>2000:200::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>11</pkt-cnt>
                        <byte-cnt>1083</byte-cnt>
                        <dcp-session-id>30002680</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["HE_FLOW_ALL_ICMP_SESSION_IN_ONE_SPU"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>10000790</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x80000040/0x0/0x800003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>4</configured-timeout>
                    <timeout>2</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1218004</start-time>
                    <duration>2</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>192.168.100.2</source-address>
                        <source-port>25</source-port>
                        <destination-address>192.168.200.2</destination-address>
                        <destination-port>297</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40000021</flag>
                        <route>0x170010</route>
                        <gateway>192.168.100.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                        <dcp-session-id>10003118</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>192.168.200.2</source-address>
                        <source-port>297</source-port>
                        <destination-address>192.168.100.2</destination-address>
                        <destination-port>25</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40000020</flag>
                        <route>0x180010</route>
                        <gateway>192.168.200.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                        <dcp-session-id>10003118</dcp-session-id>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>10000791</session-identifier>
                    <status>Normal</status>
                    <session-flag>0x80000040/0x0/0x800003</session-flag>
                    <policy>p1/4</policy>
                    <nat-source-pool-name>Null</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>4</configured-timeout>
                    <timeout>2</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>1218005</start-time>
                    <duration>1</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>192.168.100.2</source-address>
                        <source-port>26</source-port>
                        <destination-address>192.168.200.2</destination-address>
                        <destination-port>297</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/0.0</interface-name>
                        <session-token>0x7</session-token>
                        <flag>0x40000021</flag>
                        <route>0x170010</route>
                        <gateway>192.168.100.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                        <dcp-session-id>10003119</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>192.168.200.2</source-address>
                        <source-port>297</source-port>
                        <destination-address>192.168.100.2</destination-address>
                        <destination-port>26</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>xe-2/0/1.0</interface-name>
                        <session-token>0x8</session-token>
                        <flag>0x40000020</flag>
                        <route>0x180010</route>
                        <gateway>192.168.200.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>1</pkt-cnt>
                        <byte-cnt>84</byte-cnt>
                        <dcp-session-id>10003119</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>2</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC_BOTH_2_NODE"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>1</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <flow-session junos:style="brief">
                            <session-identifier>10000003</session-identifier>
                            <status>Normal</status>
                            <session-state>Backup</session-state>
                            <session-flag>0x10000040/0x0/0x8003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>14400</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>83549</start-time>
                            <duration>18</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x60000021</flag>
                                <route>0x861d3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>0</pkt-cnt>
                                <byte-cnt>0</byte-cnt>
                                <dcp-session-id>10000002</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x60000020</flag>
                                <route>0x86043c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>0</pkt-cnt>
                                <byte-cnt>0</byte-cnt>
                                <dcp-session-id>10000002</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>1</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{secondary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC_IN_ONE_NODE"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>1</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{secondary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_ONE_FPC_IN_ONE_NODE"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>2</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{secondary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_HE_FLOW_SESSION_THAT_EMPTY"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{secondary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_HE_FLOW_SESSION_HAVE_3_ENTRIES_THAT_1_IN_A_FPC_AND_2_IN_OTHER_FPC"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>2</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{secondary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_LE_FLOW_SESSION_EMPTY"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{primary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_LE_FLOW_SESSION_THAT_ONE_ENTRY"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

               <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-session junos:style="brief">
                            <session-identifier>57</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8400040/0x0/0x108023</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <application-name>junos-telnet</application-name>
                            <application-value>10</application-value>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1784</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>70050</start-time>
                            <duration>16</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>31.0.1.1</source-address>
                                <source-port>55048</source-port>
                                <destination-address>11.0.1.1</destination-address>
                                <destination-port>23</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth0.0</interface-name>
                                <session-token>0x7</session-token>
                                <flag>0x1021</flag>
                                <route>0x4c6bc2</route>
                                <gateway>31.0.1.1</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>10</pkt-cnt>
                                <byte-cnt>676</byte-cnt>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>11.0.1.1</source-address>
                                <source-port>23</source-port>
                                <destination-address>31.0.1.1</destination-address>
                                <destination-port>55048</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>.local..0</interface-name>
                                <session-token>0x2</session-token>
                                <flag>0x1030</flag>
                                <route>0xfffb0006</route>
                                <gateway>11.0.1.1</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>8</pkt-cnt>
                                <byte-cnt>576</byte-cnt>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>1</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{primary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_LE_FLOW_SESSION_THAT_HAVE_MULTI_SESSIONS"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

               <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-session junos:style="brief">
                            <session-identifier>57</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8400040/0x0/0x108023</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <application-name>junos-telnet</application-name>
                            <application-value>10</application-value>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1784</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>70050</start-time>
                            <duration>16</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>31.0.1.1</source-address>
                                <source-port>55048</source-port>
                                <destination-address>11.0.1.1</destination-address>
                                <destination-port>23</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth0.0</interface-name>
                                <session-token>0x7</session-token>
                                <flag>0x1021</flag>
                                <route>0x4c6bc2</route>
                                <gateway>31.0.1.1</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>10</pkt-cnt>
                                <byte-cnt>676</byte-cnt>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>11.0.1.1</source-address>
                                <source-port>23</source-port>
                                <destination-address>31.0.1.1</destination-address>
                                <destination-port>55048</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>.local..0</interface-name>
                                <session-token>0x2</session-token>
                                <flag>0x1030</flag>
                                <route>0xfffb0006</route>
                                <gateway>11.0.1.1</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>8</pkt-cnt>
                                <byte-cnt>576</byte-cnt>
                            </flow-information>
                        </flow-session>
                        <flow-session junos:style="brief">
                            <session-identifier>2</session-identifier>
                            <status>Normal</status>
                            <session-state>Backup</session-state>
                            <session-flag>0x10400040/0x0/0x8023</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <application-name>junos-telnet</application-name>
                            <application-value>10</application-value>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>14388</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>69242</start-time>
                            <duration>15</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>31.0.1.1</source-address>
                                <source-port>55048</source-port>
                                <destination-address>11.0.1.1</destination-address>
                                <destination-port>23</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth0.0</interface-name>
                                <session-token>0x7</session-token>
                                <flag>0x21</flag>
                                <route>0x4f03c2</route>
                                <gateway>31.0.1.1</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>0</pkt-cnt>
                                <byte-cnt>0</byte-cnt>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>11.0.1.1</source-address>
                                <source-port>23</source-port>
                                <destination-address>31.0.1.1</destination-address>
                                <destination-port>55048</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>.local..0</interface-name>
                                <session-token>0x2</session-token>
                                <flag>0x30</flag>
                                <route>0xfffb0006</route>
                                <gateway>11.0.1.1</gateway>
                               <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>0</pkt-cnt>
                                <byte-cnt>0</byte-cnt>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>2</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{primary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_LE_FLOW_SESSION_THAT_HAVE_MULTI_SESSIONS_ON_BOTH_NODE"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

               <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-session junos:style="brief">
                            <session-identifier>57</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8400040/0x0/0x108023</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <application-name>junos-telnet</application-name>
                            <application-value>10</application-value>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1784</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>70050</start-time>
                            <duration>16</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>31.0.1.1</source-address>
                                <source-port>55048</source-port>
                                <destination-address>11.0.1.1</destination-address>
                                <destination-port>23</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth0.0</interface-name>
                                <session-token>0x7</session-token>
                                <flag>0x1021</flag>
                                <route>0x4c6bc2</route>
                                <gateway>31.0.1.1</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>10</pkt-cnt>
                                <byte-cnt>676</byte-cnt>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>11.0.1.1</source-address>
                                <source-port>23</source-port>
                                <destination-address>31.0.1.1</destination-address>
                                <destination-port>55048</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>.local..0</interface-name>
                                <session-token>0x2</session-token>
                                <flag>0x1030</flag>
                                <route>0xfffb0006</route>
                                <gateway>11.0.1.1</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>8</pkt-cnt>
                                <byte-cnt>576</byte-cnt>
                            </flow-information>
                        </flow-session>
                                                <flow-session junos:style="brief">
                            <session-identifier>2</session-identifier>
                            <status>Normal</status>
                            <session-state>Backup</session-state>
                            <session-flag>0x10400040/0x0/0x8023</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <application-name>junos-telnet</application-name>
                            <application-value>10</application-value>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>14388</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>69242</start-time>
                            <duration>15</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>31.0.1.1</source-address>
                                <source-port>55048</source-port>
                                <destination-address>11.0.1.1</destination-address>
                                <destination-port>23</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth0.0</interface-name>
                                <session-token>0x7</session-token>
                                <flag>0x21</flag>
                                <route>0x4f03c2</route>
                                <gateway>31.0.1.1</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>0</pkt-cnt>
                                <byte-cnt>0</byte-cnt>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>11.0.1.1</source-address>
                                <source-port>23</source-port>
                                <destination-address>31.0.1.1</destination-address>
                                <destination-port>55048</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>.local..0</interface-name>
                                <session-token>0x2</session-token>
                                <flag>0x30</flag>
                                <route>0xfffb0006</route>
                                <gateway>11.0.1.1</gateway>
                               <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>0</pkt-cnt>
                                <byte-cnt>0</byte-cnt>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>2</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-session junos:style="brief">
                            <session-identifier>2</session-identifier>
                            <status>Normal</status>
                            <session-state>Backup</session-state>
                            <session-flag>0x10400040/0x0/0x8023</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <application-name>junos-telnet</application-name>
                            <application-value>10</application-value>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>14388</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>69242</start-time>
                            <duration>15</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>31.0.1.1</source-address>
                                <source-port>55048</source-port>
                                <destination-address>11.0.1.1</destination-address>
                                <destination-port>23</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth0.0</interface-name>
                                <session-token>0x7</session-token>
                                <flag>0x21</flag>
                                <route>0x4f03c2</route>
                                <gateway>31.0.1.1</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>0</pkt-cnt>
                                <byte-cnt>0</byte-cnt>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>11.0.1.1</source-address>
                                <source-port>23</source-port>
                                <destination-address>31.0.1.1</destination-address>
                                <destination-port>55048</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>.local..0</interface-name>
                                <session-token>0x2</session-token>
                                <flag>0x30</flag>
                                <route>0xfffb0006</route>
                                <gateway>11.0.1.1</gateway>
                               <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>0</pkt-cnt>
                                <byte-cnt>0</byte-cnt>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>1</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{primary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_LE_FLOW_SESSION_INVALID_RESPONSE_THAT_ONLY_ONE_NODE_RESPONSE"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/12.3I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/12.3I0/junos-flow">
                        <flow-fpc-pic-id> on FPC1 PIC0:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/12.3I0/junos-flow">
                        <flow-fpc-pic-id> on FPC2 PIC0:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/12.3I0/junos-flow">
                        <flow-fpc-pic-id> on FPC3 PIC0:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/12.3I0/junos-flow">
                        <flow-fpc-pic-id> on FPC4 PIC0:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{primary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_HE_FLOW_SESSION_HAVE_ALG_ELEMENT"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <resource-manager-information junos:style="brief">
                                <client-name>FTP ALG</client-name>
                                <group-identifier>1</group-identifier>
                                <resource-identifier>0</resource-identifier>
                            </resource-manager-information>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>2</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <flow-session junos:style="brief">
                            <session-identifier>10000040</session-identifier>
                            <status>Normal</status>
                            <session-state>Active</session-state>
                            <session-flag>0x8000040/0x8000000/0x108003</session-flag>
                            <policy>default-policy-logical-system-00/2</policy>
                            <nat-source-pool-name>Null</nat-source-pool-name>
                            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                            <encryption-traffic-name> Unknown</encryption-traffic-name>
                            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                            <configured-timeout>1800</configured-timeout>
                            <timeout>1788</timeout>
                            <sess-state>Valid</sess-state>
                            <logical-system></logical-system>
                            <wan-acceleration></wan-acceleration>
                            <start-time>82632</start-time>
                            <duration>17</duration>
                            <session-mask>0</session-mask>
                            <flow-information junos:style="brief">
                                <direction>In</direction>
                                <source-address>192.168.100.2</source-address>
                                <source-port>52072</source-port>
                                <destination-address>192.168.200.2</destination-address>
                                <destination-port>2121</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth1.0</interface-name>
                                <session-token>0x6</session-token>
                                <flag>0x40001021</flag>
                                <route>0x861c3c2</route>
                                <gateway>192.168.100.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>9</pkt-cnt>
                                <byte-cnt>508</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                            <flow-information junos:style="brief">
                                <direction>Out</direction>
                                <source-address>192.168.200.2</source-address>
                                <source-port>2121</source-port>
                                <destination-address>192.168.100.2</destination-address>
                                <destination-port>52072</destination-port>
                                <protocol>tcp</protocol>
                                <conn-tag>0x0</conn-tag>
                                <interface-name>reth2.0</interface-name>
                                <session-token>0x8</session-token>
                                <flag>0x40001020</flag>
                                <route>0x432e3c2</route>
                                <gateway>192.168.200.2</gateway>
                                <tunnel-information>0</tunnel-information>
                                <port-sequence>0</port-sequence>
                                <fin-sequence>0</fin-sequence>
                                <fin-state>0</fin-state>
                                <seq-ack-diff>0</seq-ack-diff>
                                <pkt-cnt>6</pkt-cnt>
                                <byte-cnt>450</byte-cnt>
                                <dcp-session-id>10000364</dcp-session-id>
                            </flow-information>
                        </flow-session>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                        <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                        <displayed-session-count>0</displayed-session-count>
                    </flow-session-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{secondary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["INVALID_FLOW_STATUS_RESPONSE"] = """
        <flow-status-al xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
            <flow-forwarding-mod>
                <flow-forwarding-mode-ine>flow based</flow-forwarding-mode-ine>
                <flow-forwarding-mode-ine6>flow based</flow-forwarding-mode-ine6>
                <flow-forwarding-mode-mpl>drop</flow-forwarding-mode-mpl>
                <flow-forwarding-mode-is>drop</flow-forwarding-mode-is>
            </flow-forwarding-mod>
            <flow-trace-optio>
                <flow-trace-statu>on</flow-trace-statu>
                <flow-trace-optio>all</flow-trace-optio>
            </flow-trace-optio>
            <flow-session-distributio>
                <mod>Hash-based</mod>
                <gtpu-distr-stat>Disabled</gtpu-distr-stat>
            </flow-session-distributio>
            <flow-ipsec-performance-acceleratio>
                <ipa-statu>off</ipa-statu>
            </flow-ipsec-performance-acceleratio>
            <flow-packet-orderin>
                <ordering-mod>Hardware</ordering-mod>
            </flow-packet-orderin>
        </flow-status-al>
        """

        self.response["FLOW_STATUS_FROM_HA_NODE0"] = """
        <multi-routing-engine-results>

            <multi-routing-engine-item>

                <re-name>node0</re-name>

                <flow-status-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                    <flow-forwarding-mode>
                        <flow-forwarding-mode-inet>flow based</flow-forwarding-mode-inet>
                        <flow-forwarding-mode-inet6>flow based</flow-forwarding-mode-inet6>
                        <flow-forwarding-mode-mpls>drop</flow-forwarding-mode-mpls>
                        <flow-forwarding-mode-iso>drop</flow-forwarding-mode-iso>
                        <flow-enhanced-routing-mode>Disabled</flow-enhanced-routing-mode>
                    </flow-forwarding-mode>
                    <flow-trace-option>
                        <flow-trace-status>off</flow-trace-status>
                    </flow-trace-option>
                    <flow-session-distribution>
                        <mode>RR-based</mode>
                        <gtpu-distr-status>Disabled</gtpu-distr-status>
                    </flow-session-distribution>
                    <flow-ipsec-performance-acceleration>
                        <ipa-status>off</ipa-status>
                    </flow-ipsec-performance-acceleration>
                    <flow-packet-ordering>
                        <ordering-mode>Hardware</ordering-mode>
                    </flow-packet-ordering>
                </flow-status-all>
            </multi-routing-engine-item>

        </multi-routing-engine-results>
        """

        self.response["FLOW_STATUS_FROM_HA_NODE1"] = """
        <multi-routing-engine-results>

            <multi-routing-engine-item>

                <re-name>node1</re-name>

                <flow-status-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                    <flow-forwarding-mode>
                        <flow-forwarding-mode-inet>flow based</flow-forwarding-mode-inet>
                        <flow-forwarding-mode-inet6>flow based</flow-forwarding-mode-inet6>
                        <flow-forwarding-mode-mpls>drop</flow-forwarding-mode-mpls>
                        <flow-forwarding-mode-iso>drop</flow-forwarding-mode-iso>
                        <flow-enhanced-routing-mode>Disabled</flow-enhanced-routing-mode>
                    </flow-forwarding-mode>
                    <flow-trace-option>
                        <flow-trace-status>off</flow-trace-status>
                    </flow-trace-option>
                    <flow-session-distribution>
                        <mode>RR-based</mode>
                        <gtpu-distr-status>Disabled</gtpu-distr-status>
                    </flow-session-distribution>
                    <flow-ipsec-performance-acceleration>
                        <ipa-status>off</ipa-status>
                    </flow-ipsec-performance-acceleration>
                    <flow-packet-ordering>
                        <ordering-mode>Hardware</ordering-mode>
                    </flow-packet-ordering>
                </flow-status-all>
            </multi-routing-engine-item>

        </multi-routing-engine-results>
        """

        self.response["FLOW_STATUS_WITH_ERROR_MSG"] = """
            <multi-routing-engine-results>

            <multi-routing-engine-item>

            <re-name>node0</re-name>
            <flow-status-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                    <flow-forwarding-mode>
                        <flow-forwarding-mode-inet>flow based</flow-forwarding-mode-inet>
                        <flow-forwarding-mode-inet6>flow based</flow-forwarding-mode-inet6>
                        <flow-forwarding-mode-mpls>drop</flow-forwarding-mode-mpls>
                        <flow-forwarding-mode-iso>drop</flow-forwarding-mode-iso>
                        <flow-enhanced-routing-mode>Disabled</flow-enhanced-routing-mode>
                    </flow-forwarding-mode>
                    <flow-trace-option>
                        <flow-trace-status>off</flow-trace-status>
                    </flow-trace-option>
                    <flow-session-distribution>
                        <mode>RR-based</mode>
                        <gtpu-distr-status>Disabled</gtpu-distr-status>
                    </flow-session-distribution>
                    <flow-ipsec-performance-acceleration>
                        <ipa-status>off</ipa-status>
                    </flow-ipsec-performance-acceleration>
                    <flow-packet-ordering>
                        <ordering-mode>Hardware</ordering-mode>
                    </flow-packet-ordering>
            </flow-status-all>
            <error>
            <source-daemon>/usr/sbin/uspinfo</source-daemon>
            <message>usp_ipc_client_recv: failed to read message from ipc pipe</message>
            </error>
            </multi-routing-engine-item>

            </multi-routing-engine-results>
        """

        self.response["FLOW_SESSION_FROM_SINGLE_NODE"] = """
            <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
                <multi-routing-engine-results>

                    <multi-routing-engine-item>

                        <re-name>node1</re-name>

                        <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                            <flow-session junos:style="brief">
                                <session-identifier>335</session-identifier>
                                <status>Normal</status>
                                <session-state>Active</session-state>
                                <session-flag>0x80000040/0x8000000/0x800003</session-flag>
                                <policy>default-policy-logical-system-00/2</policy>
                                <nat-source-pool-name>Null</nat-source-pool-name>
                                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                                <encryption-traffic-name> Unknown</encryption-traffic-name>
                                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                                <configured-timeout>4</configured-timeout>
                                <timeout>2</timeout>
                                <sess-state>Valid</sess-state>
                                <logical-system></logical-system>
                                <wan-acceleration></wan-acceleration>
                                <start-time>271675</start-time>
                                <duration>2</duration>
                                <session-mask>0</session-mask>
                                <flow-information junos:style="brief">
                                    <direction>In</direction>
                                    <source-address>192.168.100.2</source-address>
                                    <source-port>329</source-port>
                                    <destination-address>192.168.200.2</destination-address>
                                    <destination-port>30556</destination-port>
                                    <protocol>icmp</protocol>
                                    <conn-tag>0x0</conn-tag>
                                    <interface-name>reth1.0</interface-name>
                                    <session-token>0x7</session-token>
                                    <flag>0x21</flag>
                                    <route>0x50f3c2</route>
                                    <gateway>192.168.100.2</gateway>
                                    <tunnel-information>0</tunnel-information>
                                    <port-sequence>0</port-sequence>
                                    <fin-sequence>0</fin-sequence>
                                    <fin-state>0</fin-state>
                                    <seq-ack-diff>0</seq-ack-diff>
                                    <pkt-cnt>1</pkt-cnt>
                                    <byte-cnt>84</byte-cnt>
                                </flow-information>
                                <flow-information junos:style="brief">
                                    <direction>Out</direction>
                                    <source-address>192.168.200.2</source-address>
                                    <source-port>30556</source-port>
                                    <destination-address>192.168.100.2</destination-address>
                                    <destination-port>329</destination-port>
                                    <protocol>icmp</protocol>
                                    <conn-tag>0x0</conn-tag>
                                    <interface-name>reth2.0</interface-name>
                                    <session-token>0x8</session-token>
                                    <flag>0x20</flag>
                                    <route>0x4e23c2</route>
                                    <gateway>192.168.200.2</gateway>
                                    <tunnel-information>0</tunnel-information>
                                    <port-sequence>0</port-sequence>
                                    <fin-sequence>0</fin-sequence>
                                    <fin-state>0</fin-state>
                                    <seq-ack-diff>0</seq-ack-diff>
                                    <pkt-cnt>1</pkt-cnt>
                                    <byte-cnt>84</byte-cnt>
                                </flow-information>
                            </flow-session>
                            <flow-session junos:style="brief">
                                <session-identifier>336</session-identifier>
                                <status>Normal</status>
                                <session-state>Active</session-state>
                                <session-flag>0x80000040/0x8000000/0x800003</session-flag>
                                <policy>default-policy-logical-system-00/2</policy>
                                <nat-source-pool-name>Null</nat-source-pool-name>
                                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                                <encryption-traffic-name> Unknown</encryption-traffic-name>
                                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                                <configured-timeout>4</configured-timeout>
                                <timeout>2</timeout>
                                <sess-state>Valid</sess-state>
                                <logical-system></logical-system>
                                <wan-acceleration></wan-acceleration>
                                <start-time>271676</start-time>
                                <duration>1</duration>
                                <session-mask>0</session-mask>
                                <flow-information junos:style="brief">
                                    <direction>In</direction>
                                    <source-address>192.168.100.2</source-address>
                                    <source-port>330</source-port>
                                    <destination-address>192.168.200.2</destination-address>
                                    <destination-port>30556</destination-port>
                                    <protocol>icmp</protocol>
                                    <conn-tag>0x0</conn-tag>
                                    <interface-name>reth1.0</interface-name>
                                    <session-token>0x7</session-token>
                                    <flag>0x21</flag>
                                    <route>0x50f3c2</route>
                                    <gateway>192.168.100.2</gateway>
                                    <tunnel-information>0</tunnel-information>
                                    <port-sequence>0</port-sequence>
                                    <fin-sequence>0</fin-sequence>
                                    <fin-state>0</fin-state>
                                    <seq-ack-diff>0</seq-ack-diff>
                                    <pkt-cnt>1</pkt-cnt>
                                    <byte-cnt>84</byte-cnt>
                                </flow-information>
                                <flow-information junos:style="brief">
                                    <direction>Out</direction>
                                    <source-address>192.168.200.2</source-address>
                                    <source-port>30556</source-port>
                                    <destination-address>192.168.100.2</destination-address>
                                    <destination-port>330</destination-port>
                                    <protocol>icmp</protocol>
                                    <conn-tag>0x0</conn-tag>
                                    <interface-name>reth2.0</interface-name>
                                    <session-token>0x8</session-token>
                                    <flag>0x20</flag>
                                    <route>0x4e23c2</route>
                                    <gateway>192.168.200.2</gateway>
                                    <tunnel-information>0</tunnel-information>
                                    <port-sequence>0</port-sequence>
                                    <fin-sequence>0</fin-sequence>
                                    <fin-state>0</fin-state>
                                    <seq-ack-diff>0</seq-ack-diff>
                                    <pkt-cnt>1</pkt-cnt>
                                    <byte-cnt>84</byte-cnt>
                                </flow-information>
                            </flow-session>
                            <displayed-session-count>2</displayed-session-count>
                        </flow-session-information>
                    </multi-routing-engine-item>

                </multi-routing-engine-results>
                <cli>
                    <banner>{secondary:node0}</banner>
                </cli>
            </rpc-reply>
        """

        self.response["SA_LE_FLOW_SESSION_RESOURCE_MANAGER"] = """
    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
        <flow-session junos:style="brief">
            <session-identifier>398</session-identifier>
            <status>Normal</status>
            <session-flag>0x0/0x20000000/0x10103</session-flag>
            <policy>p1/4</policy>
            <nat-source-pool-name>pool1</nat-source-pool-name>
            <application-name>junos-ftp</application-name>
            <application-value>1</application-value>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>1800</configured-timeout>
            <timeout>1796</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>97295</start-time>
            <duration>6</duration>
            <session-mask>0</session-mask>
            <module-name>resource-manager</module-name>
            <internal-module-identifier>0</internal-module-identifier>
            <resource-manager-information junos:style="brief">
                <client-name>FTP ALG</client-name>
                <group-identifier>1</group-identifier>
                <resource-identifier>0</resource-identifier>
            </resource-manager-information>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>11.33.55.7</source-address>
                <source-port>42305</source-port>
                <destination-address>22.44.66.8</destination-address>
                <destination-port>21</destination-port>
                <protocol>tcp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/0.0</interface-name>
                <session-token>0x7</session-token>
                <flag>0x621</flag>
                <route>0xb0010</route>
                <gateway>11.33.55.7</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>9</pkt-cnt>
                <byte-cnt>439</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>22.44.66.8</source-address>
                <source-port>21</source-port>
                <destination-address>12.12.12.12</destination-address>
                <destination-port>13232</destination-port>
                <protocol>tcp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x620</flag>
                <route>0xa0010</route>
                <gateway>1.1.1.2</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>12</pkt-cnt>
                <byte-cnt>696</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>399</session-identifier>
            <status>Normal</status>
            <session-flag>0x4001000/0x0/0x8103</session-flag>
            <policy>p1/4</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <application-name>junos-ftp-data</application-name>
            <application-value>79</application-value>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>300</configured-timeout>
            <timeout>300</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>97295</start-time>
            <duration>6</duration>
            <session-mask>0</session-mask>
            <module-name>resource-manager</module-name>
            <internal-module-identifier>0</internal-module-identifier>
            <resource-manager-information junos:style="brief">
                <client-name>FTP ALG</client-name>
                <group-identifier>1</group-identifier>
                <resource-identifier>1</resource-identifier>
            </resource-manager-information>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>11.33.55.7</source-address>
                <source-port>40786</source-port>
                <destination-address>22.44.66.8</destination-address>
                <destination-port>49960</destination-port>
                <protocol>tcp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/0.0</interface-name>
                <session-token>0x7</session-token>
                <flag>0x1021</flag>
                <route>0xb0010</route>
                <gateway>11.33.55.7</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>11466</pkt-cnt>
                <byte-cnt>600352</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>22.44.66.8</source-address>
                <source-port>49960</source-port>
                <destination-address>12.12.12.12</destination-address>
                <destination-port>9655</destination-port>
                <protocol>tcp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x1020</flag>
                <route>0xa0010</route>
                <gateway>1.1.1.2</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>69961</pkt-cnt>
                <byte-cnt>96325908</byte-cnt>
            </flow-information>
        </flow-session>
        <displayed-session-count>2</displayed-session-count>
    </flow-session-information>
        """

        self.response["HA_HE_FLOW_SESSION_SUMMARY"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
            </flow-session-information>
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <active-unicast-sessions>0</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <active-services-offload-sessions>0</active-services-offload-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>0</active-sessions>
                <active-session-valid>0</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>0</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>6291456</max-sessions>
            </flow-session-summary-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow"></flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
            </flow-session-information>
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <active-unicast-sessions>0</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <active-services-offload-sessions>0</active-services-offload-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>0</active-sessions>
                <active-session-valid>0</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>0</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>6291456</max-sessions>
            </flow-session-summary-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow"></flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
            </flow-session-information>
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <active-unicast-sessions>0</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <active-services-offload-sessions>0</active-services-offload-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>0</active-sessions>
                <active-session-valid>0</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>0</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>6291456</max-sessions>
            </flow-session-summary-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow"></flow-session-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
            </flow-session-information>
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <active-unicast-sessions>0</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <active-services-offload-sessions>0</active-services-offload-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>1</active-sessions>
                <active-session-valid>0</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>1</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>6291456</max-sessions>
            </flow-session-summary-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow"></flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
            </flow-session-information>
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <active-unicast-sessions>2</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <active-services-offload-sessions>0</active-services-offload-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>3</active-sessions>
                <active-session-valid>2</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>1</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>6291456</max-sessions>
            </flow-session-summary-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow"></flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
            </flow-session-information>
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <active-unicast-sessions>2</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <active-services-offload-sessions>0</active-services-offload-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>4</active-sessions>
                <active-session-valid>2</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>2</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>6291456</max-sessions>
            </flow-session-summary-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow"></flow-session-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["SA_LE_FLOW_SESSION_SUMMARY"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
    </flow-session-information>
    <flow-session-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
        <active-unicast-sessions>4</active-unicast-sessions>
        <active-multicast-sessions>0</active-multicast-sessions>
        <failed-sessions>0</failed-sessions>
        <active-sessions>6</active-sessions>
        <active-session-valid>4</active-session-valid>
        <active-session-pending>0</active-session-pending>
        <active-session-invalidated>2</active-session-invalidated>
        <active-session-other>0</active-session-other>
        <max-sessions>524288</max-sessions>
    </flow-session-summary-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["FLOW_SESSION_SUMMARY_WITH_NO_INFORMATION"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <flow-session-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
        <active-unicast-sessions>4</active-unicast-sessions>
        <active-multicast-sessions>0</active-multicast-sessions>
        <failed-sessions>0</failed-sessions>
        <active-sessions>6</active-sessions>
        <active-session-valid>4</active-session-valid>
        <active-session-pending>0</active-session-pending>
        <active-session-invalidated>2</active-session-invalidated>
        <active-session-other>0</active-session-other>
        <max-sessions>524288</max-sessions>
    </flow-session-summary-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """


        self.response["HA_LE_FLOW_SESSION_SUMMARY_WITH_MORE_OPTIONS"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.2I0/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-flow">
                <displayed-session-valid>0</displayed-session-valid>
                <displayed-session-pending>0</displayed-session-pending>
                <displayed-session-invalidated>0</displayed-session-invalidated>
                <displayed-session-other>0</displayed-session-other>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-flow">
                <displayed-session-valid>0</displayed-session-valid>
                <displayed-session-pending>0</displayed-session-pending>
                <displayed-session-invalidated>0</displayed-session-invalidated>
                <displayed-session-other>0</displayed-session-other>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["SA_HE_FLOW_SESSION_SUMMARY_WITH_MORE_OPTIONS"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.2I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-flow">
        <flow-fpc-pic-id> on FPC6 PIC1:</flow-fpc-pic-id>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-flow">
        <flow-fpc-pic-id> on FPC6 PIC2:</flow-fpc-pic-id>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-flow">
        <flow-fpc-pic-id> on FPC6 PIC3:</flow-fpc-pic-id>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["SA_HE_FLOW_SESSION_SUMMARY_FOR_ROOT_TAG"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.3I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>9</flow-fpc-id>
            <flow-pic-id>1</flow-pic-id>
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <active-unicast-sessions>1</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <active-services-offload-sessions>0</active-services-offload-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>1</active-sessions>
                <active-session-valid>1</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>0</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>6291456</max-sessions>
            </flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>9</flow-fpc-id>
            <flow-pic-id>2</flow-pic-id>
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <active-unicast-sessions>1</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <active-services-offload-sessions>0</active-services-offload-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>2</active-sessions>
                <active-session-valid>1</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>0</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>6291456</max-sessions>
            </flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>9</flow-fpc-id>
            <flow-pic-id>3</flow-pic-id>
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <active-unicast-sessions>1</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <active-services-offload-sessions>0</active-services-offload-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>3</active-sessions>
                <active-session-valid>1</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>0</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>6291456</max-sessions>
            </flow-session-summary-information>
        </flow-session-per-pic>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["HA_LE_FLOW_SESSION_SUMMARY_FOR_ROOT_TAG"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.3I0/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                    <flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                        <active-unicast-sessions>0</active-unicast-sessions>
                        <active-multicast-sessions>0</active-multicast-sessions>
                        <active-services-offload-sessions>0</active-services-offload-sessions>
                        <failed-sessions>0</failed-sessions>
                        <active-sessions>0</active-sessions>
                        <active-session-valid>0</active-session-valid>
                        <active-session-pending>0</active-session-pending>
                        <active-session-invalidated>0</active-session-invalidated>
                        <active-session-other>0</active-session-other>
                        <max-sessions>4194304</max-sessions>
                    </flow-session-summary-information>
                </flow-session-per-pic>
            </flow-session-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                    <flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                        <active-unicast-sessions>0</active-unicast-sessions>
                        <active-multicast-sessions>0</active-multicast-sessions>
                        <active-services-offload-sessions>0</active-services-offload-sessions>
                        <failed-sessions>0</failed-sessions>
                        <active-sessions>1</active-sessions>
                        <active-session-valid>0</active-session-valid>
                        <active-session-pending>0</active-session-pending>
                        <active-session-invalidated>1</active-session-invalidated>
                        <active-session-other>0</active-session-other>
                        <max-sessions>4194304</max-sessions>
                    </flow-session-summary-information>
                </flow-session-per-pic>
            </flow-session-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{secondary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["SA_HE_FLOW_SESSION_SUMMARY_WITH_MORE_OPTION_FOR_ROOT_TAG"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.3I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>6</flow-fpc-id>
            <flow-pic-id>1</flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>1</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>0</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>0</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>0</dcp-displayed-session-other>
                <dcp-displayed-session-count>1</dcp-displayed-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>6</flow-fpc-id>
            <flow-pic-id>2</flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>1</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>0</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>0</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>0</dcp-displayed-session-other>
                <dcp-displayed-session-count>1</dcp-displayed-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>6</flow-fpc-id>
            <flow-pic-id>3</flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>0</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>0</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>0</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>0</dcp-displayed-session-other>
                <dcp-displayed-session-count>0</dcp-displayed-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>7</flow-fpc-id>
            <flow-pic-id>0</flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>0</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>0</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>0</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>0</dcp-displayed-session-other>
                <dcp-displayed-session-count>0</dcp-displayed-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>7</flow-fpc-id>
            <flow-pic-id>1</flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>0</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>0</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>0</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>0</dcp-displayed-session-other>
                <dcp-displayed-session-count>0</dcp-displayed-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>7</flow-fpc-id>
            <flow-pic-id>2</flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>0</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>0</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>0</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>0</dcp-displayed-session-other>
                <dcp-displayed-session-count>0</dcp-displayed-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <flow-fpc-id>7</flow-fpc-id>
            <flow-pic-id>3</flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>0</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>0</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>0</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>0</dcp-displayed-session-other>
                <dcp-displayed-session-count>0</dcp-displayed-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["HA_HE_FLOW_CP_SESSION"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC1:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC2:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC3:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC1:</dcp-flow-fpc-pic-id>
                <flow-session junos:style="terse">
                    <session-identifier>10040149</session-identifier>
                    <status></status>
                    <session-flag>0x180000</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>3</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>0.0.0.0</source-address>
                        <source-port>0</source-port>
                        <destination-address>0.0.0.0</destination-address>
                        <destination-port>0</destination-port>
                        <protocol>0</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>121.11.20.2</source-address>
                        <source-port>47629</source-port>
                        <destination-address>121.11.15.11</destination-address>
                        <destination-port>1135</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="terse">
                    <session-identifier>10040150</session-identifier>
                    <status></status>
                    <session-flag>0x180000</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>3</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>0.0.0.0</source-address>
                        <source-port>0</source-port>
                        <destination-address>0.0.0.0</destination-address>
                        <destination-port>0</destination-port>
                        <protocol>0</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>121.11.20.2</source-address>
                        <source-port>47629</source-port>
                        <destination-address>121.11.15.11</destination-address>
                        <destination-port>1113</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="terse">
                    <session-identifier>10040151</session-identifier>
                    <status></status>
                    <session-flag>0xc00001</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>1</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>121.11.10.2</source-address>
                        <source-port>1567</source-port>
                        <destination-address>121.11.20.2</destination-address>
                        <destination-port>47629</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>121.11.20.2</source-address>
                        <source-port>47629</source-port>
                        <destination-address>121.11.15.11</destination-address>
                        <destination-port>1147</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <displayed-session-count>3</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC2:</dcp-flow-fpc-pic-id>
                <flow-session junos:style="terse">
                    <session-identifier>20039231</session-identifier>
                    <status></status>
                    <session-flag>0xc00005</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>2</session-spu-id>
                    <sess-state>Invalidated</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>121.11.10.2</source-address>
                        <source-port>1564</source-port>
                        <destination-address>121.11.20.2</destination-address>
                        <destination-port>47629</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>121.11.20.2</source-address>
                        <source-port>47629</source-port>
                        <destination-address>121.11.15.11</destination-address>
                        <destination-port>1130</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="terse">
                    <session-identifier>20039232</session-identifier>
                    <status></status>
                    <session-flag>0xc00001</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>2</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>121.11.10.2</source-address>
                        <source-port>1568</source-port>
                        <destination-address>121.11.20.2</destination-address>
                        <destination-port>47629</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>0.0.0.0</source-address>
                        <source-port>0</source-port>
                        <destination-address>0.0.0.0</destination-address>
                        <destination-port>0</destination-port>
                        <protocol>0</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <displayed-session-count>2</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC3:</dcp-flow-fpc-pic-id>
                <flow-session junos:style="terse">
                    <session-identifier>30039283</session-identifier>
                    <status></status>
                    <session-flag>0xc00005</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>3</session-spu-id>
                    <sess-state>Invalidated</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>121.11.10.2</source-address>
                        <source-port>1565</source-port>
                        <destination-address>121.11.20.2</destination-address>
                        <destination-port>47629</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>0.0.0.0</source-address>
                        <source-port>0</source-port>
                        <destination-address>0.0.0.0</destination-address>
                        <destination-port>0</destination-port>
                        <protocol>0</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="terse">
                    <session-identifier>30039284</session-identifier>
                    <status></status>
                    <session-flag>0xc00000</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>3</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>121.11.10.2</source-address>
                        <source-port>1566</source-port>
                        <destination-address>121.11.20.2</destination-address>
                        <destination-port>47629</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>0.0.0.0</source-address>
                        <source-port>0</source-port>
                        <destination-address>0.0.0.0</destination-address>
                        <destination-port>0</destination-port>
                        <protocol>0</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="terse">
                    <session-identifier>30039285</session-identifier>
                    <status></status>
                    <session-flag>0x180000</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>2</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>0.0.0.0</source-address>
                        <source-port>0</source-port>
                        <destination-address>0.0.0.0</destination-address>
                        <destination-port>0</destination-port>
                        <protocol>0</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>121.11.20.2</source-address>
                        <source-port>47629</source-port>
                        <destination-address>121.11.15.11</destination-address>
                        <destination-port>1097</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="terse">
                    <session-identifier>30039286</session-identifier>
                    <status></status>
                    <session-flag>0xc00001</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>3</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>121.11.10.2</source-address>
                        <source-port>1569</source-port>
                        <destination-address>121.11.20.2</destination-address>
                        <destination-port>47629</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>0.0.0.0</source-address>
                        <source-port>0</source-port>
                        <destination-address>0.0.0.0</destination-address>
                        <destination-port>0</destination-port>
                        <protocol>0</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <displayed-session-count>4</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["SA_HE_FLOW_SESSION_SUMMARY_WITH_ROOT_TAG"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/19.4I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/19.4I0/junos-flow">
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/19.4I0/junos-flow">
            <!-- keep alive -->
            <!-- keep alive -->
            <!-- keep alive -->
            <!-- keep alive -->
            <!-- keep alive -->
            <!-- keep alive -->
            <flow-session-summary-information xmlns="http://xml.juniper.net/junos/19.4I0/junos-flow">
                <active-unicast-sessions>519192</active-unicast-sessions>
                <active-multicast-sessions>0</active-multicast-sessions>
                <failed-sessions>0</failed-sessions>
                <active-sessions>519192</active-sessions>
                <active-session-valid>519192</active-session-valid>
                <active-session-pending>0</active-session-pending>
                <active-session-invalidated>0</active-session-invalidated>
                <active-session-other>0</active-session-other>
                <max-sessions>524288</max-sessions>
            </flow-session-summary-information>
        </flow-session-per-pic>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["SA_LE_FLOW_CP_SESSION_EMPTY"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4D0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-flow">
        <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-flow">
        <dcp-flow-fpc-pic-id> on FPC0 PIC1:</dcp-flow-fpc-pic-id>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-flow">
        <dcp-flow-fpc-pic-id> on FPC0 PIC2:</dcp-flow-fpc-pic-id>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-flow">
        <dcp-flow-fpc-pic-id> on FPC0 PIC3:</dcp-flow-fpc-pic-id>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["HA_HE_FLOW_CP_SESSION_WITH_ONE_SPU_AND_ONE_SESSION"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC1:</dcp-flow-fpc-pic-id>
                <flow-session junos:style="terse">
                    <session-identifier>10040149</session-identifier>
                    <status></status>
                    <session-flag>0x180000</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>3</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>In</direction>
                        <source-address>0.0.0.0</source-address>
                        <source-port>0</source-port>
                        <destination-address>0.0.0.0</destination-address>
                        <destination-port>0</destination-port>
                        <protocol>0</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>121.11.20.2</source-address>
                        <source-port>47629</source-port>
                        <destination-address>121.11.15.11</destination-address>
                        <destination-port>1135</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["HA_HE_FLOW_CP_SESSION_FOR_NO_WING"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC1:</dcp-flow-fpc-pic-id>
                <flow-session junos:style="terse">
                    <session-identifier>10040149</session-identifier>
                    <status></status>
                    <session-flag>0x180000</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>3</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["HA_HE_FLOW_CP_SESSION_FOR_ONE_WAY_WING"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC1:</dcp-flow-fpc-pic-id>
                <flow-session junos:style="terse">
                    <session-identifier>10040149</session-identifier>
                    <status></status>
                    <session-flag>0x180000</session-flag>
                    <policy></policy>
                    <nat-source-pool-name></nat-source-pool-name>
                    <application-name></application-name>
                    <application-value>0</application-value>
                    <dynamic-application-name>INVALID</dynamic-application-name>
                    <configured-timeout>0</configured-timeout>
                    <timeout>0</timeout>
                    <session-spu-id>3</session-spu-id>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>0</start-time>
                    <duration>0</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="terse">
                        <direction>Out</direction>
                        <source-address>121.11.20.2</source-address>
                        <source-port>47629</source-port>
                        <destination-address>121.11.15.11</destination-address>
                        <destination-port>1135</destination-port>
                        <protocol>icmp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name></interface-name>
                        <session-token>0x0</session-token>
                        <flag>0x0</flag>
                        <route>0x0</route>
                        <gateway>0.0.0.0</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["HA_HE_FLOW_CP_SESSION_SUMMARY"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-valid>10</displayed-session-valid>
                <displayed-session-pending>20</displayed-session-pending>
                <displayed-session-invalidated>30</displayed-session-invalidated>
                <displayed-session-other>40</displayed-session-other>
                <displayed-session-count>50</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC1:</dcp-flow-fpc-pic-id>
                <displayed-session-valid>10</displayed-session-valid>
                <displayed-session-pending>20</displayed-session-pending>
                <displayed-session-invalidated>30</displayed-session-invalidated>
                <displayed-session-other>40</displayed-session-other>
                <displayed-session-count>50</displayed-session-count>
                <max-session-count>7549747</max-session-count>
                <max-inet6-session-count>7549747</max-inet6-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC2:</dcp-flow-fpc-pic-id>
                <displayed-session-valid>10</displayed-session-valid>
                <displayed-session-pending>20</displayed-session-pending>
                <displayed-session-invalidated>30</displayed-session-invalidated>
                <displayed-session-other>40</displayed-session-other>
                <displayed-session-count>50</displayed-session-count>
                <max-session-count>7549747</max-session-count>
                <max-inet6-session-count>7549747</max-inet6-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC3:</dcp-flow-fpc-pic-id>
                <displayed-session-valid>10</displayed-session-valid>
                <displayed-session-pending>20</displayed-session-pending>
                <displayed-session-invalidated>30</displayed-session-invalidated>
                <displayed-session-other>40</displayed-session-other>
                <displayed-session-count>50</displayed-session-count>
                <max-session-count>7549747</max-session-count>
                <max-inet6-session-count>7549747</max-inet6-session-count>
            </flow-session-information>
        </multi-routing-engine-item>
        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
                <displayed-session-valid>20</displayed-session-valid>
                <displayed-session-pending>30</displayed-session-pending>
                <displayed-session-invalidated>40</displayed-session-invalidated>
                <displayed-session-other>50</displayed-session-other>
                <displayed-session-count>60</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC1:</dcp-flow-fpc-pic-id>
                <displayed-session-valid>20</displayed-session-valid>
                <displayed-session-pending>30</displayed-session-pending>
                <displayed-session-invalidated>40</displayed-session-invalidated>
                <displayed-session-other>50</displayed-session-other>
                <displayed-session-count>60</displayed-session-count>
                <max-session-count>7549747</max-session-count>
                <max-inet6-session-count>7549747</max-inet6-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC2:</dcp-flow-fpc-pic-id>
                <displayed-session-valid>20</displayed-session-valid>
                <displayed-session-pending>30</displayed-session-pending>
                <displayed-session-invalidated>40</displayed-session-invalidated>
                <displayed-session-other>50</displayed-session-other>
                <displayed-session-count>60</displayed-session-count>
                <max-session-count>7549747</max-session-count>
                <max-inet6-session-count>7549747</max-inet6-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
                <dcp-flow-fpc-pic-id> on FPC0 PIC3:</dcp-flow-fpc-pic-id>
                <displayed-session-valid>20</displayed-session-valid>
                <displayed-session-pending>30</displayed-session-pending>
                <displayed-session-invalidated>40</displayed-session-invalidated>
                <displayed-session-other>50</displayed-session-other>
                <displayed-session-count>60</displayed-session-count>
                <max-session-count>7549747</max-session-count>
                <max-inet6-session-count>7549747</max-inet6-session-count>
            </flow-session-information>
        </multi-routing-engine-item>
    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["HE_SA_FLOW_CP_SESSION_SUMMARY"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-flow">
        <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-flow">
        <dcp-flow-fpc-pic-id> on FPC0 PIC1:</dcp-flow-fpc-pic-id>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
        <max-session-count>7549747</max-session-count>
        <max-inet6-session-count>7549747</max-inet6-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-flow">
        <dcp-flow-fpc-pic-id> on FPC0 PIC2:</dcp-flow-fpc-pic-id>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
        <max-session-count>7549747</max-session-count>
        <max-inet6-session-count>7549747</max-inet6-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-flow">
        <dcp-flow-fpc-pic-id> on FPC0 PIC3:</dcp-flow-fpc-pic-id>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
        <max-session-count>7549747</max-session-count>
        <max-inet6-session-count>7549747</max-inet6-session-count>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["HE_SA_FLOW_CP_SESSION_SUMMARY_ONE_SPU"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-flow">
        <dcp-flow-fpc-pic-id> on FPC0 PIC0:</dcp-flow-fpc-pic-id>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["HE_SA_FLOW_CP_SESSION_SUMMARY_WITH_ROOT_TAG"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.3I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <dcp-flow-fpc-id>9</dcp-flow-fpc-id>
            <dcp-flow-pic-id>0</dcp-flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>10</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>20</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>30</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>40</dcp-displayed-session-other>
                <dcp-displayed-session-count>50</dcp-displayed-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <dcp-flow-fpc-id>9</dcp-flow-fpc-id>
            <dcp-flow-pic-id>1</dcp-flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>10</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>20</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>30</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>40</dcp-displayed-session-other>
                <dcp-displayed-session-count>50</dcp-displayed-session-count>
                <max-session-count>7549747</max-session-count>
                <max-inet6-session-count>7549747</max-inet6-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <dcp-flow-fpc-id>9</dcp-flow-fpc-id>
            <dcp-flow-pic-id>2</dcp-flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>0</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>0</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>2</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>0</dcp-displayed-session-other>
                <dcp-displayed-session-count>2</dcp-displayed-session-count>
                <max-session-count>7549747</max-session-count>
                <max-inet6-session-count>7549747</max-inet6-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
        <flow-session-per-pic xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
            <dcp-flow-fpc-id>9</dcp-flow-fpc-id>
            <dcp-flow-pic-id>3</dcp-flow-pic-id>
            <dcp-flow-session-summary-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
                <dcp-displayed-session-valid>0</dcp-displayed-session-valid>
                <dcp-displayed-session-pending>0</dcp-displayed-session-pending>
                <dcp-displayed-session-invalidated>1</dcp-displayed-session-invalidated>
                <dcp-displayed-session-other>0</dcp-displayed-session-other>
                <dcp-displayed-session-count>1</dcp-displayed-session-count>
                <max-session-count>7549747</max-session-count>
                <max-inet6-session-count>7549747</max-inet6-session-count>
            </dcp-flow-session-summary-information>
        </flow-session-per-pic>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["verify_flow_session_USER_CASE_1"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-flow">
        <flow-session junos:style="brief">
            <session-identifier>140</session-identifier>
            <status>Normal</status>
            <session-flag>0x40/0x0/0x23</session-flag>
            <policy>self-traffic-policy/1</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <application-name>junos-ike</application-name>
            <application-value>54</application-value>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>60</configured-timeout>
            <timeout>44</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>4133</start-time>
            <duration>15</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>2.1.1.1</source-address>
                <source-port>500</source-port>
                <destination-address>1.1.1.1</destination-address>
                <destination-port>500</destination-port>
                <protocol>udp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x21</flag>
                <route>0xb0010</route>
                <gateway>1.1.1.2</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>4</pkt-cnt>
                <byte-cnt>915</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>1.1.1.1</source-address>
                <source-port>500</source-port>
                <destination-address>2.1.1.1</destination-address>
                <destination-port>500</destination-port>
                <protocol>udp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>.local..0</interface-name>
                <session-token>0x2</session-token>
                <flag>0x30</flag>
                <route>0xfffb0006</route>
                <gateway>1.1.1.1</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>2</pkt-cnt>
                <byte-cnt>640</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>141</session-identifier>
            <status>Normal</status>
            <session-flag>0x10000/0x0/0x1</session-flag>
            <policy>N/A</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>N/A</configured-timeout>
            <timeout>N/A</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>4133</start-time>
            <duration>15</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>2.1.1.1</source-address>
                <source-port>2621</source-port>
                <destination-address>1.1.1.1</destination-address>
                <destination-port>35742</destination-port>
                <protocol>esp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x100621</flag>
                <route>0xb0010</route>
                <gateway>1.1.1.2</gateway>
                <tunnel-information>0</tunnel-information>
                <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>142</session-identifier>
            <status>Normal</status>
            <session-flag>0x10000/0x0/0x1</session-flag>
            <policy>N/A</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>N/A</configured-timeout>
            <timeout>N/A</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>4133</start-time>
            <duration>15</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>2.1.1.1</source-address>
                <source-port>0</source-port>
                <destination-address>1.1.1.1</destination-address>
                <destination-port>0</destination-port>
                <protocol>esp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x621</flag>
                <route>0xb0010</route>
                <gateway>1.1.1.2</gateway>
                <tunnel-information>0</tunnel-information>
                <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>144</session-identifier>
            <status>Normal</status>
            <session-flag>0x40/0x0/0x23</session-flag>
            <policy>self-traffic-policy/1</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <application-name>junos-ike</application-name>
            <application-value>54</application-value>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>60</configured-timeout>
            <timeout>46</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>4134</start-time>
            <duration>14</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>3.1.1.1</source-address>
                <source-port>500</source-port>
                <destination-address>1.1.1.1</destination-address>
                <destination-port>500</destination-port>
                <protocol>udp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x21</flag>
                <route>0xb0010</route>
                <gateway>1.1.1.2</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>4</pkt-cnt>
                <byte-cnt>915</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>1.1.1.1</source-address>
                <source-port>500</source-port>
                <destination-address>3.1.1.1</destination-address>
                <destination-port>500</destination-port>
                <protocol>udp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>.local..0</interface-name>
                <session-token>0x2</session-token>
                <flag>0x30</flag>
                <route>0xfffb0006</route>
                <gateway>1.1.1.1</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>2</pkt-cnt>
                <byte-cnt>640</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>145</session-identifier>
            <status>Normal</status>
            <session-flag>0x10000/0x0/0x1</session-flag>
            <policy>N/A</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>N/A</configured-timeout>
            <timeout>N/A</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>4134</start-time>
            <duration>14</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>3.1.1.1</source-address>
                <source-port>34060</source-port>
                <destination-address>1.1.1.1</destination-address>
                <destination-port>44617</destination-port>
                <protocol>esp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x100621</flag>
                <route>0xb0010</route>
                <gateway>1.1.1.2</gateway>
                <tunnel-information>0</tunnel-information>
                <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>146</session-identifier>
            <status>Normal</status>
            <session-flag>0x10000/0x0/0x1</session-flag>
            <policy>N/A</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>N/A</configured-timeout>
            <timeout>N/A</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>4134</start-time>
            <duration>14</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>3.1.1.1</source-address>
                <source-port>0</source-port>
                <destination-address>1.1.1.1</destination-address>
                <destination-port>0</destination-port>
                <protocol>esp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x621</flag>
                <route>0xb0010</route>
                <gateway>1.1.1.2</gateway>
                <tunnel-information>0</tunnel-information>
                <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>150</session-identifier>
            <status>Normal</status>
            <session-flag>0x40/0x0/0x8003</session-flag>
            <policy>GROUP_IKE_ID_VPN_POL/4</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <application-name>junos-telnet</application-name>
            <application-value>10</application-value>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>1800</configured-timeout>
            <timeout>1794</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>4137</start-time>
            <duration>11</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>15.15.15.1</source-address>
                <source-port>60119</source-port>
                <destination-address>14.14.14.1</destination-address>
                <destination-port>23</destination-port>
                <protocol>tcp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x401021</flag>
                <route>0x0</route>
                <gateway>15.15.15.1</gateway>
                <tunnel-information>67108900</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>21</pkt-cnt>
                <byte-cnt>1201</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>14.14.14.1</source-address>
                <source-port>23</source-port>
                <destination-address>15.15.15.1</destination-address>
                <destination-port>60119</destination-port>
                <protocol>tcp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/0.0</interface-name>
                <session-token>0x7</session-token>
                <flag>0x1020</flag>
                <route>0xa0010</route>
                <gateway>14.14.14.1</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>17</pkt-cnt>
                <byte-cnt>1148</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>159</session-identifier>
            <status>Normal</status>
            <session-flag>0x80000040/0x0/0x800003</session-flag>
            <policy>GROUP_IKE_ID_VPN_POL/4</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>4</configured-timeout>
            <timeout>2</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>4146</start-time>
            <duration>2</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>13.13.13.1</source-address>
                <source-port>14</source-port>
                <destination-address>14.14.14.1</destination-address>
                <destination-port>29963</destination-port>
                <protocol>icmp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x400021</flag>
                <route>0x0</route>
                <gateway>13.13.13.1</gateway>
                <tunnel-information>50331684</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>1</pkt-cnt>
                <byte-cnt>84</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>14.14.14.1</source-address>
                <source-port>29963</source-port>
                <destination-address>13.13.13.1</destination-address>
                <destination-port>14</destination-port>
                <protocol>icmp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/0.0</interface-name>
                <session-token>0x7</session-token>
                <flag>0x20</flag>
                <route>0xa0010</route>
                <gateway>14.14.14.1</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>1</pkt-cnt>
                <byte-cnt>84</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>160</session-identifier>
            <status>Normal</status>
            <session-flag>0x80000040/0x0/0x800003</session-flag>
            <policy>GROUP_IKE_ID_VPN_POL/4</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>4</configured-timeout>
            <timeout>2</timeout>
            <sess-state>Valid</sess-state>
            <logical-system></logical-system>
            <wan-acceleration></wan-acceleration>
            <start-time>4147</start-time>
            <duration>1</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>13.13.13.1</source-address>
                <source-port>15</source-port>
                <destination-address>14.14.14.1</destination-address>
                <destination-port>29963</destination-port>
                <protocol>icmp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x400021</flag>
                <route>0x0</route>
                <gateway>13.13.13.1</gateway>
                <tunnel-information>50331684</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>1</pkt-cnt>
                <byte-cnt>84</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>14.14.14.1</source-address>
                <source-port>29963</source-port>
                <destination-address>13.13.13.1</destination-address>
                <destination-port>15</destination-port>
                <protocol>icmp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/0.0</interface-name>
                <session-token>0x7</session-token>
                <flag>0x20</flag>
                <route>0xa0010</route>
                <gateway>14.14.14.1</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>1</pkt-cnt>
                <byte-cnt>84</byte-cnt>
            </flow-information>
        </flow-session>
        <displayed-session-count>9</displayed-session-count>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["FLOW_SESSION_FOR_ADDRESS_IN_BEHAVIOR"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.1I0/junos"> <flow-session-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-flow"> <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id> <displayed-session-count>0</displayed-session-count> </flow-session-information> <flow-session-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-flow"> <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id> <flow-session junos:style="brief"> <session-identifier>20001048</session-identifier> <status>Normal</status> <session-flag>0x0/0x0/0x2008003</session-flag> <policy>t_un/5</policy> <nat-source-pool-name>root_src_v4_pat</nat-source-pool-name> <application-name>junos-telnet</application-name> <application-value>10</application-value> <dynamic-application-name>junos:UNKNOWN</dynamic-application-name> <encryption-traffic-name> Unknown</encryption-traffic-name> <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name> <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name> <configured-timeout>1800</configured-timeout> <timeout>1798</timeout> <sess-state>Valid</sess-state> <logical-system></logical-system> <wan-acceleration></wan-acceleration> <start-time>147472</start-time> <duration>35</duration> <session-mask>0</session-mask> <flow-information junos:style="brief"> <direction>In</direction> <source-address>100.0.0.2</source-address> <source-port>60437</source-port> <destination-address>100.0.1.2</destination-address> <destination-port>23</destination-port> <protocol>tcp</protocol> <conn-tag>0x0</conn-tag> <interface-name>xe-2/0/2.0</interface-name> <session-token>0x600b</session-token> <flag>0x40001021</flag> <route>0xb0010</route> <gateway>100.0.0.2</gateway> <tunnel-information>0</tunnel-information> <port-sequence>0</port-sequence> <fin-sequence>0</fin-sequence> <fin-state>0</fin-state> <seq-ack-diff>0</seq-ack-diff> <pkt-cnt>22</pkt-cnt> <byte-cnt>1253</byte-cnt> <dcp-session-id>20001469</dcp-session-id> </flow-information> <flow-information junos:style="brief"> <direction>Out</direction> <source-address>100.0.1.2</source-address> <source-port>23</source-port> <destination-address>30.0.1.1</destination-address> <destination-port>11181</destination-port> <protocol>tcp</protocol> <conn-tag>0x0</conn-tag> <interface-name>xe-2/0/3.0</interface-name> <session-token>0x800c</session-token> <flag>0x60001020</flag> <route>0x80010</route> <gateway>100.0.1.2</gateway> <tunnel-information>0</tunnel-information> <port-sequence>0</port-sequence> <fin-sequence>0</fin-sequence> <fin-state>0</fin-state> <seq-ack-diff>0</seq-ack-diff> <pkt-cnt>18</pkt-cnt> <byte-cnt>1202</byte-cnt> <dcp-session-id>30001103</dcp-session-id> </flow-information> </flow-session> <displayed-session-count>1</displayed-session-count> </flow-session-information> <flow-session-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-flow"> <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id> <displayed-session-count>0</displayed-session-count> </flow-session-information> <cli> <banner></banner> </cli> </rpc-reply>
        """

        self.response["HA_LE_FLOW_VTY_ALL_SESSION"] = """
================ tnp_0x1001081 ================


 Session Id: 401187, Logical system: root-logical-system, Policy: 2, Timeout: 6s 6s , state: 3, flags: 80800040/8002000/3
 Forward, failover cnt 37, sync id 0x10186d7e, retry cnt 0,0
   (in)*  : 121.11.10.2/34998 -> 121.11.30.2/23;6, Conn Tag: 0x0, If: reth1.0 (7), CP session Id: 0, CP sess SPU Id: 0, flag: 0021, wsf: 0, diff: 0, spd info: 0000
            thread id:1, classifier cos: 0, dp: 0, cosflag 0x0, nh: 0x0, tunnel_info: 0x0, pkts: 1, bytes: 60
            pmtu : 1500,  tunnel pmtu: 0
   (out)  : 121.11.10.2/34998 <- 121.11.30.2/23;6, Conn Tag: 0x0, If: reth3.0 (8), CP session Id: 0, CP sess SPU Id: 0, flag: 0020, wsf: 0, diff: 0, spd info: 0000
            thread id:255, classifier cos: 0, dp: 0, cosflag 0x0, nh: 0x572f28, tunnel_info: 0x0, pkts: 0, bytes: 0
            pmtu : 1500,  tunnel pmtu: 0

 Session Id: 401188, Logical system: root-logical-system, Policy: 2, Timeout: 14414s 14414s , state: 3, flags: 10000040/8000000/8003
 Backup, failover cnt 37, sync id 0x200001c6, retry cnt 0,0
   (in)*  : 121.11.10.2/34998 -> 121.11.30.2/23;6, Conn Tag: 0x0, If: reth1.0 (7), CP session Id: 0, CP sess SPU Id: 0, flag: 0021, wsf: 0, diff: 0, spd info: 0000
            thread id:1, classifier cos: 0, dp: 0, cosflag 0x0, nh: 0x5393c2, tunnel_info: 0x0, pkts: 2, bytes: 120
            pmtu : 1500,  tunnel pmtu: 0
   (out)  : 121.11.10.2/34998 <- 121.11.30.2/23;6, Conn Tag: 0x0, If: reth3.0 (8), CP session Id: 0, CP sess SPU Id: 0, flag: 0020, wsf: 0, diff: 0, spd info: 0000
            thread id:255, classifier cos: 0, dp: 0, cosflag 0x0, nh: 0x572f28, tunnel_info: 0x0, pkts: 0, bytes: 0
            pmtu : 1500,  tunnel pmtu: 0
        """

        self.response["SA_LE_FLOW_VTY_ALL_SESSION"] = """
================ tnp_0x10000080 ================


 Session Id: 1, Logical system: root-logical-system, Policy: 0, Timeout: -1s -1s , state: 3, flags: 10000/0/1
   (in)*  : 2030:0:0:0:0:0:0:2/21825 -> 2030:0:0:0:0:0:0:1/12609;50, Conn Tag: 0x0, VRF GRP ID: 0(0), If: ge-0/0/1.0 (9), CP session Id: 0, CP sess SPU Id: 0, flag: 0623, wsf: 0, diff: 0
            thread id:1, classifier cos: 0, dp: 0, is tunnel cos ready: Nonh: 0x1b0010, tunnel_info: 0x0, pkts: 0, bytes: 0
            pmtu : 0,  tunnel pmtu: 0
 Anchor tunnel session with nsp_tunnel - 0x2abf2300, tunnel info - 0x20020002
 iked_dist_id 1024, anchor spu id 256
 tunnel id: 131074, PMTU tunnel overhead: 96, flag 0x42/0x30, tun_flag 0x60
 Bind if - st0.1, If - ge-0/0/1.0, HA if - ge-0/0/1.0
 tunnel session token 7 nt_next 0x0 nt_prev 0x0
 tunnel session nexthop 0x0  final nh 0x587f6c00

 Session Id: 2, Logical system: root-logical-system, Policy: 0, Timeout: -1s -1s , state: 3, flags: 10000/0/1
   (in)*  : 2030:0:0:0:0:0:0:2/0 -> 2030:0:0:0:0:0:0:1/0;50, Conn Tag: 0x0, VRF GRP ID: 0(0), If: ge-0/0/1.0 (9), CP session Id: 0, CP sess SPU Id: 0, flag: 0623, wsf: 0, diff: 0
            thread id:1, classifier cos: 0, dp: 0, is tunnel cos ready: Nonh: 0x1b0010, tunnel_info: 0x0, pkts: 0, bytes: 0
            pmtu : 0,  tunnel pmtu: 0
 Anchor tunnel session with nsp_tunnel - 0x2abf2600, tunnel info - 0x20020002
 iked_dist_id 1024, anchor spu id 256
 tunnel id: 131074, PMTU tunnel overhead: 96, flag 0x44/0x30, tun_flag 0x40
 Bind if - st0.1, If - ge-0/0/1.0, HA if - N/A
 tunnel session token 7 nt_next 0x0 nt_prev 0x0
 tunnel session nexthop 0x0  final nh 0x587f6c00
 CP session not installed

 Session Id: 3, Logical system: root-logical-system, Policy: 0, Timeout: -1s -1s , state: 3, flags: 10000/0/1
   (in)*  : 30.30.30.254/13759 -> 30.30.30.1/13751;50, Conn Tag: 0x0, VRF GRP ID: 0(0), If: ge-0/0/1.0 (9), CP session Id: 0, CP sess SPU Id: 0, flag: 0621, wsf: 0, diff: 0, spd info: 0000
            thread id:1, classifier cos: 0, dp: 0, is tunnel cos ready: Nonh: 0x190010, tunnel_info: 0x0, pkts: 0, bytes: 0
            pmtu : 0,  tunnel pmtu: 0
 Anchor tunnel session with nsp_tunnel - 0x2abf2900, tunnel info - 0x20020001
 iked_dist_id 1024, anchor spu id 256
 tunnel id: 131073, PMTU tunnel overhead: 64, flag 0x2/0x30, tun_flag 0x60
 Bind if - st0.0, If - ge-0/0/1.0, HA if - ge-0/0/1.0
 tunnel session token 7 nt_next 0x0 nt_prev 0x0
 tunnel session nexthop 0x0  final nh 0x587f5440

 Session Id: 4, Logical system: root-logical-system, Policy: 0, Timeout: -1s -1s , state: 3, flags: 10000/0/1
   (in)*  : 30.30.30.254/0 -> 30.30.30.1/0;50, Conn Tag: 0x0, VRF GRP ID: 0(0), If: ge-0/0/1.0 (9), CP session Id: 0, CP sess SPU Id: 0, flag: 0621, wsf: 0, diff: 0, spd info: 0000
            thread id:1, classifier cos: 0, dp: 0, is tunnel cos ready: Nonh: 0x190010, tunnel_info: 0x0, pkts: 0, bytes: 0
            pmtu : 0,  tunnel pmtu: 0
 Anchor tunnel session with nsp_tunnel - 0x2abf2c00, tunnel info - 0x20020001
 iked_dist_id 1024, anchor spu id 256
 tunnel id: 131073, PMTU tunnel overhead: 64, flag 0x4/0x30, tun_flag 0x40
 Bind if - st0.0, If - ge-0/0/1.0, HA if - N/A
 tunnel session token 7 nt_next 0x0 nt_prev 0x0
 tunnel session nexthop 0x0  final nh 0x587f5440
 CP session not installed
        """

        self.response["EXPECT_HA_LE_FLOW_VTY_ALL_SESSION"] = [
            {
                "backup_session": False,
                "failover_cnt": "37",
                "flags": "80800040/8002000/3",
                "forward_session": True,
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
                "in_protocol": "6",
                "in_flag": "0021",
                "in_if": "reth1.0 (7)",
                "in_nh": "0x0",
                "in_pkts": "1",
                "in_pmtu": "1500",
                "in_spd_info": "0000",
                "in_src_addr": "121.11.10.2",
                "in_src_port": "34998",
                "in_protocol": "6",
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
                "out_protocol": "6",
                "out_flag": "0020",
                "out_if": "reth3.0 (8)",
                "out_nh": "0x572f28",
                "out_pkts": "0",
                "out_pmtu": "1500",
                "out_spd_info": "0000",
                "out_src_addr": "121.11.10.2",
                "out_src_port": "34998",
                "out_protocol": "6",
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
            {
                "backup_session": True,
                "failover_cnt": "37",
                "flags": "10000040/8000000/8003",
                "forward_session": False,
                "in_bytes": "120",
                "in_classifier_cos": "0",
                "in_conn_tag": "0x0",
                "in_cosflag": "0x0",
                "in_cp_sess_spu_id": "0",
                "in_cp_session_id": "0",
                "in_diff": "0",
                "in_dp": "0",
                "in_dst_addr": "121.11.30.2",
                "in_dst_port": "23",
                "in_protocol": "6",
                "in_flag": "0021",
                "in_if": "reth1.0 (7)",
                "in_nh": "0x5393c2",
                "in_pkts": "2",
                "in_pmtu": "1500",
                "in_spd_info": "0000",
                "in_src_addr": "121.11.10.2",
                "in_src_port": "34998",
                "in_protocol": "6",
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
                "out_protocol": "6",
                "out_flag": "0020",
                "out_if": "reth3.0 (8)",
                "out_nh": "0x572f28",
                "out_pkts": "0",
                "out_pmtu": "1500",
                "out_spd_info": "0000",
                "out_src_addr": "121.11.10.2",
                "out_src_port": "34998",
                "out_protocol": "6",
                "out_thread_id": "255",
                "out_tunnel_info": "0x0",
                "out_tunnel_pmtu": "0",
                "out_wsf": "0",
                "policy": "2",
                "retry_cnt": "0",
                "session_id": "401188",
                "state": "3",
                "sync_id": "0x200001c6",
                "timeout": "14414s 14414s"
            }
        ]

        self.response["EXPECT_SA_LE_FLOW_VTY_ALL_SESSION"] = [
            {
                "anchor_spu_id": "256",
                "anchor_tunnel_session_with_nsp_tunnel": "0x2abf2300",
                "backup_session": False,
                "bind_if": "st0.1",
                "final_nh": "0x587f6c00",
                "flag": "0x42/0x30",
                "flags": "10000/0/1",
                "forward_session": False,
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
                "in_protocol": "50",
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
            {
                "anchor_spu_id": "256",
                "anchor_tunnel_session_with_nsp_tunnel": "0x2abf2600",
                "backup_session": False,
                "bind_if": "st0.1",
                "final_nh": "0x587f6c00",
                "flag": "0x44/0x30",
                "flags": "10000/0/1",
                "forward_session": False,
                "ha_if": "N/A",
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
                "in_dst_port": "0",
                "in_protocol": "50",
                "in_flag": "0623",
                "in_if": "ge-0/0/1.0 (9)",
                "in_is_tunnel_cos_ready": "Nonh: 0x1b0010",
                "in_pkts": "0",
                "in_pmtu": "0",
                "in_src_addr": "2030:0:0:0:0:0:0:2",
                "in_src_port": "0",
                "in_protocol": "50",
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
                "session_id": "2",
                "state": "3",
                "timeout": "-1s -1s",
                "tun_flag": "0x40",
                "tunnel_id": "131074",
                "tunnel_info": "0x20020002",
                "tunnel_session_nexthop": "0x0",
                "tunnel_session_token": "7"
            },
            {
                "anchor_spu_id": "256",
                "anchor_tunnel_session_with_nsp_tunnel": "0x2abf2900",
                "backup_session": False,
                "bind_if": "st0.0",
                "final_nh": "0x587f5440",
                "flag": "0x2/0x30",
                "flags": "10000/0/1",
                "forward_session": False,
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
                "in_dst_addr": "30.30.30.1",
                "in_dst_port": "13751",
                "in_protocol": "50",
                "in_flag": "0621",
                "in_if": "ge-0/0/1.0 (9)",
                "in_is_tunnel_cos_ready": "Nonh: 0x190010",
                "in_pkts": "0",
                "in_pmtu": "0",
                "in_spd_info": "0000",
                "in_src_addr": "30.30.30.254",
                "in_src_port": "13759",
                "in_protocol": "50",
                "in_thread_id": "1",
                "in_tunnel_info": "0x0",
                "in_tunnel_pmtu": "0",
                "in_vrf_grp_id": "0(0)",
                "in_wsf": "0",
                "logical_system": "root-logical-system",
                "nt_next": "0x0",
                "nt_prev": "0x0",
                "pmtu_tunnel_overhead": "64",
                "policy": "0",
                "session_id": "3",
                "state": "3",
                "timeout": "-1s -1s",
                "tun_flag": "0x60",
                "tunnel_id": "131073",
                "tunnel_info": "0x20020001",
                "tunnel_session_nexthop": "0x0",
                "tunnel_session_token": "7"
            },
            {
                "anchor_spu_id": "256",
                "anchor_tunnel_session_with_nsp_tunnel": "0x2abf2c00",
                "backup_session": False,
                "bind_if": "st0.0",
                "final_nh": "0x587f5440",
                "flag": "0x4/0x30",
                "flags": "10000/0/1",
                "forward_session": False,
                "ha_if": "N/A",
                "if": "ge-0/0/1.0",
                "iked_dist_id": "1024",
                "in_bytes": "0",
                "in_classifier_cos": "0",
                "in_conn_tag": "0x0",
                "in_cp_sess_spu_id": "0",
                "in_cp_session_id": "0",
                "in_diff": "0",
                "in_dp": "0",
                "in_dst_addr": "30.30.30.1",
                "in_dst_port": "0",
                "in_protocol": "50",
                "in_flag": "0621",
                "in_if": "ge-0/0/1.0 (9)",
                "in_is_tunnel_cos_ready": "Nonh: 0x190010",
                "in_pkts": "0",
                "in_pmtu": "0",
                "in_spd_info": "0000",
                "in_src_addr": "30.30.30.254",
                "in_src_port": "0",
                "in_protocol": "50",
                "in_thread_id": "1",
                "in_tunnel_info": "0x0",
                "in_tunnel_pmtu": "0",
                "in_vrf_grp_id": "0(0)",
                "in_wsf": "0",
                "logical_system": "root-logical-system",
                "nt_next": "0x0",
                "nt_prev": "0x0",
                "pmtu_tunnel_overhead": "64",
                "policy": "0",
                "session_id": "4",
                "state": "3",
                "timeout": "-1s -1s",
                "tun_flag": "0x40",
                "tunnel_id": "131073",
                "tunnel_info": "0x20020001",
                "tunnel_session_nexthop": "0x0",
                "tunnel_session_token": "7"
            }
        ]


        self.response["TICKET_5532_XML"] = """
    <rpc-reply xmlns:junos="http://xml.juniper.net/junos/19.2R0/junos">
        <flow-session-information xmlns="http://xml.juniper.net/junos/19.2R0/junos-flow">
            <flow-session junos:style="brief">
                <session-identifier>1</session-identifier>
                <status>Normal</status>
                <session-flag>0x10000/0x0/0x0/0x1</session-flag>
                <policy>N/A</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>N/A</configured-timeout>
                <timeout>N/A</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>241</start-time>
                <duration>600</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>22.22.22.22</source-address>
                    <source-port>16634</source-port>
                    <destination-address>21.21.21.21</destination-address>
                    <destination-port>33428</destination-port>
                    <protocol>esp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/2.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x100621</flag>
                    <route>0x1c0010</route>
                    <gateway>21.21.21.22</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                    <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                    <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                    <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                    <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                    <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                    <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                    <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>91</pkt-cnt>
                    <byte-cnt>16520</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>2</session-identifier>
                <status>Normal</status>
                <session-flag>0x10000/0x0/0x0/0x1</session-flag>
                <policy>N/A</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>N/A</configured-timeout>
                <timeout>N/A</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>241</start-time>
                <duration>600</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>22.22.22.22</source-address>
                    <source-port>0</source-port>
                    <destination-address>21.21.21.21</destination-address>
                    <destination-port>0</destination-port>
                    <protocol>esp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/2.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x621</flag>
                    <route>0x1c0010</route>
                    <gateway>21.21.21.22</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                    <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                    <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                    <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                    <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                    <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                    <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                    <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>0</pkt-cnt>
                    <byte-cnt>0</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>3</session-identifier>
                <status>Normal</status>
                <session-flag>0x10000/0x0/0x0/0x1</session-flag>
                <policy>N/A</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>N/A</configured-timeout>
                <timeout>N/A</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>241</start-time>
                <duration>600</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>24.24.24.24</source-address>
                    <source-port>15627</source-port>
                    <destination-address>23.23.23.23</destination-address>
                    <destination-port>41782</destination-port>
                    <protocol>esp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/3.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x100621</flag>
                    <route>0x1e0010</route>
                    <gateway>23.23.23.24</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                    <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                    <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                    <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                    <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                    <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                    <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                    <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>91</pkt-cnt>
                    <byte-cnt>16520</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>4</session-identifier>
                <status>Normal</status>
                <session-flag>0x10000/0x0/0x0/0x1</session-flag>
                <policy>N/A</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>N/A</configured-timeout>
                <timeout>N/A</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>241</start-time>
                <duration>600</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>24.24.24.24</source-address>
                    <source-port>0</source-port>
                    <destination-address>23.23.23.23</destination-address>
                    <destination-port>0</destination-port>
                    <protocol>esp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/3.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x621</flag>
                    <route>0x1e0010</route>
                    <gateway>23.23.23.24</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                    <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                    <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                    <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                    <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                    <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                    <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                    <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>0</pkt-cnt>
                    <byte-cnt>0</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>5</session-identifier>
                <status>Normal</status>
                <session-flag>0x10000/0x0/0x0/0x1</session-flag>
                <policy>N/A</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>N/A</configured-timeout>
                <timeout>N/A</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>241</start-time>
                <duration>600</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>26.26.26.26</source-address>
                    <source-port>58933</source-port>
                    <destination-address>25.25.25.25</destination-address>
                    <destination-port>10853</destination-port>
                    <protocol>esp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/4.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x100621</flag>
                    <route>0x1d0010</route>
                    <gateway>25.25.25.26</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                    <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                    <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                    <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                    <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                    <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                    <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                    <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>99</pkt-cnt>
                    <byte-cnt>17984</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>6</session-identifier>
                <status>Normal</status>
                <session-flag>0x10000/0x0/0x0/0x1</session-flag>
                <policy>N/A</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>N/A</configured-timeout>
                <timeout>N/A</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>241</start-time>
                <duration>600</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>26.26.26.26</source-address>
                    <source-port>0</source-port>
                    <destination-address>25.25.25.25</destination-address>
                    <destination-port>0</destination-port>
                    <protocol>esp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/4.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x621</flag>
                    <route>0x1d0010</route>
                    <gateway>25.25.25.26</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                    <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                    <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                    <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                    <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                    <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                    <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                    <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>0</pkt-cnt>
                    <byte-cnt>0</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>8</session-identifier>
                <status>Normal</status>
                <session-flag>0x10000/0x0/0x0/0x1</session-flag>
                <policy>N/A</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>N/A</configured-timeout>
                <timeout>N/A</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>274</start-time>
                <duration>567</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>9.9.9.2</source-address>
                    <source-port>1</source-port>
                    <destination-address>9.9.9.1</destination-address>
                    <destination-port>1</destination-port>
                    <protocol>gre</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>st0.0</interface-name>
                    <session-token>0xc00b</session-token>
                    <flag>0x100621</flag>
                    <route>0x170010</route>
                    <gateway>9.9.9.0</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                    <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                    <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                    <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                    <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                    <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                    <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                    <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>0</pkt-cnt>
                    <byte-cnt>0</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>12</session-identifier>
                <status>Normal</status>
                <session-flag>0x10000/0x0/0x0/0x1</session-flag>
                <policy>N/A</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>N/A</configured-timeout>
                <timeout>N/A</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>292</start-time>
                <duration>549</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>10.10.10.2</source-address>
                    <source-port>1</source-port>
                    <destination-address>10.10.10.1</destination-address>
                    <destination-port>1</destination-port>
                    <protocol>gre</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>st0.1</interface-name>
                    <session-token>0xc00b</session-token>
                    <flag>0x100621</flag>
                    <route>0x190010</route>
                    <gateway>10.10.10.0</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                    <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                    <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                    <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                    <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                    <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                    <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                    <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>0</pkt-cnt>
                    <byte-cnt>0</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>13</session-identifier>
                <status>Normal</status>
                <session-flag>0x10000/0x0/0x0/0x1</session-flag>
                <policy>N/A</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>N/A</configured-timeout>
                <timeout>N/A</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>332</start-time>
                <duration>509</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>11.11.11.2</source-address>
                    <source-port>1</source-port>
                    <destination-address>11.11.11.1</destination-address>
                    <destination-port>1</destination-port>
                    <protocol>gre</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>st0.2</interface-name>
                    <session-token>0xc00b</session-token>
                    <flag>0x100621</flag>
                    <route>0x1b0010</route>
                    <gateway>11.11.11.0</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                    <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                    <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                    <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                    <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                    <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                    <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                    <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>0</pkt-cnt>
                    <byte-cnt>0</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>43</session-identifier>
                <status>Normal</status>
                <session-flag>0x40/0x0/0x2/0x23</session-flag>
                <policy>self-traffic-policy/1</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <application-name>junos-ike</application-name>
                <application-value>54</application-value>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>60</configured-timeout>
                <timeout>58</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>739</start-time>
                <duration>102</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>24.24.24.24</source-address>
                    <source-port>500</source-port>
                    <destination-address>23.23.23.23</destination-address>
                    <destination-port>500</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/3.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x21</flag>
                    <route>0x1e0010</route>
                    <gateway>23.23.23.24</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>11</pkt-cnt>
                    <byte-cnt>1232</byte-cnt>
                </flow-information>
                <flow-information junos:style="brief">
                    <direction>Out</direction>
                    <source-address>23.23.23.23</source-address>
                    <source-port>500</source-port>
                    <destination-address>24.24.24.24</destination-address>
                    <destination-port>500</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>.local..0</interface-name>
                    <session-token>0x2</session-token>
                    <flag>0x30</flag>
                    <route>0xfffb0006</route>
                    <gateway>23.23.23.23</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>11</pkt-cnt>
                    <byte-cnt>1232</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>44</session-identifier>
                <status>Normal</status>
                <session-flag>0x40/0x0/0x2/0x23</session-flag>
                <policy>self-traffic-policy/1</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <application-name>junos-ike</application-name>
                <application-value>54</application-value>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>60</configured-timeout>
                <timeout>50</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>741</start-time>
                <duration>100</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>22.22.22.22</source-address>
                    <source-port>500</source-port>
                    <destination-address>21.21.21.21</destination-address>
                    <destination-port>500</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/2.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x21</flag>
                    <route>0x1c0010</route>
                    <gateway>21.21.21.22</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>10</pkt-cnt>
                    <byte-cnt>1120</byte-cnt>
                </flow-information>
                <flow-information junos:style="brief">
                    <direction>Out</direction>
                    <source-address>21.21.21.21</source-address>
                    <source-port>500</source-port>
                    <destination-address>22.22.22.22</destination-address>
                    <destination-port>500</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>.local..0</interface-name>
                    <session-token>0x2</session-token>
                    <flag>0x30</flag>
                    <route>0xfffb0006</route>
                    <gateway>21.21.21.21</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>10</pkt-cnt>
                    <byte-cnt>1120</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>45</session-identifier>
                <status>Normal</status>
                <session-flag>0x40/0x0/0x2/0x23</session-flag>
                <policy>self-traffic-policy/1</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>1800</configured-timeout>
                <timeout>1778</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>744</start-time>
                <duration>97</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>20.20.20.20</source-address>
                    <source-port>65169</source-port>
                    <destination-address>20.20.20.21</destination-address>
                    <destination-port>179</destination-port>
                    <protocol>tcp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>.local..0</interface-name>
                    <session-token>0x2</session-token>
                    <flag>0x31</flag>
                    <route>0xfffb0006</route>
                    <gateway>20.20.20.20</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>5</pkt-cnt>
                    <byte-cnt>336</byte-cnt>
                </flow-information>
                <flow-information junos:style="brief">
                    <direction>Out</direction>
                    <source-address>20.20.20.21</source-address>
                    <source-port>179</source-port>
                    <destination-address>20.20.20.20</destination-address>
                    <destination-port>65169</destination-port>
                    <protocol>tcp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/2.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x20</flag>
                    <route>0x1c0010</route>
                    <gateway>21.21.21.22</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>7</pkt-cnt>
                    <byte-cnt>440</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>46</session-identifier>
                <status>Normal</status>
                <session-flag>0x40/0x0/0x2/0x23</session-flag>
                <policy>self-traffic-policy/1</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <application-name>junos-ike</application-name>
                <application-value>54</application-value>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>60</configured-timeout>
                <timeout>54</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>745</start-time>
                <duration>96</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>26.26.26.26</source-address>
                    <source-port>500</source-port>
                    <destination-address>25.25.25.25</destination-address>
                    <destination-port>500</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>ge-0/0/4.0</interface-name>
                    <session-token>0x8</session-token>
                    <flag>0x21</flag>
                    <route>0x1d0010</route>
                    <gateway>25.25.25.26</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>10</pkt-cnt>
                    <byte-cnt>1120</byte-cnt>
                </flow-information>
                <flow-information junos:style="brief">
                    <direction>Out</direction>
                    <source-address>25.25.25.25</source-address>
                    <source-port>500</source-port>
                    <destination-address>26.26.26.26</destination-address>
                    <destination-port>500</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>.local..0</interface-name>
                    <session-token>0x2</session-token>
                    <flag>0x30</flag>
                    <route>0xfffb0006</route>
                    <gateway>25.25.25.25</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>10</pkt-cnt>
                    <byte-cnt>1120</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>47</session-identifier>
                <status>Normal</status>
                <session-flag>0x40/0x0/0x2/0x123</session-flag>
                <policy>self-traffic-policy/1</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>60</configured-timeout>
                <timeout>60</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>772</start-time>
                <duration>70</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>13.13.13.1</source-address>
                    <source-port>36051</source-port>
                    <destination-address>13.13.13.2</destination-address>
                    <destination-port>36050</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>.local..12</interface-name>
                    <session-token>0xc002</session-token>
                    <flag>0x631</flag>
                    <route>0xfffb0006</route>
                    <gateway>13.13.13.1</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>69</pkt-cnt>
                    <byte-cnt>22389</byte-cnt>
                </flow-information>
                <flow-information junos:style="brief">
                    <direction>Out</direction>
                    <source-address>13.13.13.2</source-address>
                    <source-port>36050</source-port>
                    <destination-address>13.13.13.1</destination-address>
                    <destination-port>36051</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>gr-0/0/0.0</interface-name>
                    <session-token>0xc00b</session-token>
                    <flag>0x620</flag>
                    <route>0xf0010</route>
                    <gateway>13.13.13.2</gateway>
                    <tunnel-id>87</tunnel-id>
                    <tunnel-type>Generic</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>69</pkt-cnt>
                    <byte-cnt>8613</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>48</session-identifier>
                <status>Normal</status>
                <session-flag>0x40/0x0/0x2/0x123</session-flag>
                <policy>self-traffic-policy/1</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>60</configured-timeout>
                <timeout>60</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>772</start-time>
                <duration>70</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>14.14.14.1</source-address>
                    <source-port>36051</source-port>
                    <destination-address>14.14.14.2</destination-address>
                    <destination-port>36050</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>.local..12</interface-name>
                    <session-token>0xc002</session-token>
                    <flag>0x631</flag>
                    <route>0xfffb0006</route>
                    <gateway>14.14.14.1</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>69</pkt-cnt>
                    <byte-cnt>22389</byte-cnt>
                </flow-information>
                <flow-information junos:style="brief">
                    <direction>Out</direction>
                    <source-address>14.14.14.2</source-address>
                    <source-port>36050</source-port>
                    <destination-address>14.14.14.1</destination-address>
                    <destination-port>36051</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>gr-0/0/0.1</interface-name>
                    <session-token>0xc00b</session-token>
                    <flag>0x620</flag>
                    <route>0x120010</route>
                    <gateway>14.14.14.2</gateway>
                    <tunnel-id>88</tunnel-id>
                    <tunnel-type>Generic</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>69</pkt-cnt>
                    <byte-cnt>8613</byte-cnt>
                </flow-information>
            </flow-session>
            <flow-session junos:style="brief">
                <session-identifier>49</session-identifier>
                <status>Normal</status>
                <session-flag>0x40/0x0/0x2/0x123</session-flag>
                <policy>self-traffic-policy/1</policy>
                <nat-source-pool-name>Null</nat-source-pool-name>
                <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                <encryption-traffic-name> Unknown</encryption-traffic-name>
                <url-category-name> </url-category-name>
                <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                <configured-timeout>60</configured-timeout>
                <timeout>60</timeout>
                <sess-state>Valid</sess-state>
                <wan-acceleration></wan-acceleration>
                <start-time>772</start-time>
                <duration>70</duration>
                <session-mask>0</session-mask>
                <flow-information junos:style="brief">
                    <direction>In</direction>
                    <source-address>15.15.15.1</source-address>
                    <source-port>36051</source-port>
                    <destination-address>15.15.15.2</destination-address>
                    <destination-port>36050</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>.local..12</interface-name>
                    <session-token>0xc002</session-token>
                    <flag>0x631</flag>
                    <route>0xfffb0006</route>
                    <gateway>15.15.15.1</gateway>
                    <tunnel-id>0</tunnel-id>
                    <tunnel-type>None</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>70</pkt-cnt>
                    <byte-cnt>22714</byte-cnt>
                </flow-information>
                <flow-information junos:style="brief">
                    <direction>Out</direction>
                    <source-address>15.15.15.2</source-address>
                    <source-port>36050</source-port>
                    <destination-address>15.15.15.1</destination-address>
                    <destination-port>36051</destination-port>
                    <protocol>udp</protocol>
                    <conn-tag>0x0</conn-tag>
                    <interface-name>gr-0/0/0.2</interface-name>
                    <session-token>0xc00b</session-token>
                    <flag>0x620</flag>
                    <route>0x150010</route>
                    <gateway>15.15.15.2</gateway>
                    <tunnel-id>89</tunnel-id>
                    <tunnel-type>Generic</tunnel-type>
                    <port-sequence>0</port-sequence>
                    <fin-sequence>0</fin-sequence>
                    <fin-state>0</fin-state>
                    <seq-ack-diff>0</seq-ack-diff>
                    <pkt-cnt>70</pkt-cnt>
                    <byte-cnt>8738</byte-cnt>
                </flow-information>
            </flow-session>
            <displayed-session-count>16</displayed-session-count>
        </flow-session-information>
        <cli>
            <banner></banner>
        </cli>
    </rpc-reply>
    """

        self.response["FLOW_GATE_HA_LE"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.2I0/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-gate-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-flow">
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-gate-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-flow">
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["FLOW_GATE_HA_HE"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/19.2I0/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC2 PIC0:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC2 PIC1:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC5 PIC0:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC5 PIC1:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC5 PIC2:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC5 PIC3:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC2 PIC0:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC2 PIC1:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC5 PIC0:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC5 PIC1:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC5 PIC2:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
            <flow-gate-information xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <flow-gate-fpc-pic-id> on FPC5 PIC3:</flow-gate-fpc-pic-id>
                <displayed-gate-valid>0</displayed-gate-valid>
                <displayed-gate-pending>0</displayed-gate-pending>
                <displayed-gate-invalidated>0</displayed-gate-invalidated>
                <displayed-gate-other>0</displayed-gate-other>
                <displayed-gate-count>0</displayed-gate-count>
            </flow-gate-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node0}</banner>
    </cli>
</rpc-reply>
        """

        self.response["FLOW_GATE_SA_LE"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.1I0/junos">
    <flow-gate-information xmlns="http://xml.juniper.net/junos/20.1I0/junos-flow">
        <displayed-gate-valid>0</displayed-gate-valid>
        <displayed-gate-pending>0</displayed-gate-pending>
        <displayed-gate-invalidated>0</displayed-gate-invalidated>
        <displayed-gate-other>0</displayed-gate-other>
        <displayed-gate-count>0</displayed-gate-count>
    </flow-gate-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["FLOW_GATE_SA_HE"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.2I0/junos">
    <flow-gate-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-flow">
        <flow-gate-fpc-pic-id> on FPC0 PIC0:</flow-gate-fpc-pic-id>
        <displayed-gate-valid>0</displayed-gate-valid>
        <displayed-gate-pending>0</displayed-gate-pending>
        <displayed-gate-invalidated>0</displayed-gate-invalidated>
        <displayed-gate-other>0</displayed-gate-other>
        <displayed-gate-count>0</displayed-gate-count>
    </flow-gate-information>
    <flow-gate-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-flow">
        <flow-gate-fpc-pic-id> on FPC0 PIC1:</flow-gate-fpc-pic-id>
        <displayed-gate-valid>0</displayed-gate-valid>
        <displayed-gate-pending>0</displayed-gate-pending>
        <displayed-gate-invalidated>0</displayed-gate-invalidated>
        <displayed-gate-other>0</displayed-gate-other>
        <displayed-gate-count>0</displayed-gate-count>
    </flow-gate-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["TICKET_5532_XML_1"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/18.3I0/junos-flow">
        <flow-session junos:style="brief">
            <session-identifier>1</session-identifier>
            <status>Normal</status>
            <session-flag>0x10000/0x0/0x0/0x1</session-flag>
            <policy>N/A</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>N/A</configured-timeout>
            <timeout>N/A</timeout>
            <sess-state>Valid</sess-state>
            <wan-acceleration></wan-acceleration>
            <start-time>370</start-time>
            <duration>174</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>70.0.0.1</source-address>
                <source-port>1</source-port>
                <destination-address>30.0.0.1</destination-address>
                <destination-port>1</destination-port>
                <protocol>ipip</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/0.0</interface-name>
                <session-token>0x9</session-token>
                <flag>0x100621</flag>
                <route>0x150010</route>
                <gateway>50.0.0.2</gateway>
                <tunnel-information>0</tunnel-information>
                <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>2</session-identifier>
            <status>Normal</status>
            <session-flag>0x10000/0x0/0x0/0x1</session-flag>
            <policy>N/A</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>N/A</configured-timeout>
            <timeout>N/A</timeout>
            <sess-state>Valid</sess-state>
            <wan-acceleration></wan-acceleration>
            <start-time>370</start-time>
            <duration>174</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>70.0.0.1</source-address>
                <source-port>1</source-port>
                <destination-address>30.0.0.1</destination-address>
                <destination-port>1</destination-port>
                <protocol>ipv6</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/0.0</interface-name>
                <session-token>0x9</session-token>
                <flag>0x621</flag>
                <route>0x150010</route>
                <gateway>50.0.0.2</gateway>
                <tunnel-information>0</tunnel-information>
                <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>3</session-identifier>
            <status>Normal</status>
            <session-flag>0x10000/0x0/0x0/0x1</session-flag>
            <policy>N/A</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>N/A</configured-timeout>
            <timeout>N/A</timeout>
            <sess-state>Valid</sess-state>
            <wan-acceleration></wan-acceleration>
            <start-time>391</start-time>
            <duration>153</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>8001::1</source-address>
                <source-port>1</source-port>
                <destination-address>3001::1</destination-address>
                <destination-port>1</destination-port>
                <protocol>gre</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ip-0/0/0.0</interface-name>
                <session-token>0x9</session-token>
                <flag>0x100623</flag>
                <route>0x160010</route>
                <gateway>::</gateway>
                <tunnel-information>0</tunnel-information>
                <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>10</session-identifier>
            <status>Normal</status>
            <session-flag>0x40/0x0/0x0/0x3</session-flag>
            <policy>default-policy-logical-system-00/2</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>60</configured-timeout>
            <timeout>2</timeout>
            <sess-state>Valid</sess-state>
            <wan-acceleration></wan-acceleration>
            <start-time>485</start-time>
            <duration>59</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>3ffd::2</source-address>
                <source-port>7</source-port>
                <destination-address>7ffd::2</destination-address>
                <destination-port>3526</destination-port>
                <protocol>icmp6</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x23</flag>
                <route>0x180010</route>
                <gateway>3ffd::2</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>1</pkt-cnt>
                <byte-cnt>104</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>7ffd::2</source-address>
                <source-port>3526</source-port>
                <destination-address>3ffd::2</destination-address>
                <destination-port>7</destination-port>
                <protocol>icmp6</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>gr-0/0/0.0</interface-name>
                <session-token>0x9</session-token>
                <flag>0x22</flag>
                <route>0x170010</route>
                <gateway>::</gateway>
                <tunnel-information>74</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>11</session-identifier>
            <status>Normal</status>
            <session-flag>0x40/0x0/0x0/0x3</session-flag>
            <policy>default-policy-logical-system-00/2</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>60</configured-timeout>
            <timeout>2</timeout>
            <sess-state>Valid</sess-state>
            <wan-acceleration></wan-acceleration>
            <start-time>486</start-time>
            <duration>58</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>3ffd::2</source-address>
                <source-port>8</source-port>
                <destination-address>7ffd::2</destination-address>
                <destination-port>3526</destination-port>
                <protocol>icmp6</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x23</flag>
                <route>0x180010</route>
                <gateway>3ffd::2</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>1</pkt-cnt>
                <byte-cnt>104</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>7ffd::2</source-address>
                <source-port>3526</source-port>
                <destination-address>3ffd::2</destination-address>
                <destination-port>8</destination-port>
                <protocol>icmp6</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>gr-0/0/0.0</interface-name>
                <session-token>0x9</session-token>
                <flag>0x22</flag>
                <route>0x170010</route>
                <gateway>::</gateway>
                <tunnel-information>74</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>12</session-identifier>
            <status>Normal</status>
            <session-flag>0x40/0x0/0x0/0x3</session-flag>
            <policy>default-policy-logical-system-00/2</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>60</configured-timeout>
            <timeout>4</timeout>
            <sess-state>Valid</sess-state>
            <wan-acceleration></wan-acceleration>
            <start-time>487</start-time>
            <duration>57</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>3ffd::2</source-address>
                <source-port>9</source-port>
                <destination-address>7ffd::2</destination-address>
                <destination-port>3526</destination-port>
                <protocol>icmp6</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x23</flag>
                <route>0x180010</route>
                <gateway>3ffd::2</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>1</pkt-cnt>
                <byte-cnt>104</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>7ffd::2</source-address>
                <source-port>3526</source-port>
                <destination-address>3ffd::2</destination-address>
                <destination-port>9</destination-port>
                <protocol>icmp6</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>gr-0/0/0.0</interface-name>
                <session-token>0x9</session-token>
                <flag>0x22</flag>
                <route>0x170010</route>
                <gateway>::</gateway>
                <tunnel-information>74</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>44</session-identifier>
            <status>Normal</status>
            <session-flag>0x40/0x0/0x0/0x8003</session-flag>
            <policy>default-policy-logical-system-00/2</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <application-name>junos-http</application-name>
            <application-value>6</application-value>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>300</configured-timeout>
            <timeout>300</timeout>
            <sess-state>Valid</sess-state>
            <wan-acceleration></wan-acceleration>
            <start-time>535</start-time>
            <duration>9</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>3ffd::2</source-address>
                <source-port>44527</source-port>
                <destination-address>7ffd::2</destination-address>
                <destination-port>80</destination-port>
                <protocol>tcp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>ge-0/0/1.0</interface-name>
                <session-token>0x8</session-token>
                <flag>0x1023</flag>
                <route>0x180010</route>
                <gateway>3ffd::2</gateway>
                <tunnel-information>0</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>192</pkt-cnt>
                <byte-cnt>19912</byte-cnt>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>7ffd::2</source-address>
                <source-port>80</source-port>
                <destination-address>3ffd::2</destination-address>
                <destination-port>44527</destination-port>
                <protocol>tcp</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>gr-0/0/0.0</interface-name>
                <session-token>0x9</session-token>
                <flag>0x1022</flag>
                <route>0x170010</route>
                <gateway>::</gateway>
                <tunnel-information>74</tunnel-information>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>97</pkt-cnt>
                <byte-cnt>13072</byte-cnt>
            </flow-information>
        </flow-session>
        <displayed-session-count>7</displayed-session-count>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["FLOW_SESSION_WITH_NA_TIMEOUT"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.3I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
        <flow-session junos:style="brief">
            <session-identifier>4135</session-identifier>
            <status>Normal</status>
            <session-flag>0x10000/0x0/0x0/0x1</session-flag>
            <policy>N/A</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <url-category-name> </url-category-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>N/A</configured-timeout>
            <timeout>N/A</timeout>
            <sess-state>Valid</sess-state>
            <wan-acceleration></wan-acceleration>
            <start-time>181552</start-time>
            <duration>93</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>192.168.255.10</source-address>
                <source-port>2048</source-port>
                <destination-address>192.168.255.1</destination-address>
                <destination-port>2048</destination-port>
                <protocol>pim</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>lt-0/0/0.2</interface-name>
                <session-token>0x7</session-token>
                <flag>0x621</flag>
                <route>0x170010</route>
                <gateway>192.168.255.6</gateway>
                <tunnel-id>0</tunnel-id>
                <tunnel-type>None</tunnel-type>
                <recv-ipv4-post-frags-counter>0</recv-ipv4-post-frags-counter>
                <gen-ipv4-post-frags-counter>0</gen-ipv4-post-frags-counter>
                <recv-ipv4-pre-frags-counter>0</recv-ipv4-pre-frags-counter>
                <ipv4-tx-to-tunnel-frags>0</ipv4-tx-to-tunnel-frags>
                <gen-ipv4-pre-frags-counter>0</gen-ipv4-pre-frags-counter>
                <recv-ipv6-pre-frags-counter>0</recv-ipv6-pre-frags-counter>
                <ipv6-tx-to-tunnel-frags>0</ipv6-tx-to-tunnel-frags>
                <gen-ipv6-pre-frags-counter>0</gen-ipv6-pre-frags-counter>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
                <dcp-session-id>0</dcp-session-id>
            </flow-information>
        </flow-session>
        <flow-session junos:style="brief">
            <session-identifier>4136</session-identifier>
            <status>Normal</status>
            <session-flag>0x40/0x0/0x2/0x23</session-flag>
            <policy>self-traffic-policy/1</policy>
            <nat-source-pool-name>Null</nat-source-pool-name>
            <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
            <encryption-traffic-name> Unknown</encryption-traffic-name>
            <url-category-name> </url-category-name>
            <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
            <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
            <configured-timeout>300</configured-timeout>
            <timeout>284</timeout>
            <sess-state>Valid</sess-state>
            <wan-acceleration></wan-acceleration>
            <start-time>181553</start-time>
            <duration>92</duration>
            <session-mask>0</session-mask>
            <flow-information junos:style="brief">
                <direction>In</direction>
                <source-address>192.168.255.1</source-address>
                <source-port>1</source-port>
                <destination-address>224.0.0.13</destination-address>
                <destination-port>1</destination-port>
                <protocol>pim</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>lt-0/0/0.3</interface-name>
                <session-token>0xa008</session-token>
                <flag>0x40000021</flag>
                <route>0x0</route>
                <gateway>192.168.255.1</gateway>
                <tunnel-id>0</tunnel-id>
                <tunnel-type>None</tunnel-type>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>10</pkt-cnt>
                <byte-cnt>580</byte-cnt>
                <dcp-session-id>28891</dcp-session-id>
            </flow-information>
            <flow-information junos:style="brief">
                <direction>Out</direction>
                <source-address>224.0.0.13</source-address>
                <source-port>1</source-port>
                <destination-address>192.168.255.1</destination-address>
                <destination-port>1</destination-port>
                <protocol>pim</protocol>
                <conn-tag>0x0</conn-tag>
                <interface-name>.local..10</interface-name>
                <session-token>0xa002</session-token>
                <flag>0x40000030</flag>
                <route>0xfff80006</route>
                <gateway>224.0.0.13</gateway>
                <tunnel-id>0</tunnel-id>
                <tunnel-type>None</tunnel-type>
                <port-sequence>0</port-sequence>
                <fin-sequence>0</fin-sequence>
                <fin-state>0</fin-state>
                <seq-ack-diff>0</seq-ack-diff>
                <pkt-cnt>0</pkt-cnt>
                <byte-cnt>0</byte-cnt>
                <dcp-session-id>28891</dcp-session-id>
            </flow-information>
        </flow-session>
        <displayed-session-count>2</displayed-session-count>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["HA_LE_FLOW_PMI_STATISTICS"] = """
<rpc-reply>
<multi-routing-engine-results>
  <multi-routing-engine-item>
    <re-name>node0</re-name>
    <flow-pmi-statistics>
      <pmi-rx>0</pmi-rx>
      <pmi-tx>0</pmi-tx>
      <pmi-rfp>0</pmi-rfp>
      <pmi-drop>0</pmi-drop>
      <pmi-encap-bytes>0</pmi-encap-bytes>
      <pmi-decap-bytes>0</pmi-decap-bytes>
      <pmi-encap-pkts>0</pmi-encap-pkts>
      <pmi-decap-pkts>0</pmi-decap-pkts>
    </flow-pmi-statistics>
  </multi-routing-engine-item>
  <multi-routing-engine-item>
    <re-name>node1</re-name>
    <flow-pmi-statistics>
      <pmi-rx>0</pmi-rx>
      <pmi-tx>0</pmi-tx>
      <pmi-rfp>0</pmi-rfp>
      <pmi-drop>0</pmi-drop>
      <pmi-encap-bytes>0</pmi-encap-bytes>
      <pmi-decap-bytes>0</pmi-decap-bytes>
      <pmi-encap-pkts>0</pmi-encap-pkts>
      <pmi-decap-pkts>0</pmi-decap-pkts>
    </flow-pmi-statistics>
  </multi-routing-engine-item>
</multi-routing-engine-results>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["HA_HE_FLOW_PMI_STATISTICS"] = """
<rpc-reply>
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <pmi-spu-id>of FPC2 PIC0:</pmi-spu-id>
                <pmi-rx>0</pmi-rx>
                <pmi-tx>0</pmi-tx>
                <pmi-rfp>0</pmi-rfp>
                <pmi-drop>0</pmi-drop>
                <pmi-encap-bytes>0</pmi-encap-bytes>
                <pmi-decap-bytes>0</pmi-decap-bytes>
                <pmi-encap-pkts>0</pmi-encap-pkts>
                <pmi-decap-pkts>0</pmi-decap-pkts>
            </flow-pmi-statistics>
            <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <pmi-spu-id>of FPC2 PIC1:</pmi-spu-id>
                <pmi-rx>0</pmi-rx>
                <pmi-tx>0</pmi-tx>
                <pmi-rfp>0</pmi-rfp>
                <pmi-drop>0</pmi-drop>
                <pmi-encap-bytes>0</pmi-encap-bytes>
                <pmi-decap-bytes>0</pmi-decap-bytes>
                <pmi-encap-pkts>0</pmi-encap-pkts>
                <pmi-decap-pkts>0</pmi-decap-pkts>
            </flow-pmi-statistics>
            <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <pmi-spu-id>summary:</pmi-spu-id>
                <pmi-rx>0</pmi-rx>
                <pmi-tx>0</pmi-tx>
                <pmi-rfp>0</pmi-rfp>
                <pmi-drop>0</pmi-drop>
                <pmi-encap-bytes>0</pmi-encap-bytes>
                <pmi-decap-bytes>0</pmi-decap-bytes>
                <pmi-encap-pkts>0</pmi-encap-pkts>
                <pmi-decap-pkts>0</pmi-decap-pkts>
            </flow-pmi-statistics>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <pmi-spu-id>of FPC2 PIC0:</pmi-spu-id>
                <pmi-rx>0</pmi-rx>
                <pmi-tx>0</pmi-tx>
                <pmi-rfp>0</pmi-rfp>
                <pmi-drop>0</pmi-drop>
                <pmi-encap-bytes>0</pmi-encap-bytes>
                <pmi-decap-bytes>0</pmi-decap-bytes>
                <pmi-encap-pkts>0</pmi-encap-pkts>
                <pmi-decap-pkts>0</pmi-decap-pkts>
            </flow-pmi-statistics>
            <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <pmi-spu-id>of FPC2 PIC1:</pmi-spu-id>
                <pmi-rx>0</pmi-rx>
                <pmi-tx>0</pmi-tx>
                <pmi-rfp>0</pmi-rfp>
                <pmi-drop>0</pmi-drop>
                <pmi-encap-bytes>0</pmi-encap-bytes>
                <pmi-decap-bytes>0</pmi-decap-bytes>
                <pmi-encap-pkts>0</pmi-encap-pkts>
                <pmi-decap-pkts>0</pmi-decap-pkts>
            </flow-pmi-statistics>
            <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/19.2I0/junos-flow">
                <pmi-spu-id>summary:</pmi-spu-id>
                <pmi-rx>0</pmi-rx>
                <pmi-tx>0</pmi-tx>
                <pmi-rfp>0</pmi-rfp>
                <pmi-drop>0</pmi-drop>
                <pmi-encap-bytes>0</pmi-encap-bytes>
                <pmi-decap-bytes>0</pmi-decap-bytes>
                <pmi-encap-pkts>0</pmi-encap-pkts>
                <pmi-decap-pkts>0</pmi-decap-pkts>
            </flow-pmi-statistics>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["SA_LE_FLOW_PMI_STATISTICS"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.3I0/junos">
    <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/20.1I0/junos-flow">
        <pmi-rx>0</pmi-rx>
        <pmi-tx>0</pmi-tx>
        <pmi-rfp>0</pmi-rfp>
        <pmi-drop>0</pmi-drop>
        <pmi-encap-bytes>0</pmi-encap-bytes>
        <pmi-decap-bytes>0</pmi-decap-bytes>
        <pmi-encap-pkts>0</pmi-encap-pkts>
        <pmi-decap-pkts>0</pmi-decap-pkts>
    </flow-pmi-statistics>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["WRONG_FLOW_PMI_STATISTICS"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.3I0/junos">
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """

        self.response["SA_HE_FLOW_PMI_STATISTICS"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.3I0/junos">
    <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
        <pmi-spu-id>of FPC0 PIC0:</pmi-spu-id>
        <pmi-rx>0</pmi-rx>
        <pmi-tx>0</pmi-tx>
        <pmi-rfp>0</pmi-rfp>
        <pmi-drop>0</pmi-drop>
        <pmi-encap-bytes>0</pmi-encap-bytes>
        <pmi-decap-bytes>0</pmi-decap-bytes>
        <pmi-encap-pkts>0</pmi-encap-pkts>
        <pmi-decap-pkts>0</pmi-decap-pkts>
    </flow-pmi-statistics>
    <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
        <pmi-spu-id>of FPC0 PIC1:</pmi-spu-id>
        <pmi-rx>0</pmi-rx>
        <pmi-tx>0</pmi-tx>
        <pmi-rfp>0</pmi-rfp>
        <pmi-drop>0</pmi-drop>
        <pmi-encap-bytes>0</pmi-encap-bytes>
        <pmi-decap-bytes>0</pmi-decap-bytes>
        <pmi-encap-pkts>0</pmi-encap-pkts>
        <pmi-decap-pkts>0</pmi-decap-pkts>
    </flow-pmi-statistics>
    <flow-pmi-statistics xmlns="http://xml.juniper.net/junos/20.3I0/junos-flow">
        <pmi-spu-id>summary:</pmi-spu-id>
        <pmi-rx>0</pmi-rx>
        <pmi-tx>0</pmi-tx>
        <pmi-rfp>0</pmi-rfp>
        <pmi-drop>0</pmi-drop>
        <pmi-encap-bytes>0</pmi-encap-bytes>
        <pmi-decap-bytes>0</pmi-decap-bytes>
        <pmi-encap-pkts>0</pmi-encap-pkts>
        <pmi-decap-pkts>0</pmi-decap-pkts>
    </flow-pmi-statistics>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """



    def tearDown(self):
        """teardown after all case"""
        pass

    @mock.patch.object(dev, "execute_config_command_on_device")
    def test_configure_flow_advance_option(self, mock_send_conf_cmd):
        """checking set flow advance option"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        unittest_result = True

        # step 1: add configure
        step_info = "add flow advance option"
        print(step_info)
        checkpoint_list = []
        mock_send_conf_cmd.return_value = "commit complete"
        cmd_list = self.ins.configure_flow_advance_option(
            device=mock_device_ins,
            return_cmd=True,
            drop_matching_link_local_address=True,
            drop_matching_reserved_ip_address=True,
        )
        for cmd in cmd_list:
            if re.match(r"set\s+.*drop-matching-link-local-address", cmd):
                checkpoint_list.append(True)

            if re.match(r"set\s+.*drop-matching-reserved-ip-address", cmd):
                checkpoint_list.append(True)

        if len(checkpoint_list) != 2 or False in checkpoint_list:
            print(step_info)
            unittest_result = False
        else:
            print(step_info)

        # step 2: del configure
        step_info = "delete flow advance option"
        print(step_info)
        checkpoint_list = []
        cmd_list = self.ins.configure_flow_advance_option(
            device=mock_device_ins,
            return_cmd=True,
            drop_matching_link_local_address=False,
            drop_matching_reserved_ip_address=False,
        )
        for cmd in cmd_list:
            if re.match(r"delete\s+.*drop-matching-link-local-address", cmd):
                checkpoint_list.append(True)

            if re.match(r"delete\s+.*drop-matching-reserved-ip-address", cmd):
                checkpoint_list.append(True)

        if len(checkpoint_list) != 2 or False in checkpoint_list:
            print(step_info)
            unittest_result = False
        else:
            print(step_info)

        self.assertTrue(unittest_result is True)

        # step 3: get configure response
        step_info = "get flow advance option commit response"
        print(step_info)
        checkpoint_list = []
        response = self.ins.configure_flow_advance_option(
            device=mock_device_ins,
            get_response=True,
            drop_matching_link_local_address=False,
            drop_matching_reserved_ip_address=False,
        )
        if not re.search("commit complete", response):
            unittest_result = False

        self.assertTrue(unittest_result is True)

    @mock.patch.object(dev, "execute_config_command_on_device")
    def test_configure_flow_forwarding_option(self, mock_send_conf_cmd):
        """Checking set FLOW forwarding mode feature"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        mock_send_conf_cmd.return_value = "commit complete"
        print("Testing set forwarding mode")
        cmd_list = self.ins.configure_flow_forwarding_option(
            device=mock_device_ins,
            return_cmd=True,
            ipv6_mode="flow-based",
            iso_mode="packet-based",
            mpls_mode="packet-based",
        )

        all_patterns = (
            "set security forwarding-options family inet6 mode flow-based",
            "set security forwarding-options family iso mode packet-based",
            "set security forwarding-options family mpls mode packet-based",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

        print("Testing set forwarding mode with response")
        cmd_list = self.ins.configure_flow_forwarding_option(
            device=mock_device_ins,
            return_cmd=True,
            ipv6_mode="flow-based",
            get_response=True,
        )

        all_patterns = (
            "set security forwarding-options family inet6 mode flow-based",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

    @mock.patch.object(dev, "execute_config_command_on_device")
    def test_configure_flow_aging(self, mock_send_conf_cmd):
        """Checking set FLOW aging feature"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_send_conf_cmd.return_value = "commit complete"

        print("Testing set flow aging")
        cmd_list = self.ins.configure_flow_aging(
            device=mock_device_ins,
            return_cmd=True,
            early_ageout=100,
            high_watermark=100,
            low_watermark=100,
        )

        all_patterns = (
            "set security flow aging early-ageout 100",
            "set security flow aging high-watermark 100",
            "set security flow aging low-watermark 100",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

        print("Testing set flow aging with response")
        cmd_list = self.ins.configure_flow_aging(
            device=mock_device_ins,
            return_cmd=True,
            early_ageout=100,
            get_response=True,
        )

        all_patterns = (
            "set security flow aging early-ageout 100",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

    @mock.patch.object(dev, "execute_config_command_on_device")
    def test_configure_flow_enhance_configuration(self, mock_send_conf_cmd):
        """Checking set FLOW enhance configuration feature"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        mock_send_conf_cmd.return_value = "commit complete"

        print("Testing set flow enhance configuration")
        cmd_list = self.ins.configure_flow_enhance_configuration(
            device=mock_device_ins,
            return_cmd=True,
            force_ip_reassembly=True,
            allow_dns_reply=True,
            allow_embedded_icmp=True,
            mcast_buffer_enhance=True,
            sync_icmp_session=True,
            pending_sess_queue_length="high",
            syn_flood_protection_mode="syn-cookie",
            route_change_timeout=30,
        )

        all_patterns = (
            "set security flow force-ip-reassembly",
            "set security flow allow-dns-reply",
            "set security flow allow-embedded-icmp",
            "set security flow mcast-buffer-enhance",
            "set security flow sync-icmp-session",
            "set security flow pending-sess-queue-length high",
            "set security flow syn-flood-protection-mode syn-cookie",
            "set security flow route-change-timeout 30",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

        print("Testing set flow tcp-session with response")
        cmd_list = self.ins.configure_flow_enhance_configuration(
            device=mock_device_ins,
            return_cmd=True,
            get_response=True,
            force_ip_reassembly=True,
        )
        all_patterns = (
            "set security flow force-ip-reassembly",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

    @mock.patch.object(dev, "execute_config_command_on_device")
    def test_configure_flow_tcp_mss(self, mock_send_conf_cmd):
        """Checking set FLOW tcp-mss feature"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_send_conf_cmd.return_value = "commit complete"

        print("Testing set flow tcp-mss")
        cmd_list = self.ins.configure_flow_tcp_mss(
            device=mock_device_ins,
            return_cmd=True,
            all_tcp_mss=100,
            gre_in_mss=100,
            gre_out_mss=100,
            ipsec_vpn_mss=100,
        )

        all_patterns = (
            "set security flow tcp-mss all-tcp mss 100",
            "set security flow tcp-mss gre-in mss 100",
            "set security flow tcp-mss gre-out mss 100",
            "set security flow tcp-mss ipsec-vpn mss 100",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

        print("Testing set flow tcp-mss with response")
        cmd_list = self.ins.configure_flow_tcp_mss(
            device=mock_device_ins,
            return_cmd=True,
            get_response=True,
            all_tcp_mss=100,
            gre_in_mss=100,
        )

        all_patterns = (
            "set security flow tcp-mss all-tcp mss 100",
            "set security flow tcp-mss gre-in mss 100",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

    @mock.patch.object(dev, "execute_config_command_on_device")
    def test_configure_flow_tcp_session(self, mock_send_conf_cmd):
        """Checking set FLOW tcp-session feature"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_send_conf_cmd.return_value = "commit complete"

        print("Testing set flow tcp-session")
        cmd_list = self.ins.configure_flow_tcp_session(
            device=mock_device_ins,
            return_cmd=True,
            fin_invalidate_session=True,
            no_sequence_check=True,
            no_syn_check=True,
            no_syn_check_in_tunnel=True,
            rst_invalidate_session=True,
            rst_sequence_check=True,
            strict_syn_check=True,
            time_wait_state_apply_to_half_close_state=True,
            time_wait_state_session_ageout=True,
            maximum_window="128K",
            tcp_initial_timeout=30,
            time_wait_state_session_timeout=30,
        )

        all_patterns = (
            "set security flow tcp-session fin-invalidate-session",
            "set security flow tcp-session no-sequence-check",
            "set security flow tcp-session no-syn-check",
            "set security flow tcp-session no-syn-check-in-tunnel",
            "set security flow tcp-session rst-invalidate-session",
            "set security flow tcp-session rst-sequence-check",
            "set security flow tcp-session strict-syn-check",
            "set security flow tcp-session tcp-initial-timeout 30",
            "set security flow tcp-session time-wait-state apply-to-half-close-state",
            "set security flow tcp-session time-wait-state session-ageout",
            "set security flow tcp-session time-wait-state session-timeout 30",
            "set security flow tcp-session maximum-window 128K",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

        print("Testing set flow tcp-session with response")
        cmd_list = self.ins.configure_flow_tcp_session(
            device=mock_device_ins,
            return_cmd=True,
            get_response=True,
            fin_invalidate_session=True,
        )
        all_patterns = (
            "set security flow tcp-session fin-invalidate-session",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

    @mock.patch.object(dev, "execute_config_command_on_device")
    def test_configure_flow_traceoptions(self, mock_send_conf_cmd):
        """Checking set FLOW traceoption feature"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_send_conf_cmd.return_value = "commit complete"

        print("Testing set flow traceoption")
        cmd_list = self.ins.configure_flow_traceoptions(
            device=mock_device_ins,
            return_cmd=True,
            file_size=120058,
        )

        all_patterns = (
            "set security traceoptions file flow_trace.log size 120058",
            "set security flow traceoptions file flow_trace.log size 120058",
            "set security traceoptions flag all",
            "set security flow traceoptions flag all",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

        print("Testing set flow traceoption with response")
        cmd_list = self.ins.configure_flow_traceoptions(
            device=mock_device_ins,
            return_cmd=True,
            get_response=True,
            filename="aaa.log",
        )
        all_patterns = (
            "set security traceoptions file aaa.log size 10485760",
            "set security flow traceoptions file aaa.log size 10485760",
            "set security traceoptions flag all",
            "set security flow traceoptions flag all",
        )
        for pattern in all_patterns:
            level = "INFO" if pattern in cmd_list else "ERR"
            print("checking cmd '{}'".format(pattern))
            self.assertTrue(level == "INFO")

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_fetch_flow_session(self, mock_execute_cli_command_on_device):
        """UT CASE"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("Get session from HE platform on SA by XML")
        print("checking HighEnd platform on SA topo that 1 FPC have 1 session")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC"],
        )
        all_session_tuple = self.ins.fetch_flow_session(
            device=mock_device_ins,
            options="family inet",
            return_mode="session_tuple",
        )
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 1)
        self.assertEqual(all_session_tuple[0]["application-traffic-control-rule-name"], "INVALID")
        self.assertEqual(all_session_tuple[0]["flow-information"][0]["direction"], "In")
        self.assertEqual(all_session_tuple[0]["flow-information"][1]["direction"], "Out")
        self.assertEqual(all_session_tuple[0]["flow-fpc-pic-id"], "on FPC0 PIC2:")
        self.assertEqual(all_session_tuple[0]["sess-state"], "Valid")

        print("checking HighEnd platform on SA topo that 1 FPC have 1 session for flat response")
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_mode="flat_dict")
        print(self.tool.pprint(all_session_tuple))
        self.assertEqual(len(all_session_tuple), 1)
        self.assertEqual(all_session_tuple[0]["application_traffic_control_rule_name"], "INVALID")
        self.assertEqual(all_session_tuple[0]["application_traffic_control_rule_set_name"], "INVALID")
        self.assertEqual(all_session_tuple[0]["configured_timeout"], "1800")
        self.assertEqual(all_session_tuple[0]["duration"], "2")
        self.assertEqual(all_session_tuple[0]["dynamic_application_name"], "junos:UNKNOWN")
        self.assertEqual(all_session_tuple[0]["encryption_traffic_name"], "Unknown")
        self.assertEqual(all_session_tuple[0]["flow_fpc_pic_id"], "on FPC0 PIC2:")
        self.assertEqual(all_session_tuple[0]["in_byte_cnt"], "2816")
        self.assertEqual(all_session_tuple[0]["in_conn_tag"], "0x0")
        self.assertEqual(all_session_tuple[0]["in_dcp_session_id"], "20002443")
        self.assertEqual(all_session_tuple[0]["in_destination_address"], "2000:200::2")
        self.assertEqual(all_session_tuple[0]["in_destination_port"], "54093")
        self.assertEqual(all_session_tuple[0]["in_fin_sequence"], "0")
        self.assertEqual(all_session_tuple[0]["in_fin_state"], "0")
        self.assertEqual(all_session_tuple[0]["in_flag"], "0x40001023")
        self.assertEqual(all_session_tuple[0]["in_gateway"], "2000:100::2")
        self.assertEqual(all_session_tuple[0]["in_interface_name"], "xe-2/0/0.0")
        self.assertEqual(all_session_tuple[0]["in_pkt_cnt"], "39")
        self.assertEqual(all_session_tuple[0]["in_port_sequence"], "0")
        self.assertEqual(all_session_tuple[0]["in_protocol"], "tcp")
        self.assertEqual(all_session_tuple[0]["in_route"], "0xd0010")
        self.assertEqual(all_session_tuple[0]["in_seq_ack_diff"], "0")
        self.assertEqual(all_session_tuple[0]["in_session_token"], "0x7")
        self.assertEqual(all_session_tuple[0]["in_source_address"], "2000:100::2")
        self.assertEqual(all_session_tuple[0]["in_source_port"], "58612")
        self.assertEqual(all_session_tuple[0]["in_tunnel_information"], "0")
        self.assertEqual(all_session_tuple[0]["logical_system"], "")
        self.assertEqual(all_session_tuple[0]["nat_source_pool_name"], "Null")
        self.assertEqual(all_session_tuple[0]["out_byte_cnt"], "137776")
        self.assertEqual(all_session_tuple[0]["out_conn_tag"], "0x0")
        self.assertEqual(all_session_tuple[0]["out_dcp_session_id"], "20002443")
        self.assertEqual(all_session_tuple[0]["out_destination_address"], "2000:100::2")
        self.assertEqual(all_session_tuple[0]["out_destination_port"], "58612")
        self.assertEqual(all_session_tuple[0]["out_fin_sequence"], "0")
        self.assertEqual(all_session_tuple[0]["out_fin_state"], "0")
        self.assertEqual(all_session_tuple[0]["out_flag"], "0x40001022")
        self.assertEqual(all_session_tuple[0]["out_gateway"], "2000:200::2")
        self.assertEqual(all_session_tuple[0]["out_interface_name"], "xe-2/0/1.0")
        self.assertEqual(all_session_tuple[0]["out_pkt_cnt"], "93")
        self.assertEqual(all_session_tuple[0]["out_port_sequence"], "0")
        self.assertEqual(all_session_tuple[0]["out_protocol"], "tcp")
        self.assertEqual(all_session_tuple[0]["out_route"], "0xe0010")
        self.assertEqual(all_session_tuple[0]["out_seq_ack_diff"], "0")
        self.assertEqual(all_session_tuple[0]["out_session_token"], "0x8")
        self.assertEqual(all_session_tuple[0]["out_source_address"], "2000:200::2")
        self.assertEqual(all_session_tuple[0]["out_source_port"], "54093")
        self.assertEqual(all_session_tuple[0]["out_tunnel_information"], "0")
        self.assertEqual(all_session_tuple[0]["policy"], "p1/4")
        self.assertEqual(all_session_tuple[0]["sess_state"], "Valid")
        self.assertEqual(all_session_tuple[0]["session_flag"], "0x40/0x0/0x8003")
        self.assertEqual(all_session_tuple[0]["session_identifier"], "20000753")
        self.assertEqual(all_session_tuple[0]["session_mask"], "0")
        self.assertEqual(all_session_tuple[0]["start_time"], "1200007")
        self.assertEqual(all_session_tuple[0]["status"], "Normal")
        self.assertEqual(all_session_tuple[0]["timeout"], "1798")
        self.assertEqual(all_session_tuple[0]["wan_acceleration"], "")


        print("checking HighEnd platform on SA topo that 2 sessions in 1 FPC")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_ONE_FPC"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, options="family inet")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 2)
        self.assertTrue("re-name" not in all_session_tuple[0])
        self.assertTrue("re-name" not in all_session_tuple[1])

        print("checking HighEnd platform on SA topo that 2 FPCs have 2 sessions separately")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_MULTI_FPC"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, more_options="family inet", return_type="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 2)
        self.assertEqual(all_session_tuple[0]["flow-fpc-pic-id"], "on FPC0 PIC2:")
        self.assertEqual(all_session_tuple[0]["session-identifier"], "20000753")
        self.assertEqual(all_session_tuple[1]["flow-fpc-pic-id"], "on FPC0 PIC3:")
        self.assertEqual(all_session_tuple[1]["session-identifier"], "30000755")

        print("checking HighEnd platform on SA topo that 2 FPCs have 3 sessions. one FPC have single session, another FPC have 2 sessions")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_MULTI_FPC_2"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_mode="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 3)
        self.assertEqual(all_session_tuple[0]["flow-fpc-pic-id"], "on FPC0 PIC2:")
        self.assertEqual(all_session_tuple[0]["session-identifier"], "20000753")
        self.assertEqual(all_session_tuple[1]["flow-fpc-pic-id"], "on FPC0 PIC3:")
        self.assertEqual(all_session_tuple[1]["session-identifier"], "30000755")
        self.assertEqual(all_session_tuple[2]["flow-fpc-pic-id"], "on FPC0 PIC3:")
        self.assertEqual(all_session_tuple[2]["session-identifier"], "20000753")

        print("checking HighEnd platform on SA topo that no any session")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_HE_FLOW_SESSION_EMPTY_XML"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_mode="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 0)

        print("Get FLOW session from HE platform on HA by XML")
        print("checking HighEnd HA topo that one session in one fpc in one node")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC_IN_ONE_NODE"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_type="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 1)
        self.assertEqual(all_session_tuple[0]["flow-fpc-pic-id"], "on FPC0 PIC1:")
        self.assertEqual(all_session_tuple[0]["session-identifier"], "10000040")
        self.assertEqual(all_session_tuple[0]["re-name"], "node0")

        print("checking HighEnd HA topo that 2 sessions in one fpc in one node")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_ONE_FPC_IN_ONE_NODE"]
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins)
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 2)
        self.assertEqual(all_session_tuple[0]["re-name"], "node0")
        self.assertEqual(all_session_tuple[1]["re-name"], "node0")

        print("checking HighEnd HA topo have 3 sessions, one fpc have 2, another FPC have 1. other node no any session")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_HAVE_3_ENTRIES_THAT_1_IN_A_FPC_AND_2_IN_OTHER_FPC"]
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins)
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 3)
        self.assertEqual(all_session_tuple[0]["flow-fpc-pic-id"], "on FPC0 PIC1:")
        self.assertEqual(all_session_tuple[0]["session-identifier"], "10000040")
        self.assertEqual(all_session_tuple[0]["re-name"], "node0")
        self.assertEqual(all_session_tuple[1]["flow-fpc-pic-id"], "on FPC0 PIC1:")
        self.assertEqual(all_session_tuple[1]["session-identifier"], "10000040")
        self.assertEqual(all_session_tuple[1]["re-name"], "node0")
        self.assertEqual(all_session_tuple[2]["flow-fpc-pic-id"], "on FPC0 PIC3:")
        self.assertEqual(all_session_tuple[2]["session-identifier"], "10000040")
        self.assertEqual(all_session_tuple[2]["re-name"], "node0")

        print("checking HighEnd HA topo that one session in one fpc but 2 nodes all have sessions")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC_BOTH_2_NODE"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins)
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 2)
        self.assertEqual(all_session_tuple[0]["re-name"], "node0")
        self.assertEqual(all_session_tuple[0]["flow-fpc-pic-id"], "on FPC0 PIC1:")
        self.assertEqual(all_session_tuple[1]["re-name"], "node1")
        self.assertEqual(all_session_tuple[1]["flow-fpc-pic-id"], "on FPC0 PIC1:")

        print("checking HighEnd HA topo that no any sessions")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_THAT_EMPTY"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins)
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 0)

        print("Get FLOW session from HA platfrom by TEXT")
        mock_execute_cli_command_on_device.return_value = self.response["he_text"]
        all_session_entry = self.ins.fetch_flow_session(device=mock_device_ins, return_type="text")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_entry, str))

        print("Get FLOW session by wrong option")
        mock_execute_cli_command_on_device.return_value = self.response["he_text"]
        self.assertRaisesRegex(
            ValueError,
            r"'return_mode' must be 'SESSION_TUPLE', 'TEXT' or 'FLAT_DICT'",
            self.ins.fetch_flow_session,
            device=mock_device_ins, return_type="unknown"
        )

        print("Get FLOW session from LE platform on SA by XML")
        print("get multiple sessions from LE platform")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_LE_FLOW_SESSION_WITH_MULTI_ENTRY"])
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_type="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 4)
        self.assertTrue("re-name" not in all_session_tuple[0])
        self.assertEqual(all_session_tuple[0]["session-identifier"], "70")
        self.assertEqual(all_session_tuple[1]["session-identifier"], "71")
        self.assertEqual(all_session_tuple[2]["session-identifier"], "72")
        self.assertEqual(all_session_tuple[3]["session-identifier"], "73")

        print("get only 1 session from LE platform")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_LE_FLOW_SESSION_WITH_ONE_ENTRY"])
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_type="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 1)

        print("get no session from LE platform")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_LE_FLOW_SESSION_WITH_NO_ENTRY"])
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_type="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 0)

        print("Get FLOW session from LE platform on HA by XML")
        print("checking 1 session in a node")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_LE_FLOW_SESSION_THAT_ONE_ENTRY"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_mode="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 1)
        self.assertEqual(all_session_tuple[0]['re-name'], "node0")

        print("checking 2 sessions in a node")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_LE_FLOW_SESSION_THAT_HAVE_MULTI_SESSIONS"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_type="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 2)
        self.assertEqual(all_session_tuple[0]['re-name'], "node0")
        self.assertEqual(all_session_tuple[0]['session-identifier'], "57")
        self.assertEqual(all_session_tuple[1]['re-name'], "node0")
        self.assertEqual(all_session_tuple[1]['session-identifier'], "2")

        print("checking 3 sessions in both node")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_LE_FLOW_SESSION_THAT_HAVE_MULTI_SESSIONS_ON_BOTH_NODE"],
        )
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_type="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 3)

        print("checking no session shown")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_LE_FLOW_SESSION_EMPTY"])
        all_session_tuple = self.ins.fetch_flow_session(device=mock_device_ins, return_type="session_tuple")
        print(self.tool.pprint(all_session_tuple))
        self.assertTrue(isinstance(all_session_tuple, (list, tuple)))
        self.assertTrue(len(all_session_tuple) == 0)

        print("Get FLOW session from LE platform by TEXT")
        mock_execute_cli_command_on_device.return_value = self.response["le_text"]
        all_session_entry = self.ins.fetch_flow_session(device=mock_device_ins, return_mode="text")
        print(self.tool.pprint(all_session_entry))
        self.assertTrue(isinstance(all_session_entry, str))

        print("Get FLOW session from wrong response")
        print("checking invalid response with no xml structure")
        mock_execute_cli_command_on_device.return_value = "Invalid Response"
        self.assertRaisesRegex(
            TypeError,
            r"missing 1 required positional argument",
            self.ins.fetch_flow_session,
            return_type="session_tuple"
        )

        print("checking invalid response from invalid device response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["INVALID_HE_FLOW_FTP_SESSION"])
        self.assertRaisesRegex(
            TypeError,
            r"",
            self.ins.fetch_flow_session,
            return_type="session_tuple"
        )

        print("checking invalid response with only one node response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_LE_FLOW_SESSION_INVALID_RESPONSE_THAT_ONLY_ONE_NODE_RESPONSE"]
        )
        session_list = self.ins.fetch_flow_session(device=mock_device_ins, return_type="session_tuple")
        print(self.tool.pprint(session_list))
        self.assertTrue(isinstance(session_list, (list, tuple)))

        print("For Ticket-5532 validation")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["TICKET_5532_XML"])
        session_list = self.ins.fetch_flow_session(device=mock_device_ins, return_type="session_tuple")
        print(self.tool.pprint(session_list))
        self.assertTrue(isinstance(session_list, (list, tuple)))
        self.assertTrue(len(session_list[0]["flow-information"]) == 1)

        print("For Ticket-5532 validation flat response")
        session_list = self.ins.fetch_flow_session(device=mock_device_ins, return_mode="flat_dict")
        print(self.tool.pprint(session_list))
        self.assertEqual(len(session_list), 16)
        self.assertTrue("out_destination_address" not in session_list[0])


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_fetch_flow_session_resource_manager(self, mock_send_cli_cmd):
        """Get flow session resource manager"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        xml_dict = self.xml.xml_string_to_dict(self.response["SA_LE_FLOW_SESSION_RESOURCE_MANAGER"])
        print(xml_dict)
        mock_send_cli_cmd.return_value = xml_dict

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_fetch_flow_cp_session(self, mock_send_cli_cmd):
        """Get FLOW CP session entries"""
        mock_device_ins = mock.Mock()

        print("""Get FLOW CP session from HE HA topo""")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_FLOW_CP_SESSION"])
        entry_list = self.ins.fetch_flow_cp_session(device=mock_device_ins, node=0)
        print(self.tool.pprint(entry_list))
        self.assertEqual(entry_list[0]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[0]["displayed_session_count"], "0")
        self.assertEqual(entry_list[0]["re_name"], "node0")
        self.assertEqual(entry_list[1]["dcp_flow_fpc_pic_id"], "on FPC0 PIC1:")
        self.assertEqual(entry_list[2]["dcp_flow_fpc_pic_id"], "on FPC0 PIC2:")
        self.assertEqual(entry_list[3]["dcp_flow_fpc_pic_id"], "on FPC0 PIC3:")
        self.assertEqual(entry_list[4]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[4]["re_name"], "node1")
        self.assertEqual(entry_list[5]["dcp_flow_fpc_pic_id"], "on FPC0 PIC1:")
        self.assertEqual(entry_list[5]["re_name"], "node1")
        self.assertEqual(entry_list[5]["session_identifier"], "10040149")
        self.assertEqual(entry_list[5]["status"], "")
        self.assertEqual(entry_list[5]["session_flag"], "0x180000")
        self.assertEqual(entry_list[5]["policy"], "")
        self.assertEqual(entry_list[5]["nat_source_pool_name"], "")
        self.assertEqual(entry_list[5]["in_source_address"], "0.0.0.0")
        self.assertEqual(entry_list[5]["in_flag"], "0x0")
        self.assertEqual(entry_list[5]["out_source_address"], "121.11.20.2")
        self.assertEqual(entry_list[6]["dcp_flow_fpc_pic_id"], "on FPC0 PIC1:")
        self.assertEqual(entry_list[6]["session_identifier"], "10040150")
        self.assertEqual(entry_list[7]["session_identifier"], "10040151")
        self.assertEqual(entry_list[8]["dcp_flow_fpc_pic_id"], "on FPC0 PIC2:")
        self.assertEqual(entry_list[8]["session_identifier"], "20039231")
        self.assertEqual(entry_list[9]["session_identifier"], "20039232")
        self.assertEqual(entry_list[10]["dcp_flow_fpc_pic_id"], "on FPC0 PIC3:")
        self.assertEqual(entry_list[10]["session_identifier"], "30039283")
        self.assertEqual(entry_list[11]["session_identifier"], "30039284")
        self.assertEqual(entry_list[12]["session_identifier"], "30039285")
        self.assertEqual(entry_list[13]["session_identifier"], "30039286")
        self.assertTrue("in_direction" not in entry_list[4])
        self.assertTrue("out_direction" not in entry_list[4])
        self.assertTrue(len(entry_list) == 14)

        print("""Get FLOW CP session from LE SA topo""")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_FLOW_CP_SESSION_EMPTY"])
        entry_list = self.ins.fetch_flow_cp_session(device=mock_device_ins, more_options="family inet")
        print(self.tool.pprint(entry_list))
        self.assertEqual(entry_list[0]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[0]["displayed_session_count"], "0")
        self.assertEqual(entry_list[1]["dcp_flow_fpc_pic_id"], "on FPC0 PIC1:")
        self.assertEqual(entry_list[2]["dcp_flow_fpc_pic_id"], "on FPC0 PIC2:")
        self.assertEqual(entry_list[3]["dcp_flow_fpc_pic_id"], "on FPC0 PIC3:")
        self.assertTrue("re_name" not in entry_list[0])
        self.assertTrue(len(entry_list) == 4)

        print("""Get invalid FLOW CP session""")
        mock_send_cli_cmd.return_value = False
        entry_list = self.ins.fetch_flow_cp_session(device=mock_device_ins, more_options="family inet")
        self.assertFalse(entry_list)

        print("""Response from only 1 SPU""")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_FLOW_CP_SESSION_WITH_ONE_SPU_AND_ONE_SESSION"])
        entry_list = self.ins.fetch_flow_cp_session(device=mock_device_ins, more_options="family inet")
        print(self.tool.pprint(entry_list))
        self.assertEqual(entry_list[0]["re_name"], "node0")
        self.assertEqual(entry_list[0]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[1]["re_name"], "node1")
        self.assertEqual(entry_list[1]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[2]["re_name"], "node1")
        self.assertEqual(entry_list[2]["dcp_flow_fpc_pic_id"], "on FPC0 PIC1:")
        self.assertEqual(entry_list[2]["in_source_address"], "0.0.0.0")
        self.assertTrue(len(entry_list) == 3)

        print("""session do not have wing info""")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_FLOW_CP_SESSION_FOR_NO_WING"])
        entry_list = self.ins.fetch_flow_cp_session(device=mock_device_ins, more_options="family inet")
        print(self.tool.pprint(entry_list))
        self.assertEqual(entry_list[0]["re_name"], "node0")
        self.assertEqual(entry_list[0]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[1]["re_name"], "node1")
        self.assertEqual(entry_list[1]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[2]["re_name"], "node1")
        self.assertEqual(entry_list[2]["dcp_flow_fpc_pic_id"], "on FPC0 PIC1:")
        self.assertEqual(entry_list[2]["sess_state"], "Valid")
        self.assertTrue(len(entry_list) == 3)

        print("""session only have 1 direction wing""")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_FLOW_CP_SESSION_FOR_ONE_WAY_WING"])
        entry_list = self.ins.fetch_flow_cp_session(device=mock_device_ins, more_options="family inet")
        print(self.tool.pprint(entry_list))
        self.assertEqual(entry_list[0]["re_name"], "node0")
        self.assertEqual(entry_list[0]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[1]["re_name"], "node1")
        self.assertEqual(entry_list[1]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[2]["re_name"], "node1")
        self.assertEqual(entry_list[2]["dcp_flow_fpc_pic_id"], "on FPC0 PIC1:")
        self.assertEqual(entry_list[2]["out_destination_address"], "121.11.15.11")
        self.assertTrue(len(entry_list) == 3)


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_fetch_flow_cp_session_summary(self, mock_send_cli_cmd):
        """Get FLOW CP session entries"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("Get FLOW CP session summary info from HA HE topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_FLOW_CP_SESSION_SUMMARY"])
        entry_list = self.ins.fetch_flow_cp_session_summary(device=mock_device_ins, node="node0", more_options="source_prefix 192.168.10.0/24")
        print(self.tool.pprint(entry_list))
        self.assertEqual(entry_list[0]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[0]["displayed_session_count"], "50")
        self.assertEqual(entry_list[0]["displayed_session_invalidated"], "30")
        self.assertEqual(entry_list[0]["displayed_session_other"], "40")
        self.assertEqual(entry_list[0]["displayed_session_pending"], "20")
        self.assertEqual(entry_list[0]["displayed_session_valid"], "10")
        self.assertEqual(entry_list[0]["re_name"], "node0")
        self.assertEqual(entry_list[1]["dcp_flow_fpc_pic_id"], "on FPC0 PIC1:")
        self.assertEqual(entry_list[2]["dcp_flow_fpc_pic_id"], "on FPC0 PIC2:")
        self.assertEqual(entry_list[2]["max_inet6_session_count"], "7549747")
        self.assertEqual(entry_list[3]["dcp_flow_fpc_pic_id"], "on FPC0 PIC3:")
        self.assertEqual(entry_list[4]["dcp_flow_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(entry_list[4]["re_name"], "node1")
        self.assertEqual(entry_list[5]["displayed_session_count"], "60")
        self.assertEqual(entry_list[5]["displayed_session_invalidated"], "40")
        self.assertEqual(entry_list[5]["displayed_session_other"], "50")
        self.assertEqual(entry_list[5]["displayed_session_pending"], "30")
        self.assertEqual(entry_list[5]["displayed_session_valid"], "20")
        self.assertEqual(entry_list[5]["max_session_count"], "7549747")
        self.assertTrue(len(entry_list) == 8)

        print("Get FLOW CP session summary info from SA HE topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_SA_FLOW_CP_SESSION_SUMMARY"])
        entry_list = self.ins.fetch_flow_cp_session_summary(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 4)

        print("Get FLOW CP session summary info from only one SPU")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_SA_FLOW_CP_SESSION_SUMMARY_ONE_SPU"])
        entry_list = self.ins.fetch_flow_cp_session_summary(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 1)

        print("Get FLOW CP session summary info with invalid response")
        mock_send_cli_cmd.return_value = False
        entry_list = self.ins.fetch_flow_cp_session_summary(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertFalse(entry_list)

        print("Get FLOW CP session summary info from SA HE with root tag")
        mock_send_cli_cmd.return_value = self.response["HE_SA_FLOW_CP_SESSION_SUMMARY_WITH_ROOT_TAG"]
        entry_list = self.ins.fetch_flow_cp_session_summary(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertEqual(entry_list[0]["dcp_flow_fpc_id"], "9")
        self.assertEqual(entry_list[0]["dcp_flow_pic_id"], "0")
        self.assertEqual(entry_list[0]["displayed_session_count"], "50")
        self.assertEqual(entry_list[0]["displayed_session_invalidated"], "30")
        self.assertEqual(entry_list[0]["displayed_session_other"], "40")
        self.assertEqual(entry_list[0]["displayed_session_pending"], "20")
        self.assertEqual(entry_list[0]["displayed_session_valid"], "10")
        self.assertEqual(entry_list[0]["dcp_displayed_session_count"], "50")
        self.assertEqual(entry_list[0]["dcp_displayed_session_invalidated"], "30")
        self.assertEqual(entry_list[0]["dcp_displayed_session_other"], "40")
        self.assertEqual(entry_list[0]["dcp_displayed_session_pending"], "20")
        self.assertEqual(entry_list[0]["dcp_displayed_session_valid"], "10")
        self.assertEqual(entry_list[-1]["dcp_flow_fpc_id"], "9")
        self.assertEqual(entry_list[-1]["dcp_flow_pic_id"], "3")
        self.assertEqual(entry_list[-1]["displayed_session_count"], "1")
        self.assertEqual(entry_list[-1]["displayed_session_invalidated"], "1")
        self.assertEqual(entry_list[-1]["displayed_session_other"], "0")
        self.assertEqual(entry_list[-1]["displayed_session_pending"], "0")
        self.assertEqual(entry_list[-1]["displayed_session_valid"], "0")
        self.assertEqual(entry_list[-1]["dcp_displayed_session_count"], "1")
        self.assertEqual(entry_list[-1]["dcp_displayed_session_invalidated"], "1")
        self.assertEqual(entry_list[-1]["dcp_displayed_session_other"], "0")
        self.assertEqual(entry_list[-1]["dcp_displayed_session_pending"], "0")
        self.assertEqual(entry_list[-1]["dcp_displayed_session_valid"], "0")
        self.assertEqual(entry_list[-1]["max_inet6_session_count"], "7549747")
        self.assertEqual(entry_list[-1]["max_session_count"], "7549747")

        print("Get FLOW CP session summary all FPC counter from HA HE")
        mock_send_cli_cmd.return_value = self.response["HA_HE_FLOW_CP_SESSION_SUMMARY"]
        entry_list = self.ins.fetch_flow_cp_session_summary(device=mock_device_ins, total_all_fpcs="TRUE")
        print(self.tool.pprint(entry_list))
        self.assertTrue(entry_list[0]["re_name"] == "node0")
        self.assertTrue(entry_list[0]["displayed_session_count"] == "200")
        self.assertTrue(entry_list[0]["displayed_session_invalidated"] == "120")
        self.assertTrue(entry_list[0]["displayed_session_other"] == "160")
        self.assertTrue(entry_list[0]["displayed_session_pending"] == "80")
        self.assertTrue(entry_list[0]["displayed_session_valid"] == "40")
        self.assertTrue(entry_list[0]["max_inet6_session_count"] == "22649241")
        self.assertTrue(entry_list[0]["max_session_count"] == "22649241")
        self.assertTrue(entry_list[0]["dcp_flow_fpc_pic_id"] == "on FPC0 PIC3:")
        self.assertTrue(entry_list[1]["re_name"] == "node1")
        self.assertTrue(entry_list[1]["displayed_session_count"] == "240")
        self.assertTrue(entry_list[1]["displayed_session_invalidated"] == "160")
        self.assertTrue(entry_list[1]["displayed_session_other"] == "200")
        self.assertTrue(entry_list[1]["displayed_session_pending"] == "120")
        self.assertTrue(entry_list[1]["displayed_session_valid"] == "80")
        self.assertTrue(entry_list[1]["max_inet6_session_count"] == "22649241")
        self.assertTrue(entry_list[1]["max_session_count"] == "22649241")
        self.assertTrue(entry_list[1]["dcp_flow_fpc_pic_id"] == "on FPC0 PIC3:")
        self.assertTrue(len(entry_list) == 2)

        print("Get FLOW CP session summary all FPC counter from SA HE")
        mock_send_cli_cmd.return_value = self.response["HE_SA_FLOW_CP_SESSION_SUMMARY_WITH_ROOT_TAG"]
        entry_list = self.ins.fetch_flow_cp_session_summary(device=mock_device_ins, total_all_fpcs="TRUE")
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 1)
        self.assertTrue("re_name" not in entry_list[0])
        self.assertTrue(entry_list[0])
        self.assertTrue(entry_list[0]["displayed_session_count"] == "103")
        self.assertTrue(entry_list[0]["displayed_session_invalidated"] == "63")
        self.assertTrue(entry_list[0]["displayed_session_other"] == "80")
        self.assertTrue(entry_list[0]["displayed_session_pending"] == "40")
        self.assertTrue(entry_list[0]["displayed_session_valid"] == "20")
        self.assertTrue(entry_list[0]["dcp_displayed_session_count"] == "103")
        self.assertTrue(entry_list[0]["dcp_displayed_session_invalidated"] == "63")
        self.assertTrue(entry_list[0]["dcp_displayed_session_other"] == "80")
        self.assertTrue(entry_list[0]["dcp_displayed_session_pending"] == "40")
        self.assertTrue(entry_list[0]["dcp_displayed_session_valid"] == "20")
        self.assertTrue(entry_list[0]["max_inet6_session_count"] == "22649241")
        self.assertTrue(entry_list[0]["max_session_count"] == "22649241")
        self.assertTrue(entry_list[0]["dcp_flow_fpc_id"] == "9")
        self.assertTrue(entry_list[0]["dcp_flow_pic_id"] == "3")


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_fetch_flow_statistics(self, mock_send_cli_cmd):
        """Get FLOW statistics info from standalone and highend platform's xml response"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.is_ha.return_value = False

        print("For SA HE platform")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HE_XML_FLOW_STATISTICS_INFO"])
        response = self.ins.fetch_flow_statistics(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertTrue(isinstance(response, dict))
        self.assertTrue("flow-statistics-all" in response)
        self.assertEqual(response["flow-statistics-all"][0]["flow-spu-id"], "of FPC0 PIC1:")
        self.assertEqual(response["flow-statistics-all"][1]["flow-spu-id"], "of FPC0 PIC2:")
        self.assertEqual(response["flow-statistics-all"][2]["flow-spu-id"], "of FPC0 PIC3:")
        self.assertEqual(response["flow-statistics-all"][3]["flow-spu-id"], "Summary:")

        print("For SA HE platform's flat return")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HE_XML_FLOW_STATISTICS_INFO"])
        response = self.ins.fetch_flow_statistics(device=mock_device_ins, return_mode="flat_dict")
        print(self.tool.pprint(response))
        self.assertTrue(isinstance(response, list))
        self.assertEqual(response[0]["flow_spu_id"], "of FPC0 PIC1:")
        self.assertEqual(response[1]["flow_spu_id"], "of FPC0 PIC2:")
        self.assertEqual(response[2]["flow_spu_id"], "of FPC0 PIC3:")
        self.assertEqual(response[3]["flow_spu_id"], "Summary:")
        self.assertTrue("re_name" not in response[0])

        print("For HA LE platform")
        mock_device_ins.is_ha.return_value = True
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_XML_NODE0_FLOW_STATISTICS_INFO"])
        response = self.ins.fetch_flow_statistics(device=mock_device_ins, node=0)
        print(self.tool.pprint(response))
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(response["flow-statistics-all"]["flow-frag-count-fwd"], "0")
        self.assertEqual(response["flow-statistics-all"]["flow-pkt-count-drop"], "705")
        self.assertEqual(response["flow-statistics-all"]["flow-pkt-count-fwd"], "705")
        self.assertEqual(response["flow-statistics-all"]["flow-session-count-valid"], "0")
        self.assertEqual(response["flow-statistics-all"]["tunnel-frag-gen-post"], "0")
        self.assertEqual(response["flow-statistics-all"]["tunnel-frag-gen-pre"], "0")
        self.assertEqual(response["re-name"], "node0")

        print("For HA LE platform only 1 node for flat return")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_XML_NODE0_FLOW_STATISTICS_INFO"])
        response = self.ins.fetch_flow_statistics(device=mock_device_ins, return_mode="Flat_Dict")
        print(self.tool.pprint(response))
        self.assertTrue(isinstance(response, list))
        self.assertEqual(response[-1]["flow_frag_count_fwd"], "0")
        self.assertEqual(response[-1]["flow_pkt_count_drop"], "705")
        self.assertEqual(response[-1]["flow_pkt_count_fwd"], "705")
        self.assertEqual(response[-1]["flow_session_count_valid"], "0")
        self.assertEqual(response[-1]["tunnel_frag_gen_post"], "0")
        self.assertEqual(response[-1]["tunnel_frag_gen_pre"], "0")
        self.assertEqual(response[-1]["re_name"], "node0")

        print("Cannot get statistics result")
        mock_send_cli_cmd.return_value = ""
        response = self.ins.fetch_flow_statistics(device=mock_device_ins)
        self.assertFalse(response)

        print("For HA LE platform 2 nodes for flat return")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_HA_XML_FLOW_STATISTICS_AFTER_RLI36411"])
        response = self.ins.fetch_flow_statistics(device=mock_device_ins, return_mode="Flat_Dict")
        print(self.tool.pprint(response))
        self.assertTrue(isinstance(response, list))
        self.assertEqual(response[0]["re_name"], "node0")
        self.assertEqual(response[0]["flow_frag_count_fwd"], "0")
        self.assertEqual(response[0]["flow_pkt_count_copy"], "0")
        self.assertEqual(response[0]["flow_pkt_count_drop"], "0")
        self.assertEqual(response[0]["flow_pkt_count_fwd"], "0")
        self.assertEqual(response[0]["flow_pkt_count_rx"], "8")
        self.assertEqual(response[0]["flow_pkt_count_tx"], "8")
        self.assertEqual(response[0]["flow_session_count_valid"], "0")
        self.assertEqual(response[0]["tunnel_frag_gen_post"], "0")
        self.assertEqual(response[0]["tunnel_frag_gen_pre"], "0")
        self.assertEqual(response[1]["re_name"], "node1")
        self.assertEqual(response[1]["flow_frag_count_fwd"], "0")
        self.assertEqual(response[1]["flow_pkt_count_copy"], "0")
        self.assertEqual(response[1]["flow_pkt_count_drop"], "1")
        self.assertEqual(response[1]["flow_pkt_count_fwd"], "0")
        self.assertEqual(response[1]["flow_pkt_count_rx"], "1")
        self.assertEqual(response[1]["flow_pkt_count_tx"], "0")
        self.assertEqual(response[1]["flow_session_count_valid"], "0")
        self.assertEqual(response[1]["tunnel_frag_gen_post"], "0")
        self.assertEqual(response[1]["tunnel_frag_gen_pre"], "0")

        print("No response from device")
        mock_send_cli_cmd.return_value = False
        response = self.ins.fetch_flow_statistics(device=mock_device_ins, return_mode="Flat_Dict")
        print(self.tool.pprint(response))
        self.assertFalse(response)

        print("No statistics info in entries")
        entry_list = self.xml.xml_string_to_dict(xml_str=self.response["LE_HA_XML_FLOW_STATISTICS_AFTER_RLI36411"])
        del entry_list["rpc-reply"]["multi-routing-engine-results"]["multi-routing-engine-item"][0]["flow-statistics-all"]
        del entry_list["rpc-reply"]["multi-routing-engine-results"]["multi-routing-engine-item"][1]["flow-statistics-all"]
        mock_send_cli_cmd.return_value = entry_list
        response = self.ins.fetch_flow_statistics(device=mock_device_ins, return_mode="Flat_Dict")
        print(self.tool.pprint(response))
        self.assertEqual(response[0]["re_name"], "node0")
        self.assertEqual(response[1]["re_name"], "node1")


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_fetch_flow_gate(self, mock_execute_cli_command_on_device):
        """Get FLOW gate info"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("For HA LE normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_GATE_HA_LE"])
        response = self.ins.fetch_flow_gate(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertEqual(response[0]["re-name"], "node0")
        self.assertEqual(response[1]["re-name"], "node1")
        self.assertEqual(response[0]["flow-gate-information"]["displayed-gate-count"], "0")
        self.assertEqual(response[0]["flow-gate-information"]["displayed-gate-invalidated"], "0")
        self.assertEqual(response[0]["flow-gate-information"]["displayed-gate-other"], "0")
        self.assertEqual(response[0]["flow-gate-information"]["displayed-gate-pending"], "0")
        self.assertEqual(response[0]["flow-gate-information"]["displayed-gate-valid"], "0")

        print("For HA LE flat dict response")
        response = self.ins.fetch_flow_gate(device=mock_device_ins, return_mode="Flat_Dict")
        print(self.tool.pprint(response))
        self.assertEqual(response[1]["re_name"], "node1")
        self.assertEqual(response[0]["re_name"], "node0")
        self.assertEqual(response[0]["displayed_gate_count"], "0")
        self.assertEqual(response[0]["displayed_gate_invalidated"], "0")
        self.assertEqual(response[0]["displayed_gate_other"], "0")
        self.assertEqual(response[0]["displayed_gate_pending"], "0")
        self.assertEqual(response[0]["displayed_gate_valid"], "0")

        print("For HA HE normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_GATE_HA_HE"])
        response = self.ins.fetch_flow_gate(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertEqual(response[0]["re-name"], "node0")
        self.assertEqual(response[1]["re-name"], "node1")
        self.assertEqual(response[0]["flow-gate-information"][0]["displayed-gate-count"], "0")
        self.assertEqual(response[0]["flow-gate-information"][0]["displayed-gate-invalidated"], "0")
        self.assertEqual(response[0]["flow-gate-information"][0]["displayed-gate-other"], "0")
        self.assertEqual(response[0]["flow-gate-information"][0]["displayed-gate-pending"], "0")
        self.assertEqual(response[0]["flow-gate-information"][0]["displayed-gate-valid"], "0")
        self.assertEqual(response[0]["flow-gate-information"][0]["flow-gate-fpc-pic-id"], "on FPC2 PIC0:")
        self.assertEqual(response[0]["flow-gate-information"][1]["flow-gate-fpc-pic-id"], "on FPC2 PIC1:")
        self.assertEqual(response[0]["flow-gate-information"][2]["flow-gate-fpc-pic-id"], "on FPC5 PIC0:")
        self.assertEqual(response[0]["flow-gate-information"][3]["flow-gate-fpc-pic-id"], "on FPC5 PIC1:")
        self.assertEqual(response[0]["flow-gate-information"][4]["flow-gate-fpc-pic-id"], "on FPC5 PIC2:")
        self.assertEqual(response[0]["flow-gate-information"][5]["flow-gate-fpc-pic-id"], "on FPC5 PIC3:")

        print("For HA HE flat dict response")
        response = self.ins.fetch_flow_gate(device=mock_device_ins, return_mode="FLAT_DICT")
        print(self.tool.pprint(response))
        self.assertEqual(response[0]["re_name"], "node0")
        self.assertEqual(response[0]["displayed_gate_count"], "0")
        self.assertEqual(response[0]["displayed_gate_invalidated"], "0")
        self.assertEqual(response[0]["displayed_gate_other"], "0")
        self.assertEqual(response[0]["displayed_gate_pending"], "0")
        self.assertEqual(response[0]["displayed_gate_valid"], "0")
        self.assertEqual(response[0]["flow_gate_fpc_pic_id"], "on FPC2 PIC0:")
        self.assertEqual(response[1]["flow_gate_fpc_pic_id"], "on FPC2 PIC1:")
        self.assertEqual(response[2]["flow_gate_fpc_pic_id"], "on FPC5 PIC0:")
        self.assertEqual(response[3]["flow_gate_fpc_pic_id"], "on FPC5 PIC1:")
        self.assertEqual(response[4]["flow_gate_fpc_pic_id"], "on FPC5 PIC2:")
        self.assertEqual(response[5]["flow_gate_fpc_pic_id"], "on FPC5 PIC3:")
        self.assertEqual(response[6]["re_name"], "node1")
        self.assertEqual(len(response), 12)

        print("For SA LE normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_GATE_SA_LE"])
        response = self.ins.fetch_flow_gate(device=mock_device_ins, more_options="destination-port 22")
        print(self.tool.pprint(response))
        self.assertEqual(response["flow-gate-information"]["displayed-gate-count"], "0")
        self.assertEqual(response["flow-gate-information"]["displayed-gate-invalidated"], "0")
        self.assertEqual(response["flow-gate-information"]["displayed-gate-other"], "0")
        self.assertEqual(response["flow-gate-information"]["displayed-gate-pending"], "0")
        self.assertEqual(response["flow-gate-information"]["displayed-gate-valid"], "0")
        self.assertTrue("re-name" not in response)

        print("For SA LE flat dict response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_GATE_SA_LE"])
        response = self.ins.fetch_flow_gate(device=mock_device_ins, return_mode="FLAT_DICT")
        print(self.tool.pprint(response))
        self.assertEqual(response[0]["displayed_gate_count"], "0")
        self.assertEqual(response[0]["displayed_gate_invalidated"], "0")
        self.assertEqual(response[0]["displayed_gate_other"], "0")
        self.assertEqual(response[0]["displayed_gate_pending"], "0")
        self.assertEqual(response[0]["displayed_gate_valid"], "0")
        self.assertTrue("re-name" not in response)

        print("For SA HE normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_GATE_SA_HE"])
        response = self.ins.fetch_flow_gate(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertEqual(response["flow-gate-information"][0]["displayed-gate-count"], "0")
        self.assertEqual(response["flow-gate-information"][0]["displayed-gate-invalidated"], "0")
        self.assertEqual(response["flow-gate-information"][0]["displayed-gate-other"], "0")
        self.assertEqual(response["flow-gate-information"][0]["displayed-gate-pending"], "0")
        self.assertEqual(response["flow-gate-information"][0]["displayed-gate-valid"], "0")
        self.assertEqual(response["flow-gate-information"][0]["flow-gate-fpc-pic-id"], "on FPC0 PIC0:")
        self.assertEqual(response["flow-gate-information"][1]["flow-gate-fpc-pic-id"], "on FPC0 PIC1:")
        self.assertTrue("re-name" not in response)

        print("For SA HE flat dict response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_GATE_SA_HE"])
        response = self.ins.fetch_flow_gate(device=mock_device_ins, return_mode="FLAT_DICT")
        print(self.tool.pprint(response))
        self.assertEqual(response[0]["displayed_gate_count"], "0")
        self.assertEqual(response[0]["displayed_gate_invalidated"], "0")
        self.assertEqual(response[0]["displayed_gate_other"], "0")
        self.assertEqual(response[0]["displayed_gate_pending"], "0")
        self.assertEqual(response[0]["displayed_gate_valid"], "0")
        self.assertEqual(response[0]["flow_gate_fpc_pic_id"], "on FPC0 PIC0:")
        self.assertEqual(response[1]["flow_gate_fpc_pic_id"], "on FPC0 PIC1:")
        self.assertTrue("re_name" not in response)

        print("No xml response from device")
        mock_execute_cli_command_on_device.return_value = False
        response = self.ins.fetch_flow_gate(device=mock_device_ins, node="node0")
        self.assertFalse(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_fetch_flow_session_summary(self, mock_send_cli_cmd):
        """test get flow session summary"""
        mock_device_ins = mock.Mock()

        print("Get flow session summary info from HE HA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_HE_FLOW_SESSION_SUMMARY"])
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, node=0)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 6)
        self.assertTrue(entry_list[0]["re_name"] == "node0")
        self.assertTrue(entry_list[0]["max_sessions"] == "6291456")
        self.assertTrue(entry_list[1]["re_name"] == "node0")
        self.assertTrue(entry_list[2]["re_name"] == "node0")
        self.assertTrue(entry_list[3]["re_name"] == "node1")
        self.assertTrue(entry_list[3]["active_sessions"] == "1")
        self.assertTrue(entry_list[4]["active_session_invalidated"] == "1")
        self.assertTrue(entry_list[4]["active_sessions"] == "3")
        self.assertTrue(entry_list[4]["re_name"] == "node1")
        self.assertTrue(entry_list[5]["re_name"] == "node1")
        self.assertTrue(entry_list[5]["active_sessions"] == "4")

        print("Get flow session summary info from LE SA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_LE_FLOW_SESSION_SUMMARY"])
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue("re_name" not in entry_list[0])
        self.assertTrue(entry_list[0]["active_multicast_sessions"] == "0")
        self.assertTrue(entry_list[0]["active_session_invalidated"] == "2")
        self.assertTrue(entry_list[0]["active_session_other"] == "0")
        self.assertTrue(entry_list[0]["active_session_pending"] == "0")
        self.assertTrue(entry_list[0]["active_session_valid"] == "4")
        self.assertTrue(entry_list[0]["active_sessions"] == "6")
        self.assertTrue(entry_list[0]["active_unicast_sessions"] == "4")
        self.assertTrue(entry_list[0]["failed_sessions"] == "0")
        self.assertTrue(entry_list[0]["max_sessions"] == "524288")

        print("Cannot get flow session summary info")
        mock_send_cli_cmd.return_value = False
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins)
        self.assertFalse(entry_list)

        print("get flow session summary but no flow-session-information")
        mock_send_cli_cmd.return_value = self.response["FLOW_SESSION_SUMMARY_WITH_NO_INFORMATION"]
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins)
        self.assertTrue(len(entry_list) == 0)

        print("Get FLOW session summary with more options from HA LE platform")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_LE_FLOW_SESSION_SUMMARY_WITH_MORE_OPTIONS"])
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, more_options="destination-port 63 interface reth1.0")
        print(self.tool.pprint(entry_list))
        self.assertTrue(entry_list[0]["displayed_session_count"], "0")
        self.assertTrue(entry_list[0]["displayed_session_invalidated"], "0")
        self.assertTrue(entry_list[0]["displayed_session_other"], "0")
        self.assertTrue(entry_list[0]["displayed_session_pending"], "0")
        self.assertTrue(entry_list[0]["displayed_session_valid"], "0")
        self.assertTrue(entry_list[0]["re_name"], "node0")
        self.assertTrue(entry_list[1]["displayed_session_count"], "0")
        self.assertTrue(entry_list[1]["displayed_session_invalidated"], "0")
        self.assertTrue(entry_list[1]["displayed_session_other"], "0")
        self.assertTrue(entry_list[1]["displayed_session_pending"], "0")
        self.assertTrue(entry_list[1]["displayed_session_valid"], "0")
        self.assertTrue(entry_list[1]["re_name"], "node1")

        print("Get FLOW session summary with more options from SA HE platform")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_HE_FLOW_SESSION_SUMMARY_WITH_MORE_OPTIONS"])
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, more_options="protocol icmp")
        print(self.tool.pprint(entry_list))
        self.assertTrue(entry_list[0]["flow_fpc_pic_id"] == "on FPC6 PIC1:")
        self.assertTrue(entry_list[1]["flow_fpc_pic_id"] == "on FPC6 PIC2:")
        self.assertTrue(entry_list[2]["flow_fpc_pic_id"] == "on FPC6 PIC3:")

        print("Get FLOW session summary from SA HE for root tag")
        mock_send_cli_cmd.return_value = self.response["SA_HE_FLOW_SESSION_SUMMARY_FOR_ROOT_TAG"]
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, more_options=None)
        print(self.tool.pprint(entry_list))
        self.assertTrue(entry_list[0]["flow_fpc_id"] == "9")
        self.assertTrue(entry_list[0]["flow_pic_id"] == "1")
        self.assertTrue(entry_list[0]["active_sessions"] == "1")
        self.assertTrue(entry_list[1]["flow_fpc_id"] == "9")
        self.assertTrue(entry_list[1]["flow_pic_id"] == "2")
        self.assertTrue(entry_list[1]["active_sessions"] == "2")
        self.assertTrue(entry_list[2]["flow_fpc_id"] == "9")
        self.assertTrue(entry_list[2]["flow_pic_id"] == "3")
        self.assertTrue(entry_list[2]["active_sessions"] == "3")

        print("Get FLOW session summary from HA LE for root tag")
        mock_send_cli_cmd.return_value = self.response["HA_LE_FLOW_SESSION_SUMMARY_FOR_ROOT_TAG"]
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, more_options=None)
        print(self.tool.pprint(entry_list))
        self.assertTrue(entry_list[0]["re_name"] == "node0")
        self.assertTrue(entry_list[0]["max_sessions"] == "4194304")
        self.assertTrue(entry_list[0]["active_sessions"] == "0")
        self.assertTrue(entry_list[1]["re_name"] == "node1")
        self.assertTrue(entry_list[1]["active_sessions"] == "1")
        self.assertTrue(entry_list[1]["active_session_invalidated"] == "1")
        self.assertTrue("flow_fpc_id" not in entry_list[0])
        self.assertTrue("flow_fpc_id" not in entry_list[1])
        self.assertTrue("flow_pic_id" not in entry_list[0])
        self.assertTrue("flow_pic_id" not in entry_list[1])

        print("Get FLOW session summary from SA HE for ROOT TAG")
        mock_send_cli_cmd.return_value = self.response["SA_HE_FLOW_SESSION_SUMMARY_WITH_ROOT_TAG"]
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(entry_list[0]["active_multicast_sessions"] == "0")
        self.assertTrue(entry_list[0]["active_session_invalidated"] == "0")
        self.assertTrue(entry_list[0]["active_session_other"] == "0")
        self.assertTrue(entry_list[0]["active_session_pending"] == "0")
        self.assertTrue(entry_list[0]["active_session_valid"] == "519192")
        self.assertTrue(entry_list[0]["active_sessions"] == "519192")
        self.assertTrue(entry_list[0]["active_unicast_sessions"] == "519192")
        self.assertTrue(entry_list[0]["failed_sessions"] == "0")
        self.assertTrue(entry_list[0]["max_sessions"] == "524288")

        print("Get flow session summary info from HE HA topo for total_all_fpcs")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_HE_FLOW_SESSION_SUMMARY"])
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, total_all_fpcs=True)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 2)
        self.assertTrue(entry_list[0]["re_name"] == "node0")
        self.assertTrue(entry_list[0]["active_multicast_sessions"] == "0")
        self.assertTrue(entry_list[0]["active_services_offload_sessions"] == "0")
        self.assertTrue(entry_list[0]["active_session_invalidated"] == "0")
        self.assertTrue(entry_list[0]["active_session_other"] == "0")
        self.assertTrue(entry_list[0]["active_session_pending"] == "0")
        self.assertTrue(entry_list[0]["active_session_valid"] == "0")
        self.assertTrue(entry_list[0]["active_sessions"] == "0")
        self.assertTrue(entry_list[0]["active_unicast_sessions"] == "0")
        self.assertTrue(entry_list[0]["failed_sessions"] == "0")
        self.assertTrue(entry_list[0]["max_sessions"] == "18874368")
        self.assertTrue(entry_list[1]["re_name"] == "node1")
        self.assertTrue(entry_list[1]["active_multicast_sessions"] == "0")
        self.assertTrue(entry_list[1]["active_services_offload_sessions"] == "0")
        self.assertTrue(entry_list[1]["active_session_invalidated"] == "4")
        self.assertTrue(entry_list[1]["active_session_other"] == "0")
        self.assertTrue(entry_list[1]["active_session_pending"] == "0")
        self.assertTrue(entry_list[1]["active_session_valid"] == "4")
        self.assertTrue(entry_list[1]["active_sessions"] == "8")
        self.assertTrue(entry_list[1]["active_unicast_sessions"] == "4")
        self.assertTrue(entry_list[1]["failed_sessions"] == "0")
        self.assertTrue(entry_list[1]["max_sessions"] == "18874368")

        print("Get flow session summary info from LE SA topo with total_all_fpcs")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_LE_FLOW_SESSION_SUMMARY"])
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, total_all_fpcs="TRUE")
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 1)
        self.assertTrue("re_name" not in entry_list[0])
        self.assertTrue(entry_list[0]["active_multicast_sessions"] == "0")
        self.assertTrue(entry_list[0]["active_session_invalidated"] == "2")
        self.assertTrue(entry_list[0]["active_session_other"] == "0")
        self.assertTrue(entry_list[0]["active_session_pending"] == "0")
        self.assertTrue(entry_list[0]["active_session_valid"] == "4")
        self.assertTrue(entry_list[0]["active_sessions"] == "6")
        self.assertTrue(entry_list[0]["active_unicast_sessions"] == "4")
        self.assertTrue(entry_list[0]["failed_sessions"] == "0")
        self.assertTrue(entry_list[0]["max_sessions"] == "524288")

        print("Get FLOW session summary from SA HE for ROOT TAG with total_all_fpcs")
        mock_send_cli_cmd.return_value = self.response["SA_HE_FLOW_SESSION_SUMMARY_WITH_ROOT_TAG"]
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, total_all_fpcs=True)
        print(self.tool.pprint(entry_list))
        self.assertTrue(entry_list[0]["active_multicast_sessions"] == "0")
        self.assertTrue(entry_list[0]["active_session_invalidated"] == "0")
        self.assertTrue(entry_list[0]["active_session_other"] == "0")
        self.assertTrue(entry_list[0]["active_session_pending"] == "0")
        self.assertTrue(entry_list[0]["active_session_valid"] == "519192")
        self.assertTrue(entry_list[0]["active_sessions"] == "519192")
        self.assertTrue(entry_list[0]["active_unicast_sessions"] == "519192")
        self.assertTrue(entry_list[0]["failed_sessions"] == "0")
        self.assertTrue(entry_list[0]["max_sessions"] == "524288")

        print("Get FLOW session summary from SA HE for ROOT TAG and more_options")
        mock_send_cli_cmd.return_value = self.response["SA_HE_FLOW_SESSION_SUMMARY_WITH_MORE_OPTION_FOR_ROOT_TAG"]
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, more_options="protocol udp")
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 7)
        self.assertTrue(entry_list[0]["flow_fpc_id"] == "6")
        self.assertTrue(entry_list[0]["flow_pic_id"] == "1")
        self.assertTrue(entry_list[1]["flow_pic_id"] == "2")
        self.assertTrue(entry_list[2]["flow_pic_id"] == "3")

        print("Get FLOW session summary from SA HE for ROOT TAG and more_options with total_all_fpcs")
        mock_send_cli_cmd.return_value = self.response["SA_HE_FLOW_SESSION_SUMMARY_WITH_MORE_OPTION_FOR_ROOT_TAG"]
        entry_list = self.ins.fetch_flow_session_summary(device=mock_device_ins, more_options="protocol udp", total_all_fpcs=True)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 1)
        self.assertTrue(entry_list[0]["flow_fpc_id"] == "7")
        self.assertTrue(entry_list[0]["flow_pic_id"] == "3")
        self.assertTrue(entry_list[0]["dcp_displayed_session_count"] == "2")
        self.assertTrue(entry_list[0]["dcp_displayed_session_invalidated"] == "0")
        self.assertTrue(entry_list[0]["dcp_displayed_session_valid"] == "2")
        self.assertTrue(entry_list[0]["displayed_session_count"] == "2")
        self.assertTrue(entry_list[0]["displayed_session_invalidated"] == "0")
        self.assertTrue(entry_list[0]["displayed_session_valid"] == "2")


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_verify_flow_session(self, mock_execute_cli_command_on_device):
        """search flow session from HE platform's xml response"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("search flow session from HE SA Platform")
        print("checking IPv6 FTP control session from SA HE platform")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_MULTI_FPC"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="2000:0100::2 eq",
            in_dst_addr="2000:200::2 eq",
            in_dst_port="2121 eq",
            in_protocol="tcp",
            out_src_addr="2000:0200::2 eq",
            out_dst_addr="2000:100::2 eq",
        )
        self.assertTrue(result)

        print("checking session from specific PIC on SA HE platform")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_MULTI_FPC"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="2000:0100::2 eq",
            in_dst_addr="2000:200::2 eq",
            flow_fpc_pic_id=("PIC2", "contain"),
            in_protocol="tcp",
            out_src_addr="2000:0200::2 eq",
            out_dst_addr="2000:100::2 eq",
        )
        self.assertTrue(result)

        print("search session in specific SPU for IPv4 ICMP")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HE_FLOW_ALL_ICMP_SESSION_IN_ONE_SPU"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            flow_fpc_pic_id="FPC0 PIC1 in",
            in_src_addr="192.168.100.0/24 in",
            in_dst_addr="192.168.200.0/24 in",
            in_protocol="icmp exact",
            return_mode="counter",
        )
        self.assertTrue(result >= 2)

        print("search session by IP range")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HE_FLOW_ALL_ICMP_SESSION_IN_ONE_SPU"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.1 - 192.168.100.254 in",
            in_dst_addr="192.168.200.1-192.168.200.254 in",
            in_protocol="icmp exact",
            return_mode="counter",
        )
        self.assertTrue(result >= 2)

        print("search session by IP range; and have match_from_previous_response but previous session not existing")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HE_FLOW_ALL_ICMP_SESSION_IN_ONE_SPU"],
        )
        self.ins.runtime[str(mock_device_ins)]["flow_session_list"] = self.ins.fetch_flow_session(device=mock_device_ins, return_mode="flat_dict")
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.1 - 192.168.100.254 in",
            in_dst_addr="192.168.200.1~192.168.200.254 in",
            in_protocol="icmp exact",
            return_mode="counter",
            match_from_previous_response=True,
        )
        self.assertTrue(result >= 2)

        print("search session by IP range; and have match_from_previous_response, and previous session already existing")
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.1 ~ 192.168.100.254 in",
            in_dst_addr="192.168.200.1-192.168.200.254 in",
            in_protocol="icmp exact",
            return_mode="counter",
            match_from_previous_response=True,
        )
        self.assertTrue(result >= 2)

        print("checking cannot match session")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_MULTI_FPC"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="2000:0100::2 eq",
            in_dst_addr="2000:200::2 eq",
            flow_fpc_pic_id=("PIC2", "contain"),
            in_protocol="udp",
            out_src_addr="2000:0200::2 eq",
            out_dst_addr="2000:100::2 eq",
        )
        self.assertFalse(result)

        print("checking user issue")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["verify_flow_session_USER_CASE_1"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="15.15.15.1 eq",
            in_dst_addr="14.14.14.1 eq",
            in_protocol="tcp eq",
            in_dst_port="23 eq",
            in_interface="ge-0/0/1.0 eq",
            out_src_addr="14.14.14.1 eq",
            out_protocol="tcp eq",
            out_src_port="23 eq",
            out_dst_addr="15.15.15.1 eq",
            out_interface="ge-0/0/0.0 eq",
            # policy="GROUP_IKE_ID_VPN_POL/4 eq",
        )
        self.assertTrue(result)

        print("checking address in behavioor")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["FLOW_SESSION_FOR_ADDRESS_IN_BEHAVIOR"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="100.0.0.2",
            in_dst_addr="100.0.1.2",
            out_src_addr="100.0.1.2",
            out_dst_addr="30.0.1.1-30.0.1.2 contain",
        )
        self.assertTrue(result)

        print("Fix session-identifer error")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["FLOW_SESSION_FOR_ADDRESS_IN_BEHAVIOR"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="100.0.0.2",
            in_dst_addr="100.0.1.2",
            out_src_addr="100.0.1.2",
            out_dst_addr="30.0.1.1-30.0.1.2 contain",
            session_identifier=20001048,
        )
        self.assertTrue(result)

        print("search flow session from HE HA platform")
        print("checking match session from specific pic")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC_BOTH_2_NODE"]
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            flow_fpc_pic_id="FPC0 PIC1 in",
            in_src_addr="192.168.100.0/24 in",
            in_dst_addr="192.168.200.0/24 in",
            out_src_port=2121,
            node=1,
            in_protocol="tcp exact",
            return_mode="counter",
        )
        self.assertTrue(result == 1)

        print("checking match session from specific node")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC_BOTH_2_NODE"]
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.0/24 in",
            in_dst_addr="192.168.200.0/24 in",
            out_src_port=2121,
            node="node0",
            in_protocol="tcp exact",
            return_mode="counter",
        )
        self.assertTrue(result == 1)

        print("checking match session from specific node and IP range")
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.1 - 192.168.100.254 in",
            in_dst_addr="192.168.200.1 - 192.168.200.254 in",
            out_src_port=2121,
            node="node0",
            in_protocol="tcp exact",
            return_mode="counter",
        )
        self.assertTrue(result == 1)

        print("checking match session with option value is None")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC_BOTH_2_NODE"]
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.0/24 in",
            in_dst_addr="192.168.200.0/24 in",
            out_src_port=None,
            node=None,
            in_protocol="tcp exact",
        )
        self.assertTrue(result)

        print("checking no match session with bool return")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC_BOTH_2_NODE"]
        )
        self.assertRaisesRegex(
            ValueError,
            r"'node' must be 0, '0', node0, 1, '1' or node1",
            self.ins.verify_flow_session,
            device=mock_device_ins,
            in_src_addr="192.168.100.0/24 in",
            in_dst_addr="192.168.200.0/24 in",
            out_src_port=2121,
            node="node3",               # <==== not match
            in_protocol="tcp exact",
        )

        print("checking ISSU processing response that only from single node")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_SESSION_FROM_SINGLE_NODE"])
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.0/24 in",
            in_dst_addr="192.168.200.0/24 in",
            out_src_port=30556,
            in_protocol="icmp exact",
            node="node1",
        )
        self.assertTrue(result)

        print("checking match session by port range")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_THAT_ONE_ENTRY_IN_ONE_FPC_BOTH_2_NODE"]
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.0/24 in",
            in_dst_addr="192.168.200.0/24 in",
            in_src_port="1025-65535 in",
            in_dst_port=2121,
            out_src_port=2121,
            out_dst_port="1025-65535 in",
            in_protocol="tcp exact",
            return_mode="counter",
        )
        self.assertTrue(result == 2)

        print("match ALG related session")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_HAVE_ALG_ELEMENT"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.0/24 in",
            in_dst_addr="192.168.200.0/24 in",
            in_src_port="1025-65535 in",
            session_timeout="300-1800 in",
            out_dst_port="1025-65535 in",
            resource_manager_client_name="FTP in",
            resource_manager_group_identifier=1,
            resource_manager_resource_identifier=0,
            return_mode="counter",
        )
        self.assertTrue(result == 3)

        print("checking more_show_options and more_options")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["HA_HE_FLOW_SESSION_HAVE_ALG_ELEMENT"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.100.0/24 in",
            in_dst_addr="192.168.200.0/24 in",
            in_src_port="1025-65535 in",
            session_timeout="300-1800 in",
            out_dst_port="1025-65535 in",
            resource_manager_client_name="FTP in",
            resource_manager_group_identifier=1,
            resource_manager_resource_identifier=0,
            return_mode="counter",
            more_options="summary",
            more_show_options="more_options",
        )
        self.assertEqual(result, 3)

        print("search flow session from LE SA platfrom")
        print("checking match session with bool return")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_LE_FLOW_SESSION_WITH_MULTI_ENTRY"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="100.1.0.2",
            in_dst_addr="100.2.0.2",
            in_protocol="icmp",
            in_pkt_cnt=(1, "less_or_equal_than"),
            in_byte_cnt=(60, "gt"),
            out_src_addr="100.1.0.2   not_equal",
            out_dst_addr=("100.1.0.2", "in"),
            out_protocol="icmp",
            out_pkt_cnt="100 ne",
            out_byte_cnt=(1000, "less_than"),
        )
        self.assertTrue(result)

        print("checking match session with counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_LE_FLOW_SESSION_WITH_MULTI_ENTRY"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="100.1.0.2",
            in_dst_addr="100.2.0.2",
            in_protocol="icmp",
            in_pkt_cnt=(1, "less_or_equal_than"),
            in_byte_cnt=(60, "gt"),
            out_src_addr="100.1.0.2   not_equal",
            out_dst_addr=("100.1.0.2", "in"),
            out_protocol="icmp",
            out_pkt_cnt="100 ne",
            out_byte_cnt=(1000, "less_than"),

            return_mode="counter",
        )
        self.assertTrue(result == 4)

        print("checking match session with IP range and get match counter")
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="100.1.0.1 - 100.1.0.10 in",
            in_dst_addr="100.2.0.1 - 100.2.0.10 in",
            in_protocol="icmp",
            in_pkt_cnt=(1, "less_or_equal_than"),
            in_byte_cnt=(60, "gt"),
            out_src_addr="100.1.0.2   not_equal",
            out_dst_addr=("100.1.0.2", "in"),
            out_protocol="icmp",
            out_pkt_cnt="100 ne",
            out_byte_cnt=(1000, "less_than"),
            return_mode="counter",
        )
        self.assertTrue(result == 4)

        print("checking match session with no match")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_LE_FLOW_SESSION_WITH_MULTI_ENTRY"],
        )
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="100.1.0.2",
            in_dst_addr="100.2.0.2",
            in_protocol="icmp",
            in_pkt_cnt=(1, "less_or_equal_than"),
            in_byte_cnt=(60, "gt"),
            out_src_addr="100.1.0.2   not_equal",
            out_dst_addr=("100.1.0.2", "in"),
            out_protocol="tcp",         # not match
            out_pkt_cnt="100 ne",
            out_byte_cnt=(1000, "less_than"),
            return_mode="counter",
        )
        self.assertTrue(result == 0)

        print("search flow session with invalid option")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_LE_FLOW_SESSION_WITH_MULTI_ENTRY"],
        )
        self.assertRaisesRegex(
            TypeError,
            r"must be STR, INT, FLOAT, LIST, TUPLE or None",
            self.ins.verify_flow_session,
            device=mock_device_ins, in_src_addr=dict(),
        )

        print("search flow session extra for code coverage")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            xml_str=self.response["SA_HE_FLOW_SESSION_THAT_MULTI_ENTRY_IN_MULTI_FPC"],
        )
        ip_check_material_list = (
            ("2000:100::2", "ne"),
            ("100.1.2.0/24", "in"),
        )
        for item in ip_check_material_list:
            result = self.ins.verify_flow_session(
                device=mock_device_ins,
                in_src_addr=item,
            )
            self.assertFalse(result)

        print("checking string...")
        string_check_material_list = (
            ("igmp", "contain"),
            ("igmp", "exact"),
        )
        for item in string_check_material_list:
            result = self.ins.verify_flow_session(
                device=mock_device_ins,
                in_protocol=item,
            )
            self.assertFalse(result)

        print("checking more options...")
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            node=0,
            application="ftp",
            session_id=806573,
            logical_system="LSYS1",
            more_show_option="more option",
            in_protocol="igmp eq",
        )
        self.assertFalse(result)

        print("For TOBY Ticket-5532")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["TICKET_5532_XML"])
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="14.14.14.1 eq",
            in_dst_addr="14.14.14.2 eq",
            in_dst_port="36050 eq",
            in_protocol="udp",
            in_pkt_cnt="50 gt",
            out_pkt_cnt="50 gt",
            out_interface="gr-0/0/0.1",
            options="| no-more",
            session_id=48,
        )

        self.assertTrue(result)

        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(xml_str=self.response["TICKET_5532_XML_1"])
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr=" 3ffd::2 eq",
            in_dst_addr="7ffd::2 eq",
            in_protocol="tcp",
            out_src_addr="7ffd::2 eq",
            out_dst_addr="3ffd::2 eq",
            in_interface="ge-0/0/1.0",
            out_interface="gr-0/0/0.0",
        )

        self.assertTrue(result)

        print("Number element have STRINT value on device")
        mock_execute_cli_command_on_device.return_value = self.response["FLOW_SESSION_WITH_NA_TIMEOUT"]
        result = self.ins.verify_flow_session(
            device=mock_device_ins,
            in_src_addr="192.168.255.1",
            timeout="10 ge",
            return_mode="counter",
        )
        self.assertTrue(result == 1)


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_verify_flow_cp_session(self, mock_send_cli_cmd):
        """checking search flow cp session"""
        mock_device_ins = mock.Mock()

        print("search flow cp session from HE HA topo for bool")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_FLOW_CP_SESSION"])
        status = self.ins.verify_flow_cp_session(
            device=mock_device_ins,
            dcp_flow_fpc_pic_id="FPC0 PIC0",
            displayed_session_count=0,
        )
        self.assertTrue(status)

        print("search flow cp session from HE HA topo for counter")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_FLOW_CP_SESSION"])
        counter = self.ins.verify_flow_cp_session(
            device=mock_device_ins,
            return_mode="counter",
            session_spu_id="1-3 in",
            in_source_address="121.11.10.0/24 in",
            sess_state="Valid eq",
            node=1,
        )
        self.assertTrue(counter == 4)

        print("search flow cp session from LE SA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_FLOW_CP_SESSION_EMPTY"])
        counter = self.ins.verify_flow_cp_session(
            device=mock_device_ins,
            return_mode="counter",
            session_spu_id="1-3 in",
            in_source_address="121.11.10.0/24 in",
            sess_state="Valid eq",
        )
        self.assertTrue(counter == 0)

        print("search flow cp session have unsupported option")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_FLOW_CP_SESSION_EMPTY"])
        counter = self.ins.verify_flow_cp_session(
            device=mock_device_ins,
            return_mode="counter",
            session_spu_id="1-3 in",
            in_source_address="121.11.10.0/24 in",
            sess_state="Valid eq",
            unsupported_option="Unknown",
        )
        self.assertFalse(counter)

        print("match from previous result")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_FLOW_CP_SESSION"])
        self.ins.runtime[str(mock_device_ins)]["flow_cp_session_list"] = self.ins.fetch_flow_cp_session(device=mock_device_ins)
        counter = self.ins.verify_flow_cp_session(
            device=mock_device_ins,
            return_mode="counter",
            session_spu_id="1-3 in",
            in_source_address="121.11.10.0/24 in",
            sess_state="Valid eq",
            match_from_previous_response=True,
        )
        self.assertTrue(counter == 4)

        print("cannot get flow cp session from device")
        mock_send_cli_cmd.return_value = False
        self.ins.runtime[str(mock_device_ins)]["flow_cp_session_list"] = self.ins.fetch_flow_cp_session(device=mock_device_ins)
        counter = self.ins.verify_flow_cp_session(
            device=mock_device_ins,
            return_mode="counter",
            session_spu_id="1-3 in",
            in_source_address="121.11.10.0/24 in",
            sess_state="Valid eq",
            match_from_previous_response=True,
        )
        self.assertTrue(counter == 0)


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_verify_flow_cp_session_summary(self, mock_send_cli_cmd):
        """checking search flow cp session summary"""
        mock_device_ins = mock.Mock()

        print("search flow cp session summary from HE HA topo for bool")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_FLOW_CP_SESSION_SUMMARY"])
        status = self.ins.verify_flow_cp_session_summary(
            device=mock_device_ins,
            more_options="source-prefix 10.208.10.0/24",
            node=1,
            dcp_flow_fpc_pic_id="FPC0 PIC0",
            displayed_session_count=60,
            displayed_session_valid=("0-50", "in")
        )
        self.assertTrue(status)

        print("search flow cp session summary from HE SA topo for counter")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_SA_FLOW_CP_SESSION_SUMMARY"])
        cnt = self.ins.verify_flow_cp_session_summary(
            device=mock_device_ins,
            return_mode="counter",
            total_all_fpcs="True",
            displayed_session_count=0,
            displayed_session_valid=("0-10", "in")
        )
        self.assertTrue(cnt == 1)

        print("search flow cp session summary from invalid response")
        mock_send_cli_cmd.return_value = False
        status = self.ins.verify_flow_cp_session_summary(
            device=mock_device_ins,
            more_options="source-prefix 10.208.10.0/24",
            node=1,
            dcp_flow_fpc_pic_id="FPC0 PIC0",
            displayed_session_count=50,
            displayed_session_valid=("0-100", "in")
        )
        self.assertFalse(status)

        print("search flow cp session summary with no match")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_SA_FLOW_CP_SESSION_SUMMARY"])
        status = self.ins.verify_flow_cp_session_summary(
            device=mock_device_ins,
            dcp_flow_fpc_pic_id="PIC5",
        )
        self.assertFalse(status)

        print("unsupported option checking")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_SA_FLOW_CP_SESSION_SUMMARY"])
        status = self.ins.verify_flow_cp_session_summary(
            device=mock_device_ins,
            unknown_dcp_flow_fpc_pic_id="PIC5",
        )
        self.assertFalse(status)

        print("keyword not in reponse")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict("""
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4I0/junos">
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-flow">
        <dcp-flow-fpc-pic> on FPC0 PIC0:</dcp-flow-fpc-pic>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-flow">
        <dcp-flow-fpc-pic> on FPC0 PIC1:</dcp-flow-fpc-pic>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
        <max-session-count>7549747</max-session-count>
        <max-inet6-session-count>7549747</max-inet6-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-flow">
        <dcp-flow-fpc-pic> on FPC0 PIC2:</dcp-flow-fpc-pic>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
        <max-session-count>7549747</max-session-count>
        <max-inet6-session-count>7549747</max-inet6-session-count>
    </flow-session-information>
    <flow-session-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-flow">
        <dcp-flow-fpc-pic> on FPC0 PIC3:</dcp-flow-fpc-pic>
        <displayed-session-valid>0</displayed-session-valid>
        <displayed-session-pending>0</displayed-session-pending>
        <displayed-session-invalidated>0</displayed-session-invalidated>
        <displayed-session-other>0</displayed-session-other>
        <displayed-session-count>0</displayed-session-count>
        <max-session-count>7549747</max-session-count>
        <max-inet6-session-count>7549747</max-inet6-session-count>
    </flow-session-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        """)
        status = self.ins.verify_flow_cp_session_summary(
            device=mock_device_ins,
            dcp_flow_fpc_pic_id="PIC5",
        )
        self.assertFalse(status)

        print("Get flow cp session summary with root tag")
        mock_send_cli_cmd.return_value = self.response["HE_SA_FLOW_CP_SESSION_SUMMARY_WITH_ROOT_TAG"]
        status = self.ins.verify_flow_cp_session_summary(
            device=mock_device_ins,
            dcp_flow_fpc_id="9",
            dcp_flow_pic_id="3",
            displayed_session_count="1",
            displayed_session_invalidated="1",
            displayed_session_other="0",
            displayed_session_pending="0",
            displayed_session_valid="0",
            dcp_displayed_session_count="1",
            dcp_displayed_session_invalidated="1",
            dcp_displayed_session_other="0",
            dcp_displayed_session_pending="0",
            dcp_displayed_session_valid="0",
            max_inet6_session_count="7549747",
            max_session_count="7549747",
        )
        self.assertTrue(status)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_fetch_flow_status(self, mock_send_cli_cmd):
        """checking get flow module's status"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("Fetch FLOW status from SA Lowend platform as default")
        response = """
    <rpc-reply>
        <flow-status-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
            <flow-forwarding-mode>
                <flow-forwarding-mode-inet>flow based</flow-forwarding-mode-inet>
                <flow-forwarding-mode-inet6>flow based</flow-forwarding-mode-inet6>
                <flow-forwarding-mode-mpls>drop</flow-forwarding-mode-mpls>
                <flow-forwarding-mode-iso>drop</flow-forwarding-mode-iso>
            </flow-forwarding-mode>
            <flow-trace-option>
                <flow-trace-status>on</flow-trace-status>
                <flow-trace-options>all</flow-trace-options>
            </flow-trace-option>
            <flow-session-distribution>
                <mode>Hash-based</mode>
                <gtpu-distr-status>Disabled</gtpu-distr-status>
            </flow-session-distribution>
            <flow-ipsec-performance-acceleration>
                <ipa-status>off</ipa-status>
            </flow-ipsec-performance-acceleration>
            <flow-packet-ordering>
                <ordering-mode>Hardware</ordering-mode>
            </flow-packet-ordering>
        </flow-status-all>
        <cli>
        <banner>{primary:node0}</banner>
        </cli>
    </rpc-reply>
        """

        mock_device_ins.is_ha.return_value = False
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        xml_dict = self.ins.fetch_flow_status(device=mock_device_ins, timeout=60)
        print(self.tool.pprint(xml_dict))
        self.assertTrue(re.search(r"flow based", xml_dict["flow-status-all"]["flow-forwarding-mode"]["flow-forwarding-mode-inet"]))

        print("Fetch FLOW status from SA Lowend platform as default")
        xml_dict = self.ins.fetch_flow_status(device=mock_device_ins, return_mode="flat_dict")
        print(self.tool.pprint(xml_dict))
        self.assertEqual(xml_dict["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet"], "flow based")
        self.assertEqual(xml_dict["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet6"], "flow based")
        self.assertEqual(xml_dict["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_iso"], "drop")
        self.assertEqual(xml_dict["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_mpls"], "drop")
        self.assertEqual(xml_dict["flow_status_all_flow_ipsec_performance_acceleration_ipa_status"], "off")
        self.assertEqual(xml_dict["flow_status_all_flow_packet_ordering_ordering_mode"], "Hardware")
        self.assertEqual(xml_dict["flow_status_all_flow_session_distribution_gtpu_distr_status"], "Disabled")
        self.assertEqual(xml_dict["flow_status_all_flow_session_distribution_mode"], "Hash-based")
        self.assertEqual(xml_dict["flow_status_all_flow_trace_option_flow_trace_options"], "all")
        self.assertEqual(xml_dict["flow_status_all_flow_trace_option_flow_trace_status"], "on")
        self.assertTrue("cli" not in xml_dict)

        print("Get FLOW status from HE HA topo's node0 status")
        response = """
    <rpc-reply>
        <multi-routing-engine-results>

            <multi-routing-engine-item>

                <re-name>node0</re-name>

                <flow-status-all xmlns="http://xml.juniper.net/junos/15.1I0/junos-flow">
                    <flow-forwarding-mode>
                        <flow-forwarding-mode-inet>flow based</flow-forwarding-mode-inet>
                        <flow-forwarding-mode-inet6>flow based</flow-forwarding-mode-inet6>
                        <flow-forwarding-mode-mpls>drop</flow-forwarding-mode-mpls>
                        <flow-forwarding-mode-iso>drop</flow-forwarding-mode-iso>
                        <flow-enhanced-routing-mode>Disabled</flow-enhanced-routing-mode>
                    </flow-forwarding-mode>
                    <flow-trace-option>
                        <flow-trace-status>off</flow-trace-status>
                    </flow-trace-option>
                    <flow-session-distribution>
                        <mode>RR-based</mode>
                        <gtpu-distr-status>Disabled</gtpu-distr-status>
                    </flow-session-distribution>
                    <flow-ipsec-performance-acceleration>
                        <ipa-status>off</ipa-status>
                    </flow-ipsec-performance-acceleration>
                    <flow-packet-ordering>
                        <ordering-mode>Hardware</ordering-mode>
                    </flow-packet-ordering>
                </flow-status-all>
            </multi-routing-engine-item>

        </multi-routing-engine-results>
        <cli>
        <banner>{primary:node0}</banner>
        </cli>
    </rpc-reply>
        """

        mock_device_ins.is_ha.return_value = True
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        xml_dict = self.ins.fetch_flow_status(device=mock_device_ins, timeout=60)
        print(self.tool.pprint(xml_dict))
        self.assertTrue(re.search(r"node0", xml_dict["re-name"]))

        xml_dict = self.ins.fetch_flow_status(device=mock_device_ins, return_mode="FLAT_DICT", node="0")
        print(self.tool.pprint(xml_dict))
        self.assertEqual(xml_dict["flow_status_all_flow_forwarding_mode_flow_enhanced_routing_mode"], "Disabled")
        self.assertEqual(xml_dict["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet"], "flow based")
        self.assertEqual(xml_dict["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_inet6"], "flow based")
        self.assertEqual(xml_dict["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_iso"], "drop")
        self.assertEqual(xml_dict["flow_status_all_flow_forwarding_mode_flow_forwarding_mode_mpls"], "drop")
        self.assertEqual(xml_dict["flow_status_all_flow_ipsec_performance_acceleration_ipa_status"], "off")
        self.assertEqual(xml_dict["flow_status_all_flow_packet_ordering_ordering_mode"], "Hardware")
        self.assertEqual(xml_dict["flow_status_all_flow_session_distribution_gtpu_distr_status"], "Disabled")
        self.assertEqual(xml_dict["flow_status_all_flow_session_distribution_mode"], "RR-based")
        self.assertEqual(xml_dict["flow_status_all_flow_trace_option_flow_trace_status"], "off")
        self.assertEqual(xml_dict["re_name"], "node0")

        print("Get flow status failed")
        mock_send_cli_cmd.return_value = False
        xml_dict = self.ins.fetch_flow_status(device=mock_device_ins, timeout=60, node="0")
        print(self.tool.pprint(xml_dict))
        self.assertFalse(xml_dict)

    @mock.patch.object(flow_common_tool, "sleep")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_verify_flow_status(self, mock_send_cli_cmd, mock_sleep):
        """checking flow module's status by exact mode"""
        mock_device_ins = mock.Mock()
        mock_sleep.return_value = True

        print("check flow status by exact mode")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["flow_status"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            forwarding_mode_inet="flow based",
            forwarding_mode_inet6=("flow based", "exact"),
            forwarding_mode_mpls="drop",
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status=("off", "exact"),
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status="Disabled",
            session_distribution_mode="Hash-based",
            flow_trace_option="all",
            flow_trace_status="on",
        )
        self.assertTrue(status)

        print("check flow status by exact mode but not match")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["flow_status"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            check_mode="exact",
            forwarding_mode_inet="package",
            forwarding_mode_inet6="package",
            forwarding_mode_mpls="drop",
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status="off",
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status="Disabled",
            session_distribution_mode="Hash-based",
            flow_trace_option="all",
            flow_trace_status="on",
        )
        self.assertFalse(status)

        print("check flow status by contain mode")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["flow_status"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            forwarding_mode_inet=("flow", "contain"),
            forwarding_mode_inet6=("flow", "contain"),
            forwarding_mode_mpls=("drop", "exact"),
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status="off",
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status=("disabled", "contain"),
            session_distribution_mode=("Hash-based", "exact"),
            flow_trace_option="all",
            flow_trace_status="on",
        )
        self.assertTrue(status)

        print("check flow status by contain mode but not match")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["flow_status"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            forwarding_mode_inet=("flow", "contain"),
            forwarding_mode_inet6=("drop", "contain"),
            forwarding_mode_mpls="drop",
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status="off",
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status=("disabled", "contain"),
            session_distribution_mode="Hash-based",
            flow_trace_option="all",
            flow_trace_status="on",
        )
        self.assertFalse(status)

        print("checking invalid user value")
        self.assertRaisesRegex(
            TypeError,
            r"Value for each named options must be",
            self.ins.verify_flow_status,
            device=mock_device_ins,
            forwarding_mode_inet=mock_device_ins,
        )

        print("checking flow status with invalid response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["INVALID_FLOW_STATUS_RESPONSE"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            forwarding_mode_inet="flow",
            forwarding_mode_inet6="flow",
            forwarding_mode_mpls="drop",
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status="off",
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status="disabled",
            session_distribution_mode="Hash-based",
            flow_trace_option="all",
            flow_trace_status="on",
        )

        self.assertFalse(status)

        print("checking flow status with no response")
        mock_send_cli_cmd.return_value = False
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            forwarding_mode_inet="flow",
            forwarding_mode_inet6="flow",
            forwarding_mode_mpls="drop",
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status="off",
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status="disabled",
            session_distribution_mode="Hash-based",
            flow_trace_option="all",
            flow_trace_status="on",
        )
        self.assertFalse(status)

        print("checking flow status on HA from node0")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_STATUS_FROM_HA_NODE0"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            forwarding_mode_inet="flow based exact",
            forwarding_mode_inet6="flow based contain",
            forwarding_mode_mpls="drop",
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status="off",
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status="Disabled",
            session_distribution_mode="RR-based",
            flow_trace_status="off",
            node=0,
        )
        self.assertTrue(status)

        print("checking flow status on HA from node1")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_STATUS_FROM_HA_NODE1"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            forwarding_mode_inet="flow based",
            forwarding_mode_inet6="flow based",
            forwarding_mode_mpls="drop",
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status="off",
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status="Disabled",
            session_distribution_mode="RR-based",
            flow_trace_status="off",
            node=1,
        )
        self.assertTrue(status)

        print("checking flow status several times but encounter accident")
        mock_send_cli_cmd.return_value = False
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            forwarding_mode_inet="flow based",
            forwarding_mode_inet6="flow based",
            forwarding_mode_mpls="drop",
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status="off",
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status="Disabled",
            session_distribution_mode="RR-based",
            flow_trace_status="off",
            check_cnt=3,
            check_interval="0.01"
        )
        self.assertFalse(status)

        print("checking flow status several times because device reponse error message")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["FLOW_STATUS_WITH_ERROR_MSG"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            forwarding_mode_inet="flow based",
            forwarding_mode_inet6="flow based",
            check_cnt=3,
            check_interval="0.01"
        )
        self.assertFalse(status)

        print("checking flow status for tap mode and enhanced_services_mode")
        options = {
            "timeout": 60,
            "tap_mode": "disabled in",
            "enhanced_services_mode": "Disabled",
            "pmi-status": "disabled",
        }
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_STATUS_TAP_MODE"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            **options,
        )
        self.assertTrue(status)

        print("checking flow status with option 'check_mode'")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["FLOW_STATUS_FROM_HA_NODE1"])
        status = self.ins.verify_flow_status(
            device=mock_device_ins,
            timeout=60,
            check_mode="exact",
            forwarding_mode_inet="flow based",
            forwarding_mode_inet6="flow based",
            forwarding_mode_mpls="drop",
            forwarding_mode_iso="drop",
            ipsec_performance_acceleration_ipa_status="off",
            flow_packet_ordering_mode="Hardware",
            session_distribution_gtpu_distr_status="Disabled",
            session_distribution_mode="RR-based",
            flow_trace_status="off",
        )
        self.assertTrue(status)


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_verify_flow_statistics(self, mock_send_cli_cmd):
        """checking flow statistics"""
        mock_device_ins = mock.Mock()

        print("On LE platform, checking counter all matched")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_XML_FLOW_STATISTICS_INFO"])
        status = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            flow_session_count_valid=(0, "eq"),
            flow_pkt_count_fwd="1000 ge",
            flow_pkt_count_drop=(100, "less_than"),
            flow_frag_count_fwd=0,
        )
        self.assertTrue(status)

        print("On LE platform, check counter not matched")
        status = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            flow_session_count_valid=(0, "eq"),
            flow_pkt_count_fwd="1000 ge",
            flow_pkt_count_drop=(100, "less_than"),
            flow_frag_count_fwd=100,
        )
        self.assertFalse(status)

        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HE_XML_FLOW_STATISTICS_INFO"])
        print("On HE platform, checking counter all matched")
        status = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            flow_spu_id="summary",
            flow_pkt_count_fwd="1000 le",
            flow_pkt_count_drop=(1, "EQual"),
            flow_frag_count_fwd=0,
            flow_llf_pkt_count_prd="36 ge"
        )
        self.assertTrue(status)

        print("On HE platform, check counter not matched")
        status = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            flow_spu_id="PIC2",
            flow_session_count_valid=(0, "ge"),
            flow_pkt_count_fwd="1000 le",
            flow_pkt_count_drop=(0, "EQUAL"),
            flow_frag_count_fwd=0,
        )
        self.assertFalse(status)

        print("On HE platform, checking if a PIC matched all counter")
        status = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            flow_session_count_valid=(0, "ge"),
            flow_pkt_count_fwd="1000 le",
            flow_pkt_count_drop=(1, "EQual"),
            flow_frag_count_fwd=0,
        )
        self.assertTrue(status)

        print("On LowEnd HA platform, checking counter all matched")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_XML_NODE0_FLOW_STATISTICS_INFO"])
        status = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            node=0,
            flow_session_count_valid=(0, "eq"),
            flow_pkt_count_fwd="1000 le",
            flow_pkt_count_drop=(1, "gt"),
            flow_frag_count_fwd=0,
        )
        self.assertTrue(status)

        print("On LE platform, checking unsupported PIC's counter (Only HE have PIC name)")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_XML_FLOW_STATISTICS_INFO"])
        status = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            flow_spu_id="PIC0",
            flow_session_count_valid=(0, "eq"),
            flow_pkt_count_fwd="1000 ge",
            flow_pkt_count_drop=(100, "less_than"),
            flow_frag_count_fwd=0,
        )
        self.assertFalse(status)

        print("checking no response return")
        testcase = False
        mock_send_cli_cmd.return_value = False
        self.assertRaisesRegex(
            RuntimeError,
            r"Get flow statistics response failed",
            self.ins.verify_flow_statistics,
            device=mock_device_ins,
        )

        print("Given invalid value")
        self.assertRaisesRegex(
            TypeError,
            r"Value for each named options must be",
            self.ins.verify_flow_statistics,
            device=mock_device_ins,
            flow_spu_id=mock_device_ins,
        )

        print("check new FLOW element on HA for RLI36411")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_HA_XML_FLOW_STATISTICS_AFTER_RLI36411"])
        result = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            flow_session_count_valid=0,
            flow_pkt_count_fwd=0,
            flow_pkt_count_drop=0,
            flow_frag_count_fwd=0,
            flow_pkt_count_rx=8,
            flow_pkt_count_tx=8,
            flow_pkt_count_copy=0,
        )
        self.assertTrue(result)

        result = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            node=1,
            flow_session_count_valid=0,
            flow_pkt_count_fwd=0,
            flow_pkt_count_drop=1,
            flow_frag_count_fwd=0,
            flow_pkt_count_rx=1,
            flow_pkt_count_tx=0,
            flow_pkt_count_copy=0,
        )
        self.assertTrue(result)

        print("check new FLOW element on SA for RLI36411")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_SA_XML_FLOW_STATISTICS_AFTER_RLI36411"])
        result = self.ins.verify_flow_statistics(
            device=mock_device_ins,
            timeout=60,
            flow_session_count_valid=0,
            flow_pkt_count_fwd=0,
            flow_pkt_count_drop=0,
            flow_frag_count_fwd=0,
            flow_pkt_count_rx=8,
            flow_pkt_count_tx=8,
            flow_pkt_count_copy=0,
        )
        self.assertTrue(result)

        print("check invalid device response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_SA_XML_FLOW_STATISTICS_INVALID"])
        case = self.ins.verify_flow_statistics(
                device=mock_device_ins,
                timeout=60,
                flow_session_count_valid=0,
                flow_pkt_count_fwd=0,
                flow_pkt_count_drop=0,
                flow_frag_count_fwd=0,
                flow_pkt_count_rx=8,
                flow_pkt_count_tx=8,
                flow_pkt_count_copy=0,
            )
        self.assertFalse(case)


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_verify_flow_gate(self, mock_send_cli_cmd):
        """checking check flow gate feature"""
        mock_device_ins = mock.Mock()

        print("On HE Platform wich PIC name to checking")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HE_XML_FLOW_GATE_INFO"])
        status = self.ins.verify_flow_gate(
            device=mock_device_ins,
            timeout=60,
            fpc_pic_id="PIC2",
            displayed_gate_valid=(0, "eq"),
            displayed_gate_pending="0",
            displayed_gate_invalidated=(0, "LE"),
            displayed_gate_other=0,
            displayed_gate_count=0,
        )
        self.assertTrue(status)

        print("On HE Platform with No PIC name to checking")
        status = self.ins.verify_flow_gate(
            device=mock_device_ins,
            timeout=60,
            displayed_gate_valid=(0, "eq"),
            displayed_gate_pending="0 ge",
            displayed_gate_invalidated=(0, "LE"),
            displayed_gate_other=0,
            displayed_gate_count=0,
        )
        self.assertTrue(status)

        print("Not match")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HE_XML_FLOW_GATE_INFO"])
        status = self.ins.verify_flow_gate(
            device=mock_device_ins,
            timeout=60,
            fpc_pic_id="PIC2",
            displayed_gate_valid=(0, "gt"),
            displayed_gate_pending="0 gt",
            displayed_gate_invalidated=(0, "LT"),
            displayed_gate_other=0,
            displayed_gate_count=0,
        )
        self.assertFalse(status)

        mock_send_cli_cmd.return_value = False
        self.assertRaisesRegex(
            RuntimeError,
            r"Fetch FLOW gate information failed",
            self.ins.verify_flow_gate,
            device=mock_device_ins, fpc_pic_id="PIC3",
        )

        print("On LE Platform")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["LE_XML_FLOW_GATE_INFO"])
        status = self.ins.verify_flow_gate(
            device=mock_device_ins,
            timeout=60,
            displayed_gate_valid=(0, "eq"),
            displayed_gate_pending="0 ge",
            displayed_gate_invalidated=(0, "LE"),
            displayed_gate_other=0,
            displayed_gate_count=0,
        )
        self.assertTrue(status)

        print("On HE HA Platform")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_NODE0_XML_FLOW_GATE_INFO"])
        status = self.ins.verify_flow_gate(
            device=mock_device_ins,
            timeout=60,
            node=0,
            displayed_gate_valid=(0, "eq"),
            displayed_gate_pending="0 ge",
            displayed_gate_invalidated=(0, "LE"),
            displayed_gate_other=0,
            displayed_gate_count=0,
        )
        self.assertTrue(status)

        print("Match from previous result and invalid option")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_NODE0_XML_FLOW_GATE_INFO"])
        status = self.ins.verify_flow_gate(
            device=mock_device_ins,
            timeout=60,
            node=0,
            displayed_gate_valid=(0, "eq"),
            displayed_gate_pending="0 ge",
            displayed_gate_invalidated=(0, "LE"),
            displayed_gate_other=0,
            displayed_gate_count=0,
            unknown_option=0,
        )
        self.assertFalse(status)


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_verify_flow_session_summary(self, mock_send_cli_cmd):
        """test get flow session summary"""
        mock_device_ins = mock.Mock()

        print("Check flow session summary info from HE HA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_HE_FLOW_SESSION_SUMMARY"])
        status = self.ins.verify_flow_session_summary(
            device=mock_device_ins,
            node=1,
            re_name="node1",
            active_multicast_sessions=0,
            active_services_offload_sessions=("0", "eq"),
            active_session_invalidated=2,
            active_session_other="0",
            active_session_valid="1-10 in",
            failed_sessions=0,
        )
        self.assertTrue(status)

        print("Check flow session summary info from HE HA topo with match counter")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_HE_FLOW_SESSION_SUMMARY"])
        counter = self.ins.verify_flow_session_summary(
            device=mock_device_ins,
            return_mode="counter",
            re_name="node1",
            active_multicast_sessions=0,
            active_services_offload_sessions=("0", "eq"),
            active_session_invalidated=2,
            active_session_other="0",
            active_session_valid="1-10 in",
            failed_sessions=0,
        )
        self.assertTrue(counter == 1)

        print("Check flow session summary info from LE SA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_LE_FLOW_SESSION_SUMMARY"])
        status = self.ins.verify_flow_session_summary(
            device=mock_device_ins,
            active_multicast_sessions=0,
            active_session_invalidated=2,
            active_session_other="0",
            active_session_valid="1-10 in",
            failed_sessions=0,
        )
        self.assertTrue(status)

        status = self.ins.verify_flow_session_summary(
            device=mock_device_ins,
            active_multicast_sessions=0,
            active_services_offload_sessions=("0", "eq"),
            active_session_invalidated=0,
            active_session_other="0",
            active_session_valid="0-10 in",
            failed_sessions=0,
        )
        self.assertFalse(status)

        print("Check cannot get flow session summary info")
        mock_send_cli_cmd.return_value = False
        status = self.ins.verify_flow_session_summary(device=mock_device_ins)
        self.assertFalse(status)

        print("Check not existing flow session summary info")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_LE_FLOW_SESSION_SUMMARY"])
        status = self.ins.verify_flow_session_summary(
            device=mock_device_ins,
            active_multicast_sessions=0,
            active_services_offload_sessions=("0", "eq"),
            active_session_invalidated=2,
            active_session_other="0",
            active_session_valid="1-10 in",
            failed_sessions=0,
            un_existing_element=0,
        )
        self.assertFalse(status)

        print("Check FLOW session summary from SA HE for root tag")
        mock_send_cli_cmd.return_value = self.response["SA_HE_FLOW_SESSION_SUMMARY_FOR_ROOT_TAG"]
        status = self.ins.verify_flow_session_summary(
            device=mock_device_ins,
            return_mode="counter",
            flow_fpc_id=9,
            flow_pic_id="1-3",
            active_sessions="2 ge",
        )
        self.assertTrue(status == 2)

        print("Check FLOW session summary from HA LE for root tag")
        mock_send_cli_cmd.return_value = self.response["HA_LE_FLOW_SESSION_SUMMARY_FOR_ROOT_TAG"]
        status = self.ins.verify_flow_session_summary(
            device=mock_device_ins,
            re_name="node1",
            max_sessions="4194304",
        )
        self.assertTrue(status)

        print("Check FLOW session summary from SA HE for root tag and more options")
        mock_send_cli_cmd.return_value = self.response["SA_HE_FLOW_SESSION_SUMMARY_WITH_MORE_OPTION_FOR_ROOT_TAG"]
        status = self.ins.verify_flow_session_summary(
            device=mock_device_ins,
            dcp_displayed_session_count="1",
            displayed_session_valid="1",
            dcp_displayed_session_other="0",
            displayed_session_pending="0",
            return_mode="counter",
        )
        self.assertTrue(status == 2)



    @mock.patch("time.sleep")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_execute_clear_flow_session(self, mock_send_cli_cmd, mock_sleep):
        """checking clear flow session feature"""
        mock_device_ins = mock.Mock()
        mock_send_cli_cmd.return_value = ""

        print("checking clear command on SA platform")
        base = "clear security flow session"
        all_patterns = (
            "{} all".format(base),
            "{} advanced-anti-malware".format(base),
            "{} application-firewall".format(base),
            "{} application-traffic-control".format(base),
            "{} idp".format(base),
            "{} nat".format(base),
            "{} resource-manager".format(base),
            "{} security-intelligence".format(base),
            "{} tunnel".format(base),
            "{} {} {}".format(base, "application", "tcp"),
            "{} {} {}".format(base, "family", "inet6"),
            "{} {} {}".format(base, "interface", "ge-5/0/0"),
            "{} {} {}".format(base, "conn-tag", "10"),
            "{} {} {}".format(base, "source-port", "10000"),
            "{} {} {}".format(base, "destination-port", "20000"),
            "{} {} {}".format(base, "session-identifier", "5867"),
            "{} {} {}".format(base, "protocol", "23"),
            "{} {} {}".format(base, "source-prefix", "192.168.1.0/24"),
            "{} {} {}".format(base, "destination-prefix", "192.168.2.0/24"),
        )

        cmd_list = self.ins.execute_clear_flow_session(
            device=mock_device_ins,
            return_cmd=True,
            advanced_anti_malware=True,
            application_firewall=True,
            application_traffic_control=True,
            idp=True,
            nat=True,
            resource_manager=True,
            security_intelligence=True,
            tunnel=True,
            application="tcp",
            family="inet6",
            interface="ge-5/0/0",
            conn_tag=10,
            source_port=10000,
            destination_port=20000,
            session_identifier=5867,
            protocol=23,
            source_prefix="192.168.1.0/24",
            destination_prefix="192.168.2.0/24",
            sleep=1,
        )

        result_list = []
        print("cmd_list: ", cmd_list)
        for cmd in cmd_list:
            match_mark = "ERR"
            for pattern in all_patterns:
                if re.match(pattern, cmd):
                    match_mark = "INFO"

            print("match cmd: ", cmd)
            result_list.append(match_mark)

        self.assertTrue(False not in result_list)

        print("checking clear command on HA platform")
        cmd_list = self.ins.execute_clear_flow_session(
            device=mock_device_ins,
            return_cmd=True,
            advanced_anti_malware=True,
            node=0,
        )

        print(cmd_list)
        self.assertTrue("clear security flow session node 0 advanced-anti-malware" in cmd_list)

        print("checking clear all session")
        cmd_list = self.ins.execute_clear_flow_session(
            device=mock_device_ins,
            return_cmd=True,
        )

        self.assertTrue("clear security flow session" in cmd_list)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_execute_clear_flow_ip_action(self, mock_send_cli_cmd):
        """checking clear flow ip-action feature"""
        mock_device_ins = mock.Mock()
        mock_send_cli_cmd.return_value = ""

        print("checking clear command on SA platform")
        base = "clear security flow ip-action"
        response = self.ins.execute_clear_flow_ip_action(device=mock_device_ins)
        self.assertEqual(response, "")

        all_patterns = (
            "{} all".format(base),
            "{} {} {}".format(base, "family", "inet6"),
            "{} {} {}".format(base, "source-port", "10000"),
            "{} {} {}".format(base, "destination-port", "20000"),
            "{} {} {}".format(base, "protocol", "23"),
            "{} {} {}".format(base, "source-prefix", "192.168.1.0/24"),
            "{} {} {}".format(base, "destination-prefix", "192.168.2.0/24"),
        )

        cmd_list = self.ins.execute_clear_flow_ip_action(
            device=mock_device_ins,
            return_cmd=True,
            all=True,
            family="inet6",
            source_port=10000,
            destination_port=20000,
            protocol=23,
            source_prefix="192.168.1.0/24",
            destination_prefix="192.168.2.0/24",
        )

        result_list = []
        print("cmd_list: ", cmd_list)
        for cmd in cmd_list:
            match_mark = "ERR"
            for pattern in all_patterns:
                if re.match(pattern, cmd):
                    match_mark = "INFO"

            print("match cmd: ", cmd)
            result_list.append(match_mark)

        self.assertTrue(False not in result_list)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_execute_clear_flow_statistics(self, mock_send_cli_cmd):
        """checking clear flow statistics feature"""
        mock_device_ins = mock.Mock()
        mock_send_cli_cmd.return_value = ""

        print("checking clear command on SA platform")
        response = self.ins.execute_clear_flow_statistics(device=mock_device_ins)
        self.assertEqual(response, "")

        print("add more options")
        response = self.ins.execute_clear_flow_statistics(device=mock_device_ins, more_options="more options", return_cmd=True)
        self.assertEqual(response, "clear security flow statistics more options")

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_operation_delete_flow_configuration(self, mock_send_cli_cmd):
        """checking delete flow configuration feature"""
        mock_device_ins = mock.Mock()
        mock_send_cli_cmd.return_value = ""

        print("delete several flow configuration from list")
        base = "delete security flow"

        options = (
            "advanced-options drop-matching-link-local-address",
            "tcp-mss",
            "tcp-session",
        )

        cmd_list = self.ins.operation_delete_flow_configuration(
            device=mock_device_ins,
            return_cmd=True,
            options=options,
        )

        all_patterns = []
        for option in options:
            all_patterns.append("{} {}".format(base, option))

        result_list = []
        print(cmd_list)
        for cmd in cmd_list:
            match_mark = "ERR"
            for pattern in all_patterns:
                if re.match(pattern, cmd):
                    match_mark = "INFO"

            print("match cmd: ", cmd)
            result_list.append(match_mark)

        self.assertTrue(False not in result_list)

        print("delete sub flow configuration")
        cmd_list = self.ins.operation_delete_flow_configuration(
            device=mock_device_ins,
            return_cmd=True,
            options="advanced-options drop-matching-link-local-address",
        )
        self.assertTrue("delete security flow advanced-options drop-matching-link-local-address" in cmd_list)

        print("invalid more_options")
        self.assertRaisesRegex(
            ValueError,
            r"'options' must be STR, LIST or TUPLE",
            self.ins.operation_delete_flow_configuration,
            device=mock_device_ins,
            return_cmd=True,
            options=mock_device_ins,
        )

    @mock.patch.object(dev, "execute_vty_command_on_device")
    def test_fetch_flow_session_on_vty(self, mock_execute_vty_command_on_device):
        """checking delete flow configuration feature"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("Get session from HA LE topo")
        mock_execute_vty_command_on_device.return_value = self.response["HA_LE_FLOW_VTY_ALL_SESSION"]

        result = self.ins.fetch_flow_session_on_vty(device=mock_device_ins)
        print(self.tool.pprint(result))
        self.assertListEqual(result, self.response["EXPECT_HA_LE_FLOW_VTY_ALL_SESSION"])

        print("Get tunnel session from SA LE topo")
        mock_execute_vty_command_on_device.return_value = self.response["SA_LE_FLOW_VTY_ALL_SESSION"]

        result = self.ins.fetch_flow_session_on_vty(device=mock_device_ins)
        print(self.tool.pprint(result))
        self.assertListEqual(result, self.response["EXPECT_SA_LE_FLOW_VTY_ALL_SESSION"])


        print("Invalid test")
        self.assertRaisesRegex(
            ValueError,
            r"option 'destination' should be",
            self.ins.fetch_flow_session_on_vty,
            device=mock_device_ins, destination="Unknown",
        )

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_fetch_flow_pmi_statistics(self, mock_execute_cli_command_on_device):
        """UT"""
        mock_device_ins = mock.Mock()

        print("Get PMI statistics from HA LE topo for normal")
        mock_execute_cli_command_on_device.return_value = self.response["HA_LE_FLOW_PMI_STATISTICS"]
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins)
        print(self.tool.pprint(result))
        self.assertTrue(result[0]["re-name"] == "node0")
        self.assertTrue(result[1]["re-name"] == "node1")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-decap-bytes"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-decap-pkts"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-drop"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-encap-bytes"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-encap-pkts"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-rfp"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-rx"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-tx"] == "0")

        print("Get PMI statistics from HA LE topo for flat_dict")
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins, return_mode="flat_dict")
        print(self.tool.pprint(result))
        self.assertTrue(result[0]["re_name"] == "node0")
        self.assertTrue(result[1]["re_name"] == "node1")
        self.assertTrue(result[0]["pmi_decap_bytes"] == "0")
        self.assertTrue(result[0]["pmi_decap_pkts"] == "0")
        self.assertTrue(result[0]["pmi_drop"] == "0")
        self.assertTrue(result[0]["pmi_encap_bytes"] == "0")
        self.assertTrue(result[0]["pmi_encap_pkts"] == "0")
        self.assertTrue(result[0]["pmi_rfp"] == "0")
        self.assertTrue(result[0]["pmi_rx"] == "0")
        self.assertTrue(result[0]["pmi_tx"] == "0")

        print("Get PMI statistics from HA HE topo for normal")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_FLOW_PMI_STATISTICS"]
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins)
        print(self.tool.pprint(result))
        self.assertTrue(result[0]["re-name"] == "node0")
        self.assertTrue(result[1]["re-name"] == "node1")
        self.assertTrue(result[0]["flow-pmi-statistics"][0]["pmi-spu-id"] == "of FPC2 PIC0:")
        self.assertTrue(result[0]["flow-pmi-statistics"][1]["pmi-spu-id"] == "of FPC2 PIC1:")
        self.assertTrue(result[0]["flow-pmi-statistics"][2]["pmi-spu-id"] == "summary:")
        self.assertTrue(result[1]["flow-pmi-statistics"][0]["pmi-spu-id"] == "of FPC2 PIC0:")
        self.assertTrue(result[1]["flow-pmi-statistics"][1]["pmi-spu-id"] == "of FPC2 PIC1:")
        self.assertTrue(result[1]["flow-pmi-statistics"][2]["pmi-spu-id"] == "summary:")

        print("Get PMI statistics from HA HE topo for flat_dict")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_FLOW_PMI_STATISTICS"]
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins, return_mode="FLAT_DICT")
        print(self.tool.pprint(result))
        self.assertTrue(len(result) == 6)
        self.assertTrue(result[0]["re_name"] == "node0")
        self.assertTrue(result[-1]["re_name"] == "node1")
        self.assertTrue(result[0]["pmi_spu_id"] == "of FPC2 PIC0:")
        self.assertTrue(result[1]["pmi_spu_id"] == "of FPC2 PIC1:")
        self.assertTrue(result[2]["pmi_spu_id"] == "summary:")
        self.assertTrue(result[3]["pmi_spu_id"] == "of FPC2 PIC0:")
        self.assertTrue(result[4]["pmi_spu_id"] == "of FPC2 PIC1:")
        self.assertTrue(result[5]["pmi_spu_id"] == "summary:")

        print("Get PMI statistics from SA LE topo for normal")
        mock_execute_cli_command_on_device.return_value = self.response["SA_LE_FLOW_PMI_STATISTICS"]
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins)
        print(self.tool.pprint(result))
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-decap-bytes"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-decap-pkts"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-drop"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-encap-bytes"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-encap-pkts"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-rfp"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-rx"] == "0")
        self.assertTrue(result[0]["flow-pmi-statistics"]["pmi-tx"] == "0")
        self.assertTrue("re-name" not in result[0])

        print("Get PMI statistics from SA LE topo for FLAT_DICT")
        mock_execute_cli_command_on_device.return_value = self.response["SA_LE_FLOW_PMI_STATISTICS"]
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins, return_mode="FLAT_DICT")
        print(self.tool.pprint(result))
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0]["pmi_decap_bytes"] == "0")
        self.assertTrue(result[0]["pmi_decap_pkts"] == "0")
        self.assertTrue(result[0]["pmi_drop"] == "0")
        self.assertTrue(result[0]["pmi_encap_bytes"] == "0")
        self.assertTrue(result[0]["pmi_encap_pkts"] == "0")
        self.assertTrue(result[0]["pmi_rfp"] == "0")
        self.assertTrue(result[0]["pmi_rx"] == "0")
        self.assertTrue(result[0]["pmi_tx"] == "0")
        self.assertTrue("re_name" not in result[0])

        print("Get PMI statistics from SA HE topo for normal")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_FLOW_PMI_STATISTICS"]
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins)
        print(self.tool.pprint(result))
        self.assertTrue("re-name" not in result[0])
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0]["flow-pmi-statistics"][0]["pmi-spu-id"] == "of FPC0 PIC0:")
        self.assertTrue(result[0]["flow-pmi-statistics"][1]["pmi-spu-id"] == "of FPC0 PIC1:")
        self.assertTrue(result[0]["flow-pmi-statistics"][2]["pmi-spu-id"] == "summary:")

        print("Get PMI statistics from SA HE topo for FLAT_DICT")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_FLOW_PMI_STATISTICS"]
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins, return_mode="FLAT_DICT", node=1)
        print(self.tool.pprint(result))
        self.assertTrue("re_name" not in result[0])
        self.assertTrue(len(result) == 3)
        self.assertTrue(result[0]["pmi_spu_id"] == "of FPC0 PIC0:")
        self.assertTrue(result[1]["pmi_spu_id"] == "of FPC0 PIC1:")
        self.assertTrue(result[2]["pmi_spu_id"] == "summary:")

        print("cannot get response from device")
        mock_execute_cli_command_on_device.return_value = False
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins)
        print(self.tool.pprint(result))
        self.assertFalse(result)

        print("No PMI result in XML")
        mock_execute_cli_command_on_device.return_value = self.response["WRONG_FLOW_PMI_STATISTICS"]
        result = self.ins.fetch_flow_pmi_statistics(device=mock_device_ins, return_mode="FLAT_DICT", node=1)
        print(self.tool.pprint(result))
        self.assertTrue(result == [])


    @mock.patch.object(flows, "fetch_flow_session_on_vty")
    def test_verify_flow_session_on_vty(self, mock_fetch_flow_session_on_vty):
        """checking delete flow configuration feature"""
        mock_device_ins = mock.Mock()

        print("Get session from HA LE topo")
        mock_fetch_flow_session_on_vty.return_value = self.response["EXPECT_SA_LE_FLOW_VTY_ALL_SESSION"]
        condition = {
            "in_src_addr": "30.30.30.1-255 in",
            "in_dst_port": "1-65535 in",
            "in_dp": 0,
            "in_if": "ge-0/0/1.0 in",
            "final_nh": "0x587f5440",
            "out_src_addr": None,
        }
        result = self.ins.verify_flow_session_on_vty(device=mock_device_ins, condition=condition)
        self.assertTrue(result)

        result = self.ins.verify_flow_session_on_vty(
            device=mock_device_ins,
            in_src_addr="30.30.30.1-255 in",
            in_dst_port="1-65535 in",
            in_dp=0,
            in_if="ge-0/0/1.0 in",
            final_nh="0x587f5440",
            out_src_addr=None,
        )
        self.assertTrue(result)

        print("checking if device don't have keyword")
        condition = {
            "in_src_addr": "30.30.30.1-255 in",
            "in_dst_port": "1-65535 in",
            "in_dp": 0,
            "in_if": "ge-0/0/1.0 in",
            "final_nh": "0x587f5440",
            "unknown_keyword": "unknown",
        }
        result = self.ins.verify_flow_session_on_vty(device=mock_device_ins, condition=condition)
        self.assertFalse(result)

        print("checking if no condition or condition is empty")
        self.assertTrue(self.ins.verify_flow_session_on_vty(device=mock_device_ins))
        self.assertTrue(self.ins.verify_flow_session_on_vty(device=mock_device_ins, condition={}))

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_verify_flow_pmi_statistics(self, mock_execute_cli_command_on_device):
        """UT"""
        mock_device_ins = mock.Mock()

        print("Verify PMI statistics from HA LE topo")
        mock_execute_cli_command_on_device.return_value = self.response["HA_LE_FLOW_PMI_STATISTICS"]
        result = self.ins.verify_flow_pmi_statistics(
            device=mock_device_ins,
            return_mode="counter",
            pmi_decap_bytes=0,
            pmi_rx="0",
        )
        print(self.tool.pprint(result))
        self.assertTrue(result == 2)

        print("Get PMI statistics from HA HE topo")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_FLOW_PMI_STATISTICS"]
        result = self.ins.verify_flow_pmi_statistics(
            device=mock_device_ins,
            node=1,
            pmi_decap_bytes=0,
            pmi_spu_id="FPC2 PIC1 in",
        )
        print(self.tool.pprint(result))
        self.assertTrue(result)

        print("Get PMI statistics from SA LE topo for FLAT_DICT")
        mock_execute_cli_command_on_device.return_value = self.response["SA_LE_FLOW_PMI_STATISTICS"]
        result = self.ins.verify_flow_pmi_statistics(device=mock_device_ins, return_mode="FLAT_DICT")
        print(self.tool.pprint(result))
        result = self.ins.verify_flow_pmi_statistics(
            device=mock_device_ins,
            re_name="node1",
        )
        self.assertFalse(result)

        print("Get PMI statistics from SA HE topo for FLAT_DICT")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_FLOW_PMI_STATISTICS"]
        result = self.ins.verify_flow_pmi_statistics(
            device=mock_device_ins,
            return_mode="counter",
            pmi_decap_bytes=0,
        )
        print(self.tool.pprint(result))
        self.assertTrue(result == 3)

