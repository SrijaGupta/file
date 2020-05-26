# coding: UTF-8
"""Functions/Keywords to Configure Network Address Translation"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements


__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_nat_pool(device=None, flavour=None, pool=None, address=None, routing_instance=None, port=None,
                       overflow_pool=None, host_address_base=None, address_persistent=False, logical_system=None,
                       commit=False):
    """
    Configuring a NAT pool

    :Example:

    python:  configure_nat_pool(device=r0, flavour='source', pool='pool1', address='20.20.20.20/32', commit=False)

    robot:  Configure Nat Pool    device={r0}    flavour=source    pool=pool1    address=20.20.20.20/32    commit={True}

    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str flavour:
        **REQUIRED**  Flavour of NAT. 'source'/'destination'
    :param str pool:
        **REQUIRED**  Name of the pool
    :param str address:
        *OPTIONAL*  Numeric IPv4 or IPv6 address with prefix. Default value: address=None
    :param str routing_instance:
        *OPTIONAL*  Routing Instance name. Default value: routing_instance=None
    :param str port:
        *OPTIONAL*  Port options. Default value: port=None
    :param str overflow_pool:
        *OPTIONAL*  Overflow pool name. Default value: overflow_pool=None
    :param str host_address_base:
        *OPTIONAL*  Host Address Base. Default value: host_address_base=None
    :param bool address_persistent:
        *OPTIONAL*  Allow source address to maintain same translation. Default value: address_persistent=False
    :param str logical_system:
        *OPTIONAL*  name of Logical System. Default value: logical_system=None
    :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False
    :return:
        * ``True`` when zone configuration is entered
    :raises Exception:
        *  When mandatory parameters are missing
        *  Commit fails(when **commit** is True)
        *  Device behaves in an unexpected way while in config/cli mode
        *  Device handle goes bad(device disconnection).
    """

    if device is None:
        raise Exception("'device' is mandatory parameter for configuring nat pool")
    if flavour is None:
        device.log(level="ERROR", msg="'flavour' is a mandatory parameter for configuring nat pool")
        raise Exception("'flavour' is a mandatory parameter for configuring nat pool")
    if pool is None:
        device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring " + flavour + " nat pool")
        raise Exception("'pool' is a mandatory parameter for configuring " + flavour + " nat pool")

    commands = []

    if logical_system is not None:
        cmd_prefix = 'set logical-systems ' + logical_system + ' security nat ' + flavour + ' pool ' + pool + ' '
    else:
        cmd_prefix = 'set security nat ' + flavour + ' pool ' + pool + ' '

    if address is not None:
        commands.append(cmd_prefix + 'address ' + address)
    if routing_instance is not None:
        commands.append(cmd_prefix + 'routing-instance ' + routing_instance)
    if overflow_pool is not None:
        commands.append(cmd_prefix + 'overflow-pool ' + overflow_pool)
    if host_address_base is not None:
        commands.append(cmd_prefix + 'host-address-base ' + host_address_base)
    if port is not None:
        if isinstance(port, list):
            for x in range(0,len(port)):
                commands.append(cmd_prefix + 'port ' + port[x])
        else:
            commands.append(cmd_prefix + 'port ' + port)
    if address_persistent:
        commands.append('set security nat ' + flavour + ' address-persistent')

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


def configure_nat_rule_set(device=None, flavour=None, rule_set=None, from_routing_instance=None, from_interface=None,
                           from_zone=None, to_routing_instance=None, to_interface=None,
                           to_zone=None, rule=None, match_application=None, match_protocol=None,
                           match_source_address=None, match_destination_address=None, match_source_port=None,
                           match_destination_port=None, match_source_address_name=None,
                           match_destination_address_name=None, then_interface=False, then_pool=None, then_prefix=None,
                           then_prefix_routing_instance=None, then_off=False, raise_threshold=None, clear_threshold=None,
                           logical_system=None, commit=False):
    """
    Configuring a rule-set for NAT

    :Example:

    python:  configure_nat_rule_set(device=r0, flavour='source', rule_set='src', from_routing_instance='green',
                to_routing_instance='red', rule='r1', match_source_address='192.1.1.0/24',
                match_destination_address='192.1.2.0/24', then_pool='pool1', commit=False)

    robot:  Configure Nat Rule Set    device={r0}    flavour=source    pool=p1    rule_set=src
            ...    from_routing_instance=green    to_routing_instance=red    rule=r1
            ...    match_source_address=192.1.1.0/24    match_destination_address=192.1.2.0/24    then_pool=pool1

    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str flavour:
        **REQUIRED**  Flavour of NAT. 'source'/'destination'/'static'
    :param str rule_set:
        **REQUIRED**  Name of the rule-set.
    :param str from_routing_instance:
        *OPTIONAL*  Source routing instance. Default value: from_routing_instance=None
    :param str from_interface:
        *OPTIONAL*  Source interface. Default value: from_interface=None
    :param str from_zone:
        *OPTIONAL*  Source zone. Default value: from_zone=None
    :param str to_routing_instance:
        *OPTIONAL*  Destination routing instance. Default value: to_routing_instance=None
    :param str to_interface:
        *OPTIONAL*  Destination interface. Default value: to_interface=None
    :param str to_zone:
        *OPTIONAL*  Destination zone. Default value: to_zone=None
    :param str rule:
        **REQUIRED**  Name of the rule.
    :param str match_application:
        *OPTIONAL*  Application name. Default value: match_application=None
    :param str match_protocol:
        *OPTIONAL*  protocol name. Default value: match_protocol=None
    :param str match_source_address:
        *OPTIONAL*  Source address. Default value: match_source_address=None
    :param str match_destination_address:
        *OPTIONAL*  Destination address. Default value: match_destination_address=None
    :param str match_source_port:
        *OPTIONAL*  Source port. Default value: match_source_port=None
    :param str match_destination_port:
        *OPTIONAL*  Destination port. Default value: match_destination_port=None
    :param str match_source_address_name:
        *OPTIONAL*  Source address name. Default value: match_source_address_name=None
    :param str match_destination_address_name:
        *OPTIONAL*  Destination address name. Default value: match_destination_address_name=None
    :param bool then_interface:
        *OPTIONAL*  Option to enable NAT interface. Default value: then_interface=False
    :param str then_pool:
        *OPTIONAL*  NAT pool name that is to be used. Default value: then_pool=None
    :param str then_prefix:
        *OPTIONAL*  Static NAT Address prefix. Default value: then_prefix=None
    :param bool then_off:
        *OPTIONAL*  then flavour-nat off. Default value: then_off=False
    :param str then_prefix_routing_instance:
        *OPTIONAL*  Static NAT Address prefix routing instance name. Default value: then_prefix_routing_instance=None
    :param str raise_threshold:
        *OPTIONAL*  rule-session-count-alarm raise-threshold. Default value: raise_threshold=None
    :param str clear_threshold:
        *OPTIONAL*  rule-session-count-alarm clear-threshold. Default value: clear_threshold=None
    :param str logical_system:
        *OPTIONAL*  name of Logical System. Default value: logical_system=None
    :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False
    :return:
        * ``True`` when zone configuration is entered
    :raises Exception:
        *  When mandatory parameters are missing
        *  Commit fails(when **commit** is True)
        *  Device behaves in an unexpected way while in config/cli mode
        *  Device handle goes bad(device disconnection).
    """

    if device is None:
        raise Exception("'device' is mandatory parameter for configuring nat rule-set")
    if flavour is None:
        device.log(level="ERROR", msg="'flavour' is a mandatory parameter for configuring nat rule-set")
        raise Exception("'pool' is a mandatory parameter for configuring nat rule-set")
    if rule_set is None:
        device.log(level="ERROR", msg="'rule_set' is mandatory for configuring " + flavour + " nat rule-set")
        raise Exception("'rule_set' is a mandatory parameter for configuring source nat rule-set")
    if rule is None:
        device.log(level="ERROR", msg="'rule' is a mandatory parameter for configuring " + flavour + " nat rule-set")
        raise Exception("'rule' is a mandatory parameter for configuring source nat rule-set")

    commands = []

    if logical_system is not None:
        cmd_prefix = 'set logical-systems ' + logical_system + ' security nat '
    else:
        cmd_prefix = 'set security nat '

    # from and to commands
    if from_routing_instance is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' from routing-instance ' + from_routing_instance)
    if from_interface is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' from interface ' + from_interface)
    if from_zone is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' from zone ' + from_zone)
    if to_routing_instance is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' to routing-instance ' + to_routing_instance)
    if to_interface is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' to interface ' + to_interface)
    if to_zone is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' to zone ' + to_zone)

    # match commands
    if match_application is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' match application ' + match_application)
    if match_protocol is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' match protocol ' + match_protocol)
    if match_source_address is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' match source-address ' + match_source_address)
    if match_destination_address is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' match destination-address ' + match_destination_address)
    if match_source_port is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' match source-port ' + match_source_port)
    if match_destination_port is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' match destination-port ' + match_destination_port)
    if match_source_address_name is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' match source-address-name ' + match_source_address_name)
    if match_destination_address_name is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' match destination-address-name ' + match_destination_address_name)

    # then commands
    if then_interface:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' then ' + flavour + '-nat interface')
    if then_pool is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' then ' + flavour + '-nat pool ' + then_pool)
    if then_prefix is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' then ' + flavour + '-nat prefix ' + then_prefix)
    if then_prefix_routing_instance is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' then ' +
                        flavour + '-nat prefix routing-instance ' + then_prefix_routing_instance)
    if then_off:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' then ' + flavour + '-nat off')
    if raise_threshold is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' then ' +
                        flavour + '-nat rule-session-count-alarm raise-threshold ' + raise_threshold)
    if clear_threshold is not None:
        commands.append(cmd_prefix + flavour + ' rule-set ' + rule_set +
                        ' rule ' + rule + ' then ' +
                        flavour + '-nat rule-session-count-alarm clear-threshold ' + clear_threshold)

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
        raise Exception('Incorrect set of parameters are provided. Kindly go through the documentation and examples.')