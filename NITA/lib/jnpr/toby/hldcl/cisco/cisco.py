"""
Class for IOS Devices
"""
import os
import logging
import re
import time
import datetime
import glob

from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.connectors.sshconn import SshConn
from jnpr.toby.hldcl.connectors.telnetconn import TelnetConn
from jnpr.toby.hldcl.host import Host
from jnpr.toby.hldcl.cisco.utils import ping, get_image
from jnpr.toby.exception.toby_exception import TobyException


class Cisco(object):
    """
    Class factory to create IOS objects.
    """
    def __new__(cls, *args, **kwargs):
        """
        Factory method to create classes based on OS and model

        :param host:
            **REQUIRED** host-name or IP address of target device
        :param os:
            *OPTIONAL* Operating System of device. Default is IOS
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param password:
            *OPTIONAL* Login Password. If not provided will be derived from
            Toby framework defaults.
        :param model:
             *OPTIOANL* Model of device. Default is None.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            values are telnet/ssh.
        :param console:
            *OPTIONAL* Flag to identify console login. Default is False.
        :param mode:
            *OPTIONAL* Port on device to which connection needs to made.
        :return: Device object based on os and model
        """
        return_value = IOS(*args, **kwargs)
        return return_value


class IOS(Host):
    """
    Generic IOS class for common operations
    """

    def _connect(self):
        """
         Internal function to create the text channel for IOS devices.
         It will create text channel by telnet /ssh.
        """
        connection_class = None
        return_value = None
        port = self._kwargs.get('port', None)
        if self._kwargs.get('connect_mode', '').lower() == 'console':
            self.log(message="Cannot create 'cli_chan' for console mode",
                     level='INFO')
            return return_value
        elif self._kwargs.get('connect_mode', 'telnet').lower() == 'telnet':
            logging.info('Telnet connection')
            port = self._kwargs.get('port', 23)
            connection_class = TelnetConn
        elif self._kwargs.get('connect_mode').lower() == 'ssh':
            connection_class = SshConn
        else:
            self.log(message='Unknown connection mode '
                     '{0}'.format(self._kwargs['connect_mode']), level='ERROR')
            return return_value
        if self._kwargs.get('console', False):
            if 'con-ip' in self._kwargs:
                self.host = self._kwargs.get('con-ip')
                self.log(level='INFO', message='Host set to console ip')
            else:
                self.log(level='ERROR', message='Console ip does not exist')
        if not self.user:
            self.user = ''
        if not self.password:
            self.password = ''
        cli_chan = connection_class(host=self.host, user=self.user, password=self.password, port=port)
        return_value = cli_chan
        return return_value

    def connect(self):
        """
        Function to create text channel for IOS devices.
        Example:
        device_object.connect(host='hostname',user='username',password='password')
        """
        self.channel = self._connect()
        res = self.cli(command='terminal length 0').response()
        if re.search(r'Invalid|error', res, re.I):
            self.log(level='ERROR', message='Error setting terminal length 0')
        res = self.cli(command='terminal width 0').response()
        if re.search(r'Invalid|error', res, re.I):
            self.log(level='ERROR', message='Error setting screen-width 0')

        self.log('Text connection successful')

    # Mode Shift
    def _switch_mode(self, mode='privileged'):
        """
        This function is used to switch from one mode another mode.
        ex: user to privileged/ privileged to config
        param mode: It takes the mode as input argument.
                    The mode which you to switch
        """
        curr_mode = self.mode.lower()
        mode = mode.lower()
        if mode == curr_mode:
            return_value = True
            return return_value
        try:
            if mode == 'user':
                self._switch_mode(mode='privileged')
                self.execute(command="disable", pattern='>$')
            elif mode == 'privileged':
                if curr_mode == 'user':
                    self.enable()
                if curr_mode == 'config':
                    self.execute(command="end", pattern='#$')
            elif mode == 'config':
                self._switch_mode(mode='privileged')
                self.execute(command="configure terminal",
                             pattern=r'.*\(config\)#$')
        except Exception:
            raise TobyException('Cannot switch to ' + mode + ' mode.', host_obj=self)
        return_value = True
        self.mode = mode
        return return_value

    def __init__(self, *args, **kwargs):
        """
        Base class for IOS devices

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
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            values are telnet/ssh/netconf/console
        :param console:
            *OPTIONAL* Flag to identify console login. Default is False.
        :param port:
            *OPTIONAL* Port on device to which connection needs to made.
        :return: Device object based on os and model
        """
        # Check if host is provided
        if 'host' not in kwargs:
            raise TobyException("'host' is mandatory", host_obj=self)

        if kwargs.get('connect_mode', '').lower() == 'console':
            kwargs['strict'] = True
        kwargs['os'] = kwargs.get('os', 'IOS')

        self._kwargs = kwargs
        self.connected = False
        self.mode = 'user'
        self.prompt = '(>|#)'
        # call Device class init for common operations
        super(IOS, self).__init__(*args, **kwargs)
        # Connect to device (telnet/ssh)
        self.log(level='info', message="Connecting to device")
        self.connect()
        self.connected = True

    def execute(self, **kwargs):
        """
        Executes commands
        device_object.execute(command = 'show version')

        :param command:
            **REQUIRED** CLI command to execute
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :param pattern: Pattern to match.
        :return: Dictionary with the following keys
            'response': Response from the CLI command(text)
        """
        command = ''
        if 'command' in kwargs and kwargs['command'] is not None:
            command = kwargs['command']
        else:
            self.log(level="ERROR", message="Mandatory argument 'command' "
                                            "is missing!")

        timeout = kwargs.get('timeout', 90)
        pattern = kwargs.get('pattern')
        no_response = kwargs.get('no_response', False)

        if pattern is None:
            pattern = self.prompt

        response = self.channel.execute(cmd=command, pattern=pattern,
                                        device=self, no_response=no_response,
                                        timeout=timeout)
        if response == -1:
            raise TobyException('Timeout seen while retrieving output', host_obj=self)
        else:
            return_value = self.response
            return return_value

    def cli(self, command='', mode='privileged', pattern=None, timeout=60, kw_call=False):
        """
        Executes operational commands for user or privileged mode on IOS
        device_object.cli(command = 'show version')

        :param command:
            **REQUIRED** CLI command to execute
        :param mode:
            **OPTIONAL** 'user' or 'privileged' mode. Default: privileged
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :param pattern: Expected pattern
        :return: Object with the following methods
            'response()': Response from the CLI command(text)
        """
        if command is None:
            raise TobyException("Mandatory argument 'command' is missing!", host_obj=self)
        self._switch_mode(mode=mode)
        if not pattern:
            pattern = self.prompt
        # Only one command can be executed
        if not isinstance(command, str):
            raise TobyException("'command' should be a string", host_obj=self)

        self.log('command: ' + command)
        response = self.execute(command=command, pattern=pattern,
                                timeout=timeout)
        return_value = Response(response=response, status=True)
        return return_value

    def config(self, command_list='', pattern=None, timeout=60, kw_call=False):
        """
        Loads configurations or configures JunOS device.

        device_object.config(command_list = ['interface f0/0',
        'no shut', 'ip address 192.168.1.1 255.255.255.0'])

        :param command_list:
            **REQUIRED** List of string(s) of configuration commands to execute
        :param mode:
            *OPTIONAL* Mode of configuration. Default is None which means
            configure mode. Supported values are exclusive and private
        :param pattern:
            *OPTIONAL: Pattern expected back from device after executing
            config command
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :return: Object with the following methods
            'response()': Response from the config command
        """
        if command_list is None:
            raise TobyException("Mandatory argument 'command_list' is missing!", host_obj=self)
        if not isinstance(command_list, list):
            raise TobyException("Argument 'command_list' must be a list!", host_obj=self)
        self._switch_mode(mode='config')
        response = ''
        if not pattern:
            pattern = self.prompt

        for command in command_list:
            if not isinstance(command, str):
                raise TobyException("Argument 'command_list' must be a list of strings!", host_obj=self)
            response = self.execute(command=command, pattern=pattern, timeout=timeout)
        return_value = Response(response=response, status=True)
        return return_value

    def reconnect(self, timeout=180, interval=20):
        """
        Reconnects to IOS device
            device_object.reconnect()

        :param timeout:
            *OPTIONAL* Time till which reconnection can be attempted. Default
            is 30 seconds
        :param interval:
            *OPTIONAL* Interval in which reconnection needs to be attempted.
            Default is 20 seconds
        :return: True if the reconnection is successful, else False
        """
        return_value = False
        timestamp = time.time()
        self.log(message="disconnecting from the device", level='DEBUG')
        self.disconnect()
        while timeout > 0:
            try:
                self.log(level='INFO', message='Trying to reconnect device.')
                self.connect()
                self.log(level='INFO', message='Successfully connected to device.')
                return_value = True
                break
            except:
                self.log(level='INFO',
                         message='Unable to connect to device to device'
                         'Trying again in %s seconds' % interval)
                time.sleep(interval)
                timeout = timeout - time.time() + timestamp
                timestamp = time.time()
        if not return_value:
            self.log(level='ERROR', message='Unable to connect to device.')

        return return_value

    def disconnect(self):
        """
        Disconnects connection to IOS device.

            device_object.disconnect()

        :return: True if connection to device is terminated, else False
        """
        response = True
        if self.connected is not True:
            self.log(level='ERROR',
                     message='{0} object is closed'.format(self.host))
            return_value = False
            return return_value
        else:
            try:
                self.channel.close()
                del self.channel
                self.connected = False
            except Exception as exp:
                self.log(level="DEBUG",
                         message="Error while closing the object")
                self.log(level='ERROR',
                         message='Error while closing the object')
                self.log(level='ERROR', message=exp)
                response = False
        if response:
            logging.info('Successfully disconnected from Device')
        return_value = response
        return return_value

    def close(self):
        """

        device_object.close()

        Close connection to device and destroys the object.
        using this method.

        :param all_routing_engines
            Close handles of all routing engines
        :return: True if device object is closed successfully, else False
        """
        response = True
        try:
            if self.connected:
                self.channel.close()
        except Exception as exp:
            self.log(level="DEBUG",
                     message="Error while closing device Handle")
            self.log(level='ERROR',
                     message='Error while closing device Handle')
            self.log(level='ERROR', message=exp)
            response = False
        del self
        if response:
            logging.info('Successfully closed Device Handle')
        return_value = response
        return return_value

    def enable(self, enable_password=None):
        """
        device_object.enable(password='cisco)
        Execute enable command to move from user mode to privilege mode
        :param password
            *OPTIONAL* privilege password (enable password or enable secret
            password)

        """
        if not enable_password:
            enable_password = self.enable_password
        self.channel.execute(
            cmd='enable', pattern=['#', 'Password: '], device=self)
        res = self.channel.execute(cmd='%s' % enable_password, pattern='#',
                                   device=self)
        return_value = res
        self.mode = 'privileged'
        return return_value

    def reboot(self, wait=0, timeout=480, interval=20, option='',
               file='start', mode='privileged', all=False):
        """
        Reboot IOS device
            device_object.reboot()

        :param wait:
            *OPTIONAL* Time to sleep before reconnecting, Default value is 0
        :param timeout:
            *OPTIONAL* Time to reboot and connect to device.
            Default is 360 seconds
        :param interval:
            *OPTIONAL* Interval at which reconnect need to be attempted after
            reboot is performed. Default is 20 seconds

        Returns: True if device is rebooted and reconnection is successful,
        else an Exception is raised
        """
        self.save_config(file=file)
        response = self.cli(command='reload %s' % option, mode=mode,
                            pattern='(yes/no|confirm).*').response()

        if re.search(r'yes/no', response, re.I):
            self.execute(command="no", pattern='confirm.*')
            self.log(level='warn', message='Failed to save modified config')
            return_value = False
            return return_value
        self.execute(command='', pattern=r'.?|connection (?:to \S+ )?closed.*')
        self.log(level='INFO', message='Sleeping for {0} secs before '
                 'reconnecting'.format(wait))
        time.sleep(wait)
        response = self.reconnect(timeout=timeout, interval=interval)
        if response:
            self.log(level='INFO', message='Reboot successful')
        else:
            self.log(level='ERROR', message='Reboot failed')
            return_value = False
            return return_value
        return_value = True
        return return_value

    def save_config(self, file='', timeout=60):
        """
        save configuration for IOS device
            device_object.save_config()

        :param file:
            *REQUIRED* destination configuration file
        :param timeout:
            *OPTIONAL* Time to save config
            Default is 360 seconds


        Returns: True if device is saved successful,
        else an Exception is raised
        """
        if not file:
            raise TobyException("FILE is mandatory", host_obj=self)
        self.log(message="Attempting to store current configuration to"
                 " %s" % file, level='info')

        self.cli(command='copy running-config %s' % file,
                 pattern=[r'(error|invalid).*', r'Destination.*',
                          r'Please wait....*'], timeout=timeout).response()
        response = self.execute(command='',
                                pattern=[r'bytes copied.*', r'.*confirm].*',
                                         r'Please wait....*', r'lines built.*',
                                         r'want to overwrite?.*', '#'],
                                timeout=timeout)
        if re.search(r'want to overwrite?', response, re.I):
            response = self.execute(command='yes',
                                    pattern=r'lines built.*',
                                    timeout=timeout)
        if re.search(r'[confirm]', response, re.I):
            response = self.execute(command='',
                                    pattern=[r'bytes copied.*',
                                             r'Please wait....*', '#'],
                                    timeout=timeout)
        if re.search(r'([OK]|Building configuration...|bytes copied|'
                     r'Please wait\.\.\.|lines built|#)',
                     response, re.I):
            self.log(message='current configuration has been saved')
            return_value = True
            return return_value

        else:
            self.log(level='ERROR', message='Failed to store config to '
                     '%s' % file)
            return_value = False
            return return_value

    def switchover(self, options='', wait=180, timeout=360):
        """
        This function use to switch between routing engine of IOS device
        :param options:
            *OPTIONAL* options for switchover
        :param wait:
            *OPTIONAL* waiting time default 180 sec
        :param timeout:
            *OPTIONAL* timeout in seconds default 360 sec
        :returns:
            True if the switchover is success
            False if the switchover fails
        """
        res = self.cli(
            command="redundancy force-switchover %s" % options,
            pattern=r"(Proceed with switchover?|This will reload the active"
                    "unit and force switchover to standby).*").response()
        if not res or re.search(r'error', res):
            self.log(level='error',
                     message="redundancy force-switchover command failed")
            return False
        self.execute(command='',
                     pattern=r".?|connection (?:to \S+ )?closed.*")
        ping_result = {}
        while timeout >= 0:
            time.sleep(wait)
            ping_result = ping(device=self, host=self._kwargs['host'],
                               count=10, timeout=timeout)
            if ping_result.get('reachable'):
                break
            timeout = timeout - wait
        if not ping_result.get('reachable'):
            self.log(level='ERROR', message="Failed to ping router %s" % self._kwargs['host'])
            return False
        time.sleep(30)
        if not self.reconnect():
            self.log(level='ERROR', message="Failed to login to router after "
                                            "redundancy force-switchover")
            return False
        self.log(level='INFO', message="Router successfully Done a redundancy "
                                       "force-switchover")
        return True

    def load_config(self, option=None, local_file=None,
                    remote_file='startup-config', timeout=20):
        """
        Loads configuration using file or string to the routing
        :param option:
            *OPTIONAL* Load Options.
            Supported values are 'merge,'replace','override'.
        :param local_file:
            **REQUIRED** Path to a config file on local server
        :param remote_file:
            *OPTIONAL* Path to a config file on a remote server
            (on current device)
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :return:
            True in case configurtion is loaded successfully, else False
        """
        if not local_file:
            raise TobyException('Please specify the local file', host_obj=self)
        if option:
            load_cmd = "copy %s %s %s" % (option, local_file, remote_file)
        else:
            load_cmd = "copy %s %s" % (local_file, remote_file)
        load_config_result = False
        self.log(level="In load_config function: %s" % load_cmd)
        result = self.cli(command=load_cmd, pattern=[r'error.*',
                                                     r'Destination.*',
                                                     r'updated commit.*'],
                          timeout=timeout).response()
        if re.search(r'Destination.*', result, re.I):
            result = self.execute(command='',
                                  pattern=[r'ERROR.*', r'.*confirm].*',
                                           r'bytes copied in.*',
                                           r'.*OK].*'],
                                  timeout=timeout)
            if re.search(r'confirm', result, re.I):
                result = self.execute(command='',
                                      pattern=[r'ERROR.*', r'bytes copied.*',
                                               r'.*OK].*'],
                                      timeout=timeout)
            if re.search(r'(OK|bytes copied|#)', result, re.I):
                self.log(level='INFO',
                         message='Successfully loaded the configuration'
                         ' file into device')
                load_config_result = True
            else:
                self.log(level='DEBUG',
                         message='Failed to load the config file')
        else:
            self.log(level='DEBUG', message='Failed to load the config file')

        return load_config_result

    def get_version(self):
        """
        get current version of router software on host
        :return:
            returns router version
        """
        version = ''
        response = self.cli(command='show version', timeout=60).response()
        lines = response.split('\n')
        for line in lines:
            ver = re.search(r'Version\s+([^\s,]+)', line, re.I)
            if ver:
                version = ver.group(1)
                break
        self.log(level='INFO', message='get_version: Returning version:%s' % version)
        return version

    def get_interface_address(self, interface=None, interface_type=None,
                              family=None):
        """
        Get interface address from the router
        :param interface:
            *REQUIRED* name of the interface to get the address
        :param interface_type:
            *OPTIONAL* type of interface ex: link-local
        :param family:
            *OPTIONAL* interface belongs to which family ex:6, 4
        :return:
            IP address of the interface with subnetmask
        """
        if not interface:
            raise TobyException("Please specify the interface", host_obj=self)
        if family and str(family) == '6':
            family = 'ipv6'
        else:
            family = 'ip'
        response = self.cli(
            command="show %s interface %s" % (family, interface)).response()
        search_error = re.search(
            r'(?:invalid|incomplete)\s+(?:input|command)', response, re.I)
        if not response or search_error:
            raise TobyException("Error in executing the show interface command", host_obj=self)
        output = response.split('\n')
        interface_address = ""
        if family == 'ipv6':
            if re.search('link-local', interface_type, re.I):
                for line in output:
                    search = re.search(r'link-local address is (\S*)',
                                       line, re.I)
                    if search:
                        interface_address = search.group(1)
            else:
                for line in range(0, len(output)):
                    search = re.search('Global unicast address.*$',
                                       output[line], re.I)
                    if search:
                        search1 = re.search(r'(\S*), subnet is [^/]+(/\d+)',
                                            output[line + 1], re.I)
                        if search1:
                            interface_address = \
                                search1.group(1) + search1.group(2)
        else:
            for line in output:
                search = re.search(r'Internet address is (\S*)', line, re.I)
                if search:
                    interface_address = search.group(1)
        return interface_address

    def upgrade(self, url='flash', image=None, timeout=300):
        """
        upgrade image for IOS device
        :param url:
            *OPTIONAL* url of image (string). It can be inculed image or not
        :param image:
            *OPTIONAL* image to upgrade (string). If not defined, image have to
            include in url
        :param timeout:
            *OPTIONAL* timeout for connecting to device. Default: 300

        :returns:
            TRUE if upgrade to new image sucessfully
            FALSE if upgrade to new image unsucessfully
        """
        file_in_url = False
        if not image:
            match = re.search(r'.*(\:|\/)(\S+)$', url)
            if match:
                file_in_url = True
                image = match.group(2)
            else:
                self.log(level="Error", message="image value in url is required")
                return False

        current_image = get_image(device=self)
        match = re.search(r'.*(\:|\/)(\S+)$', current_image)
        if match:
            current_image = match.group(2)
            self.log(level="info",
                     message="Current image file: %s" % current_image)
        else:
            self.log(level="Error", message="Could not detect running image name")
            return False
        if re.search(image, current_image, re.I):
            self.log(level="info", message="Image %s already running, "
                     "no action taken" % image)
            return True
        self.config(command_list=["no boot system"], timeout=10)
        if file_in_url:
            cmd = "boot system %s" % url
        else:
            cmd = "boot system %s %s" % (url, image)
        response = self.config(command_list=[cmd], timeout=10).response()
        if re.search(r'Invalid|error', response, re.I):
            self.log(level='ERROR', message='Cannot apply config %s' % cmd)
            return False
        time_now = datetime.datetime.now()
        result = self.reboot(timeout=timeout, interval=10)
        if not result:
            self.log(level="ERROR", message="Can not reboot device")
            return False
        newtime = datetime.datetime.now() - time_now
        self.log(level="info", message="Finished after approx %s" % newtime)

        current_image = get_image(device=self)
        match = re.search(r'.*(\:|\/)(\S+)$', current_image)
        if match:
            current_image = match.group(2)
            self.log(level="INFO", message="Image %s already running" % current_image)
        else:
            self.log(level="ERROR", message="Could not detect running image name")
            return False

        if re.search(image, current_image, re.I):
            self.log(level="INFO", message="Successfully in upgrage image %s" % image)
            return True
        self.log(level="WARN", message="Unsuccessfully in upgrage image %s" % image)
        return False

    def kill_process(self, pid=None, signal=None):
        """
        Uses to kill the process
        :param pid:
            *REQUIRED* Process ID to kill
        :param signal:
            *OPTIONAL* Kill process signal
        :returns
            Response - if the kill process is success
            False - If the kill process if failes
        """
        if not pid:
            raise TobyException("Please specify the pid", host_obj=self)
        if not signal:
            signal = 9
        response = self.cli(
            command='kill -%s %s' % (pid, signal)).response()
        if response:
            self.log(level='INFO',
                     message='Kill the %s process ID' % pid)
            return response
        else:
            self.log(level="DEBUG",
                     message="Unable to kill the process ID")
            return False

    def clean_config(self, config_file='baseline-config.conf'):
        """
        This API use to clean config of router by load a config
        in flash|slot0|slo1 or on tftp server
        :param config_file
            **OPTIONAL** config file name for loadding
        :return True/False
        """
        self.cli(command="cd flash:")
        res = self.cli(command='dir').response()
        if re.search(config_file, res):
            result = self.load_config(local_file=config_file)
            return result
        else:
            self.cli(command="cd slot0:")
            res = self.cli(command='dir').response()
        if re.search(config_file, res):
            result = self.load_config(local_file=config_file)
            return result
        else:
            self.cli(command="cd slot1:")
            res = self.cli(command='dir').response()
        if re.search(config_file, res):
            result = self.load_config(local_file=config_file)
            return result
        else:
            self.cli(command="cd flash:")
            host = re.sub(r'\..*$|-con.*', "", self._kwargs['host'])
            labs = glob.glob("/volume/labtools/lab_cvs/*/machine/%s" % host)
            if os.path.exists(labs[0]):
                lab = re.sub(r"/volume/labtools/lab_cvs/|/machine/%s" % host,
                             "", labs[0])
            else:
                self.log(level="error", message="Can not finf %s on tftp "
                         "server" % config_file)
                return False

            self.log(level='WARN', message="Could not load %s on local, "
                     "trying tftp" % config_file)
            os.system("cp -f /volume/labtools/lab_cvs/%s/machine/$host/"
                      "cisco-config /volume/tftpboot/JT/%s-config.$$"
                      % (lab, host))
            if not os.path.exists('/volume/tftpboot/JT/%s-config.$$' % host):
                self.log(level='error', message="Failed to copy cisco config "
                         "for %s into tftpboot" % host)
                return False
            # tftp here
            self.cli(
                command="copy tftp://tftp.juniper.net/JT/%s-config.$$ %s"
                % (host, config_file), pattern=r"Destination filename.*\?")
            self.execute(command='', pattern=[r"bytes copied in.*",
                                              r'[confirm].*', r"error.*"])
            res = self.execute(cmd='n', pattern=[r"bytes copied in.*",
                                                 r"error.*"])
            # tftp done
            if not re.search(r"error", res, re.I):
                self.log(level='INFO', message="startup-config was "
                         "successfully transferred")
                result = self.load_config(local_file=config_file)
                return result
            else:
                return False
