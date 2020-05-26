"""
Created on Dec 2, 2016

@author: Terralogic Team
"""
import re
import datetime
import traceback
import ast
from pprint import pprint
import time
from time import sleep
import jxmlease
from jnpr.toby.hldcl.unix.unix import Unix

CHASSIS_FRU = {
    'm5': {'re': 1, 'fpc': 1, 'pem': 2, 'feb': 1, 'fan': 4},
    'm7i': {'re': 1, 'fpc': 2, 'pem': 2, 'cfeb': 1, 'fan': 4},
    'm10': {'re': 1, 'fpc': 2, 'pem': 2, 'feb': 1, 'fan': 4},
    'm10i': {'re': 2, 'fpc': 2, 'pem': 2, 'cfeb': 2, 'fan': 16},
    'm20': {'re': 2, 'fpc': 4, 'pem': 2, 'ssb': 2, 'fan': 4},
    'm40': {'re': 1, 'fpc': 8, 'pem': 2, 'scb': 1, 'fan': 4},
    'm40e': {'re': 2, 'fpc': 8, 'pem': 2, 'mcs': 2, 'sfm': 2, 'pcg': 2,
             'fan': 7},
    'm120': {'re': 2, 'fpc': 6, 'pem': 2, 'cb': 2, 'feb': 6, 'fan': 32,
             'fabric plane': 4, 'fabric control-board': 2},
    'mx150': {'re': 1, 'fpc': 1, 'pem': 1, 'fan': 2},
    'mx960': {'re': 2, 'fpc': 12, 'pem': 4, 'cb': 2, 'fan': 12,
              'fabric plane': 6, 'fabric control-board': 3},
    'mx240': {'re': 2, 'fpc': 3, 'pem': 4, 'cb': 1, 'fan': 3,
              'fabric plane': 4, 'fabric control-board': 2},
    'mx480': {'re': 2, 'fpc': 6, 'pem': 4, 'cb': 1, 'fan': 6,
              'fabric plane': 4, 'fabric control-board': 2},
    'm160': {'re': 2, 'fpc': 8, 'pem': 2, 'mcs': 2, 'sfm': 4, 'pcg': 2,
             'fan': 7},
    'm320': {'re': 2, 'fpc': 8, 'pem': 4, 'cb': 2, 'sib': 4, 'fan': 15},
    't320': {'re': 2, 'fpc': 8, 'pem': 2, 'cb': 2, 'sib': 3, 'scg': 2,
             'spmb': 2, 'fan': 17},
    't640': {'re': 2, 'fpc': 8, 'pem': 2, 'cb': 2, 'sib': 5, 'scg': 2,
             'spmb': 2, 'fan': 20},
    't1600': {'re': 2, 'fpc': 8, 'pem': 2, 'cb': 2, 'sib': 5, 'scg': 2,
              'spmb': 2, 'fan': 20},
    't4000': {'re': 2, 'fpc': 8, 'pem': 2, 'cb': 2, 'sib': 5, 'scg': 2,
              'spmb': 2, 'fan': 20},
    'tx matrix': {'re': 2, 'fpc': 8, 'pem': 2, 'cb': 2, 'sib': 5, 'scg': 2,
                  'spmb': 2, 'fan': 20},
    'txp': {'re': 2, 'fpc': 8, 'pem': 2, 'cb': 2, 'sib': 5, 'scg': 2,
            'spmb': 2, 'fan': 20},
    'irm': {'re': 1, 'fpc': 2, 'pem': 1, 'cfeb': 1},
    'j4350': {'fan': 3},
    'j6350': {'fan': 3},
    'psd': {'re': 2, 'fpc': 8},
    'a40': {'re': 1, 'fpc': 12, 'pem': 4, 'cb': 2, 'fan': 12},
    'srx5800': {'re': 1, 'fpc': 12, 'pem': 4, 'cb': 2, 'fan': 12},
    'a20': {'re': 1, 'fpc': 6, 'pem': 2, 'cb': 1, 'fan': 6},
    'srx5600': {'re': 1, 'fpc': 6, 'pem': 2, 'cb': 1, 'fan': 6},
    'srx5400': {'re': 1, 'fpc': 3, 'pem': 2, 'cb': 1, 'fan': 3},
    'a15': {'re': 1, 'fpc': 3, 'pem': 2, 'cb': 1, 'fan': 3},
    'a10': {'re': 1, 'fpc': 13, 'pem': 2, 'fan': 10},
    'srx3600': {'re': 1, 'fpc': 13, 'pem': 2, 'fan': 10},
    'a2': {'re': 1, 'fpc': 8, 'pem': 1, 'fan': 4},
    'srx3400': {'re': 1, 'fpc': 8, 'pem': 1, 'fan': 4},
    'srx1400': {'re': 1, 'fpc': 3, 'pem': 1, 'fan': 2},
    'srx345': {'re': 1, 'fpc': 1, 'pem': 1, 'fan': 4},
    'ex8208': {'re': 2, 'fpc': 8, 'pem': 6, 'cb': 2, 'fan': 12,
               'fabric plane': 12, 'fabric control-board': 3, 'lcd': 1},
    'ex8216': {'re': 2, 'fpc': 16, 'pem': 6, 'cb': 2, 'fan': 18,
               'fabric plane': 8, 'fabric control-board': 8, 'lcd': 1},
    'ptx5000': {'re': 2, 'fpc': 8, 'pdu': 2, 'psm': 8, 'cb': 2,
                'sib': 9, 'ccg': 2, 'spmb': 2, 'fan': 26},
    'amx1100': {'re': 2, 'fpc': 3, 'pem': 2, 'afeb': 1, 'fan': 5},
    'mx104': {'re': 2, 'fpc': 3, 'pem': 2, 'afeb': 1, 'fan': 5},
    'mx204': {'re': 1, 'cb': 1, 'pem': 2, 'fpc': 1, 'fan': 3},
    'mx2020': {'midplane': 2, 'pmp': 2, 'psm': 18, 'pdm': 4, 're': 2,
               'cb': 2, 'spmb': 2, 'sfb': 8, 'fpc': 20, 'adc': 20,
               'fan': 120},
    'mx2010': {'midplane': 1, 'pmp': 1, 'psm': 9, 'pdm': 2, 're': 2,
               'cb': 2, 'spmb': 2, 'sfb': 8, 'fpc': 10, 'adc': 10,
               'fan': 120},
    'mx10003': {'re': 2, 'fpc': 2, 'cb': 2, 'pem': 6, 'fan': 4},
    'mx10008': {'re': 2, 'fpc': 8, 'cb': 2, 'sfb': 6, 'fan': 2},
    'mx10016': {'re': 2, 'fpc': 16, 'cb': 2, 'sfb': 6, 'fan': 2},
    'mx2008': {'midplane': 1, 'psm': 9, 'pdm': 1, 're': 2, 'cb': 2,
               'sfb': 8, 'fpc': 10, 'adc': 10, 'fan': 120},
    'ptx3000': {'re': 2, 'fpc': 8, 'psm': 5, 'cb': 2, 'sib': 9, 'fan': 28},
    'ptx10016': {'re': 2, 'fpc': 16, 'cb': 2, 'sib': 6, 'spmb': 2, 'fan': 21},
    'ptx10008': {'re': 2, 'fpc': 8, 'cb': 2, 'sib': 6, 'fan': 22},
    'ptx10003-160c': {'re': 1, 'fpc': 4, 'sib': 2, 'fan': 10},
    'ptx10003-80c': {'re': 1, 'fpc': 4, 'sib': 2, 'fan': 10},
    'ptx10002-60c': {'re': 1, 'fpc': 2, 'fan': 10},
    'ptx1000': {'re': 1, 'fpc': 2, 'fan': 10},
    'qfx10003-160c': {'re': 1, 'fpc': 4, 'sib': 2, 'fan': 10},
    'qfx10003-80c': {'re': 1, 'fpc': 4, 'sib': 2, 'fan': 10},
    'qfx10008': {'re': 2, 'fpc': 8, 'cb': 2, 'sib': 6, 'fan': 22},
    'qfx10016': {'re': 2, 'fpc': 16, 'cb': 2, 'sib': 6, 'fan': 42},
    'qfx5200': {'re': 1, 'fpc': 1, 'cb':0 , 'sib': 0, 'fan': 6},
    'qfx5120': {'re': 1, 'fpc': 1, 'cb':0 , 'sib': 0, 'fan': 5},
    'qfx5110': {'re': 1, 'fpc': 1, 'cb':0 , 'sib': 0, 'fan': 5},
    'acx5096': {'re': 1, 'fpc': 1, 'fan': 3},
    'ex4300-48p': {'re': 1, 'fpc': 1, 'fan': 2},
    'ex3400-24t': {'re': 1, 'fpc': 1, 'fan': 2},
    'qfx5100-48s-6q': {'re': 1, 'fpc': 1, 'fan': 5},
    'ex9251': {'re': 1, 'fpc': 1, 'fan': 3},
    'ACX5448-DC-AFO': {'re': 1, 'fpc': 1, 'fan': 6},
    'acx710': {'midplane': 1, 're': 1, 'fpc': 1, 'fan': 1},
    'r6675': {'midplane': 1, 're': 1, 'fpc': 1, 'fan': 1}
}


CHECK_HARDWARE = True
CHECK_CRAFT = True
CHECK_DB = True
CHECK_MEMORY = True
CHECK_INTERFACE = True
CHECK_ALARM = True
CHECK_LED = True
TIMEOUT = 60


def check_chassis_alarm(device, **kwargs):
    """
    Robot Usage Example  :
    ${device_object}  =  Get Handle  resource=r1
    ${alarm_dict}  =  Create Dictionary   class=Major
    ...     description=PEM 2 Not OK   short-description=PEM 2 Not OK
    ...     time=2017-02-16 02:50:50 PST    type=Chassis
    ${alarm} =  Create List    ${alarm_dict}
    &{kwargs} =  Create Dictionary chassis='sfc 0' count=${1}  alarm=${alarm} check_count=${5}  class='Major'
    ${result} =  Check Chassis Alarm   device=${device_object}  &{kwargs}

    Chassis health by checking chassis alarm

    :param device:
        **REQUIRED** Device handle
    :param chassis:
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :params alarm :
        **REQUIRED** Regular expression or list of strings or list
        of dictionary of alarm description. The dictionary is same as
        get_chassis_alarm. String is used as regular expression for
        alarm checking.
    :params class :
        **REQUIRED** Major or Minor
    :params count :
        **REQUIRED** Number of alarm count
    :params check_count :
        **OPTIONAL** Check count. Default is 1
    :params check_interval :check_alarm
        **OPTIONAL** Wait time before next retry. Default 10 seconds

     :return :
     TRUE if alarm check passed
     FALSE if alarm check failed
    """
    valid_keys = ['chassis','alarm', 'class_alarm', 'count', 'check_count', 'check_interval']
    required_keys = ['alarm','class_alarm','count']
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    alarm = kwargs.get('alarm')
    class_alarm = kwargs.get('class_alarm')
    count = kwargs.get('count')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model().lower()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s function %s..." % (sub, str(kwargs)),
               level="debug")
    # if model is "TX MATRIX|TXP" and chassis is not defined
    # then it gets chassis values from get_chassis_list
    if re.search('^TX MATRIX|TXP$', model, re.I) and (not chassis):
        for chassis_list in get_chassis_list(device):
            device.log(message=" %s : checking for chassis(%s) ..."
                       % (sub, chassis_list), level="debug")

            if isinstance(alarm, dict):
                alarm_ = alarm[chassis_list]
            else:
                alarm_ = alarm
            # for each chassis value in the get_chassis_list and
            # alarm value it - calls check_chassis_alarm()
            # if check_chassis_alarm() return True then checking alarm
            # for that particular chassis is passed
            # otherwise checking is failed
            if check_chassis_alarm(
                    device,
                    chassis=chassis_list,
                    class_alarm=class_alarm,
                    alarm=alarm_,
                    count=count,
                    check_count=check_count,
                    check_interval=check_interval):
                device.log(message="%s: passed for chassis(%s)"
                           % (sub, chassis_list), level="debug")
            else:
                device.log(message="%s: failed for chassis(%s)"
                           % (sub, chassis_list), level="warn")

        return True
    # if model is "psd" and alarm value is given as dictionary
    if re.search(r'^psd', model, re.I) and isinstance(alarm, dict):
        for alarm_keys in alarm.keys():
            device.log(message="%s: checking for chassis(%s) ..."
                       % (sub, alarm_keys), level="debug")
            alarm_ = alarm[alarm_keys]
            # for each chassis value of alarm it calls check_chassis_alarm()
            # if check_chassis_alarm() return True then checking alarm
            # is passed otherwise checking is failed
            if check_chassis_alarm(
                    device,
                    chassis=chassis,
                    class_alarm=class_alarm,
                    alarm=alarm_,
                    count=count,
                    check_count=check_count,
                    check_interval=check_interval):
                device.log(message="%s: passed for chassis(%s)"
                           % (sub, alarm_keys), level="debug")
            else:
                device.log(message="%s: failed for chassis(%s)"
                           % (sub, alarm_keys), level="warn")
        return True
    # if alarm value is given as list
    if isinstance(alarm, list):
        # if alarm value contain dictionary
        if isinstance(alarm[0], dict):
            # for each alarm it calls check_chassis_alarm()
            for alarm_chassis in alarm:
                # if check_chassis_alarm() is not True it return False
                #     otherwise returns True
                if not check_chassis_alarm(device,
                                           chassis=chassis,
                                           class_alarm=alarm_chassis['class'],
                                           alarm=alarm_chassis['description'],
                                           count=count):
                    return False
        # if alarm value is not dictionary
        else:
            check = True
            for chassis_alarm in alarm:
                if not check_chassis_alarm(
                        device,
                        chassis=chassis,
                        class_alarm=class_alarm,
                        alarm=chassis_alarm,
                        count=count):
                    check = False
            if not check:
                return False
        return True
    for i in range(0, check_count):
        check_info = "count (%s), interval(%s)" % (i, check_interval)
        if i > 0:
            sleep(check_interval)
        check_alarm = get_chassis_alarm(device, chassis=chassis)
        if isinstance(check_alarm[0], list):
           check_alarm = check_alarm[0] 
        # Check count option
        if isinstance(check_alarm, list):
            current_count = len(check_alarm)
        if current_count == count:
            device.log(message="%s: alarm count(%s) check passed"
                       % (sub, current_count),
                       level="debug")
        else:
            device.log(
                message="%s: incorrect alarm count(%s), should be %s" %
                (sub, current_count, count), level="warn")
            continue

        for alarm_hash in check_alarm:
            check_ok = True
            show_data(device, alarm_hash, "%s: checking alarm entry:" % sub)
            test_info = "%s: check alarm class (%s),%s" % (
                sub, class_alarm, check_info)
            alarm_class = alarm_hash["class"]
            alarm_class = __chop(device, alarm_class)
            if re.search('^'+alarm_class+'$', class_alarm, re.I):
                device.log(message="%s: %s passed" % (sub, test_info),
                           level="debug")
            else:
                device.log(message="%s: %s failed" % (sub, test_info),
                           level="warn")
                check_ok = False
            # checks for alarm description
            show_data(device, alarm, "%s: alarm" % sub)
            test_info = "'%s': check alarm description ('%s'), '%s'"\
                        % (sub, alarm, check_info)
            matched1 = re.search(alarm, alarm_hash['description'], re.I)
            matched2 = re.search(alarm,
                                 alarm_hash['short-description'], re.I)
            alarm_hash_val = alarm_hash['short-description']
            if matched1 or alarm_hash_val and matched2:
                device.log(message="%s: %s passed" % (sub, test_info),
                           level="debug")
            else:
                device.log(message="%s: %s failed" % (sub, test_info),
                           level="warn")
                check_ok = False

            if check_ok:
                device.log(message="%s: alarm check passed, %s"
                           % (sub, check_info), level="debug")
                return True
            else:
                device.log(message="%s: alarm check failed, %s"
                           % (sub, check_info), level="warn")
    device.log(message="%s: alarm check failed, %s" % (sub, check_info),
               level="warn")
    return False
# end def check_chassis_alarm


def check_chassis_coredump(device, cmd_type='cli', **kwargs):
    """
    Robot Usage Example :
    ${device_object}  =  Get Handle  resource=r1
    ${result}  =  Check Chassis Coredump   device=${device_object}
    ...    cmd_type='vty'  fru='fpc'  slot=${4}  check_count=${5}

    Checks chassis coredump based on slot and fru type.

    :param device:
        **REQUIRED** Device handle
    :param fru  :
        **REQUIRED** sfm/fpc/ssb/cfeb/spmb or an array
    :param slot :
       **REQUIRED** slot number or an array or a dictionary of slot
    :param check_count :
       **OPTIONAL** Check count (default is 1)
    :param check_interval :
       **OPTIONAL** Wait time before next retry (default 10 seconds)

    :return :
        TRUE if the check passes
        FALSE if check fails
    """
    arg_str = str(kwargs)
    fru = kwargs.get('fru')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    # if slot value is not given it gets slot from get_fru_slots
    if 'slot' in kwargs:
        slot = kwargs.get('slot')
    else:
        slot = get_fru_slots(device, fru=fru, state='Online')
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message=" Inside %s (%s)..." % (sub, arg_str), level="debug")
    # if fru is given as list for every fru value it calls
    #    check_chassis_coredump()
    if isinstance(fru, list):
        for fru_val in fru:
            result = check_chassis_coredump(device,
                                            fru=fru_val,
                                            slot=slot[fru_val],
                                            check_count=check_count,
                                            check_interval=check_interval)
            if result:
                device.log(message="%s : fru (%s) check passed"
                           % (sub, fru_val), level="debug")
            else:
                device.log(message="%s: fru (%s) check failed"
                           % (sub, fru_val), level="warn")
                return False
        return True
    # if slot is given as list for every slot value it calls
    #    check_chassis_coredump()
    if isinstance(slot, list):
        for slot_val in slot:
            result = check_chassis_coredump(device,
                                            fru=fru,
                                            slot=slot_val,
                                            check_count=check_count,
                                            check_interval=check_interval)
            if result:
                device.log(message="%s :fru (%s) check passed for slot (%s)"
                           % (sub, slot_val, slot_val),
                           level="debug")
            else:
                device.log(message="%s: fru (%s) check failed for slot (%s)"
                           % (sub, slot_val, slot_val),
                           level="warn")
                return False
        return True
    # set fru value as the destination for the vty function
    vty_name = fru
    match1 = re.search("^spmb|scb|ssb|feb|cfeb$", fru)
    # if fru values are spmb|scb|ssb|feb|cfeb then no need to check
    if (slot or slot == 0) and match1:
        device.log(message="%s: No need to check fru (%s), slot (%s)"
                   % (sub, fru, slot), level="warn")
        return True
    if cmd_type == 'vty':
        vty_name = fru
        fru_match = re.search("^scb|ssb|feb|cfeb$", fru)
        if not fru_match:
            vty_name += str(slot)
    # if fru values are not scb|ssb|feb|cfeb
    # then append slot to the destination value
    for val in range(0, check_count):
        if cmd_type == 'vty':
            output = device.vty(destination=vty_name, command="show coredump ")
            response = output.response()
        else:
            output = device.cli(command="show system core-dumps")
            response = output.response()
        if not re.search(r'file name\s+: core-.*', response):
            device.log(
                message="%s [time #%s]: check passed on %s" % (sub, val,
                                                               vty_name))
            return True
    device.log(message="%s: check failed on %s" % (sub, vty_name))
    return False
# end def check_chassis_coredump


def check_chassis_database(device, **kwargs):
    """
    Robot Usage Example :
     ${device_object}  =  Get Handle  resource=r1
     ${result}  =  Check Chassis Database   device=${device_object}
     ...    dynamic=${1}  static=${1}  fru='fpc'

    Checks the chassis database.

    :param device:
        **REQUIRED** Device handle
    :param dynamic:
        *OPTIONAL* 1| 0 get dynamic database (default is 1)
    :param static:
        *OPTIONAL* 1| 0 get static database (default is 0)
    :param fru:
        **REQUIRED**  fpc | sib | sfm | pcg | scg | cb | pic or list of them
    :param check_count:
        *OPTIONAL* Check count. Default is 1
    :param check_interval:
        *OPTIONAL* Wait time before next retry. Default 10 seconds

    :return:
        Dynamic:
            TRUE if dynamic db for fru passed
            FALSE if dynamic db for fru failed
        Static:
            TRUE if status db check passes
            FALSE if status db check failes
    """
    valid_keys = ['dynamic', 'static', 'fru', 'check_count',
                  'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    fru = kwargs.get('fru')
    dynamic = kwargs.get('dynamic')
    static = kwargs.get('static')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model().lower()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s function %s..." % (sub, str(kwargs)))
    version = re.search(r'^6.3', device.get_version())
    match = re.match(r'^TX Matrix|TXP$', model, re.I)
    if match or version:
        device.log(message="%s : skip checking due to either verison(<6.4)"
                           " or platform(TX Matrix) NOT supported" % sub,
                   level="warn")
        return True
    if not (dynamic and static):
        dynamic = 1
        static = 1

    for count in range(0, check_count):
        check_pass = True
        device.log(message="Sleep with %s in %ss" % (count, check_interval),
                   level="info")
        sleep(check_interval)
        if not isinstance(dynamic, dict):
            dynamic = get_chassis_database(device, dynamic=1)
            if isinstance(dynamic, dict):
                dynamic = dynamic["dynamic"]
            else:
                device.log(message="%s :dynamic database is NOT dict" % sub,
                           level="warn")
                check_pass = False
                continue
    if not check_pass:
        device.log(message="%s : Checking failed for all fru."
                   % sub, level="warn")
        return False

    if isinstance(fru, list):
        for fru_val in fru:
            if check_chassis_database(device,
                                      dynamic=dynamic,
                                      fru=fru_val):
                device.log(
                    message="%s:dynamic db check for %s passed"
                    % (sub, fru_val), level="debug")
            else:
                device.log(
                    message="%s :dynamic db check for %s failed"
                    % (sub, fru_val), level="warn")
                check_pass = False

        # Final check
        if not check_pass:
            device.log(message="%s : Checking failed for all fru."
                       % sub, level="warn")
            return False

        device.log(message="%s :check passed for all fru"
                   % (sub), level="debug")
        return True

    if fru == 'fan':
        cli_cmd = "show chassis environment | " \
                  "grep fan | grep OK | count"
        response = device.cli(command=cli_cmd).response()
        match = re.search(r'Count: (\d+) lines',
                          response, re.MULTILINE)
        if match:
            if int(match.group(1)) > 0:
                if not isinstance(dynamic[fru], list):
                    device.log(message="%s: fan checking failed, "
                                       "db NOT list" % sub,
                               level="warn")
                    show_data(device, dynamic[fru],
                              "%s: dynamic db for fan= " % sub)
                    return False
            else:
                if isinstance(dynamic[fru], list):
                    device.log(message="%s :fan checking failed, "
                                       "db is array" % sub,
                               level="warn")
                    show_data(device,
                              dynamic[fru],
                              "%s: dynamic db for fan= " % sub)
                    return False
        device.log(message="%s :fan checking passed" % sub,
                   level="debug")
        return True

    fru_status = get_fru_status(device, fru=fru)
    if not isinstance(fru_status, list):
        device.log(message="%s:fru status for fru %s should be list"
                   % (sub, fru), level="warn")
        return False

    device.log(message="%s:checking dynamic database..." % sub,
               level="debug")
    fru_dynamic_db = dynamic[fru]
    if not isinstance(fru_dynamic_db, list):
        fru_dynamic_db = [fru_dynamic_db]

    if len(fru_dynamic_db) > len(fru_status):
        device.log(message="%s : dynamic db has more entries"
                           " than fru status for fru %s" % (sub, fru),
                   level="warn")
        show_data(device, fru_dynamic_db,
                  "%s: fru_dynamic_db= %s"
                  % (sub, len(fru_dynamic_db)))
        show_data(device, fru_status,
                  "%s :fru status= %s"
                  % (sub, len(fru_status)))
        check_pass = False
    for value in range(0, len(fru_status)):
        if not __check_dynamic_db(device, value,
                                  dynamic[fru], fru_status):
            check_pass = False
    if not check_pass:
        device.log(message="%s : Checking failed." % sub,
                   level='warn')
        return False
    return True
# end def check_chassis_database


def check_fan_environment(device, **kwargs):
    """
    Robot Usage Example :
     ${device_object}  =  Get Handle  resource=r1
     ${result}  =  Check Fan Environment   device=${device_object}
     ...    chassis='sfc 0'

    Checks the chassis fan environment based on the model

    :param device:
        **REQUIRED** Device handle
    :params chassis:
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :params env:
        **OPTIONAL** by default it gets value from get_chassis_environment

    :return:
    TRUE if fan environment check passes
    FALSE if fan environment check failes

    """
    valid_keys = ['chassis', 'env']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    if 'env' in kwargs:
        env = kwargs.get('env')
    else:
        env = get_chassis_environment(device, chassis=chassis)
    model = device.get_model()
    arg_str = str(kwargs)
    fans = []
    sub = function_name(device)
    device.log(message="Inside %s(%s) %s..." % (sub, model, arg_str))
    # checks fan env for m5 or m10 model
    if re.search('^m(5|10)$', model):
        fans = ['left fan 1', 'left fan 2', 'left fan 3', 'left fan 4']
    # checks fan env for m7i model
    elif model == 'm7i':
        fans = ['fan 1', 'fan 2', 'fan 3', 'fan 4']
    # checks fan env for m10 model
    elif model == 'm10i':
        fans = ['fan tray 0 fan 1', 'fan tray 0 fan 2', 'fan tray 0 fan 3',
                'fan tray 0 fan 4', 'fan tray 0 fan 5', 'fan tray 0 fan 6',
                'fan tray 0 fan 7', 'fan tray 0 fan 8', 'fan tray 1 fan 1',
                'fan tray 1 fan 2', 'fan tray 1 fan 3', 'fan tray 1 fan 4',
                'fan tray 1 fan 5', 'fan tray 1 fan 6', 'fan tray 1 fan 7',
                'fan tray 1 fan 8']
    # checks fan env for m20 model
    elif model == 'm20':
        fans = ['rear fan', 'front upper fan', 'front middle fan',
                'front bottom fan']
    # checks fan env for m40 model
    elif model == 'm40':
        fans = ['top impeller', 'bottom impeller', 'rear left fan',
                'rear center fan', 'rear right fan']
    # checks fan env for m160 or m40e model
    elif re.search('^(m160|m40e)$', model):
        fans = ['rear bottom blower', 'rear top blower',
                'front top blower', 'fan tray rear left',
                'fan tray rear right', 'fan tray front left',
                'fan tray front right']
    # checks fan env for m120 model
    elif model == 'm120':
        fans = ['front top tray fan 1', 'front top tray fan 2',
                'front top tray fan 3', 'front top tray fan 4',
                'front top tray fan 5', 'front top tray fan 6',
                'front top tray fan 7', 'front top tray fan 8',
                'front bottom tray fan 1', 'front bottom tray fan 2',
                'front bottom tray fan 3', 'front bottom tray fan 4',
                'front bottom tray fan 5', 'front bottom tray fan 6',
                'front bottom tray fan 7', 'front bottom tray fan 8',
                'rear top tray fan 1', 'rear top tray fan 2',
                'rear top tray fan 3', 'rear top tray fan 4',
                'rear top tray fan 5', 'rear top tray fan 6',
                'rear top tray fan 7', 'rear top tray fan 8',
                'rear bottom tray fan 1', 'rear bottom tray fan 2',
                'rear bottom tray fan 3', 'rear bottom tray fan 4',
                'rear bottom tray fan 5', 'rear bottom tray fan 6',
                'rear bottom tray fan 7', 'rear bottom tray fan 8']
    # checks fan env for m320 model
    elif model == 'm320':
        fans = ['top left front fan', 'top right rear fan',
                'top right front fan', 'top left rear fan',
                'bottom left front fan', 'bottom right rear fan',
                'rear fan 1 (top)', 'rear fan 2',
                'rear fan 3', 'rear fan 4', 'rear fan 5',
                'rear fan 6', 'rear fan 7 (bottom)']
    # checks fan env for t320 model
    elif model == 't320':
        fans = ['top left front fan', 'top left middle fan',
                'top left rear fan', 'top right front fan',
                'top right middle fan', 'top right rear fan',
                'bottom left front fan', 'bottom left middle fan',
                'bottom left rear fan', 'bottom right front fan',
                'bottom right middle fan', 'bottom right rear fan',
                'rear tray top fan', 'rear tray second fan',
                'rear tray middle fan', 'rear tray fourth fan',
                'rear tray bottom fan']
    # checks fan env for t640 or t1600 or TX model
    elif re.search('t640|t1600|TX', model):
        fans = ['top left front fan', 'top left middle fan',
                'top left rear fan', 'top right front fan',
                'top right middle fan', 'top right rear fan',
                'bottom left front fan', 'bottom left middle fan',
                'bottom left rear fan', 'bottom right front fan',
                'bottom right middle fan', 'bottom right rear fan',
                'rear tray top fan', 'rear tray second fan',
                'rear tray third fan', 'rear tray fourth fan',
                'rear tray fifth fan', 'rear tray sixth fan',
                'rear tray seventh fan', 'rear tray bottom fan']
    # checks fan env for mx960 or a40 or srx5800 model
    elif re.search('mx960|a40|srx5800', model):
        match = re.search('mx960', model, re.I)
        if match and check_enhance_fantray(device):
            fans = ['top tray fan 1', 'top tray fan 2', 'top tray fan 3',
                    'top tray fan 4', 'top tray fan 5', 'top tray fan 6',
                    'top tray fan 7', 'top tray fan 8', 'top tray fan 9',
                    'top tray fan 10', 'top tray fan 11',
                    'top tray fan 12', 'bottom tray fan 1',
                    'bottom tray fan 2', 'bottom tray fan 3',
                    'bottom tray fan 4', 'bottom tray fan 5',
                    'bottom tray fan 6', 'bottom tray fan 7',
                    'bottom tray fan 8', 'bottom tray fan 9',
                    'bottom tray fan 10', 'bottom tray fan 11',
                    'bottom tray fan 12']
        else:
            fans = ['top tray fan 1', 'top tray fan 2', 'top tray fan 3',
                    'top tray fan 4', 'top tray fan 5', 'top tray fan 6',
                    'bottom tray fan 1', 'bottom tray fan 2',
                    'bottom tray fan 3', 'bottom tray fan 4',
                    'bottom tray fan 5', 'bottom tray fan 6']
    # checks fan env if model is mx240
    elif model == 'mx240':
        fans = ['front fan',
                'middle fan',
                'rear fan']
    # checks fan env if model is mx480 or a15 or a20 or srx5600 or srx5400
    elif re.search('mx480|a15|a20|srx5600|srx5400', model):
        fans = ['top rear fan', 'bottom rear fan',
                'top middle fan', 'bottom middle fan',
                'top front fan', 'bottom front fan']
    # checks fan env if model is a10 or srx3600
    elif re.search('a10|srx3600', model):
        fans = ['fan 1', 'fan 2', 'fan 3', 'fan 4',
                'fan 5', 'fan 6', 'fan 7', 'fan 8',
                'fan 9', 'fan 10']
    # checks fan env if model is a2 or srx3400
    elif re.search('a2|srx3400', model):
        fans = ['fan 1', 'fan 2', 'fan 3',
                'fan 4']
    # checks fan env if model is ex8208
    elif re.search('ex8208', model):
        fans = ['fan 1', 'fan 2', 'fan 3', 'fan 4', 'fan 5', 'fan 6',
                'fan 7', 'fan 8', 'fan 9', 'fan 10', 'fan 11', 'fan 12']
    # checks fan env if model is ex8216
    elif re.search('ex8216', model):
        fans = ['top fan 1', 'top fan 2', 'top fan 3', 'top fan 4',
                'top fan 5', 'top fan 6', 'top fan 7', 'top fan 8',
                'top fan 9', 'bottom fan 1', 'bottom fan 2',
                'bottom fan 3', 'bottom fan 4', 'bottom fan 5',
                'bottom fan 6', 'bottom fan 7', 'bottom fan 8',
                'bottom fan 9']
    else:
        device.log("%s not supports in the %s model " % (sub, model))
        return False
    for fan in fans:
        if fan in env:
            device.log(message="%s: %s found" % (sub, fan),
                       level="info")
        else:
            device.log(message="%s:%s is not found" % (sub, fan),
                       level="error")
    return True
# end def check_fan_environment


def check_chassis_firmware(device, **kwargs):
    """
    Robot Usage Example :
     ${dh} =    Get Handle   resource=r1
     ${kwargs} =    Evaluate    {'version': '6.0b12', 'type_chassis': 'ROM',
     ...    'fru': 'fpc', 'check_count':'5', 'check_interval':'10'}
     ${result} =    Check Chassis Firmware    device=${dh}    &{kwargs}

    Checks the chassis firmware and operating system version

    :param device:
        **REQUIRED** Device handle
    :param fru :
        **REQUIRED** re|fpc|sib|sfm|pcg|scg|cb|pem
    :param type_chassis :
        **REQUIRED** type of fru slot
    :param version:
        **REQUIRED** firmware version
    :param check_count:
         **OPTIONAL** Check count. Default is 1
    :param check_interval:
        **OPTIONAL** Wait time before next retry. Default 10 seconds

    :return:
        TRUE if the version is passed for fru
        FALSE if the version is failed for fru
    """
    valid_keys = ['fru', 'type_chassis', 'version',
                  'check_count', 'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    fru = kwargs.get('fru')
    type_chassis = kwargs.get('type_chassis')
    version = kwargs.get('version')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)))
    # checks whether fru and chassis_type is present or not
    if not (fru and type_chassis):
        device.log(message=" %s : argument fru and type are required" % sub,
                   level="error")
        return False

    for i in range(check_count):
        # Gets the version of the chassis using get_chassis_firmware
        chassis_firmware = get_chassis_firmware(device)
        version_response = chassis_firmware[fru][type_chassis]
        if version in version_response:
            device.log(
                message="%s [time #%s]: version(%s) is passed for fru(%s)"
                % (sub, i, version, fru), level="debug")
            return True
        sleep(check_interval)
    device.log(message="%s: version(%s) is failed for fru(%s)"
               % (sub, version, fru), level="warn")
    return False
# end def check_chassis_firmware


def check_chassis_fan(device, **kwargs):
    """
    Robot Usage Example :
     ${device_object}  =  Get Handle  resource=r1
     ${sample_env_dict}   =  Evaluate  ({'sfc 0':{'top left front fan': {
     ...    'class': 'Fans','comment': 'Spinning at normal speed',
     ...    'status': 'Check'}}})
     ${result}  =  Check Chassis Fan   device=${device_object}
     ...    chassis='sfc 0'  speed='full'  env=${sample_env_dict}
     ...    check_count=${5}

    Check chassis fan speed by doing the following
        -> Checks the fan speed(high, full or normal) or
             displays unknown fan speed message.
        -> Checks fan speed and count for TX Matrix and TXP Matrix router.

    :param device:
        **REQUIRED** Device handle
    :param env :
       **REQUIRED** dictionary for chassis environment
    :params chassis:
       **REQUIRED** Type of chassis (scc | lcc 0|1|2|3 )
    :param speed :
       **REQUIRED** high (or full, full-speed) | normal
    :param check_count :
       **OPTIONAL** Check count for FRU online (default 0 no checking)
    :param check_interval :
       **OPTIONAL** Wait time before next retry (default 10 seconds)
    :params count :
       **OPTIONAL** Number of alarm count or gets value from
                                     chassis.chassis_fru[model][fan]

    :returns:
        TRUE if the log is "INFO" with the content of fan speed info
        FALSE if the log is "ERROR" or "WARN", cannot check fan speed info
    """
    valid_keys = ['chassis', 'env', 'speed', 'check_count', 'count',
                  'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    env = kwargs.get('env')
    speed = kwargs.get('speed')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model()
    count = kwargs.get('count') or CHASSIS_FRU[model.lower()]['fan']
    if check_enhance_fantray(device):
        count = 24
    else:
        count = count
    sub = function_name(device) + " (%s)..." % model
    device.log(message="Inside %s %s" % (sub, str(kwargs)))
    match = re.search('^full(-speed)*|high$', speed, re.I)
    if match:
        speed = 'high'
    elif not re.search('^normal$', speed, re.I):
        device.log(message=" %s : unknown fan speed %s "
                   % (sub, speed), level="error")
        return False
    for value in range(0, check_count):
        check_ok = True
        check_info = "count " + str(value) + \
                     " interval " + str(check_interval)
        if not env:
            env = get_chassis_environment(device, chassis=chassis)
        fans = []
        chassis_env = get_chassis_environment(device)
        if re.search('^TX Matrix$', model, re.I):
            for key in chassis_env['scc'].keys():
                if re.search('fan(?!temp)', key) or re.search('blower(?!temp)',
                                                              key):
                    fans.append(key)
                else:
                    check_ok = False
        elif re.search('^TXP$', model, re.I):
            for key in chassis_env['sfc 0']:
                if re.search('fan(?!temp)', key) or re.search('blower(?!temp)',
                                                              key):
                    fans.append(key)
                else:
                    check_ok = False
        else:
            for key in get_chassis_environment(device):
                if re.search('fan(?!temp)', key) or re.search('blower(?!temp)',
                                                              key):
                    fans.append(key)
                else:
                    check_ok = False

        fan_count = len(fans)
        if fan_count == count:
            device.log(message="%s:fan count (%s) check passed,%s"
                       % (sub, fan_count, check_info), level="debug")
        else:
            device.log(message="%s:incorrect fan count(%s) should be %s, %s"
                       % (sub, fan_count, count, check_info), level="warn")
            env = None
            continue

        if re.search('^TX', model, re.I):
            if re.search('^TX Matrix$', model, re.I):
                pfe = 'scc'
            else:
                pfe = 'sfc 0'

            for fan in fans:
                if "comment" in env[pfe][fan].keys():
                    env_val = True
                else:
                    env_val = False
                    break
                if env_val and re.search(speed + ' speed',
                                         env[pfe][fan]["comment"], re.I):
                    device.log(message="%sfan (%s) is at %s speed,%s "
                               % (sub, fan, speed, check_info),
                               level="debug")
                elif re.search('Check', env[pfe][fan]['status']):
                    device.log(message="%s: fan (%s) is NOT at %s "
                                       "speed, requires checking,%s"
                               % (sub, fan, speed, check_info),
                               level="warn")
                    check_ok = False
                    env = None
                    break
                else:
                    device.log(message=" %s: fan (%s) is NOT at %s speed %s"
                               % (sub, fan, speed, check_info),
                               level="warn")
                    check_ok = False
                    env = None
                    break
        else:
            for fan in fans:
                if "comment" in env[fan].keys():
                    env_val = True
                else:
                    env_val = False
                    break
                if env_val and re.search(speed + " speed",
                                         env[fan]["comment"], re.I):
                    device.log(message="%s: fan (%s) at %s speed,%s "
                               % (sub, fan, speed, check_info),
                               level="debug")
                elif re.search('Check', env[fan]["status"]):
                    device.log(message=" %s: fan (%s) is NOT at %s speed,"
                                       " requires checking,%s"
                               % (sub, fan, speed, check_info),
                               level='warn')
                    check_ok = False
                    env = None
                    break
                else:
                    device.log(message="%s: fan (%s) is NOT at %s speed %s "
                               % (sub, fan, speed, check_info),
                               level="warn")
                    check_ok = False
                    env = None
                    break
        if check_ok:
            device.log(message="%s: all fans run at %s speed"
                       % (sub, check_info), level="debug")
            return True
        env = None

    device.log(message="%s: some fan check failed, speed (%s),%s"
               % (sub, speed, check_info), level="warn")
    return False
# end def check_chassis_fan


def check_chassis_hardware(device, **kwargs):
    """
    Robot Usage Example :
     ${dh} =    Get Handle   resource=r1
     ${hardware} =  {'cb 0': {'description': 'Enhanced MX SCB',
     ...    'serial-number': 'CAAS1382'}, 'cb 1': {
     ...    'description': 'Enhanced MX SCB', 'serial-number': 'CAAS1153'}}
     ${kwargs} =    Evaluate    {'chassis': 'lcc', 'hardware':${hardware},
     ...    'check_count':'5', 'check_interval':'15'}
     ${result} =    Check Chassis Hardware    device=${dh}    &{kwargs}

    Checks chassis hardware inventory using cli "show chassis hardware"

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param hardware :
        **OPTIONAL** Dictionary of hardware inventory from get_chassis_hardware
    :param check_count :
        **OPTIONAL** Check count (default is 1)
    :param check_interval :
        **OPTIONAL** Wait time before next retry (default 10 seconds)

    :returns :
        TRUE when chassis hardware inventory check is passed
        FALSE when chassis hardware inventory check is failed
    """
    valid_keys = ['chassis', 'hardware', 'check_count',
                  'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    hardware = kwargs.get('hardware')
    if hardware is None:
        hardware = get_chassis_hardware(device)
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside '%s' '%s'.." % (sub, str(kwargs)))
    for count_val in range(0, check_count):
        check_info = "count(%s), interval(%s)" \
                     % (count_val, check_interval)
        __sleep(device, count_val, sub, check_interval, check_info)
        # gets hardware value from get_chassis_hardware and stores in hardware_
        hardware_ = get_chassis_hardware(device, chassis=chassis)
        # compares hardware and hardware_ data
        if compare_data(device, var1=hardware, var2=hardware_):
            device.log(message="%s: chassis hardware inventory check"
                               " passed, %s "
                       % (sub, check_info), level="debug")
            return True
        else:
            device.log(message="%s: chassis hardware inventory "
                               "check failed, %s"
                       % (sub, check_info), level="warn")
    device.log(message="%s: chassis hardware inventory "
                       "check failed, %s"
               % (sub, check_info), level="warn")
    return False
# end def check_chassis_hardware


def check_chassis_interface(device, **kwargs):
    """
    Robot Usage Example :
     ${dh} =    Get Handle   resource=r1
     ${interfaces} = {'interface-information' : { 'physical-interface' : {
     ...    'name' : 'fe-0/0/0'}}}
     ${kwargs} =    Evaluate    {'interface':${interfaces},
     ...    'skip_interface':'fxp.*|lo.*', 'check_count':'5',
     ...    'check_interval':'15'}
     ${result} =    Check Chassis Interface     device=${dh}    &{kwargs}

    Check Interface using show interfaces

    :param device:
        **REQUIRED** Device handle
    :param interface :
        **REQUIRED** dict for interfaces
    :param skip_interface :
        **REQUIRED** regular expression for interface
                                      to skip checking (i.e. 'fxp.*|lo.*')
    :param check_count :
        **OPTIONAL** Check count (default is 1)
    :param check_interval:
        **OPTIONAL** Wait time before next retry (default 10 seconds)

    :returns:
        TRUE if IFD/IFL check passes
        FALSE if IFD/IFL check failes
    """
    valid_keys = ['interface', 'skip_interface', 'check_count',
                  'check_interval']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    interface = kwargs.get('interface', get_chassis_interface(device))
    skip_interface = kwargs.get('skip_interface')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s ..." % sub, level="debug")
    check_info = None
    for count_val in range(0, check_count):
        check_info = "count(%s), interval(%s)" \
                     % (count_val, check_interval)
        __sleep(device, count_val, sub, check_interval, check_info)
        # Gets the chassis interface details
        if_ = get_chassis_interface(device, skip_interface=skip_interface)
        # comparing expected dictionary of interface details,
        # with actual interface details
        if compare_data(device, var1=interface, var2=if_):
            device.log(message="%s: IFD/IFL check passed, %s "
                       % (sub, check_info), level="debug")
            return True

    device.log(message="%s : IFD/IFL check failed, %s "
               % (sub, check_info), level="warn")
    return False
# end def check_chassis_interface


def check_chassis_memory(device, **kwargs):
    """
    Robot usage Example :
     ${dh} =    Get Handle   resource=r1
     ${memory} = Create List  '43144K'  '824K'
     ${kwargs} =    Evaluate    {'memory':${memory}, 'check_count':'5',
     ...    'check_interval':'15'}
     ${result} =    Check Chassis Memory    device=${dh}    &{kwargs}

    Check possible memory leak for chassisd

    :param device:
        **REQUIRED** Device handle
    :param memory :
        **REQUIRED** a list of [SIZE, RES] from
        show system process extensive for chassisd.
    :param check_count :
        **OPTIONAL** Check count (default is 1)
    :param check_interval :
        **OPTIONAL** Wait time before next retry (default 10 seconds)

    :return:
        TRUE if memory leak check pass
        FALSE if memory leak check fails
    """
    memory = kwargs.get('memory')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    arg_str = str(kwargs)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s subroutine(%s)" % (sub, arg_str),
               level="debug")
    value = 0
    while value < check_count:
        check_info = ("%s: memory leak check, count(%s), "
                      "interval(%s)" % (sub, value, check_interval))
        __sleep(device, value, sub, check_interval, check_info)
        current_mem = get_chassis_memory(device)
        show_data(device, memory, sub + ": previous memory usage")
        current_memory = int(current_mem[0][:-1])*1000
        if current_memory <= memory[0]:
            device.log(message=" %s passed" % check_info, level="debug")
            return True

        else:
            device.log(message="%s failed" % check_info, level="warn")
        value += 1
    device.log(message="%s failed" % check_info, level="warn")
    return False
# end def check_chassis_memory


def check_fru_valid(device, fru):
    """
    Robot Usage Example :
      ${device_object}  =  Get Handle  resource=r1
      ${result}  =  Check Fru Valid   device=${device_object}  fru='sfc 0'

    Checks whether fru is valid for a particular router or not

    :param device:
        **REQUIRED** Device handle
    :param fru :
        **REQUIRED** fru name or list of frus to check

    :return:
        TRUE if fru is valid
        FALSE if fru is not valid
    """
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s ..." % sub, level="debug")
    if fru in CHASSIS_FRU[model.lower()]:
        device.log(message="%s: fru(%s) is valid for this router model"
                   % (sub, fru), level="debug")
        return True
    device.log(message="%s: fru(%s) is NOT valid for this router model"
               % (sub, fru), level="warn")
    return False
# end def check_fru_valid


def check_craft_led(device, **kwargs):
    """
    Robot Usage Example :
     ${device_object}  =  Get Handle  resource=r1
     ${result}  =  Check Craft Led   device=${device_object}  chassis='sfc 0'
     ...    fru='fpc'  slot=${4}  led='green'

     Checks craft led for fru and displays the expected led,current led
     and the color.

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param fru  :
        **REQUIRED** re|fpc|sib|sfm|pcg|scg|cb|pem
    :param slot :
        **REQUIRED** FRU slot number
    :param led  :
        **REQUIRED** green|amber|red|yellow|major|minor
    :param craft:
       **OPTIONAL** dictionary for craft display
    :param check_count :
        **OPTIONAL** Check count (default is 1)
    :param check_interval :
        **OPTIONAL** Wait time before next retry (default 10 seconds)

    :return:
        TRUE if color of led passed
        FALSE if color of led failed
     """
    valid_keys = ['chassis', 'fru', 'slot', 'led', 'craft',
                  'check_interval', 'check_count']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    fru = kwargs.get('fru')
    slot = kwargs.get('slot')
    led = kwargs.get('led')
    craft = kwargs.get('craft')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)),
               level="debug")
    if not (fru and led):
        return __error_arg_msg(device, 'fru|led', sub)
    leds = {}
    if isinstance(led, list):
        for element in led:
            leds[element] = 1
    elif not isinstance(led, dict):
        leds[led] = 1
    else:
        leds = led

    for count_val in range(0, check_count):
        check_info = "%s: check fru (%s), slot(%s), count(%s), " \
                     "interval(%s)" \
                     % (sub, fru, slot, count_val, check_interval)
        if craft and count_val > 0:
            break
        if not craft:
            sleep(check_interval)
            craft = get_chassis_craft(device, chassis=chassis)
        fru_leds = craft[fru][slot]
        check_ok = True
        show_data(device, leds, "%s:expected leds" % sub)
        show_data(device, fru_leds, "%s: current leds" % sub)
        for element in leds.keys():
            if not fru_leds[element]:
                fru_leds[element] = 0
            if leds[element] == fru_leds[element]:
                device.log(message="%s,color (%s) passed"
                           % (check_info, element), level="debug")
            else:
                device.log(message="%s, color (%s) failed"
                           % (check_info, element), level="warn")
                check_ok = False
        if check_ok:
            device.log(message="%s: %s passed" % (sub, check_info),
                       level="debug")
            return True
    device.log(message="%s: %s failed" % (sub, check_info), level="warn")
    return False
# end def check_craft_led


def check_chassis_status(device, **kwargs):
    """
    Robot Usage Example :
     ${dh} =    Get Handle   resource=r1
     ${memory} = Create List  '43144K'  '824K'
     ${kwargs} =    Evaluate   {'chassis': 'scc', 'sd': 'rsd','check_all': 1,
     ...    'check_fru': 'sib','check_craft': 'craft',
     ...    'check_interface': 'xe-1/0/1','check_hardware': 're',
     ...    'check_memory': 'memory','check_database': 'database',
     ...    'check_alarm': {'scc': 'Chassis'},'check_count': 1,
     ...    'check_interval': 1}
     ${result} =    Check Chassis Status    device=${dh}    &{kwargs}

    Check chassis status for alarm, interface,memory usage,hardware
    inventory craft display by doing the following actions,
        - checks fru state,chassis db,chassis interface,
          chassis craft,chassis hardware,chassis alarm state,chassis memory
        - Depending on error count it will return true or false

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param sd :
        **REQUIRED** rsd | psd1|psd2|psd3|..
    :param status :
        **REQUIRED** expected chassis status to be check
        such as previous status
    :param check_fru :
        **REQUIRED** fru name or list of frus to check
    :param check_slot :
        **REQUIRED** a fru slot, a list of slots or a dict of fru slots
        for check_fru
    :param check_interface :
        **REQUIRED**  0|1 (1 get interfaces from  get_chassis_interface)
    :param skip_interface :
        **REQUIRED** regular expression for interface to skip checking
        (i.e. 'fxp.*|lo.*')
    :param check_alarm :
        **REQUIRED** 0|1 (1 get interfaces from  get_chassis_alarm)
    :param check_craft :
        **REQUIRED** 0|1 (1 get interfaces from  get_chassis_craft)
    :param check_harware :
        **REQUIRED** 0|1 (1 get interfaces from get_chassis_hardware)
    :param check_memory :
        **REQUIRED** 0|1 (1 get interfaces from get_chassis_memory)
    :param check_all :
        **REQUIRED** 0|1 (check all: check_interface, check_hardware,
        check_fru, check_craft)
    :param check_count :
        **OPTIONAL** Check count for craft display (default 0 no checking)
    :param check_interval :
        **OPTIONAL** Wait time before next retry (default 10 seconds)
    :param check_database:
        **REQUIRED** database where all the information is found
        related to chassis

    :returns:
        TRUE if check passes
        FALSE if check failes
    """
    valid_keys = ['chassis', 'sd', 'status', 'skip_interface',
                  'check_interface', 'check_fru', 'check_slot',
                  'check_slot', 'check_alarm', 'check_craft',
                  'check_hardware', 'check_memory', 'check_database',
                  'check_all', 'check_count', 'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    sd = kwargs.get('sd')
    status = kwargs.get('status', {})
    skip_interface = kwargs.get('skip_interface', '')
    check_interface = kwargs.get('check_interface')
    check_fru = kwargs.get('check_fru')
    check_slot = kwargs.get('check_slot')
    check_alarm = kwargs.get('check_alarm')
    check_craft = kwargs.get('check_craft')
    check_hardware = kwargs.get('check_hardware')
    check_memory = kwargs.get('check_memory')
    check_database = kwargs.get('check_database')
    check_all = kwargs.get('check_all')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    check_info = "check_count(%s), check_interval(%s)" \
                 % (check_count, check_interval)
    model = device.get_model().lower()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s function %s ..." % (sub, str(kwargs)))
    if check_all:
        if not check_interface:
            check_interface = 1
        if not check_hardware:
            check_hardware = 1
        if not check_craft:
            check_craft = 1
        if not check_alarm:
            check_alarm = 1
        if not check_memory:
            check_memory = 1
        if not check_fru:
            check_fru = 1
        if not check_database:
            check_database = 1

    if check_fru:
        if check_fru == 1:
            check_fru = get_fru_list(device)
            check_slot = get_fru_slots(device,
                                       chassis=chassis,
                                       sd=sd,
                                       fru=check_fru,
                                       status=status)
        if check_fru_state(device,
                           chassis=chassis,
                           sd=sd,
                           fru=check_fru,
                           state=status,
                           slot=check_slot,
                           check_count=check_count,
                           check_interval=check_interval):
            device.log(message="%s: fru(%s) check passed"
                       % (sub, check_fru), level="debug")
        else:
            device.log(message="%s: fru(%s) check failed"
                       % (sub, check_fru), level="warn")
            return False

    if check_interface:
        if check_interface == 1:
            check_interface = status.get('interface',
                                         get_chassis_interface(device))
        if check_chassis_interface(device, interface=check_interface,
                                   skip_interface=skip_interface,
                                   check_count=check_count,
                                   check_interval=check_interval):
            device.log(message="%s: Interface checking passed, %s"
                       % (sub, check_info), level="debug")
        else:
            device.log(message="%s: Interface check failed checking,%s"
                       % (sub, check_info), level="warn")
            return False

    if not re.search("^TX Matrix|TXP|psd", model, re.I) and check_craft:
        if check_chassis_craft(device, chassis=chassis,
                               status=status,
                               check_count=check_count,
                               check_interval=check_interval):
            device.log(message="%s: craft check passed, %s"
                       % (sub, check_info), level="debug")
        else:
            device.log(message="%s: craft check failed, %s"
                       % (sub, check_info), level="warn")
            return False

    if check_database:
        fru_list = get_fru_list(device)
        if check_chassis_database(device, dynamic=1,
                                  fru=fru_list,
                                  check_count=check_count,
                                  check_interval=check_interval):
            device.log(message="%s  fru %s database check passed"
                       % (sub, fru_list), level="debug")

        else:
            device.log(message="%s: fru(%s) database check failed"
                       % (sub, fru_list), level="warn")
            return False

    if check_hardware:
        if check_hardware == 1:
            check_hardware = status.get('hardware', None)
        if check_chassis_hardware(device, chassis=chassis,
                                  hardware=check_hardware,
                                  check_count=check_count,
                                  check_interval=check_interval):
            device.log(message="%s: hardware check passed, %s"
                       % (sub, check_info), level="debug")

        else:
            device.log(message="%s: hardware check failed, %s"
                       % (sub, check_info), level="warn")
            return False

    if check_alarm:
        if check_alarm == 1:
            check_alarm = status.get('alarm')
        if chassis and isinstance(check_alarm, dict):
            check_alarm = check_alarm[chassis]
        if isinstance(check_alarm, list):
            alarm_count = len(check_alarm)
        else:
            alarm_count = 0
        if check_chassis_alarm(device, chassis=chassis,
                               sd=sd,
                               alarm=check_alarm,
                               count=alarm_count,
                               check_count=check_count,
                               check_interval=check_interval):
            device.log(message="%s: alarm check passed, %s"
                       % (sub, check_info), level="debug")

        else:
            device.log(message="%s: alarm check failed,%s"
                       % (sub, check_info), level="warn")
            return False
    if check_memory:
        if check_memory == 1:
            check_memory = status.get('memory')
        if check_chassis_memory(device, memory=check_memory,
                                check_count=check_count,
                                check_interval=check_interval):
            device.log(message="%s: memory leak check passed, %s"
                       % (sub, check_info), level="debug")

        else:
            device.log(message="%s: memory leak check failed, %s"
                       % (sub, check_info), level="warn")
            return False
    return True
# end def check_chassis_status


def check_fru_state(device, **kwargs):
    """
    Robot Usage Example :
    ${dh} =    Get Handle   resource=r1
    ${kwargs} = Evaluate    {'chassis':'scc', 'sd':'rsd', 'fru':'re',
    ...    'state':{'1':'ON', '2': 'ON'},
    ...    'slot':'0', 'check_count':'3', check_interval:'10'}
    ${result} =    Check Fru State    device=${dh}    &{kwargs}

    Checks if all chassis fru is in the expected state or not and
    the slot in that fru is in expected state or not.

    :param device:
        **REQUIRED** Device handle
    :param chassis:
        **OPTIONAL** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param sd:
        **OPTIONAL** rsd | pfd1 | psd2 | psd3
    :param fru:
        **OPTIONAL**  fpc | sib | sfm | pcg | scg | cb | pic or
        list of them
    :param slot:
        **OPTIONAL** FRU slot number or list or Dictionary
    :param state:
        **OPTIONAL** Regular expression for fru state.
    :params check_count:
        **OPTIONAL** Check count. Default is 1
    :params check_interval:
        **OPTIONAL** Wait time before next retry. Default 10 seconds

    :return:
        TRUE if the fru is in the expected state
        FALSE if the fru is not in the expected state
    """
    valid_keys = ['chassis', 'sd', 'fru', 'slot', 'state',
                  'check_count', 'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    sd = kwargs.get('sd')
    fru = kwargs.get('fru')
    slot = kwargs.get('slot')
    state = kwargs.get('state')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)

    model = device.get_model().lower()
    sub = function_name(device) + " (%s)" % model

    device.log(message="Inside '%s' '%s' .." % (sub, str(kwargs)))

    if chassis and (chassis == 'scc') and not isinstance(fru, list) \
            and (re.search(r'^fpc|scg|pic$', fru, re.I)):
        device.log(message="'%s': skipped '%s' for scc" % (sub, fru),
                   level="warn")
        return True

    if re.search(r'^TX Matrix|TXP$', model, re.I) and \
            (not chassis) and (fru != 'lcc'):
        if isinstance(slot, dict):
            for slotkeys in slot.keys():
                state_ = state
                show_data(device, state, "'%s': state" % sub)
                if isinstance(state, dict):
                    state_ = state[slotkeys]
                    if check_fru_state(device, chassis=slotkeys,
                                       fru=fru,
                                       slot=slot[slotkeys],
                                       state=state_,
                                       check_count=check_count,
                                       check_interval=check_interval):
                        device.log(message="%s: chas(%s) check passed"
                                   % (sub, slotkeys), level="debug")
                    else:
                        device.log(message="%s: chas(%s) check failed"
                                   % (sub, slotkeys), level="warn")
                        return False
            return True
        else:
            device.log(message="%s: expect dict for slot(%s)"
                       % (sub, slot), level="error")
            return False

    if isinstance(fru, list):
        for fru_chas in fru:
            if chassis and (chassis == 'scc') and (
                    re.search(r'^fpc|scg|pic$', fru_chas, re.I)):
                device.log(message="%s: skipped %s for scc"
                           % (sub, fru), level="warn")
                continue

            if check_fru_state(device, chassis=chassis,
                               fru=fru_chas,
                               slot=slot[fru_chas],
                               state=state,
                               check_count=check_count,
                               check_interval=check_interval):
                device.log(message="%s: fru(%s) check passed"
                           % (sub, fru_chas), level="debug")
            else:
                device.log(message="%s: fru(%s) check failed"
                           % (sub, fru_chas), level="warn")
                return False
        return True

    if not (fru and state and slot):
        show_data(device, fru, "%s: fru" % sub)
        show_data(device, state, " %s: state" % sub)
        device.log(message="%s:argument required fru:%s,state: %s,slot:%s"
                   % (sub, fru, state, slot), level="error")
        return False

    check_ok = True
    for i in range(0, check_count):
        check_info = "count: %s " % str(i) + " interval: %s" \
                % str(check_interval)
        __sleep(device, i, sub, check_interval, check_info)
        if fru == 'pic':
            if isinstance(slot[0], list):
                for slot_chas in slot:
                    pic_status = get_fru_status(device,
                                                chassis=chassis,
                                                sd=sd,
                                                fru=fru,
                                                slot=slot_chas)
                    current_state = pic_status[0]['state']
                    if not re.search(r'^%s$' % state, current_state, re.I):
                        device.log(message="%s: fru(%s) on slot [%s] is "
                                           "NOT in state(%s), %s"
                                   % (sub, fru, slot_chas, state, check_info),
                                   level="warn")
                        check_ok = False
                        break
            else:
                # 1 pic
                pic_status = get_fru_status(device, chassis=chassis,
                                            sd=sd, fru=fru,
                                            slot=slot)

                current_state = pic_status[int(slot[0])]['state']
                _state = state
                if isinstance(state, dict):
                    show_data(device, state,
                              "'%s': fru('%s'), slot('%s'), state:"
                              % (sub, fru, current_state))
                    _state = state[fru][str(slot[0])]['state']

                device.log(message="%s: Checking fru(%s), slot(%s) ..."
                           % (sub, fru, slot), level="debug")
                if re.search(r'^%s$' % _state, current_state, re.I):
                    device.log(
                        message="%s: all slots of fru(%s) is in the state(%s), %s"
                        % (sub, fru, state, check_info),
                        level="debug")
                    return True
                else:
                    device.log(message="%s: fru(%s) on slot (%s) is NOT in "
                                       "state(%s), %s"
                               % (sub, fru, slot, state, check_info),
                               level="warn")
                    return False

        elif isinstance(slot, list):
            # Not a pic
            check_ok = True
            fru_status = get_fru_status(device, chassis=chassis,
                                        sd=sd, fru=fru)
            for slot_ in slot:
                device.log(message="%s: Checking fru(%s), slot(%s) ..."
                           % (sub, fru, slot_), level="debug")
                show_data(device, fru_status, " %s: elsif, fru_status" % sub)
                current_state = fru_status[str(slot_)]['state']
                _state = state
                if isinstance(state, dict):
                    show_data(device, state, "%s: fru(%s), slot(%s), state:"
                              % (sub, fru, slot_))
                    _state = state[fru][str(slot_)]['state']

                if not re.search(r'^%s$' % _state, current_state, re.I):
                    device.log(message=" %s: fru(%s) on slot %s is "
                                       "NOT in state(%s), %s"
                               % (sub, fru, slot_, state, check_info),
                               level="warn")
                    check_ok = False
                    break
        else:
            fru_status = get_fru_status(device, chassis=chassis,
                                        sd=sd, fru=fru, slot=slot)

            show_data(device, fru_status, "'%s': else, fru_status" % sub)
            current_state = fru_status[0]['state']
            device.log(message="%s: fru_state(%s)"
                       % (sub, fru_status), level="debug")
            if re.search(r'^%s$' % state, current_state, re.I):
                device.log(message="%s: fru(%s) on slot %s is "
                                   "in state(%s), slot(%s),  %s"
                           % (sub, fru, slot, state, slot, check_info),
                           level="debug")
                return True
            else:
                device.log(message="%s: fru(%s) not on state(%s), %s, slot:%s"
                           % (sub, fru, state, check_info, slot), level="warn")

                return False

    if check_ok:
        device.log(message="%s: all slots of fru(%s) is in state (%s), %s"
                   % (sub, fru, state, check_info), level="debug")
        return True
    else:
        return False
# end def check_fru_state


def flap_spare_sib(device, **kwargs):
    """
    Robot Usage Example :
      ${device_object} =  Get Handle  resource=r1
      ${result} =  Flap Spare Sib  device=${device}  chassis='sfc 0'

    Flaps the spare_sib

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param fru :
        **OPTIONAL** fru name or list of frus to check

    :return :
        TRUE if the process has no error
    """
    valid_keys = ['chassis', 'fru']
    request_keys = []
    kwargs = check_args(device, valid_keys, request_keys, kwargs)
    model = device.get_model().lower()
    sub = function_name(device) + " (%s)" % model
    chassis = kwargs.get('chassis')
    fru = kwargs.get('fru')
    device.log(message="Inside %s (%s) ..." % (sub, kwargs), level="debug")
    # if fru value equals to sib then it gets spare_sib value
    #    form get_fru_slots
    if fru == 'sib':
        spare_sib = get_fru_slots(device, chassis=chassis,
                                  state='Spare', fru='sib')
        # if spare_sib value is greater then it requests for fru offlline
        if spare_sib and (spare_sib[0] > 0):
            request_fru_offline(device, chassis=chassis,
                                fru='sib', slot=0)
            sleep(2)
            # resets the state of fru from offline to online if fru is offline
            request_fru_online(device, chassis=chassis, fru='sib', slot=0)
            sleep(8)
    return True
# end def flap_spare_sib


def check_spare_sib(device, **kwargs):
    """
    Robot Usage Example :
      ${dh} =    Get Handle   resource=r1
      ${kwargs} = Evaluate    {'chassis':'scc'}
      ${result} =    Check Spare Sib     device=${dh}    &{kwargs}

    Checks for the spare sib availability(online|spare)
    by doing the following
        - Checks spare is available or not for the model
        - If available,it will return TRUE or else will return false

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        *OPTIONAL* Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)

    Return
        TRUE if spare sib is available
        FALSE if no spare sib or no online spare sibs
    """
    valid_keys = ['chassis']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside  (%s) function (%s) ..." % (sub, str(kwargs)))
    match1 = re.search(r'^t\d+$', model)
    match2 = re.search('^TX Matrix|TXP$', model.strip(), re.I)
    if not (match1 or match2):
        device.log(
            message="unexpected device model : " +
            "%s ... expecting T or TXP model" % model)
        return False
    if match2:
        if not chassis:
            # spare_return = {}
            for chassis_list in get_chassis_list(device):
                if not check_spare_sib(device, chassis=chassis_list):
                    return False
            return True
    sib_slots = get_fru_slots(device, chassis=chassis,
                              fru='sib', state='(Online|Spare)')
    spare_sib_slots = get_fru_slots(device, chassis=chassis,
                                    fru='sib', state='Spare')
    if not (isinstance(sib_slots, list) and isinstance(spare_sib_slots, list)):
        device.log(message="%s: no online spare sibs" % sub, level="warn")
        return False
    if model == 't320' and len(sib_slots) == 3 or \
            (model != 't320' and len(sib_slots) == 5):
        if len(spare_sib_slots) == 1:
            device.log(message=" %s: has 1 spare sib OK" % sub, level="debug")
            return True
        else:
            device.log(message=" %s: has incorrect # of spare sib" % sub,
                       level="warn")
            return False
    else:
        device.log(message="%s : no spare sib" % sub)
        return False
# end def check_spare_sib


def delete_chassis_alarm(device, **kwargs):
    """
    Robot Usage Example :
      ${device_object} =  Get Handle  resource=r1
      ${result} =  Delete Chassis Alarm  ${device}  deactivate=${1}
      ...    commit=${1}

    Deletes or deactivates the chassis alarm created.

    :param device:
        **REQUIRED** Device handle
    :params deactivate:
        **REQUIRED** Use deactivate instead of default delete
    :param commit :
        **OPTIONAL** 1|0 commit after set (default is 0)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['deactivate', 'failover', 'commit']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    arg_str = str(kwargs)
    deactivate = kwargs.get('deactivate')
    commit = kwargs.get('commit')
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s ...." % (sub, arg_str), level="debug")
    if deactivate:
        cfg_cmd = "deactivate"
    else:
        cfg_cmd = "delete"
    cfg_cmd += " chassis alarm"
    device.config(command_list=[cfg_cmd])
    if commit:
        return device.commit().response()
    return True
# end def delete_chassis_alarm


def delete_chassis_control(device, **kwargs):
    """
    Robot Usage Example :
     ${dh} =    Get Handle   resource=r1
     ${kwargs} = Evaluate    {'deactivate':1, 'commit':1}
     ${result} =    Delete Chassis Control     device=${dh}    &{kwargs}

    Delete/deactivate system processes chassis-control configuration
        - It executes the command
           "deactivate system processes chassis-control"
          if deactivate value is specified
        - Otherwise it executes the command
           "delete system processes chassis-control"
        - Finally commits if commit value is given.

    :param device:
        **REQUIRED** Device handle
    :params deactivate:
        **REQUIRED** Use deactivate instead of default delete
    :param commit :
        **OPTIONAL** 1|0 commit after set (default is 0)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['deactivate', 'failover', 'commit']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    arg_str = str(kwargs)
    deactivate = kwargs.get('deactivate')
    commit = kwargs.get('commit')
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, arg_str), level="debug")
    if deactivate:
        cfg_cmd = "deactivate"
    else:
        cfg_cmd = "delete"
    cfg_cmd += " system processes chassis-control"
    device.config(command_list=[cfg_cmd])
    if commit:
        return device.commit().response()
    return True
# end def delete_chassis_control


def delete_chassis_graceful(device, **kwargs):
    """
    Robot Usage Example :
     ${dh} =    Get Handle   resource=r1
     ${kwargs} = Evaluate    {'deactivate':1, 'commit':1}
     ${result} =    Delete Chassis Graceful     device=${dh}    &{kwargs}

    Delete/deactivate chassis graceful, if the check_version
    (version = '9.0') of chassis is true
        - It executes the command "deactivate chassis redundancy
          graceful-switchover" if deactivate value is specified
        - Otherwise it executes the command
           "delete chassis redundancy graceful-switchover"
        - It executes the command "deactivate chassis redundancy
          graceful-switchover enable" if deactivate value is specified
        - Otherwise it executes the command
           "delete chassis redundancy graceful-switchover enable"
        - Finally commits if commit value is given.

    :param device:
        **REQUIRED** Device handle
    :params deactivate:
        **REQUIRED** Use deactivate instead of default delete
    :param commit :
        **OPTIONAL** 1|0 commit after set (default is 0)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['deactivate', 'commit']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    commit = kwargs.get('commit')
    deactivate = kwargs.get('deactivate')
    arg_str = str(kwargs)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, arg_str), level="debug")
    if deactivate:
        set_cmd = "deactivate"
    else:
        set_cmd = "delete"
    if re.search(r'^9.0', device.get_version()):
        set_cmd += " chassis redundancy graceful-switchover"
    else:
        set_cmd += " chassis redundancy graceful-switchover enable"
    device.config(command_list=[set_cmd])
    if commit:
        return device.commit().response()
    return True
# end def delete_chassis_graceful


def delete_chassis_redundancy(device, **kwargs):
    """
    Robot Usage Example :
      ${dh} =    Get Handle   resource=r1
      ${kwargs} = Evaluate    {'deactivate':1, 'commit':1}
      ${result} =    Delete Chassis Redundancy     device=${dh}    &{kwargs}

    To deactivate or delete the chassis redundancy
        - It executes the command "deactivate chassis redundancy"
          if deactivate value is specified
        - Otherwise it executes the command "delete chassis redundancy"
        - Finally commits if commit value is given.

    :param device:
        **REQUIRED** Device handle
    :params deactivate:
        **REQUIRED** Use deactivate instead of default delete
    :param commit :
        **OPTIONAL** 1|0 commit after set (default is 0)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['deactivate', 'commit']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    commit = kwargs.get('commit')
    deactivate = kwargs.get('deactivate')
    model = device.get_model()
    arg_str = str(kwargs)
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, arg_str), level="debug")
    if deactivate:
        set_cmd = "deactivate"
    else:
        set_cmd = "delete"
    set_cmd += " chassis redundancy"
    device.config(command_list=[set_cmd])
    if commit:
        return device.commit().response()
    return True
# end def delete_chassis_redundancy


def delete_chassis_manufacturing_diagnostics_mode(device, **kwargs):
    """
    Robot Usage Example :
     ${dh} =    Get Handle   resource=r1
     ${kwargs} = Evaluate    {'deactivate':1, 'commit':1}
     ${result} =   Delete Chassis Manufacturing Diagnostics Mode
     ...    device=${dh}    &{kwargs}

    Delete/deactivate chassis manufacturing-diagnostic-mode configuration.
        - It executes the command
           "deactivate chassis manufacturing-diagnostic-mode"
          if deactivate value is specified.
        - Otherwise it executes the command
           "delete chassis manufacturing-diagnostic-mode"
        - Finally commits if commit value is given.

    :param device:
        **REQUIRED** Device handle
    :params deactivate:
        **REQUIRED** Use deactivate instead of default delete
    :param commit :
        **OPTIONAL** 1|0 commit after set (default is 0)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['deactivate', 'commit']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    commit = kwargs.get('commit')
    deactivate = kwargs.get('deactivate')
    arg_str = str(kwargs)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, arg_str), level="debug")
    if deactivate:
        cfg_cmd = "deactivate"
    else:
        cfg_cmd = "delete"
    cfg_cmd += " chassis manufacturing-diagnostic-mode"
    device.config(command_list=[cfg_cmd])
    if commit:
        return device.commit().response()
    return True
# end def delete_chassis_manufacturing_diagnostics_mode


def delete_temperature_threshold(device, **kwargs):
    """
    Robot Usage Example :
       ${dh} =    Get Handle   resource=r1
       ${kwargs} = Evaluate    {'deactivate':1, 'commit':1}
       ${result} =    Delete Temperature Threshold     device=${dh}
       ...    &{kwargs}

    Delete/deactivate chassis temperature-threshold configuration
        - It executes the command "deactivate chassis temperature-threshold" if
          deactivate value is specified.
        - Otherwise it executes command "delete chassis temperature-threshold"
        - Finally commits if commit value is given.

    :param device:
        **REQUIRED** Device handle
    :params deactivate:
        **REQUIRED** Use deactivate instead of default delete
    :param commit :
        **OPTIONAL** 1|0 commit after set (default is 0)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['deactivate', 'commit']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    commit = kwargs.get('commit')
    deactivate = kwargs.get('deactivate')
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    arg_str = str(kwargs)
    device.log(message="Inside %s %s..." % (sub, arg_str), level="debug")
    if deactivate:
        cfg_cmd = "deactivate"
    else:
        cfg_cmd = "delete"
    cfg_cmd += " chassis temperature-threshold"
    device.config(command_list=[cfg_cmd])
    if commit:
        return device.commit().response()
    return True
# end def delete_temperature_threshold


def get_chassis_alarm(device, **kwargs):
    """
    Robot Usage Example :
      ${device_object} =  Get Handle  resource=r1
      ${result} =  Get Chassis Alarm  device=${device_object}  chassis='lcc 0'
      ...    sd='rsd'   xml=${1}

    Get chassis alarms using show chassis alarms command

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param sd :
        **REQUIRED** rsd | psd1|psd2|psd3|..
    :param xml :
        **OPTIONAL** 1|0 use xml output (default is 1)

    :return :
        List of chassis alarms
    """
    valid_keys = ['xml', 'sd', 'chassis']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    sd = kwargs.get('sd')
    xml = kwargs.get('xml', 1)
    alarms = {}
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s function %s..." % (sub, str(kwargs)))
    if not xml:
        alarms = __cli_get_alarm(device, chassis=chassis)
        return alarms

    if device.is_evo():
        cli_cmd = "show system alarms "
    else:
        cli_cmd = "show chassis alarms "

    if chassis:
        cli_cmd += " %s" % chassis

    rpc_str = device.get_rpc_equivalent(command=cli_cmd)
    response = device.execute_rpc(command=rpc_str).response()
    if re.search("^TX Matrix|TXP|psd", model, re.I):
        chassis_item = response.findall(
            './/multi-routing-engine-results/multi-routing-engine-item')
        if (re.search("^TX Matrix|TXP", model, re.I) and not chassis) \
                or re.search("^psd", model, re.I):
            for item in chassis_item:
                slot = item.find('.//re-name').text
                cid = __get_cid(device, slot)
                alarms[cid] = __get_alarm_info(device, item)
        if re.search("^psd", model, re.I) and sd:
            alarms = alarms[sd]
    else:
        alarms = __get_alarm_info(device, response)
    return [alarms]
# end def get_chassis_alarm


def get_chassis_craft(device, **kwargs):
    """
    Get chassis craft-interface display using cli command
    show chassis craft-interface

    :param device:
        **REQUIRED** Device handle
    :params xml:
        **OPTIONAL** 1 | 0 for xml output (default is 1)
    :params chassis:
        **REQUIRED** scc|lcc0|1|2|3

    :returns:
        Dictionary of craft-interface display.
    """
    args_str = str(kwargs)
    xml = kwargs.get('xml', 1)
    chassis = kwargs.get('chassis')
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s (%s)" % (sub, args_str))
    if not CHECK_CRAFT:
        device.log(
            message="%s: return undef since CHECK_CRAFT flag is off" % sub)
        return None
    models = "^(m5|m[124]0|m7i|m10i|IRM|mx960|mx240|mx480|" +\
             "a40|srx5800|' 'a15|a20|srx5600|srx5400|a10|srx3600|" +\
             "a2|srx3400|srx1400|ex82[01][68])$"
    if (not xml) or re.search(models, model, re.I):
        result = __cli_get_craft(device, chassis=chassis)
        return result
    craft = {}
    cli_cmd = "show chassis craft-interface"
    if chassis:
        cli_cmd += " %s" % chassis
    rpc_str = device.get_rpc_equivalent(command=cli_cmd)
    chassis_reponse = device.execute_rpc(command=rpc_str).response()
    if re.search('^TX Matrix|TXP$', model, re.I):
        chassis_item = chassis_reponse.findall(
            './/multi-routing-engine-results/multi-routing-engine-item')
        if not chassis:
            for index in range(len(chassis_item)):
                for item in chassis_item[index].getchildren():
                    cid = __get_cid(
                        device, chassis_item[index].find('.//re-name').text)
                    if cid == 'sfc0':
                        cid = "sfc 0"
                    craft[cid] = get_chassis_craft(device, chassis=cid,
                                                   xml=xml)
            return craft
    show_data(device, chassis_reponse, sub + ": chas_item")
    craft_info = chassis_reponse.findall('.//craft-information')
    show_data(device, craft_info, sub + ": craft info")
    for value in craft_info:
        for child in value.getchildren():
            key = child.tag
            device.log(message="%s: get led from key..." % key)
            if key == 'front-panel':
                for child1 in child.getchildren():
                    panel = child1.tag
                    device.log(message=sub + ": panel(%s)" % panel)
                    if panel == 'display-panel':
                        craft["display"] = []
                        for item in child1.findall("display-line"):
                            craft["display"].append(item.text.strip())
                    elif panel == 'alarm-indicators':
                        craft['alarm'] = {}
                        for item in child.findall(panel):
                            craft['alarm'] = __get_alarm_led(
                                device, {item.tag: item.text})
                    elif re.search(r'^(\S+)-panel$', panel):
                        match1 = re.match(r'^(\S+)-panel$', panel)
                        fru = match1.group(1)
                        device.log(
                            message=sub + ": panel(%s , fru(%s)" % (panel,
                                                                    fru))
                        fru_list = []
                        for item in child1.getchildren():
                            fru_list_dict = {}
                            for item2 in item.getchildren():
                                fru_list_dict[item2.tag] = item2.text
                            fru_list.append(fru_list_dict)
                        craft[fru] = __get_fru_craft(device, (fru_list))
            elif re.search(r'^(\S+)-panel$', key):
                match1 = re.search(r'^(\S+)-panel$', key)
                fru = match1.group(1)
                if fru == 'power-supply':
                    fru = 'pem'
                fru_list = []
                for item in child.getchildren():
                    fru_list_dict = {}
                    for item2 in item.getchildren():
                        fru_list_dict[item2.tag] = item2.text
                    fru_list.append(fru_list_dict)
                craft[fru] = __get_fru_craft(device, fru_list)
    show_data(device, craft, sub + ": return")
    return craft
# end def get_chassis_craft


def get_chassis_database(device, **kwargs):
    """
    Robot Usage Example :
       ${device_object} =  Get Handle  resource=r1
       ${result} =  Get Chassis Database  device=${device_object}
       ...    dynamic=${1}  static=${1}

    Get chassis database using cli command by doing the following
        - If dynamic db, show chassis hardware database dynamic command
        is passed
        - If static db, show chassis hardware database static command
        is passed
        - Returns chassis database

    :param device:
        **REQUIRED** Device handle
    :param dynamic :
        **OPTIONAL** 1|0 get dynamic database (default is 1)
    :param static :
        **OPTIONAL** 1|0 get dynamic database (default is 0)

    :return: Dictionary of chassis dynamic|static database
    """
    valid_keys = ['dynamic', 'static']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    dynamic = kwargs.get('dynamic')
    static = kwargs.get('static')
    chassis_database = {}
    model = device.get_model()
    sub = function_name(device) + "%s" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)))
    # If both dynamic and static aren't specified,by default it is taken as 1
    if not (dynamic or static):
        dynamic = static = 1
    cli_cmd = "show chassis hardware database"
    # show chassis hardware database dynamic command is executed If dynamic
    if dynamic:
        chassis_database["dynamic"] = {}
        response = device.cli(command=cli_cmd+" dynamic").response()
        chas_dynamic_db = ast.literal_eval(str(jxmlease.parse(response)))
        chas_dynamic_db_frus = dict(list(chas_dynamic_db.values())[0])
        for fru in chas_dynamic_db_frus.keys():
            chassis_database["dynamic"][fru] = {}
            device.log(message="%s: dynamic db, fru(%s)" % (sub, fru),
                       level="debug")
            # Retrieves a instance list if fru is not psd or esc
            if not (fru == 'psd' or fru == 'esc'):
                instance_list = chas_dynamic_db_frus[fru].get(
                    "%s-instance" % fru)
                if instance_list:
                    fru = __convert_db_name(device, fru, model)
                    if not isinstance(instance_list, list):
                        instance_list = [instance_list]
                    for instance in instance_list:
                        slot = instance.get("slot")
                        if not (slot and re.search(r'^\d+$', slot)):
                            device.log(message="%s: slot NOT an integer" % sub,
                                       level="warn")
                            continue
                        chassis_database["dynamic"][fru] = {}
                        chassis_database["dynamic"][fru][slot] = instance
                        if fru == 'fpc':
                            pic_list = instance['pic']['pic-instance']
                            if not isinstance(pic_list, list):
                                pic_list = [pic_list]
                            for pic_db in pic_list:
                                show_data(device, pic_db, "%s:pic = " % sub)
                                pic_slot = pic_db["slot"]
                                if not (pic_slot and re.search(r'^\d+$',
                                                               pic_slot)):
                                    device.log(
                                        message="%s: pic slot NOT an integer"
                                        % sub, level="warn")
                                    continue
                                chassis_database["dynamic"]["pic"] = {}
                                chassis_database["dynamic"]["pic"][slot] = {}
                                chassis_database["dynamic"]["pic"][slot][
                                    pic_slot] = pic_db

    # show chassis hardware database static command is executed if static
    if static:
        response = device.cli(command=cli_cmd+" static").response()
        result = ast.literal_eval(str(jxmlease.parse(response)))
        chassis_database["static"] = {}
        chassis_database["static"] = result
    show_data(device, chassis_database, "%s return" % sub)
    return chassis_database
# end def get_chassis_database


def get_chassis_environment(device, **kwargs):
    """
    Robot Usage Example :
      ${device_object} =  Get Handle  resource=r1
      ${result} =  Get Chassis Environment  device=${device_object}
      ...    chassis='lcc 0'   sd='rsd'  xml=${1}     fru='fpc'  slot=${1}

    Gets the chassis environment using cli command
    show chassis environment <fru> command

    :param device:
        **REQUIRED** Device handle
    :param xml  :
        **OPTIONAL** 1|0 for xml output (default is 1)
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param sd   :
        **REQUIRED** rsd | psd1|psd2|psd3|..
    :param fru  :
        **REQUIRED** FRU name (pem|fpc|pcg|scg|sib)
    :param slot :
        **REQUIRED** fru slot number

    :return:
        Dictionary of chassis environment information.
        With fru option, returns an list of chassis environment for each slot
    """
    valid_keys = ['xml', 'fru', 'slot', 'chassis', 'sd']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    chassis = kwargs.get('chassis')
    sd = kwargs.get('sd')
    fru = kwargs.get('fru')
    slot = kwargs.get('slot')
    xml = kwargs.get('xml', 1)
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s %s ..." % (sub, str(kwargs)))
    env = {}
    if fru:
        if xml:
            # To be implemented
            return __cli_get_environment(device, chassis=chassis, fru=fru,
                                         slot=slot)
    else:
        if not xml:
            return __cli_get_environment(device, chassis=chassis)
    cli_cmd = "show chassis environment "
    if chassis:
        cli_cmd += " %s" % chassis
    rpc_str = device.get_rpc_equivalent(command=cli_cmd)
    response = device.execute_rpc(command=rpc_str).response()
    env_info = []
    if re.search('^TX Matrix|TXP$', model, re.I):
        chas_item = response.findall(
            './/multi-routing-engine-results/multi-routing-engine-item')
        if not chassis:
            for item in chas_item:
                cid = __get_cid(device, item.find('re-name'))
                env[cid] = get_chassis_environment(device, chassis=cid,
                                                   xml=xml)
            show_data(device, env, "%s: return" % sub)
            return env
        env_info = response.findall(
            './/multi-routing-engine-results/multi-routing-engine-item/' +
            'environment-information')
    elif model is 'psd':
        chas_item = response.findall(
            './/multi-routing-engine-results/multi-routing-engine-item')
        if not sd:
            for item in chas_item:
                cid = __get_cid(device, item.find('re-name'))
                env[cid] = get_chassis_environment(device, sd=cid, xml=xml)
            show_data(device, env, "%s: return" % sub)
            return env
        else:
            for item in chas_item:
                cid = __get_cid(device, item.find('re-name'))
                env_info = item.findall(
                    './/environment-information/environment-item')
                if cid == sd:
                    break
    else:
        env_info = response.findall('.//environment-information')
    for item in env_info:
        show_data(device, item, "%s: item" % sub)
        for key in item.findall(".//environment-item"):
            env1 = {}
            for key2 in key.getchildren():
                if key2.tag == "name":
                    name_value = __convert_name(device, key2.text)
                    env1[name_value] = {}
                else:
                    env1[name_value][key2.tag] = key2.text
            env.update(env1)
        show_data(device, env, "%s: return" % sub)
    return env
# end def get_chassis_environment


def get_chassis_ethernet(device):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Ethernet  device=${device_object}

    Get switch Ethernet information
        - show chassis ethernet-switch command is passed
        - returns status,port,device,speed,duplex informations

    :param device:
        **REQUIRED** Device handle

    :return : Dictionary of chassis Ethernet switch information
    """
    out = __cli_get_ethernet(device)
    return out
# end def get_chassis_ethernet


def get_chassis_firmware(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Firmware  device=${device_object}
    ...    chassis='lcc 0'  xml=${1}

    Get chassis firmware and operating system version for
    components from multi-routing-engine and firmware-information.

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param xml  :
        **OPTIONAL** 1|0 use xml output (default is 1)

    :return :
        Dictionary of firmware version
    """
    valid_keys = ['chassis', 'xml']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    xml = kwargs.get('xml', 1)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s function %s ..." % (sub, str(kwargs)))
    if not xml:
        return __cli_get_firmware(device)
    cli_cmd = "show chassis firmware"
    if chassis:
        cli_cmd += " %s" % chassis
    rpc_str = device.get_rpc_equivalent(command=cli_cmd)
    response = device.execute_rpc(command=rpc_str).response()
    # xml_option = response.findall('..//xml_option/forcearray/firmware')
    match = re.search('^TX Matrix|TXP$', model, re.I)
    chassis_firmware = {}
    if match:
        chassis_item = response.findall('.//multi-routing-engine-results'
                                        '/multi-routing-engine-item')
        if not chassis:
            for item in chassis_item:
                cid = __get_cid(device, item.find(".//re-name").text)
                chassis_firmware[cid] = get_chassis_firmware(device,
                                                             chassis=cid)
            return chassis_firmware
        chassis_module = response.findall(
            './/multi-routing-engine-results/multi-routing-engine-item/' +
            'firmware-information/chassis/chassis-module')
    else:
        chassis_module = response.find('.//chassis-module')
    if not isinstance(chassis_module, list):
        chassis_module = [chassis_module]
    for module in chassis_module:
        name = module.find(".//name").text
        name = name.lower()
        name = __chop(device, name)
        if module.find(".//firmware") is not None:
            chassis_firmware[name] = {}
            type_ = module.find(".//type").text
            firmware_version = module.find(".//firmware-version").text
            chassis_firmware[name][__chop(device, type_)] = __chop(
                device, firmware_version)
    show_data(device, chassis_firmware, sub+": return")
    return chassis_firmware
# end def get_chassis_firmware


def get_chassis_hardware(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Hardware  device=${device_object}  chassis='lcc 0'
    ...    xml=${1}

    Get chassis hardware inventory using cli command " show chassis hardware "

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param xml  :
        **OPTIONAL** 1|0 use xml output (default is 1)
    :param detail :
        **OPTIONAL** 1|0 Include RAM modules in output (default is 0)
    :param extensive :
        **OPTIONAL** 1|0 Display ID EEPROM information (default is 0)
    :param frus :
        **OPTIONAL** 1|0 Display assembly IDs and extra PIC information
        (default is 0)
    :param models :
        **OPTIONAL** 1|0 Display Models & CLEI code information (default is 0)

    :return :
        Dictionary of chassis hardware information
    """
    # Check parameter
    valid_keys = ['xml', 'detail', 'extensive', 'frus', 'chassis', 'models']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    xml = kwargs.get('xml', 1)
    detail = kwargs.get('detail', 0)
    extensive = kwargs.get('extensive', 0)
    frus = kwargs.get('frus', 0)
    chassis = kwargs.get('chassis')
    models = kwargs.get('models', 0)
    model = device.get_model()
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level="debug")
    cli_cmd = "show chassis hardware"
    if detail:
        cli_cmd += " detail"
    elif extensive:
        cli_cmd += " extensive"
    elif frus:
        cli_cmd += " frus"
    elif models:
        cli_cmd += " models"
    if chassis:
        cli_cmd += " " + chassis

    chassis_hardware = {}
    if not xml:
        return __cli_get_hardware(device, chassis=chassis)

    rpc_str = device.get_rpc_equivalent(command=cli_cmd)
    response = device.execute_rpc(command=rpc_str).response()
    if frus:
        chassis_fru = response.find("./chassis-fru-inventory/chassis-fru")
        chassis_hardware['name'] = chassis_fru.find('.//name').text
        for i in ["assembly-identifier", "connector-type",
                  "fiber-type", "driver-strength", "description"]:
            if chassis_fru.find(".//%s" % i) is not None:
                value = chassis_fru.find(".//%s" % i).text
                chassis_hardware[i] = value

        chassis_fru_module = chassis_fru.findall('.//chassis-fru-module')
        for module in chassis_fru_module:
            name = module.find('.//name').text
            name = __chop(device, name)
            chassis_hardware[name] = {}
            for item in module.getchildren():
                key = item.tag
                if key != "name":
                    chassis_hardware[name][key] = module.find(".//"+(key)).text

    else:
        if re.search('^TX Matrix|TXP$', model, re.I) or \
                re.search('^psd', model, re.IGNORECASE):
            chas_item = response.findall(
                './/multi-routing-engine-results/multi-routing-engine-item')
            if chassis:
                for item in chas_item:
                    chassis_hardware.update(
                        __get_chassis_inventory(device,
                                                item.find(
                                                    './/chassis-inventory')))
            else:
                for item in chas_item:
                    cid = __get_cid(device, item.find('.//re-name').text)
                    device.log(message="%s: cid(%s)" % (sub, cid),
                               level="debug")
                    chassis_hardware[cid] = __get_chassis_inventory(
                        device, item.find('.//chassis-inventory'))
        else:
            chassis_hardware = __get_chassis_inventory(device, response)
    show_data(device, chassis_hardware, "%s: return" % sub)
    return chassis_hardware
# end def get_chassis_hardware


def get_chassis_hostname(device, chassis=''):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Hostname  device=${device_object}  chassis='lcc 0'

    Get the chassis hostname using the cli command "show version brief"

    :param device:
        **REQUIRED** Device handle
    :param chassis:
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)

    :return:
        chassis hostname
    """
    model = device.get_model()
    arg_str = str(chassis)
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s (%s)" % (sub, arg_str), level="debug")
    hostname = {}
    if re.search(r'^TX Matrix|TXP$', model, re.I) and not chassis:
        chassis_list = get_chassis_list(device)
        for value in chassis_list:
            device.log(message="%s: chassis(%s)" % (sub, value), level="debug")
            hostname[value] = get_chassis_hostname(device, chassis=value)
        show_data(device, hostname, sub+" return: ")
        return hostname
    cli_cmd = "show version brief"
    if chassis:
        cli_cmd += " %s" % chassis
    rpc_str = device.get_rpc_equivalent(command=cli_cmd)
    response = device.execute_rpc(command=rpc_str).response()
    if re.search('^TX Matrix|TXP$', model, re.I) \
            and chassis != 'scc':
        chas_item = response.findall(
            ".//multi-routing-engine-results/multi-routing-engine-item")
    chas_item = response.findall('.//software-information/host-name')
    for value in chas_item:
        # key = value.tag
        hostname = __chop(device, value.text)
    device.log(message="%s, hostname = %s " % (sub, hostname), level="debug")
    return hostname
# end def get_chassis_hostname


def get_chassis_list(device):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis List  device=${device_object}

    Gets slots list in chassis

    :param device:
        **REQUIRED** Device handle

    :retuns: List of slots in chassis
    """
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    chassis_list = []
    device.log(message="Inside %s... function" % sub)
    if re.search("^TX Matrix", model, re.I):
        chassis_list = ['scc']
    elif re.search("^TXP", model, re.I):
        chassis_list = ['sfc 0']
    lcc_list = get_fru_slots(device, fru='lcc')
    if isinstance(lcc_list, list):
        for element in lcc_list:
            chassis_list.append("lcc " + element)
    else:
        chassis_list.append(lcc_list)
    return chassis_list
# end def get_chassis_list


def get_chassis_memory(device):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Memory  device=${device_object}

    Get chassis memory using the cli command
    "show system processes extensive | grep chassisd"

    :param device:
        **REQUIRED** Device handle

    :return :
          Returns an array [<size>, <res>] from cli output for show
          system processes extensive. Both <size> and <res> are given in bytes
    """
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s ..." % sub)
    cmd = "show system processes extensive | grep chassisd"
    response = device.cli(command=cmd).response()
    match = re.search(
        r'^\s*\d+\s+root\s+\S+\s+\S+\s+\S+\s+(\S+)\s+(\S+).*chassisd',
        response)
    if match:
        size = match.group(1)
        searched = re.search('M$', size)
        if searched:
            size = re.sub('M$', '000000', str(size))
        searched1 = re.search('K$', size)
        if searched1:
            size = re.sub('K$', '000', str(size))
        res = match.group(2)
        res = re.sub('K$', '000', str(res))
        device.log(
            message="%s: return [size(%s), res(%s)]" % (sub, size, res),
            level="debug")
        return [size, res]
# end def get_chassis_memory


def get_chassis_mib(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Mib  device=${device_object}

    Get chassis mib variable value from jnxbox

    :param device:
        **REQUIRED** Device handle
    :param  mib :
        **OPTIONAL** Mib variable to poll (default is jnxBox)
    :param host :
        **OPTIONAL** FreeBsd host used for snmp query (default is sinkhole)

    :return:
         Returns dictionary of chassis mac-addressess
    """
    valid_keys = ['host', 'mib', 'mib_dir']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    oid = kwargs.get('mib', 'jnxBox')
    host = kwargs.get('host', 'sinkhole')
    mib_dir = kwargs.get('mib_dir')
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s ..." % sub, level="debug")

    if mib_dir == "":
        device.log(message='Invalid Router Version.', level="warn")

    bsd = Unix(host=host, user="regress", password="MaRtInI")
    test_cmd = 'test -d %s && echo exists' % mib_dir
    # resp = bsd.shell(command=test_cmd).response()
    test_res = getattr(bsd, 'shell')(command=test_cmd)
    resp = test_res.response()

    if not resp or not re.search(r'exists', resp):
        device.log(message="%s /jnxbox.mib is not found++" % mib_dir,
                   level="error")
        # bsd.close()
        getattr(bsd, 'close')()
        return False
    snmp_cmd = "/usr/local/bin/snmpwalk -Os -M %s -m all %s public %s" \
               % (mib_dir, get_chassis_hostname(device), oid)
    device.log(message="%s..." % snmp_cmd, level="debug")

    # snmp_out = bsd.shell(command=snmp_cmd, timeout=120).response()
    snmp_out_res = getattr(bsd, 'shell')(command=snmp_cmd, timeout=120)
    snmp_out = snmp_out_res.response()
    # bsd.close()
    getattr(bsd, 'close')()
    mib_data = {}
    oid_mod = {}
    chas_mib = {'chassis': {}}
    for line in snmp_out.split('\n'):
        print(line)
        device.log(message="%s:  %s" % (sub, line), level="debug")
        if re.search('^(.*) = (.*)', line):
            match = re.search('^(.*) = (.*)', line)
            name = match.group(1)
            value = match.group(2)
            mib_data[name] = value
            err_msg = sub + ': Index error for ' + line
            matched1 = re.search(r'^(jnx.*L1Index)\.\d+\.(\d+)', name)
            matched2 = re.search(r'^(jnx.*L2Index)\.\d+\.\d+\.(\d+)', name)
            matched3 = re.search(r'^(jnx.*L3Index)\.\d+\.\d+\.\d+\.(\d+)',
                                 name)
            matched4 = re.search(r'^(jnx.*Index)\.(\d+)', line)
            matched5 = re.search(r'^(\S+)Descr\.(\d+\.\d+\.\d+\.\d+)$', name)
            matched6 = re.search(r'^(\S+)Name\.(\d+\.\d+\.\d+\.\d+)$', name)
            matched7 = re.search(r'^(jnxContainers)Descr\.(\d+)$', name)
            matched8 = re.search(r'^(jnxBox\S+).0$', name)
            if matched1:
                if not matched1.group(2) == value:
                    device.log(message=err_msg, level="error")
            elif matched2:
                if not matched2.group(2) == value:
                    device.log(message=err_msg, level="error")
            elif matched3:
                if not matched3.group(2) == value:
                    device.log(message=err_msg, level="error")
            elif matched4:
                if not matched4.group(2) == value:
                    device.log(message=err_msg, level="error")
            elif matched5 or matched6:
                if matched5:
                    table = matched5.group(1)
                    oid = matched5.group(2)
                else:
                    table = matched6.group(1)
                    oid = matched6.group(2)
                mod = value
                mod = mod.lower()
                match1 = re.search(r'^routing engine (\d+)$', mod)
                match2 = re.search(r'^routing engine$', mod)
                match3 = re.search(r'^routing engine (.*)$', mod)
                match4 = re.search(r'^(\S+) slot (\d+)$', mod)
                match5 = re.search(r'^pic.*@ (\d+)/(\d+)/\*$', mod)
                match6 = re.search(r'^fpc.*@ (\d+)/\*/\*$', mod)
                match7 = re.search(r'^(sfm \d+ spr)', mod)
                if match1:
                    mod = 're' + str(match1.group(1))
                elif match2:
                    mod = 're'
                elif match3:
                    mod = 're' + str(match3.group(1))
                elif match4:
                    mod = 're' + str(match4.group(2))
                elif match5:
                    mod = 'pic' + str(match5.group(1)) + str(match5.group(2))
                elif match6:
                    mod = 'fpc' + str(match6.group(1))
                elif match7:
                    mod = match7.group(1)
                oid_mod.setdefault(table, {})
                oid_mod[table][oid] = mod
            elif matched7:
                table = matched7.group(1)
                oid = matched7.group(2)
                mod = value
                mod = mod.lower()
                if mod == 'routing engine slot':
                    mod = "re slot"
                oid_mod.setdefault(table, {})
                oid_mod[table][oid] = mod
            elif matched8:
                chas_mib['chassis'][matched8.group(1)] = value
    show_data(device, oid_mod, sub + ' : oid_mod')
    for key,value in mib_data.items():
        _match1 = re.search(
            r'^jnx(Contents|Containers|ContentsContainer|Contents|Filled|' +
            r'Operating|Redundancy|FruContents)(\S+)\.(\d+\.\d+\.\d+\.\d+)$',
            key)
        _match2 = re.search(r'^jnx(Containers)(\S+)\.(\d+)$', key)
        if _match1 or _match2:
            if _match1:
                table = 'jnx' + str(_match1.group(1))
                mib = 'jnx' + str(_match1.group(1)) + str(_match1.group(2))
                try:
                    mod = oid_mod[table][_match1.group(3)]
                except Exception:
                    continue
            else:
                table = 'jnx' + str(_match2.group(1))
                mib = 'jnx' + str(_match2.group(1)) + str(_match2.group(2))
                try:
                    mod = oid_mod[table][_match2.group(3)]
                except Exception:
                    continue
            chas_mib.setdefault(mod, {})
            chas_mib[mod][mib] = value

    show_data(device, chas_mib, sub + 'return:')
    return chas_mib
# end def get_chassis_mib


def get_chassis_pid(device):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
        ${result} =  Get Chassis Pid  device=${device_object}

    Gets chassis process id from the processes running in the chassis
    using cli command "show system processes extensive | grep chassisd""

    :param device:
        **REQUIRED** Device handle

    :return:
        Chassis process ID
    """
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="inside %s subroutine" % sub, level="debug")
    response = device.cli(
        command='show system processes | grep chassisd').response()
    match = re.search(r'^\s*(\d+)\s+.*/usr/sbin/chassisd.*$', response)
    if match:
        return match.group(1)
    return None
# end def get_chassis_pid


def get_chassis_temperature(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${sample_env_dict}  = Evaluate  ({'fpc1':{'status':'OK',
    ...    'temperature':'35 degrees C/ 95 degrees F'}})
    ${result} =  Get Chassis Temperature  device=${device_object}
    ...    chassis='sfc 0'  env=${sample_env_dict}

    Get chas min/max values of chassis fru temperatures

    :param device:
        **REQUIRED** Device handle
    :params chassis:
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :params env:
        **REQUIRED** return value of get_chassis_environment

    :return:
        list of maximum and minimum temperature
    """
    valid_keys = ['chassis', 'env']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    if 'env' in kwargs:
        env = kwargs.get('env')
    else:
        env = get_chassis_environment(device, chassis=chassis)
    maximum = 0
    minimum = 9999
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s function %s ..." % (sub, str(kwargs)))
    for element in env.keys():
        if 'temperature' in env[element]:
            temperature = env[element]['temperature']
            device.log(message="%s: checking temperature (%s) for fru (%s) ..."
                       % (sub, temperature, element), level="debug")
            match = re.search(r'^(\d+)\s+degrees', temperature)
            if match:
                if int(match.group(1)) > maximum:
                    maximum = int(match.group(1))
                if int(match.group(1)) < minimum:
                    minimum = int(match.group(1))
            else:
                device.log(
                    message="%s: incorrect temperature (%s) " % (
                        sub, temperature) +
                    "from chassis environment", level="error")
    if minimum == 0 or maximum == 9999:
        device.log(
            message="%s: incorrect max and " % sub +
            "min temperature from chassis environment", level="error")
        return None
    return [maximum, minimum]
# end def get_chassis_temperature


def get_fru_backup(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fru Backup  device=${device_object}  chassis='sfc 0'
    ...    fru='pcg'

    Get backup fru slot number

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param fru :
        **REQUIRED** pcg|scg
    :param status :
        **OPTIONAL** dictionary for fru status or gets data from get_fru_status

    :return:
        backup fru slot number
    """
    valid_keys = ['fru', 'chassis', 'status']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    fru = kwargs.get("fru")
    chassis = kwargs.get("chassis")
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s subroutine" % sub, level="debug")
    if 'status' in kwargs:
        status = kwargs.get("status")
    else:
        status = get_fru_status(device, chassis=chassis, fru=fru)
    show_data(device, status, "%s : %s %s" % (sub, fru, status))
    backup = None
    for value in range(0, len(status)):
        match = re.search(r'^(backup|Online - Standby)$',
                          status[value]["state"], re.I)
        if status[value]["status"] == 'Standby' or match:
            backup = value
            break
    return backup
# end def get_fru_backup


def get_fru_status(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fru Status  device=${device_object}

    Description:
        Get chassis FRU information using cli show chassis <fru> and
        cli show chassis fpc pic-status  commands

    :param device:
        **REQUIRED** Device handle
    :params chassis:
        **OPTION** scc | lcc 0|1|2|3
    :params sd:
        **OPTION** rsd | psd1|psd2|psd3|..
    :params fru :
        **OPTION** fpc|sib|spmb|sfm|re|feb|cfeb|scb|ssb|pic or
        an list
    :params slot:
        **OPTION** fru slot number

     :return: list or dictionary of a fru status (depends on the option
         type for fru/slot)

    """
    chassis = kwargs.get('chassis', '')
    sd = kwargs.get('sd')
    fru = kwargs.get('fru', get_test_frus(device))
    slot = kwargs.get('slot')
    mid = kwargs.get('mid')

    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s ..." % (sub, str(kwargs)), level='debug')
    fru_status = {}
    if isinstance(fru, list):
        for ele in fru:
            if not (re.search(r"scc|sfc 0", chassis,
                              re.I) and re.search(r'^(pic|fpc|scg)$', ele)):
                fru_status[ele] = get_fru_status(device, chassis=chassis,
                                                 sd=sd, fru=ele, slot=slot)
        return fru_status
    else:
        fru_status = []
    if re.search(r'^TX Matrix|TXP$', model) and (not chassis) and fru != 'lcc':
        chassis_list = get_chassis_list(device)
        for chassis in chassis_list:
            device.log(message="%s: chassis(%s), fru(%s)"
                       % (sub, chassis, fru), level='debug')
            if not (chassis == 'scc' and
                    re.search(r'^(pic|fpc|scg)$', fru)):
                fru_status.append(get_fru_status(
                    device, chassis=chassis, fru=fru, slot=slot))
        show_data(device, fru_status, "%s return:" % sub)
        return fru_status

    version = device.get_version()
    if (fru == 'fpc' and (not chassis or
                          re.search(r"scc|sfc 0", chassis, re.I))) or \
            re.search(r'^(sib|spmb|sfm|re|feb|cfeb|scb|ssb|lcc|psd)$', fru):
        if fru == 're':
            cli_cmd = "show chassis routing-engine"
            fru_name = 'route-engine'
        elif fru == 'sib' and version != '6.1':
            if re.search(r'ptx', model, re.IGNORECASE):
                cli_cmd = "show chassis sib"
            else:
                cli_cmd = "show chassis spmb sib"
            fru_name = 'sib'
        else:
            cli_cmd = "show chassis %s" % fru
            if re.search(r'^(sfm|scb|ssb|feb|cfeb)$', fru):
                fru_name = 'scb'
            else:
                fru_name = fru
        if chassis and fru != 'lcc':
            cli_cmd += " %s" % chassis
        if mid:
            cli_cmd += " member %s" % mid
        cli_cmd += " | no-more"

        rpc_str = device.get_rpc_equivalent(command=str(cli_cmd))
        response = device.execute_rpc(command=rpc_str).response()

        tmp = 'multi-routing-engine-results/multi-routing-engine-item'
        if re.search(r'^TX Matrix|TXP$', model) and fru != 'lcc':
            chassis_items = response.findall('.//%s' % tmp)
        elif re.search(r'^psd$', model) and fru != 're':
            chassis_items = response.findall('.//%s' % tmp)
        elif mid and re.search(
                r'ex45|ex42|ex43|ex34|ex23|ex8208|ex8216|ex33|ex-xre|mx',
                model):
            chassis_items = response.findall('.//%s' % tmp)
        else:
            chassis_items = response.findall('.//%s' % fru_name)

        for chassis_item in chassis_items:
            for child in chassis_item.getchildren():
                if chassis_item.find('slot') is None:
                    slot_name = 0
                else:
                    slot_name = int(
                        __chop(device, chassis_item.find('slot').text).lower())
                key = child.tag
                fru_status = fru_status +\
                    [None] * (slot_name + 1-len(fru_status))
                if fru_status[slot_name] is None:
                    fru_status[slot_name] = {}

                if key == 'state' and fru == 'spmb':
                    if chassis_item.\
                            find('state').text == "Online - Standby":
                        fru_status[slot_name]['state'] = 'Online'
                        fru_status[slot_name]['status'] = 'Standby'
                    elif chassis_item.find('state').text == 'Online':
                        fru_status[slot_name]['state'] = 'Online'
                        fru_status[slot_name]['status'] = 'Master'
                if key == 'mastership-state' and fru == 're':
                    fru_info = chassis_item.\
                            find('mastership-state').text
                    matched = re.search(
                        r'^(local\sChassis|Protocol)\s(.*?)$',
                        fru_info, re.I)
                    if matched and mid:
                        vstat = matched.group(1)
                        state = matched.group(2)
                        if re.search(r'^Local', vstat, re.I):
                            fru_info = 'Backup'
                        if re.search(r'^Protocol', vstat, re.I):
                            fru_info = state
                    fru_status[slot_name]['state'] = fru_info

                fru_status[slot_name][key] = __chop(
                    device, chassis_item.find(key).text)
    elif fru and re.search(r'^fabric (plane|control-board)$', fru):
        return get_fabric_status(device, slot=slot)

    elif fru and fru == 'pic':
        if slot:
            cli_cmd = "show chassis pic fpc-slot %s pic-slot %s" \
                      % (slot[0], slot[1])
            if chassis:
                cli_cmd += " %s" % chassis
            if mid:
                cli_cmd += " member %s" % mid
            rpc_str = device.get_rpc_equivalent(command=cli_cmd)
            response = device.execute_rpc(command=rpc_str).response()

            tmp = "multi-routing-engine-results/multi-routing-engine-item"
            if re.search(r'^TX Matrix|TXP$', model, re.I):
                chassis_items = response.findall('.//pic-detail/%s' % tmp)
            if mid and model in\
                    'ex45|ex42|ex43|ex34|ex23|ex8208|ex8216|ex33|ex-xre':
                chassis_items = response.findall('.//pic-detail/%s' % tmp)
            if re.search(r'^mx|MX', model, re.I):
                fru_status = {}
                chassis_items = response.findall('.//fpc/')

            for chassis_item in chassis_items:
                for child in chassis_item.getchildren():
                    key = child.tag

                    slot_name = int(__chop(
                        device, chassis_item.find('slot').text).lower())
                    if not re.search(r'^mx|MX', model, re.I): fru_status = fru_status + [None] * (slot_name + 1-len(fru_status))

                    if slot_name not in fru_status or fru_status[slot_name] is None:
                        fru_status[slot_name] = {}

                    fru_status[slot_name][key] = \
                        __chop(device, chassis_item.find(key).text)
        else:
            pic_status = get_pic_status(device,
                                        chassis=chassis,
                                        sd=sd,
                                        mid=mid)
            if mid and mid in pic_status.keys():
                pic_status = pic_status[mid]
            else:
                return []

            for i in range(len(pic_status)):
                pic_list = pic_status[i]
                fru_status = fru_status + [None] * (i+1-len(fru_status))
                fru_status[i] = []
                if isinstance(pic_list, list):
                    for j in range(len(pic_list)):
                        device.log(
                            message="%s: get pic info for slot([%s, %s])"
                            % (sub, i, j))
                        fru_status[i] = fru_status[i] + [None] *\
                            (j+1-len(fru_status[i]))
                        tmp = get_fru_status(device,
                                             chassis=chassis,
                                             sd=sd,
                                             fru='pic',
                                             slot=[i, j],
                                             mid=mid)

                        fru_status[i][j] = tmp[0]

    else:
        if chassis and chassis == 'scc' and fru == 'scg':
            device.log(message="%s: scg is not available on SCC" % sub)
            return []
        if fru == 'pem' and re.search(r'^(m5|m[124]0)$', model):
            env = get_chassis_environment(device, chassis=chassis)
            for i in range(2):
                pem_status = env["pem %s" % i]['status']
                if pem_status == 'OK':
                    fru_status.append({'state': 'Online'})
                else:
                    fru_status.append({'state': pem_status})
        elif fru != 'fan':
            return get_chassis_environment(device, chassis=chassis,
                                           fru=fru, slot=slot)
        else:
            return []
    show_data(device, fru_status, "%s return:" % sub)
    return fru_status
# end def get_fru_status


def get_fabric_status(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fabric Status  device=${device_object}  slot=${2}

    Gets chassis fabric summary management state using cli
    command "show chassis fabric summary" for M120 model only

    :param device:
        **REQUIRED** Device handle
    :param slot:
        **REQUIRED** fru slot number

    :returns:
        list or dictionary of fabric plane status
    """
    slot = kwargs.get('slot')
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s(%s)) ..." % (sub, str(kwargs)))
    models = "^(m120|mx960|mx240|mx480|a40|srx5800|a15|a20|srx5600|" +\
             "srx5400|a10|srx3600|a2|srx3400|ex82[01][68]|ptx[0-9]*)$"
    fabric_status = []
    if not re.search(models, model, re.IGNORECASE):
        device.log(
            message="%s is not supported on >%s< platform" % (sub, model))
        return fabric_status
    response = device.cli(command="show chassis fabric summary",
                          format='text').response()
    for line in response.split('\n'):
        matched1 = re.search(r'^\s*(\d+)\s+(\S+)\s+(\d+\w+.*)$', line)
        matched2 = re.search(r'^\s*(\d+)\s+(\S+)\s*$', line)
        matched3 = re.search(r'(\w+[0-9])\s+(\w+)\s*(\w*)', line)
        if matched1:
            plane = int(matched1.group(1))
            fabric_status = fabric_status + \
                [None] * (plane + 1 - len(fabric_status))
            fabric_status[plane] = {}
            fabric_status[plane]['state'] = matched1.group(2)
            fabric_status[plane]['uptime'] = __get_uptime(device,
                                                          matched1.group(3))
        elif matched2:
            plane = int(matched2.group(1))
            fabric_status = fabric_status + \
                [None] * (plane + 1 - len(fabric_status))
            fabric_status[plane] = {}
            fabric_status[plane]['state'] = matched2.group(2)
            fabric_status[plane]['uptime'] = 0

        elif matched3:
            status = {}
            fru = matched3.group(1)
            status[fru] = {'state': matched3.group(2)}
            if matched3.group(3):
                status[fru]['error'] = matched3.group(3)
            else:
                status[fru]['error'] = ''
            fabric_status.append(status)

    if slot:
        return fabric_status[slot]
    device.log(message="%s: return\n %s" % (sub, pprint(fabric_status)))
    return fabric_status
# end def get_fabric_status


def get_fabric_plane(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fabric Plane  device=${device_object}  plane=${2}

    Gets chassis fabric plane summary state and links status
    using cli command "show chassis fabric summary"
    for M120/MX960/MX240/MX480 only

    :param device:
        **REQUIRED** Device handle
    :param plane:
        **REQUIRED** plane number

    :returns:
        list or dictionary of fabric plane status
    """
    arg_str = str(kwargs)
    slot = kwargs.get('slot')
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s(%s) ..." % (sub, arg_str))
    models = "^(m120|mx960|mx240|mx480|a40|srx5800|a15|a20|srx5600|" +\
        "srx5400|a10|srx3600|a2|srx3400|ex82[01][68])$"
    fabric_status = {}
    if not re.search(models, model, re.IGNORECASE):
        device.log(
            message="%s is not supported on >%s< platform" % (sub, model))
        return fabric_status
    response = device.cli(
        command="show chassis fabric plane", format='text').response()
    for line in response.split('\n'):
        matched1 = re.search(r'^Plane\s+(\d+)', line)
        matched2 = re.search(r'^\s+Plane state:\s+(\S+)', line)
        if re.search(r'^m120$', model, re.I):
            matched3 = re.search(r'^\s+FEB\s+(\d+)', line)
            plane_type = 'feb'
        else:
            matched3 = re.search(r'^\s+FPC\s+(\d+)', line)
            plane_type = 'fpc'
        matched4 = re.search(r'^\s+PFE\s+(\d+)\s+:Links\s+(\S+)', line)
        if matched1:
            plane = matched1.group(1)
            fabric_status[plane] = {}
            fabric_status[plane]['links'] = {}
            fabric_status[plane]['links'][plane_type] = {}
        elif matched2:
            fabric_status[plane]['state'] = matched2.group(1)
        elif matched3:
            fpc = matched3.group(1)
            fabric_status[plane]['links'][plane_type][fpc] = {}
            fabric_status[plane]['links'][plane_type][fpc]['pfe'] = {}
        elif matched4:
            match1 = matched4.group(1)
            match2 = matched4.group(2)
            fabric_status[plane]['links'][plane_type][fpc]['pfe'][
                match1] = match2
    if slot:
        return fabric_status.get(str(slot))
    device.log(message="%s: return %s\n" % (sub, pprint(fabric_status)))
    return fabric_status
# end def get_fabric_plane


def get_fabric_feb(device, slot=None):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fabric Feb  device=${device_object}  slot=${2}

    Gets chassis summary fabric management state from fabric_feb point
    of view using cli command "show fabric feb" for M120 only

    :param device:
        **REQUIRED** Device handle
    :param slot:
        *OPTIONAL* fru slot number

    :returns:
        list or dictionary of fabric plane status
    """
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s subroutine" % sub, level="debug")
    fabric_status = {}
    if model != 'm120':
        device.log(
            message=" %s is not supported on >%s< platform" % (sub, model),
            level="error")
        return fabric_status
    response = device.cli(command="show chassis fabric feb").response()
    for line in response.split('\n'):
        matched = re.search(r'^FPC\s+(\d+)', line)
        matched1 = re.search(r'^\s+PFE\s+#(\d+)', line)
        matched2 = re.search(r'^\s+Plane\s+(\d+):\s+Plane\s+(\S+)', line)
        if matched:
            feb = matched.group(1)
            fabric_status[feb] = {}
            fabric_status[feb]['pfe'] = []
        elif matched1:
            pfe = int(matched1.group(1))
            fabric_status[feb]['pfe'].insert(pfe, {})
            fabric_status[feb]['pfe'][pfe]['plane'] = {}
        elif matched2:
            fabric_status[feb]['pfe'][pfe]['plane'][
                matched2.group(1)] = matched2.group(2)
    if slot is not None:
        if str(slot) in fabric_status.keys():
            return fabric_status[str(slot)]
        else:
            device.log(message="%s : slot not found " % sub, level="error")
    device.log(
        message="%s : return\n %s" % (sub, fabric_status), level="debug")
    return fabric_status
# end def get_fabric_feb


def get_fabric_fpc(device, slot=None):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fabric Fpc  device=${device_object}  slot=${2}

    Gets chassis summary fabric management state from fpc point of
    view using cli command "show chassis fabric fpcs" for MX960 only

    :param device:
        **REQUIRED** Device handle
    :param slot:
        **REQUIRED** fru slot number

    :returns:
        list or dictionary of fabric plane status
    """
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s subroutine" % sub, level="debug")
    models = "^(mx960|mx240|mx480|a40|srx5800|a15|a20|" \
             "srx5600|srx5400|a10|srx3600|a2|srx3400|ex82[01][68]|ptx[0-9]*)"
    fabric_status = {}
    if not re.search(models, model, re.IGNORECASE):
        device.log(
            message=" %s is not supported on >%s< platform" % (sub, model))
        return fabric_status
    response = device.cli(command="show chassis fabric fpcs").response()
    for line in response.split('\n'):
        matched = re.search(r'^FPC\s+[#]*(\d+)', line)
        matched1 = re.search(r'^\s+PFE\s+#(\d+)', line)
        if re.search("ptx[0-9]*", model, re.IGNORECASE):
            matched2 = re.search(r'\s+\(plane\s+(\d+)\)\s+(.*)', line)
        else:
            matched2 = re.search(r'^\s+Plane\s+(\d+):\s+(.*)', line)
        if matched:
            fpc = matched.group(1)
            fabric_status[fpc] = {}
            fabric_status[fpc]['pfe'] = []
        elif matched1:
            pfe = int(matched1.group(1))
            fabric_status[fpc]['pfe'].insert(pfe, {})
            fabric_status[fpc]['pfe'][pfe]['plane'] = {}
        elif matched2:
            fabric_status[fpc]['pfe'][pfe]['plane'][
                matched2.group(1)] = matched2.group(2)
    if slot is not None:
        if str(slot) in fabric_status.keys():
            return fabric_status[str(slot)]
    device.log(
        message="%s : return\n %s" % (sub, pprint(fabric_status)),
        level="debug")
    return fabric_status
# end def get_fabric_fpc


def get_chassis_interface(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Interface  device=${device_object}
    ...    interface_name='pfh-0/0/0'  skip_interface='fe-2/2.*'

    Gets chassis interface information

    :param device:
        **REQUIRED** Device handle
    :param interface_name:
        **REQUIRED** interface name
    :param skip_interface:
        **REQUIRED**  regular expression for interface to skip checking
        (i.e. 'fxp.*|lo.*')

    :returns:
        list of physical interface information
    """
    valid_keys = ['interface_name', 'skip_interface']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    interface_name = kwargs.get('interface_name', '')
    skip_interface = kwargs.get('skip_interface', '')
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s subroutine" % sub, level="debug")
    # chassis_interface = {}
    # execute show interfaces command for all/given interface
    cli_cmd = "show interfaces"
    if interface_name:
        cli_cmd += " %s" % interface_name
    cli_cmd += " terse"
    # execute show interfaces command for all/given interface
    res = device.cli(command=cli_cmd, format='xml').response()
    response = jxmlease.parse(res)['rpc-reply']['interface-information'][
        'physical-interface']
    response = response.jdict()
    # Convert the xml output into dictionary type
    response = ast.literal_eval(str(response))
    chassis_interface = response
    for key in list(response):
        if skip_interface and re.search("^"+skip_interface+"$", key, re.I):
            del chassis_interface[key]
    return chassis_interface
# end def get_chassis_interface


def get_chassis_mac(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Mac  device=${device_object}  chassis='sfc 0'

    Gets chassis mac addresses information using "show chassis mac-addresses"

    :param device:
        **REQUIRED** Device handle
    :params chassis :
        **REQUIRED** Chassis for which the MAC address is obtained

    :returns:
        dictionary of chassis mac-addresses
    """
    chassis = kwargs.get('chassis', '')
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s subroutine" % sub, level="debug")
    # calling __cli_get_mac to get details
    return __cli_get_mac(device, chassis=chassis)
# end def get_chassis_mac


def get_chassis_status(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Status  device=${device_object}  chassis='sfc 0'
    ...    sd='rsd'

    Gets chassis status for all test frus.
    -> gets fru status.
    -> gets chassis hardware details from get_chassis_hardware
    -> gets craft information from get_chassis_craft
    -> gets chassis interface details from get_chassis_interface
    -> gets chassis alarms from get_chassis_alarm

    :param device:
        **REQUIRED** Device handle
    :param chassis:
       **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param sd:
       **REQUIRED** rsd | pfd1 | psd2 | psd3
    :param skip_interface:
       **OPTIONAL** regular expression for interface to skip checking
       (i.e. 'fxp.*|lo.*')
    :param hardware:
       **OPTIONAL** dictionay  for hardware inventory
    :param interface:
       **OPTIONAL** dictionary of interface name
    :param fru:
       **OPTIONAL** re | fpc | sib | sfm | pcg | scg | cb | pem
    :param alarm:
       **OPTIONAL** list of alarm
    :param craft:
       **OPTIONAL** dictionary of craft display
    :param memory:
       **OPTIONAL** List of [SIZE,RES] from show system process extensive
       for chassisd. It can be returned from get_chassis_memory() previously

    :returns:
        dictionary of fru using get_fru_status(), get_chassis_alarm(),
        get_chassis_craft(), get_chassis_hardware(), get_chassis_interface
    """
    valid_keys = ['chassis', 'sd', 'interface', 'skip_interface', 'fru',
                  'hardware', 'alarm', 'memory', 'craft']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    sd = kwargs.get('sd')
    hardware = kwargs.get('hardware', 1)
    interface = kwargs.get('interface', 1)
    fru = kwargs.get('fru', 1)
    alarm = kwargs.get('alarm', 1)
    craft = kwargs.get('craft', 1)
    memory = kwargs.get('memory', 1)
    skip_interface = kwargs.get('skip_interface')
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s subroutine (%s)" % (sub, str(kwargs)),
               level="debug")
    status = {}
    if fru:
        # for fru status
        status['fru'] = {}
        status['fru'] = get_fru_status(device, chassis=chassis, sd=sd)
    if hardware and CHECK_HARDWARE:
        # for hardware status
        status['hardware'] = {}
        status['hardware'] = get_chassis_hardware(device, chassis=chassis)
    if craft and CHECK_LED:
        # for craft status
        status['craft'] = {}
        status['craft'] = get_chassis_craft(device, chassis=chassis)
    if interface and CHECK_INTERFACE:
        # for interface status
        status['interface'] = {}
        status['interface'] = get_chassis_interface(
            device, skip_interface=skip_interface)
    if alarm and CHECK_ALARM:
        # for alarm status
        status['alarm'] = {}
        status['alarm'] = get_chassis_alarm(device, chassis=chassis, sd=sd)
    if memory and CHECK_MEMORY:
        # for memory status
        status['mem'] = {}
        status['mem'] = get_chassis_memory(device)
    show_data(device, status, sub + " return:")
    return status
# end def get_chassis_status


def get_pic_status(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =    Get Handle    resource=r1
    ${result} =    Get Pic Status    device=${device_object}    chassis='sfc 0'
    ...    sd='rsd'

    Gets the pic status using the cli command "show chassis fpc pic-status"

    :param device:
        **REQUIRED** Device handle
    :param chassis:
       **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param sd:
       **REQUIRED** rsd | pfd1 | psd2 | psd3

    :return:
        Dictionary of PIC details for fpc slots
    """
    valid_keys = ['chassis', 'sd', 'fru', 'status', 'state', 'mid']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    sd = kwargs.get('sd')
    mid = kwargs.get('mid')
    pic_status = {}
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s  function ..." % sub)
    cli_cmd = "show chassis fpc pic-status "
    if chassis:
        cli_cmd += chassis
    if mid:
        cli_cmd += "member " + mid
    rpc_str = device.get_rpc_equivalent(command=cli_cmd)
    chassis_item = device.execute_rpc(command=rpc_str).response()
    if re.search(r'^TX Matrix|TXP$', model, re.I):
        chassis_items = chassis_item.findall('.//multi-routing-engine-item')
        if not chassis:
            for chassis_item in chassis_items:
                for child in chassis_item.getchildren():
                    key = child.tag
                    if key == "re-name":
                        re_name = __chop(device, child.text).lower()
                        cid = __get_cid(device, re_name)
                        pic_status[cid] = __get_pic_info(device, chassis_item)
            show_data(device, pic_status, "%s:  return" % sub)
            return pic_status

    if re.search(r'^psd$', model, re.I):
        chassis_items = chassis_item.findall('.//multi-routing-engine-item')
        for chassis_item in chassis_items:
            for child in chassis_item.getchildren():
                key = child.tag
                if key == "re-name":
                    re_name = __chop(device, child.text).lower()
                    cid = __get_cid(device, re_name)
                    pic_status[cid] = __get_pic_info(device, chassis_item)
        show_data(device, pic_status, "%s:  return" % sub)
        if sd:
            return pic_status[sd]
        else:
            return pic_status
    model_list = "(ex45|ex42|ex43|ex34|ex23|ex8208|ex8216|ex33|ex-xre)"
    match = re.search(model_list, model, re.I)
    if mid and match:
        chassis_items = chassis_item.findall('.//multi-routing-engine-item')
        for chassis_item in chassis_items:
            pic_status[mid] = __get_pic_info(device, chassis_item)
            show_data(device, pic_status, "%s:  return" % sub)
        return pic_status
    pic_status[chassis] = __get_pic_info(device, chassis_item)
    return pic_status
# end def get_pic_status


def get_fru_list(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fru List  device=${device_object}

    Gets the fru list and returns the key values of chassis fru's
    based on the model.

    :param device:
        **REQUIRED** Device handle

    :return:
        list containing key values of chassis fru's for the model.
    """
    test = kwargs.get('test')
    model = device.get_model().lower()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s subroutine" % sub, level="debug")
    # get fru list for chassis model
    test_frus = CHASSIS_FRU[model.lower()].keys()
    if test:
        show_data(device, test_frus, "%s, return" % sub)
    return list(test_frus)
# end def get_fru_list


def get_fru_slots(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fru Slots  device=${device_object}  chassis='sfc 0'
    ...    state='Online'

    Get fru slots in the corresponding state by doing the following
        - If fru is lcc then append lcc number to slots.
        - If model is TX Matrix or TXP then return the slots by
        calling get_fru_slots.
          To get all sib in online or spare state:
            Example: sib_slots = get_fru_slot
            (fru:'sib',state:'spare|online')
        - It should return list such as [0,1,2]

    :param device:
        **REQUIRED** Device handle
    :param chas:
        **OPTION** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param sd:
        **OPTION** rsd | psd1|psd2|psd3|
    :param fru:
        **OPTION** fru name (fpc|sfm|sib|spmb|scg|pcg|ssb|feb|pem|scb)
    :param status:
        **OPTIONAL** chassis status
    :param state:
        **REQUIRED** reqular expression for fru state (ignore case)

    :return:
        list of fru slots
    """
    valid_keys = ['chassis', 'sd', 'fru', 'status', 'state', 'mid']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    chassis = kwargs.get('chassis')
    sd = kwargs.get('sd')
    fru = kwargs.get('fru')
    status = kwargs.get('status',[])
    state = kwargs.get('state')
    mid = kwargs.get('mid')

    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s ..." % (sub, str(kwargs)),
               level='debug')
    slots = []
    members = []
    # if fru value is not given get fru values form get_fru_list()
    if not fru:
        fru = get_fru_list(device)
    # if fru value is list for each value of fru it calls get_fru_slots()
    if isinstance(fru, list):
        device.log(message="%s: fru(%s)" % (sub, fru))
        slots = {}
        for ele in fru:
            if not (chassis and re.search(r"scc|sfc 0", chassis, re.I)
                    and re.search(r'^(pic|fpc|scg)$', ele)):
                slots[ele] = get_fru_slots(device,
                                           chassis=chassis,
                                           sd=sd,
                                           fru=ele,
                                           state=state)
        show_data(device, slots, "%s for fru (%s) return" % (sub, fru))
        return slots

    # if the fru value is lcc
    if fru == 'lcc':
        cli_cmd = "show version brief"
        rpc_str = device.get_rpc_equivalent(command=cli_cmd)
        response = device.execute_rpc(command=rpc_str).response()
        chas_item = response.findall(
            ".//multi-routing-engine-results/multi-routing-engine-item")
        for slot in chas_item:
            slot = slot.find('re-name').text
            matched = re.search(r'^lcc(\d+)-re\d+$', slot)
            if matched:
                slots.append(matched.group(1))
        return slots
    # if model is TX Matrix | TXP and chassis value is not defined
    if re.search(r'^TX Matrix|TXP$', model) and not chassis:
        slots = {}
        for chas_ in get_chassis_list(device):
            device.log(message="%s: chas(%s), fru(%s)" % (sub, chas_, fru),
                       level='debug')
            if not (chas_ == 'scc' and re.search(r'^(pic|fpc|scg)$', fru)):
                slots[chas_] = get_fru_slots(device,
                                             chassis=chas_,
                                             sd=sd,
                                             status=status[chas_],
                                             fru=fru,
                                             state=state)
        show_data(device, slots, "%s return:" % sub)
        return slots
    # if mid value is not given and
    # model is ex45|ex42|ex43|ex34|ex23|ex8208|ex8216|ex33|ex-xre|mx
    if (not mid) and (re.search(r'ex45|ex42|ex43|ex34|'
                                r'ex23|ex8208|ex8216|ex33|ex-xre|mx', model)):
        cli_cmd = "show chassis hardware"
        rpc_str = device.get_rpc_equivalent(command=cli_cmd)
        response = device.execute_rpc(command=rpc_str).response()
        chassis_items = response.findall(".//multi-routing-engine-item")
        for chassis_item in chassis_items:
            for child in chassis_item.getchildren():
                key = child.tag
                if key == "re-name":
                    re_name = child.text.lower()
                    matched = re.search(r'^member(.*)', re_name)
                    if matched:
                        members.append(matched.group(1))
        # if there are values in members list
        if len(members) > 0:
            slots = {}
            for m in members:
                device.log(message="%s : fru(%s) member(%s)" % (sub, fru, m),
                           level='debug')
                if re.search(r'fpc|pic|re', fru):
                    slots["member%s" % m] = get_fru_slots(device,
                                                          fru=fru,
                                                          state=state,
                                                          mid=m)
            show_data(device, slots, "%s return:" % sub)
            return slots
    # if status value is not given get status values form get_fru_status()
    if not status:
        status = get_fru_status(device,
                                chassis=chassis, sd=sd, fru=fru, mid=mid)
    # if status value is not list then make is as list
    if not isinstance(status, list):
        status = [status]
    # for fru = 'pic'
    if fru == 'pic':
        for i in range(0, len(status)):
            show_data(device, status, "%s, status" % sub)
            fpc_info = status[i]
            if isinstance(fpc_info, list):
                for j in range(len(fpc_info)):
                    show_data(device, fpc_info, "%s, fpc_info" % sub)
                    if (not state or fpc_info[j]['state']) and\
                            re.search(r'^%s$' % state,
                                      __chop(device, fpc_info[j]['state']),
                                      re.I):
                        slots.append([i, j])
    # for all other fru values
    else:
        for i in range(0, len(status)):
            if not state:
                slots.append(i)
            elif status[i] and 'state' in status[i].keys():
                if re.search(state, __chop(device, status[i]['state']), re.I):
                    slots.append(i)
            else:
                if status[i]:
                    for data in status[i]:
                        if 'state' in status[i][data].keys() and \
                                re.search(state,
                                          __chop(device, status[i][data]['state']),
                                          re.I):
                            slots.append(int(data))
    show_data(device, slots, "%s for fru (%s) return" % (sub, fru))
    return slots
# end def get_fru_slots


def get_test_frus(device):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Test Frus  device=${device_object}

    Get all test fru names by doing the following
      - Get the field replaceable unit models from the global params
      - Call show_data by passing test_frus and return them.

    :param device:
        **REQUIRED** Device handle

    :return:
        list of test fru names
    """
    model = device.get_model().lower()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s   ..." % sub, level="debug")
    # test_frus = []
    # gets fru values from the chassis_fru dictionary
    test_frus = list(CHASSIS_FRU[model.lower()].keys())
    show_data(device, test_frus, sub + ", return")
    return test_frus
# end def get_test_frus


def get_spc_slots(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Spc Slots  device=${device_object}

    Get spc slots by doing the following using the cli command
    "show chassis hardware | match spc"

    :param device:
        **REQUIRED** Device handle
    :param node(string/integer):
        *OPTIONAL* node in SRX HA cluster environment, pass values as node-id, local, primary
    :return:
        either a scalar or list of spc slots depending on the context.
        If no spc slots found, it returns FALSE.
    """
    sub = function_name(device)
    spc_slots = []
    cli_cmd = "show chassis hardware | match spc"
    if 'node' in kwargs:
        cli_cmd = "show chassis hardware node " + str(kwargs.get('node')) + " | match spc"
    response = device.cli(command=cli_cmd, format='text').response()
    # returns spc slots from the command "show chassis hardware | match spc"
    for line in response.split('\n'):
        match = re.search(r'\s*FPC\s+(\d+)', line)
        if match:
            spc_slots.append(match.group(1))
    if spc_slots:
        device.log(message="In %s the spc slots are %s " % (sub, spc_slots),
                   level="debug")
        return spc_slots
    else:
        device.log(message="In %s No spc slots found" % sub, level="warn")
        return False
# end def get_spc_slots


def kill_chassisd(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  kill Chassisd  device=${device_object}  chassis='sfc 0'
    ...    check_slot=${2}  check_interface=${1}  skip_interface='fxp.*'
    ...    check_alarm=${1}  check_craft=${1}
    ...    check_hardware=${0}  check_memory=${1}  check_all=${0}

    Kills chassisd process

    :param device:
        **REQUIRED** Device handle
    :param chassis:
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param soft:
        **OPTIONAL** 1|0 chassid soft restart (default is 0, hard restart)
    :param status:
        **OPTIONAL** chassis status (default get it from get_chassis_status
        before kill chassisd)
    :param check_fru:
        **OPTIONAL** fru name or list of frus to check (default get all frus
        from CHAS_FRU)
    :param check_slot:
        **REQUIRED** a fru slot, a list of slots or a dictionary of fru slots
        for check_fru
    :param check_interface :
        **REQUIRED** 0|1 (1 get interfaces from get_chassis_interface()
        before kill chassisd)
    :param skip_interface:
        **REQUIRED** regular expression for interface to skip checking
        (i.e. 'fxp.*|lo.*')
    :param check_alarm:
        **REQUIRED** 0|1 (1 get alarm from get_chassis_alarm()
        before kill chassisd)
    :param check_craft:
        **REQUIRED** 0|1 (1 get craft display from get_chassis_craft()
        before kill chassisd)
    :param check_hardware:
        **REQUIRED** 0|1 (1 get hardware inventory from get_chassis_hardware()
        before kill chassisd)
    :param check_memory:
        **REQUIRED** 0|1 (1 get memory usage from get_chassis_memory()
        before kill chassisd)
    :param check_all:
        **REQUIRED** 0|1(check all:check_interface,check_hardware, check_fru,
        check_craft)
    :param check_count:
        **OPTIONAL** Check count for craft display (default 0 no checking)
    :param check_interval:
        **OPTIONAL** Wait time before next retry (default 10 seconds)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['skip_interface', 'status', 'check_interface',
                  'check_fru', 'check_slot', 'check_craft', 'check_hardware',
                  'check_memory', 'check_alarm', 'check_database',
                  'check_all', 'sleep_val', 'check_count', 'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    skip_interface = kwargs.get('skip_interface')
    status = kwargs.get('status')
    check_interface = kwargs.get('check_interface')
    check_fru = kwargs.get('check_fru')
    check_slot = kwargs.get('check_slot')
    check_craft = kwargs.get('check_craft')
    check_hardware = kwargs.get('check_hardware')
    check_memory = kwargs.get('check_memory')
    check_alarm = kwargs.get('check_alarm')
    check_database = kwargs.get('check_database')
    check_all = kwargs.get('check_all')
    sleep_val = kwargs.get('sleep_val', 4)
    check_count = kwargs.get('check_count')
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s %s ..." % (sub, str(kwargs)), level="debug")
    # Save chassis status first if not available
    if not status:
        status = get_chassis_status(device, skip_interface=skip_interface)
        # Kill chassisd
    device.su()
    kill_process(device, prog='/usr/sbin/chassisd')
    sleep(sleep_val)
    if check_all:
        if check_interface is None:
            check_interface = 1
        if check_hardware is None:
            check_hardware = 1
        if check_craft is None:
            check_craft = 1
        if check_alarm is None:
            check_alarm = 1
        if check_memory is None:
            check_memory = 1
        if check_database is None:
            check_database = 1
        # Check chassis status
    if check_chassis_status(device,
                            status=status,
                            skip_interface=skip_interface,
                            check_interface=check_interface,
                            check_hardware=check_hardware,
                            check_fru=check_fru,
                            check_memory=check_memory,
                            check_alarm=check_alarm,
                            check_slot=check_slot,
                            check_craft=check_craft,
                            check_count=check_count,
                            check_interval=check_interval):
        device.log(
            message="%s: check passed within retry %s times by %s seconds interval"
            % (sub, check_count, check_interval), level='info')
    else:
        device.log(
            message=" %s  : check failed after retry %s times by %s seconds interval"
            % (sub, check_count, check_interval), level="warn")
        return False
    return True
# end def kill_chassisd


def request_fru_offline(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =    Request Fru Offline    device=${device_object}
    ...    chassis='sfc 0'    fru='fpc'    slot=${2}    fru_if='ge-1/2/3'

    Offlines fru using cli command

    :param device:
        **REQUIRED** Device handle
    :param method:
        **OPTIONAL** request (default) | power
    :param chassis:
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param fru:
        **REQUIRED** fpc|sib|sfm|pcg|scg|cb|pic
    :param slot:
        **REQUIRED** FRU slot number
    :param interface:
        **REQUIRED** IFL or IFD name for fru: pic
    :param check_online:
        **OPTIONAL** Check if fru is online before offline it (default is 0)
    :param check_count:
        **OPTIONAL** Check count for fru offline(default is 0, no checking)
    :param check_interval:
        **OPTIONAL** Wait time before next retry (default 10 seconds)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['method', 'fru_if', 'chassis', 'fru', 'slot',
                  'check_database', 'check_online',
                  'check_count', 'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    method = kwargs.get('method', 'request')
    chassis = kwargs.get('chassis')
    fru = kwargs.get('fru', "")
    slot = kwargs.get('slot')
    check_database = kwargs.get('check_database', None)
    check_count = kwargs.get('check_count', None)
    check_interval = kwargs.get('check_interval', 10)
    check_online = kwargs.get('check_online', None)
    interface = kwargs.get("fru_if")
    model = device.get_model().lower()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s " % (sub, str(kwargs)), level="debug")
    if interface:
        if slot:
            raise Exception("%s: Cannot use both IF and SLOT arguments" % sub)

        interface1 = interface.split('-')
        slot = interface1[1].split('/')
    if not fru and not slot:
        __error_arg_msg(device, 'fru|slot', sub)
        return False
    if fru == 'pic' and isinstance(slot[0], list) or fru != 'pic' \
            and isinstance(slot, list):
        for slots in slot:
            value = request_fru_offline(device, chassis=chassis, fru=fru,
                                        slot=slots, check_online=check_online,
                                        check_count=check_count,
                                        check_interval=check_interval)
            if not value:
                return False
        device.log(message="%s:fru %s offline passed for slot %s"
                   % (sub, fru, pprint(slot)), level="debug")
        return True

    if check_online:
        if check_fru_state(device, chassis=chassis, fru=fru, state="Online"):
            device.log(message=" %s : %s is online" % (sub, fru),
                       level="debug")
        else:
            device.log(message="%s : %s is NOT online" % (sub, fru),
                       level="warn")
            return False

    if re.search(r'^(cb|pem|fpc|pcg|scg|sib|spmb|sfm|feb|ccg|fabric.*)$', fru):
        if method == 'power':
            cli_cmd = "test chassis %s slot %s power off" % (fru, slot)
        elif method == 'power_output':
            cli_cmd = "test chassis %s slot %s power-outputs off" % (fru, slot)
        elif method == 'request':
            cli_cmd = "request chassis %s offline" % fru
            if not re.search(r'^fabric', fru):
                cli_cmd += " slot"
            cli_cmd += " %s" % slot
        else:
            device.log(message=" %s: method should be request"
                               "(default)|power" % sub, level="error")
            return False
        if chassis:
            cli_cmd += " %s" % chassis
        device.cli(command=cli_cmd)
    elif fru == 'pic':
        cli_cmd = "request chassis pic offline fpc-slot %s pic-slot %s" % (
            slot[0], slot[1])
        if chassis:
            cli_cmd += " %s " % chassis
        device.cli(command=cli_cmd)
    else:
        device.log(message=" %s: invalid %s to offline" % (sub, fru),
                   level="error")

    if check_count:
        state = 'Offline'
        if re.search(r'^m[24]0$', model) and fru == 'fpc':
            state = 'Dormant|Offline'
        elif fru == 'cb':
            state = 'Offline|Present'
        if check_fru_state(device, chassis=chassis, fru=fru, slot=slot,
                           state=state, check_count=check_count,
                           check_interval=check_interval):
            device.log(message="%s: Offline fru %s passed for slot %s"
                       % (sub, fru, pprint(slot)), level="debug")

            if check_database:
                if check_chassis_database(device, fru=fru, dynamic=1):
                    device.log(
                        message="%s: check dynamic db for fru(%s) passed" % (
                            sub, fru), level="debug")
                else:
                    device.log(
                        message=" %s: check dynamic db for fru(%s) failed" % (
                            sub, fru), level="warn")
                    return False
        else:
            device.log(
                message="%s: offline fru failed for slot %s" % (sub,
                                                                pprint(slot)),
                level="warn")
            return False

        if fru == 'feb' and re.search(r'm120', model):
            i = 0
            for plane in get_fabric_plane(device):
                if plane['state'] == 'ACTIVE' and plane['links'][str(slot)]:
                    device.log(message="%s : link between FEB %s to fabric "
                                       "plane %s was not removed"
                               % (sub, slot, i), level="warn")
                i += 1
        elif fru == 'fabric plane' and re.search(r'm120', model):
            fb_plane = get_fabric_plane(device, plane=slot)
            if fb_plane['state'] == 'OFFLINE':
                device.log(message="%s :fabric plane %s should show offline"
                           % (sub, slot), level="warn")
            else:
                device.log(message="%s :fabric plane  %s not show offline"
                           % (sub, slot), level="error")
                return False

    return True
# end def request_fru_offline


def request_fru_online(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Request Fru Online  device=${device_object}    chassis='sfc 0'
    ...    fru='fpc'    slot=${2}

    Change the fru state into online using the cli command

    :param device:
        **REQUIRED** Device handle
    :param method:
       **OPTIONAL** request (default) | power
    :param chassis:
       **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param fru:
       **REQUIRED** fpc|sib|sfm|pcg|scg|cb|pic
    :param slot:
       **REQUIRED** FRU slot number
    :param check_offline:
       **OPTIONAL** Check if fru is offline before online it (default is 0)
    :param check_count:
       **OPTIONAL** Check count (default is 6)
    :param check_interval:
       **OPTIONAL** Wait time before next retry (default 10 seconds)

    :return:
       TRUE if the process has no error
       FALSE if the process has error
    """
    valid_keys = ['method', 'fru_if', 'chassis', 'fru', 'slot',
                  'check_offline', 'check_count', 'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    method = kwargs.get('method', 'request')
    chassis = kwargs.get('chassis')
    fru = kwargs.get('fru', "")
    slot = kwargs.get('slot')
    check_count = kwargs.get('check_count', None)
    check_interval = kwargs.get('check_interval', 10)
    check_offline = kwargs.get('check_offline', None)
    interface = kwargs.get("fru_if")
    model = device.get_model().lower()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s " % (sub, str(kwargs)), level="debug")
    if interface:
        if slot:
            raise Exception("%s: Cannot use both IF and SLOT arguments" % sub)

        interface1 = interface.split('-')
        slot = interface1[1].split('/')
    if not fru and not slot:
        __error_arg_msg(device, 'fru|slot', sub)
        return False
    if fru == 'pic' and isinstance(slot[0], list) or fru != 'pic' \
            and isinstance(slot, list):
        for slots in slot:
            value = request_fru_online(device, chassis=chassis, fru=fru,
                                       slot=slots, check_offline=check_offline,
                                       check_count=check_count,
                                       check_interval=check_interval)
            if not value:
                return False
        device.log(message="%s:fru %s offline passed for slot %s"
                   % (sub, fru, pprint(slot)), level="debug")
        return True

    if check_offline:
        exp_state = 'offline'
        if re.search(r'^m[24]0$', model) and fru == 'fpc':
            exp_state = 'Dormant|Offline'
        if check_fru_state(device, chassis=chassis, fru=fru,
                           state=exp_state, slot=slot):
            device.log(message=" %s: %s is offlined before online it"
                       % (sub, fru), level="debug")
        else:
            device.log(message="%s: %s is no offlined before online it"
                       % (sub, fru), level="warn")
            return False

    if re.search(r'^(cb|pem|fpc|pcg|scg|sib|spmb|sfm|feb|ccg|fabric.*)$', fru):
        if method == 'power':
            cli_cmd = "test chassis %s slot %s power on" % (fru, slot)
        elif method == 'power_output':
            cli_cmd = "test chassis %s slot %s power-outputs on" % (fru, slot)
        elif method == 'request':
            cli_cmd = "request chassis %s online" % fru
            if re.search(r'^fabric', fru):
                cli_cmd += " slot"
            cli_cmd += " %s" % slot
        else:
            device.log(message=" %s: method should be request"
                               "(default)|power" % sub, level="error")
            return False
        if chassis:
            cli_cmd += " %s" % chassis
        device.cli(command=cli_cmd)
    elif fru == 'pic':
        cli_cmd = "request chassis pic online fpc-slot %s pic-slot %s" % (
            slot[0], slot[1])
        if chassis:
            cli_cmd += " %s" % chassis
        device.cli(command=cli_cmd)
    else:
        device.log(message=" %s: fru(%s) is invalid for offline" % (sub, fru),
                   level="error")
        return False

    if check_count:
        state = r'Online( \- Standby)*|Check|Spare'
        if fru == "sib" and check_spare_sib(device):
            if model == 't320' and slot == 0:
                state = 'Spare'

        if check_fru_state(device, chassis=chassis, fru=fru, slot=slot,
                           state=state, check_count=check_count,
                           check_interval=check_interval):
            device.log(message="%s: %s online passed for slot %s"
                       % (sub, fru, pprint(slot)), level="debug")

            if fru == "feb" and model == "m120":
                i = 0
                for plane in get_fabric_plane(device):
                    if plane['state'] == "ACTIVE":
                        if not plane['links'][str(slot)] == 'ok':
                            device.log(
                                message="%s: link between FEB %s to fabric plane %s is not ok" % (sub, slot, i),
                                level="debug")
                    i += 1
            elif fru == 'fabric plane' and re.search(r'm120', model):
                fb_plane = get_fabric_plane(device, plane=slot)
                if fb_plane['state'] != 'ACTIVE':
                    device.log(message="%s: fabric plane %s should show ACTIVE"
                               % (sub, slot), level="error")
                    return False

        else:
            device.log(message="%s: %s online failed for slot"
                       % (sub, pprint(slot)), level="warn")
            return False

    return True
# end def request_fru_online


def request_fru_reset(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Request Fru Reset  device=${device_object}   chassis='sfc 0'
    ...    fru='fpc'  slot=${2}

    Reset the fru slot to Online using cli command

    :param device:
        **REQUIRED** Device handle
    :param method:
        **OPTIONAL** restart|board-reset (default is restart)
    :param chassis:
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param fru:
        **REQUIRED** fpc|sib|sfm|pcg|scg|cb|pic
    :param slot:
        **REQUIRED** FRU slot number
    :param check_count:
        **OPTIONAL** Check count for FRU online (default is 0 no checking)
    :param check_offline:
        **OPTIONAL** Check if offlined after reset (default is 1)
    :param check_interval:
        **OPTIONAL** Wait time before next retry (default is 10 seconds)
    :param state:
        **OPTIONAL** state of the fru (default- Online,final fru after reset)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['chassis', 'fru', 'slot', 'method', 'check_offline',
                  'check_count', 'check_interval', 'state']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    fru = kwargs.get('fru')
    slot = kwargs.get('slot')
    # state = kwargs.get('state', 'Online')
    method = kwargs.get('method', 'restart')
    check_offline = kwargs.get('check_offline', 1)
    check_count = kwargs.get('check_count', 0)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model().lower()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)),
               level="debug")
    if isinstance(slot, list):
        for slot_value in slot:
            if not request_fru_reset(device,
                                     fru=fru,
                                     chassis=chassis,
                                     slot=slot_value,
                                     method=method,
                                     check_offline=check_offline,
                                     check_count=check_count):
                return False
        device.log(message="%s : %s reset passed for slot %s "
                   % (sub, fru, slot), level="debug")
        return True
    if method == 'restart':
        cli_cmd = "request chassis %s slot %s restart" % (fru, slot)
        if chassis:
            cli_cmd += "%s" % chassis
        # response = device.cli(command=cli_cmd).response()
        device.cli(command=cli_cmd).response()
    elif method == 'board-reset':
        cli_cmd = "test chassis fpc slot %s board-reset trigger" % slot
        if chassis:
            cli_cmd += " %s " % chassis
        # response = device.cli(command=cli_cmd).response()
        device.cli(command=cli_cmd).response()
    else:
        device.log(message=" %s : reset method(%s) is invalid"
                   % (sub, method), level="error")
        return False
    if check_offline:
        if check_fru_state(device,
                           chassis=chassis,
                           fru=fru,
                           state='Offline|Dormant|Present|Starting',
                           slot=slot,
                           check_count=3,
                           check_interval=5):
            device.log(message=" %s : %s slot %s offlined" % (sub, fru, slot),
                       level="debug")
            return True
        else:
            device.log(message=" %s : fru(%s),slot %s not offlined"
                       % (sub, fru, slot), level="error")
            return False
    if check_count:
        if check_fru_state(device,
                           chassis=chassis,
                           fru=fru,
                           state='Online( - Standby)*',
                           slot=slot,
                           check_count=check_count,
                           check_interval=check_interval):
            device.log(message="%s : %s (slot %s)onlined"
                       % (sub, fru, slot), level="debug")
            return True
        else:
            wait_time = check_count * check_interval
            device.log(message=" %s: fru(%s), slot(%s) cannot "
                               "come online after reset after wait "
                               "for at least %s seconds"
                       % (sub, fru, slot, wait_time), level="error")
            return False
    return True
# end def request_fru_reset


def request_fru_switch(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Request Fru Switch  device=${device_object}    chassis='sfc 0'
    ...    fru='sfm'  status='Online'  check_fru=${1}    check_slot=${1}
    ...    check_interface=${1}    check_hardware=${1}    check_craft=${1}
    ...    check_alarm=${1}    check_memory=${1}    check_database=${1}

    Description:
    Request a chassis fru to switchover to backup one
    This function performs the following actions.
        -> Get cli output from request chassis routing-engine master
         method if the fru equal to re
        -> Don't confirm the cli command until defined confirm.
        -> No need of backup RE for method acquire
        -> LCC switchover does not change mastershp of SCC
        -> If no chassis is specified for non TX matrix,
            we also need to switch_re

    :param device:
        **REQUIRED** Device handle
    :params chassis:
       **REQUIRED** scc | lcc 0|1|2|3
    :params method:
        *OPTIONAL*  switch
    :params fru :
        **REQUIRED** re|cfeb|ssb|sfm
    :params status :
        **REQUIRED** chassis status (default get it from get_chas_status)
    :params check_fru :
        **REQUIRED** fru to check (list or string)
    :params check_slot:
        **REQUIRED** fruslot to check
    :params check_if:
        **REQUIRED** 0|1 or a dict from get_chas_if
    :params check_hardware :
        **REQUIRED** 0|1 or a dict from get_chas_hardware
    :params check_craft :
        **REQUIRED** hardware intentory dict from get_chas_hardware
    :params check_alarm :
        **REQUIRED** alarm has to check
    :params check_memory:
        **REQUIRED** memory to check
    :params check_database:
        **REQUIRED** Database to check
    :params check_count:
        **OPTIONAL** Check count for FRU online (default 0 no checking)
    :params check_interval :
        **OPTIONAL** Wait time before next retry (default 10 seconds)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['chassis', 'method', 'fru', 'status', 'check_fru',
                  'check_slot', 'check_interface', 'check_hardware',
                  'check_craft', 'check_alarm', 'check_memory',
                  'check_database', 'check_all', 'check_count',
                  'check_interval', 'confirm', 'reply']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis', '')
    method = kwargs.get('method', 'switch')
    fru = kwargs.get('fru')
    status = kwargs.get('status')
    check_fru = kwargs.get('check_fru')
    check_slot = kwargs.get('check_slot')
    check_interface = kwargs.get('check_interface')
    check_hardware = kwargs.get('check_hardware')
    check_craft = kwargs.get('check_craft')
    check_alarm = kwargs.get('check_alarm')
    check_memory = kwargs.get('check_memory')
    check_database = kwargs.get('check_database')
    check_all = kwargs.get('check_all')
    check_count = kwargs.get('check_count', 0)
    check_interval = kwargs.get('check_interval', 10)
    confirm = kwargs.get('confirm')
    reply = kwargs.get('reply', 'y')
    skip_interface = 'bcm. * | em. * | fxp. * | lo. *'
    model = device.get_model().lower()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)))
    if not status:
        status = get_chassis_status(device, skip_interface=skip_interface)
    fru_ = fru
    if fru == 're':
        fru_ = 'routing-engine'
    cli_cmd = "request chassis %s master %s " % (fru_, method)
    if not confirm:
        cli_cmd += " no-confirm"
    if chassis:
        cli_cmd += " %s" % chassis

    if fru == 're' and method == 'acquire':
        device.switch_re()
    if confirm:
        device.cli(command=cli_cmd, pattern="qr/yes,no/")
        device.cli(command=reply)
    else:
        device.cli(command=cli_cmd)
    match = re.search(r'scc|sfc 0', chassis, re.I)
    match1 = re.search(r'scc|sfc 0', chassis, re.I)
    if fru == 're' and (method != 'acquire' and not chassis) \
            or (method != 'acquire' and match) \
            or (method == 'acquire' and not match1):
        device.switch_re()
    if check_all:
        if check_interface is None:
            check_interface = 1
        if check_hardware is None:
            check_hardware = 1
        if check_craft is None:
            check_craft = 1
        if check_fru is None:
            check_fru = 1
        if fru != 're':
            if check_alarm is None:
                check_alarm = 1
            if check_memory is None:
                check_memory = 1
        if check_database is None:
            check_database = 1
    if check_count > 0:
        if check_chassis_status(device,
                                status=status,
                                skip_interface=skip_interface,
                                check_hardware=check_hardware,
                                check_fru=check_fru,
                                check_slot=check_slot,
                                check_craft=check_craft,
                                check_alarm=check_alarm,
                                check_memory=check_memory,
                                check_database=check_database,
                                check_count=check_count,
                                check_interval=check_interval):
            device.log(message="% s: check passed within retry %s "
                               "times by %s seconds interval "
                       % (sub, check_count, check_interval),
                       level="debug")
        else:
            device.log(message="%s : check failed after retry %s "
                               "times by %s seconds interval"
                       % (sub, check_count, check_interval),
                       level="warn")
            return False
    return True
# end def request_fru_switch


def restart_chassisd(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    &{status_dict} =  Create Dictionary  state=Online
    @{status} =  Create List  &{status_dict}
    ${result} =  Restart Chassisd    device=${device_object}    chassis='sfc 0'
    ...    soft='soft'    status=${status}    check_fru=${1}    check_slot=${1}
    ...    check_interface=${1}    check_hardware=${1}    check_craft=${1}
    ...    check_alarm=${1}    check_memory=${1}    check_database=${1}
    ...    sleep_val=${5}
    Restart chassisd (soft|hard)  usinf cli command "restart chassisid"

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED**  Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param soft    :
        **OPTIONAL**  1|0 chassid soft restart (default is 0,hard restart)
    :param status:
        **REQUIRED**  chassis status
    :param check_fru:
        **REQUIRED**  fru name or list of frus to check
    :param check_slot:
        **REQUIRED**  a fru slot, a list of slots or a dictionary of fru
        slots for check_fru
    :param check_interface:
        **REQUIRED**  0|1 (1 get interfaces from get_chassis_interface
        before restart chassisd)
    :param skip_interface:
        **REQUIRED**  regular expression for interface to skip checking
    :param check_alarm:
        **REQUIRED**  0|1 (1 get interfaces from get_chassis_alarm
        before restart chassisd)
    :param check_craft:
        **REQUIRED**  0|1 (1 get interfaces from get_chassis_craft
        before restart chassisd)
    :param check_hardware :
        **REQUIRED**  0|1 (1 get interfaces from get_chassis_hardware
         before restart chassisd)
    :param check_memory :
        **REQUIRED**  0|1 (1 get interfaces from get_chassis_memory
        before restart chassisd)
    :param check_all:
        **REQUIRED**  0|1 (check all: check_interface,check_hardware,check_fru,
        check_craft)
    :param check_count:
        **OPTIONAL**  Check count for craft display (default 0 no checking)
    :param check_interval:
        **OPTIONAL**  Wait time before next retry (default 10 seconds)
    :param sleep:
        **OPTIONAL**  sleep time in seconds after restarting chassisd,
        default is 10

    :return :
        TRUE if error count is less
        FALSE if error count is high
    """
    valid_keys = ['chassis', 'soft', 'skip_interface', 'status',
                  'check_interface', 'check_fru', 'check_slot',
                  'check_craft', 'check_hardware', 'check_memory',
                  'check_alarm', 'check_datatbase', 'check_all',
                  'sleep_val', 'check_count']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    soft = kwargs.get('soft')
    skip_interface = kwargs.get('skip_interface')
    status = kwargs.get('status')
    check_interface = kwargs.get('check_interface')
    check_fru = kwargs.get('check_fru')
    check_slot = kwargs.get('check_slot')
    check_craft = kwargs.get('check_craft')
    check_hardware = kwargs.get('check_hardware')
    check_memory = kwargs.get('check_memory')
    check_alarm = kwargs.get('check_alarm')
    check_database = kwargs.get('check_database')
    check_all = kwargs.get('check_all')
    sleep_val = kwargs.get('sleep_val')
    if not sleep_val:
        sleep_val = 10
    check_count = kwargs.get('check_count', 0)
    check_interval = kwargs.get('check_interval', 10)

    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)))
    if 'status' in kwargs:
        status = kwargs.get('status')
    else:
        status = get_chassis_status(device, skip_interface=skip_interface)

    cli_cmd = "restart chassisd"
    if chassis:
        chassis = chassis
    else:
        cli_cmd += "%s" % chassis
    if soft:
        soft = soft
    else:
        cli_cmd += " soft"
    device.cli(command=cli_cmd)
    if check_count > 0 and not soft:
        sleep(sleep_val)
    if check_all:
        check_fru = check_interface = check_hardware = check_craft\
            = check_memory = check_alarm = 1
    if check_chassis_status(device,
                            status=status,
                            skip_interface=skip_interface,
                            check_interface=check_interface,
                            check_hardware=check_hardware,
                            check_fru=check_fru,
                            check_memory=check_memory,
                            check_alarm=check_alarm,
                            check_database=check_database,
                            check_slot=check_slot,
                            check_craft=check_craft,
                            check_count=check_count,
                            check_interval=check_interval):
        device.log(message="%s: check passed within retry %s "
                           "times by %s seconds interval"
                   % (sub, check_count, check_interval),
                   level="debug")
    else:
        device.log(message="%s: check failed after retry %s times by %s "
                           "seconds interval"
                   % (sub, check_count, check_interval), level="warn")
        return False
    return True
# end def restart_chassisd


def set_chassis_control(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =    Set Chassis Control    device=${device_object}
    ...    enable=${1}    commit=${1}

    Enables/disables/failover the chassis-control using the cli
    command "set system processess chassis-control"

    :param device:
        **REQUIRED** Device handle
    :param enable:
        **REQUIRED** Option to enable the chassis-control process
    :param disable:
        **REQUIRED** Option to disable the process
    :param failover:
        **REQUIRED** Option to set the process failover
    :param commit:
        **REQUIRED** Commit the process configurations

    :return :
        TRUE if no error while configuring
        FALSE if error occurs

    """
    valid_keys = ['failover', 'disable', 'enable', 'commit']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    disable = kwargs.get('disable')
    enable = kwargs.get('enable')
    failover = kwargs.get('failover')
    commit = kwargs.get('commit')
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s ..." % (sub, str(kwargs)))
    cfg_cmd = "set system processes chassis-control"
    if enable:
        device.config(command_list=["%s enable" % cfg_cmd])
    if disable:
        device.config(command_list=["%s disable" % cfg_cmd])
    if failover:
        device.config(command_list=["%s failover" % cfg_cmd])
    if commit:
        device.config(command_list=["commit"]).response()
    return True
# end def set_chassis_control


def set_chassis_graceful(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Set Chassis Graceful  device=${device_object}

    Enables or Disables Graceful Routing Engine switchover(GRES)
    using the cli command "set chassis redundancy graceful switchover"
    and "set chassis redundancy graceful switchover enable"

    :param device:
        **REQUIRED** Device handle
    :param commit:
        **OPTIONAL** 1|0 commit after set (default is 0)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['commit']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)), level="debug")
    if re.search(r'^9.0', device.get_version()):
        device.config(
            command_list=["set chassis redundancy graceful-switchover"])
    else:
        device.config(
            command_list=["set chassis redundancy graceful-switchover enable"])
    if kwargs.get('commit'):
        device.commit().response()
    return True
# end def set_chassis_graceful


def check_chassis_craft(device, **kwargs):
    """
    Robot Usage Example :
     ${device_object} =  Get Handle  resource=r1
     &{craft_dict} =    Evaluate  ({'alarm': {'major': 0, 'minor': 0,
     ...    'red': 0, 'yellow': 0},'display': [], 'fpc': {}, 're': {'ok': 1}})
     &{status_dict} =    Evaluate  ({'fru': 1,
    ...    'alarm': {'major': '1', 'minor': '1'},
    ...    'skip_interface': 'pimd', 'chassis': ''})
    @{host}   =  Create List  sun
    ${result}  =  Check Chassis Craft   device=${device_object}
    ...    chassis='sfc 0'  craft=${craft_dict}  status=${status_dict}
    ...    host=${host}  check_count=${5}

    Test if chassis craft display is consistant with current
    chassis status by doing the following
       - Check the hostname in FPM Dispaly
       - Check alarms in FPM Display
       - Check RE LEDs in FPM Display
       - Check LEDs FPC/SIB/PEM
       - Check LEDs for CB/PCG/SCG

    :param device:
        **REQUIRED** Device handle
    :params chassis  :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :params craft :
        **REQUIRED** dictionary for craft display
        (return from get_chassis_craft)
    :params status :
        **REQUIRED** dictionary for chassis status
        (return from get_chassis_status)
    :params host:
        **REQUIRED** list of hosts
    :params check_count :
        **OPTIONAL** Check count for FRU online (default 0 no checking)
    :params check_interval :
        **OPTIONAL** Wait time before next retry (default 10 seconds)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['craft', 'status', 'chassis', 'check_count',
                  'check_interval', 'host', 'check_craft']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis')
    status = kwargs.get('status')
    craft = kwargs.get('craft')
    check_craft = kwargs.get('check_craft', True)
    host = kwargs.get('host')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s function%s..." % (sub, str(kwargs)))
    hostname_ok = False
    alarm_ok = False
    re_ok = False
    sfm_ok = False
    pass_check = False
    if not check_craft:
        device.log(message="%s() return TRUE since CHK_CRAFT is off",
                   level="debug")
        return True
    if chassis:
        host = get_chassis_hostname(device, chassis=chassis)
        device.log(message="%s: host(%s), chassis(%s)" % (sub, host, chassis),
                   level="debug")
    # For fpc|sib|pem
    fru1_ok = {}
    # For cb|scg|pcg
    fru2_ok = {}

    get_chas_craft = False
    if not craft:
        get_chas_craft = True

    for i in range(0, check_count):
        check_ok = True
        check_info = "count(%s), interval(%s)" % (check_count, check_interval)
        if i > 0:
            device.log(message="%s:wait %s seconds before next retry, %s"
                       % (sub, check_interval, check_info), level="debug")
            sleep(check_interval)
        if not status:
            status = get_chassis_status(device,
                                        chassis=chassis,
                                        skip_interface='pimd',
                                        fru=1,
                                        alarm=1)
        if get_chas_craft:
            craft = get_chassis_craft(device, chassis=chassis, display=host)
        show_data(device, craft, "%s: current chassis craft display:")
        show_data(device, status, "%s: current chassis status:")

        # Check hostname in FPM Display
        if not hostname_ok:
            device.log(message="%s:Testing hostname FPM display..." % sub,
                       level="debug")
            test_info = "%s: Check craft display for hostname(%s), %s" % (
                sub, host, check_info)
        if not host:
            host = 'noname'
        craft_display = check_craft_display(device, craft=craft, display=host)
        if craft_display:
            device.log(message="%s passed" % test_info, level="debug")
            hostname_ok = True
        else:
            device.log(message="%s failed" % test_info, level="warn")
            check_ok = False
            continue

        # Check alarms in FPM Display
        if not alarm_ok:
            test_info = "%s: Check craft display for alarm, %s" % (
                sub, check_info)
            craft_alarm = check_craft_alarm(device, chassis=chassis,
                                            craft=craft, alarm=status["alarm"])
            if craft_alarm:
                device.log(message="%s passed" % test_info, level="debug")
                alarm_ok = True
            else:
                device.log(message="%s failed" % test_info, level="warn")
                check_ok = False
                continue

        # Check RE LEDs in FPM Display
        if not re_ok:
            re_led = __check_re_led(device, craft, status)
            if re_led:
                re_ok = True
            else:
                check_ok = False
                continue

        # Check LEDs FPC/SIB/PEM
        for fru in ['fpc', 'sib', 'pem']:
            match = re.search(r'^TX Matrix|TXP|ptx5000$', model, re.I)
            if fru == 'pem' and model != 'm320' \
                    or (fru == 'fpc' and match):
                continue
            if not check_fru_valid(device, fru):
                continue
            fru1_led = __check_fru1_led(device, fru, craft, status, chassis)
            if fru1_led:
                fru1_ok[fru] = True
            else:
                check_ok = False
                break

        # Check LEDs for CB/PCG/SCG
        for fru in ['cb', 'scg', 'pcg', 'mcs']:
            match1 = re.search(r'^TX Matrix|TXP|ptx5000$', model, re.I)
            match2 = re.search(r'^(scg|pcg|mcs)$', model)
            fru_valid = check_fru_valid(device, fru=fru)
            if match1 and match2 or not fru_valid:
                continue
            fru2_led = __check_fru2_led(device, fru, craft, status)
            if fru2_led:
                fru2_ok[fru] = True
            else:
                check_ok = False
                break
        match3 = re.search(r'^(m160|m40e)$', model)
        if not sfm_ok and match3:
            sfm_led = __check_sfm_led(device, craft, status)
            if sfm_led:
                sfm_ok = True
            else:
                check_ok = False
                continue
        if check_ok:
            device.log(
                message="%s: craft-interface check OK when retry %s times"
                % (sub, i), level="debug")
            pass_check = True
            break

    if not pass_check:
        device.log(message="%s: craft display check failed" % sub,
                   level="warn")
        return False
    return True
# end def check_chassis_craft


def clear_craft_display(device, **kwargs):
    """
    Robot Usage Example :
     ${device_object} =  Get Handle  resource=r1
     &{kwargs} =  Create Dictionary   check_count=${1}  check_interval=${10}
     ${result} =  Clear Craft Display   device=${device_object}  &{kwargs}

    Clear display message in craft-interface display

    :param device:
        **REQUIRED** Device handle
    :param check_count :
       **OPTIONAL** Check count for craft display (default 0 no checking)
    :param check_interval:
       **OPTIONAL** Wait time before next retry (default 2  seconds)

    :return:
       TRUE if the process has no error
       FALSE if the process has error
    """
    valid_keys = ['check_count', 'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 2)
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)))
    # cli_cmd = "set chassis display message \"\""
    # response = device.cli(command=cli_cmd).response()
    host = get_chassis_hostname(device)
    # count = 0
    result = True
    while check_count:
        check_info = "count(%s), interval(%s)" % (check_count, check_interval)
        sleep(check_interval)
        craft = get_chassis_craft(device)
        display = craft['display'][1]
        match = re.search(r'\|%s\s+\|' % host, display, re.M)
        if not match:
            result = False
            break
        check_count -= 1
    if result:
        device.log(message="%s: no hostname (%s) in display (%s), %s "
                   % (sub, host, display, check_info), level="warn")
    return result
# end def clear_craft_display


def set_chassis_manufacturing_diagnostic_mode(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Set Chassis Manufacturing Diagnostic Mode
    ...    device=${device_object}

    Set chassis manufacturing-diagnostic-mode using cli command
    "set chassis manufacturing-diagnostic-mode"

    :param device:
        **REQUIRED** Device handle
    :param commit :
        **OPTIONAL** 1|0 commit after set (default is 0)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['commit']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)))
    cmd = ["set chassis manufacturing-diagnostic-mode"]
    device.config(command_list=cmd)
    if kwargs.get('commit'):
        device.commit().response()
    return True
# end def set_chassis_manufacturing_diagnostic_mode


def set_craft_display(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Set craft display  device=${device_object}
    ...    display='craft display message'

    Send display message to craft-interface using the cli command
    "set chassis display message <message>"

    :param device:
        **REQUIRED** Device handle
    :param display:
        **REQUIRED** a string message to display on craft-
                     interface
    :param check_count:
        **OPTIONAL** Check count for craft display (default 0 no
                     checking)
    :param check_interval:
        **OPTIONAL** Wait time before next retry (default 2 seconds)

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    valid_keys = ['display', 'check_count', 'check_interval']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    display = kwargs.get('display')
    check_count = kwargs.get('check_count')
    check_interval = kwargs.get('check_interval')
    device.log(message="Inside %s %s..." % (sub, str(kwargs)), level="debug")
    cli_cmd = "set chassis display message %s" % display
    device.cli(command=cli_cmd).response()
    if check_count > 0:
        if not check_craft_display(device, display=display,
                                   check_count=check_count,
                                   check_interval=check_interval):
            return False
    return True
# end def set_craft_display


def set_temperature_threshold(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Set Temperature Threshold  device=${device_object}
    ...    yellow_alarm='22'  red_alarm='11'

    Sets the chassis temperature threshold using the cli command
    "set chassis temperature-threshold"

    :param device:
        **REQUIRED** Device handle
    :params yellow_alarm :
        **REQUIRED** Threshold at which yellow alarm is set (centigrade)
    :params red_alarm :
        **REQUIRED** Threshold at which red alarm is set (centigrade)
    :params normal_speed :
        **REQUIRED** Threshold at which fans return to normal speed
    :params full_speed :
        **REQUIRED** Threshold at which fans run full speed (centigrade)
    :params commit :
        *OPTIONAL* To commit the chassis temperature threshold

    :return:
        TRUE if the process has no error
        FALSE if the process has error
    """
    model = device.get_model()
    sub = function_name(device) + "(%s)" % model
    valid_keys = ['yellow_alarm', 'red_alarm', 'normal_speed', 'full_speed',
                  'commit']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    yellow_alarm = kwargs.get('yellow_alarm')
    red_alarm = kwargs.get('red_alarm')
    normal_speed = kwargs.get('normal_speed')
    full_speed = kwargs.get('full_speed')
    commit = kwargs.get('commit')
    cfg_cmd = []
    device.log(message="Inside %s %s ..." % (sub, str(kwargs)), level="debug")
    cmd = "set chassis temperature-threshold"
    if yellow_alarm:
        cfg_cmd.append("%s yellow-alarm %s" % (cmd, yellow_alarm))
    if red_alarm:
        cfg_cmd.append("%s red-alarm %s" % (cmd, red_alarm))
    if normal_speed:
        cfg_cmd.append("%s fans-to-normal-speed %s" % (cmd, normal_speed))
    if full_speed:
        cfg_cmd.append("%s fans-on-full-speed %s" % (cmd, full_speed))

    if cfg_cmd:
        device.config(command_list=cfg_cmd)
        if commit:
            device.commit().response()
    else:
        device.log(message="%s: missing threshold setting argument(s)" % sub,
                   level="error")
        return False
    return True
# end def set_temperature_threshold


def test_chassis_fan(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Test Chassis Fan  device=${device_object}  speed='full'
    ...    count=${1}

    Test chassis fan speed using the cli command
    "test chassis fan speed" and checks whethere
    speed is high,normal or unknown speed

    :param device:
        **REQUIRED** Device handle
    :param speed:
        **REQUIRED** full(or full-speed,high) | normal
    :param check_count:
        **OPTIONAL** Check count for FRU online (default 0 no checking)
    :param check_interval :
        **OPTIONAL** Wait time before next retry (default 10 seconds)
    :param count :
        **REQUIRED** Check count

    :return: Dictionary of speed, count, check count, check interval
    """
    valid_key = ['speed', 'check_count', 'check_interval', 'count']
    required_key = []
    kwargs = check_args(device, valid_key, required_key, kwargs)
    speed = kwargs.get('speed')
    count = kwargs.get('count')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s %s..." % (sub, str(kwargs)))
    cli_cmd = "test chassis fan speed"
    if not speed:
        # return False
        if not test_chassis_fan(device, speed="high",
                                check_count=check_count,
                                check_interval=check_interval):
            return False
        if not test_chassis_fan(device, speed="normal",
                                check_count=check_count,
                                check_interval=check_interval):
            return False
        device.log(message="%s: test chassis fan speed passed" % sub,
                   level="debug")
        return True
    if re.search('(full|high)', speed, re.I):
        cli_cmd += " full-speed"
    elif re.search(r'^normal$', speed, re.I):
        cli_cmd += " normal"
    else:
        device.log(message="%s: unknown fan speed (%s)"
                   % (sub, speed), level="error")
        return False
    if re.search(r'^TX Matrix$', model, re.I):
        cli_cmd += 'scc'
    elif re.search(r'^TXP$', model, re.I):
        cli_cmd += ' sfc 0 tray 6'
    # response = device.cli(command=cli_cmd).response()
    device.cli(command=cli_cmd).response()
    if check_enhance_fantray(device):
        count = 24
        check_fan = check_chassis_fan(device, speed=speed,
                                      count=count,
                                      check_count=check_count,
                                      check_interval=check_interval)
        return check_fan
# end def test_chassis_fan


def __cli_get_hardware(device, **kwargs):
    """
    Gets hardware details of chassis using "show chassis hardware" cli command
       -> Greps the psd or rsd and re from the response.
       -> Gets the hardware information like Item,Version,Part number,
       Serial number,Description

    :param device:
        **REQUIRED** Device handle
    :param chassis:
        **REQUIRED** Type of Chassis (scc | lcc 0|1|2|3)

    :return : Dictionary of hardware details
    """
    valid_keys = ['chassis']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    chassis = kwargs.get('chassis', '')
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    hardware = {}
    device.log(message="Inside %s ......" % sub)
    cli_cmd = "show chassis hardware "
    if chassis:
        cli_cmd += " %s" % chassis
    response = device.cli(command=cli_cmd).response()
    result = response.split('\n')
    psd = None
    for line in result:
        search = re.search(r'^(psd\d*|rsd\d*)-re\d+', line, re.I)
        search1 = re.search(r'^(Hardware|---------|\S+-re\d+:)', line)
        match1 = re.search(r'^(Item\s+)(Version\s+)(Part number\s+)'
                           r'(Serial number\s+)(Description.*)', line)
        if search:
            psd = search.group(1)
            continue
        if search1:
            continue
        if re.search(r'^\s*$', line):
            continue
        device.log(message="%s: line = %s\n" % (sub, line))
        if match1:
            item_chars = len(match1.group(1))
            version_pos = item_chars
            version_chars = len(match1.group(2))
            part_number_pos = version_pos + version_chars
            part_number_chars = len(match1.group(3))
            serial_number_pos = part_number_pos + part_number_chars
            serial_number_chars = len(match1.group(4))
            description_pos = serial_number_pos + serial_number_chars
            device.log(
                message="%s: pos(pos),version(%s), part_number(%s), serial_number(%s), description(%s)"
                % (sub, version_pos, part_number_pos, serial_number_pos,
                   description_pos),
                level="debug")
            device.log(
                message="%s(chars): item(%s),  version(%s), part_number(%s),serial_number(%s)"
                % (sub, item_chars, version_chars, part_number_chars,
                   serial_number_chars),
                level="debug")
            continue
        item = line[:item_chars]
        name = item
        name = __chop(device, name)
        if re.search(r"^\S+", item):
            sub_module = None
            sub_sub_module = None
            module = __convert_name(device, __chop(device, item))
        elif re.search(r"^  \S+", item):
            sub_sub_module = None
            sub_module = __convert_name(device, __chop(device, item))
        else:
            sub_sub_module = __convert_name(device, __chop(device, item))

        version = __chop(device, line[item_chars:part_number_pos])
        part_number = __chop(device, line[part_number_pos:serial_number_pos])
        serial_number = __chop(device, line[serial_number_pos:description_pos])
        description = __chop(device, line[description_pos:])

        if sub_sub_module:
            if psd:
                hardware.setdefault(psd, {})
                hardware[psd].setdefault(module, {})
                hardware[psd][module].setdefault(sub_module, {})
                hardware[psd][module][sub_module].setdefault(
                    sub_sub_module, {})
                __get_hardware(
                    device, hardware[psd][module][sub_module][sub_sub_module],
                    name, version, part_number, serial_number, description)
            else:
                hardware.setdefault(module, {})
                hardware[module].setdefault(sub_module, {})
                hardware[module][sub_module].setdefault(sub_sub_module, {})
                __get_hardware(
                    device, hardware[module][sub_module][sub_sub_module],
                    name, version, part_number, serial_number, description)

        elif sub_module:
            if psd:
                hardware.setdefault(psd, {})
                hardware[psd].setdefault(module, {})
                hardware[psd][module].setdefault(sub_module, {})
                __get_hardware(
                    device, hardware[psd][module][sub_module], name,
                    version, part_number, serial_number, description)
            else:
                hardware.setdefault(module, {})
                hardware[module].setdefault(sub_module, {})
                __get_hardware(
                    device, hardware[module][sub_module], name,
                    version, part_number, serial_number, description)
        else:
            if psd:
                hardware.setdefault(psd, {})
                hardware[psd].setdefault(module, {})
                __get_hardware(device, hardware[psd][module], name, version,
                               part_number, serial_number, description)
            else:
                hardware.setdefault(module, {})
                __get_hardware(device, hardware[module], name, version,
                               part_number, serial_number, description)

    show_data(device, hardware, sub)
    return hardware
# end def __cli_get_hardware


def __cli_get_environment(device, **kwargs):
    """
    Description:
        Gets environment details (power, temperature, state) of chassis,
        specific FRUs and slots.

    :param device:
        **REQUIRED** Device handle
    : param chas :
        **REQUIRED** Type of Chassis (scc | lcc 0|1|2|3)
    : param fru :
        **REQUIRED** fru name or list of frus to check
    : param slot :
        **REQUIRED** FRU slot number or list of slots

    :return :Dictionary of lists with chassis environment details

    """
    valid_keys = ['chassis', 'fru', 'slot']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    chassis = kwargs.get('chassis')
    fru = kwargs.get('fru')
    slot = kwargs.get('slot')
    model = device.get_model().lower()
    sub = function_name(device) + "(%s)" % model
    device.log("Inside %s %s ..." % (sub, str(kwargs)))
    env = {}

    if not fru:
        # Get cli output from show chassis environment
        cli_cmd = "show chassis environment"
        if chassis:
            cli_cmd += " %s" % chassis
        response = device.cli(command=cli_cmd, format='text').response()
        for line in response.split('\n'):
            device.log("%s: line(%s)" % (sub, line))
            matched = re.search(
                r'^(Class\s+)(Item\s+)(Status\s+)Measurement.*',
                line)
            if matched:
                class_len = len(matched.group(1))
                item_len = len(matched.group(2))
                status_len = len(matched.group(3))
                device.log(
                    message="class_len(%s), item_len(%s), status_len(%s)" %
                    (class_len, item_len, status_len), level="debug")
            if not line or 'class_len' not in locals() or \
                    re.search(r'^psd|^rsd|^--', line, re.I):
                continue
            class_tmp = __chop(device, line[0:class_len])
            if class_tmp:
                if class_tmp == 'Class':
                    continue
                class_ = class_tmp
            status_pos = class_len + item_len
            item = __chop(device, line[class_len:status_pos])
            name = item
            if not name:
                continue
            item = __convert_name(device, item)
            if item not in env.keys():
                env[item] = {}
            env[item]['name'] = name
            if 'class_' in locals():
                env[item]['class'] = class_
            measurement_pos = class_len + item_len + status_len
            status = line[class_len + item_len:measurement_pos]
            env[item]['status'] = __chop(device, status)
            if len(line) >= measurement_pos+1:
                measurement = __chop(device, line[measurement_pos:])
                if measurement and re.search(r"\d+ degrees", measurement):
                    env[item]['temperature'] = measurement
                elif measurement:
                    env[item]['comment'] = measurement
        show_data(device, env, "%s : return" % sub)
        return env
    # Get output for a specific FRU
    cli_cmd = "show chassis environment %s" % fru
    if chassis:
        cli_cmd += " %s" % chassis
    response1 = device.cli(command=cli_cmd, format='text').response()
    if fru == 'routing-engine':
        fru = "routing engine"
    slot_ = 0
    for line in response1.splitlines():
        device.log(message="%s: line=%s" % (sub, line), level="debug")
        matched2 = re.search(r'^(.*) (\d+) status:', line)
        matched2_1 = re.search(r'PDU(\s+\d+\s)PSM(\s\d+\s)status:', line)
        matched2_2 = re.search(r'PDU(\s+\d+\s)', line)
        matched3 = re.search(r'^(.*) status:', line)
        matched4 = re.search(
            r'^\s+State\s+(Online|Offline).*(Master|Standby)', line)
        matched5 = re.search(r'^\s+State\s+(\S+)', line)
        matched6 = re.search(
            r"^\s+Temperature\s+(\d+ degrees C / \d+ degrees F)", line)
        matched7 = re.search(r'^\s+Temperature\s+(\S+)\s+$', line)
        matched8 = re.search(
            r"^\s+(\S+) temperature\s+(\d+ degrees C / \d+ degrees F)",
            line)
        pattern = r'^\s+(\S+ \S+) ' +\
            r'temperature\s+(\d+ degrees C \/ \d+ degrees F)'
        matched9 = re.search(pattern, line)
        matched10 = re.search(
            r"^\s+Temperature\s+(\S+)\s+(\d+ degrees C / \d+ degrees F)",
            line)
        matched12 = re.search(r'^\s+(.*):', line)
        matched13 = re.search(r"^\s+(\d+\.\d+.*)\s+(\d+) mV", line)
        matched14 = re.search(r"^\s+(\S+)\s+(\d+) MHz", line)
        matched15 = re.search(r"^\s+CMB Revision\s+(\d+)", line)
        if matched2:
            slot_ = matched2.group(2)
            env.setdefault(slot_, {})
            device.log(message="%s: fru(%s), name(%s),slot(%s)" % (
                sub, fru, matched2.group(1), matched2.group(2)))
            if model == 'ptx5000':
                tmp = re.search(r'%s' % fru, matched2.group(1), re.I)
            else:
                tmp = re.search(r'^%s$' % fru, matched2.group(1), re.I)
            if not tmp:
                device.log(message="%s: model = %s, fru=%s 1=%s" % (
                    sub, model, fru, matched2.group(1)), level="debug")
                device.log(message="%s: %s shows incorrect name (%s)" % (
                    sub, fru, matched2.group(1)), level="error")
                return None
            if matched2_1:
                st = "PDU" + ' ' + matched2_1.group(1) + ' ' + "PSM" + \
                    ' ' + matched2_1.group(2) + ' ' + "status:"
                device.log(message="%s: %s" % (sub, st), level="debug")
            elif matched2_2:
                st = "PDU" + ' ' + matched2_2.group(1) + ' ' + "status:"
                device.log(message="%s: %s" % (sub, st), level="debug")
        elif matched3:
            tmp = re.search(r'^%s$' % fru, matched3.group(1), re.I)
            if not tmp:
                device.log(message="%s: %s shows incorrect name(%s)" % (
                    sub, fru, matched3.group(1)), level="error")
                return None
        elif matched4:
            env.setdefault(slot_, {})
            env[slot_]['state'] = matched4.group(1)
            env[slot_]['status'] = matched4.group(2)
            device.log("%s: fru(%s), state(%s),status(%s)" % (
                sub, fru, matched4.group(1), matched4.group(2)))
        elif matched5:
            state = matched5.group(1)
            env.setdefault(slot_, {})
            env[slot_]['state'] = state
            device.log(message="%s: state(%s)" % (sub, state), level="debug")
            device.log(message="%s: state(%s)" % (sub, state), level="debug")
        elif matched6:
            env.setdefault(slot_, {})
            env[slot_]['temperature'] = matched6.group(1)
        elif matched7:
            env.setdefault(slot_, {})
            env[slot_]['temperature'] = matched7.group(1)
            device.log(message="sub(slot=%s): Temperature line=>%s<" % (slot_,
                                                                        line),
                       level="debug")
        elif matched8:
            env.setdefault(slot_, {})
            env[slot_].setdefault(matched8.group(1), {})
            env[slot_][matched8.group(1)]['temperature'] = \
                matched8.group(2)
        elif matched9:
            env.setdefault(slot_, {})
            env[slot_].setdefault(matched9.group(1), {})
            env[slot_][matched9.group(1)]['temperature'] = \
                matched9.group(2)
        elif matched10:
            env.setdefault(slot_, {})
            env[slot_]['temperature'] = \
                matched10.group(2)
        elif matched12:
            # field_ name such as POWER, FRQENCY etc.
            field_ = matched12.group(1)
            field = field_.lower()
            env.setdefault(slot_, {})
            env[slot_].update({field: {}})
            env[slot_][field].update({'name': {}})
            env[slot_][field]['name'] = field_
            device.log(message="%s: %s field(%s)" % (sub, field, field_),
                       level="debug")
        elif matched13 or matched14:
            name_ = __chop(device, matched13.group(1))
            value = matched13.group(2)
            name = name_.lower()
            env.setdefault(slot_, {})
            if 'field' in locals():
                env[slot_].update({field: {}})
                env[slot_][field].update({name: {}})
                env[slot_][field][name] = value
            else:
                env[slot_].update({'name': {}, 'value': {}})
                env[slot_]['name'] = name_
                env[slot_]['value'] = value
            device.log(message="%s: $name name(%s)" % (sub, name_),
                       level="debug")
            device.log(message="%s: $name value(%s)" % (sub, value),
                       level="debug")
            device.log(message="%s: $name name(%s)" % (sub, name_),
                       level="debug")
            device.log(message="%s: $name value(%s)" % (sub, value),
                       level="debug")
        elif matched15:
            env.setdefault(slot_, {})
            env[slot_]['cmb'] = matched15.group(1)
    fru_info = "%s: fru(%s)," % (sub, fru)
    if slot:
        env = env[slot]
        fru_info += "slot(%s)" % slot
    show_data(device, env, "%s: return" % sub)
    return env
# end def __cli_get_environment


def __cli_get_firmware(device):
    """
    Displays the version levels of the firmware running
        - Gets the cli response from "show chassis firmware"
        - Greps the Juniper ROM monitor version and OS

    :param device:
        **REQUIRED** Device handle
    :param :None

    :return:
        Dictionary with firmware version details
    """
    # model = device.get_model()
    sub = function_name(device)
    firmware = {}
    device.log(message="Inside %s" % sub, level="debug")
    response = device.cli(command='show chassis firmware').response()
    lines = response.split('\n')
    for line in lines:
        line = re.sub('\n', ' ', line)
        match = re.search(r'^(\S+|\S+\s+\d+)\s+(ROM|O/S)\s+(.*)', line)
        match1 = re.search(r'^\s+(O/S)\s+(.*)', line)
        if match:
            name = match.group(1)
            firmware[name] = {}
            device.log(message="%s: %s (%s)" % (name, match.group(1),
                                                match.group(2)),
                       level="debug")
            firmware[name][match.group(2)] = match.group(3)
        elif match1:
            device.log(message="%s : %s (%s)" % (name, match1.group(1),
                                                 match1.group(2)),
                       level="debug")
            firmware[name][match1.group(1)] = match1.group(2)
    return firmware
# end def __cli_get_firmware


def __cli_get_fru(device, fru):
    """
    Gets FRU information by using cli command "show chassis fru"
        - Grep the state(Online/offline),slot(0/1/2/..)  and uptime from
          the response

    :param device:
        **REQUIRED** Device handle
    :param fru:
        **REQUIRED** fpc|sib|sfm|pcg|scg|cb|pic

    :returns:
        Dictionary of FRU details
    """
    hash_val = {}
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s  ..." % sub, level="debug")
    # Count number of online/active FRUs
    online_count = 0
    if fru == 'sib' and re.search(r'^t\d+$', model):
        fru = 'spmb ' + fru
    sleep(1)
    response = device.cli(command='show chassis ' + fru).response()
    for line in response.split('\n'):
        match = re.search(r'^\s*(\d+)\s+(\S+)\s+(\d.*)', line)
        match2 = re.search(r'\s+(\d+)\s+(\S+)', line)
        if match:
            value = match.group(1)
            hash_val[value] = {}
            hash_val[value]['state'] = match.group(2)
            device.log(message="show chassis %s: Slot=>%s <,State=> %s <"
                       % (fru, match.group(1), match.group(2)),
                       level="debug")
            if match.group(2) == 'Online' or match.group(2) == 'Active':
                online_count += 1
            list_val = list(filter(None, match.group(3).split(' ')))
            hash_val[value]['description'] = list_val[0]
            if len(list_val)-1 == 5:
                hash_val[value]['temperature'] = list_val[0]
                hash_val[value]['cpu_total'] = list_val[1]
                hash_val[value]['cpu_interrupt'] = list_val[2]
                hash_val[value]['memory-dram-size'] = list_val[3]
                hash_val[value]['memory-heap-utilization'] = list_val[4]
                hash_val[value]['memory-buffer-utilization'] = list_val[5]
        elif match2:
            value1 = match2.group(1)
            if value1 not in hash_val.keys():
                hash_val[value1] = {}
            hash_val[value1]['state'] = match2.group(2)
            device.log(
                message="show chassis % s: Slot = > % s <, State = > % s < "
                % (fru, match2.group(1), match2.group(2)), level="debug")
            device.log(message="%s : # of online %s = %s ." % (sub, fru,
                                                               online_count),
                       level="debug")
            show_data(device, hash_val, "%s :hash value" % (sub))
    return hash_val
# end def __cli_get_fru


def get_chassis_routing_engine(device):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Chassis Routing Engine  device=${device_object}

    Gets routing engine details using "show chassis routing-engine"
    cli command and the response ( fru slot,state,Election priority,
    CPU Utilization,Temperature,uptime,Load averages)
    is stored in dictionary

    :param device:
        **REQUIRED** Device handle

    :return:
        Dictionary consisting chassis routing engine parameter
    """
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s  ..." % sub, level="debug")
    cli_command = 'show chassis routing-engine'
    response = device.cli(command=cli_command).response()
    lines = response.split('\n')
    frus = {}
    for line in lines:
        match = re.search(r'.*Slot (\d+)', line)
        match1 = re.search(r'\s+Current state\s+(\S+)', line)
        match2 = re.search(r'\s+Election priority\s+(\S+)\s+\(default\)', line)
        match3 = re.search(r'\s*(\d+\s+\w+)\s+\CPU utilization:', line)
        user = re.search(r'User\s+(\d+)\s+percent', line)
        kernal = re.search(r'Kernel\s+(\d+)\s+percent', line)
        bg = re.search(r'Background\s+(\d+)\s+percent', line)
        interrupt = re.search(r'Interrupt\s+(\d+)\s+percent', line)
        idle = re.search(r'Idle\s+(\d+)\s+percent', line)
        match4 = re.search(r'\s+(.*)\s+(\d+) percent', line)
        match5 = re.search(
            r'\s+Temperature\s+(\d+) degrees C / (\d+) degrees F', line)
        cpu_temp = re.search(
            r'\s+CPU temperature\s+(\d+) degrees C / (\d+) degrees F', line)
        match6 = re.search(
            r'\s+Uptime\s+(\d+) day, (\d+) hours, (\d+) minutes', line)
        match7 = re.search(
            r'\s+Uptime.*\s+(\d+) hours, (\d+) minutes, (\d+) seconds', line)
        match8 = re.search(
            r'\s+Start.*\s+(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)\s+(.*)', line)
        match9 = re.search(r'\s+Serial ID\s+(.*)', line)
        match10 = re.search(r'\s+DRAM\s+(\d+) MB', line)
        match11 = re.search(
            r'\s+Load averages:\s+(\d+) minute\s+(\d+) minute\s+(\d+) minute',
            line)
        if match:
            slot = match.group(1)
            frus[slot] = {}
        elif match1:
            frus[slot]['state'] = match1.group(1)
        elif match2:
            frus[slot]['election_priority'] = match2.group(1)
        elif match3:
            util = match3.group(1)
            frus[slot][util+' cpu_utilization'] = {}
        elif user:
            frus[slot][util+' cpu_utilization']['user'] = user.group(1)
        elif kernal:
            frus[slot][util+' cpu_utilization']['kernal'] = kernal.group(1)
        elif bg:
            frus[slot][util+' cpu_utilization']['backgound'] = bg.group(1)
        elif interrupt:
            frus[slot][util+' cpu_utilization']['interrupt'] =\
                interrupt.group(1)
        elif idle:
            frus[slot][util+' cpu_utilization']['idle'] = idle.group(1)
        elif match4:
            name = match4.group(1)
            frus[slot][name] = match4.group(2)
        elif match5:
            frus[slot]['temperature'] = match5.group(2)+" F"
        elif cpu_temp:
            frus[slot]['cpu_temperature'] = cpu_temp.group(2)+" F"
        elif match6:
            frus[slot]['uptime'] = match6.group(2)
        elif match7:
            frus[slot]['uptime'] = match7.group(2)
        elif match8:
            year = int(match8.group(1))
            month = int(match8.group(2))
            day = int(match8.group(3))
            hr = int(match8.group(4))
            mins = int(match8.group(5))
            sec = int(match8.group(6))
            dow = datetime.date(year, month, day).weekday()
            frus[slot]['start_time'] = time.asctime(
                (year, month, day, hr, mins, sec, dow, 0, 0))
        elif match9:
            frus[slot]['serial_id'] = match9.group(1)
        elif match10:
            frus[slot]['dram'] = match10.group(1)
        elif match11:
            frus[slot]['load_averges'] = [match11.group(1),
                                          match11.group(2), match11.group(3)]
    show_data(device, frus, sub + 'return:')
    return frus
# end def get_chassis_routing_engine


def __cli_get_alarm(device, **kwargs):
    """
    Gets alarm details time,class,description,short-description,
    type by "show chassis alarm" cli command which contains
     the list of alarms currently active, incorrect alarm
     and inactive alarm.

    :param device:
        **REQUIRED** Device handle
    :param chassis:
       **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)

    :returns:
        list of dictionaries with alaram details if alarm count > 0

    """
    chassis = kwargs.get('chassis', '')
    alarm_count = 0
    alarms = []
    alarm = {}
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s" % sub, level="debug")

    if device.is_evo():
        cli_cmd = "show system alarms"
    else:
        cli_cmd = "show chassis alarms"

    if chassis:
        cli_cmd += " %s" % chassis
    else:
        cli_cmd = cli_cmd

    response = device.cli(command=cli_cmd).response()
    lines = response.split('\n')
    for line in lines:
        device.log(message="%s: line > %s < " % (sub, line), level="debug")
        match = re.search(r'^(\d+-\d+-\d+ \d+:\d+:\d+ \S+)\s+(\S+)\s+(.*)',
                          line)
        match1 = re.search(r'^(\d+)|(\S+) alarms currently active', line)
        if match:
            device.log(message="%s: match >%s<" % (sub, line))
            alarm['time'] = match.group(1)
            alarm['class'] = match.group(2)
            alarm['description'] = match.group(3)
            alarm['short-description'] = match.group(3)[0:19]
            alarm['type'] = 'Chassis'
            alarms.append(alarm)
        elif match1:
            alarm_count = match1.group(1)
            device.log(message="%s: alarm_num = %s" % (sub, alarm_count),
                       level="debug")

    if alarm_count != len(alarms):
        device.log(
            message="%s : Incorrect active alarms count(%s)" % (sub,
                                                                alarm_count))
    if alarm_count:
        return alarms
    else:
        device.log(message="No alarms currently active")
        return alarms
# end def __cli_get_alarm


def __cli_get_mac(device, **kwargs):
    """
    Get chassis mac address information using cli command
    "show chassis mac-addresses"

    :param device:
        **REQUIRED** Device handle
    :params chassis :
        *OPTIONAL* Chassis for which the MAC address is obtained

    :returns:
        Dictionary of chassis mac-addresses
    """
    chassis = kwargs.get('chassis', '')
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside " + sub + "...", level="debug")
    mac_addr = {}
    cli_cmd = "show chassis mac-addresses "
    if chassis:
        cli_cmd += chassis
    else:
        cli_cmd = cli_cmd

    # Execute cli command 'show chassis mac-addresses'
    resp = device.cli(command=cli_cmd).response()
    mac_regexp = '([a-f0-9]+:[a-f0-9]+:[a-f0-9]+:[a-f0-9]+:[a-f0-9]+:[a-f0-9]+)'
    # In reponse of 'show chassis mac-addresses' search for MAC address details
    for line in resp.split('\n'):
        match = re.search(r'\s*MAC address information:', line)
        match1 = re.search(r'\s*Public base address\s*' + mac_regexp, line)
        match2 = re.search(r'\s+Public count\s+(\d+)', line)
        match3 = re.search(r'\s*Private base address\s*'+mac_regexp, line)
        match4 = re.search(r'.*\s+Private count\s+(\d+).*$', line)
        # Incase of match get the details in dictionary
        if match:
            device.log(message=sub + " MAC address information: ",
                       level="debug")
        elif match1:
            mac_addr['public-base-address'] = match1.group(1)
            device.log(
                message=sub + " Public   base address> " + match1.group(1) + "<",
                level="debug")
        elif match2:
            mac_addr['public-count'] = match2.group(1)
            device.log(message=sub + "Public  count> " + match2.group(1) + "<",
                       level="debug")
        elif match3:
            mac_addr['private-base-address'] = match3.group(1)
            device.log(
                message=sub + "Private   base address> " + match3.group(1) + "<",
                level="debug")
        elif match4:
            mac_addr['private-count'] = match4.group(1)
            device.log(
                message=sub + "Private   count> " + match4.group(1) + "<",
                level="debug")
        else:
            device.log(message="show chassis mac-addresses FAILED ! ",
                       level="error")
    return mac_addr
# end def __cli_get_mac


def __cli_get_ethernet(device):
    """
    Gets the information of the ethernet switch like port, status,
    speed, duplex and the link to which the port is connected
    to the device

    :param device:
        **REQUIRED** Device handle

    :return:
        Dictionary with details of ethernet_switch
    """
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    ethernet_switch = {}
    device.log(message="Inside %s subroutine" % sub, level="debug")
    cmd = "show chassis ethernet-switch"
    # Execute cli command "show chassis ethernet-switch"
    response = device.cli(command=cmd).response()
    lines = response.split("\n")
    device_name = ''
    # In each lines of response search for device name, port, status,
    # port speed, and duplex
    for line in lines:
        device.log(message=" line=" + line+"\n" + "", level="debug")
        match = re.search(
            r'\s*Link is (\S+) on .E port (\d+) connected to device: (.*)',
            line)
        match1 = re.search(r'^\s+Speed is (\S+)', line)
        match2 = re.search(r'^\s+Duplex is (\S+)', line)
        if match:
            status = match.group(1)
            port = match.group(2)
            device_name = match.group(3).lower()
        elif match1:
            speed = match1.group(1)
        elif match2:
            duplex = match2.group(1)
        # After reading all lines (search for new line) save the details
        # in a dictionary
        elif re.search(r"^\s*$", line):
            if device_name:
                if device_name not in ethernet_switch.keys():
                    ethernet_switch[device_name] = {}
                ethernet_switch[device_name]['port'] = port
                ethernet_switch[device_name]['status'] = status
                ethernet_switch[device_name]['speed'] = speed
                ethernet_switch[device_name]['duplex'] = duplex
                device_name = port = status = duplex = None
        else:
            device.log(
                message="show chassis ethernet-switch command has no output")
    show_data(device, ethernet_switch, sub + 'return:')
    return ethernet_switch
# end def __cli_get_ethernet


def __cli_get_craft(device, **kwargs):
    """
    Get cli output of show chassis craft interface.
       - Displays the status of LED and relays on the LCD screen
       - Displays the name of the router, how long the router
       has been operational and FPM contents.

    :param device:
        **REQUIRED** Device handle
    :param chassis :
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)

    :returns:
        Information currently on craft display
    """
    chassis = kwargs.get('chassis', '')
    model = device.get_model()
    sub = function_name(device)
    device.log(message="Inside %s (%s)" % (sub, model), level="debug")
    craft = {'alarm': {}, 'fpc': {}, 're': {}, 'display': []}
    item = ""
    cli_cmd = "show chassis craft-interface"
    if chassis:
        cli_cmd += str(chassis)
    response = device.cli(command=cli_cmd).response()
    led_value = {'on': 1, 'off': 0, 'On': 1, 'Off': 0, '*': 1, '.': 0}
    for line in response.split('\n'):
        device.log(message=" %s sub: line(%s) " % (sub, line), level="debug")
        model_list = 'm5|m[124]0|m7i|m10i|IRM'
        if model in model_list:
            match = re.search(r'Red alarm:\s+LED (\S+), relay (\S+)', line)
            match1 = re.search(r'^Yellow alarm:\s+LED (\S+), relay (\S+)',
                               line)
            match2 = re.search(r'^Routing Engine (\S+) LED:\s+(\S+)', line)
            match3 = re.search(r'^Green\s+([*.]\s.*)', line)
            match4 = re.search(r'^Red\s+([*.]\s.*)$', line)
            match5 = re.search(r'(\|.*\|)', line)
            match6 = re.search(r'(\+-.*[+|])', line)
            if match:
                value1 = led_value[match.group(1)]
                value2 = led_value[match.group(2)]
                craft['alarm']['red'] = value1
                craft['alarm']['major'] = value2
            elif match1:
                value1 = led_value[match1.group(1)]
                value2 = led_value[match1.group(2)]
                craft['alarm']['yellow'] = value1
                craft['alarm']['minor'] = value2
            elif match2:
                type_val = match2.group(1)
                type_val = type_val.lower()
                if led_value[match2.group(2)]:
                    craft['re'][type_val] = 1
            elif match3:
                fpc_green_led = match3.group(1).split(' ')
                craft['fpc'] = {}
                fpc_green_led = list(filter(None, match3.group(1).split(' ')))
                for value in range(0, len(fpc_green_led)):
                    craft['fpc'][value] = {}
                    if led_value[fpc_green_led[value]]:
                        craft['fpc'][value]['green'] = 1

            elif match4:
                fpc_red_led = list(filter(None, match4.group(1).split(' ')))
                for value in range(0, len(fpc_red_led)):
                    craft['fpc'][value] = {}
                    if led_value[fpc_red_led[value]]:
                        craft['fpc'][value]['red'] = 1

            elif match5 or match6:
                if match5:
                    craft['display'].append(match5.group(1))
                if match6:
                    craft['display'].append(match6.group(1))
        else:
            if re.search(r'^FPM Display contents:', line):
                item = 'display'
            elif re.search(r'^Front Panel Alarm Indicators:', line):
                item = 'alarm'
            elif re.search(r'\s*(\S+)\sLEDs:', line):
                match = re.search(r'\s*(\S+)\sLEDs:', line)
                item = match.group(1)
                if item == 'System':
                    item = 're'
                elif item == 'PS':
                    item = 'pem'
                else:
                    item = item.lower()
            else:
                if item == 'display':
                    match = re.search(r'(\|.*\|)', line)
                    match1 = re.search(r'(\+.*[\+\|])', line)
                    if match:
                        craft['display'].append(match.group(1))
                    if match1:
                        craft['display'].append(match1.group(1))
                elif item == 'alarm':
                    match = re.search(r'^(\S+)\s\S+\s+([*.])', line)
                    if match:
                        type_val = match.group(1)
                        type_val = type_val.lower()
                        if led_value[match.group(2)]:
                            craft['alarm'] = {}
                            craft['alarm'][type_val] = 1
                else:
                    # craft[item]={}
                    match = re.search(r'^(\S+)\s+([*.].*)$', line)
                    if match:
                        color = match.group(1).lower()
                        fru_led = match.group(2).split()
                        craft[item] = {}
                        for value in range(0, len(fru_led)):
                            if led_value[fru_led[value]]:
                                craft[item][value] = {}
                                craft[item][value][color] = 1
    show_data(device, craft, sub + 'return:')
    return craft
# end def __cli_get_craft


def check_craft_display(device, **kwargs):
    """
    Robot Usage Example :
        ${device_object}  =  Get Handle  resource=r1
        ${result}  =  Check Craft Display   device=${device_object}
        ...    chassis='sfc 0'  sd='rsd'  display='ntt'

    Check craft display for fru using cli "show chassis craft-interface" cmd
      - Not applicable for m120|mx|psd|a40|srx5800|a15|a20|srx5600|srx5400|
                        a10|srx3600|a2|srx3400|srx1400 platform

    :param device:
        **REQUIRED** Device handle
    :params chassis:
        *OPTIONAL* Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :params craft:
        *OPTIONAL*  Dictionary for craft display (get current display
        by default)
    :param display:
        **REQUIRED**  a regular expression in display message such as hostname
    :params check_count:
        **OPTIONAL** Check count. Default is 1
    :params check_interval:
        **OPTIONAL** Wait time before next retry. Default 10 seconds

    : returns: Craft display checking passed or failed.
    """
    valid_keys = ['chassis', 'craft', 'display', 'check_count',
                  'check_interval']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s ..." % sub, level="debug")
    chassis = kwargs.get('chassis', '')
    display = kwargs.get('display', '')
    craft = kwargs.get('craft')
    # pass_val = ''
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    if re.search(r'^m120|mx|psd|a40|srx5800|a15|a20|srx5600|srx5400 \
                  |a10|srx3600|a2|srx3400|srx1400', model, re.IGNORECASE):
        device.log(
            message="%s: skip display checking for " % sub +
            "(m120|mx|psd|a40|srx5800|a15|a20|srx5600|srx5400|a10|" +
            "srx3600|a2|srx3400|srx1400) platform ",
            level="warn")
        return True
    if craft:
        check_count = 1

    for value in range(0, check_count):
        check_info = "count(%s), interval(%s)" % (check_count, check_interval)
        __sleep(device, value, sub, check_interval, check_info)
        if not craft:
            craft = get_chassis_craft(device, chassis=chassis)
        craft_display = ''
        if 'display' in list(craft) and len(craft['display']) != 0:
            craft_display = craft['display'][1]
        else:
            device.log(
                message="%s: craft display (%s) does not contains display(%s),%s"
                % (sub, craft_display, display, check_info), level="warn")
            result = False
        match_val = re.search(r"\|\(noname\)*\s*\|", craft_display)
        match_val1 = re.search(r"\|"+display+r"\s*\|", craft_display)
        if (display == '' and match_val) or match_val1:
            device.log(
                message="%s: craft display (%s) contains display(%s),%s"
                % (sub, craft_display, display, check_info),
                level="debug")
            result = True
        else:
            device.log(
                message="%s: craft display (%s) does not contains display(%s),%s"
                % (sub, craft_display, display, check_info),
                level="warn")
            result = False
    return result
# end def check_craft_display


def check_craft_alarm(device, **kwargs):
    """
    Robot Usage Example :
        ${device_object} =  Get Handle  resource=r1
        ${alarm} =  Evaluate  ({'alarm':['Minor']})
        &{craft} =  Evaluate  ({'alarm': ['None'],'display': [],'fpc': {},
        ...    're': {'ok': 1}})
        ${result} =  Check Craft Alarm   device=${device_object}
        ...    chassis='sfc 0'  sd='rsd'  craft=${craft}  alarm=${alarm}

    Check craft display for fru using command "show chassis craft-interface"

    :param device:
        **REQUIRED** Device handle
    :param chassis:
        **REQUIRED** Chassis type ( scc | sfc | lcc 0| 1| 2 | 3)
    :param sd:
        **REQUIRED** rsd | psd1|psd2|psd3|..
    :param craft:
        **REQURED**  Dictionary for craft display
    :param alarm:
        **REQUIRED**  Display Screen
    :param check_count:
        **OPTIONAL** Check count. Default is 1
    :param chk_interval:
        **OPTIONAL** Wait time before next retry. Default 10 seconds

    : returns:
    Craft display checking passed or failed.
    """
    valid_keys = ['chassis', 'sd', 'craft', 'alarm', 'check_count',
                  'check_interval']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    chassis = kwargs.get('chassis')
    sd = kwargs.get('sd')
    craft = kwargs.get('craft')
    alarm = kwargs.get('alarm', '')
    check_count = kwargs.get('check_count', 1)
    check_interval = kwargs.get('check_interval', 10)
    model = device.get_model()
    sub = function_name(device) + " (%s)" % model
    device.log(message="Inside %s %s ..." % (sub, str(kwargs)))
    if not (craft or alarm):
        __error_arg_msg(device, 'craft|alarm', sub)
    pass_val = False
    for value in range(0, check_count):
        check_info = "count(%s), interval(%s)" % (check_count, check_interval)
        __sleep(device, value, sub, check_interval, check_info)
        if craft and value > 0:
            break
        if not alarm:
            alarm = get_chassis_alarm(device, chassis=chassis, sd=sd)
        if not craft:
            craft = get_chassis_craft(device, chassis=chassis, sd=sd)
        craft_alarms = []
        for j in range(0, 3):
            if not isinstance(craft, bool) and 'display' in list(craft) and\
                    len(craft['display']) != 0:
                alarm_display = craft['display'][j+2] or ''
                device.log(
                    message="%s: alarm_display(%s)" % (sub, alarm_display))
                match = re.search(r'\|Y: (.*)\s*\|', alarm_display)
                match1 = re.search(r'\|R: (.*)\s*\|', alarm_display)
                if match:
                    result = __convert_alarm_display(
                        device, 'Minor', match.group(1))
                    craft_alarms.append(result)

                elif match1:
                    result = __convert_alarm_display(
                        device, 'Major', match1.group(1))
                    craft_alarms.append(result)
            else:
                device.log(
                    message="%s: No display found, %s" % (sub, check_info),
                    level="debug")
        sleep(check_interval)
        return_value = check_chassis_alarm(device,
                                           chassis=chassis,
                                           sd=sd,
                                           alarm=craft_alarms,
                                           check_alarm=alarm)
        if return_value:
            device.log(
                message="%s: alarm display check passed, %s" % (sub,
                                                                check_info),
                level="debug")
            pass_val = True
    if not pass_val:
        device.log(message="%s:alarm display check failed")
        return False
    return True
# end def check_craft_alarm


def check_fabric_plane(device, **kwargs):
    """
    Robot Usage Example :
      ${dh} =    Get Handle   resource=r1
      ${kwargs} = Evaluate    {check_interval:'10'}
      ${result} =    Check Fabric Plane    device=${dh}    &{kwargs}

        Check fabric link ok by compare FEB and fabric status

    :param device:
        **REQUIRED** Device handle
    :param CHK_INTERVAL :
        OPTIONAL Wait time before next retry (default 10 seconds)

    :return :
        TRUE if check fabric plane successful
        FALSE if check fabric plane unsuccessful
    """
    valid_keys = ['links']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    model = device.get_model().lower()
    sub = function_name(device) + '-' + model
    device.log(message='Inside %s %s ...' % (sub, str(kwargs)), level='debug')
    patt_check_model = "m120|mx960|mx240|mx480|a40|srx5800|a15|a20|" +\
        "srx5600|srx5400|a10|srx3600|a2|srx3400|ex8208|ex8216"
    if not re.search(r"^(%s)$" % patt_check_model, model):
        device.log(
            message="%s: only %s are supported" % (patt_check_model, sub),
            level='error')
        return False
    patt_tot_pfe = "mx240|mx480|a40|srx5800|a15|a20|srx5600|srx5400|" + \
        "a10|srx3600|a2|srx3400|ex82[01][68]"
    if re.search(r"^(%s)" % patt_tot_pfe, model):
        tot_pfe = 4
    else:
        tot_pfe = 1
    if re.search(r"^m120$", model):
        feb_status = get_fru_status(device, fru='feb')
    else:
        fpc_status = get_fru_status(device, fru='fpc')
    fabric_status = get_fabric_status(device)
    result = True
    if re.search(r"^m120$", model):
        fb_planes = get_fabric_plane(device)
        for plane in range(0, len(fb_planes)):
            if re.search(r"^(Online|Check)$",
                         fabric_status[plane]['state']):
                if fb_planes[plane]['state'] == 'ACTIVE':
                    for slot in range(0, len(kwargs['links'])):
                        if feb_status[slot]['state'] == 'Online':
                            if kwargs['links'][slot] != 'ok':
                                device.log(
                                    message="%s: FEB %s Online but link to plane %s not OK"
                                    % (sub, slot, plane), level='error')
                                result = False
                        elif kwargs['links'][slot] == 'ok':
                            device.log(
                                message="%s: FEB %s not Online but link to plane %s OK"
                                % (sub, slot, plane), level='error')
                            result = False
                else:
                    device.log(message="%s: plane %s is Online but not ACTIVE"
                               % (sub, plane), level='error')
                    result = False
            elif not re.search(r'^(OFFLINE)$', fb_planes[plane]['state']):
                device.log(
                    message="%s: fabric plane %s not Online should show offline"
                    % (sub, fb_planes[plane]['state']), level='WARNING')
    else:
        fb_planes = get_fabric_plane(device)
        for plane in range(0, len(fb_planes)):
            if fb_planes[plane] is None:
                continue
            if re.search(r'^(Online|Check|Spare)$',
                         fabric_status[plane]['state']):
                if re.search(r'^(ACTIVE|SPARE)$',
                             fb_planes[plane]['state']):
                    for slot in range(
                            0, len(fb_planes[plane]['links']['fpc'])):
                        if fb_planes[plane]['links']['fpc'][slot]:
                            for pfe in range(0, tot_pfe):
                                if re.search(r'Online',
                                             fpc_status[pfe]['state'],
                                             re.M | re.I):
                                    if fb_planes[
                                            plane]['links']['fpc'][slot][
                                                'pfe'][pfe] != 'ok':
                                        device.log(message="%s: fpc %s Online but "
                                                           "link to plane %s not OK"
                                                   % (sub, slot, plane),
                                                   level='error')
                                        result = False
                                        break
                                elif fb_planes[plane]['links']['fpc'][
                                        slot]['pfe'][pfe] == 'ok':
                                    device.log(
                                        message="%s: fpc %s " % (sub, slot) +
                                        "not Online but link to " +
                                        "plane %s OK" % plane,
                                        level='error')
                                    result = False
                else:
                    device.log(
                        message="%s: plane %s is Online but not ACTIVE or SPARE"
                        % (sub, plane), level='error')
                    result = False
            elif fb_planes[plane]['state'].lower() != 'offline':
                device.log(
                    message="%s: plane %s is Online but not ACTIVE or SPARE"
                    % (sub, plane), level='error')
                result = False
    return result
# end def check_fabric_plane


def __chop(device, string):
    """
    Remove any whitespace character (space, tab, newline) at
    the begin and the end of string

    :param device:
        **REQUIRED** Device handle
    :param  str
        REQUIRED string input

    :return a new string
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')

    if string == None: return None
    new_str = string.strip().rstrip()

    return new_str
# end def __chop


def __get_pic_status(device, fpc_slot, pic, chas_fru):
    """
    Get pic status from fpc slot

    :param device:
        **REQUIRED** Device handle
    :param fpc_slot
        REQUIRED fpc slot number
    :param pic
        REQUIRED pic dictionary
    :param chas_fru
        chassis fru dictionary information

    :return chas_fru
        chassis fru dictionary information
    """

    pic_slot = pic['pic-slot']
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    if 'pic' not in chas_fru:
        chas_fru['pic'] = {}
    if fpc_slot not in chas_fru['pic']:
        chas_fru['pic'][fpc_slot] = {}
    if pic_slot not in chas_fru['pic'][fpc_slot]:
        chas_fru['pic'][fpc_slot][pic_slot] = {}

    for key in pic.keys():
        if key == 'pic-slot':
            continue
        chas_fru['pic'][fpc_slot][pic_slot][key] = pic[key]

    return chas_fru
# end def __get_pic_status


def __get_fru_craft(device, fru_list):
    """
    Create fru craft dictionary

    :param device:
        **REQUIRED** Device handle
    :param fru_list
        REQUIRED list of fru or dictionary of fru

    :return fru_craft
        the dictionary of fru_craft
    """

    fru_craft = {}

    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')

    if isinstance(fru_list, list):
        device.log(message="%s: fru_list is a list" % sub, level='debug')
        for fru in fru_list:
            if 'slot' not in fru.keys():
                continue
            slot = __chop(device, fru['slot'])
            device.log(message="%s: slot(%s)" % (sub, slot), level='debug')
            fru_craft[slot] = __get_fru_led(device, fru)
    else:
        device.log(message="%s: fru_list is NOT a list" % sub, level='debug')
        fru_craft = __get_fru_led(device, fru_list)

    return fru_craft
# end def __get_fru_craft


def __get_fru_led(device, led):
    """
    Create fru led dictionary

    :param device:
        **REQUIRED** Device handle
    :param led
        REQUIRED a dictionary of fru led

    :return fru
        the dictionary of fru
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')

    fru = {}
    for i in led.keys():
        check = re.match(r'^(\S+)-led$', i)
        if check:
            fru_key = check.group(1)
            fru[fru_key] = 1

    return fru
# end def __get_fru_led


def __get_alarm_led(device, led):
    """
    Create alarm dictionary for led

    :param device:
        **REQUIRED** Device handle
    :param led
        REQUIRED a dictionary of alarm led

    :return fru
        the dictionary of fru
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')

    fru = {}
    for i in led.keys():
        check = re.match(r'^([a-z]+)-.*$', i)
        if check:
            fru_key = check.group(1)
            fru[fru_key] = 1

    return fru
# end def __get_alarm_led


def __timeless(device, time1, time2):
    """
    Compare 2 times

    :param device:
        **REQUIRED** Device handle
    :param time1
        REQUIRED time in format %H:%M:%S
    :param time2
        REQUIRED time in format %H:%M:%S

    :return
        True if time1  < time2
        False if time1 >= time2
    """

    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    try:
        check1 = datetime.datetime.strptime(time1, '%H:%M:%S')
        check2 = datetime.datetime.strptime(time2, '%H:%M:%S')
    except Exception:
        device.log(message="Argument is not in time format", level='info')
        return False
    if check1 < check2:
        return True
    return False
# end def __timeless


def show_data(device, *args):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Show Data  device=${device_object}  'string1'  'string2'

    Show dump data for debugging

    :param device:
        **REQUIRED** Device handle
    :param *args
        REQUIRED
        arg 1st is data need for dumping
        arg 2nd is information need for debugging

    :return None
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    device.log(message="%s" % args[1], level='debug')
    device.log(message="%s" % pprint(args[0]), level='debug')
    return True
# end def show_data


def __check_fru1_led(device, fru, craft, status, chas=None):
    """
    Check fru 1 led

    :param device:
        **REQUIRED** Device handle
    :param fru string
        fru name (re,pem,fan...)
    :param craft
        Craft interface as dictionary
    :param status
        dicstionary of chasis info
    :param chas chasis
        dicstionary of chasis info

    :return  Boolean
        True: if check successfully
        False:if check unsuccessfully
    """
    sub = function_name(device)
    online_state = ''
    # get the device model
    model = device.get_model().lower()

    device.log(message="Inside %s..." % sub, level='debug')
    if fru is 'sib':
        online_state = '(Online|Spare)'
    else:
        online_state = 'Online'
    num = CHASSIS_FRU[model.lower()][fru]
    for i in range(0, num):
        device.log(message="%s: checking %s %s  ..." % (sub, fru, i),
                   level='debug')
        if i < len(status[fru]):
            if 'state' in status[fru][i]:
                state = __chop(device, status[fru][i]['state'])
            else:
                state = ''
            led_chk_info = "%s: %s %s LED check, state(%s)" % (
                sub, fru, i, state)
            if re.search(r'^tx', model, flags=re.IGNORECASE) and chas and \
                    chas is 'scc' and fru and fru is 'sib':
                led = craft[fru][i]
                if (state is 'Spare' and led.get('ok') and
                        not led.get('fail') and not led.get('active')) or \
                        (state is 'Online' and led.get('ok') and
                         not led.get('fail') and led.get('active')) or \
                        (not re.search(r'^Spare|Online$', state, re.I) and
                         not led.get('ok') and not led.get('fail') and
                         not led.get('active')):
                    device.log(message="%s (OK|Fail|Active) passed"
                               % led_chk_info, level='info')
                else:
                    device.log(message="%s (OK|Fail|Active) failed"
                               % led_chk_info, level='warn')
                    return False
            elif re.search(r'^ptx5000', model, flags=re.IGNORECASE) and \
                    fru and fru is 'sib':
                led = craft.get(fru)[i]
                if state in online_state and led.get('active') and \
                        led.get('ok'):
                    device.log(message="%s (OK|Fail|Active) failed" %
                               led_chk_info)
                    return False
            elif fru and fru is 'sib' and state and state is 'Check' or \
                    re.search(online_state, state, re.I):
                if craft.get(fru)[i].get('green') and \
                        not craft.get(fru)[i].get('red'):
                    device.log(message="%s (green) passed" % led_chk_info,
                               level="info")
                else:
                    device.log(message="%s (green) failed" % led_chk_info,
                               level="warn")
                    return False
            elif status[fru][i].get('comment') and \
                    status[fru][i].get('comment') in 'Unresponsive' \
                    or (fru and fru is 'pem' and state and state is 'Present'):
                if not craft[fru][i].get('green') and craft[fru][i].get('red'):
                    device.log(message="%s (red) passed" % led_chk_info,
                               level='info')
                else:
                    device.log(message="%s (red) failed" % led_chk_info,
                               level="warn")
                    return False
            else:
                if not craft[fru][i].get('green') and \
                        not craft[fru][i].get('red'):
                    device.log(message="%s (off) passed" % led_chk_info,
                               level='info')
                else:
                    device.log(message="%s (off) failed" % led_chk_info,
                               level="warn")
                    return False
    device.log(message="%s: fru(%s) LED check passed" % (sub, fru),
               level='info')
    return True
# end def __check_fru1_led


def __check_fru2_led(device, fru, craft, status):
    """
    Check fru 2 led

    :param device:
        **REQUIRED** Device handle
    :param fru
        fruname
    :param craft
        Craft interface as dictionary
    :param status
        Status of RE (Master, Backup...)

    :return  Boolean
        True: if check successfully
        False:if check unsuccessfully
    """

    sub = function_name(device)
    no_blue_led = False
    device.log(message="Inside %s" % sub)

    model = device.get_model().lower()
    model_list = "mx2010|mx2020|m120|mx960|mx240|mx480|a40|" + \
        "srx5800|a15|a20|srx5600|srx5400|a10|srx3600|a2|srx3400|" + \
        "ex82[01][68]"
    if fru == 'cb' and model in model_list:
        no_blue_led = True
    num = CHASSIS_FRU[model.lower()][fru]
    if model in "a40|srx5800" or not status[fru][1]['state']:
        num = 1

    device.log(message="%s: FRU count, after A40 check: %s" % (sub, num))

    for i in range(0, num):
        device.log(
            message="%s: checking %s %s now when retrying %s time(s) ..." %
            (sub, fru, i, i))

        led_chk_info = "%s: %s %s LED check" % (sub, fru, i)
        if not status[fru][i]['status'] and\
                status[fru][i]['state'] is 'Offline':
            if not craft[fru][i].get('green'):
                if not craft[fru][i].get('amber'):
                    if not craft[fru][i].get('blue') or no_blue_led:
                        device.log(message="%s (off) passed" % led_chk_info)
                    else:
                        device.log(message="%s (off) failed" % led_chk_info)
                        return False

        elif status[fru][i]['status'] and\
                status[fru][i]['state'] is 'Online':
            if craft[fru][i].get('green'):
                if not craft[fru][i].get('amber'):
                    if not craft[fru][i].get('blue') or no_blue_led:
                        device.log(message="%s (green) passed" % led_chk_info)
                    else:
                        device.log(message="%s (green) failed" % led_chk_info)
                        return False

        elif status[fru][i]['status'] is 'Master':
            if craft[fru][i].get('green'):
                if not craft[fru][i].get('amber'):
                    if craft[fru][i].get('blue') or no_blue_led:
                        device.log(message="%s (green,blue) passed" %
                                   led_chk_info)
                    else:
                        device.log(message="%s (green,blue) failed" %
                                   led_chk_info)
        elif status[fru][i]['status'] is 'Standby':
            if craft[fru][i].get('green'):
                if not craft[fru][i].get('amber'):
                    if not craft[fru][i].get('blue') or no_blue_led:
                        device.log(message="%s (blue) passed" % led_chk_info)
                    else:
                        device.log(message="%s (blue) failed" % led_chk_info)
                        return False
        else:
            device.log(message="%s: unsupported case for %s" % (sub, fru))
    device.log(message="%s: fru(%s) LED check passed" % (sub, fru))
    return True
# end def __check_fru2_led


def __check_re_led(device, craft, status):
    """
        Check led status of Chassis FRU

    :param device:
        **REQUIRED** Device handle
    :param craft:
        REQUIRED dict for craft display
    :param status:
        REQUIRED dict for fru status

    :return :
        TRUE if check re led successful
        FALSE if check re led unsuccessful
    """

    model = device.get_model().lower()
    sub = function_name(device) + ' ' + model
    device.log(message="Inside %s..." % sub, level='debug')
    _end = CHASSIS_FRU[model.lower()].get('re', 0)

    for i in range(0, _end):
        device.log(message="%s: checking re %s ..." % (sub, i), level='debug')
        led_chk_info = "%s: re %s LED check" % (sub, str(i))
        if re.search(r'^(m5|m[124]0|m7i|m10i|IRM)$', model):
            if craft['re'].get('ok') and \
                    not craft['re'].get('fail'):
                device.log(message="%s (ok) passed" % led_chk_info,
                           level='info')
            else:
                show_data(device, craft['re'], "%s, %s=" % (sub, craft['re']))
                device.log(message="%s (ok) failed)" % led_chk_info,
                           level='warn')
                return False
            break
        else:
            state = status['re'][i].get('mastership-state')
            device.log(message="%s: state(%s)" % (sub, state), level='debug')
            __chop(device, state)
            if state == 'master':
                if craft['re'][i].get('ok') and \
                        not craft['re'][i].get('fail') and \
                        craft['re'][i].get('master'):
                    device.log(message="%s (ok,master) passed" % led_chk_info,
                               level='info')
                else:
                    show_data(device, craft['re'], "%s, %s=" % (sub,
                                                                craft['re']))
                    device.log(message="%s (ok) failed" % led_chk_info,
                               level='warn')
                    return False
            elif state == 'backup':
                if craft['re'][i].get('ok') and \
                        not craft['re'][i].get('fail') and \
                        not craft['re'][i].get('master'):
                    device.log(message="%s (ok) passed" % led_chk_info,
                               level='info')
                else:
                    show_data(device, craft['re'], "%s, %s=" % (sub,
                                                                craft['re']))
                    device.log(message="%s (ok) failed" % led_chk_info,
                               level='warn')
                    return False
            elif not status['re'][i].get('status') or \
                    state == 'Present':
                if craft['re'][i].get('ok') and \
                        not craft['re'][i].get('fail') and \
                        not craft['re'][i].get('master'):
                    device.log(message="%s (off) passed" % led_chk_info,
                               level='info')
                else:
                    show_data(device, craft['re'], "%s, %s=" % (sub,
                                                                craft['re']))
                    device.log(message="%s (off) failed" % led_chk_info,
                               level='warn')
                    return False
            else:
                show_data(device, craft['re'], "%s, %s=" % (sub, craft['re']))
                device.log(message="%s: unsupported case for re" % sub,
                           level='error')
    device.log(message="%s: fru re LED check passed" % sub, level='info')
    return True
# end def __check_re_led


def __check_sfm_led(device, craft, status):
    """
        Check sfm led of Chassis FRU

    :param device:
        **REQUIRED** Device handle
    :param craft:
        REQUIRED dict for craft display
    :param status:
        REQUIRED dict for fru status

    :return :
        TRUE if check sfm led successful
        FALSE if check sfm led unsuccessful
    """

    model = device.get_model().lower()
    sub = function_name(device) + ' ' + model
    device.log(message="Inside %s..." % sub, level='debug')
    if not CHASSIS_FRU.get(model.lower()):
        device.log(message="%s: chassis_fru do not have model %s ..."
                   % (sub, model), level='error')
        return False
    _end = CHASSIS_FRU[model.lower()].get('sfm')
    if _end is None:
        device.log(message="%s: model %s has not 'sfm' key..."
                   % (sub, model), level='warn')
        return False
    for i in range(0, _end):
        device.log(message="%s: checking sfm %s ..." % (sub, i),
                   level='debug')
        led_chk_info = "%s: sfm %s LED check" % (sub, i)
        state = status['sfm'][i].get('state')
        if state is None:
            device.log(message="%s: Cannot find 'state' in status dict" % sub,
                       level='error')
            return False
        if state == 'Online':
            if craft['sfm'][i].get('green') and \
                    not craft['sfm'][i].get('amber') and \
                    craft['sfm'][i].get('blue'):
                device.log(message="%s (green,blue) passed" % led_chk_info,
                           level='info')
            else:
                device.log(message="%s (green,blue) failed" % led_chk_info,
                           level='warn')
                return False
        elif state == 'Online - Standby':
            if craft['sfm'][i].get('green') and \
                    not craft['sfm'][i].get('amber') and \
                    not craft['sfm'][i].get('blue'):
                device.log(message="%s (green) passed" % led_chk_info,
                           level='info')
            else:
                device.log(message="%s (green) failed" % led_chk_info,
                           level='warn')
                return False
        elif re.search(r'^Offline|Empty$', state):
            if not craft['sfm'][i].get('green') and \
                    not craft['sfm'][i].get('amber') and \
                    not craft['sfm'][i].get('blue'):
                device.log(message="%s (off) passed" % led_chk_info,
                           level='info')
            else:
                device.log(message="%s (off) failed" % led_chk_info,
                           level='warn')
                return False
        elif not craft['sfm'][i].get('green') and \
                craft['sfm'][i].get('amber') and \
                not craft['sfm'][i].get('blue'):
            device.log(message="%s (amber) passed" % led_chk_info,
                       level='info')
        else:
            device.log(message="%s (amber) failed" % led_chk_info,
                       level='warn')
            return False
    device.log(message="%s: sfm led check passed" % sub,
               level='info')
    return True
# end def __check_sfm_led


def __convert_alarm_display(device, level, descr):
    """
    Convert message of alarm

    :param device:
        **REQUIRED** Device handle
    :param level
        REQUIRED Level of alarm
    :param descr
        REQUIRED decription of message

    :return alarm
        Message of alarm
    """
    alarm = {}
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')

    descr = re.sub(r'Absnt', 'Absent', descr)
    descr = re.sub(r'VltSnsr', 'Volt Sensor', descr)
    descr = re.sub(r'LOS', ': SONET loss', descr)
    descr = re.sub(r'boot: alt', 'Boot from alternate media', descr)
    descr = re.sub(r'Slot \d+: errors', 'Too many unrecoverable errors',
                   descr)

    descr = descr.strip().rstrip()
    alarm['class'] = level
    alarm['description'] = descr

    device.log(message="%s: alarm(%s)" % (sub, descr), level='debug')

    return alarm
# end def __convert_alarm_display


def __convert_name(device, name):
    """
    Make fru's name consistent

    :param device:
        **REQUIRED** Device handle
    :param name
        REQUIRED string input

    :return new string name
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    if name == 'Routing Engine':
        name = 're'
    elif re.match(r'^Routing Engine (\d+)$', name):
        name = 're ' + re.match(r'^Routing Engine (\d+)$', name).group(1)
    elif name == 'Power Supply A':
        name = 'pem 0'
    elif name == 'Power Supply B':
        name = 'pem 1'
    elif re.match(r'^Power Supply (\d+)$', name):
        name = 'pem ' + re.match(r'^Power Supply (\d+)$', name).group(1)
    else:
        name = name.lower()

    return __chop(device, name)
# end def __convert_name


def __get_hardware(device, *args):
    """
    Get hardware information form args and
    store in first argument as a dictionary

    :param device:
        **REQUIRED** Device handle
    :param *args
        REQUIRED
        arg 1st is a dictionary for storing hardware information
        arg 2nd is name
        arg 3rd is version
        arg 4th is part number
        arg 5th is serial number
        arg 6th is description

    :return args[0]
    a dictionary for storing hardware information
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    args[0]['name'] = args[1]
    args[0]['version'] = args[2]
    args[0]['part-number'] = args[3]
    args[0]['serial-number'] = args[4]
    args[0]['description'] = args[5]
    return args[0]
# end def __get_hardware


def __error_arg_msg(device, *args):
    """
    Create log for debugging

    :param device:
        **REQUIRED** Device handle
    :param *args
        REQUIRED
        arg 1st is argument required
        arg 2nd is function name

    :return None
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    device.log(message="%s: argument(%s) required" % (args[1], args[0]),
               level='error')
# end def __error_arg_msg


def __sleep(device, step, sub, interval, info):
    """
    Sleep in seconds for next retry

    :param device:
        **REQUIRED** Device handle
    :param step
        REQUIRED Current step in invoking function
    :param sub
        REQUIRED name of invoked function
    :param interval
        REQUIRED Time in second for sleeping
    :param info
        REQUIRED checking info

    :return None
    """
    if step > 0:
        device.log(message="%s: wait %s seconds before next retry, %s"
                   % (sub, interval, info), level='info')
        sleep(interval)
# end def __sleep


def compare_data(device, **kwargs):
    """
    Robot Usage Example :
      ${device_object} =  Get Handle  resource=r1
      ${result} =  Compare Data   device=${device_object}  data1='String'
      ...    data2='String'

        Compare 2 data structures (ignore case)

    :param device:
        **REQUIRED** Device handle
    :param data1
        REQUIRED array, hash or string
    :param data2
        REQUIRED array, hash or string

    :return :
        TRUE if 2 datas matches
        FALSE if 2 datas does not match
    """
    valid_keys = ['var1', 'var2', 'skip_list']
    required_keys = ['var1', 'var2']
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    var1 = kwargs.get('var1')
    var2 = kwargs.get('var2')
    skip_list = kwargs.get('skip_list', "")
    sub = function_name(device)
    device.log(message="Inside %s(%s)" % (sub, pprint(kwargs)), level='debug')
    device.log(message="%s: var1: %s" % (sub, pprint(var1)), level='debug')
    device.log(message="%s: var2: %s" % (sub, pprint(var2)), level='debug')
    skip_key = []
    # Creating skip_keys from skip_list
    if isinstance(skip_list, list):
        device.log(message="%s: skip_list %s"
                   % (sub, pprint(skip_list)), level='debug')
        for key in skip_list:
            skip_key.append(key)
    else:
        device.log(message="%s: skip_list does not exist" % sub, level='debug')
    # Checking for arguments passed
    device.log(message="%s: comparing var1(%s), var2(%s)"
               % (sub, pprint(var1), pprint(var2)), level='debug')
    if isinstance(var2, dict):
        if not isinstance(var1, dict):
            # return false if type of var1 is not dict and var2 is dict
            device.log(message="%s: incorrect data type var1(%s), not a dict)"
                       % (sub, pprint(var2)), level='warn')
            show_data(device, var1, "%s: var1" % sub)
            show_data(device, var2, "%s: var2" % sub)
            return False
        # if both var1 and var2 are dict get the keys
        if len(var2.keys()) > len(var1.keys()):
            list_key = var2.keys()
        else:
            list_key = var1.keys()
        msg = '%s: compare_data() return FALSE, key(%s) not in %s'
        # compare var1 and var2 keys
        for key in list_key:
            if key in skip_key:
                continue
            elif key not in var1.keys():
                device.log(message=msg % (sub, key, 'var1'), level='warn')
                return False
            elif key not in var2.keys():
                device.log(message=msg % (sub, key, 'var2'), level='warn')
                return False
            elif not compare_data(device, var1=var1[key], var2=var2[key],
                                  skip_list=skip_list):
                device.log(
                    message="%s: compare_data() return FALSE for key(%s)"
                    % (sub, key), level='warn')
                return False
    # return false if type of var1 is not list and var2 is list
    elif isinstance(var2, list):
        if not isinstance(var1, list):
            device.log(message="%s: incorrect data type var1(%s), not a list)"
                       % (sub, pprint(var2)), level='warn')
            show_data(device, var1, "%s: var1" % sub)
            show_data(device, var2, "%s: var2" % sub)
            return False
        # var1.sort()
        # var2.sort()
        # if both var1 and var2 are list compare each element
        if len(var1) != len(var2):
            device.log(message="%s: var1 and var2 have not same length" % sub,
                       level='warn')
            return False
        for i in range(0, len(var2)):
            if not compare_data(device, var1=var1[i], var2=var2[i],
                                skip_list=skip_list):
                device.log(message="%s: incorrect data type for i=%s" % (sub,
                                                                         i),
                           level='warn')
                return False
    else:
        # return false if var2 is not dict/list and var1 is list/dict
        if isinstance(var1, dict) or isinstance(var1, list):
            device.log(message="%s: incorrect data type for var1(%s)"
                       % (sub, pprint(var1)), level='warn')
            return False
        # If var1, var2 are string compare them
        if isinstance(var1, str):
            var1 = var1.lower()
        if isinstance(var2, str):
            var2 = var2.lower()
        if var1 == var2:
            device.log(message="%s: var1 (%s) and var2 (%s) compare passed."
                       % (sub, pprint(var1), pprint(var2)), level='info')
        else:
            device.log(message="%s: var1 (%s) and var2 (%s) compare failed."
                       % (sub, pprint(var1), pprint(var2)), level='info')
            return False
    return True
# end def compare_data


def __get_chassis_inventory(device, xml):
    """
    get chassis inventory from xml object

    :param device:
        **REQUIRED** Device handle
    :param xml:
        REQUIRED xml format (string)

    :return chas_hardware:
        Dictionary of chassis hardware include name, serial-number,
        description
    """
    sub = function_name(device)
    # Call put_log
    device.log(message="Inside %s subroutine" % sub, level='debug')
    chas_hardware = {}
   
    chassis_names = xml.findall(".//chassis")
    for chassis_name in chassis_names:
        for child in chassis_name.getchildren():
            key = child.tag
            if key == "name":
                chas_name = __chop(device, chassis_name.find(key).text).\
                    lower()
                chas_hardware[chas_name] = {}
            else:
                if not key == "chassis-module":
                    chas_hardware[chas_name][key] = __chop(
                        device, chassis_name.find(key).text)

    chassis_modules = xml.findall(".//chassis-module")
    for chassis_module in chassis_modules:
        for child1 in chassis_module.getchildren():
            key1 = child1.tag
            if key1 == "name":
                module_name = __chop(device, child1.text).\
                    lower()
                module_name = __convert_name(device, module_name)
                chas_hardware[module_name] = {}
            if key1 == "chassis-sub-module":
                for sub_module in chassis_module:
                    for child2 in sub_module.getchildren():
                        key2 = child2.tag
                        if key2 == "name":
                            sub = __chop(
                                device, child2.text)
                            chas_hardware[module_name][sub] = {}
                        if key2 == "chassis-sub-sub-module":
                            for sub2_module in sub_module:
                                for child3 in sub2_module.getchildren():
                                    key3 = child3.tag
                                    if key3 == "name":
                                        sub2 = __chop(
                                            device, child3.text)
                                        chas_hardware[module_name][sub][sub2] = {}
                                    if key3 == "chassis-sub-sub-sub-module":
                                        for sub3_module in sub2_module:
                                            for child4 in \
                                                    sub3_module.getchildren():
                                                key4 = child4.tag
                                                if key4 == "name":
                                                    sub3 = __chop(device, child4.text)
                                                    chas_hardware[module_name][sub][sub2][sub3] = {}
                                                else:
                                                    chas_hardware[module_name][sub][sub2][sub3][key4] = \
                                                        __chop(device, child4.text)
                                    else:
                                        chas_hardware[module_name][sub][sub2][key3] = \
                                             __chop(device, child3.text)
                        else:
                            chas_hardware[module_name][sub][key2] = \
                                __chop(device, child2.text)
            else:
                if child1.text:
                    chas_hardware[module_name][key1] = __chop(
                        device, child1.text)
    device.log(message=" function %s, return %s"%(sub, chas_hardware), level="DEBUG")
    return chas_hardware    

# end def __get_chassis_inventory


def __get_alarm_info(device, alarm_info_xml):
    """
        Get list of detailed alarm informations

    :param device:
        **REQUIRED** Device handle
    :param alarm_info_xml
        REQUIRED alarm info in xml format

    :return alarms
        List of detailed alarm informations
    """
    sub = function_name(device)
    device.log(message="Inside %s" % sub, level='debug')

    ele = alarm_info_xml.find('.//active-alarm-count')
    if ele is None:
        alarm_count = 0
    else:
        alarm_count = __chop(device, ele.text)
        alarm_count = int(alarm_count)

    alarm_details = (alarm_info_xml.findall('.//alarm-detail'))

    alarms = []
    for alarm_detail in alarm_details:
        alarm = {}
        for child in alarm_detail.getchildren():
            key = child.tag
            matched = re.search(r'^alarm-(\S+)$', key)
            if matched:
                ele = alarm_detail.find(".//%s" % key)
                alarm[matched.group(1)] = __chop(device, ele.text)
        if 'time' in alarm.keys():
            alarm['time'].strip().rstrip()
        alarms.append(alarm)
    if alarm_count != len(alarm_details):
        device.log(
            message="%s: Incorrect active alarms count(%s)" % (sub,
                                                               alarm_count),
            level='error')
        show_data(device, alarm_details, "%s: alarm_detail" % sub)
    show_data(device, alarms, "%s return:" % sub)
    return alarms
# end def __get_alarm_info


def __get_pic_info(device, fpc_info_xml):
    """
        Get list of detailed pic status

    :param device:
        **REQUIRED** Device handle
    :param fpc_info_xml
        REQUIRED fpc info in xml format

    :return pic_status
        list of detailed pic status
        E.g.
        pic_status = [['Online', 'Online', 'Online', 'Online'],
                       None, None, None,
                       ['Online', 'Online', 'Online', 'Online'],
                       None, None, None, None, None, None,
                       ['Online', 'Online', 'Offline', 'Offline']]
    """
    sub = function_name(device)
    device.log(message="Inside %s" % sub, level='debug')
    pic_status = []
    fpc_info = fpc_info_xml.findall('.//fpc')
    for fpc in fpc_info:
        keys = []
        fpc_slot = None
        for child in fpc.getchildren():
            key = child.tag
            if key == 'slot':
                ele = fpc.find(key)
                fpc_slot = __chop(device, ele.text)
                fpc_slot = int(fpc_slot)
                pic_status = pic_status + (
                    [None] * (fpc_slot + 1 - len(pic_status)))
                pic_status[fpc_slot] = []
            keys.append(key)
        if fpc_slot is None:
            device.log(message="%s: no fpc-slot" % sub,
                       level='INFO')
            continue
        if 'pic' not in keys:
            device.log(message="%s: no pic on fpc(slot %s)" % (sub, fpc_slot),
                       level='INFO')
            continue
        pic_info = fpc.findall('.//pic')
        for pic in pic_info:
            ele = pic.find(".//pic-slot")
            if ele is not None:
                pic_slot = __chop(device, ele.text)
                pic_slot = int(pic_slot)
                pic_status[fpc_slot] = pic_status[fpc_slot] + (
                    [None] * (pic_slot + 1 - len(pic_status[fpc_slot])))
                ele = pic.find(".//pic-state")
                if ele is not None:
                    status = ele.text
                    pic_status[fpc_slot][pic_slot] = status
                    show_data(device, pic,
                              "%s: fpc-slot(%s),pic_slot(%s)\n"
                              % (status, fpc_slot, pic_slot))
    return pic_status
# end def __get_pic_info


def __get_cid(device, string):
    """
    Get cid from string input

    :param device:
        **REQUIRED** Device handle
    :param cid:
        REQUIRED string input

    :return cid value
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    check = re.search(r'^(\D+)(\d+)-re\d+$', string)

    if check:
        if check.group(1) == 'lcc':
            cid = "lcc" + check.group(2)
        elif check.group(1) == 'psd':
            cid = "psd" + check.group(2)
        elif check.group(1) == 'rsd':
            cid = "rsd"
        elif check.group(1) == 'sfc':
            cid = "sfc" + check.group(2)
        else:
            cid = "scc"
    else:
        cid = "scc"
    return cid
# end def __get_cid


def __get_psd(device):
    """
    Get psd form get_chas_hardware() function

    :param device:
        **REQUIRED** Device handle

    :return psd string/False
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    chas_hardware = get_chassis_hardware(device)

    for i in chas_hardware.keys():
        check = re.match(r'^psd(\d+)$', i)
        if check:
            return i

    return False
# end def __get_psd


def __check_dynamic_db(device, slot, dynamic_db, fru_status):
    """
        Check dynamic database

    :param device:
        **REQUIRED** Device handle
    :param slot:
        REQUIRED slot id, integer
    :param dynamic_db
        REQUIRED dynamic database
        E.g.
            dynamic_db [[{'state': 'Online'}, {'state': 'Online'},
                         {'state': 'Online'}],
                        [{'state': 'Offline'}, {'state': 'Offline'},
                         {'state': 'Offline'}]]
    :param fru_status:
        REQUIRED fru status
        E.g.
            dynamic_db [[{'state': 'Online'}, {'state': 'Online'},
                         {'state': 'Online'}],
                        [{'state': 'Offline'}, {'state': 'Offline'},
                         {'state': 'Offline'}]]

    :return :
        TRUE if check dynamic database successful
        FALSE if check dynamic database unsuccessful
    """
    sub = function_name(device)
    device.log(message="Inside %s, slot(%s)" % (sub, slot), level='debug')

    show_data(device, dynamic_db, "%s: dynamic_db" % sub)
    show_data(device, fru_status, "%s: fru_status" % sub)

    chk_state = r'^(Empty|Offline|Present)$'
    if dynamic_db and slot < len(dynamic_db):
        device.log(message="%s: dynamic database has an entry for slot (%s)"
                   % (sub, slot), level='info')
        db_slot = dynamic_db[slot]
        if not fru_status or slot >= (len(fru_status)):
            device.log(message="%s: fru status NOT exists for slot(%s)"
                       % (sub, slot), level='warn')
            return False
        status_slot = fru_status[slot]

        if isinstance(db_slot, list):
            if not isinstance(status_slot, list):
                device.log(
                    message="%s: status NOT list, slot(%s)" % (sub, slot),
                    level='warn')
                show_data(device,
                          status_slot, "%s: fru status, slot(%s)" % (sub,
                                                                     slot))
                return False
            if len(db_slot) > len(status_slot):
                show_data(
                    device,
                    db_slot, "%s: db_slot=" % sub + str(len(db_slot)))
                show_data(
                    device,
                    status_slot, "%s: status_slot=" % sub + str(
                        len(status_slot)))
                device.log(
                    message="%s: db has more entries then status, slot(%s)"
                    % (sub, slot),
                    level='warn')
                return False

            chk_pass = True
            for i in range(0, len(status_slot)):
                device.log(message="%s: checking pic slot(%s, %d) ..."
                           % (sub, slot, i), level='info')
                if not __check_dynamic_db(device, i, db_slot, status_slot):
                    chk_pass = False
                    break
            return chk_pass

        show_data(device, status_slot, "%s: status_slot(%s)" % (sub, slot))
        if re.search(chk_state, status_slot['state']):
            device.log(
                message="%s: checking failed for slot(%s)" % (sub, slot),
                level='warn')
            return False
        else:
            device.log(
                message="%s: checking passed for slot(%s)" % (sub, slot),
                level='info')
    else:
        device.log(
            message="%s: dynamic database does not have an entry for slot (%s)"
            % (sub, slot), level='warn')
        show_data(device, fru_status, "%s: fru_status(%s)" % (sub, slot))
        if not fru_status or slot > (len(fru_status)-1) or (
                isinstance(fru_status[slot], dict) and (
                    fru_status[slot]['state'] and re.search(
                        chk_state, fru_status[slot]['state']) or (
                            fru_status[slot]['comment'] and re.search(
                                r"Not Supported",
                                fru_status[slot]['comment'])))):
            device.log(
                message="%s: checking passed for slot(%s)" % (sub, slot),
                level='info')
        else:
            device.log(
                message="%s: checking failed for slot(%s)" % (sub, slot),
                level='warn')
            return False
    return True
# end def __check_dynamic_db


def __convert_db_name(device, db_name, model):
    """
        Convert database name

    :param device:
        **REQUIRED** Device handle
    :param db_name
        REQUIRED Current Database name
    :param model
        REQUIRED Model of router

    :return db_name
        New database name
    """
    sub = function_name(device)
    device.log(
        message="Inside %s db_name($db_name), model(%s) ..." % (sub, db_name),
        level='debug')
    if db_name == 'cbd':
        if re.search(r'^(m160|m40e)$', model):
            db_name = 'mcs'
        else:
            db_name = 'cb'
    elif db_name == 'cg':
        if re.search(r'^(m160|m40e)$', model):
            db_name = 'pcg'
        else:
            db_name = 'scg'
    device.log(message="%s: return name(%s)" % (sub, db_name), level='debug')
    return db_name
# end def __convert_db_name


def __get_uptime(device, uptime):
    """
    Get uptime of device

    :param device:
        **REQUIRED** Device handle
    :param uptime
        REQUIRED a string contain time

    :return times
        time in seconds
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    times = 0
    check_h = re.search(r'(\d+) hours', uptime)
    check_m = re.search(r'(\d+) minutes', uptime)
    check_s = re.search(r'(\d+) seconds', uptime)
    if check_h:
        times += 3600 * int(check_h.group(1))
    if check_m:
        times += 60 * int(check_m.group(1))
    if check_s:
        times += int(check_s.group(1))
    return times
# end def __get_uptime


def get_fpc_pic_spucp(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fpc Pic Spucp  device=${device_object}  node_id='1'

    Get SPU CP information for every fpcs of chassis device
    with cmn show chassis fpc pic-status

    :param device:
        **REQUIRED** Device handle
    :param node_id
    REQUIRED node id information
    :param type
    OPTIONAL type information as SPU CP
    :param state
    OPTIONAL state information of pic slot

    :return spc_slots
    A list of SPU CP information of pic slot
    """
    valid_keys = ['node_id', 'type', 'state']
    required_key = []
    args = check_args(device, valid_keys, required_key, kwargs)
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    _type = kwargs.get('type', 'SPU Cp')
    state = kwargs.get('state', None)
    node_id = kwargs.get('node_id')
    spc_slots = []
    cli_cmd = "show chassis fpc pic-status"
    if node_id:
        cli_cmd = cli_cmd + " node " + args['node_id']

    rpc_str = device.get_rpc_equivalent(command=cli_cmd)

    res = device.execute_rpc(command=rpc_str).response()

    if res.find('.//multi-routing-engine-item'):
        if node_id:
            topref = res.findall(
                './/multi-routing-engine-item/fpc-information/fpc')
        else:
            ref = res.findall('.//multi-routing-engine-item')
            topref = ref[0].findall('.//fpc-information/fpc')

    else:
        topref = res.findall('.//fpc')

    for fpc in topref:
        for pic in fpc.getchildren():
            key = pic.tag
            if key == 'pic':
                if state:
                    pic_state = pic.find('.//pic-state').text
                    if state.lower() in pic_state.lower():
                        value = "FPC" + fpc.find('.//slot').text
                        spc_slots.append(value)
                else:
                    pic_type = pic.find('.//pic-type').text
                    if _type.lower() in pic_type.lower():
                        value = "FPC" + fpc.find('.//slot').text + \
                            " PIC" + pic.find('.//pic-slot').text
                        spc_slots.append(value)

    if len(spc_slots) != 0:
        if state:
            msg = "the online FPC PICs"
        else:
            msg = "the SPC slots for SPU CP"
        device.log(message="In %s %s are %s" % (sub, msg, spc_slots),
                   level='info')
        return spc_slots
    else:
        device.log(message="In %s No spc slots found" % sub, level='warn')
        return False
# end def get_fpc_pic_spucp


def get_fpc_pic_spuflow(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fpc Pic Spuflow  device=${device_object}  node_id='1'

    Get SPU flow information for every fpcs of chassis device
    with cmn show chassis fpc pic-status

    :param device:
        **REQUIRED** Device handle
    :param node_id
    REQUIRED node id information

    :return spc_slots
    A list of SPU flow information of pic slot
    """
    valid_keys = ['node_id']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')
    node_id = kwargs.get('node_id')
    spc_slots = []
    cli_cmd = "show chassis fpc pic-status"
    if node_id:
        cli_cmd = "%s node %s" % (cli_cmd, node_id)

    rpc_str = device.get_rpc_equivalent(command=cli_cmd)
    response = device.execute_rpc(command=rpc_str).response()
    if response.find('.//fpc') is not None:
        topref = response.findall('.//fpc')
        for fpc in topref:
            for pic in fpc.getchildren():
                if pic.tag == 'pic':
                    pic_type = fpc.find('.//pic-type').text
                    if re.search(r'Flow', pic_type):
                        value = 'FPC' + fpc.find('.//slot').text + ' PIC' + \
                            pic.find('.//pic-slot').text
                        spc_slots.append(value)

    if not spc_slots:
        device.log(message="In %s the Flow slots are %s" % (sub, spc_slots),
                   level='info')
    else:
        device.log(message="In %s No Flow slots found" % sub, level='warning')
    return spc_slots
# end def get_fpc_pic_spuflow


def get_fpc_pic_npc(device):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Fpc Pic Npc  device=${device_object}

    Get pic slot for every fpcs of chassis device
    with cmn show chassis fpc pic-status

    :param device:
        **REQUIRED** Device handle

    :return spc_slots
    A list of npc information of pic slot
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')

    cli_cmd = "show chassis fpc pic-status"
    rpc_str = device.get_rpc_equivalent(command=cli_cmd)
    res = device.execute_rpc(command=rpc_str).response()
    model = device.get_model().lower()
    model_list = "a1|a2|a10|a15|a20|a40|srx1400|srx5600|srx5400|" + \
        "srx5800|srx3400|srx3600"
    if model in model_list:
        ref = res.findall(".//multi-routing-engine-item")
        topref = ref[0].findall(".//fpc-information/fpc")
    else:
        topref = res.findall('.//fpc')
    spc_slots = []
    for fpc in topref:
        for pic in fpc.getchildren():
            key = pic.tag
            if key == 'pic':
                pic_type = fpc.find('.//pic-type').text
                if re.search(r'NPC PIC', pic_type):
                    value = 'FPC' + fpc.find('.//slot').text + ' PIC' + \
                        pic.find('.//pic-slot').text
                    spc_slots.append(value)

    if len(spc_slots) != 0:
        device.log(message="In %s the NPC slots are %s" % (sub, spc_slots),
                   level='info')
        return spc_slots
    else:
        device.log(message="In %s No NPC slots found" % sub, level='warn')
        return False
# end def get_fpc_pic_npc


def check_enhance_fantray(device, **kwargs):
    """
    Robot Usage Example :
     ${dh} =    Get Handle   resource=r1
     ${ft} = Create List  'fan tray 0'  'fan tray 1'
     ${kwargs} =    Evaluate    {'ft':${ft}}
     ${result} =    Check Enhance Fantray    device=${dh}    &{kwargs}

    Check fantray is an enhance fantray

    :param device:
        **REQUIRED** Device handle
    :param ft:
        OPTION list fantray

    Eg: check_enhance_fantray(ft=['fan tray 0', 'fan tray 1'])
    or check_enhance_fantray()

    :return :
        TRUE if the fantray is an enhance fantray
        FALSE if the fantray is not an enhance fantray
    """
    valid_keys = ['ft']
    required_key = []
    kwargs = check_args(device, valid_keys, required_key, kwargs)
    fts = kwargs.get('ft')

    if fts:
        if not isinstance(fts, list):
            fts = [fts]

    model = device.get_model()
    sub = function_name(device) + ' ' + model
    device.log(message="Inside %s ..." % sub, level='debug')

    if not re.search(r'^mx960$', model, re.IGNORECASE):
        device.log(message="Enhance fantray only support on MX960",
                   level='warning')
        return False

    try:
        response = device.cli(command="show chassis hardware models",
                              format='text').response()
    except Exception:
        device.log(message="cannot show chassis hardware", level='error')
        return False

    if not fts:
        if re.search(r'ENH-FANTRAY', response, re.IGNORECASE):
            return True
    else:
        count = 0
        rsl = response.splitlines()
        for line in rsl:
            for _ft in fts:
                if re.search(_ft, line, re.IGNORECASE) and \
                            re.search(r'ENH-FANTRAY', line, re.IGNORECASE):
                    count += 1
        if len(fts) == count:
            return True

    device.log(message="enhance fantray is not found", level='warning')
    return False
# end def check_enhance_fantray


def get_ms_pics_info(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  Get Ms Pics Info  device=${device_object}  status='Virtual'

    Get description for pics from hardware information of chassis

    :param device:
        **REQUIRED** Device handle
    :param status
    REQUIRED information of pic in description

    :return ms_pics_info
    A dictionary contains information of pics
    """
    sub = function_name(device)
    device.log(message="Inside %s function" % sub, level='debug')

    valid_keys = ['status']
    required_key = []
    args = check_args(device, valid_keys, required_key, kwargs)

    status = args.get('status', 'MS-MPC|MS-MIC')
    chas_hardware = get_chassis_hardware(device)
    ms_pics_info = {}

    for fpc in chas_hardware.keys():
        check_fpc = re.search(r'fpc\s(\d+)', fpc)
        if check_fpc:
            fpc_numer = check_fpc.group(1)
            ms_pics_info[fpc_numer] = []
            for fpc_key in chas_hardware[fpc].keys():
                check_name = re.search(r'(\D+)\s(\d+)', fpc_key)
                if check_name and check_name.group(1).lower() == 'mic':
                    for mic in chas_hardware[fpc][fpc_key].keys():
                        check_slot = re.search(
                            r'pic\s(\d+)', mic, re.IGNORECASE)
                        if check_slot:
                            pic_slot = check_slot.group(1)
                            descr = chas_hardware[fpc][
                                fpc_key][mic]['description']
                            if status in descr:
                                ms_pics_info[fpc_numer].append(
                                    int(pic_slot))

                elif check_name and check_name.group(1).lower() == 'pic':
                    pic_slot = check_name.group(2)
                    descr = chas_hardware[fpc][fpc_key]['description']
                    if status in descr:
                        ms_pics_info[fpc_numer].append(int(pic_slot))

    if len(ms_pics_info) > 0:
        device.log(message="MS-MIC/MS-MPC PIC'S Found", level='info')
        device.log(message=pprint(ms_pics_info), level='info')
        return ms_pics_info
    else:
        device.log(message=" No MS-MIC/MS-MPC PIC'S", level='info')
        return False
# end def get_ms_pics_info


#########################################################
#########################################################

def function_name(device):
    """
        To get the fucntion name.

    :param device:
        **REQUIRED** Device handle

    :returns:
        The function name
    """
    device.log(message="Getting function name ...", level='debug')
    return traceback.extract_stack(None, 2)[0][2]
# end function_name


def check_args(device, valid_key, required_key, kw_dict):
    """
    Robot Usage:
    Example:
    ${device_object}  =  Get Handle  resource=r1
    ${valid_key}   =  Create List   name family term match action method if_specific commit
    ${required_key}  =  Create List  name term
    ${kw_dict}      =  Create Dictionary  name=Juniper  term=jnpr
    ...    action=nothing
    ${all_argument_dict}  =  Check Args  device=${device_object}
    ...    valid_key=${valid_key}  required_key=${required_key}
    ...    kw_dict=${kw_dict}

        -Check all value in valid_key list is existed in kw_dict
        -Check all value in requred_key list is existed
        in kw_dict and it is defined

    :param device:
        **REQUIRED** Device handle
    :param valid_key:
        **REQUIRED** the list of valid keys need to be checked (list)
    :param required_key:
        **REQUIRED** the list of required keys need to be checked (list)
    :param kw_dict:
        **REQUIRED** all arguments need to be checked  (dict)

    :return:
        kw_dict: all arguments
        Eg:
            valid_keys = ['name', 'family', 'term', 'match','action',
            'method', 'if_specific', 'commit']
            required_key = ['name', 'term']
            kwargs = check_args(device, valid_keys, required_key, kwargs)
    """
    # Check valid_value in kwargs
    for current_key in kw_dict.keys():
        if current_key not in valid_key:
            device.log(message="%s value is not valid" % current_key,
                       level='error')
            raise Exception("%s value is not valid" % current_key)
    # Check all value in required_key list is existed
    for required_k in required_key:
        if required_k not in valid_key or kw_dict[required_k] == '':
            device.log(message="%s value is not defined" % required_k,
                       level='error')
            raise Exception("%s value is not defined" % required_k)
    return kw_dict
# end def check_args


def kill_process(device, **kwargs):
    """
    Robot Usage Example :
    ${device_object} =  Get Handle  resource=r1
    ${result} =  kill Process  device=${device_object}

    This function is used to kill the process

    :param device:
        **REQUIRED** Device handle

    :return:
        returns True on success else False
    """
    sub = function_name(device)
    valid_keys = ["signal", "pid", "prog", "ps_options", "no_proc_ok"]
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    device.log(message="In %s" % sub, level="debug")
    pid = kwargs.get("pid", '')
    prog = kwargs.get("prog", '')
    signal = kwargs.get("signal", '9')
    ps_options = kwargs.get("ps_options", "-x")
    progs = None

    if not isinstance(pid, list):
        pid = [pid]
    if prog and not isinstance(prog, list):
        progs = [prog]
    signal = re.sub("-", "", signal)
    signal = re.sub(r"\s+", "", signal)
    if progs:
        progs_val = ""
        for prog_val in progs:
            progs_val += prog_val
        progs_val = "\"" + progs_val + "\""
        progs_val = re.sub(r'\s+', '|', progs_val)
        matched1 = re.search(r'sol|sun', progs_val, re.I)
        if matched1:
            ps_cmd = '/usr/ucb/ps'
        else:
            ps_cmd = 'ps'
        try:
            response = device.shell(
                command="%s %s | grep -w %s | grep -v grep" % (ps_cmd,
                                                               ps_options,
                                                               progs_val)).response()
        except Exception:
            raise Exception("%s: ps command failed" % sub)
        pids_val = re.findall(r'^\s{0,4}\d+', response)
        if pids_val:
            try:
                device.shell(command="kill -%s %s" % (signal, pids_val))
            except Exception:
                raise Exception("%s kill command failed" % sub)
        else:
            matched2 = re.search(r'1|true', kwargs.get("no_proc_ok", 'warn'),
                                 re.I)
            if matched2:
                return True
            device.log(message="%s No process found for %s" % (sub, progs_val),
                       level="warn")
            return False
    else:
        device.log(
            message="%s: No PID or PROG specified; Sending control-C" % sub)
        return device.send_control_char('CTRL_C')
    matched3 = re.search(r'no such|not owner|permission|permitted', response,
                         re.I)
    if matched3:
        device.log(message="%s: kill error(s): %s" % (sub, response))
        return False
    return True
# end def kill_chassis
