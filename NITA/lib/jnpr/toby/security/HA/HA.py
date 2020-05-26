"""
Copyright (C) 2016-2017, Juniper Networks, Inc.
All rights reserved.
Author: Michael Zhou, mzhou@juniper.net
Description: HA keywords
"""
import time
import re
import copy

# pylint: disable=invalid-name
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-locals

class HA(object):
    """HA keywords for SRX, tested on SRX5K

    * check_via_xpath
    * check_fpc_pic
    * do_manual_failover
    * do_ip_monitoring_failover
    * do_interface_monitor_failover
    * do_reboot_failover
    * do_preempt_failover
    * execute_cli_on_node
    * execute_shell_on_node
    * get_ha_node_name
    * get_ha_node_status
    * get_ha_healthy_status
    * get_ha_status
    * get_ha_rgs
    * reboot_node

    """
    def _quote(self, word):
        """add double quotes for a word
        """
        return '"' + word + '"'

    def _space(self, operator):
        """add space for an operator
        """
        return ' ' + operator + ' '

    def __init__(self, device=None):
        """HA constructor
        user can either pass the device handle when calling constructor
        or pass it when calling specified method
        """
        self.device = device
        self.interval_1 = 15
        self.retry_1 = 3
        self.interval_2 = 60
        self.retry_2 = 20
        self.interval_3 = 120
        self.retry_3 = 40
        self.config_timeout = 300
        self.commit_timeout = 300

    def check_fpc_pic(self, device=None, **kwargs):
        """check fpc pic-status

        :param Device device:
            **REQUIRED** Device handle
        :param int retry:
            **OPTIONAL** how many times to retry, default is 10
        :param int interval:
            **OPTIONAL** retry interval, default is 30 seconds

        :return: True or False

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.check_fpc_pic(device=r0, retry=3, interval=15)

        robot::

            ${r0}    get handle    resource=r0
            ${rt}    check fpc pic    device=${r0}   retry=3    interval=15
            should be true    ${rt}

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        retry = int(kwargs.get("retry", self.retry_2))
        interval = int(kwargs.get("interval", self.interval_2))
        check_criteria = [
            {'xpath':".//fpc/state", 'operator':"==", 'expect':"Online"},
            {'xpath':".//fpc/pic/pic-state", 'operator':"==", 'expect':"Online"}
        ]
        index = 1
        while index <= retry:
            if not self.check_via_xpath(device, command="show chassis fpc pic-status", check_criteria=check_criteria): # pylint: disable=line-too-long
                device.log(level="INFO", message=str(index) + " - Wait "+ str(interval) +" seconds and retry...") # pylint: disable=line-too-long
                index += 1
                time.sleep(interval)
            else:
                break
        else:
            device.log(level="ERROR", message="fpc pic-status are not online")
            return False
        device.log(level="INFO", message="fpc pic-status are online")
        return True

    def check_via_xpath(self, device=None, **kwargs):
        """check destination fields through xpath

        :param Device device:
            **REQUIRED** Device handle
        :param str command:
            **REQUIRED** check the output of this command
        :param list check_criteria:
            **REQUIRED** a list which has dict as the check_criteria

        :return: True or False

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            criteria = [
                {'xpath':".//redundancy-group-status",'operator':"==",'expect':"primary|secondary"},
                {'xpath':".//device-priority",'operator':"!=",'expect':0}
            ]
            ha.check_via_xpath(device=r0, command="show chassis cluster status", check_criteria=criteria)

        robot::

            ${r0}    get handle    resource=r0
            ${cmd}    set variable    show chassis cluster status
            ${criteria_1}    create dictionary
            ...              xpath=.//redundancy-group-status
            ...              operator===
            ...              expect=primary|secondary
            ${criteria_2}    create dictionary
            ...              xpath=.//device-priority
            ...              operator=!=
            ...              expect=0
            ${criteria}    create list
            ...            ${criteria_1}
            ...            ${criteria_2}
            ${rt}    check via xpath    device=${r0}   command=${cmd}    check_criteria=${criteria}
            should be true    ${rt}

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        command = kwargs.get("command")
        check_criteria = kwargs.get("check_criteria")

        rpc_cmd = device.get_rpc_equivalent(command=command)
        output_element = device.execute_rpc(command=rpc_cmd).response()
        result_dict = {}
        for criteria in check_criteria:
            xpath = criteria.get("xpath")
            expect = criteria.get("expect")
            operator = criteria.get("operator")
            expect_str = self._space(operator) + str(expect)
            elements = output_element.xpath(xpath)
            got_values = [x.text for x in elements]
            if got_values != []:
                results = []
                for value in got_values:
                    if re.search(r"\|", expect):
                        multi_values = expect.split("|")
                        first = multi_values.pop(0)
                        # judge the type of int or str based on first item
                        if re.match(r"^\d+$", str(first)):
                            expr = str(value) + self._space(operator) + str(first)
                            for item in multi_values:
                                expr += ' or ' + str(value) + self._space(operator) + str(item)
                        else:
                            expr = self._quote(str(value))  + self._space(operator) + self._quote(first) # pylint: disable=line-too-long
                            for item in multi_values:
                                expr += ' or ' + self._quote(str(value)) + self._space(operator) + self._quote(item) # pylint: disable=line-too-long
                    else:
                        if re.match(r"^\d+$", str(expect)):
                            expr = str(value) + self._space(operator) + str(expect)
                        else:
                            expr = self._quote(str(value))  + self._space(operator) + self._quote(expect) # pylint: disable=line-too-long
                    # pylint: disable=eval-used
                    results.append(eval(expr))
                result_dict[xpath] = [results, got_values, expect_str]
            else:
                device.log(level="INFO", message="Cannot get values via xpath: " + str(xpath))
                result_dict[xpath] = [[False], "Cannot get values via xpath", expect_str]
        error = 0
        for key, value in result_dict.items():
            failed = value[0].count(False)
            info = "xpath: " + str(key) + ", Got: " + str(value[1]) + ", Expect: " + str(value[2])
            if failed == 0:
                device.log(level="INFO", message="xpath checking passed! " + info)
            else:
                device.log(level="INFO", message="xpath checking failed! " + info)
                error += 1
        if error == 0:
            device.log(level="INFO", message="All xpath checking passed")
            return True
        else:
            device.log(level="INFO", message=str(error) + " xpath checking failed")
            return False

    def do_manual_failover(self, device=None, **kwargs):
        """do manual failover
        use command "request chassis cluster failover..." to do failover

        :param Device device:
            **REQUIRED** Device handle
        :param str rg:
            *OPTIONAL* Redundancy-Group(0..128) Ex. rg="0". Default: 0
        :param str node:
            *OPTIONAL* Node which needs to be made primary. "0" or "1" Ex. node="0". Default: Performs a failover
        :param Boolean force:
            *OPTIONAL* Whether do force failover. Default: False
        :param int timeout:
            *OPTIONAL* Wait a while for rg failover, and then checking whether failover succeed.
        :param int check_cnt:
            *OPTIONAL* Another solution of "timeout". With option "check_interval" to do loop checking.
                       Default: If rg=0, check_cnt=5; otherwise (1..128) check_cnt=2
        :param int check_interval:
            *OPTIONAL* With option "check_cnt" to do loop checking.
                       Default: If rg=0, check_interval=60; otherwise (1..128) check_interval=10

        :returns: True or False

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA(r0)
            ## Examples, only one is needed in your code
            ha.do_manual_failover(rg="1")
            # wait 30 seconds before checking HA status, no retrying after that
            ha.do_manual_failover(rg="1", timeout=30)
            # check HA status every 10 seconds, retrying 3 times if needed
            ha.do_manual_failover(rg="1", check_cnt=3, check_interval=10)

        robot::

            ${r0}    get handle    resource=r0
            ## Examples, only one is needed in your code
            ${result}    do manual failover    device=${r0}    rg=1
            # values of check_cnt and check_interval will be converted to int and float from string
            # so do not need use them as ${Number} in robot
            ${result}    do manual failover    device=${r0}    rg=1    check_cnt=3    check_interval=10
            should be true    ${result}

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        device.log(level="INFO", message="Start manual failover")
        return device.failover(**kwargs)

    def do_ip_monitoring_failover(self, device=None, **kwargs):
        """do ip-monitoring failover
        simulate route disconnect via disabling the related physical interfaces

        :param Device device:
            **REQUIRED** Device handle
        :param str rg:
            **REQUIRED** HA redundance-group
        :param str ip_address:
            **REQUIRED** ip-monitoring ip address
        :param str interface:
            **REQUIRED** interface which ping go through
        :param str secondary_ip_address:
            **REQUIRED** secondary-ip-address when doing ping
        :param str weight:
            *OPTIONAL* ip-monitoring weight, default 255
        :param str family:
            *OPTIONAL* inet or inet6
        :param str global_weight:
            *OPTIONAL* ip-monitoring global-weight, default 255
        :param str retry_interval:
            *OPTIONAL* ip-monitoring retry-interval, default 1
        :param str retry_count:
            *OPTIONAL* ip-monitoring retry-count, default 15

        :returns: True or False

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.do_ip_monitoring_failover(device=r0, rg="1",
                ip_address="115.0.0.25",
                secondary_ip_address="115.0.0.11",
                interface="reth0"
            )

        robot::

            ${r0}    get handle    resource=r0
            ${result}    do ip monitoring failover    device=${r0}    rg=1
            ...          ip_address=115.0.0.25
            ...          secondary_ip_address=115.0.0.11
            ...          interface=reth0
            should be true    ${result}

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        rg = kwargs.get("rg", "1")
        family = kwargs.get("family", "inet")
        global_weight = kwargs.get("global_weight", "255")
        retry_interval = kwargs.get("retry_interval", "1")
        retry_count = kwargs.get("retry_count", "15")
        ip_address = kwargs.get("ip_address")
        weight = kwargs.get("weight", "255")
        interface = kwargs.get("interface")
        if not re.search(r"^reth\d+$", interface):
            device.log(level="ERROR", message="Wrong interface format, should be reth0,...")
            return False
        secondary_ip_address = kwargs.get("secondary_ip_address")
        cmd_1 = "show configuration chassis cluster redundancy-group {} ip-monitoring".format(rg)
        cmd_2 = 'show configuration |display set |match "redundant-parent {}"'.format(interface)
        cmd_3 = "show configuration chassis cluster redundancy-group {} interface-monitor".format(rg) # pylint: disable=line-too-long
        delete_cmds = ["delete chassis cluster redundancy-group {} ip-monitoring".format(rg)]
        config_cmds = [
            # pylint: disable=line-too-long
            "set chassis cluster redundancy-group {} ip-monitoring global-weight {}".format(rg, global_weight),
            "set chassis cluster redundancy-group {} ip-monitoring retry-interval {}".format(rg, retry_interval),
            "set chassis cluster redundancy-group {} ip-monitoring retry-count {}".format(rg, retry_count),
            "set chassis cluster redundancy-group {} ip-monitoring family {} {} weight {}".format(rg, family, ip_address, weight),
            "set chassis cluster redundancy-group {} ip-monitoring family {} {} interface {} secondary-ip-address {}".format(rg, family, ip_address, interface, secondary_ip_address),
        ]
        ## check the HA status before failover
        status_1 = self.get_ha_healthy_status(device=device, rg=rg, retry=2, interval=15)
        if status_1 is False:
            device.log(level="ERROR", message="RG{} is in abnormal status before failover".format(rg))
            return False
        status_after_failover = copy.deepcopy(status_1)
        status_after_recover = copy.deepcopy(status_1)
        status_after_failover['node0']['status'], status_after_failover['node1']['status'] = \
            status_1['node1']['status'], status_1['node0']['status']
        status_after_recover['node0']['status'], status_after_recover['node1']['status'] = \
            status_1['node1']['status'], status_1['node0']['status']
        if status_1['node0']['status'] == "primary":
            status_after_failover['node0']['priority'] = "0"
            status_after_failover['node0']['monitor-failures'] = "IP"
        else:
            status_after_failover['node1']['priority'] = "0"
            status_after_failover['node1']['monitor-failures'] = "IP"
        ## delete preempt if it's enabled for specified rg
        if status_1['node0']['preempt'] == 'yes':
            config_cmds.append(
                "delete chassis cluster redundancy-group {} preempt".format(rg))
            status_after_failover['node0']['preempt'] = "no"
            status_after_failover['node1']['preempt'] = "no"
            status_after_recover['node0']['preempt'] = "no"
            status_after_recover['node1']['preempt'] = "no"
        ## delete interface-monitor if it's configured
        intf_monitor_cfg = device.cli(command=cmd_3).response()
        if not intf_monitor_cfg == '\r':
            config_cmds.append(
                "delete chassis cluster redundancy-group {} interface-monitor".format(rg))
        ## check ip-monitoring if it's already configured
        ip_monitor_cfg = device.cli(command=cmd_1).response()
        if not ip_monitor_cfg == '\r':
            device.config(command_list=delete_cmds, timeout=self.config_timeout)
            device.commit(timeout=self.commit_timeout)

        # configure ip-monitoring and delete preempt/interface-monitor
        device.config(command_list=config_cmds, timeout=self.config_timeout)
        device.commit(timeout=self.commit_timeout)

        reth_cfg = device.cli(command=cmd_2).response()
        reth_cfg_list = reth_cfg.split("\r\n")[:-1]
        if len(reth_cfg_list)%2 == 0:
            physical_interfaces = [x.split()[2] for x in reth_cfg_list]
            pivot = int(len(physical_interfaces)/2)
            if status_1['node0']['status'] == 'primary':
                disable_interface = physical_interfaces[:pivot]
            else:
                disable_interface = physical_interfaces[pivot:]
            disable_cmds = ["set interfaces {} disable".format(x) for x in disable_interface]
            enable_cmds = ["delete interfaces {} disable".format(x) for x in disable_interface]
        else:
            device.log(level="ERROR", message="get odd number of physical interface number")
            return False
        ## disconnect the routes
        device.config(command_list=disable_cmds, timeout=self.config_timeout)
        device.commit(timeout=self.commit_timeout)
        ## check the HA status after route is disconnected
        status_2 = self.get_ha_healthy_status(
            device=device, rg=rg, retry=self.retry_2, interval=self.interval_2, priority_zero=True)
        if status_2 is False:
            device.log(level="ERROR", message="RG{} status is abnormal after failover".format(rg))
            return False
        else:
            if status_2 == status_after_failover:
                device.log(level="INFO", message="RG{} ip-monitoring failover succeed".format(rg))
            else:
                device.log(level="ERROR", message="RG{} status is not expected after failover".format(rg))
                device.log(level="ERROR", message=self.get_ha_status(device=device, rg=rg, cc_status=status_2))
                return False
        ## recover the route
        device.config(command_list=enable_cmds, timeout=self.config_timeout)
        device.commit(timeout=self.commit_timeout)
        ## check the HA status after route is recovered
        status_3 = self.get_ha_healthy_status(
            device=device, rg=rg, retry=self.retry_1, interval=self.interval_1, priority_zero=True)
        ## delete ip-monitoring config before returning
        device.config(command_list=delete_cmds, timeout=self.config_timeout)
        device.commit(timeout=self.commit_timeout)
        if status_3 is False:
            device.log(level="ERROR", message="RG{} status is abnormal after failover".format(rg))
            return False
        else:
            if status_3 == status_after_recover:
                device.log(level="INFO", message="RG{} ip-monitoring recovering succeed".format(rg))
            else:
                device.log(level="ERROR", message="RG{} ip-monitoring recovering failed".format(rg))
                device.log(level="ERROR", message=self.get_ha_status(device=device, rg=rg, cc_status=status_3))
                return False
        return True

    def do_interface_monitor_failover(self, device=None, **kwargs):
        """do interface-monitor failover
        disable related physical interface to trigger this failover

        :param Device device:
            **REQUIRED** Device handle
        :param str rg:
            **REQUIRED** HA redundance-group
        :param str interface:
            **REQUIRED** interface to be monitored, such as, reth0
        :param str weight:
            *OPTIONAL* interface-monitor weight, default 255

        :returns: True or False

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.do_interface_monitor_failover(device=r0, rg="1", interface="reth0")

        robot::

            ${r0}    get handle    resource=r0
            ${result}    do interface monitor failover    device=${r0}    rg=1    interface=reth0
            should be true    ${result}

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        rg = kwargs.get("rg", "1")
        interface = kwargs.get("interface")
        if not re.search(r"^reth\d+$", interface):
            device.log(level="ERROR", message="Wrong interface format, should be reth0,...")
            return False
        weight = kwargs.get("weight", "255")
        cmd_1 = "show configuration chassis cluster redundancy-group {} interface-monitor".format(rg) # pylint: disable=line-too-long
        cmd_2 = 'show configuration |display set |match "redundant-parent {}"'.format(interface)
        cmd_3 = "show configuration chassis cluster redundancy-group {} ip-monitoring".format(rg) # pylint: disable=line-too-long
        delete_cmds = ["delete chassis cluster redundancy-group {} interface-monitor".format(rg)]

        ## check the HA status before failover
        status_1 = self.get_ha_healthy_status(device=device, rg=rg, retry=2, interval=15)
        if status_1 is False:
            device.log(level="ERROR", message="RG{} is in abnormal status before failover".format(rg))
            return False
        status_after_failover = copy.deepcopy(status_1)
        status_after_recover = copy.deepcopy(status_1)
        status_after_failover['node0']['status'], status_after_failover['node1']['status'] = \
            status_1['node1']['status'], status_1['node0']['status']
        status_after_recover['node0']['status'], status_after_recover['node1']['status'] = \
            status_1['node1']['status'], status_1['node0']['status']
        if status_1['node0']['status'] == "primary":
            status_after_failover['node0']['priority'] = "0"
            status_after_failover['node0']['monitor-failures'] = "IF"
        else:
            status_after_failover['node1']['priority'] = "0"
            status_after_failover['node1']['monitor-failures'] = "IF"

        # retrieve the physical interfaces, cli output is a str with line separator "\r\n"
        reth_cfg = device.cli(command=cmd_2).response()
        reth_cfg_list = reth_cfg.split("\r\n")[:-1]
        if len(reth_cfg_list)%2 == 0:
            physical_interfaces = [x.split()[2] for x in reth_cfg_list]
            pivot = int(len(physical_interfaces)/2)
            if status_1['node0']['status'] == 'primary':
                disable_interface = physical_interfaces[:pivot]
            else:
                disable_interface = physical_interfaces[pivot:]
            interface_monitor_cmds = [
                "set chassis cluster redundancy-group {} interface-monitor {} weight {}"
                .format(rg, x, weight) for x in physical_interfaces
            ]
            disable_cmds = ["set interfaces {} disable".format(x) for x in disable_interface]
            enable_cmds = ["delete interfaces {} disable".format(x) for x in disable_interface]
        else:
            device.log(level="ERROR", message="get odd number of physical interface number")
            return False

        ## check the interface-monitor config, delete them if existing
        intf_cfg = device.cli(command=cmd_1).response()
        if not intf_cfg == '\r':
            device.config(command_list=delete_cmds, timeout=self.config_timeout)
            device.commit(timeout=self.commit_timeout)
        ## disable preempt if it's enabled
        if status_1['node0']['preempt'] == 'yes' or status_1['node1']['preempt'] == 'yes':
            interface_monitor_cmds.append(
                "delete chassis cluster redundancy-group {} preempt".format(rg))
            status_after_failover['node0']['preempt'] = "no"
            status_after_failover['node1']['preempt'] = "no"
            status_after_recover['node0']['preempt'] = "no"
            status_after_recover['node1']['preempt'] = "no"
        ## check the ip-monitoring config, delete them if existing
        ip_monitor_cfg = device.cli(command=cmd_3).response()
        if not ip_monitor_cfg == '\r':
            interface_monitor_cmds.append(
                "delete chassis cluster redundancy-group {} ip-monitoring".format(rg))

        ## change the config to trigger failover
        cmds = interface_monitor_cmds + disable_cmds
        device.config(command_list=cmds, timeout=self.config_timeout)
        device.commit(timeout=self.commit_timeout)

        ## check the HA status after physical interfaces are disabled
        status_2 = self.get_ha_healthy_status(
            device=device, rg=rg, retry=self.retry_2, interval=self.interval_2, priority_zero=True)
        if status_2 is False:
            device.log(level="ERROR", message="RG{} status is abnormal after failover".format(rg))
            return False
        else:
            if status_2 == status_after_failover:
                device.log(level="INFO", message="RG{} interface-monitoring failover succeed".format(rg))
            else:
                device.log(level="ERROR", message="RG{} status is not expected after failover".format(rg))
                device.log(level="ERROR", message=self.get_ha_status(device=device, rg=rg, cc_status=status_2))
                return False

        ## enable the physical interfaces again
        device.config(command_list=enable_cmds, timeout=self.config_timeout)
        device.commit(timeout=self.commit_timeout)

        ## check the HA status after physical interfaces are up
        status_3 = self.get_ha_healthy_status(
            device=device, rg=rg, retry=self.retry_1, interval=self.interval_1, priority_zero=True)
        ## delete interface-monitor config before returning
        device.config(command_list=delete_cmds, timeout=self.config_timeout)
        device.commit(timeout=self.commit_timeout)
        if status_3 is False:
            device.log(level="ERROR", message="RG{} status is abnormal after failover".format(rg))
            return False
        else:
            if status_3 == status_after_recover:
                device.log(level="INFO", message="RG{} interface-monitor recovering succeed".format(rg))
            else:
                device.log(level="ERROR", message="RG{} interface-monitor recovering failed".format(rg))
                device.log(level="ERROR", message=self.get_ha_status(device=device, rg=rg, cc_status=status_3))
                return False
        return True

    def do_reboot_failover(self, device=None, **kwargs):
        """reboot primary node to do failover with CLI "request system reboot"

        :param Device device:
            **REQUIRED** Device handle
        :param str rg:
            *OPTIOAL* HA redundance-group, default is 0
        :param int wait:
            *OPTIONAL* Time to sleep before reconnecting, Default value is 60
        :param int interval:
            *OPTIONAL* Interval at which reconnect need to be attempted after reboot is performed.
            Default is 20 seconds
        :param int timeout:
            *OPTIONAL* Time to reboot and connect to device. Default is 360 seconds

        :returns: True or False

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ## Examples, only one is needed in your code
            # do reboot failover for RG1 using default arguments
            # wait 60 seconds then trying to connect every 20 seconds, declare it as down after 360 seconds
            ha.do_reboot_failover(device=r0, rg="1")
            # do reboot failover for RG1 using specified arguments
            # wait 90 seconds then trying to connect every 15 seconds, declare it as down after 420 seconds
            ha.do_reboot_failover(device=r0, rg="1", wait=90, interval=15, timeout=420)

        robot::

            ${r0}    get handle    resource=r0
            ## Examples, only one is needed in your code
            ${result}    do reboot failover    device=${r0}    rg=1
            # values of wait, interval and timeout will be converted to int from string in python
            ${result}    do reboot failover    device=${r0}    rg=1    wait=90    interval=15    timeout=420
            should be true    ${result}

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        rg = str(kwargs.get("rg", "0"))
        wait = int(kwargs.get("wait", 60))
        interval = int(kwargs.get("interval", 20))
        timeout = int(kwargs.get("timeout", 360))

        ## check the specified rg status before failover
        status_1 = self.get_ha_healthy_status(device=device, rg=rg, retry=2, interval=15)
        if status_1 is False:
            device.log(level="ERROR", message="RG{} is in abnormal status before failover".format(rg))
            return False
        if status_1['node0']['status'] == "primary":
            original_primary = "node0"
        else:
            original_primary = "node1"
        status_after_failover = copy.deepcopy(status_1)
        status_after_failover['node0']['status'], status_after_failover['node1']['status'] = \
            status_1['node1']['status'], status_1['node0']['status']

        ## check other rgs, remove preempt or failover to align with specified rg
        all_rgs = self.get_ha_rgs(device=device)
        if all_rgs is not False:
            rgs = copy.deepcopy(all_rgs)
            rgs.remove(rg)
        else:
            device.log(level="ERROR", message="Cannot get HA RGs list")
            return False
        disable_preempt = []
        to_be_failover = []
        status_after_reboot = {}
        ## disable preempt if it's enabled for specified rg
        if status_1['node0']['preempt'] == 'yes':
            disable_preempt.append("delete chassis cluster redundancy-group {} preempt".format(rg)) # pylint: disable=line-too-long
            status_1['node0']['preempt'] = "no"
            status_1['node1']['preempt'] = "no"
        for item in rgs:
            status = self.get_ha_healthy_status(device=device, rg=item, retry=2, interval=15)
            if status is False:
                device.log(level="ERROR", message="RG{} is in abnormal status before failover".format(item))
                return False
            ## disable preempt if it's enabled
            if (status['node0']['preempt'] == 'yes' or
                    status['node1']['preempt'] == 'yes'):
                disable_preempt.append("delete chassis cluster redundancy-group {} preempt".format(item)) # pylint: disable=line-too-long
                status['node0']['preempt'] = "no"
                status['node1']['preempt'] = "no"
            status_after_reboot[item] = copy.deepcopy(status)
            if not (status['node0']['status'] == status_1['node0']['status'] and
                    status['node1']['status'] == status_1['node1']['status']):
                to_be_failover.append(item)
            else:
                status_after_reboot[item]['node0']['status'], status_after_reboot[item]['node1']['status'] = \
                    status['node1']['status'], status['node0']['status']

        if len(disable_preempt) != 0:
            device.config(command_list=disable_preempt, timeout=self.config_timeout)
            device.commit(timeout=self.commit_timeout)
        if len(to_be_failover) != 0:
            for item in to_be_failover:
                self.do_manual_failover(device, rg=item)
                time.sleep(60)

        # reboot
        self.reboot_node(device=device, node=original_primary, wait=wait, interval=interval, timeout=timeout)
        device.log(level="INFO", message="wait for HA to come up")

        ## check fpc pic-status after rebooting
        if not self.check_fpc_pic(device=device):
            device.log(level="ERROR", message="fpc pic-status are not online after rebooting")
            return False
        ## check specified rg after rebooting
        status_2 = self.get_ha_healthy_status(device=device, rg=rg, retry=self.retry_3, interval=self.interval_3)
        if status_2 is False:
            device.log(level="ERROR", message="RG{} is in abnormal status after rebooting".format(rg))
            return False
        else:
            if status_2 == status_after_failover:
                device.log(level="INFO", message="failover succeed for rg: " + str(rg))
            else:
                device.log(level="ERROR", message="RG{} status is not expected after rebooting".format(rg))
                device.log(level="ERROR", message=self.get_ha_status(device=device, rg=rg, cc_status=status_2))
                return False
        ## check other rgs after rebooting
        for item in rgs:
            status = self.get_ha_healthy_status(device=device, rg=item, retry=self.retry_3, interval=self.interval_3)
            if status is False:
                device.log(level="ERROR", message="RG{} is in abnormal status after rebooting".format(item))
                return False
            else:
                if status == status_after_reboot[item]:
                    device.log(level="INFO", message="failover succeed for rg: " + str(item))
                else:
                    device.log(level="ERROR", message="RG{} status is not expected after rebooting".format(item))
                    device.log(level="ERROR", message=self.get_ha_status(device=device, rg=rg, cc_status=status))
                    return False
        device.log(level="INFO", message="reboot failover succeed for all rgs")
        return True

    def do_preempt_failover(self, device=None, **kwargs):
        """do preempt failover

        :param Device device:
            **REQUIRED** Device handle
        :param str rg:
            **REQUIRED** HA redundance-group

        :returns: True or False

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.do_preempt_failover(device=r0, rg="1")

        robot::

            ${r0}    get handle    resource=r0
            ${result}    do preempt failover    device=${r0}    rg=1
            should be true    ${result}

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        rg = kwargs.get("rg", "1")
        ## check the HA status before failover
        status_1 = self.get_ha_healthy_status(device=device, rg=rg, retry=2, interval=15)
        if status_1 is False:
            device.log(level="ERROR", message="RG{} is in abnormal status before failover".format(rg))
            return False
        node0_priority = status_1['node0']['priority']
        node1_priority = status_1['node1']['priority']
        status_after_failover = copy.deepcopy(status_1)
        status_after_recover = copy.deepcopy(status_1)
        status_after_failover['node0']['preempt'] = status_after_failover['node1']['preempt'] = "yes"
        status_after_failover['node0']['status'], status_after_failover['node1']['status'] = \
            status_1['node1']['status'], status_1['node0']['status']
        status_after_recover['node0']['status'], status_after_recover['node1']['status'] = \
            status_1['node1']['status'], status_1['node0']['status']
        preempt_cmd = ["set chassis cluster redundancy-group {} preempt".format(rg)]
        recover_cmd = ["delete chassis cluster redundancy-group {} preempt".format(rg)]
        if status_1['node0']['preempt'] == "yes":
            device.config(command_list=recover_cmd, timeout=self.config_timeout)
            device.commit(timeout=self.commit_timeout)
            status_after_recover['node0']['preempt'] = "no"
            status_after_recover['node1']['preempt'] = "no"
        if status_1['node0']['status'] == "secondary":
            preempt_cmd.append("set chassis cluster redundancy-group {} node 0 priority 254".format(rg))
            preempt_cmd.append("set chassis cluster redundancy-group {} node 1 priority 200".format(rg))
            recover_cmd.append("set chassis cluster redundancy-group {} node 0 priority {}".format(rg, node0_priority))
            recover_cmd.append("set chassis cluster redundancy-group {} node 1 priority {}".format(rg, node1_priority))
            status_after_failover['node0']['priority'] = "254"
            status_after_failover['node1']['priority'] = "200"
        else:
            preempt_cmd.append("set chassis cluster redundancy-group {} node 1 priority 254".format(rg))
            preempt_cmd.append("set chassis cluster redundancy-group {} node 0 priority 200".format(rg))
            recover_cmd.append("set chassis cluster redundancy-group {} node 1 priority {}".format(rg, node1_priority))
            recover_cmd.append("set chassis cluster redundancy-group {} node 0 priority {}".format(rg, node0_priority))
            status_after_failover['node1']['priority'] = "254"
            status_after_failover['node0']['priority'] = "200"

        ## change the priority to do preempt failover
        device.config(command_list=preempt_cmd, timeout=self.config_timeout)
        device.commit(timeout=self.commit_timeout)

        ## check the HA status after preempt
        status_2 = self.get_ha_healthy_status(device=device, rg=rg, retry=3, interval=10)
        if status_2 is False:
            device.log(level="ERROR", message="RG{} status is abnormal after failover".format(rg))
            return False
        else:
            if status_2 == status_after_failover:
                device.log(level="INFO", message="RG{} preempt failover succeed".format(rg))
            else:
                device.log(level="ERROR", message="RG{} status is not expected after failover".format(rg))
                device.log(level="ERROR", message=self.get_ha_status(device=device, rg=rg, cc_status=status_2))
                return False

        ## recover the config
        device.config(command_list=recover_cmd, timeout=self.config_timeout)
        device.commit(timeout=self.commit_timeout)
        status_3 = self.get_ha_healthy_status(device=device, rg=rg, retry=3, interval=10)

        if status_3 is False:
            device.log(level="ERROR", message="RG{} status is abnormal after recover".format(rg))
            return False
        else:
            if status_3 == status_after_recover:
                device.log(level="INFO", message="RG{} preempt recovering succeed".format(rg))
            else:
                device.log(level="ERROR", message="RG{} preempt recovering failed".format(rg))
                device.log(level="ERROR", message=self.get_ha_status(device=device, rg=rg, cc_status=status_3))
                return False
        return True

    def execute_cli_on_node(self, node, device=None, **kwargs):
        """execute CLI command on device through node name

        :param Device device:
            **REQUIRED** Device handle
        :param str command:
            **REQUIRED** command to run
        :param str node:
            **REQUIRED** node name, either 'node0' or 'node1'
        :param str timeout:
            *OPTIONAL* Time by which response should be received. Default is 60 seconds
        :param str format:
            *OPTIONAL* The output format. Default is xml. Supported values are xml/text

        :returns: output on success, otherwise Exception is raised

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.execute_cli_on_node(device=r0, node="node0", command="show version")

        robot::

            ${r0}    get handle    resource=r0
            execute cli on node    device=${r0}    node=node0    command=show version

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        if node == "node0":
            output = device.node0.cli(**kwargs).response()
        elif node == "node1":
            output = device.node1.cli(**kwargs).response()
        else:
            raise Exception("wrong node value, must be 'node0' or 'node1'")

        if output is False:
            raise Exception("Execution of cli command failed")
        device.log(level="INFO", message="Execute cli on node successfully")
        return output

    def execute_shell_on_node(self, node, device=None, **kwargs):
        """execute shell command on device through node name

        :param Device device:
            **REQUIRED** Device handle
        :param str node:
            **REQUIRED** node name, either 'node0' or 'node1'
        :param command:
            **REQUIRED** Shell command to execute
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :param pattern:
            *OPTIONAL: Pattern expected back from device after
            executing shell command
        :param raw_output:
            *OPTIONAL* Returns raw output of the command. Default is False

        :returns: output on success, otherwise Exception is raised

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.execute_shell_on_node(device=r0, node="node0", command="ls -l")

        robot::

            ${r0}    get handle    resource=r0
            execute shell on node    device=${r0}    node=node0    command=ls -l

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        if node == "node0":
            output = device.node0.shell(**kwargs).response()
        elif node == "node1":
            output = device.node1.shell(**kwargs).response()
        else:
            raise Exception("wrong node value, must be 'node0' or 'node1'")

        if output is False:
            raise Exception("Execution of shell command failed")
        device.log(level="INFO", message="Execute shell command on node successfully")
        return output

    def get_ha_rgs(self, device=None):
        """get a list for all HA redundancy-group
        for example, ["0","1"]

        :param Device device:
            **REQUIRED** Device handle

        :returns: A list on success, False on fail

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            rgs = ha.get_ha_rgs(device=r0)

        robot::

            ${r0}    get handle    resource=r0
            ${rgs}    get ha rgs    device=${r0}

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        rpc_cmd = device.get_rpc_equivalent(command="show chassis cluster status")
        output_element = device.execute_rpc(command=rpc_cmd).response()
        rgs = [x.text for x in output_element.findall(".//redundancy-group/redundancy-group-id")]
        if len(rgs) != 0:
            return rgs
        else:
            return False

    def get_ha_node_name(self, rg, status, device=None):
        """get node name for specific rg and HA status

        :param Device device:
            **REQUIRED** Device handle
        :param str rg:
            **REQUIRED** HA redundance-group
        :param str status:
            **REQUIRED** HA status

        :returns: string "node0" or "node1" on success, False on fail

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.get_ha_node_name(device=r0, rg="1", status="primary")

        robot::

            ${r0}    get handle    resource=r0
            get ha node name    device=${r0}    rg=1    status=primary

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        chassis_cluster_status = device.ha_status(rg=rg)
        for k, v in chassis_cluster_status.items():
            if v['status'].get_cdata() == status:
                device.log(level="INFO", message="Got node {}".format(k))
                return k
        device.log(level="ERROR", message="Cannot got node info")
        return False

    def get_ha_node_status(self, rg, node, device=None):
        """get HA status for specific rg and HA node name

        :param Device device:
            **REQUIRED** Device handle
        :param str rg:
            **REQUIRED** HA redundance-group
        :param str node:
            **REQUIRED** HA node name, either "node0" or "node1"

        :returns: a string "primary", "secondary" or other status on success, False on fail

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.get_ha_node_status(device=r0, rg="1", node="node0")

        robot::

            ${r0}    get handle    resource=r0
            get ha node status    device=${r0}    rg=1    node=node0

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        chassis_cluster_status = device.ha_status(rg=rg)
        if not (node == "node0" or node == "node1"):
            raise Exception("wrong node value, must be 'node0' or 'node1'")
        chassis_cluster_status = device.ha_status(rg=rg)
        return chassis_cluster_status[node]['status'].get_cdata()

    def get_ha_status(self, rg, device=None, **kwargs):
        """get HA status for specific rg

        :param Device device:
            **REQUIRED** Device handle
        :param str rg:
            **REQUIRED** HA redundance-group
        :param dict cc_status:
            **OPTIONAL** A dict returned from SrxSystem.ha_status

        :returns: a dict on success, False on fail

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.get_ha_status(device=r0, rg="1")

        robot::

            ${r0}    get handle    resource=r0
            get ha status    device=${r0}    rg=1

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        cc_status = kwargs.get("cc_status", device.ha_status(rg=rg))
        new_status = {}
        for k1, v1 in cc_status.items():
            new_status[k1] = {}
            for k2, v2 in v1.items():
                new_status[k1][k2] = v2.get_cdata()
        return new_status

    def get_ha_healthy_status(self, rg, device=None, **kwargs):
        """check and get ha status, return a dict of HA status
        if it is healthy, which means status is either primary or
        secondary, priority is not 0, otherwise return False

        :param Device device:
            **REQUIRED** Device handle
        :param str rg:
            **REQUIRED** HA redundance-group
        :param int retry:
            **OPTIONAL** how many times to retry, default is 3
        :param int interval:
            **OPTIONAL** retry interval, default is 15 seconds
        :param Boolean priority_zero:
            **OPTIONAL** priority 0 is accepted or not, default is False

        :return: True or False

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.get_ha_healthy_status(device=r0, rg="0", retry=3, interval=15)

        robot::

            ${r0}    get handle    resource=r0
            ${rt}    get ha healthy status    device=${r0}   rg=0    retry=3    interval=15
            log    ${rt}

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        retry = int(kwargs.get("retry", self.retry_1))
        interval = int(kwargs.get("interval", self.interval_1))
        priority_zero = kwargs.get("priority_zero", False)

        index = 1
        while index <= retry:
            msg = "try-{}: wait to check RG{} status ".format(index, rg)
            device.log(level="INFO", message=msg)
            time.sleep(interval)
            try:
                status = self.get_ha_status(rg=rg, device=device)
            except Exception as error:
                if index == retry:
                    raise TobyException("Unable to fetch redundancy-group:" + rg +
                                " details. Check if rg" + rg + " is configured.\n\n" + str(error), host_obj=self)
                else:
                    index += 1
                    continue
            if priority_zero is False:
                if (re.search("^primary|secondary$", status['node0']['status']) and
                        status['node0']['priority'] != "0" and
                        re.search("^primary|secondary$", status['node1']['status']) and
                        status['node1']['priority'] != "0"):
                    break
                else:
                    index += 1
            else:
                if (re.search("^primary|secondary$", status['node0']['status']) and
                        re.search("^primary|secondary$", status['node1']['status'])):
                    break
                else:
                    index += 1
        else:
            device.log(level="ERROR", message="RG{} status is abnormal".format(rg))
            device.log(level="ERROR", message=status)
            return False
        device.log(level="INFO", message="RG{} status is correct".format(rg))
        device.log(level="INFO", message=status)
        return status


    def reboot_node(self, node, device=None, **kwargs):
        """reboot device with the node name

        :param Device device:
            **REQUIRED** Device handle
        :param str node:
            **REQUIRED** Node name, either 'node0' or 'node1'
        :param int wait:
            *OPTIONAL* Time to sleep before reconnecting, Default value is 60 seconds
        :param int interval:
            *OPTIONAL* Interval at which reconnect need to be attempted after reboot is performed.
            Default is 20 seconds
        :param int timeout:
            *OPTIONAL* Time to reboot and connect to device. Default is 360 seconds
        :param str mode:
            *OPTIONAL* Mode in which reboot needs to be executed. Default is 'shell'.
            Also supports 'cli'. mode=cli is valid only for Junos devices.

        :returns: True if device is rebooted and reconnection is successful,
            else an Exception is raised

        **Example:**

        python::

            from jnpr.toby.security.HA.HA import HA
            from jnpr.toby.init.init import init
            obj = init()
            obj.Initialize(init_file="your_params.yaml")
            r0 = obj.get_handle(resource="r0")
            ha = HA()
            ha.reboot_node(device=r0, node="node0")
            ## Examples, only one is needed in your code
            # reboot device using default arguments
            # wait 60 seconds then trying to connect every 20 seconds, declare it as down after 360 seconds
            ha.reboot_node(device=r0, node="node0")
            # do reboot failover for RG1 using specified arguments
            # wait 90 seconds then trying to connect every 10 seconds, declare it as down after 420 seconds
            ha.reboot_node(device=r0, node="node0", wait=90, interval=10, timeout=420)

        robot::

            ${r0}    get handle    resource=r0
            ## Examples, only one is needed in your code
            reboot node    device=${r0}    node=node0
            reboot node    device=${r0}    node=node0    timeout=600
            reboot node    device=${r0}    node=node0    wait=90    interval=10    timeout=360

        """
        if device is None:
            if self.device is not None:
                device = self.device
            else:
                raise Exception("device handle is None")
        if not re.match(r"node[0-1]", node):
            raise Exception("Mandatory argument 'node' must be 'node0' or 'node1'!")

        ## convert arguments types since robot takes arguments as str by default
        wait = int(kwargs.get("wait", 60))
        interval = int(kwargs.get("interval", 20))
        timeout = int(kwargs.get("timeout", 360))
        mode = str(kwargs.get("mode", "cli"))

        device.log(level="INFO", message="Start to reboot node:" + str(node))
        return device.reboot(mode=mode, wait=wait, interval=interval, timeout=timeout, system_nodes=node)
