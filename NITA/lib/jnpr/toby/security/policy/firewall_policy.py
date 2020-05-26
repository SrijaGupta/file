#! /usr/local/bin/python3

"""
 DESCRIPTION:   To enable or delete services like idp, ssl, utm, app-track etc in firewall policy
     COMPANY:   Juniper Networks
"""

def configure_application_services(device=None, service=None, service_profile=None, **kwargs):
    """
    To enable and delete application service in firewall policy.
    Example:
        configure_application_services(device=device, from_zone="trust", to_zone="untrust",
        service="idp")
        configure_application_services(device=device, from_zone="trust", to_zone="untrust",
        service="ssl", service_profile="sslprofile")
        configure_application_services(device=device, from_zone="trust", to_zone="untrust",
        service="app-firewall", service_profile="xyz")
        configure_application_services(device=device, mode="delete", from_zone="trust",
        to_zone="untrust", service="anti_malware", service_profile="xyz")

    Robot Example:
        configure application services    device=${dut}    fromo_zone=trust   to_zone=untrust
        service=idp
        configure application services    device=${dut}    fromo_zone=trust   to_zone=untrust
        service=utm    service_profile=utmpolicy
        configure application services    device=${dut}    fromo_zone=trust   to_zone=untrust
        service=app-qos    service_profile=abc
        configure application services    device=${dut}    fromo_zone=trust   to_zone=untrust
        service=sec_intel    service_profile=abc

    :param Device device:
        **REQUIRED** Device handle for srx
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str service:
        **REQUIRED** Application service to be enabled in firewall policy.
        ``Supported values``: "idp", "ssl", "utm", "app-firewall", "app-qos", "anti-malware",
                              "security-intelligence"
    :param str service_profile:
        *OPTIONAL* Application service profile to be enabled along with service in firewall policy
    :param str from_zone:
        **REQUIRED** from-zone in firewall policy
    :param str to_zone:
        **REQUIRED** to-zone in firewall policy
    :param str policy_name:
        *OPTIONAL* security policy name in firewall policy
        ``Default Value``: 1
    :return:True on Success
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    mode = kwargs.get('mode', "set")
    from_zone = kwargs.get('from_zone', None)
    to_zone = kwargs.get('to_zone', None)
    policy_name = kwargs.get('policy_name', "1")
    commit = kwargs.get('commit', True)

    if from_zone is None or to_zone is None or service is None:
        device.log(
            level="ERROR",
            message="zones and service are the mandatory arguments")
        raise Exception("zones and service are the mandatory arguments")

    cmdlst = []
    cmd = "%s security policies from-zone %s to-zone %s policy %s then permit " \
         "application-services " %(mode, from_zone, to_zone, policy_name)

    if service == "idp":
        cmd = cmd + "idp"
    elif service == "ssl":
        if service_profile is not None:
            cmd = cmd + "ssl-proxy profile-name " + service_profile
        else:
            if mode == "delete":
                cmd = cmd + "ssl-proxy"
            else:
                device.log(
                          level="ERROR",
                          message="ssl_profile name is mandatory for sslfp")
                raise Exception("ssl_profile name is mandatory for sslfp")
    elif service == "utm":
        if service_profile is not None:
            cmd = cmd + "utm-policy " + service_profile
        else:
            device.log(
                level="ERROR",
                message="utm_policy is mandatory for utm")
            raise Exception("utm_policy is mandatory for utm")
    elif service == "app_firewall":
        if service_profile is not None:
            cmd = cmd + "application-firewall rule-set " + service_profile
        else:
            device.log(
                level="ERROR",
                message="rule_set_name is mandatory for app_firewall")
            raise Exception("rule_set_name is mandatory for app_firewall")
    elif service == "app_qos":
        if service_profile is not None:
            cmd = cmd + "application-traffic-control rule-set " + service_profile
        else:
            device.log(
                level="ERROR",
                message="rule_set_name is mandatory for app_qos")
            raise Exception("rule_set_name is mandatory for app_qos")
    elif service == "anti_malware":
        if service_profile is not None:
            cmd = cmd + "advanced-anti-malware-policy " + service_profile
        else:
            device.log(
                level="ERROR",
                message="anti_malware_policy is mandatory for anti_malware service")
            raise Exception("anti_malware_policy is mandatory for anti_malware service")
    elif service == "sec_intel":
        if service_profile is not None:
            cmd = cmd + "security-intelligence-policy " + service_profile
        else:
            device.log(
                level="ERROR",
                message="sec_intel_policy is mandatory for sec_intel service")
            raise Exception("sec_intel_policy is mandatory for sec_intel service")
    else:
        device.log(
            level="ERROR",
            message="Unknown service, Supported services are idp, ssl, utm, app-firewall, "
                    "app-qos, anti-malware, security-intelligence")
        raise Exception("Unknown service")

    cmdlst.append(cmd)
    device.config(command_list=cmdlst)
    if commit is True:
        device.commit(timeout=120)
