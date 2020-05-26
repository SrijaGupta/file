# coding: UTF-8
"""All unit test cases for NAT module"""
# pylint: disable=attribute-defined-outside-init,invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

from unittest import TestCase, mock

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.security.nat.nat import nat


class TestNat(TestCase):
    """Unitest cases for NAT module"""
    def setUp(self):
        """setup before all case"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.ins = nat()
        self.ins.debug_to_stdout = True


        self.response = {}
        self.response["SA_SNAT_POOL_INFO"] = """
        <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
            <total-source-nat-pools>
                <total-source-pools>2</total-source-pools>
            </total-source-nat-pools>
            <source-nat-pool-info-entry>
                <pool-name>A_POOL</pool-name>
                <pool-id>4</pool-id>
                <routing-instance-name>default</routing-instance-name>
                <host-address-base>0.0.0.0</host-address-base>
                <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
                <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
                <port-overloading-factor>1</port-overloading-factor>
                <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                <total-pool-address>256</total-pool-address>
                <address-pool-hits>0</address-pool-hits>
                <source-pool-address-range>
                    <address-range-low>192.168.1.0</address-range-low>
                    <address-range-high>192.168.1.255</address-range-high>
                    <single-port>0</single-port>
                    <twin-port>0</twin-port>
                </source-pool-address-range>
                <source-pool-address-range-sum>
                    <single-port-sum>0</single-port-sum>
                    <twin-port-sum>0</twin-port-sum>
                </source-pool-address-range-sum>
            </source-nat-pool-info-entry>
            <source-nat-pool-info-entry>
                <pool-name>B_POOL</pool-name>
                <pool-id>5</pool-id>
                <routing-instance-name>default</routing-instance-name>
                <host-address-base>0.0.0.0</host-address-base>
                <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
                <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
                <port-overloading-factor>1</port-overloading-factor>
                <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                <total-pool-address>256</total-pool-address>
                <address-pool-hits>0</address-pool-hits>
                <source-pool-address-range>
                    <address-range-low>192.168.2.0</address-range-low>
                    <address-range-high>192.168.2.255</address-range-high>
                    <single-port>0</single-port>
                    <twin-port>0</twin-port>
                </source-pool-address-range>
                <source-pool-address-range-sum>
                    <single-port-sum>0</single-port-sum>
                    <twin-port-sum>0</twin-port-sum>
                </source-pool-address-range-sum>
            </source-nat-pool-info-entry>
        </source-nat-pool-detail-information>
        """

        self.response["SA_SNAT_POOL_INFO_EXTEND_1"] = """
        <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-nat">
            <source-nat-pool-info-entry>
                <pool-name>root_src_v4_pat</pool-name>
                <pool-id>4</pool-id>
                <routing-instance-name>default</routing-instance-name>
                <source-pool-port-translation>[10001, 12500]</source-pool-port-translation>
                <port-overloading-factor>1</port-overloading-factor>
                <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                <total-pool-address>1</total-pool-address>
                <address-pool-hits>495</address-pool-hits>
                <source-pool-blk-size>1</source-pool-blk-size>
                <source-pool-blk-max-per-host>8</source-pool-blk-max-per-host>
                <source-pool-blk-atv-timeout>0</source-pool-blk-atv-timeout>
                <source-pool-last-blk-rccl-timeout>0</source-pool-last-blk-rccl-timeout>
                <source-pool-blk-interim-log-cycle>0</source-pool-blk-interim-log-cycle>
                <source-pool-blk-log>Enable</source-pool-blk-log>
                <source-pool-blk-used>4</source-pool-blk-used>
                <source-pool-blk-total>2500</source-pool-blk-total>
                <source-pool-address-range junos:style="with-twin-port">
                    <address-range-low>200.0.1.11</address-range-low>
                    <address-range-high>200.0.1.11</address-range-high>
                    <single-port>3</single-port>
                    <twin-port>0</twin-port>
                </source-pool-address-range>
                <source-pool-address-range-sum>
                    <single-port-sum>3</single-port-sum>
                    <twin-port-sum>0</twin-port-sum>
                </source-pool-address-range-sum>
            </source-nat-pool-info-entry>
        </source-nat-pool-detail-information>
        """

        self.response["SA_SNAT_POOL_INFO_EXTEND_2"] = """
        <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-nat">
            <source-nat-pool-info-entry>
                <pool-name>root_src_v4_pat_4</pool-name>
                <pool-id>7</pool-id>
                <routing-instance-name>default</routing-instance-name>
                <source-pool-port-translation>[10001, 12500]</source-pool-port-translation>
                <port-overloading-factor>1</port-overloading-factor>
                <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                <total-pool-address>1</total-pool-address>
                <address-pool-hits>0</address-pool-hits>
                <source-pool-blk-size>2500</source-pool-blk-size>
                <source-pool-determ-host-range-num>1</source-pool-determ-host-range-num>
                <source-pool-address-range junos:style="with-twin-port">
                    <address-range-low>200.0.4.14</address-range-low>
                    <address-range-high>200.0.4.14</address-range-high>
                    <single-port>0</single-port>
                    <twin-port>0</twin-port>
                </source-pool-address-range>
                <source-pool-address-range-sum>
                    <single-port-sum>0</single-port-sum>
                    <twin-port-sum>0</twin-port-sum>
                </source-pool-address-range-sum>
            </source-nat-pool-info-entry>
        </source-nat-pool-detail-information>
        """

        self.response["SA_SNAT_POOL_INFO_NO_ELEMENTS"] = """
        <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-nat">
            <source-nat-pool-info-entry>
                <pool-name>root_src_v4_pat_4</pool-name>
                <pool-id>7</pool-id>
                <routing-instance-name>default</routing-instance-name>
                <source-pool-port-translation>[10001, 12500]</source-pool-port-translation>
                <port-overloading-factor>1</port-overloading-factor>
                <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                <total-pool-address>1</total-pool-address>
                <address-pool-hits>0</address-pool-hits>
                <source-pool-blk-size>2500</source-pool-blk-size>
                <source-pool-determ-host-range-num>1</source-pool-determ-host-range-num>
            </source-nat-pool-info-entry>
        </source-nat-pool-detail-information>
        """

        self.response["SA_SNAT_POOL_INFO_NO_NEEDED_ELEMENT"] = """
        <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/20.2I0/junos-nat">
        </source-nat-pool-detail-information>
        """


        self.response["SA_SNAT_POOL_INFO_ONLY_1"] = """
        <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
            <total-source-nat-pools>
                <total-source-pools>1</total-source-pools>
            </total-source-nat-pools>
            <source-nat-pool-info-entry>
                <pool-name>A_POOL</pool-name>
                <pool-id>4</pool-id>
                <routing-instance-name>default</routing-instance-name>
                <host-address-base>0.0.0.0</host-address-base>
                <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
                <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
                <port-overloading-factor>1</port-overloading-factor>
                <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                <total-pool-address>256</total-pool-address>
                <address-pool-hits>0</address-pool-hits>
                <source-pool-address-range>
                    <address-range-low>192.168.1.0</address-range-low>
                    <address-range-high>192.168.1.255</address-range-high>
                    <single-port>0</single-port>
                    <twin-port>0</twin-port>
                </source-pool-address-range>
                <source-pool-address-range-sum>
                    <single-port-sum>0</single-port-sum>
                    <twin-port-sum>0</twin-port-sum>
                </source-pool-address-range-sum>
            </source-nat-pool-info-entry>
        </source-nat-pool-detail-information>
        """


        self.response["HA_SNAT_POOL_INFO"] = """
        <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <total-source-nat-pools>
                    <total-source-pools>3</total-source-pools>
                </total-source-nat-pools>
                <source-nat-pool-info-entry>
                    <pool-name>persistent_pool</pool-name>
                    <pool-id>4</pool-id>
                    <routing-instance-name>default</routing-instance-name>
                    <host-address-base>0.0.0.0</host-address-base>
                    <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
                    <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
                    <port-overloading-factor>1</port-overloading-factor>
                    <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                    <total-pool-address>6</total-pool-address>
                    <address-pool-hits>0</address-pool-hits>
                    <source-pool-address-range>
                        <address-range-low>192.168.150.5</address-range-low>
                        <address-range-high>192.168.150.10</address-range-high>
                        <single-port>0</single-port>
                        <twin-port>0</twin-port>
                    </source-pool-address-range>
                    <source-pool-address-range-sum>
                        <single-port-sum>0</single-port-sum>
                        <twin-port-sum>0</twin-port-sum>
                    </source-pool-address-range-sum>
                </source-nat-pool-info-entry>
                <source-nat-pool-info-entry>
                    <pool-name>A_POOL</pool-name>
                    <pool-id>5</pool-id>
                    <routing-instance-name>default</routing-instance-name>
                    <source-pool-port-translation>[1024, 65535]</source-pool-port-translation>
                    <port-overloading-factor>1</port-overloading-factor>
                    <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                    <total-pool-address>6</total-pool-address>
                    <address-pool-hits>0</address-pool-hits>
                    <source-pool-blk-size>8</source-pool-blk-size>
                    <source-pool-determ-host-range-num>1</source-pool-determ-host-range-num>
                    <source-pool-address-range>
                        <address-range-low>192.168.15.10</address-range-low>
                        <address-range-high>192.168.15.15</address-range-high>
                        <single-port>0</single-port>
                        <twin-port>0</twin-port>
                    </source-pool-address-range>
                    <source-pool-address-range-sum>
                        <single-port-sum>0</single-port-sum>
                        <twin-port-sum>0</twin-port-sum>
                    </source-pool-address-range-sum>
                </source-nat-pool-info-entry>
                <source-nat-pool-info-entry>
                    <pool-name>B_POOL</pool-name>
                    <pool-id>6</pool-id>
                    <routing-instance-name>default</routing-instance-name>
                    <source-pool-port-translation>[1024, 65535]</source-pool-port-translation>
                    <port-overloading-factor>1</port-overloading-factor>
                    <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                    <total-pool-address>6</total-pool-address>
                    <address-pool-hits>0</address-pool-hits>
                    <source-pool-blk-size>8</source-pool-blk-size>
                    <source-pool-determ-host-range-num>1</source-pool-determ-host-range-num>
                    <source-pool-address-range>
                        <address-range-low>192.168.15.20</address-range-low>
                        <address-range-high>192.168.15.25</address-range-high>
                        <single-port>0</single-port>
                        <twin-port>0</twin-port>
                    </source-pool-address-range>
                    <source-pool-address-range-sum>
                        <single-port-sum>0</single-port-sum>
                        <twin-port-sum>0</twin-port-sum>
                    </source-pool-address-range-sum>
                </source-nat-pool-info-entry>
            </source-nat-pool-detail-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <total-source-nat-pools>
                    <total-source-pools>3</total-source-pools>
                </total-source-nat-pools>
                <source-nat-pool-info-entry>
                    <pool-name>persistent_pool</pool-name>
                    <pool-id>4</pool-id>
                    <routing-instance-name>default</routing-instance-name>
                    <host-address-base>0.0.0.0</host-address-base>
                    <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
                    <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
                    <port-overloading-factor>1</port-overloading-factor>
                    <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                    <total-pool-address>6</total-pool-address>
                    <address-pool-hits>0</address-pool-hits>
                    <source-pool-address-range>
                        <address-range-low>192.168.150.5</address-range-low>
                        <address-range-high>192.168.150.10</address-range-high>
                        <single-port>0</single-port>
                        <twin-port>0</twin-port>
                    </source-pool-address-range>
                    <source-pool-address-range-sum>
                        <single-port-sum>0</single-port-sum>
                        <twin-port-sum>0</twin-port-sum>
                    </source-pool-address-range-sum>
                </source-nat-pool-info-entry>
                <source-nat-pool-info-entry>
                    <pool-name>A_POOL</pool-name>
                    <pool-id>5</pool-id>
                    <routing-instance-name>default</routing-instance-name>
                    <source-pool-port-translation>[1024, 65535]</source-pool-port-translation>
                    <port-overloading-factor>1</port-overloading-factor>
                    <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                    <total-pool-address>6</total-pool-address>
                    <address-pool-hits>0</address-pool-hits>
                    <source-pool-blk-size>8</source-pool-blk-size>
                    <source-pool-determ-host-range-num>1</source-pool-determ-host-range-num>
                    <source-pool-address-range>
                        <address-range-low>192.168.15.10</address-range-low>
                        <address-range-high>192.168.15.15</address-range-high>
                        <single-port>0</single-port>
                        <twin-port>0</twin-port>
                    </source-pool-address-range>
                    <source-pool-address-range-sum>
                        <single-port-sum>0</single-port-sum>
                        <twin-port-sum>0</twin-port-sum>
                    </source-pool-address-range-sum>
                </source-nat-pool-info-entry>
                <source-nat-pool-info-entry>
                    <pool-name>B_POOL</pool-name>
                    <pool-id>6</pool-id>
                    <routing-instance-name>default</routing-instance-name>
                    <source-pool-port-translation>[1024, 65535]</source-pool-port-translation>
                    <port-overloading-factor>1</port-overloading-factor>
                    <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                    <total-pool-address>6</total-pool-address>
                    <address-pool-hits>0</address-pool-hits>
                    <source-pool-blk-size>8</source-pool-blk-size>
                    <source-pool-determ-host-range-num>1</source-pool-determ-host-range-num>
                    <source-pool-address-range>
                        <address-range-low>192.168.15.20</address-range-low>
                        <address-range-high>192.168.15.25</address-range-high>
                        <single-port>0</single-port>
                        <twin-port>0</twin-port>
                    </source-pool-address-range>
                    <source-pool-address-range-sum>
                        <single-port-sum>0</single-port-sum>
                        <twin-port-sum>0</twin-port-sum>
                    </source-pool-address-range-sum>
                </source-nat-pool-info-entry>
            </source-nat-pool-detail-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_SNAT_POOL_INFO_ONLY_1"] = """
        <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <total-source-nat-pools>
                    <total-source-pools>1</total-source-pools>
                </total-source-nat-pools>
                <source-nat-pool-info-entry>
                    <pool-name>persistent_pool</pool-name>
                    <pool-id>4</pool-id>
                    <routing-instance-name>default</routing-instance-name>
                    <host-address-base>0.0.0.0</host-address-base>
                    <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
                    <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
                    <port-overloading-factor>1</port-overloading-factor>
                    <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                    <total-pool-address>6</total-pool-address>
                    <address-pool-hits>0</address-pool-hits>
                    <source-pool-address-range>
                        <address-range-low>192.168.150.5</address-range-low>
                        <address-range-high>192.168.150.10</address-range-high>
                        <single-port>0</single-port>
                        <twin-port>0</twin-port>
                    </source-pool-address-range>
                    <source-pool-address-range-sum>
                        <single-port-sum>0</single-port-sum>
                        <twin-port-sum>0</twin-port-sum>
                    </source-pool-address-range-sum>
                </source-nat-pool-info-entry>
            </source-nat-pool-detail-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <total-source-nat-pools>
                    <total-source-pools>1</total-source-pools>
                </total-source-nat-pools>
                <source-nat-pool-info-entry>
                    <pool-name>persistent_pool</pool-name>
                    <pool-id>4</pool-id>
                    <routing-instance-name>default</routing-instance-name>
                    <host-address-base>0.0.0.0</host-address-base>
                    <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
                    <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
                    <port-overloading-factor>1</port-overloading-factor>
                    <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                    <total-pool-address>6</total-pool-address>
                    <address-pool-hits>0</address-pool-hits>
                    <source-pool-address-range>
                        <address-range-low>192.168.150.5</address-range-low>
                        <address-range-high>192.168.150.10</address-range-high>
                        <single-port>0</single-port>
                        <twin-port>0</twin-port>
                    </source-pool-address-range>
                    <source-pool-address-range-sum>
                        <single-port-sum>0</single-port-sum>
                        <twin-port-sum>0</twin-port-sum>
                    </source-pool-address-range-sum>
                </source-nat-pool-info-entry>
            </source-nat-pool-detail-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["SA_SNAT_RULE_INFO"] = """
        <source-nat-rule-detail-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
            <total-source-nat-rules>
                <total-src-rules>1</total-src-rules>
            </total-source-nat-rules>
            <total-source-nat-rule-ref-addr-num>
                <total-source-nat-rule-ref-addr-num-v4>2</total-source-nat-rule-ref-addr-num-v4>
                <total-source-nat-rule-ref-addr-num-v6>0</total-source-nat-rule-ref-addr-num-v6>
            </total-source-nat-rule-ref-addr-num>
            <source-nat-rule-entry>
                <rule-name>A_rule</rule-name>
                <rule-set-name>A_ruleset</rule-set-name>
                <rule-id>1</rule-id>
                <rule-matching-position>1</rule-matching-position>
                <rule-from-context>zone</rule-from-context>
                <rule-from-context-name>trust</rule-from-context-name>
                <rule-to-context>zone</rule-to-context>
                <rule-to-context-name>untrust</rule-to-context-name>
                <source-address-range-entry>
                    <rule-source-address-low-range>0.0.0.0</rule-source-address-low-range>
                    <rule-source-address-high-range>0.0.0.0</rule-source-address-high-range>
                </source-address-range-entry>
                <destination-address-range-entry>
                    <rule-destination-address-low-range>0.0.0.0</rule-destination-address-low-range>
                    <rule-destination-address-high-range>0.0.0.0</rule-destination-address-high-range>
                </destination-address-range-entry>
                <src-nat-app-entry>
                    <src-nat-application>configured</src-nat-application>
                </src-nat-app-entry>
                <source-nat-rule-action-entry>
                    <source-nat-rule-action>A_POOL</source-nat-rule-action>
                    <persistent-nat-type>N/A              </persistent-nat-type>
                    <persistent-nat-mapping-type>address-port-mapping </persistent-nat-mapping-type>
                    <persistent-nat-timeout>0</persistent-nat-timeout>
                    <persistent-nat-max-session>0</persistent-nat-max-session>
                </source-nat-rule-action-entry>
                <source-nat-rule-hits-entry>
                    <rule-translation-hits>0</rule-translation-hits>
                    <succ-hits>0</succ-hits>
                    <failed-hits>0</failed-hits>
                    <concurrent-hits>0</concurrent-hits>
                </source-nat-rule-hits-entry>
            </source-nat-rule-entry>
        </source-nat-rule-detail-information>
        """

        self.response["SA_SNAT_RULE_INFO_NO_ELEMENT"] = """
        <source-nat-rule-detail-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
            <total-source-nat-rules>
                <total-src-rules>1</total-src-rules>
            </total-source-nat-rules>
            <total-source-nat-rule-ref-addr-num>
                <total-source-nat-rule-ref-addr-num-v4>2</total-source-nat-rule-ref-addr-num-v4>
                <total-source-nat-rule-ref-addr-num-v6>0</total-source-nat-rule-ref-addr-num-v6>
            </total-source-nat-rule-ref-addr-num>
            <source-nat-rule-entry>
                <rule-name>A_rule</rule-name>
                <rule-set-name>A_ruleset</rule-set-name>
                <rule-id>1</rule-id>
                <rule-matching-position>1</rule-matching-position>
                <rule-from-context>zone</rule-from-context>
                <rule-from-context-name>trust</rule-from-context-name>
                <rule-to-context>zone</rule-to-context>
                <rule-to-context-name>untrust</rule-to-context-name>
                <source-address-range-entry>
                    <rule-source-address-low-range>0.0.0.0</rule-source-address-low-range>
                    <rule-source-address-high-range>0.0.0.0</rule-source-address-high-range>
                </source-address-range-entry>
                <destination-address-range-entry>
                    <rule-destination-address-low-range>0.0.0.0</rule-destination-address-low-range>
                    <rule-destination-address-high-range>0.0.0.0</rule-destination-address-high-range>
                </destination-address-range-entry>
                <src-nat-app-entry>
                    <src-nat-application>configured</src-nat-application>
                </src-nat-app-entry>
                <source-nat-rule-hits-entry>
                    <rule-translation-hits>0</rule-translation-hits>
                    <succ-hits>0</succ-hits>
                    <failed-hits>0</failed-hits>
                    <concurrent-hits>0</concurrent-hits>
                </source-nat-rule-hits-entry>
            </source-nat-rule-entry>
        </source-nat-rule-detail-information>
        """

        self.response["HA_SNAT_RULE_INFO"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <source-nat-rule-detail-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <total-source-nat-rules>
                    <total-src-rules>2</total-src-rules>
                </total-source-nat-rules>
                <total-source-nat-rule-ref-addr-num>
                    <total-source-nat-rule-ref-addr-num-v4>4</total-source-nat-rule-ref-addr-num-v4>
                    <total-source-nat-rule-ref-addr-num-v6>0</total-source-nat-rule-ref-addr-num-v6>
                </total-source-nat-rule-ref-addr-num>
                <source-nat-rule-entry>
                    <rule-name>sr</rule-name>
                    <rule-set-name>trust_to_untrust</rule-set-name>
                    <rule-id>1</rule-id>
                    <rule-matching-position>1</rule-matching-position>
                    <rule-from-context>zone</rule-from-context>
                    <rule-from-context-name>trust</rule-from-context-name>
                    <rule-to-context>zone</rule-to-context>
                    <rule-to-context-name>untrust</rule-to-context-name>
                    <source-address-range-entry>
                        <rule-source-address-low-range>0.0.0.0</rule-source-address-low-range>
                        <rule-source-address-high-range>255.255.255.255</rule-source-address-high-range>
                    </source-address-range-entry>
                    <destination-address-range-entry>
                        <rule-destination-address-low-range>192.168.200.0</rule-destination-address-low-range>
                        <rule-destination-address-high-range>192.168.200.255</rule-destination-address-high-range>
                    </destination-address-range-entry>
                    <destination-port-entry></destination-port-entry>
                    <source-port-entry></source-port-entry>
                    <src-nat-protocol-entry></src-nat-protocol-entry>
                    <source-nat-rule-action-entry>
                        <source-nat-rule-action>persistent_pool</source-nat-rule-action>
                        <persistent-nat-type>any-remote-host  </persistent-nat-type>
                        <persistent-nat-mapping-type>address-port-mapping </persistent-nat-mapping-type>
                        <persistent-nat-timeout>300</persistent-nat-timeout>
                        <persistent-nat-max-session>30</persistent-nat-max-session>
                    </source-nat-rule-action-entry>
                    <source-nat-rule-hits-entry>
                        <rule-translation-hits>0</rule-translation-hits>
                        <succ-hits>0</succ-hits>
                        <failed-hits>0</failed-hits>
                        <concurrent-hits>0</concurrent-hits>
                    </source-nat-rule-hits-entry>
                </source-nat-rule-entry>
                <source-nat-rule-entry>
                    <rule-name>sr1</rule-name>
                    <rule-set-name>untrust_to_trust</rule-set-name>
                    <rule-id>2</rule-id>
                    <rule-matching-position>2</rule-matching-position>
                    <rule-from-context>zone</rule-from-context>
                    <rule-from-context-name>untrust</rule-from-context-name>
                    <rule-to-context>zone</rule-to-context>
                    <rule-to-context-name>trust</rule-to-context-name>
                    <source-address-range-entry>
                        <rule-source-address-low-range>0.0.0.0</rule-source-address-low-range>
                        <rule-source-address-high-range>255.255.255.255</rule-source-address-high-range>
                    </source-address-range-entry>
                    <destination-address-range-entry>
                        <rule-destination-address-low-range>192.168.100.0</rule-destination-address-low-range>
                        <rule-destination-address-high-range>192.168.100.255</rule-destination-address-high-range>
                    </destination-address-range-entry>
                    <src-nat-app-entry>
                        <src-nat-application>configured</src-nat-application>
                    </src-nat-app-entry>
                    <source-nat-rule-action-entry>
                        <source-nat-rule-action>B_POOL</source-nat-rule-action>
                        <persistent-nat-type>N/A              </persistent-nat-type>
                        <persistent-nat-mapping-type>address-port-mapping </persistent-nat-mapping-type>
                        <persistent-nat-timeout>0</persistent-nat-timeout>
                        <persistent-nat-max-session>0</persistent-nat-max-session>
                    </source-nat-rule-action-entry>
                    <source-nat-rule-hits-entry>
                        <rule-translation-hits>0</rule-translation-hits>
                        <succ-hits>0</succ-hits>
                        <failed-hits>0</failed-hits>
                        <concurrent-hits>0</concurrent-hits>
                    </source-nat-rule-hits-entry>
                </source-nat-rule-entry>
            </source-nat-rule-detail-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <source-nat-rule-detail-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <total-source-nat-rules>
                    <total-src-rules>2</total-src-rules>
                </total-source-nat-rules>
                <total-source-nat-rule-ref-addr-num>
                    <total-source-nat-rule-ref-addr-num-v4>4</total-source-nat-rule-ref-addr-num-v4>
                    <total-source-nat-rule-ref-addr-num-v6>0</total-source-nat-rule-ref-addr-num-v6>
                </total-source-nat-rule-ref-addr-num>
                <source-nat-rule-entry>
                    <rule-name>sr</rule-name>
                    <rule-set-name>trust_to_untrust</rule-set-name>
                    <rule-id>1</rule-id>
                    <rule-matching-position>1</rule-matching-position>
                    <rule-from-context>zone</rule-from-context>
                    <rule-from-context-name>trust</rule-from-context-name>
                    <rule-to-context>zone</rule-to-context>
                    <rule-to-context-name>untrust</rule-to-context-name>
                    <source-address-range-entry>
                        <rule-source-address-low-range>0.0.0.0</rule-source-address-low-range>
                        <rule-source-address-high-range>255.255.255.255</rule-source-address-high-range>
                    </source-address-range-entry>
                    <destination-address-range-entry>
                        <rule-destination-address-low-range>192.168.200.0</rule-destination-address-low-range>
                        <rule-destination-address-high-range>192.168.200.255</rule-destination-address-high-range>
                    </destination-address-range-entry>
                    <destination-port-entry></destination-port-entry>
                    <source-port-entry></source-port-entry>
                    <src-nat-protocol-entry></src-nat-protocol-entry>
                    <source-nat-rule-action-entry>
                        <source-nat-rule-action>persistent_pool</source-nat-rule-action>
                        <persistent-nat-type>any-remote-host  </persistent-nat-type>
                        <persistent-nat-mapping-type>address-port-mapping </persistent-nat-mapping-type>
                        <persistent-nat-timeout>300</persistent-nat-timeout>
                        <persistent-nat-max-session>30</persistent-nat-max-session>
                    </source-nat-rule-action-entry>
                    <source-nat-rule-hits-entry>
                        <rule-translation-hits>0</rule-translation-hits>
                        <succ-hits>0</succ-hits>
                        <failed-hits>0</failed-hits>
                        <concurrent-hits>0</concurrent-hits>
                    </source-nat-rule-hits-entry>
                </source-nat-rule-entry>
                <source-nat-rule-entry>
                    <rule-name>sr1</rule-name>
                    <rule-set-name>untrust_to_trust</rule-set-name>
                    <rule-id>2</rule-id>
                    <rule-matching-position>2</rule-matching-position>
                    <rule-from-context>zone</rule-from-context>
                    <rule-from-context-name>untrust</rule-from-context-name>
                    <rule-to-context>zone</rule-to-context>
                    <rule-to-context-name>trust</rule-to-context-name>
                    <source-address-range-entry>
                        <rule-source-address-low-range>0.0.0.0</rule-source-address-low-range>
                        <rule-source-address-high-range>255.255.255.255</rule-source-address-high-range>
                    </source-address-range-entry>
                    <destination-address-range-entry>
                        <rule-destination-address-low-range>192.168.100.0</rule-destination-address-low-range>
                        <rule-destination-address-high-range>192.168.100.255</rule-destination-address-high-range>
                    </destination-address-range-entry>
                    <src-nat-app-entry>
                        <src-nat-application>configured</src-nat-application>
                    </src-nat-app-entry>
                    <source-nat-rule-action-entry>
                        <source-nat-rule-action>B_POOL</source-nat-rule-action>
                        <persistent-nat-type>N/A              </persistent-nat-type>
                        <persistent-nat-mapping-type>address-port-mapping </persistent-nat-mapping-type>
                        <persistent-nat-timeout>0</persistent-nat-timeout>
                        <persistent-nat-max-session>0</persistent-nat-max-session>
                    </source-nat-rule-action-entry>
                    <source-nat-rule-hits-entry>
                        <rule-translation-hits>0</rule-translation-hits>
                        <succ-hits>0</succ-hits>
                        <failed-hits>0</failed-hits>
                        <concurrent-hits>0</concurrent-hits>
                    </source-nat-rule-hits-entry>
                </source-nat-rule-entry>
            </source-nat-rule-detail-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["SNAT_PORT_BLOCK_INFO"] = """
        <pba-blk-table xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
            <pba-pool-info-entry>
                <pba-pool-name>A_POOL</pba-pool-name>
                <pba-olfactor>1</pba-olfactor>
                <pba-size>128</pba-size>
                <pba-per-host>8</pba-per-host>
                <pba-timeout>0</pba-timeout>
                <pba-last-blk-timeout>0</pba-last-blk-timeout>
                <pba-blk-total>129024</pba-blk-total>
                <pba-blk-used>0</pba-blk-used>
            </pba-pool-info-entry>
        </pba-blk-table>
        """

        self.response["SNAT_PORT_BLOCK_INFO_WITH_1_ENTRY"] = """
        <pba-blk-table xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
            <pba-pool-info-entry>
                <pba-pool-name>A_POOL</pba-pool-name>
                <pba-olfactor>1</pba-olfactor>
                <pba-size>64</pba-size>
                <pba-per-host>2</pba-per-host>
                <pba-timeout>0</pba-timeout>
                <pba-last-blk-timeout>0</pba-last-blk-timeout>
                <pba-blk-total>40</pba-blk-total>
                <pba-blk-used>3</pba-blk-used>
                <pba-blk-table-entry>
                    <blk-internal-ip>121.11.10.2</blk-internal-ip>
                    <blk-reflexive-ip>121.11.15.11</blk-reflexive-ip>
                    <blk-low-port>1216</blk-low-port>
                    <blk-high-port>1279</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>64</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                    <blk-status>Query</blk-status>
                    <blk-left-time>-</blk-left-time>
                </pba-blk-table-entry>
            </pba-pool-info-entry>
        </pba-blk-table>
        """

        self.response["HE_HA_PORT_BLOCK_INFO"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <pba-blk-table xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
                <pba-pool-info-entry>
                    <pba-pool-name>A_POOL</pba-pool-name>
                    <pba-olfactor>1</pba-olfactor>
                    <pba-size>64</pba-size>
                    <pba-per-host>2</pba-per-host>
                    <pba-timeout>0</pba-timeout>
                    <pba-last-blk-timeout>0</pba-last-blk-timeout>
                    <pba-blk-total>40</pba-blk-total>
                    <pba-blk-used>3</pba-blk-used>
                    <pba-blk-table-entry>
                        <blk-internal-ip>121.11.10.2</blk-internal-ip>
                        <blk-reflexive-ip>121.11.15.11</blk-reflexive-ip>
                        <blk-low-port>1216</blk-low-port>
                        <blk-high-port>1279</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>64</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                        <blk-status>Query</blk-status>
                        <blk-left-time>-</blk-left-time>
                    </pba-blk-table-entry>
                    <pba-blk-table-entry>
                        <blk-internal-ip>121.11.10.3</blk-internal-ip>
                        <blk-reflexive-ip>121.11.15.12</blk-reflexive-ip>
                        <blk-low-port>1216</blk-low-port>
                        <blk-high-port>1279</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>64</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                        <blk-status>Query</blk-status>
                        <blk-left-time>-</blk-left-time>
                    </pba-blk-table-entry>
                    <pba-blk-table-entry>
                        <blk-internal-ip>121.11.10.4</blk-internal-ip>
                        <blk-reflexive-ip>121.11.15.13</blk-reflexive-ip>
                        <blk-low-port>1152</blk-low-port>
                        <blk-high-port>1215</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>64</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                        <blk-status>Query</blk-status>
                        <blk-left-time>-</blk-left-time>
                    </pba-blk-table-entry>
                </pba-pool-info-entry>
                <pba-pool-info-entry>
                    <pba-pool-name>B_POOL</pba-pool-name>
                    <pba-olfactor>1</pba-olfactor>
                    <pba-size>64</pba-size>
                    <pba-per-host>2</pba-per-host>
                    <pba-timeout>0</pba-timeout>
                    <pba-last-blk-timeout>0</pba-last-blk-timeout>
                    <pba-blk-total>40</pba-blk-total>
                    <pba-blk-used>0</pba-blk-used>
                </pba-pool-info-entry>
            </pba-blk-table>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <pba-blk-table xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
                <pba-pool-info-entry>
                    <pba-pool-name>A_POOL</pba-pool-name>
                    <pba-olfactor>1</pba-olfactor>
                    <pba-size>64</pba-size>
                    <pba-per-host>2</pba-per-host>
                    <pba-timeout>0</pba-timeout>
                    <pba-last-blk-timeout>0</pba-last-blk-timeout>
                    <pba-blk-total>40</pba-blk-total>
                    <pba-blk-used>0</pba-blk-used>
                </pba-pool-info-entry>
                <pba-pool-info-entry>
                    <pba-pool-name>B_POOL</pba-pool-name>
                    <pba-olfactor>1</pba-olfactor>
                    <pba-size>64</pba-size>
                    <pba-per-host>2</pba-per-host>
                    <pba-timeout>0</pba-timeout>
                    <pba-last-blk-timeout>0</pba-last-blk-timeout>
                    <pba-blk-total>40</pba-blk-total>
                    <pba-blk-used>0</pba-blk-used>
                </pba-pool-info-entry>
            </pba-blk-table>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["PERSISTENT_NAT_TABLE_SUMMARY_NEG"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.3D0/junos">
            <persist-nat-table xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
            </persist-nat-table>
            <cli>
                <banner>{primary:node0}</banner>
            </cli>
        </rpc-reply>"""

        self.response["PERSISTENT_NAT_TABLE_SUMMARY"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <persist-nat-table xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
                <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
                    <persist-nat-spu-id> on FPC0 PIC1:</persist-nat-spu-id>
                    <persist-nat-binding-total>524288</persist-nat-binding-total>
                    <persist-nat-binding-in-use>100</persist-nat-binding-in-use>
                    <persist-nat-enode-total>4194304</persist-nat-enode-total>
                    <persist-nat-enode-in-use>300</persist-nat-enode-in-use>
                </persist-nat-table-statistic>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
                <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
                    <persist-nat-spu-id> on FPC0 PIC2:</persist-nat-spu-id>
                    <persist-nat-binding-total>524288</persist-nat-binding-total>
                    <persist-nat-binding-in-use>200</persist-nat-binding-in-use>
                    <persist-nat-enode-total>4194304</persist-nat-enode-total>
                    <persist-nat-enode-in-use>200</persist-nat-enode-in-use>
                </persist-nat-table-statistic>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
                <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
                    <persist-nat-spu-id> on FPC0 PIC3:</persist-nat-spu-id>
                    <persist-nat-binding-total>524288</persist-nat-binding-total>
                    <persist-nat-binding-in-use>100</persist-nat-binding-in-use>
                    <persist-nat-enode-total>4194304</persist-nat-enode-total>
                    <persist-nat-enode-in-use>100</persist-nat-enode-in-use>
                </persist-nat-table-statistic>
            </persist-nat-table>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["PERSISTENT_NAT_TABLE_SUMMARY_LE"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <persist-nat-table xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
                <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
                    <persist-nat-spu-id> on FPC0 PIC1:</persist-nat-spu-id>
                    <persist-nat-binding-total>524288</persist-nat-binding-total>
                    <persist-nat-binding-in-use>100</persist-nat-binding-in-use>
                    <persist-nat-enode-total>4194304</persist-nat-enode-total>
                    <persist-nat-enode-in-use>300</persist-nat-enode-in-use>
                </persist-nat-table-statistic>
            </persist-nat-table>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """

        self.response["PERSISTENT_NAT_TABLE_SUMMARY_HA"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.3D0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                            <persist-nat-spu-id> on FPC0 PIC1:</persist-nat-spu-id>
                            <persist-nat-binding-total>524288</persist-nat-binding-total>
                            <persist-nat-binding-in-use>10</persist-nat-binding-in-use>
                            <persist-nat-enode-total>4194304</persist-nat-enode-total>
                            <persist-nat-enode-in-use>10</persist-nat-enode-in-use>
                        </persist-nat-table-statistic>
                    </persist-nat-table>
                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                            <persist-nat-spu-id> on FPC0 PIC2:</persist-nat-spu-id>
                            <persist-nat-binding-total>524288</persist-nat-binding-total>
                            <persist-nat-binding-in-use>10</persist-nat-binding-in-use>
                            <persist-nat-enode-total>4194304</persist-nat-enode-total>
                            <persist-nat-enode-in-use>10</persist-nat-enode-in-use>
                        </persist-nat-table-statistic>
                    </persist-nat-table>
                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                            <persist-nat-spu-id> on FPC0 PIC3:</persist-nat-spu-id>
                            <persist-nat-binding-total>524288</persist-nat-binding-total>
                            <persist-nat-binding-in-use>10</persist-nat-binding-in-use>
                            <persist-nat-enode-total>4194304</persist-nat-enode-total>
                            <persist-nat-enode-in-use>10</persist-nat-enode-in-use>
                        </persist-nat-table-statistic>
                    </persist-nat-table>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                            <persist-nat-spu-id> on FPC0 PIC1:</persist-nat-spu-id>
                            <persist-nat-binding-total>524288</persist-nat-binding-total>
                            <persist-nat-binding-in-use>10</persist-nat-binding-in-use>
                            <persist-nat-enode-total>4194304</persist-nat-enode-total>
                            <persist-nat-enode-in-use>10</persist-nat-enode-in-use>
                        </persist-nat-table-statistic>
                    </persist-nat-table>
                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                            <persist-nat-spu-id> on FPC0 PIC2:</persist-nat-spu-id>
                            <persist-nat-binding-total>524288</persist-nat-binding-total>
                            <persist-nat-binding-in-use>10</persist-nat-binding-in-use>
                            <persist-nat-enode-total>4194304</persist-nat-enode-total>
                            <persist-nat-enode-in-use>10</persist-nat-enode-in-use>
                        </persist-nat-table-statistic>
                    </persist-nat-table>
                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                            <persist-nat-spu-id> on FPC0 PIC3:</persist-nat-spu-id>
                            <persist-nat-binding-total>524288</persist-nat-binding-total>
                            <persist-nat-binding-in-use>10</persist-nat-binding-in-use>
                            <persist-nat-enode-total>4194304</persist-nat-enode-total>
                            <persist-nat-enode-in-use>10</persist-nat-enode-in-use>
                        </persist-nat-table-statistic>
                    </persist-nat-table>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{primary:node0}</banner>
            </cli>
        </rpc-reply>"""

        self.response["PERSISTENT_NAT_TABLE_SUMMARY_HA_ONE_NODE"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.3D0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-table-statistic xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                            <persist-nat-spu-id> on FPC0 PIC1:</persist-nat-spu-id>
                            <persist-nat-binding-total>524288</persist-nat-binding-total>
                            <persist-nat-binding-in-use>10</persist-nat-binding-in-use>
                            <persist-nat-enode-total>4194304</persist-nat-enode-total>
                            <persist-nat-enode-in-use>10</persist-nat-enode-in-use>
                        </persist-nat-table-statistic>
                    </persist-nat-table>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{primary:node0}</banner>
            </cli>
        </rpc-reply>"""

        self.response["SA_LE_SNAT_DETERMINISTIC"] = """
        <determ-blk-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
            <determ-pool-info-entry>
                <determ-pool-name>A_POOL</determ-pool-name>
                <determ-olfactor>1</determ-olfactor>
                <determ-blk-size>128</determ-blk-size>
                <determ-blk-total>129024</determ-blk-total>
                <determ-blk-used>0</determ-blk-used>
            </determ-pool-info-entry>
            <determ-blk-table-entry>
                <blk-internal-ip>192.168.150.0</blk-internal-ip>
                <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                <blk-low-port>1024</blk-low-port>
                <blk-high-port>1151</blk-high-port>
                <blk-ports-used>0</blk-ports-used>
                <blk-ports-total>128</blk-ports-total>
                <blk-ports-ol>1</blk-ports-ol>
            </determ-blk-table-entry>
            <determ-blk-table-entry>
                <blk-internal-ip>192.168.150.1</blk-internal-ip>
                <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                <blk-low-port>1152</blk-low-port>
                <blk-high-port>1279</blk-high-port>
                <blk-ports-used>0</blk-ports-used>
                <blk-ports-total>128</blk-ports-total>
                <blk-ports-ol>1</blk-ports-ol>
            </determ-blk-table-entry>
            <determ-blk-table-entry>
                <blk-internal-ip>192.168.150.2</blk-internal-ip>
                <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                <blk-low-port>1280</blk-low-port>
                <blk-high-port>1407</blk-high-port>
                <blk-ports-used>0</blk-ports-used>
                <blk-ports-total>128</blk-ports-total>
                <blk-ports-ol>1</blk-ports-ol>
            </determ-blk-table-entry>
            <determ-blk-table-entry>
                <blk-internal-ip>192.168.150.3</blk-internal-ip>
                <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                <blk-low-port>1408</blk-low-port>
                <blk-high-port>1535</blk-high-port>
                <blk-ports-used>0</blk-ports-used>
                <blk-ports-total>128</blk-ports-total>
                <blk-ports-ol>1</blk-ports-ol>
            </determ-blk-table-entry>
        </determ-blk-table>
        """

        self.response["SA_LE_SNAT_DETERMINISTIC_ONE"] = """
        <determ-blk-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
            <determ-pool-info-entry>
                <determ-pool-name>A_POOL</determ-pool-name>
                <determ-olfactor>1</determ-olfactor>
                <determ-blk-size>128</determ-blk-size>
                <determ-blk-total>129024</determ-blk-total>
                <determ-blk-used>0</determ-blk-used>
            </determ-pool-info-entry>
            <determ-blk-table-entry>
                <blk-internal-ip>192.168.150.0</blk-internal-ip>
                <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                <blk-low-port>1024</blk-low-port>
                <blk-high-port>1151</blk-high-port>
                <blk-ports-used>0</blk-ports-used>
                <blk-ports-total>128</blk-ports-total>
                <blk-ports-ol>1</blk-ports-ol>
            </determ-blk-table-entry>
        </determ-blk-table>
        """

        self.response["HA_LE_SNAT_DETERMINSTIC"] = """
        <multi-routing-engine-results>

            <multi-routing-engine-item>

                <re-name>node0</re-name>

                <determ-blk-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                    <determ-pool-info-entry>
                        <determ-pool-name>A_POOL</determ-pool-name>
                        <determ-olfactor>1</determ-olfactor>
                        <determ-blk-size>128</determ-blk-size>
                        <determ-blk-total>129024</determ-blk-total>
                        <determ-blk-used>0</determ-blk-used>
                    </determ-pool-info-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.0</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1024</blk-low-port>
                        <blk-high-port>1151</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.1</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1152</blk-low-port>
                        <blk-high-port>1279</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.2</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1280</blk-low-port>
                        <blk-high-port>1407</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.3</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1408</blk-low-port>
                        <blk-high-port>1535</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                </determ-blk-table>
            </multi-routing-engine-item>

            <multi-routing-engine-item>

                <re-name>node1</re-name>

                <determ-blk-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                    <determ-pool-info-entry>
                        <determ-pool-name>A_POOL</determ-pool-name>
                        <determ-olfactor>1</determ-olfactor>
                        <determ-blk-size>128</determ-blk-size>
                        <determ-blk-total>129024</determ-blk-total>
                        <determ-blk-used>0</determ-blk-used>
                    </determ-pool-info-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.0</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1024</blk-low-port>
                        <blk-high-port>1151</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.1</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1152</blk-low-port>
                        <blk-high-port>1279</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.2</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1280</blk-low-port>
                        <blk-high-port>1407</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.3</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1408</blk-low-port>
                        <blk-high-port>1535</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                </determ-blk-table>
            </multi-routing-engine-item>

        </multi-routing-engine-results>
        """

        self.response["SA_LE_SNAT_DETERMINSTIC"] = """
        <determ-blk-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
            <determ-pool-info-entry>
                <determ-pool-name>A_POOL</determ-pool-name>
                <determ-olfactor>1</determ-olfactor>
                <determ-blk-size>8</determ-blk-size>
                <determ-blk-total>48384</determ-blk-total>
                <determ-blk-used>0</determ-blk-used>
            </determ-pool-info-entry>
            <determ-blk-table-entry>
                <blk-internal-ip>192.168.10.0</blk-internal-ip>
                <blk-reflexive-ip>192.168.15.10</blk-reflexive-ip>
                <blk-low-port>1024</blk-low-port>
                <blk-high-port>1031</blk-high-port>
                <blk-ports-used>0</blk-ports-used>
                <blk-ports-total>8</blk-ports-total>
                <blk-ports-ol>1</blk-ports-ol>
            </determ-blk-table-entry>
        </determ-blk-table>
        """

        self.response["SA_LE_SNAT_DETERMINSTIC_INVALIDE"] = """
        <determ-blk xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
            <determ-pool-info-entry>
                <determ-pool-name>A_POOL</determ-pool-name>
                <determ-olfactor>1</determ-olfactor>
                <determ-blk-size>8</determ-blk-size>
                <determ-blk-total>48384</determ-blk-total>
                <determ-blk-used>0</determ-blk-used>
            </determ-pool-info-entry>
            <determ-blk-table-entry>
                <blk-internal-ip>192.168.10.0</blk-internal-ip>
                <blk-reflexive-ip>192.168.15.10</blk-reflexive-ip>
                <blk-low-port>1024</blk-low-port>
                <blk-high-port>1031</blk-high-port>
                <blk-ports-used>0</blk-ports-used>
                <blk-ports-total>8</blk-ports-total>
                <blk-ports-ol>1</blk-ports-ol>
            </determ-blk-table-entry>
        </determ-blk>
        """

        self.response["HA_LE_SNAT_DETERMINISTIC_ONE"] = """
        <multi-routing-engine-results>

            <multi-routing-engine-item>

                <re-name>node0</re-name>

                <determ-blk-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                    <determ-pool-info-entry>
                        <determ-pool-name>A_POOL</determ-pool-name>
                        <determ-olfactor>1</determ-olfactor>
                        <determ-blk-size>128</determ-blk-size>
                        <determ-blk-total>129024</determ-blk-total>
                        <determ-blk-used>0</determ-blk-used>
                    </determ-pool-info-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.0</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1024</blk-low-port>
                        <blk-high-port>1151</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                </determ-blk-table>
            </multi-routing-engine-item>

            <multi-routing-engine-item>

                <re-name>node1</re-name>

                <determ-blk-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                    <determ-pool-info-entry>
                        <determ-pool-name>A_POOL</determ-pool-name>
                        <determ-olfactor>1</determ-olfactor>
                        <determ-blk-size>128</determ-blk-size>
                        <determ-blk-total>129024</determ-blk-total>
                        <determ-blk-used>0</determ-blk-used>
                    </determ-pool-info-entry>
                    <determ-blk-table-entry>
                        <blk-internal-ip>192.168.150.0</blk-internal-ip>
                        <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                        <blk-low-port>1024</blk-low-port>
                        <blk-high-port>1151</blk-high-port>
                        <blk-ports-used>0</blk-ports-used>
                        <blk-ports-total>128</blk-ports-total>
                        <blk-ports-ol>1</blk-ports-ol>
                    </determ-blk-table-entry>
                </determ-blk-table>
            </multi-routing-engine-item>

        </multi-routing-engine-results>
        """

        self.response["HA_HE_SNAT_DETERMINISTIC"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <determ-blk-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                <determ-pool-info-entry>
                    <determ-pool-name>A_POOL</determ-pool-name>
                    <determ-olfactor>1</determ-olfactor>
                    <determ-blk-size>128</determ-blk-size>
                    <determ-blk-total>129024</determ-blk-total>
                    <determ-blk-used>0</determ-blk-used>
                </determ-pool-info-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.150.0</blk-internal-ip>
                    <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                    <blk-low-port>1024</blk-low-port>
                    <blk-high-port>1151</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.150.1</blk-internal-ip>
                    <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                    <blk-low-port>1152</blk-low-port>
                    <blk-high-port>1279</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.150.2</blk-internal-ip>
                    <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                    <blk-low-port>1280</blk-low-port>
                    <blk-high-port>1407</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.150.3</blk-internal-ip>
                    <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                    <blk-low-port>1408</blk-low-port>
                    <blk-high-port>1535</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-pool-info-entry>
                    <determ-pool-name>B_POOL</determ-pool-name>
                    <determ-olfactor>1</determ-olfactor>
                    <determ-blk-size>128</determ-blk-size>
                    <determ-blk-total>129024</determ-blk-total>
                    <determ-blk-used>0</determ-blk-used>
                </determ-pool-info-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.160.0</blk-internal-ip>
                    <blk-reflexive-ip>192.168.160.0</blk-reflexive-ip>
                    <blk-low-port>1024</blk-low-port>
                    <blk-high-port>1151</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.160.1</blk-internal-ip>
                    <blk-reflexive-ip>192.168.160.0</blk-reflexive-ip>
                    <blk-low-port>1152</blk-low-port>
                    <blk-high-port>1279</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.160.2</blk-internal-ip>
                    <blk-reflexive-ip>192.168.160.0</blk-reflexive-ip>
                    <blk-low-port>1280</blk-low-port>
                    <blk-high-port>1407</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.160.3</blk-internal-ip>
                    <blk-reflexive-ip>192.168.160.0</blk-reflexive-ip>
                    <blk-low-port>1408</blk-low-port>
                    <blk-high-port>1535</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
            </determ-blk-table>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <determ-blk-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                <determ-pool-info-entry>
                    <determ-pool-name>A_POOL</determ-pool-name>
                    <determ-olfactor>1</determ-olfactor>
                    <determ-blk-size>128</determ-blk-size>
                    <determ-blk-total>129024</determ-blk-total>
                    <determ-blk-used>0</determ-blk-used>
                </determ-pool-info-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.150.0</blk-internal-ip>
                    <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                    <blk-low-port>1024</blk-low-port>
                    <blk-high-port>1151</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.150.1</blk-internal-ip>
                    <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                    <blk-low-port>1152</blk-low-port>
                    <blk-high-port>1279</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.150.2</blk-internal-ip>
                    <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                    <blk-low-port>1280</blk-low-port>
                    <blk-high-port>1407</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.150.3</blk-internal-ip>
                    <blk-reflexive-ip>192.168.150.0</blk-reflexive-ip>
                    <blk-low-port>1408</blk-low-port>
                    <blk-high-port>1535</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-pool-info-entry>
                    <determ-pool-name>B_POOL</determ-pool-name>
                    <determ-olfactor>1</determ-olfactor>
                    <determ-blk-size>128</determ-blk-size>
                    <determ-blk-total>129024</determ-blk-total>
                    <determ-blk-used>0</determ-blk-used>
                </determ-pool-info-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.160.0</blk-internal-ip>
                    <blk-reflexive-ip>192.168.160.0</blk-reflexive-ip>
                    <blk-low-port>1024</blk-low-port>
                    <blk-high-port>1151</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.160.1</blk-internal-ip>
                    <blk-reflexive-ip>192.168.160.0</blk-reflexive-ip>
                    <blk-low-port>1152</blk-low-port>
                    <blk-high-port>1279</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.160.2</blk-internal-ip>
                    <blk-reflexive-ip>192.168.160.0</blk-reflexive-ip>
                    <blk-low-port>1280</blk-low-port>
                    <blk-high-port>1407</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
                <determ-blk-table-entry>
                    <blk-internal-ip>192.168.160.3</blk-internal-ip>
                    <blk-reflexive-ip>192.168.160.0</blk-reflexive-ip>
                    <blk-low-port>1408</blk-low-port>
                    <blk-high-port>1535</blk-high-port>
                    <blk-ports-used>0</blk-ports-used>
                    <blk-ports-total>128</blk-ports-total>
                    <blk-ports-ol>1</blk-ports-ol>
                </determ-blk-table-entry>
            </determ-blk-table>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["SA_LE_INTERFACE_NAT_PORTS"] = """
    <interface-nat-ports-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
        <interface-nat-ports-entry>
            <pool-index>0</pool-index>
            <total-ports>64510</total-ports>
            <single-ports-allocated>1</single-ports-allocated>
            <single-ports-available>63486</single-ports-available>
            <twin-ports-allocated>0</twin-ports-allocated>
            <twin-ports-available>1024</twin-ports-available>
        </interface-nat-ports-entry>
        <interface-nat-ports-entry>
            <pool-index>1</pool-index>
            <total-ports>64520</total-ports>
            <single-ports-allocated>0</single-ports-allocated>
            <single-ports-available>63486</single-ports-available>
            <twin-ports-allocated>2</twin-ports-allocated>
            <twin-ports-available>1024</twin-ports-available>
        </interface-nat-ports-entry>
        <interface-nat-ports-entry>
            <pool-index>2</pool-index>
            <total-ports>64530</total-ports>
            <single-ports-allocated>0</single-ports-allocated>
            <single-ports-available>63486</single-ports-available>
            <twin-ports-allocated>6</twin-ports-allocated>
            <twin-ports-available>1024</twin-ports-available>
        </interface-nat-ports-entry>
    </interface-nat-ports-information>
        """

        self.response["HA_LE_INTERFACE_NAT_PORTS"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <interface-nat-ports-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <interface-nat-ports-entry>
                    <pool-index>0</pool-index>
                    <total-ports>64510</total-ports>
                    <single-ports-allocated>0</single-ports-allocated>
                    <single-ports-available>63486</single-ports-available>
                    <twin-ports-allocated>0</twin-ports-allocated>
                    <twin-ports-available>1024</twin-ports-available>
                </interface-nat-ports-entry>
                <interface-nat-ports-entry>
                    <pool-index>1</pool-index>
                    <total-ports>64510</total-ports>
                    <single-ports-allocated>0</single-ports-allocated>
                    <single-ports-available>63486</single-ports-available>
                    <twin-ports-allocated>0</twin-ports-allocated>
                    <twin-ports-available>1024</twin-ports-available>
                </interface-nat-ports-entry>
                <interface-nat-ports-entry>
                    <pool-index>2</pool-index>
                    <total-ports>64510</total-ports>
                    <single-ports-allocated>0</single-ports-allocated>
                    <single-ports-available>63486</single-ports-available>
                    <twin-ports-allocated>0</twin-ports-allocated>
                    <twin-ports-available>1024</twin-ports-available>
                </interface-nat-ports-entry>
            </interface-nat-ports-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <interface-nat-ports-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <interface-nat-ports-entry>
                    <pool-index>0</pool-index>
                    <total-ports>64510</total-ports>
                    <single-ports-allocated>0</single-ports-allocated>
                    <single-ports-available>63486</single-ports-available>
                    <twin-ports-allocated>0</twin-ports-allocated>
                    <twin-ports-available>1024</twin-ports-available>
                </interface-nat-ports-entry>
                <interface-nat-ports-entry>
                    <pool-index>1</pool-index>
                    <total-ports>64510</total-ports>
                    <single-ports-allocated>0</single-ports-allocated>
                    <single-ports-available>63486</single-ports-available>
                    <twin-ports-allocated>0</twin-ports-allocated>
                    <twin-ports-available>1024</twin-ports-available>
                </interface-nat-ports-entry>
                <interface-nat-ports-entry>
                    <pool-index>2</pool-index>
                    <total-ports>64510</total-ports>
                    <single-ports-allocated>0</single-ports-allocated>
                    <single-ports-available>63486</single-ports-available>
                    <twin-ports-allocated>0</twin-ports-allocated>
                    <twin-ports-available>1024</twin-ports-available>
                </interface-nat-ports-entry>
            </interface-nat-ports-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_LE_INTERFACE_NAT_PORTS_1_ENTRY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <interface-nat-ports-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <interface-nat-ports-entry>
                    <pool-index>0</pool-index>
                    <total-ports>64510</total-ports>
                    <single-ports-allocated>0</single-ports-allocated>
                    <single-ports-available>63486</single-ports-available>
                    <twin-ports-allocated>0</twin-ports-allocated>
                    <twin-ports-available>1024</twin-ports-available>
                </interface-nat-ports-entry>
            </interface-nat-ports-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <interface-nat-ports-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <interface-nat-ports-entry>
                    <pool-index>0</pool-index>
                    <total-ports>64510</total-ports>
                    <single-ports-allocated>0</single-ports-allocated>
                    <single-ports-available>63486</single-ports-available>
                    <twin-ports-allocated>0</twin-ports-allocated>
                    <twin-ports-available>1024</twin-ports-available>
                </interface-nat-ports-entry>
            </interface-nat-ports-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """


        self.response["HA_LE_INTERFACE_NAT_PORTS_FOR_SPECIFIC_NODE"] = """
        <multi-routing-engine-results>

            <multi-routing-engine-item>

                <re-name>node0</re-name>

                <interface-nat-ports-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                    <interface-nat-ports-entry>
                        <pool-index>0</pool-index>
                        <total-ports>64510</total-ports>
                        <single-ports-allocated>0</single-ports-allocated>
                        <single-ports-available>63486</single-ports-available>
                        <twin-ports-allocated>0</twin-ports-allocated>
                        <twin-ports-available>1024</twin-ports-available>
                    </interface-nat-ports-entry>
                    <interface-nat-ports-entry>
                        <pool-index>1</pool-index>
                        <total-ports>64510</total-ports>
                        <single-ports-allocated>0</single-ports-allocated>
                        <single-ports-available>63486</single-ports-available>
                        <twin-ports-allocated>0</twin-ports-allocated>
                        <twin-ports-available>1024</twin-ports-available>
                    </interface-nat-ports-entry>
                    <interface-nat-ports-entry>
                        <pool-index>2</pool-index>
                        <total-ports>64510</total-ports>
                        <single-ports-allocated>0</single-ports-allocated>
                        <single-ports-available>63486</single-ports-available>
                        <twin-ports-allocated>0</twin-ports-allocated>
                        <twin-ports-available>1024</twin-ports-available>
                    </interface-nat-ports-entry>
                </interface-nat-ports-information>
            </multi-routing-engine-item>

        </multi-routing-engine-results>
            """

        self.response["HA_LE_INTERFACE_NAT_PORTS_INVALID_RESPONSE"] = """
        <multi-routing-engine-results>

            <multi-routing-engine-item>

                <re-name>node0</re-name>

                <nat-ports-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                    <interface-nat-ports-entry>
                        <pool-index>0</pool-index>
                        <total-ports>64510</total-ports>
                        <single-ports-allocated>0</single-ports-allocated>
                        <single-ports-available>63486</single-ports-available>
                        <twin-ports-allocated>0</twin-ports-allocated>
                        <twin-ports-available>1024</twin-ports-available>
                    </interface-nat-ports-entry>
                    <interface-nat-ports-entry>
                        <pool-index>1</pool-index>
                        <total-ports>64510</total-ports>
                        <single-ports-allocated>0</single-ports-allocated>
                        <single-ports-available>63486</single-ports-available>
                        <twin-ports-allocated>0</twin-ports-allocated>
                        <twin-ports-available>1024</twin-ports-available>
                    </interface-nat-ports-entry>
                    <interface-nat-ports-entry>
                        <pool-index>2</pool-index>
                        <total-ports>64510</total-ports>
                        <single-ports-allocated>0</single-ports-allocated>
                        <single-ports-available>63486</single-ports-available>
                        <twin-ports-allocated>0</twin-ports-allocated>
                        <twin-ports-available>1024</twin-ports-available>
                    </interface-nat-ports-entry>
                </nat-ports-information>
            </multi-routing-engine-item>

        </multi-routing-engine-results>
            """

        self.response["SA_LE_INTERFACE_NAT_PORTS_WITH_UNKOWN_ELEMENT"] = """
    <interface-nat-ports-information xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
        <interface-nat-ports-entry>
            <pool-index>0</pool-index>
            <total-ports>64510</total-ports>
            <single-ports-allocated>0</single-ports-allocated>
            <single-ports-available>63486</single-ports-available>
            <twin-ports-allocated>0</twin-ports-allocated>
            <twin-ports-available>1024</twin-ports-available>
            <new-unknown-element>0</new-unknown-element>
        </interface-nat-ports-entry>
        <interface-nat-ports-entry>
            <pool-index>1</pool-index>
            <total-ports>64510</total-ports>
            <single-ports-allocated>0</single-ports-allocated>
            <single-ports-available>63486</single-ports-available>
            <twin-ports-allocated>0</twin-ports-allocated>
            <twin-ports-available>1024</twin-ports-available>
            <new-unknown-element>0</new-unknown-element>
        </interface-nat-ports-entry>
        <interface-nat-ports-entry>
            <pool-index>2</pool-index>
            <total-ports>64510</total-ports>
            <single-ports-allocated>0</single-ports-allocated>
            <single-ports-available>63486</single-ports-available>
            <twin-ports-allocated>0</twin-ports-allocated>
            <twin-ports-available>1024</twin-ports-available>
            <new-unknown-element>0</new-unknown-element>
        </interface-nat-ports-entry>
    </interface-nat-ports-information>
        """

        self.response["HA_HE_SNAT_RESOURCE_USAGE"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <source-resource-usage-pool-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
                <resource-usage-entry junos:style="all-pat-pool">
                    <resource-usage-pool-name>A_POOL</resource-usage-pool-name>
                    <resource-usage-total-pool-num>33554432</resource-usage-total-pool-num>
                    <resource-usage-port-ol-factor>1</resource-usage-port-ol-factor>
                    <resource-usage-peak-usage>0%</resource-usage-peak-usage>
                    <resource-usage-peak-date-time junos:seconds="0">1970-01-01 08:00:00 CST</resource-usage-peak-date-time>
                    <resource-usage-total-address>10</resource-usage-total-address>
                    <resource-usage-total-used>0</resource-usage-total-used>
                    <resource-usage-total-avail>1280</resource-usage-total-avail>
                    <resource-usage-total-total>1280</resource-usage-total-total>
                    <resource-usage-total-usage>0%</resource-usage-total-usage>
                </resource-usage-entry>
                <resource-usage-entry junos:style="all-pat-pool">
                    <resource-usage-pool-name>B_POOL</resource-usage-pool-name>
                    <resource-usage-total-pool-num>33554432</resource-usage-total-pool-num>
                    <resource-usage-port-ol-factor>1</resource-usage-port-ol-factor>
                    <resource-usage-peak-usage>0%</resource-usage-peak-usage>
                    <resource-usage-peak-date-time junos:seconds="0">1970-01-01 08:00:00 CST</resource-usage-peak-date-time>
                    <resource-usage-total-address>10</resource-usage-total-address>
                    <resource-usage-total-used>0</resource-usage-total-used>
                    <resource-usage-total-avail>1280</resource-usage-total-avail>
                    <resource-usage-total-total>1280</resource-usage-total-total>
                    <resource-usage-total-usage>0%</resource-usage-total-usage>
                </resource-usage-entry>
            </source-resource-usage-pool-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <source-resource-usage-pool-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
                <resource-usage-entry junos:style="all-pat-pool">
                    <resource-usage-pool-name>A_POOL</resource-usage-pool-name>
                    <resource-usage-total-pool-num>33554432</resource-usage-total-pool-num>
                    <resource-usage-port-ol-factor>1</resource-usage-port-ol-factor>
                    <resource-usage-peak-usage>0%</resource-usage-peak-usage>
                    <resource-usage-peak-date-time junos:seconds="0">1970-01-01 08:00:00 CST</resource-usage-peak-date-time>
                    <resource-usage-total-address>10</resource-usage-total-address>
                    <resource-usage-total-used>0</resource-usage-total-used>
                    <resource-usage-total-avail>1280</resource-usage-total-avail>
                    <resource-usage-total-total>1280</resource-usage-total-total>
                    <resource-usage-total-usage>0%</resource-usage-total-usage>
                </resource-usage-entry>
                <resource-usage-entry junos:style="all-pat-pool">
                    <resource-usage-pool-name>B_POOL</resource-usage-pool-name>
                    <resource-usage-total-pool-num>33554432</resource-usage-total-pool-num>
                    <resource-usage-port-ol-factor>1</resource-usage-port-ol-factor>
                    <resource-usage-peak-usage>0%</resource-usage-peak-usage>
                    <resource-usage-peak-date-time junos:seconds="0">1970-01-01 08:00:00 CST</resource-usage-peak-date-time>
                    <resource-usage-total-address>10</resource-usage-total-address>
                    <resource-usage-total-used>0</resource-usage-total-used>
                    <resource-usage-total-avail>1280</resource-usage-total-avail>
                    <resource-usage-total-total>1280</resource-usage-total-total>
                    <resource-usage-total-usage>0%</resource-usage-total-usage>
                </resource-usage-entry>
            </source-resource-usage-pool-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["SA_HE_SNAT_RESOURCE_USAGE"] = """
            <source-resource-usage-pool-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
                <resource-usage-entry junos:style="all-pat-pool">
                    <resource-usage-pool-name>A_POOL</resource-usage-pool-name>
                    <resource-usage-total-pool-num>33554432</resource-usage-total-pool-num>
                    <resource-usage-port-ol-factor>1</resource-usage-port-ol-factor>
                    <resource-usage-peak-usage>0%</resource-usage-peak-usage>
                    <resource-usage-peak-date-time junos:seconds="0">1970-01-01 08:00:00 CST</resource-usage-peak-date-time>
                    <resource-usage-total-address>10</resource-usage-total-address>
                    <resource-usage-total-used>0</resource-usage-total-used>
                    <resource-usage-total-avail>1280</resource-usage-total-avail>
                    <resource-usage-total-total>1280</resource-usage-total-total>
                    <resource-usage-total-usage>0%</resource-usage-total-usage>
                </resource-usage-entry>
                <resource-usage-entry junos:style="all-pat-pool">
                    <resource-usage-pool-name>B_POOL</resource-usage-pool-name>
                    <resource-usage-total-pool-num>33554432</resource-usage-total-pool-num>
                    <resource-usage-port-ol-factor>1</resource-usage-port-ol-factor>
                    <resource-usage-peak-usage>0%</resource-usage-peak-usage>
                    <resource-usage-peak-date-time junos:seconds="0">1970-01-01 08:00:00 CST</resource-usage-peak-date-time>
                    <resource-usage-total-address>10</resource-usage-total-address>
                    <resource-usage-total-used>0</resource-usage-total-used>
                    <resource-usage-total-avail>1280</resource-usage-total-avail>
                    <resource-usage-total-total>1280</resource-usage-total-total>
                    <resource-usage-total-usage>0%</resource-usage-total-usage>
                </resource-usage-entry>
            </source-resource-usage-pool-information>
        """

        self.response["SA_HE_SNAT_RESOURCE_USAGE_WITH_ONE_POOL"] = """
            <source-resource-usage-pool-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
                <resource-usage-entry junos:style="all-pat-pool">
                    <resource-usage-pool-name>A_POOL</resource-usage-pool-name>
                    <resource-usage-total-pool-num>33554432</resource-usage-total-pool-num>
                    <resource-usage-port-ol-factor>1</resource-usage-port-ol-factor>
                    <resource-usage-peak-usage>0%</resource-usage-peak-usage>
                    <resource-usage-peak-date-time junos:seconds="0">1970-01-01 08:00:00 CST</resource-usage-peak-date-time>
                    <resource-usage-total-address>10</resource-usage-total-address>
                    <resource-usage-total-used>0</resource-usage-total-used>
                    <resource-usage-total-avail>1280</resource-usage-total-avail>
                    <resource-usage-total-total>1280</resource-usage-total-total>
                    <resource-usage-total-usage>0%</resource-usage-total-usage>
                </resource-usage-entry>
            </source-resource-usage-pool-information>
        """

        self.response["SA_HE_SNAT_RESOURCE_USAGE_INVALID"] = """
            <invalid-source-resource-usage-pool-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
                <resource-usage-entry junos:style="all-pat-pool">
                    <resource-usage-pool-name>A_POOL</resource-usage-pool-name>
                    <resource-usage-total-pool-num>33554432</resource-usage-total-pool-num>
                    <resource-usage-port-ol-factor>1</resource-usage-port-ol-factor>
                    <resource-usage-peak-usage>0%</resource-usage-peak-usage>
                    <resource-usage-peak-date-time junos:seconds="0">1970-01-01 08:00:00 CST</resource-usage-peak-date-time>
                    <resource-usage-total-address>10</resource-usage-total-address>
                    <resource-usage-total-used>0</resource-usage-total-used>
                    <resource-usage-total-avail>1280</resource-usage-total-avail>
                    <resource-usage-total-total>1280</resource-usage-total-total>
                    <resource-usage-total-usage>0%</resource-usage-total-usage>
                </resource-usage-entry>
            </invalid-source-resource-usage-pool-information>
        """

        self.response["HA_HE_SNAT_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <ssg-source-nat-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
                <ssg-total-source-pat-port-num>
                    <total-source-summary-pat-port-num>5120</total-source-summary-pat-port-num>
                </ssg-total-source-pat-port-num>
                <ssg-max-source-pat-port-num>
                    <max-source-pat-port-num>2576980378</max-source-pat-port-num>
                </ssg-max-source-pat-port-num>
                <ssg-total-source-pool-num>
                    <total-source-summary-pools>2</total-source-summary-pools>
                </ssg-total-source-pool-num>
                <ssg-source-pool-entry>
                    <ssg-source-pool-name>A_POOL</ssg-source-pool-name>
                    <ssg-source-pool-address-range>121.11.15.11-121.11.15.20</ssg-source-pool-address-range>
                    <ssg-source-pool-routing-instance>default</ssg-source-pool-routing-instance>
                    <ssg-source-pool-pat>yes</ssg-source-pool-pat>
                    <ssg-source-pool-total-address>10</ssg-source-pool-total-address>
                </ssg-source-pool-entry>
                <ssg-source-pool-entry>
                    <ssg-source-pool-name>B_POOL</ssg-source-pool-name>
                    <ssg-source-pool-address-range>121.11.25.11-121.11.25.20</ssg-source-pool-address-range>
                    <ssg-source-pool-routing-instance>default</ssg-source-pool-routing-instance>
                    <ssg-source-pool-pat>yes</ssg-source-pool-pat>
                    <ssg-source-pool-total-address>10</ssg-source-pool-total-address>
                </ssg-source-pool-entry>
                <ssg-total-source-rule-num>
                    <summary-total-source-rules>1</summary-total-source-rules>
                </ssg-total-source-rule-num>
                <ssg-source-rule-entry>
                    <ssg-source-rule-name>sr</ssg-source-rule-name>
                    <ssg-source-rule-set-name>t2u_ruleset</ssg-source-rule-set-name>
                    <ssg-source-rule-action>A_POOL</ssg-source-rule-action>
                    <ssg-source-rule-context-from>trust</ssg-source-rule-context-from>
                    <ssg-source-rule-context-to>untrust</ssg-source-rule-context-to>
                </ssg-source-rule-entry>
            </ssg-source-nat-summary-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <ssg-source-nat-summary-information xmlns="http://xml.juniper.net/junos/15.1X49/junos-nat">
                <ssg-total-source-pat-port-num>
                    <total-source-summary-pat-port-num>5120</total-source-summary-pat-port-num>
                </ssg-total-source-pat-port-num>
                <ssg-max-source-pat-port-num>
                    <max-source-pat-port-num>2576980378</max-source-pat-port-num>
                </ssg-max-source-pat-port-num>
                <ssg-total-source-pool-num>
                    <total-source-summary-pools>2</total-source-summary-pools>
                </ssg-total-source-pool-num>
                <ssg-source-pool-entry>
                    <ssg-source-pool-name>A_POOL</ssg-source-pool-name>
                    <ssg-source-pool-address-range>121.11.15.11-121.11.15.20</ssg-source-pool-address-range>
                    <ssg-source-pool-routing-instance>default</ssg-source-pool-routing-instance>
                    <ssg-source-pool-pat>yes</ssg-source-pool-pat>
                    <ssg-source-pool-total-address>10</ssg-source-pool-total-address>
                </ssg-source-pool-entry>
                <ssg-source-pool-entry>
                    <ssg-source-pool-name>B_POOL</ssg-source-pool-name>
                    <ssg-source-pool-address-range>121.11.25.11-121.11.25.20</ssg-source-pool-address-range>
                    <ssg-source-pool-routing-instance>default</ssg-source-pool-routing-instance>
                    <ssg-source-pool-pat>yes</ssg-source-pool-pat>
                    <ssg-source-pool-total-address>10</ssg-source-pool-total-address>
                </ssg-source-pool-entry>
                <ssg-total-source-rule-num>
                    <summary-total-source-rules>1</summary-total-source-rules>
                </ssg-total-source-rule-num>
                <ssg-source-rule-entry>
                    <ssg-source-rule-name>sr</ssg-source-rule-name>
                    <ssg-source-rule-set-name>t2u_ruleset</ssg-source-rule-set-name>
                    <ssg-source-rule-action>A_POOL</ssg-source-rule-action>
                    <ssg-source-rule-context-from>trust</ssg-source-rule-context-from>
                    <ssg-source-rule-context-to>untrust</ssg-source-rule-context-to>
                </ssg-source-rule-entry>
            </ssg-source-nat-summary-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["SHOW_SPUID_POOL"] = """
================ fpc2.pic0 ================

SPUID: 8
"""
        self.response["SHOW_SPUID_POOL_NEG"] = """
================ fpc2.pic0 ================
"""

        self.response["SHOW_USP_SPU_CHASSIS"] = """
Num of active FPC: 12
Max number of PIC per FPC: 4
SPU selection algorithm: (SPU-capacity-based)

SPU      FPC     PIC     SPU_STATE               FLOW-FUNCTION
 00       0       0      PIC empty
 01       0       1      PIC empty
 02       0       2      PIC empty
 03       0       3      PIC empty
 08       2       0      cp PIC Up                 CP (Self)
 09       2       1      XLP flow PIC Up           SPU
 10       2       2      XLP flow PIC Up           SPU
 11       2       3      XLP flow PIC Up           SPU"""


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_source_nat_interface_nat_ports(self, mock_send_cli_cmd):
        """Test get source nat interface nat ports info"""
        mock_device_ins = mock.Mock()

        print("Get interface-nat-ports info from LE SA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_INTERFACE_NAT_PORTS"])
        response = self.ins.get_source_nat_interface_nat_ports(device=mock_device_ins, node=1)
        print(self.tool.pprint(response))
        self.assertTrue(len(response) == 3)
        self.assertTrue(response[0]["pool_index"] == '0')
        self.assertTrue(response[1]["pool_index"] == '1')
        self.assertTrue(response[2]["pool_index"] == '2')

        print("Get interface-nat-ports info from LE HA topo with all node response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_INTERFACE_NAT_PORTS"])
        response = self.ins.get_source_nat_interface_nat_ports(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertTrue(isinstance(response, list))
        self.assertTrue(len(response) == 6)
        self.assertTrue("re_name" in response[0] and "re_name" in response[1])

        print("Only 1 entry for interface-nat-ports from LE HA topo with all node response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_INTERFACE_NAT_PORTS_1_ENTRY"])
        response = self.ins.get_source_nat_interface_nat_ports(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertTrue(isinstance(response, list))
        self.assertTrue(len(response) == 2)
        self.assertTrue("re_name" in response[0] and "re_name" in response[1])

        print("Get interface-nat-ports info from LE HA topo with only 1 node response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_INTERFACE_NAT_PORTS_FOR_SPECIFIC_NODE"])
        response = self.ins.get_source_nat_interface_nat_ports(device=mock_device_ins, lsys_name="lsys1", more_options="more_options")
        print(self.tool.pprint(response))
        self.assertTrue(isinstance(response, list))
        self.assertTrue(response[0]["re_name"] == "node0")

        print("code coverage")
        response = self.ins.get_source_nat_interface_nat_ports(device=mock_device_ins, node="node0")
        print(self.tool.pprint(response))
        self.assertTrue(isinstance(response, list))
        self.assertTrue(response[0]["re_name"] == "node0")

        mock_send_cli_cmd.return_value = False
        response = self.ins.get_source_nat_interface_nat_ports(device=mock_device_ins)
        self.assertFalse(response)

        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_INTERFACE_NAT_PORTS_INVALID_RESPONSE"])
        response = self.ins.get_source_nat_interface_nat_ports(device=mock_device_ins)
        self.assertFalse(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_source_nat_interface_nat_ports(self, mock_send_cli_cmd):
        """Test get source nat interface nat ports info"""
        mock_device_ins = mock.Mock()

        print("search interface-nat-ports info from LE SA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_INTERFACE_NAT_PORTS"])
        status = self.ins.search_source_nat_interface_nat_ports(
            device=mock_device_ins,
            pool_index=2,
            single_ports_allocated=("0-100", "in"),
            single_ports_available="0 - 65535 in",
            twin_ports_available="1024",
        )
        self.assertTrue(status)

        print("search interface-nat-ports info from LE HA topo with all node response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_INTERFACE_NAT_PORTS"])
        response = self.ins.search_source_nat_interface_nat_ports(
            device=mock_device_ins,
            return_mode="counter",
            single_ports_allocated=0,
            re_name="node1",
        )
        self.assertTrue(response == 3)

        print("search 1 entry for interface-nat-ports from LE HA topo with all node response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_INTERFACE_NAT_PORTS_1_ENTRY"])
        response = self.ins.search_source_nat_interface_nat_ports(
            device=mock_device_ins,
            return_mode="counter",
        )
        self.assertTrue(response == 2)

        print("search interface-nat-ports info from LE HA topo with only 1 node response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_INTERFACE_NAT_PORTS_FOR_SPECIFIC_NODE"])
        response = self.ins.search_source_nat_interface_nat_ports(
            device=mock_device_ins,
            re_name="node0",
            return_mode="counter",
            single_ports_available=("0-65535", "in"),
        )
        self.assertTrue(response == 3)

        print("search with no entry matched")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_INTERFACE_NAT_PORTS"])
        response = self.ins.search_source_nat_interface_nat_ports(
            device=mock_device_ins,
            single_ports_available=("100", "eq"),
            single_ports_allocated=0,
        )
        self.assertFalse(response)

        print("invalid option")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_INTERFACE_NAT_PORTS"])
        response = self.ins.search_source_nat_interface_nat_ports(
            device=mock_device_ins,
            return_mode="unknown",
            single_ports_available=None,
            single_ports_allocated_for_unknown="Not a number",
        )
        self.assertFalse(response)

        print("get nat interface ports info failed")
        mock_send_cli_cmd.return_value = False
        self.assertFalse(self.ins.search_source_nat_interface_nat_ports(device=mock_device_ins))

        print("unknown keywords from device")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_INTERFACE_NAT_PORTS_WITH_UNKOWN_ELEMENT"])
        status = self.ins.search_source_nat_interface_nat_ports(device=mock_device_ins)
        self.assertTrue(status)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_source_nat_deterministic(self, mock_send_cli_cmd):
        """checking get source nat deterministic info"""
        mock_device_ins = mock.Mock()

        print("Get deterministic info from HA LE platform")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_LE_SNAT_DETERMINSTIC"])
        entry_list = self.ins.get_source_nat_deterministic(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(isinstance(entry_list, list))
        self.assertTrue(len(entry_list) == 8)

        print("Get deterministic info from HA LE platform with node option")
        mock_send_cli_cmd.return_value = False
        entry_list = self.ins.get_source_nat_deterministic(device=mock_device_ins, lsys_name="all", node="node0", more_options="source_address")
        self.assertFalse(entry_list)

        print("invalid xml structure")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_LE_SNAT_DETERMINSTIC_INVALIDE"])
        entry_list = self.ins.get_source_nat_deterministic(device=mock_device_ins, node=1, more_options="source_address")
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 0)

        print("Get deterministic info from SA LE platform and only 1 entry in a pool")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_LE_SNAT_DETERMINSTIC"])
        entry_list = self.ins.get_source_nat_deterministic(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 1)

        print("invalid option check")
        self.assertRaisesRegex(
            ValueError,
            r"",
            self.ins.get_source_nat_deterministic,
            device=mock_device_ins, node="want node0",
        )

        print("No enough xml element")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str="""
        <blk-table-entry>
                <blk-internal-ip>192.168.10.0</blk-internal-ip>
                <blk-reflexive-ip>192.168.15.10</blk-reflexive-ip>
                <blk-low-port>1024</blk-low-port>
                <blk-high-port>1031</blk-high-port>
                <blk-ports-used>0</blk-ports-used>
                <blk-ports-total>8</blk-ports-total>
                <blk-ports-ol>1</blk-ports-ol>
        </blk-table-entry>
        """)
        entry_list = self.ins.get_source_nat_deterministic(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 0)


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_source_nat_pool(self, mock_send_cli_cmd):
        """checking for get SNAT pool information"""
        mock_device_ins = mock.Mock()

        print("Get SNAT pool info from SA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_POOL_INFO"])
        all_pool_list = self.ins.get_source_nat_pool(device=mock_device_ins, pool_name="all", lsys_name="all", more_options="more_options")
        print(self.tool.pprint(all_pool_list))
        self.assertTrue(len(all_pool_list) == 2)

        print("Get SNAT pool info from HA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_SNAT_POOL_INFO"])
        all_pool_list = self.ins.get_source_nat_pool(device=mock_device_ins, pool_name="all")
        print(self.tool.pprint(all_pool_list))
        self.assertTrue(len(all_pool_list) == 6)

        print("Get SNAT pool info from SA topo with only 1 pool")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_POOL_INFO_ONLY_1"])
        all_pool_list = self.ins.get_source_nat_pool(device=mock_device_ins, pool_name="all")
        print(self.tool.pprint(all_pool_list))
        self.assertTrue(len(all_pool_list) == 1)

        print("Get SNAT pool info from HA topo with only 1 pool in each node")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_SNAT_POOL_INFO_ONLY_1"])
        all_pool_list = self.ins.get_source_nat_pool(device=mock_device_ins, pool_name="all", node=1)
        print(self.tool.pprint(all_pool_list))
        self.assertTrue(len(all_pool_list) == 2)
        self.assertTrue(all_pool_list[0]["re_name"] == "node0")

        print("Get SNAT pool info with invalid response")
        mock_send_cli_cmd.return_value = {"Invalid-Node": 1,}
        response = self.ins.get_source_nat_pool(device=mock_device_ins, pool_name="A_POOL")
        self.assertFalse(response)

        print("Get SNAT pool extend 1 info from SA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_POOL_INFO_EXTEND_1"])
        all_pool_list = self.ins.get_source_nat_pool(device=mock_device_ins)
        print(self.tool.pprint(all_pool_list))
        self.assertTrue(all_pool_list[0]["source_pool_blk_size"] == "1")
        self.assertTrue(all_pool_list[0]["source_pool_blk_max_per_host"] == "8")
        self.assertTrue(all_pool_list[0]["source_pool_blk_atv_timeout"] == "0")
        self.assertTrue(all_pool_list[0]["source_pool_last_blk_rccl_timeout"] == "0")
        self.assertTrue(all_pool_list[0]["source_pool_blk_interim_log_cycle"] == "0")
        self.assertTrue(all_pool_list[0]["source_pool_blk_log"] == "Enable")
        self.assertTrue(all_pool_list[0]["source_pool_blk_used"] == "4")
        self.assertTrue(all_pool_list[0]["source_pool_blk_total"] == "2500")

        print("Get SNAT pool extend 2 info from SA topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_POOL_INFO_EXTEND_2"])
        all_pool_list = self.ins.get_source_nat_pool(device=mock_device_ins)
        print(self.tool.pprint(all_pool_list))
        self.assertTrue(all_pool_list[0]["source_pool_blk_size"] == "2500")
        self.assertTrue(all_pool_list[0]["source_pool_determ_host_range_num"] == "1")

        print("Get SNAT pool info but don't have some elements")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_POOL_INFO_NO_ELEMENTS"])
        all_pool_list = self.ins.get_source_nat_pool(device=mock_device_ins)
        print(self.tool.pprint(all_pool_list))
        self.assertTrue(all_pool_list[0]["source_pool_blk_size"] == "2500")
        self.assertTrue(all_pool_list[0]["source_pool_determ_host_range_num"] == "1")

        print("No response from device")
        mock_send_cli_cmd.return_value = False
        all_pool_list = self.ins.get_source_nat_pool(device=mock_device_ins)
        self.assertFalse(all_pool_list)

        print("No pool info from xml")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_POOL_INFO_NO_NEEDED_ELEMENT"])
        all_pool_list = self.ins.get_source_nat_pool(device=mock_device_ins)
        self.assertTrue(all_pool_list == list())


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_source_nat_resource_usage(self, mock_send_cli_cmd):
        """test get source nat resource-usage info"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("Get SNAT resource usage from HE HA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_HE_SNAT_RESOURCE_USAGE"])
        entry_list = self.ins.get_source_nat_resource_usage(device=mock_device_ins, more_options="None", lsys_name="lsys1", node="node0")
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 4)
        self.assertTrue(entry_list[0]["re_name"] == "node0")
        self.assertTrue(entry_list[-1]["re_name"] == "node1")

        print("Get SNAT resource usage from HE SA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_HE_SNAT_RESOURCE_USAGE"])
        entry_list = self.ins.get_source_nat_resource_usage(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 2)
        self.assertTrue(entry_list[0]["resource_usage_pool_name"] == "A_POOL")

        print("Get SNAT resource usage from HE SA topology with 1 pool")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_HE_SNAT_RESOURCE_USAGE_WITH_ONE_POOL"])
        entry_list = self.ins.get_source_nat_resource_usage(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 1)
        self.assertTrue(entry_list[0]["resource_usage_pool_name"] == "A_POOL")

        print("Get SNAT resource usage with invalid response")
        mock_send_cli_cmd.return_value = False
        entry_list = self.ins.get_source_nat_resource_usage(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertFalse(entry_list)

        print("Get SNAT resource usage with invalid response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_HE_SNAT_RESOURCE_USAGE_INVALID"])
        entry_list = self.ins.get_source_nat_resource_usage(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertFalse(entry_list)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_source_nat_pool(self, mock_send_cli_cmd):
        """search source nat pooln"""
        mock_device_ins = mock.Mock()

        print("search source nat pool for bool return from SA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_POOL_INFO"])
        status = self.ins.search_source_nat_pool(
            device=mock_device_ins,
            port_overloading_factor=1,
            total_pool_address=256,
            address_range_high="192.168.2.255",
            source_pool_address_range_address_range_low="192.168.2.0-192.168.2.10 in",
            source_pool_address_assignment="no-paired",
            address_pool_hits="0 ge",
        )
        self.assertTrue(status)

        print("search source nat pool for counter return")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_SNAT_POOL_INFO"])
        counter = self.ins.search_source_nat_pool(
            device=mock_device_ins,
            port_overloading_factor=1,
            total_pool_address=("0-256", "in"),
            source_pool_blk_size=8,
            source_pool_address_range_address_range_high="192.168.15.25",
            address_range_low="192.168.15.20",
            source_pool_port_translation="1024, 65535 in",
            source_pool_address_assignment=("no-paired", "contain"),
            address_pool_hits="0 eq",
            re_name="node0",
            return_mode="counter",
            single_port=0,
            single_port_sum=(0, "eq"),
            source_pool_address_range_twin_port="0",
            source_pool_address_range_sum_twin_port_sum=0,
        )
        self.assertTrue(counter == 1)

        print("search source nat pool with no value on device")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_SNAT_POOL_INFO"])
        status = self.ins.search_source_nat_pool(
            device=mock_device_ins,
            host_address_base="192.168.100.0",
        )
        self.assertFalse(status)

        print("search source nat pool but no pool matched")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_POOL_INFO"])
        status = self.ins.search_source_nat_pool(
            device=mock_device_ins,
            port_overloading_factor=1,
            total_pool_address=1024,
            source_pool_blk_size=128,
            address_range_high="100.0.0.43",
            address_range_low="100.0.0.0",
            source_pool_address_assignment=("no-paired", "contain"),
            address_pool_hits="0 ge",
        )
        self.assertFalse(status)

        print("user option have not supported filter")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_POOL_INFO"])
        status = self.ins.search_source_nat_pool(
            device=mock_device_ins,
            port_overloading_factor=1,
            total_pool_address=1024,
            source_pool_blk_size=128,
            address_range_high="100.0.0.43",
            address_range_low="100.0.0.0",
            source_pool_address_assignment=("no-paired", "contain"),
            address_pool_hits="0 ge",
            unknown_filter=10,
        )
        self.assertFalse(status)

        print("search source nat pool with invalid response")
        response = """
        <nat-pool-detail-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
            <total-source-nat-pools>
                <total-source-pools>2</total-source-pools>
            </total-source-nat-pools>
            <source-nat-pool-info-entry>
                <pool-name>A_POOL</pool-name>
                <pool-id>4</pool-id>
                <routing-instance-name>default</routing-instance-name>
                <host-address-base>0.0.0.0</host-address-base>
                <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
                <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
                <port-overloading-factor>1</port-overloading-factor>
                <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                <total-pool-address>256</total-pool-address>
                <address-pool-hits>0</address-pool-hits>
                <source-pool-address-range>
                    <address-range-low>192.168.1.0</address-range-low>
                    <address-range-high>192.168.1.255</address-range-high>
                    <single-port>0</single-port>
                    <twin-port>0</twin-port>
                </source-pool-address-range>
                <source-pool-address-range-sum>
                    <single-port-sum>0</single-port-sum>
                    <twin-port-sum>0</twin-port-sum>
                </source-pool-address-range-sum>
            </source-nat-pool-info-entry>
            <source-nat-pool-info-entry>
                <pool-name>B_POOL</pool-name>
                <pool-id>5</pool-id>
                <routing-instance-name>default</routing-instance-name>
                <host-address-base>0.0.0.0</host-address-base>
                <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
                <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
                <port-overloading-factor>1</port-overloading-factor>
                <source-pool-address-assignment>no-paired</source-pool-address-assignment>
                <total-pool-address>256</total-pool-address>
                <address-pool-hits>0</address-pool-hits>
                <source-pool-address-range>
                    <address-range-low>192.168.2.0</address-range-low>
                    <address-range-high>192.168.2.255</address-range-high>
                    <single-port>0</single-port>
                    <twin-port>0</twin-port>
                </source-pool-address-range>
                <source-pool-address-range-sum>
                    <single-port-sum>0</single-port-sum>
                    <twin-port-sum>0</twin-port-sum>
                </source-pool-address-range-sum>
            </source-nat-pool-info-entry>
        </nat-pool-detail-information>
        """

        print("Check pool with invalid response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        status = self.ins.search_source_nat_pool(
            device=mock_device_ins,
            port_overloading_factor=1,
            total_pool_address=256,
            address_range_high="192.168.2.255",
            address_range_low="192.168.2.0",
            address_pool_hits="0 ge",
        )
        self.assertFalse(status)

        print("Fetch SNAT pool info failed")
        mock_send_cli_cmd.return_value = False
        status = self.ins.search_source_nat_pool(
            device=mock_device_ins,
            port_overloading_factor=1,
            total_pool_address=256,
            address_range_high="192.168.2.255",
            address_range_low="192.168.2.0",
            address_pool_hits="0 ge",
        )
        self.assertFalse(status)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_source_nat_rule(self, mock_send_cli_cmd):
        """checking get SNAT rule info"""
        mock_device_ins = mock.Mock()

        print("SNAT rule from SA")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_RULE_INFO"])
        rule_list = self.ins.get_source_nat_rule(device=mock_device_ins, rule_name="all", lsys_name="lsys1", more_options="None")
        print(self.tool.pprint(rule_list))
        self.assertTrue(len(rule_list) == 1)
        self.assertTrue("re_name" not in rule_list[0])
        self.assertTrue(rule_list[0]["concurrent_hits"] == "0")
        self.assertTrue(rule_list[0]["destination_address_range_entry_rule_destination_address_high_range"] == "0.0.0.0")
        self.assertTrue(rule_list[0]["destination_address_range_entry_rule_destination_address_low_range"] == "0.0.0.0")
        self.assertTrue(rule_list[0]["failed_hits"] == "0")
        self.assertTrue(rule_list[0]["persistent_nat_mapping_type"] == "address-port-mapping")
        self.assertTrue(rule_list[0]["persistent_nat_max_session"] == "0")
        self.assertTrue(rule_list[0]["persistent_nat_timeout"] == "0")
        self.assertTrue(rule_list[0]["persistent_nat_type"] == "N/A")
        self.assertTrue(rule_list[0]["rule_destination_address_high_range"] == "0.0.0.0")
        self.assertTrue(rule_list[0]["rule_destination_address_low_range"] == "0.0.0.0")
        self.assertTrue(rule_list[0]["rule_from_context"] == "zone")
        self.assertTrue(rule_list[0]["rule_from_context_name"] == "trust")
        self.assertTrue(rule_list[0]["rule_id"] == "1")
        self.assertTrue(rule_list[0]["rule_matching_position"] == "1")
        self.assertTrue(rule_list[0]["rule_name"] == "A_rule")
        self.assertTrue(rule_list[0]["rule_set_name"] == "A_ruleset")
        self.assertTrue(rule_list[0]["rule_source_address_high_range"] == "0.0.0.0")
        self.assertTrue(rule_list[0]["rule_source_address_low_range"] == "0.0.0.0")
        self.assertTrue(rule_list[0]["rule_to_context"] == "zone")
        self.assertTrue(rule_list[0]["rule_to_context_name"] == "untrust")
        self.assertTrue(rule_list[0]["rule_translation_hits"] == "0")
        self.assertTrue(rule_list[0]["source_address_range_entry_rule_source_address_high_range"] == "0.0.0.0")
        self.assertTrue(rule_list[0]["source_address_range_entry_rule_source_address_low_range"] == "0.0.0.0")
        self.assertTrue(rule_list[0]["source_nat_rule_action"] == "A_POOL")
        self.assertTrue(rule_list[0]["source_nat_rule_action_entry_persistent_nat_mapping_type"] == "address-port-mapping")
        self.assertTrue(rule_list[0]["source_nat_rule_action_entry_persistent_nat_max_session"] == "0")
        self.assertTrue(rule_list[0]["source_nat_rule_action_entry_persistent_nat_timeout"] == "0")
        self.assertTrue(rule_list[0]["source_nat_rule_action_entry_persistent_nat_type"] == "N/A")
        self.assertTrue(rule_list[0]["source_nat_rule_action_entry_source_nat_rule_action"] == "A_POOL")
        self.assertTrue(rule_list[0]["source_nat_rule_hits_entry_concurrent_hits"] == "0")
        self.assertTrue(rule_list[0]["source_nat_rule_hits_entry_failed_hits"] == "0")
        self.assertTrue(rule_list[0]["source_nat_rule_hits_entry_rule_translation_hits"] == "0")
        self.assertTrue(rule_list[0]["source_nat_rule_hits_entry_succ_hits"] == "0")
        self.assertTrue(rule_list[0]["src_nat_app_entry_src_nat_application"] == "configured")
        self.assertTrue(rule_list[0]["src_nat_application"] == "configured")
        self.assertTrue(rule_list[0]["succ_hits"] == "0")

        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HA_SNAT_RULE_INFO"])
        rule_list = self.ins.get_source_nat_rule(device=mock_device_ins, rule_name="all", node=0)
        print(self.tool.pprint(rule_list))
        self.assertTrue(len(rule_list) == 4)

        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_RULE_INFO"])
        rule_list = self.ins.get_source_nat_rule(device=mock_device_ins, rule_name="A_rule")
        print(self.tool.pprint(rule_list))
        self.assertTrue(len(rule_list) == 1)

        response = """
        <nat-rule-detail-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
            <total-source-nat-rules>
                <total-src-rules>1</total-src-rules>
            </total-source-nat-rules>
            <total-source-nat-rule-ref-addr-num>
                <total-source-nat-rule-ref-addr-num-v4>2</total-source-nat-rule-ref-addr-num-v4>
                <total-source-nat-rule-ref-addr-num-v6>0</total-source-nat-rule-ref-addr-num-v6>
            </total-source-nat-rule-ref-addr-num>
            <source-nat-rule-entry>
                <rule-name>A_rule</rule-name>
                <rule-set-name>A_ruleset</rule-set-name>
                <rule-id>1</rule-id>
                <rule-matching-position>1</rule-matching-position>
                <rule-from-context>zone</rule-from-context>
                <rule-from-context-name>trust</rule-from-context-name>
                <rule-to-context>zone</rule-to-context>
                <rule-to-context-name>untrust</rule-to-context-name>
                <source-address-range-entry>
                    <rule-source-address-low-range>0.0.0.0</rule-source-address-low-range>
                    <rule-source-address-high-range>0.0.0.0</rule-source-address-high-range>
                </source-address-range-entry>
                <destination-address-range-entry>
                    <rule-destination-address-low-range>0.0.0.0</rule-destination-address-low-range>
                    <rule-destination-address-high-range>0.0.0.0</rule-destination-address-high-range>
                </destination-address-range-entry>
                <src-nat-app-entry>
                    <src-nat-application>configured</src-nat-application>
                </src-nat-app-entry>
                <source-nat-rule-action-entry>
                    <source-nat-rule-action>A_POOL</source-nat-rule-action>
                    <persistent-nat-type>N/A              </persistent-nat-type>
                    <persistent-nat-mapping-type>address-port-mapping </persistent-nat-mapping-type>
                    <persistent-nat-timeout>0</persistent-nat-timeout>
                    <persistent-nat-max-session>0</persistent-nat-max-session>
                </source-nat-rule-action-entry>
                <source-nat-rule-hits-entry>
                    <rule-translation-hits>0</rule-translation-hits>
                    <succ-hits>0</succ-hits>
                    <failed-hits>0</failed-hits>
                    <concurrent-hits>0</concurrent-hits>
                </source-nat-rule-hits-entry>
            </source-nat-rule-entry>
        </nat-rule-detail-information>
        """
        print("No enough rule info")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        status = self.ins.get_source_nat_rule(device=mock_device_ins, rule_name="A_rule")
        self.assertFalse(status)

        print("No some elements for SNAT rule")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SA_SNAT_RULE_INFO_NO_ELEMENT"])
        rule_list = self.ins.get_source_nat_rule(device=mock_device_ins, rule_name="A_rule")
        print(self.tool.pprint(rule_list))
        self.assertTrue(len(rule_list) == 1)

        print("No response from device")
        mock_send_cli_cmd.return_value = False
        rule_list = self.ins.get_source_nat_rule(device=mock_device_ins)
        print(self.tool.pprint(rule_list))
        self.assertFalse(rule_list)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_source_nat_port_block(self, mock_send_cli_cmd):
        """checking SNAT port block info"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("Get port block info from SA LE topo with no any block entry")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SNAT_PORT_BLOCK_INFO"])
        entry_list = self.ins.get_source_nat_port_block(device=mock_device_ins, lsys_name="lsys1")
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 1)
        self.assertTrue(entry_list[0]["pba_pool_name"] == "A_POOL")

        print("Get port block info from SA LE topo with only one block entry")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["SNAT_PORT_BLOCK_INFO_WITH_1_ENTRY"])
        entry_list = self.ins.get_source_nat_port_block(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 1)
        self.assertTrue(entry_list[0]["pba_pool_name"] == "A_POOL")

        print("Get port block info from HA HE topo")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HE_HA_PORT_BLOCK_INFO"])
        entry_list = self.ins.get_source_nat_port_block(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 6)

        print("Get port block info by options")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["HE_HA_PORT_BLOCK_INFO"])
        entry_list = self.ins.get_source_nat_port_block(device=mock_device_ins, more_options="pool A_POOL", node=1)
        print(self.tool.pprint(entry_list))
        self.assertTrue(len(entry_list) == 6)

        print("Get port block info failed")
        mock_send_cli_cmd.return_value = False
        entry_list = self.ins.get_source_nat_port_block(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertFalse(entry_list)

        print("Get port block info from invalid response")
        response = """
        <blk-table xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
            <pba-pool-info-entry>
                <pba-pool-name>A_POOL</pba-pool-name>
                <pba-olfactor>1</pba-olfactor>
                <pba-size>128</pba-size>
                <pba-per-host>8</pba-per-host>
                <pba-timeout>0</pba-timeout>
                <pba-last-blk-timeout>0</pba-last-blk-timeout>
                <pba-blk-total>129024</pba-blk-total>
                <pba-blk-used>0</pba-blk-used>
            </pba-pool-info-entry>
        </blk-table>
        """
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=response)
        entry_list = self.ins.get_source_nat_port_block(device=mock_device_ins)
        print(self.tool.pprint(entry_list))
        self.assertFalse(entry_list)

    @mock.patch.object(dev, "execute_vty_command_on_device")
    def test_get_pool_id_owner_spu(self, mock_send_vty_cmd):
        """test get pool id owner spu"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("Get related address by existing pool id")
        mock_send_vty_cmd.side_effect = [
            self.response["SHOW_SPUID_POOL"],
            self.response["SHOW_USP_SPU_CHASSIS"],
        ]

        spu_addr = self.ins.get_pool_id_owner_spu(device=mock_device_ins, pool_id=2, node="node1")
        self.assertTrue(spu_addr == "fpc2.pic0")

        print("Get related address by not existing pool id")
        mock_send_vty_cmd.side_effect = [
            self.response["SHOW_SPUID_POOL_NEG"],
            self.response["SHOW_USP_SPU_CHASSIS"],
        ]
        spu_addr = self.ins.get_pool_id_owner_spu(device=mock_device_ins, pool_id=4)
        self.assertFalse(spu_addr)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_source_nat_deterministic(self, mock_send_cli_cmd):
        """check persistent SNAT interface info with invalid response"""
        mock_device_ins = mock.Mock()

        print("match block entry by network and pool name from Lowend HA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_SNAT_DETERMINSTIC"])
        match_cnt = self.ins.search_source_nat_deterministic(
            device=mock_device_ins,
            return_mode="counter",
            blk_internal_ip=("192.168.150.0/30", "in"),
            blk_reflexive_ip="192.168.150.0 eq",
            blk_ports_ol=1,
        )
        print("match_cnt: {}".format(match_cnt))
        self.assertTrue(match_cnt >= 2)

        print("match block entry by network and unmatched value from Lowend HA topology")
        status = self.ins.search_source_nat_deterministic(
            device=mock_device_ins,
            blk_ports_ol=10,
        )
        self.assertFalse(status)

        print("match block entry by network and unmatched pool name from Lowend HA topology")
        match_cnt = self.ins.search_source_nat_deterministic(
            device=mock_device_ins,
            return_mode="counter",
            node=1,
            blk_internal_ip=("192.168.150.0/30", "in"),
            blk_reflexive_ip="192.168.150.0 eq",
            blk_ports_ol=1,
            blk_ports_used=0,
            blk_high_port=("1000-2000", "in"),
            blk_low_port=("1000-2000", "in"),
        )
        print("match_cnt: {}".format(match_cnt))
        self.assertTrue(match_cnt >= 2)

        print("check all option from .robot file")
        match_cnt = self.ins.search_source_nat_deterministic(
            device=mock_device_ins,
            return_mode="counter",
            node="1",
            blk_internal_ip="192.168.150.0/30 in",
            blk_reflexive_ip="192.168.150.0 eq",
            blk_ports_ol="1",
            blk_ports_used="0",
            blk_high_port="2000 le",
            blk_low_port="1224 ge",
        )
        print("match_cnt: {}".format(match_cnt))
        self.assertTrue(match_cnt >= 2)

        print("Invalid option node checking")
        self.assertRaisesRegex(
            ValueError,
            r"'node' must be",
            self.ins.search_source_nat_deterministic,
            device=mock_device_ins, node="Unknown",
        )

        print("check LowEnd SA topo response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_SNAT_DETERMINISTIC"])
        match_cnt = self.ins.search_source_nat_deterministic(
            device=mock_device_ins,
            return_mode="counter",
            blk_internal_ip="192.168.150.0/30 in",
            blk_reflexive_ip="192.168.150.0 eq",
            blk_ports_ol="1",
            blk_ports_used="0",
            blk_high_port="2000 le",
            blk_low_port="1224 ge",
        )
        print("match_cnt: {}".format(match_cnt))
        self.assertTrue(match_cnt >= 2)

        print("check LowEnd SA topo response that only have 1 block entry")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_SNAT_DETERMINISTIC_ONE"])
        match_cnt = self.ins.search_source_nat_deterministic(
            device=mock_device_ins,
            return_mode="counter",
            blk_internal_ip="192.168.150.0/30 in",
            blk_reflexive_ip="192.168.150.0 eq",
            blk_ports_ol="1",
            blk_ports_used="0",
            blk_high_port="2000 le",
            blk_low_port="1224 le",
        )
        print("match_cnt: {}".format(match_cnt))
        self.assertTrue(match_cnt == 1)

        print("check LowEnd HA topo response that only have 1 block entry")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_SNAT_DETERMINISTIC_ONE"])
        match_cnt = self.ins.search_source_nat_deterministic(
            device=mock_device_ins,
            return_mode="counter",
            blk_internal_ip="192.168.150.0/30 in",
            blk_reflexive_ip="192.168.150.0 eq",
            blk_ports_ol="1",
            blk_ports_used="0",
        )
        print("match_cnt: {}".format(match_cnt))
        self.assertTrue(match_cnt == 2)

        print("check HighEnd HA topo response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_SNAT_DETERMINISTIC"])
        match_cnt = self.ins.search_source_nat_deterministic(
            device=mock_device_ins,
            return_mode="counter",
            blk_internal_ip="192.168.160.0/30 in",
            blk_reflexive_ip="192.168.160.0 eq",
            blk_ports_ol="1",
            blk_ports_used="0",
        )
        print("match_cnt: {}".format(match_cnt))
        self.assertTrue(match_cnt == 8)

        print("check HighEnd HA topo response form node")
        match_cnt = self.ins.search_source_nat_deterministic(
            device=mock_device_ins,
            return_mode="counter",
            node=0,
            blk_internal_ip="192.168.160.0/30 in",
            blk_reflexive_ip="192.168.160.0 eq",
            blk_ports_ol="1",
            blk_ports_used="0",
        )
        print("match_cnt: {}".format(match_cnt))
        self.assertTrue(match_cnt == 4)

        print("check no entry get from device")
        mock_send_cli_cmd.return_value = False
        match_cnt = self.ins.search_source_nat_deterministic(device=mock_device_ins)
        print("match_cnt: {}".format(match_cnt))
        self.assertFalse(match_cnt)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_source_nat_rule(self, mock_send_cli_cmd):
        """search source nat rule info"""
        mock_device_ins = mock.Mock()

        print("match rule from SA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_SNAT_RULE_INFO"])
        match_cnt = self.ins.search_source_nat_rule(
            device=mock_device_ins,
            return_mode="counter",
            destination_address_range_entry_rule_destination_address_high_range=("0.0.0.0", "eq"),
            rule_from_context_name="trust",
            rule_name="A_rule",
        )
        self.assertTrue(match_cnt == 1)

        print("match rule from HA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_SNAT_RULE_INFO"])
        match_cnt = self.ins.search_source_nat_rule(
            device=mock_device_ins,
            return_mode="counter",
            re_name="node0",
            rule_destination_address_high_range=("192.168.100.0/24", "in"),
            rule_from_context_name="untrust",
        )
        self.assertTrue(match_cnt >= 1)

        print("match rule with un-supported option")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_SNAT_RULE_INFO"])
        status = self.ins.search_source_nat_rule(
            device=mock_device_ins,
            return_mode="counter",
            re_name="node0",
            rule_destination_address_high_range=("192.168.100.0/24", "in"),
            rule_from_context_name="untrust",
            unsupported_option="unknown",
        )
        self.assertFalse(status)

        print("check no entry on device")
        mock_send_cli_cmd.return_value = False
        status = self.ins.search_source_nat_rule(
            device=mock_device_ins,
            return_mode="counter",
            re_name="node0",
            rule_destination_address_high_range=("192.168.100.0/24", "in"),
            rule_from_context_name="untrust",
        )
        self.assertFalse(status)

        print("check not existing element")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_SNAT_RULE_INFO"])
        status = self.ins.search_source_nat_rule(
            device=mock_device_ins,
            src_nat_protocol_entry="hello",
        )
        self.assertFalse(status)

        print("fetch rule list failed")
        mock_send_cli_cmd.return_value = False
        status = self.ins.search_source_nat_rule(
            device=mock_device_ins,
            src_nat_protocol_entry="hello",
        )
        self.assertFalse(status)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_source_nat_port_block(self, mock_send_cli_cmd):
        """search source nat port block entry"""
        mock_device_ins = mock.Mock()

        print("match port block from SA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SNAT_PORT_BLOCK_INFO"])
        match_cnt = self.ins.search_source_nat_port_block(
            device=mock_device_ins,
            return_mode="counter",
            pba_pool_name="A_POOL",
            pba_size=(128, "ge"),
            pba_blk_total="100000-150000 in",
        )
        self.assertEqual(match_cnt, 1)

        print("match port block from HA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_HA_PORT_BLOCK_INFO"])
        match_cnt = self.ins.search_source_nat_port_block(
            device=mock_device_ins,
            return_mode="counter",
            pba_pool_name="A_POOL",
            blk_internal_ip=("121.11.10.0/24", "in"),
            blk_reflexive_ip="121.11.15.0/24 in",
            pba_size=64,
        )
        self.assertEqual(match_cnt, 3)

        print("match port block with invalid INT")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_HA_PORT_BLOCK_INFO"])
        match_cnt = self.ins.search_source_nat_port_block(
            device=mock_device_ins,
            return_mode="counter",
            pba_pool_name="A_POOL",
            blk_internal_ip="121.11.10.2",
            blk_reflexive_ip="121.11.15.0/24 in",
            blk_left_time="-",
        )
        self.assertEqual(match_cnt, 1)

        print("checking whether match port block entry")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_HA_PORT_BLOCK_INFO"])
        match = self.ins.search_source_nat_port_block(
            device=mock_device_ins,
            pba_pool_name="A_POOL",
            blk_internal_ip="121.11.10.2",
            blk_reflexive_ip="121.11.15.0/24 in",
        )
        self.assertTrue(match)

        print("checking no port block entry matched")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_HA_PORT_BLOCK_INFO"])
        match = self.ins.search_source_nat_port_block(
            device=mock_device_ins,
            pba_pool_name="C_POOL",
        )
        self.assertFalse(match)

        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HE_HA_PORT_BLOCK_INFO"])
        match_cnt = self.ins.search_source_nat_port_block(
            device=mock_device_ins,
            return_mode="counter",
            pba_pool_name="C_POOL",
        )
        self.assertEqual(match_cnt, 0)

        print("checking get port block info from device failed")
        mock_send_cli_cmd.return_value = False
        match = self.ins.search_source_nat_port_block(
            device=mock_device_ins,
            pba_pool_name="A_POOL",
        )
        self.assertFalse(match)

        print("checking invalid option")
        mock_send_cli_cmd.return_value = False
        self.assertFalse(self.ins.search_source_nat_port_block(device=mock_device_ins))

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_source_nat_resource_usage(self, mock_send_cli_cmd):
        """search source nat resource usage entry"""
        mock_device_ins = mock.Mock()

        print("match resource usage from SA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_SNAT_RESOURCE_USAGE"])
        match_cnt = self.ins.search_source_nat_resource_usage(
            device=mock_device_ins,
            return_mode="counter",
            resource_usage_pool_name="A_POOL",
            resource_usage_total_address=(10, "eq"),
            resource_usage_peak_usage="0% eq",

        )
        self.assertTrue(match_cnt == 1)

        print("match resource usage from HA topology")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_SNAT_RESOURCE_USAGE"])
        match_cnt = self.ins.search_source_nat_resource_usage(
            device=mock_device_ins,
            return_mode="counter",
            resource_usage_total_address=(10, "eq"),
            re_name="node0"
        )
        self.assertTrue(match_cnt == 2)

        print("No match entriy")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_SNAT_RESOURCE_USAGE"])
        match_cnt = self.ins.search_source_nat_resource_usage(
            device=mock_device_ins,
            resource_usage_total_address=(1000, "eq"),
            resource_usage_peak_usage="0% eq",
        )
        self.assertFalse(match_cnt)

        print("Got invalid response")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_SNAT_RESOURCE_USAGE_INVALID"])
        match_cnt = self.ins.search_source_nat_resource_usage(
            device=mock_device_ins,
            resource_usage_total_address=(1000, "eq"),
        )
        self.assertFalse(match_cnt)

        print("No entry from device")
        mock_send_cli_cmd.return_value = False
        match_cnt = self.ins.search_source_nat_resource_usage(device=mock_device_ins)
        self.assertFalse(match_cnt)


    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_pst_nat_table_summary(self, mock_send_cli_cmd):
        """check persistent SNAT table summary info"""
        mock_device_ins = mock.Mock()

        print("Test get pst nat table summary without persist-nat-table in dict")
        mock_send_cli_cmd.return_value = False
        xml_dict = self.ins.get_pst_nat_table_summary(device=mock_device_ins)
        self.assertFalse(xml_dict)

        print("Test get pst nat table summary on Low End platforms without SPU(SPM).")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["PERSISTENT_NAT_TABLE_SUMMARY_LE"])
        xml_dict = self.ins.get_pst_nat_table_summary(device=mock_device_ins)
        print(self.tool.pprint(xml_dict))
        self.assertTrue(xml_dict.get('binding in use') == 100)
        self.assertTrue(xml_dict.get('enode in use') == 300)

        print("Test get pst nat table summary on High End platforms with multiple SPU(SPM)s.")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["PERSISTENT_NAT_TABLE_SUMMARY"])
        xml_dict = self.ins.get_pst_nat_table_summary(device=mock_device_ins, root=True)
        print(self.tool.pprint(xml_dict))
        self.assertTrue(xml_dict.get('binding in use') == 400)
        self.assertTrue(xml_dict.get('enode in use') == 600)

        print("Test get pst nat table summary on High End platforms with multiple SPU(SPM)s by FLAT_DICT")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["PERSISTENT_NAT_TABLE_SUMMARY"])
        xml_dict = self.ins.get_pst_nat_table_summary(device=mock_device_ins, root=True, return_mode="flat_dict")
        print(self.tool.pprint(xml_dict))
        self.assertTrue(xml_dict[0]["persist_nat_table_statistic_persist_nat_binding_in_use"], "100")
        self.assertTrue(xml_dict[0]["persist_nat_table_statistic_persist_nat_binding_total"], "524288")
        self.assertTrue(xml_dict[0]["persist_nat_table_statistic_persist_nat_enode_in_use"], "300")
        self.assertTrue(xml_dict[0]["persist_nat_table_statistic_persist_nat_enode_total"], "4194304")
        self.assertTrue(xml_dict[0]["persist_nat_table_statistic_persist_nat_spu_id"], "on FPC0 PIC1:")
        self.assertTrue(xml_dict[1]["persist_nat_table_statistic_persist_nat_binding_in_use"], "200")
        self.assertTrue(xml_dict[1]["persist_nat_table_statistic_persist_nat_binding_total"], "524288")
        self.assertTrue(xml_dict[1]["persist_nat_table_statistic_persist_nat_enode_in_use"], "200")
        self.assertTrue(xml_dict[1]["persist_nat_table_statistic_persist_nat_enode_total"], "4194304")
        self.assertTrue(xml_dict[1]["persist_nat_table_statistic_persist_nat_spu_id"], "on FPC0 PIC2:")
        self.assertTrue(xml_dict[2]["persist_nat_table_statistic_persist_nat_binding_in_use"], "100")
        self.assertTrue(xml_dict[2]["persist_nat_table_statistic_persist_nat_binding_total"], "524288")
        self.assertTrue(xml_dict[2]["persist_nat_table_statistic_persist_nat_enode_in_use"], "100")
        self.assertTrue(xml_dict[2]["persist_nat_table_statistic_persist_nat_enode_total"], "4194304")
        self.assertTrue(xml_dict[2]["persist_nat_table_statistic_persist_nat_spu_id"], "on FPC0 PIC3:")


        print("Test get pst nat table summary on High End HA platforms with multiple SPU(SPM)s.")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["PERSISTENT_NAT_TABLE_SUMMARY_HA"])
        xml_dict = self.ins.get_pst_nat_table_summary(device=mock_device_ins, lsys='LSYS1')
        print(self.tool.pprint(xml_dict))
        self.assertTrue(xml_dict.get('binding in use') == 60)
        self.assertTrue(xml_dict.get('enode in use') == 60)

        print("Test get pst nat table summary on High End HA platforms with multiple SPU(SPM)s with return_mode flat_dict")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["PERSISTENT_NAT_TABLE_SUMMARY_HA"])
        xml_dict = self.ins.get_pst_nat_table_summary(device=mock_device_ins, lsys='LSYS1', return_mode="FLat_Dict")
        print(self.tool.pprint(xml_dict))
        self.assertTrue(xml_dict[0]["re_name"] == "node0")
        self.assertTrue(xml_dict[-1]["re_name"] == "node1")


        print("Test get pst nat table summary on High End HA platforms with multiple SPU(SPM)s with more_options.")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["PERSISTENT_NAT_TABLE_SUMMARY_HA"])
        xml_dict = self.ins.get_pst_nat_table_summary(device=mock_device_ins, more_options='logical-system LSYS1')
        print(self.tool.pprint(xml_dict))
        self.assertTrue(xml_dict.get('binding in use') == 60)
        self.assertTrue(xml_dict.get('enode in use') == 60)

        print("Test get pst nat table summary on Low End HA platforms with given node id without SPU(SPM).")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=self.response["PERSISTENT_NAT_TABLE_SUMMARY_HA_ONE_NODE"])
        xml_dict = self.ins.get_pst_nat_table_summary(device=mock_device_ins, lsys='LSYS1', node=0)
        print(self.tool.pprint(xml_dict))
        self.assertTrue(xml_dict.get('binding in use') == 10)
        self.assertTrue(xml_dict.get('enode in use') == 10)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_pst_nat_table_entry(self, mock_send_cli_cmd):
        """check persistent SNAT table entry info"""
        mock_device_ins = mock.Mock()

        xml_output = {}
        xml_output["PST_TABLE_ENTRY_NEG"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.3I0/junos">
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <persist-nat-spu-id> on FPC1 PIC1:</persist-nat-spu-id>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <persist-nat-spu-id> on FPC1 PIC2:</persist-nat-spu-id>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <persist-nat-spu-id> on FPC1 PIC3:</persist-nat-spu-id>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <persist-nat-spu-id> on FPC2 PIC0:</persist-nat-spu-id>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <persist-nat-spu-id> on FPC2 PIC1:</persist-nat-spu-id>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <persist-nat-spu-id> on FPC2 PIC2:</persist-nat-spu-id>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3I0/junos-nat">
                <persist-nat-spu-id> on FPC2 PIC3:</persist-nat-spu-id>
            </persist-nat-table>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>"""

        xml_output["PST_TABLE_ENTRY_SA"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
            <persist-nat-table xmlns="http://xml.juniper.net/junos/15.1I0/junos-nat">
                <persist-nat-table-entry>
                    <persist-nat-internal-ip>2000::2</persist-nat-internal-ip>
                    <persist-nat-internal-port>3478</persist-nat-internal-port>
                    <persist-nat-internal-proto>udp</persist-nat-internal-proto>
                    <persist-nat-reflexive-ip>200.0.1.0</persist-nat-reflexive-ip>
                    <persist-nat-reflexive-port>10039</persist-nat-reflexive-port>
                    <persist-nat-reflexive-proto>udp</persist-nat-reflexive-proto>
                    <persist-nat-pool-name>pat</persist-nat-pool-name>
                    <persist-nat-type>any-remote-host </persist-nat-type>
                    <persist-nat-left-time>-</persist-nat-left-time>
                    <persist-nat-config-time>300</persist-nat-config-time>
                    <persist-nat-current-session-num>1</persist-nat-current-session-num>
                    <persist-nat-max-session-num>30</persist-nat-max-session-num>
                    <persist-nat-rule-name>nat64_pat</persist-nat-rule-name>
                </persist-nat-table-entry>
                <persist-nat-table-entry>
                    <persist-nat-internal-ip>2000::2</persist-nat-internal-ip>
                    <persist-nat-internal-port>6000</persist-nat-internal-port>
                    <persist-nat-internal-proto>udp</persist-nat-internal-proto>
                    <persist-nat-reflexive-ip>200.0.1.1</persist-nat-reflexive-ip>
                    <persist-nat-reflexive-port>10932</persist-nat-reflexive-port>
                    <persist-nat-reflexive-proto>udp</persist-nat-reflexive-proto>
                    <persist-nat-pool-name>pat</persist-nat-pool-name>
                    <persist-nat-type>any-remote-host </persist-nat-type>
                    <persist-nat-left-time>-</persist-nat-left-time>
                    <persist-nat-config-time>300</persist-nat-config-time>
                    <persist-nat-current-session-num>1</persist-nat-current-session-num>
                    <persist-nat-max-session-num>30</persist-nat-max-session-num>
                    <persist-nat-rule-name>nat64_pat</persist-nat-rule-name>
                </persist-nat-table-entry>
            </persist-nat-table>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>"""
        xml_output["PST_TABLE_MULIT_ENTRES_SA"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.3D0/junos">
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                <persist-nat-spu-id> on FPC2 PIC1:</persist-nat-spu-id>
                <persist-nat-table-entry>
                    <persist-nat-internal-ip>172.16.0.2</persist-nat-internal-ip>
                    <persist-nat-internal-port>43702</persist-nat-internal-port>
                    <persist-nat-internal-proto>tcp</persist-nat-internal-proto>
                    <persist-nat-reflexive-ip>20.0.0.205</persist-nat-reflexive-ip>
                    <persist-nat-reflexive-port>15681</persist-nat-reflexive-port>
                    <persist-nat-reflexive-proto>tcp</persist-nat-reflexive-proto>
                    <persist-nat-pool-name>pat</persist-nat-pool-name>
                    <persist-nat-type>target-host     </persist-nat-type>
                    <persist-nat-left-time>-</persist-nat-left-time>
                    <persist-nat-config-time>300</persist-nat-config-time>
                    <persist-nat-current-session-num>1</persist-nat-current-session-num>
                    <persist-nat-max-session-num>30</persist-nat-max-session-num>
                    <persist-nat-rule-name>rule1</persist-nat-rule-name>
                </persist-nat-table-entry>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                <persist-nat-spu-id> on FPC2 PIC2:</persist-nat-spu-id>
                <persist-nat-table-entry>
                    <persist-nat-internal-ip>172.16.0.2</persist-nat-internal-ip>
                    <persist-nat-internal-port>43701</persist-nat-internal-port>
                    <persist-nat-internal-proto>tcp</persist-nat-internal-proto>
                    <persist-nat-reflexive-ip>20.0.0.204</persist-nat-reflexive-ip>
                    <persist-nat-reflexive-port>29432</persist-nat-reflexive-port>
                    <persist-nat-reflexive-proto>tcp</persist-nat-reflexive-proto>
                    <persist-nat-pool-name>pat</persist-nat-pool-name>
                    <persist-nat-type>target-host     </persist-nat-type>
                    <persist-nat-left-time>276</persist-nat-left-time>
                    <persist-nat-config-time>300</persist-nat-config-time>
                    <persist-nat-current-session-num>0</persist-nat-current-session-num>
                    <persist-nat-max-session-num>30</persist-nat-max-session-num>
                    <persist-nat-rule-name>rule1</persist-nat-rule-name>
                </persist-nat-table-entry>
            </persist-nat-table>
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                <persist-nat-spu-id> on FPC2 PIC3:</persist-nat-spu-id>
            </persist-nat-table>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """
        xml_output["PST_TABLE_ENTRY_DETAIL_SA"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.3D0/junos">
            <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                <persist-nat-spu-id> on FPC2 PIC0:</persist-nat-spu-id>
                <persist-nat-table-entry>
                    <persist-nat-internal-ip>172.16.0.3</persist-nat-internal-ip>
                    <persist-nat-internal-port>1024</persist-nat-internal-port>
                    <persist-nat-internal-proto>udp</persist-nat-internal-proto>
                    <persist-nat-reflexive-ip>20.0.0.207</persist-nat-reflexive-ip>
                    <persist-nat-reflexive-port>1232</persist-nat-reflexive-port>
                    <persist-nat-reflexive-proto>udp</persist-nat-reflexive-proto>
                    <persist-nat-pool-name>pat</persist-nat-pool-name>
                    <persist-nat-type>target-host     </persist-nat-type>
                    <persist-nat-left-time>-</persist-nat-left-time>
                    <persist-nat-config-time>300</persist-nat-config-time>
                    <persist-nat-current-session-num>2</persist-nat-current-session-num>
                    <persist-nat-max-session-num>30</persist-nat-max-session-num>
                    <persist-nat-rule-name>rule1</persist-nat-rule-name>
                </persist-nat-table-entry>
            </persist-nat-table>
            <persist-nat-external-node-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                <persist-nat-external-node-entry>
                    <persist-nat-enode-internal-ip>172.16.0.3</persist-nat-enode-internal-ip>
                    <persist-nat-enode-internal-port>1024</persist-nat-enode-internal-port>
                    <persist-nat-enode-external-ip>20.0.0.5</persist-nat-enode-external-ip>
                    <persist-nat-enode-external-port>0</persist-nat-enode-external-port>
                    <persist-nat-zone-name>untrust</persist-nat-zone-name>
                </persist-nat-external-node-entry>
                <persist-nat-external-node-entry>
                    <persist-nat-enode-internal-ip>172.16.0.3</persist-nat-enode-internal-ip>
                    <persist-nat-enode-internal-port>1024</persist-nat-enode-internal-port>
                    <persist-nat-enode-external-ip>20.0.0.4</persist-nat-enode-external-ip>
                    <persist-nat-enode-external-port>0</persist-nat-enode-external-port>
                    <persist-nat-zone-name>untrust</persist-nat-zone-name>
                </persist-nat-external-node-entry>
                <persist-nat-external-node-entry>
                    <persist-nat-enode-internal-ip>172.16.0.3</persist-nat-enode-internal-ip>
                    <persist-nat-enode-internal-port>1024</persist-nat-enode-internal-port>
                    <persist-nat-enode-external-ip>20.0.0.3</persist-nat-enode-external-ip>
                    <persist-nat-enode-external-port>0</persist-nat-enode-external-port>
                    <persist-nat-zone-name>untrust</persist-nat-zone-name>
                </persist-nat-external-node-entry>
            </persist-nat-external-node-table>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """
        xml_output["PST_TABLE_ENTRY_DETAIL_HA"] = """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.3D0/junos">
            <multi-routing-engine-results>

                <multi-routing-engine-item>

                    <re-name>node0</re-name>

                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-spu-id> on FPC0 PIC1:</persist-nat-spu-id>
                        <persist-nat-table-entry>
                            <persist-nat-internal-ip>172.16.0.3</persist-nat-internal-ip>
                            <persist-nat-internal-port>1024</persist-nat-internal-port>
                            <persist-nat-internal-proto>udp</persist-nat-internal-proto>
                            <persist-nat-reflexive-ip>20.0.0.207</persist-nat-reflexive-ip>
                            <persist-nat-reflexive-port>1232</persist-nat-reflexive-port>
                            <persist-nat-reflexive-proto>udp</persist-nat-reflexive-proto>
                            <persist-nat-pool-name>pat</persist-nat-pool-name>
                            <persist-nat-type>target-host     </persist-nat-type>
                            <persist-nat-left-time>-</persist-nat-left-time>
                            <persist-nat-config-time>300</persist-nat-config-time>
                            <persist-nat-current-session-num>2</persist-nat-current-session-num>
                            <persist-nat-max-session-num>30</persist-nat-max-session-num>
                            <persist-nat-rule-name>rule1</persist-nat-rule-name>
                        </persist-nat-table-entry>
                    </persist-nat-table>
                    <persist-nat-external-node-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-external-node-entry>
                            <persist-nat-enode-internal-ip>172.16.0.3</persist-nat-enode-internal-ip>
                            <persist-nat-enode-internal-port>1024</persist-nat-enode-internal-port>
                            <persist-nat-enode-external-ip>20.0.0.5</persist-nat-enode-external-ip>
                            <persist-nat-enode-external-port>0</persist-nat-enode-external-port>
                            <persist-nat-zone-name>untrust</persist-nat-zone-name>
                        </persist-nat-external-node-entry>
                        <persist-nat-external-node-entry>
                            <persist-nat-enode-internal-ip>172.16.0.3</persist-nat-enode-internal-ip>
                            <persist-nat-enode-internal-port>1024</persist-nat-enode-internal-port>
                            <persist-nat-enode-external-ip>20.0.0.4</persist-nat-enode-external-ip>
                            <persist-nat-enode-external-port>0</persist-nat-enode-external-port>
                            <persist-nat-zone-name>untrust</persist-nat-zone-name>
                        </persist-nat-external-node-entry>
                        <persist-nat-external-node-entry>
                            <persist-nat-enode-internal-ip>172.16.0.3</persist-nat-enode-internal-ip>
                            <persist-nat-enode-internal-port>1024</persist-nat-enode-internal-port>
                            <persist-nat-enode-external-ip>20.0.0.3</persist-nat-enode-external-ip>
                            <persist-nat-enode-external-port>0</persist-nat-enode-external-port>
                            <persist-nat-zone-name>untrust</persist-nat-zone-name>
                        </persist-nat-external-node-entry>
                    </persist-nat-external-node-table>
                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-spu-id> on FPC0 PIC2:</persist-nat-spu-id>
                    </persist-nat-table>
                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-spu-id> on FPC0 PIC3:</persist-nat-spu-id>
                    </persist-nat-table>
                </multi-routing-engine-item>

                <multi-routing-engine-item>

                    <re-name>node1</re-name>

                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-spu-id> on FPC0 PIC1:</persist-nat-spu-id>
                        <persist-nat-table-entry>
                            <persist-nat-internal-ip>172.16.0.3</persist-nat-internal-ip>
                            <persist-nat-internal-port>1024</persist-nat-internal-port>
                            <persist-nat-internal-proto>udp</persist-nat-internal-proto>
                            <persist-nat-reflexive-ip>20.0.0.207</persist-nat-reflexive-ip>
                            <persist-nat-reflexive-port>1232</persist-nat-reflexive-port>
                            <persist-nat-reflexive-proto>udp</persist-nat-reflexive-proto>
                            <persist-nat-pool-name>pat</persist-nat-pool-name>
                            <persist-nat-type>target-host     </persist-nat-type>
                            <persist-nat-left-time>-</persist-nat-left-time>
                            <persist-nat-config-time>300</persist-nat-config-time>
                            <persist-nat-current-session-num>2</persist-nat-current-session-num>
                            <persist-nat-max-session-num>30</persist-nat-max-session-num>
                            <persist-nat-rule-name>rule1</persist-nat-rule-name>
                        </persist-nat-table-entry>
                    </persist-nat-table>
                    <persist-nat-external-node-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-external-node-entry>
                            <persist-nat-enode-internal-ip>172.16.0.3</persist-nat-enode-internal-ip>
                            <persist-nat-enode-internal-port>1024</persist-nat-enode-internal-port>
                            <persist-nat-enode-external-ip>20.0.0.5</persist-nat-enode-external-ip>
                            <persist-nat-enode-external-port>0</persist-nat-enode-external-port>
                            <persist-nat-zone-name>untrust</persist-nat-zone-name>
                        </persist-nat-external-node-entry>
                        <persist-nat-external-node-entry>
                            <persist-nat-enode-internal-ip>172.16.0.3</persist-nat-enode-internal-ip>
                            <persist-nat-enode-internal-port>1024</persist-nat-enode-internal-port>
                            <persist-nat-enode-external-ip>20.0.0.4</persist-nat-enode-external-ip>
                            <persist-nat-enode-external-port>0</persist-nat-enode-external-port>
                            <persist-nat-zone-name>untrust</persist-nat-zone-name>
                        </persist-nat-external-node-entry>
                        <persist-nat-external-node-entry>
                            <persist-nat-enode-internal-ip>172.16.0.3</persist-nat-enode-internal-ip>
                            <persist-nat-enode-internal-port>1024</persist-nat-enode-internal-port>
                            <persist-nat-enode-external-ip>20.0.0.3</persist-nat-enode-external-ip>
                            <persist-nat-enode-external-port>0</persist-nat-enode-external-port>
                            <persist-nat-zone-name>untrust</persist-nat-zone-name>
                        </persist-nat-external-node-entry>
                    </persist-nat-external-node-table>
                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-spu-id> on FPC0 PIC2:</persist-nat-spu-id>
                    </persist-nat-table>
                    <persist-nat-table xmlns="http://xml.juniper.net/junos/17.3D0/junos-nat">
                        <persist-nat-spu-id> on FPC0 PIC3:</persist-nat-spu-id>
                    </persist-nat-table>
                </multi-routing-engine-item>

            </multi-routing-engine-results>
            <cli>
                <banner>{primary:node0}</banner>
            </cli>
        </rpc-reply>
        """

        print("Test get pst nat table entry with internal-ip without persist-nat-table-entry.")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=xml_output["PST_TABLE_ENTRY_NEG"])
        xml_dict = self.ins.get_pst_nat_table_entry(device=mock_device_ins, in_ip='2000::2', lsys='LSYS1', node=0)
        print(self.tool.pprint(xml_dict))
        self.assertTrue(len(xml_dict) == 0)

        print("Test get pst nat table entry with internal-ip without multi SPU(M)s.")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=xml_output["PST_TABLE_ENTRY_SA"])
        xml_dict = self.ins.get_pst_nat_table_entry(device=mock_device_ins, in_ip='2000::2', root=1)
        print(self.tool.pprint(xml_dict))
        self.assertTrue(len(xml_dict) == 2)
        self.assertTrue(xml_dict[1]["in_ip"] == '2000::2')
        self.assertTrue(xml_dict[1]["life_time"] == None)
        self.assertTrue(xml_dict[1]["persist_nat_left_time"] == None)

        print("Test get pst nat table entry with internal-ip with multi SPU(M)s.")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=xml_output["PST_TABLE_MULIT_ENTRES_SA"])
        xml_dict = self.ins.get_pst_nat_table_entry(device=mock_device_ins, in_ip='172.16.0.2')
        print(self.tool.pprint(xml_dict))
        self.assertTrue(len(xml_dict) == 2)
        self.assertTrue(xml_dict[0]["in_ip"] == '172.16.0.2')

        print("Test get pst nat table entry with internal-ip internal-port and internal-protocol with multi SPU(M)s.")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=xml_output["PST_TABLE_ENTRY_DETAIL_SA"])
        xml_dict = self.ins.get_pst_nat_table_entry(device=mock_device_ins, in_ip='172.16.0.2', in_port=1024, in_proto='udp')
        print(self.tool.pprint(xml_dict))
        self.assertTrue(len(xml_dict) == 1)
        self.assertTrue(xml_dict[0]["in_ip"] == '172.16.0.3')
        self.assertTrue(xml_dict[0]["in_port"] == '1024')

        print("Test get pst nat table entry with internal-ip internal-port and internal-protocol with HA")
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(xml_str=xml_output["PST_TABLE_ENTRY_DETAIL_HA"])
        xml_dict = self.ins.get_pst_nat_table_entry(
            device=mock_device_ins,
            in_ip='172.16.0.2',
            in_port=1024,
            in_proto='udp',
            more_options='logical-system LSYS1',
        )
        print(self.tool.pprint(xml_dict))
        self.assertTrue(len(xml_dict) == 2)
        self.assertTrue(xml_dict[0]["in_ip"] == '172.16.0.3')
        self.assertTrue(xml_dict[0]["in_port"] == '1024')

        print("No response from device")
        mock_send_cli_cmd.return_value = False
        xml_dict = self.ins.get_pst_nat_table_entry(
            device=mock_device_ins,
            in_ip='172.16.0.2',
            in_port=1024,
            in_proto='udp',
            more_options='logical-system LSYS1',
        )
        print(self.tool.pprint(xml_dict))
        self.assertFalse(xml_dict)
