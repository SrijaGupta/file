#! /usr/bin/python3
# -*- coding: utf-8 -*-
#pylint: disable=protected-access
"""
Description: Unit testcases for  usf services.py
Company: Juniper Networks
"""
import sys
import unittest2 as unittest
from optparse import Values
from jnpr.toby.services.usf.usf_services import usf_services
# jnpr.toby.hldcl.juniper.routing.router import Router
from mock import patch
from mock import Mock
from mock import MagicMock
from jnpr.toby.utils.xml_tool import xml_tool
#from collections import defaultdict

import builtins
builtins.t = {}

if sys.version < '3':
    BUILTIN_STRING = '__builtin__'
else:
    BUILTIN_STRING = 'builtins'

#from services import services

class MissingMandatoryArgument(ValueError):
    """Class for raising custom exception for missing mandatory argument"""
    def __init__(self, err_msg):
        """Constructor method to add message to missing mandatory argument"""
        builtins.t = MagicMock()
        t.log('ERROR', "Missing mandatory argument, {}".format(err_msg))
        super().__init__("Missing mandatory argument, {}".format(err_msg))

class TestServices(unittest.TestCase):
    # Mocking the router handle
    # Router = MagicMock()
    # mocked_obj = MagicMock(spec=Router)
    # mocked_obj.log = MagicMock()
    # mocked_obj.execute = MagicMock()
    """
    Class having unit testcases for usf services.py
    """
    def setUp(self):
        """
        Method setting up all required objects for unit testing framework
        """
        self.srv = usf_services(dh=None)
        self.srv.config = MagicMock()
        builtins.t = MagicMock()
        # t.is_robot = True
        # t._script_name = 'name'
        # t.log = MagicMock()
        self.srv.log = MagicMock()
        self.srv.dd = MagicMock()
        self.response = {}
        self.xml = xml_tool()
        self.mocked_obj = MagicMock()

        # self.srv.MissingMandatoryArgument = MagicMock()
        self.srv.fn_checkin = MagicMock()
        self.srv.fn_checkout = MagicMock()
        self.srv.fn_checkout.return_value = True
        # self.srv.MissingMandatoryArgument.return_value = ValueError("Missing mandatory argument,")
        self.srv.MissingMandatoryArgument = MissingMandatoryArgument
        self.srv.resource = 'esst480p'
        #builtins.t = {'resources': {'esst480p': {'interfaces': {'intf1': {'pic': 'ms-5/0/0'}}}}}
        self.srv.topo = {'intf': {'1/1': {'path': 'r0r1'}},
                         'path_res': {'esst480p': {'r0r1': ['intf1']}}}
        self.srv.intf_ss = {'ms-5/0/0': 'ss1'}
        self.srv.sset = {'ss1': {'spic': 'ms-5/0/0', 'nat_rules': ['nr1']}}
        self.srv.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'],
                                    'dst_ips_list': ['60.1.1.2', '60.1.1.3'],
                                    'sess_list': [{'src_ip': '11.1.1.2', 'src_prt': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_prt': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_prt': '5060'}]},
                            'total': 10}
        self.response["SRV_SESS_EXT_1"] = '''
ms-4/0/0
Service Set: ss1, Session: 67108866, ALG: icmpv6, Flags: 0x200000, IP Action: no, Offload: no, Asymmetric: no, Session timeout: 72
NAT PLugin Data:
NAT Action:   Translation Type - STATEFUL NAT64
    NAT source              3001::1:42583   ->   161.161.161.1:24831  
    NAT Destination   1001::401:102         ->         4.1.1.2
ICMPV6          3001::1        ->   1001::401:102        Forward  I              29
  Byte count: 3016
  Flow role: Initiator, Timeout: 100
ICMP            4.1.1.2        ->   161.161.161.1        Forward  O              28
  Byte count: 2352
  Flow role: Responder, Timeout: 100
       '''
        self.response["CLR_SRV_SESS"] = '''
       <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
           <service-msp-sess-drain-information>
               <service-msp-sess-drain>
                   <interface-name>ms-4/0/0</interface-name>
                   <service-set-name>service_set</service-set-name>
                   <sess-marked-for-deletion>0</sess-marked-for-deletion>
               </service-msp-sess-drain>
           </service-msp-sess-drain-information>
           <cli>
               <banner></banner>
           </cli>
       </rpc-reply>
       '''
        self.response["CLR_SRV_SESS_1"] = '''
       <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
           <service-msp-sess-drain-information>
               <service-msp-sess-drain>
                   <service-set-name>service_set</service-set-name>
                   <sess-marked-for-deletion>0</sess-marked-for-deletion>
               </service-msp-sess-drain>
           </service-msp-sess-drain-information>
           <cli>
               <banner></banner>
           </cli>
       </rpc-reply>
       '''
        self.response["CLR_SRV_SESS_RMV"] = '''
       <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
           <service-msp-sess-drain-information>
               <service-msp-sess-drain>
                   <interface-name>ms-4/0/0</interface-name>
                   <service-set-name>service_set</service-set-name>
                   <sess-removed>0</sess-removed>
               </service-msp-sess-drain>
           </service-msp-sess-drain-information>
           <cli>
               <banner></banner>
           </cli>
       </rpc-reply>
       '''
        self.response["GET_SESS_CNT"] = '''
       <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
           <service-msp-sess-count-information>
               <service-msp-sess-count>
                   <interface-name>ms-4/0/0</interface-name>
                   <service-set-name>service_set</service-set-name>
                   <sess-count>1</sess-count>
               </service-msp-sess-count>
           </service-msp-sess-count-information>
           <cli>
               <banner>[edit]</banner>
           </cli>
       </rpc-reply>
       '''
        self.response["GET_SESS_CNT_1"] = '''
       <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
           <service-msp-sess-count-information>
               <service-msp-sess-count>
                   <service-set-name>service_set</service-set-name>
                   <sess-count>1</sess-count>
               </service-msp-sess-count>
           </service-msp-sess-count-information>
           <cli>
               <banner>[edit]</banner>
           </cli>
       </rpc-reply>
       '''
        self.response['analysis'] = '''
       <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
    <service-session-analysis-information>
        <service-session-analysis-entry>
            <session-analysis-statistics-pic-info>
                <pic-name>ms-4/2/0</pic-name>
            </session-analysis-statistics-pic-info>
            <session-analysis-statistics-entry>
                <num-total-session-active>0</num-total-session-active>
                <num-total-tcp-session-active>0</num-total-tcp-session-active>
                <num-total-tcp-gated-session-active>0</num-total-tcp-gated-session-active>
                <num-total-tcp-tunneled-session-active>0</num-total-tcp-tunneled-session-active>
                <num-total-tcp-regular-session-active>0</num-total-tcp-regular-session-active>
                <num-total-tcp-ipv4-session-active>0</num-total-tcp-ipv4-session-active>
                <num-total-tcp-ipv6-session-active>0</num-total-tcp-ipv6-session-active>
                <num-total-udp-session-active>0</num-total-udp-session-active>
                <num-total-udp-gated-session-active>0</num-total-udp-gated-session-active>
                <num-total-udp-tunneled-session-active>0</num-total-udp-tunneled-session-active>
                <num-total-udp-regular-session-active>0</num-total-udp-regular-session-active>
                <num-total-udp-ipv4-session-active>0</num-total-udp-ipv4-session-active>
                <num-total-udp-ipv6-session-active>0</num-total-udp-ipv6-session-active>
                <num-total-other-session-active>0</num-total-other-session-active>
                <num-total-other-ipv4-session-active>0</num-total-other-ipv4-session-active>
                <num-total-other-ipv6-session-active>0</num-total-other-ipv6-session-active>
                <num-created-session-per-sec>0</num-created-session-per-sec>
                <num-deleted-session-per-sec>0</num-deleted-session-per-sec>
                <peak-total-session-active>13397751</peak-total-session-active>
                <peak-total-tcp-session-active>13397810</peak-total-tcp-session-active>
                <peak-total-udp-session-active>0</peak-total-udp-session-active>
                <peak-total-other-session-active>0</peak-total-other-session-active>
                <peak-created-session-per-second>2123</peak-created-session-per-second>
                <peak-deleted-session-per-second>1099797</peak-deleted-session-per-second>
                <session-pkts-received>1711198102</session-pkts-received>
                <session-pkts-transmitted>1816940625</session-pkts-transmitted>
                <session-slow-path-forward>83169</session-slow-path-forward>
                <session-slow-path-discard>12113</session-slow-path-discard>
            </session-analysis-statistics-entry>
        </service-session-analysis-entry>
    </service-session-analysis-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        '''
        self.response["cpu_usage"] = '''
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
    <service-set-cpu-statistics-information xmlns="http://xml.juniper.net/junos/15.1I0/junos-adaptive-services">
        <service-set-cpu-statistics>
            <service-set-name>ss</service-set-name>
            <interface-name>ms-4/2/0</interface-name>
            <cpu-utilization-percent>0.00</cpu-utilization-percent>
        </service-set-cpu-statistics>
        <service-set-cpu-statistics>
            <service-set-name>System</service-set-name>
            <interface-name>ms-4/2/0</interface-name>
            <cpu-utilization-percent>1.96</cpu-utilization-percent>
        </service-set-cpu-statistics>
        <service-set-cpu-statistics>
            <service-set-name>Idle</service-set-name>
            <interface-name>ms-4/2/0</interface-name>
            <cpu-utilization-percent>98.03</cpu-utilization-percent>
        </service-set-cpu-statistics>
        <service-set-cpu-statistics>
            <service-set-name>Receive</service-set-name>
            <interface-name>ms-4/2/0</interface-name>
            <cpu-utilization-percent>0.00</cpu-utilization-percent>
        </service-set-cpu-statistics>
        <service-set-cpu-statistics>
            <service-set-name>Transmit</service-set-name>
            <interface-name>ms-4/2/0</interface-name>
            <cpu-utilization-percent>0.00</cpu-utilization-percent>
        </service-set-cpu-statistics>
    </service-set-cpu-statistics-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        '''
        self.response['ss_summary'] = '''
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1I0/junos">
    <service-set-summary-information junos:style="summary">
        <service-set-summary-information-entry>
            <interface-name>ms-4/2/0</interface-name>
            <service-set-service-type-entry>
                <service-sets-configured>2</service-sets-configured>
                <service-set-bytes-used>2038579398</service-set-bytes-used>
                <service-set-percent-bytes-used>7.09</service-set-percent-bytes-used>
                <service-set-policy-bytes-used>3142872</service-set-policy-bytes-used>
                <service-set-percent-policy-bytes-used>0.29</service-set-percent-policy-bytes-used>
                <service-set-cpu-utilization>1.96 %</service-set-cpu-utilization>
            </service-set-service-type-entry>
        </service-set-summary-information-entry>
    </service-set-summary-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
        '''
        self.response['SFW_POLICY'] = '''
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.2I0/junos">
    <security-policies junos:style="brief">
        <security-context>
            <policies>
                <policy-information>
                    <policy-name>sfw_policy1</policy-name>
                    <policy-state>enabled</policy-state>
                    <policy-identifier>1005</policy-identifier>
                    <sfw-rule-name>sfw_rule1</sfw-rule-name>
                    <scope-policy-identifier>0</scope-policy-identifier>
                    <policy-sequence-number>1</policy-sequence-number>
                    <service-set-name>twice_nat_ss1</service-set-name>
                    <interface-name>vms-0/2/0</interface-name>
                    <match-direction>input</match-direction>
                    <source-addresses junos:style="brief">
                        <source-address>
                            <address-name>any</address-name>
                        </source-address>
                    </source-addresses>
                    <destination-addresses junos:style="brief">
                        <destination-address>
                            <address-name>any</address-name>
                        </destination-address>
                    </destination-addresses>
                    <applications junos:style="brief">
                        <application>
                            <application-name>junos-icmp-ping</application-name>
                        </application>
                        <application>
                            <application-name>junos-udp-any</application-name>
                        </application>
                        <application>
                            <application-name>junos-tcp-any</application-name>
                        </application>
                    </applications>
                    <source-identities junos:style="brief">
                    </source-identities>
                    <policy-action>
                        <action-type>permit</action-type>
                        <policy-tcp-options>
                            <policy-tcp-options-syn-check>No</policy-tcp-options-syn-check>
                            <policy-tcp-options-sequence-check>No</policy-tcp-options-sequence-check>
                            <policy-tcp-options-window-scale>No</policy-tcp-options-window-scale>
                        </policy-tcp-options>
                    </policy-action>
                    <policy-application-services>
                    </policy-application-services>
                </policy-information>
            </policies>
        </security-context>
        <security-context>
            <policies>
                <policy-information>
                    <policy-name>sfw_policy1</policy-name>
                    <policy-state>enabled</policy-state>
                    <policy-identifier>1006</policy-identifier>
                    <scope-policy-identifier>0</scope-policy-identifier>
                    <policy-sequence-number>1</policy-sequence-number>
                    <service-set-name>twice_nat_ss1</service-set-name>
                    <interface-name>vms-0/2/0</interface-name>
                    <match-direction>output</match-direction>
                    <source-addresses junos:style="brief">
                        <source-address>
                            <address-name>any</address-name>
                        </source-address>
                    </source-addresses>
                    <destination-addresses junos:style="brief">
                        <destination-address>
                            <address-name>any</address-name>
                        </destination-address>
                    </destination-addresses>
                    <applications junos:style="brief">
                        <application>
                            <application-name>junos-icmp-ping</application-name>
                        </application>
                        <application>
                            <application-name>junos-udp-any</application-name>
                        </application>
                        <application>
                            <application-name>junos-tcp-any</application-name>
                        </application>
                    </applications>
                    <source-identities junos:style="brief">
                    </source-identities>
                    <policy-action>
                        <action-type>permit</action-type>
                        <policy-tcp-options>
                            <policy-tcp-options-syn-check>No</policy-tcp-options-syn-check>
                            <policy-tcp-options-sequence-check>No</policy-tcp-options-sequence-check>
                            <policy-tcp-options-window-scale>No</policy-tcp-options-window-scale>
                        </policy-tcp-options>
                    </policy-action>
                    <policy-application-services>
                    </policy-application-services>
                </policy-information>
            </policies>
        </security-context>
    </security-policies>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
'''

        self.response['SFW_POLICY_HIT_COUNT'] = '''
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.2I0/junos">
    <policy-hit-count-service-router xmlns="http://xml.juniper.net/junos/18.2I0/junos-security-policy">
        <logical-system-name>root-logical-system</logical-system-name>
        <policy-hit-count-service-router-entry>
            <policy-hit-count-service-router-policy-name>sfw_policy1</policy-hit-count-service-router-policy-name>
            <policy-hit-count-service-router-sfw-rule-name>sfw_rule11</policy-hit-count-service-router-sfw-rule-name>
            <policy-hit-count-service-router-index>1</policy-hit-count-service-router-index>
            <policy-hit-count-service-router-service-set>twice_nat_ss1</policy-hit-count-service-router-service-set>
            <policy-hit-count-service-router-interface>vms-0/2/0</policy-hit-count-service-router-interface>
            <policy-hit-count-service-router-count>0</policy-hit-count-service-router-count>
            <policy-hit-count-service-router-direction>input</policy-hit-count-service-router-direction>
        </policy-hit-count-service-router-entry>
        <policy-hit-count-service-router-entry>
            <policy-hit-count-service-router-policy-name>sfw_policy1</policy-hit-count-service-router-policy-name>
            <policy-hit-count-service-router-sfw-rule-name>sfw_rule11</policy-hit-count-service-router-sfw-rule-name>
            <policy-hit-count-service-router-index>2</policy-hit-count-service-router-index>
            <policy-hit-count-service-router-service-set>twice_nat_ss1</policy-hit-count-service-router-service-set>
            <policy-hit-count-service-router-interface>vms-0/2/0</policy-hit-count-service-router-interface>
            <policy-hit-count-service-router-count>0</policy-hit-count-service-router-count>
            <policy-hit-count-service-router-direction>output</policy-hit-count-service-router-direction>
        </policy-hit-count-service-router-entry>
        <policy-hit-count-num>2</policy-hit-count-num>
    </policy-hit-count-service-router>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
'''
  # def test_services_init_null_dh(self):
  #     kwargs = {'dh': None}
  #     with self.assertRaises(Exception) as context:
  #         services(dh=kwargs)
  #     self.assertTrue(
  #    'Device handle is mandatory argument' in str(context.exception))

    # #TODO to be uncommented
   #  def test_set_service_pic_null_args(self):
   #      # kwargs = {'dh': self.mocked_obj}
   #      # self.srv = services(dh=kwargs)
   #      with self.assertRaises(ValueError) as context:
   #        self.srv.set_service_pic(name=None)
   #      self.assertTrue('Name is mandatory argument' in str(context.exception))

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_service_pic(self, patch1):
        """
        Unit testcase for set_service_pic success
        """
        patch1.return_value = None
        # kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'src_ip': "1.1.1.1", 'dst_ip': "2.2.2.2",
                   'sw_sip': "3.3.3.3", 'sw_dip': "4.4.4.4", 'src_wc': "0.0.0.2",
                   'dst_wc': "0.0.0.2", 'sw_sip_wc': "0.0.0.2", 'sw_dip_wc': "0.0.0.2",
                   'rpm_addr': "5.5.5.5", 'rpm_addr_step': 1, 'mpls': 1, 'sl_src_addr': "6.6.6.6",
                   'next_hop': True, 'service_opts': True}
        # self.srv.set_service_pic(name="ms-0/0/0",**options)
        self.assertNotEqual(self.srv.set_service_pic(name="ms-0/0/0", **options), None)
        with self.assertRaises(MissingMandatoryArgument) as context:
            self.srv.set_service_pic(name=None)
        self.assertTrue('Missing mandatory argument, name' in str(context.exception))
        # self.assertNotEqual(self.srv.set_service_pic(name=None), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_service_pic_else(self, patch1):
        """
        Unit testcase for set_service_pic else
        """
        patch1.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'src_ip': "1.1.1.1", 'dst_ip': "2.2.2.2",
                   'sw_dip': "4.4.4.4", 'rpm_addr': "5.5.5.5", 'rpm_addr_step': 1,
                   'service_opts': True,
                   'mpls': 1, 'sl_src_addr': "6.6.6.6", 'sw_sip': "3.3.3.3", 'next_hop': 0}
        self.assertNotEqual(self.srv.set_service_pic(name="ms-0/0/0", **options), None)

    def test_set_vlan_ipv4(self):
        """
        Unit testcase for set_vlan for ipv4 address
        """
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'vlan': 1,
                   'ip': "1.1.1.1/24", 'outer_id': 100, 'range': 10}
        self.assertNotEqual(self.srv.set_vlan(name="ms-0/0/0", **options), None)

    def test_set_vlan_range_null(self):
        """
        Unit testcase for set_vlan range as null
        """
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'vlan': 1,
                   'ip': "1.1.1.1/24", 'outer_id': 100}
        self.assertNotEqual(self.srv.set_vlan(name="ms-0/0/0", **options), None)

    def test_set_vlan_id_null(self):
        """
        Unit testcase for set_vlan vlan id as null
        """
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'vlan': 1, 'ip': "1.1.1.1/24"}
        self.assertNotEqual(self.srv.set_vlan(name="ms-0/0/0", **options), None)

    # def test_set_vlan_vlan_null(self):
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     # delattr(self.srv, 'vlan')
    #     self.srv.cmd_add = MagicMock()
    #     options = {'action': "set", 'ip': "1.1.1.1/24"}
    #     self.assertEqual(self.srv.set_vlan(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip')
    def test_set_vlan_ipv6(self, patch1):
        """
        Unit testcase for set_vlan for ipv6
        """
        patch1.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'vlan': 1, 'lr': "LR1",
                   'range': 10, 'ipv6': "2000::BEC/64"}
        self.assertNotEqual(self.srv.set_vlan(name="ms-0/0/0", **options), None)
    #@patch('RUtils.cmd_list')

    def test_set_service_set(self):
        """
        Unit testcase for set_service_set
        """
        #patch1.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set", 'syslog': 1, 'sl_host': "local", 'nh': 1, 'base_ifl': 1,
                   'nat_rules': "NAT_RULE", 'next_hop': True, 'snmp_addr_port_low': 0,
                   'nat_rule_set': 'nr1', 'num_rule_set': 1,
                   'sfw_rule_sets': 'sfw_rule1', 'sfw_rules': 'np1',
                   'snmp_addr_port_high': 1, 'snmp_flow_low': 0, 'snmp_flow_high': 1,
                   'sset_opts': True}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0",
                                                     **options), None)
        options = {'action': "set", 'syslog': 1, 'sl_host': "local", 'nh': 1,
                   'nat_rules': "NAT_RULE", 'next_hop': True, 'snmp_addr_port_low': 0,
                   'nat_rule_set': 'nr1', 'num_rule_set': 1,
                   'sfw_rule_sets': 'sfw_rule1', 'sfw_rules': 'np1',
                   'snmp_addr_port_high': 1, 'snmp_flow_low': 0, 'snmp_flow_high': 1,
                   'sset_opts': True}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0",
                                                     **options), None)

        

        options = {'action': 'set', 'syslog': 1, 'sl_host': 'local', 'nh': 1,
                   'nat_rules': "NAT_RULE",  'snmp_addr_port_low': 0,
                   'nat_rule_set': 'nr1', 'num_rule_set': 1,
                   'sfw_rule_sets': 'sfw_rule1', 'sfw_rules': 'np1',
                   'snmp_addr_port_high': 1, 'snmp_flow_low': 0, 'snmp_flow_high': 1,
                   'sset_opts': True, 'base_ifl':0, 'ams':'cf1','ams_unit':1 }
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0",
                                                     **options), None)

        options = {'action': 'delete','del_rule':'cf1', 'syslog': 1, 'sl_host': 'local', 'nh': 1,
                   'nat_rules': "NAT_RULE",  'snmp_addr_port_low': 0,
                   'nat_rule_set': 'nr1', 'num_rule_set': 1,
                   'sfw_rule_sets': 'sfw_rule1', 'sfw_rules': 'np1',
                   'snmp_addr_port_high': 1, 'snmp_flow_low': 0, 'snmp_flow_high': 1,
                   'sset_opts': True, 'base_ifl':1  }
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0",
                                                     **options), None)


    def test_set_service_set_no_ifl(self):
        """
        Unit testcase for set_service_set with no ifl
        """
        #patch1.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set", 'syslog': 1, 'sl_host': "local", 'nh': 1,
                   'nat_rules': "NAT_RULE", 'snmp_addr_port_low': 0,
                   'snmp_addr_port_high': 1, 'snmp_flow_low': 0, 'snmp_flow_high': 1}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0",
                                                     **options), None)

    def test_set_service_set_nh_null(self):
        """
        Unit testcase for set_service_set next hop as null
        """
        #patch1.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set", 'syslog': 1, 'sl_host': "local", 'nh': 1, 'base_ifl': 1,
                   'nat_rules': "NAT_RULE", 'snmp_addr_port_low': 0,
                   'snmp_addr_port_high': 1, 'snmp_flow_low': 0, 'snmp_flow_high': 1}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0",
                                                     **options), None)

    def test_set_service_set_del1(self):
        """
        Unit testcase for set_service_set action delete
        """
        #patch1.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "delete", 'syslog': 1, 'sl_host': "local", 'nh': 1,
                   'base_ifl': 1, 'sfw_rule_sets': 'sfw_rule1',
                   'nat_rules': "NAT_RULE", 'next_hop': True, 'del_rule': "NAT_RULE"}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0",
                                                     **options), None)

    def test_set_service_set_del2(self):
        """
        Unit testcase for set_service_set action delete
        """
        #patch1.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "delete", 'syslog': 1, 'sl_host': "local", 'nh': 1, 'base_ifl': 1,
                   'nat_rules': "NAT_RULE", 'next_hop': True, 'del_rule': "NAT_RULE"}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0",
                                                     **options), None)

    def test_set_service_set_del3(self):
        """
        Unit testcase for set_service_set action delete
        """
        #patch1.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "delete", 'syslog': 1, 'sl_host': "local", 'nh': 1, 'base_ifl': 1,
                   'nat_rules': "NAT_RULE", 'next_hop': False, 'del_rule': None}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0",
                                                     **options), None)


    def test_set_interface_not_has_attribure(self):
        """
        Unit testcase for set_interface print exception
        """
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        # delattr(self.srv, 'intf')
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'unit': 1, 'inet_addr': "1.1.1.1",
                   'arp_ip': "2.2.2.2", 'inet_ss': "ss1",
                   'arp_mac': "00:14:22:01:23:45", 'inet_ss_filter_in': "ss_in",
                   'inet_ss_filter_out': "ss_out"}
        self.assertNotEqual(self.srv.set_interface(name="ms-0/0/0", **options), None)
        with self.assertRaises(MissingMandatoryArgument) as context:
            self.srv.set_interface(name=None)
        self.assertTrue('Missing mandatory argument, name' in str(context.exception))
        # self.assertNotEqual(self.srv.set_interface(name=None), None)

    #TODO to be uncommented
    # def test_set_interface_name_null(self):
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     self.srv.cmd_add = MagicMock()
    #     self.srv.cmd_list = MagicMock()
    #     options = {'action': "set"}
    #     with self.assertRaises(Exception) as context:
    #       self.srv.set_interface()
    #     self.assertTrue('Name is mandatory argument' in str(context.exception))

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_interface(self, patch_sub):
        """
        Unit testcase for set_interface success
        """
        patch_sub.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'unit': 1, 'inet_addr': "1.1.1.1",
                   'arp_ip': "2.2.2.2", 'inet_ss': "ss1",
                   'arp_mac': "00:14:22:01:23:45", 'inet_ss_filter_in': "ss_in",
                   'inet_ss_filter_out': "ss_out"}
        self.assertNotEqual(self.srv.set_interface(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_interface_v6(self, patch_sub):
        """
        Unit testcase for set_interface with ipv6
        """
        patch_sub.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'inet6_addr': "1.1.1.1",
                   'arp_ip': "2.2.2.2", 'inet6_ss': "ss1",
                   'arp_mac': "00:14:22:01:23:45", 'inet6_ss_filter_in': "ss_in",
                   'inet6_ss_filter_out': "ss_out"}
        self.assertNotEqual(self.srv.set_interface(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_interface_del(self, patch_sub):
        """
        Unit testcase for set_interface action delete
        """
        patch_sub.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "del"}
        self.assertNotEqual(self.srv.set_interface(name="ms-0/0/0", **options), None)


    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_route_instance(self, patch2):
        """
        Unit testcase for set_route_instance
        """
        patch2.return_value = None
        # delattr(self.srv, 'rt_inst')
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'index': 1, 'rt_inst': "vrf1", 'lr': "LR1",
                   'if_list': "ge-0/0/0", 'num_ifls': 1,
                   'sp_intf_nh': 1, 'base_ifl': 1, 'ifl_step': 0,
                   'sp_if_list': "ms-0/0/0", 'num_sp_ifls': 0,
                   'sp_base_ifl': 0, 'l2vpn_site': "l2vpn1",
                   'l2vpn_site_identifier': 10, 'l2vpn_interface': "ae0",
                   'l2vpn_remote_site_id': 100, 'vpls_site': "vpls1",
                   'vpls_auto_site_id': 200, 'bgp_grp_name': "brg1"}
        self.assertNotEqual(self.srv.set_route_instance(name="ms-0/0/0",
                                                        inst_type="vrf", **options), None)
        with self.assertRaises(MissingMandatoryArgument) as context:
            self.srv.set_route_instance(name=None, inst_type="")
        self.assertTrue('Missing mandatory argument, name' in str(context.exception))
        # self.assertNotEqual(self.srv.set_route_instance(name=None, inst_type=""), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_route_instance_no_lr(self, patch2):
        """
        Unit testcase for set_route_instance no lr
        """
        patch2.return_value = None
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'index': 1, 'rt_inst': "vrf1",
                   'if_list': "ge-0/0/0", 'num_ifls': 0,
                   'sp_intf_nh': 1, 'base_ifl': 1, 'ifl_step': 0,
                   'sp_if_list': "ms-0/0/0", 'num_sp_ifls': 1,
                   'sp_base_ifl': 0, 'l2vpn_site': "l2vpn1",
                   'l2vpn_site_identifier': 10, 'l2vpn_interface': "ae0",
                   'l2vpn_remote_site_id': 100, 'vpls_site': "vpls1",
                   'vpls_auto_site_id': 200, 'bgp_grp_name': "brg1"}
        self.assertNotEqual(self.srv.set_route_instance(name="ms-0/0/0",
                                                        inst_type="vrf", **options), None)

    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_set_firewall_filter(self, utils_patch):
        """
        Unit testcase for set_firewall_filter
        """
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        # delattr(self.srv, 'fw_filter')
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'family': "inet", 'policer': "policy1",
                   'count': 1, 'index': 1,
                   'if_specific': False, 'fltr_specific': False, 'in_if_specific': False,
                   'ftype': 'filter', 'src_addr': None, 'src_port': None,
                   'dst_addr': None, 'dst_port': None, 'term': ""}
        utils_patch.return_value = options
        self.assertNotEqual(self.srv.set_firewall_filter(name="ms-0/0/0", **options), None)

    @patch('re.search')
    def test_set_fw_filt_no_policer(self, patch1):
        """
        Unit testcase for set_firewall_filter no policer
        """
        patch1.return_value = True
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'family': "inet", 'count': 1, 'term': "t1",
                   "action_list": "count-ipv4",
                   'routing-instance': "vrf1"}
        self.assertNotEqual(self.srv.set_firewall_filter(name="ms-0/0/0",
                                                         **options), None)

    @patch('jnpr.toby.services.services.iputils.get_network_address')
    @patch('jnpr.toby.services.services.iputils.is_ip_ipv6')
    @patch('jnpr.toby.services.services.iputils.is_ip')
    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.iputils.get_mask')
    def test_set_route_options(self, patch4, patch3, patch2, patch1, patch5):
        """
        Unit testcase for set_route_options
        """
        patch1.return_value = 6
        patch2.return_value = True
        patch3.return_value = None
        patch4.return_value = 24
        patch5.return_value = 24
        # delattr(self.srv, 'rt_opts')
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'lr': "LR1", 'if_inet_export': "lan",
                   'family': "inet", 'rib_grp': "rib1",
                   'instance': "SP1", 'inst_step': 1, 'tag': "t1",
                   'rid': "10.10.10.1", 'as': 100,
                   'dest': "20.20.20.1", 'inst_incr_after': 1, 'qnh': "127.0.0.1",
                   'nh': "30.30.30.2", 'lnh': "40.40.40.2", 'nh_incr_after': 1, 'nt': 1}
        self.assertNotEqual(self.srv.set_route_options(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.get_network_address')
    @patch('jnpr.toby.services.services.iputils.is_ip_ipv6')
    @patch('jnpr.toby.services.services.iputils.is_ip')
    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.iputils.get_mask')
    @patch('jnpr.toby.services.services.iputils.strip_mask')
    def test_set_route_options_1(self, patch5, patch4, patch3, patch2, patch1, patch6):
        """
        Unit testcase for set_route_options
        """
        patch1.return_value = 6
        patch2.return_value = False
        patch3.return_value = None
        patch4.return_value = 24
        patch5.return_value = True
        patch6.return_value = 24
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        self.srv.config.return_value = True
        options = {'action': "set", 'lr': "LR1", 'if_inet_export': "lan",
                   'family': "inet", 'rib_grp': "rib1",
                   'instance': "SP1", 'inst_step': 1, 'tag': "t1",
                   'rid': "10.10.10.1", 'as': 100, 'dest': "20.20.20.1",
                   'inst_incr_after': 0, 'qnh': "127.0.0.1", 'nh_base_ifl': 1,
                   'lnh': "40.40.40.2", 'nh_incr_after': 1, 'nh_step': 1,
                   'nt': 1, 'nh': "50.50.50.2"}
        self.assertEqual(self.srv.set_route_options(name="ms-0/0/0", **options), True)

    @patch('jnpr.toby.services.services.iputils.get_network_address')
    @patch('jnpr.toby.services.services.iputils.is_ip_ipv6')
    @patch('jnpr.toby.services.services.iputils.is_ip')
    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.iputils.get_mask')
    @patch('jnpr.toby.services.services.iputils.strip_mask')
    def test_set_route_options_2(self, patch5, patch4, patch3, patch2, patch1, patch6):
        """
        Unit testcase for set_route_options
        """
        patch1.return_value = 6
        patch2.return_value = True
        patch3.return_value = None
        patch4.return_value = 24
        patch5.return_value = True
        patch6.return_value = 24
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        self.srv.config.return_value = True
        options = {'action': "set", 'lr': "LR1", 'if_inet_export': "lan",
                   'family': "inet", 'rib_grp': "rib1",
                   'instance': "SP1", 'inst_step': 1, 'tag': "t1",
                   'rid': "10.10.10.1", 'as': 100, 'dest': "20.20.20.1",
                   'inst_incr_after': 0, 'qnh': "127.0.0.1", 'nh_base_ifl': 1,
                   'lnh': "40.40.40.2", 'nh_incr_after': 0, 'nh_step': 1,
                   'nt': 1, 'nh': "50.50.50.2"}
        self.assertNotEqual(self.srv.set_route_options(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.get_network_address')
    @patch('jnpr.toby.services.services.iputils.is_ip_ipv6')
    @patch('jnpr.toby.services.services.iputils.is_ip')
    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.iputils.get_mask')
    @patch('jnpr.toby.services.services.iputils.strip_mask')
    def test_set_route_options_no_dst(self, patch5, patch4, patch3, patch2, patch1, patch6):
        """
        Unit testcase for set_route_options no destination
        """
        patch1.return_value = 6
        patch2.return_value = False
        patch3.return_value = None
        patch4.return_value = 24
        patch5.return_value = True
        patch6.return_value = 24
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        self.srv.config.return_value = True
        options = {'action': "set", 'lr': "LR1", 'if_inet_export': "lan",
                   'family': "inet", 'rib_grp': "rib1",
                   'inst_step': 1, 'tag': "t1", 'rid': "10.10.10.1", 'as': 100,
                   'inst_incr_after': 0, 'qnh': "127.0.0.1", 'nh_base_ifl': 1,
                   'lnh': "40.40.40.2", 'nh_incr_after': 1, 'nh_step': 1,
                   'nt': 1, 'nh': "50.50.50.2"}
        self.assertEqual(self.srv.set_route_options(name="ms-0/0/0", **options), True)


    # def test_set_inline_services(self):
    #     #patch1.return_value = None
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     self.srv.get_fpc_pic_from_ifname = MagicMock()
    #     self.srv.get_fpc_pic_from_ifname.return_value = 1, 1
    #     self.srv.cmd_add = MagicMock()
    #     self.srv.cmd_list = MagicMock()
    #     self.srv.config = MagicMock()
    #     options = {'action': "set"}
    #     self.assertEqual(self.srv.set_inline_services(sp_intf="sp-0/0/0", **options), None)
    # #@patch('RUtils.get_fpc_pic_from_ifname')

    # def test_set_tunnel_services(self):
    #     #patch1.return_value = None
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     self.srv.get_fpc_pic_from_ifname = MagicMock()
    #     self.srv.get_fpc_pic_from_ifname.return_value = 1, 1
    #     self.srv.cmd_add = MagicMock()
    #     self.srv.cmd_list = MagicMock()
    #     self.srv.config = MagicMock()
    #     options = {'action': "set"}
    #     self.assertNotEqual(self.srv.set_tunnel_services(sp_intf="sp-0/0/0", **options), None)

    #TODO to be uncommented
    # def test_set_application_name_null(self):
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     self.srv.cmd_add = MagicMock()
    #     self.srv.cmd_list = MagicMock()
    #     self.srv.config = MagicMock()
    #     options = {'action': "set"}
    #     with self.assertRaises(ValueError) as context:
    #         self.assertEqual(self.srv.set_application(**options), False)
    #     self.assertTrue('Missing mandatory argument, name' in str(context.exception))

    def test_set_application(self):
        """
        Unit testcase for set_application
        """
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        # delattr(self.srv, 'apps')
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set"}
        self.assertNotEqual(self.srv.set_application(name="apps1", **options), None)
        with self.assertRaises(MissingMandatoryArgument) as context:
            self.srv.set_application()
        self.assertTrue('Missing mandatory argument, name' in str(context.exception))
        # self.assertNotEqual(self.srv.set_application(), None)

    #TODO to be uncommented
    # def test_set_application_set_name_null(self):
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     self.srv.cmd_add = MagicMock()
    #     self.srv.cmd_list = MagicMock()
    #     self.srv.config = MagicMock()
    #     self.srv.config = MagicMock()
    #     options = {'action': "set"}
    #     with self.assertRaises(ValueError) as context:
    #         self.srv.set_application_set(**options)
    #     self.assertTrue('Missing mandatory argument' in str(context.exception))

    def test_set_application_set(self):
        """
        Unit testcase for set_application print exception
        """
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        # delattr(self.srv, 'appset')
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set"}
        self.assertNotEqual(self.srv.set_application_set(name="apps1", **options), None)
        with self.assertRaises(MissingMandatoryArgument) as context:
            self.srv.set_application_set()
        self.assertTrue('Missing mandatory argument, name' in str(context.exception))
        # self.assertNotEqual(self.srv.set_application_set(), None)

    def test_set_static_route(self):
        """
        Unit testcase for set_static_route
        """
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.set_route_options = MagicMock()
        self.srv.set_route_options.return_value = True
        options = {'ss': "ss_1", 'sp': "sp-0/0/0", 'tg': None}
        self.assertEqual(self.srv.set_static_route(**options), True)

    def test_verify(self):
        """
        Unit testcase for verify
        """
        #kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.verify_sessions_count = MagicMock()
        self.srv.verify_sessions_count.return_value = True
        options = {'ss': "ss_1", 'sp': "sp-0/0/0", 'tg': None, 'tg_sess': ""}
        self.srv.intf['intf_ss'] = {}
        self.srv.intf['intf_ss']['inet6_ss'] = 10
        self.srv.intf['intf_ss_ri_map'] = {}
        # self.srv.if_ri_map['intf_ss_ri_map'] = {}
        # self.srv.intf['intf_ss_ri_map']['intf_ss'] = {}
        #
        self.srv._get_tg_port_and_config_mapping = MagicMock()
        self.srv.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'],
                                    'dst_ips_list': ['60.1.1.2', '60.1.1.3'],
                                    'sess_list': [{'src_ip': '11.1.1.2', 'src_prt': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_prt': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_prt': '5060'}]},
                            'total': 10}
        self.assertEqual(self.srv.verify(**options), None)

    def test_port_and_config_mapping(self):
        """
        Unit testcase for _get_tg_port_and_config_mapping
        """
        self.srv = usf_services(dh=None)
        self.srv.fn_checkin = MagicMock()
        self.srv._get_tg_sess = MagicMock()
        self.srv.dd = MagicMock()
        builtins.t = MagicMock()
        self.srv.resource = 'esst480p'
        builtins.t = {'resources': {'esst480p': {'interfaces': {'intf1': {'pic': 'ms-5/0/0'}}}}}
#        self.srv.tg_sess_cnt = MagicMock()
        def test():
            """
            temp
            """
        self.srv.ss_map = {'intf': {'ms-5/0/0': '1', 'r_if': 'ms-5/0/0'}}
        self.srv._get_ss_for_intf = MagicMock()
        self.srv.fn_checkout = MagicMock()
        self.srv._get_ss_for_intf = MagicMock()
        self.srv._get_ss_for_intf.return_value = test
#        self.srv.tg_sess_cnt = {'pic0': {'ss1': 1, 'ss12': 2}}
#        self.srv.ss_map = {'intf': {'ms-5/0/0': '1'}}
        self.srv.resource = 'esst480p'
        self.srv.sset = {"1": {'intf': "", 'nat_rules': "", 'pcp_rules': ""}}
        self.srv.topo = {'intf': {'1/1': {'path': 'r0r1'}},
                         'path_res': {'esst480p': {'r0r1': ['intf1']}}}
        self.srv.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'],
                                    'dst_ips_list': ['60.1.1.2', '60.1.1.3'],
                                    'sess_list': [{'src_ip': '11.1.1.2', 'src_prt': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_prt': '5060'},
                                                  {'src_ip': '11.1.1.2', 'src_prt': '5060'}]},
                            'total': 10}
        self.assertEqual(self.srv._get_tg_port_and_config_mapping(limit=1, limit_perc=1), None)

    def test_get_ss_for_intf(self):
        """
        Unit testcase for _get_ss_for_intf
        """
        self.srv = usf_services(dh=None)
        self.srv.log = MagicMock()
        self.srv.intf = {'ms-5/0/0': {'inet_ss': 'ss1'}, 'ms-5/0/1': {}}
        #self.cgn.intf_ss = {'ms-5/0/0': 'ss1'}
        self.assertNotEqual(self.srv._get_ss_for_intf(), None)
        self.srv.intf = {'ms-5/0/0': {'inet6_ss': 'ss1'}, 'ms-5/0/1': {}}
        self.assertNotEqual(self.srv._get_ss_for_intf(), None)
        self.srv.intf = {'ms-5/0/0': {}, 'ms-5/0/1': {}}
        self.srv.if_ri_map = {'ms-5/0/0': "r1"}
        self.srv.rt_inst = {'r1': {'sp_if_list': ['ms_if']}}
        self.srv.ss_map = {'spic': {'ms_if': ''}}
        self.assertNotEqual(self.srv._get_ss_for_intf(), None)

    def test_get_tg_sess(self):
        """
        Unit testcase for _get_tg_sess
        """
        self.sv = usf_services(dh=None)
        self.sv.fn_checkin = MagicMock()
        self.sv.fn_checkout = MagicMock()
        self.assertEqual(self.sv._get_tg_sess(tg_sess=""), None)
        self.sv.tg_sess = None
        self.sv.MissingMandatoryArgument = MissingMandatoryArgument
        # self.assertNotEqual(self.sv._get_tg_sess(), "")
        with self.assertRaises(MissingMandatoryArgument) as context:
            self.sv._get_tg_sess()
        self.assertTrue('Missing mandatory argument, tg_sess' in str(context.exception))

    def test_set_address_book_address(self):
        """
        Unit testcase for set_address_book_address
        """
        self.srv = usf_services(dh=None)
        self.srv.cmd_add = MagicMock()
        self.srv.fn_checkin = MagicMock()
        self.srv.fn_checkout = MagicMock()
        self.srv.fn_checkout.return_value = True
        self.srv.config = MagicMock()
        kwargs = {'action': 'set'}
        self.assertTrue(self.srv.set_address_book_address("ad_book1", "1.1.1.1",
                                                          **kwargs), True)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.iputils.is_ip')
    def test_set_sfw_policy(self, patch1, patch2):
        """
        Unit testcase for set_sfw_policy
        """
        #patch1.return_value = "10.0.0.1"
        #patch2.return_value = "20.0.0.1"
        patch1.return_value = "10.0.0.1"
        patch2.return_value = True
        #patch3.return_value = True
        #patch4.return_value = True
        self.srv = usf_services(dh=None)
        self.srv.cmd_add = MagicMock()
        self.srv.fn_checkin = MagicMock()
        self.srv.fn_checkout = MagicMock()
        self.srv.fn_checkout.return_value = True
        self.srv.config = MagicMock()

        options = {'count': 1, 'action': 'set', 'dir': 'input',
                   'sfw_rule_set_name': 'sfw1', 'src_addr': '10.0.0.1', 'src_addr_step': 0,
                   'dst_addr': '20.0.0.1', 'dst_addr_step': 0,
                   'dst_port_low': 1, 'dst_port_high': 1,
                   'src_addr_term_step': 1, 'dst_addr_term_step': 1,
                   'src_exclude': 1, 'dst_exclude': 1,
                   'del_policy': None, 'sfw_rule_name': 'R1',
                   'del_rule': None, 'del_rule_set': None,}

        self.assertTrue(self.srv.set_sfw_policy(**options), True)

        options = {'count': 1, 'action': 'set', 'dir': 'input',
                   'sfw_rule_set_name': 'sfw1', 'src_addr': None, 'src_addr_step': 0,
                   'dst_addr': None, 'dst_addr_step': 0,
                   'src_addr_term_step': 0, 'dst_addr_term_step': 0,
                   'src_exclude': None, 'dst_exclude': None,
                   'del_policy': None, 'sfw_rule_name': 'R1',
                   'del_rule': 'NAT_RULE1', 'del_rule_set': 'NAT_RULE_SET',
                   'sfw_rule_name': 'sfw1'}

        self.assertTrue(self.srv.set_sfw_policy(**options), True)

        options = {'count': 1, 'action': 'set', 'dir': 'input',
                   'sfw_rule_set_name': 'sfw1', 'src_addr': None, 'src_addr_step': 0,
                   'dst_addr': None, 'dst_addr_step': 0,
                   'src_addr_term_step': 0, 'dst_addr_term_step': 0,
                   'src_exclude': None, 'dst_exclude': None,
                   'del_policy': None, 'sfw_rule_name': None,
                   'del_rule': None, 'del_rule_set': 'NAT_RULE_SET',
                   'sfw_rule_name': 'sfw1'}

        self.assertTrue(self.srv.set_sfw_policy(**options), True)

        options = {'count': 1, 'action': 'set', 'dir': 'input',
                   'sfw_rule_set_name': None, 'src_addr': '10.0.0.1', 'src_addr_step': 0,
                   'dst_addr': '20.0.0.1', 'dst_addr_step': 0,
                   'dst_port_low': 1, 'dst_port_high': 1,
                   'src_addr_term_step': 1, 'dst_addr_term_step': 1,
                   'src_exclude': 1, 'dst_exclude': 1,
                   'del_policy': 'None', 'sfw_rule_name': 'sfw1',
                   'del_rule': 'd1', 'del_rule_set': None,}

        self.assertTrue(self.srv.set_sfw_policy(**options), True)

        options = {'count': 1, 'action': 'set', 'dir': 'input',
                   'src_addr': None, 'src_addr_step': 0,
                   'dst_addr': None, 'dst_addr_step': 0,
                   'src_addr_term_step': 1, 'dst_addr_term_step': 1,
                   'del_policy': 'dp1',
                   'del_rule': None, 'del_rule_set': None,}

        self.assertTrue(self.srv.set_sfw_policy(**options), True)

    def test_get_usf_sfw_policy(self):
        """
        Unit testcase for get_usf_sfw_policy
        """
        self.srv = usf_services(dh=None)
        self.srv.cmd_add = MagicMock()
#        self.srv.log = MagicMock()
        self.srv.fn_checkin = MagicMock()
        self.srv.fn_checkout = MagicMock()
        self.srv.fn_checkout.return_value = True
        self.srv.get_xml_output = MagicMock()
        #policy_name = sfw_policy1
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["SFW_POLICY"])
        xml_tree = xml_tree['rpc-reply']
        #self.srv.config = MagicMock()
        _xpath = 'security-policies/security-context'
        for path in  _xpath.split('/'):
            xml_tree = xml_tree[path]
        self.srv.get_xml_output.return_value = xml_tree
#        options = {'name': {'MX1_CGN4_AMS4-CONE-p1': {'pool_type': 'source'}}}
#        options = {'name':{'MX1_CGN4_AMS4-CONE-p1':{'pool_type':{'source'}}}}
        options = {'policy_name': 'sfw_policy1'}
        #self.srv.data = {}
        self.assertEqual(self.srv.get_usf_sfw_policy(**options), xml_tree)
        self.srv.get_xml_output.return_value = None
        self.assertEqual(self.srv.get_usf_sfw_policy(**options), True)

#    def verify_usf_sfw_policy(self,

    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_verify_usf_sfw_policy(self, test_cmp_dicts):
        """
        Unit testcase for verify_usf_sfw_policy
        """
#        pathch2.return_value = '1-1'
        self.srv.get_usf_sfw_policy = MagicMock()
        self.srv._get_tg_port_and_config_mapping = MagicMock()
        self.srv._get_ss_from_pool = MagicMock()
        self.srv.result = MagicMock()
        self.srv.log = MagicMock()
        temp = MagicMock(spec=list)
        #temp.return_value = True
        #act_dict = temp
        act_dict = [{'policies': {'policy-information': {'sfw-rule-name': 'sfw_rule1',
                                                         'policy-name': 'sfw_policy1',
                                                         'policy-state': 'enabled',
                                                         'service-set-name': 'twice_nat_ss1',
                                                         'interface-name': 'vms-0/2/0',
                                                         'source-addresses': {'source-address': {'address-name': 'any'}},
                                                         'destination-addresses': {'destination-address': {'address-name': 'any'}},
                                                         'policy-action': {'action-type': 'permit'},
                                                         'match-direction': 'input-output',
                                                         'applications': {'application': [{'application-name': '1'}]}}}}]

        exp_dict = {'sfw_rule_name': 'R11', 'policy_name': 'sfw_policy1',
                    'match_direction': 'input-output'}
        test_cmp_dicts.return_value = True

        self.assertEqual(self.srv.verify_usf_sfw_policy(exp_dict,
                                                        policy_name='sfw_policy1'), True)

        exp_dict = {'sfw_rule_name' : 'R11', 'policy_name' : 'sfw_policy1',
                    'match_direction': 'input'}
        test_cmp_dicts.return_value = False
        self.assertEqual(self.srv.verify_usf_sfw_policy(exp_dict, act_dict,
                                                        policy_name='sfw_policy1'), True)

        exp_dict = {'sfw_rule_name': 'R11', 'policy_name': 'sfw_policy1',
                    'match_direction': 'input-output', 'dir_flag': True}
        test_cmp_dicts.return_value = False
        self.assertEqual(self.srv.verify_usf_sfw_policy(exp_dict, act_dict,
                                                        policy_name='sfw_policy1'), True)

    def test_get_usf_sfw_policy_hit_count(self):
        """
        Unit testcase for get_usf_sfw_policy_hit_count
        """
        self.srv = usf_services(dh=None)
        self.srv.cmd_add = MagicMock()
        self.srv.fn_checkin = MagicMock()
        self.srv.fn_checkout = MagicMock()
        self.srv.fn_checkout.return_value = True
        self.srv.get_xml_output = MagicMock()
        #policy_name = sfw_policy1
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["SFW_POLICY_HIT_COUNT"])
        xml_tree = xml_tree['rpc-reply']
        #self.srv.config = MagicMock()
        _xpath = 'policy-hit-count-service-router/policy-hit-count-service-router-entry'
        for path in  _xpath.split('/'):
            xml_tree = xml_tree[path]
        self.srv.get_xml_output.return_value = xml_tree
#        options = {'name':{'MX1_CGN4_AMS4-CONE-p1':{'pool_type':'source'}}}
#        options = {'name':{'MX1_CGN4_AMS4-CONE-p1':{'pool_type':{'source'}}}}
#        options = {'policy_name':'sfw_policy1'}
        #self.srv.data = {}
        self.srv.get_xml_output.return_value = None
        self.assertEqual(self.srv.get_usf_sfw_policy_hit_count(), True)
        self.srv.get_xml_output.return_value = xml_tree
        self.assertEqual(self.srv.get_usf_sfw_policy_hit_count(), xml_tree)

#        self.srv.get_xml_output.return_value = None
#        self.assertEqual(self.srv.get_usf_sfw_policy_hit_count(), True)


    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_verify_usf_sfw_policy_hit_count(self, test_cmp_dicts):
        """
        Unit testcase for verify_usf_sfw_policy_hit_count
        """
#        pathch2.return_value = '1-1'
        self.srv.get_usf_sfw_policy_hit_count = MagicMock()
        self.srv._get_tg_port_and_config_mapping = MagicMock()
        self.srv._get_ss_from_pool = MagicMock()
        self.srv.result = MagicMock()
        self.srv.log = MagicMock()
        temp = MagicMock(spec=list)
        exp_dict = {'policy_direction': 'input', 'policy_name': 'sfw_policy1',
                    'min__policy-hit-count-service-router-count': 1}
        act_dict = [{'policy-hit-count-service-router-policy-name': 'sfw_policy1',
                     'policy-hit-count-service-router-sfw-rule-name': 'sfw_rule11',
                     'policy-hit-count-service-router-index': 1,
                     'policy-hit-count-service-router-service-set': 'twice_nat_ss1',
                     'policy-hit-count-service-router-interface': 'vms-0/2/0',
                     'policy-hit-count-service-router-count': 0,
                     'policy-hit-count-service-router-direction': 'input'}]

        test_cmp_dicts.return_value = True
        self.assertEqual(self.srv.verify_usf_sfw_policy_hit_count(exp_dict, act_dict), True)
        test_cmp_dicts.return_value = False
        self.assertEqual(self.srv.verify_usf_sfw_policy_hit_count(exp_dict, act_dict), True)
        self.assertEqual(self.srv.verify_usf_sfw_policy_hit_count(exp_dict), True)
        act_dict = {'policy-hit-count-service-router-policy-name': 'sfw_policy1',
                     'policy-hit-count-service-router-sfw-rule-name': 'sfw_rule11',
                     'policy-hit-count-service-router-index': 1,
                     'policy-hit-count-service-router-service-set': 'twice_nat_ss1',
                     'policy-hit-count-service-router-interface': 'vms-0/2/0',
                     'policy-hit-count-service-router-count': 0,
                     'policy-hit-count-service-router-direction': 'input'}
        self.assertEqual(self.srv.verify_usf_sfw_policy_hit_count(exp_dict, act_dict), True)
        test_cmp_dicts.return_value = True
        self.assertEqual(self.srv.verify_usf_sfw_policy_hit_count(exp_dict, act_dict), True)
  #TODO to be uncommented
    # def test_verify_tg_sess_none(self):
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     self.srv.verify_sessions_count = MagicMock()
    #     self.srv.verify_sessions_count.return_value = True
    #     options = {'ss': "ss_1", 'sp': "sp-0/0/0", 'tg': None, 'tg_sess':None}
    #     self.assertEqual(self.srv.verify(**options), None)

    #TODO to be uncommented
    # def test_



if __name__ == '__main__':
    unittest.main()
