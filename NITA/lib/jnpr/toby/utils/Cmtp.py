"""
Copyright (C) 2016-2017, Juniper Networks, Inc.
All rights reserved.
Authors:

Description:
    Toby Sflow test suite
"""

import re
import pprint

def sflow_agent_dict_filtered(sfile, agent_id, sip_pat, dip_pat, ver, num=1):
    """
    Parameters to get interested sampled flows identified by agent_id, source ip and destination ip
    :params sfile:
            **REQUIRED**  sflow records from sflow server
    :params agent_id:
            **REQUIRED**  configured sflow agent_id
    :params sip_pat:
            **REQUIRED**  sampled stream's source ip address
    :params dip_pat:
            **REQUIRED**  sampled stream's destination ip address
    :params ver:
            **REQUIRED**  ip version. 4 for ipv4 or 6 for ipv6
    :params n:
            **OPTIONAL**  maximum number of sflow samples to be tested. default is one
    """

    lines = sfile.split('\n')
    bld_start = 0
    flow = []
    rcd = {}
    i = 0
    sflow_agent = ''
    for line in lines:
        srcd = line.split(' ')
        if srcd[0] == 'agent':
            sflow_agent = srcd[len(srcd)-1].strip()
        if bld_start == 1:
            rcd[srcd[0]] = srcd[len(srcd)-1].strip()
        if srcd[0] == 'startSample':
            bld_start = 1
            rcd[srcd[0]] = srcd[len(srcd)-1].strip()
        elif srcd[0] == 'endSample':
            bld_start = 0
            #only insert into flow array if pattern matched
            if ver == '4':
                if 'srcIP' in rcd and 'dstIP' in rcd:
                    if re.match(agent_id, sflow_agent) and re.match(sip_pat, rcd['srcIP']) and re.match(dip_pat, rcd['dstIP']):
                        if 'IPProtocol' in rcd and rcd['IPProtocol'] == '47':
                            rcd['pkt_type'] = 'gre'
                        elif 'Label1_label' in rcd:
                            if rcd['Label1_label'] == '3': #uhp
                                rcd['pkt_type'] = 'mpls_label_3'
                            else:
                                rcd['pkt_type'] = 'mpls_label'
                        else:
                            rcd['pkt_type'] = 'ip4'
                        rcd['agent'] = sflow_agent
                        flow.append(rcd)
                        #for k in rcd:
                        #    print str(i) + " :: " + k + ": " + rcd[k]
                        i = i + 1
                        if i >= int(num):
                            break
            elif ver == '6':
                if 'srcIP6' in rcd and 'dstIP6' in rcd:
                    if re.match(agent_id, sflow_agent) and re.match(sip_pat, rcd['srcIP6']) and re.match(dip_pat, rcd['dstIP6']):
                        if 'Label1_label' in rcd:
                            if rcd['Label1_label'] == '2':
                                rcd['pkt_type'] = 'mpls_label_2'
                            elif rcd['Label1_label'] == '3' and 'Label2_label' in rcd and rcd['Label2_label'] == '2': #uhp
                                rcd['pkt_type'] = 'mpls_label_3_2'
                            else:
                                rcd['pkt_type'] = 'mpls_label'
                        else:
                            rcd['pkt_type'] = 'ip6'
                        rcd['agent'] = sflow_agent
                        flow.append(rcd)
                        #for k in rcd:
                        #    print str(i) + " :: " + k + ": " + rcd[k]
                        i = i + 1
                        if i >= int(num):
                            break
            else:
                #throw an exception
                raise ValueError("ver can be either 4 or 6")
            rcd = {}

    return flow

def rfprint(data, new_width=1):
    """
    Parameters to initialize sflow server so sflow decoder gets right ip address and udp port to listen to
    :params data:
            **REQUIRED**  input data to be printed
    :params width:
            **REQUIRED**  the width of the printout
    """
    pprint.pprint(data, width=new_width)
