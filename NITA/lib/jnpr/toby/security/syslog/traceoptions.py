# coding: UTF-8
"""Functions/Keywords to Configure traceoptions"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements


__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_traceoptions(device=None, feature=None, description='flag all', commit=False):
    """
    Configuring traceoptions

    :Example:

    python:  configure_traceoptions(device=r0, feature='flow',
                        description='packet-filter policy_test interface xe-0/0/1.0', commit=False)
             configure_traceoptions(device=r1, description='flag all', commit=False)

    robot:  Configure traceoptions    device=${r0}    feature=policies    description=file security-trace


    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str feature:
        *OPTIONAL*  Name of the feature. Ex. feature='policies', default=None
    :param str description:
        *OPTIONAL* Traceoptions configuration. Default value: description='flag all'. Other Examples:
                *  description='packet-filter policy_test interface xe-0/0/1.0'
                *  description='file debug.txt size 80000'
                *  description='file security-trace'
                *  description='file security-trace size 10000000'
                *  description='flag all'
    :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False
    :return:
        * ``True`` when scheduler configuration is entered
    :raises Exception:
        *  When mandatory parameters are missing
        *  Commit fails(when **commit** is True)
        *  Device behaves in an unexpected way while in config/cli mode
        *  Device handle goes bad(device disconnection).
    """

    if device is None:
        raise Exception("'device' is mandatory parameter for configuring traceoptions")

    if feature is not None:
        cmd_prefix = 'set security ' + feature + ' traceoptions '
    else:
        cmd_prefix = 'set security traceoptions '

    device.config(command_list=[cmd_prefix + description])

    if commit:
        return device.commit(timeout=60)
    else:
        return True
