#!/usr/bin/python3

"""
This module contains API's for Jflow verification

__author__ = [''Sandeep Rai']
__contact__ = 'rais@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

"""
import threading
import re
import copy
import itertools
import ipaddress
import jnpr.toby.utils.iputils as iputils
import jnpr.toby.services.rutils as rutils
from jnpr.toby.services import utils

class jflow_verification(object):
    """
    Class for the verification of the exported DATA TEMPLATE, OPTION TEMPLATE, \
    DATA RECORD and OPTION DATA
    """

    def __init__(self):
        """
         Constructor to initialize all the attributes to None
        """
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
        self.sampling_obs_dmn_ids = None
        self.decode_dump_with_flow_selectors = None
        self.data_template_dict = None
        self.option_template_dict = None
        self.data_templ_id = None
        self.option_templ_id = None
        self.expected_datatemp_pktflowset = None
        self.expected_optiontemp_pktflowset = None
        self.expected_data_pkt_flowset_name = None
        self.exp_optionpkt_flowset = None
        self.default_option_pktname = None
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
        self.log = utils.log
        self.template_refresh_rate = None
        self.option_refresh_rate = None
        self.data_record_status = None
        self.flow_seq_verification_status = None
        self.template_refresh_rate_status = None
        self.final_flow_seq_status = None
        self.dscp_value_verification_status = None        
        self.tmpl_verify_stat = None
        self.option_data_verify_status = None
        self.vpn_label = None

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

        | And upon receiving mandatory parameters and device handle ,
        | these parameter will be verified :-
        | - platform
        | - jflow_template_version
        | - template_family_details
        | - obs_dmn_ids (observation domain Id or Source Id)
        | - sampling_obs_dmn_ids (Sampling observation domain Id or Source Id)
        | - data_template_dict (Expected Data Template saved in dictionary format)
        | - option_template_dict (Expected Option Template saved in dictionary format)

        Please refer to documentation of corresponding APIs for more details.

        :param obj device_handle
            **REQUIRED** device handle of the router where sampling is performed

        :param string template_type
            **REQUIRED** template type defined for the samling applied on router.
                         currently Supported Values - ipv4, ipv6, mpls, mpls-v4, vpls

        :param string sampling_interface
            **REQUIRED** Interface on which sampling has been applied.

        :param list flow_colls
            **REQUIRED** collectors IP ADDRESSES to be passed as list

        :param string tshark_output
            **REQUIRED** tshark decoded output for the pcap file decoded at collector.

        :param string cflow_version
            **REQUIRED** version type for the sampling enabled .
                         supported values :- 9 for version9  or 10 for version-ipfix

        :param dict decode_dump_with_flow_selectors
            **REQUIRED** It is a dictionary which contain 2 keys:-
                         1. 'decode_dump'

                            - It's primarily a tshark output decoded in python's dictionary using
                              method name "decode_jflow_dump_on_all_col_ports" present in module
                             "decode_jflow_dump.py" .

                         2. 'flow_selector_identifier_info'

                            - The value for key 'flow_selector_identifier_info' should be \
                              a List of Dictionaries \
                              And key inside those dictionaries corresponds to \
                              the "flow selectors" used to uniquely \
                              decode the tshark output in python dictionary using method \
                              "decode_jflow_dump_on_all_col_ports" present in module \
                              "decode_jflow_dump.py" . \
                              And Value of respective keys will be list of strings.

                         Suppose for a test, \
                         user created the flows by varying only Source IP Address and \
                         and Source port while keeping Protocol, Destination Addrress and \
                         Destination port constant
                         SrcAddr - [ '70.0.0.1' , '70.0.0.2']
                         SrcPort - [ '12000' , '12001']

                         Flow 1  - 70.0.0.1 : 12000
                         Flow 2  - 70.0.0.1 : 12001
                         Flow 3  - 70.0.0.2 : 12000
                         Flow 4  - 70.0.0.2 : 12001
                         Above flows looks like cartesian product of SrcAddr and SrcPort


                         To uniquely decode the export records for above flows, \
                         user will decode using

                         flow_selectors = ['SrcAddr' , 'SrcPort']
                         to uniquely decode the tshark output in
                         python dictionary while calling method "decode_jflow_dump_on_all_col_ports"
                         present in module "decode_jflow_dump.py" .
                         please refer module "decode_jflow_dump.py" for more info.

                         So how actually 'the decode_dump_with_flow_selectors' should be :-

                         decode_dump_with_flow_selectors =
                           {'decode_dump' : decode_dict,
                            'flow_selector_identifier_info': [{'SrcAddr': ['70.0.0.1', '70.0.0.2']},
                                                               {'SrcPort' : [ '12000' , '12001']}]}
                               Where "decode_dict" is the tshark decoded output in python's \
                               dictionary format retrieved by calling \
                               "decode_jflow_dump_on_all_col_ports" present in module \
                               "decode_jflow_dump.py".

        :param string configured_observation_domain_id
            **OPTIONAL** If user has configured the observation domain  id on
                         the device then user must provide the value
                         while calling this method

        :param string configured_template_id
            **OPTIONAL** If user has configured the data template id on the device then
                         then user can pass that value using key "configured_template_id"

        :param string configured_option_template_id
            **OPTIONAL** If user has configured the data template id on the device then
                         then user can pass that value using key "configured_option_template_id"

        :return: None if all command executed correctly else raises an exception

        :rtype: None or exception

        Sample Robot file with jflow_verification APIs::

            *** Settings ***
                Library     jnpr/toby/services/jflow/decode_jflow_dump.py   WITH NAME    Dj
                Library     jnpr/toby/services/jflow/jflow_verification.py  WITH NAME    Jf

            *** Keywords ***
            Global
                Initialize

            *** Test Cases ***

            Testcase Verify_Jflow - Validating the export records
            @{selector_list}=   Create list     SrcAddr    SrcPort
            @{srcport_list}=    Jf.get_port_list     initial_port_number=12000    count=2
            ${decode_dump} =    Dj.Decode Jflow Dump On All Col Ports  device=${collector_h2}
                tcpdump_file=${dump_file}   tcpdump_decode_file=${dump_decode_file}
                cflow_port=${cflow_port}       tethereal="/usr/bin/tshark"
                flow_selectors=@{selector_list}
            ${tcpdump_start_time}    ${tcpdump_stop_time}=    Dj.Get Tcpdump Start And End Time
            ${tshark_output} =    Dj.Get Tshark Output
            @{src_ips_as_list}=    Jf.Get Ip Sequence In List     initial_ip=7000::1    count=10
            ${decode_dump_with_flow_selectors}=      Evaluate    {'decode_dump':${decode_dump},
                'flow_selector_identifier_info' : [{ 'SrcAddr' : ${src_ips_as_list}}]}
            Jf.Init    device_handle=${dh_r0}     cflow_version=9
                       template_type=${template_type}     sampling_interface=${ifn}
                       decode_dump_with_flow_selectors=${decode_dump_with_flow_selectors}
                       flow_colls=${flow_colls}     tshark_output=${tshark_output}
            ${template_timestamp_status}=    Jf.Verify Templates Timestamps And Refresh Rate
                template_refresh_rate=10     option_refresh_rate=30
                tcpdump_start_time=${tcpdump_start_time}  tcpdump_stop_time=${tcpdump_stop_time}
            Should Be True    ${template_timestamp_status}
            ${flow_seq_status}=    Jf.Verify Flow Sequence
            Should Be True    ${flow_seq_status}
            ${temp_status}=    Jf.Verify Template Record
            Should Be True    ${temp_status}
            ${expected_pdu_dict} =  Evaluate  {'DstAddr':'8000::4', 'DstPort':'1001',
               'TCP Flags':'0x00', 'IP ToS':'0x00', 'Dot1q Customer Vlan Id':'0',
               'MaxTTL':'64' , 'MinTTL':'64' , 'IPv4Ident':'0' , 'Direction': 'Ingress (0)',
               'Flow End Reason': 'Active timeout (2)' , 'Protocol': '17' ,, 'SrcPort':'12000',}
            ${data_status}=    Jf.Verify Data Record    expected_pdu_dict=${expected_pdu_dict}
            Should Be True    ${data_status}
        """
        self.cflow_version = kwarg.get('cflow_version', None)
        self.template_type = kwarg.get('template_type', None)
        self.sampling_interface = kwarg.get('sampling_interface', None)
        self.flow_colls = kwarg.get('flow_colls', None)
        self.tshark_output = kwarg.get('tshark_output', None)
        self.jflow_type = kwarg.get('jflow_type', 'INLINE')
        self.dhandle = device_handle
        self.platform = self.get_chassis_platform_info()
        self.jflow_template_version = self.get_jflow_template_version()
        configured_obs_domainid = kwarg.get('configured_observation_domain_id', '0')
        self.template_family_details = self.get_expected_template_details(**kwarg)
        self.obs_dmn_ids = self.get_all_observation_domain_ids(
            device_handle=self.dhandle, configured_obs_domainid=
            configured_obs_domainid)
        self.sampling_obs_dmn_ids = self.get_sampling_observation_domain_id(
            device_handle=self.dhandle, configured_obs_domainid=
            configured_obs_domainid)
        decode_dump_with_flow_selectors = kwarg.get('decode_dump_with_flow_selectors', {})
        self.decode_dump_with_flow_selectors = decode_dump_with_flow_selectors
        self.template_refresh_rate = kwarg.get('template_refresh_rate', None)
        self.option_refresh_rate = kwarg.get('option_refresh_rate', None)
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

    def get_expected_template_details(self, **kwarg):
        """This method will check the type of platform of router and
           will retrieve the required detail which will be saved in dict
           data structure.

        :param string configured_template_id
            **OPTIONAL** If user has configured the data template id on the device then \
                         then user can pass that value using key "configured_template_id"

        :param string configured_option_template_id
            **OPTIONAL** If user has configured the data template id on the device then \
                         then user can pass that value using key "configured_option_template_id"

        :return: dictionary type contain relevant detail related to template ID , Option
                 template ID , Flowset Name and default template ID value .

        :rtype: dict

        Example::

            python:
                Jf.get_expected_template_details()
            Robot:
                Jf.Get Expected Template Details
                    Or
                Jf.Get Expected Template Details     configured_template_id = 24999
                                                     configured_option_template_id = 24999
        """
        if self.platform == 'MX':
            mx_template_relevant_details = self.get_mx_template_details(
                **kwarg)
            return mx_template_relevant_details

    def get_mx_template_details(self, **kwarg):
        """This method will retrieve the required detail template IDs and flow_set names
          for  "MX platform" which will be saved in dict data structure.

        :param string configured_template_id
            **OPTIONAL** If user has configured the data template id on the device then \
                         then user can pass that value using key "configured_template_id"

        :param string configured_option_template_id
            **OPTIONAL** If user has configured the data template id on the device then \
                         then user can pass that value using key "configured_option_template_id"

        :return: dictionary type contain relevant detail related to template ID , Option
                 template ID , Flowset Name and default template ID value .

        :rtype: dict

        Example::

            python:
                Jf.get_expected_template_details()
            Robot:
                Jf.Get Expected Template Details
                    Or
                Jf.Get Expected Template Details     configured_template_id = 24999
                                                     configured_option_template_id = 24999
        """
        if self.template_type == 'ipv4' and self.cflow_version == '9' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '320')
            configured_option_template_id = kwarg.get('configured_option_template_id', '576')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V9) (0)'
            self.expected_optiontemp_pktflowset = 'Options Template(V9) (1)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (576)'

        elif self.template_type == 'ipv4' and self.cflow_version == '10' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '256')
            configured_option_template_id = kwarg.get('configured_option_template_id', '512')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V10 [IPFIX]) (2)'
            self.expected_optiontemp_pktflowset = 'Options Template (V10 [IPFIX]) (3)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (512)'

        elif self.template_type == 'ipv6' and self.cflow_version == '9' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '321')
            configured_option_template_id = kwarg.get('configured_option_template_id', '577')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V9) (0)'
            self.expected_optiontemp_pktflowset = 'Options Template(V9) (1)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (577)'

        elif self.template_type == 'ipv6' and self.cflow_version == '10' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '257')
            configured_option_template_id = kwarg.get('configured_option_template_id', '513')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V10 [IPFIX]) (2)'
            self.expected_optiontemp_pktflowset = 'Options Template (V10 [IPFIX]) (3)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (513)'

        elif self.template_type == 'vpls' and self.cflow_version == '9' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '322')
            configured_option_template_id = kwarg.get('configured_option_template_id', '578')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V9) (0)'
            self.expected_optiontemp_pktflowset = 'Options Template(V9) (1)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (578)'

        elif self.template_type == 'vpls' and self.cflow_version == '10' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '258')
            configured_option_template_id = kwarg.get('configured_option_template_id', '514')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V10 [IPFIX]) (2)'
            self.expected_optiontemp_pktflowset = 'Options Template (V10 [IPFIX]) (3)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (514)'

        elif self.template_type == 'mpls' and self.cflow_version == '9' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '323')
            configured_option_template_id = kwarg.get('configured_option_template_id', '579')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V9) (0)'
            self.expected_optiontemp_pktflowset = 'Options Template(V9) (1)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (579)'

        elif self.template_type == 'mpls' and self.cflow_version == '10' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '259')
            configured_option_template_id = kwarg.get('configured_option_template_id', '515')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V10 [IPFIX]) (2)'
            self.expected_optiontemp_pktflowset = 'Options Template (V10 [IPFIX]) (3)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (515)'

        elif (self.template_type == 'mpls-v4' or self.template_type == 'mpls-ipv4') \
        and self.cflow_version == '9' \
        and self.jflow_type == 'INLINE':
            self.template_type = 'mpls-ipv4'
            configured_template_id = kwarg.get('configured_template_id', '324')
            configured_option_template_id = kwarg.get('configured_option_template_id', '580')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V9) (0)'
            self.expected_optiontemp_pktflowset = 'Options Template(V9) (1)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (580)'

        elif (self.template_type == 'mpls-v4' or self.template_type == 'mpls-ipv4') \
        and self.cflow_version == '10' \
        and self.jflow_type == 'INLINE':
            self.template_type = 'mpls-ipv4'
            configured_template_id = kwarg.get('configured_template_id', '260')
            configured_option_template_id = kwarg.get('configured_option_template_id', '516')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V10 [IPFIX]) (2)'
            self.expected_optiontemp_pktflowset = 'Options Template (V10 [IPFIX]) (3)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (516)'

        elif self.template_type == 'bridge' and self.cflow_version == '9' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '326')
            configured_option_template_id = kwarg.get('configured_option_template_id', '582')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V9) (0)'
            self.expected_optiontemp_pktflowset = 'Options Template(V9) (1)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (582)'

        elif self.template_type == 'bridge' and self.cflow_version == '10' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '262')
            configured_option_template_id = kwarg.get('configured_option_template_id', '518')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V10 [IPFIX]) (2)'
            self.expected_optiontemp_pktflowset = 'Options Template (V10 [IPFIX]) (3)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (518)'

        if self.template_type == 'mpls-ipv6' and self.cflow_version == '9' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '327')
            configured_option_template_id = kwarg.get('configured_option_template_id', '583')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V9) (0)'
            self.expected_optiontemp_pktflowset = 'Options Template(V9) (1)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (583)'

        elif self.template_type == 'mpls-ipv6' and self.cflow_version == '10' \
        and self.jflow_type == 'INLINE':
            configured_template_id = kwarg.get('configured_template_id', '263')
            configured_option_template_id = kwarg.get('configured_option_template_id', '519')
            self.data_templ_id = configured_template_id
            self.option_templ_id = configured_option_template_id
            self.expected_datatemp_pktflowset = 'Data Template (V10 [IPFIX]) (2)'
            self.expected_optiontemp_pktflowset = 'Options Template (V10 [IPFIX]) (3)'
            self.expected_data_pkt_flowset_name = '(Data) (%s)' % configured_template_id
            self.exp_optionpkt_flowset = '(Data) (%s)' % configured_option_template_id
            self.default_option_pktname = '(Data) (519)'


        mx_templ_details = {}
        mx_templ_details['data_templ_id'] = self.data_templ_id
        mx_templ_details['option_templ_id'] = self.option_templ_id
        mx_templ_details['expected_data_template_pkt_flowset_name'] = \
            self.expected_datatemp_pktflowset
        mx_templ_details['expected_option_template_pkt_flowset_name'] = \
            self.expected_optiontemp_pktflowset
        mx_templ_details['expected_data_pkt_flowset_name'] = \
            self.expected_data_pkt_flowset_name
        mx_templ_details['expected_option_pkt_flowset_name'] = \
            self.exp_optionpkt_flowset
        return mx_templ_details

        #self.verify_type = 'OPTIONS_V9_INLINE'
        #self.expected_template_pkt_type = 'Options Template(V9) (1)'
        #self.verify_type = 'OPTIONS_IPFIX_INLINE'

    def get_chassis_platform_info(self):
        """
         This method will get the platform of router on
         which sampling is applied.

        :return: String type , Values can be 'MX', 'mx'

        :rtype: string

        """

        output = self.dhandle.cli(
            command='show chassis hardware | match chassis').response().replace('\r\n', '\n')
        hardware_info = output.split()[-1]
        if 'MX' in hardware_info or 'mx' in hardware_info:
            return 'MX'
        elif 'PTX' in hardware_info or 'ptx' in hardware_info:
            return 'PTX'

    def get_jflow_template_version(self):
        """This method will find jflow version like 15.1 , 18.1 and so on

           It will be called internally while calling init function

        :return: string value fro the jflow template version

        :rtype: string

        """

        if self.platform == 'MX' and self.jflow_type == 'INLINE':
            output = self.dhandle.cli(
                command='show services inline-jflow template-version | '\
                'match \"Internal modified Template Version:\"').response().replace('\r\n', '\n')
            matched = re.search(r'Internal modified Template Version:\s+(\d{2}[.]\d)\d?', output)
            mx_jflow_template_version = matched.group(1)
            return mx_jflow_template_version

        elif self.platform == 'PTX' and self.jflow_type == 'INLINE':
            output = self.dhandle.cli(
                command='show services inline-jflow template-version | '\
                'match \"Internal modified PTX Inline Jflow Template '\
                'Version:\"').response().replace('\r\n', '\n')
            matched = re.search(r'Internal modified PTX Inline Jflow '\
                'Template Version:\s+(\d{2}[.]\w+)', output)
            ptx_jflow_template_version = matched.group(1)
            return ptx_jflow_template_version

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
        if self.platform == 'MX' and self.jflow_template_version == '15.1' and \
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            return template_dict

        if self.platform == 'MX' and self.jflow_template_version == '15.1' \
        and self.cflow_version == '9' \
        and self.template_type == 'ipv4' and self.jflow_type == 'INLINE':
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['18.1', '18.3', '19.2']) \
        and self.cflow_version == '10' \
        and self.template_type == 'ipv4' and self.jflow_type == 'INLINE':
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['18.1', '18.3', '19.2']) \
        and self.cflow_version == '9' \
        and self.template_type == 'ipv4' and self.jflow_type == 'INLINE':
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['15.1', '18.1', '18.3']) \
        and self.cflow_version == '10' and self.template_type == 'ipv6' and \
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IPV6_OPTION_HEADERS'] = {
                'Length': '4', 'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64'}
            return template_dict

        if self.platform == 'MX' and (self.jflow_template_version in ['19.2']) \
        and self.cflow_version == '10' and self.template_type == 'ipv6' and \
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['BGP_IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'BGP_IPV6_NEXT_HOP', 'Element_id': '63'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IPV6_OPTION_HEADERS'] = {
                'Length': '4', 'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64'}
            return template_dict


        if self.platform == 'MX' and (self.jflow_template_version in ['18.1', '18.3']) \
        and self.cflow_version == '9' \
        and self.template_type == 'ipv6' and self.jflow_type == 'INLINE':
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IPV6_OPTION_HEADERS'] = {
                'Length': '4', 'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64'}
            return template_dict


        if self.platform == 'MX' and (self.jflow_template_version in ['19.2']) \
        and self.cflow_version == '9' \
        and self.template_type == 'ipv6' and self.jflow_type == 'INLINE':
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['BGP_IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'BGP_IPV6_NEXT_HOP', 'Element_id': '63'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IPV6_OPTION_HEADERS'] = {
                'Length': '4', 'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64'}
            return template_dict


        if self.platform == 'MX' and \
        self.jflow_template_version in ['15.1', '18.1', '18.3', '19.2'] \
        and self.cflow_version == '10' and self.template_type == 'mpls' and \
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
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            return template_dict

        if self.platform == 'MX' and self.jflow_template_version == '15.1' \
        and self.cflow_version == '9' \
        and self.template_type == 'mpls' and self.jflow_type == 'INLINE':
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

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['18.1', '18.3', '19.2']) and \
        self.cflow_version == '9' \
        and self.template_type == 'mpls' and self.jflow_type == 'INLINE':
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
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            return template_dict

        if self.platform == 'MX' and \
        self.jflow_template_version == '15.1' and self.cflow_version == '10' \
        and (self.template_type == 'mpls-v4' or self.template_type == 'mpls-ipv4') \
        and self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            return template_dict

        if self.platform == 'MX' and \
        self.jflow_template_version == '15.1' and self.cflow_version == '9' \
        and (self.template_type == 'mpls-v4' or self.template_type == 'mpls-ipv4') \
        and self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['18.1', '18.3', '19.2']) \
        and self.cflow_version == '10' \
        and (self.template_type == 'mpls-v4' or self.template_type == 'mpls-ipv4') \
        and self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['18.1', '18.3', '19.2']) \
        and self.cflow_version == '9' \
        and (self.template_type == 'mpls-v4' or self.template_type == 'mpls-ipv4') \
        and self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IP_PROTOCOL_VERSION'] = {
                'Length': '1', 'Type': 'IP_PROTOCOL_VERSION', 'Element_id': '60'}
            template_dict['BGP_NEXT_HOP'] = {
                'Length': '4', 'Type': 'BGP_NEXT_HOP', 'Element_id': '18'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['18.1', '18.3', '19.2']) \
        and self.cflow_version == '9' and self.template_type == 'vpls' and \
        self.jflow_type == 'INLINE':
            template_dict['DESTINATION_MAC'] = {
                'Length': '6', 'Type': 'DESTINATION_MAC', 'Element_id': '80'}
            template_dict['SRC_MAC'] = {'Length': '6', 'Type': 'SRC_MAC', 'Element_id': '56'}
            template_dict['ethernetType'] = {
                'Length': '2', 'Type': 'ethernetType', 'Element_id': '256'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['15.1', '18.1', '18.3', '19.2']) \
        and self.cflow_version == '10' and self.template_type == 'vpls' and \
        self.jflow_type == 'INLINE':
            template_dict['DESTINATION_MAC'] = {
                'Length': '6', 'Type': 'DESTINATION_MAC', 'Element_id': '80'}
            template_dict['SRC_MAC'] = {'Length': '6', 'Type': 'SRC_MAC', 'Element_id': '56'}
            template_dict['ethernetType'] = {
                'Length': '2', 'Type': 'ethernetType', 'Element_id': '256'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['18.1', '18.3', '19.2']) \
        and self.cflow_version == '9' and self.template_type == 'bridge' and \
        self.jflow_type == 'INLINE':
            template_dict['DESTINATION_MAC'] = {
                'Length': '6', 'Type': 'DESTINATION_MAC', 'Element_id': '80'}
            template_dict['SRC_MAC'] = {'Length': '6', 'Type': 'SRC_MAC', 'Element_id': '56'}
            template_dict['ethernetType'] = {
                'Length': '2', 'Type': 'ethernetType', 'Element_id': '256'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['18.1', '18.3', '19.2']) \
        and self.cflow_version == '10' and self.template_type == 'bridge' and \
        self.jflow_type == 'INLINE':
            template_dict['DESTINATION_MAC'] = {
                'Length': '6', 'Type': 'DESTINATION_MAC', 'Element_id': '80'}
            template_dict['SRC_MAC'] = {'Length': '6', 'Type': 'SRC_MAC', 'Element_id': '56'}
            template_dict['ethernetType'] = {
                'Length': '2', 'Type': 'ethernetType', 'Element_id': '256'}
            template_dict['INPUT_SNMP'] = {'Length': '4', 'Type': 'INPUT_SNMP', 'Element_id': '10'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            return template_dict


        if self.platform == 'MX' and (self.jflow_template_version in ['18.3']) \
        and self.cflow_version == '10' and self.template_type == 'mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IPV6_OPTION_HEADERS'] = {
                'Length': '4', 'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64'}
            return template_dict

        if self.platform == 'MX' and (self.jflow_template_version in ['18.3']) \
        and self.cflow_version == '9' \
        and self.template_type == 'mpls-ipv6' and self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
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
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IPV6_OPTION_HEADERS'] = {
                'Length': '4', 'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64'}
            return template_dict


        if self.platform == 'MX' and (self.jflow_template_version in ['19.2']) \
        and self.cflow_version == '10' and self.template_type == 'mpls-ipv6' and \
        self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['BGP_IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'BGP_IPV6_NEXT_HOP', 'Element_id': '63'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['flowStartMilliseconds'] = {
                'Length': '8', 'Type': 'flowStartMilliseconds', 'Element_id': '152'}
            template_dict['flowEndMilliseconds'] = {
                'Length': '8', 'Type': 'flowEndMilliseconds', 'Element_id': '153'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IPV6_OPTION_HEADERS'] = {
                'Length': '4', 'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64'}
            return template_dict


        if self.platform == 'MX' and (self.jflow_template_version in ['19.2']) \
        and self.cflow_version == '9' \
        and self.template_type == 'mpls-ipv6' and self.jflow_type == 'INLINE':
            template_dict['MPLS_LABEL_1'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_1', 'Element_id': '70'}
            template_dict['MPLS_LABEL_2'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_2', 'Element_id': '71'}
            template_dict['MPLS_LABEL_3'] = {
                'Length': '3', 'Type': 'MPLS_LABEL_3', 'Element_id': '72'}
            template_dict['MPLS_TOP_LABEL_ADDR'] = {
                'Length': '4', 'Type': 'MPLS_TOP_LABEL_ADDR', 'Element_id': '47'}
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
            template_dict['SRC_VLAN'] = {'Length': '2', 'Type': 'SRC_VLAN', 'Element_id': '58'}
            template_dict['IPV6_SRC_MASK'] = {
                'Length': '1', 'Type': 'IPV6_SRC_MASK', 'Element_id': '29'}
            template_dict['IPV6_DST_MASK'] = {
                'Length': '1', 'Type': 'IPV6_DST_MASK', 'Element_id': '30'}
            template_dict['SRC_AS'] = {'Length': '4', 'Type': 'SRC_AS', 'Element_id': '16'}
            template_dict['DST_AS'] = {'Length': '4', 'Type': 'DST_AS', 'Element_id': '17'}
            template_dict['IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'IPV6_NEXT_HOP', 'Element_id': '62'}
            template_dict['BGP_IPV6_NEXT_HOP'] = {
                'Length': '16', 'Type': 'BGP_IPV6_NEXT_HOP', 'Element_id': '63'}
            template_dict['TCP_FLAGS'] = {'Length': '1', 'Type': 'TCP_FLAGS', 'Element_id': '6'}
            template_dict['OUTPUT_SNMP'] = {
                'Length': '4', 'Type': 'OUTPUT_SNMP', 'Element_id': '14'}
            template_dict['BYTES'] = {'Length': '8', 'Type': 'BYTES', 'Element_id': '1'}
            template_dict['PKTS'] = {'Length': '8', 'Type': 'PKTS', 'Element_id': '2'}
            template_dict['IP TTL MINIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MINIMUM', 'Element_id': '52'}
            template_dict['IP TTL MAXIMUM'] = {
                'Length': '1', 'Type': 'IP TTL MAXIMUM', 'Element_id': '53'}
            template_dict['FIRST_SWITCHED'] = {
                'Length': '4', 'Type': 'FIRST_SWITCHED', 'Element_id': '22'}
            template_dict['LAST_SWITCHED'] = {
                'Length': '4', 'Type': 'LAST_SWITCHED', 'Element_id': '21'}
            template_dict['flowEndReason'] = {
                'Length': '1', 'Type': 'flowEndReason', 'Element_id': '136'}
            template_dict['DIRECTION'] = {'Length': '1', 'Type': 'DIRECTION', 'Element_id': '61'}
            template_dict['dot1qVlanId'] = {
                'Length': '2', 'Type': 'dot1qVlanId', 'Element_id': '243'}
            template_dict['dot1qCustomerVlanId'] = {
                'Length': '2', 'Type': 'dot1qCustomerVlanId', 'Element_id': '245'}
            template_dict['IPv4 ID'] = {'Length': '4', 'Type': 'IPv4 ID', 'Element_id': '54'}
            template_dict['IPV6_OPTION_HEADERS'] = {
                'Length': '4', 'Type': 'IPV6_OPTION_HEADERS', 'Element_id': '64'}
            return template_dict


    def get_expected_option_template(self):
        """
        This method returns the expected option template depending upon
        the cflow version , platform and jflow template version.


        It will be called internally while calling init function

        :return: dictionary output for expected option template

        :rtype: dict
        """

        template_dict = {}
        if self.platform == 'MX' and \
        (self.jflow_template_version in ['15.1', '18.1', '18.3', '19.2']) and \
        self.cflow_version == '10' and self.jflow_type == 'INLINE':
            template_dict['FLOW_EXPORTER'] = {
                'Length': '4', 'Type': 'FLOW_EXPORTER', 'Element_id': '144'}
            template_dict['TOTAL_PKTS_EXP'] = {
                'Length': '8', 'Type': 'TOTAL_PKTS_EXP', 'Element_id': '41'}
            template_dict['TOTAL_FLOWS_EXP'] = {
                'Length': '8', 'Type': 'TOTAL_FLOWS_EXP', 'Element_id': '42'}
            template_dict['systemInitTimeMilliseconds'] = {
                'Length': '8', 'Type': 'systemInitTimeMilliseconds', 'Element_id': '160'}
            template_dict['exporterIPv4Address'] = {
                'Length': '4', 'Type': 'exporterIPv4Address', 'Element_id': '130'}
            template_dict['exporterIPv6Address'] = {
                'Length': '16', 'Type': 'exporterIPv6Address', 'Element_id': '131'}
            template_dict['SAMPLING_INTERVAL'] = {
                'Length': '4', 'Type': 'SAMPLING_INTERVAL', 'Element_id': '34'}
            template_dict['FLOW_ACTIVE_TIMEOUT'] = {
                'Length': '2', 'Type': 'FLOW_ACTIVE_TIMEOUT', 'Element_id': '36'}
            template_dict['FLOW_INACTIVE_TIMEOUT'] = {
                'Length': '2', 'Type': 'FLOW_INACTIVE_TIMEOUT', 'Element_id': '37'}
            template_dict['collectorProtocolVersion'] = {
                'Length': '1', 'Type': 'collectorProtocolVersion', 'Element_id': '214'}
            template_dict['collectorTransportProtocol'] = {
                'Length': '1', 'Type': 'collectorTransportProtocol', 'Element_id': '215'}
            return template_dict

        if self.platform == 'MX' and \
        (self.jflow_template_version in ['15.1', '18.1', '18.3', '19.2']) and \
        self.cflow_version == '9' and self.jflow_type == 'INLINE':
            template_dict['System'] = {'Length': '0', 'Type': 'System', 'Element_id': '1'}
            template_dict['TOTAL_PKTS_EXP'] = {
                'Length': '8', 'Type': 'TOTAL_PKTS_EXP', 'Element_id': '41'}
            template_dict['TOTAL_FLOWS_EXP'] = {
                'Length': '8', 'Type': 'TOTAL_FLOWS_EXP', 'Element_id': '42'}
            template_dict['SAMPLING_INTERVAL'] = {
                'Length': '4', 'Type': 'SAMPLING_INTERVAL', 'Element_id': '34'}
            template_dict['FLOW_ACTIVE_TIMEOUT'] = {
                'Length': '2', 'Type': 'FLOW_ACTIVE_TIMEOUT', 'Element_id': '36'}
            template_dict['FLOW_INACTIVE_TIMEOUT'] = {
                'Length': '2', 'Type': 'FLOW_INACTIVE_TIMEOUT', 'Element_id': '37'}
            return template_dict

    def verify_template_record(self, template_to_verify='BOTH'):
        """
        | This method will compare the element names , element id and type
        | for data template or option template or both (data & option template)
        |
        | It compares expected template dictionary and actual template dictionary
        | per Collector and per Observation Domain Id and return True
        | if verification succeed else return false

        :param string template_to_verify
            **OPTIONAL** if not provided then both data template and option
                         template will be verified.
                         if template_to_verify='DATA TEMPLATE' then only data
                         template verification will be done
                         if template_to_verify='OPTION TEMPLATE' then only option
                         template verification will be done

        :return: True if template verification succeed else False

        :rtype: bool

        Example::

            python:
                verify_template_record()
                    Or
                verify_template_record(template_to_verify='DATA TEMPLATE')
                    Or
                verify_template_record(template_to_verify='OPTION TEMPLATE')
            Robot:
                Verify Template Record
                    Or
                Verify Template Record    template_to_verify='DATA TEMPLATE'
                    Or
                Verify Template Record    template_to_verify='OPTION TEMPLATE'
        """

        if self.platform == 'MX' and template_to_verify == 'BOTH' \
        and self.jflow_type == 'INLINE':
            mxdata_temp_status = self.verify_mx_template_inline(
                'DATA TEMPLATE')
            mxoption_temp_status = self.verify_mx_template_inline(
                'OPTION TEMPLATE')
            if mxdata_temp_status is True and \
            mxoption_temp_status is True:
                mx_template_verification_status = True
                self.tmpl_verify_stat = mx_template_verification_status
                return mx_template_verification_status
            else:
                mx_template_verification_status = False
                if mxdata_temp_status is False:
                    self.log("ERROR", "Data Template verification failed ")
                if mxoption_temp_status is False:
                    self.log("ERROR", "Option Template verification failed ")
                self.tmpl_verify_stat = mx_template_verification_status
                return mx_template_verification_status

        elif self.platform == 'MX' and template_to_verify == 'DATA TEMPLATE' \
        and self.jflow_type == 'INLINE':
            mxdata_temp_status = self.verify_mx_template_inline(
                'DATA TEMPLATE')
            self.tmpl_verify_stat = mxdata_temp_status
            return mxdata_temp_status

        elif self.platform == 'MX' and template_to_verify == 'OPTION TEMPLATE' \
        and self.jflow_type == 'INLINE':
            mxoption_temp_status = self.verify_mx_template_inline(
                'OPTION TEMPLATE')
            self.tmpl_verify_stat = mxoption_temp_status
            return mxoption_temp_status

    def verify_mx_template_inline(self, template_to_verify=None):
        """
        template_to_verify \'DATA TEMPLATE\' and \'OPTION TEMPLATE\'
        for MX platform

        It will be internally called by method name "verify_template_record"

        :return: True if template verification succeed else False

        :rtype: bool
        """
        result_list = []
        obs_dmn_ids = self.obs_dmn_ids
        flow_colls = self.flow_colls
        decode_dump = self.decode_dump_with_flow_selectors['decode_dump']
        if template_to_verify not in ['DATA TEMPLATE', 'OPTION TEMPLATE']:
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
            if self.cflow_version == '9' and self.default_option_pktname \
            == self.exp_optionpkt_flowset:
                verify_type = 'OPTIONS_V9_INLINE'
                expected_template_pkt_type = 'Options Template(V9) (1)'
            elif self.cflow_version == '10' and self.default_option_pktname \
            == self.exp_optionpkt_flowset:
                verify_type = 'OPTIONS_IPFIX_INLINE'
                expected_template_pkt_type = 'Options Template (V10 [IPFIX]) (3)'
            else:
                verify_type = 'OPTIONS'
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
                "for observation domain id : %s" %obs_dmn_id_tmp)
                if obs_dmn_id_tmp not in actual_obs_domn_keys:
                    result = False
                    result_list.append(result)
                    break
                if verify_type == 'TEMPLATE' or verify_type == 'OPTIONS_IPFIX_INLINE' \
                or verify_type == 'OPTIONS_V9_INLINE':
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

    def verify_option_data_record(self, **kwarg):
        """
        | This method will compare the values of Actual option data record received at
        | collector saved in dictionary data structure with our expected dictionary
        | built in test script.

        :param dict expected_option_data_pdu_dict
            **REQUIRED** it is a dictionary containing option data records like
                         {'Sampling interval' : '1' , 'Flow active timeout': '120' ,\
                             'Flow inactive timeout': '60'}

        :param string expected_flows_export
            **OPTIONAL** This optional argument can be used validate the expected
                         flows exported during a test while comapring the first
                         option data record and last option data record.

                         Suppose user send 10 flows to be actively Timed out ,then run
                         the tcpdump till (Active timeout + option refresh rate ) so that
                         we can receive the updated value of flow exported in option
                         record.


        :return: True if Option Data verification succeed else False

        :rtype: bool

        Example::

            python:
                expected_option_data_pdu_dict = {'Sampling interval' : '1' , \
                'Flow active timeout': '120', 'Flow inactive timeout': '60'}
                expected_flows_export = 10

                verify_option_data_record(
                    expected_option_data_pdu_dict = expected_option_data_pdu_dict)
                    Or
                verify_option_data_record(
                    expected_option_data_pdu_dict = expected_option_data_pdu_dict,
                    expected_flows_export = 10 )
            Robot:
                Verify Option Data Record    expected_option_data_pdu_dict=\
                                                 ${expected_option_data_pdu_dict}
                    Or
                Verify Option Data Record   expected_option_data_pdu_dict=\
                                            ${expected_option_data_pdu_dict} \
                                            expected_flows_export_count=10
        """
        if self.platform == 'MX' and self.jflow_type == 'INLINE':
            mx_option_data_record_status = self.verify_mx_option_data_inline(**kwarg)
            self.option_data_verify_status = mx_option_data_record_status
            if mx_option_data_record_status is True:
                self.log("INFO","Option data verification passed")
            else:
                self.log("ERROR","Option data verification failed")
            return mx_option_data_record_status

    def verify_mx_option_data_inline(self, **kwarg):
        """
        This method will verify option data record only for 'MX' platform

        It will be internally called by method name "verify_option_data_record"

        :return: True if template verification succeed else False

        :rtype: bool
        """
        result_list = []
        obs_dmn_ids = self.sampling_obs_dmn_ids
        flow_colls = self.flow_colls
        decode_dump = self.decode_dump_with_flow_selectors['decode_dump']
        templ_id = self.option_templ_id
        expected_template_pkt_type = self.exp_optionpkt_flowset
        expected_option_data_pdu_dict = kwarg.get('expected_option_data_pdu_dict', {})
        if 'expected_flows_export_count' in kwarg:
            expected_flows_export_count = kwarg['expected_flows_export_count']
        if len(expected_option_data_pdu_dict) == 0:
            raise ValueError(
                "Please Provide atleast one key-value pair for verification of option data record")

        if self.cflow_version == '9':
            verify_type = 'OPTIONS_DATA_V9_INLINE'
        elif self.cflow_version == '10':
            verify_type = 'OPTIONS_DATA_IPFIX_INLINE'

        for flw_col_tmp in flow_colls:
            self.log("INFO", "Now Checking the option data record "\
            "on collector IP : %s"% flw_col_tmp)
            actual_obs_domn_keys = decode_dump['FLOWS'][flw_col_tmp].keys()
            actual_obs_domn_keys = list(actual_obs_domn_keys)
            for obs_dmn_id_tmp in obs_dmn_ids:
                result = True
                obs_dmn_id_tmp = str(obs_dmn_id_tmp)
                self.log("INFO", \
                    "Now Checking the template record for observation domain id : %s" %\
                    obs_dmn_id_tmp)
                if obs_dmn_id_tmp not in actual_obs_domn_keys:
                    result = False
                    result_list.append(result)
                    break
                if verify_type == 'OPTIONS_DATA_V9_INLINE' or \
                verify_type == 'OPTIONS_DATA_IPFIX_INLINE':
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
                    actual_option_data_pdu_dict = decode_dump['FLOWS'][flw_col_tmp][
                        obs_dmn_id_tmp][templ_id][verify_type][-1]['flowset']['pdu'][0]
                    if 'expected_flows_export_count' in kwarg:
                        first_flow_exp_val = decode_dump['FLOWS'][flw_col_tmp][obs_dmn_id_tmp][
                            templ_id][verify_type][0]['flowset']['pdu'][0]['FlowsExp']
                        expected_option_data_pdu_dict['FlowsExp'] = str(
                            int(first_flow_exp_val) + int(expected_flows_export_count))
                    result2 = self.compare_flow_records(
                        expected_option_data_pdu_dict, actual_option_data_pdu_dict)
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
        if self.platform == 'MX' and self.jflow_type == 'INLINE':
            mx_data_record_verify_status = self.verify_mx_data_record_inline(**kwg)
            self.data_record_status = mx_data_record_verify_status
            if mx_data_record_verify_status is True:
                self.log("INFO","Data record verification passed")
            else:
                self.log("ERROR","Data record verification failed")
            return mx_data_record_verify_status

    def verify_mx_data_record_inline(self, **kwg):
        """
        This method will verify data record only for 'MX' platform

        It will be internally called by method name "verify_data_record"

        :return: True if template verification succeed else False

        :rtype: bool
        """

        if self.template_type == 'vpls' or self.template_type =='bridge':
            return self._verify_mx_l2_data_record_inline(**kwg)
        if 'expected_pdu_dict' in kwg:
            expected_pdu_dict = kwg['expected_pdu_dict']
        else:
            expected_pdu_dict = {}

        do_not_verify = kwg.get('do_not_verify', [])
        if self.template_type == 'mpls':
            do_not_verify.extend(['SrcAddr', 'DstAddr', 'SrcPort', 'DstPort'])
            do_not_verify.extend(['SrcAS', 'DstAS', 'SrcMask', 'DstMask'])
            do_not_verify.extend(['NextHop', 'BGPNextHop', 'Vlan Id'])

        decode_dump = self.decode_dump_with_flow_selectors['decode_dump']
        flow_colls = self.flow_colls
        if 'sampling_obs_dmn_ids' in kwg:
            obs = kwg['sampling_obs_dmn_ids']
            obs_dmn_ids = [str(obs)]
        else:
            obs_dmn_ids = self.sampling_obs_dmn_ids
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

                if float(self.jflow_template_version) >= 15.1:
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
                            elif flow_selector_identifier[count] == 'Vlan Id':
                                expected_pdu_dict['Vlan Id'] = selector
                            elif flow_selector_identifier[count] == 'Direction':
                                expected_pdu_dict['Direction'] = selector
                            elif flow_selector_identifier[count] == 'Flow End Reason':
                                expected_pdu_dict['Flow End Reason'] = selector
                            elif flow_selector_identifier[count] == 'IP ToS':
                                expected_pdu_dict['IP ToS'] = selector
                            elif flow_selector_identifier[count] == 'IPv4Ident':
                                expected_pdu_dict['IPv4Ident'] = selector
                            elif flow_selector_identifier[count] == 'Protocol':
                                expected_pdu_dict['Protocol'] = selector
                            elif flow_selector_identifier[count] == 'TCP Flags':
                                expected_pdu_dict['TCP Flags'] = selector
                            elif flow_selector_identifier[count] == 'Type':
                                expected_pdu_dict['Type'] = selector
                            elif flow_selector_identifier[count] == 'IPv6 Extension Headers':
                                expected_pdu_dict['IPv6 Extension Headers'] = selector
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
                            elif flow_selector_identifier[count] == 'Dot1q Vlan Id':
                                expected_pdu_dict['Dot1q Vlan Id'] = selector
                            elif flow_selector_identifier[count] == 'Dot1q Customer Vlan Id':
                                expected_pdu_dict['Dot1q Customer Vlan Id'] = selector
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

                                # BGPNextHop is only present in ipv4/mplsv4 record for 18.1 and in
                                # 17.4 , it was present only for ipv4-ipfix
                                if ('BGPNextHop' not in expected_pdu_dict and \
                                'BGPNextHop' not in do_not_verify) and \
                                (self.template_type == 'ipv4' or self.template_type == 'mpls-ipv4'):
                                    bgp_next_hop = self.get_bgp_nexthop(
                                        dhandle=self.dhandle, ipaddr=expected_pdu_dict['DstAddr'])
                                    if bgp_next_hop is None and \
                                    str(ipaddress.IPv4Address(expected_pdu_dict['DstAddr'])) \
                                    == expected_pdu_dict['DstAddr'] and \
                                    (self.jflow_template_version in ['18.1', '18.3', '19.2']):
                                        expected_pdu_dict['BGPNextHop'] = '0.0.0.0'
                                    elif bgp_next_hop is not None \
                                    and str(ipaddress.IPv4Address(expected_pdu_dict['DstAddr'])) \
                                    == expected_pdu_dict['DstAddr'] and \
                                    (self.jflow_template_version in ['18.1', '18.3', '19.2']):
                                        expected_pdu_dict['BGPNextHop'] = bgp_next_hop
                                    elif bgp_next_hop is not None \
                                    and str(ipaddress.IPv4Address(expected_pdu_dict['DstAddr'])) \
                                    == expected_pdu_dict['DstAddr'] and \
                                    self.jflow_template_version == '15.1' \
                                    and actual_cflow_ver == '9':
                                        expected_pdu_dict['BGPNextHop'] = bgp_next_hop

                                if 'Vlan Id' not in expected_pdu_dict and \
                                'Vlan Id' not in do_not_verify:
                                    src_vlan = self.get_vlan_assigned_to_interface(
                                        dhandle=self.dhandle, interface=self.sampling_interface)
                                    if src_vlan is None:
                                        expected_pdu_dict['Vlan Id'] = '0'
                                    else:
                                        expected_pdu_dict['Vlan Id'] = src_vlan

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

    def _verify_mx_l2_data_record_inline(self, **kwg):
        """
        This method will verify data record only for 'MX' platform

        It will be internally called by method name "verify_data_record"

        :return: True if template verification succeed else False

        :rtype: bool
        """

        if 'expected_pdu_dict' in kwg:
            expected_pdu_dict = kwg['expected_pdu_dict']
        else:
            expected_pdu_dict = {}

        decode_dump = self.decode_dump_with_flow_selectors['decode_dump']
        flow_colls = self.flow_colls
        if 'sampling_obs_dmn_ids' in kwg:
            obs = kwg['sampling_obs_dmn_ids']
            obs_dmn_ids = [str(obs)]
        else:
            obs_dmn_ids = self.sampling_obs_dmn_ids
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
                if float(self.jflow_template_version) >= 15.1:
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
                            if flow_selector_identifier[count] == 'Source Mac Address':
                                expected_pdu_dict['Source Mac Address'] = selector
                            elif flow_selector_identifier[count] == 'Destination Mac Address':
                                expected_pdu_dict['Destination Mac Address'] = selector
                            elif flow_selector_identifier[count] == 'Type':
                                expected_pdu_dict['Type'] = selector
                            elif flow_selector_identifier[count] == 'Flow End Reason':
                                expected_pdu_dict['Flow End Reason'] = selector
                            elif flow_selector_identifier[count] == 'InputInt':
                                expected_pdu_dict['InputInt'] = selector
                            elif flow_selector_identifier[count] == 'OutputInt':
                                expected_pdu_dict['OutputInt'] = selector
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

                                if 'Source Mac Address' not in expected_pdu_dict:
                                    self.log("ERROR", \
                                            "Either declare (Source Mac Address) in expected \
                                            dictionary created in ROBOT file or make it as a \
                                            part of flow_selectors")
                                    return False
                                if 'Destination Mac Address' not in expected_pdu_dict:
                                    self.log("ERROR", \
                                            "Either declare (Destination Mac Address) in expected \
                                            dictionary created in ROBOT file or make it as a \
                                            part of flow_selectors")
                                    return False
                                if 'Type' not in expected_pdu_dict:
                                    self.log("ERROR", \
                                            "Either declare (Type) in expected \
                                            dictionary created in ROBOT file or make it as a \
                                            part of flow_selectors")
                                    return False
                                if 'Flow End Reason' not in expected_pdu_dict:
                                    self.log("ERROR", \
                                            "Either declare (Flow End Reason) in expected \
                                            dictionary created in ROBOT file or make it as a \
                                            part of flow_selectors")
                                    return False
                                if 'InputInt' not in expected_pdu_dict:
                                    iif = self.get_nexthop_interface(dhandle=self.dhandle, \
                                            ipaddr=expected_pdu_dict['Source Mac Address'])
                                    self.input_if = iif
                                    input_snmp_index = self.get_snmp_index_value(
                                            dhandle=self.dhandle, interface=iif)
                                    if input_snmp_index is None:
                                        expected_pdu_dict['InputInt'] = 'NO VALUE FOUND'
                                    else:
                                        expected_pdu_dict['InputInt'] = str(input_snmp_index)
                                if 'OutputInt' not in expected_pdu_dict:
                                    iif = self.get_nexthop_interface(dhandle=self.dhandle, \
                                            ipaddr=expected_pdu_dict['Destination Mac Address'])
                                    self.input_if = iif
                                    input_snmp_index = self.get_snmp_index_value(
                                            dhandle=self.dhandle, interface=iif)
                                    if input_snmp_index is None:
                                        expected_pdu_dict['OutputInt'] = 'NO VALUE FOUND'
                                    else:
                                        expected_pdu_dict['OutputInt'] = str(input_snmp_index)

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

    def get_oif_flow_dict(self, dhandle=None, sampling_intf=None, flow_key=None, family=None, \
            flow_count=None):
        """
        This method returns the OIF->flow_key dictionary
        :param obj dhandle
            **REQUIRED** Router handle

        :param str sampling_intf
            **REQUIRED** sampling interface

        :param str flow_key
            **REQUIRED** flow key based on which traffic is being load balanced

        :param str family
            **REQUIRED** sampling family

        :param str flow_count
            **REQUIRED** count of flows
        """
        self.dhandle = dhandle
        rut1 = rutils.rutils()
        fpc_slot, pic_slot, port_num = rut1.get_fpc_pic_port_from_ifname(sampling_intf)
        del rut1
        del pic_slot
        del port_num
        pfe_instance = self.get_pfe_number(dhandle, interface=sampling_intf)

        oif_flow_dict = {}
        flow_token_dict = self.get_flow_token_dict(dhandle=dhandle, fpc_slot=fpc_slot, \
                pfe=pfe_instance, flow_key=flow_key, family=family, flow_count=flow_count)


        for token in flow_token_dict.keys():
            destination = "fpc" + fpc_slot
            output = dhandle.vty(command='show nhdb id %s recursive' % token, destination=destination)
            match_out = re.search(r'%s\(Unicast.*ifl:\d+:(.*),\s*pfe' % token, output.response())
            output_intf = match_out.group(1)
            oif = self.get_snmp_index_value(dhandle=dhandle, interface=output_intf)
            oif_flow_dict[oif] = flow_token_dict[token]
        return oif_flow_dict

    def get_flow_token_dict(self, dhandle=None, fpc_slot=None, pfe=None, flow_key=None, \
            family=None, flow_count=None):
        """
        This method returns flow_token->flow_key_list dictionary

        :param obj dhandle
            **REQUIRED** Router handle

        :param str fpc_slot
            **REQUIRED** sampling fpc slot

        :param str pfe
            **REQUIRED** pfe instance

        :param str flow_key
            **REQUIRED**  flow key based on which traffic is being load balanced

        :param str family
            **REQUIRED** sampling family

        :param str coun
            **REQUIRED** flow count
        """
        destination = "fpc" + fpc_slot
        output = dhandle.vty(command='show jnh %s services %s-flows count %s detail' %(pfe, family, \
                flow_count), destination=destination)

        lines = output.response().replace('\r\n','\n').split('\n')
        flow_token_dict = {}

        for line in range(len(lines)):
            match_regex = re.escape(flow_key) + r":\s+(.*)"
            match_key = re.search(match_regex, lines[line])
            if match_key:
                while line in range(len(lines)) and not re.search(r'Flow Number.*', lines[line]):
                    match_token = re.search(r'.*Flow Token ID:\s+(\d+)', lines[line])
                    if match_token:
                        flow_token = match_token.group(1)
                        if flow_token not in flow_token_dict.keys():
                            flow_token_dict[flow_token] = []
                            flow_token_dict[flow_token].append(match_key.group(1))
                        else:
                            flow_token_dict[flow_token].append(match_key.group(1))
                    line += 1
        return flow_token_dict

    def get_as_value(self, dhandle=None, ipaddr=None, **kwg):
        """
        This method calculates the AS value for network provided as input.

        :param obj dhandle
            **REQUIRED** Router handle

        :param string ipaddr
            **REQUIRED** IP address for which AS value to be determined

        :return: string type AS value if BGP routes exists for the ipaddress \
                 passed in argument else None

        :rtype: string or None
        """
        self.dhandle = dhandle
        output = dhandle.cli(command='show route %s' % ipaddr).\
response().replace('\r\n', '\n')
        matched = re.search(r'AS path: (\d+)', output)
        if matched:
            as_find = re.search(r'AS path: (.*) I', output)
            as_list = as_find.group(1).split()
            as_type= kwg.get('autonomous-system-type', 'origin') 
            if as_type == 'origin':
                return as_list[-1] 
            
            elif as_type == 'peer':
                return as_list[0]
        else:
            return None

    def get_ip_mask_from_route_detail(self, dhandle=None, ipaddr=None):
        """
        This method calculates the IP mask for network provided as input.

        :param obj dhandle
            **REQUIRED** Router handle

        :param string ipaddr
            **REQUIRED** IP address for which IP mask value to be determined

        :return: string type Mask value if routes exists for the ipaddress \
                 passed in argument else None

        :rtype: string or None
        """

        self.dhandle = dhandle
        output = dhandle.cli(command='show route %s | grep "/"' % ipaddr).response().replace('\r\n', '\n')
        matched = re.search(r'^\w+.*[/](\d+)\s+', output, re.MULTILINE)
        if matched:
            return matched.group(1)
        else:
            return None

    def get_nexthop(self, dhandle=None, ipaddr=None, **kwg):
        """
        This method calculates the nexhop value for network provided as input.

        :param obj dhandle
            **REQUIRED** Router handle

        :param string ipaddr
            **REQUIRED** IP address for which next hop value to be determined

        :return: string type nexthop value if routes exists for the ipaddress \
                 passed in argument else None

        :rtype: string or None
        """
        dst_ipv4_mask = str(kwg.get('dst_ipv4_mask', 32))
        dst_ipv6_mask = str(kwg.get('dst_ipv6_mask', 128))
        rt_table = kwg.get('routing_table', None)

        if '.' in ipaddr:
            ip_mask = dst_ipv4_mask
        elif ':' in ipaddr:
            ip_mask = dst_ipv6_mask

        self.dhandle = dhandle
        if rt_table is None:
            output = dhandle.cli(
            command='show route forwarding-table destination %s/%s extensive' %
            (ipaddr, ip_mask)).response().replace('\r\n', '\n')
        else:
            output = dhandle.cli(
            command='show route forwarding-table destination %s/%s extensive table %s' %
            (ipaddr, ip_mask, rt_table)).response().replace('\r\n', '\n')

        matched = re.search(r'Destination:\s+\d+.*[/]%s(.*\n)*?.*?Nexthop: (\w+[:.].*\w+)' % ip_mask, output)
        if matched:
            return matched.group(2)
        else:
            return None

    def get_nexthops_from_forwarding_table(self, dhandle=None, ipaddr=None, **kwg):
        """
        This method calculates the nexhop value for network provided as input.

        :param obj dhandle
            **REQUIRED** Router handle

        :param string ipaddr
            **REQUIRED** IP address for which next hop value to be determined

        :return: string type nexthop value if routes exists for the ipaddress \
                 passed in argument else None

        :rtype: list
        """
        dst_ipv4_mask = str(kwg.get('dst_ipv4_mask', 32))
        dst_ipv6_mask = str(kwg.get('dst_ipv6_mask', 128))
        rt_table = kwg.get('routing_table', None)

        if '.' in ipaddr:
            ip_mask = dst_ipv4_mask
        elif ':' in ipaddr:
            ip_mask = dst_ipv6_mask

        self.dhandle = dhandle
        if rt_table is None:
            output = dhandle.cli(
            command='show route forwarding-table destination %s/%s extensive' %
            (ipaddr, ip_mask)).response().replace('\r\n', '\n')
        else:
            output = dhandle.cli(
            command='show route forwarding-table destination %s/%s extensive table %s' %
            (ipaddr, ip_mask, rt_table)).response().replace('\r\n', '\n')

        matched = re.findall(r'Nexthop: (\w+[:.].*\w+)', output)
        if matched:
            return matched
        else:
            empty_list = []
            return empty_list

    def get_multiple_bgp_nexthops(self, dhandle=None, ipaddr=None):
        """
        This method calculates the BGP nexhop value for network provided as input.

        :param obj dhandle
            **REQUIRED** Router handle

        :param string ipaddr
            **REQUIRED** IP address for which BGP nexthop value to be determined

        :return: string type BGPNexthop value if routes exists for the ipaddress \
                 passed in argument else None

        :rtype: string or None
        """
        self.dhandle = dhandle
        output = dhandle.cli(
            command='show route protocol bgp %s extensive' %
            ipaddr).response().replace('\r\n', '\n')

        matched = re.findall(r'Source: (\w+[:.].*\w+)', output)
        if matched:
            return matched
        else:
            empty_list = []
            return empty_list

    def get_bgp_nexthop(self, dhandle=None, ipaddr=None):
        """
        This method calculates the BGP nexhop value for network provided as input.

        :param obj dhandle
            **REQUIRED** Router handle

        :param string ipaddr
            **REQUIRED** IP address for which BGP nexthop value to be determined

        :return: string type BGPNexthop value if routes exists for the ipaddress \
                 passed in argument else None

        :rtype: string or None
        """
        self.dhandle = dhandle
        output = dhandle.cli(
            command='show route protocol bgp %s extensive active-path' %
            ipaddr).response().replace('\r\n', '\n')

        matched = re.search(
            r'Protocol next hop: (\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|\w{1,4}:.*:\w{1,4})',
            output)
        if matched:
            return matched.group(1)

        matched = re.search(r'Source: (\w+[:.].*\w+)', output)
        if matched:
            return matched.group(1)
            
        matched = re.search(
            r'Path (?:\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|\w{1,4}:.*:\w{1,4}) from (\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|\w{1,4}:.*:\w{1,4})', output)
        if matched:
            return matched.group(1)

        matched = re.search(
            r'Path (?:\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|\w{1,4}:.*:\w{1,4})\s*\nfrom (\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|\w{1,4}:.*:\w{1,4})', output)
        if matched:
            return matched.group(1)
        else:
            return None

    def get_junos_version(self, dhandle=None):
        """
        This method will return junos version.

        :param obj dhandle
            **REQUIRED** Router handle

        """
        self.dhandle = dhandle
        output = dhandle.cli(
            command='show version | display xml | no-more | grep "junos-version"').response().replace('\r\n', '\n')

        matched = re.search(r'junos-version>(\d+[.]\d)',output)
        if matched:
            return matched.group(1)
        else:
            print("Junos version not found, plz check the output manually")


    def get_nexthop_interface(self, dhandle=None, ipaddr=None):
        """
        This method calculates the nexthop_interface value for \
        network provided as input.

        :param obj dhandle
            **REQUIRED** Router handle

        :param string ipaddr
            **REQUIRED** IP address of the interface for which nexthop interface \
                         to be determined

        :return: string type nexthop_interface value if routes exists for IP \
                 passed in argument.

        :rtype: string or None
        """

        self.dhandle = dhandle
        output = dhandle.cli(
            command='show route forwarding-table destination %s extensive' %
            ipaddr).response().replace('\r\n', '\n')
        matched = re.search(
            r'Destination:\s+%s(.*\n)*?.*?Next-hop interface: (.*?)\s' %
            ipaddr, output)
        if matched:
            if_name = matched.group(2)
            if if_name != 'local':
                return if_name
            else:
                output = dhandle.cli(
                    command='show route %s active-path' %
                    ipaddr).response().replace('\r\n', '\n')
                matched = re.search(r'Local via (.*)\s*', output)
                if_name = matched.group(1)
                return if_name
        else:
            self.log("INFO", "No routes present for %s hence cannot "\
            "retrieve next-hop-interface"% ipaddr)
            return None

    def get_nexthop_interface_via_route(self, dhandle=None, ipaddr=None, **kwg):
        """
        This method calculates the nexthop_interface value for \
        network provided as input.

        :param obj dhandle
            **REQUIRED** Router handle

        :param string ipaddr
            **REQUIRED** IP address of the interface for which nexthop interface \
                         to be determined

        :return: string type nexthop_interface value if routes exists for IP \
                 passed in argument.

        :rtype: string or None
        """
        dst_ipv4_mask = kwg.get('dst_ipv4_mask', '32')
        dst_ipv6_mask = kwg.get('dst_ipv6_mask', '128')
        src_ipv4_mask = kwg.get('src_ipv4_mask', '32')
        src_ipv6_mask = kwg.get('src_ipv6_mask', '128')
        rt_table = kwg.get('routing_table', None)
        nh_type = kwg.get('nh_type', 'oif')
        if nh_type == 'oif':
            if '.' in ipaddr:
                ip_mask = dst_ipv4_mask
            elif ':' in ipaddr:
                ip_mask = dst_ipv6_mask
        elif nh_type == 'iif':
            if '.' in ipaddr:
                ip_mask = src_ipv4_mask
            elif ':' in ipaddr:
                ip_mask = src_ipv6_mask

        self.dhandle = dhandle
        if rt_table is None:
            output = dhandle.cli(
            command='show route forwarding-table destination %s/%s extensive' %
            (ipaddr, ip_mask)).response().replace('\r\n', '\n')
        else:
            output = dhandle.cli(
            command='show route forwarding-table destination %s/%s extensive table %s' %
            (ipaddr, ip_mask, rt_table)).response().replace('\r\n', '\n')

        matched = re.search(
            r'Destination:\s+\d+.*[/]%s(.*\n)*?.*?Next-hop interface: (.*?)\s' %
            ip_mask, output)
        if matched:
            if_name = matched.group(2)
            if if_name != 'local':
                return if_name
            else:
                output = dhandle.cli(
                    command='show route %s active-path' %
                    ipaddr).response().replace('\r\n', '\n')
                matched = re.search(r'Local via (.*)\s*', output)
                if_name = matched.group(1)
                return if_name
        else:
            self.log("INFO", "No routes present for %s hence cannot "\
            "retrieve next-hop-interface"% ipaddr)
            return None

    def get_snmp_index_value(self, dhandle=None, interface=None):
        """
        This method calculates the SNMP-Index value for network provided as input.

        :param obj dhandle
            **REQUIRED** Router handle

        :param string interface
            **REQUIRED** Interface for which SNMP-Index \
                         to be determined


        :return: string type SNMP-Index value if IP address exists on router's interface \

        :rtype: string or None
        """

        self.dhandle = dhandle
        output2 = dhandle.cli(
            command='show interface %s extensive' %
            interface).response().replace('\r\n', '\n')
        matched2 = re.search(
            r'interface %s [(]Index \d+[)] [(]SNMP ifIndex (\d+)[)]' %
            interface, output2)
        if matched2:
            snmp_index = matched2.group(1)
            return snmp_index
        else:
            return None

    def get_vlan_assigned_to_interface(self, dhandle=None, interface=None):
        """
        This method calculates the VLAN ID assigned to the interface

        :param obj dhandle
            **REQUIRED** Router handle

        :param string interface
            **REQUIRED** interface for which assigned vlan id\
                         to be determined


        :return: string type VLAN ID value if vlan id is addigned to \

        :rtype: string or None
        """

        self.dhandle = dhandle
        output2 = dhandle.cli(
            command='show interface %s extensive' %
            interface).response().replace('\r\n', '\n')
        matched2 = re.search(r'VLAN-Tag.*0x8100[.](\d+)', output2)
        if matched2:
            vlan_id = matched2.group(1)
            return vlan_id
        else:
            return None

    def compare_flow_records(self, expected_dictionary, actual_dictionary):
        """
        This method will be called to compare the two dictionaries
        Where verification will be done for all the keys-values present in
        expected dictionary and will be compared against actual dictionary.

        This methos will determine that keys present in expected dictionary are
        present in actual dictionary
        And if key is present then it will do the comparision of the values for
        respective keys .

        :param dict expected_dictionary
            **REQUIRED** expected dictionary passed and appended by calling
                         method verify_data_record

        :param dict actual_dictionary
            **REQUIRED** It actually points to PDU data of decode_dump dictionary


        :return: True if all keys presnt in expected dictionary are also
                 present in actual dictionary .Further respective values for
                 all keys in expected dictionary exactly matches the values of
                 key present in actual dictionary else False

        :rtype: True or False


        """
        #self.dhandle.log("Comparing records and returning status")
        result = True
        for key in expected_dictionary:
            key = str(key)
            if key in actual_dictionary:
                if str(expected_dictionary[key]) != str(actual_dictionary[key]):
                    self.log("INFO", "value mismatch for key : %s"%key)
                    self.log("INFO", "expected_value : %s"%str(expected_dictionary[key]))
                    self.log("INFO", "actual_value : %s"%str(actual_dictionary[key]))
                    self.log("INFO", "actual_dictionary : %s"%actual_dictionary)
                    self.log("INFO", "expected_dictionary : %s"%expected_dictionary)
                    result = False
                else:
                    self.log("INFO", "expected value for %s is %s"%(str(key), str((expected_dictionary[key]))))
                    self.log("INFO", "actual value for %s is %s"%(str(key), str((actual_dictionary[key]))))
            else:
                self.log("INFO", "key  : %s not found in actual dictionary"%key)
                self.log("INFO", "actual_dictionary : %s"%actual_dictionary)
                self.log("INFO", "expected_dictionary : %s"%expected_dictionary)
                result = False
        return result

    def get_ip_sequence_in_list(self, initial_ip=None, count=1):
        """
        This method return the list of consecutive IP addresses

        :param string initial_ip
            **REQUIRED** Starting IP address

        :param string count
            **REQUIRED** Total consecutive IP address to be present in list

        :return: List of consecutives IP addresses.

        :rtype: list
        """
        ipaddr = str(ipaddress.ip_address(initial_ip))
        ip_list = []
        for i in range(1, int(count) + 1):
            ip_list.append(ipaddr)
            ipaddr = iputils.incr_ip(ipaddr)
        return ip_list

    def get_mac_sequence_in_list(self, initial_mac=None, count=1, step=1):
        """
        This method returns a list of MAC addresses bease on the values of initial MAC address, step and count parsed

        :param string initial_mac
            **REQUIRED** Starting MAC address

        :param string count
            **REQUIRED** Total MAC addresses

        :param string step
            **OPTIONAL** step to increment, will be defaulted to 1 if no parsed

        :return: List of MAC addresses

        :rtype: list
        """
        initial_mac_str = re.sub('[:._]', '', initial_mac)
        mac_int = int(initial_mac_str, 16)
        count = int(count)
        step = int(step)
        mac_list = []
        for mac_index in range(0, count):
            mac_hex = "{:012x}".format(mac_int)
            mac_list.append(":".join(mac_hex[i:i+2] for i in range(0, len(mac_hex), 2)))
            mac_int += step

        return mac_list

    def get_port_list(self, initial_port_number=None, count=None):
        """
        This method return the list of consecutive port numbers

        :param string initial_port_number
            **REQUIRED** Starting port number

        :param string count
            **REQUIRED** Total consecutive port numbers to be present in list

        :return: List of consecutives port numbers

        :rtype: list
        """
        return self.get_sequence_of_numbers_in_list(initial_number=initial_port_number, count=count)

    def get_sequence_of_numbers_in_list(self, initial_number=None, count=None):
        """
        This method return the list of consecutive numbers

        :param string initial_number
            **REQUIRED** Starting number

        :param string count
            **REQUIRED** Total consecutive numbers to be present in list

        :return: List of consecutives numbers

        :rtype: list
        """

        list_of_numbers = [
            str(x) for x in range(
                int(initial_number),
                int(initial_number) +
                int(count))]
        return list_of_numbers

    def get_flow_selector_possible_sequence(self, *args):
        """
        This method returns the list of tuples by calculating the cartesian product \
        of the lists provided.

        Suppose user sent 5 flows which firstly got actively timed out followed by \
        inactive timeout expiry.
        User varied only ip address to create multiple flow and keeping destination \
        src port , dest port , protocol constant for each ip address

        src_ip_1 = 70.0.0.1
        src_ip_2 = 70.0.0.2
        src_ip_3 = 70.0.0.3
        src_ip_4 = 70.0.0.4
        src_ip_5 = 70.0.0.5

        src_ip_list = [src_ip_1, src_ip_2, src_ip_3, src_ip_4, src_ip_5]
        timeout_list = ['Active timeout (2)' , 'Idle timeout (1)']

        To uniquely decode the above flows (5 active timed out + 5 inactive timed out)
        user will use flow selector as
        flow_selector = ['SrcAddr' , 'Flow End Reason']

        While verifying the export records from decoded dictionary , user has to pass
        "decode_dump_with_flow_selectors" where one key is decoded dictionary and other is
        flow_selector_identifier_info" which is a list of dictionaries.
        flow_selector_identifier_info = [{'SrcAddr' : src_ip_list} , {'Flow End Reason' : timeout_list}]

        cartesian product of src_ip_list and timeout_list will be :-
        [
         ('70.0.0.1', 'Active timeout (2)'),
         ('70.0.0.1', 'Idle timeout (1)'),

         ('70.0.0.2', 'Active timeout (2)'),
         ('70.0.0.2', 'Idle timeout (1)'),

         ('70.0.0.3', 'Active timeout (2)'),
         ('70.0.0.3', 'Idle timeout (1)'),

         ('70.0.0.4', 'Active timeout (2)'),
         ('70.0.0.4', 'Idle timeout (1)'),

         ('70.0.0.5', 'Active timeout (2)'),
         ('70.0.0.5', 'Idle timeout (1)')
        ]
        """
        ret = itertools.product(*args)
        ret1 = list(ret)
        return ret1

    def get_pfe_type(self, device_handle=None, fpc_slot=None):
        """
        This method return the PFE type

        :param obj device_handle
            **REQUIRED** Router's handle

        :param string fpc_slot
            **REQUIRED** Fpc number

        :return: string value for the type of pfe determined

        :rtype: string
        """
        self.dhandle = device_handle
        if self.platform is None:
            self.platform = self.get_chassis_platform_info()
        if self.platform == 'MX':
            pfe_type = None
            mxdet = self.dhandle.cli(
                command="show chassis hardware | match chassis").response()
            if 'MX104' in mxdet:
                return 'mx104'
            output = self.dhandle.cli(
                command="show chassis fpc pic-status | match \"Slot %s\"" %
                str(fpc_slot)).response()
            if 'MPC Type 2' in output or 'MPCE Type 2' in output:
                pfe_type = 'neo'
            elif 'MPC 3D 16x 10GE' in output:
                pfe_type = 'as'
            elif 'MPC Type 3' in output or 'MPCE Type 3' in output:
                pfe_type = 'hyp'
            elif 'MPC Type 4' in output or 'MPC4E' in output:
                pfe_type = 'snrkl'
            elif 'MPC Type 5' in output or 'MPC5E' in output:
                pfe_type = 'xl5'
            elif 'MPC Type 6' in output or 'MPC6E' in output:
                pfe_type = 'xl6'
            elif 'MPC7E' in output:
                pfe_type = 'stout1'
            elif 'MPC8E' in output or 'MPC9E' in output:
                pfe_type = 'stout2'
            elif 'MPC2E NG' in output or 'MPC3E NG' in output:
                pfe_type = 'aloha2'
            elif 'Virtual FPC' in output:
                pfe_type = 'vfpc'
            elif 'LC2103' in output or 'MX10002-MPC' in output or 'JNP10003-MPC' in output:
                pfe_type = 'summit'
            elif 'LC2102' in output or 'JNP10008' in mxdet or 'MX10008' in mxdet:
                pfe_type = 'vale8edge'
            elif 'JNP204' in mxdet or 'MX204' in mxdet:
                pfe_type = 'summit_1ru'
            elif 'MPC10E' in output:
                pfe_type = 'ferrari10'
            elif 'MPC11E' in output:
                pfe_type = 'redbull'
            elif 'VMX ZT MPC' in output:
                pfe_type = 'vzt'
            return pfe_type

    def get_total_pfe_instance(self, pfe_type=None):
        """
        This method return the total pfe

        :param string pfe_type
            **REQUIRED** Type of PFE

        :return: string value for the total pfe instances determined

        :rtype: string
        """
        if self.platform == 'MX':
            if pfe_type == 'neo':
                tot_pfe = 2
            elif pfe_type == 'xl5' or pfe_type == 'hyp' or pfe_type == 'mx104' or \
            pfe_type == 'aloha2':
                tot_pfe = 1
            elif pfe_type == 'xl6' or pfe_type == 'snrkl' or pfe_type == 'stout1':
                tot_pfe = 2
            elif pfe_type == 'as' or pfe_type == 'stout2':
                tot_pfe = 4
            elif pfe_type == 'vfpc' or pfe_type == 'summit_1ru':
                tot_pfe = 1
            elif pfe_type == 'vzt':
                tot_pfe = 1
            elif pfe_type == 'summit' or pfe_type == 'ferrari10':
                tot_pfe = 3
            elif pfe_type == 'vale8edge':
                tot_pfe = 6
            elif pfe_type == 'redbull':
                tot_pfe = 8

            return tot_pfe

    def get_total_lu_per_pfe(self, pfe_type=None):
        """
        This method return the total lu per pfe

        :param string pfe_type
            **REQUIRED** Type of PFE

        :return: string value for the total numbers of LU instances

        :rtype: string
        """

        if self.platform == 'MX':
            lu_per_pfe = 1
            if pfe_type == 'hyp':
                lu_per_pfe = 4
            elif pfe_type == 'snrkl':
                lu_per_pfe = 2
            return lu_per_pfe

    def get_pfe_number(self, device_handle=None, interface=None):
        """
        This method return pfe number to which interface belongs.

        :param string interface
            **REQUIRED** Interface of router

        :return: string value for pfe number to which interface belongs.

        :rtype: string
        """
        self.dhandle = device_handle
        if self.platform is None:
            self.platform = self.get_chassis_platform_info()
        if self.platform == 'MX':
            rut1 = rutils.rutils()
            fpc_slot, pic_slot, port_num = rut1.get_fpc_pic_port_from_ifname(interface)
            del rut1
            pic_slot = int(pic_slot)
            port_num = int(port_num)
            output = self.dhandle.cli(
                command="show chassis fpc pic-status | match \"Slot %s\"" %
                str(fpc_slot)).response()
            pfe_type = self.get_pfe_type(device_handle, fpc_slot)
            pfe_num = pic_slot
            if pfe_type == 'aloha2':
                pfe_num = 0
            elif pfe_type == 'vfpc' or pfe_type == 'vzt':
                pfe_num = 0
            elif pfe_type == 'mx104' or pfe_type == 'summit_1ru':
                pfe_num = 0
            elif 'MPCE Type 3 3D' in output:
                pfe_num = 0
            elif 'MPC3E NG' in output:
                pfe_num = 0
            elif pfe_type == 'neo' and (pic_slot == 0 or pic_slot == 1):
                pfe_num = 0
            elif pfe_type == 'neo' and (pic_slot == 2 or pic_slot == 3):
                pfe_num = 1
            elif pfe_type == 'snrkl' and (pic_slot == 0 or pic_slot == 1):
                pfe_num = 0
            elif pfe_type == 'snrkl' and (pic_slot == 2 or pic_slot == 3):
                pfe_num = 1
            elif pfe_type == 'as' or pfe_type == 'ferrari10':
                pfe_num = pic_slot
            elif pfe_type == 'redbull':
                pfe_num = pic_slot
            elif pfe_type == 'xl5':
                pfe_num = 0
            elif pfe_type == 'xl6' and pic_slot == 0:
                pfe_num = 0
            elif pfe_type == 'xl6' and pic_slot == 1:
                pfe_num = 1
            elif pfe_type == 'stout2' and pic_slot == 0 and (port_num <= 5):
                pfe_num = 0
            elif pfe_type == 'stout2' and pic_slot == 0 and (port_num > 5):
                pfe_num = 1
            elif pfe_type == 'stout2' and pic_slot == 1 and (port_num <= 5):
                pfe_num = 2
            elif pfe_type == 'stout2' and pic_slot == 1 and (port_num > 5):
                pfe_num = 3
            elif pfe_type == 'summit' and pic_slot == 0:
                if port_num == 0 or port_num == 1:
                    pfe_num = 0
                elif port_num == 2 or port_num == 3:
                    pfe_num = 1
                elif port_num == 4 or port_num == 5:
                    pfe_num = 2
            elif pfe_type == 'summit' and pic_slot != 0:
                if port_num >= 0 and port_num <= 3:
                    pfe_num = 0
                elif port_num >= 4 and port_num <= 7:
                    pfe_num = 1
                elif port_num >= 8 and port_num <= 11:
                    pfe_num = 2
            elif pfe_type == 'vale8edge':
                pfe_num = pic_slot
            return pfe_num

    def get_all_observation_domain_ids(self, device_handle, **kwg):
        """
        This method will retrieve all the possible observation domain \
        Ids or source Ids per template type.

        :param obj device_handle
            **REQUIRED** Router handle

        :param string sampling_interface
            **OPTIONAL** Interface where sampling has been enabled

        :param string fpc_slot
            **OPTIONAL** fpc where sampling has been enabled

        :param string template_type
            **OPTIONAL** family name for which sampling is enabled

        :param string configured_obs_domainid
             **OPTIONAL** if user has manually configured the observation domain
                          Id then user must pass that value using this key.

        :return: list of all observation domain ids

        :rtype: list


        Example::

            python:
                get_all_observation_domain_ids(
                    device_handle = router_handle,
                    sampling_interface='ge-0/0/5',
                    template_type = 'ipv4'
                    )
                    Or
                get_all_observation_domain_ids(
                    device_handle = router_handle,
                    fpc_slot='0',
                    template_type = 'ipv6'
                    )
                    Or
                get_all_observation_domain_ids(
                    device_handle = router_handle,
                    fpc_slot='0',
                    configured_obs_domainid = 24999,
                    template_type = 'mpls'
                    )
                    Or
                get_all_observation_domain_ids(
                    device_handle = router_handle,
                    sampling_interface='ge-0/0/5',
                    configured_obs_domainid = 44455,
                    template_type = 'mpls-v4'
                    )
                                                  ]
            Robot:
                Get All Observation Domain Ids    device_handle = {$router_handle}\
                    sampling_interface=ge-0/0/5   template_type = ipv4
                    Or
                Get All Observation Domain Ids    device_handle = {$router_handle}\
                    fpc_slot=0   template_type=ipv4
                    Or
                Get All Observation Domain Ids    device_handle = {$router_handle}\
                    fpc_slot=0   template_type=ipv4    configured_obs_domainid=24999
                    Or
                Get All Observation Domain Ids    device_handle = {$router_handle}\
                    sampling_interface=ge-0/0/5   template_type=mpls-v4    \
                    configured_obs_domainid=44455
        """
        if self.platform == 'MX' and self.jflow_type == 'INLINE':
            rut1 = rutils.rutils()
            if 'sampling_interface' in kwg:
                fpc_slot, pic_slot, port_num = rut1.get_fpc_pic_port_from_ifname(
                    kwg['sampling_interface'])
            elif 'fpc_slot' in kwg:
                fpc_slot = kwg['fpc_slot']
            else:
                fpc_slot, pic_slot, port_num = rut1.get_fpc_pic_port_from_ifname(
                    self.sampling_interface)
            fpc_slot = str(fpc_slot)
            if 'template_type' in kwg:
                template_type = kwg['template_type']
            else:
                template_type = self.template_type
            del rut1
            del pic_slot
            del port_num
            obs_dmn_ids = []
            configured_obs_domainid = kwg.get('configured_obs_domainid', '0')
            configured_obs_domainid_bin = str(
                bin(int(configured_obs_domainid)))[2:].zfill(8)
            pfe_type = self.get_pfe_type(device_handle, fpc_slot)
            tot_pfe = self.get_total_pfe_instance(pfe_type)
            lu_per_pfe = self.get_total_lu_per_pfe(pfe_type)
            for pfe in range(tot_pfe):
                for lu_inst in range(lu_per_pfe):
                    if template_type == 'ipv4':
                        proto = '000'
                    elif template_type == 'ipv6':
                        proto = '001'
                    elif template_type == 'mpls':
                        proto = '011'
                    elif template_type == 'mpls-ipv4' and float(self.jflow_template_version) <= 18.1:
                        proto = '011'
                    elif template_type == 'mpls-ipv4' and float(self.jflow_template_version) >= 18.3:
                        proto = '101'
                    elif template_type == 'mpls-ipv6' and float(self.jflow_template_version) >= 18.3:
                        proto = '110'
                    elif template_type == 'vpls' or template_type == 'bridge':
                        proto = '100'
                    proto = '1' + proto
                    if pfe_type == 'mx104':
                        fpc_bin = '00000000'
                    else:
                        fpc_bin = str(bin(int(fpc_slot)))[2:].zfill(8)
                    pfe_bin = str(bin(pfe))[2:].zfill(4)
                    lu_bin = str(bin(lu_inst))[2:].zfill(4)
                    #conf = '00000000'
                    conf = configured_obs_domainid_bin
                    zzz = '0000'
                    observation_domain_id_bin = conf + zzz + proto + fpc_bin + lu_bin + pfe_bin
                    observation_domain_id = str(int(observation_domain_id_bin, 2))
                    obs_dmn_ids.append(observation_domain_id)
            return obs_dmn_ids

    def get_sampling_observation_domain_id(self, device_handle, **kwg):
        """
        This method will retrieve all possible sampling observation domain \
        Ids or source Ids per template type.

        :param obj device_handle
            **REQUIRED** Router handle

        :param string sampling_interface
            **OPTIONAL** Interface where sampling has been enabled

        :param string fpc_slot
            **OPTIONAL** fpc where sampling has been enabled

        :param string template_type
            **OPTIONAL** family name for which sampling is enabled

        :param string configured_obs_domainid
             **OPTIONAL** if user has manually configured the observation domain
                          Id then user must pass that value using this key.

        :return: list of all observation domain ids

        :rtype: list


        Example::

            python:
                get_sampling_observation_domain_id(
                    device_handle = router_handle,
                    sampling_interface='ge-0/0/5',
                    template_type = 'ipv4'
                    )
                    Or
                get_sampling_observation_domain_id(
                    device_handle = router_handle,
                    fpc_slot='0',
                    template_type = 'ipv6'
                    )
                    Or
                get_sampling_observation_domain_id(
                    device_handle = router_handle,
                    fpc_slot='0',
                    configured_obs_domainid = 24999,
                    template_type = 'mpls'
                    )
                    Or
                get_sampling_observation_domain_id(
                    device_handle = router_handle,
                    sampling_interface='ge-0/0/5',
                    configured_obs_domainid = 44455,
                    template_type = 'mpls-v4'
                    )
                                                  ]
            Robot:
                Get Sampling Observation Domain Id    device_handle = {$router_handle}\
                    sampling_interface=ge-0/0/5   template_type = ipv4
                    Or
                Get Sampling Observation Domain Id    device_handle = {$router_handle}\
                    fpc_slot=0   template_type=ipv4
                    Or
                Get Sampling Observation Domain Id    device_handle = {$router_handle}\
                    fpc_slot=0   template_type=ipv4    configured_obs_domainid=24999
                    Or
                Get Sampling Observation Domain Id    device_handle = {$router_handle}\
                    sampling_interface=ge-0/0/5   template_type=mpls-v4    \
                    configured_obs_domainid=44455
        """

        self.dhandle = device_handle
        if self.platform is None:
            self.platform = self.get_chassis_platform_info()
        if 'jflow_type' in kwg:
            jflow_type = kwg['jflow_type']
        else:
            jflow_type = 'INLINE'

        self.jflow_type = jflow_type
        if self.platform == 'MX' and self.jflow_type == 'INLINE':
            rut1 = rutils.rutils()
            if 'sampling_interface' in kwg:
                fpc_slot, pic_slot, port_num = rut1.get_fpc_pic_port_from_ifname(
                    kwg['sampling_interface'])
                sampling_interface = kwg['sampling_interface']
            else:
                fpc_slot, pic_slot, port_num = rut1.get_fpc_pic_port_from_ifname(
                    self.sampling_interface)
                sampling_interface = self.sampling_interface

            if 'template_type' in kwg:
                template_type = kwg['template_type']
            else:
                template_type = self.template_type

            if 'jflow_template_version' in kwg:
                jflow_template_version = kwg['jflow_template_version']
            else:
                jflow_template_version = self.jflow_template_version

            del rut1
            del pic_slot
            del port_num
            configured_obs_domainid = kwg.get('configured_obs_domainid', '0')
            configured_obs_domainid_bin = str(
                bin(int(configured_obs_domainid)))[2:].zfill(8)
            sampling_obs_dmn_ids = []
            pfe_type = self.get_pfe_type(device_handle, fpc_slot)
            pfe_num = self.get_pfe_number(device_handle, interface=sampling_interface)
            lu_per_pfe = self.get_total_lu_per_pfe(pfe_type)
            for lu_inst in range(lu_per_pfe):
                if template_type == 'ipv4':
                    proto = '000'
                elif template_type == 'ipv6':
                    proto = '001'
                elif template_type == 'mpls':
                    proto = '011'
                elif template_type == 'mpls-ipv4' and float(jflow_template_version) <= 18.1:
                    proto = '011'
                elif template_type == 'mpls-ipv4' and float(jflow_template_version) >= 18.3:
                    proto = '101'
                elif template_type == 'mpls-ipv6' and float(jflow_template_version) >= 18.3:
                    proto = '110'
                elif template_type == 'vpls' or template_type == 'bridge':
                    proto = '100'
                proto = '1' + proto
                if pfe_type == 'mx104':
                    fpc_bin = '00000000'
                else:
                    fpc_bin = str(bin(int(fpc_slot)))[2:].zfill(8)
                pfe_bin = str(bin(pfe_num))[2:].zfill(4)
                lu_bin = str(bin(lu_inst))[2:].zfill(4)
                conf = configured_obs_domainid_bin
                zzz = '0000'
                observation_domain_id_bin = conf + zzz + proto + fpc_bin + lu_bin + pfe_bin
                observation_domain_id = str(int(observation_domain_id_bin, 2))
                sampling_obs_dmn_ids.append(observation_domain_id)
            return sampling_obs_dmn_ids

    def verify_flow_sequence(self, **kwarg):
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
        if self.platform == 'MX':
            status = self.verify_mx_flow_sequence(**kwarg)
            self.flow_seq_verification_status = status
            if status is True:
                self.log("INFO","Flow-sequence verification passed")
            else:
                self.log("ERROR","Flow-sequence verification failed")
            return status

    def verify_mx_flow_sequence(self, **kwarg):
        """
        This method will perform the flow sequence verification per observation domain
        on MX platform only

        :return: True if verification succeed per observation domain id else False

        :rtype: bool
        """
        if 'obs_dmn_ids' in kwarg:
            obs_dmn_ids = kwarg['obs_dmn_ids']
        else:
            obs_dmn_ids = self.obs_dmn_ids
        flow_seq_check_dict = {}
        for obs_dmn_tmp in obs_dmn_ids:
            self.log("INFO", \
                "Started Validating the Flow Sequence for "\
                "Observation domain ID :- %s" %str(obs_dmn_tmp))
            seq_status = self._verify_flow_sequence_and_template_refresh_rate(obs_dmn_tmp, **kwarg)
            flow_seq_status = copy.deepcopy(seq_status)
            if flow_seq_status['data_flow_seq_check'] is True:
                self.log("INFO", \
                    "For observation domain Id : %s --> Flow sequence for data "\
                    "template and data record is correct" %\
                    str(obs_dmn_tmp))
            elif flow_seq_status['data_flow_seq_check'] is False:
                self.log("ERROR", \
                    "For observation domain Id : %s --> Flow sequence for data "\
                    "template and data record is wrong" %\
                    str(obs_dmn_tmp))
            else:
                self.log("ERROR", \
                    "For observation domain Id : %s --> Invalid to test as either "\
                    "one data template or no data template captured . Capture min "\
                    "2 for validation . Run TCPDUMP for more than twice the time "\
                    "of data template refresh rate" %str(obs_dmn_tmp))
                flow_seq_status['data_flow_seq_check'] = "Invalid to test as data"\
                " template captured packet is less than 2"
            if flow_seq_status['option_flow_seq_check'] is True:
                self.log("INFO", "For observation domain Id : %s --> Flow sequence "\
                "for option template and option data is correct" %str(obs_dmn_tmp))
            elif flow_seq_status['option_flow_seq_check'] is False:
                self.log("ERROR", "For observation domain Id : %s --> Flow sequence "\
                "for option template and option data is "\
                "wrong" %str(obs_dmn_tmp))
            else:
                self.log("ERROR", "For observation domain Id : %s --> Invalid to test "\
                "as either one option template/data captured or no option "\
                "template/data captured . Capture min 2 for validation . "\
                "Run TCPDUMP for more than twice the time of option "\
                "template refresh rate" % str(obs_dmn_tmp))
                flow_seq_status['option_flow_seq_check'] = \
                "Invalid to test as option template/option data captured packet is less than 2"
            #if flow_seq_status['data_flow_seq_check'] is True and \
            #flow_seq_status['option_flow_seq_check'] is True:
            #    flow_seq_check_dict[obs_dmn_tmp] = True
            #else:
            #    flow_seq_check_dict[obs_dmn_tmp] = Fals

            flow_seq_check_dict[obs_dmn_tmp] = \
            bool(flow_seq_status['option_flow_seq_check'] \
            and flow_seq_status['data_flow_seq_check'])
        self.log("INFO", "flow_seq_check_dict : %s"%flow_seq_check_dict)
        for obs_check in flow_seq_check_dict:
            if flow_seq_check_dict[obs_check] is not True:
                self.final_flow_seq_status = False
                return False
        self.final_flow_seq_status = True
        return True

    def verify_templates_timestamps_and_refresh_rate(self, **kwarg):
        """
        This method will perform the templates rate verification per observation domain.
        Both Data template and option template refresh rate values will be calculated.
        if both verification passed then method will return True else False

        :param: string tcpdump_start_time
            **REQUIRED** epoch time retrieved from the router when tcpdump was started

        :param: string tcpdump_stop_time
            **REQUIRED** epoch time retrieved from the router when tcpdump was stopped

        :param: string template_refresh_rate
            **OPTIONAL** Data template refresh rate value configured.
                         Default value will be 10.

        :param: string option_refresh_rate
            **OPTIONAL** Option template refresh rate value configured.
                         Default value will be 30.

        :return: True if verification succeed per observation domain id else False

        :rtype: bool


        Example::

            python:
                obj.init( PASS ALL MANATORY PARAMETERS MENTIONED IN init)
                status = obj.verify_templates_timestamps_and_refresh_rate(
                                 tcpdump_start_time = 111100,
                                 tcpdump_stop_time = 111200,
                                 )
                    Or
                status = obj.verify_templates_timestamps_and_refresh_rate(
                                 tcpdump_start_time = 111100,
                                 tcpdump_stop_time = 111200,
                                 template_refresh_rate = 20
                                 option_refresh_rate = 20
                                 )
            Robot:
                ${status}=  Jf.Verify Templates Timestamps And Refresh Rate
                                  template_refresh_rate=10   option_refresh_rate=30
                                  tcpdump_start_time=${tcpdump_start_time}
                                  tcpdump_stop_time=${tcpdump_stop_time}
                    Or
                ${status}=  Jf.Verify Templates Timestamps And Refresh Rate
                                   tcpdump_start_time=${tcpdump_start_time}
                                   tcpdump_stop_time=${tcpdump_stop_time}
                Should Be True     ${status}
        """

        if self.platform == 'MX':
            status = self.verify_mx_refresh_rates(**kwarg)
            self.template_refresh_rate_status = status
            if status is True:
                self.log("INFO","Template refresh rate verification passed")
            else:
                self.log("ERROR","Template refresh rate verification failed")
            return status

    def verify_mx_refresh_rates(self, **kwarg):
        """
        This method will perform the templates rate verification per observation domain
        only on mx platform.
        Both Data template and option template refresh rate values will be calculated.
        if both verification passed then method will return True else False

        :param: string tcpdump_start_time
            **REQUIRED** epoch time retrieved from the router when tcpdump was started

        :param: string tcpdump_stop_time
            **REQUIRED** epoch time retrieved from the router when tcpdump was stopped

        :param: string template_refresh_rate
            **OPTIONAL** Data template refresh rate value configured.
                         Default value will be 10.

        :param: string option_refresh_rate
            **OPTIONAL** Option template refresh rate value configured.
                         Default value will be 30.

        :return: True if verification succeed per observation domain id else False

        :rtype: bool

        """
        default_refresh_rate = None

        if "template_refresh_rate" in kwarg:
            self.template_refresh_rate = kwarg["template_refresh_rate"]
            template_refresh_rate = self.template_refresh_rate
        if self.template_refresh_rate is None:
            if self.cflow_version == '9':
                default_refresh_rate = 60
            else:
                default_refresh_rate = 600
            self.template_refresh_rate = default_refresh_rate
            template_refresh_rate = self.template_refresh_rate
        else:
            template_refresh_rate = self.template_refresh_rate

        if "option_refresh_rate" in kwarg:
            self.option_refresh_rate = kwarg["option_refresh_rate"]
            option_refresh_rate = self.option_refresh_rate

        if self.option_refresh_rate is None:
            if self.cflow_version == '9':
                default_refresh_rate = 60
            else:
                default_refresh_rate = 600
            self.option_refresh_rate = default_refresh_rate
            option_refresh_rate = self.option_refresh_rate
        else:
            option_refresh_rate = self.option_refresh_rate


        tcpdump_start_time = kwarg.get('tcpdump_start_time', None)
        if tcpdump_start_time is None:
            raise ValueError("Tcpdump start time not provided . "\
            "please provide both start and end time to validate "\
            "the templates timestamps")
        tcpdump_stop_time = kwarg.get('tcpdump_stop_time', None)
        if tcpdump_stop_time is None:
            raise ValueError(
                "Tcpdump stop time not provided . "\
                 "please provide both start and end time to "\
                 "validate the templates timestamps")
        if 'obs_dmn_ids' in kwarg:
            obs_dmn_ids = kwarg['obs_dmn_ids']
        else:
            obs_dmn_ids = self.obs_dmn_ids
        timestamp_check_dict = {}
        for obs_dmn_tmp in obs_dmn_ids:
            self.log("INFO", "Started Validating the template timestamp "\
            "for Observation domain ID :- %s" %str(obs_dmn_tmp))
            refresh_rate_status = self._verify_flow_sequence_and_template_refresh_rate(
                obs_dmn_tmp, **kwarg)
            template_refresh_rate_status = copy.deepcopy(refresh_rate_status)
            ####################
            self.data_template_first_timestamp = \
            template_refresh_rate_status['data_template_first_timestamp']
            self.option_template_first_timestamp = \
            template_refresh_rate_status['option_template_first_timestamp']
            self.data_template_last_timestamp = \
            template_refresh_rate_status['data_template_last_timestamp']
            self.option_template_last_timestamp = \
            template_refresh_rate_status['option_template_last_timestamp']
            ####################
            if template_refresh_rate_status['first_data_template_received_timestamp_status'] \
            is True and template_refresh_rate_status\
['last_data_template_received_timestamp_status'] is True:
                if template_refresh_rate_status['Data_template_timestamp_verify_status'] is True:
                    self.log("INFO", "For observation domain Id : %s -->  "\
                    "All the data templates recieved at collector"\
                    " and export time for each packet is correct" %str(obs_dmn_tmp))
                    template_refresh_rate_status['Data_template_timestamp_final_validation_status']\
                    = True
                else:
                    self.log("ERROR", "For observation domain Id : %s --> Error seen "\
                    "while validating export time for data templates" %str(obs_dmn_tmp))
                    template_refresh_rate_status['Data_template_timestamp_'\
                    'final_validation_status'] = False
            elif template_refresh_rate_status['first_data_template_received_timestamp_status'] \
            is True and template_refresh_rate_status\
['last_data_template_received_timestamp_status'] is False:
                if template_refresh_rate_status['Data_template_timestamp_verify_status'] is True:
                    packets_expected_at_end = (int(tcpdump_stop_time) - \
                    int(template_refresh_rate_status['data_template_last_timestamp'])) \
                    / int(template_refresh_rate)
                    self.log("ERROR", "For observation domain Id : %s --> Error found as we "\
                    "expected %s data templates packet at the end" %(str(obs_dmn_tmp), \
                    str(int(packets_expected_at_end))))
                    template_refresh_rate_status['Data_template_'\
                    'timestamp_final_validation_status'] = False
                else:
                    self.log("ERROR", "For observation domain Id : %s --> Error "\
                    "seen while validating export time for data "\
                    "templates" %str(obs_dmn_tmp))
                    template_refresh_rate_status['Data_template_'\
                    'timestamp_final_validation_status'] = False
            elif template_refresh_rate_status['first_data_'\
            'template_received_timestamp_status'] is False and \
            template_refresh_rate_status['last_data_template_'\
            'received_timestamp_status'] is True:
                if template_refresh_rate_status['Data_template_timestamp_verify_status'] is True:
                    packets_expected_at_start = (int(template_refresh_rate_status\
['data_template_first_timestamp']) - int(tcpdump_start_time)) \
                    / int(template_refresh_rate)
                    self.log("ERROR", \
                    "For observation domain Id : %s --> Error found "\
                    "as we expected %s data templates packet at the Start of capture" \
                    %(str(obs_dmn_tmp), str(int(packets_expected_at_start))))
                    template_refresh_rate_status['Data_template_'\
                    'timestamp_final_validation_status'] = False
                else:
                    self.log("ERROR", \
                    "For observation domain Id : %s --> Error seen while "\
                    "validating export time for data templates" %str(obs_dmn_tmp))
                    template_refresh_rate_status['Data_template_'\
                    'timestamp_final_validation_status'] = False
            elif template_refresh_rate_status['first_data_'\
            'template_received_timestamp_status'] is None:
                self.log("ERROR", \
                    "For observation domain Id : %s --> No Data template "\
                    "packet found in the tcpdump capture" %str(obs_dmn_tmp))
                template_refresh_rate_status['Data_template_'\
                'timestamp_final_validation_status'] = "No Captured "\
                "packet -- Invalid to test"

            if template_refresh_rate_status['first_option_template_'\
            'received_timestamp_status'] is True \
            and template_refresh_rate_status['last_option_template_received_timestamp_status'] \
            is True and template_refresh_rate_status['first_option_data_'\
            'received_timestamp_status'] is True and \
            template_refresh_rate_status['last_option_data_received_'\
            'timestamp_status'] is True:
                if template_refresh_rate_status['Options_timestamp_verify_status'] \
                is True:
                    self.log("INFO", \
                        "For observation domain Id : %s --> All the option templates "\
                        "and options data recieved at collector and export time for "\
                        "each packet is correct" %str(obs_dmn_tmp))
                    template_refresh_rate_status['Options_timestamp_'\
                    'final_validation_status'] = True
                else:
                    self.log("ERROR", \
                        "For observation domain Id : %s --> Error seen "\
                         "while validating export time for option "\
                         "template/data " %str(obs_dmn_tmp))
                    template_refresh_rate_status['Options_timestamp_'\
                    'final_validation_status'] = False
            elif template_refresh_rate_status['first_option_template_'\
            'received_timestamp_status'] is True and template_refresh_rate_status['last_option_'\
            'template_received_timestamp_status'] is False and \
            template_refresh_rate_status['first_option_data_received_'\
            'timestamp_status'] is True \
            and template_refresh_rate_status['last_option_data_received_'\
            'timestamp_status'] is False:
                if template_refresh_rate_status['Options_timestamp_'\
                'verify_status'] is True:
                    packets_expected_at_end = (int(tcpdump_stop_time) - \
                    int(template_refresh_rate_status['option_template_last_timestamp'])) \
                    / int(option_refresh_rate)
                    self.log("ERROR", \
                        "For observation domain Id : %s --> Error found as we "\
                        "expected %s Option template and Option data packet at "\
                        "the end"%(str(obs_dmn_tmp), str(int(packets_expected_at_end))))
                    template_refresh_rate_status['Options_timestamp_final_validation_'\
                    'status'] = False
                else:
                    self.log("ERROR", \
                        "For observation domain Id : %s --> Error seen while "\
                        "validating export time for Option templates / Option "\
                        "Data"%str(obs_dmn_tmp))
                    template_refresh_rate_status['Options_timestamp_final_'\
                    'validation_status'] = False
            elif template_refresh_rate_status['first_option_template_'\
            'received_timestamp_status'] is False and template_refresh_rate_status['last_option_'\
            'template_received_timestamp_status'] is True and template_refresh_rate_status['first_'\
            'option_data_received_timestamp_status'] is False and \
            template_refresh_rate_status['last_option_data_received'\
            '_timestamp_status'] is True:
                if template_refresh_rate_status['Options_timestamp_verify_status'] is True:
                    packets_expected_at_start = (int(
                        template_refresh_rate_status['option_template_first_timestamp']) \
                        - int(tcpdump_start_time)) / int(option_refresh_rate)
                    self.log("ERROR", \
                        "For observation domain Id : %s -->Error found as we "\
                        "expected %s Option templates and Option data packet at "\
                        "the start"%(str(obs_dmn_tmp), str(int(packets_expected_at_start))))
                    template_refresh_rate_status['Options_timestamp_'\
                    'final_validation_status'] = False
                else:
                    self.log("ERROR", \
                        "For observation domain Id : %s --> Error seen while "\
                         "validating export time for option templates" %str(obs_dmn_tmp))
                    template_refresh_rate_status['Options_timestamp_final_'\
                    'validation_status'] = False
            elif template_refresh_rate_status['first_option_template_'\
            'received_timestamp_status'] is None and template_refresh_rate_status['first'\
           '_option_data_received_timestamp_status'] is None:
                self.log("ERROR", \
                    "For observation domain Id : %s --> No Option template packet "\
                    "and No Option Data packet found in the tcpdump capture" %str(obs_dmn_tmp))
                template_refresh_rate_status['Options_timestamp_final_'\
                'validation_status'] = "No packets captured related to "\
                "Option Data and template -- Invalid to test"
            else:
                if template_refresh_rate_status['Options_timestamp_'\
                'verify_status'] is False:
                    self.log("ERROR", \
                        "For observation domain Id : %s --> Error seen "\
                        "while validating export time for option template/data "%str(obs_dmn_tmp))
                    template_refresh_rate_status['Options_timestamp_final_'\
                    'validation_status'] = False

            #if template_refresh_rate_status['Options_timestamp_final_\
            #validation_status'] is True and template_refresh_rate_status['Data_template_\
            #timestamp_final_validation_status'] is True:
            #    timestamp_check_dict[obs_dmn_tmp] = True
            #else:
            #    timestamp_check_dict[obs_dmn_tmp] = False

            timestamp_check_dict[obs_dmn_tmp] = \
            bool(template_refresh_rate_status['Options_timestamp_final_validation_status'] and \
            template_refresh_rate_status['Data_template_timestamp_final_validation_status'])

        self.log("INFO", "timestamp_check_dict : %s"%timestamp_check_dict)
        for obs_check in timestamp_check_dict:
            if timestamp_check_dict[obs_check] is not True:
                return False
        return True

    def _verify_flow_sequence_and_template_refresh_rate(self, obs_dmn_tmp, **kwarg):
        """
        This methode will be internally called by method \
        "verify_templates_timestamps_and_refresh_rate"

        :param: string tcpdump_start_time
            **REQUIRED** epoch time retrieved from the router when tcpdump was started

        :param: string tcpdump_stop_time
            **REQUIRED** epoch time retrieved from the router when tcpdump was stopped

        :param: string template_refresh_rate
            **OPTIONAL** Data template refresh rate value configured.
                         Default value will be 10.

        :param: string option_refresh_rate
            **OPTIONAL** Option template refresh rate value configured.
                         Default value will be 30.

        :return: dictionary containing keys which inform overall verification status for
                 data , data template , option template and option data.
                 It includes flow sequence verification status , timestamp value ,
                 first timestamp for all kinds of template , last timestamp value for
                 all kinds of template.

        :rtype: dict
        """
        default_refresh_rate = None

        if "template_refresh_rate" in kwarg:
            self.template_refresh_rate = kwarg["template_refresh_rate"]
            template_refresh_rate = self.template_refresh_rate
        if self.template_refresh_rate is None:
            if self.cflow_version == '9':
                default_refresh_rate = 60
            else:
                default_refresh_rate = 600
            self.template_refresh_rate = default_refresh_rate
            template_refresh_rate = self.template_refresh_rate
        else:
            template_refresh_rate = self.template_refresh_rate

        if "option_refresh_rate" in kwarg:
            self.option_refresh_rate = kwarg["option_refresh_rate"]
            option_refresh_rate = self.option_refresh_rate

        if self.option_refresh_rate is None:
            if self.cflow_version == '9':
                default_refresh_rate = 60
            else:
                default_refresh_rate = 600
            self.option_refresh_rate = default_refresh_rate
            option_refresh_rate = self.option_refresh_rate
        else:
            option_refresh_rate = self.option_refresh_rate

        tcpdump_start_time = kwarg.get('tcpdump_start_time', 0)
        tcpdump_stop_time = kwarg.get('tcpdump_stop_time', 0)
        option_refresh_rate = int(option_refresh_rate)
        template_refresh_rate = int(template_refresh_rate)
        obs_dmn_tmp = str(obs_dmn_tmp)
        ifile = self.tshark_output
        ifile = ifile.replace('\r\n', '\n')
        v9_data_template_lists = ["(Data) (320)", "(Data) (321)", "(Data) (323)", "(Data) (324)", "(Data) (327)"]
        v9_option_template_lists = ["(Data) (576)", "(Data) (577)", "(Data) (579)", "(Data) (580)", "(Data) (583)"]
        ipfix_data_template_lists = [
            "(Data) (256)",
            "(Data) (257)",
            "(Data) (258)",
            "(Data) (259)",
            "(Data) (260)",
            "(Data) (263)"]
        ipfix_option_template_lists = [
            "(Data) (512)",
            "(Data) (513)",
            "(Data) (514)",
            "(Data) (515)",
            "(Data) (516)",
            "(Data) (519)"]

        if self.cflow_version == '9':
            v9_data_template_lists.append(self.expected_data_pkt_flowset_name)
            v9_option_template_lists.append(self.exp_optionpkt_flowset)

        if self.cflow_version == '10':
            ipfix_data_template_lists.append(self.expected_data_pkt_flowset_name)
            ipfix_option_template_lists.append(self.exp_optionpkt_flowset)

        #cflow_list = re.findall(r'(Cisco NetFlow[/]IPFIX(\n.*?)*Frame\s\d+:)',ifile)
        cfl = re.findall(r'(Cisco NetFlow[/]IPFIX.*?Frame\s\d+:)', ifile, re.DOTALL)
        #print("cflow_list : \n",cflow_list)
        cflow_list = []
        for pkt in cfl:
            if 'SourceId: %s' % obs_dmn_tmp in pkt or \
            'Observation Domain Id: %s' % obs_dmn_tmp in pkt:
                cflow_list.append(pkt)
        lst = ''
        for each_line in ifile.splitlines()[::-1]:
            lst = each_line + "\n"  + lst
            lst = lst.rstrip()
            last_frame_matches = re.search(r'Frame (\d+): \d+ bytes.*', each_line)
            if last_frame_matches :
                last_frame_number = last_frame_matches.group(1)
                break

        #last_element = re.search(r'Cisco NetFlow[/]IPFIX(\n.*)*',m[1])
        last_element = re.search(
            r'Cisco NetFlow[/]IPFIX(\n.*?)*(?:SourceId:|Observation Domain Id:) %s(?:.*\n.*)*' %
            obs_dmn_tmp, lst)
        if last_element:
            cflow_list.append(last_element.group())
            cflow_list[-1] = last_frame_number + "\n" + cflow_list[-1]

        count = 0
        for cflow in cflow_list:
            #print("cflow : ",count,"\n ",cflow)
            frame_check = re.search(r'Frame (\d+):$', cflow)
            if frame_check:
                frame_found = frame_check.group()
                frame_num = frame_check.group(1)
                cflow_list[count] = cflow_list[count].replace(frame_found, '')
                cflow_list[count] = "Frame " + str(int(frame_num) - 1) + ":\n" + cflow_list[count]
            count = count + 1
        option_temp_count = 0
        option_data_count = 0
        data_temp_count = 0
        option_temp = None
        data_temp = None
        option_flow_seq_check = True
        data_flow_seq_check = True
        options_tstamp_status = True
        data_temp_tstamp_status = True
        #option time execeeded by 1 sec
        option_execeeded_onesec = 0
        #data template time execeeded by 1 sec
        datatemp_execeeded_onesec = 0
        data_template_first_found = 0
        data_record_first_found = 0

        for cflow in cflow_list:
            flow_seq = re.search(r'FlowSequence: (\d+)', cflow)
            current_flow_seq = int(flow_seq.group(1))
            template_type = re.search(r'FlowSet Id: (.*)', cflow)
            template_type = template_type.group(1)
            current_epoch_timestamp = re.search(r'CurrentSecs: \d+|ExportTime: \d+', cflow)
            current_epoch_timestamp = re.search(r'\d+', current_epoch_timestamp.group())
            current_epoch_timestamp = int(current_epoch_timestamp.group())
            if ((template_type == "Options Template(V9) (1)") or \
            (template_type == "Options Template (V10 [IPFIX]) (3)")) \
            and option_temp is None:
                option_temp = True
                option_flow_seq = current_flow_seq
                expected_options_flow_seq = option_flow_seq

                options_current_epoch_timestamp = current_epoch_timestamp
                expected_options_epoch_tstamp = options_current_epoch_timestamp
                option_temp_count = option_temp_count + 1
                if option_temp_count == 1:
                    option_template_first_timestamp = options_current_epoch_timestamp
                    option_template_last_timestamp = options_current_epoch_timestamp
                    diff = int(option_template_first_timestamp) - int(tcpdump_start_time)
                    if diff <= int(option_refresh_rate):
                        first_option_temp_tstamp_status = True
                    elif diff > int(option_refresh_rate):
                        first_option_temp_tstamp_status = False
            elif ((template_type in v9_option_template_lists) \
            or (template_type in ipfix_option_template_lists)) \
            and option_temp is None:
                option_temp = True
                option_flow_seq = current_flow_seq
                expected_options_flow_seq = option_flow_seq + 1

                options_current_epoch_timestamp = current_epoch_timestamp
                expected_options_epoch_tstamp = options_current_epoch_timestamp + \
                    int(option_refresh_rate)
                option_data_count = option_data_count + 1
                if option_data_count == 1:
                    option_data_first_timestamp = options_current_epoch_timestamp
                    option_data_last_timestamp = options_current_epoch_timestamp
                    diff = int(option_data_first_timestamp) - int(tcpdump_start_time)
                    if diff <= int(option_refresh_rate):
                        first_option_data_tstamp_status = True
                    elif diff > int(option_refresh_rate):
                        first_option_data_tstamp_status = False

            elif (((template_type == "Options Template(V9) (1)") \
            or (template_type == "Options Template (V10 [IPFIX]) (3)")) \
            and option_temp is True) or \
            ((((template_type == "Options Template(V9) (1)") or \
            (template_type == "Options Template (V10 [IPFIX]) (3)")) and \
            option_temp is False) and options_tstamp_status is True):
                option_flow_seq = current_flow_seq
                options_current_epoch_timestamp = current_epoch_timestamp
                option_temp_count = option_temp_count + 1
                if option_flow_seq == expected_options_flow_seq and option_temp is True:
                    expected_options_flow_seq = option_flow_seq
                elif option_flow_seq != expected_options_flow_seq and option_temp is True:
                    option_temp = False
                    option_flow_seq_check = False
                    self.log("INFO", "expected Options Template flow "\
                    "sequence : %s"%expected_options_flow_seq)
                    self.log("INFO", "Actual Options Template "\
                    "flow sequence : %s"%option_flow_seq)
                    self.log("INFO", "Error found here : %s"%cflow)
                    # break;
                if options_current_epoch_timestamp == expected_options_epoch_tstamp \
                and options_tstamp_status is True:
                    expected_options_epoch_tstamp = options_current_epoch_timestamp
                elif (options_current_epoch_timestamp == expected_options_epoch_tstamp + 1) \
                and (options_tstamp_status is True):
                    self.log("INFO", \
                        "time stamp didn't matched for Option template but 1 "\
                         "second difference is fine \n --> Expected : "\
                         "%s  but Actaully got : %s" %\
                         (expected_options_epoch_tstamp, options_current_epoch_timestamp))
                    expected_options_epoch_tstamp = options_current_epoch_timestamp
                    option_execeeded_onesec = option_execeeded_onesec + 1
                elif ((options_current_epoch_timestamp != expected_options_epoch_tstamp) \
                or (options_current_epoch_timestamp != expected_options_epoch_tstamp + 1)) \
                and (options_tstamp_status is True):
                    self.log("INFO", \
                        "time stamp didn't matched for Option template --> Expected : "\
                        "%s but Actaully got : %s " %\
                        (expected_options_epoch_tstamp, options_current_epoch_timestamp))
                    options_tstamp_status = False
                if option_temp_count == 1:
                    option_template_first_timestamp = options_current_epoch_timestamp
                    option_template_last_timestamp = options_current_epoch_timestamp
                    diff = int(option_template_first_timestamp) - int(tcpdump_start_time)
                    if diff <= int(option_refresh_rate):
                        first_option_temp_tstamp_status = True
                    elif diff > int(option_refresh_rate):
                        first_option_temp_tstamp_status = False
                elif option_temp_count > 1:
                    option_template_last_timestamp = options_current_epoch_timestamp
            elif (((template_type in v9_option_template_lists) \
            or (template_type in ipfix_option_template_lists)) \
            and option_temp is True) or ((((template_type in v9_option_template_lists) \
            or (template_type in ipfix_option_template_lists)) \
            and option_temp is False) and options_tstamp_status is True):
                option_flow_seq = current_flow_seq
                options_current_epoch_timestamp = current_epoch_timestamp
                option_data_count = option_data_count + 1
                if option_flow_seq == expected_options_flow_seq and option_temp is True:
                    expected_options_flow_seq = option_flow_seq + 1
                elif option_flow_seq != expected_options_flow_seq and option_temp is True:
                    option_temp = False
                    option_flow_seq_check = False
                    self.log("INFO", "expected Options Data flow "\
                    "sequence : %s"%expected_options_flow_seq)
                    self.log("INFO", "Actual Options Data flow sequence : %s"%option_flow_seq)
                    self.log("INFO", "Error found here : %s"%cflow)
                    # break;
                if options_current_epoch_timestamp == expected_options_epoch_tstamp \
                and options_tstamp_status is True:
                    expected_options_epoch_tstamp = options_current_epoch_timestamp + \
                        int(option_refresh_rate)
                elif (options_current_epoch_timestamp == expected_options_epoch_tstamp + 1) \
                and (options_tstamp_status is True):
                    self.log("INFO", \
                        "time stamp didn't matched for Option Data but 1 "\
                        "second difference is fine \n --> Expected : "\
                        "%s"\
                        " but Actaully got : %s "%\
                        (expected_options_epoch_tstamp, options_current_epoch_timestamp))
                    expected_options_epoch_tstamp = options_current_epoch_timestamp
                    option_execeeded_onesec = option_execeeded_onesec + 1
                elif ((options_current_epoch_timestamp != expected_options_epoch_tstamp) \
                or (options_current_epoch_timestamp != expected_options_epoch_tstamp + 1)) \
                and (options_tstamp_status is True):
                    print(\
                        "INFO", \
                        "time stamp didn't matched for Option Data --> Expected : "\
                        " %s but Actaully got : %s \n"\
                        %(expected_options_epoch_tstamp, options_current_epoch_timestamp))
                    options_tstamp_status = False
                    expected_options_epoch_tstamp = expected_options_epoch_tstamp + \
                        int(option_refresh_rate)
                if option_data_count == 1:
                    option_data_first_timestamp = options_current_epoch_timestamp
                    option_data_last_timestamp = options_current_epoch_timestamp
                    diff = int(option_data_first_timestamp) - int(tcpdump_start_time)
                    if diff <= int(option_refresh_rate):
                        first_option_data_tstamp_status = True
                    elif diff > int(option_refresh_rate):
                        first_option_data_tstamp_status = False
                elif option_data_count > 1:
                    option_data_last_timestamp = options_current_epoch_timestamp

            elif (template_type == "Data Template (V9) (0)" or \
            template_type == "Data Template (V10 [IPFIX]) (2)") \
            and data_temp is None:
                data_temp = True
                data_flow_seq = current_flow_seq
                expected_data_flow_seq = data_flow_seq

                data_temp_current_epoch_tstamp = current_epoch_timestamp
                expected_data_temp_epoch_tstamp = data_temp_current_epoch_tstamp + \
                    int(template_refresh_rate)
                data_temp_count = data_temp_count + 1
                if data_temp_count == 1:
                    data_template_first_timestamp = data_temp_current_epoch_tstamp
                    data_template_last_timestamp = data_temp_current_epoch_tstamp
                    diff = int(data_template_first_timestamp) - int(tcpdump_start_time)
                    if diff <= int(template_refresh_rate):
                        first_data_temp_tstamp_status = True
                    elif diff > int(template_refresh_rate):
                        first_data_temp_tstamp_status = False

            elif ((template_type in v9_data_template_lists) \
            or (template_type in ipfix_data_template_lists)) \
            and data_temp is None:
                data_temp = True
                # In pcap , we have recieved the data record at first place rather than
                # data template
                data_flow_seq = current_flow_seq
                expected_data_flow_seq = data_flow_seq + 1
                ##########################################################################
                data_record_first_found = 1
                ##########################################################################

            elif ((template_type == "Data Template (V9) (0)" or \
            template_type == "Data Template (V10 [IPFIX]) (2)") and \
            data_temp is True) or (((template_type == "Data Template (V9) (0)" or \
            template_type == "Data Template (V10 [IPFIX]) (2)") and \
            data_temp is False) and data_temp_tstamp_status is True):
                data_flow_seq = current_flow_seq
                data_temp_current_epoch_tstamp = current_epoch_timestamp
                data_temp_count = data_temp_count + 1

                ##########################################################################
                if data_template_first_found == 0 and data_record_first_found == 1:
                    expected_data_temp_epoch_tstamp = data_temp_current_epoch_tstamp
                    data_record_first_found = -1
                    data_template_first_found = -1
                ####################################################################################

                if data_flow_seq == expected_data_flow_seq and data_temp is True:
                    expected_data_flow_seq = data_flow_seq
                elif data_flow_seq != expected_data_flow_seq and data_temp is True:
                    data_temp = False
                    data_flow_seq_check = False
                    self.log("INFO", "expected Data Template "\
                    "flow sequence : %s"%expected_data_flow_seq)
                    self.log("INFO", "Actual Data Template flow \
                    sequence : %s"%data_flow_seq)
                    self.log("INFO", "Error found here : %s"%cflow)
                    # break;
                if data_temp_current_epoch_tstamp == \
                expected_data_temp_epoch_tstamp and \
                data_temp_tstamp_status is True:
                    expected_data_temp_epoch_tstamp = \
                    data_temp_current_epoch_tstamp + \
                    int(template_refresh_rate)
                elif (data_temp_current_epoch_tstamp == \
                expected_data_temp_epoch_tstamp + 1) and \
                (data_temp_tstamp_status is True):
                    self.log("INFO", \
                        "time stamp didn't matched for Data template but 1 second "\
                        "difference is fine \n --> Expected : "\
                        "%s"\
                        " but Actaully got : %s \n"%\
                        (expected_data_temp_epoch_tstamp, data_temp_current_epoch_tstamp))
                    expected_data_temp_epoch_tstamp = \
                    data_temp_current_epoch_tstamp + \
                    int(template_refresh_rate)
                    datatemp_execeeded_onesec = datatemp_execeeded_onesec + 1
                elif ((data_temp_current_epoch_tstamp != \
                expected_data_temp_epoch_tstamp) or \
                (data_temp_current_epoch_tstamp != \
                expected_data_temp_epoch_tstamp + 1)) and \
                (data_temp_tstamp_status is True):
                    self.log("INFO", \
                        "time stamp didn't matched for Data template --> Expected : "\
                        " %s "\
                        " but Actaully got : "\
                        " %s \n"%(expected_data_temp_epoch_tstamp, data_temp_current_epoch_tstamp))
                    data_temp_tstamp_status = False
                    expected_data_temp_epoch_tstamp = \
                    expected_data_temp_epoch_tstamp + \
                        int(template_refresh_rate)
                if data_temp_count == 1:
                    data_template_first_timestamp = data_temp_current_epoch_tstamp
                    data_template_last_timestamp = data_temp_current_epoch_tstamp
                    diff = int(data_template_first_timestamp) - int(tcpdump_start_time)
                    if diff <= int(template_refresh_rate):
                        first_data_temp_tstamp_status = True
                    elif diff > int(template_refresh_rate):
                        first_data_temp_tstamp_status = False
                elif data_temp_count > 1:
                    data_template_last_timestamp = data_temp_current_epoch_tstamp

            elif ((template_type in v9_data_template_lists) or \
            (template_type in ipfix_data_template_lists)) and \
            data_temp is True:
                data_flow_seq = current_flow_seq
                if data_flow_seq == expected_data_flow_seq and \
                template_type in v9_data_template_lists:
                    expected_data_flow_seq = data_flow_seq + 1
                elif data_flow_seq == expected_data_flow_seq and \
                template_type in ipfix_data_template_lists:
                    get_exported_flows_list = re.findall(
                        r'^\s*(Flow \d)\s*\n', cflow, re.M)
                    total_exported_flows = len(get_exported_flows_list)
                    expected_data_flow_seq = data_flow_seq + total_exported_flows
                else:
                    data_temp = False
                    data_flow_seq_check = False
                    self.log("INFO", "expected Data record flow sequence "\
                    ": %s"% expected_data_flow_seq)
                    self.log("INFO", "Actual  Data record flow sequence : %s"%data_flow_seq)
                    self.log("INFO", "Error found here : %s"%cflow)
                    # break;
            else:
                pass
                #print("Not a useful packet")

        if option_temp_count > 1:
            # getting details related last captured option_template_packet
            diff = int(tcpdump_stop_time) - int(option_template_last_timestamp)
            if diff > int(option_refresh_rate):
                last_option_temp_tstamp_status = False
            elif diff <= int(option_refresh_rate):
                last_option_temp_tstamp_status = True
        elif option_temp_count == 1:
            # getting details related last captured option_template_packet
            diff = int(tcpdump_stop_time) - int(option_template_last_timestamp)
            option_flow_seq_check = None
            if diff > int(option_refresh_rate):
                last_option_temp_tstamp_status = False
            elif diff <= int(option_refresh_rate):
                last_option_temp_tstamp_status = True
        elif option_temp_count == 0:
            captured_duration = int(tcpdump_stop_time) - int(tcpdump_start_time)
            if captured_duration > int(option_refresh_rate):
                option_flow_seq_check = False
                options_tstamp_status = False
                last_option_temp_tstamp_status = False
                first_option_temp_tstamp_status = False
            else:
                self.log("INFO", "No Option Template capture found . "\
                "Please Run the TCPDUMP "\
                "for longer duration to capture atleast 2 packets , "\
                "run it for more than twice of option refresh rate")
                option_flow_seq_check = None
                options_tstamp_status = None
                last_option_temp_tstamp_status = None
                first_option_temp_tstamp_status = None

        if option_data_count > 1:
            # getting details related last captured option_template_packet
            diff = int(tcpdump_stop_time) - int(option_data_last_timestamp)
            if diff > int(option_refresh_rate):
                last_option_data_tstamp_status = False
            elif diff <= int(option_refresh_rate):
                last_option_data_tstamp_status = True
        elif option_data_count == 1:
            # getting details related last captured option_template_packet
            option_flow_seq_check = None
            diff = int(tcpdump_stop_time) - int(option_data_last_timestamp)
            if diff > int(option_refresh_rate):
                last_option_data_tstamp_status = False
            elif diff <= int(option_refresh_rate):
                last_option_data_tstamp_status = True
        elif option_data_count == 0:
            captured_duration = int(tcpdump_stop_time) - int(tcpdump_start_time)
            if captured_duration > int(option_refresh_rate):
                option_flow_seq_check = False
                options_tstamp_status = False
                last_option_data_tstamp_status = False
                first_option_data_tstamp_status = False
            else:
                self.log("INFO", "No Option Data capture found . "\
                "Please Run the TCPDUMP "\
                "for longer duration to capture atleast 2 packets , "\
                "run it for more than twice of option refresh rate")
                option_flow_seq_check = None
                options_tstamp_status = None
                last_option_data_tstamp_status = None
                first_option_data_tstamp_status = None

        if data_temp_count > 1:
            # getting details related last captured option_template_packet
            diff = int(tcpdump_stop_time) - int(data_template_last_timestamp)
            if diff > int(template_refresh_rate):
                last_data_temp_tstamp_status = False
            elif diff <= int(template_refresh_rate):
                last_data_temp_tstamp_status = True
        elif data_temp_count == 1:
            # getting details related last captured option_template_packet
            diff = int(tcpdump_stop_time) - int(data_template_last_timestamp)
            data_flow_seq_check = None
            if diff > int(template_refresh_rate):
                last_data_temp_tstamp_status = False
            elif diff <= int(template_refresh_rate):
                last_data_temp_tstamp_status = True
        elif data_temp_count == 0:
            captured_duration = int(tcpdump_stop_time) - int(tcpdump_start_time)
            if captured_duration > int(template_refresh_rate):
                data_flow_seq_check = False
                data_temp_tstamp_status = False
                last_data_temp_tstamp_status = False
                first_data_temp_tstamp_status = False
            else:
                data_flow_seq_check = None
                data_temp_tstamp_status = None
                last_data_temp_tstamp_status = None
                first_data_temp_tstamp_status = None

        status_check = {}
        status_check['option_flow_seq_check'] = option_flow_seq_check
        status_check['data_flow_seq_check'] = data_flow_seq_check
        status_check['Data_template_timestamp_verify_status'] = \
            data_temp_tstamp_status
        status_check['Options_timestamp_verify_status'] = options_tstamp_status
        status_check['option_temp_count'] = option_temp_count
        status_check['option_data_count'] = option_data_count
        status_check['data_temp_count'] = data_temp_count

        status_check['first_data_template_received_timestamp_status'] = \
            first_data_temp_tstamp_status
        status_check['last_data_template_received_timestamp_status'] = \
            last_data_temp_tstamp_status
        status_check['data_template_first_timestamp'] = data_template_first_timestamp
        status_check['data_template_last_timestamp'] = data_template_last_timestamp

        status_check['first_option_template_received_timestamp_status'] = \
            first_option_temp_tstamp_status
        status_check['last_option_template_received_timestamp_status'] = \
            last_option_temp_tstamp_status
        status_check['option_template_first_timestamp'] = option_template_first_timestamp
        status_check['option_template_last_timestamp'] = option_template_last_timestamp

        status_check['first_option_data_received_timestamp_status'] = \
            first_option_data_tstamp_status
        status_check['last_option_data_received_timestamp_status'] = \
            last_option_data_tstamp_status
        status_check['option_data_first_timestamp'] = option_data_first_timestamp
        status_check['option_data_last_timestamp'] = option_data_last_timestamp
        status_check['Data_template_timestamp_final_validation_status'] = \
            "verification pending"
        status_check['Options_timestamp_final_validation_status'] = \
            "verification pending"
        self.log("INFO", "%s"%status_check)
        return status_check

    def get_export_time_details_for_templates(self):
        """
        This method returns the dictionary containing the details for keys:-

            - data_template_last_timestamp
            - option_template_last_timestamp
            - data_template_first_timestamp
            - option_template_first_timestamp

        :return: dictionary containing relevant details related to initial and last timestam
                 of Data and option template.

        :rtype: dict

        """
        if self.platform == 'MX' and self.jflow_type == 'INLINE':
            details = {}
            details['data_template_last_timestamp'] = self.data_template_last_timestamp
            details['option_template_last_timestamp'] = self.option_template_last_timestamp
            details['data_template_first_timestamp'] = self.data_template_first_timestamp
            details['option_template_first_timestamp'] = self.option_template_first_timestamp
            return details

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
        print("LABEL RELATED INFO \n",label_related_info)
        for count, ppath in enumerate(sorted(label_related_info)):
            if len(router_details) == 1 and sampling_type == "egress":
                label_related_info[ppath]['jflow_labels_stack'] =\
                copy.deepcopy(label_related_info[ppath]['label_stack'])
            ### Newly added ##
            elif len(label_related_info) > len(self.jflow_labels_stack) and\
            len(self.jflow_labels_stack) == 1:
                label_related_info[ppath]['jflow_labels_stack'] =\
                self.jflow_labels_stack[0]
            ##################
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
        self.vpn_label = vpn_label
        return self.vpn_label

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
        This method will perform the dscp verification

        :return: True if verification succeed else False

        :rtype: bool


        Example::

            python:
                obj.init( PASS ALL MANATORY PARAMETERS MENTIONED IN init)
                status = obj.verify_dscp_value_at_collector()
            Robot:
                ${status}=    Jf.Verify Dscp Value At Collector\
                                 expected_dscp_value=0
                Should Be True     ${status}
        """
        result = None
        expected_dscp_value = kwg.get("expected_dscp_value", 0)
        ifile = self.tshark_output
        #cfl = re.findall(r'(Frame \d+: \d+ bytes on wire.*?Explicit Congestion Notification:)', ifile, re.DOTALL)
        cfl = re.findall(r'(Frame \d+: \d+ bytes on wire.*?User Datagram Protocol, Src Port)', ifile, re.DOTALL)
        for pkt in cfl:
            dscp_match = re.search(r'Differentiated Services Codepoint: .* [(](\d+)[)]', pkt)
            dscp_match_hex = re.search(r'Differentiated Services Codepoint: .* [(]0x(..)[)]', pkt)
            dscp_match_hex2 = re.search(r'Differentiated Services Codepoint: .* [(]0x(........)[)]', pkt)
            dscp_match_hex3 = re.search(r'Differentiated Services Field: .* [(]0x(........)[)]', pkt)
            if dscp_match:
                actual_dscp_value = dscp_match.group(1)
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

    def get_option_data_verification_status(self):
        """ returns option_data_verification_status """
        return self.option_data_verify_status

    def get_data_record_verification_status(self):
        """ return data_record_verification_status """
        return self.data_record_status

class instances(object):
    """ Class to create instances of
        of class "jflow_verification"
        which will later used for
        multi-thread verifications
    """

    def __init__(self):
        """ constructor initialization """
        self.objj = None

    def create_instance(self):
        """ method to create instance of
            of class "jflow_verification"
        """
        self.objj = jflow_verification()
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
        self.verify_the_data_records = False
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

        if "verify_option_data" in kwargs:
            self.verify_the_option_data = True
            self.dict_to_verify_option_data = kwargs['verify_option_data']

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

        if self.verify_the_option_data is True:
            self.obj.verify_option_data_record(**self.dict_to_verify_option_data)

        if self.verify_the_dsp_value_at_collector is True:
            self.obj.verify_dscp_value_at_collector(**self.expected_dscp_val)

        if self.verify_the_data_records is True:
            self.obj.verify_data_record(**self.dict_to_verify_data_records)
