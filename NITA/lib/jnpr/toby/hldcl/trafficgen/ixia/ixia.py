"""
IXIA module providing abstracting to sth.py function within IXIA.
"""
import os
import re
import sys
import time
import atexit
import telnetlib
import paramiko
import inspect
import six
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.hldcl.trafficgen.trafficgen import TrafficGen
from jnpr.toby.exception.toby_exception import TobyException, IxiaConnectError, TobyIxiaException, TobyIxiaAppserverConnectException, TobyIxiaChassisConnectException
# for some reason, pylint complaining on next two modules
import ruamel.yaml as yaml
import pexpect
#import pdb
# pylint: disable=bad-continuation,import-error,superfluous-parens,too-many-locals
class Ixia(TrafficGen):
    """
    IXIA emulation class
    """
    def __init__(self, system_data=None, chassis=None, appserver=None, license_server=None, ixia_lib_path=None):
        """
        IXIA abstraction layer for HLTAPI

        -- Workflow 1 --
        :param  system_data  *MANDATORY* Dictionary of IXIA information
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
                license_server: sv8-pod1-ixlic1.englab.juniper.net
                make: ixia
                model: xgs12
                name: wf-ixchassis2
                osname: IxOS

        -- Workflow 2 --
        :param  chassis  *MANDATORY* Name of chassis
        :param  appserver  *MANDATORY* Name of tcl server
        :param  license_server  *MANDATORY* Name of chassis

        :return: ixia object
        """
        self.virtual = False
        self.port_list = None
        self.session_info = None
        self.handle_to_port_map = None
        self.port_to_handle_map = None
        self.intf_to_port_map = None
        self.major_minor_version = None
        self.physical_port_type = 'fiber'
        self.user_functions = dict()
        self.connect_args = dict()
        self.cleanup_session_args = None
        self.port_order = None
        self.interfaces = None
        self.port = 8009
        self.connect_to_current_session = False
        self.connect_to_current_session_args = dict() # args just for connecting to current session
        atexit.register(self.cleanup)
        self.min_version = None
        self.username, self.password = credentials.get_credentials(os='Ixia')
        self.port_type = dict()
        # Ixia API handles
        self._ixiangpf = None
        self._ixiaixnet = None

        if ixia_lib_path:
            self.lib_path = ixia_lib_path
        else:
            environment = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__), "environment.yaml")))
            self.lib_path = environment['ixia-lib-path']
        if system_data:
            sys_pri = system_data['system']['primary']
            controller_key = list(sys_pri['controllers'].keys())[0]
            self.chassis = sys_pri['controllers'][controller_key]['mgt-ip']

            # Instantiate host object for logging
            host_args = dict()
            if 'name' in sys_pri:
                host_args['host'] = sys_pri['name']
            else:
                raise TobyIxiaException("Missing 'name' from 'primary' system stanza")
            if 'osname' in sys_pri['controllers'][controller_key]:
                host_args['os'] = sys_pri['controllers'][controller_key]['osname']
            else:
                raise TobyIxiaException("Missing 'osname' from controller " + controller_key + " stanza")
            super(Ixia, self).__init__(**host_args)


            # connect user fv- knob information and materialize kwargs for Ixia connect() call
            if 'appserver' in sys_pri:
                self.connect_args['ixnetwork_tcl_server'] = sys_pri['appserver']
            if 'appserver-port' in sys_pri:
                self.connect_args['ixnetwork_tcl_server'] = sys_pri['appserver'] + ':' + str(sys_pri['appserver-port'])
                self.port = sys_pri['appserver-port']
            if 'appserver-username' in sys_pri:
                self.connect_args['user_name'] = sys_pri['appserver-username']
            if 'appserver-password' in sys_pri:
                self.connect_args['user_password'] = sys_pri['appserver-password']
            if 'return-detailed-handles' in sys_pri:
                if sys_pri['return-detailed-handles'] == 'disable':
                    self.connect_args['return_detailed_handles'] = 0
            if 'config-file' in sys_pri:
                self.connect_args['config_file'] = sys_pri['config-file']
            else:
                self.connect_args['reset'] = 1
            if sys_pri['model'].lower().startswith('ixvm') or sys_pri['model'].lower().startswith('vixia'):
                self.virtual = True
                self.model = sys_pri['model'].lower()
                self.log(level='INFO', message="IXIA Type= Virtual")
                if 'license_server' in sys_pri:
                    self.connect_args['ixnetwork_license_servers'] = sys_pri['license_server']
                if 'license_type' in sys_pri:
                    if sys_pri['license_type'].startswith('tier'):
                        self.connect_args['ixnetwork_license_type'] = 'mixed_' + sys_pri['license_type']
                    else:
                        self.connect_args['ixnetwork_license_type'] = sys_pri['license_type']
            else:
                self.log(level='INFO', message="IXIA Type= Physical")

            if 'connect-args' in sys_pri and type(sys_pri['connect-args']) is dict:
                self.connect_args.update(sys_pri['connect-args'])
            if 'cleanup-session-args' in sys_pri and type(sys_pri['cleanup-session-args']) is dict:
                self.cleanup_session_args = sys_pri['cleanup-session-args']
            if 'port-order' in sys_pri:
                self.port_order = sys_pri['port-order']
            if 'connect-to-current-session' in sys_pri and sys_pri['connect-to-current-session'] == 'enable':
                self.connect_to_current_session = True
                self.connect_to_current_session_args['ixnetwork_tcl_server'] = self.connect_args['ixnetwork_tcl_server']
                # adding only connect-args for current session (no other arguments so can preserve session)
                if 'connect-args' in sys_pri and type(sys_pri['connect-args']) is dict:
                    self.connect_to_current_session_args.update(sys_pri['connect-args'])

            if 'min-version' in sys_pri and type(sys_pri['min-version']) is str:
                self.min_version = sys_pri['min-version']
                self.log(level='info', message="Ixia Minimum Chassis Version is set to: "+ sys_pri['min-version'])

            # Ensure mandatory connect() args are satisfied
            if 'ixnetwork_tcl_server' not in self.connect_args:
                raise TobyIxiaException("Missing appserver information (ixnetwork_tcl_server).  This may be provided via 'fv-ixia-appserver'"
                                    "knob, or via 'fv-ixia-connect-args'.", host_obj=self)
            if sys_pri['model'].lower().startswith('ixvm') or sys_pri['model'].lower().startswith('vixia'):
                if 'ixnetwork_license_servers' not in self.connect_args:
                    raise TobyIxiaException("Missing VM licensing information (ixnetwork_license_servers)." + \
                                        "This may be provided via 'fv-ixia-license-server' knob, or via 'fv-ixia-connect-args'.",
                                        host_obj=self)
                if 'ixnetwork_license_type' not in self.connect_args:
                    self.connect_args['ixnetwork_license_type'] = 'mixed_tier1'


        elif chassis and appserver:
            self.chassis = chassis
            self.appserver = appserver
            if license_server:
                self.license_server = license_server
        else:
            raise TobyIxiaException("Missing either system_data (Workflow 1) or chassis/appserver"
                                "/license_server (Workflow 2) parameters", host_obj=self)

        self.intf_status = None
        self.log(level='info', message="CHASSIS= " + self.chassis)
        self.log(level='info', message="APPSERVER= " + self.connect_args['ixnetwork_tcl_server'])

        self.wait = 1
        self.telnet_handle = None
        self.version = self._get_version()
        if self.min_version:
            if(float(self.version) < float(self.min_version)):
                raise TobyIxiaChassisConnectException("Ixia Minimum Chassis Version Check Failed", host_obj=self)
        if self.virtual:
            result = self._configure_promiscuous()
            if not result:
                self.log(level='WARN', message="Unable to set Promiscuous mode on IXIA virtual chassis")
            else:
                self.log(level='info', message="Successfully set Promiscuous mode on IXIA virtual chassis")
            if self.chassis_type is not None:
               if self.model.startswith('vixia') and re.search('Virtual Load Module', self.chassis_type, re.I):  
                   self.log(level='WARN', message="Virtual ixia chassis type is not correct as virtual modeli defined in params")
        self.ixia_lib_version = self._get_lib_version()
        self._set_envs()
        # Import core modules for native IXIA APIs
        # disable import-error because dynamic ENV changes based on IXIA version make it possible to import ok
        from ixiatcl import IxiaTcl # pylint: disable=import-error
        from ixiahlt import IxiaHlt # pylint: disable=import-error
        from ixiangpf import IxiaNgpf # pylint: disable=import-error
#        from ixiaerror import IxiaError # pylint: disable=import-error

        self.ixiatcl = IxiaTcl()
        self.ixiahlt = IxiaHlt(self.ixiatcl)
        self._ixiangpf = IxiaNgpf(self.ixiahlt)

        # Import extended ixia modules with functions
        # from jnpr/toby/trafficgen/ixia
        current_dir = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        user_module_dir = re.sub(r"jnpr\/toby.*", "jnpr/toby/trafficgen/ixia", current_dir)
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
                        raise TobyIxiaException("Duplicate functions in user contributed modules", host_obj=self)
                    self.user_functions[function_name] = function

    def _configure_promiscuous(self):
        """
        To enable promiscuous mode for Ixia Virtual Test Appliance
        """
        try:
            cmd = 'set promiscuous-mode all enable'
            if (self.version):
                match = re.match(r'(\d+.\d+).*', self.version)
                if match and float(match.group(1)) >= 8.50:
                    cmd = 'set promiscuous-mode all all enable'
            pexp = pexpect.spawn('ssh -l StrictHostKeyChecking=no %s@%s' % (self.username, self.chassis))
            pexp.expect('password:')
            time.sleep(2)
            pexp.sendline(self.password)
            pexp.expect('#')
            pexp.sendline(cmd)
            pexp.expect('#')
            output = pexp.before
            pexp.sendline('exit')
            if re.search(r'Promiscuous mode was successfully set|promiscuous mode.*enabled', output.decode('utf-8'), re.IGNORECASE):
                return True
            else:
                return False
        except Exception:
             self.log(level="ERROR", message="Unable to connect to IXIA virtual Chassis")


    def _get_version(self):
        """
        Get Chassis OS Version of IXIA TC
        :
        :return: ixia chassisversion
        """
        version = None
        chassis_type = None
        try:
            # Trying to get the ixia version with out login to the box using SSH
            retvalue = os.popen(
                'ssh -o PasswordAuthentication=no -o StrictHostKeyChecking=no '
                + self.username + '@' + self.chassis +
                ' 2>&1 | grep "Welcome to Ixia\\|IxOS Version\\|Connection refused"').readlines()
            if retvalue and len(retvalue) > 0:
                search_obj = re.search(r'Version:\s+(\d+\.\d+\.\d+\.\d+)', retvalue[1])
                if search_obj:
                    version = re.sub(r'Version:\s+', '', search_obj.group(0))
                    chassis_type = self._find_chassis_type(retvalue[0])
                elif re.search(r'Connection refused', retvalue[0], re.IGNORECASE):
                    self.log(level="INFO", message="Could not initiate ssh connection to box")
                    raise Exception("Could not initiate ssh connection to box %s" % self.chassis)
            if version is None:
                #Trying to get the ixia version by login to the box using SSH
                ssh_cl = paramiko.client.SSHClient()
                ssh_cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_cl.connect(hostname=self.chassis, username=self.username, password=self.password, allow_agent=False, look_for_keys=False)
                channel = None
                data = ''
                try:
                    channel = ssh_cl.invoke_shell(width=160)
                    time.sleep(2)
                except:
                    transport = ssh_cl.get_transport()
                    channel = transport.open_session()
                if channel.recv_ready():
                    data = channel.in_buffer.empty()
                    try:
                        data = data.decode('utf-8')
                    except UnicodeDecodeError:
                        data = data.decode('iso-8859-1')
                ver_re = re.compile(r'IxOS Version.*:\s+(\d+\.\d+\.\d+\.\d+)', re.IGNORECASE)
                ver_old_re = re.compile(r'enter chassis', re.IGNORECASE)
                version = ""
                banner_out = ""
                command_response = ''
                if ver_re.search(str(data)):
                    banner_out = str(data)
                    ver_search = ver_re.search(banner_out)
                    if ver_search:
                        version = ver_search.group(1)
                        chassis_type = self._find_chassis_type(banner_out)
                    else:
                        self.log(level="INFO", message="Connect response does not have version info: %s" % banner_out)
                        try:
                            channel.exec_command('show chassis installed-versions')
                        except:
                            transport = ssh_cl.get_transport()
                            channel = transport.open_session()
                            channel.exec_command('show chassis installed-versions')
                        time.sleep(2)
                        if channel.recv_ready():
                            command_response = channel.recv(1024)
                        version = re.search(r'Chassis:\s+\*?((\d+\.){3}\d+)', command_response.decode('utf-8'), re.IGNORECASE).group(1)
                        chassis_type = self._find_chassis_type(banner_out)
                elif ver_old_re.search(str(data)):
                    channel.send('enter chassis\n')
                    channel.send('show ixos active-version\n')
                    time.sleep(2)
                    if channel.recv_ready():
                        command_response = channel.recv(5102)
                    match = re.search(r'IxOS active version:.*?(\d+\.\d+\.\d+\.\d+)', command_response.decode('utf-8'), re.IGNORECASE)
                    if match:
                        version = match.group(1)
                        chassis_type = self._find_chassis_type(command_response)
                else:
                    self.log(level="INFO", message="Connect response does not have version info: %s" % banner_out)
                    try:
                        channel.exec_command('show ixos active-version')
                    except:
                        transport = ssh_cl.get_transport()
                        channel = transport.open_session()
                        channel.exec_command('show ixos active-version')
                    time.sleep(2)
                    if channel.recv_ready():
                        command_response = channel.recv(1024)
                    match = re.search(r'IxOS active version:\s+IxOS\s+(\d+\.\d+\.\d+\.\d+)', command_response.decode('utf-8'), re.IGNORECASE)
                    if match:
                        version = match.group(1)
                        chassis_type = self._find_chassis_type(command_response)
                ssh_cl.exec_command('exit')
                if version is not None:
                    self.log(level="INFO", message="Ixos version: %s \n" % version)
                else:
                    self.log(level="INFO", message="Could not get the ixia verion using ssh connection")
                    raise Exception("Could not get the ixia verion using ssh connection to box %s" % self.chassis)
        except Exception as ex:
            self.log(level="INFO", message="Toby was not able to find version using ssh due to: %s" % ex.__str__())
            #Trying to get the ixia version with out login to the box using Telnet
            self.log(level="INFO", message="Trying telnet for chassis %s" % self.chassis)
            try:
                telnet_handle = telnetlib.Telnet(self.chassis)
                banner_out = telnet_handle.read_until(b"Ixia>")
                time.sleep(10)
                cmd = "package require IxTclHal;version cget -ixTclHALVersion\n"
                cmd = cmd.encode('ascii')
                telnet_handle.write(cmd)
                match_results = telnet_handle.expect([br"\d+\.\d+\.\d+\.\d+"])
                version = match_results[1].group(0).decode('ascii')
                self.log(level="INFO", message="Ixos version: %s \n" % version)
                chassis_type = self._find_chassis_type(banner_out)
                telnet_handle.close()
            except Exception as ex:
                self.log(level="ERROR", message="Toby was not able to find version info using telnet connection due to: %s" % ex.__str__())
                #self.log(level="ERROR", message="Could not get the version info using telnet connection")

        if not version:
            if not check_device_reachabiliy(self, self.chassis):
                raise TobyIxiaChassisConnectException("IXIA chassis is not pingable")
            else:
                raise TobyIxiaException("Unable to detect IXIA version", host_obj=self)

        self.log(level='info', message='CHASSIS VERSION: ' + version)
        self.major_minor_version = re.search(r'^\d+\.\d+', version).group(0)

        if not self.major_minor_version:
            raise TobyIxiaException("Unable to derive major and minor version from " + version, host_obj=self)

        if float(self.major_minor_version) < 8.20:
            raise TobyIxiaException("Unsupported version " + self.major_minor_version + ". Minimum version supported: 8.20", host_obj=self)
        self.chassis_type = chassis_type
        return version

    def _find_chassis_type(self, response):
        """
        Find Chassis type based
        :return: ixia chassis type 
        """
        chassis_type = None
        search_obj = re.search(r'Welcome to Ixia (Virtual Chassis|Virtual Test Appliance|Virtual Load Module)', str(response), re.I)
        if search_obj:
            chassis_type = search_obj.group(1)
            self.log(level='info', message='Virtual chassis type: %s' % chassis_type)
        return chassis_type

    def _set_envs(self):
        """
        Set ENVs required for IXIA TC
        """
        if self.version is None:
            self._get_version()

        ixia_lib_path_prefix = self.lib_path + '/' + self.ixia_lib_version + '/lib'

        os.environ['TCLLIBPATH'] = ixia_lib_path_prefix
        sys.path.append(ixia_lib_path_prefix + '/hltapi/library/common/ixiangpf/python')
        sys.path.append(ixia_lib_path_prefix + '/PythonApi')

        self.log(level="info", message="ADDED_TO_PATH= " + os.environ['TCLLIBPATH'])
        self.log(level="info", message="ADDED_TO_PYTHONPATH= " + ixia_lib_path_prefix + '/hltapi/library/common/ixiangpf/python')
        self.log(level="info", message="ADDED_TO_PYTHONPATH= " + ixia_lib_path_prefix + '/PythonApi')

    def _get_lib_version(self):
        """
        Needed to determine which IXIA library folder to use.
        """
        ixia_lib_ver = None
        try:
            best_match = None
            ixia_lib_vers = list(filter(lambda x: os.path.isdir(os.path.join(
                self.lib_path, x)), os.listdir(self.lib_path)))
            for possible_lib_ver in ixia_lib_vers:
                if re.search(r'\d+\.\d+\.\d+\.\d+', possible_lib_ver):
                    if possible_lib_ver == self.version:
                        ixia_lib_ver = possible_lib_ver
                        break
                    elif re.search(r'^' + self.major_minor_version, possible_lib_ver):
                        best_match = possible_lib_ver
            if best_match and not ixia_lib_ver:
                ixia_lib_ver = best_match
        except:
            raise TobyIxiaException(
                "Unable to find appropriate IXIA lib version in " +
                self.lib_path + " for Ixia version " + self.version, host_obj=self)

        if not ixia_lib_ver:
            raise TobyIxiaException("Unable to find appropriate IXIA lib version in " +
                                self.lib_path + " for Ixia version " + self.version, host_obj=self)

        self.log(level="INFO", message="IXIA LIB AVAILABLE = " + str(ixia_lib_ver))
        return ixia_lib_ver

    def add_interfaces(self, interfaces):
        """
        Get interfaces{} block from yaml to use fv- knobs therein
        """
        self.interfaces = interfaces

    def add_intf_to_port_map(self, intf_to_port_map):
        """
        Add attribute to ixia object which contains
        params intf to port mappings
        """
        self.intf_to_port_map = intf_to_port_map

    def _initialize_ports(self):
        # next, initialize the port via interface_config
        fiber_port_handles = []
        copper_port_handles = []
        ge_port_handles = []
        xe_port_handles = []

        for intf in self.interfaces:
            if 'physical-port-type' in self.interfaces[intf] and self.interfaces[intf]['physical-port-type'] == 'copper':
                copper_port_handles.insert(0, self.get_port_handle(intf))
            else: # fiber
                fiber_port_handles.insert(0, self.get_port_handle(intf))
            if self.port_type:
                if re.search(r'^Novus', self.port_type[self.interfaces[intf]['name']], re.IGNORECASE):
                    if 'type' in self.interfaces[intf] and 'ge' in self.interfaces[intf]['type']:
                        ge_port_handles.insert(0, self.get_port_handle(intf))
                    elif 'type' in self.interfaces[intf] and 'xe' in self.interfaces[intf]['type']:
                        xe_port_handles.insert(0, self.get_port_handle(intf))

        if len(copper_port_handles):
            self.log("Invoking interface_config for copper ports: " + str(copper_port_handles))
            result = self._ixiangpf.interface_config(port_handle=copper_port_handles, phy_mode='copper')
            self.log('INFO', "Invokation of interface_config result: " + str(result))
        if len(fiber_port_handles):
            self.log("Invoking interface_config for fiber ports: " + str(fiber_port_handles))
            result = self._ixiangpf.interface_config(port_handle=fiber_port_handles, phy_mode='fiber')
            self.log('INFO', "Invokation of interface_config result: " + str(result))
        if len(ge_port_handles):
            self.log("Invoking interface_config for nova card GE ports: " + str(ge_port_handles))
            result = self._ixiangpf.interface_config(port_handle=ge_port_handles, autonegotiation='1', speed='ether1000')
            self.log('INFO', "Invokation of interface_config result: " + str(result))
        if len(xe_port_handles):
            self.log("Invoking interface_config for nova card XE ports: " + str(xe_port_handles))
            result = self._ixiangpf.interface_config(port_handle=xe_port_handles, autonegotiation='0', speed='ether10Gig')
            self.log('INFO', "Invokation of interface_config result: " + str(result))

    def invoke(self, command, *args, **kwargs):
        """
        Pass-through for ixnetwork.py functions
        (ixnetwork.py? or something else?)
        """

        lib = 'ngpf'

        if re.search(r'^IxNet::', command):
            lib = 'ixnet'
            command = command.replace('IxNet::', '', 1)
            # Initialize IxNet if not set up already
            if not self._ixiaixnet:
                from IxNetwork import IxNet # pylint: disable=import-error
                self._ixiaixnet = IxNet()
                self._connect_ixnet()

        if 'port_handle' in kwargs.keys():
            port_handle = kwargs['port_handle']
            if isinstance(port_handle, six.string_types):
                port_handle = port_handle.split(' ')
            if port_handle[0] in self.intf_to_port_map.keys():
                new_port_handle = list()
                for intf in port_handle:
                    new_port_handle.append(self.port_to_handle_map[self.intf_to_port_map[intf]])
                kwargs['port_handle'] = ' '.join(new_port_handle)

        # User contributed module
        if command in self.user_functions:
            self.log(level="info", message="Invoking Juniper IXIA function " + command + " with parameters " + str(kwargs))
            result = self.user_functions[command](self, **kwargs)
            self.log(level="info", message="Invocation of Juniper IXIA function " + command + " completed with result: " + str(result))
            return result
        # ngpf method
        elif lib == 'ngpf':
            self.log(level="info", message="Invoking IXIA ngpf method " + command + " with parameters " + str(kwargs))
            ixia_method = getattr(self._ixiangpf, command)
            result = ixia_method(**kwargs)
            if result['status'] == '0':
                raise TobyIxiaException("Invocation of IXIA method " + command + " failed with result: " + str(result), host_obj=self)
            else:
                self.log(level="debug", message="Invocation of IXIA method " + command + " succeeded with result: " + str(result))
                return result
        # ixnet method
        elif lib == 'ixnet':
            ixnet_args = kwargs.get('ixnet_args', None)
            if not ixnet_args and len(args) > 0: # args came in via python *args instead of via kwargs(ixnet_args)
                ixnet_args = args
            self.log("INFO", message="Invoking IXIA ixnet API '" +command + "' with parameters " + str(ixnet_args))
            ixia_method = getattr(self._ixiaixnet, command)
            if ixnet_args:
                result = ixia_method(*ixnet_args)
            else:
                result = ixia_method()
            self.log("INFO", message="Invocation of IXIA API '" + command + "' completed with result: " + str(result))
            return result

    def _connect_ixnet(self):
        tcp_port = self.session_info['connection']['port']
        client_version = self.session_info['connection']['client_version']
        self.log('INFO', "Invoking ixnet connect() on tcp port " + tcp_port + " with client version " + client_version)
        connect_status = self._ixiaixnet.connect(self.connect_args['ixnetwork_tcl_server'], '-port', tcp_port, '-version', client_version)
        self.log('INFO', "Ixnet connect status: " + str(connect_status))

    def connect(self, port_list=None):
        """
        Connect to IXIA chassis

        :param port_list (*REQUIRED): port list , ex: '1/9 1/10 1/11'
        :return: ixia connection object
        """
        if not port_list and not self.connect_to_current_session:
            raise TobyIxiaException("Missing port_list parameter", host_obj=self)
        connect_status = None

        #reorder port list if required - useful when config_file is being loaded and ports need to pair up exactly
        if self.port_order:
            duplicate_port_check = {}
            new_port_list = []
            interfaces = self.port_order.split(':')
            for intf in interfaces:
                if intf in duplicate_port_check:
                    raise TobyIxiaException("duplicate port " + intf + " found in port_list [fv-ixia-port-list]", host_obj=self)
                if intf in self.intf_to_port_map:
                    new_port_list.append(self.intf_to_port_map[intf])
                    duplicate_port_check[intf] = 1
                else:
                    raise TobyIxiaException("IXIA Port " + intf + " specified in ordered port list does not exist", host_obj=self)
            if len(port_list) != len(new_port_list):
                raise TobyIxiaException("IXIA port ordered list [fv-ixia-port-list] does not match number of interfaces present", host_obj=self)

            port_list = new_port_list

        if self.connect_to_current_session:
            self.log(level="INFO", message="Connecting to existing IXIA session via ngpf(HLTAPI) with the following arguments: "
                                            + str(self.connect_to_current_session_args))
            connect_status = self._ixiangpf.connect(**self.connect_to_current_session_args)
        else:
            ports = " ".join(port_list)
            self.connect_args['port_list'] = ports
            self.connect_args['device'] = self.chassis

            self.log(level="INFO", message="Connecting to IXIA via ngpf(HLTAPI) with parameters " + str(self.connect_args))
            connect_status = self._ixiangpf.connect(**self.connect_args)
        self.log(level="INFO", message="IXIA Connection status: " +  str(connect_status))

        if connect_status['status'] != '1':
            error_message = "Not able to connect to IXIA, "
            if not check_appserver_reachabiliy(self, self.connect_args['ixnetwork_tcl_server'], self.port):
                error_message += "Failed to connect to appserver %s using port %s" % (self.connect_args['ixnetwork_tcl_server'], self.port)
            else :
                if 'log' in connect_status:
                    error_message = error_message + " : " + connect_status['log']
            raise TobyIxiaAppserverConnectException(error_message, host_obj=self)
        self.session_info = connect_status
        try:
            root = self._invokeIxNet('getRoot')
            vports = self._invokeIxNet('getList', root, 'vport')
            for tr in vports:
                l1config = self._invokeIxNet('getList', tr, 'l1Config')
                port_detail = self._invokeIxNet('getAttribute', tr, '-connectionStatus')
                match1 = port_detail.split(";")
                interface_name = match1[1].lstrip("0").strip() + "/" + match1[2].split()[0].lstrip("0").strip()
                card_type = self._invokeIxNet('getAttribute', l1config[0], '-currentType')
                if interface_name and card_type:
                   self.port_type[interface_name] = card_type
        except:
             self.log(level="INFO", message="Unable to get card type of IXIA virtual Chassis ports")

        if port_list:
            if self.connect_to_current_session:
                result = self._ixiangpf.session_info(mode='get_session_keys', session_keys_include_filter='connect.vport_list')
                port_handle_list = result['vport_list'].split(' ')
            else:
                port_handle_list = connect_status['vport_list'].split(' ')
            self.port_list = port_list
            self.port_to_handle_map = dict(zip(port_list, port_handle_list))
            self.handle_to_port_map = dict(zip(port_handle_list, port_list))
            if not self.connect_to_current_session:
                self._initialize_ports()

    def get_port_handle(self, intf):
        """
        Use IXIA object information to get port handle keys
        """
        intf = intf.lower()
        if intf in self.intf_to_port_map.keys():
            port = self.intf_to_port_map[intf]
            if port in self.port_to_handle_map.keys():
                return self.port_to_handle_map[port]
        else:
            raise TobyIxiaException("No such params interface " + intf, host_obj=self)

    def cleanup(self):
        """
        Destructor to clean up session
        """
        print("Cleaning up Ixia port handles via cleanup_session() IXIA call")
        if self.handle_to_port_map:
            if self.cleanup_session_args:
                if 'port_handle' not in self.cleanup_session_args:
                    self.cleanup_session_args['port_handle'] = self.handle_to_port_map.keys()
                print("Clean up session args : "+str(self.cleanup_session_args))
                result = self._ixiangpf.cleanup_session(**self.cleanup_session_args)
            else:
                result = self._ixiangpf.cleanup_session()

            if result['status'] == '0':
                print("Ixia cleanup failed. Ixia API response: " + str(result))
            else:
                print("Ixia cleanup successful")

    def _invokeIxNet(self, command, *args):
        """
        To Execute Low Level APIs on the Existing Session.
        """
        self.log(level="info", message="Invoking IXIA ixNet method " + command + " with parameters " + str(args))
        ixnet = self._ixiangpf.ixnet
        ixia_method = getattr(ixnet, command)
        try:
            result = ixia_method(*args)
            self.log(level="info", message="Invocation of IXIA method " + command + " succeeded with result: " + str(result))
            return result
        except Exception as e:
            raise TobyException("Invocation of IXIA method " + command + " failed with result: " + str(e), host_obj=self)

def invoke(device, function, **kwargs):
    """
    Pass-through function for IXIA method of same name to call sth.py functions
    """
    return device.invoke(function, **kwargs)

def check_appserver_reachabiliy(self, appserver, port):
    self.log(level="INFO", message="Trying telnet to appserver %s" % appserver)
    try:
        pexp = pexpect.spawn('telnet %s' % appserver)
        pexp.expect("Ixia>")
        time.sleep(10)
        cmd = "package require IxTclNetwork\r"
        pexp.sendline(cmd)
        time.sleep(10)
        pexp.expect("Ixia>")
        match_results = pexp.before
        cmd = "ixNet connect localhost -port " + port  + "\r"
        pexp.sendline(cmd)
        pexp.expect(r"\:OK", timeout=60)
        match_results = pexp.before
        if re.search(r'::ixNet:', str(match_results), re.I):
            self.log(level="INFO", message="Successfully connected to appserver %s using port %s" % (appserver, port))
        else:
            return False
        cmd = "ixNet disconnect\n"
        cmd = cmd.encode('ascii')
        pexp.sendline(cmd)
        time.sleep(20)
        pexp.expect("Ixia>")
        pexp.close()
        return True
    except Exception:
        self.log(level="INFO", message="Faied to connect to appserver")
        check_device_reachabiliy(self, appserver)
        return False

def check_device_reachabiliy(self, host):
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

