from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from optparse import Values
from collections import defaultdict
import builtins

from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.hldcl.unix.unix import UnixHost

from jnpr.toby.services.pcp import pcp


builtins.t = {}

class MissingMandatoryArgument(ValueError):
    """Class for raising custom exception for missing mandatory argument"""
    def __init__(self, err_msg):
        """Constructor method to add message to missing mandatory argument"""
        builtins.t = MagicMock()
        t.log('ERROR', "Missing mandatory argument, {}".format(err_msg))
        super().__init__("Missing mandatory argument, {}".format(err_msg))

class Test_pcp(unittest.TestCase):

    def setUp(self):
        self.pcp = pcp(dh=None)
        self.xml = xml_tool()
        self.pcp.log = MagicMock()
        self.pcp.config = MagicMock()
        self.pcp.config.return_value = True
        self.pcp.cmd_add = MagicMock()
        self.pcp.config = MagicMock()
        self.pcp.dh = MagicMock()
        self.pcp.dh.cli = MagicMock()
        self.pcp.dh.cli = MagicMock()
        self.pcp.fn_checkin = MagicMock()
        self.pcp.fn_checkout = MagicMock()
        self.pcp.fn_checkout.return_value = True

        dd = {}
        dd = lambda:defaultdict(dd)
        self.pcp.dd = MagicMock()
        self.pcp.dd.return_value = dd()

        self.pcp.r_if = {'ss1'}
        self.pcp.resource = 'esst480p'
        #self.pcp.topo = {'intf' : {'ms-5/0/0' : { 'path' : 'r0r1'}}, 'path_res' : { 'esst480p' : { 'r0r1' : ['intf1']}}}
        self.pcp.topo = {'intf' : {'1/1' : { 'path' : 'r0r1'}}, 'path_res' : { 'esst480p' : { 'r0r1' : ['intf1']}}}
        builtins.t = {'resources' : {'esst480p' : { 'interfaces' : { 'intf1' : {'pic' : 'ms-5/0/0' }}}}}
        self.pcp.intf_ss = {'ms-5/0/0' : 'ss1'}
        self.pcp.sset = {'ss1': {'spic': 'ms-5/0/0', 'nat_rules': ['nr1']}}
        #self.pcp.nat_rule = {'nr1': {'src_pool': 'np1'}}
        #self.pcp.nat_rule = {'nr1': {'src_pool': 'np1', 'trans_type': 'dnat','trans_eim': 1,'trans_eif': 1}}
        self.pcp.nat_rule = {'nr1': {'src_pool': 'np1', 'trans_type': 'napt','trans_eim': 1,'trans_eif': 1}}
        self.pcp.nat_pool = {'np1': {'trans_type':'napt', 'addr': '112.1.1.0/24','nat_port': '1024-3456'}, 'np2': {'trans_type':'dynamic', 'addr': '120.1.1.0/24'}}
        #self.pcp.tg_sess = {'ms-5/0/0': {'sess_list': [{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'}]}}
        self.pcp.tg_sess = {'1/1': {'total': 10, 'src_ips_list': ['11.1.1.2', '11.1.1.3'], 'dst_ips_list': ['60.1.1.2', '60.1.1.3'], 'sess_list': [{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'},{'src_ip': '11.1.1.2','src_port': '5060'}]}, 'total': 10}
        self.pcp.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        #self.pcp.tg_sess_cnt_pcp = {'1/1':10, 'total': 10}
        self.pcp.pool_map = {'np1': {'tot_sess': 10}, 'np2': {'tot_sess': 10}}
        self.pcp.MissingMandatoryArgument = MissingMandatoryArgument

    @patch('jnpr.toby.services.pcp.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.pcp.utils.update_opts_from_args')
    def test_set_pcp_rule(self, utils_update, iputils_patch):
        iputils_patch.return_value = '1.1.1.1'
        options = { 'count': 1, 'action': 'set', 'dir': 'input',
                                               'term': 0, 'num_terms': 1, 'term_idx_reset': True,
                                               'src_addr': "1.1.1.1", 'src_addr_nw_step': 1,}
        utils_update.return_value = options
        self.assertNotEqual(self.pcp.set_pcp_rule(), None)

    @patch('jnpr.toby.services.pcp.iputils.incr_ip_subnet')
    @patch('jnpr.toby.services.pcp.utils.update_opts_from_args')
    def test_set_pcp_server(self, utils_update, iputils_patch):
        iputils_patch.return_value = '1.1.1.1'
        options = { 'count': 1, 'action': 'delete', 'max_clnt_maps': 128, 
                                               'min_map_life': 120, 'max_map_life': 300, 
                                               'v4_addr': '1.1.1.1', 'v6_addr': '1.1.1.1', 
                                               'v4_addr_nw_step': 1, 'v6_addr_nw_step': 1,}
        utils_update.return_value = options
        self.assertNotEqual(self.pcp.set_pcp_server(), None)

    def test_clear_pcp_statistics(self):
        self.pcp.dh.cli.return_value = True
        self.assertNotEqual(self.pcp.clear_pcp_statistics(intf=""), None)
        with self.assertRaises(MissingMandatoryArgument) as context:
          self.pcp.clear_pcp_statistics()
        self.assertTrue('Missing mandatory argument, intf' in str(context.exception))

    @patch('jnpr.toby.services.pcp.cgnat.verify')
    def test_verify(self, verify_patch):
        verify_patch.return_value = None
        self.assertNotEqual(self.pcp.verify(intf=""), "")

    @patch('jnpr.toby.services.pcp.iputils.is_ip_ipv6')
    def test_get_pcp_mappings(self, ipv6_patch):
        ipv6_patch.return_value = True
        output = """ Interface: sp-2/0/0, Service set: sset_1

 NAT pool: nat_pool1
 
 PCP Client       : 2001::c                 PCP lifetime : 119
 Mapping          : 40.0.0.2        : 1032  --> 33.33.33.11     : 1034
 Session Count    :     2
 Mapping State    : Active
 B4 Address       : 2001::c
 
 PCP Client       : 2001::e                 PCP lifetime : 119
 Mapping          : 40.0.0.2        : 1031  --> 33.33.33.11     : 1052
 Session Count    :     2
 Mapping State    : Active
 B4 Address       : 2001::e
"""     
        self.pcp.dh.cli.return_value = output
        self.assertNotEqual(self.pcp.get_pcp_mappings(), "")
        output = """"""
        self.pcp.dh.cli.return_value = output
        self.assertNotEqual(self.pcp.get_pcp_mappings(), "")
        output = """ Interface: sp-2/0/0, Service set: sset_1

 NAT pool: nat_pool1
 
 PCP Client       
 Mapping          : 40.0.0.2        : 1032  --> 33.33.33.11     : 1034
 Session Count    :     2
 Mapping State    : Active
 B4 Address       : 2001::c
 
 PCP Client       :
 Mapping          : 40.0.0.2        : 1031  --> 33.33.33.11     : 1052
 Session Count    :     2
 Mapping State    : Active
 B4 Address       : 2001::e
"""   
        self.pcp.dh.cli.return_value = output
        self.assertNotEqual(self.pcp.get_pcp_mappings(), "")

    @patch('jnpr.toby.services.pcp.iputils.cmp_ip')
    @patch('jnpr.toby.services.pcp.utils.cmp_dicts')
    def test_verify_pcp_mappings(self, cmp_patch, ip_patch):
        cmp_patch.return_value = True
        ip_patch.return_value = True
        self.pcp.get_pcp_mappings = MagicMock()
        self.pcp._get_tg_port_and_config_mapping = MagicMock()
        self.pcp.get_pcp_mappings.return_value = {'state': 'active', 'nat_port': 'ext_port'}        
        self.pcp.tg_cfg_map = {'1/1': {'rand_reqs_idx_list':[0,1], 'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.pcp.tg_sess['1/1'] = {'pcp_maps_list':[{'ext_port':"", 'ext_ip':""}, {'ext_port':"", 'ext_ip':""}]}
        self.pcp._get_pcp_ip_port_flow_from_data = MagicMock()
        self.pcp._get_pcp_ip_port_flow_from_data.return_value = {'nat_ip':""}
        self.assertNotEqual(self.pcp.verify_pcp_mappings(), "")
        self.pcp._get_pcp_ip_port_flow_from_data.return_value = {'nat_ip':None}
        # ip_patch.return_value = False
        self.assertNotEqual(self.pcp.verify_pcp_mappings(), "")
        self.pcp._get_pcp_ip_port_flow_from_data.return_value = {'nat_ip':""}
        ip_patch.return_value = False
        self.assertNotEqual(self.pcp.verify_pcp_mappings(), "")

    @patch('jnpr.toby.services.pcp.utils.update_data_from_output')
    def test_get_pcp_statistics(self, update_data):
        output = '''
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4D0/junos">
    <service-pcp-statistics-information>
        <flow-analysis-statistics-pic-info>
            <pic-name>ms-1/2/0</pic-name>
        </flow-analysis-statistics-pic-info>
        <pcp-protocol-statistics>
            <map-request-received>1</map-request-received>
            <peer-request-received>0</peer-request-received>
            <other-operational-counters>0</other-operational-counters>
            <unprocessed-requests-received>0</unprocessed-requests-received>
            <third-party-requests-received>0</third-party-requests-received>
            <prefer-fail-options-received>0</prefer-fail-options-received>
            <filter-option-received>0</filter-option-received>
            <other-options-counters>0</other-options-counters>
            <option-optional-received>0</option-optional-received>
            <pcp-success>1</pcp-success>
            <pcp-unsupported-version>0</pcp-unsupported-version>
            <not-authorized>0</not-authorized>
            <bad-requests>0</bad-requests>
            <unsupported-opcode>0</unsupported-opcode>
            <unsupported-option>0</unsupported-option>
            <bad-option>0</bad-option>
            <network-failure>0</network-failure>
            <out-of-resources>0</out-of-resources>
            <unsupported-protocol>0</unsupported-protocol>
            <user-exceeded-quota>0</user-exceeded-quota>
            <cannot-provide-external>0</cannot-provide-external>
            <address-mismatch>0</address-mismatch>
            <excessive-number-of-remote-peers>0</excessive-number-of-remote-peers>
            <processing-error>0</processing-error>
            <other-result-counters>0</other-result-counters>
        </pcp-protocol-statistics>
    </service-pcp-statistics-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>'''
        xml_tree = self.xml.xml_string_to_dict(xml_str=output)
        xml_tree = xml_tree['rpc-reply']
        self.pcp.get_xml_output = MagicMock()
        xpath = 'service-pcp-statistics-information'
        for path in  xpath.split('/'):
            xml_tree = xml_tree[path]
        self.pcp.get_xml_output.return_value = xml_tree
        self.assertNotEqual(self.pcp.get_pcp_statistics(spic=""), "")
        with self.assertRaises(MissingMandatoryArgument) as context:
            self.pcp.get_pcp_statistics()
        self.assertTrue('Missing mandatory argument, spic' in str(context.exception))


    @patch('jnpr.toby.services.pcp.utils.cmp_dicts')
    def test_verify_pcp_statistics(self, ip_patch):
        self.pcp._get_tg_port_and_config_mapping = MagicMock()
        self.pcp.tg_sess_cnt = {"spic" : {'total_pcp_reqs':""}}
        self.pcp.get_pcp_statistics = MagicMock()
        self.pcp.get_pcp_statistics.return_value = {"pcp":"", "pc":''}
        self.assertNotEqual(self.pcp.verify_pcp_statistics(other_stats_zero=True, pcp=""), "")

    def test_get_pcp_debug_statistics(self):
        output = '''
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4D0/junos">
    <service-pcp-statistics-information>
        <flow-analysis-statistics-pic-info>
            <pic-name>ms-1/2/0</pic-name>
        </flow-analysis-statistics-pic-info>
        <pcp-debug-statistics>
            <map-request-received>1</map-request-received>
            <peer-request-received>0</peer-request-received>
            <other-operational-counters>0</other-operational-counters>
            <unprocessed-requests-received>0</unprocessed-requests-received>
            <third-party-requests-received>0</third-party-requests-received>
            <prefer-fail-options-received>0</prefer-fail-options-received>
            <filter-option-received>0</filter-option-received>
            <other-options-counters>0</other-options-counters>
            <option-optional-received>0</option-optional-received>
            <pcp-success>1</pcp-success>
            <pcp-unsupported-version>0</pcp-unsupported-version>
            <not-authorized>0</not-authorized>
            <bad-requests>0</bad-requests>
            <unsupported-opcode>0</unsupported-opcode>
            <unsupported-option>0</unsupported-option>
            <bad-option>0</bad-option>
            <network-failure>0</network-failure>
            <out-of-resources>0</out-of-resources>
            <unsupported-debug>0</unsupported-debug>
            <user-exceeded-quota>0</user-exceeded-quota>
            <cannot-provide-external>0</cannot-provide-external>
            <address-mismatch>0</address-mismatch>
            <excessive-number-of-remote-peers>0</excessive-number-of-remote-peers>
            <processing-error>0</processing-error>
            <other-result-counters>0</other-result-counters>
        </pcp-debug-statistics>
    </service-pcp-statistics-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>'''
        xml_tree = self.xml.xml_string_to_dict(xml_str=output)
        xml_tree = xml_tree['rpc-reply']
        self.pcp.get_xml_output = MagicMock()
        xpath = 'service-pcp-statistics-information'
        for path in  xpath.split('/'):
            xml_tree = xml_tree[path]
        self.pcp.get_xml_output.return_value = xml_tree
        self.assertNotEqual(self.pcp.get_pcp_debug_statistics(spic=""), "")
        with self.assertRaises(MissingMandatoryArgument) as context:
            self.pcp.get_pcp_debug_statistics()
        self.assertTrue('Missing mandatory argument, spic' in str(context.exception))


    @patch('jnpr.toby.services.pcp.utils.cmp_dicts')
    def test_verify_pcp_debug_statistics(self, ip_patch):
        self.pcp._get_tg_port_and_config_mapping = MagicMock()
        self.pcp.tg_sess_cnt = {"t":{"spic" : "", 'total_pcp_reqs': 99}}
        self.pcp.get_pcp_debug_statistics = MagicMock()
        self.pcp.get_pcp_debug_statistics.return_value = {"pcp":"", "pc":''}
        self.assertNotEqual(self.pcp.verify_pcp_debug_statistics(other_stats_zero=True, pcp=""), "")

    @patch('jnpr.toby.services.pcp.cgnat._get_tg_port_and_config_mapping')
    def test__get_tg_port_and_config_mapping(self, port_patch):
        self.pcp = pcp(dh=None)
        self.pcp.log = MagicMock()        
        self.pcp.tg_sess = {'1/1' : {'total_pcp_reqs':99}}
        self.pcp.tg_cfg_map = {"1/1":{"spic" : '1/1'}}
        self.pcp.tg_sess_cnt = {"1/1":{}}
        self.assertNotEqual(self.pcp._get_tg_port_and_config_mapping(limit=2, limit_perc=1), "")
        self.pcp.tg_sess_cnt = None
        self.pcp.fn_checkin = MagicMock()
        self.pcp.fn_checkout = MagicMock()
        self.pcp.fn_checkout.return_value = True
        self.assertNotEqual(self.pcp._get_tg_port_and_config_mapping(limit=2, limit_perc=1), "")

    @patch('jnpr.toby.services.pcp.cgnat._get_tg_port_and_config_mapping')
    def test__get_pcp_ip_port_flow_from_data(self, port_patch):
        self.pcp = pcp(dh=None)
        self.pcp.log = MagicMock()    
        self.pcp.fn_checkin = MagicMock()
        self.pcp.fn_checkout = MagicMock()
        self.pcp.fn_checkout.return_value = True    
        data = {'spic':{"sset":{'nat_pool':{'pcp_ip':{'int_ip':{'int_port':""}}}}}}
        self.assertNotEqual(self.pcp._get_pcp_ip_port_flow_from_data({'pcp_ip':"pcp_ip","int_ip":"int_ip", "int_port":"int_port"}, {'spic':"spic","sset":"sset", "nat_pool":"nat_pool"}, data), None)
        data = {'spic':{"sset":{'nat_pool':{'pcp_ip':{'int_ip':{'int_port':None}}}}}}
        self.assertNotEqual(self.pcp._get_pcp_ip_port_flow_from_data({'pcp_ip':"pcp_ip","int_ip":"int_ip", "int_port":"int_port"}, {'spic':"spic","sset":"sset", "nat_pool":"nat_pool"}, data), True)
        data = {'spic':{"sset":{'nat_pool':{'pcp_ip':{}}}}}
        # with self.assertRaises(TypeError) as context:
        self.assertNotEqual(self.pcp._get_pcp_ip_port_flow_from_data({'pcp_ip':"pcp_ip","int_ip":"int_ip", "int_port":"int_port"}, {'spic':"spic","sset":"sset", "nat_pool":"nat_pool"}, data), True)
        # self.pcp._get_pcp_ip_port_flow_from_data({'pcp_ip':"pcp_ip","int_ip":"int_ip", "int_port":"int_port"}, {'spic':"spic","sset":"sset", "nat_pool":"nat_pool"}, data)
        # self.assertTrue('Missing mandatory argument, intf' in str(context.exception))

    @patch('jnpr.toby.services.pcp.iputils.is_ip_in_subnet')
    def test_is_nat_ip_in_pool(self, iputils_patch):
        iputils_patch.return_value = True
        self.pcp = pcp(dh=None)
        self.pcp.log = MagicMock()    
        self.pcp.fn_checkin = MagicMock()
        self.pcp.fn_checkout = MagicMock()
        self.assertNotEqual(self.pcp._is_nat_ip_in_pool({'nat_ip':"", 'eim_nat_ip':""}, {'nat_ip':"", 'eim_nat_ip':""}), "")
        self.assertNotEqual(self.pcp._is_nat_ip_in_pool({'nat_ip':None, 'eim_nat_ip':None}, {'nat_ip':"", 'eim_nat_ip':""}), "")
        iputils_patch.return_value = False
        self.assertNotEqual(self.pcp._is_nat_ip_in_pool({'nat_ip':"", 'eim_nat_ip':""}, {'nat_ip':"", 'eim_nat_ip':""}), "")

    
    @patch('jnpr.toby.services.cgnat.iputils.is_ip_in_subnet')
    def test_is_nat_port_in_pool(self, patch):
        self.pcp = pcp(dh=None)
        self.pcp.log = MagicMock()
        data = {'nat_port': '1025', 'eim_nat_port': '1025', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.pcp.tg_cfg_map = {'1/1': { 'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port': '1024-3456', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.pcp._is_nat_port_in_pool(data, self.pcp.tg_cfg_map['1/1']), True)

    def test_is_nat_port_in_pool_no_nat_port_in_cfg_map(self):        
        self.pcp = pcp(dh=None)
        self.pcp.log = MagicMock()
        data = {'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.pcp.tg_cfg_map = {'1/1': {'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        # del(self.pcp.tg_cfg_map['1/1']['nat_port'])
        self.assertEqual(self.pcp._is_nat_port_in_pool(data, self.pcp.tg_cfg_map['1/1']), False)

        data = {'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.pcp.tg_cfg_map = {'1/1': {'nat_port': '1024-3456', 'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.pcp._is_nat_port_in_pool(data, self.pcp.tg_cfg_map['1/1']), False)
        
        data = {'nat_port': '1', 'eim_nat_port': '1', 'ports_in_use': '10', 'sess_cnt': '0', 'state': 'active', 'state_to': '123'}
        self.pcp.tg_cfg_map = {'1/1': {'nat_port': '1024-3456', 'spic': 'ms-5/0/0', 'sset': 'ss1', 'nat_rule': 'nr1', 'nat_pool': 'np1', 'nat_ip': '112.1.1.0/24', 'nat_port_low': '1024', 'nat_port_high': '3456', 'tot_sess': 1, 'rand_sess_idx_list': [0]}}
        self.assertEqual(self.pcp._is_nat_port_in_pool(data, self.pcp.tg_cfg_map['1/1']), False)












if __name__ == '__main__':
  unittest.main()