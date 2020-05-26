"""
Class for Junos Devices
"""
# import logging
import os
import re
import time
# from copy import copy
import xml.dom.minidom as xml_dom
from xml.etree import ElementTree as ET
from lxml import etree
from jnpr.junos.device import Device as Pyez_Device
from robot.libraries.BuiltIn import BuiltIn
from jnpr.junos import version as Pyez_version
# from jnpr.junos.utils.config import Config
# from jnpr.junos.utils.fs import FS
from jnpr.junos.exception import RpcError
from jnpr.toby.utils.response import Response, response_check
from jnpr.toby.hldcl.connectors.sshconn import SshConn
from jnpr.toby.hldcl.connectors.telnetconn import TelnetConn
from jnpr.toby.hldcl.host import Host
import jnpr.toby.utils.time_utils as Time
from jnpr.toby.hldcl.channels.grpcConn import Grpc
import pdb
import ruamel.yaml as yaml
from collections import defaultdict
from jnpr.toby.exception.toby_exception import TobyException, TobyConnectLost, DeviceModeSwitchException
import socket
from jnpr.junos.exception import RpcTimeoutError, ConnectClosedError, RpcError
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.utils.utils import check_device_scan

class Junos(object):
    """
    Class factory to create JunOS objects. Auto detects model and creates
    instances based on detected model.
    """

    def __new__(cls, *args, **kwargs):
        """
        Factory method to create classes based on OS and model

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
             *OPTIOANL* Model of device. Default is None.
        :param dual_re:
            *OPTIONAL* Connect to both the RE's. Default is False. Will return
            object which is connected to master RE.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            values are telnet/ssh/netconf/console
        :param connect_targets:
            *OPTIONAL* Connect to either console or management. Default is
            management. Supported values are console/management.
        :param mode:
            *OPTIONAL* Port on device to which connection needs to made.
        :param tag:
            *OPTIONAL* Tag to uniquely idetify the device object
        :param proxy_host:
            *OPTIONAL* hostname or IP address of the proxy.
        :param proxy_user:
            *OPTIONAL* Login user name of the proxy.
        :param proxy_password:
            *OPTIONAL* Login Password of the proxy.
        :param proxy_port:
            *OPTIONAL* Port on device to which connection needs to made
            to the proxy. Default: port=22
        :return: Device object based on os and model
        """

        if 'host' not in kwargs:
            raise TobyException("'host' is mandatory")

        # Create and return objects based on the model detected
        kwargs['model'] = str(kwargs.get('model'))
        model = kwargs.get('model').upper()
        if model.upper().startswith('MX') or model.upper().startswith('VMX'):
            if kwargs.get('vc'):
                from jnpr.toby.hldcl.juniper.routing.mxvc import MxVc
                return MxVc(*args, **kwargs)
            else:
                from jnpr.toby.hldcl.juniper.routing.mx import Mx
                return Mx(*args, **kwargs)
        elif model.upper().startswith('SRX') or \
                model.upper().startswith('HA_CLUSTER'):
            from jnpr.toby.hldcl.juniper.security.srx import Srx
            return Srx(*args, **kwargs)
        elif model.upper().startswith('VSRX'):
            from jnpr.toby.hldcl.juniper.security.srx import VSrx
            return VSrx(*args, **kwargs)
        elif model.upper().startswith('EX'):
            from jnpr.toby.hldcl.juniper.switching.ex import Ex
            return Ex(*args, **kwargs)
        elif model.upper().startswith('QFX') or \
                model.upper().startswith('VQFX'):
            from jnpr.toby.hldcl.juniper.switching.ex import Qfx
            return Qfx(*args, **kwargs)
        elif model.upper().startswith('NFX'):
            from jnpr.toby.hldcl.juniper.switching.ex import Nfx
            return Nfx(*args, **kwargs)
        elif model.upper().startswith('OCX'):
            from jnpr.toby.hldcl.juniper.switching.ex import Ocx
            return Ocx(*args, **kwargs)
        elif model.upper().startswith('JPG'):
            from jnpr.toby.hldcl.juniper.jpg.jpg import Jpg
            return Jpg(*args, **kwargs)
        elif model.upper().startswith('CRPD'):
            from jnpr.toby.hldcl.juniper.routing.crpd import Crpd
            return Crpd(*args, **kwargs)
        else:
            # This is added to default to Juniper class if the model does not
            # match any above
            # PTX, VPTX, EVO, ACX, M, T, AMX, JDM models are supported.
            return Juniper(*args, **kwargs)


class Juniper(Host):
    """
    Generic JunOS class for common operations
    """

    def __init__(self, *args, **kwargs):
        """

        Base class for JunOS devices

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
        :param dual_re:
            *OPTIONAL* Connect to both the RE's. Default is False. Will return
            object which is connected to master RE.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            values are telnet/ssh/netconf/console
        :param connect_targets:
            *OPTIONAL* Connect to either console or management. Default is
            management. Supported values are console/management.
        :param port:
            *OPTIONAL* Port on device to which connection needs to made.
        :param tag:
            *OPTIONAL* Tag to uniquely idetify the device object
        :param proxy_host:
            *OPTIONAL* hostname or IP address of the proxy.
        :param proxy_user:
            *OPTIONAL* Login user name of the proxy.
        :param proxy_password:
            *OPTIONAL* Login Password of the proxy.
        :param proxy_port:
            *OPTIONAL* Port on device to which connection needs to made to
            the proxy. Default: port=22
        :return: Device object based on os and model
        """

        # Check if host is provided
        if 'host' not in kwargs:
            raise TobyException("'host' is mandatory")

        if kwargs.get('connect_mode', '').lower() == 'console':
            kwargs['strict'] = True
        kwargs['os'] = kwargs.get('os', 'JUNOS')

        self.connect_channels = kwargs.get('connect_channels', 'all')

        self._kwargs = kwargs
        self.connected = False
        self.mode = 'shell'
        self.core_path = ["/var/crash/*core*", "/var/tmp/*core*", "/var/tmp/pics/*core*", "/var/core/*/*core*",
                          "/var/lib/ftp/in/*/*core*", "/var/crash/corefiles/*core*"]
        self.destination = None
        self.config_mode = ''
        self.prompt = ['$']
        self.evo = False
        self.readonly_user = None
        self.facts = dict()
        self.rebooted = False
        self.proxy = False
        self.major_version = None
        self.version = None
        self.model = None
        self.re_name = kwargs.get('re_name', None) # is passed down from node.py
        self.modes = dict() # stores all the modes' routes/patterns from yaml
        self.modes_yaml = dict() # store the original yaml
        self.custom_modes = dict() # stores all the custom modes
        self.custom_mode = None
        self.connect_to_pyez = True # only set to false if skipped
        if 'proxy_host' in kwargs or 'proxy_hosts' in kwargs:
            self.proxy = True

        # call Device class init for common operations
        super(Juniper, self).__init__(*args, **kwargs)
        self.reboot_timeout = 500
        self.upgrade_timeout = 1200
        self.issu_timeout = 1800

        pyez_connect = True
        text_connect = True
        # Initialize channels in device
        self.channels = dict()
        self.mibs_custom_dir = kwargs.get('mibs_custom_dir', None)
        self.powercyler_pattern = ".*Type the hot key to suspend the connection.*|login:.*"

        # Create the modes routes from yaml
        self.create_mode_routes()

        # Create PyEZ channel, but not if there is a 'jump host' proxy
        if not self.proxy and 'console' not in \
                kwargs.get('connect_targets', 'management') and \
                ('all' in self.connect_channels or 'pyez' in
                 self.connect_channels):
            self.log(level='INFO', message="Connecting to 'pyez' channel")
            # Connect to given hostname/IP via PyEZ
            self.log(level='INFO', message="PyEZ Version: " +
                     Pyez_version.VERSION + "(" + Pyez_version.DATE + ")")
            try:
                self._connect_pyez()
            except Exception as err:
                self.log(level="DEBUG", message="Could not connect to 'pyez' channel due to %s and "
                         "continuing to connect 'text' channel"%(str(err)))
                pyez_connect = False
            self.configObject = None

            # Local class to support calling RPC's as functions
            class local_rpc(object):
                """
                class local_rpc
                """
                call = None

                def __getattribute__(self, item, *iargs, **ikwargs):
                    """
                    __getattribute__ function
                    """
                    self.log(
                        level="info",
                        messaga='Sending RPC : {0} with arguments {1} and '
                        'keyword arguments {2}'.format(item, iargs, ikwargs))
                    fcall = getattr(self.channels['pyez'].rpc, '__getattr__')
                    local_rpc.call = fcall(item)
                    return local_rpc.rpc_call

                @staticmethod
                def rpc_call(*iargs, **ikwargs):
                    """
                    rpc_call function
                    """
                    response = local_rpc.call(*iargs, **ikwargs)
                    self.log(level='info', message='RPC Response:'
                             ' {0}'.format(etree.tostring(response)))
                    return response

            self.rpc = local_rpc()
        else:
            self.connect_to_pyez = False
            self.log(level="DEBUG", message="Skipping 'pyez' channel creation")

        # Create a text channel(telnet/ssh)
        if 'all' in self.connect_channels or 'text' in self.connect_channels:
            self.log(level="INFO", message="Connecting to 'text' channel")
            try:
                self._connect_text()
            except Exception as err:
                self.log(level="DEBUG", message="Could not connect to 'text' channel because of "+str(err))
                text_connect = False

        else:
            self.log(level="DEBUG", message="Skipping 'text' channel creation")

        # Check if device connection is failed
        if not pyez_connect or not text_connect:
            device_args = dict()
            device_args['host'] = kwargs.get('hostname') or kwargs.get('host')
            self.log(level="DEBUG", message='Diagonistic report since text/pyez failure occured '
                                           'for %s'%str(device_args['host']))
            device_args['channel'] = 'text'
            if self._kwargs.get('text_port'):
                device_args['port'] = self._kwargs.get('text_port')
            else:
                if self._kwargs.get('connect_mode', 'ssh') == 'telnet':
                    device_args['port'] = 23
                else:
                    device_args['port'] = 22
            check_device_scan(None, channels_check=False, **device_args)
            device_args['channel'] = 'pyez'
            device_args['port'] = self._kwargs.get('pyez_port') if self._kwargs.get('pyez_port') else 22
            check_device_scan(None, channels_check=False, **device_args)

        host_name = str(kwargs.get('hostname') or kwargs.get('host'))
        if pyez_connect is False:
            if text_connect is False:
                raise TobyException("Failed to connect to 'pyez' and 'text' channels, Could not establish "
                                    "connection to {} device {}".format(str(kwargs.get('osname')),
                                                                        host_name))
            else:
                raise TobyException("Failed to connect to 'pyez' channel, Could not establish connection to {} "
                                    "device {}".format(str(kwargs.get('osname')), host_name))
        else:
            if text_connect is False:
                raise TobyException("Failed to connect to 'text' channel, Could not establish connection to {} "
                                    "device {}".format(str(kwargs.get('osname')), host_name))

        # Check if device is a EVO device and set self.evo flag accordingly
        if 'all' in self.connect_channels or 'text' in self.connect_channels:
            if not self.readonly_user:
                if 'pre_exec_epoch' in kwargs and kwargs['pre_exec_epoch'] is not None:
                    self._device_start_time = float(kwargs['pre_exec_epoch'])
                else:
                    self._get_device_start_time()
            try:
                res = self.cli(command='show version').response()
            except Exception:
                pass

        if self.readonly_user:
            self.log(level="INFO",
                     message="Skipping EVO and VMhost check for Read only users")
        else:
            self.is_evo()
            self.get_vmhost_infra()
    def powercycle(self, timeout=None):
        pattern = self.powercyler_pattern
        if not 'console' in self._kwargs.get('connect_targets', 'management'):
            err = "Powercycle can only be called with console connection"
            raise TobyException(str(err), host_obj=self)
        try:
            cntrl_p = chr(int(16))
            if self.shell(command=cntrl_p, pattern='.*option:.*'):
                time.sleep(1)
                if self.shell(command='5', pattern='.*option:.*'):
                    time.sleep(1) ###this should be varying based on user input
                    if self.shell(command='1', pattern=pattern, timeout=timeout):
                        self.disconnect()
                        self.reconnect(timeout=timeout)
                        self.log(level='info', message='Powercycle is succesfully completed')
                        return True
            self.log(level='ERROR', message='Powercycle failed')
            return False
        except Exception as err:
            raise TobyException(str(err), host_obj=self)

    def is_alive(self):
        if 'text' in self.channels:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socketTimeout = 5
                s.settimeout(socketTimeout)
                s.connect((self.host, self.channels['text'].port))
                s.close()
                self.log(level="INFO", message='Device Port Scan: Port ' + str(self.channels['text'].port) + ' is listening')
                return True
            except socket.error as err:
                self.log(level="INFO", message='Device Port Scan: Port ' + str(self.channels['text'].port) + ' is NOT listening:' + str(err))
            return False

    def create_mode_routes(self, rebuild=None):
        """
        Creates all the different mode routes via yaml
        """

        routes = dict()
        self.modes_yaml = yaml.safe_load(open(os.path.realpath(__file__).replace('junos.py', 'junos_modes.yaml')))

        def create_route(source, mode, path, destination):
            # We want to go through every mode possible to find our destination as long as it is
            # not the mode we came from
            for next_mode in self.modes_yaml[mode]['dest_modes'].keys():
                if next_mode != source:
                    path.append(mode + ':' + next_mode)
                    # If the mode we're currently at is the destination we have reached the end of our
                    # path
                    if next_mode == destination:
                        return path
                    else:
                        # When we have not yet reached our destination but can follow our next mode
                        # we call upon the function again to go one level deeper
                        route = create_route(mode, next_mode, path, destination)
                        # If we get an actual path back then we return that
                        if route is not None:
                            return route
                        # If we do not that means we followed an incorrect path and we need to make
                        # sure to remove that last command from our route
                        else:
                            del path[-1]

        # Goes through each source mode in yaml
        for source in self.modes_yaml:
            # goes through each possible destination
            for destination in self.modes_yaml:
                # only finds path from source > destination if they aren't the same
                if source != destination:
                    key = source + ":" + destination # creates the key to be stores in 'routes'
                    for mode in self.modes_yaml[source]['dest_modes'].keys():
                        # Start the path with the first mode to step to. Here we include the
                        # root mode it is coming from so later we know which instructions to run
                        path = [source + ':' + mode]
                        # Only if we have found the destination do we update the routes with the
                        # proper commands
                        if mode == destination:
                            routes.update({key:path})
                        else:
                            route = create_route(source, mode, path, destination)
                            if route is not None:
                                routes.update({key:route})
            # Also checks to see if path to itself exists for each mode and if so stores that.
            # Path to itself would exist if a mode can be entered with different arguments/options.
            if source in self.modes_yaml[source].keys():
                key = source + ":" + source
                path = [key] # the path is same as the key
                routes.update({key:path})

        # We need to store the routes as well as the modes' attributes
        self.modes['routes'] = routes

    # Setting cli prompt
    def set_prompt_cli(self, prompt):
        """
        Example: device_object.set_prompt_cli(prompt='cli > ')

        Method called by Unix new or user to set device prompt
        :param prompt: prompt to set on the device
        :return: True if set prompt is successful.
                 In all other cases Exception is raised
        """
        self.prompt = [prompt]
        res = self.channels['text'].execute(
            cmd='set cli prompt {0} '.format(prompt),
            pattern=self.prompt,
            device=self
        )
        if res == -1:
            raise TobyException('Error setting Device prompt', host_obj=self)
        self.mode = 'cli'

        res = self.channels['text'].execute(
            cmd='set cli screen-width 0',
            pattern=self.prompt,
            device=self
        )
        if res == -1:
            self.log(level='ERROR', message='Error setting screen-width 0')

        res = self.channels['text'].execute(
            cmd='set cli screen-length 0',
            pattern=self.prompt,
            device=self
        )
        if res == -1:
            self.log(level='ERROR', message='Error setting screen-length 0')

        if str(self._kwargs.get('set_cli_timestamp')) == 'enable':
            res = self.channels['text'].execute(
                cmd='set cli timestamp',
                pattern=self.prompt,
                device=self
            )
        if res == -1:
            self.log(level='ERROR', message='Error setting timestamp')

    # Setting text prompt
    def set_prompt_shell(self, prompt):
        """
        Example: device_object.set_prompt_shell(prompt='shell $ ')

        Method called by Unix new or user to set device prompt
        :param prompt: prompt to set on the device
        :return: True if set prompt is successful.
                 In all other cases Exception is raised
        """
        # puts device back into shell mode after using 'cli'
        # to confirm user is 'super-user'
        res = self.channels['text'].execute(
            cmd='start shell', pattern=[r'\$\s', r'%[\s]?', r'#[\s]?', r'>[\s]?'],
            device=self)
        if res == 3:
            self.log(level='DEBUG', message="Shell access unavailable for user '"+self.user+"'")
            self.readonly_user = True
            return False
        if res == -1:
            raise TobyException("Unable to start shell on device.", host_obj=self)
        res = self.channels['text'].execute(
            cmd='echo "$shell $SHELL"',
            pattern=[r'\$\s$', r'%[\s]?', r'#[\s]?'], device=self)
        if res == -1:
            raise TobyException("Unable to get shell type on device. Device prompt not set", host_obj=self)
        shell = self.response.split()[0]
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
            raise TobyException("Connected device has unknown shell. Device prompt not set", host_obj=self)

        res = self.channels['text'].execute(cmd=cmd, pattern=prompt, device=self)
        if res == -1:
            raise TobyException("Error setting Device prompt", host_obj=self)
        self.prompt = [prompt]
        self.mode = 'shell'
        return True

    # Method to add a new channel to the junos object
    def add_channel(self, channel_type, channel_attributes=None):
        """
        Add new Channel to Junos Object
        :param channel_type:
            *MANDATORY* Type to channel to create ,
            currently supports snmp, grpc only
        :param channel_attributes:
            *OPTIONAL* Arguments required for creating the channel
        :return: Id of the channel created
        """
        supported_channels = ['snmp', 'grpc']
        future_support_channels = ['text', 'pyez']
        if channel_type.lower() not in supported_channels:
            if channel_type.lower() not in future_support_channels:
                self.log(level="DEBUG", message="Invalid channel {0} to add "
                         "in Junos object".format(channel_type))
            else:
                self.log(level="DEBUG", message="Adding channel {0} currently"
                         " not supported".format(channel_type))
            return True

        if channel_type.lower() == 'snmp':
            return_value = self._add_snmp_channel(channel_attributes)
        elif channel_type.lower() == 'grpc':
            return_value = self._add_grpc_channel(channel_attributes)

        return return_value

    # Method for adding snmp channel
    def _add_snmp_channel(self, channel_attributes=None):
        """
        Function to create snmp handle to the router.
        Instance of SNMP Class is created and mapped as
        snmp channel to device object
        :param dev:
            **REQUIRED** Router object
        :param channel_id:
            *OPTIONAL* Channel ID to map the SNMP object.
            Will be auto generated if not provided.
        :param MIBDIRS:
            *OPTIONAL* MIB files location.
            will set to default MIBS Directory if not specified
        :param timeout:
            *OPTIONAL* Time by which output is expected. Default is
            60 seconds
        :return: Channel ID
        """
        from jnpr.toby.hldcl.channels.snmp import Snmp
        if not channel_attributes:
            channel_attributes = dict()
        channel_attributes['host'] = self.host
        channel_attributes['mibs_custom_dir'] = self.mibs_custom_dir
        snmp_instance = Snmp(channel_attributes)
        snmp_id = snmp_instance.get_snmp_id()
        if not hasattr(self, 'default_snmp_channel'):
            self.default_snmp_channel = snmp_id
            self.channels['snmp'] = dict()
        self.channels['snmp'][snmp_id] = snmp_instance
        return snmp_id

    def _grpc_init(self, channel_attributes=None):
        """
        _grpc_init function
        """
        if 'channel_id' not in channel_attributes:
            self.log(level="DEBUG", message='User has not provided any grpc '
                     'channel ID, so system will generate one ...')
        else:
            id_ = channel_attributes['channel_id']
            self.log(level='info',
                     message='User provided grpc channel name is %s ' % id_)

        if 'host' not in channel_attributes:
            grpc_instance = Grpc(rhandle=self, **channel_attributes)
        else:
            grpc_instance = Grpc(**channel_attributes)

        grpc_id = grpc_instance.get_grpc_id()

        if not hasattr(self, 'default_grpc_channel'):
            self.default_grpc_channel = grpc_id
            self.log(level='info', message='Creating a default grpc channel '
                     'with ID = %s ' % grpc_id)
            self.channels['grpc'] = dict()

        self.channels['grpc'][grpc_id] = grpc_instance
        return grpc_id

    def _grpc_connect_to_server(self, channel_attributes=None):

        """
            Function to initiate a grpc connection to the router,
            by invoking the Grpc class method open()

            :param self:
                **REQUIRED** Router-controller object
            :param grpc_id:
                *OPTIONAL* Channel ID to map the GRPC object.
                if not provided, will pick the default channel id,
                saved in grpc_init() function
            :return:
                True, upon successful creation & authentication of channel,
                False, in case of failure

        """
        channel_attributes = channel_attributes or {}
        grpc_id = channel_attributes.get('grpc_id', self.default_grpc_channel)

        g_obj = self.channels['grpc'][grpc_id]

        if not g_obj.open():
            self.log(level='error', message='Issue in channel creation')
            del self.channels['grpc'][grpc_id]
            return False
        else:
            return True

    def _add_grpc_channel(self, channel_attributes=None):
        """
        _add_grpc_channel function
        """
        grpc_id = self._grpc_init(channel_attributes)

        channel_attributes['grpc_id'] = grpc_id
        connect = self._grpc_connect_to_server(channel_attributes)

        if connect:
            return grpc_id
        else:
            return None

    def _get_device_start_time(self):
        """
        Get the device start time
        """
        result = self.shell(command='date \"+%Y%m%d %H:%M:%S\"').response()
        #result = result+'.000'
        epoch = float(time.mktime(time.strptime(result, '%Y%m%d %H:%M:%S')))
        self._device_start_time = epoch

    def _connect_pyez(self):
        """
        _connect_pyez function
        """
        # Port needs to be handled
        kwargs = self._kwargs
        kwargs['connect_mode'] = kwargs.get('connect_mode', 'telnet')

        self.log(level="DEBUG", message="Trying pyez connection to {0} "
                 "using {1}  ...".format(self.host, kwargs['connect_mode']))
        if kwargs.get('channels'):
            self.channels['pyez'] = kwargs['channels']['pyez']
        else:
            connect_mode = kwargs.get('connect_mode', 'telnet').lower()
            pyez_port = kwargs.get('pyez_port', None)
            device_args = {'host': self.host, 'user': self.user,
                           'passwd': self.password, 'gather_facts': True}
            # For ssh set port to 22
            if connect_mode == 'ssh':
                device_args['port'] = 22
            # For telnet or console mode needs to be set to make a
            # pyEZ connection
            elif connect_mode == 'telnet' or connect_mode == 'console':
                device_args['mode'] = connect_mode
            elif not connect_mode == 'netconf':
                self.log(level='ERROR', message='Invalid connect_mode')
            if 'normalize' in kwargs:
                device_args['normalize'] = kwargs['normalize']
            else:
                device_args['normalize'] = True
            if pyez_port is not None:
                device_args['port'] = int(pyez_port)
                self.log(level='info',
                         message="using pyez port: " + str(pyez_port))
            self.channels['pyez'] = Pyez_Device(**device_args)
            if kwargs.get('timeout'):
                self.channels['pyez'].auto_probe = kwargs.get('timeout')
            self.channels['pyez'].open()
            if self.pyez_timeout:
                self.channels['pyez'].__setattr__('timeout', self.pyez_timeout)
            if connect_mode == 'ssh':
                self.channels['pyez']._conn._session.transport.set_keepalive(200)

            try:
                if self.channels['pyez'].facts['version'] is None or self.channels['pyez'].facts['model'] is None:
                    self.log(level='info', message="Facts are None, refreshing the facts")
                    self.channels['pyez'].facts_refresh()
                version = str(self.channels['pyez'].facts['version'])
                model = str(self.channels['pyez'].facts['model'])
                is_master = str(self.channels['pyez'].master)
                self.version = version

                self.log(level='info', message="Device Model= " + model)
                self.log(level='info', message="[" + str(self.re_name) + "] " +
                         "Is Master= " + is_master)
                self.log(level='info', message="[" + str(self.re_name) + "] " +
                         "JUNOS Version= " + version)
            except Exception:
                pass

        self.connected = True
        self.log(level="info", message="'pyez' Connection successful")

    # Create a paramiko/telnetlib connection
    def _get_cli_connect(self):
        self.log(level='DEBUG', message="Inside _get_cli_connect ")
        cli_chan = None
        console = False
        kill_sessions = self._kwargs.get('kill_sessions', 'yes')

        # gather optional user specified TCP port
        port = self._kwargs.get('port', None)
        if port is None:
            match = re.search(r'(\S+)\s+(\d+)', self.host)
            if match:
                self.host = match.group(1)
                port = int(match.group(2))
        text_port = self._kwargs.get('text_port', None)
        if text_port is not None:
            port = int(text_port)
            self.log(level='info',
                     message="using text port: " + str(text_port))

        # gather optional ssh_key_file if supplied
        ssh_key_file = self._kwargs.get('ssh_key_file', None)

        # check if console in connect targets
        if 'console' in self._kwargs.get('connect_targets', 'management'):
            if 'con-ip' in self._kwargs:
                self.host = self._kwargs.get('con-ip')
                match = re.search(r'(\S+)\s+(\d+)', self.host)
                if match:
                    self.host = match.group(1)
                    port = int(match.group(2))
                self.log(level='DEBUG', message='Host set to console ip')
                console = True # this is used by telnetconn
            else:
                self.log(level='ERROR', message='Console ip does not exist')

        # console connection
        if self._kwargs.get('connect_mode', '').lower() == 'console':
            self.log(level="DEBUG",
                     message="Cannot create 'cli_chan' for console mode")
            return None
        # telnet connection
        elif self._kwargs.get('connect_mode', 'telnet').lower() == 'telnet':
            self.log(level="info", message='Telnet connection')
            cli_chan = TelnetConn(host=self.host, user=self.user,
                                  password=self.password, port=port,
                                  console=console, kill_sessions=kill_sessions, connect_timeout=self.connect_timeout)
        # ssh connection
        elif self._kwargs.get('connect_mode').lower() == 'ssh' or \
                self._kwargs.get('connect_mode').lower() == 'netconf':
            if not port:
                port = 22
            if 'proxy_host' in self._kwargs or 'proxy_hosts' in self._kwargs:
                self.proxy = True
                self.log(level="info", message='Proxy connection')
                hosts = self._build_proxy_hosts_stack()
                # build SshConn to proxy instead of final target resource
                cli_chan = SshConn(host=hosts[0]['host'],
                                   user=hosts[0]['user'],
                                   password=hosts[0]['password'],
                                   port=int(hosts[0].get('port', 22)),
                                   ssh_key_file=hosts[0].get('ssh_key_file',
                                                             None))
                # now hop from host to host to get to final target
                for i in range(1, len(hosts)):
                    self.log(level='info', message='Proxy connection - ' +
                             hosts[i]['connect_command'])

                    # ---
                    # Sudhir: 26-Feb-2019 : if user has specified a password as 'None', it indicates a password-less
                    # login to the host. Below condition is executed when password is not None
                    if hosts[i]['password'] and hosts[i]['password'] != "None" and not hosts[i]['ssh_key_file']:
                        res = cli_chan.execute(
                            cmd=hosts[i]['connect_command'],
                            pattern='assword', device=self)
                        res = cli_chan.execute(
                            cmd=hosts[i]['password'],
                            pattern=hosts[i]['expected_prompt_substr'],
                            device=self)
                    else:
                        res = cli_chan.execute(
                            cmd=hosts[i]['connect_command'],
                            pattern=hosts[i]['expected_prompt_substr'],
                            device=self)
                    t.log(level='INFO', message=str(res))
            else:
                cli_chan = SshConn(host=self.host, user=self.user,
                                   password=self.password, port=port,
                                   ssh_key_file=ssh_key_file)
        else:
            self.log(level='error', message='Unknown connection mode '
                     '{0}'.format(self._kwargs['connect_mode']))
            return None

        return cli_chan

    def _build_proxy_hosts_stack(self):
        """
        Used to build a list of hosts to hop to when proxy involved
        """
        if 'proxy_host' in self._kwargs:
            single_proxy = {}
            single_proxy['port'] = int(self._kwargs.get('proxy_port', 22))
            single_proxy['host'] = self._kwargs.get('proxy_host')
            single_proxy['user'] = self._kwargs.get('proxy_user', self.user)
            single_proxy['password'] = self._kwargs.get('proxy_password', self.password)
            single_proxy['ssh_key_file'] = self._kwargs.get('proxy_ssh_key_file', None)
            hosts = []
            hosts.append(single_proxy)
        else:
            hosts = self._kwargs['proxy_hosts']

        # Indicates still need to add new element to list
        # for final target device
        if 'host' in hosts[-1] and hosts[-1]['host'] != self.host:
            final_target = {}
            final_target['port'] = int(self._kwargs.get('port', 22))
            final_target['host'] = self.host
            final_target['user'] = self.user
            final_target['password'] = self.password
            final_target['ssh_key_file'] = self._kwargs.get(
                'ssh_key_file', None)
            hosts.append(final_target)
        else:
            # merge in data with users connect_command
            hosts[-1]['host'] = self.host
            hosts[-1]['port'] = int(self._kwargs.get('port', 22))
            hosts[-1]['ssh_key_file'] = self._kwargs.get('ssh_key_file', None)
            if 'user' not in hosts[-1]:
                hosts[-1]['user'] = self.user
            if 'password' not in hosts[-1]:
                hosts[-1]['password'] = self.password

        for i in range(1, len(hosts)):
            if 'port' not in hosts[i]:
                hosts[i]['port'] = 22
            if 'expected_prompt_substr' not in hosts[i]:
                hosts[i]['expected_prompt_substr'] = ['$', '>', '#', '%']
            if 'connect_command' in hosts[i]:
                p_tmp = re.compile(r'\$host')
                hosts[i]['connect_command'] = p_tmp.sub(
                    hosts[i]['host'], hosts[i]['connect_command'])
                if hosts[i]['user']:
                    p_tmp = re.compile(r'\$user')
                    hosts[i]['connect_command'] = p_tmp.sub(
                        hosts[i]['user'], hosts[i]['connect_command'])
                if hosts[i]['password']:
                    p_tmp = re.compile(r'\$password')
                    hosts[i]['connect_command'] = p_tmp.sub(
                        hosts[i]['password'], hosts[i]['connect_command'])
                if 'ssh_key_file' in hosts[i] and hosts[i]['ssh_key_file']:
                    p_tmp = re.compile(r'\$ssh_key_file')
                    hosts[i]['connect_command'] = p_tmp.sub(
                        hosts[i]['ssh_key_file'], hosts[i]['connect_command'])
            else:
                ssh_cmd = 'ssh -o StrictHostKeyChecking=no'
                if hosts[i]['user']:
                    ssh_cmd += ' -l ' + hosts[i]['user']
                if 'ssh_key_file' in hosts[i] and hosts[i]['ssh_key_file']:
                    ssh_cmd += ' -i ' + hosts[i]['ssh_key_file']
                ssh_cmd += ' ' + hosts[i]['host']
                hosts[i]['connect_command'] = ssh_cmd
        return hosts

    def _connect_text(self):
        """
        _connect_text function
        """
        self.log(level='DEBUG', message="Inside _connect_text")
        self.channels['text'] = self._get_cli_connect()
        # Set prompt
        prompt = 'Toby-%s-%s' % (os.getpid(), self.host)
        prompt += '%'
        self.channels['text'].shell_prompt = prompt
        if self.is_readonly_user():
            self.log(level="DEBUG", message="Read only users")
        else:
            self.set_prompt_shell(prompt=prompt)
        prompt = 'Toby-%s-%s' % (os.getpid(), self.host)
        prompt += '>'
        try:
            res = self.channels['text'].execute(
                cmd='cli', pattern=r'>[\s]?', device=self)
        except Exception as err:
            res = -1
        if res == -1:
            raise TobyException('Error while switching to cli mode on the device', host_obj=self)
        self.channels['text'].cli_prompt = prompt
        self.set_prompt_cli(prompt=prompt)
        self.connected = True
        self.log(level='info', message='Text connection successful')


    # Mode Shift
    def _switch_mode(self, mode='CLI', vty_cmd=None, cty_cmd=None, config_mode=''):

        if 'text' not in self.channels.keys():
            raise TobyException("'text' channel does not exist", host_obj=self)

        # If previous command was in a custom mode make sure to exit out of it
        if self.custom_mode != None:
            # Exit out of custom mode
            for i, target in reversed(list(enumerate(self.custom_modes[self.custom_mode]['targets']))):
                try:
                    # if last exit command use device's original prompt, otherwise use
                    # previous target's pattern
                    if i == 0:
                        self.execute(command=target['exit_command'], pattern=self.prompt)
                    else:
                        self.execute(command=target['exit_command'],
                                     pattern=self.custom_modes[self.custom_mode]['targets'][i-1]['pattern'])
                except Exception as err:
                    raise TobyException("Unable to exit custom mode successfully." + str(err), host_obj=self)
            # Set this to None, this will be set again when entering a new custom mode
            self.custom_mode = None

        curr_mode = self.mode.upper()
        mode = mode.upper()
        if mode == 'CONFIG':
            curr_config_mode = self.config_mode.upper()
        else:
            curr_config_mode = ''

        self.log(level='DEBUG', message='curr config mode = %s, mode = %s, '
                 'curr_mode = %s, config_mode = %s'
                 % (curr_config_mode, mode, curr_mode, config_mode.upper()))
        self.log(level='DEBUG', message='Required Prompt : %s, Device Prompt in : %s '%(mode, curr_mode))
        if mode == curr_mode and config_mode.upper() == curr_config_mode:
            self.log(level='DEBUG', message='Hence skipping mode switch')
            return True

        # A function to parse out any variables a command have, such as
        # a vty destination
        def parse_command(instruction, vty_cmd, cty_cmd, config_mode):
            # Need to first separate type of instruction from command
            instruction_type, command = instruction.split('(', maxsplit=1)
            command = command[:-1]

            if command == '\\x03':
                command = '\x03'

            # Matches against ${task} so that it can do the necessary
            # calculation/task
            tasks = re.findall(r"\$\{(\S*)\}", command)
            for task in tasks:
                if task == 'pid':
                    pid = str(os.getpid())
                    command = re.sub(r"\$\{\S*\}", pid, command, 1)

            # Matches against var[var_name] so that can replace with the
            # actual variable's values
            variables = re.findall(r"var\[(\S*)\]", command)
            for variable in variables:
                # Tries to first see if variable exists as Junos attribute, if not
                # grabs local variable
                try:
                    variable_value = getattr(self, variable)
                    if(variable == 'config_mode' and config_mode != '' and getattr(self, variable) != config_mode):
                        variable_value = eval(variable)
                except:
                    variable_value = eval(variable)
                command = re.sub(r"var\[(\S*)\]", variable_value, command, 1)

            return instruction_type, command

        self.log(level='INFO', message='Mode switch required')

        try:
            mode_lower = mode.lower()
            curr_mode_lower = curr_mode.lower()
            wanted_route = curr_mode_lower + ':' + mode_lower
            switch_mode_route = self.modes['routes'][wanted_route]
            # Goes through all the different modes it steps into and executes the
            # appropriate instructions/commands
            for steps in switch_mode_route:
                # splits the mode it is coming from to the next mode so issues
                # right instructions/commands
                prev_mode, next_mode = steps.split(':', maxsplit=1)
                # If switching to the same mode with different arguments provide the proper
                # set of instructions
                if next_mode == prev_mode:
                    instructions = self.modes_yaml[prev_mode][next_mode]
                else:
                    instructions = self.modes_yaml[prev_mode]['dest_modes'][next_mode]
                for instruction in instructions:
                    instruction_type, command = parse_command(instruction, vty_cmd, cty_cmd, config_mode)
                    # If a prompt needs to be changed do that before issuing next command
                    if instruction_type == 'prompt':
                        command = command.split('|')
                        setattr(self, 'prompt', command)
                    elif instruction_type == 'vty':
                        # Exepcts vty prompts as well, because otherwise will raise exception as 'exit' does not work
                        expected_pattern = [r"vty\)#\s", r"vty.[a-zA-Z0-9]*# ", r"fpc[a-zA-Z0-9:]*> ", r":pfe> "]
                        result = self.execute(command=command, pattern=self.prompt+expected_pattern)
                        # If syntax error is found then execute 'quit' command instead and switch the instruction
                        # to use 'quit' instead and not enter this if condition by prepending 'vty_set'
                        if 'Syntax error' in result:
                            self.execute(command="quit")
                            instructions[instructions.index(instruction)] = "vty_set(quit)"
                            setattr(self, 'prompt', self.prompt)
                    else:
                        self.execute(command=command)

            # Now that we are in the mode we set the current mode accordingly
            setattr(self, 'mode', mode)
            if mode == 'CONFIG':
                setattr(self, 'config_mode', config_mode)

        except:
            raise DeviceModeSwitchException('Cannot switch to ' + mode + ' mode.', host_obj=self)

        return True

    def is_readonly_user(self):
        """
        is_readonly_user function
        """
        if self.readonly_user is None:
            res = self.cli(command='show cli authorization | match user:', pattern=[r'>[\s]?']).response()
            if re.search('\'read-only\'', res) or re.search('\'host-admin\'', res, re.I):
                self.readonly_user = True
                return True
            self.readonly_user = False
            return False
        else:
            return self.readonly_user

    def is_master(self):
        """
        is_master function
        """
        if self.evo:
            res = self.shell(command='jwhoami | grep mastership').response()
            if re.search('Master', res):
                return True
            return False
        else:
            res = self.shell(
                command='sysctl hw.re.mastership').response()
            if re.search('hw.re.mastership: 1', res):
                return True
            return False

    def is_evo(self):
        """
        is_evo function
        """
        if hasattr(self, 'evo') and self.evo:
            return self.evo
        res = self.shell(command='ls /usr/share/cevo/').response()
        if re.search('cevo_version', res):
            self.evo = True
            return True
        return False

    def mode_shift(self, mode):
        """
        mode_shift function
        """

        #to-do why does this return True no matter what?
        if mode == self.mode:
            return True
        return True

    def add_mode(self, mode=None, origin='shell', command=None, pattern=None, exit_command=None, targets=None):
        """
        Adds custom mode to device

        device_object.add_mode(mode=custom1, command=cli,
                               pattern=>, exit_command=exit)

        OR

        device_object.add_mode(mode=custom1, targets=list_of_targets)

        :param device:
            *MANDATORY* Device handle on which custom mode is to
            be added.
        :param mode:
            *MANDATORY* Name of the custom mode.
        :param origin:
            *OPTIONAL* The starting point from which the custom mode is entered.
            By default this is 'shell' but 'cli' is the other option.
        :param command:
            *MANDATORY* Command by which to enter custom mode.
        :param pattern:
            *MANDATORY* Pattern to be expected after giving
            command.
        :param exit_command:
            *MANDATORY* Command to exit out of the mode.
        :param targets:
            *OPTIONAL* Used to pass more than one target.
            Only required if more than one target is used.
            If used, then the previous arguments are not
            required except for device and mode.
        Returns: True if succesfully adds more, otherwise
        raises an Exception.
        """
        if mode in self.custom_modes:
            raise TobyException("The mode you are trying to add already exists, please choose another.", host_obj=self)
        self.custom_modes[mode] = dict()
        self.custom_modes[mode]['targets'] = [] # makes new mode a list for targets
        self.custom_modes[mode]['origin'] = origin
        # We are only getting one target
        if targets is None:
            target = dict()
            self.custom_modes[mode]['targets'].append(target)
            self.custom_modes[mode]['targets'][0]['command'] = command
            self.custom_modes[mode]['targets'][0]['pattern'] = pattern
            self.custom_modes[mode]['targets'][0]['exit_command'] = exit_command
        else:
            self.custom_modes[mode]['targets'] = targets

        # Switch to starting point mode
        if origin == 'shell':
            self._switch_mode(mode='shell')
        elif origin == 'cli':
            self._switch_mode(mode='cli')
        else:
            raise TobyException("The origin mode " + str(origin) + " is not supported.", host_obj=self)

        # Check if able to go into custom mode
        for target in self.custom_modes[mode]['targets']:
            try:
                self.execute(command=target['command'],
                             pattern=target['pattern'])
            except Exception as err:
                raise TobyException("Unable to go to custom mode successfully." + str(err), host_obj=self)

        # Check if you are able to exit out
        for i, target in reversed(list(enumerate(self.custom_modes[mode]['targets']))):
            try:
                # if last exit command use device's original prompt, otherwise use
                # previous target's pattern
                if i == 0:
                    self.execute(command=target['exit_command'],
                                 pattern=self.prompt)
                else:
                    self.execute(command=target['exit_command'],
                                 pattern=self.custom_modes[mode]['targets'][i-1]['pattern'])
            except Exception as err:
                raise TobyException("Unable to exit custom mode successfully." + str(err), host_obj=self)

        return True

    def execute_command(self, mode=None, command=None, timeout=60, pattern=None):
        """
        Executes commands on specific mode

        device_object.execute_command(mode=custom1, command=ls)

        :param mode:
            **REQUIRED** mode in which the command should be executed
        :param command:
            **REQUIRED** command to execute
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :param pattern:
            *OPTIONAL* Pattern to match.
        :return: Object with the following methods
            'response()': Response from the command
        """

        # This gives priority to custom modes
        if mode in self.custom_modes:
            # gets the pattern of the last target in the custom mode
            if pattern is None:
                last_target_pattern = len(self.custom_modes[mode]['targets'])-1
                pattern = self.custom_modes[mode]['targets'][last_target_pattern]['pattern']

            # Don't try to re-enter mode if last executed command was the same custom mode
            prev_custom_mode = self.custom_mode
            if mode != prev_custom_mode:
                # Switch to starting point mode
                origin = self.custom_modes[mode]['origin']
                if origin == 'shell':
                    self._switch_mode(mode='shell')
                elif origin == 'cli':
                    self._switch_mode(mode='cli')
                else:
                    raise TobyException("The origin mode " + str(origin) + " is not supported.", host_obj=self)
                # Enter into custom mode
                for target in self.custom_modes[mode]['targets']:
                    try:
                        self.execute(command=target['command'], pattern=target['pattern'])
                    except Exception as err:
                        raise TobyException("Unable to go into custom mode successfully." + str(err), host_obj=self)
            # Once you enter custom mode, set the current custom mode
            self.custom_mode = mode
        # If no custom mode is found we look at the native modes
        elif mode in self.modes_yaml:
            self._switch_mode(mode=mode)
        else:
            raise TobyException("The mode you are trying to execute a command on doesn't exist, "
                                "please choose another.", host_obj=self)

        if isinstance(command, str):
            command_list = [command, ]
        elif isinstance(command, (list, tuple)):
            # deepcopy to avoid change user command
            command_list = list(copy.deepcopy(command))
        for cmd in command_list:
            # execute command
            response = self.execute(command=cmd, timeout=timeout, pattern=pattern)

        return_value = Response(response=response.rstrip(), status=True)
        return return_value

    def execute(self, **kwargs):
        """
        Executes commands on text channel

        device_object.execute(command = 'show version detail | no-more')

        :param command:
            **REQUIRED** CLI command to execute
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :param pattern: Pattern to match.
        :return: Dictionary with the following keys
            'response': Response from the CLI command(text/xml)
        """
        command = ''
        response = None
        if 'command' in kwargs and kwargs['command'] is not None:
            command = kwargs['command']
        else:
            self.log(level="ERROR", message="Mandatory argument 'command' is missing!")

        timeout = kwargs.get('timeout', 60)
        pattern = kwargs.get('pattern')
        no_response = kwargs.get('no_response', False)
        raw_output = kwargs.get('raw_output', False)
        carriage_return = kwargs.get('carriage_return', True)
        user_pattern = kwargs.get('user_pattern', False)
        show_error = kwargs.get('show_error', False)

        if pattern is None:
            pattern = self.prompt

        if 'text' not in self.channels.keys():
            raise TobyException("'text' channel does not exist", host_obj=self)

        response = self.channels['text'].execute(
            cmd=command, pattern=pattern, device=self, no_response=no_response,
            timeout=timeout, raw_output=raw_output, carriage_return=carriage_return, \
            user_pattern=user_pattern, show_error=show_error)
        if response == -1:
            self.log(level="ERROR", message='Timeout seen while retrieving output')
        else:
            return self.response

    def cli(self, **kwargs):
        """
        Executes operational commands on JunOS device.

        device_object.cli(
            command = 'show version detail | no-more', channel = 'text')

        :param command:
            **REQUIRED** CLI command to execute
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            set based on os/platform/model of the box.
        :param format:
            *OPTIONAL* The output format. Default is xml. Supported values are
            xml/text
        :param raw_output:
            *OPTIONAL* Returns raw output of the command. Default is False
        :param pattern: This is not required in pyEZ context. Will be removed.
        :param channel: Channel to use
        :return: Object with the following methods
            'response()': Response from the CLI command(text/xml)
        """
        channel = kwargs.get('channel', 'text')

        command = ''
        if 'command' in kwargs and kwargs['command'] is not None:
            command = kwargs['command']
        else:
            raise TobyException("Mandatory argument 'command' is missing!", host_obj=self)

        # Sarath Check a way to see if text handle is active ######

        # If timeout not provided, get it from ENV or framework defaults
        format_ = kwargs.get('format', 'text')
        kwargs['raw_output'] = kwargs.get('raw_output', False)
        kw_call = kwargs.get('kw_call', False)

        # Shift mode to cli
        self._switch_mode()

        #if fv-cli-timestamp is enabled
        if str(self._kwargs.get('set_cli_timestamp')) == 'enable':
            res = self.execute(command='set cli timestamp')

        # Only one command can be executed
        if not isinstance(command, str):
            raise TobyException("'command' should be a string", host_obj=self)

        if channel.lower() == 'text':
            if format_.lower() == 'xml' and not re.search(r'\|display\s*xml', command, re.I):
                command += ' |display xml'

            kwargs['command'] = command
            kwargs['user_pattern'] = False
            if 'pattern' in kwargs and kwargs['pattern'] is not None:
                if kw_call:
                    kwargs['user_pattern'] = True
                kwargs['pattern'] = kwargs.get('pattern')
            else:
                kwargs['pattern'] = kwargs.get('pattern', r'(\{.*\}\r\n)?' + self.prompt[0])
            kwargs['timeout'] = kwargs.get('timeout', self.cli_timeout)
            response = self.execute(**kwargs)
            command_status = response_check(self, response, 'cli')
            return_value = Response(response=response, status=command_status)
            return return_value
        else:
            if 'pyez' not in self.channels:
                self.log(level="DEBUG", message="pyez channel does not exist")
            # Set timeout
            self.channels['pyez'].timeout = kwargs.get('timeout', self.pyez_timeout)
            response = self.channels['pyez'].cli(command, format=format_,
                                                 warning=False)
            # Reset timeout to default
            self.channels['pyez'].timeout = self.pyez_timeout
            if isinstance(response, str):
                self.log(level='info', message='response: ' + response)
            else:
                self.log(level='info', message='response: ' + etree.tounicode(response, pretty_print=True))
            return_value = Response(response=response, status=True)
            return return_value

    def shell(self, **kwargs):
        """
        Executes shell commands on JunOS device.

         device_object.shell(command = 'ls -l')

        :param command:
            **REQUIRED** Shell command to execute
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            set based on os/platform/model of the box.
        :param pattern:
            *OPTIONAL: Pattern expected back from device after
            executing shell command
        :param raw_output:
            *OPTIONAL* Returns raw output of the command. Default is False
        :return: Object with the following methods
            'response()': Response from the shell command
        """
        command = ''
        if 'command' in kwargs and kwargs['command'] is not None:
            command = kwargs['command']
        else:
            raise TobyException("Mandatory argument 'command' is missing!", host_obj=self)

        # Sarath Check a way to see if text handle is active ######

        # mode shift
        # old_mode = self.mode
        self._switch_mode(mode='shell')

        # Only one command can be executed
        if not isinstance(command, str):
            self.log(level='error', message="'command' should be a string")
            raise TobyException("'command' should be a string", host_obj=self)

        kwargs['command'] = command
        kwargs['raw_output'] = kwargs.get('raw_output', False)
        kwargs['timeout'] = kwargs.get('timeout', self.shell_timeout)
        kwargs['user_pattern'] = False
        kw_call = kwargs.get('kw_call', False)
        if 'pattern' in kwargs:
            if kw_call:
                kwargs['user_pattern'] = True
        response = self.execute(**kwargs)
        return_value = Response(response=response.rstrip(), status=True)
        return return_value

    def config(self, **kwargs):
        """
        Loads configurations or configures JunOS device.

        device_object.config(command_list = ['set services telnet',
        'delete services web-management', 'show | compare'])

        :param command_list:
            **REQUIRED** List of string(s) of configuration commands to execute
        :param mode:
            *OPTIONAL* Mode of configuration. Default is None which means
            configure mode. Supported values are exclusive and private
        :param pattern:
            *OPTIONAL: Pattern expected back from device
            after executing config command
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            set based on os/platform/model of the box.
        :param raw_output:
            *OPTIONAL* Returns raw output of the command. Default is False
        :return: Object with the following methods
            'response()': Response from the config command
        """
        command_list = ''
        if 'command_list' in kwargs and kwargs['command_list'] is not None:
            command_list = kwargs['command_list']
        else:
            raise TobyException("Mandatory argument 'command_list' is missing!", host_obj=self)

        if not isinstance(command_list, list):
            raise TobyException("Argument 'command_list' must be a list!", host_obj=self)
        self._switch_mode(config_mode=kwargs.get('mode', ''), mode='config')
        response = ''
        kwargs['raw_output'] = kwargs.get('raw_output', False)
        kwargs['timeout'] = kwargs.get('timeout', self.config_timeout)
        pattern = kwargs.get('pattern')
        kw_call = kwargs.get('kw_call', False)
        kwargs['user_pattern'] = False
        if pattern is not None:
            if kw_call:
                kwargs['user_pattern'] = True
            if isinstance(pattern, str):
                kwargs['pattern'] = [kwargs['pattern']]
                kwargs['pattern'] = kwargs['pattern'] + self.prompt
            elif isinstance(pattern, list):
                kwargs['pattern'] = kwargs['pattern'] + self.prompt
        command_status = True
        for command in command_list:
            if not isinstance(command, str):
                raise TobyException("Argument 'command_list' must be a list of strings!", host_obj=self)
            kwargs['command'] = command
            response = response + str(
                self.execute(**kwargs).replace("[edit]", "").strip())
            command_status = response_check(self, response, 'config')
            self.command_status = command_status
        return_value = Response(response=response, status=command_status)
        return return_value

    def vty(self, command, destination, timeout=None, pattern=None,
            raw_output=False, **kwargs):
        """
        Executes vty commands on the specified destination.

        device_object.vty(command = 'show memory', destination = 'fpc1')

        :param command:
            **REQUIRED**  vty command to be executed
        :param destination:
            **REQUIRED**  destination to vty into.  example: fpc0
        :param timeout:
            **OPTIONAL**  max time to wait for response. Default is
            set based on os/platform/model of the box
        :param pattern:
            **OPTIONAL**  Pattern expected back from device
            after executing vty command
        :param raw_output:
            *OPTIONAL* Returns raw output of the command. Default is False
        :return: Exception if vty fails, else vty command response
        """
        if command is None:
            raise TobyException("None value is not allowed as 'command'", host_obj=self)
        if destination is None:
            raise TobyException("None value can not be passed as  'destination'", host_obj=self)
        if timeout is not None:
            timeout = timeout
        else:
            timeout = self.vty_timeout

        show_error = kwargs.get('show_error', False)

        if destination != self.destination:
            self._switch_mode(mode='shell')
        self._switch_mode(mode='vty', vty_cmd='vty ' + destination)

        setattr(self, 'destination', destination)

        user_pattern = False
        if pattern is not None:
            user_pattern = True
        else:
            if command.startswith('clear syslog messages'):
                pattern = ['\n']

        response = self.execute(command=command, pattern=pattern, timeout=timeout,
                                raw_output=raw_output, user_pattern=user_pattern, show_error=show_error)

        # The vty command has a syntax error
        if 'Syntax error' in response:
            self.log(level='ERROR', message='Syntax Error when executing vty command on %s' % destination)
            return_value = Response(response='Syntax Error', status=False)
            return return_value
        else:
            return_value = Response(response=response.rstrip(), status=True)
            return return_value

    def cty(self, command, destination, timeout=None, pattern=None,
            raw_output=False, **kwargs):
        """
        Executes cty commands on the specified destination.

            device_object.cty(command = 'show msp service-sets',
            destination = 'fpc1')

        :param command:
            **REQUIRED**  cty command to be executed
        :param destination:
            **REQUIRED**  destination to cty into.  example: fpc0
        :param timeout:
            **OPTIONAL**  max time to wait for response. Default is
            set based on os/platform/model of the box
        :param pattern:
            **OPTIONAL**  Pattern expected back from device
            after executing cty command
        :param raw_output:
            *OPTIONAL* Returns raw output of the command. Default is False
        :return: False if cty fails, else cty command response
        """
        if command is None:
            raise TobyException("None value is not allowed as 'command'", host_obj=self)
        if destination is None:
            raise TobyException("None value can not be passed as  'destination'", host_obj=self)
        if timeout is not None:
            timeout = timeout
        else:
            timeout = self.cty_timeout

        show_error = kwargs.get('show_error', False)

        # Only root can execute a cty command.
        if self.mode.upper() != 'CTY':
            self.su()

        if destination != self.destination:
            self._switch_mode(mode='shell')

        self._switch_mode(mode='cty', cty_cmd='cty -f ' + destination + '\n')

        setattr(self, 'destination', destination)

        user_pattern = False
        if pattern is not None:
            user_pattern = True

        response = self.execute(command=command, pattern=pattern, timeout=timeout,
                                raw_output=raw_output, user_pattern=user_pattern,show_error=show_error)
        while True:
            # If the output is paged.
            if '--(more)--' in response:
                response = re.sub(r'-*\(more\)-*', '', response)
                self.log(level='WARN',  \
                      message='Output paged .. sending a carriage return to obtain more output')
                response += self.execute(command='\r\n', pattern=pattern, timeout=timeout, user_pattern=user_pattern)
                continue
            else:
                break

        # The cty command has a syntax error
        if 'Syntax error' in response:
            self.log(level='ERROR', message='Syntax Error when executing vty command on %s' % destination)
            return_value = Response(response='Syntax Error', status=False)
            return return_value
        else:
            return_value = Response(response=response.rstrip(), status=True)
            return return_value

    def get_rpc_equivalent(self, command=None):
        """
        get_rpc_equivalent function
        """

        cmd = self.channels['pyez'].display_xml_rpc(command)
        if isinstance(cmd, str):
            try:
                ET.fromstring(cmd)
            except:
                raise TobyException('Error in get_rpc_equivalent: ' + cmd, host_obj=self)
        cmd_str = etree.tostring(cmd)
        return str(cmd_str, 'utf-8')

    def execute_rpc(self, dummy=None, command=None, **kvargs):
        """
        Executes an XML RPC and returns results as either XML or native python

            device_object.execute_rpc(command = '<get-software-information/>')

        :param command:
          can either be an XML Element or xml-as-string.  In either case
          the command starts with the specific command element, i.e., not the
          <rpc> element itself

        :param func to_py':
          Is a caller provided function that takes the response and
          will convert the results to native python types.  all kvargs
          will be passed to this function as well in the form::

            to_py( self, rpc_rsp, **kvargs )

        :raises ValueError:
            When the **command** is of unknown origin

        :raises PermissionError:
            When the requested RPC command is not allowed due to
            user-auth class privilege controls on Junos

        :raises RpcError:
            When an ``rpc-error`` element is contained in the RPC-reply

        :return: Object with the following methods
          'response()': Response from the rpc command
            RPC-reply as XML object.  If **to_py** is provided, then
            that function is called, and return of that function is
            provided back to the caller; presumably to convert the XML to
            native python data-types (e.g. ``dict``).
        """
        if command is None:
            raise TobyException("Mandatory argument 'command' is missing!", host_obj=self)

        self.log(level='INFO', message='Executing rpc :')
        rpc_cmd_log = command
        try:
            rpc_cmd_log = etree.tostring(command)
            t.log(level='INFO', message=str(rpc_cmd_log))
        except Exception:
            pass

        prev_timeout = self.channels['pyez'].timeout
        if 'timeout' in kvargs:
            timeout = kvargs.pop('timeout')
            self.channels['pyez'].timeout = timeout

        if 'ignore_rpc_error' in kvargs and kvargs['ignore_rpc_error']:
            try:
                result = self.channels['pyez'].execute(command, **kvargs)
            except RpcError as ex:
                #result = ex.xml
                error_format = kvargs.get('error_format', '')
                if error_format == 'list':
                    result = ex.errs
                else:
                    result = ex.rsp
        else:
            result = self.channels['pyez'].execute(command, **kvargs)

        if 'timeout' in kvargs:
            self.channels['pyez'].timeout = prev_timeout

        self.log(level='INFO', message='rpc reply is :')
        if isinstance(result, etree._Element):
            xml = xml_dom.parseString(etree.tostring(result))
            pretty_xml = xml.toprettyxml()
            self.log(level='INFO', message=pretty_xml)
        else:
            self.log(level='INFO', message=result)
        return_value = Response(response=result, status=True)
        return return_value

    def pyez(self, command, timeout=None, **kwargs):
        """
        Executes a pyez api call and returns results as lxml/etree

            device_object.execute_pyez(command = 'get-software-information')

        :param command:
          pyez Device object method name

        :raises ValueError:
            When the **command** is of unknown origin

        :return: Response object
        """
        if command is None:
            raise TobyException("Mandatory argument 'command' is missing!", host_obj=self)

        self.log(level="DEBUG", message="Invoking pyez method " + command + " with parameters " + str(kwargs))
        prev_timeout = self.channels['pyez'].timeout
        t.log(level='INFO', message=str(prev_timeout))
        if timeout:
            self.channels['pyez'].timeout = timeout

        try:
            pyez_method = getattr(self.channels['pyez'].rpc, command)
        except AttributeError:
            raise TobyException("PyEZ Device has no command '" + command + "'", host_obj=self)

        result = pyez_method(**kwargs)

        self.log(level='INFO', message='pyez response is :')
        if isinstance(result, etree._Element):
            xml = xml_dom.parseString(etree.tostring(result))
            pretty_xml_as_string = xml.toprettyxml()
            self.log(level='INFO', message=pretty_xml_as_string)
        else:
            self.log(level='INFO', message=result)
        return_value = Response(response=result, status=True)
        return return_value

    def reboot(self, wait=0, mode='shell', timeout=None, interval=20, device_type=None, command_args=None, ping=True, command=None):
        """
        Reboot Junos device
            device_object.reboot()

        :param wait:
            *OPTIONAL* Time to sleep before reconnecting, Default value is 0

        :param mode:
            *OPTIONAL* Mode in which reboot needs to be executed. Default is
            'shell'. Also supports 'cli'.
            mode=cli is valid only for Junos devices.

        :param timeout:
            *OPTIONAL* Time to reboot and connect to device.
            Default is set based on os/platform/model of the box.

        :param interval:
            *OPTIONAL* Interval at which reconnect need to be attempted
            after reboot is performed. Default is 20 seconds

        :param device_type:
            *OPTIONAL* This option works only with 'text' channel.
            Value should be set to 'vmhost' to reboot the vmhost

        :Returns:
            True if device is rebooted and reconnection is successful,
            else an Exception is raised
        """
        timestamp = time.time()
        if timeout is not None:
            timeout = timeout
        else:
            timeout = self.reboot_timeout

        reboot_cmd = None
        if self.evo or (device_type and re.match(r'evo', device_type, re.I)):
            cmd =  command
        elif self.get_vmhost_infra():
            cmd = 'request vmhost reboot'
            if device_type and not re.match(r'vmhost', device_type, re.I):
                cmd = 'request system reboot'
        else:
            cmd = 'request system reboot'

        patterns = [r'[Rr]eboot the vmhost \? \[yes,no\] \(no\)[\s]?',
                    r'[Rr]eboot the system \? \[yes,',
                    r'System going down|Shutdown NOW',
                    r'(?is)connection (to \S+ )?closed.*',
                    r'System reboot operation started',
                    r'.*System shutdown message from.*']

        self.log(level='INFO', message="reboot command_args %s " %command_args)
        if command_args:
            if len(command_args) > 1:
                cmd = cmd + " " + " ".join(command_args)
            else:
                cmd = cmd + " " + command_args[0]

        self.log(level='INFO', message="Reboot command to be sent  %s " % cmd)

        try:
            try:
                if mode.upper() == 'CLI':
                    self.cli(command=cmd, pattern=[r'yes.no.*'])
                    self.log(level='info', message='command: yes')
                    # Console connection does not have PyEZ channel
                    # so must send commands manually
                    if 'console' in self._kwargs.get('connect_targets', 'management'):
                        self.channels['text'].write(b'yes\r\n')
                    else:
                        self.execute(command='yes', pattern=patterns)
                elif mode.upper() == 'SHELL':
                    if not self.su():
                        self.log(level='ERROR',
                                 message='Error preventing rebooting')
                        return False
                    if 'console' in self._kwargs.get('connect_targets',
                                                     'management'):
                        self.channels['text'].write(b'reboot\r\n')
                        self.log(level='info', message='command: reboot')
                    else:
                        self.shell(command='reboot', pattern='reboot\r')
            except Exception as exp:
                self.log(level='ERROR', message=exp)

            # If console connection, wait for device to come up and wait
            # for login prompt
            # No need to reconnect as console connection is not lost on reboot
            if 'console' in self._kwargs.get('connect_targets', 'management'):
                self.log(level='INFO', message='Rebooting console connection')
                host = self.host
                user = self.user + '\r\n'
                user = user.encode(encoding='ascii')
                password = self.password + '\r\n'
                password = password.encode(encoding='ascii')
                login = self.channels['text'].expect([br'[Ll]ogin:[\s]?'], timeout=timeout)
                self.log(level='DEBUG', message=login[2].decode('ascii'))
                if login[0] == -1:
                    self.log(level="ERROR", message="Expected 'login' from %s, but instead got: %s'"
                             % (host, login[2].decode('ascii')))
                self.channels['text'].write(user)
                login = self.channels['text'].expect([br'[Pp]assword:[\s]?'], timeout=timeout)
                if login[0] == -1:
                    raise TobyException("Sent '%s' to %s, expected 'Password: '"
                                        ", but got:'%s'"
                                        % (user, host, login[2].decode('ascii')), host_obj=self)
                self.channels['text'].write(password)
                # Once you enter device, make sure that it is in shell mode
                login = self.channels['text'].expect([br'\$\s$', br'\%[\s]?$', br'\#[\s]?$', br'\>[\s]?$'],
                                                     timeout=timeout)
                if login[0] == -1:
                    raise TobyException("Sent '%s' to %s, expected 'shell/cli prompt', but got:\n'%s'"
                                        % (password, host, login[2].decode('ascii')), host_obj=self)
                if login[0] == 3:
                    self.channels['text'].write(b'start shell\n')
                    login = self.channels['text'].expect(
                        [br'\$\s$', br'\%[\s]?$', br'\#[\s]?$'],
                        timeout=timeout)
                # Making sure in shell mode and then setting column width
                if login[0] == 0 or login[0] == 1 or login[0] == 2:
                    self.channels['text'].write(b'stty cols 160\n')
                    login = self.channels['text'].expect(
                        [br'\$\s$', br'\%[\s]?$', br'\#[\s]?$'],
                        timeout=timeout)
                    if login[0] == -1:
                        self.log(level='ERROR', message="Not able to set column width to 160")
                response = True
            # Check if the device is down
            else:
                try:
                    if ping:
                        timeout = timeout - time.time() + timestamp
                        timestamp = time.time()
                        while timeout > 0:
                            self.log(level='DEBUG', message='Probing if the router has rebooted')
                            from jnpr.toby.utils.iputils import ping
                            ping_resp = ping(host=self.host, count=10, timeout=timeout, fail_ok='info', negative=True)
                            if ping_resp:
                                self.log(level='INFO', message="%s: Reboot is in progress" % self.host)
                                break
                            self.log(level='INFO', message='Router is not down yet..')
                            time.sleep(5)
                            timeout = timeout - time.time() + timestamp
                            timestamp = time.time()
                    self.log(level='INFO', message='Router is rebooting')
                except Exception as exp:
                    self.log(level='ERROR', message='Error while rebooting:'+str(exp))
                    return False

                self.log(level='INFO', message='Sleeping for {0} secs before '
                         'reconnecting'.format(wait))
                time.sleep(wait)
                self.rebooted = True
                response = self.reconnect(timeout=timeout, interval=interval)
            if response:
                self.log(level='INFO', message='Reboot successful')
            else:
                self.log(level='ERROR', message='Reboot failed')
            self.rebooted = False
            return response
        except Exception as exp:
            self.log(level='ERROR', message='Could not reboot')
            self.log(level='ERROR', message=exp)
        return False

    def su(self, password=None, **kwargs):
        """
        Switch to super user

            device_object.su()

        :param password:
            *OPTIONAL* Password of super user
        :return: True if successfully switched to super user, else False
        """
        if password is None:
            if self.su_password is not None:
                user, password = (self.su_user, self.su_password)
            else:
                user, password = self.get_su_credentials()

        su_command = kwargs.get('su_command', 'su -')

        self._switch_mode(mode='shell')
        whoami_resp = self.shell(command='whoami').response()
        if re.search(r'root', whoami_resp, re.I):
            self.log(level='INFO', message="user is already 'root'")
            return True
        else:
            self.shell(command=su_command, pattern='[Pp]assword:[\s]?')
            self.shell(command=password, pattern=[r'#[\s]?', r'%[\s]?', 'Terminal type.*'])
            self.set_prompt_shell(prompt=self.channels['text'].shell_prompt)
            whoami_resp = self.shell(command='whoami').response()
            if re.search(r'root', whoami_resp, re.I):
                self.log(level='INFO', message="Successfully switched to root")
                return True
        self.log(level='ERROR', message='Unable to switch to root!')
        return False

    def reconnect(self, timeout=30, interval=20, force=True):
        """
        Reconnects to JunOS device
            device_object.reconnect()

        :param timeout:
            *OPTIONAL* Time till which reconnection can be attempted. Default
            is 30 seconds
        :param interval:
            *OPTIONAL* Interval in which reconnection needs to be attempted.
            Default is 20 seconds
        :return: True if the reconnection is successful, else False
        """
        timestamp = time.time()
        self._kwargs.pop('channels', None)
        # del self.channels['pyez']
        # del self.channels['text']
        pyez_connected = 0
        if not force:
            if self.connected:
                try:
                    self.log(level='INFO', message='Checking for connection status...')
                    if self.channels['text'].is_active():
                       self.log(level='INFO', message='Connection is alive. Returning True')
                       return True
                    self.log(level='DEBUG', message='Connection is not alive. Trying to re-establish connection.... ')
                except:
                    pass

        self.disconnect(ignore_error=True)
        if ('all' in self.connect_channels or 'pyez' in self.connect_channels) \
             and not self.proxy and self.connect_to_pyez:
            while timeout > 0 and not pyez_connected:
                try:
                    self._connect_pyez()
                    self.log(level='INFO', message='Successfully recreated pyez channel.')
                    pyez_connected = 1
                except Exception:
                    if timeout > 0:
                        self.log(level='INFO', message='Unable to create pyez channel to device.'
                                 ' Trying again in %s seconds' % interval)
                        time.sleep(interval)
                    timeout = timeout - time.time() + timestamp
                    timestamp = time.time()

            if not pyez_connected:
                self.log(level='ERROR',
                         message='Unable to create pyez channel to device.')
                return False
        else:
            self.log(level='info', message="Skipping 'pyez' channel creation as requested by user")

        if 'all' in self.connect_channels or 'text' in self.connect_channels:
            while timeout > 0:
                try:
                    self._connect_text()
                    self.log(level='INFO', message='Successfully recreated text channel.')
                    return True
                except Exception:
                    if timeout > 0:
                        self.log(level='DEBUG', \
                                 message='Unable to create text channel to device. Trying again in %s seconds' % interval)
                        time.sleep(interval)
                    timeout = timeout - time.time() + timestamp
                    timestamp = time.time()
            self.log(level='ERROR', message='Unable to create text channel to device.')
            return False
        else:
            self.log(level='info', message="Skipping 'text' channel creation "
                     "as requested by user")

    def disconnect(self, ignore_error=False):
        """
        Disconnects connection to JunOS device.

            device_object.disconnect()

        :return: True if connection to device is terminated, else False
        """
        response = True

        if self.connected is not True:
            if not ignore_error:
                self.log(level='ERROR', message='{0} object is closed'.format(self.host))
            return False
        else:
            try:
                if not self.rebooted:
                    if 'pyez' in self.channels.keys():
                        self.channels['pyez'].close()
                        del self.channels['pyez']
                    if 'text' in self.channels.keys():
                        self.channels['text'].close()
                        del self.channels['text']
                self.connected = False
            except Exception as exp:
                if not ignore_error:
                    self.log(level='ERROR', message='Error while closing the object')
                    self.log(level='ERROR', message=exp)
                else:
                    self.log(level='DEBUG', message='Error while closing the object')
                    self.log(level='DEBUG', message=exp)
                response = False
        if response:
            self.log(level='INFO', message='Successfully disconnected from Device')
        return response

    def close(self, all=False, ignore_error=False):
        """
        device_object.close()

        Close connection to device and destroys the object.
        For an ssh proxy connection, it is mandatory to close
        the connection using this method.

        :param all_routing_engines
            Close handles of all routing engines
        :return: True if device object is closed successfully, else False
        """
        response = True
        try:
            if self.connected:
                if 'pyez' in self.channels.keys():
                    self.channels['pyez'].close()
        except Exception as exp:
            if not ignore_error:
                self.log(level='ERROR', message='Error while closing the PyEZ channel')
                self.log(level='ERROR', message=exp)
            else:
                self.log(level='INFO', message='Error while closing the PyEZ channel')
                self.log(level='INFO', message=exp)
            response = False
        try:
            if 'text' in self.channels.keys():
                self.channels['text'].close()
        except Exception as exp:
            if not ignore_error:
                self.log(level='ERROR', message='Error while closing the Text channel')
                self.log(level='ERROR', message=exp)
            else:
                self.log(level='INFO', message='Error while closing the Text channel')
                self.log(level='INFO', message=exp)
            response = False
        del self
        if response:
            t.log(level='info', message='Successfully closed Device Handle')
        return response

    def commit(self, **kwargs):
        """
        Commit configurations
            device_object.commit(comment = 'commit successful', timeout = 200)

        :param str comment: If provided logs this comment with the commit.
        :param int confirm: If provided activates confirm safeguard with
                            provided value as timeout (minutes).
        :param int timeout: If provided the command will wait for completion
                            using the provided value as timeout (seconds).
                            By default the device timeout is used.
        :param bool sync: On dual control plane systems, requests that
                            the candidate configuration on one control plane be
                            copied to the other control plane, checked for
                            correct syntax, and committed on both Routing
                            Engines.
        :param bool force_sync: On dual control plane systems, forces the
                            candidate configuration on one control plane to be
                            copied to the other control plane.
        :param bool detail: When true return commit detail as lxml object
        :param bool check:  If True, executes commit check command and checks correctness
                            of syntax and do-not apply changes. If configuration
                            check-out fails then it raises an exception otherwise returns True

        :return: True if commit succeeds. Exception of not.
            Dictionary with the following keys
            'response': Response from the commit command
        """
        timeout = kwargs.get('timeout', self.commit_timeout)
        if timeout is None:
            timeout = self.commit_timeout
        command = 'commit'
        # comment = kwargs.get('comment', '')
        # confirm = kwargs.get('confirm', 'False')

        # if a timeout is provided, then include that in the RPC
        # Check for force_sync and sync

        commit_check = kwargs.get('check', False)
        if commit_check:
            command += ' check'

        if not self.evo:
            sync = kwargs.get('sync', False)
            force_sync = kwargs.get('force_sync', False)
            if sync:
                command += ' synchronize'
                if force_sync:
                    command += ' force'
            elif force_sync:
                command += ' synchronize force'
        else:
            sync = kwargs.get('sync', False)
            force_sync = kwargs.get('force_sync', False)
            if sync:
                self.log(level='INFO', message='Ignoring sync option during commit for EVO')
            elif force_sync:
                self.log(level='INFO', message='Ignoring sync force option ' 'during commit for EVO')

        detail = kwargs.get('detail')
        if detail:
            command += ' | display detail'

        self._switch_mode(mode='config')
        try:
            rsp = self.config(command_list=[command],
                              timeout=timeout)
            if commit_check:
                if rsp.response().find('error: configuration check-out failed') != -1:
                    raise TobyException('commit check failed ' + rsp.response(), host_obj=self)
            elif rsp.response().find('commit complete') == -1:
                raise TobyException('commit failed ' + rsp.response(), host_obj=self)
        except Exception as err:
            raise TobyException(err, host_obj=self)
        return_value = Response(response=rsp.response(), status=True)
        return return_value

    def save_config(self, file, source='candidate', type='normal', timeout=60):
        """
        Save configuration on the device
            device_object.save_config(file = 'temp_config.conf',
            source = 'committed')

        :param file: File name to save the configuration
        :param source: Store 'committed'/'candidate' configuration.
            Default is 'candidate'
        :param type: Type of data in the dumped file.
            Accepted values are 'normal'/'xml'/'set'. Default is 'normal'
        :param timeout:
            *OPTIONAL* Time given to save configuration to device.
            Default is 60 seconds
        :return: Response object with status=True in case of success,
            else it will raise an Exception

        """
        if self.is_evo() and not self.is_master():
            self.log(level='DEBUG', \
               message='Config mode is not supported backup RE on EVO, skipping save config.')
            return True
        command = ' | save ' + file
        if type != 'normal' and type in('set', 'xml'):
            command = ' | display ' + type + command
        elif type == 'normal':
            pass
        else:
            raise TobyException('Invalid value in parameter "type". Accepted values are '
                                '"normal"/"xml"/"set"', host_obj=self)
        if source == 'candidate':
            command = 'show' + command
        elif source == 'committed':
            command = 'run show configuration' + command
        else:
            raise TobyException('Invalid value in parameter "source". Accepted values are '
                                '"committed"/"candidate"', host_obj=self)
        output = self.config(command_list=[command], timeout=timeout).response()
        if output.find("to '" + file + "'") != -1 and \
                output.find("Wrote") != -1:
            return_value = Response(status=True)
            return return_value
        else:
            raise TobyException('Could not save configuration on ' + \
                     self.host + '. Output: ' + output, host_obj=self)

    def load_config(self, *args, **kwargs):
        """

        Loads configuration using file or string to the routing.

        In case a single string is passed, Toby will dump the string to a file.
        dev.load_config('set systen services netconf ssh', option='set')

        In case a list of strings(set commands) is passed,
        Toby will concatenate the strings and dump it to a file.
        dev.load_config(['set systen services netconf ssh','set ...',
        'set ...'], option='set')

        In case a local file is passed, Toby will
        upload the file to the device.
        dev.load_config(local_file='my_config.conf', option='merge')
        dev.load_config(local_file='my_config.set', option='set', timeout=120)
        dev.load_config(local_file='my_config.xml',
        option='override', timeout=120)

        In case a remote file is passed, Toby will check
        if it is present on device and then load it.
        dev.load_config(remote_file='/var/tmp/my_config.conf',
        option='merge', timeout=120)
        dev.load_config(remote_file='/var/tmp/my_config.set',
        option='set', timeout=120)
        dev.load_config(remote_file='/var/tmp/my_config.xml',
        option='override')

        Once a dumped file on the device is available,
        the file is loaded to the device.

        Examples for using **device_filename** :
        dev.load_config('set systen services netconf ssh',
        device_filename='/var/tmp/testcase.set', option='set')
        dev.load_config(['set systen services netconf ssh','set ...',
        'set ...'], device_filename='/var/tmp/testcase.set', option='set')
        dev.load_config(local_file='my_config.xml',
        device_filename='/var/tmp/testcase.set',
        option='override', timeout=120)
        dev.load_config(remote_file='/var/tmp/my_config.conf',
        device_filename='/var/tmp/testcase.set', option='merge', timeout=120)


        :param args[0]:
            **OPTIONAL** The content to load. If the contents is a string,
            toby will attempt to automatically determine the format. If it is a
            list of strings, Toby will concatenate all to be loaded together.
        :param local_file:
            **OPTIONAL** Path to a config file on local server
        :param remote_file:
            *OPTIONAL* Path to a config file on a remote server
            (on current device)
        :param device_filename:
            *OPTIONAL* Dumps the configuration file on device with
            specified name. Default is '/var/tmp/toby_script_<timestamp>.conf'
        :param option:
            *OPTIONAL* Load Options. Supported values are 'merge',
            'replace', 'set', override'. Default is 'merge'.
            For set command strings and list of set command strings,
            use option='set'
        :param commit:
            *OPTIONAL* Issue the 'commit' command after loading the configuration
             Supported values are:
              'False' : Default. Do not issue commit
              'True'  : issue commit once config is loaded successfully
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :return:
            True in case configurtion is loaded successfully, else False
        """
        option = kwargs.get('option', 'merge')
        local_file = kwargs.get('local_file', None)
        remote_file = kwargs.get('remote_file', None)
        time_stamp = time.strftime("%Y%m%d%H%M%S")
        dump_file = kwargs.get('device_filename', '/tmp/toby_script_' + time_stamp + '.conf')
        timeout = kwargs.get('timeout', 60)
        commit = kwargs.get('commit', False)
        _builtin = BuiltIn()
        suite_name = _builtin.get_variable_value("${TEST_NAME}")
        host_name = self.controllers_data.get('hostname') or self.host
        if len(args):
            file_data = ''
            if isinstance(args[0], list):
                for cmd in args[0]:
                    file_data = file_data + '\r\n' + cmd
            elif isinstance(args[0], str):
                file_data = args[0]
            else:
                raise TobyException("args[0] type is invalid. Accepted types are" \
                                    " str/list[str, str ...]", host_obj=self)
            self.log(level='INFO', message='upload config file')
            self.shell(command='')
            local_temp_file = os.path.join(self.device_logger._log_dir, "toby_script_" + \
                                    host_name + "_" + time_stamp + ".conf")
            try:
                wr_fo = open(local_temp_file, "w")
                wr_fo.write(file_data)
                wr_fo.close()
                self.upload(local_file=local_temp_file, remote_file=dump_file, timeout=timeout)
            except Exception as exp:
                raise TobyException('Could not upload file: %s'%str(exp), host_obj=self)
        elif local_file:
            self.upload(local_file=local_file, remote_file=dump_file, timeout=timeout)
        elif remote_file:
            if self.shell(command='ls -lrt ' + remote_file).response().find('No such file or directory') != -1:
                raise TobyException("Mentioned remote file [ %s ] is not present on the device [ %s ]"
                                    % (str(remote_file), str(self.host)), host_obj=self)
            else:
                dump_file = remote_file
        else:
            raise TobyException("'local_file/remote_file/args[0]' option is mandatory")
        try:
            self.log(level='DEBUG', message='loading config file')
            config_response = self.config(
                command_list=['load ' + option + ' ' + dump_file],
                timeout=timeout)
            if config_response.response().find('syntax error') != -1:
                raise TobyException('Syntax Error: ' + config_response.response(), host_obj=self)
        except Exception as exp:
            log_level = 'ERROR'
            if re.search(r'severity:\s+warning', str(exp)):
                log_level = 'WARN'
            self.log(level=log_level, message='Error loading the configurations')
            self.log(level=log_level, message=exp)
            raise exp
        if not config_response.status():
            raise TobyException('Error loading the configurations', host_obj=self)

        if commit is True:
            try:
                commit_response = self.commit()
                commit_rsp_text = commit_response.response()
                return_value = Response(response="Configuration loaded "
                                                 "successfully. " + commit_rsp_text, status=True)
            except Exception as exp:
                raise TobyException("Configuration loaded successfully. Commit Failed. ", status=False)
        else:
            return_value = Response(response='Configuration loaded successfully. ', status=True)

        return return_value


    def software_install(self, package=None, pkg_set=None,
                         remote_path='/var/tmp', progress=True, validate=False,
                         checksum=None, cleanfs=True, reboot=True,
                         no_copy=False, issu=False, nssu=False, vmhost=False,
                         timeout=None, save_restore_baseline=False, **kwargs):
        """
        device_object.software_install(package = '/volume/openconfig/trunk/
        junos-openconfig-x86-32-0.0.0I20161227_1103_rbu-builder.tgz',
        progress = True)

        Performs the complete installation of the **package** that includes the
        following steps:

        1. computes the local MD5 checksum if not provided in :checksum:
        2. performs a storage cleanup if :cleanfs: is True
        3. SCP copies the package to the :remote_path: directory
        4. computes remote MD5 checksum and matches it to the local value
        5. validates the package if :validate: is True
        6. installs the package

        warning:: This process has been validated on the following deployments.
                      Tested:
                      * Single RE devices (EX, QFX, MX, SRX).
                      * MX dual-RE
                      * EX virtual-chassis when all same HW model
                      * QFX virtual-chassis when all same HW model
                      * QFX/EX mixed virtual-chassis
                      * Mixed mode VC
                      * SRX Cluster

                      Known Restrictions:

                      * MX virtual-chassis

        You can get a progress report on this process by setting progress=True.

        note:: You will need to invoke the :meth:`reboot`
        method explicitly to reboot the device.

        :param str package:
            The file-path to the install package tarball
            on the local filesystem

       :param list pkg_set:
         The file-paths as list/tuple of the install package tarballs on
         the local filesystem which will be installed on mixed VC setup.

       :param str remote_path:
         The directory on the Junos device where the package file will be
         SCP'd to or where the package is stored on the device;
         the default is ``/var/tmp``.

       :param bool validate:
         When ``True`` this method will perform a config validation against
         the new image

       :param str checksum:
         MD5 hexdigest of the package file. If this is not provided, then this
         method will perform the calculation. If you are planning on using the
         same image for multiple updates, you should consider using the
         :meth:`local_md5` method to pre calculate this value and then
         provide to this method.

       :param bool cleanfs:
         When ``True`` will perform a 'storeage cleanup' before SCP'ing the
         file to the device.  Default is ``True``.

       :param func progress:
         If provided, this is a callback function with a function prototype
         given the Device instance and the report string::
         If set to ``True``, it uses :meth:`sw.progress`
         for basic reporting by default.

       :param bool no_copy:
         When ``True`` the software package will not be SCP'd to the device.
         Default is ``False``.
       :param bool issu:
         When ``True`` the In-service software upgrade (ISSU) will be done.
         Default is ``False``
       :param bool nssu:
         When ``True`` NSSU upgrade is performed.
         Default is ``False``
       :param int timeout:
         The amount of time (seconds) before declaring an RPC timeout.  This
         argument was added since most of the time the "package add" RPC
         takes a significant amount of time.  The default RPC timeout is
         generally around 30 seconds.  So this :timeout: value will be
         used in the context of the SW installation process. Defaults is
         set based on os/platform/model of the box

       :param bool force_host:
         (Optional) Force the addition of host software package or bundle
         (ignore warnings) on the QFX5100 device.
       """
        if package is None and pkg_set is None:
            raise TobyException('software_install() takes atleast 1 argument package or pkg_set', host_obj=self)

        from jnpr.junos.utils.sw import SW
        dual_re = self.channels['pyez'].facts['2RE']

        if timeout is None:
            if issu is True:
                timeout = self.issu_timeout
            else:
                timeout = self.upgrade_timeout

        # This is added for ISSU on single RE device
        if issu and not dual_re:
            # TODO: move to acx class
            self.model = self.channels['pyez'].facts['model']
            if not self.model.lower().startswith('acx'):
                kwargs['no_reboot'] = True
            kwargs['ignore_warning'] = 'Do NOT use \/user during ISSU'
        t.log(level='info', message='kwargs : %s' % kwargs)

        img_flag = 0
        exact_pkg_name = package.split('/')[-1]
        try:
            if not no_copy and (not re.match(r'^(\/var\/tmp\/)', package, re.I)):
                remote_file = remote_path if remote_path is not None else '/var/tmp/'
                #check for the image on the device
                res = self.shell(command='ls -lrt ' + remote_file+'/'+exact_pkg_name).response()
                if re.search('No such file or directory', res):
                    img_flag = 1
                else:
                    k = re.search(r'\S+\s*\S+\s*\S+\s*\S+\s*(\d+)\s.*', res)
                    size1 = int(k.group(1))
                    #Get the size of image from execution server
                    res2 = os.popen('ls -lrt %s' %package).read()
                    size2 = int(res2.strip().split(' ')[4])
                    #compare the size of image from device and execution server
                    if size1 == size2:
                        self.log(level='WARN', message="Image already exists on the device")
                    else:
                        img_flag = 1

                #if image not present on the device, scp it from the server.
                if img_flag == 1:
                    response = self.shell(command='df -k %s'%remote_path)
                    self.log(level='info', message="Disk space before image copy \n" +str(response.resp))
                    copy_resp = self.upload(local_file=package, remote_file=remote_file)
                    if copy_resp:
                        self.log(level='info', message="Image copy was successful")
                        no_copy = True
                    else:
                        response = self.shell(command='df -k %s'%remote_path)
                        self.log(level='WARN', message="Failed to copy image to image to router")
                        self.log(level='info', message="Disk space after image copy  \n" +str(response.resp))
                        return False
        except Exception as exp:
            raise TobyException('Exception while copying image with %s'%str(exp), host_obj=self)

        response = self.shell(command='df -k %s'%remote_path)
        self.log(level='info', message="Disk space after image copy \n " +str(response.resp))

        if save_restore_baseline:
            self.save_baseline_config()
        try:
            pyez_sw = SW(self.channels['pyez'])
        except Exception as exp:
            raise TobyException('Exception while creating SW object', host_obj=self)

        def sw_install_report(dev, report):
            self.log(level='info', message="%s: PyEZ install() progress: %s"
                     % (dev.hostname, report))

        pre_install_version = str(self.channels['pyez'].facts['version'])
        self.log(level='info', message="JUNOS version prior to upgrade: " + pre_install_version)
        pyez_error = False
        if 'issu_options' in kwargs:
            if kwargs['issu_options'] is not None and len(kwargs['issu_options']) > 0:
                kwargs.update(kwargs['issu_options'])
                self.log(level='info', message="issu_options: %s " % kwargs)
            del kwargs['issu_options']
        try:

            status = pyez_sw.install(
                package=package, pkg_set=pkg_set, remote_path=remote_path,
                progress=sw_install_report, validate=validate, checksum=checksum,
                cleanfs=cleanfs, no_copy=no_copy, issu=issu, nssu=nssu, vmhost=vmhost,
                timeout=timeout, **kwargs)

        except (ConnectClosedError, RpcTimeoutError, RpcError) as error:
            pyez_error = True
            if error.__class__.__name__ == 'RpcError' and not re.search(r'VM setup failed', str(error)):
                raise

            self.log(level='WARN', message="Lost PyEZ connection to device during software install; error: " \
                                           + str(error) + ".  Checking to see if there was a version change...")
            try:
                self.reconnect(timeout=1200)
                status = self.channels['pyez'].facts_refresh()
                post_install_version = str(self.channels['pyez'].facts['version'])
                self.log(level='info', message="JUNOS version after upgrade: " + post_install_version)
                status = True
            except:
                status = False

        if status:
            self.log(level='info', message='Install status : Success')
            if reboot and not pyez_error:
                # reboot old master / new backup
                if vmhost:
                    reboot_status = self.reboot(device_type='vmhost', mode='cli', timeout=timeout)
                else:
                    reboot_status = self.reboot(mode='cli', timeout=timeout)
                if not reboot_status:
                    raise TobyException('Reboot API failed after software install', host_obj=self)
            else:
                time.sleep(120)
                self.reconnect(timeout=1200)
        else:
            self.log(level='info', message='Install status : Failure')


        try:
            self.version = self.get_version(refresh=True)
        except:
            pass

        if save_restore_baseline:
            self.restore_baseline_config()
        return status

    def switch_re_master(self, retry=True):
        """
        device_object.switch_re_master()

            """
        if self.dual_controller is False:
            self.log(level='info', message='Toby connected to only master RE, so skipping RE mastership switchover')
            return True
        try:
            resp = self.cli(command="request chassis routing-engine master switch no-confirm").response()
            if re.search(r'The (other|local) routing engine becomes the master', resp, re.IGNORECASE):
                self.log(level='INFO', message='RE mastership switchover successful')
                time.sleep(5)
                if not self.is_alive():
                    self.log(level='INFO', message='Device reboot initiated for this particular platform/function')
                    self.reconnect(timeout=500)
                return True
            elif retry is True:
                match = re.search(r'Not ready for mastership switch, '
                                  r'try after (\d+) sec.|error: Mastership switch not supported during '
                                  r'fru reconnect', resp)
                if match:
                    if match.group(1) is not None:
                        wait = int(match.group(1)) + 2
                    else:
                        wait = 30
                    self.log(level='INFO', message='A mastership switch was recently executed.'
                             ' Waiting for %s seconds before retrying.' % wait)
                    time.sleep(wait)
                    return_value = self.switch_re_master(retry=False)
                    return return_value
        except Exception as err:
            raise TobyException(str(err), host_obj=self)

    def detect_core(self, core_path=None, system_name=None, re1_hostname=None, command=None):
        """
        Detect cores on the device

            device_object.detect_core()

        :param core_path:
            *OPTIONAL* Path as a list ( where cores to be found).
            Default core_path is
            '/var/crash/*core*' , '/var/tmp/*core*', '/var/tmp/pics/*core*'
        :param system_name:
            *OPTIONAL* Primary resource name of the device
        :param re1_hostname:
        :param command: cli command to get core details

        :Return: Number of cores found in the core_path
        """

        exclude_pattern = self._kwargs.get('core-exclude', None)
        core_cmd = command or 'show system core-dumps'
        def get_cores(fallback_method, core_path):
            if not fallback_method:
                core_raw_output = self.cli(command=core_cmd, format='text').response()
            if core_path:
                exec_core_path = 'ls -ltd ' + core_path
                additional_core = self.shell(command=exec_core_path).response()
                core_raw_output += "\n" + additional_core
            return core_raw_output

        try:
            core_count = 0
            fallback_method = False # set to True if 'show system core-dumps' not available
            if core_path is None:
                core_path = self.core_path

            core_path = ' '.join(core_path)

            dev_start_time = self._device_start_time
            self.log(level='info', message='Device start time : ' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                  time.localtime(dev_start_time)))

            year = self.shell(command='date +%Y').response()
            year = re.sub(r"date \+\%Y.*\n", '', year)
            year = re.sub(r"[^\w| ]", '', year)
            if not hasattr(t, "vmhost_name_timestamp_list"):
                setattr(t, "vmhost_name_timestamp_list", [])
                t.vmhostcore_name_timestamp_list = []
            # If device has vmhost we should be copying any cores from there to Junos
            if self.get_vmhost_infra():
                vmhost_cores = self.cli(command='show vmhost crash', format='text').response()
                vmhost_core_files = re.findall(r'(\d*)\s([a-zA-Z]{3}\s[\s\d]{2}\s+\d+\:\d+)\s+(\S*)', str(vmhost_cores))
                if vmhost_core_files:
                    for c in vmhost_core_files:
                        # Need to first check to make sure the core is new before copying
                        date = c[1]
                        date += ' ' + year
                        epoch_time = float(time.mktime(time.strptime(date, "%b %d %H:%M %Y")))
                        self.log(level='info', message='Core file timestamp '
                                                       'on vmhost : ' + date+' :: epoch time : '+ str(epoch_time))
                        # if epoch_time is not None and epoch_time >= dev_start_time:
                        coresize_name_timestamp = "|".join(c)
                        if coresize_name_timestamp not in t.vmhostcore_name_timestamp_list:
                            cmd = "request vmhost file-copy crash from-jnode " + c[2] + " to-vjunos /var/tmp/" + c[2]
                            self.cli(command=cmd, format='txt')
                            t.vmhostcore_name_timestamp_list.append(coresize_name_timestamp)
                            core_del = self.cli(command='request vmhost cleanup')
                else:
                    self.log(level="INFO", message="No core(s) copied from vmhost")

            core_raw_output = self.cli(command=core_cmd, format='text').response()

            # If 'show system core-dumps' isn't available then default on searching
            # various core paths
            if re.search(r'syntax error', str(core_raw_output), re.I):
                exec_core_path = 'ls -ltd ' + core_path
                core_raw_output = self.shell(command=exec_core_path).response()
                fallback_method = True  # this way we know to not use CLI command later
            else:
                # Make sure to search any paths that are not covered by
                # 'show system core-dumps' but are included in the core_path provided
                core_path_list = core_path.split(' ')
                search = re.findall(r'(/.*)(\*core\*)|(/.*/)(.*core.*)', str(core_raw_output))
                set_of_core_paths = set()
                # add all the paths from 'show system core-dumps' to a set
                for path in search:
                    if path[0]:
                        set_of_core_paths.add(path[0]+"*core*")
                    if path[2]:
                        set_of_core_paths.add(path[2]+"*core*")
                # if 'show system core-dumps' has any path from 'core_path' remove it
                for path in set_of_core_paths:
                    if path in core_path_list:
                        core_path_list.remove(path)
                core_path = ' '.join(core_path_list)
                # if any paths left add them to the search results
                if core_path:
                    exec_core_path = 'ls -ltd ' + core_path
                    additional_core = self.shell(command=exec_core_path).response()
                    core_raw_output += "\n" + additional_core

            # Checks file permission once. If any still contain only 'user' permissions then we cannot be sure
            # the cores have been dumped so we must monitor the file size (times out after 3 minutes)
            if re.search(r'-rw-------', str(core_raw_output), re.M):
                initial_time = time.time()  # take initial timestamp
                core_raw_output = get_cores(fallback_method, core_path)

                cores_still_dumping = True
                timeout = 900
                # Stores all the core files in a dictionary with key based on core path
                # with value as the size of the core
                core_files = re.findall(r'(\d*)\s[a-zA-Z]{3}\s[\s\d]{2}\s+[:\d]+\s+(\S*)', str(core_raw_output))
                # If there are no core files we will skip checking for size
                if not core_files:
                    cores_still_dumping = False
                else:
                    cores_dict = {}
                    for core in core_files:
                        cores_dict[core[1]] = core[0]

                # Since now the core should have dumped since 'others' has permission on the file
                # we want to do a final check to ensure the core has dumped by
                while cores_still_dumping and (time.time() <= (initial_time + timeout)):
                    self.log(level="INFO", message="Core(s) are still currently being dumped. Please wait for 10 seconds "
                             "to see if all cores have dumped by then.\nDumping of core(s) will be "
                             "checked for a maximum of 15 minutes.")
                    core_raw_output = get_cores(fallback_method, core_path)
                    # This regex detects the size and path of each core and stores them in a dictionary
                    core_files = re.findall(r'(\d*)\s[a-zA-Z]{3}\s[\s\d]{2}\s+[:\d]+\s+(\S*)', str(core_raw_output))
                    cores_dict_new = {}
                    for core in core_files:
                        cores_dict_new[core[1]] = core[0]

                    # This checks to see if the size of each core has changed at all
                    for core in cores_dict:
                        # If the file name has changed we need to take another snapshot
                        if core not in cores_dict_new:
                            cores_still_dumping = True # this may have been set to False last loop iteration
                            time.sleep(10)
                            break
                        # If the size is not the same of any core we wait 5 seconds and try again
                        elif cores_dict[core] != cores_dict_new[core]:
                            cores_still_dumping = True # this may have been set to False last loop iteration
                            time.sleep(10)
                            break
                        # This means the file size has not changed
                        else:
                            cores_still_dumping = False

                    # set the current cores to the old dict for comparison in next loop
                    cores_dict = cores_dict_new

                    # If all the file sizes have not changed means all the cores have dumped however during the last
                    # comparison another core may have started dumping. For this reason we want to check one last time
                    # if there are any new cores. If so we will continue checking until timeout is reached
                    if not cores_still_dumping:
                        core_raw_output = get_cores(fallback_method, core_path)
                        core_files = re.findall(r'(\d*)\s[a-zA-Z]{3}\s[\s\d]{2}\s+[:\d]+\s+(\S*)', str(core_raw_output))
                        # Need to store in dictionary before measuring lengths to avoid duplicate core entries
                        cores_dict_temp = {}
                        for core in core_files:
                            cores_dict_temp[core[1]] = core[0]
                        # If there is a new core then need to store the newest snapshot as the old, then
                        # run the loop again and take another new snapshot to compare to the old
                        if len(cores_dict_temp) > len(cores_dict):
                            cores_dict = cores_dict_temp # store the newly found core(s) as older snapshot
                            cores_still_dumping = True # reset

                # If cores do not dump within 15 minutes, issue a warning
                if (time.time() > (initial_time + timeout)) and cores_still_dumping:
                    self.log(level='WARN', message="Core(s) have not finished dumping even after waiting for 15 minutes")

            # if (self.get_vmhost_infra()):      # This will be True if the device belongs to Mt_Rainier(vmhost infra)
                # host_core_path = '/var/crash/*core*'
                # host_core_path = 'vhclient ls -ltd \"' + host_core_path + '\"'
                # self.su()
                # host_core = self.shell(command=host_core_path).response()
                # core_raw_output = core_raw_output + '\n' + host_core

            self.log(level='DEBUG', message='Stage : %s ' %t._stage)
            self.log(level='DEBUG', message='Test Stage : %s ' %t._test_stage)

            if t._test_stage:
                t._stage = t._test_stage
            self.log(level='DEBUG', message='Stage : %s ' %t._stage)
            hstname = self.controllers_data['hostname']

            for line in re.split('\n', str(core_raw_output)):
                result = re.search(r'^(\S+)\s+\d+\s+\S+\s+\S+\s+(\d+)\s+(\S+\s+\d+'
                                   r'\s+\d+\:\d+|\d+)\s+(\S+)', line, re.I)
                if result:
                    permission, size, date, core_name = result.groups()

                    core_rename = 're0'
                    if hasattr(self, 're_name'):
                        if not self.re_name == str(None): core_rename = self.re_name

                    if not int(size):
                        if exclude_pattern and not re.search(exclude_pattern, core_name):
                            self.log(level='WARN', message='Core has zero size : ' +
                                     core_name)
                    elif core_name is None:
                        continue

                    elif re.search(r'trap_fpc\S+\.core\.\d+', core_name, re.I):
                        continue
                    elif re.search(r'ttrace_fpc\S+\.core\.\d+', core_name, re.I):
                        continue
                    elif re.search(r'\/gcov-\S+\.core\.\d+', core_name, re.I):
                        continue
                    elif re.search(r'(\/cores\/)', core_name):
                        continue

                    if not re.search(r'\.(?:\d+|[t]*gz)$', core_name, re.I):
                        self.log(level='DEBUG',
                                 message='Seems some core pattern found but not compressed to tgz or gz '
                                         'format : ' + core_name)
                        self.log(level='DEBUG', message="Checking whether '%s' is a file type or not.." % core_name)
                        if re.search(r'^-', permission):
                            self.log(level='WARN', message='Found uncompressed core : ' + core_name)
                        else:
                            self.log(level='INFO',
                                     message='Skipping %s since it is neither in file format nor in '
                                             'tgz format ' % core_name)
                            continue

                    res = re.search(r'(.*\/)(.*)', core_name)
                    if res:
                        core_found_path, core_filename = res.group(1), res.group(2)
                    else:
                        continue
                    date += ' ' + year
                    epoch_time = float(time.mktime(time.strptime(date, "%b %d %H:%M %Y")))
                    core_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
                    self.log(level='info', message='Core file timestamp '
                                                   'on router :' + core_timestamp+ " :: epoch time :"+str(epoch_time))
                else:
                    continue

                # if epoch_time is not None and epoch_time >= dev_start_time:
                stage = t._stage
                if system_name: resource_id = system_name

                if not resource_id in t.cores:
                    t.cores[resource_id] = {}

                if resource_id in t.cores:
                    if not hstname in t.cores[resource_id]:
                        t.cores[resource_id][hstname] = {}
                        if not 'core_full_path_list' in t.cores[resource_id][hstname]:
                            t.cores[resource_id][hstname]['core_full_path_list'] = []


                core_exist = core_filename + core_rename if (self.evo) \
                                else core_filename + '|' + date + '|' + core_rename
                if not exclude_pattern or (exclude_pattern and not re.search(exclude_pattern, core_filename)):
                    self.log(level='INFO',
                             message='Core is found, checking whether the core (%s) is logged or not ' % core_exist)
                    self.log(level='DEBUG', message='t.core_list : %s' % t.core_list)

                    if resource_id in t.core_list and core_exist in t.core_list[resource_id]:
                        self.log(level='INFO', message='Core is already logged (%s) ' % core_exist)
                        continue
                    else:
                        self.log(level='DEBUG',
                                 message='Core is not logged (%s). Adding to the list of the cores found ' % core_exist)

                    self.log(level='INFO', message='t.core_list : %s' % t.core_list)
                    core_count += 1
                    core_id = 'core' + str(core_count) + core_rename
                    core_full_path = None
                    if stage and system_name:
                        t.core[stage][resource_id][core_id] = defaultdict(dict)
                        t.core[stage][resource_id][core_id]['core_name'] = core_filename
                        t.core[stage][resource_id][core_id]['core_src_path'] = core_found_path
                        t.core[stage][resource_id][core_id]['core_timestamp'] = core_timestamp
                        t.core[stage][resource_id][core_id]['core_size'] = size
                        t.core[stage][resource_id][core_id]['core_re'] = core_rename
                        if re1_hostname is not None: t.core[stage][resource_id][core_id]['host1'] = re1_hostname

                        core_full_path = core_found_path + core_filename
                        t.core_list[resource_id].append(core_exist)

                        self.log(level="DEBUG", message="Creating core path for the resource "
                                 "in t.cores : " + resource_id + " and list is " + core_full_path)
                        t.cores[resource_id][hstname]['core_full_path_list'].append(core_full_path)

                    self.log(level='info', message='Core [' + core_name + ']: ' + size + ' bytes added to the core list.')
                    self.log(level='info', message='Core found (' + core_name + ';' + core_timestamp + ')')
                else:
                    self.log(level='info', message='Skipping core '+ core_filename + ' as exclude pattern is set '
                                                                                     'to :: '+ str(exclude_pattern))
                # else:
                #     self.log(level='info', message='Skipping core '
                #                                    '' + core_name + ' as the core is found before script started.')
        except Exception as err:
            raise TobyException("Error in detect_core " + str(err), host_obj=self)
        return core_count


    def get_model(self):
        '''
        Gets the model info from the router.
        '''
        if hasattr(self, 'model') and self.model is not None:
            return self.model
        else:
            try:
                if 'pyez' in self.channels and self.channels['pyez'] is not None:
                    self.model = self.channels['pyez'].facts['model']
                if hasattr(self, 'model') and self.model is not None:
                    return self.model
                else:
                    self.log(level="DEBUG", message="Not able find model using pyez channel, trying using text channel")
                    resp_xml = self.cli(command='show version', format='xml').response()
                    match = re.search(r"(\<rpc\-reply.*\<\/rpc\-reply\>)", str(resp_xml), re.S)
                    if match:
                        resp_xml = match.group(1)
                    if resp_xml:
                        root = etree.fromstring(resp_xml)
                        for product_model in root.getiterator('product-model'):
                            self.model = product_model.text.upper()
                    if self.model:
                        self.log(level="DEBUG", message="Exiting 'get_model' with"
                                " return value/code "+str(self.model))
                        return self.model
                    else:
                        self.log(level="WARN", message="Exiting 'get_model' with"
                                " return value/code "+str(None))
                        return None
            except:
                raise TobyException("Could not get model info", host_obj=self)

    def get_version(self, major=False, refresh=False):
        '''
            get the junos version info from the router.
            :param major
                **OPTION** Setting the major argument will return only
                the major version info. Default: False
             :return:
                junos version: returns the version information about
                the software specified
        '''

        if major:
            if self.major_version is not None and refresh is False:
                return self.major_version
        else:
            if self.version is not None and refresh is False:
                return self.version
        try:
            if 'pyez' in self.channels and self.channels['pyez'] != None:
                self.version = self.channels['pyez'].facts['version']
                if self.version is None:
                    self.version = self._get_version_from_textchnl()
            else:
                self.log(level="DEBUG", message="No pyez channel found, trying using text channel")
                self.version = self._get_version_from_textchnl()

            if self.version is not None:
                match = re.search(r'(\d+\.\d+).*', self.version)
                if match:
                    self.major_version = match.group(1)
            else:
                self.log(level='WARN', message="Could not find the version and returning None")
                return None

            if major:
                return self.major_version
            else:
                return self.version

        except:
            raise TobyException("Could not get version info", host_obj=self)

    def _get_version_from_textchnl(self):
        version = None
        resp_xml = self.cli(command='show version', format='xml').response()
        match = re.search(r"(\<rpc\-reply.*\<\/rpc\-reply\>)", str(resp_xml), re.S)
        if match:
            resp_xml = match.group(1)
        if resp_xml:
            root = etree.fromstring(resp_xml)
            for junos_version in root.getiterator('junos-version'):
                version = junos_version.text

        self.log(level="DEBUG", message="Exiting '_get_version_from_textchnl' " \
                                        "with return value/code " + str(version))
        return version

    def _check_interface_status(self, interfaces, timeout=40, interval=10):
        """
            This checks the interface status on all the junos resources
            :Returns: True if all the interfaces are UP else False
        """
        retry = 1

        while timeout > 0 and retry:
            output = self.cli(command='show interfaces terse', format='text').response()
            for interface in interfaces:
                if re.search(r"^" + re.escape(interface), output, re.MULTILINE):
                    intf = r"^" + re.escape(interface) + r"\s+(\S+)\s+(\S+)"
                    result = re.search(intf, output, re.MULTILINE)
                    message = ''
                    if result:
                        admin, link = result.groups()
                        t.log(level='INFO', message=str(admin))
                        if link == "up":
                            self.log(level="INFO", message="Interface " + str(interface) + " link status is : up")
                            retry = 0
                        else:
                            message = "Interface " + str(interface) + " link status is down. "
                            retry = 1
                    else:
                        message = "Could not fetch the status of the interface."
                        retry = 1
                else:
                    retry = 1
                    message = "Interface " + str(interface) + " specified in yaml does not exists on the router."
                if retry:
                    timeout = timeout - interval
                    if timeout > 0:
                        self.log(level="WARN", message=str(message) + ' Trying again in %s seconds' % interval)
                    else:
                        self.log(level="ERROR", message=str(message))
                    time.sleep(interval)
                    break

        if retry:
            return False
        return True

    def get_facts(self, attribute=None, refresh=False):
        """
        This API returns facts/device type
            Eg: evo, tvp, vc_chassis, ha, mt_rainier, manufacturing_mode
            device_object.get_facts()
        :param attribute
            **OPTIONAL** List of attributes. Ex : ['tvp', 'evo']
         :return: directory if list of attributes passed
        """
        attributes_all = ['model', 'version', 'evo', 'tvp', 'vmhost_infra', 'manufacturing_mode', 'vc_chassis', 'ha']
        # list_of_dicts = []
        if attribute is not None:
            if isinstance(attribute, list):
                attributes = attribute
            else:
                attributes = [attribute]
        else:
            attributes = attributes_all

        facts_results = dict()

        for att_key in attributes:
            facts_results[att_key] = self._get_fact(att_key, refresh)

        if attribute is None:
            return self.facts
        else:
            if len(attributes) == 1:
                return facts_results[attribute]
            else:
                return facts_results

    def _get_fact(self, attribute, refresh=False):
        """
        _get_fact function
        """
        fact_func = "_get_%s" % attribute
        func = getattr(self, fact_func)
        if attribute == 'model' or attribute == 'version':
            return_value = func(refresh=refresh)
        else:
            return_value = func()
        return return_value

    def _get_evo(self):
        """
        This API is to find weather the box is TVP box are not.
        :param major
            **Model** model of the box.
            Default: None
        :return:
            returns the True if the box belogs to tvp box.

        """
        try:
            if 'evo' in self.facts:
                return self.facts['evo']
            else:
                self.facts['evo'] = self.is_evo()
                return self.facts['evo']
        except Exception as exp:
            self.log(level='ERROR', message=exp)
            self.log(level='WARN', message="Not able to find evo attribute info")
            return None

    def _get_tvp(self):
        """
        This API is to find weather the box is TVP box are not.
        :param major
            **Model** model of the box.
            Default: None
        :return:
            returns the True if the box belogs to tvp box.

        """
        try:
            if 'tvp' in self.facts:
                return self.facts['tvp']
            model = self.model
            res = self.shell(command='sysctl -n hw.product.model').response()
            if re.search(r'pvi-model', res):
                self.facts['tvp'] = True
                return self.facts['tvp']
            if model:
                if re.search(r'(ocx|acx50)', model):
                    cmd = 'show version detail | no-more | match \"JUNOS ' + 'Host Software\"'
                    resp = self.cli(command=cmd).response()
                    self.facts['tvp'] = bool(re.search(r'JUNOS Host Software', resp))
                    return self.facts['tvp']
                else:
                    self.facts['tvp'] = False
                    return self.facts['tvp']
        except Exception as exp:
            self.log(level='ERROR', message=exp)
            self.log(level='WARN', message="Unable to set tvp attribute info")
            return None

    def get_vmhost_infra(self):

        """
        This API is to find weather the box is running vmhost or not (Mt Rainier)
        :return:
            returns the True if the box is running vmhost (Mt Rainier box) or not

        """
        try:
            if 'mt_rainier' in self.facts:
                return self.facts['mt_rainier']

            chassis_model = self.cli(
                command='show chassis routing-engine | grep Model').response()
            if re.search(r'Model.*?2X00x[4|6|8]$', chassis_model, re.I):
                self.facts['mt_rainier'] = True
                return self.facts['mt_rainier']

            model = self.get_model()
            self.facts['mt_rainier'] = False

            try:
                if re.search(r'^(nfx|ex)', model, re.I):
                    res = self.shell(command='sysctl -a | grep vmhost').response()
                    if re.search(r'(hw.product.pvi.config.platform.vmhost_support:\s*1|hw.product.pvi.config.platform.tvp_vmhost:\s*1)', res):
                        self.facts['mt_rainier'] = True
                elif not re.search(r'^mx104$', model, re.I):
                    res = self.shell(command='sysctl -a | grep vmhost_mode').response()
                    search = re.search(r'hw.re.vmhost_mode:\s*(\d+)', res)
                    self.facts['mt_rainier'] = bool(
                        search and int(search.group(1)) == 1)
                else:
                    self.facts['mt_rainier'] = False
            except Exception:
                self.log(level='WARN', message="Unable to process vmhost infra command")

            return self.facts['mt_rainier']

        except Exception:
            self.log(level='WARN', message="Unable to set mt_rainier attribute")
            return None

    def _get_manufacturing_mode(self):

        """
        This API is to find weather manufacturing mode enabled
        on the box are not.
        :return:
            returns the True if the manufacturing mode enabled on the box.
         """
        try:
            if 'manufacturing_mode' in self.facts:
                return self.facts['manufacturing_mode']
            response = self.config(command_list=["show chassis"]).response()
            fpc_search = re.search('fpc', response)
            manuf_search = re.search('boot -h -m manufacturing', response)
            self.facts['manufacturing_mode'] = bool(response and(fpc_search and manuf_search))
            return self.facts['manufacturing_mode']
        except Exception as exp:
            self.log(level='WARN', message=exp)
            self.log(level='WARN', message="Unable to set manufacturing mode attribute")
            return None

    def _get_ha(self):

        """
        This API is to find weather box is ha cluster box are not.
        :return:
            returns the True ha enabled on the box.
         """
        if 'ha' in self.facts:
            return self.facts['ha']
        model = self.model
        if model is None:
            model = self.get_model()
        if re.match(r'srx', model, re.I):
            self.facts['ha'] = bool(self.is_ha)
        else:
            self.facts['ha'] = None
        return self.facts['ha']

    def _get_vc_chassis(self):
        """
        This API is to find weather vc enabled on the box are not.
        :return:
            returns the True if the it is a vc enabled on the box.
         """
        try:
            if 'vc_chassis' in self.facts:
                return self.facts['vc_chassis']
            model = self.model
            if re.match(r'vmx|mx', model, re.I):
                res = self.shell(command='jwhoami -C').response()
                global_re = None
                if res:
                    search = re.search(r'group type\s+(\d+)', res.replace('\n', ''))
                    if int(search.group(1)) == 5:
                        self.facts['vc_chassis'] = True
                        search = re.search(r'current protocol mode\s+(\d+)', res.replace('\r\n', ''))
                        protocol_mode = int(search.group(1))
                        if protocol_mode == 1:
                            global_re = 'master'
                        elif protocol_mode == 2:
                            global_re = 'backup'
                        elif protocol_mode == 0:
                            global_re = 'local'
                    else:
                        self.facts['vc_chassis'] = False
                    return (self.facts['vc_chassis'], global_re)
            else:
                self.facts['vc_chassis'] = False
                return self.facts['vc_chassis']
        except Exception as exp:
            self.log(level='WARN', message=exp)
            self.log(level='WARN', message="Unable to set vc_chassis attribute")
            return None

    def get_package_architecture(self):
        """
            Get architecture of the package installed on the box.

            device_object.get_package_architecture()
        """
        res = self.cli(command="show version detail").response()
        if res:
            search = re.search(r'(64-bit Kernel|Kernel\s+64-bit)', res, re.I)
            arch = '64' if search else '32'
            self.log(level='INFO', message="Kernel architecture: %s" % arch)
        else:
            arch = '32'
            self.log(level='INFO', message="Setting default architecture: %s" % arch)
        return arch

    def _get_model(self, refresh=False):

        """
        This API is to find model of the  box.
        :return:
            returns the model the box.
         """
        self.log(level="DEBUG", message="Entering '_get_model'\n" + __file__)
        if 'model' in self.facts:
            self.log(level="DEBUG", message="Exiting '_get_model' with return "
                     "value/code "+str(self.facts['model']))
            return self.facts['model']
        else:
            self.facts['model'] = None
            self.facts['model'] = self.get_model()
        self.log(level="DEBUG", message="Exiting '_get_model' with return " \
                 "value/code " + str(self.facts['model']))
        return self.facts['model']

    def _get_version(self, refresh=False):

        """
        This API is to find version of the  box.
        :return:
            returns the version the box.
         """
        self.log(level="DEBUG", message="Entering '_get_version'\n" + __file__)
        if 'version' in self.facts and (refresh is False):
            self.log(level="DEBUG", message="Exiting '_get_version' with return "
                     "value/code " + str(self.facts['version']))
            return self.facts['version']
        else:
            self.facts['version'] = None
            self.facts['version'] = self.get_version(refresh=refresh)
        self.log(level="DEBUG", message="Exiting '_get_version' with return "
                 "value/code "+str(self.facts['version']))
        return self.facts['version']

    def get_host_name(self):
        """
        This API is to return hostname of the device
        :return
            returns hostname
        """
        return self.controllers_data['hostname']

    def save_baseline_config(self, remote_path='/var/tmp', timeout=120):
        """
        Save configuration on the device
            device_object.save_baseline_config(local_path = '/var/tmp',
            timeout = 120)

        :param local_path:  Baseline config file path on the router
        :param timeout:
            *OPTIONAL* Time given to save configuration to device.
            Default is 120 seconds
        :return: Response object with status=True in case of success,
            else it will raise an Exception
        """
        remote_file = remote_path + "/baseline-config.conf"
        hostname = self.host
        if not hasattr(self, 'log_dir'):
            #self.log_dir = get_log_dir()
            setattr(self, 'log_dir', get_log_dir())
        local_file = self.log_dir + "/" + hostname + "-baseline-config.conf"
        copy_resp = self.download(local_file=local_file, remote_file=remote_file)
        if copy_resp:
            self.log(level='info', message="Basline config is saved at log path: %s" % local_file)
        else:
            raise TobyException('Could not save baseline configuration to log path %s' % local_file, host_obj=self)

    def restore_baseline_config(self, remote_path='/var/tmp', timeout=120):
        """
        Save configuration on the device
            device_object.restore_baseline_config(remote_path = '/var/tmp',
            timeout = 120)

        :param remote_path:  Baseline config file path on the router
        :param timeout:
            *OPTIONAL* Time given to restore basline configuration to device.
            Default is 120 seconds
        :return: Response object with status=True in case of success,
            else it will raise an Exception
        """
        remote_file = remote_path + "/baseline-config.conf"
        hostname = self.host
        if not hasattr(self, 'log_dir'):
            setattr(self, 'log_dir', get_log_dir())
        local_file = self.log_dir + "/" + hostname + "-baseline-config.conf"
        self.su()
        copy_resp = self.upload(local_file=local_file, remote_file=remote_file)
        if copy_resp:
            self.log(level='info', message="Basline config restore successufll on the box at path: %s" % remote_file)
        else:
            raise TobyException('Could not restore baseline configuration %s', host_obj=self)
