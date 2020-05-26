# Copyright 2016- Juniper Networks
# Toby BBE development team
"""
A Interface class that used to initialize the interface attributes defined in yaml files
"""
#import ipaddress
import re
from jnpr.toby.bbe.version import get_bbe_version
import collections

__author__ = ['Yong Wang']
__credits__ = ['Benjamin Schurman']
__contact__ = 'ywang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'
__version__ = get_bbe_version()

VlanRange = collections.namedtuple('VlanRange', 'start, \
                                                 step, \
                                                 repeat, \
                                                 length')
VlanRange.__doc__ = """Vlan range for inner or outer vlans.

Fields:
    start: integer, VLAN start id
    step: integer, VLAN id step
    repeat: integer, VLAN id repeat. E.g., if start=1, step=1, repeat=2,
            VLAN ids is like 1122334455...
    length: vlan sequence length
"""

# For robot framework
ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
ROBOT_LIBRARY_VERSION = get_bbe_version()

class BBEVarInterface:
    """Property class representing a device interface in bbevar.

    BBEVarInterface represents a device interface and its associated properties.
    """

    def __init__(self, bvar, device_id, interface_id):
        """Initialize

        :param bvar: bbevar with all topology info (for now it is combined bbevar and t var)
        :param device_id: string device id, e.g., 'r0'
        :param interface_id: string interface id, e.g., 'acess0'
        """
        self.__device_id = device_id
        self.__intf_id = interface_id
        self.__device_name = bvar['resources'][device_id]['system']['primary'].get('name', None)
        self.__device_mgt_ip = bvar['resources'][device_id]['system']['primary'].get('mgt-ip', None)
        self.__device_handle = bvar['resources'][device_id]['system']['primary'].get('dh', None)
        self.__intf_link = bvar['resources'][device_id]['interfaces'][interface_id].get('link', None)
        self.__intf_name = bvar['resources'][device_id]['interfaces'][interface_id].get('name', None)
        self.__intf_pic = bvar['resources'][device_id]['interfaces'][interface_id].get('pic', None)
        # address issue where port documented as #/#/# instead of #/#
        if device_id.count("rt"):
            if re.search(r"^\d+\/\d+\/\d+", self.__intf_pic):
                self.__intf_pic = re.sub(r"^\d+\/", "", self.__intf_pic)
            elif re.search(r"^[a-z]+-\d+\/\d+\/\d+", self.__intf_pic):
                self.__intf_pic = re.sub(r"^[a-z]+-\d+\/", "", self.__intf_pic)
        self.__intf_type = bvar['resources'][device_id]['interfaces'][interface_id].get('type', [])
        if bvar == t:
            self.__intf_config = bvar['resources'][device_id]['interfaces'][interface_id].get('uv-bbe-config', {})
        else:
            self.__intf_config = bvar['resources'][device_id]['interfaces'][interface_id].get('config', {})
        self.vlan_range = None
        self.svlan_range = None
        if self.__intf_config:
            vlan_config = self.__intf_config.get('vlan', None)
            svlan_config = self.__intf_config.get('svlan', None)

            if vlan_config:
                vlan_start = vlan_config['start']
                vlan_step = vlan_config.get('step', '1')
                vlan_repeat = vlan_config.get('repeat', '1')
                vlan_length = vlan_config.get('length', '1')
                self.vlan_range = VlanRange(vlan_start, vlan_step, vlan_repeat, vlan_length)
                self.vlan_tpid = vlan_config.get('tpid', '0x8100')
            elif 'uplink0' in interface_id:
                self.vlan_range = VlanRange('1', '1', '1', '1')
                self.vlan_tpid = '0x8100'

            if svlan_config:
                vlan_start = svlan_config['start']
                vlan_step = svlan_config.get('step', '1')
                vlan_repeat = svlan_config.get('repeat', '1')
                vlan_length = svlan_config.get('length', '1')
                self.svlan_range = VlanRange(vlan_start, vlan_step, vlan_repeat, vlan_length)
                self.svlan_tpid = svlan_config.get('tpid', '0x8100')

        self.__rt_device_group_handle = None
        self.__rt_ethernet_handle = None
        self.__rt_ipv4_handle = None
        self.__rt_ipv6_handle = None
        self.__rt_lns_handle = None
        self.__rt_lns_server_session_handle = None
        self.rt_lacp_handle = None
        try:
            assert isinstance(self.__intf_config['ae'], dict)

            self.ae_enable = self.__intf_config['ae'].get('enable', '0')
            if int(self.ae_enable) > 0:
                self.__is_ae = True
            else:
                self.__is_ae = False
            self.__ae_bundle = self.__intf_config['ae'].get('bundle', None)
            self.__ae_active = self.__intf_config['ae'].get('active', False)
        except (KeyError, TypeError, AssertionError):
            self.__is_ae = False
            self.__ae_bundle = ''
            self.__ae_active = False

        try:
            assert isinstance(self.__intf_config, dict)
            self.__intf_desc = self.__intf_config.get('description', '')
        except (KeyError, TypeError, AssertionError):
            self.__intf_desc = ''

    @property
    def device_id(self):
        """Get device id

        :return: string device id, e.g., 'r0'
        """
        return self.__device_id

    @property
    def device_name(self):
        """Get physical device name

        :return: string device name, e.g., 'r100mx960wf'
        """
        return self.__device_name

    @property
    def device_mgt_ip(self):
        """Get device management ip

        :return: string device menagement ip, e.g., '10.227.2.10'
        """
        return self.__device_mgt_ip

    @property
    def device_handle(self):
        """Get device handle object

        :return: object of device handle
        """
        return self.__device_handle

    @property
    def interface_id(self):
        """Get interface id

        :return: string interface id, e.g., 'access0'
        """
        return self.__intf_id

    @property
    def interface_name(self):
        """Get physical interface name

        :return: string physical interface name, e.g., 'ge-1/0/0.0'
        """
        return self.__intf_name

    @property
    def interface_link(self):
        """Get interface link

        :return: string interface link, e.g., 'access0'
        """
        return self.__intf_link

    @property
    def interface_pic(self):
        """Get interface pic

        :return: string interface pic, e.g., 'xe-2/0/0'
        """
        return self.__intf_pic

    @property
    def interface_type(self):
        """Get interface type

        :return: list of interface type, such as [either, ge]
        """
        return self.__intf_type

    @property
    def interface_config(self):
        """Get interface config details

        :return: dict of interface config as it is in bbevar, not including the 'config' keyword.
        """
        return self.__intf_config

    @property
    def interface_description(self):
        """Get interface description

        :return: string interface description
        """
        return self.__intf_desc

    @property
    def is_ae(self):
        """If this interface is ae interface

        :return: boolean True if it is ae, False otherwise
        """
        return self.__is_ae

    @property
    def ae_bundle(self):
        """Get ae bundle name

        :return: string. AE bundle name or empty string if not using ae
        """
        return self.__ae_bundle

    @property
    def is_ae_active(self):
        """If the interface is active ae member

        :return: boolean. True if active.
        """
        return self.__ae_active

    @property
    def rt_device_group_handle(self):
        """Get RT device group handle associated with the interface.

        The handle is returned by rt.add_link()

        :return: RT device group handle
        """
        return self.__rt_device_group_handle

    @rt_device_group_handle.setter
    def rt_device_group_handle(self, handle):
        """Set RT device group handle associated with the interface.

        The handle is returned by rt.add_link()

        :param h: RT device group handle
        :return: None
        """
        self.__rt_device_group_handle = handle

    @property
    def rt_ethernet_handle(self):
        """Get RT ethernet handle associated with the interface.

        The handle is returned by rt.add_link()

        :return: RT ethernet handle
        """
        return self.__rt_ethernet_handle

    @rt_ethernet_handle.setter
    def rt_ethernet_handle(self, handle):
        """Set RT ethernet handle associated with the interface.

        The handle is returned by rt.add_link()

        :param h: RT ethernet handle
        :return: None
        """
        self.__rt_ethernet_handle = handle

    @property
    def rt_ipv4_handle(self):
        """Get RT IPv4 handle associated with the interface.

        The handle is returned by rt.add_link()

        :return: RT IPv4 handle
        """
        return self.__rt_ipv4_handle

    @rt_ipv4_handle.setter
    def rt_ipv4_handle(self, handle):
        """Set RT IPv4 handle associated with the interface.

        The handle is returned by rt.add_link()

        :param h: RT IPv4 handle
        :return: None
        """
        self.__rt_ipv4_handle = handle

    @property
    def rt_ipv6_handle(self):
        """Get RT IPv6 handle associated with the interface.

        The handle is returned by rt.add_link()

        :return: RT IPv6 handle
        """
        return self.__rt_ipv6_handle

    @rt_ipv6_handle.setter
    def rt_ipv6_handle(self, handle):
        """Set RT IPv6 handle associated with the interface.

        The handle is returned by rt.add_link()

        :param h: RT IPv6 handle
        :return: None
        """
        self.__rt_ipv6_handle = handle

    @property
    def rt_lns_handle(self):
        """Get RT IPv6 handle associated with the interface.

        The handle is returned by rt.add_l2tp_server()

        :return: RT IPv6 handle
        """
        return self.__rt_lns_handle

    @rt_lns_handle.setter
    def rt_lns_handle(self, handle):
        """Set RT LNS handle associated with the interface.

        The handle is returned by rt.add_l2tp_server()

        :param handle: RT LNS handle
        :return: None
        """
        self.__rt_lns_handle = handle

    @property
    def rt_lns_server_session_handle(self):
        """Get RT IPv6 handle associated with the interface.

        The handle is returned by rt.add_l2tp_server()

        :return: RT LNS server session handle
        """
        return self.__rt_lns_server_session_handle

    @rt_lns_server_session_handle.setter
    def rt_lns_server_session_handle(self, handle):
        """Set RT LNS handle associated with the interface.

        The handle is returned by rt.add_l2tp_server()

        :param handle: RT LNS handle
        :return: None
        """
        self.__rt_lns_server_session_handle = handle

    def __str__(self):
        return 'Interface {}: {} on {}: {}'.format(self.interface_id, self.interface_name,
                                                   self.device_id, self.device_name)

