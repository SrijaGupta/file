# Copyright 2016- Juniper Networks
# Toby BBE development team
"""
The class is used to initialize the yaml files and generate a builtin bbe
"""
import builtins
import re
import json
from jnpr.toby.bbe.version import get_bbe_version
from jnpr.toby.bbe.errors import BBEVarError, BBESubscriberError
from jnpr.toby.bbe.bbevar.interfaces import BBEVarInterface
from jnpr.toby.bbe.bbevar.devices import BBEVarDevice
from jnpr.toby.bbe.bbevar.subscribers import DHCPSubscribers, PPPoESubscribers, L2TPSubscribers, L2BSASubscribers,\
    HAGSubscribers, CUPSSubscribers, PGWSubscribers, FWASubscribers
from jnpr.toby.bbe.bbevar.rtdhcpserver import RTDHCPv4Server, RTDHCPv6Server

__author__ = ['Yong Wang']
__credits__ = ['Benjamin Schurman']
__contact__ = 'ywang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'
__version__ = get_bbe_version()

# For robot framework
ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
ROBOT_LIBRARY_VERSION = get_bbe_version()


class BBEVars:
    """This class provides operations for accessing bbevar.

    bbevar is basically a Python dictionary loaded from BBE configuration YAML file.
    The bbe initialize method from bbeinit.BBEInit class is responsible for loading
    the BBE configuration YAML file and initialize the bbevar using this class's initialize
    method.

    An instance of this class is set as builtins.bbe. So bbe object is used to access
    bbevar itself and public methods from this class.

    To access bbevar directly, use bbe.bbevar as dictionary
    To use helper methods from this class, use bbe.methodname()

    """

    def __init__(self):
        """Initialize internal containers and set self as Python builtins.bbe

        """

        self.log_tag = '[BBEVAR]'

        self.bbevar = {}         # bbevar

        # Helper data structures
        self._bbet = {}             # combined bbevar and t var
        self._connections = {}      # connections dict
        self._devices = {}          # devices dict
        self._interfaces = {}       # interfaces dict
        self._subscribers = []      # Subscribers instances list
        self._rt_dhcps_ervers = {}  # RT DHCP servers
        self.cst_stats = {}         # BBE statistics

        # The instance can be accessed by bbe
        builtins.bbe = self

       # t.log('{} BBEVars instantiated'.format(self.log_tag))

    def initialize(self, bbevar):
        """Initialize bbevar

        :param bbevar: dictionary loaded from bbe configuration yaml file
        :return: None
        """

        t.log('{} Initializing BBEVars'.format(self.log_tag))
        if bbevar != t:
            # update bbevar with yaml loaded BBE configuration file
            self.bbevar.update(bbevar)

            # store vrf name iterator object if configured
            # this operation should be done before _init_devices
            # such that BBEVarDevice has valid vrf property.
            self._generate_vrf()

            # Combine bbevar and t. t has topology (incomplete at present)
            # and bbevar has BBE configuration (and partial topology at present)
            try:
                self._bbet = self.bbevar.copy()
                self._bbet = self._dict_merge(t.__dict__, self._bbet)
            except NameError:
                raise BBEVarError('t does not exist. Please initialize Toby first')
        else:
            self._bbet = t
            self.bbevar = t
        # Initialize self._devices
        self._init_devices()

        # Initialize self._interfaces
        self._init_interfaces()

        # Initialize self._connections. A connection is represented by one end point
        # BBEVarInterface as key, the other end point BBEVarInterface as value
        self._init_connections()

        # Initialize subscribers
        self._init_subscribers()

        # Initialized dhcp servers
        # bbert.add_rt_dhcp_servers() will set interface and handle for the servers
        # if servers are needed
        self._rt_dhcps_ervers['ipv4'] = RTDHCPv4Server()
        self._rt_dhcps_ervers['ipv6'] = RTDHCPv6Server()


        t.log('{} BBEVars initialized'.format(self.log_tag))

    def _init_devices(self):
        """Initialize self._devices

        Initialize self._devices dict using devices IDs (e.g., 'r0', 'h0', 'rt0')
        as keys and instances of BBEVarDevice as values.

        :return: None
        """

        t.log('{} Initializing BBEVars devices'.format(self.log_tag))

        try:
            assert isinstance(self._bbet['resources'], dict)
        except (KeyError, TypeError, AssertionError):
            t.log('ERROR', '{} No resource found'.format(self.log_tag))
            raise BBEVarError('No resource found')

        # Iterate through devices
        for a_dev in self._bbet['resources'].keys():
            try:
                assert isinstance(self._bbet['resources'][a_dev], dict)
            except (KeyError, TypeError, AssertionError):
                # Allow devices there without any value
                self._devices[a_dev] = None
                continue

            # Create BBEVarDevice
            self._devices[a_dev] = BBEVarDevice(self._bbet, a_dev)
            t.log('{} Created BBEVars device {}'.format(self.log_tag, a_dev))

        t.log('{} Initialized BBEVars devices'.format(self.log_tag))

    def _init_interfaces(self):
        """Initialize self._interfaces

        Initialize self._interfaces dict. Keys are {device_id][interface_id]
         and a value is an instances of BBEVarDevice.
         Devices IDs are like 'r0', 'h0', 'rt0'.
         Interface IDs are like 'access-0', 'transit-1', 'uplink-0', 'radius-0'.

        :return: None
        """

        t.log('{} Initializing BBEVars interfaces'.format(self.log_tag))

        # a couple of re to match rt uplinks
        #rt_re = re.compile(r'rt', re.IGNORECASE)
        #uplink_re = re.compile(r'uplink', re.IGNORECASE)

        try:
            assert isinstance(self._bbet['resources'], dict)
        except (KeyError, TypeError, AssertionError):
            t.log('ERROR', '{} No resource found'.format(self.log_tag))
            raise BBEVarError('No resource found')

        # parse to find all interfaces and to which devices it belong
        for a_dev in self._bbet['resources'].keys():
            try:
                assert isinstance(self._bbet['resources'][a_dev]['interfaces'], dict)
            except (KeyError, TypeError, AssertionError):
                continue

            for an_intf in self._bbet['resources'][a_dev]['interfaces'].keys():
                if a_dev not in self._interfaces:
                    self._interfaces[a_dev] = {}

                # if uplink_re.match(an_intf):
                #     if rt_re.match(a_dev):
                #         # RT uplink
                #         self._interfaces[a_dev][an_intf] = BBEVarRTUplink(self._bbet, a_dev, an_intf)
                #         # set interface values
                #         self._interfaces[a_dev][an_intf].set_values()
                #     else:
                #         # Router uplink
                #         self._interfaces[a_dev][an_intf] = BBEVarRouterUplink(self._bbet, a_dev, an_intf)
                #         # set interface values
                #         self._interfaces[a_dev][an_intf].set_values()
                # else:
                #     # non uplink
                self._interfaces[a_dev][an_intf] = BBEVarInterface(self._bbet, a_dev, an_intf)

                t.log('{} Created BBEVars interface {}: {}'.format(self.log_tag, a_dev, an_intf))

        t.log('{} Initialized BBEVars interfaces'.format(self.log_tag))

    def _init_connections(self):
        """Initialize self._connections

        Use topology information to create connections mapping. A connection is
        an key value pair using BBEVarInterface objects as key and value.

        :return: None
        """

        t.log('{} Initializing BBEVars connections'.format(self.log_tag))

        try:
            assert isinstance(self._bbet['resources'], dict)
        except (KeyError, TypeError, AssertionError):
            t.log('ERROR', '{} No resource found'.format(self.log_tag))
            raise BBEVarError('No resource found')

        # interfaces and devices mapping, e.g., intf_dev['access-0'] = ['r0', 'rt0']
        intf_dev = {}

        # parse to find all interfaces and to which devices it belong
        for device in self._bbet['resources'].keys():
            try:
                assert isinstance(self._bbet['resources'][device]['interfaces'], dict)
            except (KeyError, TypeError, AssertionError):
                continue

            for intf in self._bbet['resources'][device]['interfaces'].keys():
                if intf in intf_dev:
                    intf_dev[intf].append(device)
                else:
                    intf_dev[intf] = [device]

        # init connections
        for an_intf in intf_dev:
            if len(intf_dev[an_intf]) != 2:
                # If this is an orphaned link, skip it in the connections list
                t.log('info', 'Interface {} does not connect two devices. Only connected to {}. Skipping...' \
                      .format(an_intf, intf_dev[an_intf]))
                continue

            connectors = []
            for a_dev in intf_dev[an_intf]:
                #connectors.append(self.get_interfaces(a_dev, an_intf)[0])
                for interface in self.get_interfaces(a_dev, an_intf):
                    if interface.interface_id == an_intf:
                        connectors.append(interface)
            self._connections[(connectors[0].device_id, connectors[0].interface_id)] = connectors[1]
            self._connections[(connectors[1].device_id, connectors[1].interface_id)] = connectors[0]

            t.log('{} Created connection between {}: {} and {}: {}'.format(self.log_tag,
                                                                           connectors[0].device_id,
                                                                           connectors[0].interface_id,
                                                                           connectors[1].device_id,
                                                                           connectors[1].interface_id))

        t.log('{} Initialized BBEVars connections'.format(self.log_tag))

    def _init_subscribers(self):
        """Create BBEVarSubscribers instances based on configuration

        This function is called after BBEVars._init_interfaces()
        by BBEVar.initialize().

        :return: None
        """

        t.log('{} Initializing BBEVars subscribers'.format(self.log_tag))

        # Find the device with subscribers configuration
        # rt, switch, and a router all could have access interfaces

        # Find BBEDevice subscribers are defined
        subscriber_router = None
        access_routers = self.get_devices(interfaces='access', id_only=False)
        if len(access_routers) == 0:
            t.log('WARN', '{} Did not find any device with access interface'.format(self.log_tag))
            return None

        if len(access_routers) == 1:
            # this must be the one candidate
            subscriber_router = access_routers[0]
        else:
            for router in access_routers:
                ar_os = router.device_os
                #import sys; import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
                if not re.match(r'junos', ar_os, re.IGNORECASE):
                    continue

                for intf in self.get_interfaces(router.device_id, interfaces='access', id_only=False):
                    try:
                        assert isinstance(intf.interface_config['subscribers'], dict)
                    except (KeyError, TypeError, AssertionError):
                        continue
                    else:
                        subscriber_router = router
                        break
                if not subscriber_router:
                    t.log("this router {} is not access router, skipping init_subscriber".format(router.device_id))
                    continue
                # Get rt
                access_rt = self.get_devices(devices='rt', interfaces='access', id_only=True)
                if len(access_rt) == 0:
                    raise BBESubscriberError('No rt with access interface')

                # This is rt, mostly 'rt0'
                #subscriber_routert = access_rt[0]

                # A list of BBEVarInterface
                r_access_intfs = self.get_interfaces(device=subscriber_router.device_id, interfaces='access', id_only=False)

                for r_intf in r_access_intfs:
                    # Check if the interface has subscribers defined
                    try:
                        assert isinstance(r_intf.interface_config['subscribers'], dict)
                    except (KeyError, TypeError, AssertionError):
                        continue

                    for subs_type in r_intf.interface_config['subscribers'].keys():
                        subs_type = subs_type.lower()  # dhcp, pppoe
                        # a list of subscriber groups
                        subs_groups = r_intf.interface_config['subscribers'][subs_type]
                        for a_group in subs_groups:
                            group_tag = a_group.get('tag', None)
                            if group_tag is None:
                                raise BBESubscriberError('Missing subscriber tag in {}'.format(r_intf.interface_id))

                            # get the specific rt BBEVarInterface, should be only one in the list
                            # otherwise the bbe config yaml is not correctly defined
                            #to support more than 1 testers
                            for subscriber_routert in access_rt:
                                rt_intfs = self.get_interfaces(subscriber_routert, interfaces=r_intf.interface_id)
                                if rt_intfs:
                                    break
                            #rt_intf = rt_intfs[0]
                            for rt_intf in rt_intfs:
                                if rt_intf.interface_id == r_intf.interface_id:
                                    break
                            if subs_type == 'dhcp':
                                subs_obj = DHCPSubscribers(r_intf, rt_intf, subs_type, group_tag)
                            elif subs_type == 'pppoe':
                                subs_obj = PPPoESubscribers(r_intf, rt_intf, subs_type, group_tag)
                            elif subs_type == 'l2tp':
                                subs_obj = L2TPSubscribers(r_intf, rt_intf, subs_type, group_tag)
                            elif subs_type == 'l2bsa':
                                subs_obj = L2BSASubscribers(r_intf, rt_intf, subs_type, group_tag)
                            elif subs_type == 'cups':
                                subs_obj = CUPSSubscribers(r_intf, rt_intf, subs_type, group_tag)
                            elif subs_type == 'pgw':
                                subs_obj = PGWSubscribers(r_intf, rt_intf, subs_type, group_tag)
                            elif subs_type == 'hag':
                                subs_obj = HAGSubscribers(r_intf, rt_intf, subs_type, group_tag)
                            elif subs_type == 'fwa':
                                subs_obj = FWASubscribers(r_intf, rt_intf, subs_type, group_tag) 
                            else:
                                raise BBESubscriberError('{} is not a supported subscriber type'.format(subs_type))

                            # note that self._subscribers is a list, so it is ordered
                            # RT clients will be added based on this order.
                            # Setting rt csr relies on the order
                            self._subscribers.append(subs_obj)

                            t.log('{} Created BBEVarSubscribers {} from {} {} with tag {}'.format(self.log_tag,
                                                                                                  subs_type,
                                                                                                  r_intf.device_id,
                                                                                                  r_intf.interface_id,
                                                                                                  group_tag))

        if not subscriber_router:
            t.log('WARN', '{} Did not find any JUNOS device with subscribers defined'.format(self.log_tag))
            return None
        t.log('{} Initialized BBEVars subscribers'.format(self.log_tag))


    def _generate_vrf(self):
        """Generate vrf iterator object in bbevar.

        If a device has vrf defined, instantiate a Vrf instance and store
        the object at bbevar['resources'][dev]['config']['vrf']['names'].

        :return: None
        """

        t.log('{} Generate BBEVars VRF iterator if configured'.format(self.log_tag))

        try:
            assert isinstance(self.bbevar['resources'], dict)
        except (KeyError, TypeError, AttributeError, AssertionError):
            return None

        for dev in self.bbevar['resources'].keys():
            try:
                if self.bbevar == t:
                    assert isinstance(self.bbevar['resources'][dev]['system']['primary']['uv-bbe-config']['vrf'], dict)
                else:
                    assert isinstance(self.bbevar['resources'][dev]['config']['vrf'], dict)
            except (KeyError, TypeError, AssertionError):
                #  log the err message when log is available
                continue
            if self.bbevar != t:
                vrf_iter = Vrf(**self.bbevar['resources'][dev]['config']['vrf'])
                self.bbevar['resources'][dev]['config']['vrf']['names'] = vrf_iter
            else:
                vrf_iter = Vrf(**self.bbevar['resources'][dev]['system']['primary']['uv-bbe-config']['vrf'])
                self.bbevar['resources'][dev]['system']['primary']['uv-bbe-config']['vrf']['names'] = vrf_iter

            t.log('{} Generated BBEVars VRF iterator for device {}'.format(self.log_tag, dev))

    def get_connection(self, device='r0', interface='access0'):
        """Get the other side of the connection from the given device and interface ids.

        The connection is represented by an BBEVarInterface instance. If the connection
        is found, an BBEVarInterface is returned. User can use properties of the object
        for further processing.

        Usage:
            >>> con = bbe.get_connection()
            <jnpr.toby.bbe.bbevar.interfaces.BBEVarInterface object at 0x7f08681d94e0>
            >>> str(con)
            'Interface access0: 9/7 on rt0: harpoon-ixchassis'
            >>> con.device_id
            'rt0'
            >>> con.interface_id
            'access0'
            >>> con.interface_name
            '9/7'
            >>> radcon = bbe.get_connection('h0', 'radius0')
            >>> radcon
            <jnpr.toby.bbe.bbevar.interfaces.BBEVarInterface object at 0x7f08681d9390>
            >>> str(radcon)
            'Interface radius0: xe-0/1/3.0 on r0: r46mx480wf'
            >>> radcon.interface_name
            'xe-0/1/3.0'
            >>> radcon.device_name
            'r46mx480wf'
            >>> radcon.device_id
            'r0'
            >>> radcon1 = bbe.get_connection('h0', 'radius1')
            >>> radcon is None
            True

        :param device: device id (such as r0, h0)
        :param interface: interface id (such as access0, uplink0, radius0).
        :return: The BBEVarInterface object at the other end of the connection.
        Returns None if no connection is found.
        """

        for con in self._connections:
            if device in con and interface in con:
                return self._connections[con]

    def dump(self, indent=4):
        """Dump bbevar nicely.

        obselete -- the handles stored by Tody is not json dumpable
        Using json dumps to dump bbevar with nice format when the returned string is printed.

        :param indent: indent level
        :return: string representation of bbevar
        """
        return json.dumps(self.bbevar, indent=indent)

    def get_bbevar_by_keys(self, keylist):
        """Get bbevar value by keys

        :param keylist:  Key list.
            Keys in keylist should start from the root of bbevar.
            If keylist is empty, return bbevar as a whole.

        :return: value by keys, or None if value is None or keys do not exist.
        """
        # wrong argument
        if not isinstance(keylist, list):
            #  log the err message when log is available
            return None

        # no key given, return all
        if len(keylist) == 0:
            return self.bbevar

        bv_attr = self.bbevar        # already guaranteed that __bbevar is a dictionary in initialize_bbevar
        for item in keylist:
            if item not in bv_attr:
                #  log the err message when log is available
                return None

            bv_attr = bv_attr.get(item)

            if item != keylist[-1]:  # do not allow None and non-dict in the middle
                if bv_attr is None or not isinstance(bv_attr, dict):
                    #  log the err message when log is available
                    return None

        return bv_attr

    def get_devices(self, devices=None, device_tags=None, interfaces=None, id_only=False):
        """Get devices that satisfies filters specified by kwargs

        Each device is represented by an instance of BBEVarDevice unless id_only is True.
        Keyword arguments specify filters for the desired device. The filters forms logical
        AND or the operation.

        Example sage:

            # Get a single device in the form of BBEVarDevice
            >>> bbe.get_devices(devices='r0')
            [<jnpr.toby.bbe.bbevar.devices.BBEVarDevice object at 0x7f270821f390>]

            # Get all devices IDs
            >>> all_dev_ids = bbe.get_devices(id_only=True)
            >>> all_dev_ids
            ['r1', 'src0', 'rt0', 'h0', 'r0']

            # Get all devices in the form of BBEVarDevice
            >>> all_dev = bbe.get_devices()
            >>> len(all_dev)
            4
            >>> all_dev[0]
            <jnpr.toby.bbe.bbevar.devices.BBEVarDevice object at 0x7f270821f390>

            >>> all_dev[0].device_id
            'r0'
            >>> all_dev[0].device_name
            'r46mx480wf'

            # Get all device IDs which have uplink interfaces
            >>> uplink_dev = bbe.get_devices(interfaces='uplink', id_only=True)
            >>> uplink_dev
            ['rt0', 'r1']

            # Get all device IDs whcih have access or uplink interfacaes
            >>> intf_dev = bbe.get_devices(interfaces=['acc', 'up'], id_only=True)
            >>> intf_dev
            ['rt0', 'r0', 'r1']

            # Get dut
            >>> dut = bbe.get_devices(device_tags='dut')[0]
            >>> dut
            <jnpr.toby.bbe.bbevar.devices.BBEVarDevice object at 0x7f42b8655438>
            >>> str(dut)
            'Device r0: r46mx480wf'
            >>> dut.device_id
            'r0'
            >>> dut.device_name
            'r46mx480wf'
            >>> dut.has_vrf
            True
            >>> dut.vrf
            Vrf(base=RETAILER, start=1, step=1, count=10)
            >>> for v in dut.vrf:
            ...   print(v)
            ...
            RETAILER1
            RETAILER2
            RETAILER3
            RETAILER4
            RETAILER5
            RETAILER6
            RETAILER7
            RETAILER8
            RETAILER9
            RETAILER10
            >>> dut.is_tomcat
            True
            >>> dut.is_mxvc
            False

            # Get lns
            >>> lns = bbe.get_devices(device_tags='lns')[0]
            >>> lns.device_id
            'r1'
            >>> lns.device_name
            'r47mx480wf'
            >>> lns.device_interfaces
            ['uplink1', 'uplink0', 'transit0', 'transit1']


        :param devices: Device IDs.
        Optional.
        Device ids are like 'r0', 'rt0', 'h0'.
        Value can given as a single string or a sequence of
        strings (list, set, tuple).
        Values in a sequence are used as logical OR. For example,
            device_id = ['r0', 'h0'] will choose both routers and servers.
        When devices is not given, all devices are chosen.

        :param device_tags: Device tags.
        Optional.
        A device tag is configured on the config section in the
            BBE configuration file. E.g., 'dut', 'lns'.
        Value can given as a single string or a sequence of
            strings (list, set, tuple).
        Values in a sequence are used as logical AND. For example,
           device_tag = ['dut', 'lns'] will choose routers used as both
           DUT and LNS.
        Device_tag values are used for exact match, case insensitive.
        When device_tags is not given, all devices are chosen.

        :param interfaces: Interface IDs.
        Optional.
        Interface ids are like 'access0', 'uplink0', 'radius0'.
        Value can given as a single string or a sequence of
            strings (list, set, tuple).
        Values in a sequence are used as logical OR. For example,
            interface_id = ['uplink', 'rad'] will choose all devices
            with uplink interfaces and all with rad interfaces.
        Each value is a pattern used to filter device id, case insensitive.
            For example, interface_id = 'up' will choose devices with uplinks.
            The pattern matches the start of id only, e.g., link won't match
            uplink
        When interfaces is not given, all devices with any interface are chosen.

        :param id_only: Boolean.
        Optional.
        If provided and true, returns only device ids (r0, rt0, h0, etc.).
        Else returns BBEVarDevice instances.

        :return: A list (could be empty) BBEVarDevice objects satisfying the keyword arguments.

        """
        # Allow string value arguments
        if not devices:
            filter_dev_id = []
        elif isinstance(devices, str):
            filter_dev_id = [devices]
        else:
            filter_dev_id = devices

        if not device_tags:
            filter_dev_tag = []
        elif isinstance(device_tags, str):
            filter_dev_tag = [device_tags]
        else:
            filter_dev_tag = device_tags

        if not interfaces:
            filter_intf_id = []
        elif isinstance(interfaces, str):
            filter_intf_id = [interfaces]
        else:
            filter_intf_id = interfaces


        all_device_ids = self._devices.keys()

        # filter using device_id
        chosen_by_device_ids = set()
        if not filter_dev_id:
            chosen_by_device_ids.update(all_device_ids)
        else:
            for a_filter in filter_dev_id:
                myre = re.compile(r'^' + re.escape(a_filter), re.IGNORECASE)
                for a_dev in all_device_ids:
                    if myre.match(a_dev):
                        chosen_by_device_ids.update({a_dev})

        # filter using device_tag
        chosen_by_device_tags = set()
        if not filter_dev_tag:
            chosen_by_device_tags.update(all_device_ids)
        else:
            tags_set = {t.lower() for t in filter_dev_tag}  # turn tags argument into all lower case

            for dev_id in all_device_ids:
                dev_tags_set = {t.lower() for t in self._devices[dev_id].device_tags}

                if tags_set.issubset(dev_tags_set):
                    chosen_by_device_tags.add(dev_id)

        # filter by interface_id
        chosen_by_interface_ids = set()
        if not filter_intf_id:
            chosen_by_interface_ids.update(all_device_ids)
        else:
            for a_filter in filter_intf_id:
                myre = re.compile(r'^' + re.escape(a_filter), re.IGNORECASE)
                for a_dev in all_device_ids:
                    try:
                        for an_intf in self._devices[a_dev].device_interfaces:
                            if myre.match(an_intf):
                                chosen_by_interface_ids.update({a_dev})
                    except (KeyError, TypeError, AttributeError):
                        continue

        chosen_ids = chosen_by_device_ids.intersection(chosen_by_device_tags).intersection(chosen_by_interface_ids)

        if id_only:
            return list(chosen_ids)
        else:
            return [self._devices[devid] for devid in chosen_ids]

    def get_interfaces(self, device, interfaces=None, id_only=False):
        """Get interfaces filtered by device ids and interface ids.

        Device ids are defined in configuration file under resources, such as r0, h0, rt0.
        Interface ids are defined under a device, such as access0, transit0, uplink0, radius0.
        The interface type can be access, transit, custom, uplink, radius.

        If interface argument is omitted, all_types of interfaces are returned.

        Example usage:

        # Get interface ids of r1
        >>> bbe.get_interfaces('r0', id_only=True)
        ['access1', 'transit1', 'transit0', 'access0', 'radius0']

        # Get r1 uplink interface ids
        >>> bbe.get_interfaces('r1', interfaces='up', id_only=True)
        ['uplink1', 'uplink0']

        # Get r1 uplink0
        >>> r1_up0 = bbe.get_interfaces('r1', interfaces='uplink0')[0]
        >>> r1_up0
        <jnpr.toby.bbe.bbevar.interfaces.BBEVarInterface object at 0x7f42b8655588>
        >>> str(r1_up0)
        'Interface uplink0: ge-3/0/0.0 on r1: r47mx480wf'
        >>> r1_up0.interface_name
        'ge-3/0/0.0'
        >>> r1_up0.interface_config
        {'ip': '200.0.0.1/24', 'ipv6': '3000:db8:ffff:1::1/64'}
        >>> r1_up0.interface_type
        ['ge', 'ether']


        :param device: string device name, e.g., 'r0', 'r1', 'rt0', 'h0'.

        :param interfaces: interface id.
        Optional.
        Interface ids are like 'access-0', 'uplink-0', 'radius-0',
            partial id name can be used, e.g., 'acc', 'up'.
        Value can given as a single string or a sequence of
            strings (list, set, tuple).
        Values in a sequence are used as logical OR. For example,
            interface_id = ['uplink', 'rad'] will choose all interfaces
            with uplink interfaces and all with rad interfaces.
        When interfaces is not given, all interfaces are chosen.

        :param id_only: If provided and True, returns interface ids (access-0, etc,)

        :return: list of BBEVarInterface or interface id if id_only is True.
        Return list can be empty if the specified device and interface does not exist.

        Could raise BBEVarError.
        """
        try:
            assert isinstance(self._interfaces[device], dict)
        except (KeyError, TypeError, AssertionError):
            return list()

        if not interfaces:
            interfaces = []
        elif isinstance(interfaces, str):
            interfaces = [interfaces]

        # Find interfaces
        chosen_interfaces = []

        if not interfaces:
            chosen_interfaces = [self._interfaces[device][intf] for intf in
                                 self._interfaces[device].keys()]
        else:
            for a_filter in interfaces:
                myre = re.compile(r'^' + re.escape(a_filter), re.IGNORECASE)
                for an_intf in self._interfaces[device].keys():
                    if myre.match(an_intf):
                        chosen_interfaces.append(self._interfaces[device][an_intf])

        if id_only:
            return [intf_obj.interface_id for intf_obj in chosen_interfaces]
        else:
            return chosen_interfaces

    def get_vrfs(self, device=None):
        """Get vrf iterator object for the device.

        When PE devices have vrf defined, bbevar stores the iterator object
        of vrf names at [bbevar][resources][device][config][vrf][names].

        Example usage:
            >>> vrf_iter0 = bbe.get_vrfs('r0')
            >>> list(vrf_iter0)
            ['RETAILER1', 'RETAILER2', 'RETAILER3', 'RETAILER4', 'RETAILER5']
            >>> for v0 in vrf_iter0:
            ...   print(v0)
            ...
            RETAILER1
            RETAILER2
            RETAILER3
            RETAILER4
            RETAILER5
            >>> list(bbe.get_vrfs('r1'))
            ['RETAILER1', 'RETAILER2', 'RETAILER3', 'RETAILER4', 'RETAILER5']
            >>> none_vrf_iter = bbe.get_vrfs('h0')
            >>> type(none_vrf_iter)
            <class 'NoneType'>

        Alternatively, the object can alos be obtained from bbevar:
            ###### use bbevar directly
            >>> vrf_iter = bbe.bbevar['resources']['r0']['config']['vrf']['names']
            >>> list(vrf_iter)
            ['RETAILER1', 'RETAILER2', 'RETAILER3', 'RETAILER4', 'RETAILER5']
            >>> for n in bbe.bbevar['resources']['r0']['config']['vrf']['names']:
            ...   print(n)
            ...
            RETAILER1
            [skip...]
            RETAILER5

        Can also use BBEVarDevice obj:
            >>> dut = bbe.get_devices(device_tags='dut')[0]
            >>> str(dut)
            'Device r0: r46mx480wf'
            >>> dut.has_vrf
            True
            >>> dut.vrf
            Vrf(base=RETAILER, start=1, step=1, count=10)
            >>> for v in dut.vrf:
            ...   print(v)
            ...
            RETAILER1
            [skip...]
            RETAILER10

        :param device: string device name, e.g., 'r0', 'r1'.
        :return: vrf iterator if exist or None otherwise

        Could raise BBEVarError.
        """
        try:
            assert isinstance(self.bbevar['resources'][device]['config']['vrf']['names'], Vrf)
        except (KeyError, TypeError, AssertionError):
            #  log the err message when log is available
            return None

        return self.bbevar['resources'][device]['config']['vrf']['names']

    # def get_rt_handle(self, device='rt0'):
    #     """Get router tester handle from bbevar.
    #
    #     Obselete -- Handle is going to be created by Tody init
    #
    #     When a router tester is instantiated, its handle (object) is stored in bbevar
    #     at, e.g., bbevar['resources']['rt0']['system']['primary']['dh'].
    #
    #     Example usage:
    #         >>> h = bbe.get_rt_handle()
    #         >>> type(h)
    #         <class 'jnpr.toby.bbe.hldcl.ixiatester.IxiaTester'>
    #
    #     :param device: string tester device name, e.g., 'rt0', 'r1'.
    #     :param node: node name such as 'primary'
    #     :return: rt handle
    #
    #     Could raise BBEVarError.
    #     """
    #
    #     return t.get_handle(resource=device)

    def get_subscriber_handles(self, interface=None, protocol=None, tag=None, ri=None, family=None):
        """Get subscriber handles (DHCPSubscribers and PPPoESubscribers instance objects).

        Usage examples:

            >>> all_hands = bbe.get_subscriber_handles()
            >>> for h in all_hands:
            ...   print(h)
            ...
            PPPoESubscribers with tag pppoescaling3 on access1 of r0
            PPPoESubscribers with tag pppoescaling4 on access1 of r0
            DHCPSubscribers with tag dhcpscaling2 on access1 of r0
            PPPoESubscribers with tag pppoescaling1 on access0 of r0
            PPPoESubscribers with tag pppoescaling2 on access0 of r0
            DHCPSubscribers with tag dhcpscaling1 on access0 of r0
            DHCPSubscribers with tag dhcpfunctional1 on access0 of r0

            >>> [ah.tag for ah in all_hands]
            ['dhcpscaling2', 'pppoescaling3', 'pppoescaling4', 'dhcpscaling1', 'dhcpfunctional1',
            'pppoescaling1', 'pppoescaling2']

            >>> h = bbe.get_subscriber_handles(interface='access0', protocol='dhcp')
            >>> h
            [<jnpr.toby.bbe.subscribers.DHCPSubscribers object at 0x7fdd942d1588>,
            <jnpr.toby.bbe.subscribers.DHCPSubscribers object at 0x7fdd942d1470>]

            >>> h[0].vlan_range
            VlanRange(start=1, step=1, repeat=1)

            >>> h[1].svlan_range
            VlanRange(start=1, step=1, repeat=1)

            >>> h[0].rt_port
            '9/7'
            >>> h[1].router_port
            'ge-1/0/0'
            >>> h = h[0]
            >>> h.protocol
            'dhcp'
            >>> h.option82_ari
            DHCPOption(id='agent1-ari', start=100, step=1, repeat=1)
            >>> h.option82_aci
            DHCPOption(id='agent1-aci', start=100, step=1, repeat=1)
            >>> h.option82_aci.id
            'agent1-aci'
            >>> h.option37
            DHCPOption(id='agentv6-ari', start=100, step=1, repeat=1)
            >>> h.on_ae
            True
            >>> h.is_ae_active
            True
            >>> h.ae_bundle
            'ae0'
            >>> h.clr
            50
            >>> h.count
            16000
            >>> h.has_option18
            True
            >>> h.has_option37
            True
            >>> h.has_option82
            True

            To use tag as pattern --

            >>> scale_subs = bbe.get_subscriber_handles(tag='scal')
            >>> for h in scale_subs:
            ...     print(h.tag)
            ...
            pppoescaling3
            pppoescaling4
            dhcpscaling2
            pppoescaling1
            pppoescaling2
            dhcpscaling1

            >>> func_subs = bbe.get_subscriber_handles(tag='fun')
            >>> for h in func_subs:
            ...     print(h.tag)
            ...
            dhcpfunctional1
            >>>


        :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
        :param protocol: optional, string, subscriber protocol, e.g., 'dhcp, 'pppoe'
        :param tag: optional, string, subscriber group tag. Tag could be partial match of the real tag name.
        for example, tag='scale' could match both pppoescale1 and dhcpscale2 tag values.
        :param ri: optional, string, routing instance name
        :param family: optional, string. Supported values -- 'ipv4', 'ipv6', 'dual'
        :return: A list of subscriber handles
        """
        handles = self._subscribers.copy()  # copy so my internal subscribers list won't be changed

        if interface:
            handles = [h for h in handles if h.interface_id == interface]

        if protocol:
            handles = [h for h in handles if h.protocol == protocol]

        if tag:
            tagre = re.compile(r'.*' + re.escape(tag), re.IGNORECASE)
            handles = [h for h in handles if tagre.match(h.tag)]

        if ri:
            handles = [h for h in handles if h.ri == ri]

        if family:
            handles = [h for h in handles if h.family == family or h.family == 'dual']

        return handles

    def get_configured_subscribers_count(self, interface=None, protocol=None, tag=None, ri=None, family=None):
        """Get subscribers count configured by BBE configuration

        Example usage:

            >>> total = bbe.get_configured_subscribers_count()
            >>> total
            56010
            >>> dhcptotal = bbe.get_configured_subscribers_count(protocol='dhcp')
            >>> dhcptotal
            24010
            >>> access0pppoe = bbe.get_configured_subscribers_count(interface='access0', protocol='pppoe')
            >>> access0pppoe
            16000
            >>> group_total = bbe.get_configured_subscribers_count(tag='dhcpscaling1')
            >>> group_total
            16000

            Use tag to get subscribers count:

            >>> bbe.get_configured_subscribers_count(tag='scal')
            56000
            >>> bbe.get_configured_subscribers_count(tag='func')
            10
            >>>

        :param interface: optional, string, router interface id where subscriber is defined, e.g., 'access0'
        :param protocol: optional, string, subscriber protocol, e.g., 'dhcp, 'pppoe'
        :param tag: optional, string, subscriber group tag.
        :param ri: optional, string, routing instance name
        :param family: optional, string, Supported values -- 'ipv4', 'ipv6', 'dual'
        :return: integer count
        """
        total = 0

        handles = self.get_subscriber_handles(interface=interface, protocol=protocol, tag=tag, ri=ri, family=family)

        for handle in handles:
            total += handle.count

        return total

    def get_subscribers_call_rate(self, protocol='dhcp', family='ipv4'):
        """Get subscribers csr and clr

        IXIA HLA requires a whole list of all csr and clr rates even if to set only
        one emulation handle. Rate should be set separately for dhcpv4, dhcpv6, and pppoe.

        Usage example:
            >>>> bbe.get_subscribers_call_rate()
            {'login_rate': [50, 10, 50], 'logout_rate': [50, 10, 50]}
            >>> bbe.get_subscribers_call_rate('dhcp', 'ipv6')
            {'login_rate': [50, 10, 100, 100], 'logout_rate': [50, 10, 100, 100]}
            >>> pppoe_rate = bbe.get_subscribers_call_rate('pppoe')
            >>> pppoe_rate
            {'login_rate': [100, 50, 100, 50], 'logout_rate': [100, 50, 100, 50]}

        :param protocol: 'dhcp' or 'pppoe'
        :param family: 'ipv4' or 'ipv6'. pppoe subscirbers type does not need family.
        :param rate_type: 'csr' or 'clr'
        :return: dict with two keys: login_rate and logout_rate. Values are list
        of csr values and clr values.
        """
        rates = dict()
        csr = []
        clr = []
        outstanding = []

        all_handles = self.get_subscriber_handles()

        # if dhcpv4, return dhcpv4 and dhcp dual stack
        if protocol == 'dhcp' and family == 'ipv4':
            for handle in all_handles:
                if handle.protocol == 'dhcp' and (handle.family == 'ipv4' or handle.family == 'dual'):
                    csr.append(handle.csr)
                    clr.append(handle.clr)
                    if handle.outstanding:
                        outstanding.append(handle.outstanding)
        # if dhcpv6, return dhcpv6, dhcp dual stack, pppoev6, and pppoe dual stack
        elif protocol == 'dhcp' and family == 'ipv6':
            for handle in all_handles:
                if handle.family == 'ipv6' or handle.family == 'dual':
                    if handle.rt_dhcpv6_handle:
                        csr.append(handle.csr)
                        clr.append(handle.clr)
                        if handle.outstanding:
                            outstanding.append(handle.outstanding)
        # if pppoe, return all pppoe
        elif protocol == 'pppoe':
            for handle in all_handles:
                if handle.protocol == 'pppoe' or handle.protocol == 'l2tp':
                    csr.append(handle.csr)
                    clr.append(handle.clr)
                    if handle.outstanding:
                        outstanding.append(handle.outstanding)

        rates['login_rate'] = csr
        if outstanding:
            rates['outstanding'] = outstanding
        rates['logout_rate'] = clr
        return rates

    def get_rt_dhcp_server(self, family='ipv4'):
        """Get RT DHCP server instance

        Usage:
            >>> v4server = bbe.get_rt_dhcp_server()
            >>> v4server
            <jnpr.toby.bbe.bbevar.rtdhcpserver.RTDHCPv4Server object at 0x7f7c4afe6898>
            >>> v4server.created
            False
            >>> v4server.pool_size
            32000
            >>> v6server = bbe.get_rt_dhcp_server('ipv6')
            >>> v6server.lease_time
            99999
            >>> v6server.pool_ia_type
            'iana_iapd'
            >>> v6server.pool_prefix_start
            '1000:0:1::0'

        :param family: 'ipv4' or 'ipv6'.
        :return: instance of either RT
        """
        return self._rt_dhcps_ervers[family]

    def _dict_merge(self, source, destination):
        """Copy the source to the destination
        """
        for key, value in source.items():
            if isinstance(value, dict):
                # get node or create one
                node = destination.setdefault(key, {})
                self._dict_merge(value, node)
            else:
                destination[key] = value

        return destination

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return 'BBEVars()'


class Vrf:
    """Iterator class for VRF names in bbevar.

    The iterator will be instantiated by BBEVars initialize based on the presence
    of vrf in configuration file, for example:

    bbevar:
        resources:
            r0:
                config:
                    vrf:
                        base: RETAILER
                        start: 1
                        step: 1
                        count: 100

    """

    def __init__(self, **kwargs):
        self.base = kwargs.get('base', 'RETAILER')
        self.start = kwargs.get('start', 1)
        self.step = kwargs.get('step', 1)
        self.count = kwargs.get('count', 0)
        self.max = self.start + self.step * self.count - 1
        self.cur = 0

    def __iter__(self):
        self.cur = self.start
        return self

    def __next__(self):
        if self.cur > self.max:
            raise StopIteration
        else:
            vrf_name = self.base + str(self.cur)
            self.cur += self.step
            return vrf_name

    def __repr__(self):
        """Displays nicely when bbevar is dumped

        :return: String
        """
        return 'Vrf(base={}, start={}, step={}, count={})'.format(
            self.base, self.start, self.step, self.count)
