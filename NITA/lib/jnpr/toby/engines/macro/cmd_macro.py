"""
    Utility which allows users to execute a series of batch operations
    Author: jhayes
"""
#disabling import error because they load fine
import builtins # pylint: disable=import-error
import ruamel.yaml as yaml # pylint: disable=import-error
import re
import os
import logging
import subprocess
import datetime
import time
import requests
import json
import sys
from jnpr.toby.hldcl.device import execute_cli_command_on_device as cli
from jnpr.toby.hldcl.device import execute_shell_command_on_device as shell
from jnpr.toby.hldcl.device import execute_vty_command_on_device as vty
from jnpr.toby.hldcl.device import execute_cty_command_on_device as cty
from jnpr.toby.hldcl.device import execute_config_command_on_device as config
from jnpr.toby.hldcl.device import execute_pyez_command_on_device as pyez
from jnpr.toby.hldcl.device import execute_rpc_command_on_device as rpc
from jnpr.toby.hldcl.device import execute_command_on_device as execute_custom_mode
from jnpr.toby.hldcl.trafficgen.trafficgen import execute_tester_command as Tester
from jnpr.toby.utils.Vars import Vars

from jnpr.toby.hldcl.device import add_mode
from jnpr.toby.hldcl.device import detect_core
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.logger.logger import get_log_dir
from io import StringIO
from robot.libraries.BuiltIn import BuiltIn
from ast import literal_eval
import urllib3
from jnpr.toby.utils.utils import log_file_version


# pylint: disable=unidiomatic-typecheck
### Class ###
class cmd_macro(object): # pylint: disable=too-few-public-methods
    '''
        TobyCmdBatch Class
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        '''
            Initialize TobyCmdBatch object
        '''
        self.target_macros = []
        self.nested_macros = {}
        self.all_macro_libs = {}
        self.completed_macros = {}
        self.handles = {}
        self.current_resources = None
        self.robot_vars = {}
        self.local_vars = {}
        self.loggers = {}
        self.current_time = None
        self.core_collect = {}
        self.log_files = []
        self.core_check_wait = True
        self.addon_constraints = {}
        self.user_targets = {}
        self.custom_modes = {}
        self.comments = {}
        self.verbosity = 'low'
        self.log_prefix = ''
        ## for callback show_chassis_hardware
        self.resources_modules = {}

    ### Robot Keyword ###
    def run_macros_on_failure(self, macro_lib, macro, message=None, resources='all', targets='{}', **kwargs):
        '''
            Run Macros On Failure    Keyword
        '''
        BuiltIn().set_suite_variable('${macro_engine}', True)
        BuiltIn().set_suite_variable('${macro_lib}', macro_lib)
        BuiltIn().set_suite_variable('${macro}', macro)
        BuiltIn().set_suite_variable('${macro_resources}', resources)
        #t.log_console("From within run_macros_on_failure ..." + str(targets))
        BuiltIn().set_suite_variable('${macro_targets}', str(targets))
        BuiltIn().set_suite_variable('${macro_message}', message)
        BuiltIn().set_suite_variable('${macro_already_run}', False)

        for kwarg in kwargs:
            BuiltIn().set_suite_variable('${' + kwarg + '}', kwargs[kwarg])

    def load_macros(self, macro_lib, variables=None, verbosity='low'):
        '''
            Load macro files with commands into memory
            param: macro_file
                   name of file containing command macros
        '''
        if not hasattr(builtins, 't'):
            raise TobyException('Toby has not been initialized. \n' + \
                                'Please import init from jnpr.toby.init.init, ' + \
                                'instantiate an init object, and run method Initialize\n')

        # Set verbosity
        self.verbosity = verbosity
        # Gather macros and import new user-defined constraints
        macro_files = macro_lib.split(':')
        for macro_file in macro_files:
            log_file_version(macro_file)
            abs_file_path = os.path.dirname(macro_file)
            with open(macro_file) as file_content:
                macro_file_dict = yaml.safe_load(file_content)
                if not 'filetype' in macro_file_dict:
                    raise TobyException("Missing 'filetype:<macro_lib|constraint>' key in macro file '" + macro_file + "'.")
                if macro_file_dict['filetype'] == 'macro_lib':
                    del macro_file_dict['filetype']
                    if 'import' in macro_file_dict:
                        for filename in macro_file_dict['import']:
                            if filename.startswith('/'):
                                macro_files.append(filename)
                            else: #use relative path to original macro file
                                macro_files.append(abs_file_path + '/' + filename)
                        del macro_file_dict['import']
                    self.all_macro_libs.update(macro_file_dict)
                elif macro_file_dict['filetype'] == 'constraint':
                    del macro_file_dict['filetype']
                    for constraint in macro_file_dict:
                        self.addon_constraints[constraint] = macro_file_dict[constraint]

        # Gather variables
        if 'vars' in self.all_macro_libs:
            self.local_vars = self.all_macro_libs['vars']
            del self.all_macro_libs['vars']
        if variables: # append additional variables
            self.local_vars.update(variables)

    def run_macros(self, macros, resources, message=None, targets='{}'):
        '''
            Run particular macros in macro_lib file
            param: macros
                   name of macros (colon delimited)
        '''
        self.completed_macros = {}

        if "=" in macros:
            t.log_console("No macros specified")
            self.__log("No macros specified")
            return

        # Get the testcase name from Robot Builtin library
        testname = None
        try:
            testname = Vars().get_global_variable('${TEST NAME}')
            testname = testname.replace (" ", "_")
            testname = testname + '_'
        except Exception:
            testname = ""

        # acquire time for timestamping
        dtime = datetime.datetime.now()
        self.current_time = str(dtime.year) \
             + '{:02.0f}'.format(dtime.month) \
             + '{:02.0f}'.format(dtime.day) \
             + '-' \
             + '{:02.0f}'.format(dtime.hour) \
             + '{:02.0f}'.format(dtime.minute) \
             + '{:02.0f}'.format(dtime.second)

        # create general default logger
        self.log_prefix = testname + self.current_time
        general_log_dir = get_log_dir() + '/macro_logs/' + testname + self.current_time
        os.makedirs(general_log_dir)
        self.loggers['default'] = self.__setup_logger('default', general_log_dir + '/result.log')
        self.log_files.append(general_log_dir + '/result.log')

        BuiltIn().log(level='INFO', message="Macro Engine employed. <a href=macro_logs/ target=_blank>Macro Engine Logs</a>", html=True)

        if not self.all_macro_libs:
            t.log_console("No macro libraries loaded.")
            self.__log("No macro libraries loaded.")
            return

        #reconsistute targets dictionary into true dictionary since Robot only allows scalar variables
        targets = literal_eval(targets)

        #gather master resource list
        resource_lst = None
        if type(resources) is list:
            resource_lst = resources
        elif resources != 'all':
            resource_lst = resources.split(':')
        else: #get all resources
            resource_lst = t.get_resource_list()

        self.current_resources = resource_lst

        # prep each resource
        for resource in resource_lst:
            #ensure resource handle is still connected and gracefully reconnect if not connected
            try:
                self.handles[resource] = t.get_handle(resource=resource)
                self.handles[resource].reconnect(force=False)
            except Exception:
                self.__log("Skipping resource " + resource + ". Connection lost.")
                if resource in self.handles:
                    del self.handles[resource]
                continue
            #set up logging
            resource_name = t['resources'][resource]['system']['primary']['name']
            log_dir = get_log_dir() + '/macro_logs/' + self.log_prefix + '/' + resource_name
            os.makedirs(log_dir)
            self.loggers[resource] = self.__setup_logger(resource, log_dir + '/' + resource_name + "_result.log")
            self.log_files.append(log_dir + '/' + resource_name + "_result.log")
            #user defined targets
            if resource in targets:
                self.user_targets[resource] = targets[resource]

        # Gather robot variables
        try:
            self.robot_vars = BuiltIn().get_variables()
        except Exception:
            # no robot running
            self.__log("Robot Variables unavailable")

        all_macro_libs_yaml = yaml.dump(self.all_macro_libs)
#        t.log_console(all_macro_libs_yaml)
        all_macro_libs_yaml = self.__process_vars(all_macro_libs_yaml)
        all_macro_libs_yaml = self.__process_file_vars(all_macro_libs_yaml)
        self.all_macro_libs = yaml.safe_load(all_macro_libs_yaml)
#        t.log_console(yaml.dump(self.all_macro_libs))

        self.__log('Processing macros...')
        if message:
            self.__log('Message: ' + message)

        macro_lst = macros.split(':')
        for macro in macro_lst:
            if macro not in self.all_macro_libs:
                self.__log("Macro " + macro + " not found.")
            else:
                self.target_macros.append(macro)


        t.log_console("Processing macro(s) " + str(self.target_macros) + "...\n")

        while self.target_macros:
            macro = self.target_macros.pop(0)
            if macro not in self.completed_macros:
                macro_content = self.all_macro_libs[macro]
                if type(macro_content) is dict:
                    self.__log("Processing macro " + macro + "... ")
                    self.__run_single_macro(macro, macro_content)
                    self.__log("Completed macro " + macro + "... ")
                    self.completed_macros[macro] = 'complete'
                elif type(macro_content) is list:
                    for i in range(0, len(macro_content)):
                        self.__log("Processing macro " + macro + "[" + str(i+1) + "]... ")
                        self.__run_single_macro(macro, macro_content[i])
                        self.__log("Completed macro " + macro + "[" + str(i+1) + "]... ")
                    self.completed_macros[macro] = 'complete'
                else:
                    t.log_console("Macro content is of type " + str(type(macro_content)))

        if self.core_collect:
            self.__core_collect()

        # clean up loggers and log files
        for logger_name in self.loggers:
            log = logging.getLogger(logger_name)
            handlers = list(log.handlers)
            for handle in handlers:
                log.removeHandler(handle)
                handle.flush()
                handle.close()
        for log_file in self.log_files:
            with open(log_file, 'r') as fhandle:
                new_log_content = fhandle.read().replace('\r', '')
            fhandle.close()
            with open(log_file, 'w') as fhandle:
                fhandle.write(new_log_content)
            fhandle.close()

    def __run_single_macro(self, macro, macro_content):
        '''
            Run one macro
        '''
        commands = None #dict or list
        constraints = {}

        #iterate through outer loop (content nested within macro)
        for instr_type in macro_content:
            if instr_type not in ['comment', 'constraints', 'commands', 'macros', 'system', 'target']:
                message = "Unsupported instr_type '" + instr_type + "'. Only 'commands', 'macros' & 'system' are supported."
                t.log_console(message)
                self.__log(message)
                return
            if instr_type == 'macros':
                macros = macro_content[instr_type]
                if type(macros) is not list:
                    raise TobyException("Error in macro " + macro + ". 'macros' should be a list.")
                for nested_macro in reversed(macros):
                    if nested_macro in self.target_macros or nested_macro in self.completed_macros:
                        self.__log("Loop in macro definitions. Skipping macro " + nested_macro + " since it was already run")
                        continue
                    self.target_macros.insert(0, nested_macro)
                if 'commands' not in macro_content:
                    self.__log("Completed macro " + macro + " [additionally queued macros: " + str(macros) + "]")
                    # this was just a macro of macros and nothing else, so return
                    return
#            #remove for now - may be a bit too dangerous
#            elif instr_type == 'system':
#                system_calls = macro_content[instr_type]
#                if type(system_calls) is not list:
#                    raise TobyException("Error in system " + system_calls + ". 'system' should be a list.")
#                for system_call in system_calls:
#                    system_response = self.__system(system_call)
#                    self.__log("Local System Call:\n>>> " + system_call + "\n" + system_response + "\n")
#                self.__log('Completed macro:' + macro)
#                # system call is local, so no need to look at resource information or process commands
#                return
            elif instr_type == 'commands':
                commands = macro_content[instr_type]
                if type(commands) is not list and type(commands) is not dict:
                    raise TobyException("Malformated macro " + macro + ". 'commands' syntax incorrect")
            elif instr_type == 'constraints':
                constraints = macro_content['constraints']
                if type(constraints) is not dict:
                    raise TobyException("Error in macro " + macro + ". 'constraints' should be a dictionary (no dashes).")
            elif instr_type == 'comment':
                self.comments[macro] = str(macro_content['comment'])
            else:
                # if no commands, and nested macros already processed, then nothing to do
                continue

        resources = self.current_resources
        resources_tagged = []

        #Get intersection of resources if 'tag' provided by user
        if 'params' in constraints and 'tags' in constraints['params']:
            resources_tagged = t.get_resource_list(tag=constraints['params']['tags'])
            resources = [value for value in resources if value in resources_tagged]

        # fill in custom user constraints from outside imports (ex: chipset)
        if constraints:
            self.__fill_addon_constraints(constraints)

        #Filter out resource based on 'constraints->resources' stanza
        if constraints and 'resources' in constraints:
            resource_constraints = constraints['resources']
            new_resources = []
            for resource in resources:
                match = True
                failed_constraint = ''
                for key, constraint in resource_constraints.items():
                    if key in t['resources'][resource]['system']['primary'] and key != 'tags':
                        params_value = t['resources'][resource]['system']['primary'][key]
                        if type(constraint) is list:
                            if params_value not in constraint:
                                match = False
                        elif params_value.upper() != constraint.upper():
                            match = False
                        if match is False:
                            failed_constraint += key + ','
                if match:
                    new_resources.append(resource)
                else:
                    self.__log("Skipping resource " + resource + ". Filter constraint for macro " + macro + "\n" + failed_constraint)
            resources = new_resources

        for resource in resources:
            target_lst = {}
            resource_name = t['resources'][resource]['system']['primary']['name']
            self.__log('Processing macro:' + macro + ',resource:' + resource + '(' + resource_name + ")\n", resource)
            t.log_console('Processing macro:' + macro + ',resource:' + resource + '(' + resource_name + ")\n")

            #Filter out targets based on 'constraints->targets' stanza
            if constraints and 'targets' in constraints:
                target_constraints = constraints['targets']
                for mode, target in target_constraints.items(): # ex: 'part-number', (big list of part numbers)
                    #t.log_console("Mode: " + mode + ", target: " + str(target))
                    if type(target) is str:
                        if 'var_unknown' in target:
                            #original macro had a var[] that was not satisfied
                            target = target.replace('var_unknown(', '')
                            target = target.replace(')', '')
                            self.__log("Variable var[" + target + "] undefined.")
                            target_lst[mode] = []
                            continue
                        else:
                            targets = target.split(',')
                            target_lst[mode] = targets
                    if type(target) is dict: #user is filtering - check for 'function' key
                        if 'function' not in target:
                            self.__log("Skipping resource macro " + macro + ". 'function' missing from constraint target " + mode)
                            #t.log_console("Skipping resource macro " + macro + ". 'function' missing from constraint target " + mode)
                            continue
                        callback = getattr(self, target['function'])
                        #t.log_console("Target before callback is " + str(target))
                        target_lst[mode] = callback(mode=mode, resource=resource, **target)
                    elif type(target) is list: #user is supplying simply a list of targets (ex: fpc1, fpc2, etc.)
                        target_lst[mode] = target

            if macro in self.comments:
                self.__log("\n" + self.comments[macro], resource)

            #Standardize command format
            final_commands = []
            if type(commands) is not dict: #cli() style format
                new_commands = {}
                for command in commands:
                    command = command.replace(')', '')
                    command_type, cmd = command.split('(')
                    if not cmd:
                        cmd = ''
                    if command_type in commands:
                        new_commands[command_type].append(cmd)
                    else:
                        new_commands[command_type] = [cmd]
                commands = new_commands

            for command_type in commands.keys():
                for command in commands[command_type]:
                    if command_type in target_lst:
                        for target in target_lst[command_type]:
                            final_commands.append({'mode':command_type, 'target':target, 'cmd':command})
                    else:
                        final_commands.append({'mode':command_type, 'cmd':command})

            # and finally, run commands
            for command in final_commands:
                if self.verbosity in ['medium', 'high']:
                    t.log_console("Running Command " + str(command) + " on resource " + resource)
                # for debug, put 'continue' here as needed
                # check for unassigned variables
                match_obj = re.search(r'(var_unknown|file)\[\'?[a-zA-Z0-9_]*\'?\]', str(command))
                if match_obj:
                    match = match_obj.group(0)
                    self.__log('Skipping command ' + str(command) + ' due to unassigned variable ' + match)
                    continue

                # try running a command
                response = None
                try:
                    #self.__log(resource + "(" + resource_name + ")" + " Running " + command['mode'] + ':' + str(command['cmd']))
                    if command['mode'] == 'cli':
                        response = cli(self.handles[resource], command=command['cmd'])
                    elif command['mode'] == 'config':
                        response = config(self.handles[resource], command_list=[command['cmd']], commit=True)
                    elif command['mode'] == 'shell':
                        response = shell(self.handles[resource], command=command['cmd'])
                    elif command['mode'] == 'cty':
                        response = cty(self.handles[resource], destination=command['target'], command=command['cmd'])
                    elif command['mode'] == 'vty':
                        response = vty(self.handles[resource], destination=command['target'], command=command['cmd'])
                    elif command['mode'] == 'cli-pfe':
                        if not resource in self.custom_modes:
                            self.custom_modes[resource] = {}
                        if 'cli-pfe' not in self.custom_modes[resource]:
                            try:
                                self.custom_modes[resource]['cli-pfe'] = \
                                    add_mode(self.handles[resource], mode='cli-pfe', command='cli-pfe', pattern='>', exit_command='exit')
                            except Exception:
                                self.custom_modes[resource]['cli-pfe'] = False
                        if self.custom_modes[resource]['cli-pfe']:
                            response = execute_custom_mode(self.handles[resource], mode='cli-pfe', command=command['cmd'])
                        else:
                            response = "Skipping cli-pfe command " + command['cmd'] + " (no cli-pfe available)"
                    elif command['mode'] == 'rpc':
                        response = rpc(self.handles[resource], command=command['cmd'])
                    elif command['mode'] == 'pyez':
                        response = pyez(self.handles[resource], command=command['cmd'])
#                    elif command['mode'] == 'cli-pfe':
#                        response = vty(self.handles[resource], destination=command['target'], command=command['cmd'], timeout=10)
                    elif command['mode'] == 'rest':
                        response = self._rest_call(command=command)
                    elif command['mode'] == 'fetch_cores':
                        self.core_collect[resource] = 1
                    elif command['mode'] == 'get_file':
                        stdout_orig = sys.stdout
                        sys.stdout = StringIO()
                        try:
                            log_dir = get_log_dir() + '/macro_logs/' + self.log_prefix + '/' + resource_name
                            status = self.handles[resource].download(remote_file=command['cmd'], local_file=log_dir)
                        except Exception:
                            status = False
                        sys.stdout = stdout_orig
                        if status:
                            response = "File " + command['cmd'] + " retrieved and saved to " + log_dir
                        else:
                            response = "File " + command['cmd'] + " retrieval failed"
                    else:
                        self.__log('Instruction ' + command['mode'] + ' not supported (skipping)')
                    log_message = "\n" + resource_name
                    if 'target' in command:
                        log_message += '(' + command['target'] + ')'
                    log_message += ' ' + command['mode'] + "> " + str(command['cmd']) + "\n" + response + "\n"
                    self.__log(log_message, resource)
                except Exception as error:
                    log_message = 'Command ' + str(command) + ' failed on resource ' + resource + '(' + resource_name + ')'
                    if response:
                        log_message += ' with response ' + response
                    log_message += ' and an exception error [' + str(error) + ']'
                    self.__log(log_message)
                    continue
            #self.__log('Completed macro:' + macro + ',resource:' + resource)
            #self.__log('Completed macro:' + macro + ',resource:' + resource, resource)
        #self.__log("Completed macro " + macro)

    def __core_collect(self):
        '''
            Run one macro
        '''
        self.core_check_wait = True
        for resource in self.core_collect:
            resource_name = t['resources'][resource]['system']['primary']['name']
            hostname = t['resources'][resource]['system']['primary']['controllers']['re0']['hostname']
            log_dir = get_log_dir() + '/macro_logs/' + self.log_prefix + '/' + resource_name
            if self.core_check_wait:
                #need something more sophisticated, but for now, 45 seconds for demo
                time.sleep(45)
                self.core_check_wait = False
            #self.__log("Searching for cores on resource" + resource)
            response = detect_core(self.handles[resource])
            if response:
                status = False
                stdout_orig = sys.stdout
                sys.stdout = StringIO()
                for stage in t.core.keys():
                    for controller in t.core[stage][hostname].keys():
                        core = t.core[stage][hostname][controller]['core_src_path'] + \
                            t.core[stage][hostname][controller]['core_name']
                        self.__log("Found core at resource " + resource_name + "(" + controller + "):" + core, resource)
                        try:
                            status = self.handles[resource].download(remote_file=core, local_file=log_dir)
                            folders_file = core.split(sep='/')
                            os.system('chmod 664 ' + log_dir + '/' + folders_file[-1])
                        except Exception:
                            self.__log("Unable to copy core " + core + " from resource " + resource_name + " to " + log_dir)
                if status:
                    response = "Core(s) retrieved and saved to " + log_dir
                else:
                    response = "Core retrieval failed"
                sys.stdout = stdout_orig
            else:
                response = "No Core found"
            self.__log("Core detection response for resource " + resource + ": " + str(response), resource)


    def __process_vars(self, macro_lib):
        '''
            process vars
        '''
        match_obj = True
        while match_obj:
            match_obj = re.search(r'\'?var\[\'?([a-zA-Z0-9_\-]*)\'?\]\'?', macro_lib)
            if match_obj:
                match = match_obj.group(0)
                value = None
                if '${' + match_obj.group(1) + '}' in self.robot_vars:
                    value = self.robot_vars['${' + match_obj.group(1) + '}']
                elif match_obj.group(1) in self.local_vars:
                    value = self.local_vars[match_obj.group(1)]
                else:
                    try:
                        value = tv[match_obj.group(1)] # pylint: disable=undefined-variable
                    except Exception:
                        pass
                if not value:
                    self.__log('Variable ' + match_obj.group(1) + ' does not exist')
                    value = 'var_unknown(' + match_obj.group(1) + ')'
                    match_obj = False
                value = str(value)
                macro_lib = macro_lib.replace(match, value)
#        macro_lib = macro_lib.replace('var_unknown', 'var')
        return macro_lib

    def __fill_addon_constraints(self, constraint_set):  # chipset = ichip
        '''
            fill addon constraints
        '''
        for constraint_key in constraint_set: # vty or model
            if type(constraint_set[constraint_key]) is dict:
                self.__fill_addon_constraints(constraint_set[constraint_key])
            elif constraint_key in self.addon_constraints:
                user_value = constraint_set[constraint_key] #ichip
                addon_keys = self.addon_constraints[constraint_key].keys() #ichip, bchip, trio
                if user_value in addon_keys: # ichip = ichip
                    for key in self.addon_constraints[constraint_key][user_value]:
                        constraint_set[key] = self.addon_constraints[constraint_key][user_value][key]
                    del constraint_set[constraint_key] # delete alias

    def _rest_call(self, command):
        '''
            rest call
        '''
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        kwargs = {}
        operation = 'get'
        formatter_func = None
        payload = None
        if type(command['cmd']) is dict:
            if 'operation' in command['cmd']:
                operation = command['cmd']['operation']
                if operation not in ['get', 'put', 'post', 'delete']:
                    self.__log('Skipping command ' + str(command) + ' due to illegal operation ' + operation)
                    return None
                del command['cmd']['operation']
            if 'output_formatter' in command['cmd']:
                if ':' not in command['cmd']['output_formatter']:
                    self.__log('Skipping output formatter; missing colon between library and function')
                else:
                    (lib1, function) = command['cmd']['output_formatter'].split(':', 1)
                    lib1 = lib1.replace('.py', '')
                    (module_location, module) = lib1.rsplit('/', 1)
                    sys.path.insert(0, module_location)
                    module = __import__(module)
                    formatter_func = getattr(module, function)
                del command['cmd']['output_formatter']
            if 'json' in command['cmd']:
                command['cmd']['data'] = json.dumps(command['cmd']['json'])
                payload = json.dumps(command['cmd']['json'], sort_keys=True, indent=4)
                del command['cmd']['json']
            for key in command['cmd']:
                if key == 'auth':
                    command['cmd'][key] = (command['cmd'][key]['user'], command['cmd'][key]['password'])
                kwargs[key] = command['cmd'][key]
        else:
            kwargs['url'] = command['cmd']
        rest_call = getattr(requests, operation)
        rest_response = None
        response = None
        try:
            rest_response = rest_call(**kwargs)
            response = rest_response.text
        except Exception as error:
            response = str(error)

        try:
            if rest_response.status_code == 200:
                #if json response, then cleanup with indents
                try:
                    response = str(json.dumps(rest_response.json(), sort_keys=True, indent=4))
                except Exception:
                    #not a json response, no problem, get what we can out of response
                    pass
                if formatter_func:
                    response = formatter_func(response)
            else:
                response = str(rest_response.status_code) + ":" + rest_response.reason + ":" + rest_response.text
                if payload:
                    response += "\nJSON delivered payload:\n" + payload
        except Exception:
            #use original error if status_code and other data could not be obtained
            pass
        return response

    def __log(self, message, resource=None):
        '''
            log
        '''
        if resource:
            self.loggers[resource].info(message)
        else:
            self.loggers['default'].info(message)


    def __setup_logger(self, name, log_file, level=logging.INFO):
        '''
            set up a logger
        '''
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger


    def __process_file_vars(self, macro_lib):
        '''
            process file vars
        '''
        match_obj = True
        while match_obj:
            match_obj = re.search(r'file\[\'?([\.\-\/a-zA-Z0-9_]*)\'?\]', macro_lib)
            if match_obj:
                match = match_obj.group(0)
                filename = match_obj.group(1)
                with open(filename, 'r') as fhandle:
                    file_content = fhandle.read()
                    fhandle.close()
                match = match.replace('[', '\[')
                match = match.replace("\'", "\\\'")
                match = match.replace(']', '\]')
                macro_lib = re.sub(match, file_content, macro_lib)
        return macro_lib

    def __system(self, command):
        '''
            system calls
        '''
        output = ''
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except Exception as error:
            output = str(error)
        output_list = str(output).split(sep='\\n')
        output = "\n".join(output_list)
        return output


##### Custom callbacks and dependent functions

    #learn target information from JUNOS devices
    def show_chassis_hardware(self, mode, resource, **constraints):
        '''
        callback function for targets
        '''
#        return_val = {}
#        return_val['vty'] = ['fpc0','fpc1']
#        return return_val
        if 'resource' not in self.resources_modules:
            self.resources_modules[resource] = []
            resp_json = cli(self.handles[resource], command='show chassis hardware | display json')
            resp_json = re.sub(r".*\n{", "{", resp_json) # a bit of cleanup from JUNOS CLI
            self._process_hardware_info(str(resp_json), resource)

        final_targets = []
        for module in self.resources_modules[resource]:
            module_match = True
            if not 'name' in module:
                continue
            possible_target = module['name'].replace(" ", "").lower()
            for constraint_key, constraint_value in constraints.items():
                #t.log_console("Check " + constraint_key + " in " + str(constraint_value))
                if constraint_key in module:
                    if type(constraint_value) is list:
                        if module[constraint_key] not in constraint_value:
                            module_match = False
                    elif not module[constraint_key].lower().startswith(constraint_value): #string compare
                        module_match = False
                elif constraint_key != 'function':
                    module_match = False
            if resource in self.user_targets and \
               mode in self.user_targets[resource] and \
               module['name'].replace(" ", "").lower() not in self.user_targets[resource][mode]:
                module_match = False
            if module_match is True:
                final_targets.append(possible_target)
        #t.log_console("final targets after show chassis hardware: " + str(final_targets))
        return final_targets

    def _process_hw_list(self, targets, resource):
        '''
            process hw list
        '''
        for item in targets:
            if type(item) is list:
                self._process_hw_list(item, resource)
            elif type(item) is dict:
                to_be_deleted = []
                chassis_sub_list = []
                target = {}
                for key in item:
                    if 'chassis' in key:
                        chassis_sub_list.append(item[key])
                    elif type(item[key]) is list:
                        if 'data' in item[key][0]:
                            target[key] = item[key][0]['data']
                        else:
                            target[key] = 'unknown'
                    else:
                        to_be_deleted.append(key)
                if target:
                    self.resources_modules[resource].append(target)
                for next_target in chassis_sub_list:
                    self._process_hw_list(next_target, resource)
                for key in to_be_deleted:
                    del item[key]

    def _process_hardware_info(self, json_content, resource):
        '''
            process hw info
        '''
        hardware = {}
        try:
            hardware = json.loads(json_content)
        except Exception:
            t.log_console("Unable to load show_chassis_hardware JSON content:\n" + json_content)
        if 'chassis-inventory' in hardware:
            self._process_hw_list(hardware['chassis-inventory'], resource)
        else:
            self.resources_modules[resource] = []
