"""Module contains the RUtils class for rutils methods"""
# pylint: disable=undefined-variable
__author__ = ['Sumanth Inabathini']
__contact__ = 'isumanth@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import os
import inspect

from collections import defaultdict

from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.services import utils

class MyException(RuntimeError):
    """Class for raising custom exception that also add error message to TOBY logs"""
    def __init__(self, err_msg):
        """Constructor method to add raise exception"""
        utils.log('ERROR', err_msg)
        super().__init__(err_msg)

class MissingMandatoryArgument(ValueError):
    """Class for raising custom exception for missing mandatory argument"""
    def __init__(self, err_msg):
        """Constructor method to add message to missing mandatory argument"""
        utils.log('ERROR', "Missing mandatory argument, {}".format(err_msg))
        super().__init__("Missing mandatory argument, {}".format(err_msg))

class rutils(object):
    """Class for Router utilities"""

    MissingMandatoryArgument = MissingMandatoryArgument

    def __init__(self, **kwargs):
        """Constructor method to update the instance of RUtils class."""
        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.dd = lambda: defaultdict(self.dd)
        # self.tg = None
        self.dh = None
        self.xml = xml_tool()
        self.topo = self.dd()
        self.cmd = ''
        self.tg_port_pairs = []
        self.resource = None
        self.cmd_list = []
        self.ptr = {}
        self.log = utils.log
        self._chk_in_msg = {}
        self._cmd_name_tag = None
        self._cmd_mapping = None

    def get_intf_list_in_path(self, intf=None):
        """Return the list of interfaces in the given interface path

        :param string intf:
            **REQUIRED** Interface in the path of the required interfaces. Default is None

        :return: List of Interfaces in the path of the given interface

        :rtype: list

        Example::

          Python:
            get_intf_list_in_path(intf='r0:r0_h0_1_if')

          Robot:

            Get Intf List In Path  intf=r0:r0_h0_1_if
        """

        self.log('INFO', 'Retrieving interfaces list in the path')

        if intf is None:
            raise MissingMandatoryArgument('intf')

        path = self.topo['intf'][intf]['path']

        self.log('INFO', 'Returning interfaces list in the path')

        return self.topo['path'][path]

    def parse_topo(self, pkt_path=None):
        """Parse the topology from the packet path

        :param list pkt_path:
            **REQUIRED** The packet path containing the devices. Default is None

        :return: True if successful.In all other cases False.

        :rtype: bool

        Example::

          Python:
            parse_topo(['h0', 'r0', 'h1'])

          Robot:
            @{topo}=  h0 r0 h1
            Parse Topo  @{topo}
        """
        self.log('INFO', 'Parsing the Topology')

        if pkt_path is None:
            raise MissingMandatoryArgument('pkt_path')

        self.topo['rt_list'] = [pkt_path[0], pkt_path[-1]]
        for res in pkt_path:
            self.topo['path_res'][res] = {}
            for intf in t.get_interface_list(resource=res):
                intf_data = t.get_interface(resource=res, intf=intf)
                path = intf_data['link'].split('_')[0]
                if not path.lower().startswith('path'):
                    continue
                if path not in self.topo['path']:
                    self.topo['path'][path] = []
                intf_tag = '{}:{}'.format(res, intf)
                self.topo['intf'][intf_tag]['name'] = intf_data['pic']
                self.topo['intf'][intf_tag]['link'] = intf_data['link']
                self.topo['intf'][intf_tag]['path'] = path
                self.topo['intf'][intf_tag]['res'] = res
                self.topo['path'][path].append(intf_tag)
                link = self.topo['intf'][intf_tag]['link']
                if link not in self.topo['link']:
                    self.topo['link'][link] = intf_tag
                else:
                    self.topo['intf'][intf_tag][
                        'gw_if'] = self.topo['link'][link]
                    gw_res, gw_if = self.topo['link'][link].split(':')
                    gw_data = t.get_interface(resource=gw_res, intf=gw_if)
                    if 'uv-ip' in gw_data:
                        self.topo['intf'][intf_tag]['gw_ip'] = gw_data['uv-ip']
                    self.topo['intf'][self.topo['link'][link]][
                        'gw_if'] = intf_tag
                    if 'uv-ip' in intf_data:
                        self.topo['intf'][self.topo['link'][link]][
                            'gw_ip'] = intf_data['uv-ip']

                if path not in self.topo['path_res'][res]:
                    self.topo['path_res'][res][path] = []
                self.topo['path_res'][res][path].append(intf)

        self.log('INFO', 'Parsed the Topology')

        return True

    def get_tg_port_pairs(self):
        """Return the port pairs to be used by traffic generator based on the path

        :return: True if successful.In all other cases False.

        :rtype: bool

        Example::

          Python:
            get_tg_port_pairs()

          Robot:
            Get Tg Port Pairs
        """

        self.log('INFO', 'Retrieving port pairs')
        self.tg_port_pairs = []
        for path in self.topo['path']:
            self.tg_port_pairs.append(
                [self.topo['path'][path][0], self.topo['path'][path][-1]])

        self.log('INFO', 'Returning port pairs')

        return self.tg_port_pairs

    def set_resource(self, resource=None):
        """Update the resource and device handle information

        :param string resource:
            **REQUIRED** Resource for which the device handle need to be updated. Default is None

        :return: True if successful.In all other cases raised exception.

        :rtype: bool

        Example::

          Python:
            set_resource('R0')

          Robot:
            Set Resource   R0
        """

        self.log('INFO', 'Updating  resource info')

        if resource is None:
            raise MissingMandatoryArgument('resource')

        self.resource = resource
        self.dh = t.get_handle(resource=resource)

        self.log('INFO', 'Updated  resource info')
        return True

    def init(self, resource=None, pkt_path=None):
        """Initialise the class parameters

        :param string resource:
            **REQUIRED** Resource for which the device handle need to be updated. Default is None

        :param list pkt_path:
            **REQUIRED** The packet path containing the devices. Default is None

        :return: True if successful else False

        :rtype: bool

        Example::

          Python:
            init(self, resource='h0', pkt_path=['h0', 'r0', 'h1'])

          Robot:

            @{resource}=  h0 r0 h1
            init  h0  @{resource}
        """
        self.log('INFO', 'Initializing the class ')

        if not self.set_resource(resource):
            return False

        if not self.parse_topo(pkt_path):
            return False

        self.log('INFO', 'Initialized the class ')

        return True

    def get_cli_output(self, cmd=None, frmt='text'):
        """Return the response of the command executed

        :param string cmd:
            **REQUIRED** The command string that need to be executed on the string. Default is None

        :param list pkt_path:
            **OPTIONAL** Format in which the command need to be executed. Default is 'text'

        :return: True if successful.In all other cases False.

        :rtype: bool

        Example::

          Python:
            get_cli_output(cmd='show versions', format='text')

          Robot:

            Get Cli Output  cmd=show versions  format=text
        """

        self.log('INFO', 'Retrieving  cli for command:{}'.format(cmd))

        if cmd is None:
            raise MissingMandatoryArgument('cmd_list')

        self.log('INFO', 'Returning  cli for command:{}'.format(cmd))

        return self.dh.cli(command=cmd, format=frmt).response()

    def get_xml_output(self, cmd=None, xpath=None, timeout=60, want_list=False):
        """Get the xml output

        :param string cmd:
            **REQUIRED** The command string that need to be executed on the string. Default is None

        :param string xpath:
            **OPTIONAL** The path till which the output need to be parsed. Default is None

        :param int timeout:
            **OPTIONAL** Max time to wait for the command output . Default is 60

        :param bool want_list:
            **OPTIONAL** The out need to be sent as list is decided based on this flag.
                Default is False

        :return: dictionary containing the xml output of the given command

        :rtype: dict

        Example::

          Python:
            get_xml_output('show services sessions count',
                      xpath='service-msp-sess-count-information/service-msp-sess-count',
                      want_list=True)
          Robot:

            Get Xml Output  show services sessions count
                            xpath=service-msp-sess-count-information/service-msp-sess-count
                            want_list=True
        """

        self.log('INFO', 'Retrieving  xml output for command:{}'.format(cmd))

        output = self.dh.cli(command=cmd, timeout=timeout,
                             format='xml').response()

        xml_tree = self.xml.xml_string_to_dict(xml_str=output)
        xml_tree = xml_tree['rpc-reply']

        if xpath:
            for path in xpath.split('/'):
                xml_tree = xml_tree[path]

        self.log('INFO', 'Returning  xml output for command:{}'.format(cmd))

        if want_list:
            return xml_tree if isinstance(xml_tree, list) else [xml_tree]

        return xml_tree

    def get_fpc_pic_port_from_ifname(self, intf):
        """Return FPC PIC and Port of a interface is given

        :param string intf:
            **REQUIRED** The interface for which the fpc and pic need to be returned.

        :return: fpc, pic and port of the given interface

        :rtype: tuple

        Example::

          Python:
            get_fpc_pic_port_from_ifname('ge-2/1/0')

          Robot:
            Get Fpc Pic Port From Ifname  ge-2/1/0
        """

        fpc_slot, pic_slot, port = None, None, None

        match = re.search(r'[a-z1-9]+\-([0-9]+)\/([0-9]+)\/([0-9]+)', intf)
        if match:
            fpc_slot, pic_slot, port = match.group(1), match.group(2), match.group(3)

        return fpc_slot, pic_slot, port

    def get_fpc_pic_from_ifname(self, intf):
        """Return FPC PIC and Port of a interface is given

        :param string intf:
            **REQUIRED** The interface for which the fpc and pic need to be returned.

        :return: fpc, pic of the given interface

        :rtype: tuple

        Example::

          Python:
            get_fpc_pic_from_ifname('ge-2/1/0')

          Robot:
            Get Fpc Pic From Ifname  ge-2/1/0
        """

        fpc_slot, pic_slot = None, None

        match = re.search(r'[a-z1-9]+\-([0-9]+)\/([0-9]+)\/([0-9]+)', intf)
        if match:
            fpc_slot, pic_slot = match.group(1), match.group(2)

        return fpc_slot, pic_slot

    def load_set_cfg(self, file='scaling_temp.txt', **kwargs):
        """Load config onto the device from filename given

        :param string file:
            **REQUIRED** The file from which the config need to be laoded. Default is \
                        'scaling_temp.txt'

        :return: True if successful.In all other cases False.

        :rtype: bool

        Example::

          Python:
            load_set_cfg(file='scaling_temp.txt')

          Robot:
            Load Set Cfg  file=scaling_temp.txt
        """

        self.log('INFO', 'Loading set config')

        # write the command list to the file
        file_handle = open(file, 'a')
        file_handle.writelines(self.cmd_list)
        file_handle.close()

        self.log('INFO', 'Loaded set config')

        return self.dh.load_config(local_file=file, option='set', **kwargs)

    def cmd_add(self, cmd, arg=None, opt=None, **kwargs):
        """add the given command to the commad list

        :param string cmd:
            **REQUIRED** The command string that need to be added to the command list

        :param string arg:
            **OPTIONAL** Key to be checked in the self.ptr

        :param bool opt:
            **OPTIONAL** When set to 'flag', command will be added only if arg is in self.ptr\
                and if its value is set to True. Default is None

        :param string tag:
            **OPTIONAL** Tag to be added at the end of the command. Default is None

        :param bool update:
            **OPTIONAL** Update object with the new data or not. Default is True

        :param bool mapping:
            **OPTIONAL** Update mapping with the name tag set earlier. Default is False

        :return: None

        :rtype: None

        Example::

          Python:
            cmd_add("nat-rules", arg='nat_rules', tag='1', update=False)

          Robot:
            Cmd Add  nat-rules  arg=nat_rules tag=1 update=False
        """

        update = kwargs.get('update', True)
        mapping = kwargs.get('mapping', False)
        tag = kwargs.get('tag', None)

        cmd = "{} {}".format(self.cmd, cmd)

        if arg is not None:
            if arg in self.ptr and self.ptr[arg] is not None:
                #self.log('INFO', 'Adding command:{} to command list'.format(cmd))
                if arg.endswith('_list'):
                    for key in self.ptr[arg]:
                        self.cmd_list.append("{} {}".format(cmd, key))
                else:
                    if opt is not None and opt == 'flag':
                        if self.ptr[arg]:
                            self.cmd_list.append(cmd)
                    else:
                        cmd += " " + str(self.ptr[arg])
                        if tag is not None:
                            cmd += str(tag)
                            value_tag = self.ptr[arg] + str(tag)
                            if mapping and self._cmd_name_tag is not None and \
                               self._cmd_mapping is not None:
                                if arg not in self._cmd_mapping:
                                    self._cmd_mapping[arg] = {}
                                self._cmd_mapping[arg][value_tag] = self._cmd_name_tag
                            # Update this info back in to the object
                            if update:
                                self.ptr[arg] = value_tag

                        self.cmd_list.append(cmd)
                self.log('INFO', 'Added command:{} to command list'.format(cmd))
        else:
            #self.log('INFO', 'Adding command:{} to command list'.format(cmd))
            self.cmd_list.append(cmd)
            self.log('INFO', 'Added command:{} to command list'.format(cmd))


    def config(self, **kwargs):
        """Load config onto the device from the command list

        :return: True if successful.In all other cases False.

        :rtype: bool

        Example::

          Python:
            config()

          Robot:
            Config
        """

        self.log('INFO', 'Configuring the device')

        if self.dh is None:
            raise MyException('Device handle is not set, dh')

        # if more than 50 commands to be executed, Load config onto device from file
        if len(self.cmd_list) > 50:
            status = self.load_set_cfg(self.cmd_list)
        else:
            status = self.dh.config(
                command_list=self.cmd_list, **kwargs).status()

        self.cmd_list = []
        self.cmd = ''
        self._cmd_name_tag = None
        self._cmd_mapping = None

        self.log('INFO', 'Configured the device')

        return status

    def commit(self, **kwargs):
        """Commit the config on the device

        :return: True if successful.In all other cases False.

        :rtype: bool

        Example::

          Python:
            commit()

          Robot:
            Commit
        """

        self.log('INFO', 'Commiting the config on the  device')

        return self.dh.commit(**kwargs).status()

    def set_dh(self, device_handle):
        """Update the device handle

        :return: None

        :rtype: None

        Example::

          Python:
            set_dh(Device_handle)

          Robot:
            Set Dh ${Device_handle}
        """
        self.dh = device_handle

    def fn_checkin(self, message):
        """Checkin log message of the function

        :param string message:
            **REQUIRED** Checkin message to log

        :return: None

        :rtype: None

        Example::

            fn_checkin("Configuring NAT Pool")
        """

        stack = inspect.stack()[1]
        calling_file = os.path.basename(stack[1])
        line = stack[2]
        sub = stack[3]

        _new_msg = '{}:{}:{}() - {}'.format(calling_file, line, sub, message)

        #Comment until utils is commited
        # self.log('INFO', _new_msg, show_method=False)
        self.log('INFO', _new_msg)
        #self._chk_in_msg = message
        self._chk_in_msg[sub] = message

    def fn_checkout(self, result=True, err_msg=None, err_lvl='ERROR'):
        """Checkout log message of the function

        This method uses the checkin message and logs the modified message accordingly.
        It also asserts the result

        :param bool result:
            **REQUIRED** Result of the function being checked out

        :param string err_lvl:
            **OPTIONAL** Log level for error messages. Default is 'ERROR'

        :return: True if function passed else raises MyException

        :rtype: True or exception

        Example::

            return self.fn_checkout(result)
            return self.fn_checkout(False, err_msg="No valid output found")
            return self.fn_checkout(False, err_msg="No valid output found", err_lvl='INFO')
        """

        stack = inspect.stack()[1]
        calling_file = os.path.basename(stack[1])
        line = stack[2]
        sub = stack[3]

        caller_info = '{}:{}:{}()'.format(calling_file, line, sub)

        _chkin_msg = self._chk_in_msg[sub].split(' ')
        _chkout_msg = _chkin_msg[0].lower() + ' ' + ' '.join(_chkin_msg[1:])

        if err_msg is not None:
            #self.log(err_lvl, err_msg)
            #Comment until utils is commited
            # self.log(err_lvl, '{} - {}'.format(caller_info, err_msg), show_method=False)
            self.log(err_lvl, '{} - {}'.format(caller_info, err_msg))

        if result:
            self.log('INFO', "{} - Returning after {}".format(caller_info, _chkout_msg))
            return result
        else:
            self.log('ERROR', "{} - Error while {}".format(caller_info, _chkout_msg))
            if 'ERROR' in err_lvl.upper() and err_msg is not None:
                raise RuntimeError(err_msg)
