"""
Copyright (C) 2015-2016, Juniper Networks, Inc.
All rights reserved.
Authors:
    bphillips, saptaswa, shreya, ajaykv, jpzhao
Description:
    Toby Interface Trigger Library.
    many triggers are converted from JT libraries, original authors are noted in each such trigger.

Usage(s)
    Run Event   Restart Process
    Run Event   Kill Daemon
    Run Event   Deactivate Activate config
    Run Event   Disable Enable config
    Run Event   Set Delete config
    Run Event   ON CONFIG
    Run Event   ON CLI
    Run Event   ON SHELL
    Run Event   ON VTY
    Run Event   ON CLI-PFE
    Run Event   Restart App
    Run Event   Kill App
"""
# pylint: disable=locally-disabled,undefined-variable,too-many-branches,invalid-name,bad-whitespace,import-error

import re
#import copy
#import os
#import types
import time
import jnpr.toby.hardware.chassis.chassis as chassis
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hldcl.device import reconnect_to_device
from jnpr.toby.engines.events.event_engine_utils import elog, get_pfe, nice_string
from jnpr.toby.engines.events.event_engine_utils import get_dh_name, cli_pfe, hshell, vhclient

def _check_vmhost(dh, model):
    '''
    _check_vmhost
    '''
    if dh.__dict__.get('isVMHost') is None:
        if re.search(r'^(mx|ptx)', model, re.I):
            res = dh.shell(command='sysctl -a | grep vmhost_mode').response()
        else:
            res = dh.shell(command='sysctl -a | grep vm_mode').response()

        if re.match(r'hw.re.vmhost_mode: 1', res) or re.match(r'hw.re.vm_mode: 1', res):
            dh.su()
            dh.isVMHost = True
        else:
            return False
    return True

def kill_daemon(dh, **kwargs):
    '''
    kill_daemon
    '''
    sub = chassis.function_name(dh)
    model= dh.get_model()
    router_name = get_dh_name(dh)
    signal = kwargs.get('signal', 9)
    timeout = kwargs.get('timeout', 70)
    daemon = kwargs.get('daemon', 'rpd')
    mode = kwargs.get('mode', 'shell')
    # Finding the pid of daemon
    #vmhost=_check_vmhost(dh, model)
    pid1=_check_daemon(dh, daemon, mode)


    if pid1 is None:
        elog('warn', '%s cannot find pid for %s ,it is not running on %s' % \
                    (sub, daemon, router_name))
        return False
    else:
        elog('The pid for %s daemon is %s' % (daemon, pid1))

    #The start time noted before killing
    start_time=time.time()

    # kill daemon
    dh.su()
    process_cmd = "kill -%s %s" % (signal, pid1)      
    if mode == 'hshell':
        hshell(dh, process_cmd)
    elif mode == 'vmhost':
        vhclient(dh, process_cmd)
    else:
        dh.shell(command=process_cmd)

    #Finding the new pid of daemon

    while time.time() - start_time < timeout:
        pid_new=_check_daemon(dh, daemon, mode)
        #Matching the old pid with new pid
        if pid_new and pid1 != pid_new:
            elog('daemon %s killed successfully on %s' % (daemon, router_name))
            break
        time.sleep(1)

    time_spent=time.time()-start_time
    if time_spent<timeout:
        elog('daemon %s restarted in %s seconds on %s, the new pid is %s' % \
                        (daemon, round(time_spent), router_name, pid_new))
    else:
        elog('warn', 'daemon %s failed to restart in %s seconds on %s' % \
                    (daemon, round(time_spent), router_name))
        return False

    return True

def _check_daemon(dh, daemon, mode='shell'):
    '''
    _check_daemon
    '''
    #vmhost=_check_vmhost(dh, model)
    #TVP = _check_tvp(dh, model)
    process_cmd = ("ps caux|grep -v grep|grep {0}".format(daemon))
    process_cmd2 = ("ps -aux|grep -v grep|grep {0}".format(daemon))

    if mode == 'cli':
        process_cmd = ("show system processes extensive")
        resp_obj = dh.cli(command=process_cmd)
        dh.su()
        resp = resp_obj if isinstance(resp_obj, str) else resp_obj.response()
        pattern = r"\d+ (?=.*{0})".format(daemon)
        matches = re.search(pattern, resp, re.M)
        if matches:
            pid = int(matches.group())
        else:
            pid = None
        return pid


    elif mode == 'shell':
        resp_obj = dh.shell(command=process_cmd)
        resp = resp_obj if isinstance(resp_obj, str) else resp_obj.response()
        pattern = r"\d+ (?=.*{0})".format(daemon)
        matches = re.search(pattern, resp, re.M)
        if matches:
            pid = int(matches.group())
        else:
            resp_obj = dh.shell(command=process_cmd2)
            resp = resp_obj if isinstance(resp_obj, str) else resp_obj.response()
            pattern = r"\d+ (?=.*{0})".format(daemon)
            matches = re.search(pattern, resp, re.M)
            if matches:
                pid = int(matches.group())
            else:
                pid = None

        return pid



    elif mode == 'hshell':
        resp_obj = hshell(dh, process_cmd)
        resp = resp_obj if isinstance(resp_obj, str) else resp_obj.response()
        pattern = r"\d+ (?=.*{0})".format(daemon)
        matches = re.search(pattern, resp, re.M)
        if matches:
            pid = int(matches.group())
        else:
            resp_obj = hshell(dh, process_cmd2)
            resp = resp_obj if isinstance(resp_obj, str) else resp_obj.response()
            pattern = r"\d+ (?=.*{0})".format(daemon)
            matches = re.search(pattern, resp, re.M)
            if matches:
                pid = int(matches.group())
            else:
                pid = None
        return pid


    elif mode == 'vmhost':
        resp = None
        pid = None
        process_cmd = ("pidof {0}".format(daemon))
        resp_obj = vhclient(dh, process_cmd)
        resp = resp_obj if isinstance(resp_obj, str) else resp_obj.response()
        if resp:
            pid = int(resp)
        return pid

def _check_master_re(dh):
    '''
    _check_master_re
    '''
    res = dh.shell(command='sysctl -a | grep hw.re.mastership:').response()
    if re.match(r'hw.re.mastership: 1', res):
        return True
    return False

def _check_dual_re(dh):
    '''
    _check_dual_re
    '''
    cmd_dual = ('show chassis routing-engine | display xml')
    r = dh.cli(command=cmd_dual)
    res = r.response()
    root = parseString(res)
    routing_engine_list = root.getElementsByTagName('mastership-state')
    for routing_engine in routing_engine_list :
        if re.search('backup', routing_engine.firstChild.nodeValue, re.I):
            return True
    return False

def change_config_state(dh, **kwargs):
    '''
    change_config_state
    '''
    config = kwargs.get('config')
    action = kwargs.get('action')

    if re.search(r'deactivate', action):
        cmd=("deactivate {0}".format(config))
    elif re.search(r'activate', action):
        cmd=("activate {0}".format(config))
    elif re.search(r'disable', action):
        cmd=("set {0} disable".format(config))
    elif re.search(r'enable', action):
        cmd=("delete {0} disable".format(config))

    dh.config(command_list = [cmd])
    res = dh.commit(timeout=600)
    if not res:
        dh.log(message="Commit failed: %s %s" % (action, config), level="error")
        return False
    return True


def deactivate_activate_config(dh, **kwargs):
    '''
    deactivate_activate_config
    '''
    model = dh.get_model().lower()
    sub = chassis.function_name(dh) + "(%s)" % model
    rn = get_dh_name(dh)
    config = kwargs.get('config')
    err = 0
    start_time = time.time()
    interval = kwargs.get('interval', 5)


    #CHECK before configuring deactivate , (if its already done | if its possible )
    elog('== Deactivate {} congiguration started'.format(config), **kwargs)
    res_chk_deactivate = check_deactivate_activate_config(dh=dh, config=config, \
                                action="deactivate")
    if res_chk_deactivate is False:
        if change_config_state(dh=dh, config=config, action="deactivate"):
            if check_deactivate_activate_config(dh=dh, config=config, action="deactivate"):
                dh.log(message="%s deactivate %s successful" % \
                                (rn, config))
            else:
                dh.log(message="1 %s deactivate %s failed" % \
                                (rn, config), level="warn")
        else:
            dh.log(message="2 %s deactivate %s failed" % \
                            (rn, config), level="warn")
            dh.log(message="There might be feature dependancies that require this config, \
                            check the commit error carefully. You may chose to skip this \
                            testcase.", level="warn")

    time.sleep(float(interval))

    #CHECK before configuring activate , (if its already done | if its possible )
    elog('== Activate {} congiguration started'.format(config), **kwargs)
    res_chk_activate = check_deactivate_activate_config(dh=dh, config=config, \
                                action="activate")
    if res_chk_activate is False:
        if change_config_state(dh=dh, config=config, action="activate"):
            if check_deactivate_activate_config(dh=dh, config=config, action="activate"):
                dh.log(message="%s activate %s successful" % \
                                (rn, config))
        else:
            dh.log(message="%s activate %s failed" % \
                            (rn, config), level="warn")
            err += 1

    time_spent = time.time() - start_time

    if not err:
        dh.log(message="%s on %s (%s):finished in %s seconds" % (sub, rn, config, time_spent))
        return True
    else:
        dh.log(message="%s on %s (%s):failed after %s seconds" % \
                        (sub, rn, config, time_spent), level="error")
        return False


def check_deactivate_activate_config(dh, **kwargs):
    '''
    check_deactivate_activate_config
    '''
    config = kwargs.get('config')
    action = kwargs.get('action', None)
    res = dh.config(command_list=['show {} '.format(config)])
    if res.response() == '':
        elog('warn', 'The particular configuration is not set in the router')
        return False
    state = 'activate'
    #if re.search('inactive:', res.response()):
    REGEX = re.compile(r'##\s+inactive:\s+{}'.format(config))
    if re.search(REGEX, res.response()):
        state = 'deactivate'
    if action is None:
        return state
    else:
        return  bool(re.match(state, action, re.I))


def disable_enable_config(dh, **kwargs):
    '''
    disable_enable_config
    '''
    model = dh.get_model().lower()
    sub = chassis.function_name(dh) + "(%s)" % model
    rn = dh.shell(command='hostname').response()
    config = kwargs.get('config')
    err = 0
    start_time = time.time()
    interval = kwargs.get('interval', 5)

    #CHECK before configuring disable , (if its already done | if its possible )
    dh.log(message="Disable %s congiguration started" % (config), level="info")
    elog('== Disable congiguration started', **kwargs)
    res_chk_disable = _check_disable_enable_config(dh=dh, config=config, action='disable')
    if res_chk_disable is False:
        if change_config_state(dh=dh, config=config, action='disable'):
            if _check_disable_enable_config(dh=dh, config=config, action='disable'):
                dh.log(message="%s disable %s successful" % \
                                (rn, config))
        else:
            dh.log(message="%s disable %s failed" % \
                        (rn, config), level="warn")
            dh.log(message="There might be feature dependancies that require this config, \
                check the commit error carefully. You may chose to skip this testcase.", \
                level="warn")

    time.sleep(float(interval))

    #CHECK before configuring enable , (if its already done | if its possible )
    dh.log(message="Enable %s congiguration started" % (config),level="info")
    elog('== Enable congiguration started', **kwargs)
    res_chk_disable = _check_disable_enable_config(dh=dh,config=config,action='enable')
    if res_chk_disable is False:
        if change_config_state(dh=dh,config=config,action='enable'):
            if _check_disable_enable_config(dh=dh,config=config,action='enable'):
                dh.log(message="%s enable %s successful" % \
                                (rn,config))
        else:
            dh.log(message="%s enable %s failed" % \
                            (rn,config),level="warn")
            err += 1

    time_spent = time.time() - start_time

    if not err:
        dh.log(message="%s on %s (%s):finished in %s seconds" % (sub,rn,config,time_spent))
        return True
    else:
        dh.log(message="%s on %s (%s):failed after %s seconds" % (sub,rn,config,time_spent), \
                    level="error")
        return False


def _check_disable_enable_config(dh, **kwargs):
    '''
    _check_disable_enable_config
    '''
    config = kwargs.get('config')
    action = kwargs.get('action', None)
    res = dh.config(command_list=['show {} disable'.format(config)])
    state = 'enable'
    if re.search('disable', res.response()):
        state = 'disable'
    if action is None:
        return state
    else:
        if re.match(state, action, re.I):
            return True
        else:
            return False

def set_delete_config(dh, protocol, **kwargs):
    '''
    set_delete_config
    default action is 'toggle', as the name implies.
    '''
    device = kwargs.get('device')
    model = dh.get_model().lower()
    sub = chassis.function_name(dh) + "(%s)" % model
    action = kwargs.get('action', 'toggle')
    interval = kwargs.get('interval', 5)

    if dh.__dict__.get('protocol_info') is None:
        dh.protocol_info = {}

    if dh.protocol_info.get('{}_{}'.format(device, protocol)) is None:
        protocol_config = {}

    start_time = time.time()
    cmd = ('show protocols {} | display set | display inheritance'.format(protocol))

    if not dh.protocol_info.get('{}_{}'.format(device, protocol)):
        protocol_config = dh.config(command_list=[cmd]).response()
        dh.protocol_info['{}_{}'.format(device,protocol)] = protocol_config

    if re.match(r'set|up|on', action, re.I):
        elog('== set congiguration started', **kwargs)
        if dh.protocol_info.get('{}_{}'.format(device, protocol)):
            protocol_config_list = dh.protocol_info['{}_{}'.format(device, protocol)]
            dh.config(command_list=[protocol_config_list,'commit'])
        else:
            dh.log(message="%s : No protocols %s configuration found for action %s" % \
                        (sub, protocol, action), level="error")
            return False

    elif re.match(r'delete|down|off', action, re.I):
        elog('== delete congiguration started', **kwargs)
        if dh.protocol_info.get('{}_{}'.format(device, protocol)):
            dh.config(command_list=['delete protocols ' + protocol, 'commit'])
        else:
            dh.log(message="%s : No protocols %s configuration found for action %s" % \
                            (sub, protocol, action), level="error")
            return False

    elif re.match(r'flap|toggle|bounce', action, re.I):
        elog('== delete/set congiguration', **kwargs)
        if dh.protocol_info.get('{}_{}'.format(device, protocol)):
            dh.config(command_list=['delete protocols ' + protocol, 'commit'])
        else:
            dh.log(message="%s : No protocols %s configuration found for action %s" % \
                            (sub, protocol, action), level="error")
            return False
        time.sleep(float(interval))
        if dh.protocol_info.get('{}_{}'.format(device, protocol)):
            protocol_config_list = dh.protocol_info['{}_{}'.format(device, protocol)]
            dh.config(command_list=[protocol_config_list,'commit'])
        else:
            dh.log(message="%s : No protocols %s configuration found for action %s" % \
                        (sub, protocol, action), level="error")
            return False
    else:
        dh.log('error', '{} :Unknown action.'.format(sub))
        return False

    end_time = time.time()
    t.log('info', sub + ': execution finished at {}, takes {}'.format(str(end_time), \
                  str(end_time - start_time)))
    return True


def on_cli(dh, command, **kwargs):
    '''
    run_shell commands
    Can pass in the TOBY core option args, example: pattern=yes,no
    '''
    cmd_list = []
    if isinstance(command, str):
        command = command.split(',')
 
    if isinstance(command, list):
        for cmd in command:
            if(re.match(r'^\s*\'(.*)\'\s*$',cmd)):
                cmd = re.sub(r'^\s*["\'](.*)["\']\s*$',r'\g<1>',cmd)
                print(cmd)
            if(re.match(r'^\s*"(.*)"\s*$',cmd)):
                cmd = re.sub(r'^\s*["\'](.*)["\']\s*$',r'\g<1>',cmd)
                print(cmd)
            cmd_list.append(cmd)

    for cmd in cmd_list:
        elog('run cli cmd: {}'.format(cmd), **kwargs)
        try:
            res = dh.cli(command=cmd, **kwargs)
            output = res.response()
            if res.status() is True:
                if re.search(r'syntax error|warning|not running|missing argument', output, re.I):
                    t.log('warn', "cli cmd <{}> return errors: {}".format(cmd, output))
                    return False
                else:
                    dh.log("cli cmd '{}' run successfully".format(cmd))
                #input('check')
            else:
                dh.log('Toby HLDCL returns error:' + res.response())
                return False

        except Exception as err:
            msg = "cli cmd '{}' failed: {}".format(cmd, str(err))
            dh.log('warn', msg)
            return False

    elog('done with cli commands as event')
    return True

def on_config(dh, command, **kwargs):
    '''
    run_config
    '''
    cmd_list = []
    if isinstance(command, str):
        command = command.split(',')
 
    if isinstance(command, list):
        for cmd in command:
            if(re.match(r'^\s*\'(.*)\'\s*$',cmd)):
                cmd = re.sub(r'^\s*["\'](.*)["\']\s*$',r'\g<1>',cmd)
                print(cmd)
            if(re.match(r'^\s*"(.*)"\s*$',cmd)):
                cmd = re.sub(r'^\s*["\'](.*)["\']\s*$',r'\g<1>',cmd)
                print(cmd)
            cmd_list.append(cmd)


    elog('run config cmd: {}'.format(cmd_list), **kwargs)
    try:
        res = dh.config(command_list=cmd_list, **kwargs)
        output = res.response()
        if res.status() is True:
            if re.search(r'syntax error', output, re.I):
                t.log('warn', "config cmd return errors: {}".format(output))
                return False
            else:
                dh.log("config cmd run successfully")
            #input('check')
        else:
            dh.log('Toby HLDCL returns error:' + res.response())
            return False

    except Exception as err:
        msg = "config '{}' failed: {}".format(",".join(cmd_list), str(err))
        dh.log('warn', msg)
        return False

    elog('done with config commands as event')
    return True

def on_shell(dh, command, **kwargs):
    '''
    run_shell commands
    '''
    cmd_list = []
    if isinstance(command, str):
        command = command.split(',')
 
    if isinstance(command, list):
        for cmd in command:
            if(re.match(r'^\s*\'(.*)\'\s*$',cmd)):
                cmd = re.sub(r'^\s*["\'](.*)["\']\s*$',r'\g<1>',cmd)
                print(cmd)
            if(re.match(r'^\s*"(.*)"\s*$',cmd)):
                cmd = re.sub(r'^\s*["\'](.*)["\']\s*$',r'\g<1>',cmd)
                print(cmd)
            cmd_list.append(cmd)

    for cmd in cmd_list:
        #cmd = cmd.strip('\'\"')
        elog('run shell cmd: {}'.format(cmd), **kwargs)

        if isinstance(cmd, str) and cmd.endswith(')'):
            # either hldcl method or user added method if imported via hldcl handle
            cmd = cmd.strip(r'() ')

            if hasattr(dh, cmd):
                cmd_method = getattr(dh, cmd.strip(r'() '))
            else:
                raise Exception('cannot find method {} for the linux object'.format(cmd))
            try:
                cmd_method()
            except Exception as err:
                msg = " on Linux, this cmd '{}' failed: {}".format(cmd, str(err))
                dh.log('warn', msg)
                return False

        elif isinstance(cmd, str):
            # linux/unix shell commmand
            # only available exception from hldcl is timeout, need more (To do)
            try:
                dh.shell(command=cmd, **kwargs)
            except Exception as err:
                msg = " on Linux, this cmd '{}' failed in HLDCL: {}".format(cmd, str(err))
                dh.log('warn', msg)
                return False
        else:
            elog('warn', 'linux command format can only be a string or a list')
            return False

    elog('done with shell commands as event')
    return True

def on_vty(dh, command, ifd, **kwargs):
    '''
    run_shell commands
    '''
    cmd_list = []
    if isinstance(command, str):
        command = command.split(',')
 
    if isinstance(command, list):
        for cmd in command:
            if(re.match(r'^\s*\'(.*)\'\s*$',cmd)):
                cmd = re.sub(r'^\s*["\'](.*)["\']\s*$',r'\g<1>',cmd)
                print(cmd)
            if(re.match(r'^\s*"(.*)"\s*$',cmd)):
                cmd = re.sub(r'^\s*["\'](.*)["\']\s*$',r'\g<1>',cmd)
                print(cmd)
            cmd_list.append(cmd)

    vty_args = {}
    vty_args['destination'] = kwargs.get('destination', get_pfe(dh, ifd))
    vty_args['timeout'] = kwargs.get('timeout', None)
    vty_args['pattern'] = kwargs.get('pattern', None)
    vty_args['raw_output'] = kwargs.get('raw_output', None)

    for cmd in cmd_list:
        cmd = cmd.strip('\'\"')
        elog('run vty cmd: {}'.format(cmd), **kwargs)

        res = None
        if isinstance(cmd, str) and cmd.endswith(')'):
            # either hldcl method or user added method if imported via hldcl handle
            # Todo: handle args inside method(ar1, arg2,  )
            cmd = cmd.strip(r'() ')

            if hasattr(dh, cmd):
                cmd_method = getattr(dh, cmd.strip(r'() '))
            else:
                raise Exception('cannot find method {} for the linux object'.format(cmd))
            try:
                res = cmd_method()
            except Exception as err:
                msg = " on Linux, this cmd '{}' failed: {}".format(cmd, str(err))
                dh.log('warn', msg)
                return False

        elif isinstance(cmd, str):
            #
            # only available exception from hldcl is timeout, need more (To do)
            try:
                res = dh.vty(command=cmd, **vty_args)
            except Exception as err:
                msg = " on vty, this cmd '{}' failed in HLDCL: {}".format(cmd, str(err))
                dh.log('warn', msg)
                return False
        else:
            elog('warn', 'vty command format can only be a string or a list')
            return False

    elog('done with vty command')
    return True
    ## any checking? exception handling?

def on_clipfe(dh, command, **kwargs):
    '''
    run_clipfe commands (EVO only)
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    device_name = get_dh_name(dh)

    if dh.__dict__.get('device_info') is None:
        dh.device_info = {}

    if dh.device_info.get('isEvo'):
        t.log('debug', '{} = EVO'.format(device_name))
    elif dh.is_evo():
        dh.device_info['isEvo'] = True
    else:
        elog('warn', '{}: is not EVO'.format(device_name))
        return True

    if isinstance(command, str):
        cmd_list = [cmd.strip(' \'\"') for cmd in command.split(',')]
    else:  # assume it is a list. may need more checking
        #cmd_list = command
        cmd_list = [cmd.strip(' \'\"') for cmd in command]

    for cmd in cmd_list:
        cmd = cmd.strip('\'\"')
        elog('{}: run cli-pfe cmd: {}'.format(device_name, cmd), **kwargs)
        res = None
        if isinstance(cmd, str) and cmd.endswith(')'):
            # either hldcl method or user added method if imported via hldcl handle
            # Todo: handle args inside method(ar1, arg2,  )
            cmd = cmd.strip(r'() ')

            if hasattr(dh, cmd):
                cmd_method = getattr(dh, cmd.strip(r'() '))
            else:
                raise Exception('cannot find method {} for the linux object'.format(cmd))
            try:
                res = cmd_method()
            except Exception as err:
                msg = " on Linux, this cmd '{}' failed: {}".format(cmd, str(err))
                dh.log('warn', msg)
                return False

        elif isinstance(cmd, str):
            #
            # only available exception from hldcl is timeout, need more (To do)
            try:
                res = cli_pfe(dh, cmd)
            except Exception as err:
                msg = " on cli-pfe, this cmd '{}' failed in HLDCL: {}".format(cmd, str(err))
                dh.log('warn', msg)
                return False
        else:
            elog('warn', 'cli-pfe command format can only be a string or a list')
            return False

    elog('Done with cli-pfe command')
    return True
    ## any checking? exception handling?

def restart_process(dh, process, **kwargs):
    '''
    restart_process using JUNOS cli's 'restart xxx'
    - catch syntax error, or error output from cli.
    - switch to backup re if it is ksyncd,
    - catch HLDCL exception and return false, don't quit.
    - user can send additional arguments like restart_method ,node_name
    '''

    # Check if device is EVO and call EVO restart app
    restart_method = kwargs.get('restart_method', None)
    option_force_restart_process = kwargs.get('force_restart_process', False)
    dh.log(message="restart_process ...", level="info")


    if dh.__dict__.get('device_info') is None:
        dh.device_info = {}

    if dh.is_evo() and not option_force_restart_process:
        dh.device_info['isEvo'] = True
        # If restart method is kill, then call the EVO kill_app
        # Otherwise it is CLI based restart, so call restart_app
        if restart_method == 'kill':
            elog('== restart process calling kill_app ')
            return kill_app(dh, process, **kwargs)
        elog('== restart process calling restart_app ')
        ret = restart_app(dh, process, **kwargs)
        elog('== restart app from EVO returned: {}'.format(ret))
        return ret

    if restart_method == 'kill':
        kwargs['daemon'] = process
        elog('== restart process calling kill_daemon ')
        return kill_daemon(dh, **kwargs)

    option = kwargs.get('option')
    wait_after_restart = kwargs.get('wait_after_restart', 5)
    process = process.strip(' \'\"')
    
    if kwargs.get('option') is None:
        cmd = "restart {}".format(process)
    else:
        option = kwargs['option'].strip(' \'\"')
        cmd = "restart {} {}".format(process, option)

    # Checking for ksyncd process and switching the re to perform the restart process trigger.
    backup_re=False
    if process == 'kernel-replication':
        master_re = _check_master_re(dh)
        if master_re is True:
            return_value = dh.get_current_controller_name()
            if re.match(r're0', return_value):
                re_controller='re1'
            else:
                re_controller='re0'
        else:
            re_controller = dh.get_current_controller_name()

        backup_re = dh.set_current_controller(controller=re_controller, system_node='current')
        if backup_re is False:
            dh.log(message="Router has no dual-re set in params", level='warn')
            return True


    elog('== restart process: {}'.format(cmd), **kwargs)
    start_time = time.time()
    try:
        resp = ''
        resp = dh.cli(command=cmd).response()
           
        elog("resp is {} ..  ".format(resp))

        #check if the option mentioned is correct or else it will get into a infinite loop untill
        # it get time out if the option is wrong, continue the process in a default way
        if re.search(r'error', resp):
            elog('warn', 'Failed to execute this command {} on cli: {}'.format(\
                            cmd, resp))
            return False
        elog("waiting for {} seconds.. after restart".format(wait_after_restart))
        time.sleep(wait_after_restart)

    except Exception as err:
        elog("warn", "HLDCL failed for the restart {} event on cli: {}".format(\
                            cmd, err))
        return False

    time_spent = time.time() - start_time
    elog('{} restarted in {} seconds'.format(\
                process, time_spent))

    #To change back the handle to master , in ksyncd process
    if backup_re is True:
        if re.match('re1',re_controller):
            dh.set_current_controller(controller='re0', system_node='current')
        else:
            dh.set_current_controller(controller='re1', system_node='current')

    return True

def restart_processes(dh, process, **kwargs):
    '''
    restart 1 to N processes using JUNOS/EVO cli's 'restart xxx'
    - catch syntax error, or error output from cli.
    - switch to backup re if it is ksyncd,
    - catch HLDCL exception and return false, don't quit.
    '''
    p_list = process
    if isinstance(p_list, str):
        # if the app_list is comma separated, break it into a list
        p_list = [proc.strip() for proc in p_list.split(',')]

    for p in p_list:
        restart_process(dh, process=p, **kwargs)

    return True

def restart_app(dh, app, **kwargs):
    '''
    - Handles EVO app restarts
    - Can pass in a list of apps
    - Example:
        Run Event     Restart App    app=idmdbd,idmdcounter          device=${evo}
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    app_node = kwargs.get('node', 're0')
    reconnect_timeout = kwargs.get('reconnect_timeout', 600)
    reconnect_interval = kwargs.get('reconnect_interval', 30)
    wait_for_reboot = kwargs.get('wait_for_reboot', 120)
    wait = kwargs.get('wait', 5)

    device_name = get_dh_name(dh)

    if dh.__dict__.get('device_info') is None:
        dh.device_info = {}

    if dh.device_info.get('isEvo'):
        t.log('debug', '{} = EVO'.format(device_name))
    elif dh.is_evo():
        dh.device_info['isEvo'] = True
    else:
        elog('warn', '{}: is not EVO'.format(device_name))
        return True

    if dh.device_info.get('BYPASS_APP_CHECK'):
        dh.device_info.pop('BYPASS_APP_CHECK')

    app_list = app
    if isinstance(app_list, str):
        # if the app_list is comma separated, break it into a list
        app_list = [appl.strip() for appl in app_list.split(',')]

    total_num_apps = ''
    for count, apps in enumerate(app_list, 1):
        total_num_apps = count

    elog('{}: Restarting EVO app(s): {}'.format(device_name, nice_string(app_list)))
    for x, appx in enumerate(app_list, 1):
        try:
            output1 = dh.cli(command='show system applications app {} detail | match PID' \
                             .format(appx)).response()
            match1 = re.match(r'Main\s+PID\s+:\s+(\d+)', output1)
            app_pid1 = -1
            app_pid2 = -1
            if match1 is not None:
                app_pid1 = match1.group(1)
                elog('Prior to restart : {} pid is {} '.format(appx, app_pid1))
            dh.cli(command='request system application app {} node {} restart'\
               .format(appx, app_node), pattern='yes')
            res = dh.cli(command='yes')

        except Exception:
            elog('warn', '** received toby exception from CLI')
            kwargs['force_restart_process'] = True
            return restart_process(dh, app, **kwargs)


        if re.search(r'system\s+is\s+going\s+down\s+for\s+reboot', res.response()):
            elog('warn', '** {}: EVO app: ({}) caused device to reboot **'\
                 .format(device_name, appx))
            elog('** trying to reconnect to {} within in {} seconds.**'\
                 .format(device_name, reconnect_timeout))
            time.sleep(wait_for_reboot)
            reconnect_to_device(device=dh, interval=reconnect_interval, timeout=reconnect_timeout)
            elog('{}: reconnect to device successful.'.format(device_name, apps))
            dh.device_info['BYPASS_APP_CHECK'] = True
            return False
        elif not re.search(r'restart\s+request\s+is\s+submitted', res.response()):
            elog('warn', '** {}: EVO app: ({}) may not have been restarted **'\
                 .format(device_name, appx))
        elif re.search(r'syntax\serror', res.response()):
            elog('warn','** syntax Error is seen')
        else:
            elog('** {}: EVO app: ({}) restarted **'.format(device_name, appx))
        if (total_num_apps > 1 and total_num_apps != x):
            elog('Wait {} seconds to restart next EVO app'.format(wait))
            time.sleep(wait)
        elog('wait_for_reboot: {} '.format(wait_for_reboot))
        time.sleep(wait_for_reboot)
        output2 = dh.cli(command='show system applications app {} detail | match PID' \
                         .format(appx)).response()
        match2 = re.match(r'Main\s+PID\s+:\s+(\d+)', output2)
        if match2 is not None:
            app_pid2 = match2.group(1)
            elog('After restart : {} pid is {}'.format(appx, app_pid2))
        if app_pid1 != -1 and app_pid2 != -1:
            if app_pid1 == app_pid2:
                elog('Pid did not change after restart ')
                return False
            else:
                elog('Pids differ after restart of app {}: PID prior to restart:{}, PID after restart{}'.format(appx,app_pid1,app_pid2))
                return True

    return True

def check_evo_app(dh, app, **kwargs):
    '''
    - Check evo app via cli
        - pass in enable_check=True
    - Can pass in a list of apps
    - Example:
        Run Event  Restart App   app=idmdbd,idmdcounter
        ...     device=${evo}   enable_check=True
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    app_node = kwargs.get('node', 're0')
    reconnect_timeout = kwargs.get('reconnect_timeout', 600)
    reconnect_interval = kwargs.get('reconnect_interval', 30)
    wait_for_reboot = kwargs.get('wait_for_reboot', 10)

    device_name = get_dh_name(dh)

    if dh.__dict__.get('device_info') is None:
        dh.device_info = {}

    if dh.device_info.get('BYPASS_APP_CHECK'):
        t.log('Bypass app checking.')
        return True

    if dh.device_info.get('isEvo'):
        t.log('debug', '{} = EVO'.format(device_name))
    elif dh.is_evo():
        dh.device_info['isEvo'] = True
    else:
        elog('warn', '{}: is not EVO'.format(device_name))
        return True

    app_list = app
    if isinstance(app_list, str):
        # if the app_list is comma separated, break it into a list
        app_list = [appl.strip() for appl in app_list.split(',')]

    for count, apps in enumerate(app_list, 1):
        total_num_apps = count

    total_ready = ''

    for x, apps in enumerate(app_list, 1):
        try:
            res = dh.cli(command='show system applications node {} app {}'.format(app_node, apps))
        except:
            elog('{}:{} Device may have rebooted. Trying to reconnect to device. Please wait....'\
                .format(device_name, apps))
            reconnect_to_device(device=dh, interval=reconnect_interval, timeout=reconnect_timeout)
            return False
        output = res.response()
        if re.search(r'App\s+State\s+:\s+online\s+ready', output):
            elog('{}: EVO app ({}) is online/ready'.format(device_name, apps))
            total_ready = x
        elif re.search(r'App\s+State\s+:\s+offline\s+failed', output):
            elog('warn', '{}: EVO app ({}) is offline failed. App not supported for restart/kill'\
                 .format(device_name, apps))
            elog('{}: EVO app ({}) may cause device reboot. Lets wait and see if reboot happens.'\
                 .format(device_name, apps))
            time.sleep(wait_for_reboot)
            elog('{}:{} Trying to reconnect to device. Please wait....'.format(device_name, apps))
            reconnect_to_device(device=dh, interval=reconnect_interval, timeout=reconnect_timeout)
            elog('{}:{} reconnect to device successful.'.format(device_name, apps))
            return False
        elif re.search(r'App\s+State\s+:\s+offline', output):
            elog('{}: EVO app ({}) is offline'.format(device_name, apps))
        else:
            elog('{}: EVO app: {} not ready'.format(device_name, apps))

    if total_num_apps == total_ready:
        return True

def kill_app(dh, app, **kwargs):
    '''
    - Handles kill EVO app
    - Can pass in a list of apps
    - Example:
        Run Event     Kill App    app=idmdbd,idmdcounter          device=${evo}
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())
    wait_for_reboot = kwargs.get('wait_for_reboot', 120)

    wait = kwargs.get('wait', 5)
    device_name = get_dh_name(dh)

    if dh.__dict__.get('device_info') is None:
        dh.device_info = {}

    if dh.device_info.get('isEvo'):
        t.log('debug', '{} = EVO'.format(device_name))
    elif dh.is_evo():
        dh.device_info['isEvo'] = True
    else:
        elog('warn', '{}: is not EVO'.format(device_name))
        return True

    if dh.device_info.get('BYPASS_APP_CHECK'):
        dh.device_info.pop('BYPASS_APP_CHECK')

    app_list = app

    if isinstance(app_list, str):
        # if the app_list is comma separated, break it into a list
        app_list = [appl.strip() for appl in app_list.split(',')]

    total_num_apps = ''
    for count, apps in enumerate(app_list, 1):
        total_num_apps = count

    app_pids = []
    for appx in app_list:
        output = dh.cli(command='show system applications app {} detail | match PID'\
                            .format(appx)).response()
        match = re.match(r'Main\s+PID\s+:\s+(\d+)', output)
        if match is not None:
            app_pid = match.group(1)
            app_pids.append(appx+':'+app_pid)

    elog('{}: Kill EVO app:process(s): {}'.format(device_name, nice_string(app_pids)))
    dh.su()
    for x, mpid in enumerate(app_pids, 1):
        match = re.match(r'(\D+):(\d+)', mpid)
        app_pid = None
        app_pid2 = None
        if match:
            app_name = match.group(1)
            app_pid = match.group(2)
        res = dh.shell(command='kill -9 {}'.format(app_pid))
        elog('** {}: EVO app ({}) pid: ({}) was killed **'.format(device_name, app_name, app_pid))
        time.sleep(wait_for_reboot)
        output2 = dh.cli(command='show system applications app {} detail | match PID' \
                        .format(app_name)).response()
        match2 = re.match(r'Main\s+PID\s+:\s+(\d+)', output2)
        if match2 is not None:
            app_pid2 = match2.group(1)
        if app_pid2 != app_pid:
            elog('Kill EVO app:process(s) successful with new PID {}'.format(app_pid2))
        else:
            elog('Kill EVO app:process(s) unsuccessful...new pid is not generated')
            return False

        if (total_num_apps > 1 and total_num_apps != x):
            elog('Wait {} seconds to kill next EVO pid/app/process'.format(wait))
            time.sleep(wait)

    return True
