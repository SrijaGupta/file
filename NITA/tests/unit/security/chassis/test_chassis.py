# coding: UTF-8
"""All unit test cases for CHASSIS module"""
# pylint: disable=attribute-defined-outside-init,invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import time

from unittest import TestCase, mock

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.message import message
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.security.chassis.chassis import chassis


class TestChassis(TestCase):
    """Unitest cases for CHASSIS module"""
    def setUp(self):
        """setup before all cases"""
        self.log = message(name="CHASSIS")
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.ins = chassis()

        self.var = {}

        self.response = {}
        self.response["LE_HA_FPC_INFO"] = """
        <multi-routing-engine-results>

            <multi-routing-engine-item>

                <re-name>node0</re-name>

                <fpc-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-chassis" junos:style="pic-style">
                    <fpc>
                        <slot>0</slot>
                        <state>Online</state>
                        <description>FPC</description>
                        <pic>
                            <pic-slot>0</pic-slot>
                            <pic-state>Online</pic-state>
                            <pic-type>8xGE,8xGE SFP Base PIC</pic-type>
                        </pic>
                    </fpc>
                </fpc-information>
            </multi-routing-engine-item>

            <multi-routing-engine-item>

                <re-name>node1</re-name>

                <fpc-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-chassis" junos:style="pic-style">
                    <fpc>
                        <slot>0</slot>
                        <state>Online</state>
                        <description>FPC</description>
                        <pic>
                            <pic-slot>0</pic-slot>
                            <pic-state>Online</pic-state>
                            <pic-type>8xGE,8xGE SFP Base PIC</pic-type>
                        </pic>
                    </fpc>
                </fpc-information>
            </multi-routing-engine-item>

        </multi-routing-engine-results>
        """

        self.response["LE_SA_FPC_INFO"] = """
        <fpc-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-chassis" junos:style="pic-style">
            <fpc>
                <slot>0</slot>
                <state>Online</state>
                <description>FPC</description>
                <pic>
                    <pic-slot>0</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>8xGE,8xGE SFP Base PIC</pic-type>
                </pic>
            </fpc>
        </fpc-information>
        """

        self.response["HE_HA_FPC_INFO"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>SRX5k SPC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Cp</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>4</slot>
                    <state>Online</state>
                    <description>SRX5k DPC 40x 1GE</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 1GE RichQ</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 1GE RichQ</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 1GE RichQ</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 1GE RichQ</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>SRX5k SPC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Cp</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>4</slot>
                    <state>Online</state>
                    <description>SRX5k DPC 40x 1GE</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 1GE RichQ</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 1GE RichQ</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 1GE RichQ</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 1GE RichQ</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HE_SA_FPC_INFO"] = """
        <fpc-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-chassis" junos:style="pic-style">
            <fpc>
                <slot>0</slot>
                <state>Online</state>
                <description>SRX5k SPC II</description>
                <pic>
                    <pic-slot>0</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>SPU Cp</pic-type>
                </pic>
                <pic>
                    <pic-slot>1</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>SPU Flow</pic-type>
                </pic>
                <pic>
                    <pic-slot>2</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>SPU Flow</pic-type>
                </pic>
                <pic>
                    <pic-slot>3</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>SPU Flow</pic-type>
                </pic>
            </fpc>
            <fpc>
                <slot>2</slot>
                <state>Online</state>
                <description>SRX5k IOC II</description>
                <pic>
                    <pic-slot>0</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>10x 10GE SFP+</pic-type>
                </pic>
            </fpc>
        </fpc-information>
        """

        self.response["HE_SA_FPC_PIC_STATUS"] = """
            Slot 0   Online       SRX5k SPC II
              PIC 0  Online       SPU Cp
              PIC 1  Online       SPU Flow
              PIC 2  Online       SPU Flow
              PIC 3  Online       SPU Flow
            Slot 2   Online       SRX5k IOC II
              PIC 0  Online       10x 10GE SFP+
        """

        self.response["HE_SA_IOC3_FPC_PIC_STATUS"] = """
            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>SRX5k SPC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Cp</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>1</slot>
                    <state>Online</state>
                    <description>SRX5k IOC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 10GE SFP+</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>2</slot>
                    <state>Online</state>
                    <description>SRX5k IOC3 24XGE+6XLG</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>12x 10GE SFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>12x 10GE SFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>3x 40GE QSFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>3x 40GE QSFP+</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        """

        self.response["HE_HA_IOC3_FPC_PIC_STATUS"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>SRX5k SPC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Cp</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>1</slot>
                    <state>Online</state>
                    <description>SRX5k IOC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 10GE SFP+</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>2</slot>
                    <state>Online</state>
                    <description>SRX5k IOC3 24XGE+6XLG</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>12x 10GE SFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>12x 10GE SFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>3x 40GE QSFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>3x 40GE QSFP+</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>SRX5k SPC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Cp</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>1</slot>
                    <state>Online</state>
                    <description>SRX5k IOC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 10GE SFP+</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>2</slot>
                    <state>Online</state>
                    <description>SRX5k IOC3 24XGE+6XLG</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>12x 10GE SFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>12x 10GE SFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>3x 40GE QSFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>3x 40GE QSFP+</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>
    </multi-routing-engine-results>
        """

        self.response["HE_SA_IOC3_FPC_PIC_STATUS_WITH_OFFLINE"] = """
            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>SRX5k SPC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Cp</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Flow</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>1</slot>
                    <state>Online</state>
                    <description>SRX5k IOC II</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>10x 10GE SFP+</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>2</slot>
                    <state>Online</state>
                    <description>SRX5k IOC3 24XGE+6XLG</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>12x 10GE SFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>1</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>12x 10GE SFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>2</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>3x 40GE QSFP+</pic-type>
                    </pic>
                    <pic>
                        <pic-slot>3</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>3x 40GE QSFP+</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        """

        self.response["LE_HA_FPC_PIC_STATUS"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>6x GE, 4x GE SFP Base PIC</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>6x GE, 4x GE SFP Base PIC</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Offline</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>6x GE, 4x GE SFP Base PIC</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>6x GE, 4x GE SFP Base PIC</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["LE_HA_FPC_PIC_STATUS_OFFLINE_WITH_NO_PIC_INFO"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Offline</state>
                    <description>FPC</description>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>FPC</description>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HE_HA_CHASSIS_HARDWARE"] = """
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <chassis-inventory xmlns="http://xml.juniper.net/junos/17.2I0/junos-chassis">
                        <chassis junos:style="inventory">
                            <name>Chassis</name>
                            <serial-number>JN11C3B47AGB</serial-number>
                            <description>SRX5600</description>
                            <chassis-module>
                                <name>Midplane</name>
                                <version>REV 01</version>
                                <part-number>710-024804</part-number>
                                <serial-number>ABAC2270</serial-number>
                                <description>SRX5600 Midplane</description>
                                <model-number>SRX5600-MP-A</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>FPM Board</name>
                                <version>REV 01</version>
                                <part-number>710-024631</part-number>
                                <serial-number>ZJ7513</serial-number>
                                <description>Front Panel Display</description>
                                <model-number>SRX5600-CRAFT-A</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>PEM 0</name>
                                <version>Rev 03</version>
                                <part-number>740-034701</part-number>
                                <serial-number>QCS150609048</serial-number>
                                <description>PS 1.4-2.6kW; 90-264V AC in</description>
                                <model-number>SRX5600-PWR-2520-AC-S</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>PEM 1</name>
                                <version>Rev 03</version>
                                <part-number>740-034701</part-number>
                                <serial-number>QCS150609055</serial-number>
                                <description>PS 1.4-2.6kW; 90-264V AC in</description>
                                <model-number>SRX5600-PWR-2520-AC-S</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>Routing Engine 0</name>
                                <version>REV 09</version>
                                <part-number>740-023530</part-number>
                                <serial-number>9009071983</serial-number>
                                <description>SRX5k RE-13-20</description>
                                <model-number>SRX5K-RE-13-20-A</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>CB 0</name>
                                <version>REV 05</version>
                                <part-number>710-024802</part-number>
                                <serial-number>YZ3580</serial-number>
                                <description>SRX5k SCB</description>
                                <model-number>SRX5K-SCB-A</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>FPC 0</name>
                                <version>REV 15</version>
                                <part-number>750-044175</part-number>
                                <serial-number>CABA3319</serial-number>
                                <description>SRX5k SPC II</description>
                                <clei-code>COUCASFBAA</clei-code>
                                <model-number>SRX5K-SPC-4-15-320</model-number>
                                <chassis-sub-module>
                                    <name>CPU</name>
                                    <version></version>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SRX5k DPC PPC</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 0</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SPU Cp</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 1</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SPU Flow</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 2</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SPU Flow</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 3</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SPU Flow</description>
                                </chassis-sub-module>
                            </chassis-module>
                            <chassis-module>
                                <name>FPC 4</name>
                                <version>REV 25</version>
                                <part-number>750-020235</part-number>
                                <serial-number>ZK5408</serial-number>
                                <description>SRX5k DPC 40x 1GE</description>
                                <model-number>SRX5K-40GE-SFP-A</model-number>
                                <chassis-sub-module>
                                    <name>CPU</name>
                                    <version>REV 04</version>
                                    <part-number>710-024633</part-number>
                                    <serial-number>ZE8492</serial-number>
                                    <description>SRX5k DPC PMB</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 0</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>10x 1GE RichQ</description>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 0</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>0311212243279341</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 1</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ06020JTY</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 2</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ053903R7</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 3</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0835SB48Z</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 4</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>0408252133420556</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 5</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0637418Y</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 6</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0704S51WK</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 7</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0703S01UQ</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 8</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>0309032050012803</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 9</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0703S01VH</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 1</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>10x 1GE RichQ</description>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 0</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ051002CP</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 1</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AC0649S5479</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 2</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0706S564B</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 3</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM06404GFA</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 4</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0704S505K</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 5</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0705S544B</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 6</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>0411240228135296</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 7</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM06404G7K</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 8</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM06404JAR</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 9</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0703S01U6</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 2</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>10x 1GE RichQ</description>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 0</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>AM1039SHVKU</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 1</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>AM1039SHVLB</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 2</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ054103B9</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 3</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>AM1037SHN89</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 4</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM06404GFD</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 5</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0706S56RA</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 6</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM06404GEH</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 7</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ06020L82</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 8</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AC0704S0558</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 9</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ054404GE</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 3</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>10x 1GE RichQ</description>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 0</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ050801ZS</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 9</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0803S88R0</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                </chassis-sub-module>
                            </chassis-module>
                            <chassis-module>
                                <name>Fan Tray</name>
                                <description>Enhanced Fan Tray</description>
                                <model-number>SRX5600-HC-FAN</model-number>
                            </chassis-module>
                        </chassis>
                    </chassis-inventory>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <chassis-inventory xmlns="http://xml.juniper.net/junos/17.2I0/junos-chassis">
                        <chassis junos:style="inventory">
                            <name>Chassis</name>
                            <serial-number>JN11C334CAGB</serial-number>
                            <description>SRX5600</description>
                            <chassis-module>
                                <name>Midplane</name>
                                <version>REV 01</version>
                                <part-number>710-024804</part-number>
                                <serial-number>ABAB8221</serial-number>
                                <description>SRX5600 Midplane</description>
                                <model-number>SRX5600-MP-A</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>FPM Board</name>
                                <version>REV 01</version>
                                <part-number>710-024631</part-number>
                                <serial-number>YP7140</serial-number>
                                <description>Front Panel Display</description>
                                <model-number>SRX5600-CRAFT-A</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>PEM 0</name>
                                <version>Rev 03</version>
                                <part-number>740-034701</part-number>
                                <serial-number>QCS15060902A</serial-number>
                                <description>PS 1.4-2.6kW; 90-264V AC in</description>
                                <model-number>SRX5600-PWR-2520-AC-S</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>PEM 1</name>
                                <version>Rev 03</version>
                                <part-number>740-034701</part-number>
                                <serial-number>QCS150609044</serial-number>
                                <description>PS 1.4-2.6kW; 90-264V AC in</description>
                                <model-number>SRX5600-PWR-2520-AC-S</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>Routing Engine 0</name>
                                <version>REV 09</version>
                                <part-number>740-023530</part-number>
                                <serial-number>9009068370</serial-number>
                                <description>SRX5k RE-13-20</description>
                                <model-number>SRX5K-RE-13-20-A</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>CB 0</name>
                                <version>REV 05</version>
                                <part-number>710-024802</part-number>
                                <serial-number>YR4915</serial-number>
                                <description>SRX5k SCB</description>
                                <model-number>SRX5K-SCB-A</model-number>
                            </chassis-module>
                            <chassis-module>
                                <name>FPC 0</name>
                                <version>REV 14</version>
                                <part-number>750-044175</part-number>
                                <serial-number>CABA6982</serial-number>
                                <description>SRX5k SPC II</description>
                                <clei-code>COUCASFBAA</clei-code>
                                <model-number>SRX5K-SPC-4-15-320</model-number>
                                <chassis-sub-module>
                                    <name>CPU</name>
                                    <version></version>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SRX5k DPC PPC</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 0</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SPU Cp</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 1</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SPU Flow</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 2</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SPU Flow</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 3</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>SPU Flow</description>
                                </chassis-sub-module>
                            </chassis-module>
                            <chassis-module>
                                <name>FPC 4</name>
                                <version>REV 19</version>
                                <part-number>750-020235</part-number>
                                <serial-number>XN2827</serial-number>
                                <description>SRX5k DPC 40x 1GE</description>
                                <model-number>SRX5K-40GE-SFP-A</model-number>
                                <chassis-sub-module>
                                    <name>CPU</name>
                                    <version>REV 03</version>
                                    <part-number>710-024633</part-number>
                                    <serial-number>XN5350</serial-number>
                                    <description>SRX5k DPC PMB</description>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 0</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>10x 1GE RichQ</description>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 0</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>PJH525M</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 1</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>PJH525V</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 2</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>PJN4R20</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 3</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ0528029X</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 4</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ051002CB</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 5</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>AA0937SSHNM</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 6</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>AA0937SSHNG</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 7</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>AA0937SSHNH</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 8</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>AM1040SJ3RC</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 9</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>AM1040SJ3RG</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 1</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>10x 1GE RichQ</description>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 0</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0705S545W</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 1</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ054404GQ</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 2</name>
                                        <version>REV 01</version>
                                        <part-number>740-011782</part-number>
                                        <serial-number>P9907VL</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 3</name>
                                        <version>REV 01</version>
                                        <part-number>740-011782</part-number>
                                        <serial-number>P9908CN</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 4</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM06374175</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 5</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AC0649S5482</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 6</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0637418M</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 7</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0706S56R8</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 8</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0706S56QM</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 9</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AC0703S0563</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 2</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>10x 1GE RichQ</description>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 0</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ06050Q5W</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 1</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>0311181509573536</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 2</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0703S01T4</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 3</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ06020KST</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 4</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>AA0937SSHBU</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 5</name>
                                        <version>.</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>H121CBJ</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 6</name>
                                        <version></version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AM0706S56R3</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 7</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>0311181505243559</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 8</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>AJ06020HKA</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 9</name>
                                        <version>0</version>
                                        <part-number>NON-JNPR</part-number>
                                        <serial-number>0309232234516350</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                </chassis-sub-module>
                                <chassis-sub-module>
                                    <name>PIC 3</name>
                                    <part-number>BUILTIN</part-number>
                                    <serial-number>BUILTIN</serial-number>
                                    <description>10x 1GE RichQ</description>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 0</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>PJN4ZNB</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                    <chassis-sub-sub-module>
                                        <name>Xcvr 9</name>
                                        <version>REV 02</version>
                                        <part-number>740-011613</part-number>
                                        <serial-number>PJN4XVC</serial-number>
                                        <description>SFP-SX</description>
                                    </chassis-sub-sub-module>
                                </chassis-sub-module>
                            </chassis-module>
                            <chassis-module>
                                <name>Fan Tray</name>
                                <description>Enhanced Fan Tray</description>
                                <model-number>SRX5600-HC-FAN</model-number>
                            </chassis-module>
                        </chassis>
                    </chassis-inventory>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
        """

        self.response["HE_HA_FPC_PIC_STATUS_WITH_ONLY_ONE_NODE"] = """
        <multi-routing-engine-results>

        <multi-routing-engine-item>

        <re-name>node0</re-name>

        <fpc-information style="pic-style">
        <fpc>
        <slot>0</slot>
        <state>Online</state>
        <description>FPC</description>
        <pic>
        <pic-slot>0</pic-slot>
        <pic-state>Online</pic-state>
        <pic-type>8xGE,8xGE SFP Base PIC</pic-type>
        </pic>
        </fpc>
        </fpc-information>
        </multi-routing-engine-item>

        </multi-routing-engine-results>
        """

        self.response["LE_HA_FPC_PIC_STATUS_WITH_ONLY_ONE_ONLINE"] = """
        <multi-routing-engine-results>

        <multi-routing-engine-item>

        <re-name>node0</re-name>

        <fpc-information style="pic-style"/>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

        <re-name>node1</re-name>

        <fpc-information style="pic-style">
        <fpc>
        <slot>0</slot>
        <state>Online</state>
        <description>FPC</description>
        <pic>
        <pic-slot>0</pic-slot>
        <pic-state>Online</pic-state>
        <pic-type>VSRX DPDK GE</pic-type>
        </pic>
        </fpc>
        </fpc-information>
        </multi-routing-engine-item>

        </multi-routing-engine-results>
        """

    def tearDown(self):
        """teardown after all case"""
        pass

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_chassis_hardware_info(self, mock_send_cli_cmd):
        """test get chassis hardware info"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        self.log.display_title(title=self.tool.get_current_function_name())

        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_HA_CHASSIS_HARDWARE"])
        result = self.ins.get_chassis_hardware_info(device=mock_device_ins, force_get=True)
        self.assertTrue(isinstance(result, dict))

        self.log.display_title(title="check secondary hardware info get not from previous result")
        result = self.ins.get_chassis_hardware_info(device=mock_device_ins, force_get=False)
        self.assertTrue(isinstance(result, dict))

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_chassis_fpc_info(self, mock_send_cli_cmd):
        """checking get chassis fpc info

        Because use pyez channel and format is xml, it means device response exclude 'rpc-reply' element
        """
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        self.log.display_title(msg=self.tool.get_current_function_name())
        self.log.step_num = 0

        self.log.display_step(new_step=True, show_result=False, level="INFO", msg="get fpc info from low-end HA testbed")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["LE_HA_FPC_INFO"])
        xml_dict = self.ins.get_chassis_fpc_info(device=mock_device_ins, force_get=True)
        self.assertTrue(xml_dict["multi-routing-engine-results"]["multi-routing-engine-item"][0]["fpc-information"]["fpc"]["state"] == "Online")

        self.log.display_step(new_step=True, show_result=False, level="INFO", msg="get fpc info from previous result")
        xml_dict = self.ins.get_chassis_fpc_info(device=mock_device_ins)
        self.assertTrue(xml_dict["multi-routing-engine-results"]["multi-routing-engine-item"][0]["fpc-information"]["fpc"]["state"] == "Online")

    @mock.patch("time.sleep")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_waiting_for_pic_online(self, mock_send_cli_cmd, mock_sleep):
        """checking waiting for pic online"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        self.log.display_title(msg=self.tool.get_current_function_name())
        self.log.step_num = 0

        msg = "waiting for HE SA FPC PIC are all onlined..."
        self.log.display_step(msg=msg, level="INFO", new_step=True, show_result=False)
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_HA_FPC_INFO"])
        self.assertTrue(self.ins.waiting_for_pic_online(device=mock_device_ins))

        msg = "waiting for HE SA FPC PIC with IOC3 are all onlined..."
        self.log.display_step(msg=msg, level="INFO", new_step=True, show_result=False)
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_SA_IOC3_FPC_PIC_STATUS"])
        self.assertTrue(self.ins.waiting_for_pic_online(device=mock_device_ins))

        msg = "waiting for HE SA FPC PIC with IOC3 have not onlined pic..."
        self.log.display_step(msg=msg, level="INFO", new_step=True, show_result=False)
        mock_send_cli_cmd.side_effect = [
            self.xml.xml_string_to_dict(self.response["HE_SA_IOC3_FPC_PIC_STATUS_WITH_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["HE_SA_IOC3_FPC_PIC_STATUS_WITH_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["HE_SA_IOC3_FPC_PIC_STATUS_WITH_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["HE_SA_IOC3_FPC_PIC_STATUS_WITH_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["HE_SA_IOC3_FPC_PIC_STATUS_WITH_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["HE_SA_IOC3_FPC_PIC_STATUS"]),
        ]
        self.assertTrue(self.ins.waiting_for_pic_online(device=mock_device_ins, except_component="PIC 3"))

        msg = "waiting for LE HA topology..."
        self.log.display_step(msg=msg, level="INFO", new_step=True, show_result=False)
        mock_send_cli_cmd.side_effect = [self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS"]), ]
        self.assertTrue(self.ins.waiting_for_pic_online(device=mock_device_ins))

        msg = "waiting for HE HA with not online FPC..."
        self.log.display_step(msg=msg, level="INFO", new_step=True, show_result=False)
        mock_send_cli_cmd.side_effect = [
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
        ]
        self.assertFalse(self.ins.waiting_for_pic_online(device=mock_device_ins, check_counter=10, check_interval=0.1))

        msg = "waiting for LE HA and have except component..."
        self.log.display_step(msg=msg, level="INFO", new_step=True, show_result=False)
        mock_send_cli_cmd.side_effect = [
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
        ]
        result = self.ins.waiting_for_pic_online(
            device=mock_device_ins,
            check_counter=10,
            check_interval=0.001,
            except_component=("Slot 0", "SLOT 0 PIC 1"),
        )
        self.assertTrue(result)

        mock_send_cli_cmd.side_effect = [
            False,
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE_WITH_NO_PIC_INFO"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE_WITH_NO_PIC_INFO"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_OFFLINE"]),
        ]
        result = self.ins.waiting_for_pic_online(
            device=mock_device_ins,
            check_counter=10,
            check_interval=0.001,
            except_component="PIC 0",
        )
        self.assertFalse(result)

        msg = "waiting for HA topo only one node onlined..."
        self.log.display_step(msg=msg, level="INFO", new_step=True, show_result=False)
        mock_send_cli_cmd.side_effect = [
            self.xml.xml_string_to_dict(self.response["HE_HA_FPC_PIC_STATUS_WITH_ONLY_ONE_NODE"]),
            self.xml.xml_string_to_dict(self.response["LE_HA_FPC_PIC_STATUS_WITH_ONLY_ONE_ONLINE"]),
            self.xml.xml_string_to_dict(self.response["HE_HA_FPC_PIC_STATUS_WITH_ONLY_ONE_NODE"]),
            self.xml.xml_string_to_dict(self.response["HE_HA_FPC_INFO"]),
        ]
        result = self.ins.waiting_for_pic_online(
            device=mock_device_ins,
            check_counter=4,
            check_interval=0.001,
        )
        self.assertTrue(result)
