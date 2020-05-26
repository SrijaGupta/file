"""
Class for Qfxsystem
"""
import re
from jnpr.toby.hldcl.juniper.junipersystem import JuniperSystem
import time
class QfxSystem(JuniperSystem):
    """
    Class System to create JunOS Qfx System object.
    """
    def __init__(self, system_data):
        """

        Base class for JunOS Qfx system

        :param nodedict:
            **REQUIRED** systemdict of node
        :return: Qfx system object
        """
        self.vc = False  # pylint: disable=invalid-name
        if system_data is not None and len(system_data['system'].keys()) > 1:
            for node in system_data['system'].keys():
                if re.search(r'member(\d+)', node):
                    self.vc = True
                    break

        super(QfxSystem, self).__init__(system_data)
        self.cc = self.current_node.current_controller # pylint: disable=invalid-name
        t.log(level='INFO', message="QFC VC %s " % self.vc)
    def reboot(self, wait=0, mode='shell', timeout=None, interval=20, all=False, device_type=None, system_nodes=None, command_args=None):
        """
        Reboot Junos device
            device_object.reboot()

        :param wait:
            *OPTIONAL* Time to sleep before reconnecting, Default value is 0

        :param mode:
            *OPTIONAL* Mode in which reboot needs to be executed. Default is
            'shell'. Also supports 'cli'.
            mode=cli is valid only for Junos devices.

        :param timeout:
            *OPTIONAL* Time to reboot and connect to device.
            Default is set based on os/platform/model of the box.

        :param interval:
            *OPTIONAL* Interval at which reconnect need to be attempted
            after reboot is performed. Default is 20 seconds

        :param device_type:
            *OPTIONAL* This option works only with 'text' channel.
            Value should be set to 'vmhost' to reboot the vmhost

        :Returns:
            True if device is rebooted and reconnection is successful,
            else an Exception is raised
        """
        # Make command_args a list if nothing is passed in
        if command_args == None:
            command_args = []
        member_verify = False
        reboot_local = False
        #Check for all-members
        if system_nodes == 'all-members':
            command_args.append('all-members')
            all = False
        #Check for local
        if system_nodes == 'local':
            command_args.append('local')
            reboot_local = True
            all = False

        #Here user can pass input as member1 ,member2...member n
        #Extract digit from user input and pass member 1 to reboot

        if system_nodes:
            res = re.search(r'(member)(\d+)', system_nodes)
            if res:
                command_args.append('member')
                command_args.append(res.group(2))
                member_node = res.group(2)
                member_verify = True

        # This gets rid of any duplicates between system_nodes & command_args and maintains the list in same order
        command_args_set = set()
        command_args = [cmd_elmnt for cmd_elmnt in command_args if not (cmd_elmnt in command_args_set or command_args_set.add(cmd_elmnt))]

        cmd = 'request system reboot'

        patterns = [r'[Rr]eboot the vmhost \? \[yes,no\] \(no\)[\s]?',
                    r'[Rr]eboot the system \? \[yes,',
                    r'System going down|Shutdown NOW',
                    r'(?is)connection (to \S+ )?closed.*',
                    r'>']

        if command_args:
            if len(command_args) > 1:
                cmd = cmd + " " + " ".join(command_args)
            else:
                cmd = cmd + " " + command_args[0]

        try:
            if member_verify:
                if mode.upper() == 'CLI':
                    self.cli(command=cmd, pattern=[r'yes.no.*'])
                    self.log(level='info', message='command: yes')
                    # Console connection does not have PyEZ channel
                    # so must send commands manually
                    if 'console' in self.cc.controllers_data.get('connect_targets', 'management'):
                        self.cc.channels['text'].write(b'yes\r\n')
                    else:
                        self.cc.execute(command='yes', pattern=patterns)
                    self.cli(command="show virtual-chassis status ")

                    member_poll_time = 120
                    member_incr_time = 0
                    member_up = False
                    while member_incr_time <= member_poll_time:
                        self.cli(command="show virtual-chassis status ")
                        self.log(level='INFO', message='sleeping for 10 secs interval')
                        member_incr_time = member_incr_time + 10
                        time.sleep(10)
                        match_key = "FPC %s" % member_node
                        cli_resp = self.cli(command="show virtual-chassis status | match " + "\"" + match_key + "\"").response()
                        self.cli(command="show virtual-chassis status ")
                        rs = re.search(r'NotPrsnt', cli_resp)
                        if rs:
                            self.log(level='INFO', message='FPC %s is in Not Prsnt state' %member_node)
                        else:
                            self.log(level='INFO', message='FPC %s is in Prsnt state' % member_node)
                            member_up = True
                            break

                    self.log(level='info', message='cli response is %s' % cli_resp)
                    if member_up:
                        self.log(level='INFO', message='Reboot member successful')
                        response = True
                        return response
                    else:
                        self.log(level='ERROR', message='Reboot member failed')
                        response = False
                        return response
            else:
                if self.vc and reboot_local:
                    result = self.cc.reboot(wait=wait, mode=mode, timeout=timeout, interval=interval,
                                            device_type=device_type, command_args=command_args, ping=False)
                else:
                    result = self.cc.reboot(wait=wait, mode=mode, timeout=timeout, interval=interval,
                                            device_type=device_type, command_args=command_args)
                if result:
                    self.log(level="INFO", message="Reboot has passed")
                    return True
                else:
                    self.log(level="ERROR", message="Failed to reboot the device")
                    return False
        except Exception as exp:
            self.log(level='ERROR', message=exp)
        return False

    def software_install(self, **kwargs):
        """
            Software install handle on device

            device_object.software_install(package =
            '/volume/openconfig/trunk/junos-openconfig-x86-32-0.0.0I20161227_1103_rbu-builder.tgz',
            progress = True)
        """
        kwargs['save_restore_baseline'] = True
        super(QfxSystem, self).software_install(**kwargs)

    def detect_master_node(self):
        """

        :return:
        """
        master = 'primary'
        return master
