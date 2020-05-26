"""
Spirent module providing abstracting to sth.py function within Spirent.
"""
import os
import sys
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

class Landslide(TrafficGen):
    """
    Landslide emulation class
    """
    def __init__(self, chassis=None, landslide_manager=None, system_data=None, landslide_lib_path=None, landslide_jre_path=None, landslide_tcl_bin=None):
        """
        Landslide abstraction layer for HLTAPI

        -- Workflow 1 --
        :param  system_data:  *MANDATORY* Dictionary of Spirent information
        system:
        primary:
          controllers:
            if0:
              domain: englab.juniper.net
              hostname: Systest-Landslide
              isoaddr: 47.0005.80ff.f800.0000.0108.0001.0102.5500.7000.00
              loop-ip: 10.255.7.0
              loop-ipv6: abcd::10:255:7:0
              mgt-intf-name: eth0
              mgt-ip: 10.9.4.6
              mgt-ipv6: abcd::10:9:4:6
              osname: SPIRENT
          cube:
            - COMMON-LISP::OR
            - wf-626-systest
          make: spirent
          model: spt-c100-ts
          name: Systest-Landslide
          osname: spirent
          landslide_manager: 10.4.4.42

        -- Workflow 2 --
        :param  host  *MANDATORY* FQDN/mgt-ip of of chassis
        :param  landslide_manager  *MANDATORY* landslide_manager - manager of test servers

        :return: Landslide object
        """

        self.debug = False
        self.chassis = None
        self.session_info = None
        self.intf_to_port_map = None
        self.log_dir = get_log_dir()
        atexit.register(self.cleanup)
        self.ls = None
        self.user_functions = dict()

        if landslide_lib_path and landslide_jre_path and landslide_tcl_bin:
            self.lib_path = landslide_lib_path
            self.jre_path = landslide_jre_path
            self.tcl = landslide_tcl_bin
        else:
            environment = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__), "environment.yaml")))
            self.lib_path = environment['landslide-lib-path']
            self.jre_path = environment['landslide-jre-path']
            self.tcl = environment['landslide-tcl-bin']

        if system_data:

            controller_key = list(system_data['system']['primary']['controllers'].keys())[0]

            if 'user' in system_data['system']['primary']['controllers'][controller_key]:
                self.username = system_data['system']['primary']['controllers'][controller_key]['user']
            if 'password' in system_data['system']['primary']['controllers'][controller_key]:
                self.password = system_data['system']['primary']['controllers'][controller_key]['password']

            kwargs = dict()
            kwargs['host'] = self.chassis = system_data['system']['primary']['name']
            kwargs['hostname'] = self.chassis = system_data['system']['primary']['name']
            kwargs['os'] = system_data['system']['primary']['controllers'][controller_key]['osname']
            super(Landslide, self).__init__(**kwargs)

            if 'debug' in system_data['system']['primary']:
                self.debug = system_data['system']['primary']['debug']
            if 'mgt-ip' in system_data['system']['primary']['controllers'][controller_key]:
                self.chassis = system_data['system']['primary']['controllers'][controller_key]['mgt-ip']
            self.landslide_manager = system_data['system']['primary']['landslide-manager']
        elif chassis:
            self.chassis = chassis
            self.landslide_manager = landslide_manager

        else:
            raise TobyException("Missing either system_data (Workflow 1) or chassis (Workflow 2) parameter")

        if not self.chassis:
            raise TobyException("Unable to determine chassis host information! Check for valid labserver or mgt-ip in init yaml file.")

        self.connect_info = None
        self.log("CHASSIS= " + str(self.chassis))
        cred = credentials.get_credentials(os='Landslide')
        self.username = cred['USERNAME']
        self.password = cred['PASSWORD']
        self.telnetuser = cred['TELNETUSERNAME']
        self.telnetpwd = cred['TELNETPASSWORD']

        self.wait = 1
        self.telnet_handle = None
        self.version = self._get_version()
        sys.path.append(self.lib_path)
        self._set_envs()

        #resetting sys.argv[0] is only way to get spirent htlapi logs to go to the right place
        #executable = sys.argv[0]
        #sys.argv[0] = self.log_dir
        self.ls = __import__('ls')
        #sys.argv[0] = executable
        self.log("Landslide Chassis Initialization Complete")

    def cleanup(self):
        """
        Destructor to disconnect from labserver
        """
        if self.ls:
            self.ls.logout_from_server()

    def _get_version(self):
        """
        Get Chassis OS Version of Spirent TC
        :
        :return: spirent TC version
        """
        self.log(level="DEBUG", message="Entering '_get_version'\n"+__file__)
        version = None
        try:
            self.telnet_handle = telnetlib.Telnet(self.landslide_manager)
#           self.telnet_handle.set_debuglevel(10)
#           self.telnet_handle.write(b"\n")
            time.sleep(self.wait)
            self.telnet_handle.read_until(b'login: ')
            uname = self.telnetuser + "\n"
            uname = uname.encode('ascii')
            self.telnet_handle.write(uname)
            time.sleep(self.wait)
            self.telnet_handle.read_until(b"Password: ")
            pwd = self.telnetpwd + "\n"
            pwd = pwd.encode('ascii')
            self.telnet_handle.write(pwd)
            time.sleep(self.wait)
            time.sleep(self.wait)
            self.telnet_handle.read_until(b"##>")
            cmd = "cat /usr/sms/data/tasoutput.txt | grep 'TAS started'\n"
            cmd = cmd.encode('ascii')
            self.telnet_handle.write(cmd)
            time.sleep(self.wait)
            match_results = self.telnet_handle.expect([br"\d+.\d+.\d+.\d+"])
            full_version = match_results[1].group(0).decode('ascii')
            version = full_version
            ver_re = re.compile(r'\d+.\d+.\d+(\.\d+)?')
            if ver_re.search(full_version):
                version = ver_re.search(full_version).group()
        except Exception as ex: # pylint: disable=bare-except
            #if telnet isn't listening, try ssh
            self.log(level="WARN", message="Unable to detect Landslide Chassis version use telnet due to: %s" % ex.__str__())
            try:
                ssh_handle = SshConn(host=self.landslide_manager, user=self.telnetuser, password=self.telnetpwd)
                paramiko_handle = ssh_handle.client
                paramiko_handle.send('cat /usr/sms/data/tasoutput.txt | grep "TAS started"\n')
                time.sleep(self.wait)
                response = paramiko_handle.recv(1024)
                ver_re = re.compile(r'\d+.\d+.\d+(\.\d+)?')
                if ver_re.search(str(response)):
                    version = ver_re.search(str(response)).group()
            except Exception as ex:
                self.log(level="ERROR", message="Unable to detect Landslide Chassis version using ssh connection due to: %s" % ex.__str__())

        if not version:
            self.log(level="DEBUG", message="Unable to detect Landslide Chassis version")
            raise TobyException("Unable to detect Landslide Chassis version")

        self.log('CHASSIS VERSION: ' + version)
        self.log(level="DEBUG", message="Exiting '_get_version' with return value/code :\n"+str(version))
        return version

    def _set_envs(self):
        """
        Set ENVs required for Spirent TC
        """
        self.log(level="DEBUG", message="Entering '_set_envs'\n"+__file__)

        if self.version is None:
            self._get_version()

        os.environ['LANDSLIDE_VERSION'] = self.version
        self.lib_path += "/" + self.version
        os.environ['LIBPATH'] = self.lib_path
        os.environ['JRE_PATH'] = self.jre_path
        os.environ['LS_TCL'] = self.tcl

        self.log("LANDSLIDE_VERSION= " + self.version)
        self.log("LIBPATH= " + os.environ['LIBPATH'])
        self.log("JRE_PATH= " + os.environ['JRE_PATH'])
        self.log("LS_TCL= " + os.environ['LS_TCL'])
        self.log(level="DEBUG", message="Exiting '_set_envs' with return value/code :\n None")

    def add_intf_to_port_map(self, intf_to_port_map):
        """
        Assign params intf to port map to obj
        """
        self.intf_to_port_map = intf_to_port_map

    def invoke(self, function, from_spirent_robot=False, **args):
        """
        Pass-through for sth.py functions
        """
        self.log(level="DEBUG", message="Entering 'invoke'\n"+__file__)

        # User contributed module

        landslide_func = getattr(self.ls, function)
        self.log("Landslide Invoke Parameters: " + str(args))
        result = landslide_func(**args)
        self.log("Invocation of Spirent method " + function + " resulting in: " + str(result))

        # if function != 'invoke':
        #     if result['status'] == '0':
        #         self.log("Invocation of Spirent method " + function + " failed")
        #         raise TobyException("Invocation of Spirent method " + function + " failed with result: " + str(result))
        self.log("Invocation of Spirent method " + function + " succeeded")
        self.log(level="DEBUG", message="Exiting 'invoke' with return value/code :\n"+str(result))
        return result

    def connect(self, **args):
        """
        Connect to Spirent chassis and assign port handle keys using sth.connect
        """
        self.log(level="DEBUG", message="Entering 'connect'\n"+__file__)
        self.ls.lsInit(jre_path=self.jre_path, path=self.lib_path, log_path=self.log_dir)
        connect_info = self.ls.connect(tasIp=self.landslide_manager, username=self.username, password=self.password)
        return connect_info



def invoke(device, function, **kwargs):
    """
    Pass-through function for Spirent method of same name to call sth.py functions
    """
    if function == 'connect':
        return device.connect(**kwargs)
    else:
        return device.invoke(function, **kwargs)
