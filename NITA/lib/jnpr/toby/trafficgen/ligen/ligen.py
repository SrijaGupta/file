"""Module contains the ligen class for Linux traffic generator methods"""
# pylint: disable=undefined-variable
__author__ = ['Sumanth Inabathini', 'Sandeep Maraka']
__contact__ = 'isumanth@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import ast
from optparse import Values
import time
import importlib.machinery
import paramiko
from scp import SCPClient

from jnpr.toby.utils.linux import linux_network_config
from jnpr.toby.utils.linux import linux_tool
from jnpr.toby.utils import iputils
from jnpr.toby.frameworkDefaults import credentials
from jnpr.toby.services import utils

class ligen(object):
    """Class for generating traffic using Linux devices

    Robot Example for importing::

        Library   ligen.py   tar_file_name=ligen_setup.tar.gz  \
                  tar_file_location=/volume/labtools/lib/Testsuites/ligen/  WITH NAME   hLg

    | LiGen package file is committed to CVS at
    | /volume/labtools/lib/Testsuites/ligen/ligen_setup.tar.gz.
    | It is strongly recommended to use this file only.
    | This is specified using 'tar_file_name' and 'tar_file_location'.

    |The hLg.Init need to be called in every robot testcase to have the ligen_dmn prompt

    Sample Robot file with LiGen APIs::

        *** Keywords ***
        Global
          Initialize

        *** Variables ***
        @{port_pair}    h0:h0r0_1_if  h1:h1r0_1_if
        @{iplist}    112.1.0.0/16

        *** Test Cases ***

        Testcase Traffic test - Traffic on linux machine
            hLg.Init  port_pair=@{port_pair}
            hLg.Configure Interfaces  clnt_port_ip=20.1.1.2/24   srvr_port_ip=30.1.1.2/24  \
                                      clnt_gw_ip=20.1.1.1/24   srvr_gw_ip=30.1.1.1/24
            hLg.Add Static Route  ip_list=@{iplist}  device=server
            hLg.Configure Traffic   ip_dst_addr=30.1.1.2   num_trans=1   data_length=64 \
            duration=10s   bidir=1   wait_before_stop=0   ip_src_addr=1.1.1.1   protocol=Udp  \
             num_src_ips=10   num_ports_per_src_ip=10   dst_port=12000   src_port=10000
            hLg.Start Traffic
            hLg.Stop Traffic
            hLg.Get Sessions
            hLg.Verify Statistics
            hLg.Disconnect

    Please refer to documentation of corresponding APIs for more details.

    :param string tar_file_name:
        **REQUIRED** Tar file name of the ligen package.
        This should be ligen_setup.tar.gz unless you want to use your locally modified package.

    :param string tar_file_location:
        **REQUIRED** Location of the ligen package tar file.
        This should be /volume/labtools/lib/Testsuites/ligen/ unless you want to use your locally \
         modified package.


    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, **kwargs):
        """Constructor method to update the instance of ligen class."""

        self.options = {
            'all': {
                'client': {
                    'ip_src_addr': None,
                    'ip_dst_addr': None,
                    'src_port': 10000,
                    'dst_port': 20000,
                    'num_src_ips': 1,
                    'num_ports_per_src_ip': 1,
                    'num_trans': 1,
                    'duration': '0s',
                    'data_length': 64,
                    'bidir': 1,
                    'wait_before_stop': 0,
                    'pps': 2,
                    'tos': 0,
                    'edit': None,
                    'num_dst_ips': 1,
                },
                'server': {
                    'tos': 0,
                    'edit':'',
                    'num_dst_ips': 1,
                }
            },
            'Udp': {
                'client': {
                },
                'server': {
                }
            },
            'Tcp': {
                'client': {
                },
                'server': {
                }
            },
            'Tcpfast': {
                'client': {
                },
                'server': {
                }
            },
            'HttpBase': {
                'client': {
                    'url': '/5000bytes_data_file.bin',
                    'method': 'GET',
                    'user_name': 'user',
                    'passwd': '12345',
                    'multi_auth': 0,
                    'user_hdr': "",
                    'ul_file': None,
                    'key_file': None,
                    'cert_file': 'client.pem'
                },
                'server': {
                }
            },
            'HttpStateful': {
                'client': {
                    'url': '/5000bytes_data_file.bin',
                    'method': 'GET',
                    'user_name': 'user',
                    'passwd': '12345',
                    'multi_auth': 0,
                    'user_hdr': "",
                    'ul_file': None,
                    'key_file': None,
                    'cert_file': 'client.pem'
                },
                'server': {
                }
            },
            'Tftpy': {
                'client': {
                    'dl_file': None,
                    'ul_file': None
                },
                'server': {
                    'root_dir' : '~regress/ligen/root_dir'
                }
            },
            'Dns': {
                'client': {
                },
                'server': {
                }
            },
            'Dnsudp': {
                'client': {
                },
                'server': {
                }
            },
            'Dnstcp': {
                'client': {
                },
                'server': {
                }
            },
            'Ftp': {
                'client': {
                    'user_name': 'user',
                    'passwd': '12345',
                    'dl_file': None,
                    'ul_file': None,
                    'active_mode': 0,
                    'multi_auth': 0,
                    'cmd': ""
                },
                'server': {
                    'root_dir' :  '~regress/ligen/root_dir',
                    'user_name': 'user',
                    'passwd': '12345'
                }
            },
            'HttpsBase': {
                'client': {
                    'url': '/5000bytes_data_file.bin',
                    'method': 'GET',
                    'user_name': 'user',
                    'passwd': '12345',
                    'multi_auth': 0,
                    'user_hdr': "",
                    'key_file': None,
                    'cert_file': '~regress/ligen/client.pem',
                    'ul_file': None
                },
                'server': {
                    'key_file': None,
                    'cert_file': '~regress/ligen/server.pem',
                    'ciphers': ''
                }
            },
            'HttpsStateful': {
                'client': {
                    'url': '/5000bytes_data_file.bin',
                    'method': 'GET',
                    'user_name': 'user',
                    'passwd': '12345',
                    'multi_auth': 0,
                    'user_hdr': "",
                    'key_file': None,
                    'cert_file': '~regress/ligen/client.pem',
                    'ul_file': None
                },
                'server': {
                    'key_file': None,
                    'cert_file': '~regress/ligen/server.pem',
                    'ciphers': ''
                }
            },
            'Smtp': {
                'client': {
                    'email': None,
                    'ul_file': None,
                },
                'server': {
                }
            },
            'Icmp': {
                'client': {
                },
                'server': {
                }
            },
            'Rtsp': {
                'client': {
                },
                'server': {
                }
            },
            'RtspTcp': {
                'client': {
                },
                'server': {
                }
            },
            'Ntp': {
                'client': {
                },
                'server': {
                }
            },
            'Ssh': {
                'client': {
                },
                'server': {
                }
            },
            'Sftp': {
                'client': {
                    'user_name': 'user',
                    'passwd': '12345',
                    'ul_file': None,
                    'dl_file': None
                },
                'server': {
                    'dl_file': None,
                    'ul_file': None
                }
            },
            'Sip': {
                'client': {
                },
                'server': {
                }
            },
            'Telnet': {
                'client': {
                    'user_name': 'user',
                    'passwd': '12345',
                    'multi_auth': 0
                },
                'server': {
                }
            },
            'Pop3': {
                'client': {
                    'dl_file': None,
                    'user_name': 'user',
                    'passwd': '12345',
                    'ul_file': None
                },
                'server': {
                    'dl_file': None,
                    'user_name': 'user',
                    'passwd': '12345',
                    'email' : "",
                    'ul_file': None
                }
            },
            'Imap4': {
                'client': {
                    'user_name': 'user',
                    'passwd': '12345',
                    'ul_file': None,
                    'dl_file': None,
                    'key_file': None,
                    'cert_file': '~regress/ligen/client.pem',
                    'ciphers': '',
                    'ul_file': None,
                    'email': None
                },
                'server': {
                    'user_name': 'user',
                    'passwd': '12345',
                    'ul_file': None,
                    'dl_file': None,
                    'key_file': None,
                    'cert_file': '~regress/ligen/server.pem',
                    'ciphers': '',
                    'email': None
                }
            },
            'Scapy': {
                'client': {
                },
                'server': {
                }
            },
            'Pcpc': {
                'client': {
                    'map_proto': 17,
                    'map_lifetime': 3000,
                    'map_num_ports_per_int_ip': 1,
                    'map_num_int_ips': 1,
                    'client_port': 0,
                    'map_option_list': '0x12',
                },
                'server': {
                }
            },
            'Pptp' : {
                'client' : {
                    'num_tunnels' : 1,
                    'interface_tunnel_endpoint': None
                },
                'server' : {
                    'num_tunnels' : 1,
                    'interface_tunnel_endpoint': None
                }
            }
        }


        self.connect = True
        self.dmn_file = '~regress/ligen/ligen_dmn.py'
        self.dmn_cmd = 'python3 {}'.format(self.dmn_file)
        self.dmn_prompt = 'daemon# '

        # Status variables
        self.is_connected = self.is_traffic_configured = self.is_intf_configured = False
        self.is_pcp_configured = False
        self.is_running = False

        self.port_pair = None
        self.stats = {}
        self.clnt_gw_ip = None
        self.srvr_gw_ip = None
        self.clnt_gw_ipv6 = None
        self.srvr_gw_ipv6 = None
        self.clnt_port_ip = None
        self.srvr_port_ip = None
        self.clnt_port_ipv6 = None
        self.srvr_port_ipv6 = None
        self.srvr_port = None
        self.clnt_port = None

        self.sessions = None

        self.srvr_hndl = None
        self.clnt_hndl = None
        self.clnt_node_hndl = None
        self.srvr_node_hndl = None
        self.srvr_prompt = None
        self.clnt_prompt = None
        self.clnt_res_name = None
        self.srvr_res_name = None
        self.clnt_tag = None
        self.srvr_tag = None
        self.clnt_port_ip_netmask = None
        self.srvr_port_ip_netmask = None
        self.clnt_port_ipv6_netmask = None
        self.srvr_port_ipv6_netmask = None
        self.clnt_name = None
        self.srvr_name = None
        self.clnt_port_name = None
        self.srvr_port_name = None
        self.ip_dst_addr = None

        #self.clnt_opts = {}
        #self.srvr_opts = {}
        #self.pcp_opts = {}
        self.clnt_opts_list = []
        self.srvr_opts_list = []
        self.pcp_opts_list = []

        self.msg = ''
        self.sess_cnt = None
        self.tar_file_location = None
        self.tar_file_name = None

        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.resource = {}
        self.intf_data = {}
        self.paramiko = paramiko
        self.scp_clnt = SCPClient
        self.base_setup = False
        self.dev_pkg_ver = None
        self.linux_tool_hndl = linux_tool.linux_tool()
        self.scp = None
        self.hndl = None
        self.log = utils.log

        super().__init__()

    def init(self, port_pair=None, update_pkg=True):
        """Initialize the variables and do basic configuration on Linux devices

        This sets up/upgrades linux devices, if required, and starts LiGen daemons.

        | **Setup/Upgrade**
        | If devices do not have LiGen packages already installed, they will be set up.
        | If devices are having an older version of the LiGen package,
        | they will be upgraded to the latest version. (LiGen package should be mentioned
        | using tar_file_name, tar_file_location during LiGen Class instantiation)
        | Setup/upgrade process is controlled by 'update_pkg' flag which is enabled by default.

        :param list port_pair:
            **REQUIRED** Port Pair to be used by linux traffic generator

        :param bool update_pkg:
            **OPTIONAL** Flag to update packages on device from repository. Default is True

        :return: True if successful else raises an exception

        :rtype: bool or exception

        Example::

          Python:
            hLg.init(port_pair=['h0:h0r0_1_if', 'h1:h1r0_1_if'], update_pkg=False)
          Robot:
            @{port_pair}    h0:h0r0_1_if  h1:h1r0_1_if
            hLg.init   port_pair=@{port_pair}  update_pkg=False
        """

        if port_pair is None:
            self.log('ERROR', "Missing mandatory argument, port_pair")
            raise TypeError("Missing mandatory argument, port_pair")

        self.port_pair = port_pair

        self.clnt_tag, self.srvr_tag = self.port_pair
        self.clnt_res_name, self.clnt_port_name = self.clnt_tag.split(':')
        self.srvr_res_name, self.srvr_port_name = self.srvr_tag.split(':')

        self._get_res_info(self.clnt_res_name)
        self._get_res_info(self.srvr_res_name)
        self.clnt_name = self.resource[self.clnt_res_name]['name']
        self.srvr_name = self.resource[self.srvr_res_name]['name']

        self.clnt_ip_addr = self.resource[self.clnt_res_name]['ip']
        self.srvr_ip_addr = self.resource[self.srvr_res_name]['ip']

        self.msg = 'on Client({}) and Server({})'.format(self.clnt_name, self.srvr_name)

        self.clnt_port = self.intf_data['clnt']['pic']
        self.srvr_port = self.intf_data['srvr']['pic']

        self.clnt_hndl = self.resource[self.clnt_res_name]['hndl']
        self.srvr_hndl = self.resource[self.srvr_res_name]['hndl']
        self.clnt_node_hndl = self.resource[self.clnt_res_name]['node_hndl']
        self.srvr_node_hndl = self.resource[self.srvr_res_name]['node_hndl']
        self.clnt_prompt = self.resource[self.clnt_res_name]['prompt']
        self.srvr_prompt = self.resource[self.srvr_res_name]['prompt']

        self.clnt_hndl.su()
        self.srvr_hndl.su()

        if update_pkg:
            # if not hasattr(self, 'tar_file_location') or not hasattr(self, 'tar_file_name'):
            if self.tar_file_location is None or self.tar_file_name is None:
                raise TypeError('Missing mandatory argument, tar_file_location/tar_file_name. \
                    These parameters should be passed in the constructor')
            else:
                if not self._verify_tar_version(self.clnt_hndl):
                    self._setup_files(self.clnt_ip_addr, self.clnt_hndl)

                if not self._verify_tar_version(self.srvr_hndl):
                    self._setup_files(self.srvr_ip_addr, self.srvr_hndl)

        if 'uv-ip' in self.intf_data['clnt']:
            self.clnt_port_ip = self.intf_data['clnt']['uv-ip']
        if 'uv-ipv6' in self.intf_data['clnt']:
            self.clnt_port_ipv6 = self.intf_data['clnt']['uv-ipv6']
        if 'uv-ip' in self.intf_data['srvr']:
            self.srvr_port_ip = self.intf_data['srvr']['uv-ip']
        if 'uv-ipv6' in self.intf_data['srvr']:
            self.srvr_port_ipv6 = self.intf_data['srvr']['uv-ipv6']

        if self.connect:
            self._connect()

        self.log('INFO', "Initialized Linux TG")

        return True

    def __del__(self):
        """Destructor method to destroy the instance"""

        self.disconnect()

    def disconnect(self):
        """Disconnect from Linux devices

        Disconnects from linux client and server devices only if its already connected.

        :return: True if successful.

        :rtype: bool

        Example::

          Python:
            hLg.disconnect()
          Robot:
            hLg.Disconnect
        """

        if not self.is_connected:
            return True

        self.log('INFO', "Disconnecting from daemons {}".format(self.msg))

        self.clnt_hndl.shell(command='exit', pattern=self.clnt_prompt)
        self.clnt_node_hndl.prompt = self.clnt_prompt
        self.srvr_hndl.shell(command='exit', pattern=self.srvr_prompt)
        self.srvr_node_hndl.prompt = self.srvr_prompt

        self.is_connected = False

        self.log('INFO', "Disconnected from daemons {}".format(self.msg))

        return True

    def configure_interfaces(self, **kwargs):
        """Configure Client and Server interfaces

        | Client and Server device interfaces are configured using this method.
        | If IPs are passed, Client and Server device interfaces are configured with those IPs.
        | If uv-ip is given in params.yaml, interfaces will be configured using those IPs.
        | When client/server gateway IPs are given, static routes for the corresponding IPs are
        | added.

        :param string clnt_port_ip:
            **OPTIONAL** IP of the Client port. IP has to be set using either this variable \
                or 'uv-ip' in params.yaml

        :param string clnt_port_ipv6:
            **OPTIONAL** IPv6 of the Client port. IPv6 has to be set using either this variable \
                or 'uv-ipv6' in params.yaml

        :param string srvr_port_ip:
            **OPTIONAL** IP of the Server port. IP has to be set using either this variable \
                or 'uv-ip' in params.yaml

        :param string srvr_port_ipv6:
            **OPTIONAL** IPv6 of the Server port. IPv6 has to be set using either this variable \
                or 'uv-ipv6' in params.yaml

        :param string clnt_gw_ip:
            **OPTIONAL** Gateway IP for Client port.

        :param string clnt_gw_ipv6:
            **OPTIONAL** IPv6 Gateway for Client port.

        :param string srvr_gw_ip:
            **OPTIONAL** Gateway IP for Server port.

        :param string srvr_gw_ipv6:
            **OPTIONAL** IPv6 Gateway for Server port.

        :return: True if successful else raises an exception

        :rtype: bool or exception


        Examples::

            1) When interface IPs are given in params.yaml using uv-ip
                Python:
                  hLg.configure_interfaces()
                Robot:
                  hLg.Configure Interfaces
            2) If static routes need to be added too
                Python:
                  hLg.configure_interfaces(clnt_gw_ip='1.1.1.1/24', 'srvr_gw_ip'='2.2.2.1/24')
                Robot:
                  hLg.Configure Interfaces   clnt_gw_ip=1.1.1.1/24   srvr_gw_ip=2.2.2.1/24
            3) When the IPs are given by user
                Python:
                  hLg.configure_interfaces(clnt_port_ip='1.1.1.2/24', srvr_port_ip='2.2.2.2/24')
                Robot:
                  hLg.Configure Interfaces   clnt_port_ip=1.1.1.2/24   srvr_port_ip=2.2.2.2/24
            4) When static routes need to be added along with IPs given by user
                Python:
                  hLg.configure_interfaces(clnt_port_ip='1.1.1.2/24', srvr_port_ip='2.2.2.2/24',
                                            clnt_gw_ip='1.1.1.1/24', 'srvr_gw_ip'='2.2.2.1/24')
                Robot:
                  hLg.Configure Interfaces   clnt_port_ip=1.1.1.2/24   srvr_port_ip=2.2.2.2/24
                                            clnt_gw_ip=1.1.1.1/24   srvr_gw_ip=2.2.2.1/24
        """

        if 'clnt_port_ip' not in kwargs and 'uv-ip' not in self.intf_data['clnt'] and \
           'uv-ipv6' not in self.intf_data['clnt'] and 'clnt_port_ipv6' not in kwargs:
            raise TypeError('Missing mandatory argument, clnt_port_ip')
        if 'srvr_port_ip' not in kwargs and 'uv-ip' not in self.intf_data['srvr'] and \
           'uv-ipv6' not in self.intf_data['srvr'] and 'srvr_port_ipv6' not in kwargs:
            raise TypeError('Missing mandatory argument, srvr_port_ip')

        #self.clnt_port_ip = kwargs.get('clnt_port_ip', self.intf_data['clnt']['uv-ip'])
        #self.srvr_port_ip = kwargs.get('srvr_port_ip', self.intf_data['srvr']['uv-ip'])
        self.clnt_port_ip = kwargs.get('clnt_port_ip', self.clnt_port_ip)
        self.srvr_port_ip = kwargs.get('srvr_port_ip', self.srvr_port_ip)
        self.clnt_port_ipv6 = kwargs.get('clnt_port_ipv6', self.clnt_port_ipv6)
        self.srvr_port_ipv6 = kwargs.get('srvr_port_ipv6', self.srvr_port_ipv6)

        #if iputils.is_ip_ipv4(self.clnt_port_ip):
        if self.clnt_port_ip is not None:
            self.clnt_port_ip_netmask = iputils.get_network_mask(self.clnt_port_ip)
        if self.clnt_port_ipv6 is not None:
            self.clnt_port_ipv6_netmask = iputils.get_mask(self.clnt_port_ipv6)

        #if iputils.is_ip_ipv4(self.srvr_port_ip):
        if self.srvr_port_ip is not None:
            self.srvr_port_ip_netmask = iputils.get_network_mask(self.srvr_port_ip)
        if self.srvr_port_ipv6 is not None:
            self.srvr_port_ipv6_netmask = iputils.get_mask(self.srvr_port_ipv6)

        self.log('INFO',
                 "Configuring IP on Client(interface: {}, IP:{}) and Server(interface: {}, IP:{})".
                 format(self.clnt_port, self.clnt_port_ip, self.srvr_port, self.srvr_port_ip))

        client_port = self.clnt_port + "." +str(kwargs['vlan']) if 'vlan' in kwargs else self.clnt_port
        server_port = self.srvr_port + "." +str(kwargs['vlan']) if 'vlan' in kwargs else self.srvr_port
        #try:
        if self.clnt_port_ip is not None:
            linux_network_config.configure_ip_address(device=self.clnt_hndl,
                                                      interface=client_port,
                                                      address=iputils.strip_mask(
                                                          self.clnt_port_ip),
                                                      mask=self.clnt_port_ip_netmask)
        if self.clnt_port_ipv6 is not None:
            linux_network_config.configure_ip_address(device=self.clnt_hndl,
                                                      interface=client_port,
                                                      address=iputils.strip_mask(
                                                          self.clnt_port_ipv6),
                                                      mask=self.clnt_port_ipv6_netmask)
        if self.srvr_port_ip is not None:
            linux_network_config.configure_ip_address(device=self.srvr_hndl,
                                                      interface=server_port,
                                                      address=iputils.strip_mask(
                                                          self.srvr_port_ip),
                                                      mask=self.srvr_port_ip_netmask)
        if self.srvr_port_ipv6 is not None:
            linux_network_config.configure_ip_address(device=self.srvr_hndl,
                                                      interface=server_port,
                                                      address=iputils.strip_mask(
                                                          self.srvr_port_ipv6),
                                                      mask=self.srvr_port_ipv6_netmask)
        #except Exception:
            #self.log('ERROR', "Error while configuring IPv4/v6 on client/server")
            #raise RuntimeError("Error while configuring IPv4/v6 on client/server")

        self.log('INFO',
                 "Configured IP on Client(interface: {}, IP:{}) and Server(interface: {}, IP:{})".
                 format(self.clnt_port, self.clnt_port_ip, self.srvr_port, self.srvr_port_ip))

        self.clnt_gw_ip = kwargs.get('clnt_gw_ip', None)
        self.srvr_gw_ip = kwargs.get('srvr_gw_ip', None)
        self.clnt_gw_ipv6 = kwargs.get('clnt_gw_ipv6', None)
        self.srvr_gw_ipv6 = kwargs.get('srvr_gw_ipv6', None)
        result = True
        if (self.clnt_gw_ip is not None and self.srvr_gw_ip is not None) or \
           (self.clnt_gw_ipv6 is not None and self.srvr_gw_ipv6 is not None):
            result &= self._add_routes()

        self.is_intf_configured = True

        return result

    def configure_traffic(self, **kwargs):
        """Configure traffic on Client and Server devices based on the given configuration

        | Client and Server profiles are added based on the given configuration per protocol.
        | For multi-protocol configuration, this method needs to be called separately for
        | every protocol to be configured.

        :param string ip_src_addr:
            **REQUIRED** Starting source IP address

        :param string ip_dst_addr:
            **REQUIRED** Starting destination IP address

        :param int num_src_ips:
            **OPTIONAL** Number of source IP addresses. Default is 1

        :param int start_unit:
            **OPTIONAL** starting unit for client interface. Default is 1

        :param int server_start_unit:
            **OPTIONAL** starting unit for server interface. Default is 1

        :param int num_ports_per_src_ip:
            **OPTIONAL** Number of ports to be used per source IP address. Default is 10

        :param int src_port:
            **OPTIONAL** Starting Source port to be used. Default is 10000

        :param int dst_port:
            **OPTIONAL** Starting Destination port to be used. Default is 20000

        :param string protocol:
            **OPTIONAL** Protocol to be used. Valid protocols are Udp, Tcp, HttpBase, HttpStateful,
                HttpsBase, HttpsStateful, Ftp, Dnsudp, Dnstcp, Smtp, Rtsp, Tftpy, Tcpfast, Icmp.
                Default is Udp

        :param int data_length:
            **OPTIONAL** Length of data to be used in the packet. Default is 64

        :param int num_trans:
            **OPTIONAL** Number of transactions per connection. Default is 1

        :param string duration:
            **OPTIONAL** Duration for which the transactions need to be done. Default is 10s

        :param bool bidir:
            **OPTIONAL** Flag to determine whether to send bidirectional traffic for UDP.
                Default is 1

        :param int wait_before_stop:
            **OPTIONAL** Number of seconds to wait before sending FIN. Default is 0

        :param int pps:
            **OPTIONAL** PPS rate to send. Default is 2

        :param string url:
            **OPTIONAL** URL to download for the HTTP methods

        :param string method:
            **OPTIONAL** HTTP method to use. Valid values are GET/PUT/DELETE/POST. Default is GET

        :param string dl_file:
            **OPTIONAL** The file to be downloaded in Tftpy/Ftp

        :param string ul_file:
            **OPTIONAL** The file to be uploaded in Tftpy/Ftp

        :params bool active_mode:
            **OPTIONAL** Enable Ftp active mode connections. Default is False(passive mode)

        :params string user_name:
            **OPTIONAL** Ftp Username/Identity to be used. Default is 'user'

        :params string passwd:
            **OPTIONAL** Ftp password/cipher to be used. Default is '12345'

        :params bool multi_auth:
            **OPTIONAL** Telnet/Ftp multiauth support. Default is  False

        :params string user_hdr:
            **OPTIONAL** User Provided header ex:"host:apps.facebook.com,
                Content-Type: application/x-www-form-urlencoded" Http. Default is ''

        :params string key_file:
            **OPTIONAL** SSL cert keyfile to be used for Https. Default is None

        :params string email:
            **OPTIONAL** mail From/To/Subject Strings to be changed Eg:"From=user@juni
                per.net,To=user2@juniper.net,Subject=Test" smtp. Default is None

        :params string cert_file:
            **OPTIONAL** SSL cert certificate file to be used Https. Default is client.pem

        :params string ts_size:
            **OPTIONAL** Mpeg-2 Traffic Stream size for video_monitor. Default is 188

        :params string ts_per_pkt:
            **OPTIONAL** Number of Traffic Streams per UDP pkt for video_monitor. Default is 7

        :params string ciphers:
            **OPTIONAL** SSL ciphers Algorithm to be used for Ftp. Default is None

        :param sting filename:
            **OPTIONAL** File name with obsolute path where statistics will be written. Default is
                /tmp/csv/<pid>_TrafficStats.csv

        :params string logger:
            **OPTIONAL** Logging level (INFO/DEBUG/ERROR/WARNING/CRITICAL) to
                be used for the client run. Default is ERROR)

        :params string edit:
            **OPTIONAL** To edit the packet header

        :params string num_dst_ips:
            **OPTIONAL** Number of destination IP addresses. Default is 1

        :params bool setup_subintf:
            **OPTIONAL** Setup sub_interface when num_src_ips >= 1. Default is True

        :params int num_tunnels:
            **REQUIRED** Number of tunnels to be create for PPTP. Default is 1.

        :params string interface_tunnel_endpoint:
            **REQUIRED** The interface in which sub interfaces are used as tunnel end points. 
            Default is None

        :return: True if successful else raises an exception

        :rtype: True or exception

        Examples::

          Python:
            hLg.configure_traffic(ip_src_addr='1.1.1.1', ip_dst_addr='30.1.1.1')

            hLg.configure_traffic(ip_src_addr='1.1.1.1', ip_dst_addr='30.1.1.2',
                                  dst_port=12000, src_port=10000, num_trans=1,
                                  data_length=64, duration=10s, bidir=1, wait_before_stop=0,
                                  protocol='Udp', num_src_ips=1, num_ports_per_src_ip=10)

            #In case of destination NAT separate server_ip and server_port need to passed
            hLg.configure_traffic(ip_src_addr='1.1.1.1', ip_dst_addr='30.1.1.2',
                                  dst_port=12000, src_port=10000, num_trans=1,
                                  data_length=64, duration=10s, bidir=1, wait_before_stop=0,
                                  protocol='Udp', num_src_ips=1, num_ports_per_src_ip=10,
                                  server_ip='40.0.0.1', server_port='80')
          Robot:
            hLg.Configure Traffic ip_src_addr=1.1.1.1  ip_dst_addr=30.1.1.1

            hLg.Configure Traffic   ip_dst_addr=30.1.1.2   num_trans=1   data_length=64
                                    duration=10s   bidir=1   wait_before_stop=0
                                    ip_src_addr=1.1.1.1   protocol=Udp   num_src_ips=1
                                    num_ports_per_src_ip=10   dst_port=12000   src_port=10000

        """

        self.log('INFO', "Configuring traffic {}".format(self.msg))

        if not self.is_intf_configured:
            self.log('ERROR', "Interfaces are not configured.configure_interfaces \
                need to be called before configuring traffic")
            raise RuntimeError("Interfaces are not configured. configure_interfaces needs \
                to be called before configuring traffic")

        if 'ip_src_addr' not in kwargs or 'ip_dst_addr' not in kwargs:
            self.log('ERROR', "Missing mandatory arguments, ip_src_addr and ip_dst_addr")
            raise TypeError("Missing mandatory arguments, ip_src_addr and ip_dst_addr")

        protocol = kwargs.get('protocol', 'Udp')
        #opts = self.options[kwargs['protocol']]
        if protocol not in self.options:
            self.log('ERROR', "Invalid protocol. {}".format(protocol))
            raise TypeError("Invalid protocol. {}".format(protocol))

        clnt_opts = Values()
        srvr_opts = Values()

        opts = self.options[protocol]

        clnt_opts.protocol = protocol

        # Copy default values for generic keys
        for key in self.options['all']['client']:
            # setattr(clnt_opts, key, self.options['all']['client'][key])
            setattr(clnt_opts, key, kwargs.get(key, self.options['all']['client'][key]))
        # Copy default values for protocol specific keys
        for key in opts['client']:
            # setattr(clnt_opts, key, opts['client'][key])
            setattr(clnt_opts, key, kwargs.get(key, opts['client'][key]))
        clnt_opts.logger = 'INFO'

        # Build opts for server profile
        for key in self.options['all']['server']:
            #setattr(srvr_opts, key, self.options['all']['server'][key])
            setattr(srvr_opts, key, kwargs.get(key, self.options['all']['server'][key]))
        for key in opts['server']:
            #setattr(srvr_opts, key, opts['server'][key])
            setattr(srvr_opts, key, kwargs.get(key, opts['server'][key]))
        srvr_opts.logger = 'INFO'

        for key in kwargs:
            if key.startswith('server_'):
                setattr(srvr_opts, '_'.join(key.split('_')[1:]), kwargs[key])
            else:
                setattr(clnt_opts, key, kwargs[key])

        self.ip_dst_addr = kwargs['ip_dst_addr']
        if not hasattr(srvr_opts, 'ip'):
            srvr_opts.ip = clnt_opts.ip_dst_addr
        if not hasattr(srvr_opts, 'port'):
            srvr_opts.port = int(clnt_opts.dst_port)
        if not hasattr(srvr_opts, 'protocol'):
            srvr_opts.protocol = clnt_opts.protocol

        if 'vlan' in kwargs:
            self._configure_vlan(self.clnt_port, kwargs['vlan'])
            self._configure_vlan(self.srvr_port, kwargs['vlan'])

        clnt_start_unit = kwargs.get('start_unit', 1)
        srvr_start_unit = kwargs.get('server_start_unit', 1)

        setup_subintf = kwargs.get('setup_subintf', True)

        if int(clnt_opts.num_src_ips) >= 1 and setup_subintf:
            interface = self.clnt_port + "." + str(kwargs['vlan']) if 'vlan' in kwargs else self.clnt_port
            self._conf_subintf("client", clnt_opts.ip_src_addr, interface, clnt_opts.num_src_ips, clnt_start_unit)

        if int(srvr_opts.num_dst_ips) >= 1 and setup_subintf:
            interface = self.srvr_port + "." + str(kwargs['vlan']) if 'vlan' in kwargs else self.srvr_port
            self._conf_subintf("server", srvr_opts.ip, interface, srvr_opts.num_dst_ips, srvr_start_unit)

        clnt_cmd = 'hLg.add_profile("client", {})'.format(str(clnt_opts))
        srvr_cmd = 'hLg.add_profile("server", {})'.format(str(srvr_opts))

        #self.clnt_opts[protocol] = clnt_opts
        #self.srvr_opts[protocol] = srvr_opts
        self.clnt_opts_list.append(clnt_opts)
        self.srvr_opts_list.append(srvr_opts)


        if srvr_opts.port is not 22 and srvr_opts.port is not 23:#excluding telnet and ssh ports
            self.log('INFO', 'Killing all processes running on the destination port \
                '.format(srvr_opts.port))
            self.srvr_hndl.shell(command='kill -9 $(lsof -t -i:'+ str(srvr_opts.port) +')')

        # Send server traffic profile to the server machine
        self.srvr_hndl.shell(command=srvr_cmd)

        # Send client traffic profile to the client machine
        self.clnt_hndl.shell(command=clnt_cmd)

        self.is_traffic_configured = True

        self.log('INFO', "Configured traffic {}".format(self.msg))

        return True

    def check_connectivity(self):
        """Check the connectivity between client and server

        :return: True if Server is reachable from client  else raises an exception

        :rtype: True or exception

        Example::

          Python:
            hLg.check_connectivity()

          Robot:
            hLg.Check Connectivity
        """

        if not self.is_traffic_configured:
            self.log('ERROR', "No traffic profile is configured yet. Call config_traffic() first")
            raise RuntimeError("No traffic profile is configured yet. Call config_traffic() first")

        self.log('INFO', "Checking if server is reachable from client through ping")
        self.log('INFO', "Pinging the destination ip {}".format(self.ip_dst_addr))

        status = self.linux_tool_hndl.loop_ping(self.clnt_hndl,
                                                iputils.strip_mask(self.ip_dst_addr))

        if not status:
            self.log('ERROR', "Ping failed as server is not reachable from client")
            raise RuntimeError('Ping failed as server is not reachable from client.')

        return True

    def configure_pcp_map_request(self, **kwargs):
        """Configure PCP MAP Request with the passed parameters

        :param string client_ip:
            **REQUIRED** PCP Client IP

        :param string client_port:
            **OPTIONAL** PCP Client port. Default is 0 [Port will be allotted by kernel]

        :param string server_ip:
            **REQUIRED** PCP Server IP

        :param string server_port:
            **REQUIRED** PCP Server port

        :param string map_intip:
            **REQUIRED** Internal IP in the mapping request. Default is client_ip

        :param int num_int_ips:
            **OPTIONAL** Number of internal IP addresses. Default is 1

        :param int num_ports_per_int_ip:
            **OPTIONAL** Number of ports to be used per internal IP address. Default is 1

        :param int map_intport:
            **REQUIRED** Internal port in the mapping request

        :param string map_extip:
            **REQUIRED** External IP in the mapping request

        :param int map_extport:
            **REQUIRED** External port in the mapping request

        :param int map_lifetime:
            **OPTIONAL** Mapping life time. Default is 3000(secs)

        :param int map_proto:
            **OPTIONAL** Protocol Id. Default is 17

        :returns: True on successful configuration else raises an exception

        :rtype: True or exception

        Example::

            Python:
                configure_pcp_map_request('client_ip'='11.1.1.2', 'server_ip'='120.0.0.3',
                                          'proto'=17, intport=5001, extport=5001,
                                          'extip'='44.44.44.1', lifetime=3000)

            Robot:
                Configure PCP MAP Request  client_ip=11.1.1.2  server_ip=120.0.0.3\
                                           proto=17  intport=5001  extport=5001\
                                           extip=44.44.44.1  lifetime=3000
        """

        self.log("Configuring PCP Map Request")
        if not self.is_intf_configured:
            self.log('ERROR', "Interfaces are not configured. configure_interfaces needs \
                to be called before configuring traffic")
            raise RuntimeError("Interfaces are not configured. configure_interfaces needs \
                to be called before configuring traffic")

        opts = Values()
        #opts.client_ip = kwargs.get('client_ip', None)
        #opts.server_ip = kwargs.get('server_ip', None)
        #opts.int_ip = kwargs.get('map_intip', opts.client_ip)
        #opts.intport = kwargs.get('intport', None)
        #opts.extip = kwargs.get('extip', None)
        #opts.extport = kwargs.get('extport', None)
        #opts.proto_id = kwargs.get('proto', 17)
        #opts.life_to = kwargs.get('lifetime', 3000)

        #if opts.client_ip is None or opts.server_ip is None or opts.intport is None or \
           #opts.extip is None or opts.extport is None:
        if 'client_ip' not in kwargs or 'server_ip' not in kwargs or \
           'map_intport' not in kwargs or 'map_extip' not in kwargs or \
           'map_extport' not in kwargs:
            self.log('ERROR', "Missing mandatory arguments, \
                     client_ip/server_ip/map_intport/map_extip/map_extport")
            raise TypeError("Missing mandatory arguments, \
                            client_ip/server_ip/map_intport/map_extip/map_extport")

        opts.int_ip = kwargs.get('map_intip', kwargs['client_ip'])
        opts.protocol = 'Pcpc'

        # Copy default values for generic keys
        for key in self.options['Pcpc']['client']:
            setattr(opts, key, self.options['Pcpc']['client'][key])
        opts.logger = 'INFO'
        for key in kwargs:
            setattr(opts, key, kwargs[key])

        #clnt_cmd = 'hLg.add_profile("pcp", {})'.format(str(opts))
        clnt_cmd = 'hLg.add_pcp_profile({})'.format(str(opts))
        self.clnt_hndl.shell(command=clnt_cmd)

        #cmd = 'python pcpc-oneline.py -i {} -s {} -d -t {} -P {} -p {} -e {} –l {}'.\
                #format(client_ip, server_ip, proto_id, intport, extport, extip, map_to)
        #self.clnt_hndl.shell(command=cmd)
        self.is_pcp_configured = True
        self.pcp_opts_list.append(opts)

        return True

    def start_pcp_map_requests(self):
        """Start PCP Map requests from client

        :return: True if map requests are sent else raises an exception

        :rtype: bool

        Example::

          Python:
            hLg.start_pcp_map_requests()

          Robot:
            hLg.Start PCP Map Requests
        """

        if not self.is_pcp_configured:
            self.log('ERROR', "No PCP Map requests are configured yet. \
                     Call configure_pcp_map_request() first")
            raise RuntimeError("No PCP Map requests are configured yet. \
                               Call configure_pcp_map_request() first")

        self.log('INFO', "Starting PCP Map requests on Client, {}".format(self.clnt_name))

        self.clnt_hndl.shell(command='hLg.start_pcp_map_requests()')

        self.log('INFO', "Started PCP Map requests on Client, {}".format(self.clnt_name))

        return True

    def delete_all_profiles(self):
        self.log('INFO', "Deleting all server profiles")
        self.srvr_hndl.shell(command='hLg.del_profile("server")')

        self.log('INFO', "Deleting all clients")
        self.clnt_hndl.shell(command='hLg.del_profile("client")')


        # Add PCP profiles later
        return True

    def start_traffic(self):
        """Start traffic on Server/Client devices

        Commands are issued to client and server daemons running on the linux machines.
        First, server(s) are started followed by clients.

        :return: True if traffic is started else raises an exception

        :rtype: bool

        Example::

          Python:
            hLg.start_traffic()

          Robot:
            hLg.Start Traffic
        """

        if not self.is_traffic_configured:
            self.log('ERROR', "No traffic profile is configured yet. Call config_traffic() first")
            raise RuntimeError("No traffic profile is configured yet. Call config_traffic() first")

        self.is_running = False

        self.log('INFO', "Starting traffic {}".format(self.msg))

        self.log('INFO', "Starting Servers on {}..".format(self.srvr_name))
        output = self.srvr_hndl.shell(command='hLg.start_servers()').response()
        if not self._get_traffic_status(output):
            self.log('ERROR', "Unable to start Servers")
            raise RuntimeError('Unable to start Servers')
        else:
            self.log('INFO', "Started Servers on {}..".format(self.srvr_name))


        self.log('INFO', "Starting Clients on {}..".format(self.clnt_name))
        output = self.clnt_hndl.shell(command='hLg.start_clients()').response()
        if not self._get_traffic_status(output):
            self.log('ERROR', "Unable to start Clients")
            raise RuntimeError('Unable to start Clients')
        else:
            self.log('INFO', "Started Clients on {}..".format(self.clnt_name))

        self.is_running = True

        self.log('INFO', "Started Traffic successfully {}".format(self.msg))

        return True

    def stop_traffic(self):
        """Stop traffic on Client/Server devices.

        Commands are issued to client and server daemons running on the linux machines.
        First clients are stopped followed by servers.

        :return: True

        :rtype: bool

        Example::

          Python:
            hLg.stop_traffic()

          Robot:
            hLg.Stop Traffic
        """
        
        self.output = None

        if not self.is_running:
            self.log('INFO', "Traffic is not running. So, there's nothing to do here!")
            return True

        self.log('INFO', "Stopping the traffic {}".format(self.msg))

        self.log('INFO', "Stopping Clients on {}..".format(self.clnt_name))
        output = self.clnt_hndl.shell(command='hLg.stop_clients()').response()
        if not self._get_traffic_status(output):
            self.log('ERROR', "Unable to stop the Clients")
            raise RuntimeError('Unable to stop the Clients')
        else:
            self.log('INFO', "Stopped Clients on {}..".format(self.clnt_name))

        self.log('INFO', "Stopping Servers on {}..".format(self.srvr_name))
        output = self.srvr_hndl.shell(command='hLg.stop_servers()').response()
        if not self._get_traffic_status(output):
            self.log('ERROR', "Unable to stop the Servers")
            raise RuntimeError('Unable to stop the Servers')
        else:
            self.log('INFO', "Stopped Servers on {}..".format(self.srvr_name))

        self.is_running = False

        self.log('INFO', "Stopped traffic {}".format(self.msg))

        return True

    def _get_traffic_status(self, output):
        """Return the status of the start/stop traffic.

        :param string output:
            **REQUIRED** output string once you started/stoped the client/server

        :return: True if traffic started/stopped without any issues else False

        :rtype: bool

        Example::

          Python:
            get_traffic_status(output)

        """

        match = re.search(r'THREAD-\d+ Error\:\s+(.*)', output)
        if match:
            status = ast.literal_eval(match.group(1))
            self.log('ERROR', "Issue occured {}".format(status))
            return False

        return True


    def get_statistics(self):
        """Fetch statistics from Client/Server

        :return: Dictionary if successful else raises an exception

        :rtype: dict or exception

        Example::

          Python:
            hLg.get_statistics()

          Robot:
            hLg.Get Statistics

        """

        self.stats = None
        self.log('INFO', "Getting stats from Client, {}..".format(self.clnt_name))
        output = self.clnt_hndl.shell(command='hLg.get_client_stats()').response()
        self.log('INFO', "Stats from Client: {}".format(output))
        match = re.search(r'client_stats = (.*)', output)
        if match:
            self.stats = ast.literal_eval(match.group(1))

        if not self.stats:
            raise RuntimeError('Error while retrieving statistics. The stats are empty')

        self.log('INFO', "Got stats from Client, {}..".format(self.clnt_name))

        return self.stats

    def verify_statistics(self, **kwargs):
        """Verify statistics

        :param string err_lvl:
            **OPTIONAL** Error Level. This is set to INFO if errors need to be ignored.
            Default is ERROR.

        :param int tol_perc:
            **OPTIONAL** Tolerance % for comparing stats. Default is None.

        :param int tol_val:
            **OPTIONAL** Tolerance % for comparing stats. Default is None.

        :return: True if verification passes else raises an exception

        :rtype: True or exception

        Example::

          Python:
            hLg.verify_statistics()

          Robot:
            hLg.Verify Statistics
        """

        self.log('INFO', "Going to verify statistics")

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'err_lvl': 'ERROR', 'tol_perc': None,
                                               'tol_val' : None,
                                           })
        # Fetch the statistics from the daemons
        try:
            self.get_statistics()
        except:
            raise ValueError('Error while retrieving statistics')

        result = True

        args = {}
        args['err_lvl'] = this['err_lvl']
        if this['tol_perc'] is not None:
            args['tol_perc'] = this['tol_perc']
        if this['tol_val'] is not None:
            args['tol_val'] = this['tol_val']

        for proto in self.stats:
            proto_stats = self.stats[proto]
            proto_status = True
            _msg = "Traffic stats verification for {} protocol".format(proto)
            if proto_stats['result'] == 'FAIL':
                proto_status = False
                result = False
                self.log(this['err_lvl'], "{} FAILED".format(_msg))
                # Not sure if we want to raise an exception if err_lvl is set to INFO
                #raise ValueError("{} FAILED".format(_msg))
            if not utils.cmp_val(exp_val=proto_stats['txns_tx'], act_val=proto_stats['txns_rx'],
                                 **args):
                proto_status = False
                result = False
                self.log(this['err_lvl'], "Mismatch in the number of transactions sent and \
                         received for {} protocol".format(proto))
                # Not sure if we want to raise an exception if err_lvl is set to INFO
                #raise ValueError('Mismatch in the number of transactions sent and received for {} \
                    #protocol'.format(proto))
                continue

            if proto_status:
                self.log('INFO', "{} PASSED".format(_msg))
            else:
                result = False
                self.log('INFO', "{} FAILED".format(_msg))

        if not result:
            self.log(this['err_lvl'], "Traffic stats verification FAILED")
            if 'ERROR' in this['err_lvl'].upper():
                raise RuntimeError("Traffic stats verification FAILED")
        else:
            self.log('INFO', "Traffic stats verification PASSED")

        return result

    def get_session_count(self):
        """Return number of sessions going to be sent

        :return: Dictionary containing the session count

        :rtype: dict

        Example::

          Python:
            hLg.get_session_count()

          Robot:
            hLg.Get Session Count
        """

        self.log('INFO', "Receiving configured sessions count")

        self.sess_cnt = {}

        total = 0
        for proto_opts in self.clnt_opts_list:
            #proto_opts = self.clnt_opts[proto]

            total += int(proto_opts.num_src_ips) * int(proto_opts.num_ports_per_src_ip)

        self.sess_cnt[self.clnt_tag] = total
        self.sess_cnt['total'] = total

        self.log('INFO', "Returning configured sessions count")

        return self.sess_cnt

    def get_sessions(self):
        """Return session data


        :return: Dictionary containing the sessions

        :rtype: dict

        Example::

          Python:
            hLg.get_sessions()

          Robot:
            hLg.Get Sessions
        """

        self.log('INFO', "Retrieving configured sessions")

        sess_list = []
        src_ips = []
        dst_ips = []
        pcp_maps_list = []
        #for proto in self.clnt_opts:
        for proto_opts in self.clnt_opts_list:
            #proto_opts = self.clnt_opts[proto]
            src_ip = proto_opts.ip_src_addr
            for _ in range(0, int(proto_opts.num_src_ips)):
                for port_num in range(0, int(proto_opts.num_ports_per_src_ip)):
                    sess = {}
                    sess['src_ip'] = src_ip
                    sess['src_port'] = int(proto_opts.src_port) + port_num
                    sess['dst_ip'] = proto_opts.ip_dst_addr
                    sess['dst_port'] = proto_opts.dst_port
                    sess['proto'] = proto_opts.protocol
                    sess_list.append(sess)
                    if proto_opts.ip_dst_addr not in dst_ips:
                        dst_ips.append(proto_opts.ip_dst_addr)
                if src_ip not in src_ips:
                    src_ips.append(src_ip)
                src_ip = iputils.incr_ip(src_ip)

        self.sessions = {}
        self.sessions[self.clnt_tag] = {}
        self.sessions[self.clnt_tag]['sess_list'] = sess_list
        self.sessions[self.clnt_tag]['src_ips_list'] = src_ips
        self.sessions[self.clnt_tag]['dst_ips_list'] = dst_ips
        self.sessions[self.clnt_tag]['total'] = len(sess_list)
        self.sessions['total'] = len(sess_list)

        if self.is_pcp_configured:
            for opts in self.pcp_opts_list:
                int_ip = opts.intip
                for _ in range(0, int(opts.num_int_ips)):
                    for port_num in range(0, int(opts.num_ports_per_int_ip)):
                        map_req = {}
                        map_req['pcp_ip'] = opts.client_ip
                        map_req['int_ip'] = opts.intip
                        map_req['int_port'] = opts.intport + port_num
                        map_req['ext_ip'] = opts.extip
                        map_req['ext_port'] = opts.extport
                        pcp_maps_list.append(opts)
                    int_ip = iputils.incr_ip(int_ip)
            self.sessions[self.clnt_tag]['pcp_maps_list'] = pcp_maps_list
            self.sessions[self.clnt_tag]['total_pcp_reqs'] = len(pcp_maps_list)
            self.sessions['total_pcp_reqs'] = len(pcp_maps_list)


        self.log('INFO', "Returning configured sessions")
        return self.sessions

    def add_static_route(self, device=None, ip_list=None, ipv6_list=None,**kwargs):
        """Add static route on Client or Server

        :param string device:
            **REQUIRED** Device on which the static route need to be added.

        :param list ip_list:
            **REQUIRED** List of ips to which static route need to be added on device

        :param list ipv6_list:
            **REQUIRED** List of V6 ips to which static route need to be added on device

        :return: True if successful else raises an exception

        :rtype: True or exception

        Example::

          Python:
            hLg.add_static_route(device='client', ip_list=['112.1.1.0/24'], ipv6_list=['9::/64'])
            hLg.add_static_route(device='server', ip_list=['112.1.1.0/24'], ipv6_list=['9::/64'])

          Robot:
            @{iplist}    112.1.1.0/24    @{ipv6list}    9::/64
            hLg.Add Static Route   device=client   ip_list=@{iplist}    ipv6_list=@{ipv6list}
            hLg.Add Static Route   device=server   ip_list=@{iplist}    ipv6_list=@{ipv6list}
        """

        clnt_gw_ip = kwargs.get('clnt_gw_ip', self.clnt_gw_ip)
        srvr_gw_ip = kwargs.get('srvr_gw_ip', self.srvr_gw_ip)
        clnt_gw_ipv6 = kwargs.get('clnt_gw_ipv6', self.clnt_gw_ipv6)
        srvr_gw_ipv6 = kwargs.get('srvr_gw_ipv6', self.srvr_gw_ipv6)

        if (clnt_gw_ip is None or srvr_gw_ip is None) and (clnt_gw_ipv6 is None or srvr_gw_ipv6 is None):
            raise TypeError('Missing mandatory argument(s), clnt_gw_ip/srvr_gw_ip')

        self.log('INFO', "Configuring static routes {}".format(self.msg))

        if not ip_list and not ipv6_list:
            self.log('ERROR', "Error while configuring static routes {}".format(self.msg))
            raise RuntimeError('Error while configuring static routes {}'.format(self.msg))

        if ip_list:
            for ip_addr in ip_list:
                if 'client' in device:
                    linux_network_config.add_route(device=self.clnt_hndl,
                                                   network=iputils.get_network_address(
                                                       iputils.strip_mask(ip_addr)),
                                                   netmask=iputils.get_network_mask(
                                                       ip_addr),
                                                   gateway=iputils.strip_mask(clnt_gw_ip))
                if 'server' in device:
                    linux_network_config.add_route(device=self.srvr_hndl,
                                                   network=iputils.get_network_address(
                                                       iputils.strip_mask(ip_addr)),
                                                   netmask=iputils.get_network_mask(
                                                       ip_addr),
                                                   gateway=iputils.strip_mask(srvr_gw_ip))
            self.log('INFO', "Configured static routes {}".format(self.msg))

        if ipv6_list:
            for ipv6_addr in ipv6_list:
                if 'client' in device:
                    linux_network_config.add_route(device=self.clnt_hndl,
                                                   network=iputils.get_network_address(
                                                       iputils.strip_mask(ipv6_addr)),
                                                   netmask=iputils.get_mask(ipv6_addr),
                                                   gateway=iputils.strip_mask(clnt_gw_ipv6))
                if 'server' in device:
                   linux_network_config.add_route(device=self.srvr_hndl,
                                                   network=iputils.get_network_address(
                                                       iputils.strip_mask(ipv6_addr)),
                                              netmask=iputils.get_mask(ipv6_addr),
                                              gateway=iputils.strip_mask(srvr_gw_ipv6))
            self.log('INFO', "Configured static routes {}".format(self.msg))

        return True

    def _add_routes(self):
        """Add static routes on the linux devices

        :return: True if successful else raises an exception

        :rtype: True or exception

        Example:
           _add_routes()
        """
        self.log('INFO', "Configuring static routes {}".format(self.msg))

        # try:
        if self.clnt_gw_ip is not None:
            linux_network_config.add_route(device=self.clnt_hndl,
                                           network=iputils.get_network_address(self.srvr_port_ip),
                                           netmask=self.srvr_port_ip_netmask,
                                           gateway=iputils.strip_mask(self.clnt_gw_ip))
        if self.clnt_gw_ipv6 is not None:
            linux_network_config.add_route(device=self.clnt_hndl,
                                           network=iputils.get_network_address(self.srvr_port_ipv6),
                                           netmask=self.srvr_port_ipv6_netmask,
                                           gateway=iputils.strip_mask(self.clnt_gw_ipv6))
        if self.srvr_gw_ip is not None:
            linux_network_config.add_route(device=self.srvr_hndl,
                                           network=iputils.get_network_address(self.clnt_port_ip),
                                           netmask=self.clnt_port_ip_netmask,
                                           gateway=iputils.strip_mask(self.srvr_gw_ip))
        if self.srvr_gw_ipv6 is not None:
            linux_network_config.add_route(device=self.srvr_hndl,
                                           network=iputils.get_network_address(self.clnt_port_ipv6),
                                           netmask=self.clnt_port_ipv6_netmask,
                                           gateway=iputils.strip_mask(self.srvr_gw_ipv6))
        # except Exception:
        #     self.log('ERROR', 'Error while configuring static routes {}'.format(self.msg))
        #     raise Exception('Error while configuring static routes {}'.format(self.msg))

        self.log('INFO', "Configured static routes {}".format(self.msg))

        return True

    def _connect(self):
        """Connect to the Linux devices

        :return: True if successful else raises an exception

        :rtype: True or exception

        Example:
           _connect()
        """
        self.log('INFO', "Connecting to daemons {}".format(self.msg))

        try:
            self.clnt_hndl.shell(command='ulimit -n 100000')
            self.srvr_hndl.shell(command='ulimit -n 100000')
        except Exception:
            self.log('ERROR', "Unable to set the ulimit -n config")
            raise RuntimeError('Unable to set the ulimit -n config')

        self.clnt_hndl.shell(command=self.dmn_cmd, pattern=self.dmn_prompt)
        self.clnt_node_hndl.prompt = self.dmn_prompt
        self.srvr_hndl.shell(command=self.dmn_cmd, pattern=self.dmn_prompt)
        self.srvr_node_hndl.prompt = self.dmn_prompt

        self.is_connected = True

        self.log('INFO', "Connected to daemons {}".format(self.msg))

        return True

    def _conf_subintf(self, name, start_ip, interface, count, start_unit):
        """Add configuration for the sub interfaces

        :param string start_ip:
            **REQUIRED** IP to be configured on the interface

        :param string interface:
            **REQUIRED** Interface to be configured

        :param count network:
            **REQUIRED** The number of sub interfaces to be configured

        :param int start_unit:
            **REQUIRED** Unit to be configured on the interface

        :return: True

        :rtype: True

        Example:
           _conf_subintf('1.1.1.1', 'eth1', 10)
        """

        if name == 'client':
            device_name = self.clnt_name
            device_handle = self.clnt_hndl
        else:
            device_name = self.srvr_name
            device_handle = self.srvr_hndl

        self.log('INFO', "Configuring sub interfaces on Linux devices {}({})".format(
            name, device_name))
        cmd = ''
        intf_ip = start_ip
        v6 = iputils.is_ip_ipv6(intf_ip)
        for i in range(int(start_unit), int(start_unit) + int(count)):
            # cmd = 'ifconfig {}:{} {} up ; '.format(str(interface), str(i), str(intf_ip))
            if v6:
                cmd = 'ifconfig {} inet6 add {}/{} up ;'.format(str(interface), str(iputils.strip_mask(intf_ip)), str(iputils.get_mask(intf_ip)))
            else:
                cmd = 'ifconfig {}:{} {} netmask {} up ; '.format(str(interface), str(i), str(iputils.strip_mask(intf_ip)), str(iputils.get_network_mask(intf_ip)))
            intf_ip = iputils.incr_ip(intf_ip)
            device_handle.shell(command=cmd)

        self.log('INFO', "Configured sub interfaces on Linux devices {}({})".format(
            name, device_name))
        return True


    def _configure_vlan(self, interface, vlan_id):
        """Add Vlan to the interface

        :param string interface:
            **REQUIRED** Interface to be configured

        :param count network:
            **REQUIRED** Vlan ID to be configured

        :return: True

        :rtype: True

        Example:
           _configure_vlan('eth1', 10)
        """
        self.log('INFO', "Configuring VLAN on Linux devices Client({})".format(self.clnt_name))
        cmd = 'ip link add link {} name {}.{} type vlan id {} '.format(str(interface),
                                                    str(interface), str(vlan_id), str(vlan_id))
        self.clnt_hndl.shell(command=cmd)

        self.log('INFO', "Configured VLAN on Linux devices Client({})".format(self.clnt_name))
        return True

    def _get_res_info(self, res):
        """Update the resource information in the resource variable

        :param string res:
            **REQUIRED** The name of the resource given in params YAML

        :return: True

        :rtype: True

        Example:
           _get_res_info('device0')
        """
        self.log('INFO', "Updating the port pairs info for resource({})".format(res))

        self.resource[res] = {}
        self.resource[res]['obj'] = res_info = t.get_resource(res)
        self.resource[res]['name'] = res_info['system']['primary']['name']
        if 'controllers' in res_info['system']['primary'] and 'if0' in \
            res_info['system']['primary']['controllers'] and 'mgt-ip' in \
            res_info['system']['primary']['controllers']['if0']:
            self.resource[res]['ip'] = res_info['system']['primary']['controllers']['if0']['mgt-ip']
        else:
            self.resource[res]['ip'] = res_info['system']['primary']['name']
        self.resource[res]['name'] = res_info['system']['primary']['name']
        self.resource[res]['hndl'] = t.get_handle(res)
        self.resource[res]['node_hndl'] = node_hndl = t.get_handle(
            res, controller='current')
        self.resource[res]['prompt'] = node_hndl.prompt
        self.intf_data['clnt'] = t.get_interface(
            resource=self.clnt_res_name, intf=self.clnt_port_name)
        self.intf_data['srvr'] = t.get_interface(
            resource=self.srvr_res_name, intf=self.srvr_port_name)

        self.log('INFO', "Updated the port pairs info for resource({})".format(res))

    def _create_ssh_client(self, server, port, user, password):
        """Update the resource information in the resource variable

        :param string server:
            **REQUIRED** The name of the server

        :param string port:
            **REQUIRED** The port of the resource to be used

        :param string user:
            **REQUIRED** The username  of the resource

        :param string password:
            **REQUIRED** The password of the resource

        Example:
           _create_ssh_client(servers_name, 22, root, Embe1mpls)
        """
        client = self.paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        return client

    def _setup_files(self, dev_name, dev_hndl, **kwargs):
        """Update the files and packages on the Linux device

        :param string dev_name:
            **REQUIRED** The name of the resource given in params YAML

        :param obj dev_hndl:
            **REQUIRED** The handle of the device

        :return: True

        :rtype: True

        Example:
           _setup_files('H0', Device_Handle)
        """

        if 'scp_upload_username' not in kwargs:
            kwargs['scp_upload_username'], kwargs['scp_upload_password'] \
            = credentials.get_credentials(os='LINUX')
        user = kwargs.get("scp_upload_username")
        password = kwargs.get("scp_upload_password")
        time_stamp = time.strftime("%Y%m%d-%H%M%S")
        folder = '/tmp/' + time_stamp + '/'
        dev_hndl.shell(command='mkdir -m 777 ' + folder)
        ssh = self._create_ssh_client(dev_name, 22, user, password)
        self.scp = self.scp_clnt(ssh.get_transport())
        self.scp.put(self.tar_file_location + self.tar_file_name, folder + self.tar_file_name)
        dev_hndl.shell(command='cd ' + folder)
        dev_hndl.shell(command='tar -xvf ' + self.tar_file_name)
        dev_hndl.shell(command='cd ' + self.tar_file_name.split(".")[0])
        if self.base_setup:
            dev_hndl.shell(command='sh setup.sh', timeout=300)
        dev_hndl.shell(command='sh file_setup.sh', timeout=300)
        dev_hndl.shell(command='rm -rf '+ folder)

        return True


    def _verify_tar_version(self, dev_hndl):
        """Verify version of LiGen on Client/Server devices with the one in CVS.

        Verifies if the version of LiGen on Client/Servers devices is same as the one in CVS.

        :param obj dev_hndl:
            **REQUIRED** The handle of the device

        :return: True if both versions are same else raises an excpetion

        :rtype: True or exception

        Example:
           _verify_tar_version(Device_Handle)
        """
        self.hndl = dev_hndl

        #Get version from the linux device
        try:
            self.dev_pkg_ver = self.hndl.shell(command='cat ~regress/ligen/version.py').response()
            linux_version = re.search(r'ligen_pkg_version = "(.*\..*)"', self.dev_pkg_ver)
        except (TypeError, Exception):
            linux_version = None
        version = importlib.machinery.SourceFileLoader('version.py', self.tar_file_location +
                                                       'version.py').load_module()

        if linux_version:
            cvs_version = version.ligen_pkg_version
            result = True if linux_version.group(1) == cvs_version else False
            return result
        else:
            self.base_setup = True
            return False