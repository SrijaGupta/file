# coding: UTF-8
"""Functions/Keywords to Check resource-manager details"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements

from jxmlease import parse
import jxmlease

__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def verify_resource_manager(device=None, group=None, resource=None, setting=False, summary=False,
                            group_id=None, resource_id=None, client=None, group_total=None, group_count=None,
                            resource_total=None, resource_count=None, client_count=None, session_count=None,
                            setting_timeout=None, setting_count=None, setting_pinhole_age=None):
    """
    Verifying Resource Manager Output

    :Example:

    python:  verify_resource_manager(device=r0, group='active', group_id='1', client='FTP ALG', group_total='4096',
                                    group_count='1')
             verify_resource_manager(device=r0, resource='active', group_id='1', resource_id='1', client='FTP ALG',
                                    resource_total='8192', resource_count='1')

    robot:  Verify Resource Manager    device=${r0}    group=active    group_id=1    client=FTP ALG    group_total=4096
            ...   group_count=1
            Verify Resource Manager    device=${r0}    resource=active    group_id=1    resource_id=1    client=FTP ALG
            ...   resource_total=4096    group_count=1


    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str group:
        *OPTIONAL*  Group name.Ex. group='active'
    :param str resource:
        *OPTIONAL*  Resource name.Ex. resource='active'
    :param bool setting:
        *OPTIONAL*  Verify Settings. Ex. settings=True
    :param bool summary:
        *OPTIONAL*  Verify Summary. Ex. summary=True
    :param str group_id:
        *OPTIONAL*  Verify group-id
    :param str resource_id:
        *OPTIONAL*  Verify resource-id
    :param str client:
        *OPTIONAL*  Verify client
    :param str group_total:
        *OPTIONAL*  Verify group total
    :param str group_count:
        *OPTIONAL*  verify group-count
    :param str resource_total:
        *OPTIONAL*  verify resource-total
    :param str resource_count:
        *OPTIONAL*  verify resource-count
    :param str client_count:
        *OPTIONAL*  verify client-count
    :param str session_count:
        *OPTIONAL*  verify session-count
    :param str setting_timeout:
        *OPTIONAL*  verify setting-timeout
    :param str setting_count:
        *OPTIONAL*  verify setting-count
    :param str setting_pinhole_age:
        *OPTIONAL*  verify setting-pinhole-age

    :return:
        * ``True`` when verification succeeds
    :raises Exception:
        *  When wrong parameters are passed
        *  When verification Fails
        *  CLI XML Output is not in correct xml format.
        *  Device behaves in an unexpected way while in cli mode
        *  Device handle goes bad(device disconnection).
    """

    if device is None:
        raise Exception("'device' is mandatory parameter")
    if group is None and resource is None and not setting and not summary:
        raise Exception("One of the following parameters should be mentioned:group/resource/setting/summary")
    result = False
    if group is not None:
        output = parse(device.cli(command='show security resource-manager group '+group, format='xml').response())
        output = output['rpc-reply']['resmgr-group-'+group]
        if type(output['resmgr-group-'+group+'-data']) == jxmlease.listnode.XMLListNode:
            len_range = len(output['resmgr-group-'+group+'-data'])
        else:
            len_range = 1
            output['resmgr-group-'+group+'-data'][0] = output['resmgr-group-'+group+'-data']
        for x in range(0, len_range):
            res = str(x + 1)
            device.log('Checking Group: ' + res)
            if group_id is not None:
                if output['resmgr-group-'+group+'-data'][x]['resmgr-group-'+group+'-data-grp-id'] == group_id:
                    result = True
                    device.log('Group-ID(' + group_id + ') matched.')
                else:
                    result = False
                    device.log(level='ERROR', message='Group-ID(' + group_id + ') not found.')
                    continue
            if client is not None:
                if output['resmgr-group-'+group+'-data'][x]['resmgr-group-'+group+'-data-client'] == client:
                    result = True
                    device.log('Client(' + client + ') matched.')
                else:
                    result = False
                    device.log(level='ERROR', message='Client(' + client + ') not found.')
                    continue
            if result:
                break
        if group_total is not None:
            if output['resmgr-group-'+group+'-total'] == group_total:
                result = True
                device.log('Group Total(' + group_total + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Group Total(' + group_total + ') not found.')
        if group_count is not None:
            if output['resmgr-group-'+group+'-count'] == group_count:
                result = True
                device.log('Group Count(' + group_count + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Group Count(' + group_count + ') not found.')
    if resource is not None:
        output = parse(device.cli(command='show security resource-manager resource ' + resource,
                                  format='xml').response())
        output = output['rpc-reply']['resmgr-resource-' + resource]
        if type(output['resmgr-resource-'+resource+'-data']) == jxmlease.listnode.XMLListNode:
            len_range = len(output['resmgr-resource-'+resource+'-data'])
        else:
            len_range = 1
            output['resmgr-resource-'+resource+'-data'][0] = output['resmgr-resource-'+resource+'-data']

        for x in range(0, len_range):
            res = str(x + 1)
            device.log('Checking Resource: ' + res)
            if resource_id is not None:
                if output['resmgr-resource-'+resource+'-data'][x]['resmgr-resource-'+resource+'-data-res-id'] == \
                        resource_id:
                    result = True
                    device.log('Resource-ID(' + resource_id + ') matched.')
                else:
                    result = False
                    device.log(level='ERROR', message='Resource-ID(' + resource_id + ') not found.')
                    continue
            if group_id is not None:
                if output['resmgr-resource-'+resource+'-data'][x]['resmgr-resource-'+resource+'-data-grp-id'] == \
                        group_id:
                    result = True
                    device.log('Group-ID(' + group_id + ') matched.')
                else:
                    result = False
                    device.log(level='ERROR', message='Group-ID(' + group_id + ') not found.')
                    continue
            if client is not None:
                if output['resmgr-resource-'+resource+'-data'][x]['resmgr-resource-'+resource+'-data-client'] == client:
                    result = True
                    device.log('Client(' + client + ') matched.')
                else:
                    result = False
                    device.log(level='ERROR', message='Client(' + client + ') not found.')
                    continue
            if result:
                break
        if resource_total is not None:
            if output['resmgr-resource-'+resource+'-total'] == resource_total:
                result = True
                device.log('Resource Total(' + resource_total + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Resource Total(' + resource_total + ') not found.')
        if resource_count is not None:
            if output['resmgr-resource-'+resource+'-count'] == resource_count:
                result = True
                device.log('Resource Count(' + resource_count + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Resource Count(' + resource_count + ') not found.')
    if summary:
        output = parse(
            device.cli(command='show security resource-manager summary', format='xml').response())
        output = output['rpc-reply']['resource-manager-summary-information']
        if client_count is not None:
            if output['active-client-count'] == client_count:
                result = True
                device.log('Client Count(' + client_count + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Client Count(' + client_count + ') not found.')
        if group_count is not None:
            if output['active-group-count'] == group_count:
                result = True
                device.log('Group Count(' + group_count + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Group Count(' + group_count + ') not found.')
        if resource_count is not None:
            if output['active-resource-count'] == resource_count:
                result = True
                device.log('Resource Count(' + resource_count + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Resource Count(' + resource_count + ') not found.')
        if session_count is not None:
            if output['active-session-count'] == session_count:
                result = True
                device.log('Session Count(' + session_count + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Session Count(' + session_count + ') not found.')
    if setting:
        output = parse(device.cli(command='show security resource-manager settings', format='xml').response())
        output = output['rpc-reply']['resmgr-settings']
        if setting_timeout is not None:
            if output['resmgr-settings-timeout'] == setting_timeout:
                result = True
                device.log('Setting Timeout(' + setting_timeout + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Setting Timeout(' + setting_timeout + ') not found.')
        if setting_count is not None:
            if output['resmgr-settings-count'] == setting_count:
                result = True
                device.log('Setting Count(' + setting_count + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Setting Count(' + setting_count + ') not found.')
        if setting_pinhole_age is not None:
            if output['resmgr-settings-pinhole-age'] == setting_pinhole_age:
                result = True
                device.log('Setting Pinhole Age(' + setting_pinhole_age + ') matched.')
            else:
                result = False
                device.log(level='ERROR', message='Setting Pinhole Age(' + setting_pinhole_age + ') not found.')
    if result:
        device.log('All mentioned parameters passed.')
        return True
    else:
        device.log(level='ERROR', message='One or more parameters did not pass the verification')
        raise Exception('One or more parameters did not pass the verification')
