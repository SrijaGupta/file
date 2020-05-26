'''
CST methods to get stats and health reports
'''
import jnpr.toby.bbe.cst.cstutils as cst
import re

def healthcheck_pfe_resource_monitor(timeout=600):
    """
    check the output of show system resource-monitor summary
        {'r0': {'fpc0': {'fpc-client-session-denied-count': '0',
                 'fpc-service-session-denied-count': '0',
                 'used-heap-mem': '279233552',
                 'used-heap-mem-percent': '16'},
        'fpc0_pfe_0': {'used-filter-counter': '17950080',
                       'used-filter-counter-percent': '37',
                       'used-ifl-counter': '730816',
                       'used-ifl-counter-percent': '2'},
        'fpc0_pfe_1': {'used-filter-counter': '17738224',
                       'used-filter-counter-percent': '44',
                       'used-ifl-counter': '267424',
                       'used-ifl-counter-percent': '0'},
        }}}

    :return:  dictionary of fpc/pfe info
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    resource_stats = dict()
    for router_id in router_ids:
        router = t.get_handle(router_id)
        resource_stats[router_id] = {}
        resp = router.pyez('get_resource_monitor_summary_fpc_information', timeout=timeout).resp
        fpc_infos = resp.findall('resource-monitor-summary-fpc-information-summary')

        for fpc_info in fpc_infos:
            name = 'fpc' + fpc_info.findtext('fpc-slot')
            resource_stats[router_id][name] = {}
            resource_stats[router_id][name]['fpc-client-session-denied-count'] =\
                fpc_info.findtext('fpc-client-session-denied-count')
            resource_stats[router_id][name]['fpc-service-session-denied-count'] =\
                fpc_info.findtext('fpc-service-session-denied-count')
            resource_stats[router_id][name]['used-heap-mem'] = fpc_info.findtext('used-heap-mem')
            resource_stats[router_id][name]['used-heap-mem-percent'] = fpc_info.findtext('used-heap-mem-percent')

            pfe_infos = fpc_info.findall('resource-monitor-summary-pfe-information-summary')
            for pfe_info in pfe_infos:
                if not pfe_info.findtext('pfe-num'):
                    continue
                pfename = name + '_pfe_' + pfe_info.findtext('pfe-num')
                resource_stats[router_id][pfename] = {}
                resource_stats[router_id][pfename]['used-filter-counter'] =\
                    pfe_info.findtext('used-filter-counter')
                resource_stats[router_id][pfename]['used-filter-counter-percent'] =\
                    pfe_info.findtext('used-filter-counter-percent')
                resource_stats[router_id][pfename]['used-ifl-counter'] = pfe_info.findtext('used-ifl-counter')
                resource_stats[router_id][pfename]['used-ifl-counter-percent'] =\
                    pfe_info.findtext('used-ifl-counter-percent')
    return resource_stats


def healthcheck_get_kernel_mem(timeout=300):
    """
    collect kernal memory usage
    :return: dictionary of stats
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    stats = {}
    for router_id in router_ids:
        router = t.get_handle(router_id)
        stats[router_id] = {}
        resp = router.shell(command='sysctl -a | grep mem', timeout=timeout).resp
        result = resp.split('\r\n')

        for name in ['vm.kmem_size', 'vm.kmem_map_free', 'vm.kmem_mt_used_max_percent']:
            for item in result:
                if name in item:
                    stats[router_id][name] = item.split(sep=':')[1]
                    break
    t.log("kernel memory info {}".format(stats))
    return stats


def healthcheck_get_task_memory(timeout=600):
    """
    collect task memory usage
    :return: dictionary of stats
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    taskstats = {}
    for router_id in router_ids:
        router = t.get_handle(router_id)
        taskstats[router_id] = {}
        resp = router.pyez('get_task_memory_information', detail=True, timeout=timeout).resp
        taskstats['name'] = 'virtual_memory'
        taskstats[router_id]['Dynamically allocated memory'] = resp.findtext('task-memory-dynamic-allocs')
        taskstats[router_id]['Program data+BSS memory'] = resp.findtext('task-memory-bss-bytes')
        taskstats[router_id]['Page data overhead'] = resp.findtext('task-memory-page-data-bytes')
        taskstats[router_id]['Page directory size'] = resp.findtext('task-memory-dir-bytes')
        taskstats[router_id]['Total bytes in use'] = resp.findtext('task-memory-total-bytes-in-use')
    t.log("task memory is {}".format(taskstats))
    return taskstats


def healthcheck_run_pfe_command(command, timeout=300):
    """
    using cprod to run vty command
    :param command:             vty command
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    for router_id in router_ids:
        router = t.get_handle(router_id)
        slot_list = []
        for name in t.resources[router_id]['interfaces']:
            if 'access' in name or 'transit' in name:
                match = re.match(r'\w+-(\d+)/\d+/\d+', t.resources[router_id]['interfaces'][name]['pic'])
                slot = int(match.group(1))
                if slot not in slot_list:
                    slot_list.append(slot)
        master_node = 'member0'
        for slot in slot_list:
            if router.vc:
                if router.get_model() == 'mx2020':
                    if slot >= 20:
                        slot = slot - 20
                        master_node = 'member1'
                else:
                    if slot >= 12:
                        slot = slot - 12
                        master_node = 'member1'
                router.shell(command='cprod -A {}-fpc{} -c "{}"'.format(master_node, slot, command), timeout=timeout)

            else:
                router.shell(command='cprod -A fpc{} -c "{}"'.format(slot, command), timeout=timeout)


def healthcheck_get_re_memory(timeout=600):
    """
    display chassis routing-engine memory size
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    re_mem_dict = {}
    for device_id in router_ids:
        summary = cst.get_router_sub_summary(device_id)
        re_mem_dict[device_id] = {}
        re_mem_dict[device_id]['active-count'] = summary['client']
        router = t.get_handle(device_id)
        resp = router.pyez('get_route_engine_information', normalize=True, timeout=timeout).resp
        if router.vc:
            for member in resp.findall('multi-routing-engine-item'):
                chassis_name = member.findtext('re-name')
                for item in member.findall('route-engine-information/route-engine'):
                    slot = chassis_name + '_re' + item.findtext('slot')
                    re_mem_dict[device_id][slot] = dict()
                    reutil = item.findtext('memory-buffer-utilization')
                    re_mem_dict[device_id][slot]['memory-utilization'] = reutil + '%'

        else:
            for engine in resp.findall('route-engine'):
                slot = engine.findtext('slot')
                name = 're' + slot
                re_mem_dict[device_id][name] = dict()
                reutil = engine.findtext('memory-buffer-utilization')
                re_mem_dict[device_id][name]['memory-utilization'] = reutil + '%'
    if hasattr(t, 're_mem_stats'):
        t.re_mem_stats.append(re_mem_dict)
    else:
        t.re_mem_stats = []
        t.re_mem_stats.append(re_mem_dict)
    print(re_mem_dict)

def healthcheck_get_shell_stats(timeout=300):
    """
    display shell stats
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    shellstats = {}
    shellstats2 = {}
    for router_id in router_ids:
        shellstats[router_id] = {}
        shellstats2[router_id] = {}
        router = t.get_handle(router_id)
        for item in ['netstat -p rawif', 'netstat -p ttp', 'top -b -o size']:
            resp = router.shell(command=item, timeout=timeout).resp
            print(resp)

        router.su()
        cmd1 = "ps -aux | egrep -e root -e super | awk 'BEGIN{}{cnt++}{sbytes += $4}{ rbytes += $5} END" \
               " {printf \"=%d =%.2f =%.2f\\n\", cnt, sbytes/1000, rbytes/1000}'"
        resp = router.shell(command=cmd1, timeout=timeout).resp
        resp1 = re.sub(r'=', '', resp.split(sep='\r\r\n')[1]).split()

        shellstats[router_id]['procCount'] = resp1[0]
        shellstats[router_id]['sizeM'] = resp1[1]
        shellstats[router_id]['resSizeM'] = resp1[2]

        shellstats2[router_id] = {}

        cmd1 = "ls -ltRi /mfs | sort -n +5 | tail -15 | awk '{cnt++}{bytes+=$6} END" \
               " {printf \"=%d =%d\\n\", cnt, bytes/1000000}'"
        resp = router.shell(command=cmd1, timeout=timeout).resp
        resp1 = re.sub(r'=', '', resp).split()
        shellstats2[router_id]['mfsFileCnt'] = resp1[0]
        shellstats2[router_id]['M'] = resp1[1]
    t.procCountWithMemSize = shellstats
    t.mfsFileCntSize = shellstats2
    print(shellstats)
    print(shellstats2)

def healthcheck_isvty_dfw_statesync(timeout=300):
    """
    Dump bbe_dfw_state in master and backup RE and verify whether the files are sync
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    #dest_ips = ["128.0.0.1", "128.0.0.5"]
    for router_id in router_ids:
        router = t.get_handle(router_id)
        # if router.vc:
        #     dest_ips = ["161.0.0.1", "161.0.0.6"]
        # for dstip in dest_ips:
        #     command = 'smd-plugin dfw test dump all-state'
        #     destination = '-s 7208 ' + dstip
        #     router.vty(command=command, destination=destination)
        router.execute_command(mode='bbevty_pri', command='smd-plugin dfw test dump all-state', timeout=timeout)
        if len(router.current_node.controllers.keys()) == 2:
            router.execute_command(mode='bbevty_sla', command='smd-plugin dfw test dump all-state', timeout=timeout)
        resp = []
        master_re = cst.get_master_re_name(router_id)
        if router.vc:
            vc_re_name = router.current_node.current_controller.re_name
            if 'member0' in vc_re_name:
                master_node = 'primary'
            elif 'member1' in vc_re_name:
                master_node = 'member1'
            for node in ['primary', 'member1']:
                for controller in ['re0', 're1']:
                    router.set_current_controller(controller, node)
                    if router.current_node.current_controller.is_master():
                        break
                resp1 = router.cli(command='file show /var/log/bbe_dfw_state.txt', timeout=timeout).resp
                resp.append(resp1.split(sep='FILTER INFO')[1])
            master_re = master_re.split(sep='-')[1]
            router.set_current_controller(master_re, master_node)
        else:

            for re_name in t.get_resource(router_id)['system']['primary']['controllers']:
                router.set_current_controller(controller=re_name, system_node='primary')

                resp1 = router.cli(command='file show /var/log/bbe_dfw_state.txt').resp
                resp.append(resp1.split(sep='FILTER INFO')[1])
            router.set_current_controller(controller=master_re, system_node='primary')
        if resp[0] == resp[1]:
            t.log("Master and standby RE bbe_dwf_state are in sync.")
        else:
            raise Exception("Master and standby RE bbe_dwf_state are NOT in sync.")

def healthcheck_get_pfe_vty_jnhstats(timeout=300):
    """
    for all fpc slots that have subscribers, collect jnh, interface, bvf, ttp, xqchip, thread cpu stats on master and
    backup RE and output into log
    :param kwargs:
    timeout:         vty timeout value, default toby vty timeout is 300
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    status = True
    for router_id in router_ids:
        result = cst.get_router_sub_summary_by_slot(router_id)
        router = t.get_handle(router_id)
        master_re = cst.get_master_re_name(router_id)
        router.set_current_controller(master_re, 'primary')
        if result:
            for slot in result:
                fpcname = 'fpc' + slot
                command_list = ["show jnh issu stats", "show jnh host errors", "show interface statistics",
                                "show ttp statistics", "show jnh host-path-stats", "show vbf ttp",
                                "show vbf flow summary", "show vbf ipc", "show xqchip 0 info", "show threads cpu"]
                for command in command_list:
                    resp = router.vty(destination=fpcname, command=command, timeout=timeout).resp
                    if command == 'show vbf ipc' and 'FLOW FAILED' in resp:
                        t.log('WARN', "FLOW FAILED on {}".format(fpcname))
                        status = False
                        router.vty(destination=fpcname, command='show syslog messages', timeout=timeout)

                command_list = ["show jnh 0 exceptions terse", "show jnh 1 exceptions terse"]
                for command in command_list:
                    resp = router.vty(destination=fpcname, command=command, timeout=timeout).resp
                    errors = ["undefined nexthop opcode", "sw error", "egress pfe unspecified",
                              "invalid fabric token", "dv no ctrl ifl"]
                    for error in errors:
                        if error in resp:
                            status = False
                            t.log('WARN', '{}: Found on {}: {}'.format(error, fpcname, command))
    if not status:
        raise Exception("jnh stats health check failed")
    return status

def healthcheck_hasbbe_sdb_throttle_replication_on_off():
    """
    Check BBE_SDB_THROTTLE_REPLICATION_ON BBE_SDB_THROTTLE_REPLICATION_OFF from shmlog
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    status = True
    for router_id in router_ids:
        router = t.get_handle(router_id)
        resp = router.cli(command='show shmlog entries logname bbe*|match BBE_SDB_THROTTLE', timeout=300).resp
        if 'BBE_SDB_THROTTLE_REPLICATION_ON' in resp or 'BBE_SDB_THROTTLE_REPLICATION_OFF' in resp:
            t.log('WARN', "Found BBE_SDB_THROTTLE_REPLICATION_ON/OFF in {}".format(router_id))
            status = False
    if not status:
        raise Exception("Found BBE_SDB_THROTTLE_REPLICATION_ON/OFF")
    return status


def healthcheck_isbbe_ss_state_change():
    """
    Verify whether BBE_SS_STATE_CHANGE in shmlog bbe* is more than 2.
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    status = True
    for router_id in router_ids:
        router = t.get_handle(router_id)
        resp = router.cli(command="show shmlog statistics logname bbe*|match BBE_SS_STATE_CHANGE", timeout=300).resp
        if 'BBE_SS_STATE_CHANGE' in resp:
            lines = resp.split()
            if int(lines[5]) <= 2:
                t.log("Pass, BBE_SS_STATE_CHANGE count not exceed 2.")
            else:
                t.log('WARN', "BBE_SS_STATE_CHANGE count should not exceed 2. in {}".format(router_id))
                status = False
    if not status:
        raise Exception('BBE_SS_STATE_CHANGE count should not exceed 2')
    return status


def healthcheck_shmlog_statserr(timeout=300):
    """
    Check _ERR _NOT_FOUND FAIL NACK keywords from shmlog
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)

    for router_id in router_ids:
        router = t.get_handle(router_id)
        command_list = ["_ERR", "_NOT_FOUND", "FAIL"]
        for command in command_list:
            router.cli(command="show shmlog statistics logname bbe*|match {}".format(command), timeout=timeout)
        router.cli(command="show shmlog statistics logname all | match NACK", timeout=timeout)


def healthcheck_get_bbe_vtystats(timeout=300):
    """
    collect smd ifls route services stats from vty master RE and backup RE
    :param
    timeout:         vty timeout value, default toby vty timeout is 60
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)

    #dest_ips = ["128.0.0.1", "128.0.0.5"]
    for router_id in router_ids:
        router = t.get_handle(router_id)
        # if router.vc:
        #     dest_ips = ["161.0.0.1", "161.0.0.6"]
        # for dstip in dest_ips:
        command_list = ["show smd statesync", "show smd sdb", "show ifls summary", "show route summary",
                        "show services summary", "show ifls deleted", "show route deleted",
                        "show route deleted summary"]
#           destination = '-s 7208 ' + dstip
        for command in command_list:
            router.execute_command(mode='bbevty_pri', command=command, timeout=timeout)
            if len(router.current_node.controllers.keys()) == 2:
                router.execute_command(mode='bbevty_sla', command=command, timeout=timeout)


def healthcheck_vtycos_statesync(timeout=300):
    """
    Dump bbe_cos_iflset bbe_cos_ifl_var bbe_cos_iflset_conf in master and backup RE and verify if the files are sync

    timeout:         vty timeout value, default toby vty timeout is 60
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    status = True
    #dest_ips = ["128.0.0.1", "128.0.0.5"]
    for router_id in router_ids:
        router = t.get_handle(router_id)
        # if router.vc:
        #     dest_ips = ["161.0.0.1", "161.0.0.6"]
        # for dstip in dest_ips:
        command = "smd-plugin cos dump all"
        router.execute_command(mode='bbevty_pri', command=command, timeout=timeout)
        if len(router.current_node.controllers.keys()) == 2:
            router.execute_command(mode='bbevty_sla', command=command, timeout=timeout)
        #     destination = '-s 7208 ' + dstip
        #     router.vty(command=command, destination=destination)
        file_list = ["bbe_cos_iflset_var_dump", "bbe_cos_iflset_conf_dump", "bbe_cos_ifl_var_dump"]

        master_re = cst.get_master_re_name(router_id)
        for file in file_list:
            resp = []
            if router.vc:
                vc_re_name = router.current_node.current_controller.re_name
                if 'member0' in vc_re_name:
                    master_node = 'primary'
                elif 'member1' in vc_re_name:
                    master_node = 'member1'
                for node in ['primary', 'member1']:
                    for controller in ['re0', 're1']:
                        router.set_current_controller(controller, node)
                        if router.current_node.current_controller.is_master():
                            break

                    resp1 = router.cli(command='file show /var/tmp/{}'.format(file)).resp
                    resp.append(resp1)
                master_re = master_re.split(sep='-')[1]
                router.set_current_controller(master_re, master_node)
            else:

                for re_name in t.get_resource(router_id)['system']['primary']['controllers']:
                    router.set_current_controller(controller=re_name, system_node='primary')

                    resp1 = router.cli(command='file show /var/tmp/{}'.format(file)).resp
                    resp.append(resp1)
                router.set_current_controller(controller=master_re, system_node='primary')
            if resp[0] == resp[1]:
                t.log("Master and standby RE {} are sync".format(file))
            else:
                t.log('WARN', "Master and standby RE {} are not in sync.".format(file))
                status = False
        if not status:
            raise Exception("Master and Standby RE files are not in sync")
        return status


def healthcheck_get_storage_dev_md12(timeout=300):
    """
    Looks system storage md12 size
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)

    storage_stats = {}
    for router_id in router_ids:
        router = t.get_handle(router_id)
        resp = router.cli(command="show system storage|match md12", timeout=timeout).resp
        active_count = cst.get_router_sub_summary(router_id)['client']
        storage_stats[router_id] = {}
        storage_stats[router_id]['active_count'] = active_count
        if router.vc:
            storage_stats[router_id]['member0_storage_dev_md12'] = resp.split()[2]
            storage_stats[router_id]['member1_storage_dev_md12'] = resp.split()[8]
        else:
            storage_stats[router_id]['storage_dev_md12'] = resp.split()[2]
    if hasattr(t, 'StorageDevMd12'):
        t.StorageDevMd12.append(storage_stats)
    else:
        t.StorageDevMd12 = []
        t.StorageDevMd12.append(storage_stats)


def healthcheck_verify_memorymapped_filesystemalloc(**kwargs):
    """
    Verify whether storage_dev_md12 is increased after action
    getStorageDevMd12 will be executed before execute this sub
    default tolerance is 1% if not set
    :kwargs:
    tolerance:          percentage, default is 1
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    tolerance = float(kwargs.get('tolerance', 1))
    status = True

    for router_id in router_ids:
        router = t.get_handle(router_id)
        names = ['storage_dev_md12']
        if router.vc:
            names = ['member0_storage_dev_md12', 'member1_storage_dev_md12']
        for name in names:
            if abs(float(t.StorageDevMd12[-1][router_id][name]) - float(t.StorageDevMd12[-2][router_id][name])) * 100\
                    <= float(t.StorageDevMd12[-1][router_id][name]) * tolerance:
                t.log("After the action, {} size not changed".format(name))
            else:
                t.log('WARN', "{} size had changed after the action".format(name))
                status = False
    if not status:
        raise Exception("storage_dev_md12 size changed after the action")
    return status


def healthcheck_verify_rememory(**kwargs):
    """
    Verify whether RE memory is increased after action.
    healthcheck_getREMemory will be executed before execute this sub
        default tolerance is 1% if not set
    :kwargs:
    tolerance:          percentage, default is 1
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    tolerance = float(kwargs.get('tolerance', 1))
    status = True
    for router_id in router_ids:
        for item in t.re_mem_stats[-1][router_id]:
            if 're' not in item:
                continue
            if abs(float(t.re_mem_stats[-1][router_id][item]['memory-utilization']) - float(
                    t.re_mem_stats[-2][router_id][item]['memory-utilization'])) * 100 \
                    > tolerance * float(t.re_mem_stats[-1][router_id][item]['memory-utilization']):
                status = False
                if t.re_mem_stats[-1][router_id]['active-count'] \
                        == t.re_mem_stats[-2][router_id]['active-count']:
                    t.log("WARN", "{} {} memory had been increased as expected "
                                     "after the action while active count did not change".format(router_id, item))
                else:
                    t.log("WARN", "{} {} memory had been increased as expected "
                                     "after the action while active count also changed".format(router_id, item))
    if not status:
        raise Exception("RE memory health check failed")
    return status


def healthcheck_test_preambleactions(timeout=300):
    """
    Log clear actions before the testcase.
    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    for router_id in router_ids:
        router = t.get_handle(router_id)
        command_list = ["clear ddos-protection protocols dhcpv4 statistics",
                        "clear dhcp statistics", "clear dhcpv6 statistics",
                        "clear ddos-protection protocols dhcpv6 statistics",
                        "clear system subscriber-management statistics"]
        for command in command_list:
            router.cli(command=command, timeout=timeout)


def healthcheck_dhcppacketstats(timeout=300):
    """

    :return:
    """
    router_ids = bbe.get_devices(device_tags='dut', id_only=True)
    for router_id in router_ids:
        router = t.get_handle(router_id)
        command_list = ["show ddos-protection protocols statistics terse",
                        "show ddos-protection protocols dhcpv4 statistics terse",
                        "show ddos-protection protocols dhcpv6 statistics terse",
                        "show system subscriber-management statistics dhcp extensive",
                        "show dhcp relay statistics", "show dhcpv6 relay statistics",
                        "show dhcp statistics", "show dhcpv6 statistics"]
        for command in command_list:
            router.cli(command=command, timeout=timeout)
