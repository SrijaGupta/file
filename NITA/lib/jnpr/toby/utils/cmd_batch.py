"""
    Utility which allows users to execute a series of batch operations
    Author: jhayes
"""
#disabling import error because they load fine
import builtins # pylint: disable=import-error
import ruamel.yaml as yaml # pylint: disable=import-error
import re
from jnpr.toby.hldcl.device import execute_cli_command_on_device as cli
from jnpr.toby.hldcl.device import execute_config_command_on_device as config
from jnpr.toby.hldcl.device import execute_shell_command_on_device as shell
from jnpr.toby.hldcl.device import execute_vty_command_on_device as vty
from jnpr.toby.hldcl.device import execute_cty_command_on_device as cty
from jnpr.toby.hldcl.device import execute_pyez_command_on_device as pyez
from jnpr.toby.hldcl.device import execute_rpc_command_on_device as rpc
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.logger.logger import get_log_dir
from io import StringIO
import sys

class TobyCmdBatch(object):
    '''
        TobyCmdBatch Class
    '''
    def __init__(self):
        '''
            Initialize TobyCmdBatch objct
        '''
        self.templates = None
        self.current_handle = None
        self.scp_handles = []
        if not hasattr(builtins, 't'):
            raise TobyException('Toby has not been initialized. \n' + \
                                'Please import init from jnpr.toby.init.init, ' + \
                                'instantiate an init object, and run method Initialize\n')

    def load_templates(self, template_file):
        '''
            Load templates files with commands into memory
            param: template_file
                   name of file containing command templates
        '''
        self.templates = yaml.safe_load(open(template_file))

    def run_commands(self, template):
        '''
            Run particular template in templates file
            param: template
                   name of template
        '''
        if template not in self.templates:
            raise TobyException("Template " + template + " not found.")
        batch_set = self.templates[template]
        if type(batch_set) is not list:
            raise TobyException("Malformed template file. First level of template " + template + " should be a list")
        for instr_set in batch_set:
            if 'commands' not in instr_set:
                raise TobyException("Missing 'commands' key in one of the batch sets for template " + template + ".")
            commands = instr_set['commands']
            if type(commands) is not list:
                raise TobyException("Error in template " + template + ". 'commands' should be a list.")
            resource_list = []
            if 'tags' in instr_set:
                resource_list = t.get_resource_list(tag=instr_set['tags'])
            else:
                resource_list = t.get_resource_list()
            for resource in resource_list:
                resource_osname = t['resources'][resource]['system']['primary']['osname']
                if 'osname' in instr_set and instr_set['osname'].upper() != resource_osname.upper():
                    t.log_console("Skipping resource " + resource + ": OS '" + resource_osname + \
                          "' does not match template '" + template + "' filter '" + instr_set['osname'] + "'")
                    continue
                try:
                    self.current_handle = t.get_handle(resource=resource)
                except Exception:
                    continue
                for command in commands:
                    if not re.match(r'^\S+\(', command):
                        raise TobyException("Malformed command: " + command + "\nShould resemble: cli(show version)")
                    t.log_console("Running command " + command + " on resource " + resource + "...")
                    command = command.replace(')', '')
                    instr, cmd = command.split('(')
                    response = None
                    if instr == 'config':
                        response = config(self.current_handle, command_list=[cmd])
                    elif instr == 'cli':
                        response = cli(self.current_handle, command=cmd)
                    elif instr == 'shell':
                        response = shell(self.current_handle, command=cmd)
                    elif instr == 'cty':
                        dest, cmd = cmd.split(':')
                        response = cty(self.current_handle, destination=dest, command=cmd)
                    elif instr == 'vty':
                        dest, cmd = cmd.split(':')
                        response = vty(self.current_handle, destination=dest, command=cmd)
                    elif instr == 'rpc':
                        response = rpc(self.current_handle, command=cmd)
                    elif instr == 'pyez':
                        response = pyez(self.current_handle, command=cmd)
                    elif instr == 'get_file':
                        stdout_orig = sys.stdout
                        sys.stdout = StringIO()
                        status = self.current_handle.download(remote_file=cmd, local_file=get_log_dir())
                        sys.stdout = stdout_orig
                        if status:
                            response = "File " + cmd + " retrieved and saved to " + get_log_dir() + "\n"
                        else:
                            response = "File " + cmd + " retrieval failed\n"
                    else:
                        t.log_console('Instruction ' + instr + ' not supported (skipping)')
                    if response:
                        t.log_console("Command " + command + " executed successfully and results logged")
