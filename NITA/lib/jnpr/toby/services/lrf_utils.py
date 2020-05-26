# pylint: disable=undefined-variable
# p-ylint: disable=invalid-name
"""
Description : Common Keywords to operate commands on JLRF Tool
Company : Juniper Networks
"""
__author__ = ['Mohankumar Nagarajan']
__contact__ = 'mohankumarn@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re


#def initiate_lrf(lrf_collector, **kwargs):
def initiate_lrf(lrf_collector, interface, server_ip, port, lrf_binary):
    """
    Start LRF tool based on arguments passed
    :param handle $lrf_collector
    BSD machine handle when LRF collector tool runs

    :param string interface
    Interface name on which LRF collector tool wil be running

    :param string server_ip
    Interface server_ip on which LRF collector tool wil be running

    :param string lrf_binary
    Name of the lrf binary

    :param string port
    Port number on which LRF collector tool wil be running
    """

#    interface = kwargs.get('intf', None)
#    server_ip = kwargs.get('server_ip', None)
#    lrf_binary = kwargs.get('lrf_binary', None)
#    port = kwargs.get('port', None)
    response = lrf_collector.shell(command='ifconfig %s -alias' %(interface)).response()
    t.log('info', response)
    response = lrf_collector.shell(command='/sbin/ifconfig %s down' %(interface)).response()
    t.log('info', response)
    response = lrf_collector.shell(command='/sbin/ifconfig %s %s up'
                                   %(interface, server_ip)).response()
    t.log('info', response)
    response = lrf_collector.shell(command='/sbin/ifconfig %s' %(interface)).response()
    t.log('info', response)
    response = lrf_collector.shell(command='ls /volume/systest/Mobility/JTDF/%s'
                                   %(lrf_binary)).response()
    t.log('info', response)
    response = lrf_collector.shell(command='/volume/systest/Mobility/JTDF/%s' %(lrf_binary),
                                   pattern='JSIM>').response()
    t.log('info', response)
    response = lrf_collector.shell(command="edit jlrf", pattern='JLRF#').response()
    t.log('info', response)
    response = lrf_collector.shell(command='set server-ip-addr %s' %(server_ip),
                                   pattern='JLRF#').response()
    t.log('info', response)
    response = lrf_collector.shell(command='set io-interface %s' %(interface),
                                   pattern='JLRF#').response()
    t.log('info', response)
    response = lrf_collector.shell(command='set server-port %s' %(port),
                                   pattern='JLRF#').response()
    t.log('info', response)
    return True

#def lrf_path_profile_config(lrf_collector, **kwargs):
def lrf_path_profile_config(lrf_collector, server_ip, client_ip, path_protocol):
    """
    Method to configure LRF Path_Profile

    :param handle $lrf_collector
        BSD machine handle when LRF collector tool runs

    :param string server_ip
        Interface server_ip on which LRF collector tool wil be running

    :param string client_ip
        Interface client_ip on which LRF stats collection happens(in this case DUT)

    :param string path_protocol
    """
#    server_ip = kwargs.get('server_ip', None)
#    client_ip = kwargs.get('client_ip', None)
#    path_protocol = kwargs.get('path_protocol', None)
    response = lrf_collector.shell(command="edit path-profile lrf-collector",
                                   pattern="JLRF:path-profile-lrf-collector#").response()
    t.log('info', response)
    response = lrf_collector.shell(command='set server-ip-addr %s' %(server_ip),
                                   pattern='JLRF:path-profile-lrf-collector#').response()
    t.log('info', response)
    response = lrf_collector.shell(command='set client-ip-addr %s' %(client_ip),
                                   pattern='JLRF:path-profile-lrf-collector#').response()
    t.log('info', response)
    response = lrf_collector.shell(command='set protocol %s' %(path_protocol),
                                   pattern='JLRF:path-profile-lrf-collector#').response()
    t.log('info', response)
    response = lrf_collector.shell(command="exit", pattern="JLRF#").response()
    t.log('info', response)
    return True

#def create_control_template(lrf_collector, control_template_dict, **kwargs):
def create_control_template(lrf_collector, control_template_dict, template_name):
    """
    Method to create LRF control template

    :param handle $lrf_collector
        BSD machine handle when LRF collector tool runs

    :param string kwargs[template_name]
        Name of the control template

    :param dictionary control_template_dict
        dictionary having control template parameters

    """

#    template_name = kwargs.get('template_name', None)
    response = lrf_collector.shell(command='edit lrf template %s' %(template_name),
                                   pattern='#').response()

    t.log('info', response)

    for key in control_template_dict:
        response = lrf_collector.shell(command='set template-type %s' %(key),
                                       pattern='#').response()
        t.log('info', response)
        response = lrf_collector.shell(command=
                                       'set template-type %s validate-data-template %s'
                                       %(key, control_template_dict[key]),
                                       pattern='#').response()
        t.log('info', response)

    response = lrf_collector.shell(command="exit", pattern="JLRF#").response()
    t.log('info', response)
    return True

#def create_data_template(lrf_collector, data_template_dict, **kwargs):
def create_data_template(lrf_collector, data_template_dict, template_name, template_type):

    """
    Method to create LRF data templates

    :param handle $lrf_collector
        BSD machine handle when LRF collector tool runs

    :param string kwargs[template_name]
        Name of the data template

    :param dictionary data_template_dict
        dictionary having data template parameters
    """

#    template_name = kwargs.get('template_name', None)
#    template_type = kwargs.get('template_type', None)
    response = lrf_collector.shell(command='edit data-template %s %s'
                                   %(template_type, template_name),
                                   pattern='#').response()
    t.log('info', response)

    for key in data_template_dict:
        response = lrf_collector.shell(command='set %s %s'
                                       %(key, data_template_dict[key]),
                                       pattern='#').response()
        t.log('info', response)

    response = lrf_collector.shell(command="exit", pattern="JLRF#").response()
    t.log('info', response)
    return True

#def delete_control_template(lrf_collector, **kwargs):
def delete_control_template(lrf_collector, template_name):

    """
    Method to delete control templates

    :param handle $lrf_collector
        BSD machine handle when LRF collector tool runs

    :param string kwargs[template_name]
        Name of the control template to be deleted
    """
#    template_name = kwargs.get('template_name', None)
    response = lrf_collector.shell(command='delete template %s'
                                   %(template_name), pattern="#").response()
    t.log('info', response)
    return True

#def delete_control_sub_template(lrf_collector, **kwargs):
def delete_control_sub_template(lrf_collector, template_name, template_type):

    """
    Method to delete control sub templates

    :param handle $lrf_collector
        BSD machine handle when LRF collector tool runs

    :param string kwargs[template_name]
        Name of the control template to be deleted
    """

#    template_name = kwargs.get('template_name', None)
#    template_type = kwargs.get('template_type', None)
    response = lrf_collector.shell(command='edit lrf template %s' %(template_name),
                                   pattern='#').response()
    t.log('info', response)
    response = lrf_collector.shell(command='delete template-type %s' %(template_type),
                                   pattern='#').response()
    t.log('info', response)
    response = lrf_collector.shell(command="exit", pattern="JLRF#").response()
    t.log('info', response)
    return True

#def lrf_exec_command(lrf_collector, **kwargs):
def lrf_exec_command(lrf_collector, command):

    """
    Method to execute a command in lrf tool

    :param handle $lrf_collector
        BSD machine handle when LRF collector tool runs

    :param string kwargs[command]
        Name of the lrf command to be executed

    return: string
        response from the LRF command that was executed
    """
#    command = kwargs.get('command', None)
    response = lrf_collector.shell(command='%s' %(command),
                                   pattern="JLRF#").response()
    t.log('info', response)
    return response

def stop_lrf(lrf_collector):

    """
    Method to stop lrf

    :param handle $lrf_collector
        BSD machine handle when LRF collector tool runs
    """

    response = lrf_collector.shell(command="exit", pattern="JSIM>").response()
    t.log('info', response)
    response = lrf_collector.shell(command="quit").response()
    t.log('info', response)
    return True

def data_record_validation(input_str, trigger):

    """
    Method to validate data record

    :param string input_str
    response from LRF_Exec command which is used  to validate data records

    :param string trigger
    TBD

    return boolean:
    True if data record validation passed else fail
    """


    template_type_dict = {"1":"IPv4", "2":"IPv4 Ext", "3":"IPv6", "4":"IPv6 Ext",
                          "5":"Flow ID", "6":"IPFlow", "7":"IPFlow TS", "8":"IPFlow Ext",
                          "9":"Device Data", "10":"L7 App", "11":"HTTP",
                          "12":"L7-stats", "13":"Subscriber Data", "14":"Mobile-subscriber",
                          "15":"Wireline-subscriber", "16":"IFL Subscriber",
                          "17":"Transport", "18":"Ipflow TCP ts",
                          "19":"Status code distribution", "20":"Video",
                          "21":"DNS", "22":"PCC RULE NAME", "23":"Ipflow TCP"}
    t.log('info', input_str)
    ret_val = True
    lines = input_str.splitlines()
    pattern1 = "Template type:([0-9]+)"
    pattern2 = "Validation Failed:([1-9]+)"
    uplink_pattern = "Field Type:Uplink Octects, Field Value:([0-9])+"
    downlink_pattern = "Field Type:Downlink Octects, Field Value:([0-9])+"
    record_pattern = "Field Type:Record Reason, Field Value:([0-9])+"
    failed_pattern = "Failed ([1-9])+"

    for line in lines:
        match = re.search(pattern1, line)

        if match:
            template_type = match.group(1)
            length1 = len(template_type)
        else:
            length1 = 0

        match = re.search(pattern2, line)

        if match:
            failed_records = match.group(1)
            length2 = len(failed_records)
        else:
            length2 = 0

        match = re.search(failed_pattern, line)

        if match:
            failed = match.group(1)
            failed_length = len(failed)
        else:
            failed_length = 0


        match = re.search(uplink_pattern, line)

        if match:
            uplink = match.group(1)

        match = re.search(downlink_pattern, line)

        if match:
            downlink = match.group(1)

        match = re.search(record_pattern, line)

        if match:
            record = match.group(0)
            length_rec = len(record)
        else:
            length_rec = 0

        if length_rec > 0:
            t.log('info', record)

        if length2 > 0:
            t.log('error', 'Template Type Name: %s' %(template_type_dict[template_type[0]]))
            t.log('error', 'and Number of Fail Records: %s' %(failed_records[0]))

        if failed_length > 0:
            t.log('error', "Data Templates Failed")

    for line in lines:
        match = re.search(pattern1, line)

        if match:
            template_type = match.group(1)
            length1 = len(template_type)
        else:
            length1 = 0

        match = re.search(pattern2, line)

        if match:
            failed_records = match.group(1)
            length2 = len(failed_records)
        else:
            length2 = 0

        if length1 > 0 and length2 > 0:
            return False

    return ret_val
