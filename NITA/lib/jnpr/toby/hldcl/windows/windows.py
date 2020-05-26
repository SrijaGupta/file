"""
    Windows Class
"""
import os
import time
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.hldcl.connectors.telnetconn import TelnetConn
from jnpr.toby.hldcl.connectors.common import check_socket
from jnpr.toby.hldcl.host import Host
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.connectors.sshconn import SshConn
from jnpr.toby.exception.toby_exception import TobyException

class Windows(Host):
    """
    Class housing a static method that returns an object of class TelnetConn or
    SshConn.

    """
    def __init__(self, **kwargs):
        """
        :param host:
            **REQUIRED** hostname or IP address of device to telnet to
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param password:
            *OPTIONAL* Login Password. If not provided will be derived from
            Toby framework defaults.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            value is telnet.
        """
        if 'host' not in kwargs:
            raise TobyException("Mandatory Parameter host missing")
        # if username and password are not specified by caller
        kwargs['os'] = kwargs.get('osname', 'WINDOWS')
        if not kwargs.get('user', None):
            kwargs['user'], kwargs['password'] = credentials.get_credentials(os=kwargs.get('osname', 'WINDOWS'))
        host = kwargs.get('host')
        connect_mode = kwargs.get('connect_mode', 'telnet')
        super(Windows, self).__init__(**kwargs)
        self.log(message='Trying to connect to device ' + host + ' via ' + connect_mode + ' ...')
        self.prompt = 'Toby-%s-%s' % (os.getpid(), host)
        self.prompt += '%'
        self.port = kwargs.get('text_port')
        try:
            if connect_mode == 'ssh':
                self.prompt = '>\s?'
                handle = SshConn(host=host, user=kwargs['user'], password=kwargs['password'], initialize_command='cd')
            else:
                handle = TelnetConn(host=host, user=kwargs['user'],
                                    password=kwargs['password'], port=self.port)
            self.handle = handle
            self.log(message='Connection to ' + host + ' via ' + connect_mode + ' is successful.')
        except:
            raise TobyException("Cannot connect text channel via %s to %s Device %s" % (connect_mode, kwargs['os'], host), host_obj=self)

        if self.port == 23:
            self.set_shell_prompt(prompt=self.prompt)
        else:
            self.prompt = '>\s?'
        self.connected = 1
        self.response = ''
        self.mode = 'shell'

    def set_shell_prompt(self, prompt):
        """
        Internal method that sets the Windows shell prompt

        :param prompt: prompt to set on the device
        :return: True if set prompt is successful.
                 In all other cases Exception is raised
        """
        res = self.execute(command="prompt "+prompt, pattern=prompt)
        if res == -1:
            raise TobyException("Not able to set Windows shell prompt.", host_obj=self)
        return True

    def execute(self, *args, **kvargs):
        """
        Internal method for executing command

        :param command:
            **REQUIRED** string command to be sent to the device
        :param pattern:
            *OPTIONAL* Output will be collected till this pattern is found.
        :param timeout:
            *OPTIONAL* Time by which output is expected. Default is
            60 seconds
        :return: Index of the pattern matched. -1 if not match

        """
        kvargs['pattern'] = kvargs.get('pattern', self.prompt)
        if 'command' not in kvargs:
            raise TobyException('Command for device not specified', host_obj=self)
        kvargs['device'] = self
        kvargs['cmd'] = kvargs.pop('command')
        return_value = self.handle.execute(*args, **kvargs)
        return return_value

    def shell(self, *args, **kvargs):
        """
        Shell (DOS prompt) command
        """
        if 'command' not in kvargs:
            raise TobyException('Command for device not specified', host_obj=self)
        try:
            kw_call = kvargs.pop('kw_call', False)
            patt_match = self.execute(*args, **kvargs)
            if patt_match == -1:
                raise TobyException('Timeout seen while retrieving output', host_obj=self)
            else:
                return_value = Response(response=self.response[:self.response.rfind('\n')])
                return return_value
        except:
            raise TobyException("Timeout seen while retrieving output", host_obj=self)

    def close(self):
        """
        Device object destroyer
        """
        try:
            if self.connect_mode == 'ssh':
                self.handle.client.close()
            else:
                self.handle.close()
            self.connected = 0
        except:
            raise TobyException("Unable to close Device handle", host_obj=self)
        return True

    def reboot(self, wait=60, timeout=1200, interval=30):
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
            res = self.execute(command="shutdown -r", pattern='', no_response=1)
            if res == -1:
                raise TobyException("Error sending reboot command to Device", host_obj=self)
            self.log(message='Sent the reboot command to %s' % self.host)
            if not check_socket(host=self.host, negative=1,
                                socket_type=self.connect_mode):
                raise TobyException('Device %s did not go down after executing a reboot: FAIL' % self.host, host_obj=self)
            self.log(message='Device %s has gone down. '
                             'Waiting %s seconds before checking %s socket.' %
                     (self.host, wait, self.connect_mode))
            self.handle.close()
            time.sleep(wait)
            if not check_socket(host=self.host, socket_type=self.connect_mode,
                                timeout=timeout, interval=interval):
                raise TobyException('Device %s did not come back online. Reboot FAIL' % self.host, host_obj=self)
            time.sleep(10)
            self.reconnect()
        except:
            raise TobyException("Reboot Failed", host_obj=self)
        return True

    def reconnect(self, timeout=30, interval=10):
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
        try:
            self.log(level='INFO', message="Now checking %s's %s server.." %
                     (self.host, self.connect_mode))

            if check_socket(host=self.host, socket_type=self.connect_mode,
                            timeout=timeout, interval=interval):
                self.log(level='DEBUG', message='Successfully created %s socket to %s' %
                         (self.connect_mode, self.host))
            else:
                raise TobyException('Failed to create %s socket to %s' %
                                    (self.host, self.connect_mode), host_obj=self)

            if self.connect_mode == 'ssh':
                if self.handle.client.get_transport().isAlive():
                    self.handle.client.close()
                self.handle = SshConn(host=self.host, user=self.user, password=self.password, port=22, initialize_command='cd')
            else:
                self.handle = TelnetConn(host=self.host, user=self.user, password=self.password)

            if self.port == 23:
                self.prompt = 'Toby-%s-%s' % (os.getpid(), self.host)
                self.prompt += '%'
                self.set_shell_prompt(prompt=self.prompt)
            else:
                self.prompt = '>\s?'
        except:
            raise TobyException("Error reconnecting to Device", host_obj=self)
        return True
