#!/usr/local/bin/python3
from jnpr.toby.services.jflow.decode_jflow_dump import decode_jflow_dump
from jnpr.toby.hldcl.unix.unix import UnixHost
from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from optparse import Values

import builtins
builtins.t = MagicMock()

class Test_Decode_Jflow_Dump(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()

    def test_jflow_dump_decode_arguments_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        response = Values()
        response.response = MagicMock()
        response.response.return_value = 'Pass'
        djd.device.shell.return_value = response
        djd._parse_jflow_tethereal_verbose = MagicMock()
        djd._parse_jflow_tethereal_verbose.return_value = True
        var = {}
        self.assertEqual(djd._jflow_dump_decode(), None)

    def test_jflow_dump_decode_failure_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        response = Values()
        response.response = MagicMock()
        response.response.return_value = 'No such file or directory'
        djd.device.shell.return_value = response
        var = {}
        with self.assertRaises(Exception) as context:
            djd._jflow_dump_decode()
        self.assertTrue(
            'Could not find the tethereal path on the host' in str(context.exception))

    def test_parse_jflow_tethereal_verbose_ip_udp_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        djd.decoded_dict = {}
        resp = Values()
        resp.response = MagicMock()
        resp.response.return_value = '''Frame 5: 174 bytes on wire (1392 bits), 174 bytes captured (1392 bits)\n
                                        Internet Protocol Version 4, Src: 20.50.1.1 (20.50.1.1), Dst: 20.50.1.2 (20.50.1.2)\n
                                        Source: 20.50.1.1 (20.50.1.1)\n
                                        Destination: 20.50.1.2 (20.50.1.2)\n
                                        Differentiated Services Field: 0x00 (DSCP 0x00: Default; ECN: 0x00: Not-ECT (Not ECN-Capable Transport))
                                        User Datagram Protocol, Src Port: 50101 (50101), Dst Port: 2055 (2055)\n
                                        Cisco NetFlow/IPFIXi\n
					Frame 6: 174 bytes on wire (1392 bits), 174 bytes captured (1392 bits)'''
        djd.device.shell.return_value = resp
        var = {}
        djd._decode_netflow_packet = MagicMock()
        djd._decode_netflow_packet.return_value = 1
        self.assertEqual(djd._parse_jflow_tethereal_verbose(), None)

    def test_parse_jflow_tethereal_verbose_ip_udp_negative_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        resp = Values()
        resp.response = MagicMock()
        resp.response.return_value = '''Frame 5: 174 bytes on wire (1392 bits), 174 bytes captured (1392 bits)\n
					Internet Protocol Version 4, Src: 20.50.1.1 (20.50.1.1), Dst: 20.50.1.2 (20.50.1.2)\n
					Source: 20.50.1.1 (20.50.1.1)\n
					Destination: 20.50.1.2 (20.50.1.2)\n
					Differentiated Services Field: 0x00 (DSCP 0x00: Default; ECN: 0x00: Not-ECT (Not ECN-Capable Transport))
					User Datagram Protocol, Src Port: 50101 (50101), Dst Port: 2055 (2055)\n
					Cisco NetFlow/IPFIX'''
        djd.device.shell.return_value = resp
        var = {}
        with self.assertRaises(Exception) as context:
            djd._parse_jflow_tethereal_verbose()
        self.assertTrue(
            'No flowset found in Frame 0' in str(context.exception))

    def test_decode_netflow_packet_data_template_inline_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()        
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd.mpls_over_udp = 1
        lines = ['Cisco NetFlow/IPFIX',
                       'Set 1',
                          'FlowSet Id: Data Template (V10 [IPFIX]) (2)',
                          'FlowSet Length: 116',
                          'Template (Id = 256, Count = 27)',
                          'Template Id: 256',
                          'Field (1/27): IP_SRC_ADDR',
                          '0... .... .... .... = Pen provided: No',
                          '.000 0000 0000 1000 = Type: IP_SRC_ADDR (8)',
                          'Length: 4',
			  'Field (25/30): flowStartMilliseconds',
			  '0... .... .... .... = Pen provided: No',
			  '000 0000 1001 1000 = Type: flowStartMilliseconds (152)',
			  'Length: 8',
			  'Field (1/10): DESTINATION_MAC',
			  '0... .... .... .... = Pen provided: No',
			  '.000 0000 0101 0000 = Type: DESTINATION_MAC (80)',
			  'Length: 6',
			  'Field (1/27): IPV6_SRC_ADDR',
			  '0... .... .... .... = Pen provided: No',
			  '.000 0000 0001 1011 = Type: IPV6_SRC_ADDR (27)',
			  'Length: 16',
                          '.000 0000 0001 1011 = Type: IPV6_SRC_ADDR (27)',
			  'Frame 5: 174 bytes on wire (1392 bits), 174 bytes captured (1392 bits)',
			  'Set 1']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_data_template_mpls_v9_inline_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'Version: 9',
            'SourceId: 721920',
            'FlowSet 1',
            'FlowSet Id: Data Template (V9) (0)',
            'Template (Id = 324, Count = 26)',
            'Template Id: 324',
            'Field (1/26): MPLS_LABEL_1',
            'Type: MPLS_LABEL_1 (70)',
            'Length: 3']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_data_template_mpls_v4_v9_inline_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd.mpls_over_udp = 1
        lines = ['Cisco NetFlow/IPFIX',
            'Version: 9',
            'SourceId: 721920',
            'FlowSet 1',
            'FlowSet Id: Data Template (V9) (0)',
            'FlowSet Id: (Data) (323)',
            'Field (1/26): MPLS_LABEL_1',
            'Type: MPLS_LABEL_1 (70)',
            'Field (2/26): MPLS_LABEL_1',
            'Type: MPLS_LABEL_1 (70)'
            'Length: 3']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_v9_data_packet_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd.mpls_over_udp = 1
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX:',
            'Version: 9',
            'Timestamp: May 25, 2017 10:52:27.000000000 IST',
            'FlowSequence: 339',
            'FlowSet 1',
            'FlowSet Id: (Data) (259)',
            'FlowSet Length: 104',
            'Flow 1',
            'MPLS-Label1: 16 exp-bits: 0 top-of-stack',
            'MPLS-Label2: 0 exp-bits: 0',
            'SrcAddr: 2001::2 (2001::2)',
            'SrcAddr: 1001::2 (1001::2)',
            'DstAddr: 10.50.1.2 (10.50.1.2)',
            'SrcPort: 20 (20)']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_ipfix_options_template_pic_template_scope_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'FlowSet 1',
            'FlowSet Id: Options Template(V9) (1)',
            'FlowSet Length: 28',
            'Options Template (Id = 257) (Scope Count = 1; Data Count = 3)',
            'Template Id: 257',
            'Option Scope Length: 4',
            'Option Length: 12',
            'Field (1/1) [Scope]: Template',
            'Scope Type: Template (5)',
            'Length: 2',
            'Field (1/3): FLOW_ACTIVE_TIMEOUT',
            'Type: FLOW_ACTIVE_TIMEOUT (36)',
            'Length: 2',
            'Field (2/3): FLOW_INACTIVE_TIMEOUT',
            'Type: FLOW_INACTIVE_TIMEOUT (37)'
            'Length: 2',
            'Field (3/3): SAMPLING_INTERVAL',
            'Type: SAMPLING_INTERVAL (34)',
            'Length: 4']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_ipfix_options_template_pic_system_scope_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'FlowSet 1',
            'FlowSet Id: Options Template(V9) (1)',
            'Options Template (Id = 261) (Scope Count = 1; Data Count = 1)',
            'Template Id: 261',
            'Field (1/1) [Scope]: System'
            'Scope Type: System (1)'
            'Length: 4',
            'Field (1/1): SAMPLING_ALGORITHM',
            'Type: SAMPLING_ALGORITHM (35)',
            'Length: 1']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_ipfix_options_data_pic_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'FlowSet 1',
            'FlowSet Id: (Data) (260)',
            'Flow 1',
            'ScopeTemplate: 0103',
            'Flow active timeout: 120',
            'Flow inactive timeout: 30',
            'Sampling interval: 1800000',
            'FlowSet 2',
            'FlowSet Id: (Data) (260)',
            'Flow 1',
            'ScopeSystem: 01000000',
            'Sampling algorithm: Random sampling mode configured (2)']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_options_template_v9_inline_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'Version: 9',
            'FlowSet 1',
            'FlowSet Id: Options Template(V9) (1)',
            'Options Template (Id = 580) (Scope Count = 1; Data Count = 5)',
            'Template Id: 580',
            'Field (1/1) [Scope]: System',
            'Scope Type: System (1)',
            'Length: 0',
            'Field (1/5): SAMPLING_INTERVAL',
            'Type: SAMPLING_INTERVAL (34)',
            'Length: 4',
            'Field (2/5): FLOW_ACTIVE_TIMEOUT',
            'Type: FLOW_ACTIVE_TIMEOUT (36)',
            'Field (3/5): FLOW_INACTIVE_TIMEOUT',
            'Field (4/5): TOTAL_PKTS_EXP',
            'Field (5/5): TOTAL_FLOWS_EXP']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_options_template_ipfix_inline_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'Version: 10',
            'Observation Domain Id: 721920',
	    'Set 1',
            'FlowSet Id: Options Template (V10 [IPFIX]) (3)',
            'Options Template (Id = 516) (Scope Count = 1; Data Count = 10)',
            'Template Id: 516',
            'Field (1/1) [Scope]: FLOW_EXPORTER',
            '0... .... .... .... = Pen provided: No',
            '.000 0000 1001 0000 = Type: FLOW_EXPORTER (144)',
            'Length: 4']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_options_data_v9_inline_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'Version: 9',
            'SysUptime: 19088000',
            'SourceId: 721920',
            'FlowSet 1',
            'FlowSet Id: (Data) (580)',
            'Flow 1',
            'Sampling interval: 1',
            'Flow active timeout: 180',
            'Flow inactive timeout: 60',
            'PacketsExp: 702',
            'FlowsExp: 1310']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_options_data_ipfix_inline_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'Version: 10',
            'Observation Domain Id: 721920',
            'Set 1',
            'FlowSet Id: (Data) (516)',
            'Flow 1',
            'FlowExporter: 00000002',
            'PacketsExp: 610',
            'FlowsExp: 429',
            'System Init Time: Jan 25, 2016 07:13:01.000000000 GMT+6',
            'ExporterAddr: 10.0.0.1 (10.0.0.1)',
            'Sampling interval: 1',
            'Flow active timeout: 180',
	    'FlowExporter: 00000002',
	    'ExportProtocolVersion: 10'
	    'ExportTransportProtocol: 17',
	    'ExportProtocolVersion: 10']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_options_flowset_pic_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'Version: 9',
            'SourceId: 20',
            'FlowSet 1',
            'Options FlowSet: 1',
            'Template Id: 263']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_template_flowset_pic_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'Version: 9',
            'SourceId: 20',
            'FlowSet 1',
            'Template FlowSet: 0']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_decode_netflow_packet_data_flowset_pic_case(self):
        djd = decode_jflow_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        djd._convert_time_stamp_to_epoch = MagicMock()
        djd._convert_time_stamp_to_epoch.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
            'Version: 9',
            'SourceId: 20',
            'FlowSet 1',
            'Data FlowSet (Template Id): 263']
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)

    def test_cp_flowset_v4_data_packet_with_flow_selector_case(self):
        djd = decode_jflow_dump()
        var = {}
        djd.flow_selectors = ['SrcAddr', 'DstAddr']
        frame = {'Observation Domain Id' : '525568',
            'FlowSequence' : '112',
            'Version': '10',
            'flowset': {'FlowSet Id': '(Data) (256)',
              'num_pdu': 1,
              'pdu': [{'Direction': 'Unknown (255)',
                'Dot1q Customer Vlan Id': '0',
                'DstAddr': '2.0.0.2',
                'SrcAddr': '1.0.0.1',
		'SrcPort': '20 (20)',
		'Dot1q Vlan Id': '0'}]},
	    'ip': {'dscp': '0x0', 'dst_ip': '20.50.1.2', 'src_ip': '20.50.1.1'},
	    'tmpl_type': '',
	    'frame_index': '5',
	    'udp': {'dst_port': '2055', 'src_port': '50101'}
	    }
        self.assertEqual(djd._cp_flowset(var, frame), None)

    def test_cp_flowset_v6_data_packet_with_flow_selector_negative_case(self):
        djd = decode_jflow_dump()
        var = {}
        flow_selectors = ['SrcAddr', 'DstAddr']
        frame = {'Observation Domain Id' : '525568',
            'FlowSequence' : '112',
            'Version': '10',
	    'flowset': {'FlowSet Id': '(Data) (257)',
              'num_pdu': 1,
              'pdu': [{'Direction': 'Unknown (255)',
                'Dot1q Customer Vlan Id': '0',
                'DstAddr': '2222::2',
                'SrcAddr': '1111::2',
                'SrcPort': '20',
                'Dot1q Vlan Id': '0'}]},
            'ip': {'dscp': '0x0', 'dst_ip': '20.50.1.2', 'src_ip': '20.50.1.1'},
            'tmpl_type': 'ipv6',
            'frame_index': '5',
            'udp': {'dst_port': '2055', 'src_port': '50101'}
            }
        with self.assertRaises(Exception) as context:
            djd._cp_flowset(var, frame)
        self.assertTrue(
            'DstPort not found in keys of frame as well as pdu, 			    please make sure the string being parsed is correct for pdu_index 0' in str(context.exception))

    def test_cp_flowset_v4_data_packet_flow_selector_negative_case(self):
        djd = decode_jflow_dump()
        var = {}
        flow_selectors = []
        frame = {'SourceId' : '525568',
            'FlowSequence': '0',
            'Version': '10',
            'flowset': {'FlowSet Id': '(Data) (256)',
	      'type' : 'DATA',
              'num_pdu': 1,
              'pdu': [{'Direction': 'Unknown (255)',
                'Dot1q Customer Vlan Id': '0',
                'DstAddr': '2.0.0.2',
                'SrcAddr': '1.0.0.1',
                'Dot1q Vlan Id': '0'}]},
            'ip': {'dscp': '0x0', 'dst_ip': '20.50.1.2', 'src_ip': '20.50.1.1'},
            'tmpl_type': 'mpls-ipv4',
            'frame_index': '5',
            'udp': {'dst_port': '2055', 'src_port': '50101'}
            }
        with self.assertRaises(Exception) as context:
            djd._cp_flowset(var, frame)
        self.assertTrue(
            'SrcPort not found in keys of frame as well as pdu, 			    please make sure the string being parsed is correct for pdu_index 0' in str(context.exception))

    def test_cp_flowset_v6_data_packet_with_fs_type_negative_case(self):
        djd = decode_jflow_dump()
        var = {}
        flow_selectors = ['SrcAddr', 'DstAddr']
        frame = {'Observation Domain Id' : '525568',
            'FlowSequence' : '112',
            'Version': '10',
            'flowset': {
              'num_pdu': 1,
              'pdu': [{'Direction': 'Unknown (255)',
                'Dot1q Customer Vlan Id': '0',
                'DstAddr': '2222::2',
                'SrcAddr': '1111::2',
                'SrcPort': '20',
                'Dot1q Vlan Id': '0'}]},
            'ip': {'dscp': '0x0', 'dst_ip': '20.50.1.2', 'src_ip': '20.50.1.1'},
            'tmpl_type': 'ipv6',
            'frame_index': '5',
            'udp': {'dst_port': '2055', 'src_port': '50101'}
            }
        with self.assertRaises(Exception) as context:
            djd._cp_flowset(var, frame)
        self.assertTrue(
            '' in str(context.exception))

    def test_cp_flowset_v6_template_packet_case(self):
        djd = decode_jflow_dump()
        var = {}
        flow_selectors = []
        frame = {'FlowSequence': '0',
            'Observation Domain Id': '525312',
            'flowset': {'Field Count': '27',
              'FlowSet Id': 'Data Template (V10 [IPFIX]) (2)',
              'DataRecord (Template Id)': '256',
              'field': [{'Length': '4', 'Type': 'IP_SRC_ADDR (8)'}]},
            'frame_index': 1,
            'ip': {'dscp': '0x0', 'dst_ip': '10.50.1.2', 'src_ip': '10.50.1.1'},
            'tmpl_type': 'inline-ipv4',
            'udp': {'dst_port': '2055', 'src_port': '50101'}}
        self.assertEqual(djd._cp_flowset(var, frame), None)

    def test_cp_flowset_v6_options_template_packet_case(self):
        djd = decode_jflow_dump()
        var = {}
        flow_selectors = []
        frame = {'FlowSequence': '0',
	    'Observation Domain Id': '525312',
	    'Version': '10',
	    'flowset': {'FlowSet Id': 'Options Template (V10 [IPFIX]) (3)',
	      'FlowSet Length': '56',
	      'Template Id': '512',
	      'field': [{'Length': '4', 'Type': 'FLOW_EXPORTER (144)'}]},
            'frame_index': 1,
            'ip': {'dscp': '0x0', 'dst_ip': '10.50.1.2', 'src_ip': '10.50.1.1'},
            'tmpl_type': 'mpls-inline',
            'udp': {'dst_port': '2055', 'src_port': '50101'}}
        self.assertEqual(djd._cp_flowset(var, frame), None)

    def test_cp_flowset_vpls_data_packet_case(self):
        djd = decode_jflow_dump()
        var = {}
        flow_selectors = []
        frame = {'FlowSequence' : '0',
            'Observation Domain Id': '525312',
            'Version': '10',
            'flowset': {'FlowSet Id': '(Data) (258)',
              'FlowSet Length': '56',
              'Data FlowSet (Template Id)': '258',
              'pdu': [{'Destination Mac Address' : '00:00:00:00:02:29', 'Source Mac Address' : '00:00:00:00:01:11'}]},
            'frame_index': 1,
            'ip': {'dscp': '0x0', 'dst_ip': '10.50.1.2', 'src_ip': '10.50.1.1'},
            'tmpl_type': 'vpls',
            'udp': {'dst_port': '2055', 'src_port': '50101'}}
        self.assertEqual(djd._cp_flowset(var, frame), None)

    def test_cp_flowset_mpls_ipv4_v9_data_packet_case(self):
        djd = decode_jflow_dump()
        var = {}
        flow_selectors = []
        frame = {'FlowSequence' : '0',
            'SourceId': '525312',
            'Version': '9',
            'flowset': {'FlowSet Id': '(Data) (324)',
              'FlowSet Length': '56',
              'Template Id': '324',
              'pdu': [{'SrcAddr':'20.40.2.2', 'DstAddr':'50.0.0.9', 'MPLS-Label1':'1000208', 'MPLS-Label2':'1000400', 'MPLS-Label3':'0'}]},
            'frame_index': 1,
            'ip': {'dscp': '0x0', 'dst_ip': '10.50.1.2', 'src_ip': '10.50.1.1'},
            'tmpl_type': 'mpls-v9inlineipv4',
            'udp': {'dst_port': '2055', 'src_port': '50101'}}
        self.assertEqual(djd._cp_flowset(var, frame), None)

    def test_cp_flowset_mpls_ipv4_ipfix_data_packet_case(self):
        djd = decode_jflow_dump()
        var = {}
        flow_selectors = []
        frame = {'FlowSequence' : '0',
            'Observation Domain Id': '525312',
            'Version': '10',
            'flowset': {'FlowSet Id': '(Data) (260)',
              'FlowSet Length': '56',
              'Template Id': '260',
              'pdu': [{'SrcAddr':'20.40.2.2', 'DstAddr':'50.0.0.9', 'MPLS-Label1':'1000208', 'MPLS-Label2':'1000400', 'MPLS-Label3':'0'}]},
            'frame_index': 1,
            'ip': {'dscp': '0x0', 'dst_ip': '10.50.1.2', 'src_ip': '10.50.1.1'},
            'tmpl_type': 'mplsipv4-inline',
            'udp': {'dst_port': '2055', 'src_port': '50101'}}
        self.assertEqual(djd._cp_flowset(var, frame), None)

    def test_cp_flowset_mpls_v9_data_packet_case(self):
        djd = decode_jflow_dump()
        var = {}
        flow_selectors = []
        frame = {'FlowSequence' : '0',
            'SourceId': '525312',
            'Version': '9',
            'flowset': {'FlowSet Id': '(Data) (323)',
              'FlowSet Length': '56',
              'Template Id': '323',
              'pdu': [{'MPLS-Label1':'1000208', 'MPLS-Label2':'1000400', 'MPLS-Label3':'0'}]},
            'frame_index': 1,
            'ip': {'dscp': '0x0', 'dst_ip': '10.50.1.2', 'src_ip': '10.50.1.1'},
            'tmpl_type': 'v9inline-mpls',
            'udp': {'dst_port': '2055', 'src_port': '50101'}}
        self.assertEqual(djd._cp_flowset(var, frame), None)

if __name__ == '__main__':
  unittest.main()
