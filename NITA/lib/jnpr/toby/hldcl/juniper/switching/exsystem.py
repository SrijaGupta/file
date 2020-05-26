"""
Class for Qfxsystem
"""
import re
from jnpr.toby.hldcl.juniper.junipersystem import JuniperSystem
class ExSystem(JuniperSystem):
    """
    Class System to create JunOS Ex System object.
    """
    def __init__(self, system_data):
        """

        Base class for JunOS Qfx system

        :param nodedict:
            **REQUIRED** systemdict of node
        :return: Ex system object
        """
        self.vc = False  # pylint: disable=invalid-name
        if system_data is not None and len(system_data['system'].keys()) > 1:
            for node in system_data['system'].keys():
                if re.search(r'member(\d+)', node):
                    self.vc = True
                    break

        super(ExSystem, self).__init__(system_data)
        t.log(level='INFO', message="EX VC %s " % self.vc)

    def detect_core(self, core_path=None, resource=None, command=None):
        """
            Detect cores on the device
        """
        system_core_count = 0
        system_name = ''

        if resource is not None:
            t.log('name in system: '+ t.get_t(resource=resource, attribute='name'))
            system_name = t.get_t(resource=resource, attribute='name')

        if self.vc:
            system_core_count = super(ExSystem, self).detect_core(command='show system core-dump local')
        else:
            system_core_count = super(ExSystem, self).detect_core()

        if system_core_count:
            t.log(level='WARN', message='Core is found on the device : ' + system_name + ' and its count is ' +str(system_core_count))
            return True
        t.log('Core is not found on the device : ' + system_name)
        return False

    def detect_master_node(self):
        """

        :return:
        """
        master = 'primary'
        return master
