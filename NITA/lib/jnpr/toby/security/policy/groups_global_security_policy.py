"""
Configure Security Policy
"""

__author__ = ['Sasikumar Sekar']
__contact__ = 'sasik@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_groups_global_policy(device=None, from_zone=None, to_zone=None, policy_name=None,
                                   source_address=None, destination_address=None,
                                   application=None, action=None, default_policy_action=None,
                                   global_policy=False, scheduler_name=None,
                                   default_policy=False, commit=False):
    """
    Configuring groups global policy configuration on the box

    :Example:
    python: configure_groups_global_policy(device=router_handle, from_zone=trust, to_zone=untrust,
                                               policy_name=p1, commit=True)
    robot:
    configure groups global policy    device=router_handle    from_zone=trust
                                   to_zone=untrust    policy_name=p1    commit=${TRUE}

    configure groups global policy    device=${dh}    default_policy=${True}
        default_policy_action=deny
    configure groups global policy    device=${dh}    from_zone=trust
        to_zone=untrust   policy_name=p1
        scheduler_name=daily_scheduler
    configure groups global policy    device=${dh}   global_policy=${True}
        policy_name=p1    source_address=${source}
            destination_address=${destination}
            application=any    action=permit
    configure groups global policy    device=${dh}    from_zone=trust
        to_zone=untrust   policy_name=p1
        source_address=${source}    destination_address=${destination}
            application=any    action=deny

    :param str device:
    	**REQUIRED** device handler
    :param str from_zone:
    	*OPTIONAL* Define a policy context from this zone
    :param str to_zone:
    	*OPTIONAL* Destination zone
    :param str policy_name:
    	*OPTIONAL* Security policy name
    :param list source_address:
        *OPTIONAL* Match source address
    :param list destination_address:
    	*OPTIONAL* Match destination address
    :param list application:
        *OPTIONAL* Port-based application
    :param str action:
    	*OPTIONAL* Specify policy action to take when packet match criteria
    :param str default_policy_action:
        *OPTIONAL* default policy action.
    :param str scheduler_name:
        *OPTIONAL* Name of security scheduler
    :param bool global_policy:
        *OPTIONAL* Define a global policy context. Default value: commit=False
    :param bool default_policy:
        *OPTIONAL* Configure default action when no user-defined policy match
        Default value: commit=False
    :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False
    :return:
    	* ``True`` when policy configuration is entered
    :raises Exception: when mandatory parameter is missing

    """
    if device is None:

        raise Exception("'device' is mandatory parameter for this function")

    cmd = 'set groups global security policies '

    if global_policy:
        cmd = cmd + ' global '

    if from_zone is not None and to_zone is not None:
        cmd = cmd + ' from-zone ' + from_zone + ' to-zone ' + to_zone

    if policy_name is not None:
        cmd = cmd + ' policy ' + policy_name

    if default_policy:
        cmd = cmd + ' default-policy '

    if scheduler_name is not None:
        cmd = cmd + ' scheduler-name ' + scheduler_name

    if source_address is not None:
        if isinstance(source_address, list):
            for temp in source_address:
                device.config(command_list=[cmd + ' match source-address ' + temp])
        else:
            device.config(command_list=[cmd + ' match source-address ' + source_address])
    if destination_address is not None:
        if isinstance(destination_address, list):
            for temp in destination_address:
                device.config(command_list=[cmd + ' match destination-address ' + temp])
        else:
            device.config(command_list=[cmd + ' match destination-address ' + destination_address])
    if application is not None:
        if isinstance(application, list):
            for temp in application:
                device.config(command_list=[cmd + ' match application ' + temp])
        else:
            device.config(command_list=[cmd + ' match application ' + application])

    if action is not None:
        device.config(command_list=[cmd + ' then ' + action])

    elif default_policy_action is not None:
        device.config(command_list=[cmd  + default_policy_action])

    else:
        device.config(command_list=[cmd])

    if commit:
        return device.commit(timeout=60)
    else:
        return True
