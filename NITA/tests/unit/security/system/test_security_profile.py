# coding: UTF-8
"""All unit test cases for system security-profile module"""
# pylint: disable=attribute-defined-outside-init,invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
from unittest import TestCase, mock

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.security.system.security_profile import security_profile


class TestSecurityProfile(TestCase):
    """Unitest cases for security profile module"""
    def setUp(self):
        """setup before all cases"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.ins = security_profile()

        self.mock_device_ins = mock.Mock()

        self.response = {}

        self.response["SA_HE_ADDRESS_BOOK"] = """
    <security-profile-address-book-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>4000</resources-maximum>
        </security-profile-information>
    </security-profile-address-book-information>
        """

        self.response["SA_HE_ADDRESS_BOOK_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0           0        4000
        """

        self.response["SA_HE_APPFW_PROFILE"] = """
    <security-profile-appfw-profile-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="detail">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>57344</resources-maximum>
        </security-profile-information>
    </security-profile-appfw-profile-information>
        """

        self.response["SA_HE_APPFW_PROFILE_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0           0       57344
        """

        self.response["SA_HE_APPFW_RULE"] = """
    <security-profile-appfw-rule-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>114688</resources-maximum>
        </security-profile-information>
    </security-profile-appfw-rule-information>
        """

        self.response["SA_HE_APPFW_RULE_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0           0      114688
        """

        self.response["SA_HE_APPFW_RULE_SET"] = """
    <security-profile-appfw-rule-set-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>57344</resources-maximum>
        </security-profile-information>
    </security-profile-appfw-rule-set-information>
        """

        self.response["SA_HE_APPFW_RULE_SET_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0           0       57344
        """

        self.response["SA_HE_FLOW_GATE"] = """
    <security-profile-flow-gate-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>524288</resources-maximum>
        </security-profile-information>
    </security-profile-flow-gate-information>
        """

        self.response["SA_HE_FLOW_GATE_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0           0      524288
        """

        self.response["SA_HE_FLOW_SESSION"] = """
    <security-profile-flow-session-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>4</resources-used>
            <resources-reserved>25000</resources-reserved>
            <resources-maximum>50000</resources-maximum>
        </security-profile-information>
    </security-profile-flow-session-information>
        """

        self.response["SA_HE_FLOW_SESSION_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         4       25000       50000
        """

        self.response["SA_HE_AUTH_ENTRY"] = """
    <security-profile-auth-entry-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>50000</resources-maximum>
        </security-profile-information>
    </security-profile-auth-entry-information>
        """

        self.response["SA_HE_AUTH_ENTRY_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0           0       50000
        """

        self.response["SA_HE_DSLITE_SOFTWIRE_INITIATOR"] = """
    <security-profile-dslite-softwire-initiator-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>100000</resources-maximum>
        </security-profile-information>
    </security-profile-dslite-softwire-initiator-information>
        """

        self.response["SA_HE_DSLITE_SOFTWIRE_INITIATOR_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0           0      100000
        """

        self.response["SA_HE_POLICY"] = """
    <security-profile-policy-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>100</resources-reserved>
            <resources-maximum>200</resources-maximum>
        </security-profile-information>
    </security-profile-policy-information>
        """

        self.response["SA_HE_POLICY_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0         100         200
        """

        self.response["SA_HE_POLICY_WITH_COUNT"] = """
    <security-profile-policy-with-count-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>1024</resources-maximum>
        </security-profile-information>
    </security-profile-policy-with-count-information>
    """

        self.response["SA_HE_POLICY_WITH_COUNT_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0           0        1024
        """

        self.response["SA_HE_SCHEDULER"] = """
    <security-profile-scheduler-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>256</resources-maximum>
        </security-profile-information>
    </security-profile-scheduler-information>
        """

        self.response["SA_HE_SCHEDULER_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         0           0         256
        """

        self.response["SA_HE_ZONE"] = """
    <security-profile-zone-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>SP-root</security-profile-name>
            <resources-used>3</resources-used>
            <resources-reserved>50</resources-reserved>
            <resources-maximum>60</resources-maximum>
        </security-profile-information>
    </security-profile-zone-information>
        """

        self.response["SA_HE_ZONE_TEXT"] = """
logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   SP-root                         3           5          60
        """

        self.response["HA_HE_NAT_CONE_BINDING"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-cone-binding-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>2097152</resources-maximum>
                </security-profile-information>
            </security-profile-nat-cone-binding-information>
        </multi-routing-engine-item>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <security-profile-nat-cone-binding-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>2097152</resources-maximum>
                </security-profile-information>
            </security-profile-nat-cone-binding-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["SA_LE_NAT_CONE_BINDING"] = """
    <security-profile-nat-cone-binding-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1D0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>Default-Profile</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>0</resources-maximum>
        </security-profile-information>
    </security-profile-nat-cone-binding-information>
        """

        self.response["SA_HE_NAT_CONE_BINDING_MULTI_LSYS"] = """
    <security-profile-nat-cone-binding-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>Default-Profile</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>2097152</resources-maximum>
        </security-profile-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>LSYS1</logical-system-name>
            <security-profile-name>SP1</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>2097152</resources-maximum>
        </security-profile-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/17.4I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>LSYS2</logical-system-name>
            <security-profile-name>SP2</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>2097152</resources-maximum>
        </security-profile-information>
    </security-profile-nat-cone-binding-information>
        """

        self.response["HA_HE_NAT_CONE_BINDING_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum

root-logical-system   Default-Profile                 0           0     2097152
        """

        self.response["SA_HE_NAT_DESTINATION_POOL"] = """
    <security-profile-nat-destination-pool-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>Default-Profile</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>8192</resources-maximum>
        </security-profile-information>
    </security-profile-nat-destination-pool-information>
        """

        self.response["HA_HE_NAT_DESTINATION_POOL"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-destination-pool-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>8192</resources-maximum>
                </security-profile-information>
            </security-profile-nat-destination-pool-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_DESTINATION_POOL_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum

root-logical-system   Default-Profile                 0           0        8192
        """

        self.response["HA_HE_NAT_DESTINATION_POOL_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-destination-pool-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>8192</resources-maximum>
                    <resources-available>8192</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-destination-pool-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_DESTINATION_RULE_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-destination-rule-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>8192</resources-maximum>
                    <resources-available>8192</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-destination-rule-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_DESTINATION_RULE_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   Default-Profile                 0           0        8192
        """

        self.response["HA_HE_NAT_INTERFACE_PORT_OL"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-interface-po-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>64</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>32</resources-maximum>
                </security-profile-information>
            </security-profile-nat-interface-po-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_INTERFACE_PORT_OL_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-interface-po-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>64</resources-used>
                    <resources-maximum>128</resources-maximum>
                    <resources-available>64</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>64</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>64</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-interface-po-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_INTERFACE_PORT_OL_SUMMARY_TEXT"] = """
node0:
--------------------------------------------------------------------------

global used amount      : 64
global maximum quota    : 128
global available amount : 64
total logical systems   : 1
total security profiles : 1
heaviest usage / user   : 64    / root-logical-system
lightest usage / user   : 64    / root-logical-system
        """

        self.response["HA_HE_NAT_NOPAT_ADDRESS"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-nopat-address-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>1048576</resources-maximum>
                </security-profile-information>
            </security-profile-nat-nopat-address-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_NOPAT_ADDRESS_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-nopat-address-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>1048576</resources-maximum>
                    <resources-available>1048576</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-nopat-address-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_NOPAT_ADDRESS_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   Default-Profile                 0           0     1048576
        """

        self.response["HA_HE_NAT_PAT_ADDRESS"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-pat-address-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>8192</resources-maximum>
                </security-profile-information>
            </security-profile-nat-pat-address-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_PAT_ADDRESS_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-pat-address-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>8192</resources-maximum>
                    <resources-available>8192</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-pat-address-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_PAT_ADDRESS_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   Default-Profile                 0           0        8192
        """

        self.response["HA_HE_NAT_PORT_OL_IPNUMBER"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-port-ol-ipnumber-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>2</resources-maximum>
                </security-profile-information>
            </security-profile-nat-port-ol-ipnumber-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_PORT_OL_IPNUMBER_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-port-ol-ipnumber-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>2</resources-maximum>
                    <resources-available>2</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-port-ol-ipnumber-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_PORT_OL_IPNUMBER_TEXT"] = """
node0:
--------------------------------------------------------------------------

global used amount      : 0
global maximum quota    : 2
global available amount : 2
total logical systems   : 1
total security profiles : 1
heaviest usage / user   : 0     / root-logical-system
lightest usage / user   : 0     / root-logical-system
        """

        self.response["HA_HE_NAT_RULE_REFERENCED_PREFIX"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-rule-referenced-prefix-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>1048576</resources-maximum>
                </security-profile-information>
            </security-profile-nat-rule-referenced-prefix-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_RULE_REFERENCED_PREFIX_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-rule-referenced-prefix-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>1048576</resources-maximum>
                    <resources-available>1048576</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-rule-referenced-prefix-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_RULE_REFERENCED_PREFIX_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   Default-Profile                 0           0     1048576
        """

        self.response["HA_HE_NAT_SOURCE_POOL"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-source-pool-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>8192</resources-maximum>
                </security-profile-information>
            </security-profile-nat-source-pool-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_SOURCE_POOL_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-source-pool-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>8192</resources-maximum>
                    <resources-available>8192</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-source-pool-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_SOURCE_POOL_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   Default-Profile                 0           0        8192
        """

        self.response["HA_HE_NAT_SOURCE_RULE"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-source-rule-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>8192</resources-maximum>
                </security-profile-information>
            </security-profile-nat-source-rule-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
    """
        self.response["HA_HE_NAT_SOURCE_RULE_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-source-rule-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>8192</resources-maximum>
                    <resources-available>8192</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-source-rule-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """
        self.response["HA_HE_NAT_SOURCE_RULE_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   Default-Profile                 0           0        8192
        """

        self.response["HA_HE_NAT_STATIC_RULE"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-static-rule-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>8192</resources-maximum>
                </security-profile-information>
            </security-profile-nat-static-rule-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_STATIC_RULE_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-static-rule-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>8192</resources-maximum>
                    <resources-available>8192</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-static-rule-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_HE_NAT_STATIC_RULE_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum   feature

root-logical-system   Default-Profile                 0           0        8192
        """

        self.response["HA_LE_NAT_PAT_PORTNUM"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-pat-portnum-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-securityprofile" junos:style="terse">
                    <logical-system-name>root-logical-system</logical-system-name>
                    <security-profile-name>Default-Profile</security-profile-name>
                    <resources-used>0</resources-used>
                    <resources-reserved>0</resources-reserved>
                    <resources-maximum>201326592</resources-maximum>
                </security-profile-information>
            </security-profile-nat-pat-portnum-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_LE_NAT_PAT_PORTNUM_SUMMARY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node0</re-name>

            <security-profile-nat-pat-portnum-information>
                <security-profile-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-securityprofile" junos:style="summary">
                    <resources-used>0</resources-used>
                    <resources-maximum>201326592</resources-maximum>
                    <resources-available>201326592</resources-available>
                    <total-logical-systems>1</total-logical-systems>
                    <total-profiles>1</total-profiles>
                    <heaviest-usage>0</heaviest-usage>
                    <heaviest-user>root-logical-system</heaviest-user>
                    <lightest-usage>0</lightest-usage>
                    <lightest-user>root-logical-system</lightest-user>
                </security-profile-information>
            </security-profile-nat-pat-portnum-information>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["HA_LE_NAT_PAT_PORTNUM_TEXT"] = """
node0:
--------------------------------------------------------------------------

logical system name   security profile name       usage    reserved     maximum

root-logical-system   Default-Profile                 0           0   201326592
        """

        self.response["SA_LE_LOG_STREAM_NUMBER"] = """
    <security-profile-security-log-stream-num-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>root-logical-system</logical-system-name>
            <security-profile-name>Default-Profile</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>3</resources-maximum>
        </security-profile-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-securityprofile" junos:style="terse">
            <logical-system-name>LSYS1</logical-system-name>
            <security-profile-name>null</security-profile-name>
            <resources-used>0</resources-used>
            <resources-reserved>0</resources-reserved>
            <resources-maximum>0</resources-maximum>
        </security-profile-information>
    </security-profile-security-log-stream-num-information>
        """

        self.response["SA_LE_LOG_STREAM_NUMBER_SUMMARY"] = """
    <security-profile-security-log-stream-num-information>
        <security-profile-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-securityprofile" junos:style="summary">
            <resources-used>0</resources-used>
            <resources-maximum>32</resources-maximum>
            <resources-available>32</resources-available>
            <total-logical-systems>2</total-logical-systems>
            <total-profiles>0</total-profiles>
            <heaviest-usage>0</heaviest-usage>
            <heaviest-user>root-logical-system ...(2 logical systems)</heaviest-user>
            <lightest-usage>0</lightest-usage>
            <lightest-user>root-logical-system ...(2 logical systems)</lightest-user>
        </security-profile-information>
    </security-profile-security-log-stream-num-information>
        """

        self.response["SA_LE_LOG_STREAM_NUMBER_TEXT"] = """
global used amount      : 0
global maximum quota    : 32
global available amount : 32
total logical systems   : 2
total security profiles : 0
heaviest usage / user   : 0     / root-logical-system ...(2 logical systems)
lightest usage / user   : 0     / root-logical-system ...(2 logical systems)
        """

    def tearDown(self):
        """teardown after all case"""
        pass

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_address_book(self, mock_execute_cli_command_on_device):
        """checking get address book"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_ADDRESS_BOOK"])
        response = self.ins.get_address_book(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "4000")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_ADDRESS_BOOK_TEXT"]
        response = self.ins.get_address_book(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_appfw_profile(self, mock_execute_cli_command_on_device):
        """checking get appfw profile"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_APPFW_PROFILE"])
        response = self.ins.get_appfw_profile(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "57344")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_APPFW_PROFILE_TEXT"]
        response = self.ins.get_appfw_profile(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_appfw_rule(self, mock_execute_cli_command_on_device):
        """checking get appfw rule"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_APPFW_RULE"])
        response = self.ins.get_appfw_rule(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "114688")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_APPFW_RULE_TEXT"]
        response = self.ins.get_appfw_rule(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_appfw_rule_set(self, mock_execute_cli_command_on_device):
        """checking get appfw rule set"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_APPFW_RULE_SET"])
        response = self.ins.get_appfw_rule_set(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "57344")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_APPFW_RULE_SET_TEXT"]
        response = self.ins.get_appfw_rule_set(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_auth_entry(self, mock_execute_cli_command_on_device):
        """checking get auth entry"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_AUTH_ENTRY"])
        response = self.ins.get_auth_entry(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "50000")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_AUTH_ENTRY_TEXT"]
        response = self.ins.get_auth_entry(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_dslite_softwire_initiator(self, mock_execute_cli_command_on_device):
        """checking get dslite softwire initiator"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_DSLITE_SOFTWIRE_INITIATOR"])
        response = self.ins.get_dslite_softwire_initiator(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "100000")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_DSLITE_SOFTWIRE_INITIATOR_TEXT"]
        response = self.ins.get_dslite_softwire_initiator(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_flow_gate(self, mock_execute_cli_command_on_device):
        """checking get flow gate"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_FLOW_GATE"])
        response = self.ins.get_flow_gate(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "524288")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_FLOW_GATE_TEXT"]
        response = self.ins.get_flow_gate(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_flow_session(self, mock_execute_cli_command_on_device):
        """checking get flow session"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_FLOW_SESSION"])
        response = self.ins.get_flow_session(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "50000")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_FLOW_SESSION_TEXT"]
        response = self.ins.get_flow_session(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_cone_binding(self, mock_execute_cli_command_on_device):
        """checking get nat cone binding"""
        print("SA LE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_NAT_CONE_BINDING"])
        response = self.ins.get_nat_cone_binding(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")

        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_CONE_BINDING"])
        response = self.ins.get_nat_cone_binding(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 2)
        self.assertIn("re_name", response[0])
        self.assertIn("re_name", response[1])

        print("SA HE setup with multiple LSYS entities")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_NAT_CONE_BINDING_MULTI_LSYS"])
        response = self.ins.get_nat_cone_binding(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 3)
        for item in response:
            self.assertIn("resources_maximum", item)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[1]["logical_system_name"], "LSYS1")
        self.assertEqual(response[2]["logical_system_name"], "LSYS2")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_CONE_BINDING_TEXT"]
        response = self.ins.get_nat_cone_binding(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_destination_pool(self, mock_execute_cli_command_on_device):
        """checking get nat destination pool"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_NAT_DESTINATION_POOL"])
        response = self.ins.get_nat_destination_pool(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")

        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_DESTINATION_POOL"])
        response = self.ins.get_nat_destination_pool(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_maximum"], "8192")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_DESTINATION_POOL_TEXT"]
        response = self.ins.get_nat_destination_pool(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_destination_rule(self, mock_execute_cli_command_on_device):
        """checking get nat destination rule"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_DESTINATION_RULE_SUMMARY"])
        response = self.ins.get_nat_destination_rule(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["heaviest_user"], "root-logical-system")
        self.assertEqual(response[0]["resources_available"], "8192")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_DESTINATION_RULE_TEXT"]
        response = self.ins.get_nat_destination_rule(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_interface_port_ol(self, mock_execute_cli_command_on_device):
        """checking get nat interface port ol"""
        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_INTERFACE_PORT_OL"])
        response = self.ins.get_nat_interface_port_ol(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")

        print("HA HE setup with SUMMARY response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_INTERFACE_PORT_OL_SUMMARY"])
        response = self.ins.get_nat_interface_port_ol(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_used"], "64")
        self.assertEqual(response[0]["resources_maximum"], "128")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_INTERFACE_PORT_OL_SUMMARY_TEXT"]
        response = self.ins.get_nat_interface_port_ol(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_nopat_address(self, mock_execute_cli_command_on_device):
        """checking get nat nopat address"""
        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_NOPAT_ADDRESS"])
        response = self.ins.get_nat_nopat_address(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")
        self.assertEqual(response[0]["resources_maximum"], "1048576")

        print("HA HE setup with SUMMARY response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_NOPAT_ADDRESS_SUMMARY"])
        response = self.ins.get_nat_nopat_address(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_used"], "0")
        self.assertEqual(response[0]["resources_available"], "1048576")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_NOPAT_ADDRESS_TEXT"]
        response = self.ins.get_nat_nopat_address(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_pat_address(self, mock_execute_cli_command_on_device):
        """checking get nat pat address"""
        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_PAT_ADDRESS"])
        response = self.ins.get_nat_pat_address(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")
        self.assertEqual(response[0]["resources_maximum"], "8192")

        print("HA HE setup with SUMMARY response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_PAT_ADDRESS_SUMMARY"])
        response = self.ins.get_nat_pat_address(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_used"], "0")
        self.assertEqual(response[0]["resources_available"], "8192")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_PAT_ADDRESS_TEXT"]
        response = self.ins.get_nat_pat_address(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_pat_portnum(self, mock_execute_cli_command_on_device):
        """checking get nat pat portn"""
        print("HA LE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_NAT_PAT_PORTNUM"])
        response = self.ins.get_nat_pat_portnum(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")
        self.assertEqual(response[0]["resources_maximum"], "201326592")

        print("HA HE setup with SUMMARY response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_NAT_PAT_PORTNUM_SUMMARY"])
        response = self.ins.get_nat_pat_portnum(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_used"], "0")
        self.assertEqual(response[0]["resources_available"], "201326592")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_LE_NAT_PAT_PORTNUM_TEXT"]
        response = self.ins.get_nat_pat_portnum(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_port_ol_ipnumber(self, mock_execute_cli_command_on_device):
        """checking get nat port ol ipnumber"""
        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_PORT_OL_IPNUMBER"])
        response = self.ins.get_nat_port_ol_ipnumber(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")
        self.assertEqual(response[0]["resources_maximum"], "2")

        print("HA HE setup with SUMMARY response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_PORT_OL_IPNUMBER_SUMMARY"])
        response = self.ins.get_nat_port_ol_ipnumber(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_used"], "0")
        self.assertEqual(response[0]["resources_available"], "2")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_PORT_OL_IPNUMBER_TEXT"]
        response = self.ins.get_nat_port_ol_ipnumber(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_rule_referenced_prefix(self, mock_execute_cli_command_on_device):
        """checking get nat port ol ipnumber"""
        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_RULE_REFERENCED_PREFIX"])
        response = self.ins.get_nat_rule_referenced_prefix(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")
        self.assertEqual(response[0]["resources_maximum"], "1048576")

        print("HA HE setup with SUMMARY response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_RULE_REFERENCED_PREFIX_SUMMARY"])
        response = self.ins.get_nat_rule_referenced_prefix(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_used"], "0")
        self.assertEqual(response[0]["resources_available"], "1048576")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_RULE_REFERENCED_PREFIX_TEXT"]
        response = self.ins.get_nat_rule_referenced_prefix(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_source_pool(self, mock_execute_cli_command_on_device):
        """checking get nat port ol ipnumber"""
        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_SOURCE_POOL"])
        response = self.ins.get_nat_source_pool(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")
        self.assertEqual(response[0]["resources_maximum"], "8192")

        print("HA HE setup with SUMMARY response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_SOURCE_POOL_SUMMARY"])
        response = self.ins.get_nat_source_pool(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_used"], "0")
        self.assertEqual(response[0]["resources_available"], "8192")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_SOURCE_POOL_TEXT"]
        response = self.ins.get_nat_source_pool(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_source_rule(self, mock_execute_cli_command_on_device):
        """checking get nat port ol ipnumber"""
        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_SOURCE_RULE"])
        response = self.ins.get_nat_source_rule(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")
        self.assertEqual(response[0]["resources_maximum"], "8192")

        print("HA HE setup with SUMMARY response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_SOURCE_RULE_SUMMARY"])
        response = self.ins.get_nat_source_rule(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_used"], "0")
        self.assertEqual(response[0]["resources_available"], "8192")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_SOURCE_RULE_TEXT"]
        response = self.ins.get_nat_source_rule(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_nat_static_rule(self, mock_execute_cli_command_on_device):
        """checking get nat port ol ipnumber"""
        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_STATIC_RULE"])
        response = self.ins.get_nat_static_rule(device=self.mock_device_ins, more_options="logical-system LSYS1", timeout=30)
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "Default-Profile")
        self.assertEqual(response[0]["resources_maximum"], "8192")

        print("HA HE setup with SUMMARY response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_STATIC_RULE_SUMMARY"])
        response = self.ins.get_nat_static_rule(device=self.mock_device_ins)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertIn("re_name", response[0])
        self.assertEqual(response[0]["resources_used"], "0")
        self.assertEqual(response[0]["resources_available"], "8192")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["HA_HE_NAT_STATIC_RULE_TEXT"]
        response = self.ins.get_nat_static_rule(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_policy(self, mock_execute_cli_command_on_device):
        """checking get policy"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_POLICY"])
        response = self.ins.get_policy(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "200")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_POLICY_TEXT"]
        response = self.ins.get_policy(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_policy_with_count(self, mock_execute_cli_command_on_device):
        """checking get policy with count"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_POLICY_WITH_COUNT"])
        response = self.ins.get_policy_with_count(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "1024")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_POLICY_WITH_COUNT_TEXT"]
        response = self.ins.get_policy_with_count(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_scheduler(self, mock_execute_cli_command_on_device):
        """checking get scheduler"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_SCHEDULER"])
        response = self.ins.get_scheduler(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "256")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_SCHEDULER_TEXT"]
        response = self.ins.get_scheduler(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_security_log_stream_number(self, mock_execute_cli_command_on_device):
        """checking get security log stream number"""
        print("SA LE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_LOG_STREAM_NUMBER"])
        response = self.ins.get_security_log_stream_number(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[1]["logical_system_name"], "LSYS1")
        self.assertEqual(response[1]["security_profile_name"], "null")
        self.assertEqual(response[1]["resources_maximum"], "0")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_LE_LOG_STREAM_NUMBER_TEXT"]
        response = self.ins.get_security_log_stream_number(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_zone(self, mock_execute_cli_command_on_device):
        """checking get zone"""
        print("SA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_ZONE"])
        response = self.ins.get_zone(device=self.mock_device_ins, more_options="summary")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0]["logical_system_name"], "root-logical-system")
        self.assertEqual(response[0]["security_profile_name"], "SP-root")
        self.assertEqual(response[0]["resources_maximum"], "60")

        print("TEXT response")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_ZONE_TEXT"]
        response = self.ins.get_zone(device=self.mock_device_ins, return_mode="text")
        self.assertIsInstance(response, str)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_address_book(self, mock_execute_cli_command_on_device):
        """checking search address book"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_ADDRESS_BOOK"])
        response = self.ins.search_address_book(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="4000 eq",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_appfw_profile(self, mock_execute_cli_command_on_device):
        """checking search appfw profile"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_APPFW_PROFILE"])
        response = self.ins.search_appfw_profile(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="0-57344 in",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_appfw_rule(self, mock_execute_cli_command_on_device):
        """checking search appfw rule"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_APPFW_RULE"])
        response = self.ins.search_appfw_rule(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="114688",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_appfw_rule_set(self, mock_execute_cli_command_on_device):
        """checking search appfw rule set"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_APPFW_RULE_SET"])
        response = self.ins.search_appfw_rule_set(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="0-57344 in",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

        print("HA HE setup not match response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_APPFW_RULE_SET"])
        response = self.ins.search_appfw_rule_set(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="0",
            security_profile_name="SP in",
        )
        self.assertFalse(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_auth_entry(self, mock_execute_cli_command_on_device):
        """checking search auth entry"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_AUTH_ENTRY"])
        response = self.ins.search_auth_entry(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="50000 eq",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_dslite_softwire_initiator(self, mock_execute_cli_command_on_device):
        """checking search auth entry"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_DSLITE_SOFTWIRE_INITIATOR"])
        response = self.ins.search_dslite_softwire_initiator(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="100000 eq",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_flow_gate(self, mock_execute_cli_command_on_device):
        """checking search flow gate"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_FLOW_GATE"])
        response = self.ins.search_flow_gate(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="524288 eq",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_flow_session(self, mock_execute_cli_command_on_device):
        """checking search flow session"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_FLOW_SESSION"])
        response = self.ins.search_flow_session(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=4,
            resources_reserved=25000,
            resources_maximum="50000 eq",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_policy(self, mock_execute_cli_command_on_device):
        """checking search flow policy"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_POLICY"])
        response = self.ins.search_policy(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=100,
            resources_maximum="200 eq",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_policy_with_count(self, mock_execute_cli_command_on_device):
        """checking search flow policy with count"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_POLICY_WITH_COUNT"])
        response = self.ins.search_policy_with_count(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="1024 eq",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_scheduler(self, mock_execute_cli_command_on_device):
        """checking search flow scheduler"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_SCHEDULER"])
        response = self.ins.search_scheduler(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=0,
            resources_reserved=0,
            resources_maximum="256 eq",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_zone(self, mock_execute_cli_command_on_device):
        """checking search flow zone"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_ZONE"])
        response = self.ins.search_zone(
            device=self.mock_device_ins,
            logical_system_name=["root", "in"],
            resources_used=3,
            resources_reserved=50,
            resources_maximum="60 eq",
            security_profile_name="SP in",
        )
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_cone_binding(self, mock_execute_cli_command_on_device):
        """checking search nat cone binding"""
        print("SA LE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_NAT_CONE_BINDING"])
        response = self.ins.search_nat_cone_binding(
            device=self.mock_device_ins,
            logical_system_name="root in",
            security_profile_name="Default-Profile",
            resources_used="0-10 in",
            resources_reserved=("0-10", "in"),
            resources_maximum=0,
        )
        self.assertTrue(response)

        print("HA HE setup with normal response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_CONE_BINDING"])
        response = self.ins.search_nat_cone_binding(
            device=self.mock_device_ins,
            return_mode="counter",
            logical_system_name="root in",
            security_profile_name="Default-Profile",
            resources_used="0-10 in",
            resources_reserved=("0-10", "in"),
            resources_maximum=2097152,
            re_name="node0",
        )
        self.assertEqual(response, 1)

        print("search from previous result")
        response = self.ins.search_nat_cone_binding(
            device=self.mock_device_ins,
            return_mode="counter",
            match_from_previous_response=True,
            logical_system_name="root in",
            security_profile_name="Default-Profile",
            resources_used="0-10 in",
            resources_reserved=("0-10", "in"),
            resources_maximum=2097152,
        )
        self.assertEqual(response, 2)

        print("search from multiple LSYS")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_NAT_CONE_BINDING_MULTI_LSYS"])
        response = self.ins.search_nat_cone_binding(
            device=self.mock_device_ins,
            return_mode="counter",
            logical_system_name="LSYS in",
            security_profile_name="SP2",
            resources_used="0-10 in",
            resources_reserved="0",
            resources_maximum=2097152,
        )
        self.assertEqual(response, 1)

        print("invalid option checking")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_NAT_CONE_BINDING"])
        response = self.ins.search_nat_cone_binding(
            device=self.mock_device_ins,
            unknown_option="root in",
        )
        self.assertFalse(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_destination_pool(self, mock_execute_cli_command_on_device):
        """checking search nat destination pool"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_DESTINATION_POOL_SUMMARY"])
        response = self.ins.search_nat_destination_pool(
            device=self.mock_device_ins,
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=8192,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertTrue(response)

        print("SA LE setup search by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_HE_NAT_DESTINATION_POOL"])
        response = self.ins.search_nat_destination_pool(
            device=self.mock_device_ins,
            return_mode="counter",
            security_profile_name="Default-Profile",
            resources_maximum=8192,
            resources_used=0,
            resources_reserved=0,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_destination_rule(self, mock_execute_cli_command_on_device):
        """checking search nat destination rule"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_DESTINATION_RULE_SUMMARY"])
        response = self.ins.search_nat_destination_rule(
            device=self.mock_device_ins,
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=8192,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertTrue(response)

        print("SA LE setup search by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_DESTINATION_RULE_SUMMARY"])
        response = self.ins.search_nat_destination_rule(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=8192,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_interface_port_ol(self, mock_execute_cli_command_on_device):
        """checking search nat interface port ol"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_INTERFACE_PORT_OL"])
        response = self.ins.search_nat_interface_port_ol(
            device=self.mock_device_ins,
            re_name="node0",
            resources_maximum=32,
            resources_used=64,
        )
        self.assertTrue(response)

        print("HA_HE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_INTERFACE_PORT_OL_SUMMARY"])
        response = self.ins.search_nat_interface_port_ol(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=128,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_nopat_address(self, mock_execute_cli_command_on_device):
        """checking search nat nopat address"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_NOPAT_ADDRESS"])
        response = self.ins.search_nat_nopat_address(
            device=self.mock_device_ins,
            re_name="node0",
            resources_maximum="10000-10485760 in",
            resources_used=0,
        )
        self.assertTrue(response)

        print("HA_HE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_NOPAT_ADDRESS_SUMMARY"])
        response = self.ins.search_nat_nopat_address(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=1048576,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_pat_address(self, mock_execute_cli_command_on_device):
        """checking search nat pat address"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_PAT_ADDRESS"])
        response = self.ins.search_nat_pat_address(
            device=self.mock_device_ins,
            re_name="node0",
            resources_maximum="8192",
            resources_used=0,
        )
        self.assertTrue(response)

        print("HA_HE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_PAT_ADDRESS_SUMMARY"])
        response = self.ins.search_nat_pat_address(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=8192,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_pat_portnum(self, mock_execute_cli_command_on_device):
        """checking search nat pat port"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_NAT_PAT_PORTNUM"])
        response = self.ins.search_nat_pat_portnum(
            device=self.mock_device_ins,
            re_name="node0",
            resources_maximum="201326592",
            resources_used=0,
        )
        self.assertTrue(response)

        print("HA_HE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_LE_NAT_PAT_PORTNUM_SUMMARY"])
        response = self.ins.search_nat_pat_portnum(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=201326592,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_port_ol_ipnumber(self, mock_execute_cli_command_on_device):
        """checking search nat pat address"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_PORT_OL_IPNUMBER"])
        response = self.ins.search_nat_port_ol_ipnumber(
            device=self.mock_device_ins,
            re_name="node0",
            resources_maximum="2",
            resources_used=0,
        )
        self.assertTrue(response)

        print("HA_HE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_PORT_OL_IPNUMBER_SUMMARY"])
        response = self.ins.search_nat_port_ol_ipnumber(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=2,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_rule_referenced_prefix(self, mock_execute_cli_command_on_device):
        """checking search nat rule referenced prefix"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_RULE_REFERENCED_PREFIX"])
        response = self.ins.search_nat_rule_referenced_prefix(
            device=self.mock_device_ins,
            re_name="node0",
            resources_maximum="1048576",
            resources_used=0,
        )
        self.assertTrue(response)

        print("HA_HE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_RULE_REFERENCED_PREFIX_SUMMARY"])
        response = self.ins.search_nat_rule_referenced_prefix(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=1048576,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_source_pool(self, mock_execute_cli_command_on_device):
        """checking search nat source pool"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_SOURCE_POOL"])
        response = self.ins.search_nat_source_pool(
            device=self.mock_device_ins,
            re_name="node0",
            resources_maximum="8192",
            resources_used=0,
        )
        self.assertTrue(response)

        print("HA_HE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_SOURCE_POOL_SUMMARY"])
        response = self.ins.search_nat_source_pool(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=8192,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_source_rule(self, mock_execute_cli_command_on_device):
        """checking search nat source rule"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_SOURCE_RULE"])
        response = self.ins.search_nat_source_rule(
            device=self.mock_device_ins,
            re_name="node0",
            resources_maximum="8192",
            resources_used=0,
        )
        self.assertTrue(response)

        print("HA_HE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_SOURCE_RULE_SUMMARY"])
        response = self.ins.search_nat_source_rule(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=8192,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_nat_static_rule(self, mock_execute_cli_command_on_device):
        """checking search nat static rule"""
        print("HA HE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_STATIC_RULE"])
        response = self.ins.search_nat_static_rule(
            device=self.mock_device_ins,
            re_name="node0",
            resources_maximum="8192",
            resources_used=0,
        )
        self.assertTrue(response)

        print("HA_HE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_HE_NAT_STATIC_RULE_SUMMARY"])
        response = self.ins.search_nat_static_rule(
            device=self.mock_device_ins,
            return_mode="counter",
            re_name="node0",
            lightest_user=["root", "in"],
            resources_maximum=8192,
            total_profiles="1",
            total_logical_systems=1,
        )
        self.assertEqual(response, 1)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_security_log_stream_number(self, mock_execute_cli_command_on_device):
        """checking search security log stream number"""
        print("SA LE setup with summary response")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_LOG_STREAM_NUMBER"])
        response = self.ins.search_security_log_stream_number(
            device=self.mock_device_ins,
            security_profile_name="Default-Profile",
            resources_maximum="3",
            resources_used=0,
        )
        self.assertTrue(response)

        print("SA LE setup with summary by counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["SA_LE_LOG_STREAM_NUMBER_SUMMARY"])
        response = self.ins.search_security_log_stream_number(
            device=self.mock_device_ins,
            return_mode="counter",
            lightest_user=["root", "in"],
            resources_maximum=32,
            total_profiles="0",
            total_logical_systems=2,
        )
        self.assertEqual(response, 1)
