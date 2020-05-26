# coding: UTF-8
"""Functions/Keywords to Configure Applications(set applications...)"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements


__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_single_application(device=None, application_name=None, term=None, alg=None, application_protocol=None,
                                 destination_port=None, ether_type=None, icmp_code=None, icmp_type=None,
                                 icmp6_code=None, icmp6_type=None, inactivity_timeout=None, protocol=None,
                                 rpc_program_number=None, source_port=None, uuid=None, logical_systems=None,
                                 commit=False):
    """
    Configuring a single application(set applications application...)
                                    (set logical-systems lsys1 applications application...)

    :Example:

    python:  configure_single_application(device=r0, application_name='policy_tcp_ftp', term='1',
                                 destination_port='13073', inactivity_timeout='13073', protocol='tcp',
                                 logical_systems='lsys1', commit=False)

    robot:  Configure Single Application    device=${r0}    application_name=policy_tcp_ftp    term=1
            ...    destination_port=13073    inactivity_timeout=500    protocol=tcp
            ...    logical_systems=lsys1    commit=${True}


    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str application_name:
        **REQUIRED**  Name of the application.
    :param str term:
        *OPTIONAL*  Name of the term if applicable. Default value: term=None
    :param str alg:
        *OPTIONAL*  Application Layer Gateway. Default value: alg=None
    :param str application_protocol:
        *OPTIONAL*  Application protocol type(To be used without 'term'). Default value: application_protocol=None
    :param str destination_port:
        *OPTIONAL*  Match TCP/UDP destination port. Default value: destination_port=None
    :param str ether_type:
        *OPTIONAL*  Match ether type(To be used without 'term' parameter). Default value: ether_type=None
    :param str icmp_code:
        *OPTIONAL*  Match ICMP message code. Default value: icmp_code=None
    :param str icmp_type:
        *OPTIONAL*  Match ICMP message type. Default value: icmp_type=None
    :param str icmp6_code:
        *OPTIONAL*  Match ICMP6 message code. Default value: icmp6_code=None
    :param str icmp6_type:
        *OPTIONAL*  Match ICMP6 message type. Default value: icmp6_type=None
    :param str inactivity_timeout:
        *OPTIONAL*  Application-specific inactivity timeout (seconds). Default value: inactivity_timeout=None
    :param str protocol:
        *OPTIONAL*  Match IP protocol type. Default value: protocol=None
    :param str rpc_program_number:
        *OPTIONAL*  Match range of RPC program numbers. Default value: rpc_program_number=None
    :param str source_port:
        *OPTIONAL*  Match TCP/UDP source port. Default value: source_port=None
    :param str uuid:
        *OPTIONAL*  Match universal unique identifier for DCE RPC objects. Default value: uuid=None
    :param str logical_systems:
        *OPTIONAL*  Logical System name. Default value: logical_systems=None
    :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False
    :return:
        * ``True`` when application configuration is entered
    :raises Exception:
        *  When mandatory parameters are missing
        *  Commit fails(when **commit** is True)
        *  Device behaves in an unexpected way while in config/cli mode
        *  Device handle goes bad(device disconnection).
    """

    if device is None:
        raise Exception("'device' is mandatory parameter for configuring an application")
    if application_name is None:
        device.log(level="ERROR", msg="'application_name' is a mandatory parameter for configuring an application")
        raise Exception("'application_name' is a mandatory parameter for configuring an application")

    commands = []

    if logical_systems is not None:
        cmd_prefix = 'set logical-systems ' + logical_systems + ' applications application ' + application_name + ' '
    else:
        cmd_prefix = 'set applications application ' + application_name + ' '

    if term is not None:
        cmd_prefix += 'term ' + term + ' '
        if alg is not None:
            commands.append(cmd_prefix + 'alg ' + alg)
    if term is None and application_protocol is not None:
        commands.append(cmd_prefix + 'application-protocol ' + application_protocol)
    if term is None and ether_type is not None:
        commands.append(cmd_prefix + 'ether-type ' + ether_type)
    if destination_port is not None:
        commands.append(cmd_prefix + 'destination-port ' + destination_port)
    if icmp_code is not None:
        commands.append(cmd_prefix + 'icmp-code ' + icmp_code)
    if icmp_type is not None:
        commands.append(cmd_prefix + 'icmp-type ' + icmp_type)
    if icmp6_code is not None:
        commands.append(cmd_prefix + 'icmp6-code ' + icmp6_code)
    if icmp6_type is not None:
        commands.append(cmd_prefix + 'icmp6-type ' + icmp6_type)
    if inactivity_timeout is not None:
        commands.append(cmd_prefix + 'inactivity-timeout ' + inactivity_timeout)
    if protocol is not None:
        commands.append(cmd_prefix + 'protocol ' + protocol)
    if rpc_program_number is not None:
        commands.append(cmd_prefix + 'rpc-program-number ' + rpc_program_number)
    if source_port is not None:
        commands.append(cmd_prefix + 'source-port ' + source_port)
    if uuid is not None:
        commands.append(cmd_prefix + 'uuid ' + uuid)

    # Executing the config commands
    if len(commands) != 0:
        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        device.config(command_list=commands)

        # Committing the config if asked by user
        if commit:
            return device.commit(timeout=60)
        else:
            return True
    else:
        device.log(level='ERROR', message='Incorrect set of parameters are provided. '
                                          'Kindly go through the documentation and examples.')
        raise Exception(
            'Incorrect set of parameters are provided. Kindly go through the documentation and examples.')


def configure_application_set(device=None, application_set_name=None, applications=None, logical_systems=None,
                              commit=False):
    """
    Configuring an application-set(set applications application-set...)
                                    (set logical-systems lsys1 applications application-set...)

    :Example:

    python:  configure_application_set(device=r0, application_set_name='policy_application_set',
                                 applications=['junos-pingv6', 'policy_tcp_ftp', 'policy_tcp_tftp'],
                                 logical_systems='lsys1', commit=False)

    robot:  ${applications} =    Create List    junos-pingv6    policy_tcp_ftp    policy_tcp_tftp
            Configure Application Set    device=${r0}    application_set_name=policy_tcp_ftp
            ...    applications=${applications}    logical_systems=lsys1    commit=${True}


    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str application_set_name:
        **REQUIRED**  Name of the application set.
    :param list applications:
        **REQUIRED**  Application Names as a list of strings. Ex. applications=['junos-pingv6', 'policy_tcp_ftp']
    :param logical_systems:
        *OPTIONAL*  Logical System name. Default value: logical_systems=None
    :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False
    :return:
        * ``True`` when application-set configuration is entered
    :raises Exception:
        *  When mandatory parameters are missing
        *  Commit fails(when **commit** is True)
        *  Device behaves in an unexpected way while in config/cli mode
        *  Device handle goes bad(device disconnection).
    """

    if device is None:
        raise Exception("'device' is mandatory parameter for configuring an application-set")
    if application_set_name is None:
        device.log(level="ERROR", msg="'application_set_name' is a mandatory parameter "
                                      "for configuring an application-set")
        raise Exception("'application_set_name' is a mandatory parameter for configuring an application-set")
    if applications is None or not isinstance(applications, list):
        device.log(level="ERROR", msg="'applications' is a mandatory parameter of 'list' type "
                                      "for configuring an application-set")
        raise Exception("'applications' is a mandatory parameter of 'list' type for configuring an application-set")

    commands = []

    if logical_systems is not None:
        cmd_prefix = 'set logical-systems ' + logical_systems + ' applications application-set ' + \
                     application_set_name + ' '
    else:
        cmd_prefix = 'set applications application-set ' + application_set_name + ' '

    for app in applications:
        commands.append(cmd_prefix + 'application ' + app)

    # Executing the config commands
    if len(commands) != 0:
        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        device.config(command_list=commands)

        # Committing the config if asked by user
        if commit:
            return device.commit(timeout=60)
        else:
            return True
    else:
        device.log(level='ERROR', message='Incorrect set of parameters are provided. '
                                          'Kindly go through the documentation and examples.')
        raise Exception(
            'Incorrect set of parameters are provided. Kindly go through the documentation and examples.')
