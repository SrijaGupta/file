"""
CST Test Suites
"""
import time
from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil
import random
import re
import jnpr.toby.bbe.cst.cstutils as cst
import jnpr.toby.bbe.cst.dtcp_suites as dtcp
import jnpr.toby.bbe.cst.cst_healthcheck as hk


def mxvc_vcp_link_down_test(**kwargs):
    """
    The method simulates the event of vcp link down
    Caution, this method did not simulate the reality problem, since it use delete the port from the vcp .
    the better idea is to use pswitch to build the vcp links
    :param kwargs:
    device_id:                     device name, e.g.'r0'
    new_mesh:                      create new traffic mesh(True/False)
    subs:                          subs involved in traffic (see add_susbcriber_mesh)
    duration:                      traffic running time, by default is 60 seconds
    remove_traffic_after_test:     remove traffic items after test, by default is True
    traffic_args:                  dictionary for creating traffic which include name, rate, frame_size, etc
                                   (check add_subscriber_mesh in cstutils.py)
    mininum_rx_percentage:         minimum percentage for received traffic
    maximum_rx_percentage:         maximum percentage for received traffic
    iteration:                     iteration count
    style:                         'single' => one down only,  'all' => all down, default is single
    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    cst.prepare_subscriber_traffic(**kwargs)
    cst.start_traffic(**kwargs)
    t.log("collect vcp ports")
    status = True
    router.cli(command="show virtual-chassis vc-port")
    master_re = cst.get_master_re_name(device_id)
    master_node = master_re.split(sep='-')[0]
    rename = master_re.split(sep='-')[1]
    router.set_current_controller(system_node=master_node, controller=rename)
    member = master_node
    if master_node == 'primary':
        member = 'member0'
    port_list = cst.get_vcp_ports(device_id=device_id)[member]
    style = kwargs.get('style', 'single')
    chosen_links = port_list
    if style == 'single':
        chosen_links = [random.choice(port_list)]
    ### save vcp link state before any action
    resp = []
    for link in chosen_links:
        resp.append(router.cli(command="show interface {} terse".format(link)))
    ### show subscriber info before event, on master re
    router.cli(command='show subscribers summary port')
    sub_sum_pre_action = cst.get_router_sub_summary_by_port(device_id)
    iteration = int(kwargs.get('iteration', 1))
    count = 1
    status_action = {'link_down': 'delete', 'link_up': 'set'}
    while count <= iteration:
        for event in ['link_down', 'link_up']:
            resp2 = []
            for link in chosen_links:
                match = re.match(r'vcp-(\d+)/(\d+)/(\d+)', link)
                t.log("start action {} on link {} in iteration #{}".format(event, link, count))
                router.cli(command="request virtual-chassis vc-port {} fpc-slot {} pic-slot {} port {}"
                                   "".format(status_action[event], match.group(1), match.group(2), match.group(3)))
                time.sleep(60)
                router.cli(command="show virtual-chassis vc-port")
                ### show subscriber info after event, on master re
                router.cli(command='show subscribers summary port')
                sub_sum_after_action = cst.get_router_sub_summary_by_port(device_id)
                if sub_sum_after_action != sub_sum_pre_action:
                    t.log('ERROR', "subscriber changed from {} to {}".format(sub_sum_pre_action, sub_sum_after_action))
                    status = False
                    sub_sum_pre_action = sub_sum_after_action
                cst.stop_traffic(**kwargs)
                cst.verify_traffic(**kwargs)
                cst.start_traffic(**kwargs)
                if event == 'link_up':
                    resp2.append(router.cli(command="show interface {} terse".format(link)))

        count += 1
        if resp != resp2:
            status = False
            t.log('ERROR, "vcp interface state changed from {} to {} after actions'.format(resp, resp2))
            break
        if not status:
            cst.stop_traffic()
            raise Exception("mxvc vcp link down test failed in iteration {}".format(count))
    cst.stop_traffic()



def mxvc_chassis_reboot(**kwargs):
    """
    The method simulates the event of backup/master chassis reboot in a MXVC setup
    which will be used by VCMasterReboot/vcStandbyREReboot/VCMasterPowerCycle/VCBackupReboot/VCBackupPowerCycle
    :param kwargs:
    device_id:                     device name, e.g.'r0'
    new_mesh:                      create new traffic mesh(True/False)
    subs:                          subs involved in traffic (see add_susbcriber_mesh)
    duration:                      traffic running time, by default is 60 seconds
    traffic_args:                  dictionary for creating traffic which include name, rate, frame_size, etc
                                   (check add_subscriber_mesh in cstutils.py)
    mininum_rx_percentage:         minimum percentage for received traffic
    maximum_rx_percentage:         maximum percentage for received traffic
    chassis:                       reboot chassis, e.g. 'VC-M' or 'VC-B' or 'VC-STDBY-RE-ALL'
    method:                        'cli' or 'powercycle', default is cli
    post_action_wait_time:         wait time in seconds, default is 600
    health_check:                  collect health check info, default is False
    :return:
    """
    post_action_wait_time = int(kwargs.get('post_action_wait_time', 600))
    dtcp_test = kwargs.get('dtcp_test', False)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    reboot_chassis = kwargs.get('chassis', 'VC-B').upper()
    method = kwargs.get('method', 'cli')
    health_check = kwargs.get('health_check', False)
    cst.prepare_subscriber_traffic(**kwargs)
    if dtcp_test:
        dtcp.dtcp_delete_li_trigger()
        dtcp.dtcp_add_li_trigger()
    cst.start_traffic(**kwargs)
    router.cli(command='show virtual-chassis vc-port')
    if health_check:
        cst.get_re_fpc_memory()
        hk.healthcheck_pfe_resource_monitor()
        hk.healthcheck_get_task_memory()
        hk.healthcheck_run_pfe_command(command='show heap 0 accounting pc')
        hk.healthcheck_run_pfe_command(command='show pfe manager session statistics')

    master_node = router.detect_master_node()
    cst.check_gres_ready(device_id)

    ###reboot chassis REs
    if method == 'cli':
        if reboot_chassis == 'VC-STDBY-RE-ALL':
            router.cli(command="request system reboot all-members other-routing-engine")
        elif reboot_chassis == 'VC-M':
            if master_node == 'primary':
                slot = '0'
            else:
                slot = '1'
            command = "request system reboot member {} both-routing-engines".format(slot)
            router.cli(command=command, pattern='yes,no')
            router.cli(command='yes')
        elif reboot_chassis == 'VC-B':
            if master_node == 'primary':
                slot = '1'
            else:
                slot = '0'
            command = "request system reboot member {} both-routing-engines".format(slot)
            router.cli(command=command, pattern='yes,no')
            router.cli(command='yes')
    if method == 'powercycle':
        hostname = router.current_node.current_controller.name
        cst.power_manager(chassis=hostname, action='cycle')
    t.log("waiting for {} seconds after reboot".format(post_action_wait_time))
    time.sleep(post_action_wait_time)
    router.reconnect(all)
    master_node = router.detect_master_node()
    master_re = cst.get_master_re_name(device_id).split(sep='-')[1]
    router.set_current_controller(system_node=master_node, controller=master_re)
    BBEJunosUtil.cpu_settle(cpu_threshold=20, idle_min=int(kwargs.get('cpu_settle', '75')),
                            dead_time=1200, interval=20)
    router.cli(command='show virtual-chassis status')
    if health_check:
        cst.get_re_fpc_memory()
        hk.healthcheck_pfe_resource_monitor()
        hk.healthcheck_get_task_memory()
        hk.healthcheck_run_pfe_command(command='show heap 0 accounting pc')
        hk.healthcheck_run_pfe_command(command='show pfe manager session statistics')
    t.log('verify client count after action {}'.format(method))
    cst.verify_client_count(device_id=device_id)
    t.log('verify client traffic after action {}'.format(method))
    cst.stop_traffic(**kwargs)
    cst.verify_traffic(**kwargs)
    if dtcp_test:
        t.log("remove dtcp trigger after action {}".format(method))
        dtcp.dtcp_delete_li_trigger()


def mxvc_blackout_period_test(**kwargs):
    """
    The MXVC blackout period test, must have dhcp clients, which used to test blackout
    :param kwargs:
    device_id:                      device name, e.g.'r0'
    new_mesh:                      create new traffic mesh(True/False), default is true
    subs:                          subs involved in traffic (see add_susbcriber_mesh)
    duration:                      traffic running time, by default is 60 seconds
    remove_traffic_after_test:     remove traffic items after test, by default is True
    traffic_args:                  dictionary for creating traffic which include name, rate, frame_size, etc
                                   (check add_subscriber_mesh in cstutils.py)
    mininum_rx_percentage:         minimum percentage for received traffic
    maximum_rx_percentage:         maximum percentage for received traffic

    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    dtcp_test = kwargs.get('dtcp_test', False)
    if dtcp_test:
        dtcp.dtcp_delete_li_trigger()
        dtcp.dtcp_add_li_trigger()
    cst.prepare_subscriber_traffic(**kwargs)
    cst.start_traffic()
    initial_master_re = cst.get_master_re_name(device_id)
    clients_info = cst.get_router_sub_summary(device_id)
    t.log("subscriber info before blackout period test is {}".format(clients_info))
    cst.get_vcp_ports(device_id=device_id)
    cst.check_fpc(device_id=device_id)
    timeout = kwargs.get('gres_check_timeout', 1800)
    t.log("releasing the dhcp susbcribers for blackout test")
    subs = bbe.get_subscriber_handles(protocol='dhcp')
    t.log("checking GRES ready state before test")
    cst.check_gres_ready(device_id, check_timeout=timeout)
    cst.cst_release_clients(subs=subs)
    health_check = kwargs.get('health_check', False)
    if health_check:
        cst.get_re_fpc_memory()
        hk.healthcheck_pfe_resource_monitor()
        hk.healthcheck_get_task_memory()
        hk.healthcheck_run_pfe_command(command='show heap 0 accounting pc')
        hk.healthcheck_run_pfe_command(command='show pfe manager session statistics')

    command_list = ['show chassis fpc', 'show virtual-chassis vc-port', 'show virtual-chassis status',
                    'show route summary', 'show route forwarding-table summary']

    ### log something before GRES
    for command in command_list:
        router.cli(command=command)

    rt_output = cst.get_rt_subs_info()
    base_up_subs_in_rt = rt_output['rt_sessions_up']
    base_down_subs_in_rt = rt_output['rt_sessions_down']
    result = cst.get_configured_subs(subs=subs)
    expected_subs_in_rt = result['expected_total_session_in_testers']
    t.log("starting GRES, and then rebinding subscribers")
    router.cli(command="request virtual-chassis routing-engine master switch", pattern='yes,no')
    router.cli(command='yes')
    t.log("Start dhcp clients in blackout period")

    base_time = time.time()
    for subscriber in subs:
        subscriber.start()
    retry = 0
    while retry <= kwargs.get('blackout_retry', 1):
        time.sleep(20)
        rt_output = cst.get_rt_subs_info()
        delta_up = rt_output['rt_sessions_up'] - base_up_subs_in_rt
        delta_down = rt_output['rt_sessions_down'] - base_down_subs_in_rt
        delta_time = time.time() - base_time
        if delta_up > 0:
            t.log("{} subscribers login in {} seconds after gres".format(delta_up, delta_time))
            break
        else:
            if (expected_subs_in_rt - delta_up - delta_down) == 0 and delta_time < 1200:
                t.log("restart clients")
                for subscriber in subs:
                    subscriber.restart()
            elif delta_time > 1200:
                t.log('ERROR', 'Failed to login any client in blackout time {}'.format(delta_time))
                break

    t.log("waiting for MXVC to finish GRES switch")

    router.reconnect(all, timeout=600)
    master_node = router.detect_master_node()
    new_master_re = cst.get_master_re_name(device_id)
    if new_master_re == initial_master_re:
        t.log('ERROR', 'GRES failed since master RE did not switch, new master is {}'.format(new_master_re))
    master_re = new_master_re.split(sep='-')[1]
    router.set_current_controller(system_node=master_node, controller=master_re)
    BBEJunosUtil.cpu_settle(cpu_threshold=20, idle_min=int(kwargs.get('cpu_settle', '75')),
                            dead_time=1200, interval=20)
    cst.cst_start_clients(restart_unbound_only=True)

    if health_check:
        cst.get_re_fpc_memory()
        hk.healthcheck_pfe_resource_monitor()
        hk.healthcheck_get_task_memory()
        hk.healthcheck_run_pfe_command(command='show heap 0 accounting pc')
        hk.healthcheck_run_pfe_command(command='show pfe manager session statistics')
    cst.get_vcp_ports(device_id=device_id)
    cst.check_fpc(device_id=device_id)
    cst.get_router_sub_summary(device_id)
    cst.stop_traffic()
    t.log("verify traffic after blackout test")
    cst.prepare_subscriber_traffic(**kwargs)
    if dtcp_test:
        t.log("remove dtcp trigger after test")
        dtcp.dtcp_delete_li_trigger()


def mxvc_fpc_mic_reboot_test(**kwargs):
    """
    The method simulates the event of fpc, mic or pic reboot in a MXVC setup
    :param kwargs:
    device_id:                     device name, e.g.'r0'
    new_mesh:                      create new traffic mesh(True/False)
    subs:                          subs involved in traffic (see add_susbcriber_mesh)
    duration:                      traffic running time, by default is 60 seconds
    traffic_args:                  dictionary for creating traffic which include name, rate, frame_size, etc
                                   (check add_subscriber_mesh in cstutils.py)
    mininum_rx_percentage:         minimum percentage for received traffic
    maximum_rx_percentage:         maximum percentage for received traffic
    method:                        offline/restart/panic, default is offline
    component:                     fpc/pic/mic
    slot_info:                     (optional), fpc slot in dictionary, e.g. {'member':'member0', 'slot': '1'}
    iteration:                     iteration count
    post_action_wait_time:         wait time in seconds, default is 600
    health_check:                  collect health check info, default is False
    :return:
    """
    iteration = kwargs.get('iteration', 1)
    component = kwargs.get('component', 'fpc')
    method = 'offline' if component != 'fpc' else kwargs.get('method', 'offline')
    action_list = ['offline', 'online'] if method == 'offline' else [method]
    post_action_wait_time = int(kwargs.get('post_action_wait_time', 600))
    dtcp_test = kwargs.get('dtcp_test', False)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    if dtcp_test:
        dtcp.dtcp_delete_li_trigger()
        dtcp.dtcp_add_li_trigger()
    health_check = kwargs.get('health_check', False)
    if health_check:
        cst.get_re_fpc_memory()
        hk.healthcheck_pfe_resource_monitor()
        hk.healthcheck_get_task_memory()
        hk.healthcheck_run_pfe_command(command='show heap 0 accounting pc')
        hk.healthcheck_run_pfe_command(command='show pfe manager session statistics')
    cst.prepare_subscriber_traffic(**kwargs)
    cst.start_traffic()
    cst.get_router_sub_summary(device_id)

    pic_info = cst.get_pic_info(device_id)
    chosen_list = []
    while len(chosen_list) < iteration:
        if 'slot_info' in kwargs:
            member = kwargs['slot_info']['member']
            chosen_fpc = kwargs['slot_info']['slot']
        else:
            member = random.choice(list(pic_info.keys()))
            chosen_fpc = random.choice(list(pic_info[member].keys()))
        pic_list = pic_info[member][chosen_fpc]
        chosen_mic = '0'
        if 'MPC' in pic_list.pop(-1):
            mic_list = []
            for item in pic_list:
                if item in ['0', '1']:
                    mic_list.append('0')
                if item in ['2', '3']:
                    mic_list.append('1')
            chosen_mic = random.choice(mic_list)
        chosen_pic = random.choice(pic_list)
        chosen_set = (member, chosen_fpc, chosen_mic, chosen_pic)
        if chosen_set not in chosen_list:
            chosen_list.append(chosen_set)
    t.log("the chosen list for action {} is {}".format(method, chosen_list))
    count = 1

    for item in chosen_list:
        for action in action_list:
            t.log("action {} on chosen {} in iteration #{}".format(action, item, count))
            if action == 'panic':
                router.vty(command='set parser security 10', destination='{}-fpc{}'.format(item[0], item[1]))
                router.vty(command='test panic', destination='{}-fpc{}'.format(item[0], item[1]), pattern='(.*)')
                t.log("waiting for coredump to be generated after panic test")
                #time.sleep(200)
            if component == 'fpc':
                command = "request chassis fpc slot {} member {} {}".format(item[1], item[0].strip('member'), action)
                router.cli(command=command)
            if component == 'mic':
                command = "request chassis mic mic-slot {} " \
                          "fpc-slot {} member {} {}".format(item[2], item[1], item[0].strip('member'), action)
                router.cli(command=command)
            if component == 'pic':
                command = "request chassis pic pic-slot {} fpc-slot {} member" \
                          " {} {}".format(item[3], item[1], item[0].strip('member'), action)
                router.cli(command=command)
            base_time = time.time()
            shutdown = False
            while True:
                t.log("waiting for FPC/PIC state change")
                time.sleep(20)
                resp = router.cli(command="show chassis fpc pic-status {} member {}".format(item[1], item[0].strip('member'))).resp
                if action in ['restart', 'panic']:
                    if re.search(r'Offline', resp) and not shutdown:
                        shutdown = True
                        continue
                    if not re.search(r'Offline', resp):
                        t.log("action {} finished correctly on {} fpc {}").format(action, item[0], item[1])
                        break

                elif action == 'offline':
                    if re.search(r'Offline', resp):
                        t.log("action {} started correctly on {} fpc {}".format(action, item[0], item[1]))
                        break
                elif action == 'online':
                    if not re.search(r'Offline', resp):
                        t.log("action {} started correctly on {} fpc {}".format(action, item[0], item[1]))
                        break
                if time.time() - base_time > post_action_wait_time:
                    raise Exception('{} FPC {} failed to transit to the expected state'.format(item[0], item[1]))
        cst.prepare_subscriber_traffic(**kwargs)
        if dtcp_test:
            dtcp.dtcp_list_li_trigger(**kwargs)

        if health_check:
            cst.get_re_fpc_memory()
            hk.healthcheck_pfe_resource_monitor()
            hk.healthcheck_get_task_memory()
            hk.healthcheck_run_pfe_command(command='show heap 0 accounting pc')
            hk.healthcheck_run_pfe_command(command='show pfe manager session statistics')
        count += 1

    if dtcp_test:
        dtcp.dtcp_delete_li_trigger()



def mxvc_gres_test(**kwargs):
    """
    GRES test for mxvc
    :param kwargs:
    device_id:                     device name, e.g.'r0'
    new_mesh:                      create new traffic mesh(True/False)
    subs:                          subs involved in traffic (see add_susbcriber_mesh)
    duration:                      traffic running time, by default is 60 seconds
    traffic_args:                  dictionary for creating traffic which include name, rate, frame_size, etc
                                   (check add_subscriber_mesh in cstutils.py)
    mininum_rx_percentage:         minimum percentage for received traffic
    maximum_rx_percentage:         maximum percentage for received traffic
    gres_type:                     gres type, global/local/localbackup
    gres_method:                   gres method, (cli/reboot for global, cli/kernel_crash/scb_failover for local,
                                   default is cli)
    global_gres_method:            'cli', 'kernel_crash', 'scb_failover', default is cli
    post_action_wait_time:         wait time in seconds, default is 600
    sleep_between_iteration:       wait time in seconds between iterations, default is 600
    health_check:                  collect health check info, default is False
    iteration:                     iteration count, default is 1
    :return:
    """
    post_action_wait_time = int(kwargs.get('post_action_wait_time', 600))
    sleep_between_iteration = int(kwargs.get('sleep_between_iteration', 600))
    dtcp_test = kwargs.get('dtcp_test', False)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    iteration = kwargs.get('iteration', 1)
    gres_type = kwargs.get('gres_type', 'global')
    gres_method = kwargs.get('gres_method', 'cli')
    timeout = kwargs.get('gres_check_timeout', 1800)
    initial_master_re = cst.get_master_re_name(device_id)
    router.cli(command='show virtual-chassis status')
    cst.prepare_subscriber_traffic(**kwargs)
    cst.start_traffic()
    cst.get_router_sub_summary(device_id)
    if dtcp_test:
        dtcp.dtcp_delete_li_trigger()
        dtcp.dtcp_add_li_trigger()
    cst.check_fpc(device_id=device_id)
    cst.get_vcp_ports(device_id=device_id)
    count = 1
    while count <= iteration:
        t.log("checking GRES ready state before test in iteration {}".format(count))
        cst.check_gres_ready(device_id, check_timeout=timeout)
        command_list = ['show database-replication summary',
                        'show system relay group']
        ### log something before GRES
        for command in command_list:
            router.cli(command=command)
        health_check = kwargs.get('health_check', False)
        if health_check:
            cst.get_re_fpc_memory()
            hk.healthcheck_pfe_resource_monitor()
            hk.healthcheck_get_task_memory()
            hk.healthcheck_run_pfe_command(command='show pfe manager session statistics')

        command_list = ['show chassis fpc', 'show virtual-chassis vc-port', 'show virtual-chassis status',
                        'show route summary', 'show route forwarding-table summary']

        ### log something before GRES
        for command in command_list:
            router.cli(command=command)

        t.log("starting MXVC GRES test with type {} method {}".format(gres_type, gres_method))
        if gres_type == 'global':
            if gres_method == 'cli':
                t.log("Executing a Global GRES on the master by CLI.")
                router.cli(command="request virtual-chassis routing-engine master switch", pattern='yes,no')
                router.cli(command='yes')

            elif gres_method == 'kernel_crash':
                #trigger GRES by kernel crash, old master will enter into db> and then recovered
                host = router.current_node.current_controller.name
                cst.panic_re_recover(host=host)
            elif gres_method == 'scb_failover':
                t.log("pull out scb card")
                input("PRESS ENTER TO CONTINUE.")
                time.sleep(600)
                t.log("push in scb card")
                input("PRESS ENTER TO CONTINUE.")

        if 'local' in gres_type:
            if 'localbackup' in gres_type:
                t.log("switch controller to the Vc-Bm before test")
                master_node = initial_master_re.split(sep='-')[0]
                backup_node = 'member1' if 'primary' in initial_master_re else 'primary'
                for rename in ['re0', 're1']:
                    router.set_current_controller(system_node=backup_node, controller=rename)
                    if router.current_node.current_controller.is_msater():
                        break

            if gres_method == 'reboot':
                t.log("perform GRES type {} using {}".format(gres_type, gres_method))
                router.cli(command="request system reboot local", pattern='yes,no')
                router.cli(command='yes')
            if gres_method == 'cli':
                t.log("perform GRES type {} using {}".format(gres_type, gres_method))
                resp = router.cli(command="request chassis routing-engine master switch", pattern='yes,no').resp
                if 'error' in resp or 'not honored' in resp:
                    raise Exception("failed to execute local switch")
                router.cli(command='yes')

        time.sleep(post_action_wait_time)
        router.reconnect(all, timeout=600)
        master_node = router.detect_master_node()
        new_master_re = cst.get_master_re_name(device_id)
        t.log("current master re after GRES test is {}")
        if new_master_re == initial_master_re:
            if 'localbackup' not in gres_type:
                t.log('ERROR', 'GRES failed since master RE did not switch, new master is {}'.format(new_master_re))
            else:
                t.log("localbackup switched successfully")
        else:
            t.log("GRES switched successfully, new master is {}".format(new_master_re))

        master_re = new_master_re.split(sep='-')[1]
        router.set_current_controller(system_node=master_node, controller=master_re)
        BBEJunosUtil.cpu_settle(cpu_threshold=20, idle_min=int(kwargs.get('cpu_settle', '75')),
                                dead_time=1200, interval=20)
        cst.check_fpc(device_id=device_id)
        cst.get_vcp_ports(device_id=device_id)
        cst.get_router_sub_summary(device_id)
        cst.check_link_status(router=device_id)
        cst.stop_traffic()
        cst.verify_traffic(**kwargs)
        if dtcp_test:
            dtcp.dtcp_list_li_trigger(**kwargs)
        count += 1

        time.sleep(sleep_between_iteration)
    if health_check:
        cst.get_re_fpc_memory()
        hk.healthcheck_pfe_resource_monitor()
        hk.healthcheck_get_task_memory()
        hk.healthcheck_run_pfe_command(command='show pfe manager session statistics')
    if dtcp_test:
        dtcp.dtcp_delete_li_trigger()
