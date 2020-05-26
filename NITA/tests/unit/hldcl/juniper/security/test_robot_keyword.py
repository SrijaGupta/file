"""All UT cases"""
# pylint: disable=too-many-arguments,invalid-name,too-many-statements

import unittest2 as unittest
import mock
import builtins

from jnpr.toby.init.init import init
from jnpr.toby.hldcl import device as dev
from jnpr.toby.hldcl.juniper.security import robot_keyword as ins
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem
from jnpr.toby.hldcl.system import System


class TestRobotKeyword(unittest.TestCase):
    """Test Class"""
    def setUp(self):
        """Setup"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()

        self.response = {}
        self.response["NORMAL_IPV4_LOOP_PING"] = """
        PING 1.1.1.2 (1.1.1.2) 56(84) bytes of data.
        64 bytes from 1.1.1.2: icmp_seq=1 ttl=64 time=0.151 ms
        64 bytes from 1.1.1.2: icmp_seq=2 ttl=64 time=0.034 ms
        64 bytes from 1.1.1.2: icmp_seq=3 ttl=64 time=0.068 ms
        ^C
        --- 1.1.1.2 ping statistics ---
        3 packets transmitted, 3 received, 0% packet loss, time 2239ms
        rtt min/avg/max/mdev = 0.034/0.084/0.151/0.049 ms
        """

        self.response["NORMAL_IPV6_LOOP_PING"] = """
        PING 2011::2(2011::2) 56 data bytes
        64 bytes from 2011::2: icmp_seq=1 ttl=64 time=3.75 ms
        64 bytes from 2011::2: icmp_seq=2 ttl=64 time=0.047 ms
        64 bytes from 2011::2: icmp_seq=3 ttl=64 time=0.048 ms
        ^C
        --- 2011::2 ping statistics ---
        3 packets transmitted, 3 received, 0% packet loss, time 2884ms
        rtt min/avg/max/mdev = 0.047/1.283/3.755/1.747 ms
        """

        self.response["IPV4_PING_FAILED"] = """
        PING 1.1.1.3 (1.1.1.3) 56(84) bytes of data.
        From 1.1.1.2 icmp_seq=2 Destination Host Unreachable
        From 1.1.1.2 icmp_seq=3 Destination Host Unreachable
        From 1.1.1.2 icmp_seq=4 Destination Host Unreachable
        ^C
        --- 1.1.1.3 ping statistics ---
        6 packets transmitted, 0 received, +3 errors, 100% packet loss, time 5534ms
        pipe 3
        """

        self.response["IPV6_PING_FAILED"] = """
        PING 2000:200::3(2000:200::3) 56 data bytes
        From 2000:100::1 icmp_seq=1 Destination unreachable: Address unreachable
        From 2000:100::1 icmp_seq=5 Destination unreachable: Address unreachable
        ^C
        --- 2000:200::3 ping statistics ---
        7 packets transmitted, 0 received, +2 errors, 100% packet loss, time 6556ms
        """

        self.response["SRX_IPV4_PING"] = """
PING 121.11.10.2 (121.11.10.2): 56 data bytes
64 bytes from 121.11.10.2: icmp_seq=0 ttl=64 time=1.109 ms
64 bytes from 121.11.10.2: icmp_seq=1 ttl=64 time=1.308 ms
64 bytes from 121.11.10.2: icmp_seq=2 ttl=64 time=1.005 ms
^C
--- 121.11.10.2 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max/stddev = 1.005/1.141/1.308/0.126 ms
        """

        self.response["get_interface_hardware_address_ha_normal_response_xml"] = """
    <interface-information xmlns="http://xml.juniper.net/junos/19.1I0/junos-interface" junos:style="normal">
        <physical-interface>
            <name>ge-0/0/1</name>
            <admin-status junos:format="Enabled">up</admin-status>
            <oper-status>up</oper-status>
            <local-index>144</local-index>
            <snmp-index>516</snmp-index>
            <link-level-type>Ethernet</link-level-type>
            <mtu>1514</mtu>
            <sonet-mode>LAN-PHY</sonet-mode>
            <source-filtering>disabled</source-filtering>
            <link-mode>Half-duplex</link-mode>
            <speed>1000mbps</speed>
            <eth-switch-error>none</eth-switch-error>
            <bpdu-error>none</bpdu-error>
            <ld-pdu-error>none</ld-pdu-error>
            <l2pt-error>none</l2pt-error>
            <loopback>disabled</loopback>
            <if-flow-control>disabled</if-flow-control>
            <if-auto-negotiation>enabled</if-auto-negotiation>
            <if-remote-fault>online</if-remote-fault>

            <if-device-flags>
                <ifdf-present/>
                <ifdf-running/>
            </if-device-flags>
            <if-config-flags>
                <iff-snmp-traps/>
                <internal-flags>0x4000</internal-flags>
            </if-config-flags>
            <if-media-flags>
                <ifmf-none/>
            </if-media-flags>
            <physical-interface-cos-information>
                <physical-interface-cos-hw-max-queues>8</physical-interface-cos-hw-max-queues>
                <physical-interface-cos-use-max-queues>8</physical-interface-cos-use-max-queues>
            </physical-interface-cos-information>
            <current-physical-address>00:10:db:ff:10:01</current-physical-address>
            <hardware-physical-address>4c:96:14:e9:58:01</hardware-physical-address>
            <interface-flapped junos:seconds="327458">2019-05-09 16:47:17 CST (3d 18:57 ago)</interface-flapped>
            <traffic-statistics junos:style="brief">
                <input-bps>0</input-bps>
                <input-pps>0</input-pps>
                <output-bps>0</output-bps>
                <output-pps>0</output-pps>
            </traffic-statistics>
            <active-alarms>
                <interface-alarms>
                    <alarm-not-present/>
                </interface-alarms>
            </active-alarms>
            <active-defects>
                <interface-alarms>
                    <alarm-not-present/>
                </interface-alarms>
            </active-defects>
            <ethernet-pcs-statistics junos:style="verbose">
                <bit-error-seconds>0</bit-error-seconds>
                <errored-blocks-seconds>0</errored-blocks-seconds>
            </ethernet-pcs-statistics>
            <ethernet-fec-mode junos:style="verbose">
                <enabled_fec_mode></enabled_fec_mode>
            </ethernet-fec-mode>
            <ethernet-fec-statistics junos:style="verbose">
                <fec_ccw_count>0</fec_ccw_count>
                <fec_nccw_count>0</fec_nccw_count>
                <fec_ccw_error_rate>0</fec_ccw_error_rate>
                <fec_nccw_error_rate>0</fec_nccw_error_rate>
            </ethernet-fec-statistics>
            <interface-transmit-statistics>Disabled</interface-transmit-statistics>
            <logical-interface>
                <name>ge-0/0/1.0</name>
                <local-index>70</local-index>
                <snmp-index>539</snmp-index>
                <if-config-flags>
                    <iff-up/>
                    <iff-snmp-traps/>
                    <internal-flags>0x4000</internal-flags>
                </if-config-flags>
                <encapsulation>ENET2</encapsulation>
                <policer-overhead>
                </policer-overhead>
                <traffic-statistics junos:style="brief">
                    <input-packets>1023</input-packets>
                    <output-packets>1291</output-packets>
                </traffic-statistics>
                <filter-information>
                </filter-information>
                <logical-interface-zone-name>Null</logical-interface-zone-name>
                <allowed-host-inbound-traffic>
                </allowed-host-inbound-traffic>
                <address-family>
                    <address-family-name>aenet</address-family-name>
                    <ae-bundle-name>reth1.0   Link Index: 0</ae-bundle-name>
                </address-family>
            </logical-interface>
        </physical-interface>
    </interface-information>
        """

        self.response["get_interface_hardware_address_ha_error_response_xml"] = """
<interface-information style="normal">
<rpc-error>
<error-type>protocol</error-type>
<error-tag>operation-failed</error-tag>
<error-severity>error</error-severity>
<source-daemon>
ifinfo
</source-daemon>
<error-message>
device ge-1/0/1 not found
</error-message>
</rpc-error>
</interface-information>
        """

        self.response["get_interface_hardware_address_host_normal_response"] = """
eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 121.11.10.2  netmask 255.255.255.0  broadcast 121.11.10.255
        inet6 2000:121:11:10::2  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::250:56ff:fe31:baae  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:31:ba:ae  txqueuelen 1000  (Ethernet)
        RX packets 67365  bytes 21530610 (20.5 MiB)
        RX errors 0  dropped 254  overruns 0  frame 0
        TX packets 234691  bytes 522910119 (498.6 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        """

        self.response["get_interface_hardware_address_host_error_response"] = """
ge-0/0/1: error fetching interface information: Device not found
        """

        self.response["check_vmhost_le_ha_response"] = {
            "multi-routing-engine-results": {
                "multi-routing-engine-item": {
                    "chassis-inventory": {
                        "chassis": {
                            "chassis-module": [
                                {
                                    "description": "VSRX",
                                    "name": "Midplane",
                                    "part-number": "750-058562",
                                    "serial-number": "42305991",
                                    "version": "REV 08"
                                },
                                {
                                    "name": "Pseudo CB 0"
                                },
                                {
                                    "description": "VSRX-L",
                                    "name": "Routing Engine 0",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN"
                                },
                                {
                                    "chassis-sub-module": {
                                        "description": "VSRX DPDK GE",
                                        "name": "PIC 0",
                                        "part-number": "BUILTIN",
                                        "serial-number": "BUILTIN",
                                        "version": ""
                                    },
                                    "description": "FPC",
                                    "name": "FPC 0",
                                    "part-number": "611-049549",
                                    "serial-number": "RL3714040884",
                                    "version": "REV 07"
                                }
                            ],
                            "description": "VSRX",
                            "name": "Chassis",
                            "serial-number": "14D3760EE3DC"
                        }
                    },
                    "re-name": "node0"
                }
            }
        }

        self.response["check_vmhost_he_ha_re3_response"] = {
            "multi-routing-engine-results": {
                "multi-routing-engine-item": {
                    "chassis-inventory": {
                        "chassis": {
                            "chassis-module": [
                                {
                                    "description": "SRX5600 Midplane",
                                    "model-number": "SRX5600-MP-A",
                                    "name": "Midplane",
                                    "part-number": "710-024804",
                                    "serial-number": "ABAB8221",
                                    "version": "REV 01"
                                },
                                {
                                    "description": "Front Panel Display",
                                    "model-number": "SRX5600-CRAFT-A",
                                    "name": "FPM Board",
                                    "part-number": "710-024631",
                                    "serial-number": "YP7140",
                                    "version": "REV 01"
                                },
                                {
                                    "description": "PS 1.4-2.6kW; 90-264V AC in",
                                    "model-number": "SRX5600-PWR-2520-AC-S",
                                    "name": "PEM 0",
                                    "part-number": "740-034701",
                                    "serial-number": "QCS15060902A",
                                    "version": "Rev 03"
                                },
                                {
                                    "description": "PS 1.4-2.6kW; 90-264V AC in",
                                    "model-number": "SRX5600-PWR-2520-AC-S",
                                    "name": "PEM 1",
                                    "part-number": "740-034701",
                                    "serial-number": "QCS150609044",
                                    "version": "Rev 03"
                                },
                                {
                                    "clei-code": "PROTOXCLEI",
                                    "description": "SRX5k RE-2000x6",
                                    "model-number": "SRX5K-RE3-128G",
                                    "name": "Routing Engine 0",
                                    "part-number": "750-095568",
                                    "serial-number": "CALY4279",
                                    "version": "REV 01"
                                },
                                {
                                    "clei-code": "COUCAVVBAA",
                                    "description": "SRX5k SCB4",
                                    "model-number": "SRX5K-SCB4",
                                    "name": "CB 0",
                                    "part-number": "750-095572",
                                    "serial-number": "CANA2559",
                                    "version": "REV 04"
                                },
                                {
                                    "chassis-sub-module": [
                                        {
                                            "description": "SRX5k vCPP Broadwell",
                                            "name": "CPU",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN",
                                            "version": ""
                                        },
                                        {
                                            "description": "SPU Cp-Flow",
                                            "name": "PIC 0",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN"
                                        },
                                        {
                                            "description": "SPU Flow",
                                            "name": "PIC 1",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN"
                                        }
                                    ],
                                    "clei-code": "CMUCALECAA",
                                    "description": "SPC3",
                                    "model-number": "JNP-SPC3",
                                    "name": "FPC 1",
                                    "part-number": "750-073435",
                                    "serial-number": "CALS4645",
                                    "version": "REV 28"
                                },
                                {
                                    "chassis-sub-module": [
                                        {
                                            "description": "SRX5k DPC PPC",
                                            "name": "CPU",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN",
                                            "version": ""
                                        },
                                        {
                                            "description": "SPU Flow",
                                            "name": "PIC 0",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN"
                                        },
                                        {
                                            "description": "SPU Flow",
                                            "name": "PIC 1",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN"
                                        },
                                        {
                                            "description": "SPU Flow",
                                            "name": "PIC 2",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN"
                                        },
                                        {
                                            "description": "SPU Flow",
                                            "name": "PIC 3",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN"
                                        }
                                    ],
                                    "clei-code": "COUCASFBAA",
                                    "description": "SRX5k SPC II",
                                    "model-number": "SRX5K-SPC-4-15-320",
                                    "name": "FPC 2",
                                    "part-number": "750-044175",
                                    "serial-number": "CABA3243",
                                    "version": "REV 15"
                                },
                                {
                                    "chassis-sub-module": [
                                        {
                                            "description": "SMPC PMB",
                                            "name": "CPU",
                                            "part-number": "750-057177",
                                            "serial-number": "CALK1076",
                                            "version": "REV 21"
                                        },
                                        {
                                            "chassis-sub-sub-module": [
                                                {
                                                    "description": "QSFP+-4X10G-SR",
                                                    "name": "Xcvr 0",
                                                    "part-number": "740-054053",
                                                    "serial-number": "X0JA6ZH",
                                                    "version": "REV 01"
                                                },
                                                {
                                                    "description": "QSFP+-4X10G-SR",
                                                    "name": "Xcvr 1",
                                                    "part-number": "740-054053",
                                                    "serial-number": "X0JA711",
                                                    "version": "REV 01"
                                                },
                                                {
                                                    "description": "QSFP+-4X10G-SR",
                                                    "name": "Xcvr 3",
                                                    "part-number": "740-054053",
                                                    "serial-number": "X0JA6ZJ",
                                                    "version": "REV 01"
                                                }
                                            ],
                                            "description": "MRATE-6xQSFPP-XGE-XLGE-CGE",
                                            "name": "PIC 0",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN"
                                        },
                                        {
                                            "chassis-sub-sub-module": {
                                                "description": "QSFP+-4X10G-SR",
                                                "name": "Xcvr 0",
                                                "part-number": "740-054053",
                                                "serial-number": "X0JA6Z7",
                                                "version": "REV 01"
                                            },
                                            "description": "MRATE-6xQSFPP-XGE-XLGE-CGE",
                                            "name": "PIC 1",
                                            "part-number": "BUILTIN",
                                            "serial-number": "BUILTIN"
                                        }
                                    ],
                                    "description": "SRX5k IOC4 MRATE",
                                    "name": "FPC 3",
                                    "part-number": "750-095443",
                                    "serial-number": "CALM0833",
                                    "version": "REV 46"
                                },
                                {
                                    "chassis-sub-module": [
                                        {
                                            "description": "SRX5k MPC PMB",
                                            "name": "CPU",
                                            "part-number": "711-061263",
                                            "serial-number": "CAHD1946",
                                            "version": "REV 03"
                                        },
                                        {
                                            "chassis-sub-sub-module": {
                                                "chassis-sub-sub-sub-module": [
                                                    {
                                                        "description": "SFP+-10G-SR",
                                                        "name": "Xcvr 0",
                                                        "part-number": "740-031980",
                                                        "serial-number": "CF05KN52J",
                                                        "version": "REV 01"
                                                    },
                                                    {
                                                        "description": "SFP+-10G-SR",
                                                        "name": "Xcvr 1",
                                                        "part-number": "740-031980",
                                                        "serial-number": "CF07KN06K",
                                                        "version": "REV 01"
                                                    },
                                                    {
                                                        "description": "SFP+-10G-SR",
                                                        "name": "Xcvr 2",
                                                        "part-number": "740-031980",
                                                        "serial-number": "CF07KN021",
                                                        "version": "REV 01"
                                                    },
                                                    {
                                                        "description": "SFP+-10G-SR",
                                                        "name": "Xcvr 3",
                                                        "part-number": "740-031980",
                                                        "serial-number": "CF07KN06R",
                                                        "version": "REV 01"
                                                    }
                                                ],
                                                "description": "10x 10GE SFP+",
                                                "name": "PIC 0",
                                                "part-number": "BUILTIN",
                                                "serial-number": "BUILTIN"
                                            },
                                            "clei-code": "COUIBD9BAA",
                                            "description": "10x 10GE SFP+",
                                            "model-number": "SRX-MIC-10XG-SFPP",
                                            "name": "MIC 0",
                                            "part-number": "750-049488",
                                            "serial-number": "CAJF6453",
                                            "version": "REV 11"
                                        }
                                    ],
                                    "clei-code": "COUIBCWBAE",
                                    "description": "SRX5k IOC II",
                                    "model-number": "SRX5K-MPC",
                                    "name": "FPC 4",
                                    "part-number": "750-061262",
                                    "serial-number": "CAHB3019",
                                    "version": "REV 09"
                                },
                                {
                                    "description": "Enhanced Fan Tray",
                                    "model-number": "SRX5600-HC-FAN",
                                    "name": "Fan Tray"
                                }
                            ],
                            "description": "SRX5600",
                            "name": "Chassis",
                            "serial-number": "JN11C334CAGB"
                        }
                    },
                    "re-name": "node0"
                }
            }
        }

        self.response["check_vmhost_he_sa_response"] = {
            "chassis-inventory": {
                "chassis": {
                    "chassis-module": [
                        {
                            "description": "SRX5600 Midplane",
                            "model-number": "SRX5600-MP-A",
                            "name": "Midplane",
                            "part-number": "710-024804",
                            "serial-number": "ABAB6166",
                            "version": "REV 01"
                        },
                        {
                            "description": "Front Panel Display",
                            "model-number": "SRX5600-CRAFT-A",
                            "name": "FPM Board",
                            "part-number": "710-024631",
                            "serial-number": "ZJ9180",
                            "version": "REV 01"
                        },
                        {
                            "description": "PS 1.4-2.6kW; 90-264V AC in",
                            "model-number": "SRX5600-PWR-2520-AC-S",
                            "name": "PEM 0",
                            "part-number": "740-034701",
                            "serial-number": "QCS13320901P",
                            "version": "Rev 03"
                        },
                        {
                            "description": "PS 1.4-2.6kW; 90-264V AC in",
                            "model-number": "SRX5600-PWR-2520-AC-S",
                            "name": "PEM 1",
                            "part-number": "740-034701",
                            "serial-number": "QCS13320901Z",
                            "version": "Rev 03"
                        },
                        {
                            "clei-code": "COUCATTBAB",
                            "description": "SRX5k RE-1800X4",
                            "model-number": "SRX5K-RE-1800X4",
                            "name": "Routing Engine 0",
                            "part-number": "740-056658",
                            "serial-number": "9013142621",
                            "version": "REV 03"
                        },
                        {
                            "clei-code": "FWUCAAKAAB",
                            "description": "SRX5k SCB3",
                            "model-number": "SRX5K-SCB3",
                            "name": "CB 0",
                            "part-number": "750-066337",
                            "serial-number": "CAGK2202",
                            "version": "REV 03"
                        },
                        {
                            "chassis-sub-module": [
                                {
                                    "description": "SRX5k vCPP Broadwell",
                                    "name": "CPU",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN",
                                    "version": ""
                                },
                                {
                                    "description": "SPU Cp-Flow",
                                    "name": "PIC 0",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN"
                                },
                                {
                                    "description": "SPU Flow",
                                    "name": "PIC 1",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN"
                                }
                            ],
                            "clei-code": "CMUCALECAC",
                            "description": "SPC3",
                            "model-number": "JNP-SPC3",
                            "name": "FPC 1",
                            "part-number": "750-073435",
                            "serial-number": "CAND7957",
                            "version": "REV 31"
                        },
                        {
                            "chassis-sub-module": [
                                {
                                    "description": "SMPC PMB",
                                    "name": "CPU",
                                    "part-number": "750-100223",
                                    "serial-number": "CANK6006",
                                    "version": "REV 05"
                                },
                                {
                                    "chassis-sub-sub-module": [
                                        {
                                            "description": "SFP+-10G-SR",
                                            "name": "Xcvr 0",
                                            "part-number": "740-031980",
                                            "serial-number": "AA15093MYFS",
                                            "version": "REV 01"
                                        },
                                        {
                                            "description": "SFP+-10G-SR",
                                            "name": "Xcvr 1",
                                            "part-number": "740-031980",
                                            "serial-number": "AA15093MYV7",
                                            "version": "REV 01"
                                        },
                                        {
                                            "description": "SFP+-10G-SR",
                                            "name": "Xcvr 2",
                                            "part-number": "740-031980",
                                            "serial-number": "AA15093MYFT",
                                            "version": "REV 01"
                                        },
                                        {
                                            "description": "SFP+-10G-SR",
                                            "name": "Xcvr 3",
                                            "part-number": "740-031980",
                                            "serial-number": "AA15073MM8Z",
                                            "version": "REV 01"
                                        },
                                        {
                                            "description": "SFP+-10G-SR",
                                            "name": "Xcvr 4",
                                            "part-number": "740-021308",
                                            "serial-number": "AD153530133",
                                            "version": "REV 01"
                                        },
                                        {
                                            "description": "SFP+-10G-SR",
                                            "name": "Xcvr 5",
                                            "part-number": "740-021308",
                                            "serial-number": "AD150130560",
                                            "version": "REV 01"
                                        },
                                        {
                                            "description": "SFP+-10G-SR",
                                            "name": "Xcvr 9",
                                            "part-number": "740-031980",
                                            "serial-number": "AA15093MYVU",
                                            "version": "REV 01"
                                        }
                                    ],
                                    "description": "20x10GE SFPP",
                                    "name": "PIC 0",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN"
                                },
                                {
                                    "description": "20x10GE SFPP",
                                    "name": "PIC 1",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN"
                                }
                            ],
                            "clei-code": "COUCAVTBAA",
                            "description": "SRX5k IOC4 10G",
                            "model-number": "SRX5K-IOC4-10G",
                            "name": "FPC 2",
                            "part-number": "750-095565",
                            "serial-number": "CANB0269",
                            "version": "REV 10"
                        },
                        {
                            "chassis-sub-module": {
                                "description": "SRX5k DPC PPC",
                                "name": "CPU",
                                "part-number": "BUILTIN",
                                "serial-number": "BUILTIN",
                                "version": ""
                            },
                            "clei-code": "PROTOXCLEI",
                            "description": "SRX5k SPC II",
                            "model-number": "750-044175",
                            "name": "FPC 3",
                            "part-number": "750-044175",
                            "serial-number": "ZZ1374",
                            "version": "REV 05"
                        },
                        {
                            "chassis-sub-module": {
                                "description": "SRX5k DPC PPC",
                                "name": "CPU",
                                "part-number": "BUILTIN",
                                "serial-number": "BUILTIN",
                                "version": ""
                            },
                            "clei-code": "COUCASFBAA",
                            "description": "SRX5k SPC II",
                            "model-number": "SRX5K-SPC-4-15-320",
                            "name": "FPC 4",
                            "part-number": "750-044175",
                            "serial-number": "CABA6924",
                            "version": "REV 14"
                        },
                        {
                            "description": "Enhanced Fan Tray",
                            "model-number": "SRX5600-HC-FAN",
                            "name": "Fan Tray"
                        }
                    ],
                    "description": "SRX5600",
                    "name": "Chassis",
                    "serial-number": "JN11BC1EFAGB"
                }
            }
        }

        self.response["check_vmhost_not_list_component_response"] = {
            "multi-routing-engine-results": {
                "multi-routing-engine-item": {
                    "chassis-inventory": {
                        "chassis": {
                            "chassis-module": {
                                    "description": "VSRX",
                                    "name": "Midplane",
                                    "part-number": "750-058562",
                                    "serial-number": "42305991",
                                    "version": "REV 08"
                                },
                            "description": "VSRX",
                            "name": "Chassis",
                            "serial-number": "14D3760EE3DC"
                        }
                    },
                    "re-name": "node0"
                }
            }
        }

    def test_check_feature_support(self):
        """Unit Test"""
        dev_object = mock.Mock()
        dev_object.check_feature_support.return_value = True

        self.assertTrue(ins.check_feature_support(device=dev_object, feature="HE"))

    def test_do_failover(self):
        """Unit Test"""
        dev_object = mock.Mock()
        dev_object.do_failover.return_value = True

        self.assertTrue(ins.do_failover(device=dev_object))

    def test_get_tnpdump_info(self):
        """Unit Test"""
        dev_object = mock.Mock()
        dev_object.get_tnpdump_info.return_value = True

        self.assertTrue(ins.get_tnpdump_info(device=dev_object))

    def test_get_version_info(self):
        """Unit Test"""
        dev_object = mock.Mock()
        dev_object.get_version_info.return_value = True

        self.assertTrue(ins.get_version_info(device=dev_object))

    def test_ha_switch_to_primary_node(self):
        """UT Case"""
        dev_object = mock.Mock()
        dev_object.switch_to_primary_node.return_value = True
        self.assertTrue(ins.ha_switch_to_primary_node(device=dev_object))

    @mock.patch("time.sleep")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_loop_ping(self, mock_execute_shell_command_on_device, _):
        """test loop ping"""
        dev_object = mock.Mock()
        dev_object.get_model.return_value = "linux"
        dev_object.log.return_value = None

        print("do IPv4 loop ping as normal")
        mock_execute_shell_command_on_device.return_value = self.response["NORMAL_IPV4_LOOP_PING"]
        status = ins.loop_ping(
            device=dev_object,
            dst_addr="1.1.1.2",
            ping_counter=10,
            ping_option="-c 5",
            loop_cnt=5,
            loop_interval=10,
            get_detail=False,
        )
        self.assertTrue(status)

        print("do IPv6 loop ping as normal")
        mock_execute_shell_command_on_device.return_value = self.response["NORMAL_IPV6_LOOP_PING"]
        status = ins.loop_ping(
            device=dev_object,
            dst_addr="2011::2",
            ping_counter=10,
            ping_option="-c 5",
            loop_cnt=5,
            loop_interval=10,
            get_detail=False,
        )
        self.assertTrue(status)

        print("check get detail info")
        mock_execute_shell_command_on_device.side_effect = [
            self.response["IPV4_PING_FAILED"],
            self.response["IPV4_PING_FAILED"],
            self.response["IPV4_PING_FAILED"],
            self.response["IPV4_PING_FAILED"],
            self.response["NORMAL_IPV4_LOOP_PING"],
        ]
        response = ins.loop_ping(
            device=dev_object,
            dst_addr="1.1.1.2",
            ping_counter=10,
            ping_option="-c 5",
            loop_cnt=5,
            loop_interval=10,
            get_detail=True,
        )
        self.assertTrue(response["transmitted"] == 3)
        self.assertTrue(response["received"] == 3)
        self.assertTrue(response["lost_rate"] == 0)
        self.assertTrue(response["min"] == 0.034)
        self.assertTrue(response["avg"] == 0.084)
        self.assertTrue(response["max"] == 0.151)
        self.assertTrue(response["mdev"] == 0.049)

        print("check with ping failed")
        mock_execute_shell_command_on_device.side_effect = [
            self.response["IPV4_PING_FAILED"],
        ]
        status = ins.loop_ping(
            device=dev_object,
            dst_addr="1.1.1.3",
            ping_counter=10,
            ping_option="-c 5",
            loop_cnt=1,
            loop_interval=0.01,
            get_detail=False,
        )
        self.assertFalse(status)

        print("accident check")
        mock_execute_shell_command_on_device.side_effect = [
            "Network is unreachable",
            "Network is unreachable",
            self.response["IPV4_PING_FAILED"],
        ]
        status = ins.loop_ping(
            device=dev_object,
            dst_addr="1.1.1.3",
            ping_counter=10,
            ping_option="-c 5",
            loop_cnt=3,
            loop_interval=0.01,
            get_detail=False,
        )
        self.assertFalse(status)

        print("ping several hosts and no get_detail")
        mock_execute_shell_command_on_device.side_effect = [
            "Network is unreachable",
            self.response["IPV4_PING_FAILED"],
            self.response["NORMAL_IPV4_LOOP_PING"],
            "Network is unreachable",
            self.response["IPV6_PING_FAILED"],
            self.response["NORMAL_IPV6_LOOP_PING"],
        ]
        result = ins.loop_ping(
            device=dev_object,
            dst_addr=["1.1.1.3", "2011::2"],
            ping_counter=10,
            ping_option="-c 5",
            loop_cnt=3,
            loop_interval=0.01,
            get_detail=False,
        )
        self.assertTrue(isinstance(result, list))
        self.assertTrue(False not in result)

        print("ping several hosts and get detail")
        mock_execute_shell_command_on_device.side_effect = [
            "Network is unreachable",
            self.response["IPV4_PING_FAILED"],
            self.response["NORMAL_IPV4_LOOP_PING"],
            "Network is unreachable",
            self.response["IPV6_PING_FAILED"],
            self.response["NORMAL_IPV6_LOOP_PING"],
        ]
        result = ins.loop_ping(
            device=dev_object,
            dst_addr=["1.1.1.3", "2011::2"],
            ping_counter=10,
            ping_option="-c 5",
            loop_cnt=3,
            loop_interval=0.01,
            get_detail=True,
        )
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(result["1.1.1.3"]["received"] == 3)
        self.assertTrue(result["2011::2"]["received"] == 3)

        print("device type given")
        mock_execute_shell_command_on_device.side_effect = [
            self.response["IPV4_PING_FAILED"],
            self.response["IPV4_PING_FAILED"],
            self.response["IPV4_PING_FAILED"],
            self.response["IPV4_PING_FAILED"],
            self.response["SRX_IPV4_PING"],
        ]
        response = ins.loop_ping(
            device=dev_object,
            dst_addr="1.1.1.2",
            ping_counter=10,
            ping_option="-c 5",
            loop_cnt=5,
            loop_interval=10,
            get_detail=True,
            device_type="linux",
        )
        print("response: ", response)
        self.assertTrue(response["transmitted"] == 3)
        self.assertTrue(response["received"] == 3)
        self.assertTrue(response["lost_rate"] == 0)
        self.assertTrue(response["min"] == 1.005)
        self.assertTrue(response["avg"] == 1.141)
        self.assertTrue(response["max"] == 1.308)
        self.assertTrue(response["mdev"] == 0.126)

    @mock.patch.object(dev, "execute_shell_command_on_device")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_interface_hardware_address(self, mock_execute_cli_command_on_device, mock_execute_shell_command_on_device):
        """UT Case"""
        dev_object = mock.Mock()
        dev_object.get_model.return_value = "linux"
        dev_object.log.return_value = None

        print("Get MAC from DUT")
        dev_object.get_model.return_value = "vsrx"
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            self.response["get_interface_hardware_address_ha_normal_response_xml"]
        )
        result = ins.get_interface_hardware_address(device=dev_object, interface_name="ge-0/0/0")
        self.assertTrue(result == "4c:96:14:e9:58:01")

        print("Get MAC from DUT and get uppercase response")
        result = ins.get_interface_hardware_address(device=dev_object, interface_name="ge-0/0/0", uppercase=True)
        self.assertTrue(result == "4C:96:14:E9:58:01")

        print("Get MAC from DUT but no given interface")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(
            self.response["get_interface_hardware_address_ha_error_response_xml"]
        )
        self.assertRaisesRegex(
            RuntimeError,
            r"not found",
            ins.get_interface_hardware_address,
            device=dev_object, interface_name="ge-1/0/0",
        )

        print("Get MAC from HOST")
        dev_object.get_model.return_value = "linux"
        mock_execute_shell_command_on_device.return_value = self.response["get_interface_hardware_address_host_normal_response"]
        result = ins.get_interface_hardware_address(device=dev_object, interface_name="eth1")
        self.assertTrue(result == "00:50:56:31:ba:ae")

        print("Get MAC from HOST but no given interface")
        mock_execute_shell_command_on_device.return_value = self.response["get_interface_hardware_address_host_error_response"]
        self.assertRaisesRegex(
            RuntimeError,
            r"Device not found",
            ins.get_interface_hardware_address,
            device=dev_object, interface_name="ge-1/0/0"
        )

        print("Have option 'platform'")
        print("Get MAC from HOST")
        dev_object.get_model.return_value = "linux"
        mock_execute_shell_command_on_device.return_value = self.response["get_interface_hardware_address_host_normal_response"]
        result = ins.get_interface_hardware_address(device=dev_object, interface_name="eth1", platform="linux")
        self.assertTrue(result == "00:50:56:31:ba:ae")

        del dev_object.get_model
        print("Not supported platform")
        self.assertRaisesRegex(
            RuntimeError,
            r"do not have 'get_model' method",
            ins.get_interface_hardware_address,
            device=dev_object, interface_name="ge-0/0/0",
        )

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_check_vmhost(self, mock_execute_cli_command_on_device):
        """UT Case"""
        dev_object = mock.Mock()
        dev_object.is_ha.return_value = True
        dev_object.log.return_value = None

        print("check HA Low-end device")
        mock_execute_cli_command_on_device.return_value = self.response["check_vmhost_le_ha_response"]
        result = ins.check_vmhost(device=dev_object)
        self.assertTrue(result == "system")

        print("check HA High-end RE3 device")
        mock_execute_cli_command_on_device.return_value = self.response["check_vmhost_he_ha_re3_response"]
        result = ins.check_vmhost(device=dev_object, force=True)
        self.assertTrue(result == "vmhost")

        dev_object.is_ha.return_value = False
        print("check SA High-end normal device")
        mock_execute_cli_command_on_device.return_value = self.response["check_vmhost_he_sa_response"]
        result = ins.check_vmhost(device=dev_object, force=True)
        self.assertTrue(result == "system")

        print("not force")
        result = ins.check_vmhost(device=dev_object, force=False)
        self.assertTrue(result == "system")

        print("component not list")
        dev_object.is_ha.return_value = True
        mock_execute_cli_command_on_device.return_value = self.response["check_vmhost_not_list_component_response"]
        result = ins.check_vmhost(device=dev_object, force=True)
        self.assertTrue(result == "system")


    def test_reboot_device_in_parallel(self):
        """UT CASE"""
        mock_ha_obj = mock.MagicMock(spec=SrxSystem)
        mock_ha_obj.current_node = mock.MagicMock()
        mock_ha_obj.current_node.current_controller = mock.MagicMock()
        mock_ha_obj.node0 = mock.MagicMock()
        mock_ha_obj.node1 = mock.MagicMock()

        mock_sa_obj = mock.MagicMock(spec=SrxSystem)
        mock_sa_obj.current_node = mock.MagicMock()
        mock_sa_obj.current_node.current_controller = mock.MagicMock()

        mock_host_obj = mock.MagicMock(spec=System)
        mock_host_obj.name = mock.MagicMock(return_value="vm_host")
        mock_host_obj.current_node = mock.MagicMock()
        mock_host_obj.current_node.current_controller = mock.MagicMock()

        builtins.t = mock.MagicMock(spec=init)
        t.background_logger = mock.MagicMock()

        # normal case
        mock_ha_obj.node0.reboot.side_effect = [True, True]
        mock_ha_obj.node1.reboot.side_effect = [True, True]
        mock_sa_obj.reboot.side_effect = [True, True]
        mock_host_obj.reboot.side_effect = [True, True]

        dev_list = [mock_ha_obj, mock_ha_obj, mock_sa_obj, mock_sa_obj, mock_host_obj, mock_host_obj]
        result = ins.reboot_device_in_parallel(device_list=dev_list, interval=60, timeout=600)
        self.assertTrue(result)

        # invalid option value
        self.assertRaisesRegex(
            ValueError,
            r"option 'device_list' must be a list or tuple",
            ins.reboot_device_in_parallel,
            device_list="dev_list",
        )

        # exception during reboot
        dev_list = [mock_host_obj, mock_host_obj]
        mock_host_obj.reboot.side_effect = [KeyboardInterrupt, KeyboardInterrupt]
        result = ins.reboot_device_in_parallel(device_list=dev_list, interval=60, timeout=600)
        self.assertFalse(result)

        mock_host_obj.reboot.side_effect = [True, True]
