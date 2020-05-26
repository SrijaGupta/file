"""
Elevate module providing abstracting to av.py function within Elevate.
"""
import os
import sys
import atexit
import ruamel.yaml as yaml
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.hldcl.trafficgen.trafficgen import TrafficGen
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.exception.toby_exception import TobyException

class Elevate(TrafficGen):
    """
    Spirent Elevate API abstraction class
    """
    def __init__(self, chassis=None, system_data=None):
        """
        Spirent Elevate abstraction layer for Utils.py API

        -- Workflow 1 --
        :param  system_data:  *MANDATORY* Dictionary of Elevate information
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
                make: spirent
                model: spirent
                name: elevate1
                osname: Elevate

        -- Workflow 2 --
        :param  host  *MANDATORY* FQDN/mgt-ip of of chassis


        :return: Elevate object
        """
        self.chassis = None
        self.interfaces = None
        self.model = 'Unknown'
        self.platform_type = 'Elevate'
        self.intf_to_port_map = dict()
        self.port_to_handle_map = dict()
        self.session_info = None
        self.handle_to_port_map = None
        atexit.register(self.cleanup)

        self.log_dir = get_log_dir()
        atexit.register(self.cleanup)

        environment = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__), "environment.yaml")))
        self.lib_path = environment['elevate-lib-path']
        self.api_path = self.lib_path + '/Elevate/PythonAPI/1.0.0'

        if system_data:

            controller_key = list(system_data['system']['primary']['controllers'].keys())[0]

            kwargs = dict()
            kwargs['host'] = self.chassis = system_data['system']['primary']['name']
            kwargs['hostname'] = self.chassis = system_data['system']['primary']['name']
            kwargs['os'] = system_data['system']['primary']['controllers'][controller_key]['osname']
            super(Elevate, self).__init__(**kwargs)

            if 'api-path' in system_data['system']['primary']:
                self.log("Overriding existing utils.py path with: " + system_data['system']['primary']['api-path'])
                self.api_path = system_data['system']['primary']['api-path']
            if 'mgt-ip' in system_data['system']['primary']['controllers'][controller_key]:
                self.chassis = system_data['system']['primary']['controllers'][controller_key]['mgt-ip']
            self.model = system_data['system']['primary']['model'].upper()

        elif chassis:
            self.chassis = chassis
        else:
            raise TobyException("Missing either system_data (Workflow 1) or chassis (Workflow 2) parameter")

        if not self.chassis:
            raise TobyException("Unable to determine chassis host information! Check for valid in init yaml file.", host_obj=self)

        self.connect_info = None
        self.log("CHASSIS= " + str(self.chassis))

        sys.path.append(self.api_path)

        try:
            self.elevate = __import__('Utils3')
        except Exception as err:
            raise TobyException("Unable to import Utils.py at path " + self.api_path + ": " + str(err), host_obj=self)

        self.connect()

    def cleanup(self):
        """
        Quit Elevate Session
        """
        try:
            self.elevate.SendCommand(instruction="sys:stopCallProcessing")
            self.elevate.Quit()
        except Exception:
            pass

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

        elevate_func = getattr(self.elevate, function)
        self.log("Invoking Elevate API " + function + " with the following parameters: " + str(args))
        result = elevate_func(**args)
        self.log("Invocation of Elevate method " + function + " executed resulting in: " + str(result))
        if 'Status 0' not in result:
            raise TobyException("Invocation of Spirent Elevate function " + function + " failed with result: " + str(result), host_obj=self)

        self.log("Invocation of Elevate method " + function + " succeeded")
        return result

    def connect(self):
        """
        Connect to Elevate chassis
        """
        self.log("Attempting connection to Elevate...")

        try:
            self.elevate.ConnectToInstrument(self.chassis, 33600)
            self.log("Elevate Connection Successful")
            self.log("Stop Call Processing")
            self.elevate.SendCommand(instruction="sys:stopCallProcessing")
        except Exception as err:
            raise TobyException("Elevate Initialization Failed with ERROR: " + str(err), host_obj=self)

    def get_port_handle(self, **args):
        """
        Use Elevate object information to get port handle keys
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
    Pass-through function for Elevate method of same name to call av.py functions
    """
    if function == 'connect':
        return device.connect(**kwargs)
    elif function == 'get_port_handle':
        return device.get_port_handle(**kwargs)
    else:
        return device.invoke(function, **kwargs)
