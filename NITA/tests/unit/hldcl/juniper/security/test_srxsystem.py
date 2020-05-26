"""All UT cases for srxsystem module"""

import os
import re
import inspect
from lxml import etree
import unittest2 as unittest
from mock import patch, MagicMock, Mock
# from nose.plugins.attrib import attr
import xml.etree.ElementTree as ET
import jxmlease
from collections import defaultdict
from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem
from jnpr.toby.exception.toby_exception import TobyException


class Response:
    """Response Class"""
    # To return response of shell() method
    def __init__(self, x="", y=0):
        """INIT"""
        self.resp = x
        self.stat = y

    def response(self):
        """Response"""
        return self.resp

    def status(self):
        """Status"""
        return self.stat

def get_file_path(file_name):
    """Test Function"""
    path = os.path.dirname(__file__)
    file = os.path.join(path, file_name)
    return file

class TestSrxSystem(unittest.TestCase):
    """Test SrxSystem Class"""
    def setUp(self):
        """Setup"""
        import builtins
        builtins.t = self
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()
        self.to_xml_object = lambda x: etree.fromstring(x)
        self.to_xml_dict = lambda x: jxmlease.parse(x)
        self.get_current_function_name = lambda: inspect.stack()[1][3]

        self.response = {}
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

        self.response["SA_OTHER_TNPDUMP"] = """
   Name                TNPaddr   MAC address    IF     MTU E H R
master                   0x1 02:00:00:00:00:04 em0    1500 0 0 3
master                   0x1 02:00:01:00:00:04 em1    1500 0 1 3
re0                      0x4 02:00:00:00:00:04 em0    1500 0 0 3
re0                      0x4 02:00:01:00:00:04 em1    1500 0 1 3
fpc1                    0x11 02:00:00:00:00:11 em0    1500 4 0 3
fpc2                    0x12 02:00:00:00:00:12 em0    1500 4 0 3
fpc2.pic0              0x112 02:00:10:00:01:12 em0    1500 2 0 3
fpc2.pic1              0x212 02:00:10:00:02:12 em0    1500 2 0 3
fpc2.pic2              0x312 02:00:10:00:03:12 em0    1500 3 0 3
fpc2.pic3              0x412 02:00:10:00:04:12 em0    1500 3 0 3
fpc3.pic0              0x112 02:00:10:00:01:12 em0    1500 2 0 3
fpc3.pic1              0x212 02:00:10:00:02:12 em0    1500 2 0 3
fpc3.pic2              0x312 02:00:10:00:03:12 em0    1500 3 0 3
fpc3.pic3              0x412 02:00:10:00:04:12 em0    1500 3 0 3
bcast             0xffffffff ff:ff:ff:ff:ff:ff em0    1500 0 0 3
bcast             0xffffffff ff:ff:ff:ff:ff:ff em1    1500 0 1 3
        """

        self.response["MULTI_LICENSE"] = """
    <license-usage-summary>
        <features-used/>
        <feature-summary>
            <name>idp-sig</name>
            <description>IDP Signature</description>
            <licensed>1</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <end-date>2018-12-25</end-date>
        </feature-summary>
        <feature-summary>
            <name>appid-sig</name>
            <description>APPID Signature</description>
            <licensed>1</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <end-date>2018-12-25</end-date>
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
                <remaining-validity-value>29 days</remaining-validity-value>
            </remaining-time>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["SINGLE_PERMANENT_LICENSE"] = """
    <license-usage-summary>
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
    <license-usage-summary>
        <feature-summary>
            <name>idp-sig</name>
            <description>IDP Signature</description>
            <licensed>1</licensed>
            <used-licensed>0</used-licensed>
            <needed>0</needed>
            <end-date>2018-12-25</end-date>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["SINGLE_REMAINING_TIME_LICENSE"] = """
    <license-usage-summary>
        <feature-summary>
            <name>Virtual Appliance</name>
            <description>Virtual Appliance</description>
            <licensed>1</licensed>
            <used-licensed>1</used-licensed>
            <needed>0</needed>
            <remaining-time>
                <remaining-validity-value>29 days</remaining-validity-value>
            </remaining-time>
        </feature-summary>
    </license-usage-summary>
        """

        self.response["HA_HE_FAILOVER_RG0_NODE0_SECONDARY"] = """
    <chassis-cluster-status>
        <cluster-id>1</cluster-id>
        <redundancy-group>
            <cluster-id>1</cluster-id>
            <redundancy-group-id>0</redundancy-group-id>
            <redundancy-group-failover-count>6</redundancy-group-failover-count>
            <device-stats>
                <device-name>node0</device-name>
                <device-priority>200</device-priority>
                <redundancy-group-status>secondary</redundancy-group-status>
                <preempt>no</preempt>
                <failover-mode>no</failover-mode>
                <monitor-failures>None</monitor-failures>
                <device-name>node1</device-name>
                <device-priority>1</device-priority>
                <redundancy-group-status>primary</redundancy-group-status>
                <preempt>no</preempt>
                <failover-mode>no</failover-mode>
                <monitor-failures>None</monitor-failures>
            </device-stats>
        </redundancy-group>
    </chassis-cluster-status>
        """

        self.response["HA_HE_FAILOVER_RG0_NODE0_PRIMARY"] = """
    <chassis-cluster-status>
        <cluster-id>1</cluster-id>
        <redundancy-group>
            <cluster-id>1</cluster-id>
            <redundancy-group-id>0</redundancy-group-id>
            <redundancy-group-failover-count>6</redundancy-group-failover-count>
            <device-stats>
                <device-name>node0</device-name>
                <device-priority>200</device-priority>
                <redundancy-group-status>primary</redundancy-group-status>
                <preempt>no</preempt>
                <failover-mode>no</failover-mode>
                <monitor-failures>None</monitor-failures>
                <device-name>node1</device-name>
                <device-priority>1</device-priority>
                <redundancy-group-status>secondary</redundancy-group-status>
                <preempt>no</preempt>
                <failover-mode>no</failover-mode>
                <monitor-failures>None</monitor-failures>
            </device-stats>
        </redundancy-group>
    </chassis-cluster-status>
        """

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

    @patch('jnpr.toby.hldcl.juniper.security.srxsystem.jxmlease.parse')
    @patch('jnpr.toby.hldcl.juniper.security.srxsystem.JuniperSystem.__init__')
    def test_srxsystem_init(self, sup_init_patch, jxm_patch):
        """Unit Test"""
        sobject = MagicMock()
        SrxSystem.nodes = {}
        SrxSystem.nodes['primary'] = MagicMock(return_value=sobject)
        sobject.current_controller = True
        SrxSystem.current_node = MagicMock()

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        jxm_patch.return_value = {'rpc-reply': {'multi-routing-engine-results': "results"}}
        self.assertIsInstance(SrxSystem(system_data), SrxSystem)
        self.assertTrue(sup_init_patch.called)

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        system_data['system']['primary']['controllers']['re0']['connect'] = True
        SrxSystem.is_node_connect_set = MagicMock(return_value=True)
        self.assertIsInstance(SrxSystem(system_data), SrxSystem)

        init_data = create_init_data()
        system_data = init_data['t']['resources']['r0']
        SrxSystem.nodes['test2'] = MagicMock(return_value=sobject)
        self.assertIsInstance(SrxSystem(system_data), SrxSystem)

        SrxSystem.nodes['primary'] = sobject
        sobject.is_node_status_primary = MagicMock(return_value=True)
        self.assertIsInstance(SrxSystem(system_data), SrxSystem)
        sobject.is_node_status_primary = MagicMock(return_value=False)
        self.assertIsInstance(SrxSystem(system_data), SrxSystem)

        SrxSystem.nodes.pop('test2')
        jxm_patch.return_value = {'rpc-reply':{}}
        system_data['system']['primary']['connect'] = None
        self.assertIsInstance(SrxSystem(system_data), SrxSystem)

    def test_srxsystem_is_ha(self):
        """Unit Test"""
        sobject = MagicMock(spec=SrxSystem)
        sobject.ha = True
        self.assertTrue(SrxSystem.is_ha(sobject))
        sobject.ha = False
        self.assertFalse(SrxSystem.is_ha(sobject))

    def test_srxsystem_node_name(self):
        """Unit Test"""
        sobject = MagicMock(spec=SrxSystem)
        sobject.ha = True
        sobject.current_node.node_name.return_value = "test"
        self.assertEqual(SrxSystem.node_name(sobject), "test")

        # Exception
        sobject.ha = False
        self.assertRaises(Exception, SrxSystem.node_name, sobject)

    def test_srxsystem_node_status(self):
        """Unit Test"""
        sobject = MagicMock(spec=SrxSystem)
        sobject.ha = True
        ha_status = {'r0':{'status':'test'}}
        sobject.node_name.return_value = "r0"
        sobject.ha_status.return_value = ha_status
        self.assertEqual(SrxSystem.node_status(sobject), "test")

        # Exception
        sobject.ha = False
        self.assertRaises(Exception, SrxSystem.node_status, sobject)

    def test_srxsystem_ha_status(self):
        """Unit Test"""
        sobject = MagicMock(spec=SrxSystem)

        # Exception
        sobject.ha = False
        self.assertRaises(Exception, SrxSystem.ha_status, sobject)

        sobject.ha = True
        sobject.current_node = MagicMock()
        sobject.current_node.current_controller.channels['pyez'].cli = MagicMock()

        # Exception
        self.assertRaises(Exception, SrxSystem.ha_status, sobject)

        with patch('jnpr.toby.hldcl.juniper.security.srxsystem.jxmlease') as jxm_patch:
            # Exception
            jxm_patch.parse_etree.return_value = None
            self.assertRaises(Exception, SrxSystem.ha_status, sobject, rg='0')

            status = defaultdict(lambda: defaultdict(dict))
            status = status['chassis-cluster-status']['redundancy-group']['device-stats'] =\
                     defaultdict(lambda: defaultdict(dict))

            status['device-name'][0] = 'device'
            status['device-priority'][0] = 'priority'
            status['redundancy-group-status'][0] = 'rg-status'
            status['preempt'][0] = 'preempt'
            status['failover-mode'][0] = 'mode'
            status['monitor-failures'][0] = 'failures'
            status['device-name'][1] = 'device'
            status['device-priority'][1] = 'priority'
            status['redundancy-group-status'][1] = 'rg-status'
            status['preempt'][1] = 'preempt'
            status['failover-mode'][1] = 'mode'
            status['monitor-failures'][1] = 'failures'

            jxm_patch.parse_etree.return_value = status

            node = defaultdict(lambda: defaultdict(dict))
            node['name'] = 'device'
            node['priority'] = 'priority'
            node['status'] = 'rg-status'
            node['preempt'] = 'preempt'
            node['failover-mode'] = 'mode'
            node['monitor-failures'] = 'failures'

            self.assertEqual(SrxSystem.ha_status(sobject, rg='0'), {'node0':node, 'node1':node})

    @patch('jnpr.toby.hldcl.juniper.security.srxsystem.time')
    @patch('jnpr.toby.hldcl.juniper.security.srxsystem.jxmlease.parse_etree',
           return_value={'chassis-cluster-status': {'redundancy-group': {'device-stats': {'preempt':['yes', 'yes']}}}})
    def test_srxsystem_failover(self, xmlpatch, patch_time):
        """Unit Test"""
        sobject = MagicMock(spec=SrxSystem)
        patch_time.return_value = True

        # Exception
        sobject.complex_system = False
        self.assertRaisesRegex(Exception, r"This is not an SRX/VSRX complex system", SrxSystem.failover, sobject)

        # normal check
        res_object = Mock()
        res_object.response = Mock()

        sobject.complex_system = True
        sobject.switch_to_primary_node.return_value = True
        sobject.log = MagicMock()
        sobject.cli.return_value = res_object
        sobject.get_current_function_name = Mock(return_value="failover")

        a_status = defaultdict(lambda: defaultdict(dict))
        b_status = defaultdict(lambda: defaultdict(dict))

        # node0 do failover
        a_status['node0']['status'] = "primary"
        a_status['node0']['priority'] = "200"
        a_status['node1']['status'] = "secondary"
        a_status['node1']['priority'] = "1"
        b_status['node0']['status'] = "secondary"
        b_status['node0']['priority'] = "200"
        b_status['node1']['status'] = "primary"
        b_status['node1']['priority'] = "1"

        sobject._transit_node_alias.return_value = "1"
        sobject.ha_status.side_effect = [a_status, b_status]
        res_object.response.side_effect = ["", "", self.to_xml_object(self.response["HA_HE_FAILOVER_RG0_NODE0_SECONDARY"])]
        response = SrxSystem.failover(sobject, node="0")
        self.assertTrue(response)
        self.assertTrue(sobject.log.called)

        # without argument 'node'
        b_status['node0']['status'] = "primary"
        b_status['node0']['priority'] = "0"
        b_status['node1']['status'] = "secondary"
        b_status['node1']['priority'] = "0"
        sobject.ha_status.side_effect = [
            b_status, b_status, b_status, b_status, b_status, b_status, b_status, b_status, b_status, b_status, b_status, b_status, b_status,
            b_status, b_status, b_status,
        ]
        res_object.response.side_effect = ["", "", ""]
        self.assertFalse(SrxSystem.failover(sobject))

        a_status['node0']['status'] = "secondary"
        a_status['node1']['status'] = "primary"
        sobject.ha_status.side_effect = [a_status, a_status]
        res_object.response.side_effect = ["", "", self.to_xml_object(self.response["HA_HE_FAILOVER_RG0_NODE0_SECONDARY"])]
        self.assertTrue(SrxSystem.failover(sobject, node="1", timeout="10"))
        self.assertTrue(sobject.log.called)

        # without argument 'node'
        res_object.response.side_effect = ["", "", ""]
        a_status['node0']['status'] = "None"
        a_status['node1']['status'] = "secondary"
        self.assertRaisesRegex(TobyException, r"Cannot find primary node", SrxSystem.failover, sobject)

        sobject.cli.return_value.response = MagicMock()

        # failover rg0 to node0
        a_status['node0']['status'] = "secondary"
        a_status['node0']['priority'] = "200"
        a_status['node1']['status'] = "primary"
        a_status['node1']['priority'] = "0"

        b_status['node0']['status'] = "primary"
        b_status['node0']['priority'] = "1"
        b_status['node1']['status'] = "secondary"
        b_status['node1']['priority'] = "1"
        sobject.ha_status.side_effect = [a_status, b_status, b_status]
        sobject._transit_node_alias.return_value = "0"
        self.assertTrue(SrxSystem.failover(sobject, node="0", force=True))
        self.assertTrue(sobject.log.called)

        # with argument 'rg'
        sobject.ha_status.side_effect = [a_status, b_status]
        self.assertTrue(SrxSystem.failover(sobject, node="0", rg="1"))
        self.assertTrue(sobject.log.called)

        # with option "force"
        sobject.ha_status.side_effect = [a_status, b_status]
        self.assertTrue(SrxSystem.failover(sobject, force=True, node="2", check_interval=0.0001, check_cnt=1))

        # option node is None, but need failover to node0
        a_status['node0']['status'] = "secondary"
        a_status['node0']['priority'] = "200"
        a_status['node1']['status'] = "primary"
        a_status['node1']['priority'] = "1"
        b_status['node0']['status'] = "primary"
        b_status['node0']['priority'] = "1"
        b_status['node1']['status'] = "secondary"
        b_status['node1']['priority'] = "200"
        sobject.ha_status.side_effect = [a_status, b_status]
        sobject._transit_node_alias.side_effect = ["0", "0"]
        xmlpatch.return_value = {'chassis-cluster-status': {'redundancy-group': {'device-stats': {'preempt':['no', 'no']}}}}
        res_object.response.side_effect = ["", "", self.to_xml_object(self.response["HA_HE_FAILOVER_RG0_NODE0_PRIMARY"]), ""]
        self.assertTrue(SrxSystem.failover(sobject, rg=2))
        xmlpatch.return_value = {'chassis-cluster-status': {'redundancy-group': {'device-stats': {'preempt':['yes', 'yes']}}}}

        # don't need do failover
        a_status['node0']['status'] = "primary"
        a_status['node0']['priority'] = "200"
        a_status['node1']['status'] = "secondary"
        a_status['node1']['priority'] = "1"
        sobject.ha_status.side_effect = [a_status, a_status]
        sobject._transit_node_alias.side_effect = ["0", "0"]
        res_object.response.side_effect = ["", "", self.to_xml_object(self.response["HA_HE_FAILOVER_RG0_NODE0_PRIMARY"]), ""]
        self.assertTrue(SrxSystem.failover(sobject, rg=2))

        # multiple rgs
        a_status['node0']['status'] = "primary"
        a_status['node0']['priority'] = "200"
        a_status['node1']['status'] = "secondary"
        a_status['node1']['priority'] = "0"

        b_status['node0']['status'] = "secondary"
        b_status['node0']['priority'] = "1"
        b_status['node1']['status'] = "primary"
        b_status['node1']['priority'] = "200"
        sobject.ha_status.side_effect = [
            a_status, b_status,
            a_status, b_status,
            a_status, b_status,
            a_status, b_status,
            a_status, b_status,
        ]
        res_object.response.side_effect = [
            "", "", self.to_xml_object(self.response["HA_HE_FAILOVER_RG0_NODE0_SECONDARY"]), "",
            "", "", self.to_xml_object(self.response["HA_HE_FAILOVER_RG0_NODE0_SECONDARY"]), "",
            "", "", self.to_xml_object(self.response["HA_HE_FAILOVER_RG0_NODE0_SECONDARY"]), "",
            "", "", self.to_xml_object(self.response["HA_HE_FAILOVER_RG0_NODE0_SECONDARY"]), "",
            "", "", self.to_xml_object(self.response["HA_HE_FAILOVER_RG0_NODE0_SECONDARY"]), "",
        ]
        sobject._transit_node_alias.side_effect = ["1", "1", "1", "1"]
        self.assertTrue(SrxSystem.failover(sobject, node="1", rg=[0, "1", "2", "3"]))

        # invalid testing
        self.assertRaisesRegex(TobyException, r"option 'rg' must be", SrxSystem.failover, sobject, rg=sobject)

        sobject.ha_status.side_effect = TobyException("Have exception", host_obj=sobject)
        self.assertFalse(SrxSystem.failover(sobject, node="1", rg=1))

    def test_srxsystem_switch_node(self):
        """Unit Test"""
        sobject = MagicMock(spec=SrxSystem)

        # Exception
        sobject.complex_system = False
        self.assertRaises(Exception, SrxSystem.switch_node, sobject)

        sobject.complex_system = True
        sobject.current_node = "test"
        sobject.nodes = {'primary': 'test', 'test': 'test1'}
        sobject.slave_name = "test"
        self.assertTrue(SrxSystem.switch_node(sobject))

        sobject.current_node = "test1"
        self.assertTrue(SrxSystem.switch_node(sobject))

        sobject.current_node = "test2"
        self.assertTrue(SrxSystem.switch_node(sobject))

        # node = "0"
        self.assertTrue(SrxSystem.switch_node(sobject, node="0"))

        # node = "1"
        self.assertTrue(SrxSystem.switch_node(sobject, node="1"))

        # Exception
        self.assertRaises(Exception, SrxSystem.switch_node, sobject, node="2")

    def test_srxsystem_switch_to_primary_node(self):
        """Unit Test"""
        sobject = MagicMock(spec=SrxSystem)

        # Exception
        sobject.complex_system = False
        sobject.log = MagicMock()
        self.assertRaises(Exception, SrxSystem.switch_to_primary_node, sobject)
        self.assertTrue(sobject.log.called)

        sobject.complex_system = True
        obj = MagicMock()
        sobject.nodes = {'primary': obj}
        obj.is_node_status_primary = MagicMock(return_value=True)
        self.assertTrue(SrxSystem.switch_to_primary_node(sobject))

        # return FALSE
        obj.is_node_status_primary = MagicMock(return_value=False)
        self.assertFalse(SrxSystem.switch_to_primary_node(sobject))
        sobject.nodes = {}
        self.assertFalse(SrxSystem.switch_to_primary_node(sobject))

    # Mocking the handle and its methods
    mocked_obj = MagicMock(spec=SrxSystem)
    mocked_obj.current_node = MagicMock()
    mocked_obj.current_node.current_controller = MagicMock()
    mocked_obj.node0 = MagicMock()
    mocked_obj.node1 = MagicMock()

    def test_is_multi_spu(self):
        """Unit Test"""
        mocked_obj = Mock()
        mocked_obj.current_node.current_controller.get_model = MagicMock(return_value="srx5800")
        self.assertEqual(SrxSystem.is_multi_spu(mocked_obj), True)

        mocked_obj.current_node.current_controller.get_model.return_value = "vSRX"
        self.assertEqual(SrxSystem.is_multi_spu(mocked_obj), False)

        mocked_obj.current_node.current_controller.get_model.return_value = ""
        mocked_obj.get_version_info.return_value = {"node0": {"product_model": "srx4100"}}
        self.assertEqual(SrxSystem.is_multi_spu(mocked_obj), False)

        mocked_obj.current_node.current_controller.get_model.return_value = ""
        mocked_obj.get_version_info.return_value = {"product_model": "srx5400", }
        self.assertEqual(SrxSystem.is_multi_spu(mocked_obj), True)

    def test_get_platform_type(self):
        """Unit Test"""
        res_object = Mock()
        res_object.response = Mock()
        res_object.response.return_value = "hw.product.model: srxtvp"

        mocked_obj = Mock()
        mocked_obj.current_node.current_controller.shell.return_value = res_object

        mocked_obj.current_node.current_controller.get_model.return_value = "srx300"
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "octeon")

        mocked_obj.current_node.current_controller.get_model.return_value = "vsrx"
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "x86")

        mocked_obj.current_node.current_controller.get_model.return_value = "srx5800"
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "xlp")

        mocked_obj.current_node.current_controller.get_model.return_value = "srx4100"
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "x86")

        mocked_obj.current_node.current_controller.get_model.return_value = "srx5100"
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "x86")

        mocked_obj.current_node.current_controller.get_model.return_value = ""
        mocked_obj.get_version_info.return_value = {"node0": {"product_model": "srx4100"}}
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "x86")

        mocked_obj.current_node.current_controller.get_model.return_value = ""
        mocked_obj.get_version_info.return_value = {"product_model": "srx4100", }
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "x86")

        mocked_obj.current_node.current_controller.get_model.return_value = ""
        mocked_obj.get_version_info.return_value = {"product_model": "nfx150_c_s1", }
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "nfx150")

        mocked_obj.current_node.current_controller.get_model.return_value = ""
        mocked_obj.get_version_info.return_value = {"product_model": "nfx250_s1", }
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "x86")

        mocked_obj.current_node.current_controller.get_model.return_value = ""
        res_object.response.return_value = "hw.product.model: srxtvp"
        mocked_obj.current_node.current_controller.shell.return_value = res_object
        mocked_obj.get_version_info.return_value = {"product_model": "vSRX", }
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "x86")

        mocked_obj.current_node.current_controller.get_model.return_value = ""
        res_object.response.return_value = "hw.product.model: vsrx"
        mocked_obj.get_version_info.return_value = {"product_model": "vSRX", }
        self.assertEqual(SrxSystem.get_platform_type(mocked_obj), "octeon")

    def test_get_srx_pfe_names(self):
        """Unit Test"""
        # Multiple pic values
        flow_details = {
            'fpc-information': {
                'fpc': [
                    {
                        'description': 'SRX5k IOC3 24XGE+6XLG',
                        'pic': {
                            'pic-slot': '0',
                            'pic-state': 'Online',
                            'pic-type': '12x 10GE SFP+'
                        },
                        'slot': '3'
                    },
                    {
                        'description': 'SRX5k SPC II',
                        'pic': [
                            {
                                'pic-slot': '0',
                                'pic-state': 'Online',
                                'pic-type': 'SPU Cp'
                            },
                            {
                                'pic-slot': '1',
                                'pic-state': 'Online',
                                'pic-type': 'SPU Flow'
                            },
                            {
                                'pic-slot': '2',
                                'pic-state': 'Online',
                                'pic-type': 'SPU Flow'
                            }
                        ],
                        'slot': '4',
                        'state': 'Online'
                    }
                ]
            }
        }
        flow_details1 = {
            'fpc-information': {
                'fpc': [
                    {
                        'description': 'SRX5k IOC3 24XGE+6XLG',
                        'pic': {
                            'pic-slot': '0',
                            'pic-state': 'Online',
                            'pic-type': '12x 10GE SFP+'
                        },
                        'slot': '3'
                    },
                    {
                        'description': 'SRX5k SPC II',
                        'pic': {
                            'pic-slot': '0',
                            'pic-state': 'Online',
                            'pic-type': 'SPU Flow'
                        },
                        'slot': '4',
                        'state': 'Online'
                    }
                ]
            }
        }
        flow_details_ha = [
            {
                're-name': 'node0',
                'fpc-information': {
                    'fpc': [
                        {
                            'description': 'SRX5k IOC3 24XGE+6XLG',
                            'pic': {
                                'pic-slot': '0',
                                'pic-state': 'Online',
                                'pic-type': '12x 10GE SFP+'
                            },
                            'slot': '3'
                        },
                        {
                            'description': 'SRX5k SPC II',
                            'pic': [
                                {
                                    'pic-slot': '0',
                                    'pic-state': 'Online',
                                    'pic-type': 'SPU Cp'
                                },
                                {
                                    'pic-slot': '1',
                                    'pic-state': 'Online',
                                    'pic-type': 'SPU Flow'
                                },
                                {
                                    'pic-slot': '2',
                                    'pic-state': 'Online',
                                    'pic-type': 'SPU Flow'
                                }
                            ],
                            'slot': '4',
                            'state': 'Online'
                        }
                    ]
                }
            },
            {
                're-name': 'node1',
                'fpc-information': {
                    'fpc': [
                        {
                            'description': 'SRX5k IOC3 24XGE+6XLG',
                            'pic': {
                                'pic-slot': '0',
                                'pic-state': 'Online',
                                'pic-type': '12x 10GE SFP+'
                            },
                            'slot': '3'
                        },
                        {
                            'description': 'SRX5k SPC II',
                            'pic': [
                                {
                                    'pic-slot': '0',
                                    'pic-state': 'Online',
                                    'pic-type': 'SPU Cp'
                                },
                                {
                                    'pic-slot': '1',
                                    'pic-state': 'Online',
                                    'pic-type': 'SPU Flow'
                                },
                                {
                                    'pic-slot': '2',
                                    'pic-state': 'Online',
                                    'pic-type': 'SPU Flow'
                                }
                            ],
                            'slot': '4',
                            'state': 'Online'
                        }
                    ]
                }
            }
        ]
        flow_details_ha_node1 = {
            're-name': 'node1',
            'fpc-information': {
                'fpc': [
                    {
                        'description': 'SRX5k IOC3 24XGE+6XLG',
                        'pic': {
                            'pic-slot': '0',
                            'pic-state': 'Online',
                            'pic-type': '12x 10GE SFP+'
                        },
                        'slot': '3'
                    },
                    {
                        'description': 'SRX5k SPC II',
                        'pic':  {
                            'pic-slot': '1',
                            'pic-state': 'Online',
                            'pic-type': 'SPU Flow'
                        },
                        'slot': '4',
                        'state': 'Online'
                    }
                ]
            }
        }
        # Checking single spu path
        mocked_obj = Mock()
        mocked_obj.is_multi_spu.return_value = False
        mocked_obj.get_platform_type.return_value = "octeon"
        self.assertEqual(SrxSystem.get_srx_pfe_names(mocked_obj), ["fwdd"])
        mocked_obj.get_platform_type = MagicMock(return_value="x86")
        self.assertEqual(SrxSystem.get_srx_pfe_names(mocked_obj), ["fpc0"])
        mocked_obj.get_platform_type.return_value = "test"
        self.assertEqual(SrxSystem.get_srx_pfe_names(mocked_obj), [])

        # Checking multiple spu
        mocked_obj.is_multi_spu = MagicMock(return_value=True)
        mocked_obj.get_platform_type = MagicMock(return_value="xlp")

        mocked_obj.is_ha = MagicMock(return_value=False)
        mocked_obj.execute_as_rpc_command = MagicMock(return_value=flow_details)
        self.assertEqual(SrxSystem.get_srx_pfe_names(mocked_obj), ['fpc4.pic1', 'fpc4.pic2'])
        mocked_obj.execute_as_rpc_command = MagicMock(return_value=flow_details1)
        self.assertEqual(SrxSystem.get_srx_pfe_names(mocked_obj), ['fpc4.pic0'])

        mocked_obj.is_ha = MagicMock(return_value=True)
        mocked_obj.execute_as_rpc_command = MagicMock(return_value=flow_details_ha)
        self.assertEqual(SrxSystem.get_srx_pfe_names(mocked_obj), ['node0.fpc4.pic1', 'node0.fpc4.pic2', 'node1.fpc4.pic1', 'node1.fpc4.pic2'])
        mocked_obj.execute_as_rpc_command = MagicMock(return_value=flow_details_ha_node1)
        self.assertEqual(SrxSystem.get_srx_pfe_names(mocked_obj, node="node1"), ['node1.fpc4.pic1'])

    def test_cli(self):
        """Unit Test"""
        # Error condition checking
        mocked_obj = Mock()
        mocked_obj.channels = []
        mocked_obj.name = 'foo'
        try:
            SrxSystem.cli(mocked_obj, command=None)
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory argument 'command' is missing!")

        mocked_obj.is_ha = MagicMock(return_value=False)
        mocked_obj.current_node.current_controller.cli = MagicMock(return_value=Response("14.1R1"))
        self.assertEqual(SrxSystem.cli(mocked_obj, command="show version").response(), "14.1R1")

        # HA path testing.
        mocked_obj.is_ha = MagicMock(return_value=True)
        self.assertEqual(SrxSystem.cli(mocked_obj, command="show version").response(), "14.1R1")
        self.assertEqual(SrxSystem.cli(mocked_obj, command="show version", node="node0").response(), "14.1R1")
        self.assertEqual(SrxSystem.cli(mocked_obj, command="show version", node="node1").response(), "14.1R1")
        self.assertEqual(SrxSystem.cli(mocked_obj, command="show version", node="local").response(), "14.1R1")
        mocked_obj.node0.cli = MagicMock(return_value=Response("15.1R1"))
        self.assertEqual(SrxSystem.cli(mocked_obj, command="show version", execution_node="node0").response(), "15.1R1")
        mocked_obj.node1.cli = MagicMock(return_value=Response("16.1R1"))
        self.assertEqual(SrxSystem.cli(mocked_obj, command="show version", execution_node="node1").response(), "16.1R1")
        # Error handling for HA path
        try:
            SrxSystem.cli(mocked_obj, command="show version", node="nodetest")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid HA Node value for output. Supported values are None(default)/node0/node1/local")
        try:
            SrxSystem.cli(mocked_obj, command="show version", execution_node="nodetest")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid HA Node for execution. Supported values are None(default)/node0/node1")

    def test_get_platform_type_wrapper(self):
        """Unit Test"""
        from jnpr.toby.hldcl.juniper.security import srxsystem
        dev = MagicMock()
        dev.get_platform_type.return_value = "xlp"
        self.assertEqual("xlp", srxsystem.get_platform_type(dev))

    def test_execute_as_rpc_command(self):
        """Unit Test"""
        mocked_obj = Mock()
        mocked_obj.channels = []
        mocked_obj.name = 'foo'
        # Error condition checking
        try:
            SrxSystem.execute_as_rpc_command(mocked_obj, command=None)
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory argument 'command' is missing!")
        try:
            SrxSystem.execute_as_rpc_command(mocked_obj, command="show version", command_type="test")
        except Exception as err:
            self.assertEqual(err.args[0], "incorrect command_type: test")
        try:
            SrxSystem.execute_as_rpc_command(mocked_obj, command="show version",
                                             execution_node="node3")
        except Exception as err:
            self.assertEqual(err.args[0], 'Invalid HA Node for execution. Supported values are None(default)/node0/node1')

        # Values used in testing
        rpc_response = "b'<software-information><host-name>srxdpi-vsrx17</host-name><product-model>vsrx" \
                       "</product-model><product-name>vsrx</product-name></software-information>'"
        parsed_values = {'software-information': {'host-name': 'srxdpi-vsrx17',
                                                  'product-model': 'vsrx',
                                                  'product-name': 'vsrx'}}
        parsed_values_ha = {'multi-routing-engine-results': {'multi-routing-engine-item': [{'re-name': 'node0',
                                                                                            'software-information': {
                                                                                                'host-name': 'bichiya',
                                                                                                'product-model': 'srx5600',
                                                                                                'product-name': 'srx5600'}},
                                                                                           {'re-name': 'node1',
                                                                                            'software-information': {
                                                                                                'host-name': 'beehar',
                                                                                                'product-model': 'srx5600',
                                                                                                'product-name': 'srx5600'}}]}}
        parsed_values_all = parsed_values_ha['multi-routing-engine-results']['multi-routing-engine-item']
        parsed_values_node0 = parsed_values_all[0]
        parsed_values_node1 = parsed_values_all[1]
        # Non HA related path
        mocked_obj.is_ha = MagicMock(return_value=False)
        mocked_obj.get_rpc_equivalent = MagicMock(return_value="<get-software-information/>")
        jxmlease.parse_etree = MagicMock(return_value=parsed_values)
        mocked_obj.current_node.current_controller.execute_rpc = MagicMock(return_value=Response(rpc_response))
        mocked_obj.node0.execute_rpc = MagicMock(return_value=Response(rpc_response))
        mocked_obj.node1.execute_rpc = MagicMock(return_value=Response(rpc_response))
        self.assertEqual(SrxSystem.execute_as_rpc_command(mocked_obj, command="show version"), parsed_values)
        self.assertEqual(SrxSystem.execute_as_rpc_command(mocked_obj, command="show version", command_type="rpc"), parsed_values)

        # eTree obj is True
        mocked_obj.current_node.current_controller.execute_rpc = MagicMock(return_value=Response(True))
        self.assertEqual(SrxSystem.execute_as_rpc_command(mocked_obj, command="show version"), None)

        # HA related
        mocked_obj.is_ha = MagicMock(return_value=True)
        jxmlease.parse_etree = MagicMock(return_value=parsed_values_ha)
        mocked_obj.node_name = MagicMock(return_value="node0")
        self.assertEqual(SrxSystem.execute_as_rpc_command(mocked_obj, command="show version"), parsed_values_node0)
        self.assertEqual(SrxSystem.execute_as_rpc_command(mocked_obj, command="show version", node=None), parsed_values_ha)
        self.assertEqual(SrxSystem.execute_as_rpc_command(mocked_obj, command="show version", node="all"), parsed_values_all)
        self.assertEqual(SrxSystem.execute_as_rpc_command(mocked_obj, command="show version", execution_node="node0"), parsed_values_node0)
        self.assertEqual(SrxSystem.execute_as_rpc_command(mocked_obj, command="show version", node="node0"), parsed_values_node0)
        self.assertEqual(SrxSystem.execute_as_rpc_command(mocked_obj, command="show version", execution_node="node1"), parsed_values_node1)
        self.assertEqual(
            SrxSystem.execute_as_rpc_command(mocked_obj, command="show version", execution_node="node1", node="node1"),
            parsed_values_node1)
        # Check error condition
        try:
            SrxSystem.execute_as_rpc_command(mocked_obj, command="show version", execution_node="node1", node="test")
        except ValueError as err:
            self.assertEqual(err.args[0], 'Invalid HA Node value for output. Supported None/all/node0/node1/local(default)')

        mocked_obj.node_name = MagicMock(return_value="node2")
        try:
            SrxSystem.execute_as_rpc_command(mocked_obj, command="show version")
        except ValueError as err:
            self.assertEqual(err.args[0], "Node name node2 not found in the status output")

        # eTree having dict output
        parsed_values_dict = {'multi-routing-engine-results': {'multi-routing-engine-item': {'re-name': 'node0',
                                                                                             'software-information': {
                                                                                                 'host-name': 'bichiya',
                                                                                                 'product-model': 'srx5600',
                                                                                                 'product-name': 'srx5600'}}}}
        jxmlease.parse_etree = MagicMock(return_value=parsed_values_dict)
        self.assertEqual(
            SrxSystem.execute_as_rpc_command(mocked_obj, command="show version"),
            parsed_values_dict['multi-routing-engine-results']['multi-routing-engine-item']
        )

    @patch('time.sleep')
    def test_verify_pic_status(self, mock_sleep):
        """Unit Test"""
        sobject = MagicMock(spec=SrxSystem)
        sobject.channels = []
        sobject.name = 'foo'
        mock_sleep.return_value = True
        tree = ET.parse(get_file_path('pic_status.xml'))
        root_elem = tree.getroot()
        response_object = MagicMock()
        response_object.response = MagicMock(return_value=root_elem)

        sobject.log = MagicMock(return_value=True)
        sobject.get_rpc_equivalent = MagicMock(return_value='<get-pic-information/>')
        sobject.execute_rpc = MagicMock(return_value=response_object)
        self.assertTrue(SrxSystem.verify_pic_status(sobject))

        # case where pic is offline
        tree = ET.parse(get_file_path('pic_status_offline.xml'))
        root_elem = tree.getroot()
        response_object = MagicMock()
        response_object.response = MagicMock(return_value=root_elem)
        sobject.execute_rpc = MagicMock(return_value=response_object)
        try:
            SrxSystem.verify_pic_status(sobject)
        except Exception as err:
            self.assertEqual("Pics are not online", err.args[0])

    def test_vty(self):
        """Unit Test"""
        # res_object = Mock()
        # res_object.response = Mock()
        # res_object.status = Mock()

        # dev_object = Mock(spec=SrxSystem)
        # dev_object.get_current_function_name = lambda: inspect.stack()[1][3]
        # dev_object.su = Mock()
        # dev_object.get_tnpdump_info = Mock()
        # dev_object.vty.return_value = res_object
        # dev_object.shell.return_value = res_object
        # dev_object.vty = Mock()
        # dev_object.shell = Mock()
        #
        # # compatible checking
        # dev_object.current_node = Mock()
        # dev_object.current_node.current_controller = Mock()
        # dev_object.current_node.current_controller.vty = Mock()
        # dev_object.current_node.current_controller.vty.return_value = res_object

        # try:
        #     SrxSystem.cli(mocked_obj, command=None)
        #     SrxSystem.cli(mocked_obj, command=None)
        # except Exception as err:
        #     self.assertEqual(err.args[0], "Mandatory argument 'command' is missing!")

        mocked_obj = Mock()
        mocked_obj.current_node.current_controller.cli = Mock()
        mocked_obj.current_node.current_controller.vty = Mock()
        mocked_obj.get_current_function_name = self.get_current_function_name
        mocked_obj.shell = Mock()
        mocked_obj.runtime = {}
        mocked_obj.su = Mock()
        mocked_obj.is_ha = Mock()
        mocked_obj.get_tnpdump_info = Mock()

        mocked_obj.current_node.current_controller.vty.return_value = Response("VTY response")
        response = SrxSystem.vty(mocked_obj, command="show memory", destination="SET", pattern="have pattern").response()
        self.assertRegex(response, "VTY response")

        # single cmd to given node
        mocked_obj.su.return_value = True
        mocked_obj.shell.return_value = Response("show memory response")
        mocked_obj.get_tnpdump_info.return_value = {"cp_addr": "fwdd", "spu_addr_list": ["fwdd", ], "both_addr_list": ["fwdd", ]}
        response = SrxSystem.vty(mocked_obj, command="show memory", destination="cp").response()
        self.assertRegex(response, "memory response")

        # multiple cmd to specific destination
        cmds = (
            "vty cmd 1",
            "vty cmd 2",
        )
        mocked_obj.shell.side_effect = [
            Response("vty cmd 1 spu1 response"),
            Response("vty cmd 1 spu2 response"),
            Response("vty cmd 2 spu1 response"),
            Response("vty cmd 2 spu2 response"),
        ]
        mocked_obj.get_tnpdump_info.return_value = {
            "cp_addr": "0x1000100",
            "spu_addr_list": ["0x1000200", "0x1000300"],
            "both_addr_list": ["0x1000100", "0x1000200", "0x1000300"],
        }
        response = SrxSystem.vty(mocked_obj, command=cmds, destination="spu").response()
        self.assertRegex(response, "cmd 1 spu1 response")
        self.assertRegex(response, "cmd 2 spu2 response")

        # multiple cmd to cp destination
        cmds = (
            "vty cmd 1",
            "vty cmd 2",
        )
        mocked_obj.shell.side_effect = [Response("vty cmd 1 cp response"), Response("vty cmd 2 cp response")]
        response = SrxSystem.vty(mocked_obj, command=cmds, destination="cp").response()
        self.assertRegex(response, "cmd 1 cp response")
        self.assertRegex(response, "cmd 2 cp response")

        # single cmd cp all destination
        mocked_obj.shell.side_effect = [Response("vty cp response"), Response("vty spu1 response"), Response("vty spu2 response")]
        mocked_obj.is_ha.return_value = True
        response = SrxSystem.vty(mocked_obj, command="show memory", destination="all").response()
        self.assertRegex(response, "vty cp response")
        self.assertRegex(response, "vty spu2 response")
        mocked_obj.is_ha.return_value = False

        # send cmd several times
        mocked_obj.shell.side_effect = [
            Response("Couldn't initiate connection"),
            Response("Couldn't initiate connection"),
            Response("vty response")
        ]
        response = SrxSystem.vty(mocked_obj, command="show memory", retry_cnt=3).response()
        self.assertRegex(response, "vty response")

        # customize option 'destination'
        mocked_obj.shell.side_effect = [Response("fpc0 response"), Response("fpc0 response")]
        mocked_obj.is_ha.return_value = True
        response = SrxSystem.vty(mocked_obj, command=["show memory", "show memory"], destination="node1.fpc0").response()
        self.assertRegex(response, "fpc0 response")

        # option "force_on_primary_node" check
        mocked_obj.is_ha.return_value = True
        mocked_obj.switch_to_primary_node = Mock(return_value=True)
        mocked_obj.shell.side_effect = [
            Response("vty response")
        ]
        response = SrxSystem.vty(mocked_obj, command="show memory", destination="cp", force_on_primary_node=True).response()
        self.assertRegex(response, "vty response")

        # option "node" and "force_on_primary_node" all set check
        mocked_obj.is_ha.return_value = True
        mocked_obj.shell.side_effect = [
            Response("vty response")
        ]
        response = SrxSystem.vty(mocked_obj, command="show memory", destination="cp", node=1, force_on_primary_node=True).response()
        self.assertRegex(response, "vty response")

        # option invalid checking for command
        self.assertRaisesRegex(
            TobyException,
            r"Option 'command' must be STR, LIST or TUPLE",
            SrxSystem.vty,
            mocked_obj, command=None,
        )

        # invalid checking if su failed
        mocked_obj.su.return_value = False
        self.assertRaisesRegex(
            TobyException,
            r"cannot get root permission",
            SrxSystem.vty,
            mocked_obj, command="show memory",
        )

        mocked_obj.su.return_value = True

    def test_transit_node_alias(self):
        """Unit Test"""
        for alias in ("node0", 0, "0", "Node0", "NODE0"):
            self.assertEqual(SrxSystem._transit_node_alias(alias, mode="str"), "node0") # pylint: disable=protected-access

        for alias in ("node1", 1, "1", "Node1", "NODE1"):
            self.assertEqual(SrxSystem._transit_node_alias(alias, mode="int"), 1) # pylint: disable=protected-access

        self.assertRaisesRegex(
            TobyException,
            r"option 'node_alias' must be 0, '0', node0, 1, '1' or node1",
            SrxSystem._transit_node_alias,
            "unknown",
        ) # pylint: disable=protected-access

    def test_get_tnpdump_info(self):
        """Unit Test"""
        # mock object
        res_object = Mock()
        res_object.response = Mock()
        res_object.status = Mock()
        dev_object = Mock()
        dev_object.is_ha = Mock()
        dev_object.get_model = Mock()
        dev_object.runtime = {}
        dev_object.shell = Mock()
        dev_object._transit_node_alias = Mock()
        dev_object.shell.return_value = res_object

        dev_object.node0 = Mock()
        dev_object.node1 = Mock()

        # Get tnpdump info from Lowend SA platform
        dev_object.get_model.return_value = "srx345"
        dev_object.is_ha.return_value = False
        dev_object.get_platform_type.return_value = "octeon"
        res_object.response.return_value = self.response["SA_SEIGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertEqual(result["cp_addr"], "fwdd")
        self.assertTrue("fwdd" in result["spu_addr_list"])
        self.assertTrue("fwdd" in result["both_addr_list"])

        # Get tnpdump info from Lowend SA platform from previous
        dev_object.get_model.return_value = "srx345"
        dev_object.is_ha.return_value = False
        res_object.response.return_value = self.response["SA_SEIGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=False)
        self.assertEqual(result["cp_addr"], "fwdd")
        self.assertTrue("fwdd" in result["spu_addr_list"])
        self.assertTrue("fwdd" in result["both_addr_list"])

        # Get tnpdump info from Lowend HA platform
        dev_object.get_model.return_value = "srx345"
        dev_object.is_ha.return_value = True
        res_object.response.return_value = self.response["HA_SEIGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertTrue("node0" in result)
        self.assertTrue("node1" in result)
        self.assertEqual(result["node0"]["cp_addr"], "0x1100001")
        self.assertTrue("0x2100001" in result["node1"]["spu_addr_list"])
        self.assertTrue("0x2100001" in result["node1"]["both_addr_list"])

        # Get tnpdump info from Lowend HA platform with node
        dev_object.get_model.return_value = "srx345"
        dev_object._transit_node_alias.return_value = "node0"
        res_object.response.return_value = self.response["HA_SEIGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, node=0, force_get=True)
        self.assertEqual(result["cp_addr"], "0x1100001")
        self.assertTrue("0x1100001" in result["spu_addr_list"])
        self.assertTrue("0x1100001" in result["both_addr_list"])

        # Get tnpdump info from Lowend HA platform with node
        dev_object.get_model.return_value = "srx345"
        dev_object._transit_node_alias.return_value = "node1"
        res_object.response.return_value = self.response["HA_SEIGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, node=1, force_get=True)
        self.assertEqual(result["cp_addr"], "0x2100001")
        self.assertTrue("0x2100001" in result["spu_addr_list"])
        self.assertTrue("0x2100001" in result["both_addr_list"])

        # Get tnpdump info from Lowend HA with platform option
        res_object.response.return_value = self.response["HA_SEIGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, node=1, platform="octeon", force_get=True)
        self.assertEqual(result["cp_addr"], "0x2100001")
        self.assertTrue("0x2100001" in result["spu_addr_list"])
        self.assertTrue("0x2100001" in result["both_addr_list"])

        # Get tnpdump info from Lowend HA platform from previous
        res_object.response.return_value = self.response["HA_SEIGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, node=1, platform="octeon", force_get=False)
        self.assertEqual(result["cp_addr"], "0x2100001")
        self.assertTrue("0x2100001" in result["spu_addr_list"])
        self.assertTrue("0x2100001" in result["both_addr_list"])

        # Get tnpdump info from Highend SA platform
        dev_object.get_model.return_value = "srx5600"
        dev_object.is_ha.return_value = False
        dev_object.get_platform_type.return_value = "XLP"
        res_object.response.return_value = self.response["SA_SRX5600_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertEqual(result["cp_addr"], "fpc0.pic0")
        self.assertTrue("fpc0.pic2" in result["spu_addr_list"])
        self.assertTrue("fpc0.pic0" in result["both_addr_list"])
        self.assertTrue("fpc0.pic3" in result["both_addr_list"])

        # Get tnpdump info from Highend HA platform
        dev_object.get_model.return_value = "srx5600"
        dev_object.is_ha.return_value = True
        res_object.response.return_value = self.response["HA_SRX5600_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertEqual(result["node0"]["cp_addr"], "node0.fpc0.pic0")
        self.assertTrue("node0.fpc0.pic3" in result["node0"]["spu_addr_list"])
        self.assertTrue("node0.fpc0.pic0" in result["node0"]["both_addr_list"])
        self.assertTrue("node0.fpc0.pic3" in result["node0"]["both_addr_list"])

        # Get tnpdump info from FORGE HA platform"
        dev_object.get_model.return_value = "srx1500"
        dev_object.get_platform_type.return_value = "X86"
        res_object.response.return_value = self.response["HA_FORGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertEqual(result["node1"]["cp_addr"], "node1.fpc0")
        self.assertTrue("node0.fpc0" in result["node0"]["spu_addr_list"])
        self.assertTrue("node0.fpc0" in result["node0"]["both_addr_list"])

        # Get tnpdump info from FORGE SA platform
        dev_object.get_model.return_value = "srx1500"
        dev_object.is_ha.return_value = False
        res_object.response.return_value = self.response["SA_FORGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertEqual(result["cp_addr"], "fpc0")
        self.assertTrue("fpc0" in result["spu_addr_list"])
        self.assertTrue("fpc0" in result["both_addr_list"])

        # unknown platform treat as X86 platform
        dev_object.get_model.return_value = "summit"
        dev_object.get_platform_type.return_value = "X86"
        res_object.response.return_value = self.response["SA_FORGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertEqual(result["cp_addr"], "fpc0")
        self.assertTrue("fpc0" in result["spu_addr_list"])
        self.assertTrue("fpc0" in result["both_addr_list"])

        # Get tnpdump info from FORGE HA platform
        dev_object.get_model.return_value = "srx1500"
        dev_object.is_ha.return_value = True
        res_object.response.return_value = self.response["HA_FORGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True, platform="X86")
        self.assertTrue(result["node1"]["cp_addr"] == "node1.fpc0")
        self.assertTrue("node0.fpc0" in result["node0"]["spu_addr_list"])
        self.assertTrue("node0.fpc0" in result["node0"]["both_addr_list"])

        # Get tnpdump info from FORGE HA platform
        dev_object.get_model.return_value = "nfx150-c-s1"
        dev_object.is_ha.return_value = False
        res_object.response.return_value = self.response["SA_FORGE_TNPDUMP"]
        dev_object.get_platform_type.return_value = "nfx150"
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertEqual(result["cp_addr"], "fpc1")
        self.assertTrue("fpc1" in result["spu_addr_list"])
        self.assertTrue("fpc1" in result["both_addr_list"])

        # Get tnpdump info from PORTER SA platform
        dev_object.is_ha.return_value = False
        dev_object.get_model.return_value = "nfx250_s1"
        dev_object.get_platform_type.return_value = "x86"
        res_object.response.return_value = self.response["SA_SEIGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertEqual(result["cp_addr"], "fpc0")
        self.assertTrue("fpc0" in result["spu_addr_list"])
        self.assertTrue("fpc0" in result["both_addr_list"])

        # Get tnpdump info from PORTER HA platform
        dev_object.get_model.return_value = "nfx150_c_s1"
        dev_object.is_ha.return_value = True
        dev_object.get_platform_type.return_value = "nfx150"
        res_object.response.return_value = self.response["HA_SRX550_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertTrue(result["node1"]["cp_addr"] == "node1.fpc1")
        self.assertEqual(result["node0"]["spu_addr_list"], ["node0.fpc1", ])
        self.assertEqual(result["node0"]["both_addr_list"], ["node0.fpc1", ])

        # Get tnpdump info from another slot
        dev_object.get_model.return_value = "srx5400"
        dev_object.is_ha.return_value = False
        dev_object.get_platform_type.return_value = "xlp"
        res_object.response.return_value = self.response["SA_OTHER_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True)
        self.assertTrue(result["cp_addr"] == "fpc2.pic0")
        self.assertEqual(result["spu_addr_list"], ["fpc2.pic1", "fpc2.pic2", "fpc2.pic3", "fpc3.pic0", "fpc3.pic1", "fpc3.pic2", "fpc3.pic3"])
        self.assertEqual(
            result["both_addr_list"],
            ["fpc2.pic0", "fpc2.pic1", "fpc2.pic2", "fpc2.pic3", "fpc3.pic0", "fpc3.pic1", "fpc3.pic2", "fpc3.pic3"]
        )

        # set unsupport platform type
        dev_object.get_model.return_value = "srx1500"
        res_object.response.return_value = self.response["HA_FORGE_TNPDUMP"]
        result = SrxSystem.get_tnpdump_info(dev_object, force_get=True, platform="Unknown platform")
        self.assertFalse(result)

    def test_check_feature_support(self):
        """test feature support check"""
        # mock object
        res_object = Mock()
        res_object.response = Mock()
        res_object.status = Mock()
        dev_object = Mock()
        dev_object.current_node.current_controller.get_model = Mock()
        dev_object.cli.return_value = res_object
        dev_object.list_element_to_uppercase = lambda x: [s.upper() for s in x]
        dev_object.underscore_uppercase_transit = lambda x: re.sub(r"-", "_", str(x)).upper()


        # check one feature for SA topo
        dev_object.current_node.current_controller.get_model.return_value = "srx5400"
        result = SrxSystem.check_feature_support(dev_object, feature="he")
        self.assertTrue(result)

        self.assertFalse(SrxSystem.check_feature_support(dev_object, feature="LE"))

        # check several feature for SA topo don't have license
        dev_object.current_node.current_controller.get_model.return_value = "srx345"
        self.assertFalse(SrxSystem.check_feature_support(dev_object, feature=["he", ]))

        res_object.response.return_value = self.to_xml_object(self.response["SINGLE_REMAINING_TIME_LICENSE"])
        result = SrxSystem.check_feature_support(dev_object, feature=["LE", "LSYS"])
        self.assertFalse(SrxSystem.check_feature_support(dev_object, feature=["LE", "LSYS"]))

        # get platform info failed on HA
        dev_object.current_node.current_controller.get_model.return_value = False
        dev_object.get_version_info.return_value = {"node0": {"product_model": "srx345"}, "node1": {"product_model": "srx345"}}
        result = SrxSystem.check_feature_support(dev_object, feature=["he", ])
        self.assertFalse(result)

        # get platform info failed on SA
        dev_object.current_node.current_controller.get_model.return_value = ""
        dev_object.get_version_info.return_value = {"product_model": "srx4100", }
        result = SrxSystem.check_feature_support(dev_object, feature=["he", ])
        self.assertTrue(result)

        # not supported alias
        dev_object.current_node.current_controller.get_model.return_value = "srx345"
        result = SrxSystem.check_feature_support(dev_object, feature="Unknown_Alias")
        self.assertFalse(result)

        # multi spu platform
        dev_object.current_node.current_controller.get_model.return_value = "srx5600"
        self.assertTrue(SrxSystem.check_feature_support(dev_object, feature="multi_spu"))

        dev_object.current_node.current_controller.get_model.return_value = "srx1500"
        self.assertFalse(SrxSystem.check_feature_support(dev_object, feature="multi_spu"))

        # other feature supported alias
        res_object.response.side_effect = (
            self.to_xml_object(self.response["MULTI_LICENSE"]),
            self.to_xml_object(self.response["MULTI_LICENSE"]),
            self.to_xml_object(self.response["MULTI_LICENSE"]),
            self.to_xml_object(self.response["MULTI_LICENSE"]),
            self.to_xml_object(self.response["MULTI_LICENSE"]),
        )
        result = SrxSystem.check_feature_support(dev_object, feature=("VPN", "virtual_APPLIANCE", "idp_sig", "APPID_SIG"))
        self.assertTrue(result)

    @patch('jnpr.toby.hldcl.juniper.security.srxsystem.jxmlease.parse_etree')
    def test_get_version_info(self, xmlpatch):
        """Get image version, platform, hostname, etc... info from device"""
        dev_object = Mock()
        dev_object.current_node.current_controller.get_model = Mock()
        dev_object.runtime = {}

        # Get version from SA platform
        xmlpatch.return_value = self.to_xml_dict(self.response["SA_VERSION"])
        result = SrxSystem.get_version_info(dev_object, force_get=True)
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)

        # Get version from HA platform for all node info
        xmlpatch.return_value = self.to_xml_dict(self.response["HA_VERSION"])
        result = SrxSystem.get_version_info(dev_object, force_get=True)
        self.assertTrue("node0" in result)
        self.assertTrue("node1" in result)

        # Get version from HA platform's node0
        dev_object._transit_node_alias.return_value = "node0"
        result = SrxSystem.get_version_info(dev_object, force_get=True, node=0)
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)

        # Get version from HA platform's node1
        dev_object._transit_node_alias.return_value = "node1"
        result = SrxSystem.get_version_info(dev_object, force_get=True, node="node1")
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)

        # Get HA version from previous result
        result = SrxSystem.get_version_info(dev_object, force_get=False, node="node1")
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)

        # Get SA version from previous result
        dev_object.runtime = {"version_info": {"hostname": "vsrx01", "product_name": "vsrx"}}
        xmlpatch.return_value = self.to_xml_dict(self.response["SA_VERSION"])
        result = SrxSystem.get_version_info(dev_object, force_get=False)
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)
        dev_object.runtime = {}

        # Get HA version from previous result
        dev_object.runtime = {"version_info": {str(dev_object): {"hostname": "vsrx01", "product_name": "vsrx"}}}
        xmlpatch.return_value = self.to_xml_dict(self.response["SA_VERSION"])
        result = SrxSystem.get_version_info(dev_object, force_get=False)
        self.assertTrue("hostname" in result)
        self.assertTrue("product_name" in result)
        dev_object.runtime = {}

        # Get SA version if device return invalid
        xmlpatch.return_value = self.to_xml_dict(self.response["INVALID_SA_VERSION"])
        result = SrxSystem.get_version_info(dev_object, force_get=True)
        self.assertTrue(result["hostname"] is None)
        self.assertTrue(result["product_model"] is None)

        # Get HA version if device return invalid
        xmlpatch.return_value = self.to_xml_dict(self.response["INVALID_HA_VERSION"])
        result = SrxSystem.get_version_info(dev_object, force_get=True)
        self.assertTrue(result["node0"]["hostname"] is None)
        self.assertTrue(result["node0"]["product_model"] is None)

        # Get TVP base version on HA but only have one node
        xmlpatch.return_value = self.to_xml_dict(self.response["HA_TVP_BASE_VERSION"])
        result = SrxSystem.get_version_info(dev_object, force_get=True)
        self.assertEqual(result["node0"]["hostname"], "vsrx-esx-cn46")
        self.assertEqual(result["node0"]["product_model"], "vsrx")

    @patch('jnpr.toby.hldcl.juniper.security.srxsystem.run_multiple')
    def test_reboot(self, mock_run_multiple):
        """Unit Test"""
        # mock object
        res_object = Mock()
        res_object.response = Mock()
        res_object.status = Mock()
        dev_object = Mock()
        dev_object.is_ha = Mock()
        dev_object.get_model = Mock()
        dev_object.runtime = {}
        dev_object.shell = Mock()
        dev_object._transit_node_alias = Mock()
        dev_object.shell.return_value = res_object

        dev_object.node0 = Mock()
        dev_object.node1 = Mock()
        dev_object.current_node.current_controller = Mock()

        # For SA device
        dev_object.is_ha.return_value = False
        result = SrxSystem.reboot(
            dev_object,
            wait="60",
            mode="shell",
            timeout=480,
            interval=20,
            device_type=None,
            system_nodes="all",
            on_parallel=None,
        )
        self.assertTrue(result)

        # For HA device
        dev_object.is_ha.return_value = True
        result = SrxSystem.reboot(
            dev_object,
            wait="60",
            mode="shell",
            timeout=480,
            interval=20,
            device_type=None,
            system_nodes="all",
            on_parallel=False,
        )
        self.assertTrue(result)

        result = SrxSystem.reboot(
            dev_object,
            wait="60",
            mode="shell",
            timeout=480,
            interval=20,
            device_type=None,
            system_nodes="node0",
            on_parallel=False,
        )
        self.assertTrue(result)

        mock_run_multiple.return_value = [True, True]
        result = SrxSystem.reboot(
            dev_object,
            system_nodes=1,
            on_parallel=False,
        )
        self.assertTrue(result)

        self.assertRaisesRegex(
            ValueError,
            r"option 'system_nodes' must one of 'None', 'all-members', 'all', 'node0'",
            SrxSystem.reboot,
            dev_object, system_nodes="unknown",
        )

        mock_run_multiple.return_value = True
        result = SrxSystem.reboot(
            dev_object,
            all="True",
            system_nodes="node0",
        )
        self.assertTrue(result)

        dev_object.is_ha.return_value = True
        mock_run_multiple.return_value = [True, True]
        result = SrxSystem.reboot(
            dev_object,
            all=True,
        )
        self.assertTrue(result)


def create_init_data():
    """
    Function to create init_data
    :return:
        Returns init_data
    """
    init_data = dict()
    init_data['t'] = dict()
    init_data['t']['resources'] = dict()
    init_data['t']['resources']['r0'] = dict()
    init_data['t']['resources']['r0']['system'] = dict()
    init_data['t']['resources']['r0']['system']['primary'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'abc'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['osname'] = 'junos'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['host'] = 'host1'
    init_data['t']['resources']['r0']['system']['primary']['controllers']['re0']['model'] = 'mx'
    return init_data


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestSrxSystem)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
