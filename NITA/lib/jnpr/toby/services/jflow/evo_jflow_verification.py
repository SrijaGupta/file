#!/usr/bin/python3

"""
This module contains API's for PTX Jflow verification

__author__ = [''Vimal Patel']
__contact__ = 'vimalp@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2019'

"""
import threading
import re
import ipaddress
import copy
import jnpr.toby.services.rutils as rutils
from jnpr.toby.services import utils
from jnpr.toby.services.jflow.jflow_verification import jflow_verification

class evo_jflow_verification(jflow_verification):
    """
    Class for the PTX Jflow verification of the exported
    DATA TEMPLATE, OPTION DATA, DATA RECORD and OPTION DATA
    """
    def __init__(self):
        """
         Constructor to initialize all the attributes to None
        """
        super().__init__()
        self.cflow_version = None
        self.template_type = None
        self.sampling_interface = None
        self.flow_colls = None
        self.tshark_output = None
        self.jflow_type = None
        self.dhandle = None
        self.platform = None
        self.jflow_template_version = None
        self.template_family_details = None
        self.obs_dmn_ids = None
        self.decode_dump_with_flow_selectors = None
        self.data_template_dict = None
        self.option_template_dict = None
        self.option_template_sys_dict = None
        self.data_templ_id = None
        self.option_templ_id = None
        self.option_templ_sysid = None
        self.expected_datatemp_pktflowset = None
        self.expected_optiontemp_pktflowset = None
        self.expected_data_pkt_flowset_name = None
        self.exp_optionpkt_flowset = None
        self.exp_optionpkt_sys_flowset = None
        self.flow_selector_identifier = None
        self.flow_selector_possible_sequence = None
        self.input_if = None
        self.data_template_last_timestamp = None
        self.option_template_last_timestamp = None
        self.data_template_first_timestamp = None
        self.option_template_first_timestamp = None
        self.curr_top_label_list = []
        self.full_labels_stack = []
        self.jflow_labels_stack = []
        self.temp_dict_data = None
        self.tmpl_verify_stat = None
        self.flow_seq_verification_status = None
        self.template_refresh_rate_status = None
        self.dscp_value_verification_status = None
        self.option_data_template_scope_verify_status = None
        self.option_data_system_scope_verify_status = None
        self.data_record_status = None
        self.objj = None
        self.log = utils.log

    def init(self, device_handle=None, **kwarg):
        """
        | This method will be called to initialize the default value for
        | class attributes on the basis of manadatory arguments received.

        | This public method will take these mandatory arguments :-
        | - device_handle
        | - template_type
        | - sampling_interface
        | - flow_colls
        | - tshark_output
        | - cflow_version
        |- decode_dump_with_flow_selectors
        """
        self.cflow_version = kwarg.get('cflow_version', None)
        self.template_type = kwarg.get('template_type', None)
        self.sampling_interface = kwarg.get('sampling_interface', None)
        self.flow_colls = kwarg.get('flow_colls', None)
        self.log("INFO", "JFLOW VERIFICATION TO BE STARTED FOR "\
            "TEMPLATE: %s on collector: %s"%(self.template_type, self.flow_colls[0]))
        self.tshark_output = kwarg.get('tshark_output', None)
        self.jflow_type = kwarg.get('jflow_type', 'INLINE')
        self.dhandle = device_handle
        self.platform = self.get_chassis_platform_info()
        self.jflow_template_version = self.get_jflow_template_version()
        self.template_family_details = self.get_expected_template_details(**kwarg)
        self.obs_dmn_ids = self.get_all_observation_domain_ids(
            device_handle=self.dhandle)
        decode_dump_with_flow_selectors = kwarg.get('decode_dump_with_flow_selectors', {})
        self.decode_dump_with_flow_selectors = decode_dump_with_flow_selectors
        if 'decode_dump' not in decode_dump_with_flow_selectors or\
            'flow_selector_identifier_info' not in decode_dump_with_flow_selectors:
            raise ValueError(
                "please provide the keys with name \
                \'decode_dump\' and \'flow_selector_identifier_info\'")
        if not isinstance(decode_dump_with_flow_selectors['flow_selector_identifier_info'], list):
            raise ValueError(
                "key \'flow_selector_identifier_info\' should have value of type list or tuple")
        for content in decode_dump_with_flow_selectors['flow_selector_identifier_info']:
            if not isinstance(content, dict):
                raise ValueError(
                    "\'flow_selector_identifier_info\' should be the list of dictionary")
            else:
                for key_content, val_content in content.items():
                    del key_content
                    if not isinstance(val_content, list):
                        raise ValueError(
                            "user must provide the values in list type for value \
                             corresponding to selected flow_selector ,so that user\
                             can try find the all possible combination of flow_selector\
                             like cartesian product combination")
        self.data_template_dict = self.get_expected_data_template()
        self.option_template_dict = self.get_expected_option_template()
        self.tmpl_verify_stat = None
        self.flow_seq_verification_status = None
        self.template_refresh_rate_status = None
        self.dscp_value_verification_status = None
        self.option_data_template_scope_verify_status = None
        self.option_data_system_scope_verify_status = None
        self.data_record_status = None
        self.option_template_sys_dict = self.get_expected_option_template_system_scope()

    def get_expected_template_details(self, **kwarg):
        """This method will retrieve the required detail template IDs and flow_set names
           for  "MX platform" which will be saved in dict data structure.
        """
        if self.cflow_version == '9' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('data_template_id', None)
            configured_option_template_id = kwarg.get('option_template_scope_id', None)
            option_template_sysid = kwarg.get('option_system_scope_id', None)
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.option_templ_sysid = option_template_sysid
            self.expected_datatemp_pktflowset = 'Data Template (V9) (0)'
            self.expected_optiontemp_pktflowset = 'Options Template(V9) (1)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.exp_optionpkt_sys_flowset = '(Data) (%s)' % option_template_sysid

        if self.cflow_version == '10' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('data_template_id', None)
            configured_option_template_id = kwarg.get('option_template_scope_id', None)
            option_template_sysid = kwarg.get('option_system_scope_id', None)
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.option_templ_sysid = option_template_sysid
            self.expected_datatemp_pktflowset = 'Data Template (V10 [IPFIX]) (2)'
            self.expected_optiontemp_pktflowset = 'Options Template (V10 [IPFIX]) (3)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.exp_optionpkt_sys_flowset = '(Data) (%s)' % option_template_sysid

        ptx_templ_details = {}
        ptx_templ_details['data_templ_id'] = self.data_templ_id
        ptx_templ_details['option_templ_id'] = self.option_templ_id
        ptx_templ_details['option_templ_sysid'] = self.option_templ_sysid
        ptx_templ_details['expected_data_template_pkt_flowset_name'] = \
            self.expected_datatemp_pktflowset
        ptx_templ_details['expected_option_template_pkt_flowset_name'] = \
            self.expected_optiontemp_pktflowset
        ptx_templ_details['expected_data_pkt_flowset_name'] = \
            self.expected_data_pkt_flowset_name
        ptx_templ_details['expected_option_pkt_flowset_name'] = \
            self.exp_optionpkt_flowset
        ptx_templ_details['expected_option_pkt_system_flowset_name'] = \
            self.exp_optionpkt_sys_flowset
        return ptx_templ_details

    def get_all_observation_domain_ids(self, **kwg):
        """
        This method will retrieve all the possible observation domain \
        Ids or source Ids per template type.
        """
        if  self.jflow_type == 'INLINE':
            obs_list = []
            rut1 = rutils.rutils()
            if 'sampling_interface' in kwg:
                fpc_slot, pic_slot, port_num = rut1.get_fpc_pic_port_from_ifname(
                    kwg['sampling_interface'])
            elif 'fpc_slot' in kwg:
                fpc_slot = kwg['fpc_slot']
            else:
                fpc_slot, pic_slot, port_num = rut1.get_fpc_pic_port_from_ifname(
                    self.sampling_interface)
            del rut1
            del pic_slot
            del port_num
            obs_list.append(str(int(fpc_slot) * 4))
            return obs_list

    def get_expected_data_template(self):
        """
        This method returns the expected data template for depending upon
        the cflow version , platform , jflow template version and
        template type for sampling applied.

        It will be called internally while calling init function

        :return: dictionary output for expected data template

        :rtype: dict
        """
        template_dict = {}
        if self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['ingressInterfaceType'] = {
                'Length': '4', 'Type': 'ingressInterfaceType', 'Element_id': '368'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            return template_dict

        elif self.jflow_template_version == '17.2X75' and \
        self.cflow_version == '10' and self.template_type == 'ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['icmpTypeCodeIPv6'] = {
                'Length': '2', 'Type': 'icmpTypeCodeIPv6', 'Element_id': '139'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['ingressInterfaceType'] = {
                'Length': '4', 'Type': 'ingressInterfaceType', 'Element_id': '368'}
            return template_dict

##        elif self.jflow_template_version == '19.2' and \
        elif self.jflow_template_version in ['19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['icmpTypeCodeIPv6'] = {
                'Length': '2', 'Type': 'icmpTypeCodeIPv6', 'Element_id': '139'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['ingressInterfaceType'] = {
                'Length': '4', 'Type': 'ingressInterfaceType', 'Element_id': '368'}
            template_dict['BGP_IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'BGP_IPV6_NEXT_HOP', 'Element_id': '63'}
            return template_dict

        elif self.jflow_template_version == '17.2X75' and \
        self.cflow_version == '9' and self.template_type == 'ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {
                'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

##        elif self.jflow_template_version == '19.2' and \
        elif self.jflow_template_version in ['19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {
                'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['BGP_IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'BGP_IPV6_NEXT_HOP', 'Element_id': '63'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'mpls' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['ingressInterfaceType'] = {
                'Length': '4', 'Type': 'ingressInterfaceType', 'Element_id': '368'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'mpls' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'mpls-ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['ingressInterfaceType'] = {
                'Length': '4', 'Type': 'ingressInterfaceType', 'Element_id': '368'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_IPv6_ADDRESS'] = {
                'Length': '16', 'Type': 'MPLS_TOP_LABEL_IPv6_ADDRESS', 'Element_id': '140'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'mpls-ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
            return template_dict

        elif self.jflow_template_version == '17.2X75' and \
        self.cflow_version == '10' and self.template_type == 'mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['icmpTypeCodeIPv6'] = {
                'Length': '2', 'Type': 'icmpTypeCodeIPv6', 'Element_id': '139'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['ingressInterfaceType'] = {
                'Length': '4', 'Type': 'ingressInterfaceType', 'Element_id': '368'}
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_IPv6_ADDRESS'] = {
                'Length': '16', 'Type': 'MPLS_TOP_LABEL_IPv6_ADDRESS', 'Element_id': '140'}
            return template_dict

        elif self.jflow_template_version == '19.3' and \
        self.cflow_version == '10' and self.template_type == 'mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['icmpTypeCodeIPv6'] = {
                'Length': '2', 'Type': 'icmpTypeCodeIPv6', 'Element_id': '139'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['ingressInterfaceType'] = {
                'Length': '4', 'Type': 'ingressInterfaceType', 'Element_id': '368'}
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_IPv6_ADDRESS'] = {
                'Length': '16', 'Type': 'MPLS_TOP_LABEL_IPv6_ADDRESS', 'Element_id': '140'}
            template_dict['BGP_IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'BGP_IPV6_NEXT_HOP', 'Element_id': '63'}
            return template_dict


        elif self.jflow_template_version == '17.2X75' and \
        self.cflow_version == '9' and self.template_type == 'mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
            return template_dict


        elif self.jflow_template_version == '19.3' and \
        self.cflow_version == '9' and self.template_type == 'mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
            template_dict['BGP_IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'BGP_IPV6_NEXT_HOP', 'Element_id': '63'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'mpls-ipv4-mpls-ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['INNER_IP_SRC_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['INNER_IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'mpls-ipv4-mpls-ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['INNER_IP_SRC_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['INNER_IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'mpls-ipv4-mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['icmpTypeCodeIPv6'] = {
                'Length': '2', 'Type': 'icmpTypeCodeIPv6', 'Element_id': '139'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'mpls-ipv4-mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'ipv4-mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'ipv4-mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'ipv4-mpls-ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['INNER_IP_SRC_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['INNER_IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'ipv4-mpls-ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['INNER_IP_SRC_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['INNER_IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict
            ############################################################################

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'mpls-vx-ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['INNER_IP_SRC_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['INNER_IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'mpls-vx-ipv4' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['INNER_IP_SRC_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['INNER_IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'INNER_IP_DST_ADDR', 'Element_id': '12'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '10' and self.template_type == 'mpls-vx-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] and \
        self.cflow_version == '9' and self.template_type == 'mpls-vx-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['IP_SRC_ADDR'] = {'Length': '4', 'Type': 'IP_SRC_ADDR', 'Element_id': '8'}
            template_dict['IP_DST_ADDR'] = {
                'Length': '4', 'Type': 'IP_DST_ADDR', 'Element_id': '12'}
            template_dict['L4_SRC_PORT'] = {'Length': '2', 'Type': 'L4_SRC_PORT', 'Element_id': '7'}
            template_dict['L4_DST_PORT'] = {
                'Length': '2', 'Type': 'L4_DST_PORT', 'Element_id': '11'}
            template_dict['SRC_MASK'] = {'Length': '1', 'Type': 'SRC_MASK', 'Element_id': '9'}
            template_dict['DST_MASK'] = {'Length': '1', 'Type': 'DST_MASK', 'Element_id': '13'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'IP_NEXT_HOP', 'Element_id': '15'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['INNER_MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'INNER_MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['IPV6_SRC_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_SRC_ADDR', 'Element_id': '27'}
            template_dict['IPV6_DST_ADDR'] = {
                'Length': '16', 'Type': 'IPV6_DST_ADDR', 'Element_id': '28'}
            template_dict['IP_TOS'] = {'Length': '1', 'Type': 'IP_TOS', 'Element_id': '5'}
            template_dict['PROTOCOL'] = {'Length': '1', 'Type': 'PROTOCOL', 'Element_id': '4'}
            template_dict['INNER_L4_SRC_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_SRC_PORT', 'Element_id': '7'}
            template_dict['INNER_L4_DST_PORT'] = {
                'Length': '2', 'Type': 'INNER_L4_DST_PORT', 'Element_id': '11'}
            template_dict['ICMP_TYPE'] = {'Length': '2', 'Type': 'ICMP_TYPE', 'Element_id': '32'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            return template_dict


    def get_expected_option_template(self):
        """
        This method returns the expected option template depending upon
        the cflow version , platform and jflow template version.


        It will be called internally while calling init function

        :return: dictionary output for expected option template

        :rtype:
        """
        template_dict = {}
        if self.jflow_template_version in ['17.2X75', '19.2', '19.3'] \
        and self.cflow_version == '10' and self.jflow_type == 'INLINE':
            template_dict['templateId'] = {
                'Length': '2', 'Type': 'templateId', 'Element_id': '145'}
            template_dict['SAMPLING_INTERVAL'] = {
                'Length': '4', 'Type': 'SAMPLING_INTERVAL', 'Element_id': '34'}
            template_dict['FLOW_ACTIVE_TIMEOUT'] = {
                'Length': '2', 'Type': 'FLOW_ACTIVE_TIMEOUT', 'Element_id': '36'}
            template_dict['FLOW_INACTIVE_TIMEOUT'] = {
                'Length': '2', 'Type': 'FLOW_INACTIVE_TIMEOUT', 'Element_id': '37'}
            return template_dict

        if self.jflow_template_version in ['17.2X75', '19.2', '19.3'] \
        and self.cflow_version == '9' and self.jflow_type == 'INLINE':
            template_dict['Template'] = {
                'Length': '2', 'Type': 'Template', 'Element_id': '5'}
            template_dict['SAMPLING_INTERVAL'] = {
                'Length': '4', 'Type': 'SAMPLING_INTERVAL', 'Element_id': '34'}
            template_dict['FLOW_ACTIVE_TIMEOUT'] = {
                'Length': '2', 'Type': 'FLOW_ACTIVE_TIMEOUT', 'Element_id': '36'}
            template_dict['FLOW_INACTIVE_TIMEOUT'] = {
                'Length': '2', 'Type': 'FLOW_INACTIVE_TIMEOUT', 'Element_id': '37'}
            return template_dict

    def get_expected_option_template_system_scope(self):
        """
        This method returns the expected option template system scope
        depending upon the cflow version , platform and jflow template
        version.


        It will be called internally while calling init function

        :return: dictionary output for expected option template

        :rtype:
        """
        template_dict = {}
        if self.jflow_template_version in ['17.2X75', '19.2', '19.3'] \
        and self.cflow_version == '10' and self.jflow_type == 'INLINE':
            template_dict['selectorId'] = {
                'Length': '8', 'Type': 'selectorId', 'Element_id': '302'}
            template_dict['SAMPLING_ALGORITHM'] = {
                'Length': '1', 'Type': 'SAMPLING_ALGORITHM', 'Element_id': '35'}
            return template_dict

        elif self.jflow_template_version in ['17.2X75', '19.2', '19.3'] \
        and self.cflow_version == '9' and self.jflow_type == 'INLINE':
            template_dict['System'] = {
                'Length': '4', 'Type': 'System', 'Element_id': '1'}
            template_dict['SAMPLING_ALGORITHM'] = {
                'Length': '1', 'Type': 'SAMPLING_ALGORITHM', 'Element_id': '35'}
            return template_dict

    def verify_template_record(self, template_to_verify='BOTH'):
        """
        | This method will compare the element names , element id and type
        | for data template or option template or both (data & option template)
        |
        | It compares expected template dictionary and actual template dictionary
        | per Collector and per Observation Domain Id and return True
        | if verification succeed else return false
        """
        if self.platform == 'PTX' and template_to_verify == 'BOTH' \
        and self.jflow_type == 'INLINE':
            ptxdata_temp_status = self.verify_ptx_template_inline(
                'DATA TEMPLATE')
            ptxoption_temp_status = self.verify_ptx_template_inline(
                'OPTION TEMPLATE')
            ptxoption_temp_status2 = self.verify_ptx_template_inline(
                'OPTION TEMPLATE SYSTEM SCOPE')
            if ptxdata_temp_status is True and \
            ptxoption_temp_status is True and ptxoption_temp_status2 is True:
                ptx_template_verify_status = True
                self.tmpl_verify_stat = ptx_template_verify_status
                return ptx_template_verify_status
            else:
                ptx_template_verify_status = False
                if ptxdata_temp_status is False:
                    self.log("ERROR", "Data Template verification failed ")
                if ptxoption_temp_status is False or \
                ptxoption_temp_status2 is False:
                    self.log("ERROR", "Option Template verification failed ")
                self.tmpl_verify_stat = ptx_template_verify_status
                return ptx_template_verify_status

        elif self.platform == 'PTX' and template_to_verify == 'DATA TEMPLATE' \
        and self.jflow_type == 'INLINE':
            ptxdata_temp_status = self.verify_ptx_template_inline(
                'DATA TEMPLATE')
            self.tmpl_verify_stat = ptx_template_verify_status
            return ptxdata_temp_status

        elif self.platform == 'PTX' and template_to_verify == 'OPTION TEMPLATE' \
        and self.jflow_type == 'INLINE':
            ptxoption_temp_status = self.verify_ptx_template_inline(
                'OPTION TEMPLATE')
            ptxoption_temp_status2 = self.verify_ptx_template_inline(
                'OPTION TEMPLATE SYSTEM SCOPE')
            if ptxoption_temp_status is True and \
            ptxoption_temp_status2 is True:
                ptx_template_verify_status = True
                self.tmpl_verify_stat = ptx_template_verify_status
                return ptx_template_verify_status
            else:
                ptx_template_verify_status = False
                self.tmpl_verify_stat = ptx_template_verify_status
                return ptx_template_verify_status

    def verify_ptx_template_inline(self, template_to_verify=None):
        """
        template_to_verify \'DATA TEMPLATE\' and \'OPTION TEMPLATE\'
        for PTX platform

        It will be internally called by method name "verify_template_record"

        :return: True if template verification succeed else False

        :rtype: bool
        """
        result_list = []
        obs_dmn_ids = self.obs_dmn_ids
        flow_colls = self.flow_colls
        decode_dump = self.decode_dump_with_flow_selectors['decode_dump']
        if template_to_verify not in ['DATA TEMPLATE', 'OPTION TEMPLATE' \
                                         , 'OPTION TEMPLATE SYSTEM SCOPE']:
            raise ValueError(
                "please provide input --> template_to_verify <-- as "\
                "either DATA TEMPLATE or OPTION TEMPLATE")

        if template_to_verify == 'DATA TEMPLATE':
            verify_type = 'TEMPLATE'
            templ_id = self.data_templ_id
            expected_template_dict = self.data_template_dict
            if self.cflow_version == '9':
                expected_template_pkt_type = 'Data Template (V9) (0)'
            elif self.cflow_version == '10':
                expected_template_pkt_type = 'Data Template (V10 [IPFIX]) (2)'

        elif template_to_verify == 'OPTION TEMPLATE':
            templ_id = self.option_templ_id
            expected_template_dict = self.option_template_dict
            verify_type = 'OPTIONS'
            if self.cflow_version == '9':
                expected_template_pkt_type = 'Options Template(V9) (1)'
            elif self.cflow_version == '10':
                expected_template_pkt_type = 'Options Template (V10 [IPFIX]) (3)'
        elif template_to_verify == 'OPTION TEMPLATE SYSTEM SCOPE':
            templ_id = self.option_templ_sysid
            expected_template_dict = self.option_template_sys_dict
            verify_type = 'OPTIONS'
            if self.cflow_version == '9':
                expected_template_pkt_type = 'Options Template(V9) (1)'
            elif self.cflow_version == '10':
                expected_template_pkt_type = 'Options Template (V10 [IPFIX]) (3)'
        else:
            raise ValueError(
                "Please Provide the correct template type input "\
                 "either \"DATA TEMPLATE\" or \"OPTION TEMPLATE\"")

        list_of_element_name = list(expected_template_dict.keys())
        for flw_col_tmp in flow_colls:
            self.log("INFO", "Now Checking the template record on "\
            "collector IP : %s" % flw_col_tmp)
            actual_obs_domn_keys = decode_dump['FLOWS'][flw_col_tmp].keys()
            actual_obs_domn_keys = list(actual_obs_domn_keys)
            for obs_dmn_id_tmp in obs_dmn_ids:
                result = True
                obs_dmn_id_tmp = str(obs_dmn_id_tmp)
                self.log("INFO", "Now Checking the template record "\
                "for observation domain id : %s having template id : %s"%\
                (obs_dmn_id_tmp, templ_id))
                if obs_dmn_id_tmp not in actual_obs_domn_keys:
                    result = False
                    break
                if verify_type == 'TEMPLATE' or verify_type == 'OPTIONS':
                    actual_cflow_ver = \
                    decode_dump['FLOWS'][flw_col_tmp][obs_dmn_id_tmp]\
[templ_id][verify_type][0]['Version']
                    actual_template_pkt_type = \
                    decode_dump['FLOWS'][flw_col_tmp][obs_dmn_id_tmp][templ_id]\
[verify_type][0]['flowset']['FlowSet Id']
                    exp_cflow_ver = self.cflow_version
                    if actual_cflow_ver != exp_cflow_ver:
                        self.log("ERROR", \
                            "Cflow version mismatch ----> Actual : %s"\
                            " Expected : %s"%\
                            (actual_cflow_ver, exp_cflow_ver))
                        result = False
                    if actual_template_pkt_type != expected_template_pkt_type:
                        self.log("ERROR", \
                            "template_pkt_type mismatch  ----> Actual : %s"\
                            " Expected %s: "%(actual_template_pkt_type, expected_template_pkt_type))
                        result = False
                    actual_test_template = \
                    decode_dump['FLOWS'][flw_col_tmp][obs_dmn_id_tmp][templ_id]\
[verify_type][0]['flowset']['field']
                    for elm in actual_test_template:
                        element_name = re.search(r'(.*)\s[(]\d+[)]', elm['Type'])
                        element_name = element_name.group(1)
                        if element_name not in list_of_element_name:
                            self.log("ERROR", "%s not found"%element_name)
                            result = False
                        element_id = re.search(r'[(](\d+)[)]', elm['Type'])
                        element_id = element_id.group(1)
                        element_length = re.search(r'\d+', elm['Length'])
                        element_length = element_length.group()
                        expected_element_id = expected_template_dict[element_name]['Element_id']
                        expected_element_length = expected_template_dict[element_name]['Length']
                        if element_id != expected_element_id:
                            self.log("ERROR", \
                                "element_id mismatch for element_name %s ----> Actual : %s"\
                                " Expected : %s"%\
                                (element_name, element_id, expected_element_id))
                            result = False
                        if element_length != expected_element_length:
                            self.log("ERROR", \
                                "element_length mismatch for element_name %s ----> Actual : "\
                                "%s Expected : %s" %\
                                (element_name, element_length, expected_element_length))
                            result = False
                result_list.append(result)
        for res in result_list:
            if res is False:
                return False
        return True

    def verify_option_data_record(self, option_data_to_verify='TEMPLATE SCOPE', **kwarg):
        """
        | This method will compare the values of Actual option data record received at
        | collector saved in dictionary data structure with our expected dictionary
        | built in test script.
        """
        if self.jflow_type == "INLINE":
            ptx_option_data_record_status = \
            self.verify_ptx_option_data_inline(option_data_to_verify, **kwarg)

            if option_data_to_verify == 'TEMPLATE SCOPE':
                self.option_data_template_scope_verify_status = ptx_option_data_record_status
            elif option_data_to_verify == 'SYSTEM SCOPE':
                self.option_data_system_scope_verify_status = ptx_option_data_record_status
            return ptx_option_data_record_status

    def verify_ptx_option_data_inline(self, option_data_to_verify, **kwarg):
        """
        This method will verify option data record only for 'MX' platform

        It will be internally called by method name "verify_option_data_record"

        :return: True if template verification succeed else False

        :rtype: bool
        """
        result_list = []
        obs_dmn_ids = self.obs_dmn_ids
        flow_colls = self.flow_colls
        decode_dump = self.decode_dump_with_flow_selectors['decode_dump']
        expected_option_data_pdu_dict = kwarg.get('expected_option_data_pdu_dict', {})
        if option_data_to_verify == 'TEMPLATE SCOPE':
            templ_id = self.option_templ_id
            expected_template_pkt_type = self.exp_optionpkt_flowset
            if self.cflow_version == '9':
                verify_type = 'OPTIONS_DATA_V9_INLINE'
                expected_option_data_pdu_dict['ScopeTemplate'] = '0' + \
                hex(int(self.data_templ_id))[2:]
            elif self.cflow_version == '10':
                verify_type = 'OPTIONS_DATA_IPFIX_INLINE'
                expected_option_data_pdu_dict['Template Id'] = self.data_templ_id
        elif option_data_to_verify == 'SYSTEM SCOPE':
            templ_id = self.option_templ_sysid
            expected_template_pkt_type = self.exp_optionpkt_sys_flowset
            verify_type = 'OPTIONS_DATA'

        for flw_col_tmp in flow_colls:
            self.log("INFO", "Now Checking the option data record "\
            "on collector IP : %s"% flw_col_tmp)
            actual_obs_domn_keys = decode_dump['FLOWS'][flw_col_tmp].keys()
            actual_obs_domn_keys = list(actual_obs_domn_keys)
            for obs_dmn_id_tmp in obs_dmn_ids:
                result = True
                obs_dmn_id_tmp = str(obs_dmn_id_tmp)
                self.log("INFO", \
                    "Now Checking the option data record for observation domain id : %s" %\
                    obs_dmn_id_tmp)
                if obs_dmn_id_tmp not in actual_obs_domn_keys:
                    result = False
                    break
                if verify_type == 'OPTIONS_DATA_V9_INLINE' or \
                verify_type == 'OPTIONS_DATA_IPFIX_INLINE' or \
                verify_type == 'OPTIONS_DATA':
                    if "OPTIONS_DATA_V9_INLINE" in decode_dump['FLOWS'][flw_col_tmp][obs_dmn_id_tmp][templ_id]:
                        verify_type = "OPTIONS_DATA_V9_INLINE"
                    elif "OPTIONS_DATA_IPFIX_INLINE" in decode_dump['FLOWS'][flw_col_tmp][obs_dmn_id_tmp][templ_id]:
                        verify_type = "OPTIONS_DATA_IPFIX_INLINE"
                    else:
                        verify_type = "OPTIONS_DATA"
                    actual_cflow_ver = \
                    decode_dump['FLOWS'][flw_col_tmp][obs_dmn_id_tmp][templ_id]\
[verify_type][-1]['Version']
                    actual_template_pkt_type = \
                        decode_dump['FLOWS'][flw_col_tmp][obs_dmn_id_tmp][templ_id]\
[verify_type][-1]['flowset']['FlowSet Id']
                    exp_cflow_ver = self.cflow_version
                    if actual_cflow_ver != exp_cflow_ver:
                        self.log("ERROR", \
                            "Cflow version mismatch ----> Actual : %s"\
                            " Expected : %s"%(actual_cflow_ver, exp_cflow_ver))
                        result = False
                    if actual_template_pkt_type != expected_template_pkt_type:
                        self.log("ERROR", \
                            "template_pkt_type mismatch  ----> Actual : %s"\
                            " Expected : %s"%\
                            (actual_template_pkt_type, expected_template_pkt_type))
                        result = False
                    result_list.append(result)
                    if option_data_to_verify == 'SYSTEM SCOPE':
                        actual_option_data_pdu_dict = decode_dump['FLOWS'][flw_col_tmp][
                            obs_dmn_id_tmp][templ_id][verify_type][-1]['flowset']['pdu'][0]
                        result2 = self.compare_flow_records(
                            expected_option_data_pdu_dict, actual_option_data_pdu_dict)
                        result_list.append(result2)
                    elif option_data_to_verify == 'TEMPLATE SCOPE':
                        pdu_list = decode_dump['FLOWS'][flw_col_tmp][
                            obs_dmn_id_tmp][templ_id][verify_type][-1]['flowset']['pdu']
                        matched_pdu_dict = 0
                        for elem in pdu_list:
                            find_req_pdu_dict = elem
                            found_pdu_dict = self.compare_flow_records(
                                expected_option_data_pdu_dict, find_req_pdu_dict)
                            if found_pdu_dict is True:
                                matched_pdu_dict = matched_pdu_dict + 1
                        print("matched_pdu_dict :", matched_pdu_dict)
                        if matched_pdu_dict == 1:
                            result2 = True
                            result_list.append(result2)
                        else:
                            result2 = False
                            result_list.append(result2)
        for res in result_list:
            if res is False:
                return False
        return True

    def verify_data_record(self, **kwg):
        """
        | This method will be called to validate the exported data record .
        | It will compare the values of Actual data record received at
        | collector saved in dictionary data structure with our expected dictionary
        | built via test script, "decode_dump_with_flow_selectors" and
        | few key-value pair detail will be calculated at run time of this method.
        |
        | DATA record verification comprises of 3 stages :-
        | 1. Parsing the "expected_pdu_dict" while calling this method.
        |    It should be a dictionary where we expect that values of keys
        |    will be same across all flows.
        | 2. Details provide in init with help of "decode_dump_with_flow_selectors".
        |    "decode_dump_with_flow_selectors" is mandatory argument for init section.
        |    It will have two contents as explained in init section:-
        |        2.1 decode_dump - Actual dictionary (tshark output decoded in
        |                          python's dictionary)
        |        2.2 flow_selector_identifier info - The flow selector which helped
        |                                            in creating different flows or can be the element
        |                                            which can help in uniquely decode the tshark output.
        |    During run time (key-value) detail will added in expected_pdu_dict
        | 3. For Some elements (key-value details) will be added during run to "expected_pdu_dict"
        |    which are :-
        |    3.1 SrcAs
        |    3.2 DstAs
        |    3.3 SrcMask
        |    3.4 DstMask
        |    3.5 Vlan ID
        |    3.6 NextHop
        |    3.7 BGPNextHop
        |    3.8 InputInt
        |    3.9 OutputInt

        :param dict expected_pdu_dict
            **OPTIONAL** While validating data records if you think that few elements values
                         will always be same across all the flows created then, define the
                         values keeping elements as key in dictionary
                         expected_pdu_dict = {'MaxTTL' : '64' , 'Protocol' : '17'}
        :param string flow_selector_possible_sequence
            **OPTIONAL** This optional argument can be used to validate those flows which
                         are not possible to be verified by providing information to
                         "decode_dump_with_flow_selectors" key while calling init.

                         Note:- User must provide the flow selectors keys in
                                "decode_dump_with_flow_selectors" key while calling init.
                                but keep the respective values as an empty list.

                         please refer documentation details related to
                         "decode_dump_with_flow_selectors" at init section.
                         decode_dump_with_flow_selectors =
                           { 'decode_dump' : decode_dict ,
                             'flow_selector_identifier_info' : [{'SrcAddr' : []}, {'SrcAddr' : []}]}

                         Suppose for a test, user created the flows by varying only Source IP Address
                         and Source port while keeping Protocol, Destination Addrress and
                         Destination port constant
                         Flow 1  - 70.0.0.1 : 12500
                         Flow 2  - 80.0.0.1 : 13500
                         Flow 3  - 90.0.0.1 : 14500
                         Above flows doesn't satisfy cartesian product output of SrcAddr and SrcPort
                         so these kinds of flows cannot be verified by only providing
                         "decode_dump_with_flow_selectors"

                         So to handle above scenario , follow steps mentioned below :-
                         decode_dump_with_flow_selectors =
                           { 'decode_dump' : decode_dict ,
                             'flow_selector_identifier_info' : [{'SrcAddr' : []}, {'SrcAddr' : []}]}

                         flow_selector_possible_sequence = [ ['70.0.0.1', 12500],
                                                             ['80.0.0.1', 13500],
                                                             ['90.0.0.1', 14500],
                                                           ]
                                                         It looks like List of Lists


        :return: True if data verification succeed across collector per \
                 sampling observation domain ID else False

        :rtype: bool

        Example::

            python:
                expected_pdu_dict = {'Protcol' : '1', 'MinTTL' : '64' ,\
                                    'MaxTTL' : '64' , 'Flow End Reason' : 'Idle timeout (1)}

                verify_data_record(
                    expected_pdu_dict = expected_pdu_dict)
                    Or
                flow_selector_possible_sequence = [ ['70.0.0.1', 12500],
                                                    ['80.0.0.1', 13500],
                                                    ['90.0.0.1', 14500],
                                                  ]
                verify_data_record(
                    expected_pdu_dict = expected_pdu_dict,
                    flow_selector_possible_sequence = flow_selector_possible_sequence )
            Robot:
                Verify Data Record    expected_pdu_dict=${expected_pdu_dict}
                    Or
                ${flow_selector_possible_sequence} =     Evaluate   \
                                                   [ ['70.0.0.1', 12500],
                                                     ['80.0.0.1', 13500],
                                                     ['90.0.0.1', 14500],
                                                   ]
                Verify Data Record    expected_pdu_dict=${expected_pdu_dict}
                                      flow_selector_possible_sequence = ${flow_selector_possible_sequence}


        """

        if  self.jflow_type == 'INLINE':
            ptx_data_record_verify_status = self.verify_ptx_data_record_inline(**kwg)
            self.data_record_status = ptx_data_record_verify_status
            return ptx_data_record_verify_status

    def verify_ptx_data_record_inline(self, **kwg):
        """
        This method will verify data record only for 'PTX' platform

        It will be internally called by method name "verify_data_record"

        :return: True if template verification succeed else False

        :rtype: bool
        """

        if 'expected_pdu_dict' in kwg:
            expected_pdu_dict = kwg['expected_pdu_dict']
        else:
            expected_pdu_dict = {}
        do_not_verify = kwg.get('do_not_verify', [])
        if self.template_type == 'mpls':
            do_not_verify.extend(['SrcAddr', 'DstAddr', 'SrcPort', 'DstPort'])
            do_not_verify.extend(['SrcAS', 'DstAS', 'SrcMask', 'DstMask'])
            do_not_verify.extend(['NextHop', 'BGPNextHop'])
        decode_dump = self.decode_dump_with_flow_selectors['decode_dump']
        flow_colls = self.flow_colls
        obs_dmn_ids = self.obs_dmn_ids
        verify_type = 'DATA'
        templ_id = self.data_templ_id
        expected_template_pkt_type = self.expected_data_pkt_flowset_name
        exp_cflow_ver = self.cflow_version

        flow_selector_identifier = []
        for content in self.decode_dump_with_flow_selectors['flow_selector_identifier_info']:
            for key_content, val_content in content.items():
                del val_content
                flow_selector_identifier.append(key_content)
        self.flow_selector_identifier = flow_selector_identifier
        if 'flow_selector_possible_sequence' not in kwg:
            flow_selectors_list_value = []
            for content in self.decode_dump_with_flow_selectors['flow_selector_identifier_info']:
                for key_content, val_content in content.items():
                    del key_content
                    flow_selectors_list_value.append(val_content)

                # Note :- flow_selector_possible_product will be list of flow_selector list
            flow_selector_possible_sequence = self.get_flow_selector_possible_sequence(
                *flow_selectors_list_value)
            self.flow_selector_possible_sequence = flow_selector_possible_sequence
            # Note :- flow_selector_possible_sequence is list of tuples of cartesian product
        else:
            # overriding the value of --> flow_selector_identifier <-- and -->
            # flow_selector_possible_sequence <-- which was saved in object
            self.flow_selector_possible_sequence = kwg['flow_selector_possible_sequence']
            flow_selector_possible_sequence = self.flow_selector_possible_sequence

        if len(flow_selector_possible_sequence) == 0:
            self.log("ERROR", "Either provide the expected values in list type  "\
                   "for selectors used to decode the pcap capture (while calling Init function)"\
                   " or else provide the flow_selector_possible_sequence while "\
                   "calling funtion verify_data_record()")
            return False
        result_list = []
        for flw_col_tmp in flow_colls:
            self.log("INFO", "Now Checking the option data record "\
            "on collector IP : %s"% flw_col_tmp)
            actual_obs_domn_keys = decode_dump['FLOWS'][flw_col_tmp].keys()
            actual_obs_domn_keys = list(actual_obs_domn_keys)

            for obs_dmn_id_tmp in obs_dmn_ids:
                obs_dmn_id_tmp = str(obs_dmn_id_tmp)
                self.log("INFO", \
                    "Now Checking the template record for observation domain id : %s" %\
                    obs_dmn_id_tmp)
                if obs_dmn_id_tmp not in actual_obs_domn_keys:
                    self.log("ERROR", \
                        "Observation domain id %s not found in Actual decoded dictionary"%\
                        obs_dmn_id_tmp)
                    result = False
                    result_list.append(False)
                    break
                if float(self.jflow_template_version[:4]) >= 17.2:
                    for comb in flow_selector_possible_sequence:
                        if 'DATA' not in decode_dump['FLOWS'][flw_col_tmp]\
[obs_dmn_id_tmp][templ_id].keys():
                            self.log("ERROR", \
                            "DATA not found in Actual decoded dictionary")
                            return False
                        frame = copy.deepcopy(decode_dump['FLOWS'][flw_col_tmp]\
[obs_dmn_id_tmp][templ_id][verify_type])
                        count = 0
                        for selector in comb:
                            if flow_selector_identifier[count] == 'SrcAddr':
                                expected_pdu_dict['SrcAddr'] = selector
                            elif flow_selector_identifier[count] == 'DstAddr':
                                expected_pdu_dict['DstAddr'] = selector
                            elif flow_selector_identifier[count] == 'SrcPort':
                                expected_pdu_dict['SrcPort'] = selector
                            elif flow_selector_identifier[count] == 'DstPort':
                                expected_pdu_dict['DstPort'] = selector
                            elif flow_selector_identifier[count] == 'IP ToS':
                                expected_pdu_dict['IP ToS'] = selector
                            elif flow_selector_identifier[count] == 'Protocol':
                                expected_pdu_dict['Protocol'] = selector
                            elif flow_selector_identifier[count] == 'TCP Flags':
                                expected_pdu_dict['TCP Flags'] = selector
                            elif flow_selector_identifier[count] == 'Type':
                                expected_pdu_dict['Type'] = selector
                            elif flow_selector_identifier[count] == 'IPv6 ICMP Code':
                                expected_pdu_dict['IPv6 ICMP Code'] = selector
                            elif flow_selector_identifier[count] == 'BGPNextHop':
                                expected_pdu_dict['BGPNextHop'] = selector
                            elif flow_selector_identifier[count] == 'NextHop':
                                expected_pdu_dict['NextHop'] = selector
                            elif flow_selector_identifier[count] == 'InputInt':
                                expected_pdu_dict['InputInt'] = selector
                            elif flow_selector_identifier[count] == 'OutputInt':
                                expected_pdu_dict['OutputInt'] = selector
                            elif flow_selector_identifier[count] == 'MPLS-Label1-exp-bits':
                                expected_pdu_dict['MPLS-Label1-exp-bits'] = selector
                            elif flow_selector_identifier[count] == 'MPLS-Label1':
                                expected_pdu_dict['MPLS-Label1'] = selector
                            elif flow_selector_identifier[count] == 'MPLS-Label2':
                                expected_pdu_dict['MPLS-Label2'] = selector
                            elif flow_selector_identifier[count] == 'MPLS-Label3':
                                expected_pdu_dict['MPLS-Label3'] = selector
                            elif flow_selector_identifier[count] == 'INNER_SrcAddr':
                                expected_pdu_dict['INNER_SrcAddr'] = selector
                            elif flow_selector_identifier[count] == 'INNER_DstAddr':
                                expected_pdu_dict['INNER_DstAddr'] = selector
                            elif flow_selector_identifier[count] == 'INNER_SrcPort':
                                expected_pdu_dict['INNER_SrcPort'] = selector
                            elif flow_selector_identifier[count] == 'INNER_DstPort':
                                expected_pdu_dict['INNER_DstPort'] = selector
                            if selector in frame:
                                frame = frame[selector]
                            else:
                                self.log("ERROR", \
                                    "key --> "\
                                    "%s"\
                                    " <-- not found in decode_dump or actual_dictionary"%selector)
                                self.log("INFO", \
                                    "corresponding flow_selector_identifier is : %s"%\
                                    flow_selector_identifier[count])
                                result_list.append(False)
                                break
                            count = count + 1
                            if count == len(comb):
                                actual_cflow_ver = frame['Version']
                                actual_template_pkt_type = frame['flowset']['FlowSet Id']
                                if actual_cflow_ver != exp_cflow_ver:
                                    self.log("ERROR", \
                                        "Cflow version mismatch ----> Actual : %s"\
                                        " Expected : %s"%\
                                        (actual_cflow_ver, exp_cflow_ver))
                                    result_list.append(False)
                                if actual_template_pkt_type != expected_template_pkt_type:
                                    self.log("ERROR", \
                                        "template_pkt_type mismatch  ----> Actual : %s"\
                                        " Expected : %s"%\
                                        (actual_template_pkt_type, expected_template_pkt_type))
                                    result_list.append(False)
                                actual_pdu_dict = copy.deepcopy(frame['flowset']['pdu'])
                                #print("actual_pdu_dict :- ",actual_pdu_dict)
                                if 'SrcAddr' not in expected_pdu_dict and \
                                'SrcAddr' not in do_not_verify:
                                    self.log("ERROR", \
                                        "Either declare (SrcAddr) in expected dictionary created "\
                                        "in ROBOT file or make it as a part of flow_selectors")
                                    return False
                                if 'DstAddr' not in expected_pdu_dict and \
                                'DstAddr' not in do_not_verify:
                                    self.log("ERROR", \
                                        "Either declare (DstAddr) in expected dictionary created "\
                                        "in ROBOT file or make it as a part of flow_selectors")
                                    return False
                                if 'SrcPort' not in expected_pdu_dict and \
                                'SrcPort' not in do_not_verify:
                                    self.log("ERROR", \
                                        "Either declare (SrcPort) in expected dictionary created "\
                                        "in ROBOT file or make it as a part of flow_selectors")
                                    return False
                                if 'DstPort' not in expected_pdu_dict and \
                                'DstPort' not in do_not_verify:
                                    self.log("ERROR", \
                                        "Either declare (DstPort) in expected dictionary created "\
                                        "in ROBOT file or make it as a part of flow_selectors")
                                    return False
                                if 'InputInt' not in expected_pdu_dict and \
                                'InputInt' not in do_not_verify:
                                    kwg['nh_type'] = 'iif'
                                    iif = self.get_nexthop_interface_via_route(
                                        dhandle=self.dhandle, ipaddr=expected_pdu_dict['SrcAddr'], **kwg)
                                    self.input_if = iif
                                    input_snmp_index = self.get_snmp_index_value(
                                        dhandle=self.dhandle, interface=iif)
                                    if input_snmp_index is None:
                                        expected_pdu_dict['InputInt'] = 'NO VALUE FOUND'
                                    else:
                                        expected_pdu_dict['InputInt'] = str(input_snmp_index)

                                if 'OutputInt' not in expected_pdu_dict and \
                                'OutputInt' not in do_not_verify:
                                    kwg['nh_type'] = 'oif'
                                    oif = self.get_nexthop_interface_via_route(
                                        dhandle=self.dhandle, ipaddr=expected_pdu_dict['DstAddr'], **kwg)
                                    output_snmp_index = self.get_snmp_index_value(
                                        dhandle=self.dhandle, interface=oif)
                                    if output_snmp_index is None:
                                        expected_pdu_dict['OutputInt'] = 'NO VALUE FOUND'
                                    else:
                                        expected_pdu_dict['OutputInt'] = str(output_snmp_index)

                                if 'SrcAS' not in expected_pdu_dict and \
                                'SrcAS' not in do_not_verify:
                                    as_value = self.get_as_value(
                                        dhandle=self.dhandle, ipaddr=expected_pdu_dict['SrcAddr'], **kwg)
                                    if as_value is None:
                                        expected_pdu_dict['SrcAS'] = str(4294967295)
                                    else:
                                        expected_pdu_dict['SrcAS'] = as_value
                                if 'DstAS' not in expected_pdu_dict and \
                                'DstAS' not in do_not_verify:
                                    as_value = self.get_as_value(
                                        dhandle=self.dhandle, ipaddr=expected_pdu_dict['DstAddr'], **kwg)
                                    if as_value is None:
                                        expected_pdu_dict['DstAS'] = str(4294967295)
                                    else:
                                        expected_pdu_dict['DstAS'] = as_value
                                if 'SrcMask' not in expected_pdu_dict and \
                                'SrcMask' not in do_not_verify:
                                    mask_value = self.get_ip_mask_from_route_detail(
                                        dhandle=self.dhandle, ipaddr=expected_pdu_dict['SrcAddr'])
                                    if mask_value is None:
                                        expected_pdu_dict['SrcMask'] = '0'
                                    else:
                                        expected_pdu_dict['SrcMask'] = mask_value
                                if 'DstMask' not in expected_pdu_dict and \
                                'DstMask' not in do_not_verify:
                                    mask_value = self.get_ip_mask_from_route_detail(
                                        dhandle=self.dhandle, ipaddr=expected_pdu_dict['DstAddr'])
                                    if mask_value is None:
                                        expected_pdu_dict['DstMask'] = '0'
                                    else:
                                        expected_pdu_dict['DstMask'] = mask_value
                                if 'NextHop' not in expected_pdu_dict and \
                                'NextHop' not in do_not_verify:
                                    next_hop = self.get_nexthop(
                                        dhandle=self.dhandle, ipaddr=expected_pdu_dict['DstAddr'], **kwg)
                                    if next_hop is None and \
                                    str(ipaddress.IPv4Address(expected_pdu_dict['DstAddr'])) \
                                    == expected_pdu_dict['DstAddr']:
                                        expected_pdu_dict['NextHop'] = '0.0.0.0'
                                    elif next_hop is None and \
                                    str(ipaddress.IPv6Address(expected_pdu_dict['DstAddr'])) \
                                    == expected_pdu_dict['DstAddr']:
                                        expected_pdu_dict['NextHop'] = '0::0'
                                    else:
                                        expected_pdu_dict['NextHop'] = next_hop

                                if 'BGPNextHop' not in expected_pdu_dict and \
                                'BGPNextHop' not in do_not_verify:
                                    if (self.template_type == 'ipv4' \
                                    or self.template_type == 'mpls-ipv4'\
                                    or self.template_type == 'mpls-ipv4-mpls-ipv4' or \
                                    self.template_type == 'mpls-ipv4-mpls-ipv6' or \
                                    self.template_type == 'ipv4-mpls-ipv6' or \
                                    self.template_type == 'ipv4-mpls-ipv4') and \
                                    self.jflow_template_version in ['17.2X75', '19.2', '19.3']:
                                        bgp_next_hop = self.get_bgp_nexthop(
                                            dhandle=self.dhandle,
                                            ipaddr=expected_pdu_dict['DstAddr'])
                                        if bgp_next_hop is None and \
                                        str(ipaddress.IPv4Address(expected_pdu_dict['DstAddr'])) \
                                        == expected_pdu_dict['DstAddr']:
                                            expected_pdu_dict['BGPNextHop'] = '0.0.0.0'
                                        elif bgp_next_hop is not None \
                                        and str(ipaddress.IPv4Address(expected_pdu_dict['DstAddr'])) \
                                        == expected_pdu_dict['DstAddr']:
                                            expected_pdu_dict['BGPNextHop'] = bgp_next_hop

                                #print("expected_pdu_dict :- ",expected_pdu_dict)
                                result = self.compare_flow_records(
                                    expected_pdu_dict, actual_pdu_dict)
                                result_list.append(result)
                                del frame
        self.log("INFO", "Result list :- %s"%result_list)
        final_result = True
        for res in result_list:
            if res is False:
                final_result = False
                break
        return final_result

    def verify_flow_sequence(self, **kwg):
        """
        This method will perform the flow sequence verification per observation domain

        :return: True if verification succeed per observation domain id else False

        :rtype: bool


        Example::

            python:
                obj.init( PASS ALL MANATORY PARAMETERS MENTIONED IN init)
                status = obj.verify_flow_sequence()
            Robot:
                ${status}=    Jf.Verify Flow Sequence
                Should Be True     ${status}
        """

        ifile = self.tshark_output
        obs_dmn_tmp = self.obs_dmn_ids[0]
        cflow_version = self.cflow_version
        result = True
        first_flow_sequence = kwg.get("validate_first_flow_sequence_as_zero", False)
        return_flow_sequence = kwg.get("return_flow_sequence_number",False)
        cfl = re.findall(r'(Cisco NetFlow[/]IPFIX.*?Frame\s\d+:)', ifile, re.DOTALL)
        cflow_list = []

        if self.temp_dict_data is None:
            self.temp_dict_data = {}
            self.temp_dict_data[self.template_type] = self.data_templ_id
            self.temp_dict_data['option_template_scope_id'] = self.option_templ_id
            self.temp_dict_data['option_system_scope_id'] = self.option_templ_sysid

        for pkt in cfl:
            if 'SourceId: %s' % obs_dmn_tmp in pkt or \
            'Observation Domain Id: %s' % obs_dmn_tmp in pkt:
                cflow_list.append(pkt)
        lst = ''
        for each_line in ifile.splitlines()[::-1]:
            lst = each_line + "\n"  + lst
            lst = lst.rstrip()
            last_frame_matches = re.search(r'Frame (\d+): \d+ bytes.*', each_line)
            if last_frame_matches:
                last_frame_number = last_frame_matches.group(1)
                break

        last_element = re.search(
            r'Cisco NetFlow[/]IPFIX(\n.*?)*(?:SourceId:|Observation Domain Id:) %s(?:.*\n.*)*' %
            obs_dmn_tmp, lst)
        if last_element:
            cflow_list.append(last_element.group())
            cflow_list[-1] = last_frame_number + "\n" + cflow_list[-1]

        count = 0
        for cflow in cflow_list:
            frame_check = re.search(r'Frame (\d+):$', cflow)
            if frame_check:
                frame_found = frame_check.group()
                frame_num = frame_check.group(1)
                cflow_list[count] = cflow_list[count].replace(frame_found, '')
                cflow_list[count] = "Frame " + str(int(frame_num) - 1) + ":\n" + cflow_list[count]
            count = count + 1

        if len(cflow_list) == 0:
            print("ERROR", "No Frames captured, please check the pcap or decode_dump file")
            return False
        if len(cflow_list) == 1:
            print("ERROR", "Only One Frame found in Tshark output."\
                  " Minimum 2 frame needed for flow sequence verification.")
            return False
        if cflow_version == "10":
            frame_number = 0
            for cflow in cflow_list:
                flow_seq = re.search(r'FlowSequence: (\d+)', cflow)
                current_flow_seq = int(flow_seq.group(1))
                print("INFO", "IPFIX:Current Flow Sequence Number %s"%current_flow_seq)
                template_type = re.search(r'FlowSet Id: (.*)', cflow)
                template_type = template_type.group(1)
                frame_number = frame_number + 1
                if "Template (V10 [IPFIX])" in template_type and frame_number == 1:
                    expected_flow_seq = current_flow_seq
                    if first_flow_sequence == True:
                        if current_flow_seq == 1:
                            print("First frame flow sequence value received as 1")
                        else:
                            print("ERROR","First frame flow sequence value is not 1")
                            return False
                elif "(Data)" in template_type and frame_number == 1:
                    if first_flow_sequence == True:
                        print("First frame flow sequence value received as 0 which is not expected")
                        return False
                    match_flow = re.findall(r'Flow \d+', cflow)
                    print("INFO", "Match Flow: %s"%match_flow)
                    if len(match_flow) == 0:
                        print("INFO", "Match Flow is zero")
                        match2_list = re.findall(r'FlowSet Id: [(]Data[)] [(]\d+[)]', cflow)
                        if "FlowSet Id: (Data) (%s)"%self.option_templ_id in match2_list:
                            captured_id = self.option_templ_id
                            #if captured_id == self.temp_dict_data['option_template_scope_id']:
                            if captured_id == self.option_templ_id:
                                total_present_template = len(self.temp_dict_data) - 2
                                matched3 = re.findall(r'FlowSet Length: \d.*?Data [(]\d+ '\
                                           'bytes[)],\s+no template found', cflow, re.DOTALL)
                                if len(matched3) <= (total_present_template + 1):
                                    expected_flow_seq = current_flow_seq +  \
                                    total_present_template + 1
                                    # looks like jflow is enabled for only 1 family
                                    # or with tunnel-observation also for single family
                                elif len(matched3) > (total_present_template + 1):
                                    expected_flow_seq = current_flow_seq + len(matched3)
                                    # looks like jflow is enabled for more than 1 family
                                    # make sure no tunnel-observation is enabled.
                                    # Always recommended to keep different cflow
                                    # port for different family
                            print("INFO", "Expected Flow Sequence Number %s"%expected_flow_seq)
                        else:
                            expected_flow_seq = current_flow_seq +  1
                            print("INFO", "Expected Flow Sequence Number %s"%expected_flow_seq)
                    else:
                        expected_flow_seq = current_flow_seq +  len(match_flow)
                        #Important note :- it is recommended to keep seperate cflow port for
                        # flow sequence verification
                        ############ Block below can handle ipv4/ipv6 flow-sequence together
                        #            even if clfow port and collector ip are same.
                        matched3 = re.findall(r'FlowSet Length: \d.*?Data [(]\d+ '\
                                   'bytes[)],\s+no template found', cflow, re.DOTALL)
                        if len(matched3) > 0:
                            expected_flow_seq = expected_flow_seq + len(matched3)

                elif "Template (V10 [IPFIX])" in template_type and frame_number > 1:
                    if expected_flow_seq != current_flow_seq:
                        print("INFO", "Expected flow sequence %s"%expected_flow_seq)
                        print("INFO", "Actual flow sequence %s"%current_flow_seq)
                        print("ERROR", "Flow sequence verification failed at frame %s"%cflow)
                        result = False
                        self.flow_seq_verification_status = result
                        break
                    expected_flow_seq = current_flow_seq
                elif "(Data)" in template_type and frame_number > 1:
                    if expected_flow_seq != current_flow_seq:
                        print("INFO", "Expected flow sequence %s"%expected_flow_seq)
                        print("INFO", "Actual flow sequence %"%current_flow_seq)
                        print("ERROR", "Flow sequence verification failed at frame %s"%cflow)
                        result = False
                        self.flow_seq_verification_status = result
                        break
                    match_flow = re.findall(r'Flow \d+', cflow)
                    if len(match_flow) == 0:
                        match2_list = re.findall(r'FlowSet Id: [(]Data[)] [(]\d+[)]', cflow)
                        if "FlowSet Id: (Data) (%s)"%self.option_templ_id in match2_list:
                            captured_id = self.option_templ_id
                            #if captured_id == self.temp_dict_data['option_template_scope_id']:
                            if captured_id == self.option_templ_id:
                                total_present_template = len(self.temp_dict_data) - 2
                                matched3 = re.findall(r'FlowSet Length: \d.*?Data [(]\d+ '\
                                           'bytes[)],\s+no template found', cflow, re.DOTALL)
                                if len(matched3) <= (total_present_template + 1):
                                    expected_flow_seq = current_flow_seq +  \
                                    total_present_template + 1
                                    # looks like jflow is enabled for only 1 family
                                    # or with tunnel-observation also for single family
                                elif len(matched3) > (total_present_template + 1):
                                    expected_flow_seq = current_flow_seq + len(matched3)
                                    # looks like jflow is enabled for more than 1 family
                                    # make sure no tunnel-observation is enabled.
                                    # Always recommended to keep different cflow
                                    # port for different family
                    else:
                        expected_flow_seq = current_flow_seq +  len(match_flow)
                        #Important note :- it is recommended to keep seperate cflow port for
                        # flow sequence verification
                        ############ Block below can handle ipv4/ipv6 flow-sequence together
                        #            even if clfow port and collector ip are same.
                        matched3 = re.findall(r'FlowSet Length: \d.*?Data [(]\d+ '\
                                   'bytes[)],\s+no template found', cflow, re.DOTALL)
                        if len(matched3) > 0:
                            expected_flow_seq = expected_flow_seq + len(matched3)


        if cflow_version == "9":
            frame_number = 0
            for cflow in cflow_list:
                flow_seq = re.search(r'FlowSequence: (\d+)', cflow)
                current_flow_seq = int(flow_seq.group(1))
                template_type = re.search(r'FlowSet Id: (.*)', cflow)
                template_type = template_type.group(1)
                frame_number = frame_number + 1
                if ("Template (V9)" in template_type or "Template(V9)" in template_type) \
                and frame_number == 1:
                    expected_flow_seq = current_flow_seq + 1
                    if first_flow_sequence == True:
                        if current_flow_seq == 1:
                            print("First frame flow sequence value received as 1")
                        else:
                            print("ERROR","First frame flow sequence value not received as 1")
                            return False
                elif "(Data)" in template_type and frame_number == 1:
                    expected_flow_seq = current_flow_seq +  1
                    if first_flow_sequence == True:
                        print("First frame flow sequence value received as 0 which is not expected")
                        return False
                elif ("Template (V9)" in template_type or "Template(V9)" in template_type) \
                and frame_number > 1:
                    if expected_flow_seq != current_flow_seq:
                        print("INFO", "Expected flow sequence %s"%expected_flow_seq)
                        print("INFO", "Actual flow sequence %s"%current_flow_seq)
                        print("ERROR", "Flow sequence verification failed at frame %s"%cflow)
                        result = False
                        self.flow_seq_verification_status = result
                        break
                    expected_flow_seq = current_flow_seq + 1
                elif "(Data)" in template_type and frame_number > 1:
                    if expected_flow_seq != current_flow_seq:
                        print("INFO", "Expected flow sequence %s"%expected_flow_seq)
                        print("INFO", "Actual flow sequence %s"%current_flow_seq)
                        print("ERROR", "Flow sequence verification failed at frame %s"%cflow)
                        result = False
                        self.flow_seq_verification_status = result
                        break
                    expected_flow_seq = current_flow_seq + 1

        self.flow_seq_verification_status = result
        if return_flow_sequence == 'True':
            print("INFO", "Return Flow Sequence Number %s"%current_flow_seq)
            return (result, current_flow_seq)
        return result

    def get_data_template_id_from_collector(self, **kwarg):
        fpc_slot = kwarg.get("fpc_slot", None)
        obs_id = str(int(fpc_slot) * 4)
        collector_ip_address = kwarg.get("collector_ip_address", None)
        decode_dump = kwarg.get("decode_dump", None)
        template_type = kwarg.get("template_type", None)
        data_tmpl_ids = kwarg.get("data_template_ids_list", None)
        option_tmpl_ids = kwarg.get("option_template_scope_ids_list", None)
        ## template_ids_list should be list of all template ids of particular family
        all_tmpl_received = list(decode_dump['FLOWS'][collector_ip_address][obs_id].keys())
        print("All template ids recieved at collector : ",all_tmpl_received)
        data_tmpl = None
        for tmpl in data_tmpl_ids:
            if tmpl in all_tmpl_received:
                print("INFO", "data template-id for template_type is %s" %tmpl)
                data_tmpl = tmpl
                break
        option_tmpl = None
        for tmpl in option_tmpl_ids:
            if tmpl in all_tmpl_received:
                print("INFO", "option template-id for template_type is %s" %tmpl)
                option_tmpl = tmpl
                break
        return (data_tmpl, option_tmpl)

    def get_ptx_template_ids(self, **kwarg):
        """
        output_info = kwarg.get("output_info", None)
        identifier = kwarg.get("identifier", "Option Refresh Packets")
        identifier_val = kwarg.get("identifier_val", "4800")
        template_type = kwarg.get("template_type", None)
        active_knobs = kwarg.get("active_knobs", [])
        """
        ## cmd_type=vty to be added for Scapa while calling get_ptx_template_ids
        cmd_type = kwarg.get("cmd_type", None)
        fpc_slot = kwarg.get("fpc_slot", None)
        dhandle = kwarg.get("device_handle", None)
## Below command is used in Junos based PTX
##        output_info = dhandle.shell(command="vty -s mspmand -S -c \"show log-fw template "\
##            "config summary\" fpc%s"%fpc_slot).response().replace('\r\n', '\n').strip()
## e.g. root@esst-ptx1k-b:~ # vty -s mspmand -S -c 'show log-fw template config summary' fpc0
##added
        output = dhandle.cli(command='show version | match Model').response().replace('\r\n', '\n')
        model = output.split()[-1]
        self.log("INFO", "Chassis Model is: %s" % model)
##
        #Execute below PFE cli for Brackla (ptx10003-80c or ptx10003-160c)
        if '10003' in model:
             output_info = dhandle.shell(command="cli-pfe -c \"show msvcsd "\
                 "config fpc-slot %s | no-more\""%fpc_slot).response().replace('\r\n', '\n').strip()
        #Execute below PFE cli for Scapa (ptx10008 or jnp10008)
        elif '10008' or '10001' or '10004' in model:
             output_info = dhandle.shell(command="vty -c \"show msvcsd "\
                 "config | no-more\" fpc%s"%fpc_slot).response().replace('\r\n', '\n').strip()

##        if cmd_type == 'vty':
##             output_info = dhandle.shell(command="vty -c \"show msvcsd "\
##                 "config | no-more\" fpc%s"%fpc_slot).response().replace('\r\n', '\n').strip()
##        else:
##             output_info = dhandle.shell(command="cli-pfe -c \"show msvcsd "\
##                 "config fpc-slot %s | no-more\""%fpc_slot).response().replace('\r\n', '\n').strip()
        identifier = kwarg.get("identifier", "Option Refresh Packets")
        identifier_val = kwarg.get("identifier_val", "4800")

        key_identifiers = ["Option Refresh Packets", "Option Refresh Seconds"]
        if identifier not in key_identifiers:
            print("ERROR", "Please provide identifier either as 'Option Refresh Packets'"\
                 "or 'Option Refresh Seconds'")

        if identifier == "Option Refresh Packets":
            identifier = "Refresh Packets"
        else:
            identifier = "Refresh Packets"

        output_list = re.findall(
            r'Template Id .*?AS              : \d+',
            output_info, re.DOTALL)
        output_list = output_list[::-1]
        for content in output_list:
            if "%s : %s"%(identifier, identifier_val) in content:
                last_option_id = re.search(r'Export Template Id\s+:\s(\d+)', content)
                print("INFO", self.cflow_version)
                option_templ2_id = last_option_id.group(1)
                break
        all_active_tmpl = self.get_all_active_tmpl(**kwarg)
        temp_dict_data = self.assign_tmpl_ids(option_templ2_id, all_active_tmpl,**kwarg)
        print("INFO", self.cflow_version)
        self.temp_dict_data = temp_dict_data
        return temp_dict_data

    def assign_tmpl_ids(self, option_templ2_id, all_active_tmpl,**kwarg):
        """ This nethod will assign template IDs to templates"""
        as_type_origin = kwarg.get("as_type_origin", 'True')
        as_type_peer = kwarg.get("as_type_peer", 'False')

        if as_type_origin == 'True':
            as_type_origin = True
        else:
            as_type_origin = False

        if as_type_peer == 'True':
            as_type_peer = True
        else:
            as_type_peer = False

        if as_type_origin != as_type_peer:
            tmpl_key_val = {}
            tid = int(option_templ2_id)
            for tmpl in all_active_tmpl[::-1]:
                tmpl_key_val[tmpl] = str(tid)
                tid = tid - 1
            print("INFO", self.cflow_version)
            return tmpl_key_val
        elif (as_type_origin is True) and \
             (as_type_peer is True):
            tmpl_key_val = {}
            tid = int(option_templ2_id)
            for counter, tmpl in enumerate(all_active_tmpl[::-1]):
                if counter == 0 :
                    tmpl_key_val[tmpl] = str(tid)
                    tid = tid - 2
                elif counter == 1:
                    tmpl_key_val[tmpl] = []
                    tmpl_key_val[tmpl].append(str(tid))
                    tid = tid - 1
                    tmpl_key_val[tmpl].append(str(tid))
                    tid = tid - 1
                elif counter >= 2:
                    tmpl_key_val[tmpl] = []
                    tmpl_key_val[tmpl].append(str(tid))
                    tid = tid - 1
                    tmpl_key_val[tmpl].append(str(tid))
                    tid = tid - 1
            return tmpl_key_val

    def get_all_active_tmpl(self, **kwarg):
        """ This method will find all the templates present
            on the basis of knobs used
        """
        template_type = kwarg.get("template_type", None)
        if template_type == "mpls":
            sub_tmpl = self.get_active_mpls_tmpl(**kwarg)
        if template_type == "ipv4":
            sub_tmpl = self.get_active_ipv4_tmpl(**kwarg)
        if template_type == "ipv6":
            sub_tmpl = self.get_active_ipv6_tmpl()
        print("INFO", self.cflow_version)
        return sub_tmpl

    def get_active_mpls_tmpl(self, **kwarg):
        """ This method will return template for
        Plain MPLs, MPLSV4, MPLSV6 ,MPLS-OVER-UDO """
        #template_type = "mpls"
        active_knobs = kwarg.get("active_knobs", [])
        supported_knobs = ["mpls-over-udp", "ipv4", "ipv6"]
        sub_templates = ["mpls"]
        for val in supported_knobs:
            if val in active_knobs and val == "mpls-over-udp":
                sub_templates.append("mpls-ipv4-mpls-ipv4")
                sub_templates.append("mpls-ipv4-mpls-ipv6")
            if val in active_knobs and val == "ipv4":
                sub_templates.append("mpls-ipv4")
            if val in active_knobs and val == "ipv6":
                sub_templates.append("mpls-ipv6")
        sub_templates.append("option_template_scope_id")
        for val in supported_knobs:
            if val in active_knobs and val == "ipv4":
                sub_templates.append("option_template_scope_id_ipv4")
            if val in active_knobs and val == "ipv6":
                sub_templates.append("option_template_scope_id_ipv6")
        sub_templates.append("option_system_scope_id")
        print("INFO", self.cflow_version)
        return sub_templates

    def get_active_ipv4_tmpl(self, **kwarg):
        """This method will return template for
        plain ipv4 and ipv4 with mpls-over-udp """
        #template_type = "ipv4"
        active_knobs = kwarg.get("active_knobs", [])
        supported_knobs = ["mpls-over-udp"]
        sub_templates = ["ipv4"]
        for val in supported_knobs:
            if val in active_knobs and val == "mpls-over-udp":
                sub_templates.append("ipv4-mpls-ipv4")
                sub_templates.append("ipv4-mpls-ipv6")
        sub_templates.append("option_template_scope_id")
        sub_templates.append("option_system_scope_id")
        print("INFO", self.cflow_version)
        return sub_templates

    def get_active_ipv6_tmpl(self):
        """This method will return template for
        plain ipv6 till now """
        #template_type = "ipv6"
        sub_templates = ["ipv6"]
        sub_templates.append("option_template_scope_id")
        sub_templates.append("option_system_scope_id")
        print("INFO", self.cflow_version)
        return sub_templates

    def get_mpls_details(self, **kwarg):
        """
        This method will return labels traversing through
        the core interfaces.
        """
        sampling_type = kwarg.get("sampling_type", "egress")
        dst_addr = kwarg.get("destination_address", None)
        router_details = kwarg.get("router_details", None)
        self.curr_top_label_list = []
        self.full_labels_stack = []
        for counter, rh_info in enumerate(router_details):
            if counter == 0:
                if counter == (len(router_details) -1) and\
                sampling_type == "egress":
                    rh_info['put_jflow_label'] = True
                if counter == (len(router_details) -2) and\
                sampling_type == "ingress":
                    rh_info['put_jflow_label'] = True
                label_related_info = copy.deepcopy(\
                self.get_mpls_details_via_route(destination_address =\
                dst_addr, **rh_info))
            elif counter > 0 and (counter < (len(router_details) -1)):
                if counter == (len(router_details) -2) and\
                sampling_type == "ingress":
                    rh_info['put_jflow_label'] = True
                label_related_info = self.get_mpls_info(**rh_info)
            elif counter == (len(router_details) -1):
                if sampling_type == "egress":
                    rh_info['put_jflow_label'] = True
                label_related_info = self.get_mpls_info(**rh_info)
        for count, ppath in enumerate(sorted(label_related_info)):
            if len(router_details) == 1 and sampling_type == "egress":
                label_related_info[ppath]['jflow_labels_stack'] =\
                copy.deepcopy(label_related_info[ppath]['label_stack'])
            else:
                label_related_info[ppath]['jflow_labels_stack'] =\
                self.jflow_labels_stack[count]
        self.jflow_labels_stack = []
        print("label_related_info :",label_related_info)
        return label_related_info

    def get_mpls_info(self, **rh_info):
        """ To fetch label details from core routers including
            Multipaths if configured
        """
        if len(self.curr_top_label_list) > 1:
            tlabel_list = copy.deepcopy(self.curr_top_label_list)
            full_lb_stack = copy.deepcopy(self.full_labels_stack)
            self.curr_top_label_list = []
            self.full_labels_stack = []
            label_related_info = {}
            for cnt, tlabel in enumerate(tlabel_list):
                curr_lb_stk = full_lb_stack[cnt]
                label_current_info = copy.deepcopy(\
                    self.get_mpls_details_via_label(label_value=\
                    tlabel, label_stack=curr_lb_stk, **rh_info))
                path_name = 'path' + str(int((cnt) + 1))
                label_related_info[path_name] = copy.deepcopy(\
                    label_current_info['path1'])
            if len(self.curr_top_label_list) > 0:
                curr_top_label_val = self.curr_top_label_list[-1]
                same_labels = True
                for lb in self.curr_top_label_list[:-1]:
                    if lb != curr_top_label_val:
                        same_labels = False
                        break
                if same_labels is True:
                    self.curr_top_label_list = []
                    self.curr_top_label_list.append(curr_top_label_val)
        elif len(self.curr_top_label_list) == 1:
            tlabel = self.curr_top_label_list[0]
            curr_lb_stk = self.full_labels_stack[0]
            self.curr_top_label_list = []
            self.full_labels_stack = []
            label_related_info = copy.deepcopy(\
                self.get_mpls_details_via_label(label_value=\
                tlabel, label_stack=curr_lb_stk, **rh_info))
        return label_related_info

    def get_mpls_details_via_route(self, destination_address=None, **rh_info):
        """ To fetch label details from edge routers """
        rhandle = rh_info.get("rhandle", None)
        ls_name = rh_info.get("logical-system", None)
        lsp_paths = int(rh_info.get("lsp_paths", 1))
        put_jflow_label = rh_info.get("put_jflow_label", None)
        if ls_name is None:
            rt_output = rhandle.cli(
                command="show route %s extensive active-path"% destination_address).response()
        else:
            rt_output = rhandle.cli(
                command="show route %s extensive active-path "\
                "logical-system %s"%(destination_address, ls_name)).response()
        vpn_label = re.search(r'VPN Label: (\d+)', rt_output)
        if vpn_label:
            vpn_label = vpn_label.group(1)
        else:
            vpn_label = None

        path_info = {}
        label_found = re.findall(r'Label operation: Push\s+\d+,\s+Push\s+\d+[(]top[)]',\
        rt_output)
        push2_found = re.search(r'Label operation: Push\s+2,\s+Push\s+\d+[(]top[)]',\
        rt_output)
        nh_oif_list = re.findall(r'Next hop: (?:.*) via (?:.*[.]\d+)', rt_output)
        if label_found:
            pass
        else:
            label_present = re.findall(r'Label operation: Push\s+(?:\d+)', rt_output)
        for act_pth in range(lsp_paths):
            path_name = 'path' + str(int((act_pth) + 1))
            label_stack = []
            if len(label_found) > 0:
                top_label = re.search(r'Label operation: Push\s+\d+,\s+Push\s+(\d+)[(]top[)]',\
                label_found[act_pth])
                top_label = top_label.group(1)
            else:
                top_label = re.search(r'Label operation: Push\s+(\d+)', label_present[act_pth])
                top_label = top_label.group(1)
            nh_oif = re.search(r'Next hop: (.*) via (.*[.]\d+)', nh_oif_list[act_pth])
            nh = nh_oif.group(1)
            oif = nh_oif.group(2)
            output_snmp_index = self.get_snmp_index_value(
                dhandle=rhandle, interface=oif)
            path_info[path_name] = {}
            path_info[path_name]['oif_interface'] = oif
            path_info[path_name]['output_snmp_index'] = output_snmp_index
            path_info[path_name]['nexthop'] = nh
            path_info[path_name]['top_label'] = top_label
            path_info[path_name]['vpn_label'] = vpn_label
            if vpn_label is not None:
                label_stack.append(vpn_label)
            elif push2_found:
                label_stack.append(str(2))
            else:
                label_stack.append(str(0))
            label_stack.append(top_label)
            path_info[path_name]['label_stack'] = label_stack
            self.curr_top_label_list.append(top_label)
            self.full_labels_stack.append(copy.deepcopy(label_stack))
            if put_jflow_label is True:
                self.jflow_labels_stack.append(copy.deepcopy(label_stack))
        return path_info

    def get_mpls_details_via_label(self, label_value=None, label_stack=None, **rh_info):
        """ To fetch label details from core routers """
        rhandle = rh_info.get("rhandle", None)
        ls_name = rh_info.get("logical-system", None)
        lsp_paths = int(rh_info.get("lsp_paths", 1))
        put_jflow_label = rh_info.get("put_jflow_label", None)
        if ls_name is None:
            rt_output = rhandle.cli(
                command="show route label %s extensive active-path"% label_value).response()
        else:
            rt_output = rhandle.cli(
                command="show route label %s extensive active-path "\
                "logical-system %s"%(label_value, ls_name)).response()
        path_info = {}
        push_swap_action = None
        swap_action = None
        push_action = None
        pop_action = None

        pop_found = re.findall(r' Label operation:\s+Pop', rt_output)
        if len(pop_found) == 0:
            push_swap_found = re.findall(r'Label operation:\s+Swap\s+\d+,\s+Push\s+\d+[(]top[)]', rt_output)
            if len(push_swap_found) == 0:
                swap_found = re.findall(r'Label operation:\s+Swap\s+\d+', rt_output)
                push_found = re.findall(r'Label operation:\s+Push\s+\d+', rt_output)
                if len(swap_found) > 0 and len(push_found) > 0:
                    print("INFO", "LABEL FIRSTLY SWAPPED AND NEW TOP LABEL IS PUSHED")
                    push_swap_action = False
                    push_action = True
                    swap_action = True
                elif len(swap_found) > 0 and len(push_found) == 0:
                    print("INFO", "LABEL SWAPPED")
                    push_swap_action = False
                    swap_action = True
                    push_action = False
            elif len(push_swap_found) > 0:
                push_swap_action = True
                swap_action = False
                push_action = False
        else:
            pop_action = True

        for act_pth in range(lsp_paths):
            path_name = 'path' + str(int((act_pth) + 1))
            label_stack_cp = copy.deepcopy(label_stack)
            if pop_action is True:
                label_stack_cp.pop()
            elif push_swap_action is True:
                push_swap_labels = re.search(r'Label operation:\s+Swap\s+(\d+),\s+Push\s+(\d+)[(]top[)]', push_swap_found[act_pth])
                swap_label = push_swap_labels.group(1)
                top_label = push_swap_labels.group(2)
                label_stack_cp.pop()
                label_stack_cp.append(swap_label)
                label_stack_cp.append(top_label)
            elif push_action is True and swap_action is True:
                swap_label = re.search(r'Label operation:\s+Swap\s+(\d+)', swap_found[act_pth])
                swap_label = swap_label.group(1)
                top_label = re.search(r'Label operation:\s+Push\s+(\d+)', push_found[act_pth])
                top_label = top_label.group(1)
                label_stack_cp.pop()
                label_stack_cp.append(swap_label)
                label_stack_cp.append(top_label)
            elif push_action is False and swap_action is True:
                swap_label = re.search(r'Label operation:\s+Swap\s+(\d+)', swap_found[act_pth])
                swap_label = swap_label.group(1)
                label_stack_cp.pop()
                label_stack_cp.append(swap_label)
            nh_oif_list = re.findall(r'Next hop: (?:.*) via (?:.*[.]\d+)', rt_output)
            nh_oif = re.search(r'Next hop: (.*) via (.*[.]\d+)', nh_oif_list[act_pth])
            nh = nh_oif.group(1)
            oif = nh_oif.group(2)
            output_snmp_index = self.get_snmp_index_value(
                dhandle=rhandle, interface=oif)
            path_info[path_name] = {}
            path_info[path_name]['oif_interface'] = oif
            path_info[path_name]['output_snmp_index'] = output_snmp_index
            path_info[path_name]['nexthop'] = nh
            path_info[path_name]['top_label'] = label_stack_cp[-1]
            path_info[path_name]['label_stack'] = label_stack_cp
            self.curr_top_label_list.append(label_stack_cp[-1])
            self.full_labels_stack.append(copy.deepcopy(label_stack_cp))
            if put_jflow_label is True:
                self.jflow_labels_stack.append(copy.deepcopy(label_stack_cp))
            if pop_action is True:
                return path_info
        return path_info

    def get_vpn_label(self, **kwarg):
        """ This method returns VPN label """
        rhandle = kwarg.get("rhandle", None)
        ls_name = kwarg.get("logical-system", None)
        destination_address = kwarg.get("destination_address", None)
        if ls_name is None:
            rt_output = rhandle.cli(
                command="show route %s extensive active-path"% destination_address).response()
        else:
            rt_output = rhandle.cli(
                command="show route %s extensive active-path "\
                "logical-system %s"%(destination_address, ls_name)).response()
        vpn_label = re.search(r'VPN Label: (\d+)', rt_output)
        if vpn_label:
            vpn_label = vpn_label.group(1)
        else:
            vpn_label = None
        return vpn_label

    def get_lsi_snmp_index(self, **kwarg):
        """ This method returns VPN label """
        rhandle = kwarg.get("rhandle", None)
        ls_name = kwarg.get("logical-system", None)
        label = kwarg.get("label", None)
        vrf_name = kwarg.get("vrf_name", None)
        if ls_name is None:
            rt_output = rhandle.cli(
                command="show route label %s extensive active-path"%label).response()
        else:
            rt_output = rhandle.cli(
                command="show route label %s extensive active-path "\
                "logical-system %s"%(label, ls_name)).response()
        lsi_if = re.search(r'Next hop: via lsi.(\d+) [(]%s[)], selected'%vrf_name, rt_output)
        if lsi_if:
            lsi_intf = 'lsi.' + lsi_if.group(1)
            lsi_snmp_index = self.get_snmp_index_value(
                dhandle=rhandle, interface=lsi_intf)
        else:
            lsi_snmp_index = None
        return lsi_snmp_index

    def verify_dscp_value_at_collector(self, **kwg):
        """
        This method will perform the flow sequence verification per observation domain

        :return: True if verification succeed per observation domain id else False

        :rtype: bool


        Example::

            python:
                obj.init( PASS ALL MANATORY PARAMETERS MENTIONED IN init)
                status = obj.verify_flow_sequence()
            Robot:
                ${status}=    Jf.Verify Flow Sequence
                Should Be True     ${status}
        """
        result = None
        expected_dscp_value = kwg.get("expected_dscp_value", 0)
        ifile = self.tshark_output
        #cfl = re.findall(r'(Frame \d+: \d+ bytes on wire.*?Explicit Congestion Notification:)', ifile, re.DOTALL)
        cfl = re.findall(r'(Frame \d+: \d+ bytes on wire.*?User Datagram Protocol, Src Port)', ifile, re.DOTALL)
        for pkt in cfl:
            dscp_match = re.search(r'Differentiated Services Codepoint: .* [(](\d+)[)]',pkt)
            dscp_match_hex = re.search(r'Differentiated Services Codepoint: .* [(]0x(..)[)]',pkt)
            dscp_match_hex2 = re.search(r'Differentiated Services Codepoint: .* [(]0x(........)[)]',pkt)
            dscp_match_hex3 = re.search(r'Differentiated Services Field: .* [(]0x(........)[)]',pkt)
            if dscp_match:
                actual_dscp_value = dscp_match.group(1)
                print("Actual DSCP value:",actual_dscp_value)
                if int(actual_dscp_value) != int(expected_dscp_value):
                    print("DSCP value didn't match with expected value")
                    result = False
                    break
                else:
                    result = True
            elif dscp_match_hex:
                actual_dscp_value = dscp_match_hex.group(1)
                if int(actual_dscp_value, 16) != int(expected_dscp_value):
                    print("DSCP value didn't match with expected value")
                    result = False
                    break
                else:
                    result = True
            elif dscp_match_hex2:
                actual_dscp_value = dscp_match_hex2.group(1)
                if int(actual_dscp_value, 16) != int(expected_dscp_value):
                    print("DSCP value didn't match with expected value")
                    result = False
                    break
                else:
                    result = True
            elif dscp_match_hex3:
                actual_dscp_value = dscp_match_hex3.group(1)
                if int(actual_dscp_value, 16) != int(expected_dscp_value):
                    print("DSCP value didn't match with expected value")
                    result = False
                    break
                else:
                    result = True
            else:
                print("Differentiated Services Codepoint not found")
                result = False
                break
        self.dscp_value_verification_status = result
        return result

    def get_sampling_instance_id(self, **kwarg):
        """
        This method will fetch sampling instance id from vty
        """
        fpc_slot = kwarg.get("fpc_slot", None)
        dhandle = kwarg.get("device_handle", None)
        instance_name = kwarg.get("sampling_instance_name", None)
        output_info = dhandle.shell(command="vty -S -c \"show sample instance "\
            "summary\" fpc%s"%fpc_slot).response().replace('\r\n', '\n').strip()
        for lines in output_info.splitlines():
            if (instance_name in lines) and ("Ref-Inst" not in lines):
                get_data = lines.split()
                sampling_instance_id = get_data[0]
                break
        return sampling_instance_id


    def get_template_record_verification_status(self):
        """ return template_record_verification_status """
        return self.tmpl_verify_stat

    def get_flow_sequence_verification_status(self):
        """ return flow_sequence_verification_status """
        return self.flow_seq_verification_status

    def get_template_refresh_rate_verification_status(self):
        """ return template_refresh_rate_verification_status """
        return self.template_refresh_rate_status

    def get_dscp_verification_status(self):
        """ return dscp_verification_status """
        return self.dscp_value_verification_status

    def get_option_data_template_scope_verification_status(self):
        """ returns option_data_verification_status """
        return self.option_data_template_scope_verify_status

    def get_option_data_system_scope_verification_status(self):
        """ returns option_data_verification_status """
        return self.option_data_system_scope_verify_status

    def get_data_record_verification_status(self):
        """ return data_record_verification_status """
        return self.data_record_status

    def create_instance(self):
        """ method to create instance of
            of class "evo_jflow_verification"
        """
        self.objj = evo_jflow_verification()
        #s1.init( **kwargs)
        return self.objj

    def start_jflow_verification_threads(self, *verification_list):
        """ This method accepts multiple object
            and required parameters to initiate
            multi-threading.
        """
        # Empty thread list
        th = []
        t.set_background_logger()
        for v_dict in verification_list:
            th.append(jflow_verify_thread(**v_dict))

        for thread in th:
            thread.start()

        for thread in th:
            thread.join()
        t.process_background_logger()

    def get_jflow_template_version(self):
        """This method will find jflow version like 15.1 , 18.1 and so on

           It will be called internally while calling init function

        :return: string value fro the jflow template version

        :rtype: string

        """

        if self.platform == 'QFX' and self.jflow_type == 'INLINE':
            output = self.dhandle.cli(
                command='show services inline-jflow template-version | '\
                'match \"Internal modified EVO Inline Jflow Template '\
                'Version:\"').response().replace('\r\n', '\n')
            matched = re.search(r'Internal modified EVO Inline Jflow '\
                'Template Version:\s+(\d{2}[.]\w+)', output)
            qfx_jflow_template_version = matched.group(1)
            return qfx_jflow_template_version

        elif self.platform == 'PTX' and self.jflow_type == 'INLINE':
            output = self.dhandle.cli(
                command='show services inline-jflow template-version | '\
                'match \"Internal modified EVO Inline Jflow Template '\
                'Version:\"').response().replace('\r\n', '\n')
            matched = re.search(r'Internal modified EVO Inline Jflow '\
                'Template Version:\s+(\d{2}[.]\w+)', output)
            ptx_jflow_template_version = matched.group(1)
            return ptx_jflow_template_version


class jflow_verify_thread(threading.Thread):
    """ This class performs jflow verification \
        using multi-threading approach
    """
    def __init__(self, **kwargs):
        """ Initiating the constructor """
        threading.Thread.__init__(self)
        self.obj = kwargs["object_reference"]
        self.call_init = False
        self.verify_template_refresh_rates = False
        self.verify_the_flow_sequence = False
        self.verify_the_option_data = False
        self.verify_the_option_data_template_scope = False
        self.verify_the_option_data_system_scope = False
        self.verify_the_dsp_value_at_collector = False
        self.verify_the_template_records = False

        if "init" in kwargs:
            self.call_init = True
            self.dict_to_call_init = kwargs["init"]

        if "verify_template_refresh_rates" in kwargs:
            self.verify_template_refresh_rates = True
            self.dict_to_verify_template_refresh_rate = kwargs['verify_template_refresh_rates']

        if "verify_flow_sequence" in kwargs:
            self.verify_the_flow_sequence = True
            #self.dict_to_verify_flow_sequence = kwargs.get("verify_flow_sequence",{})

        if "verify_template_records" in kwargs:
            self.verify_the_template_records = True

        if "verify_option_data_system_scope" in kwargs:
            self.verify_the_option_data_system_scope = True
            self.dict_to_verify_option_data_system_scope = kwargs['verify_option_data_system_scope']

        if "verify_option_data_template_scope" in kwargs:
            self.verify_the_option_data_template_scope = True
            self.dict_to_verify_option_data_template_scope = kwargs['verify_option_data_template_scope']

        if "verify_data_records" in kwargs:
            self.verify_the_data_records = True
            self.dict_to_verify_data_records = kwargs['verify_data_records']

        if "verify_dsp_value_at_collector" in kwargs:
            self.verify_the_dsp_value_at_collector = True
            self.expected_dscp_val = kwargs['verify_dsp_value_at_collector']

    def run(self):
        """ Method to start threads"""
        if self.call_init is True:
            self.obj.init( **self.dict_to_call_init)

        if self.verify_template_refresh_rates is True:
            self.obj.verify_templates_timestamps_and_refresh_rate(**self.dict_to_verify_template_refresh_rate)

        if self.verify_the_flow_sequence is True:
            self.obj.verify_flow_sequence()

        if self.verify_the_template_records is True:
            self.obj.verify_template_record()

        if self.verify_the_option_data_system_scope is True:
            self.obj.verify_option_data_record(**self.dict_to_verify_option_data_system_scope)

        if self.verify_the_option_data_template_scope is True:
            self.obj.verify_option_data_record(**self.dict_to_verify_option_data_template_scope)

        if self.verify_the_dsp_value_at_collector is True:
            self.obj.verify_dscp_value_at_collector(**self.expected_dscp_val)

        if self.verify_the_data_records is True:
            self.obj.verify_data_record(**self.dict_to_verify_data_records)


#class instances(object):
#    def __init__(self):
#        self.objj = None
#
#    def create_instance(self):
#        self.objj = evo_jflow_verification()
#        #s1.init( **kwargs)
#        return self.objj
#
#    def start_jflow_verification_threads(self, *verification_list):
#        # Empty thread list
#        th = []
#        t.set_background_logger()
#        for v_dict in verification_list:
#            th.append(jflow_verify_thread(**v_dict))
#
#        for thread in th:
#            thread.start()
#
#        for thread in th:
#            thread.join()
#        t.process_background_logger()