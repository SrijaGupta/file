"""
The module provide tools for CST tests
"""
import time
from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil
from jnpr.toby.hldcl.device import Device
import datetime
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from xml.dom.minidom import parseString
import re
import os
import random
import math
import difflib
import inspect
import jnpr.toby.engines.verification.verify_utils as verify_utils

def _check_bbe():
    try:
        bbe.bbevar
    except NameError:
        name = inspect.currentframe().f_back.f_code.co_name
        raise Exception("this keyword {} is for BBE only, please use others if not working on BBE feature".format(name))

def check_link_status(rt_device_id='rt0', router='r0'):
    """
    check router and tester link status, it will log ERROR if the link status is not up
    :param
    rt_device_id:                    tester device id, e.g. 'rt0'
    router:                          router id, e.g. 'r0'
    :return:
    """
    t.log("inside check_link_status, checking tester link and router link status...")
    _check_bbe()
    rt_handle = t.get_handle(rt_device_id)
    if t['resources'][rt_device_id]['system']['primary']['make'] == 'ixia':
        result = rt_handle.invoke('test_control', action='check_link_state',
                                  port_handle=rt_handle.session_info['vport_list'])
        if result['status'] != "1":
            raise Exception("some links in rt has problem, please check connections")
    dut1 = t.get_handle(router)
    result = True
    basetime = time.time()
    while True:
        for interface in bbe.get_interfaces(router):
            name = interface.interface_name
            ifid = interface.interface_id
            conn = bbe.get_connection(device=router, interface=ifid)
            if not conn:
                t.log("this interface ifid has no connection, will ignore it")
                continue
            resps = dut1.pyez('get_interface_information', terse=True,
                              interface_name=name, timeout=600).resp.findall('physical-interface')
            for resp in resps:
                status = resp.findtext('oper-status')
                if status != 'up':
                    result = False
                    t.log('Warning, interface {} status is {}'.format(interface, status))

        if result:
            t.log("all interfaces are up")
            break
        else:
            time.sleep(10)
            #reset the result value for next iteration
            result = True
            if time.time() - basetime > 600:
                raise Exception("some interfaces are still down after 600s")


def prepare_rt_before_login(rt_device_id='rt0', autoneg=True):
    """
    prepare tester status before Testing, include start up the links of custom/uplink,
    setting dhcp arp and enable protocol stacking mode for dualstack
    :param rt_device_id:            e.g. 'rt0'
    :param autoneg:            auto-negotiation , default is True
    :return:
    """
    t.log("inside prepare_rt_before_login")
    if t['resources'][rt_device_id]['system']['primary']['make'] != 'ixia':
        t.log("this prepare_rt_before_login supports IxNetwork only")
        return
    _check_bbe()
    rt_handle = t.get_handle(rt_device_id)
    ###fix the ixia port auto_detect_instrumentation_type to end_of_frame, and change the autonegotiation to 1/0
    if not autoneg:
        for rtlink in bbe.get_interfaces(rt_device_id):
            interface_args = {}
            interface_args['mode'] = 'modify'
            interface_args['port_handle'] = rt_handle.port_to_handle_map[rtlink.interface_name]
            interface_args['auto_detect_instrumentation_type'] = 'end_of_frame'
            interface_args['autonegotiation'] = '0'
            conn = bbe.get_connection(rt_device_id, rtlink.interface_id)
            if 'ge' in conn.interface_name:
                interface_args['speed'] = 'ether1000'
            elif 'xe' in conn.interface_name:
                interface_args['speed'] = 'ether10Gig'
            elif 'et' in conn.interface_name:
                interface_args['speed'] = 'ether100Gig'
            rt_handle.invoke('interface_config', **interface_args)
    else:
        for port in rt_handle.port_list:
            rt_handle.invoke('interface_config', mode='modify', port_handle=rt_handle.port_to_handle_map[port],
                             auto_detect_instrumentation_type='end_of_frame', autonegotiation=1)

    all_subs = bbe.get_subscriber_handles()
    for subs in all_subs:
        if subs.family == 'dual' or (subs.family == 'ipv6' and subs.subscribers_type != 'dhcp'):
            rt_handle.invoke('set_protocol_stacking_mode')
            break
    if rt_handle.ae:
        for handle in rt_handle.ae['handle']:
            rt_handle.invoke('client_action', handle=handle, action='start')
            time.sleep(10)

    if bbe.get_subscriber_handles(protocol='dhcp'):
        if t['resources'][rt_device_id]['system']['primary']['make'] == 'ixia':
            t.log("set interface arp transmit count to 6 to prevent arp issue for dhcp client")
            root = rt_handle.invoke('IxNet::getRoot')
            vports = rt_handle.invoke('IxNet::getList', root, 'vport')
            for vport in vports:
                rt_handle.invoke('IxNet::setAttribute', vport + '/protocolStack/options', '-ipv4McastSolicit', '6')
            rt_handle.invoke('IxNet::commit')

    if 'start-ancp-before-test' in t.user_variables['uv-bbevar']:
        if t.user_variables['uv-bbevar']['start-ancp-before-test']:
            all_subs = bbe.get_subscriber_handles()
            for subs in all_subs:
                if subs.has_ancp:
                    handle = subs.rt_ancp_handle
                    rt_handle.invoke('client_action', handle=handle, action='start')
    start_rt_links()

    ###FRA005520 IxNetwork, Add control to start NGPF emulations without delay since 8.40
    if t['resources'][rt_device_id]['system']['primary']['make'] == 'ixia' and rt_handle.version > '8.40':
        rt_handle.invoke('IxNet::execute', 'configureAll', '/globals/topology')


def prepare_router_before_login():
    """
    add bbevty_pri and bbevty_sla mode for used in future to login into the bbe vty shell
    clear the stats/shmlog, later user can call the vty shell command using
    router.execute_command(mode='bbevty_pri', command='show bbemem internals')
    :return:
    """
    t.log("inside prepare_router_before_login")
    _check_bbe()
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    bbe.cst_action_stat = {}
    bbe.cst_action_stat['processed_daemons'] = []
    for device in router_ids:
        router = t.get_handle(device)
        if hasattr(router, 'vc') and router.vc:
            mode = 'bbevty_pri'
            if mode not in router.current_node.current_controller.custom_modes:
                router.add_mode(mode='bbevty_pri', exit_command='quit', command='vty -s 7208 161.0.0.1', pattern='vty-bbe#')
            mode = 'bbevty_sla'
            if mode not in router.current_node.current_controller.custom_modes:
                router.add_mode(mode='bbevty_sla', exit_command='quit', command='vty -s 7208 161.0.0.6', pattern='vty-bbe#')
        else:
            mode = 'bbevty_pri'
            if mode not in router.current_node.current_controller.custom_modes:
                router.add_mode(mode='bbevty_pri', exit_command='quit', command='vty -s 7208 128.0.0.1', pattern='vty-bbe#')
            if len(router.current_node.controllers.keys()) == 2:
                mode = 'bbevty_sla'
                if mode not in router.current_node.current_controller.custom_modes:
                    router.add_mode(mode='bbevty_sla', exit_command='quit', command='vty -s 7208 128.0.0.5', pattern='vty-bbe#')
                # also set modes on other RE
                current_re = router.current_node.current_controller_str
                for key in router.current_node.controllers.keys():
                    if key != current_re:
                        router.set_current_controller(system_node='primary', controller=key)
                        mode = 'bbevty_pri'
                        if mode not in router.current_node.current_controller.custom_modes:
                            router.add_mode(mode='bbevty_pri', exit_command='quit', command='vty -s 7208 128.0.0.1', pattern='vty-bbe#')
                        mode = 'bbevty_sla'
                        if mode not in router.current_node.current_controller.custom_modes:
                            router.add_mode(mode='bbevty_sla', exit_command='quit', command='vty -s 7208 128.0.0.5', pattern='vty-bbe#')
                router.set_current_controller(system_node='primary', controller=current_re)
        # clear existing statistics
        command_list = []
        command_list.append('clear ppp statistics')
        command_list.append('clear pppoe statistics')
        command_list.append('clear dhcp statistics')
        command_list.append('clear dhcpv6 statistics')
        command_list.append('clear network-access aaa statistics authentication')
        command_list.append('clear network-access aaa statistics accounting')
        command_list.append('clear network-access aaa statistics radius')
        command_list.append('clear shmlog all-info logname all')
        for command in command_list:
            router.cli(command=command, timeout=120)


def cst_start_clients(**kwargs):
    """
    start clients
    :param kwargs:
    subs:                     subscriber object list that is used to start
    login_retries:            retry times, default is 10
    restart_unbound_only:     True/False, by default is false, restart unbounded clients only
    stabilize_time:           stable time after subs login
    device_id:                router resource name list to collect the client info
    check_access_route:       True/False, default is True
    verify_router:            True/False, default is true, verify the client number and access route count
    cpu_settle:               cpu idle settle value, by default is 75
    cpu_check:                True/False, default is true, check the cpu values in router,
    :return:
    """
    t.log("cst_start_client kwargs is {}".format(kwargs))
    _check_bbe()
    verify_route = kwargs.get('check_access_route', True)
    if isinstance(verify_route, str):
        verify_route = eval(verify_route)
    if 'device_id' in kwargs:
        router_ids = kwargs['device_id']
        if not isinstance(router_ids, list):
            router_ids = [router_ids]
    else:
        router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    if 'subs' in kwargs:
        subs_list = kwargs['subs']
        if not isinstance(subs_list, list):
            subs_list = [subs_list]
    else:
        subs_list = bbe.get_subscriber_handles()
    all_clients = False
    if subs_list == bbe.get_subscriber_handles():
        all_clients = True
    result = get_configured_subs(device_id=router_ids, subs=subs_list)
    all_subs_up = 0
    expected_subs_in_rt = int(result['expected_total_session_in_testers'])
    expected_login_time = expected_subs_in_rt / result['expected_login_rate']
    max_wait_time = 3 * expected_subs_in_rt / result['expected_login_rate']
    if max_wait_time < 30:
        max_wait_time = 300
    t.log('expected subs in rt will be {}'.format(expected_subs_in_rt))
    if int(expected_login_time) <= 1:
        expected_login_time += 5
    expected_subs_in_router = result['expected_total_session_in_routers']
    partial_login = False

    base_sub_list = subs_list.copy()
    if base_sub_list:
        for subscriber in subs_list:
            if subscriber.rt_state == 'started' and 'restart_unbound_only' not in kwargs:
                partial_login = True
                t.log('subs {} already in login state from rt'.format(subscriber.tag))
                base_sub_list.remove(subscriber)
                login_result = get_configured_subs(device_id=router_ids, subs=subscriber)
                expected_subs_in_router -= int(login_result['expected_total_session_in_routers'])
                expected_subs_in_rt -= int(login_result['expected_total_session_in_testers'])
        t.log('expected login session in router is {}, '
              'expected login session in tester is {}'.format(expected_subs_in_router, expected_subs_in_rt))
        if expected_subs_in_rt == 0 and expected_subs_in_router == 0 and not all_clients:
            for subscriber in subs_list:
                t.log("specified subs {} already in login state".format(subscriber.tag))
            return
        if not base_sub_list and all_clients:
            t.log('all subscribers objects already in started state, verify the real numbers in router/testers')
            result3 = get_configured_subs(device_id=router_ids)
            expected_subs_in_rt = int(result3['expected_total_session_in_testers'])
            expected_subs_in_router = int(result3['expected_total_session_in_routers'])
            total_active_subs_in_routers = 0
            for router_id in router_ids:
                summary = get_router_sub_summary(router_id)
                t.log('router {} subscriber summary: {}'.format(router_id, summary))
                total_active_subs_in_routers += summary['client'] - summary.get('terminated', 0) - summary.get('terminating', 0)
            if total_active_subs_in_routers != expected_subs_in_router:
                t.log("subscribers count in router is not the same as expected {}, "
                      "need to clear the clients in rt".format(expected_subs_in_router))
                t.log("kwargs is {}".format(kwargs))
                if total_active_subs_in_routers == 0:
                    rt_stats = get_rt_subs_info()
                    subs_in_rt_pre_start = rt_stats['rt_sessions_up']
                    if subs_in_rt_pre_start == 0:
                        t.log("the tester session already in down state")
                    else:
                        cst_release_clients(release_method='abort', **kwargs)
                else:
                    cst_release_clients(**kwargs)
            else:
                t.log('the subscriber count in router matches the expected {}'.format(expected_subs_in_router))
                t.log('check the tester stats before start login')
                rt_stats = get_rt_subs_info()
                subs_in_rt_pre_start = rt_stats['rt_sessions_up']
                if subs_in_rt_pre_start == expected_subs_in_rt:
                    t.log('the subscribers count in tester is the same as expected {}'.format(expected_subs_in_rt))
                    t.log('no need to login since all the subs are in active state')
                    return
                else:
                    t.log('WARN', "the subscribers count in tester {} is not the same as expected {} "
                                  "before start".format(subs_in_rt_pre_start, expected_subs_in_rt))
                    t.log("need to clear both the router and tester sessions")
                    cst_release_clients(release_method='abort', verify_router=False, **kwargs)
                    for router_id in router_ids:
                        clear_subscribers_in_router(device_id=router_id)

    base_up_subs_in_router = 0
    base_route_summary = 0
    base_up_subs_in_rt = 0
    collect_pfe_info_state = kwargs.get('collect_pfe_info', False)
    if 'restart_unbound_only' not in kwargs:
        for router_id in router_ids:
            summary = get_router_sub_summary(router_id)
            t.log('router {} subscriber summary: {} before login'.format(router_id, summary))
            base_up_subs_in_router += summary['client'] - summary.get('terminated', 0) - summary.get('terminating', 0)
            if verify_utils.convert_str_to_num_or_bool(verify_route):
                base_route_summary += get_route_summary(router_id)
        base_up_subs_in_rt = 0
        base_down_subs_in_rt = 0
        if partial_login or not all_clients:
            rt_output = get_rt_subs_info()
            base_up_subs_in_rt = rt_output['rt_sessions_up']
            base_down_subs_in_rt = rt_output['rt_sessions_down']
            if base_up_subs_in_rt == 0:
                if base_up_subs_in_router > 0:
                    t.log("needs to clear the subscribers in routers first")
                    clear_subscribers_in_router(**kwargs)
                    t.log("reset the base clients in router to 0")
                base_up_subs_in_router = 0
                base_route_summary = 0
                base_up_subs_in_rt = 0
            if base_up_subs_in_rt != 0 and base_up_subs_in_router != 0 and base_up_subs_in_rt == base_up_subs_in_router and base_down_subs_in_rt == 0 and rt_output['rt_sessions_not_started'] == 0 and rt_output['rt_sessions_up'] == expected_subs_in_rt:
                for subscriber in subs_list:
                    t.log("specified subs {} already in login state".format(subscriber.tag))
                return
            # if base_up_subs_in_rt < result['expected_total_session_in_testers']:
            #     base_up_subs_in_router = 0
            #expected_subs_in_router += base_up_subs_in_router

        tester = t.get_handle(kwargs.get('rt_device_id','rt0'))
        for subs in subs_list:
            if subs.has_ancp:
                tester.invoke('ancp_action', handle=subs.rt_ancp_handle, action='start')
        for subs in subs_list:
            subs.start()
        not_started_count = expected_subs_in_rt
        base_time = time.time()

        if collect_pfe_info_state:
            from threading import Thread
            interval = kwargs.get('interval', 60)
            bgfpccheck = get_fpc_vty_stats(interval)
            action_thread = Thread(target=bgfpccheck.run)
            action_thread.start()
            time.sleep(.1)
            if action_thread.is_alive():
                t.log('successfully kicked off get_fpc_vty_stats with interval {}'.format(interval))
            else:
                t.log('WARN', 'failed to start get_fpc_vty_stats with interval {}'.format(interval))
        ##waiting for tester to send out packet
        while not_started_count == expected_subs_in_rt:
            t.log('waiting for tester to start login')
            time.sleep(15)
            rt_output = get_rt_subs_info()
            total_up_subs_in_rt = rt_output['rt_sessions_up'] - base_up_subs_in_rt
            total_down_subs_in_rt = rt_output['rt_sessions_down'] - base_down_subs_in_rt
            not_started_count = expected_subs_in_rt - total_up_subs_in_rt - total_down_subs_in_rt
            if expected_subs_in_rt == 0:
                break
            if rt_output['rt_sessions_up'] >= expected_subs_in_rt:
                total_up_subs_in_rt = rt_output['rt_sessions_up']
            if rt_output['rt_sessions_down'] == 0 and rt_output['rt_sessions_up'] >= expected_subs_in_rt and rt_output['rt_sessions_not_started'] == 0:
                all_subs_up = 1
                break
            if time.time() - base_time > max_wait_time:
                rt_output = get_rt_subs_info()
                if rt_output['rt_sessions_up'] == (expected_subs_in_rt + base_up_subs_in_rt):
                    t.log("all subscribers are up & stable state in RT")
                elif not_started_count == expected_subs_in_rt:
                    t.log('WARN', 'not a single packet send out after {} seconds'.format(max_wait_time))
                    raise Exception("No tx packets was seen in rt stats after max_wait_time, please check".format(max_wait_time))
        ##polling the session counter in rt during login
        no_change_counter = 0
        base_time = time.time()
        restart_unbound = False

        while total_up_subs_in_rt < (expected_subs_in_rt + base_up_subs_in_rt):
            t.log('current up sessions in rt is {}'.format(get_rt_subs_info()['rt_sessions_up']))
            time.sleep(15)
            previous_subs_count = total_up_subs_in_rt
            rt_output = get_rt_subs_info()
            total_up_subs_in_rt = rt_output['rt_sessions_up'] - base_up_subs_in_rt
            total_down_subs_in_rt = rt_output['rt_sessions_down'] - base_down_subs_in_rt
            if total_down_subs_in_rt == 0 and total_up_subs_in_rt == expected_subs_in_rt:
                t.log('all expected subscribers {} login in testers'.format(expected_subs_in_rt))
                all_subs_up = 1
                break
            not_started_count = expected_subs_in_rt - total_up_subs_in_rt - total_down_subs_in_rt
            if not_started_count == 0:
                t.log('all clients tried, will try to restart those unbound clients')
                restart_unbound = True
                break
            delta_count = total_up_subs_in_rt - previous_subs_count
            ## try restart unbound when no sessions change in 2 minutes
            if delta_count == 0:
                no_change_counter += 1
                if no_change_counter > 5:
                    if total_up_subs_in_rt > 0:
                        restart_unbound = True
                        t.log("subscribers in rt not increasing for more than 2 minutes, will restart unbound clients")
                        break
                    else:
                        raise Exception("no subscriber login, please check router configurations")
            login_time = time.time() - base_time
            if login_time > expected_login_time * 20:
                t.log('it took {0:.2f},  more than 20 times of expected login time {1:.2f}, '
                      'will try restart those subscribers in down state'.format(login_time, expected_login_time))
                restart_unbound = True
                break
    else:
        subs_in_routers_pre_restart = 0
        for router_id in router_ids:
            summary = get_router_sub_summary(router_id)
            t.log('router {} subscriber summary pre restart: {}'.format(router_id, summary))
            subs_in_routers_pre_restart += summary['client'] - summary.get('terminated', 0) - summary.get('terminating', 0)
        started_sub_list = []
        not_started_sub_list = []
        all_started = True
        for subscriber in bbe.get_subscriber_handles():
            if subscriber.rt_state == 'started':
                started_sub_list.append(subscriber)
            else:
                if subscriber in subs_list:
                    all_started = False
                    not_started_sub_list.append(subscriber)
        t.log('current started subs are {}'.format(started_sub_list))
        t.log('current not started subs are {}'.format(not_started_sub_list))

        restart_unbound = True

        if all_started:
            result2 = get_configured_subs(device_id=router_ids,subs=started_sub_list)
            expected_subs_in_router = result2['expected_total_session_in_routers']
            if expected_subs_in_router == subs_in_routers_pre_restart:
                t.log("all specified subscribers are bounded in router")
                t.log("check if there is any sub in down state in rt")
                all_subs_up = 1
                restart_output = get_rt_subs_info()
                if restart_output['rt_sessions_down'] == 0:
                    t.log("No need to restart down since currently no subscriber is in down state in rt")
                    return
        else:
            raise Exception('some subscriber was not in started state when calling with restart unbound only')

    #tracking the delta_up_subs_in_rt(no subs in down state)
    if restart_unbound:
        retry = 1
        base_time = time.time()
        base_time_loop = base_time
        while retry <= int(kwargs.get('login_retries', 10)):
            t.log('retry #{} to restart unbound clients'.format(retry))
            for sub in subs_list:
                if retry == 3:
                    sub.start()
                sub.restart_down()
            rt_output = get_rt_subs_info()
            base_up_subs_in_rt1 = rt_output['rt_sessions_up']
            total_up_subs_in_rt1 = base_up_subs_in_rt1
            total_down_subs_in_rt1 = rt_output['rt_sessions_down']
            stable_timer = 1
            while total_down_subs_in_rt1 != 0:
                t.log('waiting for subs in down state to change')
                rt_output = get_rt_subs_info()
                total_down_subs_in_rt1 = rt_output['rt_sessions_down']
                total_up_subs_in_rt1 = rt_output['rt_sessions_up']
                delta_up_subs_in_rt = total_up_subs_in_rt1 - base_up_subs_in_rt1
                t.log('current up sessions is {}, total up sub sessions change is {}'.
                      format(total_up_subs_in_rt1, delta_up_subs_in_rt))
                if delta_up_subs_in_rt == 0 and stable_timer >= 3:
                    t.log('will restart clients since no up sessions changed for three stable timer')
                    sub.start()
                    break
                elif delta_up_subs_in_rt == 0:
                    t.log('up subs count not change within stable timer {} in retry {}'.format(stable_timer, retry))
                    stable_timer += 1
                else:
                    base_up_subs_in_rt1 = total_up_subs_in_rt1
                    continue

                max_wait_time = 6 * expected_subs_in_rt / result['expected_login_rate']
                if max_wait_time < 90:
                    max_wait_time = 90
                ##wait for 3 times of expected login time
                if time.time() - base_time_loop > max_wait_time:
                    t.log('WARN', 'subscriber still not fully bound after waiting for {:.2f}s, exit retry {}'.
                          format(max_wait_time, retry))
                    base_time_loop = time.time()
                    break
                base_up_subs_in_rt1 = total_up_subs_in_rt1
                time.sleep(10)
            total_down_subs_in_rt1 = get_rt_subs_info()['rt_sessions_down']
            if total_down_subs_in_rt1 == 0:
                if total_up_subs_in_rt1 == (expected_subs_in_rt + base_up_subs_in_rt):
                    t.log('all expected subscribers {} '
                          'in rt login successfully after rebind'.format(expected_subs_in_rt))
                    all_subs_up = 1
                    break
                else:
                    t.log('no subscriber in down state')
                    if total_up_subs_in_rt1 != (expected_subs_in_rt + base_up_subs_in_rt):
                        for subs in subs_list:
                            subs.start()

            ##wait for 10 times of expected login time
            total_max_wait_time = 20 * expected_subs_in_rt / result['expected_login_rate']
            if time.time() - base_time > total_max_wait_time:
                rt_output = get_rt_subs_info()
                total_up_subs_in_rt = rt_output['rt_sessions_up'] - base_up_subs_in_rt
                if total_up_subs_in_rt == expected_subs_in_rt:
                    t.log("all subscribers are up & stable state in RT")
                else:
                    t.log('ERROR', 'subscriber still not fully bound after waiting for {}s'.format(total_max_wait_time))
                    raise Exception("subscriber still not fully bound after waiting")
            retry += 1

        rt_output = get_rt_subs_info()
        total_up_subs_in_rt = rt_output['rt_sessions_up'] - base_up_subs_in_rt
        if total_up_subs_in_rt == expected_subs_in_rt or all_subs_up:
            t.log("all subscribers are up & stable state in RT")
        elif total_down_subs_in_rt1 > 0:
            t.log('subscriber still not fully bound after retry {}'.format(retry - 1))
            raise Exception("subscriber failed to be fully bounded after restart retries, "
                            "current session {}, expected session {}".format(total_up_subs_in_rt1, expected_subs_in_rt))

    if 'stabilize_time' in kwargs:
        if total_down_subs_in_rt == 0:
            t.log('waiting for subscribers in stable state for {} seconds'.format(kwargs['stabilize_time']))
            rt_output = get_rt_subs_info()
            previous_subs_count = rt_output['rt_sessions_up']
            base_time = time.time()
            ## raise exception when no sessions change in stabilize time
            while time.time() - base_time < kwargs['stabilize_time']:
                time.sleep(10)
                rt_result = get_rt_subs_info()
                total_up_subs_in_rt = rt_result['rt_sessions_up']
                total_down_subs_in_rt = rt_result['rt_sessions_down']
                delta_count = total_up_subs_in_rt - previous_subs_count
                if delta_count != 0 or total_down_subs_in_rt != 0:
                    t.log('subscriber not stay in stable state for specified time, try to rebind again')
                    for subs in subs_list:
                        subs.start()
                        subs.restart_down()
                    time.sleep(15)
                    # reset base time
                    base_time = time.time()
            total_down_subs_in_rt = get_rt_subs_info()['rt_sessions_down']
            if total_down_subs_in_rt == 0:
                t.log("all subscribers are in stable state in RT")
            else:
                raise Exception('subscribers are not in stable state')

    t.log('Total Expected Sessions: {} Total Up Sessions in RT: {}'.format(expected_subs_in_rt, total_up_subs_in_rt))
    if total_up_subs_in_rt == expected_subs_in_rt or all_subs_up:
        t.log('All subscribers came up, Total Expected Sessions: {}'.format(expected_subs_in_rt))
    elif rt_output['rt_sessions_down'] > 0:
        raise Exception('not all subscribers log in RT finally')

    verify_router = kwargs.get('verify_router', True)
    if collect_pfe_info_state:
        if action_thread.is_alive():
            bgfpccheck.stop()
            action_thread.join()
        t.log("background thread checking fpc memory stopped")
    if verify_utils.convert_str_to_num_or_bool(verify_router):
        ### add cpu check before issue CLI
        cpu_check = kwargs.get('cpu_check', True)
        if verify_utils.convert_str_to_num_or_bool(cpu_check):
            for router_id in router_ids:
                BBEJunosUtil.router_handle = t.get_handle(resource=router_id)
                BBEJunosUtil.cpu_settle(cpu_threshold=int(kwargs.get('cpu_process', 30)),
                                        idle_min=int(kwargs.get('cpu_settle', 75)),
                                        dead_time=int(kwargs.get('cpu_deadtime', 1200)),
                                        interval=int(kwargs.get('cpu_interval', 20)))
        ### check the router statistics
        total_active_subs_in_routers = 0
        for router_id in router_ids:
            summary = get_router_sub_summary(router_id)
            t.log('router {} subscriber summary: {}'.format(router_id, summary))
            if 'configured' in summary or 'Init' in summary or 'Terminating' in summary or 'Terminated' in summary:
                raise Exception("some subs in abnormal state in device {} with summary {}".format(router_id, summary))
            total_active_subs_in_routers += summary['client'] - summary.get('terminated', 0) - summary.get('terminating', 0)
            router_key = router_id + '_actual_subscribers'
            router = t.get_handle(router_id)
            if verify_utils.convert_str_to_num_or_bool(cpu_check):
                router.cli(command="show system resource-monitor summary")
                router.cli(command="show task memory detail")
                router.cli(command="show network-access aaa statistics authentication")
                router.cli(command="show network-access aaa statistics accounting ")
                router.cli(command="show route forwarding-table summary")

                if bbe.cst_stats['partial_login'] == 0 and 'total_ifl_sets' not in bbe.cst_stats:
                    resp = router.cli(command='show interfaces interface-set | match "Interface set index:" | count',
                                      timeout=600).resp
                    number_of_ifls = resp.split()[1]
                    bbe.cst_stats['total_ifl_sets'] = number_of_ifls
            if bbe.cst_stats['partial_login'] == 0 and router_key not in bbe.cst_stats:
                bbe.cst_stats[router_key] = summary
        if total_active_subs_in_routers >= expected_subs_in_router:
            t.log("all subscribers {} login in routers successfully".format(total_active_subs_in_routers))
            if bbe.cst_stats['partial_login'] == 0 and 'actual_clients_in_routers' not in bbe.cst_stats:
                bbe.cst_stats['actual_clients_in_routers'] = expected_subs_in_router
                bbe.cst_stats['dut_number_of_subscribers'] = expected_subs_in_router
                bbe.cst_stats['number_of_subscribers'] = expected_subs_in_rt
                bbe.cst_stats['re_fpc_memory_utilization'] = get_re_fpc_memory()

        else:
            bbe.cst_stats['dut_number_of_subscribers'] = total_active_subs_in_routers
            t.log('WARN', 'there are {} subscribers in routers, instead of'
                          ' expected {}'.format(total_active_subs_in_routers, expected_subs_in_router))
            raise Exception('there are {} subscribers in routers, instead of '
                            'expected {}'.format(total_active_subs_in_routers, expected_subs_in_router))
        if 'restart_unbound_only' not in kwargs and verify_utils.convert_str_to_num_or_bool(verify_route):
            t.log("before verify route, the base sub list is {}".format(base_sub_list))
            verify_client_route(device_id=router_ids, subs=subs_list, base_route_count=base_route_summary)


def cst_release_clients(**kwargs):
    """
    release clients
    :param kwargs:
    subs:           bbe subscriber object list
    device_id:      router_id, eg. 'r0', default is a id list of duts
    verify_router:  True/False, default is True, check access route and client count after release
    logout_retry:          retry waiting iteration, default is 20
    check_all:     True/False, default is False, to check if totally get removed
    :return:
    """
    check_total = kwargs.get('check_all', False)
    t.log("inside cst_release_clients, kwargs is {}".format(kwargs))
    _check_bbe()
    if 'device_id' in kwargs:
        router_ids = kwargs['device_id']
        if not isinstance(router_ids, list):
            router_ids = [router_ids]
    else:
        router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    if 'subs' in kwargs:
        subs_list = kwargs['subs']
        if not isinstance(subs_list, list):
            subs_list = [subs_list]
        if subs_list == bbe.get_subscriber_handles():
            logout_all = True
        else:
            logout_all = False
    else:
        subs_list = bbe.get_subscriber_handles()
        logout_all = True
    base_sub_list = subs_list.copy()
    t.log("subs_list is {}".format(subs_list))
    for subs in base_sub_list:
        if subs.rt_state == 'stopped':
            t.log('subs {} already logout from rt'.format(subs.rt_ethernet_handle))
            base_sub_list.remove(subs)
    if not base_sub_list:
        t.log('all subscribers logout from rt already, exit cst_release_clients')
        return True
    t.log("subs_list is {}".format(subs_list))
    result = get_configured_subs(device_id=router_ids, subs=subs_list)
    expected_subs_remove_in_rt = result['expected_total_session_in_testers']
    rt_output = get_rt_subs_info()
    base_up = rt_output['rt_sessions_up']
    if expected_subs_remove_in_rt > base_up:
        expected_subs_remove_in_rt = base_up
    base_count = rt_output['rt_sessions_not_started']

    # set the baseline for routers
    expected_subs_remove_in_router = result['expected_total_session_in_routers']

    base_up_subs_in_router = 0
    for router_id in router_ids:
        summary = get_router_sub_summary(router_id)
        t.log('router {} subscriber summary: {} before logout'.format(router_id, summary))
        base_up_subs_in_router += summary['client'] - summary.get('terminated', 0) - summary.get('terminating', 0)
    t.log("base_up_subs_in_router is {}".format(base_up_subs_in_router))
    if base_up_subs_in_router < expected_subs_remove_in_router:
        expected_subs_remove_in_router = base_up_subs_in_router
    expected_subs_in_router = base_up_subs_in_router - expected_subs_remove_in_router
    t.log('final expected subs in router is {}'.format(expected_subs_in_router))
    release_method = kwargs.get('release_method', 'stop')
    tester = t.get_handle(kwargs.get('rt_device_id', 'rt0'))

    for subs in subs_list:
        if release_method == 'stop':
            subs.stop()
        else:
            subs.abort()
    for subs in subs_list:
        if subs.has_ancp:
            tester.invoke('ancp_action', handle=subs.rt_ancp_handle, action='stop')
    rt_output = get_rt_subs_info()
    not_started_count = rt_output['rt_sessions_not_started'] - base_count
    loop_count = 1
    while not_started_count < expected_subs_remove_in_rt:
        if rt_output['rt_sessions_down'] == 0 and rt_output['rt_sessions_up'] == 0 and rt_output['rt_sessions_not_started'] == rt_output['rt_sessions_total'] or loop_count >= 600:
            break
        time.sleep(15)
        rt_output = get_rt_subs_info()
        not_started_count = rt_output['rt_sessions_not_started'] - base_count
        loop_count += 1

    if loop_count >= 600:
        raise Exception('some subscribers are still in tester, please check the router/tester')
    else:
        t.log('all expected subs {} logout from testers'.format(expected_subs_remove_in_rt))

    verify_router = kwargs.get('verify_router', True)
    if verify_utils.convert_str_to_num_or_bool(verify_router):
        ### check the router statistics
        retry = kwargs.get('logout_retry', 40)
        half_retry = int(retry/2)
        wait_time = int(kwargs.get('wait_time', 10))
        stable_timer = 1
        last_active_subs_in_router = 0
        while retry > 0:
            t.log('waiting for clients to release from router in countdown #{}'.format(retry))
            time.sleep(wait_time)
            total_subs = 0
            total_active_subs_in_router = 0
            for router_id in router_ids:
                result = get_router_sub_summary(router_id)
                t.log('router {} subscriber summary: {}'.format(router_id, result))
                total_subs += result['total']
                total_active_subs_in_router += result['client']
            delta_active_subs = total_active_subs_in_router - last_active_subs_in_router
            if delta_active_subs != 0:
                t.log('it is still releasing clients, waiting for 10s')
                last_active_subs_in_router = total_active_subs_in_router
                continue
            if total_active_subs_in_router > expected_subs_in_router:
                if delta_active_subs == 0 and stable_timer <= half_retry:
                    t.log('not all expected subscriber {} logout, '
                          'waiting for another stable timer'.format(expected_subs_remove_in_router))
                    stable_timer += 1
                    last_active_subs_in_router = total_active_subs_in_router
                elif delta_active_subs == 0:
                    t.log("the count of active subs not changed for 10 stable timer, exit")
                    break
            if logout_all and total_subs != 0 and check_total:
                t.log("total subs count is {}, will waiting for more time".format(total_subs))
                retry = retry - 1
                continue
            elif total_active_subs_in_router == expected_subs_in_router:
                break
            retry = retry - 1

        if total_active_subs_in_router != expected_subs_in_router:
            raise Exception('some subscribers are still in routers, please check the router')
        else:
            t.log("checking total counts after clients logout, some vlan subscribers may be still in there")
            if logout_all and total_subs != 0 and check_total:
                raise Exception("total subscribers count is still not reaching 0, please check routers")
            t.log('all specified subscribers {} logout from the routers'.format(expected_subs_remove_in_router))


def get_configured_subs(**kwargs):
    """
    get total login_rate/logout_rate/total_session defined in yaml
    :param kwargs:
    subs:       subscriber list
    device_id:  device id
    :return:    dictionary of login_rate/logout_rate/total_session
    """
    t.log("inside get_configured_subs, kwargs is {}".format(kwargs))
    result = dict()
    if 'device_id' in kwargs:
        device_ids = kwargs['device_id']
        if not isinstance(device_ids, list):
            device_ids = [device_ids]
    else:
        device_ids = bbe.get_devices(device_tags='dut', id_only=True)

    ae_member_in_rt = get_ae_info(device_id=kwargs.get('rt_device_id', 'rt0'))
    for device_id in device_ids:
        if 'rt' in device_id:
            continue
        handle = t.get_handle(device_id)
        if device_id + '_name' not in bbe.cst_stats:
            result[device_id + '_version'] = handle.get_version()
            result[device_id + '_model'] = handle.get_model().upper()
            result[device_id + '_name'] = bbe.get_devices(devices=device_id)[0].device_name
            result['mx_model'] = result[device_id + '_model'].split(sep='X')[1]
            result['image'] = result[device_id + '_version']
            if re.search(r'(B|R)\d+', str(result['image'])):
                result['build_type'] = 'milestone'
            else:
                result['build_type'] = 'daily'
            result['dut'] = result[device_id + '_name']
    result['expected_login_rate'] = 0
    result['expected_logout_rate'] = 0
    result['expected_total_session_in_testers'] = 0
    result['expected_total_session_in_routers'] = 0
    result['expected_route_count'] = 0
    result['expected_vlan_oob_in_routers'] = 0
    result['expected_essm_in_routers'] = 0
    if 'subs' in kwargs:
        if kwargs['subs']:
            subs_list = kwargs['subs']
            if not isinstance(subs_list, list):
                subs_list = [subs_list]
            if subs_list == bbe.get_subscriber_handles():
                result['partial_login'] = 0
            else:
                result['partial_login'] = 1

        else:
            return result
    else:
        subs_list = bbe.get_subscriber_handles()
        result['partial_login'] = 0
    bbe.defined_sub_info = {}
    check_access_subs = False
    dut_count = 0
    if not result['partial_login']:
        for dut_id in device_ids:
            if 'subscriber-info' in t.resources[dut_id]['system']['primary']['uv-bbe-config']:
                # bbe.defined_sub_info = True
                sub_info = t.resources[dut_id]['system']['primary']['uv-bbe-config']['subscriber-info']
                result['expected_total_session_in_routers'] += sub_info['count-in-router']
                result['expected_total_session_in_testers'] += sub_info['count-in-tester']
                result['expected_route_count'] += sub_info['route-count']
                result[dut_id] = sub_info
                bbe.defined_sub_info[dut_id] = sub_info
                t.log(' inside1: expected_route_count is: {}'.format(result['expected_route_count']))
            else:
                t.log('no subscriber-info attributes defined under dut router {}, '
                      'will calculate from sub objects'.format(dut_id))
                check_access_subs = True
                dut_count += 1

    if check_access_subs or result['partial_login']:
        for dut_id in device_ids:
            if 'subscriber-info' in t.resources[dut_id]['system']['primary']['uv-bbe-config']:
                partial_sub_count = 0
                total_sub_count = 0
                login_rate = 0
                logout_rate = 0
                for subs in subs_list:
                    partial_sub_count += subs.count
                    login_rate += int(subs.csr)
                    logout_rate += int(subs.clr)
                for subs in bbe.get_subscriber_handles():
                    total_sub_count += subs.count
                sub_ratio = partial_sub_count / total_sub_count
                print("ratio is {}".format(sub_ratio))
                sub_info = t.resources[dut_id]['system']['primary']['uv-bbe-config']['subscriber-info']
                result['expected_total_session_in_routers'] += round(sub_info['count-in-router'] * sub_ratio)
                result['expected_total_session_in_testers'] += round(sub_info['count-in-tester'] * sub_ratio)
                result['expected_route_count'] += round(sub_info['route-count'] * sub_ratio)
                t.log(' inside2: expected_route_count is: {}'.format(result['expected_route_count']))
                if len(device_ids) == 1:
                    result['expected_login_rate'] = login_rate
                    result['expected_logout_rate'] = logout_rate
                    result['attempted_cps'] = format(result['expected_login_rate'], '.2f')
                    result['attempted_clr'] = format(result['expected_logout_rate'], '.2f')
                    bbe.cst_stats.update(result)
                    return result
        if not subs_list:
            t.log("subscriber-info must be defined under routers if no subscriber defined under interface")
            raise Exception("no subscriber info defined")
        dut_no_access = False
        for subs in subs_list:
            if subs.device_id in result:
                t.log('skip subs {} from calculation since it is already'
                      ' calculated by subscriber-info in yaml'.format(subs.interface_id))
                continue
            if subs.subinfo:
                result['expected_total_session_in_routers'] += subs.subinfo['count-in-router']
                result['expected_total_session_in_testers'] += subs.subinfo['count-in-tester']
                result['expected_route_count'] += subs.subinfo['route-count']
                t.log(' inside3: expected_route_count is: {}'.format(dut_id))
                continue
            if subs.device_id not in device_ids and not dut_no_access:
                dut_no_access = True
                if len(device_ids) == 1:
                    t.log("the dut {} has no access interface defined, will calculate "
                          "from total subs defined in other routers".format(device_ids))
                else:
                    t.log('ERROR', "you must specify the subscriber-info attributes under duts")

            len_ae = 1
            if subs.ae_bundle in ae_member_in_rt:
                len_ae = len(ae_member_in_rt[subs.ae_bundle]['active'])
            ##do not count the ethernet user since no stats in rt, but router will have the subscriber(vlan-oob)
            if subs.subscribers_type == 'l2bsa':
                result['expected_total_session_in_routers'] += int(subs.count) * len_ae
                result['expected_vlan_oob_in_routers'] += int(subs.count) * len_ae
                continue
            if subs.subscribers_type == 'pppoe' and subs.family == 'ipv6' and subs.essm_count:
                result['expected_total_session_in_routers'] += int(subs.count) + int(subs.essm_count)
                result['expected_total_session_in_testers'] += int(subs.count)
                result['expected_essm_in_routers'] += int(subs.essm_count)
                continue
            # pppoev6 and pppoe dual both have pppoe up and dhcpv6 up
            elif (subs.subscribers_type == 'pppoe' or subs.subscribers_type == 'l2tp') and subs.family != 'ipv4':
                result['expected_total_session_in_routers'] += int(subs.count) * 2 * len_ae
                result['expected_total_session_in_testers'] += int(subs.count) * 2 * len_ae
                if not (subs.termination == 'lns' and subs.device_id in device_ids and len(device_ids) == 1):
                    result['expected_route_count'] += int(subs.count) * 2 * len_ae
                print(result)
                continue
            if subs.subscribers_type == 'dhcp' and subs.family == 'dual':
                if subs.single_session:
                    result['expected_total_session_in_routers'] += int(subs.count) * len_ae
                else:
                    result['expected_total_session_in_routers'] += int(subs.count) * 2 * len_ae
                result['expected_total_session_in_testers'] += int(subs.count) * 2 * len_ae
                result['expected_route_count'] += int(subs.count) * 2 * len_ae
                continue

            result['expected_total_session_in_routers'] += int(subs.count) * len_ae
            result['expected_total_session_in_testers'] += int(subs.count) * len_ae
            if not (subs.subscribers_type == 'pppoe' and subs.family == 'ipv4' and subs.termination == 'lns' and \
                            subs.device_id in device_ids and len(device_ids) == 1):
                result['expected_route_count'] += int(subs.count) * len_ae
    if dut_count > 1:
        result['expected_total_session_in_routers'] *= dut_count

    # calculate the login/logout rate from the yaml file
    result['attempted_subscribers'] = result['expected_total_session_in_testers']
    dev_ids = t.get_junos_resources()
    for dev_id in dev_ids:
        for interface in bbe.get_interfaces(dev_id, id_only=True):
            sub_list = bbe.get_subscriber_handles(interface=interface)
            if not sub_list:
                continue
            sub_list = [each_sub for each_sub in sub_list if each_sub in subs_list]
            pppoe_sub = []
            dhcpv4_sub = []
            dhcpv6_sub = []
            for subs in sub_list:
                if (subs.subscribers_type == 'pppoe' or subs.subscribers_type == 'l2tp') and subs.family != 'ipv4':
                    pppoe_sub.append(subs)
                    dhcpv6_sub.append(subs)
                elif subs.subscribers_type == 'pppoe' or subs.subscribers_type == 'l2tp':
                    pppoe_sub.append(subs)
                elif subs.subscribers_type == 'dhcp' and subs.family == 'dual':
                    dhcpv6_sub.append(subs)
                    dhcpv4_sub.append(subs)
                elif subs.subscribers_type == 'dhcp' and subs.family == 'ipv4':
                    dhcpv4_sub.append(subs)
                elif subs.subscribers_type == 'dhcp' and subs.family == 'ipv6':
                    dhcpv6_sub.append(subs)
            for sub_type in [pppoe_sub, dhcpv4_sub, dhcpv6_sub]:
                if sub_type:
                    login_sub = sorted(sub_type, key=lambda subscriber: subscriber.count / subscriber.csr)[-1]
                    login_time = login_sub.count / login_sub.csr
                    logout_sub = sorted(sub_type, key=lambda subscriber: subscriber.count / subscriber.clr)[-1]
                    logout_time = login_sub.count / logout_sub.clr
                    for subs in sub_type:
                        result['expected_login_rate'] += subs.count / login_time
                        result['expected_logout_rate'] += subs.count / logout_time
    result['attempted_cps'] = format(result['expected_login_rate'], '.2f')
    result['attempted_clr'] = format(result['expected_logout_rate'], '.2f')
    bbe.cst_stats.update(result)
    t.log('result is {}'.format(result))
    return result


def get_rt_subs_info(**kwargs):
    """
    get protocol statistics from rt
    :param kwargs:
    percent:    collect login rate to bbe.cst_stat when percent is reached
    :return:   dictionary of sessions_up/sessions_down/sessions_total/sessions_not_started/login_rate/logout_rate
    """
    t.log("inside get_rt_subs_info, kwargs is {}".format(kwargs))
    _check_bbe()
    output = dict()
    output['rt_sessions_up'] = 0
    output['rt_sessions_down'] = 0
    output['rt_sessions_total'] = 0
    output['rt_sessions_not_started'] = 0
    output['rt_login_rate'] = 0
    output['rt_logout_rate'] = 0
    tester_ids = bbe.get_devices(devices='rt', id_only=True)
    for tester in tester_ids:
        rt_handle = t.get_handle(tester)
        try:
            result = rt_handle.invoke('get_protocol_stats')
        except Exception:
            t.log("no protocol stats yet with the exception")
            continue
        if 'PPPoX Client' in result['global_per_protocol']:
            output['pppoe'] = dict()
            output['pppoe']['rt_sessions_up'] = int(result['global_per_protocol']['PPPoX Client']['sessions_up'])
            output['pppoe']['rt_login_rate'] = float(result['global_per_protocol']['PPPoX Client']['setup_avg_rate'])
            output['rt_sessions_up'] += int(result['global_per_protocol']['PPPoX Client']['sessions_up'])
            output['rt_sessions_down'] += int(result['global_per_protocol']['PPPoX Client']['sessions_down'])
            output['rt_sessions_total'] += int(result['global_per_protocol']['PPPoX Client']['sessions_total'])
            output['rt_login_rate'] += float(result['global_per_protocol']['PPPoX Client']['setup_avg_rate'])
            output['rt_logout_rate'] += float(result['global_per_protocol']['PPPoX Client']['teardown_avg_rate'])
            output['rt_sessions_not_started'] += int(result['global_per_protocol']
                                                     ['PPPoX Client']['sessions_not_started'])
        if 'DHCPv4 Client' in result['global_per_protocol']:
            output['dhcpv4'] = dict()
            output['dhcpv4']['rt_sessions_up'] = int(result['global_per_protocol']['DHCPv4 Client']['sessions_up'])
            output['dhcpv4']['rt_login_rate'] = float(result['global_per_protocol']['DHCPv4 Client']['setup_avg_rate'])
            output['rt_sessions_up'] += int(result['global_per_protocol']['DHCPv4 Client']['sessions_up'])
            output['rt_sessions_down'] += int(result['global_per_protocol']['DHCPv4 Client']['sessions_down'])
            output['rt_sessions_total'] += int(result['global_per_protocol']['DHCPv4 Client']['sessions_total'])
            output['rt_login_rate'] += float(result['global_per_protocol']['DHCPv4 Client']['setup_avg_rate'])
            output['rt_logout_rate'] += float(result['global_per_protocol']['DHCPv4 Client']['teardown_avg_rate'])
            output['rt_sessions_not_started'] += int(result['global_per_protocol']
                                                     ['DHCPv4 Client']['sessions_not_started'])
        if 'DHCPv6 Client' in result['global_per_protocol']:
            output['dhcpv6'] = dict()
            output['dhcpv6']['rt_sessions_up'] = int(result['global_per_protocol']['DHCPv6 Client']['sessions_up'])
            output['dhcpv6']['rt_login_rate'] = float(result['global_per_protocol']['DHCPv6 Client']['setup_avg_rate'])
            output['rt_sessions_up'] += int(result['global_per_protocol']['DHCPv6 Client']['sessions_up'])
            output['rt_sessions_down'] += int(result['global_per_protocol']['DHCPv6 Client']['sessions_down'])
            output['rt_sessions_total'] += int(result['global_per_protocol']['DHCPv6 Client']['sessions_total'])
            output['rt_login_rate'] += float(result['global_per_protocol']['DHCPv6 Client']['setup_avg_rate'])
            output['rt_logout_rate'] += float(result['global_per_protocol']['DHCPv6 Client']['teardown_avg_rate'])
            output['rt_sessions_not_started'] += int(result['global_per_protocol']
                                                     ['DHCPv6 Client']['sessions_not_started'])
        t.log('tester {} subscriber_info: {}'.format(tester, output))
        #if 'partial_login' in bbe.cst_stats and bbe.cst_stats['partial_login'] == 0:
        percent = output['rt_sessions_up'] / bbe.cst_stats['expected_total_session_in_testers'] * 100
        output['percentage'] = '{0:.2f}%'.format(percent)
        if 'dhcpv4' in output and 'pppoe' in output:
            output['ipv4_subscribers'] = output['dhcpv4']['rt_sessions_up'] + output['pppoe']['rt_sessions_up']
        if 'dhcpv6' in output:
            output['ipv6_subscribers'] = output['dhcpv6']['rt_sessions_up']
        # update the login rate only when reach specified percent or default 85, only mark the first time reach that value
        if percent >= kwargs.get('percent', 85) and 'rt_login_rate' not in bbe.cst_stats:
            bbe.cst_stats['rt_login_rate'] = str(output['percentage']) + '@' + str(output['rt_login_rate'])
            bbe.cst_stats['average_cps'] = bbe.cst_stats['rt_login_rate']
        # update the bbe.cst_stats only when 100% user login
        if percent == 100:
            stats = output.copy()
            stats.pop('percentage')
            stats.pop('rt_login_rate')
            stats.pop('rt_logout_rate')
            bbe.cst_stats.update(stats)
        if percent == 0 and 'rt_login_rate' in bbe.cst_stats and 'rt_logout_rate' not in bbe.cst_stats:
            bbe.cst_stats['rt_logout_rate'] = output['rt_logout_rate']
            bbe.cst_stats['observed_clr'] = output['rt_logout_rate']
    print(bbe.cst_stats)

    return output


def get_master_re_name(resource='r0'):
    """
    get master RE name
    :param resource:       eg. 'r0'
    :return: re_name, e.g. 're0'/'primary-re0'
    """
    t.log("inside get_master_re_name, resource is {}".format(resource))
    router = t.get_handle(resource)

    controller = router.current_node.current_controller
    re_list = ['re0', 're1']
    if hasattr(router, 'vc') and router.vc:
        master_node = router.detect_master_node()
        for rename in re_list:
            rehandle = t.get_handle(resource, system_node=master_node, controller=rename)
            if rehandle.is_master():
                return master_node + '-' + rename
    else:
        if controller.is_master():
            return controller.re_name

        for name in router.current_node.controllers:
            if name != controller.re_name:
                return name
    raise Exception("no master re was found")

def get_router_sub_summary(resource='r0'):
    """
    get subscriber summary from router
    :param resource:        router_id, e.g. 'r0'
    :return: dictionary of subscriber
    """
    t.log("inside get_router_sub_summary, resource is {}".format(resource))

    dev_obj = t.get_handle(resource)
    resp = dev_obj.cli(command="show subscribers summary", timeout=600).resp
    if 'error' in resp:
        raise Exception("show subscriber summary returns error with {}".format(resp))
    subs = dev_obj.pyez('get_subscribers_summary', all=True, normalize=True, timeout=600).resp
    subs_sum = dict()
    subs_sum['client'] = 0
    ###incase the get_subscribers_summary all PR not fixed
    if subs.getnext():
        subs = subs.getnext()
    for counter in subs.findall('counters'):
        if counter.findtext('session-state-active'):
            subs_sum['active'] = int(counter.findtext('session-state-active'))
        if counter.findtext('session-state-total'):
            subs_sum['total'] = int(counter.findtext('session-state-total'))
        if counter.findtext('session-state-terminating'):
            subs_sum['terminating'] = int(counter.findtext('session-state-terminating'))
        if counter.findtext('session-state-terminated'):
            subs_sum['terminated'] = int(counter.findtext('session-state-terminated'))
        if counter.findtext('session-state-init'):
            subs_sum['init'] = int(counter.findtext('session-state-init'))
        if counter.findtext('session-state-configured'):
            subs_sum['configured'] = int(counter.findtext('session-state-configured'))
        if counter.findtext('session-type-dhcp'):
            subs_sum['dhcp'] = int(counter.findtext('session-type-dhcp'))
            subs_sum['client'] += int(counter.findtext('session-type-dhcp'))
        if counter.findtext('session-type-pppoe'):
            subs_sum['pppoe'] = int(counter.findtext('session-type-pppoe'))
            subs_sum['client'] += int(counter.findtext('session-type-pppoe'))
        if counter.findtext('session-type-dyn-ip'):
            subs_sum['dyn-ip'] = int(counter.findtext('session-type-dyn-ip'))
            subs_sum['client'] += int(counter.findtext('session-type-dyn-ip'))
        if counter.findtext('session-type-l2tp'):
            subs_sum['l2tp'] = int(counter.findtext('session-type-l2tp'))
            subs_sum['client'] += int(counter.findtext('session-type-l2tp'))
        if counter.findtext('session-type-vlan'):
            subs_sum['vlan'] = int(counter.findtext('session-type-vlan'))
        if counter.findtext('session-type-vlan-oob'):
            subs_sum['vlan-oob'] = int(counter.findtext('session-type-vlan-oob'))
            subs_sum['client'] += int(counter.findtext('session-type-vlan-oob'))
        if counter.findtext('session-type-essm'):
            subs_sum['essm'] = int(counter.findtext('session-type-essm'))
            subs_sum['client'] += int(counter.findtext('session-type-essm'))
        if counter.findtext('lsri-total'):
            subs_sum['lsri-total'] = int(counter.findtext('lsri-total'))
        if counter.findtext('session-type-static'):
            subs_sum['static'] = int(counter.findtext('session-type-static'))

    t.log("subscriber summary is {}".format(subs_sum))
    return subs_sum


def get_route_summary(resource='r0'):
    """
    get output of show route summary
    :param resource:        router_id, e.g. 'r0'
    :return: route count of access route
    """
    t.log("inside get_route_summary, resource is {}".format(resource))
    _check_bbe()
    dev_obj = t.get_handle(resource)
    route_sum = dev_obj.pyez('get_route_summary_information', normalize=True, timeout=600).resp
    total_route = 0
    for table in route_sum.findall('route-table'):
        table_name = table.findtext('table-name')
        for protocol in table.findall('protocols'):
            if 'Access' not in protocol.findtext('protocol-name'):
                continue
            else:
                name = protocol.findtext('protocol-name')
                active_route = protocol.findtext('active-route-count')
                t.log('active route for {} in table {} is {}'.format(name, table_name, active_route))
                total_route += int(active_route)
    t.log('total active route in router {} is {}'.format(resource, total_route))
    return total_route


def get_router_sub_summary_by_port(resource='r0'):
    """
    get output of show subscriber summary port
    :param resource:
    :return: dictionary in the format of port:count
    """
    t.log("inside get_router_sub_summary_by_port, resource is {}".format(resource))
    dev_obj = t.get_handle(resource)
    subs = dev_obj.pyez('get_subscribers_port_summary', normalize=True, timeout=600).resp
    port_subs = {}
    for counter in subs.findall('counters'):
        if counter.findtext('port-name'):
            port = counter.findtext('port-name')
        if counter.findtext('port-count'):
            count = counter.findtext('port-count')
        port_subs[port] = count
    t.log("subscriber summary by port is {}".format(port_subs))
    return port_subs


def get_router_sub_summary_by_slot(resource='r0'):
    """
    get output of show subscriber summary slot
    :param resource:
    :return: dictionary in the format of slot:count
    """
    t.log("inside get_router_sub_summary_by_slot, resource is {}".format(resource))
    dev_obj = t.get_handle(resource)
    subs = dev_obj.pyez('get_subscribers_summary', slot=True, normalize=True, timeout=600).resp
    slot_subs = {}
    for counter in subs.findall('counters'):
        if not counter.findtext('port-name'):
            continue
        slot = counter.findtext('port-name').split(sep='-')[1]
        if counter.findtext('port-count'):
            count = counter.findtext('port-count')
        slot_subs[slot] = count
    t.log("subscriber summary by slot is {}".format(slot_subs))
    return slot_subs


def get_aaa_authentication_stats(resource='r0'):
    """
    get output of show network-access aaa statistics authentication
    :param resource:
    :return: dictionary of auth stats
    """
    t.log("inside get_aaa_authentication_stats, resource is {}".format(resource))
    auth_stats = dict()
    dev_obj = t.get_handle(resource)
    stats = dev_obj.pyez('get_aaa_module_statistics', normalize=True, authentication=True, timeout=600).resp
    resp = stats.findall('aaa-module-authentication-statistics')
    auth_stats['requests'] = resp[0].findtext('requests')
    auth_stats['accepts'] = resp[0].findtext('accepts')
    auth_stats['rejects'] = resp[0].findtext('rejects')
    auth_stats['timeouts'] = resp[0].findtext('timeouts')
    auth_stats['challenges'] = resp[0].findtext('challenges')
    return auth_stats


def get_aaa_accounting_stats(resource='r0'):
    """
    get output of show network-access aaa statistics accounting
    :param resource:         router_id, e,g, 'r0'
    :return: dictionary of accoiunting stats
    """
    t.log("inside get_aaa_accounting_stats, resource is {}".format(resource))
    acct_stats = dict()
    dev_obj = t.get_handle(resource)
    stats = dev_obj.pyez('get_aaa_module_statistics', normalize=True, accounting=True, timeout=600).resp
    resp = stats.findall('aaa-module-accounting-statistics')
    acct_stats['requests'] = resp[0].findtext('requests')
    acct_stats['accounting-response-success'] = resp[0].findtext('accounting-response-success')
    acct_stats['accounting-response-failures'] = resp[0].findtext('accounting-response-failures')
    acct_stats['timeouts'] = resp[0].findtext('timeouts')
    return acct_stats


def get_aaa_jsrc_stats(resource='r0'):
    """
    get jsrc statistics
    >>>stats
    <Element jsrc-statistics at 0x106b574c8>

    >>>resp.findtext('jsrc-tx-suspended')
    'FALSE'

    :param resource:            router_id, e,g, 'r0'
    :return: xml element
    """
    # jsrc_stats = dict()
    t.log("inside get_aaa_jsrc_stats, resource is {}".format(resource))
    dev_obj = t.get_handle(resource)
    stats = dev_obj.pyez('get_jsrc_counters', normalize=True, timeout=600).resp
    return stats


def get_ppp_stats(resource='r0'):
    """
    show the ppp stats
    :param resource:
    :return:
    """
    t.log("inside get_ppp_stats, resource is {}".format(resource))
    router = t.get_handle(resource)
    router.shell(command='netstat -p ppp')
    router.cli(command='show ppp statistics extensive')


def get_pppoe_stats(resource='r0'):
    """
    show pppoe stats
    :param resource:
    :return:
    """
    t.log("inside get_pppoe_stats, resource is {}".format(resource))
    router = t.get_handle(resource)
    router.cli(command='show pppoe statistics')


def get_pppoe_inline_keepalive_stats(resource='r0'):
    """
    get pppoe inline keepalive stats using vty command
    :param resource:
    :return:
    """
    t.log("inside get_pppoe_inline_keepalive_stats, resource is {}".format(resource))
    device = bbe.get_devices(resource)
    int_objs = bbe.get_interfaces(resource, interfaces='access')
    fpcs = []
    for intf in int_objs:
        slot = re.findall(r'.*-(\d+)\/\d+', intf.interface_pic)[0]
        if device.is_mxvc:
            if int(slot) > 11:
                fpc = 'member1-fpc' + str(int(slot) - 11)
            else:
                fpc = 'member0-fpc' + slot
        else:
            fpc = 'fpc' + slot
        if fpc not in fpcs:
            fpcs.append(fpc)
    router = t.get_handle(resource)
    for fpc in fpcs:
        router.shell(command="cprod -A {} -c 'show jnh inline-ka session 0 ppp global-stats'".format(fpc), timeout=600)


def get_dhcp_stats(resource):
    """
    show dhcp statistics
    :param resource:
    :return:
    """
    t.log("inside get_dhcp_stats, resource is {}".format(resource))
    router = t.get_handle(resource)
    router.cli(command='show dhcp server statistics')
    router.cli(command='show dhcp relay statistics')
    router.cli(command='show dhcpv6 server statistics')
    router.cli(command='show dhcpv6 relay statistics')


def add_subscriber_mesh(**kwargs):
    """
    create BBE traffic mesh
    :param kwargs:
    rt_device_id:               tester device name e.g. default is 'rt0'
    subs:                       subscribers objects for the traffic
    traffic_args:               dictionary for creating traffic which include name, rate, frame_size,
                                bidirectional
    direction:                  up/down, if omitted, it is bi-directional
                                for details, please see add_traffic API in ixiatester.py
    uplinks:                    uplink objects for the traffic
    :return:
    """
    t.log("inside add_subscriber_mesh, kwargs is {}".format(kwargs))
    _check_bbe()
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device_id)
    subs = bbe.get_subscriber_handles()
    ipv4 = False
    ipv6 = False
    ethernet = False
    eth_src_handle = []
    eth_dst_handle = []
    v4_src_handle = []
    v6_src_handle = []
    v4_dst_handle = []
    v6_dst_handle = []
    traffic_arg = dict()
    if 'subs' in kwargs:
        subs = kwargs['subs']
        if not isinstance(subs, list):
            subs = [subs]
    for subscriber in subs:
        ###skip the subscribers not in this tester
        if subscriber.rt_device_id != rt_device_id:
            t.log("subscriber {} is not on this rt {}".format(subscriber, rt_device_id))
            continue
        if subscriber.subscribers_type == 'l2bsa':
            eth_src_handle.append(subscriber.rt_ethernet_handle)
            ethernet = True
            continue
        if subscriber.family == 'dual':
            ipv4 = True
            ipv6 = True
            if subscriber.subscribers_type in ['pppoe', 'l2tp'] and subscriber.dhcpv6_ia_type == 'ndra':
                v6_src_handle.append(subscriber.rt_pppox_handle)
            else:
                v6_src_handle.append(subscriber.rt_dhcpv6_handle)
            if subscriber.subscribers_type == 'dhcp':
                v4_src_handle.append(subscriber.rt_dhcpv4_handle)
            if subscriber.subscribers_type in ['pppoe', 'l2tp']:
                v4_src_handle.append(subscriber.rt_pppox_handle)

        if subscriber.family == 'ipv4':
            ipv4 = True
            if subscriber.subscribers_type == 'dhcp':
                v4_src_handle.append(subscriber.rt_dhcpv4_handle)
            if subscriber.subscribers_type in ['pppoe', 'l2tp']:
                v4_src_handle.append(subscriber.rt_pppox_handle)
        if subscriber.family == 'ipv6':
            ipv6 = True
            # if subscriber.essm_count or subscriber.dhcpv6_ia_type == 'ndra':
            if subscriber.subscribers_type == 'pppoe' and subscriber.essm_count or subscriber.dhcpv6_ia_type == 'ndra':
                v6_src_handle.append(subscriber.rt_pppox_handle)
            else:
                v6_src_handle.append(subscriber.rt_dhcpv6_handle)

    if 'traffic_args' in kwargs:
        traffic_arg = kwargs['traffic_args'].copy()
        traffic_arg['track_by'] = kwargs['traffic_args'].get('track_by', 'endpoint_pair traffic_item')
        if 'type' in kwargs['traffic_args'] and kwargs['traffic_args']['type'] == "ipv4":
            ipv6 = False
            traffic_arg.pop('type')
        if 'type' in kwargs['traffic_args'] and kwargs['traffic_args']['type'] == "ipv6":
            ipv4 = False
            traffic_arg.pop('type')
    else:
        traffic_arg['rate'] = '10%'
    uplinks = bbe.get_interfaces(rt_device_id, interfaces='uplink', id_only=False)

    if 'uplinks' in kwargs:
        uplinks = kwargs['uplinks']
        if not isinstance(uplinks, list):
            uplinks = [uplinks]
    for uplink in uplinks:
        if uplink.device_id != rt_device_id:
            t.log("uplink {} is not on this rt {}".format(uplink, rt_device_id))
            continue
        if ipv4:
            if uplink.rt_lns_server_session_handle:
                v4_dst_handle.append(uplink.rt_lns_server_session_handle)
            elif uplink.rt_ipv4_handle:
                v4_dst_handle.append(uplink.rt_ipv4_handle)
        if ipv6:
            if uplink.rt_lns_server_session_handle:
                v6_dst_handle.append(uplink.rt_lns_server_session_handle)
            elif uplink.rt_ipv6_handle:
                v6_dst_handle.append(uplink.rt_ipv6_handle)
        if ethernet and 'uplinks' in kwargs:
            eth_dst_handle.append(uplink.rt_ethernet_handle)

    if 'direction' in kwargs and 'up' in kwargs['direction']:
        traffic_arg['bidirectional'] = '0'
    if ipv4:
        traffic_arg['source'] = v4_src_handle
        traffic_arg['destination'] = v4_dst_handle
        if 'direction' in kwargs and 'down' in kwargs['direction']:
            traffic_arg['source'] = v4_dst_handle
            traffic_arg['destination'] = v4_src_handle
            traffic_arg['bidirectional'] = '0'
        result = tester.invoke('add_traffic', **traffic_arg)
        if result['status'] != '1':
            raise Exception('failed to create v4 traffic')
        else:
            t.log("v4 subscriber mesh created successfully")
    if ipv6:
        traffic_arg['source'] = v6_src_handle
        traffic_arg['destination'] = v6_dst_handle
        if 'direction' in kwargs and 'down' in kwargs['direction']:
            traffic_arg['source'] = v6_dst_handle
            traffic_arg['destination'] = v6_src_handle
            traffic_arg['bidirectional'] = '0'
        traffic_arg['type'] = 'ipv6'

        result2 = tester.invoke('add_traffic', **traffic_arg)
        if result2['status'] != '1':
            raise Exception('failed to create v6 traffic')
        else:
            t.log("v6 subscriber mesh created successfully")

    if ethernet and eth_dst_handle:
        traffic_arg['source'] = eth_src_handle
        traffic_arg['destination'] = eth_dst_handle
        if 'direction' in kwargs and 'down' in kwargs['direction']:
            traffic_arg['source'] = eth_dst_handle
            traffic_arg['destination'] = eth_src_handle
            traffic_arg['bidirectional'] = '0'
        traffic_arg['type'] = 'ethernet_vlan'

        result2 = tester.invoke('add_traffic', **traffic_arg)
        if result2['status'] != '1':
            raise Exception('failed to create ethernet traffic')
        else:
            t.log("ethernet subscriber mesh created successfully")

def time_in_sec(time_str):
    """
    convert time string(1:20:30) to seconds
    :param time_str:      format(h:min:s)
    :return: seconds
    """
    hour, minute, second = time_str.split(':')
    return int(hour) * 3600 + int(minute) * 60 + round(float(second))


def verify_traffic(**kwargs):
    """
    verify traffic item stats
    :param kwargs:
    rt_device_id:                         rt device name e.g. 'rt0'
    minimum_rx_percentage:                minimum percentage for received traffic
    maximum_rx_percentage:                maximum percentage for received traffic
    mode:                                 traffic verification mode, e.g. traffic_item/summary/aggregate,
                                          default is aggregate
    traffic_name_loss:                    traffic name/loss percentage dictionary, key is name, loss is percent
    traffic_bias:                         used with traffic_name_loss only.
    """
    t.log("inside verify_traffic, kwargs is {}".format(kwargs))
    _check_bbe()
    tester = t.get_handle(kwargs.get('rt_device_id', 'rt0'))
    if 'duration' in kwargs:
        duration = int(kwargs['duration'])
    traffic_stopped = False
    t.log('waiting for traffic to be fully stopped')
    while not traffic_stopped:
        result = tester.invoke('traffic_action', action='poll')
        if result['stopped'] == '1':
            traffic_stopped = True
        time.sleep(3)
    if 'mode' in kwargs:
        mode = kwargs['mode']
        if 'summary' in kwargs['mode']:
            mode = 'l23_test_summary'
        if 'traffic_item' in kwargs['mode']:
            mode = 'traffic_item'
    else:
        mode = 'aggregate'
    stats_ready = False
    while not stats_ready:
        result = tester.invoke('traffic_stats', mode=mode)
        if result['waiting_for_stats'] == '0':
            stats_ready = True
        time.sleep(2)
    if mode == 'aggregate':
        rx_packets = result[mode]['rx']['total_pkts']['sum']
        tx_packets = result[mode]['tx']['total_pkts']['sum']
        t.log('tester send packets {}, received packets {}'.format(tx_packets, rx_packets))
        percentage = float(rx_packets) * 100 / int(tx_packets)
        if percentage >= float(kwargs.get('minimum_rx_percentage', 99.0)) and percentage <= \
                float(kwargs.get('maximum_rx_percentage', 100.0)):
            t.log('received {:.2f}% traffic successfully'.format(percentage))
        else:
            raise Exception('received {:.2f}% traffic, out of the specified range'.format(percentage))
    if mode == 'l23_test_summary':
        rx_packets = result[mode]['rx']['pkt_count']
        tx_packets = result[mode]['tx']['pkt_count']
        t.log('tester send packets {}, received packets {}'.format(tx_packets, rx_packets))
        percentage = float(rx_packets) * 100 / int(tx_packets)
        if percentage >= float(kwargs.get('minimum_rx_percentage', 99.0)) and percentage <= \
                float(kwargs.get('maximum_rx_percentage', 100.0)):
            t.log('received {:.2f}% traffic successfully'.format(percentage))
        else:
            raise Exception('received {:.2f}% traffic, out of the specified range'.format(percentage))
    if mode == 'traffic_item':
        if 'traffic_name_loss' in kwargs:
            t.log('traffic name loss {}'.format(kwargs['traffic_name_loss']))
            new_name_loss = dict()
            for stream_name in kwargs['traffic_name_loss']:
                for name in result[mode]:
                    if name.endswith(stream_name):
                        new_name_loss[name] = kwargs['traffic_name_loss'][stream_name]
                        break
            names = new_name_loss
            t.log('traffic item names {}'.format(names))
        elif 'traffic_name_rate' in kwargs:
            new_name_rate = dict()
            for stream_name in kwargs['traffic_name_rate']:
                for name in result[mode]:
                    if name.endswith(stream_name):
                        new_name_rate[name] = kwargs['traffic_name_rate'][stream_name]
                        break
            names = new_name_rate
        else:
            names = result[mode].keys()
        traffic_status = True
        for name in names:
            if name == 'aggregate':
                continue

            rx_packets = int(result[mode][name]['rx']['total_pkts'])
            tx_packets = int(result[mode][name]['tx']['total_pkts'])
            loss_pkts = int(result[mode][name]['rx']['loss_pkts'])
            t.log("stream {} send {} packets, received {} packets, "
                  "loss {} packets ".format(name, tx_packets, rx_packets, loss_pkts))
            rx_bytes = int(result[mode][name]['rx']['total_pkts_bytes'])
            # tx_bytes = int(result[mode][name]['tx']['total_pkts_bytes'])
            t.log("stream {} received {} bytes".format(name, rx_bytes))
            duration = time_in_sec(result[mode][name]['rx']['last_tstamp']) - \
                       time_in_sec(result[mode][name]['rx']['first_tstamp'])
            avg_rx_rate = rx_bytes * 8 / 1000000 / duration
            loss_percent = float(result[mode][name]['rx']['loss_percent'])

            if 'traffic_name_rate' in kwargs:
                specified_rate = float(new_name_rate[name])
                percentage = float(avg_rx_rate * 100 / specified_rate)
                if percentage >= kwargs.get('minimum_rx_percentage', 99.0) and percentage <= \
                        kwargs.get('maximum_rx_percentage', 100.0):
                    t.log('received stream {} traffic rate {:.2f} mbps matches the specified rate {:.2f}'.
                          format(name, avg_rx_rate, specified_rate))
                else:
                    traffic_status = False
                    t.log('WARN','received stream {} traffic rate {:.2f}, out of the specified rate {:.2f}'.
                                    format(name, avg_rx_rate, specified_rate))
            elif 'traffic_name_loss' in kwargs:
                traffic_bias = float(kwargs.get('traffic_bias', 1.0))
                specified_loss = float(new_name_loss[name])
                loss_bias = loss_percent - specified_loss
                percentage = abs(loss_bias / traffic_bias)
                if loss_bias <= 0 or percentage <= 1:
                    t.log('received stream {} traffic rate {:.2f} mbps, loss percent {:.2f}, '
                          'expected loss percent {:.2f}'.format(name, avg_rx_rate, loss_percent, specified_loss))
                else:
                    traffic_status = False
                    t.log('WARN', 'received stream {} traffic rate {:.2f} mbps, loss percent {:.2f} > expected '
                                  'loss percent {:.2f}'.format(name, avg_rx_rate, loss_percent, specified_loss))
            else:
                t.log('stream {} receive rate {:.2f} mbps, '
                      'loss percentage {:.2f}'.format(name, avg_rx_rate, loss_percent))
                percentage = rx_packets * 100 / tx_packets
                if percentage >= kwargs.get('minimum_rx_percentage', 99.0) and percentage \
                        <= kwargs.get('maximum_rx_percentage', 100.0):
                    t.log('received stream {} {:.2f}% traffic successfully'.format(name, percentage))
                else:
                    t.log('WARN', 'received stream {} {:.2f}% traffic, '
                                  'out of the specified range'.format(name, percentage))
                    traffic_status = False
        if not traffic_status:
            raise Exception("verify traffic failed, please check warning messages for detail")


def start_traffic(**kwargs):
    """
    start traffic
    :param kwargs:
     rt_device_id:                  e,g, rt0
     duration:                      traffic running time configured in tester, which followed by verify_traffic
     handle:                        traffic item handle
    :return:
    """
    t.log("inside start_traffic, kwargs is {}".format(kwargs))
    _check_bbe()
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device_id)
    start_args = dict()
    start_args['action'] = 'start'
    if 'duration' in kwargs:
        if 'new_mesh' in kwargs and not kwargs['new_mesh']:
            tester.invoke('traffic_action', action='regenerate')
        start_args['duration'] = kwargs.get('duration')
        t.log('start traffic for {} seconds'.format(start_args['duration']))
    else:
        if 'handle' not in kwargs:
            tester.invoke('traffic_action', action='regenerate')
    try:
        if 'handle' in kwargs:
            start_args['handle'] = kwargs['handle']
        print("start_args is {}".format(start_args))
        tester.invoke('traffic_action', **start_args)

        traffic_started = False
        base_time = time.time()
        while not traffic_started:
            time.sleep(2)
            result = tester.invoke('traffic_action', action='poll')
            if result['stopped'] == '0':
                traffic_started = True
            if (time.time() - base_time) > 600:
                raise Exception('failed to start traffic after 600s, please check tester for error message')
        t.log("traffic started")
    except:
        raise Exception("traffic failed to start")


def stop_traffic(**kwargs):
    """
    stop traffic
    :param kwargs:
     rt_device_id:          e.g.'rt0'
     handle:                traffic item handle
     wait:                  wait time before issue stop traffic
    :return:
    """
    t.log("inside stop_traffic, kwargs is {}".format(kwargs))
    _check_bbe()
    if 'wait' in kwargs:
        t.log("wait for {} seconds to stop traffic".format(kwargs['wait']))
        time.sleep(int(kwargs['wait']))
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device_id)
    stop_args = dict()
    stop_args['action'] = 'stop'
    if 'handle' in kwargs:
        stop_args['handle'] = kwargs['handle']
    tester.invoke('traffic_action', **stop_args)

    traffic_stopped = False
    if 'handle' in kwargs:
        t.log("stopped traffic with handle {}".format(kwargs['handle']))
        time.sleep(2)
        return
    while traffic_stopped != True:
        time.sleep(2)
        result = tester.invoke('traffic_action', action='poll')
        if result['stopped'] == '1':
            traffic_stopped = True
    t.log("traffic stopped")


def get_dhcp_addr_from_rt(**kwargs):
    """
    get dhcp stats from tester
    :param kwargs
    rt_device_id:           e.g. 'rt0'
    subs:                   bbe subscriber object
    type:                   ipv4/ipv6
    :return: a list of dhcp stats information
    """
    t.log("inside get_dhcp_addr_from_rt, kwargs is {}".format(kwargs))
    rt_handle = t.get_handle(kwargs.get('rt_device_id', 'rt0'))
    address = list()
    subs = kwargs.get('subs', bbe.get_subscriber_handles())
    for subscriber in subs:
        if 'v4' in kwargs['type']:
            handle = subscriber.rt_dhcpv4_handle
        if 'v6' in kwargs['type']:
            handle = subscriber.rt_dhcpv6_handle
        result = rt_handle.invoke('emulation_dhcp_stats', mode='session', handle=handle)
        if result['status'] == '1':
            for item in result['session']:
                if 'v4' in kwargs['type']:
                    address.append(result['session'][item]['Address'])
                if 'v6' in kwargs['type']:
                    address.append(result['session'][item]['Prefix'])
        else:
            raise Exception("failed to get dhcp stats from rt for sub {}".format(subscriber))

    return address


def get_interface_from_address(**kwargs):
    """
    get interface name from address
    :param kwargs:
    device_id:              router id, default is 'r0'
    address(Mandatory):     ip address
    :return:
    """
    t.log("inside get_interface_from_address, kwargs is {}".format(kwargs))
    _check_bbe()
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router_handle = t.get_handle(device_id)
    resps = router_handle.pyez('get-subscribers', address=kwargs['address'], timeout=600).resp
    for resp in resps.findall('subscriber'):
        if resp.findtext('ip-address') == kwargs['address']:
            return resp.findtext('interface')
    raise Exception("no interface was found for the address")

def start_rt_links(**kwargs):
    """
    start tester uplinks and custom links
    :param kwargs:
    rt_device_id:           e.g. rt0
    uplinks:                uplink interface id list, e.g.['uplink0','uplink1']

    :return:
    """
    t.log("inside start_rt_links, kwargs is {}".format(kwargs))
    _check_bbe()
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device_id)
    uplinks = bbe.get_interfaces(rt_device_id, interfaces='uplink', id_only=False)
    customs = bbe.get_interfaces(rt_device_id, interfaces='custom', id_only=False)
    uplinks += customs
    if 'uplinks' in kwargs:
        uplinks = kwargs['uplinks']
    for uplink in uplinks:
        connection = bbe.get_connection(rt_device_id, uplink.interface_id)
        if connection.is_ae:
            if 'ip' not in connection.interface_config and 'ipv6' not in connection.interface_config:
                continue
        if uplink.device_id != rt_device_id:
            t.log("uplink {} is not on this rt {}, skipping".format(uplink, rt_device_id))
            continue
        tester.invoke('link_action', handle=uplink.rt_device_group_handle, action='start')
        time.sleep(2)


def print_cst_stats():
    """
    print out bbe.cst_stats in a readable format
    :return:
    """
    for key, value in sorted(bbe.cst_stats.items()):
        if isinstance(value, dict):
            print("{0:_^40}".format(key))
            _myprint(value)
        else:
            print("{0:.<40}{1:1}".format(key, value))


def _myprint(data):
    """
    print out a dictionary
    :param data:
    :return:
    """
    for key, value in sorted(data.items()):
        if isinstance(value, dict):
            print("{0:_^40}".format(key))
            _myprint(value)
        else:
            print("   {0:.<36}{1:1}".format(key, value))


def panic_re_recover(**kwargs):
    """
    panic RE and then reset
    :param kwargs:
    host:           console hostname or console ip
    tomcat_mode:        True/False
    :return:
    """
    t.log("inside panic_re_recover, kwargs is {}".format(kwargs))
    _check_bbe()
    host = kwargs['host']
    tomcat_mode = kwargs.get('tomcat_mode', True)
    try:
        console_device = Device(host=host, user='root', password='Embe1mpls', connect_targets='console', model='JUNOS')
    except:
        raise Exception("failed to login to console")
    if tomcat_mode:
        console_device.shell(command=('~' + chr(int(2))), pattern='(.*)')
    else:
        console_device.shell(command=chr(int(29)), pattern='(.*)')
        time.sleep(1)
        console_device.shell(command='send break', pattern='(.*)')
    time.sleep(10)
    console_device.shell(command='reset', pattern='(.*)')


def power_manager(**kwargs):
    """
    Power down/up/cycle the chassis via the terminal server port
    power_manager(chassis='firebee', action='off');
    power_manager(chassis='firebee', action='on');
    power_manager(chassis='firebee', action='cycle');
    Example:
       a. telnet firebee-con
       b. ctrl ^
       c. This will bring up the menu screen below:
          r    reboot device using power-switch
          p/-  power device off
          p/+  power device on
    :param kwargs:
    chassis:                chassis name
    action:                 action name, must be one of the values of 'on', 'off', 'cycle'
    :return:
    """
    t.log("inside power_manager, kwargs is {}".format(kwargs))
    host = kwargs['chassis'] + '-con'
    action = kwargs.get('action', 'cycle')
    import pexpect

    console_device = pexpect.spawn('telnet {}'.format(host))
    console_device.sendcontrol('^')
    time.sleep(1)
    if action in ['on', 'off']:
        console_device.send('p')

    elif action == 'cycle':
        console_device.send('r')
    time.sleep(1)
    console_device.send('y')


def verify_client_count(**kwargs):
    """
    verify client count for router

    :param kwargs:
    device_id                       dut router name, e.g. 'r0'
    subs                            subs object
    base_subs_count                 base subscriber count
    base_route_count                base access route count
    :return:
    """
    t.log("inside verify_client_count, kwargs is {}".format(kwargs))
    if 'device_id' in kwargs:
        device_ids = kwargs['device_id']
        if not isinstance(device_ids, list):
            device_ids = [device_ids]
    else:
        device_ids = bbe.get_devices(device_tags='dut', id_only=True)

    check_access_route = kwargs.get('check_access_route', True)
    base_subs_count = kwargs.get('base_subs_count', 0)
    base_route_count = kwargs.get('base_route_count', 0)
    if 'subs' in kwargs:
        subs_list = kwargs['subs']
        result = get_configured_subs(device_id=device_ids, subs=subs_list)
    else:
        result = get_configured_subs(device_id=device_ids)
    t.log('configured subs info {}'.format(result))
    status = True
    total_active_client = 0
    total_active_route = 0
    for router_id in device_ids:
        summary = get_router_sub_summary(router_id)
        if 'init' in summary or 'terminated' in summary or 'configured' in summary or 'terminating' in summary:
            t.log('WARN', "some subscribers in abnormal state {} ".format(summary))
            time.sleep(30)
        route_sum = get_route_summary(router_id)
        t.log('router {} subscriber summary: {}, route {}'.format(router_id, summary, route_sum))
        ##check client count and route count
        if router_id in bbe.defined_sub_info:
            if summary['client'] == bbe.defined_sub_info[router_id]['count-in-router']:
                t.log('subscriber in router {} match the defined number {}'.format(router_id, summary['client']))
            else:
                t.log('WARN', 'subscriber in router {} does not match the '
                              'defined number {}'.format(router_id, summary['client']))
                status = False
            if verify_utils.convert_str_to_num_or_bool(check_access_route):
                if route_sum == bbe.defined_sub_info[router_id]['route-count']:
                    t.log('access route in router {} match the defined number {}'.format(router_id, route_sum))
                else:
                    t.log('WARN', 'access route in router {} does not match '
                                  'the defined number {}'.format(router_id, route_sum))
                    status = False

        total_active_client += summary['client']
        total_active_route += route_sum
    expected_client = result['expected_total_session_in_routers'] + base_subs_count
    if total_active_client == expected_client:
        t.log('all subscribers {} login successfully'.format(total_active_client))
    else:
        t.log('WARN', 'expected subscriber {}, login {}'.format(expected_client, total_active_client))
        status = False

    if verify_utils.convert_str_to_num_or_bool(check_access_route):
        expected_route = result['expected_route_count'] + base_route_count
        if total_active_route == expected_route:
            t.log('all access route {} exists'.format(total_active_route))
        else:
            t.log('WARN', 'expected route {}, actual route {}'.format(expected_route, total_active_route))
            status = False
    if not status:
        raise Exception('failed in subscriber count verification')


def verify_client_route(**kwargs):
    """
    verify the client count and access route count in routers

    :param kwargs:
    device_id                       dut router name
    subs                            subs object
    base_route_count                base route count
    :return:
    """
    t.log("inside verify_client_route, kwargs is {}".format(kwargs))
    if 'device_id' in kwargs:
        device_ids = kwargs['device_id']
        if not isinstance(device_ids, list):
            device_ids = [device_ids]
    else:
        device_ids = bbe.get_devices(device_tags='dut', id_only=True)

    base_route_count = kwargs.get('base_route_count', 0)
    print("base route count is", base_route_count)

    if 'subs' in kwargs:
        subs_list = kwargs['subs']
        if not isinstance(subs_list, list):
            subs_list = [subs_list]
        result = get_configured_subs(device_id=device_ids, subs=subs_list)
    else:
        result = get_configured_subs(device_id=device_ids)
    t.log('configured subs info {}'.format(result))
    status = False

    route_verified_count = 0
    total_active_route = 0
    for router_id in device_ids:
        summary = get_router_sub_summary(router_id)
        route_sum = get_route_summary(router_id)
        t.log('router {} subscriber summary: {}, route {}'.format(router_id, summary, route_sum))
        ##check client count and route count
        if router_id in bbe.defined_sub_info:
            route_verified_count = 1
            if route_sum == bbe.defined_sub_info[router_id]['route-count']:
                t.log('access route in router {} match the defined number {}'.format(router_id, route_sum))
                status = True
            else:
                t.log('ERROR', 'access route in router {} does not match '
                               'the defined number {}'.format(router_id, route_sum))
                status = False
                break
        total_active_route += route_sum

    if not route_verified_count:
        expected_route = result['expected_route_count'] + base_route_count
        if total_active_route == expected_route:
            t.log('all access route {} exists'.format(total_active_route))
            status = True
        else:
            t.log('ERROR', 'expected route {}, actual route {}'.format(expected_route, total_active_route))
            status = False
    if not status:
        raise Exception('failed in access route count verification')


def prepare_for_concurrent_test(**kwargs):
    """
    preparation actions before concurrent login/logout test
    :param kwargs:
    background_subs:   background subs list which is running in the background
    group_a:           one of the login/logout group list
    retry:             login restart retry
    verify_traffic:    verify background traffic in each iteration
    cpu_settle:        cpu usage before next iteration
    iteration:         iteration count, default is 10
    inflight_enable:   True/False
    :return:

    """
    # inflight_enable = kwargs.get('inflight_enable', False)
    # if not inflight_enable:
    t.log("inside prepare_for_concurrent_test, kwargs is {}".format(kwargs))
    _check_bbe()
    result = dict()
    prepare_router_before_login()
    try:
        cst_start_clients(restart_unbound_only=True, **kwargs)
    except Exception:
        t.log("start clients with restart_unbound failed with exception")
        cst_start_clients(**kwargs)

    if 'subs' in kwargs:
        subs_list = kwargs['subs']
        if not isinstance(subs_list, list):
            subs_list = [subs_list]
        kwargs.pop('subs')
    else:
        subs_list = bbe.get_subscriber_handles()

    if 'background_subs' in kwargs:
        background_subs = kwargs['background_subs']
    else:
        if len(subs_list) < 2:
            raise Exception("subscriber groups must be greater than 1")
        if len(subs_list) == 2:
            t.log("only 2 subscriber groups in this concurrent test")
            background_subs = []
        else:
            ##take 20% subs as the background sub
            bg_sub_counts = math.ceil(len(subs_list) * 0.2)
            background_subs = random.sample(subs_list, bg_sub_counts)
    subs_list = [subs for subs in subs_list if subs not in background_subs]
    result['background_group'] = background_subs
    if 'group_a' in kwargs:
        group_a = kwargs['group_a']
    else:
        group_a_count = round(len(subs_list) / 2)
        group_a = random.sample(subs_list, group_a_count)
    result['logout_group'] = group_a
    group_b = [subs for subs in subs_list if subs not in group_a]
    result['login_group'] = group_b
    t.log('background group {}, initial logout group {}, '
          'initial login group {}'.format(background_subs, group_a, group_b))
    # check subs state in each group
    background_subs_handle = []
    group_a_handle = []
    group_b_handle = []
    for subs in background_subs:
        background_subs_handle.append(subs.rt_ethernet_handle)

    for subs in group_a:
        group_a_handle.append(subs.rt_ethernet_handle)

    for subs in group_b:
        group_b_handle.append(subs.rt_ethernet_handle)

    t.log('background group {}, initial logout group {}, '
          'initial login group {}'.format(background_subs_handle, group_a_handle, group_b_handle))

    device = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    cst_release_clients(subs=group_b, device_id=device)
    verify_traffic_enable = kwargs.get('verify_traffic', True)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        add_subscriber_mesh(subs=background_subs, **kwargs)
        t.log('starting background traffic')
        start_traffic(**kwargs)

    return result


class _CstStatsAddon:
    """Maintains tester added cst stats to be published.

    """
    def __init__(self):
        self.csa_dict = dict()

    def csa_add(self, k, v):
        self.csa_dict[k] = v

    def csa_clear(self):
        self.csa_dict.clear()

    def csa_get(self):
        return self.csa_dict


# create an instance such that addon cst result callers
# don't bother to get an class handle
_cst_stats_addon_inst = _CstStatsAddon()


def add_addon_cst_result(result_key, result_value):
    """Add a CST result key value pair to the CST addon result.

    This function can be called more than one times to add different results
    Keyword usage example:
        Add Addon CST Result    result_key=pfe_cps    result_value=200

    :param result_key: CST result key.
    :param result_value: CST result value
    :return: None
    """
    _cst_stats_addon_inst.csa_add(result_key, result_value)


def clear_addon_cst_result():
    """Clear all addon CST results (empty result dict).

    CLear addon CST results if previous addon result is not to be published.
    Supposed to be called between two publish_cst_result calls if needed.
    :return: None
    """
    _cst_stats_addon_inst.csa_clear()


def get_addon_cst_result():
    """Get all addon CST results.

    :return: CST addon result dictionary
    """
    return _cst_stats_addon_inst.csa_get()


def publish_cst_result(**kwargs):
    """Generate publish scripts for CST, that user can use the generated publish file to upload cst results

    :param kwargs:
        flows_per_sub: Number of flows per subscriber.
                       When a int or string representation of int is given, it is converted to float internally.
                       When flows_per_sub is present with > 0 value, scaling publish will process
                       pfe_flow_stats.log with the given number of flows per subscriber.
                       Default is 0, which will not process pfe_flow_stats.log.
    :return:
    """
    # import getpass
    # user = getpass.getuser()
    print_cst_stats()
    tv_dict = tv['uv-bbevar']['test']
    tv_bbevar = tv['uv-bbevar']
    bbe.cst_stats['tester'] = os.environ['LOGNAME']
    bbe.cst_stats['test_date'] = str(datetime.date.today())
    current_time = str(round(time.time()))
    bbe.cst_stats['test_id'] = current_time + '_' + str(os.getpid())
    timenow = str(datetime.datetime.now()).replace(' ', '_')
    if tv_dict['type'] == 'customer':
        upload_path = '/volume/wf-cst/cst_log/' + t._script_name + '/' + str(datetime.date.today()) + '/'
        bbe.cst_stats['customer_id'] = tv_dict['id']
        bbe.cst_stats['customer'] = tv_dict['id']
    elif tv_dict['type'] == 'scaling':
        upload_path = '/volume/wf-cst/cst_log/ScalePerf/' + \
                      tv_dict['scaling-performance-model'] + '/' + timenow + '/'
    else:
        t.log('not a cst test, no publish is needed')
        return
    if 'l2tp' in tv_bbevar:
        bbe.cst_stats['target_l2tp_tunnel_count'] = tv_bbevar['l2tp']['l2tp-tunnels-count']
        bbe.cst_stats['target_total_number_of_l2tp_subscribers'] = tv_bbevar['l2tp']['total-number-of-subscribers']

    if 'pseudowire' in tv_bbevar:
        bbe.cst_stats['target_number_of_pseudowire'] = tv_bbevar['pseudowire']['number-of-pseudowires']

    bbe.cst_stats['tag'] = tv_dict['description']
    bbe.cst_stats['dhcp_server_type'] = tv_bbevar['dhcpserver']['ipv4']['mode']
    bbe.cst_stats['address_type'] = tv_dict['address-type']

    if 'ae' in tv_dict:
        bbe.cst_stats['ae'] = tv_dict['ae']
    if 'dpc-type' in tv_dict:
        bbe.cst_stats['dpc_type'] = tv_dict['dpc-type']
    if 'vlan-model' in tv_dict:
        bbe.cst_stats['vlan_model'] = tv_dict['vlan-model']
    if 'vlan-setup-type' in tv_dict:
        bbe.cst_stats['vlan_setup_type'] = tv_dict['vlan-setup-type']
    if 'vlan-tagging-type' in tv_dict:
        bbe.cst_stats['vlan_tagging_type'] = tv_dict['vlan-tagging-type']
    if 'lns-cluster' in tv_dict:
        bbe.cst_stats['lns_cluster'] = tv_dict['lns-cluster']
    if 'mcast' in tv_dict:
        bbe.cst_stats['mcast'] = tv_dict['mcast']
    if 'ppp-access-model' in tv_dict:
        bbe.cst_stats['ppp_access_model'] = tv_dict['ppp-access-model']
    if 'ppp-setup-type' in tv_dict:
        bbe.cst_stats['ppp_setup_type'] = tv_dict['ppp-setup-type']
    if 'dhcp-access-model' in tv_dict:
        bbe.cst_stats['dhcp_access_model'] = tv_dict['dhcp-access-model']
    if 'subscribers-per-vlan' in tv_dict:
        bbe.cst_stats['attempted_subscribers_per_vlan'] = tv_dict['subscribers-per-vlan']
    if 'scaling-performance-model' in tv_dict:
        bbe.cst_stats['scaling_performance_model'] = tv_dict['scaling-performance-model']
    if 'vlan-count' in tv_dict:
        bbe.cst_stats['attempted_vlans'] = tv_dict['vlan-count']
    if 'lac-l2tp' in tv_dict:
        bbe.cst_stats['LAC_l2tp'] = tv_dict['lac-l2tp']
    if 'lac-l2tp-tunnel' in tv_dict:
        bbe.cst_stats['LAC_l2tp_tunnel'] = tv_dict['lac-l2tp-tunnel']
    if 'lac-l2tp-tunnel-session' in tv_dict:
        bbe.cst_stats['LAC_l2tp_tunnel_session'] = tv_dict['lac-l2tp-tunnel-session']
    if 'lns-l2tp' in tv_dict:
        bbe.cst_stats['LNS_l2tp'] = tv_dict['lns-l2tp']
    if 'lns-l2tp-tunnel' in tv_dict:
        bbe.cst_stats['LNS_l2tp_tunnel'] = tv_dict['lns-l2tp-tunnel']
    if 'lns-l2tp-tunnel-session' in tv_dict:
        bbe.cst_stats['LNS_l2tp_tunnel_session'] = tv_dict['lns-l2tp-tunnel-session']
    script = t._script_name
    bbe.cst_stats['test_log_file'] = upload_path + script + '_log.html'
    bbe.cst_stats['test_report_file'] = upload_path + script + '_report.html'
    bbe.cst_stats['resource_usage_summary'] = 'http://eabu-sssp-orig.englab.juniper.net/cst_results/' + \
                                              script + '/' + str(datetime.date.today()) + '/performance/'
    if tv_dict['type'] == 'scaling':
        bbe.cst_stats['resource_usage_summary'] = 'http://eabu-sssp-orig.englab.juniper.net/cst_results/' + \
                                                  'ScalePerf/' + tv_dict['scaling-performance-model'] + \
                                                  '/' + timenow + '/performance/'

    # Merge with cst addon result
    bbe.cst_stats.update(get_addon_cst_result())

    element = dict_to_xml('opt', bbe.cst_stats)
    dom = parseString(tostring(element))
    create_time = current_time
    if 'image' not in bbe.cst_stats:
        get_configured_subs()
    logdir = t._log_dir
    stats_filename = create_time + '_' + bbe.cst_stats['image'] + '_Final_Stats_' + str(os.getpid()) + '.xml'
    monitor_path2 = logdir + '/' + bbe.cst_stats['dut'] + '/'
    with open(logdir + '/' + stats_filename, 'w') as file:
        file.write(dom.toprettyxml())
    file.close()
    loginname = os.getlogin()
    ##create shell publish/unpublish script
    test_id = "{}_{}".format(create_time, str(os.getpid()))
    publish_file = create_time + '_publish_' + str(os.getpid())
    with open(logdir + '/' + publish_file, 'w') as file1:
        file1.write("#!/bin/bash\n")
        file1.write('echo "Publishing {} {}"\n'.format(bbe.cst_stats['test_log_file'], stats_filename))
        file1.write("mkdir -p {}\n".format(upload_path + 'performance'))
        file1.write('echo "Copying {} to {}" \n'
                    ''.format(logdir + '/' + script + "_log.html", bbe.cst_stats['test_log_file']))
        file1.write("cp {} {}\n".format(script + "_log.html", upload_path))
        file1.write("cp {} {}\n".format(script + '.log', upload_path))
        file1.write('echo "Copying {} to {}"\n'
                    ''.format(logdir + '/' + script + '_report.html', bbe.cst_stats['test_report_file']))
        file1.write("cp {} {}\n".format(script + "_report.html", upload_path))
        file1.write('echo "Copying {} to {}"\n'.format(logdir + '/' + stats_filename, upload_path + stats_filename))
        file1.write("cp {} {}\n".format(stats_filename, upload_path))
        file1.write('echo "Copying performance monitor files {} to {}"\n'.format(monitor_path2, upload_path))
        file1.write("cp -rf {}/* {}\n".format("monitor_data/" + bbe.cst_stats['dut'], upload_path + 'performance'))
        file1.write("chmod -R 777 {}\n".format(upload_path))
        file1.write('echo "Adding test result into database"\n')
        file1.write("/volume/perl/bin/perl /volume/labtools/lib/Testsuites/CommonEdge/SSSI/test_result_mysql_util.pl "
                    "-action=add -xml_file={} -logdir={}\n".format(stats_filename, upload_path))
        if tv_dict['type'] == 'scaling':
            filename = script + '.pl'
            # obtain flows per subscriber, default is 0.0
            fps = float(kwargs.get('flows_per_sub', 0))

            file1.write("cp r0re0/*_era_*.log {}\n".format(upload_path))
            if fps > 0:
                file1.write("cp r0re0/pfe_flow_stats* {}\n".format(upload_path))
            file1.write('echo "Post processing log files, ERA files, and messages"\n')
            if fps > 0:
                file1.write("ssh {}@wfd-smoketest 'perl /homes/mcorbin/bin/scalePerfPostProcess.pl"
                        " -r {} -p {} -l {} -f {}'\n".format(loginname, upload_path, os.getpid(), filename, fps))
            else:
                file1.write("ssh {}@wfd-smoketest 'perl /homes/mcorbin/bin/scalePerfPostProcess.pl"
                            " -r {} -p {} -l {}'\n".format(loginname, upload_path, os.getpid(), filename))
        file1.close()

    unpublish_file = create_time + '_unpublish_' + str(os.getpid())
    with open(logdir + '/' + unpublish_file, 'w') as file2:
        file2.write("#!/bin/bash\n")
        file2.write('echo "unpublishing {} {}"\n'.format(bbe.cst_stats['test_log_file'], stats_filename))
        file2.write('echo "delete dir {}"\n'.format(upload_path))
        file2.write("rm -rf {}\n".format(upload_path))
        file2.write('echo "remove test from database"\n')
        file2.write("/volume/perl/bin/perl /volume/labtools/lib/Testsuites/CommonEdge/SSSI/test_result_mysql_util.pl "
                    "-action=delete -test_id={} -logdir={}\n".format(test_id, upload_path))
        file2.close()
    import subprocess
    subprocess.call(['chmod', '0755', logdir + '/' + publish_file])
    subprocess.call(['chmod', '0755', logdir + '/' + unpublish_file])


def dict_to_xml(tag, data):
    """
    Turn a simple dict of key/value pairs into XML
    :param tag:                 xml tag
    :param d:                   data
    :return:
    """
    elem = Element(tag)
    for key, val in data.items():

        if isinstance(val, dict):
            elem.append(dict_to_xml(key, val))
        else:
            child = Element(key)
            child.text = str(val)
            elem.append(child)
    return elem


def check_re_status(**kwargs):
    """
    waiting for re to come back online after reboot/crash/powercycle
    :param kwargs:
    retries:            retry count, default is 15
    re_slot:            '0'/'1', for single router only
    device_id:          e.g. default is 'r0'
    :return:
    """
    t.log("inside check_re_status, kwargs is {}".format(kwargs))
    _check_bbe()
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    if 're_slot' in kwargs:
        re_slot = kwargs['re_slot']
        picked_re = 're' + re_slot
        resp = router.pyez('get_route_engine_information', slot=re_slot, timeout=600).resp
    else:
        resp = router.pyez('get_route_engine_information', timeout=600).resp
        picked_re = 'all REs'

    retry = kwargs.get('retries', 15)
    ready = True
    while True:
        if hasattr(router, 'vc') and router.vc:
            status_list = resp.findall('multi-routing-engine-item/route-engine-information/route-engine')
        else:
            status_list = resp.findall('route-engine')
        for status in status_list:
            if status.findtext('status') != 'OK':
                picked_re = 're' + status.findtext('slot')
                t.log("waiting 30s for re {} come back".format(picked_re))
                time.sleep(30)
                ready = False
                break
        if ready:
            break
        resp = router.pyez('get_route_engine_information', timeout=600).resp
        ready = True
        retry -= 1
        if not retry:
            raise Exception("re {} failed to come back".format(picked_re))
    t.log("re {} come back online".format(picked_re))


def clear_subscribers_in_router(**kwargs):
    """
    clear subscribers
    :param kwargs:
    device_id:                          e.g. 'r0'
    type:                               dhcp/pppoe/all
    routing_instance:                   routing instance name,
    retry:                              retry count, default is 10
    :return:
    """
    t.log("inside clear_subscribers_in_router, kwargs is {}".format(kwargs))
    device_id = kwargs.get('device_id', 'r0')
    router = t.get_handle(device_id)
    sub_type = kwargs.get('type', 'all')
    ri_name = kwargs.get('routing_instance', 'default')
    if sub_type == 'all':
        sub_type = ['dhcp', 'pppoe', 'l2tp']
    else:
        sub_type = [sub_type]
    for subs in sub_type:
        if subs == 'dhcp':
            router.cli(command='clear dhcp server binding all routing-instance {}'.format(ri_name))
            router.cli(command='clear dhcpv6 server binding all routing-instance {}'.format(ri_name))
            router.cli(command='clear dhcp relay binding all routing-instance {}'.format(ri_name))
            router.cli(command='clear dhcpv6 relay binding all routing-instance {}'.format(ri_name))
        if subs == 'pppoe':
            router.cli(command='clear pppoe sessions no-confirm')
        if subs == 'l2tp':
            router.cli(command='clear services l2tp session all')
            router.cli(command='clear services l2tp tunnel all')
    router.cli(command='clear auto-configuration interfaces ps0')
    router.cli(command='clear auto-configuration interfaces demux0')

    retry = kwargs.get('retry', 10)
    count = 0
    last_active_subs_in_router = 0
    while True:
        t.log('waiting for clients to release from router')
        result = get_router_sub_summary(device_id)
        t.log('router {} subscriber summary: {}'.format(device_id, result))
        total_active_subs_in_router = result['total']
        delta_active_subs = total_active_subs_in_router - last_active_subs_in_router
        if delta_active_subs != 0:
            t.log('it is still releasing clients, waiting for 10s')
            time.sleep(10)
            last_active_subs_in_router = total_active_subs_in_router
            continue
        else:
            count += 1

        if total_active_subs_in_router == 0:
            t.log("all subscribers logout")
            break

        retry = retry - 1
        if retry == 0:
            t.log('warning, not all subscribers logout after retry waiting cycle, rebooting router now')
            router.reboot(wait=200, mode='cli', all=True)
            router.reconnect(all)
            if (hasattr(router, 'vc') and not router.vc) or (not hasattr(router, 'vc')):
                master_re = get_master_re_name(device_id)
                router.set_current_controller(controller=master_re, system_node='primary')

            check_fpc(**kwargs)
            break


def get_ae_info(**kwargs):
    """
    get ae information for router or tester(rt0)
    :param kwargs:
    device_id:     device id name e.g. 'r0'
    :return:
    """
    t.log("inside get_ae_info, kwargs is {}".format(kwargs))
    _check_bbe()
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])

    ae_members = dict()
    links = bbe.get_interfaces(device_id)
    for link in links:
        connection = link
        if 'rt' in device_id:
            connection = bbe.get_connection(device_id, link.interface_id)
        if connection.is_ae:
            ae_name = connection.ae_bundle
            if ae_name not in ae_members:
                ae_members[ae_name] = dict()
            if connection.is_ae_active:
                if 'active' not in ae_members[ae_name]:
                    ae_members[ae_name]['active'] = []
                ae_members[ae_name]['active'].append(link.interface_pic)
            else:
                if 'standby' not in ae_members[ae_name]:
                    ae_members[ae_name]['standby'] = []
                ae_members[ae_name]['standby'].append(link.interface_pic)
    t.log("AE interfaces is {}".format(ae_members))
    return ae_members


def prepare_subscriber_traffic(**kwargs):
    """
    used for prepare subscriber and traffic verification before a testcase
    :param kwargs:
    device_id:          router device id , e.g. 'r0'
    rt_device_id;       tester device id, e.g. 'rt0'
    new_mesh:           create a new traffic mesh, default it true
    verify_traffic:     verify traffic in the test, default is true
    :return:
    """
    t.log("inside prepare_subscriber_traffic, kwargs is {}".format(kwargs))
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device_id)
    subs = kwargs.get('subs', bbe.get_subscriber_handles())
    t.log('start login subs {} before test'.format(subs))
    try:
        cst_start_clients(restart_unbound_only=True, **kwargs)
    except Exception:
        t.log("got exception with restart_unbound_only, will try login without this arg")
        cst_start_clients(**kwargs)
    verify_traffic_enable = kwargs.get('verify_traffic', True)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        new_mesh = kwargs.get('new_mesh', True)
        duration = kwargs.get('duration', 60)
        if new_mesh:
            t.log('remove existing traffic mesh')
            tester.invoke('traffic_action', action='stop')
            time.sleep(15)
            tester.invoke('traffic_action', action='delete')
            time.sleep(5)
            t.log('add new traffic mesh for subs')
            add_subscriber_mesh(**kwargs)
        if 'duration' in kwargs:
            start_traffic(**kwargs)
        else:
            start_traffic(duration=duration, **kwargs)
        time.sleep(int(duration))
        stop_traffic()
        verify_traffic(**kwargs)


def get_dirty_table(**kwargs):
    """
    Looks for backup RE dirty table count
    vty -s 7208 128.0.0.5 (single RE)
    vty -s 7208 161.0.0.6 (MXVC)
    show dirty-table all
    :param kwargs:
    :return:        dirty table count eg.9
    """
    t.log("inside get_dirty_table, kwargs is {}".format(kwargs))
    _check_bbe()
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    command = kwargs.get('command', "show dirty-table all")
    if hasattr(router, 'vc') and router.vc:
        resp = router.execute_command(mode='bbevty_sla', command=command).resp
    elif get_master_re_name(device_id) == 're1':
        resp = router.execute_command(mode='bbevty_pri', command=command).resp
    else:
        resp = router.execute_command(mode='bbevty_sla', command=command).resp

    if re.search('No Object found', resp):
        count = -1
    else:
        match = re.match(r'.*Walk Count = (\d+)', resp, flags=re.MULTILINE|re.DOTALL)
        count = int(match.group(1))
    return count


def check_fpc(**kwargs):
    """
    check if fpc state to be online, raise exception if not
    :param kwargs:
    slot:                   slot number list(string type), default is to check all slots
    device_id:              e.g. default is 'r0'
    fpc_wait_time:          wait time for FPC to come up, default is 600s - increase it to more than 600s only after making sure it is not a software/hardware issue
    :return:
    """
    t.log("inside check_fpc, kwargs is {}".format(kwargs))
    device_id = kwargs.get('device_id', 'r0')
    fpc_wait_time = int(kwargs.get('fpc_wait_time', 600))
    router = t.get_handle(device_id)
    mxvc = False
    max_slots = 0
    if hasattr(router, 'vc') and router.vc:
        mxvc = True
        resp = router.shell(command='sysctl hw.product.router_max_fpc_slots').resp
        max_slots = round(int(resp.split()[1]) / 2)
    comment_list = ["Configured power off", "Unsupported FPC", "FPC incompatible with SCB"]
    slot_to_check = kwargs.get('slot', [])
    online_slot = []
    if not slot_to_check:
        resp = router.pyez('get_fpc_information', timeout=600).resp
        all_fpc_info = resp.findall('fpc')
        if mxvc:
            all_fpc_info = resp.findall('multi-routing-engine-item/fpc-information/fpc')
        for fpc_info in all_fpc_info:
            state = fpc_info.findtext('state')
            slot = fpc_info.findtext('slot')
            if slot in slot_to_check or slot in online_slot:
                slot = str(int(slot) + max_slots)
            dram_size = fpc_info.findtext('memory-dram-size')
            if state == 'Empty':
                continue
            t.log("fpc {} state is {}".format(slot, state))
            if state == 'Offline' and fpc_info.findtext('comment') in comment_list:
                t.log("fpc {} was {}".format(slot, fpc_info.findtext('comment')))
                continue
            if state != 'Online':
                slot_to_check.append(slot)
                t.log("current slot_to_check is {}".format(slot_to_check))
            else:
                if not dram_size or dram_size == '0':
                    slot_to_check.append(slot)
                else:
                    online_slot.append(slot)
    base_time = time.time()
    t.log("the slots needed to be checked is {}".format(slot_to_check))
    while True:
        if slot_to_check:
            slots = slot_to_check.copy()
            for slot in slots:
                state = 'fpc/state'
                comment = 'fpc/comment'
                dram = 'fpc/memory-dram-size'
                if mxvc:
                    state = 'multi-routing-engine-item/fpc-information/fpc/state'
                    comment = 'multi-routing-engine-item/fpc-information/fpc/comment'
                    dram = 'multi-routing-engine-item/fpc-information/fpc/memory-dram-size'
                    if int(slot) < max_slots:
                        resp = router.pyez('get_fpc_information', member='0', fpc_slot=slot, timeout=600).resp
                    else:
                        newslot = str(int(slot) - max_slots)
                        resp = router.pyez('get_fpc_information', member='1', fpc_slot=newslot, timeout=600).resp
                else:
                    resp = router.pyez('get_fpc_information', fpc_slot=slot, timeout=600).resp

                if resp.findtext(state) == 'Online':
                    dram_size = resp.findtext(dram)
                    t.log("slot {} dram_size is {}".format(slot, dram_size))
                    if dram_size and dram_size != '0':
                        slot_to_check.remove(slot)
                        online_slot.append(slot)
                elif resp.findtext(state) == 'Offline' and resp.findtext(comment) in comment_list:
                    slot_to_check.remove(slot)
        else:
            t.log("all fpcs {} are online now".format(online_slot))
            break
        if time.time() - base_time > fpc_wait_time:
            raise Exception("FPCs failed to be online after {} seconds".format(fpc_wait_time))
        if slot_to_check:
            time.sleep(30)
    return online_slot


def get_pic_info(device_id='r0'):
    """
    get the online pic and slot info, in the format of dictionary,
    e.g. {'0': ['0', '1', '2', '3', 'MPC Type 2 3D EQ'], '1': ['0', '1', 'MPC Type 2 3D EQ']}
    :param device_id:                   route id, e.g. 'r0'
    :return:                            dictionary of slot and pic of online
    """
    t.log("inside get_pic_info, kwargs is {}".format(device_id))
    _check_bbe()
    result = {}
    router = t.get_handle(device_id)
    resp = router.pyez('get_pic_information', timeout=600).resp
    all_fpc_info = resp.findall('fpc')
    if hasattr(router, 'vc') and router.vc:
        for engine in resp.findall('multi-routing-engine-item'):
            member_name = engine.findtext('re-name')
            result[member_name] = {}
            for fpc_info in engine.findall('fpc-information/fpc'):
                slot = fpc_info.findtext('slot')
                state = fpc_info.findtext('state')
                fpc_type = fpc_info.findtext('description')
                if state != 'Online':
                    t.log("Warning, {} slot {} state is {}".format(member_name, slot, state))
                    continue
                pic_list = []
                for pic_info in fpc_info.findall('pic'):
                    pic_slot = pic_info.findtext('pic-slot')
                    pic_state = pic_info.findtext('pic-state')
                    if pic_state != 'Online':
                        t.log('Warning, {} slot {} pic {} state is {}'.format(member_name, slot, pic_slot, pic_state))
                        continue
                    pic_list.append(pic_slot)
                pic_list.append(fpc_type)
                result[member_name][slot] = pic_list
    else:
        for fpc_info in all_fpc_info:
            slot = fpc_info.findtext('slot')
            state = fpc_info.findtext('state')
            fpc_type = fpc_info.findtext('description')
            if state != 'Online':
                t.log("Warning, slot {} state is {}".format(slot, state))
                continue
            pic_list = []

            for pic_info in fpc_info.findall('pic'):
                pic_slot = pic_info.findtext('pic-slot')
                pic_state = pic_info.findtext('pic-state')
                if pic_state != 'Online':
                    t.log('Warning, slot {} pic {} state is {}'.format(slot, pic_slot, pic_state))
                    continue
                pic_list.append(pic_slot)
            pic_list.append(fpc_type)
            result[slot] = pic_list

    return result


def get_vcp_ports(**kwargs):
    """
    get vcp port info
    :param kwargs:
    device_id:      device id name e.g. 'r0'
    :return: port dictionary
    """
    t.log("inside get_vcp_ports, kwargs is {}".format(kwargs))
    _check_bbe()
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    resp = router.pyez('get_virtual_chassis_port_information', timeout=600).resp
    port_dict = {}
    for member in resp.findall('multi-routing-engine-item'):
        chassis_name = member.findtext('re-name')
        info_list = member.findall('virtual-chassis-port-information/port-list/port-information')
        port_list = []
        for port_info in info_list:
            port = 'vcp-' + port_info.findtext('port-name')
            port_state = port_info.findtext('port-status').lower()
            if port_state != 'up':
                t.log('WARN', "vcp port {} state is {}".format(port, port_state))
                continue
            if port not in port_list:
                port_list.append(port)
        port_dict[chassis_name] = port_list
    return port_dict


def get_session_ids(**kwargs):
    """
    get session ids or interfaces
    :param kwargs:
    device_id:                  device id name e.g. 'r0'
    client_type:                client type , dhcp/pppoe/l2tp/gre, default is dhcp
    return_session_detail:      True/False, default is False , when True, return xml element array,
                                [<Element subscriber at 0x15f6a1308>]

    :return:
    """
    t.log("inside get_session_ids, kwargs is {}".format(kwargs))
    _check_bbe()
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    client_type = kwargs.get('client_type', 'dhcp')
    resp = router.pyez('get_subscribers', client_type=client_type, display='detail', timeout=1200).resp
    return_detail = kwargs.get('return_session_detail', False)
    detail_sessions = resp.findall('subscriber')
    if return_detail:
        return detail_sessions
    session_ids = []
    for subscriber in detail_sessions:
        session_id = subscriber.findtext('session-id')
        if session_id:
            session_ids.append(session_id)
        else:
            t.log('WARN', "no session id was found in this subscriber {}".format(subscriber))

    if not session_ids:
        raise Exception("no session id was found for the check")

    if 'count' in kwargs:
        new_list = []
        for item in range(0, int(kwargs['count'])):
            while True:
                newid = random.choice(session_id)
                if newid not in new_list:
                    new_list.append()
                    break
        session_ids = new_list

    return session_ids


def clear_subscriber_sessions(**kwargs):
    """
    clear_subscriber_sessions(method='radius', session_id_list=['19307', '19309','19310','19364'])
    dhcp client should set a long lease time, otherwise, it will be renewed soon
    :param kwargs:
    method:                     'radius'/'cli', default is cli
    device_id:                  device id name e.g. 'r0'
    client_type:                client type , dhcp/pppoe/l2tp/dhcpv6, default is pppoe
    interface_list:            the interfaces list needs to be cleared(used for pppoe/l2tp)
    session_id_list:           session id list used for dhcp or radius
    radius_id:                 radius device id, default is h0
    radius_client_ip:          router ip address in radius server ,default is 100.0.0.1
    radius_secret:             radius secret, default is joshua
    :return:
    """
    t.log("inside clear_subscriber_sessions, kwargs is {}".format(kwargs))
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    client_type = kwargs.get('client_type', 'pppoe')
    method = kwargs.get('method', 'cli')

    interface_list = kwargs.get('interface_list', [])
    session_id_list = kwargs.get('session_id_list', [])
    t.log("logout method is {}, session list is {}".format(method, session_id_list))
    if method == 'cli':
        command_list = []
        if interface_list:
            for interface in interface_list:
                if client_type == 'pppoe':
                    command_list.append('clear pppoe sessions {}'.format(interface))
                if client_type == 'l2tp':
                    command_list.append('clear services l2tp session interface {}'.format(interface))

        if session_id_list:
            for session in session_id_list:
                if client_type == 'dhcp':
                    command_list.append("clear {} server binding {}".format(client_type, session))
                    command_list.append("clear {} relay binding {}".format(client_type, session))

        for command in command_list:
            resp = router.cli(command=command).resp
            if 'not' in resp:
                raise Exception("command {} failed".format(command))

    if method == 'radius':
        radius_id = kwargs.get('radius_id', 'h0')
        radius_handle = t.get_handle(radius_id)
        server_ip = kwargs.get('radius_client_ip', '100.0.0.1')
        password = kwargs.get('radius_secret', 'joshua')
        for session in session_id_list:
            command = "echo Acct-Session-Id={} | radclient -x {}:3799 " \
                      "disconnect {}".format(session, server_ip, password)
            resp = radius_handle.shell(command=command).resp
            if 'Error-Cause' in resp:
                raise Exception("command '{}' failed in disconnect".format(command))


def subscriber_service_action(**kwargs):
    """

    :param kwargs:
    device_id:                              device id name e.g. 'r0'
    session_id_list:                        a list of session id
    service_name:                           router service profile name
    method:                                 cli or radius
    radius_id:                              radius device id, default is h0
    radius_client_ip:                       router ip address in radius server ,default is 100.0.0.1
    radius_secret:                          radius secret, default is joshua
    action:                                 activate/deactivate
    :return:
    """
    t.log("inside subscriber_service_action, kwargs is {}".format(kwargs))
    method = kwargs['method']
    chosen_sessions = kwargs['session_id_list']
    service_name = kwargs['service_name']
    service_type = kwargs.get('service_type', None)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    action = kwargs['action']
    if method == 'radius':
        radius_id = kwargs.get('radius_id', 'h0')
        radius_handle = t.get_handle(radius_id)
        server_ip = kwargs.get('radius_client_ip', '100.0.0.1')
        password = kwargs.get('radius_secret', 'joshua')
        for session in chosen_sessions:
            if action == 'activate':
                command = "echo Acct-Session-Id={},Unisphere-Activate-Service-tag1={} | radclient -x {}:3799 coa {}". \
                    format(session, service_name, server_ip, password)
            if action == 'deactivate':
                command = "echo Acct-Session-Id={},Unisphere-Deactivate-Service={} | radclient -x {}:3799 coa {}". \
                    format(session, service_name, server_ip, password)
            resp = radius_handle.shell(command=command).resp
            if 'CoA-NAK' in resp:
                router.cli(command="show network-access aaa subscriber session-id {} detail".format(session))
                raise Exception("failed to {} service using command {}".format(action, command))
            else:
                t.log("service {} was {}d for session {} successfully".format(service_name, action, session))

    if method == 'cli':
        if action == 'activate':
            cmds = 'add'
        elif action == 'deactivate':
            cmds = 'delete'
        for session in chosen_sessions:
            command = "request network-access aaa subscriber " \
                      "{} session-id {} service-profile {}".format(cmds, session, service_name)
            resp = router.cli(command=command).resp
            if 'Successful' not in resp:
                router.cli(command="show network-access aaa subscriber session-id {} detail".format(session))
                raise Exception("failed to {} service using command {}".format(action, command))
            else:
                t.log("service {} was {}d for session {} successfully".format(service_name, action, session))
            if service_type:
                resp = router.cli(command="show dynamic-configuration session "
                                          "information session-id {} | grep \"Physical IFD name\"".format(session)).resp
                result = resp.split(sep=" ")
                match = re.match(r'\S+-(\d+)/\d+', result[-1])
                if match:
                    fpc_slot = match.group(1)
                    t.log("Session id {} is on fpc slot {}".format(session, fpc_slot))
                    router.shell(command="cprod -A fpc{} -c show jnh 0 ex ter | grep firewall".format(fpc_slot))
                else:
                    t.log("not able to get the fpc slot for session id {}".format(session))
                    router.cli(command="show dynamic-configuration session information session-id {}".format(session))


def get_session_service_name(**kwargs):
    """
    get service name from a session
    :param kwargs:
    session_id:                     subscirber session id
    device_id:                      router device id, default is 'r0'

    :return:                        a list of service name
    """
    t.log("inside get_session_service_name, kwargs is {}".format(kwargs))
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    session_id = kwargs['session_id']
    command = "show network-access aaa subscribers session-id {} detail".format(session_id)
    resp = router.cli(command=command, timeout=600).resp

    return re.findall(r'Service name:\s+(.*)\r\n', resp, flags=re.IGNORECASE)


def get_re_fpc_memory():
    """
    get re and fpc memory info
    return a dictionary with the fpc memory util and clients and re memory util
    :return:
    """
    t.log("inside get_re_fpc_memory")
    _check_bbe()
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    for device_id in router_ids:
        router = t.get_handle(device_id)
        resp = router.pyez('get_fpc_information', timeout=600).resp
        pfe_mem_dict = {}
        pfe_mem_dict[device_id] = {}
        pfe_dict = {}
        if hasattr(router, 'vc') and router.vc:
            multi_engines = resp.findall('multi-routing-engine-item')
            for engine in multi_engines:
                chassis_name = engine.findtext('re-name')
                for fpc_info in engine.findall('fpc-information/fpc'):
                    state = fpc_info.findtext('state')
                    if state != 'Online':
                        continue
                    pfeutil = fpc_info.findtext('memory-heap-utilization')
                    print('pfeutil is {}'.format(pfeutil))
                    pfe_dict['memory-heap-utilization'] = pfeutil + '%'
                    slot = fpc_info.findtext('slot')
                    name = chassis_name + '_fpc' + slot
                    pfe_mem_dict[device_id][name] = pfe_dict.copy()
                    pfe_mem_dict[device_id][name]['clients'] = 0
            resp = router.pyez('get_route_engine_information', normalize=True, timeout=600).resp
            multi_engines = resp.findall('multi-routing-engine-item')
            for engine in multi_engines:
                chassis_name = engine.findtext('re-name')
                for re_eng in engine.findall('route-engine-information/route-engine'):
                    slot = re_eng.findtext('slot')
                    name = chassis_name + '_re' + slot
                    pfe_mem_dict[device_id][name] = dict()
                    reutil = re_eng.findtext('memory-buffer-utilization')
                    pfe_mem_dict[device_id][name]['memory-utilization'] = reutil + '%'

        else:
            for fpc_info in resp.findall('fpc'):
                state = fpc_info.findtext('state')
                if state != 'Online':
                    continue
                pfeutil = fpc_info.findtext('memory-heap-utilization')
                print('pfeutil is {}'.format(pfeutil))
                pfe_dict['memory-heap-utilization'] = pfeutil + '%'
                slot = fpc_info.findtext('slot')
                name = 'fpc' + slot
                pfe_mem_dict[device_id][name] = pfe_dict.copy()
                pfe_mem_dict[device_id][name]['clients'] = 0
            resp = router.pyez('get_subscribers_summary', slot=True, normalize=True, timeout=600).resp
            for counter in resp.findall('counters'):
                port_name = counter.findtext('port-name')
                if not port_name:
                    continue
                elif 'ps' not in port_name:
                    ##cover the xe or ge or ae case
                    match = re.match(r'.*[xe|ge]-(\d+)$', port_name)
                else:
                    resp2 = router.cli(command='show configuration interfaces ps0 anchor-point').resp
                    match = re.match(r'lt-(\d+)\/\d+\/\d+', resp2)

                if match:
                    clients = counter.findtext('port-count')
                    name = 'fpc' + match.group(1)
                    print('name is {}, clients is {}'.format(name, clients))
                    pfe_mem_dict[device_id][name]['clients'] += int(clients)
            resp = router.pyez('get_route_engine_information', normalize=True, timeout=600).resp
            for engine in resp.findall('route-engine'):
                slot = engine.findtext('slot')
                if not slot:
                    slot = '0'
                name = 're' + slot
                pfe_mem_dict[device_id][name] = dict()
                reutil = engine.findtext('memory-buffer-utilization')
                pfe_mem_dict[device_id][name]['memory-utilization'] = reutil + '%'

    return pfe_mem_dict


class get_fpc_vty_stats:
    """
    collect FPC vty command when login clients
    :param interval:            collect interval, default is 60s
    :return:
    """
    def __init__(self, interval):
        self._running = True
        self.interval = int(interval)
        self.router_ids = bbe.get_devices(device_tags='dut', id_only=True)
        slot_dict = {}
        for router_id in self.router_ids:
            slot_list = []
            router = t.get_handle(router_id)
            if hasattr(router, 'vc') and router.vc:
                resp = router.shell(command='sysctl hw.product.router_max_fpc_slots').resp
                max_slots = round(int(resp.split()[1]) / 2)
            for name in t.resources[router_id]['interfaces']:
                if 'access' in name or 'transit' in name:
                    match = re.match(r'\S+-(\d+)/\d+/\d+', t.resources[router_id]['interfaces'][name]['pic'])
                    slot = match.group(1)
                    if hasattr(router, 'vc') and router.vc:
                        if int(slot) >= max_slots:
                            slot = 'member1-fpc' + slot
                        else:
                            slot = 'member0-fpc' + slot
                    else:
                        slot = 'fpc' + slot
                    if slot not in slot_list:
                        slot_list.append(slot)
            slot_dict[router_id] = slot_list
        self.slot_dict = slot_dict

    def stop(self):
        '''
        force the thread to stop
        :return:
        '''
        self._running = False

    def run(self):
        '''
        begin the get_fpc_vty_stats thread
        :return:
        '''
        basetime = time.time()

        while self._running:
            for router_id in self.router_ids:
                router = t.get_handle(router_id)
                for slot in self.slot_dict[router_id]:
                    command_list = ['cprod -A {} -c show memory'.format(slot),
                                    'cprod -A {} -c show jnh 0 pool detail'.format(slot),
                                    'cprod -A {} -c show jnh 0 pool composition'.format(slot),
                                    'cprod -A {} -c show jnh 0 pool layout'.format(slot)]
                    for command in command_list:
                        router.shell(command=command)
                        time.sleep(1)
            time.sleep(self.interval)
            if time.time() - basetime > 3600:
                break


def get_cst_stats():
    """
    return bbe.cst_stats ditionary
    :return:
    """
    return bbe.cst_stats


def check_gres_ready(device_id='r0', check_timeout=1800):
    """
    check if router is gres ready
    :param device_id:               router_id, default is 'r0'
    :return:
    """
    t.log("inside check_gres_ready")
    _check_bbe()
    router = t.get_handle(device_id)
    start_time = time.time()
    master_node = 'primary'
    master_re = get_master_re_name(device_id)
    node_list = ['primary']
    if hasattr(router, 'vc') and router.vc:
        master_node = router.detect_master_node()
        master_re = get_master_re_name(device_id).split(sep='-')[1]
        node_list = ['primary', 'member1']

    while True:
        gres_ready = True
        command_list = ["request chassis routing-engine master switch check"]
        if hasattr(router, 'vc') and router.vc:
            command_list = ["request chassis routing-engine master switch check",
                            "request virtual-chassis routing-engine master switch check"]
        for command in command_list:
            resp = router.cli(command=command).resp
            if 'Switchover Ready' not in resp:
                gres_ready = False
            time.sleep(3)
        # below check may not needed since the output changes from version to version

        for node in node_list:
            for controller in ['re0', 're1']:
                router.set_current_controller(system_node=node, controller=controller)
                if node == master_node and controller == master_re:
                    continue
                command = 'show system switchover local' \
                    if (hasattr(router, 'vc') and router.vc) else 'show system switchover'
                resp = router.cli(command=command).resp
                if 'Switchover Status: Ready' not in resp and \
                                'Peer state: Steady State' not in resp and 'Switchover Ready' not in resp:
                    gres_ready = False
                    t.log("node {} controller {} is not ready for switchover".format(node, controller))

        router.set_current_controller(system_node=master_node, controller=master_re)
        resp = router.cli(command='show task replication').resp
        if 'Stateful Replication: Enabled' not in resp:
            gres_ready = False
            t.log("task replication is not ready")
        resp = router.cli(command='show database-replication summary').resp
        if not re.search(r'Database\s+Synchronized', resp) or not re.search(r'Connection\s+Up', resp):
            gres_ready = False
            t.log("database replication is not ready")
        if hasattr(router, 'vc') and router.vc:
            t.log("sysctl check for mxvc gres")
            command_list = ['sysctl -a | grep hw.re.is_slave_peer_gres_ready',
                            'sysctl -a | grep hw.re.is_local_slave_peer_gres_ready']
            for command in command_list:
                resp = router.shell(command=command).resp
                if resp.split()[1] != '1':
                    gres_ready = False
                    t.log("{} result is not 1".format(command))

            command_list = ['sysctl -a | grep hw.re.local_failover:', 'sysctl -a | grep hw.re.failover:']
            for command in command_list:
                resp = router.shell(command=command).resp
                if resp.split()[1] != '3':
                    gres_ready = False
                    t.log("{} result is not 3".format(command))

        wait_time = time.time() - start_time
        if gres_ready:
            t.log("router {} is in GRES ready state".format(device_id))
            break
        elif wait_time > check_timeout:
            raise Exception("router {} is not ready for GRES after waiting for {}".format(device_id, check_timeout))
        t.log("waiting for another 20s for checking GRES state")
        time.sleep(20)


def sp_collect_logs(resource, remote_dir, pattern, local_dir=None):
    """
    Only used for scaling performance to collect logs under /var/log
    :param resource:     **REQUIRED** router id e.g. 'r0'
    :param remote_dir:   REQUIRED,directory on the router from where the file/files need to be downloaded e.g. '/var/log'
    :param pattern:      **REQUIRED**,pattern for a set of files to be downloaded from the router e.g '*era*'
    :param local_dir:    directory on the server, e.g '/homes/<user-name>/screipts/results' default is t._log_dir_
    :return:
    """
    _check_bbe()
    if not local_dir:
        local_dir = t._log_dir
    for re_name in t.get_resource(resource)['system']['primary']['controllers'].keys():
        router = t.get_handle(resource=resource, controller=re_name)
        router.su()
        print(local_dir)
        # For every re,create a directory
        logs_dir = local_dir + '/' + resource + re_name
        os.makedirs(str(logs_dir), exist_ok=True)
        process_id = str(os.getpid())
        router.shell(command='cd {0}'.format(remote_dir))
        resp = router.shell(command='ls {0}'.format(pattern))
        leo1 = resp.response()
        # create a list of all the concerned files
        list_of_files = leo1.split()
        # loop through the list of files and download each of them to the shell server
        for file in list_of_files:
            # get the entire filename with its path on the router
            remote_file = remote_dir + '/' + file
            # actual file on the server will be the filename with process id appended to it
            filetodownload = file.replace(".log", "." + process_id + ".log")
            actual = logs_dir + "/" + filetodownload
            router.download(local_file=actual, remote_file=remote_file)


class CheckCli():
    """
    Class to store and verify that cli outputs (of show commands) have not changed

    cli_checker = CheckCli(router, ["show system subscribers"])
    ... TEST CODE
    cli_checker.verify_cli_output()
    """

    def __init__(self, router, commands):
        """

        :param router:
            router handle to run cli commands from
        :param commands:
            list of "show" cli commands to run
        """
        if not isinstance(commands, list):
            commands = [commands]
        responses = []
        base_time = time.time()
        for command in commands:
            resp = router.cli(command=command).resp
            responses.append(resp)
        self.runtime = time.time() - base_time
        self.router = router
        self.commands = commands
        self.responses = responses

    def get_runtime(self):
        """

        :return: Total run time of all show commands (during first run)
        """
        return self.runtime

    def verify_cli_output(self):
        """
        Make sure all cli outputs have not changed
        """
        fail = 0
        for command, old_resp in zip(self.commands, self.responses):
            new_resp = self.router.cli(command=command).resp
            if old_resp != new_resp:
                fail += 1
                error_message = "Response to the command \"" + command + "\" changed.\n"
                error_message += "".join(difflib.context_diff(old_resp.splitlines(True), new_resp.splitlines(True),
                                                              fromfile="Original response",
                                                              tofile="New response",
                                                              n=float("inf")))
                t.log(error_message)
        if fail > 0:
            raise Exception("{} of {} commands received a changed response".format(str(fail), str(len(self.commands))))
        else:
            t.log("No change to cli output")

def check_cli(router, commands):
    """
    :return: A new CheckCli instance
    """
    _check_bbe()
    return CheckCli(router, commands)

def get_runtime_of_check_cli(cli_checker):
    """
    :return: Runtime of a CheckCli instance
    """
    _check_bbe()
    return cli_checker.get_runtime()

def verify_cli_output(cli_checker):
    """
    Verify CLI output of a CheckCli instance
    """
    _check_bbe()
    cli_checker.verify_cli_output()

def remove_traffic(**kwargs):
    """
    remove  traffic streams in tester
    :param kwargs:
     rt_device_id:                  e,g, rt0
     handle:                        traffic item handle
    :return:
    """
    _check_bbe()
    t.log("inside start_traffic, kwargs is {}".format(kwargs))
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device_id)
    stop_args = dict()
    if 'handle' in kwargs:
        stop_args['handle'] = kwargs['handle']
    stop_args['action'] = 'delete'
    result = tester.invoke('traffic_action', **stop_args)
    if result['status'] != '1':
        raise Exception("failed to remove the traffic")

def get_l2tp_stats_for_scaling(resource='r0'):
    """
    collect l2tp stats for scaling publish report
    :param resource:
    :return:
    """
    router = t.get_handle(resource)
    tv_dict = tv['uv-bbevar']
    if 'l2tp' in tv_dict:

        bbe.cst_stats['target_l2tp_tunnel_count'] = tv_dict['l2tp']['l2tp-tunnels-count']
        bbe.cst_stats['target_total_number_of_l2tp_subscribers'] = tv_dict['l2tp']['total-number-of-subscribers']
        l2tp_cnt = bbe.cst_stats['target_total_number_of_l2tp_subscribers']
        try:
            bbe.cst_stats['target_number_of_subs_per_l2tp_tunnel'] = l2tp_cnt/bbe.cst_stats['target_l2tp_tunnel_count']
            t.log('calculate the actual l2tp statistics')
            resp = router.cli(command='show services l2tp summary', timeout=120).resp
            sh0 = re.findall(r'Tunnels:\s+\d+', resp)
            bbe.cst_stats['actual_l2tp_tunnel_count'] = int(re.findall(r'\d+', sh0[0])[0])
            sh1 = re.findall(r'Sessions:\s+\d+', resp)
            bbe.cst_stats['actual_total_number_of_l2tp_subscribers'] = int(re.findall(r'\d+', sh1[0])[0])
            actual = bbe.cst_stats['actual_total_number_of_l2tp_subscribers']
            bbe.cst_stats['actual_number_of_subs_per_l2tp_tunnel'] = actual/bbe.cst_stats['actual_l2tp_tunnel_count']
            resp = router.cli(command='show subscribers summary port', timeout=120).resp
            if 'cos' in tv_dict:
                if 'service-interface-fpc' in tv_dict['cos']:
                    number_of_si_intf = len(tv_dict['cos']['service-interface-fpc'].split(','))
                    bbe.cst_stats['target_number_of_subs_per_si_intf'] = l2tp_cnt/number_of_si_intf
                    bbe.cst_stats['actual_number_of_subs_per_si_intf'] = actual/number_of_si_intf
        except Exception as err:
            raise Exception("Could not get the stats for LAC/LNS Testing with {}".format(err.args[0]))


def print_action_result(name, result):
    """

    :param name:              Testcase name/tag
    :param result:            FASS or FAIL
    :return:
    """
    if 'custom_actions' not in bbe.cst_stats:
        bbe.cst_stats['custom_actions'] = {}
    testcase = name.upper()
    testcase = testcase.replace(' ', '_')
    bbe.cst_stats['custom_actions'][testcase] = result
