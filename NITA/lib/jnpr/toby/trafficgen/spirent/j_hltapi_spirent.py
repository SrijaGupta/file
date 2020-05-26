#!/usr/local/python-3.4.5/bin/python3

'''
#
# This is Auto-generated Spirent HLTAPI common Stub code
# please do NOT modify the format/delete any comments in this file,
#   this file is read and regenerated automatically
#
'''
import os
import glob
import random
import shutil
import traceback
from time import sleep
import re
import ipaddress
import inspect
from math import ceil
from jnpr.toby.engines.config.config_utils import _make_ip_list
true = re.compile("^1$")
false = re.compile("^0$")
# Constant to use as default value
jNone = "jNone"

global_config = dict()
global_tracking = dict()
handle_map = dict()
session_map = dict()
pim_map = dict()
v4_handles = []
v6_handles = []
burst_count = []
packet_per_burst = []
connected = 1
stream_map = dict()
link_local = ipaddress.IPv6Address('fe80::1')


def get_arg_value(rt_handle, docstring, **arguments):
    called_function = inspect.stack()[1][3]

    for key in list(arguments.keys()):
        if arguments[key] == jNone:
            del arguments[key]

    for arg in arguments:
        get_value = re.match(r'.*param\s+'+arg+'\s+\-\s+<(\S+)>.*', docstring, re.S)
        if get_value is not None:
            string_value = get_value.group(1)
        else:
            continue

        if '-' in string_value:
            range_arg = re.match(r'(\d+)\-(\d+)', string_value, re.S)
            if range_arg is not None:
                minimum = int(range_arg.group(1))
                maximum = int(range_arg.group(2))
                arg_value = int(arguments[arg])
                if arg_value < minimum:
                    arguments[arg] = minimum
                    rt_handle.log("WARN", "Argument "+arg+" value of "+called_function+" is not in valid range. Setting it to minimum value supported : "+str(minimum))
                elif arg_value > maximum:
                    arguments[arg] = maximum
                    rt_handle.log("WARN", "Argument "+arg+" value of "+called_function+" is not in valid range. Setting it to maximum value supported : "+str(maximum))
                continue
        elif ':' in string_value or '|' in string_value:
            if arguments[arg] not in string_value:
                raise RuntimeError('Argument '+arg+' value '+arguments[arg]+' is not supported for '+called_function+'. Supported values are '+string_value)
            for value in string_value.split('|'):
                if value == arguments[arg]:
                    arguments[arg] = value
                    break
                elif ':' in value and arguments[arg] in value:
                    (spirent_value, ixia_value) = value.split(':')
                    if rt_handle.os.lower() == 'spirent' or rt_handle.osname.lower() == 'spirent':
                        arguments[arg] = spirent_value
                    elif rt_handle.osname.lower() == 'ixos':
                        arguments[arg] = ixia_value
                    break
            continue
        elif re.match(r'\w+', string_value, re.S):
            if arguments[arg] != string_value:
                raise RuntimeError('Argument '+arg+' value '+arguments[arg]+' is not supported for '+called_function)

    return arguments

def j_cleanup_session(rt_handle):
    """
    :param rt_handle:       RT object
    :return response from rt_handle.invoke(<parameters>)

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    global handle_map
    global session_map
    global pim_map
    global v4_handles
    global v6_handles
    global connected

    handle_map = dict()
    session_map = dict()
    pim_map = dict()
    v4_handles = []
    v6_handles = []

    args = dict()
    args['clean_dbfile'] = 1
    args['clean_logs'] = 0
    args['maintain_lock'] = 0
    args['clean_labserver_session'] = 1
    args['port_handle'] = 'all'

    if connected == 1:
        ret = rt_handle.invoke('cleanup_session', **args)
        if ret['status'] == '1':
            connected = 0
        return ret


def j_connect(rt_handle):
    """
    :param rt_handle:       RT object
    :return response from rt_handle.invoke(<parameters>)

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    global connected

    if connected == 0:
        t.Initialize(force=True)
        connected = 1


def run_native_args(return_value, rt_handle, **native_arg):
    """
    This api executes native arguments passed to traffic_config api
    """

    for hand in return_value['stream_handles']:
        for argument in native_arg.keys():
            children = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children')
            if argument.startswith('ip_') and 'ipv4' not in children:
                ipv4_handle = rt_handle.invoke('invoke', cmd='stc::create ipv4:IPv4 -under '+hand)
            ipv4_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-ipv4:IPv4')

            if argument.startswith('arp_') and 'arp' not in children:
                arp_handle = rt_handle.invoke('invoke', cmd='stc::create arp:ARP -under '+hand)
            arp_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-arp:ARP')

            if argument.startswith('tcp_') and 'tcp:' not in children:
                tcp_handle = rt_handle.invoke('invoke', cmd='stc::create tcp:Tcp -under '+hand)
            tcp_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-tcp:Tcp')

            pduinfo = rt_handle.invoke('invoke', cmd="stc::get "+hand+" -PduInfo")
            for pdu in pduinfo.split(' '):
                if pdu.startswith('arp'):
                    arp_pdu_name = pdu[0:pdu.find(',')]
                if pdu.startswith('ethernet'):
                    ethernet_pdu_name = pdu[0:pdu.find(',')]
                if pdu.startswith('tcp'):
                    tcp_pdu_name = pdu[0:pdu.find(',')]
                if pdu.startswith('ipv4'):
                    ip_pdu_name = pdu[0:pdu.find(',')]
                if pdu.startswith('anon') and 'Vlan.' in pdu:
                    Vlan_pdu_name = pdu[0:pdu.find(',')]
                if pdu.startswith('ipv6'):
                    ipv6_pdu_name = pdu[0:pdu.find(',')]

            #Native arg execution starts
            if argument == 'arp_protocol_addr_length':
                rt_handle.invoke('invoke', cmd='stc::config '+arp_handle+' -ipAddr '+native_arg[argument])
            elif argument == 'arp_hw_address_length':
                rt_handle.invoke('invoke', cmd='stc::config '+arp_handle+' -ihAddr '+native_arg['arp_hw_address_length'])
            elif argument == 'arp_hw_address_length_mode':
                arp_hw_address_length_count = native_arg['arp_hw_address_length_count'] if 'arp_hw_address_length_count' in native_arg.keys() else "1"
                arp_hw_address_length_step = native_arg['arp_hw_address_length_step'] if 'arp_hw_address_length_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['arp_hw_address_length_mode']+" -RecycleCount \""+arp_hw_address_length_count+"\" -StepValue {"+arp_hw_address_length_step+"} -DataType \"NATIVE\" -OffsetReference {"+arp_pdu_name+".ihAddr} -Name {Modifier} -Mask {255} -Active \"TRUE\" -LocalActive \"TRUE\" -Data {6} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")
            elif argument == 'arp_protocol_addr_length_mode':
                arp_protocol_addr_length_count = native_arg['arp_protocol_addr_length_count'] if 'arp_protocol_addr_length_count' in native_arg.keys() else "1"
                arp_protocol_addr_length_step = native_arg['arp_protocol_addr_length_step'] if 'arp_protocol_addr_length_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['arp_protocol_addr_length_mode']+" -RecycleCount \""+arp_protocol_addr_length_count+"\" -StepValue {"+arp_protocol_addr_length_step+"} -DataType \"NATIVE\" -OffsetReference {"+arp_pdu_name+".ipAddr} -Name {Modifier} -Mask {255} -Active \"TRUE\" -LocalActive \"TRUE\"  -Data {4} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")
            elif argument == 'arp_operation_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['arp_operation_mode']+" -RecycleCount \"1\" -StepValue {1} -Mask {65535} -Data {1} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\"  -Offset \"0\" -OffsetReference {"+arp_pdu_name+".operation} -Active \"TRUE\"  -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'ether_type_mode':
                ether_type_count = native_arg['ether_type_count'] if 'ether_type_count' in native_arg.keys()  else "1"
                ether_type_step = native_arg['ether_type_step'] if 'ether_type_step' in native_arg.keys()  else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ether_type_mode']+" -Mask {FFFF}  -StepValue {"+ether_type_step+"} -RecycleCount \""+ether_type_count+"\"  -RepeatCount \"0\" -Data {0800} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\" -Offset \"0\" -OffsetReference {"+ethernet_pdu_name+".etherType} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'global_dest_mac_retry_count':
                rt_handle.invoke('invoke', cmd='stc::config [stc::get project1 -children-arpndconfig] -RetryCount '+native_arg[argument])
            elif argument == 'global_dest_mac_retry_delay':
                rt_handle.invoke('invoke', cmd='stc::config [stc::get project1 -children-arpndconfig] -TimeOut '+native_arg[argument])
            elif argument == 'global_enable_mac_change_on_fly':
                global_enable_mac_change_on_fly = 'False' if native_arg['global_enable_mac_change_on_fly'] == "1" else 'false'
                rt_handle.invoke('invoke', cmd='stc::config [stc::get project1 -children-arpndconfig] -ProcessGratuitousArpRequests '+global_enable_mac_change_on_fly)
            elif argument == 'ip_cost':
                tosdiffserv = rt_handle.invoke('invoke', cmd='stc::get '+ipv4_handle+' -children-tosdiffserv')
                tos = rt_handle.invoke('invoke', cmd='stc::get '+tosdiffserv+' -children-tos')
                rt_handle.invoke('invoke', cmd='stc::config '+tos+' -mbit '+native_arg[argument])
            elif argument == 'ip_delay':
                tosdiffserv = rt_handle.invoke('invoke', cmd='stc::get '+ipv4_handle+' -children-tosdiffserv')
                tos = rt_handle.invoke('invoke', cmd='stc::get '+tosdiffserv+' -children-tos')
                rt_handle.invoke('invoke', cmd='stc::config '+tos+' -dbit '+native_arg[argument])
            elif argument == 'vlan_protocol_tag_id_mode':
                vlan_protocol_tag_id_count = native_arg['vlan_protocol_tag_id_count'] if 'vlan_protocol_tag_id_count' in native_arg.keys()  else "1"
                vlan_protocol_tag_id_step = native_arg['vlan_protocol_tag_id_step'] if 'vlan_protocol_tag_id_step' in native_arg.keys()  else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['vlan_protocol_tag_id_mode']+" -Mask {FFFF} -StepValue {"+vlan_protocol_tag_id_step+"} -RecycleCount \""+vlan_protocol_tag_id_count+"\" -RepeatCount \"0\" -Data {8100} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\"  -Offset \"0\" -OffsetReference {"+ethernet_pdu_name+".vlans."+Vlan_pdu_name+".type} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            #elif argument == 'tcp_cwr_flag':
             #   rt_handle.invoke('invoke', cmd='stc::config' + " " + tcp_handle + ' -cwrBit' + ' ENABLE')
            elif argument == 'tcp_cwr_flag_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_cwr_flag_mode']+" -Mask {1} -StepValue {1} -RecycleCount \"1\"  -RepeatCount \"0\" -Data {0} -DataType \"NATIVE\" -EnableStream \"FALSE\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".cwrBit} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            #elif argument == 'tcp_ecn_echo_flag':
             #   rt_handle.invoke('invoke', cmd='stc::config' + " " + tcp_handle + ' -ecnBit' + ' ENABLE')
            elif argument == 'tcp_ecn_echo_flag_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_ecn_echo_flag_mode']+" -Mask {1} -StepValue {1} -RecycleCount \"1\"  -RepeatCount \"0\" -Data {0} -DataType \"NATIVE\" -EnableStream \"FALSE\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".ecnBit} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'tcp_fin_flag_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_fin_flag_mode']+" -Mask {1} -StepValue {1} -RecycleCount \"1\"  -RepeatCount \"0\" -Data {0} -DataType \"NATIVE\" -EnableStream \"FALSE\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".finBit} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'tcp_psh_flag_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_psh_flag_mode']+" -Mask {1} -StepValue {1} -RecycleCount \"1\"  -RepeatCount \"0\" -Data {0} -DataType \"NATIVE\" -EnableStream \"FALSE\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".pshBit} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'tcp_reserved_mode':
                tcp_reserved_count = native_arg['tcp_reserved_count'] if 'tcp_reserved_count' in native_arg.keys()  else "1"
                tcp_reserved_step = native_arg['tcp_reserved_step'] if 'tcp_reserved_step' in native_arg.keys()  else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_reserved_mode']+" -Mask {1111} -StepValue {"+tcp_reserved_step+"} -RecycleCount \""+tcp_reserved_count+"\"  -RepeatCount \"0\" -Data {0000} -DataType \"NATIVE\" -EnableStream \"FALSE\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".reserved} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'ip_reliability':
                tosdiffserv = rt_handle.invoke('invoke', cmd='stc::get '+ipv4_handle+' -children-tosdiffserv')
                tos = rt_handle.invoke('invoke', cmd='stc::get '+tosdiffserv+' -children-tos')
                rt_handle.invoke('invoke', cmd='stc::config '+tos+' -rbit' + " " + native_arg['ip_reliability'])
            elif argument == 'ip_throughput':
                tosdiffserv = rt_handle.invoke('invoke', cmd='stc::get '+ipv4_handle+' -children-tosdiffserv')
                tos = rt_handle.invoke('invoke', cmd='stc::get '+tosdiffserv+' -children-tos')
                rt_handle.invoke('invoke', cmd='stc::config '+tos+' -tbit' + " " + native_arg['ip_throughput'])

###########ipv6 next header execution##############################################
            elif argument == 'ipv6_next_header_mode':
#                ipv6_next_header = native_arg['ipv6_next_header'] if 'ipv6_next_header' in native_arg.keys() else "59"
                ipv6_next_header_count = native_arg['ipv6_next_header_count'] if 'ipv6_next_header_count' in native_arg.keys() else "1"
                ipv6_next_header_step = native_arg['ipv6_next_header_step'] if 'ipv6_next_header_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ipv6_next_header_mode']+" -RecycleCount \""+ipv6_next_header_count+"\" -StepValue {"+ipv6_next_header_step+"} -DataType \"NATIVE\" -OffsetReference {"+ipv6_pdu_name+".nextHeader} -Name {Modifier} -Mask {255} -Active \"TRUE\" -LocalActive \"TRUE\" -Data {"+native_arg['ipv6_next_header']+"} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")






####route_mesh native args execution
            if argument == 'route_mesh' and native_arg['route_mesh'] == 'fully':
                rt_handle.invoke('invoke', cmd='stc::config '+hand+' -TrafficPattern "BACKBONE"')
            elif argument == 'route_mesh' and native_arg['route_mesh'] == 'one_to_one':
                rt_handle.invoke('invoke', cmd='stc::config '+hand+' -TrafficPattern "PAIR"')

###Ethernet pause native args
            if argument == 'ethernet_pause':
                eth_hndl = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-ethernet:ethernetii')
                rt_handle.invoke('invoke', cmd='stc::delete '+eth_hndl)
                rt_handle.invoke('invoke', cmd='stc::create ethernetpause:EthernetPause -under '+hand)
                eth_pause_hand = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-ethernetpause:EthernetPause')
                rt_handle.invoke('invoke', cmd='stc::config '+eth_pause_hand+' -Parameters '+native_arg['ethernet_pause'])

###GTP native args
            if argument == 'gtp' and native_arg['gtp'] == '1':
                rt_handle.invoke('invoke', cmd='stc::create gtpv1:GTPv1 -under '+hand)
                gtp_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gtpv1:GTPv1')
                if native_arg['gtp_protocol_type'] == "GTP'":
                    rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -protcol 0')
                else:
                    rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -protcol 1')
                if native_arg['gtp_extended_header'] == '1':
                    rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -eFlg 1')
                else:
                    rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -eFlg 0')
                if native_arg['gtp_seq_num_flag'] == '1':
                    rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -sFlg 1')
                else:
                    rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -sFlg 0')
                if native_arg['gtp_n_pdu_flag'] == '1':
                    rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -pnFlg 1')
                else:
                    rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -pnFlg 0')
            if argument == 'gtp' and 'gtp_message_type' in native_arg.keys():
                rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -msgType '+native_arg['gtp_message_type'])
            if argument == 'gtp' and 'gtp_te_id' in native_arg.keys():
                rt_handle.invoke('invoke', cmd='stc::config '+gtp_handle+' -teid '+native_arg['gtp_te_id'])

#####GTP_teid_count
            if argument == 'gtp' and 'gtp_te_id_count' in native_arg.keys() and 'gtp_te_id_step' not in native_arg.keys():
                gtp_dum1 = rt_handle.invoke('invoke', cmd='stc::create "RangeModifier" -under '+hand+' -StepValue {1} -RecycleCount "'+native_arg['gtp_te_id_count']+'" -OffsetReference {'+gtp_handle+'} -Name {Modifier} -Data {10} -Mask {4294967295}')
                rt_handle.invoke('invoke', cmd='stc::delete '+gtp_dum1) 
                pduinfo = rt_handle.invoke('invoke', cmd="stc::get "+hand+" -PduInfo")
                for pdu_split in pduinfo.split(' '):
                    for pdu in pdu_split.split(','):
                        if pdu.startswith('gtpv1_'):
                            rt_handle.invoke('invoke', cmd='stc::create "RangeModifier" -under '+hand+' -StepValue {1} -RecycleCount "'+native_arg['gtp_te_id_count']+'" -OffsetReference {'+pdu+'.teid} -Name {Modifier} -Data {10} -Mask {4294967295} -EnableStream '+native_arg['enable_stream'])
            elif argument == 'gtp' and 'gtp_te_id_count' in native_arg.keys() and 'gtp_te_id_step' in native_arg.keys():
                gtp_dum2 = rt_handle.invoke('invoke', cmd='stc::create "RangeModifier" -under '+hand+' -StepValue {1} -RecycleCount "'+native_arg['gtp_te_id_count']+'" -OffsetReference {'+gtp_handle+'} -Name {Modifier} -Data {10} -Mask {4294967295}')
                rt_handle.invoke('invoke', cmd='stc::delete '+gtp_dum2)
                pduinfo = rt_handle.invoke('invoke', cmd="stc::get "+hand+" -PduInfo")
                for pdu_split in pduinfo.split(' '):
                    for pdu in pdu_split.split(','):
                        if pdu.startswith('gtpv1_'):
                            rt_handle.invoke('invoke', cmd='stc::create "RangeModifier" -under '+hand+' -StepValue {'+native_arg['gtp_te_id_step']+'} -RecycleCount "'+native_arg['gtp_te_id_count']+'" -OffsetReference {'+pdu+'.teid} -Name {Modifier} -Data {10} -Mask {4294967295} -EnableStream '+native_arg['enable_stream'])
######GRE Native args execution
            if argument == 'gre_key_enable' and native_arg['gre_key_enable'] == '1':
                gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                rt_handle.invoke('invoke', cmd='stc::config '+gre_handle+' -keyPresent 1')
                if 'gre_key' in native_arg.keys():
                    if '0x' in native_arg['gre_key'] or '0X' in native_arg['gre_key']:
                        gre_key1 = native_arg['gre_key'].lower().split('x')[-1]
                        gre_key1 = int(gre_key1, 16)
                        keys = rt_handle.invoke('invoke', cmd='stc::create keys -under '+gre_handle)
                        grekeys = rt_handle.invoke('invoke', cmd='stc::create grekey -under '+keys)
                        rt_handle.invoke('invoke', cmd='stc::config '+grekeys+' -value '+str(gre_key1))
                    else:
                        raise ValueError("Please pass the value in hex(0x or 0X) format")
            elif argument == 'gre_key_enable' and native_arg['gre_key_enable'] == '0':
                gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                rt_handle.invoke('invoke', cmd='stc::config '+gre_handle+' -keyPresent 0')
#GRE version
            if argument == 'gre_version':
                if '0x' in native_arg['gre_version'] or '0X' in native_arg['gre_version']:
                    gre_version1 = native_arg['gre_version'].lower().split('x')[-1]
                    gre_version1 = int(gre_version1, 16)
                    gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                    rt_handle.invoke('invoke', cmd='stc::config '+gre_handle+' -version '+str(gre_version1))
                else:
                    raise ValueError("Please pass the value in hex(0x or 0X) format")
#GRE sequence number
            if argument == 'gre_seq_enable' and native_arg['gre_seq_enable'] == '1':
                gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                rt_handle.invoke('invoke', cmd='stc::config '+gre_handle+' -seqNumPresent 1')
                if 'gre_seq_number' in native_arg.keys():
                    if '0x' in native_arg['gre_seq_number'] or '0X' in native_arg['gre_seq_number']:
                        gre_seq_number1 = native_arg['gre_seq_number'].lower().split('x')[-1]
                        gre_seq_number1 = int(gre_seq_number1, 16)
                        seq_num = rt_handle.invoke('invoke', cmd='stc::create seqNums -under '+gre_handle)
                        gre_seq_num = rt_handle.invoke('invoke', cmd='stc::create GreSeqNum -under '+seq_num)
                        rt_handle.invoke('invoke', cmd='stc::config '+gre_seq_num+' -value '+str(gre_seq_number1))
                    else:
                        raise ValueError("Please pass the value in hex(0x or 0X) format")
            elif argument == 'gre_seq_enable' and native_arg['gre_seq_enable'] == '0':
                gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                rt_handle.invoke('invoke', cmd='stc::config '+gre_handle+' -seqNumPresent 0')
#GRE Checksum
            if argument == 'gre_checksum_enable' and native_arg['gre_checksum_enable'] == '1':
                gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                rt_handle.invoke('invoke', cmd='stc::config '+gre_handle+' -ckPresent 1')
                if 'gre_checksum' in native_arg.keys() and 'gre_reserved1' in native_arg.keys():
                    if '0x' in native_arg['gre_checksum'] or '0X' in native_arg['gre_checksum']:
                        gre_checksum1 = native_arg['gre_checksum'].lower().split('x')[-1]
                        gre_checksum1 = int(gre_checksum1, 16)
                    else:
                        raise ValueError("Please pass the value in hex(0x or 0X) format")
                    if '0x' in native_arg['gre_reserved1'] or '0X' in native_arg['gre_reserved1']:
                        gre_reserved11 = native_arg['gre_reserved1'].lower().split('x')[-1]
                        gre_reserved11 = int(gre_reserved11, 16)
                        gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                        check_sum = rt_handle.invoke('invoke', cmd='stc::create checksums -under '+gre_handle)
                        gre_chksum = rt_handle.invoke('invoke', cmd='stc::create GreChecksum -under '+check_sum)
                        rt_handle.invoke('invoke', cmd='stc::config '+gre_chksum+' -value '+str(gre_checksum1)+' -reserved '+str(gre_reserved11))
                    else:
                        raise ValueError("Please pass the value in hex(0x or 0X) format")
                elif 'gre_reserved1' in native_arg.keys() and 'gre_checksum' not in native_arg.keys():
                    if '0x' in native_arg['gre_reserved1'] or '0X' in native_arg['gre_reserved1']:
                        gre_reserved11 = native_arg['gre_reserved1'].lower().split('x')[-1]
                        gre_reserved11 = int(gre_reserved11, 16)
                        gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                        check_sum = rt_handle.invoke('invoke', cmd='stc::create checksums -under '+gre_handle)
                        gre_chksum = rt_handle.invoke('invoke', cmd='stc::create GreChecksum -under '+check_sum)
                        rt_handle.invoke('invoke', cmd='stc::config '+gre_chksum+' -reserved '+str(gre_reserved11))
                    else:
                        raise ValueError("Please pass the value in hex(0x or 0X) format")
                elif 'gre_reserved1' not in native_arg.keys() and 'gre_checksum' in native_arg.keys():
                    if '0x' in native_arg['gre_checksum'] or '0X' in native_arg['gre_checksum']:
                        gre_checksum1 = native_arg['gre_checksum'].lower().split('x')[-1]
                        gre_checksum1 = int(gre_checksum1, 16)
                        gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                        check_sum = rt_handle.invoke('invoke', cmd='stc::create checksums -under '+gre_handle)
                        gre_chksum = rt_handle.invoke('invoke', cmd='stc::create GreChecksum -under '+check_sum)
                        rt_handle.invoke('invoke', cmd='stc::config '+gre_chksum+' -value '+str(gre_checksum1))
                    else:
                        raise ValueError("Please pass the value in hex(0x or 0X) format")
            elif argument == 'gre_checksum_enable' and native_arg['gre_checksum_enable'] == '0':
                gre_handle = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-gre:Gre')
                rt_handle.invoke('invoke', cmd='stc::config '+gre_handle+' -ckPresent 0')

####End of GRE native args execution
            if argument == 'tcp_ack_flag_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_ack_flag_mode']+" -Mask {1} -StepValue {1} -RecycleCount \"1\" -RepeatCount \"0\" -Data {1} -DataType \"NATIVE\"  -EnableStream \""+native_arg['enable_stream']+"\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".ackBit} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'tcp_ack_num_mode':
                tcp_ack_num_count = native_arg['tcp_ack_num_count'] if 'tcp_ack_num_count' in native_arg.keys() else "1"
                tcp_ack_num_step = native_arg['tcp_ack_num_step'] if 'tcp_ack_num_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_ack_num_mode']+" -Mask {4294967295}  -StepValue {"+tcp_ack_num_step+"} -RecycleCount \""+tcp_ack_num_count+"\"  -RepeatCount \"0\" -Data {234567} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\" -Offset \"0\"  -OffsetReference {"+tcp_pdu_name+".ackNum}  -Active \"TRUE\" -LocalActive \"TRUE\"  -Name {Modifier}")
            elif argument == 'tcp_rst_flag_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_rst_flag_mode']+" -Mask {1} -StepValue {1} -RecycleCount \"1\"  -RepeatCount \"0\" -Data {0} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\"  -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".rstBit} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'tcp_seq_num_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_seq_num_mode']+" -Mask {4294967295}  -StepValue {1} -RecycleCount \"1\"  -RepeatCount \"0\" -Data {123456} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\" -Offset \"0\"  -OffsetReference {"+tcp_pdu_name+".seqNum}  -Active \"TRUE\" -LocalActive \"TRUE\"  -Name {Modifier}")
            elif argument == 'tcp_syn_flag_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_syn_flag_mode']+" -Mask {1} -StepValue {1} -RecycleCount \"1\"  -RepeatCount \"0\" -Data {0} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".synBit} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'tcp_urg_flag_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_urg_flag_mode']+" -Mask {1} -StepValue {1} -RecycleCount \"1\"  -RepeatCount \"0\" -Data {0} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".urgBit} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'tcp_urgent_ptr_mode':
                tcp_urgent_ptr_count = native_arg['tcp_urgent_ptr_count'] if 'tcp_urgent_ptr_count' in native_arg.keys() else "1"
                tcp_urgent_ptr_step = native_arg['tcp_urgent_ptr_step'] if 'tcp_urgent_ptr_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_urgent_ptr_mode']+" -Mask {65535} -StepValue {"+tcp_urgent_ptr_step+"} -RecycleCount \""+tcp_urgent_ptr_count+"\"  -RepeatCount \"0\" -Data {0} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".urgentPtr} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'tcp_window_mode':
                tcp_window_count = native_arg['tcp_window_count'] if 'tcp_window_count' in native_arg.keys() else "1"
                tcp_window_step = native_arg['tcp_window_step'] if 'tcp_window_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['tcp_window_mode']+" -Mask {65535} -StepValue {"+tcp_window_step+"} -RecycleCount \""+tcp_window_count+"\"  -RepeatCount \"0\" -Data {4096} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\" -Offset \"0\" -OffsetReference {"+tcp_pdu_name+".window} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'vlan_cfi_mode':
                vlan_cfi_count = native_arg['vlan_cfi_count'] if 'vlan_cfi_count' in native_arg.keys() else "1"
                vlan_cfi_step = native_arg['vlan_cfi_step'] if 'vlan_cfi_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['vlan_cfi_mode']+" -Mask {1} -StepValue {"+vlan_cfi_step+"} -RecycleCount \""+vlan_cfi_count+"\"  -RepeatCount \"0\" -Data {0} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\"  -Offset \"0\" -OffsetReference {"+ethernet_pdu_name+".vlans."+Vlan_pdu_name+".cfi} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'ip_fragment_last_mode':
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ip_fragment_last_mode']+" -Mask {1} -StepValue {1} -RecycleCount \"1\" -RepeatCount \"0\" -Data {1} -DataType \"NATIVE\" -EnableStream \""+native_arg['enable_stream']+"\"  -Offset \"0\" -OffsetReference {"+ip_pdu_name+".flags.mfBit} -Active \"TRUE\" -LocalActive \"TRUE\" -Name {Modifier}")
            elif argument == 'ip_fragment_offset_mode':
                ip_fragment_offset_count = native_arg['ip_fragment_offset_count'] if 'ip_fragment_offset_count' in native_arg.keys() else "1"
                ip_fragment_offset_step = native_arg['ip_fragment_offset_step'] if 'ip_fragment_offset_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ip_fragment_offset_mode']+" -RecycleCount \""+ip_fragment_offset_count+"\" -StepValue {"+ip_fragment_offset_step+"} -DataType \"NATIVE\" -OffsetReference {"+ip_pdu_name+".fragOffset} -Name {Modifier} -Mask {8191} -Active \"TRUE\" -LocalActive \"TRUE\"  -Data {0} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")
            elif argument == 'ip_id_mode':
                ip_id_count = native_arg['ip_id_count'] if 'ip_id_count' in native_arg.keys() else "1"
                ip_id_step = native_arg['ip_id_step'] if 'ip_id_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ip_id_mode']+" -RecycleCount \""+ip_id_count+"\" -StepValue {"+ip_id_step+"} -DataType \"NATIVE\" -OffsetReference {"+ip_pdu_name+".identification} -Name {Modifier} -Mask {65535} -Active \"TRUE\" -LocalActive \"TRUE\"  -Data {0} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")
            elif argument == 'ip_protocol_mode':
                ip_protocol_count = native_arg['ip_protocol_count'] if 'ip_protocol_count' in native_arg.keys() else "1"
                ip_protocol_step = native_arg['ip_protocol_step'] if 'ip_protocol_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ip_protocol_mode']+" -RecycleCount \""+ip_protocol_count+"\" -StepValue {"+ip_protocol_step+"} -DataType \"NATIVE\" -OffsetReference {"+ip_pdu_name+".protocol} -Name {Modifier} -Mask {255} -Active \"TRUE\" -LocalActive \"TRUE\" -Data {253} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")
            elif argument == 'ip_reserved':
                tosdiffserv = rt_handle.invoke('invoke', cmd='stc::get '+ipv4_handle+' -children-tosdiffserv')
                tos = rt_handle.invoke('invoke', cmd='stc::get '+tosdiffserv+' -children-tos')
                rt_handle.invoke('invoke', cmd='stc::config '+tos+' -reserved' + " " + native_arg['ip_reserved'])
            elif argument == 'ip_ttl_mode':
                ip_ttl_count = native_arg['ip_ttl_count'] if 'ip_ttl_count' in native_arg.keys() else "1"
                ip_ttl_step = native_arg['ip_ttl_step'] if 'ip_ttl_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd="stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ip_ttl_mode']+" -RecycleCount \""+ip_ttl_count+"\" -StepValue {"+ip_ttl_step+"} -DataType \"NATIVE\" -OffsetReference {"+ip_pdu_name+".ttl} -Name {Modifier} -Mask {255} -Active \"TRUE\" -LocalActive \"TRUE\"  -Data {255} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")
            elif argument == 'ipv6_flow_label_mode':
                ipv6_flow_label_count = native_arg['ipv6_flow_label_count'] if 'ipv6_flow_label_count' in native_arg.keys() else "1"
                ipv6_flow_label_step = native_arg['ipv6_flow_label_step'] if 'ipv6_flow_label_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd = "stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ipv6_flow_label_mode']+" -RecycleCount \""+ipv6_flow_label_count+"\" -StepValue {"+ipv6_flow_label_step+"} -DataType \"NATIVE\" -OffsetReference {"+ipv6_pdu_name+".flowLabel} -Name {Modifier} -Mask {65535} -Active \"TRUE\" -LocalActive \"TRUE\" -Data {0} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")
            elif argument == 'ipv6_hop_limit_mode':
                ipv6_hop_limit_count = native_arg['ipv6_hop_limit_count'] if 'ipv6_hop_limit_count' in native_arg.keys() else "1"
                ipv6_hop_limit_step = native_arg['ipv6_hop_limit_step'] if 'ipv6_hop_limit_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd = "stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ipv6_hop_limit_mode']+" -RecycleCount \""+ipv6_hop_limit_count+"\" -StepValue {"+ipv6_hop_limit_step+"} -DataType \"NATIVE\" -OffsetReference {"+ipv6_pdu_name+".hopLimit} -Name {Modifier} -Mask {255} -Active \"TRUE\" -LocalActive \"TRUE\" -Data {255} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")
            elif argument == 'ipv6_traffic_class_mode':
                ipv6_traffic_class_count = native_arg['ipv6_traffic_class_count'] if 'ipv6_traffic_class_count' in native_arg.keys() else "1"
                ipv6_traffic_class_step = native_arg['ipv6_traffic_class_step'] if 'ipv6_traffic_class_step' in native_arg.keys() else "1"
                rt_handle.invoke('invoke', cmd = "stc::create \"RangeModifier\" -under "+hand+" -ModifierMode "+native_arg['ipv6_traffic_class_mode']+" -RecycleCount \""+ipv6_traffic_class_count+"\" -StepValue {"+ipv6_traffic_class_step+"} -DataType \"NATIVE\" -OffsetReference {"+ipv6_pdu_name+".trafficClass} -Name {Modifier} -Mask {255} -Active \"TRUE\" -LocalActive \"TRUE\" -Data {0} -Offset \"0\" -EnableStream \""+native_arg['enable_stream']+"\" -RepeatCount \"0\"")


    return None


def invoke_handle(rt_handle, protocol_string=jNone, port_handle=jNone, **args):
    hltapi = inspect.stack()[1][3]
    hltapi = re.sub(r'j_', '', hltapi)
    handle = args['handle']
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    handle_list = dict()
    if port_handle != jNone:
        del args['handle']
    for hndl in handle:
        status = 1
        ret = dict()
        for hnd in global_config[hndl]:
            if hnd in handle_list:
                continue
            else:
                handle_list[hnd] = 1
            if port_handle != jNone:
                args['port_handle'] = __get_handle(hndl)
            else:
                args['handle'] = hnd
            newer_ret = rt_handle.invoke(hltapi, **args)
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'handle' in newer_ret:
                global_config[protocol_string].append(newer_ret['handle'])
            for key in newer_ret:
                ret[key] = ret.get(key, [])
                ret[key].append(newer_ret[key])
        for key in ret:
            if len(ret[key]) == 1:
                ret[key] = ret[key][0]
        if 'status' in ret:
            ret['status'] = status
        if 'handles' in ret:
            ret['handle'] = ret['handles']
        ret['handles'] = protocol_string
    return ret
    
def configure_modifier(rt_handle, handles=jNone, argument=jNone, modifier_start=jNone, modifier_step=jNone, modifier_count=jNone):
    """
        Usage :
          configre_handle(rt_handle, handles=[list_of_handles],argument=’router_id’,modifier_start=’1.1.1.1’,modifier_step=’0.0.1.0’)
    """
    ## Adding below code to increment step value for ip address properly for all handles

    if handles == jNone or argument == jNone or modifier_start == jNone or modifier_step == jNone:
        rt_handle.log("ERROR","All arguments (handles,argument,modifier_start,modifier_step) are mandatory for configure_modifier api")
        return jNone

    modifier_list = []
    ip_list = []
    if modifier_count == jNone:
        modifier_count = len(handles)
    is_ip = None

    if re.match('(\d+\.){3}\d+', modifier_step) or ':' in modifier_step :
        ip_list = _make_ip_list(first = modifier_start, count = modifier_count, step = modifier_step)
        is_ip = True
    elif re.match('^\d+$', modifier_step):
        modifier_list = range(modifier_start, modifier_count + 1)

    if is_ip:
        modifier_list = [next(ip_list) for i in range(0, int(modifier_count))]

    for hand, modifier in zip(handles, modifier_list):
        rt_handle.invoke('invoke', cmd='stc::config '+ hand + ' -'+ argument + ' '+ modifier)
    rt_handle.invoke('invoke', cmd='stc::apply')

    return True    

def j_emulation_bfd_config(
        rt_handle,
        count=jNone,
        detect_multiplier=jNone,
        echo_rx_interval=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        gateway_ipv6_addr=jNone,
        gateway_ipv6_addr_step=jNone,
        handle=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_ipv6_addr=jNone,
        intf_ipv6_addr_step=jNone,
        ip_version=jNone,
        local_mac_addr=jNone,
        local_mac_addr_step=jNone,
        mode=jNone,
        remote_ip_addr=jNone,
        remote_ip_addr_step=jNone,
        remote_ipv6_addr=jNone,
        remote_ipv6_addr_step=jNone,
        vlan_id1=jNone,
        vlan_id2=jNone,
        vlan_id_mode1=jNone,
        vlan_id_mode2=jNone,
        vlan_id_step1=jNone,
        vlan_id_step2=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param count
    :param detect_multiplier - <2-100>
    :param echo_rx_interval - <0-10000>
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param gateway_ipv6_addr
    :param gateway_ipv6_addr_step
    :param handle
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_ipv6_addr
    :param intf_ipv6_addr_step
    :param ip_version - <IPv4:4|IPv6:6>
    :param local_mac_addr
    :param local_mac_addr_step
    :param mode - <create|modify|delete>
    :param remote_ip_addr
    :param remote_ip_addr_step
    :param remote_ipv6_addr
    :param remote_ipv6_addr_step
    :param vlan_id1 - <0-4095>
    :param vlan_id2 - <0-4095>
    :param vlan_id_mode1 - <fixed|increment>
    :param vlan_id_mode2 - <fixed|increment>
    :param vlan_id_step1 - <0-4095>
    :param vlan_id_step2 - <0-4095>
    :param port_handle

    Spirent Returns:


    IXIA Returns:
    {
        "bfd_router_handle": "/topology:1/deviceGroup:1/bfdRouter:2",
        "bfd_v4_interface_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1",
        "bfd_v4_session_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1/bfdv4Session",
        "handle": "/topology:1/deviceGroup:1/bfdRouter:2/item:1",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1",
        "interfaces": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1/item:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['count'] = count
    args['detect_multiplier'] = detect_multiplier
    args['echo_rx_interval'] = echo_rx_interval
    args['gateway_ip_addr'] = gateway_ip_addr
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['gateway_ipv6_addr'] = gateway_ipv6_addr
    args['gateway_ipv6_addr_step'] = gateway_ipv6_addr_step
    args['handle'] = handle
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_ipv6_addr'] = intf_ipv6_addr
    args['intf_ipv6_addr_step'] = intf_ipv6_addr_step
    args['ip_version'] = ip_version
    args['local_mac_addr'] = local_mac_addr
    args['local_mac_addr_step'] = local_mac_addr_step
    args['mode'] = mode
    args['remote_ip_addr'] = remote_ip_addr
    args['remote_ip_addr_step'] = remote_ip_addr_step
    args['remote_ipv6_addr'] = remote_ipv6_addr
    args['remote_ipv6_addr_step'] = remote_ipv6_addr_step
    args['vlan_id1'] = vlan_id1
    args['vlan_id2'] = vlan_id2
    args['vlan_id_mode1'] = vlan_id_mode1
    args['vlan_id_mode2'] = vlan_id_mode2
    args['vlan_id_step1'] = vlan_id_step1
    args['vlan_id_step2'] = vlan_id_step2
    args['port_handle'] = port_handle

    args = get_arg_value(rt_handle, j_emulation_bfd_config.__doc__, **args)
    
    if port_handle == jNone:
        __check_and_raise(handle)
    elif handle == jNone:
        __check_and_raise(port_handle)

    counter = 1
    string = "bfd_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "bfd_" + str(counter)
    global_config[string] = []
    ret = []
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
  
    if 'handle' in args.keys():
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    args['handle'] = hnd
                    if mode == 'create' or mode == 'enable' and port_handle == jNone:
                        del args['handle']
                        bfd_handle = rt_handle.invoke('invoke', cmd='stc::get '+hnd+' -AffiliatedPort')
                        args['port_handle'] = bfd_handle
                    result = rt_handle.invoke('emulation_bfd_config', **args)
                    if result.get('handle'):
                        global_config[string].extend([result['handle']])
                        result['handles'] = string
                    if mode == 'enable' or mode == 'create':
                        handle_map[hnd] = handle_map.get(hnd, [])
                        handle_map[hnd].extend(global_config[string])
                        handle_map[string] = hnd
                    ret.append(result)
            else:
                args['handle'] = hndl
                if mode == 'create' or mode == 'enable' and port_handle == jNone:
                    del args['handle']
                    bfd_handle = rt_handle.invoke('invoke', cmd='stc::get '+hndl+' -AffiliatedPort')
                    args['port_handle'] = bfd_handle
                result = rt_handle.invoke('emulation_bfd_config', **args)
                if result.get('handle'):
                    result['handles'] = string
                if mode == 'enable' or mode == 'create':
                        handle_map[hndl] = handle_map.get(hndl, [])
                        handle_map[hndl].extend(global_config[string])
                        handle_map[string] = hndl
                ret.append(result)

    elif 'port_handle' in args.keys():
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        result = rt_handle.invoke('emulation_bfd_config', **args)
        if result.get('handle'):
            global_config[string].extend([result['handle']])
            result['handles'] = string
        for hand in port_handle:
            handle_map[hand] = handle_map.get(hand, [])
            handle_map[hand].extend(global_config[string])
            handle_map[string] = hand
        ret.append(result)

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bfd_control(rt_handle, handle=jNone,
                            mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|resume_pdus:resume_pdu|stop_pdus:stop_pdu|enable_demand:demand_mode_enable|disable_demand:demand_mode_disable|initiate_poll|admin_up:set_admin_up|admin_down:set_admin_down>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    __check_and_raise(handle)

    args = get_arg_value(rt_handle, j_emulation_bfd_control.__doc__, **args)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                ret.append(rt_handle.invoke('emulation_bfd_control', **args))
        else:
            args['handle'] = hndl
            ret.append(rt_handle.invoke('emulation_bfd_control', **args))

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bfd_info(rt_handle, handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle

    Spirent Returns:


    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1": {
            "bfd_learned_info": {
                "device#": "{1}",
                "my_discriminator": "{1}",
                "my_ip_address": "{3.3.3.1}",
                "peer_discriminator": "{1}",
                "peer_ip_address": "{3.3.3.2}",
                "peer_session_state": "{Up}",
                "recvd_min_rx_interval": "{1000}",
                "recvd_multiplier": "{3}",
                "recvd_peer_flags": "{P=0| F=0| C=0| A=0| D=0|}",
                "recvd_tx_interval": "{1000}",
                "session_state": "{Up}",
                "session_type": "{Single Hop}",
                "session_up_time": "{19}",
                "session_used_by_protocol": "{NONE}"
            }
        },
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1/item:1": {
            "session": {
                "control_pkts_rx": "27",
                "control_pkts_tx": "28",
                "echo_dut_pkts_rx": "0",
                "echo_dut_pkts_tx": "0",
                "echo_self_pkts_rx": "0",
                "echo_self_pkts_tx": "0",
                "mpls_rx": "0",
                "mpls_tx": "0",
                "port_name": "1/11/2",
                "session_flap_cnt": "0",
                "sessions_auto_created": "0",
                "sessions_auto_created_up": "0",
                "sessions_configured": "1",
                "sessions_configured_up": "1"
            }
        },
        "1/11/2": {
            "aggregate": {
                "control_pkts_rx": "21",
                "control_pkts_tx": "22",
                "echo_dut_pkts_rx": "0",
                "echo_dut_pkts_tx": "0",
                "echo_self_pkts_rx": "0",
                "echo_self_pkts_tx": "0",
                "mpls_rx": "0",
                "mpls_tx": "0",
                "port_name": "1/11/2",
                "session_flap_cnt": "0",
                "sessions_auto_created": "0",
                "sessions_auto_created_up": "0",
                "sessions_configured": "1",
                "sessions_configured_up": "1",
                "status": "started"
            }
        },
        "Device Group 1": {
            "Bfdv4 Stats Per Device": {
                "control_pkts_rx": "25",
                "control_pkts_tx": "26",
                "echo_dut_pkts_rx": "0",
                "echo_dut_pkts_tx": "0",
                "echo_self_pkts_rx": "0",
                "echo_self_pkts_tx": "0",
                "mpls_rx": "0",
                "mpls_tx": "0",
                "session_flap_cnt": "0",
                "sessions_auto_created": "0",
                "sessions_auto_created_up": "0",
                "sessions_configured": "1",
                "sessions_configured_up": "1",
                "status": "started"
            }
        },
        "bfd_session_state": "{Up}",
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    ret = []
    for hndl in handle:
        new_ret = dict()
        status = 1
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                newer_ret = dict()
                args['mode'] = 'aggregate_stats'
                newer_ret.update(rt_handle.invoke('emulation_bfd_info', **args))
                args['mode'] = 'learned_info'
                newer_ret.update(rt_handle.invoke('emulation_bfd_info', **args))

                if 'status' in newer_ret:
                    if newer_ret['status'] == 0:
                        status = 0
                for key in newer_ret:
                    try:
                        new_ret[key]
                    except:
                        new_ret[key] = []
                    new_ret[key].append(newer_ret[key])
                for key in new_ret:
                    if len(new_ret[key]) == 1:
                        new_ret[key] = new_ret[key][0]
                if 'status' in new_ret:
                    new_ret['status'] = status
                if new_ret:
                    ret.append(new_ret)
        else:
            args['handle'] = hndl
            newer_ret = dict()
            args['mode'] = 'aggregate_stats'
            newer_ret.update(rt_handle.invoke('emulation_bfd_info', **args))
            args['mode'] = 'learned_info'
            newer_ret.update(rt_handle.invoke('emulation_bfd_info', **args))

            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
            for key in new_ret:
                if len(new_ret[key]) == 1:
                    new_ret[key] = new_ret[key][0]
            if 'status' in new_ret:
                new_ret['status'] = status
            if new_ret:
                ret.append(new_ret)

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bgp_config(
        rt_handle,
        bfd_registration=jNone,
        count=jNone,
        graceful_restart_enable=jNone,
        handle=jNone,
        ip_version=jNone,
        local_as=jNone,
        local_as4=jNone,
        local_as_mode=jNone,
        local_ip_addr=jNone,
        local_ipv6_addr=jNone,
        local_router_id_step=jNone,
        mac_address_start=jNone,
        md5_enable=jNone,
        md5_key=jNone,
        netmask=jNone,
        remote_ip_addr=jNone,
        remote_ipv6_addr=jNone,
        restart_time=jNone,
        staggered_start_time=jNone,
        stale_time=jNone,
        update_interval=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        remote_as=jNone,
        router_id=jNone,
        neighbor_type=jNone,
        ipv4_unicast_nlri=jNone,
        next_hop_ip=jNone,
        ipv4_mpls_nlri=jNone,
        ipv4_mpls_vpn_nlri=jNone,
        ipv4_multicast_nlri=jNone,
        hold_time=jNone,
        vpls_nlri=jNone,
        retry_time=jNone,
        retries=jNone,
        local_as_step=jNone,
        local_addr_step=jNone,
        remote_addr_step=jNone,
        ipv6_mpls_nlri=jNone,
        ipv6_mpls_vpn_nlri=jNone,
        ipv6_unicast_nlri=jNone,
        ttl_value=jNone,
        remote_loopback_ip_addr=jNone,
        ipv6_multicast_nlri=jNone,
        asnum_4byte_enable=jNone,
        local_ipv6_addr_step=jNone,
        remote_ipv6_addr_step=jNone,
        active_connect_enable=jNone,
        local_router_id_enable=jNone,
        bfd_registration_mode=jNone,
        gateway_ip_addr=jNone,
        next_hop_enable=jNone,
        netmask_ipv6=jNone,
        next_hop_ipv6=jNone,
        ipv4_multicast_vpn_nlri=jNone,
        ipv6_multicast_vpn_nlri=jNone,
        vpls_multicast_nlri=jNone,
        vpls_multicast_vpn_nlri=jNone,
        port_handle=jNone,
        staggered_start_enable=jNone,
        next_hop_ip_step=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone,
        ipv4_srtepolicy_nlri=jNone,
        ipv6_srtepolicy_nlri=jNone,
        bgp_stack_multiplier=jNone,
        ipv4_mpls_capability=jNone,
        bgp_session_ip_addr=jNone):
    """
    :param rt_handle:       RT object
    :param bfd_registration
    :param count
    :param graceful_restart_enable
    :param handle
    :param ip_version
    :param local_as - <1-65535>
    :param local_as4
    :param local_as_mode - <fixed|increment>
    :param local_ip_addr
    :param local_ipv6_addr
    :param local_router_id_step
    :param mac_address_start
    :param md5_enable
    :param md5_key
    :param netmask - <1-128>
    :param remote_ip_addr
    :param remote_ipv6_addr
    :param restart_time
    :param staggered_start_time - <0-10000>
    :param stale_time - <0-10000>
    :param update_interval - <0-10000>
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <1-4094>
    :param vlan_user_priority - <0-7>
    :param mode - <enable|disable|modify|reset>
    :param remote_as - <0-65535>
    :param router_id
    :param neighbor_type - <ibgp:internal|ebgp:external>
    :param ipv4_unicast_nlri
    :param next_hop_ip
    :param ipv4_mpls_nlri
    :param ipv4_mpls_vpn_nlri
    :param ipv4_multicast_nlri
    :param hold_time - <3-65535>
    :param vpls_nlri
    :param retry_time
    :param retries - <0-65535>
    :param local_as_step - <0-65535>
    :param local_addr_step
    :param remote_addr_step
    :param ipv6_mpls_nlri
    :param ipv6_mpls_vpn_nlri
    :param ipv6_unicast_nlri
    :param ttl_value
    :param remote_loopback_ip_addr
    :param ipv6_multicast_nlri
    :param asnum_4byte_enable
    :param local_ipv6_addr_step
    :param remote_ipv6_addr_step
    :param active_connect_enable
    :param local_router_id_enable - <1>
    :param bfd_registration_mode - <single_hop|multi_hop>
    :param gateway_ip_addr
    :param next_hop_enable - <1>
    :param netmask_ipv6 - <1-128>
    :param next_hop_ipv6
    :param ipv4_multicast_vpn_nlri
    :param ipv6_multicast_vpn_nlri
    :param vpls_multicast_nlri
    :param vpls_multicast_vpn_nlri
    :param port_handle
    :param staggered_start_enable
    :param next_hop_ip_step
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_step - <1-4094>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_user_priority - <0-7>
    :param ipv4_srtepolicy_nlri - <0|1>
    :param ipv6_srtepolicy_nlri - <0|1>
    :param bgp_stack_multiplier
    :param ipv4_mpls_capability - <0|1>
    :param bgp_session_ip_addr - <router_id>


    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "bgp_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['bfd_registration'] = bfd_registration
    args['count'] = count
    args['graceful_restart_enable'] = graceful_restart_enable
    args['handle'] = handle
    args['ip_version'] = ip_version
    args['local_as'] = local_as
    args['local_as4'] = local_as4
    args['local_as_mode'] = local_as_mode
    args['local_ip_addr'] = local_ip_addr
    args['local_ipv6_addr'] = local_ipv6_addr
    args['local_router_id_step'] = local_router_id_step
    args['mac_address_start'] = mac_address_start
    args['md5_enable'] = md5_enable
    args['md5_key'] = md5_key
    args['netmask'] = netmask
    args['remote_ip_addr'] = remote_ip_addr
    args['remote_ipv6_addr'] = remote_ipv6_addr
    args['restart_time'] = restart_time
    args['staggered_start_time'] = staggered_start_time
    args['stale_time'] = stale_time
    args['update_interval'] = update_interval
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['remote_as'] = remote_as
    args['neighbor_type'] = neighbor_type
    args['ipv4_unicast_nlri'] = ipv4_unicast_nlri
    args['next_hop_ip'] = next_hop_ip
    args['ipv4_mpls_nlri'] = ipv4_mpls_nlri
    args['ipv4_mpls_vpn_nlri'] = ipv4_mpls_vpn_nlri
    args['ipv4_multicast_nlri'] = ipv4_multicast_nlri
    args['hold_time'] = hold_time
    args['vpls_nlri'] = vpls_nlri
    args['retry_time'] = retry_time
    args['retries'] = retries
    args['local_as_step'] = local_as_step
    args['local_addr_step'] = local_addr_step
    args['remote_ip_addr_step'] = remote_addr_step
    args['ipv6_mpls_nlri'] = ipv6_mpls_nlri
    args['ipv6_mpls_vpn_nlri'] = ipv6_mpls_vpn_nlri
    args['ipv6_multicast_nlri'] = ipv6_multicast_nlri
    args['ipv6_unicast_nlri'] = ipv6_unicast_nlri
    args['remote_loopback_ip_addr'] = remote_loopback_ip_addr
    args['asnum_4byte_enable'] = asnum_4byte_enable
    args['local_ipv6_addr_step'] = local_ipv6_addr_step
    args['remote_ipv6_addr_step'] = remote_ipv6_addr_step
    args['active_connect_enable'] = active_connect_enable
    args['gateway_ip_addr'] = gateway_ip_addr
    args['netmask_ipv6'] = netmask_ipv6
    args['next_hop_ipv6'] = next_hop_ipv6
    args['ipv4_multicast_vpn_nlri'] = ipv4_multicast_vpn_nlri
    args['ipv6_multicast_vpn_nlri'] = ipv6_multicast_vpn_nlri
    args['vpls_multicast_nlri'] = vpls_multicast_nlri
    args['vpls_multicast_vpn_nlri'] = vpls_multicast_vpn_nlri
    args['port_handle'] = port_handle
    args['staggered_start_enable'] = staggered_start_enable
    args['next_hop_ip_step'] = next_hop_ip_step
    args['vlan_outer_id'] = vlan_outer_id
    args['vlan_outer_id_step'] = vlan_outer_id_step
    args['vlan_outer_id_mode'] = vlan_outer_id_mode
    args['vlan_outer_user_priority'] = vlan_outer_user_priority
    args['ipv4_srtepolicy_nlri'] = ipv4_srtepolicy_nlri
    args['ipv6_srtepolicy_nlri'] = ipv6_srtepolicy_nlri
    args['bgp_session_ip_addr'] = bgp_session_ip_addr

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_bgp_config.__doc__, **args)

    if 'neighbor_type' in args:
        args['bgp_mode'] = args['neighbor_type']
        del args['neighbor_type']

    if port_handle == jNone:
        __check_and_raise(handle)
    elif handle == jNone:
        __check_and_raise(port_handle)

    if 'local_as4' in args.keys():
        args['local_as4'] = str(local_as4)+':'+str(local_as4)
        
    if 'ip_version' in args.keys():
        if ip_version == '4' or ip_version == '6':
            args['ip_stack_version'] = '4_6'
    if bgp_stack_multiplier != jNone:
        args['local_router_id_step'] = '0.0.0.0'
        args['local_addr_step'] = '0.0.0.0'
        args['next_hop_ip_step'] = '0.0.0.0'
        args['count'] = bgp_stack_multiplier

    if router_id !=jNone:
        args['local_router_id'] = router_id
        
    if  router_id != jNone and  local_router_id_step == jNone:
        args['local_router_id_step'] = '0.0.0.1'

    if  remote_ip_addr  !=jNone and  remote_addr_step == jNone:
        args['remote_ip_addr_step'] = '0.0.0.1'
        
    if 'gateway_ip_addr' in args.keys():
        del args['gateway_ip_addr']
        args['next_hop_ip'] = gateway_ip_addr

    if ipv4_mpls_capability != jNone:
        args['ipv4_mpls_nlri'] = ipv4_mpls_capability

    if remote_ipv6_addr != jNone and remote_ipv6_addr_step == jNone:
       args['remote_ipv6_addr_step'] = '::1'

    counter = 1
    string = "bgp_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "bgp_" + str(counter)
    global_config[string] = []
    ret = []
    if handle != jNone:
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                ret.append(invoke_handle(rt_handle, protocol_string=string, **args))
                break
            else:
                args['handle'] = hndl
                result = rt_handle.invoke('emulation_bgp_config', **args)
                if result.get('handles'):
                    global_config[string].extend(result['handles'].split(' '))
#               result['handle'] = result['handles']
                    result['handles'] = string
                ret.append(result)
        if mode == 'create':
            for hndl in handle:
                if hndl in global_config.keys():
                    port_handle = __get_handle(hndl)
                else:
                    port_handle = rt_handle.invoke('invoke', cmd='stc::get '+hndl+' -AffiliatedPort')
                handle_map[port_handle].extend(global_config[string])
                handle_map[string] = port_handle
    elif port_handle != jNone:
        result = rt_handle.invoke('emulation_bgp_config', **args)
        if result.get('handle'):
            global_config[string].extend(result['handle'].split(' '))
            result['handles'] = string
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        for hand in port_handle:
            handle_map[hand] = handle_map.get(hand, [])
            handle_map[hand].extend(global_config[string])
            handle_map[string] = hand
        ret.append(result)

    if bfd_registration_mode != jNone:
        convergence_param_handle = rt_handle.invoke('invoke', cmd='stc::create' + " " + 'ConvergenceGenParams -under project1')
        if bfd_registration_mode == 'single_hop':
            rt_handle.invoke('invoke', cmd='stc::config' + " " + convergence_param_handle + " " + '-Protocol ' + 'SINGLE_HOP_BGP')
        if bfd_registration_mode == 'multi_hop':
            rt_handle.invoke('invoke', cmd='stc::config' + " " + convergence_param_handle + " " + '-Protocol ' + 'MULTI_HOP_BGP')
        rt_handle.invoke('invoke', cmd='stc::apply')

    if ttl_value != jNone:
        access_testgenconfig_expand_command_handle = rt_handle.invoke('invoke', cmd='stc::create' + " " + 'AccessStabilityGenParams -under project1')
        rt_handle.invoke('invoke', cmd='stc::config' + " " + access_testgenconfig_expand_command_handle + " " + '-Ttl ' + ttl_value)
        rt_handle.invoke('invoke', cmd='stc::apply')

    if 'handle' in args.keys():
        emu_handles = global_config[string]
        if 'local_router_id' in args.keys() and 'local_router_id_step' in args.keys():
            configure_modifier(rt_handle, handles=emu_handles, argument='RouterId', modifier_start=args['local_router_id'], modifier_step=args['local_router_id_step'])

        if 'remote_ip_addr' in args.keys() and 'remote_ip_addr_step' in args.keys():
            bgp_handles = [rt_handle.invoke('invoke', cmd='stc::get '+ hand + ' -children-BgpRouterConfig') for hand in emu_handles]
            configure_modifier(rt_handle, handles=bgp_handles, argument='DutIpv4Addr', modifier_start=args['remote_ip_addr'], modifier_step=args['remote_ip_addr_step'])
        if 'remote_ipv6_addr' in args.keys() and 'remote_ipv6_addr_step' in args.keys():
            bgp_handles = [rt_handle.invoke('invoke', cmd='stc::get '+ hand + ' -children-BgpRouterConfig') for hand in emu_handles]
            configure_modifier(rt_handle, handles=bgp_handles, argument='DutIpv6Addr', modifier_start=args['remote_ipv6_addr'], modifier_step=args['remote_ipv6_addr_step'])

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****
    #Native args execution starts here

    return ret



def j_emulation_bgp_control(
        rt_handle,
        handle=jNone,
        mode=jNone,
        route_flap_down_time=jNone,
        route_flap_up_time=jNone,
        flap_count=jNone,
        route_handle=jNone,
        link_flap_up_time=jNone,
        link_flap_down_time=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|restart|link_flap|full_route_flap>
    :param route_flap_down_time - <0-10000000>
    :param route_flap_up_time - <0-10000000>
    :param flap_count
    :param route_handle
    :param link_flap_up_time - <0-10000000>
    :param link_flap_down_time - <0-10000000>


    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode
    args['route_flap_down_time'] = route_flap_down_time
    args['route_flap_up_time'] = route_flap_up_time
    args['flap_count'] = flap_count
    args['route_handle'] = route_handle
    args['link_flap_up_time'] = link_flap_up_time
    args['link_flap_down_time'] = link_flap_down_time



    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    
    args = get_arg_value(rt_handle, j_emulation_bgp_control.__doc__, **args)
 
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if 'route_handle' in args and not isinstance(route_handle, list):
        route_handle = [route_handle]
        route_handle = list(set(route_handle))
    ret = []
    if mode == 'full_route_flap':
        for hand, rh in zip(handle, route_handle):
            if hand in global_config.keys() and rh in global_config.keys():
                for bgp, bgp_route in zip(global_config[hand], global_config[rh]):
                    args['handle'] = bgp
                    args['route_handle'] = bgp_route
                    ret.append(rt_handle.invoke('emulation_bgp_control', **args))
            else:
                args['handle'] = handle
                args['route_handle'] = route_handle
                ret.append(rt_handle.invoke('emulation_bgp_control', **args))
    else:
        for hndl in handle:
            if hndl in global_config.keys():
                hnd = " ".join(global_config[hndl])
                args['handle'] = hnd
                ret.append(rt_handle.invoke('emulation_bgp_control', **args))
            else:
                args['handle'] = hndl
                ret.append(rt_handle.invoke('emulation_bgp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bgp_info(rt_handle, handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle

    Spirent Returns:
    {
        "asn": "100",
        "ip_address": "192.85.1.3",
        "keepalive_rx": "0",
        "keepalive_tx": "0",
        "last_routes_advertised_rx": "0",
        "notify_code_rx": "0",
        "notify_code_tx": "0",
        "notify_rx": "0",
        "notify_subcode_rx": "0",
        "notify_subcode_tx": "0",
        "notify_tx": "0",
        "num_node_routes": "0",
        "open_rx": "0",
        "open_tx": "0",
        "peers": "3.3.3.2",
        "route_withdrawn_tx": "0",
        "routes_advertised_rx": "0",
        "routes_advertised_tx": "0",
        "routes_withdrawn_rx": "0",
        "routes_withdrawn_tx": "0",
        "sessions_configured": "1",
        "sessions_established": "0",
        "status": "1",
        "update_rx": "0",
        "update_tx": "0"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1/item:1": {
            "session": {
                "Hold_timer_expireds_rx": "0",
                "active_on": "True",
                "attribute_flags_error": "0",
                "attribute_length_error": "0",
                "bad_bgp_id_rx": "0",
                "bad_peer_as_rx": "0",
                "error_link_state_nlri_rx": "0",
                "external_connects_accepted": "1",
                "external_connects_rx": "1",
                "fsm_state": "Established",
                "graceful_restart_attempted": "0",
                "graceful_restart_failed": "0",
                "hold_timer_expireds_tx": "0",
                "invalid_network_field": "0",
                "invalid_next_hop_attribute": "0",
                "invalid_opens_rx": "0",
                "invalid_opens_tx": "0",
                "invalid_origin_attribute": "0",
                "keepalive_rx": "3",
                "keepalive_tx": "3",
                "last_error_rx": "0",
                "last_error_tx": "0",
                "ls_ipv4_prefix_advertised_rx": "0",
                "ls_ipv4_prefix_advertised_tx": "0",
                "ls_ipv4_prefix_withdrawn_rx": "0",
                "ls_ipv4_prefix_withdrawn_tx": "0",
                "ls_ipv6_prefix_advertised_rx": "0",
                "ls_ipv6_prefix_advertised_tx": "0",
                "ls_ipv6_prefix_withdrawn_rx": "0",
                "ls_ipv6_prefix_withdrawn_tx": "0",
                "ls_link_advertised_rx": "0",
                "ls_link_advertised_tx": "0",
                "ls_link_withdrawn_rx": "0",
                "ls_link_withdrawn_tx": "0",
                "ls_node_advertised_rx": "0",
                "ls_node_advertised_tx": "0",
                "ls_node_withdrawn_rx": "0",
                "ls_node_withdrawn_tx": "0",
                "malformed_as_path": "0",
                "messages_rx": "5",
                "messages_tx": "5",
                "notify_rx": "0",
                "notify_tx": "0",
                "open_rx": "1",
                "open_tx": "1",
                "route_withdraws_rx": "0",
                "routes_advertised": "1",
                "routes_rx": "1",
                "routes_rx_graceful_restart": "0",
                "routes_withdrawn": "0",
                "session_status": "Up",
                "starts_occurred": "1",
                "update_errors_rx": "0",
                "update_errors_tx": "0",
                "update_rx": "1",
                "update_tx": "1"
            }
        },
        "1/11/2": {
            "aggregate": {
                "Hold_timer_expireds_rx": "0",
                "active_state": "0",
                "as_routing_loop": "0",
                "attribute_flags_error": "0",
                "attribute_length_error": "0",
                "authentication_failures_rx": "0",
                "bad_bgp_id_rx": "0",
                "bad_message_length": "0",
                "bad_message_type": "0",
                "bad_peer_as_rx": "0",
                "ceases_rx": "0",
                "ceases_tx": "0",
                "connect_state": "0",
                "connection_not_synchronized": "0",
                "error_link_state_nlri_rx": "0",
                "established_state": "1",
                "external_connects_accepted": "1",
                "external_connects_rx": "1",
                "graceful_restart_attempted": "0",
                "graceful_restart_failed": "0",
                "header_errors_rx": "0",
                "header_errors_tx": "0",
                "hold_timer_expireds_tx": "0",
                "idle_state": "0",
                "invalid_header_suberror_unspecified": "0",
                "invalid_network_field": "0",
                "invalid_next_hop_attribute": "0",
                "invalid_open_suberror_unspecified": "0",
                "invalid_opens_rx": "0",
                "invalid_opens_tx": "0",
                "invalid_origin_attribute": "0",
                "invalid_update_suberror_unspecified": "0",
                "keepalive_rx": "3",
                "keepalive_tx": "3",
                "ls_ipv4_prefix_advertised_rx": "0",
                "ls_ipv4_prefix_advertised_tx": "0",
                "ls_ipv4_prefix_withdrawn_rx": "0",
                "ls_ipv4_prefix_withdrawn_tx": "0",
                "ls_ipv6_prefix_advertised_rx": "0",
                "ls_ipv6_prefix_advertised_tx": "0",
                "ls_ipv6_prefix_withdrawn_rx": "0",
                "ls_ipv6_prefix_withdrawn_tx": "0",
                "ls_link_advertised_rx": "0",
                "ls_link_advertised_tx": "0",
                "ls_link_withdrawn_rx": "0",
                "ls_link_withdrawn_tx": "0",
                "ls_node_advertised_rx": "0",
                "ls_node_advertised_tx": "0",
                "ls_node_withdrawn_rx": "0",
                "ls_node_withdrawn_tx": "0",
                "malformed_as_path": "0",
                "malformed_attribute_list": "0",
                "messages_rx": "5",
                "messages_tx": "5",
                "missing_well_known_attribute": "0",
                "non_acceptable_hold_times_rx": "0",
                "notify_rx": "0",
                "notify_tx": "0",
                "open_rx": "1",
                "open_tx": "1",
                "openconfirm_state": "0",
                "opentx_state": "0",
                "optional_attribute_error": "0",
                "port_name": "1/11/2",
                "route_withdraws_rx": "0",
                "routes_advertised": "1",
                "routes_rx": "1",
                "routes_rx_graceful_restart": "0",
                "routes_withdrawn": "0",
                "session_flap_count": "0",
                "sessions_configured": "1",
                "sessions_down": "0",
                "sessions_established": "1",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "starts_occurred": "1",
                "state_machine_errors_rx": "0",
                "state_machine_errors_tx": "0",
                "status": "started",
                "unrecognized_well_known_attribute": "0",
                "unspecified_error_rx": "0",
                "unspecified_error_tx": "0",
                "unsupported_parameters_rx": "0",
                "unsupported_versions_rx": "0",
                "update_errors_rx": "0",
                "update_errors_tx": "0",
                "update_rx": "1",
                "update_tx": "1"
            }
        },
        "Device Group 1": {
            "aggregate": {
                "Hold_timer_expireds_rx": "0",
                "active_state": "0",
                "as_routing_loop": "0",
                "attribute_flags_error": "0",
                "attribute_length_error": "0",
                "authentication_failures_rx": "0",
                "bad_bgp_id_rx": "0",
                "bad_message_length": "0",
                "bad_message_type": "0",
                "bad_peer_as_rx": "0",
                "ceases_rx": "0",
                "ceases_tx": "0",
                "connect_state": "0",
                "connection_not_synchronized": "0",
                "error_link_state_nlri_rx": "0",
                "established_state": "1",
                "external_connects_accepted": "1",
                "external_connects_rx": "1",
                "graceful_restart_attempted": "0",
                "graceful_restart_failed": "0",
                "header_errors_rx": "0",
                "header_errors_tx": "0",
                "hold_timer_expireds_tx": "0",
                "idle_state": "0",
                "invalid_header_suberror_unspecified": "0",
                "invalid_network_field": "0",
                "invalid_next_hop_attribute": "0",
                "invalid_open_suberror_unspecified": "0",
                "invalid_opens_rx": "0",
                "invalid_opens_tx": "0",
                "invalid_origin_attribute": "0",
                "invalid_update_suberror_unspecified": "0",
                "keepalive_rx": "3",
                "keepalive_tx": "3",
                "ls_ipv4_prefix_advertised_rx": "0",
                "ls_ipv4_prefix_advertised_tx": "0",
                "ls_ipv4_prefix_withdrawn_rx": "0",
                "ls_ipv4_prefix_withdrawn_tx": "0",
                "ls_ipv6_prefix_advertised_rx": "0",
                "ls_ipv6_prefix_advertised_tx": "0",
                "ls_ipv6_prefix_withdrawn_rx": "0",
                "ls_ipv6_prefix_withdrawn_tx": "0",
                "ls_link_advertised_rx": "0",
                "ls_link_advertised_tx": "0",
                "ls_link_withdrawn_rx": "0",
                "ls_link_withdrawn_tx": "0",
                "ls_node_advertised_rx": "0",
                "ls_node_advertised_tx": "0",
                "ls_node_withdrawn_rx": "0",
                "ls_node_withdrawn_tx": "0",
                "malformed_as_path": "0",
                "malformed_attribute_list": "0",
                "messages_rx": "5",
                "messages_tx": "5",
                "missing_well_known_attribute": "0",
                "non_acceptable_hold_times_rx": "0",
                "notify_rx": "0",
                "notify_tx": "0",
                "open_rx": "1",
                "open_tx": "1",
                "openconfirm_state": "0",
                "opentx_state": "0",
                "optional_attribute_error": "0",
                "route_withdraws_rx": "0",
                "routes_advertised": "1",
                "routes_rx": "1",
                "routes_rx_graceful_restart": "0",
                "routes_withdrawn": "0",
                "session_flap_count": "0",
                "sessions_configured": "1",
                "sessions_down": "0",
                "sessions_established": "1",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "starts_occurred": "1",
                "state_machine_errors_rx": "0",
                "state_machine_errors_tx": "0",
                "status": "started",
                "unrecognized_well_known_attribute": "0",
                "unspecified_error_rx": "0",
                "unspecified_error_tx": "0",
                "unsupported_parameters_rx": "0",
                "unsupported_versions_rx": "0",
                "update_errors_rx": "0",
                "update_errors_tx": "0",
                "update_rx": "1",
                "update_tx": "1"
            }
        },
        "asn": "100",
        "ip_address": "\"3.3.3.1\"",
        "keepalive_rx": "3",
        "keepalive_tx": "3",
        "notify_rx": "0",
        "notify_tx": "0",
        "open_rx": "1",
        "open_tx": "1",
        "peers": "3.3.3.2",
        "routes_advertised_rx": "1",
        "routes_advertised_tx": "1",
        "routes_withdrawn_rx": "0",
        "routes_withdrawn_tx": "0",
        "sessions_configured": "1",
        "sessions_established": "1",
        "status": "1",
        "update_rx": "1",
        "update_tx": "1"
    }

    Common Return Keys:
        "status"
        "asn"
        "ip_address"
        "keepalive_rx"
        "keepalive_tx"
        "notify_rx"
        "notify_tx"
        "open_rx"
        "open_tx"
        "peers"
        "routes_advertised_rx"
        "routes_advertised_tx"
        "routes_withdrawn_rx"
        "routes_withdrawn_tx"
        "sessions_configured"
        "sessions_established"
        "update_rx"
        "update_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        status = 1
        new_ret = dict()
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                newer_ret = dict()
                args['mode'] = 'stats'
                newer_ret.update(rt_handle.invoke('emulation_bgp_info', **args))
                args['mode'] = 'settings'
                newer_ret.update(rt_handle.invoke('emulation_bgp_info', **args))
                args['mode'] = 'neighbors'
                newer_ret.update(rt_handle.invoke('emulation_bgp_info', **args))
                args['mode'] = 'ls_results'
                newer_ret.update(rt_handle.invoke('emulation_bgp_info', **args))

                if 'status' in newer_ret:
                    if newer_ret['status'] == 0:
                        status = 0
                for key in newer_ret:
                    try:
                        new_ret[key]
                    except:
                        new_ret[key] = []
                    new_ret[key].append(newer_ret[key])
        else:
            args['handle'] = hndl
            newer_ret = dict()
            args['mode'] = 'stats'
            newer_ret.update(rt_handle.invoke('emulation_bgp_info', **args))
            args['mode'] = 'settings'
            newer_ret.update(rt_handle.invoke('emulation_bgp_info', **args))
            args['mode'] = 'neighbors'
            newer_ret.update(rt_handle.invoke('emulation_bgp_info', **args))
            args['mode'] = 'ls_results'
            newer_ret.update(rt_handle.invoke('emulation_bgp_info', **args))

            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if new_ret:
            ret.append(new_ret)

    # **** Add code to consolidate stats here ****

    for index in range(len(ret)):
        for key in ret[index]:
            if isinstance(ret[index][key], list):
                if 'sessions_configured' in key or 'sessions_established' in key or 'notify_subcode_rx' in key or 'open_rx' in key or 'routes_withdrawn_rx' in key or 'notify_code_tx' in key or 'keepalive_tx' in key or 'notify_tx' in key or 'last_routes_advertised_rx' in key or 'update_tx' in key or 'routes_withdrawn_tx' in key or 'open_tx' in key or 'routes_advertised_tx' in key or 'num_node_routes' in key or 'route_withdrawn_tx' in key or 'notify_code_rx' in key or 'update_rx' in key or 'notify_rx' in key or 'routes_advertised_rx' in key or 'notify_subcode_tx' in key or 'keepalive_rx' in key:
                    ret[index][key] = sum(list(map(int, ret[index][key])))

    # **** Add code to consolidate stats here ****


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_bgp_route_config(
        rt_handle,
        aggregator=jNone,
        handle=jNone,
        ip_version=jNone,
        ipv6_prefix_length=jNone,
        max_route_ranges=jNone,
        next_hop_ip_version=jNone,
        next_hop_set_mode=jNone,
        num_routes=jNone,
        origin=jNone,
        originator_id_enable=jNone,
        packing_to=jNone,
        rd_admin_value=jNone,
        rd_assign_step=jNone,
        route_handle=jNone,
        target=jNone,
        target_assign=jNone,
        prefix=jNone,
        mode=jNone,
        as_path=jNone,
        netmask=jNone,
        originator_id=jNone,
        rd_assign_value=jNone,
        rd_type=jNone,
        target_type=jNone,
        route_ip_addr_step=jNone,
        srte_ip_version=jNone,
        srte_aspath_segment_type=jNone,
        srte_community=jNone,
        srte_distinguisher=jNone,
        srte_endpoint=jNone,
        srte_local_pref=jNone,
        srte_nexthop=jNone,
        srte_origin=jNone,
        srte_policy_color=jNone,
        srte_binding_sid=jNone,
        srte_binding_sid_len=jNone,
        srte_color=jNone,
        srte_flags=jNone,
        srte_preference=jNone,
        srte_remote_endpoint_addr=jNone,
        srte_remote_endpoint_as=jNone,
        srte_segment_list_subtlv=jNone,
        srte_weight=jNone,
        ipv4_mpls_vpn_nlri=jNone,
        ipv4_unicast_nlri=jNone,
        label_id=jNone,
        label_incr_mode=jNone,
        label_step=jNone,
        local_pref=jNone,
        next_hop=jNone,
        min_lables=jNone,
        vpls_nlri=jNone,
        l2_enable_vlan=jNone,
        l2_vlan_id=jNone,
        l2_vlan_id_incr=jNone,
        label_block_offset=jNone,
        cluster_list_enable=jNone,
        end_of_rib=jNone,
        as_path_set_mode=jNone,
        enable_as_path=jNone,
        enable_local_pref=jNone,
        next_hop_enable=jNone,
        mtu=jNone,
        origin_route_enable=jNone,
        label_value=jNone,
        rd_admin_value_step=jNone,
        num_sites=jNone,
        prefix_step=jNone,
        target_step=jNone,
        target_count=jNone,
        communities_enable=jNone,
        next_hop_ip_step=jNone,
        srte_enable_route_target=jNone,
        srte_route_target=jNone,
        srte_aspath=jNone,
        route_type=jNone,
        srte_ipv6_endpoint=jNone,
        srte_ipv6_nexthop=jNone,
        srte_type1_label=jNone,
        srte_type1_sbit=jNone,
        srte_type1_segment_type=jNone,
        label_start=jNone,
        advertise_as_bgp_3107=jNone):


    """
    :param rt_handle:       RT object
    :param aggregator
    :param handle
    :param ip_version
    :param ipv6_prefix_length - <0-128>
    :param max_route_ranges
    :param next_hop_ip_version
    :param next_hop_set_mode - <same|manual>
    :param num_routes
    :param origin - <igp|egp|incomplete>
    :param originator_id_enable
    :param packing_to - <0-65535>
    :param rd_admin_value
    :param rd_assign_step
    :param route_handle
    :param target
    :param target_assign
    :param prefix
    :param mode - <add|modify|remove>
    :param as_path
    :param netmask
    :param originator_id
    :param rd_assign_value
    :param rd_type - <0-1>
    :param target_type
    :param route_ip_addr_step
    :param srte_ip_version
    :param srte_aspath_segment_type
    :param srte_community - <NO_EXPORT|NO_ADVERTISE>
    :param srte_distinguisher
    :param srte_endpoint
    :param srte_local_pref
    :param srte_nexthop
    :param srte_origin - <igp|egp|incomplete>
    :param srte_policy_color
    :param srte_binding_sid
    :param srte_binding_sid_len - <length_0|length_4|length_16>
    :param srte_color
    :param srte_flags - <color|preference|binding_sid|remote_endpoint>
    :param srte_preference
    :param srte_remote_endpoint_addr
    :param srte_remote_endpoint_as
    :param srte_segment_list_subtlv - <weight|0>
    :param srte_weight
    :param ipv4_mpls_vpn_nlri
    :param ipv4_unicast_nlri
    :param label_id - <0-16777215>
    :param label_incr_mode - <fixed|prefix>
    :param label_step - <0-16777215>
    :param local_pref - <0-4294927695>
    :param next_hop
    :param min_lables - <1-65535>
    :param vpls_nlri
    :param l2_enable_vlan
    :param l2_vlan_id - <0-4095>
    :param l2_vlan_id_incr - <1-4094>
    :param label_block_offset - <1-65535>
    :param cluster_list_enable
    :param end_of_rib
    :param as_path_set_mode
    :param enable_as_path - <1>
    :param enable_local_pref - <1>
    :param next_hop_enable - <1>
    :param mtu
    :param origin_route_enable - <1>
    :param label_value - <0-1048575>
    :param rd_admin_value_step
    :param num_sites
    :param prefix_step
    :param target_step
    :param target_count
    :param communities_enable - <0|1>
    :param next_hop_ip_step
    :param srte_enable_route_target - <true|false>
    :param srte_route_target
    :param srte_aspath
    :param route_type
    :param srte_ipv6_endpoint
    :param srte_ipv6_nexthop
    :param srte_type1_label - <0-1048575>
    :param srte_type1_sbit - <0|1>
    :param srte_type1_segment_type
    :param label_start
    :param advertise_as_bgp_3107

    Spirent Returns:
    {
        "handles": "bgpipv4routeconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "bgp_routes": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/bgpIPRouteProperty:2/item:1",
        "handles": "/topology:1/deviceGroup:1/networkGroup:1",
        "ip_routes": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/bgpIPRouteProperty:2",
        "macpool_ip_prefix": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1",
        "network_group_handle": "/topology:1/deviceGroup:1/networkGroup:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['aggregator'] = aggregator
    args['handle'] = handle
    args['ip_version'] = ip_version
    args['ipv6_prefix_length'] = ipv6_prefix_length
    args['max_route_ranges'] = max_route_ranges
    args['next_hop_ip_version'] = next_hop_ip_version
    args['next_hop_set_mode'] = next_hop_set_mode
    args['num_routes'] = num_routes
    args['origin'] = origin
    args['originator_id_enable'] = originator_id_enable
    args['packing_to'] = packing_to
    args['rd_admin_value'] = rd_admin_value
    args['rd_assign_step'] = rd_assign_step
    args['route_handle'] = route_handle
    args['target'] = target
    args['target_assign'] = target_assign
    args['prefix'] = prefix
    args['mode'] = mode
    args['as_path'] = as_path
    args['netmask'] = netmask
    args['originator_id'] = originator_id
    args['rd_assign_value'] = rd_assign_value
    args['rd_type'] = rd_type
    args['target_type'] = target_type
    args['route_ip_addr_step'] = route_ip_addr_step
    args['srte_ip_version'] = srte_ip_version
    args['srte_aspath_segment_type'] = srte_aspath_segment_type
    args['srte_community'] = srte_community
    args['srte_distinguisher'] = srte_distinguisher
    args['srte_endpoint'] = srte_endpoint
    args['srte_local_pref'] = srte_local_pref
    args['srte_nexthop'] = srte_nexthop
    args['srte_origin'] = srte_origin
    args['srte_policy_color'] = srte_policy_color
    args['srte_binding_sid'] = srte_binding_sid
    args['srte_binding_sid_len'] = srte_binding_sid_len
    args['srte_color'] = srte_color
    args['srte_flags'] = srte_flags
    args['srte_preference'] = srte_preference
    args['srte_remote_endpoint_addr'] = srte_remote_endpoint_addr
    args['srte_remote_endpoint_as'] = srte_remote_endpoint_as
    args['srte_segment_list_subtlv'] = srte_segment_list_subtlv
    args['srte_weight'] = srte_weight
    args['ipv4_mpls_vpn_nlri'] = ipv4_mpls_vpn_nlri
    args['ipv4_unicast_nlri'] = ipv4_unicast_nlri
    args['label_id'] = label_id
    args['label_incr_mode'] = label_incr_mode
    args['label_step'] = label_step
    args['local_pref'] = local_pref
    args['next_hop'] = next_hop
    args['min_lables'] = min_lables
    args['label_block_offset'] = label_block_offset
    args['cluster_list_enable'] = cluster_list_enable
    args['num_sites'] = num_sites
    args['prefix_step'] = prefix_step
    args['target_step'] = target_step
    args['communities_enable'] = communities_enable
    args['srte_enable_route_target'] = srte_enable_route_target
    args['srte_route_target'] = srte_route_target
    args['srte_aspath'] = srte_aspath
    args['route_type'] = route_type
    args['srte_ipv6_endpoint'] = srte_ipv6_endpoint
    args['srte_ipv6_nexthop'] = srte_ipv6_nexthop
    args['srte_type1_label'] = srte_type1_label
    args['srte_type1_sbit'] = srte_type1_sbit
    args['srte_type1_segment_type'] = srte_type1_segment_type

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_bgp_route_config.__doc__, **args)

    if 'label_id' in args:
        args['evpn_type2_encap_label'] = args['label_id']
        del args['label_id']
    if 'label_step' in args:
        args['evpn_type2_encap_label_step'] = args['label_step']
        del args['label_step']
    if 'min_lables' in args:
        args['blk_size'] = args['min_lables']
        del args['min_lables']
    if 'label_block_offset' in args:
        args['blk_offset'] = args['label_block_offset']
        del args['label_block_offset']

    if advertise_as_bgp_3107 == '1':
        args['route_sub_afi'] = 'labeled_ip'
        args['custom_mpls_label'] =  'true'

    if label_start != jNone:
        args['mpls_label'] = label_start
        if label_step != jNone:
            args['mpls_label_step'] = label_step
            del args['evpn_type2_encap_label_step']

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if 'num_sites' in list(args.keys()):
        del args['num_sites']
    if 've_id' in list(args.keys()):
        del args['ve_id']
        n_args = dict()
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    port1 = rt_handle.invoke('invoke', cmd='stc::get' + " " +  hnd  + ' -AffiliatedPort')
                    n_args['mode'] = 'create'
                    n_args['port_handle'] = port1
                    n_args['ve_id'] = site_id
                    n_args['site_count'] = num_sites
                    rt_handle.invoke('emulation_mpls_l2vpn_site_config', **n_args)
            else:
                port1 = rt_handle.invoke('invoke', cmd='stc::get' + " " +  hndl  + ' -AffiliatedPort')
                n_args['mode'] = 'create'
                n_args['port_handle'] = port1
                n_args['ve_id'] = site_id
                n_args['site_count'] = num_sites
                rt_handle.invoke('emulation_mpls_l2vpn_site_config', **n_args)
    margs = dict()
    margs['vpls_nlri'] = vpls_nlri
    margs['min_label'] = label_value
    margs['vlan_id'] = l2_vlan_id
    margs['vlan_id_step'] = l2_vlan_id_incr
    for key in list(margs.keys()):
        if margs[key] == jNone:
            del margs[key]

    if vpls_nlri != jNone  or  label_value != jNone  or  l2_vlan_id != jNone  or  l2_vlan_id_incr != jNone:
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    if mode == 'add':
                        margs['handle'] = hnd
                        margs['mode'] = 'modify'
                    elif mode == 'modify':
                        bgp_iproute_parent = rt_handle.invoke('invoke', cmd='stc::get' + " " + hnd  + ' -parent')
                        bgp_route_parent = rt_handle.invoke('invoke', cmd='stc::get' + " " + bgp_iproute_parent  + ' -parent')
                        margs['handle'] = bgp_route_parent
                        margs['mode'] = 'modify'
                    rt_handle.invoke('emulation_bgp_config', **margs)
            else:
                if mode == 'add':
                    margs['handle'] = hndl
                    margs['mode'] = 'modify'
                elif mode == 'modify':
                    bgp_iproute_parent = rt_handle.invoke('invoke', cmd='stc::get' + " " + hndl  + ' -parent')
                    bgp_route_parent = rt_handle.invoke('invoke', cmd='stc::get' + " " + bgp_iproute_parent  + ' -parent')
                    margs['handle'] = bgp_route_parent
                    margs['mode'] = 'modify'
                rt_handle.invoke('emulation_bgp_config', **margs) 

    if as_path_set_mode != jNone:
        m_args = dict()
        if as_path_set_mode in ['include_as_seq', 'sequence']:
            m_args['segment_type_selector'] = 'sequence'
        elif as_path_set_mode in ['include_as_set', 'set']:
            m_args['segment_type_selector'] = 'set'
        elif as_path_set_mode in ['include_as_seq_conf', 'confed_seq']:
            m_args['segment_type_selector'] = 'confed_seq'
        elif as_path_set_mode in ['include_as_set_conf', 'confed_set']:
            m_args['segment_type_selector'] = 'confed_set'
        elif as_path_set_mode == 'custom':
            raise ValueError("INVALID VALUE , PLEASE PROVIDE THE CORRECT VALUE")
        else:
            m_args['segment_type_selector'] = as_path_set_mode

    counter = 1
    string = "bgp_route_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "bgp_route_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()
    for hndl in handle:
        status = 1
        new_ret = dict()
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                if hnd in handle_list:
                    continue
                else:
                    handle_list[hnd] = 1
                args['handle'] = hnd
                if mode == 'modify' or mode == 'remove':
                    args['route_handle'] = hnd
                newer_ret = rt_handle.invoke('emulation_bgp_route_config', **args)
                if 'status' in newer_ret:
                    if newer_ret['status'] == 0:
                        status = 0
                if 'handle' in newer_ret:
                    global_config[string].extend([newer_ret['handle']])


                if 'handles' in newer_ret:
                    global_config[string].extend([newer_ret['handles']])
                for key in newer_ret:
                    try:
                        new_ret[key]
                    except:
                        new_ret[key] = []
                    new_ret[key].append(newer_ret[key])
        else:
            args['handle'] = hndl
            if mode == 'modify' or mode == 'remove':
                args['route_handle'] = hndl
            newer_ret = rt_handle.invoke('emulation_bgp_route_config', **args)
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'handle' in newer_ret:
                global_config[string].extend([newer_ret['handle']])
            if 'handles' in newer_ret:
                global_config[string].extend([newer_ret['handles']])
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status

        if 'handles' in new_ret:
            new_ret['handle'] = new_ret['handles']

        if 'handles' in new_ret:
            new_ret['handles'] = string
        if new_ret:
            ret.append(new_ret)
   #Native arg execution
        handle_ret = ret[0].get('handle')
        if not isinstance(handle_ret, list):
            handle_ret = [handle_ret]
        if end_of_rib != jNone or rd_admin_value_step != jNone or as_path_set_mode != jNone:
            for hand in handle_ret:
                bgp_route_handle1 = rt_handle.invoke('invoke', cmd='stc::get ' + hand + ' -parent')
                if end_of_rib != jNone:
                    if int(end_of_rib) == 1:
                        rt_handle.invoke('invoke', cmd='stc::config ' + bgp_route_handle1 + ' -Synchronization' + ' TRUE')
                    else:
                        rt_handle.invoke('invoke', cmd='stc::config ' + bgp_route_handle1 + ' -Synchronization' + ' FALSE')
                if rd_admin_value_step != jNone:
                    bgp_vpn_route_handle = rt_handle.invoke('invoke', cmd='stc::get ' + hand + ' -children-BgpVpnRouteConfig')
                    rt_handle.invoke('invoke', cmd='stc::config ' + bgp_vpn_route_handle + ' -RouteDistinguisherStep ' + rd_admin_value_step)
                    rt_handle.invoke('invoke', cmd='stc::apply')
                if as_path_set_mode != jNone:
                    m_args['handle'] = hand
                    m_args['mode'] = 'add'
                    rt_handle.invoke('emulation_bgp_custom_attribute_config', **m_args)
        if mtu != jNone:
            ports_list = rt_handle.invoke('invoke', cmd='stc::get' + " " + 'project1 -children-port').split(" ")
            for portss in range(len(ports_list)):
                phy_handle = rt_handle.invoke('invoke', cmd='stc::get' + " " +  ports_list[portss] + ' -ActivePhy-Targets')
                rt_handle.invoke('invoke', cmd='stc::config' + " " + phy_handle + ' -mtu ' + mtu)
                rt_handle.invoke('invoke', cmd='stc::apply')
        if target_count !=jNone:
            for hnd in handle_ret:
                bgp_route_handle1 = rt_handle.invoke('invoke', cmd='stc::get '+hnd+' -parent')
                rt_handle.invoke('invoke', cmd='stc::create BgpMembershipConfig -under '+bgp_route_handle1+' -RouteTargetCount '+target_count)
###Native Next_hop_step
        if next_hop_ip_step != jNone:
            for hand in handle_ret:
                rt_handle.invoke('invoke', cmd='stc::config '+hand+' -UseDeviceAddressAsNextHop "FALSE" -NextHopIncrement '+next_hop_ip_step+' -NextHopIncrementPerRouter '+next_hop_ip_step)        



   # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_config(
        rt_handle,
        dhcp6_reb_timeout=jNone,
        dhcp6_rel_max_rc=jNone,
        dhcp6_rel_timeout=jNone,
        dhcp6_ren_max_rt=jNone,
        dhcp6_ren_timeout=jNone,
        dhcp6_req_max_rc=jNone,
        dhcp6_req_max_rt=jNone,
        dhcp6_req_timeout=jNone,
        dhcp6_sol_max_rc=jNone,
        dhcp6_sol_max_rt=jNone,
        dhcp6_sol_timeout=jNone,
        handle=jNone,
        ip_version=jNone,
        release_rate=jNone,
        request_rate=jNone,
        retry_count=jNone,
        mode=jNone,
        dhcp6_reb_max_rt=jNone,
        outstanding_session_count=jNone,
        msg_timeout=jNone,
        broadcast_bit_flag=jNone,
        relay_agent_ip_addr=jNone,
        server_ip_addr=jNone,
        dhcp6_request_rate=jNone,
        dhcp6_release_rate=jNone,
        circuit_id=jNone,
        remote_id=jNone,
        client_id=jNone,
        dhcp_range_use_relay_agent=jNone,
        client_id_type=jNone,
        port_handle=jNone,
        outstanding_releases_count=jNone):
    """
    :param rt_handle:       RT object
    :param dhcp6_reb_timeout - <1-100>
    :param dhcp6_rel_max_rc - <1-32>
    :param dhcp6_rel_timeout - <1-100>
    :param dhcp6_ren_max_rt - <1-10000>
    :param dhcp6_ren_timeout - <1-100>
    :param dhcp6_req_max_rc - <1-32>
    :param dhcp6_req_max_rt - <1-10000>
    :param dhcp6_req_timeout - <1-100>
    :param dhcp6_sol_max_rc - <1-32>
    :param dhcp6_sol_max_rt - <1-10000>
    :param dhcp6_sol_timeout - <1-100>
    :param handle
    :param ip_version - <4|6>
    :param release_rate - <1-10000>
    :param request_rate - <1-10000>
    :param retry_count - <1-32>
    :param mode - <create|modify|reset>
    :param dhcp6_reb_max_rt - <1-10000>
    :param outstanding_session_count - <1-2048>
    :param msg_timeout - <1000-65535>
    :param broadcast_bit_flag - <0|1>
    :param relay_agent_ip_addr
    :param server_ip_addr
    :param dhcp6_request_rate - <1-10000>
    :param dhcp6_release_rate - <1-10000>
    :param circuit_id
    :param remote_id
    :param client_id
    :param dhcp_range_use_relay_agent - <0|1>
    :param client_id_type - <0-255>
    :param port_handle
    :param outstanding_releases_count - <1-1000>


    Spirent Returns:
    {
        "handle": {
            "port1": "dhcpv4portconfig1"
        },
        "handles": "dhcpv4portconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/dhcpv4client:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['dhcp6_reb_timeout'] = dhcp6_reb_timeout
    args['dhcp6_rel_max_rc'] = dhcp6_rel_max_rc
    args['dhcp6_rel_timeout'] = dhcp6_rel_timeout
    args['dhcp6_ren_max_rt'] = dhcp6_ren_max_rt
    args['dhcp6_ren_timeout'] = dhcp6_ren_timeout
    args['dhcp6_req_max_rc'] = dhcp6_req_max_rc
    args['dhcp6_req_max_rt'] = dhcp6_req_max_rt
    args['dhcp6_req_timeout'] = dhcp6_req_timeout
    args['dhcp6_sol_max_rc'] = dhcp6_sol_max_rc
    args['dhcp6_sol_max_rt'] = dhcp6_sol_max_rt
    args['dhcp6_sol_timeout'] = dhcp6_sol_timeout
    args['handle'] = handle
    args['ip_version'] = ip_version
    args['release_rate'] = release_rate
    args['request_rate'] = request_rate
    args['retry_count'] = retry_count
    args['mode'] = mode
    args['dhcp6_reb_max_rt'] = dhcp6_reb_max_rt
    args['broadcast_bit_flag'] = broadcast_bit_flag
    args['relay_agent_ip_addr'] = relay_agent_ip_addr
    args['server_ip_addr'] = server_ip_addr
    args['dhcp6_request_rate'] = dhcp6_request_rate
    args['dhcp6_release_rate'] = dhcp6_release_rate
    args['circuit_id'] = circuit_id
    args['remote_id'] = remote_id
    args['client_id'] = client_id
    args['dhcp_range_use_relay_agent'] = dhcp_range_use_relay_agent
    args['client_id_type'] = client_id_type
    args['port_handle'] = port_handle
    args['outstanding_releases_count'] = outstanding_releases_count


    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
   
    if ip_version == '6':
        args['dhcp6_outstanding_session_count'] = outstanding_session_count
    else:
        args['outstanding_session_count'] = outstanding_session_count

    args = get_arg_value(rt_handle, j_emulation_dhcp_config.__doc__, **args)

    if 'dhcp_range_use_relay_agent' in args:
        args['relay_agent_flag'] = args['dhcp_range_use_relay_agent']
        del args['dhcp_range_use_relay_agent']

    if 'outstanding_releases_count' in args:
        args['dhcp6_release_rate'] = args['outstanding_releases_count']
        del args['outstanding_releases_count']

    handle_map[port_handle] = handle_map.get(port_handle, [])

    ret = []
  #  handles = jNone
    if 'msg_timeout' in args.keys():
        args['msg_timeout'] = int(msg_timeout) * 1000

    counter = 1
    string = "dhcp_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "dhcp_" + str(counter)
    global_config[string] = []

    if handle != jNone:
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    args['handle'] = hnd
                    if 'mode' in args and args['mode'] == 'create':
                        args['mode'] = 'enable'
                    result = rt_handle.invoke('emulation_dhcp_config', **args)
                    if result.get('handles'):
                        global_config[string].extend(result['handles'].split(' '))
                        result['handle'] = result['handles']
                        result['handles'] = string
                    ret.append(result)
            else:
                args['handle'] = hndl
                args['mode'] = 'enable' if args['mode'] == 'create' else args['mode']
                result = rt_handle.invoke('emulation_dhcp_config', **args)
                if result.get('handles'):
                    global_config[string].extend(result['handles'].split(' '))
                    result['handle'] = result['handles']
                    result['handles'] = string
                ret.append(result)
    elif port_handle != jNone:
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        for port_hand in port_handle:
            args['port_handle'] = port_hand
            result = rt_handle.invoke('emulation_dhcp_config', **args)
            if result.get('handles'):
                global_config[string].extend(result['handles'].split(' '))
                result['handle'] = result['handles']
                result['handles'] = string
                session_map[port_hand] = session_map.get(port_hand, [])
                session_map[port_hand].extend(global_config[string])
                session_map[string] = port_hand
                handle_map[port_hand] = handle_map.get(port_hand, [])
                handle_map[port_hand].extend(global_config[string])
                handle_map[port_hand] = list(set(handle_map[port_hand]))
                handle_map[string] = port_hand
            ret.append(result)

    if mode == 'create':
        if ip_version == '6':
            v6_handles.append(global_config[ret[-1]['handles']])
        else:
            v4_handles.append(global_config[ret[-1]['handles']])

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_control(
        rt_handle,
        handle=jNone,
        port_handle=jNone,
        action=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle
    :param action

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['port_handle'] = port_handle
    args['action'] = action

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_dhcp_control.__doc__, **args)

    __check_and_raise(action)


    if args['action'] != 'release':
        __check_and_raise(handle)

    if args['action'] == 'release' and 'handle' not in args:
        return_output = []
        return_output.append(rt_handle.invoke('emulation_dhcp_control', **args))
        return return_output[0] if len(return_output) == 1 else return_output

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['ip_version'] = '4'
                if 'handle' in args:
                    del args['handle']
                if hnd in handle_map:
                    args['handle'] = handle_map[hnd]
                for indi in v6_handles:
                    if isinstance(indi, list) and hnd in indi:
                        args['ip_version'] = '6'
                ret.append(rt_handle.invoke('emulation_dhcp_control', **args))
        else:
            args['ip_version'] = '4'
            if 'handle' in args:
                del args['handle']
            if hndl in handle_map:
                args['handle'] = handle_map[hndl]
            for indi in v6_handles:
                if isinstance(indi, list) and hndl in indi:
                    args['ip_version'] = '6'
            ret.append(rt_handle.invoke('emulation_dhcp_control', **args))
    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_group_config(
        rt_handle,
        dhcp6_range_duid_enterprise_id=jNone,
        dhcp6_range_ia_t1=jNone,
        dhcp6_range_ia_t2=jNone,
        handle=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        num_sessions=jNone,
        qinq_incr_mode=jNone,
        vlan_id=jNone,
        vlan_id_count=jNone,
        vlan_id_outer_count=jNone,
        vlan_id_outer_step=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        dhcp_range_ip_type=jNone,
        encap=jNone,
        dhcp_range_server_address=jNone,
        rapid_commit_mode=jNone,
        dhcp_range_use_relay_agent=jNone,
        dhcp6_range_duid_type=jNone,
        duid_value=jNone,
        dhcp_range_relay_first_address=jNone,
        dhcp4_broadcast=jNone,
        dhcp6_client_mode=jNone,
        dhcp_range_relay_count=jNone,
        dhcp_range_relay_destination=jNone,
        dhcp6_range_duid_vendor_id=jNone,
        dhcp6_range_duid_vendor_id_increment=jNone,
        dhcp6_range_ia_id=jNone,
        dhcp6_range_ia_id_increment=jNone,
        dhcp6_range_ia_type=jNone,
        dhcp_range_relay_gateway=jNone,
        dhcp_range_param_request_list=jNone,
        dhcp_range_relay_vlan_count=jNone,
        dhcp_range_relay_first_vlan_id=jNone,
        dhcp_range_relay_vlan_increment=jNone,
        dhcp_range_relay_address_increment=jNone,
        dhcp_range_relay_subnet=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_priority=jNone,
        circuit_id=jNone,
        remote_id=jNone,
        enable_ldra=jNone,
        enable_reconfig_accept=jNone,
        circuit_id_enable=jNone,
        remote_id_enable=jNone,
        enable_router_option=jNone,
        dst_addr_type=jNone):
    """
    :param rt_handle:       RT object
    :param dhcp6_range_duid_enterprise_id
    :param dhcp6_range_ia_t1
    :param dhcp6_range_ia_t2
    :param handle
    :param mac_addr
    :param mac_addr_step
    :param num_sessions - <1-65536>
    :param qinq_incr_mode - <inner|outer|both>
    :param vlan_id - <1-4095>
    :param vlan_id_count - <1-4095>
    :param vlan_id_outer_count - <1-4094>
    :param vlan_id_outer_step - <1-4094>
    :param vlan_id_step - <1-4095>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|reset>
    :param dhcp_range_ip_type - <4:ipv4|6:ipv6>
    :param encap - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq|vc_mux|llcsnap>
    :param dhcp_range_server_address
    :param rapid_commit_mode - <ENABLE:1|DISABLE:0>
    :param dhcp_range_use_relay_agent - <0|1>
    :param dhcp6_range_duid_type - <en:duid_en|ll:duid_ll|llt:duid_llt|EN:duid_en|LL:duid_ll|LLT:duid_llt>
    :param duid_value
    :param dhcp_range_relay_first_address
    :param dhcp4_broadcast - <0|1>
    :param dhcp6_client_mode - <DHCPV6:iana|DHCPV6ANDPD:iana_iapd|DHCPPD:iapd>
    :param dhcp_range_relay_count - <1-65536>
    :param dhcp_range_relay_destination
    :param dhcp6_range_duid_vendor_id
    :param dhcp6_range_duid_vendor_id_increment
    :param dhcp6_range_ia_id
    :param dhcp6_range_ia_id_increment
    :param dhcp6_range_ia_type - <DHCPV6:iana|DHCPV6ANDPD:iana_iapd|DHCPPD:iapd>
    :param dhcp_range_relay_gateway
    :param dhcp_range_param_request_list
    :param dhcp_range_relay_vlan_count - <1-4094>
    :param dhcp_range_relay_first_vlan_id - <1-4095>
    :param dhcp_range_relay_vlan_increment - <1-4093>
    :param dhcp_range_relay_address_increment
    :param dhcp_range_relay_subnet
    :param vlan_id_outer - <1-4094>
    :param vlan_id_outer_priority - <0-7>
    :param circuit_id
    :param remote_id
    :param enable_ldra - <true|false>
    :param enable_reconfig_accept - <true|false>
    :param circuit_id_enable - <true:1|false:0>
    :param remote_id_enable - <true:1|false:0>
    :param enable_router_option - <true:1|flase:0>
    :param dst_addr_type - <ALL_DHCP_RELAY_AGENTS_AND_SERVERS|ALL_DHCP_SERVERS>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "dhcpv4blockconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/dhcpv4client:1/item:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    n_args = dict()
    args['dhcp6_range_duid_enterprise_id'] = dhcp6_range_duid_enterprise_id
    args['dhcp6_range_ia_t1'] = dhcp6_range_ia_t1
    args['dhcp6_range_ia_t2'] = dhcp6_range_ia_t2
    args['handle'] = handle
    args['mac_addr'] = mac_addr
    args['mac_addr_step'] = mac_addr_step
    args['num_sessions'] = num_sessions
    args['qinq_incr_mode'] = qinq_incr_mode
    args['vlan_id'] = vlan_id
    args['vlan_id_count'] = vlan_id_count
    args['vlan_id_outer_count'] = vlan_id_outer_count
    args['vlan_id_outer_step'] = vlan_id_outer_step
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['dhcp_range_ip_type'] = dhcp_range_ip_type
    args['encap'] = encap
    args['server_ip_addr'] = dhcp_range_server_address
    args['rapid_commit_mode'] = rapid_commit_mode
    args['dhcp_range_use_relay_agent'] = dhcp_range_use_relay_agent
    args['dhcp6_range_duid_type'] = dhcp6_range_duid_type
    args['duid_value'] = duid_value
    args['relay_agent_ip_addr'] = dhcp_range_relay_first_address
    args['dhcp6_client_mode'] = dhcp6_client_mode
    args['dhcp6_range_duid_vendor_id'] = dhcp6_range_duid_vendor_id
    args['dhcp6_range_duid_vendor_id_increment'] = dhcp6_range_duid_vendor_id_increment
    args['opt_list'] = dhcp_range_param_request_list
    args['relay_agent_ipv4_subnet_mask'] = dhcp_range_relay_subnet
    args['vlan_id_outer'] = vlan_id_outer
    args['vlan_outer_user_priority'] = vlan_id_outer_priority
    args['circuit_id'] = circuit_id
    args['remote_id'] = remote_id
    args['enable_ldra'] = enable_ldra
    args['enable_reconfig_accept'] = enable_reconfig_accept
    args['dhcp_range_relay_count'] = dhcp_range_relay_count
    args['dhcp_range_relay_destination'] = dhcp_range_relay_destination
    args['ipv4_gateway_address'] = dhcp_range_relay_gateway
    args['dhcp6_range_ia_type'] = dhcp6_range_ia_type
    args['dhcp_range_relay_first_vlan_id'] = dhcp_range_relay_first_vlan_id
    args['dhcp_range_relay_vlan_count'] = dhcp_range_relay_vlan_count
    args['dhcp_range_relay_vlan_increment'] = dhcp_range_relay_vlan_increment
    args['circuit_id_enable'] = circuit_id_enable
    args['remote_id_enable'] = remote_id_enable
    args['enable_router_option'] = enable_router_option
    args['dst_addr_type'] = dst_addr_type


    if mode == 'create':
        if encap == jNone:
            args['encap'] = 'ethernet_ii'
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_dhcp_group_config.__doc__, **args)    
    n_args['dhcp4_broadcast'] = dhcp4_broadcast
    n_args = get_arg_value(rt_handle, j_emulation_dhcp_group_config.__doc__, **n_args)

    if 'dhcp_range_use_relay_agent' in args:
        args['relay_agent_flag'] = args['dhcp_range_use_relay_agent']
        del args['dhcp_range_use_relay_agent']

    if 'dhcp4_broadcast' in n_args:
        n_args['broadcast_bit_flag'] = n_args['dhcp4_broadcast']
        del n_args['dhcp4_broadcast']

    if 'dhcp_range_relay_count' in args:
        args['num_sessions'] = args['dhcp_range_relay_count']
        del args['dhcp_range_relay_count']

    if 'dhcp6_range_ia_type' in args:
        args['dhcp6_client_mode'] = args['dhcp6_range_ia_type']
        del args['dhcp6_range_ia_type']

    if 'dhcp_range_relay_first_vlan_id' in args:
        args['vlan_id'] = args['dhcp_range_relay_first_vlan_id']
        del args['dhcp_range_relay_first_vlan_id']

    if 'dhcp_range_relay_vlan_count' in args:
        args['vlan_id_count'] = args['dhcp_range_relay_vlan_count']
        del args['dhcp_range_relay_vlan_count']

    if 'dhcp_range_relay_destination' in args:
        args['server_ip_addr'] = args['dhcp_range_relay_destination']
        del args['dhcp_range_relay_destination']

    if 'dhcp_range_relay_vlan_increment' in args:
        args['vlan_id_step'] = args['dhcp_range_relay_vlan_increment']
        del args['dhcp_range_relay_vlan_increment']

    if 'circuit_id_enable' in args:
        args['enable_circuit_id'] = args['circuit_id_enable']
        del args['circuit_id_enable']

    if 'remote_id_enable' in args:
        args['enable_remote_id'] = args['remote_id_enable']
        del args['remote_id_enable']

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    #handle = list(set(handle))
    if dhcp4_broadcast != jNone:
        for hndl in handle:
            if hndl in global_config.keys():
                for hand in global_config[hndl]:
                    n_args['ip_version'] = '4'
                    n_args['handle'] = hand
                    n_args['mode'] = mode
                    n_args['broadcast_bit_flag'] = dhcp4_broadcast
                    if mode == 'create' and not n_args['handle'].startswith('dhcp'):
                        n_args['mode'] = 'enable'
                    if mode == 'modify':
                        dhcp_router_handle1 = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -parent')
                        port_addr = rt_handle.invoke('invoke', cmd='stc::get '+dhcp_router_handle1+' -AffiliatedPort')
                        dhcp_port = rt_handle.invoke('invoke', cmd='stc::get '+port_addr+' -children-Dhcpv4PortConfig')
                        n_args['handle'] = dhcp_port
                    if mode != jNone and mode != 'reset':
                        rt_handle.invoke('emulation_dhcp_config', **n_args)
            else:
                n_args['ip_version'] = '4'
                n_args['handle'] = hndl
                n_args['mode'] = mode
                n_args['broadcast_bit_flag'] = dhcp4_broadcast
                if mode == 'create' and not n_args['handle'].startswith('dhcp'):
                    n_args['mode'] = 'enable'
                if mode == 'modify':
                    dhcp_router_handle1 = rt_handle.invoke('invoke', cmd='stc::get '+hndl+' -parent')
                    port_addr = rt_handle.invoke('invoke', cmd='stc::get '+dhcp_router_handle1+' -AffiliatedPort')
                    dhcp_port = rt_handle.invoke('invoke', cmd='stc::get '+port_addr+' -children-Dhcpv4PortConfig')
                    n_args['handle'] = dhcp_port
                if mode != jNone and mode != 'reset':
                    rt_handle.invoke('emulation_dhcp_config', **n_args)
    counter = 1
    string = "dhcp_grp_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "dhcp_grp_" + str(counter)
    global_config[string] = []
    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                if mode == 'reset':
                    #args['dhcp_range_ip_type'] = '4'
                    #if args['handle'] in v6_handles:
                        #args['dhcp_range_ip_type'] = '6'
                    args['handle'] = handle_map[args['handle']]
                elif mode == 'create' and not args['handle'].startswith('dhcp'):
                    args['mode'] = 'enable'
                result = rt_handle.invoke('emulation_dhcp_group_config', **args)
                if result.get('handles') and result['handles'].startswith('dhcpv4block'):
                    global_config[string].extend(result['handles'].split(' '))
                    result['handle_1'] = result['handle']
                    result['handle'] = result['handles']
                    result['handles'] = string
                elif result.get('dhcpv6_handle'):
                    global_config[string].extend(result['dhcpv6_handle'].split(' '))
                    result['handle'] = result['dhcpv6_handle']
                    result['handles'] = string
                ret.append(result)
        else:
            args['handle'] = hndl
            if mode == 'reset':
                #args['dhcp_range_ip_type'] = '4'
                #if args['handle'] in v6_handles:
                 #   args['dhcp_range_ip_type'] = '6'
                args['handle'] = handle_map[args['handle']]
            elif mode == 'create' and not args['handle'].startswith('dhcp'):
                args['mode'] = 'enable'
            result = rt_handle.invoke('emulation_dhcp_group_config', **args)
            if result.get('handles') and result['handles'].startswith('dhcpv4block'):
                global_config[string].extend(result['handles'].split(' '))
                result['handle_1'] = result['handle']
                result['handle'] = result['handles']
                result['handles'] = string
            elif result.get('dhcpv6_handle'):
                global_config[string].extend(result['dhcpv6_handle'].split(' '))
                result['handle'] = result['dhcpv6_handle']
                result['handles'] = string
            ret.append(result)
    if mode == 'create':
        for index in range(len(ret)):
            if 'dhcp_range_ip_type' in args.keys() and args['dhcp_range_ip_type'] == '6':
                ret[index]['handle'] = ret[index]['dhcpv6_handle']
            handle_map[ret[index]['handle']] = global_config[ret[index]['handles']]
            handle_map[ret[index]['handles']] = ret[index]['handle']
            if 'dhcp_range_ip_type' in args.keys():
                if args['dhcp_range_ip_type'] == '6':
                    v6_handles.append(global_config[ret[index]['handles']])
                else:
                    v4_handles.append(global_config[ret[index]['handles']])
    # **** Native Arguments Execution
    if mode == 'create':
        if  dhcp_range_relay_address_increment != jNone:
            for index in range(len(ret)):
                if dhcp_range_ip_type == 'ipv4' or dhcp_range_ip_type == '4':
                    myHandle = ret[index]['handle_1']
                    dhcp_router_handle1 = rt_handle.invoke('invoke', cmd='stc::get' + " " +  myHandle  + ' -children' + '-dhcpv4blockconfig')

                    if  dhcp_range_relay_address_increment != jNone:
                        rt_handle.invoke('invoke', cmd='stc::config' + " " + dhcp_router_handle1 + ' -RelayAgentIpv4AddrStep' + " " +  dhcp_range_relay_address_increment)
        if  dhcp6_range_ia_id != jNone or  dhcp6_range_ia_id_increment != jNone:
            for index in range(len(ret)):
                if 'dhcp_range_ip_type' in args.keys():
                    if dhcp_range_ip_type == 'ipv6' or dhcp_range_ip_type == '6':
                        ret[index]['handle'] = ret[index]['dhcpv6_handle']
                        myHandle = ret[index]['handle']
                        dhcp_router_handle = rt_handle.invoke('invoke', cmd='stc::get' + " " +  myHandle  + ' -children' + '-dhcpv6blockconfig')

                        if  dhcp6_range_ia_id != jNone:
                            rt_handle.invoke('invoke', cmd='stc::config' + " " + dhcp_router_handle + ' -IaidStart' + " " +  dhcp6_range_ia_id)

                        if  dhcp6_range_ia_id_increment != jNone:
                            rt_handle.invoke('invoke', cmd='stc::config' + " " + dhcp_router_handle + ' -IaidStep' + " " +  dhcp6_range_ia_id_increment)
    for index in range(len(ret)):
        if 'handle_1' in ret[index].keys():
            del ret[index]['handle_1']

    if len(ret) == 1:
        ret = ret[0]

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_server_config(
        rt_handle,
        count=jNone,
        dhcp_offer_options=jNone,
        handle=jNone,
        ip_prefix_length=jNone,
        ip_prefix_step=jNone,
        ip_repeat=jNone,
        ip_version=jNone,
        lease_time=jNone,
        local_mac=jNone,
        port_handle=jNone,
        qinq_incr_mode=jNone,
        vlan_id=jNone,
        vlan_id_count=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        ipaddress_pool=jNone,
        ipaddress_count=jNone,
        mode=jNone,
        ip_address=jNone,
        ip_step=jNone,
        ip_gateway=jNone,
        remote_mac=jNone,
        vlan_id_mode=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone,
        prefix_pool_start_addr=jNone):
    """
    :param rt_handle:       RT object
    :param count - <1-100000>
    :param dhcp_offer_options - <0|1>
    :param handle
    :param ip_prefix_length - <0-32>
    :param ip_prefix_step
    :param ip_repeat
    :param ip_version - <4|6>
    :param lease_time - <300-30000000>
    :param local_mac
    :param port_handle
    :param qinq_incr_mode - <inner|outer|both>
    :param vlan_id - <0-4095>
    :param vlan_id_count - <1-4095>
    :param vlan_id_step - <0-4095>
    :param vlan_user_priority - <0-7>
    :param ipaddress_pool
    :param ipaddress_count
    :param mode - <create|modify|reset>
    :param ip_address
    :param ip_step
    :param ip_gateway
    :param remote_mac
    :param vlan_id_mode - <fixed|increment>
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <0-4095>
    :param vlan_outer_user_priority - <0-7>
    :param prefix_pool_start_addr

    Spirent Returns:
    {
        "handle": {
            "dhcp_handle": "host3",
            "port_handle": "port2"
        },
        "handles": "host3",
        "status": "1"
    }

    IXIA Returns:
    {
        "dhcpv4server_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/dhcpv4server:1",
        "handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/dhcpv4server:1/item:1",
        "handles": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/dhcpv4server:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['count'] = count
    args['dhcp_offer_options'] = dhcp_offer_options
    args['handle'] = handle
    args['ip_prefix_length'] = ip_prefix_length
    args['ip_prefix_step'] = ip_prefix_step
    args['ip_repeat'] = ip_repeat
    args['ip_version'] = ip_version
    args['lease_time'] = lease_time
    args['local_mac'] = local_mac
    args['port_handle'] = port_handle
    args['qinq_incr_mode'] = qinq_incr_mode
    args['vlan_id'] = vlan_id
    args['vlan_id_count'] = vlan_id_count
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['ipaddress_pool'] = ipaddress_pool
    args['ipaddress_count'] = ipaddress_count
    args['mode'] = mode
    args['ip_address'] = ip_address
    args['ip_step'] = ip_step
    args['ip_gateway'] = ip_gateway
    args['remote_mac'] = remote_mac
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_outer_id'] = vlan_outer_id
    args['vlan_outer_id_mode'] = vlan_outer_id_mode
    args['vlan_outer_id_step'] = vlan_outer_id_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority
    args['prefix_pool_start_addr'] = prefix_pool_start_addr

    if ip_version == '6':
        args['local_ipv6_addr'] = ip_address
        args['local_ipv6_addr_step'] = ip_step
        args['local_ipv6_prefix_len'] = ip_prefix_length
        args['gateway_ipv6_addr'] = ip_gateway
        args['addr_pool_start_addr'] = ipaddress_pool
        args['addr_pool_addresses_per_server'] = ipaddress_count
        args['valid_lifetime'] = lease_time
        del args['ip_address']
        del args['ip_step']
        del args['ip_prefix_length']
        del args['ip_gateway']
        del args['ipaddress_pool']
        del args['ipaddress_count']
        del args['lease_time']

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
  
    args = get_arg_value(rt_handle, j_emulation_dhcp_server_config.__doc__, **args)

    ret = []
    handles = jNone
    counter = 1
    string = "dhcp_server_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "dhcp_server_" + str(counter)
    global_config[string] = []

    ##Encapsulation
    if mode == 'create':
        if 'vlan_id' in args.keys() or 'vlan_id_count' in args.keys() or 'vlan_id_step' in args.keys() or 'vlan_user_priority' in args.keys() or 'vlan_id_mode' in args.keys():
            if 'vlan_outer_id' in args.keys() or 'vlan_outer_id_mode' in args.keys() or 'vlan_outer_id_step' in args.keys() or 'vlan_outer_user_priority' in args.keys():
                args['encapsulation'] = 'ETHERNET_II_QINQ'
            else:
                args['encapsulation'] = 'ETHERNET_II_VLAN'
            args['encapsulation'] = args['encapsulation'].lower() if 'ip_version' in args and int(args['ip_version']) == 6 else args['encapsulation'].upper()
    
    if handle != jNone:
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    if ip_version == '6':
                        args['server_emulation_mode'] = 'DHCPV6'
                    #if mode == 'reset':
                        #args['ip_version'] = '6' if hnd in v6_handles else '4'
                    args['handle'] = hnd
                    if 'mode' in args and args['mode'] == 'create':
                        args['mode'] = 'enable'
                    result = rt_handle.invoke('emulation_dhcp_server_config', **args)
                    if result.get('handle'):
                        if 'dhcp_handle' in result['handle'].keys():
                            global_config[string].extend(result['handle']['dhcp_handle'].split(' '))
                            result['handle'] = result['handle']['dhcp_handle']
                            result['handles'] = string
                        elif 'dhcpv6_handle' in result['handle'].keys():
                            global_config[string].extend(result['handle']['dhcpv6_handle'].split(' '))
                            result['handle'] = result['handle']['dhcpv6_handle']
                            result['handles'] = string
                    ret.append(result)
            else:
                if ip_version == '6':
                    args['server_emulation_mode'] = 'DHCPV6'
                #if mode == 'reset':
                 #   args['ip_version'] = '6' if hndl in v6_handles else '4'
                args['handle'] = hndl
                args['mode'] = 'enable' if args['mode'] == 'create' else args['mode']
                result = rt_handle.invoke('emulation_dhcp_server_config', **args)
                if result.get('handle'):
                    if 'dhcp_handle' in result['handle'].keys():
                        global_config[string].extend(result['handle']['dhcp_handle'].split(' '))
                        result['handle'] = result['handle']['dhcp_handle']
                        result['handles'] = string
                    elif 'dhcpv6_handle' in result['handle'].keys():
                        global_config[string].extend(result['handle']['dhcpv6_handle'].split(' '))
                        result['handle'] = result['handle']['dhcpv6_handle']
                        result['handles'] = string
                ret.append(result)
    elif port_handle != jNone:
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        for port_hand in port_handle:
            args['port_handle'] = port_hand
            if ip_version == '6':
                args['server_emulation_mode'] = 'DHCPV6'
            result = rt_handle.invoke('emulation_dhcp_server_config', **args)
            if result.get('handle'):
                if 'dhcp_handle' in result['handle'].keys():
                    global_config[string].extend(result['handle']['dhcp_handle'].split(' '))
                    result['handle'] = result['handle']['dhcp_handle']
                    result['handles'] = string
                elif 'dhcpv6_handle' in result['handle'].keys():
                    global_config[string].extend(result['handle']['dhcpv6_handle'].split(' '))
                    result['handle'] = result['handle']['dhcpv6_handle']
                    result['handles'] = string
                session_map[port_hand] = session_map.get(port_hand, [])
                session_map[port_hand].extend(global_config[string])
                session_map[string] = port_hand
                handle_map[port_hand] = handle_map.get(port_hand, [])
                handle_map[port_hand].extend(global_config[string])
                handle_map[port_hand] = list(set(handle_map[port_hand]))
                handle_map[string] = port_hand
            ret.append(result)
    # ***** Return Value Modification *****
    for index in range(len(ret)):
        if 'handle' in ret[index]:
            if 'dhcp_handle' in ret[index]['handle']:
                ret[index]['handles'] = ret[index]['handle']['dhcp_handle']
                v4_handles.append(ret[index]['handles'])
            if 'ip_version' in args.keys() and ip_version == '6':
                v6_handles.append(global_config[ret[index]['handles']])
    if len(ret) == 1:
        ret = ret[0]
   
    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_server_control(
        rt_handle,
        action=jNone,
        handle=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param action
    :param handle
    :param port_handle

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['dhcp_handle'] = handle
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    if action == 'start':
        args['action'] = 'connect'
    elif action == 'stop':
        args['action'] = 'reset'

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    #handle = list(set(handle))

    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['dhcp_handle'] = hnd
                args['ip_version'] = '4'
                for indi in v6_handles:
                    if isinstance(indi, list) and args['dhcp_handle'] in indi:
                        args['ip_version'] = '6'
                ret.append(rt_handle.invoke('emulation_dhcp_server_control', **args))
        else:
            args['dhcp_handle'] = hndl
            args['ip_version'] = '4'
            for indi in v6_handles:
                if isinstance(indi, list) and args['dhcp_handle'] in indi:
                    args['ip_version'] = '6'
            ret.append(rt_handle.invoke('emulation_dhcp_server_control', **args))
    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_server_stats(rt_handle, action=jNone, handle=jNone,
                                  ip_version=jNone, port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param action
    :param handle
    :param ip_version
    :param port_handle

    Spirent Returns:
    {
        "aggregate": {
            "ack": "1",
            "decline": "0",
            "discover": "1",
            "host3": {
                "rx": {
                    "decline": "0",
                    "discover": "1",
                    "inform": "0",
                    "release": "0",
                    "request": "1"
                }
            },
            "inform": "0",
            "nak": "0",
            "offer": "1",
            "offer_count": "1",
            "release": "0",
            "release_count": "0",
            "request": "1"
        },
        "dhcp_handle": {
            "host3": {
                "tx": {
                    "ack": "1",
                    "nak": "0",
                    "offer": "1"
                }
            }
        },
        "dhcp_server_state": "UP",
        "status": "1"
    },
    {
        "aggregate": {
            "current_bound_count": "1",
            "release_count": "0",
            "rx_confirm_count": "0",
            "rx_decline_count": "0",
            "rx_info_request_count": "0",
            "rx_rebind_count": "0",
            "rx_release_count": "0",
            "rx_renew_count": "0",
            "rx_request_count": "1",
            "rx_soilicit_count": "1",
            "total_bound_count": "1",
            "total_expired_count": "0",
            "total_release_count": "0",
            "total_renewed_count": "0",
            "tx_advertise_count": "1",
            "tx_reconfigure_count": "0",
            "tx_reconfigure_rebind_count": "0",
            "tx_reconfigure_renew_count": "0",
            "tx_reply_count": "1"
        },
        "dhcp_server_state": "UP",
        "ipv6": {
            "dhcp_handle": {
                "host4": {
                    "current_bound_count": "1",
                    "rx_confirm_count": "0",
                    "rx_decline_count": "0",
                    "rx_info_request_count": "0",
                    "rx_rebind_count": "0",
                    "rx_release_count": "0",
                    "rx_renew_count": "0",
                    "rx_request_count": "1",
                    "rx_soilicit_count": "1",
                    "total_bound_count": "1",
                    "total_expired_count": "0",
                    "total_release_count": "0",
                    "total_renewed_count": "0",
                    "tx_advertise_count": "1",
                    "tx_reconfigure_count": "0",
                    "tx_reconfigure_rebind_count": "0",
                    "tx_reconfigure_renew_count": "0",
                    "tx_reply_count": "1"
                }
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "Device Group 3": {
            "aggregate": {
                "bind/rapid_commit_count": "0",
                "bind_count": "1",
                "force_renew_count": "0",
                "offer_count": "1",
                "release_count": "0",
                "renew_count": "0",
                "session_total": "1",
                "sessions_down": "0",
                "sessions_not_started": "0",
                "sessions_up": "1",
                "status": "started"
            }
        },
        "aggregate": {
            "bind/rapid_commit_count": "0",
            "bind_count": "1",
            "force_renew_count": "0",
            "offer_count": "1",
            "release_count": "0",
            "renew_count": "0",
            "session_total": "1",
            "sessions_down": "0",
            "sessions_not_started": "0",
            "sessions_up": "1",
            "status": "started"
        },
        "status": "1"
    },
    {
        "Device Group 4": {
            "aggregate": {
                "status": "started"
            }
        },
        "aggregate": {
            "status": "started"
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['dhcp_handle'] = handle
    args['ip_version'] = ip_version
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    if action is not jNone:
        args['action'] = action.upper()

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
#    handle = list(set(handle))
    
    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['dhcp_handle'] = hnd
                for indi in v6_handles:
                    if isinstance(indi, list) and hnd in indi:
                        args['ip_version'] = '6'
                ret.append(rt_handle.invoke('emulation_dhcp_server_stats', **args))
                if ip_version == jNone and 'ip_version' in args:
                    del args['ip_version']
        else:
            args['dhcp_handle'] = hndl
            for indi in v6_handles:
                if isinstance(indi, list) and hndl in indi:
                    args['ip_version'] = '6'
            ret.append(rt_handle.invoke('emulation_dhcp_server_stats', **args))
            if ip_version == jNone and 'ip_version' in args:
                del args['ip_version']
    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'aggregate' in ret[index]:
            for key in list(ret[index]['aggregate']):
                if 'rx' in ret[index]['aggregate'][key]:
                    ret[index]['aggregate'].update(ret[index]['aggregate'][key]['rx'])
                    if 'release' in ret[index]['aggregate']:
                        ret[index]['aggregate']['release_count'] = ret[index]['aggregate']['release']
        if 'dhcp_handle' in ret[index]:
            for key in list(ret[index]['dhcp_handle']):
                if 'tx' in ret[index]['dhcp_handle'][key]:
                    ret[index]['aggregate'].update(ret[index]['dhcp_handle'][key]['tx'])
                    if 'offer' in ret[index]['aggregate']:
                        ret[index]['aggregate']['offer_count'] = ret[index]['aggregate']['offer']
        if 'ipv6' in ret[index]:
            if 'dhcp_handle' in ret[index]['ipv6']:
                ret[index]['aggregate'] = dict()
                for key in list(ret[index]['ipv6']['dhcp_handle']):
                    ret[index]['aggregate'].update(ret[index]['ipv6']['dhcp_handle'][key])
                    if 'rx_release_count' in ret[index]['aggregate']:
                        ret[index]['aggregate']['release_count'] = ret[index]['aggregate']['rx_release_count']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_dhcp_stats(rt_handle, handle=jNone, port_handle=jNone, action=jNone, dhcp_version=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle
    :param action
    :param dhcp_version

    Spirent Returns:
    {
        "aggregate": {
            "ack_rx_count": "1",
            "attempted_rate": "0",
            "average_setup_time": "0.01307518",
            "bind_rate": "75.8329491130578",
            "bound_renewed": "0",
            "currently_attempting": "0",
            "currently_bound": "1",
            "currently_idle": "0",
            "discover_tx_count": "1",
            "elapsed_time": "0.01326492",
            "maximum_setup_time": "0.01307518",
            "minimum_setup_time": "0.01307518",
            "nak_rx_count": "0",
            "offer_rx_count": "1",
            "release_tx_count": "0",
            "request_tx_count": "1",
            "success_percentage": "100",
            "total_attempted": "1",
            "total_bound": "1",
            "total_failed": "0",
            "total_retried": "0"
        },
        "group": {
            "dhcpv4blockconfig1": {
                "1": {
                    "discover_resp_time": "0.00952004",
                    "error_status": "OK",
                    "ipv4_addr": "1.1.1.10",
                    "lease_left": "290.39396338",
                    "lease_rx": "300",
                    "mac_addr": "00:10:94:00:00:02",
                    "request_resp_time": "0.00355514",
                    "session_state": "BOUND",
                    "vci": "32",
                    "vlan_id": "1",
                    "vpi": "0"
                },
                "ack_rx_count": "1",
                "attempt_rate": "0",
                "bind_rate": "75.8329491130578",
                "bound_renewed": "0",
                "currently_attempting": "0",
                "currently_bound": "1",
                "currently_idle": "0",
                "discover_tx_count": "1",
                "elapsed_time": "0.01326492",
                "nak_rx_count": "0",
                "offer_rx_count": "1",
                "release_rate": "-",
                "release_tx_count": "0",
                "request_rate": "-",
                "request_tx_count": "1",
                "total_attempted": "1",
                "total_bound": "1",
                "total_failed": "0",
                "total_retried": "0"
            }
        },
        "session": {
            "dhcpv4blockconfig1": {
                "ack_rx_count": "1",
                "address": "1.1.1.10",
                "attempt_rate": "0",
                "bind_rate": "75.8329491130578",
                "bound_renewed": "0",
                "currently_attempting": "0",
                "currently_bound": "1",
                "currently_idle": "0",
                "discover_resp_time": "0.00952004",
                "discover_tx_count": "1",
                "elapsed_time": "0.01326492",
                "error_status": "OK",
                "ipv4_addr": "1.1.1.10",
                "lease_left": "290.39396338",
                "lease_rx": "300",
                "lease_time": "300",
                "mac_addr": "00:10:94:00:00:02",
                "nak_rx_count": "0",
                "offer_rx_count": "1",
                "release_rate": "-",
                "release_tx_count": "0",
                "request_rate": "-",
                "request_resp_time": "0.00355514",
                "request_tx_count": "1",
                "session_state": "BOUND",
                "total_attempted": "1",
                "total_bound": "1",
                "total_failed": "0",
                "total_retried": "0",
                "vci": "32",
                "vlan_id": "1",
                "vpi": "0"
            }
        },
        "status": "1"
    },
    {
        "aggregate": {
            "adv_rx_count": "1",
            "avg_rebind_repl_time": "0",
            "avg_release_repl_time": "0",
            "avg_renew_repl_time": "0",
            "avg_request_repl_time": "3.24344",
            "avg_soli_adv_time": "18.7403",
            "avg_soli_repl_time": "1004.3191",
            "currently_attempting": "0",
            "currently_bound": "1",
            "currently_idle": "0",
            "elapsed_time": "2.00734522",
            "info_request_tx_count": "0",
            "max_rebind_repl_time": "0",
            "max_release_repl_time": "0",
            "max_renew_repl_time": "0",
            "max_request_repl_time": "3.24344",
            "max_soli_adv_time": "18.7403",
            "max_soli_repl_time": "1004.3191",
            "min_rebind_repl_time": "0",
            "min_release_repl_time": "0",
            "min_renew_repl_time": "0",
            "min_request_repl_time": "3.24344",
            "min_soli_adv_time": "18.7403",
            "min_soli_repl_time": "1004.3191",
            "prefix_count": "1",
            "rebind_rate": "0",
            "release_tx_count": "0",
            "renew_rate": "0",
            "reply_rx_count": "1",
            "request_tx_count": "1",
            "setup_fail": "0",
            "setup_initiated": "1",
            "setup_success": "1",
            "setup_success_rate": "0.995699474400118",
            "solicits_tx_count": "1",
            "state": "BOUND"
        },
        "ipv6": {
            "aggregate": {
                "adv_rx_count": "1",
                "avg_rebind_repl_time": "0",
                "avg_release_repl_time": "0",
                "avg_renew_repl_time": "0",
                "avg_request_repl_time": "3.24344",
                "avg_soli_adv_time": "18.7403",
                "avg_soli_repl_time": "1004.3191",
                "currently_attempting": "0",
                "currently_bound": "1",
                "currently_idle": "0",
                "elapsed_time": "2.00734522",
                "info_request_tx_count": "0",
                "max_rebind_repl_time": "0",
                "max_release_repl_time": "0",
                "max_renew_repl_time": "0",
                "max_request_repl_time": "3.24344",
                "max_soli_adv_time": "18.7403",
                "max_soli_repl_time": "1004.3191",
                "min_rebind_repl_time": "0",
                "min_release_repl_time": "0",
                "min_renew_repl_time": "0",
                "min_request_repl_time": "3.24344",
                "min_soli_adv_time": "18.7403",
                "min_soli_repl_time": "1004.3191",
                "prefix_count": "1",
                "rebind_rate": "0",
                "release_tx_count": "0",
                "renew_rate": "0",
                "reply_rx_count": "1",
                "request_tx_count": "1",
                "setup_fail": "0",
                "setup_initiated": "1",
                "setup_success": "1",
                "setup_success_rate": "0.995699474400118",
                "solicits_tx_count": "1",
                "state": "BOUND"
            },
            "dhcpv6blockconfig1": {
                "1": {
                    "dhcpv6_ipv6_addr": "abcd::10",
                    "dhcpv6_lease_left": "289.9923833",
                    "dhcpv6_lease_rx": "300",
                    "dhcpv6_prefix_length": "0",
                    "dhcpv6_session_state": "BOUND",
                    "dhcpv6_status_code": "OK",
                    "dhcpv6_status_string": "",
                    "ipv6_addr": "abcd::10",
                    "lease_left": "289.9923833",
                    "lease_rx": "300",
                    "mac_addr": "00:10:94:00:00:02",
                    "pd_ipv6_addr": "::",
                    "pd_lease_left": "0",
                    "pd_lease_rx": "0",
                    "pd_prefix_length": "0",
                    "pd_session_state": "IDLE",
                    "pd_status_code": "OK",
                    "pd_status_string": "",
                    "request_resp_time": "0.00324344",
                    "session_index": "0",
                    "session_state": "BOUND",
                    "solicit_resp_time": "0.0187403",
                    "status_code": "OK",
                    "status_string": "",
                    "vlan_id": ""
                }
            }
        },
        "session": {
            "dhcpv6blockconfig1": {
                "address": "abcd::10",
                "dhcpv6_ipv6_addr": "abcd::10",
                "dhcpv6_lease_left": "289.9923833",
                "dhcpv6_lease_rx": "300",
                "dhcpv6_prefix_length": "0",
                "dhcpv6_session_state": "BOUND",
                "dhcpv6_status_code": "OK",
                "dhcpv6_status_string": "",
                "ipv6_addr": "abcd::10",
                "lease_left": "289.9923833",
                "lease_rx": "300",
                "lease_time": "300",
                "mac_addr": "00:10:94:00:00:02",
                "pd_ipv6_addr": "::",
                "pd_lease_left": "0",
                "pd_lease_rx": "0",
                "pd_prefix_length": "0",
                "pd_session_state": "IDLE",
                "pd_status_code": "OK",
                "pd_status_string": "",
                "request_resp_time": "0.00324344",
                "session_index": "0",
                "session_state": "BOUND",
                "solicit_resp_time": "0.0187403",
                "status_code": "OK",
                "status_string": "",
                "vlan_id": ""
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "1/11/2": {
            "aggregate": {
                "ack_rx_count": "1",
                "addr_discovered": "1",
                "average_setup_time": "1.00",
                "avgerage_teardown_rate": "0.00",
                "currently_attempting": "1",
                "currently_bound": "1",
                "currently_idle": "0",
                "declines_tx_count": "0",
                "discover_tx_count": "1",
                "enabled_interfaces": "1",
                "nak_rx_count": "0",
                "offer_rx_count": "1",
                "port_name": "1/11/2",
                "release_tx_count": "0",
                "request_tx_count": "1",
                "rx": {
                    "force_renew": "0"
                },
                "sessions_not_started": "0",
                "sessions_total": "1",
                "setup_fail": "0",
                "setup_initiated": "1",
                "setup_success": "1",
                "success_percentage": "100",
                "teardown_failed": "0",
                "teardown_initiated": "0",
                "teardown_success": "0",
                "total_attempted": "1",
                "total_failed": "0"
            }
        },
        "aggregate": {
            "ack_rx_count": "1",
            "addr_discovered": "1",
            "average_setup_time": "1.00",
            "avgerage_teardown_rate": "0.00",
            "currently_attempting": "1",
            "currently_bound": "1",
            "currently_idle": "0",
            "declines_tx_count": "0",
            "discover_tx_count": "1",
            "enabled_interfaces": "1",
            "nak_rx_count": "0",
            "offer_rx_count": "1",
            "port_name": "1/11/2",
            "release_tx_count": "0",
            "request_tx_count": "1",
            "rx": {
                "force_renew": "0"
            },
            "sessions_not_started": "0",
            "sessions_total": "1",
            "setup_fail": "0",
            "setup_initiated": "1",
            "setup_success": "1",
            "success_percentage": "100",
            "teardown_failed": "0",
            "teardown_initiated": "0",
            "teardown_success": "0",
            "total_attempted": "1",
            "total_failed": "0"
        },
        "session": {
            "/topology:1/deviceGroup:1/ethernet:1/dhcpv4client:1/item:1": {
                "Address": "1.1.1.10",
                "Gateway": "removePacket[Unresolved]",
                "Prefix": "24",
                "ack/rapid_commit_rx": "0",
                "ack_rx_count": "1",
                "address": "1.1.1.10",
                "declines_tx_count": "0",
                "device_group": "Device Group 1",
                "device_id": "1",
                "discover/rapid_commit_tx": "0",
                "discover_tx_count": "1",
                "gateway": "0.0.0.0",
                "information": "none",
                "lease/rapid_commit": "No",
                "lease_establishment_time": "6",
                "lease_time": "300",
                "nak_rx_count": "0",
                "offer_rx_count": "1",
                "protocol": "DHCPv4 Client 1",
                "release_tx_count": "0",
                "request_tx_count": "1",
                "rx": {
                    "force_renew": "0"
                },
                "status": "Up",
                "topology": "Topology 1"
            }
        },
        "status": "1"
    },
    {
        "1/11/2": {
            "aggregate": {
                "addr_discovered": "1",
                "adv_ignored": "0",
                "adv_rx_count": "1",
                "average_setup_time": "0.48",
                "avgerage_teardown_rate": "0.00",
                "currently_attempting": "1",
                "currently_bound": "1",
                "currently_idle": "0",
                "enabled_interfaces": "1",
                "information_request_tx": "0",
                "port_name": "1/11/2",
                "rebinds_tx": "0",
                "reconfigure_rx": "0",
                "release_tx_count": "0",
                "renew_tx": "0",
                "reply_rx_count": "1",
                "request_tx_count": "1",
                "rx": {
                    "nak": "0"
                },
                "sessions_not_started": "0",
                "sessions_total": "1",
                "setup_fail": "0",
                "setup_initiated": "1",
                "setup_success": "1",
                "solicits_tx_count": "1",
                "success_percentage": "100",
                "teardown_failed": "0",
                "teardown_initiated": "0",
                "teardown_success": "0",
                "total_attempted": "1",
                "total_failed": "0"
            }
        },
        "aggregate": {
            "addr_discovered": "1",
            "adv_ignored": "0",
            "adv_rx_count": "1",
            "average_setup_time": "0.48",
            "avgerage_teardown_rate": "0.00",
            "currently_attempting": "1",
            "currently_bound": "1",
            "currently_idle": "0",
            "enabled_interfaces": "1",
            "information_request_tx": "0",
            "port_name": "1/11/2",
            "rebinds_tx": "0",
            "reconfigure_rx": "0",
            "release_tx_count": "0",
            "renew_tx": "0",
            "reply_rx_count": "1",
            "request_tx_count": "1",
            "rx": {
                "nak": "0"
            },
            "sessions_not_started": "0",
            "sessions_total": "1",
            "setup_fail": "0",
            "setup_initiated": "1",
            "setup_success": "1",
            "solicits_tx_count": "1",
            "success_percentage": "100",
            "teardown_failed": "0",
            "teardown_initiated": "0",
            "teardown_success": "0",
            "total_attempted": "1",
            "total_failed": "0"
        },
        "session": {
            "/topology:1/deviceGroup:2/ethernet:1/dhcpv6client:1/item:1": {
                "Address": "abcd:0:0:0:0:0:0:10",
                "Gateway": "removePacket[Unresolved]",
                "NumberOfAddresses": "0",
                "NumberOfPrefixes": "0",
                "Prefix": "removePacket[Unresolved]",
                "PrefixLength": "removePacket[Unresolved]",
                "address": "abcd:0:0:0:0:0:0:10",
                "adv_ignored": "0",
                "adv_rx_count": "1",
                "device_group": "Device Group 2",
                "device_id": "1",
                "dns_search_list": "Not Available",
                "dns_server_list": "Not Available",
                "establishment_time": "1047",
                "gw_addr": "0:0:0:0:0:0:0:0",
                "info_req_tx": "0",
                "information": "none",
                "ip_addr": "abcd:0:0:0:0:0:0:10",
                "lease/rapid_commit": "No",
                "lease_id": "1",
                "lease_time": "300",
                "lease_time_prefix": "0",
                "prefix_addr": "0:0:0:0:0:0:0:0",
                "prefix_len": "0",
                "protocol": "DHCPv6 Client 1",
                "rebinds_tx": "0",
                "reconfigure_rx": "0",
                "release_tx_count": "0",
                "renew_tx": "0",
                "replies/rapid_commit_rx": "0",
                "reply_rx_count": "1",
                "request_tx_count": "1",
                "session_id": "1",
                "solicits/rapid_commit_tx": "0",
                "solicits_tx_count": "1",
                "status": "Up",
                "topology": "Topology 1"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['port_handle'] = port_handle
    args['action'] = action
    args['ip_version'] = dhcp_version

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
#    handle = list(set(handle))
    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                for indi in v6_handles:
                    if isinstance(indi, list) and hnd in indi:
                        args['ip_version'] = '6'
                    if hnd in handle_map:
                        args['handle'] = handle_map[hnd]
                stats = dict()
                if hnd.startswith('dhcpv4portconfig') or hnd.startswith('dhcpv6portconfig'):
                    args['mode'] = 'aggregate'
                    stats.update(rt_handle.invoke('emulation_dhcp_stats', **args))
                args['mode'] = 'session'
                stats.update(rt_handle.invoke('emulation_dhcp_stats', **args))
                args['mode'] = 'detailed_session'
                stats.update(rt_handle.invoke('emulation_dhcp_stats', **args))
                ret.append(stats)
                if 'ip_version' in args:
                    del args['ip_version']
        else:
            args['handle'] = hndl
            for indi in v6_handles:
                if isinstance(indi, list) and hndl in indi:
                    args['ip_version'] = '6'
                if hndl in handle_map:
                    args['handle'] = handle_map[hndl]
            stats = dict()
            if hndl.startswith('dhcpv4portconfig') or hndl.startswith('dhcpv6portconfig'):
                args['mode'] = 'aggregate'
                stats.update(rt_handle.invoke('emulation_dhcp_stats', **args))
            args['mode'] = 'session'
            stats.update(rt_handle.invoke('emulation_dhcp_stats', **args))
            args['mode'] = 'detailed_session'
            stats.update(rt_handle.invoke('emulation_dhcp_stats', **args))
            ret.append(stats)
            if 'ip_version' in args:
                del args['ip_version']
    # ***** Return Value Modification *****
    
    for index in range(len(ret)):
        if 'group' in ret[index]:
            ret[index]['session'] = dict()
            for key in ret[index]['group']:
                ret[index]['session'][key] = dict()
                for nkey in ret[index]['group'][key]:
                    if isinstance(ret[index]['group'][key][nkey], dict):
                        for gkey in ret[index]['group'][key][nkey]:
                            ret[index]['session'][key][gkey] = dict()
                            ret[index]['session'][key][gkey] = ret[index]['group'][key][nkey][gkey]
                        if 'ipv4_addr' in ret[index]['group'][key][nkey]:
                            ret[index]['session'][key]['address'] = ret[index]['group'][key][nkey]['ipv4_addr']
                        if 'lease_rx' in ret[index]['group'][key][nkey]:
                            ret[index]['session'][key]['lease_time'] = ret[index]['group'][key][nkey]['lease_rx']
                    else:
                        ret[index]['session'][key][nkey] = ret[index]['group'][key][nkey]

        if 'ipv6' in ret[index]:
            ret[index]['session'] = dict()
            for key in ret[index]['ipv6']:
                if key == 'aggregate':
                    ret[index]['aggregate'] = ret[index]['ipv6']['aggregate']
                else:
                    ret[index]['session'][key] = dict()
                    for nkey in ret[index]['ipv6'][key]:
                        if isinstance(ret[index]['ipv6'][key][nkey], dict):
                            for gkey in ret[index]['ipv6'][key][nkey]:
                                ret[index]['session'][key][gkey] = dict()
                                ret[index]['session'][key][gkey] = ret[index]['ipv6'][key][nkey][gkey]
                            if 'ipv6_addr' in ret[index]['ipv6'][key][nkey]:
                                ret[index]['session'][key]['address'] = ret[index]['ipv6'][key][nkey]['ipv6_addr']
                            if 'lease_rx' in ret[index]['ipv6'][key][nkey]:
                                ret[index]['session'][key]['lease_time'] = ret[index]['ipv6'][key][nkey]['lease_rx']
                        else:
                            ret[index]['session'][key][nkey] = ret[index]['ipv6'][key][nkey]

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_igmp_config(
        rt_handle,
        filter_mode=jNone,
        handle=jNone,
        igmp_version=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_len=jNone,
        ip_router_alert=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        port_handle=jNone,
        count=jNone,
        msg_interval=jNone,
        general_query=jNone,
        group_query=jNone,
        max_response_time=jNone,
        max_response_control=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_mode=jNone,
        vlan_id_outer_step=jNone,
        vlan_outer_user_priority=jNone):
    """
    :param rt_handle:       RT object
    :param filter_mode - <include|exclude>
    :param handle
    :param igmp_version - <v1|v2|v3>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_len - <1-32>
    :param ip_router_alert - <0|1>
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4096>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|delete|disable_all>
    :param port_handle
    :param count - <1-65535>
    :param msg_interval - <0-4294967295>
    :param general_query - <1>
    :param group_query - <1>
    :param max_response_time
    :param max_response_control
    :param vlan_id_outer - <0-4095>
    :param vlan_id_outer_mode - <fixed|increment>
    :param vlan_id_outer_step - <0-4096>
    :param vlan_outer_user_priority - <0-7>

    Spirent Returns:
    {
        "handle": "host2",
        "handles": "igmphostconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1",
        "igmp_host_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1",
        "igmp_host_iptv_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/iptv",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['filter_mode'] = filter_mode
    args['handle'] = handle
    args['igmp_version'] = igmp_version
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_len'] = intf_prefix_len
    args['ip_router_alert'] = ip_router_alert
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['neighbor_intf_ip_addr_step'] = neighbor_intf_ip_addr_step
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['port_handle'] = port_handle
    args['count'] = count
    args['msg_interval'] = msg_interval
    args['general_query'] = general_query
    args['group_query'] = group_query
    args['vlan_id_outer'] = vlan_id_outer
    args['vlan_id_outer_mode'] = vlan_id_outer_mode
    args['vlan_id_outer_step'] = vlan_id_outer_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_igmp_config.__doc__, **args)   

    if port_handle == jNone:
        __check_and_raise(handle)
    elif handle == jNone:
        __check_and_raise(port_handle)

#    if 'handle' in args and not isinstance(handle, list):
#        handle = [handle]
#        handle = list(set(handle))

    counter = 1
    string = "igmp_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "igmp_" + str(counter)
    global_config[string] = []

    ret = []
    if handle != jNone:
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                ret.append(invoke_handle(rt_handle, protocol_string=string, **args))
                break
            else:
                args['handle'] = hndl
                result = rt_handle.invoke('emulation_igmp_config', **args)
                if result.get('handles'):
                    global_config[string].extend(result['handles'].split(' '))
 #                   result['handle'] = result['handles']
                    result['handles'] = string
                    ret.append(result)
        if mode == 'create':
            for hndl in handle:
                if hndl in global_config.keys():
                    port_handle = __get_handle(hndl)
                else:
                    port_handle = rt_handle.invoke('invoke', cmd='stc::get '+hndl+' -AffiliatedPort')
                handle_map[port_handle].extend(global_config[string])
                handle_map[string] = port_handle
    elif port_handle != jNone:
        result = rt_handle.invoke('emulation_igmp_config', **args)
        if result.get('handle'):
            global_config[string].extend(result['handle'].split(' '))
            result['handles'] = string
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        if mode == 'create':
            for hand in port_handle:
                handle_map[hand] = handle_map.get(hand, [])
                handle_map[hand].extend(global_config[string])
                handle_map[hand] = list(set(handle_map[hand]))
                handle_map[string] = hand
        ret.append(result)
    if mode == 'create' or  mode == 'modify':
        if max_response_time != jNone:
            for index in range(len(ret)):
                if 'handle' in ret[index]:
                    myHandle = ret[index]['handles']
                    if myHandle in global_config.keys():
                        for hnd in global_config[myHandle]:
                            if 'igmphost' in hnd:
                                hnd = rt_handle.invoke('invoke', cmd='stc::get' + " " + hnd + ' -parent')
                            igmp_route_handle = rt_handle.invoke('invoke', cmd='stc::get' + " " + hnd  + ' -children-igmprouterconfig')
                            if 'igmp' not in igmp_route_handle:
                                igmp_route_handle = rt_handle.invoke('invoke', cmd='stc::create' + ' igmprouterconfig -under ' + hnd + ' -QueryResponseInterval' + " " + max_response_time)
                            else:
                                rt_handle.invoke('invoke', cmd='stc::config' + " " + igmp_route_handle + ' -QueryResponseInterval' + " " + max_response_time)
                    else:
                        if 'igmphost' in myHandle:
                            myHandle = rt_handle.invoke('invoke', cmd='stc::get' + " " + myHandle + ' -parent')
                        igmp_route_handle = rt_handle.invoke('invoke', cmd='stc::get' + " " + myHandle  + ' -children-igmprouterconfig')
                        if 'igmp' not in igmp_route_handle:
                            igmp_route_handle = rt_handle.invoke('invoke', cmd='stc::create' + ' igmprouterconfig -under ' + myHandle + ' -QueryResponseInterval' + " " + max_response_time)
                        else:
                            rt_handle.invoke('invoke', cmd='stc::config' + " " + igmp_route_handle + ' -QueryResponseInterval' + " " + max_response_time)

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_igmp_control(rt_handle, handle=jNone,
                             mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <restart|join:start|leave:stop>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_igmp_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            hnd = " ".join(global_config[hndl])
            args['handle'] = hnd
            ret.append(rt_handle.invoke('emulation_igmp_control', **args))
        else:
            args['handle'] = hndl
            ret.append(rt_handle.invoke('emulation_igmp_control', **args)) 
    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_igmp_group_config(
        rt_handle,
        group_pool_handle=jNone,
        handle=jNone,
        mode=jNone,
        session_handle=jNone,
        source_pool_handle=jNone,
        g_filter_mode=jNone):
    """
    :param rt_handle:       RT object
    :param group_pool_handle
    :param handle
    :param mode - <create|modify|delete|clear_all>
    :param session_handle
    :param source_pool_handle
    :param g_filter_mode - <include|exclude>

    Spirent Returns:
    {
        "group_handles": "ipv4group1",
        "handle": "igmpgroupmembership1",
        "status": "1"
    }

    IXIA Returns:
    {
        "group_handles": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList",
        "igmp_group_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList",
        "igmp_source_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList/igmpUcastIPv4SourceList",
        "source_handles": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList/igmpUcastIPv4SourceList",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "group_handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['group_pool_handle'] = group_pool_handle
    args['handle'] = handle
    args['mode'] = mode
    args['session_handle'] = session_handle
    args['source_pool_handle'] = source_pool_handle
    args['g_filter_mode'] = g_filter_mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
  
    args = get_arg_value(rt_handle, j_emulation_igmp_group_config.__doc__, **args)

    if 'g_filter_mode' in args:
        args['filter_mode'] = args['g_filter_mode']
        del args['g_filter_mode']

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    counter = 1
    string = "igmp_group_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "igmp_group_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()

    for hndl in handle:
        status = 1
        new_ret = dict()
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                if hnd in handle_list:
                    continue
                else:
                    handle_list[hnd] = 1
                args['handle'] = hnd
                if mode == 'create':
                    args['session_handle'] = hnd
                newer_ret = rt_handle.invoke('emulation_igmp_group_config', **args)
                if 'status' in newer_ret:
                    if newer_ret['status'] == 0:
                        status = 0
                if 'handle' in newer_ret:
                    global_config[string].extend([newer_ret['handle']])
                for key in newer_ret:
                    try:
                        new_ret[key]
                    except:
                        new_ret[key] = []
                    new_ret[key].append(newer_ret[key])
        else:
            if hndl in handle_list:
                continue
            else:
                handle_list[hndl] = 1
            args['handle'] = hndl
            if mode == 'create':
                args['session_handle'] = hndl
            newer_ret = rt_handle.invoke('emulation_igmp_group_config', **args)
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'handle' in newer_ret:
                global_config[string].extend([newer_ret['handle']])
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if 'handles' in new_ret:
            new_ret['handle'] = new_ret['handles']
        new_ret['handles'] = string
        if new_ret:
            ret.append(new_ret)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'group_pool_handle' in args:
            ret[index]['group_handles'] = args['group_pool_handle']
        if 'source_pool_handle' in args:
            ret[index]['source_handles'] = args['source_pool_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_igmp_info(
        rt_handle,
        handle=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle

    Spirent Returns:
    {
        "dropped_pkts": "0",
        "group_membership_stats": {
            "group_addr": {
                "225": {
                    "0": {
                        "0": {
                            "1": {
                                "host_addr": {
                                    "3": {
                                        "3": {
                                            "3": {
                                                "2": {
                                                    "duplicate_join": "false",
                                                    "join_failure": "false",
                                                    "join_latency": "0",
                                                    "join_timestamp": "4Days-03:43:59.31120207",
                                                    "leave_latency": "0",
                                                    "leave_timestamp": "0Days-00:00:00.00000000",
                                                    "state": "IDLE_MEMBER",
                                                    "state_change_timestamp": "4Days-03:44:03.48055190"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "igmpv1_mem_reports_rx": "0",
        "igmpv1_mem_reports_tx": "0",
        "igmpv1_queries_rx": "0",
        "igmpv2_group_queries_rx": "0",
        "igmpv2_leave_tx": "0",
        "igmpv2_mem_reports_rx": "0",
        "igmpv2_mem_reports_tx": "2",
        "igmpv2_queries_rx": "0",
        "igmpv3_group_queries_rx": "0",
        "igmpv3_group_src_queries_rx": "0",
        "igmpv3_mem_reports_rx": "0",
        "igmpv3_mem_reports_tx": "0",
        "igmpv3_queries_rx": "0",
        "invalid_pkts": "0",
        "port_stats": {
            "port2": {
                "-": {
                    "dropped_pkts": "0",
                    "invalid_pkts": "0"
                },
                "V1": {
                    "igmpv1_mem_reports_rx": "0",
                    "igmpv1_mem_reports_tx": "0",
                    "igmpv1_queries_rx": "0"
                },
                "V2": {
                    "igmpv2_group_queries_rx": "0",
                    "igmpv2_leave_tx": "0",
                    "igmpv2_mem_reports_rx": "0",
                    "igmpv2_mem_reports_tx": "2",
                    "igmpv2_queries_rx": "0"
                },
                "V3": {
                    "igmpv3_group_queries_rx": "0",
                    "igmpv3_group_src_queries_rx": "0",
                    "igmpv3_mem_reports_rx": "0",
                    "igmpv3_mem_reports_tx": "0",
                    "igmpv3_queries_rx": "0"
                }
            }
        },
        "session": {
            "igmphostconfig1": {
                "avg_join_latency": "0",
                "avg_leave_latency": "0",
                "max_join_latency": "0",
                "max_leave_latency": "0",
                "min_join_latency": "0",
                "min_leave_latency": "0"
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/item:1": {
            "session": {
                "igmp": {
                    "aggregate": {
                        "gen_query_rx": "1",
                        "grp_query_rx": "0",
                        "invalid_rx": "0",
                        "leave_v2_rx": "0",
                        "leave_v2_tx": "0",
                        "pair_joined": "1",
                        "port_name": "1/11/1",
                        "rprt_v1_rx": "0",
                        "rprt_v1_tx": "0",
                        "rprt_v2_rx": "0",
                        "rprt_v2_tx": "2",
                        "rprt_v3_rx": "0",
                        "rprt_v3_tx": "0",
                        "total_rx": "1",
                        "total_tx": "2",
                        "v3_allow_new_source_rx": "0",
                        "v3_allow_new_source_tx": "0",
                        "v3_block_old_source_rx": "0",
                        "v3_block_old_source_tx": "0",
                        "v3_change_mode_exclude_rx": "0",
                        "v3_change_mode_exclude_tx": "0",
                        "v3_change_mode_include_rx": "0",
                        "v3_change_mode_include_tx": "0",
                        "v3_mode_exclude_rx": "0",
                        "v3_mode_exclude_tx": "0",
                        "v3_mode_include_rx": "0",
                        "v3_mode_include_tx": "0"
                    }
                }
            }
        },
        "Device Group 2": {
            "IGMP Host Stats Per Device": {
                "igmp": {
                    "aggregate": {
                        "gen_query_rx": "1",
                        "grp_query_rx": "0",
                        "invalid_rx": "0",
                        "leave_v2_rx": "0",
                        "leave_v2_tx": "0",
                        "pair_joined": "1",
                        "rprt_v1_rx": "0",
                        "rprt_v1_tx": "0",
                        "rprt_v2_rx": "0",
                        "rprt_v2_tx": "2",
                        "rprt_v3_rx": "0",
                        "rprt_v3_tx": "0",
                        "total_rx": "1",
                        "total_tx": "2",
                        "v3_allow_new_source_rx": "0",
                        "v3_allow_new_source_tx": "0",
                        "v3_block_old_source_rx": "0",
                        "v3_block_old_source_tx": "0",
                        "v3_change_mode_exclude_rx": "0",
                        "v3_change_mode_exclude_tx": "0",
                        "v3_change_mode_include_rx": "0",
                        "v3_change_mode_include_tx": "0",
                        "v3_group_and_source_specific_queries_rx": "0",
                        "v3_mode_exclude_rx": "0",
                        "v3_mode_exclude_tx": "0",
                        "v3_mode_include_rx": "0",
                        "v3_mode_include_tx": "0"
                    }
                },
                "sessions_down": "0",
                "sessions_notstarted": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "status": "started"
            }
        },
        "igmpv1_mem_reports_rx": "0",
        "igmpv1_mem_reports_tx": "0",
        "igmpv2_group_queries_rx": "0",
        "igmpv2_leave_tx": "0",
        "igmpv2_mem_reports_rx": "0",
        "igmpv2_mem_reports_tx": "2",
        "igmpv2_queries_rx": "1",
        "igmpv3_group_src_queries_rx": "0",
        "igmpv3_mem_reports_rx": "0",
        "igmpv3_mem_reports_tx": "0",
        "status": "1"
    },
    {
        "1/11/2": {
            "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:1": {
                "querier_address": "3.3.3.1",
                "querier_version": "v2",
                "record": {
                    "1": {
                        "compatibility_mode": "v2",
                        "compatibility_timer": "0",
                        "filter_mode": "N/A",
                        "group_adress": "225.0.0.1",
                        "group_timer": "247",
                        "source_address": "N/A",
                        "source_timer": "0"
                    }
                }
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
        "igmpv1_mem_reports_rx"
        "igmpv1_mem_reports_tx"
        "igmpv2_group_queries_rx"
        "igmpv2_leave_tx"
        "igmpv2_mem_reports_rx"
        "igmpv2_mem_reports_tx"
        "igmpv2_queries_rx"
        "igmpv3_group_src_queries_rx"
        "igmpv3_mem_reports_rx"
        "igmpv3_mem_reports_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        status = 1
        new_ret = dict()
        args['handle'] = hndl
        del args['handle']
        if hndl in global_config.keys():
            port_handle = __get_handle(hndl)
        else:
            port_handle = rt_handle.invoke('invoke', cmd='stc::get '+hndl+' -AffiliatedPort')
        args['port_handle'] = port_handle
        newer_ret = dict()
        args['mode'] = 'stats'
        newer_ret.update(rt_handle.invoke('emulation_igmp_info', **args))

        if 'status' in newer_ret:
            if newer_ret['status'] == 0:
                status = 0
        for key in newer_ret:
            try:
                new_ret[key]
            except:
                new_ret[key] = []
            new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if new_ret:
            ret.append(new_ret)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'port_stats' in ret[index]:
            for key in list(ret[index]['port_stats']):
                for n_key in list(ret[index]['port_stats'][key]):
                    for new_key in list(ret[index]['port_stats'][key][n_key]):
                        ret[index][new_key] = ret[index]['port_stats'][key][n_key][new_key]

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_igmp_querier_config(
        rt_handle,
        handle=jNone,
        igmp_version=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_len=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        query_interval=jNone,
        robustness_variable=jNone,
        startup_query_count=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param igmp_version - <v1|v2|v3>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_len - <1-32>
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param query_interval - <1-31744>
    :param robustness_variable - <2-7>
    :param startup_query_count - <2-255>
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4096>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|delete>
    :param port_handle

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1",
        "igmp_querier_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1",
        "igmp_querier_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['handle'] = handle
    args['igmp_version'] = igmp_version
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_len'] = intf_prefix_len
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['neighbor_intf_ip_addr_step'] = neighbor_intf_ip_addr_step
    args['query_interval'] = query_interval
    args['robustness_variable'] = robustness_variable
    args['startup_query_count'] = startup_query_count
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_igmp_querier_config.__doc__, **args)   
   
    if port_handle == jNone:
        __check_and_raise(handle)
    elif handle == jNone:
        __check_and_raise(port_handle)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    counter = 1
    string = "igmp_querier_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "igmp_querier_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()
    if 'handle' in args.keys():
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            status = 1
            new_ret = dict()
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    if hnd in handle_list:
                        continue
                    else:
                        handle_list[hnd] = 1
                    args['handle'] = hnd
                    newer_ret = rt_handle.invoke('emulation_igmp_querier_config', **args)
                    if 'status' in newer_ret:
                        if newer_ret['status'] == 0:
                            status = 0
                    if 'handle' in newer_ret:
                        global_config[string].extend([newer_ret['handle']])
                    for key in newer_ret:
                        try:
                            new_ret[key]
                        except:
                            new_ret[key] = []
                        new_ret[key].append(newer_ret[key])
            else:
                if hndl in handle_list:
                    continue
                else:
                    handle_list[hndl] = 1
                args['handle'] = hndl
                newer_ret = rt_handle.invoke('emulation_igmp_querier_config', **args)
                if 'status' in newer_ret:
                    if newer_ret['status'] == 0:
                        status = 0
                if 'handle' in newer_ret:
                    global_config[string].extend([newer_ret['handle']])
                for key in newer_ret:
                    try:
                        new_ret[key]
                    except:
                        new_ret[key] = []
                    new_ret[key].append(newer_ret[key])
            for key in new_ret:
                if len(new_ret[key]) == 1:
                    new_ret[key] = new_ret[key][0]
            if 'status' in new_ret:
                new_ret['status'] = status
            if 'handle' in new_ret:
                new_ret['handles'] = string
            if new_ret:
                ret.append(new_ret)
            if mode == 'create':
                if hndl in global_config.keys():
                    port_handle = __get_handle(hndl)
                else:
                    port_handle = rt_handle.invoke('invoke', cmd='stc::get '+hndl+' -AffiliatedPort')
                handle_map[port_handle].extend(global_config[string])
                handle_map[port_handle] = list(set(handle_map[port_handle]))
                handle_map[string] = port_handle

    elif 'port_handle' in args.keys():
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        result = rt_handle.invoke('emulation_igmp_querier_config', **args)
        if result.get('handle'):
            global_config[string].extend([result['handle']])
            result['handles'] = string
        for hand in port_handle:
            handle_map[hand] = handle_map.get(hand, [])
            handle_map[hand].extend(global_config[string])
            handle_map[string] = hand
        ret.append(result)
    
    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_isis_config(
        rt_handle,
        area_id=jNone,
        bfd_registration=jNone,
        count=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        gateway_ipv6_addr=jNone,
        gateway_ipv6_addr_step=jNone,
        graceful_restart=jNone,
        graceful_restart_restart_time=jNone,
        handle=jNone,
        hello_interval=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_ip_prefix_length=jNone,
        intf_ipv6_addr=jNone,
        intf_ipv6_addr_step=jNone,
        intf_ipv6_prefix_length=jNone,
        intf_metric=jNone,
        intf_type=jNone,
        lsp_life_time=jNone,
        lsp_refresh_interval=jNone,
        overloaded=jNone,
        router_id=jNone,
        routing_level=jNone,
        te_enable=jNone,
        te_max_bw=jNone,
        te_max_resv_bw=jNone,
        te_unresv_bw_priority0=jNone,
        te_unresv_bw_priority1=jNone,
        te_unresv_bw_priority2=jNone,
        te_unresv_bw_priority3=jNone,
        te_unresv_bw_priority4=jNone,
        te_unresv_bw_priority5=jNone,
        te_unresv_bw_priority6=jNone,
        te_unresv_bw_priority7=jNone,
        vlan=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        wide_metrics=jNone,
        mode=jNone,
        system_id=jNone,
        port_handle=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):
    """
    :param rt_handle:       RT object
    :param area_id
    :param bfd_registration
    :param count
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param gateway_ipv6_addr
    :param gateway_ipv6_addr_step
    :param graceful_restart
    :param graceful_restart_restart_time - <0-65535>
    :param handle
    :param hello_interval - <1-65535>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_ip_prefix_length - <1-32>
    :param intf_ipv6_addr
    :param intf_ipv6_addr_step
    :param intf_ipv6_prefix_length - <1-128>
    :param intf_metric - <0-16777215>
    :param intf_type - <broadcast|ptop>
    :param lsp_life_time - <1-65535>
    :param lsp_refresh_interval - <1-65535>
    :param overloaded
    :param router_id
    :param routing_level - <L1|L2|L1L2>
    :param te_enable
    :param te_max_bw
    :param te_max_resv_bw
    :param te_unresv_bw_priority0
    :param te_unresv_bw_priority1
    :param te_unresv_bw_priority2
    :param te_unresv_bw_priority3
    :param te_unresv_bw_priority4
    :param te_unresv_bw_priority5
    :param te_unresv_bw_priority6
    :param te_unresv_bw_priority7
    :param vlan
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <1-4094>
    :param vlan_user_priority - <0-7>
    :param wide_metrics - <0|1>
    :param mode - <create|modify|delete|inactive:disable|active:enable>
    :param system_id
    :param port_handle
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <1-4094>
    :param vlan_outer_user_priority - <0-7>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "session_router": "isislspconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/isisL3:2",
        "isis_l3_handle": "/topology:1/deviceGroup:1/ethernet:1/isisL3:2",
        "isis_l3_router_handle": "/topology:1/deviceGroup:1/isisL3Router:1",
        "isis_l3_te_handle": "/topology:1/deviceGroup:1/ethernet:1/isisL3:2/isisTrafficEngineering",
        "sr_tunnel_handle_rtr": "/topology:1/deviceGroup:1/isisL3Router:1/isisSRTunnelList",
        "sr_tunnel_seg_handle_rtr": "/topology:1/deviceGroup:1/isisL3Router:1/isisSRTunnelList/isisSegmentList:1",
        "srgb_range_handle_rtr": "/topology:1/deviceGroup:1/isisL3Router:1/isisSRGBRangeSubObjectsList:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['area_id'] = area_id
    args['bfd_registration'] = bfd_registration
    args['count'] = count
    args['gateway_ip_addr'] = gateway_ip_addr
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['gateway_ipv6_addr'] = gateway_ipv6_addr
    args['gateway_ipv6_addr_step'] = gateway_ipv6_addr_step
    args['graceful_restart'] = graceful_restart
    args['graceful_restart_restart_time'] = graceful_restart_restart_time
    args['handle'] = handle
    args['hello_interval'] = hello_interval
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_ip_prefix_length'] = intf_ip_prefix_length
    args['intf_ipv6_addr'] = intf_ipv6_addr
    args['intf_ipv6_addr_step'] = intf_ipv6_addr_step
    args['intf_ipv6_prefix_length'] = intf_ipv6_prefix_length
    args['intf_metric'] = intf_metric
    args['intf_type'] = intf_type
    args['lsp_life_time'] = lsp_life_time
    args['lsp_refresh_interval'] = lsp_refresh_interval
    args['overloaded'] = overloaded
    args['router_id'] = router_id
    args['routing_level'] = routing_level
    args['te_enable'] = te_enable
    args['te_max_bw'] = te_max_bw
    args['te_max_resv_bw'] = te_max_resv_bw
    args['te_unresv_bw_priority0'] = te_unresv_bw_priority0
    args['te_unresv_bw_priority1'] = te_unresv_bw_priority1
    args['te_unresv_bw_priority2'] = te_unresv_bw_priority2
    args['te_unresv_bw_priority3'] = te_unresv_bw_priority3
    args['te_unresv_bw_priority4'] = te_unresv_bw_priority4
    args['te_unresv_bw_priority5'] = te_unresv_bw_priority5
    args['te_unresv_bw_priority6'] = te_unresv_bw_priority6
    args['te_unresv_bw_priority7'] = te_unresv_bw_priority7
    args['vlan'] = vlan
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['wide_metrics'] = wide_metrics
    args['mode'] = mode
    args['system_id'] = system_id
    args['port_handle'] = port_handle
    args['vlan_outer_id'] = vlan_outer_id
    args['vlan_outer_id_mode'] = vlan_outer_id_mode
    args['vlan_outer_id_step'] = vlan_outer_id_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority
       
    if (intf_ip_addr != jNone and intf_ipv6_addr == jNone):
        args['ip_version'] = 4
    elif (intf_ip_addr == jNone and intf_ipv6_addr != jNone):
        args['ip_version'] = 6
    elif (intf_ip_addr != jNone and intf_ipv6_addr != jNone):
        args['ip_version'] = '4_6'

    args = get_arg_value(rt_handle, j_emulation_isis_config.__doc__, **args)

    if port_handle == jNone:
        __check_and_raise(handle)
    elif handle == jNone:
        __check_and_raise(port_handle)

    if 'handle' in args and not isinstance(handle, list):
        handle = [handle]
        handle = list(set(handle))

    counter = 1
    string = "isis_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "isis_" + str(counter)
    global_config[string] = []

    ret = []
    if handle != jNone:
        ret.append(invoke_handle(rt_handle, protocol_string=string, **args))
        if mode == 'create':
            for hndl in handle:
                port_handle = __get_handle(hndl)
                handle_map[port_handle].extend(global_config[string])
                handle_map[port_handle] = list(set(handle_map[port_handle]))
                handle_map[string] = port_handle
    elif port_handle != jNone:
        result = rt_handle.invoke('emulation_isis_config', **args)
        if result.get('handle'):
            #result['handle'] = result['handle'].split(' ')
            global_config[string].extend(result['handle'].split(' '))
            result['handles'] = string
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        if mode == 'create':
            for hand in port_handle:
                handle_map[hand] = handle_map.get(hand, [])
                handle_map[hand].extend(global_config[string])
                handle_map[hand] = list(set(handle_map[hand]))
                handle_map[string] = hand
        ret.append(result)
    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_isis_control(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|restart>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode
    args = get_arg_value(rt_handle, j_emulation_isis_control.__doc__, **args)
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        hnd = " ".join(global_config[hndl])
        args['handle'] = hnd
        ret.append(rt_handle.invoke('emulation_isis_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_isis_info(rt_handle, handle=jNone,
                          port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle

    Spirent Returns:
    {
        "aggregated_l1_csnp_rx": "0",
        "aggregated_l1_csnp_tx": "0",
        "aggregated_l1_lan_hello_rx": "0",
        "aggregated_l1_lan_hello_tx": "0",
        "aggregated_l1_lsp_rx": "0",
        "aggregated_l1_lsp_tx": "0",
        "aggregated_l1_psnp_rx": "0",
        "aggregated_l1_psnp_tx": "0",
        "aggregated_l2_csnp_rx": "8",
        "aggregated_l2_csnp_tx": "0",
        "aggregated_l2_lan_hello_rx": "10",
        "aggregated_l2_lan_hello_tx": "10",
        "aggregated_l2_lsp_rx": "5",
        "aggregated_l2_lsp_tx": "1",
        "aggregated_l2_psnp_rx": "0",
        "aggregated_l2_psnp_tx": "0",
        "aggregated_p2p_hello_rx": "0",
        "aggregated_p2p_hello_tx": "0",
        "handles": "host1",
        "procName": "emulation_isis_info",
        "status": "1"
    }

    IXIA Returns:
    {
        "Device Group 1": {
            "aggregate": {
                "aggregated_l1_csnp_rx": "0",
                "aggregated_l1_csnp_tx": "0",
                "aggregated_l1_db_size": "0",
                "aggregated_l1_full_count": "0",
                "aggregated_l1_hellos_rx": "0",
                "aggregated_l1_hellos_tx": "0",
                "aggregated_l1_init_count": "0",
                "aggregated_l1_lsp_rx": "0",
                "aggregated_l1_lsp_tx": "0",
                "aggregated_l1_p2p_hellos_rx": "0",
                "aggregated_l1_p2p_hellos_tx": "0",
                "aggregated_l1_psnp_rx": "0",
                "aggregated_l1_psnp_tx": "0",
                "aggregated_l2_csnp_rx": "1",
                "aggregated_l2_csnp_tx": "0",
                "aggregated_l2_db_size": "2",
                "aggregated_l2_full_count": "1",
                "aggregated_l2_hellos_rx": "2",
                "aggregated_l2_hellos_tx": "2",
                "aggregated_l2_init_count": "0",
                "aggregated_l2_lsp_rx": "1",
                "aggregated_l2_lsp_tx": "0",
                "aggregated_l2_p2p_hellos_rx": "0",
                "aggregated_l2_p2p_hellos_tx": "0",
                "aggregated_l2_psnp_rx": "0",
                "aggregated_l2_psnp_tx": "0",
                "l1_full_neighbors": "0",
                "l1_sessions_flap": "0",
                "l1_sessions_up": "0",
                "l2_full_neighbors": "1",
                "l2_sessions_flap": "0",
                "l2_sessions_up": "1",
                "sessions_down": "0",
                "sessions_notstarted": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "status": "started"
            }
        },
        "aggregated_l1_csnp_rx": "0",
        "aggregated_l1_csnp_tx": "0",
        "aggregated_l1_lan_hello_rx": "0",
        "aggregated_l1_lan_hello_tx": "0",
        "aggregated_l1_lsp_rx": "0",
        "aggregated_l1_lsp_tx": "0",
        "aggregated_l1_psnp_rx": "0",
        "aggregated_l1_psnp_tx": "0",
        "aggregated_l2_csnp_rx": "1",
        "aggregated_l2_csnp_tx": "0",
        "aggregated_l2_lan_hello_rx": "2",
        "aggregated_l2_lan_hello_tx": "2",
        "aggregated_l2_lsp_rx": "1",
        "aggregated_l2_lsp_tx": "0",
        "aggregated_l2_psnp_rx": "0",
        "aggregated_l2_psnp_tx": "0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "aggregated_l1_csnp_rx"
        "aggregated_l1_csnp_tx"
        "aggregated_l1_lan_hello_rx"
        "aggregated_l1_lan_hello_tx"
        "aggregated_l1_lsp_rx"
        "aggregated_l1_lsp_tx"
        "aggregated_l1_psnp_rx"
        "aggregated_l1_psnp_tx"
        "aggregated_l2_csnp_rx"
        "aggregated_l2_csnp_tx"
        "aggregated_l2_lan_hello_rx"
        "aggregated_l2_lan_hello_tx"
        "aggregated_l2_lsp_rx"
        "aggregated_l2_lsp_tx"
        "aggregated_l2_psnp_rx"
        "aggregated_l2_psnp_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            args['handle'] = hnd

            newer_ret = dict()
            args['mode'] = 'stats'
            newer_ret.update(rt_handle.invoke('emulation_isis_info', **args))

            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if new_ret:
            ret.append(new_ret)

    # **** Add code to consolidate stats here ****

    for index in range(len(ret)):
        for key in ret[index]:
            if isinstance(ret[index][key], list):
                if 'aggregated_l2_lan_hello_rx' in key or 'aggregated_l1_lan_hello_rx' in key or 'aggregated_l2_psnp_rx' in key or 'aggregated_l2_csnp_tx' in key or 'aggregated_l1_csnp_rx' in key or 'aggregated_l2_psnp_tx' in key or 'aggregated_l1_csnp_tx' in key or 'aggregated_l1_psnp_rx' in key or 'aggregated_l2_lsp_rx' in key or 'aggregated_l1_lan_hello_tx' in key or 'aggregated_l1_lsp_tx' in key or 'aggregated_l2_lan_hello_tx' in key or 'aggregated_l2_lsp_tx' in key:
                    ret[index][key] = sum(list(map(int, ret[index][key])))

    # **** Add code to consolidate stats here ****

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_lacp_config(
        rt_handle,
        handle=jNone,
        mode=jNone,
        protocol=jNone,
        actor_key=jNone,
        actor_key_step=jNone,
        actor_port_priority=jNone,
        actor_port_priority_step=jNone,
        actor_port_number=jNone,
        actor_port_number_step=jNone,
        lacp_timeout=jNone,
        lacp_activity=jNone,
        actor_system_id=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <create|delete|modify|enable|disable>
    :param protocol - <lacp>
    :param actor_key - <0-65535>
    :param actor_key_step - <0-65535>
    :param actor_port_priority - <0-65535>
    :param actor_port_priority_step - <0-65535>
    :param actor_port_number - <0-65535>
    :param actor_port_number_step - <0-65535>
    :param lacp_timeout - <long|short>
    :param lacp_activity - <active|passive>
    :param actor_system_id
    :param port_handle

    Spirent Returns:

    IXIA Returns:
    {
        "handle": "/topology:1/deviceGroup:1/ethernet:1/lacp:1/item:1",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/lacp:1/item:1",
        "lacp_handle": "/topology:1/deviceGroup:1/ethernet:1/lacp:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args['protocol'] = protocol
    args['actor_key'] = actor_key
    args['actor_key_step'] = actor_key_step
    args['actor_port_priority'] = actor_port_priority
    args['actor_port_priority_step'] = actor_port_priority_step
    args['actor_port_number'] = actor_port_number
    args['actor_port_number_step'] = actor_port_number_step
    args['lacp_timeout'] = lacp_timeout
    args['lacp_activity'] = lacp_activity
    args['actor_system_id'] = actor_system_id
    args['port_handle'] = port_handle
    args['lag_handle'] = handle
    
    args = get_arg_value(rt_handle, j_emulation_lacp_config.__doc__, **args)

    if 'actor_key' in args:
        args['lacp_actor_key'] = args['actor_key']
        del args['actor_key']
    if 'actor_key_step' in args:
        args['lacp_actor_key_step'] = args['actor_key_step']
        del args['actor_key_step']
    if 'actor_port_priority' in args:
        args['lacp_actor_port_priority'] = args['actor_port_priority']
        del args['actor_port_priority']
    if 'actor_port_priority_step' in args:
        args['lacp_actor_port_priority_step'] = args['actor_port_priority_step']
        del args['actor_port_priority_step']
    if 'actor_port_number' in args:
        args['lacp_actor_port_number'] = args['actor_port_number']
        del args['actor_port_number']
    if 'actor_port_number_step' in args:
        args['lacp_actor_port_step'] = args['actor_port_number_step']
        del args['actor_port_number_step']
    handles = jNone
    if 'lag_handle' not in args and 'port_handle' not in args:
        raise RuntimeError('Either handle or port_handle argument must be passed to j_emulation_lacp_config')
    elif handle == jNone:
        handles = port_handle
    elif port_handle == jNone:
        handles = handle

    if not isinstance(handles, list):
        handles = [handles]
    handles = list(set(handles))

    ret = []
    for hndl in handles:
        if mode == 'create':
            args['port_handle'] = hndl
            handle_map[hndl] = handle_map.get(hndl, [])
        else:
            args['lag_handle'] = hndl
        ret.append(rt_handle.invoke('emulation_lag_config', **args))
        if mode == "create":
            handle_map[args['port_handle']].append(ret[-1]['lag_handle'])
            handle_map[ret[-1]['lag_handle']] = args['port_handle']


    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'lag_handle' in ret[index]:
            ret[index]['handles'] = ret[index]['lag_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_lacp_control(
        rt_handle,
        action=jNone,
        handle=jNone):
    """
    :param rt_handle:       RT object
    :param action - <start|stop>
    :param handle

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['port_handle'] = handle

    args = get_arg_value(rt_handle, j_emulation_lacp_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['port_handle'] = __get_handle(hndl)
        ret.append(rt_handle.invoke('emulation_lacp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_lacp_info(
        rt_handle,
        handle=jNone,
        mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode

    Spirent Returns:
    {
        "actor_operational_key": "1",
        "actor_port": "1",
        "actor_state": "61",
        "actor_systemid": "00:11:01:00:00:01",
        "aggregate": {
            "actor_operational_key": "1",
            "actor_port": "1",
            "actor_state": "61",
            "actor_systemid": "00:11:01:00:00:01",
            "lacp_state": "UP",
            "marker_pdus_rx": "0",
            "marker_pdus_tx": "0",
            "marker_response_pdus_rx": "0",
            "marker_response_pdus_tx": "0",
            "partner_collector_max_delay": "50000",
            "partner_operational_key": "1",
            "partner_port": "1",
            "partner_port_priority": "1",
            "partner_state": "61",
            "partner_system_id": "00:11:02:00:00:01",
            "partner_system_priority": "1",
            "pdus_rx": "4",
            "pdus_tx": "4",
            "status": "1"
        },
        "lacp_state": "UP",
        "marker_pdus_rx": "0",
        "marker_pdus_tx": "0",
        "marker_response_pdus_rx": "0",
        "marker_response_pdus_tx": "0",
        "partner_collector_max_delay": "50000",
        "partner_operational_key": "1",
        "partner_port": "1",
        "partner_port_priority": "1",
        "partner_state": "61",
        "partner_system_id": "00:11:02:00:00:01",
        "partner_system_priority": "1",
        "pdus_rx": "4",
        "pdus_tx": "4",
        "status": "1"
    },

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/lacp:1/item:1": {
            "aggregate": {
                "actor_key": "1",
                "actor_port_number": "1",
                "actor_system_id": "00 11 01 00 00 01"
            }
        },
        "Device Group 1": {
            "aggregate": {
                "device_group": "Device Group 1",
                "lacpdu_rx": "5",
                "lacpdu_tx": "5",
                "lacpdu_tx_rate_violation_count": "0",
                "lacpu_malformed_rx": "0",
                "lag_member_ports_up": "1",
                "marker_pdu_rx": "0",
                "marker_pdu_tx": "0",
                "marker_pdu_tx_rate_violation_count": "0",
                "marker_res_pdu_rx": "0",
                "marker_res_pdu_tx": "0",
                "marker_res_timeout_count": "0",
                "sessions_down": "0",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "total_lag_member_ports": "1"
            }
        },
        "InnerGlobalStats": {
            "aggregate": {
                "total_Number_of_operational_lags": "2",
                "total_number_of_user_defined_lags": "2"
            }
        },
        "[(0001:00-11-01-00-00-01:0001:00:0000):(0001:00-11-02-00-00-01:0001:00:0000)]": {
            "aggregate": {
                "lacpdu_rx": "5",
                "lacpdu_tx": "5",
                "lacpdu_tx_rate_violation_count": "0",
                "lacpu_malformed_rx": "0",
                "lag_id": "[(0001:00-11-01-00-00-01:0001:00:0000):(0001:00-11-02-00-00-01:0001:00:0000)]",
                "lag_member_ports_up": "1",
                "marker_pdu_rx": "0",
                "marker_pdu_tx": "0",
                "marker_pdu_tx_rate_violation_count": "0",
                "marker_res_pdu_rx": "0",
                "marker_res_pdu_tx": "0",
                "marker_res_timeout_count": "0",
                "session_flap_count": "0",
                "total_lag_member_ports": "1"
            }
        },
        "[(0001:00-11-02-00-00-01:0001:00:0000):(0001:00-11-01-00-00-01:0001:00:0000)]": {
            "aggregate": {
                "lacpdu_rx": "5",
                "lacpdu_tx": "5",
                "lacpdu_tx_rate_violation_count": "0",
                "lacpu_malformed_rx": "0",
                "lag_id": "[(0001:00-11-02-00-00-01:0001:00:0000):(0001:00-11-01-00-00-01:0001:00:0000)]",
                "lag_member_ports_up": "1",
                "marker_pdu_rx": "0",
                "marker_pdu_tx": "0",
                "marker_pdu_tx_rate_violation_count": "0",
                "marker_res_pdu_rx": "0",
                "marker_res_pdu_tx": "0",
                "marker_res_timeout_count": "0",
                "session_flap_count": "0",
                "total_lag_member_ports": "1"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
        "aggregate"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args['port_handle'] = handle
    args['action'] = 'collect'

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['port_handle'] = __get_handle(hndl)
        stats = dict()
        args['mode'] = 'aggregate'
        stats.update(rt_handle.invoke('emulation_lacp_info', **args))
        args['mode'] = 'state'
        stats.update(rt_handle.invoke('emulation_lacp_info', **args))
        args['mode'] = 'stats'
        stats.update(rt_handle.invoke('emulation_lacp_info', **args))
        ret.append(stats)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        ret[index]['aggregate'] = dict()
        for key in list(ret[index]):
            if key != "aggregate":
                if key == 'marker_pdus_rx':
                    ret[index]['aggregate']['marker_pdu_rx'] = ret[index][key]
                if key == 'marker_pdus_tx':
                    ret[index]['aggregate']['marker_pdu_tx'] = ret[index][key]
                if key == 'marker_response_pdus_rx':
                    ret[index]['aggregate']['marker_res_pdu_rx'] = ret[index][key]
                if key == 'marker_response_pdus_tx':
                    ret[index]['aggregate']['marker_res_pdu_tx'] = ret[index][key]
                if key == 'marker_response_pdus_tx':
                    ret[index]['aggregate']['marker_res_pdu_tx'] = ret[index][key]
                if key == 'pdus_rx':
                    ret[index]['aggregate']['lacpdu_rx'] = ret[index][key]
                if key == 'pdus_tx':
                    ret[index]['aggregate']['lacpdu_tx'] = ret[index][key]
                else:
                    ret[index]['aggregate'][key] = ret[index][key]

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ldp_config(
        rt_handle,
        bfd_registration=jNone,
        count=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        handle=jNone,
        hello_interval=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_length=jNone,
        keepalive_interval=jNone,
        label_adv=jNone,
        loopback_ip_addr=jNone,
        loopback_ip_addr_step=jNone,
        lsr_id=jNone,
        lsr_id_step=jNone,
        reconnect_time=jNone,
        remote_ip_addr=jNone,
        remote_ip_addr_step=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        enable_graceful_restart=jNone,
        graceful_recovery_time=jNone,
        mac_address_init=jNone,
        auth_key=jNone,
        auth_mode=jNone,
        port_handle=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):
    """
    :param rt_handle:       RT object
    :param bfd_registration - <0|1>
    :param count
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param handle
    :param hello_interval - <1-65535>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_length - <1-32>
    :param keepalive_interval - <1-21845>
    :param label_adv - <unsolicited|on_demand>
    :param loopback_ip_addr
    :param loopback_ip_addr_step
    :param lsr_id
    :param lsr_id_step
    :param reconnect_time - <0-300000>
    :param remote_ip_addr
    :param remote_ip_addr_step
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <1-4094>
    :param vlan_user_priority - <0-7>
    :param mode - <create|delete|inactive:disable|active:enable|modify>
    :param enable_graceful_restart - <0|1>
    :param graceful_recovery_time - <0-300000>
    :param mac_address_init
    :param auth_key - <1-255>
    :param auth_mode - <none:null|md5>
    :param port_handle
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <1-4094>
    :param vlan_outer_user_priority - <0-7>
    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpBasicRouter:1/item:1",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpBasicRouter:1",
        "ldp_basic_router_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpBasicRouter:1",
        "ldp_connected_interface_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpConnectedInterface:2",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['bfd_registration'] = bfd_registration
    args['count'] = count
    args['gateway_ip_addr'] = gateway_ip_addr
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['handle'] = handle
    args['hello_interval'] = hello_interval
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_length'] = intf_prefix_length
    args['keepalive_interval'] = keepalive_interval
    args['label_adv'] = label_adv
    args['loopback_ip_addr'] = loopback_ip_addr
    args['loopback_ip_addr_step'] = loopback_ip_addr_step
    args['lsr_id'] = lsr_id
    args['lsr_id_step'] = lsr_id_step
    args['reconnect_time'] = reconnect_time
    args['remote_ip_addr'] = remote_ip_addr
    args['remote_ip_addr_step'] = remote_ip_addr_step
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['enable_graceful_restart'] = enable_graceful_restart
    args['graceful_recovery_time'] = graceful_recovery_time
    args['mac_address_init'] = mac_address_init
    args['md5_key_id'] = auth_key
    args['auth_mode'] = auth_mode
    args['port_handle'] = port_handle
    args['vlan_outer_id'] = vlan_outer_id
    args['vlan_outer_id_mode'] = vlan_outer_id_mode
    args['vlan_outer_id_step'] = vlan_outer_id_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority
   
    args = get_arg_value(rt_handle, j_emulation_ldp_config.__doc__, **args)

    if 'enable_graceful_restart' in args:
        args['graceful_restart'] = args['enable_graceful_restart']
        del args['enable_graceful_restart']
     
    if 'graceful_recovery_time' in args:
        args['graceful_recovery_timer'] = args['graceful_recovery_time']
        del args['graceful_recovery_time']  

    if 'auth_mode' in args:
        args['authentication_mode'] = args['auth_mode']
        del args['auth_mode']
 
    if 'auth_key' in args:
        args['md5_key_id'] = args['auth_key']
        del args['auth_key']

    if port_handle == jNone:
        __check_and_raise(handle)
    elif handle == jNone:
        __check_and_raise(port_handle)

    counter = 1
    string = "ldp_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "ldp_" + str(counter)
    global_config[string] = []
    ret = []
    if 'handle' in args.keys():
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    args['handle'] = hnd
                    result = rt_handle.invoke('emulation_ldp_config', **args)
                    if result.get('handle'):
                        global_config[string].extend([result['handle']])
                        result['handles'] = string
                    if mode == 'enable' or  mode == 'create':
                        handle_map[hnd] = handle_map.get(hnd, [])
                        handle_map[hnd].extend(global_config[string])
                        handle_map[string] = hnd
                    ret.append(result) 
            else:
                args['handle'] = hndl
                result = rt_handle.invoke('emulation_ldp_config', **args)
                if result.get('handle'):
                    global_config[string].extend([result['handle']])
                    result['handles'] = string
                if mode == 'enable' or mode== 'create':
                    handle_map[hndl] = handle_map.get(hndl, [])
                    handle_map[hndl].extend(global_config[string])
                    handle_map[string] = hndl
                ret.append(result)
    elif 'port_handle' in args.keys():
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        result = rt_handle.invoke('emulation_ldp_config', **args)
        if result.get('handle'):
            global_config[string].extend([result['handle']])
            result['handles'] = string
        for hand in port_handle:
            handle_map[hand] = handle_map.get(hand, [])
            handle_map[hand].extend(global_config[string])
            handle_map[string] = hand
        ret.append(result)

    # ***** Return Value Modification *****
    if len(ret) == 1:
        ret = ret[0]
    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ldp_control(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|restart>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    
    args = get_arg_value(rt_handle, j_emulation_ldp_control.__doc__, **args)
  
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                ret.append(rt_handle.invoke('emulation_ldp_control', **args))
        else:
            args['handle'] = hndl
            ret.append(rt_handle.invoke('emulation_ldp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ldp_info(rt_handle, handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle

    Spirent Returns:
    {
        "abort_rx": "0",
        "abort_tx": "0",
        "elapsed_time": "60.0983300209",
        "fec_type": "ipv4_prefix ipv4_prefix",
        "hello_hold_time": "15",
        "hello_interval": "5",
        "intf_ip_addr": "10.10.10.1",
        "ip_address": "10.10.10.1",
        "keepalive_holdtime": "135",
        "keepalive_interval": "45",
        "label": "16 16",
        "label_adv": "unsolicited unsolicited",
        "label_space": "0",
        "linked_hellos_rx": "12",
        "linked_hellos_tx": "12",
        "lsp_pool_handle": "ipv4prefixlsp1",
        "map_rx": "1",
        "map_tx": "1",
        "notif_rx": "0",
        "notif_tx": "0",
        "num_incoming_egress_lsps": "1",
        "num_incoming_ingress_lsps": "1",
        "num_lsps_setup": "1",
        "num_opened_lsps": "1",
        "prefix": "20.20.20.0 20.20.20.0",
        "prefix_length": "24 24",
        "release_rx": "0",
        "release_tx": "0",
        "req_rx": "0",
        "req_tx": "0",
        "session_state": "operational",
        "source": {
            "ldplspresults1": "ldplspresults2"
        },
        "status": "1",
        "targeted_hellos_rx": "0",
        "targeted_hellos_tx": "0",
        "type": "egress egress",
        "withdraw_rx": "0",
        "withdraw_tx": "0"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ldpBasicRouter:1/item:1": {
            "session": {
                "abort_rx": "0",
                "abort_tx": "0",
                "basic_sessions": "0",
                "established_lsp_ingress": "0",
                "initialized_state_count": "0",
                "map_rx": "0",
                "map_tx": "0",
                "non_existent_state_count": "0",
                "notif_rx": "0",
                "notif_tx": "0",
                "open_state_count": "0",
                "operational_state_count": "0",
                "port_name": "1/11/2",
                "pw_status_cleared_rx": "0",
                "pw_status_cleared_tx": "0",
                "pw_status_down": "0",
                "pw_status_notif_rx": "0",
                "pw_status_notif_tx": "0",
                "release_rx": "0",
                "release_tx": "0",
                "req_rx": "0",
                "req_tx": "0",
                "targeted_session_down": "0",
                "withdraw_rx": "0",
                "withdraw_tx": "0"
            }
        },
        "1/11/2": {
            "aggregate": {
                "abort_rx": "0",
                "abort_tx": "0",
                "basic_sessions": "0",
                "established_lsp_ingress": "0",
                "initialized_state_count": "0",
                "map_rx": "0",
                "map_tx": "0",
                "non_existent_state_count": "0",
                "notif_rx": "0",
                "notif_tx": "0",
                "open_state_count": "0",
                "operational_state_count": "0",
                "port_name": "1/11/2",
                "pw_status_cleared_rx": "0",
                "pw_status_cleared_tx": "0",
                "pw_status_down": "0",
                "pw_status_notif_rx": "0",
                "pw_status_notif_tx": "0",
                "release_rx": "0",
                "release_tx": "0",
                "req_rx": "0",
                "req_tx": "0",
                "status": "started",
                "targeted_session_down": "0",
                "withdraw_rx": "0",
                "withdraw_tx": "0"
            }
        },
        "abort_rx": "0",
        "abort_tx": "0",
        "lsp_labels": {
            "fec_type_list": {
                "Fec Type": "ipv4_prefix vc vc"
            },
            "group_id_list": {
                "Group ID": "removePacket[N/A] removePacket[N/A]",
                "Group Id": "N/A"
            },
            "label_list": {
                "Label": "removePacket[N/A] removePacket[N/A] removePacket[N/A]"
            },
            "label_space_id_list": {
                "Label Space ID": "removePacket[N/A]",
                "Label Space Id": "N/A N/A"
            },
            "prefix_length_list": {
                "FEC Prefix Length": "N/A N/A"
            },
            "prefix_list": {
                "FEC": "removePacket[N/A] N/A N/A"
            },
            "source_list": {
                "Peer": "removePacket[N/A] removePacket[N/A] removePacket[N/A]"
            },
            "state_list": {
                "PW State": "N/A N/A",
                "State": "N/A"
            },
            "type_list": {
                "Type": "learned learned learned"
            },
            "vc_id_list": {
                "VC ID": "removePacket[N/A] N/A",
                "Vc Id": "N/A"
            },
            "vc_type_list": {
                "VC Type": "N/A N/A",
                "Vc Type": "N/A"
            },
            "vci_list": {
                "Vci": "N/A N/A N/A"
            },
            "vpi_list": {
                "Vpi": "N/A N/A N/A"
            }
        },
        "map_rx": "0",
        "map_tx": "0",
        "neighbors": {
            "Peer": "removePacket[N/A]"
        },
        "notif_rx": "0",
        "notif_tx": "0",
        "release_rx": "0",
        "release_tx": "0",
        "req_rx": "0",
        "req_tx": "0",
        "settings": {
            "atm_range_max_vci": {
                "atm_range_max_vci": "N/A"
            },
            "atm_range_max_vpi": {
                "atm_range_max_vpi": "N/A"
            },
            "atm_range_min_vci": {
                "atm_range_min_vci": "N/A"
            },
            "atm_range_min_vpi": {
                "atm_range_min_vpi": "N/A"
            },
            "hello_hold_time": {
                "hello_hold_time": "/multivalue:3561"
            },
            "hello_interval": {
                "hello_interval": "/multivalue:3560"
            },
            "hold_time": {
                "hold_time": "/multivalue:3561"
            },
            "intf_ip_addr": {
                "intf_ip_addr": "/multivalue:6"
            },
            "ip_address": {
                "ip_address": "/multivalue:6"
            },
            "keepalive": {
                "keepalive": "/multivalue:3552"
            },
            "keepalive_holdtime": {
                "keepalive_holdtime": "/multivalue:3553"
            },
            "keepalive_interval": {
                "keepalive_interval": "/multivalue:3552"
            },
            "label_adv": {
                "label_adv": "/multivalue:3558"
            },
            "label_space": {
                "label_space": "/multivalue:3559"
            },
            "targeted_hello": {
                "targeted_hello": "N/A"
            },
            "vci": {
                "vci": "N/A"
            },
            "vpi": {
                "vpi": "N/A"
            }
        },
        "status": "1",
        "withdraw_rx": "0",
        "withdraw_tx": "0"
    }

    Common Return Keys:
        "status"
        "abort_rx"
        "abort_tx"
        "map_rx"
        "map_tx"
        "notif_rx"
        "notif_tx"
        "release_rx"
        "release_tx"
        "req_rx"
        "req_tx"
        "withdraw_rx"
        "withdraw_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    
    ret = []
    for hndl in handle:
        status = 1
        new_ret = dict()
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                newer_ret = dict()
                args['mode'] = 'stats'
                newer_ret.update(rt_handle.invoke('emulation_ldp_info', **args))
                args['mode'] = 'settings'
                newer_ret.update(rt_handle.invoke('emulation_ldp_info', **args))
                args['mode'] = 'state'
                newer_ret.update(rt_handle.invoke('emulation_ldp_info', **args))
                args['mode'] = 'lsp_labels'
                newer_ret.update(rt_handle.invoke('emulation_ldp_info', **args))
                if 'status' in newer_ret:
                    if newer_ret['status'] == 0:
                        status = 0
                for key in newer_ret:
                    try:
                        new_ret[key]
                    except:
                        new_ret[key] = []
                    new_ret[key].append(newer_ret[key])
                for key in new_ret:
                    if len(new_ret[key]) == 1:
                        new_ret[key] = new_ret[key][0]
                if 'status' in new_ret:
                    new_ret['status'] = status
                if new_ret:
                    ret.append(new_ret)
        else:
            args['handle'] = hndl
            newer_ret = dict()
            args['mode'] = 'stats'
            newer_ret.update(rt_handle.invoke('emulation_ldp_info', **args))
            args['mode'] = 'settings'
            newer_ret.update(rt_handle.invoke('emulation_ldp_info', **args))
            args['mode'] = 'state'
            newer_ret.update(rt_handle.invoke('emulation_ldp_info', **args))
            args['mode'] = 'lsp_labels'
            newer_ret.update(rt_handle.invoke('emulation_ldp_info', **args))
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
            for key in new_ret:
                if len(new_ret[key]) == 1:
                    new_ret[key] = new_ret[key][0]
            if 'status' in new_ret:
                new_ret['status'] = status
            if new_ret:
                ret.append(new_ret)

    # **** Add code to consolidate stats here ****

    for index in range(len(ret)):
        for key in ret[index]:
            if isinstance(ret[index][key], list):
                if 'num_lsps_setup' in key or 'num_opened_lsps' in key or 'abort_rx' in key or 'release_rx' in key or 'num_incoming_ingress_lsps' in key or 'linked_hellos_rx' in key or 'release_tx' in key or 'label_space' in key or 'targeted_hellos_rx' in key or 'req_rx' in key or 'targeted_hellos_tx' in key or 'req_tx' in key or 'num_incoming_egress_lsps' in key or 'abort_tx' in key or 'max_rx' in key or 'map_tx' in key or 'notif_rx' in key or 'withdraw_tx' in key or 'notif_tx' in key or 'withdraw_rx' in key or 'linked_hellos_tx' in key:
                    ret[index][key] = sum(list(map(int, ret[index][key])))
                elif 'elapsed_time' in key:
                    ret[index][key] = sum(list(map(float, ret[index][key]))) / len(ret[index][key])
                elif 'hello_hold_time'in key or 'hello_interval' in key or 'keepalive_holdtime' in key or 'keepalive_interval' in key:
                    ret[index][key] = sum(list(map(int, ret[index][key]))) // len(ret[index][key])

    # **** Add code to consolidate stats here ****

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ldp_route_config(
        rt_handle,
        fec_ip_prefix_length=jNone,
        fec_ip_prefix_start=jNone,
        fec_vc_cbit=jNone,
        fec_vc_count=jNone,
        fec_vc_group_id=jNone,
        fec_vc_intf_mtu=jNone,
        fec_vc_id_start=jNone,
        fec_vc_id_step=jNone,
        handle=jNone,
        lsp_handle=jNone,
        mode=jNone,
        fec_type=jNone,
        fec_vc_type=jNone,
        num_lsps=jNone,
        egress_label_mode=jNone,
        label_value_start=jNone,
        fec_ip_prefix_step=jNone):
    """
    :param rt_handle:       RT object
    :param fec_ip_prefix_length - <1-32>
    :param fec_ip_prefix_start
    :param fec_vc_cbit - <0|1>
    :param fec_vc_count
    :param fec_vc_group_id
    :param fec_vc_intf_mtu - <0-65535>
    :param fec_vc_id_start - <0-2147483647>
    :param fec_vc_id_step - <0-2147483647>
    :param handle
    :param lsp_handle
    :param mode - <create|modify|delete>
    :param fec_type - <prefix:ipv4_prefix|host_addr|vc>
    :param fec_vc_type - <cem|eth|eth_vlan|eth_vpls|fr_dlci|ppp>
    :param num_lsps - <1-34048>
    :param egress_label_mode - <nextlabel> 
    :param label_value_start - <0-1046400>
    :param fec_ip_prefix_step

    Spirent Returns:
    {
        "handles": "ipv4prefixlsp1",
        "lsp_handle": "ipv4prefixlsp1",
        "status": "1"
    }

    IXIA Returns:
    {
        "fecproperty_handle": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/ldpFECProperty:1",
        "handles": "/topology:1/deviceGroup:1/networkGroup:1",
        "network_group_handle": "/topology:1/deviceGroup:1/networkGroup:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    global global_config
    args = dict()
    n_args = dict()
    args['fec_ip_prefix_length'] = fec_ip_prefix_length
    args['fec_ip_prefix_start'] = fec_ip_prefix_start
    args['fec_vc_cbit'] = fec_vc_cbit
    args['fec_vc_count'] = fec_vc_count
    args['fec_vc_group_id'] = fec_vc_group_id
    args['fec_vc_intf_mtu'] = fec_vc_intf_mtu
    args['fec_vc_id_start'] = fec_vc_id_start
    args['fec_vc_id_step'] = fec_vc_id_step
    args['handle'] = handle
    args['lsp_handle'] = lsp_handle
    args['mode'] = mode
    args['fec_type'] = fec_type
    args['fec_vc_type'] = fec_vc_type
    args['num_lsps'] = num_lsps
    args['fec_ip_prefix_step'] = fec_ip_prefix_step

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    
    args = get_arg_value(rt_handle, j_emulation_ldp_route_config.__doc__, **args)
    n_args['egress_label_mode'] = egress_label_mode
    n_args['label_value_start'] = label_value_start
    n_args = get_arg_value(rt_handle, j_emulation_ldp_route_config.__doc__, **n_args)
    
    if 'label_value_start' in n_args:
        n_args['label_start'] = n_args['label_value_start']
        del n_args['label_value_start'] 
  
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if egress_label_mode != jNone or label_value_start != jNone:
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    n_args['handle'] = hnd
                    n_args['mode'] = 'modify'
                if mode == 'modify':
                    ldp_handle = rt_handle.invoke('invoke', cmd='stc::get '+hnd+' -parent')
                    ldp_handle_1 = rt_handle.invoke('invoke', cmd='stc::get '+ldp_handle+' -parent') 
                    n_args['handle'] = ldp_handle_1
                    n_args['mode'] = mode
                if mode != jNone and mode != 'delete':
                    rt_handle.invoke('emulation_ldp_config', **n_args)
            else:
                n_args['handle'] = hndl
                n_args['mode'] = 'modify'
                if mode == 'modify':
                    ldp_handle = rt_handle.invoke('invoke', cmd='stc::get '+hndl+' -parent')
                    ldp_handle_1 = rt_handle.invoke('invoke', cmd='stc::get '+ldp_handle+' -parent')
                    n_args['handle'] = ldp_handle_1
                    n_args['mode'] = mode
                if mode != jNone and mode != 'delete':
                    rt_handle.invoke('emulation_ldp_config', **n_args)
    counter = 1
    string = "ldp_route_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "ldp_route_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()
    for hndl in handle:
        status = 1
        new_ret = dict()
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                if hnd in handle_list:
                    continue
                else:
                    handle_list[hnd] = 1
                args['handle'] = hnd
                if mode == 'modify' or mode == 'delete':
                    args['lsp_handle'] = hnd
                newer_ret = rt_handle.invoke('emulation_ldp_route_config', **args)
                if 'status' in newer_ret:
                    if newer_ret['status'] == 0:
                        status = 0
                if 'lsp_handle' in newer_ret:
                    global_config[string].extend([newer_ret['lsp_handle']])
                for key in newer_ret:
                    try:
                        new_ret[key]
                    except:
                        new_ret[key] = []
                    new_ret[key].append(newer_ret[key])
            for key in new_ret:
                if len(new_ret[key]) == 1:
                    new_ret[key] = new_ret[key][0]
            if 'status' in new_ret:
                new_ret['status'] = status
            if 'lsp_handle' in new_ret:
                new_ret['handles'] = string
            if new_ret:
                ret.append(new_ret)

        else:
            args['handle'] = hndl
            if mode == 'modify' or mode == 'delete':
                args['lsp_handle'] = hndl
            newer_ret = rt_handle.invoke('emulation_ldp_route_config', **args)
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'lsp_handle' in newer_ret:
                global_config[string].extend([newer_ret['lsp_handle']])
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
            for key in new_ret:
                if len(new_ret[key]) == 1:
                    new_ret[key] = new_ret[key][0]
            if 'status' in new_ret:
                new_ret['status'] = status
            if 'lsp_handle' in new_ret:
                new_ret['handle'] = new_ret['lsp_handle']
                new_ret['handles'] = string
            if new_ret:
                ret.append(new_ret)

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_mld_config(
        rt_handle,
        count=jNone,
        filter_mode=jNone,
        handle=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_len=jNone,
        mld_version=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        port_handle=jNone,
        general_query=jNone,
        ip_router_alert=jNone,
        group_query=jNone,
        active=jNone,
        max_response_time=jNone,
        name=jNone,
        enable_iptv=jNone,
        max_response_control=jNone,
        msg_interval=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_mode=jNone,
        vlan_id_outer_step=jNone,
        vlan_outer_user_priority=jNone):
    """
    :param rt_handle:       RT object
    :param count - <1-4000>
    :param filter_mode - <include|exclude>
    :param handle
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_len - <1-128>
    :param mld_version - <v1|v2>
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4094>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|delete>
    :param port_handle
    :param general_query
    :param ip_router_alert
    :param group_query
    :param active
    :param max_response_time - <0-999999>
    :param name
    :param enable_iptv
    :param max_response_control - <0>
    :param msg_interval - <0-999999999>
    :param vlan_id_outer - <0-4095>
    :param vlan_id_outer_mode - <fixed|increment>
    :param vlan_id_outer_step - <0-4094>
    :param vlan_outer_user_priority - <0-7>

    Spirent Returns:
    {
        "handle": "mldhostconfig1",
        "handles": "mldhostconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1",
        "mld_host_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1",
        "mld_host_iptv_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/iptv",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['count'] = count
    args['filter_mode'] = filter_mode
    args['handle'] = handle
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_len'] = intf_prefix_len
    args['mld_version'] = mld_version
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['neighbor_intf_ip_addr_step'] = neighbor_intf_ip_addr_step
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['port_handle'] = port_handle
    args['general_query'] = general_query
    args['ip_router_alert'] = ip_router_alert
    args['group_query'] = group_query
    args['max_response_control'] = max_response_control
    args['msg_interval'] = msg_interval
    args['vlan_id_outer'] = vlan_id_outer
    args['vlan_id_outer_mode'] = vlan_id_outer_mode
    args['vlan_id_outer_step'] = vlan_id_outer_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority

    args = get_arg_value(rt_handle, j_emulation_mld_config.__doc__, **args)

    if port_handle == jNone:
        __check_and_raise(handle)
    elif handle == jNone:
        __check_and_raise(port_handle)

    counter = 1
    string = "mld_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "mld_" + str(counter)
    global_config[string] = []
    ret = []
    if 'handle' in args.keys():
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                ret.append(invoke_handle(rt_handle, protocol_string=string, **args))
                break
            else:
                args['handle'] = hndl
                result = rt_handle.invoke('emulation_mld_config', **args)
                if result.get('handle'):
                    global_config[string].extend([result['handle']])
                    result['handles'] = string
                if mode == 'create':
                    handle_map[hndl] = handle_map.get(hndl, [])
                    handle_map[hndl].extend(global_config[string])
                    handle_map[string] = hndl
                ret.append(result)

    elif 'port_handle' in args.keys():
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        result = rt_handle.invoke('emulation_mld_config', **args)
        if result.get('handle'):
            global_config[string].extend([result['handle']])
            result['handles'] = string
        for hand in port_handle:
            handle_map[hand] = handle_map.get(hand, [])
            handle_map[hand].extend(global_config[string])
            handle_map[string] = hand
        ret.append(result)

    # ***** Executing Native otions *****
    for index in range(len(ret)):
        if 'handle' in ret[index]:
            myHandle = ret[index]['handle']
        else:
            continue
        if not isinstance(myHandle, list):
            myHandle = [myHandle]
        myHandle = list(set(myHandle))
        for hand in myHandle:
            if mode != 'delete':
                if active != jNone:
                    if int(active) == 1:
                        rt_handle.invoke('invoke', cmd='stc::config' + " " +  hand  + ' -active' + ' true')
                    if int(active) == 0:
                        rt_handle.invoke('invoke', cmd='stc::config' + " " +  hand  + ' -active' + ' false')
                        rt_handle.invoke('invoke', cmd='stc::apply')
                if name != jNone:
                    rt_handle.invoke('invoke', cmd='stc::config' + " " +  hand  + ' -name' + " " + name)
                    rt_handle.invoke('invoke', cmd='stc::apply')
                if max_response_time != jNone:
                    mld_router1 = rt_handle.invoke('invoke', cmd='stc::get' + " " +  hand  + ' -parent')
                    rt_handle.invoke('invoke', cmd='stc::create' + " " +  'mldrouterconfig -under' + " " + mld_router1 + ' -QueryResponseInterval' + " " + max_response_time)
                    rt_handle.invoke('invoke', cmd='stc::apply')

            if enable_iptv != jNone:
                n_args = dict()
                if int(enable_iptv) == 1:
                    n_args['handle'] = hand 
                    n_args['mode'] = 'enable'
                    rt_handle.invoke('emulation_iptv_config', **n_args)
                if int(enable_iptv) == 0:
                    n_args['handle'] = hand 
                    n_args['mode'] = 'disable'
                    rt_handle.invoke('emulation_iptv_config', **n_args)

    # **** End of Native Arguemnts *****






    # ***** Return Value Modification *****


    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_mld_control(
        rt_handle,
        group_member_handle=jNone,
        handle=jNone,
        mode=jNone):
    """
    :param rt_handle:       RT object
    :param group_member_handle
    :param handle
    :param mode - <join:start|leave:stop|leave_join:restart>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['group_member_handle'] = group_member_handle
    args['handle'] = handle
   
    if mode == 'start':
        args['mode'] = 'join'
    elif mode == 'stop':
        args['mode'] = 'leave'
    elif mode == 'restart':
        args['mode'] = 'leave_join'

    #args = get_arg_value(rt_handle, j_emulation_mld_control.__doc__, **args)

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                ret.append(rt_handle.invoke('emulation_mld_control', **args))
        else:
            args['handle'] = hndl
            ret.append(rt_handle.invoke('emulation_mld_control', **args))


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_mld_group_config(
        rt_handle,
        group_pool_handle=jNone,
        handle=jNone,
        mode=jNone,
        session_handle=jNone,
        source_pool_handle=jNone):
    """
    :param rt_handle:       RT object
    :param group_pool_handle
    :param handle
    :param mode - <create|modify|delete>
    :param session_handle
    :param source_pool_handle

    Spirent Returns:
    {
        "group_handles": "ipv6group1",
        "handle": "mldgroupmembership1",
        "status": "1"
    }

    IXIA Returns:
    {
        "group_handles": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList",
        "mld_group_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList",
        "mld_source_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList/mldUcastIPv6SourceList",
        "source_handles": "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList/mldUcastIPv6SourceList",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "group_handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['group_pool_handle'] = group_pool_handle
    args['mode'] = mode
    args['session_handle'] = session_handle
    args['source_pool_handle'] = source_pool_handle

    args = get_arg_value(rt_handle, j_emulation_mld_group_config.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    counter = 1
    string = "mld_group_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "mld_group_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()
    for hndl in handle:
        status = 1
        new_ret = dict()
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                if hnd in handle_list:
                    continue
                else:
                    handle_list[hnd] = 1
                args['handle'] = hnd
                if mode == 'create':
                    args['session_handle'] = hnd
                newer_ret = rt_handle.invoke('emulation_mld_group_config', **args)
                if 'status' in newer_ret:
                    if newer_ret['status'] == 0:
                        status = 0
                if 'handle' in newer_ret:
                    global_config[string].extend([newer_ret['handle']])
                for key in newer_ret:
                    try:
                        new_ret[key]
                    except:
                        new_ret[key] = []
                    new_ret[key].append(newer_ret[key])
            for key in new_ret:
                if len(new_ret[key]) == 1:
                    new_ret[key] = new_ret[key][0]
            if 'status' in new_ret:
                new_ret['status'] = status
            if 'handles' in new_ret:
                new_ret['handle'] = new_ret['handles']
            new_ret['handles'] = string
            if new_ret:
                ret.append(new_ret)

        else:
            args['handle'] = hndl
            if mode == 'create':
                args['session_handle'] = hndl
            newer_ret = rt_handle.invoke('emulation_mld_group_config', **args)
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'handle' in newer_ret:
                global_config[string].extend([newer_ret['handle']])
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
            for key in new_ret:
                if len(new_ret[key]) == 1:
                    new_ret[key] = new_ret[key][0]
            if 'status' in new_ret:
                new_ret['status'] = status
            if 'handles' in new_ret:
                new_ret['handle'] = new_ret['handles']
            new_ret['handles'] = string
            if new_ret:
                ret.append(new_ret)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'group_pool_handle' in args:
            ret[index]['group_handles'] = args['group_pool_handle']
        if 'source_pool_handle' in args:
            ret[index]['source_handles'] = args['source_pool_handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_mld_info(rt_handle, handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle

    Spirent Returns:
    {
        "group_membership_stats": {
            "group_addr": {
                "ff00::1111": {
                    "host_addr": {
                        "fe80::1": {
                            "join_latency": "0",
                            "leave_latency": "0",
                            "state": "IDLE_MEMBER"
                        }
                    }
                }
            }
        },
        "session": {
            "mldhostconfig1": {
                "avg_join_latency": "0",
                "avg_leave_latency": "0",
                "max_join_latency": "0",
                "max_leave_latency": "0",
                "min_join_latency": "0",
                "min_leave_latency": "0"
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "/topology:2/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/item:1": {
            "session": {
                "invalid_packets_rx": "0",
                "joined_groups": "0",
                "total_frames_rx": "0",
                "total_frames_tx": "0",
                "v1_done_rx": "0",
                "v1_done_tx": "0",
                "v1_general_queries_rx": "0",
                "v1_general_queries_tx": "0",
                "v1_group_specific_queries_rx": "0",
                "v1_group_specific_queries_tx": "0",
                "v1_membership_reports_rx": "0",
                "v1_membership_reports_tx": "0",
                "v2_allow_new_sources_rx": "0",
                "v2_allow_new_sources_tx": "0",
                "v2_block_old_sources_rx": "0",
                "v2_block_old_sources_tx": "0",
                "v2_change_to_exclude_rx": "0",
                "v2_change_to_exclude_tx": "0",
                "v2_change_to_include_rx": "0",
                "v2_change_to_include_tx": "0",
                "v2_general_queries_rx": "0",
                "v2_general_queries_tx": "0",
                "v2_group_specific_queries_rx": "0",
                "v2_group_specific_queries_tx": "0",
                "v2_membership_reports_rx": "0",
                "v2_membership_reports_tx": "0",
                "v2_mode_is_exclude_rx": "0",
                "v2_mode_is_exclude_tx": "0",
                "v2_mode_is_include_rx": "0",
                "v2_mode_is_include_tx": "0"
            }
        },
        "Device Group 2": {
            "aggregate": {
                "invalid_packets_rx": "0",
                "joined_groups": "0",
                "sessions_down": "1",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "0",
                "status": "started",
                "total_frames_rx": "0",
                "total_frames_tx": "0",
                "v1_done_rx": "0",
                "v1_done_tx": "0",
                "v1_general_queries_rx": "0",
                "v1_general_queries_tx": "0",
                "v1_group_specific_queries_rx": "0",
                "v1_group_specific_queries_tx": "0",
                "v1_membership_reports_rx": "0",
                "v1_membership_reports_tx": "0",
                "v2_allow_new_sources_rx": "0",
                "v2_allow_new_sources_tx": "0",
                "v2_block_old_sources_rx": "0",
                "v2_block_old_sources_tx": "0",
                "v2_change_to_exclude_rx": "0",
                "v2_change_to_exclude_tx": "0",
                "v2_change_to_include_rx": "0",
                "v2_change_to_include_tx": "0",
                "v2_general_queries_rx": "0",
                "v2_general_queries_tx": "0",
                "v2_group_and_source_specific_queries_rx": "0",
                "v2_group_and_source_specific_queries_tx": "0",
                "v2_group_specific_queries_rx": "0",
                "v2_group_specific_queries_tx": "0",
                "v2_membership_reports_rx": "0",
                "v2_membership_reports_tx": "0",
                "v2_mode_is_exclude_rx": "0",
                "v2_mode_is_exclude_tx": "0",
                "v2_mode_is_include_rx": "0",
                "v2_mode_is_include_tx": "0"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        stats = dict()
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                stats.update(__process_mld_info(rt_handle, **args))
                ret.append(stats)
        else:
            args['handle'] = hndl
            stats.update(__process_mld_info(rt_handle, **args))
            ret.append(stats)

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_multicast_group_config(
        rt_handle,
        handle=jNone,
        num_groups=jNone,
        mode=jNone,
        ip_addr_start=jNone,
        ip_addr_step=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param num_groups - <1-65535>
    :param mode - <create|modify|delete>
    :param ip_addr_start
    :param ip_addr_step

    Spirent Returns:
    {
        "handle": "ipv4group1",
        "handles": "ipv4group1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/igmpMcastIPv4GroupList:HLAPI0",
        "handles": "/igmpMcastIPv4GroupList:HLAPI0",
        "multicast_group_handle": "/igmpMcastIPv4GroupList:HLAPI0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['num_groups'] = num_groups
    args['mode'] = mode
    args['ip_addr_start'] = ip_addr_start
    args['handle'] = handle
    args['ip_addr_step'] = ip_addr_step

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_multicast_group_config.__doc__, **args)
 
    ret = []
    if mode == 'modify' or mode == 'delete':
        args['handle'] = handle
    elif mode == 'create' and 'handle' in args:
        del args['handle']
    ret.append(rt_handle.invoke('emulation_multicast_group_config', **args))
    if 'handle' in ret[-1]:
        pim_map[ret[-1]['handle']] = ip_addr_start

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'handle' in ret[index]:
            ret[index]['handles'] = ret[index]['handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_multicast_source_config(
        rt_handle,
        handle=jNone,
        num_sources=jNone,
        mode=jNone,
        ip_addr_start=jNone,
        ip_addr_step=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param num_sources - <1-65535>
    :param mode - <create|modify|delete>
    :param ip_addr_start
    :param ip_addr_step

    Spirent Returns:
    {
        "handle": "multicastSourcePool(0)",
        "handles": "multicastSourcePool(0)",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/igmpUcastIPv4SourceList:HLAPI0",
        "handles": "/igmpUcastIPv4SourceList:HLAPI0",
        "multicast_source_handle": "/igmpUcastIPv4SourceList:HLAPI0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['num_sources'] = num_sources
    args['mode'] = mode
    args['ip_addr_start'] = ip_addr_start
    args['handle'] = handle
    args['ip_addr_step'] = ip_addr_step

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_multicast_source_config.__doc__, **args) 

    ret = []
    if mode == 'modify' or mode == 'delete':
        args['handle'] = handle
    elif mode == 'create' and 'handle' in args:
        del args['handle']
    ret.append(rt_handle.invoke('emulation_multicast_source_config',**args))
    if 'handle' in ret[-1]:
        pim_map[ret[-1]['handle']] = ip_addr_start

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'handle' in ret[index]:
            ret[index]['handles'] = ret[index]['handle']

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ospf_config(
        rt_handle,
        area_id=jNone,
        area_id_step=jNone,
        bfd_registration=jNone,
        count=jNone,
        dead_interval=jNone,
        demand_circuit=jNone,
        graceful_restart_enable=jNone,
        handle=jNone,
        hello_interval=jNone,
        interface_cost=jNone,
        intf_prefix_length=jNone,
        md5_key_id=jNone,
        option_bits=jNone,
        router_id=jNone,
        router_priority=jNone,
        session_type=jNone,
        te_max_bw=jNone,
        te_max_resv_bw=jNone,
        te_metric=jNone,
        te_unresv_bw_priority0=jNone,
        te_unresv_bw_priority1=jNone,
        te_unresv_bw_priority2=jNone,
        te_unresv_bw_priority3=jNone,
        te_unresv_bw_priority4=jNone,
        te_unresv_bw_priority5=jNone,
        te_unresv_bw_priority6=jNone,
        te_unresv_bw_priority7=jNone,
        vci=jNone,
        vci_step=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        vpi=jNone,
        vpi_step=jNone,
        mac_address_start=jNone,
        port_handle=jNone,
        network_type=jNone,
        mode=jNone,
        intf_ip_addr=jNone,
        gateway_ip_addr=jNone,
        authentication_mode=jNone,
        te_admin_group=jNone,
        intf_ip_addr_step=jNone,
        gateway_ip_addr_step=jNone,
        password=jNone,
        mtu=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):
    """
    :param rt_handle:       RT object
    :param area_id
    :param area_id_step
    :param bfd_registration
    :param count - <1-100>
    :param dead_interval - <1-65535>
    :param demand_circuit
    :param graceful_restart_enable
    :param handle
    :param hello_interval - <1-65535>
    :param interface_cost - <1-65535>
    :param intf_prefix_length - <1-128>
    :param md5_key_id - <1-255>
    :param option_bits
    :param router_id
    :param router_priority - <0-255>
    :param session_type - <ospfv2|ospfv3>
    :param te_max_bw
    :param te_max_resv_bw
    :param te_metric
    :param te_unresv_bw_priority7
    :param vci - <0-65535>
    :param vci_step - <0-65535>
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4095>
    :param vlan_user_priority - <0-7>
    :param vpi
    :param vpi_step
    :param mac_address_start
    :param port_handle
    :param network_type - <broadcast|ptop|native:ptomp>
    :param mode - <create|delete|modify|active:enable|inactive:disable>
    :param intf_ip_addr
    :param gateway_ip_addr
    :param authentication_mode - <none:null|simple|md5>
    :param te_admin_group
    :param intf_ip_addr_step
    :param gateway_ip_addr_step
    :param password
    :param mtu - <68-9216>
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <0-4095>
    :param vlan_outer_user_priority - <0-7>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "session_router": "ospfv2routerconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1",
        "ospfv2_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1",
        "status": "1"
    }

    Common Return Keys:
        "handles"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['area_id'] = area_id
    args['area_id_step'] = area_id_step
    args['bfd_registration'] = bfd_registration
    args['count'] = count
    args['dead_interval'] = dead_interval
    args['demand_circuit'] = demand_circuit
    args['graceful_restart_enable'] = graceful_restart_enable
    args['handle'] = handle
    args['hello_interval'] = hello_interval
    args['interface_cost'] = interface_cost
    args['intf_prefix_length'] = intf_prefix_length
    args['md5_key_id'] = md5_key_id
    args['option_bits'] = option_bits
    args['router_id'] = router_id
    args['router_priority'] = router_priority
    args['session_type'] = session_type
    args['te_max_bw'] = te_max_bw
    args['te_max_resv_bw'] = te_max_resv_bw
    args['te_metric'] = te_metric
    args['te_unresv_bw_priority0'] = te_unresv_bw_priority0
    args['te_unresv_bw_priority1'] = te_unresv_bw_priority1
    args['te_unresv_bw_priority2'] = te_unresv_bw_priority2
    args['te_unresv_bw_priority3'] = te_unresv_bw_priority3
    args['te_unresv_bw_priority4'] = te_unresv_bw_priority4
    args['te_unresv_bw_priority5'] = te_unresv_bw_priority5
    args['te_unresv_bw_priority6'] = te_unresv_bw_priority6
    args['te_unresv_bw_priority7'] = te_unresv_bw_priority7
    args['vci'] = vci
    args['vci_step'] = vci_step
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['vpi'] = vpi
    args['vpi_step'] = vpi_step
    args['mac_address_start'] = mac_address_start
    args['port_handle'] = port_handle
    if network_type in ['ptomp', 'native']:
        args['network_type'] = 'native'
    else:
        args['network_type'] = network_type
    args['mode'] = mode
    args['intf_ip_addr'] = intf_ip_addr
    args['gateway_ip_addr'] = gateway_ip_addr
    args['authentication_mode'] = authentication_mode
    args['te_admin_group'] = te_admin_group
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['password'] = password
    args['vlan_outer_id'] = vlan_outer_id
    args['vlan_outer_id_mode'] = vlan_outer_id_mode
    args['vlan_outer_id_step'] = vlan_outer_id_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['neighbor_intf_ip_addr_step'] = neighbor_intf_ip_addr_step

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ospf_config.__doc__, **args)

    if 'neighbor_intf_ip_addr' in args:
        args['gateway_ip_addr'] = args['neighbor_intf_ip_addr']
        del args['neighbor_intf_ip_addr']
    if 'neighbor_intf_ip_addr_step' in args:
        args['gateway_ip_addr_step'] = args['neighbor_intf_ip_addr_step']
        del args['neighbor_intf_ip_addr_step']

    if port_handle == jNone:
        __check_and_raise(handle)

    if 'handle' in args and not isinstance(handle, list):
        handle = [handle]
        handle = list(set(handle))

    counter = 1
    string = "ospf_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "ospf_" + str(counter)
    global_config[string] = []
    ret = []
    if handle != jNone:
        ret.append(invoke_handle(rt_handle, protocol_string=string, **args))
        if mode == 'create':
            for hndl in handle:
                port_handle = __get_handle(hndl)
                handle_map[port_handle].extend(global_config[string])
                handle_map[port_handle] = list(set(handle_map[port_handle]))
                handle_map[string] = port_handle
    elif port_handle != jNone:
        result = rt_handle.invoke('emulation_ospf_config', **args)
        if result.get('handle'):
            #result['handle'] = result['handle'].split(' ')
            global_config[string].extend(result['handle'].split(' '))
            result['handles'] = string
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        if mode == 'create':
            for hand in port_handle:
                handle_map[hand] = handle_map.get(hand, [])
                handle_map[hand].extend(global_config[string])
                handle_map[hand] = list(set(handle_map[hand]))
                handle_map[string] = hand
        ret.append(result)

    # ***** Return Value Modification *****

    for index in range(len(ret)):
        if 'handles' in ret[index]:
            session_map[ret[index]['handles']] = session_type
    #########Native args Execution Start ######
    if mtu != jNone:
        ports_list = rt_handle.invoke('invoke', cmd='stc::get' + " " + 'project1 -children-port').split(" ")
        for portss in range(len(ports_list)):
            phy_handle = rt_handle.invoke('invoke', cmd='stc::get' + " " +  ports_list[portss] + ' -ActivePhy-Targets')
            rt_handle.invoke('invoke', cmd='stc::config' + " " + phy_handle + ' -mtu ' + mtu)
            rt_handle.invoke('invoke', cmd='stc::apply')
    ##########Native args execution Ends ####

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ospf_control(rt_handle, handle=jNone,
                             port_handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle
    :param mode - <start|stop|restart|stop_hellos:stop_hello|resume_hellos:resume_hello|advertise>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['port_handle'] = port_handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ospf_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        hnd = " ".join(global_config[hndl])
        args['handle'] = hnd
        ret.append(rt_handle.invoke('emulation_ospf_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ospf_network_group_config(rt_handle):
    """
    :param rt_handle:       RT object
    :return response from rt_handle.invoke(<parameters>)

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    ret = rt_handle.invoke('emulation_ospf_network_group_config', **args)

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ospf_topology_route_config(
        rt_handle,
        elem_handle=jNone,
        external_number_of_prefix=jNone,
        external_prefix_length=jNone,
        external_prefix_metric=jNone,
        external_prefix_step=jNone,
        external_prefix_type=jNone,
        grid_col=jNone,
        grid_row=jNone,
        summary_number_of_prefix=jNone,
        summary_prefix_length=jNone,
        summary_prefix_metric=jNone,
        type=jNone,
        mode=jNone,
        summary_prefix_start=jNone,
        handle=jNone,
        summary_prefix_step=jNone,
        router_abr=jNone,
        router_asbr=jNone,
        grid_router_id=jNone,
        grid_router_id_step=jNone,
        external_prefix_start=jNone,
        nssa_prefix_start=jNone,
        nssa_prefix_step=jNone,
        nssa_prefix_length=jNone,
        nssa_number_of_prefix=jNone,
        nssa_prefix_metric=jNone,
        grid_prefix_start=jNone,
        grid_prefix_step=jNone,
        grid_prefix_length=jNone,
        link_te_max_bw=jNone,
        link_te_max_resv_bw=jNone,
        link_te_metric=jNone,
        link_te_unresv_bw_priority0=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_length=jNone,
        router_id=jNone,
        router_id_step=jNone):

    """
    :param rt_handle:       RT object
    :param elem_handle
    :param external_number_of_prefix - <1-65535>
    :param external_prefix_length - <1-128>
    :param external_prefix_metric - <1-16777215>
    :param external_prefix_step
    :param external_prefix_type - <1-2>
    :param grid_col - <1-10000>
    :param grid_row - <1-10000>
    :param summary_number_of_prefix - <1-16000000>
    :param summary_prefix_length - <1-128>
    :param summary_prefix_metric - <1-16777215>
    :param type - <grid|summary_routes|ext_routes|nssa_routes>
    :param mode - <create|modify|delete>
    :param summary_prefix_start
    :param handle
    :param summary_prefix_step
    :param router_abr
    :param router_asbr
    :param grid_router_id
    :param grid_router_id_step
    :param external_prefix_start
    :param nssa_prefix_start
    :param nssa_prefix_step
    :param nssa_prefix_length - <1-128>
    :param nssa_number_of_prefix - <1-128>
    :param nssa_prefix_metric - <1-16777215>
    :param grid_prefix_start
    :param grid_prefix_step
    :param grid_prefix_length - <1-128>
    :param link_te_max_bw
    :param link_te_max_resv_bw
    :param link_te_metric - <0-65535>
    :param link_te_unresv_bw_priority0
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_length - <1-128>
    :param router_id
    :param router_id_step

    Spirent Returns:
    {
        "elem_handle": "summarylsablock1",
        "handles": "summarylsablock1",
        "status": "1",
        "summary": {
            "connected_routers": "routerlsa1",
            "summary_lsas": "summarylsablock1",
            "version": "ospfv2"
        }
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/networkGroup:1",
        "ipv4_prefix_interface_handle": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/ospfRouteProperty:1",
        "ipv4_prefix_pools_handle": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1",
        "network_group_handle": "/topology:1/deviceGroup:1/networkGroup:1",
        "status": "1"
    }


    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['elem_handle'] = elem_handle
    args['external_number_of_prefix'] = external_number_of_prefix
    args['external_prefix_length'] = external_prefix_length
    args['external_prefix_metric'] = external_prefix_metric
    args['external_prefix_step'] = external_prefix_step
    args['external_prefix_type'] = external_prefix_type
    args['grid_col'] = grid_col
    args['grid_row'] = grid_row
    args['summary_number_of_prefix'] = summary_number_of_prefix
    args['summary_prefix_length'] = summary_prefix_length
    args['summary_prefix_metric'] = summary_prefix_metric
    args['type'] = type
    args['mode'] = mode
    args['summary_prefix_start'] = summary_prefix_start
    args['handle'] = handle
    args['summary_prefix_step'] = summary_prefix_step
    args['router_abr'] = router_abr
    args['router_asbr'] = router_asbr
    args['grid_router_id'] = grid_router_id
    args['grid_router_id_step'] = grid_router_id_step
    args['external_prefix_start'] = external_prefix_start
    args['nssa_prefix_start'] = nssa_prefix_start
    args['nssa_prefix_step'] = nssa_prefix_step
    args['nssa_prefix_length'] = nssa_prefix_length
    args['nssa_number_of_prefix'] = nssa_number_of_prefix
    args['nssa_prefix_metric'] = nssa_prefix_metric
    args['grid_prefix_start'] = grid_prefix_start
    args['grid_prefix_step'] = grid_prefix_step
    args['grid_prefix_length'] = grid_prefix_length
    args['router_id'] = router_id

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ospf_topology_route_config.__doc__, **args)
    __check_and_raise(handle)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    counter = 1
    string = "ospf_route_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "ospf_route_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()

    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            if hnd in handle_list:
                continue
            else:
                handle_list[hnd] = 1
            args['handle'] = hnd
            ospf_iproute_parent = rt_handle.invoke('invoke', cmd='stc::get  '+hnd+' -children-ospfv3routerconfig')
            if 'handle' in args and ospf_iproute_parent.startswith('ospfv3routerconfig') and mode == 'create':
                args['handle'] = ospf_iproute_parent
            if mode == 'modify' or mode == 'delete':
                args['elem_handle'] = hnd
                ospf_iproute_parent = rt_handle.invoke('invoke', cmd='stc::get' + " " + hnd  + ' -parent')
                ospf_route_parent = rt_handle.invoke('invoke', cmd='stc::get' + " " + ospf_iproute_parent  + ' -parent')
                args['handle'] = ospf_route_parent
            newer_ret = rt_handle.invoke('emulation_ospf_topology_route_config', **args)
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'elem_handle' in newer_ret:
                global_config[string].extend([newer_ret['elem_handle']])
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if 'elem_handle' in new_ret:
            new_ret['handles'] = string
        if new_ret:
            ret.append(new_ret)

    n_args = dict()
    n_args['te_max_bw'] = link_te_max_bw
    n_args['te_max_resv_bw'] = link_te_max_resv_bw
    n_args['te_metric'] = link_te_metric
    n_args['te_unresv_bw_priority0'] = link_te_unresv_bw_priority0
    n_args['intf_ip_addr'] = intf_ip_addr
    n_args['intf_ip_addr_step'] = intf_ip_addr_step
    n_args['intf_prefix_length'] = intf_prefix_length
    n_args['router_id_step'] = router_id_step
    for key in list(n_args.keys()):
        if n_args[key] == jNone:
            del n_args[key]

    if  link_te_max_bw != jNone or  link_te_max_resv_bw != jNone  or link_te_metric != jNone  or link_te_unresv_bw_priority0 != jNone  or intf_ip_addr != jNone  or  intf_ip_addr_step != jNone  or  intf_prefix_length != jNone  or  router_id_step != jNone:
        n_args['handle'] = hnd
        n_args['mode'] = 'modify'
        rt_handle.invoke('emulation_ospf_config', **n_args)
    # ***** Return Value Modification *****


    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ospf_lsa_config(
        rt_handle,
        external_number_of_prefix=jNone,
        external_prefix_length=jNone,
        external_prefix_metric=jNone,
        external_prefix_step=jNone,
        external_prefix_type=jNone,
        summary_number_of_prefix=jNone,
        summary_prefix_length=jNone,
        summary_prefix_metric=jNone,
        type=jNone,
        mode=jNone,
        summary_prefix_start=jNone,
        handle=jNone,
        summary_prefix_step=jNone,
        router_abr=jNone,
        router_asbr=jNone,
        external_prefix_start=jNone,
        nssa_prefix_length=jNone,
        nssa_prefix_step=jNone,
        nssa_number_of_prefix=jNone,
        nssa_prefix_metric=jNone,
        nssa_prefix_start=jNone,
        intra_area_link_state_id=jNone,
        intra_area_prefix_start=jNone,
        intra_area_prefix_step=jNone,
        intra_area_number_of_prefix=jNone,
        intra_area_prefix_length=jNone,
        intra_area_prefix_metric=jNone,
        intra_area_ref_ls_type=jNone,
        intra_area_ref_link_state_id=jNone,
        intra_area_ref_advertising_router_id=jNone,
        te_metric=jNone,
        te_max_bw=jNone,
        te_max_resv_bw=jNone,
        te_unres_bw_priority0=jNone,
        te_unres_bw_priority1=jNone,
        te_unres_bw_priority2=jNone,
        te_unres_bw_priority3=jNone,
        te_unres_bw_priority4=jNone,
        te_unres_bw_priority5=jNone,
        te_unres_bw_priority6=jNone,
        te_unres_bw_priority7=jNone,
        te_tlv_type=jNone,
        adv_router_id=jNone):
    """
    :param rt_handle:       RT object
    :param external_number_of_prefix
    :param external_prefix_length - <1-128>
    :param external_prefix_metric
    :param external_prefix_step - <1-16777215>
    :param external_prefix_type - <1-2>
    :param summary_number_of_prefix
    :param summary_prefix_length - <1-128>
    :param summary_prefix_metric
    :param type
    :param mode - <create|modify|delete|reset>
    :param summary_prefix_start
    :param handle
    :param summary_prefix_step - <1-65535>
    :param router_abr
    :param router_asbr
    :param external_prefix_start
    :param nssa_prefix_length - <1-128>
    :param nssa_prefix_step
    :param nssa_number_of_prefix
    :param nssa_prefix_metric - <1-16777215>
    :param nssa_prefix_start
    :param intra_area_link_state_id
    :param intra_area_prefix_start
    :param intra_area_prefix_step
    :param intra_area_number_of_prefix
    :param intra_area_prefix_length - <1-128>
    :param intra_area_prefix_metric - <0-65535>
    :param intra_area_ref_ls_type
    :param intra_area_ref_link_state_id
    :param intra_area_ref_advertising_router_id
    :param te_metric - <0-65535>
    :param te_max_bw
    :param te_max_resv_bw
    :param te_unres_bw_priority0
    :param te_unres_bw_priority1
    :param te_unres_bw_priority2
    :param te_unres_bw_priority3
    :param te_unres_bw_priority4
    :param te_unres_bw_priority5
    :param te_unres_bw_priority6
    :param te_unres_bw_priority7
    :param te_tlv_type
    :param adv_router_id

    Spirent Returns:
    {
        'status': 1,
        'adv_router_id': '0.0.0.0',
        'handles': 'ospf_lsa_1',
        'summary': {
          'prefix_step': '30',
          'prefix_length': '24',
          'num_prefx': '10',
          'prefix_start': '0.0.0.0'
        },
        'lsa_handle_pylist': ['summarylsablock1'],
        'lsa_handle': 'summarylsablock1'
    }

    IXIA Returns:
    {
        'handles': '/topology:1/deviceGroup:1/networkGroup:1',
        'external2_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterType2ExtRoutes:1',
        'sim_interface_ipv4_config_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simInterface:1/simInterfaceIPv4Config:1',
        'nssa_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterStubRoutes:1',
        'summary_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterSummaryRoutes:1',
        'simulated_interface_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simInterface:1/simInterfaceIPv4Config:1/ospfPseudoInterface:1',
        'network_group_handle': '/topology:1/deviceGroup:1/networkGroup:1',
        'external1_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterType1ExtRoutes:1',
        'simulated_router_handle':'/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1',
        'stub_handle': '/topology:1/deviceGroup:1/networkGroup:1/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterStubNetworks:1',
        'status': '1'
    }


    Common Return Keys:
        "status"
        "handles"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    global global_config
    args = dict()
    args['external_number_of_prefix'] = external_number_of_prefix
    args['external_prefix_length'] = external_prefix_length
    args['external_prefix_metric'] = external_prefix_metric
    args['external_prefix_step'] = external_prefix_step
    args['external_prefix_type'] = external_prefix_type
    args['summary_number_of_prefix'] = summary_number_of_prefix
    args['summary_prefix_length'] = summary_prefix_length
    args['summary_prefix_metric'] = summary_prefix_metric
    args['type'] = type
    args['mode'] = mode
    args['summary_prefix_start'] = summary_prefix_start
    args['handle'] = handle
    args['summary_prefix_step'] = summary_prefix_step
    args['router_abr'] = router_abr
    args['router_asbr'] = router_asbr
    args['external_prefix_start'] = external_prefix_start
    args['nssa_prefix_length'] = nssa_prefix_length
    args['nssa_prefix_step'] = nssa_prefix_step
    args['nssa_number_of_prefix'] = nssa_number_of_prefix
    args['nssa_prefix_metric'] = nssa_prefix_metric
    args['nssa_prefix_start'] = nssa_prefix_start
    args['intra_area_link_state_id'] = intra_area_link_state_id
    args['intra_area_prefix_start'] = intra_area_prefix_start
    args['intra_area_prefix_step'] = intra_area_prefix_step
    args['intra_area_number_of_prefix'] = intra_area_number_of_prefix
    args['intra_area_prefix_length'] = intra_area_prefix_length
    args['intra_area_prefix_metric'] = intra_area_prefix_metric
    args['intra_area_ref_ls_type'] = intra_area_ref_ls_type
    args['intra_area_ref_link_state_id'] = intra_area_ref_link_state_id
    args['intra_area_ref_advertising_router_id'] = intra_area_ref_advertising_router_id
    args['te_metric'] = te_metric
    args['te_max_bw'] = te_max_bw
    args['te_max_resv_bw'] = te_max_resv_bw
    args['te_unresv_bw_priority0'] = te_unres_bw_priority0
    args['te_unresv_bw_priority1'] = te_unres_bw_priority1
    args['te_unresv_bw_priority2'] = te_unres_bw_priority2
    args['te_unresv_bw_priority3'] = te_unres_bw_priority3
    args['te_unresv_bw_priority4'] = te_unres_bw_priority4
    args['te_unresv_bw_priority5'] = te_unres_bw_priority5
    args['te_unresv_bw_priority6'] = te_unres_bw_priority6
    args['te_unresv_bw_priority7'] = te_unres_bw_priority7
    args['te_tlv_type'] = te_tlv_type
    args['adv_router_id'] = adv_router_id

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    args = get_arg_value(rt_handle, j_emulation_ospf_lsa_config.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    counter = 1
    string = "ospf_lsa_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "ospf_lsa_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()
    if mode == 'modify':
        args['lsa_handle'] = handle
    if 'type' not in args:
        __check_and_raise('type')
    if type == 'opaque_type_9':
        args['type'] = 'intra_area_prefix'

    if te_tlv_type == 'router':
        raise ValueError("Wraper does not support te_tlv_type = 'router'")

    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            if hnd in handle_list:
                continue
            else:
                handle_list[hnd] = 1
            args['handle'] = hnd
            if mode == 'modify' or mode == 'delete':
                args['lsa_handle'] = hnd
            newer_ret = rt_handle.invoke('emulation_ospf_lsa_config', **args)
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'lsa_handle' in newer_ret:
                global_config[string].extend([newer_ret['lsa_handle']])
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if 'lsa_handle' in new_ret:
            new_ret['handles'] = string
        if new_ret:
            ret.append(new_ret)

    # ***** Return Value Modification *****


    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret



def j_emulation_pim_config(
        rt_handle,
        bidir_capable=jNone,
        handle=jNone,
        intf_ip_prefix_len=jNone,
        ip_version=jNone,
        override_interval=jNone,
        pim_mode=jNone,
        prune_delay=jNone,
        prune_delay_enable=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        mode=jNone,
        neighbor_intf_ip_addr=jNone,
        router_id=jNone,
        count=jNone,
        type=jNone,
        port_handle=jNone,
        dr_priority=jNone,
        hello_holdtime=jNone,
        hello_interval=jNone,
        prune_delay_tbit=jNone,
        bootstrap_interval=jNone,
        bootstrap_priority=jNone,
        join_prune_holdtime=jNone,
        join_prune_interval=jNone,
        router_id_step=jNone,
        bootstrap_enable=jNone,
        bootstrap_timeout=jNone,
        generation_id_mode=jNone,
        send_generation_id=jNone,
        intf_ip_addr=jNone,
        mac_address_start=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):
    """
    :param rt_handle:       RT object
    :param bidir_capable
    :param handle
    :param intf_ip_prefix_len - <1-128>
    :param ip_version - <4|6>
    :param override_interval - <100-32767>
    :param pim_mode - <sm|ssm>
    :param prune_delay - <100-32767>
    :param prune_delay_enable
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <1-4094>
    :param vlan_user_priority - <0-7>
    :param mode - <create|modify|delete|inactive:disable|active:enable>
    :param neighbor_intf_ip_addr
    :param router_id
    :param count - <1-65535>
    :param type - <remote_rp>
    :param port_handle
    :param dr_priority - <1-4294967295>
    :param hello_holdtime - <1-65535>
    :param hello_interval - <1-65535>
    :param prune_delay_tbit
    :param bootstrap_interval - <1-3600>
    :param bootstrap_priority - <1-255>
    :param join_prune_holdtime - <1-65535>
    :param join_prune_interval - <1-65535>
    :param router_id_step
    :param bootstrap_timeout - <1-65535>
    :param generation_id_mode - <increment|random|fixed:constant>
    :param bootstrap_enable
    :param send_generation_id
    :param intf_ip_addr
    :param mac_address_start
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <1-4094>
    :param vlan_outer_user_priority - <0-7>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1",
        "pim_router_handle": "/topology:1/deviceGroup:1/pimRouter:2",
        "pim_v4_interface_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['bidir_capable'] = bidir_capable
    args['handle'] = handle
    args['intf_ip_prefix_len'] = intf_ip_prefix_len
    args['ip_version'] = ip_version
    args['override_interval'] = override_interval
    args['pim_mode'] = pim_mode
    args['prune_delay'] = prune_delay
    args['prune_delay_enable'] = prune_delay_enable
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['mode'] = mode
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['router_id'] = router_id
    args['count'] = count
    args['type'] = type
    args['port_handle'] = port_handle
    args['dr_priority'] = dr_priority
    args['hello_holdtime'] = hello_holdtime
    args['hello_interval'] = hello_interval
    args['prune_delay_enable'] = prune_delay_tbit
    args['bootstrap_interval'] = bootstrap_interval
    args['bootstrap_priority'] = bootstrap_priority
    args['join_prune_holdtime'] = join_prune_holdtime
    args['join_prune_interval'] = join_prune_interval
    args['router_id_step'] = router_id_step
    args['intf_ip_addr'] = intf_ip_addr
    args['mac_address_start'] = mac_address_start
    args['vlan_outer_id'] = vlan_outer_id
    args['vlan_outer_id_mode'] = vlan_outer_id_mode
    args['vlan_outer_id_step'] = vlan_outer_id_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
   
    args = get_arg_value(rt_handle, j_emulation_pim_config.__doc__, **args)

    if 'bootstrap_priority' in args:
        args['c_bsr_priority'] = bootstrap_priority
        del args['bootstrap_priority']
    if 'bootstrap_interval' in args:
        args['bs_period'] = bootstrap_interval
        del args['bootstrap_interval']

    if 'handle' in args and not isinstance(handle, list):
        handle = [handle]
        handle = list(set(handle))

    counter = 1
    string = "pim_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "pim_" + str(counter)
    global_config[string] = []

    ret = []
    if handle != jNone:
        ret.append(invoke_handle(rt_handle, protocol_string=string, **args))
        if mode == 'enable' or mode == 'create':
            for hndl in handle:
                port_handle = __get_handle(hndl)
                handle_map[port_handle].extend(global_config[string])
                handle_map[port_handle] = list(set(handle_map[port_handle]))
                handle_map[string] = port_handle
    elif port_handle != jNone:
        result = rt_handle.invoke('emulation_pim_config', **args)
        if result.get('handle'):
            global_config[string].extend(result['handle'].split(' '))
            result['handles'] = string
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        if mode == 'create':
            for hand in port_handle:
                handle_map[hand] = handle_map.get(hand, [])
                handle_map[hand].extend(global_config[string])
                handle_map[hand] = list(set(handle_map[hand]))
                handle_map[string] = hand
        ret.append(result)
    else:
        raise RuntimeError('Either handle or port_handle must be passed to j_emulation_pim_config')

    # **** Native Argument Execution ****
    if mode == 'create' or mode == 'modify':
        for index in range(len(ret)):
            if 'handle' in ret[index]:
                myHandle = ret[index]['handle']
            else:
                continue
            if not isinstance(myHandle, list):
                myHandle = [myHandle]
            myHandle = list(set(myHandle))
            for hand in myHandle:
                pim_router_handle = rt_handle.invoke('invoke', cmd='stc::get' + " " +  hand  + ' -children' + '-pimrouterconfig')
                if bootstrap_enable != jNone:
                    if int(bootstrap_enable) == 1:
                        rt_handle.invoke('invoke', cmd='stc::config' + " " + pim_router_handle + ' -enablebsr' + ' TRUE')
                    if int(bootstrap_enable) == 0:
                        rt_handle.invoke('invoke', cmd='stc::config' + " " + pim_router_handle + ' -enablebsr' + ' FALSE')
                rt_handle.invoke('invoke', cmd='stc::apply')

                if generation_id_mode != jNone:
                    rt_handle.invoke('invoke', cmd='stc::config' + " " + pim_router_handle + ' -GenIdMode' + " " + generation_id_mode)
                    rt_handle.invoke('invoke', cmd='stc::apply')
                if send_generation_id != jNone:
                    if int(send_generation_id) == 1:
                        rt_handle.invoke('invoke', cmd='stc::config' + " " + pim_router_handle + ' -GenIdMode' + " " + generation_id_mode)
                        rt_handle.invoke('invoke', cmd='stc::apply')
                if bootstrap_timeout != jNone:
                    rt_handle.invoke('invoke', cmd='stc::config' + " " + pim_router_handle + ' -enablebsr' + ' TRUE')
                    rt_handle.invoke('invoke', cmd='stc::config' + " " + pim_router_handle + ' -HelloHoldTime' + " " + bootstrap_timeout)
                    rt_handle.invoke('invoke', cmd='stc::apply')
    # **** End of Native Arguments ****

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_pim_control(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <stop|start|restart|join>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
     
    args = get_arg_value(rt_handle, j_emulation_pim_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        for hnd in global_config[hndl]:
            args['handle'] = hnd
            if mode == 'stop' or mode == 'start' or mode == 'restart':
               args['handle'] = hnd
               port_handle = __get_handle(hndl)
               args['port_handle'] = port_handle
            if mode == 'join' and 'handle' in args:
                pim_handle = rt_handle.invoke('invoke', cmd='stc::get '+hnd+' -parent')
                pim_handle_1 = rt_handle.invoke('invoke', cmd='stc::get '+pim_handle+' -parent')
                args['handle'] = pim_handle_1
            ret.append(rt_handle.invoke('emulation_pim_control', **args))


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_pim_group_config(
        rt_handle,
        group_pool_handle=jNone,
        handle=jNone,
        interval=jNone,
        join_prune_per_interval=jNone,
        mode=jNone,
        rate_control=jNone,
        register_per_interval=jNone,
        register_stop_per_interval=jNone,
        rp_ip_addr=jNone,
        session_handle=jNone,
        wildcard_group=jNone,
        group_pool_mode=jNone,
        source_pool_handle=jNone,
        default_mdt_mode=jNone,
        join_prune_aggregation_factor=jNone,
        register_tx_iteration_gap=jNone,
        s_g_rpt_group=jNone,
        send_null_register=jNone,
        source_group_mapping=jNone):
    """
    :param rt_handle:       RT object
    :param group_pool_handle
    :param handle
    :param interval - <1-1000>
    :param join_prune_per_interval - <1-1000>
    :param mode - <create|modify|delete>
    :param rate_control
    :param register_per_interval - <1-1000>
    :param register_stop_per_interval - <1-1000>
    :param rp_ip_addr
    :param session_handle
    :param wildcard_group
    :param group_pool_mode - <send|register>
    :param source_pool_handle
    :param default_mdt_mode
    :param join_prune_aggregation_factor
    :param register_tx_iteration_gap - <100-1000>
    :param s_g_rpt_group
    :param send_null_register
    :param source_group_mapping - <one_to_one|fully_meshed>

    Spirent Returns:
    {
        "group_handles": "ipv4group1",
        "group_pool_handle": "ipv4group1",
        "handle": "pimv4groupblk1 pimv4groupblk2",
        "source_handles": "multicastSourcePool(0)",
        "source_pool_handle": "multicastSourcePool(0)",
        "status": "1"
    }

    IXIA Returns:
    {
        "group_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4JoinPruneList",
        "pim_v4_candidate_rp_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4CandidateRPsList",
        "pim_v4_join_prune_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4JoinPruneList",
        "pim_v4_source_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4SourcesList",
        "source_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/pimV4SourcesList",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "group_handles"
        "source_handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    n_args = dict()
    args['group_pool_handle'] = group_pool_handle
    args['handle'] = handle
    args['interval'] = interval
    args['join_prune_per_interval'] = join_prune_per_interval
    args['mode'] = mode
    args['rate_control'] = rate_control
    args['register_per_interval'] = register_per_interval
    args['register_stop_per_interval'] = register_stop_per_interval
    args['rp_ip_addr'] = rp_ip_addr
    args['session_handle'] = session_handle
    args['wildcard_group'] = wildcard_group
    args['source_pool_handle'] = source_pool_handle
    args['group_pool_mode'] = group_pool_mode
    args['s_g_rpt_group'] = s_g_rpt_group
    args['source_group_mapping'] = source_group_mapping

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
   
    args = get_arg_value(rt_handle, j_emulation_pim_group_config.__doc__, **args)
    n_args['default_mdt_mode'] = default_mdt_mode
    n_args = get_arg_value(rt_handle, j_emulation_pim_group_config.__doc__, **n_args)

    if 'default_mdt_mode' in n_args:
        n_args['multicast_data_mdt_enable'] = n_args['default_mdt_mode']
        del n_args['default_mdt_mode']
  
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if mode == 'create' and  default_mdt_mode != jNone:
        n_args['mode'] = 'create'
        rt_handle.invoke('emulation_mvpn_config', **n_args)

    counter = 1
    string = "pim_group_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "pim_group_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()

    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            if hnd in handle_list:
                continue
            else:
                handle_list[hnd] = 1
            args['handle'] = hnd
            if mode == 'create':
                args['session_handle'] = hnd
            if mode == 'modify':
                pim_iproute_parent = rt_handle.invoke('invoke', cmd='stc::get' + " " + hnd  + ' -parent')
                pim_route_parent = rt_handle.invoke('invoke', cmd='stc::get' + " " + pim_iproute_parent  + ' -parent')
                args['session_handle'] = pim_route_parent
            newer_ret = rt_handle.invoke('emulation_pim_group_config', **args)
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'handle' in newer_ret:
                global_config[string].extend([newer_ret['handle']])
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if 'handles' in new_ret:
            new_ret['handle'] = new_ret['handles']
        new_ret['handles'] = string
        if new_ret:
            ret.append(new_ret)

    # ***** Native Code Execution *****
    if mode == 'create':
        if join_prune_aggregation_factor != jNone:
            if int(join_prune_aggregation_factor) >= 1:
                rt_handle.invoke('invoke', cmd='stc::config' + " " + 'pimglobalconfig1' + ' -EnablePackGroupRecord' + ' TRUE')
            else:
                rt_handle.invoke('invoke', cmd='stc::config' + " " + 'pimglobalconfig1' + ' -EnablePackGroupRecord' + ' FALSE')
            rt_handle.invoke('invoke', cmd='stc::apply')

        if register_tx_iteration_gap != jNone:
            if int(register_tx_iteration_gap) == 1:
                rt_handle.invoke('invoke', cmd='stc::config' + " " + 'pimglobalconfig1' + ' -MsgInterval' +  " " + register_tx_iteration_gap)
            else:
                rt_handle.invoke('invoke', cmd='stc::config' + " " + 'pimglobalconfig1' + ' -MsgInterval' +  " " + register_tx_iteration_gap)
            rt_handle.invoke('invoke', cmd='stc::apply')
            
        for index in range(len(ret)):
            if 'handle' in ret[index]:
                myHandle = ret[index]['handle']
            else:
                continue
            if not isinstance(myHandle, list):
                myHandle = [myHandle]
            myHandle = list(set(myHandle))
            for hand in myHandle:
                pim_router_handle1 = rt_handle.invoke('invoke', cmd='stc::get' + " " +  hand  + ' -parent')
                if send_null_register != jNone:
                    if int(send_null_register) == 1:
                        rt_handle.invoke('invoke', cmd='stc::config' + " " + pim_router_handle1 + ' -NullRegisterOnlyMode' + ' TRUE')
                    else:
                        rt_handle.invoke('invoke', cmd='stc::config' + " " + pim_router_handle1 + ' -NullRegisterOnlyMode' + ' FALSE')
                    rt_handle.invoke('invoke', cmd='stc::apply')    

    # ***** End of Native Arguments *****


    # ***** Return Value Modification *****
    for index in range(len(ret)):
        if 'source_pool_handle' in ret[index]:
            ret[index]['source_handles'] = ret[index]['source_pool_handle']
        if 'group_pool_handle' in ret[index]:
            ret[index]['group_handles'] = ret[index]['group_pool_handle']


    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_pim_info(rt_handle, handle=jNone,
                         port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param port_handle

    Spirent Returns:
    {
        "bsm_rx": "0",
        "bsm_tx": "0",
        "crp_rx": "0",
        "duration": "35.5476400852",
        "group_assert_rx": "0",
        "group_join_rx": "0",
        "group_join_tx": "0",
        "handle": "host1",
        "hello_rx": "1",
        "hello_tx": "2",
        "j_p_pdu_rx": "1",
        "j_p_pdu_tx": "1",
        "reg_rx": "0",
        "reg_stop_rx": "0",
        "router_id": "192.0.0.1",
        "router_state": "NEIGHBOR",
        "s_g_join_rx": "2",
        "s_g_join_tx": "2",
        "status": "1",
        "upstream_neighbor_addr": "3.3.3.2"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/pimV4Interface:1/item:1": {
            "session": {
                "bootstrap_rx": "0",
                "bootstrap_tx": "0",
                "group_join_rx": "0",
                "group_join_tx": "0",
                "group_prune_rx": "0",
                "group_prune_tx": "0",
                "hello_rx": "2",
                "hello_tx": "1",
                "normal_crp_adv_msg_rx": "0",
                "normal_crp_adv_msg_tx": "0",
                "null_reg_rx": "0",
                "null_reg_tx": "0",
                "num_neighbors_learnt": "1",
                "port_name": "1/11/2",
                "reg_rx": "0",
                "reg_stop_rx": "0",
                "reg_stop_tx": "0",
                "reg_tx": "0",
                "rp_join_rx": "0",
                "rp_join_tx": "0",
                "rp_prune_rx": "0",
                "rp_prune_tx": "0",
                "s_g_join_rx": "0",
                "s_g_join_tx": "0",
                "s_g_prune_rx": "0",
                "s_g_prune_tx": "0",
                "s_g_rpt_join_rx": "0",
                "s_g_rpt_join_tx": "0",
                "s_g_rpt_prune_rx": "0",
                "s_g_rpt_prune_tx": "0",
                "session_flap": "0",
                "shutdown_crp_adv_msg_rx": "0",
                "shutdown_crp_adv_msg_tx": "0"
            }
        },
        "1/11/2": {
            "aggregate": {
                "bootstrap_rx": "0",
                "bootstrap_tx": "0",
                "group_join_rx": "0",
                "group_join_tx": "0",
                "group_prune_rx": "0",
                "group_prune_tx": "0",
                "hello_rx": "2",
                "hello_tx": "1",
                "normal_crp_adv_msg_rx": "0",
                "normal_crp_adv_msg_tx": "0",
                "null_reg_rx": "0",
                "null_reg_tx": "0",
                "num_neighbors_learnt": "1",
                "num_routers_configured": "1",
                "num_routers_running": "1",
                "port_name": "1/11/2",
                "reg_rx": "0",
                "reg_stop_rx": "0",
                "reg_stop_tx": "0",
                "reg_tx": "0",
                "rp_join_rx": "0",
                "rp_join_tx": "0",
                "rp_prune_rx": "0",
                "rp_prune_tx": "0",
                "s_g_join_rx": "0",
                "s_g_join_tx": "0",
                "s_g_prune_rx": "0",
                "s_g_prune_tx": "0",
                "s_g_rpt_join_rx": "0",
                "s_g_rpt_join_tx": "0",
                "s_g_rpt_prune_rx": "0",
                "s_g_rpt_prune_tx": "0",
                "session_flap": "0",
                "shutdown_crp_adv_msg_rx": "0",
                "shutdown_crp_adv_msg_tx": "0",
                "status": "started"
            }
        },
        "bsm_rx": "0",
        "bsm_tx": "0",
        "crp_rx": "0",
        "group_join_rx": "0",
        "group_join_tx": "0",
        "hello_rx": "2",
        "hello_tx": "1",
        "reg_rx": "0",
        "reg_stop_rx": "0",
        "s_g_join_rx": "0",
        "s_g_join_tx": "0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "bsm_rx"
        "bsm_tx"
        "crp_rx"
        "group_join_rx"
        "group_join_tx"
        "hello_rx"
        "hello_tx"
        "reg_rx"
        "reg_stop_rx"
        "s_g_join_rx"
        "s_g_join_tx"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []

    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            args['handle'] = hnd

            newer_ret = dict()
            newer_ret.update(rt_handle.invoke('emulation_pim_info', **args))

            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if new_ret:
            ret.append(new_ret)

    # **** Add code to consolidate stats here ****

    for index in range(len(ret)):
        for key in ret[index]:
            if isinstance(ret[index][key], list):
                if 'reg_stop_rx' in key or 'group_assert_rx' in key or 's_g_join_rx' in key or 'group_join_rx' in key or 'crp_rx' in key or 'hello_rx' in key or 'j_p_pdu_rx' in key or 'hello_tx' in key or 'bsm_tx' in key or 'bsm_rx' in key or 'reg_rx' in key or 'group_join_tx'in key or 'j_p_pdu_tx' in key or 's_g_join_tx' in key:
                    ret[index][key] = sum(list(map(int, ret[index][key])))
                elif 'duration' in key:
                    ret[index][key] = sum(list(map(float, ret[index][key]))) / len(ret[index][key])

    # **** Add code to consolidate stats here ****

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_rsvp_config(
        rt_handle,
        count=jNone,
        gateway_ip_addr_step=jNone,
        handle=jNone,
        hello_interval=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_length=jNone,
        recovery_time=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        neighbor_intf_ip_addr=jNone,
        mode=jNone,
        bfd_registration=jNone,
        graceful_restart=jNone,
        hello_msgs=jNone,
        max_label_value=jNone,
        min_label_value=jNone,
        refresh_reduction=jNone,
        srefresh_interval=jNone,
        bundle_msg_sending=jNone,
        intf_ip_addr=jNone,
        actual_restart_time=jNone,
        hello_retry_count=jNone,
        graceful_restart_recovery_time=jNone,
        port_handle=jNone,
        gateway_ip_addr=jNone,
        vlan_outer_id=jNone,
        vlan_outer_id_mode=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone):
    """
    :param rt_handle:       RT object
    :param count
    :param gateway_ip_addr_step
    :param handle
    :param hello_interval
    :param intf_ip_addr_step
    :param intf_prefix_length
    :param recovery_time
    :param vlan_id
    :param vlan_id_mode
    :param vlan_id_step
    :param vlan_user_priority
    :param neighbor_intf_ip_addr
    :param mode - <create|active:enable|inactive:disable|modify|delete>
    :param bfd_registration
    :param graceful_restart
    :param hello_msgs
    :param max_label_value
    :param min_label_value
    :param refresh_reduction
    :param srefresh_interval
    :param bundle_msg_sending
    :param intf_ip_addr
    :param actual_restart_time
    :param hello_retry_count
    :param graceful_restart_recovery_time
    :param port_handle
    :param gateway_ip_addr
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_id_mode - <fixed|increment>
    :param vlan_outer_id_step - <1-4094>
    :param vlan_outer_user_priority - <0-7>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1",
        "rsvp_if_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config


    args = dict()
    args['count'] = count
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['handle'] = handle
    args['hello_interval'] = hello_interval
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['intf_prefix_length'] = intf_prefix_length
    args['recovery_time'] = recovery_time
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['neighbor_intf_ip_addr'] = neighbor_intf_ip_addr
    args['mode'] = mode
    args['bfd_registration'] = bfd_registration
    args['graceful_restart'] = graceful_restart
    args['hello_msgs'] = hello_msgs
    args['max_label_value'] = max_label_value
    args['min_label_value'] = min_label_value
    args['refresh_reduction'] = refresh_reduction
    args['srefresh_interval'] = srefresh_interval
    args['use_gateway_as_dut_ip_addr'] = "true"
    args['bundle_msgs'] = bundle_msg_sending
    args['intf_ip_addr'] = intf_ip_addr
    args['graceful_restart_restart_time'] = actual_restart_time
    args['graceful_restart_recovery_time'] = graceful_restart_recovery_time
    args['port_handle'] = port_handle
    args['gateway_ip_addr'] = gateway_ip_addr
    args['vlan_outer_id'] = vlan_outer_id
    args['vlan_outer_id_mode'] = vlan_outer_id_mode
    args['vlan_outer_id_step'] = vlan_outer_id_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority


    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_rsvp_config.__doc__, **args) 

    if 'handle' in args and not isinstance(handle, list):
        handle = [handle]
        handle = list(set(handle))
   
    if 'record_route' not in args.keys():
        args['record_route'] = 1

    counter = 1
    string = "rsvp_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "rsvp_" + str(counter)
    global_config[string] = []

    ret = []
    if handle != jNone:
        ret.append(invoke_handle(rt_handle, protocol_string=string, **args))
        if mode == 'create':
            for hndl in handle:
                port_handle = __get_handle(hndl)
                session_map[port_handle] = session_map.get(port_handle, [])
                session_map[port_handle].extend(global_config[string])
                session_map[string] = port_handle
    elif port_handle != jNone:
        result = rt_handle.invoke('emulation_rsvp_config', **args)
        if result.get('handle'):
            global_config[string].extend(result['handle'].split(' '))
            result['handles'] = string
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        if mode == 'create':
            for hand in port_handle:
                session_map[hand] = session_map.get(hand, [])
                session_map[hand].extend(global_config[string])
                session_map[string] = hand
                handle_map[hand] = handle_map.get(hand, [])
                handle_map[hand].extend(global_config[string])
                handle_map[string] = hand
        ret.append(result)
    else:
        raise RuntimeError('Either port_handle or handle must be passed to j_emulation_rsvp_config ')
    # ***** Native Arguments Execution ****
    for index in range(len(ret)):
        if 'handle' in ret[index]:
            myHandle = ret[index]['handle']
            rsvp_router_handle = rt_handle.invoke('invoke', cmd='stc::get' + " " +  myHandle  + ' -children' +  '-rsvprouterconfig')
            if hello_retry_count != jNone:
                rt_handle.invoke('invoke', cmd='stc::config' + " " + rsvp_router_handle + ' -RetransmitInterval' + " " + hello_retry_count)
    # **** End Native Arguments ****

    # ***** Return Value Modification *****
    if len(ret) == 1:
        ret = ret[0]
    # ***** End of Return Value Modification *****
    return ret


def j_emulation_rsvp_control(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <start|stop|restart|stop_hellos:stop_hello>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_rsvp_control.__doc__, **args)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        hnd = " ".join(global_config[hndl])
        args['handle'] = hnd
        ret.append(rt_handle.invoke('emulation_rsvp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_rsvp_info(rt_handle, handle=jNone):
    """
    :param rt_handle:       RT object
    :param handle

    Spirent Returns:
    {
        "egress_path_rx": "3",
        "egress_patherr_rx": "0",
        "egress_pathtear_rx": "0",
        "egress_resv_tx": "2",
        "egress_resvconf_rx": "0",
        "egress_resverr_tx": "0",
        "egress_resvtear_tx": "0",
        "hellos_rx": "0",
        "hellos_tx": "0",
        "ingress_path_tx": "2",
        "ingress_patherr_tx": "0",
        "ingress_pathtear_tx": "0",
        "ingress_resv_rx": "3",
        "ingress_resvconf_tx": "0",
        "ingress_resverr_rx": "0",
        "ingress_resvtear_rx": "0",
        "intf_ip_address": "10.10.10.1",
        "lsp_connecting": "0",
        "lsp_count": "1",
        "lsp_created": "1",
        "lsp_deleted": "0",
        "max_setup_time": "0",
        "min_setup_time": "0",
        "msg_rx": "6",
        "msg_tx": "4",
        "neighbor_intf_ip_addr": "10.10.10.2",
        "num_lsps_setup": "1",
        "status": "1"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1": {
            "learned_info": {
                "assigned": {
                    "BandWidth (in bps)": "0",
                    "Current State": "Up",
                    "Device#": "1",
                    "Dut IP": "10.10.10.2",
                    "ERO AS Number": "NA",
                    "ERO IP": "NA",
                    "ERO Prefix Length": "NA",
                    "ERO Type": "NA",
                    "Head End IP": "10.10.10.2",
                    "LSP ID": "1",
                    "Label": "1000",
                    "Last Flap Reason": "None",
                    "Our IP": "10.10.10.1",
                    "Reservation State(for Graceful-Restart)": "None",
                    "Session IP": "10.10.10.1",
                    "Setup Time(ms)": "0",
                    "Tunnel ID": "1",
                    "Up Time(ms)": "39276"
                },
                "p2mp": {
                    "Current State": "Down Down",
                    "Device#": "NA NA",
                    "Dut IP": "NA NA",
                    "Head End IP": "NA NA",
                    "LSP ID": "NA NA",
                    "Label": "NA NA",
                    "Last Flap Reason": "None None",
                    "Leaf IP": "NA NA",
                    "Our IP": "NA NA",
                    "P2MP ID": "NA NA",
                    "P2MP ID as Number": "NA NA",
                    "Reservation State(for Graceful-Restart)": "None None",
                    "Setup Time(ms)": "NA NA",
                    "Sub Group ID": "NA NA",
                    "Sub Group Originator ID": "NA NA",
                    "Tunnel ID": "NA NA",
                    "Up Time(ms)": "NA NA"
                },
                "received": {
                    "BandWidth (in bps)": "0",
                    "Current State": "Up",
                    "Device#": "1",
                    "Dut IP": "10.10.10.2",
                    "ERO AS Number": "NA",
                    "ERO IP": "NA",
                    "ERO Prefix Length": "NA",
                    "ERO Type": "NA",
                    "Head End IP": "10.10.10.1",
                    "LSP ID": "1",
                    "Label": "1000",
                    "Last Flap Reason": "None",
                    "Our IP": "10.10.10.1",
                    "RRO C-Type": "NA",
                    "RRO IP": "NA",
                    "RRO Label": "NA",
                    "RRO Type": "NA",
                    "Reservation State(for Graceful-Restart)": "None",
                    "Session IP": "10.10.10.2",
                    "Setup Time(ms)": "4",
                    "Symbolic Path Name": "RSVP P2P LSP 1",
                    "Tunnel ID": "1",
                    "Up Time(ms)": "39283"
                }
            }
        },
        "1/11/2": {
            "aggregate": {
                "acks_rx": "0",
                "acks_tx": "0",
                "bundle_messages_rx": "0",
                "bundle_messages_tx": "0",
                "down_state_count": "0",
                "egress_lsps_up": "1",
                "egress_out_of_order_messages_rx": "0",
                "egress_sub_lsps_up": "0",
                "hellos_rx": "0",
                "hellos_tx": "0",
                "ingress_lsps_configured": "1",
                "ingress_lsps_up": "1",
                "ingress_out_of_order_messages_rx": "0",
                "ingress_sub_lsps_configured": "0",
                "ingress_sub_lsps_up": "0",
                "nacks_rx": "0",
                "nacks_tx": "0",
                "no_of_path_re_optimizations": "0",
                "own_graceful_restarts": "0",
                "path_errs_rx": "0",
                "path_errs_tx": "0",
                "path_re_evaluation_request_tx": "0",
                "path_sent_state_count": "0",
                "path_tears_rx": "0",
                "path_tears_tx": "0",
                "paths_rx": "2",
                "paths_tx": "2",
                "paths_with_recovery_label_rx": "0",
                "paths_with_recovery_label_tx": "0",
                "peer_graceful_restarts": "0",
                "resv_confs_rx": "0",
                "resv_confs_tx": "0",
                "resv_errs_rx": "0",
                "resv_errs_tx": "0",
                "resv_tears_rx": "0",
                "resv_tears_tx": "0",
                "resvs_rx": "2",
                "resvs_tx": "2",
                "session_flap_count": "0",
                "sessions_down": "0",
                "sessions_not_started": "0",
                "sessions_total": "1",
                "sessions_up": "1",
                "srefreshs_rx": "0",
                "srefreshs_tx": "0",
                "status": "started",
                "unrecovered_resvs_deleted": "0",
                "up_state_count": "1"
            }
        },
        "hellos_rx": "0",
        "hellos_tx": "0",
        "lsp_count": "1",
        "lsp_created": "1",
        "lsp_deleted": "0",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "hellos_rx"
        "hellos_tx"
        "lsp_count"
        "lsp_created"
        "lsp_deleted"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            args['handle'] = hnd

            newer_ret = dict()
            args['mode'] = 'stats'
            newer_ret.update(rt_handle.invoke('emulation_rsvp_info', **args))
            args['mode'] = 'settings'
            newer_ret.update(rt_handle.invoke('emulation_rsvp_info', **args))

            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if new_ret:
            ret.append(new_ret)

    # **** Add code to consolidate stats here ****

    for index in range(len(ret)):
        for key in ret[index]:
            if isinstance(ret[index][key], list):
                if 'hellos_rx' in key or 'egress_resv_tx' in key or 'lsp_created' in key or 'egress_patherr_rx' in key or 'ingress_resverr_rx' in key or 'ingress_resv_rx' in key or 'lsp_connecting' in key or 'ingress_resvtear_rx' in key or 'lsp_count' in key or 'msg_rx' in key or 'hellos_tx' in key or 'egress_resvconf_rx' in key or 'egress_pathtear_rx' in key or 'egress_pathtear_rx' in key or 'max_setup_time' in key or 'ingress_pathtear_tx' in key or 'egress_path_rx' in key or 'egress_resvtear_tx' in key or 'msg_tx' in key or 'ingress_path_tx' in key or 'egress_resverr_tx' in key or 'ingress_patherr_tx' in key or 'lsp_deleted' in key or 'num_lsps_setup' in key or 'ingress_resvconf_tx' in key:
                    ret[index][key] = sum(list(map(int, ret[index][key])))
                elif 'min_setup_time'in key:
                    ret[index][key] = sum(list(map(int, ret[index][key]))) // len(ret[index][key])

    # **** Add code to consolidate stats here ****


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_rsvp_tunnel_config(
        rt_handle,
        avoid_node_id=jNone,
        count=jNone,
        fast_reroute_bandwidth=jNone,
        fast_reroute_exclude_any=jNone,
        fast_reroute_holding_priority=jNone,
        fast_reroute_include_all=jNone,
        fast_reroute_include_any=jNone,
        fast_reroute_setup_priority=jNone,
        handle=jNone,
        plr_id=jNone,
        send_detour=jNone,
        mode=jNone,
        ingress_dst_ip_addr=jNone,
        ingress_ip_addr=jNone,
        session_attr_bw_protect=jNone,
        fast_reroute=jNone,
        session_attr_ra_exclude_any=jNone,
        facility_backup=jNone,
        session_attr_resource_affinities=jNone,
        fast_reroute_hop_limit=jNone,
        one_to_one_backup=jNone,
        session_attr_hold_priority=jNone,
        session_attr_ra_include_all=jNone,
        session_attr_ra_include_any=jNone,
        session_attr_label_record=jNone,
        session_attr_local_protect=jNone,
        sender_tspec_max_pkt_size=jNone,
        sender_tspec_min_policed_size=jNone,
        session_attr_node_protect=jNone,
        sender_tspec_peak_data_rate=jNone,
        session_attr_se_style=jNone,
        session_attr_setup_priority=jNone,
        sender_tspec_token_bkt_size=jNone,
        sender_tspec_token_bkt_rate=jNone,
        ero=jNone,
        rsvp_behavior=jNone,
        ingress_dst_ip_addr_step=jNone,
        lsp_id_count=jNone,
        tunnel_id_start=jNone,
        tunnel_id_step=jNone,
        tunnel_count=jNone,
        egress_ip_addr=jNone,
        ero_list_ipv4=jNone,
        ero_list_pfxlen=jNone,
        ero_list_loose=jNone):

    """
    :param rt_handle:       RT object
    :param avoid_node_id
    :param count
    :param fast_reroute_bandwidth
    :param fast_reroute_exclude_any
    :param fast_reroute_holding_priority
    :param fast_reroute_include_all
    :param fast_reroute_include_any
    :param fast_reroute_setup_priority
    :param handle
    :param plr_id
    :param send_detour
    :param mode - <create|modify|delete>
    :param ingress_dst_ip_addr
    :param ingress_ip_addr
    :param session_attr_bw_protect
    :param fast_reroute
    :param session_attr_ra_exclude_any
    :param facility_backup
    :param session_attr_resource_affinities
    :param fast_reroute_hop_limit
    :param one_to_one_backup
    :param session_attr_hold_priority
    :param session_attr_ra_include_all
    :param session_attr_ra_include_any
    :param session_attr_label_record
    :param session_attr_local_protect
    :param sender_tspec_max_pkt_size
    :param sender_tspec_min_policed_size
    :param session_attr_node_protect
    :param sender_tspec_peak_data_rate
    :param session_attr_se_style
    :param session_attr_setup_priority
    :param sender_tspec_token_bkt_size
    :param sender_tspec_token_bkt_rate
    :param ero
    :param rsvp_behavior
    :param ingress_dst_ip_addr_step
    :param lsp_id_count
    :param tunnel_id_start
    :param tunnel_id_step
    :param tunnel_count
    :param egress_ip_addr
    :param ero_list_ipv4
    :param ero_list_pfxlen
    :param ero_list_loose 

    Spirent Returns:
    {
        "egress_handles": [
            "host1"
        ],
        "handles": "rsvpingresstunnelparams1",
        "ingress_handles": [
            "host1"
        ],
        "status": "1",
        "tunnel_handle": "rsvpingresstunnelparams1"
    }


    IXIA Returns:
    {
        "egress_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2/rsvpP2PEgressLsps",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2",
        "ingress_handles": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2/rsvpP2PIngressLsps",
        "rsvpte_lsp_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2",
        "rsvpte_p2p_egress_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2/rsvpP2PEgressLsps",
        "rsvpte_p2p_ingress_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteLsps:2/rsvpP2PIngressLsps",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "egress_handles"
        "handles"
        "ingress_handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['avoid_node_id'] = avoid_node_id
    args['count'] = count
    args['fast_reroute_bandwidth'] = fast_reroute_bandwidth
    args['fast_reroute_exclude_any'] = fast_reroute_exclude_any
    args['fast_reroute_holding_priority'] = fast_reroute_holding_priority
    args['fast_reroute_include_all'] = fast_reroute_include_all
    args['fast_reroute_include_any'] = fast_reroute_include_any
    args['fast_reroute_setup_priority'] = fast_reroute_setup_priority
    args['handle'] = handle
    args['plr_id'] = plr_id
    args['send_detour'] = send_detour
    args['mode'] = mode
    args['ingress_dst_ip_addr'] = ingress_dst_ip_addr
    args['ingress_ip_addr'] = ingress_ip_addr
    args['session_attr_bw_protect'] = session_attr_bw_protect
    args['fast_reroute'] = fast_reroute
    args['session_attr_ra_exclude_any'] = session_attr_ra_exclude_any
    args['facility_backup'] = facility_backup
    args['session_attr_resource_affinities'] = session_attr_resource_affinities
    args['fast_reroute_hop_limit'] = fast_reroute_hop_limit
    args['one_to_one_backup'] = one_to_one_backup
    args['session_attr_hold_priority'] = session_attr_hold_priority
    args['session_attr_ra_include_all'] = session_attr_ra_include_all
    args['session_attr_ra_include_any'] = session_attr_ra_include_any
    args['session_attr_label_record'] = session_attr_label_record
    args['session_attr_local_protect'] = session_attr_local_protect
    args['sender_tspec_max_pkt_size'] = sender_tspec_max_pkt_size
    args['sender_tspec_min_policed_size'] = sender_tspec_min_policed_size
    args['session_attr_node_protect'] = session_attr_node_protect
    args['sender_tspec_peak_data_rate'] = sender_tspec_peak_data_rate
    args['session_attr_se_style'] = session_attr_se_style
    args['session_attr_setup_priority'] = session_attr_setup_priority
    args['sender_tspec_token_bkt_size'] = sender_tspec_token_bkt_size
    args['sender_tspec_token_bkt_rate'] = sender_tspec_token_bkt_rate
    args['ero'] = ero
    args['rsvp_behavior'] = rsvp_behavior
    args['ingress_dst_ip_addr_step'] = ingress_dst_ip_addr_step
    args['lsp_id_count'] = lsp_id_count
    args['tunnel_id_start'] = tunnel_id_start
    args['tunnel_id_step'] = tunnel_id_step
    args['tunnel_count'] = tunnel_count
    args['egress_ip_addr'] = egress_ip_addr
    args['ero_list_ipv4'] = ero_list_ipv4
    args['ero_list_pfxlen'] = ero_list_pfxlen
    args['ero_list_loose'] = ero_list_loose

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
 
    args = get_arg_value(rt_handle, j_emulation_rsvp_tunnel_config.__doc__, **args)
 
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    counter = 1
    string = "rsvp_tunnel_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "rsvp_tunnel_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()
    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            if hnd in handle_list:
                continue
            else:
                handle_list[hnd] = 1
            args['handle'] = hnd
            if mode == 'modify' or mode == 'delete':
               args['tunnel_pool_handle'] = hnd
            newer_ret = rt_handle.invoke('emulation_rsvp_tunnel_config', **args)
            if 'ingress_dst_ip_addr' in args and 'ingress_dst_ip_addr_step' in args:
                args['ingress_dst_ip_addr'] = incrementIpV4Address(args['ingress_dst_ip_addr'], args['ingress_dst_ip_addr_step'])
            if 'ingress_ip_addr' in args and 'ingress_dst_ip_addr_step' in args:
                args['ingress_ip_addr'] = incrementIpV4Address(args['ingress_ip_addr'], args['ingress_dst_ip_addr_step'])

            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'tunnel_handle' in newer_ret:
                global_config[string].extend([newer_ret['tunnel_handle']])
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if 'tunnel_handle' in new_ret:
            new_ret['handles'] = string
            new_ret['ingress_handles'] = string
            new_ret['egress_handles'] = string
        if new_ret:
            ret.append(new_ret)


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_rsvpte_tunnel_control(
        rt_handle,
        handle=jNone,
        mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['action'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_rsvpte_tunnel_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    if mode == 'start':
        args['action'] = 'connect'

    ret = []
    for hndl in handle:
        for hnd in global_config[hndl]:
            args['handle'] = hnd
            if 'handle' in args and hnd.startswith('rsvpingresstunnelparams') and mode == 'stop':
                args['action'] = 'tear_down_outbound'
            elif 'handle' in args and hnd.startswith('rsvpegresstunnelparams') and mode == 'stop':
                args['action'] = 'tear_down_inbound'
            ret.append(rt_handle.invoke('emulation_rsvpte_tunnel_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_interface_config(
        rt_handle,
        arp_send_req=jNone,
        autonegotiation=jNone,
        clocksource=jNone,
        framing=jNone,
        gateway=jNone,
        gateway_step=jNone,
        internal_ppm_adjust=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        ipv6_gateway_step=jNone,
        ipv6_intf_addr=jNone,
        ipv6_intf_addr_step=jNone,
        ipv6_prefix_length=jNone,
        qinq_incr_mode=jNone,
        speed=jNone,
        intf_prefix_len=jNone,
        src_mac_addr=jNone,
        port_handle=jNone,
        mode=jNone,
        handle=jNone,
        ipv6_gateway=jNone,
        topology_name=jNone,
        device_group_name=jNone,
        src_mac_addr_step=jNone,
        phy_mode=jNone,
        mtu=jNone,
        intf_mode=jNone,
        duplex=jNone,
        arp_req_retries=jNone,
        vlan=jNone,
        vlan_id=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        intf_count=jNone,
        vlan_tpid=jNone,
        vlan_id_repeat_count=jNone,
        arp_on_linkup=jNone,
        transmit_mode=jNone,
        flow_control=jNone,
        type_a_ordered_sets=jNone,
        fault_type=jNone,
        block_mode=jNone,
        resolve_gateway_mac=jNone,
        gateway_mac=jNone,
        priority0=jNone,
        priority1=jNone,
        priority2=jNone,
        priority3=jNone,
        priority4=jNone,
        priority5=jNone,
        priority6=jNone,
        priority7=jNone,
        gre_count=jNone,
        gre_dst_ip_addr=jNone,
        gre_dst_ip_addr_step=jNone,
        gre_checksum_enable=jNone,
        gre_key_in=jNone,
        gre_key_out=jNone,
        gre_seq_enable=jNone):

    """
    :param rt_handle:       RT object
    :param arp_send_req - <1|0>
    :param autonegotiation - <1|0>
    :param clocksource - <internal|loop|external>
    :param framing - <sonet|sdh>
    :param gateway
    :param gateway_step
    :param internal_ppm_adjust - <-100-100>
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param ipv6_gateway_step
    :param ipv6_intf_addr
    :param ipv6_intf_addr_step
    :param ipv6_prefix_length - <0-128>
    :param qinq_incr_mode - <both|inner|outer>
    :param speed
    :param intf_prefix_len - <1-32>
    :param src_mac_addr
    :param port_handle
    :param mode - <config|modify|destroy>
    :param handle
    :param ipv6_gateway
    :param topology_name
    :param device_group_name
    :param src_mac_addr_step
    :param phy_mode - <copper|fiber>
    :param mtu - <68-9216>
    :param intf_mode - <ethernet|pos_hdlc|pos_ppp|atm|fc>
    :param duplex - <full|half>
    :param arp_req_retries - <0-100>
    :param vlan
    :param vlan_id
    :param vlan_id_step
    :param vlan_user_priority
    :param intf_count
    :param vlan_tpid
    :param vlan_id_repeat_count
    :param arp_on_linkup - <true:1|false:0>
    :param transmit_mode - <RATE_BASED:advanced|PORT_BASED:stream>
    :param flow_control - <true:1|flase:0>
    :param type_a_ordered_sets - <REMOTE:remote_fault|LOCAL:local_fault|RESET>
    :param fault_type - <CONTINUOUS>
    :param block_mode
    :param resolve_gateway_mac - <true:1|false:0>
    :param gateway_mac
    :param priority0 - <0|1>
    :param priority1 - <0|1>
    :param priority2 - <0|1>
    :param priority3 - <0|1>
    :param priority4 - <0|1>
    :param priority5 - <0|1>
    :param priority6 - <0|1>
    :param priority7 - <0|1>
    :param gre_count
    :param gre_dst_ip_addr
    :param gre_dst_ip_addr_step
    :param gre_checksum_enable
    :param gre_key_in
    :param gre_key_out
    :param gre_seq_enable


    Spirent Returns:
    {
        "handle": "host1",
        "handles": {
            "ipv4": "host1",
            "ipv6": "host2"
        },
        "ipv4_handle": "host1",
        "ipv6_handle": "host2",
        "status": "1"
    }

    IXIA Returns:
    {
        "ethernet_handle": "/topology:1/deviceGroup:1/ethernet:1",
        "handles": {
            "ipv4": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1",
            "ipv6": "/topology:1/deviceGroup:2/ethernet:1/ipv6:1"
        },
        "interface_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:1 /topology:1/deviceGroup:1/ethernet:1/item:1",
        "ipv4_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1",
        "ipv6_handle": "/topology:1/deviceGroup:2/ethernet:1/ipv6:1",
        "status": "1"
    }

    Common Return Keys:
        "handles"
        "ipv4_handle"
        "ipv6_handle"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config
    global link_local
    args = dict()
    n_args = dict()
    args['arp_send_req'] = arp_send_req
    args['autonegotiation'] = autonegotiation
    args['clocksource'] = clocksource
    args['framing'] = framing
    args['gateway_ip_addr'] = gateway
    args['gateway_ip_addr_step'] = gateway_step
    args['internal_ppm_adjust'] = internal_ppm_adjust
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_addr_step'] = intf_ip_addr_step
    args['gateway_ipv6_addr_step'] = ipv6_gateway_step
    args['intf_ipv6_addr'] = ipv6_intf_addr
    args['intf_ipv6_addr_step'] = ipv6_intf_addr_step
    args['intf_ipv6_prefix_len'] = ipv6_prefix_length
    args['qinq_incr_mode'] = qinq_incr_mode
    args['speed'] = speed
    args['intf_prefix_len'] = intf_prefix_len
    args['mac_addr'] = src_mac_addr
    args['mac_addr_step'] = src_mac_addr_step
    args['port_handle'] = port_handle
    args['mode'] = mode
    args['handle'] = handle
    args['gateway_ipv6_addr'] = ipv6_gateway
    args['phy_mode'] = phy_mode
    args['mtu'] = mtu
    args['enable_ping_response'] = 1
    args['intf_mode'] = intf_mode
    args['duplex'] = duplex
    args['arp_req_retries'] = arp_req_retries
    args['vlan'] = vlan
    args['vlan_id_step'] = vlan_id_step
    args['vlan_id_repeat_count'] = vlan_id_repeat_count
    args['intf_count'] = intf_count
    args['arp_on_linkup'] = arp_on_linkup
    args['flow_control'] = flow_control
    args['vlan_tpid'] = vlan_tpid 
    args['transmit_mode'] = transmit_mode
    args['block_mode'] = block_mode
    args['resolve_gateway_mac'] = resolve_gateway_mac
    args['gateway_mac'] = gateway_mac
    args['priority0'] = priority0
    args['priority1'] = priority1
    args['priority2'] = priority2
    args['priority3'] = priority3
    args['priority4'] = priority4
    args['priority5'] = priority5
    args['priority6'] = priority6
    args['priority7'] = priority7
    args['gre_count'] = gre_count
    args['gre_dst_addr'] = gre_dst_ip_addr
    args['gre_dst_addr_step'] = gre_dst_ip_addr_step
    args['gre_checksum'] =  gre_checksum_enable
    args['gre_in_key'] = gre_key_in
    args['gre_out_key'] = gre_key_out
    args['gre_seqnum_enabled'] = gre_seq_enable

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_interface_config.__doc__, **args)
    n_args = get_arg_value(rt_handle, j_interface_config.__doc__, **n_args)
    
    if 'transmit_mode' in args:
        args['scheduling_mode'] = args['transmit_mode']
        del args['transmit_mode']

    if 'mtu' in args:
        args['control_plane_mtu'] = args['mtu']
        del args['mtu']

    if 'intf_count' in args:
        args['count'] = args['intf_count']
        del args['intf_count']

    if 'arp_on_linkup' in  args.keys():
        del args['arp_on_linkup']
        if int(arp_on_linkup) == 1:
            n_args['auto_arp_enable'] = 'true'
        else:
            n_args['auto_arp_enable'] = 'false'
        rt_handle.invoke('arp_nd_config', **n_args)

    if 'vlan_id_step' not in args.keys():
        vlan_id_step = 0

    if intf_count != jNone:
        args['expand'] = 'true'

    if 'block_mode' in args.keys():
        if int(args['block_mode']) == 1:
            args['block_mode'] = 'multiple_device_per_block'
        else:
            args['block_mode'] = 'one_device_per_block'
    if device_group_name != jNone and block_mode != jNone:
        args['name'] = device_group_name

    if 'gre_dst_addr' in args.keys():
        args['lower_encap'] = 'gre'
        args['gre_tnl_type'] = '4'

    if 'gre_dst_addr' in args.keys() and 'gre_count' in args.keys():
        args['count'] = gre_count
        del args['gre_count']

    counter = 1
    string = "intf_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "intf_" + str(counter)
    global_config[string] = []

    nargs = dict()

    vlan_tpid_values = {'0x8100' : '33024', '0x88a8' : '34984', '0x9100' : '37120', '0x9200' : '37376', '0x9300' : '37632'}
    if 'vlan_tpid' in args:
        if isinstance(args['vlan_tpid'], list):
            for value in args['vlan_tpid']:
                if value not in vlan_tpid_values:
                    raise ValueError("vlan_tpid value "+value+" is not supported by JHLT")
        elif args['vlan_tpid'] not in vlan_tpid_values:
            raise ValueError("vlan_tpid value "+args['vlan_tpid']+" is not supported by JHLT")

    intf_conf_args = ['arp_send_req', 'autonegotiation', 'clocksource', 'framing', 'internal_ppm_adjust', 'speed', 'phy_mode', 'control_plane_mtu', 'arp_req_retries', 'intf_mode', 'duplex', 'flow_control', 'scheduling_mode', 'priority0', 'priority1', 'priority2', 'priority3', 'priority4', 'priority5', 'priority6', 'priority7'] 

    for ic_args in intf_conf_args:
        if ic_args in args:
            nargs[ic_args] = args[ic_args]
            del args[ic_args]
    args['encapsulation'] = 'ethernet_ii'
    if len(nargs):
        nargs['mode'] = 'modify'
        if 'port_handle' in args:
            nargs['port_handle'] = args['port_handle']
    ret = []
    handle_list = dict()
    __check_and_raise(mode)

    if 'vlan' in args:
        if 'vlan_id_step' not in args.keys() and not isinstance(vlan_id, list) and not isinstance(vlan_user_priority, list) and not isinstance(vlan_tpid, list):
            args['encapsulation'] = 'ethernet_ii_vlan'
            del args['vlan']
            args['vlan_id'] = vlan_id
            args['vlan_tpid'] = vlan_tpid_values[args['vlan_tpid']] if 'vlan_tpid' in args else vlan_tpid
            args['vlan_user_pri'] = vlan_user_priority
            args['count'] = intf_count

        elif 'vlan_id_step' in args.keys() and 'vlan_id_repeat_count' not in args.keys() and not isinstance(vlan_id, list) and not isinstance(vlan_id_step, list) and not isinstance(vlan_user_priority, list) and not isinstance(vlan_tpid, list):
            args['encapsulation'] = 'ethernet_ii_vlan'
            del args['vlan']
            if 'count' in args:
                del args['count']
            args['vlan_id'] = vlan_id
            args['vlan_tpid'] = vlan_tpid_values[args['vlan_tpid']] if 'vlan_tpid' in args else vlan_tpid
            args['vlan_user_pri'] = vlan_user_priority
            args['vlan_id_count'] = intf_count
        elif 'vlan_id_repeat_count' in args.keys() and 'vlan_id_step' in args.keys() and not isinstance(vlan_id, list) and not isinstance(vlan_id_step, list) and not isinstance(vlan_user_priority, list) and not isinstance(vlan_tpid, list):
            args['encapsulation'] = 'ethernet_ii_vlan'
            del args['vlan']
            del args['vlan_id_repeat_count']
            args['vlan_id'] = vlan_id
            args['vlan_tpid'] = vlan_tpid_values[args['vlan_tpid']] if 'vlan_tpid' in args else vlan_tpid
            args['vlan_user_pri'] = vlan_user_priority
            args['count'] = vlan_id_repeat_count
            args['vlan_id_count'] = int(int(intf_count)/int(vlan_id_repeat_count))
        elif isinstance(vlan_id_step, list) or isinstance(vlan_id, list) or isinstance(vlan_user_priority, list) or isinstance(vlan_tpid, list):
            if len(vlan_id) == 2 or len(vlan_id_step) == 2 or len(vlan_tpid) == 2 or (vlan_user_priority) == 2:
                args['encapsulation'] = 'ethernet_ii_qinq'
                del args['vlan']
                if 'count' in args.keys():
                    del args['count']
                args['vlan_id_count'] = 1
                if isinstance(vlan_id_step, list):
                    args['vlan_id_step'] = vlan_id_step[1]
                    args['vlan_outer_id_step'] = vlan_id_step[0]
                if isinstance(vlan_id, list):
                    args['vlan_outer_id'] = vlan_id[0]
                    args['vlan_id'] = vlan_id[1]
                args['vlan_outer_id_count'] = intf_count
                if isinstance(vlan_tpid, list):
                    args['vlan_tpid'] = vlan_tpid_values[vlan_tpid[1]] if 'vlan_tpid' in args else vlan_tpid[1] 
                    args['vlan_outer_tpid'] = vlan_tpid_values[vlan_tpid[0]] if 'vlan_tpid' in args else vlan_tpid[0]
                if isinstance(vlan_user_priority, list):
                    args['vlan_user_pri'] = vlan_user_priority[1]
                    args['vlan_outer_user_pri'] = vlan_user_priority[0]
            if len(vlan_id) == 3:
                args['encapsulation'] = 'ethernet_ii_mvlan'
                del args['vlan']
                del args['count']
                args['vlan_id'] = vlan_id[1]
                args['vlan_id_count'] = 1
                args['vlan_id_step'] = vlan_id_step[1]
                args['vlan_outer_id'] = vlan_id[0]
                args['vlan_outer_id_count'] = intf_count
                args['vlan_outer_id_step'] = vlan_id_step[0]
                args['vlan_id_list'] = vlan_id[2]
                args['vlan_id_count_list'] = 1
                args['vlan_id_step_list'] = vlan_id_step[2]
                if isinstance(vlan_tpid, list):
                    args['vlan_tpid'] = vlan_tpid_values[vlan_tpid[1]] if 'vlan_tpid' in args else vlan_tpid[1]
                    args['vlan_outer_tpid'] = vlan_tpid_values[vlan_tpid[0]] if 'vlan_tpid' in args else vlan_tpid[0]
                    args['vlan_tpid_list'] = vlan_tpid_values[vlan_tpid[2]] if 'vlan_tpid' in args else vlan_tpid[2]
                if isinstance(vlan_user_priority, list):
                    args['vlan_user_pri'] = vlan_user_priority[1]
                    args['vlan_outer_user_pri'] = vlan_user_priority[0]
                    args['vlan_user_pri_list'] = vlan_user_priority[2]

        for key in list(args.keys()):
            if args[key] == jNone:
                del args[key]
    if mode == 'modify':
        __check_and_raise(handle)
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))

        if 'vlan' in args:
            args['encapsulation'] = 'ethernet_ii_vlan'
            del args['vlan']

        for hndl in handle:
            status = 1
            new_ret = dict()
            for hnd in global_config[hndl]:
                if hnd in handle_list:
                    continue
                else:
                    handle_list[hnd] = 1
                args['handle'] = hnd
                newer_ret = rt_handle.invoke('emulation_device_config', **args)
                if 'status' in newer_ret:
                    if newer_ret['status'] == 0:
                        status = 0
                if 'handle' in newer_ret:
                    global_config[string].extend([newer_ret['handle']])
                for key in newer_ret:
                    try:
                        new_ret[key]
                    except:
                        new_ret[key] = []
                    new_ret[key].append(newer_ret[key])
            for key in new_ret:
                if len(new_ret[key]) == 1:
                    new_ret[key] = new_ret[key][0]
            if 'status' in new_ret:
                new_ret['status'] = status
            if 'handles' in new_ret:
                new_ret['handles'] = string
            if new_ret:
                ret.append(new_ret)
    elif mode == 'config':
        __check_and_raise(port_handle)
        try:
            handle_map[port_handle]
        except KeyError:
            handle_map[port_handle] = []

        args['mode'] = 'create'
        if 'intf_ipv6_addr' in args and 'intf_ip_addr' in args:
            args['ip_version'] = 'ipv46'
        elif 'intf_ipv6_addr' in args:
            args['ip_version'] = 'ipv6'
        elif 'intf_ip_addr' in args:
            args['ip_version'] = 'ipv4'

        if 'intf_ipv6_addr' in args:
            args['link_local_ipv6_addr'] = str(link_local)
            if intf_count != jNone:
                link_local = link_local + int(intf_count)
            else:
                link_local = link_local + 1
 #       if vlan not in args.keys():
 #           args['encapsulation'] = 'ethernet_ii'
        ret.append(rt_handle.invoke('emulation_device_config', **args))
        if "expand" in args.keys():
            global_config[string] = ret[-1]['handle_list'].split()
        else:
            global_config[string] = [ret[-1]['handle']]
        ret[-1]['handles'] = string
        handle_map[port_handle].extend(global_config[string])
        handle_map[string] = port_handle

        session_map[ret[-1]['handles']] = dict()
        if 'gateway_ip_addr' in args:
            session_map[ret[-1]['handles']]['gateway_ip_addr'] = args['gateway_ip_addr']
        if 'gateway_ip_addr_step' in args:
            session_map[ret[-1]['handles']]['gateway_ip_addr_step'] = args['gateway_ip_addr_step']
        if 'intf_ip_addr' in args:
            session_map[ret[-1]['handles']]['intf_ip_addr'] = args['intf_ip_addr']
        if 'intf_ip_addr_step' in args:
            session_map[ret[-1]['handles']]['intf_ip_addr_step'] = args['intf_ip_addr_step']
        if 'mac_addr' in args:
            session_map[ret[-1]['handles']]['src_mac_addr'] = args['mac_addr']
        if 'mac_addr_step' in args:
            session_map[ret[-1]['handles']]['src_mac_addr_step'] = args['mac_addr_step']
        if 'gateway_ipv6_addr' in args:
            session_map[ret[-1]['handles']]['gateway_ipv6_addr'] = args['gateway_ipv6_addr']
        if 'gateway_ipv6_addr_step' in args:
            session_map[ret[-1]['handles']]['gateway_ipv6_addr_step'] = args['gateway_ipv6_addr_step']
        if 'intf_ipv6_addr' in args:
            session_map[ret[-1]['handles']]['intf_ipv6_addr'] = args['intf_ipv6_addr']
        if 'intf_ipv6_addr_step' in args:
            session_map[ret[-1]['handles']]['intf_ipv6_addr_step'] = args['intf_ipv6_addr_step']

        if 'intf_ipv6_addr' in args and 'intf_ip_addr' in args:
            handle = ret[-1]['handles']
            ret[-1]['handles'] = dict()
            ret[-1]['handles']['ipv4'] = handle
            ret[-1]['ipv4_handle'] = handle
            ret[-1]['handles']['ipv6'] = handle
            ret[-1]['ipv6_handle'] = handle

    elif mode == 'destroy':
       # __check_and_raise(port_handle)
        if port_handle == jNone:
           __check_and_raise(handle)
        else:
           __check_and_raise(port_handle)
        margs = dict()
        if handle != jNone:
            if not isinstance(handle, list):
                handle = [handle]
            handle = list(set(handle))
            for hndl in handle:
                if hndl in global_config.keys():
                    for hnd in global_config[hndl]:
                        if not hnd.startswith('dhcpv4block') and not hnd.startswith('dhcpv6block'):
                            margs['handle'] = hnd
                            margs['mode'] = 'delete'
                            ret.append(rt_handle.invoke('emulation_device_config', **margs))
                        else:
                            margs['handle'] = hnd
                            margs['mode'] = 'reset'
                            ret.append(rt_handle.invoke('emulation_dhcp_group_config', **margs))
                else:
                    if not hndl.startswith('dhcpv4block') and not hndl.startswith('dhcpv6block'):
                        margs['handle'] = hndl
                        margs['mode'] = 'delete'
                        ret.append(rt_handle.invoke('emulation_device_config', **margs))
                    else:
                        margs['handle'] = hndl
                        margs['mode'] = 'reset'
                        ret.append(rt_handle.invoke('emulation_dhcp_group_config', **margs))
        elif port_handle != jNone:
            if not isinstance(port_handle, list):
                port_handle = [port_handle]
            port_handle = list(set(port_handle))
            for port in port_handle:
                margs['handle'] = handle_map[port]
                margs['mode'] = 'delete'
                try:
                    ret.append(rt_handle.invoke('emulation_device_config', **margs))
                except:
                    pass
                handle_map[port] = []

    if len(nargs):
        if mode == 'modify':
            for hndl in handle:
                for hnd in global_config[hndl]:
                    nargs['port_handle'] = handle_map[hndl]
                    rt_handle.invoke('interface_config', **nargs)
        else:
            rt_handle.invoke('interface_config', **nargs)


    if type_a_ordered_sets != jNone:
        if type_a_ordered_sets == 'REMOTE' or type_a_ordered_sets == 'remote_fault':
            if fault_type !='CONTINUOUS' :
                rt_handle.invoke('invoke', cmd='stc::perform L2TestStartLinkFaultSignallingCommand -Faultmode' + " " + 'REMOTE')
        elif type_a_ordered_sets == 'LOCAL' or type_a_ordered_sets == 'local_fault':
            rt_handle.invoke('invoke', cmd='stc::perform L2TestStartLinkFaultSignallingCommand -Faultmode' + " " + 'LOCAL')
        elif type_a_ordered_sets == 'RESET':
            rt_handle.invoke('invoke', cmd='stc::perform L2TestStartLinkFaultSignallingCommand -Faultmode' + " " + 'RESET')
        else:
            raise ValueError("INVALID VALUE , PLEASE PROVIDE THE CORRECT VALUE")

    if fault_type != jNone:
        if fault_type == 'CONTINUOUS':
            rt_handle.invoke('invoke', cmd='stc::perform L2TestStartLinkFaultSignallingCommand -FaultType' + " " + 'CONTINUOUS')
        else:
            raise ValueError("INVALID VALUE , PLEASE PROVIDE THE CORRECT VALUE")
        if fault_type == 'CONTINUOUS':
            if type_a_ordered_sets == 'REMOTE' or type_a_ordered_sets == 'remote_fault':
                rt_handle.invoke('invoke', cmd='stc::perform L2TestStartLinkFaultSignallingCommand -Faultmode' + " " + 'REMOTE')


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]
    if 'intf_ip_addr' in args and 'intf_ipv6_addr' not in args:
        block_hndls = ret['handles']
        if not isinstance(block_hndls, list):
            block_hndls = [block_hndls]
        block_hndls = list(set(block_hndls))
        ipv4_hndls = []
        for hndl in block_hndls:
            for hnd in global_config[hndl]:
                ipv4_hndls.append(hnd)
        ret['intf_handles'] = ipv4_hndls

    if 'intf_ipv6_addr' in args and 'intf_ip_addr' not in args:
        block_hndls = ret['handles']
        if not isinstance(block_hndls, list):
            block_hndls = [block_hndls]
        block_hndls = list(set(block_hndls))
        ipv6_hndls = []
        for hndl in block_hndls:
            for hnd in global_config[hndl]:
                ipv6_hndls.append(hnd)
        ret['intf_handles'] = ipv6_hndls

    if 'intf_ip_addr' in args and 'intf_ipv6_addr' in args:
        block_hndls = ret['handles']
        ret['intf_handles'] = {}
        ret['intf_handles'] = {}
        for k in block_hndls.keys():
            if not isinstance(block_hndls[k], list):
                block_hndls1 = [block_hndls[k]]
            block_hndls1 = list(set(block_hndls1))
            ipv4_6hndls = []
            for hndl in block_hndls1:
                for hnd in global_config[hndl]:
                    ipv4_6hndls.append(hnd)
                    if k == 'ipv4':
                        ret['intf_handles']['ipv4'] = ipv4_6hndls
                    if k == 'ipv6':
                        ret['intf_handles']['ipv6'] = ipv4_6hndls
    if gre_dst_ip_addr != jNone:
        ret['gre_handle'] = ret['handles']
    # ***** End of Return Value Modification *****
    return ret

def j_l2tp_config(
        rt_handle,
        attempt_rate=jNone,
        auth_mode=jNone,
        auth_req_timeout=jNone,
        config_req_timeout=jNone,
        echo_req_interval=jNone,
        hello_interval=jNone,
        hostname=jNone,
        l2tp_src_count=jNone,
        max_auth_req=jNone,
        max_ipcp_req=jNone,
        max_terminate_req=jNone,
        l2tp_node_type=jNone,
        num_tunnels=jNone,
        redial_max=jNone,
        redial_timeout=jNone,
        rws=jNone,
        secret=jNone,
        sessions_per_tunnel=jNone,
        udp_src_port=jNone,
        vlan_count=jNone,
        vlan_id=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        wildcard_bang_end=jNone,
        wildcard_bang_start=jNone,
        wildcard_dollar_end=jNone,
        wildcard_dollar_start=jNone,
        wildcard_pound_end=jNone,
        wildcard_pound_start=jNone,
        wildcard_question_end=jNone,
        wildcard_question_start=jNone,
        handle=jNone,
        username=jNone,
        password=jNone,
        l2_encap=jNone,
        l2tp_src_addr=jNone,
        l2tp_dst_addr=jNone,
        l2tp_mac_addr=jNone,
        ppp_server_ip=jNone,
        ppp_client_ip=jNone,
        ppp_client_step=jNone,
        port_handle=jNone,
        vlan_id_outer=jNone,
        vlan_id_step_outer=jNone,
        vlan_user_priority_outer=jNone,
        mode=jNone):
    """
    :param rt_handle:       RT object
    :param attempt_rate - <1-1000>
    :param auth_mode - <none|pap|chap|pap_or_chap>
    :param auth_req_timeout - <1-65535>
    :param config_req_timeout - <1-120>
    :param echo_req_interval - <1-65535>
    :param hello_interval - <1-180>
    :param hostname
    :param l2tp_src_count - <1-112>
    :param max_auth_req - <1-65535>
    :param max_ipcp_req - <1-255> 
    :param max_terminate_req - <1-1000>
    :param l2tp_node_type - <lac|lns>
    :param num_tunnels - <1-32000>
    :param redial_max - <1-20>
    :param redial_timeout - <1-20>
    :param rws - <1-2048>
    :param secret
    :param sessions_per_tunnel - <1-64000> 
    :param udp_src_port - <1-65535>
    :param vlan_count - <1-4094> 
    :param vlan_id - <1-4095>
    :param vlan_id_step - <0-4093>
    :param vlan_user_priority - <0-7>
    :param wildcard_bang_end - <0-65535>
    :param wildcard_bang_start - <0-65535>
    :param wildcard_dollar_end - <0-65535>
    :param wildcard_dollar_start - <0-65535>
    :param wildcard_pound_end - <0-65535>
    :param wildcard_pound_start - <0-65535>
    :param wildcard_question_end - <0-65535>
    :param wildcard_question_start - <0-65535>
    :param handle
    :param username
    :param password
    :param l2_encap - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq|atm_snap|atm_vc_mux>
    :param l2tp_src_addr
    :param l2tp_dst_addr
    :param l2tp_mac_addr
    :param ppp_server_ip
    :param ppp_client_ip
    :param ppp_client_step
    :param port_handle
    :param vlan_id_outer - <1-4095>
    :param vlan_id_step_outer - <0-4093>
    :param vlan_user_priority_outer - <0-7>
    :param mode - <create|modify|delete:remove>

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "procName": "l2tp_config",
        "status": "1"
    }

    IXIA Returns:
    {
        "ethernet_handle": "/topology:1/deviceGroup:1/ethernet:1",
        "handle": "/range:HLAPI0",
        "handles": "/range:HLAPI0",
        "ipv4_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1",
        "lns_auth_credentials_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/lnsAuthCredentials",
        "lns_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1",
        "pppox_server_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/pppoxserver:1",
        "pppox_server_sessions_handle": "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/pppoxserver:1/pppoxServerSessions",
        "status": "1"
    }
    {
        "ethernet_handle": "/topology:2/deviceGroup:1/deviceGroup:1/ethernet:1 /topology:2/deviceGroup:1/ethernet:1",
        "handle": "/range:HLAPI1",
        "handles": "/range:HLAPI1",
        "ipv4_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1",
        "lac_handle": "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/lac:1",
        "pppox_client_handle": "/topology:2/deviceGroup:1/deviceGroup:1/ethernet:1/pppoxclient:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['attempt_rate'] = attempt_rate
    args['auth_mode'] = auth_mode
    args['auth_req_timeout'] = auth_req_timeout
    args['config_req_timeout'] = config_req_timeout
    args['echo_req_interval'] = echo_req_interval
    args['hello_interval'] = hello_interval
    args['hostname'] = hostname
    args['l2tp_src_count'] = l2tp_src_count
    args['max_auth_req'] = max_auth_req
    args['max_ipcp_req'] = max_ipcp_req
    args['max_terminate_req'] = max_terminate_req
    args['l2tp_node_type'] = l2tp_node_type
    args['num_tunnels'] = num_tunnels
    args['redial_max'] = redial_max
    args['redial_timeout'] = redial_timeout
    args['rws'] = rws
    args['secret'] = secret
    args['sessions_per_tunnel'] = sessions_per_tunnel
    args['udp_src_port'] = udp_src_port
    args['vlan_count'] = vlan_count
    args['vlan_id'] = vlan_id
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['wildcard_bang_end'] = wildcard_bang_end
    args['wildcard_bang_start'] = wildcard_bang_start
    args['wildcard_dollar_end'] = wildcard_dollar_end
    args['wildcard_dollar_start'] = wildcard_dollar_start
    args['wildcard_pound_end'] = wildcard_pound_end
    args['wildcard_pound_start'] = wildcard_pound_start
    args['wildcard_question_end'] = wildcard_question_end
    args['wildcard_question_start'] = wildcard_question_start
    args['handle'] = handle
    args['username'] = username
    args['password'] = password
    args['l2_encap'] = l2_encap
    args['l2tp_src_addr'] = l2tp_src_addr
    args['l2tp_dst_addr'] = l2tp_dst_addr
    args['l2tp_mac_addr'] = l2tp_mac_addr
    args['ppp_server_ip'] = ppp_server_ip
    args['ppp_client_ip'] = ppp_client_ip
    args['ppp_client_step'] = ppp_client_step
    args['port_handle'] = port_handle
    args['vlan_id_outer'] = vlan_id_outer
    args['vlan_id_step_outer'] = vlan_id_step_outer
    args['vlan_user_priority_outer'] = vlan_user_priority_outer
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_l2tp_config.__doc__, **args)
   
    if 'mode' in args:
        args['config_mode'] = args['mode']
        del args['mode']

    if 'l2tp_node_type' in args:
        args['mode'] = args['l2tp_node_type']
        del args['l2tp_node_type']    
    
    if "port_handle" not in args.keys():
        __check_and_raise(handle)
    else:
        __check_and_raise(port_handle)

    if l2tp_node_type == 'lns':
        args['l2tp_src_addr'] = l2tp_dst_addr
        args['l2tp_dst_addr'] = l2tp_src_addr

    counter = 1
    string = "l2tp_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "l2tp_" + str(counter)
    global_config[string] = []

    ret = []
    if 'handle' in args.keys():
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    args['handle'] = hnd
                    if mode == 'modify'  or mode == 'delete' or mode == 'remove':
                        l2tp_handle = rt_handle.invoke('invoke', cmd='stc::get '+hnd+' -AffiliatedPort')
                        args['port_handle'] = l2tp_handle
                    result = rt_handle.invoke('l2tp_config', **args)
                    if result.get('handle'):
                        global_config[string].extend(result['handle'])
                        result['handles'] = string
                    if mode == 'create':
                        handle_map[hnd] = handle_map.get(hnd, [])
                        handle_map[hnd].extend(global_config[string])
                        handle_map[string] = hnd
                    ret.append(result)
            else:
                args['handle'] = hndl
                if mode == 'modify'  or mode == 'delete' or mode == 'remove':
                    args['port_handle'] = hndl
                result = rt_handle.invoke('l2tp_config', **args)
                if result.get('handle'):
                    global_config[string].extend(result['handle'])
                    result['handles'] = string
                if mode == 'create':
                    handle_map[hndl] = handle_map.get(hndl, [])
                    handle_map[hndl].extend(global_config[string])
                    handle_map[string] = hndl
                ret.append(result)
    elif 'port_handle' in args.keys():
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        result = rt_handle.invoke('l2tp_config', **args)
        if result.get('handle'):
            global_config[string].extend([result['handle']])
            result['handles'] = string
        for hand in port_handle:
            handle_map[hand] = handle_map.get(hand, [])
            handle_map[hand].extend(global_config[string])
            handle_map[string] = hand
        ret.append(result)

# ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

 
def j_l2tp_control(rt_handle, action=jNone, handle=jNone):
    """
    :param rt_handle:       RT object
    :param action - <connect|disconnect|retry>
    :param handle

    Spirent Returns:
    {
        "procName": "l2tp_control",
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_l2tp_control.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    ret= []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                ret.append(rt_handle.invoke('l2tp_control', **args))
        else:
            args['handle'] = hndl
            ret.append(rt_handle.invoke('l2tp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_l2tp_stats(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode

    Spirent Returns:
    {
        "aggregate": {
            "avg_setup_time": "8",
            "cdn_rx": "0",
            "cdn_tx": "0",
            "chap_rx": "2",
            "chap_tx": "1",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "disconnect_success": "0",
            "disconnecting": "0",
            "echo_reply_rx": "0",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "hello_rx": "0",
            "hello_tx": "0",
            "iccn_rx": "0",
            "iccn_tx": "1",
            "icrp_rx": "1",
            "icrp_tx": "0",
            "icrq_rx": "0",
            "icrq_tx": "1",
            "idle": "0",
            "ipcp_rx": "3",
            "ipcp_tx": "3",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "max_setup_time": "8",
            "min_setup_time": "8",
            "retry_count": "0",
            "scccn_rx": "0",
            "scccn_tx": "1",
            "sccrp_rx": "1",
            "sccrp_tx": "0",
            "sccrq_rx": "0",
            "sccrq_tx": "1",
            "session_status": "CONNECTED",
            "sessions_down": "0",
            "sessions_up": "1",
            "sli_rx": "0",
            "sli_tx": "0",
            "stopccn_rx": "0",
            "stopccn_tx": "0",
            "success_setup_rate": "122",
            "term_ack_rx": "0",
            "term_ack_txv": "0",
            "term_req_rx": "0",
            "term_req_tx": "0",
            "tunnels_up": "1",
            "tx_pkt_acked": "2",
            "wen_rx": "0",
            "wen_tx": "0",
            "zlb_rx": "2",
            "zlb_tx": "0"
        },
        "handles": "host2",
        "procName": "l2tp_status",
        "session": {
            "1": {
                "1": {
                    "cdn_rx": "0",
                    "cdn_tx": "0",
                    "iccn_rx": "0",
                    "iccn_tx": "1",
                    "icrp_rx": "1",
                    "icrp_tx": "0",
                    "icrq_rx": "0",
                    "icrq_tx": "1"
                }
            },
            "host2": {
                "1": {
                    "cdn_rx": "0",
                    "cdn_tx": "0",
                    "iccn_rx": "0",
                    "iccn_tx": "1",
                    "icrp_rx": "1",
                    "icrp_tx": "0",
                    "icrq_rx": "0",
                    "icrq_tx": "1"
                }
            }
        },
        "status": "1",
        "tunnel": {
            "1": {
                "hello_rx": "0",
                "hello_tx": "0",
                "scccn_rx": "0",
                "scccn_tx": "1",
                "sccrp_rx": "1",
                "sccrp_tx": "0",
                "sli_rx": "0",
                "sli_tx": "0",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tx_pkt_acked": "0",
                "wen_rx": "0",
                "wen_tx": "0"
            }
        }
    }

    IXIA Returns:
    {
        "/topology:2/deviceGroup:1/deviceGroup:1/ethernet:1/pppoxclient:1/item:1": {
            "session": {
                "ac_cookie": "Not Available",
                "ac_cookie_tag_rx": "0",
                "ac_generic_error_occured": "False",
                "ac_mac_addr": "Not Available",
                "ac_name": "Not Available",
                "ac_offers_rx": "0",
                "ac_system_error_occured": "False",
                "ac_system_error_tag_rx": "0",
                "auth_id": "user",
                "auth_latency": "1462",
                "auth_password": "secret",
                "auth_protocol_rx": "CHAP",
                "auth_protocol_tx": "None",
                "auth_total_rx": "2",
                "auth_total_tx": "1",
                "avg_setup_time": "12646",
                "call_id": "1",
                "call_state": "Established",
                "chap_auth_chal_rx": "1",
                "chap_auth_fail_rx": "0",
                "chap_auth_role": "Peer",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "cookie": "Not Available",
                "cookie_len": "0",
                "cumulative_setup_failed": "0",
                "cumulative_setup_initiated": "1",
                "cumulative_setup_succeeded": "1",
                "cumulative_teardown_failed": "0",
                "cumulative_teardown_succeeded": "0",
                "data_ns": "0",
                "destination_ip": "1.1.1.1",
                "destination_port": "1701",
                "dns_server_list": "Not Available",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "gateway_ip": "1.1.1.1",
                "generic_error_tag_rx": "0",
                "host_mac_addr": "Not Available",
                "host_name": "Not Available",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "1",
                "ipcp_cfg_nak_tx": "0",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "1",
                "ipcp_cfg_req_tx": "2",
                "ipcp_latency": "3454",
                "ipcp_state": "NCP Open",
                "ipv6_addr": "0:0:0:0:0:0:0:0",
                "ipv6_prefix_len": "0",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_latency": "0",
                "ipv6cp_router_adv_rx": "0",
                "ipv6cp_state": "NCP Disable",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_latency": "1485",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "local_ip_addr": "1.1.1.3",
                "local_ipv6_iid": "Not Available",
                "loopback_detected": "False",
                "magic_no_negotiated": "True",
                "magic_no_rx": "1816763613",
                "magic_no_tx": "1022819482",
                "mru": "1500",
                "mtu": "1500",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "negotiation_end_ms": "0",
                "negotiation_start_ms": "0",
                "padi_timeouts": "0",
                "padi_tx": "0",
                "pado_rx": "0",
                "padr_timeouts": "0",
                "padr_tx": "0",
                "pads_rx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "peer_call_id": "1",
                "peer_id": "1",
                "peer_ipv6_iid": "Not Available",
                "ppp_close_mode": "None",
                "ppp_state": "PPP Connected",
                "pppoe_discovery_latency": "0",
                "pppoe_session_id": "0",
                "pppox_state": "Init",
                "primary_wins_server": "0.0.0.0",
                "relay_session_id_tag_rx": "0",
                "remote_ip_addr": "1.1.1.1",
                "secondary_wins_server": "0.0.0.0",
                "service_name": "Not Available",
                "service_name_error_tag_rx": "0",
                "source_ip": "1.1.1.2",
                "source_port": "1701",
                "status": "up",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "total_bytes_rx": "0",
                "total_bytes_tx": "0",
                "tunnel_id": "1",
                "tunnel_state": "Tunnel established",
                "vendor_specific_tag_rx": "0"
            }
        },
        "1/25/1": {
            "aggregate": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "chap_auth_chal_rx": "1",
                "chap_auth_fail_rx": "0",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "client_interfaces_in_ppp_negotiation": "0",
                "client_session_avg_latency": "12646.00",
                "client_session_max_latency": "12646",
                "client_session_min_latency": "12646",
                "client_tunnels_up": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "cumulative_setup_failed": "0",
                "cumulative_setup_initiated": "1",
                "cumulative_setup_succeeded": "1",
                "cumulative_teardown_failed": "0",
                "cumulative_teardown_succeeded": "0",
                "duplicate_rx": "0",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "0",
                "iccn_tx": "1",
                "icrp_rx": "1",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "1",
                "in_order_rx": "2",
                "interfaces_in_pppoe_l2tp_negotiation": "0",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "1",
                "ipcp_cfg_nak_tx": "0",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "1",
                "ipcp_cfg_req_tx": "2",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_router_adv_rx": "0",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "144",
                "l2tp_tunnel_total_bytes_tx": "308",
                "lcp_avg_latency": "1485.00",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_max_latency": "1485",
                "lcp_min_latency": "1485",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "ncp_avg_latency": "3454.00",
                "ncp_max_latency": "3454",
                "ncp_min_latency": "3454",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "num_sessions": "1",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "padi_timeouts": "0",
                "padi_tx": "0",
                "pado_rx": "0",
                "padr_timeouts": "0",
                "padr_tx": "0",
                "pads_rx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "ppp_total_bytes_rx": "161",
                "ppp_total_bytes_tx": "104",
                "retransmits": "0",
                "scccn_rx": "0",
                "scccn_tx": "1",
                "sccrp_rx": "1",
                "sccrp_tx": "0",
                "sccrq_rx": "0",
                "sccrq_tx": "1",
                "sessions_failed": "0",
                "sessions_not_started": "0",
                "sessions_up": "1",
                "sli_rx": "0",
                "sli_tx": "0",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "success_setup_rate": "0",
                "teardown_failed": "0",
                "teardown_rate": "0",
                "teardown_succeeded": "0",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "total_bytes_rx": "0",
                "total_bytes_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "4",
                "tx_pkt_acked": "4",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "2",
                "zlb_tx": "0"
            }
        },
        "aggregate": {
            "cdn_rx": "0",
            "cdn_tx": "0",
            "chap_auth_chal_rx": "1",
            "chap_auth_fail_rx": "0",
            "chap_auth_rsp_tx": "1",
            "chap_auth_succ_rx": "1",
            "client_interfaces_in_ppp_negotiation": "0",
            "client_session_avg_latency": "12646.00",
            "client_session_max_latency": "12646",
            "client_session_min_latency": "12646",
            "client_tunnels_up": "1",
            "code_rej_rx": "0",
            "code_rej_tx": "0",
            "cumulative_setup_failed": "0",
            "cumulative_setup_initiated": "1",
            "cumulative_setup_succeeded": "1",
            "cumulative_teardown_failed": "0",
            "cumulative_teardown_succeeded": "0",
            "duplicate_rx": "0",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_rsp_rx": "0",
            "echo_rsp_tx": "0",
            "hello_rx": "0",
            "hello_tx": "0",
            "iccn_rx": "0",
            "iccn_tx": "1",
            "icrp_rx": "1",
            "icrp_tx": "0",
            "icrq_rx": "0",
            "icrq_tx": "1",
            "in_order_rx": "2",
            "interfaces_in_pppoe_l2tp_negotiation": "0",
            "ipcp_cfg_ack_rx": "1",
            "ipcp_cfg_ack_tx": "1",
            "ipcp_cfg_nak_rx": "1",
            "ipcp_cfg_nak_tx": "0",
            "ipcp_cfg_rej_rx": "0",
            "ipcp_cfg_rej_tx": "0",
            "ipcp_cfg_req_rx": "1",
            "ipcp_cfg_req_tx": "2",
            "ipv6cp_cfg_ack_rx": "0",
            "ipv6cp_cfg_ack_tx": "0",
            "ipv6cp_cfg_nak_rx": "0",
            "ipv6cp_cfg_nak_tx": "0",
            "ipv6cp_cfg_rej_rx": "0",
            "ipv6cp_cfg_rej_tx": "0",
            "ipv6cp_cfg_req_rx": "0",
            "ipv6cp_cfg_req_tx": "0",
            "ipv6cp_router_adv_rx": "0",
            "l2tp_calls_up": "1",
            "l2tp_tunnel_total_bytes_rx": "144",
            "l2tp_tunnel_total_bytes_tx": "308",
            "lcp_avg_latency": "1485.00",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "lcp_max_latency": "1485",
            "lcp_min_latency": "1485",
            "lcp_protocol_rej_rx": "0",
            "lcp_protocol_rej_tx": "0",
            "lcp_total_msg_rx": "2",
            "lcp_total_msg_tx": "2",
            "ncp_avg_latency": "3454.00",
            "ncp_max_latency": "3454",
            "ncp_min_latency": "3454",
            "ncp_total_msg_rx": "3",
            "ncp_total_msg_tx": "3",
            "num_sessions": "1",
            "out_of_order_rx": "0",
            "out_of_win_rx": "0",
            "padi_timeouts": "0",
            "padi_tx": "0",
            "pado_rx": "0",
            "padr_timeouts": "0",
            "padr_tx": "0",
            "pads_rx": "0",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_rx": "0",
            "pap_auth_nak_rx": "0",
            "pap_auth_req_tx": "0",
            "ppp_total_bytes_rx": "161",
            "ppp_total_bytes_tx": "104",
            "retransmits": "0",
            "scccn_rx": "0",
            "scccn_tx": "1",
            "sccrp_rx": "1",
            "sccrp_tx": "0",
            "sccrq_rx": "0",
            "sccrq_tx": "1",
            "sessions_failed": "0",
            "sessions_not_started": "0",
            "sessions_up": "1",
            "sli_rx": "0",
            "sli_tx": "0",
            "stopccn_rx": "0",
            "stopccn_tx": "0",
            "success_setup_rate": "0",
            "teardown_failed": "0",
            "teardown_rate": "0",
            "teardown_succeeded": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0",
            "total_bytes_rx": "0",
            "total_bytes_tx": "0",
            "tun_tx_win_close": "0",
            "tun_tx_win_open": "4",
            "tx_pkt_acked": "4",
            "wen_rx": "0",
            "wen_tx": "0",
            "zlb_rx": "2",
            "zlb_tx": "0"
        },
        "session": {
            "/range:HLAPI1": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "duplicate_rx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "0",
                "iccn_tx": "1",
                "icrp_rx": "1",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "1",
                "in_order_rx": "2",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "144",
                "l2tp_tunnel_total_bytes_tx": "308",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "retransmits": "0",
                "scccn_rx": "0",
                "scccn_tx": "1",
                "sccrp_rx": "1",
                "sccrp_tx": "0",
                "sccrq_rx": "0",
                "sccrq_tx": "1",
                "sli_rx": "0",
                "sli_tx": "0",
                "status": "up",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "4",
                "tx_pkt_acked": "4",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "2",
                "zlb_tx": "0"
            },
            "/topology:2/deviceGroup:1/ethernet:1/ipv4:1/lac:1/item:1_1": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "duplicate_rx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "0",
                "iccn_tx": "1",
                "icrp_rx": "1",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "1",
                "in_order_rx": "2",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "144",
                "l2tp_tunnel_total_bytes_tx": "308",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "retransmits": "0",
                "scccn_rx": "0",
                "scccn_tx": "1",
                "sccrp_rx": "1",
                "sccrp_tx": "0",
                "sccrq_rx": "0",
                "sccrq_tx": "1",
                "sli_rx": "0",
                "sli_tx": "0",
                "status": "up",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "4",
                "tx_pkt_acked": "4",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "2",
                "zlb_tx": "0"
            }
        },
        "status": "1"
    },
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/pppoxserver:1/item:1": {
            "session": {
                "ac_mac_addr": "Not Available",
                "ac_name": "Not Available",
                "auth_id": "user",
                "auth_latency": "1401",
                "auth_password": "secret",
                "auth_protocol_rx": "None",
                "auth_protocol_tx": "CHAP",
                "auth_total_rx": "1",
                "auth_total_tx": "2",
                "avg_setup_time": "9386",
                "call_id": "1",
                "call_state": "Established",
                "chap_auth_chal_tx": "1",
                "chap_auth_fail_tx": "0",
                "chap_auth_role": "Peer",
                "chap_auth_rsp_rx": "1",
                "chap_auth_succ_tx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "cookie": "Not Available",
                "cookie_len": "0",
                "data_ns": "0",
                "destination_ip": "1.1.1.2",
                "destination_port": "1701",
                "dns_server_list": "Not Available",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "gateway_ip": "1.1.1.2",
                "generic_error_tag_rx": "0",
                "host_mac_addr": "Not Available",
                "host_name": "Not Available",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "0",
                "ipcp_cfg_nak_tx": "1",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "2",
                "ipcp_cfg_req_tx": "1",
                "ipcp_latency": "3527",
                "ipcp_state": "NCP Open",
                "ipv6_addr": "0:0:0:0:0:0:0:0",
                "ipv6_prefix_len": "0",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_latency": "0",
                "ipv6cp_router_adv_tx": "0",
                "ipv6cp_router_solicitation_rx": "0",
                "ipv6cp_state": "NCP Disable",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_latency": "2442",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "local_ip_addr": "1.1.1.1",
                "local_ipv6_iid": "Not Available",
                "loopback_detected": "False",
                "magic_no_negotiated": "True",
                "magic_no_rx": "1022819482",
                "magic_no_tx": "1816763613",
                "mru": "1500",
                "mtu": "1500",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "negotiation_end_ms": "0",
                "negotiation_start_ms": "0",
                "padi_rx": "0",
                "pado_tx": "0",
                "padr_rx": "0",
                "pads_tx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_tx": "0",
                "pap_auth_nak_tx": "0",
                "pap_auth_req_rx": "0",
                "peer_call_id": "1",
                "peer_id": "1",
                "peer_ipv6_iid": "Not Available",
                "ppp_close_mode": "None",
                "ppp_state": "PPP Connected",
                "pppoe_discovery_latency": "0",
                "pppoe_session_id": "0",
                "pppox_state": "Init",
                "primary_wins_server": "0.0.0.0",
                "relay_session_id_tag_rx": "0",
                "remote_ip_addr": "1.1.1.3",
                "secondary_wins_server": "0.0.0.0",
                "service_name": "Not Available",
                "source_ip": "1.1.1.1",
                "source_port": "1701",
                "status": "up",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "total_bytes_rx": "0",
                "total_bytes_tx": "0",
                "tunnel_id": "1",
                "tunnel_state": "Tunnel established",
                "vendor_specific_tag_rx": "0"
            }
        },
        "1/25/2": {
            "aggregate": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "chap_auth_chal_tx": "1",
                "chap_auth_fail_tx": "0",
                "chap_auth_rsp_rx": "1",
                "chap_auth_succ_tx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "duplicate_rx": "0",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "1",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "1",
                "icrq_rx": "1",
                "icrq_tx": "0",
                "in_order_rx": "4",
                "interfaces_in_pppoe_l2tp_negotiation": "0",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "0",
                "ipcp_cfg_nak_tx": "1",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "2",
                "ipcp_cfg_req_tx": "1",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_router_adv_tx": "0",
                "ipv6cp_router_solicitation_rx": "0",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "210",
                "l2tp_tunnel_total_bytes_tx": "172",
                "lcp_avg_latency": "2442.00",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_max_latency": "2442",
                "lcp_min_latency": "2442",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "ncp_avg_latency": "3527.00",
                "ncp_max_latency": "3527",
                "ncp_min_latency": "3527",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "num_sessions": "1",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "padi_rx": "0",
                "pado_tx": "0",
                "padr_rx": "0",
                "pads_tx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_tx": "0",
                "pap_auth_nak_tx": "0",
                "pap_auth_req_rx": "0",
                "ppp_total_bytes_rx": "104",
                "ppp_total_bytes_tx": "161",
                "retransmits": "0",
                "scccn_rx": "1",
                "scccn_tx": "0",
                "sccrp_rx": "0",
                "sccrp_tx": "1",
                "sccrq_rx": "1",
                "sccrq_tx": "0",
                "server_interfaces_in_ppp_negotiation": "0",
                "server_session_avg_latency": "9386.00",
                "server_session_max_latency": "9386",
                "server_session_min_latency": "9386",
                "server_tunnels_up": "1",
                "sessions_failed": "0",
                "sessions_not_started": "0",
                "sessions_up": "1",
                "sli_rx": "0",
                "sli_tx": "0",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "total_bytes_rx": "0",
                "total_bytes_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "2",
                "tx_pkt_acked": "2",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "0",
                "zlb_tx": "2"
            }
        },
        "aggregate": {
            "cdn_rx": "0",
            "cdn_tx": "0",
            "chap_auth_chal_tx": "1",
            "chap_auth_fail_tx": "0",
            "chap_auth_rsp_rx": "1",
            "chap_auth_succ_tx": "1",
            "code_rej_rx": "0",
            "code_rej_tx": "0",
            "duplicate_rx": "0",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_rsp_rx": "0",
            "echo_rsp_tx": "0",
            "hello_rx": "0",
            "hello_tx": "0",
            "iccn_rx": "1",
            "iccn_tx": "0",
            "icrp_rx": "0",
            "icrp_tx": "1",
            "icrq_rx": "1",
            "icrq_tx": "0",
            "in_order_rx": "4",
            "interfaces_in_pppoe_l2tp_negotiation": "0",
            "ipcp_cfg_ack_rx": "1",
            "ipcp_cfg_ack_tx": "1",
            "ipcp_cfg_nak_rx": "0",
            "ipcp_cfg_nak_tx": "1",
            "ipcp_cfg_rej_rx": "0",
            "ipcp_cfg_rej_tx": "0",
            "ipcp_cfg_req_rx": "2",
            "ipcp_cfg_req_tx": "1",
            "ipv6cp_cfg_ack_rx": "0",
            "ipv6cp_cfg_ack_tx": "0",
            "ipv6cp_cfg_nak_rx": "0",
            "ipv6cp_cfg_nak_tx": "0",
            "ipv6cp_cfg_rej_rx": "0",
            "ipv6cp_cfg_rej_tx": "0",
            "ipv6cp_cfg_req_rx": "0",
            "ipv6cp_cfg_req_tx": "0",
            "ipv6cp_router_adv_tx": "0",
            "ipv6cp_router_solicitation_rx": "0",
            "l2tp_calls_up": "1",
            "l2tp_tunnel_total_bytes_rx": "210",
            "l2tp_tunnel_total_bytes_tx": "172",
            "lcp_avg_latency": "2442.00",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "lcp_max_latency": "2442",
            "lcp_min_latency": "2442",
            "lcp_protocol_rej_rx": "0",
            "lcp_protocol_rej_tx": "0",
            "lcp_total_msg_rx": "2",
            "lcp_total_msg_tx": "2",
            "ncp_avg_latency": "3527.00",
            "ncp_max_latency": "3527",
            "ncp_min_latency": "3527",
            "ncp_total_msg_rx": "3",
            "ncp_total_msg_tx": "3",
            "num_sessions": "1",
            "out_of_order_rx": "0",
            "out_of_win_rx": "0",
            "padi_rx": "0",
            "pado_tx": "0",
            "padr_rx": "0",
            "pads_tx": "0",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_tx": "0",
            "pap_auth_nak_tx": "0",
            "pap_auth_req_rx": "0",
            "ppp_total_bytes_rx": "104",
            "ppp_total_bytes_tx": "161",
            "retransmits": "0",
            "scccn_rx": "1",
            "scccn_tx": "0",
            "sccrp_rx": "0",
            "sccrp_tx": "1",
            "sccrq_rx": "1",
            "sccrq_tx": "0",
            "server_interfaces_in_ppp_negotiation": "0",
            "server_session_avg_latency": "9386.00",
            "server_session_max_latency": "9386",
            "server_session_min_latency": "9386",
            "server_tunnels_up": "1",
            "sessions_failed": "0",
            "sessions_not_started": "0",
            "sessions_up": "1",
            "sli_rx": "0",
            "sli_tx": "0",
            "stopccn_rx": "0",
            "stopccn_tx": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0",
            "total_bytes_rx": "0",
            "total_bytes_tx": "0",
            "tun_tx_win_close": "0",
            "tun_tx_win_open": "2",
            "tx_pkt_acked": "2",
            "wen_rx": "0",
            "wen_tx": "0",
            "zlb_rx": "0",
            "zlb_tx": "2"
        },
        "session": {
            "/range:HLAPI0": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "duplicate_rx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "1",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "1",
                "icrq_rx": "1",
                "icrq_tx": "0",
                "in_order_rx": "4",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "210",
                "l2tp_tunnel_total_bytes_tx": "172",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "retransmits": "0",
                "scccn_rx": "1",
                "scccn_tx": "0",
                "sccrp_rx": "0",
                "sccrp_tx": "1",
                "sccrq_rx": "1",
                "sccrq_tx": "0",
                "server_tunnels_up": "1",
                "session_status": "Up",
                "sli_rx": "0",
                "sli_tx": "0",
                "status": "up",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "2",
                "tx_pkt_acked": "2",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "0",
                "zlb_tx": "2"
            },
            "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/lns:1/item:1_1": {
                "cdn_rx": "0",
                "cdn_tx": "0",
                "duplicate_rx": "0",
                "hello_rx": "0",
                "hello_tx": "0",
                "iccn_rx": "1",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "1",
                "icrq_rx": "1",
                "icrq_tx": "0",
                "in_order_rx": "4",
                "l2tp_calls_up": "1",
                "l2tp_tunnel_total_bytes_rx": "210",
                "l2tp_tunnel_total_bytes_tx": "172",
                "out_of_order_rx": "0",
                "out_of_win_rx": "0",
                "retransmits": "0",
                "scccn_rx": "1",
                "scccn_tx": "0",
                "sccrp_rx": "0",
                "sccrp_tx": "1",
                "sccrq_rx": "1",
                "sccrq_tx": "0",
                "server_tunnels_up": "1",
                "session_status": "Up",
                "sli_rx": "0",
                "sli_tx": "0",
                "status": "up",
                "stopccn_rx": "0",
                "stopccn_tx": "0",
                "tun_tx_win_close": "0",
                "tun_tx_win_open": "2",
                "tx_pkt_acked": "2",
                "wen_rx": "0",
                "wen_tx": "0",
                "zlb_rx": "0",
                "zlb_tx": "2"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "status"
        "aggregate"
        "session"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    ret = []
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                stats = dict()
                args['mode'] = 'aggregate'
                stats.update(rt_handle.invoke('l2tp_stats', **args))
                args['mode'] = 'session'
                stats.update(rt_handle.invoke('l2tp_stats', **args))
                args['mode'] = 'tunnel'
                stats.update(rt_handle.invoke('l2tp_stats', **args))
                if 'session' in stats:
                    for key in list(stats['session']):
                        stats['session'][args['handle']] = stats['session'][key]
                ret.append(stats)
        else:
            args['handle'] = hndl
            stats = dict()
            args['mode'] = 'aggregate'
            stats.update(rt_handle.invoke('l2tp_stats', **args))
            args['mode'] = 'session'
            stats.update(rt_handle.invoke('l2tp_stats', **args))
            args['mode'] = 'tunnel'
            stats.update(rt_handle.invoke('l2tp_stats', **args))
            if 'session' in stats:
                for key in list(stats['session']):
                    stats['session'][args['handle']] = stats['session'][key]
            ret.append(stats)

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_pppox_config(
        rt_handle,
        attempt_rate=jNone,
        auth_mode=jNone,
        auth_req_timeout=jNone,
        config_req_timeout=jNone,
        disconnect_rate=jNone,
        echo_req_interval=jNone,
        handle=jNone,
        intermediate_agent=jNone,
        ipcp_req_timeout=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        max_auth_req=jNone,
        max_configure_req=jNone,
        max_ipcp_req=jNone,
        max_outstanding=jNone,
        max_padi_req=jNone,
        max_padr_req=jNone,
        max_terminate_req=jNone,
        num_sessions=jNone,
        padi_req_timeout=jNone,
        padr_req_timeout=jNone,
        password_wildcard=jNone,
        qinq_incr_mode=jNone,
        username_wildcard=jNone,
        vlan_id=jNone,
        vlan_id_count=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_count=jNone,
        vlan_id_outer_step=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        username=jNone,
        password=jNone,
        protocol=jNone,
        mode=jNone,
        ip_cp=jNone,
        port_handle=jNone,
        vlan_outer_user_priority=jNone,
        encap=jNone,
        echo_req=jNone):
    """
    :param rt_handle:       RT object
    :param attempt_rate - <1-1000>
    :param auth_mode - <none|pap|chap|pap_or_chap>
    :param auth_req_timeout - <1-65535>
    :param config_req_timeout - <1-120>
    :param disconnect_rate - <1-1000>
    :param echo_req_interval - <1-3600>
    :param handle
    :param intermediate_agent - <0|1>
    :param ipcp_req_timeout - <1-120>
    :param mac_addr
    :param mac_addr_step
    :param max_auth_req - <1-65535>
    :param max_configure_req - <1-255>
    :param max_ipcp_req - <1-255>
    :param max_outstanding - <2-1000>
    :param max_padi_req - <1-65535>
    :param max_padr_req - <1-65535>
    :param max_terminate_req - <1-65535>
    :param num_sessions - <1-32000>
    :param padi_req_timeout - <1-65535>
    :param padr_req_timeout - <1-65535>
    :param password_wildcard - <0|1>
    :param qinq_incr_mode - <inner|outer|both>
    :param username_wildcard - <0|1>
    :param vlan_id - <0-4095>
    :param vlan_id_count - <1-4094>
    :param vlan_id_outer - <0-4095>
    :param vlan_id_outer_count - <1-4094>
    :param vlan_id_outer_step - <0-4094>
    :param vlan_id_step - <0-4094>
    :param vlan_user_priority - <0-7>
    :param username
    :param password
    :param protocol - <pppoe|pppoa|pppoeoa>
    :param mode - <create:add|modify|reset:remove>
    :param ip_cp - <ipv4_cp|ipv6_cp|ipv4v6_cp:dual_stack>
    :param port_handle
    :param vlan_outer_user_priority - <0-7>
    :param encap - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq|vc_mux|llcsnap>
    :param echo_req - <0|1>

    Spirent Returns:
    {
        "handle": "host3",
        "handles": "host3",
        "port_handle": "port2",
        "pppoe_port": "pppoxportconfig2",
        "pppoe_session": "pppoeclientblockconfig1",
        "procName": "sth::pppox_config",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/range:HLAPI1",
        "handles": "/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1",
        "pppox_client_handle": "/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['attempt_rate'] = attempt_rate
    args['auth_mode'] = auth_mode
    args['auth_req_timeout'] = auth_req_timeout
    args['config_req_timeout'] = config_req_timeout
    args['disconnect_rate'] = disconnect_rate
    args['echo_req_interval'] = echo_req_interval
    args['handle'] = handle
    args['intermediate_agent'] = intermediate_agent
    args['ipcp_req_timeout'] = ipcp_req_timeout
    args['mac_addr'] = mac_addr
    args['mac_addr_step'] = mac_addr_step
    args['max_auth_req'] = max_auth_req
    args['max_configure_req'] = max_configure_req
    args['max_ipcp_req'] = max_ipcp_req
    args['max_outstanding'] = max_outstanding
    args['max_padi_req'] = max_padi_req
    args['max_padr_req'] = max_padr_req
    args['max_terminate_req'] = max_terminate_req
    args['num_sessions'] = num_sessions
    args['padi_req_timeout'] = padi_req_timeout
    args['padr_req_timeout'] = padr_req_timeout
    args['password_wildcard'] = password_wildcard
    args['qinq_incr_mode'] = qinq_incr_mode
    args['username_wildcard'] = username_wildcard
    args['vlan_id'] = vlan_id
    args['vlan_id_count'] = vlan_id_count
    args['vlan_id_outer'] = vlan_id_outer
    args['vlan_id_outer_count'] = vlan_id_outer_count
    args['vlan_id_outer_step'] = vlan_id_outer_step
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['vlan_outer_user_priority'] = vlan_outer_user_priority
    args['username'] = username
    args['password'] = password
    args['protocol'] = protocol
    args['mode'] = mode
    args['port_handle'] = port_handle
    args['encap'] = encap
    args['ip_cp'] = ip_cp
    #if ip_cp == 'ipv4':
     #   args['ip_cp'] = 'ipv4_cp'
    #elif ip_cp == 'ipv6':
     #   args['ip_cp'] = 'ipv6_cp'
    #elif ip_cp == 'dual_stack':
     #   args['ip_cp'] = 'ipv4v6_cp'
    args['echo_req'] = echo_req

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_pppox_config.__doc__, **args)
    ret = []
    handle_list = dict()
    counter = 1
    string = "ppp_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "ppp_" + str(counter)
    global_config[string] = []
    if port_handle != jNone:
        args['port_handle'] = port_handle
        result = rt_handle.invoke('pppox_config', **args)
        if result.get('handle'):
            result['handle'] = result['handle'].split(' ')
            if mode == 'enable' or mode == 'create':
                global_config[string].extend(result['handle'])
                result['handles'] = string
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        for hand in port_handle:
            handle_map[hand] = handle_map.get(hand, [])
            handle_map[hand].extend(global_config[string])
            handle_map[string] = hand
        ret.append(result)
    
    elif handle != jNone:
        ret.append(invoke_handle(rt_handle, protocol_string=string, **args))
    else:
        raise RuntimeError('Either handle or port_handle argument must be passed to j_pppox_config')





    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_pppox_control(rt_handle, action=jNone, handle=jNone):
    """
    :param rt_handle:       RT object
    :param action - <connect|disconnect|reset>
    :param handle

    Spirent Returns:
    {
        "handles": "host3",
        "procName": "sth::pppox_control",
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
   
    args = get_arg_value(rt_handle, j_pppox_control.__doc__, **args)
   
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))


    ret = []
    for hndl in handle:
        hnd = " ".join(global_config[hndl])
        args['handle'] = hnd
        ret.append(rt_handle.invoke('pppox_control', **args))



    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_pppox_stats(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <aggregate|session>

    Spirent Returns:
    {
        "agg": {
            "attempted": "1",
            "chap_auth_chal_rx": "2",
            "chap_auth_fail_rx": "2",
            "chap_auth_rsp_tx": "1",
            "chap_auth_succ_rx": "1",
            "completed": "0",
            "connect_success": "1",
            "echo_req_rx": "0",
            "echo_rsp_tx": "0",
            "failed_connect": "0",
            "failed_disconnect": "0",
            "ip_addr": "1.1.1.2",
            "ipcp_cfg_ack_rx": "3",
            "ipcp_cfg_ack_tx": "3",
            "ipcp_cfg_nak_rx": "3",
            "ipcp_cfg_nak_tx": "3",
            "ipcp_cfg_rej_rx": "3",
            "ipcp_cfg_rej_tx": "3",
            "ipcp_cfg_req_rx": "3",
            "ipcp_cfg_req_tx": "3",
            "ipv6_addr": "::",
            "ipv6_global_addr": "::",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "padi_rx": "0",
            "padi_tx": "1",
            "pado_rx": "1",
            "pado_tx": "0",
            "padr_rx": "0",
            "padr_tx": "1",
            "pads_rx": "1",
            "pads_tx": "0",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_rx": "0",
            "pap_auth_nak_rx": "0",
            "pap_auth_req_tx": "0",
            "setup_time": "113",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "aggregate": {
            "abort": "0",
            "atm_mode": "0",
            "avg_setup_time": "113",
            "chap_auth_chal_rx": "2",
            "chap_auth_fail_rx": "2",
            "chap_auth_rsp_tx": "1",
            "chap_auth_succ_rx": "2",
            "connect_attempts": "1",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "disconnect_failed": "0",
            "disconnect_success": "0",
            "disconnecting": "0",
            "echo_req_rx": "0",
            "echo_rsp_tx": "0",
            "idle": "0",
            "ipcp_cfg_ack_rx": "3",
            "ipcp_cfg_ack_tx": "3",
            "ipcp_cfg_nak_rx": "3",
            "ipcp_cfg_nak_tx": "3",
            "ipcp_cfg_rej_rx": "3",
            "ipcp_cfg_rej_tx": "3",
            "ipcp_cfg_req_rx": "3",
            "ipcp_cfg_req_tx": "3",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "max_setup_time": "113",
            "min_setup_time": "113",
            "num_sessions": "1",
            "padi_rx": "0",
            "padi_tx": "1",
            "pado_rx": "1",
            "padr_rx": "0",
            "padr_tx": "1",
            "pads_rx": "1",
            "pads_tx": "0",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_rx": "0",
            "pap_auth_nak_rx": "0",
            "pap_auth_req_tx": "0",
            "sessions_down": "0",
            "sessions_up": "1",
            "success_setup_rate": "8",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "handles": "host3",
        "procName": "sth::pppox_stats",
        "session": {
            "1": {
                "attempted": "1",
                "chap_auth_chal_rx": "2",
                "chap_auth_fail_rx": "2",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "completed": "0",
                "connect_success": "1",
                "echo_req_rx": "0",
                "echo_rsp_tx": "0",
                "failed_connect": "0",
                "failed_disconnect": "0",
                "ip_addr": "1.1.1.2",
                "ipcp_cfg_ack_rx": "3",
                "ipcp_cfg_ack_tx": "3",
                "ipcp_cfg_nak_rx": "3",
                "ipcp_cfg_nak_tx": "3",
                "ipcp_cfg_rej_rx": "3",
                "ipcp_cfg_rej_tx": "3",
                "ipcp_cfg_req_rx": "3",
                "ipcp_cfg_req_tx": "3",
                "ipv6_addr": "::",
                "ipv6_global_addr": "::",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "padi_rx": "0",
                "padi_tx": "1",
                "pado_rx": "1",
                "pado_tx": "0",
                "padr_rx": "0",
                "padr_tx": "1",
                "pads_rx": "1",
                "pads_tx": "0",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "setup_time": "113",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0"
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "Range 1/25/1 2 False": {
            "aggregate": {
                "auth_avg_time": "6303.00",
                "auth_max_time": "6303",
                "auth_min_time": "6303",
                "avg_setum_rate": "1.00",
                "avg_setup_time": "88601.00",
                "avg_teardown_rate": "0.00",
                "call_disconnect_notifiy_rx": "0",
                "call_disconnect_notifiy_tx": "0",
                "chap_auth_chal_rx": "1",
                "chap_auth_fail_rx": "0",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "connect_success": "1",
                "connected": "1",
                "connecting": "0",
                "cumulative_setup_failed": "0",
                "cumulative_setup_initiated": "1",
                "cumulative_setup_succeeded": "1",
                "cumulative_teardown_failed": "0",
                "cumulative_teardown_succeeded": "0",
                "device_group": "Range 1/25/1 2 False",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_resp_rx": "0",
                "echo_resp_tx": "0",
                "idle": "0",
                "incoming_call_connected_rx": "0",
                "incoming_call_connected_tx": "0",
                "incoming_call_reply_rx": "0",
                "incoming_call_reply_tx": "0",
                "incoming_call_request_rx": "0",
                "incoming_call_request_tx": "0",
                "interfaces_in_chap_negotiation": "0",
                "interfaces_in_ipcp_negotiation": "0",
                "interfaces_in_ipv6cp_negotiation": "0",
                "interfaces_in_lcp_negotiation": "0",
                "interfaces_in_pap_negotiation": "0",
                "interfaces_in_ppp_negotiation": "0",
                "interfaces_in_pppoe_l2tp_negotiation": "0",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "1",
                "ipcp_cfg_nak_tx": "0",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "1",
                "ipcp_cfg_req_tx": "2",
                "ipv6cp_avg_time": "0.00",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_max_time": "0",
                "ipv6cp_min_time": "0",
                "ipv6cp_router_adv_rx": "0",
                "lcp_avg_latency": "23071.00",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_max_latency": "23071",
                "lcp_min_latency": "23071",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "ncp_avg_latency": "6248.00",
                "ncp_max_latency": "6248",
                "ncp_min_latency": "6248",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "num_sessions": "1",
                "padi_timeout": "0",
                "padi_tx": "1",
                "pado_rx": "1",
                "padr_timeout": "0",
                "padr_tx": "1",
                "pads_rx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "ppp_total_bytes_rx": "147",
                "ppp_total_bytes_tx": "92",
                "pppoe_avg_latency": "52893.00",
                "pppoe_max_latency": "52893",
                "pppoe_min_latency": "52893",
                "pppoe_total_bytes_rx": "36",
                "pppoe_total_bytes_tx": "20",
                "sessions_down": "0",
                "sessions_failed": "0",
                "sessions_initiated": "0",
                "sessions_up": "1",
                "set_link_info_rx": "0",
                "set_link_info_tx": "0",
                "teardown_failed": "0",
                "teardown_succeded": "0",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0"
            }
        },
        "aggregate": {
            "auth_avg_time": "6303.00",
            "auth_max_time": "6303",
            "auth_min_time": "6303",
            "avg_setum_rate": "1.00",
            "avg_setup_time": "88601.00",
            "avg_teardown_rate": "0.00",
            "call_disconnect_notifiy_rx": "0",
            "call_disconnect_notifiy_tx": "0",
            "chap_auth_chal_rx": "1",
            "chap_auth_fail_rx": "0",
            "chap_auth_rsp_tx": "1",
            "chap_auth_succ_rx": "1",
            "code_rej_rx": "0",
            "code_rej_tx": "0",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "cumulative_setup_failed": "0",
            "cumulative_setup_initiated": "1",
            "cumulative_setup_succeeded": "1",
            "cumulative_teardown_failed": "0",
            "cumulative_teardown_succeeded": "0",
            "device_group": "Range 1/25/1 2 False",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_resp_rx": "0",
            "echo_resp_tx": "0",
            "idle": "0",
            "incoming_call_connected_rx": "0",
            "incoming_call_connected_tx": "0",
            "incoming_call_reply_rx": "0",
            "incoming_call_reply_tx": "0",
            "incoming_call_request_rx": "0",
            "incoming_call_request_tx": "0",
            "interfaces_in_chap_negotiation": "0",
            "interfaces_in_ipcp_negotiation": "0",
            "interfaces_in_ipv6cp_negotiation": "0",
            "interfaces_in_lcp_negotiation": "0",
            "interfaces_in_pap_negotiation": "0",
            "interfaces_in_ppp_negotiation": "0",
            "interfaces_in_pppoe_l2tp_negotiation": "0",
            "ipcp_cfg_ack_rx": "1",
            "ipcp_cfg_ack_tx": "1",
            "ipcp_cfg_nak_rx": "1",
            "ipcp_cfg_nak_tx": "0",
            "ipcp_cfg_rej_rx": "0",
            "ipcp_cfg_rej_tx": "0",
            "ipcp_cfg_req_rx": "1",
            "ipcp_cfg_req_tx": "2",
            "ipv6cp_avg_time": "0.00",
            "ipv6cp_cfg_ack_rx": "0",
            "ipv6cp_cfg_ack_tx": "0",
            "ipv6cp_cfg_nak_rx": "0",
            "ipv6cp_cfg_nak_tx": "0",
            "ipv6cp_cfg_rej_rx": "0",
            "ipv6cp_cfg_rej_tx": "0",
            "ipv6cp_cfg_req_rx": "0",
            "ipv6cp_cfg_req_tx": "0",
            "ipv6cp_max_time": "0",
            "ipv6cp_min_time": "0",
            "ipv6cp_router_adv_rx": "0",
            "lcp_avg_latency": "23071.00",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "lcp_max_latency": "23071",
            "lcp_min_latency": "23071",
            "lcp_protocol_rej_rx": "0",
            "lcp_protocol_rej_tx": "0",
            "lcp_total_msg_rx": "2",
            "lcp_total_msg_tx": "2",
            "ncp_avg_latency": "6248.00",
            "ncp_max_latency": "6248",
            "ncp_min_latency": "6248",
            "ncp_total_msg_rx": "3",
            "ncp_total_msg_tx": "3",
            "num_sessions": "1",
            "padi_timeout": "0",
            "padi_tx": "1",
            "pado_rx": "1",
            "padr_timeout": "0",
            "padr_tx": "1",
            "pads_rx": "1",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_rx": "0",
            "pap_auth_nak_rx": "0",
            "pap_auth_req_tx": "0",
            "ppp_total_bytes_rx": "147",
            "ppp_total_bytes_tx": "92",
            "pppoe_avg_latency": "52893.00",
            "pppoe_max_latency": "52893",
            "pppoe_min_latency": "52893",
            "pppoe_total_bytes_rx": "36",
            "pppoe_total_bytes_tx": "20",
            "sessions_down": "0",
            "sessions_failed": "0",
            "sessions_initiated": "0",
            "sessions_up": "1",
            "set_link_info_rx": "0",
            "set_link_info_tx": "0",
            "teardown_failed": "0",
            "teardown_succeded": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "session": {
            "/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1/item:1": {
                "ac_cookie": "",
                "ac_cookie_tag_rx": "0",
                "ac_generic_error": "False",
                "ac_mac_addr": "00:11:01:00:00:01",
                "ac_name": "ixia",
                "ac_offer_rx": "1",
                "ac_system_error": "False",
                "ac_system_error_tag_rx": "0",
                "auth_establishment_time": "6303",
                "auth_id": "user",
                "auth_password": "secret",
                "auth_protocol_rx": "CHAP",
                "auth_protocol_tx": "None",
                "auth_total_rx": "2",
                "auth_total_tx": "1",
                "call_state": "Idle",
                "cdn_rx": "0",
                "cdn_tx": "0",
                "chap_auth_chal_rx": "1",
                "chap_auth_fail_rx": "0",
                "chap_auth_role": "Peer",
                "chap_auth_rsp_tx": "1",
                "chap_auth_succ_rx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "cumulative_setup_failed": "0",
                "cumulative_setup_initiated": "1",
                "cumulative_setup_succeeded": "1",
                "cumulative_teardown_failed": "0",
                "cumulative_teardown_succeeded": "0",
                "data_ns": "0",
                "destination_ip": "0.0.0.0",
                "destination_port": "0",
                "device_group": "Range 1/25/1 2 False",
                "device_id": "1",
                "dns_server_list": "Not Available",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_resp_rx": "0",
                "echo_resp_tx": "0",
                "establishment_time": "88601",
                "gateway_ip": "0.0.0.0",
                "generic_error_tag_tx": "0",
                "host_mac_addr": "00:11:02:00:00:01",
                "host_name": "Not Available",
                "host_uniq": "",
                "iccn_rx": "0",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "0",
                "ip_cpe_establishment_time": "6248",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "1",
                "ipcp_cfg_nak_tx": "0",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "1",
                "ipcp_cfg_req_tx": "2",
                "ipcp_state": "NCP Open",
                "ipv6_addr": "0:0:0:0:0:0:0:0",
                "ipv6_cpe_establishment_time": "0",
                "ipv6_prefix_len": "0",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_router_adv_rx": "0",
                "ipv6cp_state": "NCP Disable",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_establishment_time": "23071",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "local_ip_addr": "1.1.1.2",
                "local_ipv6_iid": "Not Available",
                "loopback_detected": "False",
                "magic_no_negotiated": "True",
                "magic_no_rx": "3769293702",
                "magic_no_tx": "771179460",
                "mru": "1500",
                "mtu": "1500",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "negotiation_end_ms": "534097804",
                "negotiation_start_ms": "534009203",
                "our_call_id": "0",
                "our_cookie": "Not Available",
                "our_cookie_length": "0",
                "our_peer_id": "0",
                "our_tunnel_id": "0",
                "padi_timeout": "0",
                "padi_tx": "1",
                "pado_rx": "1",
                "padr_timeout": "0",
                "padr_tx": "1",
                "pads_rx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_rx": "0",
                "pap_auth_nak_rx": "0",
                "pap_auth_req_tx": "0",
                "peer_call_id": "0",
                "peer_ipv6_iid": "Not Available",
                "peer_tunnel_id": "0",
                "ppp_close_mode": "None",
                "ppp_state": "PPP Connected",
                "ppp_total_rx": "147",
                "ppp_total_tx": "92",
                "pppoe_latency": "52893",
                "pppoe_state": "Session",
                "pppoe_total_bytes_rx": "36",
                "pppoe_total_bytes_tx": "20",
                "primary_wins_server": "0.0.0.0",
                "protocol": "PPPoX Client 1",
                "relay_session_id_tag_rx": "0",
                "remote_ip_addr": "1.1.1.1",
                "secondary_wins_server": "0.0.0.0",
                "service_name": "",
                "service_name_error_tag_rx": "0",
                "session_id": "1",
                "source_ip": "0.0.0.0",
                "source_port": "0",
                "status": "up",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "topology": "T 1/25/1",
                "tunnel_state": "Tunnel Idle",
                "vendor_specific_tag_rx": "0"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "aggregate"
        "session"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
 
    args = get_arg_value(rt_handle, j_pppox_stats.__doc__, **args)
   
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        for hnd in global_config[hndl]:
            args['handle'] = hnd
            stats = dict()
            args['mode'] = 'aggregate'
            stats.update(rt_handle.invoke('pppox_stats', **args))
            args['mode'] = 'session'
            stats.update(rt_handle.invoke('pppox_stats', **args))
            if 'session' in stats:
                for key in list(stats['session']):
                    stats['session'][hndl] = stats['session'][key]
                    if 'ip_addr' in stats['session'][key]:
                        stats['session'][hndl]['local_ip_addr'] = stats['session'][key]['ip_addr']
            ret.append(stats)


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_test_control(rt_handle, action=jNone):
    """
    :param rt_handle:       RT object
    :param action
    :return response from rt_handle.invoke(<parameters>)

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]
    if action == 'enable' or action == 'disable' or action == 'sync':
        ret = rt_handle.invoke('test_control', **args)
    elif action == 'start_all_protocols':
        ret = rt_handle.invoke('start_devices')
    elif action == 'stop_all_protocols':
        ret = rt_handle.invoke('stop_devices')


    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret


def j_traffic_config(
        rt_handle,
        arp_dst_hw_addr=jNone,
        arp_dst_hw_count=jNone,
        arp_dst_hw_mode=jNone,
        arp_operation=jNone,
        arp_src_hw_addr=jNone,
        arp_src_hw_count=jNone,
        arp_src_hw_mode=jNone,
        bidirectional=jNone,
        burst_loop_count=jNone,
        emulation_dst_handle=jNone,
        emulation_src_handle=jNone,
        frame_size=jNone,
        frame_size_max=jNone,
        frame_size_min=jNone,
        frame_size_step=jNone,
        icmp_checksum=jNone,
        icmp_code=jNone,
        icmp_id=jNone,
        icmp_seq=jNone,
        icmp_type=jNone,
        igmp_group_addr=jNone,
        igmp_group_count=jNone,
        igmp_group_mode=jNone,
        igmp_group_step=jNone,
        igmp_max_response_time=jNone,
        igmp_msg_type=jNone,
        igmp_multicast_src=jNone,
        igmp_qqic=jNone,
        igmp_qrv=jNone,
        igmp_s_flag=jNone,
        igmp_type=jNone,
        igmp_version=jNone,
        inner_ip_dst_addr=jNone,
        inner_ip_dst_count=jNone,
        inner_ip_dst_mode=jNone,
        inner_ip_dst_step=jNone,
        inner_ip_src_addr=jNone,
        inner_ip_src_count=jNone,
        inner_ip_src_mode=jNone,
        inner_ip_src_step=jNone,
        inter_stream_gap=jNone,
        ip_checksum=jNone,
        ip_dscp=jNone,
        ip_dscp_count=jNone,
        ip_dscp_step=jNone,
        ip_dst_addr=jNone,
        ip_dst_count=jNone,
        ip_dst_mode=jNone,
        ip_dst_step=jNone,
        ip_fragment=jNone,
        ip_fragment_offset=jNone,
        ip_fragment_last=jNone,
        ip_hdr_length=jNone,
        ip_id=jNone,
        ip_precedence=jNone,
        ip_precedence_count=jNone,
        ip_precedence_step=jNone,
        ip_protocol=jNone,
        ip_src_addr=jNone,
        ip_src_count=jNone,
        ip_src_mode=jNone,
        ip_src_step=jNone,
        ip_ttl=jNone,
        ipv6_auth_payload_len=jNone,
        ipv6_auth_seq_num=jNone,
        ipv6_auth_spi=jNone,
        ipv6_auth_string=jNone,
        ipv6_dst_addr=jNone,
        ipv6_dst_count=jNone,
        ipv6_dst_mode=jNone,
        ipv6_dst_step=jNone,
        ipv6_extension_header=jNone,
        ipv6_frag_id=jNone,
        ipv6_frag_more_flag=jNone,
        ipv6_frag_offset=jNone,
        ipv6_hop_by_hop_options=jNone,
        ipv6_hop_limit=jNone,
        #ipv6_next_header=jNone,
        ipv6_routing_node_list=jNone,
        ipv6_routing_res=jNone,
        ipv6_src_addr=jNone,
        ipv6_src_count=jNone,
        ipv6_src_mode=jNone,
        ipv6_src_step=jNone,
        ipv6_traffic_class=jNone,
        l2_encap=jNone,
        l3_imix1_ratio=jNone,
        l3_imix1_size=jNone,
        l3_imix2_ratio=jNone,
        l3_imix2_size=jNone,
        l3_imix3_ratio=jNone,
        l3_imix3_size=jNone,
        l3_imix4_ratio=jNone,
        l3_imix4_size=jNone,
        l3_length=jNone,
        l3_length_max=jNone,
        l3_length_min=jNone,
        l3_protocol=jNone,
        l4_protocol=jNone,
        length_mode=jNone,
        mac_dst=jNone,
        mac_dst2=jNone,
        mac_dst_count=jNone,
        mac_dst_mode=jNone,
        mac_dst_step=jNone,
        mac_src=jNone,
        mac_src2=jNone,
        mac_src_count=jNone,
        mac_src_mode=jNone,
        mac_src_step=jNone,
        mode=jNone,
        mpls_bottom_stack_bit=jNone,
        mpls_labels=jNone,
        mpls_labels_count=jNone,
        mpls_labels_mode=jNone,
        mpls_labels_step=jNone,
        mpls_ttl=jNone,
        name=jNone,
        pkts_per_burst=jNone,
        port_handle=jNone,
        port_handle2=jNone,
        rate_bps=jNone,
        rate_percent=jNone,
        rate_pps=jNone,
        stream_id=jNone,
        tcp_ack_flag=jNone,
        tcp_ack_num=jNone,
        tcp_checksum=jNone,
        tcp_data_offset=jNone,
        tcp_dst_port_count=jNone,
        tcp_dst_port_mode=jNone,
        tcp_dst_port_step=jNone,
        tcp_fin_flag=jNone,
        tcp_psh_flag=jNone,
        tcp_reserved=jNone,
        tcp_rst_flag=jNone,
        tcp_seq_num=jNone,
        tcp_src_port=jNone,
        tcp_src_port_count=jNone,
        tcp_src_port_mode=jNone,
        tcp_src_port_step=jNone,
        tcp_syn_flag=jNone,
        tcp_urg_flag=jNone,
        tcp_urgent_ptr=jNone,
        tcp_window=jNone,
        transmit_mode=jNone,
        udp_checksum=jNone,
        udp_dst_port=jNone,
        udp_dst_port_count=jNone,
        udp_dst_port_mode=jNone,
        udp_dst_port_step=jNone,
        udp_src_port=jNone,
        udp_src_port_count=jNone,
        udp_src_port_mode=jNone,
        udp_src_port_step=jNone,
        vci=jNone,
        vci_count=jNone,
        vci_step=jNone,
        vlan_cfi=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        vpi=jNone,
        vpi_count=jNone,
        vpi_step=jNone,
        emulation_multicast_dst_handle=jNone,
        emulation_multicast_dst_handle_type=jNone,
        tcp_dst_port=jNone,
        ip_precedence_mode=jNone,
        fcs_error=jNone,
        rate_mbps=jNone,
        arp_dst_protocol_addr=jNone,
        arp_dst_protocol_addr_count=jNone,
        arp_dst_protocol_addr_mode=jNone,
        arp_dst_protocol_addr_step=jNone,
        arp_src_protocol_addr=jNone,
        arp_src_protocol_addr_count=jNone,
        arp_src_protocol_addr_mode=jNone,
        arp_src_protocol_addr_step=jNone,
        icmpv6_type=jNone,
        icmpv6_pointer=jNone,
        icmpv6_target_address=jNone,
        icmpv6_oflag=jNone,
        icmpv6_rflag=jNone,
        icmpv6_sflag=jNone,
        icmpv6_suppress_flag=jNone,
        icmpv6_max_resp_delay=jNone,
        icmpv6_mcast_addr=jNone,
        icmpv6_prefix_option_valid_lifetime=jNone,
        icmpv6_dest_address=jNone,
        icmpv6_qqic=jNone,
        icmpv6_qrv=jNone,
        vlan_id_count=jNone,
        mpls_exp_bit=jNone,
        icmpv6_code=jNone,
        high_speed_result_analysis=jNone,
        enable_stream=jNone,
        ipv4_header_options=jNone,
        ipv4_router_alert=jNone,
        ipv4_loose_source_route=jNone,
        ipv4_nop=jNone,
        ipv4_strict_source_route=jNone,
        ipv4_record_route=jNone,
        arp_dst_hw_step=jNone,
        arp_protocol_addr_length=jNone,
        arp_src_hw_step=jNone,
        data_pattern=jNone,
        data_pattern_mode=jNone,
        ether_type=jNone,
        ether_type_mode=jNone,
        ether_type_count=jNone,
        ether_type_step=jNone,
        global_dest_mac_retry_count=jNone,
        global_dest_mac_retry_delay=jNone,
        global_enable_mac_change_on_fly=jNone,
        global_enable_dest_mac_retry=jNone,
        ip_cost=jNone,
        ip_delay=jNone,
        ip_dscp_mode=jNone,
        vlan_protocol_tag_id=jNone,
        vlan_protocol_tag_id_mode=jNone,
        vlan_protocol_tag_id_count=jNone,
        vlan_protocol_tag_id_step=jNone,
        tcp_cwr_flag=jNone,
        tcp_cwr_flag_mode=jNone,
        tcp_ecn_echo_flag=jNone,
        tcp_ecn_echo_flag_mode=jNone,
        tcp_fin_flag_mode=jNone,
        tcp_psh_flag_mode=jNone,
        tcp_reserved_mode=jNone,
        tcp_reserved_count=jNone,
        tcp_reserved_step=jNone,
        vlan_user_priority_count=jNone,
        vlan_user_priority_mode=jNone,
        vlan_user_priority_step=jNone,
        ip_reliability=jNone,
        ip_throughput=jNone,
        gre_key_enable=jNone,
        gre_key=jNone,
        gre_seq_enable=jNone,
        gre_seq_number=jNone,
        gre_checksum_enable=jNone,
        gre_checksum=jNone,
        gre_reserved1=jNone,
        gre_version=jNone,
        l3_outer_protocol=jNone,
        tcp_ack_flag_mode=jNone,
        tcp_ack_num_mode=jNone,
        tcp_ack_num_count=jNone,
        tcp_ack_num_step=jNone,
        ip_ecn=jNone,
        **kwargs):

    """
    :param rt_handle:       RT object
    :param arp_dst_hw_addr
    :param arp_dst_hw_count
    :param arp_dst_hw_mode - <fixed|increment|decrement>
    :param arp_operation - <arpRequest|arpReply|rarpRequest|rarpReply>
    :param arp_src_hw_addr
    :param arp_src_hw_count
    :param arp_src_hw_mode - <fixed|increment|decrement>
    :param bidirectional
    :param burst_loop_count
    :param emulation_dst_handle
    :param emulation_src_handle
    :param frame_size
    :param frame_size_max
    :param frame_size_min
    :param frame_size_step
    :param icmp_checksum
    :param icmp_code
    :param icmp_id
    :param icmp_seq
    :param icmp_type
    :param igmp_group_addr
    :param igmp_group_count
    :param igmp_group_mode
    :param igmp_group_step
    :param igmp_max_response_time
    :param igmp_msg_type
    :param igmp_multicast_src
    :param igmp_qqic
    :param igmp_qrv
    :param igmp_s_flag
    :param igmp_type
    :param igmp_version
    :param inner_ip_dst_addr
    :param inner_ip_dst_count
    :param inner_ip_dst_mode
    :param inner_ip_dst_step
    :param inner_ip_src_addr
    :param inner_ip_src_count
    :param inner_ip_src_mode
    :param inner_ip_src_step
    :param inter_stream_gap
    :param ip_checksum
    :param ip_dscp
    :param ip_dscp_count
    :param ip_dscp_step
    :param ip_dst_addr
    :param ip_dst_count
    :param ip_dst_mode
    :param ip_dst_step
    :param ip_fragment
    :param ip_fragment_offset
    :param ip_fragment_last
    :param ip_hdr_length
    :param ip_id
    :param ip_precedence
    :param ip_precedence_count
    :param ip_precedence_step
    :param ip_protocol
    :param ip_src_addr
    :param ip_src_count
    :param ip_src_mode
    :param ip_src_step
    :param ip_ttl
    :param ipv6_auth_payload_len
    :param ipv6_auth_seq_num
    :param ipv6_auth_spi
    :param ipv6_auth_string
    :param ipv6_dst_addr
    :param ipv6_dst_count
    :param ipv6_dst_mode - <fixed|random|increment|decrement>
    :param ipv6_dst_step
    :param ipv6_extension_header
    :param ipv6_frag_id
    :param ipv6_frag_more_flag
    :param ipv6_frag_offset
    :param ipv6_hop_by_hop_options
    :param ipv6_hop_limit
    :param ipv6_next_header
    :param ipv6_routing_node_list
    :param ipv6_routing_res
    :param ipv6_src_addr
    :param ipv6_src_count
    :param ipv6_src_mode - <fixed|random|increment|decrement>
    :param ipv6_src_step
    :param ipv6_traffic_class
    :param l2_encap
    :param l3_imix1_ratio
    :param l3_imix1_size
    :param l3_imix2_ratio
    :param l3_imix2_size
    :param l3_imix3_ratio
    :param l3_imix3_size
    :param l3_imix4_ratio
    :param l3_imix4_size
    :param l3_length
    :param l3_length_max
    :param l3_length_min
    :param l3_protocol
    :param l4_protocol
    :param length_mode
    :param mac_dst
    :param mac_dst2
    :param mac_dst_count
    :param mac_dst_mode
    :param mac_dst_step
    :param mac_src
    :param mac_src2
    :param mac_src_count
    :param mac_src_mode
    :param mac_src_step
    :param mode - <create|modify|remove|enable|disable|reset|append_header>
    :param mpls_bottom_stack_bit
    :param mpls_labels
    :param mpls_labels_count
    :param mpls_labels_mode
    :param mpls_labels_step
    :param mpls_ttl
    :param name
    :param pkts_per_burst
    :param port_handle
    :param port_handle2
    :param rate_bps
    :param rate_percent
    :param rate_pps
    :param stream_id
    :param tcp_ack_flag
    :param tcp_ack_num
    :param tcp_checksum
    :param tcp_data_offset
    :param tcp_dst_port_count
    :param tcp_dst_port_mode - <increment:incr|decrement:decr>
    :param tcp_dst_port_step
    :param tcp_fin_flag
    :param tcp_psh_flag
    :param tcp_reserved
    :param tcp_rst_flag
    :param tcp_seq_num
    :param tcp_src_port
    :param tcp_src_port_count
    :param tcp_src_port_mode - <increment:incr|decrement:decr>
    :param tcp_src_port_step
    :param tcp_syn_flag
    :param tcp_urg_flag
    :param tcp_urgent_ptr
    :param tcp_window
    :param transmit_mode
    :param udp_checksum
    :param udp_dst_port
    :param udp_dst_port_count
    :param udp_dst_port_mode - <increment:incr|decrement:decr>
    :param udp_dst_port_step
    :param udp_src_port
    :param udp_src_port_count
    :param udp_src_port_mode - <increment:incr|decrement:decr>
    :param udp_src_port_step
    :param vci
    :param vci_count
    :param vci_step
    :param vlan_cfi
    :param vlan_id
    :param vlan_id_mode
    :param vlan_id_step
    :param vlan_user_priority
    :param vpi
    :param vpi_count
    :param vpi_step
    :param emulation_multicast_dst_handle
    :param emulation_multicast_dst_handle_type
    :param tcp_dst_port
    :param ip_precedence_mode - <increment:incr|decrement:decr>
    :param fcs_error
    :param rate_mbps
    :param arp_dst_protocol_addr
    :param arp_dst_protocol_addr_count
    :param arp_dst_protocol_addr_mode
    :param arp_dst_protocol_addr_step
    :param arp_src_protocol_addr
    :param arp_src_protocol_addr_count
    :param arp_src_protocol_addr_mode
    :param arp_src_protocol_addr_step
    :param icmpv6_type
    :param icmpv6_pointer
    :param icmpv6_target_address
    :param icmpv6_oflag
    :param icmpv6_rflag
    :param icmpv6_sflag
    :param icmpv6_suppress_flag
    :param icmpv6_max_resp_delay
    :param icmpv6_mcast_addr
    :param icmpv6_prefix_option_valid_lifetime
    :param icmpv6_dest_address
    :param icmpv6_qqic
    :param icmpv6_qrv
    :param vlan_id_count
    :param mpls_exp_bit
    :param icmpv6_code
    :param high_speed_result_analysis
    :param enable_stream
    :param ipv4_header_options
    :param ipv4_router_alert
    :param ipv4_loose_source_route
    :param ipv4_nop
    :param ipv4_strict_source_route
    :param ipv4_record_route
    :param arp_dst_hw_step
    :param arp_protocol_addr_length
    :param arp_src_hw_step
    :param data_pattern
    :param data_pattern_mode - <constant:fixed|incr:incr_byte|decr:decr_byte>
    :param ether_type
    :param ether_type_mode
    :param ether_type_count
    :param ether_type_step
    :param global_dest_mac_retry_count
    :param global_dest_mac_retry_delay
    :param global_enable_mac_change_on_fly
    :param global_enable_dest_mac_retry - <1>
    :param ip_cost
    :param ip_delay
    :param ip_dscp_mode
    :param vlan_protocol_tag_id
    :param vlan_protocol_tag_id_mode
    :param vlan_protocol_tag_id_count
    :param vlan_protocol_tag_id_step
    :param tcp_cwr_flag
    :param tcp_cwr_flag_mode
    :param tcp_ecn_echo_flag
    :param tcp_ecn_echo_flag_mode
    :param tcp_fin_flag_mode
    :param tcp_psh_flag_mode
    :param tcp_reserved_mode
    :param tcp_reserved_count
    :param tcp_reserved_step
    :param vlan_user_priority_count
    :param vlan_user_priority_mode - <fixed|increment:incr|decrement:decr>
    :param vlan_user_priority_step
    :param ip_reliability
    :param ip_throughput
    :param gre_key_enable
    :param gre_key
    :param gre_seq_enable
    :param gre_seq_number
    :param gre_checksum_enable
    :param gre_checksum
    :param gre_reserved1
    :param gre_version
    :param l3_outer_protocol
    :param tcp_ack_flag_mode
    :param tcp_ack_num_mode
    :param tcp_ack_num_count
    :param tcp_ack_num_step
    :param tcp_rst_flag_mode
    :param tcp_seq_num_mode
    :param tcp_syn_flag_mode
    :param tcp_urg_flag_mode
    :param tcp_urgent_ptr_mode
    :param tcp_urgent_ptr_count
    :param tcp_urgent_ptr_step
    :param tcp_window_mode
    :param tcp_window_count
    :param tcp_window_step
    :param vlan_cfi_mode
    :param vlan_cfi_count
    :param vlan_cfi_step
    :param ipv6_flow_label
    :param disable_signature
    :param ip_dst_outer_addr
    :param ip_dst_outer_count
    :param ip_outer_dscp
    :param ip_outer_dscp_count
    :param ip_outer_dscp_step
    :param ip_dst_outer_mode
    :param ip_dst_outer_step
    :param ip_fragment_outer_offset
    :param ip_hdr_outer_length
    :param ip_outer_checksum
    :param ip_outer_ttl
    :param ip_outer_id
    :param ip_outer_protocol
    :param ip_outer_precedence
    :param ip_outer_precedence_mode
    :param ip_outer_precedence_count
    :param ip_outer_precedence_step
    :param ip_src_outer_addr
    :param ip_src_outer_count
    :param ip_src_outer_mode
    :param ip_src_outer_step
    :param ipv6_dst_outer_count
    :param ipv6_dst_outer_mode
    :param ipv6_dst_outer_step
    :param ipv6_src_outer_count
    :param ipv6_src_outer_mode
    :param ipv6_src_outer_step
    :param ipv6_outer_src_addr
    :param ipv6_outer_dst_addr
    :param ipv6_outer_hop_limit
    :param ipv6_outer_traffic_class
    :param ipv6_outer_next_header
    :param ipv6_outer_flow_label
    :param ether_type_tracking
    :param ip_precedence_tracking
    :param tcp_ack_num_tracking
    :param tcp_cwr_flag_tracking
    :param tcp_dst_port_tracking
    :param tcp_ecn_echo_flag_tracking
    :param tcp_fin_flag_tracking
    :param tcp_psh_flag_tracking
    :param tcp_reserved_tracking
    :param tcp_rst_flag_tracking
    :param tcp_seq_num_tracking
    :param tcp_src_port_tracking
    :param tcp_syn_flag_tracking
    :param tcp_urg_flag_tracking
    :param tcp_urgent_ptr_tracking
    :param vlan_id_tracking
    :param vlan_cfi_tracking
    :param vlan_protocol_tag_id_tracking
    :param tcp_window_tracking
    :param udp_dst_port_tracking
    :param udp_src_port_tracking
    :param tx_delay
    :param vlan_user_priority_tracking
    :param arp_hw_address_length
    :param arp_hw_address_length_mode
    :param arp_operation_mode
    :param arp_protocol_addr_length_mode
    :param ip_cost_tracking
    :param ip_delay_tracking
    :param ip_dst_tracking
    :param arp_protocol_addr_length_step
    :param arp_protocol_addr_length_count
    :param arp_hw_address_length_count
    :param arp_hw_address_length_step
    :param ip_fragment_last_mode
    :param ip_fragment_last_tracking
    :param ip_fragment_offset_mode
    :param ip_fragment_offset_tracking
    :param ip_id_mode
    :param ip_id_tracking
    :param src_dest_mesh
    :param tcp_ack_flag_tracking
    :param ip_protocol_mode
    :param ip_protocol_tracking
    :param ip_reliability_tracking
    :param ip_reserved
    :param ip_reserved_tracking
    :param ip_src_tracking
    :param ip_throughput_tracking
    :param ip_ttl_mode
    :param ip_ttl_tracking
    :param ipv6_dst_tracking
    :param ipv6_flow_label_mode
    :param ipv6_flow_label_tracking
    :param ipv6_hop_limit_mode
    :param ipv6_hop_limit_tracking
    :param ipv6_src_tracking
    :param ipv6_traffic_class_count
    :param ipv6_traffic_class_mode
    :param ipv6_traffic_class_step
    :param ipv6_traffic_class_tracking
    :param mac_dst_tracking
    :param mac_src_tracking
    :param ip_fragment_offset_count
    :param ip_fragment_offset_step
    :param ip_id_count
    :param ip_id_step
    :param ip_protocol_count
    :param ip_protocol_step
    :param ip_ttl_count
    :param ip_ttl_step
    :param ipv6_flow_label_count
    :param ipv6_flow_label_step
    :param ipv6_hop_limit_count
    :param ipv6_hop_limit_step
    :param custom_pattern
    :param ipv6_srcprefix
    :param ipv6_dstprefix
    :param ip_dscp_tracking
    :param mac_discovery_gw
    :param mac_discovery_gw_step
    :param icmpv6_link_layer_type
    :param icmpv6_link_layer_value
    :param icmpv6_link_layer_length
    :param icmpv6_prefix_option_prefix
    :param icmpv6_prefix_option_length
    :param icmpv6_prefix_option_prefix_len
    :param icmpv6_prefix_option_abit
    :param icmpv6_prefix_option_lbit
    :param icmpv6_prefix_option_preferred_lifetime
    :param icmpv6_prefix_option_prefix_len
    :param icmpv6_prefix_option_reserved1
    :param icmpv6_prefix_option_reserved2
    :param icmpv6_prefix_option_type
    :param icmpv6_prefix_option_valid_lifetime
    :param icmpv6_mtu_option_mtu
    :param icmpv6_mtu_option_type
    :param icmpv6_mtu_option_length
    :param icmpv6_mtu_option_reserved
    :param icmpv6_ip_hop_limit
    :param icmpv6_redirect_hdr_type
    :param icmpv6_redirect_hdr_length
    :param icmpv6_redirect_hdr_reserved1
    :param icmpv6_redirect_hdr_reserved2
    :param route_mesh - <fully|one_to_one>
    :param l4_ip_dst_addr
    :param l4_ip_src_addr
    :param field_linked
    :param field_linked_to
    :param frame_rate_distribution_stream - <apply_to_all>
    :param dhcp_msg_header_type
    :param dhcp_cli_msg_client_addr
    :param dhcp_cli_msg_your_addr
    :param dhcp_cli_msg_cli_hw_client_hwa
    :param dhcp_cli_msg_type_code
    :param dhcp_cli_msg_hops
    :param dhcp_cli_msg_req_addr
    :param dhcp_srv_msg_type_code
    :param dhcp_srv_msg_next_serv_addr
    :param gtp
    :param gtp_protocol_type
    :param gtp_extended_header
    :param gtp_seq_num_flag
    :param gtp_n_pdu_flag
    :param gtp_message_type
    :param gtp_te_id 
    :param start_protocol - <0|1>
    :param gtp_te_id_count
    :param gtp_te_id_step
    :param ipv6_next_header_mode
    :param ipv6_next_header_count
    :param ipv6_next_header_step
    :param icmpv6_cur_hoplimit
    :param icmpv6_mbit
    :param icmpv6_obit
    :param icmpv6_reachable_time
    :param icmpv6_retrans_time
    :param icmpv6_router_lifetime
    :param router_adv_reserved
    :param qos_type
    :param qos_value
    :param qos_value_mode
    :param tx_port_sending_traffic_to_self_en - <true:1|false:0>
    :param ip_ecn - <00|01|10|11>
    :param disable_flow_tracking


    Spirent Returns:
    {
        "status": "1",
        "stream_handles": [
            "streamblock1",
            "streamblock2"
        ],
        "stream_id": {
            "port1": "streamblock2",
            "port2": "streamblock1"
        }
    }


    IXIA Returns:
    {
        "::ixNet::OBJ-/traffic/trafficItem:1/configElement:1": {
            "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1": {
                "headers": "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:\"ethernet-1\" ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:\"ipv4-2\" ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:\"fcs-3\""
            },
            "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:2": {
                "headers": "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:2/stack:\"ethernet-1\" ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:2/stack:\"ipv4-2\" ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:2/stack:\"fcs-3\""
            },
            "encapsulation_name": "Ethernet.IPv4",
            "endpoint_set_id": "1",
            "headers": "::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:\"ethernet-1\" ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:\"ipv4-2\" ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:\"fcs-3\"",
            "stream_ids": "::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1 ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:2"
        },
        "log": "",
        "status": "1",
        "stream_handles": [
            "TI0-HLTAPI_TRAFFICITEM_540"
        ],
        "stream_id": "TI0-HLTAPI_TRAFFICITEM_540",
        "traffic_item": "::ixNet::OBJ-/traffic/trafficItem:1/configElement:1"
    }

    Common Return Keys:
        "status"
        "stream_handles"
        "stream_id"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    native_args = dict()
    more_args = dict()
    args['arp_dst_hw_addr'] = arp_dst_hw_addr
    args['arp_dst_hw_count'] = arp_dst_hw_count
    args['arp_dst_hw_mode'] = arp_dst_hw_mode
    args['arp_operation'] = arp_operation
    args['arp_src_hw_addr'] = arp_src_hw_addr
    args['arp_src_hw_count'] = arp_src_hw_count
    args['arp_src_hw_mode'] = arp_src_hw_mode
    args['bidirectional'] = bidirectional
    args['burst_loop_count'] = burst_loop_count
    args['emulation_dst_handle'] = emulation_dst_handle
    args['emulation_src_handle'] = emulation_src_handle
    args['frame_size'] = frame_size
    args['frame_size_max'] = frame_size_max
    args['frame_size_min'] = frame_size_min
    args['frame_size_step'] = frame_size_step
    args['icmp_checksum'] = icmp_checksum
    args['icmp_code'] = icmp_code
    args['icmp_id'] = icmp_id
    args['icmp_seq'] = icmp_seq
    args['icmp_type'] = icmp_type
    args['igmp_group_addr'] = igmp_group_addr
    args['igmp_group_count'] = igmp_group_count
    args['igmp_group_mode'] = igmp_group_mode
    args['igmp_group_step'] = igmp_group_step
    args['igmp_max_response_time'] = igmp_max_response_time
    args['igmp_msg_type'] = igmp_msg_type
    args['igmp_multicast_src'] = igmp_multicast_src
    args['igmp_qqic'] = igmp_qqic
    args['igmp_qrv'] = igmp_qrv
    args['igmp_s_flag'] = igmp_s_flag
    args['igmp_type'] = igmp_type
    args['igmp_version'] = igmp_version
    args['inner_ip_dst_addr'] = inner_ip_dst_addr
    args['inner_ip_dst_count'] = inner_ip_dst_count
    args['inner_ip_dst_mode'] = inner_ip_dst_mode
    args['inner_ip_dst_step'] = inner_ip_dst_step
    args['inner_ip_src_addr'] = inner_ip_src_addr
    args['inner_ip_src_count'] = inner_ip_src_count
    args['inner_ip_src_mode'] = inner_ip_src_mode
    args['inner_ip_src_step'] = inner_ip_src_step
    args['inter_stream_gap'] = inter_stream_gap
    args['ip_checksum'] = ip_checksum
    args['ip_dscp'] = ip_dscp
    args['ip_dscp_count'] = ip_dscp_count
    args['ip_dscp_step'] = ip_dscp_step
    args['ip_dst_addr'] = ip_dst_addr
    args['ip_dst_count'] = ip_dst_count
    args['ip_dst_mode'] = ip_dst_mode
    args['ip_dst_step'] = ip_dst_step
    args['ip_fragment'] = ip_fragment
    args['ip_fragment_offset'] = ip_fragment_offset
    args['mf_bit'] = ip_fragment_last
    args['ip_hdr_length'] = ip_hdr_length
    args['ip_id'] = ip_id
    args['ip_precedence'] = ip_precedence
    args['ip_precedence_count'] = ip_precedence_count
    args['ip_precedence_step'] = ip_precedence_step
    args['ip_protocol'] = ip_protocol
    args['ip_src_addr'] = ip_src_addr
    args['ip_src_count'] = ip_src_count
    args['ip_src_mode'] = ip_src_mode
    args['ip_src_step'] = ip_src_step
    args['ip_ttl'] = ip_ttl
    args['ipv6_auth_payload_len'] = ipv6_auth_payload_len
    args['ipv6_auth_seq_num'] = ipv6_auth_seq_num
    args['ipv6_auth_spi'] = ipv6_auth_spi
    args['ipv6_auth_string'] = ipv6_auth_string
    args['ipv6_dst_addr'] = ipv6_dst_addr
    args['ipv6_dst_count'] = ipv6_dst_count
    args['ipv6_dst_mode'] = ipv6_dst_mode
    args['ipv6_dst_step'] = ipv6_dst_step
    args['ipv6_extension_header'] = ipv6_extension_header
    args['ipv6_frag_id'] = ipv6_frag_id
    args['ipv6_frag_more_flag'] = ipv6_frag_more_flag
    args['ipv6_frag_offset'] = ipv6_frag_offset
    args['ipv6_hop_by_hop_options'] = ipv6_hop_by_hop_options
    args['ipv6_hop_limit'] = ipv6_hop_limit
    #args['ipv6_next_header'] = ipv6_next_header
    args['ipv6_routing_node_list'] = ipv6_routing_node_list
    args['ipv6_routing_res'] = ipv6_routing_res
    args['ipv6_src_addr'] = ipv6_src_addr
    args['ipv6_src_count'] = ipv6_src_count
    args['ipv6_src_mode'] = ipv6_src_mode
    args['ipv6_src_step'] = ipv6_src_step
    args['ipv6_traffic_class'] = ipv6_traffic_class
    args['l2_encap'] = l2_encap
    args['l3_imix1_ratio'] = l3_imix1_ratio
    args['l3_imix1_size'] = l3_imix1_size
    args['l3_imix2_ratio'] = l3_imix2_ratio
    args['l3_imix2_size'] = l3_imix2_size
    args['l3_imix3_ratio'] = l3_imix3_ratio
    args['l3_imix3_size'] = l3_imix3_size
    args['l3_imix4_ratio'] = l3_imix4_ratio
    args['l3_imix4_size'] = l3_imix4_size
    args['l3_length'] = l3_length
    args['l3_length_max'] = l3_length_max
    args['l3_length_min'] = l3_length_min
    args['l3_protocol'] = l3_protocol
    args['l4_protocol'] = l4_protocol
    args['length_mode'] = length_mode
    args['mac_dst'] = mac_dst
    args['mac_dst2'] = mac_dst2
    args['mac_dst_count'] = mac_dst_count
    args['mac_dst_mode'] = mac_dst_mode
    args['mac_dst_step'] = mac_dst_step
    args['mac_src'] = mac_src
    args['mac_src2'] = mac_src2
    args['mac_src_count'] = mac_src_count
    args['mac_src_mode'] = mac_src_mode
    args['mac_src_step'] = mac_src_step
    args['mode'] = mode
    args['mpls_bottom_stack_bit'] = mpls_bottom_stack_bit
    args['mpls_labels'] = mpls_labels
    args['mpls_labels_count'] = mpls_labels_count
    args['mpls_labels_mode'] = mpls_labels_mode
    args['mpls_labels_step'] = mpls_labels_step
    args['mpls_ttl'] = mpls_ttl
    args['name'] = name
    args['pkts_per_burst'] = pkts_per_burst
    args['port_handle'] = port_handle
    args['port_handle2'] = port_handle2
    args['rate_bps'] = rate_bps
    args['rate_percent'] = rate_percent
    args['rate_pps'] = rate_pps
    args['stream_id'] = stream_id
    args['tcp_ack_flag'] = tcp_ack_flag
    args['tcp_ack_num'] = tcp_ack_num
    args['tcp_checksum'] = tcp_checksum
    args['tcp_data_offset'] = tcp_data_offset
    args['tcp_dst_port_count'] = tcp_dst_port_count
    args['tcp_dst_port_mode'] = tcp_dst_port_mode
    args['tcp_dst_port_step'] = tcp_dst_port_step
    args['tcp_fin_flag'] = tcp_fin_flag
    args['tcp_psh_flag'] = tcp_psh_flag
    args['tcp_reserved'] = tcp_reserved
    args['tcp_rst_flag'] = tcp_rst_flag
    args['tcp_seq_num'] = tcp_seq_num
    args['tcp_src_port'] = tcp_src_port
    args['tcp_src_port_count'] = tcp_src_port_count
    args['tcp_src_port_mode'] = tcp_src_port_mode
    args['tcp_src_port_step'] = tcp_src_port_step
    args['tcp_syn_flag'] = tcp_syn_flag
    args['tcp_urg_flag'] = tcp_urg_flag
    args['tcp_urgent_ptr'] = tcp_urgent_ptr
    args['tcp_window'] = tcp_window
    args['transmit_mode'] = transmit_mode
    args['udp_checksum'] = udp_checksum
    args['udp_dst_port'] = udp_dst_port
    args['udp_dst_port_count'] = udp_dst_port_count
    args['udp_dst_port_mode'] = udp_dst_port_mode
    args['udp_dst_port_step'] = udp_dst_port_step
    args['udp_src_port'] = udp_src_port
    args['udp_src_port_count'] = udp_src_port_count
    args['udp_src_port_mode'] = udp_src_port_mode
    args['udp_src_port_step'] = udp_src_port_step
    args['vci'] = vci
    args['vci_count'] = vci_count
    args['vci_step'] = vci_step
    args['vlan_cfi'] = vlan_cfi
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['vpi'] = vpi
    args['vpi_count'] = vpi_count
    args['vpi_step'] = vpi_step
    args['pkts_per_burst_sb'] = pkts_per_burst
    args['tcp_dst_port'] = tcp_dst_port
    args['ip_precedence_mode'] = ip_precedence_mode
    args['fcs_error'] = fcs_error
    args['rate_mbps'] = rate_mbps
    args['icmpv6_type'] = icmpv6_type
    args['icmpv6_pointer'] = icmpv6_pointer
    args['icmpv6_target_address'] = icmpv6_target_address
    args['icmpv6_oflag'] = icmpv6_oflag
    args['icmpv6_rflag'] = icmpv6_rflag
    args['icmpv6_sflag'] = icmpv6_sflag
    args['icmpv6_suppress_flag'] = icmpv6_suppress_flag
    args['icmpv6_max_resp_delay'] = icmpv6_max_resp_delay
    args['icmpv6_mcast_addr'] = icmpv6_mcast_addr
    args['icmpv6_prefix_option_valid_lifetime'] = icmpv6_prefix_option_valid_lifetime
    args['icmpv6_dest_address'] = icmpv6_dest_address
    args['icmpv6_qqic'] = icmpv6_qqic
    args['icmpv6_qrv'] = icmpv6_qrv
    args['vlan_id_count'] = vlan_id_count
    args['mpls_cos'] = mpls_exp_bit
    args['icmpv6_code'] = icmpv6_code
    args['high_speed_result_analysis'] = high_speed_result_analysis
    args['enable_stream'] = enable_stream
    args['ipv4_header_options'] = ipv4_header_options
    args['ipv4_router_alert'] = ipv4_router_alert
    args['ipv4_loose_source_route'] = ipv4_loose_source_route
    args['ipv4_nop'] = ipv4_nop
    args['ipv4_strict_source_route'] = ipv4_strict_source_route
    args['ipv4_record_route'] = ipv4_record_route
    args['arp_dst_hw_step'] = arp_dst_hw_step
    args['arp_src_hw_step'] = arp_src_hw_step
    native_args['arp_protocol_addr_length'] = arp_protocol_addr_length
    args['fill_value'] = data_pattern
    args['data_pattern_mode'] = data_pattern_mode
    args['ether_type'] = ether_type
    native_args['ether_type_mode'] = ether_type_mode
    native_args['ether_type_count'] = ether_type_count
    native_args['ether_type_step'] = ether_type_step
    args['ip_dscp_mode'] = ip_dscp_mode
    native_args['global_dest_mac_retry_count'] = global_dest_mac_retry_count
    native_args['global_dest_mac_retry_delay'] = global_dest_mac_retry_delay
    native_args['global_enable_mac_change_on_fly'] = global_enable_mac_change_on_fly
    native_args['ip_cost'] = ip_cost
    native_args['ip_delay'] = ip_delay
    args['vlan_tpid'] = vlan_protocol_tag_id
    native_args['vlan_protocol_tag_id_mode'] = vlan_protocol_tag_id_mode
    native_args['vlan_protocol_tag_id_count'] = vlan_protocol_tag_id_count
    native_args['vlan_protocol_tag_id_step'] = vlan_protocol_tag_id_step
    args['tcp_cwr_flag'] = tcp_cwr_flag
    native_args['tcp_cwr_flag_mode'] = tcp_cwr_flag_mode
    args['tcp_ecn_echo_flag'] = tcp_ecn_echo_flag
    native_args['tcp_ecn_echo_flag_mode'] = tcp_ecn_echo_flag_mode
    native_args['tcp_fin_flag_mode'] = tcp_fin_flag_mode
    native_args['tcp_psh_flag_mode'] = tcp_psh_flag_mode
    native_args['tcp_reserved_mode'] = tcp_reserved_mode
    native_args['tcp_reserved_count'] = tcp_reserved_count
    native_args['tcp_reserved_step'] = tcp_reserved_step
    args['vlan_priority_count'] = vlan_user_priority_count
    args['vlan_user_priority_mode'] = vlan_user_priority_mode
    args['vlan_priority_step'] = vlan_user_priority_step
    native_args['ip_reliability'] = ip_reliability
    native_args['ip_throughput'] = ip_throughput
    native_args['gre_key_enable'] = gre_key_enable
    native_args['gre_key'] = gre_key
    native_args['gre_seq_enable'] = gre_seq_enable
    native_args['gre_seq_number'] = gre_seq_number
    native_args['gre_checksum_enable'] = gre_checksum_enable
    native_args['gre_checksum'] = gre_checksum
    native_args['gre_reserved1'] = gre_reserved1
    native_args['gre_version'] = gre_version
    args['l3_outer_protocol'] = l3_outer_protocol
    native_args['tcp_ack_flag_mode'] = tcp_ack_flag_mode
    native_args['tcp_ack_num_mode'] = tcp_ack_num_mode
    native_args['tcp_ack_num_count'] = tcp_ack_num_count
    native_args['tcp_ack_num_step'] = tcp_ack_num_step

    more_args['tcp_rst_flag_mode'] = 'native'
    more_args['tcp_seq_num_mode'] = 'native'
    more_args['tcp_syn_flag_mode'] = 'native'
    more_args['tcp_urg_flag_mode'] = 'native'
    more_args['tcp_urgent_ptr_mode'] = 'native'
    more_args['tcp_urgent_ptr_count'] = 'native'
    more_args['tcp_urgent_ptr_step'] = 'native'
    more_args['tcp_window_mode'] = 'native'
    more_args['tcp_window_count'] = 'native'
    more_args['tcp_window_step'] = 'native'
    more_args['vlan_cfi_mode'] = 'native'
    more_args['vlan_cfi_count'] = 'native'
    more_args['vlan_cfi_step'] = 'native'
    more_args['ipv6_flow_label'] = 'hlt'
    more_args['disable_signature'] = 'hlt'
    more_args['ip_dst_outer_addr'] = 'hlt'
    more_args['ip_dst_outer_count'] = 'hlt'
    more_args['ip_outer_dscp'] = 'hlt'
    more_args['ip_outer_dscp_count'] = 'hlt'
    more_args['ip_outer_dscp_step'] = 'hlt'
    more_args['ip_dst_outer_mode'] = 'hlt'
    more_args['ip_dst_outer_step'] = 'hlt'
    more_args['ip_fragment_outer_offset'] = 'hlt'
    more_args['ip_hdr_outer_length'] = 'hlt'
    more_args['ip_outer_checksum'] = 'hlt'
    more_args['ip_outer_ttl'] = 'hlt'
    more_args['ip_outer_id'] = 'hlt'
    more_args['ip_outer_protocol'] = 'hlt'
    more_args['ip_outer_precedence'] = 'hlt'
    more_args['ip_outer_precedence_mode'] = 'hlt'
    more_args['ip_outer_precedence_count'] = 'hlt'
    more_args['ip_outer_precedence_step'] = 'hlt'
    more_args['ip_src_outer_addr'] = 'hlt'
    more_args['ip_src_outer_count'] = 'hlt'
    more_args['ip_src_outer_step'] = 'hlt'
    more_args['ip_src_outer_mode'] = 'hlt'
    more_args['ipv6_dst_outer_count'] = 'hlt'
    more_args['ipv6_dst_outer_mode'] = 'hlt'
    more_args['ipv6_dst_outer_step'] = 'hlt'
    more_args['ipv6_src_outer_count'] = 'hlt'
    more_args['ipv6_src_outer_step'] = 'hlt'
    more_args['ipv6_src_outer_mode'] = 'hlt'
    more_args['ipv6_outer_src_addr'] = 'hlt'
    more_args['ipv6_outer_dst_addr'] = 'hlt'
    more_args['ipv6_outer_hop_limit'] = 'hlt'
    more_args['ipv6_outer_traffic_class'] = 'hlt'
    more_args['ipv6_outer_next_header'] = 'hlt'
    more_args['ipv6_outer_flow_label'] = 'hlt'
    more_args['ether_type_tracking'] = 'native'
    more_args['ip_precedence_tracking'] = 'native'
    more_args['tcp_ack_num_tracking'] = 'native'
    more_args['tcp_cwr_flag_tracking'] = 'native'
    more_args['tcp_dst_port_tracking'] = 'native'
    more_args['tcp_ecn_echo_flag_tracking'] = 'native'
    more_args['tcp_fin_flag_tracking'] = 'native'
    more_args['tcp_psh_flag_tracking'] = 'native'
    more_args['tcp_reserved_tracking'] = 'native'
    more_args['tcp_rst_flag_tracking'] = 'native'
    more_args['tcp_seq_num_tracking'] = 'native'
    more_args['tcp_src_port_tracking'] = 'native'
    more_args['tcp_syn_flag_tracking'] = 'native'
    more_args['tcp_urg_flag_tracking'] = 'native'
    more_args['tcp_urgent_ptr_tracking'] = 'native'
    more_args['vlan_id_tracking'] = 'native'
    more_args['vlan_cfi_tracking'] = 'native'
    more_args['vlan_protocol_tag_id_tracking'] = 'native'
    more_args['tcp_window_tracking'] = 'native'
    more_args['udp_dst_port_tracking'] = 'native'
    more_args['udp_src_port_tracking'] = 'native'
    more_args['tx_delay'] = 'hlt'
    more_args['vlan_user_priority_tracking'] = 'native'
    more_args['arp_hw_address_length'] = 'native'
    more_args['arp_hw_address_length_mode'] = 'native'
    more_args['arp_operation_mode'] = 'native'
    more_args['arp_protocol_addr_length_mode'] = 'native'
    more_args['ip_cost_tracking'] = 'native'
    more_args['ip_delay_tracking'] = 'native'
    more_args['ip_dst_tracking'] = 'native'
    more_args['arp_protocol_addr_length_step'] = 'native'
    more_args['arp_protocol_addr_length_count'] = 'native'
    more_args['arp_hw_address_length_count'] = 'native'
    more_args['arp_hw_address_length_step'] = 'native'
    more_args['ip_fragment_last_mode'] = 'native'
    more_args['ip_fragment_last_tracking'] = 'native'
    more_args['ip_fragment_offset_mode'] = 'native'
    more_args['ip_fragment_offset_tracking'] = 'native'
    more_args['ip_id_mode'] = 'native'
    more_args['ip_id_tracking'] = 'native'
    more_args['src_dest_mesh'] = 'hlt'
    more_args['tcp_ack_flag_tracking'] = 'native'
    more_args['ip_protocol_mode'] = 'native'
    more_args['ip_protocol_tracking'] = 'native'
    more_args['ip_reliability_tracking'] = 'native'
    more_args['ip_reserved'] = 'native'
    more_args['ip_reserved_tracking'] = 'native'
    more_args['ip_src_tracking'] = 'native'
    more_args['ip_throughput_tracking'] = 'native'
    more_args['ip_ttl_mode'] = 'native'
    more_args['ip_ttl_tracking'] = 'native'
    more_args['ipv6_dst_tracking'] = 'native'
    more_args['ipv6_flow_label_mode'] = 'native'
    more_args['ipv6_flow_label_tracking'] = 'native'
    more_args['ipv6_hop_limit_mode'] = 'native'
    more_args['ipv6_hop_limit_tracking'] = 'native'
    more_args['ipv6_src_tracking'] = 'native'
    more_args['ipv6_traffic_class_count'] = 'native'
    more_args['ipv6_traffic_class_mode'] = 'native'
    more_args['ipv6_traffic_class_step'] = 'native'
    more_args['ipv6_traffic_class_tracking'] = 'native'
    more_args['mac_dst_tracking'] = 'native'
    more_args['mac_src_tracking'] = 'native'
    more_args['ip_fragment_offset_count'] = 'native'
    more_args['ip_fragment_offset_step'] = 'native'
    more_args['ip_id_count'] = 'native'
    more_args['ip_id_step'] = 'native'
    more_args['ip_protocol_count'] = 'native'
    more_args['ip_protocol_step'] = 'native'
    more_args['ip_ttl_count'] = 'native'
    more_args['ip_ttl_step'] = 'native'
    more_args['ipv6_flow_label_count'] = 'native'
    more_args['ipv6_flow_label_step'] = 'native'
    more_args['ipv6_hop_limit_count'] = 'native'
    more_args['ipv6_hop_limit_step'] = 'native'
    more_args['custom_pattern'] = 'hlt'
    more_args['ipv6_srcprefix'] = 'hlt'
    more_args['ipv6_dstprefix'] = 'hlt'
    more_args['ip_dscp_tracking'] = 'native'
    more_args['mac_discovery_gw'] = 'hlt'
    more_args['mac_discovery_gw_step'] = 'hlt'
    more_args['icmpv6_link_layer_type'] = 'hlt'
    more_args['icmpv6_link_layer_value'] = 'hlt'
    more_args['icmpv6_link_layer_length'] = 'hlt'
    more_args['icmpv6_prefix_option_prefix'] = 'hlt'
    more_args['icmpv6_prefix_option_length'] = 'hlt'
    more_args['icmpv6_prefix_option_prefix_len'] = 'hlt'
    more_args['icmpv6_prefix_option_abit'] = 'hlt'
    more_args['icmpv6_prefix_option_lbit'] = 'hlt'
    more_args['icmpv6_prefix_option_preferred_lifetime'] = 'hlt'
    more_args['icmpv6_prefix_option_prefix_len'] = 'hlt'
    more_args['icmpv6_prefix_option_reserved1'] = 'hlt'
    more_args['icmpv6_prefix_option_reserved2'] = 'hlt'
    more_args['icmpv6_prefix_option_type'] = 'hlt'
    more_args['icmpv6_prefix_option_valid_lifetime'] = 'hlt'
    more_args['icmpv6_mtu_option_mtu'] = 'hlt'
    more_args['icmpv6_mtu_option_type'] = 'hlt'
    more_args['icmpv6_mtu_option_length'] = 'hlt'
    more_args['icmpv6_mtu_option_reserved'] = 'hlt'
    more_args['icmpv6_ip_hop_limit'] = 'hlt'
    more_args['icmpv6_redirect_hdr_type'] = 'hlt'
    more_args['icmpv6_redirect_hdr_length'] = 'hlt'
    more_args['icmpv6_redirect_hdr_reserved1'] = 'hlt'
    more_args['icmpv6_redirect_hdr_reserved2'] = 'hlt'
    more_args['frame_rate_distribution_port'] = 'native'
    more_args['route_mesh'] = 'native'
    more_args['ethernet_pause'] = 'native'
    more_args['l4_ip_dst_addr'] = 'hlt'
    more_args['l4_ip_src_addr'] = 'hlt'
    more_args['field_linked'] = 'native'
    more_args['field_linked_to'] = 'native'
    more_args['frame_rate_distribution_stream'] = 'dummy'
    more_args['dhcp_msg_header_type'] = 'hlt'
    more_args['dhcp_cli_msg_client_addr'] = 'hlt'
    more_args['dhcp_cli_msg_your_addr'] = 'hlt'
    more_args['dhcp_cli_msg_cli_hw_client_hwa'] = 'hlt'
    more_args['dhcp_cli_msg_type_code'] = 'hlt'
    more_args['dhcp_cli_msg_hops'] = 'hlt'
    more_args['dhcp_cli_msg_req_addr'] = 'hlt'
    more_args['dhcp_srv_msg_type_code'] = 'hlt'
    more_args['dhcp_srv_msg_next_serv_addr'] = 'hlt'
    more_args['gtp'] = 'native'
    more_args['gtp_protocol_type'] = 'native'
    more_args['gtp_extended_header'] = 'native'
    more_args['gtp_seq_num_flag'] = 'native'
    more_args['gtp_n_pdu_flag'] = 'native'
    more_args['gtp_message_type'] = 'native'
    more_args['gtp_te_id'] = 'native'
    more_args['start_protocol'] = 'hlt'
    more_args['gtp_te_id_count'] = 'native'
    more_args['gtp_te_id_step'] = 'native'
    more_args['ipv6_next_header'] = 'native'
    more_args['ipv6_next_header_mode'] = 'native'
    more_args['ipv6_next_header_count'] = 'native'
    more_args['ipv6_next_header_step'] = 'native'
    more_args['icmpv6_cur_hoplimit'] = 'hlt'
    more_args['icmpv6_mbit'] = 'hlt'
    more_args['icmpv6_obit'] = 'hlt'
    more_args['icmpv6_reachable_time'] = 'hlt'
    more_args['icmpv6_retrans_time'] = 'hlt'
    more_args['icmpv6_router_lifetime'] = 'hlt'
    more_args['router_adv_reserved'] = 'hlt'
    more_args['qos_type'] = 'hlt'
    more_args['qos_value'] = 'hlt'
    more_args['qos_value_mode'] = 'hlt'
    more_args['tx_port_sending_traffic_to_self_en'] = 'hlt'
    args['ip_ecn'] = ip_ecn
    

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for arg in kwargs:
        arg = arg.strip()
        if arg not in more_args.keys():
            raise RuntimeError('Argument ', arg, ' is not supported by JHLT for j_traffic_config API')
        elif more_args[arg] == 'native':
            native_args[arg] = kwargs[arg]
        elif more_args[arg] == 'hlt':
            args[arg] = kwargs[arg]

        if arg.endswith('_tracking'):
            global_tracking[arg] = 1

        if arg == 'tx_delay':
            args['start_delay'] = args['tx_delay']
            del args['tx_delay']
        elif arg == 'src_dest_mesh':
            args['endpoint_map'] = args['src_dest_mesh']
            del args['src_dest_mesh']

    native_args = get_arg_value(rt_handle, j_traffic_config.__doc__, **native_args)
    args = get_arg_value(rt_handle, j_traffic_config.__doc__, **args)

    if 'port_handle2' in args.keys():
        if bidirectional == '0' or bidirectional == 'jNone' or int(args['bidirectional']) == 0:
            del args['port_handle2']
    
    if 'data_pattern_mode' in args:
        args['fill_type'] = args['data_pattern_mode']
        del args['data_pattern_mode']

    if 'ip_dscp_mode' in args:
        args['ip_tos_mode'] = args['ip_dscp_mode']
        del args['ip_dscp_mode']

    if 'vlan_user_priority_mode' in args:
        args['vlan_priority_mode'] = args['vlan_user_priority_mode']
        del args['vlan_user_priority_mode']

    if 'l3_protocol' in args and args['l3_protocol'] == 'ipv4':
        if 'ip_precedence' not in args:
            args['ip_precedence'] = '0'
    if 'qos_type' in args and 'qos_value' in args:
        if 'qos_value_mode' in args:
            if args['qos_value_mode'] == 'increment':
                args['ip_dscp_step'] = '1'
                del args['qos_value_mode']
            else:
                del args['qos_value_mode']
        if args['qos_value'] == 'dscp_default':
            args['ip_dscp'] = '0'
        elif args['qos_value'] == 'af_class1_low_precedence':
            args['ip_dscp'] = '10'
        elif args['qos_value'] == 'af_class1_medium_precedence':
            args['ip_dscp'] = '12'
        elif args['qos_value'] == 'af_class1_high_precedence' or args['qos_value'] == 'cs_precedence1':
            args['ip_dscp'] = '14'
        elif args['qos_value'] == 'af_class2_low_precedence':
            args['ip_dscp'] = '18'
        elif args['qos_value'] == 'af_class2_medium_precedence':
            args['ip_dscp'] = '20'
        elif args['qos_value'] == 'af_class2_high_precedence' or args['qos_value'] == 'cs_precedence2':
            args['ip_dscp'] = '22'
        elif args['qos_value'] == 'af_class3_low_precedence':
            args['ip_dscp'] = '26'
        elif args['qos_value'] == 'af_class3_medium_precedence':
            args['ip_dscp'] = '28'
        elif args['qos_value'] == 'af_class3_high_precedence' or args['qos_value'] == 'cs_precedence3':
            args['ip_dscp'] = '30'
        elif args['qos_value'] == 'af_class4_low_precedence':
            args['ip_dscp'] = '34'
        elif args['qos_value'] == 'af_class4_medium_precedence':
            args['ip_dscp'] = '36'
        elif args['qos_value'] == 'af_class4_high_precedence' or args['qos_value'] == 'cs_precedence4':
            args['ip_dscp'] = '38'
        elif args['qos_value'] == 'ef' or args['qos_value'] == 'cs_precedence5':
            args['ip_dscp'] = '46'
        elif args['qos_value'] == 'cs_precedence6':
            args['ip_dscp'] = '54'
        elif args['qos_value'] == 'cs_precedence7':
            args['ip_dscp'] = '62'
        del args['qos_value']
        del args['qos_type']

    if mode == 'create' or  mode == 'enable':
        if 'start_protocol' in args.keys():
            if int(args['start_protocol']) == 1:
                rt_handle.invoke('start_devices')
                del args['start_protocol']
            else:
                del args['start_protocol']
                
    if mode == 'enable' or mode == 'disable':
        if 'stream_id' in args.keys() and 'port_handle' in args.keys():
            args['stream_id'] = stream_id
            del args['port_handle']

    if 'mode' in args.keys() and mode == 'remove':
        if 'stream_id' not in args.keys() and 'port_handle' not in args.keys():
            raise RuntimeError('MiSSING ,MANDATORY ARGS, PASS EITHER stream_id OR port_handle')
        else:               
            args['mode'] = 'reset'
            args['port_handle'] = port_handle
            args['stream_id'] = stream_id
   
    if 'vlan_id_step' not in args.keys():
        vlan_id_step = 0

    if 'ip_ecn' in args.keys():
        if 'qos_type' not in more_args.keys() and 'qos_vlaue' not in more_args.keys():
            rt_handle.log("WARN","MISSING MANDATORY ARGS , PASS qos_type and qos_vlaue")

    if 'l3_protocol' in args and l3_protocol == "arp":
        args['ip_dst_addr'] = arp_dst_protocol_addr
        args['ip_dst_count'] = arp_dst_protocol_addr_count
        args['ip_dst_mode'] = arp_dst_protocol_addr_mode
        args['ip_dst_step'] = arp_dst_protocol_addr_step
        args['ip_src_addr'] = arp_src_protocol_addr
        args['ip_src_count'] = arp_src_protocol_addr_count
        args['ip_src_mode'] = arp_src_protocol_addr_mode
        args['ip_src_step'] = arp_src_protocol_addr_step


    args['enable_stream'] = 'TRUE' if 'enable_stream' not in args else args['enable_stream']
    native_args['enable_stream'] = args['enable_stream']

    if mode == 'create':
        __check_and_raise(port_handle)

    if 'frame_rate_distribution_port' in native_args and native_args['frame_rate_distribution_port'] == 'split_evenly':
        if 'bidirectional' in args and int(args['bidirectional']) == 1 and 'emulation_src_handle' in args and 'emulation_dst_handle' in args:
            if 'rate_pps' in args:
                del args['rate_pps']
            elif 'rate_bps' in args:
                del args['rate_bps']
            elif 'rate_mbps' in args:
                del args['rate_mbps']
            elif 'rate_kbps' in args:
                del args['rate_kbps']
            elif 'rate_percent' in args:
                del args['rate_percent']

    #if mode == 'create' and 'mac_discovery_gw' in args:
       #flag = 0
      #  for block_hndl in handle_map:
       #     if handle_map[block_hndl] == port_handle:
        #        flag = 1
         #       break
        #if not flag:
         #   raise RuntimeError('interface/emulated_device must be created before creating streamblocks for traffic')

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    for key in list(native_args.keys()):
        if native_args[key] == jNone:
            del native_args[key]


    if 'mf_bit' in args:
        args['mf_bit'] = int(not int(args['mf_bit']))

    if 'ipv4_header_options' in args.keys():
        if ipv4_header_options == 'router_alert':
            args['ip_router_alert'] = 1
        if ipv4_header_options == 'security' or ipv4_header_options == 'stream_id':
            del args['ipv4_header_options']

##MPLS exp_bit
    if mpls_exp_bit != jNone:
        if mpls_exp_bit == '0':
            args['mpls_cos'] = '000'
        elif mpls_exp_bit == '1':
            args['mpls_cos'] = '001'
        elif mpls_exp_bit == '2':
            args['mpls_cos'] = '010'
        elif mpls_exp_bit == '3':
            args['mpls_cos'] = '011'
        elif mpls_exp_bit == '4':
            args['mpls_cos'] = '100'
        elif mpls_exp_bit == '5':
            args['mpls_cos'] = '101'
        elif mpls_exp_bit == '6':
            args['mpls_cos'] = '110'
        elif mpls_exp_bit == '7':
            args['mpls_cos'] = '111'


###UDP source port repeat
    if udp_src_port_count != jNone or udp_src_port_mode != jNone or udp_src_port_step != jNone:
        args['udp_src_port_repeat_count'] = 0

    if 'mac_discovery_gw' not in args and 'emulation_src_handle' not in args and 'emulation_dst_handle' not in args and mode == 'create' and 'mac_dst' not in args:
        arp_resolved = rt_handle.invoke('arp_control', arp_target='all', arp_cache_retrieve=1)
        if arp_resolved['status'] != '1':
            raise RuntimeError('Failed to resolve the ARP')
        ip_address = jNone
        if 'ipv6_src_addr' in args:
            ip_address = args['ipv6_src_addr']
        elif 'ip_src_addr' in args:
            ip_address = args['ip_src_addr']

        if 'mac_src' in args and ip_address == jNone:
            hosts = rt_handle.invoke('invoke', cmd='stc::get project1 -children-EmulatedDevice')
            index = 1
            for host in hosts.split(' '):
                rt_handle.invoke('invoke', cmd='stc::get '+host+' -children')
                src_mac = rt_handle.invoke('invoke', cmd='stc::get ethiiif'+str(index)+' -SourceMac')
                if src_mac == args['mac_src']:
                    try:
                        result = rt_handle.invoke('invoke', cmd='stc::get ipv4if'+str(index)+' -Address')
                    except:
                        result = rt_handle.invoke('invoke', cmd='stc::get ipv6if'+str(index)+' -Address')
                    if(re.match(r'(\d+\.){1,3}\d+', result) or ':' in result):
                        ip_address = result
                        break
                index += 1
        for port in arp_resolved:
            if 'port' not in port:
                continue
            for arpnd_cache in arp_resolved[port]:
                for key in arp_resolved[port][arpnd_cache]:
                    if key == 'ip' and arp_resolved[port][arpnd_cache]['ip'] == ip_address:
                        args['mac_discovery_gw'] = arp_resolved[port][arpnd_cache]['gateway_ip']
                        break

    if not isinstance(emulation_dst_handle, list):
        emulation_dst_handle = [emulation_dst_handle]
    if not isinstance(emulation_src_handle, list):
        emulation_src_handle = [emulation_src_handle]

    if mode == 'create':
        args['emulation_dst_handle'] = ''
        args['emulation_src_handle'] = ''
        for hndl in emulation_dst_handle:
            if hndl in global_config:
                args['emulation_dst_handle'] = args['emulation_dst_handle'] + " " + " ".join(global_config[hndl])
            else:
                args['emulation_dst_handle'] = args['emulation_dst_handle'] + " " + hndl
        for hndl in emulation_src_handle:
            if hndl in global_config:
                args['emulation_src_handle'] = args['emulation_src_handle'] + " " + " ".join(global_config[hndl])
            else:
                args['emulation_src_handle'] = args['emulation_src_handle'] + " " + hndl
        args['emulation_dst_handle'] = args['emulation_dst_handle'].strip()
        args['emulation_src_handle'] = args['emulation_src_handle'].strip()

    if 'frame_size' in args and 'length_mode' not in args:
        args['length_mode'] = 'fixed'

    if 'vlan_id' in args:
        if not isinstance(vlan_id, list):
            args['vlan_id'] = vlan_id
            args['vlan_id_mode'] = vlan_id_mode
            args['vlan_user_priority'] = vlan_user_priority
            args['vlan_id_count'] = vlan_id_count
            args['vlan_cfi'] = vlan_cfi
        elif isinstance(vlan_id, list):
            if len(vlan_id) == 2:
                args['vlan_id'] = vlan_id[1]
                args['vlan_id_outer'] = vlan_id[0]
                if isinstance(vlan_id_count, list):
                    args['vlan_id_count'] = vlan_id_count[1]
                    args['vlan_id_outer_count'] = vlan_id_count[0]
                if isinstance(vlan_id_step, list):
                    args['vlan_id_step'] = vlan_id_step[1]
                    args['vlan_id_outer_count'] = vlan_id_count[0]
                if isinstance(vlan_id_mode, list):
                    args['vlan_id_mode'] = vlan_id_mode[1]
                    args['vlan_id_outer_mode'] = vlan_id_mode[0]
                if isinstance(vlan_user_priority, list):
                    args['vlan_user_priority'] = vlan_user_priority[1]
                    args['vlan_outer_user_priority'] = vlan_user_priority[0]
                if isinstance(vlan_cfi, list):
                    args['vlan_cfi'] = vlan_cfi[1]
                    args['vlan_outer_cfi'] = vlan_cfi[0]
            if len(vlan_id) == 3:
                args['vlan_id'] = vlan_id[2]
                args['vlan_id_outer'] = vlan_id[1]
                args['vlan_id_other'] = vlan_id[0]
                if isinstance(vlan_id_count, list):
                    args['vlan_id_count'] = vlan_id_count[2]
                    args['vlan_id_outer_count'] = vlan_id_count[1]
                    args['vlan_id_other_count'] = vlan_id_count[0]
                if isinstance(vlan_id_step, list):
                    args['vlan_id_step'] = vlan_id_step[2]
                    args['vlan_id_outer_step'] = vlan_id_step[1]
                    args['vlan_id_other_step'] = vlan_id_step[0]
                if isinstance(vlan_id_mode, list):
                    args['vlan_id_mode'] = vlan_id_mode[2]
                    args['vlan_id_outer_mode'] = vlan_id_mode[1]
                    args['vlan_id_other_mode'] = vlan_id_mode[0]
                if isinstance(vlan_user_priority, list):
                    args['vlan_user_priority'] = vlan_user_priority[2]
                    args['vlan_outer_user_priority'] = vlan_user_priority[1]
                    args['vlan_user_priority_other'] = vlan_user_priority[0]
                if isinstance(vlan_cfi, list):
                    args['vlan_cfi'] = vlan_cfi[2]
                    args['vlan_outer_cfi'] = vlan_cfi[1]
                    args['vlan_cfi_other'] = vlan_cfi[0]


    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    ipv6_extension_flag = 0
    if ipv6_extension_header == 'encapsulation':
        del args['ipv6_extension_header']
        ipv6_extension_flag = 1

## Below code creates hashing for field_linked and field_linked_to args, It works for tcp ports only currently
## Usage Eg : 'field_linked_to': ['streamblock1/stackLink:"tcp-4-dstPort-2"'], 'field_linked': ['streamblock1/stackLink:"tcp-4-srcPort-1"']
    if 'field_linked' in native_args and 'field_linked_to' in native_args:
        field_linked = native_args['field_linked'][0] if isinstance(native_args['field_linked'], list) else native_args['field_linked']
        src_port = field_linked.split('"')
        src_data = src_port[1].split('-')
        src_pdu_name = src_data[0]
        src_pdu_type = src_data[2]
        field_linked_to = native_args['field_linked_to'][0] if isinstance(native_args['field_linked_to'], list) else native_args['field_linked_to']
        dst_port = field_linked_to.split('"')
        dst_data = dst_port[1].split('-')
        dst_pdu_name = dst_data[0]
        dst_pdu_type = dst_data[2]
        if 'stream_id' in args:
            range_mod_list = rt_handle.invoke('invoke', cmd="stc::get "+args['stream_id']+" -children-rangemodifier").split()
            range_mod_header_map = {'tcp' : 'tcp'}
            range_mod_field_map = {'dstPort' : 'destPort', 'srcPort' : 'sourcePort'}
            for range_mod in range_mod_list:
                range_mod_type = rt_handle.invoke('invoke', cmd="stc::get "+range_mod+" -OffsetReference")
                if range_mod_header_map[src_pdu_name] in range_mod_type \
                    and range_mod_field_map[src_pdu_type] in range_mod_type:
                    # This is the field_linked parameter. Set enable stream as true
                    rt_handle.invoke('invoke', cmd="stc::config "+range_mod+" -EnableStream true")
                if range_mod_header_map[dst_pdu_name] in range_mod_type \
                    and range_mod_field_map[dst_pdu_type] in range_mod_type:
                    # This is the field_linked_to parameter. Set enable stream as false
                    rt_handle.invoke('invoke', cmd="stc::config "+range_mod+" -EnableStream false")
        del native_args['field_linked']
        del native_args['field_linked_to']
    if 'tcp_src_port_count' in args:
        args['tcp_src_port_repeat_count'] = 0
    if 'tcp_dst_port_count' in args:
        args['tcp_dst_port_repeat_count'] = 0

    if mode != 'append_header':
        ret = rt_handle.invoke('traffic_config', **args)
    else:
        ret = dict()
        if 'stream_id' in args:
            if 'l3_protocol' in args or 'l4_protocol' in args or 'l3_outer_protocol' in args:
                if l3_protocol == 'ipv4' or l4_protocol == 'ipv4' or l3_outer_protocol == 'ipv4':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create ipv4:ipv4 -under "+args['stream_id'])
                elif l3_protocol == 'ipv6' or l4_protocol == 'ipv6' or l3_outer_protocol == 'ipv6':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create ipv6:ipv6 -under "+args['stream_id'])
                elif l3_protocol == 'arp':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create arp:ARP -under "+args['stream_id'])
                elif l3_protocol == 'gre':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create gre:gre -under "+args['stream_id'])
                elif l4_protocol == 'udp':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create udp:udp -under "+args['stream_id'])
                elif l4_protocol == 'tcp':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create tcp:tcp -under "+args['stream_id'])
                elif l4_protocol == 'udp_dhcp_msg':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create udp_dhcp_msg:udp_dhcp_msg -under "+args['stream_id'])
                elif l4_protocol == 'icmp':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create icmp:icmp -under "+args['stream_id'])
                elif l4_protocol == 'icmpv6':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create icmpv6:icmpv6 -under "+args['stream_id'])
                elif l4_protocol == 'igmp':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create igmp:igmp -under "+args['stream_id'])
                elif l4_protocol == 'rtp':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create rtp:rtp -under "+args['stream_id'])
                elif l4_protocol == 'isis':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create isis:isis -under "+args['stream_id'])
                elif l4_protocol == 'ospf':
                    ret['header'] = rt_handle.invoke('invoke', cmd="stc::create ospf:ospf -under "+args['stream_id'])

            if ret['header'] is not None:
                del ret['header']
                ret['status'] = 1
                ret['stream_id'] = args['stream_id']
            else:
                raise RuntimeError('Failed to add header')

            return ret
    # ***** Return Value Modification *****

    if 'stream_id' in ret:
        ret['stream_handles'] = []
        if isinstance(ret['stream_id'], dict):
            if port_handle in ret['stream_id']:
                ret['stream_handles'].append(ret['stream_id'][port_handle])
            if port_handle2 in ret['stream_id']:
                ret['stream_handles'].append(ret['stream_id'][port_handle2])
        else:
            ret['stream_handles'].append(ret['stream_id'])

        if len(ret['stream_handles']) == 2:
            stream_map[ret['stream_handles'][0]] = ret['stream_handles'][1]
            stream_map[ret['stream_handles'][1]] = ret['stream_handles'][0]

    if mode == 'create' and 'frame_rate_distribution_port' in native_args and native_args['frame_rate_distribution_port'] == 'split_evenly':
        if 'bidirectional' in args and int(args['bidirectional']) == 1 and 'emulation_src_handle' in args and 'emulation_dst_handle' in args:
            count = 0
            for sh in ret['stream_handles']:
                result = rt_handle.invoke('invoke', cmd='stc::get '+sh+' -SrcBinding-targets')
                count += len(result.split(' '))
            rate_arg = dict()
            if rate_pps != jNone:
                rate_pps = int(rate_pps)/count
                rate_arg = {'mode' : 'modify', 'rate_pps' : int(rate_pps)}
            elif rate_bps != jNone:
                rate_bps = int(rate_bps)/count
                rate_arg = {'mode' : 'modify', 'rate_bps' : int(rate_bps)}
            elif rate_mbps != jNone:
                rate_mbps = int(rate_mpbs)/count
                rate_arg = {'mode' : 'modify', 'rate_mbps' : int(rate_mbps)}
            elif rate_kbps != jNone:
                rate_kbps = int(rate_kbps)/count
                rate_arg = {'mode' : 'modify', 'rate_kbps' : int(rate_kbps)}
            elif rate_percent != jNone:
                rate_percent = int(rate_percent)/count
                rate_arg = {'mode' : 'modify', 'rate_percent' : int(rate_percent)}
                
            for sh in ret['stream_handles']:
                rate_arg['stream_id'] = sh
                rt_handle.invoke('traffic_config', **rate_arg)
    if ipv6_extension_flag == 1:
        for hand in ret['stream_handles']:
            rt_handle.invoke('invoke', cmd='stc::create ipv6:Ipv6EncapsulationHeader -under '+hand)

##Native arguments pv4_header_options
    if ipv4_header_options == 'security':
        for hand in ret['stream_handles']:
            ip_header = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-ipv4:ipv4')
            options = rt_handle.invoke('invoke', cmd='stc::get '+ip_header+' -children-options')
            rt_handle.invoke('invoke', cmd='stc::create ipv4headeroption -under '+options)
            header_option = rt_handle.invoke('invoke', cmd='stc::get '+options+' -children-ipv4headeroption')
            rt_handle.invoke('invoke', cmd='stc::create security -under '+header_option)
    if ipv4_header_options == 'stream_id':
        for hand in ret['stream_handles']:
            ip_header = rt_handle.invoke('invoke', cmd='stc::get '+hand+' -children-ipv4:ipv4')
            options = rt_handle.invoke('invoke', cmd='stc::get '+ip_header+' -children-options')
            rt_handle.invoke('invoke', cmd='stc::create ipv4headeroption -under '+options)
            header_option = rt_handle.invoke('invoke', cmd='stc::get '+options+' -children-ipv4headeroption')
            rt_handle.invoke('invoke', cmd='stc::create streamid -under '+header_option)
            
    # ***** End of Return Value Modification *****
    #deleting native args which are already handled in above code
    if 'frame_rate_distribution_port' in native_args:
        del native_args['frame_rate_distribution_port']

    ## Native args execution starts
    if len(native_args) > 1 and 'mode' in args.keys() and (args['mode'] == 'create' or  args['mode'] == 'modify'):
        run_native_args(ret, rt_handle, **native_args)

    return ret


def j_traffic_control(
        rt_handle,
        action=jNone,
        duration=jNone,
        port_handle=jNone,
        db_file=jNone,
        enable_arp=jNone,
        stream_handle=jNone,
        delay_variation_enable=jNone,
        cpdp_convergence_enable=jNone,
        max_wait_timer=jNone,
        latency_control=jNone,
        latency_bins=jNone,
        latency_values=jNone):
    """
    :param rt_handle:       RT object
    :param action - <run|stop|reset|destroy|clear_stats|poll>
    :param duration
    :param port_handle
    :param db_file
    :param enable_arp
    :param stream_handle
    :param delay_variation_enable
    :param cpdp_convergence_enable
    :param max_wait_timer
    :param latency_control
    :param latency_bins
    :param latency_values

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    targs = dict()
    args = dict()
    args['action'] = action
    args['duration'] = duration
    args['port_handle'] = port_handle
    args['db_file'] = db_file
    args['enable_arp'] = enable_arp
    args['stream_handle'] = stream_handle
    args['elapsed_time'] = delay_variation_enable
    args['cpdp_convergence_enable'] = cpdp_convergence_enable
    args['max_wait_timer'] = max_wait_timer
    args['latency_control'] = latency_control
    args['latency_bins'] = latency_bins
    args['latency_values'] = latency_values

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****


    if args['enable_arp'] == jNone:
        args['enable_arp'] = 1

    args = get_arg_value(rt_handle, j_traffic_control.__doc__, **args)

    if action == 'sync_run':
        action = 'run'
        args['action'] = action
        
    if 'action' in args and args['action'] == 'run':
        if 'port_handle' in args:
            if not isinstance(port_handle, list):
                port_handle = [port_handle]
            port_handle = list(set(port_handle))
            for i in range(0,len(port_handle)):
                stream_count = 0
                stream_lists = rt_handle.invoke('invoke', cmd='stc::get' + " " + port_handle[i] + ' -children-streamblock').split(" ")
                stream_count = stream_count + len(stream_lists)
                if int(stream_count) > 0:
                    generator = rt_handle.invoke('invoke', cmd='stc::get' + " " + port_handle[i] + ' -children-Generator')
                    generatorconfig = rt_handle.invoke('invoke', cmd='stc::get' + " " + generator + ' -children-GeneratorConfig')
                    Durationmode    = rt_handle.invoke('invoke', cmd='stc::get' + " " + generatorconfig + ' -DurationMode')
                    Duration    = rt_handle.invoke('invoke', cmd='stc::get' + " " + generatorconfig + ' -Duration')
                    final_duration = int(stream_count) * int(Duration)
                    if Durationmode == 'BURSTS':
                        rt_handle.invoke('invoke', cmd='stc::config' + " " + generatorconfig + ' -Duration' + " " + str(final_duration))
                        rt_handle.invoke('invoke', cmd='stc::apply')
        else:
            stream_count = 0
            i=0
            port_lists = rt_handle.invoke('invoke', cmd='stc::get' + " " + 'project1 -children-port').split(" ")
            for port_element in port_lists:
                stream_lists = rt_handle.invoke('invoke', cmd='stc::get' + " " + port_element + ' -children-streamblock').split(" ")
                stream_count = stream_count + len(stream_lists)
            for port_element in port_lists:
                stream_lists = rt_handle.invoke('invoke', cmd='stc::get' + " " + port_element + ' -children-streamblock').split(" ")
                if 'streamblock' in stream_lists:
                    for stream_element in stream_lists:
                        targs['stream_id'] = stream_element
                        targs['mode'] = 'modify'
                        targs['burst_loop_count'] = stream_count
                        targs['pkts_per_burst'] = int(burst_count[i]) * int(packet_per_burst[i])
                        rt_handle.invoke('traffic_config', **targs)
                        i = i + 1

    #    args['port_handle'] = 'all'
    # *** Native Arguments Execution ****
    if 'cpdp_convergence_enable' in list(args.keys()):
        del args['cpdp_convergence_enable']
        if int(cpdp_convergence_enable) == 1:
            rt_handle.invoke('invoke', cmd='stc::create' + " " + 'ConvergenceGenParams' + ' -under project1' + ' -Active' + " " + 'TRUE')
            rt_handle.invoke('invoke', cmd='stc::apply')

    if 'max_wait_timer' in list(args.keys()):
        del args['max_wait_timer']
        rt_handle.invoke('invoke', cmd='stc::perform' + " " + 'GeneratorWaitForStartCommand' + ' -WaitTimeout' + " " + max_wait_timer)
        rt_handle.invoke('invoke', cmd='stc::apply')

    if 'latency_control' in list(args.keys()):
        del args['latency_control']
        if latency_control == 'store_and_forward':
            rt_handle.invoke('invoke', cmd='stc::create' + " " + 'Rfc2544BackToBackFramesConfig' + ' -under project1' + ' -LatencyType' + " " + 'LIFO')
        elif latency_control == 'mef_frame_delay':
            rt_handle.invoke('invoke', cmd='stc::create' + " " + 'Rfc2544BackToBackFramesConfig' + ' -under project1' + ' -LatencyType' + " " + 'LILO')
        elif latency_control == 'forwarding_delay':
            rt_handle.invoke('invoke', cmd='stc::create' + " " + 'Rfc2544BackToBackFramesConfig' + ' -under project1' + ' -LatencyType' + " " + 'FIFO')
        rt_handle.invoke('invoke', cmd='stc::apply')


    if action == 'run' and int(args['enable_arp']) == 1:
        n_args = dict()
        if 'stream_handle' in list(args.keys()):
            n_args['arp_target'] = 'stream'
            n_args['handle'] = stream_handle
            args['enable_arp'] = 0
        if 'port_handle' in list(args.keys()):
            n_args['arp_target'] = 'port'
            n_args['port_handle'] = port_handle
            args['enable_arp'] = 0
        else:
            n_args['arp_target'] = 'all'
        rt_handle.invoke('arp_control', **n_args)

    if 'port_handle' not in args.keys() and 'stream_handle' not in args.keys():
        args['port_handle'] = 'all'


    ret = rt_handle.invoke('traffic_control', **args)

    # ***** Return Value Modification *****

    # ***** End of Return Value Modification *****

    return ret


def j_traffic_stats(rt_handle, port_handle=jNone, mode=jNone, streams=jNone, scale_mode=jNone):
    """
    :param rt_handle:       RT object
    :param port_handle
    :param mode
    :param streams
    :param scale_mode

    Spirent Returns:
    {
        "port1": {
            "aggregate": {
                "rx": {
                    "fcoe_frame_count": "0",
                    "fcoe_frame_rate": "0",
                    "ip_pkts": "40",
                    "oversize_count": "0",
                    "oversize_rate": "0",
                    "pfc_frame_count": "0",
                    "pfc_frame_rate": "0",
                    "pkt_bit_rate": "0",
                    "pkt_byte_count": "4360",
                    "pkt_count": "20",
                    "pkt_rate": "0",
                    "raw_pkt_count": "40",
                    "tcp_checksum_errors": "0",
                    "tcp_pkts": "0",
                    "total_pkt_bytes": "4360",
                    "total_pkt_rate": "0",
                    "total_pkts": "40",
                    "udp_pkts": "0",
                    "undersize_count": "0",
                    "undersize_rate": "0",
                    "vlan_pkts_count": "0",
                    "vlan_pkts_rate": "0"
                },
                "tx": {
                    "ip_pkts": "20",
                    "pfc_frame_count": "",
                    "pkt_bit_rate": "0",
                    "pkt_byte_count": "4360",
                    "pkt_count": "20",
                    "pkt_rate": "0",
                    "raw_pkt_count": "40",
                    "raw_pkt_rate": "0",
                    "total_pkt_bytes": "4360",
                    "total_pkt_rate": "0",
                    "total_pkts": "40"
                }
            },
            "stream": {
                "streamblock2": {
                    "rx": {
                        "avg_delay": "4398.742",
                        "dropped_pkts": "0",
                        "duplicate_pkts": "0",
                        "first_tstamp": "0.0",
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "last_tstamp": "0.0",
                        "max_delay": "5396.31",
                        "max_pkt_length": "128",
                        "min_delay": "3617.53",
                        "min_pkt_length": "128",
                        "misinserted_pkts": "0",
                        "out_of_sequence_pkts": "0",
                        "prbs_bit_errors": "0",
                        "rx_port": "10.220.1.153-1-2 //1/2  10.220.1.153-1-2 //1/2 ",
                        "rx_sig_count": "10",
                        "rx_sig_rate": "0",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    },
                    "tx": {
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    }
                },
                "streamblock4": {
                    "rx": {
                        "avg_delay": "3991.514",
                        "dropped_pkts": "0",
                        "duplicate_pkts": "0",
                        "first_tstamp": "0.0",
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "last_tstamp": "0.0",
                        "max_delay": "7607.02",
                        "max_pkt_length": "128",
                        "min_delay": "2799.9",
                        "min_pkt_length": "128",
                        "misinserted_pkts": "0",
                        "out_of_sequence_pkts": "0",
                        "prbs_bit_errors": "0",
                        "rx_port": "10.220.1.153-1-2 //1/2  10.220.1.153-1-2 //1/2 ",
                        "rx_sig_count": "10",
                        "rx_sig_rate": "0",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    },
                    "tx": {
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    }
                }
            }
        },
        "port2": {
            "aggregate": {
                "rx": {
                    "fcoe_frame_count": "0",
                    "fcoe_frame_rate": "0",
                    "ip_pkts": "36",
                    "oversize_count": "0",
                    "oversize_rate": "0",
                    "pfc_frame_count": "0",
                    "pfc_frame_rate": "0",
                    "pkt_bit_rate": "0",
                    "pkt_byte_count": "4000",
                    "pkt_count": "20",
                    "pkt_rate": "0",
                    "raw_pkt_count": "36",
                    "tcp_checksum_errors": "0",
                    "tcp_pkts": "0",
                    "total_pkt_bytes": "4000",
                    "total_pkt_rate": "0",
                    "total_pkts": "36",
                    "udp_pkts": "0",
                    "undersize_count": "0",
                    "undersize_rate": "0",
                    "vlan_pkts_count": "0",
                    "vlan_pkts_rate": "0"
                },
                "tx": {
                    "ip_pkts": "20",
                    "pfc_frame_count": "",
                    "pkt_bit_rate": "0",
                    "pkt_byte_count": "4720",
                    "pkt_count": "20",
                    "pkt_rate": "0",
                    "raw_pkt_count": "44",
                    "raw_pkt_rate": "0",
                    "total_pkt_bytes": "4720",
                    "total_pkt_rate": "0",
                    "total_pkts": "44"
                }
            },
            "stream": {
                "streamblock1": {
                    "rx": {
                        "avg_delay": "14002.352",
                        "dropped_pkts": "0",
                        "duplicate_pkts": "0",
                        "first_tstamp": "0.0",
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "last_tstamp": "0.0",
                        "max_delay": "14919.78",
                        "max_pkt_length": "128",
                        "min_delay": "13072.44",
                        "min_pkt_length": "128",
                        "misinserted_pkts": "0",
                        "out_of_sequence_pkts": "0",
                        "prbs_bit_errors": "0",
                        "rx_port": "10.220.1.153-1-1 //1/1  10.220.1.153-1-1 //1/1 ",
                        "rx_sig_count": "10",
                        "rx_sig_rate": "0",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    },
                    "tx": {
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    }
                },
                "streamblock3": {
                    "rx": {
                        "avg_delay": "12167.942",
                        "dropped_pkts": "0",
                        "duplicate_pkts": "0",
                        "first_tstamp": "0.0",
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "last_tstamp": "0.0",
                        "max_delay": "12873.59",
                        "max_pkt_length": "128",
                        "min_delay": "11388.79",
                        "min_pkt_length": "128",
                        "misinserted_pkts": "0",
                        "out_of_sequence_pkts": "0",
                        "prbs_bit_errors": "0",
                        "rx_port": "10.220.1.153-1-1 //1/1  10.220.1.153-1-1 //1/1 ",
                        "rx_sig_count": "10",
                        "rx_sig_rate": "0",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    },
                    "tx": {
                        "ipv4_outer_present": "0",
                        "ipv4_present": "0",
                        "ipv6_outer_present": "0",
                        "ipv6_present": "1",
                        "tcp_present": "0",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_bytes": "1280",
                        "total_pkt_rate": "0",
                        "total_pkts": "10",
                        "udp_present": "0"
                    }
                }
            }
        },
        "status": "1",
        "traffic_item": {
            "streamblock1": {
                "rx": {
                    "avg_delay": "14002.352",
                    "dropped_pkts": "0",
                    "duplicate_pkts": "0",
                    "first_tstamp": "0.0",
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "last_tstamp": "0.0",
                    "max_delay": "14919.78",
                    "max_pkt_length": "128",
                    "min_delay": "13072.44",
                    "min_pkt_length": "128",
                    "misinserted_pkts": "0",
                    "out_of_sequence_pkts": "0",
                    "prbs_bit_errors": "0",
                    "rx_port": "10.220.1.153-1-1 //1/1  10.220.1.153-1-1 //1/1 ",
                    "rx_sig_count": "10",
                    "rx_sig_rate": "0",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                },
                "tx": {
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                }
            },
            "streamblock2": {
                "rx": {
                    "avg_delay": "4398.742",
                    "dropped_pkts": "0",
                    "duplicate_pkts": "0",
                    "first_tstamp": "0.0",
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "last_tstamp": "0.0",
                    "max_delay": "5396.31",
                    "max_pkt_length": "128",
                    "min_delay": "3617.53",
                    "min_pkt_length": "128",
                    "misinserted_pkts": "0",
                    "out_of_sequence_pkts": "0",
                    "prbs_bit_errors": "0",
                    "rx_port": "10.220.1.153-1-2 //1/2  10.220.1.153-1-2 //1/2 ",
                    "rx_sig_count": "10",
                    "rx_sig_rate": "0",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                },
                "tx": {
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                }
            },
            "streamblock3": {
                "rx": {
                    "avg_delay": "12167.942",
                    "dropped_pkts": "0",
                    "duplicate_pkts": "0",
                    "first_tstamp": "0.0",
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "last_tstamp": "0.0",
                    "max_delay": "12873.59",
                    "max_pkt_length": "128",
                    "min_delay": "11388.79",
                    "min_pkt_length": "128",
                    "misinserted_pkts": "0",
                    "out_of_sequence_pkts": "0",
                    "prbs_bit_errors": "0",
                    "rx_port": "10.220.1.153-1-1 //1/1  10.220.1.153-1-1 //1/1 ",
                    "rx_sig_count": "10",
                    "rx_sig_rate": "0",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                },
                "tx": {
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                }
            },
            "streamblock4": {
                "rx": {
                    "avg_delay": "3991.514",
                    "dropped_pkts": "0",
                    "duplicate_pkts": "0",
                    "first_tstamp": "0.0",
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "last_tstamp": "0.0",
                    "max_delay": "7607.02",
                    "max_pkt_length": "128",
                    "min_delay": "2799.9",
                    "min_pkt_length": "128",
                    "misinserted_pkts": "0",
                    "out_of_sequence_pkts": "0",
                    "prbs_bit_errors": "0",
                    "rx_port": "10.220.1.153-1-2 //1/2  10.220.1.153-1-2 //1/2 ",
                    "rx_sig_count": "10",
                    "rx_sig_rate": "0",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                },
                "tx": {
                    "ipv4_outer_present": "0",
                    "ipv4_present": "0",
                    "ipv6_outer_present": "0",
                    "ipv6_present": "1",
                    "tcp_present": "0",
                    "total_pkt_bit_rate": "0",
                    "total_pkt_bytes": "1280",
                    "total_pkt_rate": "0",
                    "total_pkts": "10",
                    "udp_present": "0"
                }
            }
        }
    }

    IXIA Returns:
    {
        "1/11/1": {
            "aggregate": {
                "duplex_mode": "N/A",
                "port_name": "1/11/1",
                "rx": {
                    "collisions_count": "N/A",
                    "control_frames": "0",
                    "crc_errors": "N/A",
                    "data_int_errors_count": "N/A",
                    "data_int_frames_count": "N/A",
                    "misdirected_packet_count": "N/A",
                    "oversize_count": "N/A",
                    "oversize_crc_errors_count": "N/A",
                    "oversize_crc_errors_rate_count": "N/A",
                    "oversize_rate": "N/A",
                    "oversize_rate_count": "N/A",
                    "pkt_bit_count": "N/A",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000",
                    "raw_pkt_count": "20",
                    "raw_pkt_rate": "0",
                    "rs_fec_corrected_error_count": "N/A",
                    "rs_fec_corrected_error_count_rate": "N/A",
                    "rs_fec_uncorrected_error_count": "N/A",
                    "rs_fec_uncorrected_error_count_rate": "N/A",
                    "rx_aal5_frames_count": "N/A",
                    "rx_aal5_frames_rate": "N/A",
                    "rx_atm_cells_count": "N/A",
                    "rx_atm_cells_rate": "N/A",
                    "total_pkts": "20",
                    "uds1_frame_count": "20",
                    "uds1_frame_rate": "0",
                    "uds2_frame_count": "20",
                    "uds2_frame_rate": "0",
                    "uds3_frame_count": "N/A",
                    "uds3_frame_rate": "N/A",
                    "uds4_frame_count": "N/A",
                    "uds4_frame_rate": "N/A",
                    "uds5_frame_count": "20",
                    "uds5_frame_rate": "0",
                    "uds6_frame_count": "20",
                    "uds6_frame_rate": "0"
                },
                "tx": {
                    "control_frames": "0",
                    "elapsed_time": "2841736040",
                    "line_speed": "N/A",
                    "pkt_bit_count": "N/A",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000",
                    "raw_pkt_count": "20",
                    "scheduled_pkt_count": "20",
                    "scheduled_pkt_rate": "N/A",
                    "total_pkt_rate": "0",
                    "total_pkts": "20",
                    "tx_aal5_bytes_count": "N/A",
                    "tx_aal5_bytes_rate": "N/A",
                    "tx_aal5_frames_count": "N/A",
                    "tx_aal5_frames_rate": "N/A",
                    "tx_aal5_scheduled_cells_count": "N/A",
                    "tx_aal5_scheduled_cells_rate": "N/A",
                    "tx_aal5_scheduled_frames_count": "20",
                    "tx_aal5_scheduled_frames_rate": "N/A",
                    "tx_atm_cells_count": "N/A",
                    "tx_atm_cells_rate": "N/A"
                }
            },
            "data_plane_port": {
                "first_timestamp": "00:00:02.003",
                "last_timestamp": "00:00:04.827",
                "rx": {
                    "avg_latency": "2039728",
                    "l1_bit_rate": "0.000",
                    "l1_load_percent": "0.000",
                    "max_latency": "4189420",
                    "min_latency": "490840",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0.000",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "l1_load_percent": "0.000",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_rate": "0.000",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000"
                }
            },
            "flow": {
                "1": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "0",
                        "last_tstamp": "0",
                        "loss_percent": "0",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_byte_rate": "0",
                        "total_pkt_bytes": "0",
                        "total_pkt_kbit_rate": "0",
                        "total_pkt_mbit_rate": "0",
                        "total_pkt_rate": "0",
                        "total_pkts": "0",
                        "total_pkts_bytes": "0"
                    },
                    "tx": {
                        "flow_name": "1/11/2 TI0-HLTAPI_TRAFFICITEM_540",
                        "pgid_value": "N/A",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "2": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:02.003",
                        "flow_name": "1/11/1 TI0-HLTAPI_TRAFFICITEM_540",
                        "last_tstamp": "00:00:02.003",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pgid_value": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0",
                        "total_pkts": "0"
                    }
                },
                "3": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "0",
                        "last_tstamp": "0",
                        "loss_percent": "0",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_byte_rate": "0",
                        "total_pkt_bytes": "0",
                        "total_pkt_kbit_rate": "0",
                        "total_pkt_mbit_rate": "0",
                        "total_pkt_rate": "0",
                        "total_pkts": "0",
                        "total_pkts_bytes": "0"
                    },
                    "tx": {
                        "flow_name": "1/11/2 TI1-HLTAPI_TRAFFICITEM_540",
                        "pgid_value": "N/A",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "4": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:04.824",
                        "flow_name": "1/11/1 TI1-HLTAPI_TRAFFICITEM_540",
                        "last_tstamp": "00:00:04.827",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pgid_value": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0",
                        "total_pkts": "0"
                    }
                }
            },
            "stream": {
                "TI0-HLTAPI_TRAFFICITEM_540": {
                    "rx": {
                        "avg_delay": "2780722",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:02.003",
                        "last_tstamp": "00:00:02.003",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "4189420",
                        "min_delay": "1358460",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "TI1-HLTAPI_TRAFFICITEM_540": {
                    "rx": {
                        "avg_delay": "1298734",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:04.824",
                        "last_tstamp": "00:00:04.827",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "2217160",
                        "min_delay": "490840",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                }
            }
        },
        "1/11/2": {
            "aggregate": {
                "duplex_mode": "N/A",
                "port_name": "1/11/2",
                "rx": {
                    "collisions_count": "N/A",
                    "control_frames": "0",
                    "crc_errors": "N/A",
                    "data_int_errors_count": "N/A",
                    "data_int_frames_count": "N/A",
                    "misdirected_packet_count": "N/A",
                    "oversize_count": "N/A",
                    "oversize_crc_errors_count": "N/A",
                    "oversize_crc_errors_rate_count": "N/A",
                    "oversize_rate": "N/A",
                    "oversize_rate_count": "N/A",
                    "pkt_bit_count": "N/A",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000",
                    "raw_pkt_count": "20",
                    "raw_pkt_rate": "0",
                    "rs_fec_corrected_error_count": "N/A",
                    "rs_fec_corrected_error_count_rate": "N/A",
                    "rs_fec_uncorrected_error_count": "N/A",
                    "rs_fec_uncorrected_error_count_rate": "N/A",
                    "rx_aal5_frames_count": "N/A",
                    "rx_aal5_frames_rate": "N/A",
                    "rx_atm_cells_count": "N/A",
                    "rx_atm_cells_rate": "N/A",
                    "total_pkts": "20",
                    "uds1_frame_count": "20",
                    "uds1_frame_rate": "0",
                    "uds2_frame_count": "20",
                    "uds2_frame_rate": "0",
                    "uds3_frame_count": "N/A",
                    "uds3_frame_rate": "N/A",
                    "uds4_frame_count": "N/A",
                    "uds4_frame_rate": "N/A",
                    "uds5_frame_count": "20",
                    "uds5_frame_rate": "0",
                    "uds6_frame_count": "20",
                    "uds6_frame_rate": "0"
                },
                "tx": {
                    "control_frames": "0",
                    "elapsed_time": "2826269560",
                    "line_speed": "N/A",
                    "pkt_bit_count": "N/A",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000",
                    "raw_pkt_count": "20",
                    "scheduled_pkt_count": "20",
                    "scheduled_pkt_rate": "N/A",
                    "total_pkt_rate": "0",
                    "total_pkts": "20",
                    "tx_aal5_bytes_count": "N/A",
                    "tx_aal5_bytes_rate": "N/A",
                    "tx_aal5_frames_count": "N/A",
                    "tx_aal5_frames_rate": "N/A",
                    "tx_aal5_scheduled_cells_count": "N/A",
                    "tx_aal5_scheduled_cells_rate": "N/A",
                    "tx_aal5_scheduled_frames_count": "20",
                    "tx_aal5_scheduled_frames_rate": "N/A",
                    "tx_atm_cells_count": "N/A",
                    "tx_atm_cells_rate": "N/A"
                }
            },
            "data_plane_port": {
                "first_timestamp": "00:00:02.006",
                "last_timestamp": "00:00:04.845",
                "rx": {
                    "avg_latency": "1310229",
                    "l1_bit_rate": "0.000",
                    "l1_load_percent": "0.000",
                    "max_latency": "2687700",
                    "min_latency": "-238220",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_count": "2560",
                    "pkt_byte_rate": "0.000",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "l1_load_percent": "0.000",
                    "pkt_bit_rate": "0.000",
                    "pkt_byte_rate": "0.000",
                    "pkt_count": "20",
                    "pkt_kbit_rate": "0.000",
                    "pkt_mbit_rate": "0.000",
                    "pkt_rate": "0.000"
                }
            },
            "flow": {
                "1": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:02.006",
                        "flow_name": "1/11/2 TI0-HLTAPI_TRAFFICITEM_540",
                        "last_tstamp": "00:00:02.008",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pgid_value": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0",
                        "total_pkts": "0"
                    }
                },
                "2": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "0",
                        "last_tstamp": "0",
                        "loss_percent": "0",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_byte_rate": "0",
                        "total_pkt_bytes": "0",
                        "total_pkt_kbit_rate": "0",
                        "total_pkt_mbit_rate": "0",
                        "total_pkt_rate": "0",
                        "total_pkts": "0",
                        "total_pkts_bytes": "0"
                    },
                    "tx": {
                        "flow_name": "1/11/1 TI0-HLTAPI_TRAFFICITEM_540",
                        "pgid_value": "N/A",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "3": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:04.840",
                        "flow_name": "1/11/2 TI1-HLTAPI_TRAFFICITEM_540",
                        "last_tstamp": "00:00:04.845",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pgid_value": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0",
                        "total_pkts": "0"
                    }
                },
                "4": {
                    "rx": {
                        "avg_delay": "N/A",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "0",
                        "last_tstamp": "0",
                        "loss_percent": "0",
                        "loss_pkts": "0",
                        "max_delay": "N/A",
                        "min_delay": "N/A",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0",
                        "total_pkt_byte_rate": "0",
                        "total_pkt_bytes": "0",
                        "total_pkt_kbit_rate": "0",
                        "total_pkt_mbit_rate": "0",
                        "total_pkt_rate": "0",
                        "total_pkts": "0",
                        "total_pkts_bytes": "0"
                    },
                    "tx": {
                        "flow_name": "1/11/1 TI1-HLTAPI_TRAFFICITEM_540",
                        "pgid_value": "N/A",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                }
            },
            "stream": {
                "TI0-HLTAPI_TRAFFICITEM_540": {
                    "rx": {
                        "avg_delay": "1807008",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:02.006",
                        "last_tstamp": "00:00:02.008",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "2687700",
                        "min_delay": "1171900",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                },
                "TI1-HLTAPI_TRAFFICITEM_540": {
                    "rx": {
                        "avg_delay": "813450",
                        "big_error": "N/A",
                        "expected_pkts": "N/A",
                        "first_tstamp": "00:00:04.840",
                        "last_tstamp": "00:00:04.845",
                        "loss_percent": "0.000",
                        "loss_pkts": "0",
                        "max_delay": "1927200",
                        "min_delay": "-238220",
                        "pkt_loss_duration": "N/A",
                        "reverse_error": "N/A",
                        "small_error": "N/A",
                        "total_pkt_bit_rate": "0.000",
                        "total_pkt_byte_rate": "0.000",
                        "total_pkt_bytes": "1280",
                        "total_pkt_kbit_rate": "0.000",
                        "total_pkt_mbit_rate": "0.000",
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10",
                        "total_pkts_bytes": "1280"
                    },
                    "tx": {
                        "total_pkt_rate": "0.000",
                        "total_pkts": "10"
                    }
                }
            }
        },
        "aggregate": {
            "duplex_mode": {
                "count": "N/A"
            },
            "port_name": {
                "count": "2"
            },
            "rx": {
                "collisions_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "control_frames": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "crc_errors": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "data_int_errors_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "data_int_frames_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "misdirected_packet_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "oversize_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "oversize_crc_errors_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "oversize_crc_errors_rate_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "oversize_rate_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "pkt_bit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_byte_count": {
                    "avg": "2560",
                    "count": "2",
                    "max": "2560",
                    "min": "2560",
                    "sum": "5120"
                },
                "pkt_byte_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "pkt_kbit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_mbit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "40.0"
                },
                "raw_pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "raw_pkt_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "rs_fec_corrected_error_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rs_fec_corrected_error_count_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rs_fec_uncorrected_error_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rs_fec_uncorrected_error_count_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rx_aal5_frames_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rx_aal5_frames_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rx_atm_cells_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "rx_atm_cells_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "total_pkts": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "uds1_frame_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20"
                },
                "uds1_frame_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "uds2_frame_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20"
                },
                "uds2_frame_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "uds3_frame_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A"
                },
                "uds3_frame_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "uds4_frame_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A"
                },
                "uds4_frame_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "uds5_frame_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20"
                },
                "uds5_frame_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "uds6_frame_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20"
                },
                "uds6_frame_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                }
            },
            "tx": {
                "control_frames": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "elapsed_time": {
                    "avg": "2834002800",
                    "count": "2",
                    "max": "2841736040",
                    "min": "2826269560",
                    "sum": "5668005600"
                },
                "line_speed": {
                    "count": "N/A"
                },
                "pkt_bit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_byte_count": {
                    "avg": "2560",
                    "count": "2",
                    "max": "2560",
                    "min": "2560",
                    "sum": "5120"
                },
                "pkt_byte_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "pkt_kbit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_mbit_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "pkt_rate": {
                    "avg": "0.0",
                    "count": "2",
                    "max": "0.000",
                    "min": "0.000",
                    "sum": "0.0"
                },
                "raw_pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "scheduled_pkt_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "scheduled_pkt_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "total_pkt_rate": {
                    "avg": "0",
                    "count": "2",
                    "max": "0",
                    "min": "0",
                    "sum": "0"
                },
                "total_pkts": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "tx_aal5_bytes_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_bytes_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_frames_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_frames_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_scheduled_cells_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_scheduled_cells_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_aal5_scheduled_frames_count": {
                    "avg": "20",
                    "count": "2",
                    "max": "20",
                    "min": "20",
                    "sum": "40"
                },
                "tx_aal5_scheduled_frames_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_atm_cells_count": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                },
                "tx_atm_cells_rate": {
                    "avg": "N/A",
                    "count": "N/A",
                    "max": "N/A",
                    "min": "N/A",
                    "sum": "N/A"
                }
            }
        },
        "flow": {
            "1": {
                "flow_name": "1/11/2 TI0-HLTAPI_TRAFFICITEM_540",
                "pgid_value": "N/A",
                "rx": {
                    "avg_delay": "1807008",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:02.006",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:02.008",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "2687700",
                    "min_delay": "1171900",
                    "misdirected_pkts": "N/A",
                    "misdirected_ports": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "port": "1/11/2",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "1280",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10",
                    "total_pkts_bytes": "1280"
                },
                "tracking": {
                    "1": {
                        "tracking_name": "Traffic Item",
                        "tracking_value": "TI0-HLTAPI_TRAFFICITEM_540"
                    },
                    "count": "1"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "port": "1/11/1",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10"
                }
            },
            "2": {
                "flow_name": "1/11/1 TI0-HLTAPI_TRAFFICITEM_540",
                "pgid_value": "N/A",
                "rx": {
                    "avg_delay": "2780722",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:02.003",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:02.003",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "4189420",
                    "min_delay": "1358460",
                    "misdirected_pkts": "N/A",
                    "misdirected_ports": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "port": "1/11/1",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "1280",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10",
                    "total_pkts_bytes": "1280"
                },
                "tracking": {
                    "1": {
                        "tracking_name": "Traffic Item",
                        "tracking_value": "TI0-HLTAPI_TRAFFICITEM_540"
                    },
                    "count": "1"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "port": "1/11/2",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10"
                }
            },
            "3": {
                "flow_name": "1/11/2 TI1-HLTAPI_TRAFFICITEM_540",
                "pgid_value": "N/A",
                "rx": {
                    "avg_delay": "813450",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:04.840",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:04.845",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "1927200",
                    "min_delay": "-238220",
                    "misdirected_pkts": "N/A",
                    "misdirected_ports": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "port": "1/11/2",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "1280",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10",
                    "total_pkts_bytes": "1280"
                },
                "tracking": {
                    "1": {
                        "tracking_name": "Traffic Item",
                        "tracking_value": "TI1-HLTAPI_TRAFFICITEM_540"
                    },
                    "count": "1"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "port": "1/11/1",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10"
                }
            },
            "4": {
                "flow_name": "1/11/1 TI1-HLTAPI_TRAFFICITEM_540",
                "pgid_value": "N/A",
                "rx": {
                    "avg_delay": "1298734",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:04.824",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:04.827",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "2217160",
                    "min_delay": "490840",
                    "misdirected_pkts": "N/A",
                    "misdirected_ports": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "port": "1/11/1",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "1280",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10",
                    "total_pkts_bytes": "1280"
                },
                "tracking": {
                    "1": {
                        "tracking_name": "Traffic Item",
                        "tracking_value": "TI1-HLTAPI_TRAFFICITEM_540"
                    },
                    "count": "1"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "port": "1/11/2",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "10"
                }
            }
        },
        "l23_test_summary": {
            "rx": {
                "avg_latency": "1674978",
                "max_latency": "4189420",
                "min_latency": "-238220",
                "pkt_bit_rate": "0.000",
                "pkt_byte_rate": "0.000",
                "pkt_count": "40",
                "pkt_kbit_rate": "0.000",
                "pkt_mbit_rate": "0.000",
                "pkt_rate": "0.000"
            },
            "tx": {
                "pkt_bit_rate": "0.000",
                "pkt_byte_rate": "0.000",
                "pkt_count": "40",
                "pkt_kbit_rate": "0.000",
                "pkt_mbit_rate": "0.000",
                "pkt_rate": "0.000"
            }
        },
        "measure_mode": "mixed",
        "status": "1",
        "traffic_item": {
            "TI0-HLTAPI_TRAFFICITEM_540": {
                "rx": {
                    "avg_delay": "2293865",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:02.003",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:02.008",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "4189420",
                    "min_delay": "1171900",
                    "misdirected_pkts": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "2560",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "20",
                    "total_pkts_bytes": "2560"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "20"
                }
            },
            "TI1-HLTAPI_TRAFFICITEM_540": {
                "rx": {
                    "avg_delay": "1056092",
                    "big_error": "N/A",
                    "expected_pkts": "N/A",
                    "first_tstamp": "00:00:04.824",
                    "l1_bit_rate": "0.000",
                    "last_tstamp": "00:00:04.845",
                    "loss_percent": "0.000",
                    "loss_pkts": "0",
                    "max_delay": "2217160",
                    "min_delay": "-238220",
                    "misdirected_pkts": "N/A",
                    "misdirected_rate": "N/A",
                    "pkt_loss_duration": "N/A",
                    "reverse_error": "N/A",
                    "small_error": "N/A",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_bytes": "2560",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "20",
                    "total_pkts_bytes": "2560"
                },
                "tx": {
                    "l1_bit_rate": "0.000",
                    "total_pkt_bit_rate": "0.000",
                    "total_pkt_byte_rate": "0.000",
                    "total_pkt_kbit_rate": "0.000",
                    "total_pkt_mbit_rate": "0.000",
                    "total_pkt_rate": "0.000",
                    "total_pkts": "20"
                }
            },
            "aggregate": {
                "rx": {
                    "avg_delay": {
                        "avg": "1674978",
                        "count": "2",
                        "max": "2293865",
                        "min": "1056092",
                        "sum": "3349957"
                    },
                    "big_error": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "expected_pkts": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "first_tstamp": {
                        "count": "2"
                    },
                    "l1_bit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "last_tstamp": {
                        "count": "2"
                    },
                    "loss_percent": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "loss_pkts": {
                        "avg": "0",
                        "count": "2",
                        "max": "0",
                        "min": "0",
                        "sum": "0"
                    },
                    "max_delay": {
                        "avg": "3203290",
                        "count": "2",
                        "max": "4189420",
                        "min": "2217160",
                        "sum": "6406580"
                    },
                    "min_delay": {
                        "avg": "466840",
                        "count": "2",
                        "max": "1171900",
                        "min": "-238220",
                        "sum": "933680"
                    },
                    "misdirected_pkts": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "misdirected_rate": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "pkt_loss_duration": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "reverse_error": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "small_error": {
                        "avg": "N/A",
                        "count": "N/A",
                        "max": "N/A",
                        "min": "N/A",
                        "sum": "N/A"
                    },
                    "total_pkt_bit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_byte_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_bytes": {
                        "avg": "2560",
                        "count": "2",
                        "max": "2560",
                        "min": "2560",
                        "sum": "5120"
                    },
                    "total_pkt_kbit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_mbit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkts": {
                        "avg": "20",
                        "count": "2",
                        "max": "20",
                        "min": "20",
                        "sum": "40"
                    },
                    "total_pkts_bytes": {
                        "avg": "2560",
                        "count": "2",
                        "max": "2560",
                        "min": "2560",
                        "sum": "5120"
                    }
                },
                "tx": {
                    "l1_bit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_bit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_byte_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_kbit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_mbit_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkt_rate": {
                        "avg": "0.0",
                        "count": "2",
                        "max": "0.000",
                        "min": "0.000",
                        "sum": "0.0"
                    },
                    "total_pkts": {
                        "avg": "20",
                        "count": "2",
                        "max": "20",
                        "min": "20",
                        "sum": "40"
                    }
                }
            }
        },
        "waiting_for_stats": "0"
    }
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['mode'] = mode
    args['streams'] = streams
    args['scale_mode'] = scale_mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    if mode == jNone:
        args['mode'] = 'all'
        
    if mode != jNone and mode == 'traffic_item':
        args['mode'] = 'all'    

    ret = rt_handle.invoke('traffic_stats', **args)

    resultoptions = rt_handle.invoke('invoke', cmd='stc::get' + " " + 'project1 -children-resultoptions')
    #if isinstance(resultoptions, str):
        #resultoptions = re.sub(r'\r\n','',resultoptions)

    resultoptions = str(resultoptions)
    resultoptions = resultoptions.strip()
    resultview = rt_handle.invoke('invoke', cmd='stc::get ' + str(resultoptions) + ' -ResultViewMode')


    if port_handle != jNone and resultview != 'HISTOGRAM':
        n_args = dict()
        n_args['query_from'] = port_handle
        n_args['drv_name'] = "drv_1"
        n_args['properties'] = 'StreamBlock.Agg.FrameLossDuration'
        ret2 = rt_handle.invoke('drv_stats', **n_args)

    ret['traffic_item'] = dict()
    for port in list(ret.keys()):
        if 'stream' in ret[port]:
            ret['traffic_item'].update(ret[port]['stream'])

    if port_handle != jNone and resultview != 'HISTOGRAM':
        j = 0
        for streamblock in ret['traffic_item'].keys():
            if streamblock != 'unknown':
                if ret2.get('item'+str(j)) is not None:
                    ret['traffic_item'][streamblock]['rx']['pkt_loss_duration'] = ret2['item'+str(j)]['StreamBlockAggFrameLossDuration']
                    j += 1
                else:
                    ret['traffic_item'][streamblock]['rx']['pkt_loss_duration'] = 'N\A'
    if len(global_tracking) != 0 and port_handle != jNone:
        if 'tracking' not in ret['traffic_item'].keys():
            ret['traffic_item']['tracking'] = dict()
        for tracking_arg in global_tracking:
            if tracking_arg == 'ether_type_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ether_type_tracking", 'properties' : 'StreamBlock.FrameConfig.ethernet:EthernetII.1.etherType'}
                ethernet_value_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ethernet_value_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['Ethernet II:Ethernet-Type'] = ret['traffic_item']['tracking'].get('Ethernet II:Ethernet-Type', [])
                        ret['traffic_item']['tracking']['Ethernet II:Ethernet-Type'].append(ethernet_value_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_precedence_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_precedence_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.tosDiffserv.tos.precedence'}
                ip_precedence_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_precedence_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Precedence'] = ret['traffic_item']['tracking'].get('IPv4:Precedence', [])
                        ret['traffic_item']['tracking']['IPv4:Precedence'].append(ip_precedence_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_ack_num_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_ack_num_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.ackNum'}
                tcp_ack_num_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_ack_num_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:Acknowledgement Number'] = ret['traffic_item']['tracking'].get('TCP:Acknowledgement Number', [])
                        ret['traffic_item']['tracking']['TCP:Acknowledgement Number'].append(tcp_ack_num_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_cwr_flag_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_cwr_flag_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.cwrBit'}
                tcp_cwr_flag_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_cwr_flag_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:CWR'] = ret['traffic_item']['tracking'].get('TCP:CWR', [])
                        ret['traffic_item']['tracking']['TCP:CWR'].append(tcp_cwr_flag_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_dst_port_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_dst_port_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.destPort'}
                tcp_dst_port_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_dst_port_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:TCP-Dest-Port'] = ret['traffic_item']['tracking'].get('TCP:TCP-Dest-Port', [])
                        ret['traffic_item']['tracking']['TCP:TCP-Dest-Port'].append(tcp_dst_port_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_ecn_echo_flag_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_ecn_echo_flag_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.ecnBit'}
                tcp_ecn_echo_flag_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_ecn_echo_flag_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:ECN-Echo'] = ret['traffic_item']['tracking'].get('TCP:ECN-Echo', [])
                        ret['traffic_item']['tracking']['TCP:ECN-Echo'].append(tcp_ecn_echo_flag_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_fin_flag_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_fin_flag_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.finBit'}
                tcp_fin_flag_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_fin_flag_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:FIN'] = ret['traffic_item']['tracking'].get('TCP:FIN', [])
                        ret['traffic_item']['tracking']['TCP:FIN'].append(tcp_fin_flag_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_psh_flag_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_psh_flag_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.pshBit'}
                tcp_psh_flag_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_psh_flag_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:PSH'] = ret['traffic_item']['tracking'].get('TCP:PSH', [])
                        ret['traffic_item']['tracking']['TCP:PSH'].append(tcp_psh_flag_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_reserved_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_reserved_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.reserved'}
                tcp_reserved_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_reserved_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:Reserved'] = ret['traffic_item']['tracking'].get('TCP:Reserved', [])
                        ret['traffic_item']['tracking']['TCP:Reserved'].append(tcp_reserved_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_rst_flag_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_rst_flag_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.rstBit'}
                tcp_rst_flag_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_rst_flag_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:RST'] = ret['traffic_item']['tracking'].get('TCP:RST', [])
                        ret['traffic_item']['tracking']['TCP:RST'].append(tcp_rst_flag_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_seq_num_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_seq_num_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.seqNum'}
                tcp_seq_num_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_seq_num_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:Sequence Number'] = ret['traffic_item']['tracking'].get('TCP:Sequence Number', [])
                        ret['traffic_item']['tracking']['TCP:Sequence Number'].append(tcp_seq_num_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_src_port_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_src_port_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.sourcePort'}
                tcp_src_port_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_src_port_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:TCP-Source-Port'] = ret['traffic_item']['tracking'].get('TCP:TCP-Source-Port', [])
                        ret['traffic_item']['tracking']['TCP:TCP-Source-Port'].append(tcp_src_port_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_syn_flag_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_syn_flag_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.synBit'}
                tcp_syn_flag_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_syn_flag_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:SYN'] = ret['traffic_item']['tracking'].get('TCP:SYN', [])
                        ret['traffic_item']['tracking']['TCP:SYN'].append(tcp_syn_flag_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_urg_flag_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_urg_flag_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.urgBit'}
                tcp_urg_flag_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_urg_flag_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:URG'] = ret['traffic_item']['tracking'].get('TCP:URG', [])
                        ret['traffic_item']['tracking']['TCP:URG'].append(tcp_urg_flag_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_urgent_ptr_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_urgent_ptr_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.urgentPtr'}
                tcp_urgent_ptr_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_urgent_ptr_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:Urgent Pointer'] = ret['traffic_item']['tracking'].get('TCP:Urgent Pointer', [])
                        ret['traffic_item']['tracking']['TCP:Urgent Pointer'].append(tcp_urgent_ptr_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'vlan_id_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "vlan_id_tracking", 'properties' : 'StreamBlock.FrameConfig.ethernet:EthernetII.vlans.Vlan.1.id'}
                vlan_id_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in vlan_id_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['VLAN:VLAN-ID'] = ret['traffic_item']['tracking'].get('VLAN:VLAN-ID', [])
                        ret['traffic_item']['tracking']['VLAN:VLAN-ID'].append(vlan_id_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'vlan_cfi_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "vlan_cfi_tracking", 'properties' : 'StreamBlock.FrameConfig.ethernet:EthernetII.vlans.Vlan.1.cfi'}
                vlan_cfi_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in vlan_cfi_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['VLAN:Canonical Format Indicator'] = ret['traffic_item']['tracking'].get('VLAN:Canonical Format Indicator', [])
                        ret['traffic_item']['tracking']['VLAN:Canonical Format Indicator'].append(vlan_cfi_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'vlan_protocol_tag_id_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "vlan_protocol_tag_id_tracking", 'properties' : 'StreamBlock.FrameConfig.ethernet:EthernetII.vlans.Vlan.1.type'}
                vlan_protocol_tag_id_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in vlan_protocol_tag_id_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['VLAN:Protocol-ID'] = ret['traffic_item']['tracking'].get('VLAN:Protocol-ID', [])
                        ret['traffic_item']['tracking']['VLAN:Protocol-ID'].append(vlan_protocol_tag_id_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_window_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_window_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.window'}
                tcp_window_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_window_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:Window'] = ret['traffic_item']['tracking'].get('TCP:Window', [])
                        ret['traffic_item']['tracking']['TCP:Window'].append(tcp_window_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'udp_dst_port_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "udp_dst_port_tracking", 'properties' : 'StreamBlock.FrameConfig.udp:Udp.destPort'}
                udp_dst_port_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in udp_dst_port_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['UDP:UDP-Dest-Port'] = ret['traffic_item']['tracking'].get('UDP:UDP-Dest-Port', [])
                        ret['traffic_item']['tracking']['UDP:UDP-Dest-Port'].append(udp_dst_port_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'udp_src_port_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "udp_src_port_tracking", 'properties' : 'StreamBlock.FrameConfig.udp:Udp.sourcePort'}
                udp_src_port_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in udp_src_port_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['UDP:UDP-Source-Port'] = ret['traffic_item']['tracking'].get('UDP:UDP-Source-Port', [])
                        ret['traffic_item']['tracking']['UDP:UDP-Source-Port'].append(udp_src_port_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'vlan_user_priority_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "vlan_user_priority_tracking", 'properties' : 'StreamBlock.FrameConfig.ethernet:EthernetII.vlans.Vlan.1.pri'}
                vlan_user_priority_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in vlan_user_priority_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['VLAN:VLAN Priority'] = ret['traffic_item']['tracking'].get('VLAN:VLAN Priority', [])
                        ret['traffic_item']['tracking']['VLAN:VLAN Priority'].append(vlan_user_priority_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_cost_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_cost_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.tosDiffserv.tos.mBit'}
                ip_cost_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_cost_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Monetary'] = ret['traffic_item']['tracking'].get('IPv4:Monetary', [])
                        ret['traffic_item']['tracking']['IPv4:Monetary'].append(ip_cost_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_delay_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_delay_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.tosDiffserv.tos.dBit'}
                ip_delay_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_delay_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Delay'] = ret['traffic_item']['tracking'].get('IPv4:Delay', [])
                        ret['traffic_item']['tracking']['IPv4:Delay'].append(ip_delay_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_dst_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_dst_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.destAddr'}
                ip_dst_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_dst_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Destination Address'] = ret['traffic_item']['tracking'].get('IPv4:Destination Address', [])
                        ret['traffic_item']['tracking']['IPv4:Destination Address'].append(ip_dst_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_fragment_last_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_fragment_last_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.flags.mfBit'}
                ip_fragment_last_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_fragment_last_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Last Fragment'] = ret['traffic_item']['tracking'].get('IPv4:Last Fragment', [])
                        ret['traffic_item']['tracking']['IPv4:Last Fragment'].append(ip_fragment_last_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_fragment_offset_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_fragment_offset_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.fragOffset'}
                ip_fragment_offset_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_fragment_offset_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Fragment offset'] = ret['traffic_item']['tracking'].get('IPv4:Fragment offset', [])
                        ret['traffic_item']['tracking']['IPv4:Fragment offset'].append(ip_fragment_offset_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_id_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_id_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.identification'}
                ip_id_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_id_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Identification'] = ret['traffic_item']['tracking'].get('IPv4:Identification', [])
                        ret['traffic_item']['tracking']['IPv4:Identification'].append(ip_id_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'tcp_ack_flag_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "tcp_ack_flag_tracking", 'properties' : 'StreamBlock.FrameConfig.tcp:Tcp.ackBit'}
                tcp_ack_flag_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in tcp_ack_flag_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['TCP:ACK'] = ret['traffic_item']['tracking'].get('TCP:ACK', [])
                        ret['traffic_item']['tracking']['TCP:ACK'].append(tcp_ack_flag_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_protocol_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_protocol_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.protocol'}
                ip_protocol_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_protocol_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Protocol'] = ret['traffic_item']['tracking'].get('IPv4:Protocol', [])
                        ret['traffic_item']['tracking']['IPv4:Protocol'].append(ip_protocol_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_reliability_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_reliability_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.tosDiffserv.tos.rBit'}
                ip_reliability_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_reliability_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Reliability'] = ret['traffic_item']['tracking'].get('IPv4:Reliability', [])
                        ret['traffic_item']['tracking']['IPv4:Reliability'].append(ip_reliability_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_src_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_src_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.sourceAddr'}
                ip_src_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_src_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Source Address'] = ret['traffic_item']['tracking'].get('IPv4:Source Address', [])
                        ret['traffic_item']['tracking']['IPv4:Source Address'].append(ip_src_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_throughput_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_throughput_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.tosDiffserv.tos.tBit'}
                ip_throughput_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_throughput_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Throughput'] = ret['traffic_item']['tracking'].get('IPv4:Throughput', [])
                        ret['traffic_item']['tracking']['IPv4:Throughput'].append(ip_throughput_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_reserved_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_reserved_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.tosDiffserv.tos.reserved'}
                ip_reserved_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_reserved_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Reserved'] = ret['traffic_item']['tracking'].get('IPv4:Reserved', [])
                        ret['traffic_item']['tracking']['IPv4:Reserved'].append(ip_reserved_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_ttl_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_throughput_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.ttl'}
                ip_ttl_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_ttl_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:TTL'] = ret['traffic_item']['tracking'].get('IPv4:TTL', [])
                        ret['traffic_item']['tracking']['IPv4:TTL'].append(ip_ttl_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ipv6_dst_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ipv6_dst_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv6:IPv6.1.destAddr'}
                ipv6_dst_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ipv6_dst_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv6:Destination Address'] = ret['traffic_item']['tracking'].get('IPv6:Destination Address', [])
                        ret['traffic_item']['tracking']['IPv6:Destination Address'].append(ipv6_dst_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ipv6_flow_label_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ipv6_flow_label_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv6:IPv6.1.flowLabel'}
                ipv6_flow_label_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ipv6_flow_label_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv6:Flow Label'] = ret['traffic_item']['tracking'].get('IPv6:Flow Label', [])
                        ret['traffic_item']['tracking']['IPv6:Flow Label'].append(ipv6_flow_label_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ipv6_hop_limit_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ipv6_hop_limit_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv6:IPv6.1.hopLimit'
}
                ipv6_hop_limit_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ipv6_hop_limit_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv6:Hop Limit'] = ret['traffic_item']['tracking'].get('IPv6:Hop Limit', [])
                        ret['traffic_item']['tracking']['IPv6:Hop Limit'].append(ipv6_hop_limit_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ipv6_src_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ipv6_src_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv6:IPv6.1.sourceAddr'}
                ipv6_src_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ipv6_src_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv4:Source Address'] = ret['traffic_item']['tracking'].get('IPv4:Source Address', [])
                        ret['traffic_item']['tracking']['IPv4:Source Address'].append(ipv6_src_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ipv6_traffic_class_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ipv6_traffic_class_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv6:IPv6.1.trafficClass'}
                ipv6_traffic_class_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ipv6_traffic_class_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IPv6:Traffic Class'] = ret['traffic_item']['tracking'].get('IPv6:Traffic Class', [])
                        ret['traffic_item']['tracking']['IPv6:Traffic Class'].append(ipv6_traffic_class_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'mac_dst_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "mac_dst_tracking", 'properties' : 'StreamBlock.FrameConfig.ethernet:EthernetII.1.dstMac'}
                mac_dst_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in mac_dst_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['EthernetII:Destination MAC Address'] = ret['traffic_item']['tracking'].get('EthernetII:Destination MAC Address', [])
                        ret['traffic_item']['tracking']['EthernetII:Destination MAC Address'].append(mac_dst_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'mac_src_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "mac_src_tracking", 'properties' : 'StreamBlock.FrameConfig.ethernet:EthernetII.1.srcMac'}
                mac_src_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in mac_src_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['EthernetII:Source MAC Address'] = ret['traffic_item']['tracking'].get('EthernetII:Source MAC Address', [])
                        ret['traffic_item']['tracking']['EthernetII:Source MAC Address'].append(mac_src_tracking['item'+str(index)][property])
                        index += 1
            elif tracking_arg == 'ip_dscp_tracking':
                new_args = {'query_from' : port_handle, 'drv_name' : "ip_dscp_tracking", 'properties' : 'StreamBlock.FrameConfig.ipv4:IPv4.1.tosDiffserv.diffServ'}
                ip_dscp_tracking = rt_handle.invoke('drv_stats', **new_args)
                property = new_args['properties'].replace('.', '')
                index = 0
                for key in ip_dscp_tracking.keys():
                    if 'item' in key:
                        ret['traffic_item']['tracking']['IP DSCP'] = ret['traffic_item']['tracking'].get('IP DSCP', [])
                        ret['traffic_item']['tracking']['IP DSCP'].append(ip_dscp_tracking['item'+str(index)][property])
                        index += 1


    # ***** Return Value Modification *****

    if mode == 'traffic_item':
        for item_1 in ret:
            if item_1.startswith('streamblock'):
                ret[item_1]['rx']['loss_percent'] = ret[item_1]['rx']['dropped_pkts_percent']
                ret[item_1]['rx']['loss_pkts'] = ret[item_1]['rx']['dropped_pkts']
            if item_1.startswith('traffic_item'):
                for item_2 in ret[item_1]:
                    if item_2.startswith('streamblock'):
                         ret[item_1][item_2]['rx']['loss_percent'] = ret[item_1][item_2]['rx']['dropped_pkts_percent']
                         ret[item_1][item_2]['rx']['loss_pkts'] = ret[item_1][item_2]['rx']['dropped_pkts']


    # ***** End of Return Value Modification *****

    return ret


def j_emulation_ospf_info(
        rt_handle,
        port_handle=jNone,
        handle=jNone):
    """
    :param rt_handle:       RT object
    :param port_handle
    :param handle

    Spirent Returns:
    {
        "adjacency_status": "FULL",
        "router_state": "POINT_TO_POINT",
        "rx_ack": "2",
        "rx_asexternal_lsa": "0",
        "rx_dd": "2",
        "rx_external_link_lsa": "0",
        "rx_external_prefix_lsa": "0",
        "rx_hello": "1",
        "rx_network_lsa": "0",
        "rx_nssa_lsa": "0",
        "rx_request": "1",
        "rx_router_asbr": "0",
        "rx_router_info_lsa": "0",
        "rx_router_lsa": "2",
        "rx_summary_lsa": "1",
        "rx_te_lsa": "0",
        "status": "1",
        "tx_ack": "2",
        "tx_as_external_lsa": "0",
        "tx_asbr_summry_lsa": "0",
        "tx_dd": "4",
        "tx_external_link_lsa": "0",
        "tx_external_prefix_lsa": "0",
        "tx_hello": "1",
        "tx_network_lsa": "0",
        "tx_nssa_lsa": "0",
        "tx_request": "1",
        "tx_router_info_lsa": "0",
        "tx_router_lsa": "2",
        "tx_summary_lsa": "1",
        "tx_te_lsa": "0"
    }

    IXIA Returns:
    {
        "/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1/item:1": {
            "session": {
                "database_description_rx": "2",
                "database_description_tx": "3",
                "hellos_rx": "3",
                "hellos_tx": "3",
                "information": "none",
                "linkstate_ack_rx": "1",
                "linkstate_ack_tx": "1",
                "linkstate_advertisement_rx": "2",
                "linkstate_advertisement_tx": "2",
                "linkstate_request_rx": "1",
                "linkstate_request_tx": "1",
                "linkstate_update_rx": "1",
                "linkstate_update_tx": "1",
                "lsa_acknowledge_rx": "2",
                "lsa_acknowledged": "2",
                "ospfIfaceState": "pointToPoint",
                "ospfNeighborState": "full",
                "status": "up"
            }
        },
        "Device Group 1": {
            "aggregate": {
                "database_description_rx": "2",
                "database_description_tx": "3",
                "external_lsa_rx": "0",
                "external_lsa_tx": "0",
                "grace_lsa_rx": "0",
                "hellos_rx": "3",
                "hellos_tx": "3",
                "helpermode_attempted": "0",
                "helpermode_failed": "0",
                "linkstate_ack_rx": "1",
                "linkstate_ack_tx": "1",
                "linkstate_advertisement_rx": "2",
                "linkstate_advertisement_tx": "2",
                "linkstate_request_rx": "1",
                "linkstate_request_tx": "1",
                "linkstate_update_rx": "1",
                "linkstate_update_tx": "1",
                "lsa_acknowledge_rx": "2",
                "lsa_acknowledged": "2",
                "neighbor_2way_count": "0",
                "neighbor_attempt_count": "0",
                "neighbor_down_count": "0",
                "neighbor_exchange_count": "0",
                "neighbor_exstart_count": "0",
                "neighbor_full_count": "1",
                "neighbor_init_count": "0",
                "neighbor_loading_count": "0",
                "network_lsa_rx": "0",
                "network_lsa_tx": "0",
                "nssa_lsa_rx": "0",
                "nssa_lsa_tx": "0",
                "opaque_area_lsa_rx": "0",
                "opaque_area_lsa_tx": "0",
                "opaque_domain_lsa_rx": "0",
                "opaque_domain_lsa_tx": "0",
                "opaque_local_lsa_rx": "0",
                "opaque_local_lsa_tx": "0",
                "router_lsa_rx": "1",
                "router_lsa_tx": "1",
                "sessions_configured": "1",
                "status": "started",
                "summary_iplsa_rx": "1",
                "summary_iplsa_tx": "1"
            }
        },
        "rx_ack": "1",
        "rx_hello": "3",
        "rx_network_lsa": "0",
        "rx_nssa_lsa": "0",
        "rx_request": "1",
        "rx_router_lsa": "1",
        "rx_summary_lsa": "1",
        "status": "1",
        "tx_ack": "3",
        "tx_hello": "3",
        "tx_network_lsa": "0",
        "tx_nssa_lsa": "0",
        "tx_request": "1",
        "tx_router_lsa": "1",
        "tx_summary_lsa": "1"
    }

    Common Return Keys:
        "status"
        "rx_ack"
        "rx_hello"
        "rx_network_lsa"
        "rx_nssa_lsa"
        "rx_request"
        "rx_router_lsa"
        "rx_summary_lsa"
        "tx_ack"
        "tx_hello"
        "tx_network_lsa"
        "tx_nssa_lsa"
        "tx_request"
        "tx_router_lsa"
        "tx_summary_lsa"
        "adjacency_status"
        "router_state"
        "rx_asexternal_lsa"
        "rx_dd"
        "tx_as_external_lsa"
        "tx_dd"

    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            args['handle'] = hnd

            newer_ret = dict()
            args['mode'] = 'stats'
            if (session_map[hndl] == 'ospfv3'):
                newer_ret.update(rt_handle.invoke('emulation_ospfv3_info', **args))
            elif (session_map[hndl] == 'ospfv2'):
                newer_ret.update(rt_handle.invoke('emulation_ospfv2_info', **args))

            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if new_ret:
            ret.append(new_ret)

    # **** Add code to consolidate stats here ****

    for index in range(len(ret)):
        for key in ret[index]:
            if isinstance(ret[index][key], list):
                if 'rx_router_lsa' in key or 'rx_external_link_lsa' in key or 'tx_te_lsa' in key or 'tx_external_link_lsa' in key or 'tx_external_prefix_lsa' in key or 'tx_ack' in key or 'tx_nssa_lsa' in key or 'tx_summary_lsa' in key or 'tx_summary_lsa' in key or 'rx_request' in key or 'rx_network_lsa' in key or 'rx_external_prefix_lsa' in key or 'tx_network_lsa' in key or 'tx_router_lsa' in key or 'rx_router_info_lsa' in key or 'rx_router_asbr' in key or 'tx_hello' in key or 'tx_router_info_lsa' in key or 'rx_dd' in key or 'tx_dd' in key or 'tx_request' in key or 'rx_asexternal_lsa' in key or 'rx_nssa_lsa' in key or 'tx_as_external_lsa' in key or 'rx_summary_lsa' in key or 'rx_ack' in key or 'tx_asbr_summry_lsa' in key or 'rx_hello' in key:
                    ret[index][key] = sum(list(map(int, ret[index][key])))

    # **** Add code to consolidate stats here ****

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_emulation_isis_topology_route_config(
        rt_handle,
        mode=jNone,
        handle=jNone,
        type=jNone,
        external_ip_start=jNone,
        external_ip_pfx_len=jNone,
        router_routing_level=jNone,
        external_up_down_bit=jNone,
        external_metric=jNone,
        router_system_id=jNone,
        external_count=jNone,
        external_ip_step=jNone,
        external_ipv6_pfx_len=jNone,
        external_ipv6_start=jNone,
        external_ipv6_step=jNone):
    """
    :param rt_handle:       RT object
    :param mode - <create|modify|delete>
    :param handle
    :param type
    :param external_ip_start
    :param external_ip_pfx_len - <1-32>
    :param router_routing_level
    :param external_up_down_bit - <0|1>
    :param external_metric - <1-63>
    :param router_system_id
    :param external_count - <1-35000>
    :param external_ip_step
    :param external_ipv6_pfx_len - <1-128>
    :param external_ipv6_start
    :param external_ipv6_step

    Spirent Returns:
    {
        "elem_handle": "isisRouteHandle0",
        "external": "num_networks 1",
        "handles": "isisRouteHandle0",
        "status": "1",
        "version": "4"
    }

    IXIA Returns:
    {
        "handles": "/topology:1/deviceGroup:1/networkGroup:1",
        "ipv4_prefix_interface_handle": "/topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/isisL3RouteProperty:1",
        "network_group_handle": "/topology:1/deviceGroup:1/networkGroup:1",
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    global global_config

    args = dict()
    args['mode'] = mode
    args['handle'] = handle
    args['external_ip_start'] = external_ip_start
    args['external_ip_pfx_len'] = external_ip_pfx_len
    args['router_routing_level'] = router_routing_level
    args['external_up_down_bit'] = external_up_down_bit
    args['external_metric'] = external_metric
    args['router_system_id'] = router_system_id
    args['external_count'] = external_count
    args['external_ip_step'] = external_ip_step
    args['external_ipv6_pfx_len'] = external_ipv6_pfx_len
    args['external_ipv6_start'] = external_ipv6_start
    args['external_ipv6_step'] = external_ipv6_step
    args['type'] = type

    if (type == 'ipv4'):
        args['ip_version'] = 4
    elif (type == 'ipv6'):
        args['ip_version'] = 6
    if (external_ip_start != jNone or external_ipv6_start != jNone):
        args['type'] = 'external'
    #elif (stub_ip_start != jNone or stub_ipv6_start != jNone):
     #   args['type'] = 'stub'

    args = get_arg_value(rt_handle, j_emulation_isis_topology_route_config.__doc__, **args)

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    counter = 1
    string = "isis_route_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "isis_route_" + str(counter)
    global_config[string] = []

    ret = []
    handle_list = dict()

    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            if hnd in handle_list:
                continue
            else:
                handle_list[hnd] = 1
            args['handle'] = hnd
            if mode == 'modify' or mode == 'delete':
                args['elem_handle'] = hnd
            newer_ret = rt_handle.invoke('emulation_isis_topology_route_config', **args)
            if router_system_id != jNone:
                router_system_id = hex(int(router_system_id, 16) + 1)[2:]
                args['router_system_id'] = router_system_id
            if 'status' in newer_ret:
                if newer_ret['status'] == 0:
                    status = 0
            if 'elem_handle' in newer_ret:
                global_config[string].extend([newer_ret['elem_handle']])
            for key in newer_ret:
                try:
                    new_ret[key]
                except:
                    new_ret[key] = []
                new_ret[key].append(newer_ret[key])
        for key in new_ret:
            if len(new_ret[key]) == 1:
                new_ret[key] = new_ret[key][0]
        if 'status' in new_ret:
            new_ret['status'] = status
        if 'elem_handle' in new_ret:
            new_ret['handles'] = string
        if new_ret:
            ret.append(new_ret)

    # ***** Return Value Modification *****


    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ptp_config(
        rt_handle,
        mode=jNone,
        port_handle=jNone,
        handle=jNone,
        log_announce_interval=jNone,
        announce_receipt_timeout=jNone,
        log_sync_interval=jNone,
        log_delay_req_interval=jNone,
        role=jNone,
        communication_mode=jNone,
        transport_type=jNone,
        master_mac_address=jNone,
        master_mac_increment_by=jNone,
        slave_mac_address=jNone,
        slave_mac_increment_by=jNone,
        master_ip_address=jNone,
        master_ip_increment_by=jNone,
        slave_ip_address=jNone,
        slave_ip_increment_by=jNone,
        master_ipv6_address=jNone,
        master_ipv6_increment_by=jNone,
        slave_ipv6_address=jNone,
        slave_ipv6_increment_by=jNone,
        first_clock=jNone,
        clock_class=jNone,
        vlan_id=jNone,
        port_number=jNone,
        domain=jNone,
        announce_frequency_traceable=jNone,
        step_mode=jNone,
        announce_time_traceable=jNone,
        announce_leap59=jNone,
        announce_leap61=jNone,
        clock_accuracy=jNone,
        priority1=jNone,
        priority2=jNone,
        signal_unicast_handling=jNone,
        use_clock_identity=jNone,
        current_utc_offset=jNone,
        intf_ip_addr=jNone,
        intf_ip_addr_step=jNone,
        intf_prefix_length=jNone,
        intf_ipv6_addr=jNone,
        intf_ipv6_addr_step=jNone,
        intf_prefixv6_length=jNone,
        neighbor_intf_ip_addr=jNone,
        neighbor_intf_ip_addr_step=jNone,
        neighbor_intf_ipv6_addr=jNone,
        neighbor_intf_ipv6_addr_step=jNone,
        vlan_id1=jNone,
        vlan_id2=jNone,
        vlan_id_mode1=jNone,
        vlan_id_mode2=jNone,
        vlan_id_step1=jNone,
        vlan_id_step2=jNone,
        vlan_priority1=jNone,
        vlan_priority2=jNone,
        multicastAddress=jNone,
        offset_scaled_log_variance=jNone):

    """
    :param rt_handle:       RT object
    :param mode - <create|delete|modify>
    :param port_handle
    :param handle
    :param log_announce_interval
    :param announce_receipt_timeout
    :param log_sync_interval
    :param log_delay_req_interval
    :param role
    :param communication_mode
    :param transport_type
    :param master_mac_address
    :param master_mac_increment_by
    :param slave_mac_address
    :param slave_mac_increment_by
    :param master_ip_address
    :param master_ip_increment_by
    :param slave_ip_address
    :param slave_ip_increment_by
    :param master_ipv6_address
    :param master_ipv6_increment_by
    :param slave_ipv6_address
    :param slave_ipv6_increment_by
    :param first_clock
    :param clock_class
    :param vlan_id
    :param port_number
    :param domain
    :param announce_frequency_traceable
    :param step_mode
    :param announce_time_traceable
    :param announce_leap59
    :param announce_leap61
    :param clock_accuracy
    :param priority1
    :param priority2
    :param signal_unicast_handling
    :param use_clock_identity
    :param current_utc_offset
    :param intf_ip_addr
    :param intf_ip_addr_step
    :param intf_prefix_length
    :param intf_ipv6_addr
    :param intf_ipv6_addr_step
    :param intf_prefixv6_length
    :param neighbor_intf_ip_addr
    :param neighbor_intf_ip_addr_step
    :param neighbor_intf_ipv6_addr
    :param neighbor_intf_ipv6_addr_step
    :param vlan_id1
    :param vlan_id2
    :param vlan_id_mode1
    :param vlan_id_mode2
    :param vlan_id_step1
    :param vlan_id_step2
    :param vlan_priority1
    :param vlan_priority2
    :param multicastAddress
    :param offset_scaled_log_variance

    Spirent Returns:
    {
        "port_handle": port1
        "handle": router1
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
        "handles"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args['port_handle'] = port_handle
    args['handle'] = handle
    args['log_announce_message_interval'] = log_announce_interval
    args['announce_receipt_timeout'] = announce_receipt_timeout
    args['log_sync_message_interval'] = log_sync_interval
    args['log_minimum_delay_request_interval'] = log_delay_req_interval
    args['transport_type'] = transport_type
    args['first_clock'] = first_clock
    args['master_clock_class'] = clock_class
    if communication_mode == 'unicast' or communication_mode == 'multicast':
        args['ptp_session_mode'] = communication_mode
    args['ptp_port_number'] = port_number
    args['ptp_domain_number'] = domain
    args['current_utc_offset'] = current_utc_offset
    args['local_ip_addr'] = intf_ip_addr
    args['local_ip_addr_step'] = intf_ip_addr_step
    args['local_ip_prefix_len'] = intf_prefix_length
    args['local_ipv6_addr'] = intf_ipv6_addr
    args['local_ipv6_addr_step'] = intf_ipv6_addr_step
    args['local_ipv6_prefix_len'] = intf_prefixv6_length
    args['remote_ip_addr'] = neighbor_intf_ip_addr
    args['remote_ip_addr_step'] = neighbor_intf_ip_addr_step
    args['remote_ipv6_addr'] = neighbor_intf_ipv6_addr
    args['remote_ipv6_addr_step'] = neighbor_intf_ipv6_addr_step
    args['vlan_id1'] = vlan_id1
    args['vlan_id2'] = vlan_id2
    args['vlan_id_mode1'] = vlan_id_mode1
    args['vlan_id_mode2'] = vlan_id_mode2
    args['vlan_id_step1'] = vlan_id_step1
    args['vlan_id_step2'] = vlan_id_step2
    args['vlan_priority1'] = vlan_priority1
    args['vlan_priority2'] = vlan_priority2

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ptp_config.__doc__, **args) 

    if "port_handle" not in args.keys():
        __check_and_raise(handle)
    else:
        __check_and_raise(port_handle)
#        try:
#            handle_map[port_handle]
#        except KeyError:
#            handle_map[port_handle] = []

#    if not isinstance(handle, list):
#        handle = [handle]
#    handle = list(set(handle))

    if role == 'slave':
        role = 'ptpSlave'
    else:
        role = 'ptpMaster'
    args['device_type'] = role
    
    if 'first_clock' in args.keys():
        if use_clock_identity != jNone and use_clock_identity == '1':
            args['ptp_clock_id'] = first_clock
            del args['first_clock']
        else:
            del args['first_clock']

    if 'device_type' in args:
        if role == 'ptpMaster' and 'slave_mac_address' not in args:
            if intf_ip_addr != jNone:
                args['local_mac_addr'] = master_mac_address
                args['local_mac_addr_step'] = master_mac_increment_by
                args['local_ip_addr'] = intf_ip_addr
                args['local_ip_addr_step'] = intf_ip_addr_step
                args['remote_ip_addr'] = neighbor_intf_ip_addr
                args['remote_ip_addr_step'] = neighbor_intf_ip_addr_step
                args['local_ip_addr'] = master_ip_address
                args['local_ip_addr_step'] = master_ip_increment_by
                args['remote_ip_addr'] = slave_ip_address
                args['remote_ip_addr_step'] = slave_ip_increment_by
            if intf_ipv6_addr != jNone:
                args['local_ipv6_addr'] = intf_ipv6_addr
                args['local_ipv6_addr_step'] = intf_ipv6_addr_step
                args['remote_ipv6_addr'] = neighbor_intf_ipv6_addr
                args['remote_ipv6_addr_step'] = neighbor_intf_ipv6_addr_step
                args['local_mac_addr'] = master_mac_address
                args['local_mac_addr_step'] = master_mac_increment_by
                args['local_ipv6_addr'] = master_ipv6_address
                args['local_ipv6_addr_step'] = master_ipv6_increment_by
                args['remote_ipv6_addr'] = slave_ipv6_address
                args['remote_ipv6_addr_step'] = slave_ipv6_increment_by
            for key in list(args.keys()):
                if args[key] == jNone:
                    del args[key]
        elif role == 'ptpMaster' and 'slave_mac_address' in args:
            del args['slave_mac_address']
            if intf_ip_addr != jNone:
                args['local_mac_addr'] = master_mac_address
                args['local_mac_addr_step'] = master_mac_increment_by
                args['local_ip_addr'] = intf_ip_addr
                args['local_ip_addr_step'] = intf_ip_addr_step
                args['remote_ip_addr'] = neighbor_intf_ip_addr
                args['remote_ip_addr_step'] = neighbor_intf_ip_addr_step
                args['local_ip_addr'] = master_ip_address
                args['local_ip_addr_step'] = master_ip_increment_by
                args['remote_ip_addr'] = slave_ip_address
                args['remote_ip_addr_step'] = slave_ip_increment_by
            if intf_ipv6_addr != jNone:
                args['local_mac_addr'] = master_mac_address
                args['local_mac_addr_step'] = master_mac_increment_by
                args['local_ipv6_addr'] = intf_ipv6_addr
                args['local_ipv6_addr_step'] = intf_ipv6_addr_step
                args['remote_ipv6_addr'] = neighbor_intf_ipv6_addr
                args['remote_ipv6_addr_step'] = neighbor_intf_ipv6_addr_step
                args['local_ipv6_addr'] = master_ipv6_address
                args['local_ipv6_addr_step'] = master_ipv6_increment_by
                args['remote_ipv6_addr'] = slave_ipv6_address
                args['remote_ipv6_addr_step'] = slave_ipv6_increment_by
            for key in list(args.keys()):
                if args[key] == jNone:
                    del args[key]
        elif role == 'ptpSlave' and 'master_mac_address' in args:
            del args['master_mac_address']
            if intf_ip_addr != jNone:
                args['local_mac_addr'] = slave_mac_address
                args['local_mac_addr_step'] = slave_mac_increment_by
                args['local_ip_addr'] = intf_ip_addr
                args['local_ip_addr_step'] = intf_ip_addr_step
                args['remote_ip_addr'] = neighbor_intf_ip_addr
                args['remote_ip_addr_step'] = neighbor_intf_ip_addr_step
                args['local_ip_addr'] = slave_ip_address
                args['local_ip_addr_step'] = slave_ip_increment_by
                args['remote_ip_addr'] = master_ip_address
                args['remote_ip_addr_step'] = master_ip_increment_by
            if intf_ipv6_addr != jNone:
                args['local_mac_addr'] = slave_mac_address
                args['local_mac_addr_step'] = slave_mac_increment_by
                args['local_ipv6_addr'] = intf_ipv6_addr
                args['local_ipv6_addr_step'] = intf_ipv6_addr_step
                args['remote_ipv6_addr'] = neighbor_intf_ipv6_addr
                args['remote_ipv6_addr_step'] = neighbor_intf_ipv6_addr_step
                args['local_ipv6_addr'] = slave_ipv6_address
                args['local_ipv6_addr_step'] = slave_ipv6_increment_by
                args['remote_ipv6_addr'] = master_ipv6_address
                args['remote_ipv6_addr_step'] = master_ipv6_increment_by
            for key in list(args.keys()):
                if args[key] == jNone:
                    del args[key]
    ret = []

    counter = 1
    string = "ptp_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "ptp_" + str(counter)
    global_config[string] = []
    if handle != jNone:
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    args['handle'] = hnd
                    if 'mode' in args and args['mode'] == 'create':
                        args['mode'] = 'enable'
                    result = rt_handle.invoke('emulation_ptp_config', **args)
                    if result.get('handle'):
                        global_config[string].extend(result['handle'].split(' '))
                       # result['handle'] = result['handle']
                        result['handles'] = string
                    ret.append(result)
            else:
                args['handle'] = hndl
                args['mode'] = 'enable' if args['mode'] == 'create' else args['mode']
                result = rt_handle.invoke('emulation_ptp_config', **args)
                if result.get('handle'):
                    global_config[string].extend(result['handle'].split(' '))
                   # result['handle'] = result['handles']
                    result['handles'] = string
                ret.append(result)
    elif port_handle != jNone:
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        for port_hand in port_handle:
            args['port_handle'] = port_hand
            result = rt_handle.invoke('emulation_ptp_config', **args)
            if result.get('handle'):
                global_config[string].extend(result['handle'].split(' '))
               # result['handle'] = result['handles']
                result['handles'] = string
                handle_map[port_hand] = handle_map.get(port_hand, [])
                handle_map[port_hand].extend(global_config[string])
                handle_map[port_hand] = list(set(handle_map[port_hand]))
                handle_map[string] = port_hand
            ret.append(result)
    # ***** Return Value Modification *****

###PTP native###
    for index in range(len(ret)):
        if 'handle' in ret[index]:
            myHandle = ret[index]['handle']
            ptp_hndle = rt_handle.invoke('invoke', cmd='stc::get '+myHandle+' -children-Ieee1588v2ClockConfig')

##announce_frequency_traceable
            if announce_frequency_traceable == 1:
#        ptp_hndle = rt_handle.invoke('invoke', cmd='stc::get '+handle+' -children-Ieee1588v2ClockConfig')
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -FrequencyTraceable true')
            elif announce_frequency_traceable == 0:
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -FrequencyTraceable false')

##current_utc_offset
            if current_utc_offset != jNone:
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -UtcOffset '+str(current_utc_offset))

##step_mode
            if step_mode == 'single-step':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -StepMode ONE_STEP')
            elif step_mode == 'two-step':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -StepMode TWO_STEP')

##announce_time_traceable
            if announce_time_traceable == '1':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -TimeTraceable true')
            elif announce_time_traceable == '0':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -TimeTraceable false')

##announce_leap59
            if announce_leap59 == '1':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -Leap59 true')
            elif announce_leap59 == '0':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -Leap59 false')

##announce_leap61
            if announce_leap61 == '1':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -Leap61 true')
            elif announce_leap61 == '0':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -Leap61 false')

#clock_accuracy
            if clock_accuracy == '32':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_025_0NS')
            elif clock_accuracy == '33':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_100_0NS')
            elif clock_accuracy == '34':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_250_0NS')
            elif clock_accuracy == '35':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_001_0US')
            elif clock_accuracy == '36':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_002_5US')
            elif clock_accuracy == '37':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_010_0US')
            elif clock_accuracy == '38':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_025_0US')
            elif clock_accuracy == '39':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_100_0US')
            elif clock_accuracy == '40':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_250_0US')
            elif clock_accuracy == '41':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_001_0MS')
            elif clock_accuracy == '42':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_002_5MS')
            elif clock_accuracy == '43':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_010_0MS')
            elif clock_accuracy == '44':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_025_0MS')
            elif clock_accuracy == '45':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_100_0MS')
            elif clock_accuracy == '46':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_250_0MS')
            elif clock_accuracy == '47':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_001_0S')
            elif clock_accuracy == '48':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy LESS_010_0S')
            elif clock_accuracy == '49':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -ClockAccuracy GREATER_010_0S')
#priority1
            if priority1 != jNone:
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -Priority1 '+str(priority1))

#priority2
            if priority2 != jNone:
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -Priority2 '+str(priority2))
#signal_unicast_handling
            if signal_unicast_handling == 'individually':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -EnableUnicastNegotiation TRUE')
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -UnicastDiscovery ENABLED')
            elif signal_unicast_handling == 'doNotSend':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -EnableUnicastNegotiation TRUE')
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -UnicastDiscovery DISABLED')
#offset_scaled_log_variance
            if offset_scaled_log_variance != jNone:
                if offset_scaled_log_variance.startswith('0x'):
                    offset_scaled_log_variance = int(offset_scaled_log_variance,16)
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -OffsetScaledLogVariance '+str(offset_scaled_log_variance))
#multicastAddress
            if multicastAddress == 'nonforwardable':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -MulticastMACAddr DEFAULT_MAC')
            if multicastAddress == 'forwardable':
                rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -MulticastMACAddr PRIMARY_MAC')
            rt_handle.invoke('invoke', cmd='stc::apply')

#communication_mode
            if communication_mode == 'mixedmode':
               rt_handle.invoke('invoke', cmd='stc::config '+ptp_hndle+' -MessagingMode  MIXED')
            rt_handle.invoke('invoke', cmd='stc::apply')


    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ptp_control(
        rt_handle,
        handle=jNone,
        action=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param action - <start|stop>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['action_control'] = action

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ptp_control.__doc__, **args) 
 
   # if 'action' in args:
   #     args['action_control']= args['action']
   #     del args['action']

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    """
    for hndl in handle:
        args['handle'] = hndl
        port_handle = __get_handle(hndl)
        #args['port_handle'] = port_handle
        ret.append(rt_handle.invoke('emulation_ptp_control', **args))
    
    for hndl in handle:
        hnd = " ".join(global_config[hndl])
        args['handle'] = hnd
        ret.append(rt_handle.invoke('emulation_ptp_control', **args))
    """
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                ret.append(rt_handle.invoke('emulation_ptp_control', **args))
        else:
            args['handle'] = hndl
            ret.append(rt_handle.invoke('emulation_ptp_control', **args))
    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ptp_stats(
        rt_handle,
        handle=jNone):
    """
    :param rt_handle   RT object
    :param handle

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]

    ret = []
    """
    for hndl in handle:
        args['handle'] = hndl

        stats = dict()
        args['mode'] = 'device'
        stats.update(rt_handle.invoke('emulation_ptp_stats', **args))
        ret.append(stats)
    
    for hndl in handle:
        status = 1
        new_ret = dict()
        for hnd in global_config[hndl]:
            args['handle'] = hnd
            stats = dict()
            args['mode'] = 'device'
            stats.update(rt_handle.invoke('emulation_ptp_stats', **args))
            ret.append(stats)
    """
    for hndl in handle:
        if hndl in global_config.keys():
            for hnd in global_config[hndl]:
                args['handle'] = hnd
                stats = dict()
                args['mode'] = 'device'
                stats.update(rt_handle.invoke('emulation_ptp_stats', **args))
                ret.append(stats)
        else:
            args['handle'] = hndl
            stats = dict()
            args['mode'] = 'device'
            stats.update(rt_handle.invoke('emulation_ptp_stats', **args))
            ret.append(stats)
    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_arp_control(
        rt_handle,
        stream_handle=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param stream_handle
    :param port_handle

    Spirent Returns:
    {
        "arpnd_status": "1",
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = stream_handle
    args['port_handle'] = port_handle
    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    if 'handle' in args and not isinstance(stream_handle, list):
        stream_handle = [stream_handle]
        args['handle'] = list(set(stream_handle))

    ret = []
    if 'handle' in args:
        if args['handle'][0].startswith('stream'):
            args['arp_target'] = 'stream'
        else:
            args['arp_target'] = 'device'
    elif 'port_handle' in args:
        args['arp_target'] = 'port'
    else:
        args['arp_target'] = 'all'
    ret.append(rt_handle.invoke('arp_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]
    # ***** End of Return Value Modification *****

    return ret

def j_test_rfc2544_config(
        rt_handle,
        mode=jNone,
        handle=jNone,
        src_port=jNone,
        dst_port=jNone,
        device_count=jNone,
        mac_addr=jNone,
        port_mac_step=jNone,
        device_mac_step=jNone,
        vlan=jNone,
        port_vlan_step=jNone,
        device_vlan_step=jNone,
        vlan_priority=jNone,
        ipv4_addr=jNone,
        port_ipv4_addr_step=jNone,
        device_ipv4_addr_step=jNone,
        ipv4_prefix_len=jNone,
        ipv4_gateway=jNone,
        port_ipv4_gateway_step=jNone,
        ipv6_addr=jNone,
        port_ipv6_addr_step=jNone,
        device_ipv6_addr_step=jNone,
        ipv6_prefix_len=jNone,
        ipv6_gateway=jNone,
        port_ipv6_gateway_step=jNone,
        test_type='b2b',
        endpoint_map=jNone,
        bidirectional=jNone,
        iteration_count=jNone,
        test_duration=jNone,
        frame_size_mode=jNone,
        frame_size=jNone,
        frame_size_start=jNone,
        frame_size_end=jNone,
        frame_size_step=jNone,
        frame_size_min=jNone,
        frame_size_max=jNone,
        load_type=jNone,
        load_unit=jNone,
        load_list=jNone,
        load_start=jNone,
        load_end=jNone,
        load_step=jNone,
        load_min=jNone,
        load_max=jNone,
        latency_type=jNone,
        start_traffic_delay=jNone,
        enable_learning=jNone,
        learning_mode=jNone,
        learning_frequency=jNone,
        learning_rate=jNone,
        l3_learning_retry_count=jNone,
        l2_learning_repeat_count=jNone,
        enable_jitter_measure=jNone,
        accept_frame_loss=jNone,
        search_mode=jNone,
        rate_lower_limit=jNone,
        rate_upper_limit=jNone,
        initial_rate=jNone,
        rate_step=jNone,
        back_off=jNone,
        resolution=jNone,
        rfc5180_enable=jNone,
        ipv6_percentage_iteration_mode=jNone,
        fixed_ipv6_percentage=jNone,
        ipv6_percentage_list=jNone,
        random_ipv6_percentage_min=jNone,
        random_ipv6_percentage_max=jNone,
        ipv6_percentage_start=jNone,
        ipv6_percentage_step=jNone,
        ipv6_percentage_end=jNone):
    """
    :param rt_handle:       RT object
    :param mode - <create|modify|delete>
    :param handle
    :param src_port
    :param dst_port
    :param device_count
    :param mac_addr
    :param port_mac_step
    :param device_mac_step
    :param vlan
    :param port_vlan_step
    :param device_vlan_step
    :param vlan_priority
    :param ipv4_addr
    :param port_ipv4_addr_step
    :param device_ipv4_addr_step
    :param ipv4_prefix_len
    :param ipv4_gateway
    :param port_ipv4_gateway_step
    :param ipv6_addr
    :param port_ipv6_addr_step
    :param device_ipv6_addr_step
    :param ipv6_prefix_len
    :param ipv6_gateway
    :param port_ipv6_gateway_step
    :param test_type
    :param endpoint_map
    :param bidirectional
    :param iteration_count
    :param test_duration
    :param frame_size_mode
    :param frame_size
    :param frame_size_start
    :param frame_size_end
    :param frame_size_step
    :param frame_size_min
    :param frame_size_max
    :param load_type
    :param load_unit
    :param load_list
    :param load_start
    :param load_end
    :param load_step
    :param load_min
    :param load_max
    :param latency_type
    :param start_traffic_delay
    :param enable_learning
    :param learning_mode
    :param learning_frequency
    :param learning_rate
    :param l3_learning_retry_count
    :param l2_learning_repeat_count
    :param enable_jitter_measure
    :param accept_frame_loss
    :param search_mode
    :param rate_lower_limit
    :param rate_upper_limit
    :param initial_rate
    :param rate_step
    :param back_off
    :param resolution
    :param rfc5180_enable
    :param ipv6_percentage_iteration_mode
    :param fixed_ipv6_percentage
    :param ipv6_percentage_list
    :param random_ipv6_percentage_min
    :param random_ipv6_percentage_max
    :param ipv6_percentage_start
    :param ipv6_percentage_step
    :param ipv6_percentage_end

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "port_handle": "port1",
        "pppox_port": "pppoxportconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/range:HLAPI0",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1",
        "pppox_server_handle": "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1",
        "pppox_server_sessions_handle": "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1/pppoxServerSessions",
        "status": "1"
    }

    Common Return Keys:
        "handles"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode
    args['handle'] = handle
    args['src_port'] = src_port
    args['dst_port'] = dst_port
    args['device_count'] = device_count
    args['mac_addr'] = mac_addr
    args['port_mac_step'] = port_mac_step
    args['device_mac_step'] = device_mac_step
    args['vlan'] = vlan
    args['port_vlan_step'] = port_vlan_step
    args['device_vlan_step'] = device_vlan_step
    args['vlan_priority'] = vlan_priority
    args['ipv4_addr'] = ipv4_addr
    args['port_ipv4_addr_step'] = port_ipv4_addr_step
    args['device_ipv4_addr_step'] = device_ipv4_addr_step
    args['ipv4_prefix_len'] = ipv4_prefix_len
    args['ipv4_gateway'] = ipv4_gateway
    args['port_ipv4_gateway_step'] = port_ipv4_gateway_step
    args['ipv6_addr'] = ipv6_addr
    args['port_ipv6_addr_step'] = port_ipv6_addr_step
    args['device_ipv6_addr_step'] = device_ipv6_addr_step
    args['ipv6_prefix_len'] = ipv6_prefix_len
    args['ipv6_gateway'] = ipv6_gateway
    args['port_ipv6_gateway_step'] = port_ipv6_gateway_step
    args['test_type'] = test_type
    args['endpoint_map'] = endpoint_map
    args['bidirectional'] = bidirectional
    args['iteration_count'] = iteration_count
    args['test_duration'] = test_duration
    args['frame_size_mode'] = frame_size_mode
    args['frame_size'] = frame_size
    args['frame_size_start'] = frame_size_start
    args['frame_size_end'] = frame_size_end
    args['frame_size_step'] = frame_size_step
    args['frame_size_min'] = frame_size_min
    args['frame_size_max'] = frame_size_max
    args['load_type'] = load_type
    args['load_unit'] = load_unit
    args['load_list'] = load_list
    args['load_start'] = load_start
    args['load_end'] = load_end
    args['load_step'] = load_step
    args['load_min'] = load_min
    args['latency_type'] = latency_type
    args['start_traffic_delay'] = start_traffic_delay
    args['enable_learning'] = enable_learning
    args['learning_mode'] = learning_mode
    args['learning_frequency'] = learning_frequency
    args['learning_rate'] = learning_rate
    args['l3_learning_retry_count'] = l3_learning_retry_count
    args['l2_learning_repeat_count'] = l2_learning_repeat_count
    args['enable_jitter_measure'] = enable_jitter_measure
    args['accept_frame_loss'] = accept_frame_loss
    args['search_mode'] = search_mode
    args['rate_lower_limit'] = rate_lower_limit
    args['rate_upper_limit'] = rate_upper_limit
    args['initial_rate'] = initial_rate
    args['rate_step'] = rate_step
    args['back_off'] = back_off
    args['resolution'] = resolution
    args['rfc5180_enable'] = rfc5180_enable
    args['ipv6_percentage_iteration_mode'] = ipv6_percentage_iteration_mode
    args['fixed_ipv6_percentage'] = fixed_ipv6_percentage
    args['ipv6_percentage_list'] = ipv6_percentage_list
    args['random_ipv6_percentage_min'] = random_ipv6_percentage_min
    args['random_ipv6_percentage_max'] = random_ipv6_percentage_max
    args['ipv6_percentage_start'] = ipv6_percentage_start
    args['ipv6_percentage_step'] = ipv6_percentage_step
    args['ipv6_percentage_end'] = ipv6_percentage_end

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_test_rfc2544_config.__doc__, **args)

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        args['handle'] = hndl
        args['endpoint_creation'] = 1
        args['test_duration_mode'] = 'seconds'
        args['traffic_pattern'] = 'pair'
        ret.append(rt_handle.invoke('test_rfc2544_config', **args))


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_test_rfc2544_control(
        rt_handle,
        action=jNone,
        wait=jNone):
    """
    :param rt_handle:       RT object
    :param action - <run|stop>
    :param wait


    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """



    args = dict()
    args['action'] = action
    args['wait'] = wait

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
 
    args = get_arg_value(rt_handle, j_test_rfc2544_control.__doc__, **args)
    
    ret = []

    ret.append(rt_handle.invoke('test_rfc2544_control', **args))


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_test_rfc2544_info(
        rt_handle,
        test_type=jNone):
    """
    :param rt_handle:       RT object
    :param test_type - <b2b|fl|latency|throughput>


    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    args = dict()
    args['test_type'] = test_type

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_test_rfc2544_info.__doc__, **args)    

    ret = []

    ret.append(rt_handle.invoke('test_rfc2544_info', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret




def j_emulation_dot1x_config(
        rt_handle,
        mode=jNone,
        port_handle=jNone,
        handle=jNone,
        eap_auth_method=jNone,
        encapsulation=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        gateway_ipv6_addr=jNone,
        gateway_ipv6_addr_step=jNone,
        ip_version=jNone,
        local_ip_addr=jNone,
        local_ip_addr_step=jNone,
        local_ip_prefix_len=jNone,
        local_ipv6_addr=jNone,
        local_ipv6_addr_step=jNone,
        local_ipv6_prefix_len=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        password=jNone,
        username=jNone,
        auth_retry_count=jNone,
        auth_retry_interval=jNone,
        max_authentications=jNone,
        supplicant_auth_rate=jNone,
        num_sessions=jNone,
        vlan_id=jNone,
        vlan_ether_type=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        vlan_outer_id=jNone,
        vlan_outer_ether_type=jNone,
        vlan_outer_id_step=jNone,
        vlan_outer_user_priority=jNone,
        supplicant_logoff_rate=jNone,
        certificate_directory=jNone,
        peer_certificate_file=jNone,
        password_wildcard=jNone,
        username_wildcard=jNone,
        wildcard_pound_start=jNone,
        wildcard_pound_end=jNone):
    """
    :param rt_handle:       RT object
    :param mode - <create|modify|delete>
    :param port_handle
    :param handle
    :param eap_auth_method - <md5|fast|tls>
    :param encapsulation - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq>
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param gateway_ipv6_addr
    :param gateway_ipv6_addr_step
    :param ip_version
    :param local_ip_addr
    :param local_ip_addr_step
    :param local_ip_prefix_len
    :param local_ipv6_addr
    :param local_ipv6_addr_step
    :param local_ipv6_prefix_len - <0-128>
    :param mac_addr
    :param mac_addr_step
    :param password
    :param username
    :param auth_retry_count - <1-100> 
    :param auth_retry_interval - <1-3600>
    :param max_authentications - <1-100>
    :param supplicant_auth_rate - <1-3600>
    :param num_sessions
    :param vlan_id - <0-4095>
    :param vlan_ether_type - <0x8100|0x88A8|0x9100|0x9200>
    :param vlan_id_step - <0-4095>
    :param vlan_user_priority - <0-7>
    :param vlan_outer_id - <0-4095>
    :param vlan_outer_ether_type - <0x8100|0x88A8|0x9100|0x9200>
    :param vlan_outer_id_step - <0-4095>
    :param vlan_outer_user_priority - <0-7>
    :param supplicant_logoff_rate - <1-1024>
    :param certificate_directory
    :param peer_certificate_file
    :param password_wildcard - <0|1>
    :param username_wildcard - <0|1>
    :param wildcard_pound_start - <0-65535>
    :param wildcard_pound_end - <0-65535> 

    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    args = dict()
    args['mode'] = mode
    args['port_handle'] = port_handle
    args['handle'] = handle
    args['eap_auth_method'] = eap_auth_method
    args['gateway_ip_addr'] = gateway_ip_addr
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['gateway_ipv6_addr'] = gateway_ipv6_addr
    args['gateway_ipv6_addr_step'] = gateway_ipv6_addr_step
    args['ip_version'] = ip_version
    args['local_ip_addr'] = local_ip_addr
    args['local_ip_addr_step'] = local_ip_addr_step
    args['local_ip_prefix_len'] = local_ip_prefix_len
    args['local_ipv6_addr'] = local_ipv6_addr
    args['local_ipv6_addr_step'] = local_ipv6_addr_step
    args['local_ipv6_prefix_len'] = local_ipv6_prefix_len
    args['mac_addr'] = mac_addr
    args['mac_addr_step'] = mac_addr_step
    args['password'] = password
    args['username'] = username
    args['auth_retry_count'] = auth_retry_count
    args['auth_retry_interval'] = auth_retry_interval
    args['max_authentications'] = max_authentications
    args['supplicant_auth_rate'] = supplicant_auth_rate
    args['num_sessions'] = num_sessions
    args['encapsulation'] = encapsulation
    args['vlan_id'] = vlan_id
    args['vlan_ether_type'] = vlan_ether_type
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['vlan_outer_id'] = vlan_outer_id
    args['vlan_outer_ether_type'] = vlan_outer_ether_type
    args['vlan_outer_id_step'] = vlan_outer_id_step
    args['vlan_outer_user_priority'] = vlan_outer_user_priority
    args['supplicant_logoff_rate'] = supplicant_logoff_rate
    args['certificate_directory'] = certificate_directory
    args['peer_certificate_file'] = peer_certificate_file
    args['password_wildcard'] = password_wildcard
    args['username_wildcard'] = username_wildcard
    args['wildcard_pound_start'] = wildcard_pound_start
    args['wildcard_pound_end'] = wildcard_pound_end

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
   
    args = get_arg_value(rt_handle, j_emulation_dot1x_config.__doc__, **args)

    if 'certificate_directory' in args.keys() and 'peer_certificate_file' in args.keys():
        args['certificate'] = str(args['certificate_directory'])+'/'+str(args['peer_certificate_file'])
        del args['certificate_directory']
        del args['peer_certificate_file']
    ret = []
    handles = jNone
    if 'handle' not in args and 'port_handle' not in args:
        raise RuntimeError('Either handle or port_handle argument must be passed to j_emulation_dot1x_config')
    elif 'handle' in args:
        handles = handle
    elif 'port_handle' in args:
        handles = port_handle

    if not isinstance(handles, list):
        handles = [handles]
    handles = list(set(handles))
    counter = 1
    string = "dot1x_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "dot1x_" + str(counter)
    global_config[string] = []

    for hndl in handles:
        args['handle'] = hndl
        if mode == 'create':
            args['port_handle'] = hndl
            del args['handle']
        elif mode == 'modify' or mode == 'delete':
            for hnd in global_config[hndl]:
                args['handle'] = hnd
        result = rt_handle.invoke('emulation_dot1x_config', **args)
        if result.get('handle'):
            global_config[string].extend(result['handle'].split(' '))
            result['handles'] = string
        if 'port_handle' in result.keys():
            if not isinstance(result['port_handle'], list):
                port_handle = [result['port_handle']]
            port_handle = list(set(port_handle))
        if mode == 'create':
            for hand in port_handle:
                session_map[hand] = session_map.get(hand, [])
                session_map[hand].extend(global_config[string])
                session_map[string] = hand
                handle_map[hand] = handle_map.get(hand, [])
                handle_map[hand].extend(global_config[string])
                handle_map[string] = hand
        ret.append(result)
    # ***** Return Value Modification *****
    if len(ret) == 1:
        ret = ret[0]
    # ***** End of Return Value Modification *****
    return ret

def j_emulation_dot1x_control(
        rt_handle,
        mode=jNone,
        handle=jNone):
    """
    :param rt_handle:       RT object
    :param mode - <start|stop|logout>
    :param handle
    """
    # ***** Following is user's custom code *****
    #
    # ***** End of user's custom code *****
    args = dict()
    args['mode'] = mode
    args['handle'] = handle
    # ***** Following is user's custom code *****
    #
    # ***** End of user's custom code *****


    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    
    args = get_arg_value(rt_handle, j_emulation_dot1x_control.__doc__, **args)
     
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    ret = []
    for hndl in handle:
        for hnd in global_config[hndl]:
            args['handle'] = hnd
            ret.append(rt_handle.invoke('emulation_dot1x_control', **args))
            if 'handle' in ret[-1]:
                ret[-1]['handles'] = ret[-1]['handle']
    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_dot1x_stats(
        rt_handle,
        mode=jNone,
        handle=jNone):
    """
    :param rt_handle:       RT object
    :param mode
    :param handle
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    args = dict()
    args['mode'] = mode
    args['handle'] = handle
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]

    ret = []
    for hndl in handle:
        for hnd in global_config[hndl]:
            args['handle'] = hnd
            stats = dict()
            args['mode'] = 'aggregate'
            stats.update(rt_handle.invoke('emulation_dot1x_stats', **args))
            args['mode'] = 'session'
            stats.update(rt_handle.invoke('emulation_dot1x_stats', **args))
            if 'session' in stats:
                for key in list(stats['session']):
                    stats['session'][args['handle']] = stats['session'][key]
            ret.append(stats)

    # ***** Return Value Modification *****
    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_pppox_server_config(
        rt_handle,
        attempt_rate=jNone,
        auth_mode=jNone,
        config_req_timeout=jNone,
        disconnect_rate=jNone,
        echo_req_interval=jNone,
        handle=jNone,
        ipcp_req_timeout=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        max_configure_req=jNone,
        max_ipcp_req=jNone,
        max_outstanding=jNone,
        max_terminate_req=jNone,
        num_sessions=jNone,
        password_wildcard=jNone,
        qinq_incr_mode=jNone,
        username_wildcard=jNone,
        vlan_id=jNone,
        vlan_id_count=jNone,
        vlan_id_outer=jNone,
        vlan_id_outer_count=jNone,
        vlan_id_outer_step=jNone,
        vlan_id_step=jNone,
        vlan_user_priority=jNone,
        vlan_outer_user_priority=jNone,
        username=jNone,
        password=jNone,
        ip_cp=jNone,
        ipv4_pool_addr_start=jNone,
        ipv4_pool_addr_prefix_len=jNone,
        ipv6_pool_addr_start=jNone,
        ipv6_pool_addr_prefix_len=jNone,
        intf_ip_addr=jNone,
        intf_ip_prefix_length=jNone,
        protocol=jNone,
        mode=jNone,
        encap=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param attempt_rate - <1-1000>
    :param auth_mode - <none|pap|chap|pap_or_chap>
    :param config_req_timeout - <1-120>
    :param disconnect_rate - <1-1000>
    :param echo_req_interval - <1-3600>
    :param handle
    :param ipcp_req_timeout - <1-120>
    :param mac_addr
    :param mac_addr_step
    :param max_configure_req - <1-255>
    :param max_ipcp_req - <1-255>
    :param max_outstanding - <2-1000>
    :param max_terminate_req - <1-65535>
    :param num_sessions - <1-32000>
    :param password_wildcard - <1|0>
    :param qinq_incr_mode - <inner|outer|both>
    :param username_wildcard - <1|0>
    :param vlan_id - <0-4095>
    :param vlan_id_count - <1-4094>
    :param vlan_id_outer - <0-4095>
    :param vlan_id_outer_count - <1-4094>
    :param vlan_id_outer_step - <0-4094>
    :param vlan_id_step - <1-4095>
    :param vlan_user_priority - <0-7>
    :param vlan_outer_user_priority - <0-7>
    :param username
    :param password
    :param ip_cp - <ipv4_cp|ipv6_cp|ipv4v6_cp:dual_stack>
    :param ipv4_pool_addr_start
    :param ipv4_pool_addr_prefix_len
    :param ipv6_pool_addr_start
    :param ipv6_pool_addr_prefix_len
    :param intf_ip_addr
    :param intf_ip_prefix_length
    :param protocol - <pppoe|pppoa|pppoeoa>
    :param mode - <create:add|modify|reset:remove>
    :param encap - <ethernet_ii|ethernet_ii_vlan|ethernet_ii_qinq|vc_mux|llcsnap>
    :param port_handle

    Spirent Returns:
    {
        "handle": "host1",
        "handles": "host1",
        "port_handle": "port1",
        "pppox_port": "pppoxportconfig1",
        "status": "1"
    }

    IXIA Returns:
    {
        "handle": "/range:HLAPI0",
        "handles": "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1",
        "pppox_server_handle": "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1",
        "pppox_server_sessions_handle": "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1/pppoxServerSessions",
        "status": "1"
    }

    Common Return Keys:
        "handles"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['attempt_rate'] = attempt_rate
    args['auth_mode'] = auth_mode
    args['config_req_timeout'] = config_req_timeout
    args['disconnect_rate'] = disconnect_rate
    args['echo_req_interval'] = echo_req_interval
    args['handle'] = handle
    args['ipcp_req_timeout'] = ipcp_req_timeout
    args['mac_addr'] = mac_addr
    args['mac_addr_step'] = mac_addr_step
    args['max_configure_req'] = max_configure_req
    args['max_ipcp_req'] = max_ipcp_req
    args['max_outstanding'] = max_outstanding
    args['max_terminate_req'] = max_terminate_req
    args['num_sessions'] = num_sessions
    args['password_wildcard'] = password_wildcard
    args['qinq_incr_mode'] = qinq_incr_mode
    args['username_wildcard'] = username_wildcard
    args['vlan_id'] = vlan_id
    args['vlan_id_count'] = vlan_id_count
    args['vlan_id_outer'] = vlan_id_outer
    args['vlan_id_outer_count'] = vlan_id_outer_count
    args['vlan_id_outer_step'] = vlan_id_outer_step
    args['vlan_id_step'] = vlan_id_step
    args['vlan_user_priority'] = vlan_user_priority
    args['vlan_outer_user_priority'] = vlan_outer_user_priority
    args['username'] = username
    args['password'] = password
    args['ip_cp'] = ip_cp
    args['ipv4_pool_addr_start'] = ipv4_pool_addr_start
    args['ipv4_pool_addr_prefix_len'] = ipv4_pool_addr_prefix_len
    args['ipv6_pool_prefix_start'] = ipv6_pool_addr_start
    args['ipv6_pool_prefix_len'] = ipv6_pool_addr_prefix_len
    args['intf_ip_addr'] = intf_ip_addr
    args['intf_ip_prefix_length'] = intf_ip_prefix_length
    args['protocol'] = protocol
    args['mode'] = mode
    args['encap'] = encap
    args['port_handle'] = port_handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    args = get_arg_value(rt_handle, j_pppox_server_config.__doc__, **args)
    ret = []
    handle_list = dict()
    counter = 1
    string = "pppox_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "pppox_" + str(counter)
    global_config[string] = []
    if port_handle != jNone:
        args['port_handle'] = port_handle
        result = rt_handle.invoke('pppox_server_config', **args)
        if result.get('handle'):
            result['handle'] = result['handle'].split(' ')
            if mode == 'enable' or mode == 'create':
                global_config[string].extend(result['handle'])
                result['handles'] = string
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        for hand in port_handle:
            handle_map[hand] = handle_map.get(hand, [])
            handle_map[hand].extend(global_config[string])
            handle_map[string] = hand
        ret.append(result)
    
    elif handle != jNone:
        ret.append(invoke_handle(rt_handle, protocol_string=string, **args))
    else:
        raise RuntimeError('Either handle or port_handle argument must be passed to j_pppox_server_config')

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_pppox_server_control(rt_handle, action=jNone, handle=jNone):
    """
    :param rt_handle:       RT object
    :param action - <abort|connect|disconnect|reset>
    :param handle

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['action'] = action
    args['handle'] = handle

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_pppox_server_control.__doc__, **args)
   
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        hnd = " ".join(global_config[hndl])
        args['handle'] = hnd
        ret.append(rt_handle.invoke('pppox_server_control', **args))


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_pppox_server_stats(rt_handle, handle=jNone, mode=jNone):
    """
    :param rt_handle:       RT object
    :param handle
    :param mode - <aggregate|session>

    Spirent Returns:
    {
        "aggregate": {
            "abort": "0",
            "atm_mode": "0",
            "avg_setup_time": "0",
            "chap_auth_rx": "1",
            "chap_auth_tx": "2",
            "connect_attempts": "0",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "disconnect_failed": "0",
            "disconnect_success": "0",
            "disconnecting": "0",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_rsp_rx": "0",
            "echo_rsp_tx": "0",
            "idle": "0",
            "ipcp_rx": "3",
            "ipcp_tx": "3",
            "ipcpv6_rx": "0",
            "ipcpv6_tx": "0",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "max_setup_time": "0",
            "min_setup_time": "0",
            "num_sessions": "1",
            "padi_rx": "1",
            "padi_tx": "0",
            "pado_rx": "0",
            "pado_tx": "1",
            "padr_rx": "1",
            "padr_tx": "0",
            "pads_rx": "0",
            "pads_tx": "1",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_rx": "0",
            "pap_auth_tx": "0",
            "session_retried": "0",
            "sessions_down": "0",
            "sessions_up": "1",
            "success_setup_rate": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "port_handle": "port1",
        "session": {
            "host1": {
                "abort": "0",
                "atm_mode": "0",
                "chap_auth_rx": "1",
                "chap_auth_tx": "2",
                "connect_success": "1",
                "connected": "1",
                "connecting": "0",
                "disconnect_failed": "0",
                "disconnect_success": "0",
                "disconnecting": "0",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_rsp_rx": "0",
                "echo_rsp_tx": "0",
                "idle": "0",
                "ipcp_rx": "3",
                "ipcp_tx": "3",
                "ipcpv6_rx": "0",
                "ipcpv6_tx": "0",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "padi_rx": "1",
                "pado_tx": "1",
                "padr_rx": "1",
                "pads_tx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_rx": "0",
                "pap_auth_tx": "0",
                "sessions_down": "0",
                "sessions_up": "1",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0"
            }
        },
        "status": "1"
    }

    IXIA Returns:
    {
        "Range 1/25/2 2 False": {
            "aggregate": {
                "auth_avg_time": "2727.30",
                "auth_max_time": "27273",
                "auth_min_time": "27273",
                "avg_setup_time": "8464.20",
                "chap_auth_chal_tx": "1",
                "chap_auth_fail_tx": "0",
                "chap_auth_rsp_rx": "1",
                "chap_auth_succ_tx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "connect_success": "1",
                "connected": "1",
                "connecting": "0",
                "device_group": "Range 1/25/2 2 False",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_resp_rx": "0",
                "echo_resp_tx": "0",
                "idle": "9",
                "interfaces_in_chap_negotiation": "0",
                "interfaces_in_ipcp_negotiation": "0",
                "interfaces_in_ipv6cp_negotiation": "0",
                "interfaces_in_lcp_negotiation": "0",
                "interfaces_in_pap_negotiation": "0",
                "interfaces_in_ppp_negotiation": "0",
                "interfaces_in_pppoe_l2tp_negotiation": "0",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "0",
                "ipcp_cfg_nak_tx": "1",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "2",
                "ipcp_cfg_req_tx": "1",
                "ipv6_cp_router_solicitaion_rx": "0",
                "ipv6cp_avg_time": "0.00",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_max_time": "0",
                "ipv6cp_min_time": "0",
                "ipv6cp_router_adv_tx": "0",
                "lcp_avg_latency": "4736.20",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_max_latency": "47362",
                "lcp_min_latency": "47362",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "ncp_avg_latency": "573.80",
                "ncp_max_latency": "5738",
                "ncp_min_latency": "5738",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "num_sessions": "10",
                "padi_rx": "1",
                "pado_tx": "1",
                "padr_rx": "1",
                "pads_tx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_tx": "0",
                "pap_auth_nak_tx": "0",
                "pap_auth_req_rx": "0",
                "ppp_total_bytes_rx": "92",
                "ppp_total_bytes_tx": "147",
                "pppoe_avg_latency": "413.50",
                "pppoe_max_latency": "4135",
                "pppoe_min_latency": "4135",
                "pppoe_total_bytes_rx": "20",
                "pppoe_total_bytes_tx": "36",
                "sessions_down": "0",
                "sessions_failed": "0",
                "sessions_initiated": "9",
                "sessions_up": "1",
                "teardown_failed": "0",
                "teardown_succeded": "0",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0"
            }
        },
        "aggregate": {
            "auth_avg_time": "2727.30",
            "auth_max_time": "27273",
            "auth_min_time": "27273",
            "avg_setup_time": "8464.20",
            "chap_auth_chal_tx": "1",
            "chap_auth_fail_tx": "0",
            "chap_auth_rsp_rx": "1",
            "chap_auth_succ_tx": "1",
            "code_rej_rx": "0",
            "code_rej_tx": "0",
            "connect_success": "1",
            "connected": "1",
            "connecting": "0",
            "device_group": "Range 1/25/2 2 False",
            "echo_req_rx": "0",
            "echo_req_tx": "0",
            "echo_resp_rx": "0",
            "echo_resp_tx": "0",
            "idle": "9",
            "interfaces_in_chap_negotiation": "0",
            "interfaces_in_ipcp_negotiation": "0",
            "interfaces_in_ipv6cp_negotiation": "0",
            "interfaces_in_lcp_negotiation": "0",
            "interfaces_in_pap_negotiation": "0",
            "interfaces_in_ppp_negotiation": "0",
            "interfaces_in_pppoe_l2tp_negotiation": "0",
            "ipcp_cfg_ack_rx": "1",
            "ipcp_cfg_ack_tx": "1",
            "ipcp_cfg_nak_rx": "0",
            "ipcp_cfg_nak_tx": "1",
            "ipcp_cfg_rej_rx": "0",
            "ipcp_cfg_rej_tx": "0",
            "ipcp_cfg_req_rx": "2",
            "ipcp_cfg_req_tx": "1",
            "ipv6_cp_router_solicitaion_rx": "0",
            "ipv6cp_avg_time": "0.00",
            "ipv6cp_cfg_ack_rx": "0",
            "ipv6cp_cfg_ack_tx": "0",
            "ipv6cp_cfg_nak_rx": "0",
            "ipv6cp_cfg_nak_tx": "0",
            "ipv6cp_cfg_rej_rx": "0",
            "ipv6cp_cfg_rej_tx": "0",
            "ipv6cp_cfg_req_rx": "0",
            "ipv6cp_cfg_req_tx": "0",
            "ipv6cp_max_time": "0",
            "ipv6cp_min_time": "0",
            "ipv6cp_router_adv_tx": "0",
            "lcp_avg_latency": "4736.20",
            "lcp_cfg_ack_rx": "1",
            "lcp_cfg_ack_tx": "1",
            "lcp_cfg_nak_rx": "0",
            "lcp_cfg_nak_tx": "0",
            "lcp_cfg_rej_rx": "0",
            "lcp_cfg_rej_tx": "0",
            "lcp_cfg_req_rx": "1",
            "lcp_cfg_req_tx": "1",
            "lcp_max_latency": "47362",
            "lcp_min_latency": "47362",
            "lcp_protocol_rej_rx": "0",
            "lcp_protocol_rej_tx": "0",
            "lcp_total_msg_rx": "2",
            "lcp_total_msg_tx": "2",
            "ncp_avg_latency": "573.80",
            "ncp_max_latency": "5738",
            "ncp_min_latency": "5738",
            "ncp_total_msg_rx": "3",
            "ncp_total_msg_tx": "3",
            "num_sessions": "10",
            "padi_rx": "1",
            "pado_tx": "1",
            "padr_rx": "1",
            "pads_tx": "1",
            "padt_rx": "0",
            "padt_tx": "0",
            "pap_auth_ack_tx": "0",
            "pap_auth_nak_tx": "0",
            "pap_auth_req_rx": "0",
            "ppp_total_bytes_rx": "92",
            "ppp_total_bytes_tx": "147",
            "pppoe_avg_latency": "413.50",
            "pppoe_max_latency": "4135",
            "pppoe_min_latency": "4135",
            "pppoe_total_bytes_rx": "20",
            "pppoe_total_bytes_tx": "36",
            "sessions_down": "0",
            "sessions_failed": "0",
            "sessions_initiated": "9",
            "sessions_up": "1",
            "teardown_failed": "0",
            "teardown_succeded": "0",
            "term_ack_rx": "0",
            "term_ack_tx": "0",
            "term_req_rx": "0",
            "term_req_tx": "0"
        },
        "session": {
            "/topology:1/deviceGroup:1/ethernet:1/pppoxserver:1/item:1": {
                "ac_mac_addr": "00:11:02:00:00:01",
                "ac_name": "",
                "auth_establishment_time": "27273",
                "auth_id": "user",
                "auth_password": "secret",
                "auth_protocol_rx": "None",
                "auth_protocol_tx": "CHAP",
                "auth_total_rx": "1",
                "auth_total_tx": "2",
                "call_state": "Idle",
                "cdn_rx": "0",
                "cdn_tx": "0",
                "chap_auth_chal_tx": "1",
                "chap_auth_fail_tx": "0",
                "chap_auth_role": "Peer",
                "chap_auth_rsp_rx": "1",
                "chap_auth_succ_tx": "1",
                "code_rej_rx": "0",
                "code_rej_tx": "0",
                "data_ns": "0",
                "destination_ip": "0.0.0.0",
                "destination_port": "0",
                "device_group": "Range 1/25/2 2 False",
                "device_id": "1",
                "dns_server_list": "Not Available",
                "echo_req_rx": "0",
                "echo_req_tx": "0",
                "echo_resp_rx": "0",
                "echo_resp_tx": "0",
                "establishment_time": "84642",
                "gateway_ip": "0.0.0.0",
                "generic_error_tag_tx": "0",
                "host_mac_addr": "00:11:01:00:00:01",
                "host_name": "Not Available",
                "iccn_rx": "0",
                "iccn_tx": "0",
                "icrp_rx": "0",
                "icrp_tx": "0",
                "icrq_rx": "0",
                "icrq_tx": "0",
                "ip_cpe_establishment_time": "5738",
                "ipcp_cfg_ack_rx": "1",
                "ipcp_cfg_ack_tx": "1",
                "ipcp_cfg_nak_rx": "0",
                "ipcp_cfg_nak_tx": "1",
                "ipcp_cfg_rej_rx": "0",
                "ipcp_cfg_rej_tx": "0",
                "ipcp_cfg_req_rx": "2",
                "ipcp_cfg_req_tx": "1",
                "ipcp_state": "NCP Open",
                "ipcp_terminate_ack_rx": "0",
                "ipcp_terminate_ack_tx": "0",
                "ipcp_terminate_req_rx": "0",
                "ipcp_terminate_req_tx": "0",
                "ipv6_addr": "0:0:0:0:0:0:0:0",
                "ipv6_cp_router_solicitaion_rx": "0",
                "ipv6_cpe_establishment_time": "0",
                "ipv6_prefix_len": "0",
                "ipv6cp_cfg_ack_rx": "0",
                "ipv6cp_cfg_ack_tx": "0",
                "ipv6cp_cfg_nak_rx": "0",
                "ipv6cp_cfg_nak_tx": "0",
                "ipv6cp_cfg_rej_rx": "0",
                "ipv6cp_cfg_rej_tx": "0",
                "ipv6cp_cfg_req_rx": "0",
                "ipv6cp_cfg_req_tx": "0",
                "ipv6cp_router_adv_tx": "0",
                "ipv6cp_state": "NCP Disable",
                "ipv6cp_terminate_ack_rx": "0",
                "ipv6cp_terminate_ack_tx": "0",
                "ipv6cp_terminate_req_rx": "0",
                "ipv6cp_terminate_req_tx": "0",
                "lcp_cfg_ack_rx": "1",
                "lcp_cfg_ack_tx": "1",
                "lcp_cfg_nak_rx": "0",
                "lcp_cfg_nak_tx": "0",
                "lcp_cfg_rej_rx": "0",
                "lcp_cfg_rej_tx": "0",
                "lcp_cfg_req_rx": "1",
                "lcp_cfg_req_tx": "1",
                "lcp_establishment_time": "47362",
                "lcp_protocol_rej_rx": "0",
                "lcp_protocol_rej_tx": "0",
                "lcp_total_msg_rx": "2",
                "lcp_total_msg_tx": "2",
                "local_ip_addr": "1.1.1.1",
                "local_ipv6_iid": "Not Available",
                "loopback_detected": "False",
                "magic_no_negotiated": "True",
                "magic_no_rx": "771179460",
                "magic_no_tx": "3769293702",
                "mru": "1500",
                "mtu": "1500",
                "ncp_total_msg_rx": "3",
                "ncp_total_msg_tx": "3",
                "negotiation_end_ms": "534096587",
                "negotiation_start_ms": "534011945",
                "our_call_id": "0",
                "our_cookie": "Not Available",
                "our_cookie_length": "0",
                "our_tunnel_id": "0",
                "padi_rx": "1",
                "pado_tx": "1",
                "padr_rx": "1",
                "pads_tx": "1",
                "padt_rx": "0",
                "padt_tx": "0",
                "pap_auth_ack_tx": "0",
                "pap_auth_nak_tx": "0",
                "pap_auth_req_rx": "0",
                "peer_call_id": "0",
                "peer_ipv6_iid": "Not Available",
                "peer_tunnel_id": "0",
                "ppp_close_mode": "None",
                "ppp_state": "PPP Connected",
                "ppp_total_rx": "92",
                "ppp_total_tx": "147",
                "pppoe_latency": "4135",
                "pppoe_state": "Session",
                "pppoe_total_bytes_rx": "20",
                "pppoe_total_bytes_tx": "36",
                "primary_wins_server": "0.0.0.0",
                "protocol": "PPPoX Server 1",
                "relay_session_id_tag_rx": "0",
                "remote_ip_addr": "1.1.1.2",
                "secondary_wins_server": "0.0.0.0",
                "service_name": "",
                "session_id": "1",
                "source_ip": "0.0.0.0",
                "source_port": "0",
                "status": "up",
                "term_ack_rx": "0",
                "term_ack_tx": "0",
                "term_req_rx": "0",
                "term_req_tx": "0",
                "topology": "T 1/25/2",
                "tunnel_state": "Tunnel Idle",
                "vendor_specific_tag_rx": "0"
            }
        },
        "status": "1"
    }

    Common Return Keys:
        "aggregate"
        "session"
        "status"
    """

    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['handle'] = handle
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_pppox_server_stats.__doc__, **args)
  
    __check_and_raise(handle)
    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))

    ret = []
    for hndl in handle:
        for hnd in global_config[hndl]:
            args['handle'] = hnd
            stats = dict()
            args['mode'] = 'aggregate'
            stats.update(rt_handle.invoke('pppox_server_stats', **args))
            args['mode'] = 'session'
            stats.update(rt_handle.invoke('pppox_server_stats', **args))
            if 'session' in stats:
                for key in list(stats['session']):
                    stats['session'][hndl] = stats['session'][key]
            ret.append(stats)


    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ipv6_autoconfig(
        rt_handle,
        mode=jNone,
        port_handle=jNone,
        handle=jNone,
        ip_version=jNone,
        encap=jNone,
        count=jNone,
        mac_addr=jNone,
        mac_addr_step=jNone,
        local_ip_addr=jNone,
        local_ip_addr_step=jNone,
        local_ip_prefix_len=jNone,
        gateway_ip_addr=jNone,
        gateway_ip_addr_step=jNone,
        router_solicit_retry=jNone,
        vlan_id=jNone,
        vlan_id_mode=jNone,
        vlan_id_step=jNone,
        vlan_id_repeat_count=jNone,
        vlan_priority=jNone,
        dad_enable=jNone):
    """
    :param rt_handle:       RT object
    :param mode - <create:config|modify|reset:destroy>
    :param port_handle
    :param handle
    :param ip_version - <6|4_6>
    :param encap - <ethernet_ii|ethernet_vlan|ethernet_ii_vlan>
    :param count - <1-65536>
    :param mac_addr
    :param mac_addr_step
    :param local_ip_addr
    :param local_ip_addr_step
    :param local_ip_prefix_len - <0-32>
    :param gateway_ip_addr
    :param gateway_ip_addr_step
    :param router_solicit_retry - <1-100>
    :param vlan_id - <0-4095>
    :param vlan_id_mode - <fixed|increment>
    :param vlan_id_step - <0-4094>
    :param vlan_id_repeat_count
    :param vlan_priority - <0-7>
    :param dad_enable
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    args = dict()
    args['mode'] = mode
    args['port_handle'] = port_handle
    args['handle'] = handle
    args['ip_version'] = ip_version
    args['encap'] = encap
    args['count'] = count
    args['mac_addr'] = mac_addr
    args['mac_addr_step'] = mac_addr_step
    args['local_ip_addr'] = local_ip_addr
    args['local_ip_addr_step'] = local_ip_addr_step
    args['local_ip_prefix_len'] = local_ip_prefix_len
    args['gateway_ip_addr'] = gateway_ip_addr
    args['gateway_ip_addr_step'] = gateway_ip_addr_step
    args['router_solicit_retry'] = router_solicit_retry
    args['vlan_id'] = vlan_id
    args['vlan_id_mode'] = vlan_id_mode
    args['vlan_id_step'] = vlan_id_step
    args['vlan_id_repeat_count'] = vlan_id_repeat_count
    args['vlan_priority'] = vlan_priority
    args['dad_enable'] = dad_enable

     # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_emulation_ipv6_autoconfig.__doc__, **args)   
    if port_handle == jNone:
        __check_and_raise(handle)
    elif handle == jNone:
        __check_and_raise(port_handle)

    if encap != jNone and encap == 'ethernet_ii_vlan':
       args['encap'] = 'ethernet_vlan'
    
    counter = 1
    string = "ipv6_auto_" + str(counter)
    while string in global_config:
        counter = counter + 1
        string = "ipv6_auto_" + str(counter)
    global_config[string] = []
    ret = []
    if handle != jNone:
        if not isinstance(handle, list):
            handle = [handle]
        handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    args['handle'] = hnd
                    if 'mode' in args and args['mode'] == 'create':
                        args['mode'] = 'enable'
                    result = rt_handle.invoke('emulation_ipv6_autoconfig', **args)
                    if result.get('handle'):
                        global_config[string].extend(result['handle'])
                        result['handles'] = string
                    if args['mode'] == 'enable':
                        handle_map[hnd] = handle_map.get(hnd, [])
                        handle_map[hnd].extend(global_config[string])
                        handle_map[string] = hnd
                    ret.append(result)
            else:
                args['handle'] = hndl
                args['mode'] = 'enable' if args['mode'] == 'create' else args['mode']
                result = rt_handle.invoke('emulation_ipv6_autoconfig', **args)
                if result.get('handle'):
                    global_config[string].extend(result['handle'])
                    result['handles'] = string
                if args['mode'] == 'enable':
                    handle_map[hndl] = handle_map.get(hndl, [])
                    handle_map[hndl].extend(global_config[string])
                    handle_map[string] = hndl
                ret.append(result)
    elif port_handle != jNone:
        if not isinstance(port_handle, list):
            port_handle = [port_handle]
        port_handle = list(set(port_handle))
        result = rt_handle.invoke('emulation_ipv6_autoconfig', **args)
        if result.get('handle'):
            global_config[string].extend([result['handle']])
            result['handles'] = string
        for hand in port_handle:
            handle_map[hand] = handle_map.get(hand, [])
            handle_map[hand].extend(global_config[string])
            handle_map[string] = hand
        ret.append(result)

        if not isinstance(result['handle'], list):
            handle = [result['handle']]
        for hndl1 in handle:
            ipv4_handle = rt_handle.invoke('invoke', cmd='stc::get '+hndl1+' -children-ipv4if')
            if ipv4_handle.startswith('ipv4'):
                ipv4_addr = rt_handle.invoke('invoke', cmd='stc::get '+ipv4_handle+' -Address')
                handle_map['ipv6_autoconfig_ipaddr'] = handle_map.get('ipv6_autoconfig_ipaddr', {})
                handle_map['ipv6_autoconfig_ipaddr'][hndl1] = ipv4_addr

    # ***** Return Value Modification *****
    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ipv6_autoconfig_control(
        rt_handle,
        action=jNone,
        port_handle=jNone,
        handle=jNone):
    """
    :param rt_handle:       RT object
    :param action - <start|stop>
    :param port_handle
    :param handle
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    args = dict()
    args['action'] = action
    args['port_handle'] = port_handle
    args['handle'] = handle
 
    args = get_arg_value(rt_handle, j_emulation_ipv6_autoconfig_control.__doc__, **args)

    if "port_handle" not in args.keys():
        __check_and_raise(handle)
    else:
        __check_and_raise(port_handle)
        try:
            handle_map[port_handle]
        except KeyError:
            handle_map[port_handle] = []

    if not isinstance(handle, list):
        handle = [handle]
    handle = list(set(handle))
    ret = []
    if 'handle' in args:
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    args['handle'] = hnd
                    ret.append(rt_handle.invoke('emulation_ipv6_autoconfig_control', **args))
            else:
                args['handle'] = hndl
                ret.append(rt_handle.invoke('emulation_ipv6_autoconfig_control', **args))

    elif 'port_handle' in args:
        ret.append(rt_handle.invoke('emulation_ipv6_autoconfig_control', **args))

     # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret

def j_emulation_ipv6_autoconfig_stats(
        rt_handle,
        action=jNone,
        handle=jNone,
        mode=jNone,
        port_handle=jNone):
    """
    :param rt_handle:       RT object
    :param action
    :param handle
    :param mode
    :param port_handle
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****
    args = dict()
    args['action'] = action
    args['handle'] = handle
    args['mode'] = mode
    args['port_handle'] = port_handle
    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    if "port_handle" not in args.keys():
        __check_and_raise(handle)
    else:
        __check_and_raise(port_handle)
    try:
        handle_map[port_handle]
    except KeyError:
        handle_map[port_handle] = []

    ret = []
    if port_handle != jNone:
        ret.append(rt_handle.invoke('emulation_ipv6_autoconfig_stats', **args))
    elif handle != jNone:
        if not isinstance(handle, list):
            handle = [handle]
            handle = list(set(handle))
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    args['handle'] = hnd
                    stats = dict()
                    stats.update(rt_handle.invoke('emulation_ipv6_autoconfig_stats', **args))
                    ret.append(stats)
            else:
                args['handle'] = hndl
                stats = dict()
                stats.update(rt_handle.invoke('emulation_ipv6_autoconfig_stats', **args))
                ret.append(stats)
    # ***** Return Value Modification *****
    port_list = []
    if port_handle != jNone:
        port_list = [port_handle]
    elif handle != jNone:
        for hndl in handle:
            if hndl in global_config.keys():
                for hnd in global_config[hndl]:
                    port_hand = __get_handle(hnd)
                    port_list.append(port_hand)
            else:
                port_hand = __get_handle(hndl)
                port_list.append(port_hand)
    index = 0
    for index in range(len(ret)):
        for port in port_list:
            if port in ret[index]:
                if 'tx_rtr_sol' in ret[index][port]:
                    ret[index]['Router Solicits Tx'] = ret[index][port].get('tx_rtr_sol')
                if 'rx_rtr_adv' in ret[index][port]:
                    ret[index]['Router Advertisements Rx'] = ret[index][port].get('rx_rtr_adv')
                if 'tx_nbr_sol' in ret[index][port]:
                    ret[index]['Neighbor Solicits Tx'] = ret[index][port].get('tx_nbr_sol')
                if 'rx_nbr_adv' in ret[index][port]:
                    ret[index]['Neighbor Advertisements Rx'] = ret[index][port].get('rx_nbr_adv')

    if 'ipv6_autoconfig_ipaddr' in handle_map:
        for port in port_list:
            handles = __get_handle(port)
            for hndl in handle:
                if hndl in global_config.keys():
                    for hnd in global_config[hndl]:
                        for index in range(len(ret)):
                            ret[index]['session'] = ret[index].get('session', {})
                            ret[index]['session']['session_ip'] = ret[index]['session'].get('session_ip', {})
                            ret[index]['session']['session_ip'][hnd] = handle_map['ipv6_autoconfig_ipaddr'][hnd]
                else:
                    for index in range(len(ret)):
                        ret[index]['session'] = ret[index].get('session', {})
                        ret[index]['session']['session_ip'] = ret[index]['session'].get('session_ip', {})
                        ret[index]['session']['session_ip'][hndl] = handle_map['ipv6_autoconfig_ipaddr'][hndl]

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_interface_control(
        rt_handle,
        port_handle=jNone,
        mode=jNone):
    """
    :param rt_handle:       RT object
    :param port_handle
    :param mode - <break_link|restore_link>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['mode'] = mode

    args = get_arg_value(rt_handle, j_interface_control.__doc__, **args)

    __check_and_raise(port_handle)

    ret = []
    ret.append(rt_handle.invoke('interface_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_save_config(
        rt_handle,
        filename=jNone):
    """
    :param rt_handle   RT object
    :param filename

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    filename, ext = os.path.splitext(filename)
    args['filename'] = filename + '.xml'

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(filename)

    ret = []
    ret.append(rt_handle.invoke('save_xml', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_packet_config_buffers(
        rt_handle,
        port_handle=jNone,
        action=jNone,
        data_plane_capture_enable=jNone,
        control_plane_capture_enable=jNone):
    """
    :param rt_handle   RT object
    :param port_handle
    :param action - <wrap|stop>
    :param data_plane_capture_enable
    :param control_plane_capture_enable

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['action'] = action

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    args = get_arg_value(rt_handle, j_packet_config_buffers.__doc__, **args)

    __check_and_raise(port_handle)
    __check_and_raise(action)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    port_handle = list(set(port_handle))

    ret = []
    for hndl in port_handle:
        args['port_handle'] = hndl
        ret.append(rt_handle.invoke('packet_config_buffers', **args))

####Native code###
    if data_plane_capture_enable != jNone:
        for port_item in port_handle:
            pac_capture = rt_handle.invoke('invoke', cmd='stc::get '+port_item+' -children-capture')
            if data_plane_capture_enable == '1':
                rt_handle.invoke('invoke', cmd='stc::config '+pac_capture+' -RealTimeMode REALTIME_ENABLE')
            elif data_plane_capture_enable == '0':
                rt_handle.invoke('invoke', cmd='stc::config '+pac_capture+' -RealTimeMode REALTIME_DISABLE')
    if control_plane_capture_enable != jNone:
        for port_item in port_handle:
            pac_capture = rt_handle.invoke('invoke', cmd='stc::get '+port_item+' -children-capture')
            if control_plane_capture_enable == '1':
                rt_handle.invoke('invoke', cmd='stc::config '+pac_capture+' -RealTimeMode REALTIME_ENABLE')
            elif control_plane_capture_enable == '0':
                rt_handle.invoke('invoke', cmd='stc::config '+pac_capture+' -RealTimeMode REALTIME_DISABLE')

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_packet_config_filter(
        rt_handle,
        port_handle=jNone,
        filter=jNone):
    """
    :param rt_handle   RT object
    :param port_handle
    :param filter

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['mode'] = 'add'
    args['filter'] = filter

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(port_handle)
    __check_and_raise(filter)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    port_handle = list(set(port_handle))

    ret = []
    for hndl in port_handle:
        args['port_handle'] = hndl
        ret.append(rt_handle.invoke('packet_config_filter', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_packet_config_triggers(
        rt_handle,
        port_handle=jNone,
        trigger=jNone):
    """
    :param rt_handle   RT object
    :param port_handle
    :param trigger

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['mode'] = 'add'
    args['trigger'] = trigger
    args['exec'] = 'start'

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]

    __check_and_raise(port_handle)
    __check_and_raise(trigger)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    port_handle = list(set(port_handle))

    ret = []
    for hndl in port_handle:
        args['port_handle'] = hndl
        ret.append(rt_handle.invoke('packet_config_triggers', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_packet_control(
        rt_handle,
        port_handle=jNone,
        action=jNone):
    """
    :param rt_handle   RT object
    :param port_handle
    :param action - <start|stop>

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['action'] = action

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
  
    args = get_arg_value(rt_handle, j_packet_control.__doc__, **args)

    __check_and_raise(port_handle)
    __check_and_raise(action)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    port_handle = list(set(port_handle))

    ret = []
    for hndl in port_handle:
        args['port_handle'] = hndl
        ret.append(rt_handle.invoke('packet_control', **args))

    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_packet_stats(
        rt_handle,
        port_handle=jNone,
        stop=jNone,
        format=jNone,
        filename=jNone,
        var_num_frames=jNone):
    """
    :param rt_handle   RT object
    :param port_handle
    :param stop
    :param format
    :param filename
    :param var_num_frames

    Spirent Returns:
    {
        "status": "1"
    }

    IXIA Returns:
    {
        "status": "1"
    }

    Common Return Keys:
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['port_handle'] = port_handle
    args['stop'] = stop
    if format == 'pcap' or format == 'cap' or format == 'txt':
        args['format'] = 'pcap'
    elif format == 'var':
        args['format'] = 'var'
        if var_num_frames != jNone:
            args['var_num_frames'] = var_num_frames

    else:
        raise ValueError("Supported capture formats - pcap | cap | txt | var")
    args['filename'] = filename

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****

    __check_and_raise(port_handle)
    if not isinstance(port_handle, list):
        port_handle = [port_handle]
    port_handle = list(set(port_handle))

    if filename == jNone:
        filename = list()
    if isinstance(filename, str):
        filename = [filename]

    if len(port_handle) > len(filename):
        file_len = len(filename)
        for index in range(file_len, len(port_handle)):
            filename.append(port_handle[index])

    for index, file_name in enumerate(filename):
        if "/" in file_name:
            filename[index] = re.sub(r'(.*)(\.pcap|\.cap|\.txt)$', r'\1', file_name)
        else:
            filename[index] = os.path.join(rt_handle.device_logger.log_dir(),
                                           re.sub(r'(.*)(\.pcap|\.cap|\.txt)$', r'\1', file_name))
    for key in list(args.keys()):
        if args[key] == jNone:
            del args[key]
    if format == 'txt':
        if shutil.which("tshark") == None:
            raise FileNotFoundError("Please install tshark")

    ret = []
    for ind, hndl in enumerate(port_handle):
        args['port_handle'] = hndl
        args['filename'] = filename[ind] + '.pcap'
        ret.append(rt_handle.invoke('packet_stats', **args))
        if format == 'var':
            continue
        if format == 'txt':
            os.system("tshark -r " + filename[ind] + '.pcap' + " > " + filename[ind] + '.txt')
        ret[ind]['capture_file'] = filename[ind] + '.' + args['format']



    # ***** Return Value Modification *****

    if len(ret) == 1:
        ret = ret[0]

    # ***** End of Return Value Modification *****

    return ret


def j_session_info(
        rt_handle,
        mode='get_traffic_items'):
    """
    :param rt_handle   RT object
    :param mode - <get_traffic_items>

    Spirent Returns:
    {
        "traffic_streams": [ ]
        "status": "1"
    }

    IXIA Returns:
    {
        "traffic_streams": [ ]
        "status": "1"
    }

    Common Return Keys:
        "traffic_streams"
        "status"
    """
    # ***** Following is user's custom code *****
    #
    #
    # ***** End of user's custom code *****

    args = dict()
    args['mode'] = mode

    # ***** Argument Modification *****

    # ***** End of Argument Modification *****
    
    args = get_arg_value(rt_handle, j_session_info.__doc__, **args)

    output = []
    ret = dict()

    port_lists = rt_handle.invoke('invoke', cmd='stc::get' + " " + 'project1 -children-port').split(" ")
    for port_element in port_lists:
        stream_lists = rt_handle.invoke('invoke', cmd='stc::get' + " " + port_element + ' -children-streamblock').split(" ")
        for stream_element in stream_lists:
            stream_name = rt_handle.invoke('invoke', cmd='stc::get' + " " +  stream_element + ' -name')
            output.append(stream_name)
            ret['traffic_streams'] = output
            ret['status'] = '1'
    return ret



def __check_and_raise(arg):
    if (arg == jNone):
        stack = traceback.extract_stack()
        filename, lineno, function, code = stack[-2]
        orig_arg = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
        raise KeyError(
            "Please provide '" +
            orig_arg +
            "' argument to " +
            function +
            "() call")


def __get_handle(handle):
    if handle in handle_map:
        return handle_map[handle]


def __process_mld_info(rt_handle, **args):

    stats = dict()
    stats.update(rt_handle.invoke('emulation_mld_info', **args))
    stat2 = {}

    if not re.search('\s', args['handle']):
        return stats
    else:
        length = len(args['handle'].split(" "))
        for key in stats:
            if not isinstance(stats[key], dict):
                stat2[key] = stats[key]
                continue
            if key == "group_membership_stats":
                stat2[key] = stats[key]
                continue
            if key == "session":
                temp = __process_dict_of_dict(stats[key], length)
                stat2[key] = temp
    return stat2


def __process_dict_of_dict(stats, length):
    stat2 = {}
    for key in stats:
        for key1 in stats[key]:
            if key1 in stat2:
                try:
                    stats[key][key1] = int(stats[key][key1])
                    stat2[key1] = stat2[key1] + stats[key][key1]
                except ValueError:
                    stats[key][key1] = stats[key][key1]
                    stat2[key1] = stat2[key1] + " " +  stats[key][key1]
            else:
                try:
                    stat2[key1] = int(stats[key][key1])
                except ValueError:
                    stat2[key1] = stats[key][key1]

    #To get Average of LAtency
    for key in stat2:
        stat2[key] = stat2[key] // length

    return stat2

def incrementIpV4Address(ipToIncrement, ipIncrementValue="0.0.0.1"):
    ipList = ipToIncrement.split(".")
    incrVals = ipIncrementValue.split(".")
    o4 = int(ipList[3]) + int(incrVals[3])
    o3 = int(ipList[2]) + int(incrVals[2])
    o2 = int(ipList[1]) + int(incrVals[1])
    o1 = int(ipList[0]) + int(incrVals[0])

    ipaddr = str(o1) + "." +  str(o2) + "." + str(o3) + "." + str(o4)
    return ipaddr


