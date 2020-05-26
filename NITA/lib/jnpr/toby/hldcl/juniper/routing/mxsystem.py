"""
Class for System
"""
import re
import time
from jnpr.toby.hldcl.juniper.junipersystem import JuniperSystem
from jnpr.toby.exception.toby_exception import TobyException

class MxSystem(JuniperSystem):
    """
    Class System to create JunOS MX System object.
    """
    def __init__(self, system_data):
        """

        Base class for JunOS MX system

        :param nodedict:
            **REQUIRED** systemdict of node
        :return: MX system object
        """
        self.vc = False
        if system_data is not None and len(system_data['system'].keys()) > 1:
            for node in system_data['system'].keys():
                if re.search(r'member(\s+)?(\d+)', node, re.I):
                    self.vc = True
                    break
        for node in system_data['system'].keys():
            if self.vc:
                system_data['system'][node]['vc'] = True
            else:
                system_data['system'][node]['vc'] = False

        t.log(level="INFO", message="vc system: " + str(self.vc))
        super(MxSystem, self).__init__(system_data)
        if self.vc:
            self.log(level="INFO", message="Set the controler to master RE of master node")
            self.set_master_node_controller()

    def switch_re_master(self):
        self.log(level="DEBUG", message="Entering 'switch_re_master'\n" + __file__)

        if self.vc:
            if not self.current_node.current_controller.switch_re_master():
                t.log(level="DEBUG", message="Exiting 'switch_re_master' with return value/code :\n"+str(False))
                return False
            ## Set the controller to corrent master member and master RE.
            time.sleep(300)
            self.reconnect(all=True)
            time.sleep(30)
            self.set_master_node_controller()
            return True
        else:
            return super(MxSystem, self).switch_re_master()


    def reboot(self, wait=0, mode='shell', timeout=None, interval=20, all=False, device_type=None, system_nodes=None, command_args=None):
        """
        Reboot device

        Returns: True if device is rebooted and reconnection is successful, else an Exception is raised
        Example:
            device_object.reboot(all=True, timeout=200)

        Example: device_object.reboot(all=True)

        """
        self.log(level="DEBUG",
                 message="Entering 'reboot API'\n" + __file__)
        try:
            result = super(MxSystem, self).reboot(wait=wait, mode=mode, \
                           timeout=timeout, interval=interval, all=all, device_type=device_type, \
                           system_nodes=system_nodes, command_args=command_args)
        except:
            self.log(level="ERROR", message="Failed to reboot the device. Resetting the master.")
            if self.vc and all:
                self.set_master_node_controller()
            raise TobyException("Unable to reboot all REs of device.")

        if result:
            self.log(level="INFO", message="Reboot has passed")

            if self.vc and all:
                self.set_master_node_controller()
            return True
        else:
            self.log(level="ERROR", message="Failed to reboot the device")
            return False

    def reconnect(self, all=False, **kwargs):
        """
            Reconnect the device
        """
        t.log(level="DEBUG", message="Entering 'reconnect'\n"+__file__)

        result = super(MxSystem, self).reconnect(all=all, **kwargs)

        if result:
            self.log(level="INFO", message="Reconnect to the device is successful")

            if self.vc and all:
                self.set_master_node_controller()
            return True
        else:
            self.log(level="ERROR", message="Failed to reconnect the device")
            return False

    def set_master_node_controller(self):
        """
        Sets the controller to master re
        :return: True(boolean) in case the handle pointer changes correctly.

        :raises: Exception
        """
        master = self.detect_master_node()
        t.log(level="INFO", message="Master of VC chassis is : '%s'" % master)
        t.log(level="INFO", message="Set the current contorller to master node and master controller")

        super(MxSystem, self).set_current_controller(controller="master", system_node=master)
        return True

    def set_current_controller(self, controller, system_node):
        """
            Device object will set its system node('primary'/'slave'/'member1') to a particular controller('re0'/'re1')
            **This will not change the current system node for the device object**

                device_object.set_current_controller(system_node='member1', controller='re1')

                device_object.set_current_controller(controller='re1')

                Below examples are also valid in case of MXVC,
                    device_object.set_current_controller(system_node='master', controller='backup')
                    device_object.set_current_controller(system_node='master', controller='master')
                    device_object.set_current_controller(system_node='backup', controller='backup')
                    device_object.set_current_controller(system_node='backup', controller='master')

            :param system_node:
                *OPTIONAL* name of the system node('primary'/'slave'/'member1') to process current controller change.
                Default is current system node.

            :param controller:
                *MANDATORY* name of the controller('re0'/'re1') to point to.

            :return: True(boolean) in case the handle pointer changes correctly.

            :raises: Exception, in case passed parameter values do not exist in the device object's System Dictionary.
        """
        if self.vc and (system_node.upper() == 'MASTER' or system_node.upper() == 'BACKUP'):
            if system_node.upper() == 'MASTER':
                master = self.detect_master_node()
                t.log("master_member : " + master)
                super(MxSystem, self).set_current_controller(controller=controller, system_node=master)
                return True
            elif system_node.upper() == 'BACKUP':
                master = self.detect_master_node()
                backup = 'member1' if master == 'primary' else 'primary'
                if backup not in self.nodes.keys():
                    backup = 'member 1'
                t.log("master_member : " + master)
                t.log("backup_member : " + backup)
                super(MxSystem, self).set_current_controller(controller=controller, system_node=backup)
                return True
        else:
            super(MxSystem, self).set_current_controller(controller=controller, system_node=system_node)
            return True

    def detect_master_node(self):
        """

        :return:
        """
        facts = self._refresh_fact(refresh_key='vc_master')

        t.log(level="INFO", message="Value of vc_master from pyez facts: %s" %facts['vc_master'])
        for _ in range(90):
            t.log(level="INFO", message="vc_master : %s" %facts['vc_master'])
            if facts['vc_master'] == None:
                t.log(level="INFO", message="vc_master info in pyez_facts is None. Retrying to refresh 'vc_master' fact after 10 seconds")
                time.sleep(10)
                facts = self._refresh_fact(refresh_key='vc_master')
            else:
                break

        t.log(level="INFO", message="pyez_facts : %s" % (facts))

        if facts['vc_master'] == None:
            raise TobyException("Unable to get the VC master from the pyez facts with timeout"
                                " of 15 minutes. Failed to set the controller object to master"
                                " node of the master controller", host_obj=self)

        master = 'member1' if (facts and 'vc_master' in facts and facts['vc_master'] == '1') else 'primary'
        if master not in self.nodes.keys():
            master = 'member 1'

        t.log(level="INFO", message="vc_master : %s " %master)
        t.log(level="INFO", message="Exiting 'detect_master_node' with return value/code :\n" + str(master))
        return master

    def _refresh_fact(self, refresh_key=None):
        if refresh_key:
            self.current_node.current_controller.channels['pyez'].facts_refresh(keys=[refresh_key])
        else:
            self.current_node.current_controller.channels['pyez'].facts_refresh()

        return self.current_node.current_controller.channels['pyez'].facts

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
            system_core_count = super(MxSystem, self).detect_core(command='show system core-dump local')
        else:
            system_core_count = super(MxSystem, self).detect_core()

        if system_core_count:
            t.log(level='WARN', message='Core is found on the device : ' + system_name + ' and its count is ' +str(system_core_count))
            return True
        t.log('Core is not found on the device : ' + system_name)
        return False


    def software_install(self, **kwargs):
        """
            Software install handle on device

        """
        if self.vc:
            kwargs['controllers_all'] = False
        super(MxSystem, self).software_install(**kwargs)

