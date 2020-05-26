"""
AppID configuration

AUTHOR:  Elango K
VERSION:  1.0
"""

def configure_appid_sig_package(device=None, mode="set", commit=True, **kwargs):
    """
    Configure the appid security package setting
    Example :-
        appid_configure_sig_package(device=dh, url="https://devdb.juniper.net/cgi-bin/index.cgi")
        appid_configure_sig_package(device=dh, secure_download=True, interval="200",
                                        start_time="09-08.12:10", commit=False)
        appid_configure_sig_package(device=dh, mode="delete")

    ROBOT Example:
        Appid Configure Sig Package   device=${dh}   url=https://devdb.juniper.net/index.cgi
        AppID Configure Sig Package   device=${dh}   secure download=${True}
                                       start_time=09-08.12:10  interval=200   commit={False}
        AppID Configure Sig Package   device=${dh}   mode=delete

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str mode:
        *OPTIONAL* Configuration mode
        ``Supported values``: set or delete
        ``Default value``   : set
    :param str url:
        *OPTIONAL* URL of appid custom signature package. Default is to use URL defined in the
        topology file, otherwise configuration ignored
    :param bool secure_download:
        *OPTIONAL* Enabling secure download, configured if it is True
    :param str start_time:
        *OPTIONAL* Automatic signature udpate start time passed in the format MM-DD.HH:MM
    :param str interval:
        *OPTIONAL* Automatic update interval in hours (24...336)
    :param bool commit:
        *OPTIONAL* To commit the configuration.
        ``Supported values``: True or False
        ``Default value``   : True
    :param bool ignore_server_validation:
        *OPTIONAL* Pass True, if want to ignore server validation.
    :return returns True if successful
    :rtype bool
    """
    if device is None:
        raise ValueError("Argument: device is mandatory")

    # Initialize variables
    url = kwargs.get('url', "")
    start_time = kwargs.get('start_time', "")
    interval = kwargs.get('interval', "")
    secure_download = kwargs.get('secure_download', False)
    ignore_server_validation = kwargs.get('ignore_server_validation', False)


    if interval != "" and start_time == "":
        device.log(level="ERROR", message="Start time is mandatory for a automatic update "
                                          "configuration")
        raise Exception("Start time is mandatory for a automatic update configuration")

    # Set configurations as empty values if delete has to be performed.
    if mode == "delete":
        url = ""
        start_time = ""
        interval = ""

    cfg_node = mode + " services application-identification download "
    cmdlist = []
    if url != "" or (url == "" and mode == "delete" and 'url' in kwargs):
        device.log(level="INFO", message="AppID download URL is %s" % url)
        cmdlist.append(cfg_node + "url " + url)
    if secure_download is True:
        cmdlist.append(cfg_node + "secure-download")
    if 'start_time' in kwargs:
        cmdlist.append(cfg_node + "automatic start-time " + start_time)
    if 'interval' in kwargs:
        cmdlist.append(cfg_node + "automatic interval " + interval)
    if ignore_server_validation is True:
        cmdlist.append(cfg_node + "ignore-server-validation")

    # delete complete secuirty-package node if no specific configuration is available
    if mode == "delete" and len(cmdlist) == 0:
        cmdlist = [cfg_node]

    # Configure and commit the configuration
    device.config(command_list=cmdlist)
    if commit is True and len(cmdlist) != 0:
        device.commit()
    return True

def configure_apptrack(device=None, mode="set", commit=True, **kwargs):
    """
    Configure apptrack
    Example :-
        configure_apptrack(device=dh, what="disable")
        configure_apptrack(device=dh, what="first-update")
        configure_apptrack(device=dh, what="first-update-interval", interval="5")
        configure_apptrack(device=dh, what="session-update-interval", interval="10")
    ROBOT Example:
        configure apptrack    device=${dh}    what=disable

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str mode:
        *OPTIONAL* Configuration mode
        ``Supported values``: set or delete
        ``Default value``   : set
    :param str what:
        *OPTIONAL* Configure multiple options of appTrack
            ``Supported values``:
              disable                   Disable Application tracking
              first-update              Generate AppTrack initial message when a session is created
              first-update-interval     Interval when the first update message is sent (minutes)
              session-update-interval   Frequency in which Application tracking update messages
                                        are generated (minutes)
    :param int interval:
        *OPTIONAL* Interval in minutes
                   Mandatory argument when "first-update-interval" or "session-update-interval"
    :param bool commit:
        *OPTIONAL* To commit the configuration.
        ``Supported values``: True or False
        ``Default value``   : True
    :return returns True if successful
    :rtype bool
    """
    if device is None:
        raise ValueError("Argument: device is mandatory")
    if (kwargs.get('what') == "first-update-interval" or kwargs.get('what')
        == "session-update-interval") and kwargs.get('interval') is None:
        device.log(level="ERROR", message="Argument: Interval is mandatory when "
                                               "first-update-interval or session-update-interval "
                                               "is operation")
        raise ValueError("Argument: Interval is mandatory when first-update-interval"
                         " or session-update-interval is operation")

    cfg_node = mode + " security application-tracking "
    cmdlist = []
    if kwargs.get('what') == "disable":
        cmdlist.append(cfg_node + " disable")
    elif kwargs.get('what') == "first-update":
        cmdlist.append(cfg_node + " first-update")
    elif kwargs.get('what') == "first-update-interval":
        cmdlist.append(cfg_node + " first-update-interval " + kwargs.get('interval'))
    elif kwargs.get('what') == "session-update-interval":
        cmdlist.append(cfg_node + " session-update-interval " + kwargs.get('interval'))

    # delete complete secuirty-package node if no specific configuration is available
    if mode == "delete" and len(cmdlist) == 0:
        cmdlist = [cfg_node]

    # Configure and commit the configuration
    device.config(command_list=cmdlist)
    if commit is True and len(cmdlist) != 0:
        device.commit()
    return True

def enable_apptrack_zone(device=None, mode="set", commit=True, zone=None, **kwargs):
    """
    enable apptrack on zone
    Example :-
        enable_apptrack_zone(device=dut, zone="trust")
        enable_apptrack_zone(device=dut, zone="trust", mode="delete")

    ROBOT Example:
        enable apptrack zone    device=dh    zone=trust

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str zone:
        **REQUIRED** Zone to enable AppTrack
    :param str mode:
        *OPTIONAL* Configuration mode
        ``Supported values``: set or delete
        ``Default value``   : set
    :param bool commit:
        *OPTIONAL* To commit the configuration.
        ``Supported values``: True or False
        ``Default value``   : True
    :return returns True if successful
    :rtype bool
    """
    if device is None or zone is None:
        raise ValueError("Argument: device is mandatory")

    cfg_node = mode + " security zones security-zone " + zone + " application-tracking "
    cmdlist = [cfg_node]

    # Configure and commit the configuration
    device.config(command_list=cmdlist)
    if commit is True and len(cmdlist) != 0:
        device.commit()
    return True

def clear_appid_stats_counters(device=None, what=None, **kwargs):
    """
    clear appid services stats or counters
    Example :-
        clear_appid_stats_counters(device=dh, what="all")
        clear_appid_stats_counters(device=dh, what="apptrack")

    ROBOT Example:
        clear appid stats counters    device=dh    what=all

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str mode:
        *OPTIONAL* Configuration mode
        ``Supported values``: set or delete
        ``Default value``   : set
    :param str what:
        **REQUIRED** appid service to clear
            ``Supported values``: apptrack, appfw, appcache, appstats or all
    :param str logical_system:
        *OPTIONAL*  logical_system value
            ``Supported values``: <logical-system-name>, all or root-logical-system
    :param str interval:
        *OPTIONAL*  argument that can be passed to clear interval in appstats
    :param str cumulative:
        *OPTIONAL*  argument that can be passed to clear cumulative in appstats
    :return returns True if successful
    :rtype bool
    """
    # Initialize variables
    node = kwargs.get('node', "local").lower()

    if device is None and what is None:
        raise ValueError("Argument: device and what is mandatory")

    if what == "apptrack":
        device.cli(command='clear security application-tracking counters')

    elif what == "appfw":
        if kwargs.get('logical_system') is not None:
            cmd = 'clear security application-firewall rule-set statistics ' + 'logical-system '\
                  + kwargs.get('logical_system')
            device.cli(command=cmd)
        else:
            device.cli(
                command='clear security application-firewall rule-set statistics')
    elif what == "appcache":
        if kwargs.get('logical_system') is not None:
            cmd = 'clear services application-identification application-system-cache ' \
                  + 'logical-system ' + kwargs.get('logical_system')
            device.cli(command=cmd)
        else:
            device.cli(
                command='clear services application-identification application-system-cache',
                )
    elif what == "appstats":
        if kwargs.get('interval') is not None:
            device.cli(
                command='clear services application-identification statistics interval')
        elif kwargs.get('cumulative') is not None:
            device.cli(
                command='clear services application-identification statistics cumulative'
                )
        else:
            device.cli(
                command='clear services application-identification statistics')
    elif what == "all":
        device.cli(command='clear security application-tracking counters')
        device.cli(command='clear security application-firewall rule-set statistics')
        device.cli(command='clear security application-firewall rule-set statistics '
                           'logical-system all')
        device.cli(command='clear services application-identification application-system-cache')
        device.cli(command='clear services application-identification application-system-cache '
                           'logical-system all')
        device.cli(command='clear services application-identification statistics')
        device.cli(command='clear services application-identification statistics interval')
        device.cli(command='clear services application-identification statistics cumulative')
    return True


def configure_application_firewall(device=None, **kwargs):
    """
    Keyword to configure appfw policy
    Example :-
        configure_application_firewall(device=dut, profile="thyag", rule="1", app="junos:HTTP",
        action="permit")
        configure_application_firewall(device=dut, profile="thyag", rule="1", app="junos:SSH",
        action="deny")
        configure_application_firewall(device=dut, profile="thyag", rule="1",
        appgroup="  junos:web:news", action="deny")

    Robot Example:-
        configure application firewall   device=${dh}    profile=thyag    rule=1    app=junos:HTTP
           action=permit

    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str profile
        **REQUIRED** Name of the appFw profile
    :param str rule
        **REQUIRED** Name of the appFw rule
    :param str app
        **REQUIRED** Name of the appFw application
    :param str appgroup
        **REQUIRED** Name of the appFw application group
    :param str action
        **REQUIRED** Action for the appFW
            ``Supported values``: permit or deny
    :param str default_rule_action
        **REQUIRED** Action for the appFW default rule
            ``Supported values``: permit or deny
            ``Default value``   : permit
    :param bool commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: True or False
            ``Default value``   : True
    :return: Returns "True"
    :rtype: bool
    """
    mode = kwargs.get('mode', "set").lower()
    commit = kwargs.get('commit', True)
    profile = kwargs.get('profile', None)
    rule = kwargs.get('rule', None)
    app = kwargs.get('app', None)
    appgroup = kwargs.get('appgroup', None)
    action = kwargs.get('action', None)
    default_action = kwargs.get('default_rule_action', "permit")

    cmdlist = []

    if device is None:
        raise ValueError("Argument: device is mandatory")
    if (profile is None and rule is None and action is None and mode == "set") and \
            (app is None or appgroup is None):
        device.log(level="ERROR",
                        message="profile, rule, action and app/appgroup is REQUIRED in "
                                "each dictionary value")
        raise ValueError(
            "profile, rule, RI and app/appgroup is REQUIRED in each dictionary value")
    if mode == "delete" and profile is None:
        device.log(level="ERROR",
                   message="To delete whole profile, argument profile is mandatory")
        raise ValueError(
            "To delete whole profile, argument profile is mandatory")

    if appgroup is not None:
        cmdlist.append(mode + " security application-firewall rule-sets " +
                       profile + " rule " + rule +
                       " match dynamic-application-group " + appgroup)
    elif app is not None:
        cmdlist.append(mode + " security application-firewall rule-sets " +
                       profile + " rule " + rule +
                       " match dynamic-application " + app)

    if mode == "delete" and len(cmdlist) == 0:
        cmdlist = [mode + " security application-firewall rule-sets " + profile ]
    elif mode != "delete":
        cmdlist.append(mode + " security application-firewall rule-sets " +
                       profile + " rule " + rule + " then " + action)
        cmdlist.append(mode + " security application-firewall rule-sets " +
                       profile + " default-rule " + default_action)

    # Configure and commit the configuration
    device.config(command_list=cmdlist)
    if commit is True and len(cmdlist) != 0:
        device.commit()
    return True


