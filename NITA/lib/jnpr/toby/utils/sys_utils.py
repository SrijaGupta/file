"""
sys_utils.py: A module for systest genric specific apis
"""

import re
import os
import codecs
from robot.api import logger
import time
import sys
import json
from os.path import isfile
from subprocess import getoutput

__author__ = "Mohan Kumar M V"
__date__ = "Dec 2016"
__copyright__ = "Juniper Networks"
__license__ = "Juniper Networks"
__version__ = "0.1"


def pcap_to_txt_converter(**kwargs):
    '''
    Method for pcap to text converter
    :param pcap_file: .pcap file
    :param text_file: output text file
    : return the converted text file
    '''
    if kwargs is not None:
        pcp_file = kwargs.get('pcap_file', None)
        text_file_name = kwargs.get('text_file', None)
    else:
        raise AssertionError("please Pass the right Arguments")
    try:
        os.system('/usr/bin/tshark -r %s -x -V > %s' % (pcp_file, text_file_name))
    except:
        raise AssertionError("File Doesn't exisst")
    logger.info("pcap to text file converted properly input file:{0} and output file:{1}"\
            .format(pcp_file, text_file_name))

    return text_file_name

def get_the_info_from_pcap_file(**kwargs):
    '''
    Method for getting the info from pcap file
    :param converted_file: converted pcap to text file
    :param match: pattern to match
    : return the ditctionary with match conditions
    '''
    converted_file_txt = kwargs.get('converted_file', None)
    pattern = kwargs.get('match', None)
    match_dict = {}

    if os.path.isfile(converted_file_txt) and os.access(converted_file_txt, os.R_OK):
        read = open(converted_file_txt, "r")
        index = 0
        for line in read:
            line = line.replace('\n', '')
            if re.match(pattern, line):
                match_dict[index] = line
                index += 1
    return match_dict

def extract_igmp_join_leave_from_pcap_file(**kwargs):
    '''
    Method Reading the PCAP text file for IGMP join/leave packets
    :param pcap_txt_file: converted pcap to text file
    :igmp_type: igmp_type to match for join/leave packets
    :return the pattern select
    '''
    pcap_txt_file = kwargs.get('pcap_txt_file', False)
    igmp_type = kwargs.get('igmp_type', False)

    logger.info("Reading the PCAP text file for IGMP join/leave packets")
    if igmp_type == "Join":
        pattern_type = "Type: Membership Report"
    elif igmp_type == "Leave":
        pattern_type = "Type: Leave Group"

    textfile = open(pcap_txt_file, "r")
    textfilelines = textfile.readlines()
    pattern_select = []
    i = 0
    if [x for x in textfilelines if pattern_type in x]:
        flag1 = 1
        while flag1 == 1:
            line = textfilelines[i]
            if pattern_type in line:
                flag = 1
                while flag == 1:
                    pattern_select.append(line)
                    if "Ethernet II" in line and "00:10:94:00:00:0e" in line:
                        flag = 0
                        flag1 = 0
                        i -= 1
                    i -= 1
                    line = textfilelines[i]
            i += 1
    else:
        logger.info("No Match found in PCAP file")
    return pattern_select

def extract_IFD_from_dhcp_discover_packet_in_pcap_file(**kwargs):

    '''
    Method for Reading the PCAP text file for IFD info in the DHCP discover packets
    and converts the extracted infromation from HEX to TEXT format
    param pacp_txt_file: converted pcap to text file
    param dhcp_type:  dhcp packet type(DISCOVER)
    param max_length_process_flag: Mode for scanning the file
    return the extracted information
    '''

    pcap_txt_file = kwargs.get('pcap_txt_file', False)
    dhcp_type = kwargs.get('dhcp_type', False)
    max_length_process_flag = kwargs.get('max_length_process_flag', 'WARN')

    logger.info("Reading the PCAP text file for IFD info in the DHCP discover packets")
    logger.console("Reading the PCAP text file for IFD info in the DHCP discover packets")

    if dhcp_type == "DHCP Discover":
        pattern_type = "Agent Circuit ID"

    textfile = open(pcap_txt_file, "r")
    textfilelines = textfile.readlines()
    pattern_select = []
    i = 0
    circuit_id = ''
    if max_length_process_flag == '1':
        hexdata = []
        if [x for x in textfilelines if pattern_type in x]:
            flag1 = 1
            i = 0
            while flag1 == 1:
                line = textfilelines[i]
                if dhcp_type in line:
                    flag = 1
                    while flag == 1:
                        line = textfilelines[i]
                        if "Startxxxx" in line:
                            flag2 = 1
                            temp = re.findall(r'\S+', line)
                            for x in range(0, 17):
                                if temp[x] == '53':
                                    index = x
                                    for t in range(index, 17):
                                        hexdata.append(temp[t])
                            while flag2 == 1:
                                i += 1
                                line = textfilelines[i]
                                if flag != 0 and flag1 != 0:
                                    temp = re.findall(r'\S+', line)
                                length = len(temp)
                                if length < 16:
                                    mx_index = length
                                else:
                                    mx_index = 17
                                for xt in range(1, mx_index):
                                    if 'ff' in temp[xt]:
                                        flag2 = 0
                                        flag = 0
                                        flag1 = 0
                                    else:
                                        if flag2 == 1 and flag == 1 and flag1 == 1:
                                            hexdata.append(temp[xt])

                        i += 1
                    i += 1
                i += 1
            for var in hexdata:
                circuit_id += var
    else:
        if [x for x in textfilelines if pattern_type in x]:
            flag1 = 1
            while flag1 == 1:
                line = textfilelines[i]
                if dhcp_type in line:
                    flag = 1
                    while flag == 1:
                        if pattern_type in line:
                            pattern_select.append(line)
                            flag = 0
                            flag1 = 0
                            i += 1
                        i += 1
                        line = textfilelines[i]
                i += 1
        else:
            logger.info("No Match found in PCAP file")

        temp = re.findall(r'\S+', pattern_select[0])
        circuit_id = temp[3]
        circuit_id.rstrip()
    circuit_interface = codecs.decode(circuit_id, 'hex')
    circuit_interface = str(circuit_interface)
    circuit_interface = circuit_interface.replace("b\'", "", 1)
    circuit_interface = circuit_interface.replace("\'", "", 1)
    return circuit_interface

def ascii2hex(**kwargs):
    '''
    This method convert ascii to hex
    :param:
        REQUIRED STRING: ASCII string
    :return:
        Returns hex value of given ascii string
    Example:
        ascii2hex('string': string);
    '''

    string = kwargs['string']
    returnhex = ' '.join("{:02x}".format(ord(c)) for c in string)
    return returnhex

def inttohex(**kwargs):
    '''
    This method convert integer to hex
    :param:
        REQUIRED INTEGER: Integer value to be converted
    :param:
        REQUIRED BYTELEN: byte length
    :return:
        Returns hex value of given integer
    Example:
        inttohex('integer': 66, 'bytelen':1)
    '''

    integer = kwargs['integer']
    bytelen = kwargs['bytelen']*2
    tmp = ''.join("{0:0%sx}" % bytelen)
    hexstring = tmp.format(integer)
    return hexstring

#def sleep(intime):
#    '''
#    This method set sleep time
#    :param:
#        REQUIRED time: time need to sleep
#    :return:
#        None
#    '''
#    if not isinstance(intime, int):
#        raise Exception("Invalid time value")
#    for i in range(intime):
#        print("Wait %s Second(s)\n" % str(intime-i))
#        time.sleep(1)

def get_idp_predefined_service_hash(**kwargs):
    '''
    This method use to get dict of idp predefined service
    :param:
        OPTIONAL path: path of file
    :return:
        dict of idp
    '''

    mFlag = False
    predefserv_file = 'Testsuites/IDP/support/predefserv'
    path = kwargs.get('path', predefserv_file)
    for dirname in sys.path:
        candidate = os.path.join(dirname, path)
        if os.path.isfile(candidate):
            path = candidate
            break
    name = ''
    predefserv = {}
    try:
        file = open(path)
        lines = file.read().splitlines()
    except Exception:
        print('%s not exist' % path)
        return None
    for line in lines:
        line = line.rstrip('\n')
        if re.match(r'^\s*\)\s*$', line) and mFlag:
            mFlag = False
            matched = re.match(r'^(.*),$',
                               predefserv['%s,members' % name], re.I)
            predefserv['%s,members' % name] = matched.group(1)
            continue
        elif re.match(r'^\s*\)\s*$', line):
            continue
        matched1 = re.match(r'^:\s*\((.*)', line)
        if matched1 and not re.match('\)', line):
            predefserv['name,%s' % matched1.group(1)] = matched1.group(1)
            name = predefserv['name,%s' % matched1.group(1)]
        matched2 = re.match(r'^\s*:(.*?)\s*?\((.*)\)$', line)
        if matched2 and mFlag is not True:
            if re.match(r'^\s*$', matched2.group(1)):
                continue
            predefserv['%s,%s' % (name, matched2.group(1))] = matched2.group(2)
        matched3 = re.match(r'^\s*:members\s*\(', line)
        if matched3:
            mFlag = True
            continue
        matched4 = re.match(r'^\s*:\s*\((.*)\)', line)
        if matched4 and mFlag:
            predefserv['%s,members' % name] = ""
            predefserv['%s,members' % name] = str(predefserv[
                '%s,members' % name]) + matched4.group(1) + ','
    file.close()
    return predefserv

def compare_list_of_dict(**kwargs):
    '''
    Compare Original list of dictionary and User list of dictionary
    :param org_lod
        REQUIRED Original list of dictionary
    :param usr_lod
        REQUIRED User list of dictionary
    :param return_list
        OPTIONAL Return value is in List or not: True/False
    :return:
        List if return_list is defined
        Boolean if return_list is defined
    '''

    org_lod = kwargs.get('org_lod', [])
    usr_lod = kwargs.get('usr_lod', [])
    return_list = kwargs.get('return_list', False)
    status = []
    print("Original List of Dict Values: %s\n" % str(org_lod))
    print("User List of Dict Values: %s\n" % str(usr_lod))
    for usr_d in usr_lod:
        print("Checking User Values: %s\n" % str(usr_d))
        tmp_status = 0
        for org_d in org_lod:
            if compare_dict(org_dict=org_d, usr_dict=usr_d):
                tmp_status = 1
                break
        status.append(tmp_status)
    if return_list:
        return status
    else:
        if 0 in status:
            return False
        else:
            return True

def compare_dict(**kwargs):
    '''
    Compare 2 dictionaries
    :param org_dict
        REQUIRED Original Dictionary
    :param usr_dict
        REQUIRED User Dictionary
    :param negate
        OPTIONAL negate, True/False, default is False
    :return:
        True/False
    '''

    org_dict = kwargs.get('org_dict', [])
    usr_dict = kwargs.get('usr_dict', [])
    negate = kwargs.get('negate', False)
    print("Original Dictionary Values: %s\n" % str(org_dict))
    print("User Dictionary Values: %s\n" % str(usr_dict))
    status = True
    for u_key in usr_dict.keys():
        if org_dict.get(u_key):
            if isinstance(usr_dict.get(u_key), int):
                var1 = str(usr_dict.get(u_key))
            else:
                var1 = ','.join((list(map(str, usr_dict.get(u_key)))))

            if isinstance(org_dict.get(u_key), int):
                var2 = str(org_dict.get(u_key))
            else:
                var2 = ','.join((list(map(str, org_dict.get(u_key)))))
            if not re.fullmatch(var1, var2, re.I | re.M):
                if negate:
                    print("PASS: Value for key %s does not match" % u_key)
                else:
                    print("FAIL: Value for key %s does not match" % u_key)
                status = False
            else:
                if negate:
                    print("FAIL: Value for key %s matched" % u_key)
                else:
                    print("PASS: Value for key %s matched" % u_key)
        else:
            if negate:
                print("FAIL: Key %s does not exist" % u_key)
            else:
                print("PASS: Key %s does not exist" % u_key)
            status = False
    if negate:
        if status:
            status = False
        else:
            status = True
    return status

def compare_list_of_list(**kwargs):
    '''
    Compare Original List of List and User List of List
    :param org_lol
        REQUIRED Original List of List
    :param usr_lol
        REQUIRED User List of List
    :param return_list
        OPTIONAL Return value is in List or not: True/False
    :return:
        List if return_list is defined
        Boolean if return_list is defined
    '''

    org_lol = kwargs.get('org_lol')
    usr_lol = kwargs.get('usr_lol')
    return_list = kwargs.get('return_list', False)
    status = []
    if not compare_list(org_list=org_lol, usr_list=usr_lol):
        status.append(0)
    else:
        status.append(1)
    if return_list:
        return status
    else:
        if 0 in status:
            return False
        else:
            return True

def compare_list(**kwargs):
    '''
    This method use to compare 2 lists
    :param:
        REQUIRED org_list: list
    :param:
        REQUIRED usr_list: list
    :return:
        True or False
    '''

    org_list = kwargs.get('org_list')
    usr_list = kwargs.get('usr_list')
    negate = kwargs.get('negate', False)
    if negate == 'True':
        negate = True
    print("Original List Values: %s\n" % str(org_list))
    print("User List Values: %s\n" % str(usr_list))
    status = True
    for val in usr_list:
        tmp1 = ''.join(list(map(str, val)))
        tmp2 = ''.join(list(map(str, org_list)))
        if re.fullmatch(tmp1, tmp2, re.I | re.M):
            if negate:
                print("FAIL: Value for val \"%s\" matched" % val)
            else:
                print("PASS: Value for val \"%s\" matched" % val)
        else:
            if negate:
                print("PASS: val \"%s\" does not exist" % val)
            else:
                print("FAIL: val \"%s\" does not exist" % val)
            status = False
    if negate:
        if status:
            status = False
        else:
            status = True
    return status

def file_presence_search(file_list):
    """
    This function searches for a file in a list beginning from the first element.
    The match condition being the presence of the file on the system.

    :param:
        REQUIRED file_list: list of file paths

    :return:
        file path if found, if none found, throws an exception
    """

    if type(file_list) is not list:
        raise Exception("Argument file_list must be of type 'list'")

    try:
        for search_file in file_list:

            if isfile(search_file) is True:
                print("Checking presence of file: '%s' - FOUND" % search_file)
                return search_file
            else:
                print("Checking presence of file: '%s' - NOT FOUND" % search_file)

    except Exception as exp:
        raise Exception("Unknown Exception caught: %s : %s" % (type(exp), exp))

    raise Exception("No Matching File Present on the System")

def extract_arp_packet_from_capture(capture_file):
    """
    This function takes a pcap file as argument and extracts all ARP packets found in it.
    It return a hash that contains the src-mac and src-ip as keys

    :param capture_file:
        REQUIRED: pcap file with complete path 

    :return:
        Dictionary containing keys as sender-mac and sender-ip of all ARP packets found
        in the capture
    """
    try:
        print("Parsing pcap file: %s for ARP Packets" % capture_file)
        print("Command for parsing: /usr/bin/tshark -r %s -x -V -T json"  % capture_file)
        json_output = getoutput("/usr/bin/tshark -r %s -x -V -T json" % capture_file)
        packet_list = json.loads(json_output)
        ret_arp_hash = {}
        for packet in packet_list:
            src_ip = ""
            src_mac = ""
            if 'arp' in packet['_source']['layers']:
                if 'arp.src.proto_ipv4' in packet['_source']['layers']['arp']:
                    src_ip = packet['_source']['layers']['arp']['arp.src.proto_ipv4']
                if 'arp.src.hw_mac' in packet['_source']['layers']['arp']:
                    src_mac = packet['_source']['layers']['arp']['arp.src.hw_mac']
                ret_arp_hash["%s,%s" % (src_mac, src_ip)] = 1

        return ret_arp_hash

    except Exception as exp:
        raise Exception("Unknown exception raised in extract_arp_pkt_from_capture: %s : %s" % (type(exp), exp))

def extract_icmpv6_packet_from_capture(capture_file):
    """
    This function takes a pcap file as argument and extracts all ICMPv6 packets found in it.
    It return a hash that contains the src-mac and src-ipv6 as keys. And icmpv6 type as values

    :param capture_file:
        REQUIRED: pcap file with complete path 

    :return:
        Dictionary containing keys as src-mac and ipv6-src of all ICMPv6 packets found
        in the capture and their icmpv6-type as values
    """
    try:
        json_output = getoutput("/usr/bin/tshark -r %s -x -V -T json" % capture_file)
        packet_list = json.loads(json_output)
        ret_icmpv6_hash = {}
        for packet in packet_list:
            src_ipv6 = ""
            src_mac = ""
            icmpv6_type = ""
            if 'ipv6' in packet['_source']['layers'] and \
               packet['_source']['layers']['ipv6']['ipv6.nxt'] == '58' and \
               'icmpv6' in packet['_source']['layers']:
                src_ipv6 = packet['_source']['layers']['ipv6']['ipv6.src']
                src_mac = packet['_source']['layers']['eth']['eth.src']
                icmpv6_type = packet['_source']['layers']['icmpv6']['icmpv6.type']
                ret_icmpv6_hash["%s,%s" % (src_mac, src_ipv6)] = icmpv6_type

        return ret_icmpv6_hash

    except Exception as exp:
        raise Exception("Unknown exception raised in extract_icmpv6_pkt_from_capture: %s : %s" % (type(exp), exp))

