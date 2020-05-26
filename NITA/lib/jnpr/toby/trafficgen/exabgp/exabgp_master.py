#!/usr/bin/python3
"""
This module can be used to pump multiple BGP routes and can add as many networks
as required between host and router

__author__ = ['Manoj Kumar V', 'Sandeep Rai']
__contact__ = 'vmanoj@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'
"""
import re
import ipaddress

class exabgp_master(object):
    """
    Class for sending BGP routes from host to router

    Robot Example for importing::

        Library    exabgp_master.py   path_loc=/tmp

    | This class contains methods which create exabgp '.ini' files, validates the path location ,
    | Creates exabgp files for ipv4 and ipv6 and can simulate the BGP routes learnt inside router
    | from host machine.


    Sample Robot file with exabgp APIs::

        *** Keywords ***
        Global
          Initialize

        *** Test Cases ***

        Testcase Exabgp - Pumping the BGP routes from host to router
            ${check}=    Check Exabgp And Path Availability    device=${dh_h0}
            Should Be True     '${check}' == 'True'
            Cleanup Exabgp    device=${dh_h0}
            Create Exabgp Files   device=${dh_h0}  base_local_ip=20.0.0.2  base_remote_ip=20.0.0.1\
            base_local_as=200    remote_as=100    base_rt_prefix=70.0.0.1/32    routes_per_peer=50\
            local_ip_step=0.0.1.0
            Start Exabgp Routing   device=${dh_h0}
            Stop Exabgp Routing   device=${dh_h0}

    Please refer to documentation of corresponding APIs for more details.

        :param string path_loc:
            **OPTIONAL**  Path Location has to be set using either this variable\
                or else by default it will be '/tmp'
    """
    def __init__(self, path_loc="/tmp"):
        """
        Constructor to initialize the path where exabgp files will be created.
        By default it will create exabgp '.ini' extension files on '/tmp' path.

        :param string path_loc:
            **OPTIONAL**  Path Location has to be set using either this variable\
                or else by default it will be '/tmp'

        Example::

            python:
                exabgp_master.ExabgpMaster()
            Robot:
                Library    exabgp_master.py
                    Or
                Library    exabgp_master.py    path_loc=/homes/xxxx/yyyy
                    Or
                Library    exabgp_master.py     /xxxx/yyyy
        """
        self._path_loc = path_loc

    def stop_exabgp_routing(self, device=None):
        """
        To stop exabgp routing

        :param obj device
          **REQUIRED** linux device handle is mandatory

        :return: None if all command executed correctly else raises an excpetion

        :rtype: None or exception

        Example::

            python:
                stop_exabgp_routing(device=linux)
            Robot:
                Stop Exabgp Routing    device=${linux}

        """
        if device is None:
            raise ValueError("device is mandatory argument")
        device.shell(command="cd %s"%self._path_loc)
        device.shell(command="pkill -f exabgp")


    def start_exabgp_routing(self, device=None):
        """
        To start exbgp routing

        :param obj device
          **REQUIRED** linux device handle is mandatory

        :return: None if all command executed correctly else raises an excpetion

        :rtype: None or exception

        Example::

            python:
                start_exabgp_routing(device=linux)
            Robot:
                Start Exabgp Routing    device=${linux}
        """
        if device is None:
            raise ValueError("device is mandatory argument")
        #device.shell(command="cd /tmp")
        device.shell(command="cd %s"%self._path_loc)
        device.shell(command="source source_exabgp &")


    def cleanup_exabgp(self, device=None):
        """
        cleanup exabgp sessions and files which were created. This is useful pre and post test

        :param obj device
          **REQUIRED** linux device handle is mandatory

        :return: None if all command executed correctly else raises an excpetion

        :rtype: None or exception

        Example::

            python:
                cleanup_exabgp(device=linux)
            Robot:
                Cleanup Exabgp    device=${linux}
        """
        if device is None:
            raise ValueError("device is mandatory argument")
        device.shell(command="pkill exabgp")
        #device.shell(command="cd /tmp")
        device.shell(command="cd %s"%self._path_loc)
        device.shell(command="rm -f test_exabgp*")
        device.shell(command="rm -f source_exabgp")

    def create_generic_exabgp_file(self, device=None):
        """
        This method will create generic_exabgp.py file in location /root and it will called \
        by method create_exabgp_files() present in the same class.
        """
        python_file = """import pdb
from sys import stdout
from time import sleep
import argparse
import ipaddress

parser = argparse.ArgumentParser()
parser.add_argument(\\"-b\\", \\"--base_network\\", help = \\"parse the base network in x.x.x.x/y format\\")
parser.add_argument(\\"-c\\", \\"--count\\", help = \\"parse the number of networks to increment\\")
parser.add_argument(\\"-nh\\", \\"--next_hop\\", help = \\"parse the desired nexthop would be defaulted to self if not parsed\\")
parser.add_argument(\\"-r\\", \\"--rate\\", help = \\"parse the rate at which the routes has to be pushed would be defaulted to 200 if not parsed\\")
args = parser.parse_args()


if args.rate:
    rate = int(args.rate)
else:
    rate = 200

if args.next_hop:
    next_hop = args.next_hop
else:
    next_hop = 'self'

base_net = ipaddress.ip_interface(args.base_network)
count = int(args.count)
base_net = base_net.network
net_step = base_net.num_addresses
base_ip,mask = str(base_net).split(\\"/\\")
route_count = rate

#Iterate through all desired routes and advertise them
for num in range(0,count):
    if route_count % rate == 0:
        sleep(1)
    message = 'announce route ' + str(base_ip) + '/' + mask + ' next-hop ' + next_hop
    stdout.write( message + '\\\\n')
    stdout.flush()
    base_ip = ipaddress.ip_address(base_ip) + net_step
    route_count += 1


#Loop endlessly to allow ExaBGP to continue running
while True:
    sleep(1)"""
        device.shell(command="cd /root")
        response_script = device.shell(command="ls -l /root/generic_exabgp.py")
        match_script = re.search(r'.*generic_exabgp.py.*No such file or directory',\
 response_script.response())
        if match_script:
            for line in python_file.splitlines():
                device.shell(command="echo \"%s\" >> generic_exabgp.py"%line)
        device.shell(command="chmod 777 generic_exabgp.py")

    def check_exabgp_and_path_availability(self, device=None):
        """ check exabgp tool presence and verifies whether path is applicable for creating\
         exabgp files

        | Check if exabgp package is installed or not in the linux host
        | and also verifies whether path where exabgp files will be created
        | does exists or not. If not then, it will try to create that path location.

        :param obj device
            **REQUIRED** linux device handle is mandatory

        :return: True only if exabgp is installed and path location is valid
             to save Exabgp .ini files else False or exception if device
             handle not passed

        :rtype: bool or exception

        Example::

            python:
                check_exabgp_and_path_availability(device=linux)
            Robot:
                Check Exabgp And Path Availability    device=${linux}
        """
        if device is None:
            raise ValueError("device is mandatory argument")
        device.shell(command="cd %s"%self._path_loc)
        response_path = device.shell(command="cd %s"%self._path_loc)
        match_path = re.search('No such file or directory', response_path.response())
        if match_path:
            device.log(level='INFO', message='Directory doesn\'t Exists thus creating the \
Directory')
            create_dir = device.shell(command="mkdir -p %s"%self._path_loc)
            check_dir = re.search('Permission denied', create_dir.response())
            if check_dir:
                device.log(level='ERROR', message='Directory path : %s cannot \
be created for the creation of exabgp files'%self._path_loc)
                return False
            else:
                device.log(level='INFO', message='Directory path : %s has \
been created for the creation of exabgp files'%self._path_loc)
        else:
            device.log(level='INFO', message='Directory Exists')

        response_exabgp = device.shell(command="whereis exabgp")
        match_exabgp = re.search('exabgp ' + '/' + '.*', response_exabgp.response())
        if match_exabgp:
            device.log(level='INFO', message='Exabgp package is installed')
        else:
            device.log(level='ERROR', message='Exabgp is not installed on the linux \
box do \"pip install exabgp\"')
            return False
        return True


    def create_exabgp_files(self, device=None, **kwargs):
        """
        Create all the exabgp files in the linux box.
        | This routine creates config files based on the number of peers parsed in the
        | arguments and a batch file.
        | The batch file consists of list of commands to bring up all the peers to the router.
        | It is the responsibility of the user to make sure all local-ips and
        | remote-ips parsed are reachable.

        :param obj device
            **REQUIRED** device handle to the linux host
        :param string peer_count
            **OPTIONAL** number of peers to bring up will be defaulted to 1 if not parsed
        :param base_local_ip
            **REQUIRED** base local ip of the linux host other peers will be incremented\
 based on local_ip_step value parsed
        :param string base_router_id
            **OPTIONAL** base_router_id of the linux host will be defaulted to\
 base_local_ip if not parsed
        :param string local_ip_step
            **OPTIONAL** value to increment local-ips of the linux host will be defaulted \
to 0.0.1.0 for v4 and 0:0:0:0:1:0:0:0 for v6
        :param string base_remote_ip
            **REQUIRED** IP address of first peer on the router side
        :param string remote_ip_step
            **OPTIONAL** value to increment ips on the router side, will be defaulted \
to 0.0.1.0 for v4 and 0:0:0:0:1:0:0:0 for v6
        :param string base_local_as
            **REQUIRED** AS of first neighbor on linux host
        :param string local_as_step
            **OPTIONAL** value to increment ASs on the linux side will be defaulted to 1 \
if not parsed
        :param string remote_as
            **REQUIRED** AS on the router side
        :param string base_rt_prefix
            **REQUIRED** first route to push format should be in x.x.x.x/y for v4 x::x/y for v6
        :param string routes_per_peer
            **OPTIONAL** number of routes to push per peer will be defaulted to 200 if not parsed
        :param string rt_rate
            **OPTIONAL** rate at which the routes will be pushed will be \
defaulted to 100 if not parsed

        :return: None if all command executed correctly else raises an excpetion

        :rtype: None or exception

        Example::

            python:
                create_exabgp_files(device=linux, peer_count=10, base_local_ip=20.0.0.2, \
base_remote_ip=20.0.0.1, local_ip_step=0.0.1.0,remote_ip_step=0.0.1.0, base_local_as=65001,\
local_as_step=1, remote_as=65000,
base_rt_prefix=100.0.0.0/24,
                  routes_per_peer=100, rt_rate=1000)
            Robot:
                Create Exabgp Files  device=${linux}  peer_count=10  base_local_ip=20.0.0.2\
    base_remote_ip=20.0.0.1   local_ip_step=0.0.1.0   remote_ip_step=0.0.1.0   \
base_local_as=65001    local_as_step=1    remote_as=65000   base_rt_prefix=100.0.0.0/24	 \
routes_per_peer=100	rt_rate=1000
        """
        if device is None:
            raise ValueError("Device handle is a mandatory Argument")
        #Set arguments to default values if not set
        peer_count = int(kwargs.get("peer_count", 1))
        base_local_ip = kwargs.get("base_local_ip", None)
        base_router_id = kwargs.get("base_router_id", base_local_ip)
        local_ip_step = kwargs.get("local_ip_step", None)
        base_remote_ip = kwargs.get("base_remote_ip", None)
        remote_ip_step = kwargs.get("remote_ip_step", None)
        base_local_as = kwargs.get("base_local_as", None)
        local_as_step = int(kwargs.get("local_as_step", 1))
        remote_as = kwargs.get("remote_as", None)
        base_rt_prefix = kwargs.get("base_rt_prefix", None)
        routes_per_peer = int(kwargs.get("routes_per_peer", 1000))
        rt_rate = int(kwargs.get("rt_rate", 200))
        if base_local_ip is None:
            raise KeyError('base_local_ip is mandatory argument')
        else:
            bgp_version = ipaddress.ip_address(base_local_ip).version
        if base_remote_ip is None:
            raise KeyError('base_remote_ip is mandatory argument')
        if base_local_as is None:
            raise KeyError('base_local_as is mandatory argument')
        if remote_as is None:
            raise KeyError('remote_as is mandatory argument')
        if base_rt_prefix is None:
            raise KeyError('base_rt_prefix is mandatory argument')
        if local_ip_step is None:
            if "6" in str(bgp_version):
                # earlier default = 0:0:0:0:1:0:0:0
                local_ip_step = '0:0:0:0:0:0:1:0'
            else:
                local_ip_step = '0.0.1.0'
        if remote_ip_step is None:
            if "6" in str(bgp_version):
                remote_ip_step = '0:0:0:0:0:0:1:0'
            else:
                remote_ip_step = '0.0.1.0'
        #Navigate to /tmp directory in the linux machine
        #device.shell(command="cd /tmp")
        base_local_as = int(base_local_as)
        device.shell(command="cd %s"%self._path_loc)
        #Convert all ip addresses to the required format
        base_local_ip = ipaddress.ip_address(str(base_local_ip))
        base_remote_ip = ipaddress.ip_address(str(base_remote_ip))
        base_router_id = ipaddress.ip_address(str(base_router_id))
        local_ip_step = ipaddress.ip_address(str(local_ip_step))
        remote_ip_step = ipaddress.ip_address(str(remote_ip_step))
        rt_prefix = ipaddress.ip_network(str(base_rt_prefix))
        #Create all the required files in /tmp directory based on the argumnets parsed
        batch_file_string = "\n"
        router_id = base_router_id
        local_ip = base_local_ip
        remote_ip = base_remote_ip
        local_as = base_local_as
        for peer_index in range(1, peer_count+1):
            exabgp_file_name = 'test_exabgp_v' + str(bgp_version) + '_' + str(peer_index) + '.ini'
            batch_file_string += 'env exabgp.daemon.user=root exabgp ./' + \
exabgp_file_name + '&' + '\n'
            conf_file_string = 'group test_exabgp' + str(peer_index) + ' {\n'
            conf_file_string += ' '*2 + 'router-id ' + str(router_id) + ';\n'
            conf_file_string += ' '*2 + 'neighbor ' + str(remote_ip) + ' {\n'
            conf_file_string += ' '*4 + 'local-address ' + str(local_ip) + ';\n'
            conf_file_string += ' '*4 + 'local-as ' + str(local_as) + ';\n'
            conf_file_string += ' '*4 + 'peer-as ' + str(remote_as) + ';\n' + ' '*4 + '}\n'
            conf_file_string += ' '*2 + 'process add-routes {\n'
            conf_file_string += ' '*4 + 'run /usr/bin/python3 /root/generic_exabgp.py -b ' + \
str(rt_prefix) + ' -c ' + str(routes_per_peer) + ' -r ' + str(rt_rate) + ';\n'
            conf_file_string += ' '*2 + '}\n}'
            #Write the sting into config file of exabgp
            cmd = 'echo ' + '\"' + conf_file_string + '\"' + ' > ' + exabgp_file_name
            device.shell(command=cmd)
            #Increment all variables as required
            router_id += int(local_ip_step)
            local_ip += int(local_ip_step)
            remote_ip += int(remote_ip_step)
            local_as += local_as_step
            ip_add, mask = str(rt_prefix).split("/")
            hosts_per_net = 0
            if "6" in str(bgp_version):
                hosts_per_net = len(list(rt_prefix.hosts())) + 1
            else:
                hosts_per_net = len(list(rt_prefix.hosts())) + 2
            increment_num = hosts_per_net * routes_per_peer
            next_rt = ipaddress.ip_address(ip_add) + increment_num
            rt_prefix = ipaddress.ip_network(str(next_rt) + '/' + str(mask))
        #Creating generic_exabgp.py if not present in path /root/
        self.create_generic_exabgp_file(device=device)
        device.shell(command="cd %s"%self._path_loc)
        #Create the batch file
        source_cmd = 'echo ' + '\"' + batch_file_string + '\"' + ' >> source_exabgp'
        device.shell(command=source_cmd)
        device.shell(command="chmod 777 source_exabgp")
        device.shell(command="chmod 777 test_exabgp*")
