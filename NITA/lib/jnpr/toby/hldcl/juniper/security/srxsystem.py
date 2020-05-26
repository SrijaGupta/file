"""
Class for System
"""
import re
import time
import jxmlease
import copy
import inspect
import json
from jnpr.toby.hldcl.juniper.junipersystem import JuniperSystem
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.utils.response import Response
from jnpr.toby.utils.utils import run_multiple
from jnpr.toby.security.system.system_license import system_license

class SrxSystem(JuniperSystem):
    """
    Class System to create JunOS SRX System object.
    """
    def __init__(self, system_data, connect_complex_system=True, connect_dual_re=True):
        """

        Base class for JunOS SRX system

        :param nodedict:
            **REQUIRED** systemdict of node
        :return: SRX system object
        """
        self.get_current_function_name = lambda: inspect.stack()[1][3]
        self.pprint = lambda x: json.dumps(x, indent=4, sort_keys=True, default=str, ensure_ascii=False)
        self.title_msg = lambda x, width=80, fillchar="=": " {} ".format(x).upper().center(width, fillchar)
        self.underscore_lowercase_transit = lambda x: re.sub(r"-", "_", str(x)).lower()
        self.underscore_uppercase_transit = lambda x: re.sub(r"-", "_", str(x)).upper()
        self.list_element_to_lowercase = lambda x: [s.lower() for s in x]
        self.list_element_to_uppercase = lambda x: [s.upper() for s in x]

        default_connect = True
        if list(self.findkeys(system_data['system'], 'connect')).__len__() > 0:
            t.log(level="INFO", message="SETTING DEFAULT to False")
            t.log(level="INFO", message=str(list(self.findkeys(system_data['system'], 'connect')).__len__()))
            default_connect = False
        self.node_connect = self.is_node_connect_set(system_data)
        for system_node in system_data['system'].keys():
            if default_connect or not self.node_connect:
                # This need to be modified to detect the master node when none of the node has connect set
                system_data['system'][system_node]['connect'] = True
            elif 'connect' not in system_data['system'][system_node].keys():
                system_data['system'][system_node]['connect'] = False
            self.controller_connect = self.is_controller_connect_set(system_data['system'][system_node])
            for controller in sorted(list(system_data['system'][system_node]['controllers'].keys())):
                if default_connect or ('connect' in system_data['system'][system_node].keys() and not self.controller_connect):
                    system_data['system'][system_node]['controllers'][controller]['connect'] = True
                else:
                    t.log(level="INFO", message="Setting connect for " + controller)

        super(SrxSystem, self).__init__(system_data)

        if len(self.nodes) > 1:
            self.complex_system = True
            self.ha = True
        else:
            self.complex_system = False
            # Check if self.ha has already been set (perhaps NFX device), if not then run command to check if device
            # is HA or not
            try:
                self.ha
            except:
                check = jxmlease.parse(
                    self.current_node.current_controller.cli(command='show version', format='xml').response())
                if 'multi-routing-engine-results' in check['rpc-reply']:
                    self.ha = True
                else:
                    self.ha = False
        for node in system_data['system']:
            if not system_data['system'][node]['connect']:
                self.complex_system = False
            if system_data['system'][node]['connect']:
                self.current_node = self.nodes[node]

        if self.complex_system:
            for key in self.nodes:
                if key == 'primary':
                    self.node0 = self.nodes[key].current_controller
                else:
                    self.slave_name = key
                    self.node1 = self.nodes[key].current_controller
                if self.nodes[key].is_node_status_primary():
                    self.current_node = self.nodes[key]

        self.runtime = {}

    @staticmethod
    def _transit_node_alias(node_alias, mode="STR"):
        """Return node name by STR or INT mode

        User may give node name by an INT (1), or STR ("1") or name ("node0"), but node name are different for CLI cmd and search re-name.
        For example, CLI cmd should tail "show security flow session node 0", but search flow session from "re-name" must be "node0".

        This method will transit user given value whatever 1, "1", or "node1" to "node1" if mode="STR", or 1 if mode="INT"
        """
        node_alias = str(node_alias).lower()
        mode = str(mode).upper()
        if node_alias in (0, "0", "node0"):
            node_str = "node0"
            node_int = 0
        elif node_alias in (1, "1", "node1"):
            node_str = "node1"
            node_int = 1
        else:
            raise TobyException("option 'node_alias' must be 0, '0', node0, 1, '1' or node1, but got '{}'".format(node_alias))

        if mode == "STR":
            return node_str

        return node_int

    def is_ha(self):
        """
        Module to check if the srx system is a High Availability system or not
        :return: Boolean. True, if system is HA, False otherwise.
        """
        return self.ha

    def node_name(self):
        """
        Module to fetch the current node name('node0'/'node1')
        :return: node name. 'node0'/'node1'
        """
        if not self.ha:
            raise TobyException('This is not an SRX/VSRX complex system. node_name()'
                                ' is valid only for a complex system.', host_obj=self)
        return self.current_node.node_name()

    def node_status(self, rg="0"):
        """
        Module to fetch the current node status
        :param rg: Redundancy group. Default: "0"
        :return: status of the chassis of mentioned rg: "primary","secondary","hold",etc.
        """
        if not self.ha:
            raise TobyException('This is not an SRX/VSRX complex system. node_status()'
                                ' is valid only for a complex system.', host_obj=self)
        return self.ha_status(rg=rg)[self.node_name().lower()]['status']

    def ha_status(self, **kwargs):
        """

        High Availability Status Check

        :param rg:
            *OPTIONAL* Redundancy-Group(0..128) Ex. rg="0". Default 0
        :return: 3D Dictionary with 'node0' and 'node1' as primary keys and following secondary keys
            {'name', 'priority', 'status', 'preempt', 'failover-mode', 'monitor-failures'}
            Raises Exception incase Chassis cluster is not enabled.

        """
        if not self.ha:
            raise TobyException('This is not an SRX/VSRX complex system. ha_status()'
                                ' is valid only for a complex system.', host_obj=self)
        # Check if rg is provided
        if 'rg' not in kwargs:
            kwargs['rg'] = "0"

        # Execute CLI command to get details
        sccs = self.current_node.current_controller.channels['pyez'].cli(
            "show chassis cluster status redundancy-group " + kwargs['rg'],
            format="xml", warning=False)
        # Get RG stats
        try:
            status = jxmlease.parse_etree(sccs)
            status = status['chassis-cluster-status']['redundancy-group']['device-stats']
        except Exception as error:
            raise TobyException("Unable to fetch redundancy-group:" + kwargs['rg'] +
                                " details. Check if rg" + kwargs['rg'] + " is configured.\n\n" + str(error), host_obj=self)

        # Create dictionaries to store node stats
        node0 = {'name': status['device-name'][0], 'priority': status['device-priority'][0],
                 'status': status['redundancy-group-status'][0]}
        node0.update({'preempt': status['preempt'][0], 'failover-mode': status['failover-mode'][0],
                      'monitor-failures': status['monitor-failures'][0]})
        node1 = {'name': status['device-name'][1], 'priority': status['device-priority'][1],
                 'status': status['redundancy-group-status'][1]}
        node1.update({'preempt': status['preempt'][1], 'failover-mode': status['failover-mode'][1],
                      'monitor-failures': status['monitor-failures'][1]})

        return {'node0': node0, 'node1': node1}

    def failover(self, **kwargs):
        """
        High Availability Failover Execution

        :param INT|STR|LIST|TUPLE rg:
            *OPTIONAL* Redundancy-Group(0..128) number or Group LIST. Ex. rg="0" or rg=[0, 1, 2, 3]. Default: 0

        :param INT|STR node:
            *OPTIONAL* Node which needs to be made primary. "0", "1", "node0" or "node1" (case insensitive). Default: Performs a failover

        :param BOOL force:
            *OPTIONAL* Whether do force failover. Default: False

        :param INT|STR timeout:
            *OPTIONAL* Wait a while for rg failover, and then checking whether failover succeed.

        :param INT|STR reset_waiting_timeout:
            *OPTIONAL* As default, this method will reset previous failover and waiting 1 second to start new failover. But sometimes we need more
                       than one second to reset, this option used for this. Default: 1

        :param INT|STR check_cnt:
            *OPTIONAL* Another solution of "timeout". With option "check_interval" to do loop checking.
                       Default: If rg=0, check_cnt=15; otherwise (1..128) check_cnt=2

        :param INT|STR check_interval:
            *OPTIONAL* With option "check_cnt" to do loop checking. Default: If rg=0, check_cnt=60; otherwise (1..128) check_cnt=10

        :return:
            Boolean(True/False) depending on passing and failing of failover.

        :example:
            + do failover for single RG: r0.failover(rg=0)
            + do failover for multiple RGs to specific node: r0.failover(rg=[0, 1, 2, 3], node=1)
        """
        if not self.complex_system:
            raise TobyException('This is not an SRX/VSRX complex system. failover() is valid only for a complex system.'
                                ' Please connect to both the nodes of the complex system.', host_obj=self)
        # User Option
        options = {}
        options["rg"] = kwargs.pop("rg", 0)
        options["node"] = kwargs.pop("node", None)
        options["force"] = kwargs.pop("force", False)
        options["check_interval"] = kwargs.pop("check_interval", None)
        options["check_cnt"] = kwargs.pop("check_cnt", None)
        options["timeout"] = kwargs.pop("timeout", None)
        options["reset_waiting_timeout"] = int(kwargs.pop("reset_waiting_timeout", 1))

        if isinstance(options["rg"], (str, int)):
            rg_list = (options["rg"], )
        elif isinstance(options["rg"], (list, tuple)):
            rg_list = options["rg"]
        else:
            raise TobyException("option 'rg' must be STR, INT, LIST or TUPLE but got '{}'".format(type(options["rg"])))

        rg_failover_result_list = []
        for rg_number in rg_list:
            # if "timeout" given, it means waiting given secs and just checking one time. If "timeout",
            # "check_cnt" and "check_interval" all existing, only "timeout" implement
            rg_number = str(rg_number)
            if options["check_interval"] is None:
                if rg_number == "0":
                    rg_check_interval = float(60)
                else:
                    rg_check_interval = float(10)
            else:
                rg_check_interval = float(options["check_interval"])

            if options["check_cnt"] is None:
                if rg_number == "0":
                    rg_check_cnt = int(15)
                else:
                    rg_check_cnt = int(2)
            else:
                rg_check_cnt = int(options["check_cnt"])

            if options["timeout"] is not None:
                rg_check_cnt = int(1)
                rg_check_interval = float(options["timeout"])

            # Get current HA chassis cluster status to decide failover node
            try:
                status = self.ha_status(rg=rg_number)
            except TobyException:
                rg_failover_result_list.append(False)
                break

            # Check if node is provided, if not then perform a failover irrespective of node details
            if options["node"] is None:
                if status['node0']['status'] == "primary":
                    options['node'] = "1"
                elif status['node1']['status'] == "primary":
                    options['node'] = "0"
                else:
                    raise TobyException("Cannot find primary node", host_obj=self)

            # Maybe user provided node by INT or string but "node0" or "node1"
            options['node'] = str(self._transit_node_alias(options["node"], mode="INT"))

            # Do failover
            if options['node'] == "0" and status['node0']['status'] == "primary":
                self.log(message="Node 0 is already in primary state for RG {}\nNo need for failover".format(rg_number))
                rg_failover_result_list.append(True)
                continue

            if options['node'] == "1" and status['node1']['status'] == "primary":
                self.log(message="Node 1 is already in primary state for RG {}\nNo need for failover".format(rg_number))
                rg_failover_result_list.append(True)
                continue

            cmd = "request chassis cluster failover reset redundancy-group {}".format(rg_number)
            self.cli(command=cmd, format="text").response()
            self.log(message="Waiting '{}' sec(s) after reset RG {}".format(options["reset_waiting_timeout"], rg_number))
            time.sleep(options["reset_waiting_timeout"])

            cmd = "request chassis cluster failover redundancy-group {} node {}".format(rg_number, options['node'])
            if options["force"] is True:
                cmd += " force"
            self.cli(command=cmd, format="text").response()
            time.sleep(2)

            # Added condition if preempt is enabled do not reset as a request of TOBY-1050
            resp = jxmlease.parse_etree(
                self.cli(command="show chassis cluster status redundancy-group {}".format(rg_number), channel="pyez", format="xml").response()
            )

            if 'preempt' in resp['chassis-cluster-status']['redundancy-group']['device-stats'] and \
               resp['chassis-cluster-status']['redundancy-group']['device-stats']['preempt'][0].upper() == 'YES':
                self.log(message="Skipping resetting of the redundancy-group {} since preempt is set to yes".format(rg_number))
            else:
                self.cli(command="request chassis cluster failover reset redundancy-group {}".format(rg_number), format="text").response()

            # check failover whether succeed
            rg_failover_result = False
            for index in range(1, rg_check_cnt + 1):
                self.log(message="Loop {}: Waiting '{}' secs for next RG {} failover checking...".format(index, rg_check_interval, rg_number))
                time.sleep(rg_check_interval)

                status = self.ha_status(rg=rg_number)
                msg = "cluster response:\nnode0 status:    {}\nnode0 priority:  {}\nnode1 status:    {}\nnode1 priority:  {}".format(
                    status['node0']["status"], status['node0']["priority"], status['node1']["status"], status['node1']["priority"]
                )
                self.log(message=msg, level="DEBUG")

                checkpoint_list = []
                if options['node'] == "0":
                    checkpoint_list.append(status['node0']["status"] == "primary")
                    checkpoint_list.append(status['node1']["status"] == "secondary")
                    checkpoint_list.append(status['node0']["priority"] != "0")
                    checkpoint_list.append(status['node1']["priority"] != "0")

                    if False not in checkpoint_list:
                        if rg_number == '0':
                            self.switch_to_primary_node()
                        self.log(message="RG {} Failover is successful".format(rg_number))
                        rg_failover_result = True
                        break

                elif options['node'] == "1":
                    checkpoint_list.append(status['node1']["status"] == "primary")
                    checkpoint_list.append(status['node0']["status"] == "secondary")
                    checkpoint_list.append(status['node1']["priority"] != "0")
                    checkpoint_list.append(status['node0']["priority"] != "0")

                    if False not in checkpoint_list:
                        if rg_number == '0':
                            self.switch_to_primary_node()
                        self.log(message="RG {} Failover is successful".format(rg_number))
                        rg_failover_result = True
                        break

                self.log(message='RG {} Failover is not complete'.format(rg_number), level='INFO')

            rg_failover_result_list.append(rg_failover_result)

        self.log(message="rg_failover_result_list: {}".format(rg_failover_result_list), level="DEBUG")
        if False not in rg_failover_result_list and len(rg_failover_result_list) == len(rg_list):
            return_value = True
        else:
            return_value = False

        self.log(message="Function {} return value:\n{}".format(self.get_current_function_name(), return_value))
        return return_value

    def switch_node(self, node=None):
        """
        Function to switch to a node handle
        :param node: Node to which user wants to switch.
                    Example: node='1' switches to node1 in the cluster.
        :return: Boolean value. True if handle switched successfully else False
        """
        if not self.complex_system:
            raise TobyException('This is not an SRX/VSRX complex system. switch_node()'
                                ' is valid only for a complex system.'
                                ' Please connect to both the nodes of the complex system.', host_obj=self)
        if node is None:
            if self.current_node == self.nodes['primary']:
                self.current_node = self.nodes[self.slave_name]
            elif self.current_node == self.nodes[self.slave_name]:
                self.current_node = self.nodes['primary']
            return True
        elif node == '0':
            self.current_node = self.nodes['primary']
            return True
        elif node == '1':
            self.current_node = self.nodes[self.slave_name]
            return True
        else:
            raise TobyException("Wrong value passed for 'node' parameter. Accepted value: node='0'/'1'", host_obj=self)

    def switch_to_primary_node(self):
        """
        Function to reset to node which has Primary status on RG0
        return: Boolean, depending on whether the device handle could be updated with primary handle
        """
        if self.complex_system:
            for key in self.nodes:
                if self.nodes[key].is_node_status_primary():
                    self.current_node = self.nodes[key]
                    return True
            return False
        else:
            message = 'This is not an SRX/VSRX complex system. switch_to_primary_node()' + \
                      ' is valid only for a complex system.' + \
                      ' Please connect to both the nodes of the complex system.'
            self.log(message=message, level="INFO")
            raise TobyException(message, host_obj=self)

    def cli(self, execution_node=None, node=None, **kwargs):
        """
        Executes operational commands on JunOS device, supports specific node in HA
        Example :-
            cli(command="show version", format="xml")
            cli(command="show version", execution_node="node0", timeout = 60)
            cli(command="show version", execution_node="node1", node="local")
            cli(command="show version", execution_node="node1", node="node0")
        :param str command:
            **REQUIRED** CLI command to execute
        :param int timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :param str format:
            *OPTIONAL* The output format. Default is text.
            ``Supported values``: xml or text
        :param str execution_node:
            *OPTIONAL* Node of the HA, where the command to be executed.
            ``Supported values``: node0 or node1
            ``Default value``   : None, The command will be executed in the primary device.
        :param str node:
            *OPTIONAL* Node of the HA where values are required. equivalent of > show version node node0
            ``Supported values``: node0 or node1 - Provides node specific output
                                  local       - Provides the output of the node where command
                                                executed.
            ``Default value``   : Returns the output completelely
        :param channel: Channel to use
        :return: Object with the following methods
            'response()': Response from the CLI command(text/xml)
        """
        if 'command' in kwargs and kwargs['command'] is not None:
            command = kwargs['command']
        else:
            raise TobyException("Mandatory argument 'command' is missing!", host_obj=self)
        # Return if it not HA
        # Decides which node output to return
        if not self.is_ha():
            cmd = command
        elif node is None:
            cmd = command
        elif node == "node0":
            cmd = command + " node " + "0"
        elif node == "node1":
            cmd = command + " node " + "1"
        elif node == "local":
            cmd = command + " node " + "local"
        else:
            raise TobyException("Invalid HA Node value for output. Supported values are "
                                "None(default)/node0/node1/local", host_obj=self)

        # Decides which node to execute the command
        kwargs["command"] = cmd
        if not self.is_ha() or execution_node is None:
            return self.current_node.current_controller.cli(**kwargs)
        elif execution_node == "node0":
            return self.node0.cli(**kwargs)
        elif execution_node == "node1":
            return self.node1.cli(**kwargs)
        else:
            raise TobyException("Invalid HA Node for execution. Supported values are None(default)/node0/node1", host_obj=self)

    def execute_as_rpc_command(self, command, execution_node=None, node="local", command_type="cli"):
        """
        Executes RPC command and returns the node specific values by removing HA tags.
        Example :-
                execute_as_rpc_command(command="show version")
                execute_as_rpc_command(command=rpc_command, command_type="rpc")
                execute_as_rpc_command(command="show version", execution_node="node0", node="node1")
                execute_as_rpc_command(command="show version", execution_node="node1", node="all")
        :param str command:
            **REQUIRED** CLI command to be executed
        :param str execution_node:
            *OPTIONAL* Node of the HA, where the command to be executed.
            ``Supported values``: node0 or node1
            ``Default value``   : None, The command will be executed in the primary device.
        :param str node:
            *OPTIONAL* Node of the HA where values are required
            ``Supported values``: node0 or node1 - Provides node specific output
                                  local- Provides the output of the node where command executed.
                                  all  - Provides the output of both nodes. The return value
                                         removes the HA tag
                                  None - Provides the output without changes. Can be Use it where no
                                         node info exist in the output (such as show license)
            ``Default value``   : local
        :param str command_type:
            *OPTIONAL* Command type passed. Supported values cli, xml
        :return: Returns the node specific etree values
        :rtype: list or dict
        """
        if command is None:
            raise TobyException("Mandatory argument 'command' is missing!", host_obj=self)
        self.log(message=command, level='DEBUG')

        # Get RPC equivalent of command
        if command_type == "cli":
            rpc_str = self.get_rpc_equivalent(command=command)
        elif command_type == "rpc":
            rpc_str = command
        else:
            raise TobyException("incorrect command_type: " + command_type, host_obj=self)

        # Execute the RPC command
        if not self.is_ha() or execution_node is None:
            etree_obj = self.current_node.current_controller.execute_rpc(command=rpc_str).response()
        elif execution_node == "node0":
            self.log(message="Executing on node0", level="DEBUG")
            etree_obj = self.node0.execute_rpc(command=rpc_str).response()
        elif execution_node == "node1":
            self.log(message="Executing on node1", level="DEBUG")
            etree_obj = self.node1.execute_rpc(command=rpc_str).response()
        else:
            self.log(message="Invalid HA Execution Node. Supported values are None(default)/node0/node1", level='ERROR')
            raise ValueError("Invalid HA Node for execution. Supported values are None(default)/node0/node1")
        # Return the value as it is for  SA device
        if not self.is_ha():
            # "show security idp attack table" returns True instead of empty dict or list when
            # attack table is emptY
            # To handle this scenario, we check for True and return None for empty value.
            # To Do - Revisit after this bug is fixed
            if etree_obj is True:
                return None
            return jxmlease.parse_etree(etree_obj)

        # Remove the HA specific tags
        status = jxmlease.parse_etree(etree_obj)
        # Return values as it is, since no node info exist
        if node is None:
            return status
        status = status['multi-routing-engine-results']['multi-routing-engine-item']
        # If commands (like sig download) runs only on primary, return without parsing since only
        #  one node info exists
        if isinstance(status, dict):
            return status

        # Find the node, where values required
        if node == "all":
            self.log(message="Values of all the node", level="DEBUG")
            return status
        if node == "local":
            if execution_node is None:
                node_str = self.node_name()
            else:
                node_str = execution_node
        elif node == "node0":
            node_str = "node0"
        elif node == "node1":
            node_str = "node1"
        else:
            self.log(
                message="Invalid HA Node value. Supported values are None/all/node0/node1/local(default)",
                level='ERROR',
            )
            raise ValueError("Invalid HA Node value for output. Supported "
                             "None/all/node0/node1/local(default)")

        # Pickup the node specific values
        self.log(message="Node to get output is " + node_str, level="DEBUG")
        if status[0]['re-name'] == node_str:
            status = status[0]
        elif status[1]['re-name'] == node_str:
            status = status[1]
        else:
            self.log(message="Node name %s not found in the status output" % (node_str), level='INFO')
            raise ValueError("Node name %s not found in the status output" % (node_str))
        return status

    def is_multi_spu(self):
        """
        Checks the device whether the device running multiple flowd instances (multiple spu)
        :return: Returns True if the device is multi spu
        :rtype: bool
        """
        model = self.current_node.current_controller.get_model()
        if not model:
            version_info = self.get_version_info()
            if "node0" in version_info:
                model = version_info["node0"]["product_model"]
            else:
                model = version_info["product_model"]

        if re.match(r"(srx5400|srx5600|srx5800)", model, re.IGNORECASE):
            return True
        return False

    def get_platform_type(self):
        """
        Returns the platform type based on the architecture
        :return: Returns octeon/x86/xlp/nfx150
        :rtype: str
        """
        model = self.current_node.current_controller.get_model()
        if not model:
            version_info = self.get_version_info()
            if "node0" in version_info:
                model = version_info["node0"]["product_model"]
            else:
                model = version_info["product_model"]

        model = model.upper()
        platform_type = 'x86'

        if model in ("SRX300", "SRX320", "SRX320-POE", "SRX340", "SRX345", "SRX345-DUAL-AC", "SRX550", "SRX550M"):
            platform_type = "octeon"
        elif model in ("SRX1500", "SRX4100", "SRX4200", "SRX4600"):
            platform_type = "x86"
        elif model in ("SRX5400", "SRX5600", "SRX5800"):
            platform_type = "xlp"
        elif re.match(r"VSRX", model):
            # VSRX2.0 and VSRX3.0 have different structure. VSRX2.0 is X86 but VSRX3.0 is OCTEON
            res = self.current_node.current_controller.shell(command="sysctl hw.product.model").response().strip()
            if re.search(r"srxtvp", res, re.IGNORECASE):     # VSRX2.0 response is: hw.product.model: srxtvp
                platform_type = "x86"
            else:
                platform_type = "octeon"                     # VSRX3.0 response is: hw.product.model: vsrx

        elif re.match(r"NFX150", model):
            # PORTER series
            platform_type = "nfx150"

        return platform_type

    def get_srx_pfe_names(self, node="all"):
        """
        Returns the flowd name for single spu and list of flowd pic name for multiple spu.
        The return value is list, For single spu use get_flow_pic_names()[0]
        :param str node:
            *OPTIONAL* Node of the HA, where the command to be executed.
            ``Supported values``: node0 or node1
            ``Default value``   : all, returns both the node pfe names.
        :return: Returns list of flowd names
        :rtype: list
        """
        platform_type = self.get_platform_type()
        # Return the values for single flow platforms
        if not self.is_multi_spu():
            if platform_type == "octeon":
                return ["fwdd"]
            elif platform_type == "x86":
                return ["fpc0"]
            else:
                return []

        # Process the pic list for the multi flow platforms
        flow_list = []
        if not self.is_ha():
            details = self.execute_as_rpc_command("show chassis fpc pic-status")
            for fpc in details['fpc-information']['fpc']:
                fpc_number = str(fpc.get('slot'))
                pic_list = fpc.get('pic')
                if isinstance(pic_list, list):
                    for pic in pic_list:
                        if pic.get('pic-type') == "SPU Flow":
                            flow_list.append("fpc%s.pic%s" % (fpc_number, str(pic.get('pic-slot'))))
                else:
                    pic = pic_list
                    if pic.get('pic-type') == "SPU Flow":
                        flow_list.append("fpc%s.pic%s" % (fpc_number, str(pic.get('pic-slot'))))
        else:
            if node == "node0" or node == "node1":
                details = [self.execute_as_rpc_command("show chassis fpc pic-status", node=node)]
            else:
                details = self.execute_as_rpc_command("show chassis fpc pic-status", node="all")
            for node_info in details:
                node_name = node_info.get('re-name')
                for fpc in node_info['fpc-information']['fpc']:
                    fpc_number = str(fpc.get('slot'))
                    pic_list = fpc.get('pic')
                    if isinstance(pic_list, list):
                        for pic in pic_list:
                            if pic.get('pic-type') == "SPU Flow":
                                flow_list.append("%s.fpc%s.pic%s" % (node_name, fpc_number, str(pic.get(
                                    'pic-slot'))))
                    else:
                        pic = pic_list
                        if pic.get('pic-type') == "SPU Flow":
                            flow_list.append("%s.fpc%s.pic%s" % (node_name, fpc_number, str(pic.get(
                                'pic-slot'))))
        return flow_list

    # verifies pic is online or offline
    def verify_pic_status(self, **kwargs):
        """
        Verifies pic status by running "show chassis fpc pic-status"
        Waits until pics comes online or rechecks still it reaches max tries with wait time.
        It can also be used for waiting pic to come online after reboot.
        :param max_tries
            *OPTIONAL*  Number of tries before returning. Default is 10
        :param sleep_time
            *OPTIONAL*  Sleep in secs before next try. Default is 30
        :param err_level:
            Supported values INFO/WARN/ERROR
            Default ERROR
        :return: True if pics are online
            Raise exception if pics are offline
            Note: For negative cases , use 'err_level', so returns False if pics are offline
        """
        i = 1
        flag = 1
        max_tries = kwargs.get('max_tries', 10)
        sleep_time = kwargs.get('sleep_time', 30)
        err_level = kwargs.get('err_level', 'ERROR')
        show_cmd = 'show chassis fpc pic-status'
        rpc_eq = self.get_rpc_equivalent(command=show_cmd)
        while i < int(max_tries):
            resp = self.execute_rpc(command=rpc_eq).response()
            for fpc in resp.findall('.//fpc'):
                for pic in fpc.findall('./pic'):
                    if pic.find('./pic-state').text.lower() != 'online':
                        flag = 0
            if flag == 1:
                self.log(message="All pics are online", level='INFO')
                return True
            i = i + 1
            time.sleep(int(sleep_time))

        if flag == 0 and err_level == 'ERROR':
            raise TobyException("Pics are not online", host_obj=self)
        else:
            # In negative cases, we don't want to raise exception
            self.log(message="Pics are not online", level=err_level)
            return False

    def detect_core(self, core_path=None, resource=None):
        """
            Detect cores on the device
        """
        system_core_count = 0
        system_name = ''

        from jnpr.toby.utils.utils import get_testcase_name
        get_testcase_name()

        if resource is not None:
            t.log('name in system: '+ t.get_t(resource=resource, attribute='name'))
            system_name = t.get_t(resource=resource, attribute='name')

        if self.ha:
            if not system_name:
                system_name = self.node0.name

            self.node0.re_name = 'node0'
            system_core_count += self.node0.detect_core(core_path=core_path, system_name=system_name,
                                                        command='show system core-dumps node 0')
            self.node1.re_name = 'node1'
            system_core_count += self.node1.detect_core(core_path=core_path, system_name=system_name,
                                                        command='show system core-dumps node 1')

        else:
            if not system_name:
                system_name = self.current_node.current_controller.name
            system_core_count += self.current_node.current_controller.detect_core(core_path=core_path, system_name=system_name)

        if system_core_count:
            t.log(level='WARN', message='Core is found on the device : ' + system_name + ' and its count is ' + str(system_core_count))
            return True
        else:
            t.log('Core is not found on the device : ' + system_name)
            return False

    def vty(self, command, **kwargs):
        """According to platform to send vty command to device and get response

        Device have different way to send command. For example, low-end or branch device use cprod command, but high-end use srx-cprod.sh. This
        method check platform type and to send cmd accordingly, then return all cmd's response.

        :param STR|LIST|TUPLE command:
            **REQUIRE** A command string or a LIST/TUPLE to send to device. If option 'destination' given, only support single command.

        :param STR destination:
            *OPTIONAL* Device component address. There are 3 pre-defined component name: "CP", "SPU" and "ALL" as below. Or set customized address.
            Default: CP

                       CP   - only send cmd to CP
                       SPU  - send cmd to all SPUs
                       ALL  - send cmd both to CP and SPUs

        :param INT retry_cnt | send_cnt:
            *OPTIONAL* send cmd times. Default: 1.

                       Sometimes vty cmd cannot send to component. This special option used to send cmd again if got error.

                       If set 3 to this option, it means every cmd will re-send 2 times if got error.

        :param BOOL force_on_primary_node:
            *OPTIONAL* Run VTY command on HA primary node. For SA topo, this option ignored. Default: None

        :param STR|INT node:
            *OPTIONAL* Run VTY command on HA specific node. This argument's priority is higher than force_on_primary_node. It means if this option set
                       to "node1", VTY command will be run as node1 even primary node is node0. Default: None

        :param INT timeout:
            *OPTIONAL* Timeout to get infomation. Default: 300

        :param STR|REGEX pattern:
            *OPTIONAL* Compatible option to send command. Default: None

        :param BOOL raw_output:
            *OPTIONAL* Compatible option to send command. Default: False

        :param STR platform:
            *OPTIONAL* Set specific platform type one of X86, XLP, OCTEON, or NFX150 (case insensitive). Default will get platform type automatically.
                       Default: None

        :return:
            All vty command's response. or raise TobyException
        """
        options = {}
        options["command"] = copy.deepcopy(command)
        options["destination"] = kwargs.pop("destination", "CP")
        options["retry_cnt"] = int(kwargs.pop("retry_cnt", 1))
        options["force_on_primary_node"] = kwargs.pop("force_on_primary_node", None)
        options["node"] = kwargs.pop("node", None)
        options['timeout'] = int(kwargs.pop("timeout", 300))
        options["pattern"] = kwargs.pop("pattern", None)
        options["raw_output"] = kwargs.pop("raw_output", False)
        options["platform"] = kwargs.pop("platform", None)

        if options["destination"].upper() not in ("CP", "SPU", "ALL") and isinstance(options["command"], str):
            kwargs = {}
            kwargs["command"] = options["command"]
            kwargs["destination"] = options["destination"]
            kwargs["timeout"] = options["timeout"]
            kwargs["raw_output"] = options["raw_output"]
            if options["pattern"] is not None:
                kwargs["pattern"] = options["pattern"]

            # compatible code to run vty like before
            return Response(response=self.current_node.current_controller.vty(**kwargs).response(), status=True)

        # option check
        if isinstance(options["command"], str):
            user_cmd_list = [options["command"], ]
        elif isinstance(options["command"], (list, tuple)):
            user_cmd_list = list(options["command"])
        else:
            raise TobyException("Option 'command' must be STR, LIST or TUPLE, but got '{}'".format(type(options["command"])))

        if re.match(r"CP|SPU|ALL", options["destination"], re.I):
            options["destination"] = options["destination"].upper()

        ha_topo = self.is_ha()
        if ha_topo:
            # if 'node' set, ignore option 'force_on_primary_node'
            if options["node"] is not None:
                options["force_on_primary_node"] = False
                self.runtime["method_vty_node_name"] = self._transit_node_alias(options["node"], mode="STR")

            # if 'node' and 'force_on_primary_node' all not set, run VTY command on current node
            if "method_vty_node_name" not in self.runtime:
                self.runtime["method_vty_node_name"] = self.node_name()

            # if 'node' not True but force_on_primary_node is, switch to primary node and run command on this node
            if options["force_on_primary_node"] is True:
                self.switch_to_primary_node()
                self.runtime["method_vty_node_name"] = self.node_name()

        # This method need root permission
        if not self.su():
            raise TobyException("{} cannot get root permission on device: {}".format(self.get_current_function_name(), str(self)))

        if ha_topo:
            tnpdump_info = self.get_tnpdump_info(
                node=self.runtime["method_vty_node_name"],
                platform=options["platform"],
                timeout=options["timeout"]
            )
        else:
            tnpdump_info = self.get_tnpdump_info(timeout=options["timeout"], platform=options["platform"])

        if options["destination"] == "CP":
            addr_list = [tnpdump_info["cp_addr"], ]
        elif options["destination"] == "SPU":
            addr_list = tnpdump_info["spu_addr_list"]
        elif options["destination"] == "ALL":
            addr_list = tnpdump_info["both_addr_list"]
        else:
            addr_list = [options["destination"], ]

        # create cmd list
        cmd_list = []
        for user_cmd in user_cmd_list:
            for addr in addr_list:
                cmd_list.append("cprod -A {} -c '{}'".format(addr, user_cmd))

        # debug info
        self.log(message="send command:\n{}".format(self.pprint(cmd_list)), level="DEBUG")

        response_list = []
        # due to sometimes vty command cannot send to component, we need re-send command several times.
        for cmd in cmd_list:
            cmd_retry_cnt = options["retry_cnt"]
            while cmd_retry_cnt:
                response = self.shell(
                    command=cmd,
                    timeout=options["timeout"],
                    pattern=options["pattern"],
                    raw_output=options["raw_output"]
                ).response()
                response_list.append(response)

                if re.search(r"Couldn't initiate connection", response, re.I):
                    cmd_retry_cnt -= 1
                else:
                    cmd_retry_cnt = 0

        return_value = "\n".join(response_list)
        self.log(message="Function {} return value:\n{}".format(self.get_current_function_name(), return_value))
        return Response(response=return_value, status=True)

    def get_tnpdump_info(self, force_get=False, platform=None, node=None, timeout=300):
        """Based on tnpdump command to archive all info

        :param BOOL force_get:
            *OPTIONAL* Set True will send command to get info every time. If set False, only first time send command to device. Default: False

        :param STR platform:
            *OPTIONAL* Device platform such as X86, OCTEON, XLP, NFX150, etc... Default: None means get platform automatically.

        :param INT|STR node:
            *OPTIONAL* For HA topology. Valid value include 0, 1, "node0" or "node1". Default: None

        :param INT timeout:
            *OPTIONAL* Timeout to run "tnpdump" command. Default: 300 (sec)

        :return:
            Return a DICT value have all archived tnpdump info, or return False

            For DICT value, if device working on StandardAlone mode, or working on HA mode but option 'node' is 0 or 1, will return DICT like below:

                {"cp_addr":     "...", "spu_addr_list":      ["spu1", "spu2"], "both_addr_list":   ["cp", "spu1", "spu2"]}

            If device working on HA mode and "node" is None, return DICT like:

                {
                    "node0":    {
                        "cp_addr":          "cp",
                        "spu_addr_list":    ["spu1", "spu2"],
                        "both_addr_list":   ["cp", "spu1", "spu2"],
                    },
                    "node1":    {
                        "cp_addr":          "cp",
                        "spu_addr_list":    ["spu1", "spu2"],
                        "both_addr_list":   ["cp", "spu1", "spu2"],
                    }
                }
        """
        func_name = self.get_current_function_name()

        options = {}
        options["force_get"] = force_get
        options["platform"] = platform
        options["node"] = node
        options["timeout"] = int(timeout)

        if options["node"] is not None:
            options["node"] = self._transit_node_alias(options["node"], mode="STR")

        if "tnpdump_info" not in self.runtime:
            self.runtime["tnpdump_info"] = {}

        # return immediatelly if have info in previous
        dev_keyword = str(self)
        if dev_keyword in self.runtime["tnpdump_info"] and options["force_get"] is False:
            if options["node"] is not None:
                return_value = self.runtime["tnpdump_info"][dev_keyword][options["node"]]
            else:
                return_value = self.runtime["tnpdump_info"][dev_keyword]

            self.log(message="Function {} return value:\n{}".format(func_name, self.pprint(return_value)), level="INFO")
            return return_value

        response = self.shell(command="tnpdump", timeout=options["timeout"]).response()
        ha_topo = self.is_ha()

        info = {}
        if options["platform"] is None:
            platform_type = self.get_platform_type().upper()
        else:
            platform_type = options["platform"].upper()

        if platform_type == "X86":
            if ha_topo is True:
                info["node0"] = {}
                info["node1"] = {}
                for line in response.splitlines():
                    match = re.search(r"(node\d+)\s+0x\d+", line)
                    if not match:
                        continue

                    node_name = match.group(1)
                    info[node_name]["cp_addr"] = "{}.fpc0".format(node_name)
                    info[node_name]["spu_addr_list"] = ["{}.fpc0".format(node_name), ]
                    info[node_name]["both_addr_list"] = ["{}.fpc0".format(node_name), ]
            else:
                info["cp_addr"] = "fpc0"
                info["spu_addr_list"] = ["fpc0", ]
                info["both_addr_list"] = ["fpc0", ]

        elif platform_type == "OCTEON":
            if ha_topo is True:
                for line in response.splitlines():
                    match = re.search(r"cluster\d+\.(node\d+)\s+(0[xX][0-9a-fA-F]+)\s+", line)
                    if not match:
                        continue

                    info[match.group(1)] = {
                        "cp_addr":          match.group(2),
                        "spu_addr_list":    [match.group(2), ],
                        "both_addr_list":   [match.group(2), ],
                    }
            else:
                info["cp_addr"] = "fwdd"
                info["spu_addr_list"] = ["fwdd", ]
                info["both_addr_list"] = ["fwdd", ]

        elif platform_type == "XLP":
            if ha_topo is True:
                info["node0"] = {}
                info["node1"] = {}
                info["node0"]["cp_addr"] = None
                info["node1"]["cp_addr"] = None
                info["node0"]["spu_addr_list"] = []
                info["node1"]["spu_addr_list"] = []
                info["node0"]["both_addr_list"] = []
                info["node1"]["both_addr_list"] = []

                for line in response.splitlines():
                    match = re.search(r"((node\d+)\.fpc\d+\.(pic\d+))\s+0[xX][0-9a-fA-F]+", line)
                    if not match:
                        continue

                    tnp_addr = match.group(1)
                    node_name = match.group(2)
                    pic_name = match.group(3)

                    if pic_name == "pic0" and info[node_name]["cp_addr"] is None:
                        info[node_name]["cp_addr"] = tnp_addr
                        info[node_name]["both_addr_list"].append(tnp_addr)
                        continue

                    info[node_name]["spu_addr_list"].append(tnp_addr)
                    info[node_name]["both_addr_list"].append(tnp_addr)

            else:
                info["cp_addr"] = None
                info["spu_addr_list"] = []
                info["both_addr_list"] = []

                for line in response.splitlines():
                    match = re.search(r"(fpc\d+\.(pic\d+))\s+0[xX][0-9a-fA-F]+", line)
                    if not match:
                        continue

                    tnp_addr = match.group(1)
                    pic_name = match.group(2)
                    if pic_name == "pic0" and info["cp_addr"] is None:
                        info["cp_addr"] = tnp_addr
                        info["both_addr_list"].append(tnp_addr)
                        continue

                    info["spu_addr_list"].append(tnp_addr)
                    info["both_addr_list"].append(tnp_addr)

        elif platform_type == "NFX150":     # PORTER3's PFE address is fpc1
            fpc_addr = "fpc1"

            if ha_topo is True:
                info["node0"] = {}
                info["node1"] = {}
                for line in response.splitlines():
                    match = re.search(r"(node\d+)\s+0x\d+", line)
                    if not match:
                        continue

                    node_name = match.group(1)
                    addr = ".".join([node_name, fpc_addr])

                    info[node_name]["cp_addr"] = addr
                    info[node_name]["spu_addr_list"] = [addr, ]
                    info[node_name]["both_addr_list"] = [addr, ]
            else:
                info["cp_addr"] = fpc_addr
                info["spu_addr_list"] = [fpc_addr, ]
                info["both_addr_list"] = [fpc_addr, ]

        else:
            self.log(message="{} unknown platform: {}".format(func_name, options["platform"]), level="ERROR")
            return False

        self.runtime["tnpdump_info"][dev_keyword] = info

        if options["node"] is not None:
            return_value = info[options["node"]]
        else:
            return_value = info

        self.log(message="Function {} return value:\n{}".format(func_name, self.pprint(return_value)), level="INFO")
        return return_value

    def check_feature_support(self, feature, timeout=300):
        """check device whether support specific feature

        This method get system license to check specific feature whether supported on device. Supported feature includes:

            +   "HE" - HighEnd series such as "SRX4100", "SRX4200", "SRX4600", "SRX5400", "SRX5600", "SRX5800", etc...

            +   "LE" - LowEnd (Branch) series. All platforms not in HE platform list.

            +   "MULTI_SPU" - Have multi-spu platform such as "SRX5400", "SRX5600", "SRX5800"

            +   "LSYS", "LD", "LOGICAL_SYSTEM", "LOGICAL_DOMAIN"

            +   "REMOTE_ACCESS_IPSEC_VPN", "IPSEC_VPN", "VPN"

            +   "VIRTUAL_APPLIANCE"

        All above feature keyword are case insensitive and "-" will be transited to "_", it means "Logical-System", "LOGICAL_SYSTEM",
        or "logical-system" are same.

        **Pay attention: This method only check whether have feature license, it means only checking feature "licensed" count >= 1 but never checking
        "used-license", "needed", "validity-type", etc... If want see license detail for specific feature, see
        jnpr.toby.security.system.system_license**

        :param STR|LIST|TUPLE feature:
            **REQUIRED** Feature STR or LIST. will checking them one by one.

        :param STR|INT timeout:
            *OPTIONAL* Timeout to get platform info. Default: 300

        :return:
            If device support all given features, return True, otherwise return False

        :example:
            status = self.feature_support_check(feature="LSYS")
            status = self.feature_support_check(feature=["HE", LSYS"])
        """
        self.log(message=self.title_msg(self.get_current_function_name()), level="INFO")

        # make sure all user feature element is uppercase and is LIST variable
        if isinstance(feature, (list, tuple)):
            feature_list = copy.deepcopy(feature)
        else:
            feature_list = (str(feature), )

        feature_list = self.list_element_to_uppercase(feature_list)

        options = {}
        options["timeout"] = int(timeout)

        supported_feature_list = (
            "HE", "HIGHEND", "HIGH_END",
            "LE", "LOWEND", "LOW_END",
            "MULTI_SPU", "MULTISPU",
            "LSYS", "LD", "LOGICAL_SYSTEM", "LOGICAL_DOMAIN",
            "REMOTE_ACCESS_IPSEC_VPN", "IPSEC_VPN", "VPN",
            "VIRTUAL_APPLIANCE",
            "IDP_SIG", "IDP_SIGNATURE",
            "APPID_SIG", "APPID_SIGNATURE",
        )
        # feature keyword validate checking
        msg = []
        for element in feature_list:
            if element not in supported_feature_list:
                msg.append("Feature name '{}' is not supported...\n".format(element))

        if msg:
            msg.append("Supported Feature List: {}\n".format(supported_feature_list))
            self.log(message="".join(msg), level="ERROR")
            return False

        # delete un-necessary license checking element to make sure whether need get license entry from device
        tmp_list = copy.deepcopy(feature_list)
        for no_license_element in ("HE", "HIGHEND", "HIGH_END", "LE", "LOWEND", "LOW_END", "MULTISPU", "MULTI_SPU"):
            if no_license_element in tmp_list:
                del tmp_list[tmp_list.index(no_license_element)]

        if tmp_list:
            device_license_list = jxmlease.parse_etree(
                self.cli(command="show system license usage", channel="pyez", format="xml", timeout=options["timeout"]).response()
            )

        multi_spu_platforms = ("SRX5400", "SRX5600", "SRX5800")
        high_end_platforms = ("SRX4100", "SRX4200", "SRX4600", "SRX5400", "SRX5600", "SRX5800")
        return_value = True
        msg = []

        ins_license = system_license()
        for element in feature_list:
            element = self.underscore_uppercase_transit(element)
            have_valid_license = False

            # highend, lowend checking
            if element in ("HE", "HIGHEND", "HIGH_END", "LE", "LOWEND", "LOW_END", "MULTI_SPU", "MULTISPU"):
                platform = self.current_node.current_controller.get_model()
                if not platform:
                    version_info = self.get_version_info()
                    if "node0" in version_info:
                        platform = version_info["node0"]["product_model"]
                    else:
                        platform = version_info["product_model"]

                platform = self.underscore_uppercase_transit(platform)
                if element in ("HE", "HIGHEND", "HIGH_END"):
                    have_valid_license = platform in high_end_platforms
                    if have_valid_license is True:
                        msg.append("Device '{}' is High-End platform".format(platform))
                    else:
                        msg.append("Device '{}' is not High-End platform".format(platform))
                        return_value = False
                elif element in ("MULTISPU", "MULTI_SPU"):
                    have_valid_license = platform in multi_spu_platforms
                    if have_valid_license is True:
                        msg.append("Device '{}' is MULTI_SPU platform".format(platform))
                    else:
                        msg.append("Device '{}' is not MULTI_SPU platform".format(platform))
                        return_value = False
                else:
                    have_valid_license = platform not in high_end_platforms
                    if have_valid_license is True:
                        msg.append("Device '{}' is Low-End platform".format(platform))
                    else:
                        msg.append("Device '{}' is not Low-End platform".format(platform))
                        return_value = False

                continue

            # for LSYS license
            elif element in ("LSYS", "LD", "LOGICAL_SYSTEM", "LOGICAL_DOMAIN"):
                have_valid_license = ins_license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name="logical-system",
                    licensed=(1, "ge"),
                )

            # VPN related license
            elif element in ("REMOTE_ACCESS_IPSEC_VPN", "IPSEC_VPN", "VPN"):
                have_valid_license = ins_license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name=("vpn", "in"),
                    licensed=(1, "ge"),
                )

            elif element in ("VIRTUAL_APPLIANCE", ):
                have_valid_license = ins_license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name="Virtual Appliance",
                    licensed=(1, "ge"),
                )

            elif element in ("IDP_SIG", "IDP_SIGNATURE"):
                have_valid_license = ins_license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name="idp-sig",
                    licensed=(1, "ge"),
                )

            elif element in ("APPID_SIG", "APPID_SIGNATURE"):
                have_valid_license = ins_license.search_license(
                    device_license_list=device_license_list,
                    match_from_previous_response=False,
                    name="appid-sig",
                    licensed=(1, "ge"),
                )

            else:   # pragma: no cover
                pass

            if have_valid_license:
                msg.append("Feature '{}' has supported on device".format(element))
            else:
                msg.append("Feature '{}' is not supported on device".format(element))
                return_value = False

        self.log(message="\n{}".format("\n".join(msg), level="INFO"))
        self.log(message="{} return value: {}".format(self.get_current_function_name(), return_value))

        return return_value

    def get_version_info(self, **kwargs):
        """Based on command "show version" to get device hostname, platform, image_info, etc...

        :param BOOL force_get:
            *OPTIONAL* Set True will send command to get info every time. If set False, only first
                       time send command to device. default: False

        :param INT|STR node:
            *OPTIONAL* Must be 0, 1, node0, node1 or BOTH. default: None

        :param INT timeout:
            *OPTIONAL* Timeout to run "show version" command. default: 60

        :return:
            Return a DICT value have all version info, or return False

            For DICT value, if device working on StandardAlone mode, or working on HA mode but option 'node' is 0 or 1, will return DICT like below:

                {"hostname":     "...", "version":      "..."}

            If device working on HA mode and "node" is None, return DICT like:

                {
                    "node0":    {
                        "hostname":         "...",
                        "version":          "...",
                        "package_comment":  "...",
                        "product_model":    "...",
                        "product_name":     "...",
                    },
                    "node1":    {
                        "hostname":         "...",
                        "version":          "...",
                        "package_comment":  "...",
                        "product_model":    "...",
                        "product_name":     "...",
                    }
                }
        """
        func_name = self.get_current_function_name()
        self.log(message=self.title_msg(func_name), level="INFO")

        options = {}
        options["force_get"] = kwargs.get("force_get", False)
        options["node"] = kwargs.get("node", None)
        options["timeout"] = int(kwargs.get("timeout", 60))

        if options["node"] is not None:
            options["node"] = self._transit_node_alias(options["node"], mode="STR")


        if "version_info" not in self.runtime:
            self.runtime["version_info"] = {}

        # If already have version info for specific device
        dev_keyword = str(self)
        if dev_keyword in self.runtime["version_info"] and options["force_get"] is False:
            if options["node"] is not None:
                node_name = options["node"]
                return_value = self.runtime["version_info"][dev_keyword][node_name]
            else:
                return_value = self.runtime["version_info"][dev_keyword]

            self.log(message="{} return value:\n{}".format(func_name, self.pprint(return_value)), level="INFO")
            return return_value

        # First time to get version info
        dev_response = self.cli(command="show version", format="xml", channel="pyez", timeout=options["timeout"]).response()
        xml_dict = jxmlease.parse_etree(dev_response)
        if "multi-routing-engine-results" in xml_dict:
            xml_dict = xml_dict["multi-routing-engine-results"]["multi-routing-engine-item"]

        # For HA, should a LIST that contain 2 node output, but sometimes node maybe lost that not a LIST
        # Even for SA, transit output to list
        if not isinstance(xml_dict, (list, tuple)):
            xml_dict = [xml_dict, ]

        info = {}
        for element in xml_dict:
            # Analyse HA return
            if "re-name" in element:
                node_name = str(element["re-name"])
                info[node_name] = {}
                info[node_name]["hostname"] = None
                info[node_name]["version"] = None
                info[node_name]["package_comment"] = None
                info[node_name]["product_model"] = None
                info[node_name]["product_name"] = None

                try:
                    info[node_name]["hostname"] = str(element["software-information"]["host-name"])
                    info[node_name]["version"] = str(element["software-information"]["junos-version"])
                    info[node_name]["package_information"] = str(element["software-information"]["package-information"])
                    info[node_name]["product_model"] = str(element["software-information"]["product-model"])
                    info[node_name]["product_name"] = str(element["software-information"]["product-name"])
                except KeyError:
                    pass

            # Analyse SA return
            else:
                info["hostname"] = None
                info["version"] = None
                info["package_comment"] = None
                info["product_model"] = None
                info["product_name"] = None

                try:
                    info["hostname"] = str(element["software-information"]["host-name"])
                    info["version"] = str(element["software-information"]["junos-version"])
                    info["package_comment"] = str(element["software-information"]["package-information"])
                    info["product_model"] = str(element["software-information"]["product-model"])
                    info["product_name"] = str(element["software-information"]["product-name"])
                except KeyError:
                    pass

        # restore for next time invoking
        self.runtime["version_info"][dev_keyword] = info

        if options["node"] is not None:
            node_name = options["node"]
            return_value = info[node_name]
        else:
            return_value = info

        self.log(message="{} return value:\n{}".format(func_name, self.pprint(return_value)), level="INFO")
        return return_value

    def reboot(self, **kwargs):
        """Reboot device and make sure all hardware component online

        As default, will use cmd "show chassis fpc pic-status" to show all components and they must online. In HA environment, will check 2
        nodes

        :param INT|STR wait:
            *OPTIONAL* Wait time to re-connect device. Default: 0 (sec)

        :param STR mode:
            *OPTIONAL* Rebooting mode that one of 'shell' or 'cli'. Default: 'cli'

                cli - 'request system reboot'
                shell - 'reboot'

        :param INT|STR timeout:
            *OPTIONAL* Timeout to reboot and reconnect device. Default: 480 (sec)

        :param INT|STR interval:
            *OPTIONAL* Re-connect check interval. Default: 20 (sec)

        :param STR device_type:
            *OPTIONAL* This option works only for 'cli' mode. Value should be set to 'vmhost' to reboot the vmhost

        :param STR system_nodes:
            *OPTIONAL* Values which can be passed: None, all-members, all, node0 or node1. Default: None

        :param BOOL all:
            *OPTIONAL* For HA setup, if set True, it means reboot all nodes, otherwise only reboot current node
                       For SA setup, will reboot current device whatever set True or False

                       This option's behavior is overlap to system_nodes, and have lower priority than system_nodes. For example:

                       + all=True, system_nodes=None: reboot 2 nodes
                       + all=True, system_nodes=node0: reboot node0
                       + all=False, system_nodes=None: reboot current nodes
                       + all=False, system_nodes=node1: reboot node1
                       + all=False, system_nodes=all: reboot 2 nodes

        :param BOOL on_parallel:
            *OPTIONAL* parallel reboot all DUT. default: None

                +  for 1 device, rebooting it as normal
                +  for 2+ devices, rebooting device on parallel as default.
                +  if on_parallel set True or False, force rebooting device on or not on parallel

            **Pay attention:** parallel reboot device will no reboot processing output logged.

        :return: Return True if all rebooting success, otherwise return False
        """
        func_name = self.get_current_function_name()
        self.log(message=self.title_msg(func_name), level="INFO")

        options = {}
        options['wait'] = int(kwargs.pop('wait', 0))
        options['timeout'] = int(kwargs.pop('timeout', 480))
        options['mode'] = kwargs.pop('mode', "cli")
        options["interval"] = int(kwargs.pop("interval", 20))
        options["device_type"] = kwargs.pop("device_type", None)
        options["system_nodes"] = str(kwargs.pop("system_nodes", None)).upper()
        options["all"] = str(kwargs.pop("all", False)).upper()
        options["on_parallel"] = kwargs.pop("on_parallel", None)

        ha_topo = self.is_ha()
        if ha_topo is True:
            if options["all"] == "FALSE":
                options["device"] = (self.current_node.current_controller, )
            elif options["all"] == "TRUE":
                options["device"] = (self.node0, self.node1)

            # if system_nodes=None (default), option 'all' will take effect
            if options["system_nodes"] == "NONE":
                pass
            elif options["system_nodes"] in ("ALL", "ALL-MEMBERS", "ALL_MEMBERS"):
                options["device"] = (self.node0, self.node1)
            elif options["system_nodes"] in ("NODE0", "0"):
                options["device"] = (self.node0, )
            elif options["system_nodes"] in ("NODE1", "1"):
                options["device"] = (self.node1, )
            else:
                raise ValueError("option 'system_nodes' must one of 'None', 'all-members', 'all', 'node0', "
                                 "'node1', '0' or '1' but got '{}'".format(options["system_nodes"]))

        else:
            options["device"] = (self.current_node.current_controller, )

        # For HA environment, reboot 2 nodes in parallel as default
        if options["on_parallel"] is None and len(options["device"]) >= 2:
            options["on_parallel"] = True
        else:
            options["on_parallel"] = False

        reboot_result_list = []
        if options["on_parallel"] is False:
            for dev in options["device"]:
                self.log(message="rebooting '{}' ...".format(dev), level="INFO")
                reboot_result_list.append(dev.reboot(
                    wait=options["wait"],
                    timeout=options["timeout"],
                    interval=options["interval"],
                    mode=options["mode"],
                    device_type=options["device_type"],
                ))
        else:
            list_of_dicts = []
            for dev in options["device"]:
                list_of_dicts.append({
                    "fname": dev.reboot,
                    "kwargs": {
                        "wait": options["wait"],
                        "timeout": options["timeout"],
                        "interval": options["interval"],
                        "mode": options["mode"],
                        "device_type": options["device_type"],
                    }
                })

            self.log(message="parallel rebooting '{}' ...".format(options["device"]))
            reboot_result_list = run_multiple(list_of_dicts)
            self.log(message="all device reboot status: {}".format(reboot_result_list), level="INFO")

        return_value = False not in reboot_result_list and len(reboot_result_list) == len(options["device"])
        self.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value


def get_platform_type(device):
    """
        Returns the platform type based on the architecture
        Example:
            ${response} = get Platform type    device=${device-handle}

        :params device:
            *REQUIRED* Device handle of which platform type has to be found
        :return: Returns octeon/x86/xlp
        :rtype: str
    """
    return device.get_platform_type()
