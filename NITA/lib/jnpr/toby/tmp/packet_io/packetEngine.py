#!/usr/bin/python3
import os
import yaml
import copy
import re
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from scapy.packet import *
from scapy.fields import *
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6, IP6Field
from struct import pack
from struct import unpack
from scapy.all import IP, TCP, RandIP, send, conf, get_if_list
from collections import defaultdict
import socket
import sys
import time
import warnings
import sys
import pdb
import threading
import inspect
import re
import string
import base64
import codecs
import binascii


pkt_data={}
count=0
results = []
p = re.compile('packet[1-9]+')
pkt_user_data={}
def store_all_nodes(data):
    
    if isinstance(data, dict):
        for k, item in data.items():
            if p.match(k):
                pkt_user_data[k]=item
            store_all_nodes(item)
    elif isinstance(data, list) or isinstance(data, tuple):
        for item in data:
             store_all_nodes(item)
    return pkt_user_data

def isMAC48Address(inputString):
    if inputString.count(":")!=5:
         return False
    if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", inputString.lower()):
          return 1
    else:
          return 0

def rand_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
    random.randint(0, 0),
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255)
    )

def rand_ip():
    ip = "192.168."
    ip += ".".join(map(str, (random.randint(0, 255)
    for _ in range(2))))
    return ip

class PacketEngine(object):

    def __init__(self):
        pkt_data={}

    @classmethod
    def ExtractPacketDetails(self,data):
        #store_all_nodes(self.pkt_data)
        if isinstance(data, dict):
            for k, item in data.items():
                if p.match(k):
                    pkt_user_data[k]=item
                store_all_nodes(item)
        elif isinstance(data, list) or isinstance(data, tuple):
            for item in data:
                 store_all_nodes(item)

        print (pkt_user_data)
        return pkt_user_data

    @classmethod
    def validateYamlPacketUserData(self,p_data):

        i=1
        for key,data in p_data.items():

            header_type= 'header_type' + str(i)
            if p_data[key] is None or p_data[key][header_type] is None or  p_data[key][header_type]['type'] is None\
            or p_data[key]['packet_interfaces'] is None or p_data[key]['packet_interfaces']['rx_int'] is None \
            or p_data[key]['packet_interfaces']['tx_int'] is None:
                raise Exception('No Valid Input is Present')
            i+=1

    @classmethod
    def get_layers_packet(self, **kwargs):
        set_method = inspect.stack()[0][3]
        lpkt=kwargs.get('pkt',False)
        layers = []
        counter = 0
        while True:
            layer = lpkt.getlayer(counter)
            if (layer != None):
                print (layer.name)
                layers.append(layer.name)
            else:
                break
            counter += 1
        print ("Layers are:{0}\n".format(layers))
        return layers 

    @classmethod
    def get_packet_attrib_data(self,**kwargs):
        #print (kwargs) 
        if kwargs is not None:
            packet_hash=kwargs.get('packet_hash')
            packet_key=kwargs.get('packet')
            attrib_value=kwargs.get('attrib')
        else:
            raise AssertionError("please Pass the right Arguments")

        if attrib_value in packet_hash[packet_key]:
            if 'packet_loop_count' in attrib_value:
                if 'count' in packet_hash[packet_key][attrib_value]:
                    try:
                        value=packet_hash[packet_key][attrib_value]['count']
                    except NameError:
                        value=1
            elif 'description' in attrib_value:
                 value=packet_hash[packet_key][attrib_value]
            elif 'packet_interfaces' in attrib_value:
                 value=packet_hash[packet_key][attrib_value]
                 print (value)
            elif attrib_value in packet_hash[packet_key]:
                print (attrib_value)
                print (packet_key)
                value=packet_hash[packet_key][attrib_value]['type']

        return value


    @classmethod
    def create_packet(self,**kwargs):

        if kwargs is not None:
            packet_hash=kwargs.get('packet_hash')
            key=kwargs.get('packet')
        else:
            raise AssertionError("please Pass the right Arguments")

        hex_dump={}
        packet_stack={}
        
        for hkey in packet_hash[key].keys():
            print ("{0}   {1}\n".format(hkey,key))
            if 'header_type' in hkey:
                index = re.search('(\d+)',hkey)
                index=index.group(0)
                if packet_hash[key][hkey]['type'] == 'MAC':
                     print ("MAC---> {0}\n".format(index))
                     packet_stack[index]="Ether(dst='ff:ff:ff:ff:ff:ff')"
                elif packet_hash[key][hkey]['type'] == 'VLAN':
                     print ("VLAN---> {0}\n".format(index))
                     packet_stack[index]="Dot1Q(vlan=100)"
                elif packet_hash[key][hkey]['type'] == 'ARP':
                     print ("ARP---->{0}\n".format(index))
                     packet_stack[index]="ARP(hwsrc='00:11:22:aa:bb:cc',pdst='172.16.20.1')"
                elif packet_hash[key][hkey]['type'] == 'IP':
                     packet_stack[index]="IP()"
                elif packet_hash[key][hkey]['type'] == 'TCP':
                     packet_stack[index]="TCP(sport=333, dport=80,seq=111222)"
                elif packet_hash[key][hkey]['type'] == 'UDP':
                     packet_stack[index]="UDP(sport=444, dport=555, len=104, chksum=0)"


        le =  len(packet_stack)
        le+=1
        packet_stack_string=''
        print (le)
        print (packet_stack)

        for i in range(1, le):
            new_string=packet_stack[str(i)]+'/'
            packet_stack_string +=new_string

        packet_stack_string = packet_stack_string.rstrip('/')
        pkt=   eval(packet_stack_string)

        print (pkt.show()) 

        for stack in packet_stack.keys():
            #print (stack)
            #print (packet_hash[key])
            #h_key= 'header_fields' + stack
            h_key= 'header_type' + stack

            if 'Ether(' in packet_stack[stack]:
                if h_key:
                    if 'Ether.src' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['Ether.src'] is None:
                            raise Exception('No Valid Input is Present') 
                        #print ("ni  -->{0}\n" .format(packet_hash[key][h_key]['Ether.src']))
                        if isMAC48Address(packet_hash[key][h_key]['header_fields']['Ether.src']):
                            pkt[Ether].src = packet_hash[key][h_key]['header_fields']['Ether.src']
                            print ("ni  -->{0}\n" .format(packet_hash[key][h_key]['header_fields']['Ether.src']))
                    else:
                        pkt[Ether].src = rand_mac()
                    if 'Ether.dst' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['Ether.dst'] is None:
                            raise Exception('No Valid Input is Present') 
                        if isMAC48Address(packet_hash[key][h_key]['header_fields']['Ether.dst']):
                            pkt[Ether].dst = packet_hash[key][h_key]['header_fields']['Ether.dst']
                    else:
                        pkt[Ether].dst = rand_mac()
                    if 'Ether.type' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['Ether.type'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[Ether].type = packet_hash[key][h_key]['header_fields']['Ether.type']
                else:
                    pkt[Ether].src = rand_mac()
                    pkt[Ether].dst = rand_mac()
            elif 'Dot1Q' in packet_stack[stack]:
                if h_key:
                    if  'Dot1Q.vlan' in packet_hash[key][h_key]['header_fields']: 
                        if packet_hash[key][h_key]['header_fields']['Dot1Q.vlan'] is None:
                            raise Exception('No Valid Input is Present') 
                        print ("info--->{0}".format(packet_hash[key][h_key]['header_fields']['Dot1Q.vlan']))
                        pkt[Dot1Q].vlan = packet_hash[key][h_key]['header_fields']['Dot1Q.vlan']
                    if 'Dot1Q.prio' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['Dot1Q.prio'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[Dot1Q].prio = packet_hash[key][h_key]['header_fields']['Dot1Q.prio']
                    if 'Dot1Q.id' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['Dot1Q.id'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[Dot1Q].id = packet_hash[key][h_key]['header_fields']['Dot1Q.id']
                    if 'Dot1Q.type' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['Dot1Q.type'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[Dot1Q].type = packet_hash[key][h_key]['header_fields']['Dot1Q.type']
            elif 'ARP(' in packet_stack[stack]:
                if h_key:
                    if 'ARP.hwsrc' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['ARP.hwsrc'] is None:
                            raise Exception('No Valid Input is Present') 
                        if isMAC48Address(packet_hash[key][h_key]['header_fields']['ARP.hwsrc']):
                            pkt[ARP].hwsrc = packet_hash[key][h_key]['header_fields']['ARP.hwsrc']
                    else:
                        pkt[ARP].hwsrc = rand_mac()
                    if 'ARP.pdst' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['ARP.pdst'] is None:
                            raise Exception('No Valid Input is Present') 
                        if not socket.inet_aton(packet_hash[key][h_key]['header_fields']['ARP.pdst']):
                            raise Exception('address/netmask is invalid') 
                        print ("info1---> {0}\n".format(packet_hash[key][h_key]['header_fields']['ARP.pdst']))
                        pkt[ARP].pdst = packet_hash[key][h_key]['header_fields']['ARP.pdst']
                    else:
                        pkt[ARP].pdst = rand_ip() 
                else:
                    pkt[ARP].hwsrc = rand_mac()
                    pkt[ARP].pdst = rand_ip()
            elif 'IP(' in packet_stack[stack]:
                if h_key:
                    if 'IP.src' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.src'] is None:
                            raise Exception('No Valid Input is Present') 
                        if not socket.inet_aton(packet_hash[key][h_key]['header_fields']['IP.src']):
                            raise Exception('address/netmask is invalid')
                        pkt[IP].src= packet_hash[key][h_key]['header_fields']['IP.src']    
                    else:
                        pkt[IP].src = rand_ip()

                    if 'IP.dst' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.dst'] is None:
                            raise Exception('No Valid Input is Present') 
                        if not socket.inet_aton(packet_hash[key][h_key]['header_fields']['IP.dst']):
                            raise Exception('address/netmask is invalid') 
                        pkt[IP].dst = packet_hash[key][h_key]['header_fields']['IP.dst']
                    else:
                        pkt[IP].dst = rand_ip() 
                    if 'IP.version' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.version'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].version = packet_hash[key][h_key]['header_fields']['IP.version']
                    if 'IP.ihl' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.ihl'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].ihl = packet_hash[key][h_key]['header_fields']['IP.ihl']
                    if 'IP.tos' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.tos'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].tos = packet_hash[key][h_key]['header_fields']['IP.tos']
                    if 'IP.len' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.len'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].len = packet_hash[key][h_key]['header_fields']['IP.len']
                    if 'IP.id' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.id'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].id = packet_hash[key][h_key]['header_fields']['IP.id']
                    if 'IP.flags' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.flags'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].flags = packet_hash[key][h_key]['header_fields']['IP.flags']
                    if 'IP.frag' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.frag'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].frag = packet_hash[key][h_key]['header_fields']['IP.frag']
                    if 'IP.ttl' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.ttl'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].ttl = packet_hash[key][h_key]['header_fields']['IP.ttl']
                    if 'IP.proto' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.proto'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].proto = packet_hash[key][h_key]['header_fields']['IP.proto']
                    if 'IP.chksum' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['IP.chksum'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[IP].chksum = packet_hash[key][h_key]['header_fields']['IP.chksum']
                else:
                    pkt[IP].src = rand_ip()  
                    pkt[IP].dst = rand_ip()  
            elif 'TCP' in packet_stack[stack]:
                if h_key:
                    if 'TCP.sport' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['TCP.sport'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[TCP].sport= packet_hash[key][h_key]['header_fields']['TCP.sport']    
                    else:
                        pkt[TCP].sport = random.randint(1000,1500) 
                    if 'TCP.dport' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['TCP.dport'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[TCP].dport = packet_hash[key][h_key]['header_fields']['TCP.dport']
                    else:
                        pkt[TCP].dport = random.randint(1600,2000) 
                    if 'TCP.seq' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['TCP.seq'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[TCP].seq = packet_hash[key][h_key]['header_fields']['TCP.seq']
                    if 'TCP.ack' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['TCP.ack'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[TCP].ack = packet_hash[key][h_key]['header_fields']['TCP.ack']
                    if 'TCP.dataofs' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['TCP.dataofs'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[TCP].dataofs = packet_hash[key][h_key]['header_fields']['TCP.dataofs']
                    if 'TCP.reserved' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['TCP.reserved'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[TCP].reserved = packet_hash[key][h_key]['header_fields']['TCP.reserved']
                    if 'TCP.flags' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['TCP.flags'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[TCP].flags = packet_hash[key][h_key]['header_fields']['TCP.flags']
                    if 'TCP.window' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['TCP.window'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[TCP].window = packet_hash[key][h_key]['header_fields']['TCP.window']
                    if 'TCP.urgptr' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['TCP.urgptr'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[TCP].urgptr = packet_hash[key][h_key]['header_fields']['TCP.urgptr']
                    if 'TCP.options' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['TCP.options']['header_fields'] is None:
                            raise Exception('No Valid Input is Present')
                        if '{' not in packet_hash[key][h_key]['header_fields']['TCP.options'] and '}' not in packet_hash[key][h_key]['header_fields']['TCP.options']:
                            raise Exception('Value should be with in {}')
                        pkt[TCP].options = packet_hash[key][h_key]['header_fields']['TCP.options']
                else:
                    pkt[TCP].sport = random.randint(1000,1500) 
                    pkt[TCP].dport = random.randint(1600,2000)
            elif 'UDP(' in packet_stack[stack]:
                if h_key:
                    if 'UDP.sport' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['UDP.sport'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[UDP].sport= packet_hash[key][h_key]['header_fields']['UDP.sport']    
                    else:
                        pkt[UDP].sport = random.randint(1000,1500) 
                    if 'UDP.dport' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['UDP.dport'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[UDP].dport = packet_hash[key][h_key]['header_fields']['UDP.dport']
                    else:
                        pkt[UDP].dport = random.randint(1600,2000) 
                    if 'UDP.chksum' in packet_hash[key][h_key]['header_fields']:
                        if packet_hash[key][h_key]['header_fields']['UDP.chksum'] is None:
                            raise Exception('No Valid Input is Present') 
                        pkt[UDP].chksum = packet_hash[key][h_key]['header_fields']['UDP.chksum']
                else:
                    pkt[UDP].sport = random.randint(1000,1500) 
                    pkt[UDP].dport = random.randint(1600,2000)
        #print (pkt)
        print (pkt.show())
        return pkt

        #send_packet_layers=self.get_layers_packet(lpkt=arppkt)
        #        for layer in send_packet_layers:
        #            print (layer)

    @classmethod
    def packet_show_command(self,packet):
        display=packet.show()
        return display


    @classmethod
    def packetHexDump(self,pkt):

        send_packet_hex=binascii.hexlify(bytes(pkt))
        send_packet_hex=send_packet_hex.decode("utf-8")
        return send_packet_hex

    @classmethod
    def packet_init(self,fname):
        pkt_user_data={}
        pkt_user_data=self.ParseTemplateYaml(yaml_file=fname,yaml_type='create')
        return pkt_user_data

    @classmethod
    def verify_packet_init(self,fname):

        verify_pkt_data={}
        verify_pkt_data=self.ParseTemplateYaml(yaml_file=fname,yaml_type='verify')

        return verify_pkt_data


    @classmethod
    def ParseTemplateYaml(self,**kwargs): 

        if kwargs is not None:
            fname=kwargs.get('yaml_file',False)
            yaml_type=kwargs.get('yaml_type',False)
        else:
            raise AssertionError("please Pass the right Arguments")

        ret_data={}
        verify_hash={}

        with open(fname, 'r') as stream:
            try:
                self.pkt_data= yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        pkt_user_data=self.ExtractPacketDetails(self.pkt_data)
        template_temp_data={}
        t_data={}
        t1_data={}
        new_pkt_user_data = defaultdict(dict)
        for key,data in pkt_user_data.items():
            t1_data={}
            if 'create' in yaml_type:
                new_pkt_user_data[key]['packet_interfaces']=pkt_user_data[key]['packet_interfaces']
                new_pkt_user_data[key]['packet_loop_count']=pkt_user_data[key]['packet_loop_count']
                new_pkt_user_data[key]['description']=pkt_user_data[key]['description']
            if 'TEMPLATE' in data:
                template_temp_data=self.get_template_details(template_info=pkt_user_data[key]['TEMPLATE'])
                with open(template_temp_data['fname'], 'r') as stream:
                    try:
                        template_data= yaml.load(stream)
                        if 'templ_args' in template_temp_data:
                            if ',' in  template_temp_data['templ_args']:
                                temp_header_args=template_temp_data['templ_args'].split(',')
                                for h_type in temp_header_args:
                                    t_data[h_type]=template_data[h_type]
                                    new_pkt_user_data[key][h_type]=template_data[h_type]
                            else:
                                temp_header_args=template_temp_data['templ_args']
                                h_type= temp_header_args
                                t_data[h_type]=template_data[h_type]
                                new_pkt_user_data[key][h_type]=template_data[h_type]
                        else:
                            for k,v in template_data.items():
                                new_pkt_user_data[key][k]=v
                    except yaml.YAMLError as exc:
                        print(exc)
                if 'verify' in yaml_type:
                    if pkt_user_data[key]['packet_fields'] == 'all':
                        verify_pk_data=self.ddict2dict(new_pkt_user_data)
                        pk=self.create_packet(packet_hash=new_pkt_user_data,packet=key)
                        p_hex=pe.packetHexDump(pk)
                        verify_hash[key]=p_hex
        new_pkt_user_data=self.ddict2dict(new_pkt_user_data)
        if 'create' in yaml_type:
            pkt_user_data=new_pkt_user_data.copy()
            self.validateYamlPacketUserData(pkt_user_data)
        elif 'verify' in yaml_type:
            pkt_user_data=verify_hash

        return pkt_user_data

    @classmethod
    def ddict(self):
        return defaultdict(ddict)

    @classmethod
    def ddict2dict(self,d):
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = self.ddict2dict(v)
        return dict(d)



    @classmethod
    def get_template_details(self,**kwargs):

        ret_data={}
        if kwargs is not None:
            template_info=kwargs.get('template_info',False)
        else:
            raise AssertionError("please Pass the right Arguments")
        if '(' not in template_info and '.yaml' in template_info:
            ret_data['fname']=template_info
        elif '(' in template_info and ')' in template_info and '.yaml' in template_info:
            split_string=template_info.split('(')
            for x in split_string:
                if '.yaml' in x:
                    ret_data['fname']=x
                elif ')' in x  and 'header_type' in x:
                    template_args= x.replace(')','')
                    ret_data['templ_args']=template_args

        return ret_data




    @classmethod
    def get_packet_io_receive_data(self,**kwargs):
    
        if kwargs is not None:
            output=kwargs.get('dump',False)
            packet_length=kwargs.get('packet_length',False)
        else:
            raise AssertionError("please Pass the right Arguments")

        out_data=output.split('\n')
        rec_hash={}
        he_flag=1
        pk_flag=1
        temp_x=[]
        p_data=[]
        header_hex=''
        packet_hex=''
        for x in out_data:
            x.strip('\n')
            #print (x)
            if 'Packet Interface' in x:
                m = re.search(':\s+(...)',x)
                rec_int=m.group(0).strip(': ')
                rec_hash['receive_interface']=rec_int
            elif 'Pkt Len:' in x:
                m = re.search(':\s+(\d+)',x)
                rec_length=m.group(0).strip(': ')
                rec_hash['pkt_len']= int(rec_length)
            elif re.match('^[a-z0-9][a-z0-9]:+',x):
                #print ("-->{0}".format(x))
                 
                x = x.replace('\s+','')
                if ':' in x[-1]:
                    x=x[:-1]
                    print ("jumm->{0}\n".format(x))
                temp_x=x.split(':')
                #print (len(temp_x[-1]))
                #if len(temp_x[-1])==0:
                #    del temp_x[-1]
                #print (temp_x)
                #print ("mohan-->{0}".format(len(temp_x[-1])))
                if temp_x[-1] == '0':
                    print ("Before-->{0}".format(temp_x[-1]))
                    temp_x[-1] = temp_x[-1] + '0'
                    print ("Mohan-->{0}".format(temp_x[-1]))
                elif len(temp_x[-1]) == 1 and temp_x[-1] > '0' and temp_x[-1] < '10':
                    temp_x[-1] = '0' + temp_x[-1]

                for y in temp_x:
                    p_data.append(y)
        for i in range(len(p_data)):
            packet_hex+=p_data[i]
        print (packet_hex)
        print (rec_length)
        print (rec_int)
        if '\r' in packet_hex:
            packet_hex = packet_hex.replace('\r','')
        rec_hash['packet_hex']=  packet_hex

        return  rec_hash
                
pe=PacketEngine()
packet_data=pe.packet_init("packet.yaml")
print (packet_data)
pk=pe.create_packet(packet_hash=packet_data,packet='packet2')
print (pk.show())
p_hex=pe.packetHexDump(pk)
print (p_hex)
p_hash=pe.verify_packet_init("verify_packet.yaml")
#print (p_hash)
#print (p_hash['packet2'])
for k,d in p_hash.items():
    print ("mohan")
    print ("key-->{0}   value--->{1}\n".format(k,d))

#dump="""Packet Interface: fp0 
#Packet packet-type: ethernet 
#Packet interface: 20 
#Pkt Len: 38
#ff:ff:ff:ff:ff:ff:00:00:00:00:00:00:81:00:00:0a:
#08:00:45:00:00:14:00:01:00:00:40:00:fa:c5:ac:10:
#14:02:ac:10:14:1"""

#res={}
#res=pe.get_packet_io_receive_data(dump=dump, packet_length=38)

#print (res)
#pk=pe.create_packet(packet_hash=packet_data,packet='packet2')
#print (pk)
#p_hex=pe.packetHexDump(pk)
#print (p_hex)

#packetData=PacketEngine("packet.yaml")
#print_all_leaf_node(self.pkt_data)
#packetData.ExtractPacketDetails()
#packetData.validateYamlPacketUserData(pkt_user_data)
#hex_dump={}
#p_data=self.packet_io_test_init("packet.yaml")
#hex_dump=packetData.packetHexdump(pkt_user_data)
#hex_dump=packetData.packetHexdump(p_data)

#for k,d in hex_dump.items():
#    print ("key-->{0}   value--->{1}\n".format(k,d))



