"""
Class for Brocade Devices
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
from jnpr.toby.exception.toby_exception import TobyException

class Brocade(Host):
    """
    Generic Brocade class for common operations
    """

    def __init__(self, *args, **kwargs):
        """
        Base class for Brocade devices

        :param host:
            **REQUIRED** host-name or IP address of target device
        :param os:
            *OPTIONAL* Operating System of device. Default is BROCADE
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
        :return: Device object based on os and model
        """
        # Check if host is provided
        if 'host' not in kwargs:
            raise TobyException("'host' is mandatory", host_obj=self)

        if kwargs.get('connect_mode', '').lower() == 'console':
            kwargs['strict'] = True
        kwargs['os'] = kwargs.get('os', 'BROCADE')

        self._kwargs = kwargs
        self.connected = False
        self.mode = 'user'
        self.prompt = '>\s+'
        # call Device class init for common operations
        super(Brocade, self).__init__(*args, **kwargs)
        # Connect to device (telnet/ssh)
        self.log(level='info', message="Connecting to device")
        self.connect()
        self.connected = True

    def _connect(self):
        """
         Internal function to create the text channel for IOS devices.
         It will create text channel by telnet /ssh.
        """
        connection_class = None
        return_value = None
        port = self._kwargs.get('port', None)
        if self._kwargs.get('connect_mode', 'telnet').lower() == 'telnet':
            logging.info('Telnet connection')
            port = self._kwargs.get('port', 23)
            connection_class = TelnetConn
        elif self._kwargs.get('connect_mode').lower() == 'ssh':
            connection_class = SshConn
        else:
            self.log(message='Unknown connection mode '
                     '{0}'.format(self._kwargs['connect_mode']), level='ERROR')
            return return_value
        if not self.user:
            self.user = ''
        if not self.password:
            self.password = ''

        return_value = connection_class(host=self.host, user=self.user, password=self.password, port=port)
        return return_value

    def connect(self):
        """
        Function to create text channel for Brocade devices.
        Example:
        device_object.connect(host='hostname',user='username',password='password')
        """
        self.channel = self._connect()
        resp = self.execute(command="switchshow")
        self.log('Text connection successful')
        if re.search(r'Invalid|error', resp, re.I):
            self.log(level='ERROR', message='Error setting screen-width 0')
        else:
            self.log(level='INFO', message=resp)

    def execute(self, **kwargs):
        """
        Executes commands
        device_object.execute(command = 'switchshow')

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
        if response:
            self.log('Successfully closed Device Handle')
            del self
        return_value = response
        return return_value
