"""
Class for System
"""
from jnpr.toby.hldcl.system import System
from jnpr.toby.hldcl.cisco.cisco import Cisco
from jnpr.toby.hldcl.cisco.cisco import IOS
import time
from jnpr.toby.hldcl.host import Host


class CiscoSystem(System):
    """
    Class Node to create IOS node objects.
    """

    def __init__(self, system_data, connect_complex_system=False,
                 connect_dual_re=False):
        """
        Base class for IOS system
        :param systemdict:
            **REQUIRED** system_data
        :return: system object based
        """
        default_connect = True
        if list(self.findkeys(system_data['system'], 'connect')).__len__() > 0:
            default_connect = False
        self.node_connect = self.is_node_connect_set(system_data)
        for system_node in system_data['system'].keys():
            if default_connect or not self.node_connect:
                # This need to be modified to detect the master node when none
                # of the node has connect set
                if connect_complex_system or system_node == 'primary':
                    system_data['system'][system_node]['connect'] = True
                elif 'connect' not in system_data[
                    'system'][system_node].keys():
                    t.log("Skipping connection for for node %s" % system_node)
                    continue
            self.controller_connect = self.is_controller_connect_set(
                system_data['system'][system_node])
            for controller in sorted(list(system_data['system'][system_node][
                    'controllers'].keys())):
                if default_connect or (
                    'connect' in system_data['system'][
                        system_node].keys() and not self.controller_connect):
                    if len(system_data['system'][
                            system_node]['controllers']) == 1:
                        t.log("Setting the active RE as %s" % controller)
                        system_data['system'][system_node][
                            'controllers'][controller]['connect'] = True
                        break
                    t.log("Determining the active RE")
                    dev_data = Cisco(**system_data[
                        'system'][system_node]['controllers'][controller])
                    Host._object_counts[system_data['system'][system_node][
                        'controllers'][controller]['hostname']] -= 1

        super(CiscoSystem, self).__init__(system_data)

    def cli(self, **kwargs):
        """
            Execute cli command on device
            device_object.cli(command = 'show version detail | no-more',
            channel = 'text')
        """
        t.log(level="DEBUG", message="Entering 'cli'\n"+__file__)
        return_value = self.current_node.current_controller.cli(**kwargs)
        t.log(level="DEBUG", message="Exiting 'cli' with return "
              "value/code :\n" + str(return_value))
        return return_value

    def config(self, **kwargs):
        """
            Execute config command on device

            device_object.config(command_list = ['set services telnet',
            'delete services web-management', 'show | compare'])
        """
        t.log(level="DEBUG", message="Entering 'config'\n"+__file__)
        return_value = self.current_node.current_controller.config(**kwargs) 
        t.log(level="DEBUG", message="Exiting 'config' with return"
              " value/code :\n" + str(return_value))
        return return_value

    def save_config(self, **kwargs):
        """
            Save config on device

            device_object.save_config(file = 'temp_config.conf',
            source = 'committed')
        """
        t.log(level="DEBUG", message="Entering 'save_config'\n"+__file__)
        return_value = self.current_node.current_controller.save_config(**kwargs)
        t.log(level="DEBUG", message="Exiting 'save_config' with "
              "return value/code :\n" + str(return_value))
        return return_value

    def clean_config(self, **kwargs):
        """
            Clean configuration on device

            device_object.clean_config(config_file = 'baseline-config.conf')
        """
        t.log(level="DEBUG", message="Entering 'clean_config'\n"+__file__)
        return_value = self.current_node.current_controller.clean_config(
            **kwargs)
        t.log(level="DEBUG", message="Exiting 'save_config' with return "
              "value/code :\n" + str(return_value))
        return return_value

    def upgrade(self, **kwargs):
        """
            Upgrade device image
            device_object.upgrade(url= 'flash', image='image path or name')
        """
        t.log(level="DEBUG", message="Entering 'upgrade'\n" + __file__)
        return_value = self.current_node.current_controller.upgrade(**kwargs)
        t.log(level="DEBUG", message="Exiting 'upgrade' with"
              " return value/code :\n" + str(return_value))
        return return_value

    def switchover(self, **kwargs):
        """
            Upgrade device image

            device_object.switchover(options='merge', wait=180)
        """
        t.log(level="DEBUG", message="Entering 'switchover'\n" + __file__)
        return_value = self.current_node.current_controller.switchover(
            **kwargs)
        t.log(level="DEBUG", message="Exiting 'switchover' with "
              "return value/code :\n" + str(return_value))
        return return_value

    def load_config(self, **kwargs):
        """
            Upgrade device image

            device_object.load_config(**kwargs)
        """
        t.log(level="DEBUG", message="Entering 'load_config'\n"+__file__)
        return_value = self.current_node.current_controller.load_config(
            **kwargs)
        t.log(level="DEBUG", message="Exiting 'load_config' with "
              "return value/code :\n" + str(return_value))
        return return_value
