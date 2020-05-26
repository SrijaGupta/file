"""
Class for System
"""
from jnpr.toby.hldcl.system import System
from jnpr.toby.hldcl.brocade.brocade import Brocade
import time
from jnpr.toby.hldcl.host import Host

class BrocadeSystem(System):
    """
    Class Node to create Brocade node objects.
    """

    def __init__(self, system_data, connect_complex_system=False,
                 connect_dual_re=False):
        """
        Base class for brocade system
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
                    dev_data = Brocade(**system_data[
                        'system'][system_node]['controllers'][controller])
                    Host._object_counts[system_data['system'][system_node][
                        'controllers'][controller]['hostname']] -= 1

        super(BrocadeSystem, self).__init__(system_data)
