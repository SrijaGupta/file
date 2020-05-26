"""
Class for System
"""
import re
from jnpr.toby.hldcl.node import Node
from jnpr.toby.hldcl.juniper.junipernode import JuniperNode
from jnpr.toby.hldcl.juniper.security.srxnode import SrxNode
from jnpr.toby.hldcl.juniper.routing.mxnode import MxNode
from jnpr.toby.hldcl.juniper.security.nfxnode import NfxNode
from jnpr.toby.hldcl.cisco.cisconode import CiscoNode
from jnpr.toby.hldcl.brocade.brocadenode import BrocadeNode
from jnpr.toby.hldcl.src.srcnode import SrcNode
from jnpr.toby.exception.toby_exception import TobyException


class System(object):
    """
    Class System to house node objects.
    """

    def __init__(self, system_data=None):
        """

        Base class for System
        :param nodedict:
            **REQUIRED** system_data of System
        :return: system object based os and model
        """

        self.nodes = {}
        self.current_node = None
        if not system_data:
            raise TobyException('System data not passed to init.')
        if list(self.findkeys(system_data['system'], 'connect')).__len__() <= 0:
            system_data['system']['primary']['connect'] = True
            for controller in system_data['system']['primary']['controllers'].keys():
                system_data['system']['primary']['controllers'][controller]['connect'] = True

        for node in system_data['system'].keys():
            if self.is_controller_connect_set(system_data['system'][node]):
                system_data['system'][node]['connect'] = True
            if 'tag_name' in system_data['system'][node].keys() and system_data['system'][node]['tag_name'] is not None:
                for controller in system_data['system'][node]['controllers'].keys():
                    system_data['system'][node]['controllers'][controller]['tag_name'] = \
                        system_data['system'][node]['tag_name']

        for node in system_data['system'].keys():
            if 'model' in system_data['system'][node] and \
            system_data['system'][node]['model'] and \
            (re.search(r'SRX\d*', str(system_data['system'][node]['model']), re.I) or \
            re.search(r'ha_cluster', str(system_data['system'][node]['model']), re.I)):
                self.nodes[node] = SrxNode(node_data=system_data['system'][node])
            elif 'model' in system_data['system'][node] and \
            system_data['system'][node]['model'] and \
            (re.search(r'MX\d*', str(system_data['system'][node]['model']), re.I)):
                self.nodes[node] = MxNode(node_data=system_data['system'][node])
            elif 'model' in system_data['system'][node] and \
            system_data['system'][node]['model'] and \
            (re.search(r'NFX\d*', str(system_data['system'][node]['model']), re.I)):
                self.nodes[node] = NfxNode(node_data=system_data['system'][node])
            elif system_data['system'][node]['osname'].upper() == 'JUNOS':
                self.nodes[node] = JuniperNode(node_data=system_data['system'][node])
            elif system_data['system'][node]['osname'].upper() == '':
                self.nodes[node] = JuniperNode(node_data=system_data['system'][node])
            elif system_data['system'][node]['osname'].upper() == 'IOS':
                self.nodes[node] = CiscoNode(node_data=system_data['system'][node])
            elif system_data['system'][node]['osname'].upper() == 'BROCADE':
                self.nodes[node] = BrocadeNode(node_data=system_data['system'][node])
            elif system_data['system'][node]['osname'].upper() == 'SRC':
                self.nodes[node] = SrcNode(node_data=system_data['system'][node])
            else:
                self.nodes[node] = Node(node_data=system_data['system'][node])

        if not self.nodes:
            raise TobyException("Unable to create any nodes (ex: Connection to 'primary')")
        self._set_current_node()

    def reboot(self, wait=0, mode='shell', timeout=None, interval=20, all=False, device_type=None, system_nodes=None, command_args=None):
        """
        Reboot device
        :param wait:
            *OPTIONAL* Time to sleep before reconnecting, Default value is 0

        :param mode:
            *OPTIONAL* Mode in which reboot needs to be executed. Default is 'shell'. Also supports 'cli'. mode=cli is
            valid only for Junos devices.

        :param timeout:
            *OPTIONAL* Time to reboot and connect to device. Default is set based the device model.

        :param interval:
            *OPTIONAL* Interval at which reconnect need to be attempted after reboot is performed. Default is 20 seconds

        :param all:
            *OPTIONAL* Valid only if the device is of Junos. When set to True, all JUNOS REs are rebooted
                 simultaneously. Default is False, where only the current RE is rebooted. If the OS is not JUNOS,
                 all=True raises an exception.

        :param device_type:
            *OPTIONAL* This option works only with 'text' channel.
            Value should be set to 'vmhost' to reboot the vmhost

        :param STR system_nodes:
            *OPTIONAL* Values which can be passed: all-members, local, member1,member2...member n  etc can be passed .
            Initial phase supports only for QFX series. For other models it is not yet supported.

        :param LIST command_args:
              *OPTIONAL List of reboot optional arguments can be passed.
               In the current phase this argument is not applicable for python workflow.

        Returns: True if device is rebooted and reconnection is successful, else an Exception is raised        Example:
            device_object.reboot(all=True, timeout=200)

        Example: device_object.reboot(all=True)

        """
        #This will call the controllers reboot
        return self.current_node.current_controller.reboot(wait=wait, mode=mode, timeout=timeout, interval=interval, device_type=device_type,
                                                           system_nodes=system_nodes, command_args=command_args)



    def reconnect(self, all=False, **kwargs):
        """
            Reconnect the device
        """
        if all:
            for node_name in self.nodes.keys():
                for controller_name in self.nodes[node_name].controllers.keys():
                    reconnect_controller = self.nodes[node_name].controllers[controller_name]
                    response = reconnect_controller.reconnect(**kwargs)
                    if not response:
                        raise TobyException('Unable to reconnect to all REs')
            return True
        else:
            return self.current_node.current_controller.reconnect(**kwargs)

    def _set_current_node(self, set_node=None):
        if set_node is not None:
            self.current_node = self.nodes[set_node.lower()]
        elif len(self.nodes.keys()) == 1:
            self.current_node = self.nodes[list(self.nodes.keys())[0]]
        else:
            for node in self.nodes:
                try:
                    if self.nodes[node].is_node_master():
                        self.current_node = self.nodes[node]
                        break
                except Exception:
                    pass
            if self.current_node is None:
                for node in self.nodes:
                    try:
                        if not self.nodes[node].is_node_master():
                            t.log(level="INFO", message="Since could not find active node, setting " + node + " as active node")
                            self.current_node = self.nodes[node]
                            break
                    except Exception:
                        pass
        if self.current_node is None:
            raise TobyException('Error : Could not set current node for the system')

    def shell(self, **kwargs):
        """
            Execute Shell command on device
        """
        return_value = self.current_node.current_controller.shell(**kwargs)
        return return_value

    def su(self, **kwargs):
        """
            switch to super user mode on device
        """
        return_value = self.current_node.current_controller.su(**kwargs)
        return return_value

    def disconnect(self, **kwargs):
        """
            Disconnect device
        """
        return_value = self.current_node.current_controller.disconnect(**kwargs)
        return return_value

    def get_current_controller_name(self):
        """
            Get controller slot name of current RE
        """
        return_value = self.current_node.current_controller_str
        return return_value

    def close(self, **kwargs):
        """
            Close the device object
        """
        return_value = self.current_node.current_controller.close(**kwargs)
        return return_value

    def upload(self, **kwargs):
        """
            Upload file to device
        """
        return_value = self.current_node.current_controller.upload(**kwargs)
        return return_value

    def download(self, **kwargs):
        """
            Download file from device
        """
        return_value = self.current_node.current_controller.download(**kwargs)
        return return_value

    def log(self, message, level='info'):
        """
            Logging for the device
        """
        return self.current_node.current_controller.log(message=message, level=level)

    def vty(self, command, destination, timeout=60, pattern=None, raw_output=False):
        """
            Execute vty command on device
        """
        return_value = self.current_node.current_controller.vty(command, destination, timeout, pattern, raw_output)
        return return_value

    def cty(self, command, destination, timeout=60, pattern=None, raw_output=False):
        """
            Execute vty command on device
        """
        return_value = self.current_node.current_controller.cty(command, destination, timeout, pattern, raw_output)
        return return_value

    def set_current_system_node(self, system_node):
        """
        Device object will set its current_node(attribute) to a particular system node('primary'/'slave'/'member1')

            device_object.set_current_system_node(system_node='member1')

            device_object.set_current_system_node(system_node='primary')

        :param system_node:
            *MANDATORY* name of the system node('primary'/'slave'/'member1') to point to.

        :return: True(boolean) in case the handle pointer changes correctly.

        :raises: Exception, in case passed parameter values do not exist in the device object's System Dictionary.
        """
        if system_node not in self.nodes.keys():
            raise TobyException('Parameter values passed are invalid. system_node :"'
                                + str(system_node) + '" is not a part of device object')
        self.current_node = self.nodes[system_node]
        return True

    def set_current_controller(self, controller, system_node):
        """
            Device object will set its system node('primary'/'slave'/'member1') to a particular controller('re0'/'re1')
            **This will not change the current system node for the device object**

                device_object.set_current_controller(system_node='member1', controller='re1')

                device_object.set_current_controller(controller='re1')

            :param system_node:
                *OPTIONAL* name of the system node('primary'/'slave'/'member1') to process current controller change.
                Default is current system node.

            :param controller:
                *MANDATORY* name of the controller('re0'/'re1') to point to.

            :return: True(boolean) in case the handle pointer changes correctly.

            :raises: Exception, in case passed parameter values do not exist in the device object's System Dictionary.
        """
        if system_node == 'current':
            if controller not in self.current_node.controllers.keys() and not (controller.upper() == 'MASTER' or controller.upper() == 'BACKUP'):
                raise TobyException('Parameter values passed are invalid. controller :"'
                                    + str(controller) + '" is not a part of device object')
            if controller.upper() == 'MASTER' or controller.upper() == 'BACKUP':
                self.current_node._set_current_controller(role=controller)
            else:
                self.current_node.current_controller = self.current_node.controllers[controller]
                self.current_node.current_controller_str = controller
        else:
            if system_node not in self.nodes.keys():
                raise TobyException('Parameter values passed are invalid. system_node :"'
                                    + str(system_node) + '" is not a part of device object')
            self.current_node = self.nodes[system_node]
            if controller not in self.nodes[system_node].controllers.keys() \
                and not (controller.upper() == 'MASTER' or controller.upper() == 'BACKUP'):
                self.nodes[system_node].current_controller.log(level='ERROR',
                                                               message='Parameter values passed are invalid. controller :"'
                                                               + str(controller) + '" is not a part of device object')
                raise TobyException('Parameter values passed are invalid. controller :"'
                                    + str(controller) + '" is not a part of device object')
            if controller.upper() == 'MASTER' or controller.upper() == 'BACKUP':
                self.nodes[system_node]._set_current_controller(role=controller)
            else:
                self.current_node.current_controller = self.nodes[system_node].controllers[controller]
                self.current_node.current_controller_str = controller
        t.log(level="DEBUG", message="Exiting 'set_current_controller' with return value/code :\n True")
        return True

    def findkeys(self, node, kv):
        """
            convenience method for finding keys in a node
        """
        if isinstance(node, list):
            for i in node:
                for x in self.findkeys(i, kv):
                    yield x
        elif isinstance(node, dict):
            if kv in node:
                yield node[kv]
            for j in node.values():
                for x in self.findkeys(j, kv):
                    yield x

    @staticmethod
    def is_node_connect_set(system):
        """
            check if connect key is in node
        """
        for system_node in system['system'].keys():
            if 'connect' in system['system'][system_node].keys():
                return 1

    @staticmethod
    def is_controller_connect_set(node):
        """
            check to see if connect in controller
        """
        for controller in node['controllers'].keys():
            if 'connect' in node['controllers'][controller].keys():
                return 1

    def get_model(self):
        """
            get_model api gets model info from the box.
            For Junos boxes gets model info from the system info
            For Linux boxes it parses the content of the file "/etc/issue" on the box
            For FreeBsd Boxes it parces 'uname -a' ouput
        """
        return_value = self.current_node.current_controller.get_model()
        return return_value

    def get_host_name(self):
        """
        Gets the hostname  of the device

        """
        return_value = self.current_node.current_controller.get_host_name()
        return  return_value

    def get_version(self, **kwargs):
        """
            get_version api get the version info from the box.
            For Junos boxes it gets the version info from the facts info from pyez channel
            For Unix/Linux boxes get the version info from 'uname -r' command
            :param major:
                *OPTIONAL* based on user request API returns only the major version info.
        """
        return_value = self.current_node.current_controller.get_version(**kwargs)
        return return_value

    def get_vmhost_infra(self, **kwargs):
        """
            get_vmhost_infra api get whether the box has vmhost infra or not.
        """
        return_value = self.current_node.current_controller.get_vmhost_infra(**kwargs)
        return return_value


    def add_channel(self, channel_type, system_node='current', controller='current', channel_attributes=None):
        """
            Add new Channel to Device Object
            :param channel_type:
                *MANDATORY* Type to channel to create , currently supports snmp,grpc only
            :param system_node:
                *OPTIONAL* Node to create the channel
            :param controller:
                *OPTIONAL* Controller to create the channel
            :param channel_attributes:
                *OPTIONAL* Arguments required for creating the channel
            :return: 2-D dictionary of channel IDs
                     i.e., per system node per controller

        """
        system_node = system_node.lower()
        channel_dict = dict()
        if system_node == 'current':
            return_dict = self.current_node.add_channel(channel_type, controller, channel_attributes)
            channel_dict['current_node'] = return_dict
            for node_key in self.nodes.keys():
                if self.current_node == self.nodes[node_key]:
                    channel_dict[node_key] = return_dict
        elif system_node == 'all':
            for node_to_call in self.nodes.keys():
                channel_dict[node_to_call] = self.nodes[node_to_call].add_channel(channel_type,
                                                                                  controller,
                                                                                  channel_attributes)
        elif system_node in self.nodes.keys():
            channel_dict[system_node] = self.nodes[system_node].add_channel(channel_type,
                                                                            controller,
                                                                            channel_attributes)
        else:
            raise TobyException("System Node %s does not exist for the device" % system_node)
        return channel_dict

    def add_mode(self, mode=None, origin='shell', command=None, pattern=None,
                 exit_command=None, targets=None):
        """
            :param device:
                *MANDATORY* Device handle on which custom mode is to
                be added.
            :param mode:
                *MANDATORY* Name of the custom mode.
            :param origin:
                *OPTIONAL* The starting point from which the custom mode is entered.
                By default this is 'shell' but 'cli' is the other option.
            :param command:
                *MANDATORY* Command by which to enter custom mode.
            :param pattern:
                *MANDATORY* Pattern to be expected after giving
                command.
            :param exit_command:
                *MANDATORY* Command to exit out of the mode.
            :param targets:
                *OPTIONAL* Used to pass more than one target.
                Only required if more than one target is used.
                If used, then the previous arguments are not
                required except for device and mode.
            Returns: True if succesfully adds more, otherwise
            raises an Exception.
        """
        # if all:
        #     for node_name in self.nodes.keys():
        #         for controller_name in self.nodes[node_name].controllers.keys():
        #             controller_to_add_to = self.nodes[node_name].controllers[controller_name]
        #             response = controller_to_add_to.add_mode(mode=mode, command=command, pattern=pattern,
        #                                                      exit_command=exit_command, targets=targets)
        #             if not response:
        #                 self.log(level='ERROR',message='Unable to add mode')
        #                 raise TobyException('Unable to add mode')
        # else:
        self.current_node.current_controller.add_mode(mode=mode, origin=origin,
                                                      command=command,
                                                      pattern=pattern,
                                                      exit_command=exit_command,
                                                      targets=targets)
        return True

    def execute_command(self, mode=None, command=None,
                        timeout=60, pattern=None):
        """
            Executes commands on specific mode

            :param mode:
                **REQUIRED** mode in which the command should be executed
            :param origin:
                *OPTIONAL* mode from which the custom mode starts at
            :param command:
                **REQUIRED** command to execute
            :param timeout:
                *OPTIONAL* Time by which response should be received. Default is
                60 seconds
            :param pattern:
                *OPTIONAL* Pattern to match.
            :return: Object with the following methods
                'response()': Response from the command
        """
        return_value = self.current_node.current_controller.execute_command(mode=mode,
                                                                            command=command,
                                                                            timeout=timeout,
                                                                            pattern=pattern)
        return return_value

    def set_device_timeout(self, target, timeout=120):
        """
            Sets the timeout value for each controller
            Example:
            set device timeout   ${dh}    target=cli    timeout=240
            :params device:
                *REQUIRED* Device handle
            :params target:
                *REQUIRED* target action, supported targets are shell/cli/config/reboot/reconnect/pyez
            :params timeout:
                *OPTIONAL* expected timeout value
                default is 120
            :return: True
        """
        for node in self.nodes.keys():
            for controller_name in self.nodes[node].controllers.keys():
                timeout_key = target.lower() + "_timeout"
                if hasattr(self.nodes[node].controllers[controller_name], timeout_key):
                    setattr(self.nodes[node].controllers[controller_name], timeout_key, int(timeout))
                if target.lower() == 'pyez' and hasattr(self.nodes[node].controllers[controller_name], 'channels'):
                    self.nodes[node].controllers[controller_name].channels['pyez'].__setattr__('timeout', int(timeout))
        return True
