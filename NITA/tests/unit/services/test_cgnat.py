from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from optparse import Values
from collections import defaultdict
import builtins

from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.hldcl.unix.unix import UnixHost

from jnpr.toby.services.cgnat import cgnat


builtins.t = {}

class Test_Cgnat(unittest.TestCase):

    def setUp(self):
        self.response = {}
        self.xml = xml_tool()
        self.response["NAT_POOL_DETAIL"] = '''
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/16.1R3/junos">
           <service-nat-pool-information>
               <sfw-per-service-set-nat-pool junos:style="detail">
                   <interface-name>mams-2/0/0 (ams4)</interface-name>
                   <service-set-name>MX1_SFW4_CGN4_AMS4</service-set-name>
                   <service-nat-pool>
                       <pool-name>MX1_CGN4_AMS4-CONE-p1</pool-name>
                       <translation-type>NAPT-44</translation-type>
                       <pool-address-range-list>
                           <pool-address-range>192.168.83.1-192.168.83.3</pool-address-range>
                       </pool-address-range-list>
                       <pool-configured-port-range>10001-10002</pool-configured-port-range>
                       <pool-port-range>10001-10002</pool-port-range>
                       <pool-ports-in-use>0</pool-ports-in-use>
                       <pool-out-of-port-errors>144</pool-out-of-port-errors>
                       <pool-parity-port-errors>0</pool-parity-port-errors>
                       <pool-preserve-range-errors>0</pool-preserve-range-errors>
                       <pool-max-ports-in-use>6</pool-max-ports-in-use>
                       <pool-app-port-errors>90</pool-app-port-errors>
                       <pool-app-exceed-port-limit-errors>0</pool-app-exceed-port-limit-errors>
                       <pool-mem-alloc-errors>0</pool-mem-alloc-errors>
                       <eif-inbound-session-count>0</eif-inbound-session-count>
                       <eif-inbound-session-limit-exceed-drop>0</eif-inbound-session-limit-exceed-drop>
                   </service-nat-pool>
               </sfw-per-service-set-nat-pool>
           </service-nat-pool-information>
           <cli>
               <banner></banner>
           </cli>
        </rpc-reply>
        '''

        self.cgn = cgnat(dh=None)
        self.cgn.log = MagicMock()
        self.cgn.config = MagicMock()
        self.cgn.config.return_value = True
        self.cgn.dh = MagicMock()
        self.cgn.dh.cli = MagicMock()
        self.cgn.dh.cli = MagicMock()
        self.cgn.fn_checkin = MagicMock()
        self.cgn.fn_checkout = MagicMock()
        self.cgn.fn_checkout.return_value = True
        self.cgn._get_intf_ss = MagicMock()
        self.cgn._get_tg_port_and_config_mapping = MagicMock()

        dd = {}
        dd = lambda:defaultdict(dd)
        self.cgn.dd = MagicMock()
        self.cgn.dd.return_value = dd()

        self.cgn.r_if = {'ss1'}
        self.cgn.resource = 'esst480p'
        #self.cgn.topo = {'intf' : {'ms-5/0/0' : { 'path' : 'r0r1'}}, 'path_res' : { 'esst480p' : { 'r0r1' : ['intf1']}}}
        self.cgn.topo = {'intf' : {'1/1' : { 'path' : 'r0r1'}}, 'path_res' : { 'esst480p' : { 'r0r1' : ['intf1']}}}
        builtins.t = {'resources' : {'esst480p' : { 'interfaces' : { 'intf1' : {'pic' : 'ms-5/0/0' }}}}}
        self.cgn.intf_ss = {'ms-5/0/0' : 'ss1'}
        self.cgn.sset = {'ss1': {'spic': 'ms-5/0/0', 'nat_rules': ['nr1']}}
        #self.cgn.nat_rule = {'nr1': {'src_pool': 'np1'}}
        #self.cgn.nat_rule = {'nr1': {'src_pool': 'np1', 'trans_type': 'dnat','trans_eim': 1,'trans_eif': 1}}
        self.cgn.nat_rule = {'nr1': {'src_pool': 'np1', 'trans_type': 'napt','trans_eim': 1,'trans_eif': 1}}
        self.cgn.nat_pool = {'np1': {'trans_type':'napt', 'addr': '112.1.1.0/24','nat_port': '1024-3456'}, 'np2': {'trans_type':'dynamic', 'addr': '120.1.1.0/24'}}
        #self.cgn.tg_sess = {'ms-5/0/0': {'sess_list': [{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'}]}}
        self.cgn.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'}]}, 'total': 10}
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        #self.cgn.tg_sess_cnt_cgn = {'1/1':10, 'total': 10}
        self.cgn.pool_map = {'np1': {'tot_sess': 10}, 'np2': {'tot_sess': 10}}

    def _validate_eim(self, is_run=False, debug=False):

        self.eim_output = self.cgn.get_nat_eim_mappings(private_ip='11.1.1.2', public_ip='112.1.1.2')
        if debug:
            import pprint
            pp = pprint.PrettyPrinter()
            pp.pprint(self.eim_output)

        if is_run:
            self.assertNotEqual(self.eim_output, None)

    def _validate_app(self, is_run=False, debug=False):

        self.app_output = self.cgn.get_nat_app_mappings(private_ip='11.1.1.2', public_ip='112.1.1.2')
        if debug:
            import pprint
            pp = pprint.PrettyPrinter()
            pp.pprint(self.app_output)

        if is_run:
            self.assertNotEqual(self.app_output, None)

    #############################################
    # set_nat_rule
    #############################################
    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_cgnat_set_nat_rule_src_dst(self, patch1):
      
      patch1.return_value = None
      self.assertEqual(self.cgn.set_nat_rule(count=1, action='set', dir='input', term=1, term_idx_reset=1, num_terms=1, src_addr='30.0.0.0', src_pfx='30.0.0.0', dst_addr='40.0.0.0', dst_pfx='40.0.0.0', clat_pfx='50.0.0.0',src_low='30.0.0.2', src_high='30.0.0.10', dst_low='40.0.0.2', dst_high='40.0.0.10', dst_port_low=1025, dst_port_high=1125, then_syslog=1, no_trans=0), True)

    #############################################
    # set_port_forward_rule
    #############################################
    def test_cgnat_set_port_forward_rule(self):
      self.assertEqual(self.cgn.set_port_forward_rule(action='set', name='pfr1', dst_port='2345', trans_port='23'), True)

    def test_cgnat_set_port_forward_rule_exception_no_dst_port(self):
       with self.assertRaises(Exception) as context:
          self.cgn.set_port_forward_rule(action='set', name='pfr1', trans_port='23')
          self.assertTrue("Missing mandatory arguments" in str(context.exception))

    def test_cgnat_set_port_forward_rule_exception_no_trans_port(self):
      with self.assertRaises(Exception) as context:
          self.cgn.set_port_forward_rule(action='set', name='pfr1', dst_port='2345')
          self.assertTrue("Missing mandatory arguments" in str(context.exception))

    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_cgnat_set_nat_rule_ruleset(self, patch1):

      patch1.return_value = None
      self.assertEqual(self.cgn.set_nat_rule(count=1, action='set', dir='input', term=1, num_terms=1, src_addr='30.0.0.0', dst_addr='40.0.0.0', rs_name='rs1'), True)

    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_cgnat_set_nat_rule_src_step_dst_step(self, patch1):
      
      patch1.return_value = None

      self.assertEqual(self.cgn.set_nat_rule(count=1, action='set', dir='input', term=1, term_idx_reset=1, num_terms=10, src_addr='30.0.0.0', src_addr_nw_step_cnt=1, src_addr_nw_step=1, src_addr_step=1, dst_addr='40.0.0.0'), True)

    #############################################
    # set_nat_pool
    #############################################
    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_set_nat_pool(self, patch1):

        patch1.return_value = None
        self.assertEqual(self.cgn.set_nat_pool(name='pool1', addr='30.0.0.0/24', addr_low='30.0.0.1', addr_high='30.0.0.100', port_low='1000', port_high='2000'), True)

    @patch('jnpr.toby.utils.iputils.incr_ip_subnet')
    def test_set_nat_pool_port_range_case(self, patch1):

        patch1.return_value = None
        self.assertEqual(self.cgn.set_nat_pool(name='pool1', addr='30.0.0.0/24', addr_low='30.0.0.1', addr_high='30.0.0.100', port_low='1000', port_high='2000', port_range_random=1, snmp_trap_low='1', snmp_trap_high='10'), True)


    def test_set_nat_pool_negative(self):

        self.assertEqual(self.cgn.set_nat_pool(name='nat_pool', action=None), True)

    #############################################
    # ::verify
    #############################################
    @patch('jnpr.toby.services.services.services.verify')
    def test_verify_wrapper(self, patch):
        patch.return_value = None
        self.cgn = cgnat(dh=None)
        self.cgn.log = MagicMock()
        self.cgn.verify_nat_pool_detail = MagicMock()
        self.cgn._get_tg_port_and_config_mapping = MagicMock()
        self.cgn.verify_sessions_extensive = MagicMock()

        self.assertEqual(self.cgn.verify(), True)

    #############################################
    # get_nat_pool_detail
    #############################################
    @patch('jnpr.toby.services.cgnat.utils.update_data_from_output')
    def test_get_nat_pool_detail(self, patch):

        patch.return_value = None
        #cgnatObj = CGNAT(dh=None)
        #cgnatObj.log= MagicMock()
        self.cgn.get_xml_output = MagicMock()
        xml_tree = self.xml.xml_string_to_dict(xml_str=self.response["NAT_POOL_DETAIL"])
        xml_tree = xml_tree['rpc-reply']
        xpath = 'service-nat-pool-information/sfw-per-service-set-nat-pool'
        for path in  xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        options = {'name':'MX1_CGN4_AMS4-CONE-p1'}
        self.cgn.data = {}
        self.assertEqual(self.cgn.get_nat_pool_detail(**options), True)

    @patch('jnpr.toby.services.cgnat.iputils.get_network_ip_range')
    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_verify_nat_pool_detail(self, test_cmp_dicts, pathch2):
        pathch2.return_value = '1-1'
        self.cgn.get_nat_pool_detail= MagicMock()
        self.cgn._get_tg_port_and_config_mapping= MagicMock()
        self.cgn._get_ss_from_pool= MagicMock()
        self.cgn.result= MagicMock()
        self.cgn.tg_sess_cnt = {'total':2}
        self.cgn.data = {'nat_pool':{'np1':{'trans_type':'napt'}, 'np2':{'trans_type':'dynamic'}, 'np3':{'trans_type':'twiceanapt'}, 'np4':{'trans_type':'deterministicanapt'}}}
        options = {'out_of_port_errs': 0, 'tg_sess':""}
        test_cmp_dicts.return_value = True
        self.cgn.nat_pool = {'np1':"", "np2":"", "np3" :"", 'np4' : {'addr':""}, 'np4_addr' : "addr"}
        self.cgn.pool_map = {'np1': {"total_sess": 10, 'spic':'ms-5/0/0', 'sset':''}, 'np2': {"total_sess": 10, 'spic':'ms-5/0/0', 'sset':''}, 'np3': {"total_sess": 10, 'spic':'ms-5/0/0', 'sset':''}, 'np4': {"total_sess": 10, 'spic':'ms-5/0/0', 'sset':''}}
        self.assertEqual(self.cgn.verify_nat_pool_detail(name=None, **options), True)
        test_cmp_dicts.return_value = False
        self.assertEqual(self.cgn.verify_nat_pool_detail(name=None, **options), True)

    #############################################
    # get_eim_mappings
    #############################################
    @patch('jnpr.toby.utils.iputils.normalize_ipv6')
    @patch('jnpr.toby.utils.iputils.is_ip_ipv6')
    def test_cgnat_get_eim_mappings_pcp_ip_multi_sess(self,patch2,patch1):
        patch1.return_value = '2001:0000:0000:0000:0000:0000:0000:000c'
        patch2.return_value = True
        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
      Interface: sp-2/0/0, Service set: sset_1

NAT pool: np1
PCP Client       : 2001::c                 PCP lifetime : 119
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c

      Interface: sp-2/0/0, Service set: sset_2
NAT pool: np2
PCP Client       : 2001::c                 PCP lifetime : 119
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c

NAT pool: np3
PCP Client       : 2001::c                 PCP lifetime : 119
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c
'''


        self.cgn.dh.cli.return_value = test
        self._validate_eim()
    
    @patch('jnpr.toby.utils.iputils.normalize_ipv6')
    @patch('jnpr.toby.utils.iputils.is_ip_ipv6')
    def test_cgnat_get_eim_mappings_pcp_ip_multi_sess_mixed(self,patch2,patch1):
        patch1.return_value = '2001:0000:0000:0000:0000:0000:0000:000c'
        patch2.return_value = True
        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
      Interface: sp-2/0/0, Service set: sset_1

NAT pool: np1
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active

NAT pool: np2
PCP Client       : 2001::c                 PCP lifetime : 119
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c

NAT pool: np3
PCP Client       : 2001::c                 PCP lifetime : 119
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c
'''


        self.cgn.dh.cli.return_value = test
        self._validate_eim()
    
    @patch('jnpr.toby.utils.iputils.normalize_ipv6')
    @patch('jnpr.toby.utils.iputils.is_ip_ipv6')
    def test_cgnat_get_eim_mappings_b4_ip_multi_sess(self,patch2,patch1):
        patch1.return_value = '2001:0000:0000:0000:0000:0000:0000:000c'
        patch2.return_value = True
        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
      Interface: sp-2/0/0, Service set: sset_1

NAT pool: np1
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c

NAT pool: np2
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c

NAT pool: np3
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c
'''


        self.cgn.dh.cli.return_value = test
        self._validate_eim()
    
    @patch('jnpr.toby.utils.iputils.normalize_ipv6')
    @patch('jnpr.toby.utils.iputils.is_ip_ipv6')
    def test_cgnat_get_eim_mappings_multi_sess(self,patch2,patch1):
        patch1.return_value = '2001:0000:0000:0000:0000:0000:0000:000c'
        patch2.return_value = True

        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
      Interface: sp-2/0/0, Service set: sset_1

NAT pool: np1
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active

NAT pool: np2
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active

NAT pool: np3
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
'''

        self.cgn.dh.cli.return_value = test
        self._validate_eim()
    
    @patch('jnpr.toby.utils.iputils.normalize_ipv6')
    def test_cgnat_get_eim_mappings(self,patch1):
        patch1.return_value = True
        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
      Interface: ms-3/0/0, Service set: ss1

NAT pool: np1
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1        :63082
Session Count    :     0
Mapping State    : Timeout (3509s)
      
      Interface: ms-3/0/0, Service set: ss1

NAT pool: np1
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1        :63082
Session Count    :     0
Mapping State    : Timeout (3509s)
'''
        self.cgn.dh.cli.return_value = test
        self._validate_eim()

    @patch('jnpr.toby.utils.iputils.normalize_ipv6')
    def test_cgnat_get_eim_mappings_no_pcp_ip(self,patch1):
        patch1.return_value = True
        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
      Interface: sp-2/0/0, Service set: sset_1

NAT pool: np1
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c

      Interface: sp-2/0/0, Service set: sset_2

NAT pool: np1
Mapping          : 11.1.1.2        : 5060  --> 60.1.1.1     : 63082
Session Count    :     2
Mapping State    : Active
B4 Address       : 2001::c
'''
        self.cgn.dh.cli.return_value = test
        self._validate_eim()

    def test_cgnat_get_eim_mappings_no_output(self):
        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
        '''
        self.cgn.dh.cli.return_value = test
        self.cgn.get_nat_eim_mappings()

    """
    def test_cgnat_verify_eim_mappings_no_output(self):

      self.cgn.get_eim_mappings = MagicMock()
      self.cgn.get_eim_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'5060': {'nat_ip': '60.1.1.1', 'nat_port': '2210', 'sess_cnt': '0', 'state': 'timeout', 'state_to': '3509'}}}}}}

      self.cgn.get_eim_mappings.side_effect = Exception("No valid output found")
      with self.assertRaises(Exception) as context:
          self.cgn.verify_eim_mappings()
          self.assertTrue("Looks like there is no valid output" in str(context.exception))
    """

    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    def test_cgnat_verify_eim_mappings(self, patch1, patch2):
      patch1.return_value = True
      patch2.return_value = True

      self.cgn.get_eim_mappings = MagicMock()
      self.cgn.get_eim_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'5060': {'nat_ip': '60.1.1.1', 'nat_port': '2210', 'sess_cnt': '0', 'state': 'timeout', 'state_to': '3509'}}}}}}
      self.cgn._get_src_ip_port_flow_from_data = MagicMock()
      self.cgn._get_src_ip_port_flow_from_data.return_value = {'src_ip': '11.1.1.2','src_port': '5060'}
      self.assertNotEqual(self.cgn.verify_nat_eim_mappings(limit=2,limit_perc=2), False)
      self.cgn._get_src_ip_port_flow_from_data.return_value = {'src_ip': '11.1.1.2','src_port': '5060', 'nat_ip' : None}
      self.assertNotEqual(self.cgn.verify_nat_eim_mappings(limit=2,limit_perc=2), False)
      self.cgn._get_src_ip_port_flow_from_data.return_value = None
      self.assertNotEqual(self.cgn.verify_nat_eim_mappings(limit=2,limit_perc=2), False)
   
    # def test_cgnat_verify_eim_mappings_flow_none_check(self):

    #   self.cgn.get_eim_mappings = MagicMock()
    #   self.cgn.get_eim_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'5060': None}}}}}
    
    #   self.assertEqual(self.cgn.verify_nat_eim_mappings(limit=2,limit_perc=2), True)
    
    # def test_cgnat_verify_eim_mappings_flow_nat_ip_none_check(self):

    #   self.cgn.get_eim_mappings = MagicMock()
    #   self.cgn._is_nat_ip_in_pool = MagicMock()
    #   self.cgn._is_nat_port_in_pool = MagicMock()
    #   self.cgn.get_eim_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'5060': { 'nat_ip': None }}}}}}
    
    #   self.assertEqual(self.cgn.verify_nat_eim_mappings(), True)
    
    # """
    # def test_cgnat_verify_eim_mappings_none_check_no_limit(self):

    #   self.cgn.get_eim_mappings = MagicMock()
    #   self.cgn.get_eim_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'5060': None}}}}}
    
    #   self.assertNotEqual(self.cgn.verify_eim_mappings(), True)
    # """
    
    # @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    # def test_cgnat_verify_eim_mappings_incorrect_NAT_ip(self,patch1):
    #   patch1.return_value = True  

    #   self.cgn.get_eim_mappings = MagicMock()
    #   self.cgn.get_eim_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'5060': {'nat_ip': '70.1.1.1', 'nat_port': '63082', 'sess_cnt': '0', 'state': 'timeout', 'state_to': '3509'}}}}}}

    #   self.assertNotEqual(self.cgn.verify_nat_eim_mappings(limit=2,limit_perc=2), True)

    # @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    # @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    # def test_cgnat_verify_eim_mappings_incorrect_NAT_port(self, patch1, patch2):
    #   patch1.return_value = True
    #   patch2.return_value = True

    #   self.cgn.get_eim_mappings = MagicMock()
    #   self.cgn.get_eim_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'5060': {'nat_ip': '60.1.1.1', 'nat_port': '63082', 'sess_cnt': '0', 'state': 'timeout', 'state_to': '3509'}}}}}}

    #   self.assertNotEqual(self.cgn.verify_nat_eim_mappings(limit=2,limit_perc=2), True)

    #############################################
    # get_app_mappings
    #############################################

#     def test_cgnat_get_app_mappings_no_output(self):
#       self.cgn.dh.cli.return_value = '''
# '''

#       self.cgn.get_nat_app_mappings()

#     def test_cgnat_get_app_mappings_no_output(self):
#       self.cgn.dh.cli.return_value = '''
# '''

#       with self.assertRaises(Exception) as context:
#           self.cgn.get_nat_app_mappings()
#       self.assertTrue("No valid output found" in str(context.exception))

    def test_get_app_mappings_multisess(self):

        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
                               Interface: ms-0/2/0, Service set: ss1
                               NAT pool: nat_pool1
                               Mapping          : 11.1.1.2         --> 112.1.1.3
                               Ports In Use     :    10
                               Session Count    :     0
                               Mapping State    : Active   (123s)

                               Mapping          : 11.1.1.3         --> 112.1.1.4
                               Ports In Use     :    10
                               Session Count    :     0
                               Mapping State    : Active
                               
                               NAT pool: nat_pool2
                               Mapping          : 11.1.1.4         --> 122.1.1.4
                               Ports In Use     :    10
                               Session Count    :     0
                               Mapping State    : Active
                               
                               Interface: ms-0/2/0, Service set: ss2
                               NAT pool: nat_pool2
                               Mapping          : 11.1.1.2         --> 122.1.1.3
                               Ports In Use     :    10
                               Session Count    :     0
                               Mapping State    : Active
        '''
        self.cgn.dh.cli.return_value = test
        self._validate_app()

    @patch('jnpr.toby.utils.iputils.normalize_ipv6')
    @patch('jnpr.toby.utils.iputils.is_ip_ipv6')
    def test_get_app_mappings_b4_multisess(self, test_patch2, test_patch3):

        test_patch2.return_value = False
        test_patch3.return_value = '2001:0000:0000:0000:0000:0000:0000:0001'
        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
                               Interface: ms-0/2/0, Service set: ss1
                               NAT pool: nat_pool1
                               Mapping          : 11.1.1.2         --> 112.1.1.3
                               Ports In Use     :    10
                               Session Count    :     0
                               Mapping State    : Active
                               B4 Address       : 2001::1

                               Mapping          : 11.1.1.3         --> 112.1.1.4
                               Ports In Use     :    10
                               Session Count    :     0
                               Mapping State    : Active
                               B4 Address       : 2001::1
                               
                               NAT pool: nat_pool2
                               Mapping          : 11.1.1.4         --> 122.1.1.5
                               Ports In Use     :    10
                               Session Count    :     0
                               Mapping State    : Active
                               B4 Address       : 2001::1
                               
                               Interface: ms-0/2/0, Service set: ss2
                               NAT pool: nat_pool2
                               Mapping          : 11.1.1.2         --> 122.1.1.3
                               Ports In Use     :    10
                               Session Count    :     0
                               Mapping State    : Active
                               B4 Address       : 2001::1
        '''
        self.cgn.dh.cli.return_value = test
        self._validate_app()

    """
    def test_cgnat_verify_app_mappings_no_output(self):

      self.cgn.get_app_mappings = MagicMock()

      self.cgn.get_app_mappings.side_effect = Exception("No valid output found")
      with self.assertRaises(Exception) as context:
          self.cgn.verify_app_mappings()
          self.assertTrue("Looks like there is no valid output" in str(context.exception))
    """

    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    def test_cgnat_verify_app_mappings(self, patch1, patch2):
      patch1.return_value = True
      patch2.return_value = True

      self.cgn.get_app_mappings = MagicMock()
      self.cgn.get_app_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'nat_ip': '112.1.1.3', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}, '11.1.1.3': {'nat_ip': '112.1.1.4', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active'}}}}}
      self.cgn._get_src_ip_flow_from_data = MagicMock()
      self.cgn._get_src_ip_flow_from_data.return_value = {'nat_ip': '112.1.1.3', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
      self.assertNotEqual(self.cgn.verify_nat_app_mappings(limit=2, limit_perc=2),None)
      self.cgn._get_src_ip_flow_from_data.return_value = None
      self.assertNotEqual(self.cgn.verify_nat_app_mappings(limit=2, limit_perc=2),None)
   
    # @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    # @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    # def test_cgnat_verify_app_mappings_no_limit(self, patch1, patch2):
    #   patch1.return_value = True
    #   patch2.return_value = True

    #   self.cgn.get_app_mappings = MagicMock()
    #   self.cgn.get_app_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'nat_ip': '112.1.1.3', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}, '11.1.1.3': {'nat_ip': '112.1.1.4', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active'}}}}}
    
    #   self.assertNotEqual(self.cgn.verify_nat_app_mappings(),None)
    
    # @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    # @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    # def test_cgnat_verify_app_mappings_no_limit_ip_notin_subnet(self, patch1, patch2):
    #   patch1.return_value = False
    #   patch2.return_value = True

    #   self.cgn.get_app_mappings = MagicMock()
    #   self.cgn.get_app_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {'nat_ip': '112.1.1.3', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}, '11.1.1.3': {'nat_ip': '112.1.1.4', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active'}}}}}
    
    #   self.assertNotEqual(self.cgn.verify_nat_app_mappings(),None)
    
    # def test_cgnat_verify_app_mappings_none_check(self):

    #   self.cgn.get_app_mappings = MagicMock()
    #   self.cgn.get_app_mappings.return_value = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': None}}}}
    
    #   self.assertNotEqual(self.cgn.verify_nat_app_mappings(limit=2,limit_perc=2),None)
    
#     #############################################
#     # get_mappings_detail
#     #############################################
#     def test_cgnat_get_mappings_detail_no_output(self):
#       self.cgn.dh.cli.return_value = '''
# '''
#      self.cgn.get_nat_mappings_detail()

    @patch('jnpr.toby.services.cgnat.utils.get_regex_ip')
    @patch('jnpr.toby.utils.iputils.is_ip_ipv6')
    def test_cgnat_get_mappings_detail_true(self, patch_new, patch_old):

        test = Values()
        test.response = MagicMock()
        test.response.return_value =  """
                                Interface: ms-1/0/0, Service set: ss100

                                   NAT pool: p100

                                   Mapping          : 11.250.28.72   :  100  --> 39.7.56.46   :  100
                                   Session Count    :     0
                                   Mapping State    : Timeout (25s)

                                   Mapping          : 11.252.189.215  --> 39.7.56.68
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (256s)

                                   Mapping          : 11.253.149.48   --> 39.7.56.39
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (80s)

                                   Mapping          : 11.249.81.44    --> 39.7.56.48
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (298s)

                                   Mapping          : 11.249.27.217   --> 39.7.56.64
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (24s)

                                   Mapping          : 11.250.86.189   --> 39.7.56.100
                                   Ports In Use     :  1008
                                   Session Count    :  1008
                                   Mapping State    : Active

                                   Mapping          : 11.251.41.56    --> 39.7.56.3
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (92s)

                                   Mapping          : 11.248.90.14    --> 39.7.56.62
                                   Ports In Use     :  1008
                                   Session Count    :  1008
                                   Mapping State    : Active

                                   Mapping          : 11.249.27.64    --> 39.7.56.41
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (20s)"""

        self.cgn.dh.cli.return_value = test
        patch_old.return_value = '(?:(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))'
        patch_new.return_value = False
        self.assertTrue(self.cgn.get_nat_mappings_detail(pool_name="p100"), dict)


    @patch('jnpr.toby.services.cgnat.utils.get_regex_ip')
    @patch('jnpr.toby.utils.iputils.is_ip_ipv6')
    def test_cgnat_get_mappings_detail_false(self, patch_new, patch_old):

        test = Values()
        test.response = MagicMock()
        test.response.return_value =  """
       Interface: ms-1/0/0, Service set: ss100

                                   NAT pool: p100

                                   Mapping          : 11.250.28.72   :  100  --> 39.7.56.46   :  100
                                   Session Count    :     0
                                   Mapping State    : Timeout 

                                   Mapping          : 11.252.189.215  --> 39.7.56.68
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (256s)

                                   Mapping          : 11.253.149.48   --> 39.7.56.39
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (80s)

                                   Mapping          : 11.249.81.44    --> 39.7.56.48
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (298s)

                                   Mapping          : 11.249.27.217   --> 39.7.56.64
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (24s)

                                   Mapping          : 11.250.86.189   --> 39.7.56.100
                                   Session Count    :  1008
                                   Mapping State    : Active

                                   Mapping          : 11.251.41.56    --> 39.7.56.3
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (92s)

                                   Mapping          : 11.248.90.14    --> 39.7.56.62
                                   Ports In Use     :  1008
                                   Session Count    :  1008
                                   Mapping State    : Active

                                   Mapping          : 11.249.27.64    --> 39.7.56.41
                                   Ports In Use     :     0
                                   Session Count    :     0
                                   Mapping State    : Timeout (20s)"""

        self.cgn.dh.cli.return_value = test
        patch_old.return_value = '(?:(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))'
        patch_new.return_value = False
        self.assertTrue(self.cgn.get_nat_mappings_detail(pool_name="p100"), dict)

    """
    def test_cgnat_verify_mappings_detail_no_output(self):

      self.cgn.get_mappings_detail = MagicMock()

      self.cgn.get_mappings_detail.side_effect = Exception("No valid output found")
      with self.assertRaises(Exception) as context:
          self.cgn.verify_mappings_detail()
          self.assertTrue("Looks like there is no valid output" in str(context.exception))
    """

    @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_cgnat_verify_mappings_detail_true(self, patch1, patch2):

        self.cgn.get_mappings_detail = MagicMock()
        self.cgn.get_mappings_detail.return_value = {'ms-5/0/0':  {'ss1': {'np1': {'11.1.1.2':  {'5060':  {'eim_nat_ip': '39.7.56.46', 'eim_nat_port': '2000', 'eim_sess_cnt': '0','eim_state': 'timeout '}, 'app_ports_in_use': '0', 'app_sess_cnt': '0', 'app_state': 'timeout', 'app_state_to': '20'}}}}}
        patch1.return_value = True
        patch2.return_value = True
        self.cgn.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'}]}, 'total': 10}
        self.cgn._get_tg_port_and_config_mapping  = MagicMock()
        self.cgn._get_src_ip_port_flow_from_data = MagicMock()
        self.cgn._get_src_ip_port_flow_from_data.return_value = {'eim_nat_ip': '39.7.56.46', 'eim_nat_port': '2000', 'eim_sess_cnt': '0','eim_state': 'timeout '}
        self.assertEqual(self.cgn.verify_nat_mappings_detail(limit=1), True)

        self.cgn._get_src_ip_port_flow_from_data.return_value = None
        self.assertEqual(self.cgn.verify_nat_mappings_detail(limit=1), True)

    # @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    # def test_cgnat_verify_mappings_detail_src_flow_none(self, patch1):

    #     patch1.return_value = True
    #     self.cgn.get_mappings_detail = MagicMock()
    #     self.cgn._get_tg_port_and_config_mapping  = MagicMock()
    #     self.cgn.get_mappings_detail.return_value= {'ms-5/0/0':{'ss1':{'np1':{'11.1.1.2':{'5060':None}}}}}
       
    #     self.assertEqual(self.cgn.verify_nat_mappings_detail(), True)

    # @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    # @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    # def test_cgnat_verify_mappings_detail_wrong_nat_port(self, patch1, patch2):

    #     self.cgn.get_mappings_detail = MagicMock()
    #     self.cgn.get_mappings_detail.return_value= {'ms-5/0/0':  {'ss1': {'np1': {'11.1.1.2':  {'5060':  {'eim_nat_ip': '39.7.56.46', 'eim_nat_port': '80', 'eim_sess_cnt': '0','eim_state': 'timeout '}, 'app_ports_in_use': '0', 'app_sess_cnt': '0', 'app_state': 'timeout', 'app_state_to': '20'}}}}}
    #     patch1.return_value = True
    #     patch2.return_value = True        
    #     self.cgn._get_tg_port_and_config_mapping  = MagicMock()
    #     self.assertEqual(self.cgn.verify_nat_mappings_detail(limit=1), False)

    # @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    # @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    # def test_cgnat_verify_mappings_detail_ip_not_in_range(self, patch1, patch2):

    #     self.cgn.get_mappings_detail = MagicMock()
    #     self.cgn.get_mappings_detail.return_value= {'ms-5/0/0':  {'ss1': {'np1': {'11.1.1.2':  {'5060':  {'eim_nat_ip': '39.7.56.46', 'eim_nat_port': '80', 'eim_sess_cnt': '0','eim_state': 'timeout '}, 'app_ports_in_use': '0', 'app_sess_cnt': '0', 'app_state': 'timeout', 'app_state_to': '20'}}}}}
    #     patch1.return_value = True
    #     patch2.return_value = False
    #     self.cgn._get_tg_port_and_config_mapping  = MagicMock()
    #     self.assertEqual(self.cgn.verify_nat_mappings_detail(limit=1), False)

    #############################################
    # get_nat_mappings_summary
    #############################################
    def test_cgnat_get_nat_mappings_summary(self):
       
        test = Values()
        test.response = MagicMock()
        test.response.return_value = '''Service Interface:                                          ms-3/1/0
            Total number of address mappings:                           1803
            Total number of endpoint independent port mappings:         0
            Total number of endpoint independent filters:               0
            Service Interface:   abc
            '''  
        self.cgn.dh.cli.return_value = test
        #pp = pprint.PrettyPrinter()
        output = self.cgn.get_nat_mappings_summary()
        #pp.pprint(output)
        self.assertNotEqual(output, None)

    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_cgnat_verify_nat_mappings_summary(self, patch):
        patch.return_value = True

        self.cgn.get_mappings_summary = MagicMock()
        self.cgn.get_mappings_summary.return_value = {'ms-5/0/0': {'addr_map': 1803, 'eif_map': 0, 'eim_map': 0}}
        self.assertEqual(self.cgn.verify_nat_mappings_summary(), True)
        
    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_cgnat_verify_nat_mappings_summary_dnat(self, patch1):
        self.cgn.nat_rule = {'nr1': {'trans_type': 'dnat', 'trans_eim': 1, 'trans_eif': 1}}
        patch1.return_value = True

        self.cgn.get_mappings_summary = MagicMock()
        self.cgn.get_mappings_summary.return_value = {'ms-5/0/0': {'addr_map': 1803, 'eif_map': 0, 'eim_map': 0}}

        self.assertEqual(self.cgn.verify_nat_mappings_summary(), True)

    #############################################
    # get_nat_statistics
    #############################################
    #@patch('utils.shift_args_val')
    #@patch('utils.update_opts_from_args')
    #def test_get_nat_statistics_no_sp(self, patch1, patch2):
    def test_get_nat_statistics_no_sp(self):
        #patch1.return_value = None
        self.cgn.get_xml_output = MagicMock()
        self.cgn.get_xml_output.return_value = {'interface-name': 'ms-5/0/0', 'query-unsupported-msg': None, 'nat-total-pkts-translated': 1, 'nat-map-allocation-successes': 2}
        #patch2.return_value = None
        #self.assertNotEqual(self.cgn.get_nat_statistics('ms-5/0/0'), None)
        #self.assertNotEqual(self.cgn.get_nat_statistics(), None)
        with self.assertRaises(Exception) as context:
          self.cgn.get_nat_statistics()
          self.assertTrue("Missing mandatory argument, sp" in str(context.exception))

    # @patch('jnpr.toby.services.cgnat.utils.shift_args_val')
    @patch('jnpr.toby.services.cgnat.utils.update_opts_from_args')
    def test_get_nat_statistics(self, patch1):
        patch1.return_value = None
        self.cgn.get_xml_output = MagicMock()
        self.cgn.get_xml_output.return_value = {'interface-name': 'ms-5/0/0', 'query-unsupported-msg': None, 'nat-total-pkts-translated': 1, 'nat-map-allocation-successes': 2}
        # patch2.return_value = None
        self.assertNotEqual(self.cgn.get_nat_statistics('ms-5/0/0'), None)

    # @patch('jnpr.toby.services.cgnat.utils.shift_args_val')
    @patch('jnpr.toby.services.cgnat.utils.update_opts_from_args')
    def test_get_nat_statistics2(self, patch1):
        patch1.return_value = None
        self.cgn.get_xml_output = MagicMock()
        self.cgn.get_xml_output.return_value = {'query-unsupported-msg':'1'}
        # patch2.return_value = 'abc'
        #self.assertEqual(self.cgn.get_nat_statistics('abc'), {'m':'4','n':'5','sp':'abc'})

    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_verify_nat_statistics(self, test_patch):
        self.cgn.get_nat_statistics = MagicMock()
        self.cgn.get_nat_statistics.return_value = {'total_trans_pkts': '10', 'map_alloc_success': '10'}
        test_patch.return_value = True
        self.assertEqual(self.cgn.verify_nat_statistics(), True)

    def test_get_pool_ips(self):
        self.assertNotEqual(self.cgn.get_nat_pool_ips(), None)
        #self.assertEqual(self.cgn.get_pool_ips(), ['112.1.1.0/24', '120.1.1.0/24'])

    def test_get_sess_cnt_per_ss_fail(self):
        with self.assertRaises(Exception) as context:
          self.cgn.get_sess_cnt_per_ss()
          self.assertTrue("Missing mandatory argument, tg/tg_sess" in str(context.exception))

    def test_get_sess_cnt_per_ss_tg_not_none(self):
        tg = MagicMock()
        tg.get_sessions = MagicMock()
        tg.get_sessions.return_value = self.cgn.tg_sess
        self.assertNotEqual(self.cgn.get_sess_cnt_per_ss(tg), None)

    def test__get_ss_from_pool(self):
        self.cgn = cgnat(dh=None)
        self.cgn.log = MagicMock()
        self.cgn.fn_checkin = MagicMock()
        self.cgn.fn_checkout = MagicMock()
        self.cgn.fn_checkout.return_value = True
        self.cgn.pool_map = {}
        self.cgn.nat_pool = {"np1":""}
        self.cgn.nat_pool_rule_map = {"src_pool": {'np1':"nr1"}}
        self.cgn.ss_map = {"nat_pool": {'np1':"ss1"}, "nat_rules":{'nr1':'ss1'}}
        self.cgn.sset = {"ss1":{'intf':"eth1"}}
        self.cgn.tg_sess_cnt = {"eth1":{'ss1':"eth1"}}
        self.assertNotEqual(self.cgn._get_ss_from_pool(), None)
        self.cgn.nat_pool_rule_map = {"src_pool": {}, "dst_pool": {'np1':"nr1"}}
        self.assertNotEqual(self.cgn._get_ss_from_pool(), None)
        self.cgn.nat_pool_rule_map = {"src_pool": {}, "dst_pool": {}}
        self.assertNotEqual(self.cgn._get_ss_from_pool(), None)
    #def test_local_routines(self):
        #self.cgn._get_profile_from_pool()
    @patch('jnpr.toby.services.cgnat.services._get_tg_port_and_config_mapping')
    def test__get_tg_port_and_config_mapping(self, patch):
        self.cgn = cgnat(dh=None)
        self.cgn.log = MagicMock()
        # delattr(self.cgn, '_get_tg_port_and_config_mapping')
        self.cgn.tg_sess_cnt = 1
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.cgn.sset = {'ss1':{'nat_rules':['nr1']}}
        self.cgn.nat_rule = {'nr1':{'src_pool':"np1" , 'dst_pool':"np1"}}
        self.cgn.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'}]}, 'total': 10}
        self.cgn.nat_pool = { "np1" : {"port_low": "1024", "port_high": "1024" , "addr" : ""}}
        self.assertEqual(self.cgn._get_tg_port_and_config_mapping(tg_sess=self.cgn.tg_sess, limit=1), None)
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.cgn.sset = {'ss1':{'nat_rules':['nr1', 'nr2']}}
        self.cgn.nat_rule = {'nr1':{'src_pool':"np1" , 'dst_pool':"np1"}}
        self.cgn.nat_pool = { "np1" : {"port_auto": 1, "addr" : ""}}
        self.cgn.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'}]}, 'total': 10}
        self.assertEqual(self.cgn._get_tg_port_and_config_mapping(tg_sess=self.cgn.tg_sess, limit=1), None)
        self.cgn.tg_sess_cnt = None
        self.assertEqual(self.cgn._get_tg_port_and_config_mapping(tg_sess=self.cgn.tg_sess, limit=1), None)

    def test__get_src_ip_flow_from_data_TypeError_exception(self):
        data = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': 1}}}}
        self.assertEqual(self.cgn._get_src_ip_flow_from_data('11.1.1.2', self.cgn.tg_cfg_map['1/1'], data), 1)

    def test__get_src_ip_flow_from_data_KeyError_exception(self):
        data = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': None}}}}
        self.assertEqual(self.cgn._get_src_ip_flow_from_data('11.1.1.2', self.cgn.tg_cfg_map['1/1'], data), None)
        data = {'ms-5/0/0': {'ss1': {'np1': {}}}}
        self.assertEqual(self.cgn._get_src_ip_flow_from_data('11.1.1.2', self.cgn.tg_cfg_map['1/1'], data), None)

    def test__get_src_ip_port_flow_from_data_TypeError_exception(self):
        self.cgn = cgnat(dh=None)
        self.cgn.log = MagicMock()
        data = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {"5030": 1}}}}}
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.cgn._get_src_ip_port_flow_from_data('11.1.1.2', '5030', self.cgn.tg_cfg_map['1/1'], data), 1)

        data = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {"5030": None}}}}}
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.cgn._get_src_ip_port_flow_from_data('11.1.1.2', '5030', self.cgn.tg_cfg_map['1/1'], data), None)

        data = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {}}}}}
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.cgn._get_src_ip_port_flow_from_data('11.1.1.2', '5030', self.cgn.tg_cfg_map['1/1'], data), None)

    # def test__get_src_ip_port_flow_from_data_KeyError_exception(self):
    #     self.cgn = cgnat(dh=None)
    #     self.cgn.log = MagicMock()
    #     data = {'ms-5/0/0': {'ss1': {'np1': {'11.1.1.2': {}}}}}
    #     self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
    #     self.assertEqual(self.cgn._get_src_ip_port_flow_from_data('11.1.1.2', '5030', self.cgn.tg_cfg_map['1/1'], data), None)

    @patch('jnpr.toby.services.cgnat.iputils.is_ip_in_subnet')
    def test_is_nat_ip_in_pool(self, patch):
        patch.return_value = True
        self.cgn = cgnat(dh=None)
        self.cgn.log = MagicMock()
        data = {'nat_ip': '1025', 'eim_nat_ip': '1025',  'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.cgn._is_nat_ip_in_pool(data, self.cgn.tg_cfg_map['1/1']), True)

        # patch.return_value = False
        data = {'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.cgn.tg_cfg_map = {'1/1': { 'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.cgn._is_nat_ip_in_pool(data, self.cgn.tg_cfg_map['1/1']), False)
        
        patch.return_value = False
        data = {'nat_ip': '1025', 'eim_nat_ip': '1025', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.cgn.tg_cfg_map = {'1/1': { 'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.cgn._is_nat_ip_in_pool(data, self.cgn.tg_cfg_map['1/1']), False)

    @patch('jnpr.toby.services.cgnat.iputils.is_ip_in_subnet')
    def test_is_nat_port_in_pool(self, patch):
        self.cgn = cgnat(dh=None)
        self.cgn.log = MagicMock()
        data = {'nat_port': '1025', 'eim_nat_port': '1025', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.cgn.tg_cfg_map = {'1/1': { 'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.cgn._is_nat_port_in_pool(data, self.cgn.tg_cfg_map['1/1']), True)

    def test_is_nat_port_in_pool_no_nat_port_in_cfg_map(self):
        self.cgn = cgnat(dh=None)
        self.cgn.log = MagicMock()
        data = {'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.cgn.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        # del(self.cgn.tg_cfg_map['1/1']['nat_port'])
        self.assertEqual(self.cgn._is_nat_port_in_pool(data, self.cgn.tg_cfg_map['1/1']), False)

        data = {'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.cgn.tg_cfg_map = {'1/1': {'nat_port': '1024-3456', 'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.cgn._is_nat_port_in_pool(data, self.cgn.tg_cfg_map['1/1']), False)
        
        data = {'nat_port': '1', 'eim_nat_port': '1', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.cgn.tg_cfg_map = {'1/1': {'nat_port': '1024-3456', 'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.cgn._is_nat_port_in_pool(data, self.cgn.tg_cfg_map['1/1']), False)

    def test_get_profile_from_ss(self):
        self.assertEqual(self.cgn._get_profile_from_ss(), None)

    def test_get_tg_sess_fail(self):
        self.cgn.tg_sess = None
        with self.assertRaises(Exception) as context:
          self.cgn._get_tg_sess()
          self.assertTrue("Missing mandatory argument, tg/tg_sess" in str(context.exception))

    def test_get_tg_sess(self):
        self.assertEqual(self.cgn._get_tg_sess(tg_sess=self.cgn.tg_sess), None)

    # def test_get_intf_ss(self):

    #     self.cgn = cgnat(dh=None)
    #     self.cgn.log = MagicMock()
    #     self.cgn.intf = {'ms-5/0/0': {'inet_ss': 'ss1'}, 'ms-5/0/1': {}}
    #     #self.cgn.intf_ss = {'ms-5/0/0' : 'ss1'}
    #     self.assertNotEqual(self.cgn._get_intf_ss(), None)

    def test_verify_syslogs_no_syslogs_enabled_in_config(self):
       # print("Inside test_verify_syslogs_no_syslogs_enabled_in_config")
       # kwargs = { 'dh' : self.mocked_obj}
       # self.cgn = services(dh=kwargs)
       self.cgn.log = MagicMock()
       self.response = {}
       self.xml = xml_tool()
       options = {'limit' : "1", 'limit_perc' : "1"}
       self.cgn.nat_rule = defaultdict(lambda: defaultdict(dict))
       self.cgn.nat_rule['then_syslog'] = None
       # self.assertEqual(self.cgn._verify_syslogs(**options), False)
       self.assertEqual(self.cgn._verify_syslogs(**options), False)

    # def test_verify_syslogs_actual_value_not_defined(self):
    #    # print("Inside test_verify_syslogs_actual_value_not_defined")
    #    # kwargs = { 'dh' : self.mocked_obj}
    #    # self.cgn = services(dh=kwargs)
    #    self.cgn.dh = MagicMock()
    #    self.cgn.log = MagicMock()
    #    self.response = {}
    #    self.xml = xml_tool()
    #    self.cgn.log.return_value = None
    #    self.cgn._get_syslogs = MagicMock()
    #    self.cgn._get_syslogs.return_value = None
    #    self.cgn._get_intf_ss = MagicMock()
    #    self.cgn.tg_sess = defaultdict(lambda: defaultdict(dict))
    #    self.cgn.nat_rule = defaultdict(lambda: defaultdict(dict))
    #    self.cgn.nat_rule['then_syslog'] = 1
    #    options = {'limit' : "1", 'limit_perc' : "1", 'msg' : "JSERVICES_SESSION_OPEN", 'xtnsv' : {'src_ip' : "10.1.1.2"}, 'src_port': "1024"}

       # with self.assertRaises(Exception) as context:
       #    self.cgn._verify_syslogs(**options)
       # self.assertTrue("No syslog message(JSERVICES_SESSION_OPEN) found for 10.1.1.2 1024" in str(context.exception))
       # options = {'limit' : "1", 'limit_perc' : "1", 'msg' : "JSERVICES_SESSION_OPEN", 'xtnsv' : {'src_ip' : "10.1.1.2"}, 'src_port': None}
       # with self.assertRaises(Exception) as context:
       #    self.cgn._verify_syslogs(**options)
       # self.assertTrue("No syslog message(JSERVICES_SESSION_OPEN) found for 10.1.1.2" in str(context.exception))

    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_verify_syslogs_src_actual_value_defined(self, patch1):
       # print("Inside test_verify_syslogs_src_actual_value_defined")
       patch1.return_value = True
       #self.cgn.dh = MagicMock()
       #self.cgn.log = MagicMock()
       #self.response = {}
       #self.xml = xml_tool()
       #self.cgn.log.return_value = None
       self.cgn._get_syslogs = MagicMock()
       act_value = {'JSERVICES_SESSION_OPEN' : {'10.1.1.2' : {'1024' : {'proto' : "UDP", 'srvr_ip' : "10.1.1.2"}}}}
       self.cgn._get_syslogs.return_value = act_value
       self.cgn.nat_rule['then_syslog'] = True
       options = {'limit' : "1", 'limit_perc' : "1", 'msg' : "JSERVICES_SESSION_OPEN", 'xtnsv' : {'proto': "UDP", 'src_ip' : "10.1.1.2", 'dst_ip' : "20.1.1.2"}, 'src_port': "1024"}
       self.assertEqual(self.cgn._verify_syslogs(**options), True)
       #exeception in if
       act_value = {'JSERVICES_SESSION_OPEN' : {'10.1.1.2' : {}}}
       self.cgn._get_syslogs.return_value = act_value      
       self.cgn.nat_rule['then_syslog'] = True
       options = {'limit' : "1", 'limit_perc' : "1", 'msg' : "JSERVICES_SESSION_OPEN", 'xtnsv' : {'proto': "UDP", 'src_ip' : "10.1.1.2", 'dst_ip' : "20.1.1.2"}, 'src_port': "1024"}
       self.assertEqual(self.cgn._verify_syslogs(**options), True)
       self.cgn._get_syslogs = MagicMock()
       act_value = {'JSERVICES_SESSION_OPEN' : {'10.1.1.2' : {'1024' : {'proto' : "UDP", 'srvr_ip' : "10.1.1.2"}}}}
       self.cgn._get_syslogs.return_value = act_value
       self.cgn.nat_rule['then_syslog'] = True
       options = {'limit' : "1", 'limit_perc' : "1", 'msg' : "JSERVICES_SESSION_OPEN", 'xtnsv' : {'proto': "UDP", 'src_ip' : "10.1.1.2", 'dst_ip' : "20.1.1.2"}, 'src_port': None}
       self.assertEqual(self.cgn._verify_syslogs(**options), True)
       #exeception in if
       act_value = {'JSERVICES_SESSION_OPEN' : {}}
       self.cgn._get_syslogs.return_value = act_value      
       self.cgn.nat_rule['then_syslog'] = True
       options = {'limit' : "1", 'limit_perc' : "1", 'msg' : "JSERVICES_SESSION_OPEN", 'xtnsv' : {'proto': "UDP", 'src_ip' : "10.1.1.2", 'dst_ip' : "20.1.1.2"}, 'src_port': None}
       self.assertEqual(self.cgn._verify_syslogs(**options), True)

    @patch('jnpr.toby.services.cgnat.utils.get_regex_ip')
    @patch('jnpr.toby.services.cgnat.utils.get_regex_if')
    def test_get_syslogs(self, patch2, patch1):
       patch1.return_value = "(?:(?:(?:[A-Fa-f\d]{0,4}:{1,2}?){2,7}(?:(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|[A-Fa-f\d]{0,4})?)|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))"
       patch2.return_value = r'(?:\b(?:\w+-\d+\/\d+\/|em|irb|as|ae|rlsq|rsp|fxp|gre|ipip|reth|lo|vlan|psgr|pimd|pime|pip0|pp0|tap)\d*(?::\d+)?(?:\.\d+)?)'
       #self.cgn.dh = MagicMock()
       #self.response = {}
       #self.xml = xml_tool()
       dd = {}
       dd = lambda:defaultdict(dd)
       self.cgn.dd = MagicMock()
       self.cgn.dd.return_value = dd()
       #self.cgn.dh.cli = MagicMock()

       test = Values()
       test.response = MagicMock()
       test.response.return_value = """JSERVICES]_LOG_SESSION_OPEN: App: icmp, ge-2/1/4.0 40.1.1.2:56350 [70.0.0.3:1024] -> 64:ff9b::6401:102:32768 [50.1.1.2] (ICMP)
                                        JSERVICES]_LOG_SESSION_OPEN: App: icmp, ge-2/1/4.0 40.1.1.2:56350 [70.0.0.3] -> 64:ff9b::6401:102:32768 [50.1.1.2:32678] (ICMP)
                                        JSERVICES]_LOG_SESSION_OPEN: App: icmp, ge-2/1/4.0 40.1.1.2:56350 [70.0.0.3:1024] -> 64:ff9b::6401:102:32768 (ICMP)
                                        JSERVICES]_LOG_SESSION_OPEN: App: icmp, ge-2/1/4.0 40.1.1.2:56350 [70.0.0.3] -> 90.1.1.2:32768 (ICMP)
                                        JSERVICES]_LOG_SESSION_OPEN: App: icmp, ge-2/1/4.0 40.1.1.2:56350 -> 90.1.1.2:32768 (ICMP)
                                        JSERVICES]_LOG_SESSION_OPEN: 40.1.1.2:56350 -> 90.1.1.2:32768 (ICMP)
                                        JSERVICES]_LOG_SESSION_OPEN: 40.1.1.2:56350 [70.0.0.3] -> 90.1.1.2:32768 (ICMP)
                                        JSERVICES]_LOG_SESSION_OPEN: 40.1.1.2:56350 [70.0.0.3:1024] -> 90.1.1.2:32768 (ICMP)
                                        JSERVICES]_LOG_SESSION_OPEN: 40.1.1.2:56350 -> 90.1.1.2:32768 [70.1.1.1] (ICMP)
                                        JSERVICES_NAT_RULE_MATCH: proto 58 (ICMPV6) application: icmpv6, 2001::2:54045 -> 64:ff9b::6401:102:32768, Match NAT rule-set: (null), rule: nat64_rule, term: 0
                                        JSERVICES_NAT_RULE_MATCH: proto 58 (ICMPV6) app: icmpv6, ge-2/1/4.0 2001::2:54045 -> 64:ff9b::6401:102:32768, Match NAT rule-set (null), rule nat64_rule, term 0
                                        JSERVICES]_LOG_SESSION_OPEN: application: icmp, ge-2/1/4.0 40.1.1.2:56350 [70.0.0.3:1024] -> [90.1.1.2] 85.1.1.2:2020 (UDP)
                                        JSERVICES_SESSION_OPEN: proto 58 (ICMPV6) application: icmp, ge-2/1/4.0:40.1.1.2:56350 -> 100.1.1.2:2048, Match NAT rule-set: (null), rule: nat64_rule, term: 0
                                        JSERVICES_SESSION_OPEN: application:icmp, ge-2/1/4.0 40.1.1.2:56350 [70.0.0.3:1024] ->  100.1.1.2:2048 (ICMP ECHO REQUEST)
                                        JSERVICES_SESSION_OPEN: application:icmpv6, ge-2/1/4.0 2001::2:54045 [80.0.0.8:1024] -> [100.1.1.2] 64:ff9b::6401:102:32768 (ICMPV6 ECHO REQUEST)
                                        JSERVICES_NAT_RULE_MATCH: proto 58 (ICMPV6 ECHO REQUEST) application: icmpv6, ge-2/1/4.0:2001::2:54045 -> 64:ff9b::6401:102:32768, Match NAT rule-set: (null), rule: nat64_rule, term: 0
                                        """
       # print("Return Value : ".format(self.cgn.dh.cli.return_value))
       #self.cgn.log = MagicMock()
       #self.cgn.log.return_value = None
       # test = Values()
       # test.response = MagicMock()
       # test.response.return_value = 
       self.cgn.dh.cli.return_value = test
       options = {'src_ip' : "10.1.1.2", 'src_port' : "1024"}
       self.assertNotEqual(self.cgn._get_syslogs(ptrn="Some dummy Argument", **options), None)

    # @patch('jnpr.toby.services.services.dh.cli')
    @patch('jnpr.toby.services.cgnat.utils.get_regex_ip')
    def test_get_sess_xtnsv_withport(self,patch_utils):
        #output=Values()
        #output.splitlines=MagicMock()
        #output.splitlines.return_value = """ms-4/0/0
        output = """ms-4/0/0
        Service Set: service_set, Session: 1546478221, ALG: none, Flags: 0x0000, IP Action: no, Offload: no, Asymmetric: no
        NAT PLugin Data:
          NAT Action:   Translation Type - NAPT-44
            NAT source             1.1.1.1:63      ->     1.1.1.1:1024
        UDP            1.1.1.1:63     ->      1.1.1.1:63     Forward  I               9
            Byte count: 414
            Flow role: Initiator, Timeout: 30
        UDP          1.1.1.1:63     ->     1.1.1.1:1024   Forward  O               0
            Byte count: 0
            Flow role: Responder, Timeout: 30
        """
        patch_utils.return_value = '1.1.1.1'
        #self.cgn.dh = MagicMock()
        #self.cgn.dh.cli = MagicMock()
        test = Values()
        test.response = MagicMock()
        test.response.return_value = output
        self.cgn.dh.cli.return_value = test
        self.assertTrue(self.cgn.get_sessions_extensive(ss='a',sp='ms-4/0/0',app_proto='tcp',src_pfx='1.1.1.1',dst_pfx='2.2.2.2',src_port='1024',limit='0'),dict)

    @patch('jnpr.toby.services.cgnat.utils.get_regex_ip')
    def test_get_sess_xtnsv_withport_continue(self,patch_utils):
        #output=Values()
        #output.splitlines=MagicMock()
        #output.splitlines.return_value = """ms-4/0/0
        output = """ms-4/0/0
        Service Set: service_set, Session: 1546478221, ALG: none, Flags: 0x0000, IP Action: no, Offload: no, Asymmetric: no
        NAT PLugin Data:
          NAT Action:   Translation Type - NAPT-64
            NAT destination             1.1.1.1:23      ->     1.1.1.1:23

        UDP            1.1.1.1:63     ->      1.1.1.1:63     Forward  I               9
            Byte count: 414
          NAT destination             1.1.1.1      ->     1.1.1.1
          NAT Action:   Translation Type - NAT64
          NAT destination             1.1.1.1      ->     1.1.1.1
            NAT destination             1.1.1.1      ->     1.1.1.1
        UDP            1.1.1.1     ->      1.1.1.1    Forward  I               9
            Byte count: 414
            Flow role: Initiator, Timeout: 30
        UDP          1.1.1.1:63     ->     1.1.1.1:1024   Forward  O               0
            Byte count: 0
            Flow role: Responder, Timeout: 30
        NAT PLugin Data:
          NAT Action:   Translation Type - NAT64
            NAT destination             1.1.1.1:63      ->     1.1.1.1:1024
        UDP            1.1.1.1:63     ->      1.1.1.1:63     Forward  I               9
            Byte count: 414
        """
        
        patch_utils.return_value = '1.1.1.1'
        #self.cgn.dh = MagicMock()
        #self.cgn.dh.cli = MagicMock()

        test = Values()
        test.response = MagicMock()
        test.response.return_value = output
        self.cgn.dh.cli.return_value = test
        self.assertTrue(self.cgn.get_sessions_extensive(ss='a',sp='ms-4/0/0',app_proto='tcp',src_pfx='1.1.1.1',dst_pfx='2.2.2.2',src_port='1024',limit='0'),dict)
    # @patch('jnpr.toby.services.services.dh.cli')
    # @patch('jnpr.toby.services.services.utils.get_regex_ip')
    # def test_get_sess_xtnsv_withip(self,patch_utils):
        # output = ms-4/0/0
        # Service Set: service_set, Session: 1546478221, ALG: none, Flags: 0x0000, IP Action: no, Offload: no, Asymmetric: no
        # NAT PLugin Data:
        #   NAT Action:   Translation Type - NAPT-44
        #     NAT source             1.1.1.1      ->     1.1.1.1
        # UDP            1.1.1.1     ->      1.1.1.1    Forward  I               9
        #   Byte count: 414
        #   Flow role: Initiator, Timeout: 30
        # UDP          1.1.1.1     ->     1.1.1.1   Forward  O               0
        #   Byte count: 0
        #   Flow role: Responder, Timeout: 30
        
        # patch_utils.return_value = '1.1.1.1' 
        # self.cgn.dh = MagicMock()
        # self.cgn.dh.cli = MagicMock()
        # self.cgn.dh.cli.return_value = output
        # self.assertTrue(self.cgn.get_sessions_extensive(),dict)
      

    # @patch('jnpr.toby.services.services.dh.cli')
    @patch('jnpr.toby.services.cgnat.utils.get_regex_ip')
    def test_get_sess_xtnsv_nonnat_withip(self,patch_utils):
        output = """ms-4/0/0 
        Service Set: AMS_NAT, Session: 838980419, ALG: icmp, Flags: 0x0000, IP Action: no, Offload: no, Asymmetric: no
        ICMP         1.1.1.1        ->    1.1.1.1        Forward  I               1
          Byte count: 1289
          Flow role: Initiator, Timeout: 300
        ICMP       1.1.1.1        ->      1.1.1.1        Forward  O               0
          Byte count: 0
          Flow role: Responder, Timeout: 300
        """
        patch_utils.return_value = '1.1.1.1'
        #self.cgn.dh = MagicMock()
        #self.cgn.dh.cli = MagicMock()
        test = Values()
        test.response = MagicMock()
        test.response.return_value = output
        self.cgn.dh.cli.return_value = test
        self.assertTrue(self.cgn.get_sessions_extensive(),dict)


    # @patch('jnpr.toby.services.services.dh.cli')
    @patch('jnpr.toby.services.cgnat.utils.get_regex_ip')
    def test_get_sess_xtnsv_nonnat_withport(self,patch_utils):
        output = """ms-4/0/0
        Service Set: AMS_NAT, Session: 838980419, ALG: icmp, Flags: 0x0000, IP Action: no, Offload: no, Asymmetric: no
        UDP         1.1.1.1:63        ->    1.1.1.1:1024        Forward  I               1
          Byte count: 1289
          Flow role: Initiator, Timeout: 300
        UDP       1.1.1.1:1024        ->      1.1.1.1:63        Forward  O               0
          Byte count: 0
          Flow role: Responder, Timeout: 300
        """
        patch_utils.return_value = '1.1.1.1'
        #self.cgn.dh = MagicMock()
        #self.cgn.dh.cli = MagicMock()
        test = Values()
        test.response = MagicMock()
        test.response.return_value = output
        self.cgn.dh.cli.return_value = test
        self.assertTrue(self.cgn.get_sessions_extensive(),dict)
   
    # @patch('jnpr.toby.services.services.dh.cli')
    # @patch('jnpr.toby.services.services.utils.get_regex_ip')
    # def test_get_sess_xtnsv_nat64_withport(self,patch_utils):
        # output = ms-4/0/0
        # Service Set: service_set, Session: 1546478221, ALG: none, Flags: 0x0000, IP Action: no, Offload: no, Asymmetric: no
        # NAT PLugin Data:
        #   NAT Action:   Translation Type - NAT64
        #     NAT destination             1.1.1.1:63      ->     1.1.1.1:1024
        # UDP            1.1.1.1:63     ->      1.1.1.1:63     Forward  I               9
        #     Byte count: 414
        #     Flow role: Initiator, Timeout: 30
        # UDP          1.1.1.1:63     ->     1.1.1.1:1024   Forward  O               0
        #     Byte count: 0
        #     Flow role: Responder, Timeout: 30
        
        # patch_utils.return_value = '1.1.1.1'
        # self.cgn.dh = MagicMock()
        # self.cgn.dh.cli = MagicMock()
        # self.cgn.dh.cli.return_value = output
        # self.assertTrue(self.cgn.get_sessions_extensive(),dict)
  
    # @patch('jnpr.toby.services.services.dh.cli')
    @patch('jnpr.toby.services.cgnat.utils.get_regex_ip')
    def test_get_sess_xtnsv_nat64_withip(self,patch_utils):
        output = """ms-4/0/0
        Service Set: service_set, Session: 1546478221, ALG: none, Flags: 0x0000, IP Action: no, Offload: no, Asymmetric: no
        NAT PLugin Data:
          NAT Action:   Translation Type - NAT64
            NAT source             1.1.1.1      ->     1.1.1.1
        UDP            1.1.1.1     ->      1.1.1.1     Forward  I               9
            Byte count: 414
            Flow role: Initiator, Timeout: 30
        UDP          1.1.1.1     ->     1.1.1.1   Forward  O               0
            Byte count: 0
            Flow role: Responder, Timeout: 30
        """
        patch_utils.return_value = '1.1.1.1'
        #self.cgn.dh = MagicMock()
        #self.cgn.dh.cli = MagicMock()
        test = Values()
        test.response = MagicMock()
        test.response.return_value = output
        self.cgn.dh.cli.return_value = test
        self.assertTrue(self.cgn.get_sessions_extensive(),dict)

    def test_cgnat_verify_sessions_extensive_true(self):

        self.cgn.get_sessions_extensive = MagicMock()
        self.cgn.get_sessions_extensive.return_value = {'sess_xtnsv':{'ms-5/0/0':  {'ss1': {'np1': {'11.1.1.2':  {'5060':  {'eim_nat_ip': '39.7.56.46', 'eim_nat_port': '2000', 'eim_sess_cnt': '0','eim_state': 'timeout ', 'nat_ip': '', 'nat_port':''}, 'app_ports_in_use': '0', 'app_sess_cnt': '0', 'app_state': 'timeout', 'app_state_to': '20'}}}}}}
        self.cgn.data =  {'sess_xtnsv':{'ms-5/0/0':  {'ss1': {'11.1.1.2':  {'5060':  {'eim_nat_ip': '39.7.56.46', 'eim_nat_port': '2000', 'eim_sess_cnt': '0','eim_state': 'timeout ', 'nat_ip': '', 'nat_port':''}, 'app_ports_in_use': '0', 'app_sess_cnt': '0', 'app_state': 'timeout', 'app_state_to': '20', 'nat_ip': '', 'nat_port':''}}}}}
        self.cgn.sset = {'ss1': {'spic': 'ms-5/0/0', 'nat_rules': ['nr1'], 'sl_class_list':['stateful-firewall-logs', 'nat-logs', 'session-logs']}}
        self.cgn.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_port': '5060', 'dst_ip': '11.1.1.2', 'protocol':''},{'src_ip': '11.1.1.2','src_port': '5060', 'dst_ip': '11.1.1.2', 'protocol':''},{'src_ip': '11.1.1.2','src_port': '5060', 'dst_ip': '11.1.1.2', 'protocol':''}]}, 'total': 10}
        self.cgn._is_nat_ip_in_pool = MagicMock()
        self.cgn._is_nat_ip_in_pool.return_value = True
        self.cgn._is_nat_port_in_pool = MagicMock()
        self.cgn._is_nat_port_in_pool.return_value = True
        self.cgn._verify_syslogs = MagicMock()
        self.cgn._verify_syslogs.return_value = True
        self.cgn._get_src_ip_flow_from_data = MagicMock()
        self.cgn._get_src_ip_flow_from_data.return_value = {'nat_ip': '', 'nat_port':''}
        self.assertEqual(self.cgn.verify_sessions_extensive(limit=1), True)

        self.cgn.data =  {'sess_xtnsv':{'ms-5/0/0':  {'ss1': {'11.1.1.2':  {'5060':  None, 'app_ports_in_use': '0', 'app_sess_cnt': '0', 'app_state': 'timeout', 'app_state_to': '20', 'nat_ip': '', 'nat_port':''}}}}}
        self.assertEqual(self.cgn.verify_sessions_extensive(limit=1), True)
        self.cgn.data =  {'sess_xtnsv':{'ms-5/0/0':  {'ss1': {'11.1.1.2': {}}}}}
        self.assertEqual(self.cgn.verify_sessions_extensive(limit=1), True)

    # def test_cgnat_verify_sessions_extensive_src_flow_none(self):

    #     self.cgn._get_src_ip_flow_from_data = MagicMock()
    #     self.cgn._get_src_ip_flow_from_data.return_value = None   
    #     self.assertEqual(self.cgn.verify_sessions_extensive(), True)

    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_verify_detnat_port_block(self, test_cmp_dicts):
        test_cmp_dicts.return_value = MagicMock()
        self.cgn.get_detnat_port_block = MagicMock()
        self.cgn.get_detnat_port_block.return_value = {"1.1.1.1":""}
        self.assertNotEqual(self.cgn.verify_detnat_port_block(internal_ip="1.1.1.1"), "")
        
    @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    def test_get_detnat_port_blocks(self, patch_cmp):
        patch_cmp.return_value = True
        output = '''
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4D0/junos">
    <service-detnat-information>
        <service-set-name></service-set-name>
        <interface-name>ms-5/0/0</interface-name>
        <pool-name>nat_pool1</pool-name>
        <detnat-internal-host>2001:2010::10</detnat-internal-host>
        <detnat-nat-ip>111.111.1.1</detnat-nat-ip>
       <detnat-nat-port-low>5120</detnat-nat-port-low>
        <detnat-nat-port-high>5375</detnat-nat-port-high>
    </service-detnat-information>
    <cli>
        <banner>[edit]</banner>
    </cli>
</rpc-reply>
        '''        
        xml_tree = self.xml.xml_string_to_dict(xml_str=output)
        xml_tree = xml_tree['rpc-reply']
        self.cgn.get_xml_output = MagicMock()
        xpath = 'service-detnat-information'
        for path in  xpath.split('/'):
            xml_tree = xml_tree[path]
        self.cgn.get_xml_output.return_value = xml_tree
        options = {'name':'MX1_CGN4_AMS4-CONE-p1'}
        self.cgn.dh.cli.return_value = output
        self.assertTrue(self.cgn.get_detnat_port_block(internal_ip="1.1.1.1"),dict)


    # @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    # @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    # def test_cgnat_verify_sessions_extensive_wrong_nat_port(self, patch1, patch2):

    #     self.cgn.get_sessions_extensive = MagicMock()
    #     self.cgn.get_sessions_extensive.return_value= {'sess_xtnsv':{'ms-5/0/0':  {'ss1': {'np1': {'11.1.1.2':  {'5060':  {'eim_nat_ip': '39.7.56.46', 'eim_nat_port': '80', 'eim_sess_cnt': '0','eim_state': 'timeout '}, 'app_ports_in_use': '0', 'app_sess_cnt': '0', 'app_state': 'timeout', 'app_state_to': '20'}}}}}}
    #     patch1.return_value = True
    #     patch2.return_value = True
    #     self.assertEqual(self.cgn.verify_sessions_extensive(limit=1), True)

    # @patch('jnpr.toby.utils.iputils.is_ip_in_subnet')
    # @patch('jnpr.toby.services.cgnat.utils.cmp_dicts')
    # def test_cgnat_verify_sessions_extensive_ip_not_in_range(self, patch1, patch2):

    #     self.cgn.get_sessions_extensive = MagicMock()
    #     self.cgn.get_sessions_extensive.return_value= {'sess_xtnsv':{'ms-5/0/0':  {'ss1': {'np1': {'11.1.1.2':  {'5060':  {'eim_nat_ip': '39.7.56.46', 'eim_nat_port': '80', 'eim_sess_cnt': '0','eim_state': 'timeout '}, 'app_ports_in_use': '0', 'app_sess_cnt': '0', 'app_state': 'timeout', 'app_state_to': '20'}}}}}}
    #     patch1.return_value = True
    #     patch2.return_value = False
    #     self.assertEqual(self.cgn.verify_sessions_extensive(limit=1), True)
    # # verify_sessions_extensive


if __name__ == '__main__':
  unittest.main()