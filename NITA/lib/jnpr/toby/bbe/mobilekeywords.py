"""
Mobile Keywords for Mobile Testing in Toby
"""
import time
import ipaddress
import re
import numpy as np
import plotly
import os
from threading import Thread

def mobile_get_sx_association_stats(cups_test_handle, key_search='all'):
    """
    This method retrieves sx association stats retrieves chosen stats by the user

    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param key_search: list of keys to access stats dictionary or the string 'all'
    :return: dictionary of requested stats with their value
    """
    t.log("inside mobile_get_sx_association_stats")
    results = mobile_get_stats_results(cups_test_handle)
    if 'Sx Association' not in results:
        raise Exception('Error: Did not properly receive Sx Association stats. Received stats:\n' + repr(results))
    result_sx_association_dict = results['Sx Association']
    stats = {}
    if isinstance(key_search, list):
        for key in key_search:
            if key in result_sx_association_dict:
                stats.update({key: result_sx_association_dict[key]})
            else:
                raise Exception('ERROR: The search \'' + key
                                + '\' does not exist in Sx Association Stats.\n'
                                + 'Retrieved Stats: \n'
                                + repr(result_sx_association_dict))
    else:
        if key_search == 'all':
            for key in result_sx_association_dict:
                stats.update({key: result_sx_association_dict[key]})
        else:
            if key_search in result_sx_association_dict:
                stats.update({key_search: result_sx_association_dict[key_search]})
            else:
                raise Exception('ERROR: The search \'' + key_search
                                + '\' does not exist in Sx Association Stats.\n'
                                + 'Retrieved Stats: \n'
                                + repr(result_sx_association_dict))
    return stats


def mobile_get_sx_session_stats(cups_test_handle, key_search='all'):
    """
    This method retrieves Sx Session stats and returns the values requested by the user.

    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param key_search: list of keys to access stats dictionary
     or the string 'all' or string for single Sx Session stat
    :return: dictionary of requested Sx Session stats with their value
    """
    # get complete dictionary of results stats
    t.log("inside mobile_get_sx_session_stats")
    results = mobile_get_stats_results(cups_test_handle)
    if 'Sx Session' not in results:
        raise Exception('Error: Did not properly receive Sx Session stats. Received stats:\n' + repr(results))
    results_sx_session_dict = results['Sx Session']
    stats = {}
    # Support of list input
    if isinstance(key_search, list):
        for key in key_search:
            if key in results_sx_session_dict:
                stats.update({key: results_sx_session_dict[key]})
            else:
                # dump stats so the user can see the available keys
                raise Exception('Error: The search \'' + key
                                + '\' does not exist in Sx Session Stats.\nRetrievable Stats:\n'
                                + repr(results_sx_session_dict))
    # Support of string input (all must be a string, not a list)
    else:
        # Returns all results for Sx Session
        if key_search == 'all':
            for key in results_sx_session_dict:
                stats.update({key: results_sx_session_dict[key]})
        # search for one string in Sx Session results
        else:
            if key_search in results_sx_session_dict:
                stats.update({key_search: results_sx_session_dict[key_search]})
            else:
                # dump stats so the user can see the available keys
                raise Exception(
                    'Error: The search \'' + key_search
                    + '\' does not exist in Sx Session Stats.\nRetrievable Stats:\n'
                    + repr(results_sx_session_dict))
    return stats


def mobile_get_traffic_stats(cups_test_handle, traffic_type, key_search='all'):
    """
    This method retrieves mobile traffic stats for a specific traffic type and returns the stats in a dictionary.

    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param traffic_type: Traffic stats type. Several types are supported (L3 Client, L3 Server,
     L4 Client, L4 Server, L5-7 Client|Basic, L5-7 Server|Basic).
    :param key_search: List of keys to access stats dictionary
     or the string 'all' or string for single traffic_type stat
    :return: dictionary of requested traffic type's stats with their value
    """
    # Retrieve all peer type results stats
    t.log("inside mobile_get_traffic_stats")
    results = mobile_get_stats_results(cups_test_handle)
    # Verify if stats search type is traffic related
    types = ('L3 Client', 'L3 Server', 'L4 Client', 'L4 Server', 'L5-7 Client|Basic', 'L5-7 Server|Basic')
    if traffic_type not in types:
        raise Exception('Error: traffic search type is not defined. Supported types are:\n'
                        + repr(types))
    # Verify if traffic stats search type exists in retrieved results
    if traffic_type not in results:
        raise Exception('Error: Did not receive expected traffic stats for '
                        + traffic_type
                        + '. Received stats:\n%s' % results.keys())
    results_dict = results[traffic_type]
    stats = {}
    # Support of list input
    if isinstance(key_search, list):
        for key in key_search:
            if key in results_dict:
                stats.update({key: results_dict[key]})
            else:
                # dump stats so the user can see the available keys
                raise Exception('Error: The search \'' + key
                                + '\' does not exist in traffic ' + traffic_type + ' stats.\nRetrievable stats:\n'
                                + repr(results_dict))
    # Support of string input (all must be a string, not a list)
    else:
        # Returns all results for traffic type
        if key_search == 'all':
            for key in results_dict:
                stats.update({key: results_dict[key]})
        # search for one specific string in traffic type results
        else:
            if key_search in results_dict:
                stats.update({key_search: results_dict[key_search]})
            else:
                # dump stats so the user can see the available keys
                raise Exception('Error: The search \'' + key_search
                                + '\' does not exist in traffic ' + traffic_type + ' stats.\nRetrievable stats:\n'
                                + repr(results_dict))
    return stats


def mobile_get_stats_results(cups_test_handle, **kwargs):
    """
    This method retrieves the complete dictionary of landslides results stats.

    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param kwargs
    filter:     Options are 'node' or 'nodal'. Provides just the single test case statistics rather than Summary view.
    :return: Dictionary of all results stats.
    """
    t.log("inside mobile_get_stats_results")
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle

    if 'filter' in kwargs:
        if kwargs['filter'].lower() == 'node':
            kwargs['tsName'] = subs.tsname
            kwargs['testCaseName'] = subs.node_test_case_name
        if kwargs['filter'].lower() == 'nodal':
            kwargs['tsName'] = subs.tsname
            kwargs['testCaseName'] = subs.nodal_test_case_name

    count = 0
    results = subs.action(action='results', **kwargs)
    while count < 30 and 'status_message' in results:
        if results['status_message'] == 'The results are not yet available. Try after 10-15s':
            time.sleep(2)
            results = subs.action(action='results', **kwargs)
        count = count + 1
    return results


def mobile_configure_sgi_traffic(cups_test_handle, **kwargs):
    """
    mobile_configure_sgi_traffic(sub, name='tcp1', size=1000, payload_type='tcp',rate=1000)
    mobile_configure_sgi_traffic(sub, name='udp1', size=1000, payload_type='tcp',rate=1000, tos_list=['1','2'])
    :param cups_test_handle:      CUPSSubscribers or PGWSubscribers handle
    :param kwargs:
     name:                  traffic name, will be prepended with script name
     payload_type:          traffic payload type, e.g.raw/udp/tcp/ping/fb_udp/fb_tcp
     traffic_type:          ipv4 or ipv6 or dual
     packet_size:           traffic packet size, default is 1400
     host_type:             traffic network host type local/remote, default is local
     host_node_count:        Number of Nodes in traffic
     vlan_id:               uplink vlan id
     svlan_id:              uplink svlan id
     rate:                  traffic transation rate
     role:                  entity which sends the traffic. Options are client or server. Default is client.
     traffic_start_mode:    default is when session established, another mode is when all sessions established
     traffic_start_delay:   time to wait (in milliseconds) after session is up before sending traffic. Default is 1000
     fireball_mode:         true/false. Enables fireball data performance mode in Test Session. Test Server must be
        configured for fireball mode to set this true. Default is false.
     host_expansion_ratio:   Controls Tx/Rx ratio for sender of traffic. Value between 0 and 100. A value of 0
        corresponds to a Tx/Rx ratio of 100/0 (100% transmit)
    :return:
    """
    t.log("inside mobile_configure_sgi_traffic")
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle
    rt_device = subs.rt_device_id
    tester = t.get_handle(rt_device)
    traffic_type = kwargs.get('traffic_type', 'ipv4')
    testcase_type = '';
    if subs.subscribers_type == 'cups':
        testcase_type = 'sgw';
    elif subs.subscribers_type == 'pgw':
        testcase_type = 'pgw';
    # uplink_obj = bbe.get_interfaces('r0', interfaces='uplink')[0]
    # if 'ip' in uplink_obj.interface_config:
    #     v4addr = ipaddress.IPv4Interface(uplink_obj.interface_config['ip'])
    #     uplink_addr = str(v4addr.ip + 1)
    #     gateway = str(v4addr.ip)
    # if 'ipv6' in uplink_obj.interface_config:
    #     v6addr = ipaddress.IPv6Interface(uplink_obj.interface_config['ipv6'])
    #     v6_uplink_addr = str(v6addr.ip + 1)
    #     v6_gateway = str(v6addr.ip)
    # conn = bbe.get_connection('r0', interface='uplink0')
    if 'ipv4' in traffic_type:
        uplink_addr = subs.traffic_start_ip
        gateway = subs.uplink_gateway
    if 'ipv6' in traffic_type:
        v6_uplink_addr = subs.traffic_start_ipv6
        v6_gateway = subs.v6_uplink_gateway

    nodal_args = {}
    nodal_args['testCaseName'] = subs.nodal_test_case_name
    nodal_args['testCaseHandle'] = subs.nodal_testcase_handle
    nodal_args['mode'] = 'modify'
    nodal_args['testSessionHandle'] = subs.test_session_handle
    nodal_args['NetworkHost'] = kwargs.get('host_type', 'local')
    nodal_args['TrafficStartDelay'] = kwargs.get('traffic_start_delay', '1000')
    nodal_args['FireballEn'] = kwargs.get('fireball_mode', 'false')

    if not hasattr(subs, 'dmf_handle') or not subs.dmf_handle:
        subs.dmf_handle = {}
        subs.dmf_role = []
        subs.dmf_transport_list = []
        subs.dmf_lib_list = []
        subs.dmf_name_list = []
        nodal_args['DataTraffic'] = "Continuous"
        nodal_args['TrafficMtu'] = kwargs.get('mtu_size', '1450')

        nodal_args['TrafficStartType'] = kwargs.get('traffic_start_mode', "When Session Established")
        nodal_args['libraryName'] = subs.libname
        nodal_args['tsName'] = subs.tsname
        nodal_args['TestActivity'] = subs.test_activity
    if nodal_args['NetworkHost'] == 'local':
        nodal_args['NetworkHostNumOfNodes'] = int(kwargs.get('host_node_count', '1'))
        if 'ipv4' in traffic_type:
            nodal_args['NetworkHostPhy'] = subs.uplink_interface
            nodal_args['NetworkHostStartingIp'] = uplink_addr
            # nodal_args['NetworkHostNumOfNodes'] = int(kwargs.get('host_nod_count', '1'))
            nodal_args['NetworkNextHop'] = gateway
        if 'ipv6' in traffic_type:
            nodal_args['NetworkHostPhyIpv6'] = subs.uplink_v6_interface
            nodal_args['NetworkHostStartingIpv6'] = v6_uplink_addr
            # nodal_args['NetworkHostNumOfNodesIpv6'] = int(kwargs.get('host_nod_count', '1'))
            nodal_args['NetworkNextHopIpv6'] = v6_gateway
        # if 'dualstack' in traffic_type:
        #     nodal_args['NetworkHost'] = 'dualstack'
        #     # v6 args
        #     nodal_args['NetworkHostPhyIpv6'] = subs.uplink_v6_interface
        #     nodal_args['NetworkHostStartingIpv6'] = v6_uplink_addr
        #     nodal_args['NetworkHostNumOfNodesIpv6'] = int(kwargs.get('host_node_count', '1'))
        #     nodal_args['NetworkNextHopIpv6'] = v6_gateway
        #     # v4 args
        #     nodal_args['NetworkHostPhy'] = subs.uplink_interface
        #     nodal_args['NetworkHostStartingIp'] = uplink_addr
        #     # nodal_args['NetworkHostNumOfNodes'] = int(kwargs.get('host_nod_count', '1'))
        #     nodal_args['NetworkNextHop'] = gateway

    if nodal_args['NetworkHost'] == 'remote':
        nodal_args['NetworkHostAddrRemoteList'] = [uplink_addr]
    if 'vlan' in kwargs or 'svlan' in kwargs:
        nodal_args['NetworkHostVlanId'] = kwargs['vlan']
        if 'dualstack' in traffic_type:
            nodal_args['NetworkHostVlanIdIpv6'] = kwargs['vlan']
        if 'svlan' in kwargs:
            nodal_args['NetworkHostVlanId'] = kwargs['svlan']
            nodal_args['NetworkHostInnerVlanId'] = kwargs['vlan']
            if 'dualstack' in traffic_type:
                nodal_args['NetworkHostVlanIdIpv6'] = kwargs['svlan']
                nodal_args['NetworkHostInnerVlanIdIpv6'] = kwargs['vlan']
    dmf_args = {}
    dmf_args['dmfName'] = t._script_name + "_" + kwargs['name']
    dmf_args['mode'] = 'create'
    dmf_args['DataProtocol'] = kwargs.get('payload_type', 'raw')
    dmf_args['TransactionRate'] = kwargs.get('rate', '1000')
    dmf_args['libraryName'] = subs.libname
    dmf_args['TotalTransactions'] = '0'

    dmf_args['PacketSize'] = kwargs.get('packet_size', '1000')
    dmf_args['TimeToLive'] = kwargs.get('ttl', '64')
    dmf_args['SegmentSize'] = kwargs.get('segment_size', '900')
    dmf_args['HostDataExpansionRatio'] = kwargs.get('host_expansion_ratio', '1')
    role = kwargs.get('role', 'client')
    transport = kwargs.get('preferred_transport', 'any')
    dmf_args['InitiatingSide'] = role
    if dmf_args['DataProtocol'] == 'udp' or dmf_args['DataProtocol'] == 'fb_udp':
        if int(dmf_args['PacketSize']) <= int(dmf_args['SegmentSize']):
            if 'udp_burst_count' in kwargs:
                dmf_args['BurstCount'] = kwargs['udp_burst_count']
    elif dmf_args['DataProtocol'] == 'tcp' or dmf_args['DataProtocol'] == 'fb_tcp':
        if 'tcp_socket_disc_side' in kwargs:
            dmf_args['DisconnectSide'] = kwargs['tcp_socket_disc_side']
        if 'tcp_3way_handshake' in kwargs:
            dmf_args['Force3Way'] = kwargs['tcp_3way_handshake']
        if 'tcp_disconnect_type' in kwargs:
            dmf_args['DisconnectType'] = kwargs['tcp_disconnect_type']
        if 'tcp_congestion_avoid' in kwargs:
            dmf_args['SlowStart'] = kwargs['tcp_congestion_avoid']
        if 'tcp_window_size' in kwargs:
            dmf_args['WindowSize'] = kwargs['tcp_window_size']
        if 'tcp_max_segment_size' in kwargs:
            dmf_args['MaxSegmentSize'] = kwargs['tcp_max_segment_size']
        if 'tcp_min_header_size' in kwargs:
            dmf_args['MinTcpHeaderSize'] = kwargs['tcp_min_header_size']
        if 'tcp_max_packets_before_ack' in kwargs:
            dmf_args['MaxPacketsToForceAck'] = kwargs['tcp_max_packets_before_ack']

    if 'tos_list' in kwargs:
        tos_list = kwargs['tos_list']
        for index in range(len(tos_list)):
            dmf_name = t._script_name + "_" + kwargs['name'] + str(index)
            dmf_args['dmfName'] = dmf_name
            if 'client_port' in kwargs:
                dmf_args['ClientPort'] = int(kwargs['client_port']) + index
            if 'server_port' in kwargs:
                dmf_args['ServerPort'] = int(kwargs['server_port']) + index
            dmf_args['TypeOfService'] = tos_list[index]

            subs.dmf_handle[dmf_name] = tester.invoke('config_dmf', **dmf_args)
            t.log("created dmf stream {} with args {}".format(dmf_name, dmf_args))
            subs.dmf_lib_list.append(subs.libname)
            subs.dmf_name_list.append(dmf_name)
            subs.dmf_role.append(role)
            subs.dmf_transport_list.append(transport)
    else:
        dmf_name = dmf_args['dmfName']
        if 'client_port' in kwargs:
            dmf_args['ClientPort'] = kwargs['client_port']
        if 'server_port' in kwargs:
            dmf_args['ServerPort'] = kwargs['server_port']
        subs.dmf_handle[dmf_name] = tester.invoke('config_dmf', **dmf_args)
        t.log("created dmf stream {} with args {}".format(dmf_name, dmf_args))
        subs.dmf_lib_list.append(subs.libname)
        subs.dmf_name_list.append(dmf_name)
        subs.dmf_role.append(role)
        subs.dmf_transport_list.append(transport)

    if subs.dmf_role:
        nodal_args['nodeRoleList'] = subs.dmf_role
    if subs.dmf_transport_list:
        nodal_args['preferredTransportList'] = subs.dmf_transport_list
    if subs.dmf_lib_list:
        nodal_args['dmfLibraryList'] = subs.dmf_lib_list
    if subs.dmf_name_list:
        nodal_args['dmfList'] = subs.dmf_name_list
    print("nodal_args is {}".format(nodal_args))

    tester.invoke(testcase_type + '_nodal_testcase', **nodal_args)

    validation_status = tester.invoke('validate_test_configuration', testSessionHandle=subs.test_session_handle)
    t.log("Validation Status: {}".format(validation_status))
    # Save the Nodal and Node testcases and test sessions
    tester.invoke('save_config', instance=subs.test_session_handle, overwrite='1')


def mobile_remove_traffic(cups_test_handle, **kwargs):
    """
    mobile_remove_traffic(sub)
    mobile_remove_traffic(sub, name='udp1')
    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param kwargs:
    name:                    traffic name, optional
    :return:
    """

    t.log("inside mobile_remove_traffic")
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle

    testcase_type = '';
    if subs.subscribers_type == 'cups':
        testcase_type = 'sgw';
    elif subs.subscribers_type == 'pgw':
        testcase_type = 'pgw';
    tester = t.get_handle(subs.rt_device_id)
    if 'name' in kwargs:
        name_list = []
        for item in subs.dmf_name_list:
            if kwargs['name'] in item:
                name_list.append(item)
        for name in name_list:
            tester.invoke('delete_dmf', dmfName=name, libraryName=subs.libname)
            subs.dmf_handle.pop(name)
            subs.dmf_name_list.remove(name)
            subs.dmf_role.pop(-1)
            subs.dmf_transport_list.pop(-1)
            subs.dmf_lib_list.pop(-1)
        if not name_list:
            raise Exception("traffic name {} is not in the {}".format(kwargs['name'], subs.dmf_name_list))
        if not subs.dmf_name_list:
            tester.invoke(testcase_type + '_nodal_testcase', mode='modify', testCaseHandle=subs.nodal_testcase_handle,
                          testSessionHandle=subs.test_session_handle, DataTraffic='Disabled')
        else:
            nodal_args = {}
            nodal_args['testCaseHandle'] = subs.nodal_testcase_handle
            nodal_args['testSessionHandle'] = subs.test_session_handle
            if subs.dmf_role:
                nodal_args['nodeRoleList'] = subs.dmf_role
            if subs.dmf_transport_list:
                nodal_args['preferredTransportList'] = subs.dmf_transport_list
            if subs.dmf_lib_list:
                nodal_args['dmfLibraryList'] = subs.dmf_lib_list
            if subs.dmf_name_list:
                nodal_args['dmfList'] = subs.dmf_name_list
            tester.invoke(testcase_type + '_nodal_testcase', mode='modify', **nodal_args)

    else:
        if hasattr(subs, 'dmf_name_list') and subs.dmf_name_list:
            for item in subs.dmf_name_list:
                tester.invoke('delete_dmf', dmfName=item, libraryName=subs.libname)
            tester.invoke(testcase_type + '_nodal_testcase', mode='modify', testCaseHandle=subs.nodal_testcase_handle,
                          testSessionHandle=subs.test_session_handle, DataTraffic='Disabled')
        else:
            t.log("test session does not have traffic enabled")
            return

    validation_status = tester.invoke('validate_test_configuration', testSessionHandle=subs.test_session_handle)
    t.log("Validation Status: {}".format(validation_status))
    # Save the Nodal and Node testcases and test sessions
    tester.invoke('save_config', instance=subs.test_session_handle, overwrite='1')
    if 'name' not in kwargs:
        subs.dmf_handle = {}
        subs.dmf_role = []
        subs.dmf_transport_list = []
        subs.dmf_lib_list = []
        subs.dmf_name_list = []


def mobile_login_sx_session(cups_test_handle, group='default', sessions_per_second='100', modify_apn=1,
                            modify_pdn=0, pdn_type=1, interval=1, retries=10, **kwargs):
    """
    This keyword logins in a cups_test_handle
    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param group: subsection of session to be logged in, defined in bbe.yaml, if not defined groups in yaml, it will login all
    :param sessions_per_second: the rate in which to login at
    :param modify_apn: flag to set whether you are choosing an apn to login on
    :param modify_pdn: flag to set if you are changing pdn (ipv4, ipv6, both)
    :param pdn_type: specifying PDN type: 1 = IPv4, 2 = IPv6, 3 = Both
    :param interval: number of seconds between checks
    :param retries: how many times to check login
    :param kwargs:
    auto_capture_on_start: Default is false. When true, all tester ports will have packet capture enabled
    auto_capture_on_start: Default is false. When true, all tester ports will have packet capture enabled
    stats_router:               Verify logout rate from the router (default: False)
    stats_router_id:            Router to use during calculating rate (default: "r0")
    stats_router_interval:      Interval in seconds between getting stats (default: 5)
    stats_router_pfe:           Log FPC memory in a background thread (default: False)
    stats_router_pfe_slots:     List of which fpc slots to log - example: ["4", "7"] (default: all from router)
    stats_router_full_graph:    Create a large graph containing both login and logout stats (default: False)
                                    If True, bearer should be consistent between login and logout calls,
                                    and this option should be enabled on both calls
    stats_tester:               Verify logout rate from the tester (default: False)
    stats_tester_full_graph:    Create a large graph containing both login and logout stats (default: False)
                                    If True, bearer should be consistent between login and logout calls,
                                    and this option should be enabled on both calls
    stats_timeout:              Timeout in seconds before successful start (default: 60)
    stats_bearer:               Type of bearer - "default"/"dedicated"/"both" (default: "default")
    stats_scale:                Number of expected sessions for default bearer (default: from cups_test_handle)
    stats_scale_dedicated:      Number of expected sessions for dedicated bearer (default: from cups_test_handle)
    stats_report_percent:       Percentage of scale to report rate (default: 90)
    stats_repeated_zeros:       Consecutive zero connect rates (after successful start) before stopping (default: 1)
    :return:
    """
    t.log("inside mobile_login_sx_session")
    stats_router = kwargs.get("stats_router", False)
    stats_tester = kwargs.get("stats_tester", False)
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'subscriber handle has multiple entries')
    else:
        subs = cups_test_handle
    tester_handle = t.get_handle(resource=subs.rt_device_id)
    if 'Command Mode' not in subs.test_activity:
        raise Exception("ERROR: Keyword login sx session only supported for CUPSSubscribers in Command Mode!\n")

    if not subs.isactive:
        # enable auto pcap if desired
        enable_pcap_on_start = kwargs.get('auto_capture_on_start', 'false')
        if 'true' in enable_pcap_on_start.lower():
            pcap_config_setup = 'ls::perform GeneratePortCaptureConfiguration -TestSession ' + subs.test_session_handle
            tester_handle.invoke('invoke', cmd=pcap_config_setup)
            pcap_config_setup = 'ls::get ' + subs.test_session_handle + ' -children-PortCaptureConfig'
            num_ports = len(tester_handle.invoke('invoke', cmd=pcap_config_setup).split('} {'))
            for count in range(0, num_ports, 1):
                invoke_cmd = 'ls::config ' + subs.test_session_handle + '.PortCaptureConfig(' + str(count) + \
                             ') -OnStart ' + enable_pcap_on_start
                tester_handle.invoke('invoke', cmd=invoke_cmd)
            tester_handle.invoke('save_config', instance=subs.test_session_handle, overwrite='1')

        subs.action(action='start')
        command_for_session_state = 'ls::get ' + subs.test_session_handle + ' -TestStateOrStep'
        for retry in range(0, int(retries)):
            retval = tester_handle.invoke('invoke', cmd=command_for_session_state)
            if '6_Waiting' in retval:
                time.sleep(interval)
                break
            elif '3_Waiting' in retval:
                for count in range(0, 3):
                    time.sleep(interval)
                    try:
                        subs.action(action='continue')
                        break
                    except Exception as errors:
                        t.log("landslide logs an {}".format(errors.args[0]))
                        if 'Session is no longer running' not in errors.args[0]:
                            break

            time.sleep(int(interval))

    # code for getting groups:
    indices = subs.subscriber_group_indices[group]


    command_mode_action = 'ControlBearer {\"op=Attach\" \"rate=' + str(sessions_per_second) \
                          + '\" \"start_sub=' + str(indices[0]) + '\" \"end_sub=' + str(indices[1]) \
                          + '\" \"mod_apn=' + str(modify_apn) \
                          + '\" \"apn=' + str(subs.apn_name) + '\" \"mod_pdn=' + str(modify_pdn) \
                          + '\" \"pdn_type=' + str(pdn_type) + '\"}'
    if stats_router or stats_tester:
        if "stats_scale" not in kwargs:
            kwargs["stats_scale"] = subs.session_count * subs.bearer_per_session
        if "stats_scale_dedicated" not in kwargs:
            kwargs["stats_scale_dedicated"] = subs.session_count * subs.dedicated_bearers
        kwargs["stats_mode"] = "login"
        if stats_router:
            stats_router_thread = Thread(target=mobile_calculate_router_stats,
                                         name="Router Stats Background Thread (Login)",
                                         kwargs=kwargs)
            stats_router_thread.start()
        if stats_tester:
            stats_tester_thread = Thread(target=mobile_calculate_tester_stats,
                                         name="Tester Stats Background Thread (Login)",
                                         args=(subs,),
                                         kwargs=kwargs)
            stats_tester_thread.start()
        # Sleep in order to prevent login call from tester_handle conflicting
        time.sleep(2)

    tester_handle.invoke('on_demand_command', testSessionHandle=subs.test_session_handle, tsName=subs.tsname,
                         testCaseName=subs.nodal_test_case_name, actionCommand=command_mode_action)

    t.log('Sx Session login initiated...\n')
    if stats_router:
        stats_router_thread.join()
        t.log("Router stats complete.")
    if stats_tester:
        stats_tester_thread.join()
        t.log("Tester stats complete.")


def mobile_logout_sx_session(cups_test_handle, group='default', sessions_per_second='100', **kwargs):
    """
    This keyword will logout specified subscribers of the corresponding cups_test_handle.

    :param cups_test_handle:    CUPSSubscribers or PGWSubscribers handle
    :param group:               subsection of session to be logged out, defined in bbe.yaml (default: "default")
    :param sessions_per_second: The logout rate (default: 100)
    :param kwargs:
    stats_router:               Verify logout rate from the router (default: False)
    stats_router_id:            Router to use during calculating rate (default: "r0")
    stats_router_interval:      Interval in seconds between getting stats (default: 5)
    stats_router_pfe:           Log FPC memory in a background thread (default: False)
    stats_router_pfe_slots:     List of which fpc slots to log - example: ["4", "7"] (default: all from router)
    stats_router_full_graph:    Create a large graph containing both login and logout stats (default: False)
                                    If True, bearer should be consistent between login and logout calls,
                                    and this option should be enabled on both calls
    stats_tester:               Verify logout rate from the tester (default: False)
    stats_tester_full_graph:    Create a large graph containing both login and logout stats (default: False)
                                    If True, bearer should be consistent between login and logout calls,
                                    and this option should be enabled on both calls
    stats_timeout:              Timeout in seconds before successful start (default: 60)
    stats_bearer:               Type of bearer - "default"/"dedicated"/"both" (default: "default")
    stats_scale:                Number of expected sessions for default bearer (default: from cups_test_handle)
    stats_scale_dedicated:      Number of expected sessions for dedicated bearer (default: from cups_test_handle)
    stats_report_percent:       Percentage of scale to report rate (default: 90)
    stats_repeated_zeros:       Consecutive zero connect rates (after successful start) before stopping (default: 1)
    :return:
    """
    t.log("inside mobile_logout_sx_session")
    stats_router = kwargs.get("stats_router", False)
    stats_tester = kwargs.get("stats_tester", False)
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle
    if group not in subs.subscriber_group_indices:
        raise Exception("Error: Subscriber group " + group
                        + " is not defined. The following subscriber groups are defined: "
                        + str(subs.subscriber_group_indices))
    group_index = subs.subscriber_group_indices[group]
    tester_handle = t.get_handle(resource=subs.rt_device_id)
    if 'Command Mode' not in subs.test_activity:
        raise Exception("Keyword Logout Sx Session only supported for CUPSSubscribers in Command Mode!\n")
    if not subs.isactive:
        raise Exception("Sx Session must be active in order to logout Sx Session.")
    command_for_session_state = 'ls::get ' + subs.test_session_handle + ' -TestStateOrStep'
    retval = tester_handle.invoke('invoke', cmd=command_for_session_state)
    if 'Waiting' not in retval:
        subs.isactive = False
        t.log("WARNING, Sx Session not properly running. Cannot execute Sx Session logout.")
        return
    command_mode_action = 'ControlBearer {\"op=Detach\" \"rate=' + str(sessions_per_second) + '\" \"start_sub=' \
                          + str(group_index[0]) + '\" ' \
                          '\"end_sub=' + str(group_index[1]) + '\"}'
    if stats_router or stats_tester:
        if "stats_scale" not in kwargs:
            kwargs["stats_scale"] = subs.session_count * subs.bearer_per_session
        if "stats_scale_dedicated" not in kwargs:
            kwargs["stats_scale_dedicated"] = subs.session_count * subs.dedicated_bearers
        kwargs["stats_mode"] = "logout"
        if stats_router:
            stats_router_thread = Thread(target=mobile_calculate_router_stats,
                                         name="Router Stats Background Thread (Logout)",
                                         kwargs=kwargs)
            stats_router_thread.start()
        if stats_tester:
            stats_tester_thread = Thread(target=mobile_calculate_tester_stats,
                                         name="Tester Stats Background Thread (Logout)",
                                         args=(subs,),
                                         kwargs=kwargs)
            stats_tester_thread.start()
        # Sleep in order to prevent logout call from tester_handle conflicting
        time.sleep(2)
    tester_handle.invoke('on_demand_command', testSessionHandle=subs.test_session_handle,
                         tsName=subs.tsname, testCaseName=subs.nodal_test_case_name,
                         actionCommand=command_mode_action)
    t.log('Sx Session logout initiated...\n')
    if stats_router:
        stats_router_thread.join()
        t.log("Router stats complete.")
    if stats_tester:
        stats_tester_thread.join()
        t.log("Tester stats complete.")

def mobile_calculate_router_stats(**kwargs):
    """
    This method is used inside of mobile_login/logout_sx_session to calculate and log the logout rate from the router
    stats_mode:                 "login"/"logout" (required)
    stats_scale:                Number of expected sessions for default bearer (required)
    stats_scale_dedicated:      Number of expected sessions for dedicated bearer (required)
    stats_router:               Verify logout rate from the router (default: False)
    stats_router_id:            Router to use during calculating rate (default: "r0")
    stats_router_interval:      Interval in seconds between getting stats (default: 5)
    stats_router_pfe:           Log FPC memory as well (default: False)
    stats_router_pfe_slots:     List of which fpc slots to log - example: ["4", "7"] (default: all from router)
    stats_router_full_graph:    Create a large graph containing both login and logout stats (default: False)
                                    If True, bearer should be consistent between login and logout calls,
                                    and this option should be enabled on both calls
    stats_timeout:              Timeout in seconds before successful start (default: 60)
    stats_bearer:               Type of bearer - "default"/"dedicated"/"both" (default: "default")
    stats_report_percent:       Percentage of scale to report rate (default: 90)
    stats_repeated_zeros:       Consecutive zero connect rates (after successful start) before stopping (default: 1)
    """
    t.log("inside mobile_calculate_router_stats")
    mode = kwargs.get("stats_mode").lower()
    router_id = kwargs.get("stats_router_id", "r0")
    router = t.get_handle(resource=router_id)
    bearer = kwargs.get("stats_bearer", "default").lower()
    timeout = int(kwargs.get("stats_timeout", 60))
    interval = int(kwargs.get("stats_router_interval", 5))
    pfe = kwargs.get("stats_router_pfe", False)
    stop_repeated = int(kwargs.get("stats_repeated_zeros", 1))
    full_graph = kwargs.get("stats_router_full_graph", False)
    graph_filename = "mobile_router_stats_{:s}.html".format(mode)
    full_graph_filename = "mobile_router_stats_full.html"

    if mode not in ["login", "logout"]:
        raise Exception("mobile_calculate_router_stats mode must be \"login\" or \"logout\"")
    if bearer not in ["default", "dedicated", "both"]:
        raise Exception("mobile_calculate_router_stats bearer must be \"default\", \"dedicated\", or \"both\"")

    default_bearer = (bearer == "default") or (bearer == "both")
    dedicated_bearer = (bearer == "dedicated") or (bearer == "both")

    if default_bearer:
        regex_obj = re.compile(r"Sessions by State:\s*(.*\s*)?\s*ESTABLISHED: (\d+)")
        scale = int(kwargs.get("stats_scale"))
    else:
        regex_obj = re.compile(r"Bearers by State:\s*(.*\s*)?\s*ESTABLISHED: (\d+)")
        scale = int(kwargs.get("stats_scale_dedicated"))
    report_scale = (scale * int(kwargs.get("stats_report_percent", 90))) / 100.0

    resp = router.cli(command="show services mobile-edge sessions summary").resp
    sessions_i = 0
    temp = regex_obj.search(resp)
    if temp:
        sessions_i = int(temp.group(2))
    time_i = time.time()
    sessions_f = sessions_i
    time_f = time_i
    sessions_start = sessions_i
    time_start = time_i

    timestamps = [time.ctime(time_i)]
    sessions = [sessions_i]
    rates = [0]

    started = False
    stop_reason = "NOT STOPPED"
    consecutive_zeros = 0
    reported_rate = None

    if pfe:
        if "stats_router_pfe_slots" in kwargs:
            pfe_slots = kwargs.get("stats_router_pfe_slots", [])
            if not isinstance(pfe_slots, list):
                pfe_slots = [pfe_slots]
            pfe_slots = ["fpc" + str(slot) for slot in pfe_slots]
        else:
            pfe_slots = []
            for name in t.resources[router_id]['interfaces']:
                if 'access' in name or 'transit' in name:
                    match = re.match(r'\S+-(\d+)/\d+/\d+', t.resources[router_id]['interfaces'][name]['pic'])
                    slot = match.group(1)
                    slot = "fpc" + slot
                    if slot not in pfe_slots:
                        pfe_slots.append(slot)

    while True:
        if pfe:
            for slot in pfe_slots:
                pfe_num = 0
                error = False
                while not error:
                    # Assume pfe slots are consecutive, this would break if pfe ids were 0 and 2 but not 1
                    command_list = ["cprod -A {} -c show jnh {} pool detail".format(slot, pfe_num),
                                    "cprod -A {} -c show jnh {} pool composition".format(slot, pfe_num),
                                    "cprod -A {} -c show jnh {} pool layout".format(slot, pfe_num),
                                    "cprod -A {} -c show memory".format(slot)]
                    for command in command_list:
                        resp = router.shell(command=command).resp
                        if "ERROR: invalid pfe instance!" in resp:
                            error = True
                            break
                    pfe_num += 1
        router.cli(command="show chassis fpc")
        router.cli(command="show system processes extensive | no-more")

        resp = router.cli(command="show services mobile-edge sessions summary").resp
        temp = regex_obj.search(resp)
        sessions_f = 0
        if temp:
            sessions_f = int(temp.group(2))
        time_f = time.time()
        rate = (sessions_f - sessions_i) / (time_f - time_i)
        if mode == "logout":
            rate *= -1
        t.log("{:s} rate from the router at {:s}: {:.3f}".format(str.capitalize(mode), time.ctime(time_f), rate))
        sessions.append(sessions_f)
        timestamps.append(time.ctime(time_f))
        rates.append(rate)
        sessions_i = sessions_f
        time_i = time_f

        if not started and rate != 0:
            started = True

        if rate == 0:
            consecutive_zeros += 1
        else:
            consecutive_zeros = 0

        if started:
            if mode == "login" and reported_rate == None and sessions_f >= report_scale:
                reported_rate = rate
            if mode == "login" and sessions_f == scale:
                stop_reason = "All sessions logged in"
                break
            if mode == "logout" and sessions_f == 0:
                stop_reason = "All sessions logged out"
                break
            if consecutive_zeros == stop_repeated:
                stop_reason = "Sessions unchanged for at least {:d} seconds".format(interval * stop_repeated)
                break
        else:
            if time.time() - time_start > timeout:
                stop_reason = "Sessions never changed, timeout after {:d} seconds".format(timeout)
                break
        time.sleep(interval)
    t.log("Finished {:s} rate from router detection because: {:s}".format(mode, stop_reason))

    rate = (sessions_f - sessions_start) / (time_f - time_start)
    if mode == "logout":
        rate *= -1
    t.log("Overall {:s} rate from router: {:.3f}".format(mode, rate))

    # Store data in a plotly graph
    data = []
    trace_rates = plotly.graph_objs.Scatter(
        x=timestamps,
        y=rates,
        mode="lines+markers",
        name="{:s} rate (Sessions/Second)".format(str.capitalize(mode)),
    )
    trace_sessions = plotly.graph_objs.Scatter(
        x=timestamps,
        y=sessions,
        mode="lines+markers",
        name="Sessions Established",
    )
    data.append(trace_rates)
    data.append(trace_sessions)
    plotly.offline.plot(data, filename=graph_filename, auto_open=False)

    if full_graph:
        if mode == "login":
            saved_data = {
                "timestamps": timestamps,
                "rates": rates,
                "sessions": sessions,
            }
            np.savez("temp_mobile_router_stats_full.npz", **saved_data)
        if mode == "logout":
            saved_data = np.load("temp_mobile_router_stats_full.npz")
            os.remove("temp_mobile_router_stats_full.npz")
            data = []

            # Store data in a plotly graph
            data = []
            login_trace_rates = plotly.graph_objs.Scatter(
                x=saved_data["timestamps"],
                y=saved_data["rates"],
                mode="lines+markers",
                name="Login rate (Sessions/Second)",
            )
            login_trace_sessions = plotly.graph_objs.Scatter(
                x=saved_data["timestamps"],
                y=saved_data["sessions"],
                mode="lines+markers",
                name="Sessions Established",
            )
            data.append(login_trace_rates)
            data.append(login_trace_sessions)
            logout_trace_rates = plotly.graph_objs.Scatter(
                x=timestamps,
                y=rates,
                mode="lines+markers",
                name="Logout rate (Sessions/Second)",
            )
            logout_trace_sessions = plotly.graph_objs.Scatter(
                x=timestamps,
                y=sessions,
                mode="lines+markers",
                name="Sessions Established",
            )
            data.append(logout_trace_rates)
            data.append(logout_trace_sessions)
            plotly.offline.plot(data, filename=full_graph_filename, auto_open=False)

    # Trim leading and trailing zeros because otherwise min/max makes no sense
    rates_for_stats = np.trim_zeros(np.array(rates))
    if rates_for_stats.size == 0:
        rates_for_stats = np.array([0.0])
    result = {
        "reported_rate": reported_rate,
        "actual_{:s}_rates_timestamps".format(mode): timestamps,
        "actual_{:s}_rates".format(mode): rates,
        "average_{:s}_rate".format(mode): np.mean(rates_for_stats),
        "maximum_{:s}_rate".format(mode): np.max(rates_for_stats),
        "minimum_{:s}_rate".format(mode): np.min(rates_for_stats),
        "median_{:s}_rate".format(mode): np.median(rates_for_stats),
        "standard_deviation_rate": np.std(rates_for_stats),
    }
    t.log(result)

def mobile_calculate_tester_stats(cups_test_handle, **kwargs):
    """
    This method is used inside of mobile_login/logout_sx_session to calculate and log the logout rate from the router
    :param cups_test_handle:    CUPSSubscribers or PGWSubscribers handle
    :param kwargs:
    stats_mode:                 "login"/"logout" (required)
    stats_scale:                Number of expected sessions for default bearer (required)
    stats_scale_dedicated:      Number of expected sessions for dedicated bearer (required)
    stats_tester:               Verify logout rate from the tester (default: False)
    stats_tester_full_graph:    Create a large graph containing both login and logout stats (default: False)
                                    If True, bearer should be consistent between login and logout calls,
                                    and this option should be enabled on both calls
    stats_timeout:              Timeout in seconds before successful start (default: 60)
    stats_bearer:               Type of bearer - "default"/"dedicated"/"both" (default: "default")
    stats_report_percent:       Percentage of scale to report rate (default: 90)
    stats_repeated_zeros:       Consecutive zero connect rates (after successful start) before stopping (default: 1)
    :return:                    A dictionary containing statistics about connection rates
    """
    t.log("inside mobile_calculate_tester_stats")
    mode = kwargs.get("stats_mode").lower()
    bearer = kwargs.get("stats_bearer", "default").lower()
    scale_default = int(kwargs.get("stats_scale"))
    scale_dedicated = int(kwargs.get("stats_scale_dedicated"))
    report_scale_percentage = int(kwargs.get("stats_report_percent", 90))
    report_scale_default = int(scale_default * report_scale_percentage / 100.0)
    report_scale_dedicated = int(scale_dedicated * report_scale_percentage / 100.0)
    stop_repeated = int(kwargs.get("stats_repeated_zeros", 1))
    stop_timeout = int(kwargs.get("stats_timeout", 60))
    full_graph = kwargs.get("stats_tester_full_graph", False)
    graph_filename = "mobile_tester_stats_{:s}.html".format(mode)
    full_graph_filename = "mobile_tester_stats_full.html"

    if mode not in ["login", "logout"]:
        raise Exception("mobile_calculate_tester_stats mode must be \"login\" or \"logout\"")
    if bearer not in ["default", "dedicated", "both"]:
        raise Exception("mobile_calculate_tester_stats bearer must be \"default\", \"dedicated\", or \"both\"")

    default_bearer = (bearer == "default") or (bearer == "both")
    dedicated_bearer = (bearer == "dedicated") or (bearer == "both")
    rate_type = None
    if mode == "login":
        rate_type = "Connect"
    if mode == "logout":
        rate_type = "Disconnect"

    reported_default_rate = None
    reported_dedicated_rate = None
    default_rates = []
    dedicated_rates = []
    sessions_established_default = []
    sessions_established_dedicated = []
    consecutive_default_rate_zeros = 0
    consecutive_dedicated_rate_zeros = 0
    consecutive_sessions_default_unchanged = 0
    consecutive_sessions_dedicated_unchanged = 0

    started = False
    timestamps = []
    stop_reason = "NOT STOPPED"
    start_time = time.time()

    while True:
        filter_node = "node" if mode == "login" else "nodal"
        stats = mobile_get_stats_results(cups_test_handle, filter=filter_node)["Test Summary"]
        timestamps.append(time.ctime())
        default_rate = float(stats.get("Actual {:s} Rate (Sessions/Second)".format(rate_type), 0.0))
        dedicated_rate = float(stats.get("Actual Dedicated Bearer Session {:s} Rate (Sessions/Second)".format(rate_type), 0.0))
        sessions_default = int(stats.get("Sessions Established", 0))
        sessions_dedicated = int(stats.get("Dedicated Bearer Sessions Established", 0))
        default_rates.append(default_rate)
        dedicated_rates.append(dedicated_rate)
        sessions_established_default.append(sessions_default)
        sessions_established_dedicated.append(sessions_dedicated)

        if default_rate == 0.0:
            consecutive_default_rate_zeros += 1
        else:
            consecutive_default_rate_zeros = 0
        if dedicated_rate == 0.0:
            consecutive_dedicated_rate_zeros += 1
        else:
            consecutive_dedicated_rate_zeros = 0
        # The rate we get may not be equal to our change in sessions. If sessions are unchanged, we stop
        if len(sessions_established_default) >= 2 and sessions_default == sessions_established_default[-2]:
            consecutive_sessions_default_unchanged += 1
        else:
            consecutive_sessions_default_unchanged = 0
        if len(sessions_established_dedicated) >= 2 and sessions_dedicated == sessions_established_dedicated[-2]:
            consecutive_sessions_dedicated_unchanged += 1
        else:
            consecutive_sessions_dedicated_unchanged = 0


        if not started:
            if default_bearer and default_rate != 0.0:
                started = True
            if dedicated_bearer and dedicated_rate != 0.0:
                started = True

        if started:
            if mode == "login":
                if default_bearer and reported_default_rate is None and sessions_default >= report_scale_default:
                    reported_default_rate = default_rate
                if dedicated_bearer and reported_dedicated_rate is None and sessions_dedicated >= report_scale_dedicated:
                    reported_dedicated_rate = dedicated_rate

                all_sessions_default_connected = not default_bearer or sessions_default == scale_default
                all_sessions_dedicated_connected = not dedicated_bearer or sessions_dedicated == scale_dedicated
                if all_sessions_default_connected and all_sessions_dedicated_connected:
                    stop_reason = "All sessions established"
                    break
            if mode == "logout":
                all_sessions_default_disconnected = not default_bearer or sessions_default == 0
                all_sessions_dedicated_disconnected = not dedicated_bearer or sessions_dedicated == 0
                if all_sessions_default_disconnected and all_sessions_dedicated_disconnected:
                    stop_reason = "All sessions disconnected"
                    break

            hit_zero_default = not default_bearer or consecutive_default_rate_zeros >= stop_repeated
            hit_zero_dedicated = not dedicated_bearer or consecutive_dedicated_rate_zeros >= stop_repeated
            if hit_zero_default and hit_zero_dedicated:
                if stop_repeated > 1:
                    stop_reason = "{:s} rate hit zero for {:d} consecutive periods".format(rate_type, stop_repeated)
                else:
                    stop_reason = "{:s} rate hit zero".format(rate_type)
                break

            sessions_not_changing_default = not default_bearer or consecutive_sessions_default_unchanged >= stop_repeated
            sessions_not_changing_dedicated = not dedicated_bearer or consecutive_sessions_dedicated_unchanged >= stop_repeated
            if sessions_not_changing_default and sessions_not_changing_dedicated:
                if stop_repeated > 1:
                    stop_reason = "Sessions unchanged between intervals"
                else:
                    stop_reason = "Sessions unchanged for {:d} consecutive periods".format(stop_repeated)
                break
        else:
            if time.time() - start_time > stop_timeout:
                stop_reason = "Sessions were never established, timeout after {:d} seconds".format(stop_timeout)
                break
        time.sleep(15)
    t.log("Finished mobile_calculate_tester_stats collection because: {:s}".format(stop_reason))

    # Store data in a plotly graph
    data = []
    if default_bearer:
        trace_rates = plotly.graph_objs.Scatter(
            x=timestamps,
            y=default_rates,
            mode="lines+markers",
            name="Actual {:s} Rate (Sessions/Second)".format(rate_type),
        )
        trace_sessions = plotly.graph_objs.Scatter(
            x=timestamps,
            y=sessions_established_default,
            mode="lines+markers",
            name="Sessions Established",
        )
        data.append(trace_rates)
        data.append(trace_sessions)
    if dedicated_bearer:
        trace_rates = plotly.graph_objs.Scatter(
            x=timestamps,
            y=dedicated_rates,
            mode="lines+markers",
            name="Actual Dedicated Bearer Session {:s} Rate (Sessions/Second)".format(rate_type),
        )
        trace_sessions = plotly.graph_objs.Scatter(
            x=timestamps,
            y=sessions_established_dedicated,
            mode="lines+markers",
            name="Dedicated Bearer Sessions Established",
        )
        data.append(trace_rates)
        data.append(trace_sessions)

    plotly.offline.plot(data, filename=graph_filename, auto_open=False)

    if full_graph:
        if mode == "login":
            saved_data = {
                "timestamps": timestamps,
            }
            if default_bearer:
                saved_data["default_rates"] = default_rates
                saved_data["sessions_established_default"] = sessions_established_default
            if dedicated_bearer:
                saved_data["dedicated_rates"] = dedicated_rates
                saved_data["sessions_established_dedicated"] = sessions_established_dedicated
            np.savez("temp_mobile_tester_stats_full.npz", **saved_data)
        if mode == "logout":
            saved_data = np.load("temp_mobile_tester_stats_full.npz")
            os.remove("temp_mobile_tester_stats_full.npz")
            data = []
            if default_bearer:
                login_trace_rates = plotly.graph_objs.Scatter(
                    x=saved_data["timestamps"],
                    y=saved_data["default_rates"],
                    mode="lines+markers",
                    name="Actual Connect Rate (Sessions/Second)",
                )
                login_trace_sessions = plotly.graph_objs.Scatter(
                    x=saved_data["timestamps"],
                    y=saved_data["sessions_established_default"],
                    mode="lines+markers",
                    name="Sessions Established",
                )
                data.append(login_trace_rates)
                data.append(login_trace_sessions)
                logout_trace_rates = plotly.graph_objs.Scatter(
                    x=timestamps,
                    y=default_rates,
                    mode="lines+markers",
                    name="Actual {:s} Rate (Sessions/Second)".format(rate_type),
                )
                logout_trace_sessions = plotly.graph_objs.Scatter(
                    x=timestamps,
                    y=sessions_established_default,
                    mode="lines+markers",
                    name="Sessions Established",
                )
                data.append(logout_trace_rates)
                data.append(logout_trace_sessions)
            if dedicated_bearer:
                login_trace_rates = plotly.graph_objs.Scatter(
                    x=saved_data["timestamps"],
                    y=saved_data["dedicated_rates"],
                    mode="lines+markers",
                    name="Actual Dedicated Bearer Session Connect Rate (Sessions/Second)",
                )
                login_trace_sessions = plotly.graph_objs.Scatter(
                    x=saved_data["timestamps"],
                    y=saved_data["sessions_established_dedicated"],
                    mode="lines+markers",
                    name="Dedicated Bearer Sessions Established",
                )
                data.append(login_trace_rates)
                data.append(login_trace_sessions)
                logout_trace_rates = plotly.graph_objs.Scatter(
                    x=timestamps,
                    y=dedicated_rates,
                    mode="lines+markers",
                    name="Actual {:s} Rate (Sessions/Second)".format(rate_type),
                )
                logout_trace_sessions = plotly.graph_objs.Scatter(
                    x=timestamps,
                    y=sessions_established_dedicated,
                    mode="lines+markers",
                    name="Sessions Established",
                )
                data.append(logout_trace_rates)
                data.append(logout_trace_sessions)
            plotly.offline.plot(data, filename=full_graph_filename, auto_open=False)

    # Trim leading and trailing zeros because otherwise min/max makes no sense
    default_rates_for_stats = np.trim_zeros(np.array(default_rates))
    if default_rates_for_stats.size == 0:
        default_rates_for_stats = np.array([0.0])
    dedicated_rates_for_stats = np.trim_zeros(np.array(dedicated_rates))
    if dedicated_rates_for_stats.size == 0:
        dedicated_rates_for_stats = np.array([0.0])

    result = {}
    rate_type = rate_type.lower()
    if default_bearer:
        result["default_bearer"] = {
            "reported_rate": reported_default_rate,
            "actual_{:s}_rates_timestamps".format(rate_type): timestamps,
            "actual_{:s}_rates".format(rate_type): default_rates,
            "average_{:s}_rate".format(rate_type): np.mean(default_rates_for_stats),
            "maximum_{:s}_rate".format(rate_type): np.max(default_rates_for_stats),
            "minimum_{:s}_rate".format(rate_type): np.min(default_rates_for_stats),
            "median_{:s}_rate".format(rate_type): np.median(default_rates_for_stats),
            "standard_deviation_rate": np.std(default_rates_for_stats),
        }
    if dedicated_bearer:
        result["dedicated_bearer"] = {
            "reported_rate": reported_dedicated_rate,
            "actual_{:s}_rates_timestamps".format(rate_type): timestamps,
            "actual_{:s}_rates".format(rate_type): dedicated_rates,
            "average_{:s}_rate".format(rate_type): np.mean(dedicated_rates_for_stats),
            "maximum_{:s}_rate".format(rate_type): np.max(dedicated_rates_for_stats),
            "minimum_{:s}_rate".format(rate_type): np.min(dedicated_rates_for_stats),
            "median_{:s}_rate".format(rate_type): np.median(dedicated_rates_for_stats),
            "standard_deviation_rate": np.std(dedicated_rates_for_stats),
        }
    t.log(result)

def mobile_pause_sgi_traffic(cups_test_handle, **kwargs):
    """
    This API is used to pause data traffic,
    Traffic can be paused for a specific DMF or a list of DMF by
    passing dmfList else all the DMFs will be paused
    Mandatory Params:
    :param cups_test_handle:    CUPSSubscribers or PGWSubscribers handle
    return:
    result
    """
    t.log("inside mobile_pause_sgi_traffic")
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle
    rt_device = subs.rt_device_id
    tester = t.get_handle(rt_device)
    if tester.os.lower() == 'spirent':
        kwargs['testSessionHandle'] = subs.test_session_handle
        kwargs['action'] = 'Pause'
        kwargs['tsName'] = subs.tsname
        kwargs['testCaseName'] = subs.nodal_test_case_name
        if 'dmfList' not in kwargs:
            kwargs['useAllDmf'] = 1
        else:
            kwargs['dmfList'] = kwargs['dmfList']
        tester.invoke('dmf_control', **kwargs)


def mobile_resume_sgi_traffic(cups_test_handle, **kwargs):
    """
    This API is used to resume data traffic,
    Traffic can be resumed for a specific DMF or a list of DMF by
    passing dmfList else all the DMFs will be resumed
    Mandatory Params:
    :param cups_test_handle:    CUPSSubscribers or PGWSubscribers handle
    return:
    result

    """
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle
    t.log("inside mobile_resume_sgi_traffic")

    rt_device = subs.rt_device_id
    tester = t.get_handle(rt_device)
    if tester.os.lower() == 'spirent':
        kwargs['testSessionHandle'] = subs.test_session_handle
        kwargs['action'] = 'Resume'
        kwargs['tsName'] = subs.tsname
        kwargs['testCaseName'] = subs.nodal_test_case_name
        if 'dmfList' not in kwargs:
            kwargs['useAllDmf'] = 1
        else:
            kwargs['dmfList'] = kwargs['dmfList']
        tester.invoke('dmf_control', **kwargs)


def mobile_configure_bearers(cups_test_handle, sdf_dict, default_bearers, dedicated_bearers, **kwargs):
    """
    Method for re-configuring certain default and dedicated bearer parameters while Test Session is not active.

    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param sdf_dict: a dictionary whose keys represent distinct bearers (B0, B1, etc). The values are lists containing
        SDF/TFT(s). The number of keys in sdf_dict must match the number of configured dedicated bearers.See below for
        examples of the data structures in use.
    :param default_bearers: Desired number of default bearers. Almost always 1. This overwrites the value configured
    in your BBE CFG YAML.
    :param dedicated_bearers: Desired number of dedicated bearers. This overwrites the value configured in your BBE
    CFG YAML.
    :param kwargs:
    downlink_ambr: Aggregate maximum bit rate for default bearer in kbps (downlink)
    uplink_ambr: Aggregate maximum bit rate for default bearer in kbps (downlink)
    ue_init_dedicated_bearer: Set true if you want UE to login with just default bearer on initial attach. Set false
        if you want UE to login with default + all configured dedicated bearers. Default is true.
    enable_qci_to_dscp_mapping: Enables upstream QCI to DSCP marking of packets. Options are true/false.
        Default is false.
    bearer_qci_list: A list of integers 1-9 indicating QCI value for each bearer. This is a required parameter
        when sdf_dict contains SDF QoS parameters. Default bearer always has QCI of 9.
    :return:
    True if tester successfully invokes command to configure TFT sets AND configuration validated/saved.
    Exception raised otherwise

     // Defining individual SDFs
    sdf1 = mobile_create_tft_dict(protocol='17', src_port_start='2002', src_port_end='2002', dst_port_start='2003',
                              dst_port_end='2003')
    sdf2 = mobile_create_tft_dict(protocol='6', src_port_start='3000', src_port_end='3000', dst_port_start='3001',
                              dst_port_end='3001')
    sdf3 = mobile_create_tft_dict(protocol='123', precedence='250')

    // Aggregate into dictionary where many SDFs can be associated with a bearer, then into a set
    // if default-bearer-sdf == true, B0 is default bearer and B1 is my dedicated
    sdf_dict = {'B0': [sdf1, sdf2], 'B1': [sdf3]}
    """
    t.log("inside mobile_configure_bearers")
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle

    testcase_type = '';
    if subs.subscribers_type == 'cups':
        testcase_type = 'sgw';
    elif subs.subscribers_type == 'pgw':
        testcase_type = 'pgw';
    tester_handle = t.get_handle(resource=subs.rt_device_id)

    subs.bearer_per_session = int(default_bearers)
    subs.dedicated_bearers = int(dedicated_bearers)

    if 'spirent' in tester_handle.os.lower():

        # SGW Nodal/Node parameters
        tft_settings = {}
        sdf_settings = {}
        nodal_args = {}
        node_args = {}
        # Set number of bearers and whether UE initiates
        nodal_args['DedicatedsPerDefaultBearer'] = subs.dedicated_bearers
        node_args['DedicatedsPerDefaultBearer'] = subs.dedicated_bearers
        nodal_args['DefaultBearers'] = subs.bearer_per_session
        node_args['DefaultBearers'] = subs.bearer_per_session
        nodal_args['UeInitBearerEn'] = kwargs.get('ue_init_dedicated_bearer', 'true')
        node_args['UeInitBearerEn'] = kwargs.get('ue_init_dedicated_bearer', 'true')

        # Enable SDF on default bearer if user says to
        node_args['TrafficSupportTftDefaultBearer'] = kwargs.get('default_bearer_sdf', 'false').lower()
        if node_args['TrafficSupportTftDefaultBearer'].lower() is not 'false':
            # Set delay of TFT creation for all default bearers to 0 seconds
            for count in range(0, subs.bearer_per_session):
                node_args['TrafficTftCreationDelayTime' + str(count)] = '0'

        # Check QCI to DSCP marking parameter
        node_args['QciToDscpMarkingsEn'] = kwargs.get('enable_qci_to_dscp_mapping', 'false')

        # Set false to override LS default. Detection of SDF QoS later shall override if needed
        node_args['TrafficSupportSdfLevelQos'] = 'false'

        # AMBR settings for non-GBR bearer
        if 'downlink_ambr' in kwargs:
            nodal_args['Gtp2AmbrDownlink'] = kwargs['downlink_ambr']
            node_args['Gtp2AmbrDownlink'] = kwargs['downlink_ambr']
        if 'uplink_ambr' in kwargs:
            nodal_args['Gtp2AmbrUplink'] = kwargs['uplink_ambr']
            node_args['Gtp2AmbrUplink'] = kwargs['uplink_ambr']

        # Bearer QCI settings
        if 'bearer_qci_list' in kwargs:
            total_bearers = int(dedicated_bearers) + int(default_bearers)
            if total_bearers <= 1:
                # Only default bearer, therefore Gtp2QosDetail is "Summary"
                node_args['Gtp2QosDetail'] = 'Summary'
                nodal_args['Gtp2QosDetail'] = 'Summary'
            else:
                # Default bearer + some amount of dedicated bearers
                node_args['Gtp2QosDetail'] = 'Individual'
                nodal_args['Gtp2QosDetail'] = 'Individual'
            for count in range(0, total_bearers):
                node_args['Gtp2QosClassId_' + str(count + 1)] = \
                    kwargs['bearer_qci_list'][count]
                nodal_args['Gtp2QosClassId_' + str(count + 1)] = \
                    kwargs['bearer_qci_list'][count]

        # bearer_counter = 0
        for bearer_id in sorted(sdf_dict.keys()):
            tft_settings[bearer_id] = []
            sdf_settings[bearer_id] = []
            bearer_sdf_counter = 0
            # bearer_counter += 1
            for sdf in sdf_dict[bearer_id]:
                # Convert direction from human-readable to ls.py's index system
                if 'bidirectional' in sdf['direction'].lower():
                    sdf['direction'] = '3'
                elif 'uplink' in sdf['direction'].lower():
                    sdf['direction'] = '2'
                elif 'downlink' in sdf['direction'].lower():
                    sdf['direction'] = '1'
                elif 'pre-rel7' in sdf['direction'].lower():
                    sdf['direction'] = '0'

                # Check if SDF has QoS attributes included. If all present, define new SDF
                if all(sdf_qos in sdf for sdf_qos in ['sdf-index', 'uplink-mbr', 'downlink-mbr', 'uplink-gate-status',
                                                      'downlink-gate-status']):

                    # Raise Exception if bearer_qci_list is undefined
                    if 'bearer_qci_list' not in kwargs:
                        raise Exception("bearer_qci_list is a required argument when SDF QoS parameters are"
                                        "specified in sdf_dict entry!\n")

                    ls_sdf_format = [sdf['uplink-mbr'], sdf['downlink-mbr'], sdf['uplink-gbr'], sdf['downlink-gbr'],
                                    sdf['uplink-gate-status'], sdf['downlink-gate-status'], sdf['precedence']]
                    sdf_settings[bearer_id].append(ls_sdf_format)
                    bearer_sdf_counter += 1
                    node_args['TrafficSupportSdfLevelQos'] = 'true'

                ls_tft_format = [sdf['precedence'], sdf['protocol-number'], '{}', sdf['start-port-remote'],
                                 sdf['end-port-remote'], sdf['remote-address'], sdf['start-port-local'],
                                 sdf['end-port-local'], sdf['tos'], '{}', sdf['security-parameter-index'],
                                 sdf['flow-label'], '{}', '{}', sdf['direction'], '{}', '{}', '{}', '{}',
                                 sdf.get('sdf-index', '{}')]
                tft_settings[bearer_id].append(ls_tft_format)

        node_args['tftSettings'] = tft_settings
        node_args['sdfSettings'] = sdf_settings

        # Remove default bearer TFT settings from nodal, since it knows nothing about default bearer TFT
        if 'default_bearer_sdf' in kwargs:
            if kwargs['default_bearer_sdf'].lower() == 'true':
                node_args['TrafficSupportTftDefaultBearer'] = 'true'
                sorted_bearer_ids = sorted(tft_settings.keys())
                adjusted_nodal_tft = dict(tft_settings)
                adjusted_nodal_tft.pop(sorted_bearer_ids[0])  # Default bearer is lowest alphanumeric key
                nodal_args['tftSettings'] = adjusted_nodal_tft
                subs.tft_settings = adjusted_nodal_tft
            else:
                nodal_args['tftSettings'] = tft_settings
                subs.tft_settings = tft_settings
        else:
            nodal_args['tftSettings'] = tft_settings
            subs.tft_settings = tft_settings

        # Attempt to modify and validate SGW Nodal
        tester_handle.invoke(testcase_type + '_nodal_testcase', mode='modify', testCaseHandle=subs.nodal_testcase_handle,
                             **nodal_args)
        validationstatus = tester_handle.invoke('validate_test_configuration',
                                                testSessionHandle=subs.test_session_handle)
        t.log("Validation Status: {}".format(validationstatus))
        tester_handle.invoke('save_config', instance=subs.nodal_testcase_handle, overwrite='1')
        tester_handle.invoke('save_config', instance=subs.test_session_handle, overwrite='1')

        # Modify, validate, and save SGW Node
        tester_handle.invoke(testcase_type + '_node_testcase', mode='modify', testCaseHandle=subs.node_testcase_handle,
                             **node_args)
        validationstatus = tester_handle.invoke('validate_test_configuration',
                                                testSessionHandle=subs.test_session_handle)
        t.log("Validation Status: {}".format(validationstatus))
        tester_handle.invoke('save_config', instance=subs.node_testcase_handle, overwrite='1')
        tester_handle.invoke('save_config', instance=subs.test_session_handle, overwrite='1')

    else:
        raise Exception("ERROR: Keyword presently only supported for Spirent Landslide!\n")

    return True


def mobile_configure_modification_tft_sets(cups_test_handle, sdf_dict, **kwargs):
    """
    Configures the Landslide TFT sets which can be added/updated/removed from a target dedicated bearer
    via mobile_modify_bearer(). This keyword requires Command Mode.

    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param sdf_dict: a dictionary whose keys represent modification sets, whose values are dictionaries. This
                    dictionary's keys refer to dedicated bearers. The values associated with the bearers are lists
                    containing the SDF/TFT(s)

                    sdf_dict['set1']['B1] =

                    {'direction': 'bidirectional', 'precedence': '254', 'protocol-number': '17',
                    'remote-address': '23.0.0.1/24', 'start-port-local': '3002', 'end-port-local': '3003',
                    'start-port-remote': '4002', 'end-port-remote': '4003', 'tos': '32',
                    'security-parameter-index': '200', 'flow-label': 'flow123'}
    :param kwargs
    :return:
    True if tester successfully invokes command to configure TFT sets AND configuration validated/saved.
    Exception raised otherwise


    // Defining individual SDFs
    sdf1 = {'direction': 'uplink', 'precedence': '255', 'protocol-number': '17', 'remote-address': '23.0.0.1/24',
            'start-port-local': '2002', 'end-port-local': '2003', 'start-port-remote': '1002',
            'end-port-remote': '1003', 'tos': '16', 'security-parameter-index': '100', 'flow-label': 'flow123'}

    sdf2 = {'direction': 'downlink', 'precedence': '254', 'protocol-number': '17', 'remote-address': '23.0.0.1/24',
            'start-port-local': '2002', 'end-port-local': '2003', 'start-port-remote': '1002',
            'end-port-remote': '1003', 'tos': '16', 'security-parameter-index': '100', 'flow-label': 'flow123'}

    sdf3 = {'direction': 'bidirectional', 'precedence': '254', 'protocol-number': '17', 'remote-address': '23.0.0.1/24',
            'start-port-local': '3002', 'end-port-local': '3003', 'start-port-remote': '4002',
            'end-port-remote': '4003', 'tos': '32', 'security-parameter-index': '200', 'flow-label': 'flow123'}

    // Aggregate into dictionary where many SDFs can be associated with a dedicated bearer, then into a set
    sdf_dict = {'B0': [sdf1, sdf2], 'B1': [sdf3]}
    tft_sets['S1'] = sdf_dict
    tft_sets['S2'] = ...

    """
    t.log("inside mobile_configure_modification_tft_sets")
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle

    testcase_type = '';
    if subs.subscribers_type == 'cups':
        testcase_type = 'sgw';
    elif subs.subscribers_type == 'pgw':
        testcase_type = 'pgw';
    tester_handle = t.get_handle(resource=subs.rt_device_id)

    if 'spirent' in tester_handle.os.lower():
        if 'Command Mode' not in subs.test_activity:
            raise Exception("ERROR: Keyword only supported for CUPSSubscribers in Command Mode!\n")

        # Init arguments for programming Landslide
        tft_args = {}
        tft_settings = {}

        # Required args
        tft_args['TestActivity'] = subs.test_activity
        tft_args['DedicatedsPerDefaultBearer'] = subs.dedicated_bearers
        tft_args['DefaultBearers'] = subs.bearer_per_session
        tft_args['tftSettings'] = subs.tft_settings
        # Parse TFT sets
        for set_id in sdf_dict.keys():
            tft_settings[set_id] = {}

            for bearer_id in sdf_dict[set_id].keys():
                tft_settings[set_id][bearer_id] = []

                for sdf in sdf_dict[set_id][bearer_id]:
                    # Convert direction from human-readable to ls.py's index system
                    if 'bidirectional' in sdf['direction'].lower():
                        sdf['direction'] = '3'
                    elif 'uplink' in sdf['direction'].lower():
                        sdf['direction'] = '2'
                    elif 'downlink' in sdf['direction'].lower():
                        sdf['direction'] = '1'
                    elif 'pre-rel7' in sdf['direction'].lower():
                        sdf['direction'] = '0'

                    ls_tft_format = [sdf['precedence'], sdf['protocol-number'], '{}', sdf['start-port-remote'],
                                     sdf['end-port-remote'], sdf['remote-address'], sdf['start-port-local'],
                                     sdf['end-port-local'], sdf['tos'], '{}', sdf['security-parameter-index'],
                                     sdf['flow-label'], '{}', 'true', sdf['direction']]
                    tft_settings[set_id][bearer_id].append(ls_tft_format)

        tft_args['modifiedTftSettings'] = tft_settings
        tft_args['Gtp2BearerModEn'] = 'true'

        tester_handle.invoke(testcase_type + '_nodal_testcase', mode='modify', testCaseHandle=subs.nodal_testcase_handle,
                             **tft_args)
        validationstatus = tester_handle.invoke('validate_test_configuration',
                                                testSessionHandle=subs.test_session_handle)
        t.log("Validation Status: {}".format(validationstatus))
        tester_handle.invoke('save_config', instance=subs.nodal_testcase_handle, overwrite='1')
        tester_handle.invoke('save_config', instance=subs.test_session_handle, overwrite='1')

    else:
        raise Exception("ERROR: Keyword presently only supported for Spirent Landslide!\n")

    return True

def mobile_configure_dhcp_ue(cups_test_handle, mac_address, **kwargs):
    """
    Configures Landslide UE DHCP settings. Currently only supports IPv4
    :param cups_test_handle: CUPSSubscribers handle. DOES NOT SUPPORT PGWSubscribers
    :param mac_address:     Nodal -> Test Configuration -> Mobile Subscribers -> MAC Address (required)
    :param kwargs:
    client_id:              Nodal -> DHCP -> Client ID
    lease_time_request:     Nodal -> DHCP -> Include Lease Time Request
    enterprise_number:      Nodal -> DHCP -> Enterprise Number (V6 Only)
    rapid_commit:           Nodal -> DHCP -> Include Rapid Commit (V6 Only)
    enable_broadcast:       Nodal -> DHCP -> Enable Broadcast ("true"/"false")
    parameter_request_list: Nodal -> DHCP -> Parameter Request List (list of integers)
    host_name:              Nodal -> DHCP -> Host Name
    vendor_class_id:        Nodal -> DHCP -> Vendor Class ID
    retries:                Nodal -> DHCP -> Retries
    v4_offer_message:       Nodal -> DHCP -> V4 Offer Message/V6 Advertise Message (interval in seconds)
    v4_ack_message:         Nodal -> DHCP -> V4 Ack Message/V6 Reply Message (interval in seconds)
    ia_option:              Nodal -> DHCP -> DHCP IA Option Type (set to "IA_TA", "IA_NA", or "IA_PD")
    interface_tag:          access/control/uplink are supported tags. Determines which base address network from your
                            YAML to generate the DHCP Relay Agent Node IP. Default is control network
    vlan_id:                Node -> Network Devices -> DHCP Relay Agent Node -> Advanced -> Vlan ID
    next_hop_ip_address:    Node -> Network Devices -> DHCP Relay Agent Node -> Next Hop IP Address
    server_port:            Node -> DHCP -> Relay Agent Settings -> Server Port
    circuit_id:             Node -> DHCP -> Relay Agent Settings -> Circuit ID
    lease_query_type:       Node -> DHCP -> Relay Agent Settings -> Query Type
                            Can be "ip_addr", "mac_addr" or "cli_id"
    :return
    True if tester successfully invokes command to configure TFT sets AND configuration validated/saved.
    Exception raised otherwise
    """
    t.log("inside mobile_configure_dhcp_ue")
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle
    if subs.subscribers_type == 'pgw':
        raise Exception("mobile_configure_dhcp_ue does not support PGWSubscribers handles")
    tester_handle = t.get_handle(resource=subs.rt_device_id)

    if 'spirent' in tester_handle.os.lower():
        nodal_args = {}
        node_args = {}

        nodal_args["UeDhcpV4En"] = "true"
        nodal_args["MacAddr"] = mac_address
        # DHCP Tab
        if "client_id" in kwargs:
            nodal_args["DhcpCliId"] = str(kwargs.get("client_id"))
        if "lease_time_request" in kwargs:
            nodal_args["DhcpLeaseTimeEn"] = "true"
            nodal_args["DhcpLeaseTime"] = str(kwargs.get("lease_time_request"))
        if "enterprise_number" in kwargs:
            # Only for use in in DHCPv6
            nodal_args["DhcpEnterprise"] = str(kwargs.get("enterprise_number"))
        if "rapid_commit" in kwargs:
            # Only for use in in DHCPv6
            nodal_args["DhcpRapidEn"] = str(kwargs.get("rapid_commit")).lower()
        if "enable_broadcast" in kwargs:
            nodal_args["DhcpBroadcastEn"] = str(kwargs.get("enable_broadcast")).lower()
        if "parameter_request_list" in kwargs:
            # Landslide wants comma-separated integers
            nodal_args["DhcpReqParmsEn"] = "true"
            parameter_request_list = kwargs.get("parameter_request_list")
            parameter_request_list = [str(param) for param in parameter_request_list]
            parameter_request_list = ",".join(parameter_request_list)
            nodal_args["DhcpReqParms"] = parameter_request_list
        if "host_name" in kwargs:
            nodal_args["DhcpHostNameEn"] = "true"
            nodal_args["DhcpHostName"] = str(kwargs.get("host_name"))
        if "vendor_class_id" in kwargs:
            nodal_args["DhcpVendorClassIdEn"] = "true"
            nodal_args["DhcpVendorClassId"] = str(kwargs.get("vendor_class_id"))
        if "retries" in kwargs:
            nodal_args["DhcpRetries"] = str(kwargs.get("retries"))
        if "v4_offer_message" in kwargs:
            nodal_args["DhcpOfferTime"] = str(kwargs.get("v4_offer_message"))
        if "v4_ack_message" in kwargs:
            nodal_args["DhcpAckTime"] = str(kwargs.get("v4_ack_message"))
        if "ia_option" in kwargs:
            nodal_args["DhcpIaOpt6Type"] = kwargs.get("ia_option").upper()

        node_args["UeDhcpV4En"] = "true"
        # Network Devices Tab -> DHCP Relay Agent Node
        interface_tag = kwargs.get("interface_tag", "control").lower()
        if interface_tag == "control":
            node_args["DhcpRelayNodePhy"] = subs.control_interface
            node_args["DhcpRelayNodeIp"] = str(next(subs.control_ip_generator))
            # DHCP -> Relay Agent Settings
            node_args["DhcpServerAddr"] = str(next(subs.control_ip_generator))
        elif interface_tag == "access":
            node_args["DhcpRelayNodePhy"] = subs.access_interface
            node_args["DhcpRelayNodeIp"] = str(next(subs.access_ip_generator))
            # DHCP -> Relay Agent Settings
            node_args["DhcpServerAddr"] = str(next(subs.access_ip_generator))
        elif interface_tag == "uplink":
            node_args["DhcpRelayNodePhy"] = subs.uplink_interface
            node_args["DhcpRelayNodeIp"] = str(next(subs.uplink_ip_generator))
            # DHCP -> Relay Agent Settings
            node_args["DhcpServerAddr"] = str(next(subs.uplink_ip_generator))
        if "vlan_id" in kwargs:
            node_args["DhcpRelayNodeVlanId"] = str(kwargs.get("vlan_id"))
        if "next_hop_ip_address" in kwargs:
            node_args["DhcpRelayNodeNextHop"] = str(kwargs.get("next_hop_ip_address"))

        # DHCP Tab
        if "server_port" in kwargs:
            node_args["DhcpSvrPort"] = str(kwargs.get("server_port"))
        if "circuit_id" in kwargs:
            node_args["DhcpRelayCircuitId"] = str(kwargs.get("circuit_id"))
        if "lease_query_type" in kwargs:
            node_args["DhcpRelayLeaseQueryEn"] = "true"
            node_args["DhcpRelayLeaseQueryType"] = str(kwargs.get("lease_query_type"))

        # Modify, validate, and save SGW Nodal
        tester_handle.invoke('sgw_nodal_testcase', mode='modify', testCaseHandle=subs.nodal_testcase_handle,
                             **nodal_args)
        validationstatus = tester_handle.invoke('validate_test_configuration',
                                                testSessionHandle=subs.test_session_handle)
        t.log("Validation Status: {}".format(validationstatus))
        tester_handle.invoke('save_config', instance=subs.nodal_testcase_handle, overwrite='1')
        tester_handle.invoke('save_config', instance=subs.test_session_handle, overwrite='1')

        # Modify, validate, and save SGW Node
        tester_handle.invoke('sgw_node_testcase', mode='modify', testCaseHandle=subs.node_testcase_handle,
                             **node_args)
        validationstatus = tester_handle.invoke('validate_test_configuration',
                                                testSessionHandle=subs.test_session_handle)
        t.log("Validation Status: {}".format(validationstatus))
        tester_handle.invoke('save_config', instance=subs.node_testcase_handle, overwrite='1')
        tester_handle.invoke('save_config', instance=subs.test_session_handle, overwrite='1')

    else:
        raise Exception("ERROR: Keyword presently only supported for Spirent Landslide!\n")

    return True

def mobile_control_bearers(cups_test_handle, action='start_dedicated_bearer', group='default', sessions_per_second='100',
                           tft_set='1', **kwargs):
    """Method used to start/stop dedicated bearers, as well as modify which TFT sets and packet filters are associated
    with a dedicated bearer.

    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param action: start_dedicated_bearer/stop_dedicated_bearer/modify_bearer
    :param group: subscriber group specified in YAML. If none defined, all subs in 'default' group
    :param sessions_per_second: Attempted session setup rate
    :param tft_set: String form of integer representing TFT set [range: 1-10]
    :param kwargs:
        tft_operation: create_new_tft/delete_existing_tft/add_filter_to_existing_tft/replace_filter_in_existing_tft
            /delete_filter_in_existing_tft. Only works with action='modify_bearer'
        modification_initiator: Options are UE/HSS/MME.

    :return:
    True if tester successfully invokes on_demand_command
    Raises Exception otherwise
    """
    t.log("inside mobile_control_bearers")
    if isinstance(cups_test_handle, list):
        subs = cups_test_handle[0]
        if len(cups_test_handle) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = cups_test_handle

    tester_handle = t.get_handle(resource=subs.rt_device_id)

    if 'spirent' in tester_handle.os.lower():
        command_mode_action = ''
        tft_opcode = ''

        if 'Command Mode' not in subs.test_activity:
            raise Exception("ERROR: Keyword only supported for CUPSSubscribers in Command Mode!\n")

        if action not in ['start_dedicated_bearer', 'stop_dedicated_bearer', 'modify_bearer']:
            raise Exception("ERROR: Keyword supports actions: start_dedicated_bearer/stop_dedicated_bearer/modify_"
                            "bearer. Please select valid action\n")

        if group not in subs.subscriber_group_indices:
            raise Exception("ERROR: Subscriber group " + group
                            + " is not defined. The following subscriber groups are defined: "
                            + str(subs.subscriber_group_indices))

        if 'tft_operation' in kwargs:
            if kwargs['tft_operation'].lower() not in ['create_new_tft', 'delete_existing_tft',
                                                       'add_filter_to_existing_tft', 'replace_filter_in_existing_tft',
                                                       'delete_filter_in_existing_tft']:
                raise Exception('ERROR: Invalid tft_operation: {}'.format(kwargs['tft_operation']))
            else:
                if 'create_new_tft' in kwargs['tft_operation'].lower():
                    tft_opcode = '1'
                elif 'delete_existing_tft' in kwargs['tft_operation'].lower():
                    tft_opcode = '2'
                elif 'add_filter_to_existing_tft' in kwargs['tft_operation'].lower():
                    tft_opcode = '3'
                elif 'replace_filter_in_existing_tft' in kwargs['tft_operation'].lower():
                    tft_opcode = '4'
                elif 'delete_filter_in_existing_tft' in kwargs['tft_operation'].lower():
                    tft_opcode = '5'

        if not subs.isactive:
            raise Exception("Sx Session must be active in order to control bearers.")

        command_for_session_state = 'ls::get ' + subs.test_session_handle + ' -TestStateOrStep'
        returnvalue = tester_handle.invoke('invoke', cmd=command_for_session_state)
        if 'waiting' not in returnvalue.lower():
            raise Exception("Sx Session not properly running. Cannot execute requested mobile_control_bearer action\n.")

        if 'modification_initiator' not in kwargs:
            kwargs['modification_initiator'] = 'UE'

        group_index = subs.subscriber_group_indices[group]
        if 'start' in action:
            command_mode_action = 'ControlBearer {\"op=StartDedicated\" \"rate=' + str(sessions_per_second) \
                          + '\" \"start_sub=' + str(group_index[0]) + '\" \"end_sub=' + str(group_index[1])  \
                          + '\" \"start_def=1\" \"end_def=' + str(subs.bearer_per_session) + '\" ' \
                          + '\"start_ded=1\" \"end_ded=' + str(subs.dedicated_bearers) + '\"}'
        elif 'stop' in action:
            command_mode_action = 'ControlBearer {\"op=StopDedicated\" \"rate=' + str(sessions_per_second) \
                          + '\" \"start_sub=' + str(group_index[0]) + '\" \"end_sub=' + str(group_index[1])  \
                          + '\" \"start_def=1\" \"end_def=' + str(subs.bearer_per_session) + '\" ' \
                          + '\"start_ded=1\" \"end_ded=' + str(subs.dedicated_bearers) + '\"}'
        elif 'modify' in action:
            if 'UE' in kwargs['modification_initiator']:
                command_mode_action = 'ControlBearer {\"op=ModifyBearer\" \"rate=' + str(sessions_per_second) \
                              + '\" \"start_sub=' + str(group_index[0]) + '\" \"end_sub=' + str(group_index[1]) \
                              + '\" \"mod_init=' + str(kwargs['modification_initiator']) + '\" \"mod_set=' \
                              + str(tft_set) + '\" \"def=' + str(subs.bearer_per_session) + '\" \"ded=' \
                              + str(subs.dedicated_bearers) + '\" \"tft_op=' + str(tft_opcode) + '\"}'
            else:
                command_mode_action = 'ControlBearer {\"op=ModifyBearer\" \"rate=' + str(sessions_per_second) \
                              + '\" \"start_sub=' + str(group_index[0]) + '\" \"end_sub=' + str(group_index[1]) \
                              + '\" \"mod_init=' + str(kwargs['modification_initiator']) + '\" \"mod_set=' \
                              + str(tft_set) + '\" \"def=' + str(subs.bearer_per_session) + '\" }'

        t.log('Attempted command mode: {}\n'.format(command_mode_action))
        tester_handle.invoke('on_demand_command', testSessionHandle=subs.test_session_handle,
                             tsName=subs.tsname, testCaseName=subs.nodal_test_case_name,
                             actionCommand=command_mode_action)
    else:
        raise Exception("ERROR: Keyword presently only supported for Spirent Landslide!\n")
    return True


def mobile_verify_traffic(cups_test_handle, minimum_rx_percentage=97, verify_by='throughput',
                          client_expected_rate=0, server_expected_rate=0, client_packet_count=-1,
                          server_packet_count=-1, error_tolerance=1, dmf='all', packet_loss_server=1,
                          packet_loss_client=1):
    """
    This method enables verifications of traffic stats via the router tester. DMF specific stat verification will only
    work if all DMF names are equal.
    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param minimum_rx_percentage: Minimum allowed throughput in %.
    :param verify_by: Defines the verification type. The following types are supported: throughput, rate, packetcount, packetloss
    Throughput: % of packets received relative to packets sent from source
    Rate: mbps of traffic received
    packetcount: total received packets in Landslide test session.
    :param client_expected_rate: mbps expected to be received by client
    :param server_expected_rate: mbps expected to be received by server
    :param client_packet_count: packets expected to be received by client
    :param server_packet_count: packets expected to be received by server
    :param error_tolerance: error tolerance for client and server rate
    :param dmf: Number of DMF to be verified. No input verifies aggregated traffic
    :param packet_loss_server: Number of maximum expected lost Server packets.
    :param packet_loss_client: Number of maximum expected lost Client packets.
    :return: returns dictionary of the stats relevant for the verification
    """
    # Retrieve aggregated stats
    results = mobile_get_stats_results(cups_test_handle)
    # Retrieve DMF specific stats
    if dmf != 'all':
        dmf_list = cups_test_handle.dmf_handle.keys()
        dmf_nmb = str(len(dmf_list)-1)
        for key in cups_test_handle.dmf_handle.keys():
            if dmf_nmb == key[-len(dmf_nmb):]:
                dmf = key[:-len(dmf_nmb)] + dmf
                break
        if dmf in results:
            results = results[dmf]
        else:
            raise Exception('error: DMF name does not exist.')
    # Verify throughput (throughput = Received/Sent)
    if verify_by == 'throughput':
        uplink_throughput_percentage = 0
        downlink_throughput_percentage = 0
        client_sent_packets = float(results['perIntervalStats']['L3 Client']['Total Packets Sent/Sec  (P-I)'].replace(',', ''))
        t.log('info', 'L3 Client sent packets: {0}%'.format(client_sent_packets))
        server_sent_packets = float(results['perIntervalStats']['L3 Server']['Total Packets Sent/Sec  (P-I)'].replace(',', ''))
        t.log('info', 'L3 Server sent packets: {0}%'.format(server_sent_packets))
        client_received_packets = float(results['perIntervalStats']['L3 Client']['Total Packets Received/Sec  (P-I)'].replace(',', ''))
        t.log('info', 'L3 Client received packets: {0}%'.format(client_received_packets))
        server_received_packets = float(results['perIntervalStats']['L3 Server']['Total Packets Received/Sec  (P-I)'].replace(',', ''))
        t.log('info', 'L3 Server received packets: {0}%'.format(server_received_packets))
        if int(client_sent_packets) != 0:
            uplink_throughput_percentage = (float(server_received_packets) / float(client_sent_packets)) * 100
        else:
            t.log('info', 'No client traffic sent')
        if int(server_sent_packets) != 0:
            downlink_throughput_percentage = (float(client_received_packets) / float(server_sent_packets)) * 100
        else:
            t.log('info', 'No server traffic sent')

        if uplink_throughput_percentage < int(minimum_rx_percentage):
            t.log('Observed aggregate uplink throughput of {0}% is less than minimum allowable '
                  'percentage of {1}%!'.format(uplink_throughput_percentage, minimum_rx_percentage))
            raise Exception('Observed aggregate uplink throughput of {0}% is less than minimum allowable '
                            'percentage of {1}%!'.format(uplink_throughput_percentage, minimum_rx_percentage))
        if downlink_throughput_percentage < int(minimum_rx_percentage):
            t.log('Observed aggregate downlink throughput of {0}% is less than minimum allowable '
                  'percentage of {1}%!'.format(downlink_throughput_percentage, minimum_rx_percentage))
            raise Exception('Observed aggregate downlink throughput of {0}% is less than minimum allowable '
                            'percentage of {1}%!'.format(downlink_throughput_percentage, minimum_rx_percentage))
        else:
            t.log('info', 'Observed aggregate uplink throughput of {0}% and downlink throughput of {1}% is greater '
                          'than or equal to the minimum allowable percentage of {2}%! Aggregate traffic throughput '
                          'verified.'
                  .format(uplink_throughput_percentage, downlink_throughput_percentage, minimum_rx_percentage))
    elif verify_by == 'packetcount':
        client_received_packets = int(results['L3 Client']['Total Packets Received'])
        server_received_packets = int(results['L3 Server']['Total Packets Received'])
        if int(client_packet_count) == int(client_received_packets):
            t.log('info', ' Client received {0} packets. {1} packets expected.'
                  .format(client_received_packets, client_packet_count))
        else:
            raise Exception('{0} packets received at client are not equal to the expected {1} packets'
                            .format(client_received_packets, client_packet_count))
        if int(server_packet_count) == int(server_received_packets):
            t.log('info', ' Server received {0} packets. {1} packets expected.'
                  .format(server_received_packets, server_packet_count))
        else:
            raise Exception('{0} packets received at server are not equal to the expected {1} packets'
                            .format(server_received_packets, server_packet_count))
    elif verify_by == 'packetloss':
        client_received_packets = int(results['L3 Client']['Total Packets Received'])
        server_received_packets = int(results['L3 Server']['Total Packets Received'])
        client_sent_packets = int(results['L3 Client']['Total Packets Sent'])
        server_sent_packets = int(results['L3 Server']['Total Packets Sent'])
        packet_loss_server_m = client_sent_packets - server_received_packets
        packet_loss_client_m = server_sent_packets - client_received_packets
        if int(packet_loss_server_m) < int(packet_loss_server):
            t.log('info', ' Server lost {0} packets. {1} packets lost expected.'
                  .format(packet_loss_server_m, packet_loss_server))
        else:
            raise Exception('Server lost {0} packets. Lost packets are higher then the expected {1} packets.'
                            .format(packet_loss_server_m, packet_loss_server))
        if int(packet_loss_client_m) < int(packet_loss_client):
            t.log('info', ' Client lost {0} packets. {1} packets lost expected.'
                  .format(packet_loss_client_m, packet_loss_client))
        else:
            raise Exception('Client lost {0} packets. Lost packets are higher then the expected {1} packets.'
                            .format(packet_loss_client_m, packet_loss_client))
    elif verify_by == 'total_throughput':
        uplink_throughput_percentage = 0
        downlink_throughput_percentage = 0
        client_received_packets = int(results['L3 Client']['Total Packets Received'])
        server_received_packets = int(results['L3 Server']['Total Packets Received'])
        client_sent_packets = int(results['L3 Client']['Total Packets Sent'])
        server_sent_packets = int(results['L3 Server']['Total Packets Sent'])
        if int(client_sent_packets) != 0:
            uplink_throughput_percentage = (float(server_received_packets) / float(client_sent_packets)) * 100
        else:
            t.log('info', 'No client traffic sent')
        if int(server_sent_packets) != 0:
            downlink_throughput_percentage = (float(client_received_packets) / float(server_sent_packets)) * 100
        else:
            t.log('info', 'No server traffic sent')

        if uplink_throughput_percentage < int(minimum_rx_percentage):
            t.log('Observed aggregate uplink throughput of {0}% is less than minimum allowable '
                  'percentage of {1}%!'.format(uplink_throughput_percentage, minimum_rx_percentage))
            raise Exception('Observed aggregate uplink throughput of {0}% is less than minimum allowable '
                            'percentage of {1}%!'.format(uplink_throughput_percentage, minimum_rx_percentage))
        if downlink_throughput_percentage < int(minimum_rx_percentage):
            t.log('Observed aggregate downlink throughput of {0}% is less than minimum allowable '
                  'percentage of {1}%!'.format(downlink_throughput_percentage, minimum_rx_percentage))
            raise Exception('Observed aggregate downlink throughput of {0}% is less than minimum allowable '
                            'percentage of {1}%!'.format(downlink_throughput_percentage, minimum_rx_percentage))
        else:
            t.log('info', 'Observed aggregate uplink throughput of {0}% and downlink throughput of {1}% is greater '
                          'than or equal to the minimum allowable percentage of {2}%! Aggregate traffic throughput '
                          'verified.'
                  .format(uplink_throughput_percentage, downlink_throughput_percentage, minimum_rx_percentage))
    elif verify_by == 'rate':
        # Calculate rate
        t.log('info', 'Started calculating rate...')
        client_received_bytes = float(results['perIntervalStats']['L3 Client']['Total Bits Received/Sec  (P-I)'].replace(',', ''))
        server_received_bytes = float(results['perIntervalStats']['L3 Server']['Total Bits Received/Sec  (P-I)'].replace(',', ''))
        client_rate = float(client_received_bytes) * 0.000001
        server_rate = float(server_received_bytes) * 0.000001
        client_lower_bound = float(client_expected_rate) - (float(error_tolerance) / 100) * float(
            client_expected_rate)
        client_upper_bound = float(client_expected_rate) + (float(error_tolerance) / 100) * float(
            client_expected_rate)
        server_lower_bound = float(server_expected_rate) - (float(error_tolerance) / 100) * float(
            server_expected_rate)
        server_upper_bound = float(server_expected_rate) + (float(error_tolerance) / 100) * float(
            server_expected_rate)
        if float(client_lower_bound) <= float(client_rate) <= float(client_upper_bound):
            # Measured rate is within bound2
            t.log('info', 'Measured rx client traffic rate of {0}mbps is within +/-{1}% range of {2}mbps!'
                  .format(client_rate, error_tolerance, client_expected_rate))
        else:
            # Measured rate is outside of expected bounds
            raise Exception('Measured rx client traffic rate of {0}mbps is NOT within +/-{1}% range of {2}mbps!'
                            .format(client_rate, error_tolerance, client_expected_rate))
        if float(server_lower_bound) <= float(server_rate) <= float(server_upper_bound):
            # Measured rate is within bounds
            t.log('info', 'Measured rx server traffic rate of {0}mbps is within +/-{1}% range of {2}mbps!'
                  .format(server_rate, error_tolerance, server_expected_rate))
        else:
            # Measured rate is outside of expected bounds
            raise Exception('Measured rx server traffic rate of {0}mbps is NOT within +/-{1}% range of {2}mbps!'
                            .format(server_rate, error_tolerance, server_expected_rate))
    else:
        raise Exception('Verification type is not supported. Supported verification types are: '
                        + 'throughput, packetcount and rate')
    traffic_dict = dict()
    traffic_dict['L3 Client'] = results['L3 Client']
    traffic_dict['L3 Server'] = results['L3 Server']
    return traffic_dict


def mobile_get_packetloss(cups_test_handle, dmf='all'):
    """
    This keyword enables users to retrieve the current server and client packets lost.
    :param cups_test_handle: CUPSSubscribers or PGWSubscribers handle
    :param dmf: Number of DMF to be verified. No input verifies aggregated traffic
    :return: packet_loss_dict dictionary containing 'packet_loss_server' and 'packet_loss_client':
    packet_loss_server: client_sent_packets - server_received_packets
    packet_loss_client: server_sent_packets - client_received_packets
    """
    # Retrieve aggregated stats
    results = mobile_get_stats_results(cups_test_handle)
    # Retrieve DMF specific stats
    if dmf != 'all':
        dmf_list = cups_test_handle.dmf_handle.keys()
        dmf_nmb = str(len(dmf_list)-1)
        for key in cups_test_handle.dmf_handle.keys():
            if dmf_nmb == key[-len(dmf_nmb):]:
                dmf = key[:-len(dmf_nmb)] + dmf
                break
        if dmf in results:
            results = results[dmf]
        else:
            raise Exception('error: DMF name does not exist.')
    client_received_packets = int(results['L3 Client']['Total Packets Received'])
    server_received_packets = int(results['L3 Server']['Total Packets Received'])
    client_sent_packets = int(results['L3 Client']['Total Packets Sent'])
    server_sent_packets = int(results['L3 Server']['Total Packets Sent'])
    packet_loss_dict = dict()
    packet_loss_dict['packet_loss_server'] = client_sent_packets - server_received_packets
    packet_loss_dict['packet_loss_client'] = server_sent_packets - client_received_packets
    return packet_loss_dict


def mobile_create_tft_dict(**kwargs):
    """
    create a sdf dict to be used by bearer method
    :param kwargs:
    precedence:                 1-255, default is 255
    direction:                  uplink/downlink/bidirectional, default is bidirectional
    protocol:                   protocol code number
    remote_address:             address
    src_port_start:             port number
    src_port_end:               port number
    dst_port_start:             port number
    dst_port_end:               port number
    tos:                        tos value
    flow_label:                 label string
    security_parameter_index:   index for security_parameter
    sdf_index:                  SDF index within a given bearer. Start at 1 and increment for each SQF QoS profile on a
                                bearer
    uplink_mbr:                 the uplink maximum bitrate in kbps, i.e '1000'
    uplink_gbr:                 the uplink guaranteed bitrate in kbps  i.e '500'
    uplink_gate_status:         the uplink gate status. '0' is open and '1' is closed
    downlink_mbr:               the downlink maximum bitrate in kbps, i.e. '1000'
    downlink_gbr:               the downlink guaranteed bitrate in kbps, i.e. '500'
    downlink_gate_status:       the downlink gate status. '0' is open and '1' is closed
    urr_name:                   name of the URR rule to assigned to the SDF

    :return:
    """
    t.log("inside mobile_create_tft_dict")
    dict1 = {}
    dict1['precedence'] = kwargs.get('precedence', '255')
    dict1['direction'] = kwargs.get('direction', 'bidirectional')
    dict1['protocol-number'] = kwargs.get('protocol', '{}')
    dict1['remote-address'] = kwargs.get('remote_address', '{}')
    dict1['start-port-local'] = kwargs.get('src_port_start', '{}')
    dict1['end-port-local'] = kwargs.get('src_port_end', '{}')
    dict1['start-port-remote'] = kwargs.get('dst_port_start', '{}')
    dict1['end-port-remote'] = kwargs.get('dst_port_end', '{}')
    dict1['tos'] = kwargs.get('tos', '{}')
    dict1['security-parameter-index'] = kwargs.get('security_parameter_index', '{}')
    dict1['flow-label'] = kwargs.get('flow_label', '{}')
    # Only included in dict for SDF level QoS
    if 'sdf_index' in kwargs:
        dict1['sdf-index'] = kwargs.get('sdf_index')
    # dict1['sdf-index'] = kwargs.get('sdf_index', '{}')
    if 'uplink_mbr' in kwargs:
        dict1['uplink-mbr'] = kwargs.get('uplink_mbr')
    # dict1['uplink-mbr'] = kwargs.get('uplink_mbr', '1')
    if 'uplink_gbr' in kwargs:
        dict1['uplink-gbr'] = kwargs.get('uplink_gbr')
    # dict1['uplink-gbr'] = kwargs.get('uplink_gbr', '1')
    if 'uplink_gate_status' in kwargs:
        dict1['uplink-gate-status'] = kwargs.get('uplink_gate_status')
    # dict1['uplink-gate-status'] = kwargs.get('uplink_gate_status', '0')     # 0 is on. 1 is off
    if 'downlink_mbr' in kwargs:
        dict1['downlink-mbr'] = kwargs.get('downlink_mbr')
    # dict1['downlink-mbr'] = kwargs.get('downlink_mbr', '1')
    if 'downlink_gbr' in kwargs:
        dict1['downlink-gbr'] = kwargs.get('downlink_gbr')
    # dict1['downlink-gbr'] = kwargs.get('downlink_gbr', '1')
    if 'downlink_gate_status' in kwargs:
        dict1['downlink-gate-status'] = kwargs.get('downlink_gate_status')
    # dict1['downlink-gate-status'] = kwargs.get('downlink_gate_status', '0')  # 0 is on. 1 is off
    if 'urr_name' in kwargs:
        dict1['urr-name'] = kwargs.get('urr_name')

    return dict1


def mobile_get_ue_session_info(**kwargs):
    """
    :param kwargs:
    router_id:           router id, default is r0
    return_by_key:       ip or seid
    :return:             a list with ip or seid as value if return_by_key is set, or return a dictionary of ip/seid
    """
    import random
    device_id = kwargs.get('router_id', 'r0')
    router = t.get_handle(device_id)
    result = {}
    result_by_key = []
    resp = router.pyez('get_services_mobile_edge_sessions_information', normalize=True, timeout=600).resp
    for session in resp.findall('session-info'):
        ipaddr = session.findtext('ip-address')
        seid = session.findtext('local-seid')
        if 'return_by_key' in kwargs and 'ip' in kwargs['return_by_key']:
            result_by_key.append(ipaddr)
        elif 'return_by_key' in kwargs and 'seid' in kwargs['return_by_key']:
            result_by_key.append(seid)
        else:
            result[ipaddr] = seid
    if 'by_random' in kwargs:
        result_by_key = random.sample(result_by_key, kwargs['by_random'])
    if 'return_by_key' in kwargs:
        return result_by_key
    else:
        return result


def mobile_configure_lawful_intercept(subscriber, count, port_number, start_time=0, stop_time=120, **kwargs):
    """Configures Lawful Intercept in SGW Nodal test case.

    :param subscriber: CUPSSubscribers or PGWSubscribers handle
    :param count: the number of sessions mirrored
    :param port_number: the specific port to send mirrored traffic on (1-65535)
    :param start_time: when to start lawful intercept (relative to session establishment)
    :param stop_time: when to stop lawful intercept (relative to start_time)
    :param kwargs:
    start_x3u_peer_teid:    Starting TEID-U of the X3U peer
    imsi_increment:         Amount by which you want tapped session starting IMSI to increment
    vlan_id:                VLAN ID for SX3LIF X3U Node
    interface_tag:          access/control/uplink are supported tags. Determines which base address network from your
                            YAML to generate the Sx3lif Node Ip. Default is control network
    :return: the allocated IPv4 address requested by user
    """

    t.log("inside mobile_configure_lawful_intercept")
    node_args = {}
    interface = '';
    testcase_type = '';
    if subscriber.subscribers_type == 'cups':
        interface = 'Sxa';
        testcase_type = 'sgw';
    elif subscriber.subscribers_type == 'pgw':
        interface = 'Sxb';
        testcase_type = 'pgw';
    node_args[interface + 'ControlLiEn'] = 'true'                    # Enable CUPS Lawful Intercept
    node_args[interface + 'ControlSx3lifEn'] = 'true'                # When true, Landslide emulates Sx3LIF Node
    node_args[interface + 'ControlLiStartTime'] = start_time
    node_args[interface + 'ControlLiStopTime'] = stop_time
    node_args['Sx3lifNodeAddrXPort'] = port_number
    node_args[interface + 'ControlX3uPeerTeid'] = kwargs.get('start_x3u_peer_teid', '1000')
    node_args[interface + 'ControlLiImsiStr'] = '#(' + subscriber.node_start_imsi + ' ' + str(count) + '/' \
                                       + str(kwargs.get('imsi_increment', 1)) + ')'
    if kwargs.get('vlan_id') is not None:
        node_args['Sx3lifNodeVlanId'] = kwargs.get('vlan_id')
    if kwargs.get('interface_tag') is not None:
        if 'control' in kwargs.get('interface_tag'):
            node_args['Sx3lifNodePhy'] = subscriber.control_interface
            node_args['Sx3lifNodeIp'] = str(next(subscriber.control_ip_generator))
        elif 'access' in kwargs.get('interface_tag'):
            node_args['Sx3lifNodePhy'] = subscriber.access_interface
            node_args['Sx3lifNodeIp'] = str(next(subscriber.access_ip_generator))
        elif 'uplink' in kwargs.get('interface_tag'):
            node_args['Sx3lifNodePhy'] = subscriber.uplink_interface
            node_args['Sx3lifNodeIp'] = str(next(subscriber.uplink_ip_generator))
    else:
        # Default is control IP network if user does not give tag
        node_args['Sx3lifNodePhy'] = subscriber.control_interface
        node_args['Sx3lifNodeIp'] = str(next(subscriber.control_ip_generator))

    # Modify, validate, and save SGW Node
    tester_handle = t.get_handle(resource=subscriber.rt_device_id)
    tester_handle.invoke(testcase_type + '_node_testcase', mode='modify', testCaseHandle=subscriber.node_testcase_handle,
                         **node_args)
    validationstatus = tester_handle.invoke('validate_test_configuration',
                                            testSessionHandle=subscriber.test_session_handle)
    t.log("Validation Status: {}".format(validationstatus))
    tester_handle.invoke('save_config', instance=subscriber.node_testcase_handle, overwrite='1')
    tester_handle.invoke('save_config', instance=subscriber.test_session_handle, overwrite='1')
    return node_args['Sx3lifNodeIp']


def mobile_create_usage_rule_dict(**kwargs):
    """
    Creates and returns a dictionary defining a usage report rule. This method is meant to be used as helper method
    inside mobile_configure_usage_rules().

    :param kwargs:
    name: the name of the rule
    measurement_methods: a list of measurement methods. Valid options are
        'duration'
        'volume'
        'event'
    reporting_triggers: a list of reporting triggers. Valid options are
        'periodic'
        'start_of_traffic'
        'volume_quota'
        'volume_threshold'
        'stop_of_traffic'
        'time_quota'
        'time_threshold'
        'dropped_dl_traffic_threshold'
        'envelope_closure'
        'quota_holding_time'
        'linked_usage'
        'event_threshold'
    measurement_period: measurement period in seconds (requires 'periodic' trigger)
    time_threshold: time threshold in seconds (requires 'duration' measurement and 'time_threshold' trigger)
    time_quota: time quota in seconds (requires 'duration' measurement and 'time_quota' trigger)
    quota_holding_time: quota hold time in seconds (requires 'duration' measurement and 'quota_holding_time' trigger)
    volume_threshold_total_bytes: volume threshold in bytes (requires 'volume' measurement and 'volume_threshold'
        trigger
    volume_threshold_uplink_bytes: uplink volume threshold in bytes (requires 'volume' measurement and
        'volume_threshold' trigger
    volume_threshold_downlink_bytes: downlink volume threshold in bytes (requires 'volume' measurement and
        'volume_threshold' trigger
    volume_quota_total_bytes: volume quota in bytes (requires 'volume' measurement and 'volume_quota' trigger)
    volume_quota_uplink_bytes: uplink volume quota in bytes (requires 'volume' measurement and 'volume_quota' trigger)
    volume_quota_downlink_bytes: downlink volume quota in bytes (requires 'volume' measurement and 'volume_quota'
        trigger)
    downlink_drop_threshold_packets: downlink drop threshold number of packets (requires 'volume' measurement and
        'dropped_dl_traffic_threshold' trigger
    downlink_drop_threshold_bytes: downlink drop threshold in bytes (requires 'volume' measurement and
        'dropped_dl_traffic_threshold' trigger
    :return: dictionary defining the usage rule
    """

    t.log("inside mobile_create_usage_rule_dict")
    rule = dict()
    if 'name' in kwargs:
        rule['name'] = kwargs['name']
    if 'measurement_methods' in kwargs:
        if isinstance(kwargs['measurement_methods'], list):
            rule['measurement_methods'] = kwargs['measurement_methods']
        else:
            rule['measurement_methods'] = [kwargs['measurement_methods']]
    else:
        raise Exception('No measurement method specified in usage rule dictionary!\n')
    if 'reporting_triggers' in kwargs:
        if isinstance(kwargs['reporting_triggers'], list):
            rule['reporting_triggers'] = kwargs['reporting_triggers']
        else:
            rule['reporting_triggers'] = [kwargs['reporting_triggers']]
    else:
        raise Exception('No reporting triggers specified in usage rule dictionary!\n')
    if 'measurement_period' in kwargs:
        rule['measurement_period'] = kwargs['measurement_period']
    if 'time_threshold' in kwargs and 'duration' in kwargs['measurement_methods']:
        rule['time_threshold'] = kwargs['time_threshold']
    if 'time_quota' in kwargs and 'duration' in kwargs['measurement_methods']:
        rule['time_quota'] = kwargs['time_quota']
    if 'quota_holding_time' in kwargs and 'duration' in kwargs['measurement_methods']:
        rule['quota_holding_time'] = kwargs['quota_holding_time']
    if 'volume_threshold_total_bytes' in kwargs and 'volume' in kwargs['measurement_methods']:
        rule['volume_threshold_total_bytes'] = kwargs['volume_threshold_total_bytes']
    if 'volume_threshold_uplink_bytes' in kwargs and 'volume' in kwargs['measurement_methods']:
        rule['volume_threshold_uplink_bytes'] = kwargs['volume_threshold_uplink_bytes']
    if 'volume_threshold_downlink_bytes' in kwargs and 'volume' in kwargs['measurement_methods']:
        rule['volume_threshold_downlink_bytes'] = kwargs['volume_threshold_downlink_bytes']
    if 'volume_quota_total_bytes' in kwargs and 'volume' in kwargs['measurement_methods']:
        rule['volume_quota_total_bytes'] = kwargs['volume_quota_total_bytes']
    if 'volume_quota_uplink_bytes' in kwargs and 'volume' in kwargs['measurement_methods']:
        rule['volume_quota_uplink_bytes'] = kwargs['volume_quota_uplink_bytes']
    if 'volume_quota_downlink_bytes' in kwargs and 'volume' in kwargs['measurement_methods']:
        rule['volume_quota_downlink_bytes'] = kwargs['volume_quota_downlink_bytes']
    if 'downlink_drop_threshold_packets' in kwargs and 'volume' in kwargs['measurement_methods']:
        rule['downlink_drop_threshold_packets'] = kwargs['downlink_drop_threshold_packets']
    if 'downlink_drop_threshold_bytes' in kwargs and 'volume' in kwargs['measurement_methods']:
        rule['downlink_drop_threshold_bytes'] = kwargs['downlink_drop_threshold_bytes']
    return rule

def mobile_configure_usage_rules(subscriber, rule_list, mode="bearer", **kwargs):
    """
    Configures one (or many) usage reporting rules in Landslide Test Session. Assignment of rules to bearers is 1:1 and
    will be processed in the order presented in rule_list parameter.

    Rules are assigned to bearers in order starting from default bearer. If you have 1 default and 1 dedicated bearer
    and pass a rule_list of size 2, the first rule will be applied to default bearer and second rule applied to
    dedicated.

    :param subscriber: CUPSSubscribers or PGWSubscribers handle
    :param rule_list: a list containing dictionaries which define a usage rule. Cannot exceed number of configured
        bearers, as rule:bearer assignments are 1:1. Example dictionaries:

        r1 = {'name': 'urr1',
         'measurement_methods': ['volume', 'duration', 'event'],
         'reporting_triggers': ['dropped_dl_traffic_threshold'],
         'downlink_drop_threshold_packets': '1500',
         'downlink_drop_threshold_bytes': '1000000'
         }
        r2 = {'name': 'urr2',
         'measurement_methods': ['volume'],
         'reporting_triggers': ['volume_quota', 'volume_threshold'],
         'volume_threshold_uplink_bytes': '5000',
         'volume_threshold_total_bytes': '1000000',
         'volume_threshold_downlink_bytes': '6000',
         'volume_quota_total_bytes': '2000000',
         'volume_quota_uplink_bytes': '11000',
         'volume_quota_downlink_bytes': '50000'
         }

         Can also check documentation of mobile_create_usage_rule_dict() for expected dict format.
    :param mode: either "bearer" (default) or "sdf"
    :param kwargs:
    sdf_dict: a dictionary whose keys represent distinct bearers (B0, B1, etc). The values are lists containing
        SDF/TFT(s). Each sdf within sdf_dict must contain a "urr_name" with the name of the usage report rule assigned.
        The number of keys in sdf_dict must match the number of configured dedicated bearers.See below for
        examples of the data structures in use
         // Defining individual SDFs
        sdf1 = mobile_create_tft_dict(protocol='17', src_port_start='2002', src_port_end='2002', dst_port_start='2003',
                                  dst_port_end='2003', urr_name="urr1")
        sdf2 = mobile_create_tft_dict(protocol='6', src_port_start='3000', src_port_end='3000', dst_port_start='3001',
                                  dst_port_end='3001', urr_name="urr2")
        sdf3 = mobile_create_tft_dict(protocol='123', precedence='250', urr_name="urr1")

        // Aggregate into dictionary where many SDFs can be associated with a bearer, then into a set
        // if default-bearer-sdf == true, B0 is default bearer and B1 is my dedicated
        sdf_dict = {'B0': [sdf1, sdf2], 'B1': [sdf3]}
    :return: True if no exceptions are raised while programming Test Session
    """
    t.log("inside mobile_configure_usage_rules")
    if isinstance(subscriber, list):
        subs = subscriber[0]
        if len(subscriber) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = subscriber

    tester_handle = t.get_handle(resource=subs.rt_device_id)
    mode = mode.lower()
    if mode not in ['bearer', 'sdf']:
        raise Exception('mobile_configure_usage_rules mode must be \"bearer\" or \"sdf\"')
    if mode == 'sdf':
        if 'sdf_dict' in kwargs:
            sdf_dict = kwargs.get('sdf_dict')
        else:
            raise Exception('sdf_dict must be passed in if using sdf mode')
    interface = '';
    testcase_type = '';
    if subs.subscribers_type == 'cups':
        interface = 'Sxa';
        testcase_type = 'sgw';
    elif subs.subscribers_type == 'pgw':
        interface = 'Sxb';
        testcase_type = 'pgw';
    node_args = dict()
    node_args[interface + 'ControlUsageRptRulesEn'] = 'true'
    node_args[interface + 'ControlNumUsageRptRules'] = len(rule_list)        # Number of rules

    for rule_index, item in enumerate(rule_list):
        # Process rule dict
        rule = mobile_create_usage_rule_dict(**item)
        # Rules is 1-indexed rather than 0-indexed
        rule_counter = rule_index + 1

        # Rule name
        if 'name' in rule.keys():
            node_args[interface + 'ControlRuleName_' + str(rule_counter)] = rule['name']
        # Enable measurement methods
        if 'volume' in rule['measurement_methods']:
            node_args[interface + 'ControlUsageRptVolumeEn_' + str(rule_counter)] = 'true'
        if 'duration' in rule['measurement_methods']:
            node_args[interface + 'ControlUsageRptDurationEn_' + str(rule_counter)] = 'true'
        if 'event' in rule['measurement_methods']:
            node_args[interface + 'ControlUsageRptEventEn_' + str(rule_counter)] = 'true'
        # Enable reporting triggers
        if 'periodic' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigPerioEn_' + str(rule_counter)] = 'true'
        if 'start_of_traffic' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigStartEn_' + str(rule_counter)] = 'true'
        if 'volume_quota' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigVolquEn_' + str(rule_counter)] = 'true'
        if 'volume_threshold' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigVolthEn_' + str(rule_counter)] = 'true'
        if 'stop_of_traffic' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigStoptEn_' + str(rule_counter)] = 'true'
        if 'time_threshold' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigTimthEn_' + str(rule_counter)] = 'true'
        if 'time_quota' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigTimquEn_' + str(rule_counter)] = 'true'
        if 'dropped_dl_traffic_threshold' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigDrothEn_' + str(rule_counter)] = 'true'
        if 'envelope_closure' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigEnvclEn_' + str(rule_counter)] = 'true'
        if 'quota_holding_time' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigQuhtiEn_' + str(rule_counter)] = 'true'
        if 'linked_usage' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigLiusaEn_' + str(rule_counter)] = 'true'
        if 'event_threshold' in rule['reporting_triggers']:
            node_args[interface + 'ControlUsageRptTrigEvethEn_' + str(rule_counter)] = 'true'
        # Values associated with triggers/measurements
        if 'volume_threshold_total_bytes' in rule.keys():
            node_args[interface + 'ControlUsageRptVolthTot_' + str(rule_counter)] = rule['volume_threshold_total_bytes']
        if 'volume_threshold_uplink_bytes' in rule.keys():
            node_args[interface + 'ControlUsageRptVolthUl_' + str(rule_counter)] = rule['volume_threshold_uplink_bytes']
        if 'volume_threshold_downlink_bytes' in rule.keys():
            node_args[' SxaControlUsageRptVolthDl_' + str(rule_counter)] = rule['volume_threshold_downlink_bytes']
        if 'volume_quota_total_bytes' in rule.keys():
            node_args[interface + 'ControlUsageRptVolquTot_' + str(rule_counter)] = rule['volume_quota_total_bytes']
        if 'volume_quota_uplink_bytes' in rule.keys():
            node_args[interface + 'ControlUsageRptVolquUl_' + str(rule_counter)] = rule['volume_quota_uplink_bytes']
        if 'volume_quota_downlink_bytes' in rule.keys():
            node_args[interface + 'ControlUsageRptVolquDl_' + str(rule_counter)] = rule['volume_quota_downlink_bytes']
        if 'downlink_drop_threshold_packets' in rule.keys():
            node_args[interface + 'ControlUsageRptDrothPkts_' + str(rule_counter)] = rule['downlink_drop_threshold_packets']
        if 'downlink_drop_threshold_bytes' in rule.keys():
            node_args[interface + 'ControlUsageRptDrothBytes_' + str(rule_counter)] = rule['downlink_drop_threshold_bytes']
        if 'time_threshold' in rule.keys():
            node_args[interface + 'ControlUsageRptTimth_' + str(rule_counter)] = rule['time_threshold']
        if 'time_quota' in rule.keys():
            node_args[interface + 'ControlUsageRptTimqu_' + str(rule_counter)] = rule['time_quota']
        if 'quota_holding_time' in rule.keys():
            node_args[interface + 'ControlUsageRptQuhti_' + str(rule_counter)] = rule['quota_holding_time']
        if 'measurement_period' in rule.keys():
            node_args[interface + 'ControlUsageRptMeasPeriod_' + str(rule_counter)] = rule['measurement_period']

    if mode == 'bearer':
        # Enable per-bearer rule assignment
        node_args[interface + 'ControlUsageRptAssignPerBearerEn'] = 'true'
        node_args[interface + 'ControlUsageRptSdfUrrEn'] = 'false'
        # Rule-to-bearer assignments
        for i in range(len(rule_list)):
            node_args[interface + 'ControlUsageRptAssignBearer_' + str(i+1)] = str(i+1)
    if mode == 'sdf':
        # Enable per-SDF rule assignment
        node_args[interface + 'ControlUsageRptAssignPerBearerEn'] = 'false'
        node_args[interface + 'ControlUsageRptSdfUrrEn'] = 'true'
        # if any('urr-name' not in sdf for sdf_list in sdf_dict.values() for sdf in sdf_list):
        # Check that all sdfs have a urr_name, and that all rules have a name
        for rule in rule_list:
            if 'name' not in rule:
                raise Exception('For SDF, each rule must be named')
        for sdf_list in sdf_dict.values():
            for sdf in sdf_list:
                if 'urr-name' not in sdf:
                    raise Exception('For SDF, sdf_dict items must include the URR name')

        for bearer_index, bearer_id in enumerate(sorted(sdf_dict.keys())):
            for sdf_index, sdf in enumerate(sdf_dict[bearer_id]):
                rule_num = None
                for rule_index, rule in enumerate(rule_list):
                    if rule['name'] == sdf['urr-name']:
                        rule_num = rule_index
                        break
                if rule_num is None:
                    raise Exception('URR name {:s} not found in rule_list'.format(sdf['urr-name']))
                # Rules are 1-indexed rather than 0-indexed
                node_args[interface + 'ControlSdfRule_' + str(bearer_index) + '_' + str(sdf_index)] = str(rule_num + 1)

    # Modify, validate, and save SGW Node
    tester_handle = t.get_handle(resource=subs.rt_device_id)
    tester_handle.invoke(testcase_type + '_node_testcase', mode='modify', testCaseHandle=subs.node_testcase_handle,
                         **node_args)
    validationstatus = tester_handle.invoke('validate_test_configuration',
                                            testSessionHandle=subs.test_session_handle)
    t.log("Validation Status: {}".format(validationstatus))
    tester_handle.invoke('save_config', instance=subs.node_testcase_handle, overwrite='1')
    tester_handle.invoke('save_config', instance=subs.test_session_handle, overwrite='1')

    return True


def mobile_load_custom_pfcp_message(subscriber, file_name, **kwargs):
    """Loads a previously saved custom PFCP message in SGW Node testcase. Assumes username where message is stored
    is 'sms' unless otherwise specified.

    :param subscriber: CUPSSubscribers or PGWSubscribers handle
    :param file_name: name of saved Custom Message Editor file on TAS. Cannot contain spaces. Use another delimiter
        like dash (-) instead.
    :param kwargs:
    username: Landslide username on TAS under which the Custom PFCP Message is saved. Keyword assumes 'sms' if not
        provided by user.
    :return:
    """

    t.log("inside mobile_load_custom_pfcp_message")
    if isinstance(subscriber, list):
        subs = subscriber[0]
        if len(subscriber) > 1:
            # for landslide/cups generally not more than one sub should be passed in list
            t.log('WARN', 'Subscriber handle has multiple entries')
    else:
        subs = subscriber

    testcase_type = '';
    if subs.subscribers_type == 'cups':
        testcase_type = 'sgw';
    elif subs.subscribers_type == 'pgw':
        testcase_type = 'pgw';
    tester_handle = t.get_handle(resource=subs.rt_device_id)
    node_args = dict()
    node_args['PfcpCustomMsgEn'] = 'true'
    node_args['PfcpCustomMsg'] = kwargs.get('username', 'sms') + '/' + str(file_name)

    tester_handle.invoke(testcase_type + '_node_testcase', mode='modify', testCaseHandle=subs.node_testcase_handle,
                         **node_args)
    validationstatus = tester_handle.invoke('validate_test_configuration',
                                            testSessionHandle=subs.test_session_handle)
    t.log("Validation Status: {}".format(validationstatus))
    tester_handle.invoke('save_config', instance=subs.node_testcase_handle, overwrite='1')
    tester_handle.invoke('save_config', instance=subs.test_session_handle, overwrite='1')
    return True
