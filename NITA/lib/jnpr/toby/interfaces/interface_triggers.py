"""
Copyright (C) 2015-2016, Juniper Networks, Inc.
All rights reserved.
Authors:
    jpzhao, bphillips
Description:
    Toby Interface Trigger Library.
    many triggers are converted from JT libraries, original authors are noted in each such trigger.

Usage:
    Run Event  Flap Interface
"""
# pylint: disable=locally-disabled,undefined-variable,invalid-name,multiple-statements
import re
import copy
import time
import random
import math
from pprint import pprint
import jnpr.toby.engines.config.config_utils as config_utils
from jnpr.toby.engines.events.event_engine_utils import get_pfe, elog, func_name, get_dh_tag, get_dh_name, get_vty_pfe_for_line_card_mode
from jnpr.toby.engines.events.event_engine_utils import interface_handler_to_ifd, nice_string, cli_pfe, strip_xml_namespace

#### REGEX ####
FPC_REGEX_ONLINE = r'\s+(\d+)\s+Online'
FPC_REGEX_OFFLINE = r'\s+(\d+)\s+Offline'
PIC_REGEX_ONLINE = r'\s+State\s+Online'
PIC_REGEX_OFFLINE = r'\s+State\s+Offline'

###############################################################
# register all ifd trigger methods here
###############################################################
def _get_ifd_func_list(method, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    ifd_functions = {
        'ifd_cfg_enable_disable': {
            'state_action': {'up': 'enable', 'down': 'disable'},
            'trigger': _ifd_cfg_enable_disable,   # mandatory
            'check': _check_ifd_cfg_enable_disable,
        },
        'ifd_cfg_set_delete': {
            'state_action': {'up': 'set', 'down': 'delete'},
            'trigger': _ifd_cfg_set_delete,   # mandatory
        },
        'ifd_cfg_activate_deactivate': {
            'state_action': {'up': 'activate', 'down': 'deactivate'},
            'trigger': _ifd_cfg_activate_deactivate,   # mandatory
            'check': _check_ifd_cfg_activate_deactivate,
        },
        'ifd_shell_up_down': {
            'state_action': {'up': 'up', 'down': 'down'},
            'trigger': _ifd_shell_up_down,   # mandatory
            'check': _check_ifd_shell_up_down,
        },
        'ifd_laser_on_off': {
            'state_action': {'up': 'on', 'down': 'off'},
            'trigger': _ifd_laser_on_off,   # mandatory
            'check': _check_ifd_laser_on_off,
            'bounce': _ifd_laser_bounce,
        },
        'ae_cfg_enable_disable': {
            'state_action': {'up': 'enable', 'down': 'disable'},
            'trigger': _ae_cfg_enable_disable,   # mandatory
            'check': _check_ae_cfg_enable_disable,
        },
        'ae_member_link_cfg_enable_disable': {
            'state_action': {'up': 'enable', 'down': 'disable'},
            'trigger': _ae_member_link_cfg_enable_disable,   # mandatory
            'check': _check_ae_member_link_cfg_enable_disable,
        },
        'ae_cfg_set_delete': {
            'state_action': {'up': 'set', 'down': 'delete'},
            'trigger': _ae_cfg_set_delete,   # mandatory
        },
        'ae_member_link_cfg_set_delete': {
            'state_action': {'up': 'set', 'down': 'delete'},
            'trigger': _ae_member_link_cfg_set_delete,   # mandatory
        },
        'ae_cfg_activate_deactivate': {
            'state_action': {'up': 'activate', 'down': 'deactivate'},
            'trigger': _ae_cfg_activate_deactivate,   # mandatory
            'check': _check_ae_cfg_activate_deactivate,
        },
        'ae_member_link_cfg_activate_deactivate': {
            'state_action': {'up': 'activate', 'down': 'deactivate'},
            'trigger': _ae_member_link_cfg_activate_deactivate,   # mandatory
            'check': _check_ae_member_link_cfg_activate_deactivate,
        },
        'ae_shell_up_down': {
            'state_action': {'up': 'up', 'down': 'down'},
            'trigger': _ae_shell_up_down,   # mandatory
            'check': _check_ae_shell_up_down,
        },
        'ae_member_link_shell_up_down': {
            'state_action': {'up': 'up', 'down': 'down'},
            'trigger': _ae_member_link_shell_up_down,   # mandatory
            'check': _check_ae_member_link_shell_up_down,
        },
        'ae_member_link_laser_on_off': {
            'state_action': {'up': 'on', 'down': 'off'},
            'trigger': _ae_member_link_laser_on_off,   # mandatory
            'check': _ae_check_ifd_laser_on_off,
        },
        'fpc_restart': {
            'state_action': {'down': 'restart'},
            'trigger': _fpc_restart,   # mandatory
            'fru_check': _check_fpc_restart, #FRU level check
        },
        'fpc_on_off': {
            'state_action': {'up': 'online', 'down': 'offline'},
            'trigger': _fpc_on_off,   # mandatory
            'fru_check': _check_fpc_on_off, #FRU level check
        },
        'ae_member_link_fpc_restart': {
            'state_action': {'down': 'restart'},
            'trigger': _ae_member_link_fpc_restart,   # mandatory
            'fru_check': _check_ae_member_link_fpc_restart, #FRU level check
        },
        'pic_on_off': {
            'state_action': {'up': 'online', 'down': 'offline'},
            'trigger': _pic_on_off,   # mandatory
            'fru_check': _check_pic_on_off,
        },
        'mic_on_off': {
            'state_action': {'up': 'online', 'down': 'offline'},
            'trigger': _mic_on_off,   # mandatory
            'fru_check': _check_mic_on_off,
        },
    }

    if ifd_functions.get(method):
        return ifd_functions[method]
    elif 'no_method' in method:
        t.log('error', 'Method not defined, you need to define a method')
        return None
    else:
        t.log('error', 'Cannot find link flap method: {}'.format(method))
        return None


# interface link flapping methods
def flap_interface(dh, interface, action='flap', method='no_method', **kwargs):
    """
    default action is 'flap', as the name implies.
    can set it to 'up/down', or activate/deactivate,...
    """

    t.log('debug', func_name())

    kwargs['ifd_list'] = []
    ifd_list = interface_handler_to_ifd(device=get_dh_tag(dh), \
                                           interface=interface)
    kwargs['ifd_list'] = ifd_list

    if method.endswith('fpc_restart'):
        if not 'panic' in action:
            action = 'restart'

    elog('==== Flap interface: {}({} / {}) interface(s): {} action: {} method: {}'\
         .format(get_dh_tag(dh), get_dh_name(dh), dh.get_model(), nice_string(ifd_list), action, method))

    if dh.__dict__.get('if_info') is None:
        dh.if_info = {}

    if dh.__dict__.get('if_config') is None:
        dh.if_config = {}

    if dh.__dict__.get('fru_info') is None:
        dh.fru_info = {}

    if dh.__dict__.get('device_info') is None:
        dh.device_info = {}

    if dh.device_info.get('isNotEvo'):
        t.log('debug', '1: {}: is not EVO'.format(get_dh_name(dh)))
    else:
        if dh.device_info.get('isEvo'):
            t.log('debug', '1: {} = EVO'.format(get_dh_name(dh)))
        elif dh.is_evo():
            t.log('debug', '2: {} = EVO'.format(get_dh_name(dh)))
            dh.device_info['isEvo'] = True
        else:
            dh.device_info['isNotEvo'] = True
            t.log('debug', '2: {}: is not EVO'.format(get_dh_name(dh)))

    kwargs['initial_action'] = action

    kwargs['member_ifd_list'] = []
    for ifd in ifd_list:
        #AE link processing
        is_ae = False
        if (isinstance(nice_string(ifd), str)):
            if (nice_string(ifd).startswith('ae')):
                is_ae = True
        elif ifd.startswith('ae'):
            is_ae = True

        if is_ae:
            if method.startswith(('ae_cfg', 'ae_shell')):
                # get all the functions related to this trigger
                func_list = _get_ifd_func_list(method, **kwargs)
                dh.log(message='take action: {} | ae bundle: {}'.format(action, ifd))
            else:
                if not method.startswith('ae_member'):
                    elog('error', '== Must use a method beginning with ae_member_<foo>')
                    return False

                member_link_pick_toggle = kwargs.get('member_link_pick', "reuse")

                if kwargs.get('member_link_percentage'):
                    pick_links_value = 'mlp_{}_pick_links'.format(kwargs['member_link_percentage'])
                elif kwargs.get('num_of_member_links'):
                    pick_links_value = 'nml_{}_pick_links'.format(kwargs['num_of_member_links'])
                elif kwargs.get('member_link_list'):
                    pick_links_value = 'mll_{}_pick_links'.format(ifd)
                else:
                    pick_links_value = 'minlink_{}_pick_links'.format(ifd)

                # now check if the ae link has enough 'up' member links to flap
                if kwargs.get('event_iteration', 1) == 1:
                    # do this only for the begining of iteration
                    if kwargs.get('debug_log_on'):
                        t.log('debug', 'AE: dumping the dh.if_info dictionary keys/values')
                        pprint(dh.if_info)

                    if ('refresh' in member_link_pick_toggle and dh.if_info.get('ae') and dh.if_info['ae'].get(ifd)):
                        pick_links = _pick_ae_member_links(dh, ifd, **kwargs)
                        config_utils.nested_set(dh.if_info['ae'], [ifd, pick_links_value], pick_links)
                        pick_links_status = 'refresh'
                    elif ('reuse' in member_link_pick_toggle and dh.if_info.get('ae') and dh.if_info['ae'].get(ifd)):
                        if dh.if_info['ae'][ifd].get(pick_links_value):
                            pick_links_status = 'cached'
                        elif not dh.if_info['ae'][ifd].get(pick_links_value):
                            pick_links = _pick_ae_member_links(dh, ifd, **kwargs)
                            config_utils.nested_set(dh.if_info['ae'], [ifd, pick_links_value], pick_links)
                            pick_links_status = 'append'
                    elif not (dh.if_info.get('ae') and dh.if_info['ae'].get(ifd)):
                        pick_links = _pick_ae_member_links(dh, ifd, **kwargs)
                        config_utils.nested_set(dh.if_info['ae'], [ifd, pick_links_value], pick_links)
                        pick_links_status = 'initial'
                    else:
                        elog('error', '==: Cannot find {0}'.format(ifd))
                        return False

                if kwargs.get('debug_log_on'):
                    t.log('debug', 'AE 2: dumping the dh.if_info dictionary keys/values')
                    pprint(dh.if_info)

                if dh.if_info['ae'][ifd][pick_links_value]:
                    elog('{}: {}, flap these member links: {}'.format(pick_links_status, ifd, \
                                    nice_string(dh.if_info['ae'][ifd][pick_links_value])))
                    kwargs['member_ifd_list'].extend(dh.if_info['ae'][ifd][pick_links_value])
                else:
                    elog('warn', 'For {}, no links can be used to flap'.format(ifd))
                    return False

    # get all the functions related to this trigger
    func_list = _get_ifd_func_list(method, **kwargs)
    ret = True
    if re.match(r'flap', action, re.I):
        interval = kwargs.get('interval', 3)  # unit second.  0.01 also works( msec)

        # execute
        act_up = func_list['state_action']['up']
        act_down = func_list['state_action']['down']
        #look for function first
        if func_list.get('bounce'):
            func_list['bounce'](dh, ifd_list, **kwargs)    ### BOUNCE
        else:
            #Capture the return value and return False if it receives False so that Toby users can handle
            ret2 = func_list['trigger'](dh, ifd_list, action=act_down, **kwargs)
            if ret2 is False:
                return ret2
            ret = _confirm_ifd_state(dh, ifd_list, act_down, method, **kwargs)
            time.sleep(float(interval))
            func_list['trigger'](dh, ifd_list, action=act_up, **kwargs)

        ret = _confirm_ifd_state(dh, ifd_list, act_up, method, **kwargs)
    else:
        #call the function directly (up/down, on/off etc)
        func_list['trigger'](dh, ifd_list, action, **kwargs)
        # confirm the event state is set:
        ret = _confirm_ifd_state(dh, ifd_list, action, method, **kwargs)

    # return True/false or raise exception when failed??
    return ret


def _get_ae_info(dh, **kwargs):
    '''
    get ae and member link details from a dut
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())
    # get all ae links all together
    # this will get all ae's set by chassis/aggregated-devices/../device-count,
    # no matter you configured it or not
    # optional:
    # regress@foo# show interfaces  | match "^ae[0-9]+ {"
    # will get only the ones that are configured ( then, what if disabled/deactivated)
    if dh.__dict__.get('if_info') is None:
        dh.if_info = {}
    if dh.if_info.get('ae'):
        if kwargs.get('debug_log_on'):
            t.log('debug', 'ae info already gathered')
        return True

    #find all ae links
    if not dh.if_info.get('ae'):
        # adding sleep so AE links to come up
        time.sleep(1)
        res = dh.cli(command='show interfaces terse media | match ae').response()
        if re.search(r'ae\d+', res) is None:
            t.log('error', '(AE bundle) or (chassis aggregated-devices ethernet \
                            device-count) not configured.')
        else:
            for ae_line in res.split('\n'):
                match = re.match(r'(ae\d+)\s+', ae_line)
                if match is not None:
                    ae = match.group(1)
                    cmd = 'show interfaces terse | match "{0}\.[0-9]+" | except "^{0}"'.format(ae)
                    res = dh.cli(command=cmd).response().strip().split('\n')
                    memlinks = {'down':[], 'up':[]}
                    for line in res:
                        mat = re.match(r'(\S+)\.\d+\s+((up|down)\s+(up|down))', line)
                        if mat is not None:
                            if re.search(r'down', mat.group(2)):
                                if mat.group(1) not in memlinks['down']:
                                    memlinks['down'].append(mat.group(1))
                            elif mat.group(1) not in memlinks['up']:
                                memlinks['up'].append(mat.group(1))
                    if memlinks['up'] or memlinks['down']:
                        config_utils.nested_set(dh.if_info, ['ae', ae, 'member_links'], \
                                                    memlinks, append=True)
                        # find min-links
                        minlink = _get_ae_min_links(dh, ae)
                        if isinstance(minlink, int):
                            config_utils.nested_set(dh.if_info, ['ae', ae, 'minimum_links'], \
                                                        minlink)


def _get_ae_min_links(dh, ae, **kwargs):

    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    cmd = 'show interfaces {} media | display xml | match minimum-links-in-aggregate'.format(ae)
    res = dh.cli(command=cmd).response().strip()
    minlink = re.sub(r'\D+', '', res)
    if re.match(r'\d+', minlink):
        minlink = int(minlink)
    return minlink


def _pick_ae_member_links(dh, ae, **kwargs):
    '''
    determine the member links to be flapped
        - default
        - with a given list of 'member_links'
        - with percentage
        - random is default.
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    if not dh.if_info.get('ae') or kwargs.get('refresh_ae_data'):
        _get_ae_info(dh, **kwargs)
    if not dh.if_info['ae'].get(ae):
        t.log('warn', 'cannot find interface: {}'.format(ae))
        return False

    up_links = []
    if kwargs.get('member_link_list'):
        # replace params tags with the ifd names
        mlink_list = kwargs.get('member_link_list')
        if isinstance(mlink_list, str):
            # if the device_list is comma separated, break it into a list
            mlink_list = [link.strip() for link in mlink_list.split(',')]
        for mlink in mlink_list:
            ifd = interface_handler_to_ifd(device=dh.tag, interface=mlink)
            if ifd is not None:
                up_links.append(ifd)
            elif ifd is None:
                raise KeyError('wrong or missing interface tag {} on device {}'.\
                                format(mlink, dh.tag))
        #then ??
        return up_links


    # now check for this ae:
    # first, pick member links
    ae_attr = copy.deepcopy(dh.if_info['ae'][ae])
    up_links = ae_attr['member_links']['up']
    num_links_to_flap = len(up_links) - ae_attr['minimum_links'] + 1
    # if percentage or num_links args defined
    if kwargs.get('num_of_member_links'):
        num_links_to_flap = int(kwargs.get('num_of_member_links'))
    elif kwargs.get('member_link_percentage'):
        num_links_to_flap = (len(up_links) + len(ae_attr['member_links']['down']))\
                            * (float(kwargs['member_link_percentage'])/100.00)
        num_links_to_flap -= len(ae_attr['member_links']['down'])
        num_links_to_flap = math.ceil(num_links_to_flap)  # at least one

    if num_links_to_flap < 1:
        t.log('warn', 'member links are already less than minimum links')
        #input()
        return False   ## TBD


    links_to_flap = random.sample(up_links, num_links_to_flap)
    return links_to_flap


def _confirm_ifd_state(dh, ifd, action, method, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    ## This will disable all ifd or fpc based checking form user input from robot
    if kwargs.get('disable_checking'):
        dh.log(message='====Confirm (Event) state checking is disabled')
        return True

    # get all the functions related to this trigger
    func_list = _get_ifd_func_list(method, **kwargs)
    st_check = True

    if func_list.get('check'):
        if isinstance(ifd, str):
            ifd = [ifd]
        for num, ifname in enumerate(ifd, 1):
            total = num
        for ifname in ifd:
            if dh.if_info.get('BYPASS_INTF_CHECK_{}'.format(ifname)):
                if total > 1:
                    ifd.remove(ifname)
                else:
                    return True

        t.log('debug', 'Checking IFD(s): {}'.format(nice_string(ifd)))
        # time in float means it can take millisecond
        timeout = float(kwargs.get('timeout', 60))
        check_interval = float(kwargs.get('check_interval', 5))
        start = time.time()
        while time.time() - start < timeout:
            if func_list['check'](dh, ifd, action, **kwargs):
                duration = time.time() - start
                st_check = duration
                dh.log(message='===={}: takes {} for {} on {}'.format(func_name(), \
                                duration, method, nice_string(ifd)))
                elog('== run event state: {} - confirmed'.format(action), **kwargs)
                break
            time.sleep(check_interval)
        else:
            elog('warn', '== {}: IFD not in expected state | method: {} | ifd: {}'.\
                format(dh.name, method, nice_string(ifd)))
            st_check = False

    elif func_list.get('fru_check'):
        if dh.fru_info.get('BYPASS_FRU_CHECK'):
            return True

        # time in float means it can take millisecond
        timeout = float(kwargs.get('timeout', 360))
        check_interval = float(kwargs.get('check_interval', 10))
        start = time.time()
        while time.time() - start < timeout:
            if func_list['fru_check'](dh, ifd, action, **kwargs):
                duration = time.time() - start
                st_check = duration
                dh.log(message='===={}: takes {} on {}'.format(func_name(), duration, ifd))
                elog('== run event state: {} - confirmed'.format(action), **kwargs)
                break
            time.sleep(check_interval)
        else:
            elog('error', '== {}: FRU not online for interface: {}'.format(dh.name, ifd))
            st_check = False
    else:
        t.log('debug', 'No check function for {}, skip'.format(method))
        st_check = True
    return st_check


def _ae_cfg_enable_disable(dh, ae, action='enable', **kwargs):
    """
    set interfaces ae0 disable ; delete interfaces ae0 enable
    Can also handle multiple ae bundles.
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    cmds = []

    ae_list = ae
    if isinstance(ae, str):
        ae_list = [ae.strip() for ae in ae.split(',')]
    for aename in ae_list:
        if re.match(r'enable|up|on', action, re.I):
            cmds.append('delete interfaces {} disable'.format(aename))
        elif re.match(r'disable|down|off', action, re.I):
            cmds.append('set interfaces {} disable'.format(aename))
        else:
            t.log('error', '{} :Unknown action'.format(func_name()))

    if kwargs.get('no_commit'):
        dh.config(command_list=cmds)
    else:
        cmds.append('commit')
        dh.config(command_list=cmds)


def _check_ae_cfg_enable_disable(dh, ae, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    all_aes = []
    cmd_response = []
    num_conf = ''
    num_act_down = ''

    ae_list = ae
    if isinstance(ae, str):
        ae_list = [ae.strip() for ae in ae.split(',')]
    for aename in ae_list:
        all_aes.append(aename)
        ae_list = list(set(all_aes))

    elog('== Check AE enable/disable for: {}'.format(nice_string(ae_list)))

    # Run all show cmds and append all laser responses of (on|up)
    for x, ifname in enumerate(ae_list, 1):
        res = dh.config(command_list=['show interfaces {} disable'.format(ifname)])
        cmd_response.append(res.response())
        num_conf = x

    # Loop thru all responses and determine if AE(s) are
    # on|up|enable or off|down|enabled state
    state = 'enable|enabled|on'
    for x, line in enumerate(cmd_response, 1):
        if re.match('disable', line):
            num_act_down = x
            if num_conf == num_act_down:
                elog('== ae: {} disabled'.format(nice_string(ae_list)), **kwargs)
                state = 'disable|disabled|off'

    if action is None:
        return state
    else:
        # compare with expected state:
        if re.match(state, action, re.I):
            return True
        else:
            return False


def _ifd_cfg_enable_disable(dh, ifd, action='enable', **kwargs):
    """
    set interfaces xe-0/0/0 disable ; delete interfaces xe-0/0/0 disable
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    cmds = []

    if isinstance(ifd, str):
        ifd = [ifd]
    new_ifd_list = []
    for ifname in ifd:
        if not isinstance(ifname, str):
            new_ifd_list.extend(ifname)
        else:
            new_ifd_list.append(ifname)

    for ifname in new_ifd_list:
        if re.match(r'enable|up|on', action, re.I):
            cmds.append('delete interfaces {} disable'.format(ifname))
        elif re.match(r'disable|down|off', action, re.I):
            cmds.append('set interfaces {} disable'.format(ifname))
        else:
            t.log('error', '{} :Unknown action'.format(func_name()))

    if kwargs.get('no_commit'):
        #config().config_engine(device_list=dh, cmd_list=cmds)
        dh.config(command_list=cmds)
    else:
        #config().config_engine(device_list=dh, cmd_list=cmds, commit=1)
        cmds.append('commit')
        dh.config(command_list=cmds)


def _check_ifd_cfg_enable_disable(dh, ifd, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    all_ifds = []
    cmd_response = []
    num_act = ''
    num_act_down = ''

    # find the current state first
    if isinstance(ifd, str):
        ifd = [ifd]
    new_ifd_list = []
    for ifname in ifd:
        if not isinstance(ifname, str):
            new_ifd_list.extend(ifname)
        else:
            new_ifd_list.append(ifname)
    for ifname in new_ifd_list:
        all_ifds.append(ifname)
        ifd_list = list(set(all_ifds))
    elog('== Check IFD enable/disable for: {}'.format(nice_string(ifd_list)))

    # Run all show cmds and append all laser responses of (on|up)
    for x, ifname in enumerate(ifd_list, 1):
        res = dh.config(command_list=['show interfaces {} disable'.format(ifname)])
        cmd_response.append(res.response())
        num_act = x

    # Loop thru all responses and determine if ifds are
    # on|up|enable or off|down|enabled state
    state = 'enable|enabled|on'
    for x, line in enumerate(cmd_response, 1):
        if re.match('disable', line):
            num_act_down = x
            if num_act == num_act_down:
                #elog('== ifd: {} are disabled'.format(nice_string(ifd_list)), **kwargs)
                state = 'disable|disabled|off'

    if action is None:
        return state
    else:
        # compare with expected state:
        if re.match(state, action, re.I):
            return True
        else:
            return False


def _ae_member_link_cfg_enable_disable(dh, ifd, action='enable', **kwargs):
    """
    set interfaces xe-0/0/0 disable ; delete interfaces xe-0/0/0 disable
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name() + ' on {}'.format(ifd))

    ifd_list = kwargs.get('member_ifd_list')

    return _ifd_cfg_enable_disable(dh, ifd_list, action=action, **kwargs)


def _check_ae_member_link_cfg_enable_disable(dh, ifd, action='enable', **kwargs):
    """
    set interfaces xe-0/0/0 disable ; delete interfaces xe-0/0/0 disable
    """
    ifd_list = kwargs.get('member_ifd_list')

    if kwargs.get('debug_log_on'):
        t.log('debug', func_name() + ' on {}'.format(ifd_list))

    return _check_ifd_cfg_enable_disable(dh, ifd_list, action=action, **kwargs)


def _ifd_cfg_set_delete(dh, ifd, action, **kwargs):
    """
    Loop thru multiple IFD's:
        - delete interfaces xe-0/0/0; set interfaces xe-0/0/0 <config> (from cache)
        or
        - delete interfaces xe-0/0/0; set interfaces xe-0/0/0 <config> (from config_egine)
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        if not dh.if_config.get('{}_{}'.format(dh.tag, ifname)):
            response = dh.cli(command='show configuration interfaces {} | display set'.\
                                format(ifname)).response()
            dh.if_config['{}_{}'.format(dh.tag, ifname)] = response

    # Loop thru all IFD to check if stored IFD level config,
    # then use the combined config from the dict
    # and take action to re-instate the config
    if re.match(r'set|up|on', action, re.I):
        set_cmds = []
        for ifname in ifd:
            if dh.if_config.get('{}_{}'.format(dh.tag, ifname)):
                ifd_set_cmds = dh.if_config['{}_{}'.format(dh.tag, ifname)]
                set_cmds.append(ifd_set_cmds)
            else:
                dh.log('{}: no dict/key ifd config found'.format(func_name()), level='error')

        if kwargs.get('no_commit'):
            dh.config(command_list=set_cmds)
        else:
            set_cmds.append('commit')
            dh.config(command_list=set_cmds)

    elif re.match(r'delete|down|off', action, re.I):
        del_cmds = []
        for ifname in ifd:
            if dh.if_config.get('{}_{}'.format(dh.tag, ifname)):
                del_cmds.append('delete interfaces {}'.format(ifname))
            else:
                dh.log('{}: no dict/key ifd config found before deleting {} config'.\
                        format(func_name(), ifname), level='error')

        if kwargs.get('no_commit'):
            dh.config(command_list=del_cmds)
        else:
            del_cmds.append('commit')
            ### If all mbr links are deleted, dut gives response below
            ### and will not commit.
            res = dh.config(command_list=del_cmds).response()
            if re.search('lesser than the required minimum', res):
                elog('error', 'cannot delete all ifds from AE bundle due to falling below' +
                                'min-links, \nplease specify arg: member_link_percentage or' +
                                'member_link_list or num_of_member_links')
                return False
    else:
        t.log('error', '{} :Unknown action. use action=flap / set|up|on or delete|down|off'.\
                        format(func_name()))

    # for ifname in ifd:
    #     if dh.if_config.get('{}_{}'.format(dh.tag, ifname)):
    #         t.log('debug', 'cleaning dict: {}_{}'.format(dh.tag, ifname))
    #         dh.if_config.pop('{}_{}'.format(dh.tag, ifname))


def _ae_member_link_cfg_set_delete(dh, ae, action='set', **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name() + ' on {}'.format(ae))

    ifd_list = kwargs.get('member_ifd_list')

    return _ifd_cfg_set_delete(dh, ifd_list, action=action, **kwargs)


def _option2_ifd_cfg_set_delete(dh, ifd, action, **kwargs):
    """
     delete interfaces xe-0/0/0; set interfaces xe-0/0/0
     optional user inputs: set_cmd/delete_cmd
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    set_ifd_key = 'set_{}'.format(ifd)
    set_cmd = kwargs['set_cmd'] if kwargs.get('set_cmd') else dh.if_info.get(set_ifd_key, [])
    if isinstance(set_cmd, str):
        set_cmd = set_cmd.split(',').strip()
    delete_cmd = kwargs.get('delete_cmd', 'delete interfaces ' + ifd)

    if re.match(r'set|up|on', action, re.I):
        if not set_cmd:
            show_cfg = 'show configuration interfaces {} | display set'.format(ifd)
            set_cmd = [cmd.strip() for cmd in \
                        dh.cli(command=show_cfg).response().strip().split('\n')]
            dh.if_info[set_ifd_key] = set_cmd
        config().config_engine(device_list=dh, cmd_list=set_cmd, commit=True)
    elif re.match(r'delete|down|off', action, re.I):
        #dh.config(command_list=['delete interfaces ' + ifd, 'commit'])
        config().config_engine(device_list=dh, cmd_list=delete_cmd, commit=True)
    else:
        t.log('error', '{} :Unknown action'.format(func_name()))


def _ae_cfg_set_delete(dh, ae, action='set', **kwargs):
    """
     delete interfaces ae5; set interfaces ae5(from cached)
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())
    ae_config = {}
    ae_list = ae
    if isinstance(ae, str):
        ae_list = [ae.strip() for ae in ae.split(',')]
    for ae in ae_list:
        if not (dh.if_info.get('ae_config') and \
                dh.if_info['ae_config'].get('{}_{}'.format(dh.tag, ae))):
            ae_config['{}_{}'.format(dh.tag, ae)] = \
                dh.cli(command='show configuration interfaces {} | display set'.format(ae)).response()

            dh.if_info['ae_config'] = ae_config

        if kwargs.get('debug_log_on'): pprint(dh.if_info['ae_config'])

        ### delete AE config
        if re.match(r'delete|down|off', action, re.I):
            if dh.if_info['ae_config'].get('{}_{}'.format(dh.tag, ae)):
                dh.config(command_list=['delete interfaces {}'.format(ae), 'commit'])
            else:
                dh.log('No AE config found in dh.if_info', level='error')

        ## re-add the set cfg
        if re.match(r'set|up|on', action, re.I):
            if dh.if_info['ae_config'].get('{}_{}'.format(dh.tag, ae)):
                ae_cfg_set = dh.if_info['ae_config']['{}_{}'.format(dh.tag, ae)]
                dh.config(command_list=[ae_cfg_set, 'commit'])
            else:
                dh.log('No AE config found in dh.if_info', level='error')


def _ifd_cfg_activate_deactivate(dh, ifd, action='activate', **kwargs):
    """
    deactivate interfaces xe-0/0/0; activate interfaces xe-0/0/0
    """
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    cmds = []
    if isinstance(ifd, str):
        ifd = [ifd]

    new_ifd_list = []
    for ifname in ifd:
        if not isinstance(ifname, str):
            new_ifd_list.extend(ifname)
        else:
            new_ifd_list.append(ifname)

    for ifname in new_ifd_list:
        if re.match(r'activate|up|on', action, re.I):
            cmds.append('activate interfaces {}'.format(ifname))
        elif re.match(r'deactivate|down|off', action, re.I):
            cmds.append('deactivate interfaces {}'.format(ifname))
        else:
            t.log('error', '{} :Unknown action'.format(func_name()))

    if kwargs.get('no_commit'):
        #config().config_engine(device_list=dh, cmd_list=cmds)
        dh.config(command_list=cmds)
    else:
        #config().config_engine(device_list=dh, cmd_list=cmds, commit=1)
        cmds.append('commit')
        dh.config(command_list=cmds)


def _ae_member_link_cfg_activate_deactivate(dh, ifd, action='activate', **kwargs):
    """
    set interfaces xe-0/0/0 disable ; delete interfaces xe-0/0/0 disable
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    ifd_list = kwargs.get('member_ifd_list')

    return _ifd_cfg_activate_deactivate(dh, ifd_list, action=action, **kwargs)


def _check_ae_member_link_cfg_activate_deactivate(dh, ifd, action='activate', **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    ifd_list = kwargs.get('member_ifd_list')

    return _check_ifd_cfg_activate_deactivate(dh, ifd_list, action=action, **kwargs)


def _check_ifd_cfg_activate_deactivate(dh, ifd, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())
    # find the current state first

    all_ifds = []
    cmd_response = []
    num_act = ''
    num_act_down = ''

    # find the current state first
    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        all_ifds.append(ifname)
        ifd_list = list(set(all_ifds))
    elog('== Check IFD activate/deactivate: {}'.format(nice_string(ifd_list)))

    state = 'activate|on'
    # Run all show cmds and append all laser responses of (on|up)
    for x, ifname in enumerate(ifd_list, 1):
        res = dh.config(command_list=['show interfaces {}'.format(ifname)])
        cmd_response.append(res.response())
        num_act = x

    # Loop thru all responses and determine if ifds are
    # on|up|enable or off|down|enabled state
    for x, line in enumerate(cmd_response, 1):
        if re.search('inactive:', line):
            num_act_down = x
            if num_act == num_act_down:
                #elog('== ifd: {} deactivated'.format(nice_string(ifd_list)), **kwargs)
                state = 'inactive|deactivate|off'

    if action is None:
        return state
    else:
        # compare with expected state:
        if re.match(state, action, re.I):
            return True
        else:
            return False


def _check_ifd_cfg_activate_deactivate_orig(dh, ifd, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())
    # find the current state first
    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        res = dh.config(command_list=['show interfaces {}'.format(ifd)])
        state = 'activate|on'

        if re.search('inactive:', res.response(), re.M):
            state = 'inactive|deactivate|off'

        if action is None:
            return state
        else:
            # compare with expected state:
            if re.match(state, action, re.I):
                return True
            else:
                return False


def _ae_cfg_activate_deactivate(dh, ae, action='activate', **kwargs):
    '''
    deactivate interface ae0, commit; activate interface ae0, commit
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    cmds = []
    ae_list = ae
    if isinstance(ae, str):
        ae_list = [ae.strip() for ae in ae.split(',')]
    for ae in ae_list:
        if re.match(r'activate|up|on', action, re.I):
            cmds.append('activate interfaces {}'.format(ae))
        elif re.match(r'deactivate|down|off', action, re.I):
            cmds.append('deactivate interfaces {}'.format(ae))
        else:
            t.log('error', '{} :Unknown action'.format(func_name()))

    if kwargs.get('no_commit'):
        dh.config(command_list=cmds)
    else:
        cmds.append('commit')
        dh.config(command_list=cmds)


def _check_ae_cfg_activate_deactivate(dh, ae, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())
    # find the current state first

    all_aes = []
    cmd_response = []
    act_num = ''
    num_act_down = ''

    ae_list = ae
    # find the current state first
    if isinstance(ae, str):
        ae_list = [ae.strip() for ae in ae.split(',')]
    for aename in ae_list:
        all_aes.append(aename)
        ae_list = list(set(all_aes))
    elog('== Check AE activate or deactivate: {}'.format(nice_string(ae_list)))

    state = 'activate|on'
    # Run all show cmds and append all laser responses of (on|up)
    for x, aename in enumerate(ae_list, 1):
        res = dh.config(command_list=['show interfaces {}'.format(aename)])
        cmd_response.append(res.response())
        act_num = x

    # Loop thru all responses and determine if ae(s) are
    # on|up|enable or off|down|enabled state
    for x, line in enumerate(cmd_response, 1):
        if re.search('inactive:', line):
            num_act_down = x
            if act_num == num_act_down:
                #elog('== ifd: {} deactivated'.format(nice_string(ae_list)), **kwargs)
                state = 'inactive|deactivate|off'

    if action is None:
        return state
    else:
        # compare with expected state:
        if re.match(state, action, re.I):
            return True
        else:
            return False


def _ifd_shell_up_down(dh, ifd, action='up', **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    dh.su()
    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        if re.match(r'up|on', action, re.I):
            dh.shell(command='ifconfig {} up'.format(ifname))
        elif re.match(r'deactivate|down|off', action, re.I):
            dh.shell(command='ifconfig {} down'.format(ifname))
        else:
            t.log('error', '{} :Unknown action'.format(func_name()))


def _check_ifd_shell_up_down(dh, ifd, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    all_ifds = []
    cmd_response = []
    num_actual = ''
    num_act_down = ''

    # find the current state first
    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        all_ifds.append(ifname)
        ifd_list = list(set(all_ifds))

    elog('== Check IFD shell {} for: {}'.format(action, nice_string(ifd_list)))

    # Run all show cmds and append all responses of (on|up)
    for x, ifname in enumerate(ifd_list, 1):
        res = dh.shell(command='ifconfig {}'.format(ifname))
        cmd_response.append(res.response())
        num_actual = x

    # Loop thru all responses and determine if ifds are
    # on|up|enable or off|down|enabled state
    state = 'enable|enabled|on|up'
    for x, line in enumerate(cmd_response, 1):
        if re.search('DOWN/HARDDOWN|DOWN', line, re.M):
            num_act_down = x
            if num_actual == num_act_down:
                #elog('== ifd: {} are ifconfig down'.format(nice_string(ifd_list)), **kwargs)
                state = 'disable|disabled|off|down'

    if action is None:
        return state
    else:
        # compare with expected state:
        if re.match(state, action, re.I):
            return True
        else:
            return False


def _ae_member_link_shell_up_down(dh, ifd, action='up', **kwargs):
    """
    """
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    ifd_list = kwargs.get('member_ifd_list')

    return _ifd_shell_up_down(dh, ifd_list, action=action, **kwargs)


def _check_ae_member_link_shell_up_down(dh, ifd, action='up', **kwargs):
    """
    """
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    ifd_list = kwargs.get('member_ifd_list')
    return _check_ifd_shell_up_down(dh, ifd_list, action=action, **kwargs)


def _ae_shell_up_down(dh, ae, action='up', **kwargs):
    '''
    ifconfig ae0 down; ifconfig ae0 up
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    dh.su()
    ae_list = ae
    if isinstance(ae, str):
        ae_list = [ae.strip() for ae in ae.split(',')]
    for ae in ae_list:
        if re.match(r'up|on', action, re.I):
            dh.shell(command='ifconfig {} up'.format(ae))
        elif re.match(r'down|off', action, re.I):
            dh.shell(command='ifconfig {} down'.format(ae))
        else:
            t.log('error', '{} :Unknown action'.format(func_name()))


def _check_ae_shell_up_down(dh, ae, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    all_aes = []
    cmd_response = []
    num_act = ''
    num_act_down = ''

    ae_list = ae
    if isinstance(ae, str):
        ae_list = [ae.strip() for ae in ae.split(',')]
    for aename in ae_list:
        all_aes.append(aename)
        ifd_list = list(set(all_aes))

    elog('== Check IFD shell {} for: {}'.format(action, nice_string(ifd_list)))

    # Run all show cmds and append all responses of (on|up)
    for x, aename in enumerate(ifd_list, 1):
        res = dh.shell(command='ifconfig {}'.format(aename))
        cmd_response.append(res.response())
        num_act = x

    # Loop thru all responses and determine if ifds are
    # on|up|enable or off|down|enabled state
    state = 'enable|enabled|on|up'
    for x, line in enumerate(cmd_response, 1):
        if re.search('DOWN', line):
            num_act_down = x
            if num_act == num_act_down:
                #elog('== ifd: {} are ifconfig down'.format(nice_string(ifd_list)), **kwargs)
                state = 'disable|disabled|off|down'

    if action is None:
        return state
    else:
        # compare with expected state:
        if re.match(state, action, re.I):
            return True
        else:
            return False


def _ifd_laser_on_off(dh, ifd, action='on', **kwargs):
    '''
    This is  the laser method of Robot keyword, ex:
    Flap Interface		device=r0	interface=r0-r5   	method=ifd_laser_on_off 	action=off

   :param dh:
        **REQUIRED** Device handle
    :param ifd  :
        **REQUIRED** IFD name
    :param action :
        **REQUIRED** Action(up|on, down|off)
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())
    #  hostname/tag should be made in init ( event init or toby init)

    if re.match(r'up|on', action, re.I):
        action = 'on'
    elif re.match(r'down|off', action, re.I):
        action = 'off'
    else:
        t.log('error', '========= {}: Could not determine action'.format(func_name()))
        return False

    res_cmds = []

    if isinstance(ifd, str):
        ifd = [ifd]
    # turn laser on/off on a list of ifd sequantially.  ( not sure if can/need to do in parallel)
    for ifname in ifd:
        cmd_dict = _get_laser_methods(dh, ifname, **kwargs)
        if cmd_dict:
            t.log('debug', '{}: selected laser function: {}.'.format(func_name(), cmd_dict))
        else:
            elog('error', '{}: Cannot find laser function for {}: ifd: {} !!!'.format(func_name(), get_dh_name(dh), ifname))
            dh.if_info['BYPASS_INTF_CHECK_{}'.format(ifname)] = True
            return False

        if cmd_dict.get('set_laser'):
            if kwargs.get('debug_log_on'): t.log('debug', '{}: set_laser/ifd: {}'.format(func_name(), ifname))
            res = cmd_dict['set_laser'](dh, ifname, action, **kwargs)
            for line in res:
                res_cmds.append(line)
        elif cmd_dict.get('set_laser_legacy'):
            if kwargs.get('debug_log_on'): t.log('debug', '{}: set_laser_legacy/ifd: {}'.format(func_name(), ifname))
            start_time = time.time()
            cmd_dict['set_laser_legacy'](dh, ifname, action, **kwargs)
            end_time = time.time()

    if res_cmds:
        if kwargs.get('debug_log_on'): t.log('debug', '{}: In res_cmds'.format(func_name()))
        all_cmds = "\n".join(res_cmds)
        start_time = time.time()
        dh.shell(command=all_cmds)
        end_time = time.time()

    t.log('info', func_name() + ': execution finished at {}, takes {}'.format(str(end_time), \
                str(end_time - start_time)))

    return True


def _check_ifd_laser_on_off(dh, ifd, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    all_ifds = []
    cmd_response = []
    num_act = ''
    num_act_up = ''
    num_act_down = ''

    status = False

    # find the current state first
    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        all_ifds.append(ifname)
        ifd_list = list(set(all_ifds))
    elog('== Check IFD laser for: {}'.format(nice_string(ifd_list)))

    for x, ifname in enumerate(ifd_list, 1):
        cmd_dict = _get_laser_methods(dh, ifname)
        cmd_response.append(cmd_dict['get_laser'](dh, ifname, **kwargs))
        num_act = x

    if re.match(r'down|off', action, re.I):
        for x, line in enumerate(cmd_response, 1):
            match = re.match('down|off', line)
            if match:
                num_act_down = x
                if num_act == num_act_down:
                    elog('== {} of {} IFD(s) down: {}'.format(num_act_down, num_act, nice_string(ifd_list)), **kwargs)
                    status = True
                    break

    elif re.match(r'on|up', action, re.I):
        for x, line in enumerate(cmd_response, 1):
            match = re.match('on|up', line)
            if match:
                num_act_up = x
                if num_act == num_act_up:
                    elog('== {} of {} IFD(s) on: {}'.format(num_act_up, num_act, nice_string(ifd_list)), **kwargs)
                    status = True
                    break

    return status


def _ae_member_link_laser_on_off(dh, ifd, action='on', **kwargs):
    """
    set interfaces xe-0/0/0 disable ; delete interfaces xe-0/0/0 disable
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    ifd_list = kwargs.get('member_ifd_list')

    return _ifd_laser_on_off(dh, ifd_list, action=action, **kwargs)


def _ae_check_ifd_laser_on_off(dh, ifd, action='on', **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    ifd_list = kwargs.get('member_ifd_list')

    return _check_ifd_laser_on_off(dh, ifd_list, action=action, **kwargs)


def _ifd_laser_bounce(dh, ifd, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    res_cmds = []
    res_cmds_off = []
    res_cmds_on = []

    interval = kwargs.get('interval', 5)  # unit second.  0.01 also works( msec)

    if isinstance(ifd, str):
        ifd = [ifd]
    # laser bounce on a list of ifd sequantially.  ( not sure if can/need to do in parallel)
    for ifname in ifd:
        # get the laser cmd based on model/pic types
        cmd_dict = _get_laser_methods(dh, ifname, **kwargs)
        if cmd_dict:
            t.log('debug', '{}: selected laser function: {}.'.format(func_name(), cmd_dict))
        else:
            elog('error', '{}: Cannot find laser function for {}: ifd: {} !!!'.format(func_name(), get_dh_name(dh), ifname))
            dh.if_info['BYPASS_INTF_CHECK_{}'.format(ifname)] = True
            return False

        if cmd_dict.get('set_laser'):
            if kwargs.get('debug_log_on'): t.log('debug', '{}: set_laser/ifd: {}'.format(func_name(), ifname))
            if cmd_dict['group'] == 'ifdev':
                res = cmd_dict['set_laser'](dh, ifname, action='bounce', **kwargs)
                for line in res:
                    res_cmds.append(line)
            else:
                res_off = cmd_dict['set_laser'](dh, ifname, action='off', **kwargs)
                res_on = cmd_dict['set_laser'](dh, ifname, action='on', **kwargs)
                for line in res_off:
                    res_cmds_off.append(line)
                for line in res_on:
                    res_cmds_on.append(line)

        elif cmd_dict.get('set_laser_legacy'):
            if kwargs.get('debug_log_on'): t.log('debug', '{}: set_laser_legacy/ifd: {}'.format(func_name(), ifname))
            res_off = cmd_dict['set_laser_legacy'](dh, ifname, action='off', **kwargs)
            res_on = cmd_dict['set_laser_legacy'](dh, ifname, action='on', **kwargs)

    start_time = time.time()

    if res_cmds:
        if kwargs.get('debug_log_on'): t.log('debug', '{}: res_cmds_1'.format(func_name()))
        all_cmds = "\n".join(res_cmds)
        dh.shell(command=all_cmds)

    if res_cmds_off and res_cmds_on:
        if kwargs.get('debug_log_on'): t.log('debug', '{}: res_cmds_2'.format(func_name()))
        all_cmds_off = "\n".join(res_cmds_off)
        all_cmds_on = "\n".join(res_cmds_on)
        dh.shell(command=all_cmds_off)
        time.sleep(float(interval))
        dh.shell(command=all_cmds_on)

    end_time = time.time()

    t.log('info', func_name() + ': execution finished at {}, takes {}'.format(str(end_time), \
                str(end_time - start_time)))

    return True


def _ae_member_link_fpc_restart(dh, ae, action=None, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    ifd_list = kwargs.get('member_ifd_list')

    return _fpc_restart(dh, ifd_list, action=action, **kwargs)


def _check_ae_member_link_fpc_restart(dh, ae, action=None, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    ifd_list = kwargs.get('member_ifd_list')

    return _check_fpc_restart(dh, ifd_list, **kwargs)


def _fpc_restart(dh, ifd, action=None, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    model = dh.get_model()
    if re.match('(m10i|m7i|mx80)', model):
        dh.log('FPC restart/panic not allowed on: {}'.format(model), level='error')
        return None

    fpc_slots = []
    cmds = []
    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        match = re.match(r'\w+-(\d+)/\d+/\d+.*', ifname)
        if match:
            fpc = match.group(1)
            fpc_slots.append(fpc)
        else:
            if kwargs.get('debug_log_on'):
                dh.log('{}: No FPC slot found'.format(func_name()), level='debug')
            return False
    fpc_slot_list = list(set(fpc_slots))
    if 'restart' in action:
        for fs in fpc_slot_list:
            cmds.append('request chassis fpc slot {} restart'.format(fs))
        cmd = "\n".join(cmds)
        elog('== restart fpc slot: {}'.format(nice_string(fpc_slot_list)), **kwargs)
        res = dh.cli(command=cmd)

    elif 'panic' in action:
        for fs in fpc_slot_list:
            elog('Action Panic fpc slot {}'.format(fs))
            #For MPC10 (Ferrari) and MPC11 (redbull), to enter VTY line card ,user needs to
            #send as VTY FPC<n>.0. So added a new function to return the FPC format needed
            #for older cards and as well as newer MPC cards
            pfe_for_vty = get_vty_pfe_for_line_card_mode(dh, fpc_slot=fs)
            elog('Action Panic fpc type is  {}'.format(pfe_for_vty))

            res = dh.vty(command='set parser security 10', destination='fpc{}'.format(pfe_for_vty)).response()

            if re.search('Security level', res):
                try:
                    dh.vty(command='test panic', destination='fpc{}'.format(pfe_for_vty), pattern='(.*)')
                except:
                    raise TobyException("Could not able to execute test panic")

        if kwargs.get('wait_for_core_file'):
            wait = kwargs.get('wait_for_core_file', 90)
            for fs in fpc_slot_list:
                elog("waiting {}s for core-dumps to be generated".format(wait))
                time.sleep(float(wait))
                sh_res = dh.cli(command='show system core-dumps').response()
                match = re.search(r'(core-\w+)'.format(fs), sh_res, re.M)
                if match:
                    core_name = match.group(1)
                    if not kwargs.get('delete_core_file'):
                        elog('FPC {} generated core during test panic.'.format(fs))
                    else:
                        elog('FPC {} generated core during test panic, deleting core file.'.format(fs))
                        dh.cli(command='file delete /var/crash/core-{}*'.format(core_name))


def _check_fpc_restart(dh, ifd, action=None, **kwargs):
    '''
    _check_fpc_restart
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    fpc_slots = []
    cmd_response = []
    num_up = ''
    num_act_up = ''

    wait = kwargs.get('wait_to_check', 5)
    elog("waiting for {} seconds..".format(wait))
    time.sleep(wait)

    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        match = re.match(r'\w+-(\d+)/\d+/\d+.*', ifname)
        if match:
            fpc = match.group(1)
            fpc_slots.append(fpc)
    fpc_slot_list = list(set(fpc_slots))
    elog('== Check FPC slot(s): {}'.format(nice_string(fpc_slot_list)))

    # Run all show cmds and append all responses
    for x, slot in enumerate(fpc_slot_list, 1):
        res = dh.cli(command='show chassis fpc {} | except Temp | except Slot'.format(slot))
        cmd_response.append(res.response())
        num_up = x

    # Loop thru all responses and determine if FPC is Online
    for x, line in enumerate(cmd_response, 1):
        fpc_match = re.search(FPC_REGEX_ONLINE, line)
        if fpc_match:
            num_act_up = x
            if num_up == num_act_up:
                elog('== FPC(s) online: {}'.format(nice_string(fpc_slot_list)), **kwargs)
                return True
                break


def _fpc_on_off(dh, ifd, action, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    model = dh.get_model()
    if re.match('(m10i|m7i|mx80)', model):
        dh.log('FPC offline/online not allowed on: {}'.format(model), level='error')
        return None

    fslots = []
    cmds = []

    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        match = re.match(r'\w+-(\d+)/\d+/\d+.*', ifname)
        if match:
            fpc = match.group(1)
            fslots.append(fpc)
        else:
            dh.log('{}: No FPC slot found'.format(func_name()), level='warn')
            return False

    fpc_slot_list = list(set(fslots))
    for fs in fpc_slot_list:
        if re.match(r'off|down|offline', action, re.I):
            cmds.append('request chassis fpc slot {} offline'.format(fs))
        elif re.match(r'on|up|online', action, re.I):
            cmds.append('request chassis fpc slot {} online'.format(fs))
        else:
            t.log('error', '{} :Unknown action'.format(func_name()))

    cmd = "\n".join(cmds)
    elog('++ {} fpc slot(s): {}'.format(action, nice_string(fpc_slot_list)), **kwargs)
    dh.cli(command=cmd)

    # if re.search('transition|already', res.response(), re.M):
    #     elog('warn', 'RES: {}'.format(res.response()))
    #     kwargs['fru_checking'] = True
    #     elog('warn', 'ARGS: {}'.format(kwargs['fru_checking']))


def _check_fpc_on_off(dh, ifd, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    fslots = []
    cmd_response = []
    num_fpcs = ''
    num_act_up = ''
    num_act_down = ''
    status = False

    wait = kwargs.get('wait_to_check', 5)
    elog("waiting for {} seconds..".format(wait))
    time.sleep(wait)

    if ifd is not None:
        if isinstance(ifd, str):
            ifd = [ifd]
        for ifname in ifd:
            match = re.match(r'\w+-(\d+)/\d+/\d+.*', ifname)
            if match:
                fpc = match.group(1)
                fslots.append(fpc)
            else:
                dh.log('{}: No FPC slot found'.format(func_name()), level='warn')
                return False

    fpc_slot_list = list(set(fslots))
    elog('== Check FPC slot(s): {}'.format(nice_string(fpc_slot_list)))

    # Run all show cmds and append all responses
    if re.match(r'offline|off|down', action, re.I):
        for x, slot in enumerate(fpc_slot_list, 1):
            res = dh.cli(command='show chassis fpc {} | except Temp | except Slot'.format(slot))
            cmd_response.append(res.response())
            num_fpcs = x

        # Loop thru all responses and determine if FPC is Offline
        for x, line in enumerate(cmd_response, 1):
            fpc_match = re.search(FPC_REGEX_OFFLINE, line)
            if fpc_match:
                num_act_down = x
                if num_fpcs == num_act_down:
                    elog('== FPC(s) offline: {}'.format(nice_string(fpc_slot_list)), **kwargs)
                    status = True
                    break

    elif re.match(r'online|on|up', action, re.I):
        for x, slot in enumerate(fpc_slot_list, 1):
            res = dh.cli(command='show chassis fpc {} | except Temp | except Slot'.format(slot))
            cmd_response.append(res.response())
            num_fpcs = x

        # Loop thru all responses and determine if FPC is Online
        for x, line in enumerate(cmd_response, 1):
            fpc_match = re.search(FPC_REGEX_ONLINE, line)
            if fpc_match:
                num_act_up = x
                if num_fpcs == num_act_up:
                    elog('== FPC(s) online: {}'.format(nice_string(fpc_slot_list)), **kwargs)
                    status = True
                    break


    return status

def _mic_on_off(dh, ifd, action, **kwargs):
    """
    trigger method for mic restart
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    model = dh.get_model()
    if re.match('(m10i|m7i|mx80)', model):
        dh.log('FPC offline/online not allowed on: {}'.format(model), level='error')
        return None

    pre_cmds = []
    cmds = []

    wait = kwargs.get('wait', 2)

    if dh.fru_info.get('BYPASS_FRU_CHECK'):
        dh.fru_info.pop('BYPASS_FRU_CHECK')

    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        match = re.match(r'\w+-(\d+)/(\d+)/\d+.*', ifname)
        if match:
            fpc = match.group(1)
            mic = _find_mic_type(dh, ifd=ifname, **kwargs)
            if not mic:
                dh.log('MIC slot not found or already offline for {}'.format(ifname), level='warn')
                dh.fru_info['BYPASS_FRU_CHECK'] = True
            else:
                pre_cmds.append('fpc-slot {} mic-slot {}'.format(fpc, mic))
        else:
            dh.log('{}: No FPC/MIC slot found'.format(func_name()), level='warn')
            return False

        if dh.fru_info.get('FPC{}/MIC{}'.format(fpc, mic)):
            dh.fru_info.pop('FPC{}/MIC{}'.format(fpc, mic))

    mic_cmd_list = list(set(pre_cmds))
    for mic_cmd in mic_cmd_list:
        if re.match(r'off|down|offline', action, re.I):
            cmds.append('request chassis mic {} offline'.format(mic_cmd))
        elif re.match(r'on|up|online', action, re.I):
            cmds.append('request chassis mic {} online'.format(mic_cmd))
        else:
            t.log('error', '{} :Unknown action'.format(func_name()))

    cmd = "\n".join(cmds)
    elog('++ {}: {}'.format(action, nice_string(mic_cmd_list)))
    mic_res = dh.cli(command=cmd)
    time.sleep(wait)

    ## If MIC is not supported on the FPC
    no_support_regex = re.compile(r'^FPC\s+\w+\s+(\d+)\s+does\s+not\s+support\s+this\s+command', re.M)
    matches = [m.groups() for m in no_support_regex.finditer(mic_res.response())]
    for m in matches: ## If router returns a do not support message, bypass fru checking
        elog('warn', '{}: FPC: {} does not support MIC offline/online...'.format(get_dh_name(dh), m[0]))
        dh.fru_info['BYPASS_FRU_CHECK'] = True

    ## If MIC is already in the the same state as the called action.
    already_regex = re.compile(r'^FPC\s+(\d+),\s+MIC\s+(\d+)\s+is\s+already\s+(\w+)', re.M)
    already_matches = [m.groups() for m in already_regex.finditer(mic_res.response())]
    for m in already_matches:
        elog('warn', 'FPC/MIC {}/{} already {}...'.format(m[0], m[1], m[2]))
        dh.fru_info['FPC{}/MIC{}'.format(m[0], m[1])] = True

    return True

def _check_mic_on_off(dh, ifd, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    fslots = {}
    cmd_response = []
    num_mics = ''
    num_act_up = ''
    num_act_down = ''
    status = False

    if ifd is not None:
        if isinstance(ifd, str):
            ifd = [ifd]
        for ifname in ifd:
            match = re.match(r'\w+-(\d+)/(\d+)/\d+.*', ifname)
            if match:
                fpc = match.group(1)
                pic = match.group(2)
                try:
                    mic = _find_mic_type(dh, ifd=ifname, **kwargs)
                    fpc_mic = '/'.join([fpc, mic])
                except:
                    dh.log('{}: No FPC/MIC slot found'.format(func_name()), level='warn')
                    return False
            else:
                dh.log('{}: No FPC/MIC slot found'.format(func_name()), level='warn')
                return False

            fslots[fpc_mic] = pic

            ## If MIC was already in opposite state of action
            ## remove the MIC from the check list, so we
            ## do not see a false failure.
            if dh.fru_info.get('FPC{}/MIC{}'.format(fpc, mic)):
                elog('Cannot check FPC {}/MIC {}'.format(fpc, mic))
                fpc_mic_remove = '/'.join([fpc, mic])
                fslots.pop(fpc_mic_remove)

    mic_slot_list = list(fslots.keys())
    if mic_slot_list is not None:
        elog('== Check FPC/MIC slot(s): {}'.format(nice_string(mic_slot_list)))
    else:
        return True

    # Run all show cmds and append all responses
    if re.match(r'offline|off|down', action, re.I):
        for x, slot in enumerate(mic_slot_list, 1):
            match = re.match(r'(\d+)\/(\d+)', slot)
            if match:
                fpc = match.group(1)
                mic = match.group(2)
                pic = fslots.get(slot)
            res = dh.cli(command='show chassis pic fpc-slot {} pic-slot {} | match State'.format(fpc, pic))
            cmd_response.append(res.response())
            num_mics = x

        # Loop thru all responses and determine if MIC is Offline
        for x, line in enumerate(cmd_response, 1):
            mic_match = re.match(PIC_REGEX_OFFLINE, line)
            if mic_match:
                num_act_down = x
                if num_mics == num_act_down:
                    elog('== {} of {} MIC(s) offline: {}'.format(num_act_down, num_mics, nice_string(mic_slot_list)), **kwargs)
                    status = True
                    break

    elif re.match(r'online|on|up', action, re.I):
        for x, slot in enumerate(mic_slot_list, 1):
            match = re.match(r'(\d+)\/(\d+)', slot)
            if match:
                fpc = match.group(1)
                mic = match.group(2)
                pic = fslots.get(slot)
            res = dh.cli(command='show chassis pic fpc-slot {} pic-slot {} | match State'.format(fpc, pic))
            cmd_response.append(res.response())
            num_mics = x

        # Loop thru all responses and determine if MIC is Online
        for x, line in enumerate(cmd_response, 1):
            mic_match = re.match(PIC_REGEX_ONLINE, line)
            if mic_match:
                num_act_up = x
                if num_mics == num_act_up:
                    elog('== {} of {} MIC(s) online: {}'.format(num_act_up, num_mics, nice_string(mic_slot_list)), **kwargs)
                    status = True
                    break

    return status

def _pic_on_off(dh, ifd, action, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    model = dh.get_model()
    if re.match('(m10i|m7i|mx80|acx2000)', model.lower()):
        dh.log('Returning False', level='info')
        dh.log('FPC offline/online not allowed on: {}'.format(model), level='error')
        #returning False instead of None which will help Toby users to verify in robot script and can take action
        return False

    pre_cmds = []
    cmds = []

    wait = kwargs.get('wait', 2)

    if dh.fru_info.get('BYPASS_FRU_CHECK'):
        dh.fru_info.pop('BYPASS_FRU_CHECK')

    if isinstance(ifd, str):
        ifd = [ifd]
    for ifname in ifd:
        match = re.match(r'\w+-(\d+)/(\d+)/\d+.*', ifname)
        if match:
            fpc = match.group(1)
            pic = match.group(2)
            pre_cmds.append('fpc-slot {} pic-slot {}'.format(fpc, pic))

        else:
            dh.log('{}: No FPC/PIC slot found'.format(func_name()), level='warn')
            return False

        if dh.fru_info.get('FPC{}/PIC{}'.format(fpc, pic)):
            dh.fru_info.pop('FPC{}/PIC{}'.format(fpc, pic))

    pic_cmd_list = list(set(pre_cmds))
    for pic_cmd in pic_cmd_list:
        if re.match(r'off|down|offline', action, re.I):
            cmds.append('request chassis pic {} offline'.format(pic_cmd))
        elif re.match(r'on|up|online', action, re.I):
            cmds.append('request chassis pic {} online'.format(pic_cmd))
        else:
            t.log('error', '{} :Unknown action'.format(func_name()))

    cmd = "\n".join(cmds)
    elog('++ {}: {}'.format(action, nice_string(pic_cmd_list)))
    pic_res = dh.cli(command=cmd)
    time.sleep(wait)

    ## If PIC is already in the same state as the action
    no_support_regex = re.compile(r'^FPC\s+\w+\s+(\d+)\s+does\s+not\s+support\s+this\s+command', re.M)
    matches = [m.groups() for m in no_support_regex.finditer(pic_res.response())]
    for m in matches: ## If router returns a do not support message, bypass fru checking
        elog('warn', 'FPC: %s does not support PIC offline/online...' % (m[0]))
        dh.fru_info['BYPASS_FRU_CHECK'] = True

    ## If PIC is already in the the same state as the called action.
    already_regex = re.compile(r'^FPC\s+(\d+),\s+PIC\s+(\d+)\s+is\s+already\s+(\w+)', re.M)
    already_matches = [m.groups() for m in already_regex.finditer(pic_res.response())]
    for m in already_matches:
        elog('warn', 'FPC/PIC {}/{} already {}...'.format(m[0], m[1], m[2]))
        dh.fru_info['FPC{}/PIC{}'.format(m[0], m[1])] = True

    return True


def _check_pic_on_off(dh, ifd, action=None, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    fslots = []
    cmd_response = []
    num_pics = ''
    num_act_up = ''
    num_act_down = ''
    status = False

    if ifd is not None:
        if isinstance(ifd, str):
            ifd = [ifd]
        for ifname in ifd:
            match = re.match(r'\w+-(\d+)/(\d+)/\d+.*', ifname)
            if match:
                fpc = match.group(1)
                pic = match.group(2)
                fpc_pic = '/'.join([fpc, pic])
            else:
                dh.log('{}: No FPC/PIC slot found'.format(func_name()), level='warn')
                return False

            fslots.append(fpc_pic)

            ## If PIC was already in opposite state of action
            ## remove the PIC from the check list, so we
            ## do not see a false failure.
            if dh.fru_info.get('FPC{}/PIC{}'.format(fpc, pic)):
                elog('Cannot check FPC {}/PIC {}'.format(fpc, pic))
                fpc_pic_remove = '/'.join([fpc, pic])
                fslots.remove(fpc_pic_remove)

    pic_slot_list = list(set(fslots))
    if pic_slot_list is not None:
        elog('== Check FPC/PIC slot(s): {}'.format(nice_string(pic_slot_list)))
    else:
        return True

    # Run all show cmds and append all responses
    if re.match(r'offline|off|down', action, re.I):
        for x, slot in enumerate(pic_slot_list, 1):
            match = re.match(r'(\d+)\/(\d+)', slot)
            if match:
                fpc = match.group(1)
                pic = match.group(2)
            res = dh.cli(command='show chassis pic fpc-slot {} pic-slot {} | match State'.format(fpc, pic))
            cmd_response.append(res.response())
            num_pics = x

        # Loop thru all responses and determine if PIC is Offline
        for x, line in enumerate(cmd_response, 1):
            pic_match = re.match(PIC_REGEX_OFFLINE, line)
            if pic_match:
                num_act_down = x
                if num_pics == num_act_down:
                    elog('== {} of {} PIC(s) offline: {}'.format(num_act_down, num_pics, nice_string(pic_slot_list)), **kwargs)
                    status = True
                    break

    elif re.match(r'online|on|up', action, re.I):
        for x, slot in enumerate(pic_slot_list, 1):
            match = re.match(r'(\d+)\/(\d+)', slot)
            if match:
                fpc = match.group(1)
                pic = match.group(2)
            res = dh.cli(command='show chassis pic fpc-slot {} pic-slot {} | match State'.format(fpc, pic))
            cmd_response.append(res.response())
            num_pics = x

        # Loop thru all responses and determine if PIC is Online
        for x, line in enumerate(cmd_response, 1):
            pic_match = re.match(PIC_REGEX_ONLINE, line)
            if pic_match:
                num_act_up = x
                if num_pics == num_act_up:
                    elog('== {} of {} PIC(s) online: {}'.format(num_act_up, num_pics, nice_string(pic_slot_list)), **kwargs)
                    status = True
                    break

    return status


###############################################
# laser trigger methods #######################
###############################################


def _laser_methods():
    '''
    '''
    pic_group = {
        ################# ifdev ###################
        # mx240|mx480|mx960|mx2020, version 16.1+ #
        'ifdev': {
            'pic_list': ['ifdev'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser': _set_ifdev_laser,
                'get_laser': _check_ifd,
                },
            },
        #################### MPC - 10GE XFP ##############
        # Router Model    FPC               PIC          #
        # mx80            MPC BUILTIN       4x 10GE XFP  #
        # mx80            MPC BUILTIN       1x 10GE XFP  #
        # mx240           MPC Type 2 3D EQ  2x 10GE  XFP #
        # mx240           MPC Type 2 3D EQ  1x 10GE  XFP #
        '10ge_xfp': {
            'pic_list': ['1x 10GE XFP', '4x 10GE XFP', '4x 10GE (LAN/WAN) XFP', \
                         '2x 10GE  XFP', '1x 10GE  XFP'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser': _set_10ge_xfp_laser,
                'get_laser': _check_10ge_xfp_laser,
                },
            },
        #################### DPC - 10GE XFP ########################
        # mx960     DPCE 4x 10GE R EQ          1x 10GE(LAN/WAN) EQ #
        # mx480     DPCE 20x 1GE + 2x 10GE R   1x 10GE(LAN/WAN)    #
        '10ge_dpc_eq_xfp': {
            'pic_list': ['1x 10GE(LAN/WAN) EQ', '1x 10GE(LAN/WAN)'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser': _set_10ge_dpc_xfp_laser,   #### STILL NEED TO TEST THIS ON DPC HW
                'get_laser': _check_10ge_xfp_laser,
                },
            },
        ################ SONET XFP PICs ##################
        # t1600     FPC Type 4-ES  4x 10GE (LAN/WAN) XFP #
        # t1600     FPC Type 4-ES  4x OC-192 SONET XFP   #
        # t4000     FPC Type 4-ES  4x OC-192 SONET XFP   #
        'sonet_xfp': {
            'pic_list': ['4x OC-192 SONET XFP'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser': _set_sonet_xfp_laser,
                'get_laser': _check_ifd,
                },
            },
        ############### T5E-based 10GE PICs ###############
        # t4000     FPC Type 5-3D  12x10GE (LAN/WAN) SFPP #
        # ptx3000   FPC            24x 10GE(LAN) SFP+     #
        # ptx5000   FPC            24x 10GE(LAN) SFP+     #
        # ptx5000   FPC E          24x 10GE(LWO) SFP+     #
        '10ge_t5e_sfpp': {
            'pic_list': ['12x10GE (LAN/WAN) SFPP', '24x 10GE(LWO) SFP+', '24x 10GE(LAN) SFP+'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser_legacy': _set_t5e_10ge_sfpp_laser,
                'get_laser': _check_ifd,
                },
            },
        ########## Agent-Smith-based 10GE PICs ##########
        # mx480     MPC 3D 16x 10GE   4x 10GE(LAN) SFP+ #
        '10ge_agent_smith': {
            'pic_list': ['4x 10GE(LAN) SFP+'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser': _set_agent_smith_laser,
                'get_laser': _check_agent_smith_laser,
                },
            },
        ########### Trinity-based 1GE PICs #############
        # mx480     MPC Type 2 3D     10x 1GE(LAN) SFP #
        '1ge_trinity': {
            'pic_list': ['10x 1GE(LAN) SFP'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser_legacy': _set_mtip_gpcs_laser,
                'get_laser': _check_mtip_gpcs_laser,
                },
            },
        ################### CFP-based PICs ######################
        # ptx5000         FPC E                4x100GE CFP2     #
        # ptx5000         FPC E               4x100GE OTN CFP2  #
        # ptx5000         FPC T                2x 100GE CFP     #
        # t4000           FPC Type 5-3D        1x100GE          #
        # mx480           MPC4E 3D 2CGE+8XGE   1X100GE CFP      #
        # mx480           MPC5E 3D Q 2CGE+4XGE 1X100GE CFP2 OTN #
        '100ge_40ge_cfp': {
            'pic_list': ['4x100GE CFP2', '2x 100GE CFP', '1X100GE CFP2 OTN', '1x100GE', \
                         '1X100GE CFP', '2x 40GE CFP', '4x100GE OTN CFP2'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser': _set_cfp_laser,
                'get_laser': _check_cfp_laser,
                },
            },
        ################ CMIC-based PICs #######################
        # mx480     MPC4E 3D 32XGE      8X10GE SFPP            #
        # mx480     MPC4E 3D 2CGE+8XGE  4x10GE SFPP            #
        #                                     10x10GE SFPP     #
        # mx960     MPC5E 3D Q 2CGE+4XGE      2X10GE SFPP OTN  #
        # mx960     MPC5E 3D Q 24XGE+6XLGE    12X10GE SFPP OTN #
        '10ge_cmic': {
            'pic_list': ['8X10GE SFPP', '4x10GE SFPP', '10X10GE SFPP', '2X10GE SFPP OTN', \
                         '12X10GE SFPP OTN'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser': _set_cmic_laser,
                'get_laser': _check_cmic_laser,
                },
            },
        ################# QSFP-based PICs ##############################################
        # mx960     MPC7E 3D MRATE-12xQSFPP-XGE-XLGE-CGE    MRATE-6xQSFPP-XGE-XLGE-CGE #
        # ptx5k     FPC E                                   48x10G/12x40G(LWO)QSFP+    #
        # ptx5k     FPC-P1                         15x100GE/15x40GE/60x10GE QSFP28 PIC #
        # ptx5k     FPC-P1                                               96x10/24x40GE #
        # qfx5200   QFX5200-32C-32Q                                32X40G/32X100G-QSFP #
        # qfx10008  ULC-36Q-12Q28                                               36X40G #
        # qfx5100   QFX5100-48S-6Q                                        48x10G-6x40G #
        # qfx10002  QFX10002-72Q                                                72X40G #
        # ptx1000   Builtin                                  288X10GE/72X40GE/24X100GE #
        # ptx       LC1102 - 12C / 36Q / 144X                12x100GE/36x40GE/144x10GE #
        # qfx5k     QFX5110-48S-4C                                       48x10G-4x100G #
        # ptx10001  JNP10001-CHAS argus                                        20X100G #
        # ptx10001  JNP10001-CHAS argus                           16xQSFP28 Macsec TIC #
        # ptx3000   FPC3-SFF-PTX-1X                               10x100/10x40/40x10GE #
        # qfx5110   QFX5110-32Q                                           32x 40G-QSFP #
        # qfx5100   QFX5100-24Q-2P                                        24x 40G-QSFP #
        # qfx5200   QFX5200-32C-32Q                                32X40G/32X100G-QSFP #
        # QFX10016  ULC-30Q28                                        30X100G           #
        # MX2010    MPC9E 3D MRATE-12xQSFPP-XGE-XLGE-CGE      MRATE-12xQSFPP-XGE-XLGE-CGE#
                            
        'qsfp_pic': {
            'pic_list': ['MRATE-6xQSFPP-XGE-XLGE-CGE', '48x10G/12x40G(LWO)QSFP+', \
                         '15x100GE/15x40GE/60x10GE QSFP28 PIC', '96x10/24x40GE', \
                         '32X40G/32X100G-QSFP', '36X40G', '48x10G-6x40G', '72X40G', \
                         'QSFP-100GBASE-SR4', '288X10GE/72X40GE/24X100GE', \
                         '48x10G-4x100G', '12x100GE/36x40GE/144x10GE', '20X100G', \
                         '10x100/10x40/40x10GE', '16xQSFP28 Macsec TIC', \
                         '24x 40G-QSFP', '32X40G/32X100G-QSFP', '32x 40G-QSFP', '48x25G-8x100G', \
                         '48x25G-6x100G','30X100G','30x100GE/30x40GE/96x10GE', '64X40G/64X100G-QSFP',
                          'MRATE-12xQSFPP-XGE-XLGE-CGE'],
            'attributes': ['legacy'],
            'methods': {
                'set_laser': _set_qsfp_laser,
                'get_laser': _check_ifd,
                },
            },
        # ptx1k   PTX10003-80C                                  4x400G/10x200G/20x100G # 

        'qsfp_picd': {
            'pic_list': ['32X40G/32X100G-QSFP', '4x400G/10x200G/20x100G'],
            'attributes': ['evo'],
            'methods': {
                'set_laser_legacy': _set_picd_laser,
                'get_laser': _check_ifd,
                },
            },
        }

    return pic_group


def _get_laser_methods(dh, ifd, **kwargs):
    '''
    action: on/off/bounce|flap ?
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    # figure out platform/pic type
    # pic type may only required in laser on/off, leave the checking in
    # corresponding methods.

    # now find PIC description to determine pic type
    pic_type = _find_pic_type(dh, ifd, **kwargs)
    t.log('debug', 'pic_type: {}'.format(pic_type))

    methods = {}

    for group, attr in _laser_methods().items():
        if (pic_type[0] in attr['pic_list'] and pic_type[1] in attr['attributes']):
            methods = attr['methods']
            methods['group'] = group
            break

    return methods


def _find_pic_type(dh, ifd=None, **kwargs):
    '''
    # need to add multi-chassis processing( found in get_ifd_hw in Interface.pm)
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    model = dh.get_model()
    version = dh.get_version(major=True)
    if re.match(r'acx(710|5448-d|5448-m|5448)', model, re.I):
        return 'ifdev', 'legacy'
    if re.match(r'r(6675)', model, re.I):
        return 'ifdev', 'legacy'

    if re.match(r'mx(104|204|240|480|960|2020)', model, re.I) and version > '16.1':
        return 'ifdev', 'legacy'

    ## Setup OS attributes
    if dh.device_info.get('isEvo'):
        device_type = 'evo'
    else:
        device_type = 'legacy'

    # check if pic type is already saved with dh
    if dh.if_info.get('pic_types') is None:
        if kwargs.get('debug_log_on'):
            t.log('debug', '{} :run show chassis hardware and save all pic_types for DUT'.\
                            format(func_name()))

        resp_xml = dh.cli(command='show chassis hardware', format='xml').response()
        response = strip_xml_namespace(resp_xml)
        fpc = \
            response.xpath("//chassis-module[contains(name, 'FPC')]/chassis-sub-module")

        pic_types = {}

        for mod in fpc:
            fpc_slot = re.sub(r'^\w+ (\d+)', r'\1', mod.findtext('../name'))
            sub_name = mod.findtext('name')
            if re.match(r'PIC', sub_name):
                pic_slot = re.sub(r'^\w+ (\d+)', r'\1', sub_name)
                pic_types['{}/{}'.format(fpc_slot, pic_slot)] = mod.findtext('description')
            else:
                for subsub in mod.xpath('.//chassis-sub-sub-module'):
                    fru_name = subsub.findtext('name')
                    if re.match(r'PIC', fru_name):
                        pic_slot = re.sub(r'^\w+ (\d+)', r'\1', fru_name)
                        pic_types['{}/{}'.format(fpc_slot, pic_slot)] = \
                            subsub.findtext('description')
                    else:
                        for sub3 in subsub.xpath('.//chassis-sub-sub-sub-module'):
                            fru_name = sub2.findtext('name')
                            if re.match(r'PIC', fru_name):
                                pic_slot = re.sub(r'^\w+ (\d+)', r'\1', fru_name)
                            pic_types['{}/{}'.format(fpc_slot, pic_slot)] = \
                                sub3.findtext('description')

        dh.if_info['pic_types'] = pic_types

    if ifd is not None:
        pic = re.sub(r'.+-(\d+/\d+).+', r'\1', ifd)
        pic_type = dh.if_info['pic_types'].get(pic)
        return pic_type, device_type
    else:
        return dh.if_info['pic_types'], device_type


def _find_mic_type(dh, ifd=None, **kwargs):
    '''
    method to check MIC/PIC
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    model = dh.get_model()
    version = dh.get_version(major=True)

    if dh.if_info.get('mic_types') is None:
        if kwargs.get('debug_log_on'):
            t.log('debug', '{} :run show chassis hardware and save all mic_types for DUT'.\
                            format(func_name()))
        rpc_cmd = dh.get_rpc_equivalent(command='show chassis hardware')
        response = dh.execute_rpc(command=rpc_cmd).response()
        fpc = \
            response.xpath("//chassis-module[contains(name, 'FPC')]/chassis-sub-module")
        mic_types = {}
        for mod in fpc:
            fpc_slot = re.sub(r'^\w+ (\d+)', r'\1', mod.findtext('../name'))
            sub_name = mod.findtext('name')
            if re.match(r'MIC', sub_name):
                mic_slot = re.sub(r'^\w+ (\d+)', r'\1', sub_name)
                pic_slot = None
                for subsub in mod.xpath('.//chassis-sub-sub-module'):
                    fru_name = subsub.findtext('name')
                    if re.match(r'PIC', fru_name):
                        pic_slot = re.sub(r'^\w+ (\d+)', r'\1', fru_name)
                        mic_types['{}/{}'.format(fpc_slot, pic_slot)] = \
                            mic_slot


        dh.if_info['mic_types'] = mic_types

    if ifd is not None:
        pic = re.sub(r'.+-(\d+/\d+).+', r'\1', ifd)
        mic_slot = dh.if_info['mic_types'].get(pic)
        return mic_slot
    else:
        return dh.if_info['mic_types']


def _set_ifdev_laser(dh, ifd, action='off', **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())


    cmds = []

    pfe = get_pfe(dh, ifd)

    if re.match(r'on|off', action, re.I):
        cmds.append("cprod -A {} -c 'test ifdev {} laser {}'".format(pfe, ifd, action))
    elif re.match(r'flap|bounce', action, re.I):
        ### default to 1 second bounce
        # duration (in msecs) of new laser state,
        # after which the laser will go to the opposite state
        msec = float(kwargs.get('interval', 5)) * 1000
        msec = int(msec)
        cmds.append("cprod -A {} -c 'test ifdev {} laser off {}'".format(pfe, ifd, msec))
    else:
        t.log('error', '====unknown action {} in {}'.format(action, func_name()))
        return None

    return cmds


def _check_ifd(dh, ifd, action=None, **kwargs):
    '''
    Used for laser checking if there are no pfe level laser check commands/outputs.
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    cmd = 'show interfaces {} terse media | except Interface'.format(ifd)
    res = dh.cli(command=cmd).response()
    if re.match(r'\w+-\d+/\d+/\d+(\:\d+\s+up\s+up|\s+up\s+up)', res):
        return 'on'
        if kwargs.get('debug_log_on'):
            dh.log(message='{}:IFD: {} is up...'.format(func_name(), ifd))
    elif re.match(r'\w+-\d+/\d+/\d+(\:\d+\s+up\s+down|\s+up\s+down)', res):
        return 'off'
        if kwargs.get('debug_log_on'):
            dh.log(message='{}:IFD: {} is down...'.format(func_name(), ifd))
    elif re.match(r'\w+-\d+/\d+/\d+(\:\d+\s+down\s+down|\s+down\s+down)', res):
        elog('warn', 'IFD: {} is admin down...'.format(ifd))
        return True
    elif re.search('not\s+found', res):
        elog('IFD: {} is not found...'.format(ifd))
        return 'off'
    else:
        dh.log(message='====Did not get IFD status, proceeding....', level='warn')
        return None


def _set_10ge_xfp_laser(dh, ifd, action='off', **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    try:
        index = _get_xfp_index(dh, ifd)
    except:
        dh.log('Cannot find 10GE XPF index', level='error')
        return

    cmds = []

    pfe = get_pfe(dh, ifd)

    if re.match(r'on', action, re.I):
        cmds.append("cprod -A {} -c 'test xfp {} laser on'".format(pfe, index))
    else:
        cmds.append("cprod -A {} -c 'test xfp {} laser off'".format(pfe, index))

    return cmds


def _get_xfp_index(dh, ifd, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    slot = re.sub(r'\w+-', '', ifd)

    if not (dh.if_info.get('index') and dh.if_info['index'].get(slot)):
        res = dh.vty(command='show xfp list', destination=get_pfe(dh, ifd)).response()
        for line in res.split('\n'):
            match = re.search(r'^\s*(\d+)\s+xfp\-(\d+/\d+/\d+)', line)
            if match:
                index = match.group(1)
                pic_slot = match.group(2)
                config_utils.nested_set(dh.if_info, ['index', pic_slot], index)
    elif dh.if_info.get('index') and dh.if_info['index'].get(slot):
        if kwargs.get('debug_log_on'):
            dh.log(message='{}: found previously saved XFP index for interface: {}'.\
                    format(func_name(), ifd), level='debug')
        return dh.if_info['index'][slot]
    else:
        if kwargs.get('debug_log_on'):
            dh.log(message='{}: no xfp index found for interface: {}'.\
                    format(func_name(), ifd), level='error')
        return None

    return dh.if_info['index'][slot]


def _check_10ge_xfp_laser(dh, ifd, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    index = _get_xfp_index(dh, ifd)

    res = dh.vty(command="show xfp {} alarm".format(index), \
                 destination=get_pfe(dh, ifd)).response()

    if re.search(r'^\s+Tx not ready:\s+\d+\s+Clear', res, re.M):
        dh.log(message='{}: Laser state is ON for interface: {}'.\
                    format(func_name(), ifd), level='info')
        return 'on'
    elif re.search(r'^\s+Tx not ready:\s+\d+\s+Set', res, re.M):
        dh.log(message='{}: Laser state is OFF for interface: {}'.\
                        format(func_name(), ifd), level='info')
        return 'off'
    else:
        dh.log(message='{}: Problem getting the laser state of ifd {}'.\
                    format(func_name(), ifd), level='error')


def _set_10ge_dpc_xfp_laser(dh, ifd, action='off', **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    try:
        index = _get_dpc_xfp_index(dh, ifd)
    except:
        dh.log('No 10GE dpc xfp index found', level='error')
        return True

    pfe = get_pfe(dh, ifd)

    cmds = []

    if re.match(r'on', action, re.I):
        cmds.append("cprod -A {} -c 'test xfp {} laser on'".format(pfe, index))
    else:
        cmds.append("cprod -A {} -c 'test xfp {} laser off'".format(pfe, index))

    return cmds

def _get_dpc_xfp_index(dh, ifd):
    '''
    '''
    slot = re.sub(r'\w+-', '', ifd)

    if not (dh.if_info.get('index') and dh.if_info['index'].get(slot)):
        res = dh.vty(command='show xfp list', destination=get_pfe(dh, ifd)).response()
        for line in res.split('\n'):
            ### TBD, NEED TO FIND A ROUTER WITH DPC'S
            match = re.search(r'^\s*(\d+)\s+XETH\-(\d+/\d+/\d+)', line, re.M)
            if match:
                index = match.group(1)
                pic_slot = match.group(2)
                config_utils.nested_set(dh.if_info, ['index', pic_slot], index)
    else:
        dh.log(message='{}: no dpc_xfp index found for interface: {}'.format(func_name(), ifd), \
                    level='error')
        return None

    return dh.if_info['index'][slot]


def _set_sonet_xfp_laser(dh, ifd, action='off', **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    try:
        index = _get_xfp_index(dh, ifd)
    except:
        dh.log('No Sonet xfp index found', level='error')
        return True

    pfe = get_pfe(dh, ifd)

    cmds = []

    if re.match(r'on', action, re.I):
        cmds.append("cprod -A {} -c 'test xfp {} laser on'".format(pfe, index))
    else:
        cmds.append("cprod -A {} -c 'test xfp {} laser off'".format(pfe, index))

    return cmds


def _check_sonet_xfp_laser(dh, ifd, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    index = _get_xfp_index(dh, ifd)

    res = dh.vty(command="show xfp {} alarm".format(index), destination=get_pfe(dh, ifd)).response()

    state = ''

    if re.search(r'^\s+Tx power low warn:\s+\d+\s+Clear', res, re.M):
        if kwargs.get('debug_log_on'):
            dh.log(message='{}: Laser state is ON for interface: {}'.format(func_name(), ifd), \
                    level='info')
        return 'on'
    elif re.search(r'^\s+Tx power low warn:\s+\d+\s+Set', res, re.M):
        if kwargs.get('debug_log_on'):
            dh.log(message='{}: Laser state is OFF for interface: {}'.format(func_name(), ifd), \
                    level='info')
        return 'off'
    else:
        if kwargs.get('debug_log_on'):
            dh.log(message='{}: Problem getting the laser state of ifd {}'.format(func_name(), \
                    ifd), level='error')
        return None


def _set_t5e_10ge_sfpp_laser_old(dh, ifd, action='off', **kwargs):
    '''
    No index needed for t5e laser
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    ### May be able to get this from somewhere else ####
    match = re.match(r'\w+-(\d+)/(\d+)/(\d+)(.*)', ifd)

    if match:
        pic_slot = match.group(2)
        port = match.group(3)
    else:
        t.log('error', 'cannot find pic slot/port')
        return None

    cmds = []

    pfe = get_pfe(dh, ifd)

    if action == 'on':
        cmds.append("cprod -A {} -c 'set parser security 10'".format(pfe))
        cmds.append("cprod -A {} -c 'test t5e-pic select {}'".format(pfe, pic_slot))
        cmds.append("cprod -A {} -c 'test t5e-pic laser-control link {} on'".format(pfe, port))
    elif action == 'off':
        cmds.append("cprod -A {} -c 'set parser security 10'".format(pfe))
        cmds.append("cprod -A {} -c 'test t5e-pic select {}'".format(pfe, pic_slot))
        cmds.append("cprod -A {} -c 'test t5e-pic laser-control link {} off 0'".format(pfe, port))
    elif re.match(r'flap|bounce', action, re.I):
        msec = float(kwargs.get('interval', 5)) * 1000
        cmds.append("cprod -A {} -c 'set parser security 10'".format(pfe))
        cmds.append("cprod -A {} -c 'test t5e-pic select {}'".format(pfe, pic_slot))
        cmds.append("cprod -A {} -c 'test t5e-pic laser-control link {} off {}'".\
                                format(pfe, port, int(msec)))
    else:
        if kwargs.get('debug_log_on'):
            dh.log(message='{}: unknown action: {}'.\
                    format(func_name(), action), level='error')
        return None

    return cmds


def _set_t5e_10ge_sfpp_laser(dh, ifd, action='off', **kwargs):
    '''
    No index needed for t5e laser
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    ### May be able to get this from somewhere else ####
    match = re.match(r'\w+-(\d+)/(\d+)/(\d+)(.*)', ifd)
    pic_slot = ''
    port = ''

    if match:
        pic_slot = match.group(2)
        port = match.group(3)
    else:
        t.log('error', 'cannot find pic slot/port')
        return None

    if re.match(r'on', action, re.I):
        full_cmd = '\n'.join(['set parser security 10',
                              'test t5e-pic select {}'.format(pic_slot),
                              'test t5e-pic laser-control link {} on'.format(port)])
        dh.vty(command=full_cmd, destination=get_pfe(dh, ifd))
    elif re.match(r'off', action, re.I):
        full_cmd = '\n'.join(['set parser security 10',
                              'test t5e-pic select {}'.format(pic_slot),
                              'test t5e-pic laser-control link {} off 0'.format(port)])
        dh.vty(command=full_cmd, destination=get_pfe(dh, ifd))
    elif re.match(r'flap|bounce', action, re.I):
        msec = float(kwargs.get('interval', 5)) * 1000
        full_cmd = '\n'.join(['set parser security 10',
                              'test t5e-pic select {}'.format(pic_slot),
                              'test t5e-pic laser-control link {} off {}'.\
                                format(port, int(msec))])
        dh.vty(command=full_cmd, destination=get_pfe(dh, ifd))
    else:
        if kwargs.get('debug_log_on'):
            dh.log(message='{}: unknown action: {}'.\
                    format(func_name(), action), level='error')
        return None


def _set_agent_smith_laser(dh, ifd, action='off', **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    try:
        index = _get_bcm_index(dh, ifd)
    except:
        dh.log(message='{}: no agent_smith index found for interface: {}'\
               .format(func_name(), ifd), level='error')
        return True

    pfe = get_pfe(dh, ifd)

    cmds = []

    if re.match('on', action):
        cmds.append("cprod -A {} -c 'test bcm8747 {} power on'".format(pfe, index))
    elif re.match('off', action):
        cmds.append("cprod -A {} -c 'test bcm8747 {} power off'".format(pfe, index))
    else:
        if kwargs.get('debug_log_on'):
            dh.log(message='{}: unknown action: {}'.format(func_name(), action), level='error')
        return None

    return cmds


def _get_bcm_index(dh, ifd):
    '''
    - check if the index is cached under dh.if_info['index'] first
    - dh_info, go to pfe and find all pic index on it, and save them for reuse
    '''

    slot = re.sub(r'\w+-', '', ifd)

    if not (dh.if_info.get('index') and dh.if_info['index'].get(slot)):
        res = dh.vty(command='show bcm8747 all', destination=get_pfe(dh, ifd)).response()
        for line in res.split('\n'):
            match = re.search(r'^\s*(\d+)\s+(\d+/\d+/\d+)', line)
            if match:
                index = match.group(1)
                pic_slot = match.group(2)
                config_utils.nested_set(dh.if_info, ['index', pic_slot], index)

    return dh.if_info['index'][slot]


def _check_agent_smith_laser(dh, ifd, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    try:
        index = _get_bcm_index(dh, ifd)
    except:
        dh.log(message='{}: no bcm8747 index found for interface: {}'.format(func_name(), ifd), \
                        level='error')

    res = dh.vty(command="show bcm8747 {}".format(index), \
                    destination=get_pfe(dh, ifd)).response()


    if re.search(r'\d+\s+ON', res, re.M):
        dh.log(message='{}: Laser state is ON for interface: {}'.format(func_name(), ifd), \
                        level='debug')
        return 'on'
    elif re.search(r'\d+\s+OFF', res, re.M):
        dh.log(message='{}: Laser state is OFF for interface: {}'.format(func_name(), ifd), \
                        level='debug')
        return 'off'
    else:
        dh.log(message='{}: Problem getting the laser state of ifd {}'.format(func_name(), ifd), \
                        level='error')
        return None


def _set_mtip_gpcs_laser(dh, ifd, action='off', **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    if ifd:
        index = _get_mtip_gpcs_index(dh, ifd)
    else:
        dh.log(message='{}: no mtip_gpcs index found for interface: {}'.format(func_name(), ifd), \
                        level='error')

    if re.match('on', action):
        full_cmd = '\n'.join(['set parser security 10',
                              'test mtip-gpcs {} register write 0 0x1140'.format(index)])
        dh.vty(command=full_cmd, destination=get_pfe(dh, ifd))
    elif re.match('off', action):
        full_cmd = '\n'.join(['set parser security 10',
                              'test mtip-gpcs {} register write 0 0x1d40'.format(index)])
        dh.vty(command=full_cmd, destination=get_pfe(dh, ifd))
    else:
        dh.log(message='{} :mtip_gpcs laser command not sent'.format(func_name(), level='error'))


def _get_mtip_gpcs_index(dh, ifd):
    '''
    - check if the index is cached under dh.if_info['index'] first
    - dh_info, go to pfe and find all pic index on it, and save them for reuse
    '''
    slot = re.sub(r'\w+-', '', ifd)

    if not (dh.if_info.get('index') and dh.if_info['index'].get(slot)):
        res = dh.vty(command='show mtip-gpcs summary', destination=get_pfe(dh, ifd)).response()
        for line in res.split('\n'):
            match = re.search(r'\s+(\d+)\s+mtip_gpcs\.(\d+).(\d+).(\d+)\s+', line)
            if match:
                index = match.group(1)
                pic_slot = '/'.join([match.group(2), match.group(3), match.group(4)])
                config_utils.nested_set(dh.if_info, ['index', pic_slot], index)

    return dh.if_info['index'][slot]


def _check_mtip_gpcs_laser(dh, ifd, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    try:
        index = _get_mtip_gpcs_index(dh, ifd)
    except:
        dh.log(message='{}: no mtip_gpcs index found for interface: {}'.format(func_name(), ifd), \
                        level='error')

    res = dh.vty(command="show mtip-gpcs {} registers".format(index), \
                    destination=get_pfe(dh, ifd)).response()

    if re.search(r'\s+control : 0x00001140', res):
        dh.log(message='{}: Laser state is ON for interface: {}'.format(func_name(), ifd), \
                        level='info')
        return 'on'
    elif re.search(r'\s+control : 0x00001d40', res):
        dh.log(message='{}: Laser state is OFF for interface: {}'.format(func_name(), ifd), \
                        level='info')
        return 'off'
    else:
        dh.log(message='{}: Problem getting the laser state of ifd {}'.format(func_name(), ifd), \
                        level='warn')
        return None


def _set_cfp_laser(dh, ifd, action='off', **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    try:
        index = _get_cfp_index(dh, ifd)
    except:
        dh.log(message='{}: no cfp index found for interface: {}'.format(func_name(), ifd), \
                        level='error')
        return True

    cmds = []

    pfe = get_pfe(dh, ifd)

    if re.match('on', action, re.I):
        cmds.append("cprod -A {} -c 'test cfp {} laser on'".format(pfe, index))
    elif re.match('off', action, re.I):
        cmds.append("cprod -A {} -c 'test cfp {} laser off'".format(pfe, index))

    return cmds


def _get_cfp_index(dh, ifd):
    '''
    - check if the index is cached under dh.if_info['index'] first
    - if not, go to pfe and find all pic index on it, and save them for reuse
    '''
    slot = re.sub(r'\w+-', '', ifd)

    if not (dh.if_info.get('index') and dh.if_info['index'].get(slot)):
        res = dh.vty(command='show cfp list', destination=get_pfe(dh, ifd)).response()
        for line in res.split('\n'):
            match = re.search(r'^\s*(\d+)\s+cfp\d?-(\d+/\d+/\d+)', line)
            if match:
                index = match.group(1)
                pic_slot = match.group(2)
                config_utils.nested_set(dh.if_info, ['index', pic_slot], index)

    return dh.if_info['index'][slot]


def _check_cfp_laser(dh, ifd, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    try:
        index = _get_cfp_index(dh, ifd)
    except:
        dh.log(message='{}: no cfp index found for interface: {}'.format(func_name(), ifd), \
                        level='error')

    res = dh.vty(command="show cfp {} alarms".format(index), \
                        destination=get_pfe(dh, ifd)).response()

    if re.search(r'^\s+Tx laser disable:\s+\d+\s+Clear', res, re.M):
        dh.log(message='{}: Laser state is ON for interface: {}'.format(func_name(), ifd), \
                        level='info')
        return 'on'
    elif re.search(r'^\s+Tx laser disable:\s+\d+\s+Set', res, re.M):
        dh.log(message='{}: Laser state is OFF for interface: {}'.format(func_name(), ifd), \
                        level='info')
        return 'off'
    else:
        dh.log(message='{}: Problem getting the laser state of ifd {}'.format(func_name(), ifd), \
                        level='warn')
        return None


def _set_cmic_laser(dh, ifd, action='off', **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    match = re.match(r'\w+-(\d+)/(\d+)/(\d+)', ifd)
    if match:
        pic_index = match.group(2)
        if_index = match.group(3)
    else:
        dh.log(message='No CMIC laser IFD match', level='error')
        return True

    cmds = []

    pfe = get_pfe(dh, ifd)

    if action == 'on':
        cmds.append("cprod -A {} -c 'test cmic {} {} laser on'".format(pfe, pic_index, if_index))
    else:
        cmds.append("cprod -A {} -c 'test cmic {} {} laser off'".format(pfe, pic_index, if_index))

    return cmds


def _check_cmic_laser(dh, ifd, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    match = re.match(r'\w+-(\d+)/(\d+)/(\d+)', ifd)
    if match:
        pic_index = match.group(2)
        if_index = match.group(3)
    else:
        dh.log(message='{}: no pic/if index found for interface: {}'.format(func_name(), ifd), \
                        level='error')
        return None

    res = dh.vty(command="show cmic {} info".format(pic_index), \
                            destination=get_pfe(dh, ifd)).response()

    if re.search(r'\s+({})\s+ON\s+\w+'.format(if_index), res):
        if kwargs.get('debug_log_on'): dh.log(message='{}: Laser state is ON for interface: \
                        {}'.format(func_name(), ifd), level='info')
        return 'on'
    elif re.search(r'\s+({})\s+OFF\s+\w+'.format(if_index), res):
        if kwargs.get('debug_log_on'): dh.log(message='{}: Laser state is OFF for \
                        interface: {}'.format(func_name(), ifd), level='info')
        return 'off'
    else:
        if kwargs.get('debug_log_on'): dh.log(message='{}: Problem getting the \
                    laser state of ifd {}, moving on...'.format(func_name(), ifd), level='warn')
        return None


def _set_qsfp_laser(dh, ifd, action='off', **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    index = None

    try:
        index = _get_qsfp_index(dh, ifd)
    except:
        dh.log(message='{}: no qsfp index found for interface: {}'.format(func_name(), ifd))

    if index is None:
        try:
            return _set_qfx_sfp_laser(dh, ifd, action, **kwargs)
        except:
            dh.log(message='{}: no qsfp index found or no sfp for: {}'.format(func_name(), ifd), \
                        level='error')
            return None

    cmds = []

    pfe = get_pfe(dh, ifd)

    if re.match(r'^\w+-\d+/\d+/\d+\:\d+$', ifd): ## Handle the 10GE QSFP with channel
        channel = re.sub(r'\w+-\d+/\d+/\d+\:', '', ifd)
        if action == 'on':
            cmds.append("cprod -A {} -c 'test qsfp {} chan {} laser-on'".format(pfe, \
                                                                index, channel))
        else:
            cmds.append("cprod -A {} -c 'test qsfp {} chan {} laser-off'".format(pfe, \
                                                                index, channel))
    elif re.match(r'^\w+-\d+/\d+/\d+$', ifd): ## Handle the 100GE QSFP - no channel
        if action == 'on':
            cmds.append("cprod -A {} -c 'test qsfp {} laser on'".format(pfe, index))
        else:
            cmds.append("cprod -A {} -c 'test qsfp {} laser off'".format(pfe, index))
    else:
        t.log('error', 'No IFD match for QSFP laser command')
        return None

    return cmds


def _get_qsfp_index(dh, ifd, **kwargs):
    '''
    - check if the index is cached under dh.if_info['index'] first
    - if not, go to pfe and find all pic index on it, and save them for reuse
    '''
    if kwargs.get('debug_log_on'): t.log('debug', func_name())

    match = re.match(r'\w+-(\d+/\d+/\d+)', ifd)
    if match:
        slot = match.group(1)

    if not (dh.if_info.get('index') and dh.if_info['index'].get(slot)):
        res = dh.vty(command='show qsfp list', destination=get_pfe(dh, ifd)).response()
        for line in res.split('\n'):
            match = re.search(r'^\s*(\d+)\s+qsfp-(\d+/\d+/\d+)', line)
            if match:
                index = match.group(1)
                pic_slot = match.group(2)
                config_utils.nested_set(dh.if_info, ['index', pic_slot], index)

    if (dh.if_info.get('index') and dh.if_info['index'].get(slot)):
        return dh.if_info['index'][slot]


def _set_qfx_sfp_laser(dh, ifd, action, **kwargs):
    '''
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    match = re.match(r'\w+-(\d+)/(\d+)/(\d+)', ifd)
    if match:
        pic_index = match.group(2)
        if_index = match.group(3)

    cmds = []

    pfe = get_pfe(dh, ifd)

    if re.match('on', action):
        cmds.append("cprod -A {} -c 'set cmqfx xcvr insert pic {} port {}'".format(pfe, \
                                                                    pic_index, if_index))
    elif re.match('off', action):
        cmds.append("cprod -A {} -c 'set cmqfx xcvr remove pic {} port {}'".format(pfe, \
                                                                    pic_index, if_index))
    else:
        elog('error', 'No sfp based IFD found')

    return cmds



def _set_picd_laser(dh, ifd, action='off', **kwargs):
    '''
    _set_picd_laser
    Laser off/on for EVO based devices
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    tag = get_dh_tag(dh)
    name = get_dh_name(dh)

    match = re.match(r'\w+-(\d+)/(\d+)/(\d+)(.*)', ifd)

    if match:
        fpc_slot = match.group(1)
        pic_slot = match.group(2)
        port = match.group(3)
    else:
        t.log('error', 'cannot find pic slot/port')
        return None

    if kwargs.get('initial_action'):
        if kwargs['initial_action'] == 'flap': ## keeping from oir_enable multiple times during multiple flap's.
            if dh.device_info.get('oir_enable'):
                t.log('debug', 'OIR already enabled for action=flap.')
            else:
                cli_pfe(dh, cmd='test picd optics fpc_slot {} pic_slot {} port {} cmd oir_enable'.format(fpc_slot, pic_slot, port))
                dh.device_info['oir_enable'] = True
        else:
            cli_pfe(dh, cmd='test picd optics fpc_slot {} pic_slot {} port {} cmd oir_enable'.format(fpc_slot, pic_slot, port))

    if re.match(r'on', action, re.I):
        cli_pfe(dh, cmd='test picd optics fpc_slot {} pic_slot {} port {} cmd laser-on'.format(fpc_slot, pic_slot, port))
    elif re.match(r'off', action, re.I):
        cli_pfe(dh, cmd='test picd optics fpc_slot {} pic_slot {} port {} cmd laser-off'.format(fpc_slot, pic_slot, port))
    else:
        if kwargs.get('debug_log_on'):
            dh.log(message='{}: unknown action: {}'.\
                    format(func_name(), action), level='error')
        return None

def check_interface_state(dh, interface, **kwargs):
    """
    """
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    num_act = ''
    num_act_up_list = []
    num_act_down_list = []
    num_admin_down_list = []
    num_not_found_list = []

    status = True

    ifd_list = interface_handler_to_ifd(device=get_dh_tag(dh), \
                                           interface=interface)

    elog('*** Post Event: Check interface state: {}({} / {}) interface(s): {}'\
         .format(get_dh_tag(dh), get_dh_name(dh), dh.get_model(), nice_string(ifd_list)))

    for intf in ifd_list:
        #AE link processing
        is_ae = False
        if (isinstance(nice_string(intf), str)):
            if (nice_string(intf).startswith('ae')):
                is_ae = True
        elif intf.startswith('ae'):
            is_ae = True

        if is_ae:
            if kwargs.get('member_link_percentage'):
                pick_links_value = 'mlp_{}_pick_links'.format(kwargs['member_link_percentage'])
            elif kwargs.get('num_of_member_links'):
                pick_links_value = 'nml_{}_pick_links'.format(kwargs['num_of_member_links'])
            elif kwargs.get('member_link_list'):
                pick_links_value = 'mll_{}_pick_links'.format(intf)
            else:
                pick_links_value = 'minlink_{}_pick_links'.format(intf)
                
            ifd_list = dh.if_info['ae'][intf][pick_links_value]

    for x, ifname in enumerate(ifd_list, 1):
        num_act = x
        cmd = 'show interfaces {} terse media | except Interface'.format(ifname)
        res = dh.cli(command=cmd).response()
        if re.match(r'\w+-\d+/\d+/\d+(\:\d+\s+up\s+up|\s+up\s+up)', res):
            num_act_up_list.append(ifname)
        elif re.match(r'\w+-\d+/\d+/\d+(\:\d+\s+up\s+down|\s+up\s+down)', res):
            num_act_down_list.append(ifname)
        elif re.match(r'\w+-\d+/\d+/\d+(\:\d+\s+down\s+down|\s+down\s+down)', res):
            elog('warn', '{}: Interface: {} admin down...'.format(get_dh_name(dh), ifname))
            num_admin_down_list.append(ifname)
        elif re.search('not\s+found', res):
            elog('warn', '{}: Interface: {} not found...'.format(get_dh_name(dh), ifname))
            num_not_found_list.append(ifname)
        else:
            elog('error', '*** {}: Did not get Interface: {} status.'.format(get_dh_name(dh), ifname))
            num_not_found_list.append(ifname)

    if num_act_down_list:
        status = False
        elog('*** {}:Interface state summary:\n*** Total Interfaces: {}\n*** UP: {}\n*** DOWN: {}\n*** ADMIN: {}\n*** NOT FOUND: {}\n'\
             .format(get_dh_name(dh), nice_string(num_act), nice_string(num_act_up_list), \
                     nice_string(num_act_down_list), nice_string(num_admin_down_list), \
                        nice_string(num_not_found_list)))
    elif (num_admin_down_list or num_not_found_list):
        elog('error', '*** {}:Interface state summary:\n*** Total Interfaces: {}\n*** UP: {}\n*** DOWN: {}\n*** ADMIN DOWN: {}\n*** NOT FOUND: {}\n'\
             .format(get_dh_name(dh), nice_string(num_act), nice_string(num_act_up_list), \
                     nice_string(num_act_down_list), nice_string(num_admin_down_list), \
                        nice_string(num_not_found_list)))
    else:
        elog('*** {}:Interface state summary:\n*** Total Interfaces: {}\n*** UP: {}\n'.format(get_dh_name(dh), num_act, nice_string(num_act_up_list)))

    return status

