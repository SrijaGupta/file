"""
Configure security interface
"""


def configure_interface(device=None, interface=None, address=None,
                        inet_mode="inet", unit='0', commit=False):
    """
    Configure security interface

    :Example:

    python: configure_interface(device=router_handle, interface=ge-0/0/1,
                                               address=40.40.40.2, inet_mode=inet6, unit='5')
    robot: configure interface    device=router_handle
                        interface=ge-0/0/1    address=40.40.40.2    inet_mode=inet    unit='5'

    :param Device device:
        **REQUIRED** device handler.
    :param str interface:
        **REQUIRED** interface name from box to host. Ex. name = "ge-0/0/1"
    :param str address:
        **REQUIRED** provide valid ip with subnet mask.
        if interface is 'st0' , address is not mandatory
    :param str unit:
        *OPTIONAL* integer value for unit. Ex. default = "0"
    :param str inet_mode:
        *OPTIONAL* inet mode. Ex. default = "inet"
    :param bool commit:
        *OPTIONAL* provide if commit is needed. Ex. default = "False"
    :return:
        * ``True`` when zone configuration is committed or not committed
    :raises Exception: when mandatory parameter is missing
    """
    if device is None:
        raise Exception("'device' is a device handle and it is a mandatory parameter ")
    if interface is None:
        device.log(level="ERROR", msg="'interface' is mandatory parameter")
        raise Exception("'interface' is a mandatory parameter ")
    if address is None and 'st0' not in interface:
        device.log(level="ERROR", msg="'address' is mandatory parameter for configuring" + \
                                      " basic interface")
        raise Exception("'address' is mandatory parameter for configuring basic interface")

    if device is not None and interface is not None \
            and address is not None and unit is not None and inet_mode is not None:
        device.config(command_list=['set interface ' + interface +
                                    ' unit ' + unit + ' family ' + inet_mode +
                                    ' address ' + address])
    if 'st0' in interface:
        device.config(command_list=['set interface ' + interface +
                                    ' unit ' + str(unit) + ' family ' + inet_mode])
    if commit is True:
        return device.commit(timeout=60)
    else:
        return True