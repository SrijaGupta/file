"""
Utilities
"""

import re
import string
#from jnpr.toby.hldcl.device import get_model_for_device


def get_pic_name(device=None,  **kwargs):
    """
    To return the pic name
    Example:
        get_pic_name(device=device, port=port)

    ROBOT Example:
        Get pic name    device=${device}   port=${port}

    :param device:
      **REQUIRED** Handle of the device
    :param str port:
        *REQUIRED*  port number for flow session

    :return: string (pic_name)
    :rtype: string
    """


    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if 'port' not in kwargs:
        raise ValueError("'port' is a mandatory argument")

    port = str(kwargs.get('port'))
    srx_model = device.get_model()
    match = re.search("SRX5.*", srx_model)
    print(match)
    if match:
        print(port)
        cmd = ("show security flow session destination-port {port}".format(**vars()))
        #cmd = "show security flow session destination-port " + port
        session_info = device.cli(command=cmd, format="text").response()
        ssl_session = re.search('.*443', session_info, re.DOTALL)
        if ssl_session:
            list_fpc = re.findall('FPC\d PIC\d', ssl_session.group(0))
            last_fpc = list_fpc[-1]
            fpc_pic_num = re.search('(?P<FPC>FPC\d).*(?P<PIC>PIC\d)', last_fpc)
            print(fpc_pic_num.group('FPC'))
            print(fpc_pic_num.group('PIC'))
            dot = "."
            final_fpc = fpc_pic_num.group('FPC') + dot + fpc_pic_num.group('PIC')
            return final_fpc
        else:
            return None
    else:
        pic_to_be_parsed = []
        pic_to_be_parsed = device.get_srx_pfe_names()
        return pic_to_be_parsed[0]



def execute_pic_command(device=None, **kwargs):
    """
    To execute a command on all the pics
    Example:
        execute_pic_command(device=device, command=command)

    ROBOT Example:
        execute pic command    device=${device}    command=${command}

    :param str device:
        **REQUIRED** device name
    :param str command:
        **REQUIRED** command to execute on pic

    :return: Returns "True"

    :rtype: bool
    """
    command = kwargs.get('command', None)
    if device is None:
        raise ValueError("'device' is a mandatory argument")
    if command is None:
        raise ValueError("'command' is a mandatory argument")

    pic_list = []
    pic_list = device.get_srx_pfe_names()
    for pic in pic_list:
        response = device.vty(command=command, destination=pic)

    return True


def get_pic_list(device=None, **kwargs):
    """
    To get the pic list
    Example:
        get_pic_list(device=device)

    ROBOT Example:
        get pic list    device=${device}

    :param str device:
        **REQUIRED** device name

    :return: Returns string ['fpc0.pic0', 'fpc0.pic1', 'fpc0.pic2']

    :rtype: list
    """
    command = kwargs.get('command', None)
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    pic_list = []
    pic_list = device.get_srx_pfe_names()
    return pic_list

