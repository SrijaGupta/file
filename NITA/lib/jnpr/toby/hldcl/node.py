"""
Module Node for system node
"""
import re
import time
from copy import copy
from jnpr.toby.exception.toby_exception import TobyException

class Node(object):
    """
    Class Node to create node objects.
    """

    def __init__(self, node_data):
        """
        Base class for node, 'controller' is often analogous to RE
        :param node_dict:
            **REQUIRED** node_data of node
        :return: node object based os and model
        """

        self.controllers = dict()
        self.current_controller = None
        self.current_controller_str = None
        # Stores the role (e.g. member0/member1) if applicable, otherwise 'null'
        if 'role' in node_data.keys():
            self.role = node_data['role']
        else:
            self.role = 'null'

        #supports multiple controllers (typically JUNOS only)
        for controller_name in node_data['controllers'].keys():
            if 'vc' in node_data.keys():
                node_data['controllers'][controller_name]['vc'] = node_data['vc']
            else:
                node_data['controllers'][controller_name]['vc'] = False

        if 'connect' in node_data.keys() and node_data['connect']:
            for controller_name in node_data['controllers'].keys():
                try:
                    if 'connect' in node_data['controllers'][controller_name].keys() and \
                            node_data['controllers'][controller_name]['connect']:
                        if node_data['controllers'][controller_name]['osname'].upper() == 'JUNOS':
                            from jnpr.toby.hldcl.juniper.junos import Junos
                            self.controllers[controller_name] = Junos(**node_data['controllers'][controller_name], re_name=controller_name)
                        elif node_data['controllers'][controller_name]['osname'].upper() == 'UNIX' or\
                            node_data['controllers'][controller_name]['osname'].upper() == 'LINUX' or \
                            node_data['controllers'][controller_name]['osname'].upper() == 'CENTOS' or \
                            node_data['controllers'][controller_name]['osname'].upper() == 'UBUNTU' or \
                            node_data['controllers'][controller_name]['osname'].upper() == 'SIFOS-LINUX' or \
                            node_data['controllers'][controller_name]['osname'].upper() == 'FREEBSD':
                            from jnpr.toby.hldcl.unix.unix import Unix
                            self.controllers[controller_name] = Unix(**node_data['controllers'][controller_name])
                        elif node_data['controllers'][controller_name]['osname'].upper() == 'WINDOWS':
                            if 'selenium' in node_data['controllers'][controller_name] and \
                                             node_data['controllers'][controller_name]['selenium'] == "enable":
                                from jnpr.toby.hldcl.windows.selenium.selenium import Selenium
                                self.controllers[controller_name] = Selenium(**node_data['controllers'][controller_name])
                            else:
                                from jnpr.toby.hldcl.windows.windows import Windows
                                self.controllers[controller_name] = Windows(**node_data['controllers'][controller_name])
                        elif node_data['controllers'][controller_name]['osname'].upper() == 'IOS':
                            from jnpr.toby.hldcl.cisco.cisco import Cisco
                            self.controllers[controller_name] = Cisco(**node_data['controllers'][controller_name])
                        elif node_data['controllers'][controller_name]['osname'].upper() == 'BROCADE':
                            from jnpr.toby.hldcl.brocade.brocade import Brocade
                            self.controllers[controller_name] = Brocade(**node_data['controllers'][controller_name])
                        elif node_data['controllers'][controller_name]['osname'].upper() == 'SRC':
                            from jnpr.toby.hldcl.src.src import Src
                            self.controllers[controller_name] = Src(**node_data['controllers'][controller_name])
                        else:
                            raise TobyException("OS is not supported " + self.controllers['controller_name']['osname'])
                        setattr(self.controllers[controller_name], 'controllers_data', node_data['controllers'][controller_name])
                    else:
                        t.log("Skipping the connection for '" + controller_name + "'")
                        # sleep required to prevent multithreading race condition
                        time.sleep(1)
                except Exception as exp:
                    raise TobyException("%s(%s) " % (str(exp), str(controller_name)))

            if self.controllers:
                self._set_current_controller()

    def _set_current_controller(self, role='MASTER'):
        if len(self.controllers.keys()) == 1:
            self.current_controller_str = list(self.controllers.keys())[0]
            self.current_controller = self.controllers[self.current_controller_str]
            self.current_controller.dual_controller = False
        else:
            for controller in self.controllers.keys():
                self.controllers[controller].dual_controller = True
                if role.upper() == 'MASTER':
                    if self.controllers[controller].is_master():
                        self.current_controller = self.controllers[controller]
                        self.current_controller_str = controller
                        break
                elif role.upper() == 'BACKUP':
                    if not self.controllers[controller].is_master():
                        self.current_controller = self.controllers[controller]
                        self.current_controller_str = controller
                        break
                else:
                    raise TobyException("Invalid Role provided, valid values are'Master/Backup'")
        if not self.current_controller:
            raise TobyException("Unable to set current_controller")

    def switch_controller(self, controller):
        """
            switch current controllerrouting engine
        """
        if len(self.controllers.keys()) == 2:
            for controller in self.controllers.keys():
                if controller is not self.current_controller_str:
                    self.current_controller = self.controllers[controller]
                    self.current_controller_str = controller
                    break

    def add_channel(self, channel_type, controller='current', channel_attributes=None):
        """
            Add new Channel to Channel Object
            :param channel_type:
                *MANDATORY* Type to channel to create , currently supports snmp, grpc only
            :param controller:
                *OPTIONAL* Controller to create the channel
            :param channel_attributes:
                *OPTIONAL* Arguments required for creating the channel
            :return: 1-D dictionary of channel ID per controller
        """
        controller = controller.lower()
        channel_dict = dict()
        if controller == 'current':
            current_controller = self.current_controller_str
            return_dict = self.current_controller.add_channel(channel_type, channel_attributes)
            channel_dict[current_controller] = return_dict
            channel_dict['current_controller'] = return_dict
        elif controller == 'all':
            for controller_to_call in self.controllers.keys():
                channel_dict[controller_to_call] = self.controllers[controller_to_call].add_channel(channel_type,
                                                                                                    channel_attributes)
        elif controller in self.controllers.keys():
            channel_dict[controller] = self.controllers[controller].add_channel(channel_type,
                                                                                channel_attributes)
        else:
            raise TobyException("Controller %s does not exist for the device" % controller)
        return channel_dict
