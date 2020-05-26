"""
Avalanche module providing abstracting to av.py function within Avalanche.
"""
import os
import sys
import six
import re
import time
import atexit
import telnetlib
import ruamel.yaml as yaml
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.hldcl.trafficgen.trafficgen import TrafficGen
from jnpr.toby.hldcl.connectors.sshconn import SshConn
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.exception.toby_exception import TobyException

class Avalanche(TrafficGen):
    """
    Avalanche emulation class
    """
    def __init__(self, chassis=None, system_data=None, avalanche_tcl_bin=None, avalanche_lib_path=None, avalanche_threats=None, avalanche_jre_path=None ):
        """
        Avalanche abstraction layer for HLTAPI

        -- Workflow 1 --
        :param  system_data:  *MANDATORY* Dictionary of Avalanche information
          rt0:
            interfaces:
              intf1:
                name: 1/8
              intf2:
                name: 1/9
            system:
              primary:
                appserver: wf-appserver2.englab.juniper.net
                controllers:
                  unknown:
                    domain: englab.juniper.net
                    hostname: wf-avchassis2
                    mgt-intf-name: mgt0
                    mgt-ip: 10.9.1.107
                    osname: IxOS
                make: avalanche
                model: xgs12
                name: wf-ixchassis2
                osname: IxOS

        -- Workflow 2 --
        :param  host  *MANDATORY* FQDN/mgt-ip of of chassis


        :return: Avalanche object
        """
        self.chassis = None
        self.interfaces = None
        self.model = 'Unknown'
        self.platform_type = 'STC'
        self.intf_to_port_map = dict()
        self.port_to_handle_map = dict()
        self.session_info = None
        self.handle_to_port_map = None
        self.login_complete = False

        #self.tcl = '/volume/systest-proj/apptest/local/ActiveTcl-8.4/bin/tclsh'
        #self.tcl = '/volume/systest-proj/apptest/local/bin/tclsh8.6'
        self.log_dir = get_log_dir()
        self.clientport = None
        self.serverport = None
        atexit.register(self.cleanup)
        self.username, self.password = credentials.get_credentials(os='Spirent')

        if avalanche_lib_path and avalanche_tcl_bin and avalanche_jre_path and avalanche_threats:
            self.lib_path = avalanche_lib_path
            self.tcl_bin = avalanche_tcl_bin
            self.jre_path = avalanche_jre_path
            self.threat_path = avalanche_threats
        else:
            environment = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__), "environment.yaml")))
            self.lib_path = environment['avalanche-lib-path']
            self.tcl_bin = environment['avalanche-tcl-bin']
            self.jre_path = environment['avalanche-jre-path']
            self.threat_path = environment['avalanche-threats']

        self.api_path = self.lib_path + '/Avalanche/PythonAPI/1.0.0'

        if system_data:

            controller_key = list(system_data['system']['primary']['controllers'].keys())[0]

            if system_data['system']['primary']['controllers'][controller_key]['user']:
                self.username = system_data['system']['primary']['controllers'][controller_key]['user']
            if system_data['system']['primary']['controllers'][controller_key]['password']:
                self.password = system_data['system']['primary']['controllers'][controller_key]['password']

            kwargs = dict()
            kwargs['host'] = self.chassis = system_data['system']['primary']['name']
            kwargs['hostname'] = self.chassis = system_data['system']['primary']['name']
            kwargs['os'] = system_data['system']['primary']['controllers'][controller_key]['osname']
            kwargs['user'] = self.username
            kwargs['password'] = self.password
            super(Avalanche, self).__init__(**kwargs)

            if 'api-path' in system_data['system']['primary']:
                self.log("Overriding existing av.py path with: " + system_data['system']['primary']['api-path'])
                self.api_path = system_data['system']['primary']['api-path']
            if 'mgt-ip' in system_data['system']['primary']['controllers'][controller_key]:
                self.chassis = system_data['system']['primary']['controllers'][controller_key]['mgt-ip']
            self.model = system_data['system']['primary']['model'].upper()
            match = re.search(r'(^C100$|3100|^C100U$)', self.model, re.I)

            if match and not (system_data['system']['primary']['controllers'][controller_key]['user'] \
                and system_data['system']['primary']['controllers'][controller_key]['password']):
                if match.group(1) == 'C100' or match.group(1) == 'C100U':
                    self.log("Model %s, so Overriding username and password" % match.group(1))
                    self.username = 'root'
                    self.password = 'welcome'
                    self.log("Login:" + self.username + ", Password:" + self.password)
                elif match.group(1) == '3100':
                    self.log("Model 3100, so Overriding username and password")
                    self.username = 'root'
                    self.password = ''
                    self.log("Login:" + self.username + ", Password:" + self.password)
                if 'license-path' in system_data['system']['primary']:
                    os.environ['SPIRENT_TCLAPI_LICENSEROOT'] = system_data['system']['primary']['license-path']
                else:
                    raise TobyException("ERROR: Must include fv-avalanche-license-path for models starting with C100", host_obj=self)
                self.platform_type = self.model

        elif chassis:
            self.chassis = chassis
        else:
            raise TobyException("Missing either system_data (Workflow 1) or chassis (Workflow 2) parameter")

        if not self.chassis:
            raise TobyException("Unable to determine chassis host information! Check for valid in init yaml file.", host_obj=self)

        self.connect_info = None
        self.log("CHASSIS= " + str(self.chassis))

        self.wait = 1
        self.telnet_handle = None
        self.version = self._get_version()
        self._set_envs()
        sys.path.append(self.api_path)
        self.log("API PATH= " + self.api_path)
        executable = sys.argv[0]
        sys.argv[0] = self.log_dir
        try:
            self.av = __import__('av') # pylint: disable=invalid-name
        except Exception as err:
            raise TobyException("Unable to import 'av' at path " + self.api_path + ": " + str(err), host_obj=self)
        sys.argv[0] = executable

        self.av.new(CHASSIS=self.chassis, TYPE=self.platform_type)

    def cleanup(self):
        """
        Logout from Avalanche device
        """
        if self.login_complete:
            self.av.logout_test()

    def _get_version(self):
        """
        Get Chassis OS Version of Avalanche TC
        :
        :return: avalanche TC version
        """

        version = None
        try:
            if self.model == 'C100':
                raise TobyException("Default to ssh for C100", host_obj=self)
            self.telnet_handle = telnetlib.Telnet(self.chassis)
#            self.telnet_handle.set_debuglevel(10)
#           self.telnet_handle.write(b"\n")
            time.sleep(self.wait)
            time.sleep(self.wait)
            self.telnet_handle.read_until(b'login: ')
            uname = self.username + "\n"
            uname = uname.encode('ascii')
            self.telnet_handle.write(uname)
            time.sleep(self.wait)
            self.telnet_handle.read_until(b"Password: ")
            pwd = self.password + "\n"
            pwd = pwd.encode('ascii')
            self.telnet_handle.write(pwd)
            time.sleep(self.wait)
            time.sleep(self.wait)
            self.telnet_handle.read_until(b"admin>")
            cmd = "version\n"
            cmd = cmd.encode('ascii')
            self.telnet_handle.write(cmd)
            time.sleep(self.wait)
            match_results = self.telnet_handle.expect([br"\d+.\d+"])
            full_version = match_results[1].group(0).decode('ascii')
            version = full_version
            ver_re = re.compile(r'\d.\d\d+')
            if ver_re.search(full_version):
                version = ver_re.search(full_version).group()
        except Exception as ex: # pylint: disable=bare-except
            #if telnet isn't listening, try ssh
            self.log(level="WARN", message="Unable to detect Avalanche Chassis version use telnet due to: %s" % ex.__str__())
            try:
                ssh_handle = SshConn(host=self.chassis, user=self.username, password=self.password)
                paramiko_handle = ssh_handle.client
                if self.model == 'C100' or re.search('3100', self.model , re.I):
                    paramiko_handle.send('/swat/bin/wawr -#\n')
                else:
                    paramiko_handle.send('version\n')
                time.sleep(self.wait)
                response = paramiko_handle.recv(1024)
                ver_re = re.compile(r'\d.\d\d+')
                if ver_re.search(str(response)):
                    version = ver_re.search(str(response)).group()
                else:
                    version = '4.58'
            except Exception as ex:
                self.log(level="ERROR", message="Unable to detect Avalanche Chassis version using ssh connection due to: %s" % ex.__str__())

        if not version:
            raise TobyException("Unable to detect Avalanche Chassis version", host_obj=self)

        return version

    def _set_envs(self):
        """
        Set ENVs required for Avalanche Tester
        """
        if self.version is None:
            self._get_version()

        os.environ['SPIRENT_TCLAPI_ROOT'] = self.lib_path + "/Spirent_TestCenter_" + \
                                            self.version + "/Layer_4_7_Application_Linux/TclAPI"
        os.environ['SPIRENT_DATA_LOCATION'] = self.log_dir + '/avalanche'
        os.environ['STC_TCL'] = self.tcl_bin
        os.environ['STC_INSTALL_DIR'] = self.lib_path + "/Spirent_TestCenter_" + \
                                        self.version + "/Spirent_TestCenter_Application_Linux"
        os.environ['JAVA_HOME'] = self.jre_path
#        os.environ['LD_LIBRARY_PATH'] = "/volume/systest-proj/apptest/local/ActiveTcl-8.4/lib"
#        os.environ['TCLLIBPATH'] = self.lib_path + '/Avalanche/PythonAPI/tcl8.5_lib_dependencies'
        os.environ['SPIRENT_TCLAPI_THREATDB'] = self.threat_path

        self.log("API PATH= " + self.lib_path + '/Avalanche/PythonAPI/1.0.0')

#        self.log("TCLLIPATH= " + os.environ['TCLLIBPATH'])
        self.log("SPIRENT_TCLAPI_ROOT= " + os.environ['SPIRENT_TCLAPI_ROOT'])
        self.log("SPIRENT_DATA_LOCATION= " + os.environ['SPIRENT_DATA_LOCATION'])
        self.log("STC_TCL= " + os.environ['STC_TCL'])
        self.log("STC_INSTALL_DIR= " + os.environ['STC_INSTALL_DIR'])
        self.log("JAVA_HOME= " + os.environ['JAVA_HOME'])
        self.log("SPIRENT_TCLAPI_THREATDB= " + os.environ['SPIRENT_TCLAPI_THREATDB'])


    def add_interfaces(self, interfaces):
        """
        Get interfaces{} block from yaml to use fv- knobs therein
        """
        self.interfaces = interfaces

    def add_intf_to_port_map(self, intf_to_port_map):
        """
        Assign params intf to port map to obj
        """
        self.intf_to_port_map = intf_to_port_map

    def invoke(self, function, **args):
        """
        Pass-through for av.py functions
        """
        if 'port_handle' in args.keys():
            port_handle = args['port_handle']
            if isinstance(port_handle, six.string_types):
                port_handle = port_handle.split(' ')
            if port_handle[0] in self.intf_to_port_map.keys():
                new_port_handle = list()
                for intf in port_handle:
                    new_port_handle.append(self.port_to_handle_map[self.intf_to_port_map[intf]])
                args['port_handle'] = ' '.join(new_port_handle)

        avalanche_func = getattr(self.av, function)
        self.log("Invoking Avalanche API " + function + " with the following parameters: " + str(args))
        result = avalanche_func(**args)
        self.log("Invocation of Avalanche method " + function + " executed resulting in: " + str(result))

        if function != 'invoke':
            if not result:
                raise TobyException("Invocation of Avalanche method " + function + " failed with result: " + str(result), host_obj=self)
        self.log("Invocation of Avalanche method " + function + " succeeded")
        return result

    def connect(self, **args): # pylint: disable=unused-argument
        """
        Connect to Avalanche chassis and assign port handle keys using av.connect
        """
        clientports = []
        serverports = []
        for intf in self.interfaces:
            if 'avalanche-port-role' in self.interfaces[intf] and self.interfaces[intf]['avalanche-port-role'] == 'client':
                clientports.append(self.interfaces[intf]['pic'])
            elif 'avalanche-port-role' in self.interfaces[intf] and self.interfaces[intf]['avalanche-port-role'] == 'server':
                serverports.append(self.interfaces[intf]['pic'])
        self.log("CLIENT PORTS: " + str(clientports) + "    SERVER PORTS: " + str(serverports))

        self.log("Attempting connection to Avalanche (init_modules)")
        if not len(clientports) or not len(serverports):
            raise TobyException('Missing client and server port designations. ' + \
                                '(set fv-avalanche-port-role to "client" or "server" in interface block)', host_obj=self)

        try:
            if self.av.init_modules(CLIENTPORT=clientports, SERVERPORT=serverports):
                if self.model == 'C100' or re.search('3100', self.model , re.I):
                    self.av.activateLicense()
                self.log("Avalanche Initialization Complete")
                self.login_complete = True
            else:
                raise TobyException("Avalanche Initialization Failed", host_obj=self)
        except Exception as err:
            raise TobyException("Avalanche Initialization Failed with ERROR: " + str(err), host_obj=self)



    def get_port_handle(self, **args):
        """
        Use Avalanche object information to get port handle keys
        """
        intf = None
        if 'intf' in args.keys():
            intf = args['intf'].lower()
            if intf in self.intf_to_port_map.keys():
                port = self.intf_to_port_map[intf]
                if port in self.port_to_handle_map.keys():
                    return self.port_to_handle_map[port]
            else:
                raise TobyException("No such port " + intf, host_obj=self)


def invoke(device, function, **kwargs):
    """
    Pass-through function for Avalanche method of same name to call av.py functions
    """
    if function == 'connect':
        return device.connect(**kwargs)
    elif function == 'get_port_handle':
        return device.get_port_handle(**kwargs)
    else:
        return device.invoke(function, **kwargs)
