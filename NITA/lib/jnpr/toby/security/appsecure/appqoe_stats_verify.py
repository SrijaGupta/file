from jnpr.toby.hldcl.device import Device
from jnpr.toby.init.init import init
import re
import time
import jxmlease
from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.utils.linux.syslog_utils import check_syslog
from jnpr.toby.utils.iputils import normalize_ipv6

__author__ = ['Sharanagoud B D']
__contact__ = ''
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2018'

"""
Keywords written for
1: get_appqoe_sla_stats
2: verify_appqoe_sla_stats
3: get_appqoe_active_probe_stats
4: verify_appqoe_active_probe_stats
5: get_appqoe_passive_probe_app_detail
6: verify_appqoe_passive_probe_app_detail
7: get_appqoe_application_status
8: verify_appqoe_application_status
9: get_appid_counter
10: verify_appid_counter
11: check_srx_appfw_hit_count
"""



"""
Advance policy based routing(APBR) SLA Stas
"""

def get_appqoe_sla_stats(device=None, node="local"):
    """
    To get the AppQoE SLA statistics as dictionary
    Example:
        get_appqoe_sla_stats(device=device)

    ROBOT Example:
        Get Appqoe Sla Stats   device=${device}

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns the dictionary for SLA statistics
    :rtype: dict
    Example returned dictionary:

    {
    'apbr-sla-statistics-passive-session-processed': '0',
    'apbr-sla-statistics-passive-probe-sessions': '0',
    'apbr-sla-statistics-passive-sessions-sampled': '0',
    'apbr-sla-statistics-passive-ongoing-sessions': '0',
    'apbr-sla-statistics-passive-ongoing-sessions': '0',
    'apbr-sla-statistics-active-probe-paths': '0',
    'apbr-sla-statistics-active-probe-sessions': '0',
    'apbr-sla-statistics-active-probe-sent': '0',
    'apbr-sla-statistics-active-path-down': '0',
    'apbr-sla-statistics-active-sla-violation': '0'
    }

    """
    if device is None:
        raise ValueError("Device handle is a mandatory argument")

    cmd = 'show security advance-policy-based-routing sla statistics'
    status = device.execute_as_rpc_command(command=cmd, node=node)
    stats = status['apbr-sla-statistics']
    return stats

def verify_appqoe_sla_stats(device=None, counter_values=None, node="local"):
    """
    To verify Appqoe sla statistics. (show security advance-policy-based-routing sla statistics)
    Example:
        verify_appqoe_sla_stats(device=dt, counter_values={'apbr-sla-statistics-passive-probe-sessions':1,
        'apbr-sla-statistics-passive-sessions-sampled':1}, node="node0")

    ROBOT Example:
        Verify Appqoe Sla Stats   device=${dt}    counter_values=${{{'apbr-sla-statistics-passive-probe-sessions':1,
        'apbr-sla-statistics-passive-sessions-sampled':1}}}    node=node0


    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param dict counter_values:
        **REQUIRED** Dictionary of counter names (key) and their expected values (value of the key).
        `Supported values of counter names (key)``: apbr-sla-statistics-passive-session-processed
                                                    apbr-sla-statistics-passive-probe-sessions
                                                    apbr-sla-statistics-passive-sessions-sampled
                                                    apbr-sla-statistics-passive-ongoing-sessions
                                                    apbr-sla-statistics-passive-ongoing-sessions
                                                    apbr-sla-statistics-active-probe-paths
                                                    apbr-sla-statistics-active-probe-sessions
                                                    apbr-sla-statistics-active-probe-sent
                                                    apbr-sla-statistics-active-path-down
                                                    apbr-sla-statistics-active-sla-violation
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: True/False , based on verification status
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")
    if counter_values is None:
        device.log(level="ERROR", message="counter_values is None, it is mandatory argument")
        raise ValueError("counter_values is None, it is mandatory argument")

    counters_in_device = get_appqoe_sla_stats(device=device, node=node)
    flag = True
    for counter in counter_values.keys():
        if counter in counters_in_device:
            if counter_values[counter] == (counters_in_device[counter]):
                device.log(level="INFO", message="%s has value %s , match successful" % (
                    counter, counters_in_device[counter]))
            else:
                flag = False
                device.log(level="ERROR", message="%s has value %s , match is not successful" % (
                    counter, counters_in_device[counter]))
        else:
            flag = False
            device.log(level="ERROR", message=counter + " counter not found in apbr sla stats")

    if flag is False:
        device.log(level="ERROR", message="APBR sla statistics validation failed")
        raise Exception("APBR sla statistics validation failed")

    device.log(level="INFO", message="APBR sla statistics validation passed")
    return flag

"""
Advance policy based routing(APBR) SLA Active Probe stats
"""

def get_appqoe_active_probe_stats(device=None, probe_name=None, node="local"):
    """
    To get the AppQoE SLA active probe statistics as dictionary
    Example:
        get_appqoe_active_probe_stats(device=device, probe_name=None)

    ROBOT Example:
        Get Appqoe Active Probe Stats   device=${device}   probe_name=probe1

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns the dictionary for SLA statistics
    :rtype: dict
    Example returned dictionary:

    {'apbr-active-statistics-info': [{'apbr-active-statistics-details-dest-ip': '42.1.1.1',
                                  'apbr-active-statistics-details-egress-jit': '2',
                                  'apbr-active-statistics-details-ingress-jit': '1',
                                  'apbr-active-statistics-details-pkt-loss': '0',
                                  'apbr-active-statistics-details-rtt': '825',
                                  'apbr-active-statistics-details-src-ip': '42.1.1.2',
                                  'apbr-active-statistics-details-two-way': '0'},
                                 {'apbr-active-statistics-details-dest-ip': '41.1.1.1',
                                  'apbr-active-statistics-details-egress-jit': '1',
                                  'apbr-active-statistics-details-ingress-jit': '2',
                                  'apbr-active-statistics-details-pkt-loss': '0',
                                  'apbr-active-statistics-details-rtt': '830',
                                  'apbr-active-statistics-details-src-ip': '41.1.1.2',
                                  'apbr-active-statistics-details-two-way': '0'},
                                 {'apbr-active-statistics-details-dest-ip': '40.1.1.1',
                                  'apbr-active-statistics-details-egress-jit': '1',
                                  'apbr-active-statistics-details-ingress-jit': '1',
                                  'apbr-active-statistics-details-pkt-loss': '0',
                                  'apbr-active-statistics-details-rtt': '794',
                                  'apbr-active-statistics-details-src-ip': '40.1.1.2',
                                  'apbr-active-statistics-details-two-way': '0'}]}

    """
    if device is None or probe_name is None:
        raise ValueError("Device handle and probe_name  is a mandatory argument")

    cmd = 'show security advance-policy-based-routing sla active-probe-statistics active-probe-params-name ' + probe_name
    status = device.execute_as_rpc_command(command=cmd, node=node)
    stats = status['apbr-active-statistics']
    return stats

def verify_appqoe_active_probe_stats(device=None, probe_name=None, source_address=None, dest_address=None, active_probe_stats_dict=None, node="local",
                                     target_pkt_loss=None, target_rtt=None, target_two_way_jitter=None, target_ingress_jitter=None,
                                     target_egress_jitter=None):

    """
    To verify AppQoE SLA active probe statistics.
    Example:
        verify_appqoe_active_probe_stats(dev_obj, probe_name='probe1', source_address='41.1.1.2', dest_address='41.1.1.1',
        target_pkt_loss= [10, 'greatereq'], target_rtt=30000, target_two_way_jitter = 10)
    ROBOT Example:
        Verify Appqoe Active Probe Stats     device=${spoke}    probe_name=probe1    source_address=${gre-spoke-ip1} \
                                         dest_address=${gre-hub-ip1}   target_pkt_loss=10 \
                                         target_rtt=200000    target_egress_jitter=10000

    :param Device device:
        **REQUIRED** Device Handle of the dut

    :param dict active_probe_stats_dict:
        *OPTIONAL* Active Probe Statistics as dictionary on which verification takes place.
        get_appqoe_active_probe_stats() returns this.
    :return: Boolean (True or False)
    :rtype: bool
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if probe_name is None:
        device.log(level="INFO", message="'probe_name' is a mandatory argument")
        raise ValueError("'probe_name' is a mandatory argument")

    if source_address is None:
        device.log(level="INFO", message="'source_address' is a mandatory argument")
        raise ValueError("'source_address' is a mandatory argument")

    if dest_address is None:
        device.log(level="INFO", message="'dest_address' is a mandatory argument")
        raise ValueError("'dest_address' is a mandatory argument")

    if active_probe_stats_dict is None:
        active_probe_stats_dict = get_appqoe_active_probe_stats(device=device, probe_name=probe_name, node=node)

    device.log(level="INFO", message="Verifying Active Probe Statistics")
    list_of_dicts = []
    active_path_found = 0
    for entry in active_probe_stats_dict['apbr-active-statistics-info']:
        if isinstance(entry, dict):
            if entry["apbr-active-statistics-details-src-ip"] == source_address and \
                            entry["apbr-active-statistics-details-dest-ip"] == dest_address:
                active_path_found = 1
                list_of_dicts.append(entry)

    if active_path_found == 1:
        device.log(level="INFO", message="source and destination address are found in active probe statistics")
    else:
        device.log(level="ERROR", message="source and destination address are not found in active probe statistics")
        raise Exception("source_address is not found in active probe statistics")

    flag = 1
    for x in list_of_dicts:
        pkt_loss_value = ''
        pkt_loss_option = ''
        if target_pkt_loss is not None:
            if isinstance(target_pkt_loss, list):
                pkt_loss_value = target_pkt_loss[0]
                pkt_loss_option = target_pkt_loss[1]
            else:
                pkt_loss_value = target_pkt_loss

            if pkt_loss_option == 'greatereq':
                if int(x['apbr-active-statistics-details-pkt-loss']) >= int(pkt_loss_value):
                    device.log(level="INFO", message=" *** Entered Greatereq *** Measured packet loss\
                    %s is greater than target packet loss %s" %(x['apbr-active-statistics-details-pkt-loss'], pkt_loss_value))
                else:
                    device.log(level="INFO", message=" *** Entered Greatereq *** Measured packet loss \
                    %s is less than target packet loss %s" %(x['apbr-active-statistics-details-pkt-loss'], pkt_loss_value))
                    flag = 0
            else:
                if int(x['apbr-active-statistics-details-pkt-loss']) <= int(pkt_loss_value):
                    device.log(level="INFO", message="Measured packet loss %s is less than target packet loss %s"\
                                           %(x['apbr-active-statistics-details-pkt-loss'], pkt_loss_value))
                else:
                    device.log(level="INFO", message="Measured packet loss %s is greater than target packet loss %s"\
                                           %(x['apbr-active-statistics-details-pkt-loss'], pkt_loss_value))
                    flag = 0

        rtt_value = ''
        rtt_option = ''
        if target_rtt is not None:
            if isinstance(target_rtt, list):
                rtt_value = target_rtt[0]
                rtt_option = target_rtt[1]
            else:
                rtt_value = target_rtt

            if rtt_option == 'greatereq':
                if int(x['apbr-active-statistics-details-rtt']) >= int(rtt_value):
                    device.log(level="INFO",
                               message=" *** Entered Greatereq *** Measured rtt %s is greater than target rtt %s"\
                                       %(x['apbr-active-statistics-details-rtt'], rtt_value))
                else:
                    device.log(level="INFO",
                               message=" *** Entered Greatereq *** Measured rtt %s is less than target rtt %s"\
                                       %(x['apbr-active-statistics-details-rtt'], rtt_value))
                    flag = 0
            else:
                if int(x['apbr-active-statistics-details-rtt']) <= int(rtt_value):
                    device.log(level="INFO",
                               message="Measured rtt %s is less than target rtt %s" \
                                       %(x['apbr-active-statistics-details-rtt'], rtt_value))
                else:
                    device.log(level="INFO", message="Measured rtt %s is greater than target rtt %s"\
                                            %(x['apbr-active-statistics-details-rtt'], rtt_value))
                    flag = 0

        two_way_jitter_value = ''
        two_way_jitter_option = ''
        if target_two_way_jitter is not None:
            if isinstance(target_two_way_jitter, list):
                two_way_jitter_value = target_two_way_jitter[0]
                two_way_jitter_option = target_two_way_jitter[1]
            else:
                two_way_jitter_value = target_two_way_jitter

            if two_way_jitter_option == 'greatereq':
                if int(x['apbr-active-statistics-details-two-way']) >= int(two_way_jitter_value):
                    device.log(level="INFO", message=" *** Entered Greatereq *** Measured two way jitter %s \
                    is greater than target two way jitter %s" %(x['apbr-active-statistics-details-two-way'],
                                                                two_way_jitter_value))
                else:
                    device.log(level="INFO", message=" *** Entered Greatereq *** Measured two way jitter %s \
                    is less than target two way jitter %s" %(x['apbr-active-statistics-details-two-way'],
                                                             two_way_jitter_value))
                    flag = 0
            else:
                if int(x['apbr-active-statistics-details-two-way']) <= int(two_way_jitter_value):
                    device.log(level="INFO", message="Measured two way jitter %s is less than target two way\
                     jitter %s" %(x['apbr-active-statistics-details-two-way'], two_way_jitter_value))
                else:
                    device.log(level="INFO", message="Measured two way jitter %s is greater than target two way\
                     jitter %s" %(x['apbr-active-statistics-details-two-way'], two_way_jitter_value))
                    flag = 0

        ingress_jitter_value = ''
        ingress_jitter_option = ''
        if target_ingress_jitter is not None:
            if isinstance(target_ingress_jitter, list):
                ingress_jitter_value = target_ingress_jitter[0]
                ingress_jitter_option = target_ingress_jitter[1]
            else:
                ingress_jitter_value = target_ingress_jitter

            if ingress_jitter_option == 'greatereq':
                if int(x['apbr-active-statistics-details-ingress-jit']) >= int(ingress_jitter_value):
                    device.log(level="INFO", message=" *** Entered Greatereq *** Measured ingress jitter %s\
                     is greater than target ingress jitter %s" %(x['apbr-active-statistics-details-ingress-jit'],
                                                                 ingress_jitter_value))
                else:
                    device.log(level="INFO", message=" *** Entered Greatereq *** Measured ingress jitter %s \
                    is less than target ingress jitter %s" %(x['apbr-active-statistics-details-ingress-jit'],
                                                             ingress_jitter_value))
                    flag = 0
            else:
                if int(x['apbr-active-statistics-details-ingress-jit']) <= int(ingress_jitter_value):
                    device.log(level="INFO", message="Measured ingress jitter %s is less than target ingress \
                     jitter %s" %(x['apbr-active-statistics-details-ingress-jit'], ingress_jitter_value))
                else:
                    device.log(level="INFO", message="Measured ingress jitter %s is greater than target ingress \
                    jitter %s" %(x['apbr-active-statistics-details-ingress-jit'], ingress_jitter_value))
                    flag = 0

        egress_jitter_value = ''
        egress_jitter_option = ''
        if target_egress_jitter is not None:
            if isinstance(target_egress_jitter, list):
                egress_jitter_value = target_egress_jitter[0]
                egress_jitter_option = target_egress_jitter[1]
            else:
                egress_jitter_value = target_egress_jitter

            if egress_jitter_option == 'greatereq':
                if int(x['apbr-active-statistics-details-egress-jit']) >= int(egress_jitter_value):
                    device.log(level="INFO", message=" *** Entered Greatereq *** Measured egress jitter %s \
                    is greater than target egress jitter %s" %(x['apbr-active-statistics-details-egress-jit'],
                                                               egress_jitter_value))
                else:
                    device.log(level="INFO", message="*** Entered Greatereq *** Measured egress jitter %s \
                     is less than target egress jitter %s" %(x['apbr-active-statistics-details-egress-jit'],
                                                             egress_jitter_value))
                    flag = 0
            else:
                if int(x['apbr-active-statistics-details-egress-jit']) <= int(egress_jitter_value):
                    device.log(level="INFO", message="Measured egress jitter %s is less than target egress \
                    jitter %s" %(x['apbr-active-statistics-details-egress-jit'], egress_jitter_value))
                else:
                    device.log(level="INFO", message="Measured egress jitter %s is greater than target egress\
                     jitter %s" %(x['apbr-active-statistics-details-egress-jit'], egress_jitter_value))
                    flag = 0

    if flag == 1:
        device.log(level="INFO", message="AppQoE active probe statistics are matched successfully")
    else:
        device.log(level="ERROR", message="AppQoE active probe statistics are not matching")
        raise Exception("AppQoE active probe statistics are not matching - Expected" + \
                        " less than or greear than or equal of passed target values")

    return True

def get_appqoe_passive_probe_app_detail(device=None, profile_name=None, application=None, dscp=None, dest_group_name=None,
                                        node="local", next_hop_id=None, server_ip=None):
    """
    To get the AppQoE SLA Application Details and SLA Metrics as dictionary
    Example:
        get_appqoe_passive_probe_app_detail(dev_obj, profile_name='apbr1', application='HTTP', dscp='63', dest_group_name='site1')

    ROBOT Example:
        Get Appqoe Passive Probe App Detail    device=${spoke}    profile_name=apbr1    application=my-http    dscp=63   dest_group_name=site1

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns the dictionary for Application Details
    :rtype: dict
    Example returned dictionary:

        </apbr-prof-app>
        {'apbr-prof-app-appid': '67',
         'apbr-prof-app-dscp': '63',
         'apbr-prof-app-appname': 'HTTP',
         'apbr-prof-app-appstate': 'SLA MET',
         'apbr-prof-app-egr-jit': '0',
         'apbr-prof-app-idlestate': '0',
         'apbr-prof-app-ing-jit': '0',
         'apbr-prof-app-ip': '40.1.1.1',
         'apbr-prof-app-pkt-loss': '0',
         'apbr-prof-app-port': '35011',
         'apbr-prof-app-profname': 'apbr1',
         'apbr-prof-app-riname': 'appqoe',
         'apbr-prof-app-rtt': '0',
         'apbr-prof-app-rulename': 'rule-app1',
         'apbr-prof-app-slaname': 'sla1',
         'apbr-prof-app-two-way': '0'}
    """
    if device is None or profile_name is None  or dest_group_name is None:
        raise ValueError("Device handle, profile_name and dest_group_name is a mandatory argument")

    version = device.get_version()
    if float(version[:4]) >= 20.2:
        if next_hop_id is None:
            next_hop_id_dict = get_next_hop_id(device=device, profile_name=profile_name, application=application, dscp=dscp, node=node)
            if 'apbr-prof-app-brief' in next_hop_id_dict.keys():
                next_hop_id = next_hop_id_dict['apbr-prof-app-brief']['apbr-prof-app-brief-info']['apbr-prof-app-brief-nh']
            else:
                raise ValueError('Appdb is not present for the application')
    if application is not None and dscp is not None:
        if float(version[:4]) >= 20.2:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
                  " " + application + " " + 'dscp' + " " + dscp + " " + 'next-hop' + " " + next_hop_id
        else:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
                   " " + application + " " + 'dscp' + " " + dscp + " " + 'destination-group-name' + " " + dest_group_name + " "
    elif application is not None:
        if float(version[:4]) >= 20.2:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
                  " " + application + " " + 'next-hop' + " " + next_hop_id
        else:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
                   " " + application + " " + 'destination-group-name' + " " + dest_group_name + " "

    elif dscp is not None:
        if float(version[:4]) >= 20.2:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'dscp' + \
                  " " + dscp + " " + 'next-hop' + " " + next_hop_id
        else:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'dscp' + \
                   " " + dscp + " " + 'destination-group-name' + " " + dest_group_name + " "
    else:
        raise ValueError("Either Application or DSCP is mandatory argument")

    status = device.execute_as_rpc_command(command=cmd, node=node)
    if status is None:
        device.log("No output found")
        raise Exception("Empty dictionary")
    stats = status['apbr-prof-app']
    return stats


def verify_appqoe_passive_probe_app_detail(device=None, profile_name=None, application=None, dscp=None, dest_group_name=None, app_details=None, 
                                           node="local", target_pkt_loss=None, target_rtt=None, target_two_way_jitter=None, target_ingress_jitter=None,
                                           target_egress_jitter=None, next_hop_id=None, server_ip=None, post_20_2_rel=None):
    """
    To verify AppQoE SLA Passive probe app details
    Example:
    verify_appqoe_passive_probe_app_detail(dev_obj, profile_name='apbr1', application='HTTP', dscp='63', dest_group_name='site1',
     app_details={'apbr-prof-app-appid': '67', 'apbr-prof-app-profname': 'apbr1', 'apbr-prof-app-riname': 'appqoe'}

    verify_appqoe_passive_probe_app_detail(dev_obj, profile_name='apbr1', application='HTTP', dscp='63',
    dest_group_name='site1', app_details={'apbr-prof-app-appid': '67', 'apbr-prof-app-profname': 'apbr1', 'apbr-prof-app-riname': 'appqoe'}, target_rtt=[30000,'greatereq'], target_pkt_loss=[10,'greatereq'], target_two_way_jitter= '10')

    ROBOT Example:
        Verify Appqoe Passive Probe App Detail    device=${spoke}    profile_name=apbr1
        ...  application=my-http    dscp=63     dest_group_name=site1  app_details=${app_details}

    :param Device device:
        **REQUIRED** Device Handle of the dut

    :param dict active_probe_stats_dict:
        *OPTIONAL* Active Probe Statistics as dictionary on which verification takes place.
        get_appqoe_active_probe_stats() returns this.
    :return: Boolean (True or False)
    :rtype: bool
    """
    if device is None or profile_name is None or dest_group_name is None:
        raise ValueError("Device handle, profile_name and dest_group_name is a mandatory argument")
    if application is None and dscp is None:
        raise ValueError("Either Application or DSCP is mandatory argument")
    if app_details is None:
        device.log(level="ERROR", message="app_details is None, it is mandatory argument")
        raise ValueError("app_details is None, it is mandatory argument")

    version = device.get_version()
    device.log(level="INFO", message="%s Device versiuon" % (version))
    app_details_in_device = get_appqoe_passive_probe_app_detail(device=device, profile_name=profile_name, application=application, dscp=dscp,
                                                                dest_group_name=dest_group_name, node=node, next_hop_id=next_hop_id, server_ip=server_ip)
    flag = 1

    # Below code is added to change the best path ip from hub to spoke for the existing scripts which is written for below 20.2 releases
    device.log(level="INFO", message="%s Device versiuon" % (version))
    if float(version[:4]) >= 20.2 and post_20_2_rel is None:
        resource_list = t.get_junos_resources()
        if ('spoke' in resource_list or 'node0' in resource_list) and 'hub' in resource_list:
            pass
        else:
            raise Exception('This method expects appqoe spoke name as spoke(SA)/node0(HA) and hub name as hub in params')
        for resource in resource_list:
            if resource in ['spoke', 'node0']:
                if app_details['apbr-prof-app-ip'] in [t['resources'][resource]['system']['primary']['uv-gre1-ipv4'], t['resources'][resource]['system']['primary']['uv-gre2-ipv4'], t['resources'][resource]['system']['primary']['uv-gre3-ipv4'], t['resources'][resource]['system']['primary'].get('uv-gre4-ipv4', '16.16.16.1')]:
                    pass
                elif t['resources']['hub']['system']['primary'].get('uv-gre1-ipv4', 'False') == app_details['apbr-prof-app-ip']:
                    app_details['apbr-prof-app-ip'] = t['resources'][resource]['system']['primary']['uv-gre1-ipv4']
                elif t['resources']['hub']['system']['primary'].get('uv-gre2-ipv4', 'False') == app_details['apbr-prof-app-ip']:
                    app_details['apbr-prof-app-ip'] = t['resources'][resource]['system']['primary']['uv-gre2-ipv4']
                elif t['resources']['hub']['system']['primary'].get('uv-gre3-ipv4', 'False') == app_details['apbr-prof-app-ip']:
                    app_details['apbr-prof-app-ip'] = t['resources'][resource]['system']['primary']['uv-gre3-ipv4']
                elif t['resources']['hub']['system']['primary'].get('uv-gre4-ipv4', 'False') == app_details['apbr-prof-app-ip']:
                    app_details['apbr-prof-app-ip'] = t['resources'][resource]['system']['primary']['uv-gre4-ipv4']
                else:
                    device.log(level="ERROR", message="Unable to get correct IP address. Hence raising a Exception. Please revisit yaml and appqoe_stats_verify.py file")
                    raise Exception("If you have more than three/four wan links then update method verify_appqoe_passive_probe_app_detail in appqoe_stats_verify.py file accordingly")
    # End of the code
    for counter in app_details.keys():
        if counter in app_details_in_device:
            if app_details[counter] == (app_details_in_device[counter]):
                device.log(level="INFO", message="%s has value %s , match successful" % (counter, app_details_in_device[counter]))
            else:
                flag = 0
                device.log(level="ERROR", message="%s has value %s , match is not successful" % (counter, app_details_in_device[counter]))
        else:
            flag = 0
            device.log(level="ERROR", message=counter + " counter not found in passive probe app details")
    pkt_loss_value = ''
    pkt_loss_option = ''
    if target_pkt_loss is not None:
        if isinstance(target_pkt_loss, list):
            pkt_loss_value = target_pkt_loss[0]
            pkt_loss_option = target_pkt_loss[1]
        else:
            pkt_loss_value = target_pkt_loss

        if pkt_loss_option == 'greatereq':
            if int(app_details_in_device['apbr-prof-app-pkt-loss']) >= int(pkt_loss_value):
                device.log(level="INFO", message="Measured packet loss %s is greater than target packet loss %s"\
                                         %(app_details_in_device['apbr-prof-app-pkt-loss'], pkt_loss_value))
            else:
                device.log(level="INFO", message="Measured packet loss %s is less than target packet loss %s"\
                                         %(app_details_in_device['apbr-prof-app-pkt-loss'], pkt_loss_value))
                flag = 0
        else:
            if int(app_details_in_device['apbr-prof-app-pkt-loss']) <= int(pkt_loss_value):
                device.log(level="INFO", message="Measured packet loss %s is less than target packet loss %s"\
                                         %(app_details_in_device['apbr-prof-app-pkt-loss'], pkt_loss_value))
            else:
                device.log(level="INFO", message="Measured packet loss %s is greater than target packet loss %s"\
                                         %(app_details_in_device['apbr-prof-app-pkt-loss'], pkt_loss_value))
                flag = 0

    rtt_value = ''
    rtt_option = ''
    if target_rtt is not None:
        if isinstance(target_rtt, list):
            rtt_value = target_rtt[0]
            rtt_option = target_rtt[1]
        else:
            rtt_value = target_rtt

        if rtt_option == 'greatereq':
            if int(app_details_in_device['apbr-prof-app-rtt']) >= int(rtt_value):
                device.log(level="INFO", message="Measured rtt %s is greater than target rtt %s"\
                                         %(app_details_in_device['apbr-prof-app-rtt'], rtt_value))
            else:
                device.log(level="INFO", message="Measured rtt %s is less than target rtt %s"\
                                         %(app_details_in_device['apbr-prof-app-rtt'], rtt_value))
                flag = 0
        else:
            if int(app_details_in_device['apbr-prof-app-rtt']) <= int(rtt_value):
                device.log(level="INFO", message="Measured rtt %s is less than target rtt %s"\
                                         %(app_details_in_device['apbr-prof-app-rtt'], rtt_value))
            else:
                device.log(level="INFO", message="Measured rtt %s is greater than target rtt %s"\
                                         %(app_details_in_device['apbr-prof-app-rtt'], rtt_value))
                flag = 0

    two_way_jitter_value = ''
    two_way_jitter_option = ''
    if target_two_way_jitter is not None:
        if isinstance(target_two_way_jitter, list):
            two_way_jitter_value = target_two_way_jitter[0]
            two_way_jitter_option = target_two_way_jitter[1]
        else:
            two_way_jitter_value = target_two_way_jitter

        if two_way_jitter_option == 'greatereq':
            if int(app_details_in_device['apbr-prof-app-two-way']) >= int(two_way_jitter_value):
                device.log(level="INFO", message="Measured two way jitter %s is greater than target two \
                way jitter %s" %(app_details_in_device['apbr-prof-app-two-way'], two_way_jitter_value))
            else:
                device.log(level="INFO", message="Measured two way jitter %s is less than target two way \
                jitter %s" %(app_details_in_device['apbr-prof-app-two-way'], two_way_jitter_value))
                flag = 0
        else:
            if int(app_details_in_device['apbr-prof-app-two-way']) <= int(two_way_jitter_value):
                device.log(level="INFO", message="Measured two way jitter %s is less than target two way\
                 jitter %s" %(app_details_in_device['apbr-prof-app-two-way'], two_way_jitter_value))
            else:
                device.log(level="INFO", message="Measured two way jitter %s is greater than target two \
                way jitter %s" %(app_details_in_device['apbr-prof-app-two-way'], two_way_jitter_value))
                flag = 0

    ingress_jitter_value = ''
    ingress_jitter_option = ''
    if target_ingress_jitter is not None:
        if isinstance(target_ingress_jitter, list):
            ingress_jitter_value = target_ingress_jitter[0]
            ingress_jitter_option = target_ingress_jitter[1]
        else:
            ingress_jitter_value = target_ingress_jitter

        if ingress_jitter_option == 'greatereq':
            if int(app_details_in_device['apbr-prof-app-ing-jit']) >= int(ingress_jitter_value):
                device.log(level="INFO", message="Measured ingress jitter %s is greater than target ingress\
                 jitter %s" %(app_details_in_device['apbr-prof-app-ing-jit'], ingress_jitter_value))
            else:
                device.log(level="INFO", message="Measured ingress jitter %s is less than target ingress \
                jitter %s" %(app_details_in_device['apbr-prof-app-ing-jit'], ingress_jitter_value))
                flag = 0
        else:
            if int(app_details_in_device['apbr-prof-app-ing-jit']) <= int(ingress_jitter_value):
                device.log(level="INFO", message="Measured ingress jitter %s is less than target ingress \
                jitter %s" %(app_details_in_device['apbr-prof-app-ing-jit'], ingress_jitter_value))
            else:
                device.log(level="INFO", message="Measured ingress jitter %s is greater than target ingress\
                 jitter %s" %(app_details_in_device['apbr-prof-app-ing-jit'], ingress_jitter_value))
                flag = 0

    egress_jitter_value = ''
    egress_jitter_option = ''
    if target_egress_jitter is not None:
        if isinstance(target_egress_jitter, list):
            egress_jitter_value = target_egress_jitter[0]
            egress_jitter_option = target_egress_jitter[1]
        else:
            egress_jitter_value = target_egress_jitter

        if egress_jitter_option == 'greatereq':
            if int(app_details_in_device['apbr-prof-app-egr-jit']) >= int(egress_jitter_value):
                device.log(level="INFO", message="Measured egress jitter %s is greater than target egress\
                 jitter %s" %(app_details_in_device['apbr-prof-app-egr-jit'], egress_jitter_value))
            else:
                device.log(level="INFO", message="Measured egress jitter %s is less than target egress\
                 jitter %s" %(app_details_in_device['apbr-prof-app-egr-jit'], egress_jitter_value))
                flag = 0
        else:
            if int(app_details_in_device['apbr-prof-app-egr-jit']) <= int(egress_jitter_value):
                device.log(level="INFO", message="Measured egress jitter %s is less than target egress\
                 jitter %s" %(app_details_in_device['apbr-prof-app-egr-jit'], egress_jitter_value))
            else:
                device.log(level="INFO", message="Measured egress jitter %s is greater than target\
                 egress jitter %s" %(app_details_in_device['apbr-prof-app-egr-jit'], egress_jitter_value))
                flag = 0

    if flag == 1:
        device.log(level="INFO", message="AppQoE passive probe application details are matched successfully")
    else:
        device.log(level="ERROR", message="AppQoE passive probe application details are not matching")
        raise Exception("AppQoE passive probe application details are not matching")

    return True

def get_appqoe_application_status(device=None, profile_name=None, application=None, dscp=None, dest_group_name=None, node="local", next_hop_id=None, server_ip=None):
    """
    To get the AppQoE SLA Application Status
    Example:
        get_appqoe_application_status(dev_obj, profile_name='apbr1', application='HTTP', dscp='36', dest_group_name='site1')

    ROBOT Example:
        Get Appqoe Application Status    device=${spoke}    profile_name=apbr1    application=HTTP    dest_group_name=site1   dscp=36

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns the dictionary for Application Details
    :rtype: dict
    Example returned dictionary:

       </apbr-prof-app-status>
        {'apbr-prof-app-status-monitor-sess': '0',
         'apbr-prof-app-status-path-switch': '7',
         'apbr-prof-app-status-sess': '0',
         'apbr-prof-app-status-sla-viol': '0'}

    """

    default_value_app_status = {'apbr-prof-app-status-monitor-sess': '0', 'apbr-prof-app-status-path-switch': '0', 'apbr-prof-app-status-sess': '0', 'apbr-prof-app-status-sla-viol': '0', 'apbr-prof-app-status-viol-probes':'0'}
    if device is None or profile_name is None  or dest_group_name is None:
        raise ValueError("Device handle, profile_name and dest_group_name is a mandatory argument")

    version = device.get_version()
    if float(version[:4]) >= 20.2:
        if next_hop_id is None:
            next_hop_id_dict = get_next_hop_id(device=device, profile_name=profile_name, application=application, dscp=dscp, node=node)
            if 'apbr-prof-app-brief' in next_hop_id_dict.keys():
                next_hop_id = next_hop_id_dict['apbr-prof-app-brief']['apbr-prof-app-brief-info']['apbr-prof-app-brief-nh']
            elif 'apbr-mesg' in next_hop_id_dict and "No data available" in next_hop_id_dict['apbr-mesg']['apbr-failed-msg']:
                stats = default_value_app_status
                return stats
    if application is not None and dscp is not None:
        if float(version[:4]) >= 20.2:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
                       " " + application + " " + 'dscp' + " " + dscp + " " + 'next-hop' + " " + next_hop_id + " " + 'status'
        else:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
                   " " + application + " " + 'dscp' + " " + dscp + " " + 'destination-group-name' + " " + dest_group_name + " " + 'status'
    elif application is not None:
        if float(version[:4]) >= 20.2:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
                       " " + application + " " + 'next-hop' + " " + next_hop_id + " " + 'status'
        else:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
                   " " + application + " " + 'destination-group-name' + " " + dest_group_name + " " + 'status'
    elif dscp is not None:
        if float(version[:4]) >= 20.2:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'dscp' + \
                       " " + dscp + " " + 'next-hop' + " " + next_hop_id + " " + 'status'
        else:
            cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'dscp' + \
                   " " + dscp + " " + 'destination-group-name' + " " + dest_group_name + " " + 'status'
    else:
        raise ValueError("Either Application or DSCP is mandatory argument")
    status = device.execute_as_rpc_command(command=cmd, node=node)
    if 'apbr-mesg' in status and "No data available" in status['apbr-mesg']['apbr-failed-msg']:
        stats = default_value_app_status
    else:
        stats = status['apbr-prof-app-status']
    return stats

def verify_appqoe_application_status(device=None, app_status=None, profile_name=None, application=None, dscp=None, dest_group_name=None, node="local", next_hop_id=None, server_ip=None):
    """
    To verify Appqoe application status.
    Example:
        verify_appqoe_application_status(dev_obj, profile_name='apbr1', application='HTTP', dest_group_name='site1',
        app_status={'apbr-prof-app-status-sla-viol': 8, 'apbr-prof-app-status-monitor-sess': 0})

    ROBOT Example:
        Verify Appqoe Application Status    device=${spoke}   profile_name=apbr1
        ...   application=HTTP    dest_group_name=site1    app_status=${violation_status}    dscp=36

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param dict app_status:
        **REQUIRED** Dictionary of counter names (key) and their expected values (value of the key).
        `Supported values of counter names (key)``: </apbr-prof-app-status>
                                                        {'apbr-prof-app-status-monitor-sess': '0',
                                                         'apbr-prof-app-status-path-switch': '7',
                                                         'apbr-prof-app-status-sess': '0',
                                                         'apbr-prof-app-status-sla-viol': '0'}
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: True/False , based on verification status
    :rtype: bool
    """
    if device is None or profile_name is None or dest_group_name is None:
        raise ValueError("Device handle, profile_name and dest_group_name is a mandatory argument")
    if application is None and dscp is None:
        raise ValueError("Either Application or DSCP is mandatory argument")
    if app_status is None:
        device.log(level="ERROR", message="app_status is None, it is mandatory argument")
        raise ValueError("app_status is None, it is mandatory argument")

    app_status_in_device = get_appqoe_application_status(device=device, profile_name=profile_name, \
                                                         application=application, dscp=dscp, dest_group_name=dest_group_name, \
                                                         node=node, next_hop_id=next_hop_id, server_ip=server_ip)
    flag = True
    #import pdb
    #pdb.set_trace()
    #import sys, pdb
    #pdb.Pdb(stdout=sys.__stdout__).set_trace()
    for counter in app_status.keys():

        if counter in app_status_in_device:
            if int(app_status[counter]) == int(app_status_in_device[counter]):
                device.log(level="INFO", message="%s has value %s , match successful" % (
                    counter, app_status_in_device[counter]))
            else:
                flag = False
                device.log(level="ERROR", message="%s has value %s , match is not successful" % (
                    counter, app_status_in_device[counter]))
        else:
            flag = False
            device.log(level="ERROR", message=counter + " counter not found in application status")

    if flag is False:
        device.log(level="ERROR", message="Application status validation failed")
        raise Exception("Application status validation failed")

    device.log(level="INFO", message="Application status validation passed")
    return flag

def get_appid_counter(device=None):
    """
    To get the AppID application counters as dictionary
    Example:
        get_appid_counter(device=device)

    ROBOT Example:
        Get Appid Counter  device=${device}

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :return: Returns the dictionary for applications statistics
    :rtype: dict
    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")
    cmd = "show services application-identification counter"
    counter_xml = device.execute_as_rpc_command(command=cmd)
    if "logical-system-counters" in counter_xml['appid-counter-information']:
        counters = counter_xml['appid-counter-information']['logical-system-counters']['appid-counter-usp']
    elif "appid-counter-usp" in counter_xml['appid-counter-information']:
        counters = counter_xml['appid-counter-information']['appid-counter-usp']
    else:
        raise ValueError("counter is not-recognised")
    counter_dict = {}
    counter_dict = dict(zip(counters['counter-name'], counters['counter-value']))
    return counter_dict

def verify_appid_counter(device=None, negate=False, counter_values=None):
    """
    To verify AppID counter.
    Example:
        verify_appid_counter(device=None, counter_values={'Unknown applications':'0'})

    ROBOT Example:
        Verify Appid Counter   device=${dt}   appcounter_dict=${'Unknown applications':'0'}

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param bool negate:
        *OPTIONAL* Pass True if you want to raise exceptions if the function fails.
    :param dict counter_values:
        *OPTIONAL* appid counter values to be matched.
    :return: Boolean (True or False)
    :rtype: bool
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")
    if counter_values is None:
        device.log(level="ERROR", message="counter_values argument is mandatory argument")
        raise ValueError("counter_values argument is mandatory argument")
    if not isinstance(counter_values, dict):
        device.log(level="ERROR", message="counter_values should be of dictionary type")
        raise ValueError("counter_values should be of dictionary type")
    if len(counter_values) == 0:
        device.log(level="ERROR", message="counter_values can't be empty, it is a mandatory argument")
        raise ValueError("counter_values can't be empty, it is a mandatory argument")
    appcounter_dict = get_appid_counter(device=device)
    keys = counter_values.keys()
    flag = 0
    for counter in keys:
        if counter in appcounter_dict:
            if counter_values[counter] == appcounter_dict[counter]:
                device.log(level="INFO", message="%s counter has the value %s , match is successful" % (
                    counter, appcounter_dict[counter]))
            else:
                flag = 1
                device.log(level="ERROR", message="%s counter has the value %s , match is not successful" % (
                    counter, appcounter_dict[counter]))
        else:
            flag = 1
            device.log(level="ERROR", message="%s counter not found in appid counters" % counter)

    if flag == 1:
        if negate:
            raise Exception("Application counters are not matching")
        return False
    return True

def check_srx_appfw_hit_count(device, rule_set=None, rule=None, match=None, redirect=None, **kwargs):
    '''
    Robot Example :
        ${srx0} =    Get Handle   resource=srx0
        Check SRX AppFW Hit Count    ${srx0}
        ...    rule_set = rule_set1
        ...    rule = rule1
        ...    application = junos:HTTP
        ...    encryption = no
        ...    action = permit
        ...    match = 2
        ...    redirect = 1

    :param str rule_set:
        *REQUIRED* rule-set name for check
    :param str rule:
        *REQUIRED* rule for check
    :param int match:
        *REQUIRED* Number of sessions matched.
    :param bool redirect:
        *REQUIRED* Number of sessions redirected.

    :param str application:
        *OPTIONAL* appfw configuration rule match dynamic_application.
    :param str action:
        *OPTIONAL* appfw configuration rule action.
    :param str encryption:
        *OPTIONAL* appfw configuration match trafic encrypted yes/no/any. Default value is any.
    :param int node:
        *OPTIONAL* check appfw hit count on HA node.
    :param str lsys:
        *OPTIONAL* check appfw hit count in logical-system.

    :return:
        TRUE: check hit count equal expect hit count
        FALSE: check hit count not equal expect hit count
    '''
# Check parameter
    valid_key = ['application', 'action', 'encryption', 'node', 'lsys']

    match = 'Number of sessions matched: %s' % match
    match = r'%s[^\w]*?Number of sessions redirected: %s' % (match, redirect)

    check_list = [rule_set]
    for key in (kwargs.get('application'), kwargs.get('encryption')):
        if key is not None:
            check_list.append(key)

    cmd = 'show security application-firewall rule-set %s' % rule_set
    if kwargs.get('node') is not None:
        cmd = '%s node %s ' % (cmd, kwargs.get('node'))
        check_list.append(kwargs.get('node'))

    if kwargs.get('lsys') is not None:
        cmd = '%s logical-system %s' % (cmd, kwargs.get('lsys'))
        check_list.append(kwargs.get('lsys'))

    return_value = device.cli(device=device, command=cmd).response()
    return_value = str(return_value)
    device.log(level='DEBUG', message="\n\nreturn_value is:\n%s\n" % return_value)

    if kwargs.get('action') is not None:
        expect = r'Rule.*?%s.*?%s[^\w]*?%s' % (rule, kwargs.get('action'), match)
    else:
        expect = r'Rule.*?%s.*?%s' % (rule, match)

    check_list.append(expect)
    device.log(level='DEBUG', message="\n\ncheck_list is:\n%s\n" % check_list)

    for key in check_list:
        if re.search(key, return_value, re.S):
            device.log(level='DEBUG', message="\ncheck_point: %s is in return_value\n" % key)
        else:
            raise Exception("check_point: %s is not in return_value" % key)

##################################################################
# From 20.2 the show command APPDB is changed.
# To get APPDB details we need next-hop id.
# Below keyword used to get the next-hop ID from new show command
#################################################################
def get_next_hop_id(device=None, profile_name=None, application=None, dscp=None, node='local'):
    """
    This keyword helps to get the next-hop id of the APPDB
    Example:
        get_next_hop_id(dev_obj, profile_name='apbr1', application='HTTP', dscp='63')

    ROBOT Example:
        Get Next Hop ID    device=${spoke}    profile_name=apbr1    application=my-http    dscp=63

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns the dictionary for Application Details
    :rtype: dict
    Example returned dictionary:

        {'apbr-prof-app-brief':
	    {'apbr-prof-app-brief-info':
		{'apbr-prof-app-brief-ip': '13.13.13.1',
		'apbr-prof-app-brief-dpg': 'site1',
		'apbr-prof-app-brief-nh': '262142',
		'apbr-prof-app-brief-server-ip': 'N/A'}}}
    """
    if device is None or profile_name is None:
        raise ValueError("Device handle, profile_name and dest_group_name is a mandatory argument")

    if application is not None and dscp is not None:
        cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
               " " + application + " " + 'dscp' + " " + dscp + " "
    elif application is not None:
        cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'application' + \
               " " + application + " "
    elif dscp is not None:
        cmd = 'show security advance-policy-based-routing sla profile ' + profile_name + " " + 'dscp' + \
               " " + dscp + " "
    else:
        raise ValueError("Either Application or DSCP is mandatory argument")
    status = device.execute_as_rpc_command(command=cmd, node=node)
    return status

