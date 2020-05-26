# coding: UTF-8
# pylint: disable=import-outside-toplevel

"""
Device factory class and ROBOT keywords functions
"""
# import sys
# import os as OS
import re
import copy
import importlib
import inspect
import jxmlease
import lxml
import json
from jnpr.toby.hldcl.device_data import DeviceData
from jnpr.toby.exception.toby_exception import TobyException

GET_FUNCTION_NAME = lambda: inspect.stack()[1][3]
PPRINT = lambda x: json.dumps(x, indent=4, sort_keys=True, default=str, ensure_ascii=False)


class Device(object):
    """
    Device factory class and wrapper function for ROBOT keywords
    Creates objects according to os(JunOS/Linux/IOS)
    and environment(Python/JAAS)

    """

    def __new__(cls, host=None, system=None, os='JUNOS', user=None,
                password=None, model=None, connect_dual_re=False,
                connect_mode='ssh', ssh_key_file=None, port=None,
                connect_targets='management', connect_complex_system=False,
                kill_sessions='yes',
                proxy_host=None, proxy_user=None, proxy_password=None,
                proxy_port=None, text_port=None, pyez_port=None, timeout=30, global_logger=True, device_logger=True):

        """
        Parameters if 'host' argument is used
        :param host:
            **REQUIRED** host-name or IP address of target device
        :param os:
            *OPTIONAL* Operating System of device. Default is JUNOS
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param password:
            *OPTIONAL* Login Password. If not provided will be derived from
            Toby framework defaults.
        :param model:
            *OPTIONAL* Model of device. Default is None.
        :param connect_dual_re:
            *OPTIONAL* Connect to both the RE's. Default is False. Will return
            object which is connected to master RE.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Supported values
            are telnet/ssh/netconf/console.
            Default is ssh. For Windows device, default is telnet.
        :param ssh_key_file:
            *OPTIONAL*  ssh_key_file to connect to device
            if connect_mode is ssh.
        :param connect_targets:
            *OPTIONAL* Connect to either console or management. Default is
            management. Supported values are console/management.
        :param kill_sessions:
            *OPTIONAL* Kills existing console sessions.
            Default is 'yes'. Supported values are 'yes'/'no'.
        :param port:
            *OPTIONAL* Port on device to which connection needs to made.
            Default is 22 for ssh, 23 for telnet, 830 for netconf
        :param proxy_host:
            **REQUIRED** hostname or IP address of the proxy.
        :param proxy_user:
            *OPTIONAL* Login user name of the proxy.
        :param proxy_password:
            *OPTIONAL* Login Password of the proxy.
        :param proxy_port:
            *OPTIONAL* Port on device to which connection
            needs to made to the proxy. Default: port=22
        :param timeout:
            *OPTIONAL* Time by which connection to device
            established(pyEZ timeout). Default is 30 seconds.

        Parameters if 'system' argument is used. All other options IGNORED!!
        :param system:
            **REQUIRED** dictionary of system 'block' from 't'
        :return: Model specific System object
        """

        # Check for t and fail if not present
        try:
            t
        except NameError:
            raise TobyException("You are trying to use Toby without Initializing"
                                " it. Please call toby_initialize/Toby "
                                "Initialize(robot) to get Toby Initialize!!")

        # See if system data is present, or fetch it from device

#        if (user is None and (password is not None and ssh_key_file is not
#                              None)) or (user is not None and (
#                                  password is None and ssh_key_file is None)):
#            raise TobyException("Arguments user and password/ssh_key_file must "
#                                "be both present or both absent!!")

        system_data = dict()
        system_data['system'] = dict()
        osname = os

        if host and not system:
            controller = None
            if osname.lower() == "junos":
                controller = 're0'
            else:
                controller = 'controller'

            system_data['system']['primary'] = dict()
            system_data['system']['primary']['name'] = host
            system_data['system']['primary']['model'] = model
            system_data['system']['primary']['osname'] = osname
            system_data['system']['primary']['controllers'] = dict()
            sys_controler = system_data['system']['primary']['controllers']
            sys_controler[controller] = dict()
            sys_controler[controller]['name'] = host
            sys_controler[controller]['connect'] = True
            if connect_targets == 'console':
                sys_controler[controller]['con-ip'] = host
            else:
                sys_controler[controller]['mgt-ip'] = host
            sys_controler[controller]['model'] = model
            sys_controler[controller]['osname'] = osname
            sys_controler[controller]['connect_mode'] = connect_mode
            sys_controler[controller]['ssh_key_file'] = ssh_key_file
            sys_controler[controller]['user'] = user
            sys_controler[controller]['password'] = password
            sys_controler[controller]['timeout'] = timeout
            if proxy_host is not None:
                sys_controler[controller]['proxy_host'] = proxy_host
                sys_controler[controller]['proxy_port'] = proxy_port
                sys_controler[controller]['proxy_user'] = proxy_user
                sys_controler[controller]['proxy_password'] = proxy_password
                if not model:
                    raise TobyException("'model' parameter is missing. "
                                        "It is mandatory for proxy ssh")

            if text_port is not None:
                text_port = int(text_port)
                sys_controler[controller]['text_port'] = text_port
            if pyez_port is not None:
                pyez_port = int(pyez_port)
                sys_controler[controller]['pyez_port'] = pyez_port

            # JUNOS 'sweeping' of additional information
            if osname.lower() == 'junos' and not model:
                if connect_targets == 'console':
                    raise TobyException("'model' parameter is missing. It is mandatory for console connection")
                dev_data = DeviceData(
                    host=host, user=user, password=password,
                    os=osname, port=port, pyez_port=pyez_port)
                if connect_complex_system and connect_dual_re:
                    system_data['system'] = dev_data.system_facts()
                else:
                    system_data['system']['primary']['model'] = \
                        dev_data.get_model()
                dev_data.close()

        elif system:
            system_data['system'] = copy.deepcopy(system)
        else:
            raise TobyException("Either 'system' parameter or 'host' are mandatory")

        # Insert argument information into system_data where appropriate
        # Will be pruned as data becomes available in yaml
        for system_node in system_data['system'].keys():
            if host:
                system_data['system'][system_node]['connect'] = bool(
                    connect_complex_system or
                    host == system_data['system'][system_node]['name'] or
                    host == system_data['system'][system_node]['mgt-ip'])

            if 'controllers' not in system_data['system'][system_node].keys() \
                    or len(system_data['system'][system_node]['controllers']) == 0:
                raise TobyException("Atleast one 'controllers' should exist in node '" + system_node + "'")

            sys_node_ctl = system_data['system'][system_node]['controllers']
            for controller in sys_node_ctl.keys():
                if 'user' not in sys_node_ctl[controller]:
                    sys_node_ctl[controller]['user'] = user
                if 'password' not in sys_node_ctl[controller]:
                    sys_node_ctl[controller]['password'] = password
                if 'connect_targets' not in sys_node_ctl[controller]:
                    sys_node_ctl[controller]['connect_targets'] = \
                        connect_targets
                if 'kill_sessions' not in sys_node_ctl[controller]:
                    sys_node_ctl[controller]['kill_sessions'] = \
                        kill_sessions
                if 'connect_mode' not in sys_node_ctl[controller]:
                    sys_node_ctl[controller]['connect_mode'] = connect_mode
                    sys_node_ctl[controller]['ssh_key_file'] = ssh_key_file
                if 'timeout' not in sys_node_ctl[controller]:
                    sys_node_ctl[controller]['timeout'] = timeout

                sys_node_ctl[controller]['model'] = \
                    system_data['system'][system_node]['model']

                # if connect_targets contains console then set connect_mode to
                # telnet, need to remove this later when there is 'ssh' support
                if 'console' in sys_node_ctl[controller]['connect_targets']:
                    sys_node_ctl[controller]['connect_mode'] = 'telnet'

                if 'mgt-ip' in sys_node_ctl[controller]:
                    sys_node_ctl[controller]['mgt-ip'] = \
                        re.sub(r'\/\d+', '',
                               sys_node_ctl[controller]['mgt-ip'])
                    sys_node_ctl[controller]['host'] = \
                        sys_node_ctl[controller]['mgt-ip']
                elif 'con-ip' in sys_node_ctl[controller]:
                    sys_node_ctl[controller]['con-ip'] = \
                        re.sub(r'\/\d+', '',
                               sys_node_ctl[controller]['con-ip'])
                    sys_node_ctl[controller]['host'] = \
                        sys_node_ctl[controller]['con-ip']
                elif 'hostname' in sys_node_ctl[controller] and \
                        'domain' in sys_node_ctl[controller]:
                    sys_node_ctl[controller]['host'] = \
                        sys_node_ctl[controller]['hostname'] + "." + \
                        sys_node_ctl[controller]['domain']
                else:
                    sys_node_ctl[controller]['host'] = \
                        sys_node_ctl[controller]['hostname']

                if connect_dual_re:
                    sys_node_ctl[controller]['connect'] = True

                if (host or system) and (port is not None):
                    sys_node_ctl[controller]['port'] = port
                if (host or system) and (pyez_port is not None):
                    pyez_port = int(pyez_port)
                    sys_node_ctl[controller]['pyez_port'] = pyez_port

                if (host or system) and (text_port is not None):
                    text_port = int(text_port)
                    sys_node_ctl[controller]['text_port'] = text_port

                if system_data['system'][system_node]['osname'].lower() \
                        == 'windows':
                    if 'fv-connect-transport' in system_data['system'][system_node] and  \
                       system_data['system'][system_node]['fv-connect-transport'] is not None:
                        sys_node_ctl[controller]['connect_mode'] = \
                            system_data['system'][system_node]['fv-connect-transport']
                    else:
                        sys_node_ctl[controller]['connect_mode'] = 'telnet'
                sys_node_ctl[controller]['global_logging'] = global_logger
                sys_node_ctl[controller]['device_logging'] = device_logger

        # Now that system_data is set and normalized based on different input
        # approaches, instantiate proper object
        if not system_data['system']['primary']['osname']:
            raise TobyException("No OS specified")

        PPRINT(system_data)
        osname_device = system_data['system']['primary']['osname'].upper()
        if osname_device == 'JUNOS':
            model_device = str(system_data['system']['primary']['model']).lower()

            if re.match(r"srx|vsrx|csrx|ha_cluster", model_device):
                from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem
                return SrxSystem(system_data)

            if re.match(r"mx|vmx", model_device):
                from jnpr.toby.hldcl.juniper.routing.mxsystem import MxSystem
                return MxSystem(system_data)

            if re.match(r"qfx", model_device):
                from jnpr.toby.hldcl.juniper.switching.qfxsystem import QfxSystem
                return QfxSystem(system_data)

            if re.match(r"ex", model_device):
                from jnpr.toby.hldcl.juniper.switching.exsystem import ExSystem
                return ExSystem(system_data)

            if re.match(r"nfx", model_device):
                from jnpr.toby.hldcl.juniper.security.nfxsystem import NfxSystem
                return NfxSystem(system_data)

            from jnpr.toby.hldcl.juniper.junipersystem import JuniperSystem
            return JuniperSystem(system_data)

        elif osname_device in ("UNIX", "LINUX", "CENTOS", "FREEBSD", "UBUNTU", "SIFOS-LINUX"):
            if 'warp17' in system_data['system']['primary']:
                from jnpr.toby.hldcl.trafficgen.warp17.warp17 import Warp17
                return Warp17(system_data=system_data)

            from jnpr.toby.hldcl.system import System
            return System(system_data)

        elif osname_device == 'IOS':
            from jnpr.toby.hldcl.cisco.ciscosystem import CiscoSystem
            return CiscoSystem(system_data)

        elif osname_device == 'BROCADE':
            from jnpr.toby.hldcl.brocade.brocadesystem import BrocadeSystem
            return BrocadeSystem(system_data)

        elif osname_device == 'SRC':
            from jnpr.toby.hldcl.src.srcsystem import SrcSystem
            return SrcSystem(system_data)

        elif osname_device == 'SPIRENT':
            if 'avalanche' in system_data['system']['primary']:
                from jnpr.toby.hldcl.trafficgen.avalanche.avalanche import Avalanche
                return Avalanche(system_data=system_data)

            if 'landslide-manager' in system_data['system']['primary']:
                from jnpr.toby.hldcl.trafficgen.spirent.landslide import Landslide
                return Landslide(system_data=system_data)

            from jnpr.toby.hldcl.trafficgen.spirent.spirent import Spirent
            return Spirent(system_data=system_data)

        elif osname_device == 'PARAGON':
            from jnpr.toby.hldcl.trafficgen.calnex.paragon import Paragon
            return Paragon(system_data=system_data)

        elif osname_device == 'IXVERIWAVE':
            from jnpr.toby.hldcl.trafficgen.ixia.ixveriwave import IxVeriwave
            return IxVeriwave(system_data=system_data)

        elif osname_device.startswith('IX'):
            if 'ixload' in system_data['system']['primary']:
                from jnpr.toby.hldcl.trafficgen.ixia.ixload import IxLoad
                return IxLoad(system_data=system_data)

            from jnpr.toby.hldcl.trafficgen.ixia.ixia import Ixia
            return Ixia(system_data=system_data)

        elif osname_device in ('BREAKINGPOINT', 'BPS'):
            from jnpr.toby.hldcl.trafficgen.breakingpoint.breakingpoint import Breakingpoint
            return Breakingpoint(system_data=system_data)

        elif osname_device == 'ELEVATE':
            from jnpr.toby.hldcl.trafficgen.spirent.elevate import Elevate
            return Elevate(system_data=system_data)

        elif osname_device == 'WINDOWS':
            from jnpr.toby.hldcl.system import System
            return System(system_data)

        else:
            raise TobyException("OS is not supported " + system_data['system']['primary']['osname'])

def _verify_method(device, method):
    """
        Verify the method exists for the given object since this is a factory function set for
        different types of device objects.
        :param device:
            *MANDATORY* Device object
        :param method:
            *MANDATORY* Method call that you wish to validate
    """
    method_call = getattr(device, method, None)
    if method_call is None:
        parent_function = inspect.stack()[1][3]
        raise TobyException("A Device of type " + type(device).__name__ + " does not support " + parent_function, host_obj=device)

def connect_to_device(*args, **kwargs):
    """
    'Connect To Device' is used to connect to a specific device (management or console).

    DESCRIPTION:
        'Connect To Device' is used to connect to a specific device (management or console).
        Things like user and password can be specified, among other parameters listed down
        below in the arguments section. This keyword allows you to make specific connections
        that may otherwise not have been established during initialization.

    ARGUMENTS:
        [args, kwargs]
        :param STR host:
            *MANDATORY* host-name or IP address of target device.
        :param STR os:
            *OPTIONAL* Operating System of device. Default is JUNOS
        :param STR user:
            *OPTIONAL* Login user name. If not provided will be derived from Toby framework defaults.
        :param STR password:
            *OPTIONAL* Login Password. If not provided will be derived from Toby framework defaults.
        :paramSTR  model:
            *OPTIONAL/MANDATORY* Model of device. MANDATORY for Non Junos devices.Default is None.
        :param STR connect_dual_re:
            *OPTIONAL* Connect to both the RE's. Default is False.
            Will return object which is connected to master RE.
        :param STR connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet.
            Supported values are telnet/ssh/netconf
        :param INT timeout:
            *OPTIONAL* Time by which connection to device
            established(pyEZ timeout). Default is 30 seconds.
        :param STR connect_targets:
            *OPTIONAL* Connect to either console or management.
            Default is management. Supported values are console/management.
        :param STR kill_sessions:
            *OPTIONAL* Kills existing console sessions.
            Default is 'yes'. Supported values are 'yes'/'no'.
        :param STR port:
            *OPTIONAL* Port on device to which connection needs to made.

    ROBOT USAGE:
        EX1. : Simple connection to a device:
        ${device-handle} =    Connect to device   host=10.10.10.10

        EX2. : Connecting to a device with a different username and password:
        ${device-handle} =    Connect to device   host=10.10.10.10   user=test
        ...    password=test123

        EX3. : Connecting to a device with an OS other than JUNOS:
        ${device-handle} =    Connect to device   host=10.10.10.10   os=linux

        EX4. : If you are connecting to console some of the optional requirements become mandatory.
        When connecting to a JUNOS device, model is required because console connection
        cannot use RPC like management connections to obtain model info. For all connections
        you must specify connect_targets=console so that it does not connect to PyEZ and so
        it uses telnet (currently console connection only supports telnet). Below are some
        examples:

        ${device} =    Connect to device   host=10.10.10.10   model=mx240   connect_targets=console

        EX5. : Here we still want to dictate os name so that we know it is not JUNOS (default) therefore
        not requiring the model info.

        ${device} =    Connect to device   host=10.10.10.10   os=linux   user=test  password=test123
        ...   connect_targets=console
        ${device} =    Connect to device   host=10.10.10.10   os=cisco   connect_targets=console

    :returns: Device object based on os and model
    """
    return_value = Device(*args, **kwargs)
    return return_value


def add_channel_to_device(device, channel_type, system_node='current',
                          controller='current', channel_attributes=None):
    """
    Add new Channel to Device Object

    ARGUMENTS:
        [device, channel_type, system_node='current',Bcontroller='current', channel_attributes=None]

        :param STR device:
            *MANDATORY* Device handle on which Channel needs to be added
        :param STR channel_type:
            *MANDATORY* Type to channel to create , currently supports snmp, grpc only
        :param STR system_node:
            *OPTIONAL* Node to create the channel, Default to current
        :param STR controller:
            *OPTIONAL* Controller to create the channel, Default to current
        :param STR channel_attributes:
            *OPTIONAL* Arguments required for creating the channel

             Following are the list of supported optional channel attributes
             when channel_type = grpc :
             rhandle       : router(device) handle
              (or)
             host          : router's hostname

             (if host is supplied then user/password is mandatory)
             user          : username for router login,
             password      : login password,
                             defaults to lab supplied non-root password

             port          : grpc server port on router, defaults to 50051
             channel_id    : unique channel name,
                 defaults to auto-computed based on pid +  timestamp
             timeout       : time to wait for command execution,
                             defaults to 300s
             grpc_lib_path : centralized path where GRPC service libraries
                are located defaults to /volume/regressions/grpc_lib/latest

    ROBOT USAGE:
        EX 1.  ${device-handle} =  Get Handle    resource=r1
        {channel_id} =  add channel to device    device=${device-handle}    channel=cli

        EX 2.   ${device-handle} =  Get Handle    resource=r1
                ${dict} =     Create Dictionary      timeout=${100}    auth_type=none
                            ....  auth_pass=none      priv_type=none     priv_pass=none
                Add Channel To Device  device=${r0}  channel_type=snmp   channel_attributes=${dict}

    :return: Id of the channel created
    """
    _verify_method(device, 'add_channel')
    return_value = device.add_channel(channel_type, system_node, controller, channel_attributes)
    return return_value


def add_mode(device, mode=None, origin='shell', command=None, pattern=None, exit_command=None, targets=None):
    """
    'Add Mode' is used to create custom modes

    DESCRIPTION:
        'Add Mode' is used to create custom modes that contain user defined steps to
        enter and exit modes that are not supported natively (such as CLI, shell, vty) by Toby.

    ARGUMENTS:
        [device, mode=None, origin='shell', command=None, pattern=None, exit_command=None, targets=None]
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR mode:
            *MANDATORY* Name of the custom mode. This can be any string that will later be
                        reference by 'Execute Command on Device' as a
                        parameter to enter said mode.
        :param STR origin:
            *OPTIONAL* This is the starting mode from which the custom mode is entered. By
                        default this value is set to 'shell', but 'cli' is also
                        an option that is available.
        :param STR command:
            *MANDATORY* Command by which to enter custom mode. This can be one simple command
                        or one command in a list of commands that eventually gets the
                        user into their custom mode.e.g. 'start shell', 'vnc', 'vty'
        :param STR pattern:
            *MANDATORY* Pattern to be expected after giving command. The prompt or line that is
                        expected after issuing one of the steps in entering the custom mode.
                        e.g. '>', '#', 'user%'
        :param STR exit_command:
            *MANDATORY* Command to exit out of the mode. When the user wishes to exit the custom mode
                        (or one its layers) they need to provide the appropriate command to do so.
                        e.g 'exit', 'quit', 'q'
        :param LIST targets:
            *OPTIONAL* Used to pass more than one target. Only required if more than one
                    target is used. If used, then the previous arguments are not required except
                    for device and mode. However for each target (read: step) the user needs
                    to provide the 'command', 'pattern', and 'exit_command' as a dictionary which
                    then is eventually passed as a list


    ROBOT USAGE:
        If going into the mode only requires one step then just provide one
        set of command/pattern/exit_command along with the custom mode name.

        Add Mode  device=${device-handle}  mode=custom name
        ...  command=request chassis satellite login fpc-slot 101
        ...  pattern=$    exit_command=quit

        If going into the mode requires more than on step, the user needs to create X
        targets that each contain a dictionary of command/pattern/exit_command where
        X is the number of steps it takes to reach the custom mode. That list of
        targets need to be passed in order to 'Add Mode' with the custom mode name.

        &{target1} =    Create Dictionary
        ...  command=request chassis satellite login fpc-slot 101
        ...  pattern=$    exit_command=quit

        &{target2} =    Create Dictionary    command=vnc 123
        ...  pattern=#    exit_command=exit

        @{targets} =    Create List    ${target1}    ${target2}

        Add Mode  device=${device-handle}  mode=custom name
        ...   targets=${targets}

        If the custom mode needs to be entered from 'cli' rather than the default 'shell'
        this can be set using the optional 'origin' parameter as such.

        Add Mode  device=${device-handle}  mode=custom name origin=cli
        ...   targets=${targets}

    :returns: True if succesfully adds more, otherwise raises an Exception.

    RELATED KEYWORDS:
        execute_command_on_device()
    """
    _verify_method(device, 'add_mode')
    return_value = device.add_mode(mode=mode, origin=origin, command=command, pattern=pattern,
                                   exit_command=exit_command, targets=targets)
    return return_value

def execute_command_on_device(device, mode=None, command=None, timeout=60, pattern=None):
    """
    It is to be used with keyword 'Add Mode' to execute commands in custom modes properly

    DESCRIPTION:
        'Execute command on device' is to be used with keyword 'Add Mode' to execute
        commands in custom modes properly. This keyword ensures stability of Toby's
        state machine by starting in shell mode and carefully entering a custom mode and
        then exiting said custom mode after it has executed the proper command.

    ARGUMENTS:
        [device, mode=None, command=None, timeout=60, pattern=None]
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR mode:
            *MANDATORY* Mode in which the command is to be executed. This is defined by
                        they keyword 'Add Mode' which creates different custom modes to be
                        used throughout user's script. e.g. 'custom1, custom2, etc.'
                        These can be any name the user wants and are a list of predefined
                        steps to enter/exit the custom mode.
        :param STR command:
            *MANDATORY* The command to be executed. This can be a variety of commands that
                        the user wants to run on their device. Similar to how they may issue
                        'ls' in shell mode or 'show interfaces' in CLI, the user can provide
                        the command they would normally enter manually in the terminal.
        :param INT timeout:
            *OPTIONAL* Time by which response should be received. Default is 60 seconds.
                        This happens if the pattern expected for the command is not met
                        in the timeout value set. Generally, after a command is issued the
                        device returns to some sort of prompt. Often if a command hangs or
                        does not complete properly, it does not return to the prompt and this
                        value is so that it does not hang Indefinitely. Other values can be
                        30 seconds, 120 seconds (2 minutes)
        :param STR pattern:
            *OPTIONAL* Overrides the default pattern to look for. Default is the last
                        target's pattern set in the custom mode. This is the pattern that
                        the command expects after its completion (usually some prompt) and
                        if it does not see this it will eventually time out.
                        e.g. '>' - commonly found in CLI mode, '#' or '$' '%' often found in
                        shell mode or any other symbol or string that one may encounter in
                        whichever mode they are

    ROBOT USAGE:
        Here ${dh0} is the device handle to be passed. Refer to 'Get Handle' for
        more information. The mode attribute value (custom1, custom2) is defined by 'Add Mode' keyword
        (refer to that for more information as well).

        Ex. 1: Executing 'ls' command on custom mode 'custom1'.
        ${response} =  Execute command on device  ${dh0}  mode=custom1  command=ls

        Ex. 2: Pass a custom timeout value instead of the default 60 seconds if the
        command needs more time.
        ${response} =  Execute command on device  ${dh0}  mode=custom1  command=show version
        ...  timeout=${120}

        Ex. 3: If the command being issued will result in returning to something different
        than the custom mode's prompt, the user can pass a different pattern.
        ${response} =  Execute command on device  ${dh0}  mode=custom1  command=show version
        ...  timeout=${120}   pattern=device~#

    :returns:
        Output of the command in a response string.

    RELATED KEYWORDS:
        add_mode()
        execute_cli_command_on_device()
        execute_config_command_on_device()
        execute_shell_command_on_device()
        execute_vty_command_on_device()
        execute_cty_command_on_device()
        execute_rpc_command_on_device()
        execute_pyez_command_on_device()
        execute_grpc_api()
    """
    _verify_method(device, 'execute_command')
    return_value = device.execute_command(mode=mode, command=command, timeout=timeout, pattern=pattern).response()
    return return_value

def execute_cli_command_on_device(device, *args, **kwargs):
    """
    'Execute CLI Command on Device' is a keyword used to execute commands on the CLI of a device.

    ARGUMENTS:
        [device, *args, **kwargs]
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR|LIST|TUPLE command:
            *MANDATORY* Single or list of multiple CLI command to execute
        :param INT|STR timeout:
            *OPTIONAL* Time by which response should be received. Default is set to 60.
        :param STR pattern:
            *OPTIONAL* Overrides the default pattern to look for after command returns.
            Default is set to Toby-process_id-host>
        :param STR format:
            *OPTIONAL* "text" or "xml" for output format. Default is set to text
        :param STR channel:
            *OPTIONAL* "text" or "pyez" that send command by SSH or PYEZ channel.
                        Default is set to text
        :param BOOLEAN raw_output:
            *OPTIONAL* Returns raw output of the command. Default is set to `False`
        :param BOOLEAN strip_xml_output:
            *OPTIONAL* Sometimes command response have illegal output for XML,
                        this option will strip all illegal string that only return
                        response between <rpc-reply> and </rpc-reply>.Default is set to `True`
        :param BOOLEAN xml_to_dict:
            *OPTIONAL* Transit XML output to Python DICT and return. Default is set to `False`
        :param BOOLEAN carriage_return:
            *OPTIONAL* By passing argument, toby adds carriage return (i.e. '\r')
                        at the end of command.Default is set to `Ture`
        :param BOOLEAN print_response:
            *OPTIONAL* Print this function return value to stdout for debuging.
                         Default is set to `False`

    ROBOT USAGE:
        User needs to pass the device handle and a command or list of commands.

        Ex1 :
        ${response} =   Execute CLI Command On Device     device=${device-handle}   command=show version

        Ex2:
        @{cmds}     Create List
        ...             show version
        ...             show chassis fpc pic-status
        ${last_cmd_response} =      Execute CLI Command On Device   device=${device-handle}     command=${cmds}

        Pass a timeout if the command will take longer than the default 60 seconds. Provide a pattern
        if user expects one different than the default cli prompt.

        Ex3:
        ${response} =   Execute CLI Command On Device     device=${device-handle}   command=show interfaces
        ...             timeout=${100}    pattern=~

        In case the user wants XML format instead there are various options to help with that.
        Use 'format' to change the response from text to XML. Use strip_xml_output in case the
        XML output has some extraneous text in the response. Use xml_to_dict to translate the
        XML output to a python dict and return that.

        Ex4:
        ${response} =   Execute CLI Command On Device     device=${device-handle}   command=show interfaces
        ...             format=xml    xml_to_dict=${TRUE}

        ${response} =   Execute CLI Command On Device     device=${device-handle}   command=show interfaces
        ...             format=xml    strip_xml_output=${FALSE}

        To change the channel which the command is sent through, user can override the default 'text' (ssh/telnet)
        to 'pyez'. The user can also include the full output without the command truncated by setting raw_output to 'True'.
        To have a whole printout of this response and the function it came from to the console set print_response to 'True'.

        Ex5:
        ${response} =   Execute CLI Command On Device     device=${device-handle}   command=show interfaces
        ...             channel=pyez    raw_output=${TRUE}   print_response=${TRUE}

        returns:
            For single command, return output of this command. Multiple commands only return the last command's output

            If format=text and channel=text or pyez, send command by SSH or NETCONF and get plaintext response.

            If format=text, channel=text or pyez, and xml_to_dict=True, send command by SSH or NETCONF and command
            response transit to Python DICT. If command response is not XML string, just return plaintext response.

            If format=xml and channel=text, send command by SSH and command response plaintext XML string.
            If option xml_to_dict=${TRUE}, will transit XML String to Python DICT

            If format=xml and channel=pyez, send command by NETCONF and command response transited to XML OBJECT.
            If option xml_to_dict=${TRUE}, will transit XML Object to Python DICT

    RELATED KEYWORDS:
        execute_command_on_device()
        execute_config_command_on_device()
        execute_shell_command_on_device()
        execute_vty_command_on_device()
        execute_cty_command_on_device()
        execute_rpc_command_on_device()
        execute_pyez_command_on_device()
        execute_grpc_api()
    """
    kwargs = copy.deepcopy(kwargs)

    if "command" not in kwargs:
        raise TobyException("Mandatory argument 'command' is missing!")

    # option "timeout" support INT or STR that can be transited to INT
    if "timeout" in kwargs:
        kwargs["timeout"] = int(kwargs["timeout"])

    # option "command" support STR, LIST and TUPLE
    if isinstance(kwargs["command"], str):
        cmd_list = (kwargs["command"], )
    elif isinstance(kwargs["command"], (list, tuple)):
        cmd_list = kwargs["command"]
    else:
        raise TobyException("'command' option must be a STR, LIST or TUPLE but got '{}'".format(type(kwargs["command"])))

    xml_to_dict = kwargs.pop("xml_to_dict", False)
    strip_xml_output = kwargs.pop("strip_xml_output", True)
    print_response = kwargs.pop("print_response", False)
    kwargs['kw_call'] = True

    # debug info
    device.log(message="send command:\n{}".format(PPRINT(cmd_list)), level="DEBUG")

    _verify_method(device, 'cli')
    for cmd in cmd_list:
        kwargs["command"] = cmd
        return_value = device.cli(*args, **kwargs).response()

    # checking last cmd's response whether be XML object, it may transit to Python DICT later
    response_type = None
    if isinstance(return_value, lxml.etree._Element):
        response_type = "xml_object"
    else:
        response_type = "string"

    # device XML plaintext output may have illegal string, strip if needed
    if strip_xml_output is True and response_type == "string":
        match = re.search(r"(\<rpc\-reply.*\<\/rpc\-reply\>)", str(return_value), re.S)
        if match:
            return_value = match.group(1)

    if xml_to_dict is True:
        if response_type == "xml_object":
            return_value = jxmlease.parse_etree(return_value)
        else:
            if re.search(r"\<\/rpc\-reply\>", return_value):
                return_value = jxmlease.parse(return_value)

    # print function return value for debuging
    if print_response is True:
        if isinstance(return_value, str):
            device.log(message="Function '{}' return value:\n{}".format(GET_FUNCTION_NAME(), return_value), level="INFO")
        else:
            device.log(message="Function '{}' return value:\n{}".format(GET_FUNCTION_NAME(), PPRINT(return_value)), level="INFO")

    return return_value


def execute_config_command_on_device(device, *args, **kwargs):
    """
    'Execute Config Command on Device' allows the user to issue one or more config

    DESCRIPTION:
        'Execute Config Command on Device' allows the user to issue one or more config
        commands on Junos devices, and commit them as well.

    ARGUMENTS:
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                         proper device resource (can be r0, h0, etc.)
        :param STR|LIST|TUPLE command_list:
            *OPTIONAL* Single or list of multiple CONFIG command to execute
        :param STR|LIST|TUPLE command:
            *MANDATORY* Alias of command_list to instead it that provide compatible interface
                        to send cmd to cli/conf/shell/vty.
        :param STR mode:
            *OPTIONAL* Mode of configuration. Default is None which means configure mode.
                       Supported values are 'exclusive' and 'private'.Default is set to None.
        :param BOOLEAN raw_output:
            *OPTIONAL* Returns raw output of the command. Default is set to `False`.
        :param BOOLEAN get_response:
            *OPTIONAL* If set True, will return STRING value which contain command response.
                        Default is set to `True`.
        :param BOOLEAN carriage_return:
            *OPTIONAL* By passing argument, toby adds carriage return (i.e. '\r') at the end of command.
                       Default is set to True
           Behaviors:

            get_response = True && commit = False:

                - Return last cmd's result. For negative testing, it can get error msg

            get_response = True && commit = True

                - reboot_if_need option worked only in this scenario. This will send cmd
                  to device and return commit string response. If device need to reboot, return
                  commit string after rebooting.

            get_response = False && commit = False

                - Just send cmd to device but not commit. Return True/False to indicate command whether send success

            get_response = False && commit = True

                - Return True/False to indicate whether commit success.

           Default: True
        :param BOOLEAN commit:
            *OPTIONAL* If set True, will send cmd to device and commit. Default is set to `False`.
        :param BOOLEAN detail:
            *OPTIONAL* This is only worked if commit=True. If detail=True, commit detail info
                       (include each module check output) will return. default is set to `False`
        :param BOOLEAN reboot_if_need:
            *OPTIONAL* If set True, it means get_response=True and commit=True, method will check commit
                        response whether have rebooting tips to reboot and reconnect DUT if needed.
                        For HA topo, will reboot 2 nodes in parallel. Default is set to `False`.
        :param STR|REGEXP reboot_keyword:
            *OPTIONAL* If reboot_if_need is True, will commit configuration automatically and loop checking
                       several reboot keywords from commit response. Due to internal combined keyword list
                       may not catch all reboot situations. This option customize reboot keyword by STR or
                       re.compile() object. Default is set to None
        :param BOOLEAN print_response:
            *OPTIONAL* Whether print device response to stdout. Default is set to `False`
        :param INT|STR timeout:
            *OPTIONAL* Command commit timeout.Default is set to 300

    ROBOT USAGE:
        User needs to pass the device handle and a command or list of commands.

        Ex. 1:
        ${response} = Execute Config Command on Device  device=${device-handle}
        ...  command_list=['set system services netconf ssh', 'set system services netconf ssh']

        The user can specify the mode of configuration they wish to enter, and return the raw output
        if they wish (it won't remove the command and extraneous text like '[edit]'). By default
        it returns only the response.

        Ex. 2:
        ${response} = Execute Config Command on Device  device=${device-handle}
        ...  command_list=['set system services netconf ssh', 'set system services netconf ssh']
        ...  mode=private  raw_output=${TRUE}

        To commit the config use the ‘commit’ option. A custom timeout value with ‘commit’ can be
        specified with ‘timeout’ option.

        Ex. 3:
        ${response} = Execute Config Command on Device  device=${device-handle}
        ...  command_list=['set system services netconf ssh', 'set system services netconf ssh']
        ...  commit=${TRUE}  detail=${TRUE}  timeout=${600}

        By default, the last config command's result is returned. By setting 'get_response' to
        false the user gets back indication of command's success as True or False. If the user sets 'commit'
        to true then they get the commit's result. Please read about 'get_response' under the
        ARGUMENTS section for more details.

        Ex. 4:
        # This will give the user True/False based on if the commit succedeed or not.
        ${response} = Execute Config Command on Device  device=${device-handle}
        ...  command_list=['set system services netconf ssh', 'set system services netconf ssh']
        ...  commit=${TRUE}  get_response=${FALSE}

        # This will give the user True/False based on if the config commands succeeded.
        ${response} = Execute Config Command on Device  device=${device-handle}
        ...  command_list=['set system services netconf ssh', 'set system services netconf ssh']
        ...  get_response=${FALSE}

        If the user knows or thinks some config will require reboot, they can set 'reboot_if_need' to
        be true and it will reboot the DUT if the response calls for it. This only works if get_response
        and commit are both true. There are a set of patterns it expects by default, but if they want to
        provide their own pattern(s) they can do that as well with reboot_keyword which takes string(s)
        or regexp. In addition they can print out the response in any scenario to stdout with print_response
        set to true.

        Ex. 5:
        ${response} = Execute Config Command on Device  device=${device-handle}
        ...  command_list=['set system services netconf ssh', 'set system services netconf ssh']
        ...  commit=${TRUE}   reboot_if_need=${TRUE}  reboot_keyword=Please reboot device

        ${response} = Execute Config Command on Device  device=${device-handle}
        ...  command_list=['set system services netconf ssh', 'set system services netconf ssh']
        ...  commit=${TRUE}   reboot_if_need=${TRUE}  print_response=${TRUE}

        For any further details on the arguments please check the appropriate parameter in the
        'ARGUMENTS' section.

    :return: Separated in each options

    RELATED KEYWORDS:
        execute_command_on_device()
        execute_cli_command_on_device()
        execute_shell_command_on_device()
        execute_vty_command_on_device()
        execute_cty_command_on_device()
        execute_rpc_command_on_device()
        execute_pyez_command_on_device()
        execute_grpc_api()
    """
    options = copy.deepcopy(kwargs)
    options["get_response"] = kwargs.pop("get_response", True)
    options["commit"] = kwargs.pop("commit", False)
    options["timeout"] = int(kwargs.get("timeout", 300))
    options["detail"] = kwargs.pop("detail", False)
    options["reboot_if_need"] = kwargs.pop("reboot_if_need", False)
    options["reboot_keyword"] = kwargs.pop("reboot_keyword", None)
    options["print_response"] = kwargs.pop("print_response", False)
    kwargs['kw_call'] = True

    # New option "command" have higher priority
    if "command" in kwargs:
        kwargs["command_list"] = kwargs["command"]

    if "command_list" not in kwargs:
        raise TobyException("Mandatory argument 'command' or 'command_list' is missing!")

    # option "command_list" support STR, LIST and TUPLE
    if isinstance(kwargs["command_list"], str):
        kwargs["command_list"] = [kwargs["command_list"], ]
    elif isinstance(kwargs["command_list"], (list, tuple)):
        # deepcopy to avoid change user command
        kwargs["command_list"] = list(copy.deepcopy(kwargs["command_list"]))
    else:
        raise TobyException("'command' or 'command_list' option must be a STR, LIST or TUPLE but got '{}'".format(type(kwargs["command_list"])))

    if "timeout" in kwargs:
        kwargs["timeout"] = int(kwargs["timeout"])

    if options["reboot_if_need"] is True:
        options["get_response"] = True
        options["commit"] = True

    # debug info
    device.log(message="send command:\n{}".format(PPRINT(kwargs["command_list"])), level="DEBUG")

    _verify_method(device, 'config')
    response = device.config(*args, **kwargs)
    if options["commit"] is True:
        response = device.commit(timeout=options["timeout"], detail=options["detail"])

    if options["get_response"] is True:
        return_value = response.response()
    else:
        return_value = response.status()

    # make sure whether need reboot device
    if options["reboot_if_need"] is True:
        need_reboot = False

        if options["reboot_keyword"] is None:
            reboot_keyword_pattern_list = (
                re.compile(r"must reboot the system"),
                re.compile(r"need to reboot"),
                re.compile(r"Multitenancy mode is changed\s+.*Must reboot"),
                re.compile(r"reboot the device"),
            )
        else:
            reboot_keyword_pattern_list = (options["reboot_keyword"], )

        for pattern in reboot_keyword_pattern_list:
            if re.search(pattern, return_value):
                need_reboot = True
                break

        # if reboot succeed, just return before rebooting's commit response
        if need_reboot:
            reboot_options = {"device": device, }
            if device.is_ha() is True:
                reboot_options["all"] = True

            device.log(message=" START REBOOTING {} ".format(device).upper().center(80, r"="), level="INFO")
            if reboot_device(**reboot_options) is False:
                return_value = False

    if options["print_response"] is True:
        device.log(message="Function '{}' return value:\n{}".format(GET_FUNCTION_NAME(), return_value), level="INFO")

    return return_value


def execute_shell_command_on_device(device, *args, **kwargs):
    """
    TO execute a command on the shell mode of a device.

    DESCRIPTION:
        'Execute Shell Command on Device' is used to execute a command on the shell
        mode of a device. It provides back a response of the command that is issued.

    ARGUMENTS:
        [device, *args, **kwargs]
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR|LIST|TUPLE command:
            *MANDATORY* Single or LIST of CLI command to execute.
        :param STR|INT timeout:
            *OPTIONAL* Time by which response should be received. Default is set to 60.
        :param STR pattern:
            *OPTIONAL* Overrides the default pattern to look for after command returns.
                        Default is set to Toby-process_id-host%
        :param BOOLEAN raw_output:
            *OPTIONAL* Returns raw output of the command. Default is set to `False`
        :param BOOLEAN print_response:
            *OPTIONAL* Whether print device response to stdout. Default is set to `False`
        :param BOOLEAN carriage_return:
            *OPTIONAL* By passing argument, toby adds carriage return (i.e. '\r') at the end
                       of command. Default is set to `True`.

    ROBOT USAGE:
        User needs to pass the device handle and a command or list of commands.

        Ex. 1:
        ${response} =  Execute Shell Command on Device  device=${device-handle}
        ...            command=mkdir temp

        User can pass a single command to this keyword, or a list of commands.

        Ex. 2:
        ${response} =   Execute Shell Command On Device     device=${device-handle}   command=show version

        Example:
        @{cmds}     Create List
        ...         mkdir temp
        ...         date
        ${last_cmd_response} =      Execute Shell Command On Device   device=${device-handle}     command=${cmds}

        Pass a timeout and/or pattern to override the defaults (default for pattern is the shell's
        Toby prompt set in Initialization)

        Ex. 3:
        ${response} =   Execute Shell Command On Device     device=${device-handle}   command=telnet fpc0
        ...             timeout=${60}    pattern=~

        The raw output (meaning the command issued is not removed from the response) can be obtained by setting
        'raw_output' to true. The user can see the response printed straight to the console by setting 'print_response'
        to true.

        Ex. 4:
        ${response} =   Execute Shell Command On Device     device=${device-handle}   command=ls -ltr
        ...             raw_output=${TRUE}    print_response=${TRUE}


    :return:**Last** command output

    RELATED KEYWORDS:
        execute_command_on_device()
        execute_cli_command_on_device()
        execute_config_command_on_device()
        execute_vty_command_on_device()
        execute_cty_command_on_device()
        execute_rpc_command_on_device()
        execute_pyez_command_on_device()
        execute_grpc_api()
    """
    options = {}
    options["print_response"] = kwargs.pop("print_response", False)

    if "timeout" in kwargs:
        kwargs["timeout"] = int(kwargs["timeout"])
    kwargs['kw_call'] = True

    if isinstance(kwargs["command"], str):
        cmd_list = [kwargs["command"], ]
    elif isinstance(kwargs["command"], (list, tuple)):
        cmd_list = list(copy.deepcopy(kwargs["command"]))
    else:
        raise TobyException("option 'command' must be a STR, LIST or TUPLE but got '{}'".format(type(kwargs["command"])))

    _verify_method(device, 'shell')

    # debug info
    device.log(message="send command:\n{}".format(PPRINT(cmd_list)), level="DEBUG")

    return_value = ""
    for cmd in cmd_list:
        kwargs["command"] = cmd
        return_value = device.shell(*args, **kwargs).response()

    if options["print_response"] is True:
        device.log(message="Function '{}' return value:\n{}".format(GET_FUNCTION_NAME(), return_value), level="INFO")

    return return_value

def reboot_device(device, wait=0, mode='shell', timeout=480, interval=20, all=False, device_type=None, system_nodes=None, **kwargs):
    """Reboot device

    ARGUMENTS:
        [device, wait=0, mode='shell', timeout=480, interval=20, all=False, device_type=None, system_nodes=None, **kwargs]
        :param OBJECT device:
            *MANDATORY* Device handler of device.
        :param INT|STR wait:
            *OPTIONAL* Time to sleep before reconnecting. Default is set to 0.
        :param STR mode:
            *OPTIONAL* Mode in which reboot needs to be executed. Default is set to 'shell'.
                       Also supports 'cli'. mode=cli is valid only for Junos devices.
        :param INT|STR timeout:
            *OPTIONAL* Timeout to reboot and reconnect device. Default is set to 480.
        :param INT|STR interval:
            *OPTIONAL* Interval at which reconnect need to be attempted after reboot is performed.
                        Default is set to 20.
        :param BOOLEAN all:
            *OPTIONAL* Valid only if the device is of Junos. When set to True, all
                        JUNOS REs are rebooted simultaneously. Default is False, where only
                        the current RE is rebooted. If the OS is not JUNOS,
                        all=True raises a TobyException.
        :param STR device_type:
            *OPTIONAL* This option works only with 'text' channel. Value should be set to 'vmhost' to reboot the vmhost
        :param STR system_nodes:
            *OPTIONAL* Values which can be passed: all-members, local, member1,member2...member n  etc can be passed .
                        Initial phase supports only for QFX series. For other models it is not yet supported.

    ROBOT USAGE:
        EX 1:${device-handle} =   Get Handle   resource=r1
             ${reconnect_re} =  Reboot Device        device=${device-handle}          wait=${120}
                ....              mode=cli       timeout=${480}        all=${False}

        Ex 2: ${device-handle} =   Get Handle   resource=r1
              ${reconnect_re} =  Reboot Device        device=${device-handle}          wait=${120}
                .....           mode=cli       timeout=${480}        all=${True}

        Ex 3: ${device-handle} =   Get Handle   resource=r1
              ${reconnect_re} =  Reboot Device        device=${device-handle}          wait=${120}
                .....           mode=cli       timeout=${480}

    :return:True if device is rebooted and reconnection is successful, else an Exception is raised.
    """
    _verify_method(device, 'reboot')
    wait = int(wait)
    interval = int(interval)
    timeout = int(timeout)

    return_value = device.reboot(
        wait=wait,
        mode=mode,
        timeout=timeout,
        interval=interval,
        all=all,
        device_type=device_type,
        system_nodes=system_nodes,
        **kwargs,
    )

    if device.current_node.current_controller.tag_name:
        tag_name = device.current_node.current_controller.tag_name
        mapped_system = t.get_system(resource=device.current_node.current_controller.tag_name)
        if 'associated_devices' in mapped_system['primary']:
            for asso_device in mapped_system['primary']['associated_devices']:
                dev = t.get_handle(resource=asso_device)
                t.log(level='INFO', message="Reconnecting Device: " + asso_device)
                dev.reconnect(timeout=timeout)
    return return_value


def close_device_handle(device, *args, **kwargs):
    """
    Close the device handle.

    DOCUMANTATION:
        Close connection to device and destroys the object.
        For an ssh proxy connection, it is mandatory to close
        the connection using this method.

    ARGUMENTS:
        [device, *args, **kwargs]
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
            be obtained by using the keyword 'Get Handle' and specifying the proper device
            resource (can be r0, h0, etc.)

    ROBOT USAGE:
        Close device handle  device=${device-handle}

    returns: True if device is reconnection closed,else an Exception is raised.
    """
    _verify_method(device, 'close')
    return_value = device.close(*args, **kwargs)
    return return_value


def software_install(device, *args, **kwrgs):
    """
    Install Software.

    ARGUMENTS:
        [args,kwargs]
        :param STR package:
            *OPTIONAL* The file-path to the install package tarball
            on the local filesystem
        :param STR pkg_set:
            *OPTIONAL* The file-paths as list/tuple of the install package
            tarballs on the local filesystem which will be installed on
            mixed VC setup.
        :param STR remote_path:
            *OPTIONAL* Time to reboot and connect to device.
            Default is 360 seconds
        :param BOOLEAN progress:
            *OPTIONAL* If set to ``True``, it uses :meth:`sw.progress`
            for basic reporting by default.
        :param STR validate:
            *OPTIONAL* MD5 hexdigest of the package file
        :param STR checksum:
            *OPTIONAL* MD5 hexdigest of the package file
        :param BOOLEAN cleanfs:
            *OPTIONAL* When ``True`` will perform a 'storeage cleanup' before
            SCP'ing the file to device. Default to True
        :param BOOLEAN no_copy:
            *OPTIONAL* When ``True`` the software package will not be SCP'd
            to the device. Default is False
        :param INT timeout:
            *OPTIONAL* Timueout for upgrade

    ROBOT USAGE:
        Software install   device=${device-handle}    no_copy=$true}
    ...    no_copy=${True}  progress=${True}   timeout=${9000}

    :returns: True if software upgrade is successful,
        else an Exception is raised
    """
    _verify_method(device, 'software_install')
    return_value = device.software_install(*args, **kwrgs)
    return return_value


def issu_upgrade(device, *args, **kwargs):
    """
    This enables you to upgrade between two different Junos OS releases with minimal disruption.

    ARGUMENST:
        [device, **kwargs]
        :param STR package:
            *OPTIONAL* The file-path to the install package tarball on the local filesystem
        :param STR pkg_set:
            *OPTIONAL* The file-paths as list/tuple of the install package
                        tarballs on the local filesystem which will be installed on
                        mixed VC setup.
        :param STR remote_path:
            *OPTIONAL* Time to reboot and connect to device.
                Default is set to 360 seconds
        :param BOOLEAN progress:
            *OPTIONAL* If set to ``True``, it uses :meth:`sw.progress`
                      for basic reporting by default.
        :param STR validate:
            *OPTIONAL* MD5 hexdigest of the package file.
        :param STR checksum:
            *OPTIONAL* MD5 hexdigest of the package file.
        :param BOOLEAN cleanfs:
            *OPTIONAL* When ``True`` will perform a 'storeage cleanup' before
                    SCP'ing the file to device. Default to True
        :param BOOLEAN no_copy:
            *OPTIONAL* When ``True`` the software package will not be SCP'd
                    to the device. Default is False
        :param INT timeout:
            *OPTIONAL* Timueout for upgrade

    ROBOT USAGE:
        issu upgrade    device=${device-handle}

    :returns: True if software upgrade is successful, else an Exception is raised.

    """
    _verify_method(device, 'software_install')
    kwargs['issu'] = True
    return_value = device.software_install(*args, **kwargs)
    return return_value


def powercycle(device, timeout=300):
    """
    powercycle   device=${device-handle}

        :param device:
            *MANDATORY* The device handle which needs to be powercycled
        :param timeout:
            *OPTIONAL* The default timeout is 300, This is max time
            it waits for reconnection to be successfull

        :Returns: True if powercycle is successful,
        else an Exception is raised
    """
    _verify_method(device, 'powercycle')
    return_value = device.powercycle(timeout=timeout)
    return return_value


def reconnect_to_device(device, *args, **kwargs):
    """
    Reconnects to JunOS device

    ARGUMENSTS:
        [timeout=30, interval=20, force=True]
        :param INT timeout:
            *OPTIONAL* Time till which reconnection can be attempted.
                      Defaultis 30 seconds.
        :param INT interval:
            *OPTIONAL* Interval in which reconnection needs to be
                    attempted.Default is 20 seconds.
        :param BOOLEAN force:
            *OPTIONAL* to force reconnect to the device
                        is already connected.Default is `True`
        :param interval:
            *OPTIONAL* Interval at which reconnect need to be attempted after
            reboot is performed. Default is 20 seconds.

    ROBOT USAGE:
        Reconnect to device    device=${device-handle}  interval=${80}
                ...  force=${True}   timeout=${100}

    :returns: True if device is reconnected successfully, else False
    """
    _verify_method(device, 'reconnect')
    return_value = device.reconnect(*args, **kwargs)
    return return_value


def disconnect_from_device(device, *args, **kwargs):
    """
    Disconnects connection to JunOS device.

    ARGUMENATS:
        [ignore_error=False]
        :param BOOLEAN ignore_error:
            *OPTIOANAL* disconnect device with error.
                        Default is set to False.

    ROBOT USAGE:
        Ex 1: Disconnect from device    device=${device-handle}
        Ex 2: Disconnect from device    device=${device-handle}
                                ...        ignore_error=${True}

    :returns:True if device is disconnected successfully,
            else an Exception is raised
    """
    _verify_method(device, 'disconnect')
    return_value = device.disconnect(*args, **kwargs)
    return return_value


def save_device_configuration(device, *args, **kwargs):
    """
    Save configuration on the device

    ARGUMENTS:
        [device, *args, **kwargs]
        :param STR file:
            *OPTIONAL* File name to save the configuration
        :param STR source:
            *OPTIONAL* Store running/candidate configuration.
                    Valid values are committed and candidate
        :param INT timeout:
            *OPTIONAL* Time given to save configuration to device.
                        Default is 60 seconds
        :param STR type:
            *OPTIONAL* Type of data in the dumped file.
                        Accepted values are 'normal'/'xml'/'set'.
                        Default is 'normal'

    ROBOT USAGE:

        Ex 1: Save device configuration    device=${device-handle}
        Ex 2: Save device configuration    device=${device-handle}     file=temp_config.conf
                source='candidate'   type='normal'        timeout=${60}

    :returns: True in case of success, else an Exception is raised
    """
    _verify_method(device, 'save_config')
    return_value = device.save_config(*args, **kwargs)
    return return_value


def load_device_configuration(device, *args, **kwargs):
    """
    Load configuration on devices.

    ARGUMENTS:
        [device]
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
            be obtained by using the keyword 'Get Handle' and specifying the proper device
            resource (can be r0, h0, etc.)
        :param args[0]:
            *OPTIONAL* The content to load. If the contents is a string,
            toby will attempt to automatically determine the format. If it is a
            list of strings, Toby will concatenate all to be loaded together.
        :param STR local_file:
            *OPTIONAL* Path to a config file on local server.
                       Default is set to None.
        :param STR remote_file:
            *OPTIONAL* Path to a config file on a remote server
            (on current device).Default is set to None.
        :param STR device_filename:
            *OPTIONAL* Dumps the configuration file on device with
            specified name. Default is '/var/tmp/toby_script_<timestamp>.conf'
        :param STR option:
            *OPTIONAL* Load Options. Supported values are 'merge',
            'replace', 'set', override'. Default is 'merge'.
             For set command strings and list of set command strings,
             use option='set'
        :param BOOLEAN commit:
            *OPTIONAL* Issue the 'commit' command after loading the configuration
             Supported values are:
              'False' : Default. Do not issue commit
              'True'  : issue commit once config is loaded successfully
        :param INT timeout:
            *OPTIONAL* Time by which response should be received.
                     Default is 60 seconds.

    ROBOT USAGE:
        Ex 1:Load device configuration    device=${device-handle}

        Ex 2:Load device configuration    local_file='my_config.set'    option='set'
                        ....       timeout=120

    returns: True in case configurtion is loaded successfully, else an Exception is raised.
    """
    _verify_method(device, 'load_config')
    return_value = device.load_config(*args, **kwargs)
    return return_value


def switch_to_superuser(device, **kwargs):
    """
    Switch to superuser.

    ARGUMENTS:
        [device, **kwargs]
        :param STR password:
            *OPTIONAL* Password of super user
        :param STR su_command:
            *OPTIONAL* command to switch to super user mode default is 'su -'

    ROBOT USAGE:
        Switch to superuser    device=${device-handle}

    :returns: True in case swicthed to super user mode,else an Exception is raised
    """
    _verify_method(device, 'su')
    return_value = device.su(**kwargs)
    return return_value


def execute_vty_command_on_device(device, command, destination, timeout=30,
                                  pattern=None, raw_output=False, **kwargs):
    """
        Executes vty command on the specified destination.

    ARGUMENTS:
        [device, command, destination, timeout=30,pattern=None, raw_output=False, **kwargs]

        :param STR command:
            *MANDATORY* VTY command to be executed.
        :param STR destination:
            *MANDATORY*  Destination to vty into. Example: fpc0
        :param INT timeout:
            *OPTIONAL*  Time by which response should be received. Default is set to 60 seconds
        :param STR pattern:
            *OPTIONAL* Overrides the default pattern to look for after command returns.
                        Default is set to 'vty.[a-zA-Z0-9]*#' (regexp)
        :param BOOLEAN raw_output:
            *OPTIONAL* Returns raw output of the command. Default is set to `False`.

    ROBOT USAGE:
        User needs provide the device handle, a command to be issued, and the
        destination of the vty mode they wish to execute in.

        Ex 1:
        ${response} =   Execute VTY Command On Device     device=${device-handle}   command=show syslog info
        ...             destination=fpc0

        Choose to provide a custom pattern in addition to the default which is 'vty.[a-zA-Z0-9]*#' (regexp)

        Ex 2:
        ${response} =   Execute VTY Command On Device     device=${device-handle}   command=show syslog info
        ...             destination=fpc0    pattern=vty-fpc0~

        In case the user wants the raw output (meaning the command is not removed from the response) they can set
        'raw_output' to true.

        Ex 3:
        ${response} =   Execute VTY Command On Device     device=${device-handle}   command=show syslog info
        ...             destination=fpc0    pattern=vty-fpc0~     raw_output=${TRUE}

    :return: Exception if vty fails, else vty command response

    RELATED KEYWORDS:
        execute_command_on_device()
        execute_shell_command_on_device()
        execute_cli_command_on_device()
        execute_config_command_on_device()
        execute_cty_command_on_device()
        execute_rpc_command_on_device()
        execute_pyez_command_on_device()
        execute_grpc_api()
    """
    _verify_method(device, 'vty')
    return_value = device.vty(command=command, destination=destination, timeout=timeout, pattern=pattern, raw_output=raw_output, **kwargs).response()
    return return_value


def execute_cty_command_on_device(device, command, destination, timeout=30,
                                  pattern=None, raw_output=False):
    """
    Executes cty command on the specified destination.

    ARGUMENTS:
        [device, command, destination, timeout=30,pattern=None, raw_output=False]
        :param STR command:
            **MANDATORY**  CTY command to be executed
        :param STR destination:
            **MANDATORY**  Destination to cty into. Example: fpc1
        :param INT timeout:
            **OPTIONAL**  Time by which response should be received. Default: 60 seconds
        :param STR pattern:
            *OPTIONAL* Overrides the default pattern to look for after command returns.
            Default: '[uart0.# ', r'-*\(more\)-*', '%']' (regexp)
        :param raw_output:
            *OPTIONAL* Returns raw output of the command. Default is False

    ROBOT USAGE:
        User needs provide the device handle, a command to be issued, and the
        destination of the cty mode they wish to execute in.

        Ex 1:
        ${response} =   Execute CTY Command On Device     device=${device-handle}   command=show msp service-sets
        ...             destination=fpc1

        User can hoose to provide a custom pattern in addition to the the default which
        is '[uart0.# ', r'-*\(more\)-*', '%']' (regexp)

        Ex 2:
        ${response} =   Execute CTY Command On Device     device=${device-handle}   command=show msp service-sets
        ...             destination=fpc1    pattern=cty-fpc1~

        In case the user wants the raw output (meaning the command is not removed from the response) they can set
        'raw_output' to true.

        Ex 3:
        ${response} =   Execute CTY Command On Device     device=${device-handle}   command=show msp service-sets
        ...             destination=fpc1    pattern=cty-fpc1~     raw_output=${TRUE}

    :return: Exception if cty fails, else cty command response

    RELATED KEYWORDS:
        execute_command_on_device()
        execute_shell_command_on_device()
        execute_cli_command_on_device()
        execute_config_command_on_device()
        execute_vty_command_on_device()
        execute_rpc_command_on_device()
        execute_pyez_command_on_device()
        execute_grpc_api()
    """
    _verify_method(device, 'cty')
    return_value = device.cty(command=command, destination=destination, timeout=timeout, pattern=pattern, raw_output=raw_output).response()
    return return_value


def get_current_controller_name(device):
    """
    Get the current controller name

    ARGUMENTS:
        [device]
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
            be obtained by using the keyword 'Get Handle' and specifying the proper device
            resource (can be r0, h0, etc.)

    ROBOT USAGE:
        Get Current Controller Name    ${device-handle}

    :retuen: return the current controller names
    """
    _verify_method(device, 'get_current_controller_name')
    return_value = device.get_current_controller_name()
    return return_value


def switch_re_master(device, **kwargs):
    """
    Switch re to master.

    ARGUMENTS:
        [device]
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
            be obtained by using the keyword 'Get Handle' and specifying the proper device
            resource (can be r0, h0, etc.)

    ROBOT USAGE:
        Switch re master   device=${device-handle}     retry=${True}

    :retuen: return re master
    """
    _verify_method(device, 'switch_re_master')
    return_value = device.switch_re_master(**kwargs)
    return return_value


def execute_rpc_command_on_device(device, **kwargs):
    """
    Execute rpc command on device by passing an XML element or xml-as-string.

    ARGUMENTS:
        [device, kwargs]
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
            be obtained by using the keyword 'Get Handle' and specifying the proper device
            resource (can be r0, h0, etc.)

        :param STR command:
            *MANDATORY* Executes an XML RPC on device. The command can either
            be an XML Element or xml-as-string.(rpc command)

        :param STR error_format:
            *OPTIONAL* error type to be displayed.Default is set to empty str

        :param func to_py':
          Is a caller provided function that takes the response and
          will convert the results to native python types.  all kvargs
          will be passed to this function as well in the form::
           to_py( self, rpc_rsp, **kvargs )

    ROBOT USAGE:
        User needs to provide the device handle as well as the command to be issued.

        Example:
        ${response} =     Execute Rpc Command on Device   device=${device-handle}
        ...               command=<get-software-information/>    error_format='LIST'


    :raises ValueError: When the **command** is of unknown origin

    :raises PermissionError:When the requested RPC command is not allowed due to
                            user-auth class privilege controls on Junos

    :raises RpcError: When an ``rpc-error`` element is contained in the RPC-reply

    :return: Object with the following methods response()': Response from the rpc command
            RPC-reply as XML object.  If **to_py** is provided, then
            that function is called, and return of that function is
            provided back to the caller; presumably to convert the XML to
            native python data-types (e.g. ``dict``).

    RELATED KEYWORDS:
        execute_command_on_device()
        execute_shell_command_on_device()
        execute_cli_command_on_device()
        execute_config_command_on_device()
        execute_vty_command_on_device()
        execute_cty_command_on_device()
        execute_pyez_command_on_device()
        execute_grpc_api()
    """
    _verify_method(device, 'execute_rpc')
    return_value = device.execute_rpc(**kwargs).response()
    return return_value


def get_rpc_equivalent(device, command):
    """
    Get rpc equivalent

    ARGUMENTS:
            [device, command]
        :param device:
            *MANDATORY* Device handle on which rpc commands
            needs to be executed
        :param command:
            *MANDATORY* any cli command.

    ROBOT USAGE:
        ${response} = Get rpc equivalent  device=${device-handle}    command=show version

    :return: get rpc equivalent command for given command.
    """

    _verify_method(device, 'get_rpc_equivalent')
    return_value = device.get_rpc_equivalent(command=command)
    return return_value

def execute_pyez_command_on_device(device, command, **kwargs):
    """
    Executes a pyez api call and returns results as lxml/etree

    ARGUMENTS:
        [device, command, **kwargs]
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR command:
            *MANDATORY* Executes a pyez method against the pyez Device object
        :param INR Timeout:
            *OPTIONAL* time to execute the command.Default is set to None.

    ROBOT USAGE:
        User needs to provide the device handle as well as the command to be issued.

        ${response} =    Execute Pyez Command on Device    device=${device-handle}
        ...              command=get-software-information

    :return: Response from the pyez command RPC-reply as lxml/etree object.

    RELATED KEYWORDS:
        execute_command_on_device()
        execute_shell_command_on_device()
        execute_cli_command_on_device()
        execute_config_command_on_device()
        execute_vty_command_on_device()
        execute_cty_command_on_device()
        execute_rpc_command_on_device()
        execute_grpc_api()
    """
    _verify_method(device, 'pyez')
    return_value = device.pyez(command=command, **kwargs).response()
    return return_value


def commit_configuration(device, **kwargs):
    """
    Configuration To be commited on Device.

    ARGUMENTS:
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR comment:
            *MANDATORY* If provided logs this comment with the commit.
        :param BOOLEAN confirm:
            *OPTIONAL* If provided activates confirm safeguard with provided
            value as timeout (minutes).
        :param INT timeout:
            *OPTIONAL* If provided the command will wait for completion using
                    the provided value as timeout (seconds).
                    By default the device timeout is used.
        :param STR sync:
            *OPTIONAL* On dual control plane systems, requests that the
                    candidate configuration on one control plane be copied to the
                    other control plane, checked for correct syntax, and committed
                    on both Routing Engines.
        :param STR force_sync:
            *MANDATORY* On dual control plane systems,
                        forces the candidate configuration on one control plane to
                        be copied to the other control plane.
        :param BOOLEAN check:
            *OPTIONAL* If True, executes commit check command and checks correctness
                        of syntax and do-not apply changes. If configuration
                        check-out fails then it raises an exception otherwise returns True
        :param BOOLEAN full:
            *MANDATORY* When true requires all the daemons to check
                        and evaluate the new configuration.
        :param BOOLEAN deatil:
            *MANDATORY* When true return commit detail as lxml object
        :param XML response:
            *MANDATORY* When true return commit as lxml object

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        Commit configuration    device=${device-handle} comment = commit successful
                       .....      full=${TRUE}    detail=${TRUE}    response=${TRUE}

    returns:  True if commit is successful, else an exception is raised
    """
    _verify_method(device, 'commit')
    return_value = device.commit(**kwargs)
    return return_value

def switchover_device(device, **kwargs):
    """
    This function use to switch between routing engine of IOS device

    ARGUMENTS:
        [device, **kwargs]
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR options:
            *OPTIONAL* options for switchover
        :param INT wait:
            *OPTIONAL* waiting time.Default is set to 180 sec
        :param INT timeout:
            *OPTIONAL* timeout in seconds.Default is set to 360 sec

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        Switchover device    device=${device-handle}

    :returns:True if the switchover is success.False if the switchover fails
    """
    _verify_method(device, 'switchover')
    return_value = device.switchover(**kwargs)
    return return_value

def upgrade_device(device, **kwargs):
    """
    Upgrade image for IOS device

    ARGUMENTS:
        [device, **kwargs]
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR url:
            *OPTIONAL* url of image (string). It can be inculed image or not
        :param STR image:
            *OPTIONAL* image to upgrade (string). If not defined, image have to
                    include in url
        :param INT timeout:
            *OPTIONAL* timeout for connecting to device. Default is set to 300.

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        Upgrade device    device=${device-handle}

    :returns:TRUE if upgrade to new image sucessfully FALSE if upgrade to new image unsucessfully

    """
    _verify_method(device, 'upgrade')
    return_value = device.upgrade(**kwargs)
    return return_value

def clean_config_on_device(device, **kwargs):
    """
    This API use to clean config of router by load a config in flash|slot0|slo1 or on tftp server.

    ARGUMENTS:
        [device, **kwargs]
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param FILE config_file:
            **OPTIONAL** config file name for loadding

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        Clean config on device     device=${device-handle}

    :returns:True if the clean config is success.False if the clean config fails
    """
    _verify_method(device, 'clean_config')
    return_value = device.clean_config(**kwargs)
    return return_value

def set_current_system_node(device, system_node):
    """
    Device object will set its current_node (attribute) to a particular system node ('primary'/'slave'/'member1')

    ARGUMENTS:
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR system_node:
            *MANDATORY* name of the system node('primary'/'slave'/'member1') to point to.

    ROBOT USAGE:
        Ex 1: ${device-handle} =  Get Handle    resource=r1
              Set Current System Node    device=${device-handle}    system_node=member1

        Ex 2: ${device-handle} =  Get Handle    resource=r1
              Set Current System Node    device=${device-handle}   system_node=primary

    :return: True(boolean) in case the handle pointer changes correctly.

    :raises: Exception, in case passed parameter values do not exist in the device
            object's System Dictionary.
    """
    _verify_method(device, 'set_current_system_node')
    return_value = device.set_current_system_node(system_node)
    return return_value


def set_current_controller(device, controller, system_node='current'):
    """
    This will not change the current system node for the device object

    DESCRIPTION:
        Device object will set its system node('primary'/'slave'/'member1')
        to a particular controller('re0'/'re1')
        **This will not change the current system node for the device object**

        ** NOTE **
        If the user has not connected to all the device's controllers during initialization,
        and if they try to connect to a controller that has not been connected
        to an error will occur. To avoid this, make sure to connect to all controllers via
        this framework variable:

        r0 {
            system {
                fv-connect-controllers "all";
            }
        }

    ARGUMENTS:
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR system_node:
            *OPTIONAL* name of the system node('primary'/'slave'/'member1')
                        to process current controller change.
                        Default is current system node.
        :param STR controller:
            *MANDATORY* name of the controller('re0'/'re1') to point to.

    ROBOT USAGE:
        Ex 1: ${device-handle} =  Get Handle    resource=r1
        Set Current Controller    device=${device-handle}   system_node=member1    controller=re1

        Ex 2: ${device-handle} =  Get Handle    resource=r1
        Set Current Controller    device=${device-handle}    controller=re1

    :return: True(boolean) in case the handle pointer changes correctly.

    :raises: Exception, in case passed parameter values do not exist in
            the device object's System Dictionary.
    """
    _verify_method(device, 'set_current_controller')
    return_value = device.set_current_controller(controller, system_node)
    return return_value


def detect_core(device, core_path=None, resource=None):
    """
    Detect core on the device

    ARGUMENTS:
        [device, core_path=None, resource=None]
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR resource:
            *MANDATORY* Logical name of the resource. Default is set to None.
       :param STR core_path:
            *OPTIONAL*  Path as a list ( where cores to be found).
                        Default core_path is '/var/crash/*core*' ,
                        '/var/tmp/*core*','/var/tmp/pics/*core*'

    ROBOT USAGE:
        Ex 1:   ${device-handle} =  Get Handle    resource=r1
                ${response} = detect core    device=${device-handle}    resource=r0

        Ex 2:   ${device-handle} =  Get Handle    resource=r1
                ${response} = detect core    device=${device-handle}    core_path=${CORE}
                    ....     resource=r0

    :returns: Returns True(if core found) else False. Return value will be scalar
    """
    _verify_method(device, 'detect_core')
    if core_path is not None:
        return_value = device.detect_core(core_path=core_path, resource=resource)
    else:
        return_value = device.detect_core(resource=resource)
    return return_value


def get_model_for_device(device, **kwargs):
    """
    Gets the model info from the box

    ARGUMENTS:
        [device]
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        ${response} = get model for device   device=${device-handle}

    :return: return model of device.

    """
    _verify_method(device, 'get_model')
    return_value = device.get_model(**kwargs)
    return return_value

def get_host_name_for_device(device, **kwargs):
    """
    Gets the  hostname of the device.

    ARGUMENTS:
        [device]
        :param STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        get host name for device     device=${device-handle}

    :return:get host names for devices.

    """
    _verify_method(device, 'get_host_name')
    return_value = device.get_host_name(**kwargs)
    return return_value

def get_version_for_device(device, **kwargs):
    """
    Gets the version info from the box

    ARGUMENTS:
        :params STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :param STR major:
            *OPTIONAL*   Based on users request API returns only major version info

    ROBOT USAGE:
        Ex 1: ${device-handle} =  Get Handle    resource=r1
              ${response} = get version for device  device=${device-handle}

        Ex 2: ${device-handle} =  Get Handle    resource=r1
              ${response} = get version for device   device=${device-handle}     major=${true}

    :return: version of device.

    """
    _verify_method(device, 'get_version')
    return_value = device.get_version(**kwargs)
    return return_value

def get_vmhost_infra_for_device(device, **kwargs):
    """
        Gets the info whether the device is with vmhost infra or not.

    ARGUMENTS:
        :params STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)

    ROBOT USAGE:
        Ex 1: ${device-handle} =  Get Handle    resource=r1
               get vmhost infra for device   device= ${device-handle}

    :return boolean:True if device is vmhost infra, False if not.
    """
    _verify_method(device, 'get_vmhost_infra')
    return_value = device.get_vmhost_infra(**kwargs)
    return return_value

def execute_grpc_api(dev, timeout=300, channel_ID=None, api_name=None, api_call=None, api_call_yaml_file=None, **kwargs):
    """
    Function to execute a grpc api on the router

    DESCRIPTION:
        Function to execute a grpc api on the router,
        by invoking the Grpc class method send_api(),
        given an instance of Grpc Class and channel ID

        NOTE: The API has a pre-requisite in that the API 'add_channel_to_device'
              needs to be invoked prior to invoking this 'execute_grpc_api' API.

    ARGUMENTS:
        [dev, timeout=300, channel_ID=None, api_name=None, api_call=None, api_call_yaml_file=None, **kwargs]
        :param INT timeout:
            *OPTIONAL* : Time by which response/output is expected
                            Default is 300 seconds
        :param STR channel_ID:
            *OPTIONAL* : Channel ID used to map the GRPC class
                        Defaults to internally computed channel id
        :param STR api_name:
            *OPTIONAL* : GRPC API name defined in the .proto file(Option 1 to invoke/exec a GRPC API)
        :param STR api_call:
            *OPTIONAL* : GRPC API name with arguments(Option 2 to invoke/exec a GRPC API)
        :param STR api_call_yaml_file:
            *OPTIONAL* : yaml file which has the GRPC service & API calls with arguments
                           (Option 3 to invoke/exec a GRPC API)

        #----------------------------- Begin: kwargs ------------------------#

        :param kwargs: Keyword arguments passed along with one of
            api_name/api_callable/grpc_api_as_yaml options

        #### ------ Mandatory kwargs when param 'api_name' is used ---------####
        :param service: Name of the stub service in which api request needs
            to be sent
            *MANDATORY*: when param 'api_name' or 'api_callable' options are used
            *OPTIONAL* : when param 'api_as_yaml' option is used
        :param STR api_args:
            *OPTIONAL* Arguments to the API request

        :param modules_to_source: list of python modules to source for
            grpc callable to be executed
            Example: (robot file statements)
                @{imp_modules}    mgd_service_pb2    openconfig_service_pb2
                    modules_to_source=@{imp_modules}

         #### -------- Mandatory kwargs when param 'api_call' is used --------####
        :param STR service: Name of the stub service in which api request
            needs to be sent
            *MANDATORY* when param 'api_name' or 'api_callable' options are used
            *OPTIONAL* when param 'api_as_yaml' option is used

        :param STR library:
            *OPTIONAL*  name of yaml file containing the list of grpc library
            files to import
            Sample file contents:
            {
                'Libraries': ['mgd_service_pb2.py','openconfig_service_pb2.py'],
            }

         ## ----- Mandatory kwargs when param 'grpc_api_as_yaml' is used -------##
        :param STR tcase_id:
            *OPTIONAL*  Unique tag/testcase id in the yaml file to match
            - This would be the main 'keys' in the dictionary format contents
                of the yaml file
            - Refer to the "CAT" tool to generate this file given
                the .proto file as input
            - The "CAT" tool generated file is then required to be manually
                edited to supply input to the API call

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        ${result1} =  execute grpc api    ${device-handle}    service=Firewall
                ....        library=${grpc_libs_file}   api_call=${api_call}

    :return:  API execution result

    RELATED KEYWORDS:
        execute_command_on_device()
        execute_shell_command_on_device()
        execute_cli_command_on_device()
        execute_config_command_on_device()
        execute_vty_command_on_device()
        execute_cty_command_on_device()
        execute_rpc_command_on_device()
        execute_pyez_command_on_device()
    """
    current_target = dev.current_node.current_controller

    # Junos:_grpc_init : default_grpc_channel
    if channel_ID is None:
        channel_ID = current_target.default_grpc_channel

    if api_name is None and api_call is None and api_call_yaml_file is None:
        raise TobyException(" Either one of the arguments:api_name | api_call | api_call_yaml_file is mandatory")

    if api_name is not None:
        if 'api_args' not in kwargs:
            raise TobyException(" Along with 'api_name' argument, 'api_args' argument is mandatory")

        if 'modules_to_source' not in kwargs:
            raise TobyException(" Along with 'api_name' argument, 'modules_to_source' argument is mandatory")

        if 'service' not in kwargs:
            raise TobyException(" Along with 'api_name' argument, 'service' argument is mandatory")

        modules = []
        modules = kwargs.get('modules_to_source')

        for module in modules:
            im_module = importlib.import_module(module, package=None)

            for tmp in dir(im_module):
                globals()[tmp] = getattr(im_module, tmp)

        grpc_callable = kwargs.get('api_args')
        kwargs['args'] = eval(grpc_callable)
        kwargs['api'] = api_name

    # setting the keyword args for the Grpc class method send_api

    kwargs['timeout'] = timeout

    if api_call is not None:
        kwargs['api_call'] = api_call

        if 'service' not in kwargs:
            raise TobyException(" Along with 'api_call' argument, 'service' argument is mandatory")

        if 'library' not in kwargs:
            raise TobyException(" Along with 'api_call' argument, 'library' argument is mandatory")

    if api_call_yaml_file is not None:
        kwargs['yaml_file'] = api_call_yaml_file

        if 'tcase_id' not in kwargs:
            raise TobyException(" Along with 'api_call_yaml_file' argument, 'tcase_id' argument is mandatory")
        else:
            kwargs['id'] = kwargs['tcase_id']

    api_res = current_target.channels['grpc'][channel_ID].send_api(**kwargs)
    return api_res


def get_platform_type(device):
    """
        Returns the platform type based on the architecture.

    ARGUMENTS:
        :params STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        ${response} = get Platform type    device=${device-handle}

    :return: Returns octeon/x86/xlp
    """
    _verify_method(device, 'get_platform_type')
    return device.get_platform_type()

def set_device_log_level(device, level='INFO'):
    """
        Sets the log level for each none and for each controller

    ARGUMENTS:
        :params STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)

        :params STR level:
            *OPTIONAL*  required level to enable  INFO/DEBUG/WARN/ERROR . case-insensitive
                        default is INFO.

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        set device log level    ${device-handle}    level='ERROR'

    :return: True
    """
    import logging
    level = logging._nameToLevel[str(level).upper()]
    for node in device.nodes.keys():
        for controller_name in device.nodes[node].controllers.keys():
            device.nodes[node].controllers[controller_name].device_logger.setLevel(level)
            device.nodes[node].controllers[controller_name].global_logger.setLevel(level)
    return True

def set_device_timeout(device, target, timeout=120):
    """
        Sets the timeout value for each controller

    ARGUMENTS:
        :params STR device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the
                        proper device resource (can be r0, h0, etc.)
        :params STR target:
            *MANDATORY* target action, supported targets are
                       shell/cli/config/reboot/reconnect/pyez/vty/cty/commit/reboot/upgrade/issu/connect
        :params STR timeout:
            *OPTIONAL* expected timeout value. Default is 120.

    ROBOT USAGE:
        ${device-handle} =  Get Handle    resource=r1
        set device timeout   ${device-handle}     target=cli    timeout=${240}

    :return: True
    """
    return device.set_device_timeout(target, timeout=timeout)
