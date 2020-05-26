"""
 Python Class for managing VNFs via Junos Device Manager (JDM)

 Author(s):
   Sudhir Akondi (sudhira@juniper.net)

"""

from robot.libraries.BuiltIn import BuiltIn

from jnpr.toby.hldcl.device import connect_to_device
from jnpr.toby.hldcl.device import disconnect_from_device
from jnpr.toby.hldcl.device import execute_cli_command_on_device
from jnpr.toby.hldcl.device import execute_shell_command_on_device
from jnpr.toby.hldcl.device import execute_config_command_on_device
from jnpr.toby.hldcl.device import close_device_handle

import re
from copy import deepcopy


class jdm_vnf:
    """
    Python class defined to handle VNFs hosted on the NFX via JDM
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __log_info__(self, message):
        t.log("INFO", "%s: %s" % (self.__class__.__name__, message))

    def __log_warning__(self, message):
        t.log("WARN", "%s: %s" % (self.__class__.__name__, message))

    def __log_error__(self, message):
        t.log("ERROR", "%s: %s" % (self.__class__.__name__, message))

    def __init__(self):
        """
        Initialize global variables
        """
        self.vnf_type = {}
        self.vnf_ssh_handles = {}
        self.vnf_console_handles = {}
        self.vnf_console_prompts = {}
        self._escape_char_ = "_"
        self.console_pattern = \
            r"(Domain not found|Escape character|ogin:|assword:|> |\$|>|#|%)[\s\t]?"

    def connect_to_vnf_via_jdm_ssh(self, tag, vnf_name, vnf_type, username, password,
                                   via_jcp=False, fips_mode=False, ssh_from="shell"):
        """
        Function to create a new connection to a VNF with JDM as proxy-host in the middle. This
        function can be used once the VNF is completely UP and has liveliness in Up state with JDM.
        This makes use of the fv-proxy functionality provided by Toby

        Python Example:
            _jdm_vnf_ = BuiltIns.get_library_instance("jdm_vnf")

            # for NFX-2 platform
            _vnf_hdl_ = _jdm_vnf_.connect_to_vnf_via_jdm_ssh(tag=r0, vnf_name='centos-1',
                                                             username='root', password='password',
                                                             vnf_type='linux')
            # for NFX-2 in FIPS mode
            _vnf_hdl_ = _jdm_vnf_.connect_to_vnf_via_jdm_ssh(tag=r0, vnf_name='centos-1',
                                                             username='root', password='password',
                                                             fips_mode=True, vnf_type='linux')
            # for NFX-3
            _vnf_hdl_ = _jdm_vnf_.connect_to_vnf_via_jdm_ssh(tag=r0, vnf_name='centos-1',
                                                             username='root', password='password',
                                                             via_jcp=True, vnf_type='linux')
            _vnf_hdl_ = _jdm_vnf_.connect_to_vnf_via_jdm_ssh(tag=r0, vnf_name='centos-1',
                                                             username='root', password='password',
                                                             via_jcp=True, vnf_type='linux',
                                                             ssh_from="cli")

        Robot Example:
            Library    jnpr/toby/jdm/jdm_vnf.py
            # for NFX-2
            ${vnf_hdl}  Connect To VNF via JDM SSH   tag=r0   vnf_name=centos-1   username=root
                        ...                          password=password   vnf_type=linux
            # for NFX-2 in FIPS mode
            ${vnf_hdl}  Connect To VNF via JDM SSH   tag=r0   vnf_name=centos-1   username=root
                        ...                          password=password  fips_mode=${true}
                        ...                          vnf_type=linux
            # for NFX-2
            ${vnf_hdl}  Connect To VNF via JDM SSH   tag=r0   vnf_name=centos-1   username=root
                        ...                          password=password  via_jcp=${true}
                        ...                          vnf_type=linux

        :param str tag:
          **REQUIRED**  Tag name of the resource
        :param str vnf_name:
          **REQUIRED** Name of the VNF , that is resolved from the JDM
        :param str vnf_type:
          **REQUIRED** Type of the VNF.
          Valid values: 'junos', 'linux'
        :param str username:
          **REQUIRED** User name for VNF login
        :param str password:
          **REQUIRED** Password for User VNF login
        :param bool via_jcp:
          **OPTIONAL** Boolean value to indicate VNF is reachable via private routing instance or
                       not. This is useful for login to VNFs on NFX-3, where the internal network
                       is on a private routing instance __juniper_private4__
        :param bool fips_mode:
          **OPTIONAL** Boolean value to indicate the box is in NFX-2 FIPS mode. If yes, the VNF is
                       reachable from the JDM, that makes it a two-hop SSH session
        :param str ssh_from:
          **OPTIONAL** Indicates where to execute the login command from.
                       When set to 'shell', the command used is 'ssh ', whereas
                       when set to 'cli', command used
                           is 'request virtual-network-functions ssh <vnfname>'

        :returns  str  vnf_handle:
          **REQUIRED** Device Handle to the VNF SSH Channel

        """
        try:

            self.__log_info__("Closing any existing SSH connection to the VNF")
            self.disconnect_ssh_to_vnf_via_jdm(tag, vnf_name)
            self.__log_info__("Attempting to connect to VNF: %s of Type: %s hosted on: %s"
                              " using credentials: %s/%s"
                              % (vnf_name, vnf_type, tag, username, password))
            _vnf_model_ = {
                "junos": "ex9204",
                "linux": "centos",
            }
            _private_routing_instance_ = "__juniper_private4__"
            _jdm_ip_ = "192.168.1.254"

            self.__log_info__("Fetching JDM Details for Proxy SSH")

            #_dut_hostname_ = tv[tag + '__name']
            #_dut_username_ = tv[tag + '__re0__user']
            #_dut_password_ = tv[tag + '__re0__password']
            _init_obj_ = BuiltIn().get_library_instance("init")
            _dut_hostname_ = _init_obj_.get_t(resource=tag, controller="re0", attribute="hostname")
            _dut_username_ = _init_obj_.get_t(resource=tag, controller="re0", attribute="user")
            _dut_password_ = _init_obj_.get_t(resource=tag, controller="re0", attribute="password")

            system_data = dict()
            system_data['system'] = dict()
            controller = None
            if vnf_type.lower() == "junos":
                controller = 're0'
            else:
                controller = 'controller'

            system_data['system']['primary'] = dict()
            system_data['system']['primary']['name'] = vnf_name
            system_data['system']['primary']['model'] = _vnf_model_[vnf_type]
            system_data['system']['primary']['osname'] = vnf_type
            system_data['system']['primary']['controllers'] = dict()
            system_data['system']['primary']['controllers'][controller] = dict()
            system_data['system']['primary']['controllers'][controller]['name'] = vnf_name
            system_data['system']['primary']['controllers'][controller]['connect'] = True
            system_data['system']['primary']['controllers'][controller]['mgt-ip'] = vnf_name
            system_data['system']['primary']['controllers'][controller]['model'] = \
                _vnf_model_[vnf_type]
            system_data['system']['primary']['controllers'][controller]['osname'] = vnf_type
            system_data['system']['primary']['controllers'][controller]['connect_mode'] = "ssh"
            system_data['system']['primary']['controllers'][controller]['user'] = username
            system_data['system']['primary']['controllers'][controller]['password'] = password
            system_data['system']['primary']['controllers'][controller]['connect_channels'] = \
                ['text']
            system_data['system']['primary']['controllers'][controller]['timeout'] = 30


            if fips_mode is False:
                if via_jcp is False:
                    self.__log_info__("NFX in Non-FIPS Mode, Via JCP set to False")
                    system_data['system']['primary']['controllers'][controller]['proxy_hosts'] = [
                        {
                            'host': _dut_hostname_,
                            'user': _dut_username_,
                            'password': _dut_password_,
                        }
                    ]
                else:
                    self.__log_info__("NFX in Non-FIPS Mode, Via JCP set to True")
                    if ssh_from == "shell":
                        self.__log_info__("ssh_from set to 'shell'")
                        system_data['system']['primary']['controllers'][controller]['proxy_hosts'] = \
                        [
                            {
                                'host': _dut_hostname_,
                                'user': _dut_username_,
                                'password': _dut_password_
                            },
                            {
                                'connect_command': "ssh -oStrictHostKeyChecking=no -JU %s -l %s %s"
                                                   % (_private_routing_instance_, username, vnf_name)
                            }
                        ]
                    else:
                        self.__log_info__("ssh_from set to 'cli'")
                        system_data['system']['primary']['controllers'][controller]['proxy_hosts'] = [
                            {
                                'host': _dut_hostname_,
                                'user': _dut_username_,
                                'password': _dut_password_
                            },
                            {
                                'connect_command': "cli -c 'request virtual-network-functions ssh %s'"
                                                   % vnf_name
                            }
                        ]

            else:
                self.__log_info__("NFX in FIPS Mode, two-hop login, to JDM then to VNF")
                system_data['system']['primary']['controllers'][controller]['proxy_hosts'] = [
                    {
                        'host': _dut_hostname_,
                        'user': _dut_username_,
                        'password': _dut_password_,
                    },
                    {
                        'host': _dut_hostname_,
                        'user': _dut_username_,
                        'password': _dut_password_,
                        'connect_command': "ssh -oStrictHostKeyChecking=no -JU %s -l %s %s" % (_private_routing_instance_, username, _jdm_ip_)
                    },
                    {
                        'connect_command': "ssh -oStrictHostKeyChecking=no -l %s %s" % (username, vnf_name)
                    },
                ]

            self.__log_info__("Prepared System Dictionary for connecting to VNF: %s" % system_data)

            _vnf_hdl_ = connect_to_device(system=system_data['system'], timeout=30)

            if _vnf_hdl_ is None:
                self.__log_error__("Unable to connect to VNF: %s" % vnf_name)
                return False

            if tag not in self.vnf_ssh_handles.keys():
                self.vnf_ssh_handles[tag] = {}
                self.vnf_type[tag] = {}

            self.vnf_ssh_handles[tag][vnf_name] = _vnf_hdl_
            self.vnf_type[tag][vnf_name] = vnf_type
            return True

        except Exception as _exception_:
            self.__log_error__("Exception Raised: %s : %s" % (type(_exception_), _exception_))
            return False

    def disconnect_ssh_to_vnf_via_jdm(self, tag, vnf_name):
        """
        Function to disconnect the SSH session to a VNF via JDM that was previously established via connect_to_vnf_ssh above

        Python Example:
            _jdm_vnf_.disconnect_ssh_to_vnf_via_jdm(tag='r0', vnf_name='centos-1')

        Robot Example:
            Disconnect SSH to VNF via JDM   tag=r0   vnf_name=centos-1

        :param str tag:
          **REQUIRED**  Tag name of the resource
        :param str vnf_name:
          **REQUIRED** Name of the VNF , that is resolved from the JDM

        """
        try:
            if tag not in self.vnf_ssh_handles or \
               vnf_name not in self.vnf_ssh_handles[tag] or \
               self.vnf_ssh_handles[tag][vnf_name] is None:
                self.__log_info__("No SSH connection found to VNF: %s on tag: %s" % (vnf_name, tag))
                self.__log_info__("Perhaps you did not connect to this VNF yet. Disconnect IGNORED")
                return True
        except Exception as _exception_:
            raise Exception("Exception raised: %s: %s" % (type(_exception_), _exception_))

        try:
            _status_ = disconnect_from_device(device=self.vnf_ssh_handles[tag][vnf_name])
            self.vnf_ssh_handles[tag][vnf_name] = None
        except Exception as _exception_:
            raise Exception("Exception Raised in disconnect_ssh_to_vnf: %s: %s" %
                            (type(_exception_), _exception_))

        if _status_ is False:
            raise Exception("Disconnect From SSH to VNF: %s on tag: %s failed." % (vnf_name, tag))

        return _status_

    def connect_to_vnf_via_jdm_console(self, tag, vnf_name, vnf_type, username, password, virsh_cmd=True, force=True):
        """
        Function to create a new connection to a VNF by executing command on the JDM. This function can be used once

        Python Example:
            _jdm_vnf_ = BuiltIns.get_library_instance("jdm_vnf")

            # for connection using virsh command
            _vnf_hdl_ = _jdm_vnf_.connect_to_vnf_via_jdm_ssh(tag=r0, vnf_name='centos-1', username='root', password='password',
                                                             vnf_type='linux', virsh_cmd=True)
            # for connection using cli command
            _vnf_hdl_ = _jdm_vnf_.connect_to_vnf_via_jdm_ssh(tag=r0, vnf_name='centos-1', username='root', password='password',
                                                             vnf_type='linux', virsh_cmd=False)

        Robot Example:
            Library  jnpr/toby/jdm/jdm_vnf.py

            # for connection using virsh command
            ${vnf_hdl}  Connect To VNF via JDM SSH   tag=r0   vnf_name=centos-1   username=root  password=password   vnf_type=linux
                        ...                          virsh_cmd=${true}
            # for cnnection using cli command
            ${vnf_hdl}  Connect To VNF via JDM SSH   tag=r0   vnf_name=centos-1   username=root  password=password  fips_mode=${true}
                        ...                          vnf_type=linux  virsh_cmd=${false}

        :param str tag:
          **REQUIRED**  Tag name of the resource
        :param str vnf_name:
          **REQUIRED** Name of the VNF , that is resolved from the JDM
        :param str vnf_type:
          **REQUIRED** Type of the VNF.
          Valid values: 'junos', 'linux'
        :param str username:
          **REQUIRED** User name for VNF login
        :param str password:
          **REQUIRED** Password for User VNF login
        :param bool virsh_cmd:
          **OPTIONAL** Boolean value to indicate login to console using virsh command or Junos cli command request vnf console
        :param bool force:
          **OPTIONAL** Boolean value to pass force option to console command

        :returns  str  vnf_handle:
          **REQUIRED** Device Handle to the VNF Console Channel
        """
        try:

            self.__log_info__("Closing any existing Console connection to the VNF")
            self.disconnect_console_to_vnf_via_jdm(tag, vnf_name)

            self.__log_info__("Attempting to connect Console to VNF: %s of Type: %s hosted on: %s"
                              " using credentials: %s/%s" % (vnf_name, vnf_type, tag, username, password))

            if virsh_cmd is True:
                if force == True:
                    _console_login_cmd_ = "virsh -e" + self._escape_char_ + " console " + vnf_name + " --force"
                else:
                    _console_login_cmd_ = "virsh -e" + self._escape_char_ + " console " + vnf_name
            else:
                if force == True:
                    _console_login_cmd_ = "cli -c 'request virtual-network-function console %s force'" % vnf_name
                else:
                    _console_login_cmd_ = "cli -c 'request virtual-network-function console %s'" % vnf_name

            self.__log_info__("Using Console Command: %s" % _console_login_cmd_)

            _init_obj_ = BuiltIn().get_library_instance("init")
            _primary_dict_ = _init_obj_.get_t(resource=tag)

            _system_dict_ = {}
            _system_dict_["primary"] = deepcopy(_primary_dict_)
            _proxy_host_type_ = ""
            for _ctrl_ in _system_dict_['primary']['controllers'].keys():
                _system_dict_['primary']['controllers'][_ctrl_]['connect_channels'] = ['text']
                _proxy_host_type_ = _system_dict_['primary']['controllers'][_ctrl_]['osname']

            self.__log_info__("Proy Host Type: %s" % _proxy_host_type_)

            _vnf_hdl_ = connect_to_device(system=_system_dict_)
            if _vnf_hdl_ is None:
                self.__log_error__("Unable to create a new connection to tag: %s" % tag)
                return False

            _cmd_ = _console_login_cmd_
            _attempts_ = 0
            _success_ = False
            while _attempts_ <= 6:
                self.__log_info__("Sending Command: %s" % _cmd_)

                _response_ = execute_shell_command_on_device(
                    device=_vnf_hdl_, command=_cmd_, pattern=self.console_pattern, raw_output=True)
                self.__log_info__("Received Response: \n--begin--\n%s\n--end--\n" % _response_)
                _attempts_ += 1
                if re.search(r'.*Domain not found.*', _response_):
                    self.__log_error__("VNF '%s' not found on Device." % vnf_name)
                    close_device_handle(_vnf_hdl_)
                    return False
                elif re.search(r'.*Escape character.*', _response_):
                    _cmd_ = " "
                elif re.search(r'.*yes/no.*', _response_, re.IGNORECASE):
                    _cmd_ = "yes"
                elif re.search(r'.*ogin:\s*', _response_):
                    _cmd_ = username
                elif re.search(r'.*word:\s*', _response_):
                    _cmd_ = password
                elif re.search('> ', _response_):
                    _cmd_ = "start shell"
                elif re.search(r'(\$|>|#|%)[\s\t]?', _response_):
                    _success_ = True
                    break

            if _success_ is not True:
                self.__log_error__(
                    "Failed to find appropriate responses in opening console connection to VNF %s" % vnf_name)
                close_device_handle(_vnf_hdl_)
                return False

            self.__log_info__(
                "Successfuly opened a console session to the VNF: %s on Tag: %s" % (vnf_name, tag))

            # set the shell prompt on the VNF as well
            if _proxy_host_type_.lower() == "junos":
                self.__log_info__("Proxy host is of type 'junos'. Setting shell prompt on vnf")
                _ret_ = self.set_junos_prompt_shell(_vnf_hdl_)
                #_ret_ = _vnf_hdl_.current_node.current_controller.set_prompt_shell(
                #    prompt=_vnf_hdl_.current_node.current_controller.prompt)
            elif _proxy_host_type_.lower() == "linux" or _proxy_host_type_.lower() == "unix":
                self.__log_info__("Proxy host is of type 'linux'. Setting shell prompt on vnf")
                _ret_ = self.set_linux_prompt_shell(_vnf_hdl_)
                #_ret_ = _vnf_hdl_.current_node.current_controller.set_prompt(
                #    prompt=_vnf_hdl_.current_node.current_controller.prompt)
            else:
                self.__log_warning__(
                    "Unknown proxy host type. Not setting the prompt on destination vnf")
                _ret_ = True

            if _ret_ is not True:
                self.__log_error__("Unable to set the shell prompt on VNF")
                return False

            if tag not in self.vnf_console_handles.keys():
                self.vnf_console_handles[tag] = {}
                self.vnf_type[tag] = {}

            self.vnf_console_handles[tag][vnf_name] = _vnf_hdl_
            self.vnf_type[tag][vnf_name] = vnf_type
            self.__log_info__("Handle: %s" % self.vnf_console_handles[tag][vnf_name])
            return True

        except Exception as _exception_:
            raise Exception("Exception Raised: %s : %s" % (type(_exception_), _exception_))

    def set_junos_prompt_shell(self, hdl):

        """
        Local function that invokes the set_prompt_shell function to set prompt on a junos shell
        """
        if isinstance(hdl.current_node.current_controller.prompt, list):
            prompt = hdl.current_node.current_controller.prompt[0]
        else:
            prompt = hdl.current_node.current_controller.prompt
        return hdl.current_node.current_controller.set_prompt_shell(prompt=prompt)

    def set_linux_prompt_shell(self, hdl):

        """
        Local function that invokes the set_prompt function to set prompt on a Linux host
        """
        if isinstance(hdl.current_node.current_controller.prompt, list):
            prompt = hdl.current_node.current_controller.prompt[0]
        else:
            prompt = hdl.current_node.current_controller.prompt
        return hdl.current_node.current_controller.set_prompt(prompt=hdl.current_node.current_controller.prompt)

    def disconnect_console_to_vnf_via_jdm(self, tag, vnf_name):
        """
        Function to disconnect the Console session to a VNF via JDM that was previously established via connect_console_to_vnf_ssh above

        Python Example:
            _jdm_vnf_.disconnect_console_to_vnf_via_jdm(tag='r0', vnf_name='centos-1')

        Robot Example:
            Disconnect console to VNF via JDM   tag=r0   vnf_name=centos-1

        :param str tag:
          **REQUIRED**  Tag name of the resource
        :param str vnf_name:
          **REQUIRED** Name of the VNF , that is resolved from the JDM

        """
        try:
            if tag not in self.vnf_console_handles or \
               vnf_name not in self.vnf_console_handles[tag] or \
               self.vnf_console_handles[tag][vnf_name] is None:
                self.__log_info__(
                    "No Console connection found to VNF: %s on tag: %s" % (vnf_name, tag))
                self.__log_info__("Perhaps you did not connect to this VNF yet. Disconnect IGNORED")
                return True
        except Exception as _exception_:
            self.__log_error__("Exception Raised in disconnect_console_to_vnf: %s: %s" %
                               (type(_exception_), _exception_))

        try:
            # --
            #  1. execute exit command on shell
            execute_shell_command_on_device(device=self.vnf_console_handles[tag][vnf_name],
                                            command="exit",
                                            pattern=self.console_pattern)
            execute_shell_command_on_device(device=self.vnf_console_handles[tag][vnf_name],
                                            command=self._escape_char_,
                                            pattern=".*")
            #_status_ = close_device_handle(device=self.vnf_console_handles[tag][vnf_name])
            self.__log_info__("Handle: %s" % self.vnf_console_handles[tag][vnf_name])

        except Exception as _exception_:
            self.__log_error__("Exception in sending exit commands over vnf console: %s : %s" %
                               (type(_exception_), _exception_))

        try:
            close_device_handle(self.vnf_console_handles[tag][vnf_name])
        except Exception as _exp_:
            raise Exception("Closing Console Handle failed to VNF %s on tag: %s. (Handle: %s): %s : %s" %
                            (vnf_name, tag, self.vnf_console_handles[tag][vnf_name], type(_exp_), _exp_))

        self.vnf_console_handles[tag][vnf_name] = None
        self.vnf_type[tag][vnf_name] = None

        return True

    def get_vnf_handle(self, tag, vnf_name, mode="ssh"):
        """
        Function to return the device handle to the console / ssh connection made to a VNF within this class.

        Python Example:
           _ssh_hdl_ =  _jdm_vnf_obj_.get_vnf_handle(tag='r0', vnf_name='centos', mode='ssh')
           _console_hdl_ =  _jdm_vnf_obj_.get_vnf_handle(tag='r0', vnf_name='centos', mode='console')

        Robot Example:
           ${ssh_hdl}   Get VNF Handle   tag=r0  vnf_name=centos  mode=ssh
           ${console_hdl}   Get VNF Handle   tag=r0  vnf_name=centos  mode=console

        :param str tag:
          **REQUIRED** Name of the resource on which the VNF is hosted

        :param str vnf_name:
          **REQUIRED** Name of the VNF

        :param str mode:
          **REQUIRED** Mode of connection to the VNF. Valid values 'ssh', 'console'
        """
        try:
            self.__log_info__("Fetching device handle of VNF: %s on %s" % (vnf_name, tag))
            _device_handle_ = None
            if mode == "console":
                self.__log_info__("console handles: %s" % self.vnf_console_handles)
                _device_handle_ = self.vnf_console_handles[tag][vnf_name]

            else:
                self.__log_info__("ssh handles: %s" % self.vnf_ssh_handles)
                _device_handle_ = self.vnf_ssh_handles[tag][vnf_name]

            return True, _device_handle_

        except Exception as _exception_:
            raise Exception("No Handle found for %s to VNF %s on %s. Exception: %s : %s" %
                               (mode, vnf_name, tag, type(_exception_), _exception_))

    def execute_command_on_vnf(self, tag, vnf_name, cmd, console=False, mode="SHELL"):
        """
        Function to execute a command on a VNF that is either of type linux / junos.

        Python Example:
            _cmd_shell_ = "uptime"
            _cmd_cli_ = "show version"
            _cmd_config_ = "show system"
            _response_ = execute_command_on_vnf(tag='r0', vnf_name='centos', cmd=_cmd_shell_, mode='shell', console=False)
            _response_ = execute_command_on_vnf(tag='r0', vnf_name='vsrx', cmd=_cmd_cli_, mode='cli', console=False)
            _response_ = execute_command_on_vnf(tag='r0', vnf_name='vjunos0', cmd=_cmd_config_, mode='config', console=False)
            _response_ = execute_command_on_vnf(tag='r0', vnf_name='centos', cmd=_cmd_shell_, mode='shell', console=True)
            _response_ = execute_command_on_vnf(tag='r0', vnf_name='vsrx', cmd=_cmd_cli_, mode='cli', console=True)
            _response_ = execute_command_on_vnf(tag='r0', vnf_name='vjunos0', cmd=_cmd_config_, mode='config', console=True)

        Robot Example:
            ${cmd_shell}    Set Variable   uptime
            ${cmd_cli}      Set Variable   show version
            ${cmd_config}   Set Variable   show system

            ${response}     Execute Command On VNF   tag=r0  vnf_name=centos   cmd=${cmd_shell}   mode=shell   console=${false}
            ${response}     Execute Command On VNF   tag=r0  vnf_name=vsrx     cmd=${cmd_cli}     mode=cli     console=${false}
            ${response}     Execute Command On VNF   tag=r0  vnf_name=vjunos0  cmd=${cmd_config}  mode=config  console=${false}
            ${response}     Execute Command On VNF   tag=r0  vnf_name=centos   cmd=${cmd_shell}   mode=shell   console=${true}
            ${response}     Execute Command On VNF   tag=r0  vnf_name=vsrx     cmd=${cmd_cli}     mode=cli     console=${true}
            ${response}     Execute Command On VNF   tag=r0  vnf_name=vjunos0  cmd=${cmd_config}  mode=config  console=${true}

        :param str tag:
          **REQUIRED** Name of the resource on which this VNF is hosted

        :param str vnf_name:
          **REQUIRED** Name of the VNF

        :param str cmd:
          **REQUIRED** Command to be executed

        :param bool console:
          **OPTIONAL** Set to True if command is to be executed on console to vnf, else to False for ssh
          Default: False

        :param str mode:
          **OPTIONAL** Mode of execution shell/cli/config. For linux VNFs, only shell is valid value and others apply for junos
                       type VNFs. It is up to the user to invoke this function accordingly
          Default: shell
        """
        try:
            self.__log_info__("Executing Command: %s in Mode: %s on VNF: %s on %s" %
                              (cmd, mode, vnf_name, tag))
            _device_handle_ = None
            if console is True:
                _status_, _device_handle_ = self.get_vnf_handle(tag, vnf_name, mode="console")
            else:
                _status_, _device_handle_ = self.get_vnf_handle(tag, vnf_name, mode="ssh")
        except Exception as _exception_:
            raise Exception("Exception caught: %s: %s" % (type(_exception_), _exception_))

        mode = mode.lower()
        _expected_modes_ = [ "shell", "cli", "config" ]
        if mode not in _expected_modes_:
            raise Exception("Unsupported value for mode: %s" % mode)
      
        try:
            if mode == "shell":
                _resp_ = execute_shell_command_on_device(device=_device_handle_, command=cmd)
            elif mode == "cli":
                _resp_ = execute_cli_command_on_device(device=_device_handle_, command=cmd)
            elif mode == "config":
                _resp_ = execute_config_command_on_device(device=_device_handle_, command_list=cmd)

            return True, _resp_

        except Exception as _exception_:
            raise Exception("Exception caught: %s: %s" % (type(_exception_), _exception_))

