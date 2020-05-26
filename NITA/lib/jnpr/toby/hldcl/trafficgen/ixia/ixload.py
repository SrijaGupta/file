"""
IxLoad module providing abstraction of IxLoad Robot keywords.
"""
import os
import re
import sys
import time
import atexit
import telnetlib
import paramiko
import ruamel.yaml as yaml
import json
import inspect
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.hldcl.trafficgen.trafficgen import TrafficGen
import pexpect
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.hldcl.trafficgen.ixia import IxRestApi as IxRestUtils

class IxLoad(TrafficGen):
    """
    IxLoad emulation class
    """
    def __init__(self, system_data=None, chassis=None, appserver=None):
        """
        IxLoad abstraction layer for HLTAPI

        -- Workflow 1 --
        :param  system_data  *MANDATORY* Dictionary of IxLoad information
          Example:
          system_data =
            system:
              primary:
                appserver: wf-appserver2.englab.juniper.net
                controllers:
                  unknown:
                    domain: englab.juniper.net
                    hostname: wf-ixchassis2
                    mgt-intf-name: mgt0
                    mgt-ip: 10.9.1.107
                    osname: IxOS
                make: ixia
                model: xgs12
                name: wf-ixchassis2
                osname: IxOS

        -- Workflow 2 --
        :param  chassis  *MANDATORY* Name of chassis
        :param  appserver  *MANDATORY* Name of tcl server

        :return: ixload object
        """
        self.port_list = None
        self.handle_to_port_map = None
        self.port_to_handle_map = None
        atexit.register(self.cleanup)
        self.intf_to_port_map = None
        self.interfaces = None
        self.session = None
        self.session_url = None
        self.user_functions = dict()
        self.username, self.password = credentials.get_credentials(os='Ixia')
        self.reconnect = None
        # IxLoad API handle
        self.ixload = None

        environment = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__), "environment.yaml")))
        self.lib_path = environment['ixia-lib-path']

        if system_data:
            system = system_data['system']['primary']
            controller_key = list(system['controllers'].keys())[0]

            kwargs = dict()
            kwargs['host'] = self.hostname = system['name']
            kwargs['hostname'] = self.hostname = system['name']
            kwargs['os'] = system['controllers'][controller_key]['osname']
            super(IxLoad, self).__init__(**kwargs)

            # Set appserver
            if 'appserver' in system:
                self.appserver = system['appserver']
            else:
                raise TobyException("Missing appserver from 'primary' stanza: " + str(system_data), host_obj=self)
            # Specify chassis
            self.chassis = system['controllers'][controller_key]['mgt-ip']
            if 'ixlod-session' in system:
                self.reconnect = system['ixlod-session']

        elif chassis and appserver:
            self.chassis = chassis
            self.appserver = appserver
        else:
            raise TobyException("Missing either system_data (Workflow 1) or chassis/appserver parameters", host_obj=self)

        self.intf_status = None
        self.log(level='info', message="CHASSIS= " + self.chassis)
        self.log(level='info', message="APPSERVER= " + self.appserver)

        self.wait = 1
        self.telnet_handle = None
        self.version = self._get_version()
        self._set_envs()
        current_dir = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        user_module_dir = re.sub(r"jnpr\/toby.*", "jnpr/toby/trafficgen/ixia/ixload", current_dir)
        sys.path.append(user_module_dir)
        file_list = list(filter(lambda x: os.path.isfile(os.path.join(user_module_dir, x)), os.listdir(user_module_dir)))
        for file_name in file_list:
            if file_name.endswith('.py') and not file_name.startswith('__'):
                module = re.sub(r"\.py$", "", file_name)
                obj = __import__(module)
                function_list = [o for o in inspect.getmembers(obj)
                                 if inspect.isfunction(o[1])]
                for function_tuple in function_list:
                    function_name, function = function_tuple
                    if function_name in self.user_functions:
                        raise TobyException("Duplicate functions in user contributed modules", host_obj=self)
                    self.user_functions[function_name] = function
        self.connection = None

    def cleanup(self):
        """
        Destructor to disconnect from IxLoad server
        """
        try:
            if self.session:
                self.log("Deleting session")
                self.ixload.delete_session(self.session)
            if self.ixload:
                self.log("Disconnecting from IxLoad chassis")
                self.ixload.disconnect()
        except Exception:
            pass

    def _get_version(self):
        """
        Get Chassis OS Version of IxLoad TC
        :
        :return: ixia chassisversion
        """
        version = None
        try:
            #Trying to get the ixia version by login to the box using SSH
            ssh_cl = paramiko.client.SSHClient()
            ssh_cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_cl.connect(hostname=self.chassis, username=self.username, password=self.password)
            channel = None
            data = None
            try:
                channel = ssh_cl.invoke_shell(width=160)
                time.sleep(2)
            except:
                transport=ssh_cl.get_transport()
                channel = transport.open_session()
            if channel.recv_ready():
                data = channel.in_buffer.empty()
                try:
                    data = data.decode('utf-8')
                except UnicodeDecodeError:
                    data = data.decode('iso-8859-1')
            ver_re = re.compile(r'IxOS Version.*:\s+(\d+\.\d+\.\d+\.\d+)', re.IGNORECASE)
            banner_out = ""
            command_response = ''
            if data:
                banner_out = str(data)
                ver_search = ver_re.search(banner_out)
                if ver_search:
                    version = ver_search.group(1)
            else:
                self.log(level="INFO", message="Connect response does not have version info: %s" % banner_out)
                channel.exec_command('show ixos active-version')
                time.sleep(2)
                if channel.recv_ready():
                    command_response = channel.recv(1024)
                match = re.search(r'IxOS active version:\s+IxOS\s+(\d+\.\d+\.\d+\.\d+)', command_response.decode('utf-8'), re.IGNORECASE)
                if match:
                    version = match.group(1)
            if ssh_cl:
                ssh_cl.exec_command('exit')
            if version is not None:
                self.log(level="INFO", message="Ixos version: %s \n" % version)
            else:
                self.log(level="INFO", message="Could not get the ixia verion using ssh connection")
                raise TobyException("Could not get the ixia verion using ssh connection to box %s" % self.chassis, host_obj=self)
        except Exception as ex:
            self.log(level="WARN", message="Toby was not able to find version use ssh due to: %s" % ex.__str__())
            self.log(level="INFO", message="Trying telnet for chassis %s" % self.chassis)
            self.telnet_handle = telnetlib.Telnet(self.chassis)
            # self.telnet_handle.set_debuglevel(10)
            self.telnet_handle.read_until(b"Ixia>")
            time.sleep(self.wait)
            cmd = "package require IxTclHal;version cget -ixTclHALVersion\n"
            cmd = cmd.encode('ascii')
            self.telnet_handle.write(cmd)
            match_results = self.telnet_handle.expect([br"\d+\.\d+\.\d+\.\d+"])
            version = match_results[1].group(0).decode('ascii')
            self.telnet_handle.close()
        if not version:
            raise TobyException("Unable to detect Ixia chassis version. Is your Ixia chassis reachable?", host_obj=self)

        self.log(level='info', message='CHASSIS VERSION: ' + version)
        major_minor_version = re.search(r'^\d+\.\d+', version).group(0)

        if not major_minor_version:
            raise TobyException("Unable to derive major and minor version from " + version, host_obj=self)

        if float(major_minor_version) < 8.20:
            raise TobyException("Unsupported version " + major_minor_version + ". Minimum version supported: 8.20", host_obj=self)
        return version

    def _set_envs(self):
        """
        Set PYTHONPATH required for IxLoad
        """

        sys.path.append(self.lib_path)
        # sys.path.append(self.ixload_lib_path + '/RestScripts/Utils')
        self.log(level="info", message="ADDED_TO_PYTHONPATH= " + self.lib_path)
        # self.log(level="info", message="ADDED_TO_PYTHONPATH= " + self.ixload_lib_path + '/RestScripts/Utils')

    def add_interfaces(self, interfaces):
        """
        Get interfaces{} block from yaml to use fv- knobs therein
        """
        self.interfaces = interfaces

    def add_intf_to_port_map(self, intf_to_port_map):
        """
        Add attribute to ixload object which contains
        params intf to port mappings
        """
        self.intf_to_port_map = intf_to_port_map

    def invoke(self, command, **kwargs):
        """
        Pass-through for ixnetwork.py functions
        (ixnetwork.py? or something else?)
        """
        if re.match(r"^http_post", command):
            reply = self.connection.http_post(url=kwargs['url'], data=kwargs['data'])
            return reply
        elif re.match(r"^http_get", command):
            if 'option' in kwargs.keys():
                reply = self.connection.http_get(url=kwargs['url'], option=kwargs['option'])
            else:
                reply = self.connection.http_get(url=kwargs['url'])
            return reply
        elif re.match(r"^http_request", command):
            reply = self.connection.http_request(method=kwargs['method'], url=kwargs['url'])
            return reply
        elif re.match(r"^http_options", command):
            reply = self.connection.http_options(url=kwargs['url'])
            return reply
        elif re.match(r"^http_patch", command):
            reply = self.connection.http_patch(url=kwargs['url'], data=kwargs['data'])
            return reply
        elif re.match(r"^http_delete", command):
            reply = self.connection.http_delete(url=kwargs['url'], data=kwargs['data'])
            return reply
        if command in self.user_functions:
            self.log(level="info", message="Invoking Juniper IXIA Ixload function " + command + " with parameters " + str(kwargs))
            result = self.user_functions[command](self, **kwargs)
            self.log(level="info", message="Invocation of Juniper IXIA Ixload function " + command + " completed with result: " + str(result))
            return result
        if command == 'get_session':
            self.log(level="info", message="Returning IxLoad Session Handle")
            return self.session_url
        self.log(level="info", message="Invoking IxLoad method " + command + " with parameters " + str(kwargs))
        ixload_method = getattr(self.ixload, command)
        result = ixload_method(**kwargs)
        if type(result) is dict and 'status' in result:
            if not result['status']:
                raise TobyException("Invocation of IxLoad method " + command + " failed with result: " + str(result), host_obj=self)
        self.log(level="info", message="Invocation of IxLoad method " + command + " succeeded with result: " + str(result))
        return result

    def reconnect_session(self, session_url):
        '''
        '''
        try:
            reply = self.connection.http_get(url=session_url, option=1)
            #return {"status": 1, "session":reply}
            if reply['isActive'] == True:
                self.session_url = session_url
            else:
                raise TobyException("Ixload session " + session_url + " is not active")
        except Exception as err:
            return {"status":0, "log": err}
        return {"status": 1, "session" : self.session_url}

    def connect(self, port_list, **kwargs):
        """
        Connect to IxLoad chassis
        :return: ixload connection object
        """
        if not port_list:
            raise TobyException("Missing port_list parameter", host_obj=self)
        self.log(level="info", message="Connecting to Ixia IxLoad service on port 8443...")
        bad_connect = self.create_session(gateway_server=self.appserver, gateway_port=8443, ixload_version=self.version)
        # Use bad version to get back error containing proper version and then turn around
        # and use proper version from error to try and create session again
        version_appserver = None
        if not bad_connect['status']:
            version_appserver = re.search(r'Available\s+versions\s+.+(\d+\.\d+\.\d+\.\d+)', str(bad_connect['log']), re.I).group(1)
            self.log(level='INFO', message="Available Version {}".format(version_appserver))
        else:
            raise TobyException("Unable to detect ixload version", host_obj=self)
        if version_appserver is None:
            raise TobyException("Could Not get the Version from Ixload Appserver")
        major_minor_version = re.search(r'^\d+\.\d+', self.version).group(0)
        if major_minor_version not in version_appserver:
            raise TobyException("Version miss match with Chassis {} and Appserver {}".format(self.version, version_appserver))
        # Trying for right connection
        self.log(level='INFO', message="Reconect data {}".format(self.reconnect))
        result = self.create_session(gateway_server=self.appserver, gateway_port=8443, ixload_version=version_appserver)
        if not result['status']:
            raise TobyException("Invocation of IxLoad connect() failed with result: " + str(result), host_obj=self)
        else:
            self.log(level="info", message="IxLoad Session Started" + str(result))
            return result['session']

    def create_session(self, gateway_server, gateway_port, ixload_version):
        '''
            This method is used to create a new session. It will return the url of the newly created session
            Args:
            - ixload_version this is the actual IxLoad Version to start
        '''
        try:
            self.connection = IxRestUtils.get_connection(gateway_server, gateway_port)
            session_url = "sessions"
            data = {"ixLoadVersion": ixload_version}
            data = json.dumps(data)
            reply = self.connection.http_post(url=session_url, data=data)
            if not reply.ok:
                raise Exception(reply.text)
            try:
                new_obj_path = reply.headers['location']
            except:
                raise Exception("Location header is not present. Please check if the action was created successfully.")
            if self.reconnect is not None:
                self.log(level="info", message="reconnecting to Ixload...")
                bad_connect = self.reconnect_session(self.reconnect)
                return bad_connect
            else:
                session_id = new_obj_path.split('/')[-1]
                self.session_url = "%s/%s" % (session_url, session_id)
                start_session_url = "%s/operations/start" % (self.session_url)
                reply = self.connection.http_post(url=start_session_url, data={})
                if not reply.ok:
                    raise Exception(reply.text)
                action_result_url = reply.headers.get('location')
                if action_result_url:
                    action_result_url = self.strip_api_and_version_from_url(action_result_url)
                    action_finished = False
                    while not action_finished:
                        action_status_obj = self.connection.http_get(url=action_result_url)
                        if action_status_obj.state == 'finished':
                            if action_status_obj.status == 'Successful':
                                action_finished = True
                            else:
                                error_msg = "Error while executing action '%s'." % start_session_url
                                if action_status_obj.status == 'Error':
                                    error_msg += action_status_obj.error
                                self.log(error_msg)
                                raise Exception(error_msg)
                        else:
                            time.sleep(0.1)
        except Exception as err:
            return {"status": 0, "log": err}
        return {"status": 1, "session" : self.session_url}

    def strip_api_and_version_from_url(self, url):
        '''
        #remove the slash (if any) at the beginning of the url
        '''
        if url[0] == '/':
            url = url[1:]
        url_elements = url.split('/')
        if 'api' in url:
            #strip the api/v0 part of the url
            url_elements = url_elements[2:]
        return '/'.join(url_elements)

    def get_port_handle(self, intf):
        """
        Use IxLoad object information to get port handle keys
        """
        intf = intf.lower()
        if intf in self.intf_to_port_map.keys():
            port = self.intf_to_port_map[intf]
            if port in self.port_to_handle_map.keys():
                return self.port_to_handle_map[port]
        else:
            raise TobyException("No such params interface " + intf, host_obj=self)

def invoke(device, function, **kwargs):
    """
    Pass-through function for IxLoad method of same name to call sth.py functions
    """
    return device.invoke(function, **kwargs)

