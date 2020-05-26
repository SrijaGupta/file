import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.utils.junos import verification_unchained
from jnpr.toby.hldcl.juniper.security.srx import Srx


class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()
    xml1 = """<rpc-reply xmlns:junos="http://xml.juniper.net/junos/12.1X46/junos">
    <static-nat-rule-information xmlns="http://xml.juniper.net/junos/12.1X46/junos-nat">
        <static-nat-rule-entry junos:style="with-pat">
            <rule-name>rule1</rule-name>
            <rule-set-name>rst1</rule-set-name>
            <rule-id>1</rule-id>
            <rule-matching-position>1</rule-matching-position>
            <rule-from-context>interface</rule-from-context>
            <rule-from-context-name>ge-1/0/2.0</rule-from-context-name>
            <static-source-address-range-entry>
                <rule-source-address-low-range>20.20.20.2</rule-source-address-low-range>
                <rule-source-address-high-range>20.20.20.2</rule-source-address-high-range>
                <rule-source-address-low-range>20.20.20.16</rule-source-address-low-range>
                <rule-source-address-high-range>20.20.20.19</rule-source-address-high-range>
            </static-source-address-range-entry>
            <static-source-port-entry>
            </static-source-port-entry>
            <rule-destination-address-prefix>20.20.20.200</rule-destination-address-prefix>
            <rule-destination-port-low>8080</rule-destination-port-low>
            <rule-destination-port-high>8080</rule-destination-port-high>
            <rule-host-address-prefix>10.10.10.200</rule-host-address-prefix>
            <rule-host-port-low>80</rule-host-port-low>
            <rule-host-port-high>80</rule-host-port-high>
            <rule-address-netmask>32</rule-address-netmask>
            <rule-host-routing-instance>N/A</rule-host-routing-instance>
            <rule-translation-hits>0</rule-translation-hits>
            <succ-hits>0</succ-hits>
            <concurrent-hits>0</concurrent-hits>
        </static-nat-rule-entry>
    </static-nat-rule-information>
    <cli>
    <banner></banner>
    </cli>
</rpc-reply>"""
    xml = """<rpc-reply>
     <ipsec-security-associations-information>
         <ipsec-security-associations-block>
             <sa-block-state>up</sa-block-state>
             <sa-tunnel-index>2</sa-tunnel-index>
             <sa-virtual-system>root</sa-virtual-system>
             <sa-vpn-name>vpn1</sa-vpn-name>
             <sa-local-gateway>25.0.134.245</sa-local-gateway>
             <sa-remote-gateway>25.0.134.241</sa-remote-gateway>
             <sa-traffic-selector-name></sa-traffic-selector-name>
             <sa-local-identity>ipv4_subnet(any:0,[0..7]=0.0.0.0/0)</sa-local-identity>
             <sa-remote-identity>ipv4_subnet(any:0,[0..7]=0.0.0.0/0)</sa-remote-identity>
             <sa-ike-version>IKEv1</sa-ike-version>
             <sa-df-bit-policy-name>
                 <sa-df-bit>clear</sa-df-bit>
                 <sa-copy-outer-dscp>Disabled</sa-copy-outer-dscp>
                 <sa-policy-name>trust-to-untrust</sa-policy-name>
                 <sa-bind-interface></sa-bind-interface>
             </sa-df-bit-policy-name>
             <sa-dev-info>
                 <sa-port>500</sa-port>
                 <sa-nego-num>1</sa-nego-num>
                 <sa-nego-fail>0</sa-nego-fail>
                 <sa-del-num>0</sa-del-num>
                 <sa-flag>0x600829</sa-flag>
             </sa-dev-info>
             <sa-ipsec-tunnel-events>
                 <sa-tunnel-event-time>Sat Apr 29 2017 19:33:03 -0700</sa-tunnel-event-time>
                 <sa-tunnel-event>IPSec SA negotiation successfully completed</sa-tunnel-event>
                 <sa-tunnel-event-num-times>1</sa-tunnel-event-num-times>
                 <sa-tunnel-event-time>Sat Apr 29 2017 19:33:03 -0700</sa-tunnel-event-time>
                 <sa-tunnel-event>IKE SA negotiation successfully completed</sa-tunnel-event>
                 <sa-tunnel-event-num-times>1</sa-tunnel-event-num-times>
                 <sa-tunnel-event-time>Sat Apr 29 2017 19:32:40 -0700</sa-tunnel-event-time>
                 <sa-tunnel-event>Tunnel is ready. Waiting for trigger event or peer to trigger negotiation</sa-tunnel-event>
                 <sa-tunnel-event-num-times>1</sa-tunnel-event-num-times>
                 <sa-tunnel-event-time>Sat Apr 29 2017 19:32:40 -0700</sa-tunnel-event-time>
                 <sa-tunnel-event>External interface's address received. Information updated</sa-tunnel-event>
                 <sa-tunnel-event-num-times>1</sa-tunnel-event-num-times>
                 <sa-tunnel-event-time>Sat Apr 29 2017 19:32:40 -0700</sa-tunnel-event-time>
                 <sa-tunnel-event>External interface's zone received. Information updated</sa-tunnel-event>                 
                 l-event-num-times>
             </sa-ipsec-tunnel-events>
             <ipsec-security-associations>
                 <sa-direction>inbound</sa-direction>
                 <sa-tunnel-index>2</sa-tunnel-index>
                 <sa-spi>b55cec75</sa-spi>
                 <sa-aux-spi>0</sa-aux-spi>
                 <sa-remote-gateway>25.0.134.241</sa-remote-gateway>
                 <sa-port>500</sa-port>
                 <sa-vpn-monitoring-state>UP</sa-vpn-monitoring-state>
                 <sa-esp-encryption-algorithm>3des/</sa-esp-encryption-algorithm>
                 <sa-hmac-algorithm>sha1</sa-hmac-algorithm>
                 <sa-hard-lifetime>Expires in 3538 seconds</sa-hard-lifetime>
                 <sa-lifesize-remaining> Unlimited</sa-lifesize-remaining>
                 <sa-soft-lifetime>Expires in 2900 seconds</sa-soft-lifetime>
                 <sa-virtual-system>root</sa-virtual-system>
                 <sa-mode>Tunnel(3 30)</sa-mode>
                 <sa-type>dynamic</sa-type>
                 <sa-state>installed</sa-state>
                 <sa-protocol>ESP</sa-protocol>
                 <sa-authentication-algorithm>hmac-sha1-96</sa-authentication-algorithm>
                 <sa-encryption-algorithm>3des-cbc</sa-encryption-algorithm>
                 <sa-anti-replay-service>counter-based enabled</sa-anti-replay-service>
                 <sa-replay-window-size>64</sa-replay-window-size>
             </ipsec-security-associations>
             <ipsec-security-associations>
                 <sa-direction>outbound</sa-direction>
                 <sa-tunnel-index>2</sa-tunnel-index>
                 <sa-spi>a26a796d</sa-spi>
                 <sa-aux-spi>0</sa-aux-spi>
                 <sa-remote-gateway>25.0.134.241</sa-remote-gateway>
                 <sa-port>500</sa-port>
                 <sa-vpn-monitoring-state>UP</sa-vpn-monitoring-state>
                 <sa-esp-encryption-algorithm>3des/</sa-esp-encryption-algorithm>
                 <sa-hmac-algorithm>sha1</sa-hmac-algorithm>
                 <sa-hard-lifetime>Expires in 3538 seconds</sa-hard-lifetime>
                 <sa-lifesize-remaining> Unlimited</sa-lifesize-remaining>
                 <sa-soft-lifetime>Expires in 2900 seconds</sa-soft-lifetime>
                 <sa-virtual-system>root</sa-virtual-system>
                 <sa-mode>Tunnel(3 30)</sa-mode>
                 <sa-type>dynamic</sa-type>
                 <sa-state>installed</sa-state>
                 <sa-protocol>ESP</sa-protocol>
                 <sa-authentication-algorithm>hmac-sha1-96</sa-authentication-algorithm>
                 <sa-encryption-algorithm>3des-cbc</sa-encryption-algorithm>
                 <sa-anti-replay-service>counter-based enabled</sa-anti-replay-service>
                 <sa-replay-window-size>64</sa-replay-window-size>
             </ipsec-security-associations>
         </ipsec-security-associations-block>
     </ipsec-security-associations-information>
     <cli>
         <banner></banner>
     </cli>
 </rpc-reply>"""

    def test_verify_values_in_hierarchy_xml(self):
        self.assertRaises(Exception, verification_unchained.verify_values_in_hierarchy_xml)
        self.assertRaises(Exception, verification_unchained.verify_values_in_hierarchy_xml, device=self.mocked_obj)
        self.assertRaises(Exception, verification_unchained.verify_values_in_hierarchy_xml, device=self.mocked_obj)
        self.assertRaises(Exception, verification_unchained.verify_values_in_hierarchy_xml, device=self.mocked_obj,
                          hierarchy='ipsec_security_associations', sa_direction='inbound')
        self.assertEquals(
            verification_unchained.verify_values_in_hierarchy_xml(cli_xml=self.xml, device=self.mocked_obj,
                                                                  hierarchy='ipsec_security_associations',
                                                                  sa_direction='inbound', sa_tunnel_index='2'), True)
        self.assertEquals(
            verification_unchained.verify_values_in_hierarchy_xml(cli_xml='show\n'+self.xml, device=self.mocked_obj,
                                                                  hierarchy='ipsec_security_associations',
                                                                  sa_direction='inbound', sa_tunnel_index='2'), True)
        self.assertEquals(
            verification_unchained.verify_values_in_hierarchy_xml(cli_xml=self.xml1, device=self.mocked_obj,
                                                                  hierarchy='static_source_address_range_entry',
                                                                  rule_source_address_low_range='20.20.20.16',
                                                                  rule_source_address_high_range='20.20.20.19'), True)
        self.assertRaises(Exception, verification_unchained.verify_values_in_hierarchy_xml, cli_xml=self.xml,
                          device=self.mocked_obj,
                          hierarchy='ipsec_security_associations',
                          sa_direction='inbound',
                          sa_tunnel_index='233')
        self.assertRaises(Exception, verification_unchained.verify_values_in_hierarchy_xml, cli_xml=self.xml,
                          device=self.mocked_obj,
                          hierarchy='ipsec_security_associations',
                          sat_direction='inbound',
                          sma_tunnel_index='233')
        self.assertRaises(Exception, verification_unchained.verify_values_in_hierarchy_xml, cli_xml=self.xml,
                          device=self.mocked_obj,
                          sa_direction='inbound',
                          sa_tunnel_index='233')
        self.assertRaises(Exception, verification_unchained.verify_values_in_hierarchy_xml, cli_xml='show\n' + self.xml,
                          device=self.mocked_obj,
                          hierarchy='ipsec_security_associations')
        self.assertRaises(Exception, verification_unchained.verify_values_in_hierarchy_xml, cli_xml='show\n' + self.xml1,
                          device=self.mocked_obj,
                          hierarchy='static_source_address_range_entry', rule_source_address_low_range='asd')

    def test_verify_values_in_cli_xml(self):
        self.assertRaises(Exception, verification_unchained.verify_values_in_cli_xml)
        self.assertRaises(Exception, verification_unchained.verify_values_in_cli_xml, device=self.mocked_obj)
        self.assertRaises(Exception, verification_unchained.verify_values_in_cli_xml, device=self.mocked_obj,
                          hierarchy=' ', abc_a=' ')
        self.assertEquals(
            verification_unchained.verify_values_in_cli_xml(cli_xml=self.xml, device=self.mocked_obj,
                                                            sa_direction='inbound', sa_tunnel_index='2'),
            True)
        self.assertEquals(
            type(verification_unchained.verify_values_in_cli_xml(cli_xml=self.xml, device=self.mocked_obj, return_output=True,
                                                            sa_direction='inbound', sa_tunnel_index='2')),
            dict)
        self.assertRaises(Exception,
            verification_unchained.verify_values_in_cli_xml, cli_xml=self.xml, device=self.mocked_obj,
                                                            sa_direction='abcf')
        self.assertRaises(Exception,
                          verification_unchained.verify_values_in_cli_xml, cli_xml=self.xml, device=self.mocked_obj,
                          a_direction='abcf')
        self.assertRaises(Exception,
                          verification_unchained.verify_values_in_cli_xml, cli_xml=self.xml, device=self.mocked_obj,
                          hierarchy='66', a_direction='abcf')
        self.assertRaises(Exception,
                          verification_unchained.verify_values_in_cli_xml, cli_xml=self.xml, device=self.mocked_obj,
                          sa_block_state='abcf')
        self.assertEquals(
            verification_unchained.verify_values_in_cli_xml(cli_xml=self.xml, device=self.mocked_obj,
                                                            sa_block_state='up'),
            True)
        self.assertEquals(
            verification_unchained.verify_values_in_cli_xml(cli_xml=self.xml1, device=self.mocked_obj,
                                                            rule_source_address_low_range='20.20.20.2'),
            True)
        self.assertRaises(Exception,
                          verification_unchained.verify_values_in_cli_xml, cli_xml=self.xml1, device=self.mocked_obj,
                          rule_source_address_low_range='asd')
        self.mocked_obj.cli = MagicMock(return_value=Response(self.xml))
        self.assertEquals(
            verification_unchained.verify_values_in_cli_xml(cli=' ', device=self.mocked_obj,
                                                            sa_block_state='up'),
            True)

if __name__ == '__main__':
    unittest.main()