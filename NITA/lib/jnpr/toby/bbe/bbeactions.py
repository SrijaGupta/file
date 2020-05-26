"""
BBEActions is the class with all action methods in BBE Engine
It uses other BBE Engines and can be called as python methods
in Testsuites lib Or as keywords in Testsuites robot file.

"""

#import sys
import re
import time
import os
import datetime
#from lxml import etree
#from jnpr.toby.utils.Vars import Vars
from jnpr.toby.engines.config import config
from jnpr.toby.hldcl.device import Device
from jnpr.toby.bbe.bbekeywords import _bbe_issue_deprecated_mesg
#from jnpr.toby.hldcl import device
#from jnpr.toby.init import init
from robot.api import logger

class BBEActions:

    """
    BBEActions is the class with all action methods in BBE Engine
    It uses other BBE Engines and can be called as python methods
    in Testsuites lib Or as keywords in Testsuites robot file.

    """

    def __init__(self):
        pass

    @staticmethod
    def restart_daemons(device=None, daemons=None, skip_daemons=None, restart_method='immediately',
                        wait_between_restarts=10, daemon_process_map=None):

        """
            !!! This keyword will be retired when Toby introduce the Event Engine.
            restart_daemons with Keyword in robot file "Restart Daemons" can be used
            to restart one or more daemons on the device mentioned with argument device.
            The mandatory arguments are device and list of daemons to restart.
            Optionally it can accept the method of restart such as soft, gracefully or immediately.
            By default it used the method immediately.
            Also for some daemons such as routing which can take optional argument for specific
            logical-system name.
            if the daemon is not in the current daemon_process_map, you need to provide the daemon names and its
            daemon_process_map, in this case, the daemons and daemon_process_map is mandatory. and

            Example:
            To restart selective list of daemons, @{daemons_list} :
            Restart Daemons    device=device0  daemons=@{daemons_list}

            To restart all daemons (available in method) by default :
            Restart Daemons    device=device0

            To restart all but few daemons as listed in @{skip_daemons} :
            Restart Daemons    device=device0   skip_daemons=@{skip_daemons}

            To restart few daemons with a specified restart_method and
            time(seconds) to wait between successive restart of daemons :
            Restart Daemons    device=device0   daemons=@{daemons_list}  restart_method=soft  wait_between_restarts=30

            :return: dictionary of name of daemons with new process id after restart
            raise Exception if any daemon is not restarted successfully

        """
        try:
            bbe.bbevar
        except NameError:
            if not daemons and not daemon_process_map:
                raise Exception("please provide dameons and daemon_process_map arguments")
        if device is None:
            logger.console("It needs a valid device handle as argument")
            t.log('ERROR', "restart_daemons needs a valid device handle as argument. None given.")
            raise Exception("Device information not given")

        t.log('Restart Daemons Actions Start')

        device = t.get_handle(resource=device)
        if daemon_process_map is None:
            daemon_process_map = {'dhcp-service': 'jdhcpd',
                                  'interface-control': 'dcd',
                                  'ppp-service': 'jpppd',
                                  'ppp': 'pppd',
                                  'class-of-service': 'cosd',
                                  'routing': 'rpd',
                                  'firewall': 'dfwd',
                                  'pppoe': 'pppoed',
                                  'l2tp-universal-edge': 'jl2tpd',
                                  'general-authentication-service': 'authd',
                                  'dynamic-flow-capture': 'dfcd',
                                  'auto-configuration': 'autoconfd',
                                  'smg-service': 'bbe-smgd',
                                  'statistics-service': 'pfed',
                                  'subscriber-management': 'smid',
                                  'captive-portal-content-delivery': 'cpcdd',
                                  'extensible-subscriber-services': 'essmd',
                                  'database-replication': 'bdbrepd',
                                  'ancpd-service': 'ancpd',
                                  'diameter-service': 'diameterd',
                                  'mobiled': 'mobiled',
                                  'analytics-agent': 'ntf-agent',
                                  'remote-device-management': 'rdmd',
                                  'bbe-stats-service': 'bbe-statsd'}

        if daemons is None:
            daemons = {'dhcp-service', 'interface-control', 'ppp-service', 'class-of-service', 'routing', 'firewall',
                       'pppoe', 'l2tp-universal-edge', 'general-authentication-service', 'dynamic-flow-capture',
                       'auto-configuration', 'smg-service', 'statistics-service', 'subscriber-management',
                       'extensible-subscriber-services', 'database-replication', 'ancpd-service', 'mobiled',
                       'diameter-service', 'analytics-agent', 'remote-device-management', 'bbe-stats-service'}

        if skip_daemons:
            skip_daemons = set(skip_daemons)
            daemons = daemons.difference(skip_daemons)
        else:
            daemons = set(daemons)

        daemon_pid_map = {}

        for daemon in daemons:
            t.log("Restart {0} Begin".format(daemon))
            cmd = ("restart {0} {1}".format(daemon, restart_method))
            if daemon in daemon_process_map:
                process = daemon_process_map[daemon]
            else:
                raise Exception("Unknown daemon {0} restart requested,\
                                 if it is valid, you need to provide the daemons and daemon_process_map".format(daemon))

            process_cmd = ("show system processes extensive")

            resp_obj = device.cli(command=process_cmd)
            resp = resp_obj.response()
            pattern = r"\d+ (?=.*{0})".format(process)
            matches = re.search(pattern, resp, re.M)
            if matches:
                process_id_before_restart = int(matches.group())
            else:
                process_id_before_restart = 0


            resp_obj = device.cli(command=cmd)
            time.sleep(5)

            resp_obj = device.cli(command=process_cmd)
            resp = resp_obj.response()
            pattern = r"\d+ (?=.*{0})".format(process)
            matches = re.search(pattern, resp, re.M)
            if matches:
                process_id_after_restart = int(matches.group())
            else:
                process_id_after_restart = 0

            if restart_method == "soft":
                t.log("{0} Daemon Restarted with method soft - process ID {1}".format(daemon, process_id_after_restart))
            else:

                if process_id_before_restart != process_id_after_restart:
                    t.log("{0} Daemon Restarted Successfully! - Old process Id {1} New process ID {2}"\
                           .format(daemon, process_id_before_restart, process_id_after_restart))
                    daemon_pid_map['daemon'] = process_id_after_restart
                elif process_id_before_restart == 0:
                    t.log("{0} Daemon was not running before calling restart, ignoring the restart!".format(daemon))
                else:
                    raise Exception("{0} Daemon Restart Failed! - Old process Id {1} New process ID {2}"\
                                    .format(daemon, process_id_before_restart, process_id_after_restart))

            time.sleep(float(wait_between_restarts))

        t.log('Restart Daemons Actions End')
        return daemon_pid_map

    @staticmethod
    def gres_by_routing_engine_master_switch(device=None, maximum_wait_for_readiness=1200):

        """
           Gres By Routing Engine Master Switch
           This function is used to initiate a "request chasssis routing-engine master switch"
           on the device supplied as argument.
           It waits for routing engines to be ready for mastership switch and does a graceful
           switch by issuing the request from CLI.

           Example:
           Gres By Routing Engine Master Switch    device=device0

           To override the maximum wait time for checking Gres readiness:
           Gres By Routing Engine Master Switch    device=device0  maximum_wait_for_readiness=300
        :param device
            **REQUIRED** device on which GRES is to be performed
        :param maximum_wait_for_readiness
            **OPTIONAL** defaults to 1200 seconds

        :return: True , if GRES is successful
        raise Exception in case of failure

        """
        print("the BBE keyword gres_by_routing_engine_master_switch is being deprecated, please use switch_re_master")
        if device is None:
            logger.console("It needs a valid device handle as argument")
            t.log('ERROR', "It needs a valid device handle as argument, none given")
            raise Exception("Device information not given")

        device_handle = t.get_handle(resource=device)
        device_re0 = t.get_handle(resource=device, controller='re0')
        device_re1 = t.get_handle(resource=device, controller='re1')
        status = True

        if device_re0.is_master():
            device = device_re0
        else:
            device = device_re1

        t.log('GRES by routing enginer master switch - Start')

        wait_for_readiness = 0
        re_ready_for_master_switch = 0

        cmd = ("request chassis routing-engine master switch check")

        while (re_ready_for_master_switch == 0) and (wait_for_readiness < maximum_wait_for_readiness):
            resp_obj = device.cli(command=cmd)
            resp = resp_obj.response()
            pattern = "Switchover Ready"
            matches = re.search(pattern, resp)
            if matches:
                re_ready_for_master_switch = 1
            else:
                time.sleep(60)
                wait_for_readiness += 60


        if re_ready_for_master_switch == 0:
            raise Exception("Routing Engine is not ready for master switch even after maximum wait of {0} seconds"\
                            .format(maximum_wait_for_readiness))
        else:
            rpc_cmd = '<get-database-replication-summary-information></get-database-replication-summary-information>'
            database_synchronized = 0
            wait_for_readiness = 0
            while (database_synchronized == 0) and (wait_for_readiness < maximum_wait_for_readiness):
                response_obj = device.execute_rpc(command=rpc_cmd)
                leo = response_obj.response()
                if (leo[0].text == 'Enabled') and(leo[3].text == 'Synchronized'):
                    t.log('Database Replication - Database Synchronized')
                    database_synchronized = 1
                else:
                    time.sleep(60)
                    wait_for_readiness += 60

            if database_synchronized == 0:
                raise Exception("Database Replication - Not Synchronized - state {0}".format(leo[3].text))
            else:
                if device_re0.is_master():
                    device = device_re1
                    new_controller = 're1'
                else:
                    device = device_re0
                    new_controller = 're0'

                master_acquire = False
                wait = int(0)
                while not master_acquire:
                    resp = device.cli(command='request chassis routing-engine master acquire no-confirm').response()
                    pattern = 'Not ready for mastership switch'
                    matches = re.search(pattern, resp)
                    if matches:
                        time.sleep(60)
                        wait += 60
                    else:
                        master_acquire = True

                    if wait == 300:
                        master_acquire = True

                t.log("Waiting for new backup to reboot and come up")
                time.sleep(300)
                if device.is_master():
                    t.log("Mastership successfully changed")
                else:
                    t.log("ERROR", "Something went wrong. New master is not up.")
                    status = False
                #device.switch_re_master()

        device_re0.reconnect()
        device_re1.reconnect()

        t.log('GRES by routing enginer master switch - End')

        if status:
            device_handle.set_current_controller(system_node='primary', controller=new_controller)
            return True
        else:
            raise Exception("GRES by master switch Failed!")

    @staticmethod
    def restart_fpc(device=None, slots=None, maximum_wait_for_online=180):
        """This function is deprecated. Please use bbe_restart_fpc."""

        _bbe_issue_deprecated_mesg(BBEActions.restart_fpc.__name__)
        return BBEActions.bbe_restart_fpc(device, slots, maximum_wait_for_online)

    @staticmethod
    def bbe_restart_fpc(device=None, slots=None, maximum_wait_for_online=180):

        """
           Restart FPC Slots list given in argument on device supplied on argument
           It performes " request chassis fpc restart slot <slot_no> " for each
           slots mentioned in the parameter.
           It waits for a default time of 180 seconds for the slots to come back Online
           The maximum wait for online state can be overridden in the argument.

           It verifies final state information
           from 'show chassis fpc' command.

           Example:
           Restart Fpc    device=device0    slots=@{slots_to_restart}
           Restart Fpc    device=device0    slots=@{slot_to_restart}  maximum_wait_for_online=60

           :return: None

        """

        if device is None:
            t.log('ERROR', "It needs a valid device handle as argument for restart of fpc")
            raise Exception("Device information not given for restart of fpc")

        if slots is None:
            t.log('ERROR', "No slots information passed in argument to restart fpc")
            raise Exception("No slots information passed in argument to restart fpc")

        device = t.get_handle(resource=device)

        #Performing all slot Restarts
        state_of_slots = {}
        for slot in slots:
            state_of_slots[slot] = 'Unknown'
            cmd = "show chassis fpc " + str(slot)
            rpc_cmd = device.get_rpc_equivalent(command=cmd)
            response_obj = device.execute_rpc(command=rpc_cmd)
            lxml_etree_obj = response_obj.response()
            slot_state = lxml_etree_obj.findtext('fpc/state')
            if slot_state == 'Online':
                t.log("Slot {0} is online, will be restarted".format(slot))
                cmd = "request chassis fpc restart slot " + str(slot)
                response_obj = device.cli(command=cmd)
                response = response_obj.response()
                if re.search('Restart initiated', response):
                    wait_for_offline = 0
                    slot_offline = 0
                    while (slot_offline == 0) and (wait_for_offline < maximum_wait_for_online):
                        cmd = "show chassis fpc " + str(slot)
                        rpc_cmd = device.get_rpc_equivalent(command=cmd)
                        response_obj = device.execute_rpc(command=rpc_cmd)
                        lxml_etree_obj = response_obj.response()
                        slot_state = lxml_etree_obj.findtext('fpc/state')
                        if slot_state == 'Offline' or slot_state == 'Present':
                            t.log("Slot {0} Restart Inititated".format(slot))
                            slot_offline = 1
                        else:
                            time.sleep(2)
                            wait_for_offline += 2
                    if slot_offline == 0:
                        t.log('ERROR', "Slot {0} is still in state {1}, restart failed".format(slot, slot_state))
                else:
                    t.log('ERROR', "Slot {0} is still in state {1}, restart failed".format(slot, slot_state))
            else:
                t.log('WARN', "Slot {0} is in state {1}, will not be restarted".format(slot, slot_state))


        #Verifying all slots are back Online
        all_slots_online = 0
        wait_for_online = 0

        while (all_slots_online == 0) and (wait_for_online < maximum_wait_for_online):
            all_slots_online = 1
            for slot, state in state_of_slots.items():
                if state != 'Online':
                    cmd = "show chassis fpc " + str(slot)
                    rpc_cmd = device.get_rpc_equivalent(command=cmd)
                    response_obj = device.execute_rpc(command=rpc_cmd)
                    lxml_etree_obj = response_obj.response()
                    slot_state = lxml_etree_obj.findtext('fpc/state')
                    state_of_slots[slot] = slot_state
                    t.log("Slot {0} is in state {1}".format(slot, slot_state))
                    if slot_state != 'Online':
                        all_slots_online = 0
            time.sleep(30)
            wait_for_online += 30

        if all_slots_online:
            t.log("FPC Restarts suceeded and all slots are back online")
        else:
            raise Exception("FPC Restart failed, not all slots are back online")

    @staticmethod
    def login_ppp_subscribers(tag="all"):

        """
        Login PPP Subscribers starts ppp subscribers login for all the emulation handles
        given in argument.
        Example:
        Login PPP Subscribers    tag="pppoescaling1"

        """

        rthandle = t.get_handle(resource='rt0')
        if tag == "all":
            sub_handles = bbe.get_subscriber_handles(protocol='pppoe')
            for ppp_handle in sub_handles:
                rthandle.invoke('pppoe_client_action', handle=ppp_handle.rt_pppox_handle, action="start")

        else:
            sub_handles = bbe.get_subscriber_handles(tag=tag)
            for ppp_handle in sub_handles:
                rthandle.invoke('pppoe_client_action', handle=ppp_handle.rt_pppox_handle, action="start")

        return True


    @staticmethod
    def logout_ppp_subscribers(tag="all"):

        """
        Logout PPP Subscribers stops ppp subscribers for all the emulation handles
        given in argument.

        Example:
        Logout PPP Subscribers    TAG="pppoescaling1"

        """

        rthandle = t.get_handle(resource='rt0')
        if tag == "all":
            sub_handles = bbe.get_subscriber_handles(protocol='pppoe')
            for ppp_handle in sub_handles:
                rthandle.invoke('pppoe_client_action', handle=ppp_handle.rt_pppox_handle, action="stop")

        else:
            sub_handles = bbe.get_subscriber_handles(tag=tag)
            for ppp_handle in sub_handles:
                rthandle.invoke('pppoe_client_action', handle=ppp_handle.rt_pppox_handle, action="stop")

        return True

    @staticmethod
    def collect_debug_information(devices=None):
        """This function is deprecated. Please use bbe_collect_debug_information."""

        _bbe_issue_deprecated_mesg(BBEActions.collect_debug_information.__name__)
        return BBEActions.bbe_collect_debug_information(devices)

    @staticmethod
    def bbe_collect_debug_information(devices=None):
        """
        Collect Debug Information from the device give in argument
        The debug information is collected after testcase run to analyze
        in case of failures.


        """
        try:
            bbe.bbevar
        except NameError:
            raise Exception("This keyword collect_debug_information is for BBE,"
                            " please use toby libs if not working on BBE feature")
        if devices is  None:
            devices = []
            duts = bbe.get_devices(device_tags='dut')
            for dut in duts:
                devices.append(dut.device_id)

        suffix = time.ctime().replace(" ", "_")
        suffix = suffix.replace(":", "_")
        filename = '/var/tmp/logs_{0}.tgz'.format(suffix)

        for device in devices:
            t.log("Collecting Traceoptions and logs on device {0}".format(device))
            device = t.get_handle(resource=device)
            device.su()
            command = 'tar -zcf {0} /var/log'.format(filename)
            device.shell(command=command)

            command = "show shmlog statistics logname all | save /var/tmp/shmlog_statistics_{0}".format(suffix)
            device.cli(command=command)

            command = "show shmlog entries logname all | save /var/tmp/shmlog_entries_{0}".format(suffix)
            device.cli(command=command)

        t.log("Logs are saved in {0}".format(filename))
        t.log("shmlog statistics are saved in /var/tmp/shmlog_statistics_{0}".format(suffix))
        t.log("shmlog entries are saved in /var/tmp/shmlog_entries_{0}".format(suffix))

        return True

    @staticmethod
    def enable_daemon_traceoptions(devices=None, daemons=None, flag='all', level='all', size='100m', files=100):
        """This function is deprecated. Please use bbe_enable_daemon_traceoptions."""

        _bbe_issue_deprecated_mesg(BBEActions.enable_daemon_traceoptions.__name__)
        return BBEActions.bbe_enable_daemon_traceoptions(devices, daemons, flag, level, size, files)

    @staticmethod
    def bbe_enable_daemon_traceoptions(devices=None, daemons=None, flag='all', level='all', size='100m', files=100):
        """
            BBE enable_daemon_traceoptions with Keyword in robot file "BBE Enable Daemon Tracetoptions" can be used
            to enable traceoptions of various daemons to debug during tests.

            :param devices
                **REQUIRED** Name of junos devices as in topology yaml file
                 If not given, it does the configuration of all devices which are dut
                 as per bbevar

            :param daemons
                **REQUIRED** List of daemons for which traceoptions need to be enabled
                If not supplied, it takes user-debug-logs as configured in bbevar

            :param flag
                **REQUIRED** flag value, defaults to 'all'

            :param level
               **REQUIRED** level value, defaults to 'all'

            :param size
               **REQUIRED** size of files, defaults to 100m

            :param files
               **REQUIRED** number of files, defaults to 100

            Example:

            enable_dameon_traceoptions

            enable_daemon_traceoption(devices=['r0', 'r1'])

            enable_daemon_traceoptions(devices=['r0'], daemons=['authd', 'jpppd'])

            enable_daemon_traceoptions(devices=['r0'], daemons=['authd'], flag='configuration')

            enable_daemon_traceoptions(devices=['r0'], daemons=['jpppd'], level='error')

            :return True
            raise Exception if any commit fails
        """

        t.log("Enabling Traceoption on devices")

        try:
            bvar = bbe.bbevar
        except NameError:
            raise Exception("This keyword enable_daemon_traceoptions is for BBE,"
                            " please use toby libs if not working on BBE feature")

        if devices is None:
            devices = []
            duts = bbe.get_devices(device_tags='dut')
            for dut in duts:
                devices.append(dut.device_id)

        if daemons is None:
            daemons = bvar['debug']['user-debug-logs']

        for device in devices:
            t.log("Enabling Traceoptions on device {0}".format(device))

            cmds = []

            if 'ancpd' in daemons:
                cmds.append("set protocols ancp traceoptions file ancpd")
                cmds.append("set protocols ancp traceoptions file size {0}".format(size))
                cmds.append("set protocols ancp traceoptions file files {0}".format(files))
                cmds.append("set protocols ancp traceoptions flag {0}".format(flag))

            if 'authd' in daemons:
                cmds.append("set system processes general-authentication-service traceoptions flag {0}"\
                            .format(flag))
                cmds.append("set system processes general-authentication-service traceoptions file authd")
                cmds.append("set system processes general-authentication-service traceoptions file size {0}"\
                            .format(size))
                cmds.append("set system processes general-authentication-service traceoptions file files {0}"\
                            .format(files))

            if 'autoconfd' in daemons:
                cmds.append("set system auto-configuration traceoptions flag {0}".format(flag))
                cmds.append("set system auto-configuration traceoptions file autoconfd")
                cmds.append("set system auto-configuration traceoptions file size {0}".format(size))
                cmds.append("set system auto-configuration traceoptions file files {0}".format(files))

            if 'bbesmgd' in daemons:
                cmds.append("set system processes smg-service traceoptions flag {0}".format(flag))
                cmds.append("set system processes smg-service traceoptions level {0}".format(level))
                cmds.append("set system processes smg-service traceoptions file autoconfd size {0} files {1}"\
                           .format(size, files))

            if 'chassisd' in daemons:
                cmds.append("set chassis traceoptions count {0} flag {1}".format(files, flag))
                cmds.append("set chassis traceoptions size {0}".format(size))

            if "cosd" in daemons:
                cmds.append("set class-of-service traceoptions flag {0}".format(flag))
                cmds.append("set class-of-service traceoptions file cosd size {0} files {1}".format(size, files))

            if "dcd" in daemons:
                cmds.append("set interfaces traceoptions flag {0}".format(flag))
                cmds.append("set interfaces traceoptions file dcd size {0} files {1}".format(size, files))

            if "dfcd" in daemons:
                cmds.append("set services radius-flow-tap traceoptions file dfcd size {0} files {1}"
                            .format(size, files))

            if "dfwd" in daemons:
                cmds.append("set firewall traceoptions flag {0}".format(flag))
                cmds.append("set firewall traceoptions file dfwd size {0} files {1}".format(size, files))

            if "jdhcpd" in daemons:
                cmds.append("set system processes dhcp-service traceoptions flag {0}".format(flag))
                cmds.append("set system processes dhcp-service traceoptions file jdhcpd size {0} files {1}"\
                            .format(size, files))

            if "jpppd" in daemons:
                cmds.append("set protocols ppp-service traceoptions flag {0}".format(flag))
                cmds.append("set protocols ppp-service traceoptions file jpppd size {0} files {1}".format(size, files))

            if "ksyncd" in daemons:
                cmds.append("set system kernel-replication traceoptions flag {0}".format(flag))
                cmds.append("set system kernel-replication traceoptions file ksyncd size {0} files {1}"\
                            .format(size, files))

            if "jl2tpd" in daemons:
                cmds.append("set services l2tp traceoptions flag {0}".format(flag))
                cmds.append("set services l2tp traceoptions level {0}".format(level))
                cmds.append("set services l2tp traceoptions file jl2tpd")
                cmds.append("set services l2tp traceoptions file size {0}".format(size))
                cmds.append("set services l2tp traceoptions file files {0}".format(files))


            if "lacpd" in daemons:
                cmds.append("set protocols lacp traceoptions flag {0}".format(flag))
                cmds.append("set protocols lacp traceoptions file lacpd size {0} files {1}".format(size, files))

            if "messages" in daemons:
                cmds.append("set system syslog file messages any any")
                cmds.append("set system syslog file messages daemon any")
                cmds.append("set system syslog file messages kernel any")
                cmds.append("set system syslog time-format millisecond")

            if "pfed" in daemons:
                cmds.append("set accounting-options traceoptions flag {0}".format(flag))

            if "pppd" in daemons:
                cmds.append("set protocols ppp traceoptions level {0}".format(level))
                cmds.append("set protocols ppp traceoptions flag {0}".format(flag))
                cmds.append("set protocols ppp traceoptions file pppd size {0} files {1}".format(size, files))

            if "pppoed" in daemons:
                cmds.append("set protocols pppoe traceoptions level {0}".format(level))
                cmds.append("set protocols pppoe traceoptions flag {0}".format(flag))
                cmds.append("set protocols pppoe traceoptions file pppoed size {0} files {1}".format(size, files))

            if "relayd" in daemons:
                cmds.append("set relayd traceoptions flag {0}".format(flag))
                cmds.append("set relayd traceoptions file relayd size {0} files {1}".format(size, files))

            if "rpd" in daemons:
                cmds.append("set routing-options traceoptions flag {0}".format(flag))
                cmds.append("set routing-options traceoptions file rpd size {0} world-readable".format(size))

            if "smid" in daemons:
                cmds.append("set system services subscriber-management traceoptions")
                cmds.append("set system services subscriber-management traceoptions file smid size {0} files {1}"\
                            .format(size, files))
                cmds.append("set system services subscriber-management traceoptions flag {0}".format(flag))
                cmds.append("set system services subscriber-management traceoptions level {0}".format(level))

            if "snmpd" in daemons:
                cmds.append("set snmp traceoptions flag {0}".format(flag))
                cmds.append("set snmp traceoptions file snmpd size {0} files {1}".format(size, files))

            if "vccpd" in daemons:
                cmds.append("set virtual-chassis traceoptions flag {0}".format(flag))
                cmds.append("set virtual-chassis traceoptions file vccpd size {0} files {1}".format(size, files))


            config.config().CONFIG_SET(device_list=[device], cmd_list=cmds, commit=True)

            return True

    @staticmethod
    def collect_debug_event(resource):
        """This function is deprecated. Please use bbe_collect_debug_event."""

        _bbe_issue_deprecated_mesg(BBEActions.collect_debug_event.__name__)
        return BBEActions.bbe_collect_debug_event(resource)

    @staticmethod
    def bbe_collect_debug_event(resource):
        """
        :param resource:    router id e.g. 'r0'
        :return:
        """
        try:
            bbe.bbevar
        except NameError:
            raise Exception("This keyword collect_debug_event is for BBE,"
                            "please use toby libs if not working on BBE feature")
        for node in t.get_resource(resource)['system']:
            if node not in ['primary', 'member1']:
                continue
            for re_name in t.get_resource(resource)['system'][node]['controllers'].keys():
                router = t.get_handle(resource=resource, system_node=node, controller=re_name)
                router.su()
                router.shell(command='echo "debug event statistics show all" > /var/log/debug-event.cmd')
                router.shell(command='echo "debug event show all" >> /var/log/debug-event.cmd')
                router.shell(command='cp /var/log/debug-event.cmd /var/log/jl2tpd.cmd')
                router.shell(command='cp /var/log/debug-event.cmd /var/log/jpppd.cmd')
                router.shell(command='cp /var/log/debug-event.cmd /var/log/pppoed.cmd')
                router.shell(command='cd /var/log')
                router.shell(command='echo " " > /var/log/jl2tpd.dbg')
                router.shell(command='echo "" > /var/log/jl2tpd.sta')
                router.shell(command='echo " " > /var/log/jpppd.dbg')
                router.shell(command='echo "" > /var/log/jpppd.sta')
                router.shell(command='echo " " > /var/log/pppoed.dbg')
                router.shell(command='echo "" > /var/log/pppoed.sta')
                router.shell(command='kill -s USR1 `cat /var/run/jpppd.pid`')
                router.shell(command='kill -s USR1 `cat /var/run/pppoed.pid`')
                router.shell(command='kill -s USR1 `cat /var/run/jl2tpd.pid`')
                resp = router.shell(command='ls -la /var/log/jpppd.dbg')
                orig_size = 0
                new_size = int(re.findall(r'wheel\s+(\d+)\s+', resp.resp)[0])
                while new_size > orig_size:
                    orig_size = new_size
                    time.sleep(3)
                    new_size = int(re.findall(r'wheel\s+(\d+)\s+', resp.resp)[0])
                router.cli(command='show configuration | save /var/log/router.cfg', timeout=1200)
                router.cli(command='show shmlog logs-summary | save /var/log/shmlog_logs_summary', timeout=1200)
                router.cli(command='show shmlog statistics logname all | save /var/log/shmlog_staticstics_logname_all',
                           timeout=1200)
                router.cli(command='show shmlog entries logname all| save /var/log/shmlog_entries_logname_all',
                           timeout=1200)

                router.shell(command='cd /var/log')
                timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                pid = os.getpid()

                # for file in ['jpppd.dbg', 'jpppd.sta' 'jl2tpd.dbg', 'jl2tpd.sta', 'pppoed.dbg',
                #              'pppoed.sta', 'shmlog_logs_summary', 'shmlog_staticstics_logname_all',
                #  'shmlog_entries_logname_all']:
                #     newfile = "{}_DebugEvents_{}_{}".format(timestamp, pid, file)
                #     command = "mv {} {}".format(file, newfile)
                #     router.shell(command=command)

                router.shell(command='cp -r /var/etc /var/log')
                router.shell(command='cd /tmp')
                router.shell(command='rm *.tgz')
                hostname = router.shell(command='hostname').resp
                tarfile = "{}_DebugEvents_{}_{}_varlog.tgz".format(timestamp, pid, hostname)
                command = 'tar cvzf {} /var/log'.format(tarfile)
                router.shell(command=command, timeout=1800)
                t.log("start downloading {} to shell server temporary and then upload to the eabu-sssp".format(tarfile))
                try:
                    remote_file = '/tmp/{}'.format(tarfile)
                    router.download(local_file='/tmp', remote_file=remote_file)
                except Exception as err:
                    t.log('ERROR', "failed to download the file from router with reason {}".format(err))
                    return
                try:
                    ftp_dev = Device(host='eabu-sssp.englab.juniper.net', os='unix', user='regress', password='MaRtInI')
                    ftp_dev.upload(local_file=remote_file, remote_file='/usr/debugEvents')
                # with SCP('eabu-sssp.englab.juniper.net', progress=True, user='regress', password='MaRtInI') as scp2:
                #     try:
                #         scp2.put(remote_file, remote_path='/usr/debugEvents')
                except Exception as err:
                    t.log('ERROR', 'failed to upload files to eabu-sssp server from shell due to {}'.format(err))
                    ftp_dev.close()
                    return
                #os.system('ls -l')
                os.system('rm -f /tmp/{}'.format(tarfile))

                # from subprocess import call
                # call('ls -l')
                # call('rm /tmp/{}'.format(tarfile))
                ftp_dev.close()
                router.shell(command='rm /tmp/*varlog.tgz')
                # router.shell(command='rm -f /var/log/*.dbg')
                # router.shell(command='rm -f /var/log/*.sta')
                router.shell(command='rm -f /var/log/shmlog_*')
                # router.shell(command='rm -f /var/log/*.gz')
                # router.shell(command='rm -f /var/log/*DebugEvents*')
                router.cli(command='clear shmlog all-info logname all')
                for msg in ['message', 'pppoed', 'jdhcpd', 'jl2tpd', 'jpppd', 'authd', 'bbesmgd', 'dfwd', 'chassisd',
                            'cosd', 'dcd']:
                    command = 'clear log {} all'.format(msg)
                    router.cli(command=command)
