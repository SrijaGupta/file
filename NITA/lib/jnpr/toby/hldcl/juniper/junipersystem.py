"""
Class for System
"""
# pylint: disable=unused-argument,unused-variable,locally-disabled,import-error
from jnpr.toby.hldcl.system import System
from jnpr.toby.hldcl.juniper.junos import Juniper
import time
import re
from jnpr.toby.hldcl.host import Host
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.utils.utils import run_multiple, check_version

class JuniperSystem(System):
    """
    Class Node to create JunOS node objects.
    """

    def __init__(self, system_data, connect_complex_system=False, connect_dual_re=False):
        """

        Base class for JunOS system

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
                # This need to be modified to detect the master node when none of the node has connect set
                if connect_complex_system or system_node == 'primary':
                    system_data['system'][system_node]['connect'] = True
                elif 'connect' not in system_data['system'][system_node].keys():
                    t.log(level="INFO", message="Skipping connection for node " + system_node + "'")
                    continue
            self.controller_connect = self.is_controller_connect_set(system_data['system'][system_node])
            for controller in sorted(list(system_data['system'][system_node]['controllers'].keys())):
                if default_connect or ('connect' in system_data['system'][system_node].keys() and not self.controller_connect):
                    if len(system_data['system'][system_node]['controllers']) == 1:
                        t.log(level="INFO", message="Setting the active RE as'" + controller + "'")
                        system_data['system'][system_node]['controllers'][controller]['connect'] = True
                        break
                    t.log(level="INFO", message="Determining the active RE")
                    try:
                        dev_data = Juniper(**system_data['system'][system_node]['controllers'][controller])
                    except Exception as err:
                        t.log('WARN', message="Failed to determine the "+str(controller)+" beacuse "+str(err))
                        if str(sorted(list(system_data['system'][system_node]['controllers'].keys()))[-1]) != controller:
                            continue
                        else:
                            raise TobyException(str(err))
                    Host._object_counts[system_data['system'][system_node]['controllers'][controller]['hostname']] -= 1
                    if dev_data.is_master():
                        t.log(level="INFO", message="Setting the active RE as'" + controller + "'")
                        system_data['system'][system_node]['controllers'][controller]['connect'] = True
                        dev_data.close()
                        break
                    else:
                        print("Skipping connection for controller" + controller)

        super(JuniperSystem, self).__init__(system_data)

    def cli(self, **kwargs):
        """
            Execute cli command on device

            device_object.cli(command = 'show version detail | no-more', channel = 'text')
        """
        return_value = self.current_node.current_controller.cli(**kwargs)
        return return_value

    def config(self, **kwargs):
        """
            Execute config command on device

            device_object.config(command_list = ['set services telnet', 'delete services web-management', 'show | compare'])
        """
        return_value = self.current_node.current_controller.config(**kwargs)
        return return_value

    def commit(self, **kwargs):
        """
            Commit config on device

            device_object.commit(comment = 'commit successful', sync = True, detail = True)
        """
        return_value = self.current_node.current_controller.commit(**kwargs)
        return return_value

    def save_config(self, **kwargs):
        """
            Save config on device

            device_object.save_config(file = 'temp_config.conf', source = 'committed')
        """
        return_value = self.current_node.current_controller.save_config(**kwargs)
        return return_value

    def load_config(self, *args, **kwargs):
        """
            Load config on device

            device_object.load_config(['set systen services netconf ssh','set ...', 'set ...'], option='set')
            device_objcet.load_config(local_file='my_config.xml', option='override', timeout=120)
        """
        return_value = self.current_node.current_controller.load_config(*args, **kwargs)
        return return_value

    def get_rpc_equivalent(self, **kwargs):
        """
            get rpc equivalent command for given command

            device_object.get_rpc_equivalent(command = 'get-software-information')
        """
        return_value = self.current_node.current_controller.get_rpc_equivalent(**kwargs)
        return return_value

    def execute_rpc(self, **kwargs):
        """
            Execute rpc command on device

            device_object.execute_rpc(command = '<get-software-information/>')
        """
        return_value = self.current_node.current_controller.execute_rpc(**kwargs)
        return return_value

    def pyez(self, command, **kwargs):
        """
            Execute rpc command on device

            device_object.execute_pyez(command = 'get-software-information')
        """
        return_value = self.current_node.current_controller.pyez(command=command, **kwargs)
        return return_value


    def switch_re_handle(self, **kwargs):
        """
            Switch handle on device

            device_object.switch_re_handle()
        """
        return_value = self.current_node.switch_re_handle(**kwargs)
        return return_value

    def software_install(self, **kwargs):
        """
            Software install handle on device

            device_object.software_install(package =
            '/volume/openconfig/trunk/junos-openconfig-x86-32-0.0.0I20161227_1103_rbu-builder.tgz',
            progress = True)
        """
        release = None
        if 'release' in kwargs:
            release = kwargs.pop('release')
        issu = kwargs.get('issu', False)
        nssu = kwargs.get('nssu', False)
        reboot = kwargs.get('reboot', True)
        internal_call = kwargs.get("parallel", None)
        if internal_call:
            internal_call = False
        else:
            internal_call = True
        controllers_all = kwargs.pop('controllers_all', True)
        kwargs['all_re'] = False
        result_list = []
        if issu is True or nssu is True:
            status = self.current_node.current_controller.software_install(**kwargs)
            t.log(level="INFO", message="software_install status: %s" % status)
            if status:
                self.reconnect(all=True, timeout=1200)
            else:
                raise TobyException('ISSU/NSSU failed.', host_obj=self)
        else:
            if controllers_all:
                for node_name in self.nodes:
                    for controller_name in self.nodes[node_name].controllers.keys():
                        result_list.append( \
                            {"target": self.nodes[node_name].controllers[controller_name].software_install, "delay": 4, "kwargs":kwargs})
                results = run_multiple(targets=result_list, internal_call=internal_call)
                if results.count(True) == len(result_list):
                    t.log(level="INFO", message="software_install status: %s" % result_list)
                    self.set_current_controller(controller='master', system_node='current')
                else:
                    raise TobyException('Software Install failed.', host_obj=self)
            else:
                status = self.current_node.current_controller.software_install(**kwargs)
                if status:
                    if self.vc:
                        self.reconnect(all=True, timeout=1200)
                    t.log(level="INFO", message="software_install status: %s" % status)
                    self.set_current_controller(controller='master', system_node='current')
                else:
                    raise TobyException('Software Install failed.', host_obj=self)
        ## version check
        if release is not None:
            message = "ISSU/NSSU" if (issu or nssu) else "Junos"
            if check_version(device=self, version=release, operator='ge', all=controllers_all):
                t.log(level="INFO", message="%s Version check passed " % message)
            else:
                t.log(level="ERROR", message="Version check Failed")
                raise TobyException('Version check Failed.', host_obj=self)
        return True

    def switch_re_master(self):
        """
            switch to the master re
        """
        is_master = self.current_node.current_controller.is_master()
        if not self.current_node.current_controller.switch_re_master():
            return False
        time.sleep(10)
        if is_master == self.current_node.current_controller.is_master():
            return False
        self.current_node._set_current_controller()
        return True

    def vty(self, command, destination, timeout=None, pattern=None, raw_output=False):
        """
            device_object.vty(command = 'show memory', destination = 'fpc1')
        """
        result = self.current_node.current_controller.vty(command=command, destination=destination, timeout=timeout,
                                                          pattern=pattern, raw_output=raw_output)
        if result is False:
            raise TobyException('vty command execution failed', host_obj=self)
        return result

    def cty(self, command, destination, timeout=None, pattern=None, raw_output=False):
        """
            device_object.cty(command = 'show msp service-sets', destination = 'fpc1')
        """
        result = self.current_node.current_controller.cty(command=command, destination=destination, timeout=timeout,
                                                          pattern=pattern, raw_output=raw_output)
        if result is False:
            raise TobyException('cty command execution failed', host_obj=self)
        return result

    def powercycle(self, timeout=None):
        return self.current_node.current_controller.powercycle(timeout=timeout)

    def detect_core(self, core_path=None, resource=None, command=None):
        """
            Detect cores on the device and return True(if core found) otherwise False.

            device_object.detect_core(resource = 'r0')
        """
        system_core_count = 0
        system_name = ''
        re1_hostname = None

        if resource is not None:
            t.log('name in system: '+ t.get_t(resource=resource, attribute='name'))
            system_name = t.get_t(resource=resource, attribute='name')

        for node in self.nodes:
            if node == 'primary':
                if len(self.nodes[node].controllers.keys()) > 1:
                    re1_hostname = t.get_t(resource=resource, system_node='primary', controller='re1', attribute='hostname', error_on_missing=False)
                    t.log('re1 hostname/IP is : ' + str(re1_hostname))

                if not system_name:
                    system_name = self.nodes[node].current_controller.name
                system_core_count += self.nodes[node].detect_core(core_path=core_path,
                                                                  system_name=system_name, re1_hostname=re1_hostname, command=command)
                break

        if system_core_count:
            t.log(level='WARN', message='Core is found on the device : ' + system_name + ' and its count is ' + str(system_core_count))
            return True
        else:
            t.log('Core is not found on the device : ' + system_name)
            return False

    def save_current_config(self, file):
        """
            Save config file on the device with the <script_name>_id_pid.conf
        """
        for node in self.nodes:
            if node == 'primary':
                self.nodes[node].save_current_config(file=file)
        return True

    def load_saved_config(self, file, config_timeout=None):
        """
            load saved config on the current RE or master RE (in case of dual-re device) from the file (<script_name>_id_pid>)
        """
        # Check if has device is 'vc' or not before detecting master node
        if hasattr(self, 'vc'):
            if self.vc: # pylint: disable=no-member
                master = self.detect_master_node() # pylint: disable=no-member
                self.nodes[master].load_saved_config(file=file, config_timeout=config_timeout)
            # If device is mx system but is not vc
            else:
                self.nodes['primary'].load_saved_config(file=file, config_timeout=config_timeout)
        # For all other non-mx juniper systems
        else:
            for node in self.nodes:
                if node == 'primary':
                    self.nodes[node].load_saved_config(file=file, config_timeout=config_timeout)
        return True

    def load_baseline_config(self, load_config_from, config_timeout=None):
        """
            load baseline config from the default path(/var/tmp/baseline-config.conf) or from the user location
        """
        self.load_saved_config(file=load_config_from, config_timeout=config_timeout)
        # Check if has device is 'vc' or not before detecting master node
        if hasattr(self, 'vc'):
            if self.vc: # pylint: disable=no-member
                master = self.detect_master_node() # pylint: disable=no-member
            # If device is mx system but is not vc
            else:
                master = 'primary'
        # For all other non-mx juniper systems
        else:
            master = 'primary'
        if len(self.nodes[master].controllers.keys()) > 1:
            self.commit(sync=True, timeout=config_timeout)
        else:
            self.commit(timeout=config_timeout)
        return True

    def check_interface_status(self, interfaces):
        """
            This checks the interface status on all the junos resources

            :Returns: True if all the interfaces are UP , else False
        """
        return_value = self.current_node.current_controller._check_interface_status(interfaces=interfaces)
        return return_value

    def is_evo(self):
        """
           Returns the boolean value True/False based on whether the device belongs to
           EVO or not
        """
        return self.current_node.current_controller.is_evo()

    def get_facts(self, attribute=None):
        """
            This API returns facts/device type
                Eg: device_object.current_node.current_controller.get_facts()
            :param attribute
                **OPTIONAL** List of attributes. Ex : ['tvp', 'evo']
            :return: directory if list of attributes passed

        """
        return self.current_node.current_controller.get_facts(attribute=attribute)

    def get_package_architecture(self):
        """
            Get architecture of the package installed on the box.

            device_object.get_package_architecture()
        """
        return_value = self.current_node.current_controller.get_package_architecture()
        return return_value


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

        Returns: True if device is rebooted and reconnection is successful, else an Exception is raised        Example:
            device_object.reboot(all=True, timeout=200)

        Example: device_object.reboot(all=True)

        """
        if mode.upper() == 'CLI' and self.current_node.current_controller.os.upper() != 'JUNOS':
            raise TobyException("Argument 'mode' can be set to CLI only if device is running Junos")

        if self.is_evo() and mode.upper() == 'CLI':
            if all == 'True' or all == 'true':
                evo_version = self.current_node.current_controller.get_version()
                evo_version_num = re.match(r'(\d+.\d).*', evo_version, re.I)
                evo_version_num = evo_version_num.group(1)
                if float(evo_version_num) < 19.4:
                    command = "request system shutdown reboot"
                else:
                    command = "request system reboot"
            else:
                current_controller_name = self.get_current_controller_name()
                command = "request node reboot %s" %(current_controller_name)
            status = self.current_node.current_controller.reboot(wait=wait, mode=mode, device_type=device_type, \
            command_args=command_args, timeout=timeout, interval=interval, command=command)

            if status:
                response = self.reconnect(all=True, timeout=1200)
                if response:
                    self.set_current_controller(controller='master', system_node='current')
                    self.log(level='INFO', message='Reboot successful')
                    return True
                else:
                    return False
            else:
                return False

        else:
            if all == 'True' or all == 'true':
                if self.current_node.current_controller.os.upper() != 'JUNOS':
                    raise TobyException("Argument 'all' can only be used to reboot Junos devices")
                list_of_dicts = []
                for node_name in self.nodes.keys():
                    for controller in self.nodes[node_name].controllers.values():
                        list_of_dicts.append({'fname': controller.reboot, 'kwargs': {'wait':wait, 'mode':mode,
                                                                                     'timeout':timeout,
                                                                                     'device_type':device_type,
                                                                                     'command_args':command_args},
                                              'interval':interval})
                if False in run_multiple(list_of_dicts):
                    raise TobyException("Unable to reboot all REs of device.")
                else:
                    self.set_current_controller(controller='master', system_node='current')
                    return True
            elif self.current_node.current_controller.os.upper() == 'JUNOS':
                return self.current_node.current_controller.reboot(wait=wait, mode=mode, timeout=timeout, interval=interval,device_type=device_type, command_args=command_args)
            else:
                return self.current_node.current_controller.reboot(wait=wait, timeout=timeout, interval=interval)


    def restore_baseline_config(self, remote_path='/var/tmp', timeout=120):
        """
        Save configuration on the device
            device_object.restore_baseline_config(remote_path = '/var/tmp',
            timeout = 120)
        """
        self.current_node.current_controller.restore_baseline_config(remote_path=remote_path, timeout=timeout)

    def save_baseline_config(self, remote_path='/var/tmp', timeout=120):
        """
        Save configuration on the device
            device_object.save_baseline_config(local_path = '/var/tmp',
            timeout = 120)
        """
        self.current_node.current_controller.save_baseline_config(remote_path=remote_path, timeout=timeout)
