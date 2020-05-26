"""
    clearing logs and stats before each test case
    and pulling logs and stats at the end of each
    test case
"""
import os
from jnpr.toby.utils.scp import SCP
from jnpr.toby.logger.logger import get_log_dir
from robot.libraries.BuiltIn import BuiltIn
from jnpr.toby.frameworkDefaults.credentials import get_credentials

def get_logs_and_stats_after_test(all_controller_handles_dict):
    """
        pulling logs and stats at the end of each
        test case
    """
    t.log("entering get logs and stats after test")
    logdir = get_log_dir()
    test_case = BuiltIn().get_variable_value('${TEST NAME}')
    logdir = logdir+'/'+test_case
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    for key in all_controller_handles_dict:
        t.log(all_controller_handles_dict)
        controller_handle = all_controller_handles_dict[key]
        username, passwrd = get_credentials(os='JUNOS')
        scp_obj = SCP(host=controller_handle.host, user=username, password=passwrd)
        scp_obj.get_file('/var/log/messages', logdir +'/'+'%s_messages.messages' % (key))
        if controller_handle.is_master():
            op = controller_handle.shell(command="ps | grep rtsockmon").response()
            flag = 0
            for line in op.splitlines():
                line = line.strip()
                if 'rtsockmon -rt' in line:
                    pid = line.split(' ')[0]
                if pid:
                    controller_handle.shell(command="kill -9 "+ pid).response()
                    flag = 1
            if flag == 0:
                controller_handle.log("\nprocess is not running")
            scp_obj = SCP(host=controller_handle.host, user=username, password=passwrd)
            scp_obj.get_file('/var/log/%s_rtsockmon.txt' % (key), logdir +'/'+'%s_rtsockmon.log' % (key))
        controller_handle.cli(command="request support information | save /var/log/%s_req_sup_info.log" % (key)).response()
        scp_obj = SCP(host=controller_handle.host, user=username, password=passwrd)
        scp_obj.get_file('/var/log/%s_req_sup_info.log' % (key), logdir +'/'+'%s_req_sup_info.log' % (key))
    t.log("exiting get logs and stats after test")

def clear_logs_and_stats_before_test(all_controller_handles_dict, cli_command_list=None, shell_command_list=None):
    """
        clearing logs and stats before each test case
    """
    t.log("entering clearing logs and stats before test")
    t.log(all_controller_handles_dict)
    for key in all_controller_handles_dict:
        controller_handle = all_controller_handles_dict[key]
        if controller_handle.is_master():
            controller_handle.cli(command="clear interface statistics all").response()
            controller_handle.cli(command="clear pfe statistics traffic").response()
            controller_handle.shell(command="rm -rf /var/log/%s_rtsockmon.txt" % (key)).response()
            controller_handle.shell(command="rtsockmon -rt > /var/log/%s_rtsockmon.txt &" % (key)).response()
            if cli_command_list != None:
                for cmd in cli_command_list:
                    cmd = cmd.strip('\"')
                    controller_handle.cli(command=cmd).response()
            if shell_command_list != None:
                for cmd in shell_command_list:
                    cmd = cmd.strip('\"')
                    controller_handle.shell(command=cmd).response()
        controller_handle.cli(command="clear log messages").response()
    t.log("exiting clearing logs and stats before test")

def get_all_handles(resource_list=None):
    """
        getting all valid controller handles in t['resources'] or passed argument resource_list
    """
    t.log("getting all valid controller handles")
    controller_handle_dict = {}
    if resource_list == None:
        for resource in t['resources']:
            for system_node in t['resources'][resource]['system']:
                if system_node != 'dh':
                    if t['resources'][resource]['system'][system_node]['osname'].upper() == 'JUNOS':
                        for controller in t['resources'][resource]['system'][system_node]['controllers']:
                            if controller in t['resources'][resource]['system']['dh'].nodes[system_node].controllers:
                                try:
                                    controller_handle = t.get_handle(resource=resource, system_node=system_node, controller=controller)
                                    key = resource.strip('\'')+'_'+system_node.strip('\'')+'_'+controller.strip('\'')
                                    controller_handle_dict[key] = controller_handle
                                except Exception:
                                    t.log("Resource=%s System_Node=%s Controller=%s not used during this test suite execution" % (resource, system_node, controller))
    else:
        for resource in resource_list:
            for system_node in t['resources'][resource]['system']:
                if system_node != 'dh':
                    if t['resources'][resource]['system'][system_node]['osname'].upper() == 'JUNOS':
                        for controller in t['resources'][resource]['system'][system_node]['controllers']:
                            if controller in t['resources'][resource]['system']['dh'].nodes[system_node].controllers:
                                try:
                                    controller_handle = t.get_handle(resource=resource, system_node=system_node, controller=controller)
                                    key = resource.strip('\'')+'_'+system_node.strip('\'')+'_'+controller.strip('\'')
                                    controller_handle_dict[key] = controller_handle
                                except Exception:
                                    t.log("Resource=%s System_Node=%s Controller=%s not used during this test suite execution" % (resource, system_node, controller))
    t.log(controller_handle_dict)
    return controller_handle_dict
