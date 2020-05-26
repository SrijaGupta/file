"""
Breakingpoint module providing connectivity to Breakingpoint chassis
"""
import os
import sys
import re
import time
import atexit
import ruamel.yaml as yaml
from jnpr.toby.hldcl.trafficgen.trafficgen import TrafficGen
from jnpr.toby.hldcl.connectors.sshconn import SshConn
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.exception.toby_exception import TobyException


class Breakingpoint(TrafficGen):
    """
    Breaking Point emulation class
    """
    def __init__(self, system_data):
        """
        Breaking Point abstraction layer

        :param  system_data  *MANDATORY* Dictionary of Breaking Point information
          Example:
          system_data =
            system:
              primary:
                controllers:
                  unknown:
                    domain: englab.juniper.net
                    hostname: wf-bpchassis2
                    mgt-intf-name: mgt0
                    mgt-ip: 10.9.1.111
                    osname: BreakingPoint
                make: breaking point
                model: bps123
                name: wf-bpchassis2
                osname: breaking point


        :return: breakingpoint object
        """

        self.bps = None
        self.port_list = None
        self.breakingpoint_version = None
        self.intf_to_port_map = None
        self.debug = False
        self.wait = 1
        self.group = 1
        atexit.register(self.cleanup)

        self.username, self.password = credentials.get_credentials(os='Breakingpoint')

        environment = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__), "environment.yaml")))
        self.lib_path = environment['breakingpoint-lib-path']

        controller_key = list(system_data['system']['primary']['controllers'].keys())[0]
        self.chassis = system_data['system']['primary']['controllers'][
            controller_key]['mgt-ip']

        if system_data['system']['primary']['controllers'][controller_key]['user']:
            self.username = system_data['system']['primary']['controllers'][controller_key]['user']
        if system_data['system']['primary']['controllers'][controller_key]['password']:
            self.password = system_data['system']['primary']['controllers'][controller_key]['password']
        if 'debug' in system_data['system']['primary']:
            self.debug = True
        if 'group' in system_data['system']['primary']:
            try:
                self.group = int(system_data['system']['primary']['group'])
                if self.group < 1 or self.group > 12:
                    raise TobyException("Illegal value for fv-breakingpoint-group (" + \
                                        str(system_data['system']['primary']['group']) + "). Should be an integer 1-12.")

            except Exception:
                raise TobyException("Illegal value for fv-breakingpoint-group (" +
                                    str(system_data['system']['primary']['group']) + "). Should be an integer 1-12.")

        kwargs = dict()
        kwargs['host'] = self.hostname = system_data['system']['primary']['name']
        kwargs['hostname'] = self.hostname = system_data['system']['primary']['name']
        kwargs['os'] = system_data['system']['primary']['controllers'][controller_key]['osname']
        kwargs['user'] = self.username
        kwargs['password'] = self.password
        super(Breakingpoint, self).__init__(**kwargs)

        if not self.username:
            raise TobyException("Username and password cannot be determined", host_obj=self)

        self.log("CHASSIS= " + self.chassis)

        self.version = self._get_version()
        self.lib_version = self._get_lib_version()
        self._set_envs()
        from bpsRest import BPS # pylint: disable=import-error

        self.bps = BPS(self.chassis, self.username, self.password)

    def _get_version(self):
        """
        Get Chassis OS Version of Breakingpoint TC
        :
        :return: breakingpoint chassisversion
        """
        version = None
        try:
            ssh_handle = SshConn(host=self.chassis, user=self.username, password=self.password)
            paramiko_handle = ssh_handle.client
            # this is for version 8.40 and above, for lower versions the command is harmless
            paramiko_handle.send('enter bps\n')
            time.sleep(4)
            paramiko_handle.send('version\n')
            ## increase waiting time from 1s to 4s, otherwise it cannot get the output
            time.sleep(4)
            response = paramiko_handle.recv(1024)
            ver_re = re.compile(r'version:(\d+\.\d+\.\d+)')
            if ver_re.search(str(response)):
                version = ver_re.search(str(response)).group(1)
        except Exception as ex:
            self.log(level="ERROR", message="Toby was not able to detect Breakingpoint version info using ssh connection due to: %s" % ex.__str__())
        if not version:
            raise TobyException("Unable to detect Breakingpoint version", host_obj=self)

        self.log('CHASSIS VERSION: ' + version)

        self.major_version = re.search(r'^\d+', version).group(0)
        if not self.major_version:
            raise TobyException("Unable to derive major and minor version from " + version, host_obj=self)

        if float(self.major_version) < 8.0:
            raise TobyException("Unsupported version " + self.major_version + ". Minimum version supported: 8.0", host_obj=self)
        return version

    def _set_envs(self):
        """
        Set ENVs required for Breakingpoint
        """
        lib_path = self.lib_path + '/' + self.lib_version
        sys.path.append(lib_path)

    def _get_lib_version(self):
        """
        Needed to determine which Breakingpoint library folder to use.
        """
        breakingpoint_lib_ver = None
        try:
            best_match = None
            breakingpoint_lib_vers = list(
                filter(lambda x: os.path.isdir(os.path.join(self.lib_path, x)), os.listdir(self.lib_path)))
            for possible_lib_ver in breakingpoint_lib_vers:
                if re.search(r'\d+\.\d+\.\d+', possible_lib_ver):
                    if possible_lib_ver == self.version:
                        breakingpoint_lib_ver = possible_lib_ver
                        break
                    elif re.search('^' + self.major_version + '.', possible_lib_ver):
                        best_match = possible_lib_ver
            if best_match and not breakingpoint_lib_ver:
                breakingpoint_lib_ver = best_match
        except:
            raise TobyException("Unable to find appropriate Breakingpoint lib version in " + self.lib_path + \
                                " for Breakingpoint version " + self.version, host_obj=self)

        if not breakingpoint_lib_ver:
            raise TobyException("Unable to find appropriate Breakingpoint lib version in " + self.lib_path + \
                                " for Breakingpoint version " + self.version, host_obj=self)

        self.log("BREAKINGPOINT LIB AVAILABLE= " + str(breakingpoint_lib_ver))
        return breakingpoint_lib_ver

    def add_intf_to_port_map(self, intf_to_port_map):
        """
        Add attribute to breakingpoint object which contains params intf
        to port mappings
        """
        self.intf_to_port_map = intf_to_port_map

    def invoke(self, method, **args):
        """
        Pass-through for ixnetwork.py functions (ixnetwork.py? or
        something else?)
        """
        breakingpoint_func = getattr(self.bps, method)
        self.log("Invoking " + method + " with parameters " + str(args))
        if self.debug:
            args['enableRequestPrints'] = True
        result = breakingpoint_func(**args)
        if result is False:
            raise TobyException("Invocation of Breakingpoint method " +  method + " failed", host_obj=self)
        else:
            self.log("Invocation of Breakingpoint method " + method + " succeeded with result: " + str(result))
            return result

    def connect(self, port_list, reset=1, **kwargs): # pylint: disable=unused-argument
        """
        Connect to Breakingpoint chassis

        :param port_list (*REQUIRED): port list , ex: '1/9 1/10 1/11'
        :return: breakingpoint connection object
        """
        self.log('Attempting to connect to Breakingpoint...')
        if not port_list:
            raise TobyException("Missing port_list parameter", host_obj=self)
        self.port_list = port_list

        try:
            self.bps.login()
        except Exception as error:
            raise TobyException("Error in 'bpsRest.py': "+str(error))

        sorted_ports = dict()
        for port in port_list:
            slot, num = port.split('/')
            sort_key = '{:03}'.format(int(slot)) + '{:03}'.format(int(num))
            sorted_ports[sort_key] = (slot, num)

        self.debug = True
        for sort_key in sorted(sorted_ports):
            slot, num = sorted_ports[sort_key]
            reserve_status = self.bps.reservePorts(
                slot=slot, portList=[num], group=self.group, force=True,
                enableRequestPrints=self.debug)
            self.log("Reserve Status for port(s) " + str(num) + ": " + str(reserve_status))

    def cleanup(self):
        """
        Remove reservation on ports and logout
        """
        try:
            if self.port_list:
                for port in self.port_list:
                    slot, num = port.split("/")
                    self.bps.unreservePorts(slot=slot, portList=[num])
            if self.bps:
                self.bps.logout()
        except Exception:
            pass


def invoke(device, function, **kwargs):
    """
    Pass-through function for Breakingpoint
    """
    return device.invoke(function, **kwargs)
