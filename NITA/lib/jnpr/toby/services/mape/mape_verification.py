#!/usr/bin/python3

"""
This module contains API's for Colecttors action

__author__ = ['Manoj Kumar']
__contact__ = 'vmanoj@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2020'

"""
import re
import copy
import pprint
import ipaddress
from jnpr.toby.services import utils
from jnpr.toby.utils import iputils

class mape_verification(object):
    """
    Class to decode and verify the mape encapsulation done by MAP-E BR router
    """

    def __init__(self):
        self.tvars = {}
        self.flow_selectors = []
        self.device = None
        self.tcpdump_file = None
        self.tethereal = None
        self.decoded_dict = None
        self.tshark_output = None
        self.tcpdump_decode_file = None
        self.dst_ipv4_start = None
        self.dst_udp_port_start = None
        self.dst_ipv4_flow_count = None
        self.src_ipv6_start = None
        self.src_ipv6_flow_count = None
        self.mape_version = None
        self.mape_v6_prefix = None
        self.mape_v4_prefix = None
        self.ea_bit_len = None
        self.psid_len = None
        self.psid_offset = None
        self.encap = None
        self.log = utils.log

    def init(self, **kwargs):
        """
        Decode and verify the mape encapsulation
        """
        self.device = kwargs.get("device", None)
        self.tcpdump_file = kwargs.get("tcpdump_file", None)
        self.tcpdump_decode_file = kwargs.get("tcpdump_decode_file", None)
        self.tethereal = kwargs.get("tethereal", None)
        self.flow_selectors = kwargs.get("flow_selectors", [])
        self.dst_ipv4_start = kwargs.get("dst_ipv4_start", None)
        self.dst_udp_port_start = kwargs.get("dst_udp_port_start", None)
        self.dst_ipv4_count = kwargs.get("dst_ipv4_count", 1)
        self.src_ipv6_start = kwargs.get("src_ipv6_start", None)
        self.src_ipv6_count = kwargs.get("src_ipv6_count", 1)
        self.dst_udp_port_count = kwargs.get("dst_udp_port_count", 1)
        self.mape_version = kwargs.get("mape_version", 7597)
        self.mape_v6_prefix = kwargs.get("mape_v6_prefix", None)
        self.mape_v4_prefix = kwargs.get("mape_v4_prefix", None)
        self.ea_bit_len = kwargs.get("ea_bit_len", None)
        self.psid_len = kwargs.get("psid_len", None)
        self.psid_offset = kwargs.get("psid_offset", 4)
        self.encap = kwargs.get("encap", True)
        self.mape_sc_address = kwargs.get("mape_sc_address", None)
        self.proto = kwargs.get("proto", "UDP")
        self.dst_tcp_port_start = kwargs.get("dst_tcp_port_start", None)
        self.dst_tcp_port_count = kwargs.get("dst_tcp_port_count", 1)
        self.dst_icmp_id_start = kwargs.get("dst_icmp_id_start", None)
        self.dst_icmp_id_count = kwargs.get("dst_icmp_id_count", None)
        self.src_ipv4 = kwargs.get("src_ipv4", None)
        self.src_udp_port = kwargs.get("src_udp_port", None)
        self.src_tcp_port = kwargs.get("src_tcp_port", None)

        if self.device is None:
            raise ValueError("device handle is mandatory argument")
        if self.tethereal is None:
            raise ValueError("Path for tshark is Mandatory argument")
        if self.ea_bit_len is None:
            raise ValueError("ea_bit_len is Mandatory argument")
        if self.psid_len is None:
            raise ValueError("psid_len is Mandatory argument")
        if self.mape_v6_prefix is None:
            raise ValueError("mape_v6_prefix is mandatory argument")
        if self.mape_v4_prefix is None:
            raise ValueError("mape_v4_prefix is mandatory argument")
        if self.mape_sc_address is None:
            raise ValueError("mape_sc_address is mandatory argument")
        if self.encap is True and self.src_ipv4 is None:
            raise ValueError("src_ipv4 is mandatory argument")
        if str(self.proto) == "UDP" and self.src_udp_port is None:
            raise ValueError("src_udp_port is mandatory argument when protocol is UDP")
        if str(self.proto) == "TCP" and self.src_tcp_port is None:
            raise ValueError("src_tcp_port is mandatory argument when protocol is TCP")

        self.decoded_dict = {}


    def decode_captured_dump(self):
        """
        Decode the captured dump
        """
        device = self.device
        response = device.shell(command="ls %s" %self.tethereal)
        if re.search(r'No such file or directory', response.response()):
            raise Exception("Could not find the tethereal path on the host")
        device.shell(command="cat /dev/null > %s" %self.tcpdump_decode_file)
        device.shell(command='/etc/rc.local')
        device.shell(command="%s -r %s -V >> %s" %(self.tethereal, \
                self.tcpdump_file, self.tcpdump_decode_file))
        self._parse_mape_tethereal_verbose()

    def _parse_mape_tethereal_verbose(self):
        """
        Parser to create dictionary of decoded packets
        """
        device = self.device
        decoded_file = self.tcpdump_decode_file
        decoded_dict = self.decoded_dict

        self.log('info', 'Decoding tethereal verbose output')
        num_pkts = -1

        #cat the decoded file and capture the output to a variable
        resp = device.shell(command="cat %s" %(decoded_file))

        ifile = resp.response().replace('\r\n', '\n')
        self.tshark_output = str(ifile)

        frame = {}
        frame['ipv6'] = {}
        frame['ipv4'] = {}
        frame['udp'] = {}
        frame['tcp'] = {}
        frame['icmp'] = {}

        #split the ouput based on new lines and store all the lines in a list
        lines = ifile.split("\n")

        #for every line in the list
        for line_num in range(len(lines)):
            #look for "Frame ([0-9]+)[\s|:]" which is a delimiter to identify a different packet
            match = re.search(r"Frame ([0-9]+)[\s|:]", lines[line_num])
            if match:
                frame_num = match.group(1)
                num_pkts += 1
                frame['frame_index'] = num_pkts + 1
                self.log('info', 'Found frame# %s' %frame_num)
                continue

            if self.encap is True:
                match_ipv6 = re.search(r"Internet Protocol Version 6, Src: (?P<source_ip>\w+.*),.*Dst: (?P<dst_ip>\w+.*)$", lines[line_num])
                match_next_header = re.search(r"Next Header: (\w+.*)", lines[line_num])
                match_ipv4 = re.search(r"Internet Protocol Version 4, Src: (?P<source_ipv4>\d+::\d+|[0-9\.]+).* Dst: (?P<dst_ipv4>\d+::\d+|[0-9\.]+)", lines[line_num])
                match_protocol = re.search(r"Protocol: (\w+)", lines[line_num])
                match_udp = re.search(r"User Datagram Protocol, Src Port: (\d+), Dst Port: (\d+)"\
                        , lines[line_num])
                match_tcp = re.search(\
                        r"Transmission Control Protocol, Src Port: (\d+), Dst Port: (\d+)",\
                        lines[line_num])
                match_icmp_type = re.search(r"Type: (\d+)", lines[line_num])
                match_icmp_code = re.search(r"Code: (\d+)", lines[line_num])
                match_icmp_id = re.search(r"Identifier \(BE\): (\d+)", lines[line_num])
                match_end = re.search(r"Data \(\d+.*\)", lines[line_num])
                if match_ipv6:
                    frame['ipv6']['src_ipv6'] = match_ipv6.group('source_ip')
                    frame['ipv6']['dst_ipv6'] = match_ipv6.group('dst_ip')
                if match_next_header:
                    frame['ipv6']['nxt_hdr'] = match_next_header.group(1)
                if match_ipv4:
                    frame['ipv4']['src_ipv4'] = match_ipv4.group('source_ipv4')
                    frame['ipv4']['dst_ipv4'] = match_ipv4.group('dst_ipv4')
                if match_protocol:
                    frame['ipv4']['protocol'] = match_protocol.group(1)
                if match_udp:
                    frame['udp']['udp_src_port'] = match_udp.group(1)
                    frame['udp']['dst_udp_port'] = match_udp.group(2)
                if match_tcp:
                    frame['tcp']['tcp_src_port'] = match_tcp.group(1)
                    frame['tcp']['tcp_dst_port'] = match_tcp.group(2)
                if match_icmp_code:
                    frame['icmp']['icmp_code'] = match_icmp_code.group(1)
                if match_icmp_type:
                    frame['icmp']['icmp_type'] = match_icmp_type.group(1)
                if match_icmp_id:
                    frame['icmp']['icmp_id'] = match_icmp_id.group(1)
                if match_end:
                    self._create_decoded_dict(frame, num_pkts+1)
                continue

        pprint.pprint(self.decoded_dict)

    def _create_decoded_dict(self, frame, frame_index):
        """
        Creates dictionary from the decoded frame
        """
        temp_dict = self.decoded_dict
        flow_selectors = self.flow_selectors
        if len(flow_selectors) == 0 or flow_selectors is None:
            flow_selectors = self._get_flow_keys()

        for selector in flow_selectors:
            pdu_dict = temp_dict
            selector_val = None
            if re.search(r".*udp_.*", selector):
                selector_val = frame['udp'][selector]
            elif re.search(r".*tcp_.*", selector):
                selector_val = frame['tcp'][selector]
            elif re.search(r".*icmp_.*", selector):
                selector_val = frame['icmp'][selector]
            elif re.search(r".*ipv4.*", selector):
                selector_val = frame['ipv4'][selector]
            elif re.search(r".*ipv6.*", selector):
                selector_val = frame['ipv6'][selector]

            if selector_val not in pdu_dict.keys():
                pdu_dict[selector_val] = {}
                if selector == flow_selectors[-1]:
                    pdu_dict[selector_val][frame_index] = copy.deepcopy(frame)
            else:
                if selector == flow_selectors[-1]:
                    pdu_dict[selector_val][frame_index] = copy.deepcopy(frame)
            temp_dict = pdu_dict[selector_val]

    def _get_flow_keys(self):
        """
        Get flow keys when not parsed
        """
        return ['dst_ipv4', 'dst_udp_port']

    def verify_mape_encap_packets(self):
        """
        Verify mape encapsulated packets
        """
        mape_version = self.mape_version
        test_status = True
        for ip_int in range(int(ipaddress.IPv4Address(self.dst_ipv4_start)), \
                int(ipaddress.IPv4Address(self.dst_ipv4_start)) + int(self.dst_ipv4_count)):
            ip = str(ipaddress.IPv4Address(ip_int))
            if str(self.proto) == "UDP":
                for port in range(int(self.dst_udp_port_start), int(self.dst_udp_port_start) + \
                        int(self.dst_udp_port_count)):
                    exp_dst_ip = self._get_encap_exp_dst_ip(ip, port)
                    port = str(port)
                    for frame_index in self.decoded_dict[ip][port].keys():
                        if str(self.decoded_dict[ip][port][frame_index]['ipv6']['src_ipv6'])  \
                                != str(self.mape_sc_address):
                            self.log("SC address does not match in frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['ipv6']['dst_ipv6']) \
                                != str(exp_dst_ip):
                            self.log("Destination v6 address does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['ipv6']['nxt_hdr']) != \
                                'IPIP (4)':
                            self.log("Next Header does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['ipv4']['src_ipv4']) != \
                                str(self.src_ipv4):
                            self.log("Source IPv4 does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['udp']['udp_src_port']) != \
                                str(self.src_udp_port):
                            self.log("Source port does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
            elif str(self.proto) == "TCP":
                for port in range(int(self.dst_tcp_port_start), int(self.dst_tcp_port_start) + \
                        int(self.dst_tcp_port_count)):
                    exp_dst_ip = self._get_encap_exp_dst_ip(ip, port)
                    port = str(port)
                    for frame_index in self.decoded_dict[ip][port].keys():
                        if str(self.decoded_dict[ip][port][frame_index]['ipv6']['src_ipv6']) != \
                                str(self.mape_sc_address):
                            self.log("SC address does not match in frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['ipv6']['dst_ipv6']) != \
                                str(exp_dst_ip):
                            self.log("Destination v6 address does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['ipv6']['nxt_hdr']) != \
                                'IPIP (4)':
                            self.log("Next Header does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['ipv4']['src_ipv4']) != \
                                str(self.src_ipv4):
                            self.log("Source IPv4 does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['tcp']['tcp_src_port']) != \
                                str(self.src_tcp_port):
                            self.log("Source port does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
            elif str(self.proto) == "ICMP":
                for port in range(int(self.dst_icmp_id_start), int(self.dst_icmp_id_start) + \
                        int(self.dst_icmp_id_count)):
                    exp_dst_ip = self._get_encap_exp_dst_ip(ip, port)
                    port = str(port)
                    for frame_index in self.decoded_dict[ip][port].keys():
                        if str(self.decoded_dict[ip][port][frame_index]['ipv6']['src_ipv6']) != \
                                str(self.mape_sc_address):
                            self.log("SC address does not match in frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['ipv6']['dst_ipv6']) != \
                                str(exp_dst_ip):
                            self.log("Destination v6 address does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['ipv6']['nxt_hdr']) != \
                                'IPIP (4)':
                            self.log("Next Header does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
                        if str(self.decoded_dict[ip][port][frame_index]['ipv4']['src_ipv4']) != \
                                str(self.src_ipv4):
                            self.log("Source IPv4 does not match for frame number %s" \
                                    %(frame_index))
                            test_status &= False
        return test_status

    def _get_encap_exp_dst_ip(self, ip, port):
        """
        Get the expected ipv6 address based on parsed ipv4 address and port number
        """
        v4_host_bit_len = 32 - int(iputils.get_mask(self.mape_v4_prefix))
        v4_bin = bin(int(ipaddress.IPv4Address(ip)))
        v4_bin_str = v4_bin[2:].zfill(32)
        p_bits = str(v4_bin)[len(v4_bin)-v4_host_bit_len : len(v4_bin)]
        port_bin = str(bin(int(port)))[2:].zfill(16)
        q_bits = port_bin[int(self.psid_offset)  : int(self.psid_offset) + int(self.psid_len)]
        v6_prefix_len = iputils.get_mask(self.mape_v6_prefix)
        v6_prefix_bin = bin(int(ipaddress.IPv6Address(iputils.strip_mask(self.mape_v6_prefix))))
        v6_prefix_bin_str = str(v6_prefix_bin[2:].zfill(128))
        nw_pad_bits = 64 - int(v6_prefix_len) - int(self.ea_bit_len)
        psid_pad_bits = 16 - int(self.psid_len)

        final_ipv6 = ""
        if int(self.mape_version) == 3:
            intf_id = v4_bin_str.zfill(len(v4_bin_str) + 8) + q_bits.zfill(16) + "".zfill(8)
            nw_bits = v6_prefix_bin_str[0:int(v6_prefix_len)] + p_bits + q_bits + \
                    "".zfill(nw_pad_bits)
            final_ipv6 = ipaddress.IPv6Address(int(nw_bits + intf_id, 2))
        else:
            intf_id = v4_bin_str.zfill(len(v4_bin_str)+16) + q_bits.zfill(len(q_bits) + \
                    psid_pad_bits)
            nw_bits = v6_prefix_bin_str[0:int(v6_prefix_len)] + p_bits + q_bits + \
                    "".zfill(nw_pad_bits)
            final_ipv6 = ipaddress.IPv6Address(int(nw_bits + intf_id, 2))
        return final_ipv6

    def delete_decoded_dict(self):
        """
        Delete contents of decoded_dict when called
        """
        del self.decoded_dict
        self.decoded_dict = {}

    def change_mape_version(self, **kwargs):
        """
        Change the value of mape_version knob to change the calculation of expected ipv6 address
        """
        self.mape_version = kwargs.get("mape_version", None)