"""
Advance policy based routing(APBR) Configuration
"""


def configure_apbr_profile(device=None, profile=None, mode="set", commit=True, **kwargs):
    """
    Configure the Advance policy based routing(APBR) profile

    Example:

        configure_apbr_profile(device=dh, profile="profile1", rulename="rule1",
                            app_list=["junos:HTTP", "junos:FTP", "junos:FACEBOOK-CHAT"],
                            appgroup_list=["junos:web:social-networking:applications", "junos:p2p"],
                            routing_instance="RI1", sla_rule="sla1")
        configure_apbr_profile(device=dh, profile="profile1", mode="delete", commit=False)

    ROBOT Example:

        Configure Apbr Profile   device=${dh}   profile=profile1   rulename=rule1
                app_list=["junos:HTTP", "junos:FTP", "junos:FACEBOOK-CHAT"]
                appgroup_list=["junos:web:social-networking:applications", "junos:p2p"]
                routing_instance=RI1   sla_rule=sla1    
        Configure Apbr Profile   device=${dh}   profile=profile1   mode=delete   commit=${False}

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str profile:
        **REQUIRED** Advance policy based routing(APBR) profile name
    :param str rulename:
        **REQUIRED** Advance policy based routing(APBR) rule name
    :param list app_list:
        **REQUIRED** Dynamic application list should be defined as match condition in APBR rule
    :param list appgroup_list:
        **REQUIRED** Dynamic application group list should be defined as match condition in
        APBR rule
    :param str routing-instance:
        **REQUIRED** Packets are directed to specified routing instance when an APBR rule match
        hit triggered
    :param list sla_rule:
        **OPTIONAL** SLA Rule which is used in AppQoE feature
    :param bool commit:
        *OPTIONAL* To commit the configuration.
        ``Supported values``: "True" or "False"
        ``Default value``   : "True"
    :param str mode:
        *OPTIONAL* Set or Delete mode
        ``Supported values``: "set" or "delete"
        ``Default value``   : "set"
    :return: True if successful
    :rtype bool
    """
    #Initialize variables.
    rulename = kwargs.get('rulename', None)
    app_list = kwargs.get('app_list', [])
    appgroup_list = kwargs.get('appgroup_list', [])
    routing_instance = kwargs.get('routing_instance', None)
    sla_rule = kwargs.get('sla_rule', None)

    if device is None:
        raise ValueError("Device handle is a mandatory argument")

    if profile is None:
        device.log(level="ERROR", message="Profile name is a mandatory argument")
        raise ValueError("Profile name is a mandatory argument")

    if isinstance(app_list, str):
        app_list = [app_list]

    if isinstance(appgroup_list, str):
        appgroup_list = [appgroup_list]

    if mode == "set":
        if rulename is None:
            device.log(level="ERROR", message="Rule name is a mandatory argument")
            raise ValueError("Rule name is a mandatory argument")

        if routing_instance is None:
            device.log(level="ERROR", message="Routing instance is a mandatory argument")
            raise ValueError("Routing instance is a mandatory argument")

        if len(app_list) == 0 and len(appgroup_list) == 0:
            device.log(level="ERROR",
                       message="Application list or applicaiton group list should not be empty")
            raise ValueError("Application list or applicaiton group list should not be empty")

    cmdlist = []
    base_cmd = mode + " security advance-policy-based-routing profile " + profile

    if rulename is not None:
        base_cmd = base_cmd + " rule " + rulename

    if len(app_list) != 0:
        if len(appgroup_list) != 0:
            device.log(level="ERROR",
                       message="Application list and applicaiton group are mutually exclusive")
            raise ValueError("Application list and application group are mutually exclusive")
        for appname in app_list:
            cmdlist.append(base_cmd + ' match dynamic-application ' + appname)

    if len(appgroup_list) != 0:
        for grpname in appgroup_list:
            cmdlist.append(base_cmd + ' match dynamic-application-group ' + grpname)

    if routing_instance is not None:
        cmdlist.append((base_cmd + " then routing-instance " + routing_instance))
    
    if sla_rule is not None:
        cmdlist.append((base_cmd + " then sla-rule " + sla_rule))

    if len(cmdlist) == 0 and mode == "delete":
        cmdlist.append(base_cmd)

    # configure and commit the configuration.
    device.config(command_list=cmdlist)
    if commit is True:
        device.commit()

    return True


def configure_apbr_traceoptions(device=None, mode="set", commit=True, **kwargs):
    """
    Configure the Advance policy based routing tracing options

    Example:

    configure_apbr_traceoptions(device=dh,filename="apbr-userfile", maxfiles="10", size="100",
                                worldreadable=True, flag="compilation", noremotetrace=True)
    configure_apbr_traceoptions(device=dh,mode="delete", filename="apbr-userfile", maxfiles="10",
                                size="100", worldreadable=True, flag="compilation",
                                noremotetrace=True)
    configure_apbr_traceoptions(device=dh,mode="delete")
    configure_apbr_traceoptions(device=dh)

    ROBOT Example:

    Configure Apbr Traceoptions    device=${dh}   filename=apbr-userfile   maxfiles=${10}
                                   size=${10}    worldreadable=${True}    flag=compilation
                                   noremotetrace=${True}
    Configure Apbr Traceoptions    device=${dh}   mode=delete
    Configure Apbr Traceoptions    device=${dh}

    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str filename:
        *OPTIONAL* Name of the apbr traceoptions file to log traces
            ``Default value``   : nsd_apbr
    :param int maxfiles:
        *OPTIONAL* Maximum no of trace files to be created on system
            ``Default value``   : 3
    :param int size:
        *OPTIONAL* Maximum size of the trace file
            ``Default value``   : 128000
    :param bool worldreadable:
        *OPTIONAL* world-readable configuration
            ``Supported values``: True or False
    :param str flag:
        *OPTIONAL* Configure trace flag options
            ``Supported values``: all, compilation, configuration, ipc, lookup
    :param str match:
        *OPTIONAL* Configure trace match options with
                   Regular expression for lines to be logged
    :param bool noremotetrace:
        *OPTIONAL* Disable remote tracing
            ``Supported values``: True or False
    :param bool commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: True or False
            ``Default value``   : True
    :return: Returns "True" if successful
    :rtype: bool
    """
    if device is None:
        raise ValueError("Device handle is a mandatory argument")

    cfg_node = mode + ' security advance-policy-based-routing traceoptions '
    cmdlist = []

    #Initialize variables.
    worldreadable = kwargs.get('worldreadable', None)

    if 'filename' in kwargs:
        cmdlist.append(cfg_node + 'file ' + kwargs.get('filename'))
    if 'maxfiles' in kwargs:
        cmdlist.append(cfg_node + 'file files ' + kwargs.get('maxfiles'))
    if 'size' in kwargs:
        cmdlist.append(cfg_node + 'file size ' + kwargs.get('size'))
    if 'match' in kwargs:
        cmdlist.append(cfg_node + 'file match ' + kwargs.get('match'))
    if 'flag' in kwargs:
        cmdlist.append(cfg_node + 'flag ' + kwargs.get('flag'))
    if 'noremotetrace' in kwargs and kwargs.get('noremotetrace') is True:
        cmdlist.append(cfg_node + 'no-remote-trace')
    if worldreadable is not None:
        if worldreadable is True:
            cmdlist.append(cfg_node + 'file ' + 'world-readable')
        else:
            cmdlist.append(cfg_node + 'file ' + 'no-world-readable')

    if len(cmdlist) == 0 and mode == "delete":
        cmdlist = [cfg_node]
    elif len(cmdlist) == 0 and mode == "set":
        cmdlist.append(cfg_node + 'file nsd_apbr')

    # configure and commit the configuration.
    device.config(command_list=cmdlist)
    if commit is True:
        device.commit()

    return True

def enable_apbr_zone(device=None, mode="set", commit=True, zone=None, profile=None):
    """
    enable apbr on zone
    Example :-
        enable_apbr_zone(device=dut, zone="trust" profile="p1")
        enable_apbr_zone(device=dut, zone="trust", profile="p1", mode="delete")

    ROBOT Example:
        enable apbr zone    device=dh    zone=trust profile p1

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str zone:
        **REQUIRED** Zone to enable Apbr
    :param str profile:
        **REQUIRED** Profile name of Apbr
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

    if device is None:
        raise ValueError("Device handle is a mandatory argument")

    if zone is None:
        device.log(level="ERROR", message="Zone is a mandatory argument")
        raise ValueError("Zone is a mandatory argument")

    if profile is None:
        device.log(level="ERROR", message="Profile is a mandatory argument")
        raise ValueError("Profile is a mandatory argument")

    cmdlist = []
    cfg_node = mode + " security zones security-zone " + zone + \
        " advance-policy-based-routing-profile " + profile

    cmdlist.append(cfg_node)
    # configure and commit the configuration.
    device.config(command_list=cmdlist)
    if commit is True:
        device.commit()

    return True


def config_apbr_tunables(device=None, max_route_change=None, drop_on_zone_change=False,
                         enable_logging=False, mode="set", commit=True):
    """
    To configure APBR Tunables (set security advance-policy-based-routing tunable)
    Example:
        config_apbr_tunables(device=dh, max_route_change=2, commit=False)

    ROBOT Example:
        Config APBR Tunables   device=${dh}   max_route_change=${2}   commit=${False}

    :param Device device:
        **REQUIRED** Device handle of the DUT
    :param int max_route_change:
        *OPTIONAL* Max no. of allowed Route changes.
    :param bool drop_on_zone_change:
        *OPTIONAL* Pass True if you want to enable "drop on zone change", else pass False. By
        default it is True.
    :param bool enable_logging:
        *OPTIONAL* Pass True if you want to enable "logging", else pass False. By default
        it is True.
    :param str mode:
        *OPTIONAL* Set or Delete mode
        ``Supported values``: "set" or "delete"
        ``Default value``   : "set"
    :param bool commit:
        *OPTIONAL* To commit the configuration once configured, pass True. Else, pass False.
        By default is is True.
    :return: returns True if successful
    :rtype: bool
    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    cmdlist = []
    base_cmd = mode + " security advance-policy-based-routing tunables"
    if max_route_change is not None:
        if mode == "set":
            cmdlist.append(base_cmd + " max-route-change " + str(max_route_change))
        else:
            cmdlist.append(base_cmd + " max-route-change ")

    if drop_on_zone_change is True:
        cmdlist.append(base_cmd + " drop-on-zone-mismatch")

    if enable_logging is True:
        cmdlist.append(base_cmd + " enable-logging")

    if len(cmdlist) == 0 and mode == "delete":
        cmdlist.append(base_cmd)

    if len(cmdlist) !=0:    
        device.config(command_list=cmdlist)
        if commit is True:
            device.commit()

    return True
