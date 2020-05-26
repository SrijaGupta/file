'''
CST DTCP Test Suites
'''
import time
from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil
import random
import re
import jnpr.toby.bbe.cst.cstutils as cst
from jnpr.toby.utils.utils import run_multiple
import hmac
import hashlib
import paramiko

def dtcp_concurrent_trigger_test(**kwargs):
    """

    :param kwargs:
    device_id:                  router device id e.g."r0"
    max_trigger_count:          maximum trigger count, by default is 100, router support maximum 1024
    minimum_rx_percentage:                minimum percentage for received traffic
    maximum_rx_percentage:                maximum percentage for received traffic
    :return:
    """
    t.log("start dtcp concurrent trigger test")
    max_count = int(kwargs.get('max_trigger_count', 100))
    trigger_type = kwargs.get('trigger_type', 'interface_id')
    check_traffic = kwargs.get('verify_traffic', True)
    delay = kwargs.get('delay', 10)
    kwargs['mode'] = 'summary'
    cst.prepare_subscriber_traffic(**kwargs)
    t.log("trying to remove existing LI triggers")
    result = dtcp_list_li_trigger(**kwargs, noraise=True)
    if isinstance(result, list):
        dtcp_delete_li_trigger(criteria_id=result, **kwargs)
    response = get_dtcp_li_candidates(**kwargs)
    if len(response[trigger_type]) < max_count:
        max_count = len(response[trigger_type])
    users = response[trigger_type]
    group_a_count = round(len(users) / 2)
    group_a = random.sample(users, group_a_count)
    t.log("adding the dtcp trigger group first")
    dtcp_add_li_trigger(trigger_list=group_a, **kwargs)
    result = dtcp_list_li_trigger(**kwargs)

    obj1 = lambda: None
    obj2 = lambda: None
    obj1.member = group_a
    obj1.role = 'delete'
    obj1.criteria = result
    obj1.active = True
    group_b = [subs for subs in users if subs not in group_a]
    obj2.member = group_b
    obj2.role = 'add'
    obj2.active = False
    obj2.criteria = []
    for iteration in range(1, int(kwargs.get('iteration', 2)) + 1):
        t.log("start iteration #{} for parallel dtcp test".format(iteration))
        for subscriber in [obj1, obj2]:
            if subscriber.role == 'delete' and subscriber.active:
                dict2 = {'target': dtcp_delete_li_trigger, 'delay': delay, 'kwargs': {'criteria_id': subscriber.criteria, **kwargs}}
            elif subscriber.role == 'add' and not subscriber.active:
                dict1 = {'target': dtcp_add_li_trigger, 'delay': delay, 'kwargs': {'trigger_list': subscriber.member, 'trigger_type': trigger_type, **kwargs}}
        try:
            result = run_multiple([dict1, dict2])
        except:
            raise Exception("the parallel run of dtcp failed")

        if check_traffic:
            t.log("verify traffic in iteration {}".format(iteration))
            duration = kwargs.get('duration', 60)
            if 'duration' in kwargs:
                cst.start_traffic(**kwargs)
            else:
                cst.start_traffic(duration=duration, **kwargs)
            time.sleep(int(duration))
            maximum_percent = kwargs.get('maximum_rx_percentage', 100.5)
            minimum_percent = kwargs.get('minimum_rx_percentage', 99)
            t.log("expecting received traffic will be {} - {} percent in LI".format(minimum_percent, maximum_percent))
            cst.verify_traffic(**kwargs)

        for subscriber in [obj1, obj2]:
            if subscriber.role == 'add' and result[0]:
                subscriber.role = 'delete'
                subscriber.active = True
                subscriber.criteria = result[0]
            else:
                subscriber.role = 'add'
                subscriber.active = False
                subscriber.criteria = []
        t.log("after iteration #{}, current group1 role is {}, group2 role is {}".format(iteration, obj1.role, obj2.role))


def dtcp_logout_login_with_same_trigger_test(**kwargs):
    """
    This testcase can be used only when X-UserName is used to add triggers, and all subscribers with unique user name
    :param kwargs:
    device_id:                  router device id e.g."r0"
    max_trigger_count:          maximum trigger count, by default is 100, router support maximum 1024
    no_trigger_change:          True or False, default is True(add trigger once)
    minimum_rx_percentage:                minimum percentage for received traffic
    maximum_rx_percentage:                maximum percentage for received traffic
    :return:
    """
    t.log("start dtcp logout login test with same trigger")
    max_count = int(kwargs.get('max_trigger_count', 100))
    t.log("trying to remove existing LI triggers")
    result = dtcp_list_li_trigger(**kwargs, noraise=True)
    if isinstance(result, list):
        dtcp_delete_li_trigger(criteria_id=result, **kwargs)
    t.log("find out the current li candidates")
    response = get_dtcp_li_candidates(**kwargs)
    if len(response['username']) < max_count:
        max_count = len(response['username'])
    users = response['username']
    picked_triggers = random.sample(users, max_count)
    kwargs['trigger_list'] = users
    tester = t.get_handle(kwargs.get('rtdevice_id', 'rt0'))
    t.log("the picked triggers are {}".format(picked_triggers))
    no_trigger_change = kwargs.get('no_trigger_change', True)

    for iteration in range(1, int(kwargs.get('iteration', 1)) + 1):
        if iteration == 1 and no_trigger_change:
            t.log("adding dtcp triggers for one time only")
            dtcp_add_li_trigger(trigger_type='username', **kwargs)
        if not no_trigger_change:
            t.log("deleting dtcp triggers in iteration {}".format(iteration))
            dtcp_delete_li_trigger(**kwargs)
        t.log("logout client in iteration {}".format(iteration))
        cst.cst_release_clients(**kwargs)
        if not no_trigger_change:
            t.log("adding dtcp triggers in iteration {}".format(iteration))
            dtcp_add_li_trigger(trigger_type='username', **kwargs)
        time.sleep(10)
        t.log("starting to login clients in iteration {}".format(iteration))
        cst.cst_start_clients(**kwargs)
        new_mesh = kwargs.get('new_mesh', True)
        duration = kwargs.get('duration', 60)
        if new_mesh:
            t.log('remove existing traffic mesh')
            tester.invoke('traffic_action', action='delete')
            time.sleep(5)
        t.log('add new traffic mesh for subs in iteration {}'.format(iteration))
        cst.add_subscriber_mesh(**kwargs)
        if 'duration' in kwargs:
            cst.start_traffic(**kwargs)
        else:
            cst.start_traffic(duration=duration, **kwargs)
        time.sleep(int(duration))
        t.log('verify traffic in iteration {}'.format(iteration))
        maximum_percent = kwargs.get('maximum_rx_percentage', 100.5)
        minimum_percent = kwargs.get('minimum_rx_percentage', 99)
        t.log("expecting received traffic will be {} - {} percent in LI".format(minimum_percent, maximum_percent))
        kwargs['mode'] = 'summary'
        cst.verify_traffic(**kwargs)

        BBEJunosUtil.cpu_settle(cpu_threshold=50, idle_min=int(kwargs.get('cpu_settle', 60)),
                                dead_time=1200, interval=20)



def dtcp_confidentiality_test(**kwargs):
    """
    Make sure intercept ID is not visible to AAA operator in 'show network-access aaa subscribers session-id <id> detail/brief.
    :param kwargs:
    :return:
    """
    t.log("start dtcp confidentiality test")
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    max_count = int(kwargs.get('max_trigger_count', 100))
    trigger_type = kwargs.get('trigger_type', 'interface_id')
    intercept_id = kwargs.get('intercept_id', '001122334455667788')
    kwargs['mode'] = 'summary'
    cst.prepare_subscriber_traffic(**kwargs)
    t.log("trying to remove existing LI triggers")
    result = dtcp_list_li_trigger(**kwargs, noraise=True)
    if isinstance(result, list):
        dtcp_delete_li_trigger(criteria_id=result, **kwargs)
    t.log("find out the current li candidates")
    response = get_dtcp_li_candidates(**kwargs)
    if len(response[trigger_type]) < max_count:
        max_count = len(response[trigger_type])
    users = response[trigger_type]
    user_session = dict(zip(users, response['session_id']))

    picked_triggers = random.sample(users, max_count)
    picked_session_id = []
    for trigger in picked_triggers:
        picked_session_id.append(user_session[trigger])
    t.log("the picked triggers are {}".format(picked_triggers))
    t.log("add triggers")
    dtcp_add_li_trigger(trigger_list=users, **kwargs)
    t.log("verify triggers count")
    resp = dtcp_list_li_trigger(**kwargs)
    if isinstance(resp, list):
        li_count = len(resp)
        if li_count == max_count:
            t.log("all specified {} li triggers in the router".format(li_count))
        else:
            raise Exception("only {} li triggers in the router, not the expected {}".format(li_count, max_count))
    else:
        raise Exception("no criteria id returned, please check logs")

    t.log("check the output of cli command, verify the intercept id is not available")
    for session in picked_session_id:
        resp = router.cli(command='show network-access aaa subscribers session-id {} detail'.format(session)).resp
        resp2 = router.cli(command='show network-access aaa subscribers session-id {}'.format(session)).resp
        if re.search(r'{}'.format(intercept_id), resp+resp2):
            t.log("intercept id for session {} is found in cli output".format(session))
            raise Exception("intercept id should not be visible in cli output")

    dtcp_delete_li_trigger(**kwargs)


def dtcp_trigger_test(**kwargs):
    """

    :param kwargs:
    device_id:                  router device id e.g."r0"
    max_trigger_count:          maximum trigger count, by default is 100, router support maximum 1024
    trigger_type:               interface_id/username, by default is interface_id
    minimum_rx_percentage:                minimum percentage for received traffic
    maximum_rx_percentage:                maximum percentage for received traffic
    :return:
    """
    kwargs['mode'] = 'summary'
    duration = kwargs.get('duration', 60)
    cst.prepare_subscriber_traffic(**kwargs)
    max_count = int(kwargs.get('max_trigger_count', 100))
    trigger_type = kwargs.get('trigger_type', 'interface_id')
    ###remove existing triggers
    t.log("trying to remove existing LI triggers")
    result = dtcp_list_li_trigger(**kwargs, noraise=True)
    if isinstance(result, list):
        dtcp_delete_li_trigger(criteria_id=result, **kwargs)
    t.log("find out the current li candidates")
    response = get_dtcp_li_candidates(**kwargs)
    if len(response[trigger_type]) < max_count:
        max_count = len(response[trigger_type])
    users = response[trigger_type]

    picked_triggers = random.sample(users, max_count)
    t.log("the picked triggers are {}".format(picked_triggers))
    t.log("add triggers")
    dtcp_add_li_trigger(trigger_list=users, **kwargs)
    t.log("verify triggers count")
    resp = dtcp_list_li_trigger(**kwargs)
    if isinstance(resp, list):
        li_count = len(resp)
        if li_count == max_count:
            t.log("all specified {} li triggers in the router".format(li_count))
        else:
            raise Exception("only {} li triggers in the router, not the expected {}".format(li_count, max_count))
    else:
        raise Exception("no criteria id returned, please check logs")

    if 'duration' in kwargs:
        cst.start_traffic(**kwargs)
    else:
        cst.start_traffic(duration=duration, **kwargs)
    time.sleep(int(duration))
    maximum_percent = kwargs.get('maximum_rx_percentage', 100.5)
    minimum_percent = kwargs.get('minimum_rx_percentage', 99)
    t.log("expecting received traffic will be {} - {} percent in LI".format(minimum_percent, maximum_percent))
    cst.verify_traffic(**kwargs)

    t.log("remove triggers after test")
    dtcp_delete_li_trigger(**kwargs)


def dtcp_flowtap_client(**kwargs):
    """

    :param kwargs:
    device_id:                  router device id e.g."r0"
    dtcp_cmds:                  dtcp commands
    append_sequence_num:        True/False, default is True
    username:                   LI username, default is LI-user
    password:                   LI password, default is joshua1
    timeout:                    time out, default is 30
    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    router.reconnect(all)
    master_re = cst.get_master_re_name(device_id)
    no_raise = kwargs.get('noraise', False)
    if 'hostname' in kwargs:
        hostname = kwargs['hostname']
    else:
        hostname = t._get_system(resource=device_id, system_node='primary', controller=master_re, attribute='hostname')
        domain = t._get_system(resource=device_id, system_node='primary', controller=master_re, attribute='domain')
        hostname = hostname + '.' + domain
    #connect_addr = t._get_system(resource=device_id, system_node='primary', controller='re0', attribute='mgt-ip')

    status = True
    username = kwargs.get('username', 'LI-user')
    password = kwargs.get('password', 'joshua1')
    key = 'Juniper'
    key = bytes(key, 'utf-8')
    dtcp_cmds = kwargs['dtcp_cmds']
    if not isinstance(dtcp_cmds, list):
        dtcp_cmds = [dtcp_cmds]

    timeout = int(kwargs.get('timeout', 30))
    retry = 0
    while True:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, port=32001, username=username, password=password, timeout=timeout)
        transport = client.get_transport()
        channel = transport.open_session()
        channel.invoke_subsystem('flow-tap-dtcp')
        t.log('channel is {}'.format(channel))
        criteria = []
        if not hasattr(bbe, 'dtcp_criteria'):
            bbe.dtcp_criteria = []
        if not hasattr(bbe, 'dtcp_seq_num'):
            bbe.dtcp_seq_num = 1
        error_count = 0
        for command in dtcp_cmds:
            dtcp_command = command + "Seq: {}\r\n".format(bbe.dtcp_seq_num)
            msg = bytes(dtcp_command, 'utf-8')
            digest_maker = hmac.new(key, msg, hashlib.sha1)
            digest = digest_maker.hexdigest()
            dtcp_command += "Authentication-Info: {}\r\n\r\n".format(digest)

            result = channel.send(dtcp_command)
            t.log("sending dtcp command {}, result is {}".format(dtcp_command, result))
            base_time = time.time()
            while not channel.recv_ready():
                time.sleep(1)
                t.log('waiting for data ready')
                if time.time() - base_time > timeout:
                    raise Exception("did not receive any data from router")
            if result > 0:
                data = channel.recv(1024*490)
                if isinstance(data, int):
                    raise Exception("dtcp channel was closed unexpectedly")
                else:
                    data = data.decode('utf-8')
                    t.log("received response {}".format(data))
                    if '200 OK' not in data:
                        status = False
                        error_count += 1
                        if not no_raise:
                            t.log('ERROR', 'DTCP command received unexpected result')
                    elif 'CRITERIA-NUM' in data:
                        ###get the criteria id from list output
                        match = re.findall(r'CRITERIA-ID:\s*(\d+)', data)
                        criteria += match
                    elif 'ADD' in command:
                        match = re.search(r'CRITERIA-ID:\s*(\d+)', data)
                        bbe.dtcp_criteria.append(match.group(1))
                        criteria.append(match.group(1))
                bbe.dtcp_seq_num += 1
                retry = 0
            else:
                client.close()
                ##retry to send the command
                retry += 1
                if retry <= 3:
                    t.log("start retry #{} to send the command")
                else:
                    raise Exception("failed to send command after retries")
                break
        if retry == 0:
            break
    client.close()
    if not status:
        if not no_raise:
            raise Exception("#{} DTCP commands failed".format(error_count))
        else:
            return False
    else:
        if criteria:
            return criteria
    return status

def dtcp_delete_li_trigger(**kwargs):
    """
    username:                               LI operator name
    password:                               LI operator password
    device_id:                              router device id, e.g.'r0'
    criteria_id:                            criteria id used to identify the LI flow
    noraise:                                Specify if you want to raise exception on command failure or continue your script(True/False)
    :param kwargs:
    :return:
    """
    version = kwargs.get('version', '0.7')
    username = kwargs.get('username', 'LI-user')
    cdest = kwargs.get('cdest', 'md1')
    criteria_id = kwargs.get('criteria_id', None)
    flags = kwargs.get('flags', 'STATIC')
    dtcp_list = []
    if 'criteria_id' in kwargs:
        if not isinstance(criteria_id, list):
            criteria_id = [criteria_id]
        for cid in criteria_id:
            cmd_template = "DELETE DTCP/{}\r\n".format(version)
            cmd_template += "Csource-ID: {}\r\n".format(username)
            cmd_template += "CRITERIA-ID: {}\r\n".format(cid)
            cmd_template += "Flags: STATIC\r\n"
            dtcp_list.append(cmd_template)
    else:
        cmd_template = "DELETE DTCP/{}\r\n".format(version)
        cmd_template += "Csource-ID: {}\r\n".format(username)
        cmd_template += "Cdest-ID: {}\r\n".format(cdest)
        cmd_template += "Flags: {}\r\n".format(flags)
        dtcp_list.append(cmd_template)

    if dtcp_flowtap_client(dtcp_cmds=dtcp_list, **kwargs):
        if 'criteria_id' in kwargs:
            for cid in criteria_id:
                bbe.dtcp_criteria.remove(cid)


def dtcp_add_li_trigger(**kwargs):
    """
    Flags: STATIC
    :param kwargs:
    device_id:                              router device id, e.g.'r0'
    username:                               LI operator name
    password:                               LI operator password
    trigger_type:                           interface_id/username/ip_addr/session_id
    trigger_list:                           a list of trigger
    noraise:                                Specify if you want to raise exception on command failure or continue your script(True/False)
    :return:
    """
    version = kwargs.get('version', '0.7')
    username = kwargs.get('username', 'LI-user')
    cdest = kwargs.get('cdest', 'md1')
    priority = kwargs.get('priority', '2')
    dest_addr = kwargs.get('md_address', '21.20.10.2')
    dest_port = kwargs.get('md_port', '7890')
    src_addr = kwargs.get('source_address', '100.0.0.1')
    src_port = kwargs.get('source_port', '12321')
    intercept_id = kwargs.get('intercept_id', '001122334455667788')
    trigger_type = kwargs.get('trigger_type', 'interface_id')
    dtcp_list = []
    trigger_list = kwargs['trigger_list']
    flags = kwargs.get('flags', 'STATIC')
    if not isinstance(trigger_list, list):
        trigger_list = [trigger_list]
    for trigger in trigger_list:
        cmd_template = "ADD DTCP/{}\r\n".format(version)
        cmd_template += "Csource-ID: {}\r\n".format(username)
        cmd_template += "Cdest-ID: {}\r\n".format(cdest)
        cmd_template += "Priority: {}\r\n".format(priority)
        cmd_template += "X-JTap-Cdest-Dest-Address: {}\r\n".format(dest_addr)
        cmd_template += "X-JTap-Cdest-Dest-Port: {}\r\n".format(dest_port)
        cmd_template += "X-JTap-Cdest-Source-Address: {}\r\n".format(src_addr)
        cmd_template += "X-JTap-Cdest-Source-Port: {}\r\n".format(src_port)
        cmd_template += "X-MD-Intercept-Id: {}\r\n".format(intercept_id)
        if 'interface_id' in trigger_type:
            cmd_template += "X-Interface-Id: {}\r\n".format(trigger)

        if 'username' in trigger_type:
            cmd_template += "X-UserName: {}\r\n".format(trigger)
        if 'session_id' in trigger_type:
            cmd_template += "X-Act-Sess-Id: {}\r\n".format(trigger)
        if 'ip_addr' in trigger_type:
            cmd_template += "X-IP-Addr: {}\r\n".format(trigger)
        cmd_template += "Flags: {}\r\n".format(flags)
        dtcp_list.append(cmd_template)

    return dtcp_flowtap_client(dtcp_cmds=dtcp_list, **kwargs)


def dtcp_list_li_trigger(**kwargs):
    """

    :param kwargs:
    device_id:                              router device id, e.g.'r0'
    username:                               LI operator name
    password:                               LI operator password
    cdest:                                  ID of the mediation device
    noraise:                                Specify if you want to raise exception on command failure or continue your script(True/False)
    :return:
    """
    version = kwargs.get('version', '0.7')
    username = kwargs.get('username', 'LI-user')
    cdest = kwargs.get('cdest', 'md1')
    cmd_template = "LIST DTCP/{}\r\n".format(version)
    cmd_template += "Csource-ID: {}\r\n".format(username)
    cmd_template += "Cdest-ID: {}\r\n".format(cdest)
    cmd_template += "Flags: BOTH\r\n"

    return dtcp_flowtap_client(dtcp_cmds=cmd_template, **kwargs)


def get_dtcp_li_candidates(**kwargs):
    """
    get the interface or username from subs, return a hash with username/interface as key
    :param kwargs:
    :return:
    """
    device_id = kwargs.get('device_id', bbe.get_devices(device_tags='dut', id_only=True)[0])
    router = t.get_handle(device_id)
    result = {}
    result['interface_id'] = []
    result['username'] = []
    result['session_id'] = []
    for client_type in ['pppoe', 'ppp', 'dhcp']:
        resp = router.pyez('get_subscribers', client_type=client_type, detail=True, timeout=600).resp
        for interface in resp.findall('subscriber/interface'):
            if interface.text == "*":
                continue
            elif interface.text and interface.text not in result['interface_id']:
                result['interface_id'].append(interface.text)
        for name in resp.findall('subscriber/user-name'):
            if name.text and name.text not in result['username']:
                result['username'].append(name.text)
        for session in resp.findall('subscriber/session-id'):
            if session.text and session.text not in result['session_id']:
                result['session_id'].append(session.text)
    return result
