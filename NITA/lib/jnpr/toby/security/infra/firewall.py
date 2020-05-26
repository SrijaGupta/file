import jxmlease

def configure_firewall_filter(filtername=None, device=None, term=None, family=None, source_address=None, destination_address=None, source_port=None, destination_port=None, protocol=None, precedence=None, dscp=None, action=None, commit=False):
    """
    Configure filrewall filter 

    :Example:

    python: configure_firewall_filter(filtername="trust", device=router_handle, term=term1)

    robot: configure firewall filter    filtername=router    device=router_handle   term=term1   

    :param str filtername:
        **REQUIRED** filtername  Ex. name = "router"
    :param Device device:
        **REQUIRED** device handler
    :param str term:
        *REQUIRED* provide valid term name . Ex. term = "term1"
    :param action:
        *OPTIONAL* action provide valid actions to be performed 
    :param str protocol:
        *OPTIONAL* provide valid protocol. Ex. default = "all"
    :return:
        * ``True`` when firewall filter  configuration is committed
    :raises Exception: when mandatory parameter is missing
    :param bool commit:
        *OPTIONAL* provide if commit is needed. Ex. default = "False"
    :return:
        * ``True`` when firewall configuration is committed or not committed


    """

    if device is None:
        raise Exception("'device' is mandatory parameter "
                        "for configuring basic firewall filter - device handle")

    if filtername is None:
        device.log(level="ERROR", msg="'filtername' is mandatory parameter for configuring basic filter")
        raise Exception("'filtername' is mandatory parameter for configuring basic filter")
    if term is None:
        device.log(level="ERROR", msg="'termname' is mandatory parameter for configuring filter")
        raise Exception("'filtername' is mandatory parameter for configuring filter")

    if action is None:
        action = ["reject", "alert", "count test", "log"]
    if family is None:
        family =   "inet"
    if filtername is not None and device is not None and term is not None and action is not None and family is not None: 
             if source_address is not None:
                 device.config(command_list=['set firewall family ' + family + ' filter ' + filtername + ' term ' + term + ' from source-address ' + source_address])
             if destination_address is not None:
                 device.config(command_list=['set firewall family ' + family + ' filter ' + filtername + ' term ' + term + ' from destination-address ' + destination_address])
             if source_port is not None:
                 device.config(command_list=['set firewall family ' + family + ' filter ' + filtername + ' term ' + term + ' from source-port ' + source_port])
             if destination_port is not None:
                 device.config(command_list=['set firewall family ' + family + ' filter ' + filtername + ' term ' + term + ' from destination-port ' + destination_port])
             if protocol is not None:
                 device.config(command_list=['set firewall family ' + family + ' filter ' + filtername + ' term ' + term + ' from protocol ' + protocol])
             if precedence is not None:
                 device.config(command_list=['set firewall family ' + family + ' filter ' + filtername + ' term ' + term + ' from precedence ' + precedence])
             if dscp is not None:
                 device.config(command_list=['set firewall family ' + family + ' filter ' + filtername + ' term ' + term + ' from dscp ' + dscp])
             for temp in action:
                device.config(command_list=['set firewall family ' + family + ' filter ' + filtername + ' term ' + term + ' then ' +temp ]) 
    if commit:
         return device.commit(timeout=60)
    else:
        return True




def apply_firewall_filter(filtername=None, device=None, interface=None, unit=None, direction=None, family=None, commit=False):
    """
    Apply filrewall filter

    :Example:

    python: apply_firewall_filter(filtername="router", device=router_handle, interface=ge-0/0/1)

    robot: apply firewall filter     filtername=router    device=router_handle    interface=ge-0/0/1

    :param str filtername:
        **REQUIRED** filtername  Ex. name = "router"
    :param Device device:
        **REQUIRED** device handler
    :param str interface:
        **REQUIRED** interface name from device to host. Ex. ge-0/0/1
    :param int unit numeber:
        *OPTIONAL* provide valid system service. Ex. default = "0"
    :param str direction:
        *OPTIONAL* provide valid protocol. Ex. default = "input"
    :param str family:
        *OPTIONAL* provide valid protocol. Ex. default = "inet"
    :return:
        * ``True`` when filter configuration is committed
    :raises Exception: when mandatory parameter is missing
    :param bool commit:
        *OPTIONAL* provide if commit is needed. Ex. default = "False"
    :return:
        * ``True`` when applying firewall configuration is committed or not committed

    """
    if device is None:
        raise Exception("'device' is mandatory parameter "
                        "for configuring basic  firewall filter- device handle")


    if filtername is None:
        device.log(level="ERROR", msg="'filtername' is mandatory parameter for configuring basic firewall filter")
        raise Exception("'filtername' is mandatory parameter for configuring basic firewall filter")
    if interface is None:
        device.log(level="ERROR", msg="'interface' is mandatory "
                                      "parameter for configuring basic filter")
        raise Exception("'interface' is mandatory parameter for "
                        "configuring basic filter - interface name for device to "
                        "host")
    if unit is None:
        unit = 0;
    if direction is None:
        direction = "input";
    if family is None:
        family = "inet";

    if filtername is not None and device is not None and interface is not None and direction is not None and  family is not None: 
         device.config(command_list=['set interfaces ' +interface+ ' unit ' +unit+ ' family ' +family+ ' filter  '+direction+ ' ' +filtername ])
    if commit:
        return device.commit(timeout=60)
    else:
        return True


