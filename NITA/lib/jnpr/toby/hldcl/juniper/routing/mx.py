"""
Class for Mx and MXVC Devices
"""
import re
from copy import copy

from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hldcl.juniper.routing import Router
from lxml import etree
from jnpr.toby.exception.toby_exception import TobyException


class Mx(Router):
    """
    Mx Class
    """
    def __init__(self, *args, **kwargs):
        super(Mx, self).__init__(**kwargs)
        self.reboot_timeout = 900
        self.upgrade_timeout = 1500
        self.issu_timeout  = 2400


'''
class MxVc(Mx):
    """
    MxVC Class
    """
    def __init__(self, *args, **kwargs):
        """

        Base class for JunOS devices

        :param host:
            **REQUIRED** host-name or IP address of target device
        :param os:
            *OPTIONAL* Operating System of device. Default is JUNOS
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param password:
            *OPTIONAL* Login Password. If not provided will be derived from
            Toby framework defaults.
        :param model:
             *OPTIONAL* Model of device. Default is None.
        :param dual_re:
            *OPTIONAL* Connect to both the RE's. Default is False. Will return
            object which is connected to master RE.
        :param routing_engine:
            *OPTIONAL*  Connect to routing engine specified.
            Supported values are master/backup.
            Cannot be used with dual_re.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            values are telnet/ssh/netconf/console
        :param console:
            *OPTIONAL* Flag to identify console login. Default is False.
        :param mode:
            *OPTIONAL* Port on device to which connection needs to made.
        : param tag:
            *OPTIONAL* Tag to uniquely idetify the device object
        :return: Device object based on os and model
        """

        # Check if host is provided
        if 'host' not in kwargs:
            raise TobyException("'host' is mandatory")

        # 'dual_re' and 'routing_engine' options cannot be used together
        if kwargs.get('dual_re') and kwargs.get('routing_engine'):
            raise TobyException("'dual_re' and 'routing_engine' cannot be used together")

        self._kwargs = kwargs
        self.connected = False
        self.shell_connection = None
        self._vc_info = kwargs.get('vc_info')
        self._connected_to_masters = False
        self._members_info = None
        self.configObject = None

        class local_rpc(object):
            call = None

            def __getattribute__(rself, item, *iargs, **ikwargs):
                self.log(
                    'Sending RPC : {0} with arguments {1} and keyword '
                    'arguments {2}'.format(item, iargs, ikwargs))
                fcall = getattr(self.handle.rpc, '__getattr__')
                local_rpc.call = fcall(item)
                return local_rpc.rpc_call

            @staticmethod
            def rpc_call(*iargs, **ikwargs):
                response = local_rpc.call(*iargs, **ikwargs)
                self.log('RPC Response: {0}'.format(etree.tostring(response)))
                return response

        self.rpc = local_rpc()

        # call Device class init for common operations
        super(Juniper, self).__init__(*args, **kwargs)

        # Open connections
        self.open()

    def open(self):
        # Connect to given hostname/IP
        self._connect()

        # Check if VC info can be derived
        # This cannot be derived if connected RE is backup
        if not self._can_get_vc_info() \
                and self._kwargs.get('strict') is None:
            # get master RE of memeber 0
            master_re = self._get_master_re(member='member0')
            self._members_info = self._get_members_info()
            self._connect_all_member_re_of_role(members_info=self._members_info, role='master')
            mhandle = getattr(self, master_re.replace('-', '_').upper())
            self._vc_info = mhandle._get_virual_chassis_info()
            self._connected_to_masters = True

        # Create a shell connection
        self.shell_connection = self._get_shell_connection()

        # Populate common properties
        if self._vc_info is None:
            self._vc_info = self._get_virual_chassis_info()
        # is_master_member = self._is_master_member(vc_info=vc_info)
        # conn_member_info = self._get_connected_member_info(vc_info=vc_info)
        self.re = self._get_re_slot_name(vc_info=self._vc_info)
        self.DUAL_RE = self._kwargs.get('dual_re')

        # If strict is None, check for connecting other members and RE's
        if self._kwargs.get('strict') is None:
            # Get all memebers and RE information

            if self._members_info is None:
                self._members_info = self._get_members_info()

            # Connect to all masters
            if self._kwargs.get('dual_re') or not self._kwargs.get('routing_engine', '').lower() == 'backup':
                if not self._connected_to_masters:
                    self._connect_all_member_re_of_role(members_info=self._members_info, role='master')

            if self._kwargs.get('dual_re') or self._kwargs.get('routing_engine', '').lower() == 'backup':
                self._connect_all_member_re_of_role(members_info=self._members_info, role='backup', vc_info=self._vc_info)

            # Point the object to the master member master/backup RE
            master_member_info = self._get_master_member_info(vc_info=self._vc_info)
            master_member_re = 'MEMBER' + master_member_info['id'] + '_RE' \
                               + self._members_info['member' + master_member_info['id']][self._kwargs.get('routing_engine', 'master')]
            self._replace_object(getattr(self, master_member_re))
            return True

    def re_slot_name(self):
        """
        Retrieves connected RE slot name

        :return: RE slot name
        """
        return self.re.upper()

    def _get_re_slot_name(self, vc_info=None):
        """

        Retrieves connected RE slot name

        :param vc_info:
        :return: RE slot name
        """

        # Get virtual chassis information
        if vc_info is None:
            vc_info = self.handle.rpc.get_virtual_chassis_information()
        members = vc_info.findall('member-list/member')

        # Derive the member-id from virtual chassis information
        member_info = self._get_connected_member_info(vc_info=vc_info)

        # Get Other RE detail
        other_re_list = self._get_other_re_list()

        # When other RE operational
        for element in other_re_list:
            mat = re.search('member{0}-(\S+)'.format(member_info['id']),
                            element, re.I)
            if mat:
                if mat.group(1).lower() == 're0':
                    return 'member' + member_info['id'] + '-re1'
                if mat.group(1).lower() == 're1':
                    return 'member' + member_info['id'] + '-re0'
                else:
                    raise TobyException('Could not determine RE name', host_obj=self)

        # When other RE is not operational
        main_re_list = self._get_re_list()
        for element in main_re_list:
            if re.search('member{0}-'.format(member_info['id']), element, re.I):
                return element

        # Else raise exception
        raise TobyException('Could not determine member RE name', host_obj=self)

    def _get_members_info(self):
        members_info = {}
        routing_engines = self.handle.rpc.get_route_engine_information()
        res = routing_engines.findall('multi-routing-engine-item')
        for element in res:
            member_id = element.find('re-name').text
            members_info[member_id] = {}
            routing_engine = element.findall('route-engine-information/route-engine')
            for re_element in routing_engine:
                members_info[member_id][re_element.find('mastership-state').text] = re_element.find('slot').text
        return members_info

    def _connect_all_member_re_of_role(self, role, members_info=None,
                                       vc_info=None):
        try:
            if members_info is None:
                members_info = self._get_members_info()

            for member in members_info.keys():
                re_name = member + '-re' + members_info[member][role.lower()]
                if getattr(self, 're', None) == re_name:
                    setattr(self, self.re.upper().replace('-', '_'), copy(self))
                else:
                    other_master_re_kwargs = self._create_other_re_kwargs(self._kwargs, re_name)
                    if vc_info is not None:
                        other_master_re_kwargs['vc_info'] = vc_info
                    setattr(self, re_name.upper().replace('-', '_'), MxVc(**other_master_re_kwargs))
                    getattr(self, re_name.upper().replace('-', '_')).re = re_name
        except Exception as exp:
            self.log(level='ERROR', message="Connection to {0} rolse's failed".format(role))
            return False
        return True

    def _create_other_re_kwargs(self, kwargs, other_re_name):
        other_re_host = self._get_connection_element(other_re_name)
        other_re_kwargs = copy(kwargs)
        other_re_kwargs['dual_re'] = None
        other_re_kwargs['host'] = other_re_host
        other_re_kwargs['strict'] = True
        if other_re_kwargs.get('handle') is not None:
            del other_re_kwargs['handle']
        return other_re_kwargs

    def _get_connection_element(self, re_name):
        """
        Retrieves name/IP of other RE.

        If rtr.host is host-name of the routing then this function retrieves
        hostname of other RE.
        If rtr.host is IP address of the routing, them this function retrieves
        IP of other RE.

        :param self: Junos routing object
        :param re_name: RE name
        :return: host name or management IP of RE
        """
        import socket
        is_ip = False
        try:
            socket.inet_aton(self.host)
            is_ip = True
        except socket.error:
            pass

        # If self.host is not IPv4 address then get host-name of other RE
        if not is_ip:
            host_name = self._get_host_name(re_name)
            # Check if the host-name's are unique
            if not self.host == host_name:
                # If host name's are uniques and since host-name was used to
                # connect to device, then assumption is that second RE name is
                # also registered in DNS and reachable
                return host_name
            # If the host-names are not unique then get IP address
            else:
                return self._get_host_ip(re_name)
        # When self.host is an IPv4 address then get management IP address
        else:
            return self._get_host_ip(re_name)

    def _get_virual_chassis_info(self):
        try:
            res = self.handle.rpc.get_virtual_chassis_information()
            return res
        except:
            return None

    def _get_master_member_info(self, vc_info=None):
        """
        Retrieves master chassis member id

        :param vc_info:
            Virtual Chassis information in xml
        :return:
            master chassis member id
        """

        # Get virtual chassis information
        if vc_info is None:
            vc_info = self.handle.rpc.get_virtual_chassis_information()

        members = vc_info.findall('member-list/member')
        member_info = {}

        for element in members:
            member_role = element.find('member-role').text.lower()
            mat = re.search('(master)', member_role, re.I)
            if mat:
                member_info['role'] = mat.group(1)
                member_info['id'] = element.find('member-id').text
                break
        if not member_info.get('id'):
            self.log(level='ERROR', message='Could not determined role and id. Seems like the MX-VC is not formed yet')
        return member_info

    def _get_connected_member_info(self, vc_info=None):
        """
        Retrieve connected member info

        :param vc_info:
            Virtual Chassis information in xml
        :return:
            Dictionary with connected member's id and role
        """
        # Get virtual chassis information
        if vc_info is None:
            vc_info = self.handle.rpc.get_virtual_chassis_information()

        members = vc_info.findall('member-list/member')
        member_info = {}

        for element in members:
            member_role = element.find('member-role').text.lower()
            mat = re.search('(\S+)\*', member_role, re.I)
            if mat:
                member_info['role'] = mat.group(1)
                member_info['id'] = element.find('member-id').text
                break
        if not member_info.get('id'):
            raise TobyException('Could not determine role and id. Perhaps MX-VC is not formed yet.', host_obj=self)
        return member_info

    def _get_other_re_list(self):
        response = self.cli(command='show version invoke-on other-routing-engine', format='xml').response()
        other_re = response.findall('multi-routing-engine-item/re-name')
        re_list = [element.text.upper() for element in other_re]
        return re_list

    def _get_re_list(self):
        response = self.cli(
            command='show version', format='xml').response()
        main_re = response.findall('multi-routing-engine-item/re-name')

        re_list = [element.text.upper() for element in main_re]
        return re_list

    def _can_get_vc_info(self):
        try:
            self.handle.rpc.get_virtual_chassis_information()
            return True
        except:
            return False

    def _get_master_re(self, member):
        response = self.handle.rpc.get_route_engine_information()
        member0 = response.find(
            'multi-routing-engine-item[re-name="{0}"]/route-engine-information'
            '/route-engine[mastership-state="master"]'.format(member)
        )
        master_re = member + '-re' + member0.find('slot').text
        return master_re
'''
