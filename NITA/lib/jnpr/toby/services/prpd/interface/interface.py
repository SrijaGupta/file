
"""
prpd-interface-api-module
"""

import jnpr.toby.services.prpd.prpd as prpd # pylint: disable=import-error

def _init(api_list):
    """
    DOcs
    """
    prpd.import_api(api_list)


def interface_initialize(dev, channel_id, **kwargs):
    """
    DOcs
    """
    initreq = prpd.RoutingInterfaceInitializeRequest()
    initreply = prpd.process_api(dev, channel_id, "RoutingInterfaceInitialize", [initreq, "RoutingInterface"], kwargs.get("timeout", None))

    return initreply

def interface_notification_register(dev, channel_id, **kwargs):
    """
    DOcs
    """
    notifreg = prpd.RoutingInterfaceNotificationRegisterRequest(address_format=0)
    notifstream = prpd.process_api(dev, channel_id, "RoutingInterfaceNotificationRegister", [notifreg, "RoutingInterface"],\
                                    kwargs.get("timeout", None))

    return  notifstream


def interface_notification_unregister(dev, channel_id, **kwargs):
    """
    DOcs
    """

    notifunreg = prpd.RoutingInterfaceNotificationUnregisterRequest()
    reply = prpd.process_api(dev, channel_id, "RoutingInterfaceNotificationUnregister", [notifunreg, "RoutingInterface"], kwargs.get("timeout", None))

    return reply


def interface_get(dev, channel_id, **kwargs):

    """
    DOcs
    """
    getreq = prpd.RoutingInterfaceGetRequest()
    getreq.address_format = 0

    if 'interface' in kwargs:
        getreq.name = kwargs.get('interface')
    else:
        getreq.index = kwargs.get('index')

    reply = prpd.process_api(dev, channel_id, "RoutingInterfaceGet", [getreq, "RoutingInterface"], kwargs.get("timeout", None))

    return reply




def interface_notification_refresh(dev, channel_id, **kwargs):
    """
    DOcs
    """

    notifreg = prpd.RoutingInterfaceNotificationRefreshRequest()
    notifstream = prpd.process_api(dev, channel_id, "RoutingInterfaceNotificationRefresh", [notifreg, "RoutingInterface"],\
                                    kwargs.get("timeout", None))

    return  notifstream






