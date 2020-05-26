"""
Spirent module providing abstracting to sth.py function within Spirent.
"""
import os
import sys
import six
import re
import time
import atexit
import telnetlib
import inspect
import socket
import subprocess
import random
# for some reason, pylint complains about importing the following two modules
import ipaddress #pylint: disable=import-error
import ruamel.yaml as yaml #pylint: disable=import-error
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.hldcl.trafficgen.trafficgen import TrafficGen
from jnpr.toby.hldcl.connectors.sshconn import SshConn
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.exception.toby_exception import TobyException, SpirentConnectError, SpirentLicenseError, TobySpirentLabserverConnectException, TobySpirentChassisConnectException, TobySpirentException



class Spirent(TrafficGen):
    """
    Spirent emulation class
    """
    def __init__(self, chassis=None, license_server=None, system_data=None, spirent_lib_path=None, spirent_tcl_bin=None):
        """
        Spirent abstraction layer for HLTAPI

        -- Workflow 1 --
        :param  system_data:  *MANDATORY* Dictionary of Spirent information
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
                    hostname: wf-ixchassis2
                    mgt-intf-name: mgt0
                    mgt-ip: 10.9.1.107
                    osname: IxOS
                license_server: sv8-pod1-ixlic1.englab.juniper.net
                make: spirent
                model: xgs12
                name: wf-ixchassis2
                osname: IxOS

        -- Workflow 2 --
        :param  host  *MANDATORY* FQDN/mgt-ip of of chassis
        :param  labserver  *OPTIONAL* FQDN/mgt-ip of of lab server
        :param  license_server *OPTIONAL* FQDN/mgt-ip of license server


        :return: Spirent object
        """

        self.debug = False
        self.virtual = False
        self.port_list = None
        self.port_order = None
        self.license_server = None
        self.chassis = None
        self.labserver = None
        self.labserver_session_name = 'toby' + str(random.randrange(1000, 9999, 1))
        self.labserver_preserve_session = False
        self.labserver_create_new_session = 1
        self.is_labserver_connected = False
        self.intf_to_port_map = None
        self.port_to_handle_map = None
        self.session_info = None
        self.config_file = None
        self.handle_to_port_map = None
        self.log_dir = get_log_dir()
        atexit.register(self.cleanup)
        self.sth = None
        self.user_functions = dict()
        self.username, self.password = credentials.get_credentials(os='Spirent')
        self.read_timeout = 60
        self.tcl = None
        self.tcl32 = None
        self.tcl64 = None

        if spirent_lib_path and spirent_tcl_bin:
            self.lib_path = spirent_lib_path
            self.tcl = spirent_tcl_bin
        else:
            environment = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__), "environment.yaml")))
            self.lib_path = environment['spirent-lib-path']
            self.tcl32 = environment['tcl32-bin']
            self.tcl64 = environment['tcl64-bin']

        if system_data:
            controller_key = list(system_data['system']['primary']['controllers'].keys())[0]

            if 'user' in system_data['system']['primary']['controllers'][controller_key] and \
                system_data['system']['primary']['controllers'][controller_key]['user']:
                self.username = system_data['system']['primary']['controllers'][controller_key]['user']
            if 'password' in system_data['system']['primary']['controllers'][controller_key] and \
                system_data['system']['primary']['controllers'][controller_key]['password']:
                self.password = system_data['system']['primary']['controllers'][controller_key]['password']

            kwargs = dict()
            kwargs['host'] = self.chassis = system_data['system']['primary']['name']
            kwargs['hostname'] = self.chassis = system_data['system']['primary']['name']
            kwargs['os'] = system_data['system']['primary']['controllers'][controller_key]['osname']
            kwargs['user'] = self.username
            kwargs['password'] = self.password
            super(Spirent, self).__init__(**kwargs)

            if 'labserver' in system_data['system']['primary']:
                self.labserver = system_data['system']['primary']['labserver']
                try:
                    ipaddress.ip_address(self.labserver)
                except Exception:
                    self.labserver = socket.gethostbyname(self.labserver)
                if 'labserver_session_name' in system_data['system']['primary']:
                    self.labserver_session_name = system_data['system']['primary']['labserver_session_name']
                    if 'labserver_connect_existing_session' in system_data['system']['primary']:
                        self.labserver_create_new_session = 0
                if 'labserver_preserve_session' in system_data['system']['primary']:
                    self.log("Preserving labserver session")
                    self.labserver_preserve_session = True
            if 'config-file' in system_data['system']['primary']:
                self.config_file = str(system_data['system']['primary']['config-file'])
            if 'port-order' in system_data['system']['primary']:
                self.port_order = system_data['system']['primary']['port-order']
            if 'debug' in system_data['system']['primary']:
                self.debug = system_data['system']['primary']['debug']
            if 'mgt-ip' in system_data['system']['primary']['controllers'][controller_key]:
                self.chassis = system_data['system']['primary']['controllers'][controller_key]['mgt-ip']

            if system_data['system']['primary']['model'].upper() == 'VSPIRENT':
                self.virtual = True
                try:
                    self.license_server = system_data['system']['primary']['license_server']
                except:
                    raise TobyException("Missing license_server 'primary' stanza: " + str(system_data), host_obj=self)

        elif chassis:
            self.chassis = chassis
            if license_server:
                self.license_server = license_server
        else:
            raise TobyException("Missing either system_data (Workflow 1) or chassis (Workflow 2) parameter", host_obj=self)

        if not self.chassis:
            raise TobyException("Unable to determine chassis host information! Check for valid labserver or mgt-ip in init yaml file.", host_obj=self)

        self.connect_info = None
        self.log("CHASSIS= " + str(self.chassis))

        self.wait = 1
        self.telnet_handle = None
        self.version = self._get_version()
        self.hltapi_lib_path = None

        if 'hltapi-path' in system_data['system']['primary']:
            self.hltapi_lib_path = system_data['system']['primary']['hltapi-path']
            self.hltapi_lib_path.rstrip('/')
        else:
            hltapi_version = self._get_hltapi_version()
            self.hltapi_lib_path = self.lib_path + '/HLTAPI/' + hltapi_version

        sys.path.append(self.hltapi_lib_path + '/SourceCode/hltapiForPython')

        self._set_envs()
        #resetting sys.argv[0] is only way to get spirent htlapi logs to go to the right place
        executable = sys.argv[0]
        sys.argv[0] = self.log_dir
        self.sth = __import__('sth')
        sys.argv[0] = executable
        self.log("Spirent Chassis Initialization Complete")

        # Import extended spirent modules with functions from jnpr/toby/trafficgen/spirent
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        user_module_dir = re.sub(r"jnpr\/toby.*", "jnpr/toby/trafficgen/spirent", current_dir)
        sys.path.append(user_module_dir)
        file_list = list(filter(lambda x: os.path.isfile(os.path.join(user_module_dir, x)), os.listdir(user_module_dir)))
        for file_name in file_list:
            if file_name.endswith('.py') and not file_name.startswith('__'):
                module = re.sub(r"\.py$", "", file_name)
                obj = __import__(module)
                function_list = [o for o in inspect.getmembers(obj) if inspect.isfunction(o[1])]
                for function_tuple in function_list:
                    function_name, function = function_tuple
                    if function_name in self.user_functions:
                        raise TobyException("Duplicate functions in user contributed modules", host_obj=self)
                    self.user_functions[function_name] = function

    def cleanup(self):
        """
        Destructor to disconnect from labserver
        """
        if self.sth:
            if self.labserver:
                if self.labserver_preserve_session:
                    self.log("Disconnecting from labserver, but preserving labserver session")
                    self.sth.labserver_disconnect(terminate_session=0)
                else:
                    self.log("Disconnecting from labserver, and destroying labserver session")
                    self.sth.labserver_disconnect(terminate_session=1)
            elif self.handle_to_port_map:
                self.sth.cleanup_session(clean_dbfile=0, port_handle=list(self.handle_to_port_map.keys()))

    def _get_version(self):
        """
        Get Chassis OS Version of Spirent TC
        :
        :return: spirent TC version
        """
        version = None
        try:
            self.telnet_handle = telnetlib.Telnet(self.chassis)
#           self.telnet_handle.set_debuglevel(10)
#           self.telnet_handle.write(b"\n")
            time.sleep(self.wait)
            self.telnet_handle.read_until(b'login: ', timeout=self.read_timeout)
            uname = self.username + "\n"
            uname = uname.encode('ascii')
            self.telnet_handle.write(uname)
            time.sleep(self.wait)
            self.telnet_handle.read_until(b"Password: ", timeout=self.read_timeout)
            pwd = self.password + "\n"
            pwd = pwd.encode('ascii')
            self.telnet_handle.write(pwd)
            time.sleep(self.wait)
            time.sleep(self.wait)
            self.telnet_handle.read_until(b"admin>", timeout=self.read_timeout)
            cmd = "version\n"
            cmd = cmd.encode('ascii')
            self.telnet_handle.write(cmd)
            time.sleep(self.wait)
            match_results = self.telnet_handle.expect([br"\d+.\d+"], timeout=self.read_timeout)
            full_version = match_results[1].group(0).decode('ascii')
            version = full_version
            ver_re = re.compile(r'\d.\d\d+')
            if ver_re.search(full_version):
                version = ver_re.search(full_version).group()
        except Exception as ex:
            self.log(level="WARN", message="Toby was not able to find version use telnet due to: %s" % ex.__str__())
            #if telnet isn't listening, try ssh
            try:
                ssh_handle = SshConn(host=self.chassis, user=self.username, password=self.password)
                paramiko_handle = ssh_handle.client
                paramiko_handle.send('version\n')
                time.sleep(self.wait)
                response = paramiko_handle.recv(1024)
                ver_re = re.compile(r'\d.\d\d+')
                if ver_re.search(str(response)):
                    version = ver_re.search(str(response)).group()
            except Exception as ex:
                self.log(level="ERROR", message="Toby was not able to find version info using ssh connection due to: %s" % ex.__str__())

        if not version:
            if not check_device_reachability(self, self.chassis):
                raise SpirentConnectError("Spirent chassis is not pingable")
            elif not check_port_status(self, self.chassis, 23, 5, "telnet"):
                raise SpirentConnectError("Spirent telnet port is down")
            elif not check_port_status(self, self.chassis, 22, 5, "SSH"):
                raise SpirentConnectError("Spirent ssh port is down")
            else:
                raise TobyException("Unable to detect Spirent Chassis version", host_obj=self)

        self.log('CHASSIS VERSION: ' + version)
        return version

    def _set_envs(self):
        """
        Set ENVs required for Spirent TC
        """

        if self.version is None:
            self._get_version()

        os.environ['STC_VERSION'] = self.version
        os.environ['TCLLIBPATH'] = self.hltapi_lib_path + "/SourceCode " + \
                                   self.lib_path + "/Spirent_TestCenter_" + self.version + "/Spirent_TestCenter_Application_Linux"
        if self.tcl is None:
            so_file = self.lib_path + "/Spirent_TestCenter_" + self.version + "/Spirent_TestCenter_Application_Linux/TestCenterSession"
            returned_value = os.popen("file %s" % so_file).read()
            self.log("Linux file command on %s returned: %s" %(so_file, returned_value))
            if re.search(r'32-bit', returned_value, re.I) or re.search(r'(cannot open|No such file or directory)', returned_value, re.I):
                os.environ['LD_LIBRARY_PATH'] = self.lib_path + "/ActiveTcl-8.4/lib"
                self.tcl = self.tcl32
                self.log('STC Linux application being used is 32-bit')
            else:
                self.tcl = self.tcl64
                os.environ['LD_LIBRARY_PATH'] = self.tcl64.replace('/bin/tclsh', '/lib')
                self.log('STC Linux application being used is 64-bit')
        os.environ['STC_TCL'] = self.tcl
        os.environ['STC_INSTALL_DIR'] = self.lib_path + "/Spirent_TestCenter_" + \
                                        self.version + "/Spirent_TestCenter_Application_Linux"
        os.environ['HLPYAPI_LOG'] = self.log_dir + "/spirent"
        os.environ['STC_LOG_OUTPUT_DIRECTORY'] = self.log_dir + "/spirent"

        self.log("STC_VERSION= " + self.version)
        self.log("TCLLIBPATH= " + os.environ['TCLLIBPATH'])
        self.log("STC_TCL= " + os.environ['STC_TCL'])
        self.log("STC_INSTALL_DIR= " + os.environ['STC_INSTALL_DIR'])
        self.log("LD_LIBRARY_PATH= " + os.environ['LD_LIBRARY_PATH'])

    def _get_hltapi_version(self):
        """
        Needed to determine which hltapi sth.py to import
        After finding version of stc, then walk backwards until hltapi ver available
        """
        sth_vers = sorted(os.listdir(self.lib_path + "/HLTAPI"), reverse=True)
        hltapi_version = "4.62"
        for sth_ver in sth_vers:
            hltapi_version = sth_ver
            break
        self.log("HLTAPI_VERSION= " + hltapi_version)
        return hltapi_version

    def add_intf_to_port_map(self, intf_to_port_map):
        """
        Assign params intf to port map to obj
        """
        self.intf_to_port_map = intf_to_port_map

    def invoke(self, function, from_spirent_robot=False, **args):
        """
        Pass-through for sth.py functions
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

        if from_spirent_robot:
            function = function.lower()
            function = function.replace(' ', '_')
            self.log("WARN", "spirent.robot will be removed on Apr 30th.  Please use...\n " \
                             "Execute Tester Command    ${rt_handle}    command=" + function + "    <args>")

        # User contributed module
        if function in self.user_functions:
            self.log("Invoking Juniper Spirent function " + function + " with parameters " + str(args))
            result = self.user_functions[function](self, **args)
            self.log("Invocation of Juniper Spirent function " + function + " completed with result: " + str(result))
            return result

        spirent_func = getattr(self.sth, function)
        self.log("Spirent Invoke Parameters: " + str(args))
        result = spirent_func(**args)
        self.log("Invocation of Spirent method " + function + " resulting in: " + str(result))

        if function != 'invoke':
            if not result:
                spirent_diagnostics(self)
                raise TobySpirentException("Invocation of Spirent method " + function + " failed with no result" , host_obj=self)
            if result['status'] == '0':
                spirent_diagnostics(self)
                raise TobySpirentException("Invocation of Spirent method " + function + " failed with result: " + str(result), host_obj=self)
        self.log("Invocation of Spirent method " + function + " succeeded")
        return result

    def connect(self, port_list):
        """
        Connect to Spirent chassis and assign port handle keys using sth.connect
        """
        #reorder port list if required - useful when config_file is being loaded and ports need to pair up exactly
        if self.port_order:
            duplicate_port_check = {}
            new_port_list = []
            interfaces = self.port_order.split(':')
            for intf in interfaces:
                if intf in duplicate_port_check:
                    raise TobyException("duplicate port " + intf + " found in port_list [fv-spirent-port-list]", host_obj=self)
                if intf in self.intf_to_port_map:
                    new_port_list.append(self.intf_to_port_map[intf])
                    duplicate_port_check[intf] = 1
                else:
                    raise TobyException("Spirent Port " + intf + " specified in ordered port list does not exist", host_obj=self)
            if len(port_list) != len(new_port_list):
                raise TobyException("Spirent port ordered list [fv-spirent-port-list] does not match number of interfaces present", host_obj=self)
            self.port_list = new_port_list
        else:
            self.port_list = port_list

        if self.debug:
            os.makedirs(name=self.log_dir + '/spirent', exist_ok=True)
            self.sth.test_config(custom_path=self.log_dir + '/spirent', log=1, logfile='spirent_logfile', vendorlog=1, \
            vendorlogfile='spirent_vendor_logfile', hltlog=1, hltlogfile='spirent_hlt_logfile', hlt2stcmapping=1, \
            hlt2stcmappingfile='spirent_hlt2stcmap_logfile')

        labserver_init = None
        if self.labserver and not self.is_labserver_connected:
            user = 'Unknown'
            if os.environ['USER']:
                user = os.environ['USER']
            labserver_init = self.sth.labserver_connect(server_ip=self.labserver, create_new_session=self.labserver_create_new_session, \
                             session_name=self.labserver_session_name, user_name=user)

            if labserver_init['status'] != '1':
                if not check_device_reachability(self, self.labserver):
                    raise TobySpirentLabserverConnectException("Spirent labserver %s is not pingable" % self.labserver)
                elif not check_port_status(self, self.labserver, 40006, 5, "labserver"):
                    raise TobySpirentLabserverConnectException("Spirent labserver port is down")
                else:
                    spirent_diagnostics(self)
                    raise TobySpirentLabserverConnectException("Not able to connect to Spirent Labserver " + str(labserver_init), host_obj=self)
            else:
                self.log("CONNECT RESULT: " + str(labserver_init))
                self.is_labserver_connected = True
        if self.config_file is not None:
            # load the STC configuration
            self.sth.load_xml(filename=self.config_file)
            config_port_list = self.sth.invoke('stc::get project1 -children-port').strip().split()
            if len(self.port_list) != len(config_port_list):
                spirent_diagnostics(self)
                raise TobySpirentException("Number of ports defined in params file are matched with ports defined in config file", host_obj=self)

        # connect to chassis - not necessary if connecting to existing labserver session
        if self.labserver_create_new_session or not self.labserver:
            if self.license_server:
                if float(self.version) > 4.51:
                    self.log("Licensing vSpirent with license server " + self.license_server)
                    stale_license_server_list = self.sth.invoke('stc::get system1.licenseservermanager -children-licenseserver')
                    for license_server_stale in stale_license_server_list.split():
                            self.sth.invoke("stc::get " + license_server_stale)
                            license_server_ip = self.sth.invoke("stc::get " + license_server_stale + " -Server")
                            if license_server_ip == self.license_server:
                                pass
                            else:
                                self.sth.invoke("stc::delete " + license_server_stale)
                    license_server_manager = self.sth.invoke('stc::get system1 -children-licenseservermanager')
                    lic_result = self.sth.invoke("stc::create licenseserver -under " + license_server_manager + " -server " + self.license_server)
                    self.log("Results from attempt to license vSpirent: " + str(lic_result))

            self.log("Attempting connection to Spirent using ports " + str(self.port_list))
            connect_info = self.sth.connect(device=self.chassis, break_locks=1, offline=0, port_list=self.port_list)
            if connect_info['status'] != '1':
                if not check_device_reachability(self, self.chassis):
                    raise TobySpirentChassisConnectException("Spirent chassis is not pingable")
                if not check_port_status(self, self.chassis, 40004, 5, "chassis_connect"):
                    raise TobySpirentChassisConnectException("Spirent chassis connect port is down")
                if re.search(r'license', connect_info['log'], re.IGNORECASE):
                    spirent_diagnostics(self)
                    raise SpirentLicenseError("Spirent License Error " +str(connect_info), host_obj=self)
                else:
                    spirent_diagnostics(self)
                    raise SpirentConnectError("Failed to connect to Spirent " + str(connect_info), host_obj=self)
            else:
                self.log("CONNECT RESULT: " + str(connect_info))

            self.port_to_handle_map = dict()
            self.handle_to_port_map = dict()
            for port in connect_info['port_handle'][self.chassis].keys():
                self.port_to_handle_map[port] = connect_info['port_handle'][self.chassis][port]
                self.handle_to_port_map[self.port_to_handle_map[port]] = port

            self.session_info = connect_info
            return connect_info

        # connecting to existing labserver session
        else:
            #check to see if ports are the same as yaml content.  Otherwise, abort
            self.port_to_handle_map = dict()
            self.handle_to_port_map = dict()
            port_handles = self.sth.invoke("stc::get project1 -children-port").split()
            for port_handle in port_handles:
                port_and_ip = self.sth.invoke("stc::get " + port_handle + " -location")
                self.log("Raw port handle location :" + port_and_ip)
                port_re = re.compile(r'\d+\/\d+$')
                if port_re.search(port_and_ip):
                    port = port_re.search(port_and_ip).group()
                    if port not in self.port_list:
                        raise TobyException("Existing labserver session port " + port + " not found in spirent params ports '" + \
                                        self.port_list + "'\n" + \
                                        "Remove fv-spirent-labserver-connect-existing-session from params/yaml content", host_obj=self)
                    else:
                        self.port_to_handle_map[port] = port_handle
                        self.handle_to_port_map[port_handle] = port
            self.log("Port to Handle Map: " + str(self.port_to_handle_map))
            self.log("Handle to Port Map: " + str(self.handle_to_port_map))
            self.log("Port Handles: " + str(port_handles))
            return labserver_init

    def get_port_handle(self, **args):
        """
        Use Spirent object information to get port handle keys

	ARGUMENTS:
	     [**args]
	     :param OBJECT device:
	        *MANDATORY* Device handle on which the commands are to be executed. This can
                        be obtained by using the keyword 'Get Handle' and specifying the 
                        proper device resource (can be rt1, rt2, etc.)
	     :param STR intf:
                *MANDATORY* interface name

	ROBOT USAGE:
	     ${rt_handle} =  Get Handle  resource=rt0
    	     ${rt_portHandle1} =  Get Port Handle  ${rt_handle}  intf=rt0-1
	
	return : port handle else raise an exception

        """
        intf = None
        if 'intf' in args.keys():
            intf = args['intf'].lower()
            if intf in self.intf_to_port_map.keys():
                port = self.intf_to_port_map[intf]
                if port in self.port_to_handle_map.keys():
                    return self.port_to_handle_map[port]
            else:
                raise TobyException("No such port " + str(intf), host_obj=self)

def invoke(device, function, **kwargs):
    """
    Pass-through function for Spirent method of same name to call sth.py functions
    """
    if function == 'connect':
        return device.connect(**kwargs)
    elif function == 'get_port_handle':
        return device.get_port_handle(**kwargs)
    else:
        return device.invoke(function, **kwargs)

def check_device_reachability(self, host):
    """
    Diagnostics to check spirent Device responding to pings
    """
    from jnpr.toby.utils.iputils import ping
    if host:
        results = "Checking device is pingable...\n"
        if ping(host=host, count=2, interval=2, timeout=10):
            results += '    Device is responding to pings\n'
            self.log(results)
            return True
        else:
            results += '    Device is not responding to pings\n'
            self.log(results)
            return False

def check_port_status(self, host, port, timeout, port_name):
    """
    Diagnostics to check Device port status
    """
    results = "Checking spirent {} port status...\n".format(port_name)
    sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_conn.settimeout(timeout)
    try:
        sock_conn.connect((host, int(port)))
        sock_conn.shutdown(socket.SHUT_RDWR)
        results += '    {} port is up and running\n'.format(port_name)
        self.log(results)
        return True
    except:
        return False
    finally:
        sock_conn.close()

def spirent_diagnostics(self):
    """
    Diagnostics to log additional information
    """
    self.log("Spirent HLTAPI library path :" + self.lib_path + '/HLTAPI/' + self._get_hltapi_version())
    hlt_log_path = self.log_dir + '/spirent/*.hltlog'
    bll_log_path = self.log_dir + '/spirent/client.bll.log'
    hlt_log = subprocess.check_output('tail -n 80 %s' % hlt_log_path, shell=True)
    bll_log = subprocess.check_output('tail -n 80 %s' % bll_log_path, shell=True)
    self.log("Spirent hlt logs for more details..")
    self.log("--------------------------------------------")
    self.log(hlt_log.decode())
    self.log("--------------------------------------------")
    self.log("Spirent bll logs for more details..")
    self.log("--------------------------------------------")
    self.log(bll_log.decode())
    self.log("--------------------------------------------")
