"""
bfd-api-module
"""
import builtins
#import logging
from jnpr.toby.exception.toby_exception import TobyException
import jnpr.toby.services.prpd.prpd as prpd # pylint: disable=import-error



def _init(api_list):
    """
    Import the Stub Files
    """
    prpd.import_api(api_list)


def bfd_initialize(dev, channel_id, **kwargs):
    """
    Initialize BFD API's.This is a must to execute for any BFD api call
    """
    init_req = prpd.InitializeRequest()
    init_res = prpd.process_api(dev, channel_id, "Initialize", [init_req, "BFD"], kwargs.get("timeout", None))

    return init_res



def bfd_notification_subscribe(dev, channel_id, **kwargs):
    """
    BFD notification resgister to subscribe to all BFD session notifications
    """
    sub_req = prpd.SubscribeRequest()
    subres_stream = prpd.process_api(dev, channel_id, "Subscribe", [sub_req, "BFD"], kwargs.get("timeout", None))
    return subres_stream


def bfd_notification_unsubscribe(dev, channel_id, **kwargs):
    """
    BFD notification Unregister to unsubscribe to all BFD session notifications
    """
    unsub_req = prpd.UnsubscribeRequest()
    unsub_res = prpd.process_api(dev, channel_id, "Unsubscribe", [unsub_req, "BFD"], kwargs.get("timeout", None))
    return unsub_res


def bfd_session_delete_all(dev, channel_id, **kwargs):
    """
    BFD DeleteAll API to delete all BFD sessions programmed by client
    """
    del_all_req = prpd.DeleteAllRequest()
    del_all_res = prpd.process_api(dev, channel_id, "SessionDeleteAll", [del_all_req, "BFD"], kwargs.get("timeout", None))
    return del_all_res

def bfd_session_delete(dev, channel_id, **kwargs):
    """
    Delete BFD Sessions
    """
    delete_return_list = []

    if 'session_id' in kwargs:
        sessionid_list = []
        if isinstance(kwargs["session_id"], int):
            sessionid_list = [kwargs["session_id"], ]
        elif isinstance(kwargs["session_id"], list):
            sessionid_list = kwargs["session_id"]

    for sess_id in sessionid_list:
        session_key = prpd.SessionKey()
        session_key.session_id = int(sess_id)
        del_req = prpd.SessionRequest(key=session_key)
        del_res = prpd.process_api(dev, channel_id, "SessionDelete", [del_req, "BFD"], kwargs.get("timeout", None))

        delete_return_list.append(del_res)

    return delete_return_list


def bfd_session_add(dev, channel_id, **kwargs):
    """
    Add BFD Sessions
    """
    add_res_list = []
    add_list = []
    add_list = bfd_session_request(**kwargs)
    for add_req in add_list:
        add_res = prpd.process_api(dev, channel_id, "SessionAdd", [add_req, "BFD"], kwargs.get("timeout", None))
        add_res_list.append(add_res)

    return add_res_list

def bfd_session_request(**kwargs):
    """
    Attributes of bfd session
    """

    sessionkey_list = []
    request_list = []

    sessionkey_list = generate_session_key(**kwargs)
    for skey in sessionkey_list:
        sessionreq = prpd.SessionRequest()

        if 'session_type' in kwargs:
            bfd_type = kwargs.get('session_type')
            if ('ECHO_LITE' in bfd_type) or ('2' in bfd_type):
                sessionreq.type = prpd.SessionRequest.ECHO_LITE

        if 'session_mode' in kwargs:
            bfd_mode = kwargs.get('session_mode')
            if ('SINGLE_HOP' in bfd_mode) or ('1' in bfd_mode):
                sessionreq.mode = prpd.SessionRequest.SINGLE_HOP

        sessionreq.key.CopyFrom(skey)
        sessionreq.params.CopyFrom(generate_session_params(**kwargs))
        request_list.append(sessionreq)

    return  request_list

def generate_session_key(**kwargs):
    """
    Session Key Generate Request
    """

    localaddr_list = []
    remoteaddr_list = []
    interface_list = []

    if 'remote_address' in kwargs:
        if isinstance(kwargs["remote_address"], str):
            remoteaddr_list = [kwargs["remote_address"], ]
        elif isinstance(kwargs["remote_address"], list):
            remoteaddr_list = kwargs["remote_address"]
    else:
        raise Exception("Mandatory parameter 'remote_address' absent")


    if 'local_address' in kwargs:
        if isinstance(kwargs["local_address"], str):
            localaddr_list = [kwargs["local_address"], ]
        elif isinstance(kwargs["local_address"], list):
            localaddr_list = kwargs["local_address"]


    if 'interface_name' in kwargs:
        if isinstance(kwargs["interface_name"], str):
            interface_list = [kwargs["interface_name"], ]
        elif isinstance(kwargs["interface_name"], list):
            interface_list = kwargs["interface_name"]


    len_remote = len(remoteaddr_list)
    list_of_session = []

    for index in range(0, len_remote):
        session_key_add = prpd.SessionKey()

        if 'local_discriminator' in kwargs:
            if isinstance(kwargs["local_discriminator"], int):
                session_key_add.local_discriminator = kwargs.get('local_discriminator')
            else:
                raise Exception("Please enter integer value for local_discriminator")


        if 'remote_discriminator' in kwargs:
            if isinstance(kwargs["remote_discriminator"], int):
                session_key_add.remote_discriminator = kwargs.get('remote_discriminator')
            else:
                raise Exception("Please enter integer value for remote_discriminator")

        if 'cookie' in kwargs:
            if isinstance(kwargs["cookie"], int):
                session_key_add.cookie = kwargs.get('cookie')
            else:
                raise Exception("Please enter integer value for cookie")

        if 'session_id' in kwargs:
            if isinstance(kwargs["session_id"], int):
                session_key_add.session_id = kwargs.get('session_id')
            else:
                raise Exception("Please enter integer value for session_id")

        len_local = len(localaddr_list)
        len_int = len(interface_list)
        ip_type = prpd.netaddr.IPAddress(remoteaddr_list[index])
        family = ip_type.version
        if family == 6:
            session_key_add.remote_address.CopyFrom(prpd.NetworkAddress(inet6=prpd.IpAddress(addr_string=remoteaddr_list[index])))
            if index < len_local:
                session_key_add.local_address.CopyFrom(prpd.NetworkAddress(inet6=prpd.IpAddress(addr_string=localaddr_list[index])))
        else:
            session_key_add.remote_address.CopyFrom(prpd.NetworkAddress(inet=prpd.IpAddress(addr_string=remoteaddr_list[index])))
            if index < len_local:
                session_key_add.local_address.CopyFrom(prpd.NetworkAddress(inet=prpd.IpAddress(addr_string=localaddr_list[index])))

        if index < len_int:
            session_key_add.interface_name = str(interface_list[index])


        list_of_session.append(session_key_add)

    return list_of_session

def generate_session_params(**kwargs):
    """
    Session Params Generate Request
    """

    session_parameters = prpd.SessionParameters()

    if 'minimum_tx_interval' in kwargs:
        session_parameters.minimum_tx_interval = int(kwargs.get('minimum_tx_interval'))

    if 'multiplier' in kwargs:
        session_parameters.multiplier = int(kwargs.get('multiplier'))


    if 'minimum_rx_interval' in kwargs:
        session_parameters.minimum_rx_interval = int(kwargs.get('minimum_rx_interval'))


    if 'minimum_echo_tx_interval' in kwargs:
        session_parameters.minimum_echo_tx_interval = int(kwargs.get('minimum_echo_tx_interval'))


    return session_parameters
