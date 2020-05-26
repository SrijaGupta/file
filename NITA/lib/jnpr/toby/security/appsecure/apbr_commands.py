#!/usr/bin/python3
"""
Advance policy based routing(APBR) Operational commands
"""
import re



def get_apbr_profile(device=None, node="local"):
    """
    To get the Apbr profile in a dictionary. If no profile configured, returns an empty dictionary.
    Example :-
        get_apbr_profile(device=dh)

    Robot Example :-
        get apbr profile  device=${dh}  node=node0

    :param Device device:
        **REQUIRED** Device handle of the DUT.
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns a dictionary (key->profile name, value->zone name)
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    cmd = 'show security advance-policy-based-routing profile'
    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['apbr-profiles']['apbr-profiles']

    dict_to_return = {}

    # If no profile configured, returns empty dictionary
    if 'profile-name' not in status.keys():
        device.log(level="INFO", message="No profile configured")

    # if only 1 profile configured
    elif not isinstance(status['profile-name'], list):
        dict_to_return[status['profile-name']] = status['zone-name']

    # if multiple profiles configured
    else:
        for profile_name, zone_name in zip(status['profile-name'], status['zone-name']):
            dict_to_return[profile_name] = zone_name

    return dict_to_return


def verify_apbr_profile(device=None, profile_name=None, zone_name=None, node="local",
                        no_profile=False, profile_dict=None):
    """
    To verify APBR profile.
    Example:
        verify_apbr_profile(device=dh, profile_name="prof1", zone_name="trust")

    ROBOT Example:
        Verify Apbr Profile   device=${dh}   profile_name=prof1   zone_name=trust

    :param Device device:
        **REQUIRED** Device handle of the DUT
    :param str profile_name:
        **REQUIRED** Name of the profile which is expected. It is mandatory argument,
        unless no_prfile=True
    :param str zone_name:
        *OPTIONAL* Name of the zone expected.
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :param bool no_profile:
        *OPTIONAL* Pass True if No profile is expected to be in output
    :param dict profile_dict:
        *OPTIONAL* dictionary which get_apbr_profile() returns
    :return: Boolean
    :rtype: bool
    """
    if device is None:
        raise Exception("'device' is a mandatory argument")

    if profile_name is None and no_profile is False:
        device.log(level="ERROR", message="'profile_name' is a mandatory argument if "
                                          "'no_profile' is False")
        raise Exception("'profile_name' is a mandatory argument")

    status = {}
    if profile_dict is None:
        status = get_apbr_profile(device=device, node=node)
    else:
        status = profile_dict

    if not status:
        if no_profile is True:
            device.log(level="INFO", message="As expected, No profile configured")
            return True
        device.log(level="ERROR", message="No profiles configured")
        raise Exception("No profiles configured")

    if no_profile is True:
        device.log(level="ERROR", message="Expected-NO profile, but some profile was found")
        raise Exception("Expected-NO profile, but some profile was found")

    for prof_name in status:
        if prof_name == profile_name:
            device.log(level="INFO", message="Profile name found")
            if zone_name is not None:
                if status[prof_name] != zone_name:
                    device.log(level="ERROR", message="Zone name NOT matching")
                    raise Exception("Zone name NOT matching")
                device.log(level="INFO", message="Zone name matched with the profile name")
            return True

    device.log(level="ERROR", message="Profile name not found")
    raise Exception("Profile name not found")


def get_apbr_stats(device=None, node="local"):
    """
    To get the APBR application statistics as dictionary
    Example:
        get_apbr_stats(device=device)

    ROBOT Example:
        get apbr Stats   device=${device}

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns the dictionary for APBR statistics
    :rtype: dict    
    Example returned dictionary:
    
    {
    'apbr-statistics-appid-requested': '0',
    'apbr-statistics-drop-zone-change': '0',
    'apbr-statistics-route-changed-midstream': '0',
    'apbr-statistics-rule-match': '0',
    'apbr-statistics-session-processed': '0'
    }
     
    """
    if device is None:
        raise ValueError("Device handle is a mandatory argument")

    cmd = 'show security advance-policy-based-routing statistics'
    status = device.execute_as_rpc_command(command=cmd, node=node)
    stats = status['apbr-statistics']['apbr-statistics']
    return stats


def verify_apbr_stats(device=None, counter_values=None, node="local"):
    """
    To verify Apbr statistics. (show security advance-policy-based-routing statistics)
    Example:
        verify_apbr_stats(device=dt, counter_values={'apbr-statistics-zone-change':1,
        'apbr-statistics-appid-requested':1}, node="node0")

    ROBOT Example:
        Verify Apbr Stats   device=${dt}    counter_values=${{{'apbr-statistics-zone-change':1,
        'apbr-statistics-appid-requested':1}}}    node=node0


    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param dict counter_values:
        **REQUIRED** Dictionary of counter names (key) and their expected values (value of the key).
        `Supported values of counter names (key)``:  apbr-statistics-session-processed
                                                     apbr-statistics-appid-cache-hits
                                                     apbr-statistics-appid-requested
                                                     apbr-statistics-route-changed-midstream
                                                     apbr-statistics-rule-match
                                                     apbr-statistics-zone-change
                                                     apbr-statistics-route-changed-cache-hits
                                                     apbr-statistics-drop-zone-change
                                                     apbr-statistics-app-rule-hit-cache-hit
                                                     apbr-statistics-url-rule-hit-cache-hit
                                                     apbr-statistics-app-rule-hit-midstream
                                                     apbr-statistics-url-rule-hit-midstream
                                                     apbr-statistics-next-hop-not-found
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: True/False , based on verification status
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")
    if counter_values is None:
        device.log(level="ERROR", message="counter_values is None, it is mandatory argument")
        raise ValueError("counter_values is None, it is mandatory argument")

    version = device.get_version()
    not_supported_counters_lt_18_4 = ["apbr-statistics-app-rule-hit-cache-hit", "apbr-statistics-url-rule-hit-cache-hit", "apbr-statistics-app-rule-hit-midstream", "apbr-statistics-url-rule-hit-midstream"]
    not_supported_counters_gt_18_4 = ["apbr-statistics-appid-cache-hits", "apbr-statistics-appid-requested", "apbr-statistics-rule-match"]
    device.log(level="INFO", message="Version of the device is %s" %(version[:4]))
    counters_in_device = get_apbr_stats(device=device, node=node)

    flag = True
    for counter in counter_values.keys():

        # not_supported_counters_gt_18_4 counters are not supported for the releases 18.4 and above
        if float(version[:4]) >= 18.4 and counter in not_supported_counters_gt_18_4:
            device.log(level="INFO", message=" %s is not supported for the release %s" %(counter, version[:4]))
            continue;
        # not_supported_counters_lt_18_4 counters are not supported for the releases less than 18.4
        elif float(version[:4]) < 18.4 and counter in not_supported_counters_lt_18_4:
            device.log(level="INFO", message=" %s is not supported for the release %s" %(counter, version[:4]))
            continue;

        if counter in counters_in_device:
            if counter_values[counter] == int(counters_in_device[counter]):
                device.log(level="INFO", message="%s has value %s , match successful" % (
                    counter, counters_in_device[counter]))
            else:
                flag = False
                device.log(level="ERROR", message="%s has value %s , match is not successful" % (
                    counter, counters_in_device[counter]))
        else:
            flag = False
            device.log(level="ERROR", message=counter + " counter not found in apbr stats")

    if flag is False:
        device.log(level="ERROR", message="APBR statistics validation failed")
        raise Exception("APBR statistics validation failed")

    device.log(level="INFO", message="APBR statistics validation passed")
    return flag



def clear_apbr_stats(device=None, node="local"):
    """
    Clear apbr stats
    Example :-
        clear_apbr_stats(device=dh)

    ROBOT Example:
        clear apbr stats device=${dh}

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: returns True if successful
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    status = device.cli(command='clear security advance-policy-based-routing statistics',
                        node=node).response()

    if re.match(".*Advance-policy-based-routing statistics clear done.*", status, re.DOTALL):
        device.log(level="INFO", message="APBR stats cleared successfully")
        return True

    device.log(level="ERROR", message="APBR stats couldn't be cleared")
    raise Exception("APBR stats couldn't be cleared")
