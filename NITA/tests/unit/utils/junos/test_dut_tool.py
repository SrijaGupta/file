# coding: UTF-8
"""All unit test cases for DUT handler module"""
# pylint: disable=attribute-defined-outside-init

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import lxml
from unittest import TestCase, mock

from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.junos.dut_tool import dut_tool


class Device(object):
    """Emulate device object"""
    def __init__(self):
        self.node0 = self
        self.node1 = self

    def cli(self):
        """Emulate send cli command"""
        return self

    def shell(self):
        """Emulate send shell command"""
        return self

    def config(self):
        """Emulate send conf command"""
        return self

    def commit(self):
        """Emulate commit action"""
        return self

    def reboot(self):
        """Emulate reboot action"""
        return self

    def node_name(self):
        """Emulate node_name action"""
        return self

    def node_status(self):
        """Emulate node_status action"""
        return self

    def failover(self):
        """Emulate failover action"""
        return self

    def su(self):
        """Emulate su action"""
        return self

    def switch_to_primary_node(self):
        """switch to primary node"""
        return self

    def is_ha(self):
        """Fake is_ha"""
        return self

    def get_tnpdump_info(self, **kwargs):
        """Fake get_tnpdump_info"""
        return kwargs


class Response(object):
    """Emulate Response object"""
    def __init__(self):
        self.response_value = None
        self.status_value = None

    def response(self):
        """Emulate device response"""
        return self.response_value

    def status(self):
        """Emulate device response status"""
        return self.status_value


class TestDutTool(TestCase):
    """Unitest cases for DutTool module"""
    def setUp(self):
        """setup before all cases"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.device = Device()
        self.ins = dut_tool()
        self.response_ins = Response()

        self.response = {}
        self.response["SA_VERSION"] = """
            <software-information>
                <host-name>qilianshan</host-name>
                <product-model>srx5600</product-model>
                <product-name>srx5600</product-name>
                <jsr/>
                <junos-version>17.3I20170502_1013_ssd-builder</junos-version>
                <package-information>
                    <name>os-kernel</name>
                    <comment>JUNOS OS Kernel 64-bit (WITNESS) [20170414.005937_fbsd-builder_stable_10]</comment>
                </package-information>
                <package-information>
                    <name>os-libs</name>
                    <comment>JUNOS OS libs [20170414.005937_fbsd-builder_stable_10]</comment>
                </package-information>
                <package-information>
                    <name>os-runtime</name>
                    <comment>JUNOS OS runtime [20170414.005937_fbsd-builder_stable_10]</comment>
                </package-information>
                <package-information>
                    <name>zoneinfo</name>
                    <comment>JUNOS OS time zone information [20170414.005937_fbsd-builder_stable_10]</comment>
                </package-information>
                <package-information>
                    <name>os-libs-compat32</name>
                    <comment>JUNOS OS libs compat32 [20170414.005937_fbsd-builder_stable_10]</comment>
                </package-information>
                <package-information>
                    <name>os-compat32</name>
                    <comment>JUNOS OS 32-bit compatibility [20170414.005937_fbsd-builder_stable_10]</comment>
                </package-information>
                <package-information>
                    <name>py-extensions</name>
                    <comment>JUNOS py extensions [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>py-base</name>
                    <comment>JUNOS py base [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>os-crypto</name>
                    <comment>JUNOS OS crypto [20170414.005937_fbsd-builder_stable_10]</comment>
                </package-information>
                <package-information>
                    <name>netstack</name>
                    <comment>JUNOS network stack and utilities [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-modules</name>
                    <comment>JUNOS modules [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-modules-platform</name>
                    <comment>JUNOS srx modules [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-libs</name>
                    <comment>JUNOS libs [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-libs-compat32</name>
                    <comment>JUNOS libs compat32 [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-runtime</name>
                    <comment>JUNOS runtime [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jweb</name>
                    <comment>JUNOS Web Management [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-libs-compat32-platform</name>
                    <comment>JUNOS srx libs compat32 [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-runtime-platform</name>
                    <comment>JUNOS srx runtime [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-platform</name>
                    <comment>JUNOS common platform support [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-platform-platform</name>
                    <comment>JUNOS srx platform support [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-libs-platform</name>
                    <comment>JUNOS srx libs [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-dp-crypto-support-platform</name>
                    <comment>JUNOS srx Data Plane Crypto Support [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-daemons</name>
                    <comment>JUNOS daemons [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-urlf</name>
                    <comment>JUNOS Services URL Filter package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-traffic-dird</name>
                    <comment>JUNOS Services TLB Service PIC package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-ssl</name>
                    <comment>JUNOS Services SSL [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-sfw</name>
                    <comment>JUNOS Services Stateful Firewall [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-rpm</name>
                    <comment>JUNOS Services RPM [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-ptsp</name>
                    <comment>JUNOS Services PTSP Container package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-pcef</name>
                    <comment>JUNOS Services PCEF package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-nat</name>
                    <comment>JUNOS Services NAT [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-mss</name>
                    <comment>JUNOS Services Mobile Subscriber Service Container package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-mobile</name>
                    <comment>JUNOS Services MobileNext Software package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-lrf</name>
                    <comment>JUNOS Services Logging Report Framework package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-llpdf</name>
                    <comment>JUNOS Services LL-PDF Container package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-jflow</name>
                    <comment>JUNOS Services Jflow Container package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-jdpi</name>
                    <comment>JUNOS Services Deep Packet Inspection package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-ipsec</name>
                    <comment>JUNOS Services IPSec [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-ids</name>
                    <comment>JUNOS Services IDS [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-idp</name>
                    <comment>JUNOS IDP Services [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-hcm</name>
                    <comment>JUNOS Services HTTP Content Management package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-crypto-base</name>
                    <comment>JUNOS Services Crypto [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-cpcd</name>
                    <comment>JUNOS Services Captive Portal and Content Delivery Container package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-cos</name>
                    <comment>JUNOS Services COS [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-appid</name>
                    <comment>JUNOS AppId Services [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-alg</name>
                    <comment>JUNOS Services Application Level Gateways [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jservices-aacl</name>
                    <comment>JUNOS Services AACL Container package [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jsd-jet-1</name>
                    <comment>JUNOS Extension Toolkit [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jpfe-wrlinux</name>
                    <comment>JUNOS Packet Forwarding Engine Support (wrlinux) [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jpfe-platform</name>
                    <comment>JUNOS Packet Forwarding Engine Support (MX/EX92XX Common) [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jpfe-common</name>
                    <comment>JUNOS Packet Forwarding Engine Support (M/T Common) [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jpfe-X</name>
                    <comment>JUNOS Packet Forwarding Engine Support (MX Common) [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jfirmware</name>
                    <comment>JUNOS jfirmware [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jdocs</name>
                    <comment>JUNOS Online Documentation [20170502.101325_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jail-runtime</name>
                    <comment>JUNOS jail runtime [20170414.005937_fbsd-builder_stable_10]</comment>
                </package-information>
            </software-information>
        """

        self.response["HA_TVP_BASE_VERSION"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <software-information>
                <host-name>vsrx-esx-cn46</host-name>
                <product-model>vsrx</product-model>
                <product-name>vsrx</product-name>
                <junos-version>18.2-2018-02-28.0_DEV_COMMON</junos-version>
                <package-information>
                    <name>os-kernel</name>
                    <comment>JUNOS OS Kernel 64-bit  [20180214.102357_fbsd-builder_stable_11]</comment>
                </package-information>
                <package-information>
                    <name>os-libs</name>
                    <comment>JUNOS OS libs [20180214.102357_fbsd-builder_stable_11]</comment>
                </package-information>
                <package-information>
                    <name>os-runtime</name>
                    <comment>JUNOS OS runtime [20180214.102357_fbsd-builder_stable_11]</comment>
                </package-information>
                <package-information>
                    <name>zoneinfo</name>
                    <comment>JUNOS OS time zone information [20180214.102357_fbsd-builder_stable_11]</comment>
                </package-information>
                <package-information>
                    <name>os-libs-compat32</name>
                    <comment>JUNOS OS libs compat32 [20180214.102357_fbsd-builder_stable_11]</comment>
                </package-information>
                <package-information>
                    <name>os-compat32</name>
                    <comment>JUNOS OS 32-bit compatibility [20180214.102357_fbsd-builder_stable_11]</comment>
                </package-information>
                <package-information>
                    <name>py-extensions</name>
                    <comment>JUNOS py extensions [20180228.140141_ssd-builder_dev_common]</comment>
                    </package-information>
                <package-information>
                    <name>py-base</name>
                    <comment>JUNOS py base [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>os-vmguest</name>
                    <comment>JUNOS OS vmguest [20180214.102357_fbsd-builder_stable_11]</comment>
                </package-information>
                <package-information>
                    <name>os-crypto</name>
                    <comment>JUNOS OS crypto [20180214.102357_fbsd-builder_stable_11]</comment>
                </package-information>
                <package-information>
                    <name>netstack</name>
                    <comment>JUNOS network stack and utilities [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-libs</name>
                    <comment>JUNOS libs [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-libs-compat32</name>
                    <comment>JUNOS libs compat32 [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-runtime</name>
                    <comment>JUNOS runtime [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jweb-srxtvp</name>
                    <comment>JUNOS Web Management Platform Package [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-libs-compat32-platform</name>
                    <comment>JUNOS srx libs compat32 [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-runtime-platform</name>
                    <comment>JUNOS srx runtime [20180228.140141_ssd-builder_dev_common]</comment>
                    </package-information>
                <package-information>
                    <name>junos-platform-platform</name>
                    <comment>JUNOS srx platform support [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-platform</name>
                    <comment>JUNOS common platform support [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-runtime-srxtvp</name>
                    <comment>JUNOS srxtvp runtime [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-pppoe</name>
                    <comment>JUNOS pppoe [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-net-platform</name>
                    <comment>JUNOS mtx network modules [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-modules</name>
                    <comment>JUNOS modules [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-modules-platform</name>
                    <comment>JUNOS srxtvp modules [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-libs-srxtvp</name>
                    <comment>JUNOS srxtvp libs [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-libs-platform</name>
                    <comment>JUNOS srx libs [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-dp-crypto-support-platform</name>
                    <comment>JUNOS srx Data Plane Crypto Support [20180228.140141_ssd-builder_dev_common]</comment>
                    </package-information>
                <package-information>
                    <name>junos-daemons</name>
                    <comment>JUNOS daemons [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>junos-daemons-platform</name>
                    <comment>JUNOS srx daemons [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jsd-jet-1</name>
                    <comment>JUNOS Extension Toolkit [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jinsight</name>
                    <comment>JUNOS J-Insight [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jdocs</name>
                    <comment>JUNOS Online Documentation [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
                <package-information>
                    <name>jail-runtime</name>
                    <comment>JUNOS jail runtime [20180214.102357_fbsd-builder_stable_11]</comment>
                </package-information>
                <package-information>
                    <name>fips-mode</name>
                    <comment>JUNOS FIPS mode utilities [20180228.140141_ssd-builder_dev_common]</comment>
                </package-information>
            </software-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["INVALID_SA_VERSION"] = """
            <software-information>
                <host-namename>qilianshan</host-namename>
                <product-modelmodel>srx5600</product-modelmodel>
                <product-name>srx5600</product-name>
                <jsr/>
                <junos-version>17.3I20170502_1013_ssd-builder</junos-version>
                <package-information>
                    <name>os-kernel</name>
                    <comment>JUNOS OS Kernel 64-bit (WITNESS) [20170414.005937_fbsd-builder_stable_10]</comment>
                </package-information>
            </software-information>
        """

        self.response["HA_VERSION"] = """
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <software-information>
                        <host-name>stroller</host-name>
                        <product-model>srx5600</product-model>
                        <product-name>srx5600</product-name>
                        <jsr/>
                        <junos-version>17.3-20170430_dev_common.1</junos-version>
                        <package-information>
                            <name>junos</name>
                            <comment>JUNOS Software Release [17.3-20170430_dev_common.1]</comment>
                        </package-information>
                    </software-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <software-information>
                        <host-name>sprinter</host-name>
                        <product-model>srx5600</product-model>
                        <product-name>srx5600</product-name>
                        <jsr/>
                        <junos-version>17.3-20170430_dev_common.1</junos-version>
                        <package-information>
                            <name>junos</name>
                            <comment>JUNOS Software Release [17.3-20170430_dev_common.1]</comment>
                        </package-information>
                    </software-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
        """

        self.response["INVALID_HA_VERSION"] = """
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <software-information>
                        <host-namename>stroller</host-namename>
                        <product-modelname>srx5600</product-modelname>
                        <product-name>srx5600</product-name>
                        <jsr/>
                        <junos-version>17.3-20170430_dev_common.1</junos-version>
                        <package-information>
                            <name>junos</name>
                            <comment>JUNOS Software Release [17.3-20170430_dev_common.1]</comment>
                        </package-information>
                    </software-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <software-information>
                        <host-name>sprinter</host-name>
                        <product-model>srx5600</product-model>
                        <product-name>srx5600</product-name>
                        <jsr/>
                        <junos-version>17.3-20170430_dev_common.1</junos-version>
                        <package-information>
                            <name>junos</name>
                            <comment>JUNOS Software Release [17.3-20170430_dev_common.1]</comment>
                        </package-information>
                    </software-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
        """


        self.response["SA_FORGE_TNPDUMP"] = """
           Name                TNPaddr   MAC address    IF     MTU E H R
        master                   0x1 00:00:00:00:00:00 lo0    1500 0 0 3
        """

        self.response["SA_SEIGE_TNPDUMP"] = """
           Name                TNPaddr   MAC address    IF     MTU E H R
        master                   0x1 00:00:00:00:00:00 lo0    1500 0 0 3
        master                   0x1 00:00:00:00:00:00 fxp2   1500 0 1 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff fxp2   1500 0 1 3
        """

        self.response["SA_SRX550_TNPDUMP"] = """
           Name                TNPaddr   MAC address    IF     MTU E H R
        master                   0x1 00:00:00:00:00:00 fxp2   1500 0 1 3
        master                   0x1 00:00:00:00:00:00 lo0    1500 0 0 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff fxp2   1500 0 1 3
        """

        self.response["SA_SRX5600_TNPDUMP"] = """
           Name                TNPaddr   MAC address    IF     MTU E H R
        master                   0x1 02:00:00:00:00:04 em0    1500 0 0 3
        master                   0x1 02:00:01:00:00:04 em1    1500 0 1 3
        re0                      0x4 02:00:00:00:00:04 em0    1500 0 0 3
        re0                      0x4 02:00:01:00:00:04 em1    1500 0 1 3
        fpc0                    0x10 02:00:00:00:00:10 em0    1500 4 0 3
        fpc2                    0x12 02:00:00:00:00:12 em0    1500 5 0 3
        fpc0.pic0              0x110 02:00:10:00:01:10 em0    1500 2 0 3
        fpc0.pic1              0x210 02:00:10:00:02:10 em0    1500 2 0 3
        fpc0.pic2              0x310 02:00:10:00:03:10 em0    1500 2 0 3
        fpc0.pic3              0x410 02:00:10:00:04:10 em0    1500 2 0 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff em0    1500 0 0 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff em1    1500 0 1 3
        """

        self.response["HA_SRX550_TNPDUMP"] = """
           Name                TNPaddr   MAC address    IF     MTU E H R
        cluster1.node0     0x1100001 20:4e:71:fe:b2:9f fxp1   1500 0 1 3
        cluster1.node0     0x1100001 00:00:00:00:00:00 fxp2   1500 0 1 3
        cluster1.node1     0x2100001 20:4e:71:fe:bf:9f fxp1   1500 2 1 3
        cluster1.master    0xf100001 20:4e:71:fe:b2:9f fxp1   1500 0 0 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff fxp1   1500 0 1 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff fxp2   1500 0 1 3
        """

        self.response["HA_SEIGE_TNPDUMP"] = """
           Name                TNPaddr   MAC address    IF     MTU E H R
        cluster1.node0     0x1100001 84:c1:c1:a8:9e:c2 fxp1   1500 0 1 3
        cluster1.node0     0x1100001 00:00:00:00:00:00 fxp2   1500 0 1 3
        cluster1.node1     0x2100001 84:c1:c1:a8:b6:c2 fxp1   1500 3 1 3
        cluster1.master    0xf100001 84:c1:c1:a8:b6:c2 fxp1   1500 3 1 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff fxp1   1500 0 1 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff fxp2   1500 0 1 3
        """

        self.response["HA_FORGE_TNPDUMP"] = """
           Name                TNPaddr   MAC address    IF     MTU E H R
        cluster1.node0     0x1100001 02:00:00:01:01:04 em0    1500 0 1 3
        cluster1.node1     0x2100001 02:00:00:02:01:04 em0    1500 2 1 3
        cluster1.master    0xf100001 02:00:00:01:01:04 em0    1500 0 0 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff em0    1500 0 1 3
        """

        self.response["HA_SRX5600_TNPDUMP"] = """
           Name                TNPaddr   MAC address    IF     MTU E H R
        cluster1.node0     0x1100001 02:00:00:01:00:04 em0    1500 0 0 3
        cluster1.node0     0x1100001 02:00:01:01:00:04 em1    1500 0 1 3
        node0.re0          0x1100004 02:00:00:01:00:04 em0    1500 0 0 3
        node0.re0          0x1100004 02:00:01:01:00:04 em1    1500 0 1 3
        node0.fpc0         0x1100010 02:00:00:01:00:10 em0    1500 4 0 3
        node0.fpc2         0x1100012 02:00:00:01:00:12 em0    1500 4 0 3
        node0.fpc0.pic0    0x1100110 02:00:10:01:01:10 em0    1500 2 0 3
        node0.fpc0.pic1    0x1100210 02:00:10:01:02:10 em0    1500 2 0 3
        node0.fpc0.pic2    0x1100310 02:00:10:01:03:10 em0    1500 3 0 3
        node0.fpc0.pic3    0x1100410 02:00:10:01:04:10 em0    1500 3 0 3
        cluster1.node1     0x2100001 02:00:00:02:00:04 em0    1500 2 0 3
        node1.fpc0         0x2100010 02:00:00:02:00:10 em0    1500 5 0 3
        node1.fpc2         0x2100012 02:00:00:02:00:12 em0    1500 4 0 3
        node1.fpc0.pic0    0x2100110 02:00:10:02:01:10 em0    1500 2 0 3
        node1.fpc0.pic1    0x2100210 02:00:10:02:02:10 em0    1500 2 0 3
        node1.fpc0.pic2    0x2100310 02:00:10:02:03:10 em0    1500 3 0 3
        node1.fpc0.pic3    0x2100410 02:00:10:02:04:10 em0    1500 3 0 3
        cluster1.master    0xf100001 02:00:00:01:00:04 em0    1500 0 0 3
        cluster1.master    0xf100001 02:00:01:01:00:04 em1    1500 0 1 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff em0    1500 0 0 3
        bcast             0xffffffff ff:ff:ff:ff:ff:ff em1    1500 0 1 3
        """

        self.response["HA_SHOW_VERSION"] = """
            <software-information>
                <host-name>qilianshan</host-name>
                <product-model>srx5600</product-model>
                <product-name>srx5600</product-name>
                <jsr/>
                <junos-version>15.1I20170502_x_151_x49.0-850286</junos-version>
                <package-information>
                    <name>junos</name>
                    <comment>JUNOS Software Release [15.1I20170502_x_151_x49.0-850286]</comment>
                </package-information>
            </software-information>
        """

        self.response["FULL_TEXT_XML"] = """
        regress@srx345-01> show version | display xml
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.3D0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <software-information>
                        <host-name>srx345-01</host-name>
                        <product-model>srx345</product-model>
                        <product-name>srx345</product-name>
                        <jsr/>
                        <junos-version>17.3-20170426_dev_common.1</junos-version>
                        <package-information>
                            <name>junos</name>
                            <comment>JUNOS Software Release [17.3-20170426_dev_common.1]</comment>
                        </package-information>
                    </software-information>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <software-information>
                        <host-name>srx345-02</host-name>
                        <product-model>srx345</product-model>
                        <product-name>srx345</product-name>
                        <jsr/>
                        <junos-version>17.3-20170426_dev_common.1</junos-version>
                        <package-information>
                            <name>junos</name>
                            <comment>JUNOS Software Release [17.3-20170426_dev_common.1]</comment>
                        </package-information>
                    </software-information>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{secondary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        self.response["HA_SEIGE_VTY"] = """
        ================ cluster1.node0 ================

        gate global usage and global maximum:
        gate limit and usage on this PIC:
        Total bucket size:      3072,
        Share bucket size:      3072, used: 0
         LSYS (id)                       Reserve      Maximum Used(rsv+shr)
        ---------------------------------------------------------------------------------------
         root-logical-system   ( 0)            0         3072            0(0+0)
        """

        self.response["SRX_SOFTWARE_INSTALL"] = """
initramfs.cpio.gz: OK
version.txt: OK
upgrade_platform: Checksum verified and OK...
upgrade_platform: Staging of /var/tmp/junos-srx-mr-vsrx-17.3I20170605_0958_hchen-linux.tgz completed
upgrade_platform: System need *REBOOT* to complete the upgrade
upgrade_platform: Run upgrade_platform with option -r | --rollback to rollback the upgrade

Host OS upgrade staged. Reboot the system to complete installation!


WARNING:     A REBOOT IS REQUIRED TO LOAD THIS SOFTWARE CORRECTLY. Use the
WARNING:     'request system reboot' command when software installation is
WARNING:     complete. To abort the installation, do not reboot your system,
WARNING:     instead use the 'request system software delete junos'
WARNING:     command as soon as this operation completes.

Saving state for rollback ...
        """

        self.response["HA_HAVE_COREDUMP"] = """
node0:
--------------------------------------------------------------------------
/var/tmp/pics/*core*: No such file or directory
/var/crash/kernel.*: No such file or directory
/var/jails/rest-api/tmp/*core*: No such file or directory
/tftpboot/corefiles/*core*: No such file or directory

/var/crash/corefiles:
total blocks: 36
drwxr-xr-x  2 root  wheel       4096 Jun 26 09:01 cores/
total files: 0

/var/tmp/cores:
total blocks: 8
total files: 0

node1:
--------------------------------------------------------------------------
/var/tmp/pics/*core*: No such file or directory
/var/crash/kernel.*: No such file or directory
/var/jails/rest-api/tmp/*core*: No such file or directory
/tftpboot/corefiles/*core*: No such file or directory

/var/crash/corefiles:
total blocks: 223644
drwxr-xr-x  2 root  wheel       4096 Jul 19 02:55 cores/
-rw-r--r--  1 root  wheel  114494531 Aug 29 03:11 localhost.srxpfe.5897.1503975896.core.tgz
-rw-r--r--  1 root  wheel  114494531 Aug 29 03:12 localhost.srxpfe.5897.1503975898.core.tgz
total files: 1

/var/tmp/cores:
total blocks: 8
total files: 0
        """

        self.response["SA_HAVE_COREDUMP"] = """
/var/tmp/*core*: No such file or directory
/var/tmp/pics/*core*: No such file or directory
/var/crash/kernel.*: No such file or directory
/var/jails/rest-api/tmp/*core*: No such file or directory
/tftpboot/corefiles/*core*: No such file or directory

/var/crash/corefiles:
total blocks: 1537484
-rw-r--r--  1 root  wheel   34540125 Aug 16 19:58 forge-cn04-node.bcmLINK.0.4239.1502884602.core.tgz
-rw-r--r--  1 root  wheel   34545099 Aug 23 17:11 forge-cn04-node.bcmLINK.0.4617.1503479304.core.tgz
-rw-r--r--  1 root  wheel   34548862 Aug 16 20:01 forge-cn04-node.bcmLINK.0.4827.1502884791.core.tgz
-rw-r--r--  1 root  wheel   33942076 Aug 23 17:14 forge-cn04-node.bcmLINK.0.4940.1503479594.core.tgz
-rw-r--r--  1 root  wheel   34544667 Aug 17 11:13 forge-cn04-node.bcmLINK.0.5143.1502939519.core.tgz
-rw-r--r--  1 root  wheel   34545968 Aug 16 20:04 forge-cn04-node.bcmLINK.0.5157.1502884955.core.tgz
-rw-r--r--  1 root  wheel   34503273 Aug 16 19:29 forge-cn04-node.bcmLINK.0.5210.1502882856.core.tgz
-rw-r--r--  1 root  wheel   33122818 Aug 23 17:17 forge-cn04-node.bcmLINK.0.5237.1503479773.core.tgz
-rw-r--r--  1 root  wheel   34021166 Aug 17 11:16 forge-cn04-node.bcmLINK.0.5523.1502939682.core.tgz
-rw-r--r--  1 root  wheel   34568667 Aug 23 17:20 forge-cn04-node.bcmLINK.0.5545.1503479939.core.tgz
-rw-r--r--  1 root  wheel   30717130 Aug 16 19:32 forge-cn04-node.bcmLINK.0.5547.1502883024.core.tgz
-rw-r--r--  1 root  wheel   34497236 Aug 17 11:19 forge-cn04-node.bcmLINK.0.5842.1502939844.core.tgz
-rw-r--r--  1 root  wheel   34522238 Aug 23 17:23 forge-cn04-node.bcmLINK.0.5843.1503480121.core.tgz
-rw-r--r--  1 root  wheel   34533558 Aug 16 19:34 forge-cn04-node.bcmLINK.0.5861.1502883186.core.tgz
-rw-r--r--  1 root  wheel   34595825 Aug 17 11:22 forge-cn04-node.bcmLINK.0.6161.1502940027.core.tgz
-rw-r--r--  1 root  wheel   34597859 Aug 23 17:26 forge-cn04-node.bcmLINK.0.6161.1503480301.core.tgz
-rw-r--r--  1 root  wheel   34535307 Aug 16 19:37 forge-cn04-node.bcmLINK.0.6165.1502883368.core.tgz
-rw-r--r--  1 root  wheel   33778197 Aug 17 11:25 forge-cn04-node.bcmLINK.0.6491.1502940208.core.tgz
-rw-r--r--  1 root  wheel   34503430 Aug 16 19:40 forge-cn04-node.bcmLINK.0.6498.1502883553.core.tgz
-rw-r--r--  1 root  wheel   34576219 Aug 17 11:28 forge-cn04-node.bcmLINK.0.6791.1502940391.core.tgz
-rw-r--r--  1 root  wheel   34544907 Aug 16 19:43 forge-cn04-node.bcmLINK.0.6800.1502883734.core.tgz
-rw-r--r--  1 root  wheel   34316891 Aug 16 19:47 forge-cn04-node.bcmLINK.0.7114.1502883915.core.tgz
-rw-r--r--  1 root  wheel   34522805 Aug 16 19:50 forge-cn04-node.bcmLINK.0.7457.1502884097.core.tgz
drwx------  2 root  wheel      16384 Aug 16 10:01 lost+found/
total files: 23
        """

        self.response["SA_NO_COREDUMP"] = """
/var/tmp/pics/*core*: No such file or directory
/var/crash/kernel.*: No such file or directory
/var/jails/rest-api/tmp/*core*: No such file or directory
/tftpboot/corefiles/*core*: No such file or directory

/var/crash/corefiles:
total blocks: 12
total files: 0

/var/tmp/cores:
total blocks: 12
total files: 0
        """

        self.response["MULTI_LICENSE"] = """
    <license-usage-summary xmlns="http://xml.juniper.net/junos/15.1I0/junos-license">
        <features-used/>
        <feature-summary>
            <name>idp-sig</name>
            <description>IDP Signature</description>
            <licensed>1</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <end-date junos:seconds="1545696000">2018-12-25</end-date>
        </feature-summary>
        <feature-summary>
            <name>appid-sig</name>
            <description>APPID Signature</description>
            <licensed>1</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <end-date junos:seconds="1545696000">2018-12-25</end-date>
        </feature-summary>
        <feature-summary>
            <name>logical-system</name>
            <description>Logical System Capacity</description>
            <licensed>1</licensed>
            <used-licensed>1</used-licensed>
            <used-given>0</used-given>
            <needed>0</needed>
            <validity-type>permanent</validity-type>
        </feature-summary>
        <feature-summary>
            <name>remote-access-ipsec-vpn-client</name>
            <description>remote-access-ipsec-vpn-client</description>
            <licensed>2</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <validity-type>permanent</validity-type>
        </feature-summary>
        <feature-summary>
            <name>Virtual Appliance</name>
            <description>Virtual Appliance</description>
            <licensed>1</licensed>
            <used-licensed>1</used-licensed>
            <needed>0</needed>
            <remaining-time>
                <remaining-validity-value junos:seconds="2572880">29 days</remaining-validity-value>
            </remaining-time>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["SINGLE_PERMANENT_LICENSE"] = """
    <license-usage-summary xmlns="http://xml.juniper.net/junos/15.1I0/junos-license">
        <feature-summary>
            <name>logical-system</name>
            <description>Logical System Capacity</description>
            <licensed>1</licensed>
            <used-licensed>1</used-licensed>
            <used-given>0</used-given>
            <needed>0</needed>
            <validity-type>permanent</validity-type>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["SINGLE_END_DATE_LICENSE"] = """
    <license-usage-summary xmlns="http://xml.juniper.net/junos/15.1I0/junos-license">
        <feature-summary>
            <name>idp-sig</name>
            <description>IDP Signature</description>
            <licensed>1</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <end-date junos:seconds="1545696000">2018-12-25</end-date>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["SINGLE_REMAINING_TIME_LICENSE"] = """
    <license-usage-summary xmlns="http://xml.juniper.net/junos/15.1I0/junos-license">
        <feature-summary>
            <name>Virtual Appliance</name>
            <description>Virtual Appliance</description>
            <licensed>1</licensed>
            <used-licensed>1</used-licensed>
            <needed>0</needed>
            <remaining-time>
                <remaining-validity-value junos:seconds="2572880">29 days</remaining-validity-value>
            </remaining-time>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["SA_HE_FLOW_SESSION_HAVE_UNEXPECT_OUTPUT"] = """
Message from syslogd@sprinter at Jan 29 10:54:40  ...
sprinter node1.fpc1 CMLC: Going disconnected; Routing engine chassis socket closed abruptly

Message from syslogd@sprinter at Jan 29 10:54:40  ...
sprinter node1.fpc0 RDP: Remote side closed connection: rdp.(fpc0:6151).(serverRouter:chassis)

Message from syslogd@sprinter at Jan 29 10:54:40  ...
sprinter node1.fpc5 RDP: Remote side closed connection: rdp.(fpc5:3080).(serverRouter:chassis)

Message from syslogd@sprinter at Jan 29 10:54:40  ...
sprinter node1.fpc0 CMLC: Going disconnected; Routing engine chassis socket closed abruptly

Message from syslogd@sprinter at Jan 29 10:54:40  ...
sprinter node1.fpc5 CMLC: Going disconnected; Routing engine chassis socket closed abruptly
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.2I0/junos">
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <flow-session-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC1:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC2:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>20000019</session-identifier>
                    <status>Normal</status>
                    <session-state>Backup</session-state>
                    <session-flag>0x8000000/0x8000000/0x0/0x3</session-flag>
                    <policy>t_un/4</policy>
                    <nat-source-pool-name>root_src_v6_pat_10</nat-source-pool-name>
                    <application-name>junos-syslog</application-name>
                    <application-value>23</application-value>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>6000</configured-timeout>
                    <timeout>5584</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>239720</start-time>
                    <duration>419</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000::2</source-address>
                        <source-port>10000</source-port>
                        <destination-address>2000:1::2</destination-address>
                        <destination-port>514</destination-port>
                        <protocol>udp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>reth0.0</interface-name>
                        <session-token>0x6008</session-token>
                        <flag>0x40000023</flag>
                        <route>0x76d33c2</route>
                        <gateway>2000::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>2</pkt-cnt>
                        <byte-cnt>160</byte-cnt>
                        <dcp-session-id>20000034</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:1::2</source-address>
                        <source-port>514</source-port>
                        <destination-address>3000:10::1</destination-address>
                        <destination-port>10226</destination-port>
                        <protocol>udp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>reth1.0</interface-name>
                        <session-token>0x6009</session-token>
                        <flag>0x60000022</flag>
                        <route>0x76d43c2</route>
                        <gateway>2000:1::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                        <dcp-session-id>210000017</dcp-session-id>
                    </flow-information>
                </flow-session>
                <flow-session junos:style="brief">
                    <session-identifier>20000020</session-identifier>
                    <status>Normal</status>
                    <session-state>Backup</session-state>
                    <session-flag>0x8000000/0x8000000/0x0/0x108003</session-flag>
                    <policy>t_un/4</policy>
                    <nat-source-pool-name>root_src_v6_pat_10</nat-source-pool-name>
                    <application-name>junos-telnet</application-name>
                    <application-value>10</application-value>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1388</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>239726</start-time>
                    <duration>413</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>2000::2</source-address>
                        <source-port>40241</source-port>
                        <destination-address>2000:1::2</destination-address>
                        <destination-port>23</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>reth0.0</interface-name>
                        <session-token>0x6008</session-token>
                        <flag>0x40001023</flag>
                        <route>0x76d33c2</route>
                        <gateway>2000::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>16</pkt-cnt>
                        <byte-cnt>1218</byte-cnt>
                        <dcp-session-id>20000035</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>2000:1::2</source-address>
                        <source-port>23</source-port>
                        <destination-address>3000:10::2</destination-address>
                        <destination-port>12065</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>reth1.0</interface-name>
                        <session-token>0x6009</session-token>
                        <flag>0x60001022</flag>
                        <route>0x76d43c2</route>
                        <gateway>2000:1::2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>16</pkt-cnt>
                        <byte-cnt>2905</byte-cnt>
                        <dcp-session-id>30000027</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>2</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-flow">
                <flow-fpc-pic-id> on FPC0 PIC3:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>30000018</session-identifier>
                    <status>Normal</status>
                    <session-state>Backup</session-state>
                    <session-flag>0x8000000/0x8000000/0x0/0x3</session-flag>
                    <policy>t_un/4</policy>
                    <nat-source-pool-name>root_src_v4_pat</nat-source-pool-name>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>6000</configured-timeout>
                    <timeout>5574</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>239712</start-time>
                    <duration>426</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>100.0.0.10</source-address>
                        <source-port>10000</source-port>
                        <destination-address>100.0.1.10</destination-address>
                        <destination-port>20000</destination-port>
                        <protocol>udp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>reth0.0</interface-name>
                        <session-token>0x6008</session-token>
                        <flag>0x40000021</flag>
                        <route>0xc0020006</route>
                        <gateway>100.0.0.10</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>2</pkt-cnt>
                        <byte-cnt>120</byte-cnt>
                        <dcp-session-id>30000026</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>100.0.1.10</source-address>
                        <source-port>20000</source-port>
                        <destination-address>30.0.1.2</destination-address>
                        <destination-port>11053</destination-port>
                        <protocol>udp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>reth1.0</interface-name>
                        <session-token>0x6009</session-token>
                        <flag>0x60000020</flag>
                        <route>0x0</route>
                        <gateway>100.0.1.10</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>0</pkt-cnt>
                        <byte-cnt>0</byte-cnt>
                        <dcp-session-id>200000032</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-flow">
                <flow-fpc-pic-id> on FPC5 PIC0:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-flow">
                <flow-fpc-pic-id> on FPC5 PIC1:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-flow">
                <flow-fpc-pic-id> on FPC5 PIC2:</flow-fpc-pic-id>
                <displayed-session-count>0</displayed-session-count>
            </flow-session-information>
            <flow-session-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-flow">
                <flow-fpc-pic-id> on FPC5 PIC3:</flow-fpc-pic-id>
                <flow-session junos:style="brief">
                    <session-identifier>230000011</session-identifier>
                    <status>Normal</status>
                    <session-state>Backup</session-state>
                    <session-flag>0x8000000/0x8000000/0x0/0x108103</session-flag>
                    <policy>t_un/4</policy>
                    <nat-source-pool-name>root_src_v4_pat</nat-source-pool-name>
                    <application-name>junos-telnet</application-name>
                    <application-value>10</application-value>
                    <dynamic-application-name>junos:UNKNOWN</dynamic-application-name>
                    <encryption-traffic-name> Unknown</encryption-traffic-name>
                    <application-traffic-control-rule-set-name>INVALID</application-traffic-control-rule-set-name>
                    <application-traffic-control-rule-name>INVALID</application-traffic-control-rule-name>
                    <configured-timeout>1800</configured-timeout>
                    <timeout>1380</timeout>
                    <sess-state>Valid</sess-state>
                    <logical-system></logical-system>
                    <wan-acceleration></wan-acceleration>
                    <start-time>239556</start-time>
                    <duration>421</duration>
                    <session-mask>0</session-mask>
                    <flow-information junos:style="brief">
                        <direction>In</direction>
                        <source-address>100.0.0.2</source-address>
                        <source-port>34962</source-port>
                        <destination-address>100.0.1.2</destination-address>
                        <destination-port>23</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>reth0.0</interface-name>
                        <session-token>0x6008</session-token>
                        <flag>0x40001621</flag>
                        <route>0x76da3c2</route>
                        <gateway>100.0.0.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>16</pkt-cnt>
                        <byte-cnt>898</byte-cnt>
                        <dcp-session-id>230000026</dcp-session-id>
                    </flow-information>
                    <flow-information junos:style="brief">
                        <direction>Out</direction>
                        <source-address>100.0.1.2</source-address>
                        <source-port>23</source-port>
                        <destination-address>30.0.1.1</destination-address>
                        <destination-port>10579</destination-port>
                        <protocol>tcp</protocol>
                        <conn-tag>0x0</conn-tag>
                        <interface-name>reth1.0</interface-name>
                        <session-token>0x6009</session-token>
                        <flag>0x60001620</flag>
                        <route>0x76c73c2</route>
                        <gateway>100.0.1.2</gateway>
                        <tunnel-information>0</tunnel-information>
                        <port-sequence>0</port-sequence>
                        <fin-sequence>0</fin-sequence>
                        <fin-state>0</fin-state>
                        <seq-ack-diff>0</seq-ack-diff>
                        <pkt-cnt>16</pkt-cnt>
                        <byte-cnt>2589</byte-cnt>
                        <dcp-session-id>10000032</dcp-session-id>
                    </flow-information>
                </flow-session>
                <displayed-session-count>1</displayed-session-count>
            </flow-session-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    <cli>
        <banner>{primary:node1}</banner>
    </cli>
</rpc-reply>
        """

    def tearDown(self):
        """teardown after all cases"""
        pass

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_get_version_info(self, mock_send_cli_cmd):
        """Get image version, platform, hostname, etc... info from device"""
        print("Get version from SA platform")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_VERSION"])
        result = self.ins.get_version_info(device="SA_PLATFORM", force_get=True)
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)

        print("Get version from HA platform for all node info")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_VERSION"])
        result = self.ins.get_version_info(device="HA_PLATFORM", force_get=True)
        self.assertTrue("node0" in result)
        self.assertTrue("node1" in result)

        print("Get version from HA platform's node0")
        result = self.ins.get_version_info(device="HA_PLATFORM", force_get=True, node=0)
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)

        print("Get version from HA platform's node1")
        result = self.ins.get_version_info(device="HA_PLATFORM", force_get=True, node="node1")
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)

        print("Get HA version from previous result")
        result = self.ins.get_version_info(device="HA_PLATFORM", force_get=False, node="node1")
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)

        print("Get SA version from previous result")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_VERSION"])
        result = self.ins.get_version_info(device="SA_PLATFORM", force_get=False)
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)

        print("Get SA version if device return invalid")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["INVALID_SA_VERSION"])
        result = self.ins.get_version_info(device="SA_PLATFORM", force_get=True)
        self.assertTrue(result["hostname"] is None)
        self.assertTrue(result["product_model"] is None)

        print("Get HA version if device return invalid")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["INVALID_HA_VERSION"])
        result = self.ins.get_version_info(device="HA_PLATFORM", force_get=True)
        self.assertTrue(result["node0"]["hostname"] is None)
        self.assertTrue(result["node0"]["product_model"] is None)

        print("Get TVP base version on HA but only have one node")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_TVP_BASE_VERSION"])
        result = self.ins.get_version_info(device="HA_PLATFORM", force_get=True)
        self.assertEqual(result["node0"]["hostname"], "vsrx-esx-cn46")
        self.assertEqual(result["node0"]["product_model"], "vsrx")

    def test_get_tnpdump_info(self):
        """Get DUT's tnpdump infomation"""
        result = self.ins.get_tnpdump_info(device=self.device, force_get=True)

    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_get_coredump_file(self, mock_send_cli_cmd):
        """test get coredump file"""
        print("Get HA coredump")
        mock_send_cli_cmd.return_value = self.response["HA_HAVE_COREDUMP"]
        result = self.ins.get_coredump_file(device=self.device, timeout=30)
        self.assertTrue(len(result) == 2)

        print("Get SA no coredump")
        mock_send_cli_cmd.return_value = self.response["SA_NO_COREDUMP"]
        result = self.ins.get_coredump_file(device=self.device)
        self.assertTrue(len(result) == 0)

        print("Get SA have coredump")
        mock_send_cli_cmd.return_value = self.response["SA_HAVE_COREDUMP"]
        result = self.ins.get_coredump_file(device=self.device)
        self.assertTrue(len(result) >= 4)

        print("Get SA have coredump")
        mock_send_cli_cmd.return_value = self.response["SA_HAVE_COREDUMP"]
        result = self.ins.get_coredump_file(device=self.device, return_mode="counter")
        self.assertTrue(result >= 4)

    @mock.patch.object(Device, "cli")
    def test_send_cli_cmd(self, mock_cli):
        """Send cli to DUT

        Below checking is for UT in CI server, don't know why alywas get wrong result:

             or "multi-routing-engine-results" in result

        """
        print("send cmd by pyez channel and get text response")
        self.response_ins.response_value = lxml.etree.fromstring(self.response["HA_SHOW_VERSION"])
        mock_cli.return_value = self.response_ins
        result = self.ins.send_cli_cmd(device=self.device, cmd="show version", format="text", channel="pyez")
        print("result:\n{}".format(result))
        self.assertTrue("software-information" in result or "license-usage-summary" in result or "multi-routing-engine-results" in result)

        print("send cmd by pyez channel and get xml response")
        self.response_ins.response_value = lxml.etree.fromstring(self.response["HA_SHOW_VERSION"])
        mock_cli.return_value = self.response_ins
        result = self.ins.send_cli_cmd(device=self.device, cmd="show version", format="xml", channel="pyez")
        self.assertTrue("software-information" in result  or "license-usage-summary" in result or "multi-routing-engine-results" in result)

        print("send cmd by text channel and get xml response")
        self.response_ins.response_value = self.response["FULL_TEXT_XML"]
        mock_cli.return_value = self.response_ins
        result = self.ins.send_cli_cmd(device=self.device, cmd="show version", format="xml", channel="text")
        self.assertTrue(isinstance(result, dict))
        self.assertTrue("rpc-reply" in result  or "license-usage-summary" in result or "multi-routing-engine-results" in result)

        print("send cmd by text channel and get text response")
        self.response_ins.response_value = self.response["HA_SRX550_TNPDUMP"]
        mock_cli.return_value = self.response_ins
        result = self.ins.send_cli_cmd(device=self.device, cmd=["show version", "tnpdump"], format="text", channel="text")
        self.assertTrue(re.search(r"cluster", result))

        print("invalid option for cmd check")
        self.response_ins.response_value = self.response["HA_SRX550_TNPDUMP"]
        mock_cli.return_value = self.response_ins

        case = False
        try:
            self.ins.send_cli_cmd(device=self.device, cmd=None, format="text", channel="text")
        except TypeError as err:
            print(err)
            case = True
        self.assertTrue(case)

        print("invalid option for channel check")
        self.response_ins.response_value = self.response["HA_SRX550_TNPDUMP"]
        mock_cli.return_value = self.response_ins

        case = False
        try:
            self.ins.send_cli_cmd(device=self.device, cmd="show version", format="text", channel="unknown")
        except ValueError as err:
            print(err)
            case = True
        self.assertTrue(case)

        print("invalid option for format check")
        self.response_ins.response_value = self.response["HA_SRX550_TNPDUMP"]
        mock_cli.return_value = self.response_ins

        case = False
        try:
            self.ins.send_cli_cmd(device=self.device, cmd="show version", format="unknown", channel="text")
        except ValueError as err:
            print(err)
            case = True
        self.assertTrue(case)

        print("Get XML response that have unexpect string")
        self.response_ins.response_value = self.response["SA_HE_FLOW_SESSION_HAVE_UNEXPECT_OUTPUT"]
        mock_cli.return_value = self.response_ins
        response = self.ins.send_cli_cmd(device=self.device, cmd=["show version", "tnpdump"], format="xml", channel="text")
        self.assertIsInstance(response, dict)
        self.assertIn("rpc-reply", response)

        print("Get not well-format XML response")
        self.response_ins.response_value = self.response["HA_SRX550_TNPDUMP"]
        mock_cli.return_value = self.response_ins
        self.assertRaisesRegex(
            RuntimeError,
            r"Not well-formated XML response",
            self.ins.send_cli_cmd,
            device=self.device, cmd=["show version", "tnpdump"], format="xml", channel="text"
        )

        print("Add 'no-more' to cmd in SSH channel")
        self.response_ins.response_value = self.response["SA_HE_FLOW_SESSION_HAVE_UNEXPECT_OUTPUT"]
        mock_cli.return_value = self.response_ins
        response = self.ins.send_cli_cmd(device=self.device, cmd=["show version", "tnpdump"], format="text", channel="text", no_more=True)
        self.assertIsInstance(response, str)
        self.assertIn("Message from syslogd", response)


    @mock.patch.object(Device, "shell")
    def test_send_shell_cmd(self, mock_shell):
        """Check send shell cmd"""
        print("send one shell cmd")
        self.response_ins.response_value = self.response["HA_FORGE_TNPDUMP"]
        mock_shell.return_value = self.response_ins
        result = self.ins.send_shell_cmd(device=self.device, cmd="tnpdump", timeout=30)
        self.assertTrue(re.search(r"0x1100001", result))

        print("send list of shell cmd")
        self.response_ins.response_value = self.response["HA_FORGE_TNPDUMP"]
        mock_shell.return_value = self.response_ins
        result = self.ins.send_shell_cmd(device=self.device, cmd=("tnpdump", "tnpdump"), timeout=30)
        self.assertTrue(re.search(r"0x1100001", result))

        print("check invalid option")
        self.response_ins.response_value = self.response["HA_FORGE_TNPDUMP"]
        mock_shell.return_value = self.response_ins

        case = False
        try:
            self.ins.send_shell_cmd(device=self.device, cmd=None, timeout=30)
        except TypeError as err:
            print(err)
            case = True
        self.assertTrue(case)

    @mock.patch.object(Device, "is_ha")
    @mock.patch.object(Device, "reboot")
    @mock.patch.object(Device, "commit")
    @mock.patch.object(Device, "config")
    def test_send_conf_cmd(self, mock_config, mock_commit, mock_reboot, mock_is_ha):
        """Check send conf cmd"""
        print("do configurtion and commit, then get response")
        cmds = (
            "set security policies default-policy permit-all",
        )

        self.response_ins.response_value = "commit complete"
        self.response_ins.status_value = True
        mock_config.return_value = self.response_ins
        mock_commit.return_value = self.response_ins
        mock_reboot.return_value = True
        result = self.ins.send_conf_cmd(device=self.device, cmd=cmds, commit=True, get_response=True)
        self.assertTrue(re.search(r"commit complete", result))

        print("do configurtion without commit")
        cmds = (
            "set security policies default-policy permit-all",
        )

        self.response_ins.response_value = ""
        self.response_ins.status_value = True
        mock_config.return_value = self.response_ins
        mock_reboot.return_value = True
        result = self.ins.send_conf_cmd(device=self.device, cmd=cmds, commit=False, get_response=False)
        self.assertTrue(isinstance(result, bool))

        print("do configurtion and reboot")
        cmd = "set security forwarding-options family inet6 mode flow-based"
        self.response_ins.response_value = "flow-mode changed, you must reboot the system to implement."
        self.response_ins.status_value = True
        mock_config.return_value = self.response_ins
        mock_commit.return_value = self.response_ins
        mock_reboot.return_value = True
        mock_is_ha.return_value = False
        result = self.ins.send_conf_cmd(device=self.device, cmd=cmd, commit=True, reboot_if_need=True, get_response=True)
        self.assertTrue(re.search(r"reboot", result))

        print("do configurtion and reboot but reboot failed")
        cmd = "set security forwarding-options family inet6 mode flow-based"
        self.response_ins.response_value = "flow-mode changed, you must reboot the system to implement."
        self.response_ins.status_value = True
        mock_config.return_value = self.response_ins
        mock_commit.return_value = self.response_ins
        mock_reboot.side_effect = RuntimeError
        result = self.ins.send_conf_cmd(device=self.device, cmd=cmd, commit=True, reboot_if_need=True, get_response=True)
        self.assertFalse(result)


        print("check invalid option cmd")
        self.response_ins.response_value = "flow-mode changed, you must reboot the system to implement."
        self.response_ins.status_value = True
        mock_config.return_value = self.response_ins
        mock_commit.return_value = self.response_ins

        case = False
        try:
            self.ins.send_conf_cmd(device=self.device, cmd=None, commit=True, reboot_if_need=False, get_response=True)
        except TypeError as err:
            print(err)
            case = True
        self.assertTrue(case)

        print("do configurtion and reboot 2 nodes in HA setup")
        cmd = "set security forwarding-options family inet6 mode flow-based"
        self.response_ins.response_value = "flow-mode changed, you must reboot the system to implement."
        self.response_ins.status_value = True
        mock_config.return_value = self.response_ins
        mock_commit.return_value = self.response_ins
        mock_reboot.side_effect = [True, True]
        mock_is_ha.return_value = True
        result = self.ins.send_conf_cmd(device=self.device, cmd=cmd, commit=True, reboot_if_need=True, get_response=True)
        self.assertTrue(re.search(r"reboot", result))

        print("do configurtion and reboot 2 nodes in HA setup but reboot failed")
        cmd = "set security forwarding-options family inet6 mode flow-based"
        self.response_ins.response_value = "flow-mode changed, you must reboot the system to implement."
        self.response_ins.status_value = True
        mock_config.return_value = self.response_ins
        mock_commit.return_value = self.response_ins
        mock_reboot.return_value = False
        mock_is_ha.return_value = True
        result = self.ins.send_conf_cmd(device=self.device, cmd=cmd, commit=True, reboot_if_need=True, get_response=True)
        self.assertFalse(result)

    @mock.patch.object(dut_tool, "su")
    @mock.patch.object(dut_tool, "get_tnpdump_info")
    @mock.patch.object(dut_tool, "send_shell_cmd")
    def test_send_vty_cmd(self, mock_send_shell_cmd, mock_get_tnpdump_info, mock_su):
        """Check send VTY command to DUT and get response"""
        print("send vty cmd to cp")
        mock_get_tnpdump_info.return_value = {"cp_addr": "0x1", "spu_addr_list": ["0x1", ], "both_addr_list": ["0x1", ]}
        mock_send_shell_cmd.return_value = self.response["HA_SEIGE_VTY"]
        response = self.ins.send_vty_cmd(device=self.device, cmd="show usp flow resource usage gate", platform="srx345")
        self.assertTrue(re.search(r"root-logical-system", response, re.I))

        print("send vty cmd to spu")
        mock_get_tnpdump_info.return_value = {"cp_addr": "0x1", "spu_addr_list": ["0x2",], "both_addr_list": ["0x1", "0x2", "0x3"]}
        mock_send_shell_cmd.return_value = self.response["HA_SEIGE_VTY"]
        response = self.ins.send_vty_cmd(device=self.device, cmd="show usp flow resource usage gate", platform="srx345", component="SPU")
        self.assertTrue(re.search(r"root-logical-system", response, re.I))

        print("send vty cmd to both")
        mock_get_tnpdump_info.return_value = {"cp_addr": "0x1", "spu_addr_list": ["0x2", ], "both_addr_list": ["0x1", "0x2", "0x3"]}
        mock_send_shell_cmd.return_value = self.response["HA_SEIGE_VTY"]
        response = self.ins.send_vty_cmd(device=self.device, cmd=["ls", "show usp flow resource usage gate"], platform="srx345", component="both")
        self.assertTrue(re.search(r"root-logical-system", response, re.I))

        print("send vty cmd to given tnp_addr")
        mock_get_tnpdump_info.return_value = {"cp_addr": "0x1", "spu_addr_list": ["0x2", ], "both_addr_list": ["0x1", "0x2", "0x3"]}
        mock_send_shell_cmd.return_value = self.response["HA_SEIGE_VTY"]
        response = self.ins.send_vty_cmd(device=self.device, cmd="show usp flow resource usage gate", tnpdump_addr="0x1")
        self.assertTrue(re.search(r"root-logical-system", response, re.I))

        print("send vty cmd with invalid option")
        mock_get_tnpdump_info.return_value = {"cp_addr": "0x1", "spu_addr_list": ["0x2", ], "both_addr_list": ["0x1", "0x2", "0x3"]}
        mock_send_shell_cmd.return_value = self.response["HA_SEIGE_VTY"]

        case = False
        try:
            self.ins.send_vty_cmd(device=self.device, cmd=None, tnpdump_addr="0x1")
        except TypeError as err:
            print(err)
            case = True
        self.assertTrue(case)

        print("send vty cmd with invalid option")
        mock_get_tnpdump_info.return_value = {"cp_addr": "0x1", "spu_addr_list": ["0x2", ], "both_addr_list": ["0x1", "0x2", "0x3"]}
        mock_send_shell_cmd.return_value = self.response["HA_SEIGE_VTY"]

        case = False
        try:
            self.ins.send_vty_cmd(device=self.device, cmd="ls", component="unknown")
        except (AttributeError, ValueError) as err:
            print(err)
            case = True
        self.assertTrue(case)

        print("checking option send_cnt")
        mock_get_tnpdump_info.return_value = {"cp_addr": "0x1", "spu_addr_list": ["0x2", ], "both_addr_list": ["0x1", "0x2", "0x3"]}
        mock_send_shell_cmd.return_value = """Couldn't initiate connection rslt:-1 err:Address already in use"""
        response = self.ins.send_vty_cmd(device=self.device, cmd="ls", component="cp", send_cnt=5)
        self.assertTrue(response.count("initiate connection") == 5)

        print("checking option send_cnt with multiple cmds")
        mock_get_tnpdump_info.return_value = {"cp_addr": "0x1", "spu_addr_list": ["0x2", ], "both_addr_list": ["0x1", "0x2", "0x3"]}
        mock_send_shell_cmd.return_value = """Couldn't initiate connection rslt:-1 err:Address already in use"""
        response = self.ins.send_vty_cmd(device=self.device, cmd=["ls", "df -sh", "whoami"], component="cp", send_cnt=5)
        self.assertTrue(response.count("initiate connection") == 15)

        print("checking have option send_cnt but don't need retry")
        mock_get_tnpdump_info.return_value = {"cp_addr": "0x1", "spu_addr_list": ["0x2", ], "both_addr_list": ["0x1", "0x2", "0x3"]}
        mock_send_shell_cmd.return_value = self.response["HA_SEIGE_VTY"]
        response = self.ins.send_vty_cmd(device=self.device, cmd="ls", component="cp", send_cnt=5)
        self.assertTrue(re.search(r"root-logical-system", response, re.I))

        print("checking get root permission before send command")
        mock_su.return_value = False
        case = False
        try:
            self.ins.send_vty_cmd(device=self.device, cmd="ls", component="unknown")
        except Exception as err:
            print(err)
            case = True
        self.assertTrue(case)

        print("checking get root permission before send command")
        mock_su.return_value = False
        case = False
        try:
            self.ins.send_vty_cmd(device=self.device, cmd="ls", component="cp")
        except Exception as err:
            print(err)
            case = True
        self.assertTrue(case)

    @mock.patch.object(dut_tool, "reboot")
    @mock.patch.object(dut_tool, "send_cli_cmd")
    def test_software_install(self, mock_send_cli_cmd, mock_reboot):
        """test software install"""
        print("do software install without reboot")
        mock_send_cli_cmd.return_value = self.response["SRX_SOFTWARE_INSTALL"]
        status = self.ins.software_install(device=Device, package="/var/tmp/aaa.tgz", no_copy=True, no_validate=True, reboot=False)
        self.assertTrue(status)

        print("without reboot, software install failure but still return True")
        mock_send_cli_cmd.return_value = "upgrade software failed"
        status = self.ins.software_install(device=Device, package="/var/tmp/aaa.tgz", no_copy=True, no_validate=True, reboot=False)
        self.assertTrue(status)

        print("do software install with reboot succeed")
        mock_send_cli_cmd.return_value = self.response["SRX_SOFTWARE_INSTALL"]
        mock_reboot.return_value = True
        status = self.ins.software_install(device=Device, package="/var/tmp/aaa.tgz", no_copy=True, no_validate=True, reboot=True)
        self.assertTrue(status)

        print("do software install but reboot failure")
        mock_send_cli_cmd.return_value = self.response["SRX_SOFTWARE_INSTALL"]
        mock_reboot.return_value = False
        status = self.ins.software_install(device=Device, package="/var/tmp/aaa.tgz", no_copy=True, no_validate=True, reboot=True)
        self.assertFalse(status)

    @mock.patch.object(Device, "reboot")
    def test_reboot(self, mock_reboot):
        """Check send VTY command to DUT and get response"""
        print("reboot just one dut")
        mock_reboot.return_value = True
        response = self.ins.reboot(device=self.device)
        self.assertTrue(response)

        print("reboot 2 nodes and 1 AUT")
        mock_reboot.side_effect = [True, True, True]
        response = self.ins.reboot(device=[self.device, self.device, self.device])
        self.assertTrue(response)

        print("reboot 2 nodes with failure")
        mock_reboot.side_effect = [True, False]
        response = self.ins.reboot(device=[self.device, self.device])
        self.assertFalse(response)

        print("reboot 2 nodes with raise")
        mock_reboot.side_effect = [True, RuntimeError]
        response = self.ins.reboot(device=[self.device, self.device])
        self.assertFalse(response)

        print("reboot several nodes not on parallel")
        mock_reboot.side_effect = [True, True, True]
        response = self.ins.reboot(device=[self.device, self.device, self.device], on_parallel=False)
        self.assertTrue(response)

        print("reboot 1 node not on parallel")
        mock_reboot.return_value = False
        response = self.ins.reboot(device=self.device, on_parallel=False)
        self.assertFalse(response)

        print("reboot 1 node with no on_parallel")
        mock_reboot.side_effect = [True, ]
        response = self.ins.reboot(device=self.device, wait="10", timeout="900", check_interval="30")
        self.assertTrue(response)

        print("reboot more node with no on_parallel")
        mock_reboot.side_effect = [True, True]
        response = self.ins.reboot(device=[self.device, self.device])
        self.assertTrue(response)

    @mock.patch.object(Device, "su")
    def test_su(self, mock_su):
        """Test su"""
        print("checking no previous su result")
        mock_su.return_value = True
        response = self.ins.su(device=self.device)
        self.assertTrue(response)

        print("su several devices")
        mock_su.side_effect = [True, True, True]
        response = self.ins.su(device=[self.device, self.device, self.device])
        self.assertTrue(response)

        print("su several devices but got failure")
        mock_su.side_effect = [True, True, False]
        response = self.ins.su(device=[self.device, self.device, self.device])
        self.assertFalse(response)

    @mock.patch.object(Device, "node_name")
    def test_ha_get_node_name(self, mock_node_name):
        """Check send VTY command to DUT and get response"""
        print("get node name")
        mock_node_name.return_value = "node1"
        response = self.ins.ha_get_node_name(device=self.device)
        self.assertTrue(response == "node1")

        print("get node name")
        mock_node_name.side_effect = Exception
        response = self.ins.ha_get_node_name(device=self.device)
        self.assertFalse(response)

    @mock.patch.object(Device, "node_status")
    def test_ha_get_rg_status(self, mock_node_status):
        """Check send VTY command to DUT and get response"""
        print("get one rg status")
        mock_node_status.return_value = "primary"
        response = self.ins.ha_get_rg_status(device=self.device, rg="0")
        self.assertTrue("primary" in response)

        print("get list of rg status")
        mock_node_status.return_value = "primary"
        response = self.ins.ha_get_rg_status(device=self.device, rg=[0, 1, 3])
        self.assertTrue(len(response) == 3)
        self.assertTrue("primary" in response)

        print("check invalid rg number")
        mock_node_status.return_value = "primary"

        case = False
        try:
            self.ins.ha_get_rg_status(device=self.device, rg=None)
        except TypeError as err:
            print(err)
            case = True
        self.assertTrue(case)

        print("check get status but got raise")
        mock_node_status.side_effect = TypeError
        response = self.ins.ha_get_rg_status(device=self.device)
        self.assertFalse(response)

    @mock.patch.object(Device, "failover")
    def test_ha_do_failover(self, mock_failover):
        """Check send VTY command to DUT and get response"""
        print("one rg do failover")
        mock_failover.return_value = True
        response = self.ins.ha_do_failover(device=self.device, rg="0", node=0)
        self.assertTrue(response)


        print("one rg do failover if all succeed")
        mock_failover.return_value = True
        response = self.ins.ha_do_failover(device=self.device, rg=["0", 1], node=0)
        self.assertTrue(response)

        print("multiple rgs do failover with failure")
        mock_failover.return_value = False
        response = self.ins.ha_do_failover(device=self.device, rg=[0, 1, 2, 3, 4], node=1)
        self.assertFalse(response)

        print("invalid option for rg")
        mock_failover.return_value = True
        case = False
        try:
            self.ins.ha_do_failover(device=self.device, rg=None, node=1)
        except TypeError as err:
            print(err)
            case = True
        self.assertTrue(case)

        print("invalid option for node")
        mock_failover.return_value = True
        case = False
        try:
            self.ins.ha_do_failover(device=self.device, rg=0, node=None)
        except TypeError as err:
            print(err)
            case = True
        self.assertTrue(case)

    @mock.patch.object(dut_tool, "send_cli_cmd")
    @mock.patch.object(dut_tool, "get_version_info")
    def test_feature_support_check(self, mock_get_version_info, mock_send_cli_cmd):
        """test feature support check"""
        print("check one feature for SA topo")
        mock_get_version_info.return_value = {"product_model": "srx5400", }
        result = self.ins.feature_support_check(device=None, feature="he")
        self.assertTrue(result)

        result = self.ins.feature_support_check(device=None, feature="LE")
        self.assertFalse(result)

        print("check one feature for HA topo")
        mock_get_version_info.return_value = {
            "node0":        {"product_model": "srx5400", },
            "node1":        {"product_model": "srx5400", },
        }
        result = self.ins.feature_support_check(device=None, feature="he")
        self.assertTrue(result)

        result = self.ins.feature_support_check(device=None, feature="LE")
        self.assertFalse(result)

        print("check several feature for SA topo don't have license")
        mock_get_version_info.return_value = {"product_model": "srx345", }

        result = self.ins.feature_support_check(device=None, feature=["he", ])
        mock_send_cli_cmd
        self.assertFalse(result)

        result = self.ins.feature_support_check(device=None, feature=["LE", "LSYS"])
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SINGLE_REMAINING_TIME_LICENSE"])
        self.assertFalse(result)

        print("check several feature for SA topo and have license")
        mock_get_version_info.return_value = mock_get_version_info.return_value = {
            "node0":        {"product_model": "srx5400", },
            "node1":        {"product_model": "srx5400", },
        }
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"])
        result = self.ins.feature_support_check(device=None, feature=["he", "LSYS"])
        self.assertTrue(result)

        print("get version info failed")
        mock_get_version_info.return_value = False
        result = self.ins.feature_support_check(device=None, feature=["he", ])
        self.assertFalse(result)

        print("not supported alias")
        mock_get_version_info.return_value = {"product_model": "srx345", }
        result = self.ins.feature_support_check(device=None, feature="Unknown_Alias")
        self.assertFalse(result)

        print("testing other feature supported alias")
        mock_send_cli_cmd.side_effect = (
            self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"]),
            self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"]),
            self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"]),
            self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"]),
            self.xml.xml_string_to_dict(self.response["MULTI_LICENSE"]),
        )
        result = self.ins.feature_support_check(device=None, feature=("VPN", "virtual_APPLIANCE", "idp_sig", "APPID_SIG"))
        self.assertTrue(result)
