"""
    Host module
"""

import logging
import re
import time
import xml.dom.minidom as minidom
from lxml import etree
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.logger.logger import Logger
from jnpr.toby.exception.toby_exception import TobyException
# pylint: disable=protected-access
class Host(object):
    """
        Host class
    """
    # This is to keep track of number of object for a device.
    _object_counts = {}

    def _next_log_file_name(self, name):
        """
            Get next valid log filename
            If the log filename already has logger created,
            it increments the integer value and creates a new name
            by appending new integer.

            :param name:
                **REQUIRED** Name of the device which user had sent to create TobyLogger object
            print("open if self.proxy")

            :return:  next valid log filename to be used for logging
        """
        if name not in self._object_counts or self._object_counts[name] < 0:
            self._object_counts[name] = 0
            return name
        else:
            self._object_counts[name] += 1
        return name + '.' + str(self._object_counts[name])  # if Device, then Device0

    def get_credentials(self, **kwargs):
        """
        Populates user and password based on user inputs.

        DESCRIPTION:
            Populates self.user and self.password based on user inputs. If user
            has not provided then try to get them from default credentials. Else
            raise an exception.

        ARGUMENTS:
            [kwargs]
            :param STR user:
                *OPTIONAL* user name
            :param STR password:
                *OPTIONAL* password of the device
            :param STR ssh_key_file:
                *OPTIONAL* ssh key value

        ROBOT USAGE:
            NOT EXPOSED TO ROBOT USAGE

        :return: Tuple containing username and password
        """


        # Check if user and password are passed arguments
        if (not kwargs.get('user') or not kwargs.get('password')) and \
                (not kwargs.get('user') or not kwargs.get('ssh_key_file')):
            if self.os.upper() == 'JUNOS':
                dev_cred = credentials.JUNOS
            elif self.os.upper() in ("UNIX", "LINUX", "CENTOS", "FREEBSD", "UBUNTU"):
                dev_cred = credentials.UNIX
            elif self.os.upper() == 'IOS':
                dev_cred = credentials.IOS
            elif self.os.upper() == 'SPIRENT':
                dev_cred = credentials.SPIRENT
            elif self.os.upper() == 'BREAKINGPOINT':
                dev_cred = credentials.BREAKINGPOINT
            elif self.os.upper() == 'PARAGON':
                dev_cred = credentials.PARAGON
            elif self.os.upper() == 'BPS':
                dev_cred = credentials.BREAKINGPOINT
            elif self.os.upper() == 'ELEVATE':
                dev_cred = credentials.ELEVATE
            elif self.os.upper().startswith('IX'):
                dev_cred = credentials.IXIA
            elif self.os.upper() == 'WINDOWS':
                dev_cred = credentials.WINDOWS
            else:
                raise TobyException('Unknown Device OS', host_obj=self)
            # Check if default credentials are available
            if not dev_cred['USERNAME'] and not dev_cred['PASSWORD']:
                raise TobyException("Username/Password cannot be determined", host_obj=self)
            return dev_cred['USERNAME'], dev_cred['PASSWORD']
        if kwargs.get('ssh_key_file', None):
            return kwargs['user'], kwargs.get('password', None)
        else:
            return kwargs['user'], kwargs['password']

    def get_enable_password(self):
        """
        Retrieves enable password

        ARGUMENTS:
            [self]
            :param:None

        ROBOT USAGE:
            NOT EXPOSED TO ROBOT USAGE

        :return: enable password
        """
        if self.os.upper() == 'IOS':
            dev_cred = credentials.IOS
        else:
            return None
        return dev_cred['ENABLEPASSWORD']

    def get_su_credentials(self):
        """
        Retrieves superuser credentials

        ARGUMENTS:
            [self]
            :param:None

        ROBOT USAGE:
            NOT EXPOSED TO ROBOT USAGE

        :return: tuple containing superuser and superuser password
        """
        if self.os.upper() == 'JUNOS':
            dev_cred = credentials.JUNOS
        elif self.os.upper() == 'UNIX' or self.os.upper() == 'LINUX' or \
                self.os.upper() == 'CENTOS' or self.os.upper() == 'UBUNTU' or \
                self.os.upper() == 'FREEBSD':
            dev_cred = credentials.UNIX
        elif self.os.upper() == 'IOS':
            dev_cred = credentials.IOS
        else:
            raise TobyException('Unkown Device OS', host_obj=self)
        return dev_cred['SU'], dev_cred['SUPASSWORD']

    def __init__(self, *args, **kwargs):
        self.host = kwargs['host']
        self.os = kwargs['os']
        #self.model = kwargs.get('model', None)
        self.proxy = False
        self.connect_mode = kwargs.get('connect_mode', 'telnet')
        self.tag = kwargs.get('tag')
        if 'text_port' in kwargs and kwargs['text_port'] is not None:
            self.text_port = int(kwargs['text_port'])
        else:
            self.text_port = None
        self.user, self.password = self.get_credentials(**kwargs)
        self.enable_password = self.get_enable_password()
        self.ssh_key_file = kwargs.get('ssh_key_file')
        self.proxy_host = None
        self.proxy_user = None
        self.proxy_password = None
        self.proxy_port = None
        self.proxy_ssh_key = None
        self.tag_name = kwargs.get('tag_name', None)
        self.re_name = kwargs.get('re_name',None)
        self.su_user = kwargs.get('su_user', 'root')
        self.su_password = kwargs.get('su_password', None)
        self.controllers_data = {}
        ## Set default timeout values for each object
        self.shell_timeout = 120
        self.cli_timeout = 120
        self.vty_timeout = 60
        self.cty_timeout = 60
        self.pyez_timeout = 60
        self.config_timeout = 60
        self.commit_timeout = 240
        self.reboot_timeout = 480
        self.upgrade_timeout = 600
        self.issu_timeout = 1200
        self.global_logger_flag = kwargs.get('global_logging', True)
        self.device_logger_flag = kwargs.get('device_logging', True)
        self.connect_timeout = kwargs.get('timeout', 30)
        if 'proxy_hosts' in kwargs and len(kwargs['proxy_hosts']) > 0:
            self.proxy = True
            self.proxy_host = kwargs['proxy_hosts'][0].get('host')
            self.proxy_user = kwargs['proxy_hosts'][0].get('user')
            self.proxy_password = kwargs['proxy_hosts'][0].get('password')
            self.proxy_port = kwargs['proxy_hosts'][0].get('port', 22)
            self.proxy_ssh_key = kwargs['proxy_hosts'][0].get('ssh_key_file')
        if 'hostname' in kwargs:
            self.name = kwargs['hostname']
            self.logger_name = self._next_log_file_name(self.name)
        else:
            self.name = self.host
            self.logger_name = self._next_log_file_name(self.host)

        try:
            t
            self.t_exists = True
        except NameError:
            self.t_exists = False

        if self.t_exists:
            console = True
            if t.is_robot is True:
                console = False
            if self.global_logger_flag:
                self.global_logger = Logger(t._script_name, console=console)
            if self.device_logger_flag:
                self.device_logger = Logger(self.logger_name, console=False)
        else:
            if self.device_logger_flag:
                self.device_logger = Logger(self.logger_name, console=True)

        self.log(
            level="Debug",
            message="Login User:" + self.user)
        if self.password is not None:
            self.log(
                level="Debug",
                message="Login Password:" + self.password)
        if self.ssh_key_file is not None:
            self.log(
                level="Debug",
                message="Login ssh key file:" + self.ssh_key_file)

    def log(self, level=None, message=None):
        """
        Create a log entry

        self.log('WARN', "This is a warning!")
        self.log('This is info')
        self.log('This is more info')

        :param level:
            *OPTIONAL* log level
        :param message:
            *MANDATORY* message to write to log

        ROBOT USAGE:
            NOT EXPOSED TO ROBOT USAGE

        :return: none
        """
        if level is None and message is None:
            raise TobyException("Issued 'log' without arguments. t.log() Requires min 1 argument.", host_obj=self)
        if level is not None and message is None:
            # User didn't pass in level, but passed in unnamed message
            message = level
            level = 'INFO'

        if level is None and message is not None:
            # User passed in named message only
            level = 'INFO'
        log_level_int = logging._nameToLevel[level.upper()]
        if isinstance(message, etree._Element):
            res = etree.tounicode(message, pretty_print=True)
            res = minidom.parseString(res).toprettyxml()
            message = res
        if self.device_logger_flag:
            self.device_logger._log(getattr(logging, level.upper()), message, ())

        tag_name = self.tag_name if 'tag_name' in dir(self) and self.tag_name is not None else ''
        re_name = self.re_name if 're_name' in dir(self) and self.re_name is not None else ''
        global_log_message = "[" + str(tag_name) + " " + str(self.logger_name) + " " + str(re_name) + "] " + str(message)

        if self.t_exists:
            if t.is_robot:
                import robot.api.logger as robot_logger
                if self.device_logger_flag:
                    if log_level_int >= self.global_logger.level:
                        log_func = getattr(robot_logger, level.lower())
                        log_func(global_log_message)
                        if t.background_logger: # prints logs for run_multiple
                            t.background_logger.write(global_log_message, level.upper())
                if 'console_log' in t.t_dict.keys():
                    if t.t_dict['console_log']:
                        con_log_func = getattr(robot_logger, 'console')
                        con_log_func(global_log_message)
            if self.global_logger_flag:
                self.global_logger._log(
                    getattr(logging, level.upper()), global_log_message, ())

    def upload(self, local_file, remote_file, protocol=None,
               user=None, password=None, timeout=30):
        if user is None:
            user = self.user
        if password is None:
            password = self.password
        protocols = []
        if protocol is None:
            protocols = ['scp', 'ftp']
        else:
            protocols = [protocol]

        host = self.host
        if hasattr(self, "controllers_data"):
            if 'mgt-ip' in self.controllers_data:
                host = self.controllers_data['mgt-ip']
        try:
            for protocol in protocols:
                self.log(level='DEBUG', message='uploading %s file using %s protocol' % (local_file, protocol))
                if protocol.lower() == 'ftp':
                    from jnpr.toby.utils.ftp import FTP as file_transfer
                elif protocol.lower() == 'scp':
                    from jnpr.toby.utils.scp import SCP as file_transfer
                else:
                    raise TobyException('Invalid transfer Protocol', host_obj=self)
                for ssh_retry in range(0, 3):
                    try:
                        with file_transfer(host, user=user, password=password, proxy=self.proxy, port=self.text_port,
                                           proxy_host=self.proxy_host, proxy_user=self.proxy_user,
                                           proxy_ssh_key=self.proxy_ssh_key, proxy_password=self.proxy_password,
                                           proxy_port=self.proxy_port, progress=True, timeout=timeout) as file_tnsfr:
                            file_tnsfr.put_file(local_file=local_file, remote_file=remote_file)
                            return True
                    except Exception as exp:
                        if re.search(r'(Error reading SSH protocol banner|Authentication timeout)', str(exp)):
                            self.log(level='DEBUG', message='Upload failed, retrying...')
                            if ssh_retry < 1:
                                time.sleep(2)
                                continue
                            else:
                                self.log(level='DEBUG', message='Upload failed using %s protocol, Error: %s' %(protocol, str(exp)))
                                break
                        else:
                            self.log(level='DEBUG', message='Upload failed using %s protocol, Error: %s' %(protocol, str(exp)))
                            break
            else:
                raise TobyException('Uploading %s file using %s protocol failed' %(local_file, protocols))
        except Exception as exp:
            raise TobyException('Error: %s'%str(exp), host_obj=self)

    def download(self, remote_file, local_file, protocol=None,
                 user=None, password=None, timeout=30):
        if user is None:
            user = self.user
        if password is None:
            password = self.password

        protocols = []
        if protocol is None:
            protocols = ['scp', 'ftp']
        else:
            protocols = [protocol]

        host = self.host
        if hasattr(self, "controllers_data"):
            if 'mgt-ip' in self.controllers_data:
                host = self.controllers_data['mgt-ip']
        try:
            for protocol in protocols:
                self.log(level='DEBUG', message='downloading %s file using %s protocol' % (remote_file, protocol))
                if protocol.lower() == 'ftp':
                    from jnpr.toby.utils.ftp import FTP as file_transfer
                elif protocol.lower() == 'scp':
                    from jnpr.toby.utils.scp import SCP as file_transfer
                else:
                    raise TobyException('Invalid transfer Protocol', host_obj=self)
                get_file_list = remote_file.split(':')
                for my_list in get_file_list:
                    try:
                        with file_transfer(host, user=user, password=password, proxy=self.proxy, port=self.text_port,
                                       proxy_host=self.proxy_host, proxy_user=self.proxy_user,
                                       proxy_password=self.proxy_password, proxy_ssh_key=self.proxy_ssh_key,
                                       proxy_port=self.proxy_port, progress=True, timeout=timeout) as file_tnsfr1:
                             file_tnsfr1.get_file(local_file=local_file, remote_file=my_list)
                    except Exception as exp:
                        self.log(level='DEBUG', message='Download failed using %s protocol, Error: %s' %(protocol, str(exp)))
                return True        

            else:
                raise TobyException('Downloading %s file using %s protocol failed' %(remote_file, protocols))
        except Exception as exp:
            raise TobyException('Error: %s'%str(exp), host_obj=self)


def upload_file(dev, *args, **kwargs):
    """
    Transfers file from local execution server/machine to host

    ARGUMENTS:
        :param STR local_file:
            *MANDATORY* Full path along with filename which has to be copied to the host.
                        This could be a string or list of files
        :param STR remote_file:
            *MANDATORY* File to create on the router
        :param STR protocol:
            *OPTIONAL* Transfer protocol that needs to be used.
            Acceptable values are ftp , scp or None.
            In case of None, scp is used if the device is connected via ssh else ftp is used
        :param STR user:
            *OPTIONAL* Username to be used to transfer the file.
            If not provided username from device object is taken
        :param STR password:
            *OPTIONAL* Password to be used to transfer the file.
            If not provided password from device object is taken
        :param INT timeout:
            *OPTIONAL* maximum time to upload file to a device.
                       Default is set To 30

    ROBOT USAGE:
        ${device-handle} =   Get Handle   resource=r1
        Upload File      local_file=/var/temp/iiaka.py   remote_file=/tmp/value/
          ...    user=root   password=xuma  timeout=${202}   protocal=scp

    returns:True if the file transfer is successful, else Exception is raised
    """
    result = dev.upload(*args, **kwargs)
    if not result:
        raise TobyException('Upload file failed')
    return result


def download_file(dev, *args, **kwargs):
    """
    Transfers file from host to local execution server/machine

    ARGUMENTS:
        [remote_file, local_file, protocol=None,user=None, password=None, timeout=30]

        :param STR local_file:
            *MANDATORY* Full path along with filename which has to be copied to the host.
            This could be a string or list of files
        :param STR remote_file:
            *MANDATORY* File to create on the router
        :param STR protocol:
            *OPTIONAL* Transfer protocol that needs to be used.
                 Acceptable values are ftp , scp or None.
                 In case of None, scp is used if the device is connected via ssh else ftp is used
        :param STR user:
            *OPTIONAL* Username to be used to transfer the file.
            If not provided username from device object is taken
        :param STR password:
            *OPTIONAL* Password to be used to transfer the file.
            If not provided password from device object is taken
        :param INT timeout:
            *OPTIONAL* maximum time to upload file to a device.
                    Default is set To 30

     ROBOT USAGE:
        EX 1: ${device-handle} =   Get Handle   resource=r1
              Download File    dev=${device-handle}  local_file=/tmp/file.tgz   remote_file=/tmp/file.tgz

        EX 2:${device-handle} =   Get Handle   resource=r1
                Download File    dev=${device-handle}  local_file=/tmp/file.tgz   remote_file=/tmp/file.tgz
                      . ...       user=user_name     password=pass_word     timeout=${190}     protocal=scp

    returns:True if the file transfer is successful, else Exception is raised.

    """
    result = dev.download(*args, **kwargs)
    if not result:
        raise TobyException('download file failed')
    return result

def get_last_response_status(device):
    """
    Returns the status of last command executed on the device object passed.

    ARGUMENTS:
        [device]
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are to be executed. This can
            be obtained by using the keyword 'Get Handle' and specifying the proper device
            resource (can be r0, h0, etc.)

    ROBOT USAGE:
        ${device-handle} =   Get Handle   resource=r1
        Get last Response Status

    :returns:True/False
    """
    if hasattr(device.current_node.current_controller, 'command_status'):
        return device.current_node.current_controller.command_status
    else:
        return True

