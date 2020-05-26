"""
CST Test Suites
"""
import time
from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil
from jnpr.toby.bbe.bbeactions import BBEActions
from jnpr.toby.hldcl.device import Device
import datetime
import random
import re
import os
import math
from jnpr.toby.bbe.cst.cstutils import *
import threading
from jnpr.toby.bbe.cst.cstactions import *
from jnpr.toby.utils.utils import *
from jnpr.toby.bbe.cst.cstutils import _check_bbe
import jnpr.toby.engines.verification.verify_utils as verify_utils
from jnpr.toby.hldcl import device as dev
from jnpr.toby.init.init import *
import pdb

def unicast_traffic_test(**kwargs):
    """
    suites.unicast_traffic_test(traffic_args = {'rate':'10%', 'frame_size':'1200'}, new_mesh=True, duration=90)

    :param kwargs:
    rt_device_id:                  rt device name, e.g.'rt0'
    new_mesh:                      create new traffic mesh(True/False)
    subs:                          subs involved in traffic (see add_susbcriber_mesh)
    duration:                      traffic running time, by default is 60 seconds
    remove_traffic_after_test:     remove traffic items after test, by default is True
    cpu_settle:                    cpu idle settle value, by default is 75
    verify_traffic:                verify traffic: True/False, by default True
    traffic_args:                  dictionary for creating traffic which include name, rate, frame_size, etc
                                   (check add_subscriber_mesh in cstutils.py)
    :return:
    """
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device_id)
    subs = kwargs.get('subs', bbe.get_subscriber_handles())
    t.log('start login subs {} before test'.format(subs))
    try:
        cst_start_clients(restart_unbound_only=True, **kwargs)
    except:
        cst_start_clients(**kwargs)

    verify_traffic_enable = kwargs.get('verify_traffic', True)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        new_mesh = kwargs.get('new_mesh', True)
        duration = kwargs.get('duration', 60)
        if new_mesh:
            t.log('remove existing traffic mesh')
            tester.invoke('traffic_action', action='stop')
            time.sleep(10)
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
        remove_traffic = kwargs.get('remove_traffic_after_test', True)
        if not new_mesh:
            remove_traffic = False
        if remove_traffic:
            t.log('remove traffic stream after unicast test')
            tester.invoke('traffic_action', action='delete')


def concurrent_login_logout_test(**kwargs):
    """
    concurrent_login_logout_test(iteration=2)
    :param kwargs:
    background_subs:   background subs list which is running in the background
    group_a:           one of the login/logout group list
    retry:             login restart retry
    verify_traffic:    verify background traffic in each iteration
    cpu_settle:        cpu usage before next iteration
    cpu_check          True/False
    iteration:         iteration count, default is 10
    inflight_enable:   True/False
    device_id:         router resource name list to collect the client info
    :return:
    """
    inflight_enable = kwargs.get('inflight_enable', False)
    if not inflight_enable:
        result = prepare_for_concurrent_test(**kwargs)
        group_a = result['logout_group']
        group_b = result['login_group']

    if 'group_a' in kwargs:
        group_a = kwargs['group_a']
    if 'group_b' in kwargs:
        group_b = kwargs['group_b']

    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    rt_handle = t.get_handle(resource=rt_device_id)

    group_a_handle = []
    group_b_handle = []

    for subs in group_a:
        group_a_handle.append(subs.rt_ethernet_handle)

    for subs in group_b:
        group_b_handle.append(subs.rt_ethernet_handle)

    t.log('initial logout group {}, initial login group {}'.format(group_a_handle, group_b_handle))

    iteration_count = 10
    #stop_event = None
    if 'event' in kwargs:
        stop_event = kwargs['event']
    if 'iteration' in kwargs and kwargs['iteration'] == 'unlimited':
        iteration_count = 1000000000
    else:
        iteration_count = int(kwargs.get('iteration', 10))
    for iteration in range(1, iteration_count + 1):
        t.log('concurrent login/logout started in iteration #{}'.format(iteration))
        #result = rt_handle.invoke('protocol_info', mode='aggregate')
        login_group = []
        logout_group = []
        rt_output = get_rt_subs_info()
        base_count = rt_output['rt_sessions_not_started']
        #not_started_count = base_count
        #base_time = time.time()
        for subs in group_a + group_b:
            handle_list = []
            if hasattr(subs, 'rt_dhcpv4_handle') and subs.rt_dhcpv4_handle:
                handle_list.append(subs.rt_dhcpv4_handle)
            if hasattr(subs, 'rt_dhcpv6_handle') and subs.rt_dhcpv6_handle:
                handle_list.append(subs.rt_dhcpv6_handle)
            if hasattr(subs, 'rt_pppox_handle') and subs.rt_pppox_handle:
                handle_list.append(subs.rt_pppox_handle)
            for handle in handle_list:
                result = rt_handle.invoke('protocol_info', mode='aggregate', handle=handle)
            #ethernet = subs.rt_ethernet_handle
            #base_rt_sessions_not_started = int(result[ethernet]['aggregate']['sessions_not_started'])
                base_rt_sessions_not_started = int(result[handle]['aggregate']['sessions_not_started'])
                if base_rt_sessions_not_started == 0:
                    logout_group.append(subs)
                else:
                    subs.start()
                    login_group.append(subs)
                    t.log("start login subs {} in iteration #{}".format(subs.rt_ethernet_handle, iteration))

        ##waiting for tester to send out packet
        # while not_started_count == base_count:
        #     t.log('waiting for tester to start login')
        #     time.sleep(10)
        #     rt_output = get_rt_subs_info()
        #     not_started_count = rt_output['rt_sessions_not_started']
        #     if not_started_count == base_count and int(time.time() - base_time) > 600:
        #         raise Exception("not seen any packets out after waiting for 600s in iteration #{}".format(iteration))

        # logout subscribers from logout group
        for subs in logout_group:
            subs.stop()
            t.log("start logout subs {} in iteration #{}".format(subs.rt_ethernet_handle, iteration))
        t.log('waiting for the iteration #{} to finish'.format(iteration))
        # result = rt_handle.invoke('protocol_info', mode='aggregate')
        # if result['status'] == '0':
        #     raise Exception("tester returned failure, please check tester")
        for subs in login_group:
            handle_list = []
            if hasattr(subs, 'rt_dhcpv4_handle') and subs.rt_dhcpv4_handle:
                handle_list.append(subs.rt_dhcpv4_handle)
            if hasattr(subs, 'rt_dhcpv6_handle') and subs.rt_dhcpv6_handle:
                handle_list.append(subs.rt_dhcpv6_handle)
            if hasattr(subs, 'rt_pppox_handle') and subs.rt_pppox_handle:
                handle_list.append(subs.rt_pppox_handle)
            for handle in handle_list:
                result = rt_handle.invoke('protocol_info', mode='aggregate', handle=handle)
                expected_subs_in_rt = int(subs.count)
                base_rt_sessions_up = int(result[handle]['aggregate']['sessions_up'])
                rt_sessions_up = base_rt_sessions_up
                retry = 0
                while rt_sessions_up < expected_subs_in_rt:
                    time.sleep(10)
                    t.log("check subs {} login stats".format(handle))
                    result = rt_handle.invoke('protocol_info', mode='aggregate', handle=handle)
                    rt_sessions_up = int(result[handle]['aggregate']['sessions_up'])
                    rt_sessions_down = int(result[handle]['aggregate']['sessions_down'])
                    rt_sessions_not_started = int(result[handle]['aggregate']['sessions_not_started'])
                    delta_sessions_up = rt_sessions_up - base_rt_sessions_up
                    if delta_sessions_up == 0 and rt_sessions_up > 0 and rt_sessions_not_started == 0 \
                            and rt_sessions_down > 0:
                        subs.restart_down()
                        if retry > int(kwargs.get('retry', 5)):
                            t.log('subs {} tried restart in  #{} times,'
                                  ' assume reach the stable state'.format(subs, retry))
                            break
                        retry += 1
                    if delta_sessions_up == 0 and rt_sessions_up == 0:
                        if retry > int(kwargs.get('retry', 5)):
                            raise Exception("no subscriber {}"
                                            " in login group can login".format(subs.rt_device_group_handle))
                        retry += 1

                    base_rt_sessions_up = rt_sessions_up
        t.log("all login subscriber are in stable state in RT now for iteration #{}".format(iteration))

        for subs in logout_group:
            # ethernet = subs.rt_ethernet_handle
            # result = rt_handle.invoke('protocol_info', mode='aggregate')
            handle_list = []
            if hasattr(subs, 'rt_dhcpv4_handle') and subs.rt_dhcpv4_handle:
                handle_list.append(subs.rt_dhcpv4_handle)
            if hasattr(subs, 'rt_dhcpv6_handle') and subs.rt_dhcpv6_handle:
                handle_list.append(subs.rt_dhcpv6_handle)
            if hasattr(subs, 'rt_pppox_handle') and subs.rt_pppox_handle:
                handle_list.append(subs.rt_pppox_handle)
            for handle in handle_list:
                result = rt_handle.invoke('protocol_info', mode='aggregate', handle=handle)
                expected_subs_in_rt = int(subs.count)
                rt_sessions_not_started = int(result[handle]['aggregate']['sessions_not_started'])
                while rt_sessions_not_started < expected_subs_in_rt:
                    t.log("check subs {} logout stats".format(handle))
                    time.sleep(5)
                    result = rt_handle.invoke('protocol_info', mode='aggregate', handle=handle)
                    rt_sessions_not_started = int(result[handle]['aggregate']['sessions_not_started'])

        t.log("all logout subscriber are released in RT now for iteration #{}".format(iteration))

        verify_traffic_enable = kwargs.get('verify_traffic', False)
        if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
            t.log('verify background traffic in iteration #{}'.format(iteration))
            stop_traffic()
            verify_traffic()
            if iteration < iteration_count:
                start_traffic(**kwargs)
        if 'sleep_between_iteration' in kwargs:
            time.sleep(int(kwargs['sleep_between_iteration']))
        if not inflight_enable:
            # check subs in router
            if 'device_id' in kwargs:
                router_ids = kwargs['device_id']
                if not isinstance(router_ids, list):
                    router_ids = [router_ids]
            elif 'router_id' in kwargs:
                router_ids = kwargs['router_id']
                if not isinstance(router_ids, list):
                    router_ids = [router_ids]
            else:
                router_ids = bbe.get_devices(device_tags='dut', id_only=True)

            for router_id in router_ids:
                summary = get_router_sub_summary(router_id)
                t.log('router {} has clients {} after iteration #{}'.format(router_id, summary, iteration))
            # check cpu settle
            cpu_check = kwargs.get('cpu_check', True)
            if cpu_check:
                BBEJunosUtil.cpu_settle(cpu_threshold=int(kwargs.get('process_cpu', 30)),
                                        idle_min=int(kwargs.get('cpu_settle', 75)),
                                        dead_time=int(kwargs.get('cpu_deadtime', 1200)),
                                        interval=int(kwargs.get('cpu_interval', 20)))
            t.log('cpu settled after iteration #{}'.format(iteration))
    # start all clients
    cst_start_clients(**kwargs)


def inflight_tests(list_of_action_dicts, **kwargs):
    """
    dict1 = {'fname':gres_test, 'kwargs':{'verify_traffic':False, 'iteration':2, 'gres_type':'cli'}, 'delay':10}
    suites.inflight_tests([dict1], iteration=2)

    :param
    list_of_action_dicts:    specify a list of action name and its argument, each dictionary has a mandatory
                             key 'fname' that contains the function call(without the parentheses) as well as
                             optional keys 'args' and 'kwargs' that contain lists of arguments to be passed to
                            the function. It also have a key 'delay' which denotes the number of seconds to wait
                            before the function is called.

    kwargs:                 args for concurrently login/logout, e.g. iteration

    :return:
    """
    t.log('preparing concurrent login/logout subscriber groups')
    result = prepare_for_concurrent_test(**kwargs)
    kwargs['group_a'] = result['logout_group']
    kwargs['group_b'] = result['login_group']
    kwargs['inflight_enable'] = True
    t.log('list_of_actions is {}, kwargs is {}'.format(list_of_action_dicts, kwargs))
    if not isinstance(list_of_action_dicts, list):
        t.log('list_of_action_dicts is not a list')
        list_of_action_dicts = [list_of_action_dicts]
    try:
        t.log("start concurrent login-logout thread in the background")
        args = kwargs.get('args', [])
        action = kwargs.get('bname', concurrent_login_logout_test)
        background_thread = threading.Thread(target=action, args=args, kwargs=kwargs)
        background_thread.start()
        # if background_thread.is_alive():
        #     t.log('successfully kicked off action concurrent_login_logout_test'.format(action))
        # else:
        #     t.log('ERROR', 'unable to kick off action concurrent_login_logout_test'.format(action))
        #     raise Exception("failed to start concurrent login-logout in the background")
    except:
        raise Exception("failed to start concurrent login-logout in the background")

    if 'mode' in kwargs and kwargs['mode'] == 'parallel':
        run_multiple(list_of_action_dicts)
    else:
        for index, dicts in enumerate(list_of_action_dicts):
            t.log('index is {}, dict is {}'.format(index, dicts))
            args = dicts.get('args', [])
            kwargs = dicts.get('kwargs', {})
            action = dicts.get('fname')
            delay = dicts.get('delay', 0)
            time.sleep(delay)
            t.log('args is {}, kwargs is {}, fname is {}'.format(args, kwargs, action))
            if isinstance(action, str):
                action = eval(action)
            action_thread = threading.Thread(target=action, args=args, kwargs=kwargs)
            action_thread.start()
            if action_thread.is_alive():
                t.log('successfully kicked off action {} with args {}, kwargs {}'.format(action, args, kwargs))
            else:
                t.log('ERROR', 'unable to kick off action {} with args {}, kwargs {}'.format(action, args, kwargs))
                continue
            action_thread.join()
            time.sleep(10)

            while action_thread.is_alive():
                time.sleep(10)
            t.log('action {} in the thread finished'.format(action))

    while background_thread.is_alive():
        time.sleep(10)
    action = kwargs.get('bname', 'concurrent_login_logout_test')
    t.log('action {} in the thread finished'.format(action))

    verify_traffic_enable = kwargs.get('verify_traffic', True)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        t.log('login all subscribers and verify the traffic after inflight test')
        unicast_traffic_test(**kwargs)


def gres_test(**kwargs):
    """
    gres_test(verify_traffic=False, gres_type='kernel_crash', iteration=1)
    :param kwargs:
    gres_type:              cli/kernel_crash/power_cycle, default is cli
    command:                switch/acquire/release when gres_type is cli
    iteration:              by default is 2
    device_id:              device name, by default is 'r0'
    verify_traffic:         running traffic in test, by default is True
    gres_ready_check:       True/False, default is True
    cpu_settle:             cpu idle settle value, by default is 75
    cpu_check:              True/False
    check_access_route:     verify access route count
    :return:
    """
    default_id = bbe.get_devices(device_tags='dut', id_only=True)[0]
    if len(t.get_resource(kwargs.get('device_id', default_id))['system']['primary']['controllers'].keys()) == 1:
        t.log("There is only 1 RE, ignore GRES test")
        return
    cpu_check = kwargs.get('cpu_check', True)
    verify_traffic_enable = kwargs.get('verify_traffic', True)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        unicast_traffic_test(remove_traffic_after_test=False, **kwargs)
        start_traffic(duration=3600)
    device = kwargs.get('device_id', default_id)
    check_access_route = kwargs.get('check_access_route', True)
    maximum_wait_for_readiness = kwargs.get('maximum_wait_for_readiness', 1200)
    router = t.get_handle(device)
    gres_type = kwargs.get('gres_type', 'cli')
    gres_ready_check = kwargs.get('gres_ready_check', True)
    for iteration in range(1, int(kwargs.get('iteration', 2)) + 1):
        master_re = router.get_current_controller_name()
        t.log('in iteration #{}, the current master re is {}'.format(iteration, master_re))

        t.log('GRES by routing enginer master switch in iteration #{} - Start'.format(iteration))
        if gres_ready_check:
            wait_for_readiness = 0
            re_ready_for_master_switch = False
            master_re_ready = False
            backup_re_ready = False

            comd = "request chassis routing-engine master switch check"

            while (not re_ready_for_master_switch) and (wait_for_readiness < maximum_wait_for_readiness):
                resp_obj = router.cli(command=comd)
                resp = resp_obj.response()
                pattern = "Switchover Ready"
                matches = re.search(pattern, resp)
                if matches:
                    master_re_ready = True
                    t.log("check the backup RE gres readiness")
                    for name in ['re0', 're1']:
                        if name != master_re:
                            router.set_current_controller(system_node='primary', controller=name)
                    resp = router.cli(command="show system switchover", timeout=300).resp
                    if 'Switchover Status: Ready' in resp:
                        backup_re_ready = True
                    t.log("set controller back to master RE {}".format(master_re))
                    router.set_current_controller(system_node='primary', controller=master_re)
                re_ready_for_master_switch = master_re_ready and backup_re_ready

                if not re_ready_for_master_switch:
                    time.sleep(60)
                    wait_for_readiness += 60

            if not re_ready_for_master_switch:
                raise Exception("Routing Engine is not ready for master switch"
                                " even after maximum wait of {0} seconds".format(maximum_wait_for_readiness))
            else:
                database_synchronized = 0
                wait_for_readiness = 0
                while (database_synchronized == 0) and (wait_for_readiness < maximum_wait_for_readiness):
                    response_obj = router.pyez('get_database_replication_summary_information', timeout=300).resp
                    if response_obj.findtext('replication-database-type') == 'Synchronized' and \
                                    response_obj.findtext('replication-graceful-restart-type') == 'Enabled':
                        database_synchronized = 1
                    else:
                        time.sleep(60)
                        t.log('wait for 60 seconds before checking gres state again,'
                              ' current total wait time is {}'.format(wait_for_readiness))
                        wait_for_readiness += 60

                if database_synchronized == 0:
                    raise Exception("Database Replication - Not Synchronized")
                else:
                    t.log('router is ready for a switchover in iteration #{}'.format(iteration))
        if gres_type == 'cli':
            command = kwargs.get('command', 'switch')
            if command == 'release':
                router.cli(command='request chassis routing-engine master release no-confirm')
                for name in ['re0', 're1']:
                    if name != master_re:
                        router.set_current_controller(system_node='primary', controller=name)
            elif command == 'acquire':
                for re_name in ['re0', 're1']:
                    if re_name != master_re:
                        new_master_re = re_name
                        router.set_current_controller(controller=new_master_re, system_node='primary')
                        router.cli(command='request chassis routing-engine master acquire no-confirm')
                        break
            else:
                router.cli(command='request chassis routing-engine master switch no-confirm')
                for name in ['re0', 're1']:
                    if name != master_re:
                        router.set_current_controller(system_node='primary', controller=name)

        if gres_type == 'power_cycle':
            router.cli(command='request system power-off', pattern='yes,no')
            router.cli(command='yes')
            time.sleep(10)
            for name in ['re0', 're1']:
                if name != master_re:
                    router.set_current_controller(system_node='primary', controller=name)
            time_wait_for_power_on = 0
            while True:
                resp = router.cli(command='request system power-on other-routing-engine')
                match = re.match(r'.*power-on\s+initiated', resp.resp)
                if match:
                    break
                time.sleep(10)
                time_wait_for_power_on += 10
                if time_wait_for_power_on > 300:
                    raise Exception("failed to power-on the other"
                                    " re after waiting 300s in iteration #{}".format(iteration))

        if gres_type == 'kernel_crash':
            re_name = router.get_current_controller_name()
            bbe_router = bbe.get_devices(devices=device)[0]
            if bbe_router.is_tomcat:
                tomcat_mode = True
            host = t.get_system(device)['primary']['controllers'][re_name]['con-ip']
            panic_re_recover(host=host, tomcat_mode=tomcat_mode)
            for name in ['re0', 're1']:
                if name != master_re:
                    router.set_current_controller(system_node='primary', controller=name)

        t.log("Waiting for new backup RE to reboot and come up in iteration #{}".format(iteration))
        time.sleep(200)
        if cpu_check:
            BBEJunosUtil.cpu_settle(cpu_threshold=int(kwargs.get('cpu_process', 30)),
                                    idle_min=int(kwargs.get('cpu_settle', 75)),
                                    dead_time=int(kwargs.get('cpu_deadtime', 1200)),
                                    interval=int(kwargs.get('cpu_interval', 20)))
        switch_time = 200
        while switch_time < 1200:
            try:
                router.reconnect(all=True, timeout=600)
            except:
                t.log('waiting for another 60 seconds for RE to come back online'
                      ' after switchover in iteration #{}'.format(iteration))
                time.sleep(60)
                switch_time += 60
            else:
                break
        if switch_time > 1200:
            raise Exception('router connection failed to be restored'
                            ' after waiting for {} in iteration #{}'.format(switch_time, iteration))

        new_master_re = get_master_re_name(device)
        t.log("new master re is {} after iteration #{}".format(new_master_re, iteration))
        if new_master_re != master_re:
            t.log("Mastership successfully changed,"
                  " current master is {} in iteration #{}".format(new_master_re, iteration))
            router.set_current_controller(controller=new_master_re, system_node='primary')
        else:
            raise Exception('master RE did not change, please check the router')

        if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
            # check cpu settle
            t.log('verify susbcriber/access route count and traffic in iteration #{}'.format(iteration))
            verify_client_count(**kwargs)
            if verify_utils.convert_str_to_num_or_bool(check_access_route):
                verify_client_route(**kwargs)
            stop_traffic()
            verify_traffic(**kwargs)
            start_traffic()
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        stop_traffic()

def fpc_mic_restart_test(**kwargs):
    """
    suites.fpc_mic_restart_test(verify_traffic=False, rebind=False, component='fpc', action='restart')
    suites.fpc_mic_restart_test(verify_traffic=False, rebind=False, component='mic', action='panic')
    :param kwargs:

    device_id:              device name, by default is 'r0'
    verify_traffic:         running traffic in test, by default is True
    verify_client:          verify client count after test
    check_access_route:     verify the client route count
    component:              fpc or mic
    interface_id:           interface_id e.g."transit"
    action:                 restart/panic/offon
    fpc_slot:               fpc slot
    cpu_settle:             cpu idle settle ratio, default is 75
    cpu_check:              True/False
    :return:
    """
    t.log("fpc/mic_restart test stated")
    cpu_check = kwargs.get('cpu_check', True)
    check_client = kwargs.get('verify_client', True)
    verify_traffic_enable = kwargs.get('verify_traffic', True)
    check_access_route = kwargs.get('check_access_route', True)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        t.log('login clients and verify traffic before FPC/MIC restart')
        unicast_traffic_test(**kwargs)
    device = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device)
    t.log('starting FPC/MIC restart test')
    fpc_pic_dict = {}
    if 'fpc_slot' in kwargs:
        fpcslots = kwargs['fpc_slot']
        if isinstance(fpcslots, list):
            for slot in fpcslots:
                fpc_pic_dict[slot] = ['0', '1']
        else:
            fpc_pic_dict[fpcslots] = ['0', '1']
    else:
        access_list = bbe.get_interfaces(device=device, interfaces=kwargs.get('interface_id', 'access'))
        if not access_list:
            t.log("WARN", "no interface was picked for test")
            return
        fpc_pic_dict = {}
        for access in access_list:
            match = re.match(r'.*-(\d+)/(\d+)/\d+', access.interface_pic)
            if match:
                if match.group(1) not in fpc_pic_dict:
                    fpc_pic_dict[match.group(1)] = []
                if match.group(2) not in fpc_pic_dict[match.group(1)]:
                    fpc_pic_dict[match.group(1)].append(match.group(2))
    t.log('fpc_pic_list is {}'.format(fpc_pic_dict))
    component = kwargs.get('component', 'fpc').lower()
    action = kwargs.get('action', 'restart').lower()
    if component == 'fpc':
        for fpc in fpc_pic_dict:
            if action == 'restart':
                t.log('will restart fpc slot {}'.format(fpc))
                command = 'request chassis fpc restart slot {}'.format(fpc)
                resp = router.cli(command=command).resp
                match = re.match(r'Restart\s+initiated', resp)
                if match:
                    t.log('fpc slot #{} restarted'.format(fpc))
                else:
                    raise Exception('fpc slot {} can not be restarted'.format(fpc))
            if action == 'panic':
                t.log('will panic fpc slot {}'.format(fpc))
                resp = router.vty(command='set parser security 10', destination='fpc' + fpc).resp
                if re.search('Security level', resp):
                    t.log('enter into vty security mode')
                    router.vty(command='test panic', destination='fpc' + fpc, pattern='(.*)')
                    t.log("waiting 200s for core-dumps to be generated")
                    time.sleep(200)
                    resp = router.cli(command='show system core-dumps').resp
                    if re.search('core-', resp):
                        t.log('fpc core was generated during test panic, will remove it')
                        router.cli(command='file delete /var/crash/core-*')
                else:
                    raise Exception("not able to set vty security mode")
            if action == 'offon':
                t.log("will offline/online fpc slot {}".format(fpc))
                for item in ['offline', 'online']:
                    if not re.match(r'MX(80|80-t|40|40-t|10|10-t|5|5-t)', router.get_model(), re.IGNORECASE):
                        command = "request chassis fpc slot {} {}".format(fpc, item)
                    else:
                        command = "request chassis tfeb {}".format(item)
                    resp = router.cli(command=command).resp

                    if item == 'offline':
                        offline_initiated = re.match(r'Offline\s+initiated', resp)
                        if offline_initiated:
                            t.log('fpc slot #{} offline'.format(fpc))
                            # gap between fpc offline and online
                            time.sleep(10)
                        else:
                            raise Exception('fpc slot {} failed to be offline'.format(fpc))
                    else:
                        # online, Sai's test encountered that fpc online request could hit
                        # that fpc is in a state that "FPC x is in transition, try again"
                        online_initiated = False
                        for online_retry in range(10):
                            mat = re.match(r'Online\s+initiated', resp)
                            if mat:
                                t.log('fpc slot #{} online initiated'.format(fpc))
                                online_initiated = True
                                break
                            else:
                                time.sleep(60)
                                resp = router.cli(command=command).resp

                        if not online_initiated:
                            raise Exception('fpc slot {} failed to be online'.format(fpc))

                        t.log('fpc slot {} enabled online command, wait for 100s'.format(fpc))
                        time.sleep(100)

            time.sleep(30)
            base_time = time.time()
            while True:
                resp = router.pyez('get_fpc_information', fpc_slot=fpc).resp

                if resp.findtext('fpc/state') == 'Online':
                    t.log('fpc slot {} back to online'.format(fpc))
                    break
                else:
                    time.sleep(10)

                if (time.time() - base_time) > 600:
                    raise Exception("FPC slot {} failed to come back online after 600s".format(fpc))

    if component == 'mic':
        fpc_mic_list = []
        for fpc in fpc_pic_dict:
            for mic in fpc_pic_dict[fpc]:
                fpc_mic_list.append((fpc, mic))
        t.log('fpc_mic list is {}'.format(fpc_mic_list))
        for chosen in fpc_mic_list:
            if action == 'restart':
                for cmds in ['offline', 'online']:
                    t.log('will do {} mic {}'.format(cmds, chosen))
                    command = 'request chassis mic fpc-slot {} mic-slot {} {}'.format(chosen[0], chosen[1], cmds)
                    resp = router.cli(command=command).resp
                    if re.search('not support', resp):
                        t.log('WARN', '{}'.format(resp))
                        break
                    pic_slots = ['0', '1']
                    if chosen[1] == '1':
                        pic_slots = ['2', '3']
                    retry = 5
                    while True:
                        time.sleep(10)
                        resp = router.pyez('get_pic_information', slot=chosen[0]).resp
                        break_loop = False
                        count = 0
                        for pic in resp.findall('fpc/pic'):
                            if pic.findtext('pic-slot') in pic_slots:
                                count += 1
                                if pic.findtext('pic-state').lower() == cmds and count == 2:
                                    t.log('fpc {} mic {} is {} now'.format(chosen[0], chosen[1], cmds))
                                    break_loop = True
                                    break
                        if break_loop:
                            break
                        retry = retry - 1
                        if retry == 0:
                            raise Exception("fpc {} mic {} failed to be {}".format(chosen[0], chosen[1], cmds))
            if action == 'panic':
                for cmds in ['detach', 'attach']:
                    command = "cprod -A fpc{} -c 'set parser security 10'".format(chosen[0])
                    resp = router.shell(command=command).resp
                    if not re.search('Security level set to 10', resp):
                        t.log('WARN', "Not supported for command {}".format(command))
                    command = "cprod -A fpc{} -c 'test mic {} {}'".format(chosen[0], cmds, chosen[1])
                    if cmds == 'attach':
                        command = command + ' 0'
                    router.shell(command=command)
                    if cmds == 'detach':
                        pic_state = 'offline'
                    if cmds == 'attach':
                        pic_state = 'online'
                    pic_slots = ['0', '1']
                    if chosen[1] == '1':
                        pic_slots = ['2', '3']
                    retry = 5
                    while True:
                        time.sleep(10)
                        break_loop = False
                        resp = router.pyez('get_pic_information', slot=chosen[0]).resp
                        count = 0
                        for pic in resp.findall('fpc/pic'):
                            if pic.findtext('pic-slot') in pic_slots:
                                count += 1
                                if pic.findtext('pic-state').lower() == pic_state and count == 2:
                                    t.log('fpc {} mic {} is {} now'.format(chosen[0], chosen[1], cmds))
                                    break_loop = True
                                    break
                        if break_loop:
                            break
                        retry = retry - 1
                        if retry == 0:
                            raise Exception("fpc {} mic {} failed to be {}".format(chosen[0], chosen[1], cmds))

    if verify_utils.convert_str_to_num_or_bool(check_client):
        try:
            t.log('verify subscriber count after FPC/PIC test')
            verify_client_count(subs=subs, device_id=device, check_access_route=check_access_route)
        except:
            t.log('subscriber lost during the test, needs rebinding')
            if cpu_check:
                BBEJunosUtil.cpu_settle(cpu_threshold=int(kwargs.get('cpu_process', 30)),
                                        idle_min=int(kwargs.get('cpu_settle', 75)),
                                        dead_time=int(kwargs.get('cpu_deadtime', 1200)),
                                        interval=int(kwargs.get('cpu_interval', 20)))
            #cst_release_clients(**kwargs)
            #cst_start_clients(**kwargs)
            t.log('start login subs after FPC Restart Test')
            if 'subs' in kwargs:
                subs_list = kwargs['subs']
                if not isinstance(subs_list, list):
                    subs_list = [subs_list]
                # kwargs.pop('subs')
            else:
                subs_list = bbe.get_subscriber_handles()
            interfaces = kwargs.get('interface_id', 'access')
            subs_interface = bbe.get_subscriber_handles(interface=interfaces)
            for subs in subs_interface:
                if subs not in subs_list:
                    subs_interface.remove(subs)
                else:
                    subs.stop()
                    time.sleep(60)
                    subs.abort()
                    time.sleep(60)
            try:
                cst_start_clients(restart_unbound_only=True, **kwargs)
            except:
                cst_start_clients(**kwargs)

    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        t.log('verify traffic after FPC/PIC test')
        unicast_traffic_test(**kwargs)


def daemon_restart_test(**kwargs):
    """
    daemon_restart_test(daemon_list=['jdhcpd','bbe-smgd'], re_in_action='re1',action='kill')
    :param kwargs:
    device_id:                device name e.g. 'r0'
    daemon_list:              a list of daemons
    action:                   restart/coredump/kill, by default is restart
    re_in_action:             re name, e.g. 're0'
    cpu_settle:               cpu idle value, by default is 75
    verify_traffic:           True/False, by default is true
    verify_client:            True/False, by default is true
    traffic_args:             dictionary for creating traffic which include name, rate, frame_size,
                              e.g.traffic_args = {'rate':'10%', 'frame_size':'1200'}
    cpu_check:                True/False
    :return:
    """
    check_traffic = kwargs.get('verify_traffic', True)
    if 'verify_traffic' in kwargs:
        kwargs.pop('verify_traffic')
    check_client = kwargs.get('verify_client', True)
    if 'verify_client' in kwargs:
        kwargs.pop('verify_client')
    dut_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    if 'device_id' in kwargs:
        kwargs.pop('device_id')
    daemon_actions(verify_traffic=check_traffic, verify_client=check_client, device_id=dut_id, **kwargs)


def login_logout_test(**kwargs):
    """
    login_logout_test(iteration=2)
    :param kwargs:
    device_id:              device name e.g. 'r0'
    cpu_settle:             cpu idle value, by default is 75
    cpu_check               True/False, default is True
    verify_traffic:         True/False, by default is True
    :return:
    """
    subs = kwargs.get('subs', bbe.get_subscriber_handles())
    cpu_check = kwargs.get('cpu_check', True)
    t.log('start login subs {} before test'.format(subs))
    try:
        cst_start_clients(restart_unbound_only=True, **kwargs)
    except:
        cst_start_clients(**kwargs)
    rt_device = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device)
    for iteration in range(1, int(kwargs.get('iteration', 2)) + 1):
        t.log("starting to logout clients in iteration {}".format(iteration))
        cst_release_clients(**kwargs)
        time.sleep(10)
        t.log("starting to login clients in iteration {}".format(iteration))
        cst_start_clients(**kwargs)

        verify_traffic_enable = kwargs.get('verify_traffic', True)
        if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
            new_mesh = kwargs.get('new_mesh', True)
            duration = kwargs.get('duration', 60)
            if new_mesh:
                t.log('remove existing traffic mesh')
                tester.invoke('traffic_action', action='delete')
                time.sleep(5)
                t.log('add new traffic mesh for subs in iteration {}'.format(iteration))
                add_subscriber_mesh(**kwargs)
            if 'duration' in kwargs:
                start_traffic(**kwargs)
            else:
                start_traffic(duration=duration, **kwargs)
            time.sleep(int(duration))
            verify_traffic(**kwargs)
        if cpu_check:
            BBEJunosUtil.cpu_settle(cpu_threshold=int(kwargs.get('cpu_process', 30)),
                                    idle_min=int(kwargs.get('cpu_settle', 75)),
                                    dead_time=int(kwargs.get('cpu_deadtime', 1200)),
                                    interval=int(kwargs.get('cpu_interval', 20)))

    t.log("login logout test iteration finished")


def interface_bounce_test(**kwargs):
    """

    :param kwargs:
    device_id:              device name e.g. 'r0'
    subs:                   subscriber object list
    interface_id:           interface id e.g. access0
    cpu_settle:             cpu settle idle ratio, default is 75
    cpu_check:              True/False, default is True
    verify_client:          verify client count after test
    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    cpu_check = kwargs.get('cpu_check', True)
    check_client = kwargs.get('verify_client', True)
    prepare_subscriber_traffic(**kwargs)

    t.log("starting interface bounce test")
    interface_id = kwargs.get('interface_id', 'access')
    access_interface = []
    access_list = bbe.get_interfaces(device=device_id, interfaces=interface_id)
    if access_list:
        for access in access_list:
            access_interface.append(access.interface_pic)
    command = []
    for interface in access_interface:
        command.append("set interface {} disable".format(interface))
        router.config(command_list=command)
    router.commit()

    time.sleep(30)

    command = []
    for interface in access_interface:
        command.append("delete interface {} disable".format(interface))
        router.config(command_list=command)
    router.commit()
    if cpu_check:
        BBEJunosUtil.cpu_settle(cpu_threshold=int(kwargs.get('cpu_process', 30)),
                                idle_min=int(kwargs.get('cpu_settle', 75)),
                                dead_time=int(kwargs.get('cpu_deadtime', 1200)),
                                interval=int(kwargs.get('cpu_interval', 20)))

    if verify_utils.convert_str_to_num_or_bool(check_client):
        t.log('start login subs after interface bounce test')
        if 'subs' in kwargs:
            subs_list = kwargs['subs']
            if not isinstance(subs_list, list):
                subs_list = [subs_list]
            #kwargs.pop('subs')
        else:
            subs_list = bbe.get_subscriber_handles()
        subs_interface = bbe.get_subscriber_handles(interface=interface_id)
        for subs in subs_interface:
            if subs not in subs_list:
                subs_interface.remove(subs)
            else:
                subs.stop()
                time.sleep(60)
                subs.abort()
                time.sleep(60)
        try:
            cst_start_clients(restart_unbound_only=True, **kwargs)
        except:
            cst_start_clients(**kwargs)


def ae_failover_test(**kwargs):
    """
    this testcase is suitable for AE between router and switch only,(IxNetwork does not support traffic reroute)
    :param kwargs:
    action:         switchover/deactivate/laseroff (deactivate is not supported by MX with sub)
    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    ae_members = get_ae_info(**kwargs)
    t.log("ae infomation is {}".format(ae_members))
    ae_active_list = []
    ae_protection_list = []
    aelist = kwargs.get('ae_list', [])
    for aename in ae_members:
        if aelist and aename not in aelist:
            continue
        if len(ae_members[aename]['active']) >= 2:
            ae_active_list.append(aename)
        elif 'standby' in ae_members[aename]:
            ae_protection_list.append(aename)
        else:
            t.log("ae {} only has one link".format(aename))
            continue

    if not ae_active_list and not ae_protection_list:
        t.log('WARN', "No qualified AE interface exists, quit this testcase")
        return

    prepare_subscriber_traffic(direction='down', **kwargs)
    start_traffic(**kwargs)
    action = kwargs.get('action', 'deactivate')
    t.log("start ae failover action {}".format(action))

    if action == 'switchover':
        if not ae_protection_list:
            t.log('WARN', "no AE in the router support link-switchover ")
            return
        for aename in ae_protection_list:
            t.log("check ae {} state before switch".format(aename))
            router.cli(command="show lacp interface {}".format(aename))
            resp = router.pyez('get_lacp_interface_information', interface_name=aename).resp
            for lacp_proto in resp.findall('lacp-interface-information/lag-lacp-protocol'):
                if lacp_proto.findtext('lacp-mux-state') == 'Collecting distributing':
                    pre_active_port = lacp_proto.findtext('name')
                    t.log("AE {} active port is {} before switch".format(aename, pre_active_port))
            router.cli(command='request lacp link-switchover {}'.format(aename))
            time.sleep(10)
            t.log("check ae state after switch")
            router.cli(command="show lacp interface {}".format(aename))
            resp = router.pyez('get_lacp_interface_information', interface_name=aename).resp
            for lacp_proto in resp.findall('lacp-interface-information/lag-lacp-protocol'):
                if lacp_proto.findtext('lacp-mux-state') == 'Collecting distributing':
                    post_active_port = lacp_proto.findtext('name')
                    t.log("AE {} active port is {} after switch".format(aename, post_active_port))
            if post_active_port == pre_active_port:
                raise Exception("AE {} failed to switch over".format(aename))

    if action == 'deactivate':
        if ae_protection_list:
            for aename in ae_protection_list:
                port = ae_members[aename]['active'][0]
                command = "deactivate interfaces {} gigether-options 802.3ad".format(port)
                router.config(command_list=[command])
                router.commit()
                time.sleep(10)
                router.cli(command="show lacp interface {}".format(aename))
                command = "activate interfaces {} gigether-options 802.3ad".format(port)
                router.config(command_list=[command])
                router.commit()
                router.cli(command="show lacp interface {}".format(aename))
        if ae_active_list:
            for aename in ae_active_list:
                port = random.choice(ae_members[aename]['active'])
                command = "deactivate interfaces {} gigether-options 802.3ad".format(port)
                router.config(command_list=[command])
                router.commit()
                time.sleep(10)
                router.cli(command="show lacp interface {}".format(aename))
                command = "activate interfaces {} gigether-options 802.3ad".format(port)
                router.config(command_list=[command])
                router.commit()
                router.cli(command="show lacp interface {}".format(aename))
    if action == 'laseroff':
        rt_device_id = kwargs.get('rt_device_id', 'rt0')
        rt_ae = get_ae_info(device_id=rt_device_id)
        tester = t.get_handle(rt_device_id)
        if not ae_protection_list:
            t.log('WARN', "no AE in the router support link-switchover ")
            return
        for aename in ae_protection_list:
            t.log("check ae state before switch")
            router.cli(command="show lacp interface {}".format(aename))
            resp = router.pyez('get_lacp_interface_information', interface_name=aename).resp
            for lacp_proto in resp.findall('lacp-interface-information/lag-lacp-protocol'):
                if lacp_proto.findtext('lacp-mux-state') == 'Collecting distributing':
                    pre_active_port = lacp_proto.findtext('name')
                    if pre_active_port in ae_members[aename]['active']:
                        rt_active_port = rt_ae[aename]['active'][0]
                    else:
                        rt_active_port = rt_ae[aename]['standby'][0]
                    t.log("router AE {} active port is {} before switch".format(aename, rt_active_port))
            tester.invoke('interface_config',
                          port_handle=tester.port_to_handle_map[rt_active_port], op_mode='sim_disconnect')
            time.sleep(10)
            router.cli(command="show lacp interface {}".format(aename))
            tester.invoke('interface_config', port_handle=tester.port_to_handle_map[rt_active_port], op_mode='normal')
            time.sleep(10)
            t.log("check ae state after switch")
            router.cli(command="show lacp interface {}".format(aename))
            resp = router.pyez('get_lacp_interface_information', interface_name=aename).resp
            for lacp_proto in resp.findall('lacp-interface-information/lag-lacp-protocol'):
                if lacp_proto.findtext('lacp-mux-state') == 'Collecting distributing':
                    post_active_port = lacp_proto.findtext('name')
                    t.log("AE {} active port is {} after switch".format(aename, post_active_port))
            if post_active_port == pre_active_port:
                raise Exception("AE {} failed to switch over".format(aename))

    t.log('verify clients and traffic after link action {}'.format(action))
    verify_client_count(**kwargs)
    stop_traffic()
    verify_traffic(**kwargs)


def reboot_and_rebind_test(**kwargs):
    """
    :param kwargs:
    device_id:          the device that reboot e.g. 'r0'
    verify_traffic:     True/False, by default is True
    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    verify_traffic_enable = kwargs.get('verify_traffic', True)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        prepare_subscriber_traffic(**kwargs)
    t.log("start reboot and rebind test")
    #if not router.reboot(wait=200, mode='cli', all=True):
    if not dev.reboot_device(device=router, all=True):
        raise Exception("REs failed to be online after reboot")
    t.log("router rebooted and come back online successfully")
    check_fpc(**kwargs)
    t.log("rebind subscribers after reboot")
    subs_interface = kwargs.get('subs', bbe.get_subscriber_handles())
    for subs in subs_interface:
        subs.stop()
        time.sleep(60)
        subs.abort()
        time.sleep(60)
    cst_start_clients(**kwargs)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        prepare_subscriber_traffic(**kwargs)
    t.log("reboot and rebind test finished")


def reboot_standby_re_test(**kwargs):
    """
    :param kwargs:
    device_id:          the device that reboot e.g. 'r0'
    verify_traffic:           True/False, by default is True
    traffic_args:
    :return:
    """
    verify_traffic_enable = kwargs.get('verify_traffic', True)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        prepare_subscriber_traffic(**kwargs)
        start_traffic(**kwargs)
    t.log("start reboot standby re test")
    re_actions(type='backup')
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        stop_traffic()
        verify_traffic(**kwargs)
    t.log("reboot_standby_re_test finished")


def port_laser_blink_test(**kwargs):
    """
    port_laser_blink_test(verify_traffic=False, laserofftime='10')
    :param kwargs:
    interface_type:        access/transit/custom/uplink, default is access
    device_id:             dut router id e.g. 'r0'
    laserofftime:          default is 600
    rebind:                True/False, default is True
    cpu_settle:            cpu idle settle ratio, default is 75
    cpu_check:             True/False
    :return:
    """
    status = True
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    cpu_check = kwargs.get('cpu_check', True)
    router = t.get_handle(device_id)
    prepare_subscriber_traffic(**kwargs)
    base_port_sum = get_router_sub_summary_by_port(device_id)
    interface_type = kwargs.get('interface_type', 'access')
    interfaces = bbe.get_interfaces(device_id, interfaces=interface_type)
    rebind = kwargs.get('rebind', True)
    if not interfaces:
        t.log('WARN', "the chosen interface type is not available in the router, quit this test")
        return
    local_remote_ports = {}
    for interface in interfaces:
        connection = bbe.get_connection(device_id, interface.interface_id)
        if connection:
            local_remote_ports[interface.interface_pic] = (connection.device_id, connection.interface_pic)

    dut_port_list = list(local_remote_ports.keys())
    if local_remote_ports:
        num_of_ports = random.choice(range(1, 1 + len(dut_port_list)))
        ##randomly pick ports
        picked_ports = random.sample(dut_port_list, num_of_ports)
        no_action_ports = [x for x in dut_port_list if x not in picked_ports]
        t.log("picked ports {} for test".format(picked_ports))
    else:
        t.log('WARN', "no connections for the interfaces, quit this test")
        return

    for port in picked_ports:
        remote_device = local_remote_ports[port][0]
        remote_port = local_remote_ports[port][1]
        remote_handle = t.get_handle(remote_device)

        for action in ['laseroff', 'laseron']:

            if 'rt' in remote_device:
                if action == 'laseroff':
                    op_mode = 'sim_disconnect'
                    expected_state = 'down'
                elif action == 'laseron':
                    op_mode = 'normal'
                    expected_state = 'up'
                rt_port_handle = remote_handle.port_to_handle_map[remote_port]
                remote_handle.invoke('interface_config', port_handle=rt_port_handle, op_mode=op_mode)
                if action == 'laseroff':
                    sleep_time = int(kwargs.get('laserofftime', 600))
                    t.log("will sleep {} before turn it on".format(sleep_time))
                    time.sleep(sleep_time)
                else:
                    time.sleep(5)


            elif re.match(r'^r(\d+)', remote_device):
                if action == 'laseroff':
                    expected_state = 'down'
                    command = ['set interfaces {} disable'.format(remote_port)]
                elif action == 'laseron':
                    expected_state = 'up'
                    command = ['delete interfaces {} disable'.format(remote_port)]
                remote_handle.config(command_list=command)
                remote_handle.commit()
                time.sleep(5)

            resp = router.pyez('get_interface_information', level_extra='terse', interface_name=port).resp
            state = resp.findtext('physical-interface/oper-status')
            if state != expected_state:
                t.log('ERROR', 'interface {} state is {} after set action {}'.format(port, state, action))
                status = False
            else:
                t.log('interface {} state is {} after set action {}'.format(port, state, action))

        new_stats_per_port = get_router_sub_summary_by_port(device_id)
        t.log("subscriber per port info {} after laser blink test".format(new_stats_per_port))

        t.log("checking non-action ports subscriber count")
        for no_action_port in no_action_ports:
            sum_port = None
            for sum_port in base_port_sum:
                if no_action_port in sum_port:
                    break

            if new_stats_per_port[sum_port] != base_port_sum[sum_port]:
                t.log('ERROR', "the subscriber count  {} in non-action port {} is different from the base count {}".
                      format(new_stats_per_port[sum_port], sum_port, base_port_sum[sum_port]))
                status = False
            else:
                t.log("the subscriber count  {} in non-action port {} is the same as the base count".
                      format(new_stats_per_port[sum_port], sum_port))

        if not kwargs.get('rebind', True):
            t.log("check all the subscribers after laser blink test")
            if new_stats_per_port != base_port_sum:
                t.log('ERROR', "the subscriber count per port changed")
                status = False
    if cpu_check:
        BBEJunosUtil.cpu_settle(cpu_threshold=int(kwargs.get('cpu_process', 30)),
                                idle_min=int(kwargs.get('cpu_settle', 75)),
                                dead_time=int(kwargs.get('cpu_deadtime', 1200)),
                                interval=int(kwargs.get('cpu_interval', 20)))
    if rebind:
        prepare_subscriber_traffic(**kwargs)

    if not status:
        raise Exception("port laser blink test failed")
    else:
        t.log("port laser blink test finished successfully")


def link_redundancy_test(**kwargs):
    """

    :param kwargs:
    device_id:          device id name e.g. 'r0'
    link_type:          interface link type e.g. access/uplink/transit/custom that has redundant link
    :return:
    """
    status = True
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    prepare_subscriber_traffic(**kwargs)
    ##collect ports that need to be tested
    port_list = []
    ae_info = get_ae_info(device_id=device_id)
    if ae_info:
        for ae_name in ae_info:
            port_list += ae_info[ae_name]['active']
            if 'standby' in ae_info[ae_name]:
                port_list += ae_info[ae_name]['standby']
    link_type = kwargs.get('link_type', 'access')
    bberouter = bbe.get_devices(devices=device_id)[0]
    if bberouter.is_mxvc:
        t.log("collect vcp ports")
        port_list += get_vcp_ports(device_id=device_id)['member0']

    if link_type in ['uplink', 'custom', 'transit']:
        interfaces = bbe.get_interfaces(device=device_id, interfaces=link_type)
        if len(interfaces) < 2:
            t.log('WARN', "no redundancy link for such type {}".format(link_type))

        for interface in interfaces:
            if interface.interface_pic not in port_list:
                port_list.append(interface.interface_pic)

    t.log("the possible redundant ports is {}".format(port_list))
    while port_list:
        picked_port = random.choice(port_list)
        t.log("choose port {} to do the redundant test".format(picked_port))
        port_list.remove(picked_port)
        try:
            interface_bounce(device_id=device_id, interface=picked_port, method='cli')
            verify_client_count(**kwargs)
            verify_client_route(**kwargs)
        except:
            status = False
            prepare_subscriber_traffic(**kwargs)

    if not status:
        raise Exception("link redundancy test failed")
    t.log('link redundancy test finished')


def no_radius_bind_test(**kwargs):
    """
    :param kwargs:
    :return:
    """
    try:
        cst_start_clients(**kwargs)
    except:
        t.log("failed to bring up subscriber")
    t.log('disable interface to radius')
    status = True
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    intf_obj = bbe.get_interfaces(device_id, interfaces='radius')[0]
    interface = intf_obj.interface_pic
    router.config(command_list=["set interface {} disable".format(interface), "commit"])

    time.sleep(5)
    resp = router.pyez('get_interface_information', level_extra='terse', interface_name=interface).resp
    state = resp.findtext('physical-interface/oper-status')

    if state != "down":
        t.log('ERROR', 'interface {} state is {} after disable'.format(interface, state))
        status = False
    else:
        t.log('interface {} state is {} after disable'.format(interface, state))

    if status:
        try:
            cst_start_clients(**kwargs)
        except:
            t.log("failed to bring up subscriber after disabling radius interface as expected")

        t.log('bring up interface to radius again')
        router.config(command_list=["delete interface {} disable".format(interface), "commit"])
        time.sleep(5)
        resp = router.pyez('get_interface_information', level_extra='terse', interface_name=interface).resp
        state = resp.findtext('physical-interface/oper-status')
        if state != "up":
            t.log('ERROR', 'interface {} state is {} after delete disable'.format(interface, state))
            status = False
        else:
            t.log('interface {} state is {} after delete disable'.format(interface, state))
            try:
                cst_start_clients(**kwargs)
            except:
                t.log("failed to bring up subscriber")
    if not status:
        raise Exception("no radius bind test failed")
    t.log("no radius bind test finished")


def ae_member_delete_add_test(**kwargs):
    """

    :param kwargs:
    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    ae_members = get_ae_info(**kwargs)
    status = True
    t.log("ae infomation is {}".format(ae_members))
    ae_active_list = []
    ae_protection_list = []
    port_list = []
    for aename in ae_members:
        if len(ae_members[aename]['active']) >= 2:
            ae_active_list.append(aename)
            port_list += ae_members[aename]['active']
        elif 'standby' in ae_members[aename]:
            ae_protection_list.append(aename)
            port_list += ae_members[aename]['standby']
        else:
            t.log("ae {} only has one link".format(aename))
            continue

    if not ae_active_list and not ae_protection_list:
        t.log('WARN', "No qualified AE interface exists, quit this testcase")
        return

    prepare_subscriber_traffic(direction='down', **kwargs)
    start_traffic(**kwargs)
    t.log("start AE memeber delete add test")
    for iteration in range(1, int(kwargs.get('iteration', 1)) + 1):
        for port in port_list:
            pre_resp = router.cli(command="show interfaces {} terse".format(port)).resp
            t.log("port {} configuration is going to be deleted")
            resp = router.cli(command="show configuration interfaces | display set | match {}".format(port)).resp
            command_list = resp.splitlines()
            t.log("command_list is {}".format(command_list))
            router.config(command_list=['delete interfaces {}'.format(port)])
            router.commit()
            t.log("sleeping 30s after delete the interface {}".format(port))
            time.sleep(30)
            try:
                verify_client_count(**kwargs)
            except:
                status = False
            t.log("Add port {} back to AE".format(port))
            router.config(command_list=command_list)
            router.commit()
            time.sleep(30)
            t.log("sleeping 30s after add the interface {}".format(port))
            after_resp = router.cli(command="show interfaces {} terse".format(port)).resp
            if after_resp != pre_resp:
                stop_traffic()
                raise Exception("the port {} state changed after delete/add".format(port))

            verify_client_count(**kwargs)

    stop_traffic()
    if not status:
        raise Exception("AE member add delete test failed")
    t.log("AE member add delete test finished")


def cgnat_traffic_test(**kwargs):
    """
    Tester need to configure the NAT themselves
    :param kwargs:
    device_id:          dut device id e.g. 'r0'
    rt_device_id:       tester device id e.g. 'rt0'
    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)

    prepare_subscriber_traffic(**kwargs)
    summary = get_router_sub_summary(device_id)
    t.log('router {} subscriber summary: {} before login'.format(device_id, summary))

    start_traffic(**kwargs)
    resp = router.pyez('service_msp_sess_count_information', timeout=1200).resp
    session_count = resp.findtext('service-msp-sess-count/sess-count')
    t.log("current session count is {}".format(session_count))
    if summary['client'] != session_count:
        raise Exception("the session count is not equal to the client count")
    else:
        stop_traffic()
        verify_traffic(**kwargs)
        t.log("CGNAT traffic test finished")


def lawful_intercept_test(**kwargs):
    """
    This test does not work now, since freeradius send out COA with LI information was not decoded correctly in Junos
    it seems the Unishphere-LI-Action should be in radius reply packets, not in CoA packets

    used for CoA lawful intercept test
    :param kwargs:
    device_id:                 device id name e.g. 'r0'
    client_count:              the client number that need to enable LI, default is 20
    radius_id:                 radius device id, default is h0
    radius_client_ip:          router ip address in radius server ,default is 100.0.0.1
    radius_secret:             radius secret, default is joshua
    verify_traffic:             True or False
    med_device_ip:              LI device ip
    med_device_port:            LI device port
    :return:
    """
    prepare_subscriber_traffic(**kwargs)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    client_count = int(kwargs.get('client_count', 20))
    ##get session ids
    resp = router.pyez('get_aaa_subscriber_table', timeout=600).resp
    session_ids = []
    for item in resp.findall('aaa-subscriber-table/aaa-subscriber-table-entry/session-id'):
        session_ids.append(item.text)
    if client_count > len(session_ids):
        client_count = len(session_ids)
    chosen_sessions = random.sample(session_ids, client_count)

    radius_id = kwargs.get('radius_id', 'h0')
    radius_handle = t.get_handle(radius_id)
    server_ip = kwargs.get('radius_client_ip', '100.0.0.1')
    password = kwargs.get('radius_secret', 'joshua')
    med_ip = kwargs.get('li_device_ip', '20.20.0.1')
    med_port = kwargs.get('li_device_port', 32000)
    ##Unisphere-Med-Dev-Handle=0x40000001 is a fixed value
    for session in chosen_sessions:
        command = "echo Acct-Session-Id={}, Unisphere-LI-Action=1, Unisphere-Med-Dev-Handle=0x40000001, " \
                  "Unisphere-Med-Ip-Address={}, Unisphere-Med-Port-Number={} | radclient -x {}:3799 coa {}". \
            format(session, med_ip, med_port, server_ip, password)
        resp = radius_handle.shell(command=command).resp
        if 'CoA-NAK' in resp:
            raise Exception("failed to activate lawful intercept using command {}".format(command))

    t.log("verify_traffic after LI activate")
    total_sub_count = get_router_sub_summary(device_id)['client']
    maximum_percent = (1 + client_count / total_sub_count) * kwargs.get('maximum_rx_percentage', '100.5')
    minimum_percent = (1 + client_count / total_sub_count) * kwargs.get('minimum_rx_percentage', '99.5')
    t.log("expecting received traffic will be {} - {} percent in LI".format(minimum_percent, maximum_percent))
    kwargs['maximum_rx_percentage'] = maximum_percent
    kwargs['minimum_rx_percentage'] = minimum_percent
    start_traffic(duration=60, **kwargs)
    time.sleep(60)
    verify_traffic(**kwargs)
    for session in chosen_sessions:
        command = "echo Acct-Session-Id={}, Unisphere-LI-Action=0 | radclient -x {}:3799 coa {}". \
            format(session, server_ip, password)
        resp = radius_handle.shell(command=command).resp
        if 'CoA-NAK' in resp:
            raise Exception("failed to deactivate lawful intercept using command {}".format(command))


def stress_test(**kwargs):
    """

    :param kwargs:
    device_id:          router id e.g. 'r0'
    rt_device_id:       tester id e.g. 'rt0'
    csr:                login rate list e.g.[400, 500]
    verify_traffic:     True or False, by default False
    :return:
    """
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    rt_handle = t.get_handle(rt_device_id)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    #router = t.get_handle(device_id)
    csr = kwargs.get('csr', 50)
    cst_stats_backup = bbe.cst_stats
    if not isinstance(csr, list):
        csr = [csr]
    current_login_rate = get_configured_subs()['expected_login_rate']
    # used to set the tester back to original rate
    csr.append(current_login_rate)
    #verify_traffic_enable = kwargs.get('verify_traffic', False)

    ##changing the CSR
    for rate in csr:
        if not isinstance(rate, float):
            rate = float(rate)
        cst_release_clients(**kwargs)
        prepare_router_before_login()
        if rate != current_login_rate:
            summary = get_router_sub_summary(device_id)
            if summary != 0:
                clear_subscribers_in_router(device_id=device_id)
                # router.reboot(wait=120, mode='cli', all=True)
                # cst.check_re_status(device_id=device_id)
                # check_fpc()
        ratio = rate / current_login_rate

        # modify the login rate
        dhcpv4_subs = bbe.get_subscriber_handles(protocol='dhcp', family='ipv4')
        if dhcpv4_subs:  # not an empty list, any handle is ok to rt api
            a_handle = dhcpv4_subs[0].rt_dhcpv4_handle
            rates = bbe.get_subscribers_call_rate('dhcp', 'ipv4')
            rates['login_rate'] = [round(x * ratio) for x in rates['login_rate']]
            rt_handle.invoke('set_dhcp_rate', handle=a_handle, login_rate=rates['login_rate'])

        # Set dhcpv6 rates
        dhcpv6_subs = bbe.get_subscriber_handles(family='ipv6') + bbe.get_subscriber_handles(family='dual')
        if dhcpv6_subs:  # not an empty list, any handle is ok to rt api
            a_handle = dhcpv6_subs[0].rt_dhcpv6_handle
            rates = bbe.get_subscribers_call_rate('dhcp', 'ipv6')
            rates['login_rate'] = [round(x * ratio) for x in rates['login_rate']]
            rt_handle.invoke('set_dhcp_rate', handle=a_handle, login_rate=rates['login_rate'])

        # Set pppoe rates
        pppoe_subs = bbe.get_subscriber_handles(protocol='pppoe')
        l2tp_subs = bbe.get_subscriber_handles(protocol='l2tp')
        pppoe_subs += l2tp_subs
        if pppoe_subs:  # not an empty list, any handle is ok to rt api
            a_handle = pppoe_subs[0].rt_pppox_handle
            rates = bbe.get_subscribers_call_rate('pppoe')
            rates['login_rate'] = [round(x * ratio) for x in rates['login_rate']]
            rt_handle.invoke('set_pppoe_rate', handle=a_handle, login_rate=rates['login_rate'])

        if rate != current_login_rate:
            # clear existing rt_login_rate
            if 'rt_login_rate' in bbe.cst_stats:
                rt_login_rate = bbe.cst_stats['rt_login_rate']
                bbe.cst_stats.pop('rt_login_rate')
            cst_start_clients(**kwargs)
            t.log("the current rt_login_rate is {} when csr was set to {}".format(rt_login_rate, rate))
        else:
            t.log("restore the bbe.cst_stats")
            bbe.cst_stats = cst_stats_backup
            cst_start_clients(**kwargs)


def radius_redundancy_test(**kwargs):
    """
    radius_redundancy_test()
    :param kwargs:
    device_id:                 router id e.g. 'r0'
    rt_device_id:              tester id e.g. 'rt0'
    radius_method:             default is stop
    radius_order:              radius order ['h0', 'h1']
    :return:
    """
    if len(bbe.get_devices(devices='h')) < 2:
        t.log('WARN', "There are less than 2 radius server, quit this test")
        return
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    method = kwargs.get('radius_method', 'stop')
    prepare_subscriber_traffic(verify_traffic=False, **kwargs)
    if 'radius_order' in kwargs:
        radius_order = kwargs['radius_order']
    else:
        radius_order = bbe.get_devices(devices='h', id_only=True)

    for iteration in range(1, int(kwargs.get('iteration', 1)) + 1):
        t.log("in iteration {}".format(iteration))
        for radius in radius_order:
            radius_handle = t.get_handle(radius)
            router.cli(command='clear network-access aaa statistics radius')
            router.cli(command='show network-access aaa radius-servers detail')
            sub_objs = bbe.get_subscriber_handles()
            picked_sub = random.choice(sub_objs)
            cst_release_clients(subs=picked_sub)
            t.log("radius {} will do action {}".format(radius, method))
            if method == 'stop':
                radius_handle.shell(command="/opt/JNPRsbr/radius/sbrd stop")
            else:
                resp = radius_handle.shell(command="ps aux |grep sbr.xml").resp
                match = re.match(r'root\s+(\d+).*', resp)
                if match:
                    pid = match.group(1)
                    radius_handle.shell(command="kill -9 {}".format(pid))
            t.log('sleep 20s for thw radius to shutdown completely')
            time.sleep(20)
            resp = radius_handle.shell(command="ps aux |grep sbr.xml").resp
            match = re.match(r'root\s+(\d+).*', resp)
            if not match:
                t.log("radius server has been shutdown")
            else:
                raise Exception("failed to shutdown radius server {}".format(radius))

            unicast_traffic_test(**kwargs)
            resp = router.cli(command='show network-access aaa radius-servers').resp
            if not re.search(r'DOWN', resp):
                raise Exception("router did not detect the radius {} was shutdown")
            t.log("restart radius {}".format(radius))

            radius_handle.shell(command="/opt/JNPRsbr/radius/sbrd start")
            t.log("waiting for radius {} to start".format(radius))
            time.sleep(30)
            resp = radius_handle.shell(command="ps aux |grep sbr.xml").resp
            match = re.match(r'root\s+(\d+).*', resp)
            if match:
                t.log("radius {} started successfuly".format(radius))
            else:
                raise Exception("raidus {} failed to be started".format(radius))


def bbe_issu_test(**kwargs):
    """
    :param kwargs:
    device_id:                  router id e.g. "r0"
    rt_device_id:               tester id e.g. "rt0"
    pre_issu_action:            action before ISSU, default is traffic
    post_issu_action:           action after ISSU, default is none
    upgrade_image:              the to_release build, take it from framework variable - software-install/to/release
    traffic_args:               dictionary for creating traffic which include name, rate,etc (check add subscriber mesh)
    minimum_rx_percentage:      minimum percentage for received traffic
    maximum_rx_percentage:      maximum percentage for received traffic
    dark_window:                the time that FPC stop forwarding during ISSU, default is 3
    check_show_cmds:            cli commands to check during ISSU
    check_show_cmds_max_runtime:        max runtime of check_show_cmds in seconds, default is 60s (DANGEROUS)
    verify_client:              verify_client after ISSU, default is True
    cpu_check:                  True/False
    no_copy:                    True/False, Default is False
    cleanfs:                    True/False, Default is False
    timeout:                    Issu timeout
    :return:
    """
    _check_bbe()
    device_id = kwargs.get("device_id", bbe.get_devices(device_tags="dut", id_only=True)[0])
    cpu_check = kwargs.get('cpu_check', True)
    no_copy = kwargs.get('no_copy', False)
    cleanfs = kwargs.get('cleanfs', False)
    timeout = kwargs.get('timeout', 3600)
    router = t.get_handle(device_id)
    t.log("do some test before issu")
    check_subs = kwargs.get('verify_client', True)
    pre_issu_action = kwargs.get("pre_issu_action", "traffic")
    if "traffic" in pre_issu_action:
        prepare_subscriber_traffic(**kwargs)
        start_traffic(**kwargs)
    if "gres" in pre_issu_action:
        gres_test(**kwargs)
    dark_window = int(kwargs.get("dark_window", 3))
    base_time = time.time()
    t.log("start ISSU now")
    package = kwargs["upgrade_image"]

    check_show_cmds = kwargs.get("check_show_cmds", ["show subscribers summary"])
    if not isinstance(check_show_cmds, list):
        check_show_cmds = [check_show_cmds]
    t.log("Running check_show_cmds once before ISSU")
    cli_checker = CheckCli(router, check_show_cmds)
    # Limit the time it takes to run the cmds because commands can be interrupted during ISSU
    max_runtime = int(kwargs.get("check_show_cmds_max_runtime", 60))
    if cli_checker.get_runtime() > max_runtime:
        t.log("check_show_cmds runtime is " + str(cli_checker.get_runtime()) + "s")
        t.log("check_show_cmds max runtime is " + str(max_runtime) + "s")
        raise Exception("check_show_cmds took too long to run, would cause problems during testing ISSU")

    t.log("start ISSU now with image {}".format(package))
    t.install_package(release=package, issu=True, timeout=timeout, cleanfs=cleanfs, no_copy=no_copy)
    t.log("after ISSU check")
    #router.set_current_controller(system_node='master', controller='master')

    t.log("Verifying check_show_cmds after ISSU...")
    cli_checker.verify_cli_output()
    t.log("Verified check_show_cmds after ISSU")
    if cpu_check:
        BBEJunosUtil.cpu_settle(cpu_threshold=int(kwargs.get('cpu_process', 30)),
                                idle_min=int(kwargs.get('cpu_settle', 75)),
                                dead_time=int(kwargs.get('cpu_deadtime', 1200)),
                                interval=int(kwargs.get('cpu_interval', 20)))
    if check_subs:
        verify_client_count(**kwargs)
        verify_client_route(**kwargs)
    if "traffic" in pre_issu_action:
        stop_traffic(**kwargs)
    duration = time.time() - base_time
    ratio = dark_window * 100 / duration
    post_issu_action = kwargs.get("post_issu_action", "none")
    if "traffic" in post_issu_action:
        if "minimum_rx_percentage" in kwargs:
            new_minimum = kwargs["minimum_rx_percentage"] - ratio
            kwargs["minimum_rx_percentage"] = new_minimum
        else:
            kwargs["minimum_rx_percentage"] = 99.0 - ratio
        verify_traffic(**kwargs)
    if "gres" in post_issu_action:
        gres_test(**kwargs)

def rid_coa_test(**kwargs):
    """

    :param kwargs:
    device_id:             router id e.g. 'r0'
    rt_device_id:          tester id e.g. 'rt0'
    client_type:           dhcp/pppoe/l2tp, default is dhcp
    count:                 the count of sessions do the coa test, default is 1
    nas_ip:                router nas ip, default is 100.0.0.1
    secret:                router radius secret, default is joshua
    action:                a dictionary of action and related params e.g. {'fname':'switch_re','kwargs':{'iteration':1}}
    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    radius_id = kwargs.get('radius_id', 'h0')
    radius_handle = t.get_handle(radius_id)
    prepare_subscriber_traffic(**kwargs)
    count = kwargs.get('count', 1)
    session_ids = get_session_ids(**kwargs)
    nas_ip = kwargs.get('nas_ip', '100.0.0.1')
    secret = kwargs.get('secret', 'joshua')
    dut_sum_before = get_router_sub_summary(device_id)
    rt_sum_before = get_rt_subs_info(**kwargs)
    pre_count = dut_sum_before['client']
    t.log("subscribers in router before test is {},"
          " subscribers in rt before test is {}".format(dut_sum_before, rt_sum_before))
    chosen_ids = [random.choice(session_ids) for i in range(count)]
    dicts = kwargs.get('action', None)
    ###start action in background
    if dicts:
        args = dicts.get('args', [])
        kwargs = dicts.get('kwargs', {})
        action = dicts.get('fname')
        delay = dicts.get('delay', 0)
        time.sleep(delay)
        t.log('args is {}, kwargs is {}, fname is {}'.format(args, kwargs, action))
        if isinstance(action, str):
            action = eval(action)
        action_thread = Thread(target=action, args=args, kwargs=kwargs)
        action_thread.start()
        time.sleep(.1)
        if action_thread.is_alive():
            t.log('successfully kicked off action {} with args {}, kwargs {}'.format(action, args, kwargs))
        else:
            t.log('unable to kick off action {} with args {}, kwargs {}'.format(action, args, kwargs))
    for session_id in chosen_ids:
        command = "echo 'Acct-Session-Id={}' | radclient -x {}:3799 disconnect {}".format(session_id, nas_ip, secret)
        radius_handle.shell(command=command)
    if dicts:
        while action_thread.is_alive():
            time.sleep(10)
        t.log("action {} finished")
    t.log("checking dut count and rt count")
    dut_sum = get_router_sub_summary(device_id)
    rt_sum = get_rt_subs_info(**kwargs)
    after_count = dut_sum['client']
    t.log("subscribers in router after test is {}, subscribers in rt after test is {}".format(dut_sum, rt_sum))
    diff = pre_count - after_count - len(chosen_ids)
    if diff != 0:
        raise Exception("{} of the clients failed to be disconnected from router".format(diff))

    t.log("restart all clients after testing")
    prepare_subscriber_traffic(**kwargs)


def clean_rebind_test(**kwargs):
    """
    The testcase requires switch between RT and DUT. Ideally with short DHCP lease time.
	Bring down all switch accessing ports and allow DUT to detect connection down and clear all subscribers upon lease
	expiration or keepalive failure and then rebind them.
	Good for longevity test to make sure no memory leak and such function can sustain large scale and long time.
    :param kwargs:
    switch_id:              switch device id e.g. 'r1', default is 'r1'
    device_id:              router device id, e.g. 'r0', default is dut id
    iteration:              iteration number, default is 1
    :return:
    """
    if 'verify_traffic' not in kwargs:
        kwargs['verify_traffic'] = False
    prepare_subscriber_traffic(**kwargs)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    switch_id = kwargs.get('switch_id', 'r1')
    switch_handle = t.get_handle(switch_id)
    switch_access_intf = bbe.get_interfaces(switch_id, interfaces='access')
    status = True
    for iteration in range(1, int(kwargs.get('iteration', 1)) + 1):
        t.log("disable access ports in switch in iteration #{}".format(iteration))
        port_command_list = []
        status = True
        for access in switch_access_intf:
            port_command_list.append("set interfaces {} disable".format(access.interface_pic))
        switch_handle.config(command_list=port_command_list)
        switch_handle.commit()
        t.log("verify access ports in down state")
        for access in switch_access_intf:
            resp = switch_handle.pyez('get_interface_information', level_extra='terse',
                                      interface_name=access.interface_pic).resp
            if resp.findtext('physical-interface/admin-status') == 'down' and resp.findtext(
                    'physical-interface/oper-status') == 'down':
                t.log("interface {} is in down state".format(access.interface_pic))
            else:
                t.log('WARN', "interface {} is in state {}".format(access.interface_pic, resp))
                status = False

        if not status:
            for access in switch_access_intf:
                port_command_list.append("delete interfaces {} disable".format(access.interface_pic))
            switch_handle.config(command_list=port_command_list)
            switch_handle.commit()
            raise Exception("some interfaces failed to be in down state after disable")
        base_time = time.time()
        while time.time() - base_time < 1800:
            router_count = get_router_sub_summary(device_id)['client']
            tester_count = get_rt_subs_info()['rt_sessions_up']
            if router_count == 0 and tester_count == 0:
                duration = time.time() - base_time
                t.log("all subscribers cleared from tester and router after {}s in iteration #{}".format(duration,
                                                                                                         iteration))
                break
            t.log("sleep 30s , waiting for clients cleared")
            time.sleep(30)

        result = get_router_sub_summary(device_id)

        if result['client'] != 0 or 'terminated' in result or 'terminating' in result or 'init' in result:
            status = False
            t.log('WARN', 'some subscribers stuck in unexpected state in iteration #{}'.format(iteration))

        for access in switch_access_intf:
            port_command_list.append("delete interfaces {} disable".format(access.interface_pic))
        switch_handle.config(command_list=port_command_list)
        switch_handle.commit()
        time.sleep(10)
        t.log("verify access ports in up state in iteration {}".format(iteration))
        for access in switch_access_intf:
            resp = switch_handle.pyez('get_interface_information', level_extra='terse',
                                      interface_name=access.interface_pic).resp
            if resp.findtext('physical-interface/admin-status') == 'up' and resp.findtext(
                    'physical-interface/oper-status') == 'up':
                t.log("interface {} is in up state".format(access.interface_pic))
            else:
                t.log('WARN', "interface {} is in state {}".format(access.interface_pic, resp))
                status = False

        if not status:
            raise Exception("clean test failed")
        ##set the rt subscriber state to stopped, since it is not teared down by actions
        t.log("login subscriber and verify traffic after restore the connection in iteration #{}".format(iteration))
        prepare_subscriber_traffic(**kwargs)


def subscriber_delete_test(**kwargs):
    """
    subscriber_delete_test(method='radius', client_type='dhcp', client_count=20)
    :param kwargs:
    iteration:              iteration number, default is 1
    method:                     'radius'/'cli', default is cli
    device_id:                  device id name e.g. 'r0'
    client_type:                client type , dhcp/pppoe/l2tp/dhcpv6, default is pppoe
    client_count:               client count
    #interface_list:            the interfaces list needs to be cleared(used for pppoe/l2tp)
    #session_id_list:           session id list used for dhcp or radius
    radius_id:                 radius device id, default is h0
    radius_client_ip:          router ip address in radius server ,default is 100.0.0.1
    radius_secret:             radius secret, default is joshua
    verify_traffic:            True or False, by default False
    :return:
    """
    verify_traffic_enable = kwargs.get('verify_traffic', False)
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        prepare_subscriber_traffic(**kwargs)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    client_type = kwargs.get('client_type', 'pppoe')
    interface_list = []
    session_id_list = []
    client_count = int(kwargs.get('client_count', 100))
    cst_start_clients(**kwargs)
    count_before_test = 0
    for iteration in range(1, int(kwargs.get('iteration', 1)) + 1):
        # dev_obj = t.get_handle(device_id)
        # resp = dev_obj.cli(command="show subscribers summary", timeout=600).resp
        # if 'error' in resp:
        #     raise Exception("show subscriber summary returns error with {}".format(resp))
        # subs = dev_obj.pyez('get_subscribers_summary', all=True, normalize=True, timeout=600).resp
        # if subs.getnext():
        #     subs = subs.getnext()
        # for counter in subs.findall('counters'):
        #     if client_type == 'pppoe':
        #         if counter.findtext('session-type-pppoe'):
        #             count_before_test = int(counter.findtext('session-type-pppoe'))
        #     elif client_type == 'dhcp':
        #         if counter.findtext('session-type-dhcp'):
        #             count_before_test = int(counter.findtext('session-type-dhcp'))
        #     elif client_type == 'l2tp':
        #         if counter.findtext('session-type-l2tp'):
        #             count_before_test = int(counter.findtext('session-type-l2tp'))
        count_before_test = get_router_sub_summary(device_id)['client']
        t.log("there are {} clients in iteration #{} before test".format(count_before_test, iteration))
        result = get_session_ids(return_session_detail=True, **kwargs)
        for element in result:
            interface_list.append(element.findtext('interface'))
            session_id_list.append(element.findtext('session-id'))
        if client_count > len(session_id_list):
            client_count = len(session_id_list)
        chosen_interfaces = random.sample(interface_list, client_count)
        chosen_sessions = random.sample(session_id_list, client_count)
        t.log("start to clean chosen interfaces or sessions {}".format(chosen_sessions))
        t.log("kwargs is {}".format(kwargs))
        clear_subscriber_sessions(interface_list=chosen_interfaces, session_id_list=chosen_sessions, **kwargs)
        #pdb.set_trace()
        # resp = dev_obj.cli(command="show subscribers summary", timeout=600).resp
        # if 'error' in resp:
        #     raise Exception("show subscriber summary returns error with {}".format(resp))
        # subs = dev_obj.pyez('get_subscribers_summary', all=True, normalize=True, timeout=600).resp
        # if subs.getnext():
        #     subs = subs.getnext()
        # for counter in subs.findall('counters'):
        #     for counter in subs.findall('counters'):
        #         if client_type == 'pppoe' or client_type == 'l2tp':
        #             count_after_test = int(counter.findtext('session-type-pppoe'))
        #         elif client_type == 'dhcp':
        #             count_after_test = int(counter.findtext('session-type-dhcp'))
        count_after_test = get_router_sub_summary(device_id)['client']
        t.log("there are {} clients after iteration #{}".format(count_after_test, iteration))

        if count_before_test - count_after_test == client_count:
            t.log("the chosen {} clients has been cleared in iteration #{}".format(client_count, iteration))
            if 'dhcp' in client_type:
                rt_device_id = kwargs.get('rt_device_id', 'rt0')
                rt_handle = t.get_handle(rt_device_id)
                t.log(" needs to send out renew from tester")
                for subs in bbe.get_subscriber_handles():
                    if subs.rt_dhcpv4_handle:
                        rt_handle.invoke('dhcp_client_action', handle=subs.rt_dhcpv4_handle, action='renew')
                    if subs.rt_dhcpv6_handle:
                        rt_handle.invoke('dhcp_client_action', handle=subs.rt_dhcpv6_handle, action='renew')
                wait_time = round(count_before_test / 200)
                t.log("waiting {}s dhcp clients to send renew".format(wait_time))
                time.sleep(wait_time)
            if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
                prepare_subscriber_traffic(**kwargs)
        else:
            raise Exception("please check the router, some subscribers have not been cleared")


def service_activate_deactive_test(**kwargs):
    """
    echo Acct-Session-Id=125970,Unisphere-Activate-Service='pppoe-client-profile'|radclient -x 100.0.0.1:3799 coa joshua
    :param kwargs:
    service_name(mandatory):    the service needs to be activate
    iteration:                  iteration number, default is 1
    method:                     'radius'/'cli', default is cli
    device_id:                  device id name e.g. 'r0'
    client_type:                client type , dhcp/pppoe/l2tp/dhcpv6, default is pppoe
    #interface_list:            the interfaces list needs to be cleared(used for pppoe/l2tp)
    #session_id_list:           session id list used for dhcp or radius
    radius_id:                  radius device id, default is h0
    radius_client_ip:           router ip address in radius server ,default is 100.0.0.1
    radius_secret:              radius secret, default is joshua
    verify_traffic:             True or False
    :return:
    """
    service_name = kwargs['service_name']
    prepare_subscriber_traffic(**kwargs)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    client_count = int(kwargs.get('client_count', 20))
    method = kwargs.get('method', 'cli')
    ##get session ids
    resp = router.pyez('get_aaa_subscriber_table', timeout=600).resp
    session_ids = []
    for item in resp.findall('aaa-subscriber-table/aaa-subscriber-table-entry/session-id'):
        session_ids.append(item.text)
    if client_count > len(session_ids):
        client_count = len(session_ids)
    chosen_session = random.sample(session_ids, client_count)
    for iteration in range(1, int(kwargs.get('iteration', 1)) + 1):
        t.log("starting to activate/deactivate service using method {} in iteration #{}".format(method, iteration))
        if method == 'radius':
            radius_id = kwargs.get('radius_id', 'h0')
            radius_handle = t.get_handle(radius_id)
            server_ip = kwargs.get('radius_client_ip', '100.0.0.1')
            password = kwargs.get('radius_secret', 'joshua')
            for session in chosen_session:
                command = "echo Acct-Session-Id={},Unisphere-Activate-Service-tag1={} | radclient -x {}:3799 coa {}". \
                    format(session, service_name, server_ip, password)
                resp = radius_handle.shell(command=command).resp
                if 'CoA-NAK' in resp:
                    raise Exception("failed to active service using command {}".format(command))

            time.sleep(10)
            for session in chosen_session:
                command = "echo Acct-Session-Id={},Unisphere-Deactivate-Service={} | radclient -x {}:3799 coa {}". \
                    format(session, service_name, server_ip, password)
                resp = radius_handle.shell(command=command).resp
                if 'CoA-NAK' in resp:
                    raise Exception("failed to deactive service using command {}".format(command))

        if method == 'cli':
            for action in ['activate', 'deactivate']:
                for session in chosen_session:
                    command = "request network-access aaa subscriber {} session-id {} service-profile {}". \
                        format(action, session, service_name)
                    resp = router.cli(command=command).resp
                    if 'Successful' not in resp:
                        raise Exception("failed to {} service using command {}".format(action, command))
                    time.sleep(10)
        if 'verify_traffic' in kwargs and kwargs['verify_traffic']:
            start_traffic(**kwargs)
            time.sleep(60)
            stop_traffic()
            verify_traffic(**kwargs)


def image_upgrade_test(**kwargs):
    """
    Generic image upgrade action, Supporting two styles:  'reload' and 'switchover'
    :param kwargs:
    style:                         reload/switchover, default is reload
    device_id:                     device id name e.g. 'r0'
    image_file:                    upgrade image location and file
    new_mesh:                      create new traffic mesh(True/False)
    subs:                          subs involved in traffic (see add_susbcriber_mesh)
    duration:                      traffic running time, by default is 60 seconds
    traffic_args:                  dictionary for creating traffic which include name, rate, frame_size, etc
                                   (check add_subscriber_mesh in cstutils.py)
    minimum_rx_percentage:         minimum percentage for received traffic
    maximum_rx_percentage:         maximum percentage for received traffic
    :return:
    """
    image_file = kwargs['image_file']
    upgrade_style = kwargs.get('style', 'reload')
    prepare_subscriber_traffic(**kwargs)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    start_traffic(**kwargs)

    if upgrade_style == 'reload':
        t.log("Upgrading image via reload on both REs")
        router.software_install(package=image_file, progress=True, no_copy=True, timeout=3600)
        stop_traffic()
        unicast_traffic_test(**kwargs)
    if upgrade_style == 'switch':
        t.log("Upgrading image via RE switch")
        router.software_install(package=image_file, issu=True, progress=True, no_copy=True, timeout=3600)
        stop_traffic()
        verify_traffic(**kwargs)
        verify_client_count(**kwargs)


def bbe_http_redirect_test(**kwargs):
    """

    :param kwargs:
    client_count:            client count that is chosen for activate/deactivate http redirect service
    client_type:             client type to get session ids from the router
    device_id:               device id name e.g. 'r0'
    service_profile:         service profile name
    service_interface:       service interface

    :return:
    """
    t.log("inside http_redirect test, kwargs is {}".format(kwargs))
    client_type = kwargs.get('client_type', 'dhcp')
    client_count = int(kwargs.get('client_count', '1'))
    service_name = kwargs['service_profile']
    service_interface = kwargs['service_interface']
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device_id)
    subs = kwargs.get('subs', bbe.get_subscriber_handles())
    action = kwargs.get('action', 'activate')
    t.log('start login subs {} before test'.format(subs))
    try:
        cst_start_clients(restart_unbound_only=True, **kwargs)
    except Exception:
        t.log("got exception with restart_unbound_only, will try login without this arg")
        cst_start_clients(**kwargs)
    session_ids = get_session_ids(device_id=device_id, client_type=client_type, count=client_count)
    t.log("clear cpcd stats")
    router.cli(command="clear services captive-portal-content-delivery"
                       " statistics interface {}".format(service_interface))
    router.cli(command='clear firewall all')
    t.log("activate http redirect service")
    subscriber_service_action(device_id=device_id, service_name=service_name,
                              method='cli', session_id_list=session_ids, action=action)

    t.log("Add http traffic")
    v4_src_handle = []
    v4_dst_handle = []
    for subscriber in subs:
        if subscriber.family == 'ipv4':
            if subscriber.subscribers_type == 'dhcp':
                v4_src_handle.append(subscriber.rt_dhcpv4_handle)
            if subscriber.subscribers_type in ['pppoe', 'l2tp']:
                v4_src_handle.append(subscriber.rt_pppox_handle)

    uplinks = kwargs.get('uplinks', bbe.get_interfaces(rt_device_id, interfaces='uplink', id_only=False))

    for uplink in uplinks:
        if uplink.device_id != rt_device_id:
            t.log("uplink {} is not on this rt {}".format(uplink, rt_device_id))
            continue
        if uplink.rt_lns_server_session_handle:
            v4_dst_handle.append(uplink.rt_lns_server_session_handle)
        elif uplink.rt_ipv4_handle:
            v4_dst_handle.append(uplink.rt_ipv4_handle)

    ###http redirect traffic for Ixia only
    result = tester.invoke('traffic_l47_config', mode='create', emulation_src_handle=v4_src_handle,
                           emulation_dst_handle=v4_dst_handle, circuit_endpoint_type='ipv4_application_traffic',
                           flows="HTTP_302_Redirect_Juniper")
    traffic_handle = result['traffic_l47_handle']
    tester.invoke('traffic_l47_config', mode='modify', stream_id=traffic_handle, l47_configuration=
                  'modify_flow_percentage', flow_percentage='100', flow_id='HTTP_302_Redirect_Juniper')
    tester.invoke('traffic_control', type='l47', traffic_generator='ixnetwork_540', action='run')
    time.sleep(30)
    tester.invoke('traffic_control', type='l47', traffic_generator='ixnetwork_540', action='stop')

    resp = router.pyez('get_cpcd_pic_statistics', pic_name=service_interface, timeout=600).resp
    pkts_rx = int(resp.findtext('statistics/packets-received'))
    pkts_altered = int(resp.findtext('statistics/packets-altered'))
    if pkts_rx > 0 and pkts_altered > 0:
        t.log("http get packets was redirected successfully")
    else:
        raise Exception("no http get packets was redirected")
    subscriber_service_action(device_id=device_id, service_name=service_name,
                              method='cli', session_id_list=session_ids, action='deactivate')
    tester.invoke('traffic_control', type='l47', traffic_generator='ixnetwork_540', action='run')
    time.sleep(30)
    tester.invoke('traffic_control', type='l47', traffic_generator='ixnetwork_540', action='stop')

    resp = router.pyez('get_cpcd_pic_statistics', pic_name=service_interface, timeout=600).resp
    pkts_rx2 = int(resp.findtext('statistics/packets-received'))
    pkts_altered2 = int(resp.findtext('statistics/packets-altered'))
    if pkts_rx2 == pkts_rx and pkts_altered2 == pkts_altered:
        t.log("no packets was redirected when redirect service is deactivated")
    else:
        raise Exception("packets should not be redirected when redirect service is deactivated")
