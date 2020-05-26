'''
CST Actions
'''
import time
from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil
import re
import random
import jnpr.toby.bbe.cst.cstutils as cst
import jnpr.toby.engines.verification.verify_utils as verify_utils

def re_actions(**kwargs):
    """
    re_actions(type='backup', action='kernel_crash')
    used to power cycle RE, default for backup re power cycle
    :param kwargs:
    device_id:   device id, default is 'r0'
    type:        master/backup, default is backup
    action:     reboot/power_cycle/kernel_crash, default is reboot
    :return:
    """
    t.log("inside re_actions")
    cst._check_bbe()
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    re_type = kwargs.get('type', 'backup')
    action = kwargs.get('action', 'reboot')
    origin_re = router.get_current_controller_name()
    backup_re = None
    for re_name in t.get_resource(device_id)['system']['primary']['controllers']:
        if re_name == router.get_current_controller_name():
            continue
        backup_re = re_name
        break
    picked_re = backup_re if re_type == 'backup' else origin_re
    if re_type == 'master':
        router.set_current_controller(controller=backup_re, system_node='primary')
    match = re.match(r're(\d+)', picked_re)
    if match:
        re_slot = match.group(1)
    if action == 'power_cycle':
        for command in ['power-off', 'power-on']:
            router.cli(command="show subscribers summary")
            t.log("RE {} will start powercycle".format(picked_re))
            router.cli(command="request system {} other-routing-engine".format(command))
            t.log("waiting 60s for route-engine state change")
            time.sleep(60)
            router.cli(command="show subscribers summary")

            if command == 'power-off':
                resp = router.pyez('get_route_engine_information', slot=re_slot).resp
                if resp.findtext('route-engine/mastership-state') == 'Present':
                    t.log('routing-engine {} was {}'.format(picked_re, command))
                else:
                    raise Exception("routing-engine {} was in abnormal state".format(picked_re))

            if command == 'power-on':
                t.log("routing-engine {} was {}".format(picked_re, command))
                cst.check_re_status(device_id=device_id, re_slot=re_slot)
                router.cli(command="show subscribers summary")

    if action == 'reboot':
        router.cli(command="show subscribers summary")
        t.log("RE {} will start reboot".format(picked_re))
        router.cli(command="request system reboot other-routing-engine")
        t.log("waiting 60s for route-engine state change")
        time.sleep(60)
        router.cli(command="show subscribers summary")
        cst.check_re_status(device_id=device_id, re_slot=re_slot)
        router.cli(command="show subscribers summary")

    if action == 'kernel_crash':
        router.cli(command="show subscribers summary")
        bbe_router = bbe.get_devices(devices=device_id)[0]
        if bbe_router.is_tomcat:
            tomcat_mode = True

        host = t.get_resource(device_id)['system']['primary']['controllers'][picked_re]['con-ip'] + '.' + \
               t.get_resource(device_id)['system']['primary']['controllers'][picked_re]['domain']
        t.log("will panic re {}".format(picked_re))
        cst.panic_re_recover(host=host, tomcat_mode=tomcat_mode)
        t.log("waiting 60s for route-engine state change")
        time.sleep(60)
        cst.check_re_status(device_id=device_id, re_slot=re_slot)
        router.cli(command="show subscribers summary")

    router.reconnect(all)


def interface_bounce(**kwargs):
    """
    interface_bounce(interface='xe-2/0/0:0', method='cli')
    :param kwargs:
    method:           bounce method, cli/laseroff , by default id laseroff
    interface:        the interface name
    interface_id:     interface id name , e.g. 'radius0'
    device_id:        device name, by default is 'r0'
    :return:
    """
    t.log("inside interface bounce action")
    cst._check_bbe()
    device = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device)
    method = kwargs.get('method', 'laseroff').lower()
    intfs = bbe.get_interfaces(device=device, interfaces='access')
    tester = t.get_handle('rt0')
    status = True
    interfaces = []
    for intf in intfs:
        interfaces.append(intf.interface_pic)

    ##if interface was not provided, choose a access interface randomly
    radius_interface = False
    if 'interface' in kwargs:
        interface = kwargs['interface']
    elif 'interface_id' in kwargs:
        interface = bbe.get_interfaces(device=device, interfaces=kwargs['interface_id'])[0].interface_pic
        if 'radius' in kwargs['interface_id']:
            radius_interface = True
    else:
        interface = random.choice(interfaces)

    router.cli(command='show interface {} terse'.format(interface))
    if method == 'cli':
        t.log('bounce(disable) interface {}'.format(interface))
        if radius_interface:
            router.cli(command="show network-access aaa radius-servers detail")
        if 'vcp' in interface:
            groups = re.match(r'vcp-(\d+)\/(\d+)\/(\d+)', interface)
            router.cli(command='request virtual-chassis vc-port delete fpc-slot {} pic-slot {} port {}'.
                       format(groups.group(1), groups.group(2), groups.group(3)))
            time.sleep(5)
            resp = router.cli(command="show interface {}".format(interface)).resp
            if 'error' in resp:
                t.log("interface {} was removed for vcps".format(interface))
            else:
                t.log('ERROR', "interface {} was not removed for vcps".format(interface))
                status = False
            router.cli(command='request virtual-chassis vc-port set fpc-slot {} pic-slot {} port {}'.
                       format(groups.group(1), groups.group(2), groups.group(3)))
            time.sleep(5)
            resp = router.cli(command="show interface {}".format(interface)).resp
            if 'error' in resp:
                t.log('ERROR', "interface {} was not added for vcps".format(interface))
                status = False
            else:
                t.log("interface {} was added for vcps".format(interface))

        else:
            for cmds in ['set', 'delete']:
                if cmds == 'set':
                    expected_state = 'down'
                if cmds == 'delete':
                    expected_state = 'up'
                command_list = [cmds+' interface '+interface+' disable', 'commit']
                resp = router.config(command_list=command_list).resp
                if 'error' in resp:
                    t.log('ERROR', 'the command {} was not accepted by router'.format(command_list))
                    status = False
                    router.config(command_list=['rollback'])
                    break
                time.sleep(5)
                resp = router.pyez('get_interface_information', level_extra='terse', interface_name=interface).resp
                state = resp.findtext('physical-interface/oper-status')
                if state != expected_state:
                    t.log('ERROR', 'interface {} state is {} after set action {}'.format(interface, state, cmds))
                    status = False
                else:
                    t.log('interface {} state is {} after set action {}'.format(interface, state, cmds))
                if radius_interface:
                    router.cli(command="show network-access aaa radius-servers detail")

    if method == 'laseroff':
        rt_port_handle = None
        for intf in intfs:
            if interface == intf.interface_pic:
                interface_id = intf.interface_id
                rt_interface = bbe.get_connection(device, interface=interface_id).interface_pic
                rt_port_handle = tester.port_to_handle_map[rt_interface]
                break

        rt_interface = bbe.get_connection(device, interface)
        t.log('bounce the tester port {} which connect to {}'.format(rt_interface, interface))
        for action in ['laseroff', 'laseron']:
            if action == 'laseroff':
                op_mode = 'sim_disconnect'
                expected_state = 'down'
            if action == 'laseron':
                op_mode = 'normal'
                expected_state = 'up'
            tester.invoke('interface_config', port_handle=rt_port_handle, op_mode=op_mode)
            time.sleep(5)
            resp = router.pyez('get_interface_information', level_extra='terse', interface_name=interface).resp
            state = resp.findtext('physical-interface/oper-status')
            if state != expected_state:
                t.log('ERROR', 'interface {} state is {} after set action {}'.format(interface, state, action))
                status = False
            else:
                t.log('interface {} state is {} after set action {}'.format(interface, state, action))

    if not status:
        raise Exception('interface {} state not in expected state after flapping'.format(interface))


def re_failover(**kwargs):
    """
    RE fail over
    :param kwargs:
    device_id:
    method:     reboot/power_cycle/kernel_crash, it will pick up one randomly if not provided
    :return:
    """
    method_list = ['reboot', 'power_cycle', 'kernel_crash']
    if 'method' in kwargs:
        method = kwargs['method']
    else:
        method = random.choice(method_list)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    master_re = cst.get_master_re_name(device_id)
    t.log("re failover will start with method {}".format(method))
    re_actions(device_id=device_id, type='master', action=method)
    t.log('re {} failed over after method {}'.format(master_re, method))

def fpc_actions(**kwargs):
    """
    fpc_actions(fpc='1', action='offon')
    :param kwargs:
    fpc:       fpc slot id e.g. '1'
    device_id:      router id e.g. 'r0'
    action:         restart/panic/offon
    :return:
    """
    t.log("inside fpc_actions")
    cst._check_bbe()
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    fpc_list = []
    if 'fpc' in kwargs:
        chosen_fpc = kwargs['fpc']
    else:
        access_list = bbe.get_interfaces(device=device_id, interfaces='access')
        if not access_list:
            t.log('WARN', "no access interface exist in yaml, skip the test")
            return
        for access in access_list:
            match = re.match(r'.*-(\d+)/\d+/\d+', access.interface_pic)
            if match:
                fpc_list.append(match.group(1))
        chosen_fpc = random.choice(fpc_list)
    action_list = ['restart', 'panic', 'offon']
    if 'action' in kwargs:
        action = kwargs['action']
    else:
        action = random.choice(action_list)
    t.log("start fpc {} with action {}".format(chosen_fpc, action))
    if action == 'restart':
        t.log('will restart fpc slot {}'.format(chosen_fpc))
        command = 'request chassis fpc restart slot {}'.format(chosen_fpc)
        resp = router.cli(command=command).resp
        match = re.match(r'Restart\s+initiated', resp)
        if match:
            t.log('fpc slot #{} restarted'.format(chosen_fpc))
        else:
            raise Exception('fpc slot {} can not be restarted'.format(chosen_fpc))
    if action == 'panic':
        t.log('will panic fpc slot {}'.format(chosen_fpc))
        resp = router.vty(command='set parser security 10', destination='fpc' + chosen_fpc).resp
        if re.search('Security level', resp):
            t.log('enter into vty security mode')
            router.vty(command='test panic', destination='fpc' + chosen_fpc, pattern='(.*)')
            t.log("waiting for core-dumps to be generated")
            # Wait for the core to be generated
            core_retries = 100
            core_interval = 5
            fpc_core_found = False
            while core_retries > 0:
                resp = router.cli(command='show system core-dumps').resp
                if not re.search('core-', resp):
                    core_retries -= 1
                else:
                    fpc_core_found = True
                    t.log("core dump generated for fpc {}".format(chosen_fpc))
                    break
                time.sleep(core_interval)
            if fpc_core_found is True:
                t.log('fpc core was generated during test panic, will remove it')
                router.cli(command='file delete /var/crash/core-*')
        else:
            raise Exception("not able to set vty security mode")
    if action == 'offon':
        t.log("will offline/online fpc slot {}".format(chosen_fpc))
        for item in ['offline', 'online']:
            if not re.match(r'MX(80|80-t|40|40-t|10|10-t|5|5-t)', router.get_model(), re.IGNORECASE):
                command = "request chassis fpc slot {} {}".format(chosen_fpc, item)
            else:
                command = "request chassis tfeb {}".format(item)
            resp = router.cli(command=command).resp
            if item == 'offline':
                match = re.match(r'Offline\s+initiated', resp)
                if match:
                    t.log('fpc slot #{} offline'.format(chosen_fpc))
                else:
                    raise Exception('fpc slot {} failed to be offline'.format(chosen_fpc))
            else:
                t.log('fpc slot {} enabled online command'.format(chosen_fpc))
    t.log("waiting 100s for fpc to come back")
    time.sleep(100)
    base_time = time.time()
    while True:
        resp = router.pyez('get_fpc_information', fpc_slot=chosen_fpc).resp

        if resp.findtext('fpc/state') == 'Online':
            t.log('fpc slot {} back to online'.format(chosen_fpc))
            break
        else:
            time.sleep(10)

        if (time.time() - base_time) > 600:
            raise Exception("FPC slot {} failed to come back online after 600s".format(chosen_fpc))

    rt_count = cst.get_rt_subs_info()['rt_sessions_up']
    router_count = cst.get_router_sub_summary(device_id)['active']
    time.sleep(10)
    base_time = time.time()
    while True:
        new_rt_count = cst.get_rt_subs_info()['rt_sessions_up']
        new_router_count = cst.get_router_sub_summary(device_id)['active']
        if new_router_count == router_count and new_rt_count == rt_count:
            t.log("router and tester user reached stable state")
            break
        else:
            rt_count = new_rt_count
            router_count = new_router_count
            t.log("Waiting 60s for client count to be stable on dut and rt")
            time.sleep(60)
        if time.time()-base_time > 3600:
            raise Exception("subscribers count still not stable after 3600s")


def daemon_actions(**kwargs):
    """
    daemon_actions(daemon_list=['jdhcpd','bbe-smgd'], re_in_action='re1',action='kill')
    :param kwargs:
    device_id:                device name e.g. 'r0'
    daemon_list:              a list of daemons
    action:                   restart/coredump/kill, by default is restart
    re_in_action:             re name, e.g. 're0'
    cpu_settle:               cpu idle value, by default is 50
    cpu_check:                True/False, default is True
    verify_traffic:           True/False, by default is False
    traffic_args:
    :return:
    """
    t.log("inside daemon_actions")
    cst._check_bbe()
    verify_traffic_enable = kwargs.get('verify_traffic', False)
    cpu_check = kwargs.get('cpu_check', True)
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    rt_device_id = kwargs.get('rt_device_id', 'rt0')
    tester = t.get_handle(rt_device_id)
    subs = kwargs.get('subs', bbe.get_subscriber_handles())
    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        t.log('start login subs {} before test'.format(subs))
        try:
            cst.cst_start_clients(**kwargs)
        except:
            t.log("failed to bring up subscriber")

    if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
        new_mesh = kwargs.get('new_mesh', True)
        duration = kwargs.get('duration', 60)
        if new_mesh:
            t.log('remove existing traffic mesh')
            tester.invoke('traffic_action', action='delete')
            time.sleep(5)
            t.log('add new traffic mesh for subs')
            cst.add_subscriber_mesh(**kwargs)
        if 'duration' in kwargs:
            cst.start_traffic(**kwargs)
        else:
            cst.start_traffic(duration=duration, **kwargs)
        time.sleep(int(duration))
        cst.verify_traffic(**kwargs)
        cst.start_traffic()

    daemon_action_cmds = {}
    daemon_action_cmds['authd'] = {'restart_cmd':'restart general-authentication-service',
                                   'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['jdhcpd'] = {'restart_cmd':'restart dhcp-service', 'cmds_before_action':[],
                                    'cmds_after_action':[]}
    daemon_action_cmds['dcd'] = {'restart_cmd':'restart interface-control', 'cmds_before_action':[],
                                 'cmds_after_action':[]}
    daemon_action_cmds['dfwd'] = {'restart_cmd':'restart firewall', 'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['cosd'] = {'restart_cmd':'restart class-of-service', 'cmds_before_action':[],
                                  'cmds_after_action':[]}
    daemon_action_cmds['pppd'] = {'restart_cmd':'restart ppp', 'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['jpppd'] = {'restart_cmd':'restart ppp-service',
                                   'cmds_before_action':["show route | grep Access-internal | count",
                                                         "show route terse | grep pp0 | count",
                                                         "show route | grep demux | count"],
                                   'cmds_after_action':["show route | grep Access-internal | count",
                                                        "show route terse | grep pp0 | count",
                                                        "show route | grep demux | count"]}
    daemon_action_cmds['pppoed'] = {'restart_cmd':'restart pppoe', 'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['l2-learning'] = {'restart_cmd':'restart l2-learning',
                                         'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['l2cpd-service'] = {'restart_cmd':'restart l2cpd-service',
                                           'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['jl2tpd'] = {'restart_cmd':'restart l2tp-universal-edge',
                                    'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['dfcd'] = {'restart_cmd':'restart dynamic-flow-capture',
                                  'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['autoconfd'] = {'restart_cmd':'restart auto-configuration',
                                       'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['bbe-smgd'] = {'restart_cmd':'restart smg-service',
                                      'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['pfed'] = {'restart_cmd':'restart statistics-service',
                                  'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['smid'] = {'restart_cmd':'restart subscriber-management',
                                  'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['bdbrepd'] = {'restart_cmd':'restart database-replication',
                                     'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['mib2d'] = {'restart_cmd':'restart mib-process',
                                   'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['snmpd'] = {'restart_cmd':'restart snmp', 'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['eventd'] = {'restart_cmd':'restart event-processing',
                                    'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['essmd'] = {'restart_cmd':'restart extensible-subscriber-services',
                                   'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['rpd'] = {'restart_cmd':'restart routing immediately',
                                 'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['diameterd'] = {'restart_cmd':'restart diameter-service immediately',
                                       'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['lacpd'] = {'restart_cmd':'restart lacp', 'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['pppoed'] = {'restart_cmd':'restart pppoe', 'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['chassisd'] = {'restart_cmd':'restart chassis-control',
                                      'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['ancpd'] = {'restart_cmd': 'restart ancpd-service', 'cmds_before_action':[], 'cmds_after_action':[]}
    daemon_action_cmds['bbe-statsd'] = {'restart_cmd': 'restart bbe-stats-service', 'cmds_before_action':[], 'cmds_after_action':[]}
    if 'nfx' in t.get_system(device_id)['primary']['model']:
        daemon_action_cmds['chassisd']['restart_cmd'] = 'restart chassis-control soft'
    if 'mx204' in t.get_system(device_id)['primary']['model']:
        daemon_action_cmds['chassisd']['restart_cmd'] = 'restart chassis-control soft'
    default_list = list(daemon_action_cmds.keys())
    daemon_list = kwargs.get('daemon_list', default_list)
    if not isinstance(daemon_list, list):
        daemon_list = [daemon_list]
    device = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device)

    default_cmds_before_action = ['show subscribers summary', 'show subscribers summary port']
    default_cmds_after_action = default_cmds_before_action

    master_re_name = cst.get_master_re_name(device)
    re_name = kwargs.get('re_in_action', master_re_name)
    if re_name != master_re_name:
        if hasattr(router, 'vc') and router.vc:
            master_node = re_name.split(sep='-')[0]
            rename = re_name.split(sep='-')[1]
            router.set_current_controller(controller=rename, system_node=master_node)
        else:
            router.set_current_controller(controller=re_name, system_node='primary')
        t.log('will start action in re {}'.format(re_name))
    action = kwargs.get('action', 'restart')
    for daemon in daemon_list:
        if daemon not in daemon_action_cmds:
            t.log("WARN", "daemon {} is not defined in daemon_action_cmds, will be skipped".format(daemon))
            continue
        resp = router.shell(command='ps -aux |grep {}'.format(daemon)).resp
        if not re.search('/' + daemon, resp):
            t.log("daemon {} is not running, will be skipped from the test".format(daemon))
            continue
        cmds_before_action = daemon_action_cmds[daemon]['cmds_before_action'] or default_cmds_before_action

        for cmds in cmds_before_action:
            router.cli(command=cmds, timeout=300)
            time.sleep(5)
        if action == 'restart':
            t.log("daemon {} will be restarted".format(daemon))
            router.cli(command=daemon_action_cmds[daemon]['restart_cmd'])
        if action in ['coredump', 'kill']:
            command = "ps axf | grep {} | grep -v grep".format(daemon)
            resp = router.shell(command=command).resp
            if re.match(r'\s?(\d+)\s+', resp):
                pid = re.match(r'\s?(\d+)\s+', resp).group(1)
            else:
                t.log("daemon {} is not in the system, will ignore it".format(daemon))
                continue
            router.su()
            if action == 'coredump':
                # Delete any daemon core if exists
                router.cli(command='file delete /var/tmp/{}.core*'.format(daemon))

                # Kill daemon with SIGABRT
                router.shell(command="kill -6 " + pid)

                # Check daemon is restarted with new pid
                restarted_with_new_pid = False
                new_pid_retries = 25
                new_pid_interval = 5
                new_pid = pid
                while new_pid_retries > 0:
                    time.sleep(new_pid_interval)
                    resp = router.shell(command=command).resp
                    m = re.match(r'\s?(\d+)\s+', resp)
                    if m is not None:
                        new_pid = m.group(1)
                    else:
                        t.log("daemon {} is not started yet".format(daemon))
                    if m is not None and new_pid != pid:
                        restarted_with_new_pid = True
                        t.log("daemon {} restarted with new pid {}".format(daemon, new_pid))
                        break
                    new_pid_retries -= 1

                if restarted_with_new_pid is False:
                    t.log("{} is not restarted after {} seconds".format(daemon, new_pid_retries * new_pid_interval))
                    raise Exception("daemon was not restarted")

                # Check daemon core dump
                core_retries = 100
                core_interval = 5
                daemon_core_found = False
                while core_retries > 0:
                    resp = router.shell(command="ls /var/tmp/{}.core*".format(daemon)).resp
                    if not re.search(daemon, resp):
                        core_retries -= 1
                    else:
                        daemon_core_found = True
                        t.log("core dump was generated for daemon {}".format(daemon))
                        break
                    time.sleep(core_interval)

                if daemon_core_found is False:
                    raise Exception("no core was generated for daemon {}".format(daemon))

                # Delete generated daemon core file
                # ywang tested on 19.2 that when daemon is core dumping, the helper is dumpd.
                dump_completed = False
                dump_retries = 100
                dump_interval = 10
                dump_cmd = "ps axf | grep dumpd | grep -v grep"

                while dump_retries > 0:
                    resp = router.shell(command=dump_cmd).resp
                    if re.search('dumpd', resp, re.MULTILINE):
                        time.sleep(dump_interval)
                        dump_retries -= 1
                        continue
                    else:
                        dump_completed = True
                        break

                if dump_completed:
                    router.cli(command='file delete /var/tmp/{}.core*'.format(daemon))
                    t.log("Deleted core dump generated by {}".format(daemon))
                else:
                    t.log("{} core dump is not completed after {} seconds".format(daemon, dump_retries * dump_interval))
                    raise Exception("daemon core dump takes too long")

            if action == 'kill':
                router.shell(command="kill -9 " + pid)
                time.sleep(5)
                resp = router.shell(command=command).resp
                new_pid = re.match(r'\s?(\d+)\s+', resp).group(1)
                if new_pid == pid:
                    #router.set_current_controller(controller=master_re_name, system_node='primary')
                    raise Exception("daemon {} was not killed".format(daemon))
                else:
                    t.log("daemon {} was killed, new pid is {}".format(daemon, new_pid))
        if cpu_check:
            BBEJunosUtil.cpu_settle(cpu_threshold=int(kwargs.get('cpu_process', 30)),
                                    idle_min=int(kwargs.get('cpu_settle', '75')),
                                    dead_time=int(kwargs.get('cpu_deadtime', 1200)),
                                    interval=int(kwargs.get('cpu_interval', 20)))
        check_client = kwargs.get('verify_client', False)
        if verify_utils.convert_str_to_num_or_bool(check_client):
            cst.verify_client_count(**kwargs)
        cmds_after_action = default_cmds_after_action if not daemon_action_cmds[daemon]['cmds_after_action'] else \
        daemon_action_cmds[daemon]['cmds_after_action']
        for cmds in cmds_after_action:
            router.cli(command=cmds, timeout=300)

        if verify_utils.convert_str_to_num_or_bool(verify_traffic_enable):
            cst.stop_traffic()
            cst.verify_traffic(**kwargs)
            if daemon != daemon_list[-1]:
                cst.start_traffic()

    if re_name != master_re_name:
        router.set_current_controller(controller=master_re_name, system_node='primary')
        t.log('switch back to master re {}'.format(master_re_name))

def kill_busy_process(**kwargs):
    """

    :param kwargs:
    :return:
    """

    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    resp = router.cli(command="show system processes extensive | except 0\\.00\\% | except 0\\:00 | except idle | match root").resp
    id_process_list = re.findall(r'\s+(\d+)\s+root.*\d+.\d+%\s+(.*)\r\n', resp)
    id_process_list = reversed(id_process_list)
    import itertools
    process_dict = dict(itertools.zip_longest(*[iter(id_process_list)] * 2, fillvalue=""))
    # for item in id_process_list:
    #     process_dict[item[1]] = item[0]
    t.log("process id list is {}".format(process_dict))
    chosen_process = None
    for process in process_dict:
        if process not in bbe.cst_action_stats['processed_daemon']:
            t.log("choose process {} to kill".format(process))
            chosen_process = process
            bbe.cst_action_stats['processed_daemon'].append(process)
            break

    if not chosen_process:
        chosen_process = random.choice(list(process_dict.keys()))
        t.log("randomly choose process {} to kill".format('chosen_process'))
    router.su()
    router.shell(command="kill -9 " + process_dict[chosen_process])
    time.sleep(5)
    resp = router.shell(command="ps -aux |grep {}".format(chosen_process)).resp
    new_pid = re.match(r'\s?(\d+)\s+', resp).group(1)
    if new_pid == process_dict[chosen_process]:
        raise Exception("daemon {} was not killed".format(chosen_process))
    else:
        t.log("daemon {} was killed, new pid is {}".format(chosen_process, new_pid))

def ae_reconfig(**kwargs):
    """

    :param kwargs:
    :return:
    """
    t.log("inside ae_reconfig actions")
    cst._check_bbe()
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    ae_members = cst.get_ae_info(**kwargs)
    if not ae_members:
        t.log("No AE interface exists, quit this testcase")
        return

    ae_intf = random.choice(list(ae_members.keys()))
    port_list = ae_members[ae_intf]['active'] + ae_members[ae_intf]['standby']
    chosen_port = random.choice(port_list)
    router.cli(command="show interfaces {} terse".format(chosen_port))
    resp = router.cli(command="show configuration interfaces | display set | match {}".format(chosen_port)).resp
    command_list = resp.splitlines()
    command_list.pop(0)
    command_list.pop(-1)
    t.log("start reconfig ae {}  member link {}".format(ae_intf, chosen_port))
    router.config(command_list=['delete interface'+chosen_port])
    router.commit()
    router.cli(command="show interfaces {} terse".format(chosen_port))
    time.sleep(10)
    router.config(command_list=command_list)
    router.commit()
    router.cli(command="show interfaces {} terse".format(chosen_port))
