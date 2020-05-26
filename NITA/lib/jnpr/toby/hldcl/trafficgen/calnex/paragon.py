"""
Paragon module providing abstracting to Paragon.py function within Paragon.
"""
import atexit
import os
import sys
import inspect
import re
import ruamel.yaml as yaml
from jnpr.toby.hldcl.trafficgen.trafficgen import TrafficGen
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.exception.toby_exception import TobyException
import jnpr.toby.frameworkDefaults.credentials as credentials

class Paragon(TrafficGen):
    """
    Paragon emulation class
    """
    def __init__(self, system_data=None, paragon_lib_path=None):
        """
        Paragon abstraction layer for HLTAPI

        -- Workflow 1 --
        :param  system_data:  *MANDATORY* Dictionary of Paragon information
          rt0:
            interfaces:
              intf1:
                name: 1/8
              intf2:
                name: 1/9
            system:
              primary:
                controllers:
                  unknown:
                    domain: englab.juniper.net
                    hostname: wf-paragonchassis2
                    mgt-intf-name: mgt0
                    mgt-ip: 10.9.1.107
                    osname: IxOS
                make: paragon
                model: xgs12
                name: paragonx-123
                osname: Calnex

        -- Workflow 2 --
        :param  host  *MANDATORY* FQDN/mgt-ip of of chassis


        :return: Paragon object
        """
        self.instrument_ip = None
        self.server_ip = None
        self.interfaces = None
        self.intf_to_port_map = dict()
        self.port_to_handle_map = dict()
        self.handle_to_port_map = None
        self.paragon = None
        self.log_dir = get_log_dir()
        atexit.register(self.cleanup)
        self.user_functions = dict()
        self.is_connected = False

        if paragon_lib_path:
            self.paragon_lib_path = paragon_lib_path
        else:
            environment = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__), "environment.yaml")))
            self.paragon_lib_path = environment['paragon-lib-path']

        if not system_data:
            raise TobyException("Missing system information for paragon device initialization")

        controller_key = list(system_data['system']['primary']['controllers'].keys())[0]

        kwargs = dict()
        kwargs['host'] = self.chassis = system_data['system']['primary']['name']
        kwargs['hostname'] = self.chassis = system_data['system']['primary']['name']
        kwargs['os'] = system_data['system']['primary']['controllers'][controller_key]['osname']
        super(Paragon, self).__init__(**kwargs)

        if 'mgt-ip' in system_data['system']['primary']['controllers'][controller_key]:
            self.instrument_ip = system_data['system']['primary']['controllers'][controller_key]['mgt-ip']

        if 'server-ip' in system_data['system']['primary']:
            self.server_ip = system_data['system']['primary']['server-ip']
        else:
            raise TobyException('Missing server-ip', self)

        sys.path.append(self.paragon_lib_path)
        self.paragon = __import__('paragon')

        # Import extended paragon modules with functions from jnpr/toby/trafficgen/calnex/paragon
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        user_module_dir = re.sub(r"jnpr\/toby.*", "jnpr/toby/trafficgen/calnex/paragon", current_dir)
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
        Logout from Paragon device
        """
        if self.is_connected:
            try:
                self.invoke('paragonset', "Rst", "TRUE")
                self.invoke('disconnect')
                self.log(level="INFO", message="Disconnected from Paragon device")
            except Exception:
                self.log(level="ERROR", message="It appears that you did not stop your traffic first.  Please go to paragon gui to disconnect")

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

    def invoke(self, function, *args, **kwargs):
        """
        Pass-through for Paragon.py functions
        """
        result = None
        # User contributed module
        if function in self.user_functions:
            self.log("Invoking Juniper Paragon function " + function + " with parameters " + str(args))
            result = self.user_functions[function](self, *args, **kwargs)
            self.log("Invocation of Juniper Paragon function " + function + " completed with result " + str(result))
            return result
        # Direct paragon API functions
        self.log("Invoking Paragon API " + function + " with the following parameters: " + str(args))
        paragon_func = getattr(self.paragon, function)
        result = paragon_func(*args, **kwargs)
        self.log("Invocation of Paragon method " + function + " executed. Return result: " + str(result))
        return result

    def connect(self, **args): # pylint: disable=unused-argument
        """
        Connect to Paragon server
        """
        self.log("Attempting connection to Paragon: Instrument_ip=" + self.instrument_ip + ", Server_ip=" + self.server_ip)
        # Connect (Instrument address, App server address)
        self.paragon.connect(self.instrument_ip, self.server_ip)
        #p.connect("10.216.64.36", "10.216.67.42")
        # Retrieve and print the instrument serial number
        print("Instrument serial number: " + self.paragon.paragonget("Idn"))
        # Reset the instrument to default settings
        self.is_connected = True
        self.invoke("paragonset", "Rst", "TRUE")

    def get_port_handle(self, **args):
        """
        Use Paragon object information to get port handle keys
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
    Pass-through function for Paragon method of same name to call Paragon.py functions
    """
    if function == 'connect':
        return device.connect(**kwargs)
    elif function == 'get_port_handle':
        return device.get_port_handle(**kwargs)
    else:
        return device.invoke(function, **kwargs)
