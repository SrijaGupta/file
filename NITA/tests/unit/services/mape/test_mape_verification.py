#!/usr/local/bin/python3
from jnpr.toby.services.mape.mape_verification import mape_verification
from jnpr.toby.hldcl.unix.unix import UnixHost
from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from optparse import Values

import builtins
builtins.t = MagicMock()

class Test_Mape_Verification(unittest.TestCase):
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()

    def test_mape_verification_arguments_case(self):
        mv = mape_verification()
        mv.device = MagicMock()
        mv.device.shell = MagicMock()
        response = Values()
        response.response = MagicMock()
        response.response.return_value = 'Pass'
        mv.device.shell.return_value = response
        mv._parse_mape_tethereal_verbose = MagicMock()
        mv._parse_mape_tethereal_verbose.return_value = True
        var = {}
        self.assertEqual(mv.decode_captured_dump(), None)

    def test_mape_dump_decode_failure_case(self):
        mv = mape_verification()
        mv.device = MagicMock()
        mv.device.shell = MagicMock()
        response = Values()
        response.response = MagicMock()
        response.response.return_value = 'No such file or directory'
        mv.device.shell.return_value = response
        var = {}
        with self.assertRaises(Exception) as context:
            mv.decode_captured_dump()
        self.assertTrue(
            'Could not find the tethereal path on the host' in str(context.exception))

    def test_parse_jflow_tethereal_verbose_ip_udp_case(self):
        mv = mape_verification()
        mv.device = MagicMock()
        mv.encap = True
        mv.device.shell = MagicMock()
        mv.decoded_dict = {}
        resp = Values()
        resp.response = MagicMock()
        resp.response.return_value = '''Frame 20: 100 bytes on wire (800 bits), 100 bytes captured (800 bits)\n
					Internet Protocol Version 6, Src: 2001:db8:ffff::2, Dst: 2001:db8:112:3400:0:c000:312:34\n
					Internet Protocol Version 4, Src: 20.1.1.2, Dst: 192.0.3.18\n
					User Datagram Protocol, Src Port: 1024, Dst Port: 9031'''
        mv.device.shell.return_value = resp
        var = {}
        mv._create_decoded_dict = MagicMock()
        mv._create_decoded_dict.return_value = 1
        self.assertEqual(mv._parse_mape_tethereal_verbose(), None)

    def test_create_decoded_dict(self):
        mv = mape_verification()
        mv.device = MagicMock()
        mv.device.shell = MagicMock()
        mv.decoded_dict = {}
        resp = Values()
        resp.response = MagicMock()
        mv._parse_mape_tethereal_verbose = MagicMock()
        mv._parse_mape_tethereal_verbose.return_value = True
        frame = {'ipv6' : {'src_ipv6': '2001::2',
                                 'dst_ipv6': '2001:db8::1',
                                 'nxt_hdr': 'IPIP'} ,
                       'ipv4' : {'src_ipv4': '20.1.1.2',
                                 'dst_ipv4': '192.0.2.18',
                                 'protocol': 'UDP'} ,
                       'udp': {'udp_src_port': '1024', 'dst_udp_port': '9030'}}
        self.assertEqual(mv._create_decoded_dict(frame, 1), None)

if __name__ == '__main__':
  unittest.main()