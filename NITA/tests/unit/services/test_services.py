import sys
import  unittest2 as unittest
from optparse import Values
# jnpr.toby.hldcl.juniper.routing.router import Router
from mock import patch
from mock import Mock
from mock import MagicMock
from jnpr.toby.utils.xml_tool import xml_tool
from collections import defaultdict
#from new_usf_services import usf_services

import builtins
builtins.t = {}

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

from jnpr.toby.services.services import services

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

    def setUp(self):
        self.srv = services(dh=None)
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
        builtins.t = {'resources' : {'esst480p' : { 'interfaces' : { 'intf1' : {'pic' : 'ms-5/0/0' }}}}} 
        self.srv.topo = {'intf' : {'1/1' : { 'path' : 'r0r1'}}, 'path_res' : { 'esst480p' : { 'r0r1' : ['intf1']}}}
        self.srv.intf_ss = {'ms-5/0/0' : 'ss1'}
        self.srv.sset = {'ss1': {'spic': 'ms-5/0/0', 'nat_rules': ['nr1']}}
        self.srv.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_prt': '5060'},{'src_ip': '11.1.1.2','src_prt': '5060'},{'src_ip': '11.1.1.2','src_prt': '5060'}]}, 'total': 10}
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
  # def test_services_init_null_dh(self):
  #     kwargs = { 'dh' : None}
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
        patch1.return_value = None
        # kwargs = { 'dh' : self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'src_ip': "1.1.1.1", 'dst_ip': "2.2.2.2",
                   'sw_sip': "3.3.3.3", 'sw_dip': "4.4.4.4", 'src_wc': "0.0.0.2",
                   'dst_wc': "0.0.0.2", 'sw_sip_wc': "0.0.0.2", 'sw_dip_wc': "0.0.0.2",
                   'rpm_addr': "5.5.5.5", 'rpm_addr_step': 1, 'mpls': 1, 'sl_src_addr': "6.6.6.6",
                   'next_hop': True}
        # self.srv.set_service_pic(name="ms-0/0/0",**options)
        self.assertNotEqual(self.srv.set_service_pic(name="ms-0/0/0", **options), None)        
        with self.assertRaises(MissingMandatoryArgument) as context:
          self.srv.set_service_pic(name=None)
        self.assertTrue('Missing mandatory argument, name' in str(context.exception))
        # self.assertNotEqual(self.srv.set_service_pic(name=None), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_service_pic_else(self, patch1):
        patch1.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'src_ip': "1.1.1.1", 'dst_ip': "2.2.2.2",
                   'sw_dip': "4.4.4.4", 'rpm_addr': "5.5.5.5", 'rpm_addr_step': 1,
                   'mpls': 1, 'sl_src_addr': "6.6.6.6", 'sw_sip': "3.3.3.3", 'next_hop': 0}
        self.assertNotEqual(self.srv.set_service_pic(name="ms-0/0/0", **options), None)

    def test_set_vlan_ipv4(self):
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'vlan': 1,
                   'ip': "1.1.1.1/24", 'outer_id': 100, 'range': 10}
        self.assertNotEqual(self.srv.set_vlan(name="ms-0/0/0", **options), None)

    def test_set_vlan_range_null(self):
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'vlan': 1,
                   'ip': "1.1.1.1/24", 'outer_id': 100}
        self.assertNotEqual(self.srv.set_vlan(name="ms-0/0/0", **options), None)

    def test_set_vlan_id_null(self):
        kwargs = {'dh': self.mocked_obj}
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
        patch1.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        options = {'action': "set", 'vlan': 1, 'lr': "LR1",
                   'range': 10, 'ipv6': "2000::BEC/64"}
        self.assertNotEqual(self.srv.set_vlan(name="ms-0/0/0", **options), None)
    #@patch('RUtils.cmd_list')

    def test_set_service_set(self):
        #patch1.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set", 'syslog': 1, 'sl_host': "local", 'nh': 1, 'base_ifl': 1,
                   'nat_rules': "NAT_RULE", 'next_hop': True, 'snmp_addr_port_low': 0,
                   'snmp_addr_port_high': 1, 'snmp_flow_low': 0, 'snmp_flow_high': 1}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0", **options), None)

    def test_set_service_set_no_ifl(self):
        #patch1.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set", 'syslog': 1, 'sl_host': "local", 'nh': 1,
                   'nat_rules': "NAT_RULE", 'snmp_addr_port_low': 0,
                   'snmp_addr_port_high': 1, 'snmp_flow_low': 0, 'snmp_flow_high': 1}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0", **options), None)

    def test_set_service_set_nh_null(self):
        #patch1.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set", 'syslog': 1, 'sl_host': "local", 'nh': 1, 'base_ifl': 1,
                   'nat_rules': "NAT_RULE", 'snmp_addr_port_low': 0,
                   'snmp_addr_port_high': 1, 'snmp_flow_low': 0, 'snmp_flow_high': 1}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0", **options), None)

    def test_set_service_set_del(self):
        #patch1.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "delete", 'syslog': 1, 'sl_host': "local", 'nh': 1, 'base_ifl': 1,
                   'nat_rules': "NAT_RULE", 'next_hop': True}
        self.assertNotEqual(self.srv.set_service_set(name="ms-0/0/0", intf="ge-0/0/0.0", **options), None)

    def test_set_interface_not_has_attribure(self):
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        # delattr(self.srv, 'intf')
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'unit': 1, 'inet_addr': "1.1.1.1", 'arp_ip': "2.2.2.2", 'inet_ss': "ss1",
                   'arp_mac': "00:14:22:01:23:45", 'inet_ss_filter_in': "ss_in", 'inet_ss_filter_out': "ss_out"}
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
        patch_sub.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'unit': 1, 'inet_addr': "1.1.1.1", 'arp_ip': "2.2.2.2", 'inet_ss': "ss1",
                   'arp_mac': "00:14:22:01:23:45", 'inet_ss_filter_in': "ss_in", 'inet_ss_filter_out': "ss_out"}
        self.assertNotEqual(self.srv.set_interface(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_interface_v6(self, patch_sub):
        patch_sub.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'inet6_addr': "1.1.1.1", 'arp_ip': "2.2.2.2", 'inet6_ss': "ss1",
                   'arp_mac': "00:14:22:01:23:45", 'inet6_ss_filter_in': "ss_in", 'inet6_ss_filter_out': "ss_out"}
        self.assertNotEqual(self.srv.set_interface(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_interface_del(self, patch_sub):
        patch_sub.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "del"}
        self.assertNotEqual(self.srv.set_interface(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_set_sfw_rule(self, utils_patch, patch2):
        patch2.return_value = "1.1.1.2"
        # delattr(self.srv, 'sfw_rule')
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set", 'grp_name': "group1", 'src_addr': "1.1.1.1", 'dst_addr': "2.2.2.2",
                   'src_addr_step_term': 1, 'dst_addr_step_term': 1, 'dst_port_high': 1000, 'dst_port_low': 1,
                   'rs_name': "rs1", 'direction': "input", 'term': "one", 'from_src_pfx_list': "SFW_NAT44_TRF",
                   'dst_except_list': "SFW_NAT44_EXCEPT", 'action_list': "accept",'count': 1, 'action': 'set', 'dir': 'input-output',
                                               'term': 0, 'num_terms': 1,
                                               'src_addr': '1.1.1.1', 'src_addr_step': 0,
                                               'src_addr_term_step': 1,
                                               'dst_addr':'1.1.1.1', 'dst_addr_step': 0,
                                               'dst_addr_term_step': 1}
        utils_patch.return_value = options
        self.assertNotEqual(self.srv.set_sfw_rule(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_set_sfw_rule_no_grp(self, utils_patch, patch2):
        patch2.return_value = "1.1.1.2"
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set", 'src_addr': "1.1.1.1", 'dst_addr': "2.2.2.2",
                   'src_addr_step_term': 1, 'dst_addr_step_term': 1, 'dst_port_high': 1000, 'dst_port_low': 1,
                   'rs_name': "rs1", 'direction': "input", 'term': "one", 'from_src_pfx_list': "SFW_NAT44_TRF",
                   'dst_except_list': "SFW_NAT44_EXCEPT", 'action_list': "accept", 'grp_name':"abc",'count': 1, 'action': 'set', 'dir': 'input-output',
                                               'term': 0, 'num_terms': 1, 'rs_name': None,
                                               'src_addr': None, 'src_addr_step': 0,
                                               'src_addr_term_step': 0,
                                               'dst_addr': None, 'dst_addr_step': 0,
                                               'dst_addr_term_step': 0, 'grp_name': None,}
        utils_patch.return_value = options
        self.assertNotEqual(self.srv.set_sfw_rule(name="ms-0/0/0", **options), None)

    # def test_set_sfw_rule_mis

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_route_instance(self, patch2):
        patch2.return_value = None
        # delattr(self.srv, 'rt_inst')
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'index': 1, 'rt_inst': "vrf1", 'lr': "LR1", 'if_list': "ge-0/0/0", 'num_ifls': 1,
                   'sp_intf_nh': 1, 'base_ifl': 1, 'ifl_step': 0, 'sp_if_list': "ms-0/0/0", 'num_sp_ifls': 0,
                   'sp_base_ifl': 0, 'l2vpn_site': "l2vpn1", 'l2vpn_site_identifier': 10, 'l2vpn_interface': "ae0",
                   'l2vpn_remote_site_id': 100, 'vpls_site': "vpls1", 'vpls_auto_site_id': 200, 'bgp_grp_name': "brg1"}
        self.assertNotEqual(self.srv.set_route_instance(name="ms-0/0/0", inst_type="vrf", **options), None)
        with self.assertRaises(MissingMandatoryArgument) as context:
          self.srv.set_route_instance(name=None, inst_type="")
        self.assertTrue('Missing mandatory argument, name' in str(context.exception))
        # self.assertNotEqual(self.srv.set_route_instance(name=None, inst_type=""), None)

    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    def test_set_route_instance_no_lr(self, patch2):
        patch2.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'index': 1, 'rt_inst': "vrf1", 'if_list': "ge-0/0/0", 'num_ifls': 0,
                   'sp_intf_nh': 1, 'base_ifl': 1, 'ifl_step': 0, 'sp_if_list': "ms-0/0/0", 'num_sp_ifls': 1,
                   'sp_base_ifl': 0, 'l2vpn_site': "l2vpn1", 'l2vpn_site_identifier': 10, 'l2vpn_interface': "ae0",
                   'l2vpn_remote_site_id': 100, 'vpls_site': "vpls1", 'vpls_auto_site_id': 200, 'bgp_grp_name': "brg1"}
        self.assertNotEqual(self.srv.set_route_instance(name="ms-0/0/0", inst_type="vrf", **options), None)

    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_set_firewall_filter(self, utils_patch):
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        # delattr(self.srv, 'fw_filter')
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'family': "inet", 'policer': "policy1", 'count': 1, 'action': 'set', 'index': 1,
                                               'if_specific': False, 'fltr_specific': False,'in_if_specific': False,
                                               'ftype': 'filter',
                                               'src_addr': None, 'src_port': None,
                                               'dst_addr': None, 'dst_port': None, 'term' : ""}
        utils_patch.return_value = options
        self.assertNotEqual(self.srv.set_firewall_filter(name="ms-0/0/0", **options), None)

    @patch('re.search')
    def test_set_firewall_filter_no_policer(self, patch1):
        patch1.return_value = True
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'family': "inet", 'count': 1, 'term': "t1", "action_list": "count-ipv4",
                   'routing-instance': "vrf1"}
        self.assertNotEqual(self.srv.set_firewall_filter(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.get_network_address')
    @patch('jnpr.toby.services.services.iputils.is_ip_ipv6')
    @patch('jnpr.toby.services.services.iputils.is_ip')
    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.iputils.get_mask')
    def test_set_route_options(self, patch4, patch3, patch2, patch1, patch5):
        patch1.return_value = 6
        patch2.return_value = True
        patch3.return_value = None
        patch4.return_value = 24
        patch5.return_value = 24
        # delattr(self.srv, 'rt_opts')
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        options = {'action': "set", 'lr': "LR1", 'if_inet_export': "lan", 'family': "inet", 'rib_grp': "rib1",
                   'instance': "SP1", 'inst_step': 1, 'tag': "t1", 'rid': "10.10.10.1", 'as': 100,
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
        patch1.return_value = 6
        patch2.return_value = False
        patch3.return_value = None
        patch4.return_value = 24
        patch5.return_value = True
        patch6.return_value = 24
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        self.srv.config.return_value = True
        options = {'action': "set", 'lr': "LR1", 'if_inet_export': "lan", 'family': "inet", 'rib_grp': "rib1",
                   'instance': "SP1", 'inst_step': 1, 'tag': "t1", 'rid': "10.10.10.1", 'as': 100, 'dest': "20.20.20.1",
                   'inst_incr_after': 0, 'qnh': "127.0.0.1", 'nh_base_ifl': 1,
                   'lnh': "40.40.40.2", 'nh_incr_after': 1, 'nh_step': 1, 'nt': 1, 'nh': "50.50.50.2"}
        self.assertEqual(self.srv.set_route_options(name="ms-0/0/0", **options), True)

    @patch('jnpr.toby.services.services.iputils.get_network_address')
    @patch('jnpr.toby.services.services.iputils.is_ip_ipv6')
    @patch('jnpr.toby.services.services.iputils.is_ip')
    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.iputils.get_mask')
    @patch('jnpr.toby.services.services.iputils.strip_mask')
    def test_set_route_options_2(self, patch5, patch4, patch3, patch2, patch1, patch6):
        patch1.return_value = 6
        patch2.return_value = True
        patch3.return_value = None
        patch4.return_value = 24
        patch5.return_value = True
        patch6.return_value = 24
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        self.srv.config.return_value = True
        options = {'action': "set", 'lr': "LR1", 'if_inet_export': "lan", 'family': "inet", 'rib_grp': "rib1",
                   'instance': "SP1", 'inst_step': 1, 'tag': "t1", 'rid': "10.10.10.1", 'as': 100, 'dest': "20.20.20.1",
                   'inst_incr_after': 0, 'qnh': "127.0.0.1", 'nh_base_ifl': 1,
                   'lnh': "40.40.40.2", 'nh_incr_after': 0, 'nh_step': 1, 'nt': 1, 'nh': "50.50.50.2"}
        self.assertNotEqual(self.srv.set_route_options(name="ms-0/0/0", **options), None)

    @patch('jnpr.toby.services.services.iputils.get_network_address')
    @patch('jnpr.toby.services.services.iputils.is_ip_ipv6')
    @patch('jnpr.toby.services.services.iputils.is_ip')
    @patch('jnpr.toby.services.services.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.services.iputils.get_mask')
    @patch('jnpr.toby.services.services.iputils.strip_mask')
    def test_set_route_options_no_dst(self, patch5, patch4, patch3, patch2, patch1, patch6):
        patch1.return_value = 6
        patch2.return_value = False
        patch3.return_value = None
        patch4.return_value = 24
        patch5.return_value = True
        patch6.return_value = 24
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        self.srv.config.return_value = True
        options = {'action': "set", 'lr': "LR1", 'if_inet_export': "lan", 'family': "inet", 'rib_grp': "rib1",
                   'inst_step': 1, 'tag': "t1", 'rid': "10.10.10.1", 'as': 100,
                   'inst_incr_after': 0, 'qnh': "127.0.0.1", 'nh_base_ifl': 1,
                   'lnh': "40.40.40.2", 'nh_incr_after': 1, 'nh_step': 1, 'nt': 1, 'nh': "50.50.50.2"}
        self.assertEqual(self.srv.set_route_options(name="ms-0/0/0", **options), True)

    def test_set_chassis_services(self):
        #patch1.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        # delattr(self.srv, 'ch_svc')
        self.srv.get_fpc_pic_from_ifname = MagicMock()
        self.srv.get_fpc_pic_from_ifname.return_value = 1, 1
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.config = MagicMock()
        options = {'action': "set"}
        self.assertNotEqual(self.srv.set_chassis_services(sp_intf="sp-0/0/0", **options), None)

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
        kwargs = {'dh': self.mocked_obj}
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
        kwargs = {'dh': self.mocked_obj}
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

    @patch('jnpr.toby.services.services.time.sleep')
    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_clear_session_statistics(self, patch1, time_patch):
        my_dict = {'sfw': 1, 'nat': 1, 'nat_map': 1,
                   'alg': 1, 'analysis': 1, 'to_ok_all': 0}
        patch1.return_value = my_dict
        time_patch.return_value = None
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.dh = Values()
        self.srv.dh.cli = MagicMock()
        self.srv.config = MagicMock()
        options = {'sfw': 1, 'nat': 1, 'nat_map': 1, 'alg': 1, 'analysis': 1}
        self.assertEqual(self.srv.clear_session_statistics(**options), None)

    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_get_clear_sessions(self, patch1):
        my_dict = {'ss': 1, 'src_pfx': 1, 'timeout': 0}
        patch1.return_value = my_dict
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(
            xml_str=self.response["CLR_SRV_SESS"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'service-msp-sess-drain-information/service-msp-sess-drain'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        if not isinstance(xml_tree, list):
            xml_tree = [xml_tree]
        self.srv.get_xml_output.return_value = xml_tree
        # print(self.srv.get_xml_output.return_value)
        options = {'ss': 1, 'src_pfx': 1, 'timeout': 0}
        self.srv.config = MagicMock()
        
        self.assertNotEqual(self.srv.get_clear_sessions(**options), None)

    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_get_clear_sessions_1(self, patch1):
        my_dict = {'ss': 1, 'src_pfx': 1, 'timeout': 0}
        patch1.return_value = my_dict
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(
            xml_str=self.response["CLR_SRV_SESS_1"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'service-msp-sess-drain-information/service-msp-sess-drain'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        if not isinstance(xml_tree, list):
            xml_tree = [xml_tree]
        self.srv.get_xml_output.return_value = xml_tree
        # print(self.srv.get_xml_output.return_value)
        options = {'ss': 1, 'src_pfx': 1, 'timeout': 0}
        self.srv.config = MagicMock()
        self.assertNotEqual(self.srv.get_clear_sessions(**options), None)

    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_get_clear_sessions_rmv(self, patch1):
        my_dict = {'ss': 1, 'src_pfx': 1, 'timeout': 0}
        patch1.return_value = my_dict
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.cmd_add = MagicMock()
        self.srv.cmd_list = MagicMock()
        self.srv.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(
            xml_str=self.response["CLR_SRV_SESS_RMV"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'service-msp-sess-drain-information/service-msp-sess-drain'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        if not isinstance(xml_tree, list):
            xml_tree = [xml_tree]
        self.srv.get_xml_output.return_value = xml_tree
        # print(self.srv.get_xml_output.return_value)
        options = {'ss': 1, 'src_pfx': 1, 'timeout': 0}
        self.srv.config = MagicMock()
        self.assertNotEqual(self.srv.get_clear_sessions(**options), None)

    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_clear_sessions(self, patch1):
        my_dict = {'num_sess': 0, 'verify': True}
        patch1.return_value = my_dict
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.get_clear_sessions = MagicMock()
        data = {'total_sess_cleared': 0}
        self.srv.get_clear_sessions.return_value = data
        self.srv.num_sess = 0
        # self.srv.dh.cli = MagicMock()
        # self.srv.dh.cli.return_value =  ""
        self.srv.verify_sessions_count = MagicMock()
        self.srv.verify_sessions_count.return_value = True
        options = {'verify': True}
        self.srv.config = MagicMock()
        self.assertEqual(self.srv.clear_sessions(**options), True)

    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_clear_sessions_no_verify(self, patch1):
        my_dict = {'num_sess': 0, 'verify': True}
        patch1.return_value = my_dict
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.get_clear_sessions = MagicMock()
        data = {'total_sess_cleared': 0}
        self.srv.get_clear_sessions.return_value = data
        self.srv.num_sess = 1
        self.srv.verify_sessions_count = MagicMock()
        self.srv.verify_sessions_count.return_value = True
        options = {'verify': True}
        self.srv.config = MagicMock()
        self.assertNotEqual(self.srv.clear_sessions(**options), "")

    def test_get_sessions_count(self):
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        #self.srv.dd = MagicMock
        self.srv.dd = {}
        self.srv.dd = lambda:defaultdict(self.srv.dd)
        self.srv.dd.return_value = self.srv.dd()
        self.srv.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(
            xml_str=self.response["GET_SESS_CNT"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'service-msp-sess-count-information/service-msp-sess-count'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        if not isinstance(xml_tree, list):
            xml_tree = [xml_tree]
        self.srv.get_xml_output.return_value = xml_tree
        # options = {'sess_count': 1}
        options = {}
        self.srv.config = MagicMock()
        # self.srv.get_sessions_count(**options)
        self.assertNotEqual(self.srv.get_sessions_count(**options), None)

    def test_get_sessions_count_1(self):
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        #self.srv.dd = MagicMock
        #dd = {}
        #dd = lambda:defaultdict(dd)
        #self.srv.dd.return_value = dd()
        self.srv.get_xml_output = MagicMock()
        self.srv.dd = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(
            xml_str=self.response["GET_SESS_CNT_1"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'service-msp-sess-count-information/service-msp-sess-count'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        if not isinstance(xml_tree, list):
            xml_tree = [xml_tree]
        self.srv.get_xml_output.return_value = xml_tree
        # options = {'sess_count': 1}
        options = {}

        self.assertNotEqual(self.srv.get_sessions_count(**options), None)



    def test_set_static_route(self):
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.set_route_options = MagicMock()
        self.srv.set_route_options.return_value = True
        options = {'ss': "ss_1", 'sp': "sp-0/0/0", 'tg': None}
        self.assertEqual(self.srv.set_static_route(**options), True)

    def test_verify(self):
        kwargs = {'dh': self.mocked_obj}
        # srv = services(dh=kwargs)
        self.srv.verify_sessions_count = MagicMock()
        self.srv.verify_sessions_count.return_value = True
        options = {'ss': "ss_1", 'sp': "sp-0/0/0", 'tg': None, 'tg_sess':""}
        self.srv.intf['intf_ss'] = {}
        self.srv.intf['intf_ss']['inet6_ss'] = 10
        self.srv.intf['intf_ss_ri_map'] = {}
        # self.srv.if_ri_map['intf_ss_ri_map'] = {}
        # self.srv.intf['intf_ss_ri_map']['intf_ss'] = {}
        #
        self.srv._get_tg_port_and_config_mapping = MagicMock()
        self.srv.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_prt': '5060'},{'src_ip': '11.1.1.2','src_prt': '5060'},{'src_ip': '11.1.1.2','src_prt': '5060'}]}, 'total': 10}
        self.assertEqual(self.srv.verify(**options), None)

  #TODO to be uncommented
    # def test_verify_tg_sess_none(self):
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     self.srv.verify_sessions_count = MagicMock()
    #     self.srv.verify_sessions_count.return_value = True
    #     options = {'ss': "ss_1", 'sp': "sp-0/0/0", 'tg': None, 'tg_sess':None}
    #     self.assertEqual(self.srv.verify(**options), None)

    def test_verify_sessions_count_total_zero(self):
        self.srv.get_sessions_count = MagicMock()
        data = {'total': 0, 'sp': "sp-0/0/0"}
        self.srv.get_sessions_count.return_value = data
        self.assertEqual(self.srv.verify_sessions_count(), False)

    @patch('jnpr.toby.services.services.utils.cmp_val')
    def test_verify_sessions_count_cmp_val(self, utils_patch):
        utils_patch.return_value = True
        self.srv.get_sessions_count = MagicMock()
        data = {'total': 1, 'sp': "sp-0/0/0", 'sp1':{"ss1":{}}}
        self.srv.get_sessions_count.return_value = data
        self.assertEqual(self.srv.verify_sessions_count(sp="sp1", ss="ss1", count=""), True)

    def test_verify_sessions_count_tg_sess_cnt_none(self):
        self.srv.get_sessions_count = MagicMock()
        data = {'total': 1, 'sp': "sp-0/0/0"}
        self.srv.get_sessions_count.return_value = data
        self.srv.tg_sess_cnt = None
        self.assertEqual(self.srv.verify_sessions_count(), True)

    @patch('jnpr.toby.services.services.utils.cmp_val')
    def test_verify_sessions_count(self, utils_patch):
        self.srv.get_sessions_count = MagicMock()
        data = {'total': 1, 'sp': "sp-0/0/0" , 'sp':{"ss1":{}} }
        self.srv.get_sessions_count.return_value = data
        self.srv.tg_sess_cnt = { 'sp1' : {} , 'sp' : { 'total': 0, 'ss2' : {}, 'ss1': '' }}
        self.assertEqual(self.srv.verify_sessions_count(), True)



    # def test_verify_sessions_count_ss_null(self):
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     data = {'total': 1, 'ss': "ss_1"}
    #     dct = {'ss': "ss_1"}
    #     opt = {}
    #     opt['sp-0/0/0'] = dct
    #     self.srv.get_sessions_count = MagicMock()
    #     self.srv.get_sessions_count.return_value = data
    #     self.srv.get_sess_cnt_per_ss = MagicMock()
    #     self.srv.get_sess_cnt_per_ss.return_value = opt
    #     options = {'ss': "ss_1", 'sp': "sp-0/0/0", 'tg': None}
    #     self.assertNotEqual(self.srv.verify_sessions_count(tol_val=None, tol_perc=None, **options), "")


    # @patch('jnpr.toby.services.services.utils.cmp_val')
    # def test_verify_sessions_count_ss_null_new(self, patch1):
    #     patch1.return_value = True
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     data = {'total': 1, 'sp': "ms-0/0/0"}
    #     #dct = {'ss': "ss_1"}
    #     opt = {}
    #     opt['sp'] = {}
    #     #opt['sp'] =  "ms-0/0/0"
    #     #opt['sp']['ss']=  {}
    #     opt['sp']['ss'] = "ss_1"
    #     self.srv.get_sessions_count = MagicMock()
    #     self.srv.get_sessions_count.return_value = data
    #     self.srv.get_sess_cnt_per_ss = MagicMock()
    #     self.srv.get_sess_cnt_per_ss.return_value = opt
    #     options = {'ss': "ss_1", 'sp': "ms-0/0/0", 'tg': None}
    #     options = {'ss': "ss_1", 'sp': "ms-0/0/0", 'tg': None}

    #     # self.srv.get_xml_output = MagicMock()
    #     self.assertNotEqual(self.srv.verify_sessions_count(tol_val=10, tol_perc=10, **options), "")

    # @patch('jnpr.toby.services.services.utils.cmp_val')
    # def test_verify_sessions_count_no_sess(self, patch1):
    #     patch1.return_value = True
    #     #dd = {}
    #     #dd = lambda:defaultdict(dd)
    #     opt = {}
    #     opt['ms-4/0/0'] = {}
    #     opt['total'] = 1
    #     opt['ms-4/0/0']['service_set'] = {}
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     data = {'total': 0}
    #     self.srv.get_sessions_count = MagicMock()
    #     self.srv.get_sessions_count.return_value = data
    #     options = {'ss': "service_set",
    #                'sp': "ms-4/0/0", 'count': 1, 'tg': None}
    #     self.assertEqual(self.srv.verify_sessions_count(tol_val=None, tol_perc=None, **options), False)


    # @patch('jnpr.toby.services.services.utils.cmp_val')
    # def test_verify_sessions_count(self, patch1):
    #     patch1.return_value = True
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     data = {'total': 1}
    #     dct = {'ss': "service_set"}
    #     opt = {}
    #     opt['ms-4/0/0'] = {}
    #     opt['total'] = 1
    #     opt['ms-4/0/0']['service_set'] = {}
    #     #opt['sp']['ss'] = "ss_1"
    #     self.srv.get_sessions_count = MagicMock()
    #     self.srv.get_sessions_count.return_value = opt
    #     options = {'ss': "service_set",
    #                'sp': "ms-4/0/0", 'count': 1, 'tg': None}
    #     self.assertEqual(self.srv.verify_sessions_count(tol_val=None, tol_perc=None, **options), True)

    # @patch('jnpr.toby.services.services.utils.cmp_val')
    # def test_verify_sessions_count_0(self, patch1):
    #     patch1.return_value = True
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     data = {'total': 0}
    #     #dct = {'ss': "1"}
    #     #opt = {}
    #     #opt['ms-4/0/0'] = {}
    #     #opt['total'] = 1
    #     #opt['ms-4/0/0']['service_set'] = {}
    #     self.srv.get_sessions_count = MagicMock()
    #     self.srv.get_sessions_count.return_value = data
    #     #self.srv.get_sess_cnt_per_ss = MagicMock()
    #     #self.srv.get_sess_cnt_per_ss.return_value = opt
    #     options = {'ss': "ss_1", 'sp': "ms-4/0/0", 'tg': None}
    #     self.assertEqual(self.srv.verify_sessions_count(tol_val=None, tol_perc=None, **options), False)

    # @patch('jnpr.toby.services.services.utils.cmp_val')
    # def test_verify_sessions_count_ss_1(self, patch1):
    #     patch1.return_value = True
    #     kwargs = {'dh': self.mocked_obj}
    #     # srv = services(dh=kwargs)
    #     data = {'total': 1, 'sp': {'ss': "ss_1"}}
    #     #dct = {'ss': "ss_1"}
    #     opt = {}
    #     opt['sp'] = {}
    #     #opt['sp'] =  "ms-0/0/0"
    #     #opt['sp']['ss']=  {}
    #     opt['sp']['ss'] = "ss_1"
    #     self.srv.get_sessions_count = MagicMock()
    #     self.srv.get_sessions_count.return_value = data
    #     self.srv.get_sess_cnt_per_ss = MagicMock()
    #     self.srv.get_sess_cnt_per_ss.return_value = opt
    #     options = {'ss': "ss_1", 'sp': "ms-0/0/0", 'tg': None}
    #     self.assertNotEqual(self.srv.verify_sessions_count(tol_val=10, tol_perc=10, **options), "")

    #TODO to be uncommented
    # def test_get_sess_cnt_per_ss_fail(self):
    #     with self.assertRaises(ValueError) as context:
    #       self.srv.get_sess_cnt_per_ss()
    #     self.assertTrue("Missing mandatory argument, " in str(context.exception))

    def test_get_sess_cnt_per_ss_tg_not_none(self):
        tg = Values()
        tg.get_sessions = MagicMock()
        tg.get_sessions.return_value = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_prt': '5060'},{'src_ip': '11.1.1.2','src_prt': '5060'},{'src_ip': '11.1.1.2','src_prt': '5060'}]}, 'total': 10}
        self.srv._get_ss_for_intf = MagicMock()
        # self.srv.intf_ss = {'ms-5/0/0': {'inet_ss': 'ss1'}, 'ms-5/0/1': {}}
        self.srv.dd.return_value = {'1': {"1":''}}
        self.srv.ss_map = {'intf': {'ms-5/0/0': '1'}}
        self.srv.sset = { "1" : { 'intf':"1", 'nat_rules':"", 'pcp_rules':""}}
        self.assertNotEqual(self.srv.get_sess_cnt_per_ss(tg), None)
        # def test(s):
          # self.tg_sess = ""
        # self.srv.MissingMandatoryArgument.return_value = None  
        with self.assertRaises(MissingMandatoryArgument) as context:
          self.srv.get_sess_cnt_per_ss()
        self.assertTrue('Missing mandatory argument, tg/tg_sess' in str(context.exception))
        # self.assertNotEqual(self.srv.get_sess_cnt_per_ss(), "")
        # self.assertNotEqual(self.srv.get_sess_cnt_per_ss(tg), None)

    def test_get_ss_for_intf(self):

        self.srv = services(dh=None)
        self.srv.log = MagicMock()
        self.srv.intf = {'ms-5/0/0': {'inet_ss': 'ss1'}, 'ms-5/0/1': {}}
        #self.cgn.intf_ss = {'ms-5/0/0' : 'ss1'}
        self.assertNotEqual(self.srv._get_ss_for_intf(), None)
        self.srv.intf = {'ms-5/0/0': {'inet6_ss': 'ss1'}, 'ms-5/0/1': {}}
        self.assertNotEqual(self.srv._get_ss_for_intf(), None)
        self.srv.intf = {'ms-5/0/0': {}, 'ms-5/0/1': {}}
        self.srv.if_ri_map = {'ms-5/0/0': "r1"}
        self.srv.rt_inst = {'r1':{'sp_if_list': ['ms_if']}}
        self.srv.ss_map = {'spic':{'ms_if':''}}
        self.assertNotEqual(self.srv._get_ss_for_intf(), None)

    @patch('jnpr.toby.services.services.utils.update_opts_from_args')
    def test_set_policy_options(self, utils_update):
        options = { 'from_rt_filter':1, 'name':'policy','count': 5, 'action': 'set', 'term': 1,
                                               'num_terms': 1,                                                'from_rt_filter_exact': False,
                                               'then_cmnty_add_step': False,
                                               'from_cmnty_add_step': False,
                                               'cmnty_mbrs_cmnty_step': False,
                                               'cmnty_mbrs_mbrs_step': False,}
        utils_update.return_value = options
        self.assertEqual(self.srv.set_policy_options(**options), True)
        # with lr in this
        options = {'cmnty_mbrs_dict':{'key':[0]}, 'pfx_dict': { "prfx": ["0"]},'from_rt_filter':1, 'lr': 0, 'name':'policy', 'count': 5, 'action': 'set', 'term': 1,
                                               'num_terms': 1,                                                'from_rt_filter_exact': True,
                                               'then_cmnty_add_step': True,
                                               'from_cmnty_add_step': True,
                                               'cmnty_mbrs_cmnty_step': True,
                                               'cmnty_mbrs_mbrs_step': True,}
        utils_update.return_value = options
        self.assertEqual(self.srv.set_policy_options(**options), True)

    def test_get_sessions_analysis(self):
        self.srv.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(
            xml_str=self.response["analysis"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'service-session-analysis-information/service-session-analysis-entry'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        if not isinstance(xml_tree, list):
            xml_tree = [xml_tree]
        self.srv.get_xml_output.return_value = xml_tree
        self.assertNotEqual(self.srv.get_sessions_analysis(spic="spic"), False)
        self.srv.get_xml_output.return_value = None
        self.assertNotEqual(self.srv.get_sessions_analysis(), False)

    @patch('jnpr.toby.services.services.utils.cmp_dicts')
    def test_verify_sessions_analysis(self, utils_patch):
        utils_patch.return_value = MagicMock()
        self.srv.get_sessions_analysis = MagicMock()
        self.srv._get_tg_port_and_config_mapping = MagicMock()
        data = {'total': 1, 'sp': "sp-0/0/0", 'sp': {"ss1": {} }}
        self.srv.get_sessions_analysis.return_value = data
        self.srv.tg_sess_cnt = {'sp1': {}, 'sp': {
            'total': 0, 'ss2': {}, 'ss1': '' , 'total_sess':10}}
        self.assertEqual(self.srv.verify_sessions_analysis(
            sess_active_total="10"), True)

    def test_get_service_sets_cpu_usage(self):
        self.srv.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["cpu_usage"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'service-set-cpu-statistics-information/service-set-cpu-statistics'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        if not isinstance(xml_tree, list):
            xml_tree = [xml_tree]
        self.srv.get_xml_output.return_value = xml_tree 
        self.assertNotEqual(self.srv.get_service_sets_cpu_usage(spic="spic", sset="sset"), False)
        # self.srv.get_xml_output.return_value = None
        # self.assertNotEqual(self.srv.get_service_sets_cpu_usage(), False)

    @patch('jnpr.toby.services.services.utils.cmp_val')
    def test_verify_service_sets_cpu_usage(self, utils_patch):
        utils_patch.return_value = MagicMock()
        self.srv.get_service_sets_cpu_usage = MagicMock()
        self.srv._get_tg_port_and_config_mapping = MagicMock()
        data = {'total': 1, 'sp': "sp-0/0/0", 'sp': {"ss1": {} }}
        self.srv.get_service_sets_cpu_usage.return_value = data
        self.srv.tg_sess_cnt = {'sp1': {}, 'sp': {
            'total': 0, 'ss2': {}, 'ss1': '' , 'total_sess':10}}
        self.assertEqual(self.srv.verify_service_sets_cpu_usage(), True)

    def test_get_service_sets_summary(self):
        self.srv.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["ss_summary"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'service-set-summary-information/service-set-summary-information-entry'
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        if not isinstance(xml_tree, list):
            xml_tree = [xml_tree]
        self.srv.get_xml_output.return_value = xml_tree 
        self.assertNotEqual(self.srv.get_service_sets_summary(), False)


    @patch('jnpr.toby.services.services.utils.cmp_dicts')
    def test_verify_service_sets_summary(self, utils_patch):
        utils_patch.return_value = MagicMock()
        self.srv.get_service_sets_summary = MagicMock()
        self.srv._get_tg_port_and_config_mapping = MagicMock()
        data = {'total': 1, 'sp': "sp-0/0/0", 'sp': {"ss1": {} }}
        self.srv.get_service_sets_summary.return_value = data
        self.srv.tg_sess_cnt = {'sp1': {}, 'sp': {
            'total': 0, 'ss2': {}, 'ss1': '' , 'total_sess':10}}
        self.assertNotEqual(self.srv.verify_service_sets_summary(
            sess_active_total="10"), "")

    def test_clear_log_messages(self):
        self.srv.dh = Values()
        self.srv.dh.cli = MagicMock()
        self.srv.dh.cli.return_value = ""
        self.assertEqual(self.srv.clear_log_messages(), True)

    def test_get_tg_sess(self):
        self.sv = services(dh=None)
        self.sv.fn_checkin = MagicMock()
        self.sv.fn_checkout = MagicMock()
        self.assertEqual(self.sv._get_tg_sess(tg_sess=""), None)
        self.sv.tg_sess = None
        self.sv.MissingMandatoryArgument = MissingMandatoryArgument
        # self.assertNotEqual(self.sv._get_tg_sess(), "")
        with self.assertRaises(MissingMandatoryArgument) as context:
          self.sv._get_tg_sess()
        self.assertTrue('Missing mandatory argument, tg_sess' in str(context.exception))

    def test_get_tg_port_and_config_mapping(self):
        self.sv = services(dh=None)
        self.sv.fn_checkin = MagicMock()
        self.sv._get_tg_sess = MagicMock()
        def test():
          self.sv.ss_map = {'intf': {'ms-5/0/0': '1'}}
        self.sv._get_ss_for_intf = MagicMock() 
        self.sv.fn_checkout = MagicMock() 
        self.sv._get_ss_for_intf = MagicMock() 
        self.sv._get_ss_for_intf.return_value = test
        self.sv.ss_map = {'intf': {'ms-5/0/0': '1'}}
        self.sv.resource = 'esst480p'
        self.sv.sset = { "1" : { 'intf':"", 'nat_rules':"", 'pcp_rules':""}}
        self.sv.topo = {'intf' : {'1/1' : { 'path' : 'r0r1'}}, 'path_res' : { 'esst480p' : { 'r0r1' : ['intf1']}}}
        self.sv.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_prt': '5060'},{'src_ip': '11.1.1.2','src_prt': '5060'},{'src_ip': '11.1.1.2','src_prt': '5060'}]}, 'total': 10}
        self.assertEqual(self.sv._get_tg_port_and_config_mapping(limit=1, limit_perc=1), None)

    @patch('jnpr.toby.services.services.time.sleep')
    @patch('jnpr.toby.services.services.utils.get_time_diff')
    @patch('jnpr.toby.services.services.utils.cmp_val')
    def test_verify_syslog_pba(self, cmp_patch, diff_patch, time_patch):
        cmp_patch.return_value = True
        diff_patch.return_value = 50
        test = Values()
        test.response = MagicMock()
        test.response.return_value = '''Oct 30 21:46:04  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:46:04 [FWNAT]:ASP_NAT_PORT_BLOCK_ALLOC: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099
Oct 30 21:48:35  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:48:34 [FWNAT]:ASP_NAT_PORT_BLOCK_RELEASE: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099'''

        self.srv.dh = Values()
        self.srv.dh.cli = MagicMock()
        self.srv.dh.cli.return_value = test
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=50, ip='3002:0:0:0:0:0:0:1', port_blk='1000'), True)
        #incorrect block size, diff port, ip
        cmp_patch.return_value = False
        test.response.return_value = '''Oct 30 21:46:04  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:46:04 [FWNAT]:ASP_NAT_PORT_BLOCK_ALLOC: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099
Oct 30 21:48:35  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:48:34 [FWNAT]:ASP_NAT_PORT_BLOCK_RELEASE: 3002:0:0:0:0:0:0:2 -> 33.33.0.3:-1-1090'''
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=5), False)
        # #detnat return true
        cmp_patch.return_value = False
        test.response.return_value = ''''''

        self.srv.dh.cli.return_value = test
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=5, detnat=1), True)
        
        cmp_patch.return_value = False
        test.response.return_value = '''Oct 30 21:48:35  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:48:34 [FWNAT]:ASP_NAT_PORT_BLOCK_RELEASE: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099'''

        self.srv.dh.cli.return_value = test
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=5, detnat=1), False)
        # #detnat else condition return false

        self.srv.dh.cli.return_value = test
        test.response.return_value = '''Oct 30 21:46:04  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:46:04 [FWNAT]:ASP_NAT_PORT_BLOCK_ALLOC: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099
'''
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=5), False)
        test.response.return_value = '''Oct 30 21:46:04  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:46:04 [FWNAT]:ASP_NAT_PORT_BLOCK_ALLOC: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099
Oct 30 21:48:35  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:48:34 [FWNAT]:NAT_PORT_BLOCK_ACTIVE: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099'''

        self.srv.dh = Values()
        self.srv.dh.cli = MagicMock()
        self.srv.dh.cli.return_value = test
        cmp_patch.return_value = True
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=50, active=1), True)
        #incorrect block size, diff port, ip
        cmp_patch.return_value = False
        test.response.return_value = '''Oct 30 21:46:04  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:46:04 [FWNAT]:ASP_NAT_PORT_BLOCK_ALLOC: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099
Oct 30 21:48:35  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:48:34 [FWNAT]:NAT_PORT_BLOCK_ACTIVE: 3002:0:0:0:0:0:0:2 -> 33.33.0.3:-1-1090'''
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=5, active=1), False)
        # #detnat return true
        cmp_patch.return_value = False
        test.response.return_value = ''''''

        self.srv.dh.cli.return_value = test
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=5, detnat=1, active=1), True)
        
        cmp_patch.return_value = False
        test.response.return_value = '''Oct 30 21:48:35  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:48:34 [FWNAT]:NAT_PORT_BLOCK_ACTIVE: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099'''

        self.srv.dh.cli.return_value = test
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=5, detnat=1, active=1), False)
        # #detnat else condition return false

        self.srv.dh.cli.return_value = test
        test.response.return_value = '''Oct 30 21:46:04  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:46:04 [FWNAT]:ASP_NAT_PORT_BLOCK_ALLOC: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099
'''
        self.assertEqual(self.srv.verify_syslog_pba(release_time=30, blk_size=5, active=1), False)
        #detnat and is_alloc not return false
        test.response.return_value = '''Oct 30 21:46:04  graphite (FPC Slot 2, PIC Slot 0) 2011-10-31 04:46:04 [FWNAT]:: 3002:0:0:0:0:0:0:1 -> 33.33.0.3:1050-1099
'''
        self.srv.dh.cli.return_value = test
        self.assertEqual(self.srv.verify_syslog_pba(), False)






if __name__ == '__main__':
    unittest.main()
