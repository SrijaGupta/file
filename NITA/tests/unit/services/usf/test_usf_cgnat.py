#! /usr/bin/python3
#pylint: disable=protected-access
"""
Description : Unit testcases for  usf usf_cgnat.py
Company : Juniper Networks
"""
import unittest
import unittest2 as unittest
from mock import patch
from mock import MagicMock
import builtins

from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.services.usf.usf_cgnat import usf_cgnat

builtins.t = MagicMock()

class TestCgnat(unittest.TestCase):
    """
    Unit test cases for usf usf_cgnat.py
    """
    def setUp(self):
        """
        Set up for unit testcases for usf_cgnat.py
        """
        builtins.t = MagicMock() 
        builtins.t.log = MagicMock() 
        self.response = {}
        self.xml = xml_tool()
 #       builtins.t = MagicMock()
#        builtins.t.log = MagicMock()
        self.response["NAT_POOL_DETAIL"] = '''
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.2I0/junos">
          <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-nat">
            <total-source-nat-pools>
              <total-source-pools>1</total-source-pools>
            </total-source-nat-pools>
          <source-nat-pool-info-entry>
            <interface-name>vms-0/2/0</interface-name>
            <service-set-name>snat_ss1</service-set-name>
            <pool-name>MX1_CGN4_AMS4-CONE-p1</pool-name>
            <pool-id>4</pool-id>
            <routing-instance-name>default</routing-instance-name>
            <host-address-base>0.0.0.0</host-address-base>
            <source-pool-port-translation>[1024, 63487]</source-pool-port-translation>
            <source-pool-twin-port>[63488, 65535]</source-pool-twin-port>
            <port-overloading-factor>1</port-overloading-factor>
            <source-pool-address-assignment>no-paired</source-pool-address-assignment>
            <total-pool-address>254</total-pool-address>
            <address-pool-hits>10</address-pool-hits>
            <source-pool-include-boundary-address>Disable</source-pool-include-boundary-address>
            <source-pool-eim-timeout>300</source-pool-eim-timeout>
            <source-pool-mapping-timeout>300</source-pool-mapping-timeout>
            <source-pool-eif-inbound-flows-count>0</source-pool-eif-inbound-flows-count>
            <source-pool-eif-flow-limit-exceed-drops>0</source-pool-eif-flow-limit-exceed-drops>
            <source-pool-address-range>
              <address-range-low>60.1.1.1</address-range-low>
              <address-range-high>60.1.1.254</address-range-high>
              <single-port>0</single-port>
              <twin-port>0</twin-port>
            </source-pool-address-range>
            <source-pool-address-range-sum>
              <single-port-sum>0</single-port-sum>
              <twin-port-sum>0</twin-port-sum>
            </source-pool-address-range-sum>
          </source-nat-pool-info-entry>
          </source-nat-pool-detail-information>
      <cli>
        <banner></banner>
      </cli>
    </rpc-reply>

        '''
        self.response["NAT_RULE_DETAIL"] = '''
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.2I0/junos">
    <source-nat-rule-detail-information xmlns="http://xml.juniper.net/junos/18.2I0/junos-nat">
        <source-nat-rule-entry>
            <interface-name>vms-0/2/0</interface-name>
            <service-set-name>snat_ss1</service-set-name>
            <rule-name>nr1</rule-name>
            <rule-set-name>snat_rule_set1</rule-set-name>
            <rule-id>1</rule-id>
            <rule-matching-position>1</rule-matching-position>
            <rule-from-context>zone</rule-from-context>
            <rule-from-context-name>nh-snat_ss1-ZoneIn</rule-from-context-name>
            <rule-to-context>zone</rule-to-context>
            <rule-to-context-name>nh-snat_ss1-ZoneOut</rule-to-context-name>
            <source-address-range-entry>
                <rule-source-address-low-range>20.1.1.0</rule-source-address-low-range>
                <rule-source-address-high-range>20.1.1.255</rule-source-address-high-range>
            </source-address-range-entry>
            <destination-address-range-entry>
                <rule-destination-address-low-range>30.1.1.0</rule-destination-address-low-range>
                <rule-destination-address-high-range>30.1.1.255</rule-destination-address-high-range>
            </destination-address-range-entry>
            <src-nat-app-entry>
                <src-nat-application>configured</src-nat-application>
            </src-nat-app-entry>
            <source-nat-rule-action-entry>
                <source-nat-rule-action>src_pool1</source-nat-rule-action>
                <rule-source-mapping-type>N/A</rule-source-mapping-type>
            </source-nat-rule-action-entry>
            <source-nat-rule-hits-entry>
                <rule-translation-hits>13</rule-translation-hits>
                <succ-hits>13</succ-hits>
                <failed-hits>0</failed-hits>
                <concurrent-hits>0</concurrent-hits>
            </source-nat-rule-hits-entry>
        </source-nat-rule-entry>
    </source-nat-rule-detail-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        '''
        self.response["NAT_POOL"] = """  
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3D0/junos">
<source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/18.3D0/junos-nat">
        <source-nat-pool-info-entry>
            <interface-name>vms-2/3/0</interface-name>
            <service-set-name>snat_ss1</service-set-name>
            <pool-name>src_pool1</pool-name>
            <pool-id>4</pool-id>
            <host-address-base>0.0.0.0</host-address-base>
            <source-pool-port-translation>[1024, 65535]</source-pool-port-translation>
            <port-overloading-factor>1</port-overloading-factor>
            <source-pool-address-assignment>no-paired</source-pool-address-assignment>
            <total-pool-address>254</total-pool-address>
            <address-pool-hits>0</address-pool-hits>
            <source-pool-include-boundary-address>Disable</source-pool-include-boundary-address>
            <source-pool-eim-timeout>300</source-pool-eim-timeout>
            <source-pool-mapping-timeout>300</source-pool-mapping-timeout>
            <source-pool-eif-inbound-flows-count>0</source-pool-eif-inbound-flows-count>
            <source-pool-eif-flow-limit-exceed-drops>0</source-pool-eif-flow-limit-exceed-drops>
            <source-pool-address-range junos:style="without-twin-port">
                <address-range-low>60.1.1.1</address-range-low>
                <address-range-high>60.1.1.254</address-range-high>
                <single-port>0</single-port>
            </source-pool-address-range>
            <source-pool-address-range-sum>
                <single-port-sum>0</single-port-sum>
            </source-pool-address-range-sum>
            <source-pool-error-counters>
                <out-of-port-error>0</out-of-port-error>
                <out-of-addr-error>0</out-of-addr-error>
                <parity-port-error>0</parity-port-error>
                <preserve-range-error>0</preserve-range-error>
                <app-out-of-port-error>0</app-out-of-port-error>
                <app-exceed-port-limit-error>0</app-exceed-port-limit-error>
                <out-of-blk-error>0</out-of-blk-error>
                <blk-exceed-limit-error>0</blk-exceed-limit-error>
            </source-pool-error-counters>
        </source-nat-pool-info-entry>
    </source-nat-pool-detail-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""
        self.response["NAT_POOL_Des"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.4D0/junos">
    <destination-nat-pool-information xmlns="http://xml.juniper.net/junos/18.4D0/junos-nat">
        <destination-nat-pool-entry>
            <interface-name>vms-2/3/0</interface-name>
            <service-set-name>dnat_ss1</service-set-name>
            <pool-name>dst_pool1</pool-name>
            <pool-id>1</pool-id>
            <routing-instance-name></routing-instance-name>
            <total-pool-address>1</total-pool-address>
            <address-pool-hits>0</address-pool-hits>
            <pool-address-range>
                <address-range-low>30.1.1.2</address-range-low>
                <address-range-high>30.1.1.2</address-range-high>
                <address-port>0</address-port>
            </pool-address-range>
        </destination-nat-pool-entry>
    </destination-nat-pool-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""
        self.response["NAT_POOL_False"] = """ 
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3D0/junos">
    <source-nat-pool-detail-information xmlns="http://xml.juniper.net/junos/18.3D0/junos-nat">
        <source-nat-pool-info-entry>
            <interface-name>vms-1/1/1</interface-name>
            <service-set-name>snat_ss1</service-set-name>
            <pool-name>src_pool2</pool-name>
            <pool-id>4</pool-id>
            <host-address-base>0.0.0.0</host-address-base>
            <source-pool-port-translation>[1024, 65535]</source-pool-port-translation>
            <port-overloading-factor>1</port-overloading-factor>
            <source-pool-address-assignment>no-paired</source-pool-address-assignment>
            <total-pool-address>254</total-pool-address>
            <address-pool-hits>1</address-pool-hits>
            <source-pool-include-boundary-address>Disable</source-pool-include-boundary-address>
            <source-pool-eim-timeout>300</source-pool-eim-timeout>
            <source-pool-mapping-timeout>300</source-pool-mapping-timeout>
            <source-pool-eif-inbound-flows-count>0</source-pool-eif-inbound-flows-count>
            <source-pool-eif-flow-limit-exceed-drops>0</source-pool-eif-flow-limit-exceed-drops>
            <source-pool-address-range junos:style="without-twin-port">
                <address-range-low>60.1.1.1</address-range-low>
                <address-range-high>60.1.1.254</address-range-high>
                <single-port>0</single-port>
            </source-pool-address-range>
            <source-pool-address-range-sum>
                <single-port-sum>0</single-port-sum>
            </source-pool-address-range-sum>
            <source-pool-error-counters>
                <out-of-port-error>0</out-of-port-error>
                <out-of-addr-error>0</out-of-addr-error>
                <parity-port-error>0</parity-port-error>
                <preserve-range-error>0</preserve-range-error>
                <app-out-of-port-error>0</app-out-of-port-error>
                <app-exceed-port-limit-error>0</app-exceed-port-limit-error>
                <out-of-blk-error>0</out-of-blk-error>
                <blk-exceed-limit-error>0</blk-exceed-limit-error>
            </source-pool-error-counters>
        </source-nat-pool-info-entry>
    </source-nat-pool-detail-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""
        self.response["NAT_RULE"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3D0/junos">
    <source-nat-rule-detail-information xmlns="http://xml.juniper.net/junos/18.3D0/junos-nat">
        <source-nat-rule-entry>
            <interface-name>vms-2/3/0</interface-name>
            <service-set-name>snat_ss1</service-set-name>
            <rule-name>nr1</rule-name>
            <rule-set-name>snat_rule_set1</rule-set-name>
            <rule-id>1</rule-id>
            <rule-matching-position>1</rule-matching-position>
            <rule-from-context>zone</rule-from-context>
            <rule-from-context-name>snat_ss1-ZoneIn</rule-from-context-name>
            <rule-to-context>zone</rule-to-context>
            <rule-to-context-name>snat_ss1-ZoneOut</rule-to-context-name>
            <source-address-range-entry>
                <rule-source-address-low-range>20.1.1.0</rule-source-address-low-range>
                <rule-source-address-high-range>20.1.1.255</rule-source-address-high-range>
                <rule-source-address>20.1.1.1</rule-source-address>
            </source-address-range-entry>
            <destination-address-range-entry>
                <rule-destination-address-low-range>30.1.1.0</rule-destination-address-low-range>
                <rule-destination-address-high-range>30.1.1.255</rule-destination-address-high-range>
                <rule-destination-address>30.1.1.1</rule-destination-address>
            </destination-address-range-entry>
            <src-nat-app-entry>
                <src-nat-application>configured</src-nat-application>
            </src-nat-app-entry>
            <source-nat-rule-action-entry>
                <source-nat-rule-action>src_pool1</source-nat-rule-action>
                <rule-source-mapping-type>N/A</rule-source-mapping-type>
            </source-nat-rule-action-entry>
            <source-nat-rule-hits-entry>
                <rule-translation-hits>0</rule-translation-hits>
                <succ-hits>0</succ-hits>
                <failed-hits>0</failed-hits>
                <concurrent-hits>0</concurrent-hits>
            </source-nat-rule-hits-entry>
        </source-nat-rule-entry>
    </source-nat-rule-detail-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""
        self.response["NAT_RULE_False"] = """
   <rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3D0/junos">
    <source-nat-rule-detail-information xmlns="http://xml.juniper.net/junos/18.3D0/junos-nat">
        <source-nat-rule-entry>
            <interface-name>vms-1/1/1</interface-name>
            <service-set-name>snat_ss2</service-set-name>
            <rule-name>nr1</rule-name>
            <rule-set-name>snat_rule_set1</rule-set-name>
            <rule-id>1</rule-id>
            <rule-matching-position>1</rule-matching-position>
            <rule-from-context>zone</rule-from-context>
            <rule-from-context-name>snat_ss1-ZoneIn</rule-from-context-name>
            <rule-to-context>zone</rule-to-context>
            <rule-to-context-name>snat_ss1-ZoneOut</rule-to-context-name>
            <source-address-range-entry>
                <rule-source-address-low-range>20.1.1.0</rule-source-address-low-range>
                <rule-source-address-high-range>20.1.1.255</rule-source-address-high-range>
                <rule-source-address>20.1.1.1</rule-source-address>
            </source-address-range-entry>
            <destination-address-range-entry>
                <rule-destination-address-low-range>30.1.1.0</rule-destination-address-low-range>
                <rule-destination-address-high-range>30.1.1.255</rule-destination-address-high-range>
                <rule-destination-address>30.1.1.1</rule-destination-address>
           </destination-address-range-entry>
            <src-nat-app-entry>
                <src-nat-application>configured</src-nat-application>
            </src-nat-app-entry>
            <source-nat-rule-action-entry>
                <source-nat-rule-action>src_pool1</source-nat-rule-action>
                <rule-source-mapping-type>N/A</rule-source-mapping-type>
            </source-nat-rule-action-entry>
            <source-nat-rule-hits-entry>
                <rule-translation-hits>1</rule-translation-hits>
                <succ-hits>1</succ-hits>
                <failed-hits>1</failed-hits>
                <concurrent-hits>0</concurrent-hits>
            </source-nat-rule-hits-entry>
        </source-nat-rule-entry>
    </source-nat-rule-detail-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""
     

        self.response["NAT_RULE_Des"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3D0/junos">
    <destination-nat-rule-information xmlns="http://xml.juniper.net/junos/18.3D0/junos-nat">
        <destination-nat-rule-entry>
            <interface-name>vms-2/3/0</interface-name>
            <service-set-name>dnat_ss1</service-set-name>
            <rule-name>nr1</rule-name>
            <rule-set-name>dnat_rule_set1</rule-set-name>
            <rule-id>1</rule-id>
            <rule-matching-position>1</rule-matching-position>
            <rule-source-address-range-entry>
                <rule-source-address-low-range>20.1.1.0</rule-source-address-low-range>
                <rule-source-address-high-range>20.1.1.255</rule-source-address-high-range>
                <rule-source-address>20.1.1.1</rule-source-address>
            </rule-source-address-range-entry>
            <rule-destination-address-range-entry>
                <rule-destination-address-low-range>60.1.1.2</rule-destination-address-low-range>
                <rule-destination-address-high-range>60.1.1.2</rule-destination-address-high-range>
                <rule-destination-address>60.1.1.3</rule-destination-address>
            </rule-destination-address-range-entry>
            <destination-nat-application>configured</destination-nat-application>
            <destination-nat-rule-action>dst_pool1</destination-nat-rule-action>
            <rule-translation-hits>1</rule-translation-hits>
            <succ-hits>1</succ-hits>
            <failed-hits>1</failed-hits>
            <concurrent-hits>0</concurrent-hits>
        </destination-nat-rule-entry>
    </destination-nat-rule-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""

        self.response["VERIFY_STATIC"] = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3D0/junos">
    <configuration junos:commit-seconds="1530032367" junos:commit-localtime="2018-06-26 09:59:27 PDT" junos:commit-user="root">
            <routing-instances>
                <instance>
                    <name>server-vrf1</name>
                    <instance-type>virtual-router</instance-type>
                    <interface>
                        <name>ge-1/2/5.0</name>
                    </interface>
                    <interface>
                        <name>vms-2/3/0.2</name>
                    </interface>
                    <routing-options>
                        <static>
                            <route>
                                <name>0.0.0.0/0</name>
                                <next-hop>vms-2/3/0.2</next-hop>
                            </route>
                        </static>
                    </routing-options>
                </instance>
            </routing-instances>
    </configuration>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""
        self.response["VERIFY_SESSION"]= """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3D0/junos">  
  <usf-session-count-information xmlns="http://xml.juniper.net/junos/18.3D0/junos-flow">
        <usf-session-count>
            <interface-name>vms-2/3/0</interface-name>
            <service-set-name>snat_ss1</service-set-name>
            <valid-session-count>0</valid-session-count>
            <pending-session-count>0</pending-session-count>
            <invalid-session-count>0</invalid-session-count>
            <other-session-count>0</other-session-count>
        </usf-session-count>
    </usf-session-count-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""


        self.cgn = usf_cgnat(dh=None)
        self.cgn.log = MagicMock()
        self.cgn.dh = MagicMock()
        self.cgn.dh.cli = MagicMock()
        self.cgn.dh.cli = MagicMock()
        self.cgn.fn_checkin = MagicMock()
        self.cgn.fn_checkout = MagicMock()
        self.cgn.fn_checkout.return_value = True
        self.cgn.config = MagicMock()
        self.cgn.config.return_value = True
        self.cgn._get_intf_ss = MagicMock()
        self.cgn._get_tg_port_and_config_mapping = MagicMock()
#        dd = {}
#        dd = lambda: defaultdict(dd)
#        self.cgn.dd = MagicMock()
#        self.cgn.dd.return_value = dd()
        self.cgn.r_if = {'ss1'}
        self.cgn.resource = 'esst480p'
        self.cgn.topo = {'intf' : {'1/1' : {'path' : 'r0r1'}},
                         'path_res' : {'esst480p' : {'r0r1' : ['intf1']}}}
        #builtins.t = {'resources' : {'esst480p' : {'interfaces' : {
        #    'intf1' : {'pic' : 'ms-5/0/0'}}}}}
        self.cgn.intf_ss = {'ms-5/0/0' : 'ss1'}
        self.cgn.sset = {'ss1': {'spic': 'ms-5/0/0', 'nat_rules': ['nr1']}}
        self.cgn.nat_rule = {'nr1': {'src_pool': 'np1', 'trans_type': 'napt',
                                     'trans_eim': 1, 'trans_eif': 1}}
        self.cgn.nat_pool = {'MX1_CGN4_AMS4-CONE-p1': {'pool_type' : 'source'}}
        self.cgn.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'],
                                    'dst_ips_list': ['60.1.1.2', '60.1.1.3'],
                                    'sess_list': [{'src_ip': '11.1.1.2', 'src_port': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_port': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_port': '5060'}]},
                            'total': 10}
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1',
                                       'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24',
                                       'nat_port': '1024-3456', 'nat_port_low': '1024',
                                       'nat_port_high': '3456', 'tot_sess': 1,
                                       'rand_sess_idx_list': [0]}}
        self.cgn.pool_map = {'np1': {'tot_sess': 10}, 'np2': {'tot_sess': 10}}

    #############################################
    # set_nat_rule
    #############################################
    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_cgnat_set_nat_rule_set1(self, patch1):
        """
        Unit test case for set_nat_rule_set method
        testing set action for both source and destination nat
        """
        patch1.return_value = None
        self.assertEqual(self.cgn.set_nat_rule_set(count=1, action='set',
                                                   dir='input', num_rules=1, rule_name='nr',
                                                   index=1, nat_type='source',
                                                   rs_idx_reset=False, rs_idx=1,
                                                   src_addr='10.0.0.0',
                                                   src_addr_step=1, src_addr_name='srcAdd',
                                                   dst_addr_name='dstAdd', src_addr_nw_step=1,
                                                   src_addr_nw_step_cnt=1, dst_addr='20.0.0.0',
                                                   dst_addr_step=1, same_rule_set=False,
                                                   src_low=1, src_high=1,
                                                   dst_low=1, dst_high=1), True)

    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_cgnat_set_nat_rule_set_dst(self, patch2):
        """
        Unit test case for set_nat_rule_set method
        testing set action for both destination nat
        """
        patch2.return_value = None
        self.assertEqual(self.cgn.set_nat_rule_set(count=1, action='set',
                                                   dir='input', num_rules=1, rule_name='nr',
                                                   index=1, nat_type='source', rs_idx_reset=True,
                                                   rs_idx=1, src_addr='10.0.0.0', src_addr_step=1,
                                                   src_addr_name='srcAdd', dst_addr_name='dstAdd',
                                                   src_addr_nw_step=1, dst_addr='20.0.0.0',
                                                   dst_addr_step=1, same_rule_set=True,
                                                   src_low=1, snat_off=True, dst_low=1), True)

    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_cgnat_set_nat_rule_set_src(self, patch3):
        """
        Unit test case for set_nat_rule_set method
        testing set action for both source nat
        """
        patch3.return_value = None
        self.assertEqual(self.cgn.set_nat_rule_set(count=1, action='set',
                                                   dir='input', num_rules=1, rule_name='nr',
                                                   index=1, nat_type='source', rs_idx_reset=True,
                                                   rs_idx=1, src_addr='10.0.0.0', src_addr_step=1,
                                                   src_addr_name='srcAdd', dst_addr_name='dstAdd',
                                                   src_addr_nw_step=1, dst_addr='20.0.0.0',
                                                   dst_addr_step=1, same_rule_set=True,
                                                   src_low=1, dnat_off=True, dst_low=1), True)

    #############################################
    # set_nat_pool
    #############################################
    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_set_nat_pool(self, patch4):
        """
        Unit test case for set_nat_pool method
        testing set action for  nat pool
        """
        patch4.return_value = None
        self.assertEqual(self.cgn.set_nat_pool(name='pool1', addr='30.0.0.0/24',
                                               addr_low='30.0.0.1', addr_high='30.0.0.100',
                                               port_low='1000', port_high='2000'), True)

    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_set_nat_pool_port_range(self, patch5):
        """
        Unit test case for set_nat_pool method
        testing set action for  nat pool port range
        """
        patch5.return_value = None
        self.assertEqual(self.cgn.set_nat_pool(name='pool1', addr='30.0.0.0/24',
                                               addr_low='30.0.0.1', addr_high='30.0.0.100',
                                               port_low='1000', port_high='2000',
                                               port_range_random=1, snmp_trap_low='1',
                                               snmp_trap_high='10',
                                               host_addr_base='10.0.0.1'), True)


    def test_set_nat_pool_negative(self):
        """
        Unit test case for set_nat_pool method
        testing set action for nat pool - result fail
        """
        self.assertEqual(self.cgn.set_nat_pool(name='nat_pool', action=None), True)

    #############################################
    # ::verify
    #############################################
    @patch('jnpr.toby.services.services.services.verify')
    def test_verify_wrapper(self, patch6):
        """
        Unit test case for def verify() method
        testing verify method using wrapper
        """
        patch6.return_value = None
        self.cgn = usf_cgnat(dh=None)
        self.cgn.log = MagicMock()
#        self.cgn.verify_nat_pool_detail = MagicMock()
#        self.cgn._get_tg_port_and_config_mapping = MagicMock()
#        self.cgn.verify_sessions_extensive = MagicMock()

        self.assertEqual(self.cgn.verify(), True)

    def test__get_ss_from_pool(self):
        """
        Unit test case for  method
        testing get action to get ss_map from nat pool
        """

        self.cgn = usf_cgnat(dh=None)
        self.cgn.log = MagicMock()
        self.cgn.fn_checkin = MagicMock()
        self.cgn.fn_checkout = MagicMock()
        self.cgn.fn_checkout.return_value = True
        self.cgn.pool_map = {}
        self.cgn.nat_pool = {"np1"}
        self.cgn.nat_pool_rule_map = {"src_pool": {'np1':"nr1"}}
        self.cgn.ss_map = {"nat_pool": {'np1':"ss1"}, "nat_rule_set":{'nr1':'ss1'}}
        self.cgn.sset = {"ss1":{'intf':"eth1"}}
        self.cgn.tg_sess_cnt = {"eth1":{'ss1':"eth1"}}
        self.assertNotEqual(self.cgn._get_ss_from_pool(), None)
        self.cgn.nat_pool_rule_map = {"src_pool": {}, "dst_pool": {'np1':"nr1"}}
        self.assertNotEqual(self.cgn._get_ss_from_pool(), None)
        self.cgn.nat_pool_rule_map = {"src_pool": {'pn1'}, "dst_pool": {'pn1'}}
        self.assertNotEqual(self.cgn._get_ss_from_pool(), None)
#        self.cgn.pool_map = {'np1'}
#        self.cgn.nat_pool = {}
#        self.cgn.nat_pool_rule_map = {}
#        self.cgn.nat_pool_rule_map = {"src_pool": {'np1':"nr1"}, "dst_pool": {}}
#        self.assertNotEqual(self.cgn._get_ss_from_pool(), None)

    @patch('jnpr.toby.services.cgnat.services._get_tg_port_and_config_mapping')
    def test__tg_port_config_mapping(self, patch7):
        """
        Unit test case for _get_tg_port_and_config_mapping  method
        testing get action for port getting port and config mapping
        """
        patch7.return_value = None
        self.cgn = usf_cgnat(dh=None)
        self.cgn.log = MagicMock()
        self.cgn.tg_sess_cnt = 1
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1',
                                       'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24',
                                       'nat_port': '1024-3456', 'nat_port_low': '1024',
                                       'nat_port_high': '3456', 'tot_sess': 1,
                                       'rand_sess_idx_list': [0]}}
        self.cgn.sset = {'ss1':{'nat_rule_set':['nr1']}}
        self.cgn.nat_rule_set = {'nr1':{'src_pool':"np1", 'dst_pool':"np1"}}
        self.cgn.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'],
                                    'dst_ips_list': ['60.1.1.2', '60.1.1.3'],
                                    'sess_list': [{'src_ip': '11.1.1.2', 'src_port': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_port': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_port': '5060'}]},
                            'total': 10}
        self.cgn.nat_pool = {"np1" : {"port_low": "1024", "port_high": "1024", "addr": ""}}
        self.assertEqual(self.cgn._get_tg_port_and_config_mapping(tg_sess=self.cgn.tg_sess,
                                                                  limit=1), None)
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1',
                                       'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24',
                                       'nat_port': '1024-3456', 'nat_port_low': '1024',
                                       'nat_port_high': '3456', 'tot_sess': 1,
                                       'rand_sess_idx_list': [0]}}
        self.cgn.sset = {'ss1':{'nat_rule_set':['nr1', 'nr2']}}
        self.cgn.nat_rule_set = {'nr1':{'src_pool':"np1", 'dst_pool':"np1"}}
        self.cgn.nat_pool = {"np1" : {"port_auto": 1, "addr" : ""}}
        self.cgn.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'],
                                    'dst_ips_list': ['60.1.1.2', '60.1.1.3'],
                                    'sess_list': [{'src_ip': '11.1.1.2', 'src_port': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_port': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_port': '5060'}]},
                            'total': 10}
        self.assertEqual(self.cgn._get_tg_port_and_config_mapping(tg_sess=self.cgn.tg_sess,
                                                                  limit=1), None)
        self.cgn.tg_sess_cnt = None
#        self.assertEqual(self.cgn._get_tg_port_and_config_mapping(tg_sess=self.cgn.tg_sess,
#                                                                  limit=1), None)

    #############################################
    # get_nat_pool_detail
    #############################################
    @patch('jnpr.toby.services.cgnat.utils.update_data_from_output')
    def test_get_usf_nat_pool_detail(self, patch8):
        """
        Unit test case for get_usf_nat_pool_detail  method
        testing get usf nat pool statistics from nat pool detail command
        """
        patch8.return_value = None
        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_POOL_DETAIL"])
        xml_tree = xml_tree['rpc-reply']
        _pool_type = 'source'
        _xpath = '{}-nat-pool-detail-information/{}-nat-pool-info-entry'.format(_pool_type,
                                                                                _pool_type)
        for path in  _xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        options = {'name':'MX1_CGN4_AMS4-CONE-p1'}
        self.cgn.data = {}
        self.assertEqual(self.cgn.get_usf_nat_pool_detail(**options), True)

    @patch('jnpr.toby.services.cgnat.iputils.get_network_ip_range')
    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_verify_usf_nat_pool_detail(self, test_cmp_dicts, pathch2):
        """
        Unit test case for verify_usf_nat_pool_detail method
        testing verify usf nat pool statistics from nat pool detail command
        """
        pathch2.return_value = '1-1'
        self.cgn.get_usf_nat_pool_detail = MagicMock()
        self.cgn._get_tg_port_and_config_mapping = MagicMock()
        self.cgn._get_ss_from_pool = MagicMock()
        self.cgn.result = MagicMock()
        self.cgn.tg_sess_cnt = {'total': 2}
        self.cgn.data = {'nat_pool': {'MX1_CGN4_AMS4-CONE-p1': {'pool_type': 'source'}}}
        options = {'address-assignment': 'no-paired', 'tg_sess': 1}
        test_cmp_dicts.return_value = True
        #test this later, 'addr' : ""}}
        self.cgn.nat_pool = {'MX1_CGN4_AMS4-CONE-p1': {'pool_type': 'source'}}
        self.cgn.pool_map = {'MX1_CGN4_AMS4-CONE-p1': {'total_sess': 10,
                                                       'spic': 'ms-5/0/0', 'sset': ''}}
        self.assertEqual(self.cgn.verify_usf_nat_pool_detail(name='MX1_CGN4_AMS4-CONE-p1',
                                                             **options), True)
        test_cmp_dicts.return_value = False
        self.assertEqual(self.cgn.verify_usf_nat_pool_detail(name='MX1_CGN4_AMS4-CONE-p1',
                                                             **options), True)

    #############################################
    # get_nat_rule_detail
    #############################################
    def test_get_usf_nat_rule(self):
        """
        Unit test case for get_usf_nat_rule method
        testing get nat rule statistics from show usf nat rule detail command
        """
        self.cgn.nat_rule_set = {'snat_rule_set1': {'nr1': {'nat_type': 'source'}}}
        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_RULE_DETAIL"])
        xml_tree = xml_tree['rpc-reply']
        _nat_type = 'source'
        _xpath = '{}-nat-rule-detail-information/{}-nat-rule-entry'.format(_nat_type, _nat_type)
        for path in  _xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        options = {'rs_name' : 'snat_rule_set1', 'r_name' : 'nr1'}
        self.cgn.data = {}
        self.assertEqual(self.cgn.get_usf_nat_rule(**options), True)


    @patch('jnpr.toby.services.cgnat.iputils.get_network_ip_range')
    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_verify_usf_nat_rule(self, test_cmp_dicts, pathch9):
        """
        Unit test case for verify_usf_nat_rule method
        testing verify nat rule statistics from show usf nat rule detail command
        """
        pathch9.return_value = '1-1'
        self.cgn.get_usf_nat_rule = MagicMock()
        self.cgn._get_tg_port_and_config_mapping = MagicMock()
        self.cgn._get_ss_from_pool = MagicMock()
        self.cgn.result = MagicMock()
        self.cgn.tg_sess_cnt = {'total': 2}
        self.cgn.data = {'nat_rule_set': {'snat_rule_set1': {'nr1': {'app': 'configured',
                                                                     'per_nat_type': 'N/A',
                                                                     'per_map_type':
                                                                     'address-port-mapping'}}}}
        self.cgn.ss_map = {'nat_pool': {'MX1_CGN4_AMS4-CONE-p1': "snat_ss1"},
                           'nat_rule_set': {'snat_rule_set1': 'snat_ss1'}}
        options = {'rs_name': 'snat_rule_set1', 'r_name': 'nr1', 'tg_sess': 1}
        test_cmp_dicts.return_value = True
        self.cgn.nat_rule_set = {'snat_rule_set1': {'nr1': {'nat_type': 'source'}}}
        self.cgn.pool_map = {'MX1_CGN4_AMS4-CONE-p1': {'total_sess': 10,
                                                       'spic': 'ms-5/0/0', 'sset': ''}}
        self.assertEqual(self.cgn.verify_usf_nat_rule(**options), True)
        test_cmp_dicts.return_value = False
        self.assertEqual(self.cgn.verify_usf_nat_rule(**options), True)


    #############################################
    # verify_usfnat_pool_detail
    #############################################
    def test_verify_usf_nat_pool_(self):
        """ Function to test verify usf nat pool detail """

        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_POOL"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'source-nat-pool-detail-information/source-nat-pool-info-entry'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        option = {'interface-name':'vms-2/3/0', 'pool-name':'src_pool1','service-set-name':'snat_ss1','total-pool-address':'254','address-range-high':'60.1.1.254','address-range-low':'60.1.1.1'}
        self.assertEqual(self.cgn.verify_nat_pool(name=None, nat_type = "source", expected_output = option),True)

    def test_verify_usf_nat_pool(self):
        """ Function to test verify usf nat pool detail """

        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_POOL_Des"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'destination-nat-pool-information/destination-nat-pool-entry'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        option = {'interface-name':'vms-2/3/0', 'pool-name':'src_pool1','service-set-name':'snat_ss1','total-pool-address':'254','address-range-high':'60.1.1.254','address-range-low':'60.1.1.1'}
        self.assertEqual(self.cgn.verify_nat_pool(name=None, nat_type = "destination",  expected_output = option),True)




    def test_usf_nat_fail(self):
        """ Function to test wrong usf nat pool details"""

        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_POOL_False"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'source-nat-pool-detail-information/source-nat-pool-info-entry'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        option = {'interface-name':'vms-2/3/0', 'pool-name':'src_pool1','service-set-name':'snat_ss1','total-pool-address':'254','address-range-high':'60.1.1.254','address-range-low':'60.1.1.1'}
        self.assertEqual(self.cgn.verify_nat_pool(name=None, nat_type = "source", expected_output = option),True)

    #############################################
    # verify_usfnat_rule_detail
    #############################################


    def test_usf_nat_rule_(self):
        """ Function to test verify usf nat rule detail"""

        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_RULE"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'source-nat-rule-detail-information/source-nat-rule-entry'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        option = {'interface-name':'vms-2/3/0', 'rule-set-name':'snat_rule_set1','service-set-name':'snat_ss1','rule-source-address-low-range':'20.1.1.0','rule-source-address-high-range':'20.1.1.255','rule-destination-address-low-range':'30.1.1.0','rule-destination-address-high-range':'30.1.1.255','rule-source-address':'20.1.1.1', 'rule-destination-address':'30.1.1.1' }
        self.assertEqual(self.cgn.verify_nat_rule(name=None, nat_type = "source", expected_output = option),True)



    def test_usf_nat_rule(self):
        """ Function to test verify usf nat rule detail"""

        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_RULE_Des"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'destination-nat-rule-information/destination-nat-rule-entry'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        option = {'interface-name':'vms-2/3/0', 'rule-set-name':'snat_rule_set1','service-set-name':'snat_ss1','rule-source-address-low-range':'20.1.1.0','rule-source-address-high-range':'20.1.1.255','rule-destination-address-low-range':'30.1.1.0','rule-destination-address-high-range':'30.1.1.255','rule-source-address':'20.1.1.1', 'rule-destination-address':'60.1.1.2' }
        self.assertEqual(self.cgn.verify_nat_rule(name=None, nat_type = "destination", expected_output = option),True)







    def test_usf_nat_rule_failure(self):
        """ Function to test verify wrong usf nat rule detail"""

        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_RULE_False"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'source-nat-rule-detail-information/source-nat-rule-entry'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        option = {'interface-name':'vms-2/3/0', 'rule-set-name':'snat_rule_set1','service-set-name':'snat_ss1','rule-source-address-low-range':'20.1.1.0','rule-source-address-high-range':'20.1.1.255','rule-destination-address-low-range':'30.1.1.0','rule-destination-address-high-range':'30.1.1.255', 'rule-source-address':'20.1.1.4', 'rule-destination-address':'30.1.1.4' }
        #import pdb; pdb.set_trace()
        self.cgn.verify_nat_rule(name=None, nat_type = "source", expected_output = option)
        self.cgn.fn_checkout.assert_called_with(False)


    #############################################
    # verify_usf_clear_commands_detail
    #############################################



    def test_verify_clear_commands(self):
        """ Function to test usf nat clear details for source"""

        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_POOL"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'source-nat-pool-detail-information/source-nat-pool-info-entry'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        xml_rule = self.xml.xml_string_to_dict(xml_str=self.response["NAT_RULE_False"])
        xml_rule = xml_rule['rpc-reply']
        _xpath = 'source-nat-rule-detail-information/source-nat-rule-entry'
        for pat in _xpath.split('/'):
            xml_rule = xml_rule[pat]
        self.cgn.get_xml_output.side_effect = (xml_tree, xml_rule, "")
        self.cgn.verify_clear_commands_for_nat(nat_type= "source", pool_name  = "src_pool1", rule_name ="snat_rule_set1")
        self.cgn.fn_checkout.assert_called_with(False)

    def test_verify_clear_dest(self):
        """ Function to test usf nat clear details for destination"""
        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_POOL_Des"])
        xml_tree = xml_tree['rpc-reply']
        _xpath = 'destination-nat-pool-information/destination-nat-pool-entry'
        for path in _xpath.split('/'):
            xml_tree = xml_tree[path]
        xml_rule = self.xml.xml_string_to_dict(xml_str=self.response["NAT_RULE_Des"])
        xml_rule = xml_rule['rpc-reply']
        _xpath = 'destination-nat-rule-information/destination-nat-rule-entry'
        for pat in _xpath.split('/'):
            xml_rule = xml_rule[pat]
        self.cgn.get_xml_output.side_effect = (xml_tree, xml_rule, "")
        self.cgn.verify_clear_commands_for_nat(nat_type= "destination", pool_name ="dst_pool1", rule_name ="nr1")
        self.cgn.fn_checkout.assert_called_with(False)





  
    #############################################
    # verify_usf_session_count
    #############################################


    def test_verify_session_count(self):
        """Function to test verify session count"""
        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["VERIFY_SESSION"])
        xml_tree = xml_tree['rpc-reply']
        _xpath = 'usf-session-count-information/usf-session-count'
        for path in _xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value =  xml_tree
        self.cgn.verify_session_count(application_dict ={'udp':'1'})
        self.cgn.fn_checkout.assert_called_with(False)



    #############################################
    # verify_usf_static_route
    #############################################


    def test_verify_static_route(self):
        """ Function to test verify static route"""
        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["VERIFY_STATIC"])
        xml_tree = xml_tree['rpc-reply']
        _xpath = 'configuration/routing-instances/instance/routing-options/static/route'
        for path in _xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value =  xml_tree
        self.cgn.verify_static_routes_in_routing_instances(vrf_dict={'client-vrf1':['0.0.0.0/0','vms-0/2/0.1']})
        self.cgn.fn_checkout.assert_called_with(False)




    

if __name__ == '__main__':
    unittest.main()
