"""
Configure groups global security forwarding-options
"""
__author__ = ['Sasikumar Sekar']
__contact__ = 'sasik@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_global_security_forwarding_options(device=None, family=None, mode=None, commit=False):
    """
    Configure groups global security forwarding-options

    :Example:

    python: configure_global_security_forwarding_options(device=router_handle, family=inet6,
                                               mode=drop)
    robot: configure global security forwarding options    device=router_handle
                        family=inet6    mode=drop

    :param Device device:
        **REQUIRED** device handler.
    :param str family:
        **REQUIRED** Family IPv6
    :param str mode:
        **REQUIRED** Forwarding mode
    :param bool commit:
            *OPTIONAL* provide if commit is needed. Ex. default = "False"
    :return:
        * ``True`` when forwarding-option configuration is committed or not committed
    :raises Exception: when mandatory parameter is missing
    """
    if device is None:
        raise Exception("'device' is a device handle and it is a mandatory parameter ")
    if family is None:
        device.log(level="ERROR", msg="'family' is mandatory parameter")
        raise Exception("'family' is a mandatory parameter ")
    if mode is None:
        device.log(level="ERROR", msg="'mode' is mandatory parameter")
        raise Exception("'mode' is mandatory parameter")

    if device is not None and family is not None\
            and mode is not None:
        device.config(command_list=['set groups global security forwarding-options'
                                    ' family ' + family + ' mode ' + mode])
    if commit is True:
        return device.commit(timeout=60)
    else:
        return True
