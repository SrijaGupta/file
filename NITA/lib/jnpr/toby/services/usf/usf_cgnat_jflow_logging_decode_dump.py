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
from jnpr.toby.services import utils

class usf_cgnat_jflow_logging_decode_dump(object):
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
        self.oops_call = True
        if self.device is None:
            raise ValueError("device handle is mandatory argument")
        if self.tethereal is None:
            raise ValueError("Path for tshark is Mandatory argument")
        if "router_handle" in kwargs:
            self.rhh = kwargs['router_handle']
            self.rh_handle_passed = True
        else:
            self.rh_handle_passed = False
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

        #return self._parse_jflow_tethereal_verbose()
        self._parse_jflow_tethereal_verbose()

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
            match_udp = re.search(r"User Datagram Protocol, Src Port: (?P<src_port>[0-9|a-z]+).*Dst Port: \
                    [0-9|a-z]+ \((?P<dst_port>[0-9]+)\)", lines[line_num])
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


            #Format the keys and values obtained after split with ":" for e.g.,IP address may occur
	    #twice, in such case, format the value to store only one
            key_type = stype.strip()
            value = svalue.strip()

            match_ip = re.search(r"(\d+.\d+.\d+.\d+)\s*\(\d+.\d+.\d+.\d+\)", value)
            match_type_temp = re.search(r".*\d = (Type)", key_type)
            match_ipv6 = re.search(r"(\w+:.*:\w+)\s*\(\w+:.*:\w+\)\s*", value)
            match_port = re.search(r"^(\d+)\s+\(\d+\)", value)
            if match_ip:
                value = match_ip.group(1)
            if match_ipv6:
                value = match_ipv6.group(1)
            if match_port:
                value = match_port.group(1)
            if match_type_temp:
                key_type = match_type_temp.group(1)
            if key_type == 'Protocol':
                match_protocol = re.search(r"^(.*)\s+[(](\d+)[)]", value)
                if match_protocol:
                    value = match_protocol.group(2)
            if key_type == 'Nat Event':
                match_event = re.search(r"\w+.*\s+\((\d+)\)", value)
                if match_event:
                    value = match_event.group(1)

            #categorize the type of exported packet into OPTIONS/DATA/TEMPLATE based on flowset type
            if flowset != -1:
                if re.search(r"Template FlowSet", key_type):
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
                frame['flowset']['pdu'][pdu][key_type] = value
                if svalue1 is not None:
                    frame['flowset']['pdu'][pdu][key_type + "-" + type1] = svalue1
                if tos is not None:
                    frame['flowset']['pdu'][pdu][key_type + "-" + tos] = 1
            elif pdu < 0:
                frame['flowset']['field'][field][key_type] = value
                if re.search(r"natEvent", value):
                    frame['tmpl_type'] += 'nat_logging'
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

        if re.search(r"DATA", fs_type):
            if fs_type not in bkt[tmpl_id].keys():
                bkt[tmpl_id][fs_type] = {}
            if len(flow_selectors) == 0 or flow_selectors is None:
	        #if nothing is parsed to flow_selectors, initialize this list to
                flow_selectors = ['Nat Event']

            #this piece of code builds the dictionary in the
	    #hierarch of flow_selectot fields which were parsed
            temp_dict = bkt[tmpl_id][fs_type]
            for pdu_index in range(len(frame['flowset']['pdu'])):
                pdu_data = copy.deepcopy(frame['flowset']['pdu'][0])
                del frame['flowset']['pdu'][0]
                pdu_dict = temp_dict
                #import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
                for selector in flow_selectors:
                    if selector in pdu_data.keys():
                        if pdu_data[selector] not in pdu_dict:
                            pdu_dict[pdu_data[selector]] = {}
                            if selector == flow_selectors[-1]:
                                temp_frame = copy.deepcopy(frame)
                                del temp_frame['flowset']['pdu']
                                temp_frame['flowset']['pdu'] = copy.deepcopy(pdu_data)
                                pdu_dict[pdu_data[selector]] = copy.deepcopy(temp_frame)
                        pdu_dict = pdu_dict[pdu_data[selector]]
                    elif selector in frame.keys():
                        if frame[selector] not in pdu_dict:
                            pdu_dict[frame[selector]] = {}
                            if selector == flow_selectors[-1]:
                                temp_frame = copy.deepcopy(frame)
                                del temp_frame['flowset']['pdu']
                                temp_frame['flowset']['pdu'] = copy.deepcopy(pdu_data)
                                pdu_dict[frame[selector]] = copy.deepcopy(temp_frame)
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
        self.objj = usf_cgnat_jflow_logging_decode_dump()
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
