#!/usr/local/bin/python3
from jnpr.toby.services.usf.usf_cgnat_jflow_logging_decode_dump import usf_cgnat_jflow_logging_decode_dump
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
        djd = usf_cgnat_jflow_logging_decode_dump()
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
        djd = usf_cgnat_jflow_logging_decode_dump()
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
        djd = usf_cgnat_jflow_logging_decode_dump()
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
        djd = usf_cgnat_jflow_logging_decode_dump()
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

    def test_decode_netflow_packet_data_template_case(self):
        djd = usf_cgnat_jflow_logging_decode_dump()
        djd.device = MagicMock()
        djd.device.shell = MagicMock()        
        frame = {}
        var = {}
        djd._cp_flowset = MagicMock()
        djd._cp_flowset.return_value = True
        lines = ['Cisco NetFlow/IPFIX',
                'Version: 10',
                'Length: 40',
                'Timestamp: Mar  1, 2019 09:20:40.000000000 IST',
                'ExportTime: 1551412240',
                'FlowSequence: 2',
                'Observation Domain Id: 20',
                'Set 1 [id=2] (Data Template): 261',
                'FlowSet Id: Data Template (V10 [IPFIX]) (2)',
                'FlowSet Length: 24',
                'Template (Id = 261, Count = 4)',
                'Template Id: 261',
                'Field Count: 4',
                'Field (1/4): observationTimeMilliseconds',
                '0... .... .... .... = Pen provided: No',
                '.000 0001 0100 0011 = Type: observationTimeMilliseconds (323)',
                'Length: 8',
                'Field (2/4): natEvent',
                '0... .... .... .... = Pen provided: No',
                '.000 0000 1110 0110 = Type: natEvent (230)',
                'Length: 1',
                'Field (3/4): postNATSourceIPv4Address',
                '0... .... .... .... = Pen provided: No',
                '.000 0000 1110 0001 = Type: postNATSourceIPv4Address (225)',
                'Length: 4',
                'Field (4/4): PROTOCOL',
                '0... .... .... .... = Pen provided: No',
                '.000 0000 0000 0100 = Type: PROTOCOL (4)',
                'Length: 1'
              ]
        self.assertEqual(djd._decode_netflow_packet(lines=lines,line_num=0, num_pkts=0, frame=frame, var=var, flow_selectors='SrcAddr'), 0)


if __name__ == '__main__':
  unittest.main()