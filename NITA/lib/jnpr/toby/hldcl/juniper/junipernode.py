"""
Class for JuniperNode Devices
"""
from jnpr.toby.hldcl.node import Node


class JuniperNode(Node):
    """
    Class Node to create JunOS node objects.
    """

    def __init__(self, node_data):
        """
        Base class for JunOS devices

        :param nodedict:
            **REQUIRED** node_data of node
        :return: node object based os and model
        """
        super(JuniperNode, self).__init__(node_data)

    def reboot(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        reboot_all = kwargs.pop('all', False)
        if not reboot_all:
            return self.current_controller.reboot(**kwargs)
        re0 = self.controllers['re0'].reboot(**kwargs)
        re1 = self.controllers['re1'].reboot(**kwargs)
        if re0 and re1:
            self._set_current_controller()
            return True
        return False

    def is_node_master(self):
        """
            return true if the current node is master else false
        """
        if self.current_controller.is_master():
            return True
        return False

    def get_testcase_name(self):
        """
           Set the test stage using the robot builtin variable.
        """
        from robot.libraries.BuiltIn import BuiltIn
        t._test_stage = BuiltIn().get_variable_value('${TEST_NAME}')

    def detect_core(self, core_path=None, system_name=None, re1_hostname=None, command=None):
        """
            Detect cores on the device
        """
        cont_core_count = 0
        self.get_testcase_name()
        for controller in self.controllers:
            cont_core_count += self.controllers[controller].detect_core(core_path=core_path, \
                               system_name=system_name, re1_hostname=re1_hostname, command=command)
        return cont_core_count

    def save_current_config(self, file):
        """
            Save config file on the device with the <script_name>_id_pid.conf
        """
        for controller in self.controllers:
            self.controllers[controller].save_config(file)
        return True

    def load_saved_config(self, file, config_timeout=None):
        """
            load saved config on the current RE or master RE (in case of dual-re device) from the file (<script_name>_id_pid>)
        """
        for controller in self.controllers:
            if self.controllers[controller].is_master():
                kwargs = {}
                kwargs['remote_file'] = file
                kwargs['option'] = 'update'
                if config_timeout:
                    kwargs['timeout'] = config_timeout
                self.controllers[controller].load_config(**kwargs)
                break
        return True
