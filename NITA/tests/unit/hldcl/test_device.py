"""
Device.py Unit Test
"""

import lxml
import unittest
from mock import patch, MagicMock, Mock

import builtins

from jnpr.toby.hldcl.device import Device, connect_to_device, execute_cli_command_on_device, \
    execute_config_command_on_device, execute_shell_command_on_device, reboot_device, close_device_handle, \
    software_install, issu_upgrade, reconnect_to_device, disconnect_from_device, save_device_configuration, \
    load_device_configuration, switch_to_superuser, execute_vty_command_on_device, execute_cty_command_on_device, \
    switch_re_master, execute_rpc_command_on_device, commit_configuration, set_current_system_node, \
    get_current_controller_name, set_current_controller, execute_grpc_api, switchover_device, clean_config_on_device,\
    upgrade_device

from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.utils.flow_common_tool import flow_common_tool

builtins.t = MagicMock()


class TestDevice(unittest.TestCase):
    """
    TestDevice class to handle Device.py unit tests
    """

    def setUp(self):
        """setup before all cases"""
        self.tool = flow_common_tool()
        self.to_xml_object = lambda x: lxml.etree.fromstring(x)

        self.response = {}

        self.response["FULL_TEXT_XML"] = """
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

        self.response["SA_NO_RPC_VERSION"] = """
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

    def __check_assertion__(self, mode=None, system_data=None):
        """
        Function to check exceptions raised
        :param mode:
            Mode can be hostname, system or None
        :param system_data:
            system_data required for system mode
        :return:
            Returns true or false depending on test results
        """
        if mode is None:
            if system_data is None:
                self.assertRaises(Exception, Device)
                self.assertRaises(Exception, Device, user='user', password='password')
            else:
                del system_data['system']['primary']['osname']
                self.assertRaises(Exception, Device, system=system_data['system'], os=None)
                system_data['system']['primary']['osname'] = 'JUNOS'
        elif mode == 'hostname':
            self.assertRaises(Exception, Device, user='user', password='password', host='hostname', os=None)
            self.assertRaises(Exception, Device, user='user', password='password', host='hostname', os='OSX')
        elif mode == 'system':
            system_data['system']['primary']['osname'] = 'OSX'
            self.assertRaises(Exception, Device, system=system_data['system'])
            system_data['system']['primary']['osname'] = 'JUNOS'
            system_data['system']['primary']['controllers']['re0']['connect_mode'] = 'connect'
            system_data['system']['primary']['controllers']['re0']['connect_mode'] = None
            system_data['system']['primary']['controllers']['re0']['connect_mode'] = 'ssh'
            system_data['system']['primary']['controllers']['re0']['timeout'] = None
            system_data['system']['primary']['controllers']['re0']['timeout'] = 100
            system_data['system']['primary']['controllers']['re0']['user'] = None
            system_data['system']['primary']['controllers']['re0']['user'] = 'user'
            system_data['system']['primary']['controllers']['re0']['password'] = None
            system_data['system']['primary']['controllers']['re0']['password'] = 'password'


    # @patch('jnpr.toby.hldcl.device.OS')
    # @patch('jnpr.toby.hldcl.cisco.cisco.Cisco')
    @patch('jnpr.toby.hldcl.device.DeviceData')
    @patch('jnpr.toby.hldcl.juniper.junipersystem.JuniperSystem')
    @patch('jnpr.toby.hldcl.juniper.security.srxsystem.SrxSystem')
    @patch('jnpr.toby.hldcl.system.System')
    @patch('jnpr.toby.hldcl.trafficgen.spirent.spirent.Spirent')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixia.Ixia')
    def test_device_new(self, ixia_mock, spirent_mock, system_mock, srxsystem_mock, junipersystem_mock, devicedata_mock):
        """
        Tests Device.__new__ method
        :param spirent_mock:
            Mocked object for SpirentSystem class
        :param system_mock:
            Mocked object for System class
        :param srxsystem_mock:
            Mocked object for SrxSystem class
        :param junipersystem_mock:
            Mocked object for JuniperSystem class
        :param devicedata_mock:
            Mocked object for DeviceData class
        :param os_mock:
            Mocked object for device.OS class
        :param cisco_mock:
            Mocked object for Cisco class
        :return:
            Returns true or false depending on test results
        """

        system_data = dict()
        system_data['system'] = dict()
        system_data['system']['primary'] = dict()
        self.assertRaises(Exception, Device, system=system_data['system'])

        system_data = create_system_data()
        self.__check_assertion__()
        self.__check_assertion__(None, system_data)

        junipersystem_mock.return_value = 'juniper_system'
        devicedata_mock.return_value.system_facts.return_value = system_data['system']
        devicedata_mock.return_value.get_model.return_value = 'model'

#        Python Mode
#         os_mock.getenv.return_value = False
        dobject = Device(user='user', password='password', host='hostname')
        self.assertEqual(dobject, 'juniper_system')

        self.__check_assertion__('hostname')
        self.__check_assertion__('system', system_data)

        dobject = Device(user='user', password='password', host='hostname', connect_dual_re=True)
        self.assertTrue(devicedata_mock.return_value.get_model.called)
        self.assertEqual(dobject, 'juniper_system')

        dobject = Device(user='user', password='password', host='hostname', timeout=100)
        self.assertEqual(dobject, 'juniper_system')
        self.assertEqual(system_data['system']['primary']['controllers']['re0']['timeout'], 100)

        dobject = Device(user='user', password='password', host='hostname', connect_dual_re=True, connect_complex_system=True)
        self.assertTrue(devicedata_mock.return_value.system_facts.called)
        self.assertEqual(dobject, 'juniper_system')

        dobject = Device(user='user', password='password', system=system_data['system'])
        self.assertEqual(dobject, 'juniper_system')

        system_data['system']['primary']['name'] = 'hostname'
        system_data['system']['primary']['mgt-ip'] = 'hostname'
        dobject = Device(host='hostname1', system=system_data['system'], connect_complex_system=False)
        self.assertEqual(dobject, 'juniper_system')

        dobject = Device(system=system_data['system'], connect_complex_system=False)
        self.assertEqual(dobject, 'juniper_system')

        del system_data['system']['primary']['controllers']['re0']['user']
        del system_data['system']['primary']['controllers']['re0']['password']
        del system_data['system']['primary']['controllers']['re0']['connect_mode']
        del system_data['system']['primary']['controllers']['re0']['timeout']
        dobject = Device(user='user', password='password', system=system_data['system'])
        self.assertEqual(dobject, 'juniper_system')

        del system_data['system']['primary']['controllers']['re0']['mgt-ip']
        system_data['system']['primary']['controllers']['re0']['hostname'] = 'hostname'
        dobject = Device(user='user', password='password', system=system_data['system'])
        self.assertEqual(dobject, 'juniper_system')

        system_data['system']['primary']['controllers']['re0']['domain'] = 'domain.net'
        dobject = Device(user='user', password='password', system=system_data['system'])
        self.assertEqual(dobject, 'juniper_system')

        system_data['system']['primary']['controllers']['re0']['domain'] = 'domain.net'
        dobject = Device(user='user', password='password', port='port', system=system_data['system'])
        self.assertEqual(dobject, 'juniper_system')

        system_data = create_system_data('secondary', 're1', system_data)
        dobject = Device(user='user', password='password', system=system_data['system'], connect_complex_system=False)
        self.assertEqual(dobject, 'juniper_system')

        system_data = create_system_data('primary', 're1')
        dobject = Device(user='user', password='password', system=system_data['system'], connect_dual_re=False)
        self.assertEqual(dobject, 'juniper_system')

        system_data['system']['primary']['osname'] = None
        self.assertRaises(Exception, Device, user='user', password='password', system=system_data['system'])

        system_data['system']['primary']['osname'] = 'JUNOS'
        srxsystem_mock.return_value = 'srx_system'
        dobject = Device(user='user', password='password', host='hostname', model='srx')
        self.assertEqual(dobject, 'srx_system')

        ## Added code to test device object creation by passing  pyez_port and text_port arguments
        system_data['system']['primary']['osname'] = 'JUNOS'
        srxsystem_mock.return_value = 'srx_system'
        dobject = Device(user='user', password='password', host='hostname', model='srx', pyez_port=22, text_port=22)
        self.assertEqual(dobject, 'srx_system')

        system_mock.return_value = 'unix_system'
        dobject = Device(user='user', password='password', host='hostname', os='unix')
        self.assertEqual(dobject, 'unix_system')

        system_mock.return_value = 'windows_system'
        dobject = Device(user='user', password='password', host='hostname', os='windows')
        self.assertEqual(dobject, 'windows_system')

        #dobject = Device(user='user', password='password', host='hostname', os='ios')

        spirent_mock.return_value = 'spirent_system'
        dobject = Device(user='user', password='password', host='hostname', os='spirent')
        self.assertEqual(dobject, 'spirent_system')

        ixia_mock.return_value = 'ixia_system'
        dobject = Device(user='user', password='password', host='hostname', os='ixia')
        self.assertEqual(dobject, 'ixia_system')

        # If global variable 't' do not exists
        del builtins.t
        self.assertRaisesRegex(
            NameError,
            r"name 't' is not defined",
            Device,
            user='user', password='password', host='hostname',
        )

        builtins.t = MagicMock()

        # connect target is "console"
        ixia_mock.return_value = 'ixia_system'
        dobject = Device(user='user', password='password', host='hostname', connect_targets='console', os='ixia')
        self.assertEqual(dobject, 'ixia_system')

        # proxy host configured
        self.assertRaisesRegex(
            TobyException,
            r"'model' parameter is missing",
            Device,
            user='user', password='password', host='hostname', proxy_host="127.0.0.1",
            proxy_user='regress', proxy_password='abcd1234', proxy_port=4433, os='ixia',
        )

        # mode option check for junos
        system_data['system']['primary']['osname'] = 'JUNOS'
        srxsystem_mock.return_value = 'srx_system'
        self.assertRaisesRegex(
            TobyException,
            r"'model' parameter is missing",
            Device,
            user='user', password='password', host='hostname', connect_targets="console", os='junos',
        )

        # no os_name checking
        system_data['system']['primary']['osname'] = None
        srxsystem_mock.return_value = 'srx_system'
        self.assertRaisesRegex(
            TobyException,
            r"No OS specified",
            Device,
            user='user', password='password', host='hostname', os='',
        )

        # MX instance creation
        # system_data['system']['primary']['model'] = 'VMX'
        # srxsystem_mock.return_value = 'mx_system'
        # junipersystem_mock.return_value = 'juniper_system'
        # dobject = Device(user='user', password='password', host='hostname', os='junos', model="VMX")
        # self.assertEqual(dobject, "juniper_system")

        # # IOS device
        # dobject = Device(user='user', password='password', host='hostname', os='ios')
        # self.assertIsInstance(dobject, MagicMock)
        #
        # # BROCADE device
        # dobject = Device(user='user', password='password', host='hostname', os='brocade')
        # self.assertIsInstance(dobject, MagicMock)
        #
        # # SRC device
        # dobject = Device(user='user', password='password', host='hostname', os='src')
        # self.assertIsInstance(dobject, MagicMock)

        # # PARAGON device
        # dobject = Device(user='user', password='password', host='hostname', os='paragon')
        # self.assertIsInstance(dobject, MagicMock)
        #
        # # BPS device
        # dobject = Device(user='user', password='password', host='hostname', os='bps')
        # self.assertIsInstance(dobject, MagicMock)
        #
        # dobject = Device(user='user', password='password', host='hostname', os='breakingpoint')
        # self.assertIsInstance(dobject, MagicMock)

        # # ELEVATE device
        # dobject = Device(user='user', password='password', host='hostname', os='elevate')
        # self.assertIsInstance(dobject, MagicMock)

    @patch('jnpr.toby.hldcl.device.Device')
    def test_device_connect_to_device(self, device_mock):
        """
        Tests connect_to_device function
        :param device_mock:
            Mocked object for Device
        :return:
            Raises exception or true or false depending on tests
        """
        device_mock.return_value = True
        self.assertTrue(connect_to_device())

    def test_device_execute_cli_command_on_device(self):
        """
        Tests execute_cli_command_on_device function
        :return:
            Raises exception or true or false depending on tests
        """
        # robject = MagicMock()
        # robject.response = MagicMock(return_value='test_str')
        # dobject = MagicMock()
        # dobject.cli = MagicMock(return_value=robject)
        # self.assertEqual(execute_cli_command_on_device(dobject), 'test_str')

        response_obj = Mock()
        response_obj.response = Mock()
        device_obj = Mock()
        device_obj.cli = Mock()

        device_obj.cli.return_value = response_obj

        # basic check
        response_obj.response.return_value = self.response["FULL_TEXT_XML"]
        response = execute_cli_command_on_device(device=device_obj, command="show version")
        self.assertRegex(response, r"multi-routing-engine-results")

        # check command LIST
        response_obj.response.side_effect = (self.response["FULL_TEXT_XML"], self.response["SA_NO_COREDUMP"])
        response = execute_cli_command_on_device(device=device_obj, command=["show version", "show system coredump"])
        self.assertRegex(response, r"/var/crash/corefiles")

        # check command TUPLE
        response_obj.response.side_effect = (self.response["FULL_TEXT_XML"], self.response["SA_NO_COREDUMP"])
        response = execute_cli_command_on_device(device=device_obj, command=("show version", "show system coredump"))
        self.assertRegex(response, r"/var/crash/corefiles")

        # check timeout value support STR
        response_obj.response.side_effect = (self.response["FULL_TEXT_XML"], "")
        response = execute_cli_command_on_device(device=device_obj, command="show version", timeout="30")
        self.assertRegex(response, r"multi-routing-engine-results")

        # check transit XML to dict if needed
        response_obj.response.side_effect = (self.response["FULL_TEXT_XML"], "")
        response = execute_cli_command_on_device(device=device_obj, command="show version", xml_to_dict=True)
        self.assertEqual(response["rpc-reply"]["multi-routing-engine-results"]["multi-routing-engine-item"][0]["re-name"], "node0")

        # check transit XML to dict but device response is plain text
        response_obj.response.side_effect = (self.response["SA_NO_COREDUMP"], "")
        response = execute_cli_command_on_device(device=device_obj, command="show version", xml_to_dict=True)
        self.assertRegex(response, r"/var/crash/corefiles")

        # check transit XML to dict but device response is plain text
        response_obj.response.side_effect = (self.response["SA_NO_COREDUMP"], "")
        response = execute_cli_command_on_device(device=device_obj, command="show version", xml_to_dict=True)
        self.assertRegex(response, r"/var/crash/corefiles")

        # check strip xml illegal output
        response_obj.response.side_effect = (self.response["SA_HE_FLOW_SESSION_HAVE_UNEXPECT_OUTPUT"], "")
        response = execute_cli_command_on_device(device=device_obj, command="show version", xml_to_dict=True)
        self.assertEqual(response["rpc-reply"]["multi-routing-engine-results"]["multi-routing-engine-item"]\
        ["flow-session-information"][0]["displayed-session-count"], "0")

        # check do not strip xml illegal output
        response_obj.response.side_effect = (self.response["SA_HE_FLOW_SESSION_HAVE_UNEXPECT_OUTPUT"], "")
        response = execute_cli_command_on_device(device=device_obj, command="show version", strip_xml_output=False, print_response=True)
        self.assertRegex(response, r"Message from syslogd")

        # check device response is xml object
        response_obj.response.side_effect = (self.to_xml_object(self.response["FULL_TEXT_XML"]), "")
        response = execute_cli_command_on_device(
            device=device_obj, command="show version", channel="pyez",
            format="xml", xml_to_dict=True, print_response=True
        )
        self.assertEqual(response["rpc-reply"]["multi-routing-engine-results"]["multi-routing-engine-item"][0]["re-name"], "node0")

        # do not checking, only for print xml object
        response_obj.response.side_effect = (self.to_xml_object(self.response["FULL_TEXT_XML"]), "")
        response = execute_cli_command_on_device(
            device=device_obj, command="show version", channel="pyez",
            format="xml", xml_to_dict=False, print_response=True
        )

        # device response is empty
        response_obj.response.side_effect = ("", "")
        response = execute_cli_command_on_device(device=device_obj, command="show version", channel="pyez", format="xml", xml_to_dict=False)
        self.assertEqual(response, "")

        # check no "command" value
        self.assertRaisesRegex(
            TobyException,
            r"Mandatory argument 'command' is missing",
            execute_cli_command_on_device,
            device=device_obj,
        )

        # check invalid "command" value
        self.assertRaisesRegex(
            TobyException,
            r"must be a STR, LIST or TUPLE",
            execute_cli_command_on_device,
            device=device_obj, command=object,
        )

    def test_device_execute_config_command(self):
    # def test_device_execute_config_command(self, mock_config, mock_commit, mock_reboot, mock_is_ha):
        """
        Tests execute_config_command_on_device function
        :return:
            Raises exception or true or false depending on tests
        """
        response_obj = Mock()
        response_obj.response = Mock()
        response_obj.status = Mock()
        device_obj = Mock()
        device_obj.config = Mock()
        device_obj.is_ha = Mock()
        device_obj.commit = Mock()
        device_obj.name = Mock(return_value="test_dev")

        device_obj.config.return_value = response_obj
        device_obj.commit.return_value = response_obj

        # do single cmd configurtion and commit, then get response
        cmds = "set security policies default-policy permit-all"

        response_obj.response.side_effect = ["commit complete", True]
        response_obj.status.return_value = True
        response = execute_config_command_on_device(device=device_obj, command=cmds, commit=True, get_response=True, timeout=30)
        self.assertRegex(response, r"commit complete")

        # single cmd in tuple but not commit, then get response
        cmds = (
            "set security policies default-policy permit-all",
        )
        response_obj.response.side_effect = ["error: config failed", ]
        response = execute_config_command_on_device(device=device_obj, command=cmds, commit=False, get_response=True, print_response=True)
        self.assertRegex(response, r"error")

        # multiple cmd and commit, but not get response
        cmds = (
            "cmd 1: set security policies default-policy permit-all",
            "cmd 2: set security policies default-policy permit-all",
        )
        response_obj.status.side_effect = [False, ]
        response = execute_config_command_on_device(device=device_obj, command=cmds, commit=True, get_response=False)
        self.assertFalse(response)

        # reboot automatically
        response_obj.response.side_effect = ["must reboot the system", ]
        device_obj.is_ha.return_value = False

        from jnpr.toby.hldcl import device
        device.reboot_device = Mock()
        device.reboot_device.return_value = True
        response = execute_config_command_on_device(device=device_obj, command=cmds, commit=True, get_response=False, reboot_if_need=True)
        self.assertRegex(response, "reboot the system")

        # customized reboot keyword
        response_obj.response.side_effect = ["don't know why, but need reboot", ]
        device_obj.is_ha.return_value = True
        response = execute_config_command_on_device(device=device_obj, command=cmds, reboot_keyword="need reboot", reboot_if_need=True)
        self.assertRegex(response, "don't know why")

        # reboot device failed
        response_obj.response.side_effect = ["device need to reboot", ]
        device_obj.is_ha.return_value = False
        device.reboot_device.return_value = False
        response = execute_config_command_on_device(device=device_obj, command=cmds, reboot_if_need=True)
        self.assertFalse(response)

        # no command given
        self.assertRaisesRegex(
            TobyException,
            r"Mandatory argument 'command' or 'command_list' is missing",
            execute_config_command_on_device,
            device=device_obj,
        )

        # invalid command or command_list
        self.assertRaisesRegex(
            TobyException,
            r"option must be a STR, LIST or TUPLE",
            execute_config_command_on_device,
            device=device_obj, command=None,
        )

        self.assertRaisesRegex(
            TobyException,
            r"option must be a STR, LIST or TUPLE",
            execute_config_command_on_device,
            device=device_obj, command_list=object,
        )

    def test_device_execute_shell_command(self):
        """
        Tests execute_shell_command_on_device function
        :return:
            Raises exception or true or false depending on tests
        """
        response_obj = Mock()
        response_obj.response = Mock()
        response_obj.status = Mock()
        device_obj = Mock()
        device_obj.shell = Mock()
        device_obj.shell.return_value = response_obj

        # single cmd
        response_obj.response.return_value = "device response"
        self.assertEqual(execute_shell_command_on_device(device=device_obj, command="ls -l"), 'device response')

        # multiple cmds with str timeout
        response_obj.response.side_effect = ["device response", "device response"]
        response = execute_shell_command_on_device(device=device_obj, command=["ls -l", "du -h"], timeout="30", print_response=True)
        self.assertRegex(response, 'device response')

        # invalid cmd type
        self.assertRaisesRegex(
            TobyException,
            r"must be a STR, LIST or TUPLE",
            execute_shell_command_on_device,
            device=device_obj, command=None,
        )

    def test_device_reboot_device(self):
        """
        Tests reboot_device function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.reboot = MagicMock(return_value='test_str')
        self.assertEqual(reboot_device(dobject), 'test_str')

    def test_device_close_device_handle(self):
        """
        Tests close_device_handle function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.close = MagicMock(return_value='test_str')
        self.assertEqual(close_device_handle(dobject), 'test_str')


    def test_device_software_install(self):
        """
        Tests software_install function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.software_install = MagicMock(return_value='test_str')
        self.assertEqual(software_install(dobject), 'test_str')


    def test_device_issu_upgrade(self):
        """
        Tests issu_upgrade function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.software_install = MagicMock(return_value='test_str')
        self.assertEqual(issu_upgrade(dobject), 'test_str')


    def test_device_reconnect_to_device(self):
        """
        Tests reconnect_to_device function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.reconnect = MagicMock(return_value='test_str')
        self.assertEqual(reconnect_to_device(dobject), 'test_str')


    def test_device_disconnect_from_device(self):
        """
        Tests disconnect_from_device function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.disconnect = MagicMock(return_value='test_str')
        self.assertEqual(disconnect_from_device(dobject), 'test_str')


    def test_device_save_device_configuration(self):
        """
        Tests save_device_configuration function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.save_config = MagicMock(return_value='test_str')
        self.assertEqual(save_device_configuration(dobject), 'test_str')


    def test_device_load_device_configuration(self):
        """
        Tests load_device_configuration function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.load_config = MagicMock(return_value='test_str')
        self.assertEqual(load_device_configuration(dobject), 'test_str')


    def test_device_switch_to_superuser(self):
        """
        Tests switch_to_superuser function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.su = MagicMock(return_value='test_str')
        self.assertEqual(switch_to_superuser(dobject), 'test_str')


    def test_device_execute_vty_command_on_device(self):
        """
        Tests execute_vty_command_on_device function
        :return:
            Raises exception or true or false depending on tests
        """
        robject = MagicMock()
        robject.response = MagicMock(return_value='test_str')
        dobject = MagicMock()
        dobject.vty = MagicMock(return_value=robject)
        self.assertEqual(execute_vty_command_on_device(dobject, 'dummy cmd', 'fpc0'), 'test_str')


    def test_device_execute_cty_command_on_device(self):
        """
        Tests execute_cty_command_on_device function
        :return:
            Raises exception or true or false depending on tests
        """
        robject = MagicMock()
        robject.response = MagicMock(return_value='test_str')
        dobject = MagicMock()
        dobject.cty = MagicMock(return_value=robject)
        self.assertEqual(execute_cty_command_on_device(dobject, command="", destination=""), 'test_str')


    def test_device_switch_re_master(self):
        """
        Tests switch_re_master function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.switch_re_master = MagicMock(return_value='test_str')
        self.assertEqual(switch_re_master(dobject), 'test_str')

    def test_device_switchover_device(self):
        """Test device switchover device"""
        dobject = MagicMock()
        dobject.switchover.return_value = 'test_str'
        self.assertEqual(switchover_device(dobject), 'test_str')

    def test_device_upgrade_device(self):
        """Test device upgrade device"""
        dobject = MagicMock()
        dobject.upgrade.return_value = 'test_str'
        self.assertEqual(upgrade_device(dobject), 'test_str')
    def test_device_clean_config_on_device(self):
        """Test device clean config on device"""
        dobject = MagicMock()
        dobject.clean_config.return_value = 'test_str'
        self.assertEqual(clean_config_on_device(dobject), 'test_str')

    def test_device_execute_rpc_command_on_device(self):
        """
        Tests execute_rpc_command_on_device function
        :return:
            Raises exception or true or false depending on tests
        """
        robject = MagicMock()
        robject.response = MagicMock(return_value='test_str')
        dobject = MagicMock()
        dobject.execute_rpc = MagicMock(return_value=robject)
        self.assertEqual(execute_rpc_command_on_device(dobject), 'test_str')


    def test_device_commit_configuration(self):
        """
        Tests commit_configuration function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.commit = MagicMock(return_value='test_str')
        self.assertEqual(commit_configuration(dobject), 'test_str')

    @staticmethod
    def test_execute_grpc_api():
        """Test execute grpc api"""
        from jnpr.toby.hldcl import device
        dev = MagicMock()
        dev.current_node.current_controller.default_grpc_channel = 1
        dev.current_node.current_controller.channels = {'grpc':[MagicMock(), MagicMock()]}
        dev.current_node.current_controller.channels['grpc'][1].send_api.return_value = "test"
        kwargs = {}
        try:
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name=None, api_call=None, api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass

        try:
            device.execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="test", api_call=None, api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass

        kwargs = {'api_args': 'test'}
        try:
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="test", api_call=None, api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass

        kwargs = {'api_args': 'test', 'modules_to_source': 'test_modules'}
        try:
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="test", api_call=None, api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass

        kwargs = {'api_args': 'test', 'modules_to_source': 'test_modules', 'service': 'test_service'}
        try:
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="test", api_call=None, api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass


class TestDevice2(unittest.TestCase):
    """
    TestDevice class to handle Device.py unit tests
    """

    def test_device_get_current_controller_name(self):
        """
        Tests get_current_controller_name function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.get_current_controller_name = MagicMock(return_value='test_str')
        self.assertEqual(get_current_controller_name(dobject), 'test_str')

    def test_device_set_current_controller(self):
        """
        Tests set_current_controller function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.set_current_controller = MagicMock(return_value='test_str')
        self.assertEqual(set_current_controller(dobject, 're0'), 'test_str')

    def test_device_set_current_system_node(self):
        """
        Tests set_current_system_node function
        :return:
            Raises exception or true or false depending on tests
        """
        dobject = MagicMock()
        dobject.set_current_system_node = MagicMock(return_value='test_str')
        self.assertEqual(set_current_system_node(dobject, 'primary'), 'test_str')

    @staticmethod
    @patch('jnpr.toby.hldcl.device.importlib')
    def test_execute_grpc_api(importlib_patch):
        """Test execute grpc api"""
        from jnpr.toby.hldcl import device
        dev = MagicMock()
        dev.current_node.current_controller.default_grpc_channel = 1
        dev.current_node.current_controller.channels = {'grpc':[MagicMock(), MagicMock()]}
        dev.current_node.current_controller.channels['grpc'][1].send_api.return_value = "test"
        kwargs = {}
        try:
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name=None, api_call=None, api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass

        try:
            device.execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="test", api_call=None, api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass

        kwargs = {'api_args': 'test'}
        try:
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="test", api_call=None, api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass

        kwargs = {'api_args': 'test', 'modules_to_source': [MagicMock()]}
        try:
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="test", api_call=None, api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass

        kwargs = {'api_args': "{'k':'v'}", 'modules_to_source': ['system'], 'service': 'test_service'}
        execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="upload_file", api_call=None, api_call_yaml_file=None, **kwargs)

        kwargs = {'api_args': "{'k':'v'}", 'modules_to_source': ['system']}
        try:
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name=None, api_call="test", api_call_yaml_file=None, **kwargs)
        except BaseException:
            kwargs = {
                'api_args': "{'k':'v'}",
                'modules_to_source': ['system'],
                'tcase_id': 'testcase_id',
                'id': '',
                'service': 'test',
                'library': 'test'
            }
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name=None, api_call="test", api_call_yaml_file="test_yaml", **kwargs)

        try:
            kwargs = {'api_args': "{'k':'v'}", 'modules_to_source': ['system'], 'service': 'service_value'}
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="upload_file", api_call="test", api_call_yaml_file=None, **kwargs)
        except BaseException:
            pass

        try:
            kwargs = {'api_args': "{'k':'v'}", 'modules_to_source': ['system'], 'service': 'service_value', 'library': 'test'}
            execute_grpc_api(dev, timeout=300, channel_ID=None, api_name="upload_file", api_call="test", api_call_yaml_file="test_yaml", **kwargs)
        except BaseException:
            pass

    def test_detect_core(self):
        """Test detect core"""
        from jnpr.toby.hldcl import device
        dev = MagicMock()
        dev.detect_core.return_value = True
        self.assertTrue(device.detect_core(dev, core_path="test", resource="test_resource"))
        self.assertTrue(device.detect_core(dev, resource="test_resource"))

    def test_get_version_for_device(self):
        """Test get version for device"""
        from jnpr.toby.hldcl import device
        dev = MagicMock()
        dev.get_version.return_value = "version"
        self.assertEqual("version", device.get_version_for_device(dev))

    def test_get_model_for_device(self):
        """Test get model for device"""
        from jnpr.toby.hldcl import device
        dev = MagicMock()
        dev.get_model.return_value = "model"
        self.assertEqual("model", device.get_model_for_device(dev))

    def test_get_vmhost_infra_for_device(self):
        """Test get vmhost for device"""
        from jnpr.toby.hldcl import device
        dev = MagicMock()
        dev.get_vmhost_infra.return_value = True
        self.assertEqual(True, device.get_vmhost_infra_for_device(dev))

    def test_execute_pyez_command_on_device(self):
        """Test execute pyez command on device"""
        from jnpr.toby.hldcl import device
        from jnpr.toby.utils.response import Response
        dev = MagicMock()
        dev.pyez.return_value = Response(response="show version response")
        self.assertEqual("show version response", device.execute_pyez_command_on_device(dev, command="show version"))

    def test_add_channel_to_device(self):
        """Test add channel to device"""
        from jnpr.toby.hldcl import device
        dev = MagicMock()
        dev.add_channel.return_value = "channel"
        self.assertEqual("channel", device.add_channel_to_device(dev, channel_type="type"))


    def test_get_platform_type(self):
        """Test get platform type"""
        from jnpr.toby.hldcl import device
        dev = MagicMock()
        dev.get_platform_type.return_value = "xlp"
        self.assertEqual("xlp", device.get_platform_type(dev))


def create_system_data(mode='primary', routing_engine='re0', system_data=None):
    """
    Function to create system_data
    :param mode:
        Mode can be primary or secondary
    :param routing_engine:
        routing_engine can be re0 or re1
    :param system_data:
        Pass existing system_data to append
    :return:
        Returns system_data
    """
    if system_data is None:
        system_data = dict()
        system_data['system'] = dict()
    system_data['system'][mode] = dict()
    system_data['system'][mode]['name'] = 'hostname'
    system_data['system'][mode]['model'] = 'model'
    system_data['system'][mode]['osname'] = 'JUNOS'
    system_data['system'][mode]['controllers'] = dict()
    system_data['system'][mode]['controllers'][routing_engine] = dict()
    system_data['system'][mode]['controllers'][routing_engine]['name'] = 'hostname'
    system_data['system'][mode]['controllers'][routing_engine]['mgt-ip'] = 'hostname'
    system_data['system'][mode]['controllers'][routing_engine]['model'] = 'model'
    system_data['system'][mode]['controllers'][routing_engine]['osname'] = 'JUNOS'
    system_data['system'][mode]['controllers'][routing_engine]['connect_mode'] = 'ssh'
    system_data['system'][mode]['controllers'][routing_engine]['user'] = 'user'
    system_data['system'][mode]['controllers'][routing_engine]['password'] = 'password'
    return system_data

if __name__ == '__main__':  # pragma: no coverage
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDevice)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)
    unittest.main()
