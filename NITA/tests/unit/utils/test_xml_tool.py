# coding: UTF-8
"""All unit test cases for XmlHandler"""
# pylint: disable=attribute-defined-outside-init,invalid-name,no-member

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import jxmlease
from lxml import etree
from unittest import TestCase, mock

from jnpr.toby.utils.xml_tool import xml_tool


class TestXmlTool(TestCase):
    """All unit test cases for XmlHandler"""
    def setUp(self):
        """setup before all case"""
        self.ins = xml_tool()

        self.response = {}

        self.response["SA_LE_XML_NORMAL"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <software-information>
                <host-name>qilianshan</host-name>
                <product-model>srx5600</product-model>
                <product-name>srx5600</product-name>
                <jsr/>
                <junos-version>15.1I20161030_x_151_x49.0-813072</junos-version>
                <package-information>
                    <name>junos</name>
                    <comment>JUNOS Software Release [15.1I20161030_x_151_x49.0-813072]</comment>
                </package-information>
            </software-information>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["SA_HE_XML_NORMAL"] = """
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

        self.response["HA_LE_XML_NORMAL"] = """
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

        self.response["HA_HE_XML_NORMAL"] = """
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


    def test_xml_obj_to_dict(self):
        """checking xml object to dict"""
        xml_obj = etree.fromstring(self.response["SA_LE_XML_NORMAL"])

        print("Transit XML object to dict")
        xml_dict = self.ins.xml_obj_to_dict(xml_obj=xml_obj)
        print(self.ins.pprint(xml_dict))
        # self.assertTrue(isinstance(xml_dict, (jxmlease.XMLDictNode, dict)))

    def test_xml_obj_to_string(self):
        """checking xml object to string"""
        import lxml
        xml_obj = lxml.etree.fromstring(self.response["SA_LE_XML_NORMAL"])

        print("Transit XML object to string")
        xml_string = self.ins.xml_obj_to_string(xml_obj=xml_obj)
        print(self.ins.pprint(xml_string))
        # self.assertRegex(xml_string, r'xml version="1\.0"')

    def test_xml_string_to_dict(self):
        """checking xml string to dict"""
        print("Transit XML string to dict")
        xml_dict = self.ins.xml_string_to_dict(xml_str=self.response["SA_LE_XML_NORMAL"])
        print(self.ins.pprint(xml_dict))
        self.assertIn("software-information", xml_dict["rpc-reply"])

    def test_xml_to_pure_dict(self):
        """UT Case"""
        print("XML string to dict")
        xml_response = self.ins.xml_to_pure_dict(xml_structure=self.response["HA_HE_XML_NORMAL"], pprint=True)
        self.assertIsInstance(xml_response, dict)
        self.assertTrue("rpc-reply" in xml_response)

        print("JXMLEASE object to dict")
        xml_response = self.ins.xml_to_pure_dict(xml_structure=self.ins.xml_str_to_dict(xml_str=self.response["SA_HE_XML_NORMAL"]), pprint=True)
        self.assertIsInstance(xml_response, dict)
        self.assertTrue("rpc-reply" in xml_response)

        print("LXML object to dict")
        xml_response = self.ins.xml_to_pure_dict(xml_structure=etree.fromstring(self.response["SA_HE_XML_NORMAL"]), pprint=True)
        self.assertIsInstance(xml_response, dict)
        # self.assertTrue("rpc-reply" in xml_response or "multi-routing-engine-results"in xml_response)

        print("DICT to DICT")
        xml_response = self.ins.xml_to_pure_dict(xml_structure=xml_response, pprint=True)
        self.assertIsInstance(xml_response, dict)
        # self.assertTrue("rpc-reply" in xml_response or "multi-routing-engine-results"in xml_response)

        print("Unknown object")
        self.assertRaisesRegex(
            ValueError,
            r"Given xml_structure must be",
            self.ins.xml_to_pure_dict,
            self.ins,
        )

        print("special xml object")
        for obj in (None, True, False):
            self.assertEqual(self.ins.xml_to_pure_dict(obj), obj)


    def test_strip_xml_response(self):
        """UT Case"""
        print("strip SA HE response")
        result = self.ins.strip_xml_response(xml_response = self.ins.xml_string_to_dict(xml_str=self.response["SA_HE_XML_NORMAL"]))
        print(self.ins.pprint(result))
        self.assertTrue("flow-session-information" in result[0])

        print("strip SA LE response")
        result = self.ins.strip_xml_response(xml_response = self.ins.xml_string_to_dict(xml_str=self.response["SA_LE_XML_NORMAL"]))
        print(self.ins.pprint(result))
        self.assertTrue("software-information" in result[0])

        print("strip HA HE response")
        result = self.ins.strip_xml_response(xml_response = self.ins.xml_string_to_dict(xml_str=self.response["HA_HE_XML_NORMAL"]))
        print(self.ins.pprint(result))
        self.assertTrue("re-name" in result[0])
        self.assertTrue("flow-session-information" in result[0])

        print("strip HA LE response")
        result = self.ins.strip_xml_response(xml_response = self.ins.xml_string_to_dict(xml_str=self.response["HA_LE_XML_NORMAL"]))
        print(self.ins.pprint(result))
        self.assertTrue("re-name" in result[0])
        self.assertTrue("flow-session-information" in result[0])

        print("change rpc-reply keyword")
        result = self.ins.strip_xml_response(
            xml_response = self.ins.xml_string_to_dict(xml_str=self.response["HA_LE_XML_NORMAL"]),
            rpc_tag="unknown",
        )
        print(self.ins.pprint(result))
        self.assertTrue("rpc-reply" in result[0])

        print("change ha keyword")
        result = self.ins.strip_xml_response(
            xml_response = self.ins.xml_string_to_dict(xml_str=self.response["HA_LE_XML_NORMAL"]),
            ha_keyword="unknown",
        )
        print(self.ins.pprint(result))
        self.assertTrue("multi-routing-engine-results" in result[0])

        print("strip HA pyez response")
        result = self.ins.strip_xml_response(xml_response=self.ins.xml_string_to_dict(xml_str=self.response["HA_LE_FLOW_SESSION_BY_PYEZ"]))
        print(self.ins.pprint(result))
        self.assertTrue("flow-session-information" in result[0])

        print("strip SA pyez response")
        result = self.ins.strip_xml_response(xml_response=self.ins.xml_string_to_dict(xml_str=self.response["SA_LE_FLOW_SESSION_SUMMARY_BY_PYEZ"]))
        print(self.ins.pprint(result))
        self.assertTrue("flow-session-summary-information" in result[0])
