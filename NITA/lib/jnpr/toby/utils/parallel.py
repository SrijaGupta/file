"""
Copyright (C) 2016-2017, Juniper Networks, Inc.
All rights reserved.
Authors: hgona, jpzhao

Description:
    Run In Parallel
"""

# pylint: disable=no-member,unused-import,no-self-use,trailing-whitespace

from robot.libraries.BuiltIn import BuiltIn
from jnpr.toby.utils.utils import run_multiple
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.engines.verification.verifyEngine import verifyEngine
from robot.running.context import EXECUTION_CONTEXTS
import importlib
import re
import copy
import sys

class parallel(object):
    '''
    parallel Class
    Contains run_in_parallel method and its utils
    '''

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        # stores all the job names and keywords
        self._jobs = {}
        self._jobs['default'] = {}
        # stores the user variables
        self._vars = {}
        self._vars['default'] = {}

    def run_in_parallel(self, *args):
        '''
        Run all keywords in paralle

        ARGUMENTS:
            [tasks, job]
            :param STR job:
                *MANDATORY/OPTIONAL* Mandatory when Tasks or keyword is not passed.
                                        Name of the Tasks
            :param STR tasks:
                *MANDATORY/OPTIONAL* Mandatory when job or keyword is not passed.
                                      Job name.
           
        ROBOT USAGE:
            Ex 1: run all keywords in parallel:
                Create Task   task=task1   $(res)   Config Engine    device_list=r0    config_file=some.cfg.yaml    commit=${True}     timeout=${30}
                Create Task   task=task2   $(res)   Config Engine    device_list=r0    config_file=some.cfg.yaml    commit=${True}     timeout=${30}
                Run In Parallel   tasks=task1,task2

            EX 2: Run In Parallel  job=<key - word>

            Ex 3: run set of keywords in serial and different sets in parallel
                (I)   Run In Parallel  job=my_job
                (II)  Run In Paralleorl  tasks=task1,task2
                (III) Run In Parallel  job=my_job  tasks=task1,task3
        '''
        job = None
        tasks = None
        
        
        if args and 'job' in args[0]:
            job = args[0].split("=")[1]
            args = args[1:]
        
        
        if args and 'tasks' in args[0]:
            tasks = args[0].split("=")[1]
            args = args[1:]
        
        # checking if keywords passed directly to Run In Parallel
        if not job and not tasks:
            if not args:
                raise TobyException("No keywords passed to run in parallel")
            result = self._run_all_tasks(None, None, *args)
        # checking for task names in args  
        elif not tasks:
            result = self._run_all_tasks(job=job)
        # checking for job name in args
        elif not job:
            result = self._run_all_tasks(tasks=tasks)
        # checking for specific tasks passed to run inside a job
        else:
            result = self._run_all_tasks(job=job, tasks=tasks)

        return result

    def create_job(self, job=None, tasks=None):
        '''
        Creates a job with given tasks.

        ARGUMENTS:
            [job=None, tasks=None]
            :param STR job:
                *MANDATORY* job name.Default will be set to None.
            :param STR tasks:
                *MANDATORY*task name.Default will be set to None.
        
        ROBOT USAGE:
            Create Job       job=job_name     tasks=task_name

        :retur:None else raise an exception.
        '''
        if isinstance(tasks, str):
            tasks = tasks.split(',')
        if job:
            # initializes a job
            self._jobs[job] = {}
            # initializes vars for a job
            self._vars[job] = {}
            if tasks:
                for task in tasks:
                    # checks if task name is defined
                    if task in self._jobs['default']:
                        self._vars[job][task] = {}
                        self._jobs[job][task] = []
                        self._jobs[job][task].extend(self._jobs['default'][task])
                    else:
                        raise TobyException("Task "+ task +" is not defined.")
        else:
            raise TobyException("Job name is not specified")

    def create_task(self, *args):
        '''
        Creates a Task and adds keywords passed to the task.

        DESCRIPTION:
            All the keyword names,args and kwargs are passed
            as args to this method with a delimeter('')

        ARGUMENTS:
            [*args]
            Args can be any toby or robot keywords with relavent arguments to it
        
        ROBOT USAGE:
            Create Task   task=task1
            ...  \  $(res)   Config Engine    device_list=r0    config_file=name.cfg.yaml
                    ...       cmd_list=template['a']   commit=${True}     timeout=${30}

        :return:None
        '''
    
        if not args:
            raise TobyException("No arguments passed to create task")
        
        # iterate through each arg and check for delimetter
        self._resolve_args('create', *args)
        
    def append_to_task(self, *args):
        '''
        Appends keywords passed to an existing task.

        DESCRIPTION:
            All the keyword names,args and kwargs are passed
            as args to this method with a delimeter('')

        ARGUMENTS:
            [*args]
        
        ROBOT USAGE:
            Append To Task   task=${router_handle}_add_rift

        :return:None
        '''
        if not args:
            raise TobyException("No arguments passed to append to the task")
        
        # iterate through each arg and check for delimetter
        self._resolve_args('append', *args)
        
    def _wrapped_f(self, *keyword_list, **tasks):
        '''
        Wrapped function passed to run_multiple.
        '''
        result = []
        if isinstance(keyword_list, dict):
            keyword_list = [keyword_list]
        for element in keyword_list:
            keyword = element.get('keyword').lower()
            args = element.get('args', [])
            kwargs = element.get('kwargs', {})
            task = tasks.get('task')
            job = tasks.get('job')
            # resolves vars in args
            args = tuple(self._resolve_vars(job=job, task=task, args=args))
            # resolves vars in kwargs
            kwargs = self._resolve_vars(job=job, task=task, args=kwargs)
            # Gets the library name of the keyword
            handle = self._get_handler_from_keyword(keyword)
            libname = handle.libname
            # Gets the library method instance of the keyword
            method = self._get_library_method(keyword)
            try:
                lib = self._get_library_instance(libname)
            except:
                raise TobyException("Library "+libname+" not found")
            # Runs the keyword and gets the result
            result = getattr(lib, "%s" % method)(*args, **kwargs)
            if result is False:
                return result
            # saves result in the var if given
            if 'var_name' in element:
                var_name = element['var_name']
                self._vars[job][task][var_name] = result
        return  True
                
    def _run_all_tasks(self, job='default', tasks=None, *args):
        '''
        Runs all the tasks in a job in parallel.
        '''
        targets = []
        # Checks if task names are inputted
        if tasks:
            # checks if tasks is a list
            try:
                tasks = eval(tasks)
            except (NameError, SyntaxError):
                pass
            # checks if tasks is string
            if isinstance(tasks, str):
                tasks = tasks.split(',')
            # parses tasks and gets the keywords, args and kwargs
            for task in tasks:
                target_dict = {}
                target_dict['target'] = self._wrapped_f
                list_args = self._jobs[job].get(task, [])
                if not list_args:
                    raise TobyException("Task "+ task +" is not defined")
                target_dict['args'] = []
                target_dict['args'].extend(list_args)
                target_dict['kwargs'] = {'job': job, 'task': task}
                targets.append(target_dict)
        # checks if a job name is inputted and parses tasks defined in it
        elif job is not 'default' and job:
            for task in self._jobs[job]:
                target_dict = {}
                target_dict['target'] = self._wrapped_f
                list_args = self._jobs[job].get(task)
                target_dict['args'] = []
                target_dict['args'].extend(list_args)
                target_dict['kwargs'] = {'job': job, 'task': task}
                targets.append(target_dict)
        # checks if keywords are passed directly to run in parallel
        elif args:
            targets = self._resolve_args('run', *args)
        else:
            raise TobyException("No arguments passed to run")
        # Creates threads, waits for thread execution to complete and returns results
        try:
            output = run_multiple(targets)
        except Exception as exp:
            raise TobyException("Unable to run one or more threads: %s" % exp)
        
        # Logs the output of the threads as a list
        t.log(output)
        
        # Raises Exception if any of the threads fail
        if False in output:
            raise TobyException("One or more tasks failed during execution")
        else:
            return output
    
    def _resolve_args(self, mode, *args):
 
        list_args = []
        kwargs = {}
        count = len(args)
        job = 'default'
        task = None
        targets = []
        t.log('debug', "Running on mode: %s" % mode)
        
        # iterate through each arg and check for delimetter
        for index, arg in enumerate(args):
            if isinstance(arg, str):
                # split the arg to check for kwarg
                arg = arg.split('=', 1)
            else:
                arg = [arg]
            # checking if arg is a kwarg
            if len(arg) == 2:
                if arg[1] != 'set':
                    try:
                        # evaluates lists and dictionaries
                        arg[1] = eval(arg[1])
                    except:
                        # catching exception if arg is a string
                        pass
                kwargs[arg[0]] = arg[1]
            # checking if arg is a list arg and it is not empty
            elif len(arg) == 1 and arg[0]:
                list_args.append(arg[0])
            # checking if arg is empty(delimeter) or is the last arg
            if not arg[0] or index == count-1:
                if 'job' in kwargs:
                    job = kwargs.pop('job')
                if 'task' in kwargs:
                    task = kwargs.pop('task')
                    # Checks and raises exception if job name is not passed
                    if job not in self._jobs:
                        raise TobyException("Job "+job+" is not defined")
                    # creates a new task
                    if mode=='create':
                        self._jobs[job][task] = []
                        self._vars[job][task] = {}
                    # appends to task if exists or creates new
                    else:
                        if task not in self._jobs[job]:
                            self._jobs[job][task] = []
                            self._vars[job][task] = {}
                # Raises exception if task name is not passed
                if not task and mode!='run':
                    raise TobyException('Task name is not defined')
                if list_args:
                    list_args = tuple(list_args)
                    keyword = list_args[0]
                    list_args = list_args[1:]
                    # matches the var name passed as "$(var_name)" 
                    match = re.match(r'^\$\((\w*)\)\s?=?', keyword)
                    if match:
                        var_name = match.group(1)
                        keyword = list_args[0]
                        list_args = list_args[1:]
                        task_element = {'keyword': keyword, 'args': list_args, 'kwargs': kwargs, 'var_name': var_name}
                    else:
                        task_element = {'keyword': keyword, 'args': list_args, 'kwargs': kwargs}
                    if task:
                        self._jobs[job][task].append(task_element)
                    else:
                        target_dict = {}
                        target_dict['target'] = self._wrapped_f
                        target_dict['args'] = [task_element]
                        targets.append(target_dict)
                    list_args = []
                    kwargs = {}
                     
        return targets

    def get_var_from_task(self, job='default', task=None, var=None):
        '''
        Get Var from the specified Job and/or Tasks

        ARGUMENTS:
            [job='default', task=None, var=None]
            :param STR job:
                *OPTIONAL* job name.Default is set to "default".
            :param STR task:
                *MANDATORY* name of the task.To get var details.
                            Default is set to None.
            :param STR var:
                *MANDATORY* Name of the var.Default is set to None.

        ROBOT USAGE:
            Run In Parallel   tasks=task1,task2,task3,task4
            ${res} =  Get Var From Task  task=task1  var=$(res)

        :return:return vars. else raise exception.
        '''
        if not task:
            raise TobyException("Task name need to be passed get var")
        if not var:
            raise TobyException("Variable name need to be passed get var")
        match = re.match(r'^\$\((\w*)\)\s?', var)
        if match:
            var_name = match.group(1)
        else:
            var_name = var
        if task not in self._vars[job]:
            raise TobyException("Task "+task+" is not defined")
        if var_name not in self._vars[job][task]:
            raise TobyException("Variable "+var+" is not defined")
        return self._vars[job][task][var_name]

    def _get_library_instance(self, libname):
        '''
        Gets library instance from library name.
        '''
        if libname == 'init':
            return t
        elif libname == 'verification':
            ve_obj = BuiltIn().get_library_instance('verifyEngine')
            lib = globals()['verifyEngine']()
            if ve_obj.verification_file:
                lib.verification_file = ve_obj.verification_file
                lib.tmpl_data = copy.deepcopy(ve_obj.tmpl_data)
                lib.pylib = copy.deepcopy(ve_obj.pylib)
                lib.ve_data = copy.deepcopy(ve_obj.ve_data)
                lib.tmpl_file = ve_obj.tmpl_file
        elif importlib.util.find_spec(libname):
            obj = BuiltIn().get_library_instance(libname)
            try:
                lib = copy.deepcopy(obj)
            except:
                lib = importlib.import_module(libname)
                if hasattr(lib, libname):
                    lib = getattr(lib, libname)()
        else:
            lib = BuiltIn().get_library_instance(libname)

        return lib

    def _get_library_method(self, keyword):
        '''
        Gets library method of a library keyword.
        '''
        if keyword == 'verify':
            method = keyword + "_specific_checks_api"
        elif keyword == 'get':
            method = keyword + "_specific_data"
        else:
            keyword = keyword.replace(' ', '_')
            mat = re.match(r"(.+\.)*(.+)", keyword)
            method = mat.group(2)
            
        return method
 

    def _resolve_vars(self, job=None, task=None, args=[]):
        '''
        Resolves variables used inside a task.
        '''
        if isinstance(args, tuple):
            args = list(args)
        for k, val in enumerate(args):
            if isinstance(val, str):
                match = re.match(r'^\$\((\w*)\)', val)
                if match:
                    var_name = match.group(1)
                    if var_name in self._vars[job][task]:
                        args[k] = self._vars[job][task][var_name]
                    else:
                        raise TobyException("Variable " +val+ " is not defined")
        return args

    def _get_handler_from_keyword(self, keyword):
        ''' Gets the Robot Framework handler associated with the given keyword '''
        if EXECUTION_CONTEXTS.current is None:
            raise RobotNotRunningError('Cannot access execution context')
        return EXECUTION_CONTEXTS.current.get_runner(keyword)
