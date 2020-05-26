# Copyright 2016- Juniper Networks
# Toby BBE development team
"""
This module contains classes for RT DHCP servers.
"""

import abc
from jnpr.toby.bbe.version import get_bbe_version


__author__ = ['Yong Wang']
__credits__ = ['Benjamin Schurman']
__contact__ = 'ywang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'
__version__ = get_bbe_version()

# For robot framework
ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
ROBOT_LIBRARY_VERSION = get_bbe_version()


class RTDHCPServerDefault:
    """Default for RT DHCP server

    """
    IPV4_LEASE_TIME = 99999
    IPV4_POOL_SIZE = 32000
    IPV4_POOL_START_ADDR = '100.16.0.1'
    IPV4_POOL_MASK_LENGTH = 8
    IPV4_POOL_GATEWAY = '100.0.0.1'
    # multiple-sever values
    # When uplink has more than one vlans and dhcp servers are configured as non-local in cfg yaml,
    # the same number of dhcp server instances are configured on RT.
    # configuration for more than dhcp servers can be as easy as defined by the steps.
    # You can also customize individual values by giving a string customized values for each server.
    #
    # Example multiple dhcp servers config in cfg yaml (note the values are for demo only)
    #
    # t:
    #     user_variables:
    #         uv-bbevar:
    #             dhcpserver:
    #                 ipv4:
    #                     lease-time: 99999
    #                     pool-gateway: 100.0.0.1
    #                     pool-start-address: 100.16.0.1
    #                     multi-servers:  # Custom configuration for more than one servers
    #                         pool-gateways: 100.15.0.1,100.16.0.1,100.8.0.1
    #                         pool-gateway-inside-step: 0.0.1.0
    #                         pool-inside-step: 0.1.0.0
    #                         pool-start-addresses: 100.15.0.2,100.16.0.2,100.8.0.2 # comma separated, no space
    #                         pool-sizes: 16000,32000,16000                         # comma separated, no space
    #                         pool-mask-lengths: 8,10,9                             # comma separated, no space
    #                         lease-times: 55555,66666,77777                        # comma separated, no space
    #                         assign-ip-on-specific-subnet: 0,1,1                   # comma separated, no space, 1 or 0
    #                     ri: default          # routing-instance info
    #                     mode: active        # local | active| passive | proxy
    #                 ipv6:                   # list
    #                     lease-time: 99999   # lease
    #                     pool-start-address: 2000::2
    #                     pool-prefix-start: 1000:0:1::0
    #                     multi-servers:  # Custom configuration for more than one servers
    #                         pool-start-addresses: 2000:8::2,2010:9::2,2102:12::2
    #                         pool-sizes: 16000,18000,12000
    #                         pool-inside-step: 1:0:0:0:0:0:0:0
    #                         pool-mask-lengths: 60,62,65
    #                         pool-prefix-inside-step: 1:0:0:0:0:0:0:0
    #                         pool-prefix-starts: 1080:0:1::0,1235:0:1::0,1202:0:1::0
    #                         pool-prefix-sizes: 8000,16000,36000
    #                         pool-prefix-lengths: 51,52,55
    #                     ri: default
    #                     mode: active  # local | active| passive | proxy
    #                     type: PD  # NA, PD, or Both
    #                     ndra: false  # boolean
    #
    #     resources:
    #         r0:
    #             interfaces:
    #                 uplink0:
    #                     uv-bbe-config:
    #                         ip: 200.0.0.1/24
    #                         ip-step: 0.0.1.0
    #                         ipv6: 3000:db8:ffff:5::1/64
    #                         ipv6-step: 0:0:0:1:0:0:0:0
    #                         vlan:
    #                             start: 1
    #                             step: 1
    #                             repeat: 1
    #                             length: 3

    IPV4_POOL_INSIDE_STEP = '0.1.0.0'          # valid value is like '0.1.0.0'
    IPV4_POOL_GATEWAY_INSIDE_STEP = '0.0.1.0'  # valid value is like '0.0.1.0'
    IPV4_POOL_START_ADDRS = None               # E.g., pool-start-addresses: 32.16.0.2,100.16.0.2,110.17.0.2
    IPV4_POOL_SIZES = None                     # E.g., pool-sizes: 8000,12000,64000
    IPV4_POOL_MASK_LENGTHS = None              # E.g., pool-mask-lengths: 8,10,9
    IPV4_POOL_GATEWAYS = None                  # E.g., pool-gateways: 32.16.0.1,100.16.0.1,110.17.0.1
    IPV4_LEASE_TIMES = None                    # E.g., lease_times: 55555,66666,777777
    IPV4_ADDR_ASSIGN = None                    # E.g., assign-ip-on-specific-subnet: 1,1,1

    IPV6_LEASE_TIME = 99999
    IPV6_POOL_SIZE = 32000
    IPV6_POOL_START_ADDR = '2000::2'
    IPV6_POOL_MASK_LENGTH = 64
    IPV6_IA_TYPE = 'iana_iapd'
    IPV6_POOL_PREFIX_START = '1000:0:1::0'
    IPV6_POOL_PREFIX_LENGTH = 48
    IPV6_POOL_PREFIX_SIZE = 16000
    IPV6_POOL_INSIDE_STEP = '1:0:0:0:0:0:0:0'         # valid value is like '1:0:0:0:0:0:0:0'
    IPV6_POOL_PREFIX_INSIDE_STEP = '1:0:0:0:0:0:0:0'  # valid value is like '1:0:0:0:0:0:0:0'
    IPV6_POOL_START_ADDRS = None             # E.g. 2000:8::2,2010::2, if multi servers want customized addrs
    IPV6_POOL_SIZES = None                   # E.g. 128000,64000, if multiple servers want customized addrs
    IPV6_POOL_PREFIX_STARTS = None           # E.g. 1080:0:1::0,1235:0:1::0, if multi servers want customized prefixes
    IPV6_POOL_PREFIX_SIZES = None            # E.g. 24000,48000
    IPV6_POOL_MASK_LENGTHS = None            # E.g. 64,70
    IPV6_POOL_PREFIX_LENGTHS = None          # E.g. 48,56


class RTDHCPServer(abc.ABC):
    """Abstract DHCP server

    """
    def __init__(self):
        """Initialize.

        :param uplink: BBEVarRTUplink instance
        """
        # BBEVarRTUplink interface
        self.__server_interface = None
        # RT handle
        self.__server_handle = None
        # if the server is created on RT
        self.__created = False

    @property
    def created(self):
        """If the server is created and started on RT

        :return: boolean. True if server is created on RT
        """
        return self.__created

    @created.setter
    def created(self, c_bool):
        """Set after the server is created on RT

        :param c_bool: boolean.
        :return: boolean. True if server is created on RT
        """
        self.__created = c_bool

    @property
    def server_interface(self):
        """Get BBEVarRTUplink instance associated with the server

        :return: BBEVarRTUplink instance associated with the server, or None if not available.
        """
        return self.__server_interface

    @server_interface.setter
    def server_interface(self, intf):
        """Set BBEVarRTUplink instance associated with the server

        :param intf: BBEVarRTUplink instance associated with the server
        :return: None
        """
        self.__server_interface = intf

    @property
    def server_handle(self):
        """Get the server RT handle.

        :return: Server RT handle.
        """
        return self.__server_handle

    @server_handle.setter
    def server_handle(self, handle):
        """Set the server RT handle.

        :param h: Server RT handle.
        :return: None
        """
        self.__server_handle = handle


class RTDHCPv4Server(RTDHCPServer):
    """DHCPv4 server

    """
    def __init__(self):
        """Initialize.

        """
        super().__init__()

        self.__family = 'ipv4'
        if bbe.bbevar == t:
            config = bbe.bbevar['user_variables']['uv-bbevar'].get('dhcpserver', {})
        else:
            config = bbe.bbevar.get('dhcpserver', {})
        v4_config = config.get('ipv4', {})

        self.server_mode = v4_config['mode']
        self.__lease_time = v4_config.get('lease-time', RTDHCPServerDefault.IPV4_LEASE_TIME)
        self.__pool_size = v4_config.get('pool-size', RTDHCPServerDefault.IPV4_POOL_SIZE)
        self.__pool_start_address = v4_config.get('pool-start-address', RTDHCPServerDefault.IPV4_POOL_START_ADDR)
        self.__pool_mask_length = v4_config.get('pool-mask-length', RTDHCPServerDefault.IPV4_POOL_MASK_LENGTH)
        self.__pool_gateway = v4_config.get('pool-gateway', RTDHCPServerDefault.IPV4_POOL_GATEWAY)

        self._multi_servers = v4_config.get('multi-servers', None)
        self._multi_servers_config = None   # no need to configure it if None
        if self._multi_servers is not None:
            self._multi_servers_config = dict()
            self._multi_servers_config['pool_inside_step'] = \
                self._multi_servers.get('pool-inside-step', RTDHCPServerDefault.IPV4_POOL_INSIDE_STEP)
            self._multi_servers_config['pool_gateway_inside_step'] = \
                self._multi_servers.get('pool-gateway-inside-step', RTDHCPServerDefault.IPV4_POOL_GATEWAY_INSIDE_STEP)
            self._multi_servers_config['pool_sizes'] = \
                self._multi_servers.get('pool-sizes', RTDHCPServerDefault.IPV4_POOL_SIZES)
            self._multi_servers_config['pool_start_addresses'] = \
                self._multi_servers.get('pool-start-addresses', RTDHCPServerDefault.IPV4_POOL_START_ADDRS)
            self._multi_servers_config['pool_mask_lengths'] = \
                self._multi_servers.get('pool-mask-lengths', RTDHCPServerDefault.IPV4_POOL_MASK_LENGTHS)
            self._multi_servers_config['pool_gateways'] = \
                self._multi_servers.get('pool-gateways', RTDHCPServerDefault.IPV4_POOL_GATEWAYS)
            self._multi_servers_config['lease_times'] = \
                self._multi_servers.get('lease-times', RTDHCPServerDefault.IPV4_LEASE_TIMES)
            self._multi_servers_config['subnet_addr_assign'] = \
                self._multi_servers.get('assign-ip-on-specific-subnet', RTDHCPServerDefault.IPV4_ADDR_ASSIGN)

    @property
    def family(self):
        """Get server family.

        :return: 'ipv4'
        """
        return self.__family

    @property
    def lease_time(self):
        """Get lease time

        :return: integer, lease time
        """
        return self.__lease_time

    @property
    def pool_size(self):
        """Get pool size

        :return: integer. Pool size.
        """
        return self.__pool_size

    @property
    def pool_start_address(self):
        """Get pool start address.

        :return: string. Pool start address.
        """
        return self.__pool_start_address

    @property
    def pool_mask_length(self):
        """Get pool mask length

        :return: integer. Pool mask length.
        """
        return self.__pool_mask_length

    @property
    def pool_gateway(self):
        """Get pool gateway

        :return: string. Pool gateway.
        """
        return self.__pool_gateway

    @property
    def multi_servers_config(self):
        """Get dhcpv4 multi-servers config.

        :return: None or dict.
        """
        return self._multi_servers_config


class RTDHCPv6Server(RTDHCPServer):
    """DHCPv6 server

    """
    def __init__(self):
        """Initialize.

        """
        super().__init__()

        self.__family = 'ipv6'

        if bbe.bbevar == t:
            config = bbe.bbevar['user_variables']['uv-bbevar'].get('dhcpserver', {})
        else:
            config = bbe.bbevar.get('dhcpserver', {})
        v6_config = config.get('ipv6', {})
        self.server_mode = v6_config['mode']
        self.__lease_time = v6_config.get('lease-time', RTDHCPServerDefault.IPV6_LEASE_TIME)
        self.__pool_size = v6_config.get('pool-size', RTDHCPServerDefault.IPV6_POOL_SIZE)
        self.__pool_start_address = v6_config.get('pool-start-address', RTDHCPServerDefault.IPV6_POOL_START_ADDR)
        self.__pool_mask_length = v6_config.get('pool-mask-length', RTDHCPServerDefault.IPV6_POOL_MASK_LENGTH)
        self.__pool_prefix_start = v6_config.get('pool-prefix-start', RTDHCPServerDefault.IPV6_POOL_PREFIX_START)
        self.__pool_prefix_length = v6_config.get('pool-prefix-length', RTDHCPServerDefault.IPV6_POOL_PREFIX_LENGTH)
        self.__pool_prefix_size = v6_config.get('pool-prefix-size', RTDHCPServerDefault.IPV6_POOL_PREFIX_SIZE)
        self.__pool_ia_type = v6_config.get('pool-ia-type', RTDHCPServerDefault.IPV6_IA_TYPE)

        self._multi_servers = v6_config.get('multi-servers', None)
        self._multi_servers_config = None   # no need to configure it if None
        if self._multi_servers is not None:
            self._multi_servers_config = dict()
            self._multi_servers_config['pool_inside_step'] = \
                self._multi_servers.get('pool-inside-step', RTDHCPServerDefault.IPV6_POOL_INSIDE_STEP)
            self._multi_servers_config['pool_prefix_inside_step'] = \
                self._multi_servers.get('pool-prefix-inside-step', RTDHCPServerDefault.IPV6_POOL_PREFIX_INSIDE_STEP)
            self._multi_servers_config['pool_sizes'] = \
                self._multi_servers.get('pool-sizes', RTDHCPServerDefault.IPV6_POOL_SIZES)
            self._multi_servers_config['pool_start_addresses'] = \
                self._multi_servers.get('pool-start-addresses', RTDHCPServerDefault.IPV6_POOL_START_ADDRS)
            self._multi_servers_config['pool_prefix_sizes'] = \
                self._multi_servers.get('pool-prefix-sizes', RTDHCPServerDefault.IPV6_POOL_PREFIX_SIZES)
            self._multi_servers_config['pool_prefix_starts'] = \
                self._multi_servers.get('pool-prefix-starts', RTDHCPServerDefault.IPV6_POOL_PREFIX_STARTS)
            self._multi_servers_config['pool_mask_lengths'] = \
                self._multi_servers.get('pool-mask-lengths', RTDHCPServerDefault.IPV6_POOL_MASK_LENGTHS)
            self._multi_servers_config['pool_prefix_lengths'] = \
                self._multi_servers.get('pool-prefix-lengths', RTDHCPServerDefault.IPV6_POOL_PREFIX_LENGTHS)

    @property
    def family(self):
        """Get server family.

        :return: 'ipv4'
        """
        return self.__family

    @property
    def lease_time(self):
        """Get lease time

        :return: integer, lease time
        """
        return self.__lease_time

    @property
    def pool_size(self):
        """Get pool size

        :return: integer. Pool size.
        """
        return self.__pool_size

    @property
    def pool_start_address(self):
        """Get pool start address.

        :return: string. Pool start address.
        """
        return self.__pool_start_address

    @property
    def pool_mask_length(self):
        """Get pool mask length

        :return: integer. Pool mask length.
        """
        return self.__pool_mask_length

    # @property
    # def pool_gateway(self):
    #     """Get pool gateway
    #
    #     :return: string. Pool gateway.
    #     """
    #     return self.__pool_gateway

    @property
    def pool_prefix_start(self):
        """Get pool prefix start.

        :return: string. Pool prefix start.
        """
        return self.__pool_prefix_start

    @property
    def pool_prefix_length(self):
        """Get pool prefix length.

        :return: integer. Pool prefix length.
        """
        return self.__pool_prefix_length

    @property
    def pool_prefix_size(self):
        """Get pool prefix size

        :return: integer. pool prefix size
        """
        return self.__pool_prefix_size

    @property
    def pool_ia_type(self):
        """Get pool ia type

        :return: string. Pool ia type.
        """
        return self.__pool_ia_type

    @property
    def multi_servers_config(self):
        """Get dhcpv6 multi-servers config.

        :return: None or dict.
        """
        return self._multi_servers_config
