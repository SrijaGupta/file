import codecs
import ipaddress
import json
import os
import re
import time

import jnpr.toby.security.aamw.util.helper_util as helper
from jnpr.toby.utils.xml_tool import xml_tool


def get_vty_web_xlist_cnt(srx_handle):
    """
    Get VTY aamw web xlist counter
    :param srx_handle: SRX handle
    :return: result dict
    """
    result = {
        'http': {
            'blacklist': 0,
            'whitelist': 0,
        },
        'https': {
            'blacklist': 0,
            'whitelist': 0,
        }
    }

    # get data
    cmd = '%s "plugin jsf_aamw show counters session"' % \
          helper.get_vty_cmd_prefix(srx_handle)
    data = srx_handle.shell(command=cmd).response().split('\n')

    # counting
    def search_num(input_str):
        """
        Search for num in input_str
        :param input_str: input string
        :return: Number found
        """
        res = re.search('([0-9]+)', input_str)
        assert res, 'Not finding numeric value in result: %s' % input_str
        return int(res.group(1))

    found = False
    for i, value in enumerate(data):
        if 'HTTP:' in value:
            found = True
            for protocol_key, list_key, loc in \
                    [('http', 'blacklist', i + 1),
                     ('http', 'whitelist', i + 2),
                     ('https', 'blacklist', i + 4),
                     ('https', 'whitelist', i + 5)]:
                result[protocol_key][list_key] += search_num(data[loc])
    if not found:
        raise ValueError('Not finding web protocol blwl values')

    srx_handle.log('VTY web protocol counting result: %s' % result)
    return result


def get_vty_category_cnt(srx_handle):
    """
    Get VTY aamw category counter
    :param srx_handle: SRX handle
    :return: result dict
    """
    result = {
        'category': {},
        'hash': {}
    }

    # get data
    cmd = '%s "plugin jsf_aamw show counters file_category"' % \
          helper.get_vty_cmd_prefix(srx_handle)
    data = srx_handle.shell(command=cmd).response().split('\n')

    # counting
    cnt_flag = 'category'
    cat_list = []
    for string in data:
        if any(['----' in string, '====' in string, not string.strip(),
                'Syntax error' in string, 'Possible choices' in string,
                'No subtree' in string]):
            pass
        elif 'File category counters' in string:
            cnt_flag = 'category'
            cat_list = []
        elif 'File Hash counters' in string:
            cnt_flag = 'hash'
            cat_list = []
        elif 'Category' in string:
            cat_list = list(
                map(lambda x: x.replace(' ', '_').replace('-', '_').lower(),
                    re.findall('([a-zA-Z\-_]+ ?[a-zA-Z\-_]+)', string)[1:]))
        elif ':' in string:
            key, val = string.split(':')
            key = key.strip().replace(' ', '_').replace('-', '_').lower()
            val = int(val.strip())
            result[cnt_flag][key] = val + result[cnt_flag].get(key, 0)
        else:
            cat_name, cat_cnt = string.split()[0].lower(), \
                                [int(x) for x in string.split()[1:]]
            assert len(cat_cnt) == len(cat_list), \
                'Mismatched length for category action list and counter ' \
                'list: %s and %s' % (len(cat_list), len(cat_cnt))
            result[cnt_flag].setdefault(cat_name, dict())
            for cat_act, cat_act_val in zip(cat_list, cat_cnt):
                result[cnt_flag][cat_name][cat_act] = \
                    cat_act_val + result[cnt_flag][cat_name].get(cat_act, 0)

    srx_handle.log('VTY category counter result: %s' % result)
    return result


def get_vty_application_cnt(srx_handle):
    """
    Get VTY aamw application counter
    :param srx_handle: SRX handle
    :return: result dict
    """
    result = {}
    # get data
    cmd = '%s "plugin jsf_aamw show counters application"' % \
          helper.get_vty_cmd_prefix(srx_handle)
    data = srx_handle.shell(command=cmd).response().split('\n')

    protocol = None

    # counting
    for s in data:
        if any(['----' in s, '====' in s, not s.strip(),
                'Syntax error' in s, 'Possible choices' in s,
                'No subtree' in s]):
            pass
        elif re.match('Application [A-Z]+', s):
            protocol = re.search('Application ([A-Z]+)', s).group(1).lower()
            result.setdefault(protocol, dict())
        elif ':' in s:
            tmp_list = s.split(':')
            cat, val = tmp_list[0].split()[1], int(tmp_list[-1].strip())
            result[protocol][cat] = val + result[protocol].get(cat, 0)

    srx_handle.log('VTY application counter result: %s' % result)
    return result


def get_trace_telemetry_json(srx_handle, trace_file_path, timeout=360):
    """
    Try to extract telemetry JSON from trace file
    :param srx_handle: SRX handle
    :param trace_file_path: Trace file path for aamw trace
    :param timeout: Max time to wait for telemetry
    :return: result dict
    """
    srx_handle.log('Getting telemetry counters')
    retry = 0
    local_file = 'test_aamw_trace_telemetry.log'
    pattern = '[a-zA-Z]{3}\ +[0-9]{1,2}\ +[0-9]{2}\:[0-9]{2}\:[0-9]{2}\ +(.*)'

    end_time = time.time() + timeout
    while time.time() < end_time:
        retry += 1
        srx_handle.log('Retrieving telemetry attempt: %s' % retry)
        try:
            os.remove(local_file)
        except OSError:
            pass
        srx_handle.download(remote_file=trace_file_path, local_file=local_file,
                            user='root', password='Embe1mpls')
        with codecs.open(local_file, mode='r', encoding='utf-8',
                         errors='ignore') as file:
            res, start = '', False
            srx_handle.log(level='DEBUG',
                           message='Start parsing telemetry file')
            for s in file.read().split('\n'):
                if 'telemetry_string' in s:
                    srx_handle.log(level='DEBUG', message='Start parsing')
                    start = True
                    continue
                if start and len(s):
                    tmp = re.search(pattern, s)
                    srx_handle.log(level='DEBUG',
                                   message='Date pattern found successfully '
                                           'in trace line')
                    if tmp:
                        res += tmp.group(1)
                        srx_handle.log(level='DEBUG',
                                       message='String attached to res: %s'
                                       % tmp.group(1))
                if res:
                    srx_handle.log(level='DEBUG', message='res: %s' % res)
                    try:
                        telemetry_cnt = json.loads(res)
                        srx_handle.log('Telemetry Counter: %s' % telemetry_cnt)
                        return telemetry_cnt
                    except Exception:
                        srx_handle.log(
                            level='DEBUG',
                            message='res NOT recognized successfully')
        srx_handle.log('Telemetry counters not found in trace file')
        helper.sleep(30, 'Wait for a while before retry')
    else:
        raise TimeoutError('Fail to fetch telemetry counters within %ss '
                           'timeout' % timeout)


def verify_telemetry_item(srx_handle, trace_file_path, key_list, exp_val,
                          max_retry=5, timeout=360):
    """
    Verify aamw telemetry item matches expectation
    :param srx_handle: SRX handle
    :param trace_file_path: Trace file path for AAMW trace
    :param key_list: Item key list
    :param exp_val: Expected value
    :param max_retry: Maximum retry for verifying
    :param timeout: Time out
    :return: True for pass, otherwise False
    """
    key_str = ''.join('[%s]' % x for x in key_list)
    srx_handle.log('Verifying telemetry data %s is %s' %
                   (key_str, exp_val))
    assert key_list, 'Key list cannot be empty'

    retry = 0
    while retry < max_retry:
        retry += 1
        srx_handle.log('Verification attempt: %s' % retry)
        try:
            res = get_trace_telemetry_json(srx_handle, trace_file_path,
                                           timeout)
        except TimeoutError:
            srx_handle.log(level='WARN',
                           message='Timeout retrieving telemetry data')
        else:
            for key in key_list:
                res = res[key]
            if any([res == exp_val, str(res) == str(exp_val),
                    int(res) >= int(exp_val)]):
                srx_handle.log('Telemetry %s actual value and expected value '
                               'are matching correctly' % key_str)
                return True
            else:
                srx_handle.log('Telemetry %s actual value and '
                               'expected value are not matching correctly: '
                               '%s and %s' % (key_str, res, exp_val))
        srx_handle.cli(command='clear log %s' %
                       os.path.basename(trace_file_path))
    else:
        error_msg = 'Fail to verify telemetry data %s as %s with %s max ' \
                    'retry' % (key_str, exp_val, max_retry)
        srx_handle.log(level='ERROR', message=error_msg)
        raise TimeoutError(error_msg)


def get_ha_dynamic_address(srx_handle, start_ip=None, end_ip=None):
    """
    Get dynamic address items for Infected Hosts
    :param srx_handle: SRX handle
    :param start_ip: start IP
    :param end_ip: end IP
    :return: result list
    """
    srx_handle.log("Checking dynamic address for Infected Host")

    cmd = "show security dynamic-address category-name Infected-Hosts"
    if start_ip is not None:
        cmd += ' ip-start %s' % start_ip
        srx_handle.log("Start IP: %s" % start_ip)
    if end_ip is not None:
        cmd += ' ip-end %s' % end_ip
        srx_handle.log("End IP: %s" % end_ip)

    resp = srx_handle.cli(command=cmd).response()

    res = []
    exp_item_num = 5
    tag_list = ['ip_start', 'ip_end', 'feed', 'address']
    for line in resp.split('\n'):
        tmp_list = line.split()
        if len(tmp_list) == exp_item_num and re.match('\d+', tmp_list[0]):
            res.append({x: y for x, y in zip(tag_list, tmp_list[1:])})
    srx_handle.log('Host analyzer IP list: %s' % res)
    return res


def is_ip_in_db_file(srx_handle, ip):
    """
    Check if ip is in DB file
    :param srx_handle: SRX handle
    :param ip: IP address to check
    :return: True for found, otherwise False
    """
    srx_handle.log("Checking DB file for ip %s" % ip)
    cmd = 'cat /var/db/secinteld/download/Infected-Hosts*'

    # work for both IPv4 and IPv6
    ip_int = int(ipaddress.ip_address(ip))
    srx_handle.su()
    resp = srx_handle.shell(command=cmd).response()
    start = False
    for s in resp.split('\n'):
        if '#add' in s:
            start = True
        if start and str(ip_int) in s:
            srx_handle.log('IP %s found in db file' % ip)
            return True
    srx_handle.log('IP %s not found in db file' % ip)
    return False


def verify_ip_in_ha(srx_handle, ip, timeout=240):
    """
    Verify if IP is found in Infected Hosts
    :param srx_handle: SRX handle
    :param ip: IP to find
    :param timeout: Timeout
    :return: True for found, otherwise False
    """
    retry = 0
    end_time = time.time() + timeout

    in_db_file, in_dynamic_addr = False, False
    while time.time() < end_time:
        retry += 1
        srx_handle.log('Trying to find IP %s in Infected Host with retry: %s'
                       % (ip, retry))
        if not in_db_file and is_ip_in_db_file(srx_handle, ip):
            srx_handle.log('IP %s found in DB file' % ip)
            in_db_file = True
        if not in_dynamic_addr and get_ha_dynamic_address(srx_handle, ip, ip):
            srx_handle.log('IP %s found in dynamic-address' % ip)
            in_dynamic_addr = True
        if in_dynamic_addr and in_db_file:
            srx_handle.log('IP %s found in both dynamic-address and db file'
                           % ip)
            return True
        helper.sleep(30, 'Wait for Host Analyzer update')
    err_msg = 'Error: IP %s not found in both dynamic-address and db ' \
              'file with in %ss timeout.' % (ip, timeout)
    if not in_db_file:
        err_msg += ' Not found in DB file.'
    if not in_dynamic_addr:
        err_msg += ' Not found in dynamic-address.'
    srx_handle.log(level='ERROR', message=err_msg)
    raise TimeoutError(err_msg)


def verify_no_session_in_security_flow(session):
    """
    Verify no session in security flow
    :param session: Session name
    :return: True for no session, otherwise False
    """
    pattern = "Total sessions: ([0-9]+)"
    regex = re.compile(pattern)
    for match in regex.finditer(session):
        if int(match.group(1)) != 0:
            return False

    return True


def verify_argon_profile(srx_handle, profile_name, enabled_expected):
    """
    Verify argon profile
    :param srx_handle: SRX handle
    :param profile_name: profile name
    :param enabled_expected: Dict with expected settings
    :return: True for matched, otherwise False
    """
    response = srx_handle.cli(
        command='show services advanced-anti-malware profile %s' %
                profile_name).response()

    if not response or "Disabled categories" not in response \
            or "Category_thresholds" not in response:
        return False

    categories = response.split("Disabled categories:")[-1]
    enabled = categories.split("Category_thresholds:")[-1]
    enabled_match = True

    for line in enabled.split("\n"):
        if "Category" in line:
            pattern = "Category\s+([a-zA-Z_]+)"
            enabled_match = (re.search(pattern, line).group(1) ==
                             enabled_expected[0]["category"])
        if "min size" in line:
            pattern = "min size:\s+([0-9]+)"
            enabled_match = (int(re.search(pattern, line).group(1)) ==
                             enabled_expected[0]['min_size'])
        if "max size" in line:
            pattern = "max size:\s+([0-9]+)"
            enabled_match = (int(re.search(pattern, line).group(1)) ==
                             enabled_expected[0]['max_size'])

    return enabled_match


def verify_argon_smtp_action(srx_handle, argon_policy, action):
    """
    Verify aamw SMTP action
    :param srx_handle: SRX handle
    :param argon_policy: AAMW policy name
    :param action: Action name
    :return: True for verified, otherwise False
    """
    response = srx_handle.cli(
        command='show services advanced-anti-malware policy %s' %
        argon_policy).response()

    if not response or "Protocol: SMTP" not in response:
        return False

    policy = response.split("Protocol: SMTP")[-1]

    for line in policy.split("\n"):
        if "Action" in line:
            pattern = "Action: User-Defined-in-Cloud \(([a-zA-Z-]+)\)"
            if re.search(pattern, line).group(1) == action:
                return True

    return False


def verify_secintel_feed_download(srx_handle, category, feed,
                                  logical_system=None, tenant=None):
    """
    Verify SecIntel feed downloaded
    :param srx_handle: SRX handle
    :param category: Category name
    :param feed: Feed name
    :param logical_system: LDOM name
    :param tenant: Tenant name
    :return: True for verified, otherwise False
    """
    prefix = 'show services security-intelligence category detail ' \
             'category-name {} feed-name {} count 0 start 0' \
             ''.format(category, feed)
    if logical_system is not None:
        command = prefix + ' logical-system {}'.format(logical_system)
    elif tenant is not None:
        command = prefix + ' tenant {}'.format(tenant)
    else:
        command = prefix
    response = srx_handle.cli(command=command).response()
    srx_handle.log(response)

    if not response or "Update status" not in response:
        return False

    for line in response.split("\n"):
        if "Update status" in line:
            pattern = "Update status\s+:([a-zA-Z ]+)"
            srx_handle.log(re.search(pattern, line))
            if re.search(pattern, line).group(1) == 'Store succeeded':
                return True
    return False


def verify_secintel_stats(srx_handle, profile, action, logical_system=None,
                          tenant=None):
    """
    Verify SecIntel statistics
    :param srx_handle: SRX handle
    :param profile: Profile name
    :param action: Action name
    :param logical_system: Logical system name
    :param tenant: Tenant name
    :return: True for pass, otherwise False
    """
    action_set = {
        'permit',
        'block drop',
        'block close',
        'block close redirect',
        'no action'
    }
    cnt_dict = {
        'Permit sessions': 0,
        'Block drop sessions': 0,
        'Block close sessions': 0,
        'Close redirect sessions': 0
    }
    action = action.lower()
    assert action in action_set, 'Invalid action: {}, valid actions: {}' \
        ''.format(action, action_set)
    prefix = 'show services security-intelligence statistics profile '\
             + profile
    if logical_system is not None:
        command = prefix + ' logical-system ' + logical_system
    elif tenant is not None:
        command = prefix + ' tenant ' + tenant
    else:
        command = prefix
    response = srx_handle.cli(command=command).response()
    srx_handle.log(response)
    response = response.splitlines()
    profile_found = False
    for line in response:
        if not profile_found:
            if 'Profile ' + profile in line:
                profile_found = True
        elif 'Category' in line or 'Profile' in line:
            srx_handle.log('SecIntel counter not found')
            return False
        else:
            for cnt in cnt_dict:
                if cnt in line:
                    cnt_dict[cnt] = int(re.search('(\d+)', line).group(0))
    srx_handle.log(cnt_dict)
    if action == 'permit':
        return cnt_dict['Permit sessions'] > 0
    elif action == 'block drop':
        return cnt_dict['Block drop sessions'] > 0
    elif action == 'block close':
        return cnt_dict['Block close sessions'] > 0
    elif action == 'block close redirect':
        return cnt_dict['Block close sessions'] > 0 and \
               cnt_dict['Close redirect sessions'] > 0
    elif action == 'no action':
        return not any([cnt_dict['Permit sessions'],
                        cnt_dict['Block drop sessions'],
                        cnt_dict['Block close sessions'],
                        cnt_dict['Close redirect sessions']])


def get_syslog(device_handle, syslog_type):
    """
    Get syslog file
    :param device_handle: Device handle
    :param syslog_type: Syslog type
    :return: Syslog response
    """
    device_handle.su()
    return device_handle.shell(
        command='cat /var/log/messages | grep %s' % syslog_type).response()


def verify_da_feed_loaded(srx_handle, category=None, feed_name=None,
                          logical_system=None, tenant=None):
    """
    Verify if feed is loaded into dynamic address
    :param srx_handle: SRX handle
    :param category: Category name
    :param feed_name: Feed name
    :param logical_system: Logical system name
    :param tenant: Tenant name
    :return: True for pass, otherwise False
    """
    command_list = ['show security dynamic-address']
    if category is not None:
        command_list.extend(['category-name', category])
    if feed_name is not None:
        command_list.extend(['feed-name', feed_name])
    if logical_system is not None:
        command_list.extend(['logical-system', logical_system])
    elif tenant is not None:
        command_list.extend(['tenant', tenant])

    command = ' '.join(command_list)
    response = srx_handle.cli(command=command).response()
    srx_handle.log(response)
    response = response.splitlines()

    for line in response:
        if 'Total number of matching entries: 0' in line:
            return False
    return True


def verify_action_syslog(device_handle, prefix='SECINTEL_ACTION_LOG',
                         negative=False, **kwargs):
    """
    Check if items are found in syslog.
    This function is designed to be used on single action log
    :param device_handle: Device handle
    :param prefix: Prefix of syslog. Default value for secintel action log
    :param negative: True if want no items found
    :param kwargs: items dict
    :return: True for pass checking, otherwise False
    """
    output = str(get_syslog(device_handle, prefix))
    device_handle.log('Log found: ' + output)
    if prefix not in output:
        if negative:
            device_handle.log(
                "Action log not found, which is expected.")
            return True
        device_handle.log(
            "Action log not found, which is unexpected.",
            level='error')
        return False

    error = 0
    device_handle.log('Key and value to be found: {}'.format(str(kwargs)))
    for key, val in kwargs.items():
        string_to_find = key.replace('_', '-') + '=' + val
        device_handle.log('Finding: {}...'.format(string_to_find))
        if string_to_find in output:
            device_handle.log(
                'String {} found in syslog.'.format(string_to_find))
        else:
            error += 1
            device_handle.log(
                'String {} NOT found in syslog.'.format(string_to_find),
                level='error')
    if error:
        device_handle.log('Some strings not found in syslog.', level='error')
        return False
    device_handle.log('All strings found in syslog.')
    return True


def verify_secintel_action_syslog(device_handle, negative=False, **kwargs):
    """
    Check if items are found in secintel action syslog.
    This function is for script backward compatibility.
    :param device_handle: Device handle
    :param negative: True if want no items found
    :param kwargs: items dict
    :return: True for pass checking, otherwise False
    """
    # fixme: fix script, using verify_action_syslog instead of this keyword

    return verify_action_syslog(device_handle, prefix='SECINTEL_ACTION_LOG',
                                negative=negative, **kwargs)


def get_secintel_feed_summary_specific(srx_handle, feed_category, feed_name,
                                       status_type='status', device_type='SA', logical_system=None, tenant=None):
    """
    Get SecIntel feed Summary
    :param srx_handle: SRX handle
    :param feed_category: Feed Category name
    :param feed_name: Feed name
    :param logical_system: LDOM name
    :param tenant: Tenant name
    :param status_type: (Default value: status)
           Feed summary field you want this function to return - values should be one of these:
           (status, update-status, name, version, objects, create-time, update-time, expired, options)
    :param device_type: Is it HA or SA Device (Default value: HA)
    :return: Requested value
    """
    prefix = 'show services security-intelligence category summary ' \
             '{}' \
             ''.format(feed_category)
    if logical_system is not None:
        command = prefix + ' logical-system {}'.format(logical_system)
    elif tenant is not None:
        command = prefix + ' tenant {}'.format(tenant)
    else:
        command = prefix
    response = srx_handle.cli(command=command, format="XML", channel="PYEZ").response()
    srx_handle.log(response)

    summary_dict = xml_tool().xml_obj_to_dict(response)
    srx_handle.log(summary_dict)

    dict_location = None
    if device_type is 'HA':
        dict_location = summary_dict["multi-routing-engine-results"]["multi-routing-engine-item"]["secintel-category"][
            "secintel-category-summary"]["secintel-category-summary-feed"]
    elif device_type is 'SA':
        dict_location = summary_dict["secintel-category"]["secintel-category-summary"]["secintel-category-summary-feed"]
    if str(type(dict_location)) == '<class \'jxmlease.dictnode.XMLDictNode\'>':
        return dict_location["secintel-category-summary-feed-" + status_type]
    elif str(type(dict_location)) == '<class \'jxmlease.listnode.XMLListNode\'>':
        for ind in range(len(dict_location)):
            if dict_location[ind]["secintel-category-summary-feed-name"] in feed_name:
                return dict_location[ind]["secintel-category-summary-feed-" + status_type]


def get_aamw_stats(srx_handle, protocol=None, action='interested', device_type='SA', logical_system=None, tenant=None):
    """
    Get SecIntel feed Summary
    :param srx_handle: SRX handle
    :param protocol: What protocol you need counters for: (http,https,smtp,smtps,imap,imaps,total)
    :param action: can be one of the following:
                   blacklist-hit-counter
                   ignored
                   interested
                   whitelist-hit-counter
                   file-fallback-blocked
                   file-fallback-permitted
                   file-ignored_by_sample_rate
                   file-submission-failure
                   file-submission-not-needed
                   file-submission-success
                   file-verdict-meets_threshold
                   file-verdict-under_threshold
                   hash-eligible
                   hash-fail
                   hash-known
                   hash-selected
                   hash-submitted
                   hash-unknown
                   hash-verdict-timeout
                   session-actives
                   session-blocked
                   session-permitted
                   email-blacklist
                   email-blocked
                   email-fallback-blocked
                   email-fallback-permitted
                   email-hit-whitelist
                   email-permitted
                   email-quarantined
                   email-scanned
                   email-tag-and-delivered
    :param device_type: Is it HA or SA Device (Default value: HA)
    :param logical_system: LDOM name
    :param tenant: Tenant name
    :return: counter value
    """
    prefix = 'show services advanced-anti-malware statistics '
    if logical_system is not None:
        command = prefix + ' logical-system {}'.format(logical_system)
    elif tenant is not None:
        command = prefix + ' tenant {}'.format(tenant)
    else:
        command = prefix
    response = srx_handle.cli(command=command, format="XML", channel="PYEZ").response()
    srx_handle.log(response)
    statistics_dict = xml_tool().xml_obj_to_dict(response)
    srx_handle.log(statistics_dict)

    dict_location = None
    if device_type is 'HA':
        dict_location = statistics_dict["multi-routing-engine-results"]["multi-routing-engine-item"][
            "aamw-statistics"]["aamw-statistics"]
    elif device_type is 'SA':
        dict_location = statistics_dict["aamw-statistics"]["aamw-statistics"]
    if protocol is None:
        return dict_location["aamw-statistics" + "-" + action]
    else:
        return dict_location["aamw-statistics-" + protocol + "-" + action]
