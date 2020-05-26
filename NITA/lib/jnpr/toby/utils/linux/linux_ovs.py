"""
Keywords/Functions to fetch OVS Information from Linux Device
"""
import re

#=========================================================================
#
#         FILE:  linux_ovs.py
#  DESCRIPTION:  Keywords to fetch information from OVS
#       AUTHOR:  Sudhir V R Akondi (sudhira)
#      COMPANY:  Juniper Networks
#      VERSION:  1.0
#=========================================================================


def extract_ports_in_ovs_bridge(device_handle, bridge_name):

    """
    To extract information on ports/interfaces that are part of an OVS bridge
    Example:
        extract_ports_in_ovs_bridge(device_handle=linux, bridge_name='ovs-sys-br')

    Robot Example:
        Extract Ports In OVS Bridge    device_handle=${linux}  bridge_name=ovs-sys-br

    :param str device_handle:
      **REQUIRED** Device Handle pointing to the Linux Device

    :param str bridge_name:
      **REQUIRED** Name of the OVS bridge

    :return: Tuple containing status and a dictionary of ports as keys and vlan/mode info as values.
    e.g.
        status : True if bridge was found and ports were listed, else False
        dict = {
                 '<port-1>'  : {
                                'mode' : access/trunk
                                'vlan' : list of vlans
                               }
               }
    """
    _return_dict_ = {}

    if bridge_name == "":
        raise Exception("Empty Bridge Name argument in extract_ports_in_ovs_bridge")

    try:
        _cmd_ = "ovs-vsctl show"
        _tmp_ = device_handle.shell(command=_cmd_)
        _output_ = _tmp_.response()
    except Exception as exception:
        raise Exception("extract_ports_in_ovs_bridge: %s : %s" %(type(exception), exception))

    try:
        _bridge_ = False
        _port_ = None
        _bridge_found_ = False
        for _row_ in _output_.split("\n"):

            _match_ = re.match(r"\s+Bridge\s+(\S+)", _row_)
            if _match_ is not None:
                _tmp_bridge_ = _match_.group(1)
                _tmp_bridge_ = _tmp_bridge_.replace("\"", "")
                if _tmp_bridge_ == bridge_name:
                    device_handle.log(level='DEBUG', message="Bridge: %s found" % bridge_name)
                    _bridge_ = True
                    _bridge_found_ = True
                else:
                    _bridge_ = False

                continue

            _match_ = re.match(r"\s+Port\s+\"(\S+)\"", _row_)
            if _match_ is not None and \
                _bridge_ is True:
                _port_ = _match_.group(1)
                _port_ = str(_port_)
                device_handle.log(level='DEBUG', message="Port %s found in bridge" % _port_)
                _return_dict_[_port_] = {}
                continue

            _match_ = re.match(r"\s+Port\s+(\S+)", _row_)
            if _match_ is not None and \
                _bridge_ is True:
                _port_ = _match_.group(1)
                _port_ = str(_port_)
                device_handle.log(level='DEBUG', message="Port %s found in bridge" % _port_)
                _return_dict_[_port_] = {}
                continue

            _match_ = re.match(r"\s+(\S+):\s(.*)", _row_)
            if _match_ is not None and \
                    _bridge_ is True and \
                    _port_ is not None:
                _item_ = _match_.group(1)
                _value_ = _match_.group(2)

                _value_ = _value_.replace("[", "")
                _value_ = _value_.replace("]", "")
                _value_ = _value_.replace(" ", "")
                _value_ = _value_.rstrip()

                if _item_ == "trunks":
                    _vlan_list_ = _value_.split(",")
                    device_handle.log(level='DEBUG', message="Value: %s, Vlans: %s on port: %s, Mode: Trunk"
                                      % (_value_, _vlan_list_, _port_))
                    if "mode" in _return_dict_[_port_].keys():
                        _return_dict_[_port_]["native_vlan"] = _return_dict_[_port_]["vlan"][0]
                    _return_dict_[_port_]["mode"] = "trunk"
                    _return_dict_[_port_]["vlan"] = []
                    _return_dict_[_port_]["vlan"] += _vlan_list_
                elif _item_ == "tag":
                    device_handle.log(level='DEBUG', message="Value: %s, Vlans: %s on port: %s, Mode: Access"
                                      % (_value_, _value_, _port_))
                    _return_dict_[_port_]["mode"] = "access"
                    _return_dict_[_port_]["vlan"] = [_value_]
                elif _item_ == "type":
                    _return_dict_[_port_]["type"] = _value_
                elif _item_ != "ovs_version":
                    device_handle.log(level='DEBUG', message="Unknown port attribute: %s found in output"
                                      % _item_)

    except Exception as exception:
        raise Exception("extract_ports_in_ovs_bridge: %s : %s" %(type(exception), exception))

    if _bridge_found_ is False:
        raise Exception("No bridge with name: %s found" % bridge_name)

    if _bridge_found_ is True and len(_return_dict_.keys()) == 0:
        device_handle.log(level="INFO", message="No ports found under bridge: %s" % bridge_name)
        return True, {}

    return True, _return_dict_

def check_ports_in_bridge(device_handle, port, bridge_name):

    """
    To verify if the given ports are part of an OVS bridge or not.
    Example:
        check_ports_in_bridge(device_handle=_dh_, port='vjunos0_em1', bridge_name='ovs-sys-br')

    Robot Example:
        Check Ports In Bridge   device_handle=${linux}   port=vjunos0_em1   bridge_name=ovs-sys-br

    :param str device_handle:
      **REQUIRED** Device handle pointing to the Linux host

    :param str/list port:
      **REQUIRED** port name or a list of port names

    :param str bridge_name:
      **REQUIRED** Name of the OVS Bridge
    """

    try:
        device_handle.log(level='INFO', message="Verifying if port: %s are part of ovs bridge: %s on device: %s"
                          % (port, bridge_name, device_handle))

        _ports_list_ = []
        if type(port) is str:
            _ports_list_.append(port)
        elif type(port) is list:
            _ports_list_ += port
        else:
            raise Exception("Unknown format of argument port: %s" % port)

        _status_, _ovs_ports_list_ = extract_ports_in_ovs_bridge(device_handle, bridge_name)
        if _status_ is False:
            raise Exception("Error in fetching ports that are part of OVS bridge: %s" % bridge_name)

        _flag_ = True
        for _p_ in _ports_list_:

            _p_ = str(_p_)
            if _p_ in _ovs_ports_list_.keys():
                device_handle.log(level='DEBUG', message="Port: %s is present in OVS Bridge: %s" % (_p_, bridge_name))
            else:
                device_handle.log(level='DEBUG', message="Port: %s is NOT present in OVS Bridge: %s" % (_p_, bridge_name))
                _flag_ = False

        if _flag_ is False:
            raise Exception("One or more ports not found as expected in OVS bridge")

        device_handle.log(level='INFO', message="All ports verified to be found in OVS bridge")
        return True

    except Exception as _exception_:
        raise Exception("Exception found in extract_ports_in_ovs_bridge. : %s : %s" % (type(_exception_), _exception_))

def check_port_info_in_bridge(device_handle, port, bridge_name, mode, vlan):

    """
    To verify the vlan properties of port(s) on an OVS bridge w.r.t mode and vlan membership
    Example:
        check_port_info_in_bridge(device_handle=_dh_, port='vjunos0_em1', bridge_name='ovs-sys-br', mode='access', vlan='101')
        check_port_info_in_bridge(device_handle=_dh_, port=['port-1', 'port-2'], bridge_name='ovs-sys-br', mode='trunk', vlan='11')
        check_port_info_in_bridge(device_handle=_dh_, port='vjunos0_em1', bridge_name='ovs-sys-br', mode='trunk', vlan=[14, 15, 4001])

    Robot Example:
        Check Port Info In Bridge    device_handle=${linux}  port=vjunos0_em1   bridge_name=ovs-sys-br   mode=access   vlan=101

        ${ports_list}                Create List   port-1    port-2
        Check Port Info In Bridge    device_handle=${linux}  port=${ports_list}   bridge_name=ovs-sys-br   mode=trunk    vlan=11

        ${vlans_list}                Create List   15    15   4001
        Check Port Info In Bridge    device_handle=${linux}  port=vjunos0_em1   bridge_name=ovs-sys-br   mode=native   vlan=${vlans_list}

    :param str device_handle:
      **REQUIRED** Device Handle pointing to the Linux Device

    :param str/list port:
      **REQUIRED** Port Name or a List of Port Names

    :param str bridge_name:
      **REQUIRED** Name of the OVS bridge

    :param str mode:
      **REQUIRED** Interface Mode i.e. access / trunk

    :param str/list vlan:
      **REQUIRED** Vlan Id or List of Vlan Ids

    """
    try:
        device_handle.log(level='INFO', message="Verifying Port Info for: %s on Bridge: %s, Mode: %s, Vlan: %s"
                          %(port, bridge_name, mode, vlan))

        _ports_list_ = []
        if type(port) is str:
            _ports_list_.append(port)
        elif type(port) is list:
            _ports_list_ += port
        else:
            raise Exception("Unknown format of argument port: %s" % port)

        _vlan_list_ = []
        if type(vlan) is str:
            _vlan_list_.append(vlan)
        elif type(vlan) is list:
            _vlan_list_ += vlan
        else:
            raise Exception("Unknown format of argument port: %s" % vlan)

        _status_, _ovs_ports_list_ = extract_ports_in_ovs_bridge(device_handle, bridge_name)
        if _status_ is False:
            raise Exception("Error in fetching ports that are part of OVS bridge: %s" % bridge_name)

        _flag_ = True
        for _p_ in _ports_list_:

            _p_ = str(_p_)
            device_handle.log(level='DEBUG', message="Looking for info on Port: %s" % _p_)
            if _p_ not in _ovs_ports_list_.keys():
                device_handle.log(level='ERROR', message="Port: %s is NOT present in OVS Bridge: %s" % (_p_, bridge_name))
                _flag_ = False

            if mode != "":
                if "mode" not in _ovs_ports_list_[_p_].keys():
                    device_handle.log(level='ERROR', message="Attribute 'mode' not found for port: %s" % _p_)
                    _flag_ = False
                else:
                    device_handle.log(level='INFO', message="Attribute 'mode' for Port: %s. Expected: %s, Found: %s"
                                      %(_p_, mode, _ovs_ports_list_[_p_]["mode"]))
                    if _ovs_ports_list_[_p_]["mode"] != mode:
                        device_handle.log(level='ERROR', message="Mismatch in attribute 'mode'")
                        _flag_ = False
            else:
                device_handle.log(level='INFO', message="Mode is set to ''. Skipping mode check")

            if len(_vlan_list_) > 0:
                if "vlan" not in _ovs_ports_list_[_p_].keys():
                    device_handle.log(level='ERROR', message="Attribute 'vlan' not found for Port: %s" % _p_)
                    _flag_ = False
                else:
                    device_handle.log(level='INFO', message="Attribute 'vlan' for Port: %s. Expected: %s, Found: %s"
                                      %(_p_, vlan, _ovs_ports_list_[_p_]["vlan"]))

                    _vflag_ = True
                    for _exp_vlan_ in _vlan_list_:
                        if _exp_vlan_ not in _ovs_ports_list_[_p_]["vlan"]:
                            device_handle.log(level='ERROR', message="Port: %s not found in OVS Vlan: %s" % (_p_, _exp_vlan_))
                            _vflag_ = False

                    if _vflag_ is False:
                        device_handle.log(level='ERROR', message="Mismatch in attribute 'vlan'")
                        _flag_ = False
            else:
                device_handle.log(level='INFO', message="No Vlans to verify, skipping vlan membership check")

        if _flag_ is False:
            raise Exception("One or more ports not found as expected in OVS bridge")

        device_handle.log(level='INFO', message="All ports verified to be found in OVS bridge")
        return True

    except Exception as _exception_:
        raise Exception("Exception found in check_ports_in_bridge: %s : %s" % (type(_exception_), _exception_))

def fetch_ovs_interface_number(device_handle, bridge_name, intf_name):

    """
    Keyword to execute OVS command and find the port number assigned to an interface
    Example:
        fetch_ovs_interface_number(device_handle=_dh_, bridge_name='ovs-sys-br', intf_name='vjunos0_em1')

    Robot Example:
        Fetch OVS Interface Number    device_handle=${linux}   bridge_name=ovs-sys-br   intf_name=vjunos0_em1

    :param str device_handle:
      **REQUIRED** Device Handle

    :param str bridge_name:
      **REQUIRED** Name of the OVS Bridge

    :param str intf_name:
      **REQUIRED** Name of the OVS interface

    :return: Port Number corresponding to the OVS interface
    :rtype: integer
    """

    try:

        _cmd_ = "ovs-ofctl show %s | grep %s" %(bridge_name, intf_name)

        _tmp_ = device_handle.shell(command=_cmd_)
        _output_ = _tmp_.response()

        for _row_ in _output_.split("\n"):
            _match_ = re.match(r"\s+(\d+)\(.*", _row_)
            if _match_ is not None:
                return True, _match_.group(1)

        return False, None
    except Exception as _exception_:
        raise Exception("Exception found in find_ovs_interface_number: %s : %s" % (type(_exception_), _exception_))
