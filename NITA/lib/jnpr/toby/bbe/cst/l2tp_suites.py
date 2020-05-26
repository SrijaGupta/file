"""
CST L2TP Test Suites
"""
import time
from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil
import random
import jnpr.toby.bbe.cst.cstutils as cst
import jnpr.toby.bbe.cst.dtcp_suites as dtcp
import jnpr.toby.bbe.cst.cstsuites as suites


def l2tp_disconnect_test(**kwargs):
    """
    Disconnect all L2TP sessions/tunnel on given box either by:
    clear services l2tp tunnel all
    clear services l2tp session all
    in yaml file, the lac/lns needs to be tagged with lac/lns, l2tp clients needs with tag l2tpx
    :param kwargs:
    device_id:                     device name, e.g.'r0'
    new_mesh:                      create new traffic mesh(True/False)
    subs:                          subs involved in traffic (see add_susbcriber_mesh)
    duration:                      traffic running time, by default is 60 seconds
    traffic_args:                  dictionary for creating traffic which include name, rate, frame_size, etc
                                   (check add_subscriber_mesh in cstutils.py)
    mininum_rx_percentage:         minimum percentage for received traffic
    maximum_rx_percentage:         maximum percentage for received traffic
    clear_by:                      session/tunnel, default is session
    clear_on:                      lac/lns, default is lns
    post_action_wait_time:         wait time in seconds, default is 600
    sleep_between_iteration:       wait time in seconds between iterations, default is 600
    dtcp_test:                     True/False
    check_interval:                interval to check if the subs on lac/lns are synced, default is 120s
    check_tunnel_close:            True/False, default is False
    iteration:                     iteration count, default is 1
    :return:
    """
    interval = int(kwargs.get('check_interval', 120))
    check_tunnel_close = kwargs.get('check_tunnel_close', False)
    clear_by = kwargs.get('clear_by', 'session')
    clear_on = kwargs.get('clear_on', 'lns')
    iteration = int(kwargs.get('iteration', 1))
    dut_list = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True))
    dtcp_test = kwargs.get('dtcp_test', False)

    lac_device = bbe.get_devices(device_tags='lac', id_only=True)
    lns_device = bbe.get_devices(device_tags='lns', id_only=True)
    device_list = lac_device + lns_device
    count = 1
    while count <= iteration:

        cst.prepare_subscriber_traffic(**kwargs)
        cst.start_traffic()
        for device in device_list:
            dev1 = t.get_handle(device)
            dev1.cli(command="show service l2tp summary")
            cst.get_aaa_accounting_stats(device)
        t.log("clearing {} on {} in iteration {}".format(clear_by, clear_on, count))
        clear_on_device = bbe.get_devices(device_tags=clear_on, id_only=True)
        for device in clear_on_device:
            dev2 = t.get_handle(device)
            dev2.cli(command="clear services l2tp {} all | no-more".format(clear_by))
        time.sleep(90)

        for device in device_list:
            dev1 = t.get_handle(device)
            BBEJunosUtil.set_bbe_junos_util_device_handle(dev1)
            BBEJunosUtil.cpu_settle(cpu_threshold=10, idle_min=int(kwargs.get('cpu_settle', '85')),
                                    dead_time=1200, interval=20)
        t.log("waiting for subscriber stable after teardown l2tp subs")
        total_subs = bbe.get_subscriber_handles()
        l2tp_subs = bbe.get_subscriber_handles(tag='l2tp')
        for item in l2tp_subs:
            total_subs.remove(item)
        other_subs = total_subs
        result1 = cst.get_configured_subs(subs=other_subs)
        basetime = time.time()
        while True:
            try:
                cst.verify_client_count(subs=other_subs)
            except:
                t.log("waiting {}s to check the client counts".format(interval))
                time.sleep(interval)
                if time.time() - basetime > 1800:
                    raise Exception("clients failed to reach the specified count after 1800s")
            else:
                break
        result = cst.get_rt_subs_info()
        if result['rt_sessions_up'] != result1['expected_total_session_in_testers']:
            raise Exception("subscribers count {} in tester is not the same as expected"
                            " {}".format(result['rt_sessions_up'], result1['expected_total_session_in_testers']))
        status = True
        for device in dut_list:
            dev1 = t.get_handle(device)
            resp = dev1.pyez('get_l2tp_summary_information').resp
            tunnel_count = int(resp.findtext('l2tp-summary-table/l2tp-tunnels'))
            session_count = int(resp.findtext('l2tp-summary-table/l2tp-sessions'))
            if clear_by == 'tunnel' and tunnel_count > 0:
                status = False
                t.log('WARN', 'failed to clear tunnel in iteration {} clear by {}'.format(count, clear_by))
            if clear_by == 'session' and check_tunnel_close and tunnel_count > 0:
                status = False
                t.log('WARN', 'failed to clear tunnel in iteration {} clear by {}'.format(count, clear_by))

            if session_count > 0:
                status = False
                t.log('WARN', 'failed to clear session in iteration {} clear by {}'.format(count, clear_by))
            cst.get_aaa_accounting_stats(device)
        if not status:
            raise Exception("failed to clear session or tunnel in iteration {}".format(count))
        cst.stop_traffic()
        if dtcp_test:
            dtcp.dtcp_delete_li_trigger()
            dtcp.dtcp_add_li_trigger()
        cst.cst_start_clients(subs=l2tp_subs, restart_unbound_only=True)
        suites.unicast_traffic_test(**kwargs)
        t.log("l2tp disconnect test finished in iteration #{}".format(count))
        count += 1


def lns_cluster_failover_test(**kwargs):
    """
    Bring down one LNS in LNS cluster and verify that affected subscribers can be bound on working LNS
    :param kwargs:
    device_id:                     device name, e.g.'r0'
    new_mesh:                      create new traffic mesh(True/False)
    subs:                          subs involved in traffic (see add_susbcriber_mesh)
    duration:                      traffic running time, by default is 60 seconds
    traffic_args:                  dictionary for creating traffic which include name, rate, frame_size, etc
                                   (check add_subscriber_mesh in cstutils.py)
    mininum_rx_percentage:         minimum percentage for received traffic
    maximum_rx_percentage:         maximum percentage for received traffic

    post_action_wait_time:         wait time in seconds, default is 600
    sleep_between_iteration:       wait time in seconds between iterations, default is 600
    dtcp_test:                     True/False
    iteration:                     iteration count, default is 1
    :return:
    """
    dut_list = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True))
    dtcp_test = kwargs.get('dtcp_test', False)
    lac_device = bbe.get_devices(device_tags='lac', id_only=True)
    lns_device = bbe.get_devices(device_tags='lns', id_only=True)
    device_list = lac_device + lns_device
    for iteration in range(1, int(kwargs.get('iteration', 1)) + 1):
        cst.prepare_subscriber_traffic(**kwargs)
        cst.start_traffic()

        for device in device_list:
            dev1 = t.get_handle(device)
            dev1.cli(command="show service l2tp summary")
            cst.get_aaa_accounting_stats(device)
        lns_id = random.choice(lns_device)
        router = t.get_handle(lns_id)
        t.log("bring down interfaces on {} and reboot".format(lns_id))
        command_list = []
        for intf in bbe.get_interfaces(device=lns_id):
            command_list.append('set interfaces {} disable'.format(intf.pic))
        command_list.append('commit')
        router.config(command_list=command_list)
        router.reboot(all=True)
        t.log("waiting for cpu settle in LNS")
        base_time = time.time()
        for device in device_list:
            dev1 = t.get_handle(device)
            BBEJunosUtil.set_bbe_junos_util_device_handle(dev1)
            BBEJunosUtil.cpu_settle(cpu_threshold=10, idle_min=int(kwargs.get('cpu_settle', '85')),
                                    dead_time=1200, interval=20)
        initial_client = 0
        for dutid in dut_list:
            summary = cst.get_router_sub_summary(dutid)
            initial_client += summary['client']

        while True:
            current_client = 0
            for dutid in dut_list:
                summary = cst.get_router_sub_summary(dutid)
                current_client += summary['client']
            if current_client != initial_client:
                initial_client = current_client
            else:
                t.log("client count {} is in stable state".format(current_client))
                break
            if time.time() - base_time > 1200:
                cst.stop_traffic()
                raise Exception("client count is not stable after 1200s")
            t.log("waiting for 60s to check the subscriber count again")
            time.sleep(60)

        cst.stop_traffic()
        t.log("relogin unbounded clients and verify traffic")
        cst.cst_start_clients(restart_unbound_only=True)
        if dtcp_test:
            dtcp.dtcp_delete_li_trigger()
            dtcp.dtcp_add_li_trigger()
        suites.unicast_traffic_test(**kwargs)
        if dtcp_test:
            dtcp.dtcp_list_li_trigger(**kwargs)

    if dtcp_test:
        dtcp.dtcp_delete_li_trigger()


def lns_load_balance_test(**kwargs):
    """
    Developed for LNS cluster
    Bring down sessions always from one LNS, rebind them and verify each LNS has close amount of subscribers
    LAC should establish sessions in existing tunnels
    :param kwargs:
    :return:
    """
    lac_device = bbe.get_devices(device_tags='lac', id_only=True)
    tunnel_dict = {}
    for lac_id in lac_device:
        router = t.get_handle(lac_id)
        tunnel_dict['lac_id'] = {}
        resp = router.pyez('get_l2tp_summary_information').resp
        tunnel_dict['lac_id']['l2tp_destination'] = resp.findtext('l2tp-summary-table/l2tp-destinations')
        tunnel_dict['lac_id']['l2tp_tunnels'] = resp.findtext('l2tp-summary-table/l2tp-tunnels')
        tunnel_dict['lac_id']['l2tp_sessions'] = resp.findtext('l2tp-summary-table/l2tp-sessions')
        tunnel_dict['lac_id']['l2tp_switched_sessions'] = resp.findtext('l2tp-summary-table/l2tp-switched-sessions')
    t.log("the tunnel information before test is {}".format(tunnel_dict))
    lns_device = bbe.get_devices(device_tags='lns', id_only=True)
    for iteration in range(1, int(kwargs.get('iteration', 1)) + 1):
        chosen_sub = random.choice(bbe.get_subscriber_handles(tag='l2tp'))
        cst.cst_release_clients(subs=chosen_sub)
        cst.cst_start_clients(subs=chosen_sub)
        t.log("checking l2tp infor in LNS in iteration {}".format(iteration))
        for lns_id in lns_device:
            router = t.get_handle(lns_id)
            tunnel_dict['lns_id'] = {}
            resp = router.pyez('get_l2tp_summary_information').resp
            tunnel_dict['lns_id']['l2tp_destination'] = resp.findtext('l2tp-summary-table/l2tp-destinations')
            tunnel_dict['lns_id']['l2tp_tunnels'] = resp.findtext('l2tp-summary-table/l2tp-tunnels')
            tunnel_dict['lns_id']['l2tp_sessions'] = resp.findtext('l2tp-summary-table/l2tp-sessions')
            tunnel_dict['lns_id']['l2tp_switched_sessions'] = resp.findtext('l2tp-summary-table/l2tp-switched-sessions')
        t.log("the tunnel information after iteration {} is {}".format(iteration, tunnel_dict))
