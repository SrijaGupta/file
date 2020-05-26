"""
Unix.py script
"""
import logging
import os
import re
import time
from select import select

from jnpr.toby.hldcl.connectors.sshconn import SshConn
from jnpr.toby.hldcl.connectors.telnetconn import TelnetConn

import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.hldcl.connectors.common import check_socket
from jnpr.toby.hldcl.host import Host
from jnpr.toby.utils.response import Response
from jnpr.toby.exception.toby_exception import TobyException, TobyConnectLost
import socket

def _build_proxy_hosts_stack(kvargs):
    """
    Used to build a list of hosts to hop to when proxy involved
    """
    if 'proxy_host' in kvargs:
        single_proxy = {}
        single_proxy['port'] = int(kvargs.get('proxy_port', 22))
        single_proxy['host'] = kvargs.get('proxy_host')
        single_proxy['user'] = kvargs.get('proxy_user', kvargs.get('user'))
        single_proxy['password'] = kvargs.get('proxy_password', kvargs.get('password'))
        single_proxy['ssh_key_file'] = kvargs.get('proxy_ssh_key_file', None)
        hosts = []
        hosts.append(single_proxy)
    else:
        hosts = kvargs['proxy_hosts']

    #indicates still need to add new element to list for final target device
    if 'host' in hosts[-1] and hosts[-1]['host'] != kvargs.get('host'):
        final_target = {}
        final_target['port'] = int(kvargs.get('port', 22))
        final_target['host'] = kvargs.get('host')
        final_target['user'] = kvargs.get('user')
        final_target['password'] = kvargs.get('password')
        final_target['ssh_key_file'] = kvargs.get('ssh_key_file', None)
        hosts.append(final_target)
    else: # merge in data with users connect_command
        hosts[-1]['host'] = kvargs.get('host')
        hosts[-1]['port'] = int(kvargs.get('port', 22))
        hosts[-1]['ssh_key_file'] = kvargs.get('ssh_key_file', None)
        if 'user' not in hosts[-1]:
            hosts[-1]['user'] = kvargs.get('user')
        if 'password' not in hosts[-1]:
            hosts[-1]['password'] = kvargs.get('password')

    for i in range(1, len(hosts)):
        if 'port' not in hosts[i]:
            hosts[i]['port'] = 22
        if 'expected_prompt_substr' not in hosts[i]:
            hosts[i]['expected_prompt_substr'] = ['$', '>', '#', '%']
        if 'connect_command' in hosts[i]:
            pattern = re.compile(r'\$host')
            hosts[i]['connect_command'] = pattern.sub(hosts[i]['host'], hosts[i]['connect_command'])
            if hosts[i]['user']:
                pattern = re.compile(r'\$user')
                hosts[i]['connect_command'] = pattern.sub(hosts[i]['user'], hosts[i]['connect_command'])
            if hosts[i]['password']:
                pattern = re.compile(r'\$password')
                hosts[i]['connect_command'] = pattern.sub(hosts[i]['password'], hosts[i]['connect_command'])
            if hosts[i]['ssh_key_file']:
                pattern = re.compile(r'\$ssh_key_file')
                hosts[i]['connect_command'] = pattern.sub(hosts[i]['ssh_key_file'], hosts[i]['connect_command'])
        else:
            ssh_cmd = 'ssh -o StrictHostKeyChecking=no'
            if hosts[i]['user']:
                ssh_cmd += ' -l ' + hosts[i]['user']
            if hosts[i]['ssh_key_file']:
                ssh_cmd += ' -i ' + hosts[i]['ssh_key_file']
            ssh_cmd += ' ' + hosts[i]['host']
            hosts[i]['connect_command'] = ssh_cmd

    return hosts

def _connect_unix(kvargs):
    """
    _connect_unix function
    Used to connect to Unix device
    """
    if kvargs.get('connect_targets') == "console":
        host = kvargs.get('con-ip')
    else:
        host = kvargs.get('host')

    connect_mode = kvargs.get('connect_mode', 'ssh')
    osname = kvargs.get('osname', 'unix')
    connect_timeout = kvargs.get('timeout', '30')
    try:
        if connect_mode == 'ssh':
            if 'proxy_host' in kvargs or 'proxy_hosts' in kvargs:
                proxy = True
                hosts = _build_proxy_hosts_stack(kvargs)
                # build SshConn to proxy instead of final target resource
                t.log(level="INFO", message='Trying to connect to device ' + hosts[0]['host'] + ' via SSH ...')
                handle = SshConn(host=hosts[0]['host'],
                                 user=hosts[0]['user'],
                                 password=hosts[0]['password'],
                                 port=int(hosts[0].get('port', 22)),
                                 ssh_key_file=hosts[0].get('ssh_key_file', None))
                tnh = handle.client
                # now hop from host to host to get to final target
                for i in range(1, len(hosts)):
                    t.log(level="INFO", message='Proxy connection - ' + hosts[i]['connect_command'])
                    res = tnh.send(hosts[i]['connect_command'] + '\r')

                    # if user has specified a password key as 'None', it indicates a password-less
                    # login to the host. Below condition is executed when password is not None
                    if hosts[i]['password'] and hosts[i]['password'] != "None" and not hosts[i]['ssh_key_file']:
                        t.log(level="INFO", message="PASSWORD: " + hosts[i]['password'])
                        got = ''
                        # read the channel until password prompt is thrown
                        t.log(level="DEBUG", message="waiting for password prompt")
                        while True:
                            read, write, err = select([tnh], [], [], 10)
                            if read:
                                data = tnh.recv(1024)
                                data = data.decode("utf-8")
                                got = got + data

                                t.log(level="DEBUG", message="Read Data:\n---\n%s\n---" % data)
                                # in case the connect command is 'ssh' and we are prompted with a
                                # key update, go ahead and pass 'yes' and continue waiting on the
                                # until password prompt appears
                                if re.search(r"Are you sure you want to continue connecting \(yes/no\)", data):
                                    tnh.send("yes\r")

                                # if password prompt appears, send password and break this loop
                                if re.search(r'assword', data):
                                    res = tnh.send(hosts[i]['password'] + '\r')
                                    break

                    pattern = hosts[i]['expected_prompt_substr']
                    pattern = "(" + ")|(".join(pattern) + ")"
                    got = ''
                    while True:
                        read, write, err = select([tnh], [], [], 10)
                        if read:
                            data = tnh.recv(1024)
                            data = data.decode("utf-8")
                            got = got + data
                            if re.search(re.compile(pattern), data):
                                break

            else:
                text_port = kvargs.get('text_port', None)
                if text_port is not None:
                    text_port = int(text_port)
                    t.log(level='info', message="using text port: " + str(text_port))
                t.log(level="INFO", message='Trying to connect to device ' + str(host) + ' via SSH ...')
                handle = SshConn(host=host, user=kvargs['user'], port=text_port, \
                                 password=kvargs['password'], ssh_key_file=kvargs.get('ssh_key_file', None))

        else:
            t.log(level="INFO", message='Trying to connect to device ' + host + ' via Telnet ...')
            handle = TelnetConn(host=host, user=kvargs['user'],
                                password=kvargs['password'], connect_timeout=connect_timeout)
    except:
        raise TobyException("Cannot connect to %s Device %s" % (osname, host))

    return handle

class Unix(object):
    """
    Unix class
    """
    @staticmethod
    def __new__(cls, **kvargs):
        """
        Static method that returns a device object of class CentOS, FreeBSD, or
        Ubuntu.
        :param host:
            **REQUIRED** hostname or IP address of device to telnet to
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param password:
            *OPTIONAL* Login Password. If not provided will be derived from
            Toby framework defaults.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is ssh. Supported
            values are telnet/ssh
        :param model:
            *OPTIONAL* Unix model of device to connect
        :return: Device object based on os and model

        """

        if 'host' not in kvargs:
            raise TobyException("Mandatory Parameter host missing")
        #username and password are not specified by caller
        if not kvargs['user']:
            kvargs['user'], kvargs['password'] = credentials.get_credentials(os=kvargs['osname'])

        if kvargs.get('connect_targets') == "console":
            host = kvargs.get('con-ip')
        else:
            host = kvargs.get('host')

        connect_mode = kvargs.get('connect_mode', 'ssh')
        cls.handle = ''
        # returns appropiate handle for device connection
        cls.handle = _connect_unix(kvargs)

        if connect_mode == 'ssh':
            kvargs['port'] = 22
            tnh = cls.handle.client
            try:
                if tnh.recv_ready():
                    tnh.in_buffer.empty()
                tnh.send('uname -sr\n')
                time.sleep(1)
            except Exception as exp:
                message="Failed to send command '%s' to %s: %s" % ('uname -sr', host, exp.__str__())
                raise TobyConnectLost(message=message)
            got = ''
            while True:
                read, write, err = select([tnh], [], [], 10)
                if read:
                    data = tnh.recv(1024)
                    data = data.decode("utf-8")
                    got = got + data
                    if re.search(r'(\$|>|#|%)[\s\t]?$', data):
                        break
            if re.search('FreeBSD', got, flags=re.IGNORECASE):
                unix_flavour = 'FreeBSD'
            elif re.search('Linux', got, flags=re.IGNORECASE):
                unix_flavour = 'CentOS'
            else:
                if 'model' in kvargs:
                    unix_flavour = kvargs['model']
                else:
                    unix_flavour = 'Unknown'
            if 'model' in kvargs and kvargs['model']=='sifos':
                unix_flavour = 'Sifos'
        else:
            kvargs['port'] = 23
            unix_flavour = cls._get_unix_flavour(cls)

        if 'model' in kvargs:
            kvargs['unix_flavour'] = kvargs['model']

        if unix_flavour:
            if unix_flavour.upper() == 'CENTOS':
                unix_handle = CentOS(handle=cls.handle, **kvargs)
            elif unix_flavour.upper() == 'FREEBSD':
                unix_handle = FreeBSD(handle=cls.handle, **kvargs)
            elif unix_flavour.upper() == 'UBUNTU':
                unix_handle = UnixHost(handle=cls.handle, **kvargs)
            elif unix_flavour.upper() == 'LINUX':
                unix_handle = UnixHost(handle=cls.handle, **kvargs)
            elif unix_flavour.upper() == 'SIFOS':
                unix_handle = Sifos(handle=cls.handle, **kvargs)
                return unix_handle
            else:
                raise TobyException("Invalid Unix model detected: '%s'" % unix_flavour)
        else:
            raise TobyException("Invalid Unix model detected: '%s'" % unix_flavour)

        prompt = 'Toby-%s-%s%% ' % (os.getpid(), unix_handle.host)
        unix_handle.set_prompt(prompt)
        return unix_handle

    def _get_unix_flavour(cls):
        """
        Private method to return Unix flavor of device
        :param: handle
            **Required** Handle of Unix device.
        :return: Unix flavor of device.
        """
        cls.handle.write(b'uname -sr\r\n')
        response = cls.handle.expect([br'\$\s', br'%[\s]?', br'#[\s]?'], timeout=20)
        if response[0] == -1:
            raise TobyException("Expected $ or %% or # but instead got:\r\n'%s'"
                                % (response[2].decode('utf-8')))
        unix_flavour = ''
        if re.search('Linux', response[2].decode('utf-8')):
            unix_flavour = 'CentOS'
        else:
            if re.search('FreeBSD', response[2].decode('utf-8')):
                unix_flavour = 'FreeBSD'
        if unix_flavour == '':
            logging.info('CONNECTED DEVICE HAS UNKNOWN UNIX FLAVOR')
            unix_flavour = 'Unknown'
        return unix_flavour

class UnixHost(Host):
    """
    Class housing a static method that returns an object of class TelnetConn or
    SshConn.

    """
    def __init__(self, **kwargs):
        """
        Creates the device object if its Unix flavour is unknown
        :param kwargs:
        :return:
        """
        self._kwargs = kwargs
        self.model = kwargs.get('unix_flavour')
        kwargs['os'] = kwargs.get('osname')
        super(UnixHost, self).__init__(**kwargs)
        self.handle = kwargs.get('handle')
        self.connected = 1
        self.shelltype = 'sh'
        self.response = ''
        self.prompt = "\$ "
        self.version = None
        self.close_obj = None
        self.port = kwargs.get('port')
        self.mode = "shell"

    def execute(self, **kvargs):
        """
        Internal method for executing command

        :param command:
            **REQUIRED** string command to be sent to the device
        :param pattern:
            *OPTIONAL* Output will be collected till this pattern is found.
        :param timeout:
            *OPTIONAL* Time by which output is expected. Default is
            set based on os/platform/model of the box
        :return: Index of the pattern matched. -1 if not match

        """
        kw_call = kvargs.pop('kw_call', False)
        kvargs['pattern'] = kvargs.get('pattern', self.prompt)
        if 'command' not in kvargs:
            raise TobyException('Command for device not specified', host_obj=self)
        kvargs['device'] = self
        kvargs['cmd'] = kvargs.pop('command')
        kvargs['timeout'] = kvargs.get('timeout', self.shell_timeout)
        return_value = self.handle.execute(**kvargs)
        return return_value

    def shell(self, *args, **kvargs):
        """
        Method called by user to send a string command to device and save its
        response.

        :param command:
            **REQUIRED** string command to be sent to the device
        :param pattern:
            *OPTIONAL* Output will be collected till this pattern is found.
        :param timeout:
            *OPTIONAL* Time by which output is expected. Default is
            set based on os/platform/model of the box
        :return: response from device. exception if timeout seen

        """
        if 'command' not in kvargs:
            raise TobyException('Command for device not specified', host_obj=self)
        try:
            kvargs['timeout'] = kvargs.get('timeout', self.shell_timeout)
            patt_match = self.execute(*args, **kvargs)
            if patt_match == -1:
                raise TobyException('Timeout seen while retrieving output', host_obj=self)
            else:
                return_value = Response(response=self.response)
                return return_value
        except:
            raise TobyException("Timeout seen while retrieving output", host_obj=self)

    def close(self):
        """
        Device object destroyer
        """
        self.disconnect()

        try:
            del self
        except NameError as Exception:
            raise TobyException("self not defined for deleting")
        except:
            raise TobyException("Unable to destroy Unix object")

        return True

    def disconnect(self):
        """
        Disconnect
        """
        try:
            if self.connect_mode == 'ssh':
                if self.close_obj:
                    self.close_obj.close()
                else:
                    self.handle.client.close()
            else:
                self.handle.close()
            self.connected = 0
            t.log(level='info', message='Successfully closed Device Handle')
        except:
            raise TobyException("Unable to disconnect Device handle", host_obj=self)

        return True

    def set_prompt(self, prompt):
        """
        Method called by Unix new or user to set device prompt
        :param prompt: prompt to set on the device
        :return: True if set prompt is successful.
                 In all other cases Exception is raised
        """
        res = self.execute(command='echo "$shell $SHELL"', pattern=[r'\$[\s]?$', r'%[\s]?', r'#[\s]?', r'>[\s]?', self.prompt])
        if res == -1:
            raise TobyException("Unable to get shell type on device. Device prompt not set", host_obj=self)
        shell = self.response
        self.log(level='DEBUG', message=shell)
        if re.search(r'\/bin\/sh', shell, re.IGNORECASE):
            cmd = 'PS1="' + prompt + '"'
            self.shelltype = 'sh'
        elif re.search(r'\/bin\/bash', shell, re.IGNORECASE):
            cmd = 'PS1="' + prompt + '"'
            self.shelltype = 'sh'
        elif re.search('csh', shell, re.IGNORECASE):
            cmd = 'set prompt="' + prompt + '"'
            self.shelltype = 'csh'
        else:
            raise TobyException("Connected device has unknown shell;  Device prompt not set", host_obj=self)

        res = self.execute(command=cmd, pattern=prompt)
        if res == -1:
            raise TobyException("Error setting Device prompt", host_obj=self)
        self.prompt = prompt
        return True

    def su(self, **kwargs):
        """
        Method called by user to login as root

        :param password:
            *OPTIONAL* Super user Password. If not provided will be derived
            from Toby framework defaults.
        :return: True if able to change to root user. In
                 all other cases Exception is raised
        """
        su_command = kwargs.get('su_command', 'su -')
        try:
            whoami_resp = self.shell(command='whoami').response()
            if re.search(r'root', whoami_resp, re.I):
                self.log(level='INFO', message="user is already 'root'")
                return True
            res = self.execute(command=su_command, pattern=["# ", "#", "Password: ", "Password:", self.prompt])
            if res == -1:
                raise TobyException('Error switching to root user', host_obj=self)
            if 'password' in kwargs:
                su_password = kwargs['password']
            else:
                su_user, su_password = self.get_su_credentials()
            res = self.execute(command=su_password, pattern=["# ", "#", "Password: ", "Password:", self.prompt])
            if res == -1:
                raise TobyException("Invalid Password", host_obj=self)
            self.set_prompt(self.prompt)
            if self.shell(command='whoami').response().find('root') == -1:
                raise TobyException("Wrong superuser password!", host_obj=self)
        except:
            raise TobyException("Not able to switch to root user", host_obj=self)
        return True

    def reboot(self, wait=60, timeout=1200, interval=30, mode=None, device_type=None, system_nodes=None, command_args=None):
        """
        Method called by user to reboot the Host
        :param wait:
            *OPTIONAL* Time to sleep before reconnecting, Default value is 60
        :param timeout:
            *OPTIONAL* Time by which device need to reboot. Default is
            1200 seconds
        :param interval:
            *OPTIONAL* Interval at which reconnect need to be attempted after
            reboot is performed. Default is 30 seconds
        :return: True if device reboot is successful. In
            all other cases Exception is raised
        """
        try:
            self.su()
            try:
                res = self.shell(command="reboot", pattern='', timeout=2)
            except:
                pass
            self.log(message='Sent the reboot command to %s' % self.host)
            time.sleep(5)
            if self.is_alive():
                raise TobyException('Device %s did not go down after executing a reboot: FAIL' % self.host, host_obj=self)
            else:
                self.log(level='INFO', message='Device reboot initiated for this particular platform/function')
                self.reconnect(timeout=timeout, interval=interval)
        except:
            raise TobyException("Reboot Failed", host_obj=self)
        return True

    def reconnect(self, timeout=30, interval=10, force=True):
        """
        Method called by user to reconnect to Host
        :param timeout:
            *OPTIONAL* Time by which device need to reconnect. Default is
            30 seconds
        :param interval:
            *OPTIONAL* Interval at which reconnect need to be attempted.
            Default is 10 seconds
        :return: True if device reconnection is successful. In
            all other cases Exception is raised
        """
        if force is True:
            try:
                oldprompt = self.prompt
                self.prompt = '\$'

                if 'proxy_host' not in self._kwargs and 'proxy_hosts' not in self._kwargs:
                    self.log(level='INFO', message="Now checking %s's %s server.." % (self.host, self.connect_mode))
                    if check_socket(host=self.host, socket_type=self.connect_mode, timeout=timeout, interval=interval):
                        self.log(level='INFO', message='Successfully created %s socket to %s' %
                                 (self.connect_mode, self.host))
                    else:
                        raise TobyException('Failed to create %s socket to %s' %
                                            (self.host, self.connect_mode), host_obj=self)

                if self.connect_mode == 'ssh':
                    if self.handle.client.get_transport().isAlive():
                        self.handle.client.close()

                self.handle = _connect_unix(self._kwargs)

                self.set_prompt(oldprompt)
            except:
                raise TobyException("Error reconnecting to Device", host_obj=self)
            return True
        else:
            try:
                if self.handle.client.get_transport().isAlive():
                    self.log(level='INFO', message='Unix channel is alive')
                    return True
            except:
                pass

    def is_alive(self):
        """
        Function to find if a handle is active or not
        """
        # if 'text' in self.channels:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_timeout = 5
            sock.settimeout(socket_timeout)
            sock.connect((self.host, self.port))
            sock.close()
            self.log('Device Port Scan: Port ' + str(self.port) + ' is listening')
            return True
        except socket.error as err:
            self.log('Device Port Scan: Port ' + str(self.port) + ' is NOT listening: ' + str(err))
        return False

    def get_model(self):
        '''
        Gets the model info from the Linux devices.
        '''
        if hasattr(self, 'model') and self.model != None:
            return self.model
        else:
            try:
                res = self.shell(command='cat /etc/issue')
                match = re.search(r'^(\S+).*', res.response())
                if match:
                    self.model = match.group(1)
                    return self.model
                else:
                    return None
            except:
                raise TobyException("Could not get model info", host_obj=self)

    def get_version(self):
        '''
        Gets the version info from the host devices.
        '''
        if hasattr(self, 'version') and self.version != None:
            return self.version
        else:
            try:
                res = self.shell(command='uname -r')
                match = re.search(r'^(\S+).*', res.response())
                if match:
                    self.version = match.group(1)
                    return self.version
                else:
                    return None

            except:
                raise TobyException("Could not get version info", host_obj=self)

class Sifos(UnixHost):
    """
    Class to create an object representing a FreeBSD device.

    """
    def __init__(self, *vargs, **kvargs):
        """
        Sends received arguments straight to Host.__init__ to set object
        attributes

        :param host:
            **REQUIRED** hostname or IP address of device to telnet to
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            values are telnet/ssh
        :param os:
            **REQUIRED** OS of the device

        """
        super(Sifos, self).__init__(**kvargs)
        prompt = 'Toby-%s-%s%% ' % (os.getpid(), self.host)
        self.std_shell_path = '/root/PowerShell_TCL.SH'
        self.set_prompt(prompt)
        self.shell(command=kvargs.get('sifos_shell_path', self.std_shell_path), pattern="'N' to alter...")
        self.shell(command='N', pattern='Enter IP Address of PSA To Connect:')
        self.shell(command=kvargs.get('sifos_ip'), pattern='>')
        if kvargs.get('sifos_ip'):
            self.shell(command='psa %s'%kvargs.get('sifos_ip'), pattern='>')
        else:
            raise TobyException('Missing mandatory framework variable fv-sifos-ip')

class FreeBSD(UnixHost):
    """
    Class to create an object representing a FreeBSD device.

    """
    def __init__(self, *vargs, **kvargs):
        """
        Sends received arguments straight to Host.__init__ to set object
        attributes

        :param host:
            **REQUIRED** hostname or IP address of device to telnet to
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            values are telnet/ssh
        :param os:
            **REQUIRED** OS of the device

        """
        super(FreeBSD, self).__init__(*vargs, **kvargs)


    def get_model(self):
        '''
        Gets the model info from the FreeBSD boxes.
        '''
        if hasattr(self, 'model') and self.model != None:
            return self.model
        else:
            try:
                res = self.shell(command='uname -a')
                match = re.search(r'^(\S+).*', res.response())
                if match:
                    self.model = match.group(1)
                    return self.model
                else:
                    return None
            except:
                raise TobyException("Could not get model info", host_obj=self)


class CentOS(UnixHost):
    """
    Class to create an object representing a CentOS device.

    """

    def __init__(self, **kvargs):
        """
        Sends received arguments straight to Host.__init__ to set object
        attributes

        :param host:
            **REQUIRED** hostname or IP address of device to telnet to
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            values are telnet/ssh
        :param os:
            **REQUIRED** OS of the device

        """

        super(CentOS, self).__init__(**kvargs)
