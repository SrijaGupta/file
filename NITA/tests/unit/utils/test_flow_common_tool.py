# coding: UTF-8
"""All unit test cases for CommonTool"""
# pylint: disable=attribute-defined-outside-init,invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
# import requests
from unittest import TestCase, mock
from mock import patch
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool


class Req():
    """mock request"""
    def __init__(self):
        """init"""
        self.content = None
        self.status_code = None

class TestFlowCommonTool(TestCase):
    """Unitest cases for CommonTool module"""
    def setUp(self):
        """setup before all case"""
        self.xml = xml_tool()
        self.ins = flow_common_tool()

        self.response = {}
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

        self.response["HA_LE_FLOW_SESSION_BY_PYEZ"] = """
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
        """

        self.response["SA_LE_FLOW_SESSION_SUMMARY_BY_PYEZ"] = """
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
        """

        self.response["FILTER_OPTION_FROM_ENTRY_LIST_1"] = [
            {
                "blk_high_port": "1151",
                "blk_internal_ip": "192.168.150.0",
                "blk_low_port": "1024",
                "blk_ports_ol": "1",
                "blk_ports_total": "128",
                "blk_ports_used": "0",
                "blk_reflexive_ip": "192.168.150.0",
                "re_name": "node0"
            },
            {
                "blk_high_port": "1279",
                "blk_internal_ip": "192.168.150.1",
                "blk_low_port": "1152",
                "blk_ports_ol": "1",
                "blk_ports_total": "128",
                "blk_ports_used": "0",
                "blk_reflexive_ip": "192.168.150.0",
                "re_name": "node0"
            },
            {
                "blk_high_port": "1407",
                "blk_internal_ip": "192.168.150.2",
                "blk_low_port": "1280",
                "blk_ports_ol": "1",
                "blk_ports_total": "128",
                "blk_ports_used": "0",
                "blk_reflexive_ip": "192.168.150.0",
                "re_name": "node0"
            },
            {
                "blk_high_port": "1535",
                "blk_internal_ip": "192.168.150.3",
                "blk_low_port": "1408",
                "blk_ports_ol": "1",
                "blk_ports_total": "128",
                "blk_ports_used": "0",
                "blk_reflexive_ip": "192.168.150.0",
                "re_name": "node0"
            },
            {
                "blk_high_port": "1151",
                "blk_internal_ip": "192.168.150.0",
                "blk_low_port": "1024",
                "blk_ports_ol": "1",
                "blk_ports_total": "128",
                "blk_ports_used": "0",
                "blk_reflexive_ip": "192.168.150.0",
                "re_name": "node1"
            },
            {
                "blk_high_port": "1279",
                "blk_internal_ip": "192.168.150.1",
                "blk_low_port": "1152",
                "blk_ports_ol": "1",
                "blk_ports_total": "128",
                "blk_ports_used": "0",
                "blk_reflexive_ip": "192.168.150.0",
                "re_name": "node1"
            },
            {
                "blk_high_port": "1407",
                "blk_internal_ip": "192.168.150.2",
                "blk_low_port": "1280",
                "blk_ports_ol": "1",
                "blk_ports_total": "128",
                "blk_ports_used": "0",
                "blk_reflexive_ip": "192.168.150.0",
                "re_name": "node1"
            },
            {
                "blk_high_port": "1535",
                "blk_internal_ip": "192.168.150.3",
                "blk_low_port": "1408",
                "blk_ports_ol": "1",
                "blk_ports_total": "128",
                "blk_ports_used": "0",
                "blk_reflexive_ip": "192.168.150.0",
                "re_name": "node1"
            }
        ]




    def test_get_current_function_name(self):
        """checking get current function name function"""
        response = self.ins.get_current_function_name()
        self.assertTrue(response == "test_get_current_function_name")

    def test_split_string_to_value_and_action(self):
        """checking split string to value and action method"""
        print("checking without mode")
        without_mode_cases = (
            ("hello world", "IN"),
            ("hello, I'm Jon, write this script to testing method for unittest.", "IN"),
            ("a string and check pattern ne", "NE"),
            ("hello world exact", "EXACT"),
            ("hello world equal", "EQUAL"),
            ("hello world eq", "EQ"),
            ("hello world in", "IN"),
            ("hello world contain", "CONTAIN"),
            ("10000 eq", "EQ"),
            ("10000 equal", "EQUAL"),
            ("10020 ne", "NE"),
            ("10020 not_equal", "NOT_EQUAL"),
            ("10010 great_than", "GREAT_THAN"),
            ("10010 gt", "GT"),
            ("20010 ge", "GE"),
            ("20010 great_or_equal_than", "GREAT_OR_EQUAL_THAN"),
            ("30010 lt", "LT"),
            ("30010 less_than", "LESS_THAN"),
            ("40010 le", "LE"),
            ("40010 less_or_equal_than", "LESS_OR_EQUAL_THAN"),
            ("56789 not a pattern", "IN"),
            ("192.168.100.10 - 192.168.100.20 in", "IN"),
            ("192.168.100.10-192.168.100.20 contain", "CONTAIN"),
        )

        all_result_list = []
        for index, case in enumerate(without_mode_cases, start=1):
            user_value = case[0]
            expect_action = case[1]
            result = self.ins.split_string_to_value_and_action(user_string=user_value)
            if re.match(str(result[0]), user_value) and result[1] == expect_action:
                check_result = True
            else:
                check_result = False

            print("{:02d} {: <5s} splited_result: {}".format(index, str(check_result), result))
            all_result_list.append(check_result)

        self.assertTrue(False not in all_result_list)

        print("check with mode option")
        with_mode_cases = (
            ("100", ("100", "EQ", "INT")),
            ("1 gt", ("1", "GT", "INT")),
            ("1 - 10", ("1 - 10", "IN", "INT")),
            ("1~10", ("1~10", "IN", "INT")),
            ("1.0 gt", ("1.0", "GT", "FLOAT")),
            ("1.0-10.0", ("1.0-10.0", "IN", "FLOAT")),
            ("1.0 ~ 10.0", ("1.0 ~ 10.0", "IN", "FLOAT")),
            ("100.0001", ("100.0001", "EQ", "FLOAT")),
            ("100.0001 ne", ("100.0001", "NE", "FLOAT")),
            ("ge-0/0/1 in", ("ge-0/0/1", "IN", "STR")),
            ("ge-0/0/1.0", ("ge-0/0/1.0", "IN", "STR")),
            ("ge-0/0/1.0 eq", ("ge-0/0/1.0", "EQ", "STR")),
            ("::", ("::", "EQ", "IP")),
            ("1.1.1.0/24", ("1.1.1.0/24", "IN", "IP")),
            ("1.1.1.0/24 eq", ("1.1.1.0/24", "EQ", "IP")),
            ("1.1.1.1-254 in", ("1.1.1.1~1.1.1.254", "IN", "IP")),
            ("1.1.1.1-254 eq", ("1.1.1.1~1.1.1.254", "EQ", "IP")),
            ("  2020-03-25 00:00:00 ~ 2020-03-31 23:59:59 ", ("2020-03-25 00:00:00 ~ 2020-03-31 23:59:59", "IN", "DATE")),
            ("  2020-03-25 00:00:00 ~ 2020-03-31 23:59:59 in", ("2020-03-25 00:00:00 ~ 2020-03-31 23:59:59", "IN", "DATE")),
            ("2020-03-25 00:00:00 ge", ("2020-03-25 00:00:00", "GE", "DATE")),
        )

        all_result_list = []
        for index, case in enumerate(with_mode_cases, start=1):
            user_value = case[0]
            expect_value = case[1][0]
            expect_action = case[1][1]
            expect_mode = case[1][2]
            result = self.ins.split_string_to_value_and_action(user_string=user_value, with_mode=True)
            if re.match(str(result[0]), expect_value) and result[1] == expect_action and result[2] == expect_mode:
                check_result = True
            else:
                check_result = False

            print("{:02d} {: <5s} splited_result: {}".format(index, str(check_result), result))
            all_result_list.append(check_result)

        self.assertTrue(False not in all_result_list)

        result = self.ins.split_string_to_value_and_action(user_string="hello", with_mode=True, default_mode="IP")
        print("default mode result: ", result)
        self.assertEqual(result, ("hello", "EQ", "IP"))

        print("check with_mode option")
        check_list = (
            ("100", ("100", None, "INT")),
            ("1 gt", ("1", "gt", "INT")),
            ("1.0 gt", ("1.0", "gt", "FLOAT")),
            ("100.0001", ("100.0001", None, "FLOAT")),
            ("100.0001 ne", ("100.0001", "ne", "FLOAT")),
            ("ge-0/0/1 in", ("ge-0/0/1", "in", "STR")),
            ("ge-0/0/1.0", ("ge-0/0/1.0", None, "STR")),
            ("::", ("::", None, "IP")),
            ("1.1.1.0/24", ("1.1.1.0/24", None, "IP")),
            ("1.1.1.0/24 eq", ("1.1.1.0/24", "eq", "IP")),
            ("1.1.1.1-254 in", ("1.1.1.1-254", "in", "IP")),
            ("1.1.1.1-254 eq", ("1.1.1.1-254", "eq", "IP")),
            ("   1.1.1.1-254 eq  ", ("1.1.1.1-254", "eq", "IP")),
            ("200::q", ("2000::/64", "eq", "IP")),
        )
        all_result_list = []
        for index, case in enumerate(check_list, start=1):
            user_value = case[0]
            expect_action = case[1]
            result = self.ins.split_string_to_value_and_action(user_string=user_value)
            if re.match(str(result[0]), user_value) and result[1] == expect_action:
                check_result = True
            else:
                check_result = False

            print("{:02d} {: <5s} splited_result: {}".format(index, str(check_result), result))
            all_result_list.append(check_result)

        self.assertTrue(True not in all_result_list)


    def test_do_compare(self):
        """check do compare"""
        mock_device_ins = mock.Mock()

        material = (
            # mode, value_a, value_b, action, expect_result
            ("IP", "192.168.1.0/24", "192.168.2.0/24", "EQ", False),
            ("IPADDR", "192.168.0.0/16", "192.168.2.0/24", "EQUAL", False),
            ("IPADDRESS", "100.1.1.1/32", "100.1.1.1", "eq", True),
            ("IP", "100.1.1/32", "100.1.1.1/32", "EQUAL", False),
            ("NETWORK", "192.168.1.1/24", "192.168.1.1/32", "equal", False),
            ("NETWORK", "200.1.1.1", "200.1.1.1", "EQ", True),
            ("IPADDR", "200.1.0.0/16", "200.1.0.0/24", "EQ", False),

            ("IP", "192.168.1.0/24", "192.168.2.0/24", "NE", True),
            ("IP", "192.168.0.0/16", "192.168.2.0/24", "NE", True),
            ("IP", "100.1.1.1/32", "100.1.1.1", "NE", False),
            ("IP", "192.168.1.1/24", "192.168.1.1/32", "NE", True),  # Even mask is 24, still equal
            ("IP", "200.1.1.1", "200.1.1.1", "NOT_EQUAL", False),
            ("IP", "200.1.0.0/16", "200.1.0.0/24", "NOT_EQUAL", True),

            ("IP", "192.168.1.1", "192.168.2.0/24", "IN", False),
            ("IP", "192.168.1.1", "192.168.1.0/24", "CONTAIN", True),
            ("IP", "192.168.0.0/16", "192.168.2.0/24", "CONTAIN", False),
            ("IP", "192.168.2.0/24", "192.168.0.0/16", "CONTAIN", True),
            ("IP", "100.1.1.1/32", "100.1.1.1", "CONTAIN", True),
            ("IP", "200.1.1.1", "200.1.1.1", "CONTAIN", True),
            ("IP", "200.1.0.0/16", "200.1.0.0/24", "CONTAIN", False),
            ("IP", "200.1.0.0/24", "200.1.0.0/16", "CONTAIN", True),
            ("IP", "    200.1.0.0/24   ", "   200.1.0.0/16   ", "CONTAIN", True),
            ("IP", "192.168.100.15", "192.168.100.10-192.168.100.20", "IN", True),
            ("IP", "192.168.100.15", "192.168.100.10 - 192.168.100.20", "IN", True),
            ("IP", "192.168.200.15", "192.168.100.10 - 192.168.200.20", "IN", True),
            ("IP", "192.168.200.15", "192.168.100.10 ~ 192.168.200.20", "IN", True),
            ("IP", "192.168.100.5", "192.168.100.10 - 192.168.100.20", "IN", False),
            ("IP", "192.168.100.5", "192.168.100.10 - 192.168.200.20", "IN", False),
            ("IP", "192.168.100.5", "192.168.100.10 ~ 192.168.200.20", "IN", False),
            ("IP", "30.0.1.1", "30.0.1.0-30.0.1.2", "IN", True),
            ("IP", "192.168.10.20", "192.168.1.1-100", "IN", False),

            ("INT", 1, 2, "LT", True),
            ("NUMBER", 1, 1, "LT", False),
            ("FLOAT", "1", "2", "LT", True),
            ("INTEGER", "1", "1", "LESS_THAN", False),
            ("INT", 20, 10, "LESS_THAN", False),
            ("INT", "20", "10", "LESS_THAN", False),
            ("INT", 1048576, 1050768, "LESS_THAN", True),
            ("INT", 15, "10-20", "IN", True),
            ("FLOAT", "10", "10-20", "IN", True),
            ("FLOAT", "20", "10-20", "IN", True),
            ("FLOAT", "5", "10-20", "IN", False),

            ("NUMBER", 1, 2, "LE", True),
            ("NUMBER", 1, 1, "LE", True),
            ("NUMBER", "1", "2", "LE", True),
            ("NUMBER", "1", "1", "LESS_OR_EQUAL_THAN", True),
            ("NUMBER", "1", "1", "LESS_OR_EQUAL_THAN", True),
            ("NUMBER", 20, 10, "LESS_OR_EQUAL_THAN", False),
            ("NUMBER", "20", "10", "LESS_OR_EQUAL_THAN", False),
            ("NUMBER", 1048576, 1050768, "LESS_OR_EQUAL_THAN", True),

            ("INT", 1, 2, "EQ", False),
            ("INT", 1, 1, "EQ", True),
            ("INT", "1", "2", "EQ", False),
            ("INT", "1", "1", "EQ", True),
            ("INT", "1", 1, "EQUAL", True),
            ("INT", 20, 10, "EQUAL", False),
            ("INT", "20", "10", "EQUAL", False),
            ("INT", 1048576, 1050768, "EQUAL", False),
            ("INT", "1.01", 1.01, "EQUAL", True),

            ("INT", 1, 2, "NE", True),
            ("INT", 1, 1, "NE", False),
            ("INT", "1", "2", "NE", True),
            ("INT", "1", "1", "NE", False),
            ("INT", "1", 1, "NE", False),
            ("INT", 20, 10, "NOT_EQUAL", True),
            ("INT", "20", "10", "NOT_EQUAL", True),
            ("INT", 1048576, 1050768, "NOT_EQUAL", True),
            ("INT", "1.01", 1.01, "NOT_EQUAL", False),

            ("INT", 1, 2, "GT", False),
            ("INT", 1, 1, "GT", False),
            ("INT", "1", "2", "GT", False),
            ("INT", "1", "1", "GT", False),
            ("INT", "1", 1, "GREAT_THAN", False),
            ("INT", 20, 10, "GREAT_THAN", True),
            ("INT", "20", "10", "GREAT_THAN", True),
            ("INT", 1048576, 1050768, "GREAT_THAN", False),
            ("INT", "1.01", 1.01, "GREAT_THAN", False),
            ("INT", "10", 10, "IN", True),

            ("INT", 1, 2, "GE", False),
            ("INT", 1, 1, "GE", True),
            ("INT", "1", "2", "GE", False),
            ("INT", "1", "1", "GE", True),
            ("INT", "1", 1, "GREAT_OR_EQUAL_THAN", True),
            ("INT", 20, 10, "GREAT_OR_EQUAL_THAN", True),
            ("INT", "20", "10", "GREAT_OR_EQUAL_THAN", True),
            ("INT", 1048576, 1050768, "GREAT_OR_EQUAL_THAN", False),
            ("INT", "1.01", 1.01, "GREAT_OR_EQUAL_THAN", True),

            # mode, value_a, value_b, action, case_insensitive, expect_result
            ("STR", "HELLO", "HELLO WORLD", "IN", True, True),
            ("STRING", "hello", "Hey hello world", "IN", True, True),
            ("TEXT", "HELLO", "Hello", "IN", True, True),
            ("STR", "1", "number '1' in", "CONTAIN", True, True),
            ("STR", "HELLO", "I don't like you!", "CONTAIN", True, False),

            ("TEXT", "HELLO", "HELLO WORLD", "IN", False, True),
            ("STR", "1024, 65535", "[1024, 65535]", "IN", False, True),
            ("TEXT", "hello", "Hey Hello World", "IN", False, False),
            ("text", "HELLO", "Hello", "CONTAIN", False, False),
            ("text", "1", "number '1' in", "IN", False, True),

            # ("STRING", "HELLO", "HELLO WORLD", "EXACT", True, False),
            ("STRING", "HELLO", "Hello", "EQ", True, True),
            ("STRING", "1", "number '1' in", "EXACT", True, False),

            ("STR", "HELLO", "HELLO", "EQ", False, True),
            ("STR", "HELLO", "HELLO WORLD", "EQ", False, False),
            ("STR", "HELLO", "Hello", "EQ", False, False),
            ("STR", "1", "number '1' in", "EQ", False, False),
            ("DATE", "2016-12-30 18:00:00", "2017-12-30 18:00:00", "LT", True),
            ("DATE", "2016-12-30 18:00:00", "2017-12-30 18:00:00", "LE", True),
            ("TIME", "2016-12-30 18:00:00", "2017-12-30 18:00:00", "EXACT", False),
            ("TIME", "2016-12-30 18:00:00", "2016-12-30 18:00:00", "eq", True),
            ("TIME", "2016-12-30 18:00:00", "2017-12-30 18:00:00", "GT", False),
            ("TIME", "2018-12-30 18:00:00", "2017-12-30 18:00:00", "GE", True),
            ("TIME", "2018-12-30 18:00:00", "2017-12-30 18:00:00", "NE", True),
            ("TIME", "2017-12-30 18:00:00", "2017-12-30 18:00:00", "NE", False),
            ("DATE", "2016-12-30 18:00:00", "2015-12-30 18:00:00 ~ 2018-12-30 18:00:00", "IN", True),
            ("DATE", "2018-12-25 00:00:00", "2018-12-25 00:00:00", "EQ", True),
        )

        # got raise error
        invalid_material = (
            # mode, value_a, value_b, action,
            ("IPADDR", "129.0.0.1/54", "129.0.0.1/54", "EQ"),
            ("NETWORK", "100.1.1.356/32", "100.1.1.1/32", "NOT_EQUAL"),
            ("IP", "129.0.0.1/54", "129.0.0.1/54", "NOT_EQUAL"),
            ("IP", "100.1.1.356/32", "100.1.1.1/32", "IN"),
            ("IP", "129.0.0.1/54", "129.0.0.1/54", "CONTAIN"),
            ("IP", "192.168.1.1/124", "192.168.1.1/32", "IN"),
            ("IP", "192.168.1.1", "192.168.1.1", "GE"),
            ("IP", "192.168.1.1-192.168.1.10", "192.168.1.1", "IN"),
            ("IP", "192.168.1.1 ~ 10", "192.168.1.1", "IN"),
            ("IP", "192.168.1.1", "192.168.1.1-192.168.1.10~20", "IN"),
            ("IP", 10, 20, "GE"),
            ("UNKNOwn", "192.168.1.1/24", "192.168.1.1/32", "IN"),
            ("INT", "hello", 10, "LE"),
            ("INT", "1", 10, "LEESS_THAN"),
            ("INT", "1", 10, "LB"),
            ("NUMBER", "hello", 10, "LESS_OR_EQUAL"),
            ("INT", "10hello", 10, "EQUAL"),
            ("INT", "10hello", 10, "NOT_EQUAL"),
            ("INT", "10hello", 5, "GREAT_THAN"),
            ("INT", "10hello", 5, "GREAT_OR_EQUAL"),
            ("INT", 10, 5, "EXact"),
            ("STR", 1, 1, "IN"),
            ("TEXT", 1, 1, "IN"),
            ("STRING", 1, 1, "EQ"),
            ("STRING", "hello world", "hello", "ge"),
            ("STRING", 1, 1, "NE"),
            ("INT", "10-20", 15, "IN"),
            ("DATE", "2018-12-30 18:00:003251", "2018-12-30 18:00:003251", "EQ"),
            ("DATE", "2018-12-30", "2018-12-30", "EQ"),
            ("TIME", "2018-12-30 18:30:00", "2017-12-30~2019-12-30", "IN"),
            ("TIME", object, "2017-12-30", "IN"),
            ("TIME", "2017.12.30 18:30:00", "2017.12.30 18:30:00", "EQ"),
            ("TIME", "2017-12-30 18:30:00", "2017-12-30 18:30:00", "You Guess?"),
        )

        testcase = True
        for element in material:
            mode = element[0]
            if mode.upper() in ("STR", "TEXT", "STRING"):
                value_a = element[1]
                value_b = element[2]
                action = element[3]
                case_insensitive = element[4]
                expect_result = element[5]
            else:
                value_a = element[1]
                value_b = element[2]
                action = element[3]
                expect_result = element[4]
                case_insensitive = False

            result = self.ins.do_compare(
                value_a=value_a,
                value_b=value_b,
                mode=mode,
                case_insensitive=case_insensitive,
                action=action,
            )
            if result is expect_result:
                level = "INFO"
            else:
                level = "ERR"
                testcase = False

            print("{:>18s} <==> {:<18s} action: {:<18s} expect_result: {:<8s}".format(str(value_a), str(value_b), str(action), str(expect_result)))

        self.assertTrue(testcase)

        print("raise ValueError and have device object")
        for element in invalid_material:
            mode, value_a, value_b, action = element
            self.assertRaisesRegex(
                ValueError,
                r"",
                self.ins.do_compare,
                value_a=value_a,
                value_b=value_b,
                mode=mode,
                action=action,
                device=mock_device_ins,
            )

        print("do not raise ValueError and no device object")
        for element in invalid_material:
            mode, value_a, value_b, action = element

            self.assertFalse(self.ins.do_compare(
                value_a=value_a,
                value_b=value_b,
                mode=mode,
                action=action,
                device=None,
                raise_exception=False,
            ))


    def test_sleep(self):
        """checking CommonTool.sleep method"""
        result = self.ins.sleep(secs=0.1, msg="conf implements", add_title=False)
        self.assertTrue(result)

        result = self.ins.sleep(secs=0.1)
        self.assertTrue(result)

        result = self.ins.sleep(secs="0.1", msg="string int test")
        self.assertTrue(result)

    def test_sleep_with_wrong_option(self):
        """checking CommonTool.sleep method with wrong option"""
        result = self.ins.sleep(secs="aaa")
        self.assertFalse(result)

        result = self.ins.sleep(secs=None)
        self.assertFalse(result)

    def test_get_user_values(self):
        """checking get_user_values"""
        print("Normal checking")
        default_value_mode_action_dict = {
            # value: (default_value, default_check_mode, default_check_action)
            "blk_high_port":        (None, "INT", "eq"),
            "blk_low_port":         (None, "INT", "eq"),
            "blk_internal_ip":      (None, "IP", "eq"),
            "blk_ports_ol":         (None, "INT", "eq"),
            "blk_ports_total":      (None, "INT", "eq"),
            "blk_ports_used":       (None, "INT", "eq"),
            "blk_reflexive_ip":     (None, "IP", "eq"),
            "blk_new_node1":        (None, "STR", "in"),
            "blk_new_node2":        (None, "STR", "in"),
            "blk_new_node3":        (None, "INT", "eq"),
            "blk_new_node4":        (None, "IP", "IN"),
            "blk_new_node5":        (None, "STR", "in"),
        }

        user_value_dict = {
            "blk_high_port":        "1000 lt",
            "blk_low_port":         "2000-3000 in",
            "blk_internal_ip":      "192.168.10.0/24 in",
            "blk_ports_ol":         (1000, "eq"),
            "blk_ports_total":      ("2000", "gt"),
            "blk_ports_used":       ("3000-5000", "in"),
            "blk_reflexive_ip":     "192.168.100.1",
            "blk_new_node1":        "Hello world in",
            "blk_new_node2":        ("Hello world", "eq"),
            "unknown_str_user_value":   "1000",
            "unknown_list_user_value":  [1000, 'in'],
        }

        options = self.ins.get_user_values(default_value_mode_action_dict, user_value_dict)
        print(self.ins.pprint(options))

        self.assertTrue(options["blk_high_port"] == ("1000", "INT", "LT"))
        self.assertTrue(options["blk_low_port"] == ("2000-3000", "INT", "IN"))
        self.assertTrue(options["blk_internal_ip"] == ("192.168.10.0/24", "IP", "IN"))
        self.assertTrue(options["blk_ports_ol"] == (1000, "INT", "EQ"))
        self.assertTrue(options["blk_ports_total"] == ("2000", "INT", "GT"))
        self.assertTrue(options["blk_ports_used"] == ("3000-5000", "INT", "IN"))
        self.assertTrue(options["blk_reflexive_ip"] == ("192.168.100.1", "IP", "EQ"))
        self.assertTrue(options["blk_new_node1"] == ("Hello world", "STR", "IN"))
        self.assertTrue(options["blk_new_node2"] == ("Hello world", "STR", "EQ"))
        self.assertTrue(options["blk_new_node3"] == (None, "INT", "EQ"))
        self.assertTrue(options["blk_new_node4"] == (None, "IP", "IN"))
        self.assertTrue(options["blk_new_node5"] == (None, "STR", "IN"))
        self.assertTrue(options["unknown_str_user_value"] == ("1000", "STR", "EQ"))
        self.assertTrue(options["unknown_list_user_value"] == (1000, "STR", "IN"))


        print("check option 'delete_value_none_keyword'")
        options = self.ins.get_user_values(default_value_mode_action_dict, user_value_dict, delete_value_none_keyword=True)
        print(self.ins.pprint(options))
        self.assertTrue("blk_new_node3" not in options)
        self.assertTrue("blk_new_node4" not in options)
        self.assertTrue("blk_new_node5" not in options)

        print("Invalid user value")
        user_value_dict = {
            "blk_high_port":        None,
            "blk_low_port":         object,
        }
        self.assertRaisesRegex(
            ValueError,
            r"Unknown given value",
            self.ins.get_user_values,
            default_value_mode_action_dict, user_value_dict
        )

    def test_get_node_value(self):
        """UT Case"""
        check_point_list = (
            # user_value, mode, expect_result
            (0, "str", "node0"),
            ("0", "str", "node0"),
            (1, "str", "node1"),
            ("1", "str", "node1"),
            ("node0", "str", "node0"),
            ("node1", "str", "node1"),

            (0, "int", 0),
            ("0", "int", 0),
            (1, "int", 1),
            ("1", "int", 1),
            ("node0", "int", 0),
            ("node1", "int", 1),
        )
        for ele in check_point_list:
            self.assertTrue(self.ins.get_node_value(ele[0], mode=ele[1]) == ele[2])

        invalid_check_point_list = (
            (3, "str"),
            ("nodie0", "str"),
            (None, "int"),
        )
        for ele in invalid_check_point_list:
            case = False
            try:
                self.ins.get_node_value(ele[0], mode=ele[1])
            except ValueError:
                case = True
            self.assertTrue(case)

    @patch("builtins.open", read_data="data")
    @patch("requests.get")
    def test_download_file_by_http(self, mock_request_get, mock_file):
        """Test download file by http"""
        mock_request_get.return_value.status_code = 100

        dst_path = "/tmp/test_flow_common_tool_tmp"
        status = self.ins.download_file_by_http(url="http://simple_file.py", dst_path=dst_path)
        self.assertFalse(status)

        status = self.ins.download_file_by_http(url="http://simple_file.py", dst_path=dst_path, username="user", password="user")
        self.assertFalse(status)

        mock_request_get.return_value.status_code = 200
        mock_file.write.return_value = True
        status = self.ins.download_file_by_http(url="http://simple_file.py", dst_path=dst_path)
        self.assertTrue(status)

    def test_check_boolean(self):
        """UT Case"""
        self.assertTrue(self.ins.check_boolean(True))
        self.assertTrue(self.ins.check_boolean(value="True"))
        self.assertTrue(self.ins.check_boolean(value="TRUE"))

        self.assertFalse(self.ins.check_boolean(False))
        self.assertFalse(self.ins.check_boolean(value="False"))
        self.assertFalse(self.ins.check_boolean(value="FALSE"))

        self.assertEqual(self.ins.check_boolean(None), None)
        self.assertEqual(self.ins.check_boolean("NONE"), None)
        self.assertEqual(self.ins.check_boolean("none"), None)

        self.assertRaisesRegex(
            ValueError,
            r"Boolean string must be",
            self.ins.check_boolean,
            "Unknown",
        )

    def test_flat_dict(self):
        """UT Case"""
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

        self.assertEqual(
            self.ins.flat_dict(dict_variable=complex_dict),
            {
                'aaa_bbb_dd': 'bb',
                'aaa_ccc_ee': 'cc',
                'aaa_eee_fff': 'fff',
                'aaa_eee_ggg': 'GGG',
                'ddd': 'dd',
            }
        )

        self.assertEqual(
            self.ins.flat_dict(dict_variable=complex_dict, parent_key="snat"),
            {
                'snat_aaa_bbb_dd': 'bb',
                'snat_aaa_ccc_ee': 'cc',
                'snat_aaa_eee_fff': 'fff',
                'snat_aaa_eee_ggg': 'GGG',
                'snat_ddd': 'dd',
            }
        )

        self.assertEqual(
            self.ins.flat_dict(dict_variable=complex_dict, lowercase=False),
            {
                'aaa_BBB_dd': 'bb',
                'aaa_Ccc_ee': 'cc',
                'aaa_eee_fff': 'fff',
                'aaa_eee_ggg': 'GGG',
                'ddd': 'dd',
            }
        )

        self.assertEqual(
            self.ins.flat_dict(dict_variable=complex_dict, replace_dash_to_underline=False),
            {
                'aaa_bbb-dd': 'bb',
                'aaa_ccc_ee': 'cc',
                'aaa_eee_fff': 'fff',
                'aaa_eee_ggg': 'GGG',
                'ddd': 'dd',
            }
        )

    def test_create_verify_filters(self):
        """UT"""
        mock_device_ins = mock.Mock()

        print("normal checking for named option")
        named_options = {
                "in_src_addr": ["192.168.1.0/24", "in"],
                "in_dst_addr": "192.168.2.1",
                "in_src_port": "1024-65535 in",
                "in_dst_port": 21,
                "in_protocol": "tcp",
                "in_pkt_cnt": "10 gt",
                "sess_timeout": "20.5 - 30.5",
                "log_date": " 2020-03-02 18:00:00~2020-03-05 00:00:00 ",
                "not_wanted": None,
                "re_name": 1,
        }
        filters = self.ins.create_verify_filters(device=mock_device_ins, named_options=named_options, align_re_name=True, log_level="INFO")
        print("filters: \n{}".format(self.ins.pprint(filters)))
        self.assertEqual(filters["in_src_addr"], ("192.168.1.0/24", "IN", "IP"))
        self.assertEqual(filters["in_dst_addr"], ("192.168.2.1", "EQ", "IP"))
        self.assertEqual(filters["in_src_port"], ("1024-65535", "IN", "INT"))
        self.assertEqual(filters["in_dst_port"], ("21", "EQ", "INT"))
        self.assertEqual(filters["in_protocol"], ("tcp", "IN", "STR"))
        self.assertEqual(filters["in_pkt_cnt"], ("10", "GT", "INT"))
        self.assertEqual(filters["sess_timeout"], ("20.5 - 30.5", "IN", "FLOAT"))
        self.assertEqual(filters["log_date"], ("2020-03-02 18:00:00~2020-03-05 00:00:00", "IN", "DATE"))
        self.assertEqual(filters["re_name"], ("node1", "IN", "STR"))
        self.assertEqual(len(filters), 9)
        self.assertTrue("not_wanted" not in filters)

        print("check skip no element if value is None")
        named_options = {
            "node": 0,
            "aaa": None,
        }

        filters = self.ins.create_verify_filters(device=mock_device_ins, named_options=named_options, skip_for_none=True, debug_to_stdout=True)
        print("filters: \n{}".format(self.ins.pprint(filters)))
        self.assertEqual(filters["re_name"], ("node0", "IN", "STR"))
        self.assertTrue("aaa" not in filters)

        print("check special case for 'node'")
        named_options = {
            "node": None,
            "in_src_addr": None,
        }

        filters = self.ins.create_verify_filters(device=mock_device_ins, named_options=named_options, align_re_name=True, skip_for_none=False)
        print("filters: \n{}".format(self.ins.pprint(filters)))
        self.assertTrue("re_name" not in filters)
        self.assertEqual(filters["in_src_addr"], ("None", "IN", "STR"))

        print("illegal option")
        self.assertRaisesRegex(
            TypeError,
            r"must be STR, INT, FLOAT, LIST, TUPLE or None",
            self.ins.create_verify_filters,
            device=mock_device_ins, named_options={"illegal_value": re, }
        )

        print("align option keyword")
        named_options = {
                "in-src-ADDR": ["192.168.1.0/24", "in"],
                "in_dst-addr": "192.168.2.1",
                "IN_src_port": "1024-65535 in",
                "in_dst_port": 21,
                "In_Protocol": "tcp",
                "in_pkt_cnt": "10 gt",
                "SESS-TIMEOUT": "20.5 - 30.5",
                "log_date": " 2020-03-02 18:00:00~2020-03-05 00:00:00 ",
                "not_wanted": None,
                "re_name": 1,
        }
        filters = self.ins.create_verify_filters(device=mock_device_ins, named_options=named_options, align_re_name=True, align_option_keyword=True)
        print("filters: \n{}".format(self.ins.pprint(filters)))
        self.assertEqual(filters["in_src_addr"], ("192.168.1.0/24", "IN", "IP"))
        self.assertEqual(filters["in_dst_addr"], ("192.168.2.1", "EQ", "IP"))
        self.assertEqual(filters["in_src_port"], ("1024-65535", "IN", "INT"))
        self.assertEqual(filters["in_dst_port"], ("21", "EQ", "INT"))
        self.assertEqual(filters["in_protocol"], ("tcp", "IN", "STR"))
        self.assertEqual(filters["in_pkt_cnt"], ("10", "GT", "INT"))
        self.assertEqual(filters["sess_timeout"], ("20.5 - 30.5", "IN", "FLOAT"))
        self.assertEqual(filters["log_date"], ("2020-03-02 18:00:00~2020-03-05 00:00:00", "IN", "DATE"))
        self.assertEqual(filters["re_name"], ("node1", "IN", "STR"))
        self.assertEqual(len(filters), 9)
        self.assertTrue("not_wanted" not in filters)

    def test_filter_option_from_entry_list(self):
        mock_device_ins = mock.Mock()

        print("Normal testing")
        filters = {
            "blk_internal_ip": ("192.168.150.0", "IN", "IP"),
            "blk_low_port": ("1000", "GE", "INT"),
            "blk_ports_ol": ("1", "EQ", "INT"),
            "re_name": ("0", "IN", "STR"),
        }
        matched_entry_list = self.ins.filter_option_from_entry_list(
            device=mock_device_ins,
            filters=filters,
            entries=self.response["FILTER_OPTION_FROM_ENTRY_LIST_1"],
            index_option="blk_high_port",
            debug_to_stdout=True,
        )
        print(self.ins.pprint(matched_entry_list))
        self.assertTrue(matched_entry_list[0]["blk_high_port"] == "1151")
        self.assertTrue(matched_entry_list[0]["blk_internal_ip"] == "192.168.150.0")
        self.assertTrue(matched_entry_list[0]["blk_low_port"] == "1024")
        self.assertTrue(matched_entry_list[0]["blk_ports_ol"] == "1")
        self.assertTrue(matched_entry_list[0]["blk_ports_total"] == "128")
        self.assertTrue(matched_entry_list[0]["blk_ports_used"] == "0")
        self.assertTrue(matched_entry_list[0]["blk_reflexive_ip"] == "192.168.150.0")
        self.assertTrue(matched_entry_list[0]["re_name"] == "node0")

        print("Filter keyword is not exists in entry")
        filters = {
            "unknown": ("192.168.150.0", "IN", "IP"),
            "blk_low_port": ("1000", "GE", "INT"),
            "blk_ports_ol": ("1", "EQ", "INT"),
            "re_name": ("0", "IN", "STR"),
        }
        matched_entry_list = self.ins.filter_option_from_entry_list(
            device=mock_device_ins,
            filters=filters,
            entries=self.response["FILTER_OPTION_FROM_ENTRY_LIST_1"],
            index_option="blk_high_port",
            debug_to_stdout=True,
        )
        print(self.ins.pprint(matched_entry_list))
        self.assertTrue(matched_entry_list == list())

        print("Have compat_element_list")
        compat_element_list = (
            ["internal_ip", "blk_internal_ip"],
        )

        filters = {
            "blk_internal_ip": ("192.168.150.0", "IN", "IP"),
            "blk_low_port": ("1000", "GE", "INT"),
            "blk_ports_ol": ("1", "EQ", "INT"),
            "re_name": ("0", "IN", "STR"),
        }
        matched_entry_list = self.ins.filter_option_from_entry_list(
            device=mock_device_ins,
            compat_element_list=compat_element_list,
            filters=filters,
            entries=self.response["FILTER_OPTION_FROM_ENTRY_LIST_1"],
            index_option="blk_high_port",
            debug_to_stdout=True,
        )
        print(self.ins.pprint(matched_entry_list))
        self.assertTrue(matched_entry_list[0]["blk_high_port"] == "1151")
        self.assertTrue(matched_entry_list[0]["blk_internal_ip"] == "192.168.150.0")
        self.assertTrue(matched_entry_list[0]["internal_ip"] == "192.168.150.0")
        self.assertTrue(matched_entry_list[0]["blk_low_port"] == "1024")
        self.assertTrue(matched_entry_list[0]["blk_ports_ol"] == "1")
        self.assertTrue(matched_entry_list[0]["blk_ports_total"] == "128")
        self.assertTrue(matched_entry_list[0]["blk_ports_used"] == "0")
        self.assertTrue(matched_entry_list[0]["blk_reflexive_ip"] == "192.168.150.0")
        self.assertTrue(matched_entry_list[0]["re_name"] == "node0")


    def test_print_result_table(self):
        """UT case"""
        mock_device_ins = mock.Mock()

        print("Normal checking")
        filters = {
            "in_src_addr": ("192.168.1.0/24", "IN", "IP"),
            "in_dst_addr": ("192.168.2.1", "EQ", "IP"),
            "in_src_port": ("1024-65535", "IN", "INT"),
            "in_dst_port": ("21", "EQ", "INT"),
            "in_protocol": ("tcp", "IN", "STR"),
            "in_pkt_cnt": ("10", "GT", "INT"),
            "sess_timeout": ("20.5 - 30.5", "IN", "FLOAT"),
            "log_date": ("2020-03-02 18:00:00~2020-03-05 00:00:00", "IN", "DATE"),
        }
        entries = [
            {
                "in_src_addr": "192.168.1.0/24",
                "in_dst_addr": "192.168.2.1",
                "in_src_port": "1024-65535",
                "in_dst_port": "21",
                "in_protocol": "tcp",
                "in_pkt_cnt": "10",
                "sess_timeout": "20.5 - 30.5",
                "log_date": "2020-03-02 18:00:00~2020-03-05 00:00:00",
                "unknown_keyword_1": "1",
                "unknown_keyword_2": "1",
                "unknown_keyword_3": "1",
                "unknown_keyword_4": "1",
            },
            {
                "in_src_addr": "192.168.1.0/24",
                "in_dst_addr": "192.168.2.1",
                "in_src_port": "1024-65535",
                "in_dst_port": "22",
                "in_protocol": "tcp",
                "in_pkt_cnt": "10",
                "sess_timeout": "20.5 - 30.5",
                "log_date": "2020-03-02 18:00:00~2020-03-05 00:00:00",
                "unknown_keyword_1": "1",
                "unknown_keyword_2": "1",
                "unknown_keyword_3": "1",
                "unknown_keyword_4": "1",
            },
            {
                "in_src_addr": "192.168.1.0/24",
                "in_dst_addr": "192.168.2.1",
                "in_src_port": "1024-65535",
                "in_dst_port": "23",
                "in_protocol": "tcp",
                "in_pkt_cnt": "10",
                "sess_timeout": "20.5 - 30.5",
                "log_date": "2020-03-02 18:00:00~2020-03-05 00:00:00 2020-03-02 18:00:00~2020-03-05 00:00:00",
                "unknown_keyword_1": "1",
                "unknown_keyword_2": "1",
                "unknown_keyword_3": "1",
                "unknown_keyword_4": "1",
            },
        ]

        lines = self.ins.print_result_table(device=mock_device_ins, filters=filters, entries=entries, debug_to_stdout=True)
        self.assertTrue(re.match(r"Match entry", lines[0]))

        print("defind index name")
        lines = self.ins.print_result_table(device=mock_device_ins, filters=filters, entries=entries, index_option="in_dst_port", debug_to_stdout="TRUE")
        self.assertEqual(lines[0], "Match 'in_dst_port=21':")
