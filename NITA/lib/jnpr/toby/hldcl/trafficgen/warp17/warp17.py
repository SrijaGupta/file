"""
Warp17 module providing abstracting to Warp17.py function within Warp17.
"""
import six
import atexit
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.trafficgen.warp17.Warp17api import Warp17api
from jnpr.toby.hldcl.trafficgen.trafficgen import TrafficGen
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.exception.toby_exception import TobyException

class Warp17(TrafficGen):
    """
    Warp17 emulation class
    """
    def __init__(self, chassis=None, system_data=None):
        """
        Warp17 abstraction layer for HLTAPI

        -- Workflow 1 --
        :param  system_data:  *MANDATORY* Dictionary of Warp17 information
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
                    hostname: wf-warp17chassis2
                    mgt-intf-name: mgt0
                    mgt-ip: 10.9.1.107
                    osname: IxOS
                make: warp17
                model: xgs12
                name: wf-ixchassis2
                osname: IxOS

        -- Workflow 2 --
        :param  host  *MANDATORY* FQDN/mgt-ip of of chassis


        :return: Warp17 object
        """
        self.chassis = None
        self.interfaces = None
        self.model = 'Unknown'
        self.intf_to_port_map = dict()
        self.port_to_handle_map = dict()
        self.session_info = None
        self.handle_to_port_map = None
        self.login_complete = False
        self.log_dir = get_log_dir()
        self.clientport = None
        self.serverport = None
        atexit.register(self.cleanup)
        self.username, self.password = credentials.get_credentials(os='Unix')

        self.connect_kwargs = {
            'virtual_machine':0,
            'ring_if_pairs':None,
            'dpdk_dev_bind_path':None,
            'host_name':"localhost",
            'ucb_pool_sz':0,
            'tcb_pool_sz':0,
            'lcores':None
        }

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
            super(Warp17, self).__init__(**kwargs)

            if 'mgt-ip' in system_data['system']['primary']['controllers'][controller_key]:
                self.chassis = system_data['system']['primary']['controllers'][controller_key]['mgt-ip']
            self.model = system_data['system']['primary']['model'].upper()

            warp17_options_str = system_data['system']['primary']['warp17']
            if warp17_options_str == 'enable':
                t.log(level="INFO", message="Using default warp17 options")
            else:
                option_list = warp17_options_str.split(':')
                for option in option_list:
                    key, value = option.split('=')
                    if key and value and key in self.connect_kwargs:
                        self.connect_kwargs[key] = value

        elif chassis:
            self.chassis = chassis
        else:
            raise TobyException("Missing either system_data (Workflow 1) or chassis (Workflow 2) parameter")

        if not self.chassis:
            raise TobyException("Unable to determine chassis host information! Check for valid in init yaml file.", host_obj=self)

        self.connect_info = None
        self.log("CHASSIS= " + str(self.chassis))

        self.warp17 = Warp17api(server_name=self.chassis) # pylint: disable=import-error

    def cleanup(self):
        """
        Logout from Warp17 device
        """
        self.warp17.cleanup_warp()
        self.log(level="INFO", message="Cleaning up Warp17")

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

    def invoke(self, method, **args):
        """
        Pass-through for Warp17.py methods
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

        warp17_func = getattr(self.warp17, method)
        self.log("Invoking Warp17 API " + method + " with the following parameters: " + str(args))
        result = warp17_func(**args)
        self.log("Invocation of Warp17 method " + method + " executed resulting in: " + str(result))

        if not result:
            raise TobyException("Invocation of Warp17 method " + method + " failed with result: " + str(result), host_obj=self)
        self.log("Invocation of Warp17 method " + method + " succeeded")
        return result

    def connect(self, **args): # pylint: disable=unused-argument
        """
        Connect to Warp17 chassis and assign port handle keys using warp17.connect
        """
        port_list = []
        for intf in self.interfaces:
            port_list.append(self.interfaces[intf]['name'])
        self.log("Attempting connection to Warp17 with parameters " + str(self.connect_kwargs))
        self.warp17.connect(port_list=port_list, **self.connect_kwargs)


    def get_port_handle(self, **args):
        """
        Use Warp17 object information to get port handle keys
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
        return None

def invoke(device, function, **kwargs):
    """
    Pass-through function for Warp17 method of same name to call Warp17.py functions
    """
    if function == 'connect':
        return device.connect(**kwargs)
    elif function == 'get_port_handle':
        return device.get_port_handle(**kwargs)
    return device.invoke(function, **kwargs)
