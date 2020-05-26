# Copyright 2016- Juniper Networks
# Toby BBE development team

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


class BBEVarDevice:
    """Property class representing a device in bbevar.

    BBEVarDevice represents a device and its associated properties.
    The properties represent  values in bbrvar but convenient to access.

    A device may not have all the properties. If not, the property value is None.
    For example, a router device does not have 'device_labserver'.

    """

    def __init__(self, bvar, device_id):
        """Initialize

        :param bvar: bbevar with all topology info (for now it is combined bbevar and t var)
        :param device_id: string device id, e.g., 'r0'
        """
        self.__device_id = device_id
        self.__device_name = bvar['resources'][device_id]['system']['primary'].get('name', None)
        # mgt-ip and domain are no longer available there with latest toby-find
        #self.__device_domain = bvar['resources'][device_id]['system']['primary'].get('domain', None)
        #self.__device_mgt_ip = bvar['resources'][device_id]['system']['primary'].get('mgt-ip', None)
        self.__device_controllers = bvar['resources'][device_id]['system']['primary'].get('controllers', None)
        self.__device_os = bvar['resources'][device_id]['system']['primary'].get('osname', None)
        # TODO stop using os if Togy-find creates ymal using osname only
        if not self.__device_os:
            self.__device_os = bvar['resources'][device_id]['system']['primary'].get('os', None)
        self.__device_model = bvar['resources'][device_id]['system']['primary'].get('model', None)
        self.__device_make = bvar['resources'][device_id]['system']['primary'].get('make', None)
        self.__device_labserver = bvar['resources'][device_id]['system']['primary'].get('labserver', None)
        self.__device_handle = bvar['resources'][device_id]['system'].get('dh', None)
        if bvar == t:
            self.__device_config = bvar['resources'][device_id]['system']['primary'].get('uv-bbe-config', None)
        else:
            self.__device_config = bvar['resources'][device_id].get('config', None)

        if self.__device_config:
            self.__device_tags = self.__device_config.get('tags', [])
        else:
            self.__device_tags = []

        try:
            self.__intf_list = [intf for intf in bvar['resources'][device_id]['interfaces']]
        except (KeyError, TypeError):
            self.__intf_list = []

        # device may not have tags
        try:
            self.__is_dut = 'dut' in self.__device_config['tags']
        except (KeyError, TypeError):
            self.__is_dut = False

        try:
            self.__is_lns = 'lns' in self.__device_config['tags']
        except (KeyError, TypeError):
            self.__is_lns = False

        try:
            self.__is_mxvc = 'mxvc' in self.__device_config['tags']
        except (KeyError, TypeError):
            self.__is_mxvc = False

        # tomcat only applies to Junos devices
        try:
            self.__is_tomcat = 'non-tomcat' not in self.__device_config['tags']
        except (KeyError, TypeError):
            self.__is_tomcat = True if self.__device_os.lower() == 'junos' else False

        try:
            assert isinstance(self.__device_config['vrf'], dict)
            self.__has_vrf = True
            self.__vrf = self.__device_config['vrf'].get('names', None)
        except (KeyError, TypeError, AssertionError):
            self.__has_vrf = False
            self.__vrf = None

        try:
            assert isinstance(self.__device_config['quickcst'], dict)
            self.__is_quickcst = True
            self.__quickcst_file = self.__device_config['quickcst'].get('skip', None)
        except (KeyError, TypeError, AssertionError):
            self.__has_vrf = False
            self.__vrf = None

    @property
    def device_tags(self):
        """Get device tags.

        :return: list (maybe empty) of device tags
        """
        return self.__device_tags

    @property
    def has_vrf(self):
        """If the device has vrf defined

        :return: boolean, True if the device has vrf, False otherwise
        """
        return self.__has_vrf

    @property
    def vrf(self):
        """Get vrf

        Note: recommend to call has_vrf() before access vrf, and expect None value.

        :return: iterator object of Vrf
        """
        return self.__vrf

    @property
    def device_id(self):
        """Get device id

        :return: None or string device id, e.g., 'r0'
        """
        return self.__device_id

    @property
    def device_name(self):
        """Get physical device name

        :return: None or string physical device name, e.g., 'r1mx960wf'
        """
        return self.__device_name

    @property
    def device_controllers(self):
        """Get device device_controllers data

        :return: None or dict of device controllers data
        """
        return self.__device_controllers

    # @property
    # def device_mgt_ip(self):
    #     """Get device management IP address
    #
    #     :return: None or string device management IP, e.g., '10.227.2.1'
    #     """
    #     return self.__device_mgt_ip

    @property
    def device_os(self):
        """Get device OS

        Note: The os is based on the name from pbuilder or toby-find.
        Not all device has os, for example. IXIA rt has osname bot bot os.

        :return: None or string device os, e.g., 'JunOS'
        """
        return self.__device_os

    @property
    def device_model(self):
        """Get device model

        :return: None or string device model, e.g., 'mx960', 'linux'
        """
        return self.__device_model

    @property
    def device_make(self):
        """Get device make

        :return: None or string device make, e.g., 'juniper'
        """
        return self.__device_make

    @property
    def device_labserver(self):
        """Get device labserver

        Note: only RT has labserver

        :return: None or string RT device labserver, e.g., 'harpoon.englab.juniper.net'
        """
        return self.__device_labserver

    @property
    def device_handle(self):
        """Get device handle object

        :return: object of device handle
        """
        return self.__device_handle

    @property
    def device_config(self):
        """Get device config dict as it is in bbevar

        Use device_config if certain config is required by script
        but does not in this class's properties.

        :return: dict of device config as it is in bbevar, not including the 'config' keyword.
        """
        return self.__device_config

    @property
    def device_interfaces(self):
        """Get device interface

        :return: list of dvice interfaces, e.g., [access-0, uplink-0]
        """
        return self.__intf_list

    @property
    def is_dut(self):
        """If this device is dut

        Note: A device need 'dut' in config file tags to be identified as dut.

        :return: boolean, True if this device is a dut. False otherwise.
        """
        return self.__is_dut

    @property
    def is_lns(self):
        """If this device is a lns.

        Note: A device need 'lns' in config file tags to be identified as lns.

        :return: boolean, True if this device is a lns. False otherwise.
        """
        return self.__is_lns

    @property
    def is_mxvc(self):
        """If this device is a mxvc.

        Note: A device need 'mxvc' in config file tags to be identified as mxvc.

        :return: boolean, True if this device is a mxvc. False otherwise.
        """
        return self.__is_mxvc

    @property
    def is_tomcat(self):
        """If this device has tomcat junos software.

        Note: A device need 'non-tomcat' in config file tags to be identified as not being tomcat.

        :return: boolean, True if this device is has tomcat build. False otherwise.
        """
        return self.__is_tomcat

    def __str__(self):
        return 'Device {}: {}'.format(self.device_id, self.device_name)
