#!/usr/bin/python3

"""
Copyright (C) 2015-2016, Juniper Networks, Inc.
All rights reserved.
Author: Mohan Kumar M.V
Description:  This module is used to craft the network packet using
using Scapy.
Date: 09/27/2018
"""

from collections import OrderedDict
import binascii
import os
import re
import logging
import yaml
import yaml.constructor
from scapy.all import *
#from scapy.packet import *
#from scapy.fields import *
#from scapy.layers.inet import IP
#from scapy.layers.inet6 import IPv6, IP6Field
#from scapy.all import IP, TCP, RandIP, send, conf, get_if_list
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

class OrderedDictYAMLLoader(yaml.Loader):
    '''
    A YAML loader that loads mappings into ordered dictionaries.
    '''
    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)
        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        """
        API for Initilizing the Order dictionary
        :param node:
            **REQUIRED**   Head Pointer of yaml data
        :return:
            None
        """
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        """
        Mapping the yaml content in to dictionary in order
        :param node:
            **REQUIRED**  Head Pointer of yaml data
        :return:
            Yaml structure with ordererd dictionary
        """
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,\
            'expected a mapping node, but found %s' % node.id, node.start_mark)

        mapping = OrderedDict()

        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping', \
            node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

class ScapyPacket(object):
    """
    Class for Creating the Scapy packet
    """
    def __init__(self):
        self.send_packet_hex = None
        self.verify_packet_hex = {}
        self.raw_send_packet = {}
        self.raw_verify_packet = {}
        self.pkt_data = {}

        self.pkt_user_data = {}
        self.pkt_template_data = {}
        self.pkt_template_defination_data = {}
    def store_all_nodes(self, data, extract_type):
        """
        Function to store yaml data from dictionary based on user yaml
        file for packet send and packet verify.
        :param data:
            **REQUIRED**   data from yaml file.
        :param extract_type:
            **REQUIRED**  Extract type from yaml for create and verify.
        :return:
            returns the data of yaml in dictionary
        """
        pattern1 = re.compile('packet[1-9]+')
        pattern2 = re.compile('USE_TEMPLATE')
        if isinstance(data, dict):
            for key, item in data.items():
                if pattern1.match(key) and ('PKT_SEND' or 'PKT_VERIFY') in extract_type:
                    self.pkt_user_data[key] = item
                elif pattern2.match(key) and ('PKT_SEND' or 'PKT_VERIFY') in extract_type:
                    self.pkt_template_data[key] = item
                elif 'PKT_TMPLATE' in extract_type:
                    self.pkt_template_defination_data[key] = item
                self.store_all_nodes(item, extract_type)
        elif isinstance(data, (list, tuple)):
            for item in data:
                self.store_all_nodes(item, extract_type)
        if 'PKT_SEND' in extract_type:
            return (self.pkt_user_data, self.pkt_template_data)
        elif 'PKT_TMPLATE' in extract_type:
            return self.pkt_template_defination_data

    def extract_packet_details(self, data, extract_type):
        """
        Function to extract yaml data to dictionary based on user yaml
        file for packet send and packet verify.

        :param data:
            **REQUIRED**   data from yaml file.
        :param extract_type:
            **REQUIRED**  Extract type from yaml for create and verify.

        :return:
            returns the data of yaml in dictionary
        """
        pattern1 = re.compile('packet[1-9]+')
        pattern2 = re.compile('USE_TEMPLATE')
        if isinstance(data, dict):
            for key, item in data.items():
                if pattern1.match(key) and ('PKT_SEND' or 'PKT_VERIFY') in extract_type:
                    self.pkt_user_data[key] = item
                elif pattern2.match(key) and ('PKT_SEND' or 'PKT_VERIFY') in extract_type:
                    self.pkt_template_data[key] = item
                elif 'PKT_TMPLATE' in extract_type:
                    self.pkt_template_defination_data[key] = item
                self.store_all_nodes(item, extract_type)
        elif isinstance(data, (list, tuple)):
            for item in data:
                self.store_all_nodes(item, extract_type)
        if 'PKT_SEND' or 'PKT_VERIFY' in extract_type:
            return (self.pkt_user_data, self.pkt_template_data)
        elif 'PKT_TMPLATE' in extract_type:
            return self.pkt_template_defination_data

    def create_and_get_hex_dump_packet_for_send(self, **kwargs):
        """
        Robot Usage Example :
        ${hex_dump} =      Create And Get Hex Dump Packet For Send     packet=packet1
        Function to generate the hex dump of the packet of send packet
        :param packet:
            **REQUIRED**  packet index ,Example packet1, packet2
        :return:
            returns the hexdump of the packet
        """

        if kwargs is not None:
            key = kwargs.get('packet')
        else:
            raise AssertionError("please Pass the right Arguments")
        if key in self.raw_send_packet:
            packet_string = self.raw_send_packet[key]
            pkt = eval(packet_string)
            packet_hex = self.packet_hex_dump(pkt)
        else:
            raise AssertionError("Invalid Packet Index")

        return packet_hex

    def create_and_get_hex_dump_packet_for_verify(self, **kwargs):
        """
        Robot Usage Example :
        ${hex_dump} =      Create And Get Hex Dump Packet For Verify     packet=packet1
        Function to generate the hex dump of the packet of verify packet
        :param packet:
            **REQUIRED**  packet index ,Example packet1, packet2
        :return:
            returns the hexdump of the packet
        """

        if kwargs is not None:
            key = kwargs.get('packet')
        else:
            raise AssertionError("please Pass the right Arguments")
        if key in self.raw_verify_packet:
            packet_string = self.raw_verify_packet[key]
            pkt = eval(packet_string)
            packet_hex = self.packet_hex_dump(pkt)
        else:
            raise AssertionError("Invalid Packet Index")

        return packet_hex

    def packet_show_command(self, **kwargs):
        """
        Robot Usage Example :
        Packet Show Command       packet=packet1   packet_mode=Send
        Packet Show Command       packet=packet1   packet_mode=Verify
        Function wrapper for Scapy built in function to display packet content
        :param packet:
            **REQUIRED**  packet index ,Example packet1, packet2
        :param packet_mode:
            **REQUIRED**   packet mode to be Send/Verify
        :return:
            None
        """
        if kwargs is not None:
            key = kwargs.get('packet')
            request_type = kwargs.get('packet_mode')
        else:
            raise AssertionError("please Pass the right Arguments")
        if request_type == 'Send':
            if key in self.raw_send_packet:
                packet_string = self.raw_send_packet[key]
            else:
                raise AssertionError("Invalid Packet Index")
        elif request_type == 'Verify':
            if key in self.raw_verify_packet:
                packet_string = self.raw_verify_packet[key]
            else:
                raise AssertionError("Invalid Packet Index")
        pkt = eval(packet_string)
        pkt.show()
        return True


    def packet_hex_dump(self, pkt):
        """
        Function to generate the packet in hex dump
        :param pkt:
            **MANDATORY**  packet pointer
        :return:
            returns the hex dump of the packet
        """
        self.send_packet_hex = binascii.hexlify(bytes(pkt))
        self.send_packet_hex = self.send_packet_hex.decode("utf-8")
        return self.send_packet_hex

    def packet_init(self, fname):
        """
        Robot Usage Example :
        Packet Init    packet.yaml
        Function to Init the yaml file for packet creation
        :param: fname
            ** MANDATORY **   yaml file name
        :return:
            return True
        """
        if os.path.exists(fname):
            self.parse_template_yaml(yaml_file=fname, yaml_type='create')
        else:
            raise AssertionError("File doesn't exists")
        return True

    def verify_packet_init(self, fname):
        """
        Robot Usage Example :
        Verify Packet Init    verify_packet.yaml
        Function to Init the yaml file for packet verification
        :param: fname
            ** MANDATORY **   yaml file name
        :return:
            return True
        """
        if os.path.exists(fname):
            self.parse_template_yaml(yaml_file=fname, yaml_type='verify')
        else:
            raise AssertionError("File doesn't exists")
        return True


    def parse_template_yaml(self, **kwargs):
        """
        Function to Parse the Template yaml
        :param: yaml_file
            ** MANDATORY **   yaml file
        :param: yaml_type
            ** MANDATORY **    yaml type is create/verify
        :return:
            None
        """

        if kwargs is not None:
            fname = kwargs.get('yaml_file', False)
            yaml_type = kwargs.get('yaml_type', False)
        else:
            raise AssertionError("please Pass the right Arguments")
        user_input_type = ""
        with open(fname, 'r') as stream:
            try:
                self.pkt_data = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        if 'create' in yaml_type:
            user_input_type = "PKT_SEND"
        elif 'verify' in yaml_type:
            user_input_type = "PKT_VERIFY"
        (pkt_user_data, pkt_template_data) = \
                self.extract_packet_details(self.pkt_data, user_input_type)
        template_dict = {}
        if 'USE_TEMPLATE' in pkt_template_data:
            template_files = pkt_template_data['USE_TEMPLATE']

            for template_yaml_file in template_files:
                with open(template_yaml_file, 'r') as stream:
                    try:
                        self.pkt_data = yaml.load(stream, OrderedDictYAMLLoader)
                    except yaml.YAMLError as exc:
                        print(exc)
                if '/' in template_yaml_file:
                    fname_data = template_yaml_file.split('/')
                else:
                    fname_data = [template_yaml_file]
                    temp_fname = fname_data[-1].split('.')
                    fname = temp_fname[0]
                template_dict[fname] = self.pkt_data
        for key, data in pkt_user_data.items():
            tmp_data = {}
            tmp_data = data
            template_name_list = [k for k in tmp_data.keys()]
            template_name = template_name_list[0]
            arg_user_dict = tmp_data[template_name]
            arg_user_packet_headers = arg_user_dict['Headers']
            packet_stack = []
            if 'template' in template_name:
                template_name = template_name.replace('template[', '')
                template_name = template_name[1:len(template_name)-2]
            else:
                raise AssertionError("Template name is not defined")
            for template_data in template_dict.values():
                template_def_name_list = [k for k in template_data.keys()]
                template_def_name = template_def_name_list[0]
                if template_name == template_def_name:
                    default_arg_template_dict = template_data[template_def_name]
                    default_arg_dict = default_arg_template_dict['ARGS']
                    template_def_headers = template_data[template_def_name]['headers']
                    pkt_string = ''
                    for pkt_header in template_def_headers:
                        if pkt_header in arg_user_packet_headers:
                            pkt_fields_list = \
                                  template_data[template_def_name]['headers'][pkt_header]['fields']
                            pkt_fields_list = pkt_fields_list.split(' ')
                            for i, p_field in enumerate(pkt_fields_list):
                                temp_p_field = p_field.split('.')
                                layer_field_type = temp_p_field[1]
                                if i == 0:
                                    layer_type = temp_p_field[0]
                                    pkt_string = layer_type  + '('
                                if p_field in arg_user_dict:
                                    p_field_value = str(arg_user_dict[p_field])
                                else:
                                    if p_field not in pkt_string:
                                        p_field_value = str(default_arg_dict[p_field])
                                if p_field_value.isdigit():
                                    p_field_tvalue = int(p_field_value)
                                    tmp_field_string = layer_field_type + '='+ str(p_field_tvalue)
                                else:
                                    tmp_field_string = \
                                            layer_field_type + '=\''+ str(p_field_value) + '\''
                                pkt_string = pkt_string + tmp_field_string + ','
                            pkt_string = pkt_string[:-1]
                            pkt_string = pkt_string + ')'
                            packet_stack.append(pkt_string)
            final_packet_string = '/'.join(packet_stack)
            if 'create' in yaml_type:
                self.raw_send_packet[key] = final_packet_string
            elif 'verify' in yaml_type:
                self.raw_verify_packet[key] = final_packet_string

