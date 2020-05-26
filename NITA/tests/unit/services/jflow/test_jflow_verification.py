#!/usr/local/bin/python3

import sys
import copy
import mock
from mock import patch
from mock import Mock
from mock import MagicMock
import unittest
import unittest2 as unittest
from optparse import Values
from jnpr.toby.services.jflow.jflow_verification import jflow_verification
import builtins
builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'


class Test_jflow_verification(unittest.TestCase):

    def setUp(self):
        self.jf = jflow_verification()
        t.log = MagicMock()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli = MagicMock()
        self.jf.log = t.log
        self.jf.platform = 'MX'
        self.jf.jflow_type = 'INLINE'
        self.maxDiff = None

    def test_main_init(self):
        self.assertEqual(self.jf.log, t.log)

    def test_init_without_kwarg(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        with self.assertRaises(Exception) as context:
            self.jf.init()
        self.assertTrue(
            "please provide the keys with name" in str(context.exception))

    def test_init_with_decode_dump_with_flow_selectors_1(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        with self.assertRaises(Exception) as context:
            self.jf.init(decode_dump_with_flow_selectors = {'decode_dump': {}, 'flow_selector_identifier_info': '2'})
        self.assertTrue(
            "key \'flow_selector_identifier_info\' should have value of type list or tuple" in str(context.exception))

    def test_init_with_decode_dump_with_flow_selectors_2(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        with self.assertRaises(Exception) as context:
            self.jf.init(decode_dump_with_flow_selectors = {'decode_dump': {}, 'flow_selector_identifier_info': [1,2]})
        self.assertTrue(
            "\'flow_selector_identifier_info\' should be the list of dictionary" in str(context.exception))

    def test_init_with_decode_dump_with_flow_selectors_3(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        with self.assertRaises(Exception) as context:
            self.jf.init(decode_dump_with_flow_selectors = {'decode_dump': {}, 'flow_selector_identifier_info': [{'SrcAddr' : '70.0.0.1'}]})
        self.assertTrue(
            "user must provide the values in list type" in str(context.exception))

    def test_init_with_decode_dump_with_flow_selectors_4(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        self.jfdata_template_dict = MagicMock()
        self.jf.option_template_dict = MagicMock()
        self.assertEqual(self.jf.init(decode_dump_with_flow_selectors = {'decode_dump': {}, 'flow_selector_identifier_info': [{'SrcAddr' : ['70.0.0.1']}]}), None)

    def test_get_expected_template_details(self):
        self.jf.get_mx_template_details = MagicMock()
        self.jf.get_mx_template_details.return_value = {'templ_id' : '257'}
        self.assertEqual(self.jf.get_expected_template_details(),{'templ_id' : '257'})

    def test_get_mx_template_details_ipv4_v9(self):
        format_dict = {'data_templ_id': '320', 'expected_option_template_pkt_flowset_name': 'Options Template(V9) (1)', 'expected_data_pkt_flowset_name': '(Data) (320)', 'expected_data_template_pkt_flowset_name': 'Data Template (V9) (0)', 'option_templ_id': '576', 'expected_option_pkt_flowset_name': '(Data) (576)'}
        self.jf.template_type = 'ipv4'
        self.jf.cflow_version = '9'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_ipv6_v9(self):
        format_dict = {'data_templ_id': '321', 'expected_option_template_pkt_flowset_name': 'Options Template(V9) (1)', 'expected_data_pkt_flowset_name': '(Data) (321)', 'expected_data_template_pkt_flowset_name': 'Data Template (V9) (0)', 'option_templ_id': '577', 'expected_option_pkt_flowset_name': '(Data) (577)'}
        self.jf.template_type = 'ipv6'
        self.jf.cflow_version = '9'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_mpls_v9(self):
        format_dict = {'data_templ_id': '323', 'expected_option_template_pkt_flowset_name': 'Options Template(V9) (1)', 'expected_data_pkt_flowset_name': '(Data) (323)', 'expected_data_template_pkt_flowset_name': 'Data Template (V9) (0)', 'option_templ_id': '579', 'expected_option_pkt_flowset_name': '(Data) (579)'}
        self.jf.template_type = 'mpls'
        self.jf.cflow_version = '9'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_mplsv4_v9(self):
        format_dict = {'data_templ_id': '324', 'expected_option_template_pkt_flowset_name': 'Options Template(V9) (1)', 'expected_data_pkt_flowset_name': '(Data) (324)', 'expected_data_template_pkt_flowset_name': 'Data Template (V9) (0)', 'option_templ_id': '580', 'expected_option_pkt_flowset_name': '(Data) (580)'}
        self.jf.template_type = 'mpls-v4'
        self.jf.cflow_version = '9'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_mplsv6_v9(self):
        format_dict = {'data_templ_id': '327', 'expected_option_template_pkt_flowset_name': 'Options Template(V9) (1)', 'expected_data_pkt_flowset_name': '(Data) (327)', 'expected_data_template_pkt_flowset_name': 'Data Template (V9) (0)', 'option_templ_id': '583', 'expected_option_pkt_flowset_name': '(Data) (583)'}
        self.jf.template_type = 'mpls-ipv6'
        self.jf.cflow_version = '9'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_ipv4_v10(self):
        format_dict = {'data_templ_id': '256', 'expected_option_template_pkt_flowset_name': 'Options Template (V10 [IPFIX]) (3)', 'expected_data_pkt_flowset_name': '(Data) (256)', 'expected_data_template_pkt_flowset_name': 'Data Template (V10 [IPFIX]) (2)', 'option_templ_id': '512', 'expected_option_pkt_flowset_name': '(Data) (512)'}
        self.jf.template_type = 'ipv4'
        self.jf.cflow_version = '10'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_ipv6_v10(self):
        format_dict = {'data_templ_id': '257', 'expected_option_template_pkt_flowset_name': 'Options Template (V10 [IPFIX]) (3)', 'expected_data_pkt_flowset_name': '(Data) (257)', 'expected_data_template_pkt_flowset_name': 'Data Template (V10 [IPFIX]) (2)', 'option_templ_id': '513', 'expected_option_pkt_flowset_name': '(Data) (513)'}
        self.jf.template_type = 'ipv6'
        self.jf.cflow_version = '10'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_mpls_v10(self):
        format_dict = {'data_templ_id': '259', 'expected_option_template_pkt_flowset_name': 'Options Template (V10 [IPFIX]) (3)', 'expected_data_pkt_flowset_name': '(Data) (259)', 'expected_data_template_pkt_flowset_name': 'Data Template (V10 [IPFIX]) (2)', 'option_templ_id': '515', 'expected_option_pkt_flowset_name': '(Data) (515)'}
        self.jf.template_type = 'mpls'
        self.jf.cflow_version = '10'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_mplsv4_v10(self):
        format_dict = {'data_templ_id': '260', 'expected_option_template_pkt_flowset_name': 'Options Template (V10 [IPFIX]) (3)', 'expected_data_pkt_flowset_name': '(Data) (260)', 'expected_data_template_pkt_flowset_name': 'Data Template (V10 [IPFIX]) (2)', 'option_templ_id': '516', 'expected_option_pkt_flowset_name': '(Data) (516)'}
        self.jf.template_type = 'mpls-v4'
        self.jf.cflow_version = '10'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_mplsv6_v10(self):
        format_dict = {'data_templ_id': '263', 'expected_option_template_pkt_flowset_name': 'Options Template (V10 [IPFIX]) (3)', 'expected_data_pkt_flowset_name': '(Data) (263)', 'expected_data_template_pkt_flowset_name': 'Data Template (V10 [IPFIX]) (2)', 'option_templ_id': '519', 'expected_option_pkt_flowset_name': '(Data) (519)'}
        self.jf.template_type = 'mpls-ipv6'
        self.jf.cflow_version = '10'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_vpls_v10(self):
        format_dict = {'data_templ_id': '258', 'expected_option_template_pkt_flowset_name': 'Options Template (V10 [IPFIX]) (3)', 'expected_data_pkt_flowset_name': '(Data) (258)', 'expected_data_template_pkt_flowset_name': 'Data Template (V10 [IPFIX]) (2)', 'option_templ_id': '514', 'expected_option_pkt_flowset_name': '(Data) (514)'}
        self.jf.template_type = 'vpls'
        self.jf.cflow_version = '10'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_vpls_v9(self):
        format_dict = {'data_templ_id': '322','expected_option_template_pkt_flowset_name': 'Options Template(V9) (1)', 'expected_data_pkt_flowset_name': '(Data) (322)', 'expected_data_template_pkt_flowset_name': 'Data Template (V9) (0)', 'option_templ_id': '578', 'expected_option_pkt_flowset_name': '(Data) (578)'}
        self.jf.template_type = 'vpls'
        self.jf.cflow_version = '9'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_bridge_v10(self):
        format_dict = {'data_templ_id': '262', 'expected_option_template_pkt_flowset_name': 'Options Template (V10 [IPFIX]) (3)', 'expected_data_pkt_flowset_name': '(Data) (262)', 'expected_data_template_pkt_flowset_name': 'Data Template (V10 [IPFIX]) (2)', 'option_templ_id': '518', 'expected_option_pkt_flowset_name': '(Data) (518)'}
        self.jf.template_type = 'bridge'
        self.jf.cflow_version = '10'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_mx_template_details_bridge_v9(self):
        format_dict = {'data_templ_id': '326','expected_option_template_pkt_flowset_name': 'Options Template(V9) (1)', 'expected_data_pkt_flowset_name': '(Data) (326)', 'expected_data_template_pkt_flowset_name': 'Data Template (V9) (0)', 'option_templ_id': '582', 'expected_option_pkt_flowset_name': '(Data) (582)'}
        self.jf.template_type = 'bridge'
        self.jf.cflow_version = '9'
        self.assertEqual(self.jf.get_mx_template_details(), format_dict)

    def test_get_chassis_platform_info(self):
        response_path = Values()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MX MX MX MX"
        self.assertEqual(self.jf.get_chassis_platform_info(), 'MX')

    def test_get_jflow_template_version(self):
        response_path = Values()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "Internal modified Template Version: 18.1"
        self.assertEqual(self.jf.get_jflow_template_version(), '18.1')

    def test_get_expected_data_template_ipv4_v10_151(self):
        self.jf.jflow_template_version = '15.1'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'ipv4'
        format_dict = {'DIRECTION': {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}, 'PROTOCOL': {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}, 'DST_MASK': {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}, 'L4_SRC_PORT': {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}, 'SRC_AS': {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}, 'IP_NEXT_HOP': {'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}, 'INPUT_SNMP': {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}, 'IP_TOS': {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}, 'DST_AS': {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}, 'IP TTL MINIMUM': {'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}, 'OUTPUT_SNMP': {'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}, 'IP TTL MAXIMUM': {'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}, 'dot1qCustomerVlanId': {'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}, 'flowEndReason': {'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}, 'dot1qVlanId': {'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}, 'SRC_MASK': {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}, 'L4_DST_PORT': {'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}, 'flowStartMilliseconds': {'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}, 'PKTS': {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}, 'IP_SRC_ADDR': {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}, 'BYTES': {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}, 'SRC_VLAN': {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}, 'IPv4 ID': {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}, 'TCP_FLAGS': {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}, 'flowEndMilliseconds': {'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}, 'ICMP_TYPE': {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}, 'IP_DST_ADDR': {'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}}
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_ipv4_v9_151(self):
        self.jf.jflow_template_version = '15.1'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'ipv4'
        format_dict = {'DST_AS': {'Type': 'DST_AS', 'Element_id': '17', 'Length': '4'}, 'DIRECTION': {'Type': 'DIRECTION', 'Element_id': '61', 'Length': '1'}, 'DST_MASK': {'Type': 'DST_MASK', 'Element_id': '13', 'Length': '1'}, 'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'IP_DST_ADDR': {'Type': 'IP_DST_ADDR', 'Element_id': '12', 'Length': '4'}, 'IP_TOS': {'Type': 'IP_TOS', 'Element_id': '5', 'Length': '1'}, 'L4_SRC_PORT': {'Type': 'L4_SRC_PORT', 'Element_id': '7', 'Length': '2'}, 'ICMP_TYPE': {'Type': 'ICMP_TYPE', 'Element_id': '32', 'Length': '2'}, 'IP_PROTOCOL_VERSION': {'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60', 'Length': '1'}, 'PROTOCOL': {'Type': 'PROTOCOL', 'Element_id': '4', 'Length': '1'}, 'TCP_FLAGS': {'Type': 'TCP_FLAGS', 'Element_id': '6', 'Length': '1'}, 'L4_DST_PORT': {'Type': 'L4_DST_PORT', 'Element_id': '11', 'Length': '2'}, 'LAST_SWITCHED': {'Type': 'LAST_SWITCHED', 'Element_id': '21', 'Length': '4'}, 'SRC_AS': {'Type': 'SRC_AS', 'Element_id': '16', 'Length': '4'}, 'SRC_MASK': {'Type': 'SRC_MASK', 'Element_id': '9', 'Length': '1'}, 'IP_NEXT_HOP': {'Type': 'IP_NEXT_HOP', 'Element_id': '15', 'Length': '4'}, 'FIRST_SWITCHED': {'Type': 'FIRST_SWITCHED', 'Element_id': '22', 'Length': '4'}, 'IP_SRC_ADDR': {'Type': 'IP_SRC_ADDR', 'Element_id': '8', 'Length': '4'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'SRC_VLAN': {'Type': 'SRC_VLAN', 'Element_id': '58', 'Length': '2'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}, 'BGP_NEXT_HOP': {'Type': 'BGP_NEXT_HOP', 'Element_id': '18', 'Length': '4'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}}
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_ipv4_v10_181(self):
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'ipv4'
        format_dict = {'IP_NEXT_HOP': {'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}, 'INPUT_SNMP': {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}, 'DST_MASK': {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}, 'OUTPUT_SNMP': {'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}, 'BYTES': {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}, 'IP_DST_ADDR': {'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}, 'SRC_VLAN': {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}, 'flowEndMilliseconds': {'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}, 'flowEndReason': {'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}, 'TCP_FLAGS': {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}, 'IP TTL MINIMUM': {'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}, 'dot1qCustomerVlanId': {'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}, 'ICMP_TYPE': {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}, 'PROTOCOL': {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}, 'L4_SRC_PORT': {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}, 'L4_DST_PORT': {'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}, 'IP TTL MAXIMUM': {'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}, 'dot1qVlanId': {'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}, 'SRC_AS': {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}, 'IPv4 ID': {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}, 'DIRECTION': {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}, 'PKTS': {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}, 'IP_TOS': {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}, 'IP_PROTOCOL_VERSION': {'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}, 'BGP_NEXT_HOP': {'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}, 'IP_SRC_ADDR': {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}, 'DST_AS': {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}, 'flowStartMilliseconds': {'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}, 'SRC_MASK': {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}}
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_ipv4_v9_181(self):
        format_dict = {'INPUT_SNMP': {'Element_id': '10', 'Type': 'INPUT_SNMP', 'Length': '4'}, 'FIRST_SWITCHED': {'Element_id': '22', 'Type': 'FIRST_SWITCHED', 'Length': '4'}, 'PKTS': {'Element_id': '2', 'Type': 'PKTS', 'Length': '8'}, 'DST_MASK': {'Element_id': '13', 'Type': 'DST_MASK', 'Length': '1'}, 'IP_SRC_ADDR': {'Element_id': '8', 'Type': 'IP_SRC_ADDR', 'Length': '4'}, 'IP_TOS': {'Element_id': '5', 'Type': 'IP_TOS', 'Length': '1'}, 'L4_SRC_PORT': {'Element_id': '7', 'Type': 'L4_SRC_PORT', 'Length': '2'}, 'IPv4 ID': {'Element_id': '54', 'Type': 'IPv4 ID', 'Length': '4'}, 'PROTOCOL': {'Element_id': '4', 'Type': 'PROTOCOL', 'Length': '1'}, 'TCP_FLAGS': {'Element_id': '6', 'Type': 'TCP_FLAGS', 'Length': '1'}, 'dot1qVlanId': {'Element_id': '243', 'Type': 'dot1qVlanId', 'Length': '2'}, 'DIRECTION': {'Element_id': '61', 'Type': 'DIRECTION', 'Length': '1'}, 'SRC_AS': {'Element_id': '16', 'Type': 'SRC_AS', 'Length': '4'}, 'IP TTL MINIMUM': {'Element_id': '52', 'Type': 'IP TTL MINIMUM', 'Length': '1'}, 'IP_NEXT_HOP': {'Element_id': '15', 'Type': 'IP_NEXT_HOP', 'Length': '4'}, 'BYTES': {'Element_id': '1', 'Type': 'BYTES', 'Length': '8'}, 'BGP_NEXT_HOP': {'Element_id': '18', 'Type': 'BGP_NEXT_HOP', 'Length': '4'}, 'SRC_VLAN': {'Element_id': '58', 'Type': 'SRC_VLAN', 'Length': '2'}, 'flowEndReason': {'Element_id': '136', 'Type': 'flowEndReason', 'Length': '1'}, 'SRC_MASK': {'Element_id': '9', 'Type': 'SRC_MASK', 'Length': '1'}, 'dot1qCustomerVlanId': {'Element_id': '245', 'Type': 'dot1qCustomerVlanId', 'Length': '2'}, 'IP_DST_ADDR': {'Element_id': '12', 'Type': 'IP_DST_ADDR', 'Length': '4'}, 'IP_PROTOCOL_VERSION': {'Element_id': '60', 'Type': 'IP_PROTOCOL_VERSION', 'Length': '1'}, 'L4_DST_PORT': {'Element_id': '11', 'Type': 'L4_DST_PORT', 'Length': '2'}, 'LAST_SWITCHED': {'Element_id': '21', 'Type': 'LAST_SWITCHED', 'Length': '4'}, 'OUTPUT_SNMP': {'Element_id': '14', 'Type': 'OUTPUT_SNMP', 'Length': '4'}, 'IP TTL MAXIMUM': {'Element_id': '53', 'Type': 'IP TTL MAXIMUM', 'Length': '1'}, 'ICMP_TYPE': {'Element_id': '32', 'Type': 'ICMP_TYPE', 'Length': '2'}, 'DST_AS': {'Element_id': '17', 'Type': 'DST_AS', 'Length': '4'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'ipv4'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_ipv6_v10(self):
        format_dict = {'L4_DST_PORT': {'Length': '2', 'Element_id': '11', 'Type': 'L4_DST_PORT'}, 'L4_SRC_PORT': {'Length': '2', 'Element_id': '7', 'Type': 'L4_SRC_PORT'}, 'flowEndMilliseconds': {'Length': '8', 'Element_id': '153', 'Type': 'flowEndMilliseconds'}, 'SRC_AS': {'Length': '4', 'Element_id': '16', 'Type': 'SRC_AS'}, 'IPV6_DST_MASK': {'Length': '1', 'Element_id': '30', 'Type': 'IPV6_DST_MASK'}, 'SRC_VLAN': {'Length': '2', 'Element_id': '58', 'Type': 'SRC_VLAN'}, 'flowStartMilliseconds': {'Length': '8', 'Element_id': '152', 'Type': 'flowStartMilliseconds'}, 'IP TTL MAXIMUM': {'Length': '1', 'Element_id': '53', 'Type': 'IP TTL MAXIMUM'}, 'IPV6_DST_ADDR': {'Length': '16', 'Element_id': '28', 'Type': 'IPV6_DST_ADDR'}, 'flowEndReason': {'Length': '1', 'Element_id': '136', 'Type': 'flowEndReason'}, 'icmpTypeCodeIPv6': {'Length': '2', 'Element_id': '139', 'Type': 'icmpTypeCodeIPv6'}, 'INPUT_SNMP': {'Length': '4', 'Element_id': '10', 'Type': 'INPUT_SNMP'}, 'IPV6_SRC_ADDR': {'Length': '16', 'Element_id': '27', 'Type': 'IPV6_SRC_ADDR'}, 'OUTPUT_SNMP': {'Length': '4', 'Element_id': '14', 'Type': 'OUTPUT_SNMP'}, 'PROTOCOL': {'Length': '1', 'Element_id': '4', 'Type': 'PROTOCOL'}, 'IPV6_OPTION_HEADERS': {'Length': '4', 'Element_id': '64', 'Type': 'IPV6_OPTION_HEADERS'}, 'DST_AS': {'Length': '4', 'Element_id': '17', 'Type': 'DST_AS'}, 'dot1qVlanId': {'Length': '2', 'Element_id': '243', 'Type': 'dot1qVlanId'}, 'IPV6_NEXT_HOP': {'Length': '16', 'Element_id': '62', 'Type': 'IPV6_NEXT_HOP'}, 'IP_TOS': {'Length': '1', 'Element_id': '5', 'Type': 'IP_TOS'}, 'TCP_FLAGS': {'Length': '1', 'Element_id': '6', 'Type': 'TCP_FLAGS'}, 'DIRECTION': {'Length': '1', 'Element_id': '61', 'Type': 'DIRECTION'}, 'BYTES': {'Length': '8', 'Element_id': '1', 'Type': 'BYTES'}, 'dot1qCustomerVlanId': {'Length': '2', 'Element_id': '245', 'Type': 'dot1qCustomerVlanId'}, 'IP TTL MINIMUM': {'Length': '1', 'Element_id': '52', 'Type': 'IP TTL MINIMUM'}, 'PKTS': {'Length': '8', 'Element_id': '2', 'Type': 'PKTS'}, 'IPV6_SRC_MASK': {'Length': '1', 'Element_id': '29', 'Type': 'IPV6_SRC_MASK'}, 'IPv4 ID': {'Length': '4', 'Element_id': '54', 'Type': 'IPv4 ID'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'ipv6'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)


    def test_get_expected_data_template_ipv6_v10_192(self):
        format_dict = {'L4_DST_PORT': {'Length': '2', 'Element_id': '11', 'Type': 'L4_DST_PORT'}, 'L4_SRC_PORT': {'Length': '2', 'Element_id': '7', 'Type': 'L4_SRC_PORT'}, 'flowEndMilliseconds': {'Length': '8', 'Element_id': '153', 'Type': 'flowEndMilliseconds'}, 'SRC_AS': {'Length': '4', 'Element_id': '16', 'Type': 'SRC_AS'}, 'IPV6_DST_MASK': {'Length': '1', 'Element_id': '30', 'Type': 'IPV6_DST_MASK'}, 'SRC_VLAN': {'Length': '2', 'Element_id': '58', 'Type': 'SRC_VLAN'}, 'flowStartMilliseconds': {'Length': '8', 'Element_id': '152', 'Type': 'flowStartMilliseconds'}, 'IP TTL MAXIMUM': {'Length': '1', 'Element_id': '53', 'Type': 'IP TTL MAXIMUM'}, 'IPV6_DST_ADDR': {'Length': '16', 'Element_id': '28', 'Type': 'IPV6_DST_ADDR'}, 'flowEndReason': {'Length': '1', 'Element_id': '136', 'Type': 'flowEndReason'}, 'icmpTypeCodeIPv6': {'Length': '2', 'Element_id': '139', 'Type': 'icmpTypeCodeIPv6'}, 'INPUT_SNMP': {'Length': '4', 'Element_id': '10', 'Type': 'INPUT_SNMP'}, 'IPV6_SRC_ADDR': {'Length': '16', 'Element_id': '27', 'Type': 'IPV6_SRC_ADDR'}, 'OUTPUT_SNMP': {'Length': '4', 'Element_id': '14', 'Type': 'OUTPUT_SNMP'}, 'PROTOCOL': {'Length': '1', 'Element_id': '4', 'Type': 'PROTOCOL'}, 'IPV6_OPTION_HEADERS': {'Length': '4', 'Element_id': '64', 'Type': 'IPV6_OPTION_HEADERS'}, 'DST_AS': {'Length': '4', 'Element_id': '17', 'Type': 'DST_AS'}, 'dot1qVlanId': {'Length': '2', 'Element_id': '243', 'Type': 'dot1qVlanId'}, 'IPV6_NEXT_HOP': {'Length': '16', 'Element_id': '62', 'Type': 'IPV6_NEXT_HOP'}, 'IP_TOS': {'Length': '1', 'Element_id': '5', 'Type': 'IP_TOS'}, 'TCP_FLAGS': {'Length': '1', 'Element_id': '6', 'Type': 'TCP_FLAGS'}, 'DIRECTION': {'Length': '1', 'Element_id': '61', 'Type': 'DIRECTION'}, 'BYTES': {'Length': '8', 'Element_id': '1', 'Type': 'BYTES'}, 'dot1qCustomerVlanId': {'Length': '2', 'Element_id': '245', 'Type': 'dot1qCustomerVlanId'}, 'IP TTL MINIMUM': {'Length': '1', 'Element_id': '52', 'Type': 'IP TTL MINIMUM'}, 'PKTS': {'Length': '8', 'Element_id': '2', 'Type': 'PKTS'}, 'IPV6_SRC_MASK': {'Length': '1', 'Element_id': '29', 'Type': 'IPV6_SRC_MASK'}, 'IPv4 ID': {'Length': '4', 'Element_id': '54', 'Type': 'IPv4 ID'},'BGP_IPV6_NEXT_HOP': {'Length': '16', 'Element_id': '63', 'Type': 'BGP_IPV6_NEXT_HOP'}}
        self.jf.jflow_template_version = '19.2'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'ipv6'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_ipv6_v9(self):
        format_dict = {'L4_SRC_PORT': {'Type': 'L4_SRC_PORT', 'Element_id': '7', 'Length': '2'}, 'PROTOCOL': {'Type': 'PROTOCOL', 'Element_id': '4', 'Length': '1'}, 'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'SRC_VLAN': {'Type': 'SRC_VLAN', 'Element_id': '58', 'Length': '2'}, 'IPv4 ID': {'Type': 'IPv4 ID', 'Element_id': '54', 'Length': '4'}, 'IPV6_OPTION_HEADERS': {'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64', 'Length': '4'}, 'DIRECTION': {'Type': 'DIRECTION', 'Element_id': '61', 'Length': '1'}, 'LAST_SWITCHED': {'Type': 'LAST_SWITCHED', 'Element_id': '21', 'Length': '4'}, 'IPV6_DST_ADDR': {'Type': 'IPV6_DST_ADDR', 'Element_id': '28', 'Length': '16'}, 'dot1qCustomerVlanId': {'Type': 'dot1qCustomerVlanId', 'Element_id': '245', 'Length': '2'}, 'IPV6_SRC_ADDR': {'Type': 'IPV6_SRC_ADDR', 'Element_id': '27', 'Length': '16'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'FIRST_SWITCHED': {'Type': 'FIRST_SWITCHED', 'Element_id': '22', 'Length': '4'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}, 'IP_TOS': {'Type': 'IP_TOS', 'Element_id': '5', 'Length': '1'}, 'icmpTypeCodeIPv6': {'Type': 'icmpTypeCodeIPv6', 'Element_id': '139', 'Length': '2'}, 'DST_AS': {'Type': 'DST_AS', 'Element_id': '17', 'Length': '4'}, 'dot1qVlanId': {'Type': 'dot1qVlanId', 'Element_id': '243', 'Length': '2'}, 'L4_DST_PORT': {'Type': 'L4_DST_PORT', 'Element_id': '11', 'Length': '2'}, 'IPV6_DST_MASK': {'Type': 'IPV6_DST_MASK', 'Element_id': '30', 'Length': '1'}, 'flowEndReason': {'Type': 'flowEndReason', 'Element_id': '136', 'Length': '1'}, 'IPV6_NEXT_HOP': {'Type': 'IPV6_NEXT_HOP', 'Element_id': '62', 'Length': '16'}, 'TCP_FLAGS': {'Type': 'TCP_FLAGS', 'Element_id': '6', 'Length': '1'}, 'SRC_AS': {'Type': 'SRC_AS', 'Element_id': '16', 'Length': '4'}, 'IP TTL MINIMUM': {'Type': 'IP TTL MINIMUM', 'Element_id': '52', 'Length': '1'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}, 'IP TTL MAXIMUM': {'Type': 'IP TTL MAXIMUM', 'Element_id': '53', 'Length': '1'}, 'IPV6_SRC_MASK': {'Type': 'IPV6_SRC_MASK', 'Element_id': '29', 'Length': '1'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'ipv6'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)


    def test_get_expected_data_template_ipv6_v9(self):
        format_dict = {'L4_SRC_PORT': {'Type': 'L4_SRC_PORT', 'Element_id': '7', 'Length': '2'}, 'PROTOCOL': {'Type': 'PROTOCOL', 'Element_id': '4', 'Length': '1'}, 'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'SRC_VLAN': {'Type': 'SRC_VLAN', 'Element_id': '58', 'Length': '2'}, 'IPv4 ID': {'Type': 'IPv4 ID', 'Element_id': '54', 'Length': '4'}, 'IPV6_OPTION_HEADERS': {'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64', 'Length': '4'}, 'DIRECTION': {'Type': 'DIRECTION', 'Element_id': '61', 'Length': '1'}, 'LAST_SWITCHED': {'Type': 'LAST_SWITCHED', 'Element_id': '21', 'Length': '4'}, 'IPV6_DST_ADDR': {'Type': 'IPV6_DST_ADDR', 'Element_id': '28', 'Length': '16'}, 'dot1qCustomerVlanId': {'Type': 'dot1qCustomerVlanId', 'Element_id': '245', 'Length': '2'}, 'IPV6_SRC_ADDR': {'Type': 'IPV6_SRC_ADDR', 'Element_id': '27', 'Length': '16'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'FIRST_SWITCHED': {'Type': 'FIRST_SWITCHED', 'Element_id': '22', 'Length': '4'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}, 'IP_TOS': {'Type': 'IP_TOS', 'Element_id': '5', 'Length': '1'}, 'icmpTypeCodeIPv6': {'Type': 'icmpTypeCodeIPv6', 'Element_id': '139', 'Length': '2'}, 'DST_AS': {'Type': 'DST_AS', 'Element_id': '17', 'Length': '4'}, 'dot1qVlanId': {'Type': 'dot1qVlanId', 'Element_id': '243', 'Length': '2'}, 'L4_DST_PORT': {'Type': 'L4_DST_PORT', 'Element_id': '11', 'Length': '2'}, 'IPV6_DST_MASK': {'Type': 'IPV6_DST_MASK', 'Element_id': '30', 'Length': '1'}, 'flowEndReason': {'Type': 'flowEndReason', 'Element_id': '136', 'Length': '1'}, 'IPV6_NEXT_HOP': {'Type': 'IPV6_NEXT_HOP', 'Element_id': '62', 'Length': '16'}, 'TCP_FLAGS': {'Type': 'TCP_FLAGS', 'Element_id': '6', 'Length': '1'}, 'SRC_AS': {'Type': 'SRC_AS', 'Element_id': '16', 'Length': '4'}, 'IP TTL MINIMUM': {'Type': 'IP TTL MINIMUM', 'Element_id': '52', 'Length': '1'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}, 'IP TTL MAXIMUM': {'Type': 'IP TTL MAXIMUM', 'Element_id': '53', 'Length': '1'}, 'IPV6_SRC_MASK': {'Type': 'IPV6_SRC_MASK', 'Element_id': '29', 'Length': '1'},'BGP_IPV6_NEXT_HOP': {'Length': '16', 'Element_id': '63', 'Type': 'BGP_IPV6_NEXT_HOP'}}
        self.jf.jflow_template_version = '19.2'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'ipv6'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)


    def test_get_expected_data_template_mpls_v10_181(self):
        format_dict = {'MPLS_LABEL_2': {'Type': 'MPLS_LABEL_2', 'Element_id': '71', 'Length': '3'}, 'MPLS_LABEL_3': {'Type': 'MPLS_LABEL_3', 'Element_id': '72', 'Length': '3'}, 'flowEndReason': {'Type': 'flowEndReason', 'Element_id': '136', 'Length': '1'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}, 'flowEndMilliseconds': {'Type': 'flowEndMilliseconds', 'Element_id': '153', 'Length': '8'}, 'flowStartMilliseconds': {'Type': 'flowStartMilliseconds', 'Element_id': '152', 'Length': '8'}, 'MPLS_LABEL_1': {'Type': 'MPLS_LABEL_1', 'Element_id': '70', 'Length': '3'}, 'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'mpls'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_mpls_v9_151(self):
        format_dict = {'FIRST_SWITCHED': {'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}, 'LAST_SWITCHED': {'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}, 'MPLS_LABEL_1': {'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}, 'BYTES': {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}, 'MPLS_LABEL_3': {'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}, 'PKTS': {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}, 'OUTPUT_SNMP': {'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}, 'MPLS_LABEL_2': {'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}, 'INPUT_SNMP': {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}}
        self.jf.jflow_template_version = '15.1'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'mpls'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_mpls_v9_181(self):
        format_dict = {'MPLS_LABEL_1': {'Element_id': '70', 'Length': '3', 'Type': 'MPLS_LABEL_1'}, 'PKTS': {'Element_id': '2', 'Length': '8', 'Type': 'PKTS'}, 'flowEndReason': {'Element_id': '136', 'Length': '1', 'Type': 'flowEndReason'}, 'FIRST_SWITCHED': {'Element_id': '22', 'Length': '4', 'Type': 'FIRST_SWITCHED'}, 'LAST_SWITCHED': {'Element_id': '21', 'Length': '4', 'Type': 'LAST_SWITCHED'}, 'BYTES': {'Element_id': '1', 'Length': '8', 'Type': 'BYTES'}, 'MPLS_LABEL_3': {'Element_id': '72', 'Length': '3', 'Type': 'MPLS_LABEL_3'}, 'MPLS_LABEL_2': {'Element_id': '71', 'Length': '3', 'Type': 'MPLS_LABEL_2'}, 'INPUT_SNMP': {'Element_id': '10', 'Length': '4', 'Type': 'INPUT_SNMP'}, 'OUTPUT_SNMP': {'Element_id': '14', 'Length': '4', 'Type': 'OUTPUT_SNMP'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'mpls'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_mplsv4_v10_151(self):
        format_dict = {'flowEndReason': {'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}, 'MPLS_TOP_LABEL_ADDR': {'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}, 'MPLS_LABEL_1': {'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}, 'DST_MASK': {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}, 'IP TTL MAXIMUM': {'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}, 'dot1qVlanId': {'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}, 'IP_NEXT_HOP': {'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}, 'flowEndMilliseconds': {'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}, 'dot1qCustomerVlanId': {'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}, 'IP_DST_ADDR': {'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}, 'TCP_FLAGS': {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}, 'INPUT_SNMP': {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}, 'DIRECTION': {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}, 'IP_TOS': {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}, 'L4_DST_PORT': {'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}, 'PKTS': {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}, 'MPLS_LABEL_2': {'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}, 'IP TTL MINIMUM': {'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}, 'IP_SRC_ADDR': {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}, 'BYTES': {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}, 'IPv4 ID': {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}, 'PROTOCOL': {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}, 'ICMP_TYPE': {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}, 'flowStartMilliseconds': {'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}, 'SRC_MASK': {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}, 'DST_AS': {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}, 'SRC_AS': {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}, 'OUTPUT_SNMP': {'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}, 'MPLS_LABEL_3': {'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}, 'L4_SRC_PORT': {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}, 'SRC_VLAN': {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}}
        self.jf.jflow_template_version = '15.1'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'mpls-v4'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)


    def test_get_expected_data_template_mplsv4_v9_151(self):
        format_dict = {'IP_PROTOCOL_VERSION': {'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60', 'Length': '1'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'MPLS_LABEL_1': {'Type': 'MPLS_LABEL_1', 'Element_id': '70', 'Length': '3'}, 'PROTOCOL': {'Type': 'PROTOCOL', 'Element_id': '4', 'Length': '1'}, 'L4_DST_PORT': {'Type': 'L4_DST_PORT', 'Element_id': '11', 'Length': '2'}, 'SRC_AS': {'Type': 'SRC_AS', 'Element_id': '16', 'Length': '4'}, 'IP_SRC_ADDR': {'Type': 'IP_SRC_ADDR', 'Element_id': '8', 'Length': '4'}, 'ICMP_TYPE': {'Type': 'ICMP_TYPE', 'Element_id': '32', 'Length': '2'}, 'SRC_MASK': {'Type': 'SRC_MASK', 'Element_id': '9', 'Length': '1'}, 'DIRECTION': {'Type': 'DIRECTION', 'Element_id': '61', 'Length': '1'}, 'BGP_NEXT_HOP': {'Type': 'BGP_NEXT_HOP', 'Element_id': '18', 'Length': '4'}, 'TCP_FLAGS': {'Type': 'TCP_FLAGS', 'Element_id': '6', 'Length': '1'}, 'IP_TOS': {'Type': 'IP_TOS', 'Element_id': '5', 'Length': '1'}, 'MPLS_LABEL_3': {'Type': 'MPLS_LABEL_3', 'Element_id': '72', 'Length': '3'}, 'LAST_SWITCHED': {'Type': 'LAST_SWITCHED', 'Element_id': '21', 'Length': '4'}, 'DST_AS': {'Type': 'DST_AS', 'Element_id': '17', 'Length': '4'}, 'MPLS_LABEL_2': {'Type': 'MPLS_LABEL_2', 'Element_id': '71', 'Length': '3'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}, 'MPLS_TOP_LABEL_ADDR': {'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47', 'Length': '4'}, 'FIRST_SWITCHED': {'Type': 'FIRST_SWITCHED', 'Element_id': '22', 'Length': '4'}, 'IP_DST_ADDR': {'Type': 'IP_DST_ADDR', 'Element_id': '12', 'Length': '4'}, 'IP_NEXT_HOP': {'Type': 'IP_NEXT_HOP', 'Element_id': '15', 'Length': '4'}, 'SRC_VLAN': {'Type': 'SRC_VLAN', 'Element_id': '58', 'Length': '2'}, 'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'DST_MASK': {'Type': 'DST_MASK', 'Element_id': '13', 'Length': '1'}, 'L4_SRC_PORT': {'Type': 'L4_SRC_PORT', 'Element_id': '7', 'Length': '2'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}}
        self.jf.jflow_template_version = '15.1'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'mpls-v4'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_mplsv4_v10_181(self):
        format_dict = {'IP_PROTOCOL_VERSION': {'Element_id': '60', 'Length': '1', 'Type': 'IP_PROTOCOL_VERSION'}, 'PROTOCOL': {'Element_id': '4', 'Length': '1', 'Type': 'PROTOCOL'}, 'L4_SRC_PORT': {'Element_id': '7', 'Length': '2', 'Type': 'L4_SRC_PORT'}, 'BGP_NEXT_HOP': {'Element_id': '18', 'Length': '4', 'Type': 'BGP_NEXT_HOP'}, 'MPLS_LABEL_3': {'Element_id': '72', 'Length': '3', 'Type': 'MPLS_LABEL_3'}, 'TCP_FLAGS': {'Element_id': '6', 'Length': '1', 'Type': 'TCP_FLAGS'}, 'flowEndReason': {'Element_id': '136', 'Length': '1', 'Type': 'flowEndReason'}, 'DST_MASK': {'Element_id': '13', 'Length': '1', 'Type': 'DST_MASK'}, 'INPUT_SNMP': {'Element_id': '10', 'Length': '4', 'Type': 'INPUT_SNMP'}, 'BYTES': {'Element_id': '1', 'Length': '8', 'Type': 'BYTES'}, 'IP_NEXT_HOP': {'Element_id': '15', 'Length': '4', 'Type': 'IP_NEXT_HOP'}, 'dot1qCustomerVlanId': {'Element_id': '245', 'Length': '2', 'Type': 'dot1qCustomerVlanId'}, 'ICMP_TYPE': {'Element_id': '32', 'Length': '2', 'Type': 'ICMP_TYPE'}, 'SRC_AS': {'Element_id': '16', 'Length': '4', 'Type': 'SRC_AS'}, 'IP_SRC_ADDR': {'Element_id': '8', 'Length': '4', 'Type': 'IP_SRC_ADDR'}, 'PKTS': {'Element_id': '2', 'Length': '8', 'Type': 'PKTS'}, 'IPv4 ID': {'Element_id': '54', 'Length': '4', 'Type': 'IPv4 ID'}, 'flowEndMilliseconds': {'Element_id': '153', 'Length': '8', 'Type': 'flowEndMilliseconds'}, 'MPLS_LABEL_1': {'Element_id': '70', 'Length': '3', 'Type': 'MPLS_LABEL_1'}, 'OUTPUT_SNMP': {'Element_id': '14', 'Length': '4', 'Type': 'OUTPUT_SNMP'}, 'IP TTL MINIMUM': {'Element_id': '52', 'Length': '1', 'Type': 'IP TTL MINIMUM'}, 'flowStartMilliseconds': {'Element_id': '152', 'Length': '8', 'Type': 'flowStartMilliseconds'}, 'IP TTL MAXIMUM': {'Element_id': '53', 'Length': '1', 'Type': 'IP TTL MAXIMUM'}, 'IP_TOS': {'Element_id': '5', 'Length': '1', 'Type': 'IP_TOS'}, 'DST_AS': {'Element_id': '17', 'Length': '4', 'Type': 'DST_AS'}, 'DIRECTION': {'Element_id': '61', 'Length': '1', 'Type': 'DIRECTION'}, 'dot1qVlanId': {'Element_id': '243', 'Length': '2', 'Type': 'dot1qVlanId'}, 'MPLS_LABEL_2': {'Element_id': '71', 'Length': '3', 'Type': 'MPLS_LABEL_2'}, 'IP_DST_ADDR': {'Element_id': '12', 'Length': '4', 'Type': 'IP_DST_ADDR'}, 'SRC_VLAN': {'Element_id': '58', 'Length': '2', 'Type': 'SRC_VLAN'}, 'L4_DST_PORT': {'Element_id': '11', 'Length': '2', 'Type': 'L4_DST_PORT'}, 'MPLS_TOP_LABEL_ADDR': {'Element_id': '47', 'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR'}, 'SRC_MASK': {'Element_id': '9', 'Length': '1', 'Type': 'SRC_MASK'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'mpls-v4'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)


    def test_get_expected_data_template_mplsv4_v9_181(self):
        format_dict = {'MPLS_LABEL_1': {'Length': '3', 'Element_id': '70', 'Type': 'MPLS_LABEL_1'}, 'FIRST_SWITCHED': {'Length': '4', 'Element_id': '22', 'Type': 'FIRST_SWITCHED'}, 'IPv4 ID': {'Length': '4', 'Element_id': '54', 'Type': 'IPv4 ID'}, 'SRC_MASK': {'Length': '1', 'Element_id': '9', 'Type': 'SRC_MASK'}, 'L4_DST_PORT': {'Length': '2', 'Element_id': '11', 'Type': 'L4_DST_PORT'}, 'IP_SRC_ADDR': {'Length': '4', 'Element_id': '8', 'Type': 'IP_SRC_ADDR'}, 'IP_NEXT_HOP': {'Length': '4', 'Element_id': '15', 'Type': 'IP_NEXT_HOP'}, 'ICMP_TYPE': {'Length': '2', 'Element_id': '32', 'Type': 'ICMP_TYPE'}, 'IP TTL MAXIMUM': {'Length': '1', 'Element_id': '53', 'Type': 'IP TTL MAXIMUM'}, 'flowEndReason': {'Length': '1', 'Element_id': '136', 'Type': 'flowEndReason'}, 'DST_AS': {'Length': '4', 'Element_id': '17', 'Type': 'DST_AS'}, 'MPLS_LABEL_3': {'Length': '3', 'Element_id': '72', 'Type': 'MPLS_LABEL_3'}, 'MPLS_TOP_LABEL_ADDR': {'Length': '4', 'Element_id': '47', 'Type': 'MPLS_TOP_LABEL_ADDR'}, 'SRC_VLAN': {'Length': '2', 'Element_id': '58', 'Type': 'SRC_VLAN'}, 'DST_MASK': {'Length': '1', 'Element_id': '13', 'Type': 'DST_MASK'}, 'TCP_FLAGS': {'Length': '1', 'Element_id': '6', 'Type': 'TCP_FLAGS'}, 'PROTOCOL': {'Length': '1', 'Element_id': '4', 'Type': 'PROTOCOL'}, 'INPUT_SNMP': {'Length': '4', 'Element_id': '10', 'Type': 'INPUT_SNMP'}, 'SRC_AS': {'Length': '4', 'Element_id': '16', 'Type': 'SRC_AS'}, 'BYTES': {'Length': '8', 'Element_id': '1', 'Type': 'BYTES'}, 'L4_SRC_PORT': {'Length': '2', 'Element_id': '7', 'Type': 'L4_SRC_PORT'}, 'IP_PROTOCOL_VERSION': {'Length': '1', 'Element_id': '60', 'Type': 'IP_PROTOCOL_VERSION'}, 'DIRECTION': {'Length': '1', 'Element_id': '61', 'Type': 'DIRECTION'}, 'OUTPUT_SNMP': {'Length': '4', 'Element_id': '14', 'Type': 'OUTPUT_SNMP'}, 'PKTS': {'Length': '8', 'Element_id': '2', 'Type': 'PKTS'}, 'IP_DST_ADDR': {'Length': '4', 'Element_id': '12', 'Type': 'IP_DST_ADDR'}, 'dot1qCustomerVlanId': {'Length': '2', 'Element_id': '245', 'Type': 'dot1qCustomerVlanId'}, 'BGP_NEXT_HOP': {'Length': '4', 'Element_id': '18', 'Type': 'BGP_NEXT_HOP'}, 'dot1qVlanId': {'Length': '2', 'Element_id': '243', 'Type': 'dot1qVlanId'}, 'MPLS_LABEL_2': {'Length': '3', 'Element_id': '71', 'Type': 'MPLS_LABEL_2'}, 'IP_TOS': {'Length': '1', 'Element_id': '5', 'Type': 'IP_TOS'}, 'LAST_SWITCHED': {'Length': '4', 'Element_id': '21', 'Type': 'LAST_SWITCHED'}, 'IP TTL MINIMUM': {'Length': '1', 'Element_id': '52', 'Type': 'IP TTL MINIMUM'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'mpls-v4'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_vpls_v9_181(self):
        format_dict = {'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'FIRST_SWITCHED': {'Length': '4', 'Element_id': '22', 'Type': 'FIRST_SWITCHED'}, 'DESTINATION_MAC': {'Type': 'DESTINATION_MAC', 'Element_id': '80', 'Length': '6'}, 'flowEndReason': {'Type': 'flowEndReason', 'Element_id': '136', 'Length': '1'}, 'LAST_SWITCHED': {'Length': '4', 'Element_id': '21', 'Type': 'LAST_SWITCHED'}, 'SRC_MAC': {'Type': 'SRC_MAC', 'Element_id': '56', 'Length': '6'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'ethernetType': {'Type': 'ethernetType', 'Element_id': '256', 'Length': '2'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'vpls'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_vpls_v10_181(self):
        format_dict = {'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'flowStartMilliseconds': {'Type': 'flowStartMilliseconds', 'Element_id': '152', 'Length': '8'}, 'DESTINATION_MAC': {'Type': 'DESTINATION_MAC', 'Element_id': '80', 'Length': '6'}, 'flowEndReason': {'Type': 'flowEndReason', 'Element_id': '136', 'Length': '1'}, 'flowEndMilliseconds': {'Type': 'flowEndMilliseconds', 'Element_id': '153', 'Length': '8'}, 'SRC_MAC': {'Type': 'SRC_MAC', 'Element_id': '56', 'Length': '6'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'ethernetType': {'Type': 'ethernetType', 'Element_id': '256', 'Length': '2'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'vpls'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_evpn_v10_181(self):
        format_dict = {'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'flowStartMilliseconds': {'Type': 'flowStartMilliseconds', 'Element_id': '152', 'Length': '8'}, 'DESTINATION_MAC': {'Type': 'DESTINATION_MAC', 'Element_id': '80', 'Length': '6'}, 'flowEndReason': {'Type': 'flowEndReason', 'Element_id': '136', 'Length': '1'}, 'flowEndMilliseconds': {'Type': 'flowEndMilliseconds', 'Element_id': '153', 'Length': '8'}, 'SRC_MAC': {'Type': 'SRC_MAC', 'Element_id': '56', 'Length': '6'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'ethernetType': {'Type': 'ethernetType', 'Element_id': '256', 'Length': '2'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'bridge'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_evpn_v9_181(self):
        format_dict = {'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'FIRST_SWITCHED': {'Length': '4', 'Element_id': '22', 'Type': 'FIRST_SWITCHED'}, 'DESTINATION_MAC': {'Type': 'DESTINATION_MAC', 'Element_id': '80', 'Length': '6'}, 'flowEndReason': {'Type': 'flowEndReason', 'Element_id': '136', 'Length': '1'}, 'LAST_SWITCHED': {'Length': '4', 'Element_id': '21', 'Type': 'LAST_SWITCHED'}, 'SRC_MAC': {'Type': 'SRC_MAC', 'Element_id': '56', 'Length': '6'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'ethernetType': {'Type': 'ethernetType', 'Element_id': '256', 'Length': '2'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'bridge'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_mplsv6_v10(self):
        format_dict = {'L4_DST_PORT': {'Length': '2', 'Element_id': '11', 'Type': 'L4_DST_PORT'}, 'L4_SRC_PORT': {'Length': '2', 'Element_id': '7', 'Type': 'L4_SRC_PORT'}, 'flowEndMilliseconds': {'Length': '8', 'Element_id': '153', 'Type': 'flowEndMilliseconds'}, 'SRC_AS': {'Length': '4', 'Element_id': '16', 'Type': 'SRC_AS'}, 'IPV6_DST_MASK': {'Length': '1', 'Element_id': '30', 'Type': 'IPV6_DST_MASK'}, 'SRC_VLAN': {'Length': '2', 'Element_id': '58', 'Type': 'SRC_VLAN'}, 'flowStartMilliseconds': {'Length': '8', 'Element_id': '152', 'Type': 'flowStartMilliseconds'}, 'IP TTL MAXIMUM': {'Length': '1', 'Element_id': '53', 'Type': 'IP TTL MAXIMUM'}, 'IPV6_DST_ADDR': {'Length': '16', 'Element_id': '28', 'Type': 'IPV6_DST_ADDR'}, 'flowEndReason': {'Length': '1', 'Element_id': '136', 'Type': 'flowEndReason'}, 'icmpTypeCodeIPv6': {'Length': '2', 'Element_id': '139', 'Type': 'icmpTypeCodeIPv6'}, 'INPUT_SNMP': {'Length': '4', 'Element_id': '10', 'Type': 'INPUT_SNMP'}, 'IPV6_SRC_ADDR': {'Length': '16', 'Element_id': '27', 'Type': 'IPV6_SRC_ADDR'}, 'OUTPUT_SNMP': {'Length': '4', 'Element_id': '14', 'Type': 'OUTPUT_SNMP'}, 'PROTOCOL': {'Length': '1', 'Element_id': '4', 'Type': 'PROTOCOL'}, 'IPV6_OPTION_HEADERS': {'Length': '4', 'Element_id': '64', 'Type': 'IPV6_OPTION_HEADERS'}, 'DST_AS': {'Length': '4', 'Element_id': '17', 'Type': 'DST_AS'}, 'dot1qVlanId': {'Length': '2', 'Element_id': '243', 'Type': 'dot1qVlanId'}, 'IPV6_NEXT_HOP': {'Length': '16', 'Element_id': '62', 'Type': 'IPV6_NEXT_HOP'}, 'IP_TOS': {'Length': '1', 'Element_id': '5', 'Type': 'IP_TOS'}, 'TCP_FLAGS': {'Length': '1', 'Element_id': '6', 'Type': 'TCP_FLAGS'}, 'DIRECTION': {'Length': '1', 'Element_id': '61', 'Type': 'DIRECTION'}, 'BYTES': {'Length': '8', 'Element_id': '1', 'Type': 'BYTES'}, 'dot1qCustomerVlanId': {'Length': '2', 'Element_id': '245', 'Type': 'dot1qCustomerVlanId'}, 'IP TTL MINIMUM': {'Length': '1', 'Element_id': '52', 'Type': 'IP TTL MINIMUM'}, 'PKTS': {'Length': '8', 'Element_id': '2', 'Type': 'PKTS'}, 'IPV6_SRC_MASK': {'Length': '1', 'Element_id': '29', 'Type': 'IPV6_SRC_MASK'}, 'IPv4 ID': {'Length': '4', 'Element_id': '54', 'Type': 'IPv4 ID'},'MPLS_LABEL_1': {'Length': '3', 'Element_id': '70', 'Type': 'MPLS_LABEL_1'},'MPLS_LABEL_2': {'Length': '3', 'Element_id': '71', 'Type': 'MPLS_LABEL_2'},'MPLS_LABEL_3': {'Length': '3', 'Element_id': '72', 'Type': 'MPLS_LABEL_3'},'MPLS_TOP_LABEL_ADDR': {'Length': '4', 'Element_id': '47', 'Type': 'MPLS_TOP_LABEL_ADDR'}}
        self.jf.jflow_template_version = '18.3'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'mpls-ipv6'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)


    def test_get_expected_data_template_mplsv6_v10_192(self):
        format_dict = {'L4_DST_PORT': {'Length': '2', 'Element_id': '11', 'Type': 'L4_DST_PORT'}, 'L4_SRC_PORT': {'Length': '2', 'Element_id': '7', 'Type': 'L4_SRC_PORT'}, 'flowEndMilliseconds': {'Length': '8', 'Element_id': '153', 'Type': 'flowEndMilliseconds'}, 'SRC_AS': {'Length': '4', 'Element_id': '16', 'Type': 'SRC_AS'}, 'IPV6_DST_MASK': {'Length': '1', 'Element_id': '30', 'Type': 'IPV6_DST_MASK'}, 'SRC_VLAN': {'Length': '2', 'Element_id': '58', 'Type': 'SRC_VLAN'}, 'flowStartMilliseconds': {'Length': '8', 'Element_id': '152', 'Type': 'flowStartMilliseconds'}, 'IP TTL MAXIMUM': {'Length': '1', 'Element_id': '53', 'Type': 'IP TTL MAXIMUM'}, 'IPV6_DST_ADDR': {'Length': '16', 'Element_id': '28', 'Type': 'IPV6_DST_ADDR'}, 'flowEndReason': {'Length': '1', 'Element_id': '136', 'Type': 'flowEndReason'}, 'icmpTypeCodeIPv6': {'Length': '2', 'Element_id': '139', 'Type': 'icmpTypeCodeIPv6'}, 'INPUT_SNMP': {'Length': '4', 'Element_id': '10', 'Type': 'INPUT_SNMP'}, 'IPV6_SRC_ADDR': {'Length': '16', 'Element_id': '27', 'Type': 'IPV6_SRC_ADDR'}, 'OUTPUT_SNMP': {'Length': '4', 'Element_id': '14', 'Type': 'OUTPUT_SNMP'}, 'PROTOCOL': {'Length': '1', 'Element_id': '4', 'Type': 'PROTOCOL'}, 'IPV6_OPTION_HEADERS': {'Length': '4', 'Element_id': '64', 'Type': 'IPV6_OPTION_HEADERS'}, 'DST_AS': {'Length': '4', 'Element_id': '17', 'Type': 'DST_AS'}, 'dot1qVlanId': {'Length': '2', 'Element_id': '243', 'Type': 'dot1qVlanId'}, 'IPV6_NEXT_HOP': {'Length': '16', 'Element_id': '62', 'Type': 'IPV6_NEXT_HOP'}, 'IP_TOS': {'Length': '1', 'Element_id': '5', 'Type': 'IP_TOS'}, 'TCP_FLAGS': {'Length': '1', 'Element_id': '6', 'Type': 'TCP_FLAGS'}, 'DIRECTION': {'Length': '1', 'Element_id': '61', 'Type': 'DIRECTION'}, 'BYTES': {'Length': '8', 'Element_id': '1', 'Type': 'BYTES'}, 'dot1qCustomerVlanId': {'Length': '2', 'Element_id': '245', 'Type': 'dot1qCustomerVlanId'}, 'IP TTL MINIMUM': {'Length': '1', 'Element_id': '52', 'Type': 'IP TTL MINIMUM'}, 'PKTS': {'Length': '8', 'Element_id': '2', 'Type': 'PKTS'}, 'IPV6_SRC_MASK': {'Length': '1', 'Element_id': '29', 'Type': 'IPV6_SRC_MASK'}, 'IPv4 ID': {'Length': '4', 'Element_id': '54', 'Type': 'IPv4 ID'},'MPLS_LABEL_1': {'Length': '3', 'Element_id': '70', 'Type': 'MPLS_LABEL_1'},'MPLS_LABEL_2': {'Length': '3', 'Element_id': '71', 'Type': 'MPLS_LABEL_2'},'MPLS_LABEL_3': {'Length': '3', 'Element_id': '72', 'Type': 'MPLS_LABEL_3'},'MPLS_TOP_LABEL_ADDR': {'Length': '4', 'Element_id': '47', 'Type': 'MPLS_TOP_LABEL_ADDR'},'BGP_IPV6_NEXT_HOP': {'Length': '16', 'Element_id': '63', 'Type': 'BGP_IPV6_NEXT_HOP'}}
        self.jf.jflow_template_version = '19.2'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'mpls-ipv6'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_data_template_mplsv6_v9(self):
        format_dict = {'L4_SRC_PORT': {'Type': 'L4_SRC_PORT', 'Element_id': '7', 'Length': '2'}, 'PROTOCOL': {'Type': 'PROTOCOL', 'Element_id': '4', 'Length': '1'}, 'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'SRC_VLAN': {'Type': 'SRC_VLAN', 'Element_id': '58', 'Length': '2'}, 'IPv4 ID': {'Type': 'IPv4 ID', 'Element_id': '54', 'Length': '4'}, 'IPV6_OPTION_HEADERS': {'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64', 'Length': '4'}, 'DIRECTION': {'Type': 'DIRECTION', 'Element_id': '61', 'Length': '1'}, 'LAST_SWITCHED': {'Type': 'LAST_SWITCHED', 'Element_id': '21', 'Length': '4'}, 'IPV6_DST_ADDR': {'Type': 'IPV6_DST_ADDR', 'Element_id': '28', 'Length': '16'}, 'dot1qCustomerVlanId': {'Type': 'dot1qCustomerVlanId', 'Element_id': '245', 'Length': '2'}, 'IPV6_SRC_ADDR': {'Type': 'IPV6_SRC_ADDR', 'Element_id': '27', 'Length': '16'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'FIRST_SWITCHED': {'Type': 'FIRST_SWITCHED', 'Element_id': '22', 'Length': '4'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}, 'IP_TOS': {'Type': 'IP_TOS', 'Element_id': '5', 'Length': '1'}, 'icmpTypeCodeIPv6': {'Type': 'icmpTypeCodeIPv6', 'Element_id': '139', 'Length': '2'}, 'DST_AS': {'Type': 'DST_AS', 'Element_id': '17', 'Length': '4'}, 'dot1qVlanId': {'Type': 'dot1qVlanId', 'Element_id': '243', 'Length': '2'}, 'L4_DST_PORT': {'Type': 'L4_DST_PORT', 'Element_id': '11', 'Length': '2'}, 'IPV6_DST_MASK': {'Type': 'IPV6_DST_MASK', 'Element_id': '30', 'Length': '1'}, 'flowEndReason': {'Type': 'flowEndReason', 'Element_id': '136', 'Length': '1'}, 'IPV6_NEXT_HOP': {'Type': 'IPV6_NEXT_HOP', 'Element_id': '62', 'Length': '16'}, 'TCP_FLAGS': {'Type': 'TCP_FLAGS', 'Element_id': '6', 'Length': '1'}, 'SRC_AS': {'Type': 'SRC_AS', 'Element_id': '16', 'Length': '4'}, 'IP TTL MINIMUM': {'Type': 'IP TTL MINIMUM', 'Element_id': '52', 'Length': '1'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}, 'IP TTL MAXIMUM': {'Type': 'IP TTL MAXIMUM', 'Element_id': '53', 'Length': '1'}, 'IPV6_SRC_MASK': {'Type': 'IPV6_SRC_MASK', 'Element_id': '29', 'Length': '1'},'MPLS_LABEL_1': {'Length': '3', 'Element_id': '70', 'Type': 'MPLS_LABEL_1'},'MPLS_LABEL_2': {'Length': '3', 'Element_id': '71', 'Type': 'MPLS_LABEL_2'},'MPLS_LABEL_3': {'Length': '3', 'Element_id': '72', 'Type': 'MPLS_LABEL_3'},'MPLS_TOP_LABEL_ADDR': {'Length': '4', 'Element_id': '47', 'Type': 'MPLS_TOP_LABEL_ADDR'}}
        self.jf.jflow_template_version = '18.3'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'mpls-ipv6'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)


    def test_get_expected_data_template_mplsv6_v9_192(self):
        format_dict = {'L4_SRC_PORT': {'Type': 'L4_SRC_PORT', 'Element_id': '7', 'Length': '2'}, 'PROTOCOL': {'Type': 'PROTOCOL', 'Element_id': '4', 'Length': '1'}, 'BYTES': {'Type': 'BYTES', 'Element_id': '1', 'Length': '8'}, 'SRC_VLAN': {'Type': 'SRC_VLAN', 'Element_id': '58', 'Length': '2'}, 'IPv4 ID': {'Type': 'IPv4 ID', 'Element_id': '54', 'Length': '4'}, 'IPV6_OPTION_HEADERS': {'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64', 'Length': '4'}, 'DIRECTION': {'Type': 'DIRECTION', 'Element_id': '61', 'Length': '1'}, 'LAST_SWITCHED': {'Type': 'LAST_SWITCHED', 'Element_id': '21', 'Length': '4'}, 'IPV6_DST_ADDR': {'Type': 'IPV6_DST_ADDR', 'Element_id': '28', 'Length': '16'}, 'dot1qCustomerVlanId': {'Type': 'dot1qCustomerVlanId', 'Element_id': '245', 'Length': '2'}, 'IPV6_SRC_ADDR': {'Type': 'IPV6_SRC_ADDR', 'Element_id': '27', 'Length': '16'}, 'OUTPUT_SNMP': {'Type': 'OUTPUT_SNMP', 'Element_id': '14', 'Length': '4'}, 'FIRST_SWITCHED': {'Type': 'FIRST_SWITCHED', 'Element_id': '22', 'Length': '4'}, 'PKTS': {'Type': 'PKTS', 'Element_id': '2', 'Length': '8'}, 'IP_TOS': {'Type': 'IP_TOS', 'Element_id': '5', 'Length': '1'}, 'icmpTypeCodeIPv6': {'Type': 'icmpTypeCodeIPv6', 'Element_id': '139', 'Length': '2'}, 'DST_AS': {'Type': 'DST_AS', 'Element_id': '17', 'Length': '4'}, 'dot1qVlanId': {'Type': 'dot1qVlanId', 'Element_id': '243', 'Length': '2'}, 'L4_DST_PORT': {'Type': 'L4_DST_PORT', 'Element_id': '11', 'Length': '2'}, 'IPV6_DST_MASK': {'Type': 'IPV6_DST_MASK', 'Element_id': '30', 'Length': '1'}, 'flowEndReason': {'Type': 'flowEndReason', 'Element_id': '136', 'Length': '1'}, 'IPV6_NEXT_HOP': {'Type': 'IPV6_NEXT_HOP', 'Element_id': '62', 'Length': '16'}, 'TCP_FLAGS': {'Type': 'TCP_FLAGS', 'Element_id': '6', 'Length': '1'}, 'SRC_AS': {'Type': 'SRC_AS', 'Element_id': '16', 'Length': '4'}, 'IP TTL MINIMUM': {'Type': 'IP TTL MINIMUM', 'Element_id': '52', 'Length': '1'}, 'INPUT_SNMP': {'Type': 'INPUT_SNMP', 'Element_id': '10', 'Length': '4'}, 'IP TTL MAXIMUM': {'Type': 'IP TTL MAXIMUM', 'Element_id': '53', 'Length': '1'}, 'IPV6_SRC_MASK': {'Type': 'IPV6_SRC_MASK', 'Element_id': '29', 'Length': '1'},'MPLS_LABEL_1': {'Length': '3', 'Element_id': '70', 'Type': 'MPLS_LABEL_1'},'MPLS_LABEL_2': {'Length': '3', 'Element_id': '71', 'Type': 'MPLS_LABEL_2'},'MPLS_LABEL_3': {'Length': '3', 'Element_id': '72', 'Type': 'MPLS_LABEL_3'},'MPLS_TOP_LABEL_ADDR': {'Length': '4', 'Element_id': '47', 'Type': 'MPLS_TOP_LABEL_ADDR'},'BGP_IPV6_NEXT_HOP': {'Length': '16', 'Element_id': '63', 'Type': 'BGP_IPV6_NEXT_HOP'}}
        self.jf.jflow_template_version = '19.2'
        self.jf.cflow_version = '9'
        self.jf.template_type = 'mpls-ipv6'
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)


    def test_get_expected_option_template_v10_181(self):
        format_dict = {'FLOW_EXPORTER': {'Type': 'FLOW_EXPORTER', 'Element_id': '144', 'Length': '4'}, 'collectorTransportProtocol': {'Type': 'collectorTransportProtocol', 'Element_id': '215', 'Length': '1'}, 'collectorProtocolVersion': {'Type': 'collectorProtocolVersion', 'Element_id': '214', 'Length': '1'}, 'exporterIPv6Address': {'Type': 'exporterIPv6Address', 'Element_id': '131', 'Length': '16'}, 'systemInitTimeMilliseconds': {'Type': 'systemInitTimeMilliseconds', 'Element_id': '160', 'Length': '8'}, 'FLOW_INACTIVE_TIMEOUT': {'Type': 'FLOW_INACTIVE_TIMEOUT', 'Element_id': '37', 'Length': '2'}, 'FLOW_ACTIVE_TIMEOUT': {'Type': 'FLOW_ACTIVE_TIMEOUT', 'Element_id': '36', 'Length': '2'}, 'TOTAL_FLOWS_EXP': {'Type': 'TOTAL_FLOWS_EXP', 'Element_id': '42', 'Length': '8'}, 'exporterIPv4Address': {'Type': 'exporterIPv4Address', 'Element_id': '130', 'Length': '4'}, 'SAMPLING_INTERVAL': {'Type': 'SAMPLING_INTERVAL', 'Element_id': '34', 'Length': '4'}, 'TOTAL_PKTS_EXP': {'Type': 'TOTAL_PKTS_EXP', 'Element_id': '41', 'Length': '8'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '10'
        self.assertEqual(self.jf.get_expected_option_template(), format_dict)


    def test_get_expected_option_template_v9_181(self):
        format_dict = {'FLOW_INACTIVE_TIMEOUT': {'Element_id': '37', 'Length': '2', 'Type': 'FLOW_INACTIVE_TIMEOUT'}, 'TOTAL_FLOWS_EXP': {'Element_id': '42', 'Length': '8', 'Type': 'TOTAL_FLOWS_EXP'}, 'SAMPLING_INTERVAL': {'Element_id': '34', 'Length': '4', 'Type': 'SAMPLING_INTERVAL'}, 'FLOW_ACTIVE_TIMEOUT': {'Element_id': '36', 'Length': '2', 'Type': 'FLOW_ACTIVE_TIMEOUT'}, 'TOTAL_PKTS_EXP': {'Element_id': '41', 'Length': '8', 'Type': 'TOTAL_PKTS_EXP'}, 'System': {'Element_id': '1', 'Length': '0', 'Type': 'System'}}
        self.jf.jflow_template_version = '18.1'
        self.jf.cflow_version = '9'
        self.assertEqual(self.jf.get_expected_option_template(), format_dict)


    def test_verify_template_record_both_True(self):
        self.jf.verify_mx_template_inline = MagicMock()
        self.jf.verify_mx_template_inline.return_value = True
        self.assertEqual(self.jf.verify_template_record(), True)

    def test_verify_template_record_one_True_one_False_part1(self):
        self.jf.verify_mx_template_inline = MagicMock(side_effect=[True, False])
        self.assertEqual(self.jf.verify_template_record(), False)

    def test_verify_template_record_one_True_one_False_part2(self):
        self.jf.verify_mx_template_inline = MagicMock(side_effect=[False, True])
        self.assertEqual(self.jf.verify_template_record(), False)

    def test_verify_template_record_data_template(self):
        self.jf.verify_mx_template_inline = MagicMock()
        self.jf.verify_mx_template_inline.return_value = True
        self.assertEqual(self.jf.verify_template_record(template_to_verify = 'DATA TEMPLATE'), True)

    def test_verify_template_record_option_template(self):
        self.jf.verify_mx_template_inline = MagicMock()
        self.jf.verify_mx_template_inline.return_value = True
        self.assertEqual(self.jf.verify_template_record(template_to_verify = 'OPTION TEMPLATE'), True)

    def test_verify_option_data_record(self):
        self.jf.verify_mx_option_data_inline = MagicMock()
        self.jf.verify_mx_option_data_inline.return_value = True
        self.assertEqual(self.jf.verify_option_data_record(), True)

    def test_verify_data_record(self):
        self.jf.verify_mx_data_record_inline = MagicMock()
        self.jf.verify_mx_data_record_inline.return_value = True
        self.assertEqual(self.jf.verify_data_record(), True)

    def test_verify_l2_data_record(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'262': {'DATA': {'00:00:00:00:02:11': {'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (262)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'Destination Mac Address': '00:00:00:00:02:11',
                                                                                                                    'Flow End Reason': 'Active timeout (2)',
                                                                                                                    'InputInt': '603',
                                                                                                                    'Octets': '307200',
                                                                                                                    'OutputInt': '600',
                                                                                                                    'Packets': '1200',
                                                                                                                    'Source Mac Address': '00:00:00:00:01:11',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        dst_mac_address = ['00:00:00:00:02:11']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'Destination Mac Address': dst_mac_address}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'bridge', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '15.1'
        self.jf.data_templ_id = '262'
        self.jf.expected_data_pkt_flowset_name = '(Data) (262)'
        expected_pdu_dict = {'Source Mac Address': '00:00:00:00:01:11', 'Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '600', 'InputInt': '603'}
        self.assertEqual(self.jf._verify_mx_l2_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), True)

    def test_verify_mx_data_record(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'70.0.0.1': {'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0x00',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'DstAddr': '80.0.0.4', 'Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','Vlan Id': '0','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), True)

    def test_verify_mx_data_record_dstaddr(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'80.0.0.4':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0x00',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        DstAddr = ['80.0.0.4']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'DstAddr': DstAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','Vlan Id': '0','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), True)



    def test_verify_mx_data_record_vlan(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'0':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0x00',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        Vlan_Id = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'Vlan Id': Vlan_Id}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'DstAddr':'80.0.0.4','Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), True)

    def test_verify_mx_data_record_vlan2(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'0':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0x00',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        Vlan_Id = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'Dot1q Vlan Id': Vlan_Id}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'DstAddr':'80.0.0.4','Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2','Vlan Id': '0'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), True)


    def test_verify_mx_data_record_vlan3(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'0':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        Vlan_Id = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'Dot1q Customer Vlan Id': Vlan_Id}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'DstAddr':'80.0.0.4','Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2','Vlan Id': '0'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), True)





    def test_verify_mx_data_record_tos(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'0':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        tos = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'IP ToS': tos}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'DstAddr':'80.0.0.4','Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2','Vlan Id': '0'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), True)



    def test_verify_mx_data_record_frag(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'0':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        frag = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'IPv4Ident': frag}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'DstAddr':'80.0.0.4','Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2','Vlan Id': '0'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), True)



    def test_verify_mx_data_record_all(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'0':{'0':{'0':{'0':{'0':{'0':{'0':{'0':{'0':{'40.0.0.2':{'30.0.0.2':{'2':{'1':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '0',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '0',
                                                                                     'DstPort': '0',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': '2',
                                                                                     'IP ToS': '0',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '0',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '0',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Direction': '1',
                                                                                     'Protocol': '0',
                                                                                     'SrcAS': '0',
                                                                                     'SrcMask': '0',
                                                                                     'SrcPort': '0',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '0'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}}}}}}}}}}}}}
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{'Type': ['0']},{'TCP Flags': ['0']}, {'SrcMask': ['0']},{'DstMask': ['0']}, {'InputInt': ['0']},{'OutputInt':['0']}, {'SrcPort':['0']}, {'DstPort':['0']}, {'Protocol':['0']}, {'BGPNextHop':['40.0.0.2']}, {'NextHop':['30.0.0.2']}, {'Flow End Reason': ['2']}, {'Direction': ['1']}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'DstAddr':'80.0.0.4','SrcAS': '0','DstAS': '0','NextHop': '30.0.0.2','BGPNextHop': '40.0.0.2','Vlan Id': '0','SrcMask':'0','DstMask': '0'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), True)


    def test_verify_mx_data_record_dst_fail(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'70.0.0.1': {'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0x00',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','Vlan Id': '0','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), False)


    def test_verify_mx_data_record_src_fail(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'80.0.0.4':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0x00',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        DstAddr = ['80.0.0.4']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'DstAddr': DstAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','Vlan Id': '0','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), False)



    def test_verify_mx_data_record_srcport_fail(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'80.0.0.4':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0x00',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        DstAddr = ['80.0.0.4']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'DstAddr': DstAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','Vlan Id': '0','DstPort': '1001','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), False)


    def test_verify_mx_data_record_dstport_fail(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'256': {'DATA': {'80.0.0.4':{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (256)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '300',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'DstMask': '32',
                                                                                     'DstPort': '1001',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Flow End Reason': 'Active '
                                                                                                        'timeout '
                                                                                                        '(2)',
                                                                                     'IP ToS': '0x00',
                                                                                     'IPv4Ident': '0',
                                                                                     'InputInt': '543',
                                                                                     'MaxTTL': '64',
                                                                                     'MinTTL': '64',
                                                                                     'NextHop': '30.0.0.2',
                                                                                     'Octets': '3673936',
                                                                                     'OutputInt': '545',
                                                                                     'BGPNextHop': '40.0.0.2',
                                                                                     'Packets': '32803',
                                                                                     'Protocol': '17',
                                                                                     'SrcAS': '200',
                                                                                     'SrcMask': '32',
                                                                                     'SrcPort': '12000',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'TCP Flags': '0x00',
                                                                                     'Vlan Id': '0',
                                                                                                                    'Type': '2048'},
                                                                                                            }
                                                                                                }
                                                                                                }}}}}}
        DstAddr = ['80.0.0.4']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'DstAddr': DstAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipv4', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '18.1'
        self.jf.data_templ_id = '256'
        self.jf.expected_data_pkt_flowset_name = '(Data) (256)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','Vlan Id': '0','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), False)


if __name__ == '__main__':
    unittest.main()
