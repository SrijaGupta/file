#!/usr/bin/python3

"""
This module contains API's for Colecttors action

__author__ = ['Manoj Kumar']
__contact__ = 'vmanoj@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

"""

import re
import copy
import pprint
import threading
import json
import ipaddress
from jnpr.toby.services import utils

class decode_jflow_dump(object):
    """Class to decode jflow dump file stored on the jflow collector
    """

    def __init__(self):
        self.tvars = {}
        self.flow_selectors = []
        self.tcpdump_decode_file = None
        self.cflow_port = None
        self.decoded_dict = None
        self.device = None
        self.tcpdump_file = None
        self.tethereal = None
        self.mpls_over_udp = 0
        self.tshark_output = None
        self.time_before_tcpdump_started = None
        self.time_after_tcpdump_stopped = None
        self.kill_earlier_process = True
        self.oops_call = False
        self.rhh = None
        self.interface = None
        self.protocol = None
        self.rh_handle_passed = None
        self.size = None
        self.objj = None
        self.thr = None
        self.log = utils.log
        self.imon = False
        self.append_data_to_list = False

    def init(self, **kwargs):
        """
        Decode the jflow dump on all collector ports and return decoded output as dictionary
        """
        self.device = kwargs.get("device", None)
        self.tcpdump_file = kwargs.get("tcpdump_file", None)
        self.tcpdump_decode_file = kwargs.get("tcpdump_decode_file", None)
        self.cflow_port = kwargs.get("cflow_port", 2055)
        self.tethereal = kwargs.get("tethereal", None)
        self.flow_selectors = kwargs.get("flow_selectors", [])
        self.mpls_over_udp = kwargs.get("mpls_over_udp", 0)
        self.protocol = kwargs['protocol']
        self.size = kwargs.get('size', '2000')
        self.interface = kwargs['interface']
        self.kill_earlier_process = kwargs.get('kill_earlier_process', 'True')
        self.imon = bool(kwargs.get('imon', False))
        self.append_data_to_list = bool(kwargs.get('append_data_to_list', False))
        self.dump_decode_json_file = kwargs.get('dump_decode_json_file', None)
        self.imon_decode_type = kwargs.get('imon_decode_type', 'ipv4_udp')
        self.imon_decode_template = kwargs.get('imon_decode_template', None)
        self.oops_call = True
        if self.device is None:
            raise ValueError("device handle is mandatory argument")
        if self.tethereal is None:
            raise ValueError("Path for tshark is Mandatory argument")
        if "router_handle" in kwargs:
            self.rhh = kwargs['router_handle']
            self.rh_handle_passed = True
            print("\n Router Handle recieved \n")
        else:
            self.rh_handle_passed = False
            print("\n Router Handle not recieved \n")
        if self.imon is True and self.dump_decode_json_file is None:
            raise ValueError("dump_decode_json_file is mandatory argument for Inline Monitoring")
        if not isinstance(self.flow_selectors, list) and (self.flow_selectors is not None):
            self.flow_selectors = list(self.flow_selectors)
        self.decoded_dict = {}
        self.time_before_tcpdump_started = None
        self.time_after_tcpdump_stopped = None


    def decode_jflow_dump_on_all_col_ports(self, **kwargs):
        """
        Decode the jflow dump on all collector ports and return decoded output as dictionary

        This public method when called, will decode the pcap file captured by the collector
        as netflow packets. This decode will happen based on the parameters parsed with the
        help of tshark installed in the same machine/VM. The decoded dump is again stored in
        another file and each line in this file is parsed to build a dictionary. This dictionary
        can be used by the user to compare his expected values and decide to PASS or FAIL the
        case he is testing.

        :param obj device:
          **REQUIRED** device handle of the JFlow collector

        :param string tethereal:
          **REQUIRED** path to the tshark application in the Jflow collector

        :param string tcpdump_file:
          **OPTIONAL** path to the captured pcap file, default is /tmp/dump

        :param string tcpdump_decode_file:
          **OPTIONAL** path to store the decoded dump, default is /tmp/dump.decode

        :param string cflow_port:
          **OPTIONAL** UDP port number to which the jflow export packets are sent, default is 2055

        :param list flow_selectors:
          **OPTIONAL** list of flow keys to be used, default is selected by API itself based on
                       based on template ID

        :return: Decoded dictionary in key value format


	The dictionary will be built as follows::

        decoded_dict {'FLOWS' :
                         {'Col_IP' :
                             {'Domain ID' :
                                 {'Template ID' :
                                     {'Type of Packet' :
                                         {keys based on parsed value of flow_selectors :
                                             {hash of decoded netflow packet}
                                         }
                                      }
                                  }
                              }
                           }
                       }
        In the sample mentioned above, The description for each keys is as below:

        FLOWS: It is used to identify that it is a hash of decoded netflow packets
        Col_IP: The IP address of the flow collector on which the flows were collected
        Domain ID: It is the observation domain ID value of a particular packet
        Template ID: It is the template ID of a particular packet
        Type of packet: Used to identify the packet (TEMPLATE/OPTIONS/OPTIONS_DATA/DATA)
        Keys based on parsed value of flow_selectors: The user can choose the flow_selector
                          fields based on the parameters he is varying to create flows.

        For example, If [SrcAddr, DstAddr] is parsed as flow_selectors, then dictionary will
	will be built as below::

        decoded_dict {'FLOWS' :
                         {'Col_IP' :
                             {'Domain ID' :
                                 {'Template ID' :
                                     {'Type of Packet' :
                                         {Value for SrcAddr :
                                             {Value for DstAddr :
                                                 {hash of decoded netflow packet}
                                             }
                                         }
                                      }
                                  }
                              }
                           }
                       }

        An example of decoded dictionary is pasted below for the reference of the user.
        This example is for the data packet of IPv4 IPfix template. Here, SrcAddr, DstAddr
	was parsed as flow_selectors::

        decoded_dict {'FLOWS': {'10.50.1.2': '525313': {'256': {'DATA': {'1.0.0.1': {'2.0.0.1': {
                                               'ExportTime': '1474282062',
                                               'FlowSequence': '110',
                                               'Length': '105',
                                               'Observation Domain Id': '525313',
                                               'Timestamp': '1474282062',
                                               'Version': '10',
                                               'flowset': {'FlowSet Id': '(Data) (256)',
                                               'FlowSet Length': '89',
                                               'field': [],
                                               'num_field': 0,
                                               'num_pdu': 1,
                                               'pdu': {'Direction': 'Unknown (255)',
                                                       'Dot1q Customer Vlan Id': '0',
                                                       'Dot1q Vlan Id': '0',
                                                       'DstAS': '0',
                                                       'DstAddr': '2.0.0.1',
                                                       'DstMask': '8',
                                                       'DstPort': '50',
                                                       'EndTime': '1474282062',
                                                       'Flow End Reason': 'Active timeout (2)',
                                                       'IP ToS': '0x00',
                                                       'IPv4Ident': '0',
                                                       'InputInt': '660',
                                                       'MaxTTL': '20',
                                                       'MinTTL': '20',
                                                       'NextHop': '12.1.1.2',
                                                       'Octets': '35351874',
                                                       'OutputInt': '641',
                                                       'Packets': '768519',
                                                       'Protocol': '17',
                                                       'SrcAS': '0',
                                                       'SrcAddr': '1.0.0.1',
                                                       'SrcMask': '8',
                                                       'SrcPort': '20',
                                                       'StartTime': '1474281484',
                                                       'TCP Flags': '0x00',
                                                       'Type': '0',
                                                       'Vlan Id': '0',
                                                       },
                                              'frame_index': 7,
                                              'ip': {'dscp': '0x0',
                                                     'dst_ip': '10.50.1.2',
                                                     'src_ip': '10.50.1.1'},
                                              'udp': {'dst_port': '2055',
                                                      'src_port': '50101'}
                                                      },
                                                      }
                                                    }
                                                }
                                          }
                                      }
                                }
                          }

        """
        if self.oops_call is False:
            if "device" not in kwargs:
                raise ValueError("device handle is mandatory argument")
            if "tethereal" not in  kwargs:
                raise ValueError("Path for tshark is Mandatory argument")

            self.device = kwargs["device"]
            self.tcpdump_file = kwargs["tcpdump_file"]
            self.tcpdump_decode_file = kwargs["tcpdump_decode_file"]
            self.cflow_port = kwargs.get("cflow_port", 2055)
            self.tethereal = kwargs["tethereal"]
            self.flow_selectors = kwargs.get("flow_selectors", [])
            self.mpls_over_udp = kwargs.get("mpls_over_udp", 0)

            if not isinstance(self.flow_selectors, list) and (self.flow_selectors is not None):
                self.flow_selectors = list(self.flow_selectors)
            self.decoded_dict = {}
            self._jflow_dump_decode()
            self.log('info', 'decoded dump is :')
            pprint.pprint(self.decoded_dict)
            return self.decoded_dict

        if self.oops_call is True:
            self.decoded_dict = {}
            self._jflow_dump_decode()
            self.log('info', 'decoded dump is :')
            pprint.pprint(self.decoded_dict)
            return self.decoded_dict

    def decode_jflow_dump_on_collector(self):
        """
        Decode the jflow dump on all collector ports and return decoded output as dictionary
        """
        self._jflow_dump_decode()
        self.log('info', 'decoded dump is :')
        pprint.pprint(self.decoded_dict)
        return self.decoded_dict

    def get_python_decoded_dictionary(self):
        """ xxxxxxx """
        return self.decoded_dict

    def _jflow_dump_decode(self):
        """
            It decodes the pcap containing export records

            This definition decodes the pcap file containing export records and creates a decoded
	    file. This decoded file will be used to create the dictionary.
        """
        device = self.device
        response = device.shell(command="ls %s" %self.tethereal)
        if re.search(r'No such file or directory', response.response()):
            #self.log('error', "Could not find %s on host" %self.tethereal)
            raise Exception("Could not find the tethereal path on the host")

        device.shell(command="cat /dev/null > %s" %self.tcpdump_decode_file)
        device.shell(command='/etc/rc.local')
        device.shell(command="%s -r %s -d udp.port==%s,cflow -V >> %s" \
            %(self.tethereal, self.tcpdump_file, self.cflow_port, self.tcpdump_decode_file))

        if self.imon is True:
            device.shell(command="cat /dev/null > %s" %self.dump_decode_json_file)
            device.shell(command="%s -r %s -d udp.port==%s,cflow -T json -V >> %s" \
                %(self.tethereal, self.tcpdump_file, self.cflow_port, self.dump_decode_json_file))
            self.decoded_json = json.loads(self._get_decoded_json())
        #return self._parse_jflow_tethereal_verbose()
        self._parse_jflow_tethereal_verbose()

    def _get_decoded_json(self):
        """
        Returns the decoded json
        """
        device = self.device
        response = device.shell(command="cat %s" %self.dump_decode_json_file)
        return response.response()

    def _parse_jflow_tethereal_verbose(self):
        """
            A parser to create dictionary of decoded packets

            This definition is a parser which converts the file decoded by tshark to dictionary
	    format.It parses every line in the decoded packet and stores the detail of ip/udp
	    headers to the decoded dictionary. Once it sees the netflow payload, the control is
	    taken over by _decode_netflow_packet method which will store the netflow payload
	    details to dictionary.
        """
        device = self.device
        decoded_file = self.tcpdump_decode_file
        decoded_dict = self.decoded_dict

        self.log('info', 'Decoding tethereal verbose output')
        num_pkts = -1

        #cat the decoded file and capture the output to a variable
        resp = device.shell(command="cat %s" %(decoded_file))
        #ifile = resp.response()
        ifile = resp.response().replace('\r\n', '\n')
        self.tshark_output = str(ifile)
        #(fl_srvr, ip, udp, netflow) = (None, None, None, None)

        frame = {}
        frame['ip'] = {}
        frame['udp'] = {}

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
                #frame is dictionary which will be constructed based on the lines being
                #parsed frame['frame_index'] gives the index of exported packet
                self.log('info', 'Found frame# %s' %frame_num)
                continue

            match_src_ip = re.search(r"Source: (?P<source_ip>\d+::\d+|[0-9\.]+)", lines[line_num])
            #look to capture source/destination IPs,source/destination ports in the IP/UDP header
            #of the exported packet
            match_dst_ip = re.search(r"Destination: (?P<dst_ip>\d+::\d+|[0-9\.]+)", lines[line_num])
            match_udp = re.search(r"User Datagram Protocol, Src Port: (?P<src_port>[0-9|a-z]+).*Dst Port: [0-9|a-z]+ \((?P<dst_port>[0-9]+)\)", lines[line_num])
            dscp_regex_list = [r"Differentiated Services Field: 0x.. \(DSCP 0x(..):",
                               r"Differentiated Services Field: Class Selector . \(0x000000(..)\)",
                               r"Differentiated Services Field: Default \(0x000000(..)\)",
                               r"Differentiated Services Codepoint: Default \(0x(..)\)",
                               r"Differentiated Services Codepoint: Expedited \
                                   Forwarding \(0x(..)\)",
                               r"Differentiated Services Field: Expedited \
				   Forwarding \(0x000000(..)\)",
                               r"Differentiated Services Field: Unknown \(0x000000(..)\)",
                               r"Differentiated Services Codepoint: Unknown \(0x(..)\)/"]
            #look if dscp is being exported capture the value into frame['ip']['dscp'] if so
            for regex in dscp_regex_list:
                match_dscp = re.search(regex, lines[line_num])
                if match_dscp:
                    print("dscp value:", match_dscp.group(1))
                    frame['ip']['dscp'] = hex(int(match_dscp.group(1), 16))
            #store the captured values of source/destination IPs,source/destination ports in to
            #dictionary frame with appropriate keys
            if match_src_ip:
                frame['ip']['src_ip'] = match_src_ip.group('source_ip')
            elif match_dst_ip:
                frame['ip']['dst_ip'] = match_dst_ip.group('dst_ip')
            elif match_udp:
                frame['udp']['src_port'] = match_udp.group('src_port')
                frame['udp']['dst_port'] = match_udp.group('dst_port')
            elif re.search(r"Cisco NetFlow", lines[line_num]):
              #If Cisco NetFlow is found, it means it is netflow data call
              #_decode_netflow_packet API
                line_num = self._decode_netflow_packet(lines=lines, \
                    line_num=line_num, num_pkts=num_pkts, frame=frame, decoded_dict=decoded_dict)
                continue
        print("Number of packets", num_pkts)
        decoded_dict['NUM_FRAMES'] = num_pkts
        self.log('info', 'Completed decoding of the flows')

        self.decoded_dict = decoded_dict

    def _decode_netflow_packet(self, **kwargs):
        """
	    Decodes the netflow payload.

            This definition converts netflow payload in a packet to dictionary format.
            This method mainly identifies the type of netflow packet and stores the type
            in the dictionary. Also, stores as key value pairs till flowset is found.
            The flowset part is taken care by _cp_flowset method.

	    :param list lines
	        **REQUIRED** lines in the decoded file

	    :param int line_num
	        **REQUIRED** line number from where the metod starts parsing

	    :param int num_pkts
	        **REQUIRED** number of packets in decoded dump

	    :param dict frame
	        **REQUIRED** decoded frame in dictionary format

	    :param dict decoded_dict
	        **REQUIRED** decoded dictionary being updated for all packets
        """
        lines = kwargs.get("lines", None)
        line_index = kwargs.get("line_num", None)
        pkt = kwargs.get("num_pkts", None)
        frame = kwargs.get("frame", None)
        decoded_dict = kwargs.get("decoded_dict", None)

        flowset = field = pdu = -1
        self.log('info', "Decoding frame# %d" %(pkt + 1))
        options_v9_inline = options_ipfix_inline = differentiator = options_imon = 0

        for line_num in range(line_index, len(lines)):
            #v9_inline = 0
            if re.search(r"Frame [0-9]+", lines[line_num]):
                break
            if re.search(r"Set [0-9]+", lines[line_num]):
	        #if line being parsed has text "Set [0-9]+",
		#copy the data to main dictionary which will be returned using _cp_flowset API
                if flowset != -1:
                    self._cp_flowset(decoded_dict, frame)
                flowset += 1
                frame['tmpl_type'] = ''
                frame['flowset'] = {}
                frame['flowset']['field'] = []
                frame['flowset']['pdu'] = []
                frame['flowset']['num_field'] = 0
                frame['flowset']['num_pdu'] = 0
                pdu = -1
                field = -1
                continue
            elif re.search(r"Field \(", lines[line_num]):
	        #if line has "Field \(", it is a template packet and keep appending the list
		#frame['flowset']['field'] with field
                field += 1
                if flowset != -1:
                    frame['flowset']['num_field'] += 1
		    #keep incrementing frame['flowset']['num_field'] everytime this condition is hit
                    frame['flowset']['field'].append({})
                pdu = -1
                continue

            if (re.search(r"Flow [0-9]+", lines[line_num])) or (re.search(r"pdu [0-9]+", \
		lines[line_num])):
	        #if it is a pdu/flow info keep appending frame['flowset']['pdu']
                pdu += 1
                if flowset != -1:
                    frame['flowset']['num_pdu'] += 1
		    #keep incrementing frame['flowset']['num_pdu'] to find number of pdu's in a particular packet
                    frame['flowset']['pdu'].append({})
                field = -1
                continue

            if (re.search(r"Pen provided", lines[line_num])) or not \
		re.search(r"\:", lines[line_num]):
                continue

            if (re.search(r"PEN: Juniper Networks, Inc. [(]2636[)]", lines[line_num])) or not \
                re.search(r"\:", lines[line_num]):
                continue


            (stype, svalue, type1, svalue1, tos) = (None, None, None, None, None)
	    #if none of the above conditions are met, split the line with ":" only once so
	    #that v6 addresses having ":" does not get split
            temp = lines[line_num].split(":")
            #if len(temp) == 1:
            #    continue
            if len(temp)+1 > 3:
                (stype, svalue) = lines[line_num].split(":", 1)
            else:
                (stype, svalue) = lines[line_num].split(":")

            match1 = re.search(r"(MPLS-Label[0-9])\s*:\s*(\d+)\s*(exp-bits)\s*:\s*(\d+)", \
		lines[line_num])
            mat2 = re.\
search(r"(MPLS-Label[0-9]):\s*(\d+)\s*(exp-bits)\s*:\s*(\d+)\s*(top-of-stack)", \
		lines[line_num])

            if match1:
                (stype, svalue, type1, svalue1) = (match1.group(1), match1.group(2), \
			match1.group(3), match1.group(4))
            if mat2:
                (stype, svalue, type1, svalue1, tos) = (mat2.group(1), \
			mat2.group(2), mat2.group(3), mat2.group(4), mat2.group(5))

            #Format the keys and values obtained after split with ":" for e.g.,IP address may occur
	    #twice, in such case, format the value to store only one
            key_type = stype.strip()
            value = svalue.strip()

            match_ip = re.search(r"(\d+.\d+.\d+.\d+)\s*\(\d+.\d+.\d+.\d+\)", value)
            match_type_temp = re.search(r".*\d = (Type)", key_type)
            match_scope_type = re.search(r"Scope (Type)", key_type)
            match_type = re.search(r".*(ICMP Type)", key_type)
            match_ethernet_type = re.search(r".*(Ethernet Type)", key_type)
            #match_time = re.search(r"\w+\s+\d+,\s\d+\s\d+:\d+:\d+\.\d+\s+\w+", value)
            match_ipv6 = re.search(r"(\w+:.*:\w+)\s*\(\w+:.*:\w+\)\s*", value)
            match_port = re.search(r"^(\d+)\s+\(\d+\)", value)
            match_fragident = re.search(r"^fragIdent", key_type)
            match_nh = re.search(r"^::\s+[(](::)[)]", value)
            match_nh2 = re.search(r"^::ffff:\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\s+[(](::ffff:\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})[)]", value)
            match_ipversion = re.search("^IPVersion", key_type)
            match_mac_addr = re.search("Mac Address", key_type)
            match_data_link_frame_section = re.search("Data Link Frame Section", key_type)
            clip_length_found =  re.search("String_len_short", key_type)  

            if clip_length_found:
                key_type = 'clip_length' 
            if value == "Unknown (368)":
                value = "ingressInterfaceType (368)"
            if value == "32767 [pen: Juniper Networks, Inc.]":
                value = "FWD_CLASS (32767)"
            if value == "32766 [pen: Juniper Networks, Inc.]":
                value = "PKT_LOSS_PRIORITY (32766)"
            if match_ip:
                value = match_ip.group(1)
            if match_ipv6:
                value = match_ipv6.group(1)
            if match_type or match_ethernet_type:
                key_type = 'Type'
                if "0x" in value:
                    value = str(int(value, 16))
            if match_type_temp:
                key_type = match_type_temp.group(1)
            if match_scope_type:
                key_type = match_scope_type.group(1)
                #key_type = match_type.group(1)
            #if match_time:
            #    value = self._convert_time_stamp_to_epoch(value)
            if match_port:
                value = match_port.group(1)
            if key_type == 'Protocol':
                match_protocol = re.search(r"^(.*)\s+[(](\d+)[)]", value)
                if match_protocol:
                    value = match_protocol.group(2)
            if match_fragident:
                key_type = 'IPv4Ident'
            if key_type == 'TCP Flags':
                match_tcp_flags = re.search(r"^0x..", value)
                if match_tcp_flags:
                    value = match_tcp_flags.group()
            if match_nh:
                value = match_nh.group(1)
            if match_nh2:
                value = match_nh2.group(1)
            if match_ipversion:
                value = str(int(value))
            if match_mac_addr:
                value = re.sub('[_]', ':', value)
            if len(temp) == 4:
                if temp[0].strip() == 'Enterprise Private entry' and temp[2].strip() == 'Value (hex bytes)':
                    jnpr_type_32767 = re.search(r'[(]Juniper Networks, Inc.[)] Type 32767',temp[1])
                    if jnpr_type_32767:
                        key_type = 'FwdClass'
                        value = ''.join([chr(int('0x{}'.format(a),16)) for a in temp[-1].strip().split()])
                    jnpr_type_32766 = re.search(r'[(]Juniper Networks, Inc.[)] Type 32766',temp[1])
                    if jnpr_type_32766:
                        key_type = 'PktLossPriority'
                        value =  temp[-1].strip()
                        if value == '00':
                            value = 'low'
                        if value == '01':
                            value = 'medium-low'
                        if value == '02':
                            value = 'medium-high'
                        if value == '03':
                            value = 'high'
                            
            if (self.mpls_over_udp) and (pdu >= 0):
                pdu_dict = frame['flowset']['pdu'][pdu]
                if key_type in pdu_dict.keys():
                    key_type = "INNER_" + key_type
            elif (self.mpls_over_udp) and (field > 0):
                field_list = frame['flowset']['field']
                for field_identifier in field_list:
                    if ('Type' in field_identifier.keys()) and value == field_identifier['Type']:
                        value = "INNER_" + value

            #categorize the type of exported packet into OPTIONS/DATA/TEMPLATE based on flowset type
            if flowset != -1:
                if re.search(r"Options FlowSet", key_type):
                    frame['flowset']['type'] = 'OPTIONS'
                    pdu = -1
                    field = -1
                elif re.search(r"Template FlowSet", key_type):
                    frame['flowset']['type'] = 'TEMPLATE'
                    pdu = -1
                    field = -1
                elif (re.search(r"Data FlowSet", key_type)) or (re.search(r"DataRecord", key_type)):
                    frame['flowset']['type'] = 'DATA'
                    pdu = -1
                    field = -1

            if flowset < 0:
                frame[key_type] = value
            elif (pdu < 0) and (field < 0):
                frame['flowset'][key_type] = value
                #if (re.search(r"Template Id", key_type)) and ((value == 323) or (value == 324)):
                    #v9_inline = 1
                #if (re.search(r"FlowSet Id", key_type)) and ((value == 323) or (value == 324)):
                    #v9_inline = 1
            elif field < 0:
	        #categorize the type of options data packet based on the value of field
                if re.search(r"Sampling algorithm", key_type):
                    frame['flowset']['type'] = frame['tmpl_type'] = 'OPTIONS_DATA'
                    frame['flowset']['opt_type'] = 'SYSTEM'
                    if re.search(r"Random sampling mode configured \(2\)", value):
                        value = str(2)
                    elif re.search(r"Random sampling \(2\)", value):
                        value = str(2)

                if re.search(r"Flow active timeout", key_type):
                    frame['flowset']['type'] = frame['tmpl_type'] = 'OPTIONS_DATA'
                    frame['flowset']['opt_type'] = 'TEMPLATE'

                if (re.search(r"Sampling interval", key_type)) or \
		    (re.search(r"Flow active timeout", key_type)) or \
		    (re.search(r"PacketsExp", key_type)) or \
		    (re.search(r"Flow inactive timeout", key_type)) or \
		    (re.search(r"FlowsExp", key_type)):
                    options_v9_inline += 1

                if (re.search(r"FlowExporter", key_type)) or \
		    (re.search(r"System Init Time", key_type)) or \
		    (re.search(r"ExporterAddr", key_type)) or \
		    (re.search(r"ExportProtocolVersion", key_type)) or \
		    (re.search(r"ExportTransportProtocol", key_type)):
                    options_ipfix_inline += 1

                if (re.search(r"Sampling interval", key_type)) or \
                    (re.search(r"FlowExporter", key_type)) and \
                    self.imon is True:
                    options_imon += 1

                if options_imon == 2:
                    frame['flowset']['type'] = frame['tmpl_type'] = 'OPTIONS_DATA'

                if options_v9_inline == 5:
                    frame['flowset']['type'] = frame['tmpl_type'] = 'OPTIONS_DATA_V9_INLINE'
                    frame['flowset']['opt_type'] = 'SYSTEM'

                #if v9_inline == 1:
                    #self.log('debug', 'type is v9_inline')

                if options_ipfix_inline == 6:
                    frame['flowset']['type'] = frame['tmpl_type'] = 'OPTIONS_DATA_IPFIX_INLINE'
                    frame['flowset']['opt_type'] = 'SYSTEM'

                if (re.search(r"ExporterAddr", key_type)) and (differentiator == 0):
                    key_type += "v4"
                    frame['flowset']['pdu'][pdu][key_type] = value
                    differentiator += 1
                else:
                    imon_decoded_dict = {}
                    if match_data_link_frame_section:
                        value = self._get_data_link_frame_section(frame['frame_index'])
                        imon_decoded_dict = self._decode_imon_frame_section(value)
                        for imon_field in imon_decoded_dict.keys():
                            frame['flowset']['pdu'][pdu][imon_field] = imon_decoded_dict[imon_field]

                    frame['flowset']['pdu'][pdu][key_type] = value
                    if svalue1 is not None:
                        frame['flowset']['pdu'][pdu][key_type + "-" + type1] = svalue1
                    if tos is not None:
                        frame['flowset']['pdu'][pdu][key_type + "-" + tos] = 1

            elif pdu < 0:
                frame['flowset']['field'][field][key_type] = value
                if re.search(r"SAMPLING_ALGORITHM", value):
                    frame['tmpl_type'] = 'OPTIONS'
                    frame['flowset']['opt_type'] = 'SYSTEM'

                if re.search(r"FLOW_ACTIVE_TIMEOUT", value):
                    frame['tmpl_type'] = 'OPTIONS'
                    frame['flowset']['opt_type'] = 'TEMPLATE'

                if re.search(r"FLOW_EXPORTER", value):
                    frame['tmpl_type'] = frame['flowset']['type'] = 'OPTIONS_IPFIX_INLINE'
                    frame['flowset']['opt_type'] = 'SYSTEM'

                if (re.search(r"FLOW_ACTIVE_TIMEOUT", value)) and \
                (re.search(r"583|580|576|579|577|582|578", \
		frame['flowset']['Template Id'])):
                    frame['tmpl_type'] = frame['flowset']['type'] = 'OPTIONS_V9_INLINE'
                    frame['flowset']['opt_type'] = 'SYSTEM'

                if re.search(r"IP_SRC_ADDR", value):
                    frame['tmpl_type'] += 'ipv4'
                elif re.search(r"IPV6_SRC_ADDR", value):
                    frame['tmpl_type'] += 'ipv6'
                elif re.search(r"MPLS_LABEL_1", value):
                    frame['tmpl_type'] += 'mpls'
                elif re.search(r"DESTINATION_MAC", value):
                    frame['tmpl_type'] += 'vpls'

                if re.search(r"flowStart", value):
                    frame['tmpl_type'] += '-inline'
                if ('Template Id' in frame['flowset'].keys()) and \
		    re.search(r"32[34]", frame['flowset']['Template Id']) and not \
		    re.search(r"v9inline", frame['tmpl_type']):
                    frame['tmpl_type'] += 'v9inline'
                if ('FlowSet Id' in frame['flowset'].keys()) and \
		    re.search(r"32[34]", frame['flowset']['FlowSet Id']) and not \
		    re.search(r"v9inline", frame['tmpl_type']):
                    frame['tmpl_type'] += 'v9inline'
            self.log('debug', 'end %d' %line_num)


        if flowset == -1:
            raise Exception('No flowset found in Frame %s' %pkt)
        else:
            self._cp_flowset(decoded_dict, frame)

        #$v->{FRAMES}->[$pkt]->{num_flowset} = $flowset + 1;
        #$line_num--

        return line_index

    def _cp_flowset(self, decoded_dict, frame):
        """
            This method updtates the dictionary with flowset details.

            Copies the flow set to the dictionary. It also builds the dictionary based on the
            flow_selectors list which was parsed.

	    :param dict decoded_dict
	        **REQUIRED** decoded dictionary being updated for all packets

	    :param dic frame
	        **REQUIRED** decoded fram in dictionary format
        """
        self.log('info', 'going to copy the flowsets from frame into global variable')
        flow_selectors = self.flow_selectors

        fss = frame['flowset']
	#create a dictionary 'fss' so that, any updates to this dictionary will
	#update frame['flowset']
        col_ip = frame['ip']['dst_ip']
        tmpl_id = None
        domain_id = None

        #store domain_id based on the values in frame
        if 'Observation Domain Id' in frame.keys():
            domain_id = frame['Observation Domain Id']
        elif 'SourceId' in frame.keys():
            domain_id = frame['SourceId']

        #store template ID value based on the values in fss
        if 'Template Id' in fss.keys():
            tmpl_id = fss['Template Id']
        elif 'DataRecord (Template Id)' in fss.keys():
            tmpl_id = fss['DataRecord (Template Id)']
        elif 'Data FlowSet (Template Id)' in fss.keys():
            tmpl_id = fss['Data FlowSet (Template Id)']


        if 'type' in fss.keys():
            fs_type = fss['type']
        else:
            fs_type = None

        if 'FlowSet Id' in fss.keys():
            fs_id = fss['FlowSet Id']
        else:
            fs_id = None

        #categorize the frames into TEMPLATE/OPTIONS/DATA types based on value of fs_type
        if (fs_type is None) and (fs_id is not None):
            if re.search(r"Data Template", fs_id):
                fs_type = 'TEMPLATE'
            elif re.search(r"Options Template", fs_id):
                fs_type = 'OPTIONS'
            match_fs = re.search(r"\(Data\) \((\d+)\)", fs_id)
            if match_fs:
                fs_type = 'DATA'
                if tmpl_id is None:
                    tmpl_id = match_fs.group(1)

        if (tmpl_id is None) and (fs_id is not None):
            match_fs = re.search(r"\(Data\) \((\d+)\)", fs_id)
            if match_fs:
                tmpl_id = match_fs.group(1)

        if (tmpl_id is None) and (fs_type is None):
            #self.log('error', 'unable to determine PDU type or template ID for this frame')
            raise Exception('unable to determine PDU type or template ID')

        #update frame['tmpl_type'] with appropriate family type and jflow type info
        if re.search(r"mpls-inline", frame['tmpl_type']):
            frame['tmpl_type'] = 'inline-mpls'
        elif re.search(r"mplsipv4-inline", frame['tmpl_type']):
            frame['tmpl_type'] = 'inline-mpls-ipv4'
        elif re.search(r"mpls-v9inlineipv4", frame['tmpl_type']):
            frame['tmpl_type'] = 'v9inline-mpls-ipv4'
        elif re.search(r"v9inline-mpls", frame['tmpl_type']):
            frame['tmpl_type'] = 'v9inline-mpls'
        elif re.search(r"ipv6", frame['tmpl_type']):
            frame['tmpl_type'] = 'inline-ipv6'
        elif re.search(r"vpls", frame['tmpl_type']):
            frame['tmpl_type'] = 'inline-vpls'
        elif re.search(r"ipv4", frame['tmpl_type']):
            if re.search(r"mpls", frame['tmpl_type']):
                frame['tmpl_type'] = 'mpls-ipv4'
            elif re.search(r"inline", frame['tmpl_type']):
                frame['tmpl_type'] = 'inline-ipv4'

        self.log('info', 'Template type for frame %s is %s' %(frame['frame_index'], \
	    frame['tmpl_type']))
        tmpl_type = frame['tmpl_type'] if 'tmpl_type' in frame.keys() else None

        #create the dictionary hierarchy var['FLOWS'][col_ip][domain_id][tmpl_id]
        if 'FLOWS' not in decoded_dict.keys():
            decoded_dict['FLOWS'] = {}
        if col_ip not in decoded_dict['FLOWS'].keys():
            decoded_dict['FLOWS'][col_ip] = {}
        if domain_id not in decoded_dict['FLOWS'][col_ip].keys():
            decoded_dict['FLOWS'][col_ip][domain_id] = {}
        if tmpl_id not in decoded_dict['FLOWS'][col_ip][domain_id].keys():
            decoded_dict['FLOWS'][col_ip][domain_id][tmpl_id] = {}

        if tmpl_type is not None:
            self.log('info', 'Template Type of template "\
            "id, %s is %s' %(tmpl_id, frame['tmpl_type']))
            decoded_dict['FLOWS'][col_ip][domain_id][tmpl_id]['tmpl_type'] = frame['tmpl_type']

        del frame['tmpl_type']

        bkt = decoded_dict['FLOWS'][col_ip][domain_id]
	#create a dictionary 'bkt' so that, any updated to
	#'bkt' will update decoded_dict['FLOWS'][col_ip][domain_id]
        num_flow = "num_flowsets_" + fs_type

        num_flowsets = bkt[tmpl_id][num_flow] if num_flow in bkt[tmpl_id].keys() else 0

        if re.search(r"DATA", fs_type) and not re.search(r"OPTIONS_DATA", fs_type):
            if fs_type not in bkt[tmpl_id].keys():
                bkt[tmpl_id][fs_type] = {}
            if len(flow_selectors) == 0 or flow_selectors is None:
	        #if nothing is parsed to flow_selectors, initialize this list to
		#default using _get_flow_keys API
                flow_selectors = self._get_flow_keys(tmpl_id)

            #this piece of code builds the dictionary in the
	    #hierarch of flow_selectot fields which were parsed
            temp_dict = bkt[tmpl_id][fs_type]
            for pdu_index in range(len(frame['flowset']['pdu'])):
                pdu_data = copy.deepcopy(frame['flowset']['pdu'][0])
                del frame['flowset']['pdu'][0]
                pdu_dict = temp_dict
                for selector in flow_selectors:
                    if selector in pdu_data.keys():
                        if pdu_data[selector] not in pdu_dict:
                            pdu_dict[pdu_data[selector]] = {}
                            if selector == flow_selectors[-1]:
                                temp_frame = copy.deepcopy(frame)
                                del temp_frame['flowset']['pdu']
                                temp_frame['flowset']['pdu'] = copy.deepcopy(pdu_data)
                                if self.append_data_to_list is True:
                                    if isinstance(pdu_dict[pdu_data[selector]], list):
                                        pdu_dict[pdu_data[selector]].append(copy.deepcopy(temp_frame))
                                    else:
                                        del pdu_dict[pdu_data[selector]]
                                        pdu_dict[pdu_data[selector]] = []
                                        pdu_dict[pdu_data[selector]].append(copy.deepcopy(temp_frame))
                                else:
                                    pdu_dict[pdu_data[selector]] = copy.deepcopy(temp_frame)
                        else:
                            if selector == flow_selectors[-1]:
                                temp_frame = copy.deepcopy(frame)
                                del temp_frame['flowset']['pdu']
                                temp_frame['flowset']['pdu'] = copy.deepcopy(pdu_data)
                                if self.append_data_to_list is True:
                                    if isinstance(pdu_dict[pdu_data[selector]], list):
                                        pdu_dict[pdu_data[selector]].append(copy.deepcopy(temp_frame))
                                    else:
                                        del pdu_dict[pdu_data[selector]]
                                        pdu_dict[pdu_data[selector]] = []
                                        pdu_dict[pdu_data[selector]].append(copy.deepcopy(temp_frame))
                                else:
                                    pdu_dict[pdu_data[selector]] = copy.deepcopy(temp_frame)
                        pdu_dict = pdu_dict[pdu_data[selector]]
                    elif selector in frame.keys():
                        if frame[selector] not in pdu_dict:
                            pdu_dict[frame[selector]] = {}
                            if selector == flow_selectors[-1]:
                                temp_frame = copy.deepcopy(frame)
                                del temp_frame['flowset']['pdu']
                                temp_frame['flowset']['pdu'] = copy.deepcopy(pdu_data)
                                if self.append_data_to_list is True:
                                    if isinstance(pdu_dict[pdu_data[selector]], list):
                                        pdu_dict[pdu_data[selector]].append(copy.deepcopy(temp_frame))
                                    else:
                                        del pdu_dict[pdu_data[selector]]
                                        pdu_dict[pdu_data[selector]] = []
                                        pdu_dict[pdu_data[selector]].append(copy.deepcopy(temp_frame))
                                else:
                                    pdu_dict[pdu_data[selector]] = copy.deepcopy(temp_frame)
                        else:
                            if selector == flow_selectors[-1]:
                                temp_frame = copy.deepcopy(frame)
                                del temp_frame['flowset']['pdu']
                                temp_frame['flowset']['pdu'] = copy.deepcopy(pdu_data)
                                if self.append_data_to_list is True:
                                    if isinstance(pdu_dict[pdu_data[selector]], list):
                                        pdu_dict[pdu_data[selector]].append(copy.deepcopy(temp_frame))
                                    else:
                                        del pdu_dict[pdu_data[selector]]
                                        pdu_dict[pdu_data[selector]] = []
                                        pdu_dict[pdu_data[selector]].append(copy.deepcopy(temp_frame))
                                else:
                                    pdu_dict[pdu_data[selector]] = copy.deepcopy(temp_frame)
                        pdu_dict = pdu_dict[frame[selector]]
                    elif (selector not in frame.keys()) and (selector not in pdu_data.keys()):
                        raise Exception("%s not found in keys of frame as well as pdu, \
			    please make sure the string being parsed is correct for pdu_index %s" %(selector, pdu_index))
        else:
            if fs_type not in bkt[tmpl_id].keys():
                bkt[tmpl_id][fs_type] = []

            bkt[tmpl_id][fs_type].append({})

            bkt[tmpl_id][fs_type][num_flowsets] = copy.deepcopy(frame)

        num_flowsets += 1
        bkt[tmpl_id][num_flow] = num_flowsets

        #return True

    def _get_flow_keys(self, tmpl_id):
        """
	    This method returns the list of flow selector fields to be used

            This method is called when flow_selectors was parsed as an empty list.
            The script identifies the template id and parses the template id to this
            method. The flow_selectors list will be returned by this method based on
            the value of the template id.

	    :param str tmpl_id
	        **REQUIRED** template id of a particular export packet

	    :return: list of flow selector fields
        """
        tmpl_id = int(tmpl_id)
        print("device handle: ", self.device)
        if self.imon is True:
            return ['SrcAddr']
        elif (tmpl_id == 256) or (tmpl_id == 257) or (tmpl_id == 320) or (tmpl_id == 321):
            return ['SrcAddr', 'DstAddr', 'SrcPort', 'DstPort']
        elif (tmpl_id == 260) or (tmpl_id == 324):
            return ['SrcAddr', 'DstAddr', 'MPLS-Label1', 'MPLS-Label2', 'MPLS-Label3']
        elif (tmpl_id == 258) or (tmpl_id == 322):
            return ['Source Mac Address', 'Destination Mac Address']
        elif (tmpl_id == 259) or (tmpl_id == 323):
            return ['MPLS-Label1', 'MPLS-Label2', 'MPLS-Label3']

    def _convert_time_stamp_to_epoch(self, time_stamp):
        """
            This method converts human readable date to epoch time

            The script itself identifies any timestamps in the decoded dump and parses the
            timestamp to this method. This method converts this timestamp to epoch and returns
            the epoch time.

            :param str time_stamp
                **REQUIRED** human readable time stamp

            :return: epoch time/unix time
        """
        device = self.device
        cmd = "date +%s -d \"" + time_stamp + "\""
        response = device.shell(command=cmd)
        match_response = re.search(r"\w+\s+(\d+).*", response.response())

        if match_response:
            timestamp = match_response.group(1)
        return str(int(timestamp))

    def start_tcp_dump_at_collector(self, **kwarg):
        """
        This method will start the tcpdump at colelctor and will
        also find the epoch time at router to approximately know the
        tcpdump start time with reference to router where sampling
        is applied

        :param: obj device
            **REQUIRED** Collector handle

        :param: string tcpdump_file
            **REQUIRED** pcap file name

        :param: string tcpdump_decode_file
            **REQUIRED** tshark decoded file name

        :param: string protocol
            **REQUIRED** To capture packets relevant to protocol

        :param: string cflow_port
            **REQUIRED** port number at which collector is receiving the
                         exported packets

        :param: string interface
             **REQUIRED** Interface needed to start tcpdump capturing process

        :param: string size
            **OPTIONAL** maximum packets size to be captured in tcpdump process

        :param obj router_handle
            **OPTIONAL** Router handle to know the epoch time with
                         refrence to tcpdump process started on collector
                         It will be useful for varifying export time on
                         flow templates and data records.

        :return: None
        """
        if self.oops_call is False:
            size = kwarg.get('size', '2000')
            if "device" in kwarg:
                device = kwarg['device']
            if "tcpdump_file" in kwarg:
                tcpdump_file = kwarg['tcpdump_file']
            if "tcpdump_decode_file" in kwarg:
                tcpdump_decode_file = kwarg['tcpdump_decode_file']
            if "protocol" in kwarg:
                protocol = kwarg['protocol']
            if "cflow_port" in kwarg:
                cflow_port = kwarg['cflow_port']
            if "interface" in kwarg:
                interface = kwarg['interface']
            kill_earlier_process = kwarg.get('kill_earlier_process', True)
            if kill_earlier_process is True:
                device.shell(command="killall -INT tcpdump")
            device.shell(command="rm -rf %s %s"%(tcpdump_file, tcpdump_decode_file))
            if 'router_handle' in kwarg:
                rhh = kwarg['router_handle']
                self.time_before_tcpdump_started = \
                    str(int(rhh.shell(command="date +%s").\
response().replace('\r\n', '\n').strip()) +5)
            device.shell(command="tcpdump -x -i %s -s %s -w %s %s port %s &"%\
               (interface, size, tcpdump_file, protocol, cflow_port))
        if self.oops_call is True:
            if self.kill_earlier_process == 'True':
                self.device.shell(command="killall -INT tcpdump")
            self.device.shell(command="rm -rf %s %s"%(self.tcpdump_file, self.tcpdump_decode_file))
            if self.rh_handle_passed is True:
                print("\n Router Handle recieved \n")
                self.time_before_tcpdump_started = \
                    str(int(self.rhh.shell(command="date +%s").\
response().replace('\r\n', '\n').strip()) +5)
            self.device.shell(command="tcpdump -x -i %s -s %s -w %s %s port %s &"%\
               (self.interface, self.size, self.tcpdump_file, self.protocol, self.cflow_port))

    def stop_tcp_dump_at_collector(self, **kwarg):
        """
        This method will stop the tcpdump at collector and will
        also find the epoch time at router to approximately know the
        tcpdump stop time with reference to router where sampling
        is applied.

        :param obj router_handle
            **OPTIONAL** Router handle to know the epoch time with
                         refrence to tcpdump process stopped on collector
                         It will be useful for varifying export time on
                         flow templates and data records.

        :return: None

        """
        if self.oops_call is False:
            device = kwarg['device']
            device.shell(command="killall -INT tcpdump")
            if self.time_before_tcpdump_started is not None:
                if 'router_handle' in kwarg:
                    rhh = kwarg['router_handle']
                    self.time_after_tcpdump_stopped = \
                    str(int(rhh.shell(command="date +%s").\
response().replace('\r\n', '\n').strip()) -5)
        if self.oops_call is True:
            self.device.shell(command="killall -INT tcpdump")
            if self.time_before_tcpdump_started is not None:
                if self.rh_handle_passed is True:
                    print("\n Router Handle recieved \n")
                    self.time_after_tcpdump_stopped = \
                    str(int(self.rhh.shell(command="date +%s").\
response().replace('\r\n', '\n').strip()) -5)


    def get_tshark_output(self):
        """
        This method will return the tshark decoded output.

        :return: Tshark decoded output
        """
        return self.tshark_output

    def get_tcpdump_start_and_end_time(self):
        """
        This  method will return the tcpdump start and stop time
        calculated on router where sampling is enabled

        :return: tuple containg time_before_tcpdump_started and
                     time_after_tcpdump_stopped
        """
        return (self.time_before_tcpdump_started, self.time_after_tcpdump_stopped)

    def create_instance(self, **kwargs):
        """ Method to create instances of \
            decode_jflow_dump.py.
        """
        self.objj = decode_jflow_dump()
        self.objj.init(**kwargs)
        return self.objj

    def start_jflow_decoding_threads(self, *obj_list):
        """ Starts multiple threads to decode the pcap in \
            python dictionary.
        """
        self.thr = []
        t.set_background_logger()
        for obj in obj_list:
            self.thr.append(decode_thread(object_reference=obj, process_type='decode_pcap'))
        for thread in self.thr:
            thread.start()
        for thread in self.thr:
            thread.join()
        t.process_background_logger()

    def start_tcpdump_threads(self, *obj_list):
        """ Starts multiple threads to start tcpdump at collector """
        self.thr = []
        t.set_background_logger()
        for obj in obj_list:
            self.thr.append(decode_thread(object_reference=obj, process_type='start_tcpdump'))
        for thread in self.thr:
            thread.start()
        for thread in self.thr:
            thread.join()
        t.process_background_logger()

    def stop_tcpdump_threads(self, *obj_list):
        """ Starts multiple threads to stop tcpdump at collector """
        self.thr = []
        t.set_background_logger()
        for obj in obj_list:
            self.thr.append(decode_thread(object_reference=obj, process_type='stop_tcpdump'))
        for thread in self.thr:
            thread.start()
        for thread in self.thr:
            thread.join()
        t.process_background_logger()

    def _get_data_link_frame_section(self, frame_index):
        """
        Returns the value of Data Link Frame Section field for Imon
        """
        json_frame_dict = self.decoded_json[frame_index-1]
        frame_section = list(self._extract_value_of_key(json_frame_dict, "cflow.data_link_frame_section"))
        return frame_section[0]

    def _extract_value_of_key(self, var, key):
        """
        Returns the value of a particular key from a nested dictionary
        """
        ret_value = None
        if isinstance(var, dict):
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, (dict, list)):
                    yield from self._extract_value_of_key(v, key)
        elif isinstance(var, list):
            for d in var:
                yield from self._extract_value_of_key(d, key)

    def _decode_imon_frame_section(self, frame_section):
        """
        Decodes the data link frame section
        """
        data = frame_section.split(":")
        data_in_hex = ''.join(data)
        hex_size = len(data_in_hex)*4
        data_in_bin = str(bin(int(data_in_hex, 16)))
        data_in_bin = data_in_bin[2:len(data_in_bin)]
        data_in_bin = data_in_bin.zfill(hex_size)
        decoded_frame = {}
        if self.imon_decode_template is not None:
            decode_template = self.imon_decode_template
        else:
            if self.imon_decode_type == 'v4_v6_udp':
                ether_type = int(data_in_bin[96:112], 2)
                if ether_type == 2048:
                    decode_template = self._get_imon_decode_template('ipv4_udp')
                elif ether_type == 34525:
                    decode_template = self._get_imon_decode_template('ipv6_udp')
            else:
                decode_template = self._get_imon_decode_template(self.imon_decode_type)

        for field in decode_template.keys():
            offset = int(decode_template[field]["Offset"])
            size = None
            value = None
            if field == "Payload":
                value = data_in_bin[offset:len(data_in_bin)]
            else:
                size = offset+int(decode_template[field]["Size"])
                value = data_in_bin[offset:size]

            if "Type" not in decode_template[field].keys():
                value = str(int(value, 2))
            elif decode_template[field]["Type"] == "Mac":
                mac_size = int(len(value)/4)
                value = str(hex(int(value,2)))
                value = value[2:len(value)].zfill(mac_size)
                value = value[0:2]+":"+value[2:4]+":"+value[4:6]+":"+value[6:8]+":"+ \
                        value[8:10]+":"+value[10:12]
            elif decode_template[field]["Type"] == "Hex":
                value = str(hex(int(value, 2)))
            elif decode_template[field]["Type"] == "Bin":
                value = value
            elif decode_template[field]["Type"] == "IPv4":
                value = str(int(value[0:8], 2)) + "." + str(int(value[8:16], 2)) + \
                        "." + str(int(value[16:24], 2)) + "." + str(int(value[24:32], 2))
            elif decode_template[field]["Type"] == "IPv6":
                addr_size = int(len(value)/4)
                value = str(hex(int(value,2)))
                value = value[2:len(value)].zfill(addr_size)
                value = value[0:4]+":"+value[4:8]+":"+value[8:12]+":"+value[12:16]+ \
                        ":"+value[16:20]+":"+value[20:24]+":"+value[24:28]+":"+value[28:32]
                value = str(ipaddress.IPv6Address(value))
            decoded_frame[field] = value

        return decoded_frame

    def _get_imon_decode_template(self, decode_type):
        """
        Returns the dictionary with respect to which IMON Data Link Frame will be decoded
        """
        template = {}
        if decode_type == 'ipv4_udp':
            template = { "Destination Mac Address": {"Offset": "0", "Size": "48", "Type": "Mac"},
                         "Source Mac Address": {"Offset": "48", "Size": "48", "Type": "Mac"},
                         "Ether Type": {"Offset": "96", "Size": "16", "Type": "Hex"},
                         "IP Version": {"Offset": "112", "Size": "4"},
                         "IP Header Length": {"Offset": "116", "Size": "4"},
                         "IP TOS": {"Offset": "120", "Size": "8", "Type": "Hex"},
                         "IP Total Length": {"Offset": "128", "Size": "16"},
                         "IP Identification": {"Offset": "144", "Size": "16", "Type": "Hex"},
                         "IP Flags": {"Offset": "160", "Size": "3", "Type": "Bin"},
                         "IP Fragmentation Offset": {"Offset": "163", "Size": "13", "Type": "Hex"},
                         "IP TTL": {"Offset": "176", "Size": "8"},
                         "Protocol": {"Offset": "184", "Size": "8"},
                         "IP Header Checksum": {"Offset": "192", "Size": "16", "Type": "Hex"},
                         "SrcAddr": {"Offset": "208", "Size": "32", "Type": "IPv4"},
                         "DstAddr": {"Offset": "240", "Size": "32", "Type": "IPv4"},
                         "SrcPort": {"Offset": "272", "Size": "16"},
                         "DstPort": {"Offset": "288", "Size": "16"},
                         "UDP Length": {"Offset": "304", "Size": "16"},
                         "UDP Checksum": {"Offset": "320", "Size": "16", "Type": "Hex"},
                         "Payload": {"Offset": "336", "Type": "Hex"}
                         }
        elif decode_type == 'ipv6_udp':
            template = { "Destination Mac Address": {"Offset": "0", "Size": "48", "Type": "Mac"},
                         "Source Mac Address": {"Offset": "48", "Size": "48", "Type": "Mac"},
                         "Ether Type": {"Offset": "96", "Size": "16", "Type": "Hex"},
                         "IP Version": {"Offset": "112", "Size": "4"},
                         "Traffic Class": {"Offset": "116", "Size": "8", "Type": "Hex"},
                         "Flow Label": {"Offset": "124", "Size": "20", "Type": "Hex"},
                         "Payload Length": {"Offset": "144", "Size": "16"},
                         "Next Header": {"Offset": "160", "Size": "8"},
                         "Hop Limit": {"Offset": "168", "Size": "8"},
                         "SrcAddr": {"Offset": "176", "Size": "128", "Type": "IPv6"},
                         "DstAddr": {"Offset": "304", "Size": "128", "Type": "IPv6"},
                         "SrcPort": {"Offset": "432", "Size": "16"},
                         "DstPort": {"Offset": "448", "Size": "16"},
                         "UDP Length": {"Offset": "464", "Size": "16"},
                         "UDP Checksum": {"Offset": "480", "Size": "16", "Type": "Hex"},
                         "Payload": {"Offset": "496", "Type": "Hex"}
                         }
        return template


class decode_thread(threading.Thread):
    """ Class for multi-threading action for the methods \
        present in decode_jflow_dump.py.
    """
    def __init__(self, **kwargs):
        """ Initializing the constructor """
        threading.Thread.__init__(self)
        self.obj = kwargs['object_reference']
        self.process_type = kwargs['process_type']

    def run(self):
        """ Method to run the threads """
        if self.process_type == 'decode_pcap':
            self.obj.decode_jflow_dump_on_collector()
        if self.process_type == 'start_tcpdump':
            self.obj.start_tcp_dump_at_collector()
        if self.process_type == 'stop_tcpdump':
            self.obj.stop_tcp_dump_at_collector()


#class instances(object):
#    """ Class to instantiate object of \
#        decode_jflow_dump.py as well as \
#        initiating the multi-threads execution for \
#        starting tcpdump, stopping tcpdump and \
#        decoding the pcap in tshark output/python dictionary.
#    """
#    def __init__(self):
#        """ Initializing constructor """
#        self.objj = None
#        self.thr = None
#    def create_instance(self, **kwargs):
#        """ Method to create instances of \
#            decode_jflow_dump.py.
#        """
#        self.objj = decode_jflow_dump()
#        self.objj.init(**kwargs)
#        return self.objj
#    #def sequence_call(self, *obj_list):
#    #    """ xxxxxxx """
#    #    print("thread list :", obj_list)
#    #    for i in obj_list:
#    #        i.decode_jflow_dump_on_collector()
#    def start_jflow_decoding_threads(self, *obj_list):
#        """ Starts multiple threads to decode the pcap in \
#            python dictionary.
#        """
#        self.thr = []
#        t.set_background_logger()
#        for obj in obj_list:
#            self.thr.append(decode_thread(object_reference=obj, process_type='decode_pcap'))
#        for thread in self.thr:
#            thread.start()
#        for thread in self.thr:
#            thread.join()
#        t.process_background_logger()
#    def start_tcpdump_threads(self, *obj_list):
#        """ Starts multiple threads to start tcpdump at collector """
#        self.thr = []
#        t.set_background_logger()
#        for obj in obj_list:
#            self.thr.append(decode_thread(object_reference=obj, process_type='start_tcpdump'))
#        for thread in self.thr:
#            thread.start()
#        for thread in self.thr:
#            thread.join()
#        t.process_background_logger()
#    def stop_tcpdump_threads(self, *obj_list):
#        """ Starts multiple threads to stop tcpdump at collector """
#        self.thr = []
#        t.set_background_logger()
#        for obj in obj_list:
#            self.thr.append(decode_thread(object_reference=obj, process_type='stop_tcpdump'))
#        for thread in self.thr:
#            thread.start()
#        for thread in self.thr:
#            thread.join()
#        t.process_background_logger()

