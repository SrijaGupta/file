# coding: UTF-8
"""Functions/Keywords to Configure routing-options and routing-instances"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches

__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_routing_options(device=None, interface_routes_rib_group=None, static_rib_group=None, static_route=None,
                              import_rib=None, commit=False):
    """
    Configuring routing-options

    :Example:

    python:  configure_routing_options(device=r0, interface_routes_rib_group=['inet', 'if-rib1'],
                static_rib_group='if-rib1', static_route=['13.13.0.0/16', '5.1.1.2'], import_rib=['if-rib1', 'inet.0'],
                commit=False)

    robot:  ${interface_routes_rib_group} =    Create List    inet    if-rib1
            ${static_route} =    Create List    13.13.0.0/16    5.1.1.2
            ${import_rib} =    Create List    if-rib1    inet.0

            Configure Routing Options    device=${r0}    interface_routes_rib_group=${interface_routes_rib_group}
            ...   static_rib_group=if-rib1    static_route=${static_route}    import_rib=${import_rib}    commit=${True}


    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param list interface_routes_rib_group:
        *OPTIONAL*  Interface route of rib-group. List of two strings. [type of address, name of group].
                    Ex. interface_routes_rib_group = ['inet6', 'if-rib2']
    :param str static_rib_group:
        *OPTIONAL*  Static rib-group(Routing table group). Default value: static_rib_group=None
    :param list static_route:
        *OPTIONAL*  Static route and next hop. List of two strings. [route network, next hop ip].
                    Ex. static_route = ['13.13.0.0/16', '5.1.1.2']
    :param list import_rib:
        *OPTIONAL*  Import rib to rib group. List of two strings. [rib-group, rib to be imported].
                    Ex. import_rib = ['if-rib1', 'inet.0']
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
        raise Exception("'device' is mandatory parameter for configuring routing options")

    commands = []

    if interface_routes_rib_group is not None:
        if isinstance(interface_routes_rib_group, list) and len(interface_routes_rib_group) == 2:
            commands.append('set routing-options interface-routes rib-group ' + ' '.join(interface_routes_rib_group))
        else:
            device.log(level='ERROR', message='"interface_routes_rib_group" is not provided in the correct format.'
                                              'It is a list of two strings. [type of address, name of group].'
                                              'Ex. interface_routes_rib_group = ["inet6", "if-rib2"]')
    if static_rib_group is not None:
        commands.append('set routing-options static rib-group ' + static_rib_group)
    if static_route is not None:
        if isinstance(static_route, list) and len(static_route) == 2:
            commands.append('set routing-options static route ' + ' next-hop '.join(static_route))
        else:
            device.log(level='ERROR', message='"static_route" is not provided in the correct format.'
                                              'It is a list of two strings. [route network, next hop ip].'
                                              'Ex. static_route = ["13.13.0.0/16", "5.1.1.2"]')
    if import_rib is not None:
        if isinstance(import_rib, list) and len(import_rib) == 2:
            commands.append('set routing-options rib-groups ' + ' import-rib '.join(import_rib))
        else:
            device.log(level='ERROR', message='"import_rib" is not provided in the correct format.'
                                              'It is a list of two strings. [rib-group, rib to be imported].'
                                              'Ex. import_rib = ["if-rib1", "inet.0"]')
    # Executing the config commands
    if len(commands) != 0:
        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        device.config(command_list=commands)

        # Committing the config if asked by user
        if commit:
            return device.commit(timeout=240)
        else:
            return True
    else:
        device.log(level='ERROR', message='Incorrect set of parameters are provided. '
                                          'Kindly go through the documentation and examples.')
        raise Exception(
            'Incorrect set of parameters are provided. Kindly go through the documentation and examples.')


def configure_routing_instances(device=None, routing_instance_name=None, instance_type=None, interface=None,
                                routing_options=None, interface_routes_rib_group=None, commit=False):
    """
    Configuring routing-instances

    :Example:

    python:  configure_routing_instances(device=r0, routing_instance_name='green', instance_type='virtual-router',
                interface='fe-0/0/2.0', interface_routes_rib_group=['inet', 'if-rib1'], commit=False)

    robot:  ${interface_routes_rib_group} =    Create List    inet    if-rib1
            Configure Routing Instances    device=${r0}    routing_instance_name=green    instance_type=virtual-router
            ...    interface=fe-0/0/2.0    interface_routes_rib_group=${interface_routes_rib_group}    commit=${True}


    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str routing_instance_name:
        **REQUIRED**  Name of the routing instance.
    :param str instance_type:
        *OPTIONAL*  Routing instance type. Default value: instance_type=None
                    Ex. instance_type='virtual-router'
    :param str interface:
        *OPTIONAL*  Interface linked to routing instance. Default value: interface=None
                    Ex. interface='fe-0/0/2.0'
    :param list interface_routes_rib_group:
        *OPTIONAL*  Interface route of rib-group for the routing instance.
                    List of two strings. [type of address, name of group].
                    Ex. interface_routes_rib_group = ['inet6', 'if-rib2']
    :param str routing_options:
        *OPTIONAL*  String or List of strings of routing options
                    Ex. routing_options = 'static route 20.0.0.0/24 next-table inet.0'
                    Ex. routing_options = ['static route 20.0.0.0/24 next-table inet.0',
                        'static route 20.0.0.0/24 next-table inet.0']
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
        raise Exception("'device' is mandatory parameter for configuring routing instances")
    if routing_instance_name is None:
        device.log(level="ERROR",
                   msg="'routing_instance_name' is a mandatory parameter for configuring routing instances")
        raise Exception("'routing_instance_name' is a mandatory parameter for configuring routing instances")

    commands = []

    if instance_type is not None:
        commands.append('set routing-instances  ' + routing_instance_name +
                        ' instance-type ' + instance_type)
    if interface is not None:
        commands.append('set routing-instances  ' + routing_instance_name +
                        ' interface ' + interface)
    if interface_routes_rib_group is not None:
        if isinstance(interface_routes_rib_group, list) and len(interface_routes_rib_group) == 2:
            commands.append('set routing-instances ' + routing_instance_name +
                            ' routing-options interface-routes rib-group ' + ' '.join(interface_routes_rib_group))
        else:
            device.log(level='ERROR', message='"interface_routes_rib_group" is not provided in the correct format.'
                                              'It is a list of two strings. [type of address, name of group].'
                                              'Ex. interface_routes_rib_group = ["inet", "if-rib1"]')
    if routing_options is not None:
        if isinstance(routing_options, list):
            for x in range(0, len(routing_options)):
                commands.append('set routing-instances  ' + routing_instance_name +
                                ' routing-options ' + routing_options[x])
        else:
            commands.append('set routing-instances  ' + routing_instance_name +
                            ' routing-options ' + routing_options)

    # Executing the config commands
    if len(commands) != 0:
        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        device.config(command_list=commands)

        # Committing the config if asked by user
        if commit:
            return device.commit(timeout=240)
        else:
            return True
    else:
        device.log(level='ERROR', message='Incorrect set of parameters are provided. '
                                          'Kindly go through the documentation and examples.')
        raise Exception(
            'Incorrect set of parameters are provided. Kindly go through the documentation and examples.')
