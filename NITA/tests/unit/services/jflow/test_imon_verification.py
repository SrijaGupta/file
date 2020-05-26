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
from jnpr.toby.services.jflow.imon_verification import imon_verification
import builtins
builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'


class Test_imon_verification(unittest.TestCase):

    def setUp(self):
        self.jf = imon_verification()
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
        self.jf.get_mx_template_details.return_value = {'templ_id' : '384'}
        self.assertEqual(self.jf.get_expected_template_details(),{'templ_id' : '384'})

    def test_get_mx_template_details_ipv4_v10(self):
        format_dict = {'data_templ_id': '384', 'expected_option_template_pkt_flowset_name': 'Options Template (V10 [IPFIX]) (3)', 'expected_data_pkt_flowset_name': '(Data) (384)', 'expected_data_template_pkt_flowset_name': 'Data Template (V10 [IPFIX]) (2)', 'option_templ_id': '640', 'expected_option_pkt_flowset_name': '(Data) (640)'}
        self.jf.template_type = 'ipvx'
        self.jf.cflow_version = '10'
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
        response_path.response.return_value = "Internal Modified MX IMON Template Version: 19.3"
        self.assertEqual(self.jf.get_jflow_template_version(), '19.3')

    def test_get_expected_data_template_ipv4_v10_193(self):
        self.jf.jflow_template_version = '19.3'
        self.jf.cflow_version = '10'
        self.jf.template_type = 'ipvx'
        format_dict = {'dataLinkFrameSize': {'Element_id': '312', 'Type': 'dataLinkFrameSize', 'Length': '2'}, 'OUTPUT_SNMP': {'Element_id': '14', 'Type': 'OUTPUT_SNMP', 'Length': '4'}, 'INPUT_SNMP': {'Element_id': '10', 'Type': 'INPUT_SNMP', 'Length': '4'}, 'DIRECTION': {'Element_id': '61', 'Type': 'DIRECTION', 'Length': '1'}, 'dataLinkFrameSection': {'Element_id': '315', 'Type': 'dataLinkFrameSection', 'Length': '65535'}}
        self.assertEqual(self.jf.get_expected_data_template(), format_dict)

    def test_get_expected_option_template_v10_193(self):
        format_dict = {'SAMPLING_INTERVAL': {'Type': 'SAMPLING_INTERVAL', 'Element_id': '34', 'Length': '4'}, 'FLOW_EXPORTER': {'Type': 'FLOW_EXPORTER', 'Element_id': '144', 'Length': '4'}}
        self.jf.jflow_template_version = '19.3'
        self.jf.cflow_version = '10'
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

    def test_verify_option_data_record_false(self):
        self.jf.verify_mx_option_data_inline = MagicMock()
        self.jf.verify_mx_option_data_inline.return_value = False
        self.assertEqual(self.jf.verify_option_data_record(), False)

    def test_verify_data_record(self):
        self.jf.verify_mx_data_record_inline = MagicMock()
        self.jf.verify_mx_data_record_inline.return_value = True
        self.assertEqual(self.jf.verify_data_record(), True)

    def test_verify_data_record_false(self):
        self.jf.verify_mx_data_record_inline = MagicMock()
        self.jf.verify_mx_data_record_inline.return_value = False
        self.assertEqual(self.jf.verify_data_record(), False)


    def test_verify_mx_data_record(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'70.0.0.1': [{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}
        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
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
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'80.0.0.4':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}
        DstAddr = ['80.0.0.4']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'DstAddr': DstAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
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
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'0':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}
        Vlan_Id = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'Vlan Id': Vlan_Id}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
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
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'0':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}
        Vlan_Id = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'Dot1q Vlan Id': Vlan_Id}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
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
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'0':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}
        Vlan_Id = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'Dot1q Customer Vlan Id': Vlan_Id}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
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
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'0':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}
        tos = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'IP ToS': tos}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
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
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'0':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}
        frag = ['0']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'IPv4Ident': frag}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
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
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'0':{'0':{'0':{'0':{'0':{'0':{'0':{'0':{'0':{'40.0.0.2':{'30.0.0.2':{'2':{'1':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}}}}}}}}}}}}}
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{'Type': ['0']},{'TCP Flags': ['0']}, {'SrcMask': ['0']},{'DstMask': ['0']}, {'InputInt': ['0']},{'OutputInt':['0']}, {'SrcPort':['0']}, {'DstPort':['0']}, {'Protocol':['0']}, {'BGPNextHop':['40.0.0.2']}, {'NextHop':['30.0.0.2']}, {'Flow End Reason': ['2']}, {'Direction': ['1']}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'mpls', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
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
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'70.0.0.1':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}
        SrcAddr = ['70.0.0.1']
        src_ip_list = self.jf.get_ip_sequence_in_list(initial_ip = '70.0.0.1')
        number_list = self.jf.get_port_list(initial_port_number = '12000', count=1)
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
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
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'80.0.0.4':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
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
                                                                                                }]
                                                                                                }}}}}}
        DstAddr = ['80.0.0.4']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'DstAddr': DstAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
        expected_pdu_dict = {'Type': '2048', 'Flow End Reason': 'Active timeout (2)', 'OutputInt': '545', 'InputInt': '543','SrcAS': '200','DstAS': '300','NextHop': '30.0.0.2','Vlan Id': '0','DstPort': '1001','SrcPort': '12000','SrcMask': '32','DstMask': '32','BGPNextHop': '40.0.0.2'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), False)

    def test_verify_mx_data_record_all_1(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384': {'DATA': {'0':{'0':{'0':{'0':{'0':{'0':{'0':{'0':{'0':{'40.0.0.2':{'30.0.0.2':{'2':{'1':[{'FlowSequence': '98',
                                                                                                'Length': '185',
                                                                                                'Observation Domain Id': '786688',
                                                                                                'Version': '10',
                                                                                                'flowset': {'FlowSet Id': '(Data) (384)',
                                                                                                            'FlowSet Length': '169',
                                                                                                            'field': [],
                                                                                                            'num_field': 0,
                                                                                                            'num_pdu': 3,
                                                                                                            'pdu': {'SrcAddr': '70.0.0.1',
                                                                                     'Dot1q Customer Vlan Id': '0',
                                                                                     'Dot1q Vlan Id': '0',
                                                                                     'DstAS': '0',
                                                                                     'DstAddr': '80.0.0.4',
                                                                                     'Inner SrcPort': '0',
                                                                                     'DstPort': '0',
                                                                                     'EndTime': '157094.976000000 '
                                                                                                'seconds',
                                                                                     'Inner SrcAddr': '2',
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
                                                                                     'Inner DstAddr': '0',
                                                                                     'Inner DstPort': '0',
                                                                                     'StartTime': '156974.912000000 '
                                                                                                  'seconds',
                                                                                     'IPv6 ICMP Code': '0',
                                                                                     'Vlan Id': '0',
                                                                                                                    'IPv6 Extension Headers': '0'},
                                                                                                            }
                                                                                                }]
                                                                                                }}}}}}}}}}}}}}}}}}
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{'IPv6 Extension Headers': ['0']},{'IPv6 ICMP Code': ['0']}, {'Inner DstAddr': ['0']},{'Inner SrcPort': ['0']}, {'InputInt': ['0']},{'OutputInt':['0']}, {'Inner DstPort':['0']}, {'DstPort':['0']}, {'Protocol':['0']}, {'BGPNextHop':['40.0.0.2']}, {'NextHop':['30.0.0.2']}, {'Inner SrcAddr': ['2']}, {'Direction': ['1']}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'mpls', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
        expected_pdu_dict = {'SrcAddr': '70.0.0.1', 'DstAddr':'80.0.0.4','SrcAS': '0','DstAS': '0','NextHop': '30.0.0.2','BGPNextHop': '40.0.0.2','Vlan Id': '0','SrcMask':'0','DstMask': '0'}
        self.assertEqual(self.jf.verify_mx_data_record_inline(expected_pdu_dict=expected_pdu_dict, sampling_obs_dmn_ids='786688'), False)



    def test_verify_mx_template_record_inline_1(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384':{'TEMPLATE': [{'ExportTime': '1564987184',
                                                            'FlowSequence': '0',
                                                            'Length': '140',
                                                            'Observation Domain Id': '786688',
                                                            'Timestamp': 'Aug  '
                                                                         '5, '
                                                                         '2019 '
                                                                         '12:09:44.000000000 '
                                                                         'IST',
                                                            'Version': '10',
                                                            '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                               'flow '
                                                                                               'sequence '
                                                                                               'for '
                                                                                               'domain '
                                                                                               'ID '
                                                                                               '590338 '
                                                                                               '(expected '
                                                                                               '27, '
                                                                                               'got '
                                                                                               '209)]',
                                                            '[Group': 'Sequence]',
                                                            '[Severity level': 'Warning]',
                                                            'flowset': {'Field Count': '29',
                                                                        'FlowSet Id': 'Data '
                                                                                      'Template '
                                                                                      '(V10 '
                                                                                      '[IPFIX]) '
                                                                                      '(2)',
                                                                        'FlowSet Length': '124',
                                                                        'Template Id': '39416',
                                                                        'field': [{'Length': '4',
                                                                                   'Type': 'IP_SRC_ADDR '
                                                                                           '(8)'},
                                                                                  {'Length': '4',
                                                                                   'Type': 'IP_DST_ADDR '
                                                                                           '(12)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'IP_TOS '
                                                                                           '(5)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'PROTOCOL '
                                                                                           '(4)'},
                                                                                  {'Length': '2',
                                                                                   'Type': 'L4_SRC_PORT '
                                                                                           '(7)'},
                                                                                  {'Length': '2',
                                                                                   'Type': 'L4_DST_PORT '
                                                                                           '(11)'},
                                                                                  {'Length': '2',
                                                                                   'Type': 'ICMP_TYPE '
                                                                                           '(32)'},
                                                                                  {'Length': '4',
                                                                                   'Type': 'INPUT_SNMP '
                                                                                           '(10)'},
                                                                                  {'Length': '2',
                                                                                   'Type': 'SRC_VLAN '
                                                                                           '(58)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'SRC_MASK '
                                                                                           '(9)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'DST_MASK '
                                                                                           '(13)'},
                                                                                  {'Length': '4',
                                                                                   'Type': 'SRC_AS '
                                                                                           '(16)'},
                                                                                  {'Length': '4',
                                                                                   'Type': 'DST_AS '
                                                                                           '(17)'},
                                                                                  {'Length': '4',
                                                                                   'Type': 'IP_NEXT_HOP '
                                                                                           '(15)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'TCP_FLAGS '
                                                                                           '(6)'},
                                                                                  {'Length': '4',
                                                                                   'Type': 'OUTPUT_SNMP '
                                                                                           '(14)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'IP '
                                                                                           'TTL '
                                                                                           'MINIMUM '
                                                                                           '(52)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'IP '
                                                                                           'TTL '
                                                                                           'MAXIMUM '
                                                                                           '(53)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'flowEndReason '
                                                                                           '(136)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'IP_PROTOCOL_VERSION '
                                                                                           '(60)'},
                                                                                  {'Length': '4',
                                                                                   'Type': 'BGP_NEXT_HOP '
                                                                                           '(18)'},
                                                                                  {'Length': '1',
                                                                                   'Type': 'DIRECTION '
                                                                                           '(61)'},
                                                                                  {'Length': '2',
                                                                                   'Type': 'dot1qVlanId '
                                                                                           '(243)'},
                                                                                  {'Length': '2',
                                                                                   'Type': 'dot1qCustomerVlanId '
                                                                                           '(245)'},
                                                                                  {'Length': '4',
                                                                                   'Type': 'IPv4 '
                                                                                           'ID '
                                                                                           '(54)'},
                                                                                  {'Length': '8',
                                                                                   'Type': 'BYTES '
                                                                                           '(1)'},
                                                                                  {'Length': '8',
                                                                                   'Type': 'PKTS '
                                                                                           '(2)'},
                                                                                  {'Length': '8',
                                                                                   'Type': 'flowStartMilliseconds '
                                                                                           '(152)'},
                                                                                  {'Length': '8',
                                                                                   'Type': 'flowEndMilliseconds '
                                                                                           '(153)'}],
                                                                        'num_field': 29,
                                                                        'num_pdu': 0,
                                                                        'pdu': []},
                                                            'frame_index': 10,
                                                            'ip': {'dst_ip': '1000::2',
                                                                   'src_ip': '1000::1'},
                                                            'udp': {}}]
                                                                                                }}}}}
        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
        self.jf.obs_dmn_ids = '786688'
        self.jf.flow_colls = ['5000::2']
        self.jf.data_template_dict = {'dataLinkFrameSize': {'Element_id': '312', 'Type': 'dataLinkFrameSize', 'Length': '2'}, 'OUTPUT_SNMP': {'Element_id': '14', 'Type': 'OUTPUT_SNMP', 'Length': '4'}, 'INPUT_SNMP': {'Element_id': '10', 'Type': 'INPUT_SNMP', 'Length': '4'}, 'DIRECTION': {'Element_id': '61', 'Type': 'DIRECTION', 'Length': '1'}, 'dataLinkFrameSection': {'Element_id': '315', 'Type': 'dataLinkFrameSection', 'Length': '65535'}}
        self.assertEqual(self.jf.verify_mx_template_inline(template_to_verify='DATA TEMPLATE'), False)


    def test_verify_mx_template_record_inline_2(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'384':{'TEMPLATE': [{'ExportTime': '1564987184',
                                                            'FlowSequence': '0',
                                                            'Length': '140',
                                                            'Observation Domain Id': '786688',
                                                            'Timestamp': 'Aug  '
                                                                         '5, '
                                                                         '2019 '
                                                                         '12:09:44.000000000 '
                                                                         'IST',
                                                            'Version': '10',
                                                            '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                               'flow '
                                                                                               'sequence '
                                                                                               'for '
                                                                                               'domain '
                                                                                               'ID '
                                                                                               '590338 '
                                                                                               '(expected '
                                                                                               '27, '
                                                                                               'got '
                                                                                               '209)]',
                                                            '[Group': 'Sequence]',
                                                            '[Severity level': 'Warning]',
                                                            'flowset': {'Field Count': '29',
                                                                        'FlowSet Id': 'Data '
                                                                                      'Template '
                                                                                      '(V10 '
                                                                                      '[IPFIX]) '
                                                                                      '(2)',
                                                                        'FlowSet Length': '124',
                                                                        'Template Id': '384',
                                                                        'field': [{'Length': '4',
                                                                                'Type': 'INPUT_SNMP '
                                                                                        '(10)'},
                                                                               {'Length': '4',
                                                                                'Type': 'OUTPUT_SNMP '
                                                                                        '(14)'},
                                                                               {'Length': '1',
                                                                                'Type': 'DIRECTION '
                                                                                        '(61)'},
                                                                               {'Length': '2',
                                                                                'Type': 'dataLinkFrameSize '
                                                                                        '(312)'},
                                                                               {'Length': '65535 '
                                                                                          '[i.e.: '
                                                                                          '"Variable '
                                                                                          'Length"]',
                                                                                'Type': 'dataLinkFrameSection '
                                                                                        '(315)'}],
                                                                        'num_field': 29,
                                                                        'num_pdu': 0,
                                                                        'pdu': []},
                                                            'frame_index': 10,
                                                            'ip': {'dst_ip': '1000::2',
                                                                   'src_ip': '1000::1'},
                                                            'udp': {}}]
                                                                                                }}}}}
        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.data_templ_id = '384'
        self.jf.expected_data_pkt_flowset_name = '(Data) (384)'
        self.jf.obs_dmn_ids = ['786688']
        self.jf.flow_colls = ['5000::2']
        self.jf.data_template_dict = {'dataLinkFrameSize': {'Element_id': '312', 'Type': 'dataLinkFrameSize', 'Length': '2'}, 'OUTPUT_SNMP': {'Element_id': '14', 'Type': 'OUTPUT_SNMP', 'Length': '4'}, 'INPUT_SNMP': {'Element_id': '10', 'Type': 'INPUT_SNMP', 'Length': '4'}, 'DIRECTION': {'Element_id': '61', 'Type': 'DIRECTION', 'Length': '1'}, 'dataLinkFrameSection': {'Element_id': '315', 'Type': 'dataLinkFrameSection', 'Length': '65535'}}
        self.assertEqual(self.jf.verify_mx_template_inline(template_to_verify='DATA TEMPLATE'), True)


    def test_verify_mx_template_record_inline_3(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'640':{'OPTIONS_IPFIX_INLINE': [{'ExportTime': '1564655641',
                                                                     'FlowSequence': '14 '
                                                                                     '(expected '
                                                                                     '0)',
                                                                     'Length': '36',
                                                                     'Observation Domain Id': '786688',
                                                                     'Timestamp': 'Aug  '
                                                                                  '1, '
                                                                                  '2019 '
                                                                                  '03:34:01.000000000 '
                                                                                  'PDT',
                                                                     'Version': '10',
                                                                     '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                        'flow '
                                                                                                        'sequence '
                                                                                                        'for '
                                                                                                        'domain '
                                                                                                        'ID '
                                                                                                        '65536 '
                                                                                                        '(expected '
                                                                                                        '0, '
                                                                                                        'got '
                                                                                                        '14)]',
                                                                     '[Group': 'Sequence]',
                                                                     '[Severity level': 'Warning]',
                                                                     'flowset': {'FlowSet Id': 'Options '
                                                                                               'Template '
                                                                                               '(V10 '
                                                                                               '[IPFIX]) '
                                                                                               '(3)',
                                                                                 'FlowSet Length': '20',
                                                                                 'Scope Field Count': '1',
                                                                                 'Template Id': '640',
                                                                                 'Total Field Count': '2',
                                                                                 'field': [{'Length': '4',
                                                                                            'Type': 'FLOW_EXPORTER '
                                                                                                    '(144)'},
                                                                                           {'Length': '4',
                                                                                            'Padding': '0000',
                                                                                            'Type': 'SAMPLING_INTERVAL '
                                                                                                    '(34)',
                                                                                            '[Expected Sequence Number': '0]',
                                                                                            '[Previous Frame in Sequence': '10]'}],
                                                                                 'num_field': 2,
                                                                                 'num_pdu': 0,
                                                                                 'opt_type': 'SYSTEM',
                                                                                 'pdu': [],
                                                                                 'type': 'OPTIONS_IPFIX_INLINE'},
                                                                     'frame_index': 12,
                                                                     'ip': {'dst_ip': '50.1.1.11',
                                                                            'src_ip': '50.1.1.1'},
                                                                     'udp': {}}]
                                                                                                }}}}}
        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.jflow_template_version = '19.3'
        self.jf.option_templ_id = '640'
        self.jf.expected_data_pkt_flowset_name = '(Data) (640)'
        self.jf.obs_dmn_ids = ['786688']
        self.jf.flow_colls = ['5000::2']
        self.jf.option_template_dict = {'SAMPLING_INTERVAL': {'Type': 'SAMPLING_INTERVAL', 'Element_id': '34', 'Length': '4'}, 'FLOW_EXPORTER': {'Type': 'FLOW_EXPORTER', 'Element_id': '144', 'Length': '4'}}
        self.assertEqual(self.jf.verify_mx_template_inline(template_to_verify='OPTION TEMPLATE'), True)


    def test_verify_mx_option_data_record_1(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'640': {'OPTIONS_DATA':[{'ExportTime': '1564655641',
                                                                  'FlowSequence': '14',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:34:01.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '14)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 13,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}},
                                                                 {'ExportTime': '1564655671',
                                                                  'FlowSequence': '15',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:34:31.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '15)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 28,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}},
                                                                 {'ExportTime': '1564655701',
                                                                  'FlowSequence': '16',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:35:01.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '16)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 43,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}}]
                                                                                                }}}}}

        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.sampling_obs_dmn_ids = ['786688']
        self.jf.flow_colls = ['5000::2']
        self.jf.jflow_template_version = '19.3'
        self.jf.option_templ_id = '640'
        self.jf.exp_optionpkt_flowset = '(Data) (640)'
        expected_option_data_pdu_dict = {'Sampling interval': '1'}
        self.assertEqual(self.jf.verify_mx_option_data_inline(expected_option_data_pdu_dict=expected_option_data_pdu_dict), True)



    def test_verify_mx_option_data_record_2(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'78668': {'640': {'OPTIONS_DATA':[{'ExportTime': '1564655641',
                                                                  'FlowSequence': '14',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:34:01.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '14)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 13,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}},
                                                                 {'ExportTime': '1564655671',
                                                                  'FlowSequence': '15',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:34:31.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '15)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 28,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}},
                                                                 {'ExportTime': '1564655701',
                                                                  'FlowSequence': '16',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '78668',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:35:01.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '16)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 43,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}}]
                                                                                                }}}}}

        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.sampling_obs_dmn_ids = ['786688']
        self.jf.flow_colls = ['5000::2']
        self.jf.jflow_template_version = '19.3'
        self.jf.option_templ_id = '640'
        self.jf.exp_optionpkt_flowset = '(Data) (640)'
        expected_option_data_pdu_dict = {'Sampling interval': '1'}
        self.assertEqual(self.jf.verify_mx_option_data_inline(expected_option_data_pdu_dict=expected_option_data_pdu_dict), False)



    def test_verify_mx_option_data_record_3(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'78668': {'640': {'OPTIONS_DATA':[{'ExportTime': '1564655641',
                                                                  'FlowSequence': '14',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:34:01.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '14)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 13,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}},
                                                                 {'ExportTime': '1564655671',
                                                                  'FlowSequence': '15',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:34:31.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '15)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 28,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}},
                                                                 {'ExportTime': '1564655701',
                                                                  'FlowSequence': '16',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '78668',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:35:01.000000000 '
                                                                               'PDT',
                                                                  'Version': '9',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '16)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 43,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}}]
                                                                                                }}}}}

        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.sampling_obs_dmn_ids = ['786688']
        self.jf.flow_colls = ['5000::2']
        self.jf.jflow_template_version = '19.3'
        self.jf.option_templ_id = '640'
        self.jf.exp_optionpkt_flowset = '(Data) (640)'
        expected_option_data_pdu_dict = {'Sampling interval': '1'}
        self.assertEqual(self.jf.verify_mx_option_data_inline(expected_option_data_pdu_dict=expected_option_data_pdu_dict), False)


    def test_verify_mx_option_data_record_1(self):
        self.jf.get_chassis_platform_info = MagicMock()
        self.jf.get_jflow_template_version = MagicMock()
        self.jf.get_expected_template_details = MagicMock()
        self.jf.get_all_observation_domain_ids = MagicMock()
        self.jf.get_sampling_observation_domain_id = MagicMock()
        device_handle = MagicMock()
        flow_coll_ips = ['5000::2']
        tshark_output = MagicMock()
        decode_dump = {'FLOWS': {'5000::2': {'786688': {'640': {'OPTIONS_DATA':[{'ExportTime': '1564655641',
                                                                  'FlowSequence': '14',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:34:01.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '14)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 13,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}},
                                                                 {'ExportTime': '1564655671',
                                                                  'FlowSequence': '15',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:34:31.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '15)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '1'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 28,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}},
                                                                 {'ExportTime': '1564655701',
                                                                  'FlowSequence': '16',
                                                                  'Length': '28',
                                                                  'Observation Domain Id': '786688',
                                                                  'Timestamp': 'Aug  '
                                                                               '1, '
                                                                               '2019 '
                                                                               '03:35:01.000000000 '
                                                                               'PDT',
                                                                  'Version': '10',
                                                                  '[Expert Info (Warning/Sequence)': 'Unexpected '
                                                                                                     'flow '
                                                                                                     'sequence '
                                                                                                     'for '
                                                                                                     'domain '
                                                                                                     'ID '
                                                                                                     '65536 '
                                                                                                     '(expected '
                                                                                                     '0, '
                                                                                                     'got '
                                                                                                     '16)]',
                                                                  '[Group': 'Sequence]',
                                                                  '[Severity level': 'Warning]',
                                                                  'flowset': {'FlowSet Id': '(Data) '
                                                                                            '(640)',
                                                                              'FlowSet Length': '12',
                                                                              '[Template Frame': '12]',
                                                                              'field': [],
                                                                              'num_field': 0,
                                                                              'num_pdu': 1,
                                                                              'pdu': [{'FlowExporter': '1',
                                                                                       'Sampling interval': '3'}],
                                                                              'type': 'OPTIONS_DATA'},
                                                                  'frame_index': 43,
                                                                  'ip': {'dst_ip': '50.1.1.11',
                                                                         'src_ip': '50.1.1.1'},
                                                                  'udp': {}}]
                                                                                                }}}}}

        SrcAddr = ['70.0.0.1']
        decode_dump_with_flow_selectors = {'decode_dump': decode_dump, 'flow_selector_identifier_info' : [{ 'SrcAddr': SrcAddr}]}
        self.jf.init(device_handle = device_handle, cflow_version = '10', template_type = 'ipvx', sampling_interface = 'ge-1/0/5.0', decode_dump_with_flow_selectors=decode_dump_with_flow_selectors, tshark_output = tshark_output, flow_colls=flow_coll_ips)
        #self.jf.get_jflow_template_version = MagicMock()
        #self.jf.get_jflow_template_version.return_value = '15.1'
        self.jf.sampling_obs_dmn_ids = ['786688']
        self.jf.flow_colls = ['5000::2']
        self.jf.jflow_template_version = '19.3'
        self.jf.option_templ_id = '640'
        self.jf.exp_optionpkt_flowset = '(Data) (640)'
        expected_option_data_pdu_dict = {'Sampling interval': '1'}
        self.assertEqual(self.jf.verify_mx_option_data_inline(expected_option_data_pdu_dict=expected_option_data_pdu_dict), False)

    def test_verify_templates_timestamps_and_refresh_rate_true(self):
        self.jf.verify_mx_refresh_rates = MagicMock()
        self.jf.verify_mx_refresh_rates.return_value = True
        self.assertEqual(self.jf.verify_templates_timestamps_and_refresh_rate(), True)

    def test_verify_templates_timestamps_and_refresh_rate_false(self):
        self.jf.verify_mx_refresh_rates = MagicMock()
        self.jf.verify_mx_refresh_rates.return_value = False
        self.assertEqual(self.jf.verify_templates_timestamps_and_refresh_rate(), False)

    def test_verify_flow_sequence_true(self):
        self.jf.verify_mx_flow_sequence = MagicMock()
        self.jf.verify_mx_flow_sequence.return_value = True
        self.assertEqual(self.jf.verify_flow_sequence(), True)

    def test_verify_flow_sequence_false(self):
        self.jf.verify_mx_flow_sequence = MagicMock()
        self.jf.verify_mx_flow_sequence.return_value = False
        self.assertEqual(self.jf.verify_flow_sequence(), False)


    def test_total_lu_per_pfe_hyp(self):
        self.assertEqual(self.jf.get_total_lu_per_pfe(pfe_type='hyp'), 4)

    def test_total_lu_per_pfe_snrkl(self):
        self.assertEqual(self.jf.get_total_lu_per_pfe(pfe_type='snrkl'), 2)

    def test_get_total_pfe_instance_1(self):
        self.assertEqual(self.jf.get_total_pfe_instance(pfe_type='neo'), 2)

    def test_get_total_pfe_instance_2(self):
        self.assertEqual(self.jf.get_total_pfe_instance(pfe_type='hyp'), 1)

    def test_get_total_pfe_instance_3(self):
        self.assertEqual(self.jf.get_total_pfe_instance(pfe_type='snrkl'), 2)

    def test_get_total_pfe_instance_4(self):
        self.assertEqual(self.jf.get_total_pfe_instance(pfe_type='as'), 4)

    def test_get_total_pfe_instance_5(self):
        self.assertEqual(self.jf.get_total_pfe_instance(pfe_type='vfpc'), 1)

    def test_get_total_pfe_instance_6(self):
        self.assertEqual(self.jf.get_total_pfe_instance(pfe_type='vzt'), 1)

    def test_get_total_pfe_instance_7(self):
        self.assertEqual(self.jf.get_total_pfe_instance(pfe_type='summit'), 3)

    def test_get_total_pfe_instance_8(self):
        self.assertEqual(self.jf.get_total_pfe_instance(pfe_type='vale8edge'), 6)

    def test_get_export_records_traversed(self):
        self.jf.list_traverser = '1'
        self.assertEqual(self.jf.get_export_records_traversed(), '1')


    def test_get_pfe_type_1(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MX104"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'mx104')

    def test_get_pfe_type_2(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC Type 2"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'neo')

    def test_get_pfe_type_3(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC 3D 16x 10GE"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'as')

    def test_get_pfe_type_4(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC Type 3"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'hyp')


    def test_get_pfe_type_5(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC Type 4"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'snrkl')

    def test_get_pfe_type_6(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC Type 5"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'xl5')

    def test_get_pfe_type_7(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC Type 6"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'xl6')

    def test_get_pfe_type_8(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC7E"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'stout1')


    def test_get_pfe_type_9(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC8E"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'stout2')


    def test_get_pfe_type_10(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC2E NG"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'aloha2')


    def test_get_pfe_type_11(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "Virtual FPC"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'vfpc')


    def test_get_pfe_type_12(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "LC2103"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'summit')

    def test_get_pfe_type_13(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "LC2102"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'vale8edge')

    def test_get_pfe_type_14(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "JNP204"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'summit_1ru')

    def test_get_pfe_type_15(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "MPC10E"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'ferrari10')


    def test_get_pfe_type_16(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "VMX ZT MPC"
        self.assertEqual(self.jf.get_pfe_type(device_handle= self.jf.dhandle, fpc_slot='2'), 'vzt')


    def test_get_pfe_num_1(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.get_pfe_type = MagicMock()
        self.jf.get_pfe_type.return_value = "hhh"
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "VMX ZT MPC"
        self.assertEqual(self.jf.get_pfe_number(device_handle= self.jf.dhandle, interface='ge-2/1/0.0'), 1)


    def test_get_pfe_num_2(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.get_pfe_type = MagicMock()
        self.jf.get_pfe_type.return_value = "summit"
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "VMX ZT MPC"
        self.assertEqual(self.jf.get_pfe_number(device_handle= self.jf.dhandle, interface='ge-2/0/13.0'), 0)

    def test_get_pfe_num_3(self):
        response_path = Values()
        self.jf.dhandle = MagicMock()
        self.jf.get_pfe_type = MagicMock()
        self.jf.get_pfe_type.return_value = "summit"
        self.jf.dhandle.cli.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "VMX ZT MPC"
        self.assertEqual(self.jf.get_pfe_number(device_handle= self.jf.dhandle, interface='ge-2/1/13.0'), 1)


if __name__ == '__main__':
    unittest.main()
