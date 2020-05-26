"""
Keywords/Functions for Junos Utilities
"""
from robot.libraries.BuiltIn import BuiltIn
from copy import deepcopy
import re
from lxml import etree

#=========================================================================
#
#         FILE:  junos_utils.py
#  DESCRIPTION:  Keywords for junos utilities
#       AUTHOR:  Sudhir V R Akondi (sudhira)
#      COMPANY:  Juniper Networks
#      VERSION:  1.0
#=========================================================================

def get_updated_system_dictionary(resource, user="", password="", connect_channel="all", os="junos"):

    """
    Function to get the system dictionary for a resource listed in the topology yaml
    and update its elements with the new username , password and connect_method

    :param str resource: 
      **REQUIRED** Name of the resource as listed in the params file
  
    :param str user:
      **OPTIONAL** User Name for login
 
    :param str password:
      **OPTIONAL** Password for the user

    :param str connect_channel:
      **OPTIONAL** text / pyez / all
    """

    try:

        _init_obj_ = BuiltIn().get_library_instance("init")

        _dict_ = deepcopy(_init_obj_.get_t(resource=resource))

        # if username defined, update it
        if user != "":
            _dict_['controllers']['re0']['user'] = user

        if password != "":
            _dict_['controllers']['re0']['password'] = password

        if connect_channel != "all" and os.upper() == "JUNOS":
            _dict_['controllers']['re0']['connect_channels'] = connect_channel

        _system_dict_ = {}
        _system_dict_['primary'] = _dict_

        return _system_dict_

    except Exception as _exception_:
      raise Exception("Exception Raised in get_updated_system_dictionary: %s : %s" %(type(_exception_),_exception_))

def get_xml_equivalent_of_set_commands(device_handle, commands):

    """
    Python function to get the xml equivalent of a list of set commands from a Junos Device.
    Modus operandi for execution is to apply the set commands on the Junos device in config
    mode and run 'show | compare | display xml' to get the xml config. Followed by a rollback 0
    to leave the candidate configuration untouched.

    :params str device_handle:
        Handle to the Junos Device

    :params list cmd_list:
        List of Set Commands

    :returns: 
      XML string containing the equivalent configuration

    Python Example:
      commands = [
          "set system hostname test-hostname",
          "set system ntp server 10.204.195.50",
      ]
      r0_h         init.get_handle(resource="r0")
      xml_config = get_xml_equivalent_of_set_commands(device_handle=r0_h, cmd_list=commands)

    Robot Example:

      ${cmds}    Create List
                 ...   set system hostname test-hostname
                 ...   set system ntp server 10.204.195.50
      ${r0}      Get Handle   resource=r0
      ${xml}     Get XML Equivalent Of Set Commands   device_handle=${r0}   cmd_list=${cmds}
    """

    try:

        if device_handle is None or commands is None:
            raise Exception("Mandatory argument missing !")

        device_handle.config(command_list=commands)
    
        _cmd_ = ["show | compare | display xml"]
        _response_ = device_handle.config(command_list=_cmd_).response()
        t.log('INFO', "XML: %s" % str(_response_))
    
        _rollback_ = ["rollback 0"]
        device_handle.config(command_list=_rollback_)
    
        _match_ = re.match(r".*\<configuration\>(.*)\<\/configuration\>.*", str(_response_), re.MULTILINE|re.DOTALL)
        if _match_ is None:
            raise Exception("Response does not contain Configuration XML element")

        _xml_string_ = "<configuration>%s</configuration>" % _match_.group(1)

        return _xml_string_
    
    except Exception as _exception_:
      raise Exception("Exception Raised in get_xml_equivalent_of_set_commands: %s : %s" %(type(_exception_),_exception_))



def get_junos_pid(device=None, process_name=None):
    """
    To get the PID, of the corresponding Processes in Juniper Box

    Example:
        get_junos_pid(device=dut, process_name=["/usr/sbin/chassisd", "/usr/sbin/alarmd"])
    ROBOT Example:
        Get Junos PID    device=${dut}    process_name=${p_list}

    :param str device:
        **REQUIRED** Device handle of the DUT.
    :param list process_name:
        **REQUIRED** List of the process names whose PID is required. Even a single process needs
        to be passed in a list
    :return: Dictionary (key-> process names, value->PID). PID returned is 0 if it is not running
    :rtype: dict
    """
    if device is None:
        raise ValueError("device is a mandatory argument")

    if process_name is None:
        device.log(level="ERROR", message="Process_name is a mandatory argument")
        raise ValueError("Process_name is a mandatory argument")

    status = device.cli(command="show system processes").response().splitlines()
    dict_to_return = {}

    for x in process_name:
        found_flag = 0
        for y in status:
            match = re.search("\s*([0-9]+).*" + x, y, re.DOTALL)
            if match:
                found_flag = 1
                dict_to_return[x] = match.group(1)
                break
        if found_flag == 0:
            dict_to_return[x] = "0"
            device.log(level="ERROR", message="Following process is not running : " + x)

    return dict_to_return

def get_equivalent_rpc(device=None, command=None):
    """
    To get the xml rpc equivalent to a Junos cli command.

    Example:
      Python:
        xml_rpc = get_equivalent_rpc(device=dh, command="show version")

      Robot:
        ${xml_rpc}   Get Equivalent RPC   device=${dh}   command=show version

    :param str device:
        **REQUIRED** Device Handle to the Junos DUT

    :param str command:
        **REQUIRED** CLI Command 

    :return: String containing the xml rpc equivalent of the cli command
    :rtype str:
    """

    if device is None:
        raise ValueError("device is a mandatory argument")

    if command is None:
        raise ValueError("command is a mandatory argument")

    try:
        _xml_rpc_ = device.get_rpc_equivalent(command=command)
    except Exception as err:
        raise Exception("Exception raised in get_equivalent_rpc: %s : %s" %(type(err), err))

    # display_xml_rpc returns bytes, convert to string
    #_xml_rpc_ = _xml_rpc_.decode("utf-8")
    return _xml_rpc_

def extract_rpc_and_arguments_from_command(device=None, command=None):
    """
    """

    try:

        _rpc_ = get_equivalent_rpc(device=device, command=command)
        _xml_rpc_ = etree.fromstring(_rpc_)

        _rpc_ = _xml_rpc_.tag
        _args_xml_list_ = list(_xml_rpc_)
        _arg_dict_ = {}
        for _arg_ in _args_xml_list_:
            _arg_dict_[_arg_.tag] = _arg_.text

        return _rpc_, _arg_dict_

    except Exception as err:
        raise Exception("Exception raised in extract_rpc_and_arguments_from_command: %s : %s" %(type(err), err))

